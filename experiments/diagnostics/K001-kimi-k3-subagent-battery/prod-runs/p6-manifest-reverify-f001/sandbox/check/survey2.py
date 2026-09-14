import os, json, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEX64 = re.compile(r'^[0-9a-f]{64}$')
for dp, dns, fns in os.walk(ROOT):
    dns.sort(); fns.sort()
    rel0 = os.path.relpath(dp, ROOT)
    if rel0.split(os.sep)[0] not in ('experiments', 'docs'):
        continue
    for fn in sorted(os.listdir(dp)):
        p = os.path.join(dp, fn)
        if not os.path.isfile(p) or not fn.endswith('.json'):
            continue
        try:
            with open(p) as f:
                data = json.load(f)
        except Exception:
            continue
        rel = os.path.relpath(p, ROOT)
        # scan recursively: find dicts whose any value is hex64 with a sibling path-ish key
        def scan(o, trail):
            if isinstance(o, dict):
                vals = list(o.values())
                if any(isinstance(v, str) and HEX64.match(v) for v in vals):
                    keys = sorted(o.keys())
                    print(rel, trail, '->', keys)
                for k, v in o.items():
                    scan(v, trail + '.' + str(k))
            elif isinstance(o, list):
                for i, v in enumerate(o[:3]):
                    scan(v, trail + '[%d]' % i)
        scan(data, '')
