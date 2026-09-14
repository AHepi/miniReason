import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, 'out', 'manifest-reverify.json')))
md = open(os.path.join(ROOT, 'out', 'manifest-reverify.md')).read()
errs = []
t = d['totals']
assert t['MISMATCH'] == 0 and t['UNPARSED'] == 0, t
assert len(d['non_match_entries']) == t['MISSING']
assert t['MATCH'] == 2353 and t['MISSING'] == 104, t
assert d['credential_scan']['hit_count'] == 0
for k in ('What this walk would not catch', 'Credential scan', 'plan.json files', 'Summary',
          'Every non-MATCH entry', 'Completeness claims'):
    assert k in md, k
# confirm plans section text present
assert 'derivation' in md
# plan results: 11 MATCH + 2 C001 not-recomputed
pm = [p for p in d['plan_json'] if p['derivation_matches'] is True]
pn = [p for p in d['plan_json'] if p['derivation_matches'] is None]
assert len(pm) == 11 and len(pn) == 2, (len(pm), len(pn))
assert all('C001' in p['path'] for p in pn)
assert all('F00' in p['path'] for p in pm)
print('OK', json.dumps(t))
