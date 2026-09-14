"""Drive the reading trials over the pre-registered reading set (wave 4, W4-READER).

Purpose
-------
For every row of the pre-registered reading set, drive the guarded trial of
W3-TRIAL, register every surviving reading into the graph through
:func:`minireason.loop.graph.register_reading`, and hand back one frozen
record in five registers kept separate and never combined: ``registered``
(the readings the graph accepted), ``blocks`` (every guard block, by reason
code, with both blob refs), ``dispositions`` (the row-level endings the
critic's own answer forces), ``indeterminate`` (coordinates a record shows
were claimed and never answered - reported as such, never as an absence) and
``unread`` (every open cell nothing read).

The module speaks to no model: every provider call is W3-TRIAL's, and every
record of one is W2-ROLES'.  Its own work is the *row* bookkeeping the trial
cannot see - one trial per pre-registered row, the resume rule that refuses to
re-send a claimed-and-unanswered coordinate, the write-once row records, the
planned/dispatched accounting PREFLIGHT compares (design §4.1 S1), and the
decision to open the graph's door on a survivor.

What it reads off a ``TrialResult``, and why it reads nothing else
-----------------------------------------------------------------
W3-TRIAL landed after this module was drafted, and the draft was written
against a *fake* ``TrialResult`` whose ``outcome`` was an object with a
``.status`` in six tokens, whose ``blocks`` carried ``reason``/``prompt_ref``
and whose ``transcript`` was a record.  None of those is the real shape.  The
real one, imported here and never restated:

* ``TrialResult.outcome`` is a **string**, a member of :data:`trial.OUTCOMES`
  - ``blocked``, ``not-sustained``, ``sustained``, ``no-trial``,
  ``unresolved`` - five, not six, and ``indeterminate`` is not among them
  because a trial that did not answer returns no result at all;
* ``TrialResult.blocks`` is a tuple of :class:`trial.Block`, whose fields are
  ``code``, ``check``, ``detail``, ``prompt_ref_path``, ``raw_ref_path``,
  ``prompt_sha``, ``raw_sha``;
* ``TrialResult.transcript`` is the **emitted transcript text**;
* ``TrialResult.reading`` is the :class:`~minireason.loop.graph.ReadingResult`
  a sustained trial built, and this module registers *that object* rather than
  assembling a second one.  That is the whole answer to WAVE3-INTERFACE §8
  question 4 ("which seat spelling does W4-READER write?"): it writes none.
  The spelling is ``seats.Seat.label`` / ``roles.Coordinate.seat_label``
  (``judge#1``), it is written once, by the trial, and a reader that rebuilt
  the record would be a second owner of it - which is exactly the defect
  WAVE3-INTERFACE §6 found in the audit layer's invented ``judge-1`` panel.
* ``TrialResult.critic`` is the :class:`~minireason.loop.contracts.CriticOutput`,
  and its ``outside_vocabulary`` is where D6's preserved text lives.

Design section implemented
--------------------------
Design of record §2.3 (the two critic short-circuits), §2.4 (only a fully
guarded reading registers; a blocked trial registers nothing and is logged by
reason code with its prompt and raw blob refs), §3 ("Consequences" - two
surviving rivals leave the cell contested and are a discrimination problem,
never an average), §4.3 (coordinate-grain resume, and ``INDETERMINATE`` for a
request without a response) and the W4-READER entry of §7.

Deviations from the design entry, and why
-----------------------------------------
0. **Import edges ``custody``, ``roles``, ``standard`` and ``types`` beyond
   the declared ``depends_on: [W1-GRAPH, W3-TRIAL]``.**  Each because a
   spelling has exactly one owner (wave-2 integration decision 54):
   ``types`` owns :class:`~minireason.loop.types.LoopError`; ``custody`` owns
   the fence and the write-once write; ``standard`` owns the rubric's absolute
   mode; ``contracts`` owns ``assert_no_scoring_keys``, which G12 runs over
   every record this module emits before it is written; ``roles`` owns the
   call record's ``record``/``call_record`` spelling, which is how this module
   tells a claimed coordinate that answered from one that did not without
   inventing a second layout.  The ``obligations``
   disposition token is mirrored as a spelling with the mirror asserted by
   test, never imported, so W4 adds no edge to W1-OBLIGATIONS.
1. **Three keyword-only arguments the entry's signature does not spell.**
   ``trial_runner=`` defaults to :func:`trial.run_trial` itself and exists so
   the dry run can bind the same function with its own fixtures;
   ``registered_by=`` defaults to :func:`graph.register_reading`;
   ``provider_factory=`` is passed straight through to the trial, which is how
   W6-DRYRUN runs the whole reading arm on ``OfflineProvider`` with zero
   sockets.  **The seam is not a bypass**: the default runner is the real
   guard, every test in ``tests/loop/test_reader.py`` drives the real
   :func:`trial.run_trial` at least once, and a runner that answered without
   running the guard would register a reading the graph refuses, because the
   object the graph is handed is the trial's own ``ReadingResult``.
2. **``table`` is any iterable of row descriptors**, coerced by
   :meth:`ReadingRow.coerce`: a mapping carrying ``row_key`` and ``surface``,
   optionally ``cell``.  A row does **not** declare the relation under trial.
   The draft required one; the critic nominates it (§2.3) and G4 is the only
   gate on it, so a row that declared one would be the reader telling the
   guard what it must find.
3. **Cell keys default to the row key**, because a relation reading cell *is*
   its row (§3(c)).  Two rows may name one cell: that is how "multiple
   nominated relations are tried as separate trials" is spelled, and it is why
   each row gets its own records directory - two trials of one cell must not
   collide on one write-once coordinate.
4. **``Readings.unread`` and ``Readings.dispositions`` are exposed beyond the
   entry's three registers.**  ``unread`` answers WAVE3-INTERFACE §8 question
   3: W3-REPORT unions the plan's reading set with ``state.unread``, and this
   is the thing that computes it - every cell open in the graph that this pass
   registered no reading for, including cells the reading set never named.
5. **A claimed-and-unanswered coordinate is not re-sent.**  §4.3's rule at
   coordinate grain: the row is *not dispatched*, it is reported
   ``INDETERMINATE``, and ``planned`` therefore exceeds ``dispatched`` on a
   resumed pass.  The pair is an identity to compare, never a ratio.

What this module refuses to do
------------------------------
It never averages, merges, ranks or votes: two surviving readings of one cell
are two registrations and ``contested`` is read back from the graph's own
adjudication, never decided here.  It retries nothing.  It counts nothing
beyond the declared ``planned``/``dispatched`` pair.  Every record it writes
goes through :func:`minireason.loop.custody.write_new`, so a second pass over
a row that already wrote one refuses rather than overwrites.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

from minireason.loop import contracts, custody, graph, roles, standard, trial, types


__all__ = [
    "BlockRecord",
    "DISPOSITION_CRITIC_NONE",
    "DISPOSITION_INDETERMINATE",
    "DISPOSITION_NOT_SUSTAINED",
    "DISPOSITION_OUTSIDE_VOCABULARY",
    "DISPOSITION_REASONS",
    "DISPOSITION_SCHEMA",
    "IndeterminateRecord",
    "NEW_CODES",
    "OUTCOMES",
    "READER_OUTCOME_UNKNOWN",
    "READER_ROW_DUPLICATE",
    "READER_ROW_INVALID",
    "READER_SCHEMA",
    "ReaderError",
    "ReadingRow",
    "Readings",
    "RegisteredReading",
    "RowDisposition",
    "read_table",
    "unanswered_coordinates",
]


# --------------------------------------------------------------------- failures

READER_ROW_INVALID = "READER_ROW_INVALID"
READER_ROW_DUPLICATE = "READER_ROW_DUPLICATE"
READER_OUTCOME_UNKNOWN = "READER_OUTCOME_UNKNOWN"

#: Codes this module raises, each with the one-line reason it exists.  Every
#: one is reached by a call site in this module: a declared code nothing can
#: raise is a code no register ever prints, which is what
#: ``test_types.py::test_every_declared_code_is_reached_by_the_package_or_allow_listed``
#: exists to catch.
NEW_CODES: Mapping[str, str] = MappingProxyType({
    READER_ROW_INVALID:
        "a table row is not a mapping carrying a row_key and a resolvable "
        "surface, so there is no declared row to read",
    READER_ROW_DUPLICATE:
        "two rows of one table carry one row_key, so their write-once records "
        "and their trial coordinates would collide inside one directory",
    READER_OUTCOME_UNKNOWN:
        "the trial answered with an outcome outside trial.OUTCOMES, so the "
        "guard's answer cannot be read and guessing at it would mint a "
        "standing nothing decided",
})


class ReaderError(types.LoopError):
    """A declared refusal from the reader layer; ``.code`` is the receipt token."""


# --------------------------------------------------------------------- vocabulary

#: The content ``schema`` name of every record this module authors.
READER_SCHEMA = "minireason.loop.reader.v1"

#: The ``record`` token of a disposition, which is what W1-OBLIGATIONS' o1 and
#: o4 predicates read.  Mirrored rather than imported, so W4 adds no import
#: edge to W1-OBLIGATIONS; ``tests/loop/test_reader.py`` asserts the mirror.
DISPOSITION_SCHEMA = "disposition"

#: The row-level endings this module can write.  ``critic-none`` and
#: ``unresolved:outside-vocabulary`` are §2.3's two short-circuits; the other
#: two name a row that was read and did not sustain, and a coordinate the
#: record shows was claimed and never answered (§4.3).
DISPOSITION_CRITIC_NONE = "critic-none"
DISPOSITION_OUTSIDE_VOCABULARY = "unresolved:outside-vocabulary"
DISPOSITION_NOT_SUSTAINED = "not-sustained"
DISPOSITION_INDETERMINATE = "INDETERMINATE"

DISPOSITION_REASONS: tuple[str, ...] = (
    DISPOSITION_CRITIC_NONE,
    DISPOSITION_OUTSIDE_VOCABULARY,
    DISPOSITION_NOT_SUSTAINED,
    DISPOSITION_INDETERMINATE,
)

#: W3-TRIAL's own outcome vocabulary, imported and never retyped.  A token
#: outside it is :data:`READER_OUTCOME_UNKNOWN`, not a guess.
OUTCOMES: tuple[str, ...] = trial.OUTCOMES


# --------------------------------------------------------------------- rows


@dataclass(frozen=True)
class ReadingRow:
    """One pre-registered reading row: a key, a surface, and the cell it attacks.

    ``row_key`` is the reading-set spelling the plan declares and the name of
    the row's own write-once records directory; ``surface`` is the resolvable
    material surface (W1-SURFACE), handed to the trial uninspected; ``cell`` is
    the cell whose unresolved default a surviving reading refutes, defaulting
    to the row key.  The relation is **not** here: the critic nominates it and
    G4 is its only gate.
    """

    row_key: str
    surface: Any
    cell: graph.CellKey | None = None

    @property
    def key(self) -> graph.CellKey:
        """The cell this row's reading attacks - the explicit key, else the row."""
        return self.cell if self.cell is not None else graph.CellKey(self.row_key)

    @classmethod
    def coerce(cls, value: "ReadingRow | Mapping[str, Any]") -> "ReadingRow":
        if isinstance(value, ReadingRow):
            return value
        if isinstance(value, Mapping):
            row_key = value.get("row_key") or value.get("key")
            if not isinstance(row_key, str) or not row_key.strip():
                raise ReaderError(
                    READER_ROW_INVALID, "a reading row needs a non-empty row_key")
            surface = value.get("surface")
            if surface is None:
                raise ReaderError(
                    READER_ROW_INVALID,
                    f"row {row_key}: no resolvable surface was supplied")
            cell = value.get("cell")
            try:
                key = graph.CellKey.coerce(cell) if cell is not None else None
            except types.LoopError as exc:
                raise ReaderError(
                    READER_ROW_INVALID, f"row {row_key}: {exc.detail}") from exc
            return cls(row_key=row_key, surface=surface, cell=key)
        raise ReaderError(READER_ROW_INVALID, f"{type(value).__name__} is not a row")


