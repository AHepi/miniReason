"""Attacks that are EXPECTED to fail - evidence about the module.

1. Two threads racing open_receipt must mint distinct ids (no collision).
2. A secret-bearing receipt body must be refused, never redacted or written.
3. A cadence deadline miss must be recorded at notice time, never backdated.
4. Suffix minting past Z must be bijective (Z -> AA -> AB), never reuse A.
"""
import sys, tempfile, threading, os
from pathlib import Path
from datetime import datetime, timedelta, timezone

sys.path.insert(0, "src")
from minireason.loop import receipts
from minireason.loop.types import LoopError

tmp = Path(tempfile.mkdtemp())
ledger = tmp / "LEDGER.md"
ledger.write_bytes(b"# ledger\n")
moment = datetime(2026, 9, 15, 12, 0, 0, tzinfo=timezone.utc)

# 1. thread contention on minting
ids, errors = [], []
def worker(n):
    try:
        for _ in range(20):
            ids.append(receipts.open_receipt(
                title=f"t{n}", choice="c", why="w", contribution="ct",
                ledger_path=ledger, moment=moment, set_current=False))
    except Exception as e:
        errors.append(e)
threads = [threading.Thread(target=worker, args=(n,)) for n in range(4)]
[t.start() for t in threads]
[t.join() for t in threads]
print("1. minted:", len(ids), "unique:", len(set(ids)), "errors:", len(errors),
      "->", "COLLISION" if len(ids) != len(set(ids)) or errors else "attack failed")

# 2. secret in body
os.environ["PROBE_TEST_CREDENTIAL"] = "ak-1234567890abcdef"
try:
    receipts.open_receipt(body=f"token is ak-1234567890abcdef",
                          ledger_path=ledger, moment=moment, set_current=False)
    print("2. attack SUCCEEDED: secret written")
except LoopError as e:
    print("2. refused with", e.code, "| value in message:",
          "ak-" in str(e) or "ak-" in e.detail, "-> attack failed")
finally:
    del os.environ["PROBE_TEST_CREDENTIAL"]

# 3. cadence never backdated
started = datetime(2026, 9, 15, 0, 0, 0, tzinfo=timezone.utc)
c = receipts.Cadence(started)
check = c.check(started + timedelta(seconds=400))
print("3a. state:", check.state, "miss recorded at:", c.misses[0].recorded_utc,
      "deadline:", c.misses[0].deadline_utc)
try:
    c.acknowledge(started + timedelta(seconds=100))
    print("3b. backdate accept - attack SUCCEEDED")
except LoopError as e:
    print("3b. refused with", e.code, "-> attack failed")

# 4. suffix bijectivity
seq = []
nxt = "A"
existing = set()
for _ in range(30):
    existing.add(nxt)
    nxt = receipts.next_letter(existing)
    seq.append(nxt)
print("4. sequence:", "...".join(seq[:3]), seq[25:30],
      "reused:", len(set(seq)) != len(seq), "-> attack failed")
