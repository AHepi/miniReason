from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile
import unittest

from minireason.pilot.assemble import assemble, carryable_result
from minireason.pilot.spawn import SpawnHost
from minireason.pilot.templates import normalize_inputs
from minireason.pilot.util import digest


def worker_output(status: str, answer: str, unresolved=None) -> dict:
    return {
        "status": status,
        "answer": answer,
        "source_refs": [],
        "unresolved": list(unresolved or []),
        "verification_refs": [],
    }


def subtask(name: str, *, depends_on=None) -> dict:
    value = {
        "id": name,
        "template_id": "direct_answer",
        "inputs": normalize_inputs(f"Solve fixture {name}."),
    }
    if depends_on is not None:
        value["depends_on"] = list(depends_on)
    return value


class PartialCarryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=os.environ["TMP"], prefix="partial-carry-")
        self.addCleanup(self.temporary.cleanup)
        self.calls = type("CallsStub", (), {"root": Path(self.temporary.name)})()

    def test_carryable_result_is_strict_for_partial_and_legacy_complete(self) -> None:
        legacy_complete = {
            "result_ref": "c0001",
            "status": "accepted",
            "output": worker_output("complete", "complete answer"),
        }
        explicit_partial = {
            "result_ref": "c0002",
            "status": "unaccepted",
            "output_status": "partial",
            "output": worker_output("partial", "partial answer", ["leaf remains"]),
        }
        self.assertTrue(carryable_result(legacy_complete))
        self.assertTrue(carryable_result(explicit_partial))

        for contradiction in (
            {**deepcopy(explicit_partial), "output_status": "complete"},
            {**deepcopy(explicit_partial), "status": "accepted"},
            {**deepcopy(explicit_partial), "output": worker_output("failed", "failed")},
            {**deepcopy(legacy_complete), "output_status": "partial"},
        ):
            with self.subTest(contradiction=contradiction):
                self.assertFalse(carryable_result(contradiction))

    def test_attempt3_shaped_partial_assembles_without_acceptance_laundering(self) -> None:
        child = {
            "result_ref": "c0001",
            "template_id": "evidence_read",
            "status": "unaccepted",
            "output_status": "partial",
            "depends_on": [],
            "output": worker_output(
                "partial",
                "attempt-3 public answer",
                ["HTV-6 remains supplementary"],
            ),
        }
        before = deepcopy(child)
        artifact = assemble([child])

        self.assertEqual(child, before)
        self.assertEqual(artifact["status"], "partial")
        self.assertEqual(artifact["answer"], "attempt-3 public answer")
        self.assertEqual(artifact["source_refs"], ["c0001"])
        self.assertEqual(artifact["dependencies"], {"c0001": digest(child)})
        self.assertIn("HTV-6 remains supplementary", artifact["unresolved"])
        self.assertIn("PARTIAL_CHILD_NOT_ACCEPTED", "\n".join(artifact["unresolved"]))
        self.assertEqual(child["status"], "unaccepted")

    def test_failed_or_cannot_decide_children_remain_refused(self) -> None:
        for output_status in ("failed", "cannot_decide"):
            child = {
                "result_ref": "c0001",
                "status": "unaccepted",
                "output_status": output_status,
                "output": worker_output(output_status, "not carryable"),
            }
            with self.subTest(output_status=output_status), self.assertRaisesRegex(
                ValueError, "UNACCEPTED_DEPENDENCY"
            ):
                assemble([child])

    def test_nested_partial_is_supplied_and_forces_dependent_partial(self) -> None:
        seen_dependencies: list[dict] = []

        def executor(template_id, inputs, depth):
            if inputs["task"].endswith("leaf."):
                return worker_output("partial", "partial leaf", ["retry leaf"])
            seen_dependencies.append(json.loads(inputs["premises"][-1]))
            return worker_output("complete", "claimed complete dependent")

        host = SpawnHost(self.calls, executor=executor)
        results = host.spawn(
            [subtask("leaf"), subtask("dependent", depends_on=["leaf"])],
            depth=2,
            receipt={"decision": "carry partial leaf"},
        )

        leaf, dependent = results
        self.assertEqual(leaf["status"], "unaccepted")
        self.assertEqual(leaf["output_status"], "partial")
        self.assertIn("PARTIAL_CHILD_NOT_ACCEPTED", leaf["refusal_reason"])
        self.assertEqual(seen_dependencies, [leaf])
        self.assertEqual(dependent["status"], "unaccepted")
        self.assertEqual(dependent["output_status"], "partial")
        self.assertEqual(dependent["output"]["status"], "partial")
        self.assertIn("Partial dependency c0001", "\n".join(dependent["output"]["unresolved"]))

        stored = json.loads(
            (Path(self.temporary.name) / "children" / "c0002.json").read_text(encoding="utf-8")
        )
        self.assertEqual(stored, dependent)

    def test_default_packet_labels_partial_separately_from_accepted(self) -> None:
        captured: dict = {}

        class TaskInputsStub:
            @staticmethod
            def compact_inputs(inputs):
                return {"unit_id": "a" * 64, "start": 0, "end": 64, "encoding": "json"}

        class CallsSpy:
            root = Path(self.temporary.name)
            task_inputs = TaskInputsStub()

            def call(spy_self, **kwargs):
                captured.update(kwargs)
                return worker_output("complete", "dependent")

        host = SpawnHost(CallsSpy())
        accepted = {
            "result_ref": "c0001",
            "status": "accepted",
            "output_status": "complete",
            "output": worker_output("complete", "accepted"),
        }
        partial = {
            "result_ref": "c0002",
            "status": "unaccepted",
            "output_status": "partial",
            "refusal_reason": "PARTIAL_CHILD_NOT_ACCEPTED: fixture",
            "output": worker_output("partial", "partial"),
        }
        output = host._default_execute(
            "direct_answer",
            normalize_inputs("Solve dependent fixture."),
            1,
            [accepted, partial],
            [],
        )
        packet = json.loads(captured["messages"][1]["content"])

        self.assertEqual(output["answer"], "dependent")
        self.assertEqual(packet["accepted_dependencies"], [accepted])
        self.assertEqual(packet["partial_dependencies"], [partial])
        self.assertNotIn(partial, packet["accepted_dependencies"])

    def test_invalid_later_subtask_still_dispatches_nothing(self) -> None:
        executed: list[str] = []

        def executor(template_id, inputs, depth):
            executed.append(inputs["task"])
            return worker_output("partial", "unused")

        host = SpawnHost(self.calls, executor=executor)
        with self.assertRaisesRegex(ValueError, "unavailable or forward dependencies"):
            host.spawn(
                [subtask("leaf"), subtask("bad", depends_on=["absent"])],
                receipt="validate whole batch",
            )
        self.assertEqual(executed, [])


if __name__ == "__main__":
    unittest.main()
