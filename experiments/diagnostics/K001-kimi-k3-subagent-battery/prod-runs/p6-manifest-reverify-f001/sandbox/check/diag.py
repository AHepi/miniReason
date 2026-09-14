import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, 'out', 'manifest-reverify.json')))
from collections import Counter, defaultdict
by = defaultdict(Counter)
for m in d['manifests']:
    c = Counter(e['verdict'] for e in m['entry_results'])
    by[m['path']] = c
for k, c in by.items():
    print(k, dict(c))
miss = [e for e in d['non_match_entries'] if e['verdict'] == 'MISSING']
print('sample missing paths:')
for e in miss[:10]:
    print(' ', e['manifest'], '->', e['path'])
