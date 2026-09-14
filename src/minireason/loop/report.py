"""W3-REPORT: the run's rendered record - READING_TABLE, COMPARISON, CYCLE, CLOSING.

Purpose
-------
The four documents a run prints, each a pure function onto Markdown text:
``render_reading_table(harness, plan)`` for ``READING_TABLE.md`` (the whole
use-relation table in the unread / unresolved / machine-unresolved trichotomy),
``render_comparison(harness, plan)`` for ``COMPARISON.md`` (the C001 registers,
marked separately and never combined), ``render_cycle(decision, state)`` for one
cycle's ``CYCLE.md``, and ``render_closing(run)`` for ``CLOSING.md`` (the run's
closing record: the frozen ceiling block, the block register by reason code with
counts, the audit record in force, the stopping sentence, ``losses_outside_P``,
the INDETERMINATE list, and the appellate declaration).

Design §6: the renderer **refuses to emit any table or report without the frozen
ceiling at its pinned sha**, and the refusal is the custody vocabulary's own:
the plan's pin map must name the ceiling data file at
:data:`standard.CEILING_SHA256` (absent is ``SOURCE_PIN_MISSING``, shifted is
``SOURCE_PIN_MISMATCH``, both :class:`custody.CustodyMismatch`, both already
members of ``types.FAILURE_CODES``), and a supplied ceiling *text* that digests
otherwise is refused by :class:`standard.StandardInvalid`
(``STANDARD_DATA_MALFORMED``) - a record built over bytes nobody pinned is a
malformed ceiling, and a pin that moved is a custody fact rather than a report's
private refusal.  Every required ceiling sentence
(:data:`standard.CEILING_REQUIRED_SENTENCES`, imported, never retyped) appears
verbatim on every rendered table and on the closing record, each as its own
plain paragraph: a renderer that re-wraps or blockquotes would make "verbatim"
mean "by normalisation", and the checks here read the plain string.

What a rendered artifact never contains
---------------------------------------
No score, no rank, no average, no majority, no percentage, no progress meter,
and no combined register: the four registers are four columns of a table header
and four cells of a row, and no field anywhere holds two registers' marks as one
value.  The only quantities in any artifact are the block register's counts -
which the frozen ceiling itself demands ("printed with counts on every table") -
plus ``appellate_rulings: N``, where N names the tuple the graph holds.  Every
rendered byte passes :func:`standard.assert_no_scoring_headers`,
``contracts.assert_no_scoring_keys`` over the record structure, and
:func:`standard.assert_no_exhaustion_claim`: a reached ceiling is a declared
resource boundary, and a renderer that said otherwise is refused here rather
than downstream.

A run whose every reading was blocked renders as **declined-to-read**, never as
"no relations found": the block register is an account of the instrument, and
the ceiling's block-register clause forbids converting it into a claim about the
material.  The three cell states print as three things, in
:data:`TRICHOTOMY_WORDS`, derived from the ceiling's own sixth clause at import
rather than composed here.

Deviations from the design entry, and why
-----------------------------------------
1. **The two published constants are re-exports, not definitions.**  The wave
   plan publishes ``CEILING_REQUIRED_SENTENCES`` and ``BLOCK_REGISTER_HEADINGS``
   on this module; ``standard``'s own "Ownership after wave-0 integration"
   paragraph already declares W3-REPORT *imports* ``CEILING_REQUIRED_SENTENCES``
   from W0-STANDARD, so the name here ``is`` that object, and
   ``BLOCK_REGISTER_HEADINGS`` is built from ``types.CEILING_BLOCK_REASONS`` -
   the ceiling's own nine spellings in the ceiling's own order - rather than
   retyped.  ``__all__`` carries both so a caller does not change.
2. **``plan`` is the plan body, not a plan object.**  A mapping carrying the
   ``pins`` map of design 4.2 (or a declared :class:`ReportPlan`) is read the
   same way ``custody.verify_pins`` reads one, so rendering and custody answer
   from one record.  A plan whose body carries no pins map, and a ``Decision``
   offered as the run's stopping record while the chain is open, are refused
   with the standard's own ``STANDARD_DATA_MALFORMED`` / the decide module's
   ``DECISION_…`` vocabulary is *not* raised here: an open chain at CLOSE is
   refused as an invalid report input rather than renamed.
3. **``render_cycle``'s ``state`` is a declared record** (:class:`CycleState`),
   not a live database.  W1-GRAPH holds no block register (a blocked trial
   registers nothing), so the cycle's blocks, unread rows and indeterminate
   coordinates reach the report as data the caller already has - W4-READER's
   ``Readings.blocks``, W3-TRIAL's block lists, ``steps.scan_coordinates``'s
   ``indeterminate``.  A report that re-mined the step ledger would be a second
   reader of every coordinate; it renders what it is given and refuses what it
   is not.
4. **The same for ``render_closing(run)``** - :class:`ClosingRun` - with the
   decision record mandatory, because the closing record prints the stopping
   sentence and inventing one would be retyping W2-DECIDE's sentences.  An open
   chain is refused rather than rendered as if closed.
5. **``custody`` and the ``CUSTODY``/``STANDARD_DATA`` code names are used
   although the wave plan's ``depends_on`` names only W0-CONTRACTS, W1-GRAPH and
   W2-DECIDE.**  The wave-2 code frontier is empty: a wave-3 module declares no
   new failure codes, and a ceiling refusal is exactly the fact a custody code
   already names, so it rides that table rather than a private one.  The edge
   ``report -> custody`` joins the two custody consumers that already exist;
   ``tests/loop/test_report.py``'s import-graph test is where the edge is
   recorded.

6. **``render_reading_table`` and ``render_comparison`` take a keyword-only
   ``state``, and it is the same deviation as 3.**  A blocked trial registers
   nothing, so no block is readable from the harness; the draft built an empty
   block list inside ``render_reading_table`` and never filled it, and the
   table therefore printed ``x0`` against every reason on a run that had been
   entirely blocked, with an always-empty machine-unresolved section under it.
   The wave plan's two-argument call still renders, so a caller written to the
   declared signature is not broken - it gets a table whose block register is
   honestly empty, which is the right answer only where there are no blocks.

7. **Three ways of reading nothing, and they are three facts.**
   ``_declined_to_read`` prints the declined sentence for a run with blocks and
   no reading, and for a table with no cells at all - never for a run whose
   cells were *deliberately read* and stayed at the grounded default. The draft
   claimed "every reading cell was blocked" over that third run.

8. **Two framing sentences are re-exported from W2-DECIDE, not written here.**
   ``PROTECTED_LOSS_SENTENCE`` and ``LOSSES_OUTSIDE_P_SENTENCE`` are
   ``decide.PROTECTED_LOSS_SENTENCE`` and ``decide.NET_WITHDRAWAL_SENTENCE``.
   The draft wrote a paraphrase of each, which would have put two different
   statements of one rule in one paragraph beside
   ``decision.record_sentences``' own. And the ceiling's pin key is
   ``standard.CEILING_PIN_KEY``, imported: the draft rebuilt it out of
   ``types.PINNED_SOURCE_PATHS[0].split("/")[0]`` and a retyped path.

9. **Every stop prints ``would_reopen``, a protected loss included** (design 5:
   "Every stop carries a mandatory ``would_reopen`` prose field"). The draft
   printed the protected-loss sentence *instead of* the field.

:data:`NEW_CODES` is declared and **empty**, on purpose: this module raises
nothing ``types.FAILURE_CODES`` does not already name, and the wave-3 integrator
has nothing of this module's to fold in.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence, Tuple

from . import types as _t
from .contracts import assert_no_scoring_keys
from .custody import CustodyMismatch
from .decide import (
    NET_WITHDRAWAL_SENTENCE,
    PROTECTED_LOSS_SENTENCE,
    Decision,
)
from .graph import CellStanding
from .obligations import Loss
from .standard import (
    CEILING_PIN_KEY,
    CEILING_REQUIRED_SENTENCES,
    CEILING_SHA256,
    StandardInvalid,
    assert_no_exhaustion_claim,
    assert_no_scoring_headers,
)

__all__ = [
    "NEW_CODES",
    "ReportRefused",
    "CEILING_REQUIRED_SENTENCES",
    "BLOCK_REGISTER_HEADINGS",
    "DECLINED_TO_READ",
    "DECLINED_TO_READ_SENTENCE",
    "TRICHOTOMY_HEADING",
    "TRICHOTOMY_WORDS",
    "APPELLATE_HEADING",
    "APPELLATE_NOT_VALIDATED_SENTENCE",
    "INDETERMINATE_SENTENCE",
    "AUDIT_IN_FORCE_SENTENCE",
    "CELL_READ_SENTENCE",
    "CELL_UNREAD_SENTENCE",
    "CELL_UNRESOLVED_SENTENCE",
    "CELL_MACHINE_WORD",
    "CELL_CONTESTED_WORD",
    "CELL_ORPHANED_WORD",
    "NO_READING_SET",
    "EMPTY_LIST",
    "CEILING_HEADING",
    "CEILING_PRELUDE",
    "STOPPING_SENTENCE_HEADING",
    "CHAIN_OPEN_SENTENCE",
    "STOP_WORD",
    "CONTINUE_WORD",
    "NO_AUDIT_RECORDS",
    "NO_LOSSES_OUTSIDE_P",
    "LOSSES_OUTSIDE_P_SENTENCE",
    "PROTECTED_LOSS_SENTENCE",
    "UNREAD_SENTENCE",
    "STILL_TURNING_SENTENCE",
    "NO_INDETERMINATE_COORDINATES",
    "AUDIT_HEADER_CELLS",
    "UNRESOLVED_DEFAULT_WORD",
    "RegisterRow",
    "ReportPlan",
    "CycleState",
    "ClosingRun",
    "RENDERED_FILES_RECORD",
    "rendered_files_record",
    "ceiling_key_of",
    "block_line",
    "audit_line",
    "render_reading_table",
    "render_comparison",
    "render_cycle",
    "render_closing",
]


#: The record ``obligations.no_scoring_key`` (p4) and p12 read to find what the
#: run rendered, and the answer to WAVE2-INTERFACE open question 3: **this
#: module owns the shape**. ``files`` maps the artifact's path to its *rendered
#: bytes* - not a summary of them - because p4 tokenises headings and table
#: header rows out of the text itself. Every renderer here builds one over its
#: own output and runs the scoring-key guard across it before returning, so a
#: renderer cannot emit what the obligation would refuse; the driver registers
#: the run's whole map through W1-GRAPH.
RENDERED_FILES_RECORD = "rendered_files"


def rendered_files_record(files: Mapping[str, str]) -> dict[str, Any]:
    """The ``rendered_files`` record over ``{path: rendered text}``."""
    return {"record": RENDERED_FILES_RECORD,
            "files": {str(path): str(text) for path, text in files.items()}}


#: Every code this module can name that ``types.FAILURE_CODES`` does not
#: already carry, with its one-line reason.  There are none: the ceiling
#: refusal is custody's own, and every input refusal is a declared shape
#: violation the owning modules already name.  Declared (and asserted) so that
#: the wave-3 integrator's fold-in sweep has a table to read.
NEW_CODES: Mapping[str, str] = MappingProxyType({})


class ReportRefused(CustodyMismatch):
    """A declared refusal from the renderers.  ``code`` is the stable token.

    A :class:`~minireason.loop.custody.CustodyMismatch`, so one ``except``
    catches the ceiling refusal and every pin refusal beside it, and so the
    code a refused render carries is one a halt receipt can already spell.  The
    detail never changes the code.
    """

    def __init__(self, code: str, detail: str = "") -> None:
        CustodyMismatch.__init__(self, code, detail)


# --------------------------------------------------------------------------
# The block register: names and sentences
# --------------------------------------------------------------------------

#: The header row the renderer prints for the block register, and the closing
#: record's own row set.  Built from ``types.CEILING_BLOCK_REASONS`` - the
#: ceiling's own spelling and order - so the printed register is the one the
#: frozen ceiling promises, and ``blocked:constitution`` (G0, the one member of
#: ``types.BLOCK_CODES`` the ceiling does not name) is appended plain as the
#: register's own tenth row, where the pre-registration bundle must state that
#: a constitution block is reported (PR-12, disposition (b)).
BLOCK_REGISTER_HEADINGS: Tuple[str, ...] = (
    tuple(_t.CEILING_BLOCK_REASONS) + ("constitution",))

#: A run whose reading table holds nothing that was read is an instrument that
#: declined to read, and is printed as exactly that - never as an absence of
#: relations in the material.
DECLINED_TO_READ = "declined-to-read"

DECLINED_TO_READ_SENTENCE = (
    "This run's every reading cell was blocked, so it is reported as the "
    "instrument having declined to read; it is never an absence of relations."
)


def _trichotomy_words() -> Tuple[str, str, str]:
    """The three state words, read out of the frozen ceiling's sixth clause.

    Composed here would be a second spelling of a promise the ceiling already
    makes; read at import, a ceiling that stopped naming them fails loudly.
    """

    clause = next(sentence for sentence in CEILING_REQUIRED_SENTENCES
                  if "Three cell states are distinct" in sentence)
    words: list[str] = []
    for word in ("unread", "unresolved", "machine-unresolved"):
        found = f"*{word}*"
        if clause.count(found) == 1:
            words.append(word)
        else:
            raise StandardInvalid(
                "CEILING_TEXT_MALFORMED",
                f"the frozen ceiling names {word!r} "
                f"{clause.count(found)} times, not once")
    return tuple(words)  # type: ignore[return-value]


#: The three printed spellings, owned by the ceiling and derived above.
TRICHOTOMY_WORDS: Tuple[str, str, str] = _trichotomy_words()

#: An INDETERMINATE coordinate is a request or attempt with no response: a
#: delivery fact, and never a reading of the material.
INDETERMINATE_SENTENCE = (
    "An INDETERMINATE coordinate is a request or an attempt that has no "
    "response on record. It is a delivery fact, never a reading, and it is "
    "listed rather than counted because the run must answer for every one."
)

#: Printed where the run's audit record in force is summarised; the graph's
#: audit findings are the record, and none is distilled into a metric.
AUDIT_IN_FORCE_SENTENCE = (
    "The audit record in force is the appellate and audit artifacts registered "
    "in the graph; each is printed as entered, and none of the audit results "
    "is reduced to a measure of the reader."
)

#: ``appellate_rulings: 0`` renders exactly this.  The ceiling's
#: appellate clause carries the same rule, but the closing record states it
#: where the count is printed, so a reader need not cross-reference to learn
#: the run was not validated.
APPELLATE_NOT_VALIDATED_SENTENCE = (
    "This record does not describe the run as validated, checked or confirmed. "
    "That the loop ran without a human is a fact about the loop, not a fact "
    "about the readings."
)

APPELLATE_HEADING = "appellate_rulings"

#: The one word per graph standing, so the three the ceiling names print as
#: three distinct things and the two the ceiling does not name print as their
#: own words - contested is a discrimination problem, orphaned is not false,
#: and neither borrows a trichotomy word it would blur.
CELL_READ_SENTENCE = "read"
CELL_UNREAD_SENTENCE = TRICHOTOMY_WORDS[0]
CELL_UNRESOLVED_SENTENCE = TRICHOTOMY_WORDS[1]
CELL_MACHINE_WORD = TRICHOTOMY_WORDS[2]
CELL_CONTESTED_WORD = "contested"
CELL_ORPHANED_WORD = "orphaned"

#: The trichotomy table's header row.  The third column names the block code
#: that declined the cell - the ceiling's own promise.
TRICHOTOMY_HEADING = (
    "| cell | states as three things | block reason that declined it |")

#: Printed where a fixed section carries nothing, so absence is always an
#: explicit sentence and never a missing section.
EMPTY_LIST = "- none"
NO_READING_SET = "_No use-relation rows were read this run._"
NO_AUDIT_RECORDS = "- none: no audit record entered the graph this run."
NO_LOSSES_OUTSIDE_P = "- none"
NO_INDETERMINATE_COORDINATES = INDETERMINATE_SENTENCE + "\n\n- none"

#: Where the frozen ceiling block is printed: a fixed heading, then every
#: invariant sentence as its own plain paragraph, verbatim.
CEILING_HEADING = "the frozen ceiling block"
CEILING_PRELUDE = (
    f"CEILING.md is pinned into the plan at sha256 `{CEILING_SHA256}`. Every "
    "invariant sentence of it is printed verbatim below; the per-cell claim "
    "template it also carries is a clause a cell asserts and this table "
    "states no cell's claim."
)

#: A cycle record carries its decision's own sentences; a stop says what stops.
STOPPING_SENTENCE_HEADING = "the stopping sentence"
CHAIN_OPEN_SENTENCE = (
    "The chain did not stop at this cycle; no stopping sentence applies."
)
STOP_WORD = "STOP"
CONTINUE_WORD = "CONTINUE"

#: ``losses_outside_P`` is printed every cycle and every closing, present even
#: when empty (FW5:802). Both framing sentences are **W2-DECIDE's**, imported:
#: the draft wrote its own paraphrase of each, so the same rule would have been
#: stated twice in one record in two different forms, and a reader could not
#: tell whether the two were saying the same thing. One owner, one spelling -
#: and ``decision.record_sentences`` already carries decide's own, so a
#: paraphrase beside it was a second voice in the same paragraph.
LOSSES_OUTSIDE_P_SENTENCE = NET_WITHDRAWAL_SENTENCE

#: What an unread cell's prose says, and what it does not.  Two different
#: reasons the reading arm may not have reached a cell, and they print as two
#: different sentences, because conflating them lets an unfinished worksheet
#: read as a finding.
UNREAD_SENTENCE = (
    "an unread cell is one nobody and nothing has read - it was never "
    "dispatched to the reading arm. Absence of a reading here is silent about "
    "content."
)
STILL_TURNING_SENTENCE = (
    "the reading arm asked and the asking did not finish; the trial ended "
    "blocked or ended unanswered, and the block reason beside the cell names "
    "what declined it."
)

#: The audit register's header cells.  None names a magnitude.
AUDIT_HEADER_CELLS: Tuple[str, ...] = ("| seat | kind | detail |",)

#: An opened cell at its grounded default is ``unresolved`` by adjudication,
#: not by anyone's entry; the word is the ceiling's second trichotomy word.
UNRESOLVED_DEFAULT_WORD = CELL_UNRESOLVED_SENTENCE


# --------------------------------------------------------------------------
# Declared records
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class RegisterRow:
    """One register cell's mark, for COMPARISON.md.

    ``blocks`` is the bare block reasons this cell's trials ended in (each a
    member of ``types.CEILING_BLOCK_REASONS`` or the register's "constitution"
    extra); ``mark`` is one of ``standard.MARKS``, and a cell no mark entered
    stays at the unresolved default.
    """

    cell: str
    register: str
    comparison: str | None = None
    mark: str = "unresolved"
    blocks: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "cell", _text(self.cell, "cell"))
        object.__setattr__(self, "register", _text(self.register, "register"))
        if self.comparison is not None:
            object.__setattr__(self, "comparison", str(self.comparison))
        object.__setattr__(self, "mark", _text(self.mark, "mark"))
        object.__setattr__(self, "blocks", _block_reasons(self.blocks))

    @property
    def key_token(self) -> str:
        """The one-line cell spelling, with the register and comparison in it."""
        parts = [self.cell, self.register]
        if self.comparison is not None:
            parts.append(self.comparison)
        return "|".join(parts)


@dataclass(frozen=True)
class ReportPlan:
    """The plan fragment a table render needs, declared rather than mapped.

    ``pins`` is the plan's pin map as design 4.2 folds it: repo-relative POSIX
    path to sha256.  ``reading_set`` is the frozen declaration that drives the
    "unread" half of the trichotomy.  ``loop_plan_id`` rides on the closing
    record.  The renderers refuse if the ceiling's own pin is absent, which is
    the only clause they answer for.
    """

    loop_plan_id: str = ""
    pins: Mapping[str, str] | None = None
    reading_set: Tuple[str, ...] | None = None
    ceiling_text: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.pins, Mapping):
            raise ReportRefused("SOURCE_PIN_MISSING",
                                "a plan carries its pins map")
        object.__setattr__(self, "pins",
                           MappingProxyType({str(key): str(digest)
                                             for key, digest in self.pins.items()}))
        if self.reading_set is not None:
            object.__setattr__(self, "reading_set",
                               tuple(_text(value, "reading_set")
                                     for value in self.reading_set))
        if self.ceiling_text is not None:
            object.__setattr__(self, "ceiling_text", str(self.ceiling_text))


@dataclass(frozen=True)
class CycleState:
    """What one cycle handed this renderer (deviation 3).

    ``standings`` are W1-GRAPH's own read-backs; ``blocks`` is ``(cell,
    reason)`` pairs from the trial arm, bare reason spellings;
    ``indeterminate`` is ``steps.scan_coordinates``' list of coordinates with a
    request or an attempt and no response; ``unread`` is the reading rows the
    cycle never reached.  All four default empty, because an absent account is
    the account of an absent thing - but the *sections themselves* are
    unconditional in the rendered record, so a missing section is the bug.
    """

    standings: Tuple[CellStanding, ...] = ()
    blocks: Tuple[tuple, ...] = ()
    indeterminate: Tuple[str, ...] = ()
    unread: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("standings", "indeterminate", "unread"):
            object.__setattr__(self, name, tuple(getattr(self, name)))
        object.__setattr__(self, "blocks", tuple(tuple(pair) for pair in self.blocks))
        for standing in self.standings:
            if not isinstance(standing, CellStanding):
                raise StandardInvalid(
                    "STANDARD_DATA_MALFORMED",
                    f"{type(standing).__name__} is not a CellStanding")
        _block_reasons([reason for _cell, reason in self.blocks])


@dataclass(frozen=True)
class ClosingRun:
    """The run as the closing record reads it (deviation 4).

    ``decision`` is the run's last DECIDE step's decision; the closing record
    prints its stopping sentence and its ``losses_outside_P`` register, both of
    which only a decision may own.  A run whose chain is still open is refused:
    the renderer does not invent the sentence.  ``blocks`` and
    ``audit_findings`` are the run's whole registers (not one cycle's);
    ``appellate_rulings`` is the graph's own tuple so a caller holding it needs
    no coercion discipline.
    """

    plan: ReportPlan
    decision: Decision
    blocks: Tuple[tuple, ...] = ()
    standings: Tuple[CellStanding, ...] = ()
    indeterminate: Tuple[str, ...] = ()
    unread: Tuple[str, ...] = ()
    audit_findings: Tuple[Mapping[str, Any], ...] = ()
    appellate_rulings: Tuple[str, ...] = ()
    state: CycleState | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.plan, ReportPlan):
            raise StandardInvalid("STANDARD_DATA_MALFORMED",
                                  "closing run takes a ReportPlan")
        if not isinstance(self.decision, Decision):
            raise StandardInvalid("STANDARD_DATA_MALFORMED",
                                  "the closing record takes the run's last Decision")
        object.__setattr__(self, "blocks", tuple(tuple(pair) for pair in self.blocks))
        object.__setattr__(self, "standings", tuple(self.standings))
        object.__setattr__(self, "indeterminate", tuple(self.indeterminate))
        object.__setattr__(self, "unread", tuple(self.unread))
        object.__setattr__(self, "audit_findings", tuple(self.audit_findings))
        object.__setattr__(self, "appellate_rulings", tuple(self.appellate_rulings))
        for standing in self.standings:
            if not isinstance(standing, CellStanding):
                raise StandardInvalid(
                    "STANDARD_DATA_MALFORMED",
                    f"{type(standing).__name__} is not a CellStanding")
        for finding in self.audit_findings:
            if not isinstance(finding, Mapping):
                raise StandardInvalid(
                    "STANDARD_DATA_MALFORMED",
                    f"{type(finding).__name__} is not an audit finding")
        _block_reasons([reason for _cell, reason in self.blocks])
        if self.state is not None and not isinstance(self.state, CycleState):
            raise StandardInvalid("STANDARD_DATA_MALFORMED",
                                  "state must be a CycleState or absent")


# --------------------------------------------------------------------------
# Small gates
# --------------------------------------------------------------------------

def _text(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise StandardInvalid("STANDARD_DATA_MALFORMED",
                              f"{where} is a non-empty string")
    return value


def _block_reasons(values: Iterable[str]) -> Tuple[str, ...]:
    """Bare block reasons, checked against the one closed vocabulary.

    A reason the ceiling's nine do not name prints only if it is the register's
    tenth row (``constitution``); anything else is refused rather than rendered
    inside a table that claims completeness.
    """

    reasons = []
    for raw in values:
        reason = str(raw)
        bare = reason.removeprefix(_t.BLOCK_CODE_PREFIX)
        if bare not in BLOCK_REGISTER_HEADINGS:
            raise StandardInvalid(
                "STANDARD_DATA_MALFORMED",
                f"{reason!r} is not a block reason this register prints")
        reasons.append(bare)
    return tuple(reasons)


def ceiling_key_of(plan: Any) -> str:
    """The plan's pin for ``standard.CEILING_PATH``, verified on its declared sha.

    Design §6: the renderer refuses without CEILING.md at its pinned sha.  The
    plan names it under the path's repo-relative POSIX spelling; both a raw
    ``pins`` mapping and a :class:`ReportPlan` are accepted so a caller holding
    the plan body does not have to rebuild it.  Absent is
    ``SOURCE_PIN_MISSING`` and shifted is ``SOURCE_PIN_MISMATCH`` - the two
    facts custody itself reports on a tree, so one vocabulary covers the plan
    and the tree it pins.
    """

    key = CEILING_PIN_KEY
    if isinstance(plan, ReportPlan):
        pins = plan.pins or {}
    elif isinstance(plan, Mapping):
        pins = plan.get("pins")
        if not isinstance(pins, Mapping):
            raise ReportRefused("PIN_MAP_MISSING", "the plan body carries no pins map")
    else:
        raise StandardInvalid("STANDARD_DATA_MALFORMED", type(plan).__name__)
    digest = pins.get(key)
    if digest is None:
        raise ReportRefused(
            "SOURCE_PIN_MISSING",
            f"the plan pins no ceiling under {key!r}; no table or report "
            "renders without CEILING.md at its pinned sha")
    if digest != CEILING_SHA256:
        raise ReportRefused(
            "SOURCE_PIN_MISMATCH",
            f"the plan pins CEILING.md as {digest!r}, not the frozen "
            f"{CEILING_SHA256!r}")
    return key


def _verify_ceiling_text(text: str | None, where: str) -> None:
    """If the run carried the ceiling's bytes, they must be the pinned bytes."""
    if text is None:
        return
    from deepreason_core.canonical import sha256_hex

    if sha256_hex(text.encode("utf-8")) != CEILING_SHA256:
        raise StandardInvalid(
            "STANDARD_DATA_MALFORMED",
            f"{where} carries ceiling bytes that do not digest to "
            f"{CEILING_SHA256!r}; a record may not render a ceiling it "
            "invented")


