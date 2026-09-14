#!/usr/bin/env python3
"""Shared machinery for the STAGING-v3 FW5 citation verification.

Everything here is computed from the two declared files:
  SRC     = docs/sources/FW5-explanatory-construction.md  (the FW5 reading edition)
  STAGING = staging/STAGING-v3.md
"""
import bisect
import hashlib
import re

EXPECTED_SHA = "8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a"
SRC = "docs/sources/FW5-explanatory-construction.md"
STAGING = "staging/STAGING-v3.md"

# ---------------------------------------------------------------- extraction
# Citation forms:  FW5:N  FW5:N-M  FW5:N–M  bare :N  bare :N-M  bare :N–M
# with N and M 2-4 digit numbers.  A bare citation may not be preceded by a
# letter or digit (so FW5-form is captured only once and words ending in
# letters, e.g. "PLAN:184-188", do not produce bare matches).
# Staging also writes some ranges with a repeated colon (":950-:952"); the
# optional second colon is absorbed by the ':?' in the end group.
CIT_RE_TEXT = (
    r"(?:FW5:([0-9]{2,4})(?:[-\u2013]:?([0-9]{2,4}))?)"
    r"|(?<![0-9A-Za-z]):([0-9]{2,4})(?:[-\u2013]:?([0-9]{2,4}))?"
)
CIT_RE = re.compile(CIT_RE_TEXT)

# A pattern hit is a citation of a *different* file when the text immediately
# before the colon is a filename (with extension), optionally backtick-closed.
FOREIGN_RE = re.compile(r"[A-Za-z0-9_./-]+\.(?:json|md|py|toml|txt|jsonl)`?\s*$")


def sha256_of(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def load_lines(path):
    """Split file on newline, 1-based; drop the artefactual element after a
    trailing newline so that len(lines) is the real line count."""
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    return lines


def extract_citations(staging_lines):
    """Return list of hits: dict(staging_line, citation, start, end,
    preceded_by, foreign)."""
    hits = []
    for ln, line in enumerate(staging_lines, start=1):
        for m in CIT_RE.finditer(line):
            start = int(m.group(1) or m.group(3))
            end_g = m.group(2) or m.group(4)
            end = int(end_g) if end_g else start
            preceded = line[max(0, m.start() - 80):m.start()]
            fm = FOREIGN_RE.search(preceded)
            hits.append(
                {
                    "staging_line": ln,
                    "citation": m.group(0),
                    "start": start,
                    "end": end,
                    "preceded_by": preceded[-60:],
                    "foreign": fm.group(0).strip(" `") if fm else None,
                }
            )
    return hits


# ---------------------------------------------------------------- fragments
TYPO = {"\u201c": '"', "\u201d": '"', "\u2018": "'", "\u2019": "'"}
BACKTICK_SPAN = re.compile(r"`([^`]*)`")
STRAIGHT_SPAN = re.compile(r'"([^"]*)"')
TYPO_SPAN = re.compile(r"\u201c([^\u201d]*)\u201d")
LATEX_SPAN = re.compile(r"\\\\\((.*?)\\\\\)")

MIN_FRAG = 12


def norm_typo(s):
    """Typographic quotes -> straight."""
    for k, v in TYPO.items():
        s = s.replace(k, v)
    return s


def collapse_ws(s):
    return re.sub(r"\s+", " ", s).strip()


def normalise(s):
    return collapse_ws(norm_typo(s))


def fragments_on_line(line):
    """Quoted fragments on one staging line.  Spans sitting inside a backtick
    span are not double-counted as quote spans.  Returns a list of
    dict(fragment, style, start)."""
    spans = []
    for style, rx in (("backtick", BACKTICK_SPAN), ("straight", STRAIGHT_SPAN),
                      ("typographic", TYPO_SPAN), ("latex", LATEX_SPAN)):
        for m in rx.finditer(line):
            spans.append({"fragment": m.group(1), "style": style,
                          "start": m.start(), "end": m.end()})
    bts = [(s["start"], s["end"]) for s in spans if s["style"] == "backtick"]

    def inside_bt(s):
        return any(s["start"] >= a and s["end"] <= b for a, b in bts)

    out = []
    for s in spans:
        if s["style"] != "backtick" and inside_bt(s):
            continue
        out.append(s)
    out.sort(key=lambda s: s["start"])
    return out


# ---------------------------------------------------------------- matching
class Source:
    def __init__(self, lines):
        self.lines = lines  # 0-based list; line N is self.lines[N-1]
        self.norm_lines = [normalise(l) for l in lines]
        # whole-document normalised text with offsets -> line mapping
        self.joined = " ".join(self.norm_lines)
        self.offsets = []
        pos = 0
        for i, nl in enumerate(self.norm_lines):
            self.offsets.append(pos)
            pos += len(nl) + 1

    def target_raw(self, start, end):
        if end < start:
            return ""
        return "\n".join(self.lines[start - 1:end])

    def target_norm(self, start, end):
        if end < start:
            return ""
        return " ".join(self.norm_lines[start - 1:end])

    def find_lines(self, norm_frag, limit=4):
        """Lines whose normalised text contains norm_frag."""
        return [i + 1 for i, nl in enumerate(self.norm_lines)
                if norm_frag in nl][:limit]

    def find_anywhere(self, norm_frag):
        """First line at which norm_frag occurs in the whole normalised
        document (allows spanning line breaks)."""
        idx = self.joined.find(norm_frag)
        if idx < 0:
            return None
        i = bisect.bisect_right(self.offsets, idx) - 1
        return i + 1
