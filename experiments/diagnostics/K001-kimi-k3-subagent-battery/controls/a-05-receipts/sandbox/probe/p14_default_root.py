"""Deviation 8: 'DEFAULT_REPO_ROOT is found by walking up for
tools/repo_activity.py ... and is None when this module was not imported from a
checkout - which is what an installed wheel is.'

An installed wheel that happens to sit *under* some checkout carrying that
marker is not None: the walk stops at the nearest ancestor with the marker,
whichever repository that is.  Here the package is installed into a virtualenv
inside an unrelated checkout, and the module is re-imported from there.
"""
from __future__ import annotations

import _bootstrap  # noqa: F401
import importlib
import shutil
import sys
import tempfile
from pathlib import Path

SANDBOX = Path(_bootstrap.ROOT)

with tempfile.TemporaryDirectory() as tmp:
    other = Path(tmp) / "some-other-checkout"
    (other / "tools").mkdir(parents=True)
    (other / "tools" / "repo_activity.py").write_text("# the marker\n", encoding="utf-8")
    (other / "docs").mkdir()
    ledger = other / "docs" / "DECISION_LEDGER.md"
    ledger.write_bytes(b"# Another project's decision ledger\n\n"
                       b"REC-20260914-A opened at 2026-09-14 00:00:00 UTC: not ours.\n")

    site = other / ".venv" / "lib" / "python3" / "site-packages"
    site.mkdir(parents=True)
    shutil.copytree(SANDBOX / "src" / "minireason", site / "minireason")
    shutil.copytree(SANDBOX / "src" / "deepreason_core", site / "deepreason_core")

    for name in [n for n in sys.modules if n.split(".")[0] in ("minireason", "deepreason_core")]:
        del sys.modules[name]
    sys.path.insert(0, str(site))
    try:
        R = importlib.import_module("minireason.loop.receipts")
        print("imported from       :", R.__file__)
        print("DEFAULT_REPO_ROOT   :", R.DEFAULT_REPO_ROOT)
        print("DEFAULT_LEDGER_PATH :", R.DEFAULT_LEDGER_PATH)
        print("is that this run's repository?  no - it is", other.name)
        before = ledger.read_bytes()
        rid = R.open_receipt(title="a receipt with no ledger_path=",
                             choice="use the default", why="O3 says pass it explicitly",
                             contribution="shows what the default resolves to")
        print("open_receipt() with no ledger_path minted:", rid)
        print("and appended into the other checkout's ledger:",
              ledger.read_bytes() != before)
        print(ledger.read_text(encoding="utf-8"))
    finally:
        sys.path.remove(str(site))
