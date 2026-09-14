"""Probe 9: fenced() returns the run root itself, resolved.

fenced's docstring: "Accepts a root-relative path, ''/'.' for the root
itself". The fence therefore hands back a resolved root path. The question,
given that the module pairs write_new with fenced("both are needed"): can a
caller that fenced its target still write a file directly at the run root, or
outside the nominally fenced tree, without tripping any other guard?
(The guards each do their own job - this records what the pair admits.)
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import custody


def main() -> None:
    with tempfile.TemporaryDirectory() as scratch:
        run_root = Path(scratch) / "run"
        run_root.mkdir()

        # fenced returns the root; writing a file directly at the root is
        # allowed by the pair (the run root's own plan.json writes need this).
        resolved = custody.fenced(run_root, "")
        custody.write_new(resolved / "plan.json", {"pins": {}})
        ok = (run_root / "plan.json").exists()
        print("RESULT", "PASS" if ok else "FAIL",
              "write at the fenced root itself succeeds (the layout needs this):", ok)

        # The fence's ".." refusal is static, and the docstring says so: even
        # 'a/../b' - which nobody would call an escape - is refused outright.
        try:
            custody.fenced(run_root, "steps/../plan.json")
        except custody.CustodyMismatch as exc:
            print("RESULT PASS '..' that would resolve back inside is refused outright:",
                  exc.code, "| conservative, documented")
        else:
            print("RESULT FAIL 'a/../b' allowed")

        # Depth is unbounded: any depth under the root is fenced-identical.
        deep = custody.fenced(run_root, "a/b/c/d/e/f.json")
        print("RESULT NOTE depth is unbounded inside the root:", deep)


if __name__ == "__main__":
    main()
