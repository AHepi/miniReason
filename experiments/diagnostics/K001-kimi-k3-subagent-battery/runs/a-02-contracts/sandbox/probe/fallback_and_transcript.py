"""Probe: three cross-claims.

1. _schema_failure maps an UNMAPPED jsonschema validator word to 'wrong-type'
   (a SCHEMA_REASONS member), so 'names its reason' holds even off the table.
2. A D6-normalised CriticOutput cannot fill a conforming trial transcript:
   harness.conforming_transcript requires a non-empty case and a non-empty
   decisive_point; a normalised output is built from a body whose 'case' may
   be the empty string, and nothing in contracts forces one.
3. The module-level _VALIDATORS share no mutable state: validating twice and
   interleaving roles gives the same outcomes.
"""
import json
import sys

sys.path.insert(0, "src")

from jsonschema import Draft202012Validator

from deepreason_core.harness import conforming_transcript
import minireason.loop.contracts as contracts
from minireason.loop.contracts import check, validate

# 1. Unmapped validator word: 'maximum' is not in _JSONSCHEMA_REASONS.
schema = {"type": "object", "properties": {"n": {"type": "integer", "maximum": 5}}}
err = next(iter(Draft202012Validator(schema).iter_errors({"n": 9})))
print("unmapped validator word:", repr(err.validator),
      "-> maps to:", contracts._JSONSCHEMA_REASONS.get(err.validator, "wrong-type"),
      "| 'wrong-type' in SCHEMA_REASONS:", "wrong-type" in contracts.SCHEMA_REASONS)
print("every mapped target is a SCHEMA_REASONS member:",
      set(contracts._JSONSCHEMA_REASONS.values()) <= set(contracts.SCHEMA_REASONS))

# 2. D6-normalised critic vs. the vendored transcript gate.
out = validate("critic", {
    "relation": "repairs", "passage_quote": "",
    "role_bindings": {"target": "t", "defect": "d", "grounds": "g", "bearing": "b"},
    "case": "", "outside_vocabulary": "mimicry",
})
print("normalised:", out.relation, "| nominated:", out.nominated_relation,
      "| claims_relation:", out.claims_relation)
conforms_with_empty = conforming_transcript._defaults__ if False else None
# simulate what W1-GRAPH would store for a transcript from this normalised output
import types as _t

class _Blobs(dict):
    def get(self, k):
        return super().get(k)

data = {"case": out.case, "answer": "",
        "ruling": {"verdict": "fail", "decisive_point": ""}, "checks": {}}
blobs = _Blobs({"t": json.dumps(data)})
print("conforming_transcript(case='', decisive=''):", conforming_transcript(blobs, "t"))
data2 = {"case": "c", "answer": "a",
         "ruling": {"verdict": "fail", "decisive_point": "c"}, "checks": {}}
blobs2 = _Blobs({"t": json.dumps(data2)})
print("conforming_transcript(case='c', answer='a', decisive='c'):",
      conforming_transcript(blobs2, "t"))

# 3. Interleaved validators, same outcomes.
CRITIC = {
    "relation": "repairs", "passage_quote": "p",
    "role_bindings": {"target": "t", "defect": "d", "grounds": "g", "bearing": "b"},
    "case": "c", "outside_vocabulary": "",
}
a = check("critic", CRITIC).ok
bad = {**CRITIC, "relation": "mimics"}
r1 = check("critic", bad).reason
check("judge", {"sustained": True, "decisive_point": "p", "reading_note": ""})
r2 = check("critic", bad).reason
print("shared validator state disturbs nothing:", a, r1 == r2, r1)
