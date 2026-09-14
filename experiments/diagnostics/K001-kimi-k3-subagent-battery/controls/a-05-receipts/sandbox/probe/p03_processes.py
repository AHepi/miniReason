"""Module docstring: 'The receipt id is minted under the same lock that performs
the append, so two concurrent agents cannot mint the same letter.'

'Two agents' is two processes, not two threads: the in-process RLock cannot
serialise them, so this arm exercises the flock alone.  8 processes x 12 receipts.
"""
from __future__ import annotations

import _bootstrap  # noqa: F401
import multiprocessing as mp
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from minireason.loop import receipts as R

MOMENT = datetime(2026, 9, 14, 9, 12, 33, tzinfo=timezone.utc)
PROCS, PER = 8, 12


def child(ledger_str: str, start, out) -> None:
    ledger = Path(ledger_str)
    start.wait()
    got = []
    for _ in range(PER):
        got.append(R.open_receipt(title="t", choice="c", why="w", contribution="k",
                                  ledger_path=ledger, moment=MOMENT,
                                  set_current=False))
    out.put(got)


if __name__ == "__main__":
    context = mp.get_context("fork")
    with tempfile.TemporaryDirectory() as tmp:
        ledger = Path(tmp) / "DECISION_LEDGER.md"
        ledger.write_bytes(b"# ledger\n")
        start = context.Barrier(PROCS)
        out = context.Queue()
        procs = [context.Process(target=child, args=(str(ledger), start, out))
                 for _ in range(PROCS)]
        for proc in procs:
            proc.start()
        minted = []
        for _ in procs:
            minted.extend(out.get())
        for proc in procs:
            proc.join()

        data = ledger.read_bytes()
        ids = re.findall(rb"^REC-20260914-([A-Z]+) opened at ", data, re.M)
        print("expected            :", PROCS * PER)
        print("ids returned        :", len(minted), "distinct:", len(set(minted)))
        print("paragraphs in file  :", len(ids), "distinct:", len(set(ids)))
        duplicates = sorted({i for i in minted if minted.count(i) > 1})
        print("duplicate ids minted:", duplicates)
        lines = [line for line in data.split(b"\n")
                 if line and not line.startswith(b"REC-") and line != b"# ledger"]
        print("torn / stray lines  :", len(lines), lines[:1])
