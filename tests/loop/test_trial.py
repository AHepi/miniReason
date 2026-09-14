"""W3-TRIAL: the §10 guard procedure G0-G12, end to end, offline.

Every class is named for one clause of the W3-TRIAL acceptance list, and every
test in it is one reading of that clause. The material is a small hand-built
use row whose surface W1-SURFACE itself builds (nothing of it is published
material, and the docstrings inside the module's packs are quoted matter, not
pack code); the provider fixture is the same OfflineProvider the house fixture
``tests/loop/test_roles.py`` runs on, scripted per coordinate; the seats are
W1-SEATS' own plan over a fixture registry with two distinct lineages. The
socket layer is removed from under every trial exactly as test_roles does.
"""
from __future__ import annotations

import ast
import contextlib
import json
import shutil
import socket
import tempfile
import unittest
from pathlib import Path

from minireason import provider_openai_compat as transport
from minireason.loop import contracts as C
from minireason.loop import graph as G
from minireason.loop import packs as P
from minireason.loop import roles
from minireason.loop import seats
from minireason.loop import standard as STD
from minireason.loop import surface as S
from minireason.loop import trial as T
from minireason.loop import types as loop_types
from minireason.loop.types import LoopError

MODULE = Path(T.__file__).resolve()


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
    """Remove the socket layer for the duration of the block."""

    socket.socket = socket.create_connection = transport._open = _refuse_socket
    try:
        yield
    finally:
        socket.socket, socket.create_connection, transport._open = _PRISTINE


# --------------------------------------------------------------------------
# The material row (hand-built; the surface is W1-SURFACE's build of it)
# --------------------------------------------------------------------------

REFERRING = (
    "The objection reads the account second record and carries its terms "
    "into a narrower claim about cadence."
)
TARGET = (
    "Written confirmation settles what an agreement meant, so the written "
    "line controls the later disagreement."
)
#: Occurs exactly once in the surface, inside the target record only.
QUOTE = "the written line controls the later disagreement"
CASE = "The objection takes up the account claim and keeps its central term."
ANSWER = "The juxtaposition shows the term reused, and that is all it shows."
#: A decisive point present exactly once in ``CASE + "\n" + ANSWER``.
POINT = "that is all it shows"


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
            "run_id": "trial-test",
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


def build_registry() -> dict:
    """A registry with three lineages, so §2.2's rules have room to hold.

    Six endpoints over six lineages: two
    judges, a critic outside both, a defender outside the critic, and a
    variator left over.
    """

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
        endpoint("synthetic/alpha-1", "alpha-family", "SYNTHETIC_ALPHA_KEY"),
        endpoint("synthetic/alpha-2", "alpha-family", "SYNTHETIC_ALPHA_KEY"),
        endpoint("synthetic/beta", "beta-family", "SYNTHETIC_BETA_KEY"),
        endpoint("synthetic/gamma", "gamma-family", "SYNTHETIC_GAMMA_KEY"),
        endpoint("synthetic/delta", "delta-family", "SYNTHETIC_DELTA_KEY"),
        endpoint("synthetic/epsilon", "epsilon-family", "SYNTHETIC_EPSILON_KEY"),
    ]
    return {e.name: e for e in entries}


# --------------------------------------------------------------------------
# The scripted providers
# --------------------------------------------------------------------------


class Scripted:
    """The provider factory, one script per (role, coordinate).

    The protocol is the one ``roles._bind_factory`` binds: ``(role,
    coordinate, records_dir, *, seat=..., endpoint=...)``. Each call hands
    out one OfflineProvider over the scripted replies, so a coordinate whose
    script is exhausted fails with the transport's own code and a coordinate
    this test did not script fails the test itself.
    """

    def __init__(self, scripts: dict) -> None:
        # One queue per (role, coordinate), consumed ACROSS calls. W2-ROLES
        # builds a fresh provider per call, so a provider handed the whole
        # reply list replays it from index 0 every time: the draft's fixture
        # gave both judge seats the *first* reply and no scripted dissent ever
        # reached a second seat, which is why the split, order-swap and
        # paraphrase-flip clauses all read as "no block" against a module that
        # blocks them correctly.
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


def judge_output(point: str = POINT, sustained: bool = True, note: str = "noted") -> dict:
    return {"sustained": sustained, "decisive_point": point, "reading_note": note}


def variator_output(*paraphrases: str) -> dict:
    return {"paraphrases": list(paraphrases)}


def paraphrase_of(case: str, answer: str, *, keep: bool = True, tag: str = "") -> str:
    """One restatement of the exchange, holding the quoted span byte-for-byte."""
    text = f"{case} Restated plainly. {answer} Restated likewise."
    if keep:
        text += f" The citation still reads as: {QUOTE}"
    if tag:
        text += f" {tag}"
    return text


#: A re-ruling decisive point that resolves once inside the paraphrase text.
PARA_POINT = "Restated plainly"


