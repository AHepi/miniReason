import json
from pathlib import Path
import tempfile
import unittest

from creib.forge.mini.executor import ScriptedResponder
from creib.forge.mini.manifest import compile_manifest
from creib.forge.mini.runner import run_mini
from minireason.templates import TEMPLATES, manifest_for, register_task_seats


class TemplateTests(unittest.TestCase):
    def test_all_original_templates_compile_and_run_with_actual_machine_feedback(self):
        register_task_seats()
        for template_id in TEMPLATES:
            with self.subTest(template=template_id), tempfile.TemporaryDirectory() as temp:
                base = Path(temp)
                path = base / "manifest.json"
                path.write_text(json.dumps(manifest_for(template_id=template_id)))
                plan = compile_manifest(path)
                script = {"conjecture": [json.dumps({"body": "A proposed empty result.", "commitments": "[]"})],
                          "criticise": [json.dumps({"body": "Unused stock must still be returned.", "commitments": "Preserve empty stock behavior."})],
                          "revise": [json.dumps({"body": "No valid repair demonstrated.", "commitments": "[]"})]}
                responder = ScriptedResponder(script)
                outcome = run_mini(plan, base / "run", responder, "calibration")
                self.assertEqual(outcome.cycles_completed, 1)
                self.assertIn("execute", outcome.stages_entered)
                self.assertIn("revise", outcome.stages_entered)
                self.assertTrue(all(not key.endswith("#commitments") for key in responder.used))

    def test_control_withholds_feedback_and_return_path_at_active_stage_ports(self):
        manifest = manifest_for(feedback=False, return_path=False)
        stages = {s["stage_id"]: s for s in manifest["stages"]}
        self.assertNotIn("execute", stages)
        self.assertNotIn("observations", stages["criticise"]["ports"])
        self.assertNotIn("criticism", stages["revise"]["ports"])
        self.assertNotIn("observations", stages["revise"]["ports"])

    def test_invalid_submission_ends_loudly_without_spending_hidden_repair_calls(self):
        register_task_seats()
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            manifest = manifest_for(completion_tokens_per_call=100)
            self.assertEqual(manifest["cycles"]["max_calls"], 3)
            self.assertEqual(manifest["cycles"]["max_completion_tokens"], 300)
            path = base / "manifest.json"
            path.write_text(json.dumps(manifest))
            plan = compile_manifest(path)
            responder = ScriptedResponder({"conjecture": ["not JSON"]}, completion_cap=100)
            result = run_mini(plan, base / "run", responder, "invalid-control")
            self.assertEqual(sum(responder.used.values()), 1)
            self.assertEqual(result.cycles_completed, 0)
            self.assertNotIn("revise", result.stages_entered)
            self.assertIn("FORMAT_FAILURE", (base / "run" / "log.jsonl").read_text())


if __name__ == "__main__":
    unittest.main()
