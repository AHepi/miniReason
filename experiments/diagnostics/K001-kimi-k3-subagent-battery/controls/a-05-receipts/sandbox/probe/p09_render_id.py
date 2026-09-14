"""Property 2: 'The receipt id is minted under the same lock that performs the
append, so two concurrent agents cannot mint the same letter.'

Minting reads the ledger's own bytes (scan_receipt_ids), so an id is only spent
if the paragraph that is appended carries it.  open_receipt(render=...) hands
the render the id and appends whatever the render returns, unchecked.
"""
from __future__ import annotations

import _bootstrap  # noqa: F401
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from minireason.loop import receipts as R

MOMENT = datetime(2026, 9, 14, 9, 12, 33, tzinfo=timezone.utc)

with tempfile.TemporaryDirectory() as tmp:
    ledger = Path(tmp) / "DECISION_LEDGER.md"
    ledger.write_bytes(b"# ledger\n")

    def render_without_the_id(receipt_id: str, stamp: str) -> str:
        return f"Pre-registration opened at {stamp}: a paragraph that omits its own id."

    first = R.open_receipt(render=render_without_the_id, ledger_path=ledger,
                           moment=MOMENT, set_current=False)
    second = R.open_receipt(title="an ordinary receipt", choice="c", why="w",
                            contribution="k", ledger_path=ledger, moment=MOMENT,
                            set_current=False)
    third = R.open_receipt(render=render_without_the_id, ledger_path=ledger,
                           moment=MOMENT, set_current=False)
    print("ids returned to three callers:", first, second, third)
    print("ids visible in the ledger    :", R.scan_receipt_ids(ledger.read_bytes(), "20260914"))
    print("collision                    :", first == second == third)
    print("--- ledger ---")
    print(ledger.read_text(encoding="utf-8"))

    # the same, one step removed: a render that lower-cases the id it was given.
    ledger2 = Path(tmp) / "second.md"
    ledger2.write_bytes(b"# ledger\n")
    a = R.open_receipt(render=lambda rid, stamp: f"{rid.lower()} opened at {stamp}: x.",
                       ledger_path=ledger2, moment=MOMENT, set_current=False)
    b = R.open_receipt(render=lambda rid, stamp: f"{rid.lower()} opened at {stamp}: y.",
                       ledger_path=ledger2, moment=MOMENT, set_current=False)
    print("lower-cased id in the paragraph:", a, b, "-> same id twice:", a == b)

    # and the shape open_preregistration relies on, for contrast.
    ledger3 = Path(tmp) / "third.md"
    ledger3.write_bytes(b"# ledger\n")
    p1 = R.open_preregistration(ledger3, loop_plan_id="deadbeef", run_id="RUN-1",
                                moment=MOMENT)
    p2 = R.open_receipt(title="t", choice="c", why="w", contribution="k",
                        ledger_path=ledger3, moment=MOMENT, set_current=False)
    print("open_preregistration then open_receipt:", p1, p2, "-> distinct:", p1 != p2)

    # activity()'s decision field is not held to RECEIPT_ID_RE, unlike _follow_up's.
    from types import SimpleNamespace
    repo = Path(tmp) / "repo"
    (repo / "tools").mkdir(parents=True)
    (repo / "tools" / "repo_activity.py").write_text("# stand-in\n", encoding="utf-8")
    argv = R.activity("event", "an action", "why", "goal",
                      decision="not-a-receipt-id", repo_root=repo,
                      runner=lambda argv, **kw: SimpleNamespace(returncode=0))
    print("activity decision field:", argv[argv.index("--decision") + 1])
    try:
        R.close_receipt("not-a-receipt-id", "done", ledger_path=ledger)
    except Exception as error:                       # noqa: BLE001
        print("close_receipt same string ->", getattr(error, "code", type(error).__name__))
