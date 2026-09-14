"""Is the pre-registered guard content reachable and editable at run time?

Module docstring: "The schemas moved for one reason: a plan pins the standard body
by sha256, and until §2.3 was inside that body, editing a schema or a word limit
changed **no digest at all** - so §5's 'changing any threshold after first look
mints a new ``loop_plan_id``' did not reach the guard content this module holds.
The body now carries the word limits and ``sha256(canonical(SCHEMAS))``."

Nothing is written to any file here; the mutation is in this process only and is
undone at the end.
"""
from __future__ import annotations

import _boot  # noqa: F401

from minireason.loop import contracts, standard

BEFORE = standard.STANDARD_BODY_SHA256
print("SCHEMAS is a MappingProxyType:", type(contracts.SCHEMAS).__name__)
try:
    contracts.SCHEMAS["critic"] = {}
except TypeError as exc:
    print("SCHEMAS itself refuses assignment:", exc)

enum = contracts.CRITIC_SCHEMA["properties"]["relation"]["enum"]
print("CRITIC_SCHEMA['properties']['relation']['enum'] is a", type(enum).__name__,
      "->", enum)

body = {
    "relation": "outperforms",
    "passage_quote": "p",
    "role_bindings": {"target": "t", "defect": "d", "grounds": "g", "bearing": "b"},
    "case": "c",
    "outside_vocabulary": "",
}
print("before: check('critic', relation='outperforms') ->",
      contracts.check("critic", dict(body)).reason)

enum.append("outperforms")
contracts.WORD_LIMITS  # untouched; the word bound lives in a MappingProxyType
after_check = contracts.check("critic", dict(body))
print("after enum.append('outperforms'): check(...) -> ok=", after_check.ok,
      " value.relation=", getattr(after_check.value, "relation", None))
print("standard.STANDARD_BODY_SHA256 unchanged:",
      standard.STANDARD_BODY_SHA256 == BEFORE, BEFORE[:16] + "...")
print("standard.ROLE_SCHEMAS_SHA256 unchanged:",
      standard.ROLE_SCHEMAS_SHA256 ==
      standard._role_contracts_section()["schemas_sha256"])

enum.remove("outperforms")
print("restored: check('critic', relation='outperforms') ->",
      contracts.check("critic", dict(body)).reason)

print()
print("the same question for the per-register token set:")
print("  type(contracts.DIFFERENCE_KINDS) =",
      type(contracts.DIFFERENCE_KINDS).__name__)
print("  difference_kinds_for('Q') ->", end=" ")
try:
    contracts.difference_kinds_for("Q")
except contracts.SchemaInvalid as exc:
    print(f"SchemaInvalid({exc.reason})")
contracts.DIFFERENCE_KINDS["Q"] = ("invented_kind",)
print("  after DIFFERENCE_KINDS['Q'] = ('invented_kind',):",
      contracts.difference_kinds_for("Q"))
print("  check('marker', differs/grounds_source, register='Q') ->",
      contracts.check("marker", {"mark": "differs",
                                 "difference_kind": "grounds_source",
                                 "left_quote": "l", "right_quote": "r",
                                 "case": "c"}, register="Q").reason)
del contracts.DIFFERENCE_KINDS["Q"]
print("  restored; registers now:", sorted(contracts.DIFFERENCE_KINDS))
print("  WORD_LIMITS type:", type(contracts.WORD_LIMITS).__name__,
      "  FORBIDDEN_KEYS type:", type(contracts.FORBIDDEN_KEYS).__name__,
      "  AGGREGATE_KEYS type:", type(contracts.AGGREGATE_KEYS).__name__)
