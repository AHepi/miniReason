"""The ``std:reading-rubric/v1`` standard artifact body (wave 0, module W0-STANDARD).

Purpose
-------
This module is the *content* of the one standard artifact the automated loop registers
before any provider call: the rubric text for each question class and its mode, the
reading vocabulary closed to the six published values together with the published
non-exclusivity note it is closed against, the four C001 PLAN §8a registers mirrored
byte-identically, the register-to-falsifier mapping, the closed per-register
``difference_kind`` token sets, the guard parameters, the pre-registered reopen-reason
list, the calibration anchors whose ground truth is true by construction, and the frozen
claim ceiling.  Nothing here reads anything, calls anything or decides anything: it is
data plus the two pure functions that serialise and parse it.

Design section implemented
--------------------------
Automated-loop design of record, §2.1 ("The standard artifact ``std:reading-rubric/v1``")
and §6 ("The claim ceiling of a fully automated run"), with the register text taken from
the frozen C001 ``PLAN.md`` §8a and its ``material.json`` ``reading_rule`` mirror, and the
reading vocabulary imported from :mod:`minireason.use_relation_h005` rather than retyped.

The body is content-addressed: :func:`build_standard` emits canonical JSON bytes (sorted
keys, compact separators, UTF-8 — ``deepreason_core.canonical.canonical_json``), so
:data:`STANDARD_BODY_SHA256` and :data:`CEILING_SHA256` are what a plan pins.  A revised
rubric is a successor artifact and a new ``loop_plan_id``, never an edit (§2.1).

What this module refuses to do
------------------------------
It emits no scalar meter, no rank, no score and no aggregate over readings or marks:
every integer in the built body lies under ``guard_parameters`` or under
``role_contracts.word_limits``, and each one is a declared resource, seat count or prose
bound.  It never describes a stop as exhaustion; the only occurrence of that token in the
shipped bytes is the ceiling's own denial of it.  Counts are never warrants (FW5:851),
and a reading is never a merit predicate (FW5:849).

Deviations from the design, and why
-----------------------------------
1. ``SPEC_ID`` is ``"reading-v1"``, not ``"std:reading-rubric/v1"``.  The design leaves
   the spelling underspecified.  ``Commitment.eval`` is ``"rubric:<spec-id>"`` and the
   design fixes the eval string as ``rubric:reading-v1``, so ``<spec-id>`` is
   ``reading-v1``; the artifact's published *name* is kept separately as
   :data:`STANDARD_NAME` and the assembled eval string as :data:`RUBRIC_EVAL`, so no
   caller has to concatenate.
2. The closed ``difference_kind`` token sets are wider than the one-token-per-register
   list the source design sketched (``T: target_set_membership``; ``E: record_engaged``;
   ``D: disposition_value``; ``G: grounds_source``).  One token per register makes kind
   grain identical to register grain, which is exactly the over-suppression of ``differs``
   that decision D4 rejected.  Every sketched token is kept, spelled identically, and the
   added tokens are only distinctions PLAN §8a itself draws in the register it belongs
   to: the prefix-intact rule for T, the reference-or-quotation rule for E, and the FCL
   field list for D.  G keeps one token, because PLAN §8a gives G a single axis whose
   values already include "none"; inventing a second kind there would not be mirroring.
3. The ceiling's first clause carries per-cell placeholders (the standard digest, the
   relation, the paraphrase count, the audit record), so it cannot be a verbatim required
   sentence.  It is exposed separately as :data:`CEILING_CLAIM_TEMPLATE`;
   :data:`CEILING_REQUIRED_SENTENCES` holds the eleven invariant clauses, each a single
   unwrapped paragraph.  They are stored unwrapped, with the design's blockquote markers
   stripped, so that "appears verbatim" survives a renderer that re-wraps.
4. The design's §6 renders ``CEILING.md`` inside a blockquote; the shipped
   ``data/ceiling_v1.md`` is the same text as plain paragraphs.  The digest pinned into a
   plan is the digest of the shipped bytes.
5. A forbidden-key token set is defined here rather than imported from W0-CONTRACTS.
   The wave-0 integration settled the dependency edge in the other direction:
   :mod:`minireason.loop.contracts` imports this module, so this module may not import
   it.  :data:`FORBIDDEN_KEYS` is therefore owned here, mirrors
   ``tools/contrast_triple_study.FORBIDDEN_KEYS``, and is what ``contracts.FORBIDDEN_KEYS``
   now *is* - one object, not two lists that can drift.
6. **The §2.3 role contracts live here and are pinned into the body.**  They were in
   W0-CONTRACTS, where editing a schema or a word limit changed no digest at all:
   ``loop_plan_id`` folds ``config ∪ pins`` and no pinned path covers this package, so
   §5's "changing any threshold after first look mints a new ``loop_plan_id``" did not
   reach them.  :data:`SCHEMAS`, :data:`WORD_LIMITS`, :data:`ROLE_NAMES`,
   :data:`ROLE_BINDING_FIELDS` and :data:`ALL_DIFFERENCE_KINDS` are therefore owned here
   and re-exported by ``contracts`` under the same names and as the same objects, and the
   built body carries a ``role_contracts`` section holding the word limits and
   ``sha256(canonical(SCHEMAS))``.  Editing either changes :data:`STANDARD_BODY_SHA256`.
   The schemas ride as a digest rather than as their own JSON so that the body's integer
   oracle stays exact (deviation 6 of ``_role_contracts_section``).
7. **The unanimity rule names no number of seats.**  ``judge_seats`` is a successor
   standard's parameter with an admissible range wider than two, and a rule reading "Both
   judge seats" would ship a sentence describing two seats to a three-seat panel, whose
   natural repair is a majority - the one thing G5 forbids.  It reads "Every judge seat",
   and R10 of the relation rubric matches it.
8. **One reconciliation between the two owners of the guard parameters.**
   :func:`assert_config_matches_standard` refuses a loop config whose ``seats`` block or
   ``reopen_reasons`` contradict :data:`GUARD_PARAMETERS`.  PREFLIGHT must call it (W5).

Ownership after wave-0 integration
----------------------------------
This module is the single owner of every constant the loop's role contracts and its
renderers share: :data:`READING_VOCABULARY`, :data:`NOMINABLE_RELATIONS`,
:data:`CRITIC_RELATIONS`, :data:`NONE_TOKEN`, :data:`UNRESOLVED_TOKEN`,
:data:`OUTSIDE_VOCABULARY_FIELD`, :data:`READING_BANNER`, :data:`MARKS`,
:data:`REGISTER_IDS` (also exported as :data:`REGISTERS`, the spelling W0-CONTRACTS
publishes), :data:`DIFFERENCE_KINDS`, :data:`ALL_DIFFERENCE_KINDS`, :data:`ROLE_NAMES`,
:data:`ROLE_BINDING_FIELDS`, :data:`WORD_LIMITS`, :data:`SCHEMAS` (and the five per-role
schemas), :data:`FORBIDDEN_KEYS` and :data:`CEILING_REQUIRED_SENTENCES`.
``contracts.py`` imports all of them and defines none of them; W3-REPORT imports
:data:`CEILING_REQUIRED_SENTENCES` and :func:`assert_no_scoring_headers` from here.  This
module imports :mod:`minireason.loop.types` (for :class:`~minireason.loop.types.LoopError`
only) and nothing else from the package, so the edge
``types -> standard -> contracts`` is acyclic.

Two collisions the integration closed
-------------------------------------
* The frozen ceiling clause "A reached ceiling is a declared resource boundary, **not
  exhaustion of the inquiry**" contains the token ``exhaustion``, and a renderer-side scan
  that banned the token outright would delete the sentence that states the house rule.
  :func:`assert_no_exhaustion_claim` is that scan, with
  :data:`CEILING_EXHAUSTION_DENIAL` as its one exemption; the frozen ceiling passes it and
  a renderer string carrying the token anywhere else is refused.
* Ceiling clause seven fixes nine block reason codes by name — ``ensemble-split``,
  ``referential-integrity``, ``operative-target``, ``order-swap``, ``paraphrase-flip``,
  ``outside-vocabulary``, ``schema``, ``provider``, ``baseline-forced-same``.  W0-TYPES'
  ``BLOCK_CODES`` now carries all nine plus ``blocked:constitution``, and
  ``types.CEILING_BLOCK_REASONS`` names the nine; ``tests/loop/test_standard.py`` asserts
  the correspondence against this module's own ceiling bytes, in both directions.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Final, Mapping, Sequence

from deepreason_core.canonical import canonical_json, sha256_hex

from minireason.loop.types import CEILING_BLOCK_REASONS, LoopError
from minireason.use_relation_h005 import ROOT_READING_VOCABULARY, USE_RELATION_BANNER

__all__ = [
    "ALL_DIFFERENCE_KINDS",
    "CALIBRATION_ANCHORS",
    "CEILING_CLAIM_TEMPLATE",
    "CEILING_EXHAUSTION_DENIAL",
    "CEILING_PATH",
    "CEILING_REQUIRED_SENTENCES",
    "CEILING_SHA256",
    "CEILING_TEXT",
    "CRITIC_RELATIONS",
    "CRITIC_SCHEMA",
    "CalibrationAnchor",
    "DEFENDER_SCHEMA",
    "DIFFERENCE_KINDS",
    "DifferenceKind",
    "FALSIFIER_MAP",
    "FORBIDDEN_KEYS",
    "Falsifier",
    "GUARD_PARAMETERS",
    "GUARD_PARAMETER_KEYS",
    "JUDGE_SCHEMA",
    "MARKER_SCHEMA",
    "MARKS",
    "MODES",
    "MODE_ABSOLUTE",
    "MODE_PAIRWISE",
    "NOMINABLE_RELATIONS",
    "DIFFERS_MARK",
    "NONE_TOKEN",
    "OUTSIDE_VOCABULARY_FIELD",
    "PLAN_8A_MIRROR",
    "PLAN_8A_MIRROR_PATH",
    "PLAN_8A_REGISTERS",
    "READING_BANNER",
    "READING_VOCABULARY",
    "REGISTERS",
    "REGISTER_IDS",
    "REOPEN_REASONS",
    "ROLE_BINDING_FIELDS",
    "ROLE_NAMES",
    "ROLE_SCHEMAS_SHA256",
    "RUBRIC_EVAL",
    "RUBRIC_V1",
    "Register",
    "RubricClass",
    "SCHEMAS",
    "SPEC_ID",
    "STANDARD_BODY",
    "STANDARD_BODY_SHA256",
    "STANDARD_NAME",
    "STANDARD_SCHEMA",
    "StandardInvalid",
    "UNRESOLVED_TOKEN",
    "VARIATOR_SCHEMA",
    "WORD_LIMITS",
    "assert_config_matches_standard",
    "assert_no_exhaustion_claim",
    "assert_no_scoring_headers",
    "build_standard",
    "standard_body",
]


# --------------------------------------------------------------------- failures

class StandardInvalid(LoopError, ValueError):
    """A declared refusal.  ``code`` is the stable token; the message carries detail.

    The repository convention (``tools/contrast_triple_study.failure_code``) reads a
    declared ``code`` attribute first, so the detail in the message never changes the
    code a receipt records.

    A subclass of :class:`~minireason.loop.types.LoopError`, so one ``except LoopError``
    catches every wave-0 refusal and every code is listed in
    ``types.FAILURE_CODES``; still a ``ValueError``, so a caller written against the
    original spelling keeps working.  The rendered message is unchanged.
    """

    def __init__(self, code: str, detail: str = "") -> None:
        LoopError.__init__(self, code, detail)


#: Mirrored from ``tools/contrast_triple_study.FORBIDDEN_KEYS``; see deviation 5.  This
#: module owns the set for the package: ``contracts.FORBIDDEN_KEYS`` *is* this object.
FORBIDDEN_KEYS: Final[frozenset[str]] = frozenset({
    "score", "scores", "scoring", "rank", "ranking", "ranks", "merit", "grade", "grades",
    "rating", "ratings", "points", "novelty", "creativity", "quality", "winner", "win",
    "best", "worst", "better", "worse", "weight", "weights", "percentile", "verdict",
})


#: An ATX Markdown heading: up to three leading spaces, one to six ``#``, text.
_MD_HEADING: Final[re.Pattern[str]] = re.compile(r"^ {0,3}(#{1,6})\s+(.*?)\s*#*\s*$")

#: A word a header cell or a heading can carry, for the G12 token comparison.
_MD_WORD: Final[re.Pattern[str]] = re.compile(r"[A-Za-z][A-Za-z0-9_]*")

#: The characters a GitHub-flavoured table's delimiter row is made of.
_MD_DELIMITER_CHARS: Final[frozenset[str]] = frozenset("|:- \t")

#: What a Markdown line may carry before its content: a blockquote marker, a
#: bullet, an ordered-list number, an ATX heading's hashes.  Stripped before a
#: token scan so a rendering decision cannot hide (or fabricate) a match.
_MD_LINE_PREFIX: Final[re.Pattern[str]] = re.compile(r"\A[ \t]*(?:[>#*+-]|\d+[.)])[ \t]*")

#: The characters that carry emphasis, code and strikethrough.  Removed - not
#: replaced by a space - so ``**exhaust**ion`` reads as one word, the way a
#: reader sees it.
_MD_EMPHASIS: Final[re.Pattern[str]] = re.compile(r"[*_`~]+")


def _normalised(value: Any) -> str:
    """NFKC, with format characters (``Cf``) removed.

    A token scan that reads raw code points can be walked past with a zero-width
    joiner inside the word or a compatibility spelling of a letter; both render
    as the word a reader sees.  Normalising first means the scan reads what is
    read.
    """

    text = "".join(ch for ch in str(value) if unicodedata.category(ch) != "Cf")
    return unicodedata.normalize("NFKC", text)


def _strip_markdown(text: Any) -> str:
    """One line-joined, prefix- and emphasis-stripped, NFKC copy of ``text``.

    Used by the two token scans, which ask what a *reader* sees rather than what
    a renderer wrote: a clause the design of record quotes as a blockquote, or
    re-wrapped across lines, or with a word emphasised, is the same clause.
    """

    lines = []
    for line in _normalised(text).split("\n"):
        previous = None
        while previous != line:
            previous = line
            line = _MD_LINE_PREFIX.sub("", line, count=1)
        lines.append(line)
    return _MD_EMPHASIS.sub("", " ".join(" ".join(lines).split()))


def _is_delimiter_row(line: str) -> bool:
    """``|---|:--:|`` - the row that turns the line above it into a header.

    A delimiter row must carry a ``|``: ``---`` on its own is a thematic break
    (or a setext underline), and reading it as a delimiter would make the prose
    line above it a table header.
    """

    stripped = line.strip()
    return (bool(stripped) and "-" in stripped and "|" in stripped
            and set(stripped) <= _MD_DELIMITER_CHARS)


def _refuse_scoring_words(text: str, where: str) -> None:
    for word in _MD_WORD.findall(_normalised(text)):
        if word.lower() in FORBIDDEN_KEYS:
            raise StandardInvalid(
                "SCORING_KEY_FORBIDDEN",
                f"{where} carries the scoring word {word!r}; a label that names an "
                "outcome is not a quantity and no header may assert one",
            )


def assert_no_scoring_headers(text: str, where: str = "record") -> None:
    """G12 over a **rendered** file: its table headers and its headings.

    Design §2.4 G12 runs the scoring-key guard "over every emitted artifact,
    **every table header and every rendered file**".  A rendered file is a string,
    not a key structure, so :func:`~minireason.loop.contracts.assert_no_scoring_keys`
    cannot see into it - and silently answering ``None`` for a ``READING_TABLE.md``
    carrying a ``score`` column would make §5's protected obligation *p4* ("no
    scoring key appears anywhere") unfalsifiable on two of its three named subjects.
    This is the scanner for the other two.

    Scanned: every ATX Markdown heading, and the **header row** of every Markdown
    table - which is GitHub-flavoured Markdown's own rule, *the line immediately
    above a delimiter row*, and nothing else.  It used to be "the first row of
    each contiguous block of pipe rows", under which a paragraph line that
    happened to end in ``|`` became the header and the real header below it -
    the one carrying the ``score`` column - was read as a body row and never
    scanned.  Body rows are prose and are not scanned: a cell may *say* the word
    ``score`` in a sentence, exactly as :func:`assert_no_scoring_keys` admits a
    scoring word in a value.

    Out of scope, and stated so rather than implied: **setext** headings
    (``Title`` over ``===``) and any table written as HTML (``<th>``).  Neither
    appears in this repository's rendered records; a wave that starts emitting
    one extends this scan in the same commit.

    Raises :class:`StandardInvalid` with code ``SCORING_KEY_FORBIDDEN`` (the same
    code the key guard raises, so a receipt records one token for one rule).  Pure:
    it reads only its argument.  The frozen ceiling passes it unchanged.
    """

    lines = str(text).split("\n")
    for index, line in enumerate(lines):
        heading = _MD_HEADING.match(line)
        if heading is not None:
            _refuse_scoring_words(heading.group(2), f"{where} heading on line {index + 1}")
            continue
        if index == 0 or not _is_delimiter_row(line):
            continue
        header = lines[index - 1]
        if "|" not in header or _is_delimiter_row(header):
            continue                      # a delimiter row under no header
        for cell in header.strip().strip("|").split("|"):
            _refuse_scoring_words(cell, f"{where} table header on line {index}")


def _refuse_forbidden_keys(value: Any) -> None:
    """Raise ``SCORING_KEY_FORBIDDEN`` if a scoring key is nested anywhere in ``value``."""
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).lower() in FORBIDDEN_KEYS:
                raise StandardInvalid("SCORING_KEY_FORBIDDEN", str(key))
            _refuse_forbidden_keys(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _refuse_forbidden_keys(item)


# ------------------------------------------------------------------ identity

#: The ``<spec-id>`` half of the commitment eval; see deviation 1.
SPEC_ID: Final[str] = "reading-v1"

#: The standard artifact's published name (design §2.1).
STANDARD_NAME: Final[str] = "std:reading-rubric/v1"

#: ``Commitment.eval`` for the cell commitment kappa_read.  ``ontology/commitment.py``
#: requires the spec-id to resolve to a registered standard artifact (spec §10.3).
RUBRIC_EVAL: Final[str] = f"rubric:{SPEC_ID}"

#: Schema token of the serialised body.
STANDARD_SCHEMA: Final[str] = "minireason.loop.reading-rubric.v1"

#: What the cell's commitment says, and what a sustained trial makes fail (design D3).
COMMITMENT_READS: Final[str] = (
    "No relation from the registered vocabulary is established for this cell by a "
    "guarded trial over the frozen juxtaposition. A sustained trial is a `fail` on this "
    "commitment; an unsustained trial registers nothing and the cell stays unresolved."
)


# ------------------------------------------------------------------- data files

_DATA: Final[Path] = Path(__file__).resolve().parent / "data"

#: The byte-identical PLAN §8a excerpt and its ``material.json`` mirror.
PLAN_8A_MIRROR_PATH: Final[Path] = _DATA / "plan_8a_mirror.json"

#: The frozen claim ceiling (design §6).
CEILING_PATH: Final[Path] = _DATA / "ceiling_v1.md"

#: The four PLAN §8a register ids, named before the mirror is read so the mirror
#: can be checked against them rather than believed.
_PLAN_REGISTER_IDS: Final[tuple[str, ...]] = ("T", "E", "D", "G")

#: The three marks, likewise.  A mirror that widened this would widen
#: :data:`MARKS`, :data:`MARKER_SCHEMA` and the body in one edit, and a mark
#: value spelled ``better`` would be a scoring word inside the instrument.
_PLAN_MARKS: Final[tuple[str, ...]] = ("differs", "same", "unresolved")

#: The keys the mirror must carry, each of which reaches the standard body.
_PLAN_MIRROR_KEYS: Final[frozenset[str]] = frozenset({
    "marks", "never_aggregated", "order_of_reading", "preamble",
    "register_to_falsifier", "registers", "replicate_baseline", "source",
    "two_readers",
})

#: The ceiling is twelve clauses: one per-cell claim template and eleven
#: invariants (design §6).  A truncated file would leave
#: :data:`CEILING_REQUIRED_SENTENCES` short - or empty - and W3-REPORT's
#: "every one appears verbatim" assertion would pass over nothing.
_CEILING_CLAUSE_COUNT: Final[int] = 12

#: How clause 0 opens.  It is the clause a cell renders, and a file whose first
#: paragraph is something else is not this ceiling.
_CEILING_CLAIM_OPENING: Final[str] = "**What this run claims.**"


def _read_data(path: Path) -> bytes:
    """Read one shipped data file, or refuse with a code.

    A missing or unreadable file used to raise ``FileNotFoundError`` out of
    import: not a :class:`LoopError`, so a caller that catches one saw nothing.
    """

    try:
        return path.read_bytes()
    except OSError as exc:
        raise StandardInvalid(
            "STANDARD_DATA_MISSING",
            f"{path.name} cannot be read: {type(exc).__name__}") from exc


def _load_plan_mirror(path: Path) -> Mapping[str, Any]:
    """Parse and **check the shape of** the frozen PLAN §8a mirror.

    Nothing downstream re-checks it: :data:`MARKS`, :data:`MARKER_SCHEMA`, the
    register set and the standard body are all derived from this file, so an
    edit to it is an edit to the instrument.  The checks below are the ones that
    would otherwise be made by nobody.
    """

    raw = _read_data(path)
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise StandardInvalid("STANDARD_DATA_MALFORMED", f"{path.name}: {exc}") from exc
    if not isinstance(parsed, dict):
        raise StandardInvalid("PLAN_MIRROR_MALFORMED",
                              f"{path.name} is {type(parsed).__name__}, not an object")
    missing = sorted(_PLAN_MIRROR_KEYS - set(parsed))
    if missing:
        raise StandardInvalid("PLAN_MIRROR_MALFORMED", f"{path.name} is missing {missing}")
    marks = parsed["marks"]
    if not isinstance(marks, list) or tuple(marks) != _PLAN_MARKS:
        raise StandardInvalid(
            "PLAN_MIRROR_MALFORMED",
            f"marks must be exactly {list(_PLAN_MARKS)}, not {marks!r}")
    registers = parsed["registers"]
    if not isinstance(registers, dict) or set(registers) != set(_PLAN_REGISTER_IDS):
        raise StandardInvalid(
            "REGISTER_SET_MISMATCH",
            f"the mirror names {sorted(registers) if isinstance(registers, dict) else registers!r}, "
            f"not {sorted(_PLAN_REGISTER_IDS)}")
    for rid in _PLAN_REGISTER_IDS:
        block = registers[rid]
        if not isinstance(block, dict):
            raise StandardInvalid("PLAN_MIRROR_MALFORMED", f"register {rid} is not an object")
        for field_name in ("plan_text", "name"):
            if not str(block.get(field_name, "")).strip():
                raise StandardInvalid("REGISTER_TEXT_EMPTY", f"{rid}.{field_name}")
    return MappingProxyType(parsed)


def _ceiling_clauses(text: str, where: str) -> tuple[str, ...]:
    """The ceiling's paragraphs, checked for the shape §6 promises."""

    clauses = tuple(para.strip() for para in text.split("\n\n") if para.strip())
    if len(clauses) != _CEILING_CLAUSE_COUNT:
        raise StandardInvalid(
            "CEILING_TEXT_MALFORMED",
            f"{where} holds {len(clauses)} clauses, not {_CEILING_CLAUSE_COUNT}")
    if not clauses[0].startswith(_CEILING_CLAIM_OPENING):
        raise StandardInvalid(
            "CEILING_TEXT_MALFORMED",
            f"{where} clause 0 does not open {_CEILING_CLAIM_OPENING!r}")
    register_clause = [c for c in clauses if "block register by reason code" in c]
    if len(register_clause) != 1:
        raise StandardInvalid("CEILING_TEXT_MALFORMED",
                              f"{where} names the block register in "
                              f"{len(register_clause)} clauses, not one")
    absent = [reason for reason in CEILING_BLOCK_REASONS
              if f"`{reason}`" not in register_clause[0]]
    if absent:
        raise StandardInvalid(
            "CEILING_TEXT_MALFORMED",
            f"{where}'s block-register clause does not print {absent}; W3-REPORT "
            "prints the register this clause promises")
    return clauses


