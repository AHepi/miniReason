"""W1-GRAPH — how readings and marks enter the graph, and how they leave it again.

Every assertion here is about the *calculus*, not about a convenience: the unresolved
default is accepted because nothing attacks it, a reading displaces it because a warrant
does, and refuting the standard, hitting the seat in an audit or ruling on appeal all
reinstate it through the vendored closures in pass 1 — with no delete, no rewrite, and no
status rule outside ``att`` and ``dep``.

The design of record is §3 of the automated-loop design; §2.4 G2b/G12 and §2.5 supply the
transcript and audit conditions the W1-GRAPH wave-plan entry lists as acceptance.
"""

from __future__ import annotations

import ast
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from deepreason_core.harness import Harness, conforming_transcript
from deepreason_core.ontology import (
    Artifact,
    LLMCall,
    Provenance,
    Status,
    Warrant,
    WarrantType,
)

from minireason.loop import graph as g
from minireason.loop.contracts import ScoringKeyForbidden
from minireason.loop.standard import (
    DIFFERENCE_KINDS,
    FORBIDDEN_KEYS,
    MARKS,
    READING_VOCABULARY,
    REGISTER_IDS,
    STANDARD_BODY,
)
from minireason.loop.types import LoopError

MODULE = Path(g.__file__).resolve()


def module_source() -> str:
    return MODULE.read_text(encoding="utf-8")


def transcript(point: str = "without qualification") -> g.Transcript:
    """A conforming transcript whose decisive point occurs exactly once in the exchange."""
    return g.Transcript(
        case="the later record re-deploys the earlier term without qualification",
        answer="the defence disputes that the two terms are the same term at all",
        decisive_point=point,
        checks={"unique_offset": True, "order_swap": "agreed", "paraphrase": "held"},
        meta={"pack_sha": "a" * 64, "raw_refs": ["b" * 64]},
    )


def mark_transcript(point: str = "the target set differs") -> g.Transcript:
    """A pairwise mark's transcript; the decisive point is unique in the exchange."""
    return g.Transcript(
        case="ORIGINAL names o1 where CONTROL names o2, so the target set differs",
        answer="the defence concedes the two commitments do not name one target",
        decisive_point=point,
        checks={"order_swap": "agreed", "baseline_kind": "absent"},
    )


def attack(harness: Harness, target_id: str, note: str) -> tuple[str, str]:
    """An ordinary argumentative attack, exactly as ``tests/graph_core/helpers`` mints one.

    Deliberately *not* built through :mod:`minireason.loop.graph`: the closures under test
    must fire for any registered attacker, not only for one this module authored.
    """
    nu = harness.create_artifact(
        f"nu: the attack {note!r} is sound and relevant",
        provenance=Provenance(role="user"))
    warrant = Warrant(id=f"w-{note}", target=target_id,
                      type=WarrantType.ARGUMENTATIVE, validity_node=nu.id)
    critic = harness.create_artifact(
        f"critic: {note}", provenance=Provenance(role="critic"), warrants=[warrant])
    return critic.id, nu.id