def _loss_row(loss: Loss) -> str:
    membership = loss.membership or "outside P"
    return (f"- {loss.kind}: {loss.subject} was {loss.was}, now {loss.now} "
            f"[{membership}] - {loss.detail}")


def _require_sentences(text: str, where: str) -> None:
    """The acceptance clause as a program: every required ceiling sentence
    appears verbatim in the finished text, or the render is refused.

    "Verbatim" is the plain string, printed as an unwrapped paragraph; a
    sentence a renderer re-wrapped would no longer be present as itself, and
    the refusal names what went missing.
    """

    absent = [sentence for sentence in CEILING_REQUIRED_SENTENCES
              if sentence not in text]
    if absent:
        raise StandardInvalid(
            "CEILING_TEXT_MALFORMED",
            f"{where} does not print {len(absent)} of the frozen ceiling's "
            f"{len(CEILING_REQUIRED_SENTENCES)} invariant sentences verbatim; "
            f"the first missing opens {absent[0][:40]!r}")


def _final(text: str, where: str) -> str:
    """Every rendered artifact answers the same four gates before it leaves."""
    body = text.rstrip() + "\n"
    _require_sentences(body, where)
    assert_no_exhaustion_claim(body, where)
    assert_no_scoring_headers(body, where)
    return body


def _ceiling_block() -> list[str]:
    """The frozen ceiling, printed verbatim as its own section.

    Every invariant sentence is its own paragraph; none is wrapped, quoted,
    headed or summarised.  The per-cell claim template is pointed at, not
    paraphrased: this run's table states no cell's claim.
    """

    lines = [f"## {CEILING_HEADING}", "", CEILING_PRELUDE, ""]
    for sentence in CEILING_REQUIRED_SENTENCES:
        lines.extend([sentence, ""])
    return lines


