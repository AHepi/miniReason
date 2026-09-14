"""Probe 5: identity claims, difference_kinds_for, schema_for, VALIDATORS.

Claims tested:
 * Interface table: "the names on both sides are the same objects, asserted by
   identity (assertIs)".
 * MARKS comment: "the three marks, in PLAN §8a's order" (= the mirror file's
   order).
 * schema_for returns a DEEP copy "safe for a caller to embed or edit".
 * VALIDATORS forwards register= (O11).
"""
import sys, os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import contracts, standard
from minireason.use_relation_h005 import ROOT_READING_VOCABULARY, USE_RELATION_BANNER

pairs = [
    ("READING_VOCABULARY", contracts.READING_VOCABULARY, standard.READING_VOCABULARY),
    ("CRITIC_RELATIONS", contracts.CRITIC_RELATIONS, standard.CRITIC_RELATIONS),
    ("REGISTERS", contracts.REGISTERS, standard.REGISTER_IDS),
    ("DIFFERENCE_KINDS", contracts.DIFFERENCE_KINDS, standard.DIFFERENCE_KINDS),
    ("FORBIDDEN_KEYS", contracts.FORBIDDEN_KEYS, standard.FORBIDDEN_KEYS),
    ("SCHEMAS", contracts.SCHEMAS, standard.SCHEMAS),
    ("WORD_LIMITS", contracts.WORD_LIMITS, standard.WORD_LIMITS),
    ("ROLE_NAMES", contracts.ROLE_NAMES, standard.ROLE_NAMES),
    ("READING_BANNER", contracts.READING_BANNER, standard.READING_BANNER),
    ("MARKS", contracts.MARKS, standard.MARKS),
    ("CRITIC_SCHEMA", contracts.CRITIC_SCHEMA, standard.CRITIC_SCHEMA),
    ("UNRESOLVED", contracts.UNRESOLVED, standard.UNRESOLVED_TOKEN),
    ("assert_no_scoring_headers", contracts.assert_no_scoring_headers,
     standard.assert_no_scoring_headers),
]
for name, a, b in pairs:
    print(f"identity {name}: {a is b}")

print(f"\nvocabulary is the instrument's own tuple object: "
      f"{standard.READING_VOCABULARY is ROOT_READING_VOCABULARY}")
print(f"banner is the instrument's own string: {standard.READING_BANNER is USE_RELATION_BANNER}")

with open(os.path.join(ROOT, 'src/minireason/loop/data/plan_8a_mirror.json'),
          encoding='utf-8') as fh:
    mirror = json.load(fh)
print(f"MARKS == mirror marks order: {tuple(contracts.MARKS) == tuple(mirror['marks'])}"
      f"  marks={contracts.MARKS} mirror={tuple(mirror['marks'])}")

# REGISTERS vs register order in the mirror file
print(f"REGISTERS={contracts.REGISTERS}  mirror key order={tuple(mirror['registers'])}")

# schema_for deep-copy safety
s = contracts.schema_for("critic")
s["properties"]["relation"]["enum"].append("bogus")
s["additionalProperties"] = True
clean = contracts.CRITIC_SCHEMA["properties"]["relation"]["enum"]
print(f"\nschema_for: after mutating the copy, CRITIC_SCHEMA enum = {clean}")
try:
    contracts.schema_for("decider")
except Exception as exc:
    print(f"schema_for('decider'): raised {type(exc).__name__} "
          f"reason={getattr(exc, 'reason', '-')} code={exc.code}")

# difference_kinds_for
for reg in ("T", "E", "D", "G"):
    print(f"difference_kinds_for({reg!r}) = {contracts.difference_kinds_for(reg)}")
try:
    contracts.difference_kinds_for("bogus")
except Exception as exc:
    print(f"difference_kinds_for('bogus'): raised {type(exc).__name__} "
          f"role={getattr(exc, 'role', '-')!r} reason={exc.reason!r} "
          f"in SCHEMA_REASONS: {exc.reason in contracts.SCHEMA_REASONS}")

# VALIDATORS forwards register=
mk = {"mark": "differs", "difference_kind": "target_set_membership",
      "left_quote": "l", "right_quote": "r", "case": "c"}
v_union = contracts.VALIDATORS["marker"](mk)
v_reg_T = contracts.VALIDATORS["marker"](mk, register="T")
v_reg_G = contracts.VALIDATORS["marker"](mk, register="G")
print(f"\nVALIDATORS marker, union: ok={v_union.ok}")
print(f"VALIDATORS marker, register='T': ok={v_reg_T.ok}")
print(f"VALIDATORS marker, register='G': ok={v_reg_G.ok} reason={v_reg_G.reason}")

# ALL_DIFFERENCE_KINDS sorted claim ("the 7 tokens, sorted")
adk = contracts.ALL_DIFFERENCE_KINDS
print(f"\nALL_DIFFERENCE_KINDS={adk}")
print(f"sorted: {list(adk) == sorted(adk)}  len={len(adk)}")
print("done")
