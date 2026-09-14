"""W2-DECIDE - the pre-registered stop/continue program, clause by clause.

Every acceptance clause of the wave-plan entry has at least one test here, and
every fixture graph is populated **only** through ``minireason.loop.graph``:

* "decide() is total and returns exactly one outcome" -
  :class:`DecideIsTotalAndReturnsExactlyOneOutcome`.
* "a protected loss stops and names the loss" - :class:`AProtectedLossStops`.
* "an o satisfied without this cycle's own artifacts does not continue" -
  :class:`ProducedByDecidesWhetherASatisfiedObligationContinues`.
* "identical mark-triple sets stop as a set identity and not as a count" -
  :class:`ClauseFourIsSetIdentity`.
* "a budget stop carries the boundary-not-exhaustion sentence and a
  would_reopen field" - :class:`TheDeclaredBoundaryStop`.
* "a block streak stops as instrument_fault naming a fault in the instrument,
  not a finding about the material" - :class:`TheGuardRailsComeFirst`.
* "no count of readings, marks, endpoints or differs appears in any clause" -
  :class:`NoClauseIsAMeter`.
* "the module digest matches the one pinned in plan.json" -
  :class:`TheModuleIsPinnedAndCallsNoModel`.

The obligations documents here are deliberately small: ``o5``
(``audit_in_force``) and ``p8`` (``appellate_optional``) are the two predicates
that reach a verdict on a graph W1-GRAPH alone has populated *and* can be moved
by registering one more artifact, so each clause can be exercised on a real
harness rather than on a stub.  No provider, no socket, nothing written outside
a temporary directory.
"""

from __future__ import annotations

import ast
import dataclasses
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from deepreason_core.canonical import canonical_json, sha256_hex
from deepreason_core.ontology import Provenance

from minireason.loop import custody, graph
from minireason.loop import decide as mod
from minireason.loop import obligations as ob
from minireason.loop import standard
from minireason.loop.decide import (
    ALL_ARMS_ENDED_SENTENCE,
    ALWAYS_SENTENCES,
    CLAUSE_ALL_ARMS_ENDED,
    CLAUSE_ALL_SATISFIED,
    CLAUSE_CUSTODY_HALT,
    CLAUSE_DISCHARGE,
    CLAUSE_INSTRUMENT_FAULT,
    CLAUSE_NONE,
    CLAUSE_ORDER,
    CLAUSE_PROTECTED_LOSS,
    CLAUSE_RESOURCE_BOUNDARY,
    CLAUSE_SET_IDENTITY,
    CONTINUE_DISCHARGED,
    CONTINUE_OPEN,
    CONTINUE_REASONS,
    DECIDE_SCHEMA,
    DECIDE_SHA256,
    NEW_CODES,
    REASON_SENTENCES,
    RESOURCE_BOUNDARY_SENTENCE,
    STOP_ALL_ARMS_ENDED,
    STOP_CUSTODY_HALT,
    STOP_INSTRUMENT_FAULT,
    STOP_NO_NEW_READING_CHANGES,
    STOP_OBLIGATIONS_DISCHARGED,
    STOP_PROTECTED_LOSS,
    STOP_RESOURCE_BOUNDARY,
    WOULD_REOPEN,
    Decision,
    DecisionRefused,
    Instrument,
    decide,
    declared_boundary_reached,
    instrument_bound_crossed,
    mark_triples,
    render_decision,
    situation,
)
from minireason.loop import types as loop_types
from minireason.loop.types import STOP_REASONS, LoopConfig, LoopError, is_stop_reason

SOURCE = Path(mod.__file__).resolve()
MATERIAL = b'{"row_key": "r1", "cells": {}}'

CONFIG = {
    "schema": "minireason.loop.config.v1",
    "run_id": "LOOP-01",
    "study": "h005",
    "occurrences": ["experiments/h005/occurrence-01"],
    "runner": "tools/multicycle_commitment_study_multi_v2.py",
    "cycle_budget": 3,
    "max_calls": 240,
    "reading_set": ["p1/mini_fcl/cycle-1/n1#r3"],
    "obligations_path": "experiments/loops/LOOP-01/obligations.json",
    "graph_root": "experiments/loops/LOOP-01/graph",
    "reopen_reasons": ["new-material", "repaired-guard", "appellate-ruling"],
    "audit": {
        "period": 2,
        "judge_err_max": 0.2,
        "judge_err_max_account": "five anchors, so this margin is one anchor",
        "streak_max": 5,
        "streak_max_account": "longer than any run of blocks the dry run produced",
    },
}

#: (id, membership, predicate) for the two obligations these fixtures move.
DECLARED = (("o5", "O", "audit_in_force"), ("p8", "P", "appellate_optional"))


def entry(identifier: str, membership: str, check: str) -> dict:
    return {
        "id": identifier,
        "set": membership,
        "statement": f"the pre-registered prose of {identifier}",
        "check": {"predicate": f"obligations.{check}",
                  "artifact": [f"experiments/loops/T001/{identifier}.json"],
                  "detail": f"how the program reads {identifier}"},
        "why_not_a_count": "a universal quantification over a fixed named key set",
    }


def document(rows=DECLARED) -> dict:
    body = {"schema": ob.OBLIGATIONS_SCHEMA, "run_id": "T001",
            "obligations": [entry(*row) for row in rows]}
    body["obligations_sha256"] = sha256_hex(canonical_json(body))
    return body


class DecideTestCase(unittest.TestCase):
    """One harness on a deterministic clock, two open cells, two obligations."""

    CELL = "r1/c1"

    def setUp(self) -> None:
        super().setUp()
        self.root = Path(tempfile.mkdtemp(prefix="loop-decide-"))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.obligations = self.write()
        self.harness = graph.open_graph(self.root / "graph", clock=graph.fixed_clock())
        self.standard_id = graph.register_standard(self.harness)
        self.material = graph.register_material(self.harness, MATERIAL)
        self.mark_cell = graph.CellKey(self.CELL, "T", "original-vs-control")
        self.opened = graph.open_cells(
            self.harness, [graph.CellKey(self.CELL), self.mark_cell],
            material_id=self.material)
        self.config = LoopConfig.from_mapping(CONFIG)

    # -- fixture builders, every one a call W5-DRIVER will make -------------- #

    def write(self, rows=DECLARED, name: str = "obligations.json") -> ob.Obligations:
        path = self.root / name
        path.write_text(json.dumps(document(rows), indent=2), encoding="utf-8")
        return ob.load_obligations(path)

    def audit(self, covers: str) -> str:
        """An audit record declaring which cycle it covers - o5's whole subject."""
        return graph.register_audit_warrant(self.harness, graph.AuditFinding(
            seat="judge-2", kind="paraphrase-invariance", detail="no flip",
            body={"covers": [covers], "seats": ["judge-1", "judge-2"],
                  "calibration_sha256": "d" * 64}))

    def blocker(self) -> str:
        """A record declaring itself blocked on the appellate - p8's defeater."""
        artifact = self.harness.create_artifact(
            json.dumps({"record": "cell_open", "key": self.CELL,
                        "blocked_on": "appellate"}, sort_keys=True).encode("utf-8"),
            codec="json", provenance=Provenance(role="import"))
        return artifact.id

    def mark(self, token: str = "differs") -> graph.ReadingIds:
        transcript = graph.Transcript(
            case="ORIGINAL names o1 where CONTROL names o2, so the target set differs",
            answer="the defence concedes the two commitments do not name one target",
            decisive_point="the target set differs")
        return graph.register_mark(self.harness, graph.ReadingResult(
            key=self.mark_cell, relation=token, seat="judge-1",
            transcript=transcript, difference_kind="target_set_membership",
            material_id=self.material), self.standard_id)

    def at(self, cycle: int, registered=()) -> ob.Situation:
        return situation(self.harness, cycle, self.obligations, registered=registered)


