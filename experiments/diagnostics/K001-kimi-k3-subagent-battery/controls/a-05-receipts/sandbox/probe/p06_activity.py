"""activity(): 'No command is ever forwarded - the wrapper has no command
channel at all, so no record can carry raw command text' and 'Every way the
logger can fail carries a code from the table.'

The sandbox carries no tools/repo_activity.py, so a fake tool file and a
recording runner stand in for it; the argv the wrapper builds is the object
under test.
"""
from __future__ import annotations

import _bootstrap  # noqa: F401
import subprocess
import tempfile
from pathlib import Path
from types import SimpleNamespace

from minireason.loop import receipts as R
from minireason.loop.types import LoopError

seen: list[list[str]] = []


def ok_runner(argv, **kwargs):
    seen.append(list(argv))
    return SimpleNamespace(returncode=0, stdout="", stderr="")


with tempfile.TemporaryDirectory() as tmp:
    repo = Path(tmp)
    (repo / "tools").mkdir()
    (repo / "tools" / "repo_activity.py").write_text("# stand-in\n", encoding="utf-8")
    common = dict(decision="REC-20260914-A", repo_root=repo, runner=ok_runner)

    print("=== raw command text in `action` ===")
    for action in ("git push --force origin main",
                   "python3 tools/auto_loop.py run --config loop.json",
                   "rm -rf experiments/loops/RUN-1",
                   "git commit -m msg && git push",
                   "curl -X POST https://api.example/v1/chat"):
        try:
            argv = R.activity("event", action, "why", "goal", **common)
            print(f"  ACCEPTED  {action!r}")
        except LoopError as error:
            print(f"  refused   {action!r} -> {error.code}")

    print("=== a path that is an option of the logger's own CLI ===")
    seen.clear()
    argv = R.activity("event", "an action", "why", "goal",
                      paths=["--agent", "someone-else", "--decision", "REC-20260101-Z"],
                      **common)
    print("  argv:", argv[argv.index("--paths"):])
    print("  full argv tail:", argv[2:])

    print("=== paths given as a plain string ===")
    argv = R.activity("event", "an action", "why", "goal",
                      paths="docs/STATUS.md", **common)
    print("  argv tail:", argv[argv.index("--paths"):][:8], "... total tokens:", len(argv))

    print("=== how the logger can fail ===")

    def raise_oserror(argv, **kwargs):
        raise OSError(8, "Exec format error")

    def raise_timeout(argv, **kwargs):
        raise subprocess.TimeoutExpired(argv, 30.0)

    def no_returncode(argv, **kwargs):
        return SimpleNamespace(stdout="", stderr="")

    def nonzero(argv, **kwargs):
        return SimpleNamespace(returncode=3, stdout="", stderr="")

    for name, runner in (("timeout", raise_timeout), ("no returncode", no_returncode),
                         ("exit 3", nonzero), ("OSError from spawn", raise_oserror)):
        kwargs = dict(common)
        kwargs["runner"] = runner
        try:
            R.activity("event", "an action", "why", "goal", **kwargs)
            print(f"  {name:20s} -> returned normally")
        except LoopError as error:
            print(f"  {name:20s} -> LoopError {error.code}")
        except BaseException as error:            # noqa: BLE001
            print(f"  {name:20s} -> {type(error).__name__} (NOT a LoopError): {error}")
