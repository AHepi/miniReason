"""Determinism of the identity functions.

  D1  canonical_bytes of one config is byte-stable across constructions.
  D2  StepReceipt.key is a pure function of its arguments (repeat calls).
  D3  loop_plan_id is a pure function of (config, pins).
  D4  reading_dir is a pure function of row_key.
  D5  step_key CHANGES when any one of (kind, cycle, wave, inputs) changes -
      including 'wave' None->'w1', and a changed input digest; and NOT when
      'index' changes (documents the coordinate-only seam).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minireason.loop.types import (LoopConfig, loop_plan_id, StepReceipt,
                                    run_paths)

GOOD = dict(
    run_id="r1", study="s", occurrences=["o1"], runner="run.py",
    cycle_budget=1, max_calls=5, reading_set=["a"], obligations_path="ob.json",
    graph_root="g", reopen_reasons=["x"],
    audit=dict(period=1, judge_err_max=0.5, streak_max=3,
               judge_err_max_account="a", streak_max_account="b"),
)
cfg = LoopConfig.from_mapping(GOOD)
print("D1 bytes stable:", cfg.canonical_bytes() == LoopConfig.from_mapping(dict(GOOD)).canonical_bytes())

k = StepReceipt.key
base = k("0"*64, "SEND", 1, "w1", {"a/x": "c"*64})
print("D2 key pure:", base == k("0"*64, "SEND", 1, "w1", {"a/x": "c"*64}))
print("D3 id pure:", loop_plan_id(cfg, {}) == loop_plan_id(cfg, {}))
rp = run_paths("/repo", "r1")
print("D4 reading_dir pure:", rp.reading_dir("p/a/cycle-1/n#r3") == rp.reading_dir("p/a/cycle-1/n#r3"))

print("D5a kind changes key:", base != k("0"*64, "READ", 1, "w1", {"a/x": "c"*64}))
print("D5b cycle changes key:", base != k("0"*64, "SEND", 2, "w1", {"a/x": "c"*64}))
print("D5c wave changes key:", base != k("0"*64, "SEND", 1, "w2", {"a/x": "c"*64}))
print("D5d wave None vs w1 :", k("0"*64, "SEND", 1, None, {"a/x": "c"*64}) != base)
print("D5e input changes key:", base != k("0"*64, "SEND", 1, "w1", {"a/x": "d"*64}))
print("D5f plan changes key :", base != k("1"*64, "SEND", 1, "w1", {"a/x": "c"*64}))
r0 = StepReceipt.build(loop_plan_id="0"*64, index=0, kind="SEND", cycle=1, wave="w1",
                       inputs_sha256={"a/x": "c"*64}, started_utc="2024-01-01T00:00:00Z")
r9 = StepReceipt.build(loop_plan_id="0"*64, index=9, kind="SEND", cycle=1, wave="w1",
                       inputs_sha256={"a/x": "c"*64}, started_utc="2024-01-01T00:00:00Z")
print("D5g index change, key same:", r0.step_key == r9.step_key,
      "| filenames:", r0.filename, r9.filename)
