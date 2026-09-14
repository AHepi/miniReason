import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = 'experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/use_table.json'
d = json.load(open(os.path.join(ROOT, p)))
for k in ('custody', 'method', 'banner', 'occurrence', 'scope'):
    print(k, '=>', repr(d.get(k))[:600])
