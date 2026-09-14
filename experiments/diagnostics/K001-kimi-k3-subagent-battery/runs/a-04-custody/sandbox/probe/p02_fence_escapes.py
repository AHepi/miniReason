"""Probe 2: fenced() against escape constructions.

Claim under test (W0-CUSTODY acceptance): "a path escaping the run root is
refused", and the fenced docstring: "Refuses any ``..`` component outright ...
refuses a path that resolves outside the root - which is what catches an
intermediate symlink pointing away".

Constructions: literal .., an absolute path outside, an absolute path inside, a
relative root, ''-for-the-root, a mid-path symlink pointing outside, and
sibling-prefix confusions (/tmp/root vs /tmp/root-evil - the classic failure
of a text-prefix fence). Uses only tempfile space. Prints RESULT lines.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import custody


def attempt(root, path, label, expect_refusal):
    try:
        resolved = custody.fenced(root, path)
    except custody.CustodyMismatch as exc:
        status = "refused"  # the fence did its job
        ok = expect_refusal
        print("RESULT", "PASS" if ok else "FAIL", label, "->", status,
              "code=", exc.code, "detail=", exc.detail)
        return None
    status = f"allowed -> {resolved}"
    ok = not expect_refusal
    print("RESULT", "PASS" if ok else "FAIL", label, "->", status)
    return resolved


def main() -> None:
    with tempfile.TemporaryDirectory() as scratch:
        base = Path(scratch)
        run_root = base / "run"
        (run_root / "steps").mkdir(parents=True)
        outside = base / "outside.txt"
        outside.write_bytes(b"outside-bytes")

        attempt(run_root, "../outside.txt", "literal ..", True)
        attempt(run_root, "steps/../../outside.txt", ".. mid-path", True)
        attempt(run_root, str(outside), "absolute outside", True)
        attempt(run_root, str(run_root / "steps" / "x.json"), "absolute inside", False)
        attempt(run_root, "", "empty path = root itself", False)
        attempt(run_root, ".", "dot = root itself", False)

        # Relative root resolved against the CWD: docstring says "A relative
        # ROOT is resolved against the current working directory."
        old_cwd = os.getcwd()
        os.chdir(base)
        try:
            attempt(Path("run"), "steps/x.json", "relative root from CWD", False)
        finally:
            os.chdir(old_cwd)

        # Mid-path symlink pointing outside (the docstring's own example).
        link = run_root / "link-out"
        link.symlink_to(base)
        attempt(run_root, "link-out/../outside.txt", ".. through a symlink", True)
        attempt(run_root, "link-out/outside.txt", "symlink pointing outside", True)

        # Sibling-prefix confusion: a text-prefix check (/tmp/root vs
        # /tmp/root-evil) lets the sibling through; a component check does not.
        sibling = base / "run-evil"
        sibling.mkdir()
        (sibling / "loot.txt").write_bytes(b"loot")
        attempt(run_root, str(sibling / "loot.txt"), "sibling sharing the name prefix", True)


if __name__ == "__main__":
    main()
