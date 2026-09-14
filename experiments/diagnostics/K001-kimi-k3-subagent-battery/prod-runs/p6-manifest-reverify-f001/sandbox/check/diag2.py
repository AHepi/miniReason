import json, os
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, 'out', 'manifest-reverify.json')))
for m in d['manifests']:
    c = Counter(e['verdict'] for e in m['entries'])
    if c.get('MISSING') or not c.get('MATCH'):
        continue
    print('ALL MATCH:', m['path'], dict(c))
print('---- MISSING by (manifest-family, kind):')
pl = Counter((e['manifest'], e['kind']) for e in d['non_match_entries'])
agg = Counter()
for (man, k), v in pl.items():
    fam = man.rstrip('0123456789')
    agg[(fam.split('-')[0].split('/')[-1], k)] += v
for k, v in sorted(agg.items()):
    print(k, v)
print('---- missing entries whose resolution note is suffix-ambiguous or other:')
c2 = Counter(e['resolution'] for e in d['non_match_entries'])
print(c2)
print('---- one use_table MATCH examples (resolution kinds):')
for m in d['manifests']:
    if 'occurrence-01/use-table/use_table.json' in m['path'] and 'F002' in m['path']:
        c = Counter(e['resolution'] for e in m['entries'] if e['verdict'] == 'MATCH')
        print(m['path'], c)
        miss = [e for e in m['entries'] if e['verdict'] == 'MISSING']
        print(' missing sample:', [e['path'] for e in miss][:6])
        break
