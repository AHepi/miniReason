"""Check that B1's proposed predicate separates the renders that spend the id
from the ones that do not.  It does not patch src/; it evaluates the predicate
against the same render callables the defect probe used.
"""
from __future__ import annotations

import _bootstrap  # noqa: F401

from minireason.loop.receipts import scan_receipt_ids

TOKEN = "20260914"
RECEIPT_ID = "REC-20260914-A"
SUFFIX = RECEIPT_ID.rsplit("-", 1)[1]

RENDERS = {
    "omits the id (the defect)":
        lambda rid, stamp: f"Pre-registration opened at {stamp}: a paragraph that omits its own id.",
    "lower-cases the id (the defect)":
        lambda rid, stamp: f"{rid.lower()} opened at {stamp}: x.",
    "the shipped pre-registration header shape":
        lambda rid, stamp: f"**{rid} opened at {stamp}: pre-register the loop.**\n\nbody.",
    "carries the id mid-sentence":
        lambda rid, stamp: f"Opened at {stamp} under {rid}: body.",
    "carries a DIFFERENT id only":
        lambda rid, stamp: f"REC-20260914-Q opened at {stamp}: body.",
}

for label, render in RENDERS.items():
    text = render(RECEIPT_ID, "2026-09-14 09:12:33 UTC")
    spends = SUFFIX in scan_receipt_ids(text.encode("utf-8"), TOKEN)
    print(f"{'refused' if not spends else 'accepted':>8}  {label}")
    print(f"          scan_receipt_ids -> {scan_receipt_ids(text.encode('utf-8'), TOKEN)}")