def _declined_to_read(standings: Sequence[CellStanding],
                      blocks: Sequence[tuple]) -> bool:
    """Did the instrument decline to read, or did it read and stay unresolved?

    Three different runs would all answer "nothing was read", and only two of
    them are the instrument declining. A run with blocks and no reading is the
    guard refusing to resolve; a table with no cells at all is a worksheet, and
    it carries the sentence so it cannot be mistaken for a finding. A run whose
    cells were *deliberately read* and stayed at the grounded default is
    neither: the trichotomy's own unresolved section says what happened, and
    claiming "every reading cell was blocked" over it would be false. An
    unresolved cell proves neither presence nor absence, and neither does a
    blocked one - but they are not the same fact and are not printed as one.
    """
    if any(standing.state == "read" for standing in standings):
        return False
    return bool(blocks) or not standings


def _block_register(lines: list[str], blocks: Sequence[tuple]) -> list[str]:
    """The register by reason code, with counts - every heading row present.

    Every one of :data:`BLOCK_REGISTER_HEADINGS` prints every time, with its
    tally; a reason the run never met prints its name and `x0`, so the register
    is complete even where the tally is none.  The count is the ceiling's own
    requirement ("printed with counts on every table") and appears nowhere else.
    """

    tally = {reason: 0 for reason in BLOCK_REGISTER_HEADINGS}
    for _cell, reason in blocks:
        tally[reason] = tally[reason] + 1
    lines.extend(["## block register by reason code", "",
                  "| reason code | cell |",
                  "| --- | --- |"])
    for reason in BLOCK_REGISTER_HEADINGS:
        named = ", ".join(sorted(str(cell) for cell, why in blocks if why == reason))
        lines.append(f"| `{reason}` x{tally[reason]} | {named or '-'} |")
    lines.append("")
    return lines


