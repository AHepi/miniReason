"""Hard persistence invariants: immutable records, unambiguous objects,
strict event order, and non-writing time-travel views.

Vendored from AHepi/DeepReason@9607fba tests/test_persistence_invariants.py;
see VENDOR_NOTES.md.
"""

from __future__ import annotations

import hashlib
import json

from pydantic import ValidationError

from deepreason_core.canonical import canonical_json
from deepreason_core.harness import Harness, ReadOnlyHarnessError, WellFormednessError
from deepreason_core.log.event_log import EventSequenceError
from deepreason_core.ontology import (
    Commitment,
    Interface,
    Problem,
    ProblemProvenance,
    Provenance,
    Rule,
)
from deepreason_core.storage.objects import ObjectConflictError, ObjectStore

from .helpers import TempDirTestCase


def _problem(pid: str = "pi-1", description: str = "a problem") -> Problem:
    return Problem(
        id=pid,
        description=description,
        criteria=["k"],
        provenance=ProblemProvenance.model_validate({"trigger": "seed", "from": []}),
    )


def _tree_digest(root) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(str(path.relative_to(root)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


class PersistenceInvariantTests(TempDirTestCase):
    def test_registered_ontology_records_are_deeply_immutable(self) -> None:
        harness = Harness(self.tmp_path / "run")
        commitment = harness.register_commitment(
            Commitment(
                id="k", eval="predicate:True", budget={"extra": {"case": "fixed"}}
            )
        )
        problem = harness.register_problem(_problem())
        artifact = harness.create_artifact(
            "claim",
            interface=Interface(commitments=[commitment.id]),
            provenance=Provenance(role="seed"),
        )

        with self.assertRaises(ValidationError):
            commitment.eval = "predicate:False"
        with self.assertRaisesRegex(TypeError, "immutable"):
            commitment.budget.extra["case"] = "rewritten"
        with self.assertRaisesRegex(TypeError, "immutable"):
            problem.criteria.append("another")
        with self.assertRaisesRegex(TypeError, "immutable"):
            artifact.interface.commitments.append("another")
        with self.assertRaises(ValidationError):
            artifact.provenance.school = "rewritten"

        self.assertEqual(Harness(harness.root).state, harness.state)

    def test_harness_rejects_same_id_commitment_and_problem_conflicts(self) -> None:
        harness = Harness(self.tmp_path / "run")
        harness.register_commitment(Commitment(id="k", eval="predicate:True"))
        harness.register_problem(_problem())
        before = harness.log.path.read_bytes()

        with self.assertRaisesRegex(WellFormednessError, "commitment id"):
            harness.register_commitment(Commitment(id="k", eval="predicate:False"))
        with self.assertRaisesRegex(WellFormednessError, "problem id"):
            harness.register_problem(_problem(description="a rewritten problem"))

        self.assertEqual(harness.log.path.read_bytes(), before)

    def test_object_store_is_namespaced_and_rejects_cross_schema_collision(self) -> None:
        store = ObjectStore(self.tmp_path / "objects")
        commitment = Commitment(id="shared-id", eval="predicate:True")
        store.put("commitment", commitment)

        self.assertTrue(store._schema_path("commitment", commitment.id).exists())
        self.assertFalse(store._path(commitment.id).exists())
        with self.assertRaisesRegex(ObjectConflictError, "conflicts"):
            store.put("problem", _problem(pid="shared-id"))
        with self.assertRaisesRegex(ObjectConflictError, "conflicts"):
            store.put("commitment", Commitment(id="shared-id", eval="predicate:False"))

        # Typed reads must not hide a second namespaced record in a corrupt root.
        problem = _problem(pid="shared-id")
        conflicting = {
            "schema": "problem",
            "id": problem.id,
            "data": problem.model_dump(mode="json", by_alias=True),
        }
        path = store._schema_path("problem", problem.id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(canonical_json(conflicting))
        with self.assertRaisesRegex(ObjectConflictError, "multiple schemas"):
            store.get("shared-id", schema="commitment")

    def test_legacy_flat_object_is_readable_and_lazily_namespaced(self) -> None:
        store = ObjectStore(self.tmp_path / "objects")
        commitment = Commitment(id="k-legacy", eval="predicate:True")
        record = {
            "schema": "commitment",
            "id": commitment.id,
            "data": commitment.model_dump(mode="json", by_alias=True),
        }
        legacy = store._path(commitment.id)
        legacy.parent.mkdir(parents=True, exist_ok=True)
        legacy.write_bytes(canonical_json(record))

        schema, loaded = store.get(commitment.id)
        self.assertEqual(schema, "commitment")
        self.assertEqual(loaded, commitment)
        store.put("commitment", commitment)
        self.assertTrue(legacy.exists())  # old record is never deleted (D8)
        self.assertTrue(store._schema_path("commitment", commitment.id).exists())

    def test_time_travel_harness_rejects_every_write_and_changes_no_bytes(self) -> None:
        root = self.tmp_path / "run"
        live = Harness(root)
        live.register_commitment(Commitment(id="k", eval="predicate:True"))
        live.register_problem(_problem())
        live.create_artifact("claim", provenance=Provenance(role="seed"))
        past = Harness.at(root, 1)
        before = _tree_digest(root)

        with self.assertRaisesRegex(ReadOnlyHarnessError, "read-only"):
            past.create_artifact("forbidden", provenance=Provenance(role="seed"))
        with self.assertRaisesRegex(ReadOnlyHarnessError, "read-only"):
            past.record_measure(inputs=["forbidden"])
        with self.assertRaisesRegex(RuntimeError, "read-only"):
            past.blobs.put(b"forbidden")
        with self.assertRaisesRegex(RuntimeError, "read-only"):
            past.objects.put("commitment", Commitment(id="other", eval="predicate:True"))
        with self.assertRaisesRegex(RuntimeError, "read-only"):
            past.log.append(list(live.log.read())[0])

        self.assertEqual(_tree_digest(root), before)

    def test_time_travel_does_not_create_or_repair_storage(self) -> None:
        missing = self.tmp_path / "missing"
        with self.assertRaises(FileNotFoundError):
            Harness.at(missing, 0)
        self.assertFalse(missing.exists())

        root = self.tmp_path / "run"
        harness = Harness(root)
        harness.create_artifact("durable", provenance=Provenance(role="seed"))
        with open(harness.log.path, "a", encoding="utf-8") as stream:
            stream.write('{"seq":1,"rule":"Meas')
        before = harness.log.path.read_bytes()
        with self.assertWarnsRegex(UserWarning, "dropping torn final line"):
            Harness.at(root, 1)
        self.assertEqual(harness.log.path.read_bytes(), before)

    def _reject_bad_sequence(self, bad_seq: int) -> None:
        root = self.tmp_path / "run"
        harness = Harness(root)
        harness.create_artifact("a", provenance=Provenance(role="seed"))
        harness.create_artifact("b", provenance=Provenance(role="seed"))
        records = [
            json.loads(line) for line in harness.log.path.read_text().splitlines()
        ]
        records[1]["seq"] = bad_seq
        harness.log.path.write_text(
            "".join(
                json.dumps(record, separators=(",", ":")) + "\n" for record in records
            )
        )

        with self.assertRaisesRegex(EventSequenceError, "expected 1"):
            Harness(root)

    def test_replay_rejects_duplicate_event_sequence(self) -> None:
        self._reject_bad_sequence(0)

    def test_replay_rejects_gapped_event_sequence(self) -> None:
        self._reject_bad_sequence(3)

    def test_failed_append_rolls_live_state_back_to_durable_log(self) -> None:
        root = self.tmp_path / "run"
        first, stale = Harness(root), Harness(root)
        durable = first.create_artifact("durable", provenance=Provenance(role="seed"))

        with self.assertRaises(Exception):
            stale.create_artifact("must roll back", provenance=Provenance(role="seed"))

        reopened = Harness(root)
        self.assertEqual(stale.state, reopened.state)
        self.assertEqual(set(stale.state.artifacts), {durable.id})
        self.assertEqual(stale._next_seq, 1)

    def test_event_log_rejects_wrong_seq_before_append(self) -> None:
        harness = Harness(self.tmp_path / "run")
        event = harness._commit(Rule.MEASURE, inputs=["ok"], outputs=[])
        wrong = event.model_copy(update={"seq": 7})

        with self.assertRaisesRegex(EventSequenceError, "expected 1"):
            harness.log.append(wrong)
