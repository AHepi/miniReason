import copy
from collections import deque
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from minireason.pilot.pilot import Pilot, envelope
from minireason.pilot.templates import normalize_inputs

EXAMPLES = Path("research/deepseek-flash-pilot/examples")

class PilotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=os.environ["TMP"], prefix="p34-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.network = patch("socket.socket", side_effect=AssertionError("NETWORK_FORBIDDEN"))
        self.network.start()
        self.addCleanup(self.network.stop)

    def fixture(self, kind="direct"):
        return tuple(json.loads((EXAMPLES / (kind + suffix)).read_text(encoding="utf-8"))
                     for suffix in (".task.json", ".scripted.json"))

    def with_stop_decision(self, responses):
        """Consume the published fixture, then make the mandatory stop turn."""
        queue = deque(copy.deepcopy(responses))

        def scripted(**context):
            if context["role"] == "continue_or_stop":
                packet = json.loads(context["messages"][-1]["content"])
                verification_ref = packet["verification"]["verification_ref"]
                return {
                    "decision": "stop",
                    "reason": f"Verification {verification_ref} resolves this fixture.",
                    "what_changes_next": "",
                    "stop_rule": packet.get("stop_rule") or "Stop after the fixture answer is verified.",
                }
            if not queue:
                raise AssertionError("unexpected non-continuation fixture call")
            return queue.popleft()

        return scripted

    def test_full_offline_arithmetic_and_no_replay(self):
        task, scripted = self.fixture()
        pilot = Pilot(task, self.root / "run", scripted=self.with_stop_decision(scripted), max_calls=4)
        result = pilot.run()
        self.assertEqual((result["status"], result["answer"], result["calls"]), ("complete", "42", 4))
        self.assertEqual(result["logical_calls"], 4)
        self.assertEqual(result["verification"]["execution"]["comparison"], "agrees")
        for name in ["RUN.md", "TRACE.md", "ANSWER.md", "task.json", "assembly.json", "config.json"]:
            self.assertTrue((pilot.root / name).exists())
        with self.assertRaises(FileExistsError):
            Pilot(task, pilot.root, scripted=self.with_stop_decision(scripted))

    def test_full_evidence_and_quote_refusal(self):
        task, scripted = self.fixture("evidence")
        self.assertEqual(Pilot(task, self.root / "good", scripted=self.with_stop_decision(scripted)).run()["status"], "complete")
        scripted[-1]["quotes"][0]["quote"] = "timeout to 99 seconds"
        scripted.extend([copy.deepcopy(scripted[-1])] * 3)
        pilot = Pilot(task, self.root / "bad", scripted=self.with_stop_decision(scripted))
        result = pilot.run()
        self.assertEqual(result["status"], "partial")
        self.assertEqual((result["logical_calls"], result["calls"]), (4, 7))
        self.assertEqual(result["verification"]["failure_code"], "SCHEMA_REJECTED")
        outcomes = [json.loads((pilot.root / "calls" / "c0003" / attempt / "outcome.json").read_text(encoding="utf-8"))
                    for attempt in ("a00", "a01", "a02", "a03")]
        self.assertEqual([item["status"] for item in outcomes],
                         ["contract_rejected"] * 4)
        self.assertTrue(all("QUOTE_CUSTODY_FAILURE: quotes[0]" in item["validation_error"]
                            for item in outcomes))
        self.assertTrue(all("quote does not resolve to exact UTF-8 bytes" in item["validation_error"]
                            for item in outcomes))

    def test_budget_partial(self):
        task, scripted = self.fixture()
        result = Pilot(task, self.root / "budget", scripted=self.with_stop_decision(scripted), max_calls=2).run()
        self.assertEqual((result["status"], result["calls"]), ("partial", 2))

    def test_checker_disagreement(self):
        task, scripted = self.fixture()
        scripted[-1]["answer"] = "43"
        result = Pilot(task, self.root / "wrong", scripted=self.with_stop_decision(scripted)).run()
        self.assertEqual(result["status"], "partial")
        self.assertEqual(result["verification"]["execution"]["comparison"], "disagrees")

    def test_no_critic_is_unavailable(self):
        task, scripted = self.fixture()
        del task["check"]
        result = Pilot(task, self.root / "no-critic", scripted=self.with_stop_decision(scripted)).run()
        self.assertEqual(result["verification"]["status"], "unavailable")
        self.assertEqual(result["status"], "partial")

    def test_different_lineage_critic_path(self):
        task, scripted = self.fixture()
        del task["check"]
        task["critic_seats"] = ["ollama/qwen3.5-397b.native"]
        scripted.append({"verdict": "supported", "reason": "Multiplication yields 42.", "objections": []})
        result = Pilot(task, self.root / "critic", scripted=self.with_stop_decision(scripted)).run()
        self.assertEqual((result["status"], result["calls"]), ("complete", 5))
        self.assertEqual(result["verification"]["kind"], "different-lineage-critic")

    def test_same_lineage_alias_is_not_independent(self):
        task, scripted = self.fixture()
        del task["check"]
        task["critic_seats"] = ["ollama/deepseek-v4.1-flash.native"]
        result = Pilot(task, self.root / "same", scripted=self.with_stop_decision(scripted)).run()
        self.assertEqual((result["status"], result["calls"]), ("partial", 4))

    def test_tool_idempotence_order_and_fallback(self):
        task, scripted = self.fixture()
        pilot = Pilot(task, self.root / "tools", scripted=[scripted[-1]])
        call = {"id": "provider-1", "type": "function", "function": {"name": "route", "arguments": json.dumps({"template_id": "invented", "reason": "bad"})}}
        first = pilot.dispatch(call)
        self.assertEqual(pilot.dispatch(call), first)
        self.assertEqual(first["tool_call_id"], call["id"])
        self.assertEqual(pilot.route["template_id"], "direct_answer")
        call["function"]["arguments"] = json.dumps({"template_id": "direct_answer", "reason": "changed"})
        with self.assertRaises(ValueError): pilot.dispatch(call)
        with self.assertRaises(ValueError): pilot.handle_tool("verify", {"artifact_ref": "fake"})
        pilot.handle_tool("spawn", scripted[1])
        pilot.handle_tool("assemble", {"result_refs": [pilot.results[0]["result_ref"]], "answer": "42", "unresolved": []})
        pilot.handle_tool("verify", {"artifact_ref": pilot.artifact["artifact_ref"]})
        verification_ref = pilot.verification["verification_ref"]
        pilot.handle_tool("continue_or_stop", {
            "decision": "stop",
            "reason": f"Verification {verification_ref} supports stopping.",
            "what_changes_next": "",
            "stop_rule": "Stop after the arithmetic answer is verified.",
        })
        self.assertEqual(pilot.state, "COMPLETE")

    def test_sealed_inputs_cannot_be_replaced(self):
        task, scripted = self.fixture()
        pilot = Pilot(task, self.root / "sealed", scripted=[])
        pilot.handle_tool("route", scripted[0])
        scripted[1]["subtasks"][0]["inputs"]["task"] = "Different task"
        with self.assertRaises(ValueError): pilot.handle_tool("spawn", scripted[1])
        self.assertEqual(pilot.calls.count, 0)

    def test_false_verification_reference_refused(self):
        task, scripted = self.fixture()
        scripted[-1]["verification_refs"] = ["invented-pass"]
        result = Pilot(task, self.root / "refs", scripted=self.with_stop_decision(scripted)).run()
        self.assertEqual(result["status"], "failed")

    def test_checker_policy_blocks_filesystem(self):
        task, scripted = self.fixture()
        task["check"]["source"] = "import pathlib"
        result = Pilot(task, self.root / "policy", scripted=self.with_stop_decision(scripted)).run()
        self.assertEqual(result["verification"]["execution"]["status"], "REFUSED_POLICY")
        self.assertEqual(result["status"], "partial")

    def test_decomposition_with_dependencies_and_synthesis(self):
        task = {"task": "Compute two independent products and synthesize their sum.", "features": {"kind": "decompose"}, "critic_seats": ["ollama/qwen3.5-397b.native"]}
        inputs = normalize_inputs(task["task"])
        steps = [{"id": "s1", "template_id": "direct_answer", "inputs": normalize_inputs("Compute 2 times 3."), "depends_on": []},
                 {"id": "s2", "template_id": "direct_answer", "inputs": normalize_inputs("Use the prior result and add 4."), "depends_on": ["s1"]}]
        synthesis = {**envelope("10"), "steps": ["6", "10"], "dependencies": ["s2 uses s1"], "synthesis": "10"}
        scripts = [{"template_id": "decompose_synthesize", "reason": "There are separable results to synthesize."}, {"subtasks": [{"template_id": "decompose_synthesize", "inputs": inputs}]}, {"steps": steps}, envelope("6"), envelope("10"),
                   {"verdict": "supported", "reason": "The accepted leaves support the result.", "objections": []}, synthesis,
                   {"verdict": "supported", "reason": "The sum follows.", "objections": []}]
        result = Pilot(task, self.root / "decomp", scripted=self.with_stop_decision(scripts)).run()
        self.assertEqual((result["status"], result["calls"], result["answer"]), ("complete", 9, "10"))
        events = list((self.root / "decomp" / "events").glob("*.json"))
        self.assertGreaterEqual(sum("nested-spawn" in p.read_text(encoding="utf-8") for p in events), 2)


    def test_route_four_invalid_attempts_use_deterministic_fallback(self):
        task, scripted = self.fixture()
        invalid = {"template_id": "invented", "reason": "Invalid choice."}
        scripts = [invalid] * 4 + [scripted[1], scripted[2]]
        pilot = Pilot(task, self.root / "fallback", scripted=self.with_stop_decision(scripts))
        result = pilot.run()
        self.assertEqual((result["status"], result["calls"]), ("complete", 7))
        self.assertTrue(pilot.route["fallback"])

    def test_critic_return_two_lineages_and_use(self):
        task = {"task": "Criticize and revise this short arithmetic answer.", "features": {"kind": "critic"},
                "inputs": {"candidate": "6 times 7 is 42", "premises": ["Multiply the integers 6 and 7"], "objections": ["The answer might be 41"], "protected_obligations": ["Keep the multiplication question"]},
                "critic_seats": ["ollama/qwen3.5-397b.native", "ollama/glm-5.3.native"]}
        inputs = normalize_inputs(task["task"], task["inputs"])
        judgment = {"verdict": "supported", "reason": "Multiplication supports the statement.", "objections": []}
        returned = {**envelope("6 times 7 is 42"), "objections": [{"id": "o0001", "target": "6 times 7 is 42", "grounds": "The answer might be 41"}], "dispositions": [{"id": "o0001", "status": "rejected-with-reason", "reason": "Six groups of seven give 42, not 41."}], "revision": "6 times 7 is 42", "dependent_use": ""}
        scripts = [{"template_id": "critic_return", "reason": "An existing candidate needs criticism and revision."},
                   {"subtasks": [{"template_id": "critic_return", "inputs": inputs}]}, judgment, judgment, returned,
                   envelope("42 divided by 7 is 6"), judgment]
        # P-A2 deliberately has no production window declaration for GLM.
        # This offline test concerns two-lineage orchestration, so declare an
        # isolated synthetic window instead of granting that live route access.
        from minireason.pilot.inputs.preflight import _ROUTE_WINDOWS
        from minireason.reason.config import endpoint_for, load_endpoint_snapshot
        endpoint = endpoint_for("ollama/glm-5.3.native", load_endpoint_snapshot()["data"])
        fixture_window = {"model": endpoint.model, "family": endpoint.family,
                          "base_url": endpoint.base_url, "context_window": 64000,
                          "source_url": "offline-fixture-only:no-provider-qualification",
                          "identity_scope": "synthetic offline window for lineage fixture only"}
        from minireason.pilot.delivery import ROUTE_LIMITS
        with patch.dict(_ROUTE_WINDOWS, {"ollama/glm-5.3.native": fixture_window}), patch.dict(ROUTE_LIMITS, {"ollama/glm-5.3.native": {"maximum": 32768, "source": "offline-fixture", "scope": "synthetic output limit"}}):
            result = Pilot(task, self.root / "return", scripted=self.with_stop_decision(scripts)).run()
        self.assertEqual((result["status"], result["calls"]), ("complete", 8))

    def test_engineer_proposal_is_partial_and_fake_tests_refused(self):
        task = {"task": "Propose a bounded parser fix.", "features": {"kind": "engineer"},
                "inputs": {"allowed_files": ["parser.py"], "documents": [{"id": "parser.py", "text": "return False"}],
                           "behavior_contract": "Return True", "test_commands": ["python -m unittest"]},
                "critic_seats": ["ollama/qwen3.5-397b.native"]}
        inputs = normalize_inputs(task["task"], task["inputs"])
        proposal = {**envelope("Propose changing the boolean."), "patches": [{"path": "parser.py", "patch": "-return False\n+return True"}], "rationale": "Meet the bounded contract", "test_claims": []}
        route = {"template_id": "engineer_patch", "reason": "This is a bounded code change."}
        spawn = {"subtasks": [{"template_id": "engineer_patch", "inputs": inputs}]}
        judgment = {"verdict": "supported", "reason": "The proposal meets the requested behavior.", "objections": []}
        scripts = [route, spawn, proposal, judgment, {**proposal, "dispositions": []}, judgment]
        result = Pilot(task, self.root / "engineer", scripted=self.with_stop_decision(scripts)).run()
        self.assertEqual((result["status"], result["calls"]), ("partial", 7))
        self.assertFalse((self.root / "engineer" / "parser.py").exists())
        proposal = copy.deepcopy(proposal); proposal["test_claims"] = ["All tests passed"]
        result = Pilot(task, self.root / "fake-tests", scripted=self.with_stop_decision([route, spawn, proposal])).run()
        self.assertEqual((result["status"], result["calls"]), ("failed", 3))

    def test_rejected_assembly_preserves_state_and_action_id(self):
        task, scripted = self.fixture()
        pilot = Pilot(task, self.root / "refused-assembly", scripted=[scripted[-1]])
        pilot.handle_tool("route", scripted[0])
        pilot.handle_tool("spawn", scripted[1])
        arguments = {"result_refs": [pilot.results[0]["result_ref"]], "answer": "42", "unresolved": []}
        events_before = len(pilot.events)
        for rejected in [dict(arguments, answer="43"), dict(arguments, result_refs=["absent"])]:
            with self.assertRaises(ValueError):
                pilot.handle_tool("assemble", rejected, tool_call_id="assembly-1")
            self.assertIsNone(pilot.artifact)
            self.assertEqual(pilot.state, "CHILD_RESULTS_VALIDATED")
            self.assertNotIn("assembly-1", pilot.actions)
            self.assertEqual(len(pilot.events), events_before)
            self.assertFalse((pilot.root / "assembly.json").exists())
        self.assertEqual(pilot.finish("assembly refused")["answer"], "42")
        result = pilot.handle_tool("assemble", arguments, tool_call_id="assembly-1")
        self.assertEqual(result["status"], "assembled")
        self.assertEqual(pilot.artifact["answer"], "42")
        self.assertEqual(pilot.calls.count, 1)

    def test_tampered_assembly_cannot_be_verified(self):
        task, scripted = self.fixture()
        pilot = Pilot(task, self.root / "tamper", scripted=[scripted[-1]])
        pilot.handle_tool("route", scripted[0])
        pilot.handle_tool("spawn", scripted[1])
        pilot.handle_tool("assemble", {"result_refs": [pilot.results[0]["result_ref"]], "answer": "42", "unresolved": []})
        pilot.artifact["answer"] = "43"
        with self.assertRaisesRegex(ValueError, "CUSTODY"):
            pilot.handle_tool("verify", {"artifact_ref": pilot.artifact["artifact_ref"]})

if __name__ == "__main__": unittest.main()
