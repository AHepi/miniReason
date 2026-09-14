"""W4-READER: the reading table driven over the real guard, offline.

Every class is named for one clause of the W4-READER acceptance list, and every
test in it is one reading of that clause.

**The guard is real.**  The draft this file replaces injected a fake
``TrialResult`` and never ran W3-TRIAL at all, so no test of it could see a
guard block, a vocabulary refusal or a registration the graph would accept.
Here ``read_table`` is driven with its **default** ``trial_runner`` -
:func:`minireason.loop.trial.run_trial` - over the same scripted
``OfflineProvider`` fixture ``tests/loop/test_trial.py`` and
``tests/loop/test_roles.py`` use, with the socket layer removed from under
every call.  The one seam the suite binds is ``provider_factory``, which is
the seam W6-DRYRUN itself binds: the guard runs, the packs render, the call
records are spent write-once, and only the transport is offline.

Two tests inject a runner: one asserts the seam exists for the dry run, and
one hands back a *real* ``TrialResult`` with its outcome field replaced, to
reach the one refusal a well-formed guard can never produce.  Neither
bypasses a guard: both start from a result the real guard built.
"""
from __future__ import annotations

import ast
import contextlib
import dataclasses
import json
import shutil
import socket
import tempfile
import unittest
from pathlib import Path

from minireason import provider_openai_compat as transport
from minireason.loop import contracts as C
from minireason.loop import graph as G
from minireason.loop import obligations as OB
from minireason.loop import reader as R
from minireason.loop import seats
from minireason.loop import standard as STD
from minireason.loop import surface as S
from minireason.loop import trial as T
from minireason.loop import types as loop_types

MODULE = Path(R.__file__).resolve()


# --------------------------------------------------------------------------
# The socket guard, captured-and-restored once
# --------------------------------------------------------------------------


class _SocketsUsed(AssertionError):
    """Raised the instant anything in the process reaches for a socket."""


_PRISTINE = (socket.socket, socket.create_connection, transport._open)


def _refuse_socket(*args, **kwargs):
    raise _SocketsUsed("a test opened a socket")


@contextlib.contextmanager
def no_sockets():
    socket.socket = socket.create_connection = transport._open = _refuse_socket
    try:
        yield
    finally:
        socket.socket, socket.create_connection, transport._open = _PRISTINE


# --------------------------------------------------------------------------
# The material (hand-built; the surface is W1-SURFACE's build of it)
# --------------------------------------------------------------------------

REFERRING = (
    "The objection reads the account second record and carries its terms "
    "into a narrower claim about cadence."
)
TARGET = (
    "Written confirmation settles what an agreement meant, so the written "
    "line controls the later disagreement."
)
QUOTE = "the written line controls the later disagreement"
CASE = "The objection takes up the account claim and keeps its central term."
ANSWER = "The juxtaposition shows the term reused, and that is all it shows."
POINT = "that is all it shows"
PARA_POINT = "Restated plainly"

#: A second material, so a second row reads a second cell.
REFERRING_B = (
    "The reply revisits the earlier ruling and narrows the ground it stands on."
)
TARGET_B = (
    "An undertaking once accepted binds the party that gave it, whatever "
    "later convenience suggests."
)
QUOTE_B = "whatever later convenience suggests"


def build_row(referring: str = REFERRING, target: str = TARGET) -> dict:
    coordinate = {"problem": "synth", "arm": "mini_fcl", "cycle": 1,
                  "node": "objection"}
    other = dict(coordinate, node="account")
    return {
        "referring_coordinate": coordinate,
        "referring_coordinate_key": "synth/mini_fcl/cycle01/objection",
        "referring_record_id": "o2",
        "referring_record_verbatim": referring,
        "referring_record_source_span": [0, len(referring)],
        "ref_field": "depends",
        "ref_verbatim": "p.objection.0#a2",
        "ref_grain": "record",
        "target_coordinate": other,
        "target_coordinate_key": "synth/mini_fcl/cycle01/account",
        "target_record_id": "a2",
        "target_record_verbatim": target,
        "target_record_source_span": [0, len(target)],
        "referring_body_passages": [],
        "resolver_notes": [],
    }