# ---------------------------------------------------------------------------
# The module's identity, and the absence of any model
# ---------------------------------------------------------------------------


class TheModuleIsPinnedAndCallsNoModel(unittest.TestCase):
    """Design section 5: ``decide.py``'s own digest is inside ``loop_plan_id``."""

    BANNED_IMPORT_WORDS = ("roles", "provider", "openai", "socket", "http",
                           "urllib", "requests", "anthropic")

    @classmethod
    def setUpClass(cls) -> None:
        cls.tree = ast.parse(SOURCE.read_text(encoding="utf-8"))

    def imported(self) -> set[str]:
        names: set[str] = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                base = node.module or ""
                names.add(base)
                names.update(f"{base}.{alias.name}" for alias in node.names)
        return {name for name in names if name}

    def test_the_module_publishes_the_sha256_of_its_own_bytes(self):
        self.assertEqual(
            DECIDE_SHA256,
            hashlib.sha256(SOURCE.read_bytes()).hexdigest())

    def test_that_digest_is_what_custody_would_pin_for_this_path(self):
        """The value ``loop_plan_id`` folds is ``custody.pins``' value, or the
        plan pins a digest of something else."""
        self.assertEqual(DECIDE_SHA256, custody.sha256_path(SOURCE))

    def test_the_digest_rides_in_every_decision_record(self):
        record = Decision(cycle=1, stop=False, reason=CONTINUE_OPEN,
                          clause=CLAUSE_NONE, would_reopen="prose").as_dict()
        self.assertEqual(record["decide_sha256"], DECIDE_SHA256)
        self.assertEqual(record["schema"], DECIDE_SCHEMA)

    def test_the_module_imports_no_role_dispatch_and_no_provider(self):
        for name in sorted(self.imported()):
            for banned in self.BANNED_IMPORT_WORDS:
                with self.subTest(imported=name, banned=banned):
                    self.assertNotIn(banned, name.lower())

    def test_nothing_in_the_module_opens_a_call(self):
        source = SOURCE.read_text(encoding="utf-8")
        for token in ("call_role(", "provider(", "urlopen", "socket.", "requests."):
            with self.subTest(token=token):
                self.assertNotIn(token, source)

    def test_every_new_code_is_a_module_constant_with_a_one_line_reason(self):
        self.assertTrue(NEW_CODES)
        for code, why in NEW_CODES.items():
            with self.subTest(code=code):
                self.assertEqual(code, code.upper())
                self.assertEqual(getattr(mod, code), code)
                self.assertTrue(why.strip())
                self.assertNotIn("\n", why)

    def test_no_refusal_is_raised_with_a_bare_string_literal(self):
        """Codes are raised as module constants, never retyped at the raise."""
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Call):
                continue
            name = getattr(node.func, "id", "")
            if name != "DecisionRefused" or not node.args:
                continue
            with self.subTest(line=node.lineno):
                self.assertIsInstance(node.args[0], ast.Name)

    def test_every_refusal_code_is_declared_in_new_codes(self):
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Call):
                continue
            if getattr(node.func, "id", "") != "DecisionRefused" or not node.args:
                continue
            with self.subTest(line=node.lineno):
                self.assertIn(getattr(mod, node.args[0].id), NEW_CODES)


# ---------------------------------------------------------------------------
# Totality
# ---------------------------------------------------------------------------


class DecideIsTotalAndReturnsExactlyOneOutcome(DecideTestCase):

    def outcomes(self) -> list[Decision]:
        before = self.at(cycle=1)
        empty = mark_triples(self.harness)
        self.mark()
        moved = mark_triples(self.harness)
        audited = self.audit("2")
        after = self.at(cycle=2, registered=[audited])
        unattributed = self.at(cycle=2)
        self.blocker()
        lost = self.at(cycle=3)
        return [
            decide(None, before, 1, self.config, self.obligations),
            decide(before, after, 2, self.config, self.obligations),
            decide(before, unattributed, 2, self.config, self.obligations),
            decide(before, unattributed, 2, self.config, self.obligations,
                   prev_triples=empty, curr_triples=empty),
            decide(before, unattributed, 2, self.config, self.obligations,
                   prev_triples=empty, curr_triples=moved),
            decide(after, lost, 3, self.config, self.obligations),
            decide(before, after, 3, self.config, self.obligations),
            decide(before, after, 2, self.config, self.obligations,
                   instrument=Instrument(custody_halted=True)),
            decide(before, after, 2, self.config, self.obligations,
                   instrument=Instrument(arms_ended=True)),
            decide(before, after, 2, self.config, self.obligations,
                   instrument={"block_streak": 9}),
        ]

    def test_every_call_returns_exactly_one_decision(self):
        for result in self.outcomes():
            with self.subTest(clause=result.clause):
                self.assertIsInstance(result, Decision)

    def test_every_reason_is_declared_and_stop_and_continue_are_complements(self):
        for result in self.outcomes():
            with self.subTest(clause=result.clause, reason=result.reason):
                self.assertIn(result.clause, CLAUSE_ORDER)
                self.assertIs(result.continues, not result.stop)
                if result.stop:
                    self.assertTrue(is_stop_reason(result.reason))
                    self.assertIn(result.reason, STOP_REASONS)
                else:
                    self.assertIn(result.reason, CONTINUE_REASONS)
                    self.assertFalse(is_stop_reason(result.reason))

    def test_every_stop_carries_the_mandatory_would_reopen_prose(self):
        for result in self.outcomes():
            if result.stop:
                with self.subTest(reason=result.reason):
                    self.assertTrue(result.would_reopen.strip())

    def test_a_continuation_is_never_a_stop_reason_under_another_name(self):
        for token in CONTINUE_REASONS:
            with self.subTest(token=token):
                self.assertNotIn(token, STOP_REASONS)

    def test_a_decision_without_would_reopen_is_refused_at_construction(self):
        with self.assertRaises(DecisionRefused) as caught:
            Decision(cycle=1, stop=True, reason=STOP_RESOURCE_BOUNDARY,
                     clause=CLAUSE_RESOURCE_BOUNDARY, would_reopen="  ")
        self.assertEqual(caught.exception.code, "DECISION_WOULD_REOPEN_MISSING")

    def test_a_reason_outside_both_vocabularies_is_refused(self):
        with self.assertRaises(DecisionRefused) as caught:
            Decision(cycle=1, stop=True, reason="ran_out_of_ideas",
                     clause=CLAUSE_NONE, would_reopen="prose")
        self.assertEqual(caught.exception.code, "DECISION_REASON_UNKNOWN")

    def test_malformed_arguments_are_refused_by_a_declared_code(self):
        good = self.at(cycle=1)
        cases = (
            (lambda: decide(None, object(), 1, self.config, self.obligations),
             "DECISION_SITUATION_INVALID"),
            (lambda: decide(object(), good, 1, self.config, self.obligations),
             "DECISION_SITUATION_INVALID"),
            (lambda: decide(None, good, "1", self.config, self.obligations),
             "DECISION_CYCLE_INVALID"),
            (lambda: decide(None, good, True, self.config, self.obligations),
             "DECISION_CYCLE_INVALID"),
            (lambda: decide(None, good, 1, object(), self.obligations),
             "DECISION_CONFIG_INVALID"),
            (lambda: decide(None, good, 1, self.config, object()),
             "DECISION_SITUATION_INVALID"),
            (lambda: decide(None, good, 1, self.config, self.obligations,
                            instrument=object()),
             "DECISION_INSTRUMENT_INVALID"),
            (lambda: decide(None, good, 1, self.config, self.obligations,
                            instrument={"block_rate": 3}),
             "DECISION_INSTRUMENT_INVALID"),
        )
        for call, code in cases:
            with self.subTest(code=code):
                with self.assertRaises(DecisionRefused) as caught:
                    call()
                self.assertEqual(caught.exception.code, code)
                self.assertIsInstance(caught.exception, LoopError)

    def test_the_config_may_be_the_frozen_mapping_rather_than_the_object(self):
        good = self.at(cycle=1)
        by_object = decide(None, good, 1, self.config, self.obligations)
        by_mapping = decide(None, good, 1, CONFIG, self.obligations)
        self.assertEqual(by_object.as_dict(), by_mapping.as_dict())


