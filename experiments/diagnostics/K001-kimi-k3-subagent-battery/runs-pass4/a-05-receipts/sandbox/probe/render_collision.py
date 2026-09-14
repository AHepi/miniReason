"""A render callback to open_receipt runs under _APPEND_LOCK (a RLock), so a
same-thread re-entry is admitted - and then deadlocks: fcntl.flock on a second
open description of the same file blocks forever, in the same process, with no
refusal code. The mint_receipt_id docstring claims the lock 'is not re-entrant
across threads'; it says nothing truthful about the same thread, where render
runs.

Run with an alarm so the hang is observable rather than silent.
"""
import signal, sys, tempfile
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, "src")
from minireason.loop import receipts

def alarm(signum, frame):
    print("DEADLOCK: same-thread re-entry blocked on flock, no exception raised")
    sys.exit(0)

signal.signal(signal.SIGALRM, alarm)
signal.alarm(8)

tmp = Path(tempfile.mkdtemp())
ledger = tmp / "LEDGER.md"
ledger.write_bytes(b"# ledger\n")
moment = datetime(2026, 9, 15, 12, 0, 0, tzinfo=timezone.utc)

def reentering_render(receipt_id, stamp):
    # mint_receipt_id is published API; calling it from a render callback is
    # exactly what the docstring discusses. It hangs the whole process.
    receipts.mint_receipt_id(ledger, today=moment)
    return "outer body"

rid = receipts.open_receipt(render=reentering_render, ledger_path=ledger,
                            moment=moment, set_current=False)
print("completed:", rid, "(no deadlock)")
