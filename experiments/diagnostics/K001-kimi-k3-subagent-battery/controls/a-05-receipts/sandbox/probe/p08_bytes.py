"""Property 1: 'Appends are byte mode and locked, and never rewrite or re-encode
a byte that is already in the file.'  And scan_receipt_ids' 'a stray undecodable
byte cannot stop a receipt from being written.'

Also: does LEDGER_APPEND_NOT_VERIFIED actually fire when the read-back differs?
"""
from __future__ import annotations

import _bootstrap  # noqa: F401
import hashlib
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from minireason.loop import receipts as R
from minireason.loop.types import LoopError

MOMENT = datetime(2026, 9, 14, 9, 12, 33, tzinfo=timezone.utc)

MIXED = (b"# Decision ledger\r\n\r\n"
         b"REC-20260913-Z opened at 2026-09-13 00:00:00 UTC: an earlier day.\r\n\r\n"
         b"REC-20260914-A opened at 2026-09-14 00:00:00 UTC: caf\xc3\xa9 \xe2\x80\x94 prose.\n"
         b"A stray undecodable byte: \xff\xfe and a lone \r carriage return.\n")

with tempfile.TemporaryDirectory() as tmp:
    ledger = Path(tmp) / "DECISION_LEDGER.md"
    ledger.write_bytes(MIXED)
    before = ledger.read_bytes()
    print("prefix sha256 before:", hashlib.sha256(before).hexdigest()[:16],
          "len", len(before))

    rid = R.open_receipt(title="a receipt beside undecodable bytes",
                         choice="append", why="the file must not be re-encoded",
                         contribution="proves property 1",
                         ledger_path=ledger, moment=MOMENT, set_current=False)
    after = ledger.read_bytes()
    print("minted:", rid, "(new UTC date letters restart:",
          R.scan_receipt_ids(before, "20260913"), "->", R.scan_receipt_ids(after, "20260914"), ")")
    print("prefix preserved byte-for-byte:", after[:len(before)] == before)
    print("appended region:", after[len(before):][:80])

    # CRLF tail: no spurious blank line, and no CRLF rewritten to LF.
    crlf = Path(tmp) / "crlf.md"
    crlf.write_bytes(b"# ledger\r\nREC-20260914-A opened at x: seed.\r\n")
    R.ledger_append("a second paragraph", crlf)
    print("crlf file now:", crlf.read_bytes())

    # LEDGER_APPEND_NOT_VERIFIED: a handle that claims more than it writes.
    class Lying:
        def __init__(self, handle):
            self._handle = handle

        def write(self, data):
            self._handle.write(memoryview(data)[:-1])
            return len(data)

        def __getattr__(self, name):
            return getattr(self._handle, name)

        def __enter__(self):
            self._handle.__enter__()
            return self

        def __exit__(self, *exc):
            return self._handle.__exit__(*exc)

    victim = Path(tmp) / "victim.md"
    victim.write_bytes(b"# ledger\n")
    plain = R._open_append
    R._open_append = lambda path: Lying(plain(path))
    try:
        R.ledger_append("this write drops its last byte", victim)
    except LoopError as error:
        print("lying handle ->", error.code)
    finally:
        R._open_append = plain
    print("victim bytes:", victim.read_bytes())

    # LEDGER_INCOMPLETE_WRITE: a handle that writes nothing.
    class Deaf:
        def __init__(self, handle):
            self._handle = handle

        def write(self, data):
            return 0

        def __getattr__(self, name):
            return getattr(self._handle, name)

        def __enter__(self):
            self._handle.__enter__()
            return self

        def __exit__(self, *exc):
            return self._handle.__exit__(*exc)

    R._open_append = lambda path: Deaf(plain(path))
    try:
        R.ledger_append("nothing lands", victim)
    except LoopError as error:
        print("deaf handle  ->", error.code, "|", error.detail)
    finally:
        R._open_append = plain