PLAN_8A_MIRROR: Final[Mapping[str, Any]] = _load_plan_mirror(PLAN_8A_MIRROR_PATH)

CEILING_TEXT: Final[str] = _read_data(CEILING_PATH).decode("utf-8")
CEILING_SHA256: Final[str] = sha256_hex(_read_data(CEILING_PATH))

_CEILING_CLAUSES: Final[tuple[str, ...]] = _ceiling_clauses(CEILING_TEXT,
                                                            CEILING_PATH.name)

#: The ceiling's per-cell clause.  Not a verbatim requirement; see deviation 3.
CEILING_CLAIM_TEMPLATE: Final[str] = _CEILING_CLAUSES[0]

#: The eleven invariant ceiling clauses.  Every rendered table and the closing record
#: must carry each of these verbatim (design §6).  W3-REPORT imports this tuple from
#: here; it is the one place the required sentences live.
CEILING_REQUIRED_SENTENCES: Final[tuple[str, ...]] = _CEILING_CLAUSES[1:]


# ------------------------------------------------- the resource-boundary token scan

#: The one phrase in which the token below is admitted: the ceiling's own denial.  Every
#: other occurrence, anywhere in a generated record, is a stop described as the inquiry
#: having run out of things to say, which AGENTS.md forbids and design §4.4 keeps out of
#: the stop vocabulary.
CEILING_EXHAUSTION_DENIAL: Final[str] = "not exhaustion of the inquiry"

