"""Smaller observations: the pin list, direct construction, hashability."""
import dataclasses
import os

from _fixture import H1, ROOT, config, show  # noqa: E402

from minireason.loop import types  # noqa: E402

cfg = config()

print("--- PINNED_SOURCE_PATHS is exported but loop_plan_id never requires it")
print("PINNED_SOURCE_PATHS =", types.PINNED_SOURCE_PATHS)
print("loop_plan_id(cfg, {}) ->", types.loop_plan_id(cfg, {}))
print("loop_plan_id(cfg, {'unrelated.txt': H1}) ->",
      types.loop_plan_id(cfg, {"unrelated.txt": H1}))
print("present in this snapshot:")
for path in types.PINNED_SOURCE_PATHS:
    print(f"  {path:56} exists={os.path.exists(os.path.join(ROOT, path))}")

print()
print("--- LoopConfig is a public dataclass with no __post_init__")
print("LoopConfig has __post_init__:", hasattr(types.LoopConfig, "__post_init__"))
print("StepReceipt has __post_init__:", hasattr(types.StepReceipt, "__post_init__"))
hand = types.LoopConfig(
    run_id="../../etc", study="", occurrences=("/abs/path",), runner="..\\x",
    cycle_budget=-1, max_calls=-1, reading_set=(), obligations_path="../o.json",
    graph_root="/", reopen_reasons=(), audit=types.AuditConfig.from_mapping(cfg["audit"]))
print("hand-built config accepted by the constructor; its run_id is", repr(hand.run_id))
print("loop_plan_id(hand-built, {}) ->", types.loop_plan_id(hand, {}))
show("LoopConfig.from_mapping(hand.as_dict())", types.LoopConfig.from_mapping, hand.as_dict())

print()
print("--- frozen dataclasses that are not hashable")
UTC = "2026-09-14T00:00:00Z"
plan = types.loop_plan_id(cfg, {"src/a.py": H1})
receipt = types.StepReceipt.build(loop_plan_id=plan, index=0, kind="PREFLIGHT",
                                  started_utc=UTC)
for label, value in (("TimeoutsConfig()", types.TimeoutsConfig()),
                     ("LoopConfig (loaded)", types.LoopConfig.from_mapping(cfg)),
                     ("StepReceipt", receipt),
                     ("CustodyReport()", types.CustodyReport()),
                     ("RunPaths", types.run_paths("/repo", "loop-001"))):
    print(f"  frozen={value.__class__.__dataclass_params__.frozen}", end="  ")
    show(f"hash({label})", hash, value)

print()
print("--- LoopConfig.load on a missing file is not a LoopError")
show("LoopConfig.load('no-such-file.json')", types.LoopConfig.load,
     os.path.join(ROOT, "no-such-file.json"))
show("LoopConfig.load(<a directory>)", types.LoopConfig.load, ROOT)

print()
print("--- StepReceipt.build passes **rest straight to the constructor")
show("build(..., nonsense=1)", types.StepReceipt.build,
     loop_plan_id=plan, index=0, kind="PREFLIGHT", started_utc=UTC, nonsense=1)
show("build(..., step_key='x')", types.StepReceipt.build,
     loop_plan_id=plan, index=0, kind="PREFLIGHT", started_utc=UTC, step_key="x")
print("from_dict, by contrast:")
show("from_dict({... 'nonsense': 1})", types.StepReceipt.from_dict,
     dict(receipt.as_dict(), nonsense=1))
