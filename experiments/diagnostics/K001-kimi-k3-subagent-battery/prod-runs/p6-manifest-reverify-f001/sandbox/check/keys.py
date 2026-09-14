import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
names = ('audit.json', 'report.json', 'side_table.json', 'use_table.json', 'arms.json', 'plan.json', 'residue.json')
for dp, dns, fns in os.walk(os.path.join(ROOT, 'experiments')):
    for fn in fns:
        if fn in names:
            p = os.path.join(dp, fn)
            try:
                with open(p) as f:
                    d = json.load(f)
                ks = sorted(d.keys()) if isinstance(d, dict) else type(d).__name__
            except Exception as e:
                ks = 'ERR %s' % e
            print(os.path.relpath(p, ROOT), '->', ks)
