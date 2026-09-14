"""publish_ref early-refusal and misc shapes.

  P1 'origin/main' accepted; 'origin/../x', 'origin/x..y', '/abs/ref',
     no-slash 'main', double slash 'a//b', trailing content.
  P2 the interface says _PUBLISH_REF mirrors split_publish_ref "origin/x" ->
     ("origin","refs/heads/x"); here we only check the loop-local gate.
  M1 StepReceipt with cycle=0 refused; cycle=100 refused; wave with bad char.
  M2 status FAILED without failure_code refused; COMPLETE with failure_code refused.
  M3 step receipt 'custody' given as a dict -> coerced (from_dict path) and as a
      foreign object -> refused?
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minireason.loop.types import (LoopConfig, StepReceipt, LoopError)

GOOD = dict(
    run_id="r1", study="s", occurrences=["o1"], runner="run.py",
    cycle_budget=1, max_calls=5, reading_set=["a"], obligations_path="ob.json",
    graph_root="g", reopen_reasons=["x"],
    audit=dict(period=1, judge_err_max=0.5, streak_max=3,
               judge_err_max_account="a", streak_max_account="b"),
)
for ref in ("origin/main", "origin/claude/proj-x", "origin/../x",
            "origin/x..y", "main", "a//b", "origin/", "/o/x"):
    try:
        LoopConfig.from_mapping(dict(GOOD, publish_ref=ref))
        print("P1", repr(ref), "ACCEPTED")
    except LoopError as exc:
        print("P1", repr(ref), "->", exc.code)

lpid = "0"*64
def rc(label, **kw):
    try:
        StepReceipt.build(loop_plan_id=lpid, index=0, kind="SEND",
                          started_utc="2024-01-01T00:00:00Z", **kw)
        print(label, "ACCEPTED")
    except LoopError as exc:
        print(label, "->", exc.code)

rc("M1 cycle=0", cycle=0)
rc("M1 cycle=100", cycle=100)
rc("M1 cycle=1", cycle=1)
rc("M1 wave='with space'", wave="with space")
rc("M1 wave='w-1'", wave="w-1")
rc("M2 FAILED no code", status="FAILED")
rc("M2 COMPLETE w/ code", failure_code="STEP_TIMEOUT")
rc("M2 HALTED w/ code", status="HALTED", failure_code="UNRESOLVED_STEP")

# M3 custody coercion
r = StepReceipt.build(loop_plan_id=lpid, index=0, kind="SEND",
                      started_utc="2024-01-01T00:00:00Z",
                      custody={"verified": True, "checks": ["A"]})
print("M3 dict custody coerced:", r.custody.verified, r.custody.checks)
class Foreign:  # carries verified/checks attrs but is not a CustodyReport/Mapping
    verified = True
    checks = ()
try:
    r = StepReceipt.build(loop_plan_id=lpid, index=0, kind="SEND",
                          started_utc="2024-01-01T00:00:00Z", custody=Foreign())
    print("M3 foreign custody coerced?:", r.custody)
except LoopError as exc:
    print("M3 foreign custody refused:", exc.code)
