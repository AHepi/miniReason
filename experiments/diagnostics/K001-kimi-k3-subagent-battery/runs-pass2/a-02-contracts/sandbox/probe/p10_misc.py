"""Probe 10: remaining seams.

 * _critic_failure: 'none' / outside_vocabulary short-circuit on a passing
   schema (only reachable when case/quote are present but empty).
 * None/whitespace decisive_point on the judge (schema has minLength=1).
 * Exception hierarchy invariants (interface §3): ScoringKeyForbidden is a
   ContractError is a LoopError is a ValueError; SchemaInvalid likewise.
 * O2's premise: standard.FORBIDDEN_KEYS contains 'verdict' (the vendored
   warrant's field), so the guard refuses the vendored record (executed in
   p04b); the note pins a test in tests/loop/test_contracts.py — not shipped
   in this sandbox; check the name is referenced anywhere here.
 * The marker 'unresolved' mark with a difference_kind: forbidden.
"""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import contracts, standard
from minireason.loop.contracts import (
    check, ScoringKeyForbidden, SchemaInvalid, ContractError,
)
from minireason.loop.types import LoopError

# critic short-circuit needs a passing schema: give present-but-empty values
v = check("critic", {"relation": "none", "passage_quote": "",
                     "role_bindings": {"target": "", "defect": "",
                                       "grounds": "", "bearing": ""},
                     "case": "", "outside_vocabulary": ""})
print(f"critic 'none' with empty case/quote: ok={v.ok} "
      f"claims_relation={v.value.claims_relation}")

# named relation, present-but-empty case/quote -> program refusal
v = check("critic", {"relation": "retains", "passage_quote": "",
                     "role_bindings": {"target": "t", "defect": "d",
                                       "grounds": "g", "bearing": "b"},
                     "case": "", "outside_vocabulary": ""})
print(f"critic 'retains' empty quote+case: ok={v.ok} reason={v.reason} path={v.path}")
v = check("critic", {"relation": "retains", "passage_quote": "p",
                     "role_bindings": {"target": "t", "defect": "d",
                                       "grounds": "g", "bearing": "b"},
                     "case": "", "outside_vocabulary": ""})
print(f"critic 'retains' empty case only: ok={v.ok} reason={v.reason} path={v.path}")

# judge boundaries
v = check("judge", {"sustained": True, "decisive_point": "", "reading_note": ""})
print(f"judge empty decisive_point: ok={v.ok} reason={v.reason}")
v = check("judge", {"sustained": True, "decisive_point": "x", "reading_note": ""})
print(f"judge empty reading_note: ok={v.ok}")

# marker: unresolved mark with difference_kind
v = check("marker", {"mark": "unresolved", "difference_kind": "grounds_source",
                     "left_quote": "", "right_quote": "", "case": ""})
print(f"marker 'unresolved' + kind: ok={v.ok} reason={v.reason}")

# hierarchy invariants
print(f"\nhierarchy: ScoringKeyForbidden MRO -> "
      f"{[c.__name__ for c in ScoringKeyForbidden.__mro__]}")
print(f"str(ScoringKeyForbidden()) == 'SCORING_KEY_FORBIDDEN': "
      f"{str(ScoringKeyForbidden()) == 'SCORING_KEY_FORBIDDEN'}")
si = SchemaInvalid("critic", "wrong-type", "m")
print(f"SchemaInvalid is LoopError: {isinstance(si, LoopError)}, "
      f"is ValueError: {isinstance(si, ValueError)}")

# FORBIDDEN_KEYS membership relevant to O2
print(f"\n'verdict' in FORBIDDEN_KEYS: {'verdict' in standard.FORBIDDEN_KEYS}")

# does the pinned O2 test name exist anywhere in this sandbox?
for dirpath, _dirs, files in os.walk(ROOT):
    if "/probe" in dirpath:
        continue
    for fn in files:
        if fn.endswith((".py", ".md", ".json")):
            p = os.path.join(dirpath, fn)
            try:
                with open(p, encoding="utf-8", errors="ignore") as fh:
                    if "test_the_guard_refuses_the_vendored_warrants_own_verdict_field_name" in fh.read():
                        print("O2 pinned test name FOUND in", p)
            except OSError:
                pass
else:
    print("O2 pinned test name: not found under sandbox (tests not shipped)")
print("done")
