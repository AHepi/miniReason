import os, json, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEX64 = re.compile(r'^[0-9a-f]{64}$')
for dp, dns, fns in os.walk(ROOT):
    dns.sort(); fns.sort()
    if 'check' in dp or 'out' in dp.split(os.sep)[0]:
        continue
    for fn in fns:
        p = os.path.join(dp, fn)
        rel = os.path.relpath(p, ROOT)
        base = fn.lower()
        hits = []
        if 'manifest' in base or base.endswith('.sha256'):
            hits.append('NAME')
        if base.endswith('.json'):
            try:
                with open(p) as f:
                    data = json.load(f)
            except Exception as e:
                hits.append('JSON-PARSE-FAIL')
                data = None
            if isinstance(data, dict):
                for k, v in data.items():
                    if k in ('files', 'entries', 'sha256', 'digests', 'pins'):
                        shape = type(v).__name__
                        extra = ''
                        if isinstance(v, dict):
                            sample = list(v.items())[:2]
                            extra = repr(sample)[:160]
                        elif isinstance(v, list) and v and isinstance(v[0], dict):
                            keys = sorted(v[0].keys())
                            extra = 'item keys: %s' % keys
                        hits.append('KEY %s (%s) %s' % (k, shape, extra))
        if hits:
            print(rel, '=>', ' | '.join(hits))