# --------------------------------------------------------------------- records


@dataclass(frozen=True)
class BlockRecord:
    """One guard block, at the grain o4's ``blocks_named`` reads it.

    The fields are :class:`trial.Block`'s own - ``code``, ``check``,
    ``detail`` and the two blob refs with their digests - carried across
    without renaming, so a block in the reader's register and a block on the
    trial's result are one fact spelled one way.  Both refs are empty on a
    ``blocked:constitution``, because nothing was dispatched.
    """

    row_key: str
    cell: str
    code: str
    check: str
    detail: str = ""
    prompt_ref_path: str = ""
    raw_ref_path: str = ""
    prompt_sha: str | None = None
    raw_sha: str | None = None

    @classmethod
    def of(cls, row_key: str, cell: str, block: trial.Block) -> "BlockRecord":
        return cls(
            row_key=row_key,
            cell=cell,
            code=block.code,
            check=block.check,
            detail=block.detail,
            prompt_ref_path=block.prompt_ref_path,
            raw_ref_path=block.raw_ref_path,
            prompt_sha=block.prompt_sha,
            raw_sha=block.raw_sha,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": READER_SCHEMA,
            "record": DISPOSITION_SCHEMA,
            "key": self.row_key,
            "cell": self.cell,
            "reason": self.code,
            "check": self.check,
            "detail": self.detail,
            "prompt_ref": {"path": self.prompt_ref_path, "sha256": self.prompt_sha},
            "raw_ref": {"path": self.raw_ref_path, "sha256": self.raw_sha},
        }


