"""Probe: check() documents 'Never raises'. A provider hands back bytes; can a
pathological byte string escape the contract layer as something other than a
Validation?
"""
import sys

sys.path.insert(0, "src")

from minireason.loop.contracts import check

def build(depth, leaf='"x"'):
    return "[" * depth + leaf + "]" * depth

for depth in (100, 1_000, 10_000, 100_000):
    raw = build(depth)
    try:
        v = check("critic", raw)
        print(f"malformed-JSON depth {depth:>7}: returned Validation(ok={v.ok}, reason={v.reason!r})")
    except Exception as exc:  # noqa: BLE001 - we are hunting exactly this
        print(f"malformed-JSON depth {depth:>7}: ESCAPED as {type(exc).__name__}: {str(exc)[:70]!r}")

raw = ("[" * 100_000 + ']' * 100_000).encode()
try:
    v = check("variator", raw)
    print("bytes depth 100000: returned", f"Validation(ok={v.ok}, reason={v.reason!r})")
except Exception as exc:  # noqa: BLE001
    print("bytes depth 100000: ESCAPED as", type(exc).__name__)

# Deep nesting that IS valid JSON, pre-parsed by the caller, then handed in as a dict.
def deep_dict(depth):
    inner = "x"
    for _ in range(depth):
        inner = [inner]
    return {"relation": "none", "passage_quote": "", "role_bindings":
            {"target": "t", "defect": "d", "grounds": "g", "bearing": "b"},
            "case": "", "outside_vocabulary": "", "nested": inner}

for depth in (100, 500, 1_000, 5_000):
    try:
        v = check("critic", deep_dict(depth))
        print(f"pre-parsed deep dict depth {depth:>6}: Validation(ok={v.ok}, reason={v.reason!r}, path0={v.path[:1]!r})")
    except Exception as exc:  # noqa: BLE001
        print(f"pre-parsed deep dict depth {depth:>6}: ESCAPED as {type(exc).__name__}")

# And through the guard, whose own recursion has no depth guard either.
from minireason.loop.contracts import assert_no_scoring_keys
for depth in (100, 1_000, 5_000):
    value = "v"
    for _ in range(depth):
        value = {"k": value}
    try:
        assert_no_scoring_keys(value)
        print(f"guard depth {depth:>6}: PASSED silently")
    except Exception as exc:  # noqa: BLE001
        print(f"guard depth {depth:>6}: ESCAPED as {type(exc).__name__}")
