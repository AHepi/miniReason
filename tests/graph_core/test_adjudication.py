"""P0 acceptance tests (spec §16) — deterministic core.

Grounded extension correctness, reinstatement (Lemma 3.1), validity-node
closure, two-pass support cascade, dep cycle rejection, and the case-law
closure: standard refutation => dependent-verdict collapse => target
reinstatement, all in pass 1.

Vendored from AHepi/DeepReason@9607fba tests/test_adjudication.py; see
VENDOR_NOTES.md.
"""

from __future__ import annotations

from deepreason_core.harness import Harness, WellFormednessError, transcript_blob
from deepreason_core.ontology import (
    Artifact,
    Commitment,
    Interface,
    Provenance,
    Ref,
    Status,
    Warrant,
    WarrantType,
)

from .helpers import HarnessTestCase, TempDirTestCase, art, attack


class AdjudicationTests(HarnessTestCase):
    def test_grounded_extension_unattacked_accepted(self) -> None:
        a = art(self.harness, "claim A")
        self.assertEqual(self.harness.state.status[a.id], Status.ACCEPTED)

    def test_attack_refutes(self) -> None:
        target = art(self.harness, "target claim")
        critic, nu = attack(self.harness, target.id, "c1")
        status = self.harness.state.status
        self.assertEqual(status[target.id], Status.REFUTED)
        self.assertEqual(status[critic.id], Status.ACCEPTED)
        self.assertEqual(status[nu.id], Status.ACCEPTED)

    def test_reinstatement_lemma_3_1(self) -> None:
        """k attacks a, j attacks k, j unattacked => {j, a} accepted."""
        a = art(self.harness, "target claim")
        k, _ = attack(self.harness, a.id, "k")
        self.assertEqual(self.harness.state.status[a.id], Status.REFUTED)
        j, _ = attack(self.harness, k.id, "j")
        status = self.harness.state.status
        self.assertEqual(status[j.id], Status.ACCEPTED)
        self.assertEqual(status[k.id], Status.REFUTED)
        # reinstated, derived not ruled
        self.assertEqual(status[a.id], Status.ACCEPTED)

    def test_validity_node_closure(self) -> None:
        """Attacking a warrant's nu attacks the warrant (via its carrier)."""
        target = art(self.harness, "target claim")
        critic, nu = attack(self.harness, target.id, "c1")
        self.assertEqual(self.harness.state.status[target.id], Status.REFUTED)
        attack(self.harness, nu.id, "nu-is-unsound")
        status = self.harness.state.status
        self.assertEqual(status[nu.id], Status.REFUTED)
        # closure lifted the attack
        self.assertEqual(status[critic.id], Status.REFUTED)
        # reinstated
        self.assertEqual(status[target.id], Status.ACCEPTED)

    def test_validity_attack_disables_every_carrier_of_a_warrant(self) -> None:
        """Carriage is many-to-many: one warrant may be packaged more than once."""
        target = art(self.harness, "target claim")
        nu = art(self.harness, "nu: the shared warrant is valid")
        warrant = Warrant(
            id="w-shared",
            target=target.id,
            type=WarrantType.ARGUMENTATIVE,
            validity_node=nu.id,
        )
        first = self.harness.create_artifact(
            "first packaging of the attack",
            provenance=Provenance(role="critic"),
            warrants=[warrant],
        )
        second = self.harness.create_artifact(
            "second packaging of the attack",
            provenance=Provenance(role="critic"),
            warrants=[warrant],
        )
        self.assertEqual(self.harness.state.status[target.id], Status.REFUTED)

        attack(self.harness, nu.id, "shared-warrant-is-unsound")

        self.assertEqual(self.harness.state.status[first.id], Status.REFUTED)
        self.assertEqual(self.harness.state.status[second.id], Status.REFUTED)
        self.assertEqual(self.harness.state.status[target.id], Status.ACCEPTED)

    def test_support_cascade_orphaned_not_false(self) -> None:
        premise = art(self.harness, "premise")
        dependent = art(
            self.harness,
            "dependent claim",
            interface=Interface(refs=[Ref(target=premise.id, role="dependence")]),
        )
        self.assertEqual(self.harness.state.status[dependent.id], Status.ACCEPTED)
        attack(self.harness, premise.id, "kills-premise")
        status = self.harness.state.status
        self.assertEqual(status[premise.id], Status.REFUTED)
        # NOT refuted
        self.assertEqual(status[dependent.id], Status.SUSPENDED_UNSUPPORTED)

    def test_mutual_attack_suspended(self) -> None:
        """An unresolved attack cycle leaves both suspended (grounded semantics)."""
        nu1 = art(self.harness, "nu 1")
        nu2 = art(self.harness, "nu 2")
        w1 = Warrant(
            id="w1", target="B", type=WarrantType.ARGUMENTATIVE, validity_node=nu1.id
        )
        a = Artifact(
            id="A", content_ref="inline:critic A", warrants=["w1"],
            provenance=Provenance(role="critic"),
        )
        # target "B" dangles until B registers
        self.harness.register_artifact(a, warrants=[w1])
        w2 = Warrant(
            id="w2", target="A", type=WarrantType.ARGUMENTATIVE, validity_node=nu2.id
        )
        b = Artifact(
            id="B", content_ref="inline:critic B", warrants=["w2"],
            provenance=Provenance(role="critic"),
        )
        self.harness.register_artifact(b, warrants=[w2])
        self.assertEqual(self.harness.state.status["A"], Status.SUSPENDED)
        self.assertEqual(self.harness.state.status["B"], Status.SUSPENDED)

    def test_dep_cycle_rejected(self) -> None:
        a = Artifact(
            id="A",
            content_ref="inline:a",
            interface=Interface(refs=[Ref(target="B", role="dependence")]),
            provenance=Provenance(role="import"),
        )
        self.harness.register_artifact(a)  # dangling dependence: no edge yet
        b = Artifact(
            id="B",
            content_ref="inline:b",
            interface=Interface(refs=[Ref(target="A", role="dependence")]),
            provenance=Provenance(role="import"),
        )
        with self.assertRaises(WellFormednessError):
            # materializing B would close the cycle
            self.harness.register_artifact(b)

    def test_standard_refutation_collapses_verdicts_and_reinstates(self) -> None:
        """Case-law closure (§1): refute a standard => every nu citing it is
        attacked => warrants fall => targets reinstate (parallel fifths)."""
        self.harness.register_commitment(
            Commitment(id="kappa-taste", eval="rubric:std-1")
        )
        standard = art(self.harness, "standard std-1: no parallel fifths")
        target = art(
            self.harness,
            "informal work",
            interface=Interface(commitments=["kappa-taste"]),
        )
        nu = art(
            self.harness,
            "nu: judged under std-1",
            interface=Interface(refs=[Ref(target=standard.id, role="mention")]),
        )
        verdict_warrant = Warrant(
            id="w-verdict",
            target=target.id,
            type=WarrantType.DEMONSTRATIVE,
            commitment="kappa-taste",
            verdict="fail",
            trace_ref=transcript_blob(
                self.harness,
                case="the work violates clause 1 of std-1",
                answer="the defence disputes the clause's scope",
                decisive_point="violates clause 1",
            ),
            validity_node=nu.id,
        )
        critic = self.harness.create_artifact(
            "critic: fails std-1",
            provenance=Provenance(role="critic"),
            warrants=[verdict_warrant],
        )
        self.assertEqual(self.harness.state.status[target.id], Status.REFUTED)

        # The productive attack lands on the standard, not the work (§10.3).
        attacker, _ = attack(self.harness, standard.id, "std-1-is-wrong")
        status = self.harness.state.status
        self.assertEqual(status[standard.id], Status.REFUTED)
        # case-law extension
        self.assertEqual(status[nu.id], Status.REFUTED)
        # validity-node closure
        self.assertEqual(status[critic.id], Status.REFUTED)
        # reinstated, computed not curated
        self.assertEqual(status[target.id], Status.ACCEPTED)
        self.assertEqual(status[attacker.id], Status.ACCEPTED)

    def test_unregistered_warrant_rejected(self) -> None:
        a = Artifact(
            id="X", content_ref="inline:x", warrants=["ghost"],
            provenance=Provenance(role="critic"),
        )
        with self.assertRaises(WellFormednessError):
            self.harness.register_artifact(a)


class ReplayByteIdentityTests(TempDirTestCase):
    def test_R_g_informal_only_run_replays_byte_identical(self) -> None:
        """D2 rev 2 Item 6 acceptance check 1: an informal-only run (no
        candidate ever populates the new commitment field, no relatedness
        claim minted) is BYTE-IDENTICAL to today at the event-log level --
        reader-before-writer, absence-tolerant (R30: no new absence-tolerant
        Event field was even added this tranche, unlike rung-4's own M19
        precedent, since the new commitment attaches via the EXISTING
        two-phase draft/register path)."""
        root = self.tmp_path / "run"
        harness = Harness(root)
        a = art(harness, "plain prose, no formal commitment of any kind")
        attacker, _ = attack(harness, a.id, "an ordinary argumentative attack")

        self.assertEqual(harness.state.status[a.id], Status.REFUTED)
        self.assertEqual(harness.state.status[attacker.id], Status.ACCEPTED)
        self.assertEqual(
            Harness(root).state.model_dump_json(), harness.state.model_dump_json()
        )
