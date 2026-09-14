"""Attacks on custody.fenced: escape by ``..``, by symlink, by absolute path,
by sibling-prefix, by backslash, and the accepted forms the docstring names.
"""
import _boot  # noqa: F401
import os
import tempfile
from pathlib import Path

from minireason.loop.custody import fenced, CustodyMismatch


def show(label, root, path):
    try:
        out = fenced(root, path)
    except CustodyMismatch as exc:
        print(f"{label:<44} REFUSED {exc.code} detail={exc.detail!r}")
    except Exception as exc:  # noqa: BLE001
        print(f"{label:<44} RAISED  {type(exc).__name__}: {exc}")
    else:
        print(f"{label:<44} OK      {out}")


with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp).resolve()
    root = base / "run"
    (root / "sub").mkdir(parents=True)
    (base / "outside").mkdir()
    (base / "outside" / "secret.txt").write_bytes(b"x")
    (root / "sub" / "kept.txt").write_bytes(b"y")

    # symlinks
    os.symlink(base / "outside", root / "away")                  # dir -> outside
    os.symlink(base / "outside" / "secret.txt", root / "aim")    # file -> outside
    os.symlink(root / "sub", root / "inward")                    # dir -> inside
    os.symlink(base / "outside" / "nothere", root / "dangling")  # dangling -> outside
    os.symlink(base, root / "up")                                # dir -> parent of root

    print("root =", root)
    show("relative inside", root, "sub/kept.txt")
    show("relative not-yet-existing", root, "steps/0001-S0.json")
    show("empty string", root, "")
    show("dot", root, ".")
    show("dot-slash", root, "./")
    show("parent traversal", root, "../outside/secret.txt")
    show("embedded ..", root, "sub/../../outside/secret.txt")
    show("absolute inside", root, str(root / "sub" / "kept.txt"))
    show("absolute outside", root, str(base / "outside" / "secret.txt"))
    show("absolute sibling-prefix", root, str(base / "running" / "x"))
    show("symlink dir -> outside", root, "away/secret.txt")
    show("symlink file -> outside", root, "aim")
    show("symlink dir -> inside", root, "inward/kept.txt")
    show("dangling symlink -> outside", root, "dangling")
    show("symlink -> parent of root", root, "up/outside/secret.txt")
    show("backslash-spelled traversal", root, "sub\\..\\..\\outside\\secret.txt")
    show("root itself as absolute", root, str(root))
    show("nul byte", root, "sub/a\x00b")

    # a root that is itself reached through a symlink
    os.symlink(root, base / "rootlink")
    show("symlinked root, relative", base / "rootlink", "sub/kept.txt")
    show("symlinked root, abs real", base / "rootlink", str(root / "sub" / "kept.txt"))

    # a relative root, resolved against the cwd
    os.chdir(base)
    show("relative root", "run", "sub/kept.txt")
    show("relative root, escape", "run", "../outside/secret.txt")
os.chdir("/")
