"""C001 register marking over the residue W2-MARKPREP leaves (wave 4, W4-MARKER).

What this is
------------
One :class:`minireason.loop.markprep.Cell` is a ``(endpoint, arm)`` table of a
C001 occurrence.  W2-MARKPREP has already settled everything the *program* can
settle before any call - the byte-identity defeater, the under-replication
rule, register E's bare-token forcing, registers T and D parsed on the FCL arm
- and has left a **residue**: exactly the ``(comparison, register)`` rows it
could not decide.  This module marks those rows and nothing besides them, and
then reads PLAN §8a's register-to-falsifier mapping against the result.

1.  **The sealed baseline first (G8).**  :func:`mark_cell` refuses an unsealed
    cell or a sha the cell does not carry, and every pack it renders goes
    through :func:`minireason.loop.packs.render_register`, which is where G8
    lives: *no cross-case pack exists to send* until the seal does, and the
    digest is pinned into the pack record, so every call record that carries
    the pack digest carries the baseline's too.  Revising the baseline
    afterwards changes a hash those records already hold.
2.  **Pairwise trials with mandatory order-swap.**  Every undecided row is put
    to the two marker seats - §2.2's "the marker reuses the judge pair" - in
    **both** presentation orders, through
    :func:`minireason.loop.packs.both_orders`.  A seat that moves with the
    order is ``blocked:order-swap``; two seats that disagree at one
    presentation are ``blocked:ensemble-split``.  Both leave the row
    ``unresolved``.  Neither is ever averaged or majority-voted.
3.  **The program downgrade at kind grain (G9).**  A ``differs`` whose
    ``difference_kind`` is already in the frozen within-ORIGINAL baseline's
    kind set for that register is **written** ``same`` **by the program**, with
    the forcing baseline replicate pair recorded on the row.
4.  **The falsifier evaluation.**  :func:`falsifiers` reads D1, F2 and F3 off
    :data:`minireason.loop.standard.FALSIFIER_MAP`: a falsifier *fires* where a
    ``differs`` stands on a carrying register of its declared comparison, and
    the program's byte-identity finding - G10(a) - stands beside the marks and
    *defeats* D1.  **G alone never carries D1**, and F2 and F3 fire only on T,
    E or D: both are read off the frozen map's
    ``carrying_registers``/``excluded_registers`` and never restated here.

The four registers are marked separately and never combined: there is no
cell-level mark, no aggregate view, no ``combined`` property, and no key in the
graph that could hold a mark for two registers at once.  Nothing here sums,
ranks, scores, meters or averages, and a budget that binds is a declared
resource boundary.

Why this module does not call ``trial.run_trial``, and what it uses instead
--------------------------------------------------------------------------
The draft this file replaces called :func:`minireason.loop.trial.run_trial`
with ``mode="pairwise"``, against a *declared* interface written before
W3-TRIAL existed.  The trial as built **refuses exactly that call**, twice
over and deliberately: ``mode`` must be
:data:`~minireason.loop.standard.MODE_ABSOLUTE` or the trial raises
``TRIAL_MODE_UNEXPECTED``, and a :class:`~minireason.loop.graph.CellKey` that
names a register is refused with the same code and the message *"marks run
pairwise through W4-MARKER's caller, not through the relation trial"*.
W3-TRIAL's own record says the same thing twice more (its module docstring:
"It seals no baseline (G8-G10 are W2-MARKPREP's and W4-MARKER's, and marks
ride the same *roles* gates through their own callers)"; deviation 2), and
WAVE3-INTERFACE §1 records G8/G9/G10 as absent from ``trial`` on purpose.

So the pairwise guard is **this module's**, built out of the same owners the
relation trial is built out of: W2-PACKS renders the register pack and its two
orders, W2-ROLES spends the call through the same two gates and writes the
same write-once call record, W1-SURFACE resolves the two quotes through
:func:`minireason.loop.markprep.resolve_pair`, and the block-code spellings
are **imported from** ``trial`` so a marker block and a trial block are one
vocabulary with one owner.  The edge to W3-TRIAL the wave plan declares is
therefore real - it is the block vocabulary and the guard-check names - and
there is no second implementation of the relation trial here.

Deviations from the design entry, and why
-----------------------------------------
1. **``records_dir=`` is a required keyword argument** the entry's signature
   does not spell, for W3-TRIAL's own reason (its deviation 1): W2-ROLES'
   call records are write-once and no call is ever made with nowhere to write
   it.  ``provider_factory=`` is the offline seam W6-DRYRUN binds;
   ``marker_caller=`` and ``registered_by=`` default to
   :func:`minireason.loop.roles.call_marker` and
   :func:`minireason.loop.graph.register_mark`.  **The seams are not
   bypasses**: the defaults are the real dispatch and the real registration,
   and ``tests/loop/test_marker.py`` drives every acceptance clause through
   them over ``OfflineProvider`` fixtures with the socket layer removed.
2. **``residue=`` narrows what is trialled**, defaulting to the cell's own
   residue.  A row offered that the program has already decided is
   :data:`MARKER_RESIDUE_CONTRADICTED`, not a re-reading.
3. **A mark's transcript exchange is the two seats' cases at the as-declared
   presentation, and its decisive point is the program-framed quote pair.**
   The marker contract carries no ``decisive_point`` - no seat picks one -
   but ``graph``'s rubric-typed warrant demands a conforming transcript, so
   the program composes one from the two citations it has already resolved
   against the material under G2, and asserts by program that it resolves
   exactly once in ``case + "\\n" + answer``.  Where it does not, the row is
   ``unresolved`` under ``blocked:referential-integrity`` - W1-SURFACE's own
   code, not a private one.
4. **The register cells must already be open.**  Opening the unresolved
   defaults is PREREGISTER's (§4.1 S0, §3(c)); a cell this module cannot
   register into is named **before any call is spent**, never after.
5. **An ``unresolved`` row registers nothing.**  ``unresolved`` is the cell's
   grounded default and :meth:`graph.ReadingResult.validated` refuses it as a
   mark; the row is returned, written and reported, and the default stands.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any

from minireason.loop import contracts, custody, graph, markprep, packs, roles
from minireason.loop import standard as standard_module
from minireason.loop import trial, types


__all__ = [
    "CellMarks",
    "MARKER_INPUT_MALFORMED",
    "MARKER_RESIDUE_CONTRADICTED",
    "MARKER_SCHEMA",
    "MARKS",
    "MarkRow",
    "MarkerRefused",
    "NEW_CODES",
    "PROGRAM_SOURCE",
    "REGISTERS",
    "RegisterMarks",
    "TRIAL_SOURCE",
    "falsifiers",
    "mark_cell",
]


# --------------------------------------------------------------------- codes

MARKER_INPUT_MALFORMED = "MARKER_INPUT_MALFORMED"
MARKER_RESIDUE_CONTRADICTED = "MARKER_RESIDUE_CONTRADICTED"

#: Codes this module raises, each with the one-line reason it exists.  Both are
#: reached by a call site here; a declared code nothing can raise is a code no
#: register ever prints.  Every block a *mark* can carry is a member of
#: :data:`types.BLOCK_CODES` and is **returned on the row**, never raised.
NEW_CODES: Mapping[str, str] = MappingProxyType({
    MARKER_INPUT_MALFORMED:
        "an argument to mark_cell or falsifiers is not the record it names - a "
        "cell, seal, seat plan, config, records directory, residue row or marks "
        "value - or a register cell it must register into was never opened",
    MARKER_RESIDUE_CONTRADICTED:
        "a row offered for marking is one the program already decided, or one "
        "with no readable replicate to build a side from, so there is nothing "
        "the residue could have left open there",
})


class MarkerRefused(types.LoopError, ValueError):
    """A marking input, or an ordering, the program refuses.

    ``(code, detail="")``, the argument order every earlier wave's exception
    takes, on the same two bases: a :class:`~minireason.loop.types.LoopError`
    so one ``except LoopError`` catches every loop refusal, and a
    ``ValueError`` so a record-shaped mistake stays a type-level fault.
    """


def _refuse(code: str, detail: str = "") -> MarkerRefused:
    return MarkerRefused(code, detail)


# --------------------------------------------------------------------- vocabulary

MARKER_SCHEMA = "minireason.loop.marker.v1"

#: The four PLAN §8a registers.  One owner - ``standard.REGISTER_IDS`` -
#: imported, never retyped.
REGISTERS: tuple[str, ...] = standard_module.REGISTER_IDS

#: The three marks, likewise mirrored from the frozen material by ``standard``.
MARKS: tuple[str, ...] = standard_module.MARKS
DIFFERS = standard_module.DIFFERS_MARK
UNRESOLVED = standard_module.UNRESOLVED_TOKEN
SAME = next(mark for mark in MARKS if mark not in (DIFFERS, UNRESOLVED))

#: Who wrote a mark.
PROGRAM_SOURCE = "program"
TRIAL_SOURCE = "trial"

#: The block spellings a mark can carry, imported from W3-TRIAL - the one
#: owner of the guard's vocabulary - so a marker block and a trial block are
#: one code and not two.
SCHEMA_BLOCK = trial.SCHEMA_BLOCK
PROVIDER_BLOCK = trial.PROVIDER_BLOCK
ENSEMBLE_SPLIT_BLOCK = trial.ENSEMBLE_SPLIT_BLOCK
ORDER_SWAP_BLOCK = trial.ORDER_SWAP_BLOCK
REFERENTIAL_INTEGRITY_BLOCK = trial.REFERENTIAL_INTEGRITY_BLOCK
OPERATIVE_TARGET_BLOCK = trial.OPERATIVE_TARGET_BLOCK

#: The guard steps a mark row records, in §2.4's order.  G8, G9 and G10 are
#: here because the pairwise leg is where they live; G5 and G6 carry the same
#: names they carry on a relation trial, imported from ``trial``.
G1_SCHEMA = trial.G1_SCHEMA
G2_UNIQUENESS = trial.G2A_UNIQUENESS
G3_OPERATIVE_TARGET = trial.G3_OPERATIVE_TARGET
G5_UNANIMITY = trial.G5_UNANIMITY
G6_ORDER_SWAP = trial.G6_ORDER_SWAP
G8_BASELINE_SEAL = "G8-baseline-seal"
G9_REPLICATE_BASELINE = "G9-replicate-baseline"
G10_PROGRAM_PREEMPT = "G10-program-pre-empt"
G12_NO_SCORING_KEY = trial.G12_NO_SCORING_KEY

GUARD_CHECKS: tuple[str, ...] = (
    G8_BASELINE_SEAL,
    G10_PROGRAM_PREEMPT,
    G1_SCHEMA,
    G2_UNIQUENESS,
    G3_OPERATIVE_TARGET,
    G5_UNANIMITY,
    G6_ORDER_SWAP,
    G9_REPLICATE_BASELINE,
    G12_NO_SCORING_KEY,
)

PERFORMED = trial.PERFORMED
NOT_PERFORMED = trial.NOT_PERFORMED

#: The program line that frames a mark's two citations into one decisive point.
CITATION_FRAME = "A: {left}\nB: {right}"


# --------------------------------------------------------------------- rows


@dataclass(frozen=True)
class MarkRow:
    """One ``(comparison, register)`` mark, at the grain PLAN §8a pins it.

    ``mark`` is one of :data:`MARKS`; ``difference_kind`` is a member of the
    register's closed set and is present exactly where the mark is ``differs``.
    ``source`` is :data:`PROGRAM_SOURCE` for a G9/G10 verdict - a baseline
    downgrade included - and :data:`TRIAL_SOURCE` for a pairwise trial's
    agreed mark.  ``block`` carries the one block code that left the row
    unresolved, ``forced_by`` the baseline replicate pairs a downgrade names,
    and ``checks`` every guard step this row reached, ``performed`` or
    ``not_performed``.
    """

    comparison: str
    left_case: str
    right_case: str
    register: str
    mark: str
    difference_kind: str | None
    source: str
    block: str | None = None
    forced_by: tuple[Mapping[str, Any], ...] = ()
    checks: Mapping[str, str] = field(default_factory=dict)
    evidence: Mapping[str, Any] = field(default_factory=dict)
    baseline_sha256: str = ""
    registered: str | None = None

    def __post_init__(self) -> None:
        if self.mark not in MARKS:
            raise _refuse(MARKER_INPUT_MALFORMED, f"{self.mark!r} is not one of {MARKS}")
        if self.register not in REGISTERS:
            raise _refuse(MARKER_INPUT_MALFORMED,
                          f"{self.register!r} is not one of {REGISTERS}")
        if self.source not in (PROGRAM_SOURCE, TRIAL_SOURCE):
            raise _refuse(MARKER_INPUT_MALFORMED, f"{self.source!r} wrote no mark")
        if self.block is not None and self.block not in types.BLOCK_CODES:
            raise _refuse(MARKER_INPUT_MALFORMED, f"{self.block!r} is no block code")
        if (self.difference_kind is None) == (self.mark == DIFFERS):
            raise _refuse(
                MARKER_INPUT_MALFORMED,
                "a differs owes its difference_kind, and no other mark carries one")
        allowed = contracts.difference_kinds_for(self.register)
        if self.difference_kind is not None and self.difference_kind not in allowed:
            raise _refuse(
                MARKER_INPUT_MALFORMED,
                f"{self.register}: {self.difference_kind!r} is outside {allowed}")

    @property
    def differs(self) -> bool:
        return self.mark == DIFFERS

    @property
    def unresolved(self) -> bool:
        return self.mark == UNRESOLVED

    def as_dict(self) -> dict[str, Any]:
        record = {
            "comparison": self.comparison,
            "left_case": self.left_case,
            "right_case": self.right_case,
            "register": self.register,
            "mark": self.mark,
            "difference_kind": self.difference_kind,
            "source": self.source,
            "block": self.block,
            "forced_by": [dict(pair) for pair in self.forced_by],
            "checks": dict(self.checks),
            "evidence": dict(self.evidence),
            "baseline_sha256": self.baseline_sha256,
            "registered": self.registered,
        }
        contracts.assert_no_scoring_keys(record)
        return record


@dataclass(frozen=True)
class RegisterMarks:
    """The four registers of one comparison, kept four and kept apart.

    A mapping view keyed by register.  There is deliberately no aggregate view
    and no ``combined`` property, because no caller is owed one.
    """

    comparison: str
    left_case: str
    right_case: str
    rows: Mapping[str, MarkRow]

    def __post_init__(self) -> None:
        if set(self.rows) != set(REGISTERS):
            raise _refuse(
                MARKER_INPUT_MALFORMED,
                f"a comparison carries exactly {REGISTERS}, not {sorted(self.rows)}")

    def row(self, register: str) -> MarkRow:
        return self.rows[register]

    def as_dict(self) -> dict[str, Any]:
        record = {
            "comparison": self.comparison,
            "left_case": self.left_case,
            "right_case": self.right_case,
            "registers": {r: self.rows[r].as_dict() for r in REGISTERS},
        }
        contracts.assert_no_scoring_keys(record)
        return record


@dataclass(frozen=True)
class CellMarks:
    """Every comparison's four register marks, the pinned seal, and the program
    findings they were judged beside - carried verbatim, so the falsifier
    evaluation stands them beside the marks rather than after them."""

    cell: str
    endpoint: str
    arm: str
    baseline_sha256: str
    comparisons: Mapping[str, RegisterMarks]
    program_findings: Mapping[str, Any] = field(default_factory=dict)
    calls: tuple[Mapping[str, Any], ...] = ()

    def row(self, comparison: str, register: str) -> MarkRow:
        return self.comparisons[comparison].row(register)

    def as_dict(self) -> dict[str, Any]:
        record = {
            "schema": MARKER_SCHEMA,
            "cell": self.cell,
            "endpoint": self.endpoint,
            "arm": self.arm,
            "baseline_sha256": self.baseline_sha256,
            "comparisons": {
                label: block.as_dict() for label, block in self.comparisons.items()
            },
            "program_findings": dict(self.program_findings),
            "calls": [dict(call) for call in self.calls],
        }
        contracts.assert_no_scoring_keys(record)
        return record


# --------------------------------------------------------------------- inputs


def _require_cell(cell: Any) -> markprep.Cell:
    if not isinstance(cell, markprep.Cell):
        raise _refuse(MARKER_INPUT_MALFORMED,
                      f"a markprep.Cell, not {type(cell).__name__}")
    return cell


def _require_seal(cell: markprep.Cell, baseline_sha: Any) -> str:
    """G8, before anything else: the seal exists and is the one the cell carries."""
    if baseline_sha is None:
        raise markprep.BaselineNotFirst(
            markprep.BASELINE_NOT_FIRST,
            f"{cell.cell_id}: mark_cell renders no cross-case pack without the seal")
    if not isinstance(baseline_sha, str) or len(baseline_sha) != 64:
        raise _refuse(MARKER_INPUT_MALFORMED, "baseline_sha is a sha256 hex digest")
    cell.require_seal("mark_cell")
    if baseline_sha != cell.baseline_sha:
        raise markprep.BaselineNotFirst(
            markprep.BASELINE_NOT_FIRST,
            f"{cell.cell_id}: the sha offered is not the seal the cell carries; a "
            "revised baseline is a different hash and G8 refuses it")
    return baseline_sha


def _require_seats(seats: Any) -> Any:
    judges = getattr(seats, "judges", None)
    if judges is None or len(judges) < 2:
        raise _refuse(
            MARKER_INPUT_MALFORMED,
            "the marker reuses the judge pair (§2.2), so a seat plan with two "
            "judge seats is required")
    return seats


def _require_records_dir(records_dir: Any) -> Path:
    if records_dir is None:
        raise _refuse(
            MARKER_INPUT_MALFORMED,
            "records_dir= is required; every call record is write-once and no "
            "call is ever made with nowhere to write it")
    return Path(records_dir)


def _require_residue(residue: Any) -> tuple[markprep.ResidueRow, ...]:
    if isinstance(residue, (str, bytes)):
        raise _refuse(MARKER_INPUT_MALFORMED, "a residue is a sequence of rows")
    try:
        rows = tuple(residue)
    except TypeError as exc:
        raise _refuse(MARKER_INPUT_MALFORMED, f"the residue is not a sequence: {exc}")
    for row in rows:
        if not isinstance(row, markprep.ResidueRow):
            raise _refuse(MARKER_INPUT_MALFORMED,
                          f"{type(row).__name__} is no residue row")
    return rows


def _comparison_slug(left_case: str, right_case: str) -> str:
    """The coordinate segment of a comparison.

    A coordinate segment admits no space, so the comparison *label*
    (``ORIGINAL vs CONTROL``) cannot be one.  The slug is built from the two
    case names ``markprep`` owns and is the only place a coordinate spelling of
    a comparison exists.
    """
    return f"{left_case}-vs-{right_case}"


def _open_cell_keys(harness: Any) -> frozenset[str]:
    return frozenset(standing.key for standing in graph.cell_standings(harness))


def _mark_key(cell: markprep.Cell, register: str, comparison: str) -> graph.CellKey:
    return graph.CellKey(cell=cell.cell_id, register=register, comparison=comparison)


# --------------------------------------------------------------------- program rows


def _program_row(
    cell: markprep.Cell,
    program: Mapping[str, Any],
    label: str,
    register: str,
    seal: str,
) -> MarkRow:
    """The program's own verdict for one row (G9/G10), as a mark row.

    Where the program decided, **no marker seat is called at all**: that is
    §2.4 G10's whole point, and the forcing baseline pair a downgrade recorded
    is what the published mark has to carry to be the same fact.
    """
    entry = program["comparisons"][label]
    record = entry["registers"][register]
    block: str | None = None
    forced_by: tuple[Mapping[str, Any], ...] = ()
    for detail in record.get("kinds", {}).values():
        if detail.get("block") and detail.get("forced_by"):
            block = detail["block"]
            forced_by = tuple(dict(pair) for pair in detail["forced_by"].get("pairs", ()))
            break
    mark = record["mark"]
    return MarkRow(
        comparison=label,
        left_case=entry["left_case"],
        right_case=entry["right_case"],
        register=register,
        mark=mark,
        difference_kind=record.get("difference_kind") if mark == DIFFERS else None,
        source=PROGRAM_SOURCE,
        block=block,
        forced_by=forced_by,
        checks={
            G8_BASELINE_SEAL: PERFORMED,
            G10_PROGRAM_PREEMPT: PERFORMED,
            G9_REPLICATE_BASELINE: PERFORMED if forced_by else NOT_PERFORMED,
        },
        evidence={
            "program_decided": record.get("program_decided"),
            "forced_unresolved": record.get("forced_unresolved"),
            "kinds": record.get("kinds", {}),
        },
        baseline_sha256=seal,
    )


# --------------------------------------------------------------------- the pairwise leg


def _sides_of(cell: markprep.Cell, row: markprep.ResidueRow) -> tuple[str, str, Any, Any]:
    """The two case-representative replicates a pairwise surface is built from.

    The first *readable* replicate on each side: markprep names them at read
    time, so choosing the first readable is a function of the record and not a
    preference.  A side with no readable replicate could never have carried a
    surface, and refusing is the honest answer.
    """
    picked: list[str] = []
    for side, keys in (("left", row.left_replicates), ("right", row.right_replicates)):
        for key in keys:
            replicate = cell.replicate(key)
            if replicate.commitments is not None:
                picked.append(key)
                break
        else:
            raise _refuse(
                MARKER_RESIDUE_CONTRADICTED,
                f"{cell.cell_id} {row.comparison} {row.register}: no readable "
                f"{side} replicate, so no pairwise surface can be built")
    left_key, right_key = picked
    return left_key, right_key, cell.replicate(left_key), cell.replicate(right_key)


def _unresolved_row(
    row: markprep.ResidueRow,
    *,
    block: str | None,
    checks: Mapping[str, str],
    evidence: Mapping[str, Any],
    seal: str,
) -> MarkRow:
    return MarkRow(
        comparison=row.comparison,
        left_case=row.left_case,
        right_case=row.right_case,
        register=row.register,
        mark=UNRESOLVED,
        difference_kind=None,
        source=TRIAL_SOURCE,
        block=block,
        checks=dict(checks),
        evidence=dict(evidence),
        baseline_sha256=seal,
    )


def _mark_row(
    cell: markprep.Cell,
    row: markprep.ResidueRow,
    baseline: Any,
    seal: str,
    standard_body: Any,
    plan: Any,
    records_dir: Path,
    *,
    marker_caller: Callable[..., Any],
    provider_factory: Any,
    calls: list[Mapping[str, Any]],
) -> MarkRow:
    """One residue row, through the pairwise guard, end to end.

    Order: G8 (the seal, already asserted and re-asserted by the pack), G1
    (schema and delivery), G2/G3 (the two citations against the material),
    G5 (the two seats at the as-declared presentation), G6 (each seat's two
    presentations), then G9 (the kind-grain downgrade).  The first failure
    leaves the row ``unresolved`` with its block code; nothing registers.
    """
    checks = {name: NOT_PERFORMED for name in GUARD_CHECKS}
    checks[G8_BASELINE_SEAL] = PERFORMED
    checks[G10_PROGRAM_PREEMPT] = PERFORMED

    left_key, right_key, left, right = _sides_of(cell, row)
    surface = markprep.pairwise_surface(cell, left_key, right_key)
    sides = (
        packs.MarkSide(arm=row.left_case, text=left.commitments),
        packs.MarkSide(arm=row.right_case, text=right.commitments),
    )
    # W2-PACKS reads a cell as a string, a mapping, or an object with ``.cell``
    # (``graph.CellKey``'s spelling); ``markprep.Cell`` spells it ``cell_id``,
    # so the id is handed over rather than the record.
    pack = packs.render_register(
        cell.cell_id, row.register, row.comparison, seal, standard_body,
        sides=sides)
    slug = _comparison_slug(row.left_case, row.right_case)
    base_coordinate = f"{cell.cell_id}/{slug}/{row.register}"

    per_seat: dict[str, dict[str, Any]] = {}
    for seat_index, seat in enumerate(plan.judges):
        for presented in packs.both_orders(pack):
            suffix = ("" if presented.order == packs.ORDER_AS_DECLARED
                      else "#order-swapped")
            coordinate = base_coordinate + suffix
            result = marker_caller(
                seat,
                presented,
                records_dir,
                coordinate=coordinate,
                register=row.register,
                seat_index=seat_index,
                provider_factory=provider_factory,
                seat_token=f"{seat.label}@{coordinate}",
            )
            calls.append({
                "role": packs.ROLE_MARKER,
                "coordinate": coordinate,
                "seat_label": result.coordinate.seat_label,
                "order": presented.order,
                "register": row.register,
                "status": result.status,
                "block": result.block,
                "pack_sha256": packs.pack_sha(presented),
                "baseline_sha256": seal,
                "record_path": result.record_path,
            })
            if result.blocked:
                return _unresolved_row(
                    row,
                    block=result.block or SCHEMA_BLOCK,
                    checks=checks,
                    evidence={"detail": result.detail or result.reason,
                              "coordinate": coordinate,
                              "order": presented.order},
                    seal=seal)
            per_seat.setdefault(seat.label, {})[presented.order] = result
    checks[G1_SCHEMA] = PERFORMED

    # ---- G2/G3: the two citations, against the material ---------------------
    checks[G2_UNIQUENESS] = PERFORMED
    checks[G3_OPERATIVE_TARGET] = PERFORMED
    for label, by_order in per_seat.items():
        for order, result in by_order.items():
            output = result.output
            if output.mark != DIFFERS:
                # `same` and `unresolved` cite nothing: the contract gives them
                # no quotes to resolve, so there is nothing for G2 to check.
                continue
            resolved = markprep.resolve_pair(
                surface, output.left_quote, output.right_quote)
            if resolved.block is not None:
                return _unresolved_row(
                    row, block=resolved.block, checks=checks,
                    evidence={"seat": label, "order": order,
                              "left_count": resolved.left_count,
                              "right_count": resolved.right_count},
                    seal=seal)

    # ---- G5: the two seats, at the as-declared presentation ------------------
    declared = {
        label: by_order[packs.ORDER_AS_DECLARED].output
        for label, by_order in per_seat.items()
    }
    values = {
        label: (output.mark, output.difference_kind)
        for label, output in declared.items()
    }
    checks[G5_UNANIMITY] = PERFORMED
    if len(set(values.values())) != 1:
        return _unresolved_row(
            row, block=ENSEMBLE_SPLIT_BLOCK, checks=checks,
            evidence={"rulings": {label: {"mark": output.mark,
                                          "difference_kind": output.difference_kind,
                                          "case": output.case}
                                  for label, output in declared.items()},
                      "note": "both rulings stand verbatim; a split is never "
                              "averaged and never majority-voted"},
            seal=seal)

    # ---- G6: each seat, in both presentations --------------------------------
    checks[G6_ORDER_SWAP] = PERFORMED
    for label, by_order in per_seat.items():
        first = by_order[packs.ORDER_AS_DECLARED].output
        second = by_order[packs.ORDER_SWAPPED].output
        if (first.mark, first.difference_kind) != (second.mark, second.difference_kind):
            return _unresolved_row(
                row, block=ORDER_SWAP_BLOCK, checks=checks,
                evidence={"seat": label,
                          packs.ORDER_AS_DECLARED: {"mark": first.mark,
                                                    "difference_kind":
                                                        first.difference_kind},
                          packs.ORDER_SWAPPED: {"mark": second.mark,
                                                "difference_kind":
                                                    second.difference_kind},
                          "note": "a mark that changes with the presentation "
                                  "order is not a mark"},
                seal=seal)

    agreed = next(iter(declared.values()))
    evidence = {
        "coordinate": base_coordinate,
        "left_replicate": left_key,
        "right_replicate": right_key,
        "surface_digest": surface.digest,
        "cases": {label: output.case for label, output in declared.items()},
        "quotes": {"left": agreed.left_quote, "right": agreed.right_quote},
    }

    if agreed.mark != DIFFERS:
        checks[G9_REPLICATE_BASELINE] = NOT_PERFORMED
        return MarkRow(
            comparison=row.comparison, left_case=row.left_case,
            right_case=row.right_case, register=row.register,
            mark=agreed.mark, difference_kind=None, source=TRIAL_SOURCE,
            checks=checks, evidence=evidence, baseline_sha256=seal)

    # ---- G9: the kind-grain replicate baseline -------------------------------
    checks[G9_REPLICATE_BASELINE] = PERFORMED
    kind = agreed.difference_kind
    if baseline.exhibits(row.register, kind):
        forcing = tuple(
            pair.as_dict() if hasattr(pair, "as_dict") else dict(pair)
            for pair in baseline.pairs if kind in pair.kinds
        )
        return MarkRow(
            comparison=row.comparison, left_case=row.left_case,
            right_case=row.right_case, register=row.register,
            mark=SAME, difference_kind=None, source=PROGRAM_SOURCE,
            block=markprep.BASELINE_FORCED_SAME_BLOCK,
            forced_by=forcing, checks=checks,
            evidence=dict(evidence, downgraded_from_kind=kind, note=(
                "the within-ORIGINAL baseline already exhibits this kind "
                "between a pair of replicates, so the program writes same "
                "(PLAN 8a, G9) and records the forcing pair")),
            baseline_sha256=seal)

    return MarkRow(
        comparison=row.comparison, left_case=row.left_case,
        right_case=row.right_case, register=row.register,
        mark=DIFFERS, difference_kind=kind, source=TRIAL_SOURCE,
        checks=checks, evidence=evidence, baseline_sha256=seal)


#: The program's own decisive line for a mark it wrote without asking a seat.
PROGRAM_POINT = "the program read {register} on {comparison} as {mark}"


def _transcript_of(cell_key: graph.CellKey, marked: MarkRow) -> graph.Transcript | None:
    """A mark's conforming transcript, composed from what the guard resolved.

    The marker contract carries no ``decisive_point`` - no seat picks one - but
    W1-GRAPH's rubric-typed warrant demands a conforming transcript, so the
    program composes one and asserts by program that it resolves exactly once
    in ``case + "\n" + answer``.

    * For a mark a **trial** wrote, the exchange is the two seats' cases at the
      as-declared presentation - the presentation the record cites - and the
      point is the program's framing of the two citations G2 already resolved
      against the material.
    * For a mark the **program** wrote (G9's downgrade, G10's pre-empt), there
      are no seat cases at all: the exchange is the program's own verdict line
      and the kind-grain evidence behind it.

    ``None`` where the point does not resolve exactly once, which is the row's
    ``blocked:referential-integrity``.
    """
    cases = dict(marked.evidence.get("cases") or {})
    meta = {
        "cell": cell_key.token,
        "register": marked.register,
        "comparison": marked.comparison,
        "baseline_sha256": marked.baseline_sha256,
        "source": marked.source,
        "forced_by": [dict(pair) for pair in marked.forced_by],
    }
    if marked.source == PROGRAM_SOURCE or len(cases) < 2:
        point = PROGRAM_POINT.format(register=marked.register,
                                     comparison=marked.comparison,
                                     mark=marked.mark)
        answer = json.dumps(
            {"evidence": dict(marked.evidence),
             "forced_by": [dict(pair) for pair in marked.forced_by],
             "block": marked.block},
            sort_keys=True, ensure_ascii=False)
        if f"{point}\n{answer}".count(point) != 1:
            return None
        return graph.Transcript(case=point, answer=answer, decisive_point=point,
                                checks=dict(marked.checks), meta=meta)
    labels = sorted(cases)
    quotes = dict(marked.evidence.get("quotes") or {})
    point = CITATION_FRAME.format(left=quotes.get("left", ""),
                                  right=quotes.get("right", ""))
    case = f"{point}\n\n{cases[labels[0]]}"
    answer = cases[labels[1]]
    if f"{case}\n{answer}".count(point) != 1:
        return None
    return graph.Transcript(case=case, answer=answer, decisive_point=point,
                            checks=dict(marked.checks), meta=meta)


# --------------------------------------------------------------------- mark_cell


def mark_cell(
    harness: Any,
    cell: Any,
    baseline_sha: Any,
    standard: Any,
    seats: Any,
    config: Any,
    *,
    records_dir: Any = None,
    residue: Sequence[markprep.ResidueRow] | None = None,
    marker_caller: Callable[..., Any] = roles.call_marker,
    registered_by: Callable[..., graph.ReadingIds] = graph.register_mark,
    provider_factory: Any = None,
    out_dir: Any = None,
) -> CellMarks:
    """Mark one C001 cell over its residue, register by register, never combined.

    The design entry's six arguments stand first and positional.  Every mark
    the *program* settled is taken from :func:`markprep.program_marks` and no
    seat is asked about it; every row the residue left open goes through the
    pairwise guard of :func:`_mark_row`; a ``differs`` and a ``same`` are
    registered through ``registered_by`` and an ``unresolved`` registers
    nothing, because ``unresolved`` is the cell's standing and not a mark.
    """

    cell = _require_cell(cell)
    seal = _require_seal(cell, baseline_sha)
    plan = _require_seats(seats)
    records = _require_records_dir(records_dir)
    if config is None:
        raise _refuse(MARKER_INPUT_MALFORMED, "a loop config is required")

    program = markprep.program_marks(cell)
    rows = _require_residue(
        markprep.residue(cell) if residue is None else residue)
    offered = {(row.comparison, row.register): row for row in rows}

    decided = {
        (label, register)
        for label, entry in program["comparisons"].items()
        for register, record in entry["registers"].items()
        if record["program_decided"]
    }
    contradicted = sorted(set(offered) & decided)
    if contradicted:
        raise _refuse(
            MARKER_RESIDUE_CONTRADICTED,
            f"{cell.cell_id}: rows the program already decided were offered for "
            "marking: " + ", ".join(f"{c}/{r}" for c, r in contradicted))

    # Deviation 4: every register cell this pass could register into is named
    # BEFORE a single call is spent, never after.
    open_keys = _open_cell_keys(harness)
    missing = sorted(
        _mark_key(cell, register, label).token
        for label, entry in program["comparisons"].items()
        for register in REGISTERS
        if _mark_key(cell, register, label).token not in open_keys
    )
    if missing:
        raise _refuse(
            MARKER_INPUT_MALFORMED,
            f"{cell.cell_id}: no unresolved default is open for {missing}; "
            "opening the defaults is PREREGISTER's (§3(c)) and a mark is never "
            "the thing that opens the cell it attacks")

    baseline = markprep.build_baseline(cell)
    calls: list[Mapping[str, Any]] = []
    comparisons: dict[str, RegisterMarks] = {}

    for label, entry in program["comparisons"].items():
        marked: dict[str, MarkRow] = {}
        for register in REGISTERS:
            row = offered.get((label, register))
            if row is None:
                marked[register] = _program_row(cell, program, label, register, seal)
                continue
            marked[register] = _mark_row(
                cell, row, baseline, seal, standard, plan, records,
                marker_caller=marker_caller,
                provider_factory=provider_factory,
                calls=calls)
        comparisons[label] = RegisterMarks(
            comparison=label,
            left_case=entry["left_case"],
            right_case=entry["right_case"],
            rows=marked,
        )

    registered = _register_marks(harness, cell, comparisons, registered_by)
    result = CellMarks(
        cell=cell.cell_id,
        endpoint=cell.endpoint,
        arm=cell.arm,
        baseline_sha256=seal,
        comparisons=registered,
        program_findings=program,
        calls=tuple(calls),
    )
    if out_dir is not None:
        root = Path(out_dir)
        root.mkdir(parents=True, exist_ok=True)
        custody.write_new(custody.fenced(root, "marks.json"), result.as_dict())
    return result


def _register_marks(
    harness: Any,
    cell: markprep.Cell,
    comparisons: Mapping[str, RegisterMarks],
    registered_by: Callable[..., graph.ReadingIds],
) -> dict[str, RegisterMarks]:
    """Enter every admissible mark, one register at a time (§3, "marks enter
    the same way per register").

    An ``unresolved`` row registers nothing: it *is* the cell's standing, and
    :meth:`graph.ReadingResult.validated` refuses it as a mark.  A row whose
    decisive point could not be composed is turned back into
    ``blocked:referential-integrity`` before anything is registered.
    """
    out: dict[str, RegisterMarks] = {}
    for label, block in comparisons.items():
        rows: dict[str, MarkRow] = {}
        for register, marked in block.rows.items():
            if marked.unresolved:
                rows[register] = marked
                continue
            key = _mark_key(cell, register, label)
            transcript = _transcript_of(key, marked)
            if transcript is None:
                rows[register] = _unresolved_from(marked, REFERENTIAL_INTEGRITY_BLOCK)
                continue
            cases = marked.evidence.get("cases") or {}
            seat = sorted(cases)[0] if cases else PROGRAM_SOURCE
            ids = registered_by(
                harness,
                graph.ReadingResult(
                    key=key,
                    relation=marked.mark,
                    seat=seat,
                    transcript=transcript,
                    difference_kind=marked.difference_kind,
                    body={"source": marked.source,
                          "baseline_sha256": marked.baseline_sha256,
                          "forced_by": [dict(p) for p in marked.forced_by],
                          "checks": dict(marked.checks)},
                    roles=dict.fromkeys(sorted(cases), "marker"),
                ),
                _standard_id(harness),
            )
            rows[register] = MarkRow(
                comparison=marked.comparison, left_case=marked.left_case,
                right_case=marked.right_case, register=marked.register,
                mark=marked.mark, difference_kind=marked.difference_kind,
                source=marked.source, block=marked.block,
                forced_by=marked.forced_by, checks=marked.checks,
                evidence=marked.evidence, baseline_sha256=marked.baseline_sha256,
                registered=ids.reading)
        out[label] = RegisterMarks(
            comparison=block.comparison, left_case=block.left_case,
            right_case=block.right_case, rows=rows)
    return out


def _unresolved_from(marked: MarkRow, block: str) -> MarkRow:
    return MarkRow(
        comparison=marked.comparison, left_case=marked.left_case,
        right_case=marked.right_case, register=marked.register,
        mark=UNRESOLVED, difference_kind=None, source=marked.source,
        block=block, forced_by=marked.forced_by, checks=marked.checks,
        evidence=dict(marked.evidence, note=(
            "the mark's two citations did not compose a decisive point that "
            "resolves once in the exchange, so no warrant was minted")),
        baseline_sha256=marked.baseline_sha256)


def _standard_id(harness: Any) -> str:
    """The registered standard's artifact id, read off the graph.

    One owner: the standard is registered at PREREGISTER through
    :func:`graph.register_standard`, and re-registering it here would be a
    second body under a second id.
    """
    body = standard_module.STANDARD_BODY
    return graph.register_standard(harness, body)


# --------------------------------------------------------------------- falsifiers


def falsifiers(marks: Any, program_findings: Any = None) -> dict[str, Any]:
    """PLAN §8a's register-to-falsifier mapping, evaluated against the marks.

    One entry per falsifier of :data:`standard.FALSIFIER_MAP`: ``fired`` where
    a ``differs`` stands on a **carrying** register of that falsifier's
    declared comparison, and ``defeated`` where the program's byte-identity
    finding (G10(a)) stands beside the marks.  The two are reported side by
    side and never merged into one verdict: the program finding is a fact about
    bytes and the mark a fact about the material, and §8a reads them together.

    ``carrying_registers`` and ``excluded_registers`` are the frozen map's own,
    so **G alone never carries D1** and **F2 and F3 fire only on T, E or D**
    are read off the standard rather than restated here.  Nothing is summed,
    ranked, scored or combined; a falsifier that did not fire is reported *not
    fired*, never as a quantity.
    """

    if isinstance(marks, CellMarks):
        findings = dict(marks.program_findings)
        blocks: Mapping[str, Any] = marks.comparisons
        seal = marks.baseline_sha256
        cell_id = marks.cell
    elif isinstance(marks, Mapping):
        cell_id = str(marks.get("cell", ""))
        seal = str(marks.get("baseline_sha256", ""))
        findings = dict(marks.get("program_findings") or {})
        raw = marks.get("comparisons")
        if not isinstance(raw, Mapping):
            raise _refuse(MARKER_INPUT_MALFORMED, "marks carry no comparisons")
        blocks = raw
    else:
        raise _refuse(MARKER_INPUT_MALFORMED, f"marks: {type(marks).__name__}")
    if program_findings is not None:
        if not isinstance(program_findings, Mapping):
            raise _refuse(MARKER_INPUT_MALFORMED, "program_findings is a mapping")
        findings = dict(program_findings)

    byte_identity = findings.get("byte_identity") or {}
    d1_not_exhibited = bool(byte_identity.get("d1_not_exhibited"))

    out: dict[str, Any] = {}
    for name in sorted(standard_module.FALSIFIER_MAP):
        declared = standard_module.FALSIFIER_MAP[name]
        label = markprep.COMPARISON_LABELS[tuple(declared.comparison)]
        block = blocks.get(label)
        carried: list[dict[str, Any]] = []
        fired_rows: list[dict[str, Any]] = []
        excluded: list[dict[str, Any]] = []
        if block is not None:
            rows = block.rows if isinstance(block, RegisterMarks) else block
            rows = rows["registers"] if isinstance(rows, Mapping) and "registers" in rows else rows
            for register in declared.carrying_registers:
                row = rows[register]
                body = row.as_dict() if hasattr(row, "as_dict") else dict(row)
                carried.append(body)
                if body.get("mark") == DIFFERS:
                    fired_rows.append(body)
            for register in declared.excluded_registers:
                row = rows[register]
                body = row.as_dict() if hasattr(row, "as_dict") else dict(row)
                excluded.append(body)
        entry = {
            "schema": MARKER_SCHEMA,
            "falsifier": name,
            "comparison": label,
            "cell": cell_id,
            "baseline_sha256": seal,
            "carrying_registers": list(declared.carrying_registers),
            "excluded_registers": list(declared.excluded_registers),
            "rule": declared.rule,
            "exclusion_reason": declared.exclusion_reason,
            "carried": carried,
            "excluded": excluded,
            "fired_rows": fired_rows,
            "fired": bool(fired_rows),
            "program_finding": dict(byte_identity),
            "defeated": bool(name == "D1" and d1_not_exhibited),
        }
        contracts.assert_no_scoring_keys(entry)
        out[name] = entry
    return out