def block_line(cell: str, reason: str) -> str:
    """One line of the machine-unresolved list: the cell and the code that declined it."""
    return f"- {cell}: `{reason}`"


def audit_line(finding: Mapping[str, Any]) -> str:
    """The audit register row, as the finding was entered - never distilled."""
    seat = str(finding.get("seat", ""))
    kind = str(finding.get("kind", ""))
    detail = str(finding.get("detail", ""))
    name = seat or "the run"
    line = f"- {kind} for {name}"
    if detail:
        line = f"{line}: {detail}"
    return line


def _trichotomy(standings: Sequence[CellStanding], blocks: Sequence[tuple],
                unread: Sequence[str]) -> list[str]:
    """The unread / unresolved / machine-unresolved trichotomy, three sections.

    A cell prints in exactly one.  The machine list names the block code that
    declined it; a cell that ended as the grounded default through a deliberate
    reading is *unresolved*; and one nothing and nobody read is *unread* - and
    the prose says which way it is unread, because the two are not the same
    fact.
    """

    by_key = {standing.key: standing for standing in standings}
    declined = sorted((str(cell), reason) for cell, reason in blocks)
    machine_keys = {cell for cell, _reason in declined}

    lines = ["## the unread / unresolved / machine-unresolved trichotomy", "",
             TRICHOTOMY_HEADING,
             "| --- | --- | --- |"]
    for key in sorted(set(by_key) | {str(cell) for cell in unread} | machine_keys):
        standing = by_key.get(key)
        reason = next((f"`{why}`" for cell, why in declined if cell == key), "-")
        if standing is None and key in machine_keys:
            # The guard declined a cell that never reached a default. It is
            # machine-unresolved, not unread: something did read it, and the
            # block code says what stopped. Printing it as unread here while
            # also listing it below was the one way a cell appeared in two of
            # the three states the ceiling says are distinct.
            word = f"{CELL_MACHINE_WORD} ({reason.lstrip('`').rstrip('`')})"
        elif standing is None:
            word = CELL_UNREAD_SENTENCE
        elif standing.state == "read":
            word = f"{CELL_READ_SENTENCE}: {standing.relation}"
        elif standing.state == "unresolved":
            word = (f"{CELL_MACHINE_WORD} ({reason.lstrip('`').rstrip('`')})"
                    if key in machine_keys else CELL_UNRESOLVED_SENTENCE)
        elif standing.state == "contested":
            word = CELL_CONTESTED_WORD
        else:
            word = CELL_ORPHANED_WORD
        lines.append(f"| {key} | {word} | {reason} |")
    lines.append("")
    lines.extend(["### unread", ""])
    rows = [f"- {key}: {UNREAD_SENTENCE}"
            for key in sorted(str(cell) for cell in unread)
            if key not in machine_keys and key not in by_key]
    lines.extend(rows or [EMPTY_LIST])
    lines.append("")
    lines.extend(["### unresolved", ""])
    rows = []
    for key in sorted(by_key):
        standing = by_key[key]
        if standing.state == "unresolved" and key not in machine_keys:
            rows.append(f"- {key}: the deliberate reading of this cell stays "
                        "unresolved; it proves neither presence nor absence.")
    lines.extend(rows or [EMPTY_LIST])
    lines.append("")
    lines.extend(["### machine-unresolved", ""])
    rows = [block_line(cell, reason) for cell, reason in declined]
    lines.extend(rows or [EMPTY_LIST])
    lines.append("")
    return lines


