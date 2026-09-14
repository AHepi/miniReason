"""Spec §16 P0 acceptance, stated item by item.

The P0 row of the phase table reads:

    Deterministic core passes unit tests: grounded extension correctness,
    reinstatement (Lemma 3.1), two-pass support cascade, cycle rejection in
    `dep`, standard-refutation => dependent-verdict collapse => target
    reinstatement via closure, replay-from-log reproduces state
    byte-for-byte.

Each of those six items gets one named test here, reusing the scenarios the
vendored upstream suite already pins, so the acceptance row is checkable
without reading the rest of the suite. A seventh test is a deterministic
golden: two independent builds of the same small graph must produce
byte-identical JSONL logs and byte-identical object/blob files, and each
must replay to the same state.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

import deepreason_core
from deepreason_core.harness import Harness, WellFormednessError, transcript_blob
from deepreason_core.ontology import (
    Artifact,
    Commitment,
    Interface,
    Problem,
    ProblemProvenance,
    Provenance,
    Ref,
    Status,
    Warrant,
    WarrantType,
)

from . import golden_build
from .golden_build import build_reference_graph, frozen_clock
from .helpers import HarnessTestCase, TempDirTestCase, art, attack


class P0AcceptanceTests(HarnessTestCase):
    """The six P0 acceptance items of spec §16, one test each."""

    def test_p0_item_1_grounded_extension_correctness(self) -> None:
        """Dung grounded extension: unattacked => accepted; attacked from the
        extension => refuted; an unresolved attack cycle => suspended (§4)."""
        unattacked = art(self.harness, "an unattacked claim")
        self.assertEqual(self.harness.state.status[unattacked.id], Status.ACCEPTED)

        target = art(self.harness, "an attacked claim")
        critic, nu = attack(self.harness, target.id, "grounded-1")
        status = self.harness.state.status
        self.assertEqual(status[target.id], Status.REFUTED)
        self.assertEqual(status[critic.id], Status.ACCEPTED)
        self.assertEqual(status[nu.id], Status.ACCEPTED)

        # Mutual attack: neither side is in the (skeptical) grounded extension.
        nu1 = art(self.harness, "nu for the mutual attack A->B")
        nu2 = art(self.harness, "nu for the mutual attack B->A")
        w1 = Warrant(
            id="w-mutual-1", target="B", type=WarrantType.ARGUMENTATIVE,
            validity_node=nu1.id,
        )
        self.harness.register_artifact(
            Artifact(
                id="A", content_ref="inline:critic A", warrants=["w-mutual-1"],
                provenance=Provenance(role="critic"),
            ),
            warrants=[w1],
        )
        w2 = Warrant(
            id="w-mutual-2", target="A", type=WarrantType.ARGUMENTATIVE,
            validity_node=nu2.id,
        )
        self.harness.register_artifact(
            Artifact(
                id="B", content_ref="inline:critic B", warrants=["w-mutual-2"],
                provenance=Provenance(role="critic"),
            ),
            warrants=[w2],
        )
        self.assertEqual(self.harness.state.status["A"], Status.SUSPENDED)
        self.assertEqual(self.harness.state.status["B"], Status.SUSPENDED)

    def test_p0_item_2_reinstatement_lemma_3_1(self) -> None:
        """k attacks a, j attacks k, j unattacked => {j, a} accepted.
        Reinstatement is DERIVED from pass 1, never a rule (§3)."""
        a = art(self.harness, "the reinstated claim")
        k, _ = attack(self.harness, a.id, "refuter")
        self.assertEqual(self.harness.state.status[a.id], Status.REFUTED)

        j, _ = attack(self.harness, k.id, "refuter-of-the-refuter")
        status = self.harness.state.status
        self.assertEqual(status[j.id], Status.ACCEPTED)
        self.assertEqual(status[k.id], Status.REFUTED)
        self.assertEqual(status[a.id], Status.ACCEPTED)

    def test_p0_item_3_two_pass_support_cascade(self) -> None:
        """Pass 2 over the dep DAG: refuting a premise leaves its dependents
        ``suspended_unsupported``, NOT refuted — orphaned != false (§4)."""
        premise = art(self.harness, "the premise")
        dependent = art(
            self.harness,
            "the dependent claim",
            interface=Interface(refs=[Ref(target=premise.id, role="dependence")]),
        )
        grandchild = art(
            self.harness,
            "a claim depending on the dependent claim",
            interface=Interface(refs=[Ref(target=dependent.id, role="dependence")]),
        )
        self.assertEqual(self.harness.state.status[dependent.id], Status.ACCEPTED)
        self.assertEqual(self.harness.state.status[grandchild.id], Status.ACCEPTED)

        attack(self.harness, premise.id, "kills-the-premise")
        status = self.harness.state.status
        self.assertEqual(status[premise.id], Status.REFUTED)
        self.assertEqual(status[dependent.id], Status.SUSPENDED_UNSUPPORTED)
        # The cascade propagates through the whole DAG, still not as refutation.
        self.assertEqual(status[grandchild.id], Status.SUSPENDED_UNSUPPORTED)

    def test_p0_item_4_cycle_rejection_in_dep(self) -> None:
        """``dep`` must stay a DAG (§1): the registration whose materialized
        edges would close a cycle is rejected, and nothing is written."""
        a = Artifact(
            id="A",
            content_ref="inline:a",
            interface=Interface(refs=[Ref(target="B", role="dependence")]),
            provenance=Provenance(role="import"),
        )
        self.harness.register_artifact(a)  # dangling dependence: no edge yet
        before = self.harness.log.path.read_bytes()

        b = Artifact(
            id="B",
            content_ref="inline:b",
            interface=Interface(refs=[Ref(target="A", role="dependence")]),
            provenance=Provenance(role="import"),
        )
        with self.assertRaises(WellFormednessError):
            self.harness.register_artifact(b)

        self.assertEqual(self.harness.log.path.read_bytes(), before)
        self.assertNotIn("B", self.harness.state.artifacts)

    def test_p0_item_5_standard_refutation_collapses_verdicts_and_reinstates(self) -> None:
        """Case-law closure (§1/§10.3): refuting the standard attacks every nu
        citing it; the validity-node closure then disables every carrier, so
        the verdict's target reinstates — all inside pass 1."""
        self.harness.register_commitment(
            Commitment(id="kappa-standard", eval="rubric:std-1")
        )
        standard = art(self.harness, "standard std-1: no parallel fifths")
        target = art(
            self.harness,
            "the judged work",
            interface=Interface(commitments=["kappa-standard"]),
        )
        nu = art(
            self.harness,
            "nu: judged under std-1",
            interface=Interface(refs=[Ref(target=standard.id, role="mention")]),
        )
        verdict_warrant = Warrant(
            id="w-standard-verdict",
            target=target.id,
            type=WarrantType.DEMONSTRATIVE,
            commitment="kappa-standard",
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
            "critic: the work fails std-1",
            provenance=Provenance(role="critic"),
            warrants=[verdict_warrant],
        )
        self.assertEqual(self.harness.state.status[target.id], Status.REFUTED)

        attacker, _ = attack(self.harness, standard.id, "std-1-is-wrong")
        status = self.harness.state.status
        self.assertEqual(status[standard.id], Status.REFUTED)
        self.assertEqual(status[nu.id], Status.REFUTED)      # case-law closure
        self.assertEqual(status[critic.id], Status.REFUTED)  # validity-node closure
        self.assertEqual(status[target.id], Status.ACCEPTED)  # reinstated
        self.assertEqual(status[attacker.id], Status.ACCEPTED)



