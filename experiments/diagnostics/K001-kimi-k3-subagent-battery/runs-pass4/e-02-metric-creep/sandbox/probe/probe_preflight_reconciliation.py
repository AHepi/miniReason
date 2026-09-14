"""Probe: is PREFLIGHT's required guard-reconciliation call enforced anywhere
in this sandbox?

standard.py deviation 8 and types.py SeatsConfig docstring both say PREFLIGHT
*must* call standard.assert_config_matches_standard(...). If nothing calls
it, the seat/panel numbers in a LoopConfig can contradict the pinned standard
silently. Also probe: does the C condition hold in practice, i.e. can a
config declare min_judge_families=8 while the standard freezes 2, with no
module in this sandbox refusing it?
"""
import sys, pathlib

root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "src"))

name = "assert_config_matches_standard"
hits = []
for path in sorted(root.rglob("*.py")):
    if "probe" in path.parts or "test" in path.name:
        continue
    for lineno, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if name in line and "def " not in line:
            hits.append(f"{path.relative_to(root)}:{lineno}: {line.strip()[:90]}")
print(f"non-defining, non-test references to {name}:")
for h in hits:
    print("   ", h)
print(f"call sites found: {sum(1 for h in hits if 'docstring' not in h.lower())} "
      "(docstring mentions only)" if hits else "NONE - the function is never called")

# Now demonstrate the un-enforced condition concretely:
from minireason.loop.types import SeatsConfig
from minireason.loop import standard

cfg = SeatsConfig.from_mapping({"min_judge_families": 8, "paraphrase_n": 5})
print()
print(f"SeatsConfig accepted min_judge_families={cfg.min_judge_families}, "
      f"paraphrase_n={cfg.paraphrase_n}")
print(f"standard freezes min_judge_families="
      f"{standard.GUARD_PARAMETERS['min_judge_families']}, paraphrase_n="
      f"{standard.GUARD_PARAMETERS['paraphrase_n']}")
try:
    standard.assert_config_matches_standard(cfg.as_dict(), None, where="probe")
    print("reconciliation: NO REFUSAL (unexpected)")
except standard.StandardInvalid as exc:
    print(f"reconciliation when called: refuses with code {exc.code}")
print("=> the panel-shape numbers only respect the pinned standard if a later "
      "module (PREFLIGHT / W5) makes the call; in this sandbox nothing does")
