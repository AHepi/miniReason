"""``standard_body`` as a gate, and the published mappings as objects.

``standard_body``'s docstring: "Parse a serialised standard body and refuse
anything that is not one."  This probe hands it bodies that ``build_standard``
itself refuses to emit, and then asks whether the published constants can be
edited in place by any caller that imports the module.
"""
from __future__ import annotations

import json

import _boot  # noqa: F401

from minireason.loop import standard as S

good = json.loads(S.STANDARD_BODY)


def parse(label: str, mutate) -> None:
    raw = json.loads(S.STANDARD_BODY)
    mutate(raw)
    try:
        out = S.standard_body(json.dumps(raw))
    except S.StandardInvalid as exc:
        print("REFUSED  %-52s %s" % (label, exc.code))
    else:
        print("ADMITTED %-52s (%d sections)" % (label, len(out)))


print("-- bodies build_standard would refuse, offered to standard_body --")
parse("round trip, untouched", lambda b: None)
parse("vocabulary emptied", lambda b: b["vocabulary"].update(values=[], closed=False))
parse("vocabulary values outside the six",
      lambda b: b["vocabulary"].update(values=["is-better-than", "unresolved"]))
parse("'unresolved' removed from the vocabulary",
      lambda b: b["vocabulary"].update(values=["retains"]))
parse("guard_parameters emptied", lambda b: b.update(guard_parameters={}))
parse("judge_seats = 0", lambda b: b["guard_parameters"].update(judge_seats=0))
parse("paraphrase_n = 0 (G7 switched off)",
      lambda b: b["guard_parameters"].update(paraphrase_n=0))
parse("schema_repair_budget = 99",
      lambda b: b["guard_parameters"].update(schema_repair_budget=99))
parse("reopen_reasons widened",
      lambda b: b.update(reopen_reasons=["anything-at-all"]))
parse("unanimity_rule emptied",
      lambda b: b["guard_parameters"].update(unanimity_rule=""))
parse("registers reduced to one",
      lambda b: b.update(registers={"T": b["registers"]["T"]}))
parse("a register's difference_kinds emptied",
      lambda b: b["registers"]["G"].update(difference_kinds=[]))
parse("G given a falsifier",
      lambda b: b["falsifiers"]["D1"].update(carrying_registers=["T", "E", "D", "G"]))
parse("rubric mode flipped to pairwise",
      lambda b: b["rubric"]["relation"].update(mode="pairwise"))
parse("ceiling sha256 replaced",
      lambda b: b["ceiling"].update(sha256="0" * 64))
parse("a required ceiling sentence deleted",
      lambda b: b["ceiling"].update(
          required_sentences=b["ceiling"]["required_sentences"][:3]))
parse("a scoring key nested in the body (control)",
      lambda b: b["guard_parameters"].update(rank=1))

print()
print("-- the published mappings as objects --")
before = S.STANDARD_BODY_SHA256
S.GUARD_PARAMETERS["paraphrase_n"] = 7
S.REOPEN_REASONS  # a tuple: immutable
S.DIFFERENCE_KINDS["G"] = ("grounds_source", "smuggled_kind")
S.PLAN_8A_MIRROR["marks"].append("better")
rebuilt = json.loads(S.build_standard())
print("GUARD_PARAMETERS mutated in place  ->", dict(S.GUARD_PARAMETERS)["paraphrase_n"])
print("rebuilt body guard_parameters.paraphrase_n =",
      rebuilt["guard_parameters"]["paraphrase_n"])
print("rebuilt body marks                         =", rebuilt["marks"])
print("DIFFERENCE_KINDS['G']                      =", S.DIFFERENCE_KINDS["G"])
print("STANDARD_BODY_SHA256 (frozen at import)    =", before)
print("sha256 of a fresh build                    =",
      __import__("deepreason_core.canonical", fromlist=["sha256_hex"]).sha256_hex(
          S.build_standard()))
print("build_standard() == STANDARD_BODY          =", S.build_standard() == S.STANDARD_BODY)
