"""Attacks on ``assert_no_scoring_headers`` - G12 over a rendered file."""
from __future__ import annotations

import _boot  # noqa: F401

from minireason.loop import standard as S


def run(label: str, text: str) -> None:
    try:
        S.assert_no_scoring_headers(text, where="READING_TABLE.md")
    except S.StandardInvalid as exc:
        print("REFUSED  %-44s %s | %s" % (label, exc.code, exc.detail[:66]))
    else:
        print("ADMITTED %-44s" % label)


print("-- what it must refuse --")
run("ATX heading", "# Scores by seat\n")
run("table header row", "| cell | score |\n|---|---|\n| a | 1 |\n")
run("backticked header cell", "| cell | `rank` |\n|---|---|\n")
run("hyphenated header cell", "| cell | win-rate |\n|---|---|\n")
run("heading with closing hashes", "## Merit ##\n")

print()
print("-- what it must admit --")
run("CEILING_TEXT as shipped", S.CEILING_TEXT)
run("a body row saying the word", "| cell | note |\n|---|---|\n| a | it scores nothing |\n")
run("a heading with a longer word", "# Scoreboard-free rendering\n")

print()
print("-- bypasses --")
bypass = (
    "The register table follows |\n"
    "| register | score |\n"
    "|---|---|\n"
    "| T | 1 |\n"
)
run("header row after a prose line ending in '|'", bypass)
print("    the file that was admitted:")
for line in bypass.rstrip("\n").split("\n"):
    print("      " + line)

for tail, note in (("`", "ends in a backtick"), ("|", "ends in a pipe")):
    rendered = (
        "## Block register\n"
        "\n"
        "Seat note, verbatim: the registers are written T|E|D|G" + tail + "\n"
        "| reason | score |\n"
        "|---|---|\n"
        "| schema | 2 |\n"
    )
    run("rendered record whose prose line " + note, rendered)
    print("    the file offered:")
    for line in rendered.rstrip("\n").split("\n"):
        print("      " + line)

setext = "Scores by seat\n==============\n"
run("setext heading", setext)
print("    the file that was admitted:")
for line in setext.rstrip("\n").split("\n"):
    print("      " + line)

html = "<table><tr><th>cell</th><th>score</th></tr></table>\n"
run("HTML table header", html)

second = (
    "| register | mark |\n"
    "|---|---|\n"
    "| T | differs |\n"
    "\n"
    "| register | score |\n"
    "|---|---|\n"
    "| T | 1 |\n"
)
run("second table after a blank line (control)", second)

glued = (
    "| register | mark |\n"
    "|---|---|\n"
    "| T | differs |\n"
    "| register | score |\n"
    "|---|---|\n"
    "| T | 1 |\n"
)
run("second table glued to the first", glued)
print("    the file that was admitted:")
for line in glued.rstrip("\n").split("\n"):
    print("      " + line)
