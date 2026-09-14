"""BLOCKER: LoopConfig.canonical_bytes() / loop_plan_id() hash non-deterministic junk.

The docstring says 'so both give one id' and 'two loads of one config give one
identity'. But LoopConfig carries mutable field defaults and from_mapping never
normalises non-ASCII, and canonical_json emits ``ensure_ascii=False``.  A config
whose study name differs only in unicode vs NFC/NFD form produces *different*
plan ids (bytes differ), yet the docstring of loop_plan_id claims identity is a
pure function of declared values.  Also StepReceipt.build accepts arbitrary
**rest that is neither validated nor folded into step_key.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minireason.loop.types import LoopConfig, loop_plan_id, StepReceipt

GOOD = dict(
    run_id="r1", study="s", occurrences=["o1"], runner="run.py",
    cycle_budget=1, max_calls=5, reading_set=["a"], obligations_path="ob.json",
    graph_root="g", reopen_reasons=["x"],
    audit=dict(period=1, judge_err_max=0.5, streak_max=3,
               judge_err_max_account="a", streak_max_account="b"),
)

c1 = LoopConfig.from_mapping(GOOD)
c2 = LoopConfig.from_mapping(dict(GOOD, run_id="r2"))
print("same config mapping, one id?", loop_plan_id(c1, {}) == loop_plan_id(c1, {}))

# 1) NFC vs NFD study name - same declared value, different bytes
import unicodedata
nfc = unicodedata.normalize("NFC", "e\u0301")   # 'é' as composed
nfd = unicodedata.normalize("NFD", "e\u0301")   # 'é' as decomposed
c_nfc = LoopConfig.from_mapping(dict(GOOD, study="study-" + nfc))
c_nfd = LoopConfig.from_mapping(dict(GOOD, study="study-" + nfd))
print("NFC plan id:", loop_plan_id(c_nfc, {}))
print("NFD plan id:", loop_plan_id(c_nfd, {}))
print("NFC == NFD plan id?", str(c_nfc), str(c_nfd) if False else loop_plan_id(c_nfc, {}) == loop_plan_id(c_nfd, {}))

# 2) unvalidated **rest swallowed by build
r = StepReceipt.build(loop_plan_id="0"*64, index=0, kind="PREFLIGHT",
                      started_utc="2024-01-01T00:00:00Z", unvalidated="junk")
print("unvalidated rest key accepted; step_key matches key?",
      r.step_key == StepReceipt.key(r.loop_plan_id, r.kind, r.cycle, r.wave, r.inputs_sha256))
