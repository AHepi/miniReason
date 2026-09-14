"""Baseline facts the interface note and docstrings claim of W0-STANDARD."""
from __future__ import annotations

import json

from _probe_setup import check

from minireason.loop import standard
from minireason.use_relation_h005 import ROOT_READING_VOCABULARY, USE_RELATION_BANNER


def main() -> None:
    check("module imports", True, standard.__name__)

    body = json.loads(standard.STANDARD_BODY)
    check("standard_body round-trips STANDARD_BODY",
          standard.standard_body(standard.STANDARD_BODY) == body)

    check("build_standard() is byte-stable",
          standard.build_standard() == standard.STANDARD_BODY,
          f"{len(standard.build_standard())} bytes")

    check("READING_VOCABULARY is the instrument's own tuple object",
          standard.READING_VOCABULARY is ROOT_READING_VOCABULARY,
          f"{list(standard.READING_VOCABULARY)}")
    check("READING_BANNER is the instrument's own banner object",
          standard.READING_BANNER is USE_RELATION_BANNER)

    n = len(standard.CEILING_REQUIRED_SENTENCES)
    check("CEILING_REQUIRED_SENTENCES holds 11 clauses", n == 11, f"got {n}")
    ceiling_paras = [p.strip() for p in standard.CEILING_TEXT.split("\n\n") if p.strip()]
    check("ceiling text has 12 paragraphs (template + 11)",
          len(ceiling_paras) == 12, f"got {len(ceiling_paras)}")
    check("every required sentence occurs verbatim in the ceiling text",
          all(sentence in standard.CEILING_TEXT
              for sentence in standard.CEILING_REQUIRED_SENTENCES))
    check("required sentences are exactly the ceiling paragraphs, in order",
          list(standard.CEILING_REQUIRED_SENTENCES) == ceiling_paras[1:])
    check("claim template is the first ceiling paragraph",
          standard.CEILING_CLAIM_TEMPLATE == ceiling_paras[0])

    # Interface note §0: CEILING_REQUIRED_SENTENCES is 11 and CEILING_EXHAUSTION_DENIAL.
    check("exhaustion denial constant",
          standard.CEILING_EXHAUSTION_DENIAL == "not exhaustion of the inquiry")

    check("FALSIFIER_MAP ids", sorted(standard.FALSIFIER_MAP) == ["D1", "F2", "F3"],
          f"{sorted(standard.FALSIFIER_MAP)}")
    check("G carries none of them",
          not any(f.carries("G") for f in standard.FALSIFIER_MAP.values()))
    check("each falsifier carries exactly T,E,D",
          all(f.carrying_registers == ("T", "E", "D") and f.excluded_registers == ("G",)
              for f in standard.FALSIFIER_MAP.values()))

    check("REGISTER_IDS", standard.REGISTER_IDS == ("T", "E", "D", "G"),
          f"{standard.REGISTER_IDS}")
    check("REGISTERS is REGISTER_IDS (one object)",
          standard.REGISTERS is standard.REGISTER_IDS)

    check("MODES", standard.MODES == ("absolute", "pairwise"), f"{standard.MODES}")
    check("rubric relation mode absolute", standard.RUBRIC_V1["relation"].mode == "absolute")
    check("rubric contrast-mark mode pairwise",
          standard.RUBRIC_V1["contrast-mark"].mode == "pairwise")
    check("body declares absolute for relation trials",
          body["rubric"]["relation"]["mode"] == "absolute")
    check("body declares pairwise for marks",
          body["rubric"]["contrast-mark"]["mode"] == "pairwise")

    print()
    print("ceiling paragraphs:")
    for i, para in enumerate(ceiling_paras):
        print(f"  [{i}] {para[:70]}...")


if __name__ == "__main__":
    main()
