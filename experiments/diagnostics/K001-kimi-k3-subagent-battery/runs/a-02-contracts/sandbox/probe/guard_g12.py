"""Probe: the G12 guard - key structures, ordering, case folding, rendered files,
and the assert_no_aggregate_fields schema audit.

The audit's own docstring (contracts.py) claims it refuses 'no ``number`` or
``integer`` type, and no open object through which one could arrive'; its
implementation inspects every schema position where such a type could hide.
"""
import copy
import sys

sys.path.insert(0, "src")

from jsonschema import Draft202012Validator

from minireason.loop import contracts, standard
from minireason.loop.contracts import (
    AGGREGATE_KEYS, FORBIDDEN_KEYS, ContractError, ScoringKeyForbidden,
    assert_no_aggregate_fields, assert_no_scoring_keys,
)


def attempt(label, fn, *args):
    try:
        fn(*args)
        print(f"{label:70s} -> PASSED SILENTLY (no exception)")
    except Exception as exc:
        print(f"{label:70s} -> {type(exc).__name__}({exc})")


def schema_probe(label, schema, instance):
    """Is `instance` admissible under `schema`, and does the audit see the schema?"""
    valid = not any(Draft202012Validator(schema).iter_errors(instance))
    print(f"    [{label}] the schema ADMITS {instance!r}: {valid}")
    attempt(label, assert_no_aggregate_fields, schema)


# ---- the artifact guard -----------------------------------------------------
attempt("deeply nested scoring key",
        assert_no_scoring_keys, {"a": [{"b": 1}, ({"c": {"rank": 3}},)], "d": []})
attempt("scoring key in a tuple (docstring: tool's guard does not descend here)",
        assert_no_scoring_keys, ({"score": 1},))
attempt("CASE-VARIANT key 'SCORE' (lowercased)",
        assert_no_scoring_keys, {"SCORE": 1})
attempt("non-str key coerced: {1.0: 'x'} -> '1.0'",
        assert_no_scoring_keys, {1.0: "x"})
attempt("'verdict' (O2: the vendored warrant's own field name)",
        assert_no_scoring_keys, {"verdict": "fail"})
attempt("a str VALUE containing a scoring word is content, never scanned",
        assert_no_scoring_keys, {"note": "the score is not recorded here"})
attempt("whole argument is a rendered file (str)",
        assert_no_scoring_keys, "# Readings\n\n| cell | score |\n|---|--|\n| a | 9 |\n")
attempt("whole argument is bytes",
        assert_no_scoring_keys, b"| rank |")

# Clean value must pass.
assert_no_scoring_keys({"readings": [{"cell": "c1", "note": "no scoring key", "n": 3}]})
print("clean nested value                                                        -> PASSED (correctly silent)")

# First-hit ordering: which key fires when several are present?
for value in (
    {"b": {"rank": 1}, "a": {"rank": 2}},
    {"a": {"rank": 2}, "b": {"rank": 1}},
    {"outer": {"z": [{"score": 1}, {"merit": 2}]}},
):
    try:
        assert_no_scoring_keys(value)
    except ScoringKeyForbidden as exc:
        print("first hit for", repr(value), "->", exc.path)

# AGGREGATE_KEYS is wider than FORBIDDEN_KEYS but is not part of the artifact guard.
attempt("artifact key 'count' (AGGREGATE but not FORBIDDEN)",
        assert_no_scoring_keys, {"count": 3})
print("FORBIDDEN_KEYS count:", len(FORBIDDEN_KEYS),
      "| AGGREGATE_KEYS count:", len(AGGREGATE_KEYS))

# ---- the schema audit: every position it claims to cover ---------------------
schema_probe("audit: numeric property type, closed object",
             {"type": "object", "additionalProperties": False,
              "properties": {"x": {"type": ["integer", "null"]}}},
             {"x": 3})
schema_probe("audit: open object (properties, no additionalProperties)",
             {"type": "object", "properties": {"x": {"type": "string"}}},
             {"x": "s", "count": 9})
schema_probe("audit: numeric under oneOf",
             {"anyOf": [{"type": "number"}, {"type": "string"}]}, 3.5)
schema_probe("audit: numeric under array items",
             {"type": "array", "items": {"type": "integer"}}, [7])
