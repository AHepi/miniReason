"""Probe 8: verify_pins over pin-map keys that are not plain strings.

The interface line is verify_pins(plan: Mapping[str, Any], repo). The
docstring's reason for requiring the "pins" envelope is: "a plan body whose
values all happened to be strings would be verified as a pin map, which is the
sort of silent misreading this module exists to refuse."

A JSON-loaded plan cannot carry a non-string key, but the public entry point
is any Mapping. The question: is a malformed pin map *named*, or can it slide
through the published seam as a non-custody exception / a silent pass?
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
        repo = Path(scratch)
        (repo / "a.py").write_bytes(b"x\n")

        # 1. Non-string key, well-formed-looking digest value.
        try:
            findings = custody.verify_pins({"pins": {7: "0" * 64}}, repo)
        except Exception as exc:
            ok = isinstance(exc, custody.CustodyMismatch)
            result(ok, "non-string key:", type(exc).__name__,
                   "code=", getattr(exc, "code", None), "| detail:", str(exc)[:80])
        else:
            result(False, "non-string key: verified with no complaint:", findings)

        # 2. Non-string key alongside a good key; sorted(key=str) orders them.
        good = custody.pins(repo, ["a.py"])
        try:
            findings = custody.verify_pins({"pins": {7: "0" * 64, **good}}, repo)
        except Exception as exc:
            print("RESULT NOTE mixed map:", type(exc).__name__, getattr(exc, "code", None))
        else:
            print("RESULT NOTE mixed map findings:",
                  [f.as_dict() for f in findings])

        # 3. A key that is a string but not a path anyone pinned: "pins" itself.
        findings = custody.verify_pins({"pins": {"pins": "0" * 64}}, repo)
        result([f.code for f in findings] == ["SOURCE_PIN_MISSING"],
               "key equal to the envelope's own name:", [f.code for f in findings])

        # 4. pins() over a non-string entry - the freeze-time mirror.
        try:
            custody.pins(repo, [7])
        except Exception as exc:
            ok = isinstance(exc, custody.CustodyMismatch)
            result(ok, "pins([7]):", type(exc).__name__, getattr(exc, "code", None),
                   "| detail:", str(exc)[:80])
        else:
            result(False, "pins([7]): pinned with no complaint")


if __name__ == "__main__":
    main()