def build_config() -> loop_types.LoopConfig:
    return loop_types.LoopConfig.from_mapping(
        {
            "run_id": "reader-test",
            "study": "synthetic",
            "occurrences": ["occ"],
            "runner": "tools/multicycle_commitment_study_multi_v2.py",
            "cycle_budget": 1,
            "max_calls": 100,
            "reading_set": ["row-a"],
            "obligations_path": "obligations.json",
            "graph_root": "graph",
            "reopen_reasons": list(STD.REOPEN_REASONS),
            "audit": {
                "period": 4,
                "judge_err_max": 0.2,
                "streak_max": 3,
                "judge_err_max_account": "one wrong anchor of five is one too many",
                "streak_max_account": "three guard blocks in a row stop one role",
            },
        }
    )


#: Key-env NAMES only, never values, and deliberately this wave's own: runner
#: v2's ``key_gate`` registry is process-wide and refuses a second cap for one
#: credential, so a fixture that reused ``SYNTHETIC_ALPHA_KEY`` (cap 2 in
#: ``loop.synthetic``) at cap 5 would make ``tests/loop/test_roles.py`` raise
#: CONCURRENCY_LIMIT_CONFLICT depending on discovery order.
def build_registry() -> dict:
    def endpoint(name: str, family: str, key_env: str) -> transport.Endpoint:
        return transport.Endpoint(
            name=name,
            base_url=f"https://{name.split('/')[-1]}.synthetic.invalid/v1",
            model=f"model-{name.split('/')[-1]}",
            key_env=key_env,
            family=family,
            chat_path="/chat/completions",
            native=False,
            max_concurrency=5,
            timeout_seconds=120,
        )

    entries = [
        endpoint("synthetic/alpha-1", "alpha-family", "W4_ALPHA_KEY"),
        endpoint("synthetic/alpha-2", "alpha-family", "W4_ALPHA_KEY"),
        endpoint("synthetic/beta", "beta-family", "W4_BETA_KEY"),
        endpoint("synthetic/gamma", "gamma-family", "W4_GAMMA_KEY"),
        endpoint("synthetic/delta", "delta-family", "W4_DELTA_KEY"),
        endpoint("synthetic/epsilon", "epsilon-family", "W4_EPSILON_KEY"),
    ]
    return {e.name: e for e in entries}


class Scripted:
    """The provider factory: one reply queue per ``(role, coordinate)``.

    W2-ROLES builds a fresh provider per call, so a provider handed the whole
    reply list would replay it from index 0 every time and both judge seats
    would read the first reply.  The queue is consumed **across** calls, which
    is what lets a scripted dissent reach the second seat.
    """

    def __init__(self, scripts: dict) -> None:
        self.scripts = {key: list(replies) for key, replies in scripts.items()}
        self.calls: list = []

    def __call__(self, role, coordinate, records_dir, *, seat=None, endpoint=None):
        self.calls.append((role, coordinate))
        queue = self.scripts.get((role, coordinate))
        if queue is None:
            raise AssertionError(f"unscripted call {role!r} {coordinate!r}")
        if not queue:
            raise AssertionError(
                f"the script for {role!r} {coordinate!r} is exhausted; this "
                "call was not planned for")
        return transport.OfflineProvider(
            endpoint, records_dir, [json.dumps(queue.pop(0))]
        )


def critic_output(case: str = CASE, quote: str = QUOTE, relation: str = "retains",
                  outside: str = "") -> dict:
    return {
        "relation": relation,
        "passage_quote": quote,
        "role_bindings": {"target": "a2", "defect": "none alleged",
                          "grounds": quote, "bearing": "the row settles"},
        "case": case,
        C.OUTSIDE_VOCABULARY_FIELD: outside,
    }


def defender_output(answer: str = ANSWER) -> dict:
    return {"answer": answer, "concedes": False}


def judge_output(point: str = POINT, sustained: bool = True,
                 note: str = "noted") -> dict:
    return {"sustained": sustained, "decisive_point": point, "reading_note": note}


def variator_output(*paraphrases: str) -> dict:
    return {"paraphrases": list(paraphrases)}


def paraphrase_of(case: str, answer: str, *, quote: str = QUOTE,
                  tag: str = "") -> str:
    text = f"{case} Restated plainly. {answer} Restated likewise."
    text += f" The citation still reads as: {quote}"
    if tag:
        text += f" {tag}"
    return text


