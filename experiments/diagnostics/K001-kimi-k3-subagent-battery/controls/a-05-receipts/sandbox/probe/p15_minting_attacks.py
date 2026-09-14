"""Attacks on the minting rule that did not work.

  * quote a high receipt id inside a receipt body and see whether a later mint
    can be made to reuse a letter;
  * push one UTC date past Z (deviation 2's bijective base 26);
  * a stray undecodable byte in the ledger while minting.
"""
from __future__ import annotations

import _bootstrap  # noqa: F401
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from minireason.loop import receipts as R

MOMENT = datetime(2026, 9, 14, 9, 12, 33, tzinfo=timezone.utc)

with tempfile.TemporaryDirectory() as tmp:
    ledger = Path(tmp) / "a.md"
    ledger.write_bytes(b"# ledger\n")

    a = R.open_receipt(body="quoting REC-20260914-ZZ and REC-20260913-ZZZZ for effect",
                       ledger_path=ledger, moment=MOMENT, set_current=False)
    b = R.open_receipt(title="t", choice="c", why="w", contribution="k",
                       ledger_path=ledger, moment=MOMENT, set_current=False)
    c = R.open_receipt(title="t", choice="c", why="w", contribution="k",
                       ledger_path=ledger, moment=MOMENT, set_current=False)
    print("after quoting REC-20260914-ZZ:", a, b, c)
    print("any reuse:", len({a, b, c}) != 3)

    # bijective base 26 straight through Z
    print("next_letter([])      :", R.next_letter([]))
    print("next_letter(['Z'])   :", R.next_letter(["Z"]))
    print("next_letter(['AZ'])  :", R.next_letter(["AZ"]))
    print("next_letter(['ZZ'])  :", R.next_letter(["ZZ"]))
    print("next_letter(['B','A']):", R.next_letter(["B", "A"]))
    seen = set()
    value: list[str] = []
    for _ in range(30):
        letter = R.next_letter(value)
        value.append(letter)
        seen.add(letter)
    print("30 successive letters:", " ".join(value[:5]), "...", " ".join(value[-5:]),
          "| all distinct:", len(seen) == 30)

    # mint beside an undecodable byte
    gnarly = Path(tmp) / "b.md"
    gnarly.write_bytes(b"# ledger\n\nREC-20260914-A ... \xff\xfe\x80 ...\n")
    print("mint beside \\xff\\xfe\\x80 ->",
          R.open_receipt(title="t", choice="c", why="w", contribution="k",
                         ledger_path=gnarly, moment=MOMENT, set_current=False))

    # a lowercase or mixed-case id in the ledger is not a receipt id
    mixed = Path(tmp) / "c.md"
    mixed.write_bytes(b"# ledger\n\nrec-20260914-a and REC-20260914-b lowercase\n")
    print("suffixes scanned:", R.scan_receipt_ids(mixed.read_bytes(), "20260914"))
    print("mint             ->",
          R.open_receipt(title="t", choice="c", why="w", contribution="k",
                         ledger_path=mixed, moment=MOMENT, set_current=False))