# ---------------------------------------------------------------------------
# Clause 1
# ---------------------------------------------------------------------------


class AProtectedLossStops(DecideTestCase):
    """Clause 1: any *p* lost stops the chain, the loss named and exposed."""

    def losing_pair(self):
        self.audit("2")
        before = self.at(cycle=2)
        self.blocker()
        return before, self.at(cycle=3)

    def test_a_protected_loss_stops_and_names_the_loss(self):
        before, after = self.losing_pair()
        result = decide(before, after, 2, self.config, self.obligations)
        self.assertTrue(result.stop)
        self.assertEqual(result.reason, STOP_PROTECTED_LOSS)
        self.assertEqual(result.clause, CLAUSE_PROTECTED_LOSS)
        self.assertEqual([loss.subject for loss in result.protected_losses], ["p8"])
        self.assertIn("p8", result.detail)

    def test_the_rendered_record_names_the_loss_and_claims_no_repair(self):
        before, after = self.losing_pair()
        text = render_decision(decide(before, after, 2, self.config, self.obligations))
        self.assertIn("## protected_losses", text)
        self.assertIn("p8 was satisfied, now not_satisfied", text)
        self.assertIn(REASON_SENTENCES[STOP_PROTECTED_LOSS][0], text)

    def test_the_loss_register_is_the_obligations_modules_and_is_not_recomputed(self):
        before, after = self.losing_pair()
        result = decide(before, after, 2, self.config, self.obligations)
        self.assertEqual([loss.as_dict() for loss in result.protected_losses],
                         [loss.as_dict() for loss in ob.protected_losses(before, after)])
        self.assertEqual([loss.as_dict() for loss in result.losses_outside_p],
                         [loss.as_dict() for loss in ob.losses_outside_p(before, after)])

    def test_a_protected_obligation_that_became_unreadable_is_not_a_loss(self):
        """FW5 R5: non-evaluability is exposed beside the register, never inside it."""
        obligations = self.write([("p6", "P", "no_aggregation")], name="p6.json")
        empty = situation(self.harness, 1, obligations)
        result = decide(None, empty, 1, self.config, obligations)
        self.assertEqual(result.protected_losses, ())
        self.assertEqual(result.protected_not_evaluable, ("p6",))
        text = render_decision(result)
        self.assertIn("## protected_not_evaluable", text)
        self.assertIn("- p6", text)

    def test_the_record_prints_protected_not_evaluable_beside_the_loss_register(self):
        before, after = self.losing_pair()
        text = render_decision(decide(before, after, 2, self.config, self.obligations))
        self.assertLess(text.index("## protected_losses"),
                        text.index("## protected_not_evaluable"))
        self.assertLess(text.index("## protected_not_evaluable"),
                        text.index("## losses_outside_P"))


# ---------------------------------------------------------------------------
# Clause 2 and clause 3
# ---------------------------------------------------------------------------


class ProducedByDecidesWhetherASatisfiedObligationContinues(DecideTestCase):
    """Clause 2 is a construction account, not temporal succession (FW5:800)."""

    def test_an_o_this_cycle_built_continues_the_chain(self):
        before = self.at(cycle=1)
        audited = self.audit("2")
        after = self.at(cycle=2, registered=[audited])
        result = decide(before, after, 2, self.config, self.obligations)
        self.assertFalse(result.stop)
        self.assertEqual(result.reason, CONTINUE_DISCHARGED)
        self.assertEqual(result.clause, CLAUSE_DISCHARGE)
        self.assertEqual(result.discharged, ("o5",))

    def test_the_same_satisfied_o_without_this_cycles_artifacts_does_not_continue(self):
        before = self.at(cycle=1)
        self.audit("2")
        after = self.at(cycle=2, registered=())
        self.assertEqual(after.obligations.pin, before.obligations.pin)
        result = decide(before, after, 2, self.config, self.obligations)
        self.assertNotEqual(result.reason, CONTINUE_DISCHARGED)
        self.assertNotEqual(result.clause, CLAUSE_DISCHARGE)
        self.assertEqual(result.discharged, ())

    def test_that_same_reading_stops_on_clause_three_instead(self):
        before = self.at(cycle=1)
        self.audit("2")
        after = self.at(cycle=2, registered=())
        result = decide(before, after, 2, self.config, self.obligations)
        self.assertTrue(result.stop)
        self.assertEqual(result.reason, STOP_OBLIGATIONS_DISCHARGED)
        self.assertEqual(result.clause, CLAUSE_ALL_SATISFIED)

    def test_an_artifact_registered_this_cycle_that_changes_nothing_discharges_nothing(self):
        audited = self.audit("2")
        before = self.at(cycle=2)
        spare = self.blocker()
        after = self.at(cycle=2, registered=[spare])
        self.assertIn(audited, after.nodes)
        result = decide(before, after, 2, self.config, self.obligations)
        self.assertNotEqual(result.clause, CLAUSE_DISCHARGE)

    def test_clause_three_reads_every_o_satisfied_and_not_the_absence_of_failures(self):
        """A not_evaluable member of O never terminates the chain."""
        obligations = self.write(
            [("o1", "O", "row_disposition_complete"), ("p8", "P", "appellate_optional")],
            name="unreadable.json")
        here = situation(self.harness, 1, obligations)
        reading = ob.evaluate(obligations, here)
        self.assertEqual(reading.not_evaluable, ("o1",))
        self.assertFalse(reading.every_o_satisfied)
        result = decide(None, here, 1, self.config, obligations)
        self.assertNotEqual(result.reason, STOP_OBLIGATIONS_DISCHARGED)
        self.assertEqual(result.not_evaluable, ("o1",))

    def test_before_cycle_one_there_is_no_prior_reading_and_the_first_build_continues(self):
        audited = self.audit("1")
        first = self.at(cycle=1, registered=[audited])
        result = decide(None, first, 1, self.config, self.obligations)
        self.assertEqual(result.reason, CONTINUE_DISCHARGED)
        self.assertEqual(result.discharged, ("o5",))


