#!/usr/bin/env python3
"""W5-DRIVER - the CLI and the S0-S15 state machine of the automated loop.

Implements the wave-5 module ``W5-DRIVER`` of *The automated end-to-end harness
loop - FINAL design of record*, section 4: PREREGISTER, PREFLIGHT, PUBLISH_PLAN,
the per-cycle PREPARE / PUBLISH_IN / SEND / PUBLISH_EV / IMPORT / USE_TABLE /
READ / MARK / ADJUDICATE / DECIDE / PUBLISH_CY chain, CLOSE, reopen and appeal.

What this module is
-------------------

The *only* thing in the loop that holds state across steps and across cycles.
Every act it performs belongs to a module that owns it: W1-STEPS owns the
receipt ledger and the resume rule, W0-PUBLISH owns every git operation,
W1-GRAPH owns the graph's door, W3-TRIAL owns the guard, W4-READER owns the
reading arm's bookkeeping, W4-MARKER owns the pairwise guard, W2-DECIDE owns
the stop rule and W3-REPORT owns every rendered artifact.  This module
sequences them, files the facts none of them can see (the guard-block streak,
the ended arms, the halted step, the indeterminate coordinates), and publishes.

The one injection seam
----------------------

:class:`Modules` carries **one provider seam** - ``provider_factory`` - which is
the seam ``W6-DRYRUN`` binds and the only one that exists.  It is handed
unchanged to W2-ROLES (through W3-TRIAL and W4-MARKER) and to runner v2's
``send_wave``, because ``synthetic.ScriptedProviders`` answers both shapes.
Binding it replaces the **transport** and nothing else: every guard, every
pack, every write-once record and every custody check runs exactly as it does
live.  The other two fields are not seams onto behaviour: ``repo_root`` is the
tree the run is resolved against (wave-0 open question O3) and ``sleep`` is the
publisher's backoff clock, which changes how long a rejected push waits and
nothing about whether it succeeded.

Runner v2 is **imported** (``seats.runner_module()``, one process, one gate
registry) and ``send_round`` is called in-process.  Nothing here shells it, and
``run.lock`` refuses a second driver on the same run, because the five-per-key
ceiling of ``provider_openai_compat.slots_for`` holds only inside one process
(design 4.6).

Deviations from the design entry, and why
-----------------------------------------

* **The trial's cell key is minted from the reading-set key, not used raw.**
  ``roles.Coordinate`` admits only ``[A-Za-z0-9][A-Za-z0-9._#-]*`` per ``/``
  segment, and the pre-registered reading set's own keys carry ``->``
  (``h005-row/daily/mini_fcl/cycle01/objection#o1/target/p.objection.0#c1->…``).
  Read
  raw, every H005 row of the frozen reading set would refuse
  ``ROLE_COORDINATE_INVALID`` at its first critic call.  :func:`cell_key_for`
  folds each key to an admissible spelling and appends a twelve-character
  digest of the exact key, so the fold is injective; the correspondence is
  written into ``plan.json`` under ``reading_cells`` and PREFLIGHT asserts both
  admissibility and injectivity over the declared set.  The plan's own
  spelling stays the ``row_key`` throughout, so every record can be read both
  ways.
* **``dry_run(config, out)`` builds the gate's occurrence and walks ``run()``.**
  The induced-fault battery and its per-receipt assertions are W6-DRYRUN's
  (``tests/loop/test_dry_run_end_to_end.py``); this module carries no test
  logic.  With no config it returns what it built and ``ran: False`` rather
  than minting a plan it was not asked to freeze.
* **An appellate ruling ingested at a cycle open re-salts that invocation's
  ADJUDICATE / DECIDE step inputs** with the applied ruling ids.  Pass 1 of the
  reopened harness flips the label; a replayable step re-read over the flipped
  graph is not the same step, and recording it under the unsalted key would
  write a second receipt for a step whose recorded bytes it cannot reproduce.
* **A pinned file that moved between preregistration and ``run()`` refuses with
  ``SOURCE_PIN_MISMATCH``**, which is the code design 4.4's halt list names for
  that fact; a refusal to *compute* the identity stays ``PIN_INVALID`` /
  ``PLAN_ID_MISMATCH``.
* **S0 and S1 are the two public functions** ``preregister`` / ``preflight``;
  the ledger's steps begin at S2, matching 4.3's step classes.
* **SEND is refused (``INPUT_NOT_PUBLISHED``) when the plan commit is not on its
  ref.**  Publication-before-dispatch stated as a custody check: a dispatch over
  bytes the ref does not carry is the failure 4.1's "<- before any socket"
  arrow exists to prevent.
* **A later cycle reads what is left, not the whole table again.**  The
  reading tree is the run's, not the cycle's (4.2), so a row a previous cycle
  spent is a spent coordinate: W2-ROLES refuses to re-enter it (``NO_REPLAY``)
  and G11 refuses a re-read with no listed reopen reason.  A spent row is
  re-read only when a reason this plan declared is recorded through
  ``reopen()``, and the ``READ`` receipt names both the rows it skipped and the
  reason in force.
* **Only the publications and the dispatch are bracketed in the activity log.**
  4.5 brackets "every search, read, modification, test and dispatch"; those two
  are the acts this driver performs on the repository, and every other step's
  own write-once receipt is the record of it.  ``receipts.activity`` shells
  ``tools/repo_activity.py`` and is never reimplemented; a tree carrying no
  decision ledger mints no receipt, brackets nothing, and says so in
  ``plan.json["activity"]``.
* **PREFLIGHT's planned-call figure covers the two legs it can derive** - the
  reading rows and the cross-case mark cells, at the per-row costs the guard
  parameters fix - and reports the remainder of ``max_calls`` as the audit
  window's declared allowance rather than recomputing a window whose sample of
  readings-on-record does not exist before cycle 1.  The clause the design
  states ("refuse if planned calls exceed ``config.max_calls``") is enforced on
  that figure.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping, Sequence

from minireason.loop import (
    audits as audits_module,
    contracts as contracts_module,
    custody,
    decide as decide_module,
    graph as graph_module,
    marker as marker_module,
    markprep as markprep_module,
    obligations as obligations_module,
    publish as publish_module,
    reader as reader_module,
    receipts as receipts_module,
    report as report_module,
    roles as roles_module,
    seats as seats_module,
    standard as standard_module,
    steps as steps_module,
    surface as surface_module,
    synthetic as synthetic_module,
    trial as trial_module,
)
from minireason.loop.types import (
    PINNED_SOURCE_PATHS,
    PROVIDER_MODES,
    LoopConfig,
    LoopError,
    run_paths,
    loop_plan_id as mint_plan_id,
)

__all__ = [
    "ARM_ENDED_TEXT",
    "BLOCK_STREAK_DEFINITION",
    "LEG_MARK",
    "LEG_READING",
    "LOOP_SOURCE_PINS",
    "MAX_WAVES_PER_CYCLE",
    "MODULE_PIN_KEYS",
    "Modules",
    "NEW_CODES",
    "STATE_RESPONSIBILITIES",
    "adjudicate",
    "appeal",
    "block_streak",
    "cell_key_for",
    "close",
    "dry_run",
    "effective_budget",
    "main",
    "planned_calls",
    "preregister",
    "preflight",
    "reopen",
    "row_identity",
    "run",
    "runner_v2",
    "seal_baselines",
    "status",
]

# --------------------------------------------------------------------------- #
# Codes, texts and definitions this module owns
# --------------------------------------------------------------------------- #

#: Codes this module introduces, with the one-line reason each exists.  Every
#: other code it raises is a member of ``types.FAILURE_CODES`` owned elsewhere
#: and is imported, never retyped (wave-0 open question O9).  ``tools/`` is
#: outside the package ``tests/loop/test_types.py`` walks, so these are folded
#: into ``FAILURE_CODES`` by hand and listed in that file's ``UNREACHED`` table
#: naming this driver; ``tests/loop/test_auto_loop.py`` runs the same token scan
#: over this file and asserts every one of them is reached here.
NEW_CODES: Mapping[str, str] = MappingProxyType({
    "RUN_NOT_FOUND":
        "status(), adjudicate(), appeal(), reopen() or close() could not locate a written plan for the run it was pointed at.",
    "APPEAL_PATH_INVALID":
        "appeal() was given no ruling path to stage, or a path that is not a readable appellate ruling document.",
    "APPEAL_TARGET_INVALID":
        "an appellate ruling names no registered target: a validity node, the standard, a prior ruling, or a cell:register token.",
    "READING_ROW_UNRESOLVED":
        "a pre-registered reading-set key names no row of the use table this cycle built, so the row could be neither read nor honestly reported as read.",
    "READING_KEY_INADMISSIBLE":
        "a pre-registered reading-set key folds to a coordinate W2-ROLES refuses, or two keys fold to one coordinate, so a call could not be addressed or two rows would share one records tree.",
    "BLOCK_STREAK_DEFINITION_MISMATCH":
        "PREFLIGHT's self-test of the guard-block streak counter did not reproduce the definition config.audit.streak_max_account states, so the account beside the number would be false.",
    "REGISTER_CELLS_DISAGREE":
        "the register cells opened at PREREGISTER are not the set markprep.program_marks will produce, so a mark would be refused after its calls were spent.",
    "CALIBRATION_NOT_FOUND":
        "the run declares an audit schedule and its run root carries no calibration.json, so o5's planted-flaw clause could never be discharged by the program that evaluates it.",
})

#: The fixed text the closing receipt and CYCLE.md print for an arm a delivery
#: failure ended (design 4.4; FW5 R5: non-evaluability is not refutation).
ARM_ENDED_TEXT = ("delivery ended this arm; no semantic verdict is issued "
                  "for its coordinates")

#: The closing record's own section for every failure and refusal **this run**
#: recorded, by the code its receipt or its refusal carried.  Design 4.7 asks
#: the closing receipt to name each induced failure by code, and a run is
#: resumable: the invocation that halts is usually not the invocation that
#: closes, so the section is minted from the run's own step ledger and run
#: state rather than from whatever this process still holds in memory.
RECORDED_FAILURES_HEADING = "failures and refusals this run recorded"
#: The closing record's section for the arms a delivery failure ended.
ARMS_ENDED_HEADING = "arms a delivery failure ended"
RECORDED_FAILURES_SENTENCE = (
    "Each line names the code the run's own receipt or refusal carried. A "
    "refusal is an act of the instrument, never a reading of the material, "
    "and mints no warrant either way.")
NOTHING_REFUSED = "- nothing in this run was refused or failed"

#: The guard-block streak, as WAVE3-INTERFACE §8 item 1 settles it and as
#: ``config.audit.streak_max_account`` states it.  PREFLIGHT asserts by
#: self-test that :func:`block_streak` is this and not another definition.
BLOCK_STREAK_DEFINITION = (
    "consecutive guard blocks per role, over that role's trials in dispatch "
    "order within the reading arm, reset by any trial of that role whose "
    "outcome is not a block")

#: The module-constant pins design 4.2 folds into ``loop_plan_id`` beside the
#: six repo-relative paths of ``types.PINNED_SOURCE_PATHS``.  They are named,
#: not path-shaped, so ``custody.verify_pins`` is never asked to re-derive them
#: from the tree; the source files that carry them are pinned by path as well.
MODULE_PIN_KEYS: Mapping[str, str] = MappingProxyType({
    # W3-REPORT refuses to render any table or report without the ceiling
    # pinned under ``standard.CEILING_PIN_KEY``; that key is the one owner of
    # the spelling and is never retyped here.
    standard_module.CEILING_PIN_KEY: standard_module.CEILING_SHA256,
    "minireason.loop.standard.STANDARD_BODY_SHA256":
        standard_module.STANDARD_BODY_SHA256,
    "minireason.loop.standard.CEILING_SHA256": standard_module.CEILING_SHA256,
    "minireason.loop.audits.CALIBRATION_EXCHANGES_SHA256":
        audits_module.CALIBRATION_EXCHANGES_SHA256,
    "minireason.loop.decide.DECIDE_SHA256": decide_module.DECIDE_SHA256,
})

#: Loop-package sources whose constants the plan leans on and whose bytes are
#: therefore inside the identity.  ``roles.py`` is here because the declared
#: resource conditions (``ROLE_MAX_TOKENS``, the ``min(timeout, 300)`` wall,
#: ``thinking``) are its constants and no config key carries them
#: (CLONE-PATCH item 4); ``decide.py`` because the stop rule is its program.
LOOP_SOURCE_PINS: tuple[str, ...] = (
    "src/minireason/loop/roles.py",
    "src/minireason/loop/decide.py",
    "src/minireason/loop/standard.py",
    "src/minireason/loop/audits.py",
)

#: The S0-S15 states, with the function implementing each (design 4.1).
STATE_RESPONSIBILITIES: tuple[tuple[str, str, str], ...] = (
    ("S0", "PREREGISTER", "preregister"),
    ("S1", "PREFLIGHT", "preflight"),
    ("S2", "PUBLISH_PLAN", "run/_publish_plan"),
    ("S3", "CYCLE_OPEN", "run/_cycle_open"),
    ("S4", "PREPARE", "run/_prepare"),
    ("S5", "PUBLISH_IN", "run/_publish_in"),
    ("S6", "SEND", "run/_send"),
    ("S7", "PUBLISH_EV", "run/_publish_ev"),
    ("S8", "IMPORT", "run/_import"),
    ("S9", "USE_TABLE", "run/_use_table"),
    ("S10", "READ", "run/_read"),
    ("S11", "MARK", "run/_mark"),
    ("S12", "ADJUDICATE", "adjudicate"),
    ("S13", "DECIDE", "run/_decide"),
    ("S14", "PUBLISH_CY", "run/_publish_cycle"),
    ("S15", "CLOSE", "close"),
)

_OVERRIDES_NAME = "overrides.json"
_RUN_FILE = "_run.json"
_NO_LEDGER_RECEIPT = "REC-00000000-NOLEDGER"
_CALIBRATION_NAME = "calibration.json"

#: The legs a reading-set key may name, by its first path segment.
LEG_READING = "h005-row"
LEG_MARK = "c001-mark"

_UNSAFE_SEGMENT = re.compile(r"[^A-Za-z0-9._#-]")


def _fail(code: str, detail: str = "") -> LoopError:
    return LoopError(code, detail)


# --------------------------------------------------------------------------- #
# Reading-set keys: the plan's spelling, and the coordinate a call is spent on
# --------------------------------------------------------------------------- #

def cell_key_for(row_key: str) -> str:
    """An admissible ``roles.Coordinate`` key for one reading-set key.

    Each ``/`` segment is folded to the coordinate alphabet and a twelve
    character digest of the **exact** key is appended, so the fold is a pure,
    injective function of the plan's own spelling and two keys that fold alike
    still get two coordinates and two records trees.  The plan's spelling is
    never replaced: it stays the ``row_key`` on every record.
    """

    key = str(row_key)
    if not key:
        raise _fail("READING_KEY_INADMISSIBLE", "a reading-set key is non-empty")
    parts = [part for part in key.split("/") if part]
    if not parts:
        raise _fail("READING_KEY_INADMISSIBLE", f"{key!r} has no segments")
    folded = []
    for part in parts:
        text = _UNSAFE_SEGMENT.sub("-", part).strip("-") or "x"
        if not text[0].isalnum():
            text = "x" + text
        folded.append(text)
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]
    folded[-1] = f"{folded[-1]}#{digest}"
    return "/".join(folded)


def row_identity(row_key: str) -> tuple[str, str, str, str] | None:
    """The use-table row one ``h005-row/`` key names, or ``None``.

    The grammar the pre-registration writes is
    ``h005-row/<referring_coordinate_key>#<record_id>/<ref_field>/<ref_verbatim>``
    ``-><target_coordinate_key>#<target_record_id>``.  The tuple returned is the
    identity ``use_relation_h005`` gives each row:
    ``(referring_coordinate_key, referring_record_id, ref_field, ref_verbatim)``.
    """

    key = str(row_key)
    if not key.startswith(LEG_READING + "/"):
        return None
    body = key[len(LEG_READING) + 1:]
    left = body.split("->", 1)[0]
    try:
        prefix, ref_field, ref_verbatim = left.rsplit("/", 2)
        coordinate_key, record_id = prefix.rsplit("#", 1)
    except ValueError:
        return None
    if not (coordinate_key and record_id and ref_field and ref_verbatim):
        return None
    return (coordinate_key, record_id, ref_field, ref_verbatim)


def _table_index(rows: Sequence[Mapping[str, Any]]) -> dict[tuple, Mapping[str, Any]]:
    index: dict[tuple, Mapping[str, Any]] = {}
    for row in rows:
        identity = (str(row.get("referring_coordinate_key", "")),
                    str(row.get("referring_record_id", "")),
                    str(row.get("ref_field", "")),
                    str(row.get("ref_verbatim", "")))
        index.setdefault(identity, row)
    return index


# --------------------------------------------------------------------------- #
# The guard-block streak (WAVE3 §8 item 1; CLONE-PATCH item 5)
# --------------------------------------------------------------------------- #

def _role_of(block: Any) -> str:
    """The seat role a block record was spent on, off W2-ROLES' own layout.

    ``roles.Coordinate.slug`` is ``<key>/<role>[-<seat>]``, so the record path
    a block names ends ``…/<key>/<role>-<n>/provider/call-NNNN.<part>.json``.
    A block that dispatched nothing - ``blocked:constitution`` - names no ref
    and belongs to no role; it therefore neither extends nor resets a streak.
    """

    for attribute in ("prompt_ref_path", "raw_ref_path"):
        raw = str(getattr(block, attribute, "") or "")
        if not raw:
            continue
        parts = [part for part in Path(raw).parts if part not in ("/", "")]
        for part in reversed(parts):
            head = part.split("-", 1)[0].split(".", 1)[0]
            if head in roles_module.ROLES:
                return head
    return ""


def block_streak(blocks: Iterable[Any], outcomes: Iterable[tuple[str, str]] = ()) -> int:
    """The longest live per-role streak, as :data:`BLOCK_STREAK_DEFINITION`.

    ``blocks`` is ``reader.Readings.blocks`` - the block records in dispatch
    order.  ``outcomes`` is ``(row_key, outcome)`` in the same order, so a row
    whose trial did **not** block resets the streak of every role that answered
    it; a reader that hands no outcomes resets on nothing and the count is the
    run of consecutive blocked rows alone.  The number returned is the largest
    streak standing at the end of the pass, over every role.
    """

    by_row: dict[str, set[str]] = {}
    order: list[str] = []
    for block in blocks:
        row = str(getattr(block, "row_key", ""))
        if row not in by_row:
            by_row[row] = set()
            order.append(row)
        role = _role_of(block)
        if role:
            by_row[row].add(role)
    blocked_rows = {row for row in by_row}
    sequence = [(row, outcome) for row, outcome in outcomes] or \
        [(row, trial_module.OUTCOME_BLOCKED) for row in order]
    streaks: dict[str, int] = {}
    longest = 0
    for row, outcome in sequence:
        roles_here = by_row.get(row, set())
        if outcome == trial_module.OUTCOME_BLOCKED and row in blocked_rows:
            for role in roles_here:
                streaks[role] = streaks.get(role, 0) + 1
                longest = max(longest, streaks[role])
        else:
            # A trial of this row that did not block resets every role that
            # answered it.  A role that answered nothing here is untouched.
            for role in roles_here or set(streaks):
                streaks[role] = 0
    return longest


_STREAK_PROBE: tuple[tuple[str, str, str, int], ...] = (
    # (row, role, outcome, the streak that must stand after this row)
    ("row-1", "judge", trial_module.OUTCOME_BLOCKED, 1),
    ("row-2", "judge", trial_module.OUTCOME_BLOCKED, 2),
    ("row-3", "judge", trial_module.OUTCOME_SUSTAINED, 0),
    ("row-4", "judge", trial_module.OUTCOME_BLOCKED, 1),
)


@dataclass(frozen=True)
class _ProbeBlock:
    row_key: str
    prompt_ref_path: str
    raw_ref_path: str = ""


def _streak_self_test() -> None:
    """PREFLIGHT's assertion that :data:`BLOCK_STREAK_DEFINITION` is in force."""

    blocks = [_ProbeBlock(row, f"{row}/{role}-1/provider/call-0001.request.json")
              for row, role, outcome, _ in _STREAK_PROBE
              if outcome == trial_module.OUTCOME_BLOCKED]
    outcomes = [(row, outcome) for row, _role, outcome, _ in _STREAK_PROBE]
    for index, (_row, _role, _outcome, expected) in enumerate(_STREAK_PROBE, start=1):
        observed = block_streak(
            [b for b in blocks
             if b.row_key in {r for r, _, _, _ in _STREAK_PROBE[:index]}],
            outcomes[:index])
        standing = max(expected, max(
            (value for _r, _x, _o, value in _STREAK_PROBE[:index]), default=0))
        if observed != standing:
            raise _fail(
                "BLOCK_STREAK_DEFINITION_MISMATCH",
                f"the counter answered {observed} where {standing} is the "
                f"streak {BLOCK_STREAK_DEFINITION} leaves after {index} rows")


