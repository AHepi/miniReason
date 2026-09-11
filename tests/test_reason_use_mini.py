"""Offline actual-Mini transport checks, independent of study interpretation."""
from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from minireason.provider import Settings
from minireason.reason_use_mini import (
    EMPTY_CRITICISM_TRANSPORT, STAGES, prepare_reason_use, run_reason_use,
)
from minireason.reason_use_study import stage_prompt as renderer


class ProseProvider:
    def __init__(self, failure_stage=None, cap=2048):
        self.settings = Settings(max_tokens=cap)
        self.requests = []
        self.failure_stage = failure_stage

    def complete(self, messages, *, json_output, coordinate):
        self.requests.append({"messages": messages, "json_output": json_output, "coordinate": coordinate})
        if coordinate["stage"] == self.failure_stage:
            raise RuntimeError("OFFLINE_INTENDED_TRANSPORT_FAILURE")
        return {"content": coordinate["stage"].upper() + "_ACTUAL λ ???\n",
                "usage": {"prompt_tokens": 11, "completion_tokens": 7}}


class ReasonUseMiniTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.material = {
            "source_text": "ONLY_SOURCE\n" + "source λ. " * 2000,
            "construction_text": "ONLY_ORIGINAL_CONSTRUCTION\n" + "construction λ. " * 1000,
            "criticism_text": "ONLY_FROZEN_CRITICISM\n" + "criticism λ. " * 1000,
            "use_data_text": "ONLY_USE_DATA",
            "use_questions_text": "ONLY_USE_QUESTIONS",
            "stage_instructions": {"respond": "Make a response.", "use": "Use the response."},
            "system_message": "RAW SYSTEM", "max_tokens": 2048,
        }

    def test_two_actual_stages_use_only_three_declared_ports_and_preserve_prose(self):
        provider = ProseProvider()
        result = run_reason_use(provider, self.root, **self.material)
        self.assertEqual(result["status"], "COMPLETE", result["alarms"])
        self.assertEqual(result["mini_outcome"]["calls"], 2)
        self.assertEqual([row["stage"] for row in result["history"]], list(STAGES))
        history = []
        for request, row in zip(provider.requests, result["history"]):
            self.assertFalse(request["json_output"])
            self.assertEqual(request["messages"][0], {"role": "system", "content": self.material["system_message"]})
            self.assertEqual(request["messages"][1]["content"], renderer(self.material, row["stage"], history))
            self.assertEqual(row["text"], row["answer"]["body"])
            self.assertEqual(row["text"], row["answer"]["commitments"])
            self.assertFalse(row["proposed_changes_installed"])
            history.append(row)
        use = json.loads((self.root / "requests/001-use.json").read_text())
        for marker in ("ONLY_SOURCE", "ONLY_ORIGINAL_CONSTRUCTION", "ONLY_FROZEN_CRITICISM"):
            self.assertNotIn(marker, use["mini_brief"])
            self.assertNotIn(marker, use["sent_prompt"])
        self.assertIn("RESPOND_ACTUAL λ ???\n", use["mini_brief"])
        self.assertEqual(use["source_fields_visible"], ["use_data_text", "use_questions_text"])
        self.assertFalse(use["source_packet_port_visible"])
        self.assertFalse(use["original_construction_port_visible"])
        self.assertFalse(use["criticism_port_visible"])
        manifest = json.loads((self.root / "manifest.json").read_text())
        stage = next(stage for stage in manifest["stages"] if stage["stage_id"] == "use")
        self.assertEqual(stage["ports"], ["use_data", "use_questions", "actual_response"])
        self.assertEqual(stage["kind_id"], "mini.verdict.v1")
        self.assertTrue(result["terminal_kind"]["transport_only"])
        events = [json.loads(line) for line in (self.root / "run/log.jsonl").read_text().splitlines()]
        artifacts = [event for event in events if event["type"] == "ARTIFACT_SUBMITTED"]
        self.assertEqual(len(artifacts), 7)
        self.assertTrue(all(event["payload"]["about"] == [] and event["payload"]["answers"] == [] for event in artifacts))

    def test_omitted_criticism_is_zero_bytes_and_marker_never_reaches_provider(self):
        material = {**self.material, "criticism_text": ""}
        provider = ProseProvider()
        result = run_reason_use(provider, self.root, **material)
        self.assertEqual(result["status"], "COMPLETE", result["alarms"])
        self.assertEqual((self.root / "sources/criticism.txt").read_bytes(), b"")
        self.assertTrue(provider.requests[0]["messages"][1]["content"].endswith("Supplemental criticism:\n"))
        brief = json.loads((self.root / "requests/001-respond.json").read_text())["mini_brief"]
        self.assertIn(EMPTY_CRITICISM_TRANSPORT, brief)
        self.assertTrue(all(EMPTY_CRITICISM_TRANSPORT not in request["messages"][1]["content"] for request in provider.requests))

    def test_extra_original_criticism_at_use_is_rejected_before_second_dispatch(self):
        from creib.forge.mini.runner import render_brief as original

        def contaminated(plan, state, blobs, stage, cycle=0):
            brief, exposed = original(plan, state, blobs, stage, cycle)
            if stage.stage_id == "use":
                brief += "\n\n" + self.material["criticism_text"]
            return brief, exposed

        provider = ProseProvider()
        with mock.patch("creib.forge.mini.runner.render_brief", side_effect=contaminated):
            result = run_reason_use(provider, self.root, **self.material)
        self.assertEqual(result["status"], "OPERATIONAL_FAILURE")
        self.assertEqual(len(provider.requests), 1)
        self.assertEqual([row["stage"] for row in result["history"]], ["respond"])
        self.assertIn("REASON_USE_ROUTING_MISMATCH", {alarm["code"] for alarm in result["alarms"]})

    def test_mutated_prepared_runtime_ports_fail_before_dispatch(self):
        prepared = prepare_reason_use(self.root / "prepared", **self.material)
        stages = tuple(replace(stage, ports=stage.ports + ("source",)) if stage.stage_id == "use" else stage
                       for stage in prepared.plan.stages)
        changed = replace(prepared, plan=replace(prepared.plan, stages=stages))
        provider = ProseProvider()
        result = run_reason_use(provider, self.root / "run", changed, **self.material)
        self.assertEqual(result["status"], "OPERATIONAL_FAILURE")
        self.assertEqual(provider.requests, [])
        self.assertIn("REASON_USE_PREPARED_PLAN_MISMATCH", {alarm["code"] for alarm in result["alarms"]})

    def test_reuses_prepared_root_without_recompilation_and_checks_source_binding(self):
        prepared = prepare_reason_use(self.root, **self.material)
        with mock.patch("minireason.reason_use_mini.compile_manifest", side_effect=AssertionError("unexpected recompile")):
            result = run_reason_use(ProseProvider(), self.root, prepared, **self.material)
        self.assertEqual(result["status"], "COMPLETE", result["alarms"])
        provider = ProseProvider()
        changed = replace(prepared, plan=replace(prepared.plan, sources=(
            replace(prepared.plan.sources[0], raw=b"changed"),) + prepared.plan.sources[1:]))
        result = run_reason_use(provider, self.root / "changed", changed, **self.material)
        self.assertEqual(result["status"], "OPERATIONAL_FAILURE")
        self.assertEqual(provider.requests, [])

    def test_use_failure_retains_actual_response_without_final_artifact(self):
        provider = ProseProvider(failure_stage="use")
        result = run_reason_use(provider, self.root, **self.material)
        self.assertEqual(result["status"], "OPERATIONAL_FAILURE")
        self.assertEqual([row["stage"] for row in result["history"]], ["respond"])
        self.assertIsNone(result["final"])
        self.assertTrue((self.root / "reason-use-result.json").exists())
        self.assertTrue((self.root / "reason-use-errata.json").exists())

    def test_no_return_prepared_route_cannot_be_rebound_to_present_route(self):
        material = {**self.material, "return_path": False}
        prepared = prepare_reason_use(self.root / "prepared", **material)
        provider = ProseProvider()
        changed = replace(prepared, plan=replace(prepared.plan, stages=tuple(
            replace(stage, ports=stage.ports + ("actual_response",)) if stage.stage_id == "use" else stage
            for stage in prepared.plan.stages)))
        result = run_reason_use(provider, self.root / "changed", changed, **material)
        self.assertEqual(result["status"], "OPERATIONAL_FAILURE")
        self.assertEqual(provider.requests, [])
        provider = ProseProvider()
        result = run_reason_use(provider, self.root / "changed-setting", prepared,
                              **{**material, "return_path": True})
        self.assertEqual(result["status"], "OPERATIONAL_FAILURE")
        self.assertEqual(provider.requests, [])

    def test_no_return_route_rejects_response_injected_into_actual_brief(self):
        from creib.forge.mini.runner import render_brief as original

        def contaminated(plan, state, blobs, stage, cycle=0):
            brief, exposed = original(plan, state, blobs, stage, cycle)
            if stage.stage_id == "use":
                brief += "\n\nRESPOND_ACTUAL λ ???\n"
            return brief, exposed

        provider = ProseProvider()
        with mock.patch("creib.forge.mini.runner.render_brief", side_effect=contaminated):
            result = run_reason_use(provider, self.root, **{**self.material, "return_path": False})
        self.assertEqual(result["status"], "OPERATIONAL_FAILURE")
        self.assertEqual(len(provider.requests), 1)
        self.assertEqual([row["stage"] for row in result["history"]], ["respond"])
        self.assertIn("REASON_USE_ROUTING_MISMATCH", {alarm["code"] for alarm in result["alarms"]})


if __name__ == "__main__":
    unittest.main()
