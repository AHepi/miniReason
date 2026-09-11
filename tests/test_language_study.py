import json
import hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from minireason.language_study import (_signed, make_preparation_plan, make_probe_plan,
    run_preparation, run_probe_test, stage_prompt)
from minireason.provider import write_new


class FakeProvider:
    def __init__(self, settings, root, responses):
        self.settings, self.root = settings, root
        self.responses = list(responses)
        self.calls = self.prompt_tokens = self.completion_tokens = 0

    def complete(self, messages, *, json_output=True, coordinate=None):
        self.calls += 1
        self.prompt_tokens += 10
        self.completion_tokens += 5
        text = self.responses.pop(0)
        answer = {"content": text, "usage": {"prompt_tokens": 10, "completion_tokens": 5},
                  "status": "COMPLETE", "finish_reason": "stop"}
        write_new(self.root / f"call-{self.calls:04d}.request.json", {"messages": messages, "json_output": json_output})
        write_new(self.root / f"call-{self.calls:04d}.response.json", answer)
        return answer


def corpus():
    return _signed({"schema": "minireason.language-corpus.v1", "text": "PRIVATE_SOURCE_SENTENCE",
                    "problem": "Fixture problem", "model": "test", "origin_plan_id": "fixture"}, "corpus_id")


def packet():
    return _signed({"schema": "minireason.language-packet.v1", "corpus": corpus(),
                    "languages": {"lean": "LEAN_ONLY_MEANING", "nonlean": "NONLEAN_ONLY_MEANING"},
                    "origin_plan_id": "fixture", "model": "test", "status": "FROZEN_UNADJUDICATED"}, "packet_id")