# --------------------------------------------------------------------------- #
# The planned-call figure (design 4.1 S1)
# --------------------------------------------------------------------------- #

def planned_calls(config: LoopConfig, mark_cells: int = 0) -> dict[str, Any]:
    """The reading and mark legs' worst-case call counts, with the arithmetic.

    Neither number is a metric: both are the spend boundary S1 refuses past
    (``max_calls``), reported as an arithmetic a reader can check.
    """

    judges = max(1, len(config.seats.judges))
    paraphrases = max(0, int(config.seats.paraphrase_n))
    row_cost = 1 + 1 + judges + judges + 1 + judges * paraphrases
    mark_cost = judges + judges + 1 + judges * paraphrases
    rows = [key for key in config.reading_set if str(key).startswith(LEG_READING + "/")]
    total = len(rows) * row_cost + mark_cells * mark_cost
    return {
        "row_cost": row_cost,
        "row_cost_arithmetic": (
            f"1 critic + 1 defender + {judges} judges + {judges} order-swapped "
            f"+ 1 variator + {judges} judges x {paraphrases} paraphrases = {row_cost}"),
        "rows": len(rows),
        "mark_cost": mark_cost,
        "mark_cells": mark_cells,
        "planned_calls": total,
    }


# --------------------------------------------------------------------------- #
# The injection seam
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Modules:
    """The driver's seams.  One of them is a provider seam; the others are not.

    ``provider_factory`` is W6-DRYRUN's, handed unchanged to W2-ROLES and to
    runner v2's ``send_wave``.  ``repo_root`` is the tree paths resolve against
    (wave-0 O3).  ``sleep`` is the publisher's backoff clock.  Nothing here can
    replace a guard, a pack, a record or a custody check.
    """

    provider_factory: Any = None
    repo_root: Any = None
    sleep: Callable[[float], None] | None = None

    def root(self) -> Path:
        root = self.repo_root if self.repo_root is not None \
            else receipts_module.DEFAULT_REPO_ROOT
        if root is None:
            raise _fail("RUN_NOT_FOUND",
                        "no repository root is discoverable; pass "
                        "Modules(repo_root=...)")
        return Path(root)


def runner_v2() -> Any:
    """Runner v2, imported in-process under its one canonical name.

    ``seats.runner_module()`` is the one importer: one process holds one
    ``key_gate`` registry, and a second import under a second name would be a
    second ceiling on one credential (design 4.6).
    """

    return seats_module.runner_module()


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #

def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(custody.encoded(value))


def _read_json(path: Path) -> Any:
    return json.loads(path.read_bytes().decode("utf-8"))


def _write_overrides(run_root: Path, overrides: Mapping[str, Any]) -> None:
    _write_json(run_root / _OVERRIDES_NAME,
                {"schema": "minireason.loop.overrides.v1", **dict(overrides)})


def _read_overrides(run_root: Path) -> dict[str, Any]:
    try:
        raw = _read_json(run_root / _OVERRIDES_NAME)
    except (OSError, ValueError):
        return {}
    if not isinstance(raw, dict):
        return {}
    return {k: v for k, v in raw.items() if k != "schema"}


def _save_run_state(run_root: Path, state: Mapping[str, Any]) -> None:
    _write_json(run_root / _RUN_FILE, dict(state))


def _load_run_state(run_root: Path) -> dict[str, Any]:
    try:
        raw = _read_json(run_root / _RUN_FILE)
    except (OSError, ValueError):
        return {}
    return dict(raw) if isinstance(raw, dict) else {}


def effective_budget(config: LoopConfig, budget_override: int | None) -> int:
    """The cycle budget after a ``--cycles`` override.  Downward only (4.2)."""

    if budget_override is None:
        return config.cycle_budget
    try:
        budget = int(budget_override)
    except (TypeError, ValueError):
        raise _fail("CONFIG_INVALID_VALUE",
                    f"--cycles must be an integer: {budget_override!r}")
    if budget < 1:
        raise _fail("CONFIG_INVALID_VALUE",
                    f"--cycles must be at least one cycle: {budget}")
    if budget > config.cycle_budget:
        raise _fail(
            "BUDGET_RAISED",
            f"--cycles {budget} would raise the declared budget "
            f"{config.cycle_budget}; an upward change is a new plan, never an "
            "override")
    return budget


def _load_config(config_path: str | Path, budget_override: int | None = None,
                 provider_mode: str | None = None,
                 publish_ref: str | None = None) -> LoopConfig:
    """Load the frozen config, with the two flags that may touch it.

    ``--mode`` and ``--publish-ref`` are both **inside** ``loop_plan_id``, so
    neither may silently change a frozen declaration: a mode that disagrees
    with the config's is refused rather than applied, and a ref is accepted only
    where the config declares none (design 4.2's "default: the branch's
    upstream").  Forcing ``OfflineProvider`` everywhere is ``dry-run``'s, which
    binds the provider seam; a flag cannot do it without changing the identity.
    """

    config = LoopConfig.load(config_path)
    effective_budget(config, budget_override)  # raise before anything is written
    if provider_mode is not None:
        if provider_mode not in PROVIDER_MODES:
            raise _fail("CONFIG_INVALID_VALUE",
                        f"--mode must be one of {list(PROVIDER_MODES)}")
        if provider_mode != config.provider_mode:
            raise _fail(
                "CONFIG_INVALID_VALUE",
                f"--mode {provider_mode} disagrees with the frozen "
                f"provider_mode {config.provider_mode}; the mode is inside "
                "loop_plan_id and a new mode is a new pre-registration")
    if publish_ref:
        if config.publish_ref and config.publish_ref != publish_ref:
            raise _fail(
                "CONFIG_INVALID_VALUE",
                f"--publish-ref {publish_ref} disagrees with the frozen "
                f"publish_ref {config.publish_ref}")
        if not config.publish_ref:
            config = LoopConfig.from_mapping(
                {**config.as_dict(), "publish_ref": publish_ref})
    return config


def _occurrence_dirs(root: Path, names: Iterable[str]) -> list[Path]:
    return [root / str(name) for name in names]


# --------------------------------------------------------------------------- #
# The driver
# --------------------------------------------------------------------------- #

