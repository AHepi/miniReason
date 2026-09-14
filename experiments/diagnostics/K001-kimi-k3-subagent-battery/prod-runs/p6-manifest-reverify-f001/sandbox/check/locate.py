import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for dp, dns, fns in os.walk(ROOT):
    dns.sort()
    top = os.path.relpath(dp, ROOT).split(os.sep)[0]
    if top in ('check', 'out', 'src'):
        continue
    for fn in fns:
        if fn in ('arms.json', 'plan.json'):
            print(os.path.relpath(os.path.join(dp, fn), ROOT))
