"""bracket(): 'Bracket one repository act with begin and outcome records.'
What reaches the caller when the outcome record is the thing that fails?

And the two re-entrancy warnings: mint_receipt_id's 'Never call this from inside
a render callback' and _append's 'It must not itself append.'
"""
from __future__ import annotations

import _bootstrap  # noqa: F401
import os
import tempfile
import threading
import traceback
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

from minireason.loop import receipts as R

MOMENT = datetime(2026, 9, 14, 9, 12, 33, tzinfo=timezone.utc)


class Disk(RuntimeError):
    """Stands in for the real repository failure the bracket is wrapping."""


with tempfile.TemporaryDirectory() as tmp:
    repo = Path(tmp) / "repo"
    (repo / "tools").mkdir(parents=True)
    (repo / "tools" / "repo_activity.py").write_text("# stand-in\n", encoding="utf-8")

    calls = {"n": 0}

    def flaky(argv, **kwargs):
        calls["n"] += 1
        # the begin record lands; the outcome record's logger has since died.
        return SimpleNamespace(returncode=0 if calls["n"] == 1 else 9)

    try:
        with R.bracket("write the plan", "the run needs a plan", "publish before dispatch",
                       decision="REC-20260914-A", repo_root=repo, runner=flaky):
            raise Disk("the disk went away")
    except BaseException as error:              # noqa: BLE001
        print("what the caller catches :", type(error).__name__,
              getattr(error, "code", ""), "|", error)
        print("what it replaced        :",
              type(error.__context__).__name__, "|", error.__context__)
        print("traceback tail:")
        print("   ", traceback.format_exception_only(type(error), error)[0].strip())

    # re-entrancy: mint_receipt_id inside a render callback.
    ledger = Path(tmp) / "DECISION_LEDGER.md"
    ledger.write_bytes(b"# ledger\n")

    def render_that_mints(receipt_id: str, stamp: str) -> str:
        nested = R.mint_receipt_id(ledger, today=MOMENT)
        return f"{receipt_id} opened at {stamp}: nested mint returned {nested}."

    print("mint_receipt_id inside render ->", end=" ")
    done: list[str] = []
    worker = threading.Thread(
        target=lambda: done.append(R.open_receipt(render=render_that_mints,
                                                  ledger_path=ledger, moment=MOMENT,
                                                  set_current=False)),
        daemon=True)
    worker.start()
    worker.join(timeout=5.0)
    print("returned" if done else "STILL BLOCKED after 5 s", done)
    if done:
        print("   paragraph:", ledger.read_bytes().split(b"\n")[2])

    # re-entrancy: ledger_append inside a render callback (the documented "must not").
    def render_that_appends(receipt_id: str, stamp: str) -> str:
        R.ledger_append("a nested paragraph", ledger)
        return f"{receipt_id} opened at {stamp}: outer."

    print("ledger_append inside render   ->", end=" ")
    finished: list[object] = []
    worker = threading.Thread(
        target=lambda: finished.append(R.open_receipt(render=render_that_appends,
                                                      ledger_path=ledger, moment=MOMENT,
                                                      set_current=False)),
        daemon=True)
    worker.start()
    worker.join(timeout=5.0)
    print("returned" if finished else "STILL BLOCKED after 5 s (self-deadlock)", finished)

os._exit(0)
