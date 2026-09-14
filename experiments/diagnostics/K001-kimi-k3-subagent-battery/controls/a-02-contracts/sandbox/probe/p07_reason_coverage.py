"""Acceptance (design-s7-wave-plan, W0-CONTRACTS): "every malformed fixture
raises SchemaInvalid naming its reason".

One fixture per member of SCHEMA_REASONS.  For each, print the reason `check`
returned and the reason `validate` raised, and flag any member of SCHEMA_REASONS
no fixture reaches.
"""
from __future__ import annotations

import _boot  # noqa: F401

from minireason.loop import contracts

CRITIC = {
    "relation": "retains",
    "passage_quote": "p",
    "role_bindings": {"target": "t", "defect": "d", "grounds": "g", "bearing": "b"},
    "case": "c",
    "outside_vocabulary": "",
}
MARKER = {
    "mark": "differs",
    "difference_kind": "grounds_source",
    "left_quote": "l",
    "right_quote": "r",
    "case": "c",
}


def critic(**over):
    body = {k: (dict(v) if isinstance(v, dict) else v) for k, v in CRITIC.items()}
    body.update(over)
    return body


def marker(**over):
    body = dict(MARKER)
    body.update(over)
    return body


FIXTURES = [
    ("unknown-role", ("decider", {}), {}),
    ("not-json", ("critic", "{not json"), {}),
    ("not-an-object", ("critic", "[1,2]"), {}),
    ("missing-field", ("defender", {"answer": "a"}), {}),
    ("unexpected-field", ("defender", {"answer": "a", "concedes": False,
                                       "score": 1}), {}),
    ("wrong-type", ("defender", {"answer": "a", "concedes": "yes"}), {}),
    ("not-in-enum", ("critic", critic(relation="outperforms")), {}),
    ("empty-field", ("defender", {"answer": "", "concedes": False}), {}),
    ("too-few-items", ("variator", {"paraphrases": []}), {}),
    ("not-unique", ("variator", {"paraphrases": ["a", "a"]}), {}),
    ("word-limit", ("critic", critic(case="w " * 401)), {}),
    ("case-required", ("critic", critic(case="")), {}),
    ("passage-quote-required", ("critic", critic(passage_quote="")), {}),
    ("difference-kind-required", ("marker", marker(difference_kind=None)), {}),
    ("difference-kind-forbidden", ("marker", marker(mark="same")), {}),
    ("difference-kind-unknown", ("marker", marker()), {"register": "T"}),
    ("quote-required", ("marker", marker(left_quote="")), {}),
    ("unknown-register", ("marker", marker()), {"register": "Z"}),
]

seen = set()
for expected, (role, raw), kwargs in FIXTURES:
    out = contracts.check(role, raw, **kwargs)
    try:
        contracts.validate(role, raw, **kwargs)
        raised = "DID NOT RAISE"
    except contracts.SchemaInvalid as exc:
        raised = f"SchemaInvalid(reason={exc.reason!r}, path={exc.path})"
    seen.add(out.reason)
    flag = "" if out.reason == expected else "   <-- NOT the expected reason"
    print(f"{expected:<24} check -> {out.reason!r:<26} validate -> {raised}{flag}")

print()
print("members of SCHEMA_REASONS no fixture above reached:",
      [r for r in contracts.SCHEMA_REASONS if r not in seen])
print("reasons produced that are NOT in SCHEMA_REASONS:",
      sorted(r for r in seen if r not in contracts.SCHEMA_REASONS))
