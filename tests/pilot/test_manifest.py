from __future__ import annotations

import json
from pathlib import Path
import unittest

from minireason.pilot.manifest import TOOLS, get_tool, validate_tool_args
from minireason.pilot.templates import normalize_inputs


class ManifestTests(unittest.TestCase):
    def test_checked_in_json_matches_python_manifest(self) -> None:
        path = Path(__file__).parents[2] / "src" / "minireason" / "pilot" / "tools.json"
        self.assertEqual(json.loads(path.read_text(encoding="utf-8")), TOOLS)

    def test_every_schema_object_is_strict_and_required(self) -> None:
        def walk(schema: object) -> None:
            if not isinstance(schema, dict):
                return
            if schema.get("type") == "object":
                self.assertFalse(schema.get("additionalProperties", True))
                self.assertEqual(set(schema.get("properties", {})), set(schema.get("required", [])))
            for value in schema.values():
                if isinstance(value, dict):
                    walk(value)
                elif isinstance(value, list):
                    for item in value:
                        walk(item)

        self.assertEqual(
            [tool["function"]["name"] for tool in TOOLS],
            ["route", "spawn", "assemble", "verify", "continue_or_stop"],
        )
        for tool in TOOLS:
            self.assertEqual(tool["type"], "function")
            self.assertTrue(tool["function"]["strict"])
            walk(tool["function"]["parameters"])

    def test_route_and_spawn_validate_and_fail_closed(self) -> None:
        route = validate_tool_args("route", {"template_id": "direct_answer", "reason": "Short closed task."})
        self.assertEqual(route["template_id"], "direct_answer")
        with self.assertRaises(ValueError):
            validate_tool_args("route", {"template_id": "unknown", "reason": "x"})
        with self.assertRaises(ValueError):
            validate_tool_args("route", {"template_id": "direct_answer", "reason": "x", "extra": 1})
        with self.assertRaises(ValueError):
            get_tool("shell")

        packet = normalize_inputs("answer this")
        validate_tool_args("spawn", {"subtasks": [{"template_id": "direct_answer", "inputs": packet}] * 24})
        with self.assertRaises(ValueError):
            validate_tool_args("spawn", {"subtasks": [{"template_id": "direct_answer", "inputs": packet}] * 25})

    def test_beta_wire_subset_keeps_stronger_host_bounds(self) -> None:
        def walk(value):
            if isinstance(value, dict):
                self.assertFalse(set(value) & {"minLength", "maxLength", "minItems", "maxItems"})
                for item in value.values():
                    walk(item)
            elif isinstance(value, list):
                for item in value:
                    walk(item)
        for tool in TOOLS:
            walk(tool["function"]["parameters"])
        with self.assertRaises(ValueError):
            validate_tool_args("spawn", {"subtasks": []})
        with self.assertRaises(ValueError):
            validate_tool_args("route", {"template_id": "direct_answer", "reason": ""})

    def test_assemble_and_verify_contracts(self) -> None:
        validate_tool_args("assemble", {"result_refs": ["sha256:abc"], "answer": "result", "unresolved": []})
        validate_tool_args("verify", {"artifact_ref": "sha256:def"})
        with self.assertRaises(ValueError):
            validate_tool_args("verify", {"artifact_ref": ""})

    def test_continue_or_stop_contract(self) -> None:
        stop = {
            "decision": "stop",
            "reason": "The cited verification resolves the fixture.",
            "what_changes_next": "",
            "stop_rule": "Stop when the answer is verified.",
        }
        validate_tool_args("continue_or_stop", stop)
        validate_tool_args("continue_or_stop", {
            **stop,
            "decision": "continue",
            "what_changes_next": "Use evidence_read on the unresolved source claim.",
        })
        for invalid in (
            {**stop, "decision": "again"},
            {**stop, "reason": ""},
            {**stop, "stop_rule": ""},
        ):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                validate_tool_args("continue_or_stop", invalid)


if __name__ == "__main__":
    unittest.main()
