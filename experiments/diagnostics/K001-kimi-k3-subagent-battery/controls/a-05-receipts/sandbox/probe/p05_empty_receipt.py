"""open_receipt's two guards against a contentless receipt:

  RECEIPT_FIELDS_MISSING -- 'title, choice, why and contribution are required
                            without body or render'
  LEDGER_EMPTY_PARAGRAPH -- raised when the rendered paragraph is blank

and the docstring sentence 'Three mutually exclusive ways to say what the
receipt says'.
"""
from __future__ import annotations

import _bootstrap  # noqa: F401
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from minireason.loop import receipts as R
from minireason.loop.types import LoopError

MOMENT = datetime(2026, 9, 14, 9, 12, 33, tzinfo=timezone.utc)


def fresh(root: Path, name: str) -> Path:
    path = root / name
    path.write_bytes(b"# ledger\n")
    return path


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)

    # 1. four fields present but all whitespace -> the guard passes.
    ledger = fresh(root, "a.md")
    rid = R.open_receipt(title=" ", choice=" ", why=" ", contribution=" ",
                         ledger_path=ledger, moment=MOMENT, set_current=False)
    print("1 whitespace fields   -> minted", rid)
    print("  paragraph:", ledger.read_bytes().split(b"\n")[2])

    # 2. body="" -> LEDGER_EMPTY_PARAGRAPH does not fire either.
    ledger = fresh(root, "b.md")
    rid = R.open_receipt(body="", ledger_path=ledger, moment=MOMENT, set_current=False)
    print("2 body=''             -> minted", rid)
    print("  paragraph:", ledger.read_bytes().split(b"\n")[2])

    # 3. render returning "" -> this one IS caught.
    ledger = fresh(root, "c.md")
    try:
        R.open_receipt(render=lambda rid_, stamp: "", ledger_path=ledger,
                       moment=MOMENT, set_current=False)
    except LoopError as error:
        print("3 render->'' ", "        ->", error.code)

    # 4. 'mutually exclusive': body together with the four house fields.
    ledger = fresh(root, "d.md")
    rid = R.open_receipt(title="T", choice="C", why="W", contribution="K",
                         evidence="E", paths=["p"], source_identity="S",
                         body="only this survives", ledger_path=ledger,
                         moment=MOMENT, set_current=False)
    print("4 body + four fields  -> minted", rid, "(no RECEIPT_BODY_AMBIGUOUS)")
    print("  paragraph:", ledger.read_bytes().split(b"\n")[2])

    # 5. render together with the four house fields.
    ledger = fresh(root, "e.md")
    rid = R.open_receipt(title="T", choice="C", why="W", contribution="K",
                         source_identity="digest changed to abc",
                         render=lambda rid_, stamp: f"{rid_} opened at {stamp}: only this.",
                         ledger_path=ledger, moment=MOMENT, set_current=False)
    print("5 render + four fields-> minted", rid, "(no RECEIPT_BODY_AMBIGUOUS)")
    print("  paragraph:", ledger.read_bytes().split(b"\n")[2])

    # 6. paths given as a plain string, which Sequence[str] admits.
    ledger = fresh(root, "f.md")
    R.open_receipt(title="T", choice="C", why="W", contribution="K",
                   paths="src/minireason/loop/receipts.py",
                   ledger_path=ledger, moment=MOMENT, set_current=False)
    print("6 paths='...' (a str) -> paragraph:")
    print("  ", ledger.read_bytes().split(b"\n")[2][:200])