class _Driver:
    """One invocation's worth of state: config, paths, plan id, ledger, lock."""

    def __init__(self, config: LoopConfig, modules: Modules | None,
                 config_path: Path | None = None) -> None:
        self.config = config
        self.modules = modules if modules is not None else Modules()
        self.paths = run_paths(self.modules.root(), config.run_id)
        self.config_path = config_path
        self.budget = config.cycle_budget
        self.plan: Mapping[str, Any] = {}
        self.plan_id: str = ""
        self.ledger: steps_module.StepLedger | None = None
        self.lock: steps_module.RunLock | None = None
        self.harness: Any = None
        self.obligations: Any = None
        self.seat_plan: Any = None
        self.ended_arms: list[dict[str, Any]] = []
        self.receipt_id = _NO_LEDGER_RECEIPT
        self.rulings_applied_this_run: list[str] = []
        self.readings_by_cycle: dict[int, Any] = {}
        self.marks_by_cycle: dict[int, list[Any]] = {}
        self.tables: dict[int, list[Mapping[str, Any]]] = {}
        self.situations: dict[int, Any] = {}
        self.decisions: dict[int, Any] = {}
        #: The guard-block streak this pass measured, per cycle, over the rows
        #: it dispatched in dispatch order (never a rate and never a share).
        self.block_streaks: dict[int, int] = {}
        self.audit_findings: list[Mapping[str, Any]] = []
        self.rendered: dict[str, str] = {}
        self.since_seq = 0

    # -- identity ----------------------------------------------------------- #

    def _path_pins(self) -> dict[str, str]:
        """Every path-shaped pin, digested against the tree now."""

        root = self.modules.root()
        wanted: list[str] = [rel for rel in PINNED_SOURCE_PATHS
                             if (root / rel).is_file()]
        wanted += [rel for rel in LOOP_SOURCE_PINS if (root / rel).is_file()]
        for name in ("obligations.json", "CEILING.md", _CALIBRATION_NAME):
            path = self.paths.run_root / name
            if path.is_file():
                wanted.append(path.relative_to(root).as_posix())
        for occurrence in _occurrence_dirs(root, self.config.occurrences):
            for name in ("plan.json", "material.json"):
                if (occurrence / name).is_file():
                    wanted.append((occurrence / name).relative_to(root).as_posix())
        for occurrence in _occurrence_dirs(root, self.config.contrast.occurrences):
            for name in ("comparison.json", "material.json"):
                if (occurrence / name).is_file():
                    wanted.append((occurrence / name).relative_to(root).as_posix())
        return custody.pins(root, sorted(set(wanted)))

    def _pins(self) -> dict[str, str]:
        """The frozen identity's pin map: paths plus the named module pins."""

        pins = self._path_pins()
        pins.update(MODULE_PIN_KEYS)
        return pins

    def _tree_pins(self, plan: Mapping[str, Any]) -> dict[str, str]:
        """The subset ``custody.verify_pins`` can re-derive from this tree.

        A named module pin (``minireason.loop.…``) is a constant, not a path,
        and asking custody to find a file of that name would be a refusal about
        the pin's spelling rather than about the tree.  The **sources** that
        carry those constants are pinned by path beside them, so nothing goes
        unchecked.
        """

        root = self.modules.root()
        return {key: value for key, value in dict(plan.get("pins", {})).items()
                if "/" in key and (key not in MODULE_PIN_KEYS
                                   or (root / key).is_file())}

    def _plan_view(self) -> dict[str, Any]:
        view = dict(self.config.as_dict())
        stored = _read_overrides(self.paths.run_root)
        if "cycle_budget" in stored:
            view["cycle_budget"] = int(stored["cycle_budget"])
        return view

    def _mint(self) -> str:
        return mint_plan_id(self._plan_view(), self._pins())

    def _ledger_file(self) -> Path | None:
        path = self.modules.root() / receipts_module.LEDGER_RELATIVE
        return path if path.is_file() else None

    def _open_ledger(self) -> steps_module.StepLedger:
        return steps_module.StepLedger(
            self.paths.run_root, self.plan_id,
            timeouts=self.config.timeouts,
            ledger_path=self._ledger_file())

    def _graph_root(self) -> Path:
        return graph_module.resolve_graph_root(self.modules.root(),
                                               self.config.graph_root)

    def _open_harness(self) -> Any:
        return graph_module.open_graph(self._graph_root(),
                                       clock=graph_module.fixed_clock())

    def _registry(self) -> Any:
        """The frozen endpoints registry: the pinned file, never a default.

        ``endpoints.json`` is one of the six ``types.PINNED_SOURCE_PATHS``, so
        the registry a seat plan is built from is the one the plan identity
        pins - not whichever copy happens to sit beside the installed package.
        """

        path = self.modules.root() / "src/minireason/data/endpoints.json"
        return seats_module.load_registry(path if path.is_file() else None) \
            if path.is_file() else seats_module.load_registry()

    def seats(self) -> Any:
        if self.seat_plan is None:
            self.seat_plan = seats_module.select_seats(self._registry(),
                                                       self.config.seats)
        return self.seat_plan

    def judge_labels(self) -> tuple[str, ...]:
        """The panel the audit layer is asked about: the pinned judge seats.

        WAVE4 §8 item 4: a program-written mark carries the seat ``program``,
        which ``graph.seats_on_record`` reports, and paraphrase-auditing the
        program is not a thing the audit layer should be asked to do.  The
        panel is therefore always explicit.
        """

        plan = self.seats()
        labels = []
        for index, _seat in enumerate(getattr(plan, "judges", ()) or ()):
            labels.append(roles_module.Coordinate(
                role="judge", key="panel", seat_index=index).seat_label)
        return tuple(labels)

    # -- steps -------------------------------------------------------------- #

    # -- the activity log (design 4.5) -------------------------------------- #

    def _activity(self, action: str, why: str, paths: Sequence[str] = ()) -> Any:
        """Bracket one repository act with ``begin`` and ``outcome`` records.

        ``receipts.activity`` **shells** ``tools/repo_activity.py`` and this
        module never reimplements it; ``receipts.DEFAULT_AGENT`` is already
        ``auto_loop``, which is this caller.  A run whose tree carries no
        ledger minted no receipt id, and an activity record is addressed to a
        receipt: such a run brackets nothing and its plan says so
        (``plan.json["activity"]``).  That is one stated condition - is this the
        publication checkout? - and not a per-call guard.

        **What is bracketed.** Design 4.5 brackets "every search, read,
        modification, test and dispatch".  The acts this driver performs on the
        repository are two: every **publication** (the modification) and the
        **dispatch** (SEND).  Every other step writes inside the run's own tree,
        and its own write-once receipt is the record of it; a second record of
        one act in another log would be two statements of one fact.
        """

        if not self.receipt_id or self.receipt_id == _NO_LEDGER_RECEIPT:
            return contextlib.nullcontext()
        return receipts_module.bracket(
            action, why, "walk the pre-registered loop to its own stopping rule",
            list(paths), decision=self.receipt_id,
            repo_root=self.modules.root())

    def _run_step(self, kind: str, cycle: int | None,
                  inputs: Mapping[str, Any] | None,
                  fn: Callable[[steps_module.StepHandle], Any],
                  *, wave: str | None = None) -> Any:
        assert self.ledger is not None
        if kind != "SEND":
            return self.ledger.run_step(kind, cycle, inputs, fn, wave=wave)
        with self._activity(
                f"loop step {kind}",
                f"the {kind} transition of run {self.config.run_id}"
                + (f", cycle {cycle}" if cycle else ""),
                [self.rel(occurrence) for occurrence
                 in _occurrence_dirs(self.modules.root(),
                                     self.config.occurrences)]):
            return self.ledger.run_step(kind, cycle, inputs, fn, wave=wave)

    def _publish(self, kind: str, paths: list[str], message: str, *,
                 cycle: int | None = None, wave: str | None = None,
                 inputs: Mapping[str, Any] | None = None) -> Any:
        """Every git operation goes through publish(); never shelled."""

        assert self.ledger is not None
        with self._activity(f"publish {kind}",
                            f"publication before dispatch for run "
                            f"{self.config.run_id}", paths):
            return self.ledger.publish_step(
                kind, self.modules.root(), paths, message,
                ref=self.config.publish_ref or None, cycle=cycle, wave=wave,
                inputs=inputs, sleep=self.modules.sleep)

    def rel(self, path: Path) -> str:
        return Path(path).resolve().relative_to(
            self.modules.root().resolve()).as_posix()


# --------------------------------------------------------------------------- #
# S0 PREREGISTER
# --------------------------------------------------------------------------- #

def _stage_bundle(drv: _Driver) -> None:
    """Put obligations, the ceiling and the calibration rows under the run root."""

    root = drv.modules.root()
    obligations_src = root / drv.config.obligations_path
    body = obligations_src.read_bytes()
    drv.obligations = obligations_module.load_obligations(obligations_src)
    if drv.paths.obligations.resolve() != obligations_src.resolve():
        drv.paths.obligations.write_bytes(body)
    drv.paths.ceiling.write_text(standard_module.CEILING_TEXT, encoding="utf-8")
    target = drv.paths.run_root / _CALIBRATION_NAME
    if not target.is_file() and drv.config_path is not None:
        source = Path(drv.config_path).resolve().parent / _CALIBRATION_NAME
        if source.is_file() and source.resolve() != target.resolve():
            target.write_bytes(source.read_bytes())


def _open_inventory(drv: _Driver) -> dict[str, Any]:
    """Open every cell this run may read, before any call (design 3(c)).

    Three families, and the third is why the trichotomy can be complete:

    * one cell per pre-registered reading row;
    * one register cell per ``(cell, register, comparison)`` W4-MARKER may
      mark, which ``mark_cell`` refuses to call into if it is not already open
      (WAVE4 §8 item 3);
    * one cell per **juxtaposition of the attached contrast study**, marked or
      not.  ``reader.Readings.unread`` is every open cell nothing read, so a
      juxtaposition this run never marks is still inventoried as unread rather
      than being absent from the record (CLONE-PATCH item 6).
    """

    root = drv.modules.root()
    reading_keys = [cell_key_for(key) for key in drv.config.reading_set
                    if str(key).startswith(LEG_READING + "/")]
    register_keys: list[graph_module.CellKey] = []
    juxtapositions: list[str] = []

    cells = _mark_cells(drv)
    seal_baselines(drv, cells)
    for cell in cells:
        for comparison, register in _register_cells_of(cell):
            register_keys.append(graph_module.CellKey(
                cell=cell.cell_id, register=register, comparison=comparison))

    study = str(drv.config.contrast.study or "")
    if study:
        for occurrence in sorted((root / study).glob("occurrence-*")):
            comparison = occurrence / "comparison.json"
            if not comparison.is_file():
                continue
            try:
                loaded = markprep_module.load_occurrence(occurrence)
            except Exception:
                continue
            for endpoint, arm in loaded.cell_keys:
                juxtapositions.append(
                    f"{LEG_MARK}/{Path(study).name}/{occurrence.name}/"
                    f"{endpoint}/{arm}")

    keys: list[Any] = list(reading_keys) + list(register_keys) + list(juxtapositions)
    opened = graph_module.open_cells(drv.harness, keys)
    return {
        "reading_cells": sorted(reading_keys),
        "register_cells": sorted(key.token for key in register_keys),
        "juxtaposition_cells": sorted(juxtapositions),
        "opened": len(opened) if isinstance(opened, Mapping) else 0,
    }


def _register_cells_of(cell: Any) -> list[tuple[str, str]]:
    """Every ``(comparison, register)`` W4-MARKER may write into for one cell.

    Read off ``markprep.program_marks``' own record - the ``registers`` block of
    each comparison - so the set PREFLIGHT asserts is the set the marker will
    produce and not a product this module recomputed (WAVE4 §8 item 3).
    """

    marks = markprep_module.program_marks(cell)
    found: list[tuple[str, str]] = []
    for comparison, block in sorted((marks.get("comparisons") or {}).items()):
        for register in sorted((block.get("registers") or {})):
            found.append((str(comparison), str(register)))
    return found


def _baseline_dir(drv: _Driver, cell: Any) -> Path:
    return drv.paths.run_root / "contrast" / _slugify(cell.cell_id) / "baseline"


def seal_baselines(drv: "_Driver", cells: Sequence[Any]) -> dict[str, str]:
    """Write every cell's within-ORIGINAL baseline once, and seal the cell (G8).

    This happens at **S0**, before ``markprep.program_marks`` is asked anything
    and long before any cross-case pack can render: the baseline is written
    first or it is not a baseline.  On every later pass the file is already
    there and the seal is re-derived from its bytes, never rewritten.
    """

    seals: dict[str, str] = {}
    for cell in cells:
        target = _baseline_dir(drv, cell)
        sealed = target / markprep_module.BASELINE_FILENAME
        if sealed.is_file():
            seals[cell.cell_id] = cell.seal(custody.sha256_path(sealed))
        else:
            target.mkdir(parents=True, exist_ok=True)
            seals[cell.cell_id] = markprep_module.write_baseline(cell, None, target)
    return seals


def _mark_cells(drv: _Driver) -> list[Any]:
    """Every ``markprep.Cell`` the contrast leg of this run marks.

    Two declared shapes, both ``markprep``'s own: a published C001 occurrence
    (``comparison.json`` plus its material, through ``load_occurrence``), and a
    contrast leg document in ``markprep.CONTRAST_LEG_SCHEMA`` (``contrast.json``
    beside the occurrence, through ``cell_from_contrast_leg``).  Nothing else is
    a cell source and nothing here invents one.
    """

    if not drv.config.contrast.attached:
        return []
    cells: list[Any] = []
    root = drv.modules.root()
    for occurrence in _occurrence_dirs(root, drv.config.contrast.occurrences):
        if (occurrence / "comparison.json").is_file():
            loaded = markprep_module.load_occurrence(occurrence)
            for endpoint, arm in loaded.cell_keys:
                cells.append(loaded.cell(endpoint, arm))
            continue
        leg_path = occurrence / "contrast.json"
        if leg_path.is_file():
            leg = _read_json(leg_path)
            # The address space is the leg's own.  ``markprep`` resolves every
            # replicate's refs through it, and a cell built without it reads no
            # reference as engaging a criticism: the within-ORIGINAL baseline
            # then computes EMPTY for every register, which makes G9's program
            # downgrade unreachable for every contrast-leg cell in the loop.  A
            # leg declaring neither key behaves exactly as it did before.
            addresses = leg.get("addresses")
            ids = leg.get("objection_ids")
            for case in sorted((leg.get("cases") or {})):
                cells.append(markprep_module.cell_from_contrast_leg(
                    leg, case,
                    addresses=addresses if isinstance(addresses, Mapping) else None,
                    objection_ids=tuple(ids) if isinstance(ids, (list, tuple)) else ()))
    return cells


