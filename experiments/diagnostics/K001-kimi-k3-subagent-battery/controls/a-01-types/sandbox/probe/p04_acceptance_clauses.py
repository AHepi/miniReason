"""The W0-TYPES acceptance clauses of design-s7-wave-plan.md, executed.

"Two loads of one config give the same plan_id; a changed pin changes it; an
unknown config key is refused; the token 'exhaustion' appears in no vocabulary;
every block code used anywhere in the package is a member of BLOCK_CODES."
"""
import dataclasses
import json
import os
import tempfile

from _fixture import H1, H2, ROOT, config  # noqa: E402

from minireason.loop import types  # noqa: E402

cfg = config()

print("--- clause 1: two loads of one config give the same plan_id")
with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "config.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(cfg, handle, indent=2)
    one = types.LoopConfig.load(path)
    two = types.LoopConfig.load(path)
    pins = {"src/minireason/use_relation_h005.py": H1}
    print("load/load identical id:", types.loop_plan_id(one, pins) == types.loop_plan_id(two, pins))
    print("mapping == object      :", types.loop_plan_id(cfg, pins) == types.loop_plan_id(one, pins))
    reordered = dict(reversed(list(cfg.items())))
    print("config key order       :", types.loop_plan_id(reordered, pins) == types.loop_plan_id(cfg, pins))
    explicit = one.as_dict()
    print("defaults resolved      :", types.loop_plan_id(explicit, pins) == types.loop_plan_id(cfg, pins))

print()
print("--- clause 2: a changed pin changes it (single-spelling pin maps)")
print("H1 vs H2:", types.loop_plan_id(cfg, {"a.py": H1}) != types.loop_plan_id(cfg, {"a.py": H2}))
print("added pin:", types.loop_plan_id(cfg, {"a.py": H1}) != types.loop_plan_id(cfg, {"a.py": H1, "b.py": H2}))
print("pin order (distinct keys):",
      types.loop_plan_id(cfg, {"a.py": H1, "b.py": H2})
      == types.loop_plan_id(cfg, {"b.py": H2, "a.py": H1}))

print()
print("--- clause 3: an unknown config key is refused")
for where, raw in (("top level", dict(cfg, nope=1)),
                   ("seats", dict(cfg, seats={"nope": 1})),
                   ("audit", dict(cfg, audit=dict(cfg["audit"], nope=1))),
                   ("timeouts", dict(cfg, timeouts={"nope": 1})),
                   ("contrast", dict(cfg, contrast={"nope": 1}))):
    try:
        types.LoopConfig.from_mapping(raw)
        print(f"  {where}: ACCEPTED")
    except types.LoopError as exc:
        print(f"  {where}: {exc.code}: {exc.detail}")

print()
print("--- clause 4: the token 'exhaustion' appears in no vocabulary")
tables = {
    "STOP_REASONS": types.STOP_REASONS,
    "BLOCK_CODES": types.BLOCK_CODES,
    "CEILING_BLOCK_REASONS": types.CEILING_BLOCK_REASONS,
    "FAILURE_CODES": types.FAILURE_CODES,
    "STEP_KINDS": types.STEP_KINDS,
    "STEP_STATUSES": types.STEP_STATUSES,
    "PROVIDER_MODES": types.PROVIDER_MODES,
    "REPLAYABLE_STEPS": types.REPLAYABLE_STEPS,
    "SPENDING_STEPS": types.SPENDING_STEPS,
}
for name, table in tables.items():
    hits = sorted(t for t in table if "exhaust" in t.lower())
    print(f"  {name}: {len(table)} members, 'exhaust' hits: {hits}")

print()
print("--- clause 5: BLOCK_CODES vs the frozen ceiling's own list")
ceiling = open(os.path.join(ROOT, "src/minireason/loop/data/ceiling_v1.md"),
               encoding="utf-8").read()
clause = [line for line in ceiling.splitlines() if "block register by reason code" in line][0]
import re  # noqa: E402
printed = re.findall(r"`([a-z-]+)`", clause)
print("ceiling order :", printed)
print("CEILING_BLOCK_REASONS:", list(types.CEILING_BLOCK_REASONS))
print("same list, same order:", printed == list(types.CEILING_BLOCK_REASONS))
derived = {types.BLOCK_CODE_PREFIX + r for r in types.CEILING_BLOCK_REASONS}
print("BLOCK_CODES == ceiling nine + blocked:constitution:",
      types.BLOCK_CODES == derived | {"blocked:constitution"})
print("block_code round trip:", [types.block_code(r) for r in types.CEILING_BLOCK_REASONS][:3], "...")
try:
    types.block_code("made-up")
except types.LoopError as exc:
    print("block_code('made-up'):", exc.code)

print()
print("--- every declared config value reaches as_dict (and so the plan id)")
for klass in (types.LoopConfig, types.SeatsConfig, types.ContrastConfig,
              types.AuditConfig, types.TimeoutsConfig):
    names = {f.name for f in dataclasses.fields(klass)}
    if klass is types.LoopConfig:
        emitted = set(types.LoopConfig.from_mapping(cfg).as_dict()) - {"schema"}
    elif klass is types.AuditConfig:
        emitted = set(types.AuditConfig.from_mapping(cfg["audit"]).as_dict())
    else:
        emitted = set(klass.from_mapping({}).as_dict())
    print(f"  {klass.__name__}: fields-not-emitted = {sorted(names - emitted)}")

print()
print("--- REPLAYABLE_STEPS / SPENDING_STEPS are disjoint subsets of STEP_KINDS")
print("disjoint:", not (types.REPLAYABLE_STEPS & types.SPENDING_STEPS))
print("subsets :", (types.REPLAYABLE_STEPS | types.SPENDING_STEPS) <= set(types.STEP_KINDS))
print("neither :", sorted(set(types.STEP_KINDS) - types.REPLAYABLE_STEPS - types.SPENDING_STEPS))
