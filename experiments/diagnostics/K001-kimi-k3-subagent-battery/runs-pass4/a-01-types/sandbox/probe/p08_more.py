"""Probe: relative-path canonicalisation and wave id shape."""
import sys
sys.path.insert(0, "src")

from minireason.loop.types import StepReceipt, LoopConfig, LoopError

PID = "ab" * 32
STAMP = "2026-01-01T00:00:00Z"

cfg = {"run_id": "r", "study": "s", "occurrences": ["o"], "runner": "t/x.py",
       "cycle_budget": 1, "max_calls": 5, "reading_set": ["r1"],
       "obligations_path": "o.json", "graph_root": "g",
       "reopen_reasons": ["new-material"],
       "audit": {"period": 1, "judge_err_max": 0.4, "streak_max": 2,
                 "judge_err_max_account": "a", "streak_max_account": "b"}}

try:
    c = LoopConfig.from_mapping(dict(cfg, occurrences=["a/../b"]))
    print("'a/../b' occurrence: accepted", c.occurrences)
except LoopError as e:
    print("'a/../b' occurrence refused:", e.code)
c = LoopConfig.from_mapping(dict(cfg, occurrences=["a/./b"]))
print("'a/./b' occurrence accepted as:", c.occurrences)
c = LoopConfig.from_mapping(dict(cfg, occurrences=["//a"]))
print("'//a' occurrence accepted as:", c.occurrences)

r2 = StepReceipt.build(loop_plan_id=PID, index=1, kind="SEND", started_utc=STAMP,
                       wave="w-1.2", cycle=1)
print("wave 'w-1.2' accepted:", r2.wave)

# run_id with separator refused
from minireason.loop.types import run_paths
for rid in ("a/b", "..", "a b", "ok-1.2"):
    try:
        run_paths("/repo", rid)
        print(f"run_id {rid!r}: accepted")
    except LoopError as e:
        print(f"run_id {rid!r}: refused {e.code}")