def preregister(config: LoopConfig | str | Path, *,
                modules: Modules | None = None,
                budget_override: int | None = None) -> Mapping[str, Any]:
    """S0 - freeze the config, mint ``loop_plan_id``, write and open the bundle."""

    config_path = None if isinstance(config, LoopConfig) else Path(config)
    if not isinstance(config, LoopConfig):
        config = _load_config(config, budget_override)
    drv = _Driver(config, modules, config_path)
    budget = effective_budget(config, budget_override)
    drv.budget = budget
    drv.paths.run_root.mkdir(parents=True, exist_ok=True)
    if budget_override is not None:
        _write_overrides(drv.paths.run_root, {"cycle_budget": budget})
    _write_json(drv.paths.config, config.as_dict())
    _stage_bundle(drv)

    calibration = drv.paths.run_root / _CALIBRATION_NAME
    calibration_sha = custody.sha256_path(calibration) if calibration.is_file() else ""

    drv.plan_id = drv._mint()
    ledger_file = drv._ledger_file()
    if ledger_file is not None:
        drv.receipt_id = receipts_module.open_preregistration(
            ledger_path=ledger_file, loop_plan_id=drv.plan_id,
            run_id=config.run_id, source_identity=decide_module.DECIDE_SHA256)
        receipts_module.set_current_receipt(drv.receipt_id)
    prereg_text = receipts_module.render_preregistration(
        drv.receipt_id, receipts_module.utc_stamp(),
        loop_plan_id=drv.plan_id, run_id=config.run_id,
        source_identity=decide_module.DECIDE_SHA256)
    standard_module.assert_no_exhaustion_claim(prereg_text, "preregistration.md")
    drv.paths.preregistration.write_text(prereg_text, encoding="utf-8")

    drv.harness = drv._open_harness()
    standard_id = graph_module.register_standard(drv.harness)
    kappa_id = graph_module.register_kappa_read(drv.harness)
    inventory = _open_inventory(drv)

    plan = {
        "schema": "minireason.loop.plan.v1",
        "loop_plan_id": drv.plan_id,
        "config": config.as_dict(),
        "cycle_budget": budget,
        "pins": drv._pins(),
        "reading_set": [str(row) for row in config.reading_set],
        # CLONE-PATCH item 1: the digest o5's planted-flaw clause reads back
        # off every AuditReport this run registers.
        "calibration_sha256": calibration_sha,
        # The plan's spelling of each row, beside the coordinate a call on it
        # is addressed to (see the module docstring's first deviation).
        "reading_cells": {str(key): cell_key_for(key)
                          for key in config.reading_set},
        "block_streak_definition": BLOCK_STREAK_DEFINITION,
        "receipt_id": drv.receipt_id,
        "activity": ("bracketed through receipts.activity"
                     if drv.receipt_id != _NO_LEDGER_RECEIPT
                     else "not bracketed: this tree carries no decision ledger, "
                          "so no receipt was minted for an activity record to "
                          "address"),
        "opened_cells": inventory,
        "standard_id": standard_id,
        "kappa_id": kappa_id,
    }
    _write_json(drv.paths.plan, plan)
    drv.plan = plan

    _save_run_state(drv.paths.run_root, {
        "receipt_id": drv.receipt_id,
        "standard_id": standard_id,
        "kappa_id": kappa_id,
        "arms_ended": [],
        "applied_rulings": [],
        "closing_names": [],
        "since_seq": 0,
    })
    return {"loop_plan_id": drv.plan_id, "run_root": str(drv.paths.run_root),
            "cycle_budget": budget,
            "calibration_sha256": calibration_sha,
            "opened_cells": inventory,
            "preregistration_receipt": drv.receipt_id}


# --------------------------------------------------------------------------- #
# S1 PREFLIGHT
# --------------------------------------------------------------------------- #

def preflight(config: LoopConfig | str | Path, *,
              modules: Modules | None = None) -> Mapping[str, Any]:
    """S1 - the offline check of design 4.1 S1.

    No socket and no credential: the seat plan is built off the frozen
    registry, every pin is re-derived, every reading key is self-tested for
    coordinate admissibility and offset resolution, the guard-block streak
    counter is self-tested against its declared definition, the opened register
    cells are compared with the set ``markprep.program_marks`` will produce, and
    a planned-call figure larger than ``config.max_calls`` is refused by name.
    """

    config_path = None if isinstance(config, LoopConfig) else Path(config)
    if not isinstance(config, LoopConfig):
        config = _load_config(config)
    drv = _Driver(config, modules, config_path)
    if not drv.paths.plan.is_file():
        raise _fail("RUN_NOT_FOUND", f"{drv.paths.plan} is absent; preregister first")
    drv.plan = _read_json(drv.paths.plan)
    drv.plan_id = str(drv.plan.get("loop_plan_id", ""))

    report: dict[str, Any] = {
        "schema": "minireason.loop.preflight.v1",
        "loop_plan_id": drv.plan_id,
        "mode": "offline",
        "provider_calls": 0,
        "checks": [],
        "status": "OK",
    }

    def refuse(code: str, detail: str) -> LoopError:
        report["status"] = "REFUSED"
        _write_json(drv.paths.preflight, report)
        return _fail(code, detail)

    if _frozen_plan_id(drv) != drv.plan_id:
        raise refuse("PLAN_ID_MISMATCH",
                     "the frozen config no longer mints the plan id")

    findings = custody.verify_pins({"pins": drv._tree_pins(drv.plan)},
                                   drv.modules.root())
    report["checks"].append(
        {"check": "pins", "pins": len(drv.plan.get("pins", {})),
         "findings": [f.as_dict() for f in findings]})
    if findings:
        code = "SOURCE_PIN_MISMATCH" if any(
            f.code == "SOURCE_PIN_MISMATCH" for f in findings) else "CUSTODY_MISMATCH"
        names = ", ".join(f"{f.code} at {getattr(f, 'path', '')}" for f in findings)
        raise refuse(code, f"{len(findings)} pinned source(s) moved: {names}")

    for key in MODULE_PIN_KEYS:
        if drv.plan.get("pins", {}).get(key) != MODULE_PIN_KEYS[key]:
            raise refuse("SOURCE_PIN_MISMATCH",
                         f"{key} is not at the digest the plan froze")

    standard_module.assert_config_matches_standard(
        config.seats.as_dict(), config.reopen_reasons, where="config")
    plan_seats = seats_module.select_seats(drv._registry(), config.seats)
    seats_module.require_cross_family_judges(plan_seats)
    drv.seat_plan = plan_seats
    report["checks"].append({"check": "seats", "digest": plan_seats.digest,
                             "panel": list(drv.judge_labels())})

    # Coordinate admissibility and injectivity over the declared reading set.
    minted: dict[str, str] = {}
    for key in config.reading_set:
        coordinate = cell_key_for(key)
        try:
            roles_module.Coordinate(role="critic", key=coordinate)
        except LoopError as exc:
            raise refuse("READING_KEY_INADMISSIBLE",
                         f"{key!r} folds to {coordinate!r}, which W2-ROLES "
                         f"refuses: {exc.detail}")
        if coordinate in minted:
            raise refuse("READING_KEY_INADMISSIBLE",
                         f"{key!r} and {minted[coordinate]!r} fold to one "
                         f"coordinate {coordinate!r}")
        minted[coordinate] = str(key)
    report["checks"].append({"check": "reading_cells", "rows": len(minted)})

    _streak_self_test()
    report["checks"].append({"check": "block_streak",
                             "definition": BLOCK_STREAK_DEFINITION})

    # Every register cell the marker may write into is open already.
    cells = _mark_cells(drv)
    seal_baselines(drv, cells)
    wanted: set[str] = set()
    for cell in cells:
        for comparison, register in _register_cells_of(cell):
            wanted.add(graph_module.CellKey(
                cell=cell.cell_id, register=register,
                comparison=comparison).token)
    declared = set(drv.plan.get("opened_cells", {}).get("register_cells", ()))
    if wanted != declared:
        raise refuse(
            "REGISTER_CELLS_DISAGREE",
            f"{len(wanted)} register cells will be marked and "
            f"{len(declared)} were opened at PREREGISTER")
    report["checks"].append({"check": "register_cells", "cells": len(wanted)})

    if config.audit.period and not (drv.paths.run_root / _CALIBRATION_NAME).is_file():
        raise refuse("CALIBRATION_NOT_FOUND",
                     f"{drv.paths.run_root / _CALIBRATION_NAME} is absent and "
                     "audit.period declares a schedule")
    report["checks"].append(
        {"check": "calibration",
         "calibration_sha256": str(drv.plan.get("calibration_sha256", "")),
         "anchors": len(audits_module.build_calibration_set(
             standard_module.STANDARD_BODY))})

    derivation = planned_calls(config, mark_cells=len(wanted))
    derivation["audit_allowance"] = config.max_calls - derivation["planned_calls"]
    report["checks"].append({"check": "planned_calls", **derivation})
    report["planned_calls"] = derivation["planned_calls"]
    report["max_calls"] = config.max_calls
    if derivation["planned_calls"] > config.max_calls:
        raise refuse(
            "CONFIG_INVALID_VALUE",
            f"planned calls {derivation['planned_calls']} exceed "
            f"config.max_calls {config.max_calls}; preflight refuses")

    _write_json(drv.paths.preflight, report)
    return report


def _frozen_plan_id(drv: _Driver) -> str:
    """The plan id the *written* config mints now, over the plan's frozen pins.

    The pins are taken from ``plan.json`` and **not** re-derived from the tree,
    because the two facts are different and design 4.4 names them differently:
    a config that no longer mints the frozen id is ``PLAN_ID_MISMATCH``, and a
    pinned source whose bytes moved is a custody fact, checked inside the
    cycle's own step so that it halts, writes an erratum and stays sticky until
    an operator acknowledges it.
    """

    view = dict(_read_json(drv.paths.config))
    stored = _read_overrides(drv.paths.run_root)
    if "cycle_budget" in stored:
        view["cycle_budget"] = int(stored["cycle_budget"])
    return mint_plan_id(view, dict(drv.plan.get("pins", {})))


# --------------------------------------------------------------------------- #
# run(): S2..S14 in one invocation; S15 through close()
# --------------------------------------------------------------------------- #

def run(config: LoopConfig | str | Path, *,
        modules: Modules | None = None,
        budget_override: int | None = None,
        acknowledge: str | None = None,
        reason: str | None = None) -> Mapping[str, Any]:
    """S2..S15.  Resume is calling this again on the same run (design 4.3)."""

    config_path = None if isinstance(config, LoopConfig) else Path(config)
    if not isinstance(config, LoopConfig):
        config = _load_config(config, budget_override)
    drv = _Driver(config, modules, config_path)
    if not drv.paths.plan.is_file():
        raise _fail("RUN_NOT_FOUND", f"{drv.paths.plan} is absent; preregister first")
    drv.plan = _read_json(drv.paths.plan)
    drv.plan_id = str(drv.plan["loop_plan_id"])
    if _frozen_plan_id(drv) != drv.plan_id:
        raise _fail("PLAN_ID_MISMATCH",
                    "the frozen config no longer mints the plan id")
    frozen = LoopConfig.load(drv.paths.config)
    drv.config = frozen
    stored = _read_overrides(drv.paths.run_root)
    drv.budget = effective_budget(
        frozen, budget_override if budget_override is not None
        else (int(stored["cycle_budget"]) if "cycle_budget" in stored else None))
    if budget_override is not None and "cycle_budget" not in stored:
        _write_overrides(drv.paths.run_root, {"cycle_budget": drv.budget})
    if drv.budget != frozen.cycle_budget:
        # ``--cycles`` lowers the DECLARED budget, and clause 5 of the stop rule
        # reads ``config.cycle_budget``: handing decide() the unlowered config
        # would make an override the run honours a boundary the record never
        # reaches.  The lowering is itself recorded, in overrides.json and in
        # plan.json, so the two budgets are both readable.
        drv.config = LoopConfig.from_mapping(
            {**frozen.as_dict(), "cycle_budget": drv.budget})
    drv.obligations = obligations_module.load_obligations(
        drv.modules.root() / frozen.obligations_path)
    drv.ledger = drv._open_ledger()
    state = _load_run_state(drv.paths.run_root)
    drv.ended_arms = list(state.get("arms_ended", []))
    drv.since_seq = int(state.get("since_seq", 0) or 0)
    drv.receipt_id = str(state.get("receipt_id", _NO_LEDGER_RECEIPT))
    if drv.receipt_id and drv.receipt_id != _NO_LEDGER_RECEIPT:
        receipts_module.set_current_receipt(drv.receipt_id)

    if acknowledge is not None:
        if not reason:
            raise _fail("STEP_NOT_HALTED", "--acknowledge requires --reason")
        drv.ledger.acknowledge(acknowledge, reason)

    drv.lock = steps_module.RunLock(drv.paths.lock, drv.plan_id)
    drv.lock.acquire()
    try:
        drv.harness = drv._open_harness()
        _ingest_rulings(drv)
        _publish_plan(drv)
        prev_situation = None
        prev_triples = None
        decision = None
        cycles_completed = 0
        for cycle in range(1, drv.budget + 1):
            boundary = decide_module.declared_boundary_reached(
                cycle - 1, drv.config, _instrument(drv))
            _cycle_open(drv, cycle, boundary)
            if not boundary:
                _dispatch(drv, cycle)
                _import(drv, cycle)
                table = _use_table(drv, cycle)
                _read(drv, cycle, table)
                _mark(drv, cycle)
            situation = adjudicate(None, _driver=drv, _cycle=cycle)
            decision = _decide(drv, cycle, prev_situation, situation, prev_triples)
            _publish_cycle(drv, cycle, decision)
            cycles_completed = cycle
            prev_triples = decide_module.mark_triples(drv.harness)
            prev_situation = situation
            if boundary or (decision is not None and getattr(decision, "stop", False)):
                break
        closing = close(None, _driver=drv, _decision=decision)
        return {"loop_plan_id": drv.plan_id,
                "cycles_completed": cycles_completed,
                "closing": closing,
                "stop_reason": getattr(decision, "reason", None)
                if decision is not None else "open"}
    finally:
        drv.lock.release()