_EXHAUSTION_STEM: Final[str] = "exhaust"

if CEILING_EXHAUSTION_DENIAL not in CEILING_TEXT:
    raise StandardInvalid(
        "CEILING_TEXT_MALFORMED",
        f"{CEILING_PATH.name} does not carry the denial "
        f"{CEILING_EXHAUSTION_DENIAL!r}; the one sentence that states the house "
        "rule is also the one exemption the token scan grants")


def assert_no_exhaustion_claim(text: str, where: str = "record") -> None:
    """Refuse a record that describes a reached ceiling as the inquiry running out.

    A blanket token scan cannot simply ban the stem: the frozen ceiling *denies* the
    claim in so many words, and banning the denial would delete the sentence that states
    the house rule.  So :data:`CEILING_EXHAUSTION_DENIAL` is removed first, and what
    remains is scanned for the stem ``exhaust`` - which also catches ``exhausted`` and
    ``exhaustive``, neither of which belongs in a stop record either.

    The removal is **whitespace-, case-, prefix- and emphasis-insensitive**.  Deviation 3
    stores the ceiling clauses unwrapped so that "appears verbatim" survives a renderer
    that re-wraps, and a byte-exact exemption would have refused exactly that: the denial
    re-wrapped across two lines, sentence-cased at the start of a sentence, or upper-cased
    in a heading.  Design §6 renders the clause as a **blockquote**, which puts ``> `` in
    front of every line it wraps onto, and a renderer may emphasise a word inside it;
    both used to break the exemption, so the record that states the house rule was
    refused for stating it.  The scanned copy is therefore :func:`_strip_markdown` of the
    text - line prefixes removed, emphasis removed, lines joined, NFKC, case-folded - and
    the denial is removed from it in the same form.  The smuggle direction is unchanged:
    removing the denial concatenates the halves of any claim built around it, and the stem
    scan then catches the join.

    Raises :class:`StandardInvalid` with code ``RESOURCE_BOUNDARY_MISDESCRIBED``.  Pure:
    it reads only its argument.
    """

    flattened = _strip_markdown(text).casefold()
    scanned = flattened.replace(_strip_markdown(CEILING_EXHAUSTION_DENIAL).casefold(), "")
    index = scanned.find(_EXHAUSTION_STEM)
    if index >= 0:
        raise StandardInvalid(
            "RESOURCE_BOUNDARY_MISDESCRIBED",
            f"{where} describes a boundary as {scanned[index:index + 24]!r}; "
            "a reached ceiling is a declared resource boundary",
        )


