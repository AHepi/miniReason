"""Does loop_plan_id honour 'two loads of one config give one identity'?

Attacks:
  A) The same *declared value* written in two byte forms (NFC vs NFD study name)
     — should give one identity if identity is over declared values.
  B) StepReceipt.build(**rest) — an unvalidated arbitrary field.
"""
import sys, os, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minireason.loop.types import LoopConfig, loop_plan_id, StepReceipt

GOOD = dict(
    run_id="r1", study="s", occurrences=["o1"], runner="run.py",
    cycle_budget=1, max_calls=5, reading_set=["a"], obligations_path="ob.json",
    graph_root="g", reopen_reasons=["x"],
    audit=dict(period=1, judge_err_max=0.5, streak_max=3,
               judge_err_max_account="a", streak_max_account="b"),
)

pid = loop_plan_id(LoopConfig.from_mapping(GOOD), {})
print("A0 self-consistency:", loop_plan_id(LoopConfig.from_mapping(GOOD), {}) == pid)

composed = "study-e\u00e9"        # 'é' as ONE codepoint (NFC)
decomposed = unicodedata.normalize("NFD", composed)   # 'e' + combining accent
assert composed != decomposed and composed.encode() != decomposed.encode()

pid_nfc = loop_plan_id(LoopConfig.from_mapping(dict(GOOD, study=composed)), {})
pid_nfd = loop_plan_id(LoopConfig.from_mapping(dict(GOOD, study=decomposed)), {})
print("A1 NFC id :", pid_nfc)
print("A2 NFD id :", pid_nfd)
print("A3 equal  :", pid_nfc == pid_nfd)

# B) build() with junk rest
try:
    r = StepReceipt.build(loop_plan_id="0"*64, index=0, kind="PREFLIGHT",
                          started_utc="2024-01-01T00:00:00Z",
                          unvalidated_field="junk")
    print("B1 build swallowed unknown rest ->", type(r).__name__)
except TypeError as exc:
    print("B1 TypeError:", exc)
