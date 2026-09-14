#!/usr/bin/env python3
"""Mechanical audit of docs/AGENT_ACTIVITY.jsonl.

Computes line/parse stats, key census, timestamp monotonicity, agent and
action distributions, sensitive-path mentions (values masked after '='),
and a raw-byte credential scan. Credential hits report ONLY line numbers;
matched text is never printed or stored.

Writes out/activity-audit.json and out/activity-audit.md.
"""
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone

SOURCE = "docs/AGENT_ACTIVITY.jsonl"
OUT_DIR = "out"
OUT_JSON = os.path.join(OUT_DIR, "activity-audit.json")
OUT_MD = os.path.join(OUT_DIR, "activity-audit.md")
MD_MAX_ACTION_ROWS = 25

CRED_PATTERNS = [
    ("hex_prefixed_api_key", rb"sk-[0-9a-f]{32}"),
    ("hex32_dot_long_token", rb"[0-9a-f]{32}\.[A-Za-z0-9_-]{20,}"),
]
SENSITIVE_MARKERS = [".env", "key.txt", "uploads/"]

TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}")
AGENT_CANDIDATES = ["agent", "actor", "role", "user", "author"]
ACTION_CANDIDATES = ["action", "action_kind", "kind", "operation", "op", "event_type"]
PATHS_CANDIDATES = ["paths", "path", "files", "targets"]

KIND_RULE = (
    "Heuristic mapping from the free-text action field: 'GitHub fetch[/returned]' "
    "-> read-remote; other 'GitHub ...' -> modify-remote; 'Publisher Git ...' -> "
    "local-git; first word Run/Verify/Probe/Test -> test; first word Inspect/Read/"
    "Check/Locate/Search/Determine/List -> read; everything else -> write-or-record."
)

LIMITS_PARAGRAPH = (
    "These patterns would not catch: credentials whose shape differs from the two "
    "regexes - high-entropy tokens without a recognizable prefix or length, "
    "base64- or hex-only secrets, keys split across two lines, secrets inside "
    "non-UTF-8 or binary encodings, or values hidden behind environment-variable "
    "or config-file indirection where only the variable name (for example "
    "DEEPSEEK_API_KEY, which appears in action text here) is logged; sensitive "
    "files that were touched without any path entry at all, since the audit can "
    "only inspect records that exist; action strings that lie about what "
    "actually ran, because the action-kind tally trusts self-reported text and "
    "never executes or diffs anything; mild timeline forgery, because a "
    "non-decreasing timestamp check ignores equal-timestamp interleavings and "
    "cannot prove wall-clock truth (the two decreases found here are "
    "microsecond-level concurrent-append reorderings, not evidence of "
    "backdating); and whether a sensitive path name such as '.env' or "
    "'uploads/' actually leaked a secret, since the path scan sees names only, "
    "not file contents. In short, the audit verifies the shape and hygiene of "
    "the log itself, not the truthfulness of the actions it records."
)


def parse_iso(s):
    v = s.strip()
    if v.endswith("Z"):
        v = v[:-1] + "+00:00"
    dt = datetime.fromisoformat(v)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def detect_field(records, candidates):
    counts = Counter()
    for _, rec in records:
        for c in candidates:
            if c in rec:
                counts[c] += 1
    if not counts:
        return None
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def classify_action(action):
    a = action.strip().lower()
    if a.startswith("github fetch"):
        return "read-remote"
    if a.startswith("github "):
        return "modify-remote"
    if a.startswith("publisher git"):
        return "local-git"
    parts = a.split(None, 1)
    first = parts[0] if parts else ""
    if first in ("run", "verify", "probe", "test"):
        return "test"
    if first in ("inspect", "read", "check", "locate", "search", "determine", "list"):
        return "read"
    return "write-or-record"


def mask_equals(value):
    s = str(value)
    if "=" in s:
        return s[: s.index("=")] + "=***MASKED***"
    return s


def esc(cell):
    return str(cell).replace("|", "\\|")


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(" --- " for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(esc(c) for c in r) + " |")
    return "\n".join(out)


