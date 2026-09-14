"""Ontology sanity: the one schema round-trips (spec §1).

Vendored from AHepi/DeepReason@9607fba tests/test_ontology.py; see
VENDOR_NOTES.md.
"""

from __future__ import annotations

import unittest

from deepreason_core.ontology import (
    Artifact,
    Commitment,
    Event,
    Interface,
    Problem,
    ProblemProvenance,
    Provenance,
    Ref,
    Rule,
    SpawnTrigger,
    Warrant,
    WarrantType,
)


class OntologyTests(unittest.TestCase):
    def test_artifact_round_trip(self) -> None:
        a = Artifact(
            id="deadbeef",
            content_ref="inline:hello",
            codec="utf8",
            interface=Interface(
                commitments=["c1"], refs=[Ref(target="x", role="dependence")]
            ),
            provenance=Provenance(role="seed"),
        )
        self.assertEqual(Artifact.model_validate_json(a.model_dump_json()), a)

    def test_compute_id_deterministic_and_content_sensitive(self) -> None:
        interface = Interface(commitments=["c1"])
        id1 = Artifact.compute_id("inline:x", "utf8", interface)
        self.assertEqual(
            id1, Artifact.compute_id("inline:x", "utf8", Interface(commitments=["c1"]))
        )
        self.assertNotEqual(id1, Artifact.compute_id("inline:y", "utf8", interface))
        self.assertNotEqual(id1, Artifact.compute_id("inline:x", "json", interface))
        self.assertEqual(len(id1), 64)  # sha256 hex

    def test_artifact_has_no_kind_field(self) -> None:
        # Untypedness (Def 3.2, §0): dispatch is on interface structure only.
        self.assertNotIn("kind", Artifact.model_fields)

    def test_warrant_round_trip(self) -> None:
        w = Warrant(
            id="w1", target="a1", type=WarrantType.ARGUMENTATIVE, validity_node="v1"
        )
        self.assertEqual(Warrant.model_validate_json(w.model_dump_json()), w)

    def test_problem_provenance_alias(self) -> None:
        p = Problem(
            id="p1",
            description="seed problem",
            provenance=ProblemProvenance.model_validate(
                {"trigger": SpawnTrigger.SEED, "from": []}
            ),
        )
        self.assertIs(p.provenance.trigger, SpawnTrigger.SEED)

    def test_event_round_trip(self) -> None:
        e = Event(seq=0, ts="2026-01-01T00:00:00Z", rule=Rule.REGISTER)
        self.assertEqual(Event.model_validate_json(e.model_dump_json()), e)

    def test_commitment_defaults(self) -> None:
        c = Commitment(id="c1", eval="predicate:true")
        self.assertIs(c.observation_valued, False)
        self.assertEqual(c.budget.steps, 100_000)
