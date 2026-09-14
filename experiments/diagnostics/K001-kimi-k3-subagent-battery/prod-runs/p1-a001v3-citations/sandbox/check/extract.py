#!/usr/bin/env python3
"""Step 1: verify the FW5 sha256, extract every citation by pattern, report
counts, and dump the raw hits to out/extracted.json for the verdict step."""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from citecommon import (EXPECTED_SHA, SRC, STAGING, CIT_RE_TEXT, extract_citations,
                        load_lines, sha256_of)

os.makedirs("out", exist_ok=True)

# step 0: sha256 of the designated reading edition
sha = sha256_of(SRC)
print(f"source bytes: {os.path.getsize(SRC)}")
print(f"computed sha256: {sha}")
print(f"designated sha256: {EXPECTED_SHA}")
print(f"match: {sha == EXPECTED_SHA}")
if sha != EXPECTED_SHA:
    sys.exit("SHA MISMATCH - aborting")

src_lines = load_lines(SRC)
print(f"source lines (1-based, split on newline): {len(src_lines)}")
print(f"source line 1502 first 100 chars: {src_lines[1501][:100]!r}")

staging_lines = load_lines(STAGING)
hits = extract_citations(staging_lines)

print(f"\nextraction pattern (python re): {CIT_RE_TEXT!r}")
print(f"total pattern hits: {len(hits)}")
foreign = [h for h in hits if h["foreign"]]
print(f"hits preceded by a filename (EXCLUDED, foreign target): {len(foreign)}")
for h in foreign:
    print(f"  staging line {h['staging_line']}: citation {h['citation']!r} "
          f"belongs to {h['foreign']!r}")

cits = [h for h in hits if not h["foreign"]]
distinct = sorted({(h["start"], h["end"]) for h in cits})
print(f"\nFW5 citations kept: {len(cits)}")
print(f"distinct (start,end) targets: {len(distinct)}")
n_ranges_inverted = sum(1 for a, b in distinct if b < a)
print(f"ranges with end < start (in distinct set): {n_ranges_inverted}")
out_of_range = [d for d in distinct if d[1] > len(src_lines)]
print(f"targets beyond source length {len(src_lines)} (in distinct set): {out_of_range}")

# sanity probes of the pattern
probes = ["FW5:172", ":1364", ":950-:952", ":950\u2013:952", ":148-150",
          "FW5:609/:622", "FW5:1362-1364", "FW5:1502", "FW5:787-800",
          "PLAN:184-188 does not bare-match"]
pat = re.compile(CIT_RE_TEXT)
for pr in probes:
    ms = [m.group(0) for m in pat.finditer(pr)]
    print(f"  probe {pr!r} -> {ms}")

json.dump(
    {"sha256": sha, "source_lines": len(src_lines), "hits": cits,
     "excluded_foreign": foreign, "distinct": distinct},
    open("out/extracted.json", "w", encoding="utf-8"), indent=2)
print(f"\nwrote out/extracted.json")