class GraphTestCase(unittest.TestCase):
    """One harness on a deterministic clock, one standard, one row, two open cells."""

    CELL = "r1/c1"
    REGISTER_CELL = g.CellKey("r1/c1", "T", "original-vs-control")

    def setUp(self) -> None:
        super().setUp()
        self.tmp = Path(tempfile.mkdtemp(prefix="loop-graph-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.root = self.tmp / "graph"
        self.harness = g.open_graph(self.root, clock=g.fixed_clock())
        self.standard = g.register_standard(self.harness, STANDARD_BODY)
        self.material = g.register_material(self.harness, b'{"row_key": "r1", "cells": {}}')
        self.cells = g.open_cells(
            self.harness, [self.CELL, self.REGISTER_CELL], material_id=self.material)

    # -- builders -------------------------------------------------------------

    def reading(self, relation: str = "re-deploys", *, seat: str = "judge-1",
                point: str = "without qualification", **kwargs) -> g.ReadingIds:
        result = g.ReadingResult(
            key=g.CellKey(self.CELL), relation=relation, seat=seat,
            transcript=transcript(point), material_id=self.material,
            school="family-a+family-b",
            roles={"critic": "seat-c", "defender": "seat-d", "judge": seat},
            body=kwargs.pop("body", {"offsets": [[0, 21]]}),
            **kwargs)
        return g.register_reading(self.harness, result, self.standard)

    def mark(self, token: str = "differs", *, kind: str | None = "target_set_membership",
             seat: str = "judge-1", key: g.CellKey | None = None) -> g.ReadingIds:
        result = g.ReadingResult(
            key=key or self.REGISTER_CELL, relation=token, seat=seat,
            transcript=mark_transcript(), difference_kind=kind,
            material_id=self.material)
        return g.register_mark(self.harness, result, self.standard)

    def status(self, artifact_id: str) -> Status:
        return self.harness.state.status[artifact_id]


# --------------------------------------------------------------------------- (1)

class TheTableStartsEntirelyUnresolved(GraphTestCase):
    """§3(c): the unresolved default is registered first and is accepted because nothing
    attacks it — the table does not start unresolved by decree."""

    def test_the_default_is_unresolved_before_any_reading(self):
        self.assertEqual(g.cell_state(self.harness, self.CELL), g.UNRESOLVED)
        self.assertEqual(
            g.cell_state(self.harness, self.REGISTER_CELL.token), g.UNRESOLVED)

    def test_the_default_is_accepted_by_pass_one_not_by_a_status_rule(self):
        default = self.cells[self.CELL]
        self.assertEqual(self.status(default), Status.ACCEPTED)
        self.assertEqual(
            [edge for edge in self.harness.state.att if edge[1] == default], [])

    def test_the_default_body_is_the_designs_own_shape(self):
        artifact = self.harness.state.artifacts[self.cells[self.CELL]]
        body = json.loads(self.harness.blobs.get(artifact.content_ref))
        self.assertEqual(body["cell"], self.CELL)
        self.assertEqual(body["state"], "unresolved")
        self.assertEqual(body["schema"], g.CELL_OPEN_SCHEMA)
        self.assertNotIn("register", body)

    def test_the_default_declares_the_rubric_commitment_and_depends_on_the_material(self):
        artifact = self.harness.state.artifacts[self.cells[self.CELL]]
        commitment = self.harness.commitments[artifact.interface.commitments[0]]
        self.assertEqual(commitment.eval, "rubric:reading-v1")
        self.assertEqual(
            [(r.target, r.role.value) for r in artifact.interface.refs],
            [(self.material, "dependence")])

    def test_registering_the_standard_twice_registers_nothing_twice(self):
        before = list(self.harness.log.read())
        again = g.register_standard(self.harness, STANDARD_BODY)
        self.assertEqual(again, self.standard)
        g.open_cells(self.harness, [self.CELL], material_id=self.material)
        self.assertEqual([e.seq for e in self.harness.log.read()],
                         [e.seq for e in before])

    def test_a_standing_is_refused_for_a_cell_that_was_never_opened(self):
        with self.assertRaises(g.GraphError) as caught:
            g.cell_state(self.harness, "r9/c9")
        self.assertEqual(caught.exception.code, "CELL_NOT_OPEN")

    def test_a_reading_is_refused_before_its_default_exists(self):
        result = g.ReadingResult(key=g.CellKey("r9/c9"), relation="retains",
                                 seat="judge-1", transcript=transcript())
        with self.assertRaises(g.GraphError) as caught:
            g.register_reading(self.harness, result, self.standard)
        self.assertEqual(caught.exception.code, "CELL_NOT_OPEN")


# --------------------------------------------------------------------------- (2)

class AGuardedReadingDisplacesTheDefault(GraphTestCase):
    """§3(d)-(f): the reading attacks its own default and nothing else, and the vendored
    gate refuses it outright without a conforming trial transcript."""

    def test_a_guarded_reading_is_accepted_and_the_default_no_longer_stands(self):
        ids = self.reading()
        self.assertEqual(self.status(ids.reading), Status.ACCEPTED)
        # The design's "suspended" is the vendored `refuted`: a default with an accepted
        # attacker. `suspended` in that vocabulary means an attack pass 1 could not settle.
        self.assertEqual(self.status(ids.target), Status.REFUTED)
        standing = g.cell_standing(self.harness, self.CELL)
        self.assertEqual(standing.state, g.READ)
        self.assertEqual(standing.relation, "re-deploys")
        self.assertEqual(standing.accepted, (ids.reading,))

    def test_the_warrant_is_demonstrative_rubric_typed_and_carries_the_transcript(self):
        ids = self.reading()
        warrant = self.harness.warrants[ids.warrant]
        self.assertEqual(warrant.type, WarrantType.DEMONSTRATIVE)
        self.assertEqual(warrant.target, ids.target)
        self.assertEqual(warrant.validity_node, ids.soundness)
        self.assertTrue(
            self.harness.commitments[warrant.commitment].eval.startswith("rubric:"))
        self.assertTrue(conforming_transcript(self.harness.blobs, warrant.trace_ref))

    def test_registration_is_refused_when_the_decisive_point_is_not_unique(self):
        doubled = g.Transcript(
            case="the term is re-deployed and the term is re-deployed",
            answer="the defence disputes it",
            decisive_point="the term is re-deployed",
            checks={"unique_offset": False})
        result = g.ReadingResult(key=g.CellKey(self.CELL), relation="re-deploys",
                                 seat="judge-1", transcript=doubled)
        with self.assertRaises(g.GraphError) as caught:
            g.register_reading(self.harness, result, self.standard)
        self.assertEqual(caught.exception.code, "TRANSCRIPT_POINT_NOT_UNIQUE")
        self.assertEqual(g.cell_state(self.harness, self.CELL), g.UNRESOLVED)

    def test_the_vendored_gate_is_what_refuses_a_transcript_missing_its_exchange(self):
        empty = g.Transcript(case="", answer="an answer", decisive_point="an answer")
        with self.assertRaises(g.GraphError) as caught:
            g.register_transcript(self.harness, empty)
        self.assertEqual(caught.exception.code, "TRANSCRIPT_MALFORMED")
        bare = self.harness.blobs.put(b'{"case": "c", "answer": "a"}')
        self.assertFalse(conforming_transcript(self.harness.blobs, bare))

    def test_provenance_is_critic_and_the_literal_role_names_ride_in_content_and_the_call(self):
        call = LLMCall(role="judge", model="m-1", endpoint="e-1",
                       prompt_ref="c" * 64, raw_ref="d" * 64)
        result = g.ReadingResult(
            key=g.CellKey(self.CELL), relation="qualifies", seat="judge-1",
            transcript=transcript(), material_id=self.material, llm=call,
            roles={"critic": "seat-c", "defender": "seat-d", "judge": "judge-1"})
        ids = g.register_reading(self.harness, result, self.standard)
        artifact = self.harness.state.artifacts[ids.reading]
        self.assertEqual(artifact.provenance.role.value, "critic")
        body = json.loads(self.harness.blobs.get(artifact.content_ref))
        self.assertEqual(body["roles"]["judge"], "judge-1")
        events = [e for e in self.harness.log.read() if ids.reading in e.outputs]
        self.assertEqual([e.llm.role for e in events], ["judge"])

    def test_the_validity_node_is_split_and_bearing_is_load_bearing(self):
        ids = self.reading()
        soundness = self.harness.state.artifacts[ids.soundness]
        roles = {(r.target, r.role.value) for r in soundness.interface.refs}
        self.assertIn((self.standard, "mention"), roles)
        self.assertIn((ids.bearing, "evidence"), roles)
        # Deviation 1: the material is a dependence of the reading, never evidence of the
        # validity node, so refuting it orphans rather than refutes.
        self.assertNotIn((self.material, "evidence"), roles)

    def test_a_reading_mints_no_att_or_dep_edge_on_a_node_under_study(self):
        ids = self.reading()
        self.mark()
        studied = {self.material, self.standard}
        for attacker, target in self.harness.state.att:
            self.assertNotIn(target, studied, f"{attacker} attacked a studied node")
            self.assertNotEqual(target, ids.reading)
        reading = self.harness.state.artifacts[ids.reading]
        self.assertEqual(
            [r.target for r in reading.interface.refs if r.role.value == "dependence"],
            [self.material])
        for dependent, dependency in self.harness.state.dep:
            self.assertFalse(
                dependent in studied and dependency in studied,
                f"a dep edge was minted between two studied nodes: {dependent}")

    def test_a_reading_may_not_enter_the_unresolved_token(self):
        result = g.ReadingResult(key=g.CellKey(self.CELL), relation="unresolved",
                                 seat="judge-1", transcript=transcript())
        with self.assertRaises(g.GraphError) as caught:
            g.register_reading(self.harness, result, self.standard)
        self.assertEqual(caught.exception.code, "READING_TOKEN_UNRESOLVED")

    def test_a_token_outside_the_closed_vocabulary_is_refused(self):
        result = g.ReadingResult(key=g.CellKey(self.CELL), relation="improves",
                                 seat="judge-1", transcript=transcript())
        with self.assertRaises(g.GraphError) as caught:
            g.register_reading(self.harness, result, self.standard)
        self.assertEqual(caught.exception.code, "READING_TOKEN_UNKNOWN")
        self.assertNotIn("improves", READING_VOCABULARY)

    def test_a_reading_citing_an_unregistered_standard_is_refused(self):
        result = g.ReadingResult(key=g.CellKey(self.CELL), relation="retains",
                                 seat="judge-1", transcript=transcript())
        with self.assertRaises(g.GraphError) as caught:
            g.register_reading(self.harness, result, "f" * 64)
        self.assertEqual(caught.exception.code, "STANDARD_NOT_REGISTERED")


# --------------------------------------------------------------------------- (3)

class TheClosuresReinstateTheDefault(GraphTestCase):
    """§3's four computed consequences: refute the standard, hit the seat, rule on appeal,
    or invalidate the material — each lands in the calculus, none in a status rule."""

    def test_refuting_the_rubric_standard_reinstates_the_default_with_no_delete(self):
        ids = self.reading()
        self.assertEqual(g.cell_state(self.harness, self.CELL), g.READ)
        before_ids = set(self.harness.state.artifacts)
        before_log = self.root.joinpath("log.jsonl").read_bytes()

        attacker, _ = attack(self.harness, self.standard, "the-rubric-misreads-the-vocabulary")

        self.assertEqual(self.status(self.standard), Status.REFUTED)
        self.assertEqual(self.status(ids.soundness), Status.REFUTED)   # case law
        self.assertEqual(self.status(ids.reading), Status.REFUTED)     # validity closure
        self.assertEqual(self.status(ids.target), Status.ACCEPTED)     # reinstated
        self.assertEqual(self.status(attacker), Status.ACCEPTED)
        self.assertEqual(g.cell_state(self.harness, self.CELL), g.UNRESOLVED)

        after_log = self.root.joinpath("log.jsonl").read_bytes()
        self.assertTrue(after_log.startswith(before_log), "a published event was rewritten")
        self.assertTrue(before_ids <= set(self.harness.state.artifacts), "an id vanished")

    def test_one_standard_refutation_reinstates_every_cell_in_one_pass(self):
        first = self.reading()
        second = self.mark()
        attack(self.harness, self.standard, "the-rubric-is-unsound")
        self.assertEqual(g.cell_state(self.harness, self.CELL), g.UNRESOLVED)
        self.assertEqual(g.cell_state(self.harness, self.REGISTER_CELL), g.UNRESOLVED)
        self.assertEqual(self.status(first.reading), Status.REFUTED)
        self.assertEqual(self.status(second.reading), Status.REFUTED)

    def test_an_audit_hit_against_the_seat_reinstates_every_reading_of_that_seat(self):
        hit = self.reading(seat="judge-1")
        clean = self.reading(relation="retains", seat="judge-2",
                             point="the two terms are the same term")
        other_cell = g.open_cells(self.harness, ["r1/c2"], material_id=self.material)

        finding = g.AuditFinding(seat="judge-1", kind="paraphrase-invariance",
                                 detail="a fresh paraphrase flipped the ruling")
        audit = g.register_audit_warrant(self.harness, finding)

        self.assertEqual(self.status(hit.soundness), Status.REFUTED)
        self.assertEqual(self.status(hit.reading), Status.REFUTED)
        self.assertEqual(self.status(clean.soundness), Status.ACCEPTED)
        self.assertEqual(self.status(audit), Status.ACCEPTED)
        self.assertIn(hit.soundness, g.validity_nodes_for_seat(self.harness, "judge-1"))
        self.assertNotIn(clean.soundness, g.validity_nodes_for_seat(self.harness, "judge-1"))
        self.assertEqual(other_cell["r1/c2"], g.cell_standing(self.harness, "r1/c2").default_id)

    def test_an_audit_warrant_is_program_typed_and_is_itself_attackable(self):
        ids = self.reading()
        audit = g.register_audit_warrant(
            self.harness, g.AuditFinding(seat="judge-1", kind="premise-deletion"))
        warrants = [self.harness.warrants[w]
                    for w in self.harness.carried_warrant_ids(audit)]
        self.assertEqual({w.type for w in warrants}, {WarrantType.DEMONSTRATIVE})
        self.assertTrue(all(
            self.harness.commitments[w.commitment].eval.startswith("program:")
            for w in warrants))
        self.assertEqual(self.status(ids.target), Status.ACCEPTED)

        attack(self.harness, warrants[0].validity_node, "the-audit-check-is-unsound")
        self.assertEqual(self.status(audit), Status.REFUTED)
        self.assertEqual(self.status(ids.reading), Status.ACCEPTED)
        self.assertEqual(g.cell_state(self.harness, self.CELL), g.READ)

    def test_an_audit_kind_outside_the_three_that_mint_warrants_is_refused(self):
        with self.assertRaises(g.GraphError) as caught:
            g.register_audit_warrant(
                self.harness, g.AuditFinding(seat="judge-1", kind="ensemble-disagreement"))
        self.assertEqual(caught.exception.code, "AUDIT_KIND_UNKNOWN")
        self.assertNotIn("ensemble-disagreement", g.AUDIT_KINDS)

    def test_an_appellate_ruling_against_bearing_flips_the_label_through_pass_one(self):
        ids = self.reading()
        before_log = self.root.joinpath("log.jsonl").read_bytes()
        ruling = g.AppellateRuling(
            ruling_id="APP-001", target=ids.bearing, standard_id=self.standard,
            ground="the relation as read does not bear on the claim it was offered for")
        precedent = g.apply_appeal(self.harness, ruling)

        self.assertEqual(self.status(ids.bearing), Status.REFUTED)
        self.assertEqual(self.status(ids.soundness), Status.REFUTED)  # evidence closure
        self.assertEqual(self.status(ids.reading), Status.REFUTED)
        self.assertEqual(g.cell_state(self.harness, self.CELL), g.UNRESOLVED)
        self.assertEqual(g.appellate_rulings(self.harness), (precedent,))
        self.assertTrue(
            self.root.joinpath("log.jsonl").read_bytes().startswith(before_log))

    def test_an_appellate_warrant_carries_no_commitment_and_demands_no_transcript(self):
        ids = self.reading()
        precedent = g.apply_appeal(self.harness, g.AppellateRuling(
            ruling_id="APP-002", target=ids.soundness,
            ground="the guard as run was not sound on these bytes"))
        warrant = self.harness.warrants[
            self.harness.carried_warrant_ids(precedent)[0]]
        self.assertEqual(warrant.type, WarrantType.ARGUMENTATIVE)
        self.assertIsNone(warrant.commitment)
        self.assertIsNone(warrant.trace_ref)
        self.assertEqual(
            self.harness.state.artifacts[precedent].provenance.role.value, "user")

    def test_an_appeal_naming_an_unregistered_node_is_refused(self):
        with self.assertRaises(g.GraphError) as caught:
            g.apply_appeal(self.harness, g.AppellateRuling(
                ruling_id="APP-003", target="e" * 64, ground="a ground"))
        self.assertEqual(caught.exception.code, "APPEAL_TARGET_UNKNOWN")

    def test_an_unsettled_attack_leaves_the_cell_suspended_and_not_read(self):
        """The fifth state: an attack pass 1 cannot settle.  The reading does not stand,
        and neither does the default — which is precisely not the same as unresolved."""
        ids = self.reading()
        h = self.harness
        nu_one = h.create_artifact("nu: counter one is sound",
                                   provenance=Provenance(role="user"))
        nu_two = h.create_artifact("nu: counter two is sound",
                                   provenance=Provenance(role="user"))
        first = Warrant(id="w-mutual-1", target="B-critic",
                        type=WarrantType.ARGUMENTATIVE, validity_node=nu_one.id)
        h.register_artifact(
            Artifact(id="A-critic", content_ref="inline:critic A",
                     warrants=["w-mutual-1"], provenance=Provenance(role="critic")),
            warrants=[first])
        second = Warrant(id="w-mutual-2", target="A-critic",
                         type=WarrantType.ARGUMENTATIVE, validity_node=nu_two.id)
        h.register_artifact(
            Artifact(id="B-critic", content_ref="inline:critic B",
                     warrants=["w-mutual-2"], provenance=Provenance(role="critic")),
            warrants=[second])
        third = Warrant(id="w-mutual-3", target=ids.soundness,
                        type=WarrantType.ARGUMENTATIVE, validity_node=nu_one.id)
        h.register_artifact(
            Artifact(id="A-critic", content_ref="inline:critic A",
                     warrants=["w-mutual-1", "w-mutual-3"],
                     provenance=Provenance(role="critic")),
            warrants=[first, third])

        self.assertEqual(self.status("A-critic"), Status.SUSPENDED)
        self.assertEqual(self.status(ids.soundness), Status.SUSPENDED)
        self.assertEqual(self.status(ids.reading), Status.SUSPENDED)
        self.assertEqual(self.status(ids.target), Status.SUSPENDED)
        self.assertEqual(g.cell_state(self.harness, self.CELL), g.SUSPENDED)

    def test_refuting_the_material_suspends_the_reading_unsupported_not_refuted(self):
        ids = self.reading()
        attack(self.harness, self.material, "the-row-was-imported-at-the-wrong-grain")
        self.assertEqual(self.status(self.material), Status.REFUTED)
        self.assertEqual(self.status(ids.reading), Status.SUSPENDED_UNSUPPORTED)
        self.assertNotEqual(self.status(ids.reading), Status.REFUTED)
        self.assertEqual(g.cell_state(self.harness, self.CELL), g.UNSUPPORTED)


# --------------------------------------------------------------------------- (4)

class TwoSurvivingRivalsAreAProblemNotAnAverage(GraphTestCase):
    """§3: two rival readings of one cell both attack the default and both survive, which
    Spawns a discrimination problem.  Disagreement becomes a problem, never an average."""

    def test_two_surviving_readings_leave_the_cell_contested(self):
        first = self.reading("re-deploys")
        second = self.reading("qualifies", seat="judge-2",
                              point="the two terms are the same term")
        standing = g.cell_standing(self.harness, self.CELL)
        self.assertEqual(standing.state, g.CONTESTED)
        self.assertIsNone(standing.relation)
        self.assertEqual(set(standing.accepted), {first.reading, second.reading})
        self.assertEqual(self.status(first.reading), Status.ACCEPTED)
        self.assertEqual(self.status(second.reading), Status.ACCEPTED)

    def test_a_contested_cell_names_both_rivals_and_combines_neither(self):
        self.reading("re-deploys")
        self.reading("repairs", seat="judge-2", point="the two terms are the same term")
        standing = g.cell_standing(self.harness, self.CELL)
        relations = {
            json.loads(self.harness.blobs.get(
                self.harness.state.artifacts[a].content_ref))["relation"]
            for a in standing.accepted}
        self.assertEqual(relations, {"re-deploys", "repairs"})
        self.assertIsNone(standing.relation)

    def test_discriminating_one_rival_leaves_the_other_standing_alone(self):
        first = self.reading("re-deploys")
        second = self.reading("qualifies", seat="judge-2",
                              point="the two terms are the same term")
        attack(self.harness, second.soundness, "the-second-guard-was-not-cross-family")
        standing = g.cell_standing(self.harness, self.CELL)
        self.assertEqual(standing.state, g.READ)
        self.assertEqual(standing.accepted, (first.reading,))
        self.assertEqual(standing.relation, "re-deploys")


# --------------------------------------------------------------------------- (5)

class MarksEnterPerRegisterAndAreNeverCombined(GraphTestCase):
    """§3: "marks enter the same way per register, never combined"."""

    def test_no_mark_is_combined_across_registers(self):
        keys = [g.CellKey("r1/c1", register, "original-vs-control")
                for register in REGISTER_IDS]
        g.open_cells(self.harness, keys, material_id=self.material)
        for register in REGISTER_IDS:
            kind = DIFFERENCE_KINDS[register][0]
            self.mark(key=g.CellKey("r1/c1", register, "original-vs-control"), kind=kind)
        triples = g.mark_triples(self.harness)
        self.assertEqual({register for _, register, _ in triples}, set(REGISTER_IDS))
        for cell, register, token in triples:
            self.assertIn(register, REGISTER_IDS)
            self.assertIn(token, MARKS)
            self.assertNotIn("|", register)

    def test_a_cell_key_cannot_name_two_registers(self):
        with self.assertRaises(g.GraphError) as caught:
            g.CellKey("r1/c1", "T|E", "original-vs-control")
        self.assertEqual(caught.exception.code, "CELL_KEY_INVALID")
        with self.assertRaises(g.GraphError):
            g.CellKey("r1/c1", "TE", "original-vs-control")

    def test_a_mark_on_a_cell_that_names_no_register_is_refused(self):
        result = g.ReadingResult(key=g.CellKey(self.CELL), relation="differs",
                                 seat="judge-1", transcript=transcript())
        with self.assertRaises(g.GraphError) as caught:
            g.register_mark(self.harness, result, self.standard)
        self.assertEqual(caught.exception.code, "READING_TOKEN_UNKNOWN")

        retains = g.ReadingResult(key=g.CellKey(self.CELL), relation="retains",
                                  seat="judge-1", transcript=transcript())
        with self.assertRaises(g.GraphError) as second:
            g.register_mark(self.harness, retains, self.standard)
        self.assertEqual(second.exception.code, "MARK_REGISTER_MISSING")

    def test_a_relation_reading_may_not_occupy_a_per_register_cell(self):
        result = g.ReadingResult(key=self.REGISTER_CELL, relation="same",
                                 seat="judge-1", transcript=transcript())
        with self.assertRaises(g.GraphError) as caught:
            g.register_reading(self.harness, result, self.standard)
        self.assertEqual(caught.exception.code, "MARK_REGISTER_UNEXPECTED")

    def test_a_difference_kind_outside_its_registers_closed_set_is_refused(self):
        with self.assertRaises(g.GraphError) as caught:
            self.mark(kind="record_engaged")           # an E token offered for T
        self.assertEqual(caught.exception.code, "DIFFERENCE_KIND_UNKNOWN")
        self.assertNotIn("record_engaged", DIFFERENCE_KINDS["T"])

    def test_a_relation_reading_carries_no_difference_kind(self):
        with self.assertRaises(g.GraphError) as caught:
            self.reading(difference_kind="target_set_membership")
        self.assertEqual(caught.exception.code, "DIFFERENCE_KIND_UNEXPECTED")

    def test_an_unmarked_register_cell_contributes_its_unresolved_standing(self):
        self.assertEqual(
            g.mark_triples(self.harness),
            frozenset({("r1/c1", "T", "unresolved")}))
        self.mark()
        self.assertEqual(
            g.mark_triples(self.harness),
            frozenset({("r1/c1", "T", "differs")}))

    def test_a_contested_register_cell_contributes_no_triple_at_all(self):
        self.mark("differs")
        self.mark("same", kind=None, seat="judge-2")
        self.assertEqual(g.cell_state(self.harness, self.REGISTER_CELL), g.CONTESTED)
        self.assertEqual(g.mark_triples(self.harness), frozenset())

    def test_the_mark_trial_runs_pairwise_and_the_relation_trial_absolute(self):
        self.assertEqual(g.CellKey(self.CELL).mode, "absolute")
        self.assertEqual(self.REGISTER_CELL.mode, "pairwise")
        ids = self.mark()
        body = json.loads(self.harness.blobs.get(
            self.harness.state.artifacts[ids.reading].content_ref))
        self.assertEqual(body["mode"], "pairwise")


# --------------------------------------------------------------------------- (6)

class NothingHereCountsScoresOrRanksAReading(GraphTestCase):
    """G12, and the wave plan's "no function exposes a count, score or rank of readings"."""

    COUNTING = frozenset({
        "count", "counts", "counted", "tally", "total", "totals", "sum", "average",
        "mean", "median", "percent", "percentage", "frequency", "n", "num", "number",
        "most", "least", "top", "highest", "lowest", "majority",
    })

    def public_names(self) -> set[str]:
        names: set[str] = set(g.__all__)
        for name in list(g.__all__):
            value = getattr(g, name)
            names.update(getattr(value, "__dataclass_fields__", {}))
            if callable(value) and hasattr(value, "__code__"):
                names.update(value.__code__.co_varnames[:value.__code__.co_argcount])
        return names

    def test_no_public_name_is_a_count_a_score_or_a_rank(self):
        banned = self.COUNTING | set(FORBIDDEN_KEYS)
        for name in sorted(self.public_names()):
            for token in re.split(r"[_\W]+", name.lower()):
                with self.subTest(name=name, token=token):
                    self.assertNotIn(token, banned, f"{name} names a quantity")

    def test_no_public_callable_returns_a_number_and_nothing_returns_a_length(self):
        tree = ast.parse(module_source())
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                annotation = ast.unparse(node.returns) if node.returns else ""
                with self.subTest(function=node.name):
                    self.assertNotIn(annotation, ("int", "float", "int | None"))
            if isinstance(node, ast.Return) and isinstance(node.value, ast.Call):
                func = node.value.func
                with self.subTest(line=node.lineno):
                    self.assertNotEqual(getattr(func, "id", ""), "len")

    def test_every_body_this_module_authors_passes_the_scoring_key_guard(self):
        self.reading()
        self.mark()
        g.register_audit_warrant(
            self.harness, g.AuditFinding(seat="judge-2", kind="planted-flaw-calibration"))
        g.apply_appeal(self.harness, g.AppellateRuling(
            ruling_id="APP-004", target=self.standard, standard_id=self.standard,
            ground="the rubric's absolute mode is the wrong mode for this question"))
        seen: set[str] = set()
        for artifact in self.harness.state.artifacts.values():
            body = g._decode(self.harness, artifact)
            if body is None or body.get("schema") not in g.PRODUCED_SCHEMAS:
                continue
            seen.add(body["schema"])
            from minireason.loop.contracts import assert_no_scoring_keys
            assert_no_scoring_keys(body)          # G12, over artifact content
        self.assertEqual(seen, set(g.PRODUCED_SCHEMAS))

    def test_a_reading_body_carrying_a_scoring_key_is_refused_not_stripped(self):
        with self.assertRaises(ScoringKeyForbidden):
            self.reading(body={"guard": {"paraphrase": {"score": 0.9}}})
        self.assertEqual(g.cell_state(self.harness, self.CELL), g.UNRESOLVED)

    def test_the_vendored_verdict_field_is_the_named_exemption_and_nothing_wider(self):
        # O2: `verdict` is a FORBIDDEN_KEYS member AND the vendored warrant's own field
        # name AND the transcript's ruling field.  Both stay; the boundary is named.
        ids = self.reading()
        self.assertIn("verdict", FORBIDDEN_KEYS)
        self.assertEqual(self.harness.warrants[ids.warrant].verdict, "fail")
        stored = json.loads(self.harness.blobs.get(ids.transcript))
        self.assertEqual(stored["ruling"]["verdict"], "fail")
        from minireason.loop.contracts import assert_no_scoring_keys
        with self.assertRaises(ScoringKeyForbidden):
            assert_no_scoring_keys(stored)        # which is why it is exempt, by name
        self.assertEqual(
            set(g.G12_EXEMPT),
            {"deepreason_core.ontology.Warrant.verdict",
             "deepreason_core.harness.transcript_blob:ruling.verdict"})

    def test_the_cell_states_are_five_tokens_and_none_of_them_is_a_quantity(self):
        self.assertEqual(len(set(g.CELL_STATES)), 5)
        for state in g.CELL_STATES:
            self.assertNotIn(state, FORBIDDEN_KEYS)
        self.assertTrue(
            {s.state for s in g.cell_standings(self.harness)} <= set(g.CELL_STATES))


# --------------------------------------------------------------------------- (7)

class TheGraphIsAppendOnlyAndReplaysByteIdentically(GraphTestCase):
    """The deterministic clock is what turns "replay is deterministic" into a byte
    assertion; ``produced`` is what W1-OBLIGATIONS intersects for ProducedBy."""

    def build(self, root: Path) -> Harness:
        harness = g.open_graph(root, clock=g.fixed_clock())
        standard = g.register_standard(harness, STANDARD_BODY)
        material = g.register_material(harness, b'{"row_key": "r1", "cells": {}}')
        g.open_cells(harness, [self.CELL, self.REGISTER_CELL], material_id=material)
        g.register_reading(harness, g.ReadingResult(
            key=g.CellKey(self.CELL), relation="re-deploys", seat="judge-1",
            transcript=transcript(), material_id=material), standard)
        return harness

    def test_two_builds_on_a_fixed_clock_are_byte_identical(self):
        first, second = self.tmp / "a", self.tmp / "b"
        self.build(first)
        self.build(second)
        self.assertEqual((first / "log.jsonl").read_bytes(),
                         (second / "log.jsonl").read_bytes())

    def test_reopening_the_log_reproduces_every_label(self):
        ids = self.reading()
        attack(self.harness, self.standard, "the-rubric-is-unsound")
        live = self.harness.state.model_dump_json()
        reopened = g.open_graph(self.root)
        self.assertEqual(reopened.state.model_dump_json(), live)
        self.assertEqual(g.cell_state(reopened, self.CELL), g.UNRESOLVED)
        self.assertEqual(reopened.state.status[ids.reading], Status.REFUTED)

    def test_produced_names_this_cycles_artifacts_and_not_the_previous_cycles(self):
        first = g.produced(self.harness)
        self.assertIn(self.material, first.artifact_ids)
        ids = self.reading()
        second = g.produced(self.harness, since_seq=first.upto_seq)
        self.assertEqual(second.artifact_ids, frozenset(ids.artifact_ids))
        self.assertNotIn(self.material, second.artifact_ids)
        self.assertGreater(second.upto_seq, first.upto_seq)

    def test_a_time_travel_view_refuses_a_registration(self):
        self.reading()
        past = g.open_graph(self.root, upto_seq=1)
        with self.assertRaises(g.GraphError) as caught:
            g.register_material(past, b'{"row_key": "r2"}')
        self.assertEqual(caught.exception.code, "GRAPH_READ_ONLY")

    def test_every_refusal_is_a_loop_error_with_a_declared_code(self):
        self.assertTrue(issubclass(g.GraphError, LoopError))
        with self.assertRaises(LoopError) as caught:
            g.cell_state(self.harness, "r9/c9")
        self.assertIn(caught.exception.code, g.NEW_CODES)
        for code, reason in g.NEW_CODES.items():
            with self.subTest(code=code):
                self.assertRegex(code, r"\A[A-Z][A-Z0-9_]*\Z")
                self.assertTrue(reason.strip())

    def test_the_declared_graph_root_is_resolved_against_the_repository_root(self):
        resolved = g.resolve_graph_root(self.tmp, "experiments/loops/run-1/graph")
        self.assertEqual(resolved, self.tmp / "experiments/loops/run-1/graph")
        for bad in ("/abs/graph", "../escape", ""):
            with self.subTest(graph_root=bad), self.assertRaises(g.GraphError) as caught:
                g.resolve_graph_root(self.tmp, bad)
            self.assertEqual(caught.exception.code, "GRAPH_ROOT_INVALID")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
