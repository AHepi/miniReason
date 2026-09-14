"""The published shapes W0-STANDARD and notes/WAVE0-INTERFACE.md assert."""
from __future__ import annotations

import _boot  # noqa: F401

from minireason.loop import standard as S
from minireason import use_relation_h005 as U

print("READING_VOCABULARY          =", S.READING_VOCABULARY)
print("is ROOT_READING_VOCABULARY  =", S.READING_VOCABULARY is U.ROOT_READING_VOCABULARY)
print("NOMINABLE_RELATIONS         =", S.NOMINABLE_RELATIONS)
print("CRITIC_RELATIONS            =", S.CRITIC_RELATIONS)
print("MARKS                       =", S.MARKS)
print("REGISTERS is REGISTER_IDS   =", S.REGISTERS is S.REGISTER_IDS)
print("READING_BANNER is banner    =", S.READING_BANNER is U.USE_RELATION_BANNER)
print("DIFFERENCE_KINDS            =", dict(S.DIFFERENCE_KINDS))
print("ALL_DIFFERENCE_KINDS  n=%d" % len(S.ALL_DIFFERENCE_KINDS), S.ALL_DIFFERENCE_KINDS)
print("GUARD_PARAMETER_KEYS  n=%d" % len(S.GUARD_PARAMETER_KEYS))
print("CEILING clauses total       =", len(S.CEILING_TEXT.split("\n\n")))
print("CEILING_REQUIRED_SENTENCES n=", len(S.CEILING_REQUIRED_SENTENCES))
print("CEILING_CLAIM_TEMPLATE[:44] =", repr(S.CEILING_CLAIM_TEMPLATE[:44]))
print("CALIBRATION_ANCHORS n=%d must_sustain=%d" % (
    len(S.CALIBRATION_ANCHORS),
    sum(1 for a in S.CALIBRATION_ANCHORS if a.must_sustain)))
print("FALSIFIER_MAP keys          =", sorted(S.FALSIFIER_MAP))
for fid, f in sorted(S.FALSIFIER_MAP.items()):
    print("   %s carries=%s excludes=%s G? %s" % (
        fid, f.carrying_registers, f.excluded_registers, f.carries("G")))
print("STANDARD_BODY_SHA256        =", S.STANDARD_BODY_SHA256)
print("build twice byte-identical  =", S.build_standard() == S.build_standard() == S.STANDARD_BODY)

body = S.standard_body(S.STANDARD_BODY)
print("body rubric modes           =", {k: v["mode"] for k, v in body["rubric"].items()})
print("body marks                  =", body["marks"])
print("body registers              =", sorted(body["registers"]))

# The interface table calls every one of these a Mapping; which are writable?
import json
from types import MappingProxyType
for name in ("PLAN_8A_MIRROR", "PLAN_8A_REGISTERS", "DIFFERENCE_KINDS", "FALSIFIER_MAP",
             "GUARD_PARAMETERS", "RUBRIC_V1", "WORD_LIMITS", "SCHEMAS"):
    value = getattr(S, name)
    print("%-18s type=%-18s read-only=%s" % (
        name, type(value).__name__, isinstance(value, MappingProxyType)))
