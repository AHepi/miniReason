"""Probe: run_id / wave edges (remainder of p08)."""
import sys
sys.path.insert(0, "src")

from minireason.loop.types import StepReceipt, run_paths, LoopError

PID = "ab" * 32
STAMP = "2026-01-01T00:00:00Z"

r2 = StepReceipt.build(loop_plan_id=PID, index=1, kind="SEND", started_utc=STAMP,
                       wave="w-1.2", cycle=1)
print("wave 'w-1.2' accepted:", r2.wave)

for rid in ("a/b", "..", "a b", "ok-1.2", "a\\b"):
    try:
        run_paths("/repo", rid)
        print(f"run_id {rid!r}: accepted")
    except LoopError as e:
        print(f"run_id {rid!r}: refused {e.code}")