@dataclass(frozen=True)
class IndeterminateRecord:
    """A coordinate the record shows was claimed and never answered.

    §4.3's spelling: a coordinate with a request or attempt but no response is
    ``INDETERMINATE`` - its own register, beside the blocks, and never folded
    into ``unread``.  A row carrying one is **not re-sent**: a call may have
    been billed, and re-entering it would be the retry §4.4 forbids.
    """

    row_key: str
    coordinate: str
    detail: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": READER_SCHEMA,
            "record": DISPOSITION_SCHEMA,
            "key": self.row_key,
            "reason": DISPOSITION_INDETERMINATE,
            "coordinate": self.coordinate,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class RowDisposition:
    """A row-level ending, named by the reason o1 reads.

    ``text`` carries the critic's ``outside_vocabulary`` verbatim where that is
    the reason: the escape preserves the criticism's own words, because they
    are the record of why the closed vocabulary refused service (§2.3 D6).
    """

    row_key: str
    cell: str
    reason: str
    text: str = ""

    def as_dict(self) -> dict[str, Any]:
        body: dict[str, Any] = {
            "schema": READER_SCHEMA,
            "record": DISPOSITION_SCHEMA,
            "key": self.row_key,
            "cell": self.cell,
            "reason": self.reason,
        }
        if self.text:
            body[standard.OUTSIDE_VOCABULARY_FIELD] = self.text
        return body


