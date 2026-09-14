"""Probe 2: reason table completeness and exception invariants.

Claims tested:
 * "Every reason SchemaInvalid can name" is SCHEMA_REASONS (module docstring on
   the SCHEMA_REASONS constant).
 * Interface: "str(exc) is exactly SCORING_KEY_FORBIDDEN"; ScoringKeyForbidden
   path reporting.
 * Interface: ContractError is "(code=CONTRACT_VIOLATION, detail='')" with the
   wave-0 argument order.
 * SchemaInvalid: ".detail carry the location and the message" — interface says
   "`.path` and `.detail` carry the location and the message".
"""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import contracts
from minireason.loop.contracts import (
    SCHEMA_REASONS, SchemaInvalid, ScoringKeyForbidden, ContractError,
    CONTRACT_VIOLATION, SCORING_KEY_FORBIDDEN, SCHEMA_INVALID, check, validate,
)

# 2a: str(ScoringKeyForbidden) must be exactly the code
exc = ScoringKeyForbidden(("a", "b"))
print(f"2a str(ScoringKeyForbidden(('a','b'))) = {str(exc)!r}")
print(f"2a .code = {exc.code!r}  .path = {exc.path!r}  .detail = {exc.detail!r}")

# 2b: guard raises with exact str when key found via assert_no_scoring_keys
try:
    contracts.assert_no_scoring_keys({"x": [{"SCORE": 1}]})
except ScoringKeyForbidden as e:
    print(f"2b str = {str(e)!r} path = {e.path!r} detail = {e.detail!r}")

# 2c: SchemaInvalid detail/message split (interface: ".path and .detail carry
#     the location and the message"; module docstring: ".detail carry the
#     location and the message")
si = SchemaInvalid("critic", "missing-field", "no case field", ("case",))
print(f"2c str  = {str(si)!r}")
print(f"2c .detail = {si.detail!r}  .path = {si.path!r}  .code = {si.code!r}")

# 2d: every reason check() can emit is in SCHEMA_REASONS.
#     Sweep invalid bodies per role and collect reasons.
roles = ["critic", "defender", "judge", "marker", "variator"]
collector = set()

def see(role, raw, **kw):
    v = check(role, raw, **kw)
    if not v.ok:
        collector.add(v.reason)

for role in roles:
    see(role, None)
    see(role, "not json {")
    see(role, [])
    see(role, {})
    see(role, {"zzz": 1})
    see(role, "42")

GOOD = {
    "critic": {"relation": "re-deploys", "passage_quote": "p",
               "role_bindings": {"target": "t", "defect": "d", "grounds": "g",
                                  "bearing": "b"},
               "case": "c", "outside_vocabulary": ""},
    "defender": {"answer": "a", "concedes": False},
    "judge": {"sustained": True, "decisive_point": "d", "reading_note": "n"},
    "marker": {"mark": "differs", "difference_kind": "grounds_source",
                "left_quote": "l", "right_quote": "r", "case": "c"},
    "variator": {"paraphrases": ["one", "two"]},
}

# field-level damage on every field of every good body
import json
def variants(role, good):
    for key in good:
        for bad in (None, 0, True, [], {}, "x" * 3000, " "):
            yield role, {**good, key: bad}
for role in roles:
    for r, body in variants(role, GOOD[role]):
        see(r, body)
        see(r, json.dumps(body))

# word limits
see("critic", {**GOOD["critic"], "case": "w " * 401})
see("defender", {"answer": "w " * 401, "concedes": False})
see("judge", {**GOOD["judge"], "reading_note": "w " * 121})
see("marker", {**GOOD["marker"], "case": "w " * 121})
# program checks
see("critic", {**GOOD["critic"], "case": ""})
see("critic", {**GOOD["critic"], "passage_quote": ""})
see("marker", {**GOOD["marker"], "difference_kind": None})
see("marker", {**GOOD["marker"], "left_quote": ""})
see("marker", {**GOOD["marker"], "right_quote": ""})
see("marker", {**GOOD["marker"], "mark": "same"})
see("marker", {**GOOD["marker"], "difference_kind": "target_set_membership"},
    register="G")
see("marker", {**GOOD["marker"], "mark": "same", "difference_kind": None},
    register="bogus-register")

extra = sorted(collector - set(SCHEMA_REASONS))
unused = sorted(set(SCHEMA_REASONS) - collector)
print(f"2d reasons emitted by check(): {sorted(collector)}")
print(f"2d reasons emitted but NOT in SCHEMA_REASONS: {extra}")
print(f"2d SCHEMA_REASONS members not produced by this sweep: {unused}")
print("done")
