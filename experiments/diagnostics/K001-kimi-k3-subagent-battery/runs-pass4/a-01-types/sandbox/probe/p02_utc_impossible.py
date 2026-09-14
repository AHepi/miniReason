"""Probe: does the receipt timestamp check admit impossible dates?

_utc's failure message claims the value "must be an ISO-8601 UTC timestamp
(Z or +00:00)". ISO-8601 has months 01-12, hours 00-23, minutes/seconds 00-59.
"""
import sys
sys.path.insert(0, "src")

from minireason.loop.types import StepReceipt, LoopError

PID = "ab" * 32
base = dict(loop_plan_id=PID, index=0, kind="PREFLIGHT")

for stamp in ("2026-01-01T12:00:00Z",        # sane control
              "2026-13-40T25:61:61Z",        # month 13, day 40, hour 25
              "2026-02-30T00:00:00+00:00",   # February 30 does not exist
              "2026-01-01 12:00:00Z"):       # space instead of T
    try:
        r = StepReceipt.build(started_utc=stamp, **base)
        print(f"{stamp!r}: ACCEPTED, receipt.started_utc = {r.started_utc!r}")
    except LoopError as e:
        print(f"{stamp!r}: refused {e.code}")
