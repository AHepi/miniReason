"""W0-TYPES - shared types, closed vocabularies and layout constants for the loop.

Implements the wave-0 module ``W0-TYPES`` of *The automated end-to-end harness
loop - FINAL design of record*: the ``minireason.loop.config.v1`` schema and its
strict loader (design section 4.2), ``loop_plan_id`` (4.2), the
``minireason.loop.step.v1`` receipt and its ``step_key`` (4.3), the stop
vocabulary (4.4), the guard block reason codes (2.4), the operational failure
codes (4.4) and the run directory layout (4.2).

Nothing here decides anything. Every name below is a closed vocabulary, a
record shape or a path: no clause of this module reads a quantity, orders a
vocabulary, or turns a count into a warrant. ``resource_boundary`` names a
declared budget - an attention-and-spend boundary, never a claim that an
inquiry ran out of things to say - and the stop vocabulary carries no token
that would say otherwise (``tests/loop/test_types.py`` names the token it
must never carry).

Canonical JSON is :func:`deepreason_core.canonical.canonical_json`, reused
rather than retyped; it is byte-identical to ``minireason.provider.digest``'s
and ``provider_openai_compat.digest``'s serialisation
(``sort_keys=True``, ``separators=(",", ":")``, ``ensure_ascii=False``), so a
digest taken here and one taken by runner v2 agree.

Deviations from the design, and why
-----------------------------------

*  **The step receipt carries ``wave``.** Section 4.3's sample record omits it
   while the same section's ``step_key`` formula reads it. A receipt that
   cannot recompute its own key from its own bytes is not checkable, so the
   field is present and ``None`` on the steps that have no wave.
*  **``step_key`` and ``loop_plan_id`` hash a named envelope**, not a
   positional tuple / a literal key union: ``{"kind": ..., "cycle": ...}``
   rather than ``canonical(loop_plan_id, kind, cycle, ...)``, and
   ``{"config": ..., "pins": ...}`` rather than ``config`` union ``pins``. The
   union is ambiguous (a pinned path could shadow a config key) and a
   positional tuple is silently reorderable. Both envelopes carry a schema
   token so the digest says what it is a digest of.
*  **A receipt validates its own ``step_key``, and its ``spending`` flag must
   match the design's classification of its kind** (4.3). Both are derivable,
   and a record that could disagree with the rule it is written under is a
   record that can lie.
*  **``blocked:constitution`` is added to** :data:`BLOCK_CODES`. G0 leaves
   *coordinates* ``NOT_DISPATCHED`` (an operational reason, never a semantic
   result - that stays in :data:`FAILURE_CODES`), but G0 also runs inside
   ``run_trial``, whose acceptance requires every block path to carry a code
   from this set. It is the **one** member of :data:`BLOCK_CODES` the frozen
   ceiling does not name; the other nine are exactly the nine reason codes
   ``standard.CEILING_TEXT``'s block-register clause promises are "printed
   with counts on every table", and a test asserts that correspondence in both
   directions.
*  **An open step marker is ``NNNN-KIND.json.open``**, the spelling of section
   4.2's layout block; section 4.3's prose spells the same marker
   ``.open.json``. Both are exposed through one call
   (:meth:`RunPaths.step_path`) so the two spellings cannot drift apart in
   downstream modules.
*  **Seat names and ``publish_ref`` may be absent.** Section 2.2 draws seats
   from the endpoint registry by a deterministic rule, so a config that names
   none is complete; ``None``/empty means "assign by W1-SEATS' rule". Section
   4.2's CLI defaults ``--publish-ref`` to the branch's upstream, so ``None``
   means that.
*  **``provider_mode`` defaults to ``offline``.** A config that does not
   declare a spending mode does not spend.
*  **``LoopError`` does not enforce** :data:`FAILURE_CODES` **membership.**
   Later waves own codes this module cannot enumerate; the shape
   (``^[A-Z][A-Z0-9_]*$``) is enforced and the declared set is exported for
   the modules that can check it.
*  **``loop_plan_id`` requires every member of** :data:`PINNED_SOURCE_PATHS`.
   That constant is named "the fixed part of the identity", and an id computed
   over a pin map that omits one of the six is an id for a different plan than
   the one it claims to name. The run-specific rest of design 4.2's list stays
   the caller's to supply, and a missing fixed pin is ``PIN_INVALID`` naming
   the paths that are absent.

What this module does **not** promise
-------------------------------------

*  **A record validates at its named door, not at the constructor.**
   :class:`LoopConfig` and its four sub-records validate in ``from_mapping``;
   constructing one directly with prepared values performs no check beyond the
   dataclass's own. :class:`StepReceipt` and :class:`CustodyReport` do have a
   ``__post_init__`` and so validate at every door.
*  **These frozen records are not hashable.** ``inputs_sha256`` and
   ``outputs_sha256`` are held as ``MappingProxyType``, so ``hash(receipt)``
   raises ``TypeError`` - not a :class:`LoopError`. A caller that needs a set
   of steps keys it by ``step_key`` or by a coordinate of its own.
*  **``step_key`` is not tamper-evidence.** It binds five of the receipt's
   sixteen fields (see :meth:`StepReceipt.key`); a reader who needs the
   record's bytes digests the file.

The code tables, and the one rule that partitions them
------------------------------------------------------

Wave 0 raises five sibling exception classes - ``contracts.ContractError``,
``standard.StandardInvalid``, ``custody.CustodyMismatch``,
``receipts.ReceiptError`` and ``publish.PublishError``. Every one of them is a
subclass of :class:`LoopError` (keeping the base it already had, so an existing
``except ValueError`` / ``except FileExistsError`` still catches it), so every
one of them carries a ``.code``. **Membership is not enforced when the
exception is raised** - a later wave owns codes this module cannot enumerate -
but the tables below must be *complete for wave 0*, because the operator page
lists them.

The rule ``tests/loop/test_types.py`` enforces, in one sentence:

    Every string literal in ``src/minireason/loop/*.py`` that can reach a
    record as a stable token - the first argument of a loop exception
    constructor (or of ``super().__init__`` inside one of their subclasses, or
    of a module-private ``_fail`` helper that builds one), the ``reason``
    argument of ``contracts.SchemaInvalid``, and any ``code = "..."`` class
    attribute - belongs to exactly one declared table, and its **spelling says
    which**: ``blocked:<name>`` to :data:`BLOCK_CODES`, ``<lower-with-hyphens>``
    to ``contracts.SCHEMA_REASONS``, ``UPPER_SNAKE_CASE`` to
    :data:`FAILURE_CODES` - or, for the one token that names something the loop
    *did* rather than something it refused, to :data:`OUTCOME_CODES`. The four
    tables are pairwise disjoint and the test asserts it.

``custody.CUSTODY_CODES`` is the custody-only slice of :data:`FAILURE_CODES`
rather than a rival table: a halt receipt records one code, so there is one
place a reader looks it up. The same test asserts ``CUSTODY_CODES`` is a
subset. ``contracts.SCHEMA_REASONS`` is a genuinely different grain - its
members are the sub-reasons of the single block code ``blocked:schema``, not
codes a receipt's ``failure_code`` may carry - which is why it is spelled in
lower case and is disjoint from both other tables.

Underspecified signatures resolved here, documented for the waves that import
them: ``run_paths(root, run_id)`` takes the **repository root** and returns the
tree under ``<root>/experiments/loops/<run_id>``; ``loop_plan_id(config, pins)``
accepts either a :class:`LoopConfig` or a raw mapping (validated identically,
so both give one id); ``StepReceipt`` is a frozen record with ``as_dict`` /
``from_dict`` and a static ``key``.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from deepreason_core.canonical import canonical_json, sha256_hex

__all__ = [
    # schemas and layout
    "CONFIG_SCHEMA",
    "STEP_SCHEMA",
    "PLAN_ID_SCHEMA",
    "STEP_KEY_SCHEMA",
    "LOOPS_ROOT",
    "PINNED_SOURCE_PATHS",
    # closed vocabularies
    "STOP_REASONS",
    "PREREGISTERED_CONDITION_PREFIX",
    "is_stop_reason",
    "BLOCK_CODES",
    "BLOCK_CODE_PREFIX",
    "CEILING_BLOCK_REASONS",
    "block_code",
    "FAILURE_CODES",
    "is_failure_code",
    "HTTP_STATUS_PREFIX",
    "NO_REPLAY",
    "OUTCOME_CODES",
    "is_outcome_code",
    "STEP_KINDS",
    "REPLAYABLE_STEPS",
    "SPENDING_STEPS",
    "STEP_STATUSES",
    "PROVIDER_MODES",
    # errors
    "LoopError",
    # config
    "SeatsConfig",
    "ContrastConfig",
    "AuditConfig",
    "TimeoutsConfig",
    "LoopConfig",
    "loop_plan_id",
    # step receipts
    "CustodyReport",
    "StepReceipt",
    # run layout
    "CyclePaths",
    "RunPaths",
    "run_paths",
]


# --------------------------------------------------------------------------
# Schemas, layout constants
# --------------------------------------------------------------------------

#: The frozen loop configuration (design 4.2).
CONFIG_SCHEMA = "minireason.loop.config.v1"
#: One write-once step receipt (design 4.3).
STEP_SCHEMA = "minireason.loop.step.v1"
#: The envelope ``loop_plan_id`` digests.
PLAN_ID_SCHEMA = "minireason.loop.plan-id.v1"
#: The envelope ``StepReceipt.key`` digests.
STEP_KEY_SCHEMA = "minireason.loop.step-key.v1"

#: Run directories live here, under the repository root (design 4.2).
LOOPS_ROOT = "experiments/loops"

#: The fixed repo-relative files design 4.2 pins into ``loop_plan_id``. The
#: rest of that list - prompt templates, ``obligations.json``, ``CEILING.md``,
#: the standard body, each attached study's ``PLAN.md`` and ``material.json`` -
#: is run-specific and is supplied by the caller of :func:`loop_plan_id`.
PINNED_SOURCE_PATHS: tuple[str, ...] = (
    "src/minireason/data/endpoints.json",
    "src/minireason/graph_import_h005.py",
    "src/minireason/provider_openai_compat.py",
    "src/minireason/use_relation_h005.py",
    "tools/contrast_triple_study.py",
    "tools/multicycle_commitment_study_multi_v2.py",
)


# --------------------------------------------------------------------------
# Closed vocabularies
# --------------------------------------------------------------------------

#: Design 4.4's stop vocabulary. ``preregistered_condition:<id>`` is the one
#: parameterised member; :func:`is_stop_reason` admits it.
STOP_REASONS: frozenset[str] = frozenset({
    "protected_loss",
    "obligations_discharged",
    "no_new_reading_changes",
    "resource_boundary",
    "custody_halt",
    "all_arms_ended",
    "instrument_fault",
})

PREREGISTERED_CONDITION_PREFIX = "preregistered_condition:"

#: The write-once refusal, owned here (wave-2 integration, Kimi family-C judge
#: finding 2). It was a member of :data:`FAILURE_CODES` and nothing more, so
#: ``roles.py`` retyped the literal to have a name to raise: two spellings of one
#: token, and a rename in one of them would have been silent. This module
#: declares it, :data:`FAILURE_CODES` is built from the constant, and
#: ``roles.NO_REPLAY`` is an import of this name. The *raising* of it is still
#: runner v2's and W2-ROLES'; the *spelling* is this module's, like every other
#: member of the tables.
NO_REPLAY = "NO_REPLAY"

#: Design 2.4's guard blocks. A block registers nothing, leaves the cell
#: unresolved and is counted by its code; a high block rate is the instrument
#: declining to read and is never an absence of relations.
#:
#: Nine of the ten are exactly the reason codes the frozen ceiling's
#: block-register clause names, in the order it names them, and promises are
#: "printed with counts on every table"; ``blocked:constitution`` is the one
#: extra (G0, above). Three of the nine are reached by a route section 2.4
#: spells differently - ``outside-vocabulary`` is G4's forced-``unresolved``
#: reason, ``provider`` is section 4.4's delivery failure ending an arm, and
#: ``baseline-forced-same`` is G9's program writing ``same`` over a ``differs``
#: - but the ceiling promises **one** register printed with counts, so there is
#: one table, and a renderer that printed only the seven guard-internal blocks
#: would under-report the instrument declining to read.
BLOCK_CODES: frozenset[str] = frozenset({
    "blocked:ensemble-split",
    "blocked:referential-integrity",
    "blocked:operative-target",
    "blocked:order-swap",
    "blocked:paraphrase-flip",
    "blocked:outside-vocabulary",
    "blocked:schema",
    "blocked:provider",
    "blocked:baseline-forced-same",
    "blocked:constitution",
})

#: The nine the ceiling names, in the ceiling's own order, without the
#: ``blocked:`` prefix it prints them under. Exported so the reconciliation
#: test and W3-REPORT read one list rather than re-parsing prose.
CEILING_BLOCK_REASONS: tuple[str, ...] = (
    "ensemble-split",
    "referential-integrity",
    "operative-target",
    "order-swap",
    "paraphrase-flip",
    "outside-vocabulary",
    "schema",
    "provider",
    "baseline-forced-same",
)

#: ``blocked:`` + a ceiling reason. The spelling convention for every member of
#: :data:`BLOCK_CODES`, stated once so no caller retypes the prefix.
BLOCK_CODE_PREFIX = "blocked:"


def block_code(reason: str) -> str:
    """``blocked:<reason>``, refusing a reason :data:`BLOCK_CODES` does not carry."""

    code = BLOCK_CODE_PREFIX + str(reason)
    if code not in BLOCK_CODES:
        raise _fail("BLOCK_CODE_UNKNOWN", f"{reason!r} is not a declared block reason")
    return code

#: Operational codes. Every member names a delivery, custody, publication,
#: step, standard, receipt or configuration fact. None of them is a semantic
#: result about any material under study, and none may be rendered as one.
#:
#: The table is **complete for waves 0, 1 and 2** - all sixteen modules: every
#: UPPER_SNAKE token any of them can put on an exception's ``.code`` is here,
#: grouped by the module that raises it, and ``tests/loop/test_types.py`` scans
#: the package sources and fails if one is missing. A module still being written
#: in another wave is listed there as not yet folded in; its author adds its
#: codes here in the commit that lands it (O9). Membership is still not enforced
#: at raise time (see :class:`LoopError`).
#:
#: One wave-1 token is deliberately **not** here: ``APPELLATE_RULING_APPLIED``
#: names an induced *outcome* the dry run produces, not an operational failure,
#: and it lives in :data:`OUTCOME_CODES` instead.
FAILURE_CODES: frozenset[str] = frozenset({
    # provider / delivery (provider_openai_compat's and runner v2's own codes)
    "HTTP_429",
    "KEY_MISSING",
    "TRANSPORT_OR_RESPONSE_ERROR",
    "SECRET_IN_REQUEST",
    "CONCURRENCY_LIMIT_CONFLICT",
    NO_REPLAY,
    "NOT_DISPATCHED",
    "INDETERMINATE",
    # custody: the aggregate names, plus every member of custody.CUSTODY_CODES
    "CUSTODY_MISMATCH",
    "REQUEST_NOT_FROM_PLAN",
    "ARTIFACT_NOT_DERIVED_FROM_DELIVERY",
    "TIMEOUT_NOT_APPLIED",
    "PROVIDER_REQUEST_FILE_CHANGED",
    "TRANSPORT_PIN_MISMATCH",
    "INPUT_NOT_PUBLISHED",
    "RUNTIME_SOURCE_CHANGED",
    "CREDENTIAL_IN_OUTPUT",
    "CREDENTIAL_SCAN_INCOMPLETE",
    "PATH_ESCAPES_RUN_ROOT",
    "PATH_NOT_RESOLVABLE",
    "PIN_MAP_MISSING",
    "RECORD_NOT_SERIALISABLE",
    "RECORD_WRITE_FAILED",
    "SOURCE_PIN_MALFORMED",
    "SOURCE_PIN_MISMATCH",
    "SOURCE_PIN_MISSING",
    "SOURCE_PIN_NOT_A_FILE",
    "SOURCE_PIN_OUTSIDE_REPOSITORY",
    "WRITE_ONCE_VIOLATION",
    # publication (loop/publish.py)
    "PUBLISH_PENDING",
    "PUBLISH_REF_CHANGED",
    "PUBLISH_REF_UNRESOLVED",
    "PUBLISH_REF_INVALID",
    "PUBLISH_PATHS_EMPTY",
    "PUBLISH_PATHS_UNTRACKED",
    "PUBLISH_MESSAGE_EMPTY",
    "PUBLISH_ATTEMPT_INVALID",
    "PUBLISH_NOT_CONVERGING",
    "GIT_OPERATION_FAILED",
    "HISTORY_REWRITE_REFUSED",
    "GIT_SUBCOMMAND_NOT_ALLOWED",
    "SECRET_IN_STAGED_DIFF",
    "UNEXPECTED_STAGED_FILES",
    "REPO_NOT_A_GIT_CHECKOUT",
    "CHECK_TARGET_UNKNOWN",
    "PATH_NOT_EXPLICIT",
    "PATH_IS_REPO_ROOT",
    "PATH_OUTSIDE_REPO",
    "PATH_MISSING",
    # receipts and the activity log (loop/receipts.py)
    "SECRET_IN_RECEIPT",
    "LEDGER_NOT_FOUND",
    "LEDGER_EMPTY_PARAGRAPH",
    "LEDGER_INCOMPLETE_WRITE",
    "LEDGER_APPEND_NOT_VERIFIED",
    "LEDGER_APPEND_REENTERED",
    "ACTIVITY_PATH_INVALID",
    "CADENCE_THRESHOLD_INVALID",
    "RECEIPT_ID_MALFORMED",
    "RECEIPT_SUFFIX_MALFORMED",
    "RECEIPT_FORM_MALFORMED",
    "RECEIPT_BODY_AMBIGUOUS",
    "RECEIPT_FIELDS_MISSING",
    "PREREGISTRATION_SENTENCE_MISSING",
    "ACTIVITY_PHASE_UNKNOWN",
    "ACTIVITY_DECISION_MISSING",
    "ACTIVITY_TOOL_MISSING",
    "ACTIVITY_LOGGER_FAILED",
    "ACTIVITY_RAW_COMMAND_TEXT",
    "ACTIVITY_CONTROL_CHARACTER",
    "CADENCE_BACKDATED",
    "CADENCE_THRESHOLDS_INVERTED",
    "MOMENT_NOT_AWARE",
    "MOMENT_NOT_DATETIME",
    # the standard artifact (loop/standard.py)
    "STANDARD_ARGUMENT_REFUSED",
    "STANDARD_BODY_MALFORMED",
    "STANDARD_DATA_MISSING",
    "STANDARD_DATA_MALFORMED",
    "CEILING_TEXT_MALFORMED",
    "PLAN_MIRROR_MALFORMED",
    "STANDARD_SCHEMA_MISMATCH",
    "STANDARD_SECTION_MISSING",
    "SPEC_ID_MISMATCH",
    "REGISTER_SET_MISMATCH",
    "REGISTER_TEXT_EMPTY",
    "DIFFERENCE_KIND_SET_EMPTY",
    "DIFFERENCE_KIND_DUPLICATE",
    "VOCABULARY_EMPTY",
    "VOCABULARY_DUPLICATE",
    "VOCABULARY_NOT_CLOSED",
    "UNRESOLVED_NOT_IN_VOCABULARY",
    "GUARD_PARAMETER_UNKNOWN",
    "GUARD_PARAMETER_MISSING",
    "GUARD_PARAMETER_INVALID",
    "REOPEN_REASON_SET_EMPTY",
    "REOPEN_REASON_UNKNOWN",
    "RESOURCE_BOUNDARY_MISDESCRIBED",
    # role contracts (loop/contracts.py); the sub-reason rides on .reason
    "SCHEMA_INVALID",
    "CONTRACT_VIOLATION",
    # steps (loop/steps.py, W1-STEPS; the last five folded in by the wave-1
    # integrator from that module's own NEW_CODES table)
    "UNRESOLVED_STEP",
    "STEP_NONDETERMINISTIC",
    "STEP_TIMEOUT",
    "STEP_KEY_MISMATCH",
    "STEP_RECEIPT_INVALID",
    "PLAN_ID_MISMATCH",
    "BUDGET_RAISED",
    "RUN_LOCKED",
    "STEP_BODY_FAILED",
    "STEP_CLASS_DISAGREEMENT",
    "STEP_NOT_HALTED",
    "STEP_OUTPUTS_INVALID",
    # the pre-registered obligations document (loop/obligations.py,
    # W1-OBLIGATIONS). Every one is a refusal to read a document or a
    # situation; none is a verdict, which is always one of the three tokens.
    "OBLIGATIONS_FILE_MISSING",
    "OBLIGATIONS_MALFORMED",
    "OBLIGATIONS_NOT_A_MAPPING",
    "OBLIGATIONS_SCHEMA_UNKNOWN",
    "OBLIGATIONS_UNKNOWN_KEY",
    "OBLIGATIONS_MISSING_KEY",
    "OBLIGATIONS_DIGEST_MISMATCH",
    "OBLIGATIONS_PIN_SHIFTED",
    "OBLIGATION_FIELD_MISSING",
    "OBLIGATION_FIELD_INVALID",
    "OBLIGATION_ID_MALFORMED",
    "OBLIGATION_ID_DUPLICATE",
    "OBLIGATION_IN_BOTH_SETS",
    "OBLIGATION_MEMBERSHIP_UNKNOWN",
    "OBLIGATION_CHECK_UNKNOWN",
    "OBLIGATION_UNKNOWN",
    "PREDICATE_CONTRACT_VIOLATED",
    "SITUATION_INVALID",
    # how readings and marks enter the graph (loop/graph.py, W1-GRAPH). Every
    # one is a formation refusal: nothing here is a standing, and no status is
    # ever named by a code (the adjudication computes those).
    "GRAPH_ROOT_INVALID",
    "GRAPH_READ_ONLY",
    "IDENTIFIER_INVALID",
    "APPEAL_MALFORMED",
    "APPEAL_TARGET_UNKNOWN",
    "CELL_KEY_INVALID",
    "CELL_NOT_OPEN",
    "STANDARD_NOT_REGISTERED",
    "READING_TOKEN_UNKNOWN",
    "READING_TOKEN_UNRESOLVED",
    "MARK_REGISTER_MISSING",
    "MARK_REGISTER_UNEXPECTED",
    "DIFFERENCE_KIND_UNKNOWN",
    "DIFFERENCE_KIND_UNEXPECTED",
    "TRANSCRIPT_MALFORMED",
    "TRANSCRIPT_POINT_NOT_UNIQUE",
    "TRANSCRIPT_NOT_CONFORMING",
    "AUDIT_KIND_UNKNOWN",
    "REGISTRATION_REFUSED",
    # the offline dry-run fixture (loop/synthetic.py, W1-SYNTHETIC). Its third
    # token, APPELLATE_RULING_APPLIED, is an outcome and is in OUTCOME_CODES.
    "SYNTHETIC_INDUCTION_UNKNOWN",
    "SYNTHETIC_COORDINATE_UNSCRIPTED",
    # seat assignment (loop/seats.py, W1-SEATS - folded in by the wave-1 author's
    # own NEW_CODES table, which names the reason for each)
    "SEAT_COUNT_INSUFFICIENT",
    "REGISTRY_INVALID",
    "RUNNER_NOT_IMPORTABLE",
    # the resolvable surface (loop/surface.py, W1-SURFACE)
    "SURFACE_ROW_MALFORMED",
    "SURFACE_SPAN_DISAGREES",
    "SURFACE_NO_MATERIAL",
    # guard and instrument
    "BASELINE_NOT_FIRST",
    "SCORING_KEY_FORBIDDEN",
    "FAMILY_COUNT_INSUFFICIENT",
    "NEW_PREREGISTRATION_REQUIRED",
    "REOPEN_REFUSED",
    "BLOCK_CODE_UNKNOWN",
    "STOP_REASON_UNKNOWN",
    # pack rendering (loop/packs.py, W2-PACKS), folded in by the wave-2
    # integrator from that module's own NEW_CODES table. Every one is a refusal
    # to RENDER: none of them is a reading, a mark or a standing.
    "PACK_INPUT_INVALID",
    "PACK_ADJUDICATION_KEY",
    "EXCHANGE_MALFORMED",
    "PRECEDENT_QUERY_INVALID",
    # role dispatch (loop/roles.py, W2-ROLES). PROVIDER_GATEWAY_WALL is the one
    # of the ten that no exception carries: it is a *reason* recorded on a
    # returned blocked result beside the transport's own code, so it is listed
    # in the test's UNREACHED table with HTTP_429 and the rest of the delivery
    # facts the loop records rather than raises.
    "PROVIDER_GATEWAY_WALL",
    "ROLE_UNKNOWN",
    "ROLE_SEAT_MISMATCH",
    "ROLE_COORDINATE_INVALID",
    "ROLE_PACK_INVALID",
    "ROLE_PACK_NOT_JSON_MODE_READY",
    "ROLE_SCHEMA_NOT_THE_CONTRACT",
    "ROLE_REGISTER_REQUIRED",
    "ROLE_REPAIR_REFUSED",
    "ROLE_TOKEN_BUDGET_UNREACHABLE",
    # the C001 program pre-pass and the sealed baseline (loop/markprep.py,
    # W2-MARKPREP). BASELINE_NOT_FIRST is already declared above and is one
    # refusal with one name whether the pack or the residue trips it.
    "MARKPREP_INPUT_MALFORMED",
    "COMPARISON_SCHEMA_UNKNOWN",
    "CELL_NOT_IN_OCCURRENCE",
    "REPLICATE_BYTES_DISAGREE",
    "BASELINE_RESEALED",
    "BASELINE_SEAL_BROKEN",
    "REGISTER_UNKNOWN",
    "REPLICATE_UNKNOWN",
    "REPLICATE_NOT_READABLE",
    # the pre-registered stop/continue program (loop/decide.py, W2-DECIDE).
    # Every one is a refusal to DECIDE on a malformed input; the outcome
    # vocabulary is STOP_REASONS and is not here.
    "DECISION_SITUATION_INVALID",
    "DECISION_CYCLE_INVALID",
    "DECISION_CONFIG_INVALID",
    "DECISION_INSTRUMENT_INVALID",
    "DECISION_WOULD_REOPEN_MISSING",
    "DECISION_REASON_UNKNOWN",
    # configuration and layout (raised by this module)
    "CONFIG_NOT_A_MAPPING",
    "CONFIG_NOT_FOUND",
    "CONFIG_SCHEMA_UNKNOWN",
    "CONFIG_UNKNOWN_KEY",
    "CONFIG_MISSING_KEY",
    "CONFIG_INVALID_VALUE",
    "PIN_INVALID",
    "RUN_ID_INVALID",
    "PATH_INVALID",
    "CYCLE_OUT_OF_RANGE",
})

#: Outcomes, not failures. An UPPER_SNAKE token a record may carry to name
#: **something the loop did**, where :data:`FAILURE_CODES` names something it
#: refused. The two tables are disjoint by construction and a token belongs to
#: exactly one of them, because a reader who cannot tell a refusal from a result
#: cannot read the closing record.
#:
#: The table is small on purpose, and it is not a place to move an awkward
#: failure to: a member is a thing that *happened and was meant to happen*, and
#: the value is the reason it is declared rather than left as prose.
OUTCOME_CODES: Mapping[str, str] = MappingProxyType({
    "APPELLATE_RULING_APPLIED":
        "an appellate ruling was ingested and pass 1 recomputed under it, so a "
        "label moved. W1-SYNTHETIC induces exactly this in the dry run and the "
        "closing receipt names it; it is never a refusal and never a block.",
})


def is_outcome_code(code: Any) -> bool:
    """True for a declared outcome token (never a member of :data:`FAILURE_CODES`)."""

    return isinstance(code, str) and code in OUTCOME_CODES


#: The S0-S15 transitions of design 4.1, plus ``AUDIT`` - section 4.3 classes
#: it as a spending step, and section 2.5 runs it inside ``ADJUDICATE`` on a
#: schedule, so it resolves its own marker rather than its parent's.
STEP_KINDS: tuple[str, ...] = (
    "PREREGISTER", "PREFLIGHT", "PUBLISH_PLAN", "CYCLE_OPEN", "PREPARE",
    "PUBLISH_IN", "SEND", "PUBLISH_EV", "IMPORT", "USE_TABLE", "READ", "MARK",
    "ADJUDICATE", "AUDIT", "DECIDE", "PUBLISH_CY", "CLOSE",
)

#: Offline, deterministic and pure: re-run on resume, and byte-identical
#: outputs are asserted (design 4.3).
REPLAYABLE_STEPS: frozenset[str] = frozenset({
    "PREFLIGHT", "IMPORT", "USE_TABLE", "ADJUDICATE", "DECIDE",
})

#: A call may have been billed, or a remote may have moved: an open marker is
#: written before the step and an unresolved marker halts on resume.
SPENDING_STEPS: frozenset[str] = frozenset({
    "SEND", "READ", "MARK", "AUDIT",
    "PUBLISH_PLAN", "PUBLISH_IN", "PUBLISH_EV", "PUBLISH_CY",
})

STEP_STATUSES: tuple[str, ...] = ("COMPLETE", "FAILED", "HALTED")

#: Mirrors ``multicycle_commitment_study_multi_v2.PROVIDER_MODES``.
PROVIDER_MODES: tuple[str, ...] = ("live", "offline")


# ---- BEGIN REFUSED TOKEN ---------------------------------------------------
# The one region of this module that may spell the token the loop never claims.
# Everything between these two markers exists to REFUSE it; the rest of the file
# does not contain it, and ``tests/loop/test_types.py`` asserts exactly that by
# splitting the source on these markers. This is the same exemption the frozen
# ceiling's denial sentence has in W0-STANDARD (S5): a denial must name what it
# denies, and a guard must name what it refuses.

#: The stem no stop reason may carry, in any case - not as a member of
#: :data:`STOP_REASONS`, and not inside the id of a
#: ``preregistered_condition:``. A run that stopped spent its declared boundary;
#: it never ran out of things to say, and the one member of the stop vocabulary
#: that takes an argument is the one door that would let a record say otherwise.
_REFUSED_STOP_STEM = "exhaust"


def is_stop_reason(token: Any) -> bool:
    """True for a member of :data:`STOP_REASONS` or ``preregistered_condition:<id>``.

    The parameterised tail is an identifier, and an identifier carrying
    :data:`_REFUSED_STOP_STEM` in any case is refused: a condition id spelled
    ``inquiry_exhausted`` would put the one claim the ceiling denies into the
    closing record through the vocabulary's one open argument.
    """

    if not isinstance(token, str) or not token:
        return False
    if token in STOP_REASONS:
        return True
    if not token.startswith(PREREGISTERED_CONDITION_PREFIX):
        return False
    condition = token[len(PREREGISTERED_CONDITION_PREFIX):]
    if _REFUSED_STOP_STEM in condition.casefold():
        return False
    return bool(_ID.fullmatch(condition))

# ---- END REFUSED TOKEN -----------------------------------------------------


#: The one parameterised family of :data:`FAILURE_CODES`, as
#: ``preregistered_condition:<id>`` is of :data:`STOP_REASONS` (wave-1
#: integration decision 42(b)). The transport raises ``HTTP_<status>`` for
#: every status it meets, not only the ``429`` the table lists by name, and a
#: receipt carrying ``HTTP_503`` was carrying a code no table declared.
#: ``HTTP_429`` stays an explicit member: it is the one the design names.
HTTP_STATUS_PREFIX = "HTTP_"

_HTTP_STATUS = re.compile(r"HTTP_[1-5][0-9][0-9]\Z")


def is_failure_code(code: Any) -> bool:
    """True for a declared operational code, ``HTTP_<status>`` included.

    The transport's own codes are the loop's to *record*, never to raise, and it
    produces one per HTTP status. Membership is therefore the table plus that
    one declared family; nothing else is parameterised.
    """

    if not isinstance(code, str):
        return False
    return code in FAILURE_CODES or bool(_HTTP_STATUS.fullmatch(code))


# --------------------------------------------------------------------------
# Errors
# --------------------------------------------------------------------------

_CODE = re.compile(r"[A-Z][A-Z0-9_]*\Z")


class LoopError(RuntimeError):
    """A loud loop failure carrying a stable code and a detail.

    The code is never a semantic result: it says what the machinery refused or
    could not do. Membership of :data:`FAILURE_CODES` is *not* enforced - later
    waves own codes wave 0 cannot enumerate - but the shape is.
    """

    def __init__(self, code: str, detail: str = ""):
        if not isinstance(code, str) or not _CODE.fullmatch(code):
            raise ValueError("A LoopError code is UPPER_SNAKE_CASE")
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


# --------------------------------------------------------------------------
# Validation helpers
# --------------------------------------------------------------------------

#: The repository's own identifier shape
#: (``multicycle_commitment_study_multi_v2.ID``).
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}\Z")
_HEX64 = re.compile(r"[0-9a-f]{64}\Z")
_UTC = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)\Z")
_SLUG_UNSAFE = re.compile(r"[^A-Za-z0-9_.-]")
#: ``origin/claude/some-branch`` - the shape ``multicycle_commitment_study_multi_v2``
#: `` .split_publish_ref`` accepts. That function stays authoritative at publish
#: time; this is the early refusal, so a mistyped ref is caught before a run
#: opens rather than after the first wave is prepared.
_PUBLISH_REF = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_./-]*\Z")


def _fail(code: str, detail: str) -> LoopError:
    return LoopError(code, detail)


def _text(value: Any, where: str, code: str = "CONFIG_INVALID_VALUE") -> str:
    if type(value) is not str or not value.strip():
        raise _fail(code, f"{where} must be a non-empty string")
    return value


def _identifier(value: Any, where: str, code: str = "CONFIG_INVALID_VALUE") -> str:
    if type(value) is not str or not _ID.fullmatch(value):
        raise _fail(code, f"{where} must match {_ID.pattern}")
    return value


def _whole(value: Any, where: str, code: str = "CONFIG_INVALID_VALUE",
           *, low: int, high: int) -> int:
    # ``type(value) is not int`` rejects ``bool``: ``True`` is not a budget.
    if type(value) is not int or not low <= value <= high:
        raise _fail(code, f"{where} must be a whole number from {low} to {high}")
    return value


def _fraction(value: Any, where: str, code: str = "CONFIG_INVALID_VALUE") -> float:
    if type(value) not in (int, float) or type(value) is bool or not 0.0 <= value <= 1.0:
        raise _fail(code, f"{where} must be a number from 0 to 1")
    return float(value)


def _flag(value: Any, where: str, code: str = "CONFIG_INVALID_VALUE") -> bool:
    if type(value) is not bool:
        raise _fail(code, f"{where} must be true or false")
    return value


def _relative(value: Any, where: str, code: str = "CONFIG_INVALID_VALUE") -> str:
    """A repo-relative POSIX path, spelled one way only.

    No absolute root, no ``..``, no backslash, no ``~``, no trailing ``/`` - and,
    since ``Path.as_posix`` folds them away in silence, no ``.`` component and no
    component that begins or ends with whitespace. Two spellings of one file
    ( ``src/a.py`` and ``./src/a.py`` ) used to normalise to one key, which is
    how a pin map could hold two entries and mint one identity; the path space
    this function admits is now the space it returns, so a spelling is a file.
    """

    text = _text(value, where, code)
    if (text.startswith("/") or text.endswith("/") or "\\" in text
            or ".." in Path(text).parts or text.startswith("~")):
        raise _fail(code, f"{where} must be a relative path inside the repository")
    for part in text.split("/"):
        if part == ".":
            raise _fail(code, f"{where} must not spell a component '.'")
        if part != part.strip():
            raise _fail(code, f"{where} must not pad a component with whitespace")
    return Path(text).as_posix()


def _mapping(value: Any, where: str, code: str = "CONFIG_INVALID_VALUE") -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise _fail(code, f"{where} must be an object")
    for key in value:
        if type(key) is not str:
            raise _fail(code, f"{where} keys must be strings")
    return value


def _sequence(value: Any, where: str, code: str = "CONFIG_INVALID_VALUE") -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise _fail(code, f"{where} must be a list")
    return value


def _unique_texts(value: Any, where: str, code: str = "CONFIG_INVALID_VALUE") -> tuple[str, ...]:
    items = tuple(_text(item, f"{where}[{index}]", code)
                  for index, item in enumerate(_sequence(value, where, code)))
    if len(set(items)) != len(items):
        raise _fail(code, f"{where} must not repeat an entry")
    return items


def _relatives(value: Any, where: str, code: str = "CONFIG_INVALID_VALUE") -> tuple[str, ...]:
    items = tuple(_relative(item, f"{where}[{index}]", code)
                  for index, item in enumerate(_sequence(value, where, code)))
    if len(set(items)) != len(items):
        raise _fail(code, f"{where} must not repeat a path")
    return items


def _keys(raw: Mapping[str, Any], where: str, code: str | None = None, *,
          required: frozenset[str], optional: frozenset[str]) -> None:
    """Refuse an unknown or missing key.

    ``code`` overrides both refusal codes at once, for a record whose keys are
    not a config's (a receipt's custody block answers STEP_RECEIPT_INVALID, not
    CONFIG_UNKNOWN_KEY).
    """

    unknown = sorted(set(raw) - required - optional)
    if unknown:
        detail = f"{where} declares unknown keys: {unknown}"
        if code is None:
            raise _fail("CONFIG_UNKNOWN_KEY", detail)
        raise _fail(code, detail)
    missing = sorted(required - set(raw))
    if missing:
        detail = f"{where} is missing: {missing}"
        if code is None:
            raise _fail("CONFIG_MISSING_KEY", detail)
        raise _fail(code, detail)


def _digests(value: Any, where: str, code: str = "CONFIG_INVALID_VALUE") -> dict[str, str]:
    """A path -> sha256 map, refusing two spellings of one path.

    :func:`_relative` normalises the key, so ``src/a.py`` and ``src//a.py`` name
    one file; folding them into one entry would let a map that holds two digests
    mint one identity, and would make the identity depend on insertion order.
    A post-normalisation duplicate is therefore a refusal, as it already is for
    a list of paths (:func:`_relatives`).
    """

    out: dict[str, str] = {}
    spelling: dict[str, str] = {}
    for key, digest in _mapping(value, where, code).items():
        path = _relative(key, f"{where} key", code)
        if path in spelling:
            raise _fail(code, f"{where} names {path!r} twice, as {spelling[path]!r} "
                              f"and {key!r}")
        spelling[path] = key
        out[path] = (digest if type(digest) is str and _HEX64.fullmatch(digest)
                     else _refuse_digest(where, key, code))
    return dict(sorted(out.items()))


def _refuse_digest(where: str, key: str, code: str) -> str:
    raise _fail(code, f"{where}[{key!r}] must be a lowercase sha256 hex digest")


def _utc(value: Any, where: str, code: str = "STEP_RECEIPT_INVALID") -> str:
    if type(value) is not str or not _UTC.fullmatch(value):
        raise _fail(code, f"{where} must be an ISO-8601 UTC timestamp (Z or +00:00)")
    return value


# --------------------------------------------------------------------------
# Configuration - minireason.loop.config.v1 (design 4.2)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class SeatsConfig:
    """Seat declarations and the guard parameters of design 2.2 / 2.3.

    A seat left ``None`` (or ``judges`` left empty) is assigned by W1-SEATS'
    deterministic rule over the endpoint registry, which design 2.2 pins into
    ``plan.json`` before dispatch. Naming a seat here pins it instead; either
    way the choice is a pure function of (registry, config).

    ``min_judge_families``, ``paraphrase_n`` and ``schema_repair_budget`` are
    **also** frozen in the standard artifact (``standard.GUARD_PARAMETERS``), and
    both owners are folded into ``loop_plan_id``. The admissible ranges below are
    ``standard._INT_PARAMS``' own, so the two owners can no longer have disjoint
    ranges - a config could once turn G7 off with ``paraphrase_n = 0`` that
    ``build_standard`` refuses - and ``schema_repair_budget`` is pinned to the
    single value the standard states, since raising it turns a re-ask into a
    budgeted new coordinate the standard has not pre-registered. Equal ranges are
    not equal values: **PREFLIGHT must call**
    ``standard.assert_config_matches_standard(config.seats.as_dict(),
    config.reopen_reasons)`` (W5), which is the one place the standard wins over
    a config that declares something else. This module cannot call it itself: it
    imports no sibling, which is what keeps the package graph acyclic.
    """

    critic: str | None = None
    defender: str | None = None
    variator: str | None = None
    judges: tuple[str, ...] = ()
    #: Design 2.2: two judge seats from two distinct ``family`` values.
    min_judge_families: int = 2
    #: Design 2.3: ``TRIAL_PARAPHRASE_N``. Low bound 1, not 0: 0 is G7 switched
    #: off, which the standard's own range refuses.
    paraphrase_n: int = 2
    #: Design 2.3: a re-ask is a new coordinate, and the budget for one is 0.
    #: The standard freezes the value, so this is 0 until a successor standard
    #: says otherwise - and a successor standard is a new ``loop_plan_id``.
    schema_repair_budget: int = 0

    _REQUIRED = frozenset()
    _OPTIONAL = frozenset({"critic", "defender", "variator", "judges",
                           "min_judge_families", "paraphrase_n",
                           "schema_repair_budget"})

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "SeatsConfig":
        raw = _mapping(raw, "seats")
        _keys(raw, "seats", required=cls._REQUIRED, optional=cls._OPTIONAL)
        seat = lambda name: (None if raw.get(name) is None
                             else _text(raw[name], f"seats.{name}"))
        judges = _unique_texts(raw.get("judges", ()), "seats.judges")
        config = cls(
            critic=seat("critic"), defender=seat("defender"), variator=seat("variator"),
            judges=judges,
            min_judge_families=_whole(raw.get("min_judge_families", 2),
                                      "seats.min_judge_families", low=2, high=8),
            paraphrase_n=_whole(raw.get("paraphrase_n", 2),
                                "seats.paraphrase_n", low=1, high=8),
            schema_repair_budget=_whole(raw.get("schema_repair_budget", 0),
                                        "seats.schema_repair_budget", low=0, high=0))
        if judges and len(judges) < config.min_judge_families:
            raise _fail("CONFIG_INVALID_VALUE",
                        "seats.judges names fewer seats than seats.min_judge_families")
        return config

    def as_dict(self) -> dict[str, Any]:
        return {"critic": self.critic, "defender": self.defender,
                "variator": self.variator, "judges": list(self.judges),
                "min_judge_families": self.min_judge_families,
                "paraphrase_n": self.paraphrase_n,
                "schema_repair_budget": self.schema_repair_budget}


@dataclass(frozen=True)
class ContrastConfig:
    """The optional C001 contrast leg (design 4.2 ``contrast{...}``)."""

    attached: bool = False
    study: str | None = None
    occurrences: tuple[str, ...] = ()

    _OPTIONAL = frozenset({"attached", "study", "occurrences"})

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "ContrastConfig":
        raw = _mapping(raw, "contrast")
        _keys(raw, "contrast", required=frozenset(), optional=cls._OPTIONAL)
        attached = _flag(raw.get("attached", False), "contrast.attached")
        study = None if raw.get("study") is None else _text(raw["study"], "contrast.study")
        occurrences = _relatives(raw.get("occurrences", ()), "contrast.occurrences")
        if attached and (study is None or not occurrences):
            raise _fail("CONFIG_INVALID_VALUE",
                        "an attached contrast leg needs a study and at least one occurrence")
        if not attached and (study is not None or occurrences):
            raise _fail("CONFIG_INVALID_VALUE",
                        "a detached contrast leg names no study and no occurrence")
        return cls(attached=attached, study=study, occurrences=occurrences)

    def as_dict(self) -> dict[str, Any]:
        return {"attached": self.attached, "study": self.study,
                "occurrences": list(self.occurrences)}


@dataclass(frozen=True)
class AuditConfig:
    """Design 2.5 / 4.2 ``audit{period, judge_err_max, streak_max}``, each margin
    carrying the account that justifies it.

    All three thresholds are pre-registered, so none of them has a default: a
    threshold that appears by default was never pre-registered. Changing one
    after first look mints a new ``loop_plan_id`` (design 5).

    **Each threshold carries an account, and the account is required.** A bare
    constant whose margin carries no reason is the defect
    ``docs/reviews/fw5-vs-harness-spec-2026-09-14.md`` charges the spec with
    ("``HV_MIN`` is a bare config constant whose margin carries no account"), and
    R9 requires a stated anchor. ``judge_err_max_account`` and
    ``streak_max_account`` are non-empty prose, they are inside the config and so
    inside ``loop_plan_id``, and they are rendered beside the number - so the
    margin is attackable rather than merely declared.

    **What ``judge_err_max`` is a rate over, and what it may never be used for.**
    The planted-flaw calibration set is five anchors (design 2.5; two that must
    sustain, three clean controls), so the attainable granularity of a fraction
    over it is 0.2: any value below 0.2 means "one wrong anchor ends the reading
    arm", and the account should say whether that is intended. The rate is a
    **panel-level instrument signal**: crossing it names ``instrument_fault``,
    which stops the reading arm and Spawns ``audit-the-reader``. It is never
    computed per seat for comparison. The anchors are run per seat, so an
    ``errors / anchors`` per seat is easy to write and would be a merit predicate
    over endpoints - which ceiling clause 8 forbids in as many words ("Endpoints
    are independent occasions to look for one pattern, never competitors",
    FW5:849). Design 2.5's per-hit demonstrative warrant is the mechanism that
    does the work; ``instrument_fault`` names the instrument, never a losing seat.
    """

    period: int
    judge_err_max: float
    streak_max: int
    judge_err_max_account: str
    streak_max_account: str

    _REQUIRED = frozenset({"period", "judge_err_max", "streak_max",
                           "judge_err_max_account", "streak_max_account"})

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "AuditConfig":
        raw = _mapping(raw, "audit")
        _keys(raw, "audit", required=cls._REQUIRED, optional=frozenset())
        return cls(
            period=_whole(raw["period"], "audit.period", low=1, high=99),
            judge_err_max=_fraction(raw["judge_err_max"], "audit.judge_err_max"),
            streak_max=_whole(raw["streak_max"], "audit.streak_max", low=1, high=9999),
            judge_err_max_account=_text(raw["judge_err_max_account"],
                                        "audit.judge_err_max_account"),
            streak_max_account=_text(raw["streak_max_account"],
                                     "audit.streak_max_account"))

    def as_dict(self) -> dict[str, Any]:
        return {"period": self.period, "judge_err_max": self.judge_err_max,
                "judge_err_max_account": self.judge_err_max_account,
                "streak_max": self.streak_max,
                "streak_max_account": self.streak_max_account}


@dataclass(frozen=True)
class TimeoutsConfig:
    """Design 4.4 layers 2 and 3.

    Layer 1 - the provider wall clock - is **not** here: it is read off the
    endpoint's own ``timeout_seconds`` from the frozen plan, and a disagreement
    is ``TIMEOUT_NOT_APPLIED``. No config key can change it.
    """

    #: Per step kind; a kind absent from the mapping has no step deadline.
    step_seconds: Mapping[str, int] = field(default_factory=dict)
    #: Runner v2's git timeout.
    git_seconds: int = 90

    _OPTIONAL = frozenset({"step_seconds", "git_seconds"})

    def __post_init__(self) -> None:
        object.__setattr__(self, "step_seconds",
                           MappingProxyType(dict(sorted(self.step_seconds.items()))))

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "TimeoutsConfig":
        raw = _mapping(raw, "timeouts")
        _keys(raw, "timeouts", required=frozenset(), optional=cls._OPTIONAL)
        steps = _mapping(raw.get("step_seconds", {}), "timeouts.step_seconds")
        resolved: dict[str, int] = {}
        for kind, seconds in steps.items():
            if kind not in STEP_KINDS:
                raise _fail("CONFIG_INVALID_VALUE",
                            f"timeouts.step_seconds names an unknown step kind: {kind!r}")
            resolved[kind] = _whole(seconds, f"timeouts.step_seconds[{kind}]",
                                    low=1, high=86400)
        return cls(step_seconds=resolved,
                   git_seconds=_whole(raw.get("git_seconds", 90), "timeouts.git_seconds",
                                      low=1, high=3600))

    def as_dict(self) -> dict[str, Any]:
        return {"step_seconds": dict(self.step_seconds), "git_seconds": self.git_seconds}


@dataclass(frozen=True)
class LoopConfig:
    """One frozen ``minireason.loop.config.v1`` declaration.

    Every field is a declaration made before the first call. Loading is strict:
    an unknown key is refused rather than ignored, because a key the loader
    drops is a pre-registration the run does not honour.
    """

    run_id: str
    study: str
    occurrences: tuple[str, ...]
    runner: str
    cycle_budget: int
    max_calls: int
    reading_set: tuple[str, ...]
    obligations_path: str
    graph_root: str
    reopen_reasons: tuple[str, ...]
    audit: AuditConfig
    seats: SeatsConfig = field(default_factory=SeatsConfig)
    contrast: ContrastConfig = field(default_factory=ContrastConfig)
    timeouts: TimeoutsConfig = field(default_factory=TimeoutsConfig)
    #: ``None`` means the CLI default: the branch's upstream (design 4.2).
    publish_ref: str | None = None
    #: A config that does not declare a spending mode does not spend.
    provider_mode: str = "offline"
    #: ``multicycle_commitment_study_multi_v2.MAX_PER_KEY``. The real ceiling is
    #: ``provider_openai_compat.slots_for``; this may not exceed it.
    max_per_key: int = 5

    _REQUIRED = frozenset({"run_id", "study", "occurrences", "runner", "cycle_budget",
                           "max_calls", "reading_set", "obligations_path", "graph_root",
                           "reopen_reasons", "audit"})
    _OPTIONAL = frozenset({"schema", "seats", "contrast", "timeouts", "publish_ref",
                           "provider_mode", "max_per_key"})

    @classmethod
    def load(cls, path: Path | str) -> "LoopConfig":
        """Read and validate one config file. Two loads give one identity.

        A path that cannot be read is ``CONFIG_NOT_FOUND`` - a missing or
        unreadable pre-registration is a loop refusal with a code, not an
        ``OSError`` escaping into a caller that catches :class:`LoopError`.
        """

        try:
            raw_bytes = Path(path).read_bytes()
        except OSError as exc:
            raise _fail("CONFIG_NOT_FOUND",
                        f"{path} cannot be read: {type(exc).__name__}") from exc
        try:
            raw = json.loads(raw_bytes)
        except ValueError as exc:
            raise _fail("CONFIG_NOT_A_MAPPING", f"{path} is not JSON: {exc}") from exc
        return cls.from_mapping(raw)

    @classmethod
    def from_mapping(cls, raw: Any) -> "LoopConfig":
        if isinstance(raw, LoopConfig):
            return raw
        if not isinstance(raw, Mapping):
            raise _fail("CONFIG_NOT_A_MAPPING", "a loop config is a JSON object")
        for key in raw:
            if type(key) is not str:
                raise _fail("CONFIG_NOT_A_MAPPING", "config keys must be strings")
        if "schema" in raw and raw["schema"] != CONFIG_SCHEMA:
            raise _fail("CONFIG_SCHEMA_UNKNOWN",
                        f"config schema must be {CONFIG_SCHEMA}, not {raw['schema']!r}")
        _keys(raw, "config", required=cls._REQUIRED, optional=cls._OPTIONAL)
        occurrences = _relatives(raw["occurrences"], "occurrences")
        if not occurrences:
            raise _fail("CONFIG_INVALID_VALUE", "occurrences names no occurrence")
        publish_ref = raw.get("publish_ref")
        if publish_ref is not None:
            publish_ref = _text(publish_ref, "publish_ref")
            if not _PUBLISH_REF.fullmatch(publish_ref) or ".." in publish_ref:
                raise _fail("CONFIG_INVALID_VALUE",
                            "publish_ref must read <remote>/<branch>")
        mode = _text(raw.get("provider_mode", "offline"), "provider_mode")
        if mode not in PROVIDER_MODES:
            raise _fail("CONFIG_INVALID_VALUE",
                        f"provider_mode must be one of {list(PROVIDER_MODES)}")
        return cls(
            run_id=_identifier(raw["run_id"], "run_id", "RUN_ID_INVALID"),
            study=_text(raw["study"], "study"),
            occurrences=occurrences,
            runner=_relative(raw["runner"], "runner"),
            cycle_budget=_whole(raw["cycle_budget"], "cycle_budget", low=1, high=99),
            max_calls=_whole(raw["max_calls"], "max_calls", low=0, high=1_000_000),
            reading_set=_unique_texts(raw["reading_set"], "reading_set"),
            obligations_path=_relative(raw["obligations_path"], "obligations_path"),
            graph_root=_relative(raw["graph_root"], "graph_root"),
            reopen_reasons=_unique_texts(raw["reopen_reasons"], "reopen_reasons"),
            audit=AuditConfig.from_mapping(raw["audit"]),
            seats=SeatsConfig.from_mapping(raw.get("seats", {})),
            contrast=ContrastConfig.from_mapping(raw.get("contrast", {})),
            timeouts=TimeoutsConfig.from_mapping(raw.get("timeouts", {})),
            publish_ref=publish_ref,
            provider_mode=mode,
            max_per_key=_whole(raw.get("max_per_key", 5), "max_per_key", low=1, high=5))

    def as_dict(self) -> dict[str, Any]:
        """The fully explicit config: every key present, every default resolved."""

        return {
            "schema": CONFIG_SCHEMA,
            "audit": self.audit.as_dict(),
            "contrast": self.contrast.as_dict(),
            "cycle_budget": self.cycle_budget,
            "graph_root": self.graph_root,
            "max_calls": self.max_calls,
            "max_per_key": self.max_per_key,
            "obligations_path": self.obligations_path,
            "occurrences": list(self.occurrences),
            "provider_mode": self.provider_mode,
            "publish_ref": self.publish_ref,
            "reading_set": list(self.reading_set),
            "reopen_reasons": list(self.reopen_reasons),
            "run_id": self.run_id,
            "runner": self.runner,
            "seats": self.seats.as_dict(),
            "study": self.study,
            "timeouts": self.timeouts.as_dict(),
        }

    def canonical_bytes(self) -> bytes:
        return canonical_json(self.as_dict())


def loop_plan_id(config: LoopConfig | Mapping[str, Any],
                 pins: Mapping[str, str]) -> str:
    """``sha256`` over the canonical config and the frozen source pins (design 4.2).

    ``config`` may be a :class:`LoopConfig` or the raw mapping one was loaded
    from: the mapping is validated the same way, so a file and the object read
    from it give one id. Formatting, key order and resolved defaults are
    therefore not part of the identity, but every declared value is. ``pins``
    maps a repo-relative path to its lowercase sha256; a null pin is refused,
    since an unpinned file inside a plan identity pins nothing.

    Every member of :data:`PINNED_SOURCE_PATHS` must appear, because that
    constant is *the fixed part of the identity* and an id computed without one
    of them is an id for a different plan than the one it claims. A missing pin
    is ``PIN_INVALID`` naming the paths that are absent; the run-specific rest
    of the list stays the caller's to supply. Two spellings of one path are
    refused rather than folded, so the id does not depend on pin order.
    """

    body = LoopConfig.from_mapping(config).as_dict()
    digests = _digests(pins, "pins", "PIN_INVALID")
    missing = sorted(set(PINNED_SOURCE_PATHS) - set(digests))
    if missing:
        # REVIEW-PREREG PR-07: the refusal a caller meets must name the paths it
        # has to supply, in the spelling ``pins`` is keyed by, and say that the
        # six are the fixed part of the identity rather than a suggestion. The
        # earlier wording ("the plan identity pins [...], which pins names none
        # of") listed them but read as though they were the ones supplied.
        raise _fail("PIN_INVALID",
                    "the plan identity is fixed by "
                    f"{len(PINNED_SOURCE_PATHS)} source pins and pins supplies "
                    f"no digest for {len(missing)} of them: "
                    + ", ".join(missing))
    return sha256_hex(canonical_json({
        "schema": PLAN_ID_SCHEMA,
        "config": body,
        "pins": digests,
    }))


# --------------------------------------------------------------------------
# Step receipts - minireason.loop.step.v1 (design 4.3)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class CustodyReport:
    """What the step's custody check found.

    ``checks`` holds stable codes - a :data:`FAILURE_CODES` member, a pinned
    path - not prose: a receipt is read by a program. The narrative belongs in
    the erratum the halt writes.
    """

    verified: bool = False
    checks: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if type(self.verified) is not bool:
            raise _fail("STEP_RECEIPT_INVALID", "custody.verified must be true or false")
        object.__setattr__(self, "checks", tuple(
            _text(check, f"custody.checks[{index}]", "STEP_RECEIPT_INVALID")
            for index, check in enumerate(
                _sequence(self.checks, "custody.checks", "STEP_RECEIPT_INVALID"))))

    @classmethod
    def from_mapping(cls, raw: Any) -> "CustodyReport":
        """One custody block, from the mapping a receipt file carries.

        ``checks`` is handed to the constructor **unconverted**: calling
        ``tuple()`` on it here would turn the string ``"SOURCE_PIN_MISMATCH"``
        into nineteen one-character checks before ``__post_init__``'s list guard
        could see it, and a receipt claiming nineteen custody findings where one
        file moved is a receipt that miscounts a halt.
        """

        raw = _mapping(raw, "custody", "STEP_RECEIPT_INVALID")
        _keys(raw, "custody", "STEP_RECEIPT_INVALID", required=frozenset(),
              optional=frozenset({"verified", "checks"}))
        return cls(verified=raw.get("verified", False),
                   checks=raw.get("checks", ()))

    @classmethod
    def from_findings(cls, findings: Any) -> "CustodyReport":
        """The receipt block for what a custody check found.

        The one adapter between ``custody.verify_pins``' findings and this
        record, so W1-STEPS has one way to fill a receipt rather than each
        caller inventing a projection. Import-free by construction: any object
        carrying a ``.code`` is accepted, which is what
        ``custody.CustodyFinding`` is, so this module keeps importing none of
        its siblings.

        ``verified`` is true exactly when there were no findings - an empty
        result is the only thing that means *every pinned file is still at its
        pinned bytes*. ``checks`` keeps one code per finding, in the order
        ``verify_pins`` returned them (sorted by path, then code), and does
        **not** de-duplicate: two files that moved are two checks, and a
        receipt that collapsed them would under-report the halt.

        A bare ``str``/``bytes`` is refused rather than iterated: one code
        handed in by mistake is one finding spelled wrong, never one character
        per letter. Anything else that is not iterable is refused with the same
        code, so no caller of this adapter meets a bare ``TypeError``.
        """

        if isinstance(findings, (str, bytes, bytearray)):
            raise _fail("STEP_RECEIPT_INVALID",
                        f"custody findings must be a sequence of findings, not a "
                        f"{type(findings).__name__}")
        try:
            rows = tuple(findings)
        except TypeError as exc:
            raise _fail("STEP_RECEIPT_INVALID",
                        f"custody findings must be iterable: {exc}") from exc
        checks: list[str] = []
        for index, finding in enumerate(rows):
            code = finding if isinstance(finding, str) else getattr(finding, "code", None)
            if code is None:
                raise _fail("STEP_RECEIPT_INVALID",
                            f"custody finding {index} carries no code")
            checks.append(_text(code, f"custody.checks[{index}]",
                                "STEP_RECEIPT_INVALID"))
        return cls(verified=not rows, checks=tuple(checks))

    def as_dict(self) -> dict[str, Any]:
        return {"verified": self.verified, "checks": list(self.checks)}


@dataclass(frozen=True)
class StepReceipt:
    """One write-once step receipt.

    A receipt is checkable against itself: :meth:`key` is recomputed from the
    receipt's own fields and must equal ``step_key``, and ``spending`` must
    equal design 4.3's classification of ``kind``. A record that can disagree
    with the rule it was written under is a record that can lie.
    """

    step_key: str
    index: int
    kind: str
    loop_plan_id: str
    status: str
    started_utc: str
    cycle: int | None = None
    wave: str | None = None
    inputs_sha256: Mapping[str, str] = field(default_factory=dict)
    outputs_sha256: Mapping[str, str] = field(default_factory=dict)
    spending: bool | None = None
    finished_utc: str | None = None
    custody: CustodyReport = field(default_factory=CustodyReport)
    failure_code: str | None = None
    published_commit: str | None = None
    schema: str = STEP_SCHEMA

    def __post_init__(self) -> None:
        if self.schema != STEP_SCHEMA:
            raise _fail("STEP_RECEIPT_INVALID", f"schema must be {STEP_SCHEMA}")
        if self.kind not in STEP_KINDS:
            raise _fail("STEP_RECEIPT_INVALID", f"unknown step kind: {self.kind!r}")
        if self.status not in STEP_STATUSES:
            raise _fail("STEP_RECEIPT_INVALID",
                        f"status must be one of {list(STEP_STATUSES)}")
        if type(self.index) is not int or not 0 <= self.index <= 9999:
            raise _fail("STEP_RECEIPT_INVALID", "index must be a whole number 0..9999")
        if type(self.loop_plan_id) is not str or not _HEX64.fullmatch(self.loop_plan_id):
            raise _fail("STEP_RECEIPT_INVALID", "loop_plan_id must be a sha256 hex digest")
        if self.cycle is not None:
            _whole(self.cycle, "cycle", "CYCLE_OUT_OF_RANGE", low=1, high=99)
        if self.wave is not None:
            _identifier(self.wave, "wave", "STEP_RECEIPT_INVALID")
        object.__setattr__(self, "inputs_sha256", MappingProxyType(
            _digests(self.inputs_sha256, "inputs_sha256", "STEP_RECEIPT_INVALID")))
        object.__setattr__(self, "outputs_sha256", MappingProxyType(
            _digests(self.outputs_sha256, "outputs_sha256", "STEP_RECEIPT_INVALID")))
        expected_spending = self.kind in SPENDING_STEPS
        if self.spending is None:
            object.__setattr__(self, "spending", expected_spending)
        elif self.spending is not expected_spending:
            raise _fail("STEP_RECEIPT_INVALID",
                        f"{self.kind} is {'' if expected_spending else 'not '}a spending step")
        _utc(self.started_utc, "started_utc")
        if self.finished_utc is not None:
            _utc(self.finished_utc, "finished_utc")
        if self.failure_code is not None:
            if type(self.failure_code) is not str or not _CODE.fullmatch(self.failure_code):
                raise _fail("STEP_RECEIPT_INVALID", "failure_code is UPPER_SNAKE_CASE")
        if self.status == "COMPLETE" and self.failure_code is not None:
            raise _fail("STEP_RECEIPT_INVALID", "a COMPLETE step carries no failure_code")
        if self.status != "COMPLETE" and self.failure_code is None:
            raise _fail("STEP_RECEIPT_INVALID",
                        f"a {self.status} step must name its failure_code")
        if not isinstance(self.custody, CustodyReport):
            object.__setattr__(self, "custody", CustodyReport.from_mapping(self.custody))
        if self.published_commit is not None:
            if (type(self.published_commit) is not str
                    or not re.fullmatch(r"[0-9a-f]{7,64}", self.published_commit)):
                raise _fail("STEP_RECEIPT_INVALID",
                            "published_commit must be a lowercase git object id")
        computed = self.key(self.loop_plan_id, self.kind, self.cycle, self.wave,
                            self.inputs_sha256)
        if self.step_key != computed:
            raise _fail("STEP_KEY_MISMATCH",
                        f"step_key {self.step_key!r} is not this step's key")

    @staticmethod
    def key(loop_plan_id: str, kind: str, cycle: int | None, wave: str | None,
            inputs_sha256: Mapping[str, str]) -> str:
        """``sha256(canonical(loop_plan_id, kind, cycle, wave, inputs_sha256))``.

        Five of the receipt's sixteen fields, which is the whole of what this
        key binds: ``status``, ``outputs_sha256``, ``custody``, ``failure_code``,
        ``published_commit``, the two timestamps and ``index`` are **not** in
        it. Two receipts for one step with different outcomes have one
        ``step_key``; it identifies the step, and is not a tamper-evident digest
        of the record. A reader who needs the record's bytes digests the file.
        """

        if kind not in STEP_KINDS:
            raise _fail("STEP_RECEIPT_INVALID", f"unknown step kind: {kind!r}")
        if type(loop_plan_id) is not str or not _HEX64.fullmatch(loop_plan_id):
            raise _fail("STEP_RECEIPT_INVALID", "loop_plan_id must be a sha256 hex digest")
        return sha256_hex(canonical_json({
            "schema": STEP_KEY_SCHEMA,
            "loop_plan_id": loop_plan_id,
            "kind": kind,
            "cycle": None if cycle is None else _whole(cycle, "cycle",
                                                       "CYCLE_OUT_OF_RANGE",
                                                       low=1, high=99),
            "wave": None if wave is None else _identifier(wave, "wave",
                                                          "STEP_RECEIPT_INVALID"),
            "inputs_sha256": _digests(inputs_sha256, "inputs_sha256",
                                      "STEP_RECEIPT_INVALID"),
        }))

    @classmethod
    def build(cls, *, loop_plan_id: str, index: int, kind: str, started_utc: str,
                cycle: int | None = None, wave: str | None = None,
                inputs_sha256: Mapping[str, str] | None = None,
                status: str = "COMPLETE", **rest: Any) -> "StepReceipt":
        """Build a receipt, computing ``step_key`` from the fields given.

        A misspelled field name is ``STEP_RECEIPT_INVALID``, the same refusal
        :meth:`from_dict` gives it, rather than the ``TypeError`` the
        constructor would raise: both doors into a receipt answer with a code.
        """

        unknown = sorted(set(rest) - cls._REST_FIELDS)
        if unknown:
            raise _fail("STEP_RECEIPT_INVALID", f"unknown receipt keys: {unknown}")
        inputs = dict(inputs_sha256 or {})
        return cls(step_key=cls.key(loop_plan_id, kind, cycle, wave, inputs),
                   index=index, kind=kind, loop_plan_id=loop_plan_id, status=status,
                   started_utc=started_utc, cycle=cycle, wave=wave,
                   inputs_sha256=inputs, **rest)

    #: The sixteen field names a receipt file may carry.
    _FIELDS = frozenset({
        "schema", "step_key", "index", "kind", "cycle", "wave", "loop_plan_id",
        "inputs_sha256", "outputs_sha256", "spending", "started_utc",
        "finished_utc", "status", "custody", "failure_code", "published_commit"})

    #: What :meth:`build` may be handed as ``**rest``: every field it does not
    #: name itself, minus ``step_key``, which it computes.
    _REST_FIELDS = _FIELDS - frozenset({
        "step_key", "index", "kind", "loop_plan_id", "status", "started_utc",
        "cycle", "wave", "inputs_sha256"})

    @classmethod
    def from_dict(cls, raw: Any) -> "StepReceipt":
        raw = _mapping(raw, "step receipt", "STEP_RECEIPT_INVALID")
        known = cls._FIELDS
        unknown = sorted(set(raw) - known)
        if unknown:
            raise _fail("STEP_RECEIPT_INVALID", f"unknown receipt keys: {unknown}")
        missing = sorted({"step_key", "index", "kind", "loop_plan_id", "status",
                          "started_utc"} - set(raw))
        if missing:
            raise _fail("STEP_RECEIPT_INVALID", f"receipt is missing: {missing}")
        return cls(
            step_key=raw["step_key"], index=raw["index"], kind=raw["kind"],
            loop_plan_id=raw["loop_plan_id"], status=raw["status"],
            started_utc=raw["started_utc"], cycle=raw.get("cycle"),
            wave=raw.get("wave"), inputs_sha256=raw.get("inputs_sha256", {}),
            outputs_sha256=raw.get("outputs_sha256", {}), spending=raw.get("spending"),
            finished_utc=raw.get("finished_utc"),
            custody=CustodyReport.from_mapping(raw.get("custody", {})),
            failure_code=raw.get("failure_code"),
            published_commit=raw.get("published_commit"),
            schema=raw.get("schema", STEP_SCHEMA))

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "step_key": self.step_key,
            "index": self.index,
            "kind": self.kind,
            "cycle": self.cycle,
            "wave": self.wave,
            "loop_plan_id": self.loop_plan_id,
            "inputs_sha256": dict(self.inputs_sha256),
            "outputs_sha256": dict(self.outputs_sha256),
            "spending": self.spending,
            "started_utc": self.started_utc,
            "finished_utc": self.finished_utc,
            "status": self.status,
            "custody": self.custody.as_dict(),
            "failure_code": self.failure_code,
            "published_commit": self.published_commit,
        }

    @property
    def replayable(self) -> bool:
        return self.kind in REPLAYABLE_STEPS

    @property
    def filename(self) -> str:
        return f"{self.index:04d}-{self.kind}.json"


# --------------------------------------------------------------------------
# Run layout (design 4.2)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class CyclePaths:
    """``cycles/cycle-NN/{import,use-table,readings,contrast,decision.json,CYCLE.md}``."""

    cycle: int
    root: Path

    @property
    def import_dir(self) -> Path:
        return self.root / "import"

    @property
    def use_table(self) -> Path:
        return self.root / "use-table"

    @property
    def readings(self) -> Path:
        return self.root / "readings"

    @property
    def contrast(self) -> Path:
        return self.root / "contrast"

    @property
    def decision(self) -> Path:
        return self.root / "decision.json"

    @property
    def cycle_md(self) -> Path:
        return self.root / "CYCLE.md"

    def as_dict(self) -> dict[str, str]:
        return {"cycle": str(self.cycle), "root": self.root.as_posix(),
                "import": self.import_dir.as_posix(),
                "use_table": self.use_table.as_posix(),
                "readings": self.readings.as_posix(),
                "contrast": self.contrast.as_posix(),
                "decision": self.decision.as_posix(),
                "cycle_md": self.cycle_md.as_posix()}


@dataclass(frozen=True)
class RunPaths:
    """Every path design 4.2 names for one run, derived and never guessed.

    Occurrence trees are **not** here: the loop references them where runner v2
    and the contrast tool own them and writes nothing inside them.
    """

    repo_root: Path
    run_id: str
    run_root: Path

    @property
    def config(self) -> Path:
        return self.run_root / "config.json"

    @property
    def preregistration(self) -> Path:
        return self.run_root / "preregistration.md"

    @property
    def obligations(self) -> Path:
        return self.run_root / "obligations.json"

    @property
    def ceiling(self) -> Path:
        return self.run_root / "CEILING.md"

    @property
    def plan(self) -> Path:
        return self.run_root / "plan.json"

    @property
    def preflight(self) -> Path:
        return self.run_root / "preflight.json"

    @property
    def lock(self) -> Path:
        return self.run_root / "run.lock"

    @property
    def steps(self) -> Path:
        return self.run_root / "steps"

    @property
    def graph(self) -> Path:
        """The default harness root. ``LoopConfig.graph_root`` overrides it."""

        return self.run_root / "graph"

    @property
    def cycles(self) -> Path:
        return self.run_root / "cycles"

    @property
    def readings(self) -> Path:
        return self.run_root / "readings"

    @property
    def audits(self) -> Path:
        return self.run_root / "audits"

    @property
    def appeals(self) -> Path:
        return self.run_root / "appeals"

    @property
    def errata(self) -> Path:
        return self.run_root / "errata"

    @property
    def closing(self) -> Path:
        return self.run_root / "CLOSING.md"

    @property
    def reading_table(self) -> Path:
        return self.run_root / "READING_TABLE.md"

    @property
    def comparison(self) -> Path:
        return self.run_root / "COMPARISON.md"

    def cycle(self, cycle: int) -> CyclePaths:
        if type(cycle) is not int or not 1 <= cycle <= 99:
            raise _fail("CYCLE_OUT_OF_RANGE", "a cycle index is a whole number 1..99")
        return CyclePaths(cycle=cycle, root=self.cycles / f"cycle-{cycle:02d}")

    def step_path(self, index: int, kind: str, *, open_marker: bool = False) -> Path:
        """``steps/NNNN-KIND.json``, or its ``.open`` marker (design 4.2, 4.3)."""

        if type(index) is not int or not 0 <= index <= 9999:
            raise _fail("STEP_RECEIPT_INVALID", "a step index is a whole number 0..9999")
        if kind not in STEP_KINDS:
            raise _fail("STEP_RECEIPT_INVALID", f"unknown step kind: {kind!r}")
        name = f"{index:04d}-{kind}.json" + (".open" if open_marker else "")
        return self.steps / name

    def reading_dir(self, row_key: str) -> Path:
        """``readings/<row_key>`` as a path-safe, collision-free directory.

        A row key is a coordinate expression - ``problem/arm/cycle-1/node#r3`` -
        and is not a directory component. Unsafe characters fold to ``_`` and a
        twelve-character digest of the exact key is appended, so two keys that
        fold alike still get two directories and the mapping stays a pure
        function of the key.
        """

        key = _text(row_key, "row_key")
        folded = _SLUG_UNSAFE.sub("_", key)[:80].strip(".") or "row"
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]
        return self.readings / f"{folded}-{digest}"

    def as_dict(self) -> dict[str, str]:
        return {name: getattr(self, name).as_posix() for name in (
            "run_root", "config", "preregistration", "obligations", "ceiling", "plan",
            "preflight", "lock", "steps", "graph", "cycles", "readings", "audits",
            "appeals", "errata", "closing", "reading_table", "comparison")}


def run_paths(root: Path | str, run_id: str) -> RunPaths:
    """The layout of one run under ``<root>/experiments/loops/<run_id>``.

    ``root`` is the **repository root**, so :data:`LOOPS_ROOT` stays a constant
    of this module rather than a string each caller retypes. ``run_id`` is
    checked against the repository's identifier shape, which already forbids
    a separator and ``..``, so a run id can never reach outside the loops root.
    """

    run_id = _identifier(run_id, "run_id", "RUN_ID_INVALID")
    repo_root = Path(root)
    return RunPaths(repo_root=repo_root, run_id=run_id,
                    run_root=repo_root / LOOPS_ROOT / run_id)
