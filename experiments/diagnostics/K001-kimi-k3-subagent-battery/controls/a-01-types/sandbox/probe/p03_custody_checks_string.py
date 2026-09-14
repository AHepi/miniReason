"""_sequence refuses a bare string; does every door into CustodyReport use it?"""
from _fixture import H1, config  # noqa: E402

from minireason.loop import types  # noqa: E402

cfg = config()
plan = types.loop_plan_id(cfg, {"src/a.py": H1})
UTC = "2026-09-14T00:00:00Z"

print("--- door 1: the constructor (goes through _sequence)")
try:
    types.CustodyReport(verified=False, checks="SOURCE_PIN_MISMATCH")
    print("constructor: accepted")
except types.LoopError as exc:
    print("constructor: raised LoopError code=%r msg=%r" % (exc.code, str(exc)))

print()
print("--- door 2: from_mapping (tuple() before _sequence sees it)")
report = types.CustodyReport.from_mapping(
    {"verified": False, "checks": "SOURCE_PIN_MISMATCH"})
print("from_mapping: accepted, len(checks) =", len(report.checks))
print("from_mapping: as_dict() =", report.as_dict())

print()
print("--- door 3: from_findings on a bare string")
report3 = types.CustodyReport.from_findings("SOURCE_PIN_MISMATCH")
print("from_findings: accepted, len(checks) =", len(report3.checks))
print("from_findings: verified =", report3.verified)

print()
print("--- it reaches a published step receipt through from_dict")
good = types.StepReceipt.build(loop_plan_id=plan, index=3, kind="SEND",
                               started_utc=UTC, cycle=1, status="HALTED",
                               failure_code="CUSTODY_MISMATCH")
raw = good.as_dict()
raw["custody"] = {"verified": False, "checks": "SOURCE_PIN_MISMATCH"}
bad = types.StepReceipt.from_dict(raw)
print("receipt accepted; custody block re-emitted as:")
print(" ", bad.as_dict()["custody"])
print("number of custody checks recorded:", len(bad.custody.checks))

print()
print("--- and the honest record, for comparison")


class Finding:
    def __init__(self, code):
        self.code = code


honest = types.CustodyReport.from_findings([Finding("SOURCE_PIN_MISMATCH")])
print("from_findings([one finding]):", honest.as_dict())
