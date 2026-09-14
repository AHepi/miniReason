"""Probe: pin order vs pin renames; null pin; identity stability across loads."""
import sys, json, tempfile
from pathlib import Path
sys.path.insert(0, "src")

from minireason.loop.types import LoopConfig, loop_plan_id, LoopError

cfg_raw = {
    "schema": "minireason.loop.config.v1",
    "run_id": "r1", "study": "s1",
    "occurrences": ["occ/a"], "runner": "tools/x.py",
    "cycle_budget": 5, "max_calls": 10,
    "reading_set": ["row/1"], "obligations_path": "obs.json",
    "graph_root": "graph", "reopen_reasons": ["new-material"],
    "audit": {"period": 2, "judge_err_max": 0.2, "streak_max": 3,
              "judge_err_max_account": "because", "streak_max_account": "because"},
}
H = "aa" * 32
H2 = "bb" * 32

a = loop_plan_id(cfg_raw, {"f1.py": H, "f2.py": H2})
b = loop_plan_id(cfg_raw, {"f2.py": H2, "f1.py": H})
print("pin order irrelevant:", a == b)

# rename a pin key: not claimed to be refused anywhere, observe
c = loop_plan_id(cfg_raw, {"renamed.py": H, "f2.py": H2})
print("pin rename changes id:", a != c)

# null pin refused
try:
    loop_plan_id(cfg_raw, {"f1.py": None})
    print("null pin: ACCEPTED (bad)")
except LoopError as e:
    print("null pin refused:", e.code)

# load from file twice -> same id
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "c.json"
    p.write_text(json.dumps(cfg_raw))
    d = loop_plan_id(LoopConfig.load(p), {"f1.py": H})
    e = loop_plan_id(LoopConfig.load(p), {"f1.py": H})
    print("two loads one id:", d == e)

# non-str pin key
try:
    loop_plan_id(cfg_raw, {1: H})
    print("int pin key: ACCEPTED (bad)")
except LoopError as e:
    print("int pin key refused:", e.code)