def clean_script(cell: str, *, case: str = CASE, quote: str = QUOTE,
                 answer: str = ANSWER, point: str = POINT,
                 relation: str = "retains", repeats: int = 1) -> dict:
    """The whole script of one clean sustained trial of ``cell``.

    ``repeats`` multiplies every queue, so one cell can carry more than one
    trial - which is how "multiple nominated relations are separate trials"
    is exercised without two cells pretending to be one.
    """

    def times(*replies):
        return [dict(reply) for _ in range(repeats) for reply in replies]

    return {
        ("critic", cell): times(critic_output(case, quote, relation)),
        ("defender", cell): times(defender_output(answer)),
        ("judge", cell): times(judge_output(point), judge_output(point)),
        ("judge", cell + "#order-swapped"): times(judge_output(point),
                                                  judge_output(point)),
        ("variator", cell): times(variator_output(
            paraphrase_of(case, answer, quote=quote),
            paraphrase_of(case, answer, quote=quote, tag="Again."),
        )),
        ("judge", cell + "#paraphrase-0"): times(judge_output(point=PARA_POINT),
                                                 judge_output(point=PARA_POINT)),
        ("judge", cell + "#paraphrase-1"): times(judge_output(point=PARA_POINT),
                                                 judge_output(point=PARA_POINT)),
    }