def _file_map(root) -> dict[str, str]:
    """relative path -> sha256 of the bytes, for every file under ``root``."""
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def _build_in_subprocess(root, *, cwd, hashseed: str) -> dict:
    """Build the reference graph in a SEPARATE interpreter and return its receipt."""
    src_dir = os.path.dirname(os.path.dirname(os.path.abspath(deepreason_core.__file__)))
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = hashseed
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = os.pathsep.join(
        [str(cwd), src_dir, *([env["PYTHONPATH"]] if env.get("PYTHONPATH") else [])]
    )
    completed = subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "tests.graph_core.golden_build", str(root)],
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "second-interpreter build failed\n"
            f"stdout: {completed.stdout}\nstderr: {completed.stderr}"
        )
    return json.loads(completed.stdout.strip().splitlines()[-1])


class P0ReplayDeterminismTests(TempDirTestCase):
    def test_p0_item_6_replay_from_log_reproduces_state_byte_for_byte(self) -> None:
        """Reopening a root replays the log through the SAME code path the
        live registration used, so the materialized state is byte-identical."""
        root = self.tmp_path / "run"
        live = build_reference_graph(root)
        replayed = Harness(root)

        self.assertEqual(
            replayed.state.model_dump_json(), live.state.model_dump_json()
        )
        self.assertEqual(replayed.commitments, live.commitments)
        self.assertEqual(replayed.warrants, live.warrants)
        # A time-travel view of the final seq agrees with the live view.
        last_seq = max(event.seq for event in live.log.read())
        self.assertEqual(
            Harness.at(root, last_seq).state.model_dump_json(),
            live.state.model_dump_json(),
        )

    def test_two_interpreters_build_byte_identical_roots(self) -> None:
        """Deterministic golden across PROCESSES, not just calls.

        An in-process "second build" reuses one interpreter's string-hash
        seed, so any set/dict iteration order that leaked into the written
        bytes would agree with itself and the assertion would pass on a
        genuinely nondeterministic core. The second root is therefore built
        by a separate interpreter started with a different ``PYTHONHASHSEED``;
        both builds take the same frozen clock, the only other nondeterministic
        input to the log.
        """
        parent_seed = os.environ.get("PYTHONHASHSEED", "<unset>")
        child_seed = "12345" if parent_seed == "0" else "0"

        first_root = self.tmp_path / "first"
        with frozen_clock():
            first = build_reference_graph(first_root)

        second_root = self.tmp_path / "second"
        receipt = _build_in_subprocess(
            second_root,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            hashseed=child_seed,
        )
        # The second build really happened elsewhere, under another seed.
        self.assertNotEqual(receipt["pid"], os.getpid())
        self.assertEqual(receipt["pythonhashseed"], child_seed)
        self.assertNotEqual(receipt["pythonhashseed"], parent_seed)

        # Non-emptiness and shape FIRST: comparing two empty trees is not a
        # byte-identity proof, and a truncated build must fail loudly here.
        first_log = (first_root / "log.jsonl").read_bytes()
        second_log = (second_root / "log.jsonl").read_bytes()
        first_objects = _file_map(first_root / "objects")
        first_blobs = _file_map(first_root / "blobs")
        second_objects = _file_map(second_root / "objects")
        second_blobs = _file_map(second_root / "blobs")

        self.assertTrue(first_log)
        self.assertEqual(
            len(first_log.splitlines()), golden_build.EXPECTED_EVENTS
        )
        self.assertEqual(len(first.state.artifacts), golden_build.EXPECTED_ARTIFACTS)
        self.assertEqual(len(first_objects), golden_build.EXPECTED_OBJECTS)
        self.assertEqual(len(first_blobs), golden_build.EXPECTED_BLOBS)
        self.assertEqual(receipt["events"], golden_build.EXPECTED_EVENTS)
        self.assertEqual(receipt["artifacts"], golden_build.EXPECTED_ARTIFACTS)
        self.assertEqual(receipt["objects"], golden_build.EXPECTED_OBJECTS)
        self.assertEqual(receipt["blobs"], golden_build.EXPECTED_BLOBS)

        # Then the byte identity itself, compared from the parent.
        self.assertEqual(first_log, second_log)
        self.assertEqual(sorted(first_objects.items()), sorted(second_objects.items()))
        self.assertEqual(sorted(first_blobs.items()), sorted(second_blobs.items()))
        # The whole root, not just the parts named above.
        self.assertEqual(_file_map(first_root), _file_map(second_root))

        # ... and each root replays to the same state.
        self.assertEqual(
            Harness(first_root).state.model_dump_json(),
            Harness(second_root).state.model_dump_json(),
        )

    def test_two_in_process_builds_replay_alike(self) -> None:
        """The in-process replay check, kept alongside the cross-process
        golden: two roots built by this interpreter agree on state, so a
        failure of the cross-process test localizes to hash-seed dependence
        rather than to the construction itself."""
        first_root = self.tmp_path / "first"
        second_root = self.tmp_path / "second"
        with frozen_clock():
            first = build_reference_graph(first_root)
            second = build_reference_graph(second_root)

        self.assertEqual(
            (first_root / "log.jsonl").read_bytes(),
            (second_root / "log.jsonl").read_bytes(),
        )
        self.assertEqual(_file_map(first_root), _file_map(second_root))
        self.assertEqual(
            first.state.model_dump_json(), second.state.model_dump_json()
        )
        self.assertEqual(
            Harness(first_root).state.model_dump_json(),
            Harness(second_root).state.model_dump_json(),
        )