def _publish_plan(drv: _Driver) -> None:
    """S2 - commit + push + verify the plan; publication precedes dispatch."""

    names = ("config.json", "preregistration.md", "obligations.json",
             "CEILING.md", "plan.json", _CALIBRATION_NAME, "preflight.json")
    paths = [drv.rel(drv.paths.run_root / name) for name in names
             if (drv.paths.run_root / name).is_file()]
    drv._publish("PUBLISH_PLAN", paths, "loop plan published",
                 inputs={"loop_plan_id": drv.plan_id})


def _cycle_open(drv: _Driver, cycle: int, boundary: str) -> None:
    """S3 - custody, budget check, appellate rulings ingested, cycle receipt.

    The custody check is **here**, inside the cycle's first step and before any
    dispatch step of the cycle, so that a pinned source whose bytes moved halts
    the step (design 4.4): W1-STEPS writes the HALTED receipt and the erratum
    stub under ``<run>/errata/``, the process exits non-zero, and every later
    step is blocked until ``--acknowledge <step_key> --reason`` is recorded.
    The loop never works around custody.
    """

    def body(handle: steps_module.StepHandle) -> Mapping[str, Any]:
        findings = custody.verify_pins({"pins": drv._tree_pins(drv.plan)},
                                       drv.modules.root())
        handle.record_custody(findings)
        handle.record_output("cycle", cycle)
        handle.record_output("boundary", boundary or "open")
        handle.record_output("budget", drv.budget)
        handle.record_output("rulings", sorted(drv.rulings_applied_this_run))
        if findings:
            raise custody.CustodyMismatch(
                "SOURCE_PIN_MISMATCH" if any(
                    f.code == "SOURCE_PIN_MISMATCH" for f in findings)
                else "CUSTODY_MISMATCH",
                f"{len(findings)} pinned source(s) moved under the plan: "
                + ", ".join(sorted(str(getattr(f, "path", "")) for f in findings)))
        return {}

    drv._run_step("CYCLE_OPEN", cycle, {"cycle": cycle}, body)


def _ingest_rulings(drv: _Driver) -> None:
    """Apply every staged ruling in name order; the applied flip is pass 1's.

    Called once, before this invocation's first cycle step, so every receipt of
    the invocation reads one graph: the one with the ruling already in.
    """

    appeals = drv.paths.appeals
    if not appeals.is_dir():
        return
    state = _load_run_state(drv.paths.run_root)
    applied = list(state.get("applied_rulings", []))
    seen = {str(row.get("staged")) for row in applied}
    for path in sorted(appeals.iterdir()):
        if not path.is_file() or path.name in seen:
            continue
        raw = _read_json(path)
        if not isinstance(raw, Mapping):
            continue
        outcome = "APPELLATE_RULING_APPLIED"
        try:
            ruling = graph_module.AppellateRuling(
                ruling_id=str(raw.get("ruling_id", path.stem)),
                target=str(raw.get("target", "")),
                ground=str(raw.get("ground", "")),
                standard_id=str(raw.get("standard_id", "")),
                body=raw.get("body", {}))
            graph_module.apply_appeal(drv.harness, ruling)
            drv.rulings_applied_this_run.append(str(ruling.ruling_id))
        except Exception as exc:  # a ruling the graph refuses stays staged
            outcome = f"APPEAL_TARGET_INVALID: {type(exc).__name__}"
        applied.append({"staged": path.name, "target": raw.get("target"),
                        "outcome": outcome})
    state["applied_rulings"] = applied
    _save_run_state(drv.paths.run_root, state)


# --------------------------------------------------------------------------- #
# S4..S7 - the dispatch chain, runner v2 in-process
# --------------------------------------------------------------------------- #

def _problem_ids(drv: _Driver, occurrence: Path) -> list[str]:
    runner = runner_v2()
    material, _plan = runner.verify(drv.modules.root(), occurrence)
    return [str(problem["id"]) for problem in material.get("problems", ())]


#: A cycle's waves are bounded so a driver cannot spin: runner v2 prepares at
#: most ``wave_capacity`` coordinates per wave and every occurrence here is a
#: finite template, so a cycle that has not drained in this many waves is a
#: fault, not a long queue.
MAX_WAVES_PER_CYCLE = 64


def _waves_on_disk(drv: _Driver) -> int:
    total = 0
    for occurrence in _occurrence_dirs(drv.modules.root(), drv.config.occurrences):
        total += len(list((occurrence / "waves").glob("wave*.json")))
    return total


def _pending_waves(drv: _Driver) -> list[str]:
    runner = runner_v2()
    pending = []
    for occurrence in _occurrence_dirs(drv.modules.root(), drv.config.occurrences):
        wave = runner.pending_wave(occurrence)
        if wave is not None:
            pending.append(f"{drv.rel(occurrence)}:{wave['wave_id']}")
    return pending


def _dispatch(drv: _Driver, cycle: int) -> None:
    """S4..S7, repeated until ``ready_coordinates`` is empty for this cycle.

    The wave label is read off the **tree** (the wave files runner v2 has
    written), not off a counter this function keeps, so a resumed cycle re-enters
    at the wave the occurrence is actually at and a step already taken is a step
    already keyed.
    """

    for _ in range(MAX_WAVES_PER_CYCLE):
        wave = f"wave{_waves_on_disk(drv) + 1:04d}"
        _prepare(drv, cycle, wave)
        if not _pending_waves(drv):
            return
        _publish_in(drv, cycle, wave)
        _send(drv, cycle, wave)
        _publish_ev(drv, cycle, wave)
    raise _fail("STEP_BODY_FAILED",
                f"cycle {cycle} did not drain in {MAX_WAVES_PER_CYCLE} waves")


def _prepare(drv: _Driver, cycle: int, wave: str) -> None:
    """S4 - runner v2 ``prepare_wave`` per occurrence, in-process."""

    def body(handle: steps_module.StepHandle) -> Mapping[str, Any]:
        runner = runner_v2()
        prepared: list[dict[str, Any]] = []
        for occurrence in _occurrence_dirs(drv.modules.root(),
                                           drv.config.occurrences):
            if runner.pending_wave(occurrence) is not None:
                continue
            for problem in _problem_ids(drv, occurrence):
                try:
                    built = runner.prepare_wave(drv.modules.root(), occurrence,
                                                problem, cycle)
                except ValueError as exc:
                    # An occurrence's frozen scope names the problems and cycles
                    # it authorises; the loop's cycle index is not the
                    # occurrence's, and a cycle outside that scope is a
                    # declaration, not a failure.  It is recorded and nothing is
                    # dispatched for it.
                    if str(exc) != "SCOPE_EXCLUDED":
                        raise
                    prepared.append({"occurrence": drv.rel(occurrence),
                                     "problem": problem,
                                     "wave_id": None, "coordinates": 0,
                                     "scope": "SCOPE_EXCLUDED"})
                    continue
                prepared.append({"occurrence": drv.rel(occurrence),
                                 "problem": problem,
                                 "wave_id": built.get("wave_id"),
                                 "coordinates": len(built.get("coordinates") or ())})
        handle.record_output("prepared", prepared)
        return {}

    drv._run_step("PREPARE", cycle, {"cycle": cycle, "wave": wave}, body,
                  wave=wave)


def _publish_in(drv: _Driver, cycle: int, wave: str) -> None:
    """S5 - commit + push + verify the prepared wave inputs, before any socket.

    What is published is the occurrence tree runner v2 just wrote its requests
    and traces into, because that is what ``check_published`` byte-compares
    before it will send.  An untracked path is ``publish()``'s own refusal and
    nothing here works around it.
    """

    paths = [drv.rel(occurrence) for occurrence
             in _occurrence_dirs(drv.modules.root(), drv.config.occurrences)]
    paths.append(drv.rel(drv.paths.run_root / "plan.json"))
    drv._publish("PUBLISH_IN", paths,
                 f"cycle {cycle} {wave} inputs published",
                 cycle=cycle, wave=wave, inputs={"cycle": cycle, "wave": wave})


def _send(drv: _Driver, cycle: int, wave: str) -> None:
    """S6 - runner v2 ``send_round`` in-process, over one published HEAD.

    A provider failure ends one arm: runner v2's own ``arm_stopped`` is what
    says so, ``ready_coordinates`` then returns an empty queue for that arm, and
    the driver records ``arm_ended{arm, cycle, node, failure_code}``, mints no
    warrant, and leaves the other arms running (design 4.4).
    """

    def body(handle: steps_module.StepHandle) -> Mapping[str, Any]:
        root = drv.modules.root()
        if not publish_module.check_published(
                root, drv.rel(drv.paths.run_root / "plan.json"),
                ref=drv.config.publish_ref or None):
            raise _fail("INPUT_NOT_PUBLISHED",
                        "the plan's bytes are not on its ref; SEND is refused")
        runner = runner_v2()
        occurrences = _occurrence_dirs(root, drv.config.occurrences)
        rows = runner.send_round(root, occurrences,
                                 provider_factory=drv.modules.provider_factory,
                                 notify=lambda *_a, **_k: None,
                                 publish_ref=drv.config.publish_ref or None)
        handle.record_output("dispatched", rows)
        ended = _record_ended_arms(drv, cycle, occurrences, runner)
        if ended:
            handle.record_output("arm_ended", ended)
        handle.record_output("arm_ended_text", ARM_ENDED_TEXT)
        return {}

    drv._run_step("SEND", cycle, {"cycle": cycle, "wave": wave}, body, wave=wave)


def _record_ended_arms(drv: _Driver, cycle: int, occurrences: Sequence[Path],
                       runner: Any) -> list[dict[str, Any]]:
    """Read runner v2's ``arm_stopped`` and file what it says, verbatim."""

    state = _load_run_state(drv.paths.run_root)
    known = {(row.get("occurrence"), row.get("arm"))
             for row in state.get("arms_ended", [])}
    ended: list[dict[str, Any]] = []
    for occurrence in occurrences:
        try:
            material, plan = runner.verify(drv.modules.root(), occurrence)
        except Exception:
            continue
        arms = plan["arms"]
        for problem in material.get("problems", ()):
            for arm in sorted(arms):
                try:
                    stopped = runner.arm_stopped(occurrence, material, problem,
                                                 arm, cycle, arms)
                except Exception:
                    continue
                if not stopped or (drv.rel(occurrence), arm) in known:
                    continue
                node, code = _ended_arm_detail(runner, occurrence, material,
                                               problem, arm, cycle, arms)
                record = {"occurrence": drv.rel(occurrence), "arm": str(arm),
                          "cycle": cycle, "node": node, "failure_code": code,
                          "text": ARM_ENDED_TEXT}
                ended.append(record)
                known.add((record["occurrence"], record["arm"]))
    if ended:
        drv.ended_arms.extend(ended)
        state["arms_ended"] = list(drv.ended_arms)
        _save_run_state(drv.paths.run_root, state)
    return ended


def _ended_arm_detail(runner: Any, occurrence: Path, material: Mapping[str, Any],
                      problem: Mapping[str, Any], arm: str, cycle: int,
                      arms: Mapping[str, Any]) -> tuple[str, str]:
    """The node an arm ended at and the provider's own stable code."""

    for index in range(1, cycle + 1):
        for node in runner.nodes_for(material, problem, arm, index, arms):
            coordinate = runner.coordinate(problem["id"], arm, index, node["id"])
            path = runner.at(occurrence, "responses", coordinate)
            if not path.exists():
                continue
            receipt = runner.load(path)
            if receipt.get("status") == "FAILED":
                return str(node["id"]), str(receipt.get("failure_code") or
                                            receipt.get("failure_type") or "")
    return "", ""


def _publish_ev(drv: _Driver, cycle: int, wave: str) -> None:
    """S7 - commit + push + verify this wave's records."""

    paths = [drv.rel(occurrence) for occurrence
             in _occurrence_dirs(drv.modules.root(), drv.config.occurrences)]
    drv._publish("PUBLISH_EV", paths,
                 f"cycle {cycle} {wave} records published",
                 cycle=cycle, wave=wave, inputs={"cycle": cycle, "wave": wave})


# --------------------------------------------------------------------------- #
# S8 IMPORT / S9 USE_TABLE
# --------------------------------------------------------------------------- #

def _import(drv: _Driver, cycle: int) -> None:
    """S8 - ``graph_import_h005`` per occurrence, then custody verified."""

    def body(handle: steps_module.StepHandle) -> Mapping[str, Any]:
        from minireason import graph_import_h005

        out_root = drv.paths.cycle(cycle).import_dir
        reports: list[dict[str, Any]] = []
        for occurrence in _occurrence_dirs(drv.modules.root(),
                                           drv.config.occurrences):
            target = out_root / occurrence.name
            if not target.exists():
                graph_import_h005.import_occurrence(occurrence, target)
            # IMPORT is replayable, so what the receipt digests must be a fact
            # about the graph on disk and not about which branch this pass took:
            # the importer's own report, read back from where it wrote it.
            reports.append({"occurrence": drv.rel(occurrence),
                            "graph": drv.rel(target),
                            "report": custody.sha256_path(target / "report.json")})
        handle.record_output("imported", reports)
        findings = custody.verify_pins({"pins": drv._tree_pins(drv.plan)},
                                       drv.modules.root())
        handle.record_custody(findings)
        if findings:
            raise custody.CustodyMismatch(
                "SOURCE_PIN_MISMATCH" if any(
                    f.code == "SOURCE_PIN_MISMATCH" for f in findings)
                else "CUSTODY_MISMATCH",
                f"{len(findings)} custody finding(s) at IMPORT of cycle {cycle}")
        return {}

    drv._run_step("IMPORT", cycle, {"cycle": cycle}, body)