@dataclass(frozen=True)
class RegisteredReading:
    """A surviving reading's identity: which relation, read under which seat,
    and every artifact id its registration minted.

    ``seat`` and ``roles`` are the trial's own - this module neither spells nor
    normalises them - so ``graph.validity_nodes_for_seat`` and every audit
    warrant target read the string the call record carries.
    """

    row_key: str
    cell: str
    relation: str
    seat: str
    roles: Mapping[str, str]
    ids: graph.ReadingIds

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": READER_SCHEMA,
            "row_key": self.row_key,
            "cell": self.cell,
            "relation": self.relation,
            "seat": self.seat,
            "roles": dict(self.roles),
            "ids": self.ids.as_dict(),
        }


@dataclass(frozen=True)
class Readings:
    """What one pass over the reading table produced, in five registers.

    ``planned`` and ``dispatched`` are the PREFLIGHT accounting identity
    (§4.1 S1): rows the declared table asked for, rows actually sent.  They are
    reported as an identity, never as a ratio and never as a rate; on a first
    pass over the offline fixture they are equal by construction, and they
    differ exactly where a claimed-and-unanswered coordinate refused a re-send.

    ``unread`` is every cell open in the graph that this pass registered no
    reading for - the completeness W3-REPORT's trichotomy rests on.
    """

    blocks: tuple[BlockRecord, ...] = ()
    registered: tuple[RegisteredReading, ...] = ()
    indeterminate: tuple[IndeterminateRecord, ...] = ()
    dispositions: tuple[RowDisposition, ...] = ()
    unread: frozenset[str] = frozenset()
    planned: int = 0
    dispatched: int = 0

    def as_dict(self) -> dict[str, Any]:
        """The whole pass as a record - G12-clean before it is returned."""
        record = {
            "schema": READER_SCHEMA,
            "blocks": [record.as_dict() for record in self.blocks],
            "registered": [record.as_dict() for record in self.registered],
            "indeterminate": [record.as_dict() for record in self.indeterminate],
            "dispositions": [record.as_dict() for record in self.dispositions],
            "unread": sorted(self.unread),
            "planned": self.planned,
            "dispatched": self.dispatched,
            "planned_equals_dispatched": self.planned == self.dispatched,
        }
        contracts.assert_no_scoring_keys(record)
        return record


