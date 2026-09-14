"""Probe 1: write_new on an already-existing path.

Claim under test (W0-CUSTODY acceptance): "write_new refuses an existing path".

Exercises: an existing regular file, an existing directory, and a dangling
symlink, and prints any bytes smuggled out through the refusal object itself.
Uses only tempfile space. Prints RESULT lines.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import custody


def result(ok: bool, *parts: object) -> None:
    print("RESULT", "PASS" if ok else "FAIL", *parts)


def main() -> None:
    with tempfile.TemporaryDirectory() as scratch:
        base = Path(scratch)

        # 1. Existing regular file, JSON value.
        target = base / "record.json"
        custody.write_new(target, {"a": 1})
        try:
            custody.write_new(target, {"a": 2})
        except Exception as exc:
            is_expected = (type(exc).__name__ == "WriteOnceViolation"
                           and getattr(exc, "code", None) == "WRITE_ONCE_VIOLATION")
            result(is_expected,
                   "existing regular file:", type(exc).__name__,
                   "code=", getattr(exc, "code", None),
                   "is FileExistsError:", isinstance(exc, FileExistsError))
        else:
            result(False, "existing regular file: NO EXCEPTION")

        # 2. Existing directory at the target path.
        directory = base / "as-dir"
        directory.mkdir()
        try:
            custody.write_new(directory, {"a": 1})
        except Exception as exc:
            result(type(exc).__name__ == "WriteOnceViolation",
                   "existing directory:", type(exc).__name__,
                   "code=", getattr(exc, "code", None))
        else:
            result(False, "existing directory: NO EXCEPTION")

        # 3. Dangling symlink at the target path (symlink to a missing file).
        link = base / "dangling"
        link.symlink_to(base / "does-not-exist")
        try:
            custody.write_new(link, b"payload")
            leaked = link.read_bytes()
            result(False, "dangling symlink: WRITE SUCCEEDED, bytes present via link:",
                   leaked)
        except Exception as exc:
            result(type(exc).__name__ == "WriteOnceViolation",
                   "dangling symlink:", type(exc).__name__,
                   "code=", getattr(exc, "code", None))

        # 4. Does the refusal object carry the refused value as exception state?
        refused_value = {"smuggled": "these bytes survive inside the exception object"}
        try:
            custody.write_new(target, refused_value)
        except Exception as exc:
            carried = any(refused_value == arg or (isinstance(arg, dict) and arg is refused_value)
                          for arg in exc.args)
            print("RESULT NOTE refusal object args:", exc.args,
                  "| refused value reachable from exception state:", carried)


if __name__ == "__main__":
    main()