class TrialCase(unittest.TestCase):
    """One temp run: harness and cell prepared, surface built, seats selected."""

    CELL = "row-a"

    def setUp(self) -> None:
        super().setUp()
        self.tmp = Path(tempfile.mkdtemp(prefix="loop-trial-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.prepared = T.open_trial_harness(self.tmp / "graph", self.CELL)
        self.surface = S.build_surface(build_row())
        self.config = build_config()
        self.plan = seats.select_seats(build_registry())
        self.records = self.tmp / "records"
        self.records.mkdir()

    def scripts(self, *overrides: dict) -> Scripted:
        """The full clean-trial script; a test overrides the one call it breaks.

        ``overrides`` are mappings from a ``(role, coordinate)`` tuple to that
        call's reply list - a tuple key, never a keyword, because a coordinate
        is not a Python identifier. The judge coordinate carries one reply per
        seat in seat order (seat 1 first), exactly as W2-ROLES hands out one
        OfflineProvider per call.
        """
        script: dict = {
            ("critic", self.CELL): [critic_output()],
            ("defender", self.CELL): [defender_output()],
            ("judge", self.CELL): [judge_output(), judge_output()],
            ("judge", self.CELL + "#order-swapped"): [judge_output(), judge_output()],
            ("variator", self.CELL): [
                variator_output(
                    paraphrase_of(CASE, ANSWER),
                    paraphrase_of(CASE, ANSWER, tag="Again."),
                )
            ],
            ("judge", self.CELL + "#paraphrase-0"): [
                judge_output(point=PARA_POINT), judge_output(point=PARA_POINT)
            ],
            ("judge", self.CELL + "#paraphrase-1"): [
                judge_output(point=PARA_POINT), judge_output(point=PARA_POINT)
            ],
        }
        for override in overrides:
            for key, replies in override.items():
                script[key] = list(replies)
        return Scripted(script)

    def override(self, role: str, coordinate: str, *replies) -> Scripted:
        """The clean script with one call's replies replaced."""
        return self.scripts({(role, coordinate): list(replies)})

    def run_on(self, prepared, records, factory=None, **kwargs) -> T.TrialResult:
        # NOTE (sandbox): this copy of the repository carries no tools/
        # package, so seats.runner_module() cannot import runner v2 and
        # seats.key_gate_for raises RUNNER_NOT_IMPORTABLE - its declared
        # behaviour for exactly this situation. In the integrated tree the
        # gate works and run_trial passes through it unchanged; here tests
        # patch ``roles.key_gate_for`` with a BoundedSemaphore of the plan's
        # own cap so the guard, packs and custody paths run under test rather
        # than the gate's absence. roles._claim is what write-once enforces,
        # and it never touches the gate.
        import unittest.mock as mock
        from threading import BoundedSemaphore

        kwargs.setdefault("mode", STD.MODE_ABSOLUTE)
        kwargs.setdefault("key", self.CELL)
        kwargs.setdefault("provider_factory", factory or self.scripts())
        plan = kwargs.pop("seats_override", self.plan)
        with mock.patch.object(roles, "key_gate_for",
                               return_value=BoundedSemaphore(seats.MAX_PER_KEY)):
            with no_sockets():
                return T.run_trial(
                    prepared, self.surface, STD.STANDARD_BODY, plan,
                    self.config, records_dir=records, **kwargs
                )

    def go(self, factory=None, **kwargs) -> T.TrialResult:
        return self.run_on(self.prepared, self.records, factory, **kwargs)

    def fresh(self, label: str) -> tuple:
        """A second prepared harness and records dir, for a second trial."""
        prepared = T.open_trial_harness(self.tmp / f"graph-{label}", self.CELL)
        records = self.tmp / f"records-{label}"
        records.mkdir()
        return prepared, records

    def judge_labels(self) -> tuple:
        return tuple(seat.label for seat in self.plan.judges)


class TheFixtureWorks(TrialCase):
    """The wiring, proven before any acceptance clause is read off it."""

    def test_the_seat_plan_satisfies_the_constitution(self):
        self.assertEqual(len(self.plan.judges), 2)
        self.assertNotEqual(*self.plan.judge_lineages)
        self.assertNotIn(self.plan.critic.lineage, self.plan.judge_lineages)
        self.assertNotEqual(self.plan.defender.lineage, self.plan.critic.lineage)
        self.assertEqual(self.plan.relaxations, ())

    def test_the_quote_resolves_uniquely_into_the_target_record(self):
        offset = S.resolve_unique(self.surface, QUOTE)
        self.assertIsNotNone(offset)
        self.assertEqual(offset.side, S.SIDE_TARGET_RECORD)
        self.assertTrue(S.within_declared_span(self.surface, offset))

    def test_the_decisive_point_resolves_uniquely_on_the_exchange(self):
        exchange = P.exchange_surface(CASE, ANSWER)
        self.assertEqual(exchange.count(POINT), 1)
        self.assertTrue(exchange.conforming(POINT))
        self.assertIsNotNone(exchange.resolve(POINT))

    def test_the_paraphrase_point_resolves_uniquely_on_the_restatement(self):
        restated = paraphrase_of(CASE, ANSWER)
        par_surface = P.paraphrase_surface(restated, of=P.exchange_surface(CASE, ANSWER))
        self.assertEqual(par_surface.count(PARA_POINT), 1)

    def test_the_standard_is_registered_and_the_cell_is_open(self):
        self.assertIn(self.prepared.standard_id, self.prepared.harness.state.artifacts)
        self.assertEqual(G.cell_state(self.prepared.harness, self.CELL), G.UNRESOLVED)

    def test_no_measure_event_stands_before_any_trial(self):
        rules = [getattr(e.rule, "value", e.rule)
                 for e in self.prepared.harness.log.read()]
        self.assertNotIn("Measure", rules)


# --------------------------------------------------------------------------
# Acceptance 1
# --------------------------------------------------------------------------


class EveryBlockPathYieldsNoWarrantOneMeasureAndAReasonCode(TrialCase):
    """Acceptance 1, proven across every block path the module can take."""

    def _blocked(self, overrides: dict) -> T.TrialResult:
        result = self.go(factory=self.scripts(overrides))
        self.assertTrue(result.blocked, result.outcome)
        return result

    def test_a_blocked_trial_registers_nothing(self):
        result = self._blocked(
            {("critic", self.CELL): [critic_output(quote="a phrase nobody wrote")]})
        harness = self.prepared.harness
        standing = G.cell_standing(harness, self.CELL)
        self.assertEqual(standing.state, G.UNRESOLVED)
        self.assertEqual(standing.standing, ())
        self.assertEqual(standing.accepted, ())
        # Only the standard and the cell-open artifacts the preparation wrote.
        self.assertEqual(len(harness.state.artifacts), 2)
        self.assertIsNone(result.reading)

    def test_a_blocked_trial_appends_exactly_one_measure_event(self):
        before = list(self.prepared.harness.log.read())
        result = self._blocked(
            {("critic", self.CELL): [critic_output(quote="a phrase nobody wrote")]})
        after = list(self.prepared.harness.log.read())
        new = after[len(before):]
        self.assertEqual(len(new), 1)
        self.assertEqual(getattr(new[0].rule, "value", new[0].rule), "Measure")
        self.assertEqual(result.measures, (new[0].seq,))

    def test_the_block_reason_is_always_a_member_of_block_codes(self):
        scenarios = {
            "referential-integrity": {("critic", self.CELL): [
                critic_output(quote="a phrase nobody wrote")]},
            "operative-target": {("critic", self.CELL): [
                critic_output(quote="referring record")]},
            "outside-vocabulary": {("critic", self.CELL): [
                critic_output(outside="a reading outside the six values")]},
            "ensemble-split": {("judge", self.CELL): [
                judge_output(sustained=True), judge_output(sustained=False)]},
            "order-swap": {("judge", self.CELL + "#order-swapped"): [
                judge_output(sustained=True), judge_output(sustained=False)]},
            "schema": {("critic", self.CELL): [{"relation": "not-a-relation"}]},
            "paraphrase-flip": {("judge", self.CELL + "#paraphrase-0"): [
                judge_output(point=PARA_POINT, sustained=True),
                judge_output(point=PARA_POINT, sustained=False)]},
        }
        for index, (name, overrides) in enumerate(scenarios.items()):
            with self.subTest(block=name):
                prepared, records = self.prepared, self.records
                if index:
                    prepared, records = self.fresh(name)
                result = self.run_on(prepared, records,
                                     factory=self.scripts(overrides))
                self.assertIn(result.outcome,
                              (T.OUTCOME_BLOCKED, T.OUTCOME_UNRESOLVED), name)
                self.assertEqual(len(result.blocks), 1)
                self.assertIn(result.blocks[0].code, loop_types.BLOCK_CODES)
                self.assertEqual(result.blocks[0].code,
                                 loop_types.block_code(name))
                self.assertEqual(len(result.measures), 1)
                self.assertIsNone(result.reading)

    def test_the_measure_event_names_the_cells_default_artifact(self):
        result = self._blocked(
            {("critic", self.CELL): [critic_output(quote="a phrase nobody wrote")]})
        default_id = G.cell_standing(self.prepared.harness, self.CELL).default_id
        event = list(self.prepared.harness.log.read())[result.measures[0]]
        self.assertIn(default_id, event.inputs)

    def test_a_block_record_carries_the_spent_prompt_and_raw_refs(self):
        result = self._blocked(
            {("critic", self.CELL): [critic_output(quote="a phrase nobody wrote")]})
        block = result.blocks[0]
        self.assertTrue(Path(block.prompt_ref_path).is_file())
        self.assertTrue(Path(block.raw_ref_path).is_file())
        event = list(self.prepared.harness.log.read())[result.measures[0]]
        self.assertIsNotNone(event.llm)
        self.assertEqual(event.llm.prompt_ref, block.prompt_ref_path)
        self.assertEqual(event.llm.raw_ref, block.raw_ref_path)

    def test_a_provider_failure_is_the_tenth_block_path_and_mints_no_warrant(self):
        """``blocked:provider`` is a member of ``BLOCK_CODES`` and the draft's
        scenario table did not exercise it: it asserted the constant equals
        ``roles.PROVIDER_BLOCK`` and never ran a trial through it. A route that
        did not answer is a delivery fact - one Measure, no warrant, and the
        cell stays unresolved."""
        clean = self.scripts()

        def failing(role, coordinate, records_dir, *, seat=None, endpoint=None):
            clean.calls.append((role, coordinate))
            if role == "critic":
                # An exhausted offline script is the transport's own failure.
                return transport.OfflineProvider(endpoint, records_dir, [])
            return clean(role, coordinate, records_dir, seat=seat,
                         endpoint=endpoint)

        before = list(self.prepared.harness.log.read())
        result = self.go(factory=failing)
        self.assertTrue(result.blocked)
        self.assertEqual(result.blocks[0].code, T.PROVIDER_BLOCK)
        self.assertIn(result.blocks[0].code, loop_types.BLOCK_CODES)
        self.assertEqual(len(result.measures), 1)
        self.assertIsNone(result.reading)
        self.assertEqual(G.cell_state(self.prepared.harness, self.CELL),
                         G.UNRESOLVED)
        after = list(self.prepared.harness.log.read())
        self.assertEqual(len(after) - len(before), 1)

    def test_a_transports_own_words_are_quoted_and_never_rewritten(self):
        """W2-ROLES' ruling (wave-2 item 42(h)) applies here too. The transport
        spells an empty offline script "offline script exhausted"; running N9's
        scan over that made the transcript raise
        ``RESOURCE_BOUNDARY_MISDESCRIBED`` and the provider block could not be
        rendered at all. The quoted detail is lifted out of the scan - and a
        claim this module itself made is not."""
        clean = self.scripts()

        def failing(role, coordinate, records_dir, *, seat=None, endpoint=None):
            clean.calls.append((role, coordinate))
            if role == "critic":
                return transport.OfflineProvider(endpoint, records_dir, [])
            return clean(role, coordinate, records_dir, seat=seat,
                         endpoint=endpoint)

        result = self.go(factory=failing)
        self.assertIn("exhausted", result.blocks[0].detail)
        self.assertIn(result.blocks[0].detail, result.transcript)
        with self.assertRaises(STD.StandardInvalid):
            T._assert_this_module_claims_no_exhaustion(
                "the inquiry is exhausted\n", ())

    def test_a_constitution_block_dispatches_nothing_and_names_no_ref(self):
        plan = seats.SeatPlan(
            critic=self.plan.critic,
            defender=self.plan.defender,
            judges=(self.plan.judges[0],),
            variator=self.plan.variator,
            relaxations=self.plan.relaxations,
            registry_digest=self.plan.registry_digest,
            families=self.plan.families,
        )
        import unittest.mock as mock
        from threading import BoundedSemaphore

        with mock.patch.object(roles, "key_gate_for",
                               return_value=BoundedSemaphore(5)):
            with no_sockets():
                result = T.run_trial(
                    self.prepared, self.surface, STD.STANDARD_BODY, plan,
                    self.config, mode=STD.MODE_ABSOLUTE, key=self.CELL,
                    records_dir=self.records,
                    provider_factory=self.scripts(),
                )
        self.assertTrue(result.blocked)
        self.assertEqual(result.blocks[0].code, loop_types.block_code("constitution"))
        self.assertEqual(result.blocks[0].check, T.G0_CONSTITUTION)
        self.assertEqual(result.blocks[0].prompt_ref_path, "")
        self.assertEqual(result.blocks[0].raw_ref_path, "")
        self.assertEqual(result.calls, ())
        self.assertEqual(list(self.records.iterdir()), [])


# --------------------------------------------------------------------------
# Acceptance 2
# --------------------------------------------------------------------------


class AnEnsembleSplitBlocksAndRecordsBothRulingsVerbatim(TrialCase):
    """Acceptance 2. A split is a block, never a majority."""

    def split(self, first: bool, second: bool) -> T.TrialResult:
        return self.go(factory=self.scripts({("judge", self.CELL): [judge_output(sustained=first),
                                      judge_output(sustained=second)]}))

    def test_a_split_blocks_with_the_ensemble_split_code(self):
        result = self.split(True, False)
        self.assertTrue(result.blocked)
        self.assertEqual(result.blocks[0].code,
                         loop_types.block_code("ensemble-split"))
        self.assertEqual(result.blocks[0].check, T.G5_UNANIMITY)

    def test_both_rulings_are_recorded_verbatim_on_the_trial(self):
        result = self.split(True, False)
        labels = self.judge_labels()
        self.assertEqual(sorted(result.rulings), sorted(labels))
        self.assertEqual(
            result.rulings[labels[0]].as_dict(),
            judge_output(sustained=True),
        )
        self.assertEqual(
            result.rulings[labels[1]].as_dict(),
            judge_output(sustained=False),
        )

    def test_the_transcript_prints_both_rulings_and_settles_nothing(self):
        result = self.split(True, False)
        for seat in self.judge_labels():
            with self.subTest(seat=seat):
                self.assertIn(f"{seat}:", result.transcript)
        self.assertIn("sustained: True", result.transcript)
        self.assertIn("sustained: False", result.transcript)

    def test_nothing_in_a_split_computes_a_majority(self):
        result = self.split(True, False)
        text = result.transcript
        for token in ("majority", "1-1", "split vote", "tied"):
            with self.subTest(token=token):
                self.assertNotIn(token, text)
        self.assertIsNone(result.reading)
        self.assertEqual(G.cell_state(self.prepared.harness, self.CELL), G.UNRESOLVED)

    def test_a_unanimous_no_is_not_a_split(self):
        """Both seats decline in BOTH presentations. The draft's fixture
        declined only as-declared and left the swapped order sustaining, so
        what it actually built was an order-swap flip - and read the block that
        followed as evidence that a unanimous no was being called a split."""
        result = self.go(factory=self.scripts(
            {("judge", self.CELL): [judge_output(sustained=False),
                                    judge_output(sustained=False)],
             ("judge", self.CELL + "#order-swapped"): [
                 judge_output(sustained=False), judge_output(sustained=False)]}))
        self.assertEqual(result.outcome, T.OUTCOME_NOT_SUSTAINED)
        self.assertEqual(result.blocks, ())
        self.assertIsNone(result.reading)

    def test_one_seat_moving_with_the_order_is_an_order_swap_not_a_split(self):
        """The two findings are different facts about different things: a split
        is the two families disagreeing, a flip is one seat moving with the
        presentation. The draft's G5 took the union of both orders, so every
        G6 flip was published under the split code."""
        result = self.go(factory=self.scripts(
            {("judge", self.CELL + "#order-swapped"): [
                judge_output(sustained=True), judge_output(sustained=False)]}))
        self.assertEqual(result.blocks[0].code,
                         loop_types.block_code("order-swap"))
        self.assertEqual(result.blocks[0].check, T.G6_ORDER_SWAP)


# --------------------------------------------------------------------------
# Acceptance 3
# --------------------------------------------------------------------------


class AQuoteOccurringTwiceInTheMaterialBlocks(TrialCase):
    """Acceptance 3.

    The referring record is built carrying the target's own sentence, so one
    quote really does resolve twice in the surface. The draft's fixture claimed
    ``"carries its terms"`` occurred twice and never ran the count - it occurs
    once (probed: ``surface.count`` returns 1), so the class named for this
    acceptance clause exercised nothing about a doubled quote.
    """

    SHARED = QUOTE

    def setUp(self) -> None:
        super().setUp()
        self.surface = S.build_surface(
            build_row(referring=f"{REFERRING} {self.SHARED}"))

    def test_the_fixture_really_carries_the_quote_twice(self):
        self.assertEqual(self.surface.count(self.SHARED), 2)
        self.assertIsNone(S.resolve_unique(self.surface, self.SHARED))

    def test_a_quote_carried_by_both_records_blocks_referential_integrity(self):
        shared = self.SHARED
        self.assertEqual(self.surface.count(shared), 2)
        result = self.go(factory=self.scripts({("critic", self.CELL): [critic_output(quote=shared)]}))
        self.assertTrue(result.blocked)
        self.assertEqual(result.blocks[0].code, S.REFERENTIAL_INTEGRITY_BLOCK)
        self.assertEqual(result.blocks[0].check, T.G2A_UNIQUENESS)
        self.assertIn("2 times", result.blocks[0].detail)

    def test_a_quote_nowhere_in_the_material_blocks_the_same_code(self):
        absent = "no material wrote this sentence"
        self.assertEqual(self.surface.count(absent), 0)
        result = self.go(factory=self.scripts({("critic", self.CELL): [critic_output(quote=absent)]}))
        self.assertEqual(result.blocks[0].code, S.REFERENTIAL_INTEGRITY_BLOCK)

    def test_a_quote_that_resolves_twice_registers_no_warrant(self):
        self._verify_no_warrant_after(quote=self.SHARED)

    def _verify_no_warrant_after(self, quote: str) -> None:
        self.go(factory=self.scripts({("critic", self.CELL): [critic_output(quote=quote)]}))
        self.assertEqual(G.cell_state(self.prepared.harness, self.CELL),
                         G.UNRESOLVED)


# --------------------------------------------------------------------------
# Acceptance 4
# --------------------------------------------------------------------------


class AQuoteResolvingOnlyIntoThePackFramingBlocks(TrialCase):
    """Acceptance 4."""

    #: A token of the surface's own label line, occurring exactly once in the
    #: surface and wholly outside every declared span.
    FRAMING_TOKEN = "referring record"

    def test_the_fixture_token_is_unique_and_framing_only(self):
        self.assertEqual(self.surface.count(self.FRAMING_TOKEN), 1)
        offset = S.resolve_unique(self.surface, self.FRAMING_TOKEN)
        self.assertIsNotNone(offset)
        self.assertTrue(offset.is_framing)
        self.assertFalse(S.within_declared_span(self.surface, offset))

    def test_a_quote_of_the_pack_scaffolding_blocks_operative_target(self):
        result = self.go(factory=self.scripts({("critic", self.CELL): [critic_output(quote=self.FRAMING_TOKEN)]}))
        self.assertTrue(result.blocked)
        self.assertEqual(result.blocks[0].code, S.OPERATIVE_TARGET_BLOCK)
        self.assertEqual(result.blocks[0].check, T.G3_OPERATIVE_TARGET)
        self.assertIn("scaffolding", result.blocks[0].detail)

    def test_the_g2_check_ran_and_g3_is_where_it_stopped(self):
        result = self.go(factory=self.scripts({("critic", self.CELL): [critic_output(quote=self.FRAMING_TOKEN)]}))
        self.assertEqual(result.checks[T.G2A_UNIQUENESS], T.PERFORMED)
        self.assertEqual(result.checks[T.G3_OPERATIVE_TARGET], T.PERFORMED)
        self.assertEqual(result.checks[T.G5_UNANIMITY], T.NOT_PERFORMED)


# --------------------------------------------------------------------------
# Acceptance 5
# --------------------------------------------------------------------------


class ADecisivePointAbsentFromTheExchangeBlocks(TrialCase):
    """Acceptance 5, and the emitted transcript's conformance."""

    def test_zero_occurrences_on_the_exchange_blocks(self):
        result = self.go(factory=self.scripts({("judge", self.CELL): [
                judge_output(point="a point nobody wrote"),
                judge_output(point="a point nobody wrote"),
            ]}))
        self.assertTrue(result.blocked)
        self.assertEqual(result.blocks[0].code,
                         loop_types.block_code("referential-integrity"))
        self.assertEqual(result.blocks[0].check, T.G2B_UNIQUENESS)
        self.assertIn("absent", result.blocks[0].detail)

    def test_a_point_resolving_twice_on_the_exchange_blocks_the_same_way(self):
        doubled = ANSWER + " all it shows"
        self.assertGreater(
            P.exchange_surface(CASE, doubled).count("all it shows"), 1)
        result = self.go(factory=self.scripts({("defender", self.CELL): [defender_output(answer=doubled)],
               ("judge", self.CELL): [
                   judge_output(point="all it shows"),
                   judge_output(point="all it shows")]}))
        self.assertTrue(result.blocked)
        self.assertEqual(result.blocks[0].check, T.G2B_UNIQUENESS)

    def test_the_emitted_transcript_satisfies_the_vendored_gate(self):
        result = self.go()
        self.assertTrue(result.sustained)
        transcript = result.reading.transcript
        harness = self.prepared.harness
        from deepreason_core.harness import conforming_transcript, transcript_blob

        ref = transcript_blob(
            harness,
            case=transcript.case,
            answer=transcript.answer,
            decisive_point=transcript.decisive_point,
            checks=dict(transcript.checks),
        )
        self.assertTrue(conforming_transcript(harness.blobs, ref))

    def test_the_graph_transcript_half_of_the_gate_agrees(self):
        result = self.go()
        # graph.Transcript.validated asserts the program's stronger check,
        # exactly-once in case + newline + answer, before the vendored one.
        self.assertIs(result.reading.transcript.validated(),
                      result.reading.transcript)

    def test_the_sustained_reading_registers_and_the_cell_reads(self):
        result = self.go()
        ids = G.register_reading(
            self.prepared.harness, result.reading, self.prepared.standard_id)
        self.assertEqual(ids.key, self.CELL)
        self.assertEqual(G.cell_state(self.prepared.harness, self.CELL), G.READ)


# --------------------------------------------------------------------------
# Acceptance 6
# --------------------------------------------------------------------------


class AnOrderSwapFlipBlocks(TrialCase):
    """Acceptance 6."""

    def flip(self, swapped_pair: tuple) -> T.TrialResult:
        return self.go(factory=self.scripts({("judge", self.CELL + "#order-swapped"): [
                judge_output(sustained=swapped_pair[0]),
                judge_output(sustained=swapped_pair[1])]}))

    def test_a_flip_between_one_seats_two_orders_blocks_order_swap(self):
        result = self.flip((True, False))
        # As-declared both seats sustain; swapped: seat 2 flips.
        self.assertTrue(result.blocked)
        self.assertEqual(result.blocks[0].code, loop_types.block_code("order-swap"))
        self.assertEqual(result.blocks[0].check, T.G6_ORDER_SWAP)

    def test_the_block_is_logged_against_the_seat_that_flipped(self):
        result = self.flip((False, True))
        self.assertIn(self.judge_labels()[0], result.blocks[0].detail)

    def test_both_orders_are_actually_dispatched(self):
        script = self.scripts()
        self.go(factory=script)
        judge_keys = [key for role, key in script.calls if role == "judge"]
        self.assertIn(self.CELL, judge_keys)
        self.assertIn(self.CELL + "#order-swapped", judge_keys)


# --------------------------------------------------------------------------
# Acceptance 7
# --------------------------------------------------------------------------


class AParaphraseFlipBlocksAndIsLoggedAgainstTheSeat(TrialCase):
    """Acceptance 7."""

    def flip(self, token: str = "#paraphrase-0",
             pair: tuple = (True, False)) -> T.TrialResult:
        return self.go(factory=self.scripts({("judge", self.CELL + token): [
                judge_output(point=PARA_POINT, sustained=pair[0]),
                judge_output(point=PARA_POINT, sustained=pair[1])]}))

    def test_a_flip_under_a_paraphrase_blocks_paraphrase_flip(self):
        result = self.flip()
        self.assertTrue(result.blocked)
        self.assertEqual(result.blocks[0].code,
                         loop_types.block_code("paraphrase-flip"))
        self.assertEqual(result.blocks[0].check, T.G7_PARAPHRASE)

    def test_the_flip_is_logged_against_the_seat_whose_ruling_moved(self):
        result = self.flip()
        self.assertIn(self.judge_labels()[1], result.blocks[0].detail)

    def test_a_paraphrase_flip_registers_no_warrant(self):
        result = self.flip()
        self.assertIsNone(result.reading)
        self.assertEqual(G.cell_state(self.prepared.harness, self.CELL),
                         G.UNRESOLVED)

    def test_a_flip_on_the_second_paraphrase_blocks_identically(self):
        result = self.flip(token="#paraphrase-1", pair=(False, True))
        self.assertEqual(result.blocks[0].code,
                         loop_types.block_code("paraphrase-flip"))
        self.assertIn(self.judge_labels()[0], result.blocks[0].detail)


# --------------------------------------------------------------------------
# Acceptance 8
# --------------------------------------------------------------------------


class AParaphraseThatLostASpanMarksTheSpotCheckNotPerformed(TrialCase):
    """Acceptance 8."""

    def script_with_lost_span(self) -> Scripted:
        return self.scripts({("variator", self.CELL): [variator_output(
                paraphrase_of(CASE, ANSWER, keep=False),
                paraphrase_of(CASE, ANSWER, tag="Again."),
            )]})

    def test_the_spot_check_is_recorded_not_performed(self):
        result = self.go(factory=self.script_with_lost_span())
        self.assertEqual(result.checks[T.G7_PARAPHRASE], T.NOT_PERFORMED)
        self.assertIn(f"{T.G7_PARAPHRASE}: {T.NOT_PERFORMED}", result.transcript)

    def test_no_re_ruling_is_requested_over_the_spanless_paraphrase(self):
        script = self.script_with_lost_span()
        self.go(factory=script)
        judge_keys = [key for role, key in script.calls if role == "judge"]
        self.assertIn(self.CELL + "#paraphrase-1", judge_keys)
        self.assertNotIn(self.CELL + "#paraphrase-0", judge_keys)

    def test_a_lost_span_neither_passes_nor_flips_the_cell(self):
        result = self.go(factory=self.script_with_lost_span())
        self.assertTrue(result.sustained)
        self.assertIsNotNone(result.reading)
        self.assertEqual(result.blocks, ())

    def test_every_span_preserved_records_the_check_performed(self):
        result = self.go()
        self.assertEqual(result.checks[T.G7_PARAPHRASE], T.PERFORMED)


# --------------------------------------------------------------------------
# Acceptance 9
# --------------------------------------------------------------------------


class ReReadWithoutAListedReasonRaisesReopenRefused(TrialCase):
    """Acceptance 9, and 'enforced by refusing the write'."""

    def prior_trial(self) -> None:
        self.go(factory=self.scripts({("critic", self.CELL): [critic_output(quote="a phrase nobody wrote")]}))

    def test_the_second_trial_is_refused_with_reopen_refused(self):
        self.prior_trial()
        prepared, records = self.fresh("second")
        with self.assertRaises(T.ReopenRefused) as caught:
            # NOTE: the gate reads the TRIAL's harness; the re-read is against
            # the same graph even though its records would live elsewhere.
            self.run_on(self.prepared, self.tmp / "records-second",
                        factory=self.scripts())
        self.assertEqual(caught.exception.code, "REOPEN_REFUSED")

    def test_the_write_is_refused_before_any_coordinate_is_claimed(self):
        self.prior_trial()
        before = sorted(p.as_posix() for p in self.tmp.rglob("call.json"))
        script = self.scripts()
        second_records = self.tmp / "records-second"
        second_records.mkdir()
        with self.assertRaises(T.ReopenRefused):
            self.run_on(self.prepared, second_records, factory=script)
        self.assertEqual(script.calls, [])
        after = sorted(p.as_posix() for p in self.tmp.rglob("call.json"))
        self.assertEqual(before, after)

    def test_a_listed_reopen_reason_is_admitted(self):
        self.prior_trial()
        second_records = self.tmp / "records-second"
        second_records.mkdir()
        result = self.run_on(self.prepared, second_records,
                             factory=self.scripts(),
                             reopen_reason="appellate-ruling")
        self.assertTrue(result.sustained)
        self.assertEqual(result.reopen_reason, "appellate-ruling")

    def test_an_unlisted_reason_is_refused_and_names_itself(self):
        self.prior_trial()
        second_records = self.tmp / "records-second"
        second_records.mkdir()
        with self.assertRaises(T.ReopenRefused) as caught:
            self.run_on(self.prepared, second_records,
                        factory=self.scripts(),
                        reopen_reason="because-i-want-to")
        self.assertIn("because-i-want-to", caught.exception.detail)
        self.assertIn("appellate-ruling", caught.exception.detail)

    def test_the_reopen_list_is_the_standards_and_never_retyped_here(self):
        self.assertIs(T.REOPEN_REASONS, STD.REOPEN_REASONS)

    def test_reopen_refused_is_a_loop_error_carrying_the_declared_code(self):
        self.assertTrue(issubclass(T.ReopenRefused, LoopError))
        self.assertIn("REOPEN_REFUSED", loop_types.FAILURE_CODES)
        self.assertNotIn("REOPEN_REFUSED", T.NEW_CODES)


# --------------------------------------------------------------------------
# Acceptance 10
# --------------------------------------------------------------------------


class TheWholeModuleRunsOnOfflineProviderFixturesWithZeroSockets(TrialCase):
    """Acceptance 10."""

    def test_the_clean_trial_runs_with_no_socket_layer_at_all(self):
        result = self.go()  # every trial in this file runs inside no_sockets()
        self.assertTrue(result.sustained)
        self.assertEqual(result.checks[T.G0_CONSTITUTION], T.PERFORMED)
        self.assertEqual(result.checks[T.G7_PARAPHRASE], T.PERFORMED)
        self.assertEqual(result.checks[T.G12_NO_SCORING_KEY], T.PERFORMED)

    def test_every_call_record_was_written_by_the_offline_provider(self):
        result = self.go()
        for call in result.calls:
            with self.subTest(coordinate=call.coordinate):
                sent = json.loads(
                    Path(call.result.prompt_ref.path).read_text(encoding="utf-8"))
                self.assertTrue(sent.get("synthetic") or "not_contacted" in json.dumps(sent))

    def test_no_provider_but_the_scripted_offline_one_ever_answers(self):
        script = self.scripts()
        result = self.go(factory=script)
        self.assertEqual(
            sorted(script.calls),
            sorted((call.role, call.coordinate) for call in result.calls),
        )

    def test_every_call_coordinate_was_spent_exactly_once(self):
        """A coordinate is ``(role, seat, key)`` - two judge seats answering one
        exchange are two coordinates, not one spent twice; W2-ROLES' own slug
        carries the seat label for exactly that reason."""
        result = self.go()
        coordinates = [f"{call.role}/{call.seat_label}/{call.coordinate}"
                       for call in result.calls]
        self.assertEqual(len(coordinates), len(set(coordinates)))
        self.assertEqual(len(coordinates), 11)

    def test_a_second_call_on_a_spent_coordinate_still_raises_no_replay(self):
        self.go()
        with self.assertRaises(roles.RoleRefused) as caught:
            with no_sockets():
                roles.call_critic(
                    self.plan.critic, b"return one JSON object", self.records,
                    coordinate=self.CELL,
                    provider_factory=self.scripts())
        self.assertEqual(caught.exception.code, roles.NO_REPLAY)


# --------------------------------------------------------------------------
# The outcomes that are not blocks
# --------------------------------------------------------------------------


class ACriticAnsweringNoneEndsTheRowAtOneCall(TrialCase):
    """§2.3's escape, on the trial's side of it."""

    def none(self) -> T.TrialResult:
        return self.go(factory=self.scripts({("critic", self.CELL): [
            critic_output(relation="none", quote="", case="")]}))

    def test_none_is_no_trial_and_is_not_a_block(self):
        result = self.none()
        self.assertEqual(result.outcome, T.OUTCOME_NO_TRIAL)
        self.assertFalse(result.blocked)
        self.assertEqual(result.blocks, ())

    def test_none_leaves_one_measure_so_g11_can_see_the_row_was_asked(self):
        """The draft left no event at all, so a ``none`` was the one outcome a
        caller could re-read freely - no ``reopen_reason``, and nothing on the
        record saying the row had been read. A Measure is information, not a
        verdict, and the not-sustained outcome already writes one."""
        before = list(self.prepared.harness.log.read())
        result = self.none()
        after = list(self.prepared.harness.log.read())
        self.assertEqual(len(after) - len(before), 1)
        self.assertEqual(len(result.measures), 1)
        default_id = G.cell_standing(self.prepared.harness, self.CELL).default_id
        self.assertIn(default_id, after[-1].inputs)

    def test_a_re_read_after_none_is_refused_without_a_reopen_reason(self):
        self.none()
        second = self.tmp / "records-after-none"
        second.mkdir()
        with self.assertRaises(T.ReopenRefused):
            self.run_on(self.prepared, second, factory=self.scripts())
        result = self.run_on(self.prepared, second, factory=self.scripts(),
                             reopen_reason="new-material")
        self.assertTrue(result.sustained)

    def test_none_spends_exactly_the_critics_call(self):
        script = self.scripts({("critic", self.CELL): [critic_output(relation="none", quote="", case="")]})
        self.go(factory=script)
        self.assertEqual(script.calls, [("critic", self.CELL)])

    def test_the_cell_stays_unresolved_after_none(self):
        self.go(factory=self.scripts({("critic", self.CELL): [critic_output(relation="none", quote="", case="")]}))
        self.assertEqual(G.cell_state(self.prepared.harness, self.CELL), G.UNRESOLVED)


class ANonEmptyOutsideVocabularyForcesUnresolved(TrialCase):
    """G4/D6: the text is preserved and the block is the ceiling's own code."""

    OUTSIDE = "the reading I want is not one of the closed six"

    def result(self) -> T.TrialResult:
        return self.go(factory=self.scripts({("critic", self.CELL): [critic_output(outside=self.OUTSIDE)]}))

    def test_the_outcome_is_unresolved_with_the_outside_vocabulary_block(self):
        result = self.result()
        self.assertEqual(result.outcome, T.OUTCOME_UNRESOLVED)
        self.assertEqual(result.blocks[0].code,
                         loop_types.block_code("outside-vocabulary"))
        self.assertIn("outside-vocabulary", loop_types.CEILING_BLOCK_REASONS)
        self.assertEqual(len(result.measures), 1)

    def test_the_text_is_preserved_on_the_record(self):
        result = self.result()
        assert result.critic is not None
        self.assertEqual(
            result.critic.as_dict()[C.OUTSIDE_VOCABULARY_FIELD], self.OUTSIDE)
        # contracts normalises the relation away from the named token; the
        # trial record keeps the text, exactly as D6 requires.
        self.assertEqual(result.critic.relation, C.NONE_RELATION)
        self.assertIn(self.OUTSIDE, result.transcript)


class ANotSustainedRulingRegistersNothing(TrialCase):
    """The panel unanimously declines: a ruling, not a block, not a warrant."""

    def result(self) -> T.TrialResult:
        return self.go(factory=self.scripts({("judge", self.CELL): [judge_output(sustained=False),
                                      judge_output(sustained=False)],
               ("judge", self.CELL + "#order-swapped"): [
                   judge_output(sustained=False),
                   judge_output(sustained=False)]}))

    def test_the_outcome_is_not_sustained(self):
        result = self.result()
        self.assertEqual(result.outcome, T.OUTCOME_NOT_SUSTAINED)
        self.assertFalse(result.blocked)
        self.assertEqual(result.blocks, ())
        self.assertIsNone(result.reading)

    def test_the_paraphrase_check_never_ran_and_says_so(self):
        """G7 guards a *sustained* ruling only; nothing else ever could run it."""
        result = self.result()
        self.assertEqual(result.checks[T.G7_PARAPHRASE], T.NOT_PERFORMED)


# --------------------------------------------------------------------------
# The transcript as an emitted artifact
# --------------------------------------------------------------------------


class TheEmittedTranscript(TrialCase):
    """The acceptance's last half: what the transcript itself must satisfy."""

    def test_every_guard_check_is_printed_performed_or_not_performed(self):
        result = self.go()
        self.assertEqual(tuple(result.checks), T.GUARD_CHECKS)
        for name in T.GUARD_CHECKS:
            with self.subTest(check=name):
                self.assertIn(result.checks[name], (T.PERFORMED, T.NOT_PERFORMED))
                self.assertIn(f"{name}: {result.checks[name]}", result.transcript)

    def test_build_transcript_is_deterministic_over_the_result(self):
        result = self.go()
        self.assertEqual(T.build_transcript(result), result.transcript)
        self.assertEqual(T.build_transcript(result), T.build_transcript(result))

    def test_build_transcript_accepts_the_results_mapping_form(self):
        result = self.go()
        self.assertEqual(T.build_transcript(result.as_dict()), result.transcript)

    def test_the_transcript_never_describes_a_boundary_as_exhaustion(self):
        result = self.go()
        STD.assert_no_exhaustion_claim(result.transcript, "test transcript")

    def test_the_record_is_g12_clean(self):
        C.assert_no_scoring_keys(self.go().as_dict())
        blocked = self.run_on(*self.fresh("blocked"), factory=self.scripts({("critic", self.CELL): [critic_output(quote="a phrase nobody wrote")]}))
        C.assert_no_scoring_keys(blocked.as_dict())

    def test_a_transcript_built_from_a_declared_block_is_well_formed(self):
        prepared, records = self.fresh("declared")
        result = self.run_on(prepared, records, factory=self.scripts({("critic", self.CELL): [critic_output(quote="a phrase nobody wrote")]}))
        self.assertIn(loop_types.block_code("referential-integrity"), result.transcript)
        self.assertIn("blocks:", result.transcript)
        self.assertIn(result.blocks[0].prompt_ref_path, result.transcript)

    def test_two_runs_of_the_same_arguments_render_identical_transcripts(self):
        first = self.go()
        second = self.run_on(*self.fresh("again"), factory=self.scripts())
        # The two transcripts agree in everything but the coordinate-local digests.
        self.assertEqual(first.checks, second.checks)
        self.assertEqual(first.outcome, second.outcome)


# --------------------------------------------------------------------------
# The module's own declarations
# --------------------------------------------------------------------------


class TheModuleItself(unittest.TestCase):

    def test_the_import_graph_stays_inside_the_declared_dependencies(self):
        tree = ast.parse(MODULE.read_text(encoding="utf-8"))
        siblings = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                siblings.add(node.module.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module and \
                    node.module.startswith("minireason.loop."):
                siblings.add(node.module.rsplit(".", 1)[-1])
        # The depends_on list plus seats, whose SeatPlan the entry's `seats`
        # argument already is. No wave-2-plus module beyond packs and roles.
        self.assertLessEqual(siblings, {
            "contracts", "graph", "packs", "roles", "seats", "standard",
            "surface", "types",
        })

    def test_no_block_code_is_retyped_with_the_prefix(self):
        source = MODULE.read_text(encoding="utf-8")
        self.assertNotIn('"blocked:', source)
        self.assertNotIn("'blocked:", source)

    def test_every_block_constant_is_the_owner_modules_own(self):
        self.assertIs(T.BLOCK_CODES, loop_types.BLOCK_CODES)
        self.assertEqual(T.REFERENTIAL_INTEGRITY_BLOCK, S.REFERENTIAL_INTEGRITY_BLOCK)
        self.assertEqual(T.OPERATIVE_TARGET_BLOCK, S.OPERATIVE_TARGET_BLOCK)
        self.assertEqual(T.SCHEMA_BLOCK, roles.SCHEMA_BLOCK)
        self.assertEqual(T.PROVIDER_BLOCK, roles.PROVIDER_BLOCK)
        self.assertIs(T.REOPEN_REASONS, STD.REOPEN_REASONS)

    def test_every_new_code_carries_a_reason_and_is_folded_in(self):
        """The wave-3 integrator's fold-in contract, in the wave-2 spelling:
        every ``NEW_CODES`` key is a member of ``FAILURE_CODES`` and of neither
        other table. Before the fold-in this test read "the table does NOT carry
        it", which is true only until the module lands."""
        self.assertTrue(T.NEW_CODES)
        for code, reason in T.NEW_CODES.items():
            with self.subTest(code=code):
                self.assertRegex(code, r"\A[A-Z][A-Z0-9_]*\Z")
                self.assertTrue(reason.strip())
                self.assertIn(code, loop_types.FAILURE_CODES)
                self.assertNotIn(code, loop_types.OUTCOME_CODES)
                self.assertNotIn(code, loop_types.STOP_REASONS)

    def test_a_seats_argument_that_is_not_a_seat_plan_names_its_own_code(self):
        """The shape refusal and G0 are two different things, and each has its
        own name. The draft declared ``TRIAL_SEAT_PLAN_INVALID`` for G0's
        family rules - which deviation 5 settles as a *block* - so nothing in
        the package could raise it."""
        with self.assertRaises(T.TrialRefused) as caught:
            T.run_trial(object(), object(), STD.STANDARD_BODY, object(), {},
                        mode=STD.MODE_ABSOLUTE, key="row-a", records_dir=".")
        self.assertEqual(caught.exception.code, T.TRIAL_SEAT_PLAN_INVALID)

    def test_the_span_lost_outcome_is_a_recorded_state_and_not_a_code(self):
        self.assertNotIn("TRIAL_PARAPHRASE_SPAN_LOST", loop_types.FAILURE_CODES)
        self.assertFalse(hasattr(T, "TRIAL_PARAPHRASE_SPAN_LOST"))
        self.assertIn(T.NOT_PERFORMED, (T.PERFORMED, T.NOT_PERFORMED))

    def test_the_one_code_this_module_raises_that_was_already_declared(self):
        self.assertIn("REOPEN_REFUSED", loop_types.FAILURE_CODES)
        self.assertEqual(T.ReopenRefused("d").code, "REOPEN_REFUSED")

    def test_no_code_is_raised_as_a_bare_literal(self):
        import re

        source = MODULE.read_text(encoding="utf-8")
        self.assertEqual(re.findall(r'_refuse\(\s*"', source), [])
        self.assertEqual(re.findall(r'TrialRefused\(\s*"', source), [])

    def test_the_public_interface_the_wave_plan_names_is_present(self):
        self.assertTrue(callable(T.run_trial))
        self.assertTrue(callable(T.build_transcript))
        self.assertTrue(issubclass(T.ReopenRefused, LoopError))
        for name in ("outcome", "blocks", "transcript"):
            with self.subTest(field=name):
                self.assertIn(name, T.TrialResult.__dataclass_fields__)

    def test_build_transcript_refuses_a_block_code_outside_the_table(self):
        bad = {
            "cell": "row-a",
            "outcome": T.OUTCOME_BLOCKED,
            "checks": {name: T.PERFORMED for name in T.GUARD_CHECKS},
            "blocks": [{"code": "blocked:not-a-reason", "check": T.G1_SCHEMA}],
        }
        with self.assertRaises(T.TrialRefused) as caught:
            T.build_transcript(bad)
        self.assertEqual(caught.exception.code, T.TRIAL_ARGUMENT_INVALID)

    def test_build_transcript_refuses_a_checks_mapping_with_a_gap(self):
        bad = {
            "cell": "row-a",
            "outcome": T.OUTCOME_SUSTAINED,
            "checks": {name: T.PERFORMED for name in T.GUARD_CHECKS[1:]},
        }
        with self.assertRaises(T.TrialRefused):
            T.build_transcript(bad)

    def test_the_module_reads_no_socket_and_no_credential(self):
        tree = ast.parse(MODULE.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        for banned in ("socket", "urllib", "requests", "http"):
            with self.subTest(module=banned):
                self.assertNotIn(banned, imported)


class TheModuleImportsClean(unittest.TestCase):

    def test_import_and_reload_under_the_sandboxs_default_warning_filter(self):
        # The one known repository defect in the import chain is
        # use_relation_h005.py's docstring (an unescaped backslash-s), which
        # the wave-2 interface note defers to the SRC-003 erratum and this
        # module may not edit; so this check runs without -W error, as the
        # task prescribes for exactly that failure.
        import importlib

        import minireason.loop.trial as module

        reloaded = importlib.reload(module)
        self.assertTrue(hasattr(reloaded, "run_trial"))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
