import json, os, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = 'experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/plan.json'
d = json.load(open(os.path.join(ROOT, p)))
target = d['plan_id']
body = {k: v for k, v in d.items() if k != 'plan_id'}
for desc, s in [
    ('canonical-minus-planid', json.dumps(body, sort_keys=True, separators=(',', ':'))),
    ('canonical-indented', json.dumps(body, sort_keys=True, indent=2)),
]:
    print(desc, hashlib.sha256(s.encode()).hexdigest(), '== target?', hashlib.sha256(s.encode()).hexdigest() == target)
print('target', target)
