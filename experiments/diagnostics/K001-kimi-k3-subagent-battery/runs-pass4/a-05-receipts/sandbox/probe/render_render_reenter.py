"""Bounded probe: a render callback that re-enters ledger_append (the published
seam open_receipt hands user code to, under the RLock) deadlocks on flock in
the same thread on this platform. SIGALRM bounds the hang so we can observe it.
"""
import signal, sys, tempfile, threading
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, "src")
from minireason.loop import receipts

def give_up(signum, frame):
    print("DEADLOCK: re-entrant ledger_append from a render callback hung on "
          "flock in the same thread; no exception, no code")
    sys.exit(3)

signal.signal(signal.SIGALRM, give_up)
signal.alarm(6)

print("platform:", sys.platform)
print("_APPEND_LOCK type:", type(receipts._APPEND_LOCK).__name__)

tmp = Path(tempfile.mkdtemp())
ledger = tmp / "LEDGER.md"
ledger.write_bytes(b"# ledger\n")
moment = datetime(2026, 9, 15, 12, 0, 0, tzinfo=timezone.utc)

def reentering_render(receipt_id, stamp):
    # ledger_append holds the RLock re-entrantly in this thread, then calls
    # flock() on a second open description of the same file and blocks forever.
    receipts.ledger_append("sneaked in from render", ledger_path=ledger)
    return "outer body"

rid = receipts.open_receipt(render=reentering_render, ledger_path=ledger,
                            moment=moment, set_current=False)
print("completed without deadlock:", rid)
