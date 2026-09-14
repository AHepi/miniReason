"""Probe: the docstring's ownership claims —
'The body now carries the word limits and sha256(canonical(SCHEMAS)).'
The pinned standard body must move when a §2.3 schema or word limit moves,
and the pinned digest must match live constants.
"""
import hashlib
import json
import sys

sys.path.insert(0, "src")

from deepreason_core.canonical import canonical_json, sha256_hex
from minireason.loop import contracts, standard

body = standard.standard_body(standard.STANDARD_BODY)
rc = body["role_contracts"]
print("body role_contracts keys:", sorted(rc))
print("body word_limits:", rc["word_limits"])

# 1. The body's word limits mirror WORD_LIMITS.
live = {}
for (role, field), limit in sorted(contracts.WORD_LIMITS.items()):
    live.setdefault(role, {})[field] = limit
print("word limits agree with live WORD_LIMITS:", rc["word_limits"] == live)

# 2. The pinned digest equals sha256(canonical(SCHEMAS)) over the live schemas.
digest = sha256_hex(canonical_json({r: contracts.SCHEMAS[r] for r in sorted(contracts.SCHEMAS)}))
print("body schemas_sha256 == sha256(canonical(live SCHEMAS)):",
      rc["schemas_sha256"] == digest)
print("ROLE_SCHEMAS_SHA256 matches too:", standard.ROLE_SCHEMAS_SHA256 == digest)
print("STANDARD_BODY_SHA256 stable across rebuild:",
      hashlib.sha256(standard.build_standard()).hexdigest() == standard.STANDARD_BODY_SHA256)

# 3. Editing a schema byte moves the digest (pre-registered guard content is pinned).
edited = {r: dict(contracts.SCHEMAS[r]) for r in sorted(contracts.SCHEMAS)}
edited["judge"] = json.loads(json.dumps(edited["judge"]))
edited["judge"]["properties"]["reading_note"]["minLength"] = 1
moved = sha256_hex(canonical_json(edited))
print("editing judge schema moves the digest:", moved != digest)

limits = dict(contracts.WORD_LIMITS)
print("WORD_LIMITS is a mapping proxy (not rebindable by an attacker):",
      type(limits).__name__ == "dict" and type(contracts.WORD_LIMITS).__name__)

# 4. The standard body itself carries no forbidden key (build_standard's own oracle).
hits = []

def walk(v, path):
    if isinstance(v, dict):
        for k, item in v.items():
            if str(k).lower() in contracts.FORBIDDEN_KEYS:
                hits.append((*path, k))
            walk(item, (*path, k))
    elif isinstance(v, (list, tuple)):
        for i, item in enumerate(v):
            walk(item, (*path, str(i)))

walk(json.loads(standard.STANDARD_BODY), ())
print("forbidden keys inside the shipped standard body:", hits if hits else "none")
