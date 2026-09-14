"""`check` is published as "never raises".  Which arguments make it raise?

Interface entry (notes/WAVE0-INTERFACE.md sec.3):
    check(role: str, raw: Any, *, register: str | None = None) -> Validation  # never raises
Docstring (contracts.check): "Never raises."
"""
from __future__ import annotations

import json
import sys

import _boot  # noqa: F401

from minireason.loop import contracts

GOOD_MARKER = {
    "mark": "differs",
    "difference_kind": "grounds_source",
    "left_quote": "l",
    "right_quote": "r",
    "case": "c",
}
GOOD_CRITIC = {
    "relation": "retains",
    "passage_quote": "p",
    "role_bindings": {"target": "t", "defect": "d", "grounds": "g", "bearing": "b"},
    "case": "c",
    "outside_vocabulary": "",
}


def attempt(label, fn):
    try:
        out = fn()
    except BaseException as exc:          # noqa: BLE001 - the point of the probe
        print(f"{label}: RAISED {type(exc).__name__}: {str(exc)[:90]}")
        return
    print(f"{label}: returned Validation(ok={out.ok}, reason={out.reason!r})")


attempt("check(role=['critic'], raw={})",
        lambda: contracts.check(["critic"], {}))
attempt("check(role={'a':1}, raw={})",
        lambda: contracts.check({"a": 1}, {}))
attempt("check(role=None, raw={})",
        lambda: contracts.check(None, {}))
attempt("check('marker', good, register=['T'])",
        lambda: contracts.check("marker", dict(GOOD_MARKER), register=["T"]))
attempt("check('marker', mark=same, register={'T':1})",
        lambda: contracts.check(
            "marker",
            {"mark": "same", "difference_kind": None, "left_quote": "",
             "right_quote": "", "case": ""},
            register={"T": 1}))
attempt("check('critic', good, register=['T'])  (register ignored for critic)",
        lambda: contracts.check("critic", dict(GOOD_CRITIC), register=["T"]))

deep = "[" * 200000 + "]" * 200000
attempt("check('critic', '[' * 200000 + ']' * 200000)  (200k-deep JSON text)",
        lambda: contracts.check("critic", deep))

deep_obj = json.dumps({"a": 1})
attempt("VALIDATORS['marker'](good, register=['T'])",
        lambda: contracts.VALIDATORS["marker"](dict(GOOD_MARKER), register=["T"]))

attempt("schema_for(['critic'])", lambda: contracts.schema_for(["critic"]))
attempt("difference_kinds_for(['T'])", lambda: contracts.difference_kinds_for(["T"]))
attempt("validate(['critic'], {})", lambda: contracts.validate(["critic"], {}))
print("python:", sys.version.split()[0], "recursionlimit:", sys.getrecursionlimit())
print("unused:", deep_obj[:0])
