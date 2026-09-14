"""Acceptance (W0-CONTRACTS): "no ordering is defined on the vocabulary and no
aggregate field is expressible"; and the module's own "It ranks nothing: no member
of any vocabulary here is ordered against another, no field of any schema is
numeric, and there is no aggregate, count, majority or mean anywhere in a role's
output".

(a) walk every shipped schema and list every `type` it declares;
(b) walk every shipped schema for any property name in FORBIDDEN_KEYS or
    AGGREGATE_KEYS;
(c) scan contracts.py for an ordering operation applied to a vocabulary name.
"""
from __future__ import annotations

import os
import re

import _boot  # noqa: F401

from minireason.loop import contracts

types_seen: set[str] = set()
names_seen: list[str] = []


def walk(node, path=()):
    if isinstance(node, dict):
        declared = node.get("type")
        for name in ((declared,) if isinstance(declared, str)
                     else tuple(declared or ())):
            types_seen.add(name)
        for key, sub in (node.get("properties") or {}).items():
            names_seen.append("/".join((*path, str(key))))
            walk(sub, (*path, str(key)))
        for key in ("items", "contains", "not"):
            if key in node:
                walk(node[key], (*path, key))
        for key in ("anyOf", "oneOf", "allOf", "prefixItems"):
            for index, sub in enumerate(node.get(key) or ()):
                walk(sub, (*path, key, str(index)))


for role in sorted(contracts.SCHEMAS):
    walk(contracts.SCHEMAS[role], (role,))

print("(a) every `type` declared anywhere in the five schemas:", sorted(types_seen))
print("    'number' or 'integer' among them:",
      bool({"number", "integer"} & types_seen))
banned = contracts.FORBIDDEN_KEYS | contracts.AGGREGATE_KEYS
hits = [n for n in names_seen if n.rsplit("/", 1)[-1].lower() in banned]
print("(b) property names:", len(names_seen), "| any in FORBIDDEN_KEYS |"
      " AGGREGATE_KEYS:", hits)
for role in sorted(contracts.SCHEMAS):
    contracts.assert_no_aggregate_fields(contracts.SCHEMAS[role], (role,))
print("    assert_no_aggregate_fields on all five: no refusal")

SOURCE = os.path.join(_boot.ROOT, "src", "minireason", "loop", "contracts.py")
text = open(SOURCE, encoding="utf-8").read()
VOCAB = ("READING_VOCABULARY", "CRITIC_RELATIONS", "MARKS", "REGISTERS",
         "DIFFERENCE_KINDS", "ALL_DIFFERENCE_KINDS", "UNRESOLVED",
         "NONE_RELATION")
ORDERING = (r"sorted\(", r"\.index\(", r"max\(", r"min\(", r"\.sort\(",
            r"[<>]=?", r"enumerate\(")
print("(c) ordering operations applied to a vocabulary name in contracts.py:")
found = 0
for number, line in enumerate(text.split("\n"), 1):
    if not any(v in line for v in VOCAB):
        continue
    for pattern in ORDERING:
        if re.search(pattern, line):
            found += 1
            print(f"    line {number}: {line.strip()}  (matched {pattern!r})")
            break
print("    total:", found)
