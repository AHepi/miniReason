"""Int oracle (fixed), forbidden-key count, ceiling <-> BLOCK_CODES correspondence,
and G2b judge schema check."""
import json
import sys

sys.path.insert(0, "src")

from minireason.loop import standard as s
from minireason.loop import types as t

# int oracle
body = json.loads(s.STANDARD_BODY)
found = []

def walk(value, path):
    if isinstance(value, bool):
        return
    if isinstance(value, int):
        found.append((path, value))
    elif isinstance(value, dict):
        for k, v in value.items():
            walk(v, f"{path}.{k}")
    elif isinstance(value, list):
        for i, v in enumerate(value):
            walk(v, f"{path}[{i}]")

walk(body, "")
bad = [(p, v) for p, v in found
       if not (p.lstrip(".").startswith("guard_parameters")
               or p.lstrip(".").startswith("role_contracts.word_limits"))]
print("integers outside the two admitted sections:", bad or "NONE")

# forbidden key count vs interface's "G12, 24 keys"
print("FORBIDDEN_KEYS count:", len(s.FORBIDDEN_KEYS))
print(sorted(s.FORBIDDEN_KEYS))

# ceiling clause 7 block reasons vs types
import re
clause7 = [c for c in s.CEILING_REQUIRED_SENTENCES if "block register" in c][0]
reasons = re.findall(r"`([a-z-]+)`", clause7)
print("ceiling clause 7 codes:", reasons)
print("types.CEILING_BLOCK_REASONS:", list(t.CEILING_BLOCK_REASONS))
print("sets equal:", set(reasons) == set(t.CEILING_BLOCK_REASONS))
prefixed = {"blocked:" + r for r in reasons}
print("all in BLOCK_CODES:", prefixed <= set(t.BLOCK_CODES))

# G2b in the judge schema: decisive_point must equal substring of case+answer;
# schema only enforces type+minLength
print("JUDGE decisive_point schema:", s.JUDGE_SCHEMA["properties"]["decisive_point"])