# --------------------------------------------------------------------------
# The four renderers
# --------------------------------------------------------------------------

def render_reading_table(harness: Any, plan: Any, *,
                        state: "CycleState | None" = None) -> str:
    """``READING_TABLE.md``: the whole use-relation table, plus the registers.

    Reads W1-GRAPH's standings exactly as the adjudication left them and the
    plan's frozen ``reading_set`` for what nothing reached; the cell states
    print as the three the ceiling names, with the block code beside each
    machine-declined one.  A run with nothing read renders declined-to-read,
    with the block register by reason code above it, and never as an absence
    of relations.

    ``plan`` is the plan body (ceiling pin or refusal) or a
    :class:`ReportPlan`; where it declares a ``reading_set``, rows it names
    that the graph has no opened cell for print as unread.

    ``state`` is the cycle's own record (deviation 3, and deviation 6): a
    blocked trial registers nothing, so **no block is readable from the
    harness**, and a table rendered without one prints an empty block register
    over a run that was declined. It is keyword-only, so the wave plan's
    declared two-argument call still renders - it renders a table whose block
    register is honestly empty, which is the right answer only for a run with
    no blocks. The unread inventory is the union of the plan's undelivered
    reading-set rows and the caller's own ``state.unread``, because a cell the
    reading set never named is unread too (REVIEW-PREREG PR-13).
    """

    ceiling_key_of(plan)
    if isinstance(plan, ReportPlan):
        confirmed_plan = plan
    else:
        confirmed_plan = ReportPlan(pins=plan["pins"])
    _verify_ceiling_text(confirmed_plan.ceiling_text, "reading table plan")
    if state is not None and not isinstance(state, CycleState):
        raise StandardInvalid("STANDARD_DATA_MALFORMED",
                              "state must be a CycleState or absent")

    from . import graph as _graph

    standings = tuple(_graph.cell_standings(harness))
    machine: tuple = () if state is None else state.blocks
    opened = {standing.key for standing in standings}
    declared = (confirmed_plan.reading_set or ())
    supplied = () if state is None else state.unread
    unread = [key for key in list(declared) + list(supplied)
              if key not in opened]

    header = confirmed_plan.loop_plan_id or "(plan unpinned)"
    lines: list[str] = [f"# Reading table - {header}", ""]
    lines = _block_register(lines, machine)
    if _declined_to_read(standings, machine):
        lines.extend([DECLINED_TO_READ_SENTENCE, ""])
    if not standings:
        lines.extend([NO_READING_SET, ""])
    lines.extend(_trichotomy(standings, machine, unread))
    if any(standing.state == "read" for standing in standings):
        lines.append("cells read:")
    for standing in standings:
        if standing.state != "read":
            continue
        lines.append(f"- {standing.key}: read as `{standing.relation}`")
    lines.append("")
    for standing in standings:
        if standing.state == "contested":
            lines.append(f"- {standing.key}: {CELL_CONTESTED_WORD}; two rival "
                         "readings survive and the cell is a discrimination "
                         "problem, never an average.")
    lines.append("")
    lines.extend(_ceiling_block())
    text = _final("\n".join(lines), "reading table")
    assert_no_scoring_keys(rendered_files_record({"READING_TABLE.md": text}))
    return text


