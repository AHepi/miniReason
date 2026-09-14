"""Probe 12: AGGREGATE_KEYS application points.

Interface §3: "AGGREGATE_KEYS ... schema-name ban, wider than FORBIDDEN_KEYS;
NOT applied to artifacts".
"""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop.contracts import (
    assert_no_scoring_keys, assert_no_aggregate_fields, AGGREGATE_KEYS,
    FORBIDDEN_KEYS,
)

def outcome(fn, *a):
    try:
        fn(*a)
        return "passed"
    except Exception as exc:
        return f"raised {type(exc).__name__} code={getattr(exc, 'code', '-')}"

artifact = {"blocks": [{"reason": "blocked:schema", "count": 3}],
            "total": 7, "confidence_note": "n/a"}
print("artifact with 'count'/'total' keys under assert_no_scoring_keys:",
      outcome(assert_no_scoring_keys, artifact))

numeric_artifact = {"reading": "retains", "cycle": 3, "word_total": 42}
print("artifact with numeric values under assert_no_scoring_keys:",
      outcome(assert_no_scoring_keys, numeric_artifact))

bad_schema_num = {"type": "object", "additionalProperties": False,
                  "properties": {"n": {"type": "integer"}}}
print("schema with integer property:", outcome(assert_no_aggregate_fields, bad_schema_num))

bad_schema_open = {"type": "object", "properties": {"x": {"type": "string"}}}
print("schema open object (no additionalProperties False):",
      outcome(assert_no_aggregate_fields, bad_schema_open))

bad_schema_name = {"type": "object", "additionalProperties": False,
                   "properties": {"tally": {"type": "string"}}}
print("schema with property named 'tally':",
      outcome(assert_no_aggregate_fields, bad_schema_name))

print("AGGREGATE_KEYS disjoint from FORBIDDEN_KEYS:",
      AGGREGATE_KEYS.isdisjoint(FORBIDDEN_KEYS))
print("done")