# ------------------------------------------------------------------ vocabulary

#: The six published values, imported from the instrument rather than retyped.
#: ``tuple()`` of a tuple returns the published object itself, so this *is*
#: ``use_relation_h005.ROOT_READING_VOCABULARY`` and cannot drift from it.
READING_VOCABULARY: Final[tuple[str, ...]] = tuple(ROOT_READING_VOCABULARY)

#: The token shared by the reading vocabulary and the mark vocabulary, and the state
#: every cell starts in (design D3: it is the position that must be beaten).
UNRESOLVED_TOKEN: Final[str] = "unresolved"

#: The five values a critic may nominate.  ``unresolved`` is where a cell stays when no
#: trial sustains; it is never a relation a critic argues for, so the critic's own schema
#: offers the five relations and the ``none`` token instead (design §2.3).
NOMINABLE_RELATIONS: Final[tuple[str, ...]] = tuple(
    value for value in READING_VOCABULARY if value != UNRESOLVED_TOKEN
)

#: The critic's "no relation is being claimed" answer.  It ends the row at one call.
NONE_TOKEN: Final[str] = "none"

#: Exactly what a critic's schema enumerates: the nominable relations in the published
#: order, then the ``none`` token.  Derived here so W0-CONTRACTS' ``CRITIC_RELATIONS``
#: is this object rather than a second list that could be reordered independently.
#: The order is the instrument's published order and carries no rank: nothing in this
#: package compares two members or maps one to a number.
CRITIC_RELATIONS: Final[tuple[str, ...]] = NOMINABLE_RELATIONS + (NONE_TOKEN,)

#: The escape that keeps a reading the six values do not cover (design D6).
OUTSIDE_VOCABULARY_FIELD: Final[str] = "outside_vocabulary"

OUTSIDE_VOCABULARY_EFFECT: Final[str] = (
    "A non-empty `outside_vocabulary` forces the machine cell to `unresolved` with "
    "reason `outside-vocabulary`, registers no relation, and preserves the text "
    "unaltered for a human reader."
)

#: The instrument's own banner, imported so the standard cannot drift from it.
READING_BANNER: Final[str] = USE_RELATION_BANNER

#: Reproduced verbatim from the published note on
#: ``minireason.use_relation_h005.ROOT_READING_VOCABULARY``.  Closing the vocabulary is a
#: narrowing of a published instrument and the ceiling says so; the note is carried inside
#: the standard so that what is being narrowed is attackable alongside the narrowing.
VOCABULARY_NOTE: Final[str] = (
    "A **suggested** vocabulary for ``root_reading``, published so that the cell\n"
    "has a declared range and so that two readers of two tables mean the same\n"
    "thing by the same word. It is not a closed single-valued enum: review §5 P1\n"
    "names five relations without saying a row carries only one, and `qualifies`,\n"
    "`repairs` and `rejects-with-reason` are not obviously exclusive on a record\n"
    "that concedes one point while repairing another. Root may write more than\n"
    "one, and may write a reading this vocabulary does not cover - and say so.\n"
    "The instrument never selects from it, and nothing here is enforced in code."
)


# ---------------------------------------------------------------- rubric classes

MODE_ABSOLUTE: Final[str] = "absolute"
MODE_PAIRWISE: Final[str] = "pairwise"
MODES: Final[tuple[str, ...]] = (MODE_ABSOLUTE, MODE_PAIRWISE)


@dataclass(frozen=True)
class RubricClass:
    """One question class of the standard, with the mode it is tried in."""

    id: str
    mode: str
    question: str
    body: str
    values: tuple[str, ...]

    def as_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "mode": self.mode,
            "question": self.question,
            "body": self.body,
            "values": list(self.values),
        }


_RELATION_BODY: Final[str] = """\
R1. The question is never "what relation is this?". It is: does the cited passage
    establish the relation the critic named, on the frozen material and on nothing else?
R2. The mode is absolute. Each nominated relation is tried on its own occasion; no two
    relations and no two seats are compared, and no seat is ranked against another. There
    is no merit predicate here (FW5:849), and endpoints are independent occasions to look
    for one pattern, never competitors.
R3. The position defended is the null: that the juxtaposition does not establish the
    claimed relation. A sustained trial is a `fail` on the cell's own commitment and
    nothing else is thereby decided.
R4. `unresolved` is a first-class outcome and is where the cell stays. Non-evaluability
    is not refutation (FW5:657, :682, :688), and an unresolved cell proves neither
    presence nor absence (FW5:634).
R5. A lexical overlap is not evidence of use. A witness of reason use "must preserve
    internal role bindings, not merely the endpoint string" (FW5:628); prompt appearance
    is a delivery fact while actual use is "not automatically machine-maintainable"
    (FW5:640). Shared wording alone sustains nothing.
R6. The citation must be a passage of the material. It must occur exactly once in the
    resolvable surface, and its resolved span must lie inside the declared referring
    record, the declared target record or a listed referring body passage. A span in the
    pack's headings, instruction, vocabulary list, banner or resolver notes is void:
    scrutiny must reach the operative target, and a reading grounded in the prompt's own
    scaffolding is not a reading of the material.
R7. The vocabulary is closed to the six published values for this run, and the closing is
    part of the claim. A reading the six do not cover is written into
    `outside_vocabulary`, which forces the cell to `unresolved` with reason
    `outside-vocabulary` and preserves the text.
R8. `rejects-with-reason` is a reading of what a record's content does. It is never an
    attack edge. No reading of any value mints an `att` or a `dep` on any node under
    study; promoting a declared relation into an adjudicative edge is the error FW5:653
    names.
R9. The strongest positive outcome available to this procedure is *consistent-with*. A
    sustained relation is not a witness of reason use.
R10. Where the judge seats do not return the same ruling, the cell is unresolved and
    every ruling is recorded verbatim. A disagreement is never averaged and never
    settled by majority (FW5:634)."""

_MARK_BODY: Final[str] = """\
M1. The mode is pairwise: one cell, one comparison, one register, one call. No call sees
    a second register, so no call can trade one register off against another.
M2. The marks are `differs`, `same` and `unresolved`. The register definitions are PLAN
    §8a's own, mirrored byte-identically and not paraphrased here.
M3. The four registers are reported separately and stand or fall separately. They are
    never summed, averaged, weighted, ranked or reduced to one mark (FW5:851).
M4. A mark is not a quantity, and no count of marks warrants anything (FW5:851). Counts
    may defeat; they never warrant.
M5. The within-ORIGINAL baseline is written first and is not revised afterwards. A
    `differs` is admissible only if its `difference_kind` token is absent from the frozen
    baseline's kind set for that register; where the token is present the program writes
    `same` and records the baseline replicate pair that forced it.
M6. Register E: a bare id token shared with the account document is `unresolved` for that
    register and never `differs`.
M7. Absent data is reported as absent data. Fewer than three resolved replicates of a
    case yields no mark for that case; it is reported unresolved, never as an absence of
    difference.
M8. Where two readers disagree on a register, that register is `unresolved` for that cell
    and the disagreement is recorded, never averaged (FW5:634)."""

#: The rubric text per question class.  Relation trials are ``absolute``; contrast marks
#: are ``pairwise`` (design §2.1).
RUBRIC_V1: Final[Mapping[str, RubricClass]] = MappingProxyType({
    "relation": RubricClass(
        id="relation",
        mode=MODE_ABSOLUTE,
        question=(
            "Does the cited passage, read on the frozen juxtaposition alone, establish "
            "the named relation between the referring record and the target record?"
        ),
        body=_RELATION_BODY,
        values=READING_VOCABULARY,
    ),
    "contrast-mark": RubricClass(
        id="contrast-mark",
        mode=MODE_PAIRWISE,
        question=(
            "On this one register and this one case pair, does the successor's "
            "commitment surface differ in a way the within-ORIGINAL replicate baseline "
            "does not already show?"
        ),
        body=_MARK_BODY,
        values=tuple(PLAN_8A_MIRROR["marks"]),
    ),
})

#: The three marks, mirrored from the frozen material.
MARKS: Final[tuple[str, ...]] = tuple(PLAN_8A_MIRROR["marks"])

#: The one mark that owes a ``difference_kind`` and two quotes. Named here, once,
#: because it is a **program** token: W0-CONTRACTS tested for it as a retyped
#: literal at two sites, and a literal retyped is a literal that can drift from
#: the frozen material it is supposed to mirror.
DIFFERS_MARK: Final[str] = "differs"


# -------------------------------------------------------------------- registers

REGISTER_IDS: Final[tuple[str, ...]] = _PLAN_REGISTER_IDS

#: The spelling W0-CONTRACTS publishes for the same four ids, so a caller that imported
#: ``contracts.REGISTERS`` and a caller that imported ``standard.REGISTER_IDS`` hold one
#: object.  They are marked separately and are never summed, averaged, weighted, ranked
#: or reduced to one mark.
REGISTERS: Final[tuple[str, ...]] = REGISTER_IDS


