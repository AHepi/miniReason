"""``assert_config_matches_standard`` - the reconciliation PREFLIGHT must call.

Deviation 8: "refuses a loop config whose ``seats`` block or ``reopen_reasons``
contradict :data:`GUARD_PARAMETERS`".  types.SeatsConfig's docstring: "The
admissible ranges below are ``standard._INT_PARAMS``' own, so the two owners can
no longer have disjoint ranges".
"""
from __future__ import annotations

import inspect

import _boot  # noqa: F401

from minireason.loop import standard as S
from minireason.loop import types as T


def run(label: str, seats, reasons=None) -> None:
    try:
        S.assert_config_matches_standard(seats, reasons)
    except S.StandardInvalid as exc:
        print("REFUSED  %-50s %s | %s" % (label, exc.code, exc.detail[:60]))
    else:
        print("ADMITTED %-50s" % label)


default = T.SeatsConfig().as_dict()
print("SeatsConfig().as_dict() =", default)
print()
print("-- every field a SeatsConfig can carry --")
run("the default config", default)
run("no seats block at all", None)
run("min_judge_families raised", dict(default, min_judge_families=3))
run("paraphrase_n lowered", dict(default, paraphrase_n=1))
run("schema_repair_budget raised", dict(default, schema_repair_budget=1))
run("three judge seats named", dict(default, judges=["a", "b", "c"]))
run("two judge seats named", dict(default, judges=["a", "b"]))
run("reopen reason outside the list", default, ["retry-until-it-sticks"])
run("reopen list narrowed to one", default, ["appellate-ruling"])
run("reopen list emptied", default, [])

print()
print("-- shapes the docstring says it accepts ('the raw config block') --")
run("a typo'd seat key", {"paraphrase_N": 9})
run("an unknown seat key", {"judge_seats": 9})
run("judges as a bare string of two characters", dict(default, judges="ab"))
run("judges as a bare string of three characters", dict(default, judges="abc"))
run("reopen_reasons as a bare string", default, "new-material")
run("seats as a list", [], None)

print()
print("-- the two owners' admissible ranges --")
src = inspect.getsource(T.SeatsConfig.from_mapping)
print("types.SeatsConfig.from_mapping bounds:")
for line in src.split("\n"):
    if "low=" in line:
        print("   ", line.strip())
print("standard._INT_PARAMS:")
for key in ("min_judge_families", "paraphrase_n", "schema_repair_budget"):
    print("    %-22s %s" % (key, S._INT_PARAMS[key]))
print("design 2.3 says: 'where the config raises it to 1 the re-ask is a new coordinate'")
print("  a config with schema_repair_budget=1 is refused by types with:")
try:
    T.SeatsConfig.from_mapping({"schema_repair_budget": 1})
except T.LoopError as exc:
    print("   ", exc.code, "|", exc.detail)
print("  and by the standard's reconciliation with:")
try:
    S.assert_config_matches_standard({"schema_repair_budget": 1}, None)
except S.StandardInvalid as exc:
    print("   ", exc.code, "|", exc.detail[:80])
print("  while build_standard admits it as a successor standard's parameter:",
      len(S.build_standard(params=dict(S.GUARD_PARAMETERS, schema_repair_budget=1))), "bytes")
