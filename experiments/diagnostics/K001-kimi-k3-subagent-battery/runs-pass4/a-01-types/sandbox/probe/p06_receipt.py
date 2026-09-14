"""Probe: receipt self-validation — step_key recompute, spending mismatch,
failure_code/status agreement, round-trip from_dict/as_dict, replayable,
filename collision between kinds with same index."""
import sys
sys.path.insert(0, "src")

from minireason.loop.types import StepReceipt, LoopError

PID = "cd" * 32
STAMP = "2026-01-01T00:00:00Z"

def build(**kw):
    kw.setdefault("failure_code", None)
    return StepReceipt.build(loop_plan_id=PID, index=1, kind="SEND",
                             started_utc=STAMP, **kw)

# 1. tampered step_key refused
r = build(inputs_sha256={"a.txt": "ee" * 32})
d = r.as_dict()
d["inputs_sha256"]["evil.txt"] = "ff" * 32
try:
    StepReceipt.from_dict(d)
    print("tampered inputs: ACCEPTED (bad)")
except LoopError as e:
    print("tampered inputs refused:", e.code)

# 2. spending mismatch refused
try:
    StepReceipt.build(loop_plan_id=PID, index=2, kind="PREFLIGHT",
                      started_utc=STAMP, spending=True)
    print("spending=True on PREFLIGHT: ACCEPTED (bad)")
except LoopError as e:
    print("spending mismatch refused:", e.code)

# 3. auto spending fill
print("SEND auto spending:", build().spending)

# 4. FAILED without failure_code
try:
    StepReceipt.build(loop_plan_id=PID, index=3, kind="SEND", started_utc=STAMP,
                      status="FAILED")
    print("FAILED w/o failure_code: ACCEPTED (bad)")
except LoopError as e:
    print("FAILED w/o failure_code refused:", e.code)

# 5. COMPLETE with a failure_code
try:
    StepReceipt.build(loop_plan_id=PID, index=4, kind="SEND", started_utc=STAMP,
                      failure_code="TRANSPORT_OR_RESPONSE_ERROR")
    print("COMPLETE with failure_code: ACCEPTED (bad)")
except LoopError as e:
    print("COMPLETE with failure_code refused:", e.code)

# 6. round trip
r2 = build(status="HALTED", failure_code="STEP_TIMEOUT", wave="w1", cycle=2)
back = StepReceipt.from_dict(r2.as_dict())
print("round trip equal dicts:", back.as_dict() == r2.as_dict())

# 7. block code in failure_code? shape passes, membership not enforced
r3 = StepReceipt.build(loop_plan_id=PID, index=5, kind="SEND", started_utc=STAMP,
                       status="FAILED", failure_code="BLOCKED:SCHEMA".replace(":", "_"))
print("failure_code shape-only (BLOCKED_SCHEMA):", r3.failure_code)