class ReaderCase(unittest.TestCase):
    """One temp run: a graph with the standard in it, two open cells, two rows."""

    CELL = "row-a"
    CELL_B = "row-b"

    def setUp(self) -> None:
        super().setUp()
        self.tmp = Path(tempfile.mkdtemp(prefix="loop-reader-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        prepared = T.open_trial_harness(self.tmp / "graph", self.CELL)
        self.harness = prepared.harness
        self.standard_id = prepared.standard_id
        G.open_cells(self.harness, [G.CellKey(self.CELL_B)])
        self.surface = S.build_surface(build_row())
        self.surface_b = S.build_surface(build_row(REFERRING_B, TARGET_B))
        self.config = build_config()
        self.plan = seats.select_seats(build_registry())
        self.records = self.tmp / "readings"

    # -- drivers ----------------------------------------------------------

    def rows(self, *keys: str) -> list[dict]:
        table = []
        for key in keys or (self.CELL,):
            surface = self.surface_b if key == self.CELL_B else self.surface
            table.append({"row_key": key, "surface": surface})
        return table

    def drive(self, table, factory, **kwargs) -> R.Readings:
        with no_sockets():
            return R.read_table(
                self.harness, table, STD.STANDARD_BODY, self.plan, self.config,
                self.records, provider_factory=factory, **kwargs)

    def clean(self, *cells: str, **kwargs) -> Scripted:
        """The clean script for each named cell, quoting that cell's own material.

        ``row-b`` reads a second material, so its critic must quote a passage
        that resolves uniquely *there*: a script that quoted row-a's passage
        would block on G2(a), which is the guard working and not a fixture.
        """
        script: dict = {}
        for cell in cells or (self.CELL,):
            per_cell = dict(kwargs)
            if cell == self.CELL_B:
                per_cell.setdefault("quote", QUOTE_B)
            script.update(clean_script(cell, **per_cell))
        return Scripted(script)

    def with_override(self, cell: str, *overrides: dict, **kwargs) -> Scripted:
        script = clean_script(cell, **kwargs)
        for override in overrides:
            script.update({k: list(v) for k, v in override.items()})
        return Scripted(script)


# --------------------------------------------------------------------------
# Clause 1 - only guarded readings reach the graph
# --------------------------------------------------------------------------


class OnlyGuardedReadingsReachTheGraph(ReaderCase):
    """W4-READER acceptance clause 1, over the real guard."""

    def test_a_sustained_trial_is_registered_and_the_cell_reads(self):
        out = self.drive(self.rows(), self.clean())
        self.assertEqual(len(out.registered), 1)
        self.assertEqual(out.blocks, ())
        self.assertEqual(G.cell_state(self.harness, self.CELL), G.READ)

    def test_the_registered_reading_is_the_trials_own_not_a_rebuild(self):
        out = self.drive(self.rows(), self.clean())
        entry = out.registered[0]
        self.assertEqual(entry.relation, "retains")
        # the ids the graph minted are all present, the warrant included
        for field in ("reading", "soundness", "bearing", "transcript", "warrant"):
            self.assertTrue(getattr(entry.ids, field))

    def test_a_referential_integrity_block_registers_nothing(self):
        # A passage_quote that is nowhere in the material: G2(a) blocks.
        factory = self.with_override(
            self.CELL,
            {("critic", self.CELL): [critic_output(quote="no such passage here")]},
        )
        out = self.drive(self.rows(), factory)
        self.assertEqual(out.registered, ())
        self.assertEqual([b.code for b in out.blocks],
                         [T.REFERENTIAL_INTEGRITY_BLOCK])
        self.assertEqual(out.blocks[0].check, T.G2A_UNIQUENESS)
        self.assertEqual(G.cell_state(self.harness, self.CELL), G.UNRESOLVED)

    def test_an_ensemble_split_blocks_and_registers_nothing(self):
        factory = self.with_override(
            self.CELL,
            {("judge", self.CELL): [judge_output(), judge_output(sustained=False)],
             ("judge", self.CELL + "#order-swapped"): [
                 judge_output(), judge_output(sustained=False)]},
        )
        out = self.drive(self.rows(), factory)
        self.assertEqual(out.registered, ())
        self.assertEqual([b.code for b in out.blocks], [T.ENSEMBLE_SPLIT_BLOCK])
        self.assertEqual(G.cell_state(self.harness, self.CELL), G.UNRESOLVED)

    def test_every_block_carries_its_reason_code_and_both_blob_refs(self):
        factory = self.with_override(
            self.CELL,
            {("critic", self.CELL): [critic_output(quote="no such passage here")]},
        )
        out = self.drive(self.rows(), factory)
        block = out.blocks[0]
        self.assertIn(block.code, loop_types.BLOCK_CODES)
        self.assertTrue(block.prompt_ref_path)
        self.assertTrue(block.raw_ref_path)

    def test_blocks_are_written_write_once_under_the_row_directory(self):
        factory = self.with_override(
            self.CELL,
            {("critic", self.CELL): [critic_output(quote="no such passage here")]},
        )
        self.drive(self.rows(), factory)
        written = sorted((self.records / self.CELL).glob("block-*.json"))
        self.assertEqual(len(written), 1)
        body = json.loads(written[0].read_text())
        self.assertEqual(body["record"], R.DISPOSITION_SCHEMA)
        self.assertEqual(body["reason"], T.REFERENTIAL_INTEGRITY_BLOCK)

    def test_a_not_sustained_trial_registers_nothing_and_says_it_was_read(self):
        factory = self.with_override(
            self.CELL,
            {("judge", self.CELL): [judge_output(sustained=False),
                                    judge_output(sustained=False)],
             ("judge", self.CELL + "#order-swapped"): [
                 judge_output(sustained=False), judge_output(sustained=False)]},
        )
        out = self.drive(self.rows(), factory)
        self.assertEqual(out.registered, ())
        self.assertEqual(out.blocks, ())
        self.assertEqual([d.reason for d in out.dispositions],
                         [R.DISPOSITION_NOT_SUSTAINED])
        self.assertEqual(G.cell_state(self.harness, self.CELL), G.UNRESOLVED)


# --------------------------------------------------------------------------
# Clause 2 - a critic answering none ends the row at one call
# --------------------------------------------------------------------------


class ACriticAnsweringNoneEndsTheRowAtOneCall(ReaderCase):
    """W4-READER acceptance clause 2, over the real guard."""

    def none_factory(self) -> Scripted:
        return Scripted({("critic", self.CELL): [critic_output(relation="none")]})

    def test_exactly_one_call_is_dispatched(self):
        factory = self.none_factory()
        self.drive(self.rows(), factory)
        self.assertEqual(factory.calls, [("critic", self.CELL)])

    def test_nothing_registers_and_the_cell_stays_unresolved(self):
        out = self.drive(self.rows(), self.none_factory())
        self.assertEqual(out.registered, ())
        self.assertEqual(out.blocks, ())
        self.assertEqual(G.cell_state(self.harness, self.CELL), G.UNRESOLVED)

    def test_the_disposition_is_the_reason_o1_reads(self):
        out = self.drive(self.rows(), self.none_factory())
        self.assertEqual([d.reason for d in out.dispositions],
                         [R.DISPOSITION_CRITIC_NONE])
        body = json.loads(
            (self.records / self.CELL / "disposition.json").read_text())
        self.assertEqual(body["reason"], R.DISPOSITION_CRITIC_NONE)
        self.assertEqual(body["record"], R.DISPOSITION_SCHEMA)

    def test_a_none_is_not_a_block_and_prints_in_no_block_register(self):
        out = self.drive(self.rows(), self.none_factory())
        self.assertEqual(out.blocks, ())
        self.assertNotIn(R.DISPOSITION_CRITIC_NONE, loop_types.BLOCK_CODES)


# --------------------------------------------------------------------------
# Clause 3 - a non-empty outside_vocabulary forces unresolved, text preserved
# --------------------------------------------------------------------------


class OutsideVocabularyForcesUnresolvedWithTheTextPreserved(ReaderCase):
    """W4-READER acceptance clause 3, over the real guard (G4/D6)."""

    TEXT = "the objection neither retains nor repairs: it re-sites the ground"

    def escape_factory(self) -> Scripted:
        return Scripted({
            ("critic", self.CELL): [critic_output(relation="none",
                                                  outside=self.TEXT)],
        })

    def test_the_row_ends_unresolved_and_nothing_registers(self):
        out = self.drive(self.rows(), self.escape_factory())
        self.assertEqual(out.registered, ())
        self.assertEqual(G.cell_state(self.harness, self.CELL), G.UNRESOLVED)

    def test_the_text_is_preserved_verbatim_in_the_returned_record(self):
        out = self.drive(self.rows(), self.escape_factory())
        self.assertEqual([d.reason for d in out.dispositions],
                         [R.DISPOSITION_OUTSIDE_VOCABULARY])
        self.assertEqual(out.dispositions[0].text, self.TEXT)

    def test_the_text_is_preserved_verbatim_on_disk(self):
        self.drive(self.rows(), self.escape_factory())
        body = json.loads(
            (self.records / self.CELL / "disposition.json").read_text())
        self.assertEqual(body[STD.OUTSIDE_VOCABULARY_FIELD], self.TEXT)

    def test_the_guards_own_block_is_kept_beside_the_disposition(self):
        # Two registers, one row: o1 reads the ending, o4 reads the code.
        out = self.drive(self.rows(), self.escape_factory())
        self.assertEqual([b.code for b in out.blocks],
                         [T.OUTSIDE_VOCABULARY_BLOCK])
        self.assertEqual(out.blocks[0].check, T.G4_VOCABULARY)

    def test_no_call_past_the_critic_is_made(self):
        factory = self.escape_factory()
        self.drive(self.rows(), factory)
        self.assertEqual(factory.calls, [("critic", self.CELL)])


# --------------------------------------------------------------------------
# Clause 4 - separate trials, two survivors contested, never averaged
# --------------------------------------------------------------------------


class MultipleNominationsAreSeparateTrialsAndTwoSurvivorsAreContested(ReaderCase):
    """W4-READER acceptance clause 4, over the real guard."""

    ROW_1 = "row-a#n1"
    ROW_2 = "row-a#n2"

    def two_rows(self) -> list[dict]:
        return [{"row_key": self.ROW_1, "surface": self.surface, "cell": self.CELL},
                {"row_key": self.ROW_2, "surface": self.surface, "cell": self.CELL}]

    def two_nominations(self) -> Scripted:
        """One cell, two rows, two nominated relations, both sustained."""
        first = clean_script(self.CELL, relation="retains")
        second = clean_script(self.CELL, relation="re-deploys")
        merged = {key: list(first[key]) + list(second[key]) for key in first}
        return Scripted(merged)

    def test_two_rows_on_one_cell_are_two_trials(self):
        factory = self.two_nominations()
        out = self.drive(self.two_rows(), factory)
        self.assertEqual(out.planned, 2)
        self.assertEqual(out.dispatched, 2)
        self.assertEqual(
            [c for c in factory.calls if c[0] == "critic"],
            [("critic", self.CELL), ("critic", self.CELL)])

    def test_each_trial_spends_its_own_records_directory(self):
        self.drive(self.two_rows(), self.two_nominations())
        self.assertTrue((self.records / self.ROW_1 / self.CELL).is_dir())
        self.assertTrue((self.records / self.ROW_2 / self.CELL).is_dir())

    def test_two_survivors_leave_the_cell_contested_and_never_averaged(self):
        out = self.drive(self.two_rows(), self.two_nominations())
        self.assertEqual(len(out.registered), 2)
        self.assertEqual({e.relation for e in out.registered},
                         {"retains", "re-deploys"})
        self.assertEqual(G.cell_state(self.harness, self.CELL), G.CONTESTED)

    def test_both_reading_ids_stand_and_neither_is_merged(self):
        out = self.drive(self.two_rows(), self.two_nominations())
        ids = {entry.ids.reading for entry in out.registered}
        self.assertEqual(len(ids), 2)

    def test_a_survivor_and_a_block_leave_the_cell_read_not_contested(self):
        first = clean_script(self.CELL, relation="retains")
        second = clean_script(self.CELL)
        second[("critic", self.CELL)] = [critic_output(quote="no such passage")]
        merged = {key: list(first[key]) + list(second.get(key, []))
                  for key in first}
        out = self.drive(self.two_rows(), Scripted(merged))
        self.assertEqual(len(out.registered), 1)
        self.assertEqual(len(out.blocks), 1)
        self.assertEqual(G.cell_state(self.harness, self.CELL), G.READ)

    def test_no_returned_field_combines_the_two_readings(self):
        out = self.drive(self.two_rows(), self.two_nominations())
        body = out.as_dict()
        self.assertEqual(len(body["registered"]), 2)
        for forbidden in ("score", "rank", "average", "mean", "majority",
                          "combined", "aggregate"):
            self.assertNotIn(forbidden, json.dumps(body))


# --------------------------------------------------------------------------
# Clause 5 - planned equals dispatched on the offline fixture
# --------------------------------------------------------------------------


class PlannedEqualsDispatchedOnTheOfflineFixture(ReaderCase):
    """W4-READER acceptance clause 5, over the real guard."""

    def test_two_rows_two_cells_plan_and_dispatch_alike(self):
        out = self.drive(self.rows(self.CELL, self.CELL_B),
                         self.clean(self.CELL, self.CELL_B))
        self.assertEqual(out.planned, 2)
        self.assertEqual(out.dispatched, 2)
        self.assertTrue(out.as_dict()["planned_equals_dispatched"])

    def test_the_pair_is_an_identity_and_never_a_rate(self):
        source = MODULE.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp):
                self.assertNotIsInstance(
                    node.op, (ast.Div, ast.FloorDiv),
                    "the reader computes no ratio of planned to dispatched")

    def test_zero_sockets_were_opened(self):
        # The whole pass runs inside no_sockets(); reaching here is the proof.
        out = self.drive(self.rows(self.CELL, self.CELL_B),
                         self.clean(self.CELL, self.CELL_B))
        self.assertEqual(len(out.registered), 2)

    def test_the_default_runner_is_the_real_guard(self):
        self.assertIs(
            R.read_table.__kwdefaults__["trial_runner"], T.run_trial)
        self.assertIs(
            R.read_table.__kwdefaults__["registered_by"], G.register_reading)

    def test_the_provider_factory_seam_reaches_the_trial(self):
        """The one seam W6-DRYRUN binds: the guard runs, the transport is offline."""
        seen: list = []

        def watching(harness, surface, body, plan, config, **kwargs):
            seen.append(sorted(kwargs))
            return T.run_trial(harness, surface, body, plan, config, **kwargs)

        out = self.drive(self.rows(), self.clean(), trial_runner=watching)
        self.assertEqual(len(out.registered), 1)
        self.assertIn("provider_factory", seen[0])
        self.assertIn("records_dir", seen[0])
        self.assertIn("key", seen[0])
        self.assertIn("mode", seen[0])


# --------------------------------------------------------------------------
# Resume: a claimed-and-unanswered coordinate is INDETERMINATE
# --------------------------------------------------------------------------


class AClaimedCoordinateThatNeverAnsweredIsIndeterminate(ReaderCase):
    """Design §4.3 at coordinate grain: never re-sent, never an absence."""

    def claim_without_a_record(self) -> Path:
        claim = self.records / self.CELL / self.CELL / "critic"
        (claim / "provider").mkdir(parents=True)
        return claim

    def test_the_row_is_not_dispatched(self):
        self.claim_without_a_record()
        factory = Scripted({})
        out = self.drive(self.rows(), factory)
        self.assertEqual(factory.calls, [])
        self.assertEqual(out.planned, 1)
        self.assertEqual(out.dispatched, 0)

    def test_it_is_reported_indeterminate_beside_the_blocks_not_inside_them(self):
        self.claim_without_a_record()
        out = self.drive(self.rows(), Scripted({}))
        self.assertEqual(out.blocks, ())
        self.assertEqual([r.reason_token() if hasattr(r, "reason_token") else
                          r.as_dict()["reason"] for r in out.indeterminate],
                         [R.DISPOSITION_INDETERMINATE])
        self.assertEqual(out.indeterminate[0].coordinate,
                         f"{self.CELL}/critic")

    def test_an_answered_coordinate_is_not_indeterminate(self):
        out = self.drive(self.rows(), self.clean())
        self.assertEqual(out.indeterminate, ())
        self.assertEqual(
            R.unanswered_coordinates(self.records / self.CELL), ())

    def test_the_scan_reads_the_roles_layout_not_the_steps_one(self):
        """W1-STEPS reads requests/attempts/responses; W2-ROLES claims
        ``<key>/<role>/``.  The reading arm's records are the second."""
        from minireason.loop import steps
        self.claim_without_a_record()
        scan = steps.scan_coordinates(self.records / self.CELL)
        self.assertEqual(scan.indeterminate, frozenset())
        self.assertEqual(R.unanswered_coordinates(self.records / self.CELL),
                         (f"{self.CELL}/critic",))


# --------------------------------------------------------------------------
# The unread inventory (WAVE3 open question 3, PR-13's program half)
# --------------------------------------------------------------------------


class TheUnreadInventoryIsEveryOpenCellNothingRead(ReaderCase):
    """W3-REPORT prints ``state.unread``; this is what computes it."""

    def test_a_cell_the_table_never_named_is_still_named_unread(self):
        out = self.drive(self.rows(self.CELL), self.clean(self.CELL))
        self.assertIn(self.CELL_B, out.unread)
        self.assertNotIn(self.CELL, out.unread)

    def test_a_blocked_cell_is_unread_because_nothing_read_it(self):
        factory = self.with_override(
            self.CELL,
            {("critic", self.CELL): [critic_output(quote="no such passage")]},
        )
        out = self.drive(self.rows(), factory)
        self.assertIn(self.CELL, out.unread)

    def test_the_inventory_is_a_set_of_cells_and_carries_no_count(self):
        out = self.drive(self.rows(), self.clean())
        self.assertIsInstance(out.unread, frozenset)
        self.assertEqual(sorted(out.as_dict()["unread"]), sorted(out.unread))


# --------------------------------------------------------------------------
# The seat spelling (WAVE3 open question 4)
# --------------------------------------------------------------------------


class TheSeatSpellingIsTheTrialsOwnAndHasOneOwner(ReaderCase):
    """Everything in the audit layer hangs on this string."""

    def test_the_seat_written_is_the_seat_plans_label(self):
        out = self.drive(self.rows(), self.clean())
        self.assertEqual(out.registered[0].seat, self.plan.judges[0].label)
        self.assertEqual(out.registered[0].seat, "judge#1")

    def test_the_graph_can_find_the_validity_node_under_that_spelling(self):
        out = self.drive(self.rows(), self.clean())
        seat = out.registered[0].seat
        self.assertTrue(G.validity_nodes_for_seat(self.harness, seat))
        self.assertIn(seat, G.seats_on_record(self.harness))

    def test_the_roles_map_names_the_judging_pair(self):
        out = self.drive(self.rows(), self.clean())
        self.assertEqual(sorted(out.registered[0].roles),
                         [seat.label for seat in self.plan.judges])

    def test_the_module_spells_no_seat_label_of_its_own(self):
        source = MODULE.read_text(encoding="utf-8")
        body = source.split('"""', 2)[2]
        self.assertNotIn("judge#", body)
        self.assertNotIn("judge-1", body)


# --------------------------------------------------------------------------
# The refusals, the codes, and the module surface
# --------------------------------------------------------------------------


class EveryRefusalIsNamedAndReachable(ReaderCase):

    def test_a_row_without_a_row_key_is_refused(self):
        with self.assertRaises(R.ReaderError) as caught:
            R.ReadingRow.coerce({"surface": self.surface})
        self.assertEqual(caught.exception.code, R.READER_ROW_INVALID)

    def test_a_row_without_a_surface_is_refused(self):
        with self.assertRaises(R.ReaderError) as caught:
            R.ReadingRow.coerce({"row_key": "row-a"})
        self.assertEqual(caught.exception.code, R.READER_ROW_INVALID)

    def test_anything_else_is_not_a_row(self):
        with self.assertRaises(R.ReaderError) as caught:
            R.ReadingRow.coerce(["row-a"])
        self.assertEqual(caught.exception.code, R.READER_ROW_INVALID)

    def test_a_row_object_round_trips_through_coerce(self):
        row = R.ReadingRow("row-a", self.surface)
        self.assertIs(R.ReadingRow.coerce(row), row)
        self.assertEqual(row.key, G.CellKey("row-a"))

    def test_two_rows_with_one_key_are_refused_before_the_second_trial(self):
        table = [{"row_key": self.CELL, "surface": self.surface},
                 {"row_key": self.CELL, "surface": self.surface}]
        with self.assertRaises(R.ReaderError) as caught:
            self.drive(table, self.clean(self.CELL, repeats=2))
        self.assertEqual(caught.exception.code, R.READER_ROW_DUPLICATE)

    def test_an_outcome_outside_the_trials_own_five_is_refused(self):
        """Reached from a *real* result whose outcome field is replaced."""

        def bent(*args, **kwargs):
            result = T.run_trial(*args, **kwargs)
            return dataclasses.replace(result, outcome="probably")

        with self.assertRaises(R.ReaderError) as caught:
            self.drive(self.rows(), self.clean(), trial_runner=bent)
        self.assertEqual(caught.exception.code, R.READER_OUTCOME_UNKNOWN)

    def test_the_reader_error_is_a_loop_error(self):
        self.assertTrue(issubclass(R.ReaderError, loop_types.LoopError))

    def test_every_new_code_is_upper_snake_with_a_one_line_reason(self):
        for code, reason in R.NEW_CODES.items():
            self.assertRegex(code, r"^[A-Z][A-Z0-9_]*$")
            self.assertTrue(reason and "\n" not in reason)

    def test_every_new_code_is_folded_into_the_failure_table_only(self):
        for code in R.NEW_CODES:
            self.assertIn(code, loop_types.FAILURE_CODES)
            self.assertNotIn(code, loop_types.BLOCK_CODES)
            self.assertNotIn(code, loop_types.OUTCOME_CODES)


class TheModuleInventsNoShapeAndOpensNoSocket(unittest.TestCase):

    def test_the_outcome_vocabulary_is_the_trials_own(self):
        self.assertIs(R.OUTCOMES, T.OUTCOMES)

    def test_the_disposition_tokens_mirror_obligations_without_importing_it(self):
        for token in (R.DISPOSITION_CRITIC_NONE, R.DISPOSITION_OUTSIDE_VOCABULARY):
            self.assertIn(token, OB.DISPOSITION_REASONS)

    def test_the_module_imports_no_provider_module(self):
        source = MODULE.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
            elif isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
        self.assertNotIn("minireason.provider_openai_compat", imported)
        for name in imported:
            self.assertNotIn("socket", name)

    def test_the_only_sibling_edges_are_the_declared_ones(self):
        source = MODULE.read_text(encoding="utf-8")
        tree = ast.parse(source)
        siblings = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "minireason.loop":
                siblings.update(alias.name for alias in node.names)
        self.assertEqual(
            siblings,
            {"contracts", "custody", "graph", "roles", "standard", "trial",
             "types"})

    def test_no_block_code_is_spelled_as_a_literal(self):
        source = MODULE.read_text(encoding="utf-8")
        body = source.split('"""', 2)[2]
        self.assertNotIn('"blocked:', body)
        self.assertNotIn("'blocked:", body)

    def test_the_module_names_no_token_the_stop_vocabulary_forbids(self):
        source = MODULE.read_text(encoding="utf-8").lower()
        self.assertNotIn("exhaustion", source)
