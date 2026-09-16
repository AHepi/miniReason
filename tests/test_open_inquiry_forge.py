"""Actual Forge integration checks; scripted replies are not reasoning evidence."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from creib.forge.mini.executor import Reply
from creib.forge.mini.manifest import compile_manifest
from minireason.open_inquiry import (
    ExecutionEnvelope, MATERIAL_KIND, ROLES, TEMPLATES, install_source_bridge,
    make_manifest, run_open_inquiry, write_bundle,
)


class RecordingResponder:
    def __init__(self, completion_cap=None):
        self.seen = []
        self.completion_cap = completion_cap

    def reply(self, request):
        self.seen.append(request)
        text = f"PUBLIC-{request.stage_id}-CYCLE-{request.cycle}: ◇? is still undefined; this framing may be mistaken. STOP is prose, not host control."
        return Reply(text=text, prompt_tokens=23, completion_tokens=7)


class ForgeIntegration(unittest.TestCase):
    def setUp(self):
        install_source_bridge()

    def test_all_four_manifests_compile_and_route_two_cycles(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            paths = write_bundle(b"Something is missing, but I cannot name it.", base / "bundle", ExecutionEnvelope(2))
            for name, path in zip(TEMPLATES, paths):
                with self.subTest(template=name):
                    plan = compile_manifest(path)
                    self.assertTrue(all(f.freeform for f in plan.formats.values()))
                    responder = RecordingResponder()
                    outcome = run_open_inquiry(plan, base / ("run-" + name), responder, responder_id="offline scripted test")
                    self.assertEqual(outcome.cycles_completed, 2)
                    self.assertEqual(outcome.stop_reason, "cycle_cap")
                    expected = (len(ROLES[name]) + 1) * 2
                    self.assertEqual(len(responder.seen), expected)
                    self.assertEqual(outcome.calls, expected)
                    second = next(r for r in responder.seen if r.cycle == 2)
                    self.assertIn("PUBLIC-continue-CYCLE-1", second.brief)
                    self.assertIn("◇? is still undefined", second.brief)

    def test_full_text_after_excerpt_and_problem_field_bounds_is_visible(self):
        text = "Unsettled material. " * 900 + "TAIL-QUALIFIER-DO-NOT-OMIT\r\nMāori ∀ ◇?"
        raw = text.encode("utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = write_bundle(raw, root / "bundle", ExecutionEnvelope(1))[0]
            responder = RecordingResponder()
            run_open_inquiry(compile_manifest(path), root / "run", responder, responder_id="offline source test")
            self.assertIn(text, responder.seen[0].brief)
            self.assertIn("TAIL-QUALIFIER-DO-NOT-OMIT", responder.seen[0].brief)

    def test_blank_opening_is_not_rejected_as_an_ill_defined_problem(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = write_bundle(b"", root / "bundle", ExecutionEnvelope(1))[0]
            responder = RecordingResponder()
            outcome = run_open_inquiry(compile_manifest(path), root / "run", responder, responder_id="offline blank source test")
            self.assertEqual(outcome.calls, 2)

    def test_no_source_is_also_admissible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "manifest.json"
            path.write_text(json.dumps(make_manifest("open_turn", [], ExecutionEnvelope(1))))
            responder = RecordingResponder()
            outcome = run_open_inquiry(compile_manifest(path), root / "run", responder, responder_id="offline no-source test")
            self.assertEqual(outcome.calls, 2)
            self.assertIn("unspecified problem is not a semantic failure", responder.seen[0].brief)

    def test_blind_reader_receives_only_current_encoding_not_source_or_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = write_bundle(b"WITHHELD-SOURCE-SENTINEL-8732", root / "bundle", ExecutionEnvelope(2))
            responder = RecordingResponder()
            run_open_inquiry(compile_manifest(paths[3]), root / "run", responder, responder_id="offline isolation test")
            readers = [r for r in responder.seen if r.stage_id == "read"]
            self.assertEqual(len(readers), 2)
            for request in readers:
                self.assertNotIn("WITHHELD-SOURCE-SENTINEL-8732", request.brief)
                self.assertIn(f"PUBLIC-encode-CYCLE-{request.cycle}", request.brief)
                self.assertNotIn("PUBLIC-continue-CYCLE-1", request.brief)
                self.assertNotIn("PUBLIC-compare-CYCLE-1", request.brief)
            self.assertNotIn("PUBLIC-encode-CYCLE-1", readers[1].brief)
            self.assertIn("WITHHELD-SOURCE-SENTINEL-8732", next(r for r in responder.seen if r.stage_id == "compare").brief)

    def test_explicit_route_away_from_intake_is_not_bypassed_by_source_bridge(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = write_bundle(b"MUST-NOT-LEAK-THIS-SOURCE", root / "bundle", ExecutionEnvelope(1))[0]
            manifest = json.loads(path.read_text())
            manifest["routing"] = {"evidence": [{"from_tier": "evidence", "to": {"target": "port_type", "port_type": "evidence_legend"}}]}
            path.write_text(json.dumps(manifest))
            responder = RecordingResponder()
            run_open_inquiry(compile_manifest(path), root / "run", responder, responder_id="offline route isolation test")
            self.assertNotIn("MUST-NOT-LEAK-THIS-SOURCE", responder.seen[0].brief)

    def test_model_stop_text_cannot_override_call_budget_or_create_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = write_bundle(b"Open concern", root / "bundle", ExecutionEnvelope(3, 1, 100, 100))[1]
            responder = RecordingResponder(completion_cap=100)
            outcome = run_open_inquiry(compile_manifest(path), root / "run", responder, responder_id="offline resource boundary test")
            self.assertEqual(len(responder.seen), 1)
            self.assertEqual(outcome.calls, 1)
            self.assertIn("budget", outcome.stop_reason)
            self.assertNotIn("solved", outcome.stop_reason)


if __name__ == "__main__":
    unittest.main()
