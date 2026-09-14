"""How deep does a provider's JSON text have to be before `check` raises?

Deviation 3 in the module docstring:
  "``raw`` may arrive as JSON text. A provider hands back bytes. Passing
   ``str``/``bytes`` is accepted and parsed; a parse failure is the reason
   ``not-json`` rather than a ``json`` exception escaping the contract layer."
"""
from __future__ import annotations

import sys

import _boot  # noqa: F401

from minireason.loop import contracts


def outcome(raw) -> str:
    try:
        out = contracts.check("critic", raw)
    except BaseException as exc:                      # noqa: BLE001
        return f"RAISED {type(exc).__name__}"
    return f"Validation(ok={out.ok}, reason={out.reason!r})"


for depth in (1, 100, 500, 900, 990, 995, 1000, 5000):
    text = "[" * depth + "]" * depth
    print(f"str  depth={depth:>5} ({len(text):>6} chars): {outcome(text)}")

# The same shape, arriving as bytes rather than str - the provider's real form.
for depth in (900, 990, 1000, 5000):
    deep = b'{"role_bindings":' * depth + b"1" + b"}" * depth
    print(f"bytes depth={depth:>5} ({len(deep):>6} bytes): {outcome(deep)}")

print("recursionlimit:", sys.getrecursionlimit())
