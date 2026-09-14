"""W3-AUDITS - judge audits over readings already on record.

Purpose
-------
Design 2.5 runs four audits, on a schedule, over readings **already on record**:

*   **paraphrase invariance** - re-rule a logged exchange on a fresh variator
    paraphrase of it; a flip is a hit;
*   **premise deletion** - delete the cited ``decisive_point`` from the
    exchange and re-rule; a ruling that survives the removal of its own
    stated grounds is easy to vary, and is a hit;
*   **planted-flaw calibration** - a constructed set whose ground truth is
    true *by construction*, seeded at PREREGISTER and pinned. An error share
    above the declared ``judge_err_max`` returns a Spawn signal;
*   **ensemble disagreement** - a measure series, never a verdict: a variance
    between two seats is a disagreement, so every row here is ``unresolved``
    on purpose.

Every hit is registered through ``graph.register_audit_warrant`` as an
``eval:program`` DEMONSTRATIVE warrant against the ``nu_soundness`` of every
reading that seat carried in the window - so the readings collapse in pass 1
by D10's closure, and nobody decided to withdraw anything. Every audit output
is an artifact with its own validity node (``nu_audit``) and is itself
attackable: attacking the finding reinstates every reading it collapsed.

Design section implemented
--------------------------
Design 2.5 ("Judge audits, on a schedule") in full, and the W3-AUDITS entry of
the section 7 wave plan for the public interface and the acceptance list.

What the judge caller is
------------------------
``judge_caller(seat_label, pack, coordinate) -> JudgeRuling | None`` is the
one provider boundary of this module. The driver binds it to
``roles.call_judge`` with one seat, one records directory and one offline
fixture factory; ``None`` is a blocked or absent reply (a delivery fact about
the route, never a reading) and never raises. This module itself imports no
provider module and opens no connection.

The pack text is the re-ruling pack: the rubric's own relation body, the
exchange under re-ruling (the original, a paraphrase of it, or the exchange
with the premise removed), the ruling under audit reproduced verbatim, and the
instrument's lexical-overlap banner, imported from ``standard`` and never
retyped. It is rendered locally and byte-stably: W2-PACKS renders the packs of
the *trial* being audited and has no shape for an audit re-ruling pack, so
there is nothing there to reuse and this module never imports ``packs``.

The recompute
-------------
"Collapses that seat's readings on recompute" is read on a SECOND harness -
``graph.open_graph`` over the same root - because a reopened harness replays
the log and adjudicates once at the end, which is exactly the recompute the
calculus promises. ``run_audits`` returns ``(cell key, state)`` pairs read
from that reopened view; the labels are the vendored adjudicator's, never
this module's.

Deviations from the design, and why
-----------------------------------
1. **``planted_flaw_calibration`` returns a calibration outcome, not a bare
   float.** The wave plan's declared ``-> float|None`` is kept exactly as
   ``CalibrationOutcome.share``: the float, or ``None`` when no seat was
   exercised. What a bare float cannot carry is what makes the share
   pre-registered - the errors as a set identity, the per-error warrants those
   errors registered, and, where the share crossed the bound, the Spawn signal
   naming every exercised anchor and the margin's own account. ``__float__``
   and equality against a float keep the bare reading a caller written to the
   plan's signature expects; a rate with no declared denominator, anchor and
   account is a meter (design 5, FW5:851), and this module does not mint one.
   **The share adjudicates nothing**: it does not enter a reading's standing,
   it is never compared between seats, and the only consequence it may have is
   crossing a pre-registered instrument bound (ruling 7). What collapses a
   reading is the demonstrative warrant each error already registered.
2. **The calibration set's exchange bytes are fixed strings this module
   holds.** The set is seeded at PREREGISTER from the registered standard's
   anchor list and pinned; regrowing it at audit time would be a second source
   of ground truth. The anchors' ``construction`` and ``ground_truth_reason``
   are read off the registered standard body, so the true-by-construction
   claim is the standard's own text.
3. **The panel is the driver's or the graph's; this module spells none.**
   Design 2.5's calibration runs above the panel and the disagreement series is
   over the *ensemble*, so both need seat labels - but a label invented here is
   not the label ``graph.register_reading`` stored, and a warrant minted against
   an invented label attaches to an empty window. ``run_audits`` takes an
   optional ``panel=`` (the pinned seat plan's labels) and otherwise reads
   :data:`PANEL_ON_RECORD`, ``graph.seats_on_record`` - the seats that actually
   carry readings here, which are exactly the seats a hit can collapse.
4. **The audit never paraphrases the material.**  ``paraphrase_invariance``
   re-asks on a paraphrase of the *exchange* (the case and the answer), which
   is design 2.4 G7's own boundary: the surface bytes the offsets resolve
   against are untouched, exactly because they are the material.
5. **The ensemble-disagreement arm never fabricates its second seat.**
   ``graph.register_reading`` stores a ``roles`` mapping when the caller
   supplies one and leaves it empty otherwise. Where the record names two
   distinct seats they are the pair; where it does not, the panel is; and where
   neither yields two, the reading contributes **no row** rather than a row in
   which one seat answers twice. One seat's two answers are never a variance
   between two seats, and a row saying "agreed" about an ensemble that was
   never asked is worse than no row.

6. **``judge_err_max`` and its account come from the frozen config, and this
   module has no fallback for either.** ``types.AuditConfig`` already rules that
   no threshold has a default and that each carries a required account; a
   default here would be a second, unpinned spelling of a pre-registered margin.
   REVIEW-PREREG PR-09 shows what an invented account costs: the "five anchors,
   so the margin is one anchor of five" reading misstates its own denominator
   against a nine-row ``calibration.json``. An absent bound or an empty account
   is ``CONFIG_MISSING_KEY`` / ``CONFIG_INVALID_VALUE``, not a guess.

The refusal codes this module introduces are declared in :data:`NEW_CODES` -
none: every refusal here is one ``graph`` or ``types`` already owns. The one
token this module coins is the Spawn signal ``audit-the-critic``, because
design 2.4 and 2.5 both name it and no module owned it yet; it is a string on
a signal, never a failure code and never a status.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Mapping, Sequence

from . import graph
from .contracts import JudgeRuling
from .standard import READING_BANNER, RUBRIC_V1, STANDARD_BODY, UNRESOLVED_TOKEN
from .types import LoopError

__all__ = [
    "AUDITS_SCHEMA",
    "AUDIT_PACK_SCHEMA",
    "CALIBRATION_EXCHANGES_SHA256",
    "PANEL_ON_RECORD",
    "SPAWN_AUDIT_THE_CRITIC",
    "AuditError",
    "NEW_CODES",
    "CalibrationCase",
    "CalibrationOutcome",
    "AuditHit",
    "Disagreement",
    "SpawnSignal",
    "AuditReport",
    "build_calibration_set",
    "paraphrase_invariance",
    "premise_deletion",
    "planted_flaw_calibration",
    "disagreement_series",
    "run_audits",
    "render_ruling_pack",
]


AUDITS_SCHEMA = "minireason.loop.audits.v1"

#: The schema name the audit re-ruling pack would carry were it registered.
#: None is registered: the schema name is declared so a reader of the graph
#: can tell an audit pack artifact from a trial pack artifact were a later
#: wave to register one.
AUDIT_PACK_SCHEMA = "minireason.loop.audits.audit-pack.v1"

#: The Spawn signal design 2.5 names for an error share past ``judge_err_max``.
#: A signal token on a report, never a failure code and never a status.
SPAWN_AUDIT_THE_CRITIC = "audit-the-critic"

#: This module introduces no failure code: every refusal it can raise is one
#: ``graph`` or ``types`` already declares. Declared, per W0 open question O9.
NEW_CODES: Mapping[str, str] = MappingProxyType({})

#: This module declares no panel. The seats it audits are the seats on record -
#: ``graph.seats_on_record`` - or the panel the driver passes, which is the one
#: the pinned seat plan froze. A seat spelling invented here would not be the
#: spelling ``graph.register_reading`` stored (W2-ROLES writes ``judge#1`` on a
#: call record and ``judge-1`` only in a directory slug), so every warrant it
#: minted would attach to an empty window: a hit that reads as a hit and
#: collapses nothing. Integration probe, before the fix: a reading registered by
#: ``judge#1`` left ``validity_nodes_for_seat(harness, "judge-1") == ()`` while
#: six calibration errors registered against it.
PANEL_ON_RECORD = "graph.seats_on_record"


class AuditError(LoopError):
    """A declared refusal from the audit layer. Carries ``(code, detail="")``."""


def _fail(code: str, detail: str = "") -> AuditError:
    return AuditError(code, detail)


# --------------------------------------------------------------------- helpers


def _ruling(value: Any) -> JudgeRuling | None:
    """Coerce the caller's answer to a ruling; ``None`` is a delivery fact.

    A blocked or absent reply is not an audit outcome and never an exception:
    the caller returns it as ``None`` and the audit records the call and moves
    on. Anything that is not a ruling and not ``None`` is refused at this
    boundary, because "the caller returned something unreadable" is a plan
    error, not an observation.
    """
    if value is None:
        return None
    if isinstance(value, JudgeRuling):
        return value
    ok = getattr(value, "ok", None)
    output = getattr(value, "output", None)
    if ok is True and isinstance(output, JudgeRuling):
        return output
    if ok is False:
        return None
    raise _fail(
        "CONFIG_INVALID_VALUE",
        f"a judge caller answered {type(value).__name__}, not a JudgeRuling, "
        "a RoleResult, or None")


# --------------------------------------------------------------------- records


@dataclass(frozen=True)
class CalibrationCase:
    """One planted-flaw anchor, with its exchange bytes and its ground truth.

    ``expected_sustained`` is drawn from the standard's calibration anchor set;
    the ``case``/``answer`` bytes are constructed beside the anchor so the
    ground truth is true by *construction* - a fact about how the bytes were
    built, never a reading of them. A clean control is an anchor whose
    ``expected_sustained`` is false.
    """

    anchor: str
    case: str
    answer: str
    expected_sustained: bool
    expected_relation: str | None
    construction: str
    ground_truth_reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "anchor": self.anchor,
            "case": self.case,
            "answer": self.answer,
            "expected_sustained": self.expected_sustained,
            "expected_relation": self.expected_relation,
            "construction": self.construction,
            "ground_truth_reason": self.ground_truth_reason,
        }


@dataclass(frozen=True)
class AuditHit:
    """One audit finding, after ``graph.register_audit_warrant`` has taken it.

    ``targets`` is the validity node set the warrant attacks: the seat's whole
    window by default. ``finding_id`` is the registered finding artifact, so
    the report can say what the hit became and what may be attacked back.
    """

    kind: str
    seat: str
    coordinate: str
    detail: str
    finding_id: str
    targets: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind, "seat": self.seat, "coordinate": self.coordinate,
            "detail": self.detail, "finding_id": self.finding_id,
            "targets": list(self.targets),
        }


@dataclass(frozen=True)
class Disagreement:
    """One row of the ensemble-disagreement series: a variance, unresolved.

    Design 2.5: the series is a Measure, never a verdict. ``disagrees``
    records that two seats answered the same coordinate differently; nothing
    here compares two seats for merit and nothing counts the rows.
    """

    left_seat: str
    right_seat: str
    coordinate: str
    left_sustained: bool | None
    right_sustained: bool | None

    @property
    def disagrees(self) -> bool:
        return (self.left_sustained is not None
                and self.right_sustained is not None
                and self.left_sustained != self.right_sustained)

    def as_dict(self) -> dict[str, Any]:
        return {
            "left_seat": self.left_seat, "right_seat": self.right_seat,
            "coordinate": self.coordinate,
            "left_sustained": self.left_sustained,
            "right_sustained": self.right_sustained,
            "outcome": UNRESOLVED_TOKEN,
        }


@dataclass(frozen=True)
class SpawnSignal:
    """The audit-the-critic signal: past the declared error share, say so.

    It is *returned* on the report, never raised: an instrument fault is a
    fact about the instrument, and the driver decides what follows. It carries
    the anchor ids the share was taken over and the declared account of the
    margin crossed, so the signal is attackable in the same place the margin
    is.
    """

    trigger: str
    observed: float
    bound: float
    account: str
    anchors: tuple[str, ...]

    def prompt(self) -> str:
        """The signal and its own account, in one sentence, for the record."""
        return (
            f"{self.trigger}: the planted-flaw calibration observed share "
            f"{self.observed} past the declared bound {self.bound} "
            f"({self.account}); exercised anchors {sorted(self.anchors)}"
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "trigger": self.trigger, "observed": self.observed, "bound": self.bound,
            "account": self.account, "anchors": list(self.anchors),
        }


@dataclass(frozen=True)
class CalibrationOutcome:
    """What ``planted_flaw_calibration`` answers (the wave plan's ``float|None``).

    ``share`` is the float the declared signature promises: the error share
    over the anchors actually exercised, ``None`` when no seat answered. The
    rest of the record is what makes the float pre-registered: the errors as a
    set identity, the hits those errors already registered against their seats'
    windows, and the Spawn signal where the share crossed the *declared* bound.
    The stated denominator is the exercised set - never recomputed, never
    widened after the fact.

    The share adjudicates nothing. It is never compared with another seat's, it
    never enters a reading's standing, and the only thing it may do is cross a
    pre-registered instrument bound and say so with that bound's own account
    (ruling 7). What collapses a reading is the per-error warrant in ``hits``,
    which is a demonstrative warrant against a validity node and not a rate.
    """

    share: float | None
    errors: tuple[str, ...]
    exercised: tuple[str, ...]
    spawn: SpawnSignal | None = None
    hits: tuple[AuditHit, ...] = ()

    @property
    def crossed(self) -> bool:
        return self.spawn is not None

    def __float__(self) -> float:
        if self.share is None:
            raise TypeError("no seat was exercised, so there is no share")
        return self.share

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, CalibrationOutcome):
            return (self.share, self.errors, self.exercised, self.spawn,
                    self.hits) == (other.share, other.errors, other.exercised,
                                   other.spawn, other.hits)
        if isinstance(other, float) or other is None:
            return self.share == other
        return NotImplemented

    def __hash__(self) -> int:
        return hash(("CalibrationOutcome", self.share, self.errors,
                     self.exercised, self.spawn, self.hits))

    def as_dict(self) -> dict[str, Any]:
        return {
            "share": self.share, "errors": list(self.errors),
            "exercised": list(self.exercised),
            "spawn": self.spawn.as_dict() if self.spawn is not None else None,
            "hits": [hit.as_dict() for hit in self.hits],
        }


@dataclass(frozen=True)
class AuditReport:
    """One audit pass: the findings, the series, the calibration, the recompute.

    ``collapsed`` is the ``(cell key, state)`` pairs whose standing changed on
    the reopened harness - the recomputed vendored labels, never a verdict
    this module assigned. ``logs`` is one entry per audit coordinate called,
    so "every audit call reached the log exactly once" is a decidable question
    about this record rather than an inference about a provider's bookkeeping.
    """

    schema: str
    findings: tuple[AuditHit, ...]
    series: tuple[Disagreement, ...]
    calibration: CalibrationOutcome
    collapsed: tuple[tuple[str, str], ...]
    logs: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "findings": [hit.as_dict() for hit in self.findings],
            "series": [row.as_dict() for row in self.series],
            "calibration": self.calibration.as_dict(),
            "collapsed": [list(pair) for pair in self.collapsed],
            "logs": list(self.logs),
        }


# --------------------------------------------------------------------- the pack


def render_ruling_pack(*, kind: str, coordinate: str, exchange: str,
                       original: JudgeRuling | None = None,
                       instruction: str = "") -> bytes:
    """The audit re-ruling pack for one coordinate, byte-stable.

    One renderer for all four arms, so no arm invents its own prompt: the
    rubric's relation body and the instrument's banner are imported from
    ``standard`` and never retyped; the exchange under re-ruling and the
    ruling under audit (verbatim) are the only model-facing variables. The
    pack carries no label, no status and no adjudication key, exactly as a
    trial pack may not.
    """
    blocks = [
        f"audit: {kind} on {coordinate}",
        "",
        READING_BANNER,
        "",
        RUBRIC_V1["relation"].body,
        "",
        "--- the exchange under re-ruling ---",
        exchange,
    ]
    if original is not None:
        blocks += [
            "",
            "--- the ruling under audit, reproduced verbatim ---",
            f"sustained: {original.sustained}",
            f"decisive_point: {original.decisive_point}",
            f"reading_note: {original.reading_note}",
        ]
    if instruction:
        blocks += ["", instruction]
    blocks += [
        "",
        "Return one JSON object with the fields sustained, decisive_point and "
        "reading_note.",
    ]
    return "\n".join(blocks).encode("utf-8")


# --------------------------------------------------------------------- the set


#: The constructed exchanges of the five shipped anchors, fixed at pin time.
#: Built so each anchor's claim about its pair holds before any reading:
#: "true by construction" is a property of the bytes, not of a seat's answer.
_ANCHOR_EXCHANGES: Mapping[str, tuple[str, str]] = MappingProxyType({
    "self-juxtaposition": (
        "case: the record o1 disputes that the proposal answers the objection "
        "and says so in its own terms; the target is o1 itself. Does o1 retain "
        "its own content?",
        "answer: the juxtaposition is o1 against o1; retaining is the identity "
        "reading, and no further ground is asked for.",
    ),
    "no-shared-reference": (
        "case: the referring record describes a drainage budget for the south "
        "field and the target record is a recipe for bread; nothing in either "
        "binds a role in the other.",
        "answer: there is no shared reference, no quotation and no preserved "
        "binding; the critic's answer is none.",
    ),
    "quotes-and-rejects": (
        "case: the record quotes the target verbatim - 'the objection is "
        "discharged by the repair' - and states a ground for declining it.",
        "answer: the quotation supplies the passage and the stated ground "
        "supplies the reason; the reading is rejects-with-reason.",
    ),
    "clean-control-lexical-overlap-only": (
        "case: the referring record and the target record share the words "
        "'objection', 'repair' and 'discharge'; there is no reference, no "
        "quotation and no preserved role binding between them.",
        "answer: a lexical overlap is not evidence of use; no relation from the "
        "vocabulary is established here.",
    ),
    "clean-control-framing-only-passage": (
        "case: the only span that could be cited sits in the pack's own "
        "banner - 'the tool records juxtapositions' - and not in the material; "
        "the candidate passage is the framing.",
        "answer: a reading grounded in the prompt's own scaffolding is not a "
        "reading of the material; the operative-target check declines it.",
    ),
})


#: The sha256 of the constructed exchange table above, so "the set is fixed at
#: pin time" is a checkable statement rather than a promise. The *anchors* are
#: pinned by ``standard.STANDARD_BODY_SHA256``; their exchange bytes are not in
#: the standard body (design 2.1 says the standard carries "anchor exemplars",
#: and ``standard.CalibrationAnchor`` carries a construction and a ground-truth
#: reason but no exchange), so the bytes are pinned here and the gap is recorded
#: for the bundle reviser in ``WAVE3-INTERFACE.md``.
CALIBRATION_EXCHANGES_SHA256 = hashlib.sha256(
    "\n".join(f"{anchor}\u0000{case}\u0000{answer}"
              for anchor, (case, answer) in sorted(_ANCHOR_EXCHANGES.items())
              ).encode("utf-8")).hexdigest()


def _anchor_rows(standard: Any) -> tuple[Mapping[str, Any], ...]:
    """The calibration anchor rows of a standard, whatever form it arrived in."""
    from . import standard as _standard_mod

    if isinstance(standard, (bytes, bytearray, str)):
        return tuple(_standard_mod.standard_body(standard)["calibration_anchors"])
    if isinstance(standard, Mapping):
        rows = standard.get("calibration_anchors")
        if rows is None:
            raise _fail(
                "CONFIG_INVALID_VALUE",
                "a standard mapping carries no calibration_anchors")
        return tuple(rows)
    return tuple(anchor.as_json() for anchor in standard)


def build_calibration_set(standard: bytes | str | Mapping[str, Any] | Sequence[Any],
                          ) -> list[CalibrationCase]:
    """The planted-flaw calibration set, seeded by the standard's anchors.

    True by construction: each row's ground truth is the anchor's
    ``must_sustain`` from the registered standard body, and the exchange bytes
    are the fixed constructions beside it. The set is seeded once - at
    PREREGISTER - and is fixed by the plan pin; it is never regrown at audit
    time. A clean control (``must_sustain`` false) that a seat sustains is an
    error, exactly as a must-sustain anchor a seat declines is.
    """
    rows: list[CalibrationCase] = []
    for anchor in _anchor_rows(standard):
        anchor_id = str(anchor["id"])
        if anchor_id not in _ANCHOR_EXCHANGES:
            raise _fail(
                "CONFIG_INVALID_VALUE",
                f"no constructed exchange for anchor {anchor_id!r}; the set is "
                "fixed at pin time and a new anchor is a successor standard")
        case, answer = _ANCHOR_EXCHANGES[anchor_id]
        rows.append(CalibrationCase(
            anchor=anchor_id,
            case=case,
            answer=answer,
            expected_sustained=bool(anchor["must_sustain"]),
            expected_relation=anchor["expected_relation"],
            construction=str(anchor["construction"]),
            ground_truth_reason=str(anchor["ground_truth_reason"]),
        ))
    return rows


# --------------------------------------------------------------------- the arms


def _register_hit(harness: Any, *, kind: str, seat: str, coordinate: str,
                  detail: str, body: Mapping[str, Any]) -> AuditHit:
    """Register one finding and keep what it became.

    ``graph.register_audit_warrant`` mints one warrant per validity node in
    the seat's window, all carried by the one finding artifact and all sharing
    the finding's own ``nu_audit`` - so the finding is attackable exactly
    where the readings it collapsed were.
    """
    targets = graph.validity_nodes_for_seat(harness, seat)
    finding_id = graph.register_audit_warrant(harness, graph.AuditFinding(
        seat=seat, kind=kind, detail=detail, targets=targets,
        body=dict(body, window=list(targets))))
    return AuditHit(kind=kind, seat=seat, coordinate=coordinate, detail=detail,
                    finding_id=finding_id, targets=targets)


def _readings(harness: Any, readings: Sequence[str],
              ) -> tuple[tuple[str, Mapping[str, Any]], ...]:
    """The named reading bodies, in the order named.

    Through ``graph.reading_bodies``: the reading body's shape is W1-GRAPH's and
    a second decoder here would be a parallel bookkeeping of it. A name that is
    not a registered reading contributes nothing - an absent window audits as
    nothing rather than as a refusal.
    """
    return graph.reading_bodies(harness, readings)


def _panel(harness: Any, panel: Sequence[str] | None) -> tuple[str, ...]:
    """The seats this audit asks, in order, with no spelling invented here.

    An explicit ``panel`` is the driver's - the labels the pinned seat plan
    froze. Without one the panel is :data:`PANEL_ON_RECORD`: the seats that
    carry a ``nu_soundness`` in this graph, which are exactly the seats whose
    readings a hit can collapse. Duplicates are dropped and order is kept.
    """
    source = panel if panel is not None else graph.seats_on_record(harness)
    seen: list[str] = []
    for seat in source:
        if not isinstance(seat, str) or not seat.strip():
            raise _fail("CONFIG_INVALID_VALUE", "a panel member is a non-empty seat label")
        if seat not in seen:
            seen.append(seat)
    return tuple(seen)


def _exchange(harness: Any, body: Mapping[str, Any]) -> tuple[str, str]:
    transcript = graph.reading_transcript(harness, body) or {}
    case = transcript.get("case", "")
    answer = transcript.get("answer", "")
    return (case if isinstance(case, str) else "",
            answer if isinstance(answer, str) else "")


def _original_ruling(harness: Any, body: Mapping[str, Any]) -> JudgeRuling | None:
    """The ruling on record, read back out of the transcript blob.

    The vendored transcript spells a sustained trial's ruling ``verdict:
    "fail"`` - a fail on the cell's commitment is the sustained reading - so
    ``sustained`` is rebuilt from that spelling and never retyped elsewhere.
    """
    transcript = graph.reading_transcript(harness, body)
    if not isinstance(transcript, Mapping):
        return None
    ruling = transcript.get("ruling")
    if not isinstance(ruling, Mapping):
        return None
    point = ruling.get("decisive_point", "")
    if not isinstance(point, str) or not point:
        return None
    return JudgeRuling(
        sustained=ruling.get("verdict") == "fail",
        decisive_point=point,
        reading_note=str(transcript.get("reading_note", "")),
    )


def _paraphrase_of(case: str, answer: str) -> str:
    """The deterministic paraphrase of one exchange - a program, not a model.

    The spot-check re-asks the seat on a restatement the seat did not write,
    which is what makes a flip evidence about the seat rather than about the
    prompt.
    """
    return ("Restated: " + " ".join(case.split())
            + " / On the defence: " + " ".join(answer.split()))


def paraphrase_invariance(
    harness: Any,
    judge_caller: Callable[..., Any],
    readings: Sequence[str],
) -> list[AuditHit]:
    """Re-rule each logged exchange on a fresh paraphrase of it; a flip is a hit.

    For each named reading on record the exchange is read off the transcript,
    the seat is asked to rule again on a deterministic paraphrase of the
    *exchange* (never of the material - 2.4 G7's boundary), and a ruling that
    disagrees with the one on record registers a finding against that seat's
    whole window. A seat that did not answer is a delivery fact, never a hit.
    """
    hits: list[AuditHit] = []
    for _reading_id, body in _readings(harness, readings):
        seat = str(body.get("seat", ""))
        key = str(body.get("key", ""))
        if not seat or not key:
            continue
        case, answer = _exchange(harness, body)
        original = _original_ruling(harness, body)
        if original is None:
            continue
        pack = render_ruling_pack(
            kind="paraphrase-invariance", coordinate=key,
            exchange=_paraphrase_of(case, answer), original=original,
            instruction=("The exchange above is a paraphrase of the one the "
                         "ruling below was returned on."))
        coordinate = f"audit-pva/{key}"
        again = _ruling(judge_caller(seat, pack, coordinate))
        if again is None:
            continue        # a delivery fact about the route, never a reading
        if again.sustained != original.sustained:
            hits.append(_register_hit(
                harness, kind="paraphrase-invariance", seat=seat,
                coordinate=key,
                detail=(f"the seat ruled {original.sustained} on the logged "
                        f"exchange and {again.sustained} on a paraphrase of it"),
                body={"coordinate": coordinate,
                      "original_sustained": original.sustained,
                      "paraphrase_sustained": again.sustained}))
    return hits


def premise_deletion(
    harness: Any,
    judge_caller: Callable[..., Any],
    readings: Sequence[str],
) -> list[AuditHit]:
    """Delete the cited ``decisive_point`` from the exchange and re-rule.

    A sustained ruling that survives the removal of its own stated grounds is
    easy to vary and is a hit - design 2.5's premise-deletion arm. A ruling
    that is not on record as sustained (nothing registered) is not audited:
    there is nothing the deletion could falsify. The deleted point is named in
    the detail, so the record says what the ruling claimed and what was
    removed.
    """
    hits: list[AuditHit] = []
    for _reading_id, body in _readings(harness, readings):
        seat = str(body.get("seat", ""))
        key = str(body.get("key", ""))
        if not seat or not key:
            continue
        case, answer = _exchange(harness, body)
        original = _original_ruling(harness, body)
        if original is None or not original.sustained:
            continue
        exchange = f"{case}\n{answer}"
        if exchange.count(original.decisive_point) != 1:
            # G2b held at registration; a re-read that finds otherwise is a
            # custody question about the blob, never an audit finding.
            continue
        pack = render_ruling_pack(
            kind="premise-deletion", coordinate=key,
            exchange=exchange.replace(original.decisive_point, "", 1),
            original=original,
            instruction=("The premise the ruling below cited has been removed "
                         "from the exchange above."))
        coordinate = f"audit-pd/{key}"
        again = _ruling(judge_caller(seat, pack, coordinate))
        if again is None:
            continue
        if again.sustained:
            hits.append(_register_hit(
                harness, kind="premise-deletion", seat=seat, coordinate=key,
                detail=(f"the ruling survived the deletion of its own cited "
                        f"decisive_point {original.decisive_point!r}, which is "
                        "easy to vary and is a hit"),
                body={"coordinate": coordinate,
                      "deleted_point": original.decisive_point}))
    return hits


def planted_flaw_calibration(
    harness: Any,
    judge_caller: Callable[..., Any],
    calibration_set: Sequence[CalibrationCase],
    *,
    panel: Sequence[str] | None = None,
    bound: float | None = None,
    account: str = "",
) -> CalibrationOutcome:
    """Ask the panel the planted-flaw set; past a *declared* bound, Spawn.

    Every anchor is true by construction, so a disagreement between a seat and
    the set is an error the seat made, never a dispute about the material: a
    must-sustain anchor declined, or a clean control sustained - the acceptance
    clause names the second of those. Each error registers its own hit against
    that seat's window through ``graph``, and the hits ride back on the outcome
    so the report can name what collapsed a reading.

    ``bound`` and ``account`` are the frozen config's ``judge_err_max`` and its
    ``judge_err_max_account``, and this function invents neither: called without
    a bound it answers the share and the error set and mints no signal. A
    threshold this module chose for itself would be a margin nobody
    pre-registered, and an account this module wrote would be an account of its
    own arithmetic rather than of the pre-registration's (ruling 7; REVIEW-PREREG
    PR-09, where exactly that account is shown to misstate its own denominator).
    """
    seats = _panel(harness, panel)
    errors: list[str] = []
    exercised: list[str] = []
    hits: list[AuditHit] = []
    for row in calibration_set:
        for seat in seats:
            coordinate = f"audit-cal/{row.anchor}/{seat}"
            pack = render_ruling_pack(
                kind="planted-flaw-calibration", coordinate=coordinate,
                exchange=f"{row.case}\n{row.answer}")
            ruling = _ruling(judge_caller(seat, pack, coordinate))
            if ruling is None:
                continue    # a delivery fact; the anchor went unexercised
            exercised.append(row.anchor)
            if ruling.sustained != row.expected_sustained:
                errors.append(f"{seat}:{row.anchor}")
                hits.append(_register_hit(
                    harness, kind="planted-flaw-calibration", seat=seat,
                    coordinate=coordinate,
                    detail=(f"the seat answered {ruling.sustained} on "
                            f"{row.anchor}, whose ground truth "
                            f"({row.expected_sustained}) is true by "
                            f"construction: {row.ground_truth_reason}"),
                    body={"coordinate": coordinate, "anchor": row.anchor,
                          "expected_sustained": row.expected_sustained,
                          "observed_sustained": ruling.sustained}))
    distinct = sorted(set(exercised))
    if not distinct:
        return CalibrationOutcome(share=None, errors=(), exercised=(),
                                  hits=tuple(hits))
    share = _calibration_share(len(errors), len(exercised))
    spawn: SpawnSignal | None = None
    if share is not None and bound is not None and share > bound:
        spawn = SpawnSignal(
            trigger=SPAWN_AUDIT_THE_CRITIC, observed=share, bound=float(bound),
            account=account, anchors=tuple(distinct))
    return CalibrationOutcome(
        share=share, errors=tuple(errors), exercised=tuple(distinct),
        spawn=spawn, hits=tuple(hits))


def _calibration_bound(config: Any) -> tuple[float, str]:
    """The frozen config's ``judge_err_max`` and the account that justifies it.

    Both are required and neither has a default. ``types.AuditConfig`` already
    says why - "a threshold that appears by default was never pre-registered",
    and "each threshold carries an account, and the account is required" - so a
    fallback here would be a second, unpinned spelling of a pre-registered
    margin. Ruling 7 admits ``judge_err_max`` as a bound on the *instrument*,
    and only on the condition that its firing carries an account; a firing whose
    account this module wrote accounts for nothing.
    """
    block = config.get("audit") if isinstance(config, Mapping) else getattr(config, "audit", None)
    if block is None:
        raise _fail("CONFIG_MISSING_KEY",
                    "an audit pass reads judge_err_max off the frozen config's audit block")
    if isinstance(block, Mapping):
        bound = block.get("judge_err_max")
        account = block.get("judge_err_max_account", "")
    else:
        bound = getattr(block, "judge_err_max", None)
        account = getattr(block, "judge_err_max_account", "")
    if not isinstance(bound, (int, float)) or isinstance(bound, bool):
        raise _fail("CONFIG_MISSING_KEY",
                    "audit.judge_err_max is a declared number and has no default")
    if not isinstance(account, str) or not account.strip():
        raise _fail("CONFIG_INVALID_VALUE",
                    "audit.judge_err_max_account is required prose: a margin whose "
                    "firing carries no account is a bare threshold (ruling 7)")
    return float(bound), account


def _pair_for(body: Mapping[str, Any], panel: Sequence[str]) -> tuple[str, ...]:
    """The two seats the disagreement series asks of one reading.

    The reading's own ``roles`` record names them where a caller supplied it;
    otherwise the panel does. Fewer than two *distinct* seats is not a pair and
    this function says so by answering an empty tuple: one seat's two answers
    are never a variance between two seats, and a second seat invented here
    would make a fabricated pair look like an ensemble.
    """
    named: list[str] = []
    roles_body = body.get("roles")
    if isinstance(roles_body, Mapping):
        for seat in roles_body.values():
            if isinstance(seat, str) and seat and seat not in named:
                named.append(seat)
    if len(named) < 2:
        named = [seat for seat in panel]
    return (named[0], named[1]) if len(named) >= 2 else ()


def disagreement_series(
    harness: Any,
    judge_caller: Callable[..., Any],
    readings: Sequence[str],
    *,
    panel: Sequence[str] | None = None,
) -> tuple[Disagreement, ...]:
    """The ensemble-disagreement series: a measure, never a verdict.

    For each named reading, both seats of the judging pair are re-asked on the
    logged exchange; where the two answers differ the row records ``outcome:
    unresolved``, because a disagreement is unresolved (design 2.4 G5, R10)
    and this arm is never averaged, never vote-counted and never a hit. A seat
    that did not answer contributes ``None``, which is a missing answer and
    never a vote. A reading for which no pair can be named contributes **no
    row**: an ensemble that does not exist is not a row saying it agreed.
    """
    seats = _panel(harness, panel)
    series: list[Disagreement] = []
    for _reading_id, body in _readings(harness, readings):
        key = str(body.get("key", ""))
        if not key:
            continue
        pair = _pair_for(body, seats)
        if not pair:
            continue
        left, right = pair
        case, answer = _exchange(harness, body)
        answers: dict[str, bool | None] = {}
        for member in (left, right):
            coordinate = f"audit-ens/{key}/{member}"
            pack = render_ruling_pack(
                kind="ensemble-disagreement", coordinate=coordinate,
                exchange=f"{case}\n{answer}")
            ruling = _ruling(judge_caller(member, pack, coordinate))
            answers[member] = None if ruling is None else ruling.sustained
        series.append(Disagreement(
            left_seat=left, right_seat=right, coordinate=key,
            left_sustained=answers[left], right_sustained=answers[right]))
    return tuple(series)


def run_audits(
    harness: Any,
    judge_caller: Callable[..., Any],
    readings: Sequence[str],
    config: Any,
    *,
    panel: Sequence[str] | None = None,
) -> AuditReport:
    """One audit pass: both invariant arms, the calibration, the series, and
    the recompute over a reopened harness.

    ``config`` is the frozen loop config or its mapping; the calibration's bound
    and its account are read off ``config.audit`` and nowhere else. ``panel`` is
    the pinned seat plan's labels where the driver has them, and otherwise the
    seats on record. Returns an :class:`AuditReport`; ``calibration.spawn`` is
    the Spawn signal, ``findings`` carries every hit from all three warranting
    arms, and ``collapsed`` is what the reopened graph says fell. ``logs`` is one
    entry per audit coordinate spent, which is the whole of "every audit call
    reached the log exactly once".
    """
    bound, account = _calibration_bound(config)
    seats = _panel(harness, panel)
    before = _standings(harness)
    logs: list[str] = []

    def called(seat: str, pack: bytes, coordinate: str) -> JudgeRuling | None:
        logs.append(coordinate)
        return _ruling(judge_caller(seat, pack, coordinate))

    hits = list(paraphrase_invariance(harness, called, readings))
    hits.extend(premise_deletion(harness, called, readings))
    calibration = planted_flaw_calibration(
        harness, called, build_calibration_set(STANDARD_BODY),
        panel=seats, bound=bound, account=account)
    hits.extend(calibration.hits)
    series = disagreement_series(harness, called, readings, panel=seats)
    after = _standings(graph.open_graph(harness.root))
    collapsed = tuple(
        (key, after.get(key, "")) for key in sorted(set(before) | set(after))
        if before.get(key) != after.get(key))
    return AuditReport(
        schema=AUDITS_SCHEMA, findings=tuple(hits), series=series,
        calibration=calibration, collapsed=collapsed, logs=tuple(logs))


def _standings(harness: Any) -> dict[str, str]:
    """Cell key -> state, read back out of the adjudication and nothing else."""
    return {standing.key: standing.state
            for standing in graph.cell_standings(harness)}


def _calibration_share(errors: int, exercised: int) -> float | None:
    """The error share over the exercised anchors - the one division the
    pre-registration declares: the calibration's own rate, with the exercised
    exercises as its stated denominator, and ``None`` when the denominator is
    empty."""
    if exercised == 0:
        return None
    return errors / exercised