# ---------------------------------------------------------------------------
# Clause 4
# ---------------------------------------------------------------------------


class ClauseFourIsSetIdentity(DecideTestCase):
    """Integration decision 4: the set ``graph.mark_triples`` emits, compared
    for identity - never for a size, a fraction or a direction."""

    def unchanged_pair(self):
        before = self.at(cycle=1)
        return before, self.at(cycle=2)

    def test_mark_triples_is_the_graphs_own_set_and_not_a_second_spelling(self):
        self.assertEqual(mark_triples(self.harness), graph.mark_triples(self.harness))
        self.assertIsInstance(mark_triples(self.harness), frozenset)
        self.assertEqual(mark_triples(self.harness),
                         frozenset({(self.CELL, "T", "unresolved")}))

    def test_identical_triple_sets_stop_the_chain(self):
        before, after = self.unchanged_pair()
        triples = mark_triples(self.harness)
        result = decide(before, after, 2, self.config, self.obligations,
                        prev_triples=triples, curr_triples=triples)
        self.assertTrue(result.stop)
        self.assertEqual(result.reason, STOP_NO_NEW_READING_CHANGES)
        self.assertEqual(result.clause, CLAUSE_SET_IDENTITY)
        self.assertTrue(result.triples_identical)
        self.assertEqual(result.triples_entered, ())
        self.assertEqual(result.triples_left, ())

    def test_two_sets_of_the_same_size_but_different_members_do_not_stop(self):
        """The stop is a set identity and not a count: both sets hold one
        triple, and the chain continues because the triple is a different one."""
        before = self.at(cycle=1)
        earlier = mark_triples(self.harness)
        self.mark()
        later = mark_triples(self.harness)
        after = self.at(cycle=2)
        self.assertEqual(earlier, frozenset({(self.CELL, "T", "unresolved")}))
        self.assertEqual(later, frozenset({(self.CELL, "T", "differs")}))
        result = decide(before, after, 2, self.config, self.obligations,
                        prev_triples=earlier, curr_triples=later)
        self.assertFalse(result.stop)
        self.assertFalse(result.triples_identical)
        self.assertEqual(result.triples_entered, ((self.CELL, "T", "differs"),))
        self.assertEqual(result.triples_left, ((self.CELL, "T", "unresolved"),))

    def test_which_triples_moved_is_the_record_and_is_printed(self):
        before = self.at(cycle=1)
        earlier = mark_triples(self.harness)
        self.mark()
        text = render_decision(decide(
            before, self.at(cycle=2), 2, self.config, self.obligations,
            prev_triples=earlier, curr_triples=mark_triples(self.harness)))
        self.assertIn("## mark triples", text)
        self.assertIn(f"- entered: ({self.CELL}, T, differs)", text)
        self.assertIn(f"- left: ({self.CELL}, T, unresolved)", text)

    def test_an_unsupplied_prior_set_leaves_clause_four_silent_and_says_so(self):
        before, after = self.unchanged_pair()
        result = decide(before, after, 2, self.config, self.obligations,
                        curr_triples=mark_triples(self.harness))
        self.assertFalse(result.triples_compared)
        self.assertNotEqual(result.reason, STOP_NO_NEW_READING_CHANGES)
        self.assertIn("clause four was silent", render_decision(result))

    def test_at_cycle_one_there_is_no_prior_set_so_the_clause_cannot_fire(self):
        first = self.at(cycle=1)
        result = decide(None, first, 1, self.config, self.obligations,
                        curr_triples=mark_triples(self.harness))
        self.assertNotEqual(result.reason, STOP_NO_NEW_READING_CHANGES)


# ---------------------------------------------------------------------------
# Clause 5
# ---------------------------------------------------------------------------


class TheDeclaredBoundaryStop(DecideTestCase):
    """Clause 5: an attention-and-spend boundary, never an adjudication."""

    def budget_pair(self):
        self.audit("2")
        before = self.at(cycle=2)
        return before, self.at(cycle=3)

    def test_reaching_the_declared_budget_stops_as_a_resource_boundary(self):
        before, after = self.budget_pair()
        result = decide(before, after, self.config.cycle_budget, self.config,
                        self.obligations)
        self.assertTrue(result.stop)
        self.assertEqual(result.reason, STOP_RESOURCE_BOUNDARY)
        self.assertEqual(result.clause, CLAUSE_RESOURCE_BOUNDARY)

    def test_the_stop_carries_the_frozen_ceilings_boundary_sentence_verbatim(self):
        before, after = self.budget_pair()
        result = decide(before, after, self.config.cycle_budget, self.config,
                        self.obligations)
        self.assertIn(RESOURCE_BOUNDARY_SENTENCE, result.record_sentences)
        self.assertIn(RESOURCE_BOUNDARY_SENTENCE, standard.CEILING_REQUIRED_SENTENCES)
        self.assertIn(RESOURCE_BOUNDARY_SENTENCE, render_decision(result))

    def test_the_stop_carries_a_would_reopen_field(self):
        before, after = self.budget_pair()
        result = decide(before, after, self.config.cycle_budget, self.config,
                        self.obligations)
        self.assertEqual(result.would_reopen, WOULD_REOPEN[STOP_RESOURCE_BOUNDARY])
        text = render_decision(result)
        self.assertIn("## What would reopen this:", text)
        self.assertIn(result.would_reopen, text)

    def test_the_record_never_describes_the_boundary_as_the_inquiry_running_out(self):
        before, after = self.budget_pair()
        text = render_decision(decide(before, after, self.config.cycle_budget,
                                      self.config, self.obligations))
        standard.assert_no_exhaustion_claim(text, "decision record")
        self.assertIn(standard.CEILING_EXHAUSTION_DENIAL, text)

    def test_the_declared_call_budget_is_reported_and_not_recomputed_here(self):
        before, after = self.budget_pair()
        result = decide(before, after, 2, self.config, self.obligations,
                        instrument=Instrument(calls_reached=True))
        self.assertEqual(result.reason, STOP_RESOURCE_BOUNDARY)
        self.assertIn(str(self.config.max_calls), result.detail)

    def test_a_cycle_inside_the_budget_does_not_stop_on_this_clause(self):
        before, after = self.budget_pair()
        result = decide(before, after, 2, self.config, self.obligations)
        self.assertNotEqual(result.reason, STOP_RESOURCE_BOUNDARY)

    def test_the_boundary_predicate_is_the_one_place_the_cycle_index_is_compared(self):
        self.assertEqual(
            declared_boundary_reached(2, self.config, Instrument()), "")
        self.assertIn("reached the declared budget",
                      declared_boundary_reached(3, self.config, Instrument()))


