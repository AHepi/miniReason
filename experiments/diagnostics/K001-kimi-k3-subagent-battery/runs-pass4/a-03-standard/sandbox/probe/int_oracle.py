"""The module docstring claims: 'every integer in the built body lies under
guard_parameters or under role_contracts.word_limits'. Enumerate all ints."""
import json
import sys

sys.path.insert(0, "src")

from minireason.loop import standard as s

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
       if not (p.startswith("guard_parameters") or p.startswith("role_contracts.word_limits"))]
print("integers found:", len(found))
for p, v in found:
    print(" ", p, "=", v)
print("integers outside the two admitted sections:", bad or "NONE")
