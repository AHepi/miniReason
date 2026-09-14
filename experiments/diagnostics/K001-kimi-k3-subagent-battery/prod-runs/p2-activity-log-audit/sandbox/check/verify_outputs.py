#!/usr/bin/env python3
"""Verify out/activity-audit.json and out/activity-audit.md against the source.

Recomputes every reported value from docs/AGENT_ACTIVITY.jsonl by independent
assertion, checks markdown/JSON agreement, validates the masking helper, and
guarantees that neither output file contains any credential-shaped string.
Exits non-zero on any failure. Prints only counts and booleans; never prints
any matched credential text.
"""
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone

SOURCE = "docs/AGENT_ACTIVITY.jsonl"
OUT_JSON = "out/activity-audit.json"
OUT_MD = "out/activity-audit.md"

CRED_PATTERN = rb"sk-[0-9a-f]{32}|[0-9a-f]{32}\.[A-Za-z0-9_-]{20,}"
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}")
SENSITIVE = [".env", "key.txt", "uploads/"]
MASKED = "***MASKED***"
REQUIRED_TOP_KEYS = [
    "source", "generator", "file_bytes", "line_count", "json_object_lines",
    "non_parse_line_numbers", "blank_line_numbers", "top_level_keys",
    "timestamp", "agents", "actions", "action_kinds_derived",
    "sensitive_path_mentions", "credential_scan", "last_ten_records",
    "pattern_limits",
]

failures = []
passes = 0


def check(cond, name):
    global passes
    print(("PASS" if cond else "FAIL"), name)
    if cond:
        passes += 1
    else:
        failures.append(name)


def parse_iso(s):
    v = s.strip()
    if v.endswith("Z"):
        v = v[:-1] + "+00:00"
    dt = datetime.fromisoformat(v)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def mask_equals(value):
    s = str(value)
    if "=" in s:
        return s[: s.index("=")] + "=" + MASKED
    return s