# ---------------------------------------------------------------------------
# The guard rails
# ---------------------------------------------------------------------------


class TheGuardRailsComeFirst(DecideTestCase):
    """Design section 5 clause 6: evaluated before 1-5, and never reading a cell."""

    def losing_pair(self):
        self.audit("2")
        before = self.at(cycle=2)
        self.blocker()
        return before, self.at(cycle=3)

    def test_a_halted_step_stops_as_custody_halt_before_clause_one(self):
        before, after = self.losing_pair()
        self.assertTrue(ob.protected_losses(before, after))
        result = decide(before, after, 2, self.config, self.obligations,
                        instrument=Instrument(custody_halted=True,
                                              halted_step="0007-SEND"))
        self.assertEqual(result.reason, STOP_CUSTODY_HALT)
        self.assertEqual(result.clause, CLAUSE_CUSTODY_HALT)
        self.assertIn("0007-SEND", result.detail)

    def test_every_arm_ended_stops_as_all_arms_ended(self):
        before, after = self.losing_pair()
        result = decide(before, after, 2, self.config, self.obligations,
                        instrument=Instrument(arms_ended=True,
                                              ended_arms=("mini_fcl", "mini_prose")))
        self.assertEqual(result.reason, STOP_ALL_ARMS_ENDED)
        self.assertEqual(result.clause, CLAUSE_ALL_ARMS_ENDED)
        self.assertIn(ALL_ARMS_ENDED_SENTENCE, render_decision(result))

    def test_a_block_streak_above_the_declared_bound_stops_as_instrument_fault(self):
        before = self.at(cycle=1)
        after = self.at(cycle=2)
        result = decide(before, after, 2, self.config, self.obligations,
                        instrument=Instrument(block_streak=9))
        self.assertEqual(result.reason, STOP_INSTRUMENT_FAULT)
        self.assertEqual(result.clause, CLAUSE_INSTRUMENT_FAULT)

    def test_the_instrument_fault_names_a_fault_in_the_instrument(self):
        before = self.at(cycle=1)
        result = decide(before, self.at(cycle=2), 2, self.config, self.obligations,
                        instrument=Instrument(block_streak=9))
        text = render_decision(result)
        self.assertIn("This is a fault in the instrument, not a finding about "
                      "the material.", text)
        self.assertIn("It is never an absence of relations.", text)

    def test_the_declared_bound_is_rendered_beside_the_account_that_justifies_it(self):
        result = instrument_bound_crossed(
            Instrument(block_streak=9), self.config)
        self.assertIn(str(self.config.audit.streak_max), result)
        self.assertIn(self.config.audit.streak_max_account, result)

    def test_a_calibration_error_above_the_declared_bound_stops_as_instrument_fault(self):
        before = self.at(cycle=1)
        result = decide(before, self.at(cycle=2), 2, self.config, self.obligations,
                        instrument=Instrument(judge_err_observed=0.6))
        self.assertEqual(result.reason, STOP_INSTRUMENT_FAULT)
        self.assertIn(self.config.audit.judge_err_max_account, result.detail)

    def test_a_bound_the_driver_did_not_report_is_not_crossed(self):
        self.assertEqual(instrument_bound_crossed(Instrument(), self.config), "")
        self.assertEqual(
            instrument_bound_crossed(Instrument(block_streak=1), self.config), "")
        self.assertEqual(
            instrument_bound_crossed(Instrument(judge_err_observed=0.1), self.config), "")

    def test_an_absent_instrument_report_is_an_all_clear_one(self):
        before = self.at(cycle=1)
        after = self.at(cycle=2)
        self.assertEqual(decide(before, after, 2, self.config, self.obligations).clause,
                         decide(before, after, 2, self.config, self.obligations,
                                instrument=Instrument()).clause)

    def test_the_guard_rails_read_no_cell(self):
        """Nothing on the instrument report is a cell, a mark or a reading."""
        for name in Instrument().as_dict():
            with self.subTest(field=name):
                self.assertNotIn("cell", name)
                self.assertNotIn("mark", name)
                self.assertNotIn("reading", name)

    def test_the_instrument_report_accepts_its_mapping_form_and_refuses_strangers(self):
        self.assertEqual(Instrument.of({"custody_halted": True}),
                         Instrument(custody_halted=True))
        self.assertEqual(Instrument.of(None), Instrument())
        with self.assertRaises(DecisionRefused):
            Instrument.of({"unknown_signal": True})


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------


