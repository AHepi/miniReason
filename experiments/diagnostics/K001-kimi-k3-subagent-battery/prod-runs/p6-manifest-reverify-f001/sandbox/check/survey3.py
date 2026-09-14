import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for dp, dns, fns in os.walk(os.path.join(ROOT, 'experiments')):
    dns.sort(); fns.sort()
    for fn in fns:
        b = fn.lower()
        if 'manifest' in b or b.endswith('.sha256') or 'sha256' in b or 'digest' in b:
            print(os.path.relpath(os.path.join(dp, fn), ROOT))
