"""Independent verification of out/ledger-audit.json against raw bytes.

Recomputes every audited quantity WITHOUT importing check/common.py, then
compares against the written JSON. Also checks the markdown exists and that
neither output contains anything matching the credential patterns
(only line numbers may appear; matched text must never be printed).

Exits 0 on PASS, 1 on FAIL.
"""
import json
import os
import re
import sys

LEDGER = os.path.join("docs", "DECISION_LEDGER.md")
OUT_JSON = os.path.join("out", "ledger-audit.json")
OUT_MD = os.path.join("out", "ledger-audit.md")

rec_re = re.compile(r"REC-\d{8}-[A-Z]+")
vt_re = re.compile(r"VERIFIED ([0-9a-f]{40}) TREE ([0-9a-f]{40})")
cred1 = re.compile(r"sk-[0-9a-f]{32}")
cred2 = re.compile(r"[0-9a-f]{32}\.[A-Za-z0-9_-]{20,}")


def fail(msg):
    print("FAIL: " + msg)
    sys.exit(1)


def main():
    raw = open(LEDGER, "rb").read()
    audit = json.load(open(OUT_JSON, encoding="utf-8"))

    # independent census
    total = raw.count(b"\n") + (0 if raw.endswith(b"\n") else 1)
    crlf_count = raw.count(b"\r\n")
    bare_lf_count = raw.count(b"\n") - crlf_count
    crlf_lines = [i + 1 for i, seg in enumerate(raw.split(b"\n"))
                  if seg.endswith(b"\r")]
    if raw.endswith(b"\n") and crlf_lines and crlf_lines[-1] == raw.count(b"\n") + 1:
        fail("phantom trailing segment counted")

    c = audit["line_census"]
    assert c["total_lines"] == total, "total_lines"
    assert c["crlf_line_count"] == crlf_count, "crlf_line_count"
    assert c["bare_lf_line_count"] == bare_lf_count, "bare_lf_line_count"
    assert c["crlf_line_numbers"] == crlf_lines, "crlf_line_numbers"

    text_lines = raw.decode("utf-8").split("\n")
    if text_lines and text_lines[-1] == "":
        text_lines = text_lines[:-1]
    contents = [ln[:-1] if ln.endswith("\r") else ln for ln in text_lines]

    # independent receipt ids
    first = {}
    counts = {}
    for i, ln in enumerate(contents, 1):
        ids_here = set()
        for m in rec_re.finditer(ln):
            ids_here.add(m.group(0))
            if m.group(0) not in first:
                first[m.group(0)] = i
        for rid in ids_here:
            counts[rid] = counts.get(rid, 0) + 1
    rows = audit["receipt_ids"]["ids"]
    assert audit["receipt_ids"]["distinct_count"] == len(first)
    assert [r["id"] for r in rows] == list(first.keys())
    for r in rows:
        assert r["first_appearance_line"] == first[r["id"]]
        assert r["lines_carrying_id"] == counts[r["id"]]

    # independent today's receipts
    pref = "REC-20260914-"
    todays = [r["id"] for r in rows if r["id"].startswith(pref)]
    t = audit["today_receipts"]
    assert t["count_distinct_ids"] == len(todays)
    assert [r["id"] for r in t["ids_in_first_appearance_order"]] == todays
    letters = [rid[len(pref):] for rid in todays]
    assert t["letter_sequence_first_appearance"] == letters
    singles = sorted({s for s in letters if len(s) == 1})
    full = singles == [chr(x) for x in range(65, 91)]
    assert t["a_to_z_fully_used"] is full
    multi = [rid for rid in todays if len(rid) > len(pref) + 1]
    assert t["two_letter_or_longer_suffix_exists"] is bool(multi)
    assert t["two_letter_or_longer_ids"] == multi

    # independent entry counts
    a = [i for i, ln in enumerate(contents, 1) if ln.startswith("REC-")]
    b = [i for i, ln in enumerate(contents, 1)
         if ln.startswith("REC-") or ln.startswith("**REC-")]
    blocks, cur = [], []
    for i, ln in enumerate(contents, 1):
        if ln.strip() == "":
            if cur:
                blocks.append(cur)
                cur = []
        else:
            cur.append((i, ln))
    if cur:
        blocks.append(cur)
    cblk = []
    for blk in blocks:
        bt = "\n".join(x for _, x in blk).lstrip()
        ft = bt.split(None, 1)[0] if bt else ""
        if ft.startswith("REC-") or ft.startswith("**REC-"):
            cblk.append(blk[0][0])
    e = audit["entry_counts"]
    assert e["definition_a"]["count"] == len(a) and e["definition_a"]["line_numbers"] == a
    assert e["definition_b"]["count"] == len(b) and e["definition_b"]["line_numbers"] == b
    assert e["definition_c"]["count"] == len(cblk) and e["definition_c"]["first_line_numbers"] == cblk

    # independent marker
    hits = [i for i, ln in enumerate(contents, 1)
            if "Prior verified commit/tree:" in ln]
    p = audit["prior_verified_marker"]
    assert p["line_count"] == len(hits) and p["line_numbers"] == hits

    # independent verified-tree lines
    ids_by_line = {i: rec_re.findall(ln) for i, ln in enumerate(contents, 1)}
    vt = []
    for i, ln in enumerate(contents, 1):
        m = vt_re.search(ln)
        if not m:
            continue
        near = None
        for j in range(i - 1, 0, -1):
            cand = ids_by_line[j]
            if cand:
                near = (cand[-1], j)
                break
        vt.append((i, m.group(1), m.group(2), near))
    v = audit["verified_tree_lines"]
    assert v["count"] == len(vt)
    assert len(v["matches"]) == len(vt)
    for (i, com, tree, near), got in zip(vt, v["matches"]):
        assert got["line"] == i and got["commit"] == com and got["tree"] == tree
        if near is None:
            assert got["nearest_receipt_above"] is None
        else:
            assert got["nearest_receipt_above"] == near[0]
            assert got["nearest_receipt_line"] == near[1]
    if vt:
        assert v["last_match"]["line"] == vt[-1][0]
        assert v["last_match"]["commit"] == vt[-1][1]
        assert v["last_match"]["tree"] == vt[-1][2]
        near = vt[-1][3]
        if near is None:
            assert v["last_match"]["nearest_receipt_above"] is None
        else:
            assert v["last_match"]["nearest_receipt_above"] == near[0]
    else:
        assert v["last_match"] is None

    # independent credential scan (ledger)
    cred_hits = [i for i, ln in enumerate(contents, 1)
                 if cred1.search(ln) or cred2.search(ln)]
    cs = audit["credential_scan"]
    assert cs["hit_line_count"] == len(cred_hits)
    assert cs["hit_line_numbers"] == cred_hits

    # independent last five
    last = audit["last_five_lines"]
    assert len(last) == min(5, len(contents))
    n_all = len(contents)
    expected = contents[-5:]
    for item, exp in zip(last, expected):
        assert item["content"] == exp
    assert [item["line"] for item in last] == list(range(n_all - len(expected) + 1, n_all + 1))

    # outputs must not themselves contain strings matching the credential patterns
    assert os.path.exists(OUT_MD), "markdown output missing"
    md_text = open(OUT_MD, encoding="utf-8").read()
    j_text = open(OUT_JSON, encoding="utf-8").read()
    for blob, name in ((md_text, OUT_MD), (j_text, OUT_JSON)):
        if cred1.search(blob) or cred2.search(blob):
            fail("%s contains a credential-shaped string (not printing it)" % name)

    print("PASS: out/ledger-audit.json matches an independent recomputation; "
          "credential scans clean (counts only).")


if __name__ == "__main__":
    main()