class TheDecisionRecord(DecideTestCase):

    def any_decision(self, **kwargs) -> Decision:
        before = self.at(cycle=1)
        return decide(before, self.at(cycle=2), 2, self.config, self.obligations,
                      **kwargs)

    def test_losses_outside_p_is_a_section_present_even_when_empty(self):
        result = self.any_decision()
        self.assertEqual(result.losses_outside_p, ())
        text = render_decision(result)
        self.assertIn("## losses_outside_P", text)
        section = text.split("## losses_outside_P")[1].split("##")[0]
        self.assertIn("- none", section)

    def test_the_record_says_a_cycle_may_be_net_withdrawal_and_still_be_progress(self):
        text = render_decision(self.any_decision())
        self.assertIn("A cycle may be net withdrawal and still be progress", text)

    #: ``REASON_SENTENCES`` and ``WOULD_REOPEN`` are keyed by the PREFIX for the
    #: one parameterised stop reason, because the reason itself carries the
    #: condition's id (decision 28(d)). A test that walks the tables has to turn
    #: that key back into a usable reason before building a Decision from it.
    @staticmethod
    def reason_for_key(key: str) -> str:
        if key == loop_types.PREREGISTERED_CONDITION_PREFIX:
            return f"{key}material-withdrawn"
        return key

    def test_every_record_sentence_of_every_reason_is_emitted_verbatim(self):
        for key, sentences in REASON_SENTENCES.items():
            reason = self.reason_for_key(key)
            stop = reason not in CONTINUE_REASONS
            clause = CLAUSE_RESOURCE_BOUNDARY if stop else CLAUSE_NONE
            result = Decision(cycle=1, stop=stop, reason=reason, clause=clause,
                              would_reopen=WOULD_REOPEN[key],
                              record_sentences=(*sentences, *ALWAYS_SENTENCES))
            text = render_decision(result)
            for sentence in (*sentences, *ALWAYS_SENTENCES):
                with self.subTest(reason=reason, sentence=sentence[:40]):
                    self.assertIn(sentence, text)

    def test_the_rendered_record_carries_no_scoring_heading(self):
        standard.assert_no_scoring_headers(render_decision(self.any_decision()),
                                           "decision record")

    def test_no_rendered_record_describes_a_boundary_as_the_inquiry_running_out(self):
        for key in REASON_SENTENCES:
            reason = self.reason_for_key(key)
            stop = reason not in CONTINUE_REASONS
            result = Decision(
                cycle=1, stop=stop, reason=reason,
                clause=CLAUSE_RESOURCE_BOUNDARY if stop else CLAUSE_NONE,
                would_reopen=WOULD_REOPEN[key],
                record_sentences=(*REASON_SENTENCES[key], *ALWAYS_SENTENCES))
            with self.subTest(reason=reason):
                standard.assert_no_exhaustion_claim(render_decision(result))

    def test_a_record_that_misdescribed_the_boundary_is_refused_at_the_renderer(self):
        result = Decision(cycle=1, stop=True, reason=STOP_RESOURCE_BOUNDARY,
                          clause=CLAUSE_RESOURCE_BOUNDARY,
                          would_reopen="the inquiry is exhausted")
        with self.assertRaises(standard.StandardInvalid) as caught:
            render_decision(result)
        self.assertEqual(caught.exception.code, "RESOURCE_BOUNDARY_MISDESCRIBED")

    def test_render_decision_takes_a_decision_and_nothing_else(self):
        with self.assertRaises(DecisionRefused):
            render_decision({"stop": True})

    def test_the_record_is_deterministic(self):
        self.assertEqual(render_decision(self.any_decision()),
                         render_decision(self.any_decision()))

    def test_the_record_names_the_obligations_pin_it_was_read_under(self):
        result = self.any_decision()
        self.assertEqual(result.obligations_pin, self.obligations.pin)
        self.assertIn(self.obligations.pin, render_decision(result))


# ---------------------------------------------------------------------------
# The hard rule
# ---------------------------------------------------------------------------


