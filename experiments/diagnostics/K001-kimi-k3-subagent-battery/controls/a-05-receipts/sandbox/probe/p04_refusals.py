"""The three refusals the module names of itself:

  * 'A refusal names the environment variable, never the value, and writes
    nothing.'                                   (module docstring, property 3)
  * 'A ledger that does not exist is refused unless create=True.'  (deviation 7)
  * LEDGER_EMPTY_PARAGRAPH on a blank paragraph.
"""
from __future__ import annotations

import _bootstrap  # noqa: F401
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from minireason.loop import receipts as R
from minireason.loop.types import LoopError

MOMENT = datetime(2026, 9, 14, 9, 12, 33, tzinfo=timezone.utc)

os.environ["PROBE_FAKE_KEY"] = "sk-probe-0123456789abcdef"
from minireason.provider_openai_compat import register_secret_envs  # noqa: E402
register_secret_envs(["PROBE_FAKE_KEY"])
print("registered:", "PROBE_FAKE_KEY")

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)

    # 1. a credential in the paragraph of an EXISTING ledger.
    existing = root / "existing.md"
    existing.write_bytes(b"# ledger\n")
    before = existing.read_bytes()
    try:
        R.ledger_append("the key is sk-probe-0123456789abcdef", existing)
    except LoopError as error:
        print("1 existing ledger  ->", type(error).__name__, error.code, "|", error.detail)
        print("   names:", getattr(error, "names", None))
        print("   bytes unchanged:", existing.read_bytes() == before)

    # 2. the same refusal on a ledger that does not exist yet, create=True.
    fresh = root / "fresh.md"
    print("2 before: fresh.md exists =", fresh.exists())
    try:
        R.ledger_append("the key is sk-probe-0123456789abcdef", fresh, create=True)
    except LoopError as error:
        print("2 fresh ledger     ->", error.code)
    print("   after refusal: fresh.md exists =", fresh.exists(),
          "size =", fresh.stat().st_size if fresh.exists() else None)

    # 3. ... and what that leaves for the create=False guard of deviation 7.
    rid = R.open_receipt(title="t", choice="c", why="w", contribution="k",
                         ledger_path=fresh, moment=MOMENT, set_current=False)
    print("3 create=False into the file the refusal left behind ->", rid)

    # 4. a ledger that genuinely does not exist, create=False.
    missing = root / "nope.md"
    try:
        R.ledger_append("hello", missing)
    except LoopError as error:
        print("4 missing ledger   ->", error.code)
    print("   nope.md exists =", missing.exists())

    # 5. LEDGER_EMPTY_PARAGRAPH
    try:
        R.ledger_append("   \n\n  ", existing)
    except LoopError as error:
        print("5 blank paragraph  ->", error.code)

    # 6. the default-path refusal of deviation 8
    try:
        R.ledger_append("hello", None)
    except LoopError as error:
        print("6 no default       ->", error.code)