def _use_table(drv: _Driver, cycle: int) -> list[Mapping[str, Any]]:
    """S9 - ``use_relation_h005`` build; every root cell starts empty."""

    def body(handle: steps_module.StepHandle) -> Mapping[str, Any]:
        from minireason import use_relation_h005

        out_root = drv.paths.cycle(cycle).use_table
        rows: list[Mapping[str, Any]] = []
        written: list[str] = []
        for occurrence in _occurrence_dirs(drv.modules.root(),
                                           drv.config.occurrences):
            target = out_root / occurrence.name
            document = target / "use_table.json"
            if not document.is_file():
                table = use_relation_h005.build_use_table(occurrence)
                use_relation_h005.write_use_table(table, target)
            body_json = _read_json(document)
            rows.extend(body_json.get("rows") or ())
            written.append(drv.rel(document))
        drv.tables[cycle] = rows
        handle.record_output("use_table", {"rows": len(rows), "files": written})
        return {"rows": len(rows)}

    drv._run_step("USE_TABLE", cycle, {"cycle": cycle}, body)
    if cycle not in drv.tables:
        rows = []
        out_root = drv.paths.cycle(cycle).use_table
        for document in sorted(out_root.glob("*/use_table.json")):
            rows.extend((_read_json(document).get("rows") or ()))
        drv.tables[cycle] = rows
    return drv.tables[cycle]


# --------------------------------------------------------------------------- #
# S10 READ / S11 MARK
# --------------------------------------------------------------------------- #

def _reading_rows(drv: _Driver, table: Sequence[Mapping[str, Any]]
                  ) -> tuple[list[dict[str, Any]], list[str]]:
    """The reader's table, and the declared keys this cycle's table cannot name."""

    index = _table_index(table)
    rows: list[dict[str, Any]] = []
    unresolved: list[str] = []
    for key in drv.config.reading_set:
        identity = row_identity(key)
        if identity is None:
            continue
        found = index.get(identity)
        if found is None:
            unresolved.append(str(key))
            continue
        rows.append({"row_key": str(key),
                     "surface": surface_module.build_surface(found),
                     "cell": cell_key_for(key)})
    return rows, unresolved


def _reopen_reason_in_force(drv: _Driver) -> str:
    """The pre-registered reopen reason an operator recorded, or ``""``.

    ``reopen()`` writes it; nothing else does, and a reason outside
    ``config.reopen_reasons`` never got that far.  Without one, a spent row is
    not re-read - which is G11's rule and W2-ROLES' ``NO_REPLAY`` together.
    """

    state = _load_run_state(drv.paths.run_root)
    rows = list(state.get("reopened", []))
    return str(rows[-1].get("reason", "")) if rows else ""


def _read(drv: _Driver, cycle: int, table: Sequence[Mapping[str, Any]]) -> Any:
    """S10 - the guarded trials over the pre-registered reading set.

    Resume is coordinate-grain and W4-READER owns it: a coordinate with a
    request or an attempt and no response is ``INDETERMINATE``, never re-sent
    and never an absence (4.3).  **W5-DRIVER is the record that names one**
    (WAVE3 §8 item 2): ``steps.scan_coordinates`` reads runner v2's dispatch
    tree and ``reader.unanswered_coordinates`` reads W2-ROLES' claim layout, so
    the two are read separately and both are filed.
    """

    def body(handle: steps_module.StepHandle) -> Mapping[str, Any]:
        records = drv.paths.readings
        records.mkdir(parents=True, exist_ok=True)
        rows, unresolved = _reading_rows(drv, table)
        if unresolved:
            raise _fail("READING_ROW_UNRESOLVED",
                        f"{len(unresolved)} declared row(s) name no use-table "
                        f"row: {', '.join(unresolved[:3])}")
        reason = _reopen_reason_in_force(drv)
        # The reading tree is the RUN's, not the cycle's (design 4.2), so a row
        # a previous cycle spent is a spent coordinate: W2-ROLES refuses to
        # re-enter it (NO_REPLAY) and G11 refuses a re-read with no listed
        # reopen reason.  A later cycle therefore reads what is left, and a
        # re-read happens only when a reason this plan declared is in force.
        already = [row for row in rows
                   if custody.fenced(records, row["row_key"]).exists()]
        if not reason:
            rows = [row for row in rows if row not in already]
        handle.record_output("already_read",
                             sorted(row["row_key"] for row in already))
        handle.record_output("reopen_reason", reason or "")
        dispatch_scan = steps_module.scan_coordinates(records)
        claimed = reader_module.unanswered_coordinates(records)
        readings = reader_module.read_table(
            drv.harness, rows, standard_module.STANDARD_BODY, drv.seats(),
            drv.config, records, reopen_reason=reason or None,
            provider_factory=drv.modules.provider_factory)
        drv.readings_by_cycle[cycle] = readings
        handle.record_output("readings", {
            "planned": readings.planned,
            "dispatched": readings.dispatched,
            "registered": [row.row_key for row in readings.registered],
            "blocks": [[row.row_key, row.code] for row in readings.blocks],
            "dispositions": [[row.row_key, row.reason]
                             for row in readings.dispositions],
            "unread": sorted(readings.unread),
        })
        handle.record_output("indeterminate", {
            "roles_layout": sorted(set(claimed)
                                   | {row.coordinate
                                      for row in readings.indeterminate}),
            "dispatch_tree": sorted(dispatch_scan.indeterminate),
        })
        # The streak's definition resets on a trial of that role whose outcome
        # is not a block, so the counter is handed this pass's outcomes in
        # DISPATCH order - the order the rows were sent in - and not the block
        # register alone, which can only ever count upward.
        blocked = {record.row_key for record in readings.blocks}
        outcomes = [(row["row_key"],
                     trial_module.OUTCOME_BLOCKED if row["row_key"] in blocked
                     else trial_module.OUTCOME_SUSTAINED)
                    for row in rows]
        streak = block_streak(readings.blocks, outcomes)
        drv.block_streaks[cycle] = streak
        handle.record_output("block_streak", streak)
        return {"planned": readings.planned, "dispatched": readings.dispatched}

    drv._run_step("READ", cycle, {"cycle": cycle}, body)
    return drv.readings_by_cycle.get(cycle)


def _mark(drv: _Driver, cycle: int) -> None:
    """S11 - the sealed baseline first, the program's pre-empt, then the marks."""

    def body(handle: steps_module.StepHandle) -> Mapping[str, Any]:
        cells = _mark_cells(drv)
        if not cells:
            handle.record_output("marks", {"cells": 0,
                                           "contrast_attached": False})
            return {}
        records = drv.paths.cycle(cycle).contrast
        records.mkdir(parents=True, exist_ok=True)
        seals = seal_baselines(drv, cells)
        marked: list[dict[str, Any]] = []
        for cell in cells:
            out_dir = records / _slugify(cell.cell_id)
            out_dir.mkdir(parents=True, exist_ok=True)
            seal = seals[cell.cell_id]
            marks = marker_module.mark_cell(
                drv.harness, cell, seal, standard_module.STANDARD_BODY,
                drv.seats(), drv.config, records_dir=out_dir / "marks",
                provider_factory=drv.modules.provider_factory,
                out_dir=out_dir)
            drv.marks_by_cycle.setdefault(cycle, []).append(marks)
            marked.append({
                "cell": marks.cell,
                "baseline_sha256": marks.baseline_sha256,
                "rows": [[comparison, register, row.mark, row.block or ""]
                         for comparison, register_marks
                         in sorted(marks.comparisons.items())
                         for register, row in sorted(register_marks.rows.items())],
            })
        handle.record_output("marks", {"cells": len(cells), "marked": marked})
        return {"cells": len(cells)}

    drv._run_step("MARK", cycle, {"cycle": cycle}, body)


def _slugify(value: str) -> str:
    return _UNSAFE_SEGMENT.sub("-", str(value).replace("/", "__")) or "cell"


# --------------------------------------------------------------------------- #
# S12 ADJUDICATE
# --------------------------------------------------------------------------- #

def adjudicate(run_ref: str | Path | None = None, *,
               modules: Modules | None = None,
               _driver: _Driver | None = None,
               _cycle: int | None = None) -> Any:
    """S12 - audits when due, the rendered files registered, the labels read.

    Replayable: a replay must reproduce the recorded digests or W1-STEPS raises
    ``STEP_NONDETERMINISTIC``.
    """

    drv = _driver if _driver is not None else _load_driver_from_run(run_ref, modules)
    if drv.ledger is None:
        drv.ledger = drv._open_ledger()
    if drv.harness is None:
        drv.harness = drv._open_harness()
    cycle = _cycle if _cycle is not None else max(
        [row.receipt.cycle or 0 for row in drv.ledger.records()] or [1])

    if _audit_due(drv, cycle):
        _audit(drv, cycle)

    def body(handle: steps_module.StepHandle) -> Mapping[str, Any]:
        rendered = _render_tables(drv, cycle)
        record = report_module.rendered_files_record(rendered)
        contracts_module.assert_no_scoring_keys(record)
        rendered_id = graph_module.register_material(
            drv.harness, custody.encoded(record))
        handle.record_output("rendered_files",
                             {"files": sorted(rendered), "id": rendered_id})
        production = graph_module.produced(drv.harness, since_seq=drv.since_seq)
        situation = decide_module.situation(drv.harness, cycle, drv.obligations,
                                            registered=production)
        drv.situations[cycle] = situation
        drv.since_seq = int(getattr(production, "upto_seq", drv.since_seq))
        state = _load_run_state(drv.paths.run_root)
        state["since_seq"] = drv.since_seq
        _save_run_state(drv.paths.run_root, state)
        handle.record_output("standings", _standings_output(drv))
        handle.record_output("obligations_pin", drv.obligations.pin)
        return {"cycle": cycle}

    step_inputs: dict[str, Any] = {"cycle": cycle}
    if drv.rulings_applied_this_run:
        step_inputs["rulings"] = sorted(drv.rulings_applied_this_run)
    drv._run_step("ADJUDICATE", cycle, step_inputs, body)
    if cycle in drv.situations:
        return drv.situations[cycle]
    situation = decide_module.situation(drv.harness, cycle, drv.obligations)
    drv.situations[cycle] = situation
    return situation


def _audit(drv: _Driver, cycle: int) -> None:
    """The §2.5 audits, as their own spending step (design 4.3's step classes).

    ``AUDIT`` is a spending kind: it calls the judge seats, so it writes its own
    ``.open`` marker and resolves it with its own receipt.  Running it inside
    the replayable ADJUDICATE would put a spent coordinate inside a step a
    resume re-enters, and W2-ROLES would refuse the second entry ``NO_REPLAY``.
    """

    def body(handle: steps_module.StepHandle) -> Mapping[str, Any]:
        handle.record_output("audit", _run_audits(drv, cycle))
        return {}

    drv._run_step("AUDIT", cycle, {"cycle": cycle}, body)


def _standings_output(drv: _Driver) -> list[list[str]]:
    return [[standing.key.token if hasattr(standing.key, "token")
             else str(standing.key), str(standing.state)]
            for standing in graph_module.cell_standings(drv.harness)]


def _audit_due(drv: _Driver, cycle: int) -> bool:
    period = int(getattr(drv.config.audit, "period", 0) or 0)
    return bool(period) and cycle % period == 0


def _run_audits(drv: _Driver, cycle: int) -> Mapping[str, Any]:
    """The §2.5 audits, with the panel named explicitly (WAVE4 §8 item 4)."""

    readings = drv.readings_by_cycle.get(cycle)
    ids = [row.ids.reading for row in getattr(readings, "registered", ())
           if getattr(getattr(row, "ids", None), "reading", None)]

    def judge_caller(seat_label: str, pack: Any, coordinate: str) -> Any:
        seat = _judge_seat(drv, seat_label)
        if seat is None:
            return None
        result = roles_module.call_judge(
            seat, pack, drv.paths.audits / f"cycle-{cycle:02d}" / "calls",
            coordinate=coordinate, seat_index=_seat_index(drv, seat_label),
            provider_factory=drv.modules.provider_factory,
            max_per_key=drv.config.max_per_key)
        # ``None`` is a delivery fact about the route, never a reading: a
        # blocked call answers nothing and the audit layer records it as such.
        return result.output if result.ok else None

    report_body = audits_module.run_audits(
        drv.harness, judge_caller, ids, drv.config, panel=list(drv.judge_labels()))
    body = {
        "schema": report_body.schema,
        "cycle": cycle,
        # CLONE-PATCH item 1: what o5's clause reads back.
        "calibration_sha256": str(drv.plan.get("calibration_sha256", "")),
        "covers": [cycle],
        "seats": list(drv.config.seats.judges),
        "panel": list(drv.judge_labels()),
        "findings": [finding.as_dict() if hasattr(finding, "as_dict")
                     else str(finding) for finding in report_body.findings],
        "collapsed": [list(pair) for pair in report_body.collapsed],
    }
    contracts_module.assert_no_scoring_keys(body)
    graph_module.register_material(drv.harness, custody.encoded(body))
    drv.audit_findings.extend(
        finding.as_dict() if hasattr(finding, "as_dict") else {"detail": str(finding)}
        for finding in report_body.findings)
    _write_json(drv.paths.audits / f"cycle-{cycle:02d}" / "audit.json", body)
    return {"findings": len(body["findings"]),
            "calibration_sha256": body["calibration_sha256"],
            "covers": body["covers"], "seats": body["seats"]}


def _seat_index(drv: _Driver, seat_label: str) -> int:
    for index, label in enumerate(drv.judge_labels()):
        if label == seat_label:
            return index
    return 0


