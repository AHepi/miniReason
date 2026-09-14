"""Acceptance clause: 'Concurrent appends from two threads interleave with no
loss and no torn record under simulated short writes; id minting under
contention never collides.'

Two arms:
  A. 16 threads x 8 open_receipt calls, ordinary writes.
  B. the same, with _open_append replaced by a wrapper whose write() lands at
     most 3 bytes at a time (the 'simulated short writes' the clause names).
"""
from __future__ import annotations

import _bootstrap  # noqa: F401
import re
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path

from minireason.loop import receipts as R

MOMENT = datetime(2026, 9, 14, 9, 12, 33, tzinfo=timezone.utc)
THREADS, PER = 16, 8


class ShortWriter:
    """A handle that writes at most ``chunk`` bytes per write() call."""

    def __init__(self, handle, chunk=3):
        self._handle = handle
        self._chunk = chunk

    def write(self, data):
        view = memoryview(data)[: self._chunk]
        return self._handle.write(view)

    def __getattr__(self, name):
        return getattr(self._handle, name)

    def __enter__(self):
        self._handle.__enter__()
        return self

    def __exit__(self, *exc):
        return self._handle.__exit__(*exc)


def run(ledger: Path, short: bool) -> None:
    ledger.write_bytes(b"# ledger\n")
    minted: list[str] = []
    errors: list[BaseException] = []
    guard = threading.Lock()

    def worker() -> None:
        for _ in range(PER):
            try:
                rid = R.open_receipt(title="t", choice="c", why="w",
                                     contribution="k", ledger_path=ledger,
                                     moment=MOMENT, set_current=False)
            except BaseException as error:          # noqa: BLE001
                with guard:
                    errors.append(error)
                return
            with guard:
                minted.append(rid)

    plain = R._open_append
    if short:
        R._open_append = lambda path: ShortWriter(plain(path))
    try:
        threads = [threading.Thread(target=worker) for _ in range(THREADS)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    finally:
        R._open_append = plain

    data = ledger.read_bytes()
    written = re.findall(rb"^REC-20260914-([A-Z]+) opened at .+ State: pending\.$",
                         data, re.M)
    label = "short-write" if short else "plain"
    print(f"[{label}] expected={THREADS * PER} minted={len(minted)} "
          f"distinct_minted={len(set(minted))} well_formed_paragraphs={len(written)} "
          f"distinct_paragraph_ids={len(set(written))} errors={len(errors)}")
    if errors:
        print(f"[{label}] first error: {type(errors[0]).__name__}: {errors[0]}")
    stray = [line for line in data.split(b"\n")
             if line and not line.startswith(b"REC-") and not line.startswith(b"# ledger")]
    print(f"[{label}] lines that are neither the header nor a whole receipt: {len(stray)}")
    if stray:
        print(f"[{label}] first stray line: {stray[0][:90]!r}")


with tempfile.TemporaryDirectory() as tmp:
    run(Path(tmp) / "plain.md", short=False)
    run(Path(tmp) / "short.md", short=True)
