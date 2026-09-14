"""The interface promise: 'the mapping is validated the same way, so a file and
 the object read from it give one id.'

  V1  loop_plan_id(LoopConfig) == loop_plan_id(equivalent raw mapping)?
      The object resolves defaults; the raw mapping omits them. as_dict() fills
      every key, so they should agree.  Test.
  V2  from_mapping returns the SAME object when given a LoopConfig (no copy).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minireason.loop.types import LoopConfig, loop_plan_id

RAW = dict(
    run_id="r1", study="s", occurrences=["o1"], runner="run.py",
    cycle_budget=1, max_calls=5, reading_set=["a"], obligations_path="ob.json",
    graph_root="g", reopen_reasons=["x"],
    audit=dict(period=1, judge_err_max=0.5, streak_max=3,
               judge_err_max_account="a", streak_max_account="b"),
)
obj = LoopConfig.from_mapping(RAW)
pins = {"tools/x.py": "b"*64}
a = loop_plan_id(obj, pins)
b = loop_plan_id(RAW, pins)
print("V1 object id == mapping id:", a == b)
print("   ", a)
print("   ", b)
c = LoopConfig.from_mapping(obj)
print("V2 from_mapping(LoopConfig) is same object:", c is obj)

# canonical_bytes stable across two loads
print("V3 canonical_bytes stable:",
      LoopConfig.from_mapping(RAW).canonical_bytes()
      == LoopConfig.from_mapping(dict(RAW)).canonical_bytes())
