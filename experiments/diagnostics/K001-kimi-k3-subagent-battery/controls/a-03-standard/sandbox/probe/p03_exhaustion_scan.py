"""Attacks on ``assert_no_exhaustion_claim`` and on its one exemption."""
from __future__ import annotations

import textwrap

import _boot  # noqa: F401

from minireason.loop import standard as S


def run(label: str, text: str) -> None:
    try:
        S.assert_no_exhaustion_claim(text, where="record")
    except S.StandardInvalid as exc:
        print("REFUSED  %-46s %s | %s" % (label, exc.code, exc.detail[:70]))
    else:
        print("ADMITTED %-46s" % label)


print("-- the frozen artifacts --")
run("CEILING_TEXT as shipped", S.CEILING_TEXT)
run("STANDARD_BODY as shipped", S.STANDARD_BODY.decode("utf-8"))
run("every required sentence joined", "\n\n".join(S.CEILING_REQUIRED_SENTENCES))

print()
print("-- plain claims a stop record must not make --")
run("'the inquiry is exhausted'", "The run stopped: the inquiry is exhausted.")
run("'exhaustive search'", "An exhaustive search of the material.")
run("upper case", "THE INQUIRY WAS EXHAUSTED.")
run("denial with the stem emphasised (inline bold)",
    "A reached ceiling is a declared resource boundary, not **exhaustion of the "
    "inquiry**, and this record states which was reached.")

print()
print("-- the smuggle the docstring names: a claim built around the exemption --")
denial = S.CEILING_EXHAUSTION_DENIAL
run("halves joined by the removal", "exh" + denial + "austion")
run("halves with spaces around the exemption", "exh " + denial + " austion")
run("the denial repeated three times", " ".join([denial] * 3))
run("denial plus a real claim elsewhere",
    "A reached ceiling is a declared resource boundary, %s. The budget is "
    "exhausted." % denial)

print()
print("-- the denial as the design of record renders it (deviation 4: blockquote) --")
clause = next(c for c in S.CEILING_REQUIRED_SENTENCES
              if S.CEILING_EXHAUSTION_DENIAL in c)
print("the ceiling clause carrying the denial =")
print("   ", clause)
for width in (40, 50, 60, 70, 80):
    quoted = "\n".join("> " + line for line in textwrap.wrap(clause, width))
    label = "blockquote, wrapped at %d columns" % width
    run(label, quoted)
print()
print("the 60-column blockquote, verbatim:")
print(textwrap.indent("\n".join("> " + l for l in textwrap.wrap(clause, 60)), "    "))

print()
print("-- list-item and table renderings of the same clause --")
run("bullet item, wrapped at 60", "\n".join(
    ("- " if i == 0 else "  ") + line
    for i, line in enumerate(textwrap.wrap(clause, 60))))
run("one table cell", "| clause |\n|---|\n| %s |" % clause)
