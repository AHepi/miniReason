"""Cadence: 'a missed cadence deadline is recorded and never backdated'
(W0-RECEIPTS acceptance) and 'The clock refuses to move backwards'
(loop/__init__.py).
"""
from __future__ import annotations

import _bootstrap  # noqa: F401
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from minireason.loop import receipts as R
from minireason.loop.types import LoopError

T0 = datetime(2026, 9, 14, 9, 0, 0, tzinfo=timezone.utc)


def at(seconds: float) -> datetime:
    return T0 + timedelta(seconds=seconds)


with tempfile.TemporaryDirectory() as tmp:
    ledger = Path(tmp) / "DECISION_LEDGER.md"
    ledger.write_bytes(b"# ledger\n")

    clock = R.Cadence(T0, ledger_path=ledger)
    for seconds in (0, 239.9, 240, 299.9, 300, 480):
        check = clock.check(at(seconds))
        print(f"  t+{seconds:<6} state={check.state:<8} due={check.due} "
              f"missed={check.missed} overdue={check.overdue_seconds:.1f}")
    print("  misses:", [(m.deadline_utc.isoformat(), m.recorded_utc.isoformat(),
                         round(m.overdue_seconds, 1)) for m in clock.misses])

    appended = clock.record_checkpoint(at(500), "REC-20260914-A",
                                       "read the module and wrote two probes",
                                       "probe/p07_cadence.py",
                                       next_action="write the review")
    print("  checkpoint text:", appended.text)
    print("  clock reset to :", clock.since.isoformat())

    print("  backwards check ->", end=" ")
    try:
        clock.check(at(400))
    except LoopError as error:
        print(error.code, "|", error.detail)

    print("  backwards acknowledge ->", end=" ")
    try:
        clock.acknowledge(at(100))
    except LoopError as error:
        print(error.code)

    print("  naive datetime ->", end=" ")
    try:
        clock.check(datetime(2026, 9, 14, 10, 0, 0))
    except LoopError as error:
        print(error.code)

    print("  inverted thresholds ->", end=" ")
    try:
        R.Cadence(T0, warn_seconds=300.0, deadline_seconds=240.0)
    except LoopError as error:
        print(error.code)

    print("  negative thresholds ->", end=" ")
    negative = R.Cadence(T0, warn_seconds=-10.0, deadline_seconds=-5.0)
    print("accepted;", "check at t+0 state =", negative.check(T0).state)

    # the same deadline seen twice records one miss, at first notice.
    clock2 = R.Cadence(T0, ledger_path=ledger)
    clock2.check(at(400))
    clock2.check(at(900))
    print("  one deadline, two looks -> misses:",
          [(m.recorded_utc.isoformat(), round(m.overdue_seconds, 1)) for m in clock2.misses])

    # a caller can still stamp a follow-up paragraph in the past.
    late = R.checkpoint_receipt("REC-20260914-A", "progress", ledger_path=ledger,
                                moment=T0 - timedelta(days=400))
    print("  checkpoint_receipt(moment=T0-400d):", late.text[:70])