class LanguageStudyTests(unittest.TestCase):
    def test_reinterpretation_omits_corpus_and_nonselected_language(self):
        plan = make_probe_plan("fixture", packet(), "lean_candidate", "Test source masking")
        prompt = stage_prompt(plan, "reinterpret", [{"stage": "express", "text": "EXPRESSION_BYTES"}])
        self.assertIn("LEAN_ONLY_MEANING", prompt)
        self.assertIn("EXPRESSION_BYTES", prompt)
        self.assertNotIn("PRIVATE_SOURCE_SENTENCE", prompt)
        self.assertNotIn("NONLEAN_ONLY_MEANING", prompt)
        self.assertNotIn(plan["packet_id"], prompt)

    def test_expression_prose_escape_is_retained_without_automatic_language_credit(self):
        plan = make_probe_plan("fixture", packet(), "lean_candidate", "Test escaped criticism")
        escaped = "PROSE-ESCAPE: PRIVATE_SOURCE_SENTENCE cannot be expressed here."
        prompt = stage_prompt(plan, "reinterpret", [{"stage": "express", "text": escaped}])
        self.assertIn(escaped, prompt)
        self.assertIn("does not establish", prompt)

    def test_frozen_corpus_precedes_language_setup_and_raw_invalid_packet_survives(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cp = make_preparation_plan("C0", "corpus")
            write_new(root / "corpus-plan.json", cp)
            result = run_preparation(root / "corpus-plan.json", root / "corpus-run",
                       provider_factory=lambda settings, path: FakeProvider(settings, path, ["An uncertain original conjecture."]))
            self.assertEqual(result["status"], "PREPARATION_RECORDED")
            frozen = json.loads((root / "corpus-run/corpus.json").read_text())
            lp = make_preparation_plan("L0", "languages", corpus=frozen)
            self.assertIn(frozen["text"], lp["prompt"])
            write_new(root / "languages-plan.json", lp)
            result = run_preparation(root / "languages-plan.json", root / "languages-run",
                       provider_factory=lambda settings, path: FakeProvider(settings, path, ["Substantive prose, but no paired envelope."]))
            self.assertEqual(result["status"], "PREPARATION_INCOMPLETE")
            self.assertEqual(result["resources"]["calls"], 1)
            self.assertIn("Substantive prose", (root / "languages-run/raw-artifact.json").read_text())
            self.assertFalse((root / "languages-run/packet.json").exists())

    def test_direct_probe_records_arbitrary_prose_and_uses_no_json_response_gate(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plan = make_probe_plan("probe", packet(), "nonlean_candidate", "Probe original language", arms=["matched"])
            write_new(root / "plan.json", plan)
            summary = run_probe_test(root / "plan.json", root / "run", jobs=1,
                        provider_factory=lambda settings, path: FakeProvider(settings, path,
                          ["A proposed expression without JSON.", "An unresolved reading.", "A prose objection to the language."]))
            row = summary["arms"][0]
            self.assertEqual(row["status"], "OBSERVATIONS_RECORDED")
            self.assertEqual(row["resources"]["calls"], 3)
            result = json.loads((root / "run/matched-r01/result.json").read_text())
            self.assertEqual([r["stage"] for r in result["history"]], ["express", "reinterpret", "criticize"])
            request = json.loads((root / "run/matched-r01/calls/call-0002.request.json").read_text())
            self.assertFalse(request["json_output"])
            self.assertNotIn("PRIVATE_SOURCE_SENTENCE", request["messages"][1]["content"])

    def test_tampered_packet_and_invalid_concurrency_refused_before_calls(self):
        damaged = packet()
        damaged["languages"]["lean"] = "CHANGED"
        with self.assertRaisesRegex(ValueError, "FROZEN_IDENTITY_CHANGED"):
            make_probe_plan("broken", damaged, "prose", "No mutation")
        with self.assertRaisesRegex(ValueError, "CONCURRENCY"):
            run_probe_test(Path("does-not-exist"), Path("unused"), jobs=6)

    def test_one_shot_control_has_one_call_and_preserves_frozen_packet(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plan = make_probe_plan("single", packet(), "prose", "Practical control", arms=["bare"])
            write_new(root / "plan.json", plan)
            summary = run_probe_test(root / "plan.json", root / "run", jobs=1,
                        provider_factory=lambda settings, path: FakeProvider(settings, path, ["Unconstrained expression."]))
            self.assertEqual(summary["arms"][0]["resources"]["calls"], 1)
            stored = json.loads((root / "run/packet.json").read_text())
            self.assertEqual(stored["packet_id"], plan["packet_id"])

    def test_late_provider_failure_keeps_completed_direct_artifacts_in_result(self):
        class FailsLater(FakeProvider):
            def complete(self, *args, **kwargs):
                if self.calls == 1:
                    self.calls += 1
                    raise RuntimeError("injected late provider failure")
                return super().complete(*args, **kwargs)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plan = make_probe_plan("partial", packet(), "prose", "Preserve partial evidence", arms=["matched"])
            write_new(root / "plan.json", plan)
            run_probe_test(root / "plan.json", root / "run", jobs=1,
                provider_factory=lambda settings, path: FailsLater(settings, path, ["Completed expression survives."]))
            result = json.loads((root / "run/matched-r01/result.json").read_text())
            self.assertEqual(result["status"], "OPERATIONAL_FAILURE")
            self.assertEqual(result["history"][0]["text"], "Completed expression survives.")
            self.assertEqual(len(result["history"]), 1)
            self.assertTrue((root / "run/matched-r01/express.artifact.json").is_file())

    def test_real_mini_uses_same_outgoing_requests_and_preserves_raw_prose(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plan = make_probe_plan("parity", packet(), "lean_candidate", "Calibrate actual Mini routing",
                                   arms=["matched", "mini"])
            write_new(root / "plan.json", plan)
            output = ["PROSE-ESCAPE: the language cannot carry this objection.",
                      "The reading remains unresolved.", "The escape must remain a legitimate criticism."]
            summary = run_probe_test(root / "plan.json", root / "run", jobs=1,
                        provider_factory=lambda settings, path: FakeProvider(settings, path, output))
            self.assertTrue(all(row["status"] == "OBSERVATIONS_RECORDED" for row in summary["arms"]))
            for index in range(1, 4):
                name = f"calls/call-{index:04d}.request.json"
                direct = json.loads((root / "run/matched-r01" / name).read_text())
                mini = json.loads((root / "run/mini-r01" / name).read_text())
                self.assertEqual(direct["messages"], mini["messages"])
                self.assertFalse(mini["json_output"])
            result = json.loads((root / "run/mini-r01/result.json").read_text())
            direct_result = json.loads((root / "run/matched-r01/result.json").read_text())
            self.assertEqual(result["schema"], "minireason.language-arm.v1")
            self.assertIn("route_schema", result)
            self.assertEqual([row["text"] for row in result["history"]], output)
            self.assertEqual([row["text_sha256"] for row in result["history"]],
                             [row["text_sha256"] for row in direct_result["history"]])
            self.assertEqual(result["mini_outcome"]["cycles_completed"], 1)
            self.assertEqual(result["resources"]["calls"], 3)
            self.assertTrue((root / "run/mini-r01/run/log.jsonl").is_file())

    def test_failed_actual_manifest_preflight_blocks_every_provider_and_records_cause(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plan = make_probe_plan("bad-material", packet(), "prose", "Record a configuration failure",
                                   arms=["bare", "mini", "matched_native"])
            plan["stage_instructions"]["express"] = "Oversized original instruction. " * 200
            plan = _signed({key: value for key, value in plan.items() if key != "plan_id"}, "plan_id")
            write_new(root / "plan.json", plan)
            with patch("minireason.language_study.DeepSeek") as unused:
                summary = run_probe_test(root / "plan.json", root / "run", provider_factory=unused)
            unused.assert_not_called()
            self.assertEqual(summary["preflight"]["status"], "CONFIGURATION_PREFLIGHT_FAILED")
            self.assertEqual(summary["interpretation_status"], "NOT_RUN_CONFIGURATION_FAILURE")
            self.assertTrue(all(row["resources"]["calls"] == 0 for row in summary["arms"]))
            self.assertTrue(all(row["status"] == "CONFIGURATION_PREFLIGHT_FAILED" for row in summary["arms"]))
            self.assertIn("MINI_MANIFEST_INVALID", (root / "run/errata.json").read_text())
            self.assertIn("before any provider", (root / "run/REPORT.md").read_text())
            for arm in plan["arms"]:
                self.assertTrue((root / f"run/{arm}-r01/result.json").is_file())

    def test_material_snapshot_mismatch_is_recorded_before_provider_construction(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plan = make_probe_plan("snapshot", packet(), "prose", "Bind exact source bytes", arms=["bare"])
            plan["material_snapshots"]["packet_text"]["sha256"] = "0" * 64
            plan = _signed({key: value for key, value in plan.items() if key != "plan_id"}, "plan_id")
            write_new(root / "plan.json", plan)
            with patch("minireason.language_study.DeepSeek") as unused:
                summary = run_probe_test(root / "plan.json", root / "run", provider_factory=unused)
            unused.assert_not_called()
            self.assertIn("MATERIAL_SNAPSHOT_MISMATCH", summary["preflight"]["alarms"][0]["detail"])
            self.assertTrue((root / "run/REPORT.md").is_file())

    def test_real_frozen_packet_all_carriers_preflight_once_and_route_losslessly(self):
        from minireason import language_mini
        packet_path = Path(__file__).resolve().parents[1] / "experiments/records/E004-paired-languages/packet.json"
        real_packet = json.loads(packet_path.read_text())
        output = ["Expression fixture with α and trailing newline.\n", "Source-text-withheld reading.\n",
                  "The criticism remains ordinary prose.\n"]
        for carrier in ("prose", "lean_candidate", "nonlean_candidate"):
            with self.subTest(carrier=carrier), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                plan = make_probe_plan("real-material", real_packet, carrier, "E005 size-boundary regression",
                                       arms=["matched", "mini", "mini_native"])
                self.assertGreater(len(plan["packet_text"]), 8192)
                if carrier != "prose":
                    self.assertGreater(len(plan["selected_language_text"]), 4000)
                raw = plan["packet_text"].encode("utf-8")
                self.assertEqual(plan["material_snapshots"]["packet_text"]["sha256"], hashlib.sha256(raw).hexdigest())
                self.assertEqual(plan["material_snapshots"]["packet_text"]["bytes"], len(raw))
                write_new(root / "plan.json", plan)
                def factory(settings, path):
                    recorded = json.loads((root / "run/preflight.json").read_text())
                    self.assertEqual(recorded["status"], "CONFIGURATION_PREFLIGHT_PASSED")
                    return FakeProvider(settings, path, output)
                with patch("minireason.language_mini.compile_manifest", wraps=language_mini.compile_manifest) as compile_once:
                    summary = run_probe_test(root / "plan.json", root / "run", jobs=3, provider_factory=factory)
                self.assertEqual(compile_once.call_count, 1)
                self.assertTrue(all(row["status"] == "OBSERVATIONS_RECORDED" for row in summary["arms"]), summary)
                for index in range(1, 4):
                    direct = json.loads((root / f"run/matched-r01/calls/call-{index:04d}.request.json").read_text())
                    for arm in ("mini", "mini_native"):
                        routed = json.loads((root / f"run/{arm}-r01/calls/call-{index:04d}.request.json").read_text())
                        self.assertEqual(direct["messages"], routed["messages"])
                bindings = summary["preflight"]["mini"]["sources"]
                self.assertTrue(any(row["sha256"] == hashlib.sha256(raw).hexdigest() for row in bindings))

    def test_concurrent_configurations_keep_their_material_and_language_routes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cases = []
            for index, carrier in enumerate(("lean_candidate", "nonlean_candidate")):
                frozen_corpus = _signed({"schema": "minireason.language-corpus.v1", "text": f"DISTINCT_SOURCE_{index}",
                    "problem": "Concurrency fixture", "model": "test", "origin_plan_id": "fixture"}, "corpus_id")
                frozen_packet = _signed({"schema": "minireason.language-packet.v1", "corpus": frozen_corpus,
                    "languages": {"lean": f"LEAN_MEANING_{index}", "nonlean": f"RELATIONAL_MEANING_{index}"},
                    "origin_plan_id": "fixture", "model": "test", "status": "FROZEN_UNADJUDICATED"}, "packet_id")
                plan = make_probe_plan(f"concurrent-{index}", frozen_packet, carrier, "Check per-plan source binding",
                                       arms=["matched", "mini"])
                folder = root / str(index)
                write_new(folder / "plan.json", plan)
                cases.append(folder)
            def run_case(folder):
                return run_probe_test(folder / "plan.json", folder / "run", jobs=2,
                    provider_factory=lambda settings, path: FakeProvider(settings, path,
                        [f"EXPRESSION_{folder.name}", f"READING_{folder.name}", f"CRITICISM_{folder.name}"]))
            with ThreadPoolExecutor(max_workers=2) as pool:
                summaries = list(pool.map(run_case, cases))
            self.assertTrue(all(row["status"] == "OBSERVATIONS_RECORDED" for summary in summaries for row in summary["arms"]))
            for index, folder in enumerate(cases):
                for step in range(1, 4):
                    direct = json.loads((folder / f"run/matched-r01/calls/call-{step:04d}.request.json").read_text())
                    routed = json.loads((folder / f"run/mini-r01/calls/call-{step:04d}.request.json").read_text())
                    self.assertEqual(direct["messages"], routed["messages"])
                    self.assertNotIn(f"DISTINCT_SOURCE_{1 - index}", routed["messages"][1]["content"])


if __name__ == "__main__":
    unittest.main()
