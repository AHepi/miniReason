"""Follow-ups.

1. p07 section G tested "upper case" with a digest of all digits, which has no
   case. Redone here with a letter-bearing digest.
2. How much of a step receipt does its own step_key actually bind?
3. Which UPPER_SNAKE codes does types.py itself raise, and are they declared?
"""
import ast
import os
import re

from _fixture import H1, ROOT, config, show  # noqa: E402

from minireason.loop import types  # noqa: E402

cfg = config()
plan = types.loop_plan_id(cfg, {"src/a.py": H1})
UTC = "2026-09-14T00:00:00Z"
HEX_A = "a" * 64

print("--- 1. upper case, redone with a letter-bearing digest")
show("  pins {'a.py': 'a'*64}", types.loop_plan_id, cfg, {"a.py": HEX_A})
show("  pins {'a.py': 'A'*64}", types.loop_plan_id, cfg, {"a.py": HEX_A.upper()})
show("  pins {'a.py': 'a'*63 + 'g'}", types.loop_plan_id, cfg, {"a.py": "a" * 63 + "g"})

print()
print("--- 2. what the receipt's self-check binds, field by field")
good = types.StepReceipt.build(loop_plan_id=plan, index=2, kind="SEND",
                               started_utc=UTC, cycle=1, wave="w1",
                               inputs_sha256={"in/a.json": H1},
                               outputs_sha256={"out/a.json": H1},
                               finished_utc="2026-09-14T00:01:00Z",
                               published_commit="abc1234")
base = good.as_dict()
edits = {
    "index": 7,
    "status": "FAILED",
    "outputs_sha256": {"out/a.json": "b" * 64},
    "finished_utc": "2030-01-01T00:00:00Z",
    "published_commit": "deadbee",
    "custody": {"verified": True, "checks": []},
    "spending": True,
}
for field, value in edits.items():
    raw = dict(base, **{field: value})
    if field == "status":
        raw["failure_code"] = "STEP_TIMEOUT"
    try:
        edited = types.StepReceipt.from_dict(raw)
        print(f"  edit {field:17} -> ACCEPTED, step_key unchanged: "
              f"{edited.step_key == good.step_key}")
    except types.LoopError as exc:
        print(f"  edit {field:17} -> {exc.code}")
print("  fields in as_dict():", len(base))

print()
print("--- 3. codes raised inside types.py, against FAILURE_CODES")
source = open(os.path.join(ROOT, "src/minireason/loop/types.py"), encoding="utf-8").read()
tree = ast.parse(source)
raised = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("_fail", "LoopError"):
        if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
            raised.add(node.args[0].value)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("_identifier", "_relative", "_digests"):
        for arg in node.args[2:]:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                raised.add(arg.value)
        for kw in node.keywords:
            if kw.arg == "code" and isinstance(kw.value, ast.Constant):
                raised.add(kw.value.value)
print("  literal codes reachable from a raise in types.py:", len(raised))
for code in sorted(raised):
    print(f"    {code:26} in FAILURE_CODES: {code in types.FAILURE_CODES}")
print("  interface's list for types.py, not reachable from a literal here:")
interface = {"CONFIG_NOT_A_MAPPING", "CONFIG_SCHEMA_UNKNOWN", "CONFIG_UNKNOWN_KEY",
             "CONFIG_MISSING_KEY", "CONFIG_INVALID_VALUE", "PIN_INVALID",
             "RUN_ID_INVALID", "CYCLE_OUT_OF_RANGE", "STEP_RECEIPT_INVALID",
             "STEP_KEY_MISMATCH", "BLOCK_CODE_UNKNOWN"}
print("   ", sorted(interface - raised), "| extra here:", sorted(raised - interface))
print("  len(FAILURE_CODES) =", len(types.FAILURE_CODES))

print()
print("--- 4. a few _relative spellings that are accepted")
for text in (".", "a ", "C:/x", "a/b/", "a.py\t", "\u2024\u2024/x"):
    show(f"  _relative({text!r})", types._relative, text, "where")