def _judge_seat(drv: _Driver, seat_label: str) -> Any:
    plan = drv.seats()
    judges = list(getattr(plan, "judges", ()) or ())
    for index, seat in enumerate(judges):
        label = roles_module.Coordinate(role="judge", key="panel",
                                        seat_index=index).seat_label
        if label == seat_label or getattr(seat, "name", "") == seat_label:
            return seat
    return None


def _report_plan(drv: _Driver) -> Any:
    return report_module.ReportPlan(
        loop_plan_id=drv.plan_id,
        pins=dict(drv.plan.get("pins", {})),
        reading_set=tuple(str(key) for key in drv.config.reading_set),
        ceiling_text=standard_module.CEILING_TEXT)


def _mark_blocks(marks: Any) -> list[tuple[str, str]]:
    """One ``(cell, reason)`` pair per blocked register row of a marked cell.

    ``baseline-forced-same`` is a heading of W3-REPORT's block register and
    **only a mark row can fill it**: a register fed by the reading arm alone
    leaves one of the ceiling's own rows unfillable by construction.  The pair
    names the marker's own coordinate, so the register row points at the record
    the block was written on.
    """

    rows: list[tuple[str, str]] = []
    for comparison, register_marks in sorted(marks.comparisons.items()):
        for register, row in sorted(register_marks.rows.items()):
            if not row.block:
                continue
            rows.append((mark_cell_key(marks.cell, register, comparison),
                         str(row.block).split(":", 1)[-1]))
    return rows


def mark_cell_key(cell: str, register: str, comparison: str) -> str:
    """One spelling for a register cell, and it is W1-GRAPH's own.

    ``cell_standings`` prints ``<cell>|<register>|<comparison>``; a block
    register that spelled the same cell the marker's coordinate way would put
    two names for one thing in one record.
    """

    return f"{cell}|{register}|{comparison}"


def _cycle_state(drv: _Driver, cycle: int) -> Any:
    readings = drv.readings_by_cycle.get(cycle)
    blocks = [(row.cell, row.code.split(":", 1)[-1])
              for row in getattr(readings, "blocks", ())]
    for marks in drv.marks_by_cycle.get(cycle, ()):
        blocks.extend(_mark_blocks(marks))
    indeterminate = tuple(sorted(
        {row.coordinate for row in getattr(readings, "indeterminate", ())}))
    unread = tuple(sorted(getattr(readings, "unread", ()) or ()))
    return report_module.CycleState(
        standings=tuple(graph_module.cell_standings(drv.harness)),
        blocks=tuple(blocks), indeterminate=indeterminate, unread=unread)


def _run_blocks(drv: _Driver) -> tuple[tuple[str, str], ...]:
    """The **run's** whole block register, read off the run's own records.

    ``ClosingRun`` says its register is the run's and not one cycle's, and a
    run is resumable: the cycle that read is often not the invocation that
    closes, so a register assembled from the objects this process happens to
    hold would forget every block an earlier invocation wrote.  W4-READER's
    ``block-NN.json`` records and W4-MARKER's ``marks.json`` are write-once and
    are the run's own, so they are what is read here.
    """

    rows: list[tuple[str, str]] = []
    readings = drv.paths.readings
    if readings.is_dir():
        for path in sorted(readings.rglob("block-*.json")):
            record = _read_json(path)
            if not isinstance(record, Mapping):
                continue
            reason = str(record.get("reason", ""))
            if reason:
                rows.append((str(record.get("cell", "")),
                             reason.split(":", 1)[-1]))
    cycles = drv.paths.run_root / "cycles"
    if cycles.is_dir():
        for path in sorted(cycles.glob("*/contrast/*/marks.json")):
            record = _read_json(path)
            if not isinstance(record, Mapping):
                continue
            cell = str(record.get("cell", ""))
            for comparison, body in sorted(
                    dict(record.get("comparisons", {})).items()):
                for register, row in sorted(
                        dict(body.get("registers", {})).items()):
                    block = str(row.get("block") or "")
                    if block:
                        rows.append((mark_cell_key(cell, register, comparison),
                                     block.split(":", 1)[-1]))
    # One cell declined for one reason is one entry, however many cycles met it
    # again: the register counts the cells a reason declined, never the number
    # of occasions on which the run re-met one.
    return tuple(sorted(set(rows)))


def _render_tables(drv: _Driver, cycle: int) -> dict[str, str]:
    """READING_TABLE.md and COMPARISON.md, through W3-REPORT and nothing else."""

    plan = _report_plan(drv)
    state = _cycle_state(drv, cycle)
    table = report_module.render_reading_table(drv.harness, plan, state=state)
    comparison = report_module.render_comparison(drv.harness, plan, state=state)
    drv.paths.reading_table.write_text(table, encoding="utf-8")
    drv.paths.comparison.write_text(comparison, encoding="utf-8")
    drv.rendered = {drv.rel(drv.paths.reading_table): table,
                    drv.rel(drv.paths.comparison): comparison}
    return dict(drv.rendered)


# --------------------------------------------------------------------------- #
# S13 DECIDE
# --------------------------------------------------------------------------- #

def _instrument(drv: _Driver) -> Any:
    """The facts ``decide()`` reads that no artifact carries.

    ``custody_halted`` / ``halted_step`` come off the ledger's blocking resume
    action; ``arms_ended`` off runner v2's own ``arm_stopped`` as SEND filed it;
    ``calls_reached`` off the spending receipts against ``max_calls``;
    ``block_streak`` off :func:`block_streak` over the reader's block records.
    """

    blocking = drv.ledger.blocking() if drv.ledger is not None else None
    halted = (blocking is not None
              and blocking.code not in (None, "PUBLISH_PENDING", "UNRESOLVED_STEP"))
    spenders = 0
    if drv.ledger is not None:
        spenders = sum(1 for row in drv.ledger.records()
                       if row.receipt.spending and row.receipt.status == "COMPLETE")
    state = _load_run_state(drv.paths.run_root)
    arms = list(state.get("arms_ended", []))
    declared: set[tuple[str, str]] = set()
    try:
        runner = runner_v2()
        for occurrence in _occurrence_dirs(drv.modules.root(),
                                           drv.config.occurrences):
            _material, plan = runner.verify(drv.modules.root(), occurrence)
            for arm in plan["arms"]:
                declared.add((drv.rel(occurrence), str(arm)))
    except Exception:
        declared = set()
    ended = {(str(row.get("occurrence", "")), str(row.get("arm", "")))
             for row in arms}
    streak = max(drv.block_streaks.values(), default=0)
    return decide_module.Instrument(
        custody_halted=halted,
        # ``all_arms_ended`` is true only when every declared arm is over: one
        # delivery failure names an arm and never stops the other arms (4.4).
        arms_ended=bool(declared) and declared <= ended,
        block_streak=streak or None,
        calls_reached=bool(drv.config.max_calls) and spenders >= drv.config.max_calls,
        halted_step=(f"{blocking.index:04d}-{blocking.kind}"
                     if halted and blocking is not None else ""),
        ended_arms=tuple(sorted({str(row.get("arm", "")) for row in arms})),
        would_reopen="", detail="", preregistered_condition="")


def _decide(drv: _Driver, cycle: int, prev_situation: Any, situation: Any,
            prev_triples: Any) -> Any:
    """S13 - the pre-registered stop/continue program; ``decision.json``."""

    def body(handle: steps_module.StepHandle) -> Mapping[str, Any]:
        decision = decide_module.decide(
            prev_situation, situation, cycle, drv.config, drv.obligations,
            instrument=_instrument(drv), prev_triples=prev_triples,
            curr_triples=decide_module.mark_triples(drv.harness))
        text = decide_module.render_decision(decision)
        standard_module.assert_no_exhaustion_claim(text, "decision.json")
        path = drv.paths.cycle(cycle).decision
        record = {"schema": "minireason.loop.decision.v1", "cycle": cycle,
                  "stop": bool(decision.stop), "reason": decision.reason,
                  "clause": decision.clause,
                  "would_reopen": decision.would_reopen, "text": text}
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.is_file():
            # DECIDE is replayable and the file is write-once: a replay must
            # not rewrite it, and decide() is pure over its arguments, so the
            # recorded digest is what the replay reproduces.
            path.write_bytes(custody.encoded(record))
        drv.decisions[cycle] = decision
        handle.record_output("decision", record)
        return {"decision_file": drv.rel(path)}

    step_inputs: dict[str, Any] = {"cycle": cycle}
    if drv.rulings_applied_this_run:
        step_inputs["rulings"] = sorted(drv.rulings_applied_this_run)
    drv._run_step("DECIDE", cycle, step_inputs, body)
    if cycle not in drv.decisions:
        # A skipped replayable step on resume: read the decision back off the
        # write-once record rather than re-deriving a second one.
        drv.decisions[cycle] = decide_module.decide(
            prev_situation, situation, cycle, drv.config, drv.obligations,
            instrument=_instrument(drv), prev_triples=prev_triples,
            curr_triples=decide_module.mark_triples(drv.harness))
    return drv.decisions[cycle]


# --------------------------------------------------------------------------- #
# S14 PUBLISH_CY / S15 CLOSE
# --------------------------------------------------------------------------- #

def _publish_cycle(drv: _Driver, cycle: int, decision: Any) -> None:
    """S14 - CYCLE.md through W3-REPORT, then commit + push + verify."""

    text = report_module.render_cycle(decision, _cycle_state(drv, cycle))
    standard_module.assert_no_exhaustion_claim(text, f"cycle-{cycle:02d}/CYCLE.md")
    cycle_md = drv.paths.cycle(cycle).cycle_md
    cycle_md.parent.mkdir(parents=True, exist_ok=True)
    cycle_md.write_text(text, encoding="utf-8")
    paths = [drv.rel(drv.paths.cycles), drv.rel(drv.paths.reading_table),
             drv.rel(drv.paths.comparison)]
    if drv.paths.readings.is_dir():
        paths.append(drv.rel(drv.paths.readings))
    if drv.paths.audits.is_dir():
        paths.append(drv.rel(drv.paths.audits))
    drv._publish("PUBLISH_CY", paths, f"cycle {cycle} published",
                 cycle=cycle, inputs={"cycle": cycle})


def recorded_failures(drv: "_Driver") -> list[str]:
    """Every failure and refusal on this run's own record, one line each.

    Three registers, all of them the run's and none of them this process's:
    the step ledger's receipts (a ``FAILED`` or ``HALTED`` step carries the
    code it failed with, and survives every later invocation), the run state's
    refusals (an entry that refused before any step began records its code
    there), and the run state's applied rulings (an outcome, not a failure -
    ``APPELLATE_RULING_APPLIED`` is in ``types.OUTCOME_CODES``, and the closing
    record must name it as the design's list asks).  No line here carries a
    number of any kind: the one register that prints counts is W3-REPORT's
    block register, because the frozen ceiling requires it there, and this
    section names codes and the receipts that carry them and nothing else.
    """

    ledger = drv.ledger if drv.ledger is not None else drv._open_ledger()
    lines: list[str] = []
    for row in ledger.records():
        code = row.receipt.failure_code
        if not code:
            continue
        cycle = "-" if row.receipt.cycle is None else row.receipt.cycle
        lines.append(f"- `{code}`: step {row.index:04d} {row.receipt.kind} "
                     f"(cycle {cycle}) recorded {row.receipt.status}")
    state = _load_run_state(drv.paths.run_root)
    for refusal in state.get("refusals", []):
        if not isinstance(refusal, Mapping):
            continue
        lines.append(f"- `{refusal.get('code')}`: the {refusal.get('entry')} "
                     f"entry refused {refusal.get('detail')}")
    for applied in state.get("applied_rulings", []):
        if not isinstance(applied, Mapping):
            continue
        outcome = str(applied.get("outcome", "")).split(":", 1)[0]
        if not outcome:
            continue
        lines.append(f"- `{outcome}`: the staged ruling {applied.get('staged')} "
                     f"against {applied.get('target')}")
    return lines


def close(run_ref: str | Path | None = None, *,
          modules: Modules | None = None,
          _driver: _Driver | None = None,
          _decision: Any = None) -> Mapping[str, Any]:
    """S15 - the closing record, through W3-REPORT, with the ceiling verbatim."""

    drv = _driver if _driver is not None else _load_driver_from_run(run_ref, modules)
    if drv.ledger is None:
        drv.ledger = drv._open_ledger()
    if drv.harness is None:
        drv.harness = drv._open_harness()
    decision = _decision if _decision is not None else _last_decision(drv)
    state = _load_run_state(drv.paths.run_root)

    def body(handle: steps_module.StepHandle) -> Mapping[str, Any]:
        cycle = max(drv.readings_by_cycle or drv.decisions or {1: None})
        cycle_state = _cycle_state(drv, cycle)
        closing = report_module.ClosingRun(
            plan=_report_plan(drv), decision=decision,
            blocks=_run_blocks(drv), standings=cycle_state.standings,
            indeterminate=cycle_state.indeterminate, unread=cycle_state.unread,
            audit_findings=tuple(drv.audit_findings),
            appellate_rulings=graph_module.appellate_rulings(drv.harness),
            state=cycle_state)
        text = report_module.render_closing(closing)
        arms = list(state.get("arms_ended", []))
        if arms:
            text = (text.rstrip("\n") + "\n\n## " + ARMS_ENDED_HEADING + "\n\n")
            for arm in arms:
                text += (f"- {arm.get('occurrence')} / {arm.get('arm')} at node "
                         f"{arm.get('node') or '-'} in cycle {arm.get('cycle')}: "
                         f"{arm.get('failure_code') or '-'} - {ARM_ENDED_TEXT}.\n")
        named = recorded_failures(drv)
        text = text.rstrip("\n") + "\n\n## " + RECORDED_FAILURES_HEADING + "\n\n"
        text += RECORDED_FAILURES_SENTENCE + "\n\n"
        text += "\n".join(named or [NOTHING_REFUSED]) + "\n"
        standard_module.assert_no_exhaustion_claim(text, "CLOSING.md")
        drv.paths.closing.parent.mkdir(parents=True, exist_ok=True)
        drv.paths.closing.write_text(text, encoding="utf-8")
        handle.record_output("closing", custody.sha256_bytes(text.encode("utf-8")))
        handle.record_output("stop_reason", decision.reason)
        handle.record_output("arms_ended", arms)
        handle.record_output("closing_names", named)
        state["closing_names"] = named
        _save_run_state(drv.paths.run_root, state)
        return {}

    drv._run_step("CLOSE", None, {"loop_plan_id": drv.plan_id}, body)
    drv._publish("PUBLISH_CY", [drv.rel(drv.paths.closing)],
                 "closing record published", inputs={"closing": drv.plan_id})
    return {"loop_plan_id": drv.plan_id, "closing": str(drv.paths.closing),
            "stop_reason": decision.reason}