def audit():
    with open(SOURCE, "rb") as fh:
        raw = fh.read()
    raw_lines = raw.split(b"\n")
    if raw_lines and raw_lines[-1] == b"":
        raw_lines = raw_lines[:-1]
    line_count = len(raw_lines)

    blank, nonparse = [], []
    records = []
    for i, bl in enumerate(raw_lines, 1):
        if bl.strip() == b"":
            blank.append(i)
            continue
        try:
            obj = json.loads(bl.decode("utf-8"))
        except Exception:
            nonparse.append(i)
            continue
        if not isinstance(obj, dict):
            nonparse.append(i)
            continue
        records.append((i, obj))

    key_counts = Counter()
    for _, rec in records:
        for k in rec:
            key_counts[k] += 1

    # Timestamp field: key whose string values most often parse as ISO-8601.
    tcounts = {}
    for _, rec in records:
        for k, v in rec.items():
            if isinstance(v, str) and TS_RE.match(v):
                try:
                    parse_iso(v)
                except ValueError:
                    continue
                tcounts[k] = tcounts.get(k, 0) + 1
    ts_field = (
        sorted(tcounts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        if tcounts else None
    )

    ts_entries, ts_bad = [], []
    if ts_field:
        for ln, rec in records:
            if ts_field not in rec:
                continue
            v = rec[ts_field]
            if isinstance(v, str):
                try:
                    ts_entries.append((ln, v, parse_iso(v)))
                except ValueError:
                    ts_bad.append(ln)
            else:
                ts_bad.append(ln)
    decreases = []
    for prev, cur in zip(ts_entries, ts_entries[1:]):
        if cur[2] < prev[2]:
            decreases.append({
                "line": cur[0],
                "value": cur[1],
                "previous_line": prev[0],
                "previous_value": prev[1],
            })

    agent_field = detect_field(records, AGENT_CANDIDATES)
    action_field = detect_field(records, ACTION_CANDIDATES)
    paths_field = detect_field(records, PATHS_CANDIDATES)

    agent_counts = Counter(
        str(rec[agent_field]) for _, rec in records
        if agent_field and agent_field in rec
    )
    action_counts = Counter(
        str(rec[action_field]) for _, rec in records
        if action_field and action_field in rec
    )
    kind_counts = Counter(classify_action(a) for a in action_counts.elements())

    hits = []
    if paths_field:
        for ln, rec in records:
            val = rec.get(paths_field)
            vals = val if isinstance(val, list) else ([val] if val is not None else [])
            matched = []
            for v in vals:
                s = str(v)
                ms = [m for m in SENSITIVE_MARKERS if m in s]
                if ms:
                    matched.append({"markers": ms, "value": mask_equals(s)})
            if matched:
                hits.append({"line": ln, "field": paths_field, "entries": matched})

    cred_hits = set()
    for i, bl in enumerate(raw_lines, 1):
        for _, pat in CRED_PATTERNS:
            if re.search(pat, bl):
                cred_hits.add(i)
                break
    cred_hits = sorted(cred_hits)

    last10 = []
    for ln, rec in records[-10:]:
        pv = rec.get(paths_field) if paths_field else None
        pl = pv if isinstance(pv, list) else ([pv] if pv else [])
        last10.append({
            "line": ln,
            "timestamp": rec.get(ts_field, "") if ts_field else "",
            "agent": rec.get(agent_field, "") if agent_field else "",
            "action": rec.get(action_field, "") if action_field else "",
            "first_path": str(pl[0]) if pl else "",
        })

    ordered = lambda c: dict(sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))
    result = {
        "source": SOURCE,
        "generator": "check/audit_activity.py",
        "file_bytes": len(raw),
        "line_count": line_count,
        "json_object_lines": len(records),
        "non_parse_line_numbers": nonparse,
        "blank_line_numbers": blank,
        "top_level_keys": ordered(key_counts),
        "timestamp": {
            "field": ts_field,
            "records_with_field": len(ts_entries),
            "records_with_unparseable_value": ts_bad,
            "first": ({"line": ts_entries[0][0], "value": ts_entries[0][1]}
                      if ts_entries else None),
            "last": ({"line": ts_entries[-1][0], "value": ts_entries[-1][1]}
                     if ts_entries else None),
            "non_decreasing": not decreases,
            "decreases": decreases,
        },
        "agents": {
            "field": agent_field,
            "distinct_values": len(agent_counts),
            "counts": ordered(agent_counts),
        },
        "actions": {
            "field": action_field,
            "distinct_values": len(action_counts),
            "counts": ordered(action_counts),
        },
        "action_kinds_derived": {"rule": KIND_RULE, "counts": ordered(kind_counts)},
        "sensitive_path_mentions": {
            "field": paths_field,
            "markers": SENSITIVE_MARKERS,
            "hit_count": len(hits),
            "hit_lines": [h["line"] for h in hits],
            "hits": hits,
            "masking": "text after the first '=' in each matched value replaced with ***MASKED***",
        },
        "credential_scan": {
            "scope": "raw bytes, per line",
            "patterns": [{"name": n, "regex": p.decode()} for n, p in CRED_PATTERNS],
            "hit_count": len(cred_hits),
            "hit_line_numbers": cred_hits,
            "note": "line numbers only; matched text intentionally never reported",
        },
        "last_ten_records": last10,
        "pattern_limits": LIMITS_PARAGRAPH,
    }
    return result


