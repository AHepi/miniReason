import json, os
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, 'out', 'manifest-reverify.json')))
for e in d['non_match_entries']:
    if e['manifest'].endswith('inventory.json') or e['manifest'].endswith('PLAN.md'):
        print(e['manifest'], '|', e['kind'], '|', e['path'], '|', e['resolution'])
print('---use_table missing:')
seen = set()
for e in d['non_match_entries']:
    key = (e['path'])
    if 'use_table' in e['manifest'] and key not in seen:
        seen.add(key)
        print(e['manifest'].split('/')[2][:3], e['manifest'].split('/')[3], '|', e['path'])
