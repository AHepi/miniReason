"""Two attacks on the step receipt.

  U1 (collision): two receipts with different `index` for the same
      (loop_plan_id, kind, cycle, wave, inputs) share ONE step_key, because
      key() does not include `index`; filename differs but key does not.
      W1-STEPS keys the ledger on step_key, so the second write collides with
      the first.
  U2 (failure_code): a receipt whose status is FAILED with
      failure_code='blocked:schema' (a BLOCK code, not a FAILURE code) is
      accepted, because __post_init__ only checks the UPPER_SNAKE shape and
      never the FAILURE_CODES table.  Yet the ceiling promises one register of
      block codes, counted by code, and the BLOCK_CODES/FAILED_CODES split is
      the one rule that partitions them.
  U3  failed receipt accepts an INVENTED code not in FAILURE_CODES.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minireason.loop.types import StepReceipt, LoopError, FAILURE_CODES

lpid = "0"*64

# U1 two indexes, same key
r0 = StepReceipt.build(loop_plan_id=lpid, index=0, kind="SEND",
                       started_utc="2024-01-01T00:00:00Z")
r1 = StepReceipt.build(loop_plan_id=lpid, index=1, kind="SEND",
                       started_utc="2024-01-01T00:00:00Z")
print("U1 two builds, keys equal:", r0.step_key == r1.step_key,
      "| filenames:", r0.filename, r1.filename)

# U2 BLOCK code as failure_code on a FAILED step
try:
    r = StepReceipt.build(loop_plan_id=lpid, index=0, kind="READ",
                          started_utc="2024-01-01T00:00:00Z", status="FAILED",
                          failure_code="blocked:schema")
    print("U2 lowercase block code as failure_code:")
    # _CODE = ^[A-Z][A-Z0-9_]*$ ; 'blocked:schema' has lowercase+colon -> should fail shape
    print("   ACCEPTED", r.failure_code)
except LoopError as exc:
    print("U2 refused:", exc.code)

# but an UPPER_SNAKE invented code, not in FAILURE_CODES
try:
    r = StepReceipt.build(loop_plan_id=lpid, index=0, kind="READ",
                          started_utc="2024-01-01T00:00:00Z", status="FAILED",
                          failure_code="MADE_UP_CODE")
    print("U3 invented-but-uppersnake failure_code ACCEPTED;",
          "in FAILURE_CODES?", r.failure_code in FAILURE_CODES)
except LoopError as exc:
    print("U3 refused:", exc.code)

# a valid FAILURE_CODES member is fine
r = StepReceipt.build(loop_plan_id=lpid, index=0, kind="READ",
                      started_utc="2024-01-01T00:00:00Z", status="FAILED",
                      failure_code="STEP_TIMEOUT")
print("U3b real code accepted:", r.failure_code)
