"""Two seams disclose the same missed deadline with different numbers.

Cadence.record_checkpoint hands checkpoint_receipt the stored CadenceMiss (the
one frozen at FIRST notice); a caller who calls checkpoint_receipt directly with
the CadenceCheck gets the lateness AT WRITE TIME.  Same clock, same deadline,
same paragraph moment.

Also: LedgerAppend.sha256 is the digest of the whole file after the append, and
it is taken after the flock is released.
"""
from __future__ import annotations

import _bootstrap  # noqa: F401
import hashlib
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from minireason.loop import receipts as R

T0 = datetime(2026, 9, 14, 9, 0, 0, tzinfo=timezone.utc)


def at(seconds: float) -> datetime:
    return T0 + timedelta(seconds=seconds)


with tempfile.TemporaryDirectory() as tmp:
    ledger = Path(tmp) / "a.md"
    ledger.write_bytes(b"# ledger\n")

    # Arm A: the clock is looked at once past the deadline, then the receipt is
    # written 500 s later.
    a = R.Cadence(T0, ledger_path=ledger)
    a.check(at(310))                       # first notice, 10 s late
    appended = a.record_checkpoint(at(810), "REC-20260914-A", "arm A progress")
    print("A record_checkpoint       :", appended.text)

    # Arm B: identical clock and identical moments, but the caller passes the
    # CadenceCheck itself, which is what checkpoint_receipt's own branch expects.
    ledger_b = Path(tmp) / "b.md"
    ledger_b.write_bytes(b"# ledger\n")
    b = R.Cadence(T0, ledger_path=ledger_b)
    b.check(at(310))
    check = b.check(at(810))
    appended_b = R.checkpoint_receipt("REC-20260914-A", "arm B progress",
                                      cadence=check, ledger_path=ledger_b,
                                      moment=check.now)
    print("B checkpoint_receipt(check):", appended_b.text)

    print()
    print("A discloses overdue:", a.misses[-1].overdue_seconds, "s")
    print("B discloses overdue:", check.overdue_seconds, "s")
    print("true lateness at the moment both paragraphs are stamped: 510.0 s")

    # LedgerAppend.sha256
    print()
    data = ledger.read_bytes()
    print("append.sha256            :", appended.sha256[:16])
    print("sha256(whole file)       :", hashlib.sha256(data).hexdigest()[:16])
    payload = data[appended.offset:appended.end]
    print("sha256(appended payload) :", hashlib.sha256(payload).hexdigest()[:16])

    # the read-back happens after the flock is released: an external appender
    # that lands in that window is inside the digest this append reports.
    ledger_c = Path(tmp) / "c.md"
    ledger_c.write_bytes(b"# ledger\n")
    plain_unlock = R._unlock

    def unlock_then_outsider(handle):
        plain_unlock(handle)
        with open(ledger_c, "ab", buffering=0) as other:   # a second agent
            other.write(b"\nsomeone else's paragraph\n")

    R._unlock = unlock_then_outsider
    try:
        out = R.ledger_append("mine", ledger_c)
    finally:
        R._unlock = plain_unlock
    print()
    print("c.md after         :", ledger_c.read_bytes())
    print("my append verified :", ledger_c.read_bytes()[out.offset:out.end])
    print("out.sha256 covers the outsider's bytes:",
          out.sha256 == hashlib.sha256(ledger_c.read_bytes()).hexdigest())
