from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from minireason.pilot.recording import RecordedCalls
from minireason.pilot.spawn import SpawnHost
from minireason.pilot.templates import OUTPUT_SCHEMA, normalize_inputs


def output(status: str = "complete", answer: str = "done") -> dict:
    return {
        "status": status,
        "answer": answer,
        "source_refs": [],
        "unresolved": [] if status == "complete" else ["fixture boundary"],
        "verification_refs": [],
    }


def task(name: str, **extra) -> dict:
    value = {
        "id": name,
        "template_id": "direct_answer",
        "inputs": normalize_inputs(f"Solve fixture {name}."),
    }
    value.update(extra)
    return value


class SpawnHostTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=r"C:\tw34")
        self.addCleanup(self.temporary.cleanup)
        self.calls = type("CallsStub", (), {"root": Path(self.temporary.name)})()

    def test_constructor_enforces_host_bounds(self) -> None:
        for fanout in (0, 9, True):
            with self.subTest(fanout=fanout), self.assertRaises(ValueError):
                SpawnHost(object(), fanout=fanout)
        for depth in (0, 3, True):
            with self.subTest(depth=depth), self.assertRaises(ValueError):
                SpawnHost(object(), max_depth=depth)

    def test_invalid_later_task_causes_no_partial_dispatch(self) -> None:
        executed: list[str] = []

        def executor(template_id, inputs, depth):
            executed.append(inputs["task"])
            return output()

        host = SpawnHost(self.calls, executor=executor)
        invalid = [
            task("s1"),
            task("s2", depends_on=["s3"]),
        ]
        with self.assertRaises(ValueError):
            host.spawn(invalid, receipt={"decision": "fixture"})
        self.assertEqual(executed, [])

    def test_dependencies_are_earlier_and_results_are_host_minted(self) -> None:
        executed: list[tuple[dict, int]] = []

        def executor(template_id, inputs, depth):
            executed.append((inputs, depth))
            return output(answer=inputs["task"])

        host = SpawnHost(self.calls, executor=executor)
        results = host.spawn(
            [task("read"), task("answer", depends_on=["read"])],
            receipt="decision-1",
        )
        self.assertEqual(executed[0][0]["task"], "Solve fixture read.")
        self.assertEqual(executed[0][1], 1)
        self.assertEqual(executed[1][0]["task"], "Solve fixture answer.")
        self.assertEqual(executed[1][1], 1)
        injected = json.loads(executed[1][0]["premises"][-1])
        self.assertEqual(injected["result_ref"], "c0001")
        self.assertEqual(injected["output"]["answer"], "Solve fixture read.")
        self.assertEqual([item["result_ref"] for item in results], ["c0001", "c0002"])
        self.assertEqual([item["status"] for item in results], ["accepted", "accepted"])
        self.assertEqual(results[1]["depends_on"], ["read"])
        self.assertTrue((Path(self.temporary.name) / "children" / "c0001.json").is_file())
        self.assertTrue((Path(self.temporary.name) / "children" / "c0002.json").is_file())

    def test_partial_output_is_never_accepted_or_used_as_dependency(self) -> None:
        def executor(template_id, inputs, depth):
            return output("partial") if inputs["task"].endswith("first.") else output()

        host = SpawnHost(self.calls, executor=executor)
        with self.assertRaisesRegex(ValueError, "unaccepted"):
            host.spawn(
                [task("first"), task("second", depends_on=["first"])],
                receipt="decision-partial",
            )

    def test_nested_spawn_requires_a_new_receipt(self) -> None:
        host = SpawnHost(self.calls, executor=lambda *_: output())
        host.spawn([task("one")], depth=2, receipt={"id": "nested-1"})
        with self.assertRaisesRegex(ValueError, "new decision receipt"):
            host.spawn([task("two")], depth=2, receipt={"id": "nested-1"})
        result = host.spawn([task("three")], depth=2, receipt={"id": "nested-2"})
        self.assertEqual(result[0]["result_ref"], "c0002")

    def test_default_leaf_runs_one_recorded_call(self) -> None:
        with tempfile.TemporaryDirectory(dir=r"C:\tw34") as temporary:
            calls = RecordedCalls(
                Path(temporary) / "run",
                scripted=[{"content": json.dumps(output(answer="leaf"))}],
            )
            host = SpawnHost(calls)
            result = host.spawn([task("leaf")], receipt="leaf-decision")
        self.assertEqual(result[0]["status"], "accepted")
        self.assertEqual(result[0]["output"]["answer"], "leaf")
        self.assertEqual(calls.count, 1)

    def test_missing_inputs_and_unknown_template_are_rejected(self) -> None:
        host = SpawnHost(self.calls, executor=lambda *_: output())
        for invalid in (
            [{"template_id": "direct_answer"}],
            [{"template_id": "unknown", "inputs": {}}],
        ):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                host.spawn(invalid, receipt="invalid")

    def test_default_executor_refuses_compound_template(self) -> None:
        with tempfile.TemporaryDirectory(dir=r"C:\tw34") as temporary:
            calls = RecordedCalls(Path(temporary) / "compound", scripted=[])
            host = SpawnHost(calls)
            inputs = normalize_inputs(
                "Patch one file.",
                {
                    "allowed_files": ["a.py"],
                    "documents": [{"id": "a.py", "text": "pass"}],
                    "behavior_contract": "Return a bounded proposal.",
                    "test_commands": ["python -m unittest"],
                },
            )
            with self.assertRaisesRegex(ValueError, "multi-seat executor"):
                host.spawn(
                    [{"template_id": "engineer_patch", "inputs": inputs}],
                    receipt="compound-refusal",
                )
            self.assertEqual(calls.count, 0)


if __name__ == "__main__":
    unittest.main()
