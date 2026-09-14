"""The seam between custody.verify_pins' notion of a well-formed pin map and
types.loop_plan_id's, which is the function that folded those pins into the
plan identity in the first place (design 4.2).
"""
import _boot  # noqa: F401
import sys
import tempfile
from pathlib import Path

from minireason.loop import custody
from minireason.loop import types as t

print("python:", sys.version.split()[0])

CONFIG = {
    "schema": t.CONFIG_SCHEMA,
    "run_id": "RUN-0001",
    "study": "C001",
    "occurrences": ["experiments/occ/one"],
    "runner": "tools/runner_v2.py",
    "cycle_budget": 3,
    "max_calls": 100,
    "reading_set": ["row-1"],
    "obligations_path": "experiments/obligations.json",
    "graph_root": "experiments/graph",
    "reopen_reasons": ["new-material"],
    "audit": {"period": 1, "judge_err_max": 0.2, "streak_max": 3,
              "judge_err_max_account": "a", "streak_max_account": "b"},
}
GOOD = "a" * 64


def plan_id(pinmap, label):
    try:
        t.loop_plan_id(CONFIG, pinmap)
    except t.LoopError as exc:
        print(f"  loop_plan_id({label:<28}) -> {exc.code}: {exc.detail}")
    else:
        print(f"  loop_plan_id({label:<28}) -> accepted")


with tempfile.TemporaryDirectory() as tmp:
    repo = Path(tmp).resolve()
    (repo / "src").mkdir()
    f = repo / "src" / "a.py"
    f.write_bytes(b"one\n")
    real = custody.sha256_path(f)

    cases = [
        ("digest + trailing \\n", {"src/a.py": real + "\n"}),
        ("digest + trailing space", {"src/a.py": real + " "}),
        ("UPPERCASE digest", {"src/a.py": real.upper()}),
        ("backslash key", {"src\\a.py": real}),
        ("absolute key inside repo", {str(f): real}),
        ("'./'-prefixed key", {"./src/a.py": real}),
        ("trailing-slash key", {"src/a.py/": real}),
    ]
    for label, pinmap in cases:
        print(label)
        findings = custody.verify_pins({"pins": pinmap}, repo)
        print(f"  verify_pins({label:<28}) -> "
              f"{[ (x.code, x.path) for x in findings ] or 'CLEAN'}")
        plan_id(pinmap, label)

    # symlink loop under the repo: does the fence still name its refusal?
    import os
    os.symlink(repo / "loopb", repo / "loopa")
    os.symlink(repo / "loopa", repo / "loopb")
    for fn, label in ((lambda: custody.fenced(repo, "loopa"), "fenced(repo,'loopa')"),
                      (lambda: custody.pins(repo, ["loopa"]), "pins(repo,['loopa'])"),
                      (lambda: custody.verify_pins({"pins": {"loopa": GOOD}}, repo),
                       "verify_pins loopa")):
        try:
            out = fn()
        except custody.CustodyMismatch as exc:
            print(f"{label:<28} REFUSED {exc.code}")
        except Exception as exc:  # noqa: BLE001
            print(f"{label:<28} ESCAPED {type(exc).__name__}: {exc}")
        else:
            print(f"{label:<28} OK {out}")
