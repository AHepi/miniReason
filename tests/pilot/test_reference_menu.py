from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from minireason.pilot.inputs import TaskInputs
from minireason.pilot.references import ReferenceMenu


class ReferenceMenuTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=os.environ["TMP"])
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.inputs = TaskInputs.from_task(
            {"task": "fixture", "inputs": {"task": "Use € exactly."}}, self.root
        )
        self.menu = ReferenceMenu(self.inputs)
        self.input_ref = self.inputs.input_ref

    def subtask(self, **changes):
        value = {
            "id": "leaf",
            "template_id": "direct_answer",
            "inputs": dict(self.input_ref),
            "depends_on": [],
            "source_reads": [],
        }
        value.update(changes)
        return value

    def test_snapshot_names_exact_input_unit_and_ranges(self) -> None:
        snapshot = self.menu.snapshot(1)
        entry = snapshot["namespaces"]["input_units"][0]
        self.assertEqual(snapshot["schema"], "pilot.reference-menu.pa5.v1")
        self.assertEqual(entry["ref"], self.input_ref["unit_id"])
        self.assertEqual(entry["input_ref"], self.input_ref)
        self.assertEqual(entry["range"], {"start": 0, "end": self.input_ref["end"]})
        self.assertEqual(entry["source_read"]["unit_id"], self.input_ref["unit_id"])
        self.assertEqual(snapshot["valid_ids"]["inputs"], [self.input_ref["unit_id"]])

    def test_artifact_namespaces_pass_visibility_and_read_unit(self) -> None:
        child = self.menu.register("child", "c0001", {"answer": "partial"}, 1, "partial")
        assembly = self.menu.register(
            "assembly", "sha256:" + "a" * 64, {"answer": "assembled"}, 2, "partial"
        )
        verification = self.menu.register(
            "verification", "sha256:" + "b" * 64, {"passed": False}, 2, "recorded"
        )
        first = self.menu.snapshot(1)
        second = self.menu.snapshot(2)
        self.assertEqual([item["ref"] for item in first["namespaces"]["children"]], ["c0001"])
        self.assertEqual(first["namespaces"]["assemblies"], [])
        self.assertEqual(second["namespaces"]["assemblies"][0], assembly)
        self.assertEqual(second["namespaces"]["verifications"][0], verification)
        self.assertIn(child["unit_id"], second["valid_ids"]["source_reads"])
        artifact = json.loads(self.menu.read_source(child["unit_id"])["content"])
        self.assertEqual(artifact["ref"], "c0001")
        self.assertEqual(artifact["status"], "partial")
        self.assertEqual(artifact["value"], {"answer": "partial"})

    def test_identical_registration_dedups_at_earliest_pass_and_conflict_refuses(self) -> None:
        later = self.menu.register("child", "c0001", {"answer": "same"}, 3, "accepted")
        earlier = self.menu.register("child", "c0001", {"answer": "same"}, 1, "accepted")
        self.assertEqual(later["unit_id"], earlier["unit_id"])
        self.assertEqual(earlier["pass_number"], 1)
        self.assertEqual(len(self.menu.snapshot(3)["namespaces"]["children"]), 1)
        with self.assertRaisesRegex(ValueError, "immutable reference conflict for child:c0001"):
            self.menu.register("child", "c0001", {"answer": "changed"}, 4, "accepted")
        with self.assertRaisesRegex(ValueError, "immutable reference conflict for child:c0001"):
            self.menu.register("child", "c0001", {"answer": "same"}, 4, "partial")

    def test_validate_subtasks_accepts_task_input_artifact_read_and_dependencies(self) -> None:
        child = self.menu.register("child", "c0001", {"answer": "partial"}, 1, "partial")
        first = self.subtask(
            id="first",
            source_reads=[{**child["source_read"], "limit": child["byte_count"]}],
            depends_on=["c0001"],
        )
        second = self.subtask(id="second", depends_on=["first"])
        before_receipts = list(self.inputs.receipts)
        self.assertIsNone(self.menu.validate_subtasks([first, second], pass_number=1))
        self.assertEqual(self.inputs.receipts, before_receipts)

    def test_raw_normalized_inputs_defer_without_parsing_or_mutation(self) -> None:
        raw_inputs = {
            "task": "Narrow one part of the fixture.",
            "premises": ["The established schema admits normalized inputs."],
            "documents": [],
        }
        subtask = self.subtask(template_id="critic_return", inputs=raw_inputs)
        before = deepcopy(subtask)
        before_receipts = list(self.inputs.receipts)
        self.assertIsNone(self.menu.validate_subtasks([subtask], pass_number=1))
        self.assertEqual(subtask, before)
        self.assertEqual(self.inputs.receipts, before_receipts)

    def test_child_ref_is_never_a_source_unit_and_error_lists_full_menu(self) -> None:
        child = self.menu.register("child", "c0001", {"answer": "partial"}, 1, "partial")
        invalid = self.subtask(
            source_reads=[{"unit_id": "c0001", "start": 0, "end": 1, "limit": 1}]
        )
        with self.assertRaises(ValueError) as caught:
            self.menu.validate_subtasks([invalid], pass_number=1)
        message = str(caught.exception)
        self.assertIn("'c0001'", message)
        self.assertIn(child["unit_id"], message)
        self.assertIn(self.input_ref["unit_id"], message)
        self.assertIn('"depends_on":["c0001"]', message)
        with self.assertRaisesRegex(ValueError, "invalid source-read unit id: 'c0001'"):
            self.menu.read_source("c0001")

    def test_invalid_input_range_dependency_and_utf8_boundary_list_valid_ids(self) -> None:
        child = self.menu.register("child", "c0001", {"answer": "ok"}, 1, "accepted")
        bad_input = self.subtask(inputs={**self.input_ref, "end": self.input_ref["end"] - 1})
        bad_dependency = self.subtask(depends_on=["missing-child"])
        euro = self.inputs._units[self.input_ref["unit_id"]].index("€".encode("utf-8"))
        bad_utf8 = self.subtask(source_reads=[{
            "unit_id": self.input_ref["unit_id"],
            "start": euro + 1,
            "end": euro + 3,
            "limit": 2,
        }])
        for invalid, expected in (
            (bad_input, "complete JSON unit"),
            (bad_dependency, "missing-child"),
            (bad_utf8, "splits UTF-8"),
        ):
            with self.subTest(expected=expected), self.assertRaises(ValueError) as caught:
                self.menu.validate_subtasks([invalid], pass_number=1)
            self.assertIn(expected, str(caught.exception))
            self.assertIn(child["unit_id"], str(caught.exception))

    def test_source_read_limit_is_host_schema_bound(self) -> None:
        invalid = self.subtask(source_reads=[{
            "unit_id": self.input_ref["unit_id"],
            "start": 0,
            "end": self.input_ref["end"],
            "limit": 65537,
        }])
        with self.assertRaisesRegex(ValueError, "invalid source-read range"):
            self.menu.validate_subtasks([invalid])


if __name__ == "__main__":
    unittest.main()