@dataclass(frozen=True)
class DifferenceKind:
    """One token of a register's closed ``difference_kind`` set."""

    token: str
    reads: str
    plan_grounding: str

    def as_json(self) -> dict[str, Any]:
        return {
            "token": self.token,
            "reads": self.reads,
            "plan_grounding": self.plan_grounding,
        }


@dataclass(frozen=True)
class Register:
    """One PLAN §8a register: its frozen text, and the kinds a difference may take."""

    id: str
    name: str
    plan_text: str
    reads: str
    differs_iff: str
    difference_kinds: tuple[DifferenceKind, ...]
    carries_falsifiers: tuple[str, ...]

    @property
    def kind_tokens(self) -> tuple[str, ...]:
        return tuple(kind.token for kind in self.difference_kinds)

    def as_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "plan_text": self.plan_text,
            "reads": self.reads,
            "differs_iff": self.differs_iff,
            "difference_kinds": [kind.as_json() for kind in self.difference_kinds],
            "carries_falsifiers": list(self.carries_falsifiers),
        }


_KINDS: Final[Mapping[str, tuple[DifferenceKind, ...]]] = {
    "T": (
        DifferenceKind(
            token="target_set_membership",
            reads="The two sides name different sets of distinct targets.",
            plan_grounding="`differs` iff the two sets of distinct targets are not the same set.",
        ),
        DifferenceKind(
            token="target_prefix_source",
            reads=(
                "The same bare target name is carried under a different source-artifact "
                "prefix on the two sides."
            ),
            plan_grounding=(
                "read **with the source artifact prefix intact** — a reference into "
                "the account is not a reference into the objection."
            ),
        ),
    ),
    "E": (
        DifferenceKind(
            token="record_engaged",
            reads="The two sides take up different objection records.",
            plan_grounding=(
                "Which of the objection document's records (`o1 o2 o3 c1 c2 o4 p1 u1`) "
                "the successor takes up, by prefix-qualified reference (resolved per "
                "§7) or by quotation of that record's own text."
            ),
        ),
        DifferenceKind(
            token="engagement_form",
            reads=(
                "The same objection record is taken up by prefix-qualified reference on "
                "one side and by quotation of that record's own text on the other."
            ),
            plan_grounding=(
                "by prefix-qualified reference (resolved per §7) or by quotation of "
                "that record's own text."
            ),
        ),
    ),
    "D": (
        DifferenceKind(
            token="disposition_value",
            reads="The disposition attached to the same criticism changes.",
            plan_grounding="`differs` iff the disposition attached to the same criticism changes.",
        ),
        DifferenceKind(
            token="disposition_carrier_field",
            reads=(
                "The same disposition is carried by a different FCL field on the two "
                "sides, among `type`, `uptake`, `revises`, `withdraws` and `action`."
            ),
            plan_grounding=(
                "FCL arm: read off record `type`, `uptake`, `revises`, `withdraws` and "
                "the `action` field."
            ),
        ),
    ),
    "G": (
        DifferenceKind(
            token="grounds_source",
            reads="The cited source of grounds is not the same.",
            plan_grounding=(
                "Whether the successor grounds that disposition in the objection's "
                "grounds, the account's, the rival's, or none. `differs` iff the cited "
                "source of grounds is not the same."
            ),
        ),
    ),
}

_CARRIES: Final[Mapping[str, tuple[str, ...]]] = {
    "T": ("D1", "F2", "F3"),
    "E": ("D1", "F2", "F3"),
    "D": ("D1", "F2", "F3"),
    "G": (),
}


def _build_registers() -> Mapping[str, Register]:
    mirrored = PLAN_8A_MIRROR["registers"]
    return {
        rid: Register(
            id=rid,
            name=mirrored[rid]["name"],
            plan_text=mirrored[rid]["plan_text"],
            reads=mirrored[rid]["reads"],
            differs_iff=mirrored[rid]["differs_iff"],
            difference_kinds=_KINDS[rid],
            carries_falsifiers=_CARRIES[rid],
        )
        for rid in REGISTER_IDS
    }


#: The four C001 registers, their PLAN §8a text byte-identical to the frozen plan.
PLAN_8A_REGISTERS: Final[Mapping[str, Register]] = MappingProxyType(dict(_build_registers()))

#: The closed ``difference_kind`` token set per register.  ``contracts.DIFFERENCE_KINDS``
#: *is* this object; there is one owner and nothing left to drift.
DIFFERENCE_KINDS: Final[Mapping[str, tuple[str, ...]]] = MappingProxyType({
    rid: PLAN_8A_REGISTERS[rid].kind_tokens for rid in REGISTER_IDS
})

#: Every token any register admits, sorted.  The marker enum, and what
#: ``contracts.check`` holds a marker to when the register is not known.
ALL_DIFFERENCE_KINDS: Final[tuple[str, ...]] = tuple(sorted(
    {token for tokens in DIFFERENCE_KINDS.values() for token in tokens}
))


# --------------------------------------------------------------- role contracts
#
# §2.3's prompt contracts are pre-registered guard content: the five role schemas
# and the prose word bounds.  They live here, not in W0-CONTRACTS, for one reason
# (deviation 6): the standard body is the artifact a plan pins, and until §2.3 was
# inside it, editing a schema or a word limit changed no digest at all -
# ``loop_plan_id`` folds ``config ∪ pins`` and no pin covers this package.  §5 says
# "changing any threshold after first look mints a new ``loop_plan_id``", so the
# threshold has to be inside something the id is taken over.  ``contracts.py``
# imports every name below and defines none of them, exactly as it already does for
# the vocabularies, and the built body carries :data:`WORD_LIMITS` and the digest of
# :data:`SCHEMAS`.

#: The five model roles.  ``decider`` is absent on purpose: it is a program (§2.3).
ROLE_NAMES: Final[tuple[str, ...]] = ("critic", "defender", "judge", "marker", "variator")

#: The criticism constituents of FW5:609, which a critic must bind by name.
ROLE_BINDING_FIELDS: Final[tuple[str, ...]] = ("target", "defect", "grounds", "bearing")

#: §2.3's prose bounds, as ``(role, field) -> maximum whitespace-separated words``.
#: A bound on how much a seat may write - a declared resource bound, never a measure
#: of a reading: exceeding it blocks the output with ``blocked:schema`` and registers
#: nothing, and nothing anywhere compares two outputs' lengths.
WORD_LIMITS: Final[Mapping[tuple[str, str], int]] = MappingProxyType({
    ("critic", "case"): 400,
    ("defender", "answer"): 400,
    ("judge", "reading_note"): 120,
    ("marker", "case"): 120,
})

_DRAFT: Final[str] = "https://json-schema.org/draft/2020-12/schema"


def _text_schema(*, min_length: int = 0) -> dict[str, Any]:
    schema: dict[str, Any] = {"type": "string"}
    if min_length:
        schema["minLength"] = min_length
    return schema


CRITIC_SCHEMA: Final[dict[str, Any]] = {
    "$schema": _DRAFT,
    "title": "loop.critic.v1",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "relation", "passage_quote", "role_bindings", "case",
        OUTSIDE_VOCABULARY_FIELD,
    ],
    "properties": {
        "relation": {"type": "string", "enum": list(CRITIC_RELATIONS)},
        "passage_quote": _text_schema(),
        "role_bindings": {
            "type": "object",
            "additionalProperties": False,
            "required": list(ROLE_BINDING_FIELDS),
            "properties": {field: _text_schema() for field in ROLE_BINDING_FIELDS},
        },
        "case": _text_schema(),
        OUTSIDE_VOCABULARY_FIELD: _text_schema(),
    },
}

DEFENDER_SCHEMA: Final[dict[str, Any]] = {
    "$schema": _DRAFT,
    "title": "loop.defender.v1",
    "type": "object",
    "additionalProperties": False,
    "required": ["answer", "concedes"],
    "properties": {
        "answer": _text_schema(min_length=1),
        "concedes": {"type": "boolean"},
    },
}

JUDGE_SCHEMA: Final[dict[str, Any]] = {
    "$schema": _DRAFT,
    "title": "loop.judge.v1",
    "type": "object",
    "additionalProperties": False,
    "required": ["sustained", "decisive_point", "reading_note"],
    "properties": {
        "sustained": {"type": "boolean"},
        "decisive_point": _text_schema(min_length=1),
        "reading_note": _text_schema(),
    },
}

MARKER_SCHEMA: Final[dict[str, Any]] = {
    "$schema": _DRAFT,
    "title": "loop.marker.v1",
    "type": "object",
    "additionalProperties": False,
    "required": ["mark", "difference_kind", "left_quote", "right_quote", "case"],
    "properties": {
        "mark": {"type": "string", "enum": list(MARKS)},
        "difference_kind": {
            "type": ["string", "null"],
            "enum": [*ALL_DIFFERENCE_KINDS, None],
        },
        "left_quote": _text_schema(),
        "right_quote": _text_schema(),
        "case": _text_schema(),
    },
}

VARIATOR_SCHEMA: Final[dict[str, Any]] = {
    "$schema": _DRAFT,
    "title": "loop.variator.v1",
    "type": "object",
    "additionalProperties": False,
    "required": ["paraphrases"],
    "properties": {
        "paraphrases": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": _text_schema(min_length=1),
        },
    },
}

