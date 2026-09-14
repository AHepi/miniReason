"""W2-DECIDE: the pre-registered stop/continue program, and its record.

Purpose
-------
After each cycle the loop asks one question and is allowed exactly one answer:
stop, and under which pre-registered reason, or continue.  This module is that
question written as a program.  It evaluates the guard rails first, then the
five O/P clauses of the design in order, and returns one :class:`Decision`
carrying the reason, the loss registers, the obligations' standing, what moved
in the reading set, the sentences the record must print verbatim, and the
mandatory ``would_reopen`` prose.  :func:`render_decision` turns that into the
cycle's decision record.

It calls no model.  There is no seat here, no pack, no provider and no socket:
the decision is a program over registered artifacts, and
``tests/loop/test_decide.py`` asserts by an import scan that this module
imports neither ``roles`` nor any provider module.

Design of record
----------------
Section 5, "The decision rule - pre-registered, and not a scalar meter".  The
order is the design's own:

* **Guard rails, evaluated before everything and stopping immediately.**  A
  ``HALTED`` step is ``custody_halt``; every arm ended is ``all_arms_ended``; a
  guard-block streak above the declared ``streak_max`` or a calibration error
  above the declared ``judge_err_max`` is ``instrument_fault``, which names a
  fault in the instrument and never a finding about the material.  No guard
  rail reads a cell.
* **Clause 1** - any *p* lost between the two situations: STOP
  ``protected_loss``, the loss named and exposed, no continuation and no repair
  claim.  A protected obligation that became *unreadable* is not a loss; it is
  printed as ``protected_not_evaluable`` beside the loss register (FW5 R5).
* **Clause 2** - an obligation of O that did not hold at the prior situation
  holds now **and** ``ProducedBy`` is discharged, that is, the artifacts making
  it hold were registered by this cycle and withholding them makes it stop
  holding: CONTINUE.  Temporal succession alone is not production (FW5:800).
* **Clause 3** - every *o* satisfied: STOP ``obligations_discharged``.  The
  antecedent is ``Evaluation.every_o_satisfied``, never "no failures", so an
  obligation answering ``not_evaluable`` never terminates the chain.
* **Clause 4** - this cycle's ``(cell, register, mark)`` triples are the same
  **set** as the previous cycle's: STOP ``no_new_reading_changes``.  Set
  identity, exactly the set ``graph.mark_triples`` emits, with no second
  spelling between there and here.
* **Clause 5** - the cycle index has reached the declared budget, or the
  declared call budget is reached: STOP ``resource_boundary``, carrying the
  frozen ceiling's own sentence that a reached ceiling is a declared resource
  boundary and not the inquiry running out.
* Nothing fired: CONTINUE.

``losses_outside_P`` is written every cycle, present even when empty
(FW5:802), and a cycle may be net withdrawal and still be progress (FW5:810) -
which is why the loss register is a section of the record rather than an input
to any clause.  Every stop carries ``would_reopen``.

The hard rule: no clause is a meter
-----------------------------------
No clause reads a quantity of readings, marks, endpoints or ``differs``.  The
module contains no arithmetic operator, no numeric literal outside a subscript,
no ``len``/``sum``/``min``/``max``, and no identifier naming a count, a rate, a
threshold or a score; ``tests/loop/test_decide.py`` asserts all of that over
this file's own syntax tree, exactly as ``tests/loop/test_obligations.py``
asserts it over W1-OBLIGATIONS.

**Exactly three numeric comparisons exist in this module**, each an *instrument
bound* rather than a reading of the material, and each isolated in one named
function so that the clause bodies stay free of them:

1. ``instrument_bound_crossed`` - the guard-block streak against the declared
   ``audit.streak_max``;
2. ``instrument_bound_crossed`` - the calibration error against the declared
   ``audit.judge_err_max``;
3. ``declared_boundary_reached`` - the cycle index against the declared
   ``cycle_budget``.

The first two are panel-level signals about the instrument; both bounds are
pre-registered and both carry the account the config requires beside them, so
the margin is attackable rather than merely declared.  The third is an
attention-and-spend boundary (spec sections 0 and 11), never an adjudication.
Whether the declared call budget is reached is *reported* to this module as a
fact by the driver, for the same reason: reaching it is a spend fact off the
step ledger, not something to be recomputed here.

Deviations from the design of record and from the wave-plan entry
-----------------------------------------------------------------
1. **``decide`` takes one extra keyword-only argument, ``instrument``.**  Three
   of the guard rails - a ``HALTED`` step, every arm ended, the guard-block
   streak and the calibration error - are facts about the *run*, and none of
   them is a registered artifact: ``obligations.RECORD_KINDS`` has no token for
   a step receipt, an arm state, a block register or a calibration report.  The
   design requires the guard rails to be evaluated "never reading a cell", so
   they are reported by W5-DRIVER as an :class:`Instrument` record rather than
   inferred from the graph.  An omitted ``instrument`` is an all-clear one, so
   ``decide`` stays callable with the five positional arguments the wave plan
   names.
2. **``decide`` takes ``prev_triples`` and ``curr_triples``.**  Clause 4
   compares two cycles' mark-triple sets; a :class:`Situation` is a reading of
   the graph's *records* and does not carry them, and the prior cycle's harness
   is not in hand at decision time - its triple set is carried forward in the
   prior decision record.  Both default to ``None``, meaning "not supplied", in
   which case clause 4 cannot fire and the record says so; at cycle 1 there is
   no prior set and the clause is silent by construction.
3. **``situation`` takes the obligations document, and the wave plan's
   two-argument entry cannot be restored** (wave-2 integration, Kimi family-C
   judge finding 1).  The declared entry is ``situation(harness, cycle)``; what
   is implemented is ``situation(harness, cycle, obligations, *,
   registered=())``, and the third argument is required rather than optional
   for a reason that is not convenience:

   * ``obligations`` is a **field** of :class:`obligations.Situation`, not an
     argument of a later call on it.  ``Situation.verdict(o)`` and
     ``Situation.check(o)`` evaluate the predicate O and P name; a situation
     built without them carries no predicates and answers ``not_evaluable`` to
     every question.
   * The obligations document is **not in the graph**.  W1-GRAPH registers the
     standard, the material, the cell-opens, the readings, the validity nodes,
     the warrants, the audits and the appeals; it has no obligations artifact,
     and ``obligations.RECORD_KINDS`` contains no token for one.  ``harness``
     therefore cannot supply what the two-argument entry would have to find.
   * Giving it an **empty default** would be worse than the deviation: a caller
     using the declared spelling would receive a well-formed ``Situation`` that
     discharges nothing, ``decide`` would read "no ``o`` was discharged this
     cycle" off it, and clause 2 would silently never fire.  A missing argument
     is a ``TypeError`` at the call; a silently empty O is a wrong decision in
     a published record.
   * Re-binding O onto a situation inside ``decide`` would make the prior
     situation and the current one evaluable under **different** documents,
     which is exactly what FW5:787 forbids inside one assessment.

   The signature is therefore pinned by test
   (``tests/loop/test_decide.py::TheDeclaredEntryPoints``) rather than restored,
   and this deviation is the record of why.  A wave-3 or wave-5 caller that
   wants the declared spelling gets it by partial application at the driver,
   where the pinned obligations are already in hand.
4. **Clause 5 reads "has reached" and not "equals".**  The design says the
   cycle index *equals* the declared budget; a driver that overshoots by one
   would then never stop, and ``decide`` is required to be total.  The record
   prints the index and the declared budget, so the two readings are
   distinguishable in the record.
5. **``standard`` is imported although the wave plan's ``depends_on`` names
   only W0-TYPES, W1-OBLIGATIONS and W1-GRAPH.**  The resource-boundary
   sentence is the frozen ceiling's, not this module's, and
   :func:`standard.assert_no_exhaustion_claim` is run over every rendered
   record: a boundary described as the inquiry running out is refused here
   rather than at the renderer.  W1-GRAPH already depends on W0-STANDARD, so
   the import graph is unchanged in shape.
6. **The module's own sha256 is exposed as ``DECIDE_SHA256``, under the pin key
   :data:`MODULE_PIN_KEY`.**  Design section 5 puts ``decide.py``'s digest
   inside ``loop_plan_id``; it is computed from this file's bytes at import, so
   it is the value ``custody.pins`` would record for this path and the value
   W5-DRIVER folds into the plan identity at PREREGISTER.  It is **not** a
   member of ``types.PINNED_SOURCE_PATHS``: that constant is wave 0's fixed
   six, and this is one of design 4.2's run-specific pins the caller supplies
   (wave-1 integration decision 28(h)).  :data:`MODULE_PIN_KEY` is the
   repo-relative key it goes in under, published here so the driver does not
   spell the path itself.
7. **No loss is recomputed here.**  ``protected_losses`` and
   ``losses_outside_p`` are W1-OBLIGATIONS', called once each and carried into
   the record whole.
8. **``preregistered_condition:<id>`` is evaluated last, after clause 5**
   (wave-1 integration decision 28(d)).  ``types.STOP_REASONS`` carries it as
   its one parameterised member and ``is_stop_reason`` admits it, but nothing
   in the five clauses can produce one: a pre-registered condition is a
   condition the *pre-registration* declared and the *driver* observes, not a
   reading of the graph.  It arrives on the instrument report as
   ``preregistered_condition``, the bare id, and it is tested **after** clause
   5 and before the open continuation, so that it can mask no clause: a
   protected loss, a discharge, a satisfied O, an identical triple set and the
   declared boundary are all decided first, and a declared condition can only
   stop a chain that no clause had already stopped.  The id may not contain
   ``exhaust`` - ``types.is_stop_reason`` refuses it, because the ceiling's
   denial sentence is not a condition id.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from . import graph as _graph
from . import obligations as _obligations
from . import standard as _standard
from .obligations import Loss, Obligations, Situation, Verdict
from . import types as _types
from .types import STOP_REASONS, LoopConfig, LoopError, is_stop_reason

__all__ = [
    "DECIDE_SCHEMA",
    "DECIDE_SHA256",
    "MODULE_PIN_KEY",
    "NEW_CODES",
    "DECISION_SITUATION_INVALID",
    "DECISION_CYCLE_INVALID",
    "DECISION_CONFIG_INVALID",
    "DECISION_INSTRUMENT_INVALID",
    "DECISION_WOULD_REOPEN_MISSING",
    "DECISION_REASON_UNKNOWN",
    "DecisionRefused",
    "STOP_PROTECTED_LOSS",
    "STOP_OBLIGATIONS_DISCHARGED",
    "STOP_NO_NEW_READING_CHANGES",
    "STOP_RESOURCE_BOUNDARY",
    "STOP_CUSTODY_HALT",
    "STOP_ALL_ARMS_ENDED",
    "STOP_INSTRUMENT_FAULT",
    "CONTINUE_DISCHARGED",
    "CONTINUE_OPEN",
    "CONTINUE_REASONS",
    "CLAUSE_CUSTODY_HALT",
    "CLAUSE_ALL_ARMS_ENDED",
    "CLAUSE_INSTRUMENT_FAULT",
    "CLAUSE_PROTECTED_LOSS",
    "CLAUSE_DISCHARGE",
    "CLAUSE_ALL_SATISFIED",
    "CLAUSE_SET_IDENTITY",
    "CLAUSE_RESOURCE_BOUNDARY",
    "CLAUSE_PREREGISTERED_CONDITION",
    "CLAUSE_NONE",
    "CLAUSE_ORDER",
    "PROTECTED_LOSS_SENTENCE",
    "DISCHARGED_SENTENCE",
    "SET_IDENTITY_SENTENCE",
    "RESOURCE_BOUNDARY_SENTENCE",
    "BLOCK_REGISTER_SENTENCE",
    "CUSTODY_HALT_SENTENCE",
    "ALL_ARMS_ENDED_SENTENCE",
    "INSTRUMENT_FAULT_SENTENCE",
    "CONTINUE_DISCHARGED_SENTENCE",
    "CONTINUE_OPEN_SENTENCE",
    "PREREGISTERED_CONDITION_SENTENCE",
    "NET_WITHDRAWAL_SENTENCE",
    "WHY_NOT_A_METER",
    "ALWAYS_SENTENCES",
    "REASON_SENTENCES",
    "WOULD_REOPEN",
    "WOULD_REOPEN_LABEL",
    "Instrument",
    "Decision",
    "situation",
    "mark_triples",
    "instrument_bound_crossed",
    "declared_boundary_reached",
    "decide",
    "render_decision",
]

#: The decision record's schema token.
DECIDE_SCHEMA = "minireason.loop.decide.v1"

#: This file's own sha256, for ``loop_plan_id`` (design section 5, deviation 6).
DECIDE_SHA256: str = hashlib.sha256(
    Path(__file__).resolve().read_bytes()).hexdigest()

#: The repo-relative key :data:`DECIDE_SHA256` is folded into ``pins`` under at
#: PREREGISTER (wave-1 integration decision 28(h)).  It is a *run-specific* pin
#: of design 4.2's list, supplied by the driver; ``types.PINNED_SOURCE_PATHS``
#: is the fixed six and does not carry it.  Published here so the driver does
#: not retype the path, and so a moved module is a changed key rather than a
#: silently absent pin.
MODULE_PIN_KEY = "src/minireason/loop/decide.py"


# --------------------------------------------------------------------------
# Refusals
# --------------------------------------------------------------------------

DECISION_SITUATION_INVALID = "DECISION_SITUATION_INVALID"
DECISION_CYCLE_INVALID = "DECISION_CYCLE_INVALID"
DECISION_CONFIG_INVALID = "DECISION_CONFIG_INVALID"
DECISION_INSTRUMENT_INVALID = "DECISION_INSTRUMENT_INVALID"
DECISION_WOULD_REOPEN_MISSING = "DECISION_WOULD_REOPEN_MISSING"
DECISION_REASON_UNKNOWN = "DECISION_REASON_UNKNOWN"

#: Every code this module can put on an exception, with the one-line reason it
#: exists.  W0-TYPES folds these into ``types.FAILURE_CODES`` when W2 lands.
NEW_CODES: Mapping[str, str] = MappingProxyType({
    DECISION_SITUATION_INVALID:
        "the cycle-end reading handed to the decision is not a Situation, "
        "or the prior reading is neither a Situation nor absent",
    DECISION_CYCLE_INVALID:
        "the cycle index is not a whole number, so it cannot be compared "
        "with the declared budget",
    DECISION_CONFIG_INVALID:
        "the frozen configuration handed to the decision is neither a "
        "LoopConfig nor a mapping that loads as one",
    DECISION_INSTRUMENT_INVALID:
        "the driver's instrument report is not an Instrument and does not "
        "load as one, so the guard rails cannot be read",
    DECISION_WOULD_REOPEN_MISSING:
        "a stop was built without the mandatory would_reopen prose, which "
        "every stop must carry (design section 5)",
    DECISION_REASON_UNKNOWN:
        "a decision names a reason outside the pre-registered stop vocabulary "
        "and outside this module's two continue reasons",
})


class DecisionRefused(LoopError):
    """A declared refusal of this module.  ``code`` is the stable token."""

    def __init__(self, code: str, detail: str = "") -> None:
        LoopError.__init__(self, code, detail)


# --------------------------------------------------------------------------
# The outcome vocabulary
# --------------------------------------------------------------------------

STOP_PROTECTED_LOSS = "protected_loss"
STOP_OBLIGATIONS_DISCHARGED = "obligations_discharged"
STOP_NO_NEW_READING_CHANGES = "no_new_reading_changes"
STOP_RESOURCE_BOUNDARY = "resource_boundary"
STOP_CUSTODY_HALT = "custody_halt"
STOP_ALL_ARMS_ENDED = "all_arms_ended"
STOP_INSTRUMENT_FAULT = "instrument_fault"

#: The two ways the chain stays open.  Neither is a member of
#: ``types.STOP_REASONS``: a continuation is not a stop under another name.
CONTINUE_DISCHARGED = "obligation_discharged"
CONTINUE_OPEN = "chain_open"
CONTINUE_REASONS: tuple[str, ...] = (CONTINUE_DISCHARGED, CONTINUE_OPEN)

#: Which clause decided, in the design's own order.
CLAUSE_CUSTODY_HALT = "guard_rail_custody_halt"
CLAUSE_ALL_ARMS_ENDED = "guard_rail_all_arms_ended"
CLAUSE_INSTRUMENT_FAULT = "guard_rail_instrument_fault"
CLAUSE_PROTECTED_LOSS = "clause_one_protected_loss"
CLAUSE_DISCHARGE = "clause_two_produced_by_discharge"
CLAUSE_ALL_SATISFIED = "clause_three_every_o_satisfied"
CLAUSE_SET_IDENTITY = "clause_four_set_identity"
CLAUSE_RESOURCE_BOUNDARY = "clause_five_declared_boundary"
#: Evaluated after clause 5 so that it masks nothing (decision 28(d)).
CLAUSE_PREREGISTERED_CONDITION = "declared_condition_after_clause_five"


def _condition_reason(condition_id: str) -> str:
    """``preregistered_condition:<id>``, spelled through the types prefix.

    Written as a format rather than a concatenation because this module's own
    guard (``tests/loop/test_decide.py::NoClauseIsAMeter``) refuses every
    binary operator in this file, so that no reader has to check whether a
    ``+`` was joining prose or adding a quantity.
    """

    return f"{_types.PREREGISTERED_CONDITION_PREFIX}{condition_id}"
CLAUSE_NONE = "no_clause_fired"

CLAUSE_ORDER: tuple[str, ...] = (
    CLAUSE_CUSTODY_HALT,
    CLAUSE_ALL_ARMS_ENDED,
    CLAUSE_INSTRUMENT_FAULT,
    CLAUSE_PROTECTED_LOSS,
    CLAUSE_DISCHARGE,
    CLAUSE_ALL_SATISFIED,
    CLAUSE_SET_IDENTITY,
    CLAUSE_RESOURCE_BOUNDARY,
    CLAUSE_PREREGISTERED_CONDITION,
    CLAUSE_NONE,
)


def _declared() -> None:
    """Every stop token here is a member of the frozen stop vocabulary."""

    for token in (STOP_PROTECTED_LOSS, STOP_OBLIGATIONS_DISCHARGED,
                  STOP_NO_NEW_READING_CHANGES, STOP_RESOURCE_BOUNDARY,
                  STOP_CUSTODY_HALT, STOP_ALL_ARMS_ENDED,
                  STOP_INSTRUMENT_FAULT):
        if token not in STOP_REASONS:
            raise DecisionRefused(DECISION_REASON_UNKNOWN, token)
    for token in CONTINUE_REASONS:
        if is_stop_reason(token):
            raise DecisionRefused(DECISION_REASON_UNKNOWN,
                                  f"{token} is a stop reason, not a continuation")


_declared()


# --------------------------------------------------------------------------
# The sentences the record prints verbatim
# --------------------------------------------------------------------------

def _ceiling_sentence(phrase: str) -> str:
    """The frozen ceiling clause carrying that phrase, verbatim.

    Selected by its own words rather than by position, so a re-ordered ceiling
    does not silently change which sentence a stop prints.
    """

    for sentence in _standard.CEILING_REQUIRED_SENTENCES:
        if phrase in sentence:
            return sentence
    raise DecisionRefused(
        DECISION_REASON_UNKNOWN,
        f"the frozen ceiling carries no clause saying {phrase!r}")


#: The ceiling's own resource-boundary clause: the one that denies the reading
#: this module is forbidden to give a reached ceiling.
RESOURCE_BOUNDARY_SENTENCE: str = _ceiling_sentence(
    _standard.CEILING_EXHAUSTION_DENIAL)

#: The ceiling's block-register clause, printed beside an ``instrument_fault``.
BLOCK_REGISTER_SENTENCE: str = _ceiling_sentence("is the instrument declining to read")

PROTECTED_LOSS_SENTENCE = (
    "A protected obligation held at the prior situation and does not hold now. "
    "The chain stops here, the loss is named below, and this record makes no "
    "claim that it was repaired."
)

DISCHARGED_SENTENCE = (
    "Every obligation of O is satisfied. The chain stops because what it was "
    "opened to discharge is discharged; this clause terminates the chain and "
    "does not reward it."
)

SET_IDENTITY_SENTENCE = (
    "This cycle's (cell, register, mark) triples are the same set as the "
    "previous cycle's. The comparison is set identity: which triples moved is "
    "the whole reading, and nothing here was enumerated or read as a magnitude."
)

CUSTODY_HALT_SENTENCE = (
    "A step halted under custody. The halt is sticky until it is acknowledged "
    "with a recorded reason, and nothing this cycle produced stands on the "
    "halted step."
)

ALL_ARMS_ENDED_SENTENCE = (
    "Every arm ended before the cycle closed. What the arms did not reach is "
    "unread, and an unread cell is silent about content."
)

INSTRUMENT_FAULT_SENTENCE = (
    "This is a fault in the instrument, not a finding about the material. The "
    "reading arm stops and an audit of the reader is spawned; what the "
    "instrument declined to read stays unread."
)

CONTINUE_DISCHARGED_SENTENCE = (
    "An obligation of O that did not hold at the prior situation holds now, "
    "and the artifacts that make it hold were registered by this cycle and are "
    "what makes it hold. The chain continues because something was built, not "
    "because time passed."
)

CONTINUE_OPEN_SENTENCE = (
    "No clause stopped the chain: nothing of O was discharged this cycle, O is "
    "not wholly satisfied, the reading set moved or was not compared, and the "
    "declared boundary is not reached."
)

PREREGISTERED_CONDITION_SENTENCE = (
    "A condition this run pre-registered before cycle one was observed by the "
    "driver and stopped the chain. It was evaluated after every clause, so it "
    "masked none of them, and it is a declared condition rather than a reading "
    "of any cell."
)

NET_WITHDRAWAL_SENTENCE = (
    "A cycle may be net withdrawal and still be progress, and it may add and "
    "still be no progress. The register below is written every cycle, present "
    "even when it is empty."
)

WHY_NOT_A_METER = (
    "No clause of this program reads a magnitude. Clause four compares two "
    "sets for identity and clause five compares the cycle index with the "
    "declared budget; nothing else in this decision is numeric."
)

#: Printed on every record, stop or continue.
ALWAYS_SENTENCES: tuple[str, ...] = (WHY_NOT_A_METER, NET_WITHDRAWAL_SENTENCE)

#: reason -> the sentences that reason requires, before the always-printed two.
REASON_SENTENCES: Mapping[str, tuple[str, ...]] = MappingProxyType({
    STOP_PROTECTED_LOSS: (PROTECTED_LOSS_SENTENCE,),
    STOP_OBLIGATIONS_DISCHARGED: (DISCHARGED_SENTENCE,),
    STOP_NO_NEW_READING_CHANGES: (SET_IDENTITY_SENTENCE,),
    STOP_RESOURCE_BOUNDARY: (RESOURCE_BOUNDARY_SENTENCE,),
    STOP_CUSTODY_HALT: (CUSTODY_HALT_SENTENCE,),
    STOP_ALL_ARMS_ENDED: (ALL_ARMS_ENDED_SENTENCE,),
    STOP_INSTRUMENT_FAULT: (INSTRUMENT_FAULT_SENTENCE, BLOCK_REGISTER_SENTENCE),
    CONTINUE_DISCHARGED: (CONTINUE_DISCHARGED_SENTENCE,),
    CONTINUE_OPEN: (CONTINUE_OPEN_SENTENCE,),
    # Keyed by the PREFIX, because the reason carries the condition's id.
    _types.PREREGISTERED_CONDITION_PREFIX: (PREREGISTERED_CONDITION_SENTENCE,),
})

WOULD_REOPEN_LABEL = "What would reopen this:"

#: The default ``would_reopen`` prose per reason.  A driver may supply its own
#: on the instrument report; it may not supply none.
WOULD_REOPEN: Mapping[str, str] = MappingProxyType({
    STOP_PROTECTED_LOSS:
        "A custody correction, or a successful attack on whatever withdrew the "
        "artifact the protected obligation stood on, would restore it and "
        "reopen the chain.",
    STOP_OBLIGATIONS_DISCHARGED:
        "A successful attack on the standard, on a register definition, or on "
        "any reading that discharged an obligation collapses it again; a new "
        "obligation added to O is a new pre-registration and a new chain.",
    STOP_NO_NEW_READING_CHANGES:
        "Any of the declared reopen reasons would move the triple set and "
        "reopen the chain.",
    STOP_RESOURCE_BOUNDARY:
        "A new pre-registration declaring a wider boundary would reopen it. "
        "The cells this run did not reach are unread, and the record says "
        "which they are.",
    STOP_CUSTODY_HALT:
        "Correcting the custody defect, writing the erratum and acknowledging "
        "the halt with a recorded reason would reopen the chain.",
    STOP_ALL_ARMS_ENDED:
        "A delivery route that stays open for a whole cycle would reopen it; "
        "the arms that ended carried no reading away with them.",
    STOP_INSTRUMENT_FAULT:
        "An audit of the reader that clears the fault, or a repaired guard, "
        "would reopen the reading arm.",
    CONTINUE_DISCHARGED:
        "The chain is open; this record states what it discharged and on which "
        "artifacts that discharge stands.",
    CONTINUE_OPEN:
        "The chain is open; this record states what it did not discharge.",
    _types.PREREGISTERED_CONDITION_PREFIX:
        "The pre-registered condition named in the reason no longer obtaining "
        "would reopen the chain; so would a new pre-registration that does not "
        "declare it. The cells this run did not reach are unread.",
})


def _reason_key(reason: str) -> str:
    """The table key for a reason, folding the one parameterised member.

    ``preregistered_condition:<id>`` carries its id in the token, so the two
    prose tables are keyed by the prefix and every other reason is its own key.
    """

    if str(reason).startswith(_types.PREREGISTERED_CONDITION_PREFIX):
        return _types.PREREGISTERED_CONDITION_PREFIX
    return reason


# --------------------------------------------------------------------------
# What the driver reports that the graph does not hold
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Instrument:
    """The guard rails' facts, reported by W5-DRIVER (deviation 1).

    None of these is a reading of the material and none is read off a cell: a
    halted step and an ended arm are custody and delivery facts off the step
    ledger, the block streak is the guard's own register, and the calibration
    error is the audit panel's.  Every field is optional and an omitted
    instrument report is an all-clear one, so ``decide`` stays total.
    """

    custody_halted: bool = False
    arms_ended: bool = False
    block_streak: int | None = None
    judge_err_observed: float | None = None
    calls_reached: bool = False
    halted_step: str = ""
    ended_arms: tuple[str, ...] = ()
    would_reopen: str = ""
    detail: str = ""
    #: The bare id of a pre-registered condition the driver observed, or "".
    #: ``decide`` tests it after clause 5 so that it masks nothing (28(d)); the
    #: reason it produces is ``preregistered_condition:<id>``, which
    #: ``types.is_stop_reason`` admits and which refuses an id carrying
    #: ``exhaust``.
    preregistered_condition: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "ended_arms",
                           tuple(str(value) for value in self.ended_arms))
        object.__setattr__(self, "preregistered_condition",
                           str(self.preregistered_condition).strip())
        if self.preregistered_condition and not is_stop_reason(
                _condition_reason(self.preregistered_condition)):
            raise DecisionRefused(
                DECISION_INSTRUMENT_INVALID,
                f"{self.preregistered_condition!r} is not a usable "
                "pre-registered condition id")

    @classmethod
    def of(cls, value: Any) -> "Instrument":
        """An Instrument, its mapping form, or absence."""

        if value is None:
            return cls()
        if isinstance(value, Instrument):
            return value
        if isinstance(value, Mapping):
            unknown = tuple(sorted(set(value).difference(_INSTRUMENT_FIELDS)))
            if unknown:
                raise DecisionRefused(
                    DECISION_INSTRUMENT_INVALID,
                    f"the instrument report names {unknown}")
            return cls(**dict(value))
        raise DecisionRefused(DECISION_INSTRUMENT_INVALID,
                              f"{type(value).__name__} is not an instrument report")

    def as_dict(self) -> dict[str, Any]:
        return {
            "custody_halted": self.custody_halted,
            "arms_ended": self.arms_ended,
            "block_streak": self.block_streak,
            "judge_err_observed": self.judge_err_observed,
            "calls_reached": self.calls_reached,
            "halted_step": self.halted_step,
            "ended_arms": list(self.ended_arms),
            "would_reopen": self.would_reopen,
            "detail": self.detail,
            "preregistered_condition": self.preregistered_condition,
        }


_INSTRUMENT_FIELDS: frozenset[str] = frozenset({
    "custody_halted", "arms_ended", "block_streak", "judge_err_observed",
    "calls_reached", "halted_step", "ended_arms", "would_reopen", "detail",
    "preregistered_condition",
})


# --------------------------------------------------------------------------
# The two named bound comparisons, and nothing numeric outside them
# --------------------------------------------------------------------------

def instrument_bound_crossed(instrument: Instrument, config: LoopConfig) -> str:
    """Has a declared **instrument bound** been crossed?  Prose, or empty.

    This is one of the two functions in this module that compares numbers, and
    it compares only bounds on the *instrument*: the guard-block streak against
    the pre-registered ``audit.streak_max`` and the calibration error against
    the pre-registered ``audit.judge_err_max``.  Both are panel-level signals
    that the reader has stopped reading and started declining; neither is a
    reading of any cell, neither is computed per seat, and crossing one names
    ``instrument_fault``, which is a fault in the instrument and never a
    finding about the material.

    Each bound carries the account the config requires beside it, so the margin
    is rendered attackable rather than merely declared (R9).  A bound the
    driver did not report is not crossed: absence of a report is not a reading.
    """

    streak = instrument.block_streak
    if streak is not None and streak > config.audit.streak_max:
        return (f"the guard-block streak reached {streak}, above the declared "
                f"bound {config.audit.streak_max}: "
                f"{config.audit.streak_max_account}")
    observed = instrument.judge_err_observed
    if observed is not None and observed > config.audit.judge_err_max:
        return (f"the calibration error reached {observed}, above the declared "
                f"bound {config.audit.judge_err_max}: "
                f"{config.audit.judge_err_max_account}")
    return ""


def declared_boundary_reached(cycle_index: int, config: LoopConfig,
                              instrument: Instrument) -> str:
    """Has the declared resource boundary been reached?  Prose, or empty.

    The other numeric comparison: the cycle index against the pre-registered
    ``cycle_budget``.  This is an attention-and-spend boundary and never an
    adjudication - the design says so in as many words, and the ceiling's own
    sentence, printed on every such stop, says a reached ceiling is a declared
    resource boundary.

    Whether the declared call budget is reached is *reported* on the instrument
    rather than recomputed here: it is a spend fact off the step ledger, and
    this module holds no ledger.
    """

    if cycle_index >= config.cycle_budget:
        return (f"the cycle index {cycle_index} reached the declared budget "
                f"{config.cycle_budget}")
    if instrument.calls_reached:
        return (f"the declared call budget {config.max_calls} was reached "
                "before the cycle budget")
    return ""


# --------------------------------------------------------------------------
# The decision
# --------------------------------------------------------------------------

Triple = tuple[str, str, str]


@dataclass(frozen=True)
class Decision:
    """Exactly one outcome, with everything the cycle record must print."""

    cycle: int
    stop: bool
    reason: str
    clause: str
    would_reopen: str
    detail: str = ""
    obligations_pin: str = ""
    record_sentences: tuple[str, ...] = ()
    protected_losses: tuple[Loss, ...] = ()
    protected_not_evaluable: tuple[str, ...] = ()
    losses_outside_p: tuple[Loss, ...] = ()
    discharged: tuple[str, ...] = ()
    failed: tuple[str, ...] = ()
    not_evaluable: tuple[str, ...] = ()
    triples_compared: bool = False
    triples_identical: bool = False
    triples_entered: tuple[Triple, ...] = ()
    triples_left: tuple[Triple, ...] = ()

    def __post_init__(self) -> None:
        if self.stop:
            if not is_stop_reason(self.reason):
                raise DecisionRefused(DECISION_REASON_UNKNOWN, self.reason)
            if not str(self.would_reopen).strip():
                raise DecisionRefused(DECISION_WOULD_REOPEN_MISSING, self.reason)
        elif self.reason not in CONTINUE_REASONS:
            raise DecisionRefused(DECISION_REASON_UNKNOWN, self.reason)
        if self.clause not in CLAUSE_ORDER:
            raise DecisionRefused(DECISION_REASON_UNKNOWN, self.clause)
        for name in ("record_sentences", "protected_not_evaluable", "discharged",
                     "failed", "not_evaluable"):
            object.__setattr__(self, name,
                               tuple(str(value) for value in getattr(self, name)))
        for name in ("protected_losses", "losses_outside_p"):
            object.__setattr__(self, name, tuple(getattr(self, name)))
        for name in ("triples_entered", "triples_left"):
            object.__setattr__(self, name, _ordered(getattr(self, name)))

    @property
    def continues(self) -> bool:
        """The chain is open.  The complement of :attr:`stop`, spelled once."""
        return not self.stop

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": DECIDE_SCHEMA,
            "decide_sha256": DECIDE_SHA256,
            "cycle": self.cycle,
            "stop": self.stop,
            "reason": self.reason,
            "clause": self.clause,
            "detail": self.detail,
            "obligations_pin": self.obligations_pin,
            "would_reopen": self.would_reopen,
            "record_sentences": list(self.record_sentences),
            "protected_losses": [loss.as_dict() for loss in self.protected_losses],
            "protected_not_evaluable": list(self.protected_not_evaluable),
            "losses_outside_P": [loss.as_dict() for loss in self.losses_outside_p],
            "discharged": list(self.discharged),
            "failed": list(self.failed),
            "not_evaluable": list(self.not_evaluable),
            "mark_triples": {
                "compared": self.triples_compared,
                "identical": self.triples_identical,
                "entered": [list(item) for item in self.triples_entered],
                "left": [list(item) for item in self.triples_left],
            },
        }


def _ordered(triples: Iterable[Triple]) -> tuple[Triple, ...]:
    return tuple(sorted(tuple(str(part) for part in item) for item in triples))


# --------------------------------------------------------------------------
# The two readings the decision quantifies over
# --------------------------------------------------------------------------

def situation(harness: Any, cycle: int, obligations: Obligations,
              *, registered: Any = ()) -> Situation:
    """The cycle-end reading of the graph, under the pinned obligations.

    A thin, declared seam onto ``obligations.Situation.from_harness``: it reads
    the two-pass adjudication's own labels and writes nothing.  ``registered``
    is this cycle's registration record - either an iterable of artifact ids or
    a ``graph.Production`` - and an empty one discharges nothing.
    """

    ids = getattr(registered, "artifact_ids", registered)
    return Situation.from_harness(harness, cycle=cycle, obligations=obligations,
                                  registered=ids)


def mark_triples(harness: Any) -> frozenset[Triple]:
    """The ``(cell, register, mark)`` set clause 4 compares, from W1-GRAPH.

    Delegation, not a second spelling: wave-1 integration decision 4 states
    that ``graph.mark_triples``' return value *is* the identity this module
    compares, with no normalisation between there and here.  A register cell
    standing at its unresolved default contributes its ``unresolved`` triple; a
    contested or unsupported cell contributes none; a relation cell contributes
    none.
    """

    return _graph.mark_triples(harness)


# --------------------------------------------------------------------------
# The program
# --------------------------------------------------------------------------

def _config_of(config: Any) -> LoopConfig:
    if isinstance(config, LoopConfig):
        return config
    if isinstance(config, Mapping):
        return LoopConfig.from_mapping(config)
    raise DecisionRefused(DECISION_CONFIG_INVALID,
                          f"{type(config).__name__} is not a loop configuration")


def _cycle_of(cycle_index: Any) -> int:
    if isinstance(cycle_index, bool) or not isinstance(cycle_index, int):
        raise DecisionRefused(DECISION_CYCLE_INVALID,
                              f"{cycle_index!r} is not a cycle index")
    return cycle_index


def _situations(prev: Any, curr: Any) -> None:
    if not isinstance(curr, Situation):
        raise DecisionRefused(DECISION_SITUATION_INVALID,
                              "the cycle-end reading must be a Situation")
    if prev is not None and not isinstance(prev, Situation):
        raise DecisionRefused(DECISION_SITUATION_INVALID,
                              "the prior reading must be a Situation or absent")


def _triples_of(value: Any) -> frozenset[Triple] | None:
    if value is None:
        return None
    return frozenset(tuple(str(part) for part in item) for item in value)


def _failed_at_prior(before: Any, obligation_id: str) -> bool:
    """Did that obligation fail at the prior situation?

    Before cycle 1 there is no prior situation and nothing had been discharged,
    so every obligation of O counts as failed there - which is the reading that
    lets the first cycle continue on what it built.
    """

    if before is None:
        return True
    return before.verdict(obligation_id) is not Verdict.SATISFIED


def decide(prev: Situation | None, curr: Situation, cycle_index: int,
           config: LoopConfig | Mapping[str, Any], obligations: Obligations,
           *, instrument: Instrument | Mapping[str, Any] | None = None,
           prev_triples: Iterable[Triple] | None = None,
           curr_triples: Iterable[Triple] | None = None) -> Decision:
    """The guard rails, then the five clauses in order.  Exactly one outcome.

    Total: for any well-formed arguments it returns one :class:`Decision`,
    whose ``reason`` is a member of ``types.STOP_REASONS`` when it stops and of
    :data:`CONTINUE_REASONS` when it does not.  Pure: it reads the two
    situations, the frozen config, the pinned obligations and the driver's
    instrument report, and writes nothing anywhere.
    """

    _situations(prev, curr)
    cycle = _cycle_of(cycle_index)
    settings = _config_of(config)
    reported = Instrument.of(instrument)
    if not isinstance(obligations, Obligations):
        raise DecisionRefused(DECISION_SITUATION_INVALID,
                              "decide() takes a loaded Obligations")

    after = _obligations.evaluate(obligations, curr)
    before = _obligations.evaluate(obligations, prev) if prev is not None else None
    protected = tuple(_obligations.protected_losses(prev, curr))
    outside = tuple(_obligations.losses_outside_p(prev, curr))
    earlier = _triples_of(prev_triples)
    now = _triples_of(curr_triples)

    shared: dict[str, Any] = {
        "cycle": cycle,
        "obligations_pin": after.pin,
        "protected_losses": protected,
        "protected_not_evaluable": after.protected_not_evaluable,
        "losses_outside_p": outside,
        "discharged": after.discharged,
        "failed": after.failed,
        "not_evaluable": after.not_evaluable,
    }
    if earlier is not None and now is not None:
        shared["triples_compared"] = True
        shared["triples_identical"] = earlier == now
        shared["triples_entered"] = _ordered(now.difference(earlier))
        shared["triples_left"] = _ordered(earlier.difference(now))

    # -- guard rails, before every clause and never reading a cell ----------
    if reported.custody_halted:
        return _stop(STOP_CUSTODY_HALT, CLAUSE_CUSTODY_HALT, reported,
                     reported.detail or reported.halted_step, shared)
    if reported.arms_ended:
        return _stop(STOP_ALL_ARMS_ENDED, CLAUSE_ALL_ARMS_ENDED, reported,
                     reported.detail or ", ".join(reported.ended_arms), shared)
    crossed = instrument_bound_crossed(reported, settings)
    if crossed:
        return _stop(STOP_INSTRUMENT_FAULT, CLAUSE_INSTRUMENT_FAULT, reported,
                     crossed, shared)

    # -- clause 1: a protected obligation was lost --------------------------
    if protected:
        lost = ", ".join(loss.subject for loss in protected)
        return _stop(STOP_PROTECTED_LOSS, CLAUSE_PROTECTED_LOSS, reported,
                     f"the protected obligations lost here are {lost}", shared)

    # -- clause 2: an o failed at the prior reading and this cycle built it --
    produced = tuple(identifier for identifier in after.discharged
                     if _failed_at_prior(before, identifier))
    if produced:
        return _continue(CONTINUE_DISCHARGED, CLAUSE_DISCHARGE, reported,
                         f"this cycle discharged {', '.join(produced)}", shared)

    # -- clause 3: every o satisfied ----------------------------------------
    if after.every_o_satisfied:
        return _stop(STOP_OBLIGATIONS_DISCHARGED, CLAUSE_ALL_SATISFIED, reported,
                     "every obligation of O is satisfied at this reading", shared)

    # -- clause 4: the same set of triples as the previous cycle ------------
    if shared.get("triples_identical"):
        return _stop(STOP_NO_NEW_READING_CHANGES, CLAUSE_SET_IDENTITY, reported,
                     "the two cycles' triple sets are identical", shared)

    # -- clause 5: the declared boundary ------------------------------------
    reached = declared_boundary_reached(cycle, settings, reported)
    if reached:
        return _stop(STOP_RESOURCE_BOUNDARY, CLAUSE_RESOURCE_BOUNDARY, reported,
                     reached, shared)

    # -- after clause 5: a condition the pre-registration declared ----------
    # Last, so that it masks nothing (28(d)): every clause above has already
    # had its say, and a declared condition can only stop a chain no clause
    # had stopped. It is the driver's observation, never a reading of a cell.
    if reported.preregistered_condition:
        return _stop(_condition_reason(reported.preregistered_condition),
                     CLAUSE_PREREGISTERED_CONDITION, reported,
                     "the pre-registered condition "
                     f"{reported.preregistered_condition} was observed by the "
                     "driver after every clause had been evaluated", shared)

    return _continue(CONTINUE_OPEN, CLAUSE_NONE, reported,
                     "no clause fired at this reading", shared)


def _stop(reason: str, clause: str, instrument: Instrument, detail: str,
          shared: Mapping[str, Any]) -> Decision:
    key = _reason_key(reason)
    return Decision(stop=True, reason=reason, clause=clause, detail=detail,
                    would_reopen=instrument.would_reopen or WOULD_REOPEN[key],
                    record_sentences=(*REASON_SENTENCES[key], *ALWAYS_SENTENCES),
                    **shared)


def _continue(reason: str, clause: str, instrument: Instrument, detail: str,
              shared: Mapping[str, Any]) -> Decision:
    key = _reason_key(reason)
    return Decision(stop=False, reason=reason, clause=clause, detail=detail,
                    would_reopen=instrument.would_reopen or WOULD_REOPEN[key],
                    record_sentences=(*REASON_SENTENCES[key], *ALWAYS_SENTENCES),
                    **shared)


# --------------------------------------------------------------------------
# The record
# --------------------------------------------------------------------------

EMPTY_SECTION = "- none"
NOT_COMPARED = "- the prior cycle's triples were not supplied, so clause four was silent"


def _section(title: str, rows: Sequence[str]) -> list[str]:
    body = [f"## {title}", ""]
    body.extend(rows if rows else [EMPTY_SECTION])
    body.append("")
    return body


def _loss_rows(losses: Sequence[Loss]) -> list[str]:
    return [f"- {loss.kind}: {loss.subject} was {loss.was}, now {loss.now}"
            f" [{loss.membership or 'outside P'}] - {loss.detail}"
            for loss in losses]


def _id_rows(identifiers: Sequence[str]) -> list[str]:
    return [f"- {identifier}" for identifier in identifiers]


def _triple_rows(label: str, triples: Sequence[Triple]) -> list[str]:
    return [f"- {label}: ({cell}, {register}, {mark})"
            for cell, register, mark in triples]


def render_decision(d: Decision) -> str:
    """The cycle's decision record, with every required sentence verbatim.

    The sections are fixed: what was decided, the sentences the reason
    requires, the protected register with ``protected_not_evaluable`` printed
    beside it, ``losses_outside_P`` present even when empty, the obligations'
    standing, what moved in the mark-triple set, and the mandatory
    ``would_reopen`` prose.

    ``standard.assert_no_exhaustion_claim`` is run over the finished text, so a
    record that described a reached ceiling as the inquiry running out is
    refused here rather than at the renderer.
    """

    if not isinstance(d, Decision):
        raise DecisionRefused(DECISION_REASON_UNKNOWN,
                              "render_decision() takes a Decision")
    lines: list[str] = [
        f"# Decision - cycle {d.cycle}",
        "",
        f"- outcome: {'STOP' if d.stop else 'CONTINUE'}",
        f"- reason: {d.reason}",
        f"- clause: {d.clause}",
        f"- detail: {d.detail}",
        f"- obligations_pin: {d.obligations_pin}",
        f"- decide_sha256: {DECIDE_SHA256}",
        "",
    ]
    lines.extend(_section("record sentences", [
        f"{sentence}\n" for sentence in d.record_sentences]))
    lines.extend(_section("protected_losses", _loss_rows(d.protected_losses)))
    lines.extend(_section("protected_not_evaluable",
                          _id_rows(d.protected_not_evaluable)))
    lines.extend(_section("losses_outside_P", _loss_rows(d.losses_outside_p)))
    lines.extend(_section("obligations discharged this cycle",
                          _id_rows(d.discharged)))
    lines.extend(_section("obligations of O that do not hold", _id_rows(d.failed)))
    lines.extend(_section("obligations the program could not read",
                          _id_rows(d.not_evaluable)))
    if d.triples_compared:
        moved = _triple_rows("entered", d.triples_entered)
        moved.extend(_triple_rows("left", d.triples_left))
        if not moved:
            moved = ["- the two sets are identical; no triple moved"]
        lines.extend(_section("mark triples", moved))
    else:
        lines.extend(_section("mark triples", [NOT_COMPARED]))
    lines.extend(_section(WOULD_REOPEN_LABEL, [d.would_reopen]))
    body = "\n".join(lines).rstrip()
    text = f"{body}\n"
    _standard.assert_no_exhaustion_claim(text, "decision record")
    return text
