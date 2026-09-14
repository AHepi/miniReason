"""What ``build_standard`` emits when a caller mints a successor standard.

``build_standard``'s docstring: "``None`` means 'the module's own frozen default'
for each argument, which is what the loop registers; a caller narrowing the
vocabulary or the guard parameters is minting a successor standard and therefore
a new ``loop_plan_id``."  So a narrowed build is a supported operation.  This
probe builds three of them and reads back the sections that describe the same
thing twice.
"""
from __future__ import annotations

import json

import _boot  # noqa: F401

from minireason.loop import standard as S

# --- 1. a narrowed vocabulary -------------------------------------------------
narrow_vocab = ("retains", "unresolved")
body = json.loads(S.build_standard(vocabulary=narrow_vocab))
print("[vocabulary] argument                 =", narrow_vocab)
print("[vocabulary] body.vocabulary.closed   =", body["vocabulary"]["closed"])
print("[vocabulary] body.vocabulary.values   =", body["vocabulary"]["values"])
print("[vocabulary] body.vocabulary.nominable=", body["vocabulary"]["nominable_relations"])
print("[vocabulary] body.rubric.relation.values =", body["rubric"]["relation"]["values"])
print("[vocabulary] rubric R7 sentence still reads:")
r7 = [line for line in body["rubric"]["relation"]["body"].split("\n") if line.startswith("R7.")]
print("            ", r7[0])
print("[vocabulary] refused? no - build_standard returned", len(S.build_standard(
    vocabulary=narrow_vocab)), "bytes")

# --- 2. narrowed reopen reasons ----------------------------------------------
params = dict(S.GUARD_PARAMETERS)
params["reopen_reasons"] = ("appellate-ruling",)
body2 = json.loads(S.build_standard(params=params))
print()
print("[reopen] params['reopen_reasons']             =", params["reopen_reasons"])
print("[reopen] body.guard_parameters.reopen_reasons =",
      body2["guard_parameters"]["reopen_reasons"])
print("[reopen] body.reopen_reasons (top level)      =", body2["reopen_reasons"])
print("[reopen] the two sections agree               =",
      body2["guard_parameters"]["reopen_reasons"] == body2["reopen_reasons"])

# --- 3. a new difference_kind token in a successor register ------------------
from dataclasses import replace  # noqa: E402

extra = S.DifferenceKind(token="target_arm", reads="x", plan_grounding="y")
regs = dict(S.PLAN_8A_REGISTERS)
regs["T"] = replace(regs["T"],
                    difference_kinds=regs["T"].difference_kinds + (extra,))
body3 = json.loads(S.build_standard(registers=regs))
print()
print("[kinds] body.registers.T.difference_kinds =",
      [k["token"] for k in body3["registers"]["T"]["difference_kinds"]])
print("[kinds] MARKER_SCHEMA enum (whose digest the body pins) =",
      S.MARKER_SCHEMA["properties"]["difference_kind"]["enum"])
print("[kinds] body.role_contracts.schemas_sha256 unchanged =",
      body3["role_contracts"]["schemas_sha256"] == S.ROLE_SCHEMAS_SHA256)

# --- 4. what PREFLIGHT reconciles a config against ---------------------------
# assert_config_matches_standard reads the module default, not the body registered.
params4 = dict(S.GUARD_PARAMETERS)
params4["judge_seats"] = 3
params4["paraphrase_n"] = 4
body4 = json.loads(S.build_standard(params=params4))
print()
print("[preflight] registered body guard_parameters:",
      {k: body4["guard_parameters"][k] for k in ("judge_seats", "paraphrase_n")})
refuse = {"judges": ["a", "b", "c"], "min_judge_families": 2, "paraphrase_n": 4,
          "schema_repair_budget": 0}
try:
    S.assert_config_matches_standard(refuse, None)
    print("[preflight] a config matching the registered body reconciles")
except S.StandardInvalid as exc:
    print("[preflight] a config matching the registered body is REFUSED:")
    print("            code=%s detail=%s" % (exc.code, exc.detail))
admit = {"judges": ["a", "b"], "min_judge_families": 2, "paraphrase_n": 2,
         "schema_repair_budget": 0}
try:
    S.assert_config_matches_standard(admit, None)
    print("[preflight] a config contradicting the registered body (paraphrase_n=2,")
    print("            judges=2) is ADMITTED: no exception")
except S.StandardInvalid as exc:
    print("[preflight] refused:", exc.code, exc.detail)
