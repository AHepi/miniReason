"""Smoke: what the module resolves to in this sandbox, and one plain append."""
from __future__ import annotations

import _bootstrap  # noqa: F401
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from minireason.loop import receipts as R
from minireason.loop.types import FAILURE_CODES

print("DEFAULT_REPO_ROOT   =", R.DEFAULT_REPO_ROOT)
print("DEFAULT_LEDGER_PATH =", R.DEFAULT_LEDGER_PATH)
print("interface-note codes missing from the module's own raises:")
import re
src = Path(R.__file__).read_text(encoding="utf-8")
raised = sorted(set(re.findall(r'ReceiptError\(\s*"([A-Z_0-9]+)"', src))
                | {"SECRET_IN_RECEIPT"})
print("  raised in receipts.py :", raised)
print("  all in FAILURE_CODES  :", all(c in FAILURE_CODES for c in raised))

NOTE_CODES = {
    "SECRET_IN_RECEIPT", "LEDGER_EMPTY_PARAGRAPH", "LEDGER_INCOMPLETE_WRITE",
    "LEDGER_APPEND_NOT_VERIFIED", "RECEIPT_ID_MALFORMED", "RECEIPT_SUFFIX_MALFORMED",
    "RECEIPT_FORM_MALFORMED", "RECEIPT_BODY_AMBIGUOUS", "RECEIPT_FIELDS_MISSING",
    "PREREGISTRATION_SENTENCE_MISSING", "ACTIVITY_PHASE_UNKNOWN",
    "ACTIVITY_DECISION_MISSING", "ACTIVITY_TOOL_MISSING", "ACTIVITY_LOGGER_FAILED",
    "ACTIVITY_RAW_COMMAND_TEXT", "ACTIVITY_CONTROL_CHARACTER", "CADENCE_BACKDATED",
    "CADENCE_THRESHOLDS_INVERTED", "MOMENT_NOT_AWARE", "MOMENT_NOT_DATETIME",
}
print("  raised but not in WAVE0-INTERFACE section 5:", sorted(set(raised) - NOTE_CODES))

with tempfile.TemporaryDirectory() as tmp:
    ledger = Path(tmp) / "DECISION_LEDGER.md"
    ledger.write_bytes(b"# Decision ledger\r\n\r\nREC-20260914-A opened at x: seed.\r\n")
    moment = datetime(2026, 9, 14, 9, 12, 33, tzinfo=timezone.utc)
    rid = R.open_receipt(title="A title", choice="do the thing", why="because",
                         contribution="it helps", evidence="probe/p01_smoke.py",
                         paths=["src/minireason/loop/receipts.py"],
                         ledger_path=ledger, moment=moment)
    print("minted:", rid)
    print("--- ledger bytes after ---")
    print(repr(ledger.read_bytes()))
