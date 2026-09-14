"""The ownership / identity claims contracts.py and the interface make.

Interface (notes/WAVE0-INTERFACE.md sec.0): "the names on both sides are the same
objects, asserted by identity (assertIs), not by equality" and
"READING_VOCABULARY (6 published values, the instrument's own tuple object)".

Interface (sec.3): "AGGREGATE_KEYS: frozenset[str]  # schema-name ban, wider than
FORBIDDEN_KEYS; NOT applied to artifacts".
Docstring (contracts.AGGREGATE_KEYS): "Wider than :data:`FORBIDDEN_KEYS`".
"""
from __future__ import annotations

import _boot  # noqa: F401

from minireason import use_relation_h005
from minireason.loop import contracts, standard

print("READING_VOCABULARY is ROOT_READING_VOCABULARY:",
      contracts.READING_VOCABULARY is use_relation_h005.ROOT_READING_VOCABULARY)
print("type(ROOT_READING_VOCABULARY):",
      type(use_relation_h005.ROOT_READING_VOCABULARY).__name__)
print("READING_BANNER is USE_RELATION_BANNER:",
      contracts.READING_BANNER is use_relation_h005.USE_RELATION_BANNER)

for name in ("READING_VOCABULARY", "CRITIC_RELATIONS", "MARKS", "REGISTERS",
             "DIFFERENCE_KINDS", "ALL_DIFFERENCE_KINDS", "FORBIDDEN_KEYS",
             "WORD_LIMITS", "SCHEMAS", "ROLE_NAMES", "ROLE_BINDING_FIELDS",
             "CRITIC_SCHEMA", "DEFENDER_SCHEMA", "JUDGE_SCHEMA",
             "MARKER_SCHEMA", "VARIATOR_SCHEMA"):
    here = getattr(contracts, name)
    there = getattr(standard, name if name != "REGISTERS" else "REGISTERS")
    print(f"  contracts.{name} is standard.{name}: {here is there}")

print()
print("AGGREGATE_KEYS >= FORBIDDEN_KEYS (i.e. 'wider'):",
      contracts.AGGREGATE_KEYS >= contracts.FORBIDDEN_KEYS)
print("AGGREGATE_KEYS & FORBIDDEN_KEYS:",
      sorted(contracts.AGGREGATE_KEYS & contracts.FORBIDDEN_KEYS))
print("len(AGGREGATE_KEYS)=", len(contracts.AGGREGATE_KEYS),
      " len(FORBIDDEN_KEYS)=", len(contracts.FORBIDDEN_KEYS))
missing = sorted(contracts.FORBIDDEN_KEYS - contracts.AGGREGATE_KEYS)
print("in FORBIDDEN_KEYS but NOT in AGGREGATE_KEYS:", missing)

print()
print("MARKS:", standard.MARKS)
print("MARKS comes from the shipped data file, not a literal:")
import json  # noqa: E402
raw = json.loads(standard.PLAN_8A_MIRROR_PATH.read_text(encoding="utf-8"))
print("  plan_8a_mirror.json['marks'] ==", raw["marks"],
      "  tuple(...) == standard.MARKS:", tuple(raw["marks"]) == standard.MARKS)
