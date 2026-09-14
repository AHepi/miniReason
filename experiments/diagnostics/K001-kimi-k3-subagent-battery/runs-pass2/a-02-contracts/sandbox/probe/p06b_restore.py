"""Probe 6b: shared-object mutability continued (fresh process).

Observation from p06: the top-level SCHEMAS proxy blocks replacement of a
role, but the nested schema dicts are the very objects the live
Draft202012Validator reads, so in-place mutation of a schema changes live
validation. Here: characterise what that does to validate() and check(),
then restore, then confirm purity of repeat calls on the untouched module.
"""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import contracts

# pristine behaviour
v0 = contracts.check("defender", {})
print(f"pristine: check('defender', {{}}) ok={v0.ok} reason={v0.reason}")

# in-place mutation of the shared schema: the kind a caller achieves without
# touching the proxy (schema_for() exists to hand out deep copies, but the
# published SCHEMAS itself exposes the originals).
saved = list(contracts.DEFENDER_SCHEMA["required"])
contracts.DEFENDER_SCHEMA["required"].clear()

# (1) a {} defender now escapes BOTH the schema gate and _build's KeyError?
try:
    v1 = contracts.check("defender", {})
    print(f"mutated : check returned ok={v1.ok} value={v1.value!r}")
except Exception as exc:
    print(f"mutated : check RAISED {type(exc).__name__}: {exc} "
          f"-- 'never raises' broken under in-place mutation")

# (2) a COMPLETE body still validates
try:
    v2 = contracts.check("defender", {"answer": "a", "concedes": True})
    print(f"mutated : full body ok={v2.ok} value={v2.value!r}")
except Exception as exc:
    print(f"mutated : full body RAISED {type(exc).__name__}: {exc}")

# (3) does the pinned digest still match? (It should: canonical(SCHEMAS) is
#     recomputed over the same (now-mutated) objects only if the caller does
#     so; the module's ROLE_SCHEMAS_SHA256 was frozen at import.)
from deepreason_core.canonical import canonical_json, sha256_hex
from minireason.loop import standard
now = sha256_hex(canonical_json({r: standard.SCHEMAS[r] for r in sorted(standard.SCHEMAS)}))
print(f"mutated : recomputed digest == pinned digest: "
      f"{now == standard.ROLE_SCHEMAS_SHA256}  "
      f"(False means the digest still points at the PRE-mutation schemas)")

# restore
contracts.DEFENDER_SCHEMA["required"].extend(saved)
v3 = contracts.check("defender", {})
print(f"restored: check('defender', {{}}) ok={v3.ok} reason={v3.reason}")
now2 = sha256_hex(canonical_json({r: standard.SCHEMAS[r] for r in sorted(standard.SCHEMAS)}))
print(f"restored: recomputed digest == pinned digest: "
      f"{now2 == standard.ROLE_SCHEMAS_SHA256}")

# purity on the restored module: strict equality of Validation objects
inp = {"mark": "same", "difference_kind": None,
       "left_quote": "", "right_quote": "", "case": ""}
runs = [contracts.check("marker", dict(inp)) for _ in range(3)]
print(f"three identical checks equal: {runs[0] == runs[1] == runs[2]}")
print("done")
