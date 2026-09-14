"""Probe 6: schema shapes, parity, digest, purity, shared-object mutability.

Claims tested:
 * §2.3 variator contract publishes '["…", "…"]' (two paraphrases) and
   §2.1/2.4 freeze TRIAL_PARAPHRASE_N = 2; VARIATOR_SCHEMA has minItems 1 only.
 * standard deviation 6: body carries sha256(canonical(SCHEMAS)); recompute.
 * WORD_LIMITS: whitespace-separated tokens.
 * SCHEMAS is a MappingProxyType but the nested schema dicts are mutable and
   shared (module comment: "re-exported here" — what does mutation do to
   validate()?).
 * Purity: identical inputs give identical Validation across repeats.
"""
import sys, os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import contracts, standard
from deepreason_core.canonical import canonical_json, sha256_hex

vs = contracts.VARIATOR_SCHEMA["properties"]["paraphrases"]
print(f"variator paraphrases schema: {json.dumps(vs, sort_keys=True)}")
print(f"has maxItems: {'maxItems' in vs}  has fixed-length constraint: "
      f"{'minItems' in vs and vs.get('minItems') == vs.get('maxItems')}")
print(f"guard paraphrase_n frozen at: {standard.GUARD_PARAMETERS['paraphrase_n']}")
# the acceptance path: three paraphrases validate?
v = contracts.check("variator", {"paraphrases": ["a", "b", "c"]})
print(f"check 3 paraphrases: ok={v.ok}  -> {v.value}")

# digest cross-check: does sha256(canonical(SCHEMAS)) == body digest?
body = standard.standard_body(standard.STANDARD_BODY)
body_digest = body["role_contracts"]["schemas_sha256"]
recomputed = sha256_hex(canonical_json({r: standard.SCHEMAS[r] for r in sorted(standard.SCHEMAS)}))
print(f"\nbody schemas_sha256 == recomputed: {body_digest == recomputed}")
print(f"standard.ROLE_SCHEMAS_SHA256 matches too: "
      f"{standard.ROLE_SCHEMAS_SHA256 == body_digest}")

# word-limit counting: whitespace-separated
lim = contracts.WORD_LIMITS[("judge", "reading_note")]
print(f"\njudge reading_note limit = {lim}")
mkj = {"sustained": True, "decisive_point": "d"}
exact = " ".join(["w"] * lim)
over = " ".join(["w"] * (lim + 1))
tabs = "w\t" * (lim)  # glued by tabs: still whitespace-separated
nb = ("w" + " ") * lim  # NBSP-glued: NOT whitespace for str.split()? (' '.isspace() is True)
print(f"exact {lim} words ok: {contracts.check('judge', {**mkj, 'reading_note': exact}).ok}")
print(f"{lim+1} words ok: {contracts.check('judge', {**mkj, 'reading_note': over}).ok}")
print(f"{lim} tab-joined words ok: {contracts.check('judge', {**mkj, 'reading_note': tabs}).ok}")
print(f"{lim} NBSP-joined words ok (NBSP is space for split): "
      f"{contracts.check('judge', {**mkj, 'reading_note': nb}).ok}")
# multi-space runs don't inflate: one word 'w' + 400 spaces
v = contracts.check("judge", {**mkj, "reading_note": "w" + " " * 5000})
print(f"one word + 5000 spaces ok: {v.ok}")

# mutability of the SHARED schema object
mut = dict(contracts.SCHEMAS["defender"])  # shallow copy for reference of original
orig_required = list(contracts.DEFENDER_SCHEMA["required"])
print(f"\nSCHEMAS type: {type(contracts.SCHEMAS).__name__}")
proxy_blocked = False
try:
    contracts.SCHEMAS["defender"] = {}
except TypeError:
    proxy_blocked = True
print(f"top-level proxy blocks SCHEMAS['defender']=...: {proxy_blocked}")
contracts.DEFENDER_SCHEMA["required"].clear()   # mutate THROUGH the shared object
v = contracts.check("defender", {})
print(f"after clearing DEFENDER_SCHEMA['required'] in place: "
      f"check('defender', {{}}) ok={v.ok} reason={v.reason}")
# restore for subsequent probes in this process
contracts.DEFENDER_SCHEMA["required"].extend(orig_required)
v2 = contracts.check("defender", {})
print(f"after restore: check('defender', {{}}) ok={v2.ok} reason={v2.reason}")

# purity: same input, three calls, identical outcome
inp = {"relation": "none", "passage_quote": "", "role_bindings":
       {"target": "", "defect": "", "grounds": "", "bearing": ""},
       "case": "", "outside_vocabulary": ""}
sig = None
stable = True
for _ in range(3):
    v = contracts.check("critic", dict(inp))
    now = (v.ok, v.reason, repr(v.value))
    stable = stable and (sig is None or sig == now)
    sig = now
print(f"\nthree identical checks give identical outcome: {stable}")
print("done")
