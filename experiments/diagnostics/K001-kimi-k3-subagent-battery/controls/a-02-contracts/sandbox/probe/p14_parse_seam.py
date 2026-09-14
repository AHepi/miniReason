"""What the parse in `_as_object` accepts on the provider's behalf.

Deviation 3: "``raw`` may arrive as JSON text. A provider hands back bytes.
Passing ``str``/``bytes`` is accepted and parsed; a parse failure is the reason
``not-json`` rather than a ``json`` exception escaping the contract layer."
"""
from __future__ import annotations

import json

import _boot  # noqa: F401

from minireason.loop import contracts

dup = ('{"relation": "retains", "passage_quote": "p", '
       '"role_bindings": {"target": "t", "defect": "d", "grounds": "g", '
       '"bearing": "b"}, "case": "c", "outside_vocabulary": "", '
       '"relation": "none"}')
out = contracts.check("critic", dup)
print("duplicate `relation` key in the provider's text:")
print("  raw text says       :", '"relation": "retains"  ... "relation": "none"')
print("  check -> ok=", out.ok, " value.relation=",
      getattr(out.value, "relation", None))
print("  json.loads on the same bytes gives:", json.loads(dup)["relation"])

print()
print("non-standard JSON literals the parser accepts:")
for text in ('{"paraphrases": [NaN]}', '{"paraphrases": [Infinity]}',
             '{"paraphrases": ["a"], }'):
    res = contracts.check("variator", text)
    print(f"  {text!r:<30} -> reason={res.reason!r}")

print()
print("byte forms:")
for raw in (b'\xef\xbb\xbf{"answer": "a", "concedes": false}',
            b'\xff\xfe',
            bytearray(b'{"answer": "a", "concedes": false}')):
    res = contracts.check("defender", raw)
    print(f"  {raw[:20]!r:<40} -> ok={res.ok} reason={res.reason!r}")
