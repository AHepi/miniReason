"""Closures, guards and fences the vendored core claims but did not pin.

New (not converted from upstream). Each class answers one adversarial-review
finding against the first vendoring pass:

* the **evidence closure** (spec §1 lines 109-114) is kept in
  ``adjudication/edges.py`` and named in VENDOR_NOTES §5 as "kept intact and
  exercised by the suite" — but nothing exercised it;
* the **trial guard** (§2/§3) that makes a rubric-derived demonstrative
  warrant unregisterable without a conforming transcript had no negative test,
  so the inlined ``conforming_transcript`` could have been a no-op;
* ``Harness.at`` is documented as a physically read-only view, but no test
  asserted that merely OPENING one writes nothing, nor that a sealed holdout
  blob stays unreadable at a pre-reveal fence;
* explicit **warrant carriage** (``StateDiff.carry_add``) is what lets one
  warrant attack from a second carrier without changing a content-addressed
  id; the vendored suite covered it only through ``create_artifact``;
* ``state.conn`` is deliberately a zero map (VENDOR_NOTES §D), which is a
  claim about every artifact, not about the field's presence.
"""

from __future__ import annotations

from deepreason_core.canonical import canonical_json
from deepreason_core.harness import Harness, WellFormednessError, transcript_blob
from deepreason_core.ontology import (
    Artifact,
    Commitment,
    Interface,
    Provenance,
    Ref,
    Rule,
    Status,
    Warrant,
    WarrantType,
)
from deepreason_core.storage.blobs import FencedBlobStore

from .helpers import HarnessTestCase, TempDirTestCase, art, attack


class EvidenceClosureTests(HarnessTestCase):
    """Spec §1 (closure extension, evidence), lines 109-114.

    "`att` construction adds `(x → ν)` for every attacker `x` of the evidence
    or any artifact in its transitive dependence lineage. The ordinary closure
    rule then attacks every carrier of the warrant, so invalidating a source
    can reinstate the target without any status rule outside `att`/`dep`."
    """

    def _grounded_attack(self, evidence_id: str, target_id: str):
        """A warrant against ``target`` whose ν is grounded in ``evidence``."""
        nu = art(
            self.harness,
            "nu: the attack is sound, and it is grounded in the evidence",
            interface=Interface(refs=[Ref(target=evidence_id, role="evidence")]),
        )
        warrant = Warrant(
            id="w-grounded",
            target=target_id,
            type=WarrantType.ARGUMENTATIVE,
            validity_node=nu.id,
        )
        carrier = self.harness.create_artifact(
            "critic: the target fails, on the evidence",
            provenance=Provenance(role="critic"),
            warrants=[warrant],
        )
        return carrier, nu

    def test_attacking_the_evidence_collapses_the_warrant_and_reinstates(self) -> None:
        evidence = art(self.harness, "E: the recorded observation series")
        target = art(self.harness, "T: the claim under attack")
        carrier, nu = self._grounded_attack(evidence.id, target.id)

        status = self.harness.state.status
        self.assertEqual(status[target.id], Status.REFUTED)
        self.assertEqual(status[carrier.id], Status.ACCEPTED)
        self.assertEqual(status[nu.id], Status.ACCEPTED)
        self.assertIn((carrier.id, target.id), self.harness.state.att)

        # Attack the EVIDENCE, from an artifact nothing attacks.
        breaker, breaker_nu = attack(self.harness, evidence.id, "E-is-fabricated")
        status = self.harness.state.status
        self.assertEqual(status[breaker.id], Status.ACCEPTED)
        self.assertEqual(status[breaker_nu.id], Status.ACCEPTED)
        self.assertEqual(status[evidence.id], Status.REFUTED)
        self.assertEqual(status[nu.id], Status.REFUTED)       # evidence closure
        self.assertEqual(status[carrier.id], Status.REFUTED)  # validity-node closure
        self.assertEqual(status[target.id], Status.ACCEPTED)  # reinstated

        # Derived in att, never a hidden status check: both lifted edges are
        # in the materialized attack relation.
        self.assertIn((breaker.id, evidence.id), self.harness.state.att)
        self.assertIn((breaker.id, nu.id), self.harness.state.att)
        self.assertIn((breaker.id, carrier.id), self.harness.state.att)
        # ... and the derivation survives replay from the log.
        self.assertEqual(
            Harness(self.harness.root).state.model_dump_json(),
            self.harness.state.model_dump_json(),
        )

    def test_attacking_the_evidence_lineage_collapses_the_warrant(self) -> None:
        """Spec §1: an attacker of any artifact in the evidence's
        transitive dependence lineage attacks the validity node too."""
        source = art(self.harness, "S: the raw instrument log")
        evidence = art(
            self.harness,
            "E: the series derived from the instrument log",
            interface=Interface(refs=[Ref(target=source.id, role="dependence")]),
        )
        target = art(self.harness, "T: the claim under attack")
        carrier, nu = self._grounded_attack(evidence.id, target.id)
        self.assertEqual(self.harness.state.status[target.id], Status.REFUTED)

        # Attack the SOURCE the evidence depends on, not the evidence itself.
        breaker, _ = attack(self.harness, source.id, "instrument-was-miscalibrated")
        status = self.harness.state.status
        self.assertEqual(status[source.id], Status.REFUTED)
        # Pass 2: the evidence is orphaned, not false (§4).
        self.assertEqual(status[evidence.id], Status.SUSPENDED_UNSUPPORTED)
        self.assertIn((breaker.id, nu.id), self.harness.state.att)
        self.assertEqual(status[nu.id], Status.REFUTED)
        self.assertEqual(status[carrier.id], Status.REFUTED)
        self.assertEqual(status[target.id], Status.ACCEPTED)


