"""Shared probe harness: put the sandbox's src/ on sys.path, run checks, print.

Every probe imports CHECK from here and prints "PASS <name> -- <detail>" for a
check that the module survives, and "FAIL <name> -- <detail>" for one it does
not. A probe exits 0 whether or not a FAIL printed: the printout IS the
finding, mirrored verbatim into review/standard.md.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _entry in (ROOT, os.path.join(ROOT, "src")):
    if _entry not in sys.path:
        sys.path.insert(0, _entry)


def check(name: str, ok: bool, detail: str = "") -> bool:
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" -- {detail}" if detail else ""))
    return ok
