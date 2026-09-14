"""Probe: purity of check/validate (argument never mutated, no state), word-limit
behaviour and the boundary, booleans vs. the string word counter, and immutability.
"""
import copy
import sys

sys.path.insert(0, "src")

from minireason.loop import contracts
from minireason.loop.contracts import check, validate

CRITIC = {
    "relation": "repairs",
    "passage_quote": "the passage",
    "role_bindings": {"target": "t", "defect": "d", "grounds": "g", "bearing": "b"},
    "case": "the case",
    "outside_vocabulary": "",
}

# 1. The argument is never mutated - checked on three paths: success, schema failure,
#    and a program-rule failure.
for label, mutate in (
    ("success", lambda b: None),
    ("schema failure (unexpected field)", lambda b: b.update({"extra": 1})),
    ("program failure (case-required)", lambda b: b.update({"case": ""})),
):
    body = copy.deepcopy(CRITIC)
    mutate(body)
    snapshot = copy.deepcopy(body)
    check("critic", body)
    print(f"argument mutation on {label:34s}:", "MUTATED" if body != snapshot else "none")

# 2. Deterministic repeated failure selection.
trials = {
    tuple(check("critic", {**CRITIC, "case": "x " * 401}).path or ())
    for _ in range(5)
}
print("deterministic failure path across repeats:", trials)

# 3. Word-limit boundaries (whitespace-separated tokens: docstring deviation).
for n in (400, 401):
    v = check("critic", {**CRITIC, "case": "word " * n})
    print(f"critic case {n} words -> ok={v.ok} reason={v.reason!r}")
for n in (120, 121):
    v = check("marker", {"mark": "same", "difference_kind": None, "left_quote": "",
                         "right_quote": "", "case": "w " * n})
    print(f"marker case {n} words -> ok={v.ok} reason={v.reason!r}")
v = check("critic", {**CRITIC, "case": ""})
print("critic empty case with relation 'repairs':", v.reason)

# 4. A non-string in a word-limited field is a schema error, not a crash in the counter.
v = check("critic", {**CRITIC, "case": True})
print("critic case=True:", f"ok={v.ok}", "reason:", repr(v.reason))
v = check("critic", {**CRITIC, "case": 401})
print("critic case=401 (int):", f"ok={v.ok}", "reason:", repr(v.reason))

# 5. Variator: minItems / uniqueItems / per-item minLength all map to declared reasons.
for raw, label in (
    ({"paraphrases": []}, "empty list"),
    ({"paraphrases": ["x", "x"]}, "duplicate items"),
    ({"paraphrases": ["x", ""]}, "empty item"),
    ({"paraphrases": ["x", 1]}, "non-string item"),
):
    v = check("variator", raw)
    print(f"variator {label:16s} -> ok={v.ok} reason={v.reason!r} path={v.path}")

# 6. check never raises, on anything (documented contract).
weird = [None, 42, 3.14, b"\xff\xfe", "not json {", {"unexpected": 1},
         {"paraphrases": [0]}, Ellipsis, object()]
escaped = []
for raw in weird:
    try:
        check("variator", raw)
    except Exception as exc:  # noqa: BLE001 - we are proving it never happens
        escaped.append((repr(raw), type(exc).__name__))
print("check() raised on any input:", escaped if escaped else "never")

# 7. Module surfaces an attacker cannot rebind.
try:
    contracts.SCHEMAS["rogue"] = {}
except TypeError:
    print("contracts.SCHEMAS refuses a new role: TypeError")
try:
    contracts.WORD_LIMITS[("critic", "case")] = 1
except TypeError:
    print("contracts.WORD_LIMITS refuses a rewrite: TypeError")
schema = contracts.schema_for("critic")
schema["properties"]["relation"]["enum"] = ["anything"]
v = check("critic", {**CRITIC, "relation": "mimics"})
print("after editing a schema_for copy, enum still closed:", f"ok={v.ok}", v.reason)

# 8. Validation record shape on failure and on success.
v = check("critic", {**CRITIC, "extra": 1})
print("failure Validation:", v.ok, v.role, v.reason, v.path)
v = check("critic", CRITIC)
print("success Validation:", v.ok, v.role, type(v.value).__name__, v.reason, v.path)
