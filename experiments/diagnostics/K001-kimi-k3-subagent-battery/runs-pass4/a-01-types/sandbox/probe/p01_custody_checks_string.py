"""Probe: does CustodyReport.from_mapping accept and garble a bare-string `checks`,
while the constructor refuses the same input?"""
import runpy, sys, os
sys.path.insert(0, "src")

from minireason.loop.types import CustodyReport, LoopError

# 1. Direct constructor with a bare string is refused.
try:
    CustodyReport(verified=False, checks="SOURCE_PIN_MISSING")
    print("constructor(bare string): ACCEPTED (unexpected)")
except LoopError as e:
    print(f"constructor(bare string): refused {e.code}: {e.detail}")

# 2. The from_mapping load path, given a bare string.
report = CustodyReport.from_mapping({"verified": False, "checks": "SOURCE_PIN_MISSING"})
print("from_mapping(bare string): ACCEPTED, checks =", report.checks)
print("as_dict:", report.as_dict())

# 3. from_findings given a bare string as the whole argument.
report2 = CustodyReport.from_findings("SOURCE_PIN_MISSING")
print("from_findings(bare string): verified =", report2.verified,
      "checks =", report2.checks)
