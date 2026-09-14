"""Probe: WAVE0-INTERFACE section 0's 'one owner' identity claims for contracts.

Every shared constant contracts re-exports must be the SAME object standard owns,
and READING_VOCABULARY must be the instrument's own published tuple.
"""
import sys

sys.path.insert(0, "src")

from minireason import use_relation_h005
from minireason.loop import contracts, standard

CHECKS = [
    ("READING_VOCABULARY", contracts.READING_VOCABULARY, standard.READING_VOCABULARY),
    ("CRITIC_RELATIONS", contracts.CRITIC_RELATIONS, standard.CRITIC_RELATIONS),
    ("UNRESOLVED", contracts.UNRESOLVED, standard.UNRESOLVED_TOKEN),
    ("NONE_RELATION", contracts.NONE_RELATION, standard.NONE_TOKEN),
    ("OUTSIDE_VOCABULARY_FIELD", contracts.OUTSIDE_VOCABULARY_FIELD, standard.OUTSIDE_VOCABULARY_FIELD),
    ("READING_BANNER", contracts.READING_BANNER, standard.READING_BANNER),
    ("MARKS", contracts.MARKS, standard.MARKS),
    ("REGISTERS", contracts.REGISTERS, standard.REGISTER_IDS),
    ("DIFFERENCE_KINDS", contracts.DIFFERENCE_KINDS, standard.DIFFERENCE_KINDS),
    ("ALL_DIFFERENCE_KINDS", contracts.ALL_DIFFERENCE_KINDS, standard.ALL_DIFFERENCE_KINDS),
    ("FORBIDDEN_KEYS", contracts.FORBIDDEN_KEYS, standard.FORBIDDEN_KEYS),
    ("ROLE_NAMES", contracts.ROLE_NAMES, standard.ROLE_NAMES),
    ("ROLE_BINDING_FIELDS", contracts.ROLE_BINDING_FIELDS, standard.ROLE_BINDING_FIELDS),
    ("WORD_LIMITS", contracts.WORD_LIMITS, standard.WORD_LIMITS),
    ("SCHEMAS", contracts.SCHEMAS, standard.SCHEMAS),
    ("CRITIC_SCHEMA", contracts.CRITIC_SCHEMA, standard.CRITIC_SCHEMA),
    ("DEFENDER_SCHEMA", contracts.DEFENDER_SCHEMA, standard.DEFENDER_SCHEMA),
    ("JUDGE_SCHEMA", contracts.JUDGE_SCHEMA, standard.JUDGE_SCHEMA),
    ("MARKER_SCHEMA", contracts.MARKER_SCHEMA, standard.MARKER_SCHEMA),
    ("VARIATOR_SCHEMA", contracts.VARIATOR_SCHEMA, standard.VARIATOR_SCHEMA),
    ("assert_no_scoring_headers", contracts.assert_no_scoring_headers, standard.assert_no_scoring_headers),
]
failures = 0
for name, got, owner in CHECKS:
    same = got is owner
    failures += not same
    print(f"{name:24s} identity={'SAME OBJECT' if same else 'DIFFERENT OBJECT'}")

print()
print("READING_VOCABULARY is the instrument's own tuple:",
      contracts.READING_VOCABULARY is use_relation_h005.ROOT_READING_VOCABULARY)
print("READING_BANNER is the instrument's own banner:  ",
      contracts.READING_BANNER is use_relation_h005.USE_RELATION_BANNER)
print("vocabulary values:", list(contracts.READING_VOCABULARY))
print("CRITIC_RELATIONS :", list(contracts.CRITIC_RELATIONS))
print("MARKS            :", list(contracts.MARKS))
print("REGISTERS        :", list(contracts.REGISTERS))
print("DIFFERENCE_KINDS :", {k: list(v) for k, v in contracts.DIFFERENCE_KINDS.items()})
print("ALL_DIFFERENCE_KINDS (sorted?):", list(contracts.ALL_DIFFERENCE_KINDS),
      "sorted =", list(contracts.ALL_DIFFERENCE_KINDS) == sorted(contracts.ALL_DIFFERENCE_KINDS))
print("FORBIDDEN_KEYS count:", len(contracts.FORBIDDEN_KEYS))
print("AGGREGATE_KEYS disjoint from FORBIDDEN_KEYS:",
      not (contracts.AGGREGATE_KEYS & contracts.FORBIDDEN_KEYS))
print("WORD_LIMITS:", {k: v for k, v in contracts.WORD_LIMITS.items()})
print("ROLE_NAMES:", list(contracts.ROLE_NAMES), " '| decider' present:", "decider" in contracts.ROLE_NAMES)
print("SCHEMA_REASONS count:", len(contracts.SCHEMA_REASONS))

# The wave-0 import-graph claim: types -> standard -> contracts, no cycle.
import minireason.loop.types as types_mod
print()
print("standard imports contracts:", "minireason.loop.contracts" in {
    m for m in sys.modules if m.startswith("minireason.loop")} and "contracts" in vars(standard))
print("types.FAILURE_CODES covers contracts' codes:",
      {"SCHEMA_INVALID", "CONTRACT_VIOLATION", "SCORING_KEY_FORBIDDEN"} <= types_mod.FAILURE_CODES)
print("SCHEMA_REASONS disjoint from FAILURE_CODES:",
      not (set(contracts.SCHEMA_REASONS) & types_mod.FAILURE_CODES))
print("SCHEMA_REASONS disjoint from BLOCK_CODES:",
      not (set(contracts.SCHEMA_REASONS) & types_mod.BLOCK_CODES))

sys.exit(1 if failures else 0)
