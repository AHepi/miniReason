"""P-A4 worker-delivery recovery tests derived from live attempt-two bytes."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from minireason import provider_openai_compat as provider
from minireason.pilot import delivery
from minireason.pilot.delivery import output_policy
from minireason.pilot.pilot import Pilot
from minireason.pilot.recording import RecordedCalls
from minireason.pilot.templates import OUTPUT_SCHEMA
from minireason.reason.types import ReasonFailure


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).parent / "fixtures" / "live-20260917"
UC1_TASK = ROOT / "research" / "deepseek-flash-pilot" / "usecases" / "UC1-blender-blocking" / "task.json"
UC1_CEILING = FIXTURES / "UC1-attempt2-c0007-a00.response-body.json"
UC1_CEILING_SHA256 = "880d49b30b4472fccf100347d86fbdd902a7c98a53cd34510b771aec30120168"
SMALL_USAGE = {
    "prompt_tokens": 1,
    "completion_tokens": 1,
    "prompt_cache_hit_tokens": 0,
    "prompt_cache_miss_tokens": 1,
    "total_tokens": 2,
}
SIMPLE_TASK = {
    "task": "What is 6 times 7? Return the integer as plain text.",
    "features": {"short_closed": True},
    "check": {
        "source": (
            "import json, sys\n"
            "x = json.load(sys.stdin)\n"
            "value = x['artifact']['answer'] == '42'\n"
            "print(json.dumps({'relation_id':'pilot-result','value':value,'derivation':'fixture'}))\n"
        ),
        "expected": True,
        "scope": "The answer is 42.",
        "fixtures": {},
    },
}


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def read_json(path: Path) -> dict:
    return json.loads(read_text(path))


def complete(answer: str = "42", *, source_refs=()) -> dict:
    return {
        "status": "complete",
        "answer": answer,
        "source_refs": list(source_refs),
        "unresolved": [],
        "verification_refs": [],
    }


def scripted_content(value, *, finish_reason: str = "stop", usage=None) -> dict:
    content = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return {
        "content": content,
        "finish_reason": finish_reason,
        "usage": copy.deepcopy(usage or SMALL_USAGE),
    }


def user_packet(messages: list[dict], key: str | None = None) -> dict:
    for message in reversed(messages):
        if message.get("role") != "user":
            continue
        try:
            value = json.loads(message["content"])
        except (KeyError, TypeError, ValueError):
            continue
        if isinstance(value, dict) and (key is None or key in value):
            return value
    raise AssertionError(f"no user packet containing {key!r}")


class WorkerRecoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=os.environ["TMP"], prefix="p-a4-worker-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        network = mock.patch.object(provider, "_open", side_effect=AssertionError("NETWORK_FORBIDDEN"))
        network.start()
        self.addCleanup(network.stop)

    def pilot(self, name: str, task: dict, scripted) -> Pilot:
        return Pilot(copy.deepcopy(task), self.root / name, scripted=scripted, repo_root=ROOT)

    def test_output_policy_formula_defaults_control_cap_and_preflight_refusal(self) -> None:
        small = {"resolved_source_reads": [{"receipt": {"unit_id": "a" * 64, "start": 10, "end": 110}}]}
        policy = output_policy("evidence_read", small)
        self.assertEqual(policy["routed_bytes"], 100)
        self.assertEqual(policy["requested_output_bytes"], 100 + delivery.OUTPUT_FRAMING_BYTES)
        self.assertEqual(policy["output_token_upper_bound"], policy["requested_output_bytes"])
        self.assertEqual(policy["default_tokens"], 16384)
        self.assertEqual(policy["max_tokens"], 16384)

        large = {"resolved_source_reads": [{"receipt": {"unit_id": "b" * 64, "start": 0, "end": 20000}}]}
        raised = output_policy("plan", large)
        self.assertEqual(raised["requested_output_bytes"], 20000 + delivery.OUTPUT_FRAMING_BYTES)
        self.assertEqual(raised["max_tokens"], 384000)
        self.assertEqual(output_policy("route", large)["max_tokens"], 4096)

        pilot = self.pilot("preflight-refusal", SIMPLE_TASK, scripted=[])
        oversized = {"resolved_source_reads": [{"receipt": {
            "unit_id": "c" * 64,
            "start": 0,
            "end": delivery.ROUTE_LIMITS["deepseek-flash"]["maximum"] + 1,
        }}]}
        with mock.patch.object(pilot.calls, "call") as dispatch:
            with self.assertRaises(ReasonFailure) as caught:
                pilot.ask("evidence_read", oversized, OUTPUT_SCHEMA)
        self.assertEqual(caught.exception.code, "OUTPUT_RANGE_TOO_LARGE")
        self.assertEqual(caught.exception.record["status"], "refused")
        dispatch.assert_not_called()
        self.assertEqual((pilot.calls.logical_count, pilot.calls.count), (0, 0))

    def test_three_repairs_keep_original_context_immediate_failure_and_spend(self) -> None:
        bodies = [
            "{}",
            '{"status":"complete"}',
            '{"status":"bogus","answer":"x"}',
            '{"status":"complete","answer":1}',
        ]
        seen: list[dict] = []

        def scripted(**context):
            seen.append(context)
            return scripted_content(bodies[context["attempt"]])

        messages = [
            {"role": "system", "content": "Return one JSON object."},
            {"role": "user", "content": "Use the exact public source context."},
        ]
        calls = RecordedCalls(self.root / "three-repairs", scripted=scripted)
        with self.assertRaises(ReasonFailure) as caught:
            calls.call("answer", messages, schema=OUTPUT_SCHEMA)
        self.assertEqual(caught.exception.code, "SCHEMA_REJECTED")
        self.assertEqual((calls.logical_count, calls.count), (1, 4))
        self.assertEqual([receipt["status"] for receipt in calls.receipts], ["contract_rejected"] * 4)
        snapshot = calls.budget_snapshot()
        self.assertEqual(snapshot["attempts"], 4)
        self.assertEqual(snapshot["logical_calls"], 1)
        self.assertEqual(snapshot["usage"]["total_tokens"], 8)
        self.assertGreater(float(snapshot["estimated_usd"]), 0.0)

        for attempt in range(1, 4):
            self.assertEqual(seen[attempt]["messages"][:2], messages)
            self.assertEqual(
                seen[attempt]["messages"][-2],
                {"role": "assistant", "content": bodies[attempt - 1]},
            )
            previous = read_json(
                self.root / "three-repairs" / "calls" / "c0001" /
                f"a{attempt - 1:02d}" / "outcome.json"
            )
            repair = seen[attempt]["messages"][-1]["content"]
            self.assertIn(previous["validation_error"], repair)
            self.assertIn(f"schema repair {attempt} of 3", repair)
        self.assertFalse((self.root / "three-repairs" / "calls" / "c0001" / "a04").exists())

    def test_live_uc1_ceiling_bytes_recover_through_actual_decomposition_plan(self) -> None:
        body = read_text(UC1_CEILING)
        self.assertEqual(hashlib.sha256(body.encode("utf-8")).hexdigest(), UC1_CEILING_SHA256)
        custody = read_json(FIXTURES / "ATTEMPT2-CUSTODY.json")
        source = next(row for row in custody["entries"]
                      if row["occurrence"].startswith("UC1-attempt2") and row["call_id"] == "c0007")
        self.assertEqual(source["finish_reason"], "length")
        seen: list[dict] = []
        holder: dict[str, Pilot] = {}

        def scripted(**context):
            seen.append(context)
            if context["role"] == "plan" and context["call_id"] == "c0001":
                return scripted_content(body, finish_reason="length", usage=source["usage"])
            if context["role"] == "plan":
                inputs = copy.deepcopy(holder["pilot"].input_ref)
                inputs["overrides"] = {
                    "task": "Answer the bounded arithmetic leaf: what is 6 times 7?",
                }
                return scripted_content({"steps": [{
                    "id": "bounded-arithmetic",
                    "template_id": "direct_answer",
                    "inputs": inputs,
                    "depends_on": [],
                }]})
            if context["role"] == "direct_answer":
                return scripted_content(complete())
            raise AssertionError(f"unexpected role {context['role']}")

        pilot = self.pilot("uc1-live-ceiling", read_json(UC1_TASK), scripted)
        holder["pilot"] = pilot
        pilot.critics = []
        result = pilot.execute_template("decompose_synthesize", pilot.inputs, 1)
        self.assertEqual(result["status"], "partial")
        self.assertEqual(result["answer"], "Partial decomposition; see recorded leaf results")
        self.assertEqual(
            [item["prepared"]["kwargs"]["max_tokens"] for item in seen[:2]],
            [16384, 384000],
        )
        self.assertEqual([item["role"] for item in seen], ["plan", "plan", "direct_answer"])
        self.assertEqual((pilot.calls.logical_count, pilot.calls.count), (3, 3))

        response = read_json(pilot.root / "calls" / "c0001" / "a00" / "provider" / "call-0001.response.json")
        self.assertEqual(response["content"], body)
        self.assertEqual(hashlib.sha256(response["content"].encode("utf-8")).hexdigest(), source["public_content_sha256"])
        first = read_json(pilot.root / "calls" / "c0001" / "a00" / "outcome.json")
        self.assertEqual((first["status"], first["failure_code"]), ("failed", "CEILING_HIT"))
        self.assertEqual(first["public_content_sha256"], source["public_content_sha256"])
        self.assertEqual(read_json(pilot.root / "calls" / "c0001" / "a00" / "decision.json")["max_tokens"], 16384)
        self.assertEqual(read_json(pilot.root / "calls" / "c0002" / "a00" / "decision.json")["max_tokens"], 384000)

    def test_max_initial_ceiling_splits_exact_utf8_halves_then_synthesizes(self) -> None:
        task = copy.deepcopy(SIMPLE_TASK)
        task["inputs"] = {"premises": ["\u00e9\u03bb\u6f22\U0001f642" * 20]}
        seen: list[dict] = []

        def scripted(**context):
            seen.append(context)
            if len(seen) == 1:
                return scripted_content('{"status":"partial"', finish_reason="length")
            return scripted_content(complete("half" if context["role"] == "range-worker" else "joined"))

        pilot = self.pilot("split-halves", task, scripted)
        packet = {"inputs": copy.deepcopy(pilot.input_ref)}
        small_limit = {"maximum": 2048, "source": "isolated test cap", "scope": "test only"}
        with mock.patch.object(delivery, "WORKER_TOKENS", 32), \
             mock.patch.object(delivery, "OUTPUT_FRAMING_BYTES", 0), \
             mock.patch.dict(delivery.ROUTE_LIMITS, {"deepseek-flash": small_limit}):
            result = pilot.ask("direct_answer", packet, OUTPUT_SCHEMA)

        self.assertEqual(result["answer"], "joined")
        self.assertEqual((pilot.calls.logical_count, pilot.calls.count), (4, 4))
        self.assertEqual(seen[0]["prepared"]["kwargs"]["max_tokens"], 2048)
        self.assertEqual([context["role"] for context in seen],
                         ["direct_answer", "range-worker", "range-worker", "direct_answer"])
        original = pilot.task_inputs._units[pilot.input_ref["unit_id"]][pilot.input_ref["start"]:pilot.input_ref["end"]]
        halves = []
        ranges = []
        for context in seen[1:3]:
            fragment = user_packet(context["messages"], "resolved_source_reads")
            read = fragment["resolved_source_reads"][0]
            receipt = read["receipt"]
            ranges.append((receipt["start"], receipt["end"]))
            halves.append(read["content"].encode("utf-8"))
        self.assertEqual(halves[0] + halves[1], original)
        self.assertEqual(ranges[0][0], pilot.input_ref["start"])
        self.assertEqual(ranges[0][1], ranges[1][0])
        self.assertEqual(ranges[1][1], pilot.input_ref["end"])
        merged = user_packet(seen[3]["messages"], "range_results")
        self.assertEqual(len(merged["range_results"]), 2)
        first = read_json(pilot.root / "calls" / "c0001" / "a00" / "outcome.json")
        self.assertEqual((first["status"], first["failure_code"]), ("failed", "CEILING_HIT"))
        self.assertNotEqual(result["answer"], read_text(pilot.root / "calls" / "c0001" / "a00" / "provider" / "call-0001.response.json"))

    def test_repeated_same_range_stops_pass_then_model_can_continue_and_succeed(self) -> None:
        worker_calls = 0
        continue_packets: list[dict] = []
        stop_rule = "Stop after a verified complete answer or a second delivery failure."

        def scripted(**context):
            nonlocal worker_calls
            role = context["role"]
            packet = user_packet(context["messages"])
            if role == "route":
                return scripted_content({"template_id": "direct_answer", "reason": "Use the bounded direct worker."})
            if role == "spawn":
                inputs = copy.deepcopy(packet["inputs"])
                if packet["pass_number"] > 1:
                    inputs["overrides"] = {"premises": ["Changed second pass after recorded delivery failure."]}
                return scripted_content({"subtasks": [{"template_id": "direct_answer", "inputs": inputs}]})
            if role == "direct_answer":
                worker_calls += 1
                if worker_calls <= 2:
                    return scripted_content('{"status":"partial"', finish_reason="length")
                return scripted_content(complete())
            if role == "continue_or_stop":
                continue_packets.append(packet)
                verification_ref = packet["verification"]["verification_ref"]
                if len(continue_packets) == 1:
                    return scripted_content({
                        "decision": "continue",
                        "reason": verification_ref + " records worker delivery failure; retry with a changed premise mix.",
                        "stop_rule": stop_rule,
                        "what_changes_next": "Change the premise mix and rerun one direct worker.",
                    })
                return scripted_content({
                    "decision": "stop",
                    "reason": verification_ref + " records a verified complete answer.",
                    "stop_rule": stop_rule,
                    "what_changes_next": "",
                })
            raise AssertionError(f"unexpected role {role}")

        pilot = self.pilot("continue-after-ceiling", SIMPLE_TASK, scripted)
        result = pilot.run()
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["answer"], "42")
        self.assertEqual(worker_calls, 3)
        self.assertEqual((result["logical_calls"], result["calls"]), (9, 9))
        self.assertEqual(len(result["passes"]), 2)
        first_verification = result["passes"][0]["verification"]
        self.assertEqual(first_verification["failure_code"], "WORKER_CEILING_REPEATED")
        self.assertEqual(first_verification["kind"], "worker-delivery-failure")
        self.assertEqual(continue_packets[0]["verification"], first_verification)
        self.assertEqual(continue_packets[0]["pass_number"], 1)
        first_ref = result["passes"][0]["spawned_refs"][0]["inputs"]
        second_ref = result["passes"][1]["spawned_refs"][0]["inputs"]
        self.assertNotEqual(first_ref["unit_id"], second_ref["unit_id"])
        self.assertEqual(
            pilot.task_inputs.expand_inputs(second_ref, call_id="test-second-pass")["premises"],
            ["Changed second pass after recorded delivery failure."],
        )
        for call_id in ("c0003", "c0004"):
            outcome = read_json(pilot.root / "calls" / call_id / "a00" / "outcome.json")
            self.assertEqual((outcome["status"], outcome["failure_code"]), ("failed", "CEILING_HIT"))
        self.assertEqual(read_json(pilot.root / "calls" / "c0008" / "a00" / "outcome.json")["status"], "accepted")

    def test_schema_exhaustion_stops_pass_then_changed_pass_succeeds(self) -> None:
        worker_attempts = 0
        continue_packets: list[dict] = []
        stop_rule = "Stop after a verified complete answer or a second delivery failure."

        def scripted(**context):
            nonlocal worker_attempts
            role = context["role"]
            packet = user_packet(context["messages"])
            if role == "route":
                return scripted_content({"template_id": "direct_answer", "reason": "Use the bounded direct worker."})
            if role == "spawn":
                inputs = copy.deepcopy(packet["inputs"])
                if packet["pass_number"] > 1:
                    inputs["overrides"] = {"premises": ["Changed second pass after schema delivery failure."]}
                return scripted_content({"subtasks": [{"template_id": "direct_answer", "inputs": inputs}]})
            if role == "direct_answer":
                worker_attempts += 1
                return scripted_content({} if worker_attempts <= 4 else complete())
            if role == "continue_or_stop":
                continue_packets.append(packet)
                verification_ref = packet["verification"]["verification_ref"]
                if len(continue_packets) == 1:
                    return scripted_content({
                        "decision": "continue",
                        "reason": verification_ref + " records exhausted schema delivery; retry with changed inputs.",
                        "stop_rule": stop_rule,
                        "what_changes_next": "Change the premise mix and rerun one direct worker.",
                    })
                return scripted_content({
                    "decision": "stop",
                    "reason": verification_ref + " records a verified complete answer.",
                    "stop_rule": stop_rule,
                    "what_changes_next": "",
                })
            raise AssertionError(f"unexpected role {role}")

        pilot = self.pilot("continue-after-schema", SIMPLE_TASK, scripted)
        result = pilot.run()
        self.assertEqual((result["status"], result["answer"]), ("complete", "42"))
        self.assertEqual(worker_attempts, 5)
        self.assertEqual((result["logical_calls"], result["calls"]), (8, 11))
        self.assertEqual(len(result["passes"]), 2)
        first_verification = result["passes"][0]["verification"]
        self.assertEqual(first_verification["failure_code"], "SCHEMA_REJECTED")
        self.assertEqual(first_verification["kind"], "worker-delivery-failure")
        self.assertEqual(continue_packets[0]["verification"], first_verification)
        self.assertEqual(continue_packets[0]["pass_number"], 1)
        rejected = [
            read_json(pilot.root / "calls" / "c0003" / f"a{attempt:02d}" / "outcome.json")
            for attempt in range(4)
        ]
        self.assertEqual([item["status"] for item in rejected], ["contract_rejected"] * 4)
        first_ref = result["passes"][0]["spawned_refs"][0]["inputs"]
        second_ref = result["passes"][1]["spawned_refs"][0]["inputs"]
        self.assertNotEqual(first_ref["unit_id"], second_ref["unit_id"])
        self.assertEqual(
            pilot.task_inputs.expand_inputs(second_ref, call_id="test-schema-second-pass")["premises"],
            ["Changed second pass after schema delivery failure."],
        )



if __name__ == "__main__":
    unittest.main()
