"""Actual A-to-B offline flow; scripted provider prose is no research finding."""
from copy import deepcopy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from minireason.inquiry_study import freeze_occurrence, make_plan as make_a, run_test as run_a
from minireason.provider import digest, write_new
from minireason.successor_data import BASELINE_INSTRUCTION
from minireason.successor_study import (ARMS, STAGES, _signed, _verify, make_plan,
    run_test, stage_prompt, successor_source_identity)
from minireason.template_chain import freeze_handoff, make_chain_plan
from test_template_chain import RecordedFake, checkpoint, git

BASE = Path(__file__).resolve().parents[1]
B_OUTPUTS = {"locate":" The suggested defect is uncertain: λ.\n",
    "discriminate":"No distinct successor is justified; the proposed observation has not been executed.\n???\n",
    "followup":"No distinct successor is justified after considering the live accounts.\n"}


class FollowupFake:
    def __init__(self,settings,root,*,failure_stage=None,usage=None):
        self.settings,self.root = settings,root
        self.calls=self.prompt_tokens=self.completion_tokens=0
        self.failure_stage,self.usage=failure_stage,usage

    def complete(self,messages,*,json_output,coordinate):
        self.calls+=1
        self.prompt_tokens+=7
        self.completion_tokens+=5
        request={"messages":messages,"json_output":json_output,"coordinate":coordinate,"settings":self.settings.to_dict()}
        write_new(self.root/f"call-{self.calls:04d}.request.json",request)
        if coordinate["stage"]==self.failure_stage:
            raise RuntimeError("DELIBERATE_DISCRIMINATION_DELIVERY_FAILURE")
        response={"content":B_OUTPUTS[coordinate["stage"]],"finish_reason":"stop","status":"COMPLETE",
            "usage":{"prompt_tokens":7,"completion_tokens":5} if self.usage is None else self.usage}
        write_new(self.root/f"call-{self.calls:04d}.response.json",response)
        return response


class SuccessorStudyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temp=tempfile.TemporaryDirectory()
        cls.addClassCleanup(temp.cleanup)
        cls.parent=Path(temp.name)/"parent"
        cls.parent.mkdir()
        packet=json.loads((BASE/"experiments/records/E004-paired-languages/packet.json").read_text())
        issue=freeze_occurrence("What, if anything, survives? λ\n",{"source":"OFFLINE-FIXTURE"},packet["packet_id"])
        a=make_a("OFFLINE-A",packet,issue,"prose","Instrument fixture only.",arms=["mini"])
        chain=make_chain_plan("OFFLINE-CHAIN",a,"OFFLINE-B","Examine the actual unresolved occurrence.")
        write_new(cls.parent/"plan.json",a)
        write_new(cls.parent/"chain.json",chain)
        summary=run_a(cls.parent/"plan.json",cls.parent/"record",provider_factory=RecordedFake)
        if summary["arms"][0]["status"]!="OBSERVATIONS_RECORDED":
            raise AssertionError(summary)
        git(cls.parent,"init","-q")
        cls.handoff=freeze_handoff(cls.parent/"chain.json",cls.parent/"record",cls.parent,checkpoint(cls.parent))

    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)

    def plan(self):
        return make_plan("OFFLINE-B",self.handoff,self.handoff["chain_plan"]["allocation_reason"])

    def run_plan(self,plan,*,factory=FollowupFake,folder="run"):
        path=self.root/(folder+"-plan.json")
        write_new(path,plan)
        return run_test(path,self.root/folder,provider_factory=factory),self.root/folder

    def test_six_arms_share_one_real_a_handoff_and_matched_conditional_parity(self):
        from minireason.successor_mini import compile_manifest
        plan=self.plan()
        self.assertIn(self.handoff["material"]["packet_text"],plan["handoff_text"])
        with patch("minireason.successor_mini.compile_manifest",wraps=compile_manifest) as compiler:
            summary,root=self.run_plan(plan)
        self.assertEqual(compiler.call_count,1)
        self.assertTrue(all(a["status"]=="OBSERVATIONS_RECORDED" for a in summary["arms"]),summary)
        self.assertEqual(sum(a["resources"]["calls"] for a in summary["arms"]),10)
        self.assertFalse(summary["automatic_successor_started"])
        for arm in ARMS:
            result=json.loads((root/f"{arm}-r01/result.json").read_text())
            expected=["followup"] if arm in {"bare","native"} else list(STAGES)
            self.assertEqual([r["stage"] for r in result["history"]],expected)
            self.assertEqual([r["text"] for r in result["history"]],[B_OUTPUTS[s] for s in expected])
            self.assertEqual(result["handoff_id"],plan["handoff_id"])
            self.assertEqual(result["standing_effect"],"none")
            self.assertFalse(result["automatic_successor_started"])
            for index,row in enumerate(result["history"],1):
                _verify(row,"occurrence_id")
                request=json.loads((root/f"{arm}-r01/calls/call-{index:04d}.request.json").read_text())
                self.assertFalse(request["json_output"])
                self.assertIn(plan["handoff_text"],request["messages"][1]["content"])
                self.assertEqual(row["origin"]["prompt_sha256"],hashlib.sha256(request["messages"][1]["content"].encode()).hexdigest())
            if arm in {"bare","native"}:
                self.assertTrue(request["messages"][1]["content"].startswith(BASELINE_INSTRUCTION))
                self.assertIn("distinguishes the live accounts",request["messages"][1]["content"])
                self.assertIn("no further problem is presently warranted",request["messages"][1]["content"])
            else:
                for index in (1,2):
                    actual=json.loads((root/f"{arm}-r01/calls/call-{index:04d}.request.json").read_text())
                    comparator="matched_native" if arm.endswith("native") else "matched"
                    control=json.loads((root/f"{comparator}-r01/calls/call-{index:04d}.request.json").read_text())
                    self.assertEqual(actual["messages"],control["messages"])
                    self.assertEqual(actual["settings"],control["settings"])
                self.assertEqual(result["history"][1]["origin"]["supplied_input_occurrence_ids"],
                    [plan["handoff_id"],result["history"][0]["occurrence_id"]])
        a_manifest=json.loads((self.parent/"record/mini-r01/manifest.json").read_text())
        b_manifest=json.loads((root/"mini-r01/manifest.json").read_text())
        self.assertEqual(a_manifest["cycles"]["max_cycles"],1)
        self.assertEqual(b_manifest["cycles"]["max_cycles"],1)
        a_log=json.loads((self.parent/"record/mini-r01/run/log.jsonl").read_text().splitlines()[0])
        b_log=json.loads((root/"mini-r01/run/log.jsonl").read_text().splitlines()[0])
        self.assertNotEqual(a_log["event_id"],b_log["event_id"])

    def test_second_call_failure_keeps_b_locate_and_every_original_a_byte(self):
        before={str(p.relative_to(self.parent)):p.read_bytes() for p in (self.parent/"record").rglob("*") if p.is_file()}
        _,root=self.run_plan(self.plan(),factory=lambda settings,path:FollowupFake(settings,path,failure_stage="discriminate"))
        for arm in ("matched","matched_native","mini","mini_native"):
            result=json.loads((root/f"{arm}-r01/result.json").read_text())
            self.assertEqual(result["status"],"OPERATIONAL_FAILURE")
            self.assertEqual(result["resources"]["calls"],2)
            self.assertEqual([r["stage"] for r in result["history"]],["locate"])
            self.assertEqual(result["history"][0]["text"],B_OUTPUTS["locate"])
            self.assertFalse((root/f"{arm}-r01/discriminate.artifact.json").exists())
        self.assertEqual(before,{str(p.relative_to(self.parent)):p.read_bytes() for p in (self.parent/"record").rglob("*") if p.is_file()})
        with self.assertRaises(FileExistsError):
            run_test(self.root/"run-plan.json",root,provider_factory=FollowupFake)

    def test_resigned_handoff_or_derived_plan_mutations_block_before_provider_creation(self):
        for index,field in enumerate(("handoff_text","stage_instructions","baseline_instruction","handoff")):
            plan=self.plan()
            if field=="handoff":
                plan[field]["material"]["occurrences"][0]["text"]+="changed"
                plan[field]=_signed({k:v for k,v in plan[field].items() if k!="handoff_id"},"handoff_id")
            elif field=="stage_instructions":
                plan[field]["discriminate"]="Force another problem."
            else:
                plan[field]+="changed"
            plan=_signed({k:v for k,v in plan.items() if k!="plan_id"},"plan_id")
            with patch("minireason.successor_study.DeepSeek") as factory:
                summary,_=self.run_plan(plan,factory=factory,folder="changed"+str(index))
            factory.assert_not_called()
            self.assertEqual(summary["preflight"]["status"],"CONFIGURATION_PREFLIGHT_FAILED")
            self.assertTrue(all(r["resources"]["calls"]==0 for r in summary["arms"]))

    def test_plan_freeze_rejects_output_conditioned_settings_arm_or_allocation_changes(self):
        args=("OFFLINE-B",self.handoff,self.handoff["chain_plan"]["allocation_reason"])
        for kwargs in ({"arms":["mini"]},{"settings":replace(__import__("minireason.provider",fromlist=["Settings"]).Settings(),max_tokens=1)}):
            with self.assertRaises(ValueError):
                make_plan(*args,**kwargs)
        with self.assertRaisesRegex(ValueError,"PREDECLARED_ALLOCATION"):
            make_plan("OFFLINE-B",self.handoff,"Choose the apparently best answer.")
        copied=deepcopy(self.handoff)
        plan=make_plan("OFFLINE-B",copied,args[2])
        copied["material"]["occurrences"][0]["text"]+="later mutation"
        self.assertNotEqual(copied["material"],plan["handoff"]["material"])

    def test_source_drift_and_provider_setting_drift_are_operational_failures(self):
        plan=self.plan()
        current=successor_source_identity()
        changed=deepcopy(current)
        changed["probe_modules"]["successor_study.py"]="0"*64
        with patch("minireason.successor_study.successor_source_identity",return_value=changed),patch("minireason.successor_study.DeepSeek") as factory:
            summary,_=self.run_plan(plan,factory=factory,folder="source-drift")
        factory.assert_not_called()
        self.assertEqual(summary["preflight"]["status"],"CONFIGURATION_PREFLIGHT_FAILED")
        summary,_=self.run_plan(plan,folder="provider-drift",factory=lambda settings,path:FollowupFake(replace(settings,thinking=not settings.thinking),path))
        self.assertTrue(all(r["status"]=="OPERATIONAL_FAILURE" and r["resources"]["calls"]==0 for r in summary["arms"]))

    def test_exact_stage_history_and_completion_usage_required(self):
        plan=self.plan()
        for history in ([],[{"stage":"locate","text":"x"},{"stage":"locate","text":"y"}]):
            with self.assertRaisesRegex(ValueError,"EXACT_LOCATE_HISTORY"):
                stage_prompt(plan,"discriminate",history)
        with self.assertRaisesRegex(ValueError,"INITIAL_HISTORY_FORBIDDEN"):
            stage_prompt(plan,"followup",[{"stage":"locate","text":"unavailable"}])
        summary,root=self.run_plan(plan,factory=lambda settings,path:FollowupFake(settings,path,usage={}))
        self.assertTrue(all(r["status"]=="OPERATIONAL_FAILURE" and r["resources"]["calls"]==1 for r in summary["arms"]))
        self.assertTrue(all(json.loads((root/f"{arm}-r01/result.json").read_text())["history"]==[] for arm in ARMS))


if __name__ == "__main__":
    unittest.main()
