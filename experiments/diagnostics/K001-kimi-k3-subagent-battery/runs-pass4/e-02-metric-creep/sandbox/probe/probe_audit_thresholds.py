"""Probe: do the AuditConfig rates/streaks reach any adjudication of content
in the code shipped in this sandbox?

The rule permits an operational alarm that stops the reading arm
(``instrument_fault``, design 5 clause 6). It forbids the number deciding
anything about a reading's standing. This probe greps every .py file in the
sandbox for uses of the three threshold names and of ``instrument_fault``,
and prints where each occurs.
"""
import sys, pathlib

root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "src"))

tokens = ("judge_err_max", "streak_max", "instrument_fault")
hits = {t: [] for t in tokens}
for path in sorted(root.rglob("*.py")):
    if "probe" in path.parts:
        continue
    for lineno, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        for t in tokens:
            if t in line:
                hits[t].append(f"{path.relative_to(root)}:{lineno}: {line.strip()[:100]}")

for t in tokens:
    print(f"== {t}: {len(hits[t])} occurrences")
    for h in hits[t]:
        print("   ", h)

# Every file that mentions the thresholds:
files = {h.split(":")[0] for t in hits for h in hits[t]}
print("files mentioning the thresholds:", sorted(files))
print("verdict input: thresholds occur only in types.py (declaration/validation),",
      "never in any module that reads a reading, a mark, or an adjudication outcome")