class RubricTrialGuardTests(HarnessTestCase):
    """§2/§3: a rubric-derived demonstrative warrant registers ONLY with a
    conforming trial transcript. Both refusal branches of the guard."""

    def setUp(self) -> None:
        super().setUp()
        self.harness.register_commitment(
            Commitment(id="kappa-rubric", eval="rubric:std-2")
        )
        self.standard = art(self.harness, "standard std-2: no unresolved dissonance")
        self.target = art(
            self.harness,
            "the judged work",
            interface=Interface(commitments=["kappa-rubric"]),
        )
        self.nu = art(
            self.harness,
            "nu: judged under std-2",
            interface=Interface(refs=[Ref(target=self.standard.id, role="mention")]),
        )

    def _verdict(self, wid: str, trace_ref: str | None) -> Warrant:
        return Warrant(
            id=wid,
            target=self.target.id,
            type=WarrantType.DEMONSTRATIVE,
            commitment="kappa-rubric",
            verdict="fail",
            trace_ref=trace_ref,
            validity_node=self.nu.id,
        )

    def _assert_refused(self, warrant: Warrant) -> None:
        before = self.harness.log.path.read_bytes()
        with self.assertRaisesRegex(
            WellFormednessError, "conforming trial transcript"
        ):
            self.harness.create_artifact(
                "critic: the work fails std-2",
                provenance=Provenance(role="critic"),
                warrants=[warrant],
            )
        # Refused before anything durable was written, and no edge landed.
        self.assertEqual(self.harness.log.path.read_bytes(), before)
        self.assertNotIn(warrant.id, self.harness.warrants)
        self.assertEqual(self.harness.state.status[self.target.id], Status.ACCEPTED)

    def test_rubric_warrant_without_any_trace_ref_is_refused(self) -> None:
        self._assert_refused(self._verdict("w-no-trace", None))

    def test_rubric_warrant_with_a_nonconforming_transcript_is_refused(self) -> None:
        # Well formed JSON, wrong content: the decisive point appears nowhere
        # in the exchange, so the ruling is not re-checkable against it.
        ref = self.harness.blobs.put(
            canonical_json(
                {
                    "case": "the work has a dissonance in bar 4",
                    "answer": "the defence says bar 4 resolves on the downbeat",
                    "ruling": {
                        "verdict": "fail",
                        "decisive_point": "a point nobody in this trial made",
                    },
                    "checks": {},
                }
            )
        )
        self._assert_refused(self._verdict("w-bad-trace", ref))

    def test_the_same_warrant_registers_with_a_conforming_transcript(self) -> None:
        """Positive control: the guard refuses content, not rubric warrants."""
        warrant = self._verdict(
            "w-good-trace",
            transcript_blob(
                self.harness,
                case="the work has a dissonance in bar 4",
                answer="the defence disputes that bar 4 is unresolved",
                decisive_point="dissonance in bar 4",
            ),
        )
        critic = self.harness.create_artifact(
            "critic: the work fails std-2",
            provenance=Provenance(role="critic"),
            warrants=[warrant],
        )
        self.assertIn("w-good-trace", self.harness.warrants)
        self.assertEqual(self.harness.state.status[self.target.id], Status.REFUTED)
        self.assertEqual(self.harness.state.status[critic.id], Status.ACCEPTED)


