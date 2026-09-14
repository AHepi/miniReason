"""G12.  Acceptance (design-s7-wave-plan, W0-CONTRACTS): "a scoring key nested
anywhere raises SCORING_KEY_FORBIDDEN".

Docstring (contracts.assert_no_scoring_keys): "Mappings are checked by key and
descended; lists and tuples are descended by index."

Each carrier below holds the key 'score' somewhere.  "silent pass" means the
guard returned None.
"""
from __future__ import annotations

import collections
import dataclasses
import types as pytypes

import _boot  # noqa: F401

from minireason.loop import contracts


@dataclasses.dataclass(frozen=True)
class Cell:
    score: int


def offer(label, value):
    try:
        contracts.assert_no_scoring_keys(value)
    except contracts.ScoringKeyForbidden as exc:
        print(f"{label:<52} REFUSED at {exc.path}")
    except contracts.ContractError as exc:
        print(f"{label:<52} ContractError: {exc.detail[:60]}")
    else:
        print(f"{label:<52} silent pass")


offer("{'score': 1}                       (the control)", {"score": 1})
offer("[{'score': 1}]                     (the control)", [{"score": 1}])
offer("({'score': 1},)                    (the control)", ({"score": 1},))
offer("{'a': {'b': [{'score': 1}]}}       (the control)", {"a": {"b": [{"score": 1}]}})
offer("a frozen dataclass with a `score` field", Cell(1))
offer("a list holding that dataclass", [Cell(1)])
offer("SimpleNamespace(score=1)", pytypes.SimpleNamespace(score=1))
offer("collections.deque([{'score': 1}])", collections.deque([{"score": 1}]))
offer("a set of one frozenset-of-items", {frozenset({("score", 1)})})
offer("a generator over [{'score': 1}]", (x for x in [{"score": 1}]))
offer("dict_values of {'k': {'score': 1}}", {"k": {"score": 1}}.values())
offer("memoryview(b'| score |')", memoryview(b"| score |"))
offer("'| score |' (a rendered file)", "| score |")
offer("b'| score |' (rendered bytes)", b"| score |")

print()
print("the same rendered text through the scanner the docstring points at:")
try:
    contracts.assert_no_scoring_headers("| score | note |\n|---|---|\n| a | b |\n")
    print("  assert_no_scoring_headers: silent pass")
except Exception as exc:                              # noqa: BLE001
    print(f"  assert_no_scoring_headers: {type(exc).__name__}: {exc}")

print()
print("what the module's own published record objects are:")
crit = contracts.validate("critic", {
    "relation": "none", "passage_quote": "", "case": "",
    "role_bindings": {"target": "", "defect": "", "grounds": "", "bearing": ""},
    "outside_vocabulary": ""})
print("  type(validate('critic', ...)) =", type(crit).__name__,
      "- a dataclass:", dataclasses.is_dataclass(crit))
offer("  that CriticOutput handed straight to the guard", crit)
