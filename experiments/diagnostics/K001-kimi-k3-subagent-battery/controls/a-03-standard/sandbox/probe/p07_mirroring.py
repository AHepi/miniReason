"""What is mirrored, and what is retyped.

Design 2.1 requires "the six-value vocabulary **with its published
non-exclusivity note reproduced verbatim** from ``ROOT_READING_VOCABULARY``'s
docstring" and "the four C001 registers T/E/D/G **mirrored byte-identically from
PLAN 8a**".  Deviation 2 says the added ``difference_kind`` tokens "are only
distinctions PLAN 8a itself draws in the register it belongs to".
"""
from __future__ import annotations

import re

import _boot  # noqa: F401

from minireason.loop import standard as S


def flat(text: str) -> str:
    return " ".join(text.split())


print("-- register plan_text against data/plan_8a_mirror.json --")
for rid in S.REGISTER_IDS:
    mirrored = S.PLAN_8A_MIRROR["registers"][rid]
    reg = S.PLAN_8A_REGISTERS[rid]
    print("   %s plan_text identical=%s  reads identical=%s  differs_iff identical=%s" % (
        rid,
        reg.plan_text == mirrored["plan_text"],
        reg.reads == mirrored["reads"],
        reg.differs_iff == mirrored["differs_iff"]))

print()
print("-- each difference_kind's plan_grounding against that register's plan_text --")
for rid in S.REGISTER_IDS:
    plan = flat(S.PLAN_8A_REGISTERS[rid].plan_text)
    for kind in S.PLAN_8A_REGISTERS[rid].difference_kinds:
        g = flat(kind.plan_grounding)
        print("   %s %-28s quoted verbatim from plan_text: %s" % (rid, kind.token, g in plan))
        if g not in plan:
            print("      grounding : %s" % g)
            print("      plan_text : %s" % plan)

print()
print("-- VOCABULARY_NOTE against the published note in use_relation_h005 --")
src = open("src/minireason/use_relation_h005.py", encoding="utf-8").read()
block = re.search(r"((?:^#: .*\n)+)ROOT_READING_VOCABULARY = \(", src, re.M).group(1)
published = "\n".join(line[3:] for line in block.rstrip("\n").split("\n"))
print("   byte-identical:", published == S.VOCABULARY_NOTE)
if published != S.VOCABULARY_NOTE:
    print("   published:", repr(published[:120]))
    print("   standard :", repr(S.VOCABULARY_NOTE[:120]))
print("   imported rather than retyped:",
      any(S.VOCABULARY_NOTE is getattr(__import__(
          "minireason.use_relation_h005", fromlist=["x"]), n, None)
          for n in dir(__import__("minireason.use_relation_h005", fromlist=["x"]))))

print()
print("-- falsifier rules against the material mirror --")
for fid, f in sorted(S.FALSIFIER_MAP.items()):
    print("   %s rule is the material text: %s" % (
        fid, f.rule == S.PLAN_8A_MIRROR["material_register_to_falsifier"][fid]))
print("   PLAN prose in the body says G alone does not carry D1:",
      "`G` alone does not carry D1" in S.PLAN_8A_MIRROR["register_to_falsifier"])