# --------------------------------------------------------------------- helpers


def unanswered_coordinates(records_dir: Path | str) -> tuple[str, ...]:
    """Every coordinate under ``records_dir`` that was claimed and never answered.

    W2-ROLES claims a coordinate by creating its directory and its ``provider``
    subdirectory *before* anything can be sent, and writes the call record into
    it only once the provider has answered.  A claim without a call record is
    therefore §4.3's "a request or attempt but no response".

    W1-STEPS' :func:`~minireason.loop.steps.scan_coordinates` does **not** serve
    here and is deliberately not called: it reads a
    ``requests/``-``attempts/``-``responses/`` tree, which is runner v2's
    dispatch layout, while the reading arm's records are W2-ROLES'
    ``<key>/<role>/`` claims.  The two layouts are not the same tree, so the
    reading arm's ``INDETERMINATE`` list has to be read off the layout that
    actually holds it (WAVE4-INTERFACE §8).

    The record kind is :data:`roles.RECORD_KIND` under
    :data:`roles.RECORD_FIELD` - imported, never retyped - so a claim is
    identified by what W2-ROLES wrote and not by a filename this module guessed.
    """

    root = Path(records_dir)
    if not root.is_dir():
        return ()
    found: list[str] = []
    for provider_dir in sorted(root.rglob("provider")):
        if not provider_dir.is_dir():
            continue
        claim = provider_dir.parent
        if _has_call_record(claim):
            continue
        found.append(str(claim.relative_to(root)))
    return tuple(found)


def _has_call_record(claim: Path) -> bool:
    for candidate in sorted(claim.glob("*.json")):
        try:
            body = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(body, Mapping) and body.get(roles.RECORD_FIELD) == roles.RECORD_KIND:
            return True
    return False


