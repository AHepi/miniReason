"""D6 / G4: what survives the critic normalisation, and into what token?

CriticOutput docstring: "the nominated token is kept on :attr:`nominated_relation`
so nothing is lost, and the ``outside_vocabulary`` text is carried through
unaltered. ``.as_dict()`` emits the normalised relation, so what is recorded is
what a renderer reads."

Module docstring: "**G4** (closed vocabulary; a non-empty ``outside_vocabulary``
forces ``unresolved`` and the text is preserved)".

Design §2.3: "`relation: \"none\"` ends the row at one call: no trial, cell stays
unresolved.  A non-empty `outside_vocabulary` forces `unresolved` with that reason
and preserves the text."
contracts.NONE_RELATION docstring: "It is *not* a reading of ``unresolved``: the
cell was read and nothing was found".
"""
from __future__ import annotations

import json

import _boot  # noqa: F401

from minireason.loop import contracts

nominated = {
    "relation": "qualifies",
    "passage_quote": "the quoted passage",
    "role_bindings": {"target": "t", "defect": "d", "grounds": "g", "bearing": "b"},
    "case": "the case",
    "outside_vocabulary": "reads as a partial concession with a repair",
}
out = contracts.validate("critic", nominated)
print("seat sent relation      :", nominated["relation"])
print("out.relation            :", out.relation)
print("out.nominated_relation  :", out.nominated_relation)
print("out.is_outside_vocabulary:", out.is_outside_vocabulary)
print("out.claims_relation     :", out.claims_relation)
print("UNRESOLVED token        :", contracts.UNRESOLVED)
print("NONE_RELATION token     :", contracts.NONE_RELATION)
print("out.relation == UNRESOLVED:", out.relation == contracts.UNRESOLVED)

record = out.as_dict()
print()
print("as_dict() (what is recorded):", json.dumps(record, sort_keys=True))
print("'nominated_relation' in the record:", "nominated_relation" in record)

back = contracts.validate("critic", json.dumps(record))
print("re-validated from the record -> relation=", back.relation,
      " nominated_relation=", repr(back.nominated_relation))
print("round trip preserves the nomination:",
      back.nominated_relation == out.nominated_relation)

plain_none = dict(nominated, relation="none", outside_vocabulary="")
plain = contracts.validate("critic", plain_none)
print()
print("a plain `none` answer: relation=", plain.relation,
      " is_outside_vocabulary=", plain.is_outside_vocabulary,
      " claims_relation=", plain.claims_relation)
print("the two cases are distinguishable in the record only by "
      "`outside_vocabulary` being non-empty:",
      record["relation"] == plain.as_dict()["relation"])
