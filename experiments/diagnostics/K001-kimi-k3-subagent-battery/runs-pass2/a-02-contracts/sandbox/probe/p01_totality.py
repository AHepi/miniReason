"""Probe 1: contracts.check claims "Never raises."

Docstring of check(): "Validate ``raw`` as ``role``'s output and **return** the
outcome. Never raises."

Feed boundary inputs at exactly-passing bodies to find a raise.
"""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import contracts
from minireason.loop.contracts import check

GOOD = {
    "critic": {"relation": "re-deploys",
               "passage_quote": "p",
               "role_bindings": {"target": "t", "defect": "d",
                                  "grounds": "g", "bearing": "b"},
               "case": "c", "outside_vocabulary": ""},
    "defender": {"answer": "a", "concedes": False},
    "judge": {"sustained": True, "decisive_point": "d", "reading_note": "n"},
    "marker": {"mark": "differs", "difference_kind": "grounds_source",
                "left_quote": "l", "right_quote": "r", "case": "c"},
    "variator": {"paraphrases": ["one", "two"]},
}

CASES = [
    ("critic outside_vocabulary=None", "critic",
     {**GOOD["critic"], "outside_vocabulary": None}, {}),
    ("critic outside_vocabulary=0", "critic",
     {**GOOD["critic"], "outside_vocabulary": 0}, {}),
    ("critic case=None passing relation", "critic",
     {**GOOD["critic"], "case": None}, {}),
    ("critic passage_quote=None passing relation", "critic",
     {**GOOD["critic"], "passage_quote": None}, {}),
    ("marker difference_kind=0 with differs", "marker",
     {**GOOD["marker"], "difference_kind": 0}, {}),
    ("marker difference_kind=True with differs", "marker",
     {**GOOD["marker"], "difference_kind": True}, {}),
    ("marker left_quote=None with differs", "marker",
     {**GOOD["marker"], "left_quote": None}, {}),
    ("marker right_quote=0 with differs", "marker",
     {**GOOD["marker"], "right_quote": 0}, {}),
    ("marker case=None differs", "marker",
     {**GOOD["marker"], "case": None}, {}),
    ("marker mark=None", "marker", {**GOOD["marker"], "mark": None}, {}),
    ("variator paraphrases=['x', 0]", "variator",
     {"paraphrases": ["x", 0]}, {}),
    ("variator paraphrases=[None, 'x']", "variator",
     {"paraphrases": [None, "x"]}, {}),
    ("judge reading_note=None", "judge",
     {**GOOD["judge"], "reading_note": None}, {}),
    ("defender answer=None", "defender",
     {"answer": None, "concedes": True}, {}),
]

for name, role, body, kw in CASES:
    import json as _json
    dumped = _json.dumps(body)
    try:
        v = check(role, body, **kw)
        # the same body as JSON text must give the same verdict
        v2 = check(role, dumped, **kw)
        match = "same" if (v.ok, v.reason) == (v2.ok, v2.reason) else "DIVERGES-AS-TEXT"
        print(f"(returned) {name}: ok={v.ok} reason={v.reason} text-form={match}")
    except Exception as exc:
        print(f"(RAISED)   {name}: {type(exc).__name__}: {exc}")

print("done")
