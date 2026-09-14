"""Attack the receipt self-check guarantee and the layout conventions.

claims:
  - "A receipt is checkable against itself: key is recomputed and must equal step_key"
  - "step_path ... so the two spellings cannot drift apart"
  - "run_id is checked ... a run id can never reach outside the loops root"

test:
  R1  build a receipt, tamper one field after the fact (frozen? object.__setattr__?)
  R2  receipt.filename == RunPaths.step_path(index, kind).name  (same spelling)
  R3  open marker spelling: step_path(...,open_marker=True) ends '.json.open'
  R4  run_id with '/', '..', '.', '~', leading sep - all must be refused
  R5  receipt.step_key recomputation catches a hand-forged step_key
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minireason.loop.types import StepReceipt, RunPaths, run_paths, LoopError

rp = run_paths("/repo", "run1")
R2 = None
for i, kind in [(0, "PREREGISTER"), (7, "SEND"), (9999, "CLOSE")]:
    rec = StepReceipt.build(loop_plan_id="0"*64, index=i, kind=kind,
                            started_utc="2024-01-01T00:00:00Z")
    sp = rp.step_path(i, kind).name
    print("R2", kind, "filename==path name:", rec.filename == sp, repr(rec.filename), repr(sp))

print("R3 open marker:", rp.step_path(3, "SEND", open_marker=True).name)

for bad in ("a/b", "../x", ".", "~", "/etc", "a\\b", "a b", "", "ok_run.1-2"):
    try:
        run_paths("/repo", bad)
        print("R4", repr(bad), "ACCEPTED")
    except LoopError as exc:
        print("R4", repr(bad), "refused:", exc.code)

# hand-forged step_key must be caught
good = StepReceipt.key("0"*64, "SEND", None, None, {})
try:
    StepReceipt(step_key="f"*64, index=1, kind="SEND", loop_plan_id="0"*64,
                status="COMPLETE", started_utc="2024-01-01T00:00:00Z")
    print("R5 forged ACCEPTED")
except LoopError as exc:
    print("R5 forged ->", exc.code)

# frozen?
rec = StepReceipt.build(loop_plan_id="0"*64, index=0, kind="PREFLIGHT",
                        started_utc="2024-01-01T00:00:00Z")
try:
    object.__setattr__(rec, "status", "HALTED")
    print("R1 object.__setattr__ bypass OK ->", rec.status)
except Exception as exc:
    print("R1 frozen:", type(exc).__name__)