#: The five §2.3 schemas.  ``contracts.SCHEMAS`` is this object.
SCHEMAS: Final[Mapping[str, dict[str, Any]]] = MappingProxyType({
    "critic": CRITIC_SCHEMA,
    "defender": DEFENDER_SCHEMA,
    "judge": JUDGE_SCHEMA,
    "marker": MARKER_SCHEMA,
    "variator": VARIATOR_SCHEMA,
})


def _role_contracts_section() -> dict[str, Any]:
    """The §2.3 contracts as the pinned body carries them.

    The schemas ride as a **digest**, not as their own JSON: a schema carries
    ``minLength`` and ``minItems`` integers that are neither a guard parameter nor a
    word bound, and the body's own oracle - every integer in it is a declared bound -
    is worth more than having the schemas legible twice.  Editing any byte of any
    schema still changes the digest, and therefore :data:`STANDARD_BODY_SHA256`.
    """

    limits: dict[str, dict[str, int]] = {}
    for (role, field), limit in sorted(WORD_LIMITS.items()):
        limits.setdefault(role, {})[field] = limit
    return {
        "roles": list(ROLE_NAMES),
        "role_binding_fields": list(ROLE_BINDING_FIELDS),
        "schemas_sha256": sha256_hex(canonical_json({
            role: SCHEMAS[role] for role in sorted(SCHEMAS)
        })),
        "word_limits": limits,
        "word_limits_read": (
            "A bound on how much a seat may write. Exceeding it blocks the output with "
            "`blocked:schema` and registers nothing; no two outputs' lengths are ever "
            "compared, and a length is never a reading."
        ),
    }


#: The digest of the five §2.3 schemas, as the pinned body carries it.
ROLE_SCHEMAS_SHA256: Final[str] = _role_contracts_section()["schemas_sha256"]


# ------------------------------------------------------------------- falsifiers

@dataclass(frozen=True)
class Falsifier:
    """One entry of PLAN §8a's register-to-falsifier mapping."""

    id: str
    comparison: tuple[str, str]
    carrying_registers: tuple[str, ...]
    excluded_registers: tuple[str, ...]
    rule: str
    exclusion_reason: str

    def carries(self, register: str) -> bool:
        """Whether a difference on ``register`` can fire this falsifier."""
        return register in self.carrying_registers

    def as_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "comparison": list(self.comparison),
            "carrying_registers": list(self.carrying_registers),
            "excluded_registers": list(self.excluded_registers),
            "rule": self.rule,
            "exclusion_reason": self.exclusion_reason,
        }


_MATERIAL_FALSIFIERS: Final[Mapping[str, str]] = dict(
    PLAN_8A_MIRROR["material_register_to_falsifier"]
)

_G_EXCLUDED: Final[str] = (
    "`G` alone does not carry D1, since the control has no objection grounds to cite and "
    "a `G` difference there is forced by the design."
)

_F_EXCLUDED: Final[str] = (
    "PLAN §8a names only T, E or D as firing this falsifier; a `G` difference alone "
    "does not fire it."
)

#: D1, F2 and F3 with the registers that can carry them.  G is excluded from all three:
#: G alone never carries D1, and F2/F3 fire only on T, E or D.
FALSIFIER_MAP: Final[Mapping[str, Falsifier]] = MappingProxyType({
    "D1": Falsifier(
        id="D1",
        comparison=("ORIGINAL", "CONTROL"),
        carrying_registers=("T", "E", "D"),
        excluded_registers=("G",),
        rule=_MATERIAL_FALSIFIERS["D1"],
        exclusion_reason=_G_EXCLUDED,
    ),
    "F2": Falsifier(
        id="F2",
        comparison=("ORIGINAL", "RECODING"),
        carrying_registers=("T", "E", "D"),
        excluded_registers=("G",),
        rule=_MATERIAL_FALSIFIERS["F2"],
        exclusion_reason=_F_EXCLUDED,
    ),
    "F3": Falsifier(
        id="F3",
        comparison=("ORIGINAL", "CARRIER"),
        carrying_registers=("T", "E", "D"),
        excluded_registers=("G",),
        rule=_MATERIAL_FALSIFIERS["F3"],
        exclusion_reason=_F_EXCLUDED,
    ),
})


# -------------------------------------------------------------- guard parameters

#: The pre-registered reasons a cell whose prior outcome was `unresolved` may be re-read
#: at all (design §2.4 G11).  Anything else is refused at the write.
REOPEN_REASONS: Final[tuple[str, ...]] = (
    "new-material",
    "repaired-guard",
    "appellate-ruling",
)

#: G5, worded for **every** admissible panel.  ``judge_seats`` may be raised by a
#: successor standard (:data:`_INT_PARAMS`), and a rule that said "Both judge seats"
#: would then ship a sentence describing two seats to a panel of three - whose natural
#: repair is a majority, the one thing G5 forbids.  No numeral, no "both": the rule
#: reads the same whatever the panel size, and unanimity is unanimity.
_UNANIMITY_RULE: Final[str] = (
    "Every judge seat must return the same `sustained` value. A split blocks the cell "
    "with reason `ensemble-split`, records every ruling verbatim, and is never averaged "
    "and never settled by majority vote (FW5:634)."
)

#: The guard parameters the standard freezes (design §2.1).  ``order_swap_both_orders``
#: and ``min_resolved_replicates_per_case`` are added to §2.1's list because §2.4 states
#: them numerically and a guard parameter that is not in the pinned standard cannot be
#: attacked by attacking the standard.
GUARD_PARAMETERS: Final[Mapping[str, Any]] = MappingProxyType({
    "critic_seats": 1,
    "defender_seats": 1,
    "judge_seats": 2,
    "variator_seats": 1,
    "marker_reuses_judge_seats": True,
    "min_judge_families": 2,
    "paraphrase_n": 2,
    "schema_repair_budget": 0,
    "order_swap_both_orders": True,
    "min_resolved_replicates_per_case": 3,
    "unanimity_rule": _UNANIMITY_RULE,
    "reopen_reasons": REOPEN_REASONS,
})

GUARD_PARAMETER_KEYS: Final[frozenset[str]] = frozenset(GUARD_PARAMETERS)

_INT_PARAMS: Final[Mapping[str, tuple[int, int]]] = {
    "critic_seats": (1, 8),
    "defender_seats": (1, 8),
    "judge_seats": (2, 8),
    "variator_seats": (1, 8),
    "min_judge_families": (2, 8),
    "paraphrase_n": (1, 8),
    # Literally equal to types.SeatsConfig's range for the same parameter: the
    # budget is 0 in this run, and a raised budget is a successor standard with a
    # new loop_plan_id, never a config that turns schema repair on.
    "schema_repair_budget": (0, 0),
    "min_resolved_replicates_per_case": (3, 16),
}

_BOOL_PARAMS: Final[tuple[str, ...]] = (
    "marker_reuses_judge_seats",
    "order_swap_both_orders",
)

#: The ``seats`` keys a loop config and this standard both declare, and the guard
#: parameter each one must equal.  ``judges`` is handled separately: it names seats
#: rather than counting them.
_SEATS_TO_GUARD: Final[Mapping[str, str]] = MappingProxyType({
    "min_judge_families": "min_judge_families",
    "paraphrase_n": "paraphrase_n",
    "schema_repair_budget": "schema_repair_budget",
})


def assert_config_matches_standard(seats_mapping: Mapping[str, Any] | None,
                                   reopen_reasons: Sequence[str] | None,
                                   where: str = "config",
                                   *,
                                   guard_parameters: Mapping[str, Any] | None = None
                                   ) -> None:
    """Refuse a loop config that contradicts the guard parameters this standard freezes.

    Two owners declare the same guard values: ``types.SeatsConfig`` (what the operator
    wrote) and :data:`GUARD_PARAMETERS` (what the pinned standard says).  Both are folded
    into ``loop_plan_id``, so a disagreement between them is *frozen* rather than caught,
    and a later wave has to guess which owner wins.  This is the reconciliation that
    settles it: the standard wins, and a config that differs is refused before the first
    call rather than published as a pre-registration the run does not honour.

    **PREFLIGHT must call this** (W5), and must pass ``guard_parameters=`` from the body
    it actually registered: ``standard_body(registered)["guard_parameters"]``.  Left out,
    the comparison is against this module's own :data:`GUARD_PARAMETERS`, which is the
    right answer only while the registered body is this module's - and the failure when
    it is not runs both ways: a config that *matches* the registered standard is refused,
    and a config that *contradicts* it is admitted.  The default is kept so the existing
    two-argument call still binds.

    It takes plain data - a ``seats`` mapping (``SeatsConfig.as_dict()`` or the raw config
    block), the config's ``reopen_reasons``, and the registered body's guard parameters -
    because :mod:`minireason.loop.types` may import no sibling and this module may not
    import it.

    Raises :class:`StandardInvalid` with ``GUARD_PARAMETER_INVALID`` for a seat parameter
    that differs from the standard's, and ``REOPEN_REASON_UNKNOWN`` for a reopen reason
    outside :data:`REOPEN_REASONS` (G11: the reopen list "is the only mechanical defence
    against retrying until something sticks", so a run may narrow it and may not widen
    it).  ``None`` for either argument means "the config declares none", which is the
    module default and reconciles.
    """

    mapping = {} if seats_mapping is None else seats_mapping
    frozen_params = GUARD_PARAMETERS if guard_parameters is None else guard_parameters
    if not isinstance(frozen_params, Mapping):
        raise StandardInvalid("GUARD_PARAMETER_INVALID",
                              f"guard_parameters must be an object, not "
                              f"{type(frozen_params).__name__}")
    needed = set(_SEATS_TO_GUARD.values()) | {"judge_seats"}
    absent = sorted(needed - set(frozen_params))
    if absent:
        raise StandardInvalid("GUARD_PARAMETER_MISSING", str(absent))
    if not isinstance(mapping, Mapping):
        raise StandardInvalid("GUARD_PARAMETER_INVALID",
                              f"{where}.seats must be an object, not "
                              f"{type(mapping).__name__}")
    for key, parameter in _SEATS_TO_GUARD.items():
        if key not in mapping:
            continue
        declared, frozen = mapping[key], frozen_params[parameter]
        if declared != frozen:
            raise StandardInvalid(
                "GUARD_PARAMETER_INVALID",
                f"{where}.seats.{key}={declared!r} contradicts the pinned standard's "
                f"{parameter}={frozen!r}; a successor standard is a new loop_plan_id, "
                "never a config override",
            )
    judges = tuple(mapping.get("judges") or ())
    if judges and len(judges) != frozen_params["judge_seats"]:
        raise StandardInvalid(
            "GUARD_PARAMETER_INVALID",
            f"{where}.seats.judges names {len(judges)} seats and the pinned standard "
            f"freezes judge_seats={frozen_params['judge_seats']!r}",
        )
    listed = tuple(frozen_params.get("reopen_reasons") or REOPEN_REASONS)
    unlisted = [reason for reason in (reopen_reasons or ()) if reason not in listed]
    if unlisted:
        raise StandardInvalid(
            "REOPEN_REASON_UNKNOWN",
            f"{where}.reopen_reasons carries {unlisted!r}, which the pinned standard "
            f"does not list: {list(listed)}",
        )


