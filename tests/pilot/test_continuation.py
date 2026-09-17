from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from minireason.pilot.pilot import Pilot, envelope
from minireason.pilot.templates import normalize_inputs


TASK = {
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


def user_packet(messages: list[dict], key: str) -> dict:
    for message in messages:
        if message.get("role") != "user":
            continue
        try:
            value = json.loads(message["content"])
        except (KeyError, TypeError, ValueError):
            continue
        if isinstance(value, dict) and key in value:
            return value
    raise AssertionError(f"fixture packet with {key!r} was not found")


def provider_fixture(public: dict, usage: dict) -> dict:
    return {"content": json.dumps(public, ensure_ascii=False), "usage": usage}


def with_overrides(reference: dict, **overrides) -> dict:
    """Return one compact input reference with only declared mutable overrides."""
    value = copy.deepcopy(reference)
    self_contained = {"unit_id", "start", "end", "encoding", "overrides"}
    if "unit_id" not in value or set(value) - self_contained:
        raise AssertionError("fixture expected a compact P-A2 input reference")
    value["overrides"] = {**value.get("overrides", {}), **copy.deepcopy(overrides)}
    return value


SMALL_PRICED_USAGE = {
    "prompt_tokens": 1,
    "completion_tokens": 1,
    "reasoning_tokens": 0,
    "prompt_cache_hit_tokens": 0,
    "prompt_cache_miss_tokens": 1,
    "total_tokens": 2,
}


class ContinuationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=os.environ["TMP"], prefix="p38-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        network = patch("socket.socket", side_effect=AssertionError("NETWORK_FORBIDDEN"))
        network.start()
        self.addCleanup(network.stop)

    @staticmethod
    def three_pass_fixture(decision_packets: list[dict], spawn_packets: list[dict]):
        stop_rule = "Stop after pass 3 has a verified answer."

        def scripted(**context):
            role = context["role"]
            if role == "route":
                return {"template_id": "direct_answer", "reason": "Use the bounded direct fixture."}
            if role == "spawn":
                packet = user_packet(context["messages"], "pass_number")
                spawn_packets.append(copy.deepcopy(packet))
                inputs = copy.deepcopy(packet["inputs"])
                if packet["pass_number"] > 1:
                    inputs = with_overrides(
                        inputs,
                        premises=[f"Pass {packet['pass_number']} checks a changed premise mix."],
                    )
                return {"subtasks": [{"template_id": "direct_answer", "inputs": inputs}]}
            if role == "direct_answer":
                return envelope("42")
            if role == "continue_or_stop":
                packet = user_packet(context["messages"], "pass_number")
                decision_packets.append(copy.deepcopy(packet))
                verification_ref = packet["verification"]["verification_ref"]
                continuing = packet["pass_number"] < 3
                return {
                    "decision": "continue" if continuing else "stop",
                    "reason": f"Verification {verification_ref} is verified; "
                              + ("change the premise mix next." if continuing else "the stop rule is met."),
                    "what_changes_next": (
                        f"Change the direct subtask premises for pass {packet['pass_number'] + 1}."
                        if continuing else ""
                    ),
                    "stop_rule": stop_rule,
                }
            raise AssertionError(f"unexpected fixture role: {role}")

        return scripted

    def test_three_pass_rule_budget_input_and_per_pass_records(self) -> None:
        decision_packets: list[dict] = []
        spawn_packets: list[dict] = []
        pilot = Pilot(
            copy.deepcopy(TASK),
            self.root / "three-pass",
            scripted=self.three_pass_fixture(decision_packets, spawn_packets),
        )
        result = pilot.run()

        self.assertEqual((result["status"], result["answer"]), ("complete", "42"))
        self.assertEqual((result["logical_calls"], result["calls"]), (12, 12))
        self.assertEqual([item["pass_number"] for item in result["passes"]], [1, 2, 3])
        self.assertEqual(len(decision_packets), 3)
        self.assertEqual([packet["pass_number"] for packet in decision_packets], [1, 2, 3])
        self.assertEqual([packet["stop_rule"] for packet in decision_packets], [None, result["stop_rule"], result["stop_rule"]])
        for packet in decision_packets:
            self.assertIn("verification_ref", packet["verification"])
            self.assertIn("status", packet["verification"])
            self.assertTrue({
                "max_calls", "logical_calls", "remaining_calls", "attempts",
                "max_spend_usd", "estimated_usd", "remaining_usd", "ceiling_reached",
                "dispatch_allowed", "stop_reason",
            }.issubset(packet["budget"]))
        self.assertEqual([packet["pass_number"] for packet in spawn_packets], [1, 2, 3])
        first_ref = spawn_packets[0]["inputs"]
        self.assertEqual(set(first_ref), {"unit_id", "start", "end", "encoding"})
        self.assertEqual(len(first_ref["unit_id"]), 64)
        self.assertNotIn("premises", first_ref)
        self.assertNotIn("overrides", result["passes"][0]["spawned_refs"][0]["inputs"])
        self.assertEqual(
            pilot.task_inputs.expand_inputs(
                result["passes"][1]["spawned_refs"][0]["inputs"], "test-recorded-pass"
            )["premises"],
            ["Pass 2 checks a changed premise mix."],
        )
        for number, item in enumerate(result["passes"], 1):
            pass_path = pilot.root / "passes" / f"p{number:04d}" / "pass.json"
            self.assertTrue(pass_path.is_file())
            recorded = json.loads(pass_path.read_text(encoding="utf-8"))
            self.assertEqual(recorded["pass_number"], number)
            self.assertEqual(len(recorded["continuation_decisions"]), 1)
            self.assertIn(
                decision_packets[number - 1]["verification"]["verification_ref"],
                recorded["continuation_decisions"][0]["reason"],
            )
            self.assertIn("usage_and_spend", recorded)
            self.assertIn("cumulative_calls", recorded)
        run = (pilot.root / "RUN.md").read_text(encoding="utf-8")
        trace = (pilot.root / "TRACE.md").read_text(encoding="utf-8")
        for number in (1, 2, 3):
            self.assertIn(f"## Pass {number}", run)
            self.assertIn(f"## Pass {number}", trace)
        self.assertIn("No fixed pass count", run)
        self.assertIn("Spend is an estimate from published prices, not a bill", run)

    def test_identical_pass_is_refused_before_workers_then_host_stops(self) -> None:
        decisions: list[dict] = []
        worker_calls = 0
        stop_rule = "Stop when repetition cannot produce changed work."

        def scripted(**context):
            nonlocal worker_calls
            role = context["role"]
            if role == "route":
                return {"template_id": "direct_answer", "reason": "Use the direct fixture."}
            if role == "spawn":
                packet = user_packet(context["messages"], "pass_number")
                return {"subtasks": [{"template_id": "direct_answer", "inputs": packet["inputs"]}]}
            if role == "direct_answer":
                worker_calls += 1
                return envelope("42")
            if role == "continue_or_stop":
                packet = user_packet(context["messages"], "pass_number")
                decisions.append(copy.deepcopy(packet))
                verification_ref = packet["verification"]["verification_ref"]
                return {
                    "decision": "continue",
                    "reason": f"Verification {verification_ref} permits one changed pass.",
                    "what_changes_next": "Change the premises, despite this adversarial fixture repeating them.",
                    "stop_rule": stop_rule,
                }
            raise AssertionError(role)

        result = Pilot(copy.deepcopy(TASK), self.root / "repeat", scripted=scripted).run()
        self.assertEqual(result["status"], "partial")
        self.assertIn("REPEATED_IDENTICAL_PASS", result["detail"])
        self.assertEqual(worker_calls, 1)
        self.assertEqual(len(result["passes"]), 2)
        refusals = result["passes"][1]["refusals"]
        self.assertEqual([item["refusal_count"] for item in refusals], [1, 2, 3])
        self.assertEqual(len(decisions), 3)
        self.assertIsNotNone(decisions[1]["previous_refusal"])
        self.assertEqual(decisions[1]["previous_refusal"]["refusal_count"], 1)
        self.assertEqual(decisions[2]["previous_refusal"]["refusal_count"], 2)

    def test_continuation_semantic_failure_gets_one_recorded_repair(self) -> None:
        decision_attempts: list[int] = []
        stop_rule = "Stop when the fixture is verified."

        def scripted(**context):
            role = context["role"]
            if role == "route":
                return {"template_id": "direct_answer", "reason": "Use the direct fixture."}
            if role == "spawn":
                packet = user_packet(context["messages"], "pass_number")
                return {"subtasks": [{"template_id": "direct_answer", "inputs": packet["inputs"]}]}
            if role == "direct_answer":
                return envelope("42")
            if role == "continue_or_stop":
                packet = user_packet(context["messages"], "pass_number")
                decision_attempts.append(context["attempt"])
                if context["attempt"] == 0:
                    return {"decision": "continue", "reason": "Try again.", "what_changes_next": "", "stop_rule": stop_rule}
                verification_ref = packet["verification"]["verification_ref"]
                return {"decision": "stop", "reason": f"Verification {verification_ref} satisfies the rule.",
                        "what_changes_next": "", "stop_rule": stop_rule}
            raise AssertionError(role)

        result = Pilot(copy.deepcopy(TASK), self.root / "repair", scripted=scripted).run()
        self.assertEqual(result["status"], "complete")
        self.assertEqual((result["logical_calls"], result["calls"]), (4, 5))
        self.assertEqual(decision_attempts, [0, 1])
        receipts = [item for item in pilot_receipts(self.root / "repair") if item.get("call_id") == "c0004"]
        self.assertEqual([item["status"] for item in receipts], ["contract_rejected", "accepted"])

    def test_logical_call_ceiling_records_resource_stop(self) -> None:
        decisions: list[dict] = []
        spawns: list[dict] = []
        result = Pilot(
            copy.deepcopy(TASK),
            self.root / "ceiling",
            max_calls=3,
            scripted=self.three_pass_fixture(decisions, spawns),
        ).run()
        self.assertEqual(result["status"], "partial")
        self.assertEqual((result["logical_calls"], result["calls"]), (3, 3))
        self.assertEqual(result["detail"], "CALL_BUDGET")
        self.assertEqual(decisions, [])
        trace = (self.root / "ceiling" / "TRACE.md").read_text(encoding="utf-8")
        self.assertIn("CALL_BUDGET", trace)

    def test_stop_rule_may_only_be_preserved_or_tightened_with_or(self) -> None:
        pilot = Pilot(copy.deepcopy(TASK), self.root / "rules", scripted=[])
        pilot.last_verification = {"verification_ref": "verify-1"}
        pilot.stop_rule = "Stop when verified"
        base = {"decision": "stop", "reason": "verify-1 is verified", "what_changes_next": ""}
        pilot._validate_decision({**base, "stop_rule": "Stop when verified"})
        pilot._validate_decision({**base, "stop_rule": "Stop when verified OR stop if no call budget remains"})
        with self.assertRaisesRegex(ValueError, "STOP_RULE_RELAXATION_REFUSED"):
            pilot._validate_decision({**base, "stop_rule": "Stop when verified AND wait for another failure"})

    def test_default_and_task_level_logical_call_ceilings(self) -> None:
        default = Pilot(copy.deepcopy(TASK), self.root / "default-ceiling", scripted=[])
        self.assertEqual(default.calls.max_calls, 300)
        raised_task = copy.deepcopy(TASK)
        raised_task["max_calls"] = 450
        raised = Pilot(raised_task, self.root / "raised-ceiling", scripted=[])
        self.assertEqual(raised.calls.max_calls, 450)
        raised_task["max_spend_usd"] = 9.5
        spend = Pilot(raised_task, self.root / "raised-spend", scripted=[])
        self.assertEqual(spend.calls.budget_snapshot()["max_spend_usd"], "9.5")
        with self.assertRaisesRegex(ValueError, "MAX_CALLS_POSITIVE_INTEGER"):
            Pilot(copy.deepcopy(TASK), self.root / "invalid-ceiling", max_calls=0, scripted=[])

    def test_spend_ceiling_stops_after_first_priced_attempt(self) -> None:
        task = copy.deepcopy(TASK)
        task["max_spend_usd"] = 0.000001
        fixture_calls = 0

        def scripted(**context):
            nonlocal fixture_calls
            fixture_calls += 1
            self.assertEqual(context["role"], "route")
            return provider_fixture(
                {"template_id": "direct_answer", "reason": "Use the direct fixture."},
                SMALL_PRICED_USAGE,
            )

        result = Pilot(task, self.root / "spend-ceiling", scripted=scripted).run()
        self.assertEqual((result["status"], result["detail"]), ("partial", "SPEND_CEILING"))
        self.assertEqual((result["calls"], fixture_calls), (1, 1))
        self.assertEqual(result["logical_calls"], 1)
        self.assertTrue(result["budget"]["ceiling_reached"])
        self.assertFalse((self.root / "spend-ceiling" / "calls" / "c0002").exists())

    def test_spend_reached_by_rejected_attempt_blocks_schema_repair(self) -> None:
        task = copy.deepcopy(TASK)
        task["max_spend_usd"] = 0.000001
        fixture_calls = 0

        def scripted(**context):
            nonlocal fixture_calls
            fixture_calls += 1
            return provider_fixture({}, SMALL_PRICED_USAGE)

        result = Pilot(task, self.root / "repair-spend", scripted=scripted).run()
        self.assertEqual((result["status"], result["detail"]), ("partial", "SPEND_CEILING"))
        self.assertEqual((result["logical_calls"], result["calls"], fixture_calls), (1, 1, 1))
        self.assertFalse((self.root / "repair-spend" / "calls" / "c0001" / "a01").exists())

    def test_missing_priced_usage_stops_before_next_dispatch(self) -> None:
        fixture_calls = 0

        def scripted(**context):
            nonlocal fixture_calls
            fixture_calls += 1
            return provider_fixture(
                {"template_id": "direct_answer", "reason": "Use the direct fixture."},
                {},
            )

        result = Pilot(copy.deepcopy(TASK), self.root / "missing-usage", scripted=scripted).run()
        self.assertEqual((result["status"], result["detail"]), ("failed", "SPEND_UNKNOWN; USAGE_UNAVAILABLE"))
        self.assertEqual((result["calls"], fixture_calls), (1, 1))
        self.assertEqual(result["logical_calls"], 1)
        self.assertEqual(result["budget"]["missing_usage_receipts"], ["c0001/a00"])
        self.assertFalse((self.root / "missing-usage" / "calls" / "c0002").exists())

    def test_unavailable_verification_is_delivered_to_stop_decision(self) -> None:
        task = copy.deepcopy(TASK)
        del task["check"]
        seen: list[dict] = []

        def scripted(**context):
            role = context["role"]
            if role == "route":
                return {"template_id": "direct_answer", "reason": "Use the direct fixture."}
            if role == "spawn":
                packet = user_packet(context["messages"], "pass_number")
                return {"subtasks": [{"template_id": "direct_answer", "inputs": packet["inputs"]}]}
            if role == "direct_answer":
                return envelope("42")
            if role == "continue_or_stop":
                packet = user_packet(context["messages"], "pass_number")
                seen.append(copy.deepcopy(packet))
                verification_ref = packet["verification"]["verification_ref"]
                return {"decision": "stop", "reason": f"Verification {verification_ref} is unavailable.",
                        "what_changes_next": "", "stop_rule": "Stop when independent verification is unavailable."}
            raise AssertionError(role)

        result = Pilot(task, self.root / "unavailable", scripted=scripted).run()
        self.assertEqual(result["status"], "partial")
        self.assertEqual(seen[0]["verification"]["status"], "unavailable")
        self.assertEqual(seen[0]["verification"]["judgment"]["reason"], "Different-lineage critic unavailable")

    def test_critic_objections_are_delivered_to_stop_decision(self) -> None:
        task = copy.deepcopy(TASK)
        del task["check"]
        task["critic_seats"] = ["ollama/qwen3.5-397b.native"]
        seen: list[dict] = []

        def scripted(**context):
            role = context["role"]
            if role == "route":
                return {"template_id": "direct_answer", "reason": "Use the direct fixture."}
            if role == "spawn":
                packet = user_packet(context["messages"], "pass_number")
                return {"subtasks": [{"template_id": "direct_answer", "inputs": packet["inputs"]}]}
            if role == "direct_answer":
                return envelope("42")
            if role == "verify-critic":
                return {"verdict": "challenged", "reason": "The answer lacks a public derivation.",
                        "objections": ["Show the multiplication steps."]}
            if role == "continue_or_stop":
                packet = user_packet(context["messages"], "pass_number")
                seen.append(copy.deepcopy(packet))
                verification_ref = packet["verification"]["verification_ref"]
                return {"decision": "stop", "reason": f"Verification {verification_ref} contains an unresolved objection.",
                        "what_changes_next": "", "stop_rule": "Stop when a critic objection remains unresolved."}
            raise AssertionError(role)

        result = Pilot(task, self.root / "critic-objection", scripted=scripted).run()
        self.assertEqual(result["status"], "partial")
        self.assertEqual(seen[0]["verification"]["status"], "failed")
        self.assertEqual(seen[0]["verification"]["judgment"]["objections"], ["Show the multiplication steps."])

    def test_actual_pilot_reaches_depth_three_and_refuses_depth_four(self) -> None:
        task = copy.deepcopy(TASK)
        task["features"] = {"kind": "decompose"}
        task["critic_seats"] = ["ollama/qwen3.5-397b.native"]
        nested_inputs = normalize_inputs("Compute a bounded intermediate result.")
        plan_count = 0

        def decomposition(answer: str) -> dict:
            return {
                **envelope(answer),
                "steps": ["bounded leaf"],
                "dependencies": ["the leaf is accepted"],
                "synthesis": answer,
            }

        def scripted(**context):
            nonlocal plan_count
            role = context["role"]
            if role == "route":
                return {"template_id": "decompose_synthesize", "reason": "Use nested bounded dependencies."}
            if role == "spawn":
                packet = user_packet(context["messages"], "input_catalog")
                return {"subtasks": [{"template_id": "decompose_synthesize", "inputs": packet["inputs"]}]}
            if role == "plan":
                plan_count += 1
                packet = user_packet(context["messages"], "input_catalog")
                if plan_count == 1:
                    return {"steps": [{"id": "nested", "template_id": "decompose_synthesize",
                                       "inputs": with_overrides(packet["inputs"], task="Compute a bounded intermediate result."),
                                       "depends_on": []}]}
                return {"steps": [{"id": "leaf", "template_id": "direct_answer",
                                   "inputs": with_overrides(packet["inputs"], task="Compute 6 times 7."),
                                   "depends_on": []}]}
            if role == "direct_answer":
                return envelope("42")
            if role == "decompose-critic":
                return {"verdict": "supported", "reason": "The accepted result supports 42.", "objections": []}
            if role == "synthesis":
                return decomposition("42")
            if role == "continue_or_stop":
                packet = user_packet(context["messages"], "pass_number")
                verification_ref = packet["verification"]["verification_ref"]
                return {"decision": "stop", "reason": f"Verification {verification_ref} supports stopping.",
                        "what_changes_next": "", "stop_rule": "Stop after the depth-three result is verified."}
            raise AssertionError(role)

        pilot = Pilot(task, self.root / "depth-three", scripted=scripted)
        result = pilot.run()
        self.assertEqual((result["status"], result["answer"]), ("complete", "42"))
        nested_depths = [event["evidence"]["depth"] for event in pilot.events if event["choice"] == "nested-spawn"]
        self.assertEqual(nested_depths, [2, 3])

        refused = Pilot(task, self.root / "depth-four", scripted=[])
        with self.assertRaisesRegex(ValueError, "NO_RECURSIVE_DECOMPOSITION"):
            refused.execute_template("decompose_synthesize", nested_inputs, depth=3)
        self.assertEqual(refused.calls.logical_count, 0)

    def test_outer_multi_child_pass_records_synthesis(self) -> None:
        def scripted(**context):
            role = context["role"]
            if role == "route":
                return {"template_id": "direct_answer", "reason": "Use two bounded checks."}
            if role == "spawn":
                packet = user_packet(context["messages"], "pass_number")
                second = with_overrides(packet["inputs"], premises=["Independent second calculation."])
                return {"subtasks": [
                    {"template_id": "direct_answer", "inputs": packet["inputs"]},
                    {"template_id": "direct_answer", "inputs": second},
                ]}
            if role == "direct_answer":
                return envelope("42")
            if role == "assembly-synthesis":
                return envelope("42")
            if role == "continue_or_stop":
                packet = user_packet(context["messages"], "pass_number")
                verification_ref = packet["verification"]["verification_ref"]
                return {"decision": "stop", "reason": f"Verification {verification_ref} supports stopping.",
                        "what_changes_next": "", "stop_rule": "Stop after both checks synthesize and verify."}
            raise AssertionError(role)

        pilot = Pilot(copy.deepcopy(TASK), self.root / "multi", scripted=scripted)
        result = pilot.run()
        self.assertEqual((result["status"], result["logical_calls"], result["calls"]), ("complete", 6, 6))
        self.assertEqual(len(result["passes"][0]["spawned"]), 2)
        self.assertEqual(len(result["passes"][0]["results"]), 2)
        synthesis_decision = json.loads(
            (pilot.root / "calls" / "c0005" / "a00" / "decision.json").read_text(encoding="utf-8")
        )
        self.assertEqual(synthesis_decision["role"], "assembly-synthesis")


def pilot_receipts(root: Path) -> list[dict]:
    receipts = []
    for path in sorted((root / "calls").glob("c*/a*/outcome.json")):
        receipts.append(json.loads(path.read_text(encoding="utf-8")))
    return receipts


if __name__ == "__main__":
    unittest.main()
