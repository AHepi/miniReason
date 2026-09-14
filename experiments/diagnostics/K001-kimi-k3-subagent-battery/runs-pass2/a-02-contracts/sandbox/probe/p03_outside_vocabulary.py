"""Probe 3: G4 / D6 — what check() actually returns for the two G4 shapes.

Design §2.4 G4: "Any token outside the six values ⇒ `unresolved`. A non-empty
`outside_vocabulary` ⇒ `unresolved:outside-vocabulary`, text preserved (D6)."
Design §2.3: "A non-empty `outside_vocabulary` forces `unresolved` with that
reason and preserves the text."

CriticOutput docstring: "Refusing would discard the very text D6 exists to
preserve" and "**normalised, not refused**: ``.relation`` becomes
:data:`NONE_RELATION`".
"""
import sys, os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import contracts
from minireason.loop.contracts import check, validate, CriticOutput
from minireason.loop import standard

reasons = set(__import__("minireason.loop.contracts", fromlist=["x"]).SCHEMA_REASONS)

# reachability of the three reasons the sweep missed
for role, raw, kw in [
    ("bogus-role", {}, {}),
    ("defender", {"answer": "", "concedes": True}, {}),
    ("variator", {"paraphrases": ["same", "same"]}, {}),
]:
    v = check(role, raw, **kw)
    print(f"reach {role}: ok={v.ok} reason={v.reason}")

BASE = {"relation": "re-deploys", "passage_quote": "p",
        "role_bindings": {"target": "t", "defect": "d", "grounds": "g",
                           "bearing": "b"},
        "case": "c", "outside_vocabulary": ""}

# G4 shape (a): relation token outside the six values
v = check("critic", {**BASE, "relation": "glosses"})
print(f"\n(a) relation='glosses': ok={v.ok} reason={v.reason} value={v.value}")

# G4 shape (b): NON-EMPTY outside_vocabulary WITH a named relation
v = check("critic", {**BASE, "outside_vocabulary": "glosses-as-praise"})
print(f"\n(b) relation + outside_vocabulary: ok={v.ok} reason={v.reason}")
out = v.value
print(f"    type={type(out).__name__}")
print(f"    .relation={out.relation!r}  .nominated_relation={out.nominated_relation!r}")
print(f"    .outside_vocabulary={out.outside_vocabulary!r}")
print(f"    .is_outside_vocabulary={out.is_outside_vocabulary}  .claims_relation={out.claims_relation}")
print(f"    .as_dict()={json.dumps(out.as_dict(), sort_keys=True)}")

# where does the token 'unresolved' appear? nowhere in the value or as_dict:
blob = json.dumps(out.as_dict())
print(f"    token 'unresolved' anywhere in as_dict(): {'unresolved' in blob}")
print(f"    token 'outside-vocabulary' (the reason) anywhere: {'outside-vocabulary' in blob}")

# (c) D6 normalisation is also applied by DIRECT construction, no check() involved
direct = CriticOutput(relation="repairs", passage_quote="p",
                      role_bindings=contracts.RoleBindings("t", "d", "g", "b"),
                      case="c", outside_vocabulary="x")
print(f"\n(c) direct CriticOutput: relation={direct.relation!r} "
      f"nominated={direct.nominated_relation!r}")

# (d) outside_vocabulary alone, relation 'none': what is lost?
v = check("critic", {**BASE, "relation": "none",
                     "outside_vocabulary": "some uncovered reading"})
o = v.value
print(f"\n(d) relation='none' + outside_vocabulary: ok={v.ok} "
      f"nominated={o.nominated_relation!r} relation={o.relation!r} "
      f"is_ov={o.is_outside_vocabulary}")
print("done")