# ------------------------------------------------------------ calibration anchors

@dataclass(frozen=True)
class CalibrationAnchor:
    """One anchor of the planted-flaw calibration set (design §2.5).

    ``expected_relation`` is ``None`` where the construction establishes that no relation
    from the vocabulary holds.  ``must_sustain`` is what a sound seat does with it; a
    clean control is an anchor a seat must *not* sustain.
    """

    id: str
    construction: str
    expected_relation: str | None
    must_sustain: bool
    ground_truth_reason: str

    def as_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "construction": self.construction,
            "expected_relation": self.expected_relation,
            "must_sustain": self.must_sustain,
            "ground_truth_reason": self.ground_truth_reason,
        }


#: Ground truth true by construction, plus clean controls that must not sustain.
CALIBRATION_ANCHORS: Final[tuple[CalibrationAnchor, ...]] = (
    CalibrationAnchor(
        id="self-juxtaposition",
        construction=(
            "A row read against itself, built with the referring region alone: the "
            "row carries a referring record and declares no target record, and the "
            "relation asked about is the record's relation to its own content. The "
            "record's bytes therefore appear in the resolvable surface exactly "
            "once, and a quote of any span of it resolves uniquely inside a "
            "declared region."
        ),
        expected_relation="retains",
        must_sustain=True,
        ground_truth_reason=(
            "A record retains its own content by construction; the ground truth is a "
            "property of how the anchor was built, not a reading of it. It is built "
            "with the referring region alone because a surface carrying the same "
            "bytes twice has no uniquely resolving quote at all: every substring "
            "occurs twice, G2(a) blocks every window for every seat, and an anchor "
            "that can never sustain would charge the panel an error it did not make "
            "(REVIEW-WAVE1 B3, REVIEW-PREREG PR-06). W1-SURFACE's own rule makes "
            "the construction available: a region the row does not carry is absent, "
            "not empty."
        ),
    ),
    CalibrationAnchor(
        id="no-shared-reference",
        construction=(
            "Two records drawn from documents with no reference, no quotation and no "
            "shared distinctive token between them."
        ),
        expected_relation=None,
        must_sustain=False,
        ground_truth_reason=(
            "Nothing in either record can bind a role in the other, so no relation from "
            "the vocabulary is established and the critic's answer is `none`."
        ),
    ),
    CalibrationAnchor(
        id="quotes-and-rejects",
        construction=(
            "A record that quotes the target record verbatim and states a ground for "
            "declining it."
        ),
        expected_relation="rejects-with-reason",
        must_sustain=True,
        ground_truth_reason=(
            "The quotation supplies the passage and the stated ground supplies the "
            "reason, both by construction."
        ),
    ),
    CalibrationAnchor(
        id="clean-control-lexical-overlap-only",
        construction=(
            "Two records sharing distinctive vocabulary, with no reference, no quotation "
            "and no preserved role binding between them."
        ),
        expected_relation=None,
        must_sustain=False,
        ground_truth_reason=(
            "A lexical overlap is not evidence of use (FW5:628, FW5:640); a seat that "
            "sustains a relation here is reading the overlap, not the material."
        ),
    ),
    CalibrationAnchor(
        id="clean-control-framing-only-passage",
        construction=(
            "A pair whose only candidate passage lies in the pack's framing - the "
            "banner, the vocabulary list or the resolver notes - and not in the "
            "referring record, the target record or a listed body passage."
        ),
        expected_relation=None,
        must_sustain=False,
        ground_truth_reason=(
            "A reading grounded in the prompt's own scaffolding is not a reading of the "
            "material; the guard must decline it on the operative-target check."
        ),
    ),
)


# ------------------------------------------------------------------ build / parse

def _validate_registers(registers: Mapping[str, Register]) -> None:
    if set(registers) != set(REGISTER_IDS):
        raise StandardInvalid(
            "REGISTER_SET_MISMATCH",
            f"expected {sorted(REGISTER_IDS)}, got {sorted(registers)}",
        )
    for rid in REGISTER_IDS:
        register = registers[rid]
        if not isinstance(register, Register):
            raise StandardInvalid("REGISTER_SET_MISMATCH", f"{rid} is not a Register")
        if register.id != rid:
            raise StandardInvalid("REGISTER_SET_MISMATCH", f"{rid} carries id {register.id!r}")
        if not register.plan_text.strip():
            raise StandardInvalid("REGISTER_TEXT_EMPTY", rid)
        if not register.difference_kinds:
            raise StandardInvalid("DIFFERENCE_KIND_SET_EMPTY", rid)
        tokens = register.kind_tokens
        if len(set(tokens)) != len(tokens):
            raise StandardInvalid("DIFFERENCE_KIND_DUPLICATE", rid)


def _validate_vocabulary(vocabulary: Sequence[str]) -> None:
    values = tuple(vocabulary)
    if not values:
        raise StandardInvalid("VOCABULARY_EMPTY", "")
    if len(set(values)) != len(values):
        raise StandardInvalid("VOCABULARY_DUPLICATE", str(values))
    outside = [value for value in values if value not in READING_VOCABULARY]
    if outside:
        raise StandardInvalid("VOCABULARY_NOT_CLOSED", str(outside))
    if UNRESOLVED_TOKEN not in values:
        raise StandardInvalid("UNRESOLVED_NOT_IN_VOCABULARY", str(values))


def _validate_params(params: Mapping[str, Any]) -> None:
    unknown = sorted(set(params) - GUARD_PARAMETER_KEYS)
    if unknown:
        raise StandardInvalid("GUARD_PARAMETER_UNKNOWN", str(unknown))
    missing = sorted(GUARD_PARAMETER_KEYS - set(params))
    if missing:
        raise StandardInvalid("GUARD_PARAMETER_MISSING", str(missing))
    for key, (low, high) in _INT_PARAMS.items():
        value = params[key]
        if isinstance(value, bool) or not isinstance(value, int):
            raise StandardInvalid("GUARD_PARAMETER_INVALID", f"{key} is not an integer")
        if not low <= value <= high:
            raise StandardInvalid(
                "GUARD_PARAMETER_INVALID", f"{key}={value} outside [{low},{high}]"
            )
    for key in _BOOL_PARAMS:
        if not isinstance(params[key], bool):
            raise StandardInvalid("GUARD_PARAMETER_INVALID", f"{key} is not a boolean")
    if not str(params["unanimity_rule"]).strip():
        raise StandardInvalid("GUARD_PARAMETER_INVALID", "unanimity_rule is empty")
    reasons = tuple(params["reopen_reasons"])
    if not reasons:
        raise StandardInvalid("REOPEN_REASON_SET_EMPTY", "")
    unlisted = [reason for reason in reasons if reason not in REOPEN_REASONS]
    if unlisted:
        raise StandardInvalid("REOPEN_REASON_UNKNOWN", str(unlisted))


def _refuse_successor_argument(name: str, given: Any, default: Any) -> None:
    """Refuse an argument that is not the module's own frozen default.

    See :func:`build_standard` for why a successor standard is a source edit.
    ``None`` means "the default"; a value equal to the default is the default
    spelled out, and is accepted so a caller may be explicit.
    """

    if given is None:
        return
    if isinstance(default, Mapping):
        same = isinstance(given, Mapping) and dict(given) == dict(default)
    else:
        same = (not isinstance(given, (str, bytes))
                and isinstance(given, Sequence) and tuple(given) == tuple(default))
    if not same:
        raise StandardInvalid(
            "STANDARD_ARGUMENT_REFUSED",
            f"build_standard({name}=...) would mint a successor standard; a successor "
            "is a source edit and a new digest, never a call",
        )