def render_comparison(harness: Any, plan: Any, *,
                     state: "CycleState | None" = None) -> str:
    """``COMPARISON.md``: the C001 register table, four registers, never combined.

    Every mark comes from a ``(cell, register, comparison)`` key of W1-GRAPH
    and prints under its own register's column; no field holds two registers at
    once, so no combined register can appear.  The key is taken apart with
    ``graph.CellKey.coerce`` and never by splitting on a separator this module
    would then own a second spelling of.  The block register prints with counts,
    over ``state.blocks`` where the caller has them (deviation 6): a blocked
    mark registers nothing, so the harness cannot answer for one.
    """

    ceiling_key_of(plan)
    if isinstance(plan, ReportPlan):
        confirmed_plan = plan
    else:
        confirmed_plan = ReportPlan(pins=plan["pins"])
    _verify_ceiling_text(confirmed_plan.ceiling_text, "comparison plan")
    if state is not None and not isinstance(state, CycleState):
        raise StandardInvalid("STANDARD_DATA_MALFORMED",
                              "state must be a CycleState or absent")

    from . import graph as _graph

    standings = tuple(_graph.cell_standings(harness))
    register_standing = [standing for standing in standings
                         if standing.register is not None]
    lines: list[str] = ["# Comparison", ""]
    lines = _block_register(lines, () if state is None else state.blocks)
    lines.extend(["| cell | register | comparison | mark |",
                  "| --- | --- | --- | --- |"])
    for standing in sorted(register_standing, key=lambda s: s.key):
        word = standing.relation if standing.state == "read" else standing.state
        key = _graph.CellKey.coerce(standing.key)
        lines.append(f"| {key.cell} | {key.register} | "
                     f"{key.comparison or '-'} | {word} |")
    if not register_standing:
        lines.append("| - | - | - | - |")
    lines.append("")
    lines.extend(["The four registers are marked separately and never combined; "
                  "each row is one register of one cell, and no cell's marks "
                  "are ever summed, averaged, weighted, ranked or reduced to "
                  "one mark."])
    lines.append("")
    lines.extend(_ceiling_block())
    text = _final("\n".join(lines), "comparison")
    assert_no_scoring_keys(rendered_files_record({"COMPARISON.md": text}))
    return text