def render_md(r):
    b = []
    b.append("# Mechanical audit of `docs/AGENT_ACTIVITY.jsonl`")
    b.append("")
    b.append("Generated by `check/audit_activity.py` from `%s` (%d bytes)." % (r["source"], r["file_bytes"]))
    b.append("")
    b.append("## 1. Lines and parsing")
    b.append("")
    b.append(md_table(["metric", "value"], [
        ["total lines", r["line_count"]],
        ["lines parsing as JSON objects", r["json_object_lines"]],
        ["non-parse lines", len(r["non_parse_line_numbers"])],
        ["non-parse line numbers", ", ".join(map(str, r["non_parse_line_numbers"])) or "none"],
        ["blank lines", len(r["blank_line_numbers"])],
        ["blank line numbers", ", ".join(map(str, r["blank_line_numbers"])) or "none"],
    ]))
    b.append("")
    b.append("## 2. Top-level keys")
    b.append("")
    b.append(md_table(["key", "records carrying it"], r["top_level_keys"].items()))
    b.append("")
    ts = r["timestamp"]
    b.append("## 3. Timestamp field")
    b.append("")
    b.append(md_table(["metric", "value"], [
        ["field name", "`%s`" % ts["field"]],
        ["records with parseable value", ts["records_with_field"]],
        ["first value (line %s)" % ts["first"]["line"], ts["first"]["value"]],
        ["last value (line %s)" % ts["last"]["line"], ts["last"]["value"]],
        ["sequence non-decreasing", ts["non_decreasing"]],
        ["decrease count", len(ts["decreases"])],
        ["unparseable timestamp lines", ", ".join(map(str, ts["records_with_unparseable_value"])) or "none"],
    ]))
    if ts["decreases"]:
        b.append("")
        b.append(md_table(
            ["line", "value", "previous line", "previous value"],
            [[d["line"], d["value"], d["previous_line"], d["previous_value"]]
             for d in ts["decreases"]],
        ))
    b.append("")
    b.append("## 4. Agent / role field `%s`" % r["agents"]["field"])
    b.append("")
    b.append("%d distinct values:" % r["agents"]["distinct_values"])
    b.append("")
    b.append(md_table(["value", "count"], r["agents"]["counts"].items()))
    b.append("")
    b.append("## 5. Action-kind field `%s`" % r["actions"]["field"])
    b.append("")
    b.append("%d distinct values. Coarse classification (heuristic, see JSON `action_kinds_derived.rule`):" % r["actions"]["distinct_values"])
    b.append("")
    b.append(md_table(["derived kind", "count"], r["action_kinds_derived"]["counts"].items()))
    b.append("")
    action_items = list(r["actions"]["counts"].items())
    shown = action_items[:MD_MAX_ACTION_ROWS]
    b.append("Distinct action values (top %d of %d by count; full map in the JSON):" % (
        len(shown), len(action_items)))
    b.append("")
    rows = list(shown)
    omitted = len(action_items) - len(shown)
    if omitted:
        rows.append(["... (%d more values omitted; see JSON)" % omitted, ""])
    b.append(md_table(["action", "count"], rows))
    b.append("")
    sp = r["sensitive_path_mentions"]
    b.append("## 6. Sensitive path mentions in `%s`" % sp["field"])
    b.append("")
    b.append("Markers: %s. Values shown with text after `=` masked." %
             ", ".join("`%s`" % m for m in sp["markers"]))
    b.append("")
    if sp["hits"]:
        rows = []
        for h in sp["hits"]:
            for e in h["entries"]:
                rows.append([h["line"], ", ".join(e["markers"]), e["value"]])
        b.append(md_table(["line", "markers", "value (masked)"], rows))
    else:
        b.append("No hits (line numbers: none).")
    b.append("")
    cs = r["credential_scan"]
    b.append("## 7. Credential scan over raw bytes")
    b.append("")
    b.append(md_table(["pattern", "regex"],
                      [[p["name"], "`%s`" % p["regex"]] for p in cs["patterns"]]))
    b.append("")
    b.append(md_table(["metric", "value"], [
        ["hit count", cs["hit_count"]],
        ["hit line numbers", ", ".join(map(str, cs["hit_line_numbers"])) or "none"],
    ]))
    b.append("")
    b.append("Matched text is deliberately never reported; line numbers only.")
    b.append("")
    b.append("## 8. Last ten records")
    b.append("")
    b.append(md_table(
        ["line", "timestamp", "agent", "action", "first path"],
        [[x["line"], x["timestamp"], x["agent"], x["action"], x["first_path"]]
         for x in r["last_ten_records"]],
    ))
    b.append("")
    b.append("## What the patterns would not catch")
    b.append("")
    b.append(r["pattern_limits"])
    b.append("")
    return "\n".join(b)


def main():
    result = audit()
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
        fh.write("\n")
    with open(OUT_MD, "w", encoding="utf-8") as fh:
        fh.write(render_md(result))
    print("wrote %s and %s" % (OUT_JSON, OUT_MD))
    print("lines=%d parsed=%d nonparse=%d blank=%d" % (
        result["line_count"], result["json_object_lines"],
        len(result["non_parse_line_numbers"]), len(result["blank_line_numbers"])))
    print("timestamp field=%s non_decreasing=%s decreases=%d" % (
        result["timestamp"]["field"], result["timestamp"]["non_decreasing"],
        len(result["timestamp"]["decreases"])))
    print("sensitive path hit lines=%d credential hit lines=%d" % (
        result["sensitive_path_mentions"]["hit_count"],
        result["credential_scan"]["hit_count"]))


if __name__ == "__main__":
    main()
