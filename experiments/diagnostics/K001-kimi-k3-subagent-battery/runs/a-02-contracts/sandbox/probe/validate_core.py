"""Probe: happy paths plus the branch coverage of _critic_failure / _marker_failure,
and the judge-schema floor for reading_note.
"""
import sys

sys.path.insert(0, "src")

from minireason.loop import contracts
from minireason.loop.contracts import (
    SchemaInvalid, check, difference_kinds_for, schema_for, validate,
)


def show(label, role, raw, register=None):
    v = check(role, raw, register=register)
    print(f"{label:52s} ok={v.ok!s:5s} reason={v.reason!r:28s} path={v.path!r}")
    return v


CRITIC_GOOD = {
    "relation": "repairs",
    "passage_quote": "the passage",
    "role_bindings": {"target": "t", "defect": "d", "grounds": "g", "bearing": "b"},
    "case": "the case",
    "outside_vocabulary": "",
}

# --- happy paths -----------------------------------------------------------
show("critic: nominated relation", "critic", CRITIC_GOOD)
show("critic: none ends the row, empty case ok", "critic",
     {**CRITIC_GOOD, "relation": "none", "passage_quote": "", "case": ""})
show("critic: outside_vocabulary, empty case ok", "critic",
     {**CRITIC_GOOD, "passage_quote": "", "case": "",
      "outside_vocabulary": "the real relation is mimicry"})
show("defender", "defender", {"answer": "no relation is established", "concedes": False})
show("judge: full", "judge",
     {"sustained": True, "decisive_point": "p", "reading_note": "the point stands"})
show("marker: differs + kind", "marker",
     {"mark": "differs", "difference_kind": "grounds_source",
      "left_quote": "l", "right_quote": "r", "case": "c"}, register="G")
show("marker: same + null kind", "marker",
     {"mark": "same", "difference_kind": None, "left_quote": "",
      "right_quote": "", "case": ""}, register="T")
show("variator", "variator", {"paraphrases": ["p1", "p2"]})
show("critic: raw arrives as JSON text", "critic", __import__("json").dumps(CRITIC_GOOD))
show("critic: raw arrives as bytes", "critic", __import__("json").dumps(CRITIC_GOOD).encode())

# --- critic branch coverage ---------------------------------------------------
show("critic: relation but empty case", "critic", {**CRITIC_GOOD, "case": ""})
show("critic: relation but empty passage", "critic", {**CRITIC_GOOD, "passage_quote": ""})
show("critic: relation outside enum", "critic", {**CRITIC_GOOD, "relation": "mimics"})
show("critic: unexpected field", "critic", {**CRITIC_GOOD, "severity": "high"})
show("critic: not json", "critic", "{not json")
show("critic: not an object", "critic", [1, 2])

# D6 normalisation: relation + outside_vocabulary is normalised, not refused.
out = validate("critic", {**CRITIC_GOOD, "outside_vocabulary": "mimicry"})
print("D6 normalised:", out.relation, "| nominated kept:", out.nominated_relation,
      "| text preserved:", out.outside_vocabulary)
print("claims_relation:", out.claims_relation, "| as_dict relation:", out.as_dict()["relation"])
try:
    out.relation = "repairs"
except Exception as exc:
    print("frozen record refuses mutation:", type(exc).__name__)

# --- judge: the reading_note floor -----------------------------------------
show("judge: EMPTY reading_note", "judge",
     {"sustained": True, "decisive_point": "p", "reading_note": ""})
show("judge: empty decisive_point", "judge",
     {"sustained": True, "decisive_point": "", "reading_note": "n"})

# --- schema_for deep copy -----------------------------------------------------
s = schema_for("judge")
s["properties"]["reading_note"]["minLength"] = 99
print("schema_for is a deep copy (module schema untouched):",
      "minLength" not in contracts.JUDGE_SCHEMA["properties"]["reading_note"])
try:
    schema_for("nope")
except SchemaInvalid as exc:
    print("schema_for unknown role:", exc.reason, "| code:", exc.code)
print("difference_kinds_for('E'):", difference_kinds_for("E"))
try:
    difference_kinds_for("Q")
except SchemaInvalid as exc:
    print("difference_kinds_for('Q'):", exc.reason)

# --- exception shapes ------------------------------------------------------------
try:
    validate("critic", {**CRITIC_GOOD, "case": ""})
except SchemaInvalid as exc:
    print("SchemaInvalid str:", str(exc))
    print("  .code:", exc.code, "| .reason:", exc.reason, "| .path:", exc.path,
          "| .detail:", repr(exc.detail))
    print("  isinstance LoopError / ValueError:", isinstance(exc, contracts.LoopError),
          isinstance(exc, ValueError))
e = contracts.ScoringKeyForbidden(("payload",))
print("ScoringKeyForbidden str:", repr(str(e)), "| .code:", e.code, "| .path:", e.path,
      "| detail:", repr(e.detail))
