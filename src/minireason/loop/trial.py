"""W3-TRIAL - the guard procedure G0-G12 end to end.

Purpose
-------
One guarded trial: critic, defender, the cross-family judge ensemble, then
constitution, schema, uniqueness on both surfaces, operative target,
vocabulary, unanimity, order-swap, the paraphrase spot-check, no-re-read and
no-scoring-key - in §2.4's order, each deterministic check a line of Python
and none of them a model call of this module's own. A **blocked** trial
registers nothing: no warrant, no reading, one ``Measure`` event logging the
block by its reason code with the prompt blob ref and the raw blob ref
already spent beside it, and the cell stays unresolved. A **sustained** trial
returns the :class:`~minireason.loop.graph.ReadingResult` W4-READER registers;
a **not-sustained** one is a ruling and not a warrant, and the Measure log
records it so the exchange is replayable without ever claiming the relation.

Design section implemented
--------------------------
W3-TRIAL of *The automated end-to-end harness loop - FINAL design of record*:
§2.4 ("The §10 guard procedure, step by step") in full against §2.3's five
prompt contracts, §3(d)-(f) for what a surviving trial hands the graph, and
§2.3's variator note ("on failure the spot-check itself is *unresolved* and
the cell keeps the unparaphrased outcome") for the one place a check is
*not performed* rather than passed or failed.

Order of evaluation, and where each guard runs
----------------------------------------------
===== ====================================================================
G0    ``_constitution`` - the seat plan must satisfy §2.2's family rules.
      Unsatisfiable means a ``blocked:constitution`` block: the coordinates
      are **not dispatched**, no call record exists, and the refs the block
      record carries are empty rather than invented.
G11   ``_reopen_gate``, *at the write* - before the first call coordinate
      of a re-read is claimed, since the write-once record is the thing the
      design says is refused. "Prior outcome unresolved" is read off the
      graph: a prior trial of this cell left a ``Measure`` event whose
      inputs name the cell's default artifact, so re-reading is detectable
      without a side table.
critic      ``roles.call_critic`` on the row pack; blocked stops here. A
      ``none`` ends the row at one call (§2.3); a non-empty
      ``outside_vocabulary`` forces ``blocked:outside-vocabulary`` with the
      text preserved (G4, D6).
G2(a) the critic's ``passage_quote`` must resolve **uniquely** in the
      surface ``M`` (``surface.resolve_unique``).
G3    that resolution must lie inside a declared span
      (``surface.within_declared_span``); a quote of the surface's own
      framing blocks with ``blocked:operative-target``.
defender    ``roles.call_defender`` on the exchange pack.
judges      ``roles.call_judge`` per seat, on identical packs, in **both**
      presentation orders (G6 is discharged *by* running both).
G2(b) each ``decisive_point`` must resolve uniquely in ``E = case + "\\n" +
      answer`` (``packs.Exchange.count``/``resolve`` - the stronger check
      first; the vendored ``conforming_transcript`` gate is re-asserted
      through ``graph.Transcript.validated`` when the hand-off transcript
      is built, so the guard and the registration gate cannot diverge).
G5    every ruling of the panel must carry one ``sustained`` value; a split
      blocks ``blocked:ensemble-split`` and both rulings are recorded
      verbatim. Never a majority, never an average (FW5:634).
G6    one seat across its two orders must not flip the outcome; a flip
      blocks ``blocked:order-swap``.
G7    on a sustained ruling only: ``paraphrase_n`` variator paraphrases of
      the exchange, the quoted spans asserted byte-identical, and each
      surviving paraphrase re-ruled by both seats. A flip or a split blocks
      ``blocked:paraphrase-flip`` and is logged **against that seat**. A
      paraphrase that lost a quoted span is never re-ruled and never
      passes: the spot-check is recorded ``not_performed`` and the cell
      keeps the unparaphrased outcome.
G12   every record this module emits passes
      ``contracts.assert_no_scoring_keys``; the transcript passes
      ``standard.assert_no_exhaustion_claim``.
===== ====================================================================

A block is logged as exactly one ``Measure`` event (§2.4: *a* ``Rule.MEASURE``
*event recording both rulings verbatim* for a split, and the block's own log
line otherwise) with ``inputs`` naming the cell's default artifact - which is
what lets ``_reopen_gate`` see the prior attempt - and an ``llm`` record
carrying the prompt and raw refs of the call that provoked it. No ``att`` or
``dep`` edge is ever minted here; a block is the instrument declining to read.

What this module is not
-----------------------
No score, rank, average, majority vote, percentage or progress meter anywhere:
a disagreement is ``unresolved``. It renders no pack itself (W2-PACKS does),
speaks to no model directly (W2-ROLES does), and registers no reading itself
(W1-GRAPH's door is W4-READER's). It seals no baseline (G8-G10 are
W2-MARKPREP's and W4-MARKER's, and marks ride the same *roles* gates through
their own callers). The one thing it owns is the guard's sequencing and the
records the sequencing leaves.

Deviations from the wave-plan interface, and why
------------------------------------------------
1. **``run_trial`` takes three keyword-only arguments the entry's signature
   does not carry**, because the guard physically cannot run without them:
   ``key=`` (the cell key - *required*; a trial that cannot name its cell
   cannot enforce G11, cannot address its write-once coordinates, and cannot
   name its transcript), ``records_dir=`` (where W2-ROLES' write-once call
   records are spent), and ``provider_factory=`` (the way every provider
   interaction goes through the OfflineProvider fixtures the acceptance
   demands, exactly as W2-ROLES already takes one). ``harness`` may be a
   :class:`PreparedTrial` from :func:`open_trial_harness`, which additionally
   carries the registered standard's id.
2. **``mode`` is asserted, not dispatched on.** The standard declares the
   relation trial :data:`~minireason.loop.standard.MODE_ABSOLUTE`; any other
   mode is refused with :data:`TRIAL_MODE_UNEXPECTED`, and a register key is
   refused the same way - marks run pairwise through W4-MARKER's own caller,
   not through a second reading of this rubric.
3. **``TrialResult.transcript`` is the emitted transcript text**
   (``build_transcript(result)``). ``TrialResult.reading`` is the
   :class:`~minireason.loop.graph.ReadingResult` built on a sustained trial;
   registration is deliberately *not* done here, because W4-READER owns the
   decision to register and this module owns the guard.
4. **The paraphrase re-ruling's ``decisive_point`` is checked for a flip,
   not re-resolved against the paraphrase.** §2.4 G7 asks for a flip or a
   split; it does not ask the point to resolve inside the restated exchange,
   and the pack the re-ruling seat sees is the standard judge pack with one
   restated text, so the stronger G2(b) re-check would be a check the design
   never named, run over a text no citation resolves against. Recorded here
   as required.
5. **G0 is a block in the result, not an exception.** ``blocked:constitution``
   is a member of ``types.BLOCK_CODES`` precisely so a G0 block reads like
   every other block: one Measure event, no call record, empty refs.
6. **A ``none`` answer is not a block, and it still leaves one Measure
   event.** It is an answer - the row ends at one call, §2.3 - so ``blocks``
   is empty and the outcome is :data:`OUTCOME_NO_TRIAL`, not a block code. But
   a Measure is information, not a verdict (the same event is written for a
   not-sustained ruling, which is also not a block), and G11 reads a cell's
   prior attempt off exactly these events: a ``none`` that left no trace was a
   cell any caller could re-read without a ``reopen_reason``, which is the
   "retry until something sticks" the gate exists to refuse.

New failure codes (:data:`NEW_CODES`)
-------------------------------------
See the table; each names a trial that could not be *formed*, which is not a
cell block and gets no Measure event.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Callable, Mapping, Sequence

from deepreason_core.canonical import canonical_json, sha256_hex
from deepreason_core.ontology import LLMCall, Rule

from minireason.loop import contracts, graph, standard
from minireason.loop import packs, roles
from minireason.loop import surface as surface_mod
from minireason.loop import types as loop_types
from minireason.loop.contracts import (
    CriticOutput,
    DefenderOutput,
    JudgeRuling,
    VariatorOutput,
)
from minireason.loop.graph import CellKey, ReadingResult, Transcript
from minireason.loop.packs import (
    Exchange,
    PrecedentSlice,
    both_orders,
    exchange_surface,
    held_spans_of,
    pack_sha,
    paraphrase_surface,
    precedent_slice,
    render_exchange,
    render_paraphrase_request,
    render_row,
)
from minireason.loop.roles import RoleResult
from minireason.loop.seats import SeatPlan
from minireason.loop.standard import REOPEN_REASONS
from minireason.loop.surface import Surface, resolve_unique, within_declared_span
from minireason.loop.types import LoopError, block_code

__all__ = [
    "TRIAL_SCHEMA",
    "OUTCOME_BLOCKED",
    "OUTCOME_NOT_SUSTAINED",
    "OUTCOME_SUSTAINED",
    "OUTCOME_NO_TRIAL",
    "OUTCOME_UNRESOLVED",
    "OUTCOMES",
    "GUARD_CHECKS",
    "G0_CONSTITUTION",
    "G1_SCHEMA",
    "G2A_UNIQUENESS",
    "G2B_UNIQUENESS",
    "G3_OPERATIVE_TARGET",
    "G4_VOCABULARY",
    "G5_UNANIMITY",
    "G6_ORDER_SWAP",
    "G7_PARAPHRASE",
    "G11_NO_REREAD",
    "G12_NO_SCORING_KEY",
    "PERFORMED",
    "NOT_PERFORMED",
    "REOPEN_REASONS",
    "BLOCK_CODES",
    "CONSTITUTION_BLOCK",
    "SCHEMA_BLOCK",
    "PROVIDER_BLOCK",
    "ENSEMBLE_SPLIT_BLOCK",
    "REFERENTIAL_INTEGRITY_BLOCK",
    "OPERATIVE_TARGET_BLOCK",
    "ORDER_SWAP_BLOCK",
    "PARAPHRASE_FLIP_BLOCK",
    "OUTSIDE_VOCABULARY_BLOCK",
    "TRIAL_ARGUMENT_INVALID",
    "TRIAL_MODE_UNEXPECTED",
    "TRIAL_SEAT_PLAN_INVALID",
    "TRIAL_PRIOR_STATE_UNREADABLE",
    "NEW_CODES",
    "ReopenRefused",
    "TrialRefused",
    "Block",
    "CallRecord",
    "PreparedTrial",
    "TrialResult",
    "build_transcript",
    "open_trial_harness",
    "run_trial",
]


# --------------------------------------------------------------------------
# Codes
# --------------------------------------------------------------------------

TRIAL_ARGUMENT_INVALID = "TRIAL_ARGUMENT_INVALID"
TRIAL_MODE_UNEXPECTED = "TRIAL_MODE_UNEXPECTED"
TRIAL_SEAT_PLAN_INVALID = "TRIAL_SEAT_PLAN_INVALID"
TRIAL_PRIOR_STATE_UNREADABLE = "TRIAL_PRIOR_STATE_UNREADABLE"

#: Codes this module introduces, each with the one-line reason the wave
#: integrator needs to fold it into ``types.FAILURE_CODES`` (W0-TYPES open
#: question O9). None of them is a block code and none is a semantic result:
#: every one names a trial that could not be formed and so has no Measure
#: event attached to it. ``REOPEN_REFUSED`` is deliberately absent - it is
#: already a member of ``types.FAILURE_CODES``, and :class:`ReopenRefused`
#: raises exactly that spelling, never a retyped one.
NEW_CODES: Mapping[str, str] = MappingProxyType({
    TRIAL_ARGUMENT_INVALID:
        "run_trial was handed something that is not the surface, the "
        "standard body, the seat plan, the config, the cell key or the "
        "records directory it can spend, so no coordinate was ever claimed",
    TRIAL_MODE_UNEXPECTED:
        "the trial was asked to run under a mode that is not the standard's "
        "absolute relation rubric, or for a register cell; marks run "
        "pairwise through W4-MARKER, not through a second branch here",
    TRIAL_SEAT_PLAN_INVALID:
        "the seats argument is not a seats.SeatPlan, so the trial has no seat "
        "table to read and no coordinate to spend. This is the refused SHAPE "
        "and not G0: a plan that IS a SeatPlan but cannot satisfy section "
        "2.2's family rules is a blocked:constitution BLOCK with its own "
        "Measure event (deviation 5), never an exception",
    TRIAL_PRIOR_STATE_UNREADABLE:
        "G11's gate could not establish the cell's prior state, so the "
        "write is refused with the reason rather than admitted on a guess",
})

# G7's span-survival outcome is NOT a code. A paraphrase that did not preserve
# a quoted span is discarded, its re-ruling is never requested, and the
# spot-check is recorded :data:`NOT_PERFORMED` - which is a recorded state of a
# trial that ran, not a refusal to form one. The draft declared a
# ``TRIAL_PARAPHRASE_SPAN_LOST`` code for it whose own stated reason described
# a non-raise, and nothing in the package could ever raise it; a code no call
# site reaches is a code no register prints.


def _refuse(code: str, detail: str = "") -> "TrialRefused":
    return TrialRefused(code, detail)


class TrialRefused(LoopError):
    """A trial that could not be *formed* - argument, mode or seat plan.

    ``(code, detail="")`` like every wave-0 exception, and a
    :class:`~minireason.loop.types.LoopError`, so one ``except LoopError``
    catches it with everything else. A block of the cell under trial is
    **not** this: a block is a returned :class:`TrialResult` with its
    Measure event already logged.
    """


class ReopenRefused(LoopError):
    """G11: the write is refused because a re-read carried no listed reason.

    Raised at the write - before the first write-once call coordinate of the
    re-read is claimed - which is "enforced by refusing the write, not by a
    convention" (§2.4 G11). The code is ``REOPEN_REFUSED``
    (``types.FAILURE_CODES``); the reason list is exactly the config's
    pre-registered ``reopen_reasons``, which must be the standard's own.
    """

    def __init__(self, detail: str = "") -> None:
        super().__init__("REOPEN_REFUSED", detail)


# --------------------------------------------------------------------------
# Vocabulary
# --------------------------------------------------------------------------

#: The trial record's and transcript's own schema name.
TRIAL_SCHEMA = "minireason.loop.trial.v1"

#: What a trial can return. None of these values is a quantity; only
#: ``sustained`` ever carries a :class:`~minireason.loop.graph.ReadingResult`.
OUTCOME_BLOCKED = "blocked"
OUTCOME_NOT_SUSTAINED = "not-sustained"
OUTCOME_SUSTAINED = "sustained"
#: The critic answered ``none``: the row ends at one call, the cell stays
#: unresolved, and nothing was tried (§2.3).
OUTCOME_NO_TRIAL = "no-trial"
#: A non-empty ``outside_vocabulary`` forced the cell unresolved (G4/D6).
OUTCOME_UNRESOLVED = "unresolved"

OUTCOMES: tuple[str, ...] = (
    OUTCOME_BLOCKED,
    OUTCOME_NOT_SUSTAINED,
    OUTCOME_SUSTAINED,
    OUTCOME_NO_TRIAL,
    OUTCOME_UNRESOLVED,
)

#: The guard entries every transcript prints, in §2.4 order. A check that the
#: run never reached is printed ``not_performed``, never omitted: "the guard
#: stopped the line" is a fact the register reads as well as "it held".
G0_CONSTITUTION = "G0-constitution"
G1_SCHEMA = "G1-schema"
G2A_UNIQUENESS = "G2a-uniqueness"
G2B_UNIQUENESS = "G2b-uniqueness"
G3_OPERATIVE_TARGET = "G3-operative-target"
G4_VOCABULARY = "G4-vocabulary"
G5_UNANIMITY = "G5-unanimity"
G6_ORDER_SWAP = "G6-order-swap"
G7_PARAPHRASE = "G7-paraphrase-spot-check"
G11_NO_REREAD = "G11-no-reread"
G12_NO_SCORING_KEY = "G12-no-scoring-key"

GUARD_CHECKS: tuple[str, ...] = (
    G0_CONSTITUTION,
    G1_SCHEMA,
    G2A_UNIQUENESS,
    G2B_UNIQUENESS,
    G3_OPERATIVE_TARGET,
    G4_VOCABULARY,
    G5_UNANIMITY,
    G6_ORDER_SWAP,
    G7_PARAPHRASE,
    G11_NO_REREAD,
    G12_NO_SCORING_KEY,
)

PERFORMED = "performed"
NOT_PERFORMED = "not_performed"

#: The ten block codes a block register counts, imported and never retyped.
#: ``types.block_code(reason)`` is the one way a spelling of one is built.
BLOCK_CODES = loop_types.BLOCK_CODES

CONSTITUTION_BLOCK = block_code("constitution")
SCHEMA_BLOCK = roles.SCHEMA_BLOCK
PROVIDER_BLOCK = roles.PROVIDER_BLOCK
ENSEMBLE_SPLIT_BLOCK = block_code("ensemble-split")
REFERENTIAL_INTEGRITY_BLOCK = surface_mod.REFERENTIAL_INTEGRITY_BLOCK
OPERATIVE_TARGET_BLOCK = surface_mod.OPERATIVE_TARGET_BLOCK
ORDER_SWAP_BLOCK = block_code("order-swap")
PARAPHRASE_FLIP_BLOCK = block_code("paraphrase-flip")
OUTSIDE_VOCABULARY_BLOCK = block_code("outside-vocabulary")


# --------------------------------------------------------------------------
# Records
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class CallRecord:
    """One spent call, kept for the transcript's roster.

    Nothing of the answer beyond its block state and its refs is here: the
    answers live on ``TrialResult.critic``/``defender``/``rulings``, and the
    bytes live in the call record W2-ROLES already wrote.
    """

    role: str
    coordinate: str
    seat_label: str
    result: RoleResult

    def as_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "coordinate": self.coordinate,
            "seat_label": self.seat_label,
            "status": self.result.status,
            "block": self.result.block,
            "reason": self.result.reason,
            "record_path": self.result.record_path,
            "prompt_ref": self.result.prompt_ref.as_dict(),
            "raw_ref": self.result.raw_ref.as_dict(),
            "pack_sha256": self.result.record.get("pack_sha256"),
        }


@dataclass(frozen=True)
class Block:
    """One guard block: the instrument declining to read, named by its code.

    ``code`` is a member of :data:`BLOCK_CODES`; ``check`` names the guard
    step that fired. The prompt and raw blob refs of the call that provoked
    the block ride beside it, exactly as §2.4 requires - **empty** for a G0
    constitution block, because nothing was dispatched, and never empty
    otherwise.
    """

    code: str
    check: str
    detail: str
    prompt_ref_path: str = ""
    raw_ref_path: str = ""
    prompt_sha: str | None = None
    raw_sha: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "check": self.check,
            "detail": self.detail,
            "prompt_ref": {"path": self.prompt_ref_path, "sha256": self.prompt_sha},
            "raw_ref": {"path": self.raw_ref_path, "sha256": self.raw_sha},
        }


@dataclass(frozen=True)
class PreparedTrial:
    """A harness with the standard and the cell's unresolved default in it.

    :func:`open_trial_harness` returns this; ``run_trial`` accepts it in the
    ``harness`` argument, so a trial and its graph never disagree about which
    standard the trial ran under.
    """

    harness: Any
    standard_id: str
    cell: str
    material_id: str | None = None


def open_trial_harness(
    root: Any,
    cell: Any,
    *,
    material: bytes | str = b"",
    clock: Callable[[], str] | None = None,
) -> PreparedTrial:
    """Register the standard and the cell's default; return the prepared harness.

    ``root`` is the graph directory; ``cell`` a cell key in any spelling
    ``graph.CellKey.coerce`` accepts. Every registration goes through
    W1-GRAPH, on the deterministic clock it owns, so a replay of the log is
    byte-identical.
    """

    key = CellKey.coerce(cell)
    harness = graph.open_graph(
        root, clock=clock if clock is not None else graph.fixed_clock()
    )
    standard_id = graph.register_standard(harness, standard.STANDARD_BODY)
    material_id = graph.register_material(harness, material) if material else None
    graph.open_cells(harness, [key], material_id=material_id)
    return PreparedTrial(
        harness=harness,
        standard_id=standard_id,
        cell=key.token,
        material_id=material_id,
    )


@dataclass(frozen=True)
class TrialResult:
    """The complete record of one guarded trial.

    Every field is a plain record; nothing here orders, sums or averages
    anything. ``checks`` carries every member of :data:`GUARD_CHECKS`,
    performed or ``not_performed``.
    """

    cell: str
    mode: str
    outcome: str
    blocks: tuple[Block, ...]
    transcript: str
    checks: Mapping[str, str]
    calls: tuple[CallRecord, ...]
    standard_id: str
    critic: CriticOutput | None = None
    defender: DefenderOutput | None = None
    rulings: Mapping[str, JudgeRuling] = field(default_factory=dict)
    paraphrases: tuple[str, ...] = ()
    paraphrase_rulings: Mapping[str, Mapping[str, JudgeRuling]] = field(
        default_factory=dict
    )
    reading: ReadingResult | None = None
    measures: tuple[int, ...] = ()
    reopen_reason: str | None = None
    surface_digest: str = ""
    exchange_digest: str = ""
    pack_digests: Mapping[str, str] = field(default_factory=dict)

    @property
    def blocked(self) -> bool:
        return self.outcome == OUTCOME_BLOCKED

    @property
    def sustained(self) -> bool:
        return self.outcome == OUTCOME_SUSTAINED

    @property
    def block(self) -> Block | None:
        return self.blocks[0] if self.blocks else None

    def block_codes(self) -> tuple[str, ...]:
        return tuple(block.code for block in self.blocks)

    def as_dict(self) -> dict[str, Any]:
        """The whole record - G12-clean before it is returned."""
        record = {
            "schema": TRIAL_SCHEMA,
            "cell": self.cell,
            "mode": self.mode,
            "outcome": self.outcome,
            "standard": self.standard_id,
            "surface_digest": self.surface_digest,
            "exchange_digest": self.exchange_digest,
            "pack_digests": dict(self.pack_digests),
            "blocks": [block.as_dict() for block in self.blocks],
            "checks": dict(self.checks),
            "calls": [call.as_dict() for call in self.calls],
            "critic": self.critic.as_dict() if self.critic else None,
            "defender": self.defender.as_dict() if self.defender else None,
            "rulings": {seat: ruling.as_dict() for seat, ruling in self.rulings.items()},
            "paraphrases": list(self.paraphrases),
            "paraphrase_rulings": {
                token: {seat: ruling.as_dict() for seat, ruling in seat_map.items()}
                for token, seat_map in self.paraphrase_rulings.items()
            },
            "reopen_reason": self.reopen_reason,
            "transcript": self.transcript,
        }
        contracts.assert_no_scoring_keys(record)
        return record

    def _replace(self, *, transcript: str) -> "TrialResult":
        return TrialResult(**{**self.__dict__, "transcript": transcript})


# --------------------------------------------------------------------------
# build_transcript
# --------------------------------------------------------------------------


def build_transcript(result: TrialResult | Mapping[str, Any]) -> str:
    """Render the emitted trial transcript.

    Takes a :class:`TrialResult` (the ``run_trial`` return) or the same
    fields as a mapping. Deterministic: two renderings of one result are
    byte-identical. The transcript prints **every** guard check, performed
    or ``not_performed`` - a check the run never reached is never omitted -
    and prints a split panel as both rulings verbatim rather than as any
    settlement between them. No score, no tally, no majority: a disagreement
    reads as a disagreement.

    ``standard.assert_no_exhaustion_claim`` runs over the text before it is
    returned: the first generated records of the loop may not describe a
    boundary as the inquiry running out (N9). It runs over *this module's own
    prose* - a block's ``detail``, which carries a transport's verbatim words
    about a delivery, is lifted out first, on W2-ROLES' own ruling that an
    observation is never rewritten. See
    :func:`_assert_this_module_claims_no_exhaustion`.
    """

    if isinstance(result, TrialResult):
        fields: dict[str, Any] = {
            "cell": result.cell,
            "mode": result.mode,
            "outcome": result.outcome,
            "standard": result.standard_id,
            "surface_digest": result.surface_digest,
            "exchange_digest": result.exchange_digest,
            "reopen_reason": result.reopen_reason,
            "checks": dict(result.checks),
            "blocks": list(result.blocks),
            "pack_digests": dict(result.pack_digests),
            "critic": result.critic.as_dict() if result.critic else None,
            "defender": result.defender.as_dict() if result.defender else None,
            "rulings": {seat: r.as_dict() for seat, r in result.rulings.items()},
            "paraphrases": list(result.paraphrases),
            "paraphrase_rulings": {
                token: {seat: r.as_dict() for seat, r in seat_map.items()}
                for token, seat_map in result.paraphrase_rulings.items()
            },
        }
    elif isinstance(result, Mapping):
        fields = dict(result)
    else:
        raise _refuse(
            TRIAL_ARGUMENT_INVALID,
            "build_transcript takes a TrialResult or its mapping form",
        )

    cell = str(fields.get("cell", ""))
    mode = str(fields.get("mode", standard.MODE_ABSOLUTE))
    outcome = str(fields.get("outcome", ""))
    if outcome not in OUTCOMES:
        raise _refuse(
            TRIAL_ARGUMENT_INVALID, f"outcome {outcome!r} is not one of {OUTCOMES}"
        )
    checks = dict(fields.get("checks") or {})
    missing_checks = [name for name in GUARD_CHECKS if name not in checks]
    if missing_checks:
        raise _refuse(
            TRIAL_ARGUMENT_INVALID,
            f"checks omits {missing_checks}; a transcript prints every guard "
            "entry performed or not_performed rather than omitting it",
        )
    blocks = [
        block
        if isinstance(block, Block)
        else Block(
            code=str(block["code"]),
            check=str(block["check"]),
            detail=str(block.get("detail", "")),
            prompt_ref_path=str((block.get("prompt_ref") or {}).get("path", "")),
            raw_ref_path=str((block.get("raw_ref") or {}).get("path", "")),
            prompt_sha=(block.get("prompt_ref") or {}).get("sha256"),
            raw_sha=(block.get("raw_ref") or {}).get("sha256"),
        )
        for block in fields.get("blocks", ())
    ]
    for block in blocks:
        if block.code not in BLOCK_CODES:
            raise _refuse(
                TRIAL_ARGUMENT_INVALID,
                f"{block.code!r} is not a member of types.BLOCK_CODES",
            )

    lines: list[str] = ["# trial transcript", ""]
    lines.append(f"cell: {cell}")
    lines.append(f"outcome: {outcome}")
    lines.append(f"mode: {mode}")
    if fields.get("standard"):
        lines.append(f"standard: {fields['standard']}")
    if fields.get("surface_digest"):
        lines.append(f"surface: {fields['surface_digest']}")
    if fields.get("exchange_digest"):
        lines.append(f"exchange: {fields['exchange_digest']}")
    if fields.get("reopen_reason") is not None:
        lines.append(f"reopen_reason: {fields['reopen_reason']}")
    lines += ["", "checks:"]
    for name in GUARD_CHECKS:
        lines.append(f"  {name}: {checks[name]}")
    pack_digests = dict(fields.get("pack_digests") or {})
    if pack_digests:
        lines += ["", "packs:"]
        for name, digest in sorted(pack_digests.items()):
            lines.append(f"  {name}: {digest}")
    critic = fields.get("critic")
    if critic is not None:
        critic = dict(critic)
        lines += ["", "critic:"]
        lines.append(f"  relation: {critic['relation']}")
        if critic.get("nominated_relation"):
            lines.append(f"  nominated: {critic['nominated_relation']}")
        lines.append(f"  passage_quote: {critic['passage_quote']!r}")
        lines.append(f"  case: {critic['case']!r}")
        outside = critic.get(contracts.OUTSIDE_VOCABULARY_FIELD, "")
        if outside:
            lines.append(f"  outside_vocabulary: {outside!r}")
    defender = fields.get("defender")
    if defender is not None:
        lines += ["", "defender:"]
        lines.append(f"  answer: {defender['answer']!r}")
        lines.append(f"  concedes: {defender['concedes']}")
    rulings = dict(fields.get("rulings") or {})
    if rulings:
        lines += ["", "rulings:"]
        for seat in sorted(rulings):
            ruling = dict(rulings[seat])
            lines.append(f"  {seat}:")
            lines.append(f"    sustained: {ruling['sustained']}")
            lines.append(f"    decisive_point: {ruling['decisive_point']!r}")
            lines.append(f"    reading_note: {ruling['reading_note']!r}")
    paraphrase_rulings = dict(fields.get("paraphrase_rulings") or {})
    if paraphrase_rulings:
        lines += ["", "paraphrase re-rulings:"]
        for token in sorted(paraphrase_rulings):
            lines.append(f"  {token}:")
            for seat in sorted(paraphrase_rulings[token]):
                ruling = dict(paraphrase_rulings[token][seat])
                lines.append(f"    {seat}: sustained: {ruling['sustained']}")
                lines.append(f"      decisive_point: {ruling['decisive_point']!r}")
    paraphrases = list(fields.get("paraphrases") or ())
    if paraphrases:
        lines += ["", "paraphrases:"]
        for index, text in enumerate(paraphrases):
            lines.append(f"  {index + 1}: {text!r}")
    lines.append("")
    quoted: list[str] = []
    if blocks:
        lines.append("blocks:")
        for block in blocks:
            quoted.append(str(block.detail))
            lines.append(f"- {block.code} ({block.check}): {block.detail}")
            if block.prompt_ref_path:
                lines.append(f"  prompt: {block.prompt_ref_path}")
            if block.raw_ref_path:
                lines.append(f"  raw: {block.raw_ref_path}")
    else:
        lines.append(
            "blocks: none - every check the run reached held; a check it did "
            "not reach is marked not_performed above."
        )
    text = "\n".join(lines) + "\n"
    _assert_this_module_claims_no_exhaustion(text, quoted)
    return text


def _assert_this_module_claims_no_exhaustion(text: str, quoted: Sequence[str]) -> None:
    """N9's scan over what *this module wrote*, and not over what a route said.

    A block detail is a **quoted observation**: the transport's own words about
    a delivery, carried verbatim so the record can be read back. W2-ROLES
    already rules that the exhaustion scan is not run over delivery error
    strings (wave-2 integration item 42(h): "an observation is never
    rewritten"), and this module has to honour the same boundary for the same
    reason - the transport spells an empty offline script "offline script
    exhausted", and scanning it made a provider block **unrenderable**: the
    transcript raised ``RESOURCE_BOUNDARY_MISDESCRIBED`` and the tenth block
    path could not be emitted at all. The quoted spans are lifted out and the
    module's own prose is scanned; an *exhaustion* claim this module made
    survives the lift, because it is not inside a quoted detail.
    """
    scanned = text
    for detail in quoted:
        if detail:
            scanned = scanned.replace(detail, "")
    standard.assert_no_exhaustion_claim(scanned, "trial transcript")


# --------------------------------------------------------------------------
# The gates that refuse rather than return
# --------------------------------------------------------------------------


def _constitution(plan: SeatPlan) -> str | None:
    """G0, pre-dispatch. Returns the block detail, or ``None`` when it holds.

    The refused *shape* - a plan that cannot carry §2.2's family rules at
    all - is :class:`TrialRefused`; what returns here is a plan the selection
    produced that cannot satisfy the constraints for this trial, which §2.4
    spells as coordinates not dispatched.
    """

    minimum = int(standard.GUARD_PARAMETERS["min_judge_families"])
    if len(plan.judges) < minimum:
        return (
            f"the seat plan carries {len(plan.judges)} judge seats and §2.2 "
            f"requires {minimum}; the coordinates are not dispatched"
        )
    judge_lineages = frozenset(plan.judge_lineages)
    if len(judge_lineages) != len(plan.judges):
        return "two judge seats share one lineage"
    if plan.critic.lineage in judge_lineages:
        return "the critic is seated inside a judge lineage"
    if plan.defender.lineage == plan.critic.lineage:
        return "the defender is seated inside the critic's lineage"
    return None


def _reopen_gate(
    harness: Any,
    key: CellKey,
    *,
    default_id: str,
    reopen_reason: str | None,
    config: loop_types.LoopConfig,
) -> None:
    """G11: refuse the re-read of an unresolved cell, at the write.

    "The write" is the first call record of the re-read, so this gate runs
    before any coordinate of it is claimed - a refusal after three calls were
    spent would be a convention, not the enforcement §2.4 requires. A *prior
    outcome* is read off the graph: a blocked or otherwise resolved trial of
    this cell left a ``Measure`` event whose inputs name the cell's default
    artifact. The config's ``reopen_reasons`` must be the standard's own
    list: a config that admits a fourth reason is a second reopen list.
    """

    listed = tuple(config.reopen_reasons)
    if listed != tuple(REOPEN_REASONS):
        raise _refuse(
            TRIAL_PRIOR_STATE_UNREADABLE,
            f"config.reopen_reasons is {listed}, not the standard's own "
            f"{tuple(REOPEN_REASONS)}; no config may widen the reopen list",
        )
    try:
        events = list(harness.log.read())
    except (OSError, ValueError) as exc:
        raise _refuse(
            TRIAL_PRIOR_STATE_UNREADABLE,
            f"{key.token}: the trial log could not be read ({exc})",
        ) from exc
    prior = any(
        event.rule == Rule.MEASURE and default_id in event.inputs for event in events
    )
    if not prior:
        return
    if reopen_reason is None:
        raise ReopenRefused(
            f"{key.token} already carries a trial; a re-read needs a "
            f"reopen_reason from {listed} and this call carries none"
        )
    if reopen_reason not in listed:
        raise ReopenRefused(
            f"{key.token} already carries a trial and {reopen_reason!r} is "
            f"not one of the pre-registered reopen reasons {listed}"
        )


# --------------------------------------------------------------------------
# Blocks, and the one Measure event each is logged by
# --------------------------------------------------------------------------


def _llm_of(call: RoleResult) -> LLMCall:
    """The structured link between a block and what was already spent.

    ``prompt_ref`` and ``raw_ref`` are the refs §2.4 names beside a block;
    ``ms`` is the call's own recorded elapsed time, never re-measured.
    """

    return LLMCall(
        role=str(call.role),
        model=str(call.seat.get("model", "")),
        endpoint=str(call.seat.get("name", "")),
        prompt_ref=str(call.prompt_ref.path),
        raw_ref=str(call.raw_ref.path),
        tokens=0,
        ms=int(call.record["outcome"].get("elapsed_ms") or 0),
    )


def _block(
    harness: Any,
    code: str,
    check: str,
    detail: str,
    *,
    default_id: str,
    of: RoleResult | None = None,
) -> tuple[Block, int]:
    """Assemble one block and append the one Measure event it is logged by.

    The event's ``inputs`` name the cell's default artifact, which is what
    G11's gate reads back as "a prior outcome stands on this cell"; the
    ``llm`` field carries the prompt and raw refs of the call that provoked
    the block - present in a call-provoked block, ``None`` where nothing was
    dispatched (G0) or no call provoked it (a split, an outside-vocabulary
    answer still names its critic's call).
    """

    event = harness.record_measure(
        inputs=[default_id], llm=_llm_of(of) if of is not None else None
    )
    block = Block(
        code=code,
        check=check,
        detail=detail,
        prompt_ref_path=str(of.prompt_ref.path) if of is not None else "",
        raw_ref_path=str(of.raw_ref.path) if of is not None else "",
        prompt_sha=of.prompt_ref.sha256 if of is not None else None,
        raw_sha=of.raw_ref.sha256 if of is not None else None,
    )
    return block, int(event.seq)


# --------------------------------------------------------------------------
# run_trial
# --------------------------------------------------------------------------


def run_trial(
    harness: Any,
    surface: Any,
    standard_body: Any,
    seats: Any,
    config: Any,
    *,
    mode: str,
    key: Any = None,
    records_dir: Any = None,
    reopen_reason: str | None = None,
    provider_factory: Any = None,
    precedents: PrecedentSlice | None = None,
    framing: Any = None,
) -> TrialResult:
    """Run the §2.4 guard over one cell, end to end.

    ``harness`` is a live ``deepreason_core`` harness - or the
    :class:`PreparedTrial` :func:`open_trial_harness` returned. ``surface``
    is the W1-SURFACE of the row; ``standard_body`` the pinned standard
    (bytes, text or parsed body); ``seats`` the frozen
    :class:`~minireason.loop.seats.SeatPlan`; ``config`` a
    :class:`~minireason.loop.types.LoopConfig` or its mapping. ``mode`` must
    be the standard's absolute mode. ``key`` is the cell's key - required,
    because a trial that cannot name its cell cannot refuse a re-read, and
    it must agree with a :class:`PreparedTrial`'s cell when one is handed.
    ``records_dir`` is where the write-once call records are spent, and is
    required: no call is *ever* made without one. ``provider_factory`` is the
    OfflineProvider factory the acceptance demands every provider interaction
    go through.

    A blocked outcome registers nothing: ``blocks`` names the first failing
    check by its ``BLOCK_CODES`` reason code, ``measures`` holds the single
    Measure event's sequence number, and the cell's standing in the graph is
    untouched. A sustained outcome carries ``reading``, the
    :class:`~minireason.loop.graph.ReadingResult` W4-READER registers.
    """

    # ---- form errors: the trial was never configured ----------------------
    if not isinstance(seats, SeatPlan):
        raise _refuse(TRIAL_SEAT_PLAN_INVALID, "seats is a seats.SeatPlan")
    plan = seats
    if isinstance(config, loop_types.LoopConfig):
        cfg = config
    elif isinstance(config, Mapping):
        cfg = loop_types.LoopConfig.from_mapping(config)
    else:
        raise _refuse(TRIAL_ARGUMENT_INVALID, "config is a LoopConfig or a mapping")
    if not isinstance(surface, Surface):
        raise _refuse(TRIAL_ARGUMENT_INVALID, "surface is a surface.Surface")
    if mode != standard.MODE_ABSOLUTE:
        raise _refuse(
            TRIAL_MODE_UNEXPECTED,
            f"mode {mode!r} is not {standard.MODE_ABSOLUTE!r}; the relation "
            "trial of the standard is absolute and there is no other branch",
        )
    if isinstance(harness, PreparedTrial):
        prepared: PreparedTrial | None = harness
        live = prepared.harness
    else:
        prepared = None
        live = harness
    if getattr(live, "state", None) is None or getattr(live, "log", None) is None:
        raise _refuse(TRIAL_ARGUMENT_INVALID, "harness is not a live deepreason_core harness")
    if key is None and prepared is None:
        raise _refuse(
            TRIAL_ARGUMENT_INVALID, "key= is required: a trial names its cell"
        )
    try:
        cell = CellKey.coerce(key if key is not None else prepared.cell)
    except LoopError as exc:
        raise _refuse(TRIAL_ARGUMENT_INVALID, str(exc)) from exc
    if cell.is_register_cell:
        raise _refuse(
            TRIAL_MODE_UNEXPECTED,
            f"{cell.token} names a register cell; marks run pairwise through "
            "W4-MARKER's caller, not through the relation trial",
        )
    if prepared is not None and cell.token != prepared.cell:
        raise _refuse(
            TRIAL_ARGUMENT_INVALID,
            f"key {cell.token!r} disagrees with the prepared cell {prepared.cell!r}",
        )
    if records_dir is None:
        raise _refuse(
            TRIAL_ARGUMENT_INVALID,
            "records_dir= is required; every call record is write-once and "
            "run_trial never issues a call with nowhere to write it",
        )
    parsed = standard.standard_body(standard_body)
    standard_id = (
        prepared.standard_id if prepared is not None else _standard_id_in(live, parsed)
    )
    material_id = prepared.material_id if prepared is not None else None

    checks: dict[str, str] = {name: NOT_PERFORMED for name in GUARD_CHECKS}
    calls: list[CallRecord] = []
    blocks: list[Block] = []
    measures: list[int] = []
    rulings: dict[str, JudgeRuling] = {}
    paraphrase_rulings: dict[str, dict[str, JudgeRuling]] = {}
    packs_digest: dict[str, str] = {}
    critic: CriticOutput | None = None
    defender: DefenderOutput | None = None
    exchange: Exchange | None = None
    held: tuple[str, ...] = ()

    def finish(
        outcome: str,
        *,
        reading: ReadingResult | None = None,
        paraphrases: tuple[str, ...] = (),
    ) -> TrialResult:
        result = TrialResult(
            cell=cell.token,
            mode=mode,
            outcome=outcome,
            blocks=tuple(blocks),
            transcript="",
            checks=dict(checks),
            calls=tuple(calls),
            standard_id=standard_id,
            critic=critic,
            defender=defender,
            rulings=dict(rulings),
            paraphrases=paraphrases,
            paraphrase_rulings=dict(paraphrase_rulings),
            reading=reading,
            measures=tuple(measures),
            reopen_reason=reopen_reason,
            surface_digest=surface.digest if isinstance(surface, Surface) else "",
            exchange_digest=exchange.digest if exchange is not None else "",
            pack_digests=dict(packs_digest),
        )
        # G12 over the one emitted artifact this module authors, before its
        # text is emitted; the transcript's own assertion rides in build_transcript.
        result.as_dict()
        return result._replace(transcript=build_transcript(result))

    def declare(code: str, check: str, detail: str, of: RoleResult | None = None,
                outcome: str = OUTCOME_BLOCKED, **kwargs: Any) -> TrialResult:
        block, seq = _block(live, code, check, detail, default_id=default_id, of=of)
        blocks.append(block)
        measures.append(seq)
        return finish(outcome, **kwargs)

    # ---- the cell's prior standing, for G11 and the Measure inputs --------
    try:
        default_id = graph.cell_standing(live, cell).default_id
    except LoopError as exc:
        raise _refuse(
            TRIAL_PRIOR_STATE_UNREADABLE,
            f"{cell.token}: the cell's standing could not be read ({exc.detail})",
        ) from exc

    # ---- G0 constitution, pre-dispatch ------------------------------------
    constitution_failure = _constitution(plan)
    if constitution_failure is not None:
        checks[G0_CONSTITUTION] = NOT_PERFORMED
        return declare(CONSTITUTION_BLOCK, G0_CONSTITUTION, constitution_failure)
    checks[G0_CONSTITUTION] = PERFORMED

    # ---- G11 no re-reading for resolution, at the write --------------------
    _reopen_gate(
        live, cell, default_id=default_id, reopen_reason=reopen_reason, config=cfg
    )
    checks[G11_NO_REREAD] = PERFORMED

    # ---- the critic's pack ------------------------------------------------
    row_pack = render_row(surface, parsed, framing)
    packs_digest[roles.ROLES[0]] = pack_sha(row_pack)

    # ---- the critic ---------------------------------------------------------
    critic_call = roles.call_critic(
        plan.critic,
        row_pack,
        records_dir,
        coordinate=cell.token,
        provider_factory=provider_factory,
        seat_token=f"critic@{cell.token}",
    )
    calls.append(CallRecord("critic", cell.token, critic_call.coordinate.seat_label, critic_call))
    if critic_call.blocked:
        code = critic_call.block or SCHEMA_BLOCK
        return declare(
            code, G1_SCHEMA, critic_call.detail or critic_call.reason or code,
            of=critic_call,
        )
    checks[G1_SCHEMA] = PERFORMED
    critic = critic_call.output
    assert isinstance(critic, CriticOutput)

    # ---- G4 the closed vocabulary --------------------------------------------
    checks[G4_VOCABULARY] = PERFORMED
    if critic.is_outside_vocabulary:
        return declare(
            OUTSIDE_VOCABULARY_BLOCK,
            G4_VOCABULARY,
            "the critic preserved a reading outside the closed vocabulary; "
            "the cell stays unresolved and the text is on the call record",
            of=critic_call,
            outcome=OUTCOME_UNRESOLVED,
        )
    if critic.relation == contracts.NONE_RELATION:
        # §2.3: "none" ends the row at one call. It is an answer and not a
        # block - ``blocks`` stays empty - but the row WAS read, the cell is
        # left unresolved, and G11 reads a prior attempt off the Measure log.
        # Leaving no event made a `none` the one outcome a caller could re-read
        # freely, without a reopen_reason and without anything on the record
        # saying the row had been asked: the exact "retry until something
        # sticks" G11 exists to refuse, on the answer most likely to invite it.
        checks[G2A_UNIQUENESS] = NOT_PERFORMED
        checks[G3_OPERATIVE_TARGET] = NOT_PERFORMED
        event = live.record_measure(inputs=[default_id], llm=_llm_of(critic_call))
        measures.append(int(event.seq))
        return finish(OUTCOME_NO_TRIAL)

    # ---- G2(a) uniqueness on M ---------------------------------------------
    quote = critic.passage_quote
    offset = resolve_unique(surface, quote)
    if offset is None:
        count = surface.count(quote)
        detail = (
            f"the quoted passage resolves {count} times in the material"
            if count
            else "the quoted passage is nowhere in the material"
        )
        checks[G2A_UNIQUENESS] = PERFORMED
        return declare(
            REFERENTIAL_INTEGRITY_BLOCK, G2A_UNIQUENESS, detail, of=critic_call
        )
    checks[G2A_UNIQUENESS] = PERFORMED

    # ---- G3 operative target -------------------------------------------------
    if not within_declared_span(surface, offset):
        checks[G3_OPERATIVE_TARGET] = PERFORMED
        return declare(
            OPERATIVE_TARGET_BLOCK,
            G3_OPERATIVE_TARGET,
            "the quoted passage resolves only into the surface's own framing; "
            "a reading grounded in the prompt's scaffolding is not a reading "
            "of the material",
            of=critic_call,
        )
    checks[G3_OPERATIVE_TARGET] = PERFORMED
    held = held_spans_of(critic)

    # ---- the defender --------------------------------------------------------
    defender_pack = render_exchange(row_pack, critic)
    packs_digest["defender"] = pack_sha(defender_pack)
    defender_call = roles.call_defender(
        plan.defender,
        defender_pack,
        records_dir,
        coordinate=cell.token,
        provider_factory=provider_factory,
        seat_token=f"defender@{cell.token}",
    )
    calls.append(CallRecord("defender", cell.token, defender_call.coordinate.seat_label, defender_call))
    if defender_call.blocked:
        code = defender_call.block or SCHEMA_BLOCK
        return declare(
            code, G1_SCHEMA, defender_call.detail or defender_call.reason or code,
            of=defender_call,
        )
    defender = defender_call.output
    assert isinstance(defender, DefenderOutput)
    exchange = exchange_surface(critic.case, defender.answer)

    # ---- the judge ensemble, in both presentation orders -------------------
    if precedents is None:
        precedents = precedent_slice(live, standard_id)
    per_seat: dict[str, dict[str, JudgeRuling]] = {}
    per_seat_call: dict[str, dict[str, RoleResult]] = {}
    for seat_index, seat in enumerate(plan.judges):
        judge_pack = render_exchange(row_pack, critic, defender, precedents=precedents)
        for presented in both_orders(judge_pack):
            order_key = "" if presented.order == packs.ORDER_AS_DECLARED else "#order-swapped"
            coordinate = cell.token + order_key
            packs_digest[f"judge/{seat.label}/{presented.order}"] = pack_sha(presented)
            judge_call = roles.call_judge(
                seat,
                presented,
                records_dir,
                coordinate=coordinate,
                seat_index=seat_index,
                provider_factory=provider_factory,
                seat_token=f"{seat.label}@{cell.token}",
            )
            calls.append(
                CallRecord("judge", coordinate, judge_call.coordinate.seat_label, judge_call)
            )
            if judge_call.blocked:
                code = judge_call.block or SCHEMA_BLOCK
                rulings.update({
                    label: seat_rulings[packs.ORDER_AS_DECLARED]
                    for label, seat_rulings in per_seat.items()
                    if packs.ORDER_AS_DECLARED in seat_rulings
                })
                return declare(
                    code, G1_SCHEMA, judge_call.detail or judge_call.reason or code,
                    of=judge_call,
                )
            ruling = judge_call.output
            assert isinstance(ruling, JudgeRuling)
            per_seat.setdefault(seat.label, {})[presented.order] = ruling
            per_seat_call.setdefault(seat.label, {})[presented.order] = judge_call

    # ---- G2(b) the decisive point against E, for both orders of every seat ---
    for label, seat_rulings in per_seat.items():
        for order, ruling in seat_rulings.items():
            if exchange.resolve(ruling.decisive_point) is None:
                count = exchange.count(ruling.decisive_point)
                detail = (
                    f"the decisive point resolves {count} times in "
                    "case + newline + answer"
                    if count
                    else "the decisive point is absent from "
                    "case + newline + answer"
                )
                checks[G2B_UNIQUENESS] = PERFORMED
                rulings.update({
                    other: seat_map[packs.ORDER_AS_DECLARED]
                    for other, seat_map in per_seat.items()
                    if packs.ORDER_AS_DECLARED in seat_map
                })
                return declare(
                    REFERENTIAL_INTEGRITY_BLOCK, G2B_UNIQUENESS, detail,
                    of=per_seat_call[label][order],
                )
    checks[G2B_UNIQUENESS] = PERFORMED
    rulings = {
        label: seat_rulings[packs.ORDER_AS_DECLARED]
        for label, seat_rulings in per_seat.items()
    }

    # ---- G5 cross-family unanimity; never a majority, never an average -------
    # G5 compares the two SEATS at one presentation, and G6 compares one seat's
    # two presentations. Taking the union of both orders here made every G6 flip
    # report as `blocked:ensemble-split`: a seat that moved with the order was
    # named as a disagreement between the two families, which is a different
    # finding about a different thing and routes to a different Spawn. Design
    # 2.4 runs G5 before G6 for that reason, and each names its own fact.
    sustained_values = {
        label: ruling.sustained for label, ruling in rulings.items()
    }
    if len(set(sustained_values.values())) != 1:
        ordered = list(rulings.items())
        first = f"{ordered[0][0]} sustains={ordered[0][1].sustained}"
        second = f"{ordered[1][0]} sustains={ordered[1][1].sustained}"
        checks[G5_UNANIMITY] = PERFORMED
        return declare(
            ENSEMBLE_SPLIT_BLOCK,
            G5_UNANIMITY,
            f"{first} and {second}; both rulings are recorded verbatim on "
            "this trial and nothing is settled between them",
        )
    checks[G5_UNANIMITY] = PERFORMED

    # ---- G6 order-swap: one seat's two orders must not flip the outcome ------
    for label, seat_rulings in per_seat.items():
        declared = seat_rulings[packs.ORDER_AS_DECLARED]
        swapped = seat_rulings[packs.ORDER_SWAPPED]
        if declared.sustained != swapped.sustained:
            checks[G6_ORDER_SWAP] = PERFORMED
            return declare(
                ORDER_SWAP_BLOCK,
                G6_ORDER_SWAP,
                f"{label} sustains={declared.sustained} as-declared but "
                f"sustains={swapped.sustained} swapped; the answer moved "
                "with the presentation order",
                of=per_seat_call[label][packs.ORDER_SWAPPED],
            )
    checks[G6_ORDER_SWAP] = PERFORMED
    # Every seat and both of its orders now carry one value; the as-declared
    # one is the one the record cites.
    agreed = next(iter(sustained_values.values()))

    if not agreed:
        # §2.4 G7 guards *sustained* rulings only: a not-sustained ruling
        # registers nothing, and the Measure records the answered exchange.
        event = live.record_measure(inputs=[default_id], llm=None)
        measures.append(int(event.seq))
        return finish(OUTCOME_NOT_SUSTAINED)

    # ---- G7 the paraphrase spot-check ---------------------------------------
    variator_pack = render_paraphrase_request(exchange, held_spans=held)
    packs_digest["variator"] = pack_sha(variator_pack)
    variator_call = roles.call_variator(
        plan.variator,
        variator_pack,
        records_dir,
        coordinate=cell.token,
        paraphrase_n=int(standard.GUARD_PARAMETERS["paraphrase_n"]),
        provider_factory=provider_factory,
        seat_token=f"variator@{cell.token}",
    )
    calls.append(
        CallRecord("variator", cell.token, variator_call.coordinate.seat_label, variator_call)
    )
    if variator_call.blocked:
        code = variator_call.block or SCHEMA_BLOCK
        return declare(
            code, G7_PARAPHRASE, variator_call.detail or variator_call.reason or code,
            of=variator_call,
        )
    variator = variator_call.output
    assert isinstance(variator, VariatorOutput)
    paraphrases = tuple(variator.paraphrases)

    g7_performed = True
    for index, text in enumerate(paraphrases):
        token = f"#paraphrase-{index}"
        # §2.3: a paraphrase that did not hold a quoted span byte-identically
        # is discarded; no re-ruling is requested on it - which is the only
        # way "the spot-check did not pass" cannot be faked by skipping the
        # text the span no longer lives in.
        missing = [span for span in held if span not in text]
        if missing:
            g7_performed = False
            paraphrase_rulings[token] = {}
            continue
        par_surface = paraphrase_surface(text, of=exchange)
        re_pack = render_exchange(
            row_pack, critic, defender, precedents=precedents, exchange=par_surface
        )
        packs_digest[f"judge/re-ruling{token}"] = pack_sha(re_pack)
        seat_map: dict[str, JudgeRuling] = {}
        for seat_index, seat in enumerate(plan.judges):
            re_call = roles.call_judge(
                seat,
                re_pack,
                records_dir,
                coordinate=cell.token + token,
                seat_index=seat_index,
                provider_factory=provider_factory,
                seat_token=f"{seat.label}@{cell.token}{token}",
            )
            calls.append(
                CallRecord("judge", cell.token + token,
                           re_call.coordinate.seat_label, re_call)
            )
            if re_call.blocked:
                code = re_call.block or SCHEMA_BLOCK
                paraphrase_rulings[token] = dict(seat_map)
                checks[G7_PARAPHRASE] = PERFORMED if g7_performed else NOT_PERFORMED
                return declare(
                    code, G7_PARAPHRASE, re_call.detail or re_call.reason or code,
                    of=re_call, paraphrases=paraphrases,
                )
            re_ruling = re_call.output
            assert isinstance(re_ruling, JudgeRuling)
            seat_map[seat.label] = re_ruling
        paraphrase_rulings[token] = seat_map
        del re_pack

    # Any flip against the trial's answer, or any split between the two
    # seats on one paraphrase, is blocked:paraphrase-flip and is logged
    # against the seat whose ruling moved.
    for token, seat_map in paraphrase_rulings.items():
        if not seat_map:
            continue  # span lost on this paraphrase: not performed, never passed
        for label, re_ruling in seat_map.items():
            if re_ruling.sustained != agreed:
                flip_call = per_seat_call.get(label, {}).get(packs.ORDER_AS_DECLARED)
                checks[G7_PARAPHRASE] = PERFORMED if g7_performed else NOT_PERFORMED
                return declare(
                    PARAPHRASE_FLIP_BLOCK,
                    G7_PARAPHRASE,
                    f"{label} sustains={re_ruling.sustained} on the "
                    f"paraphrase {token} and the trial's answer stands at "
                    f"sustains={agreed}; the ruling moved with the wording, "
                    f"against {label}",
                    of=flip_call,
                    paraphrases=paraphrases,
                )
    checks[G7_PARAPHRASE] = PERFORMED if g7_performed else NOT_PERFORMED

    # ---- the hand-off --------------------------------------------------------
    decided = rulings[plan.judges[0].label]
    transcript = Transcript(
        case=critic.case,
        answer=defender.answer,
        decisive_point=decided.decisive_point,
        checks=dict(checks),
        meta={
            # Only the record's own coordinates and digests: never the
            # vendored reserved keys (graph.Transcript refuses them), and
            # only the decisive point's *string*, never the transcript's
            # verdict-bearing blob (W1-GRAPH's G12_EXEMPT boundary).
            "cell": cell.token,
            "surface_digest": surface.digest,
            "offset": offset.as_dict(),
            "exchange_digest": exchange.digest,
            "pack_digests": dict(packs_digest),
        },
    )
    # The program's stronger G2(b) ran above; the vendored predicate is
    # re-asserted here, at the moment the transcript exists, so the guard and
    # the registration gate W4-READER will pass through cannot diverge.
    transcript.validated()
    checks[G12_NO_SCORING_KEY] = PERFORMED
    reading = ReadingResult(
        key=cell,
        relation=critic.relation,
        seat=plan.judges[0].label,
        transcript=transcript,
        body={
            "surface_digest": surface.digest,
            "offset": offset.as_dict(),
            "pack_digests": dict(packs_digest),
        },
        roles={label: label for label in rulings},
        material_id=material_id,
    )
    return finish(OUTCOME_SUSTAINED, reading=reading, paraphrases=paraphrases)


def _standard_id_in(harness: Any, parsed: Mapping[str, Any]) -> str:
    """The registered standard artifact's id, found, never guessed.

    A trial cites the standard the graph carries under exactly those bytes;
    if no registered artifact holds this body the trial refuses to be formed,
    because the case-law closure only arms against what is registered.
    """

    digest = sha256_hex(canonical_json(dict(parsed)))
    for artifact_id, artifact in getattr(harness.state, "artifacts", {}).items():
        ref = str(getattr(artifact, "content_ref", ""))
        if not ref or getattr(artifact, "codec", None) != graph.CODEC_JSON:
            continue
        try:
            raw = harness.blobs.get(ref)
        except (KeyError, OSError, ValueError):
            continue
        if not isinstance(raw, (bytes, bytearray)):
            continue
        if sha256_hex(bytes(raw)) == digest:
            return artifact_id
    raise _refuse(
        TRIAL_PRIOR_STATE_UNREADABLE,
        "the standard body handed to run_trial is not registered in this "
        "harness; register_standard runs first",
    )


del json  # imported only as a guard of last resort; nothing here parses JSON
