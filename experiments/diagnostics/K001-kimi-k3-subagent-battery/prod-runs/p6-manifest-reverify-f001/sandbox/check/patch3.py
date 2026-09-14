p = 'check/run_all.py'
s = open(p).read()

old = """DIAG_TOKENS = {'artifacts', 'attempts', 'requests', 'responses', 'provider', 'traces',
               'briefs', 'preflight.json', 'arms.json', 'plan.json',
               'material.json', 'manifests'}
"""
new = """DIAG_TOKENS = {'artifacts', 'attempts', 'requests', 'responses', 'provider', 'traces',
               'briefs', 'preflight.json', 'arms.json', 'plan.json',
               'material.json', 'manifests'}

def study_prefixed(lit, cur_digest):
    "\"\"\"B001 inventory and similar: keys like '<STUDY>/<occurrence>/<subpath>'
    where STUDY names a diagnostics study root. Try under each matching study dir.\"\"\"
    first = lit.split('/', 1)[0]
    roots = [d for d in DIRS if os.path.basename(d) == first]
    if not roots or '/' not in lit:
        return None
    rest = lit.split('/', 1)[1]
    hits = []
    for r in roots:
        c = os.path.join(ROOT, r, rest).replace(os.sep, '/')
        if os.path.isfile(c):
            if hashlib.sha256(open(c, 'rb').read()).hexdigest() == cur_digest:
                hits.append((c, 'study-root-relative(hash-match)'))
            else:
                hits.append((c, 'study-root-relative'))
    # prefer hash matches
    for c, how in hits:
        if 'hash-match' in how:
            return c, how
    if hits:
        return hits[0]
    return None
"""
assert old in s
s = s.replace(old, new)

old2 = """def resolve(mdir, lit):
"""
new2 = """def resolve(mdir, lit):
"""
# now modify body: after sandbox-root check, add study_prefixed call
old3 = """    for c, how in cands:
        if os.path.isfile(c):
            return c, how
    if toks[0] in DIAG_TOKENS:
"""
new3 = """    for c, how in cands:
        if os.path.isfile(c):
            return c, how
    sp = study_prefixed(lit, cur_digest)
    if sp:
        return sp
    if toks[0] in DIAG_TOKENS:
"""
assert old3 in s
s = s.replace(old3, new3)
open(p, 'w').write(s)
print('patched')
