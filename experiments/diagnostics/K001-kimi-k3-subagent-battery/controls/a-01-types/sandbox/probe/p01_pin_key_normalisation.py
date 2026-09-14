"""Do two distinct pin maps mint one loop_plan_id, and does pin order matter?

Checks the wave-plan acceptance clause "a changed pin changes it" and the
package docstring's "Pin *order* does not affect the identity".
"""
from _fixture import H1, H2, H3, config  # noqa: E402

from minireason.loop import types  # noqa: E402

cfg = config()

print("--- 1. two spellings of one path, both accepted by _digests")
print("_digests:", types._digests({"src/a.py": H1, "./src/a.py": H2}, "pins", "PIN_INVALID"))

print()
print("--- 2. a pin that changes does NOT change the plan id")
a = types.loop_plan_id(cfg, {"src/a.py": H1, "./src/a.py": H2})
b = types.loop_plan_id(cfg, {"src/a.py": H3, "./src/a.py": H2})
print("pins A = {'src/a.py': H1, './src/a.py': H2} ->", a)
print("pins B = {'src/a.py': H3, './src/a.py': H2} ->", b)
print("H1 != H3 but ids equal:", a == b)

print()
print("--- 3. an added pin is silently dropped")
c = types.loop_plan_id(cfg, {"src/a.py": H1})
d = types.loop_plan_id(cfg, {"src/a.py": H1, "./src/a.py": H1})
print("one pin  ->", c)
print("two pins ->", d)
print("ids equal:", c == d)

print()
print("--- 4. pin ORDER changes the identity")
e = types.loop_plan_id(cfg, {"src/a.py": H1, "./src/a.py": H2})
f = types.loop_plan_id(cfg, {"./src/a.py": H2, "src/a.py": H1})
print("order 1 ->", e)
print("order 2 ->", f)
print("ids equal:", e == f)

print()
print("--- 5. the same hole in StepReceipt.key (inputs_sha256)")
plan = types.loop_plan_id(cfg, {"src/a.py": H1})
k1 = types.StepReceipt.key(plan, "SEND", 1, None, {"in/x.json": H1, "./in/x.json": H2})
k2 = types.StepReceipt.key(plan, "SEND", 1, None, {"in/x.json": H3, "./in/x.json": H2})
print("inputs {x: H1, ./x: H2} ->", k1)
print("inputs {x: H3, ./x: H2} ->", k2)
print("step keys equal:", k1 == k2)

print()
print("--- 6. contrast: _relatives (occurrences) DOES refuse the same collision")
try:
    types._relatives(["src/a.py", "./src/a.py"], "occurrences")
    print("_relatives: accepted")
except types.LoopError as exc:
    print("_relatives: raised LoopError code=%r msg=%r" % (exc.code, str(exc)))

print()
print("--- 7. other spellings that normalise together")
for spelling in ("src/a.py", "./src/a.py", "src//a.py", "src/./a.py", "src/a.py/."):
    print("  %-16r -> %r" % (spelling, types._relative(spelling, "pins key", "PIN_INVALID")))