def _last_decision(drv: _Driver) -> Any:
    if drv.decisions:
        return drv.decisions[max(drv.decisions)]
    raise _fail("RUN_NOT_FOUND",
                "this run has no DECIDE step; a closing record is a decision's")


# --------------------------------------------------------------------------- #
# status / reopen / appeal
# --------------------------------------------------------------------------- #

def _load_driver_from_run(run_ref: str | Path | None,
                          modules: Modules | None) -> _Driver:
    if run_ref is None:
        raise _fail("RUN_NOT_FOUND", "a run root or config path is required")
    path = Path(run_ref)
    config_path = path / "config.json" if path.is_dir() else path
    config = LoopConfig.load(config_path)
    if modules is None and path.is_dir() and len(path.parents) >= 3:
        modules = Modules(repo_root=path.parents[2])
    drv = _Driver(config, modules, config_path)
    if not drv.paths.plan.is_file():
        raise _fail("RUN_NOT_FOUND", f"{drv.paths.plan} is absent")
    drv.plan = _read_json(drv.paths.plan)
    drv.plan_id = str(drv.plan.get("loop_plan_id", ""))
    try:
        drv.obligations = obligations_module.load_obligations(
            drv.modules.root() / drv.config.obligations_path)
    except Exception:
        drv.obligations = None
    drv.ledger = drv._open_ledger()
    drv.receipt_id = str(_load_run_state(drv.paths.run_root).get(
        "receipt_id", _NO_LEDGER_RECEIPT))
    return drv


def status(run_ref: str | Path | None = None, *,
           modules: Modules | None = None) -> Mapping[str, Any]:
    """A read-only digest of the run: the ledger's resume plan."""

    drv = _load_driver_from_run(run_ref, modules)
    if drv.ledger is None:
        raise _fail("RUN_NOT_FOUND", f"{run_ref} has no step ledger")
    blocking = drv.ledger.blocking()
    # The step key is printed beside every action, and again under
    # ``acknowledge``.  ``--acknowledge`` takes a step key and an operator has
    # none to hand otherwise: it is on the receipt, and reading a receipt to
    # type a flag the status entry could have printed is a human step the
    # design does not ask for (WAVE5-INTERFACE §9 item 10).
    return {
        "loop_plan_id": drv.plan_id,
        "run_root": str(drv.paths.run_root),
        "actions": [{"action": a.action, "index": a.index, "kind": a.kind,
                     "code": a.code, "step_key": a.step_key, "detail": a.detail}
                    for a in drv.ledger.resume_plan()],
        "blocking": None if blocking is None else blocking.code,
        "acknowledge": None if blocking is None else blocking.step_key,
    }


def reopen(run_ref: str | Path | None, ruling: Any = None, *,
           modules: Modules | None = None,
           reason: str | None = None) -> Mapping[str, Any]:
    """Re-enter a closed coordinate on a pre-registered reason (design §5)."""

    drv = _load_driver_from_run(run_ref, modules)
    ruling_reason = str(ruling.get("reopen_reason", "")) \
        if isinstance(ruling, Mapping) else ""
    declared = set(getattr(drv.config, "reopen_reasons", ()) or ())
    allowed = reason or ruling_reason
    if allowed not in declared:
        # The refusal is filed before it is raised: design 4.7 asks the closing
        # receipt to name a re-read refused for want of a reopen_reason, and a
        # refusal nothing records is a refusal no record can name.  It is an
        # act of the instrument, so it goes in the run state beside the halts
        # and never in the block register, which is the material's.
        state = _load_run_state(drv.paths.run_root)
        refusals = list(state.get("refusals", []))
        refusals.append({"entry": "reopen", "code": "REOPEN_REFUSED",
                         "detail": f"{allowed or '<none>'}, which this plan "
                                   f"does not declare"})
        state["refusals"] = refusals
        _save_run_state(drv.paths.run_root, state)
        raise _fail("REOPEN_REFUSED",
                    f"{allowed or '<none>'} is not a pre-registered reopen "
                    f"reason of this plan")
    state = _load_run_state(drv.paths.run_root)
    reopened = list(state.get("reopened", []))
    reopened.append({"reason": allowed, "via": "ruling" if ruling else "cli"})
    state["reopened"] = reopened
    _save_run_state(drv.paths.run_root, state)
    return {"reopened": True, "reason": allowed}


def appeal(run_ref: str | Path | None = None, path: str | Path | None = None, *,
           modules: Modules | None = None) -> Mapping[str, Any]:
    """Stage an appellate ruling; it is applied at the next ``run()``."""

    if path is None:
        raise _fail("APPEAL_PATH_INVALID", "a ruling path is required")
    drv = _load_driver_from_run(run_ref, modules)
    try:
        raw = _read_json(Path(path))
    except (OSError, ValueError) as exc:
        raise _fail("APPEAL_PATH_INVALID",
                    f"{path} is not a readable ruling: {type(exc).__name__}")
    if not isinstance(raw, Mapping):
        raise _fail("APPEAL_TARGET_INVALID", "an appellate ruling is a mapping")
    target = str(raw.get("target", ""))
    if not target:
        raise _fail("APPEAL_TARGET_INVALID", "the ruling names no target")
    drv.paths.appeals.mkdir(parents=True, exist_ok=True)
    staged = drv.paths.appeals / (
        f"ruling-{len(list(drv.paths.appeals.iterdir())):04d}.json")
    custody.write_new(custody.fenced(drv.paths.run_root, staged), dict(raw))
    return {"staged": staged.name, "target": target, "applies_at": "next-run"}


# --------------------------------------------------------------------------- #
# dry-run - the acceptance gate's entry (design 4.7)
# --------------------------------------------------------------------------- #

def dry_run(config: LoopConfig | str | Path | None = None,
            out: str | Path | None = None, *,
            modules: Modules | None = None,
            seed: int = synthetic_module.DEFAULT_SEED,
            induce: Iterable[str] = ()) -> Mapping[str, Any]:
    """Build the synthetic occurrence and, given a config, walk ``run()`` on it.

    The provider is ``synthetic.provider_factory``, which answers both W2-ROLES'
    shape and runner v2's, so one seam serves the reading arm and the dispatch
    arm; every guard, pack, record and custody check is the real one.  With no
    config this returns what it built and ``ran: False`` rather than minting a
    plan it was not asked to freeze.
    """

    out_dir = Path(out) if out is not None else Path("dry-run-output")
    out_dir.mkdir(parents=True, exist_ok=True)
    bound = modules if modules is not None else Modules()
    freeze = synthetic_module.runner_freeze(bound.root())
    occurrence = synthetic_module.build_occurrence(
        out_dir / "occurrence", seed=seed, induce=induce, freeze=freeze)
    verdict: dict[str, Any] = {
        "seed": seed,
        "out": str(out_dir),
        "occurrence": str(occurrence.root),
        "induced": list(occurrence.induced),
        "inducible": list(synthetic_module.INDUCIBLE),
        "induced_codes": dict(synthetic_module.INDUCED_CODES),
    }
    if config is None:
        verdict["ran"] = False
        return verdict
    cfg = config if isinstance(config, LoopConfig) else LoopConfig.load(config)
    if bound.provider_factory is None:
        bound = Modules(provider_factory=synthetic_module.provider_factory(
            seed=seed, induce=induce, aliases=_dry_run_aliases(cfg)),
            repo_root=bound.repo_root, sleep=bound.sleep)
    verdict["staged"] = _stage_dry_run_material(bound.root(), cfg, seed=seed)
    paths = run_paths(bound.root(), cfg.run_id)
    if not paths.plan.is_file():
        verdict["preregister"] = dict(preregister(cfg, modules=bound))
        verdict["preflight"] = dict(preflight(cfg, modules=bound))
    try:
        verdict["run"] = run(cfg, modules=bound)
    except LoopError as exc:
        # A dry run that refused is a dry run that reported: the verdict is
        # written with the refusal on it rather than lost with the exception.
        verdict["ran"] = False
        verdict["refused"] = {"code": exc.code, "detail": exc.detail}
        _write_json(out_dir / "dry-run.json", verdict)
        raise
    verdict["ran"] = True
    _write_json(out_dir / "dry-run.json", verdict)
    return verdict


def _dry_run_aliases(cfg: LoopConfig) -> dict[str, str]:
    """Which folded reading coordinate answers to which synthetic row script.

    A reading row is addressed by the coordinate ``cell_key_for`` folds the
    pre-registered key into, and ``synthetic`` scripts by its own short row
    names; this driver is the one thing that knows both spellings, so the map
    is minted here and handed to the factory.  A declared row that names no
    synthetic row contributes nothing and falls through to the script's own
    loose answer.
    """

    by_identity = {tuple(identity): name for name, identity
                   in synthetic_module.READING_COORDINATES.items()}
    aliases: dict[str, str] = {}
    for key in cfg.reading_set:
        identity = row_identity(key)
        short = by_identity.get(tuple(identity)) if identity else None
        if short:
            aliases[cell_key_for(key)] = short
    return aliases


def _stage_dry_run_material(root: Path, cfg: LoopConfig, *,
                            seed: int) -> dict[str, Any]:
    """Write the synthetic material every occurrence the config names needs.

    Design 4.7 gives ``loop/synthetic.py`` the occurrence and the contrast leg,
    and W5's own record (WAVE5-INTERFACE §9 item 2) found that an occurrence
    written **delivered** is one runner v2 cannot re-read: ``read_terminal``
    reads a ``provider_payload`` the canned records do not carry.  So the
    material and the arms are written and the plan is frozen through runner
    v2's own ``initialize``, with **nothing delivered** - S4..S7 then produce
    every delivery through the same runner, which is the walk a live run makes.
    An occurrence the tree already carries is left exactly as it stands.
    """

    staged: dict[str, Any] = {"occurrences": [], "contrast": []}
    runner = runner_v2()
    for occurrence in _occurrence_dirs(root, cfg.occurrences):
        if (occurrence / "plan.json").is_file():
            continue
        occurrence.mkdir(parents=True, exist_ok=True)
        material = occurrence / "material.json"
        arms = occurrence / "arms.json"
        material.write_bytes(custody.encoded(
            synthetic_module.material_document(seed)))
        arms.write_bytes(custody.encoded(synthetic_module.arms_document()))
        runner.initialize(root, occurrence, material, arms)
        staged["occurrences"].append(occurrence.relative_to(root).as_posix())
    for leg in _occurrence_dirs(root, cfg.contrast.occurrences):
        if (leg / "contrast.json").is_file():
            continue
        leg.mkdir(parents=True, exist_ok=True)
        (leg / "contrast.json").write_bytes(
            custody.encoded(synthetic_module.contrast_leg(seed)))
        staged["contrast"].append(leg.relative_to(root).as_posix())
    return staged


# --------------------------------------------------------------------------- #
# CLI (design 4.2)
# --------------------------------------------------------------------------- #

def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="auto_loop",
        description="W5-DRIVER: the S0-S15 state machine of the automated loop")
    sub = parser.add_subparsers(dest="command", required=True)
    entries = {
        "preregister": ("--config", "--cycles", "--mode", "--publish-ref"),
        "preflight": ("--config", "--mode"),
        "run": ("--config", "--cycles", "--mode", "--acknowledge", "--reason",
                "--publish-ref"),
        "status": ("--run",),
        "adjudicate": ("--run",),
        "appeal": ("--run", "--path"),
        "reopen": ("--run", "--ruling", "--reason"),
        "close": ("--run",),
        "dry-run": ("--config", "--dry-run-out"),
    }
    for name, flags in entries.items():
        entry = sub.add_parser(name)
        for flag in flags:
            if flag == "--cycles":
                entry.add_argument(flag, type=int, default=None)
            else:
                entry.add_argument(flag, default=None)
    return parser


def main(argv: list[str] | None = None, *,
         modules: Modules | None = None) -> int:
    """Exit 0 on success; non-zero on any refusal, whose code goes to stderr."""

    args = _parser().parse_args(argv)
    name = args.command
    try:
        if name == "status":
            print(json.dumps(status(args.run, modules=modules), indent=2,
                             sort_keys=True))
            return 0
        if name == "adjudicate":
            adjudicate(args.run, modules=modules)
            return 0
        if name == "appeal":
            appeal(args.run, path=args.path, modules=modules)
            return 0
        if name == "reopen":
            ruling = _read_json(Path(args.ruling)) if args.ruling else None
            reopen(args.run, ruling, modules=modules, reason=args.reason)
            return 0
        if name == "close":
            close(args.run, modules=modules)
            return 0
        if name == "dry-run":
            dry_run(Path(args.config) if args.config else None,
                    args.dry_run_out, modules=modules)
            return 0
        config = _load_config(args.config, getattr(args, "cycles", None),
                              getattr(args, "mode", None),
                              getattr(args, "publish_ref", None))
        if name == "preregister":
            preregister(config, modules=modules, budget_override=args.cycles)
            return 0
        if name == "preflight":
            preflight(config, modules=modules)
            return 0
        if name == "run":
            run(config, modules=modules, budget_override=args.cycles,
                acknowledge=args.acknowledge, reason=args.reason)
            return 0
    except LoopError as exc:
        print(f"{exc.code}: {exc.detail}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