def _tree_listing(root) -> list[tuple[str, str]]:
    """(relative path, kind) for every entry under ``root``, sorted."""
    return sorted(
        (str(p.relative_to(root)), "dir" if p.is_dir() else "file")
        for p in root.rglob("*")
    )


class TimeTravelFenceTests(TempDirTestCase):
    def test_opening_a_time_travel_view_creates_no_file_or_directory(self) -> None:
        """``Harness.at`` materializes in memory only: opening one at any seq
        leaves the on-disk tree — files AND directories — exactly as it was."""
        root = self.tmp_path / "run"
        live = Harness(root)
        live.register_commitment(Commitment(id="k", eval="predicate:True"))
        claim = art(live, "a durable claim")
        attack(live, claim.id, "a durable attack")
        last_seq = max(event.seq for event in live.log.read())

        before = _tree_listing(root)
        self.assertTrue(before)  # the listing is not vacuously empty
        for seq in range(last_seq + 1):
            past = Harness.at(root, seq)
            self.assertTrue(past._read_only)
        self.assertEqual(_tree_listing(root), before)

        # Not even the blob/object/log sub-roots are created for a root that
        # has none of them yet.
        bare = self.tmp_path / "bare"
        bare.mkdir()
        empty_before = _tree_listing(bare)
        Harness.at(bare, 0)
        self.assertEqual(_tree_listing(bare), empty_before)
        self.assertEqual(empty_before, [])

    def test_sealed_holdout_blob_is_unreadable_before_its_reveal(self) -> None:
        """§10.5/§1: the holdout fence is physical, not advisory. A blob with
        an unrevealed holdout marker is refused by the time-travel view's
        FencedBlobStore, and becomes readable only at a fence after Reveal."""
        root = self.tmp_path / "run"
        live = Harness(root)
        sealed_bytes = b"held-out evidence: the 2027 replication series"
        artifact = live.create_artifact(
            sealed_bytes, codec="raw", provenance=Provenance(role="import")
        )
        ref = artifact.content_ref
        (root / "holdout").mkdir()
        (root / "holdout" / ref).write_bytes(sealed_bytes)
        sealed_seq = max(event.seq for event in live.log.read())

        past = Harness.at(root, sealed_seq)
        self.assertIsInstance(past.blobs, FencedBlobStore)
        self.assertIn(ref, past.blobs.sealed_refs)
        self.assertFalse(past.blobs.is_grounding_available(ref))
        with self.assertRaisesRegex(KeyError, "sealed at this historical fence"):
            past.blobs.get(ref)
        # The live, unfenced store still has the bytes: the fence is a property
        # of the historical view, not a deletion (D8).
        self.assertEqual(live.blobs.get(ref), sealed_bytes)

        reveal = live._commit(Rule.REVEAL, inputs=[artifact.id], outputs=[])
        revealed = Harness.at(root, reveal.seq)
        self.assertEqual(revealed.blobs.sealed_refs, frozenset())
        self.assertTrue(revealed.blobs.is_grounding_available(ref))
        self.assertEqual(revealed.blobs.get(ref), sealed_bytes)
        # The earlier fence is unchanged: revealing later does not unseal the past.
        self.assertIn(ref, Harness.at(root, sealed_seq).blobs.sealed_refs)


