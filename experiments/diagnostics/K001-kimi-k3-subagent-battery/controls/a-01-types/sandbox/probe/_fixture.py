"""Shared sys.path setup and one valid config fixture for the probes.

Mirrors run_tests.py: sandbox root and <root>/src on sys.path, nothing else.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _entry in (ROOT, os.path.join(ROOT, "src")):
    if _entry not in sys.path:
        sys.path.insert(0, _entry)

H1 = "1" * 64
H2 = "2" * 64
H3 = "3" * 64

CONFIG = {
    "run_id": "loop-001",
    "study": "C001",
    "occurrences": ["experiments/occurrences/c001-a"],
    "runner": "tools/multicycle_commitment_study_multi_v2.py",
    "cycle_budget": 3,
    "max_calls": 120,
    "reading_set": ["row-1", "row-2"],
    "obligations_path": "experiments/loops/loop-001/obligations.json",
    "graph_root": "experiments/loops/loop-001/graph",
    "reopen_reasons": ["new-material", "repaired-guard", "appellate-ruling"],
    "audit": {
        "period": 2,
        "judge_err_max": 0.2,
        "streak_max": 3,
        "judge_err_max_account": "0.2 is one wrong anchor of five; see design 2.5.",
        "streak_max_account": "Three blocked cycles in a row is an instrument fault.",
    },
}


def config():
    import copy

    return copy.deepcopy(CONFIG)


def show(label, fn, *args, **kwargs):
    """Run fn and print either its value or the exception class and code."""
    try:
        value = fn(*args, **kwargs)
    except BaseException as exc:  # noqa: BLE001 - a probe reports what it got
        code = getattr(exc, "code", None)
        print(f"{label}: raised {type(exc).__name__} code={code!r} msg={str(exc)!r}")
        return None
    print(f"{label}: returned {value!r}")
    return value
