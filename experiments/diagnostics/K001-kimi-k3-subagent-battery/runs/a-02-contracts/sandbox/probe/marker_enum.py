"""Probe: the marker schema's difference_kind enum admits NONE of the seven tokens.

The docstring claim under test (contracts.py, 'Deviations' section):
    'The marker schema closes ``difference_kind`` over :data:`ALL_DIFFERENCE_KINDS` ...
    so a token outside it is refused at the schema with reason ``not-in-enum`` before
    anything is registered.'
"""
import sys

sys.path.insert(0, "src")

from minireason.loop import contracts
from minireason.loop.contracts import ALL_DIFFERENCE_KINDS, check

MARKER = {
    "mark": "differs",
    "difference_kind": "grounds_source",
    "left_quote": "l",
    "right_quote": "r",
    "case": "c",
}

# 1. A differs mark on every allowed kind: accepted.
for kind in ALL_DIFFERENCE_KINDS:
    v = check("marker", {**MARKER, "difference_kind": kind}, register="G" if kind == "grounds_source" else None)
    print(f"allowed token {kind!r:30s} ok={v.ok} reason={v.reason!r}")

# 2. A token outside the closed set: docstring says reason = 'not-in-enum' from the SCHEMA.
v = check("marker", {**MARKER, "difference_kind": "made_up_kind"})
print()
print("unknown token, no register   :", f"ok={v.ok}", "reason:", repr(v.reason), "path:", v.path)
print("  message:", v.message)

# 3. Same with register= supplied.
v = check("marker", {**MARKER, "difference_kind": "made_up_kind"}, register="G")
print("unknown token, register='G'  :", f"ok={v.ok}", "reason:", repr(v.reason))

# 4. The per-register narrowing claim: a kind that is a real token of register T but
#    not of register G must be refused when register='G' and admitted otherwise.
v = check("marker", {**MARKER, "difference_kind": "target_set_membership"})
print("T-kind, union check          :", f"ok={v.ok}", "reason:", repr(v.reason))
v = check("marker", {**MARKER, "difference_kind": "target_set_membership"}, register="G")
print("T-kind on register G         :", f"ok={v.ok}", "reason:", repr(v.reason))
v = check("marker", {**MARKER, "difference_kind": "target_set_membership"}, register="Q")
print("differs + unknown register Q :", f"ok={v.ok}", "reason:", repr(v.reason))

# 5. Non-differs branches.
v = check("marker", {**MARKER, "mark": "same", "difference_kind": "grounds_source"}, register="G")
print("same + kind                  :", f"ok={v.ok}", "reason:", repr(v.reason))
v = check("marker", {**MARKER, "mark": "same", "difference_kind": None}, register="Q")
print("same + unknown register Q    :", f"ok={v.ok}", "reason:", repr(v.reason))
v = check("marker", {**MARKER, "difference_kind": None})
print("differs + null kind          :", f"ok={v.ok}", "reason:", repr(v.reason))
v = check("marker", {**MARKER, "difference_kind": "grounds_source", "left_quote": ""})
print("differs + empty left_quote   :", f"ok={v.ok}", "reason:", repr(v.reason))

# VALIDATORS forwards register= (O11 deviation).
v = contracts.VALIDATORS["marker"]({**MARKER, "difference_kind": "target_set_membership"}, register="G")
print("VALIDATORS['marker'], T-kind on G:", f"ok={v.ok}", "reason:", repr(v.reason))
