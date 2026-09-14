import os, json, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEX64 = re.compile(r'^[0-9a-f]{64}$')
base = 'experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01'
for rel in ('use-table/use_table.json',):
    with open(os.path.join(ROOT, base, rel)) as f:
        d = json.load(f)
    fr = d.get('files_read')
    print(rel, type(fr).__name__)
    if isinstance(fr, dict):
        for k, v in list(fr.items())[:5]:
            print(' MAP', k, '=>', repr(v)[:100])
    elif isinstance(fr, list):
        for v in fr[:5]:
            print(' LIST', repr(v)[:150])
print('---side_table artifacts sample')
with open(os.path.join(ROOT, base, 'import/side_table.json')) as f:
    d = json.load(f)
for k in ('artifacts', 'documents', 'records', 'labels', 'validity_nodes'):
    v = d.get(k)
    print(k, type(v).__name__, len(v) if hasattr(v, '__len__') else '')
    if isinstance(v, list) and v:
        print('  sample keys:', sorted(v[0].keys()) if isinstance(v[0], dict) else repr(v[0])[:120])
    elif isinstance(v, dict):
        kk = list(v.items())[:1]
        print('  sample:', repr(kk)[:200])
# audit.json sample
with open(os.path.join(ROOT, base, 'audit.json')) as f:
    d = json.load(f)
print('---audit invocations sample')
inv = d.get('invocations')
print(type(inv).__name__)
print(repr(inv)[:400] if not isinstance(inv, list) else repr(inv[:1])[:400])