def render_cycle(decision: Decision, state: CycleState) -> str:
    """One cycle's ``CYCLE.md``: the stopping sentence and the registers around it.

    The decision's own ``record_sentences`` print verbatim, and
    ``losses_outside_P`` prints beside the block register - present even when
    empty.  A cycle that did not stop prints the open-chain sentence under the
    stopping-sentence heading, so the heading is never a lie by omission.
    """

    if not isinstance(decision, Decision):
        raise StandardInvalid("STANDARD_DATA_MALFORMED",
                              "render_cycle takes a Decision")
    if not isinstance(state, CycleState):
        raise StandardInvalid("STANDARD_DATA_MALFORMED",
                              "render_cycle takes a CycleState")

    lines: list[str] = [f"# Cycle {decision.cycle:02d}", ""]
    lines.extend([f"## {STOPPING_SENTENCE_HEADING}", ""])
    lines.append(("STOP: " if decision.stop else "CONTINUE: ") + decision.reason)
    lines.append("")
    lines.extend([f"- outcome: {STOP_WORD if decision.stop else CONTINUE_WORD}",
                  f"- clause: {decision.clause}",
                  f"- detail: {decision.detail}",
                  ""])
    for sentence in decision.record_sentences:
        lines.extend([sentence, ""])
    if decision.stop:
        if decision.reason == "protected_loss":
            lines.extend([PROTECTED_LOSS_SENTENCE, ""])
        # Design 5: "Every stop carries a mandatory would_reopen prose field."
        # A protected loss is a stop, so it carries one too; printing the
        # protected-loss sentence *instead of* it dropped the field from the one
        # record that most needs to say what would reopen the question.
        lines.extend([f"- would_reopen: {decision.would_reopen}", ""])
    else:
        lines.extend([CHAIN_OPEN_SENTENCE, ""])
    lines = _block_register(lines, state.blocks)
    lines.extend(["## losses_outside_P", "", LOSSES_OUTSIDE_P_SENTENCE, ""])
    losses = [_loss_row(loss) for loss in decision.losses_outside_p]
    lines.extend(losses or [NO_LOSSES_OUTSIDE_P])
    lines.append("")
    lines.extend(["## INDETERMINATE - requests and attempts without a response", "",
                  INDETERMINATE_SENTENCE, ""])
    lines.extend([f"- {coordinate}" for coordinate in state.indeterminate]
                 or [EMPTY_LIST])
    lines.append("")
    lines.extend(_trichotomy(state.standings, state.blocks, state.unread))
    lines.extend(_ceiling_block())
    text = _final("\n".join(lines), "cycle record")
    assert_no_scoring_keys(rendered_files_record({"CYCLE.md": text}))
    return text


