"""P-A4 worker/control delivery contract tests grounded in live response bytes."""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile
import unittest

from minireason.pilot.manifest import CONTINUE_PARAMETERS, ROUTE_PARAMETERS, validate_tool_args
from minireason.pilot.pilot import Pilot
from minireason.pilot.templates import (
    EVIDENCE_SCHEMA,
    SPAWN_INPUT_SCHEMA,
    TEMPLATE_IDS,
    TEMPLATES,
    normalize_delivery,
    normalize_inputs,
    response_example,
    validate,
    worker_response_contract,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).parent / "fixtures" / "live-20260917"
USECASES = ROOT / "research" / "deepseek-flash-pilot" / "usecases"
TASK_PATHS = {
    "UC2": USECASES / "UC2-hard-to-vary-story" / "task.json",
    "UC3": USECASES / "UC3-reading-between-lines" / "task.json",
    "UC4": USECASES / "UC4-fw5-adversarial-mapping" / "task.json",
}


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def read_json(path: Path) -> dict:
    return json.loads(read_text(path))


class WorkerContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=os.environ["TMP"], prefix="worker-contract-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def test_normalize_delivery_changes_only_declared_prose(self) -> None:
        raw = {
            "status": "partial",
            "answer": {"heading": "Finding", "body": ["one", "two"]},
            "unresolved": {"question": ["what remains"]},
        }
        normalized = normalize_delivery(raw, EVIDENCE_SCHEMA)
        self.assertEqual(
            normalized["answer"],
            '{"body":["one","two"],"heading":"Finding"}',
        )
        self.assertEqual(normalized["unresolved"], ['{"question":["what remains"]}'])
        self.assertEqual(normalized["source_refs"], [])
        self.assertEqual(normalized["verification_refs"], [])
        self.assertEqual(normalized["quotes"], [])
        self.assertEqual(normalized["contradictions"], [])
        self.assertEqual(normalized["not_found"], [])
        validate(normalized, EVIDENCE_SCHEMA)

        bad_ref = {**raw, "source_refs": "story"}
        with self.assertRaisesRegex(ValueError, r"source_refs: expected array"):
            validate(normalize_delivery(bad_ref, EVIDENCE_SCHEMA), EVIDENCE_SCHEMA)
        with self.assertRaisesRegex(ValueError, "unexpected fields"):
            validate(normalize_delivery({**raw, "decision": "continue"}, EVIDENCE_SCHEMA), EVIDENCE_SCHEMA)

    def test_quote_defaults_do_not_change_exact_source_or_quote(self) -> None:
        raw = {
            "status": "partial",
            "answer": ["A", "B"],
            "quotes": [{
                "source_id": "story",
                "quote": "caf\u00e9",
                "claim": {"point": "opening bytes"},
            }],
        }
        normalized = normalize_delivery(raw, EVIDENCE_SCHEMA)
        self.assertEqual(normalized["answer"], "A\nB")
        self.assertEqual(normalized["quotes"][0]["source_id"], "story")
        self.assertEqual(normalized["quotes"][0]["quote"], "caf\u00e9")
        self.assertEqual(normalized["quotes"][0]["locator"], "")
        self.assertEqual(normalized["quotes"][0]["claim"], '{"point":"opening bytes"}')
        validate(normalized, EVIDENCE_SCHEMA)

    def test_worker_contract_uses_exact_task_document_bytes(self) -> None:
        text = "caf\u00e9 first line\nsecond line"
        inputs = normalize_inputs("Inspect the supplied story.", {
            "documents": [{"id": "story", "text": text}],
            "requested_claims": ["opening"],
        })
        contract = worker_response_contract("evidence_read", "reader", inputs)
        example = contract["response_example"]
        validate(example, contract["schema"])
        quote = example["quotes"][0]
        self.assertEqual(quote["source_id"], "story")
        self.assertEqual(quote["quote"], text)
        self.assertEqual(quote["locator"], f"bytes:0:{len(text.encode('utf-8'))}")
        self.assertIn("host resolves the exact quote bytes", contract["instruction"])

    def test_every_worker_contract_has_valid_filled_form_and_p_a4_ceiling(self) -> None:
        inputs = normalize_inputs("Assess the supplied unit.", {
            "documents": [{"id": "unit", "text": "exact unit text"}],
            "candidate": "candidate text",
            "allowed_files": ["allowed.py"],
            "requested_claims": ["claim"],
            "objections": ["objection"],
        })
        for template_id in TEMPLATE_IDS:
            with self.subTest(template_id=template_id):
                contract = worker_response_contract(template_id, "example-stage", inputs)
                validate(contract["response_example"], contract["schema"])
                self.assertTrue(all(seat["max_completion_tokens"] == 16384
                                    for seat in TEMPLATES[template_id]["seats"]))
                self.assertIn("three", TEMPLATES[template_id]["repair_rule"])

    def test_control_examples_preserve_action_fields_and_context(self) -> None:
        input_ref = {"unit_id": "a" * 64, "start": 0, "end": 51, "encoding": "json"}
        route = response_example(ROUTE_PARAMETERS, {
            "template_id": "evidence_read",
            "task": {"task": "Read the supplied story.", "inputs": input_ref},
        })
        self.assertEqual(route["template_id"], "evidence_read")
        validate(route, ROUTE_PARAMETERS)
        normalized_route = validate_tool_args("route", {
            "template_id": "evidence_read",
            "reason": {"finding": ["Use the supplied story", "Preserve source custody"]},
        })
        self.assertEqual(
            normalized_route["reason"],
            '{"finding":["Use the supplied story","Preserve source custody"]}',
        )

        verification_ref = "sha256:" + "b" * 64
        stop_rule = "Stop when the exact story claim is verified."
        decision = response_example(CONTINUE_PARAMETERS, {
            "inputs": input_ref,
            "verification": {"verification_ref": verification_ref, "status": "verified"},
            "stop_rule": stop_rule,
        })
        self.assertEqual(decision["decision"], "stop")
        self.assertIn(verification_ref, decision["reason"])
        self.assertEqual(decision["stop_rule"], stop_rule)
        validate(decision, CONTINUE_PARAMETERS)
        normalized_stop = validate_tool_args("continue_or_stop", {
            "decision": "stop", "reason": [verification_ref, "verified"], "stop_rule": stop_rule,
        })
        self.assertEqual(normalized_stop["what_changes_next"], "")
        self.assertEqual(normalized_stop["reason"], verification_ref + "\nverified")

    def test_dynamic_plan_example_uses_bounded_task_override(self) -> None:
        step_schema = {
            "type": "object",
            "properties": {
                "template_id": {"type": "string", "enum": list(TEMPLATE_IDS)},
                "inputs": deepcopy(SPAWN_INPUT_SCHEMA),
                "id": {"type": "string", "minLength": 1},
                "depends_on": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["template_id", "inputs", "id", "depends_on"],
            "additionalProperties": False,
        }
        schema = {
            "type": "object",
            "properties": {"steps": {"type": "array", "minItems": 1, "items": step_schema}},
            "required": ["steps"],
            "additionalProperties": False,
        }
        input_ref = {"unit_id": "c" * 64, "start": 0, "end": 7650, "encoding": "json"}
        resolved = normalize_inputs("Produce the complete original artifact.")
        example = response_example(schema, {"inputs": input_ref, "resolved_inputs": resolved})
        validate(example, schema)
        step = example["steps"][0]
        self.assertEqual(step["inputs"]["unit_id"], input_ref["unit_id"])
        self.assertNotEqual(step["inputs"]["overrides"]["task"], resolved["task"])
        self.assertIn("bounded decisive part", step["inputs"]["overrides"]["task"])

    def test_attempt2_repaired_evidence_is_accepted_with_host_resolved_spans(self) -> None:
        for usecase in ("UC2", "UC3", "UC4"):
            with self.subTest(usecase=usecase):
                body = read_text(FIXTURES / f"{usecase}-attempt2-c0003-a01.response-body.json")
                authored = json.loads(body)
                pilot = Pilot(
                    read_json(TASK_PATHS[usecase]),
                    self.root / usecase.lower(),
                    scripted=[{"content": body}],
                    repo_root=ROOT,
                )
                output = pilot.execute_template("evidence_read", pilot.inputs, 1)
                event = next(item for item in pilot.events if item["choice"] == "quote-locations-resolved")
                locations = event["evidence"]["locations"]
                self.assertEqual(len(locations), len(output["quotes"]))
                for index, location in enumerate(locations):
                    self.assertEqual(location["authored_locator_hint"], authored["quotes"][index]["locator"])
                    self.assertTrue(location["resolved_spans"])
                    span = location["resolved_spans"][0]
                    self.assertEqual(output["quotes"][index]["locator"], f"bytes:{span['start']}:{span['end']}")


if __name__ == "__main__":
    unittest.main()
