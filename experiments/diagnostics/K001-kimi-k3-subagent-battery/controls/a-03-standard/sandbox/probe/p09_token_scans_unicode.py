"""Both token scans against text that is not plain ASCII.

The two scans are the module's only guards over *rendered* records, and a
rendered record carries model-authored prose verbatim (a judge's
``reading_note``, a critic's ``case``).  Neither scan normalises its input.
"""
from __future__ import annotations

import unicodedata

import _boot  # noqa: F401

from minireason.loop import standard as S


def exhaustion(label: str, text: str) -> None:
    try:
        S.assert_no_exhaustion_claim(text, "CLOSING.md")
    except S.StandardInvalid as exc:
        print("REFUSED  %-52s %s" % (label, exc.code))
    else:
        print("ADMITTED %-52s %r" % (label, text[:46]))


def headers(label: str, text: str) -> None:
    try:
        S.assert_no_scoring_headers(text, "READING_TABLE.md")
    except S.StandardInvalid as exc:
        print("REFUSED  %-52s %s" % (label, exc.code))
    else:
        print("ADMITTED %-52s %r" % (label, text[:46]))


print("-- assert_no_exhaustion_claim --")
exhaustion("plain ascii (control)", "the inquiry is exhausted")
exhaustion("zero-width space inside the stem", "the inquiry is exhaus​ted")
exhaustion("soft hyphen inside the stem", "the inquiry is exhaus­ted")
exhaustion("fullwidth letters", "the inquiry is ｅxhausted")
exhaustion("NFKD-decomposed nothing to fold (control)",
           unicodedata.normalize("NFKD", "the inquiry is exhausted"))

print()
print("-- assert_no_scoring_headers --")
headers("plain ascii (control)", "| cell | score |\n|---|---|\n")
headers("zero-width space in the header cell", "| cell | sc​ore |\n|---|---|\n")
headers("fullwidth S in the heading", "# Ｓcore by seat\n")
headers("heading, plain ascii (control)", "# Score by seat\n")
