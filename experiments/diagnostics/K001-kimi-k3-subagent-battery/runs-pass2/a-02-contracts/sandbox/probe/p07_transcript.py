"""Probe 7: the vendored registration gate versus the contracts outputs.

contracts module docstring, deviation "Program checks beyond JSON Schema":
"Three further checks are enforced the same way because the vendored
registration gate would otherwise reject the artifact later, with less to say
about why: deepreason_core.harness.conforming_transcript requires a non-empty
``case`` and ``answer`` and a non-empty ``decisive_point``, so a critic that
claims a relation must supply a case and a passage to quote, and a marker that
claims ``differs`` must supply both sides' quotes and a ``difference_kind``."

Question: do the role outputs, composed as the transcript will be composed
(transcript_blob(case, answer, decisive_point) -> conforming_transcript),
actually pass the vendored gate at every allowed boundary?
"""
import sys, os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import contracts
from deepreason_core.harness import conforming_transcript, transcript_blob

class FakeBlobs:
    def __init__(self): self.store = {}
    def put(self, data):
        if isinstance(data, bytes): data = data.decode("utf-8")
        key = "blob:%08x" % len(self.store)
        self.store[key] = data
        return key
    def get(self, ref): return self.store[ref]

def gate(case, answer, decisive_point):
    blobs = FakeBlobs()
    ref = transcript_blob(type("H", (), {"blobs": blobs})(), case=case,
                          answer=answer, decisive_point=decisive_point)
    return conforming_transcript(blobs, ref)

# 7a: a critic that validates with a named relation; defender with min answer;
#     judge with min decisive_point that IS in the exchange
critic_ok = contracts.validate("critic", {
    "relation": "retains", "passage_quote": "p",
    "role_bindings": {"target": "t", "defect": "d", "grounds": "g", "bearing": "b"},
    "case": "c", "outside_vocabulary": ""})
defender_ok = contracts.validate("defender", {"answer": "a", "concedes": False})
judge_ok = contracts.validate("judge", {"sustained": True,
                                        "decisive_point": "c", "reading_note": ""})
print(f"7a gate(case='c', answer='a', decisive='c'): {gate(critic_ok.case, defender_ok.answer, judge_ok.decisive_point)}")

# 7b: judge reading_note EMPTY is allowed by contracts; the docstring sentence
#     claims the vendored gate requires a non-empty decisive_point only — but
#     does it? decisive_point must be non-empty AND inside case+\n+answer.
judge_empty_note = contracts.validate("judge", {"sustained": True,
                                                "decisive_point": "c",
                                                "reading_note": ""})
print(f"7b judge allows empty reading_note: sustained={judge_empty_note.sustained} "
      f"note={judge_empty_note.reading_note!r}")

# 7c: whitespace-only fields pass contracts' non-emptiness checks?
critic_ws = contracts.check("critic", {
    "relation": "retains", "passage_quote": " ",
    "role_bindings": {"target": " ", "defect": " ", "grounds": " ", "bearing": " "},
    "case": " ", "outside_vocabulary": ""})
print(f"7c critic with whitespace-only case/quote: ok={critic_ws.ok}")
def_ws = contracts.check("defender", {"answer": " ", "concedes": False})
print(f"   defender with whitespace-only answer: ok={def_ws.ok}")
jd_ws = contracts.check("judge", {"sustained": True, "decisive_point": " ",
                                   "reading_note": ""})
print(f"   judge with whitespace-only decisive_point: ok={jd_ws.ok}")
if def_ws.ok:
    print(f"   -> gate(case='c', answer=' '): {gate('c', ' ', 'c')}")

# 7d: the D6-normalised critic (outside_vocabulary) never reaches a transcript
norm = contracts.check("critic", {
    "relation": "repairs", "passage_quote": "p",
    "role_bindings": {"target": "t", "defect": "d", "grounds": "g", "bearing": "b"},
    "case": "c", "outside_vocabulary": "some text"})
print(f"7d normalised critic claims_relation={norm.value.claims_relation} "
      f"(must be False: no transcript is built from it)")
print("done")