def main():
    raw = open(SOURCE, "rb").read()
    raw_lines = raw.split(b"\n")
    if raw_lines and raw_lines[-1] == b"":
        raw_lines = raw_lines[:-1]

    data = json.load(open(OUT_JSON, "r", encoding="utf-8"))
    md = open(OUT_MD, "r", encoding="utf-8").read()
    json_bytes = open(OUT_JSON, "rb").read()
    md_bytes = open(OUT_MD, "rb").read()

    # 0. Schema keys present.
    check(all(k in data for k in REQUIRED_TOP_KEYS), "json has all named top-level keys")

    # 1. Lines / parsing.
    recs = []
    blank, nonparse = [], []
    for i, bl in enumerate(raw_lines, 1):
        if bl.strip() == b"":
            blank.append(i)
            continue
        try:
            o = json.loads(bl.decode("utf-8"))
            assert isinstance(o, dict)
            recs.append(o)
        except Exception:
            nonparse.append(i)
    check(data["line_count"] == len(raw_lines) == 2097, "line count matches source")
    check(data["json_object_lines"] == len(recs) == 2097, "parsed object count matches source")
    check(data["blank_line_numbers"] == blank == [], "blank line numbers match source")
    check(data["non_parse_line_numbers"] == nonparse == [], "non-parse line numbers match source")
    check(data["file_bytes"] == len(raw) == 1098223, "file byte count matches source")

    # 2. Key census.
    kc = Counter()
    for r in recs:
        for k in r:
            kc[k] += 1
    check(Counter(data["top_level_keys"]) == kc, "top-level key counts match source")
    check(len(data["top_level_keys"]) == 13, "thirteen distinct top-level keys")

    # 3. Timestamp sequence.
    ts = data["timestamp"]
    check(ts["field"] == "timestamp_utc", "timestamp field name found from data")
    parsed = [(i, r["timestamp_utc"], parse_iso(r["timestamp_utc"]))
              for i, r in enumerate(recs, 1) if isinstance(r.get("timestamp_utc"), str)]
    check(ts["records_with_field"] == len(parsed) == 2097, "all records carry parseable timestamps")
    check(ts["records_with_unparseable_value"] == [], "no unparseable timestamps")
    check(ts["first"]["line"] == 1 and ts["first"]["value"] == parsed[0][1], "first timestamp matches")
    check(ts["last"]["line"] == len(raw_lines) and ts["last"]["value"] == parsed[-1][1],
          "last timestamp matches")
    dec = []
    for p, c in zip(parsed, parsed[1:]):
        if c[2] < p[2]:
            dec.append({"line": c[0], "value": c[1],
                        "previous_line": p[0], "previous_value": p[1]})
    check(ts["decreases"] == dec, "decrease list recomputed exactly")
    check(len(dec) == 2 and [d["line"] for d in dec] == [802, 1000],
          "two decreases at lines 802 and 1000")
    check(ts["non_decreasing"] is False, "non-decreasing flag is False")
    check(all(TS_RE.match(v) for _, v, _ in parsed), "timestamp shape regex consistent")

    # 4. Agent counts.
    ac = Counter(str(r["agent"]) for r in recs)
    check(Counter(data["agents"]["counts"]) == ac, "agent counts match source")
    check(data["agents"]["field"] == "agent", "agent field name")
    check(data["agents"]["distinct_values"] == len(ac) == 31, "31 distinct agent values")
    check(ac["/root"] + ac["root"] == 1295, "root forms carry 1295 records")

    # 5. Action counts.
    xc = Counter(str(r["action"]) for r in recs)
    check(Counter(data["actions"]["counts"]) == xc, "action counts match source")
    check(data["actions"]["distinct_values"] == len(xc) == 969, "969 distinct action values")
    kk = data["action_kinds_derived"]["counts"]
    check(sum(kk.values()) == 2097, "derived action kinds total all records")

    # 6. Sensitive paths.
    hits = []
    for i, r in enumerate(recs, 1):
        for v in r.get("paths", []):
            s = str(v)
            if any(m in s for m in SENSITIVE):
                hits.append(i)
    sp = data["sensitive_path_mentions"]
    check(sp["hit_lines"] == hits == [], "sensitive path hit lines match source (none)")
    check(sp["hit_count"] == 0, "sensitive path hit count zero")
    # Masking helper behavior.
    assert mask_equals("a=b=c") == "a=" + MASKED
    assert mask_equals("token=xyz") == "token=" + MASKED
    assert mask_equals("plain/path") == "plain/path"
    assert mask_equals("") == ""
    check(True, "mask_equals masks after first '=' only")
    check(sp["hits"] == [], "no masked-hit entries needed when there are no hits")

    # 7. Credential scan.
    chits = sorted(i for i, bl in enumerate(raw_lines, 1) if re.search(CRED_PATTERN, bl))
    cs = data["credential_scan"]
    check(cs["hit_line_numbers"] == chits == [], "credential hit lines match source (none)")
    check(cs["hit_count"] == 0, "credential hit count zero")
    # Outputs themselves must contain no credential-shaped strings.
    check(re.search(CRED_PATTERN, json_bytes) is None, "json output contains no credential-shaped string")
    check(re.search(CRED_PATTERN, md_bytes) is None, "md output contains no credential-shaped string")

    # 8. Last ten records.
    want = []
    for i, r in list(enumerate(recs, 1))[-10:]:
        pl = r.get("paths", [])
        want.append({"line": i, "timestamp": r["timestamp_utc"], "agent": r["agent"],
                     "action": r["action"], "first_path": str(pl[0]) if pl else ""})
    check(data["last_ten_records"] == want, "last ten records recomputed exactly")
    check(all(data["last_ten_records"][j]["line"] == 2088 + j for j in range(10)),
          "last ten line numbers are 2088..2097")

    # Markdown agreements.
    check(str(data["line_count"]) in md and "timestamp_utc" in md, "md includes core values")
    check("| 802 |" in md and "| 1000 |" in md, "md lists both decrease lines")
    check("publisher-occ03" in md, "md last-ten rows present")
    check("What the patterns would not catch" in md, "md ends section present")
    check(md.rstrip().endswith("it records."), "md ends with limits paragraph")

    if failures:
        print("\n%d FAILURES: %s" % (len(failures), failures))
        sys.exit(1)
    print("\nall %d checks passed" % passes)


if __name__ == "__main__":
    main()
