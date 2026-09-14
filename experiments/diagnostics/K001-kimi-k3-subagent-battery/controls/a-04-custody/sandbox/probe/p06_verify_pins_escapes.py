"""verify_pins says: "Raises only :class:`CustodyMismatch` ``PIN_MAP_MISSING``".
This probe looks for trees and plan bodies that make it raise something else.
"""
import _boot  # noqa: F401
import os
import tempfile
from pathlib import Path

from minireason.loop import custody
from minireason.loop.custody import verify_pins, CustodyMismatch
from minireason.loop.types import LoopError

GOOD = "a" * 64
print("euid:", os.geteuid())


def probe(label, plan, repo):
    try:
        out = verify_pins(plan, repo)
    except CustodyMismatch as exc:
        print(f"{label:<40} CustodyMismatch {exc.code}")
    except LoopError as exc:  # noqa: PERF203
        print(f"{label:<40} LoopError(other) {exc.code}")
    except Exception as exc:  # noqa: BLE001
        print(f"{label:<40} ESCAPED {type(exc).__name__}: {exc} "
              f"(is LoopError: {isinstance(exc, LoopError)}, has .code: {hasattr(exc, 'code')})")
    else:
        print(f"{label:<40} returned {[(f.code, f.path) for f in out] or 'CLEAN'}")


with tempfile.TemporaryDirectory() as tmp:
    repo = Path(tmp).resolve()
    (repo / "src").mkdir()
    (repo / "src" / "a.py").write_bytes(b"one\n")

    probe("NUL in a pin key", {"pins": {"src/\x00a.py": GOOD}}, repo)
    probe("key of 5000 chars", {"pins": {"x" * 5000: GOOD}}, repo)
    probe("key is a FIFO", {"pins": {"fifo": GOOD}}, repo)

    os.mkfifo(repo / "fifo")
    probe("key is a FIFO (made)", {"pins": {"fifo": GOOD}}, repo)

    os.symlink(repo / "l2", repo / "l1")
    os.symlink(repo / "l1", repo / "l2")
    probe("symlink loop", {"pins": {"l1": GOOD}}, repo)

    # unreadable file
    secret = repo / "src" / "locked.py"
    secret.write_bytes(b"x")
    os.chmod(secret, 0o000)
    probe("unreadable pinned file", {"pins": {"src/locked.py": GOOD}}, repo)
    os.chmod(secret, 0o644)

    # a repo argument that is not a directory at all
    probe("repo is a regular file", {"pins": {"src/a.py": GOOD}}, repo / "src" / "a.py")
    probe("repo does not exist", {"pins": {"src/a.py": GOOD}}, repo / "nope")

    # non-string keys
    probe("integer pin key", {"pins": {1: GOOD}}, repo)
    probe("None pin key", {"pins": {None: GOOD}}, repo)
    probe("tuple pin key", {"pins": {("a", "b"): GOOD}}, repo)

    # and fenced / write_new for the same trees
    for label, fn in (
        ("fenced NUL", lambda: custody.fenced(repo, "src/\x00a.py")),
        ("fenced symlink loop", lambda: custody.fenced(repo, "l1")),
        ("write_new parent is a file",
         lambda: custody.write_new(repo / "src" / "a.py" / "k.json", {"k": 1})),
        ("write_new into a symlink loop",
         lambda: custody.write_new(repo / "l1" / "k.json", {"k": 1})),
    ):
        try:
            fn()
        except CustodyMismatch as exc:
            print(f"{label:<40} CustodyMismatch {exc.code}")
        except Exception as exc:  # noqa: BLE001
            print(f"{label:<40} ESCAPED {type(exc).__name__}: {exc} "
                  f"(is LoopError: {isinstance(exc, LoopError)})")
        else:
            print(f"{label:<40} OK")