class NoClauseIsAMeter(DecideTestCase):
    """No clause reads a quantity of readings, marks, endpoints or differs.

    The same syntax-tree rule ``tests/loop/test_obligations.py`` applies to
    W1-OBLIGATIONS, with one addition this module needs: the three numeric
    comparisons the design does admit are *instrument bounds*, and each must
    live inside one of the two named functions that own them.
    """

    FORBIDDEN = frozenset({
        "count", "counts", "rate", "rates", "threshold", "thresholds", "score",
        "scores", "scoring", "ratio", "percent", "percentage", "mean", "median",
        "average", "avg", "total", "sum", "tally", "majority", "weighted", "num",
        "n", "quantity", "amount", "many", "size", "length", "len", "rank",
    })
    ARITHMETIC = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod,
                  ast.Pow, ast.MatMult, ast.LShift, ast.RShift)
    ORDERING = (ast.Gt, ast.GtE, ast.Lt, ast.LtE)
    BANNED_CALLS = frozenset({"len", "sum", "min", "max", "abs", "round"})

    #: The only functions an ordering comparison may appear in: the two
    #: the pre-registration names as instrument bounds, and nothing else.
    ORDERING_ALLOWED = ("instrument_bound_crossed", "declared_boundary_reached")

    @staticmethod
    def exempt_constants(tree) -> set:
        """Numeric literals an index may legitimately carry.

        The slice ITSELF (``row[1]``), or a bound of a ``Slice`` (``span[2:3]``)
        - not every constant anywhere inside a subscript's subtree, which is
        what the exemption used to be (REVIEW-WAVE1 S5).
        """

        exempt = set()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Subscript):
                continue
            inner = node.slice
            if isinstance(inner, ast.Constant):
                exempt.add(inner.value)
            elif isinstance(inner, ast.Slice):
                for bound in (inner.lower, inner.upper, inner.step):
                    if isinstance(bound, ast.Constant):
                        exempt.add(bound.value)
            elif isinstance(inner, ast.UnaryOp) and isinstance(inner.operand,
                                                               ast.Constant):
                exempt.add(inner.operand.value)
        return exempt

    def enclosing_function(self, target) -> str:
        """The name of the function a node sits in, or "" at module level."""

        for node in ast.walk(self.tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for inner in ast.walk(node):
                if inner is target:
                    return node.name
        return ""

    # -- REVIEW-WAVE1 S5: the guard's own holes, each closed and probed ------ #

    #: Comparison operators that read a MAGNITUDE. ``==`` and ``!=`` are not
    #: here: set identity and token equality are the two things this program is
    #: allowed to do, and clause four is exactly a set-identity test.
    ORDERING = (ast.Lt, ast.LtE, ast.Gt, ast.GtE)

    #: Callables that produce, order or tally a quantity. ``sorted`` is banned
    #: for a different reason from ``len``: an ORDER over readings is the rank
    #: the vocabulary has no room for. A sort of record IDS or of a rendered
    #: block, which is what this module actually does, goes through
    #: ``_ordered``/``sorted`` at a call site the exemption below names.
    BANNED_ORDERING_CALLS = frozenset({"statistics", "Counter", "mean", "median"})

    def test_the_module_compares_no_magnitudes(self):
        """S5: ``>`` and ``<`` were not in the arithmetic assertion at all.

        A module that computes no arithmetic can still read a threshold, and a
        ``>`` is how it would. Every ordering comparison in these two modules
        is either absent or, where one is the pre-registered instrument bound,
        confined to the function the decision names.
        """

        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Compare):
                continue
            for operator in node.ops:
                if not isinstance(operator, self.ORDERING):
                    continue
                where = self.enclosing_function(node)
                with self.subTest(line=node.lineno, function=where):
                    self.assertIn(where, self.ORDERING_ALLOWED,
                                  "an ordering comparison outside the functions "
                                  "the pre-registration names")

    def test_the_module_imports_no_statistics_and_counts_nothing(self):
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = ([alias.name for alias in node.names]
                         + [getattr(node, "module", "") or ""])
                for name in names:
                    with self.subTest(imported=name):
                        self.assertNotIn(name.split(".")[0].casefold(),
                                         {"statistics", "collections", "numpy"})
            if isinstance(node, ast.Call):
                name = getattr(node.func, "id", getattr(node.func, "attr", ""))
                with self.subTest(call=name):
                    self.assertNotIn(name, self.BANNED_ORDERING_CALLS)

    def test_the_token_scan_is_case_folded(self):
        """S5: ``Count`` and ``COUNT`` walked past a case-sensitive membership."""

        for spelling in ("Count", "COUNT", "Rank", "TALLY", "Score"):
            with self.subTest(spelling=spelling):
                self.assertEqual(self.tokens(spelling.casefold()) & self.FORBIDDEN,
                                 {spelling.casefold()})

    def test_the_numeric_exemption_covers_only_a_constant_that_is_the_slice(self):
        """S5: the exemption used to cover every Constant ANYWHERE in a slice.

        ``table[compute(2 * 3)]`` was exempt because both literals were inside
        a ``Subscript.slice`` subtree. The exemption is now the slice itself,
        or a literal directly inside a slice's ``Slice`` bounds.
        """

        tree = ast.parse("table[compute(7)]\nrow[1]\nspan[2:3]\n")
        exempt = self.exempt_constants(tree)
        found = {node.value for node in ast.walk(tree)
                 if isinstance(node, ast.Constant)}
        self.assertEqual(found - exempt, {7},
                         "a literal buried in a call inside a slice is not an index")
        self.assertEqual({1, 2, 3} - exempt, set())
    #: The only two functions admitted to compare numbers, and what each bounds.
    BOUND_FUNCTIONS = {
        "instrument_bound_crossed": "the block streak and the calibration error",
        "declared_boundary_reached": "the cycle index against the declared budget",
    }

    @classmethod
    def setUpClass(cls) -> None:
        cls.tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        cls.docstrings = set()
        for node in ast.walk(cls.tree):
            body = getattr(node, "body", None)
            if not isinstance(body, list) or not body:
                continue
            head = body[0]
            if isinstance(head, ast.Expr) and isinstance(head.value, ast.Constant):
                if isinstance(head.value.value, str):
                    cls.docstrings.add(id(head.value))

    def tokens(self, identifier: str) -> set[str]:
        return {part.lower() for part in str(identifier).split("_") if part}

    def test_no_identifier_names_a_count_a_rate_a_threshold_or_a_score(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Name):
                found = node.id
            elif isinstance(node, ast.arg):
                found = node.arg
            elif isinstance(node, ast.Attribute):
                found = node.attr
            elif isinstance(node, ast.keyword):
                found = node.arg or ""
            elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                found = node.name
            else:
                continue
            if found.startswith("no_"):
                continue
            with self.subTest(identifier=found):
                self.assertEqual(self.tokens(found) & self.FORBIDDEN, set())

    def test_no_string_outside_a_docstring_names_one(self):
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Constant) or id(node) in self.docstrings:
                continue
            if not isinstance(node.value, str):
                continue
            words = node.value.replace(".", " ").replace("_", " ").replace("-", " ")
            with self.subTest(text=node.value[:60]):
                self.assertEqual(
                    {word.lower() for word in words.split()} & self.FORBIDDEN, set())

    def test_the_module_computes_no_arithmetic(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.BinOp):
                self.assertNotIsInstance(node.op, self.ARITHMETIC)
            if isinstance(node, ast.AugAssign):
                self.assertNotIsInstance(node.op, self.ARITHMETIC)

    def test_the_module_carries_no_numeric_literal_outside_a_subscript(self):
        indexed = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Subscript):
                for inner in ast.walk(node.slice):
                    if isinstance(inner, ast.Constant):
                        indexed.add(id(inner))
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Constant) and id(node) not in indexed:
                with self.subTest(line=node.lineno):
                    self.assertNotIn(type(node.value), (int, float))

    def test_the_module_calls_no_counting_builtin(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertNotIn(node.func.id, self.BANNED_CALLS)

    def test_every_numeric_comparison_lives_in_one_of_the_two_bound_functions(self):
        found = set()
        for function in ast.walk(self.tree):
            if not isinstance(function, ast.FunctionDef):
                continue
            for node in ast.walk(function):
                if not isinstance(node, ast.Compare):
                    continue
                if not any(isinstance(op, self.ORDERING) for op in node.ops):
                    continue
                with self.subTest(function=function.name, line=node.lineno):
                    self.assertIn(function.name, self.BOUND_FUNCTIONS)
                found.add(function.name)
        self.assertEqual(found, set(self.BOUND_FUNCTIONS))

    def test_the_two_bound_functions_document_what_they_bound(self):
        for name in self.BOUND_FUNCTIONS:
            with self.subTest(function=name):
                self.assertIn("bound", getattr(mod, name).__doc__)

    def test_the_decision_record_carries_no_number_but_the_cycle_index(self):
        before = self.at(cycle=1)
        record = decide(before, self.at(cycle=2), 2, self.config,
                        self.obligations).as_dict()
        self.assertEqual(record["cycle"], 2)

        def walk(value, where):
            if isinstance(value, dict):
                for key, nested in value.items():
                    walk(nested, f"{where}.{key}")
            elif isinstance(value, list):
                for item in value:
                    walk(item, where)
            elif not isinstance(value, bool):
                with self.subTest(where=where):
                    self.assertNotIsInstance(value, (int, float), where)

        for key, value in record.items():
            if key != "cycle":
                walk(value, key)

    def test_no_clause_reads_a_quantity_of_readings_marks_or_endpoints(self):
        """Every clause quantifies over sets and verdicts, never over sizes."""
        before = self.at(cycle=1)
        self.mark()
        result = decide(before, self.at(cycle=2), 2, self.config, self.obligations,
                        prev_triples=frozenset(), curr_triples=mark_triples(self.harness))
        for word in ("count", "rate", "score", "threshold", "average"):
            with self.subTest(word=word):
                self.assertNotIn(word, result.detail.lower())
                self.assertNotIn(word, result.reason.lower())
                self.assertNotIn(word, result.clause.lower())


# ---------------------------------------------------------------------------
# The two readings the decision quantifies over
# ---------------------------------------------------------------------------


class TheReadingsTheDecisionQuantifiesOver(DecideTestCase):

    def test_situation_reads_the_harness_under_the_pinned_obligations(self):
        here = situation(self.harness, 2, self.obligations)
        self.assertIsInstance(here, ob.Situation)
        self.assertEqual(here.cycle, 2)
        self.assertEqual(here.obligations.pin, self.obligations.pin)
        self.assertEqual(here.registered, frozenset())

    def test_situation_accepts_a_production_record_as_this_cycles_registrations(self):
        produced = graph.produced(self.harness)
        here = situation(self.harness, 1, self.obligations, registered=produced)
        self.assertEqual(here.registered, produced.artifact_ids)

    def test_situation_writes_nothing_to_the_graph(self):
        before = [event.seq for event in self.harness.log.read()]
        situation(self.harness, 1, self.obligations)
        mark_triples(self.harness)
        self.assertEqual([event.seq for event in self.harness.log.read()], before)

    def test_a_situation_pinned_to_another_document_is_refused(self):
        other = self.write([("o5", "O", "audit_in_force")], name="other.json")
        here = situation(self.harness, 1, other)
        with self.assertRaises(ob.ObligationsError) as caught:
            decide(None, here, 1, self.config, self.obligations)
        self.assertEqual(caught.exception.code, "OBLIGATIONS_PIN_SHIFTED")


# ---------------------------------------------------------------------------
# The declared entry points, and the one that could not be restored
# ---------------------------------------------------------------------------


class TheDeclaredEntryPoints(DecideTestCase):
    """Wave-2 integration: the two judge findings of family C, pinned.

    Finding 1 is the ``situation`` signature. The wave plan declares
    ``situation(harness, cycle)``; what is implemented takes the pinned
    obligations as a third argument, and deviation 3 of the module docstring
    records why the declared entry cannot be restored. These tests are that
    decision's teeth: the signature is asserted, and so is each of the three
    facts the deviation rests on, so that a later agent "simplifying" the entry
    back to two arguments has to delete a test that says what breaks.
    """

    def test_the_implemented_signature_is_the_one_the_deviation_declares(self):
        import inspect

        signature = inspect.signature(situation)
        self.assertEqual(list(signature.parameters),
                         ["harness", "cycle", "obligations", "registered"])
        obligations_parameter = signature.parameters["obligations"]
        self.assertIs(obligations_parameter.default, inspect.Parameter.empty)
        self.assertEqual(obligations_parameter.kind,
                         inspect.Parameter.POSITIONAL_OR_KEYWORD)
        self.assertEqual(signature.parameters["registered"].kind,
                         inspect.Parameter.KEYWORD_ONLY)

    def test_the_declared_two_argument_entry_is_a_type_error_and_not_a_guess(self):
        with self.assertRaises(TypeError):
            situation(self.harness, 1)

    def test_a_situation_is_defined_relative_to_obligations_it_carries(self):
        """Why the third argument cannot be optional: it is a FIELD of the value."""

        here = self.at(1)
        self.assertIs(here.obligations, self.obligations)
        self.assertIn("obligations", {f.name for f in dataclasses.fields(here)})

    def test_the_obligations_document_is_not_in_the_graph_to_be_found(self):
        """The other half: ``harness`` could not supply what it does not hold."""

        self.assertNotIn("obligations", ob.RECORD_KINDS)
        self.assertEqual(
            [name for name in dir(graph) if "obligation" in name.lower()], [])

    def test_an_empty_obligations_document_would_discharge_nothing_silently(self):
        """Why an empty default would be worse than the deviation.

        A situation built against an empty O answers every question with a
        verdict other than SATISFIED, so ``decide`` would read "nothing was
        discharged" off a well-formed value and clause 2 would never fire. A
        missing argument is a TypeError at the call; this would be a wrong
        decision in a published record.
        """

        empty = self.write([], name="empty.json")
        self.assertEqual(empty.failed, ())
        self.assertEqual(empty.protected, ())
        here = situation(self.harness, 1, empty)
        outcome = decide(None, here, 1, self.config, empty)
        self.assertEqual(outcome.discharged, ())
        self.assertNotEqual(outcome.clause, CLAUSE_DISCHARGE)

    def test_the_module_pin_key_names_this_file_and_is_not_one_of_the_fixed_six(self):
        """Decision 28(h): the driver folds DECIDE_SHA256 in under this key."""

        self.assertEqual(mod.MODULE_PIN_KEY, "src/minireason/loop/decide.py")
        self.assertNotIn(mod.MODULE_PIN_KEY, loop_types.PINNED_SOURCE_PATHS)
        source = Path(mod.__file__).resolve()
        self.assertTrue(str(source).endswith(mod.MODULE_PIN_KEY))
        self.assertEqual(mod.DECIDE_SHA256,
                         hashlib.sha256(source.read_bytes()).hexdigest())


class ADeclaredConditionIsEvaluatedAfterEveryClause(DecideTestCase):
    """Wave-1 integration decision 28(d), applied.

    ``preregistered_condition:<id>`` is ``types.STOP_REASONS``' one
    parameterised member and no clause of the five can produce one: it is the
    pre-registration's condition and the driver's observation. It is therefore
    tested last, so it masks nothing.
    """

    def observed(self, condition: str, **rest):
        return mod.Instrument(preregistered_condition=condition, **rest)

    def test_a_declared_condition_stops_the_chain_when_no_clause_did(self):
        outcome = decide(None, self.at(1), 1, self.config, self.obligations,
                         instrument=self.observed("material-withdrawn"))
        self.assertTrue(outcome.stop)
        self.assertEqual(outcome.reason,
                         "preregistered_condition:material-withdrawn")
        self.assertEqual(outcome.clause, mod.CLAUSE_PREREGISTERED_CONDITION)
        self.assertTrue(is_stop_reason(outcome.reason))
        self.assertTrue(outcome.would_reopen.strip())

    def test_it_masks_no_clause_because_it_is_evaluated_after_all_of_them(self):
        self.assertEqual(mod.CLAUSE_ORDER[-2], mod.CLAUSE_PREREGISTERED_CONDITION)
        self.assertEqual(mod.CLAUSE_ORDER[-1], mod.CLAUSE_NONE)
        self.assertGreater(
            mod.CLAUSE_ORDER.index(mod.CLAUSE_PREREGISTERED_CONDITION),
            mod.CLAUSE_ORDER.index(CLAUSE_RESOURCE_BOUNDARY))

    def test_a_custody_halt_still_wins_over_a_declared_condition(self):
        outcome = decide(None, self.at(1), 1, self.config, self.obligations,
                         instrument=self.observed("material-withdrawn",
                                                  custody_halted=True,
                                                  halted_step="0007-SEND"))
        self.assertEqual(outcome.reason, mod.STOP_CUSTODY_HALT)

    def test_the_declared_boundary_still_wins_over_a_declared_condition(self):
        outcome = decide(None, self.at(9), 9, self.config, self.obligations,
                         instrument=self.observed("material-withdrawn"))
        self.assertEqual(outcome.reason, mod.STOP_RESOURCE_BOUNDARY)

    def test_a_condition_id_naming_exhaustion_is_refused_at_the_report(self):
        with self.assertRaises(mod.DecisionRefused) as caught:
            self.observed("exhausted-the-material")
        self.assertEqual(caught.exception.code, mod.DECISION_INSTRUMENT_INVALID)

    def test_the_rendered_record_names_the_condition_and_no_magnitude(self):
        outcome = decide(None, self.at(1), 1, self.config, self.obligations,
                         instrument=self.observed("material-withdrawn"))
        text = render_decision(outcome)
        self.assertIn("material-withdrawn", text)
        self.assertIn(mod.PREREGISTERED_CONDITION_SENTENCE, text)
        standard.assert_no_exhaustion_claim(text)
        standard.assert_no_scoring_headers(text, "decision record")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