def build_standard(
    registers: Mapping[str, Register] | None = None,
    vocabulary: Sequence[str] | None = None,
    params: Mapping[str, Any] | None = None,
) -> bytes:
    """Assemble the standard artifact body as canonical JSON bytes.

    Pure and byte-stable: two builds return identical bytes, and the bytes are what
    :data:`STANDARD_BODY_SHA256` addresses, so a plan pins the body by digest.

    **The three arguments may name only the module's own defaults.**  They are kept so
    the signature a caller imported still binds, and so a caller may say explicitly which
    standard it means; anything else is ``STANDARD_ARGUMENT_REFUSED``.  The reason is
    that this function never honoured them: a narrowed vocabulary reached
    ``body["vocabulary"]`` while the rubric's own ``values`` kept the six, a narrowed
    reopen list reached ``guard_parameters.reopen_reasons`` while the top-level
    ``reopen_reasons`` kept the wide one, and added difference kinds reached
    ``registers`` while ``role_contracts.schemas_sha256`` still addressed the shipped
    ``MARKER_SCHEMA``.  Every one of those bodies contradicted itself, and a
    self-contradicting standard is worse than no successor at all.  A successor standard
    is a **source edit** - new constants, new digest, new ``loop_plan_id`` - which is
    what §5 means by "changing any threshold after first look mints a new plan".

    Raises :class:`StandardInvalid` with a declared ``code``: ``STANDARD_ARGUMENT_REFUSED``
    for a non-default argument, and - over its own frozen defaults, which a source edit
    can break - a register set that is not the four PLAN §8a registers, a vocabulary not
    closed under the six published values or lacking ``unresolved``, an unknown, missing
    or out-of-range guard parameter, an unlisted reopen reason, or a scoring key anywhere
    in the result.
    """
    _refuse_successor_argument("registers", registers, PLAN_8A_REGISTERS)
    _refuse_successor_argument("vocabulary", vocabulary, READING_VOCABULARY)
    _refuse_successor_argument("params", params, GUARD_PARAMETERS)

    registers = PLAN_8A_REGISTERS
    vocabulary = READING_VOCABULARY
    params = GUARD_PARAMETERS

    _validate_registers(registers)
    _validate_vocabulary(vocabulary)
    _validate_params(params)

    values = tuple(vocabulary)
    body: dict[str, Any] = {
        "schema": STANDARD_SCHEMA,
        "spec_id": SPEC_ID,
        "standard_name": STANDARD_NAME,
        "commitment_eval": RUBRIC_EVAL,
        "commitment_reads": COMMITMENT_READS,
        "modes": list(MODES),
        "rubric": {cid: rubric.as_json() for cid, rubric in sorted(RUBRIC_V1.items())},
        "vocabulary": {
            "closed": True,
            "values": list(values),
            "nominable_relations": [v for v in values if v != UNRESOLVED_TOKEN],
            "none_token": NONE_TOKEN,
            "published_note": VOCABULARY_NOTE,
            "outside_vocabulary_field": OUTSIDE_VOCABULARY_FIELD,
            "outside_vocabulary_effect": OUTSIDE_VOCABULARY_EFFECT,
            "instrument_banner": READING_BANNER,
        },
        "marks": list(MARKS),
        "registers": {rid: registers[rid].as_json() for rid in REGISTER_IDS},
        "plan_8a": {
            "source": dict(PLAN_8A_MIRROR["source"]),
            "preamble": PLAN_8A_MIRROR["preamble"],
            "replicate_baseline": PLAN_8A_MIRROR["replicate_baseline"],
            "order_of_reading": PLAN_8A_MIRROR["order_of_reading"],
            "register_to_falsifier": PLAN_8A_MIRROR["register_to_falsifier"],
            "two_readers": PLAN_8A_MIRROR["two_readers"],
            "never_aggregated": PLAN_8A_MIRROR["never_aggregated"],
        },
        "falsifiers": {
            fid: falsifier.as_json() for fid, falsifier in sorted(FALSIFIER_MAP.items())
        },
        "guard_parameters": {
            key: (list(value) if isinstance(value, tuple) else value)
            for key, value in sorted(params.items())
        },
        "reopen_reasons": list(REOPEN_REASONS),
        "role_contracts": _role_contracts_section(),
        "calibration_anchors": [anchor.as_json() for anchor in CALIBRATION_ANCHORS],
        "ceiling": {
            "sha256": CEILING_SHA256,
            "path": CEILING_PATH.name,
            "claim_template": CEILING_CLAIM_TEMPLATE,
            "required_sentences": list(CEILING_REQUIRED_SENTENCES),
        },
    }
    _refuse_forbidden_keys(body)
    return canonical_json(body)


def standard_body(raw: bytes | str) -> dict[str, Any]:
    """Parse a serialised standard body and refuse anything that is not one.

    Accepts the bytes :func:`build_standard` emits, or the same text.  Raises
    :class:`StandardInvalid` for malformed JSON, a non-object body, a schema or spec-id
    that is not this standard's, a missing top-level section, or a scoring key nested
    anywhere.  The returned value is a plain ``dict`` and is not shared with the module's
    own frozen data.
    """
    text = raw.decode("utf-8") if isinstance(raw, (bytes, bytearray)) else raw
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        raise StandardInvalid("STANDARD_BODY_MALFORMED", str(exc)) from exc
    if not isinstance(parsed, dict):
        raise StandardInvalid("STANDARD_BODY_MALFORMED", type(parsed).__name__)
    if parsed.get("schema") != STANDARD_SCHEMA:
        raise StandardInvalid("STANDARD_SCHEMA_MISMATCH", repr(parsed.get("schema")))
    if parsed.get("spec_id") != SPEC_ID:
        raise StandardInvalid("SPEC_ID_MISMATCH", repr(parsed.get("spec_id")))
    required = (
        "calibration_anchors", "ceiling", "commitment_eval", "commitment_reads",
        "falsifiers", "guard_parameters", "marks", "modes", "plan_8a", "registers",
        "reopen_reasons", "role_contracts", "rubric", "standard_name", "vocabulary",
    )
    missing = [key for key in required if key not in parsed]
    if missing:
        raise StandardInvalid("STANDARD_SECTION_MISSING", str(missing))
    _refuse_forbidden_keys(parsed)
    _validate_body_shapes(parsed)
    return parsed


def _validate_body_shapes(parsed: Mapping[str, Any]) -> None:
    """Re-run the three validators over a parsed body's own shapes.

    :func:`build_standard` checks its inputs; this checks a body that arrived
    from somewhere else.  Without it, every body :func:`build_standard` refuses
    was admitted here - a body naming three registers, a vocabulary without
    ``unresolved``, a ``judge_seats`` of 1 - and PREFLIGHT would register it.

    It also asserts the one internal agreement a body can break on its own: the
    top-level ``reopen_reasons`` and ``guard_parameters.reopen_reasons`` are two
    renderings of one list (G11's "the only mechanical defence against retrying
    until something sticks"), and a body carrying two different lists does not
    say what would reopen the question.
    """

    registers = parsed["registers"]
    if not isinstance(registers, Mapping) or set(registers) != set(REGISTER_IDS):
        raise StandardInvalid(
            "REGISTER_SET_MISMATCH",
            f"expected {sorted(REGISTER_IDS)}, got "
            f"{sorted(registers) if isinstance(registers, Mapping) else type(registers).__name__}")
    for rid in REGISTER_IDS:
        block = registers[rid]
        if not isinstance(block, Mapping):
            raise StandardInvalid("REGISTER_SET_MISMATCH", f"{rid} is not an object")
        if block.get("id") != rid:
            raise StandardInvalid("REGISTER_SET_MISMATCH",
                                  f"{rid} carries id {block.get('id')!r}")
        if not str(block.get("plan_text", "")).strip():
            raise StandardInvalid("REGISTER_TEXT_EMPTY", rid)
        kinds = block.get("difference_kinds") or ()
        if not kinds:
            raise StandardInvalid("DIFFERENCE_KIND_SET_EMPTY", rid)
        tokens = [kind.get("token") if isinstance(kind, Mapping) else kind
                  for kind in kinds]
        if len(set(tokens)) != len(tokens):
            raise StandardInvalid("DIFFERENCE_KIND_DUPLICATE", rid)
    vocabulary = parsed["vocabulary"]
    if not isinstance(vocabulary, Mapping):
        raise StandardInvalid("VOCABULARY_EMPTY", type(vocabulary).__name__)
    _validate_vocabulary(vocabulary.get("values") or ())
    params = parsed["guard_parameters"]
    if not isinstance(params, Mapping):
        raise StandardInvalid("GUARD_PARAMETER_INVALID", type(params).__name__)
    _validate_params(params)
    top_level = tuple(parsed.get("reopen_reasons") or ())
    inner = tuple(params.get("reopen_reasons") or ())
    if top_level != inner:
        raise StandardInvalid(
            "REOPEN_REASON_UNKNOWN",
            f"the body's two reopen lists disagree: {list(top_level)} at the top "
            f"level, {list(inner)} under guard_parameters")


#: The standard body the loop registers, and the digest a plan pins.
STANDARD_BODY: Final[bytes] = build_standard()
STANDARD_BODY_SHA256: Final[str] = sha256_hex(STANDARD_BODY)
