"""Which .code does each refusal actually carry?

The helpers _text, _whole and _mapping hard-code CONFIG_INVALID_VALUE while
_identifier, _relative and _digests take a ``code`` argument. Where a caller
passes PIN_INVALID or STEP_RECEIPT_INVALID, does the refusal keep it?
"""
from _fixture import H1, config, show  # noqa: E402

from minireason.loop import types  # noqa: E402

cfg = config()
plan = types.loop_plan_id(cfg, {"src/a.py": H1})
UTC = "2026-09-14T00:00:00Z"

print("--- pins: the package docstring promises PIN_INVALID")
show("pins is not a mapping        ", types.loop_plan_id, cfg, ["src/a.py"])
show("pin key is the empty string  ", types.loop_plan_id, cfg, {"": H1})
show("pin key is whitespace        ", types.loop_plan_id, cfg, {"   ": H1})
show("pin key is not a string      ", types.loop_plan_id, cfg, {7: H1})
print("  for comparison, the paths the docstring names:")
show("pin key is absolute          ", types.loop_plan_id, cfg, {"/etc/passwd": H1})
show("pin key bears ..             ", types.loop_plan_id, cfg, {"../x.py": H1})
show("pin value is null            ", types.loop_plan_id, cfg, {"src/a.py": None})

print()
print("--- step receipts: the module has CYCLE_OUT_OF_RANGE and STEP_RECEIPT_INVALID")
show("RunPaths.cycle(0)            ", types.run_paths("/repo", "loop-001").cycle, 0)
show("StepReceipt.key cycle=0      ", types.StepReceipt.key, plan, "SEND", 0, None, {})
show("StepReceipt.key cycle=100    ", types.StepReceipt.key, plan, "SEND", 100, None, {})
show("StepReceipt.build cycle=0    ", types.StepReceipt.build,
     loop_plan_id=plan, index=1, kind="SEND", started_utc=UTC, cycle=0)
show("StepReceipt.key inputs=[]    ", types.StepReceipt.key, plan, "SEND", 1, None, [])
show("StepReceipt.key inputs {'':h}", types.StepReceipt.key, plan, "SEND", 1, None, {"": H1})

print()
print("--- CustodyReport: from_findings' docstring says STEP_RECEIPT_INVALID")


class Finding:
    def __init__(self, code):
        self.code = code


show("finding carries code=None    ", types.CustodyReport.from_findings, [Finding(None)])
show("finding carries code=''      ", types.CustodyReport.from_findings, [Finding("")])
show("finding carries code=7       ", types.CustodyReport.from_findings, [Finding(7)])
show("CustodyReport(checks=7)      ", types.CustodyReport, False, 7)

print()
print("--- which codes does the module actually route where?")
print("CYCLE_OUT_OF_RANGE in FAILURE_CODES:", "CYCLE_OUT_OF_RANGE" in types.FAILURE_CODES)
print("PIN_INVALID in FAILURE_CODES:       ", "PIN_INVALID" in types.FAILURE_CODES)
