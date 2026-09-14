"""notes/WAVE0-INTERFACE.md section 5 against the module it records."""
from __future__ import annotations

import _bootstrap  # noqa: F401
import inspect

from minireason.loop import receipts as R

NOTE = {
    "mint_receipt_id": "(ledger_path=DEFAULT_LEDGER_PATH, *, today=None) -> str",
    "ledger_append": "(text, ledger_path=DEFAULT_LEDGER_PATH, *, newline=b'\\n') -> LedgerAppend",
    "open_receipt": "(*, title, choice, why, contribution, evidence, paths, source_identity, "
                    "state='pending', body, render, form='opened', ledger_path, moment, "
                    "set_current=True) -> str",
    "open_preregistration": "(ledger_path=DEFAULT_LEDGER_PATH, *, loop_plan_id, run_id, "
                            "source_identity, moment) -> str",
}

for name, recorded in NOTE.items():
    actual = str(inspect.signature(getattr(R, name)))
    print(name)
    print("  note  :", recorded)
    print("  actual:", actual)
    print("  'create' in the actual signature:", "create" in actual)
    print()

print("DEFAULT_REPO_ROOT   note: 'Path'  actual:", type(R.DEFAULT_REPO_ROOT).__name__,
      "=", R.DEFAULT_REPO_ROOT)
print("DEFAULT_LEDGER_PATH note: 'Path'  actual:", type(R.DEFAULT_LEDGER_PATH).__name__,
      "=", R.DEFAULT_LEDGER_PATH)
print()
print("O3 says DEFAULT_REPO_ROOT is Path(__file__).parents[3]. Source of the module:")
import re
from pathlib import Path
src = Path(R.__file__).read_text(encoding="utf-8")
print("  'parents[3]' occurs in receipts.py:", "parents[3]" in src)
print("  the marker walk:", re.search(r"for candidate in .*\n.*\n.*\n", src).group().strip())