schema_probe("audit: aggregate field name nested in anyOf",
             {"type": "object", "additionalProperties": False,
              "properties": {"p": {"anyOf": [
                  {"type": "object", "additionalProperties": False,
                   "properties": {"confidence": {"type": "string"}}},
                  {"type": "null"}]}}},
             {"p": {"confidence": "high"}})
schema_probe("audit: numeric under allOf",
             {"allOf": [{"type": "integer"}]}, 4)
schema_probe("audit: numeric under prefixItems",
             {"type": "array", "prefixItems": [{"type": "number"}]}, [4.5, "x"])
schema_probe("audit: numeric under contains",
             {"type": "array", "contains": {"type": "number"}}, ["a", 4.5])

# ---- the positions the audit does NOT descend -------------------------------
schema_probe("audit: numeric under if/then (conditional)",
             {"if": {"properties": {"mark": {"const": "differs"}}},
              "then": {"properties": {"count": {"type": "number"}}}},
             None)  # admissibility checked separately below
schema_probe("audit: numeric under dependentSchemas",
             {"type": "object", "dependentSchemas":
              {"flag": {"properties": {"tally": {"type": "integer"}}}}},
             None)
schema_probe("audit: numeric under patternProperties (open object caught first?)",
             {"type": "object", "additionalProperties": False,
              "properties": {"x": {"type": "string"}},
              "patternProperties": {".*score.*": {"type": "integer"}}},
             {"x": "s", "my_score": 5})
schema_probe("audit: numeric under propertyNames",
             {"type": "object", "additionalProperties": False,
              "properties": {"x": {"type": "string"}},
              "propertyNames": {"enum": ["x", "count"]}},
             None)

print()
print("admissibility through an if/then numeric property:")
cond = {"if": {"properties": {"mark": {"const": "differs"}}},
        "then": {"properties": {"count": {"type": "number"}}}}
print("   {'mark': 'differs', 'count': 3} admissible:",
      not any(Draft202012Validator(cond).iter_errors({"mark": "differs", "count": 3})))
print("   {'mark': 'differs', 'count': 'three'} admissible (then violated?):",
      not any(Draft202012Validator(cond).iter_errors({"mark": "differs", "count": "three"})))
dep = {"type": "object", "dependentSchemas": {"flag": {"properties": {"tally": {"type": "integer"}}}}}
print("   dependentSchemas {'flag': 1, 'tally': 3} admissible:",
      not any(Draft202012Validator(dep).iter_errors({"flag": 1, "tally": 3})))

# ---- the import-time self-check on the five owned schemas ---------------------
assert_no_aggregate_fields(contracts.MARKER_SCHEMA)
print("MARKER_SCHEMA passes the schema audit                                     -> PASSED (correctly silent)")
for name, schema in contracts.SCHEMAS.items():
    assert_no_aggregate_fields(schema)
print("all five owned schemas pass the import-time audit                         -> PASSED")

broken = copy.deepcopy(dict(contracts.SCHEMAS))
broken["judge"]["properties"]["sustained"] = {"type": ["boolean", "integer"]}
attempt("a hypothetically numeric judge schema is caught",
        assert_no_aggregate_fields, broken["judge"])

# ---- the rendered-file header scanner (W0-STANDARD's, re-exported) -------------
attempt("rendered file with a score column HEADER",
        standard.assert_no_scoring_headers, "| cell | score |\n|---|---|\n| a | ok |\n")
attempt("rendered file, scoring word in a body ROW only",
        standard.assert_no_scoring_headers, "| cell | note |\n|---|---|\n| a | the score was ok |\n")
attempt("rendered file, heading carrying a scoring word",
        standard.assert_no_scoring_headers, "## Rank of cells\n\n| cell |\n|---|\n| a |\n")
attempt("the header scanner as re-exported by contracts, on a clean heading",
        contracts.assert_no_scoring_headers, "# quality control record\n")

# prose/title mentions of a scoring word are not field names.
schema_probe("schema whose title mentions 'rank' as prose",
             {"type": "object", "additionalProperties": False, "title": "no rank here",
              "properties": {"x": {"type": "string"}}}, {"x": "s"})
