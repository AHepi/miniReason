"""P-A5 reference repair and prior-pass read integration."""
from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile
import traceback
import unittest
from unittest import mock

from minireason import provider_openai_compat as provider
from minireason.pilot.pilot import Pilot
from .test_worker_recovery import SIMPLE_TASK, complete, scripted_content, user_packet


class MultipassReferenceFlowTests(unittest.TestCase):
    def test_second_pass_consumes_host_menu_artifacts_and_repairs_synthesis(self):
        with tempfile.TemporaryDirectory(dir=os.environ["TMP"], prefix="pa5-flow-") as temp:
            seen, holder, rejected, errors = [], {}, [], []
            def scripted_inner(**ctx):
                packet = user_packet(ctx["messages"])
                seen.append((ctx["role"], packet))
                pilot = holder["pilot"]
                if ctx["role"] == "route":
                    return scripted_content({"template_id": "direct_answer", "reason": "Fixture arithmetic."})
                if ctx["role"] == "spawn":
                    ref = deepcopy(pilot.input_ref)
                    if packet["pass_number"] == 1:
                        return scripted_content({"subtasks": [{"template_id": "direct_answer", "inputs": ref}]})
                    menu = packet["reference_menu"]["namespaces"]
                    entries = [menu[name][0] for name in ("children", "assemblies", "verifications")]
                    self.assertTrue(all(item["pass_number"] == 1 for item in entries))
                    ref["overrides"] = {"task": "Use prior records to independently recheck the arithmetic."}
                    other = deepcopy(ref)
                    other["overrides"]["task"] = "Recheck the result using the partial dependency and state limitations."
                    return scripted_content({"subtasks": [
                        {"template_id": "direct_answer", "inputs": ref,
                         "source_reads": [item["source_read"] for item in entries]},
                        {"template_id": "direct_answer", "inputs": other}]})
                if ctx["role"] == "direct_answer":
                    if pilot.pass_number == 2 and "resolved_source_reads" in packet:
                        records = [json.loads(item["content"]) for item in packet["resolved_source_reads"]]
                        self.assertEqual([item["kind"] for item in records], ["child", "assembly", "verification"])
                        self.assertEqual(records[0]["status"], "partial")
                        self.assertEqual(records[1]["status"], "partial")
                        self.assertEqual(records[2]["value"]["kind"], "checker")
                    value = complete()
                    value.update(status="partial", unresolved=["Independently recheck this result."])
                    return scripted_content(value)
                if ctx["role"] == "assembly-synthesis":
                    if ctx["attempt"] == 0:
                        value = complete(source_refs=["stale-child"])
                        rejected.append(json.dumps(value, ensure_ascii=False))
                        return scripted_content(rejected[-1])
                    self.assertEqual(ctx["messages"][-2]["content"], rejected[-1])
                    repair = ctx["messages"][-1]["content"]
                    self.assertIn("UNAUTHORIZED_SYNTHESIS_REFERENCE", repair)
                    self.assertIn("valid IDs", repair)
                    for child in pilot.results:
                        self.assertIn(child["result_ref"], repair)
                        self.assertEqual(child["output_status"], "partial")
                    return scripted_content(complete(source_refs=[r["result_ref"] for r in pilot.results]))
                if ctx["role"] == "continue_or_stop":
                    self.assertEqual(packet["artifact"]["status"], "partial")
                    self.assertEqual(packet["verification"]["kind"], "checker", json.dumps(packet["verification"], ensure_ascii=False))
                    self.assertEqual(packet["verification"]["execution"]["comparison"], "agrees")
                    return scripted_content({"decision": "continue" if pilot.pass_number == 1 else "stop",
                        "reason": packet["verification"]["verification_ref"] + " records a passed arithmetic check, with partial dependency limitations retained.",
                        "what_changes_next": "Read prior artifacts and independently recheck with two dependent workers." if pilot.pass_number == 1 else "",
                        "stop_rule": "Stop after the second scripted verification."})
                raise AssertionError(ctx["role"])
            def scripted(**ctx):
                try:
                    return scripted_inner(**ctx)
                except AssertionError:
                    errors.append(traceback.format_exc())
                    raise
            with mock.patch.object(provider, "_open", side_effect=AssertionError("NETWORK_FORBIDDEN")):
                pilot = Pilot(SIMPLE_TASK, Path(temp) / "run", scripted=scripted)
                holder["pilot"] = pilot
                result = pilot.run()
            self.assertEqual(result["status"], "partial", result["detail"] + "\n" + "\n".join(errors))
            self.assertTrue(result["readable_outcome"])
            self.assertEqual(len(result["passes"]), 2)
            self.assertEqual(result["logical_calls"], 10)
            self.assertEqual(result["calls"], 11)
            outcomes = [r for r in pilot.calls.receipts if r["role"] == "assembly-synthesis"]
            self.assertEqual([r["status"] for r in outcomes], ["contract_rejected", "accepted"])
            self.assertEqual(outcomes[0]["call_id"], outcomes[1]["call_id"])
            self.assertEqual(result["passes"][0]["results"][0]["output_status"], "partial")
            self.assertEqual([p["continuation_decisions"][0]["decision"] for p in result["passes"]], ["continue", "stop"])


    def test_nested_partial_dependency_reaches_synthesis_without_becoming_complete(self):
        with tempfile.TemporaryDirectory(dir=os.environ["TMP"], prefix="pa5-nested-") as temp:
            holder, seen = {}, []
            def scripted(**ctx):
                packet = user_packet(ctx["messages"])
                seen.append(ctx)
                if ctx["role"] == "plan":
                    ref = deepcopy(holder["pilot"].input_ref)
                    ref["overrides"] = {"task": "Derive a bounded arithmetic contribution."}
                    dependent = deepcopy(ref)
                    dependent["overrides"]["task"] = "Check the earlier contribution and retain its unresolved work."
                    return scripted_content({"steps": [
                        {"id": "leaf", "template_id": "direct_answer", "inputs": ref, "depends_on": []},
                        {"id": "next", "template_id": "direct_answer", "inputs": dependent, "depends_on": ["leaf"]}]})
                if ctx["role"] == "direct_answer":
                    value = complete()
                    if not packet["inputs"]["premises"]:
                        value.update(status="partial", unresolved=["Exact fixture limitation."])
                    else:
                        dep = json.loads(packet["inputs"]["premises"][-1])
                        self.assertEqual(dep["result_ref"], "c0001")
                        self.assertEqual(dep["output_status"], "partial")
                    return scripted_content(value)
                if ctx["role"] == "decompose-critic":
                    self.assertEqual([r["output_status"] for r in packet["candidate"]], ["partial", "partial"])
                    return scripted_content({"verdict": "supported", "reason": "The partial contributions retain their limitations.", "objections": []})
                if ctx["role"] == "synthesis":
                    value = {**complete(), "steps": ["leaf", "next"], "dependencies": [], "synthesis": "42"}
                    if ctx["attempt"] == 0:
                        value["source_refs"] = ["missing-child"]
                    else:
                        self.assertIn("valid IDs", ctx["messages"][-1]["content"])
                        self.assertIn("c0001", ctx["messages"][-1]["content"])
                        self.assertIn("c0002", ctx["messages"][-1]["content"])
                        value["source_refs"] = ["c0001", "c0002"]
                    return scripted_content(value)
                raise AssertionError(ctx["role"])
            fixture_task = {**deepcopy(SIMPLE_TASK), "critic_seats": ["ollama/qwen3.5-397b.native"]}
            with mock.patch.object(provider, "_open", side_effect=AssertionError("NETWORK_FORBIDDEN")):
                pilot = Pilot(fixture_task, Path(temp) / "run", scripted=scripted)
                holder["pilot"] = pilot
                result = pilot.execute_template("decompose_synthesize", pilot.inputs, 1)
            self.assertEqual(result["status"], "partial")
            self.assertIn("Exact fixture limitation.", result["unresolved"])
            self.assertIn("PARTIAL_CHILD_NOT_ACCEPTED", "\n".join(result["unresolved"]))
            dependent = pilot.spawn_host._results["c0002"]
            self.assertEqual(dependent["depends_on"], ["c0001"])
            self.assertEqual(dependent["output_status"], "partial")
            repairs = [r for r in pilot.calls.receipts if r["role"] == "synthesis"]
            self.assertEqual([r["status"] for r in repairs], ["contract_rejected", "accepted"])
            self.assertEqual(repairs[0]["call_id"], repairs[1]["call_id"])


if __name__ == "__main__":
    unittest.main()
