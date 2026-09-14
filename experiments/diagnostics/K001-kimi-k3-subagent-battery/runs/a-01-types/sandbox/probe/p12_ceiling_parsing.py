"""Cross-check the frozen ceiling's block-register clause against BLOCK_CODES.

The module claims: 'the other nine are exactly the nine reason codes
standard.CEILING_TEXT's block-register clause promises are "printed with counts
on every table"'.  The data file here is loop/data/ceiling_v1.md (the frozen
ceiling text this sandbox ships).  Parse the clause and compare both ways.
"""
import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minireason.loop import types

ROOT = os.path.join(os.path.dirname(__file__), "..")
text = open(os.path.join(ROOT, "src/minireason/loop/data/ceiling_v1.md"),
            encoding="utf-8").read()

m = re.search(r"The block register by reason code - (.*?) - is printed", text, re.S)
if not m:
    m = re.search(r"reason code \S+ (.*?) \S+ is printed", text, re.S)
seg = m.group(1) if m else ""
codes = re.findall(r"`([a-z][a-z-]+)`", seg)
print("ceiling clause codes:", codes)
ceiling_set = set(codes)
table_set = set(types.CEILING_BLOCK_REASONS)
print("order matches tuple:", codes == list(types.CEILING_BLOCK_REASONS))
print("ceiling minus table:", sorted(ceiling_set - table_set))
print("table minus ceiling:", sorted(table_set - ceiling_set))
print("BLOCK_CODES minus ceiling:", sorted(types.BLOCK_CODES
      - {types.BLOCK_CODE_PREFIX + c for c in ceiling_set}))
print("count BLOCK_CODES:", len(types.BLOCK_CODES))
