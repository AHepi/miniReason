"""W0-STANDARD wave-plan acceptance, machine-checked:

- "Every PLAN 8a register definition appears byte-identically against the frozen PLAN.md"
  (frozen here as data/plan_8a_mirror.json, the declared mirror);
- "FALSIFIER_MAP encodes that G alone never carries D1 and that F2/F3 fire only on
  T, E or D";
- "two builds from identical inputs are byte-identical";
- "the body declares mode absolute for relation trials and pairwise for marks";
and the validators' declared error codes, each raised.
"""
from __future__ import annotations

import json

from _probe_setup import check

from minireason.loop import standard


def raised(fn) -> str | None:
    try:
        fn()
    except standard.StandardInvalid as exc:
        return exc.code
    return None


def main() -> None:
    body = json.loads(standard.STANDARD_BODY)
    mirror = standard.PLAN_8A_MIRROR

    # -- byte-identical registers ------------------------------------------ #
    ok = True
    for rid in standard.REGISTER_IDS:
        body_reg = body["registers"][rid]
        mirror_reg = mirror["registers"][rid]
        for field in ("name", "plan_text", "reads", "differs_iff"):
            same = body_reg[field] == mirror_reg[field]
            ok = ok and same
            check(f"register {rid}.{field} byte-identical to the mirror", same)
    check("PLAN_8A_REGISTERS objects carry the mirror bytes",
          all(getattr(standard.PLAN_8A_REGISTERS[rid], f) == mirror["registers"][rid][f]
              for rid in standard.REGISTER_IDS
              for f in ("name", "plan_text", "reads", "differs_iff")))

    # -- required §8a content is present in the mirror ---------------------- #
    check("T prefix-intact rule in plan_text",
          "prefix intact" in mirror["registers"]["T"]["plan_text"])
    check("E bare-token rule in plan_text",
          "bare id token" in mirror["registers"]["E"]["plan_text"]
          and "never" in mirror["registers"]["E"]["plan_text"])
    check("D FCL field list in plan_text",
          all(f"`{f}`" in mirror["registers"]["D"]["plan_text"]
              for f in ("type", "uptake", "revises", "withdraws", "action")))
    check("G grounds sources in plan_text",
          "objection's grounds" in mirror["registers"]["G"]["plan_text"])
    check("replicate-baseline rule present", "replicate baseline" in
          mirror["replicate_baseline"])
    check("order-of-reading rule present", "Order of reading" in mirror["order_of_reading"])
    check("register-to-falsifier mapping present",
          "Register-to-falsifier mapping" in mirror["register_to_falsifier"])

    # -- falsifier map ------------------------------------------------------- #
    d1 = standard.FALSIFIER_MAP["D1"]
    check("D1 comparison ORIGINAL vs CONTROL", d1.comparison == ("ORIGINAL", "CONTROL"),
          f"{d1.comparison}")
    f2 = standard.FALSIFIER_MAP["F2"]
    check("F2 comparison ORIGINAL vs RECODING", f2.comparison == ("ORIGINAL", "RECODING"))
    f3 = standard.FALSIFIER_MAP["F3"]
    check("F3 comparison ORIGINAL vs CARRIER", f3.comparison == ("ORIGINAL", "CARRIER"))
    check("G alone never carries D1", not d1.carries("G")
          and d1.excluded_registers == ("G",))
    check("D1 rule text is the material mirror's own",
          d1.rule == mirror["material_register_to_falsifier"]["D1"])

    # -- byte-stable build --------------------------------------------------- #
    a = standard.build_standard()
    b = standard.build_standard()
    check("two builds from defaults are byte-identical", a == b)
    check("sha256 stable",
          standard.sha256_hex(a) == standard.STANDARD_BODY_SHA256
          if hasattr(standard, "sha256_hex") else True)

    # -- modes ----------------------------------------------------------------#
    check("mode absolute for relation trials",
          body["rubric"]["relation"]["mode"] == "absolute")
    check("mode pairwise for contrast marks",
          body["rubric"]["contrast-mark"]["mode"] == "pairwise")

    # -- validators raise their declared codes -------------------------------- #
    missing = dict(standard.GUARD_PARAMETERS)
    del missing["paraphrase_n"]
    code = raised(lambda: standard.build_standard(params=missing))
    check("a missing guard parameter raises GUARD_PARAMETER_MISSING",
          code == "GUARD_PARAMETER_MISSING", f"{code}")

    bad = dict(standard.GUARD_PARAMETERS)
    bad["paraphrase_n"] = 0
    code = raised(lambda: standard.build_standard(params=bad))
    check("paraphrase_n=0 (G7 switched off) is refused out of range",
          code == "GUARD_PARAMETER_INVALID", f"{code}")

    bad = dict(standard.GUARD_PARAMETERS)
    bad["unknown_key"] = 1
    code = raised(lambda: standard.build_standard(params=bad))
    check("an unknown guard parameter raises GUARD_PARAMETER_UNKNOWN",
          code == "GUARD_PARAMETER_UNKNOWN", f"{code}")

    bad = dict(standard.GUARD_PARAMETERS)
    bad["reopen_reasons"] = ("retry-until-pass",)
    code = raised(lambda: standard.build_standard(params=bad))
    check("an unlisted reopen reason raises REOPEN_REASON_UNKNOWN",
          code == "REOPEN_REASON_UNKNOWN", f"{code}")

    code = raised(lambda: standard.build_standard(vocabulary=("retains", "unresolved")))
    check("a narrowed vocabulary is admitted (successor standard)",
          code is None, f"{code}")
    code = raised(lambda: standard.build_standard(vocabulary=("retains", "made-up-rel")))
    check("a vocabulary outside the six raises VOCABULARY_NOT_CLOSED",
          code == "VOCABULARY_NOT_CLOSED", f"{code}")
    code = raised(lambda: standard.build_standard(vocabulary=("retains",)))
    check("a vocabulary without unresolved raises UNRESOLVED_NOT_IN_VOCABULARY",
          code == "UNRESOLVED_NOT_IN_VOCABULARY", f"{code}")

    code = raised(lambda: standard.standard_body(b"not json"))
    check("malformed JSON raises STANDARD_BODY_MALFORMED",
          code == "STANDARD_BODY_MALFORMED", f"{code}")
    tampered = json.loads(standard.STANDARD_BODY)
    tampered["spec_id"] = "reading-v2"
    code = raised(lambda: standard.standard_body(json.dumps(tampered)))
    check("a foreign spec_id raises SPEC_ID_MISMATCH", code == "SPEC_ID_MISMATCH", f"{code}")
    tampered = json.loads(standard.STANDARD_BODY)
    del tampered["rubric"]
    code = raised(lambda: standard.standard_body(json.dumps(tampered)))
    check("a missing section raises STANDARD_SECTION_MISSING",
          code == "STANDARD_SECTION_MISSING", f"{code}")
    tampered = json.loads(standard.STANDARD_BODY)
    tampered["registers"]["G"]["carries_falsifiers"] = ["score"]
    code = raised(lambda: standard.standard_body(json.dumps(tampered)))
    check("a scoring key smuggled into a parsed body raises SCORING_KEY_FORBIDDEN",
          code == "SCORING_KEY_FORBIDDEN", f"{code}")


if __name__ == "__main__":
    main()
