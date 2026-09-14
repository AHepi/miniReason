p = 'check/run_all.py'
s = open(p).read()

# 1) resolve(): remove suffix-match fallback, add occurrence-context resolution
old = """def resolve(mdir, lit):
    cands = []
    if mdir:
        cands.append((os.path.normpath(os.path.join(ROOT, mdir, lit)).replace(os.sep, '/'), 'manifest-dir'))
    cands.append((os.path.normpath(os.path.join(ROOT, lit)).replace(os.sep, '/'), 'sandbox-root'))
    # generic suffix match: paths in manifests can be shortened ("experiments/.../x.json")
    tail = lit.rsplit('/', 1)[-1]
    seen = set()
    for c, how in cands[:]:
        if c in seen:
            continue
        seen.add(c)
        if os.path.isfile(c):
            return c, how
    short = [f for f in EXP_FILES if f == lit or f.endswith('/' + lit)]
    if len(short) == 1:
        return short[0], 'suffix-match'
    if short:
        return None, 'suffix-ambiguous(%d)' % len(short)
    return None, None
"""
new = """DIAG_TOKENS = {'artifacts', 'attempts', 'requests', 'responses', 'provider', 'traces',
               'briefs', 'preflight.json', 'arms.json', 'plan.json',
               'material.json', 'manifests'}

def resolve(mdir, lit):
    "\"\"\"Order: manifest's own directory, then the occurrence dir named in that
    path (occurrence-NN), then sandbox root. Diagnostics-shape relative paths
    (artifacts/, requests/, ...; arms/plan/material/manifests) are looked up in the
    diagnostics occurrences: unique if one exists, else the hash-matching one.\"\"\"
    toks = lit.split('/')
    cands = []
    if mdir:
        cands.append((os.path.normpath(os.path.join(ROOT, mdir, lit)).replace(os.sep, '/'),
                      'manifest-dir'))
    if mdir:
        mo = re.search(r'occurrence-\\d+', mdir)
        if mo:
            cands.append((os.path.normpath(os.path.join(ROOT, mo.group(0), lit)).replace(os.sep, '/'),
                          'occurrence-dir'))
    cands.append((os.path.normpath(os.path.join(ROOT, lit)).replace(os.sep, '/'), 'sandbox-root'))
    for c, how in cands:
        if os.path.isfile(c):
            return c, how
    if toks[0] in DIAG_TOKENS:
        shape = [f for f in EXP_FILES
                 if f.startswith('experiments/diagnostics/') and '/' + lit in f[len('experiments/diagnostics') : ] and f.endswith('/' + lit)]
        shape = [f for f in shape if f.endswith(lit)]
        uniq = sorted(set(shape))
        if len(uniq) == 1:
            return os.path.join(ROOT, uniq[0]).replace(os.sep, '/'), 'diagnostics-suffix-unique'
        if uniq:
            hits = []
            for f in uniq:
                full = os.path.join(ROOT, f)
                if sha256_of(full) == cur_digest:
                    hits.append(full)
            if hits:
                return hits[0].replace(os.sep, '/'), 'diagnostics-hash-match(%d found, %d match)' % (len(uniq), len(hits))
    return None, None
"""
assert old in s
s = s.replace(old, new)

# 2) set cur_digest before resolve call
old2 = """    for e in m['entries']:
        lit = e['path']
        full, how = resolve(mdir, lit)
"""
new2 = """    for e in m['entries']:
        lit = e['path']
        cur_digest = e['digest']
        full, how = resolve(mdir, lit)
"""
assert old2 in s
s = s.replace(old2, new2)
open(p, 'w').write(s)
print('patched')
