"""Attacks on W0-TYPES that did not succeed. Recorded because a failed attack
is evidence about the module."""
import json

from _fixture import H1, H2, config, show  # noqa: E402

from minireason.loop import types  # noqa: E402

cfg = config()
plan = types.loop_plan_id(cfg, {"src/a.py": H1})
UTC = "2026-09-14T00:00:00Z"

print("--- A. escape the loops root through run_id")
for run_id in ("../../etc", "..", ".", "a/b", "a\\b", "", "~root", "-x",
               "a" * 65, "․․/x", "a\n", "a%2f..%2fb"):
    show(f"  run_paths(root, {run_id!r})", lambda r=run_id: types.run_paths("/repo", r).run_root.as_posix())

print()
print("--- B. escape readings/ through a row key")
paths = types.run_paths("/repo", "loop-001")
for key in ("problem/arm/cycle-1/node#r3", "../../../etc/passwd", "..", "...",
            "./.", "a" * 300, "NUL"):
    try:
        out = paths.reading_dir(key)
        inside = str(out).startswith("/repo/experiments/loops/loop-001/readings/")
        print(f"  {key[:24]!r:30} -> {out.name!r} inside readings/: {inside}")
    except types.LoopError as exc:
        print(f"  {key[:24]!r:30} -> {exc.code}")
print("  two keys that fold alike get two directories:",
      paths.reading_dir("a/b").name, paths.reading_dir("a#b").name)

print()
print("--- C. a boolean as a budget or a count")
for key in ("cycle_budget", "max_calls", "max_per_key"):
    show(f"  {key}=True", types.LoopConfig.from_mapping, dict(cfg, **{key: True}))
show("  audit.period=True", types.AuditConfig.from_mapping, dict(cfg["audit"], period=True))
show("  audit.judge_err_max=True", types.AuditConfig.from_mapping,
     dict(cfg["audit"], judge_err_max=True))
show("  RunPaths.cycle(True)", paths.cycle, True)
show("  step index=True", types.StepReceipt.build, loop_plan_id=plan, index=True,
     kind="PREFLIGHT", started_utc=UTC)

print()
print("--- D. turn a pre-registered guard parameter off from the config")
show("  seats.paraphrase_n=0", types.SeatsConfig.from_mapping, {"paraphrase_n": 0})
show("  seats.schema_repair_budget=1", types.SeatsConfig.from_mapping,
     {"schema_repair_budget": 1})
show("  seats.min_judge_families=1", types.SeatsConfig.from_mapping,
     {"min_judge_families": 1})
show("  one judge seat, two families", types.SeatsConfig.from_mapping,
     {"judges": ["a"], "min_judge_families": 2})
show("  duplicate judge seats", types.SeatsConfig.from_mapping, {"judges": ["a", "a"]})

print()
print("--- E. make a receipt lie about spending, kind, status or its own key")
show("  SEND declared spending=False", types.StepReceipt.build, loop_plan_id=plan,
     index=1, kind="SEND", started_utc=UTC, spending=False)
show("  IMPORT declared spending=True", types.StepReceipt.build, loop_plan_id=plan,
     index=1, kind="IMPORT", started_utc=UTC, spending=True)
show("  COMPLETE with a failure_code", types.StepReceipt.build, loop_plan_id=plan,
     index=1, kind="IMPORT", started_utc=UTC, failure_code="STEP_TIMEOUT")
show("  HALTED with no failure_code", types.StepReceipt.build, loop_plan_id=plan,
     index=1, kind="IMPORT", started_utc=UTC, status="HALTED")
good = types.StepReceipt.build(loop_plan_id=plan, index=2, kind="SEND",
                               started_utc=UTC, cycle=1, wave="w1",
                               inputs_sha256={"in/a.json": H1})
for field, value in (("step_key", "0" * 64), ("kind", "READ"), ("cycle", 2),
                     ("wave", "w2"), ("inputs_sha256", {"in/a.json": H2}),
                     ("loop_plan_id", "0" * 64)):
    show(f"  tamper {field}", types.StepReceipt.from_dict,
         dict(good.as_dict(), **{field: value}))

print()
print("--- F. the receipt round-trips and the envelope is not reorderable")
back = types.StepReceipt.from_dict(good.as_dict())
print("  from_dict(as_dict(r)) == r:", back == good)
print("  as_dict is byte-stable   :", json.dumps(back.as_dict(), sort_keys=True)
      == json.dumps(good.as_dict(), sort_keys=True))
print("  cycle=1/wave=None differs from cycle=None/wave='1':",
      types.StepReceipt.key(plan, "SEND", 1, None, {})
      != types.StepReceipt.key(plan, "SEND", None, "1", {}))
print("  a pin named 'config' cannot shadow the config block:",
      types.loop_plan_id(cfg, {"config": H1}) != types.loop_plan_id(cfg, {"pins": H1}))

print()
print("--- G. smuggle a trailing newline or upper case past the shape checks")
show("  LoopError code 'ABC\\n'", types.LoopError, "ABC\n")
show("  LoopError code 'abc'", types.LoopError, "abc")
show("  pin digest upper case", types.loop_plan_id, cfg, {"a.py": H1.upper()})
show("  pin digest 63 chars", types.loop_plan_id, cfg, {"a.py": H1[:63]})
show("  pin digest with newline", types.loop_plan_id, cfg, {"a.py": H1 + "\n"})
show("  started_utc naive", types.StepReceipt.build, loop_plan_id=plan, index=1,
     kind="IMPORT", started_utc="2026-09-14T00:00:00")
show("  started_utc +01:00", types.StepReceipt.build, loop_plan_id=plan, index=1,
     kind="IMPORT", started_utc="2026-09-14T00:00:00+01:00")

print()
print("--- H. publish_ref and provider_mode")
for ref in ("origin/claude/x", "origin/../x", "/origin/x", "origin", "origin/x/../y",
            "origin/claude/a-b.c_d"):
    show(f"  publish_ref={ref!r}", lambda r=ref: types.LoopConfig.from_mapping(
        dict(cfg, publish_ref=r)).publish_ref)
show("  provider_mode='LIVE'", types.LoopConfig.from_mapping, dict(cfg, provider_mode="LIVE"))
print("  provider_mode default:", types.LoopConfig.from_mapping(cfg).provider_mode)

print()
print("--- I. non-ASCII config values survive a JSON round trip with one identity")
uni = dict(cfg, study="étude — C001")
once = types.loop_plan_id(uni, {"a.py": H1})
twice = types.loop_plan_id(json.loads(json.dumps(uni)), {"a.py": H1})
thrice = types.loop_plan_id(json.loads(json.dumps(uni, ensure_ascii=True)), {"a.py": H1})
print("  id stable across ensure_ascii True/False:", once == twice == thrice)

print()
print("--- J. canonical_json agrees with the transport's own digest")
from deepreason_core.canonical import canonical_json, sha256_hex  # noqa: E402
from minireason import provider_openai_compat as poc  # noqa: E402
sample = {"b": [1, 2, {"z": None}], "a": "é", "n": 1.5, "t": True}
print("  sha256_hex(canonical_json(v)) == poc.digest(v):",
      sha256_hex(canonical_json(sample)) == poc.digest(sample))
print("  poc._MIN_SECRET_LENGTH =", poc._MIN_SECRET_LENGTH)
