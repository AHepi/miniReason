"""Pinned-down defect: receipt cycle-range raises the CONFIG table's code.

types.py __post_init__ calls the shared helper _whole(), which ALWAYS raises
CONFIG_INVALID_VALUE.  A bad cycle on a step RECEIPT is therefore reported as a
configuration error - the wrong declared table, and a code the receipt can
never legitimately carry.  Contrast RunPaths.cycle(), which uses
CYCLE_OUT_OF_RANGE.

Also: LoopError shape enforcement and str() form.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minireason.loop import types

lpid = "0"*64
# receipt path
try:
    types.StepReceipt.build(loop_plan_id=lpid, index=0, kind="SEND",
                            started_utc="2024-01-01T00:00:00Z", cycle=0)
except types.LoopError as exc:
    print("receipt cycle=0        ->", exc.code)

# the layout path uses CYCLE_OUT_OF_RANGE
rp = types.run_paths("/repo", "run1")
try:
    rp.cycle(0)
except types.LoopError as exc:
    print("RunPaths.cycle(0)      ->", exc.code)

# key() path also leaks CONFIG_INVALID_VALUE
try:
    types.StepReceipt.key(lpid, "SEND", 0, None, {})
except types.LoopError as exc:
    print("StepReceipt.key cycle=0->", exc.code)

# LoopError shape
for code in ("low", "1ABC", "HAS SPACE", "OK_CODE", "_LEAD"):
    try:
        e = types.LoopError(code, "detail here")
        print("LoopError", repr(code), "-> str:", str(e))
    except ValueError as exc:
        print("LoopError", repr(code), "shape-refused:", exc)
