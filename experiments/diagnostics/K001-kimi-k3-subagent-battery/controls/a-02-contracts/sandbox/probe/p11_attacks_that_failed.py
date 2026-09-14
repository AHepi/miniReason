"""Attacks on contracts.py that did NOT succeed.  Each line is the attack and
what the module did instead.

Claims under attack:
  Purity: "Every callable here is a pure function of its arguments. ... no
  argument is mutated".
  Acceptance: "no aggregate field is expressible"; "validators are pure".
  Docstring (_schema_failure): "The first schema error, chosen deterministically
  (path, validator, text)."
"""
from __future__ import annotations

import copy
import json

import _boot  # noqa: F401

from minireason.loop import contracts

CRITIC = {
    "relation": "retains",
    "passage_quote": "p",
    "role_bindings": {"target": "t", "defect": "d", "grounds": "g", "bearing": "b"},
    "case": "c",
    "outside_vocabulary": "",
}

# 1. Does check() mutate its argument, or leak state between calls?
arg = copy.deepcopy(CRITIC)
snapshot = copy.deepcopy(arg)
first = contracts.check("critic", arg)
second = contracts.check("critic", arg)
print("1. argument unchanged after two checks:", arg == snapshot,
      "| both ok:", first.ok and second.ok,
      "| identical Validation:", first == second)

# 2. Does the deep copy schema_for() hands out feed back into validation?
mine = contracts.schema_for("critic")
mine["properties"]["relation"]["enum"].append("outperforms")
print("2. after editing schema_for('critic')'s copy, check() still refuses "
      "'outperforms':",
      contracts.check("critic", dict(CRITIC, relation="outperforms")).reason)
print("   schema_for returns a fresh object each call:",
      contracts.schema_for("critic") is not contracts.schema_for("critic"),
      "| equal to the live schema:",
      contracts.schema_for("critic") == contracts.CRITIC_SCHEMA)

# 3. Can any numeric value reach a role output through a shipped schema?
NUMERIC = [
    ("critic", dict(CRITIC, case=1)),
    ("critic", dict(CRITIC, relation=1)),
    ("defender", {"answer": 1, "concedes": False}),
    ("defender", {"answer": "a", "concedes": 1}),
    ("judge", {"sustained": 1, "decisive_point": "d", "reading_note": "n"}),
    ("judge", {"sustained": True, "decisive_point": 1, "reading_note": "n"}),
    ("marker", {"mark": "same", "difference_kind": None, "left_quote": "",
                "right_quote": "", "case": 0}),
    ("marker", {"mark": 1, "difference_kind": None, "left_quote": "",
                "right_quote": "", "case": ""}),
    ("variator", {"paraphrases": [1]}),
    ("variator", {"paraphrases": 1}),
]
outcomes = [contracts.check(role, body).reason for role, body in NUMERIC]
print("3. every numeric value offered to a shipped schema was refused:",
      all(o is not None for o in outcomes), "->", sorted(set(outcomes)))

# 4. Is the reported first error stable under key-insertion order?
def shuffled(body, order):
    return {k: body[k] for k in order}

broken = {"answer": "", "concedes": "yes", "extra": 1}
orders = [("answer", "concedes", "extra"), ("extra", "concedes", "answer"),
          ("concedes", "answer", "extra")]
reports = [(contracts.check("defender", shuffled(broken, o)).reason,
            contracts.check("defender", shuffled(broken, o)).path) for o in orders]
print("4. same (reason, path) under three key orders:",
      len(set(reports)) == 1, "->", reports[0])

# 5. Word-limit boundary: is 400 admitted and 401 refused?
print("5. critic case of exactly 400 words:",
      contracts.check("critic", dict(CRITIC, case="w " * 400)).reason,
      "| 401 words:",
      contracts.check("critic", dict(CRITIC, case="w " * 401)).reason,
      "| 400 words across newlines:",
      contracts.check("critic", dict(CRITIC, case="w\n" * 400)).reason)

# 6. Can a forbidden key be smuggled into a role output?
print("6. critic with an extra 'score' key:",
      contracts.check("critic", dict(CRITIC, score=1)).reason,
      "| with 'verdict':",
      contracts.check("critic", dict(CRITIC, verdict="fail")).reason,
      "| role_bindings with an extra 'rank':",
      contracts.check("critic", dict(
          CRITIC, role_bindings=dict(CRITIC["role_bindings"], rank=1))).reason)

# 7. `from contracts import *` - does every promised name exist?
namespace: dict = {}
exec("from minireason.loop.contracts import *", namespace)   # noqa: S102
missing = [n for n in contracts.__all__ if n not in namespace]
print("7. every name in __all__ is importable:", not missing, "| missing:", missing)

# 8. Does validate() accept the exact §2.3 example bodies?
EXAMPLES = [
    ("critic", {"relation": "re-deploys", "passage_quote": "q",
                "role_bindings": {"target": "", "defect": "", "grounds": "",
                                  "bearing": ""},
                "case": "c", "outside_vocabulary": ""}),
    ("defender", {"answer": "a", "concedes": False}),
    ("judge", {"sustained": True, "decisive_point": "d", "reading_note": ""}),
    ("marker", {"mark": "unresolved", "difference_kind": None, "left_quote": "",
                "right_quote": "", "case": ""}),
    ("variator", {"paraphrases": ["one", "two"]}),
]
built = [type(contracts.validate(r, json.dumps(b))).__name__ for r, b in EXAMPLES]
print("8. the five §2.3 shapes validate and build:", built)

# 9. O11: the documented union fallback, reproduced.
print("9. marker differs/'target_set_membership' with register=None:",
      contracts.check("marker", {"mark": "differs",
                                 "difference_kind": "target_set_membership",
                                 "left_quote": "l", "right_quote": "r",
                                 "case": ""}).ok,
      "| with register='G':",
      contracts.check("marker", {"mark": "differs",
                                 "difference_kind": "target_set_membership",
                                 "left_quote": "l", "right_quote": "r",
                                 "case": ""}, register="G").reason)
