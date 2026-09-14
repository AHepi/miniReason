"""Does contracts.py retype any closed-vocabulary token as a literal?

Module docstring: "It ... re-exports, under the spellings the wave plan published
for this module, the closed vocabularies W0-STANDARD owns - including the reading
vocabulary and the instrument's banner, which no module of this package retypes."
and "**And it owns no shared vocabulary** ... The names on both sides are the
*same objects*: there is nothing left to drift."

Scan the source for every member of every closed vocabulary, as a quoted literal.
"""
from __future__ import annotations

import os
import re

import _boot  # noqa: F401

from minireason.loop import standard

SOURCE = os.path.join(_boot.ROOT, "src", "minireason", "loop", "contracts.py")
lines = open(SOURCE, encoding="utf-8").read().split("\n")

vocab = {}
for token in standard.MARKS:
    vocab.setdefault(token, []).append("MARKS")
for token in standard.CRITIC_RELATIONS:
    vocab.setdefault(token, []).append("CRITIC_RELATIONS")
for token in standard.READING_VOCABULARY:
    vocab.setdefault(token, []).append("READING_VOCABULARY")
for token in standard.ALL_DIFFERENCE_KINDS:
    vocab.setdefault(token, []).append("ALL_DIFFERENCE_KINDS")
for token in standard.REGISTERS:
    vocab.setdefault(token, []).append("REGISTERS")

print("code lines (docstrings and comments stripped) carrying a vocabulary token "
      "as a quoted literal:")
in_doc = False
hits = 0
for number, line in enumerate(lines, 1):
    stripped = line.strip()
    if stripped.startswith('"""') or stripped.endswith('"""'):
        # crude, but this module's docstrings all open and close on their own line
        if stripped.count('"""') == 1:
            in_doc = not in_doc
            continue
    if in_doc or stripped.startswith("#"):
        continue
    for token, owners in vocab.items():
        if re.search(rf"""['"]{re.escape(token)}['"]""", line):
            hits += 1
            print(f"  line {number}: {stripped}")
            print(f"      -> {token!r} is a member of {'/'.join(sorted(set(owners)))}")
print(f"total code-line hits: {hits}")
