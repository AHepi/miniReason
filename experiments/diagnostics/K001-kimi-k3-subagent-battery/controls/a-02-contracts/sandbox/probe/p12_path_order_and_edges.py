"""Two smaller seams.

(a) _schema_failure docstring: "The first schema error, chosen deterministically
    (path, validator, text)."  The path is stringified before it is sorted.
(b) check() docstring: "Pass ``register`` to hold a marker's ``difference_kind``
    to that register's own closed token set".  What happens to a bad ``register``
    on a role that is not the marker?
(c) _as_object: "if not isinstance(raw, dict)".
"""
from __future__ import annotations

import types as pytypes
from types import MappingProxyType

import _boot  # noqa: F401

from minireason.loop import contracts

# (a) two bad items, at index 2 and index 10.
paraphrases = [f"p{i}" for i in range(12)]
paraphrases[2] = 1
paraphrases[10] = 2
out = contracts.check("variator", {"paraphrases": paraphrases})
print("(a) two type errors, at index 2 and index 10")
print("    reported path:", out.path, " reason:", out.reason)
print("    sorted as strings: sorted(['2','10']) ==", sorted(["2", "10"]))

# (b) a bogus register on a role that is not the marker.
for role, body in (
    ("critic", {"relation": "none", "passage_quote": "", "case": "",
                "role_bindings": {"target": "", "defect": "", "grounds": "",
                                  "bearing": ""},
                "outside_vocabulary": ""}),
    ("judge", {"sustained": True, "decisive_point": "d", "reading_note": ""}),
    ("defender", {"answer": "a", "concedes": False}),
    ("variator", {"paraphrases": ["a"]}),
):
    res = contracts.check(role, body, register="NOT-A-REGISTER")
    print(f"(b) check({role!r}, ..., register='NOT-A-REGISTER') -> ok={res.ok}, "
          f"reason={res.reason!r}")
marker_body = {"mark": "same", "difference_kind": None, "left_quote": "",
               "right_quote": "", "case": ""}
print("    check('marker', ..., register='NOT-A-REGISTER') ->",
      contracts.check("marker", marker_body, register="NOT-A-REGISTER").reason)

# (c) a Mapping that is not a dict.
frozen = MappingProxyType({"answer": "a", "concedes": False})
print("(c) MappingProxyType body ->", contracts.check("defender", frozen).reason)


class D(dict):
    pass


print("    dict subclass body     ->",
      contracts.check("defender", D({"answer": "a", "concedes": False})).reason)
print("    SimpleNamespace body   ->",
      contracts.check("defender",
                      pytypes.SimpleNamespace(answer="a", concedes=False)).reason)
