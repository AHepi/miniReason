"""Probe 11: round-trips, word-limit-on-non-string, and reason granularity.

 * _word_limit_failure silently skips a non-str value — but schema gate must
   already have refused it; confirm the order assumption is the only way in.
 * MarkerOutput.case never carries a limit? No — WORD_LIMITS has marker/case.
 * as_dict round-trips: CriticOutput.as_dict re-validates as critic?
 * 'case-required' before 'passage-quote-required' when both missing (fixed
   order, deterministic).
"""
import sys, os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import contracts
from minireason.loop.contracts import check, validate, WORD_LIMITS

# non-str in a word-limited field: schema gate refuses first
v = check("judge", {"sustained": True, "decisive_point": "d", "reading_note": 0})
print(f"judge reading_note=0: ok={v.ok} reason={v.reason}")
v = check("critic", {"relation": "retains", "passage_quote": "p",
                     "role_bindings": {"target": "t", "defect": "d",
                                       "grounds": "g", "bearing": "b"},
                     "case": 0, "outside_vocabulary": ""})
print(f"critic case=0: ok={v.ok} reason={v.reason}")

# both case and quote empty on a nominee: which reason first, deterministically
body = {"relation": "retains", "passage_quote": "",
        "role_bindings": {"target": "t", "defect": "d", "grounds": "g", "bearing": "b"},
        "case": "", "outside_vocabulary": ""}
results = {(check("critic", body).reason, check("critic", body).path) for _ in range(3)}
print(f"both empty, 3 runs: {results}")

# marker case limit applies
v = check("marker", {"mark": "same", "difference_kind": None, "left_quote": "",
                     "right_quote": "", "case": "w " * 121})
print(f"marker case 121 words: ok={v.ok} reason={v.reason}")

# CriticOutput.as_dict re-validates (round-trip) for a nominal and a 'none' row
nominal = validate("critic", {"relation": "re-deploys", "passage_quote": "p",
                              "role_bindings": {"target": "t", "defect": "d",
                                                "grounds": "g", "bearing": "b"},
                              "case": "c", "outside_vocabulary": ""})
none_row = validate("critic", {"relation": "none", "passage_quote": "",
                               "role_bindings": {"target": "", "defect": "",
                                                 "grounds": "", "bearing": ""},
                               "case": "", "outside_vocabulary": ""})
ov_row = validate("critic", {"relation": "repairs", "passage_quote": "p",
                             "role_bindings": {"target": "t", "defect": "d",
                                               "grounds": "g", "bearing": "b"},
                             "case": "c", "outside_vocabulary": "x"})
for name, out in (("nominal", nominal), ("none_row", none_row), ("ov_row", ov_row)):
    re_v = check("critic", json.dumps(out.as_dict()))
    print(f"round-trip {name}: re-checks ok={re_v.ok} reason={re_v.reason} "
          f"relation={out.as_dict()['relation']!r}")

# nominated_relation is NOT emitted by as_dict (record drops it)
print(f"ov_row as_dict keys: {sorted(ov_row.as_dict())}  "
      f"(nominated_relation attribute: {ov_row.nominated_relation!r})")

# MarkerOutput.as_dict round-trip
mk = validate("marker", {"mark": "differs", "difference_kind": "grounds_source",
                         "left_quote": "l", "right_quote": "r", "case": "c"})
re_v = check("marker", json.dumps(mk.as_dict()))
print(f"marker round-trip: ok={re_v.ok}")
print("done")