def render_closing(run: ClosingRun) -> str:
    """``CLOSING.md``: the run's closing record.

    The mandatory pieces, each its own section: the frozen ceiling block, the
    block register by reason code with counts for the *run*, the audit record
    in force, the stopping sentence, ``losses_outside_P`` present even when
    empty, the INDETERMINATE list, the trichotomy, and ``appellate_rulings: N``
    with the not-validated sentence where N is zero.  A run refusing to close
    because its chain is still open is refused at the constructor.
    """

    if not isinstance(run, ClosingRun):
        raise StandardInvalid("STANDARD_DATA_MALFORMED",
                              "render_closing takes a ClosingRun")
    ceiling_key_of(run.plan)
    _verify_ceiling_text(run.plan.ceiling_text, "closing run")

    if run.decision.continues:
        raise StandardInvalid(
            "STANDARD_DATA_MALFORMED",
            "the chain is still open; the closing record prints the stopping "
            "sentence, and an open chain carries none")

    lines: list[str] = [f"# Closing record - {run.plan.loop_plan_id}", ""]
    lines.extend([f"- loop_plan_id: {run.plan.loop_plan_id}",
                  f"- ceiling_sha256: {CEILING_SHA256}",
                  f"- ceiling_pinned_at: {ceiling_key_of(run.plan)}",
                  ""])
    lines.extend(_ceiling_block())
    lines = _block_register(lines, run.blocks)
    if _declined_to_read(run.standings, run.blocks):
        lines.extend(DECLINED_TO_READ_SENTENCE.splitlines())
        lines.append("")
    lines.extend(["## the audit record in force", "", AUDIT_IN_FORCE_SENTENCE, ""])
    audits = [audit_line(finding) for finding in run.audit_findings]
    lines.extend(audits or [NO_AUDIT_RECORDS])
    lines.append("")
    lines.extend([f"## {STOPPING_SENTENCE_HEADING}", "",
                  f"{STOP_WORD if run.decision.stop else CONTINUE_WORD}: "
                  f"{run.decision.reason}",
                  f"- clause: {run.decision.clause}",
                  f"- detail: {run.decision.detail}",
                  f"- would_reopen: {run.decision.would_reopen}",
                  ""])
    for sentence in run.decision.record_sentences:
        lines.extend([sentence, ""])
    lines.extend(["## losses_outside_P", "", LOSSES_OUTSIDE_P_SENTENCE, ""])
    losses = [_loss_row(loss) for loss in run.decision.losses_outside_p]
    lines.extend(losses or [NO_LOSSES_OUTSIDE_P])
    lines.append("")
    lines.extend(["## INDETERMINATE - requests and attempts without a response", "",
                  INDETERMINATE_SENTENCE, ""])
    lines.extend([f"- {coordinate}" for coordinate in run.indeterminate]
                 or [EMPTY_LIST])
    lines.append("")
    if run.state is not None:
        lines.extend(_trichotomy(run.state.standings, run.state.blocks,
                                 run.state.unread))
    else:
        lines.extend(_trichotomy(run.standings, run.blocks, run.unread))
    lines.extend([f"## {APPELLATE_HEADING}", "",
                  f"`appellate_rulings: {len(run.appellate_rulings)}`.", ""])
    if run.appellate_rulings:
        for ruling in run.appellate_rulings:
            lines.append(f"- {ruling}")
        lines.append("")
    else:
        lines.extend([APPELLATE_NOT_VALIDATED_SENTENCE, ""])
    text = _final("\n".join(lines), "closing record")
    assert_no_scoring_keys(rendered_files_record({"CLOSING.md": text}))
    return text
