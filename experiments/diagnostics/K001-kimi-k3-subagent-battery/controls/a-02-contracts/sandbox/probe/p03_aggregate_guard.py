"""`assert_no_aggregate_fields` claims three things.  Which of them does it check?

Docstring (contracts.assert_no_aggregate_fields):
  "A role output may name no quantity and hold none: no property name in
   FORBIDDEN_KEYS or AGGREGATE_KEYS, no ``number`` or ``integer`` type, and no
   open object through which one could arrive."

Each schema below is offered to the guard.  "PASSED" means the guard raised
nothing.  Every schema is then handed to Draft202012Validator to show that the
instance the guard was supposed to make inexpressible does in fact validate.
"""
from __future__ import annotations

import json

import _boot  # noqa: F401

from jsonschema import Draft202012Validator

from minireason.loop import contracts

CASES = [
    ("bare open object", {"type": "object"}, {"total": 3}),
    ("open object, no `properties` key, numeric additionalProperties",
     {"type": "object", "additionalProperties": {"type": "number"}},
     {"mean": 0.5}),
    ("closed at the top, open object nested under a declared property",
     {"type": "object", "additionalProperties": False,
      "properties": {"case": {"type": "object"}}},
     {"case": {"score": 9}}),
    ("patternProperties carrying a number",
     {"type": "object", "additionalProperties": False, "properties": {},
      "patternProperties": {"^x": {"type": "number"}}},
     {"xtally": 4}),
    ("propertyNames only",
     {"type": "object", "additionalProperties": False, "properties": {},
      "propertyNames": {"pattern": "^.*$"}},
     {}),
    ("numeric hidden behind $defs/$ref",
     {"type": "object", "additionalProperties": False,
      "$defs": {"n": {"type": "number"}},
      "properties": {"case": {"$ref": "#/$defs/n"}}},
     {"case": 7}),
    ("numeric hidden in then/else",
     {"type": "object", "additionalProperties": False,
      "properties": {"case": {"if": {"type": "string"},
                              "then": {"type": "string"},
                              "else": {"type": "integer"}}}},
     {"case": 12}),
    ("integer enumerated without a `type`",
     {"type": "object", "additionalProperties": False,
      "properties": {"case": {"enum": [0, 1, 2]}}},
     {"case": 2}),
    ("dependentSchemas carrying a number",
     {"type": "object", "additionalProperties": False,
      "properties": {"mark": {"type": "string"}},
      "dependentSchemas": {"mark": {"properties": {"case": {"type": "number"}}}}},
     {"mark": "same"}),
    ("a property literally named `count` (the control: this must be refused)",
     {"type": "object", "additionalProperties": False,
      "properties": {"count": {"type": "string"}}},
     {"count": "x"}),
    ("a top-level `number` (the control: this must be refused)",
     {"type": "number"}, 3),
]

for label, schema, instance in CASES:
    try:
        contracts.assert_no_aggregate_fields(schema)
        verdict = "PASSED the guard"
    except contracts.ContractError as exc:
        verdict = f"REFUSED: {exc.detail}"
    try:
        Draft202012Validator.check_schema(schema)
        errors = list(Draft202012Validator(schema).iter_errors(instance))
        admits = "no errors" if not errors else f"{len(errors)} error(s)"
    except Exception as exc:                            # noqa: BLE001
        admits = f"schema itself rejected: {type(exc).__name__}"
    print(f"- {label}\n    guard: {verdict}\n"
          f"    instance {json.dumps(instance)} against that schema: {admits}")