def _write_record(root: Path, row_key: str, name: str, body: Mapping[str, Any]) -> None:
    """Write one record write-once under ``<records_dir>/<row_key>/<name>``.

    The fencing and the write-once discipline are W0-CUSTODY's - one owner,
    imported here, never re-implemented.
    """
    record = dict(body)
    contracts.assert_no_scoring_keys(record)   # G12, before anything is written
    directory = custody.fenced(root, row_key)
    directory.mkdir(parents=True, exist_ok=True)
    custody.write_new(custody.fenced(directory, name), record)


def _outside_vocabulary_text(result: trial.TrialResult) -> str:
    """The critic's preserved text, off the critic's own output.

    D6's "text preserved" is preserved where the contract put it:
    ``CriticOutput.outside_vocabulary``.  A result that reached
    ``OUTCOME_UNRESOLVED`` always carries a critic, because G4 runs after G1.
    """
    critic = result.critic
    text = getattr(critic, standard.OUTSIDE_VOCABULARY_FIELD, "") if critic else ""
    return text if isinstance(text, str) else ""


# --------------------------------------------------------------------- the drive


def read_table(
    harness: Any,
    table: Iterable[ReadingRow | Mapping[str, Any]],
    standard_body: Any,
    seats: Any,
    config: Any,
    records_dir: Path | str,
    *,
    trial_runner: Callable[..., trial.TrialResult] = trial.run_trial,
    registered_by: Callable[..., graph.ReadingIds] = graph.register_reading,
    provider_factory: Any = None,
    reopen_reason: str | None = None,
    framing: Any = None,
) -> Readings:
    """Drive the guarded trial over every pre-registered row; register the survivors.

    Per row, in order: coerce the row; refuse a duplicate row key; read the
    row's own records directory and, if a coordinate there was claimed and
    never answered, report it ``INDETERMINATE`` and **do not dispatch**; else
    run one guarded trial; then exactly one of the following, by
    ``TrialResult.outcome``.

    - :data:`trial.OUTCOME_NO_TRIAL` - the critic answered ``none``.  The row
      ended at one call, ``blocks`` is empty, the cell keeps its grounded
      default, and the disposition is ``critic-none``.  (§2.3)
    - :data:`trial.OUTCOME_UNRESOLVED` - a non-empty ``outside_vocabulary``.
      The disposition is ``unresolved:outside-vocabulary`` with the critic's
      text preserved verbatim, **and** the guard's own
      ``blocked:outside-vocabulary`` lands in ``blocks``: the row is both an
      ending o1 reads and a block o4 counts, and the two registers are kept
      apart rather than one standing in for the other.  (§2.3 D6, G4)
    - :data:`trial.OUTCOME_BLOCKED` - every block lands in ``blocks`` with its
      reason code, check and both blob refs; nothing registers.
    - :data:`trial.OUTCOME_NOT_SUSTAINED` - the ensemble answered and did not
      sustain.  Nothing registers; the disposition records that the row was
      read, because "read and not sustained" is not "unread".
    - :data:`trial.OUTCOME_SUSTAINED` - the trial's own ``reading`` is entered
      through ``registered_by``.  Two survivors of one cell are two
      registrations and the cell reads ``contested`` from the graph's
      adjudication; they are never averaged.

    Every record is written write-once under ``records_dir`` before the
    corresponding value is returned, so what a caller carries is what custody
    holds.
    """

    root = Path(records_dir)
    root.mkdir(parents=True, exist_ok=True)

    blocks: list[BlockRecord] = []
    registered: list[RegisteredReading] = []
    indeterminate: list[IndeterminateRecord] = []
    dispositions: list[RowDisposition] = []
    read_cells: set[str] = set()
    seen: set[str] = set()
    planned = 0
    dispatched = 0

    for raw_row in table:
        row = ReadingRow.coerce(raw_row)
        if row.row_key in seen:
            raise ReaderError(
                READER_ROW_DUPLICATE,
                f"{row.row_key} appears twice in one table; two trials of one "
                "cell are two rows with two keys and two records directories")
        seen.add(row.row_key)
        planned += 1

        cell = row.key
        row_records = custody.fenced(root, row.row_key)
        stale = unanswered_coordinates(row_records)
        if stale:
            for coordinate in stale:
                record = IndeterminateRecord(
                    row.row_key, coordinate,
                    detail="a coordinate was claimed and never answered; a call "
                           "may have been billed, so it is never re-sent")
                _write_record(
                    root, row.row_key,
                    f"indeterminate-{len(indeterminate):02d}.json", record.as_dict())
                indeterminate.append(record)
            continue

        row_records.mkdir(parents=True, exist_ok=True)
        result = trial_runner(
            harness, row.surface, standard_body, seats, config,
            mode=standard.MODE_ABSOLUTE,
            key=cell,
            records_dir=row_records,
            provider_factory=provider_factory,
            reopen_reason=reopen_reason,
            framing=framing,
        )
        dispatched += 1

        outcome = getattr(result, "outcome", None)
        if outcome not in OUTCOMES:
            raise ReaderError(
                READER_OUTCOME_UNKNOWN,
                f"{row.row_key}: the trial answered {outcome!r}, outside {OUTCOMES}")

        for block in result.blocks:
            record = BlockRecord.of(row.row_key, cell.token, block)
            _write_record(root, row.row_key, f"block-{len(blocks):02d}.json",
                          record.as_dict())
            blocks.append(record)

        if outcome == trial.OUTCOME_UNRESOLVED:
            disposition = RowDisposition(
                row.row_key, cell.token, DISPOSITION_OUTSIDE_VOCABULARY,
                text=_outside_vocabulary_text(result))
        elif outcome == trial.OUTCOME_NO_TRIAL:
            disposition = RowDisposition(
                row.row_key, cell.token, DISPOSITION_CRITIC_NONE)
        elif outcome == trial.OUTCOME_NOT_SUSTAINED:
            disposition = RowDisposition(
                row.row_key, cell.token, DISPOSITION_NOT_SUSTAINED)
        else:
            disposition = None

        if disposition is not None:
            _write_record(root, row.row_key, "disposition.json", disposition.as_dict())
            dispositions.append(disposition)
            continue

        if outcome == trial.OUTCOME_BLOCKED:
            continue

        # OUTCOME_SUSTAINED: the guard's own survivor, entered as it stands.
        reading = result.reading
        if reading is None:
            raise ReaderError(
                READER_OUTCOME_UNKNOWN,
                f"{row.row_key}: a sustained trial carries a ReadingResult and "
                "this one carries none")
        ids = registered_by(harness, reading, result.standard_id)
        entry = RegisteredReading(
            row_key=row.row_key,
            cell=cell.token,
            relation=reading.relation,
            seat=reading.seat,
            roles=dict(reading.roles),
            ids=ids,
        )
        _write_record(root, row.row_key, "reading.json", entry.as_dict())
        registered.append(entry)
        read_cells.add(cell.token)

    return Readings(
        blocks=tuple(blocks),
        registered=tuple(registered),
        indeterminate=tuple(indeterminate),
        dispositions=tuple(dispositions),
        unread=_unread_cells(harness, read_cells),
        planned=planned,
        dispatched=dispatched,
    )


def _unread_cells(harness: Any, read_cells: set[str]) -> frozenset[str]:
    """Every open cell this pass registered no reading for (WAVE3 question 3).

    Read off the graph's own cell-open artifacts rather than off the table, so
    a cell the pre-registered reading set never named is still named unread -
    which is the completeness the ceiling's unread/unresolved/machine-unresolved
    trichotomy rests on, and the half of PR-13 a program can carry.
    """
    standings = graph.cell_standings(harness)
    return frozenset(
        standing.key for standing in standings if standing.key not in read_cells
    )
