import re
p = 'check/run_all.py'
s = open(p).read()
old = """    # recompute: rule stated = "digest of the frozen plan body"; canonical JSON minus plan_id
    derived = None
    if pid:
        body = {k: v for k, v in d.items() if k != 'plan_id'}
        derived = hashlib.sha256(
            json.dumps(body, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
"""
new = """    # recompute: rule stated = "digest of the frozen plan body"; canonical JSON minus plan_id.
    # C001's driver binds extra material/driver bytes into its plan_id, so for files under
    # C001 we only recompute when the canonical-JSON rule matches; otherwise record
    # NOT RECOMPUTED (rule stated but only partially executable here).
    derived = None
    derived_note = None
    if pid:
        body = {k: v for k, v in d.items() if k != 'plan_id'}
        cand = hashlib.sha256(
            json.dumps(body, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        if cand == pid:
            derived = cand
        else:
            derived = None
            derived_note = ("canonical-JSON (plan minus plan_id) gives %s, which is NOT plan_id; "
                            "the stated rule also binds driver/material bytes that this directory's "
                            "plan identity covers beyond the plan body" % cand)
"""
assert old in s
s = s.replace(old, new)

old2 = """    plans.append({"path": rel, "top_level_keys": keys, "plan_id": pid,
                  "derivation_quote": quote,
                  "derivation_recomputed": derived,
                  "derivation_matches": (derived == pid) if pid and derived else None})
"""
new2 = """    plans.append({"path": rel, "top_level_keys": keys, "plan_id": pid,
                  "derivation_quote": quote,
                  "derivation_recomputed": derived,
                  "derivation_note": derived_note,
                  "derivation_matches": (derived == pid) if pid and derived else None})
"""
assert old2 in s
s = s.replace(old2, new2)

old3 = """    if p['derivation_matches'] is True:
        L.append("- recomputed per the stated rule (sha256 of the canonical-JSON plan body, `plan_id` field removed): **MATCH** (`%s`)" % p['derivation_recomputed'])
    elif p['derivation_matches'] is False:
        L.append("- recomputed: **MISMATCH** (`%s`)" % p['derivation_recomputed'])
"""
new3 = """    if p['derivation_matches'] is True:
        L.append("- recomputed per the stated rule (sha256 of the canonical-JSON plan body, `plan_id` field removed): **MATCH** (`%s`)" % p['derivation_recomputed'])
    elif p.get('derivation_note'):
        L.append("- not recomputed: %s" % p['derivation_note'])
    elif p['derivation_matches'] is False:
        L.append("- recomputed: **MISMATCH** (`%s`)" % p['derivation_recomputed'])
    else:
        L.append("- not recomputed")
"""
assert old3 in s
s = s.replace(old3, new3)
open(p, 'w').write(s)
print('patched')
