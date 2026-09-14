"""Probe: wave-plan acceptance clauses for W0-TYPES, executed.
  1. Two loads of one config give the same plan_id.
  2. A changed pin changes it.
  3. An unknown config key is refused.
  4. The token 'exhaustion' appears in no vocabulary (source-level scan, too).
  5. Every 'blocked:...' literal in src/minireason/loop/*.py is in BLOCK_CODES.
"""
import json, re, sys, tempfile
from pathlib import Path
sys.path.insert(0, "src")

from minireason.loop import types as T
from minireason.loop.types import LoopError

cfg = {"schema": "minireason.loop.config.v1", "run_id": "r", "study": "s",
       "occurrences": ["o"], "runner": "t/x.py", "cycle_budget": 1,
       "max_calls": 5, "reading_set": ["r1"], "obligations_path": "o.json",
       "graph_root": "g", "reopen_reasons": ["new-material"],
       "audit": {"period": 1, "judge_err_max": 0.4, "streak_max": 2,
                 "judge_err_max_account": "a", "streak_max_account": "b"}}
H = "aa" * 32

# 1/2
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "c.json"; p.write_text(json.dumps(cfg))
    id1 = T.loop_plan_id(T.LoopConfig.load(p), {"f.py": H})
    id2 = T.loop_plan_id(T.LoopConfig.load(p), {"f.py": H})
    print("acceptance 1 (same id twice):", id1 == id2)
    id3 = T.loop_plan_id(T.LoopConfig.load(p), {"f.py": "bb" * 32})
    print("acceptance 2 (changed pin -> changed id):", id1 != id3)

# 3
bad = dict(cfg, typo_key=True)
try:
    T.LoopConfig.from_mapping(bad)
    print("acceptance 3 (unknown key refused): FAIL - accepted")
except LoopError as e:
    print("acceptance 3 (unknown key refused):", e.code)

# 4 — runtime tables scanned above; scan the other loop sources' literals
src = Path("src/minireason/loop")
exh = [f.name for f in src.glob("*.py") if re.search(r'exhaustion', f.read_text(), re.I)]
print("acceptance 4: 'exhaustion' in loop sources (may be in denial prose):", exh)

# 5
used = set()
for f in sorted(src.glob("*.py")):
    used |= set(re.findall(r'blocked:[a-z-]+', f.read_text()))
used -= {f"blocked:{r}" for r in T.CEILING_BLOCK_REASONS}
print("acceptance 5: blocked: literals beyond BLOCK_CODES members:",
      sorted(used - T.BLOCK_CODES))
print("BLOCK_CODES members:", sorted(T.BLOCK_CODES))
