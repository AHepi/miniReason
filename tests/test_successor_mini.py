"""Offline custody/dispatch checks; scripted prose is not research evidence."""
from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from minireason.provider import Settings
from minireason.successor_data import STAGE_INSTRUCTIONS, SYSTEM_MESSAGE
from minireason.successor_mini import STAGES, prepare_successor, run_successor
from minireason.successor_study import stage_prompt


class ProseProvider:
    def __init__(self, failure_stage=None, cap=2048):
        self.settings = Settings(max_tokens=cap)
        self.requests = []
        self.failure_stage = failure_stage

    def complete(self, messages, *, json_output, coordinate):
        self.requests.append({"messages":messages,"json_output":json_output,"coordinate":coordinate})
        if coordinate["stage"] == self.failure_stage:
            raise RuntimeError("OFFLINE_INTENDED_TRANSPORT_FAILURE")
        return {"content":" NO SUCCESSOR JUSTIFIED: " + coordinate["stage"] + " λ ???\n",
                "usage":{"prompt_tokens":11,"completion_tokens":7}}


class SuccessorMiniTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.material = {"handoff_text":"WHOLE_HANDOFF_ORIGINAL\n" + "source φ, quotation \"x\". " * 3500 + "\n",
            "stage_instructions":dict(STAGE_INSTRUCTIONS),"system_message":SYSTEM_MESSAGE,"max_tokens":2048}

    def test_one_actual_episode_common_handoff_exact_locate_and_no_promotion(self):
        provider = ProseProvider()
        result = run_successor(provider,self.root,**self.material)
        self.assertEqual(result["status"],"COMPLETE",result["alarms"])
        self.assertEqual(result["mini_outcome"]["calls"],2)
        self.assertEqual(result["mini_outcome"]["cycles_completed"],1)
        self.assertEqual([row["stage"] for row in result["history"]],list(STAGES))
        history = []
        for request,row in zip(provider.requests,result["history"]):
            self.assertFalse(request["json_output"])
            self.assertEqual(request["messages"][0],{"role":"system","content":SYSTEM_MESSAGE})
            self.assertEqual(request["messages"][1]["content"],stage_prompt(self.material,row["stage"],history))
            self.assertIn(self.material["handoff_text"],request["messages"][1]["content"])
            self.assertEqual(row["text"],row["answer"]["body"])
            self.assertEqual(row["text"],row["answer"]["commitments"])
            self.assertFalse(row["proposed_changes_installed"])
            history.append(row)
        self.assertFalse(result["automatic_successor_started"])
        self.assertEqual(result["standing_effect"],"none")
        self.assertTrue(result["terminal_kind"]["transport_only"])
        route = json.loads((self.root/"requests/001-discriminate.json").read_text())
        self.assertEqual(route["source_fields_visible"],["handoff_text"])
        self.assertEqual(route["history_stages_visible"],["locate"])
        self.assertTrue(route["whole_handoff_port_visible"])
        self.assertTrue(route["actual_locate_port_visible"])
        self.assertIn(result["history"][0]["text"],route["mini_brief"])
        manifest = json.loads((self.root/"manifest.json").read_text())
        self.assertEqual(manifest["cycles"]["max_cycles"],1)
        self.assertEqual(manifest["cycles"]["max_calls"],2)
        self.assertEqual(next(s for s in manifest["stages"] if s["stage_id"] == "discriminate")["ports"],["handoff","actual_locate"])
        events = [json.loads(line) for line in (self.root/"run/log.jsonl").read_text().splitlines()]
        artifacts = [e for e in events if e["type"] == "ARTIFACT_SUBMITTED"]
        self.assertEqual(len(artifacts),3)
        self.assertTrue(all(e["payload"]["about"] == [] and e["payload"]["answers"] == [] for e in artifacts))

    def test_runtime_mutations_fail_before_dispatch(self):
        prepared = prepare_successor(self.root/"prepared",**self.material)
        mutations = {
            "ports":replace(prepared.plan,stages=tuple(replace(stage,ports=stage.ports+("handoff",)) if stage.stage_id == "discriminate" else stage for stage in prepared.plan.stages)),
            "source":replace(prepared.plan,sources=(replace(prepared.plan.sources[0],raw=b"changed"),)),
            "bounds":replace(prepared.plan,cycles=replace(prepared.plan.cycles,max_cycles=2)),
            "format":replace(prepared.plan,formats={}),
            "header":replace(prepared.plan,header={**prepared.plan.header,"problem":"changed"}),
        }
        for name,plan in mutations.items():
            with self.subTest(name=name):
                provider = ProseProvider()
                result = run_successor(provider,self.root/name,replace(prepared,plan=plan),**self.material)
                self.assertEqual(result["status"],"OPERATIONAL_FAILURE")
                self.assertEqual(provider.requests,[])
                self.assertIn("SUCCESSOR_PREPARED_PLAN_MISMATCH",{a["code"] for a in result["alarms"]})

    def test_second_request_failure_preserves_actual_first_output_and_refuses_rerun(self):
        provider = ProseProvider("discriminate")
        result = run_successor(provider,self.root,**self.material)
        self.assertEqual(result["status"],"OPERATIONAL_FAILURE")
        self.assertEqual(len(provider.requests),2)
        self.assertEqual([r["stage"] for r in result["history"]],["locate"])
        self.assertIsNone(result["final"])
        before = {str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        with self.assertRaises(FileExistsError):
            run_successor(provider,self.root,**self.material)
        self.assertEqual(before,{str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        self.assertEqual(len(provider.requests),2)

    def test_changed_route_is_rejected_before_second_dispatch(self):
        from creib.forge.mini.runner import render_brief as original
        def contaminated(plan,state,blobs,stage,cycle=0):
            brief,exposed = original(plan,state,blobs,stage,cycle)
            if stage.stage_id == "discriminate":
                brief += "\n\nEXTRA SOURCE: select the alleged best problem."
            return brief,exposed
        provider = ProseProvider()
        with mock.patch("creib.forge.mini.runner.render_brief",side_effect=contaminated):
            result = run_successor(provider,self.root,**self.material)
        self.assertEqual(result["status"],"OPERATIONAL_FAILURE")
        self.assertEqual(len(provider.requests),1)
        self.assertEqual([r["stage"] for r in result["history"]],["locate"])
        self.assertIn("SUCCESSOR_ROUTING_MISMATCH",{a["code"] for a in result["alarms"]})

    def test_prepared_reuse_needs_no_recompile_and_rejects_changed_material(self):
        prepared = prepare_successor(self.root,**self.material)
        with mock.patch("minireason.successor_mini.compile_manifest",side_effect=AssertionError("unexpected recompile")):
            result = run_successor(ProseProvider(),self.root,prepared,**self.material)
        self.assertEqual(result["status"],"COMPLETE",result["alarms"])
        provider = ProseProvider()
        result = run_successor(provider,self.root/"changed",prepared,**{**self.material,"handoff_text":self.material["handoff_text"]+"changed"})
        self.assertEqual(result["status"],"OPERATIONAL_FAILURE")
        self.assertEqual(provider.requests,[])


if __name__ == "__main__":
    unittest.main()