class ExplicitCarriageTests(HarnessTestCase):
    def test_carry_add_gives_a_registered_warrant_a_second_carrier(self) -> None:
        """``register_batch`` may carry an ALREADY-REGISTERED warrant on a new
        artifact without re-providing the warrant record. The relation lands in
        the event's ``carry_add``, materializes in ``state.carries``, and
        produces the attack edge — the whole point of keeping carriage out of
        ``Artifact.compute_id``."""
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
        self.assertIn("w-shared", self.harness.warrants)

        content_ref = "inline:second packaging of the attack"
        second = Artifact(
            id=Artifact.compute_id(content_ref, "utf8", Interface()),
            content_ref=content_ref,
            warrants=["w-shared"],
            provenance=Provenance(role="critic"),
        )
        registered = self.harness.register_batch([(second, [])])  # not re-provided

        self.assertEqual([a.id for a in registered], [second.id])
        event = list(self.harness.log.read())[-1]
        self.assertIn((second.id, "w-shared"), event.state_diff.carry_add)
        self.assertIn((second.id, "w-shared"), self.harness.state.carries)
        self.assertIn((second.id, target.id), self.harness.state.att)
        self.assertEqual(
            self.harness.carrier_ids("w-shared"), [first.id, second.id]
        )
        self.assertEqual(self.harness.carried_warrant_ids(second.id), ["w-shared"])

        # Both carriers attack, so attacking the shared nu disables both.
        attack(self.harness, nu.id, "shared-warrant-is-unsound")
        status = self.harness.state.status
        self.assertEqual(status[first.id], Status.REFUTED)
        self.assertEqual(status[second.id], Status.REFUTED)
        self.assertEqual(status[target.id], Status.ACCEPTED)

        # Replay rebuilds the carriage relation from the log, not from the
        # artifact record (which is content-addressed and cannot hold it).
        replayed = Harness(self.harness.root)
        self.assertIn((second.id, "w-shared"), replayed.state.carries)
        self.assertIn((second.id, target.id), replayed.state.att)
        self.assertEqual(
            replayed.state.model_dump_json(), self.harness.state.model_dump_json()
        )


class ConnZeroMapTests(HarnessTestCase):
    def test_conn_is_zero_for_every_artifact_and_is_still_serialized(self) -> None:
        """VENDOR_NOTES §D: the isolation/integration driver is stubbed (P0
        row), so ``conn`` is COMPUTED AS ZERO and persisted into every
        materialized state — the field is present with an entry per artifact,
        not absent and not partial."""
        premise = art(self.harness, "the premise")
        dependent = art(
            self.harness,
            "a dependent claim",
            interface=Interface(refs=[Ref(target=premise.id, role="dependence")]),
        )
        attack(self.harness, dependent.id, "a critic")

        conn = self.harness.state.conn
        self.assertEqual(set(conn), set(self.harness.state.artifacts))
        self.assertGreater(len(conn), 0)
        self.assertEqual(sorted(set(conn.values())), [0])
        self.assertIn('"conn":', self.harness.state.model_dump_json())
        # Unchanged by replay and by a time-travel view.
        self.assertEqual(Harness(self.harness.root).state.conn, conn)
        last_seq = max(event.seq for event in self.harness.log.read())
        self.assertEqual(Harness.at(self.harness.root, last_seq).state.conn, conn)
