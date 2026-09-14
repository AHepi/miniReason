"""Print the citation pairs 16-20 (stdout of verify_citations.py was truncated)."""

FW5_PATH = "docs/sources/FW5-explanatory-construction.md"
STAGING_PATH = "staging/a001-STAGING.md"

CITATIONS = [
    (112, 630, 630),
    (113, 630, 630),
    (113, 1200, 1206),
    (135, 1390, 1390),
    (142, 1372, 1372),
]

fw5 = open(FW5_PATH, encoding="utf-8").read().split("\n")
staging = open(STAGING_PATH, encoding="utf-8").read().split("\n")

for i, (sline, lo, hi) in enumerate(CITATIONS, start=16):
    print()
    print("### Citation %d: staging line %d -> FW5:%s" % (i, sline, str(lo) if lo == hi else "%d-%d" % (lo, hi)))
    print("--- STAGING line %d ---" % sline)
    print(staging[sline - 1])
    print("--- FW5:%s ---" % (str(lo) if lo == hi else "%d-%d" % (lo, hi)))
    for n in range(lo, hi + 1):
        print("[FW5:%d] %s" % (n, fw5[n - 1]))
    print("=" * 100)

# extra: where does FW5:630's three-case contract text live, and what is line 630 exactly?
print()
print("line 630 repr:", repr(fw5[629]))
