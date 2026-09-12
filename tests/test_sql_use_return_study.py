from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from minireason import sql_use_return_study as c
from minireason.provider import ProviderFailure

REPO = Path(c.__file__).resolve().parents[2]


class FakeProvider(c.OfflineProvider):
    instances = []
    fail_at = None
    after_response = None
    on_init = None

    def __init__(self, settings, records):
        super().__init__()
        self.settings, self.records = settings, records
        self.requests = []
        type(self).instances.append(self)
        if type(self).on_init:
            type(self).on_init()

    def complete(self, messages, *, json_output=True, coordinate=None):
        self.requests.append(copy.deepcopy({"messages": messages, "coordinate": coordinate}))
        if type(self).fail_at == self.calls + 1:
            self.calls += 1
            c.base.write_json(self.records / f"call-{self.calls:04d}.request.json", {"request": c.base.payload_for(messages, self.settings)})
            c.base.write_json(self.records / f"call-{self.calls:04d}.response.json", {"status": "SCRIPTED_OFFLINE_FAILURE"})
            raise ProviderFailure("INCOMPLETE_GENERATION", "Do not preserve untrusted exception detail")
        response = super().complete(messages, json_output=json_output, coordinate=coordinate)
        c.base.write_json(self.records / f"call-{self.calls:04d}.request.json", {"request": response["request"], "coordinate": coordinate})
        c.base.write_json(self.records / f"call-{self.calls:04d}.response.json", response)
        if type(self).after_response:
            type(self).after_response(self.calls)
        return response


class UseReturnTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.frozen, self.output = self.root / "frozen", self.root / "output"
        FakeProvider.instances = []
        FakeProvider.fail_at = FakeProvider.after_response = FakeProvider.on_init = None

    def tearDown(self):
        self.temp.cleanup()

    def prepare(self):
        with patch.object(c, "DeepSeek", side_effect=AssertionError("Offline provider instantiated")):
            return c.prepare(self.frozen, REPO)

    def run_fake(self, plan):
        with patch.object(c, "DeepSeek", FakeProvider):
            return c.run(self.frozen, self.output, REPO, plan["plan_id"])

    def test_actual_source_freeze_and_scripted_prefix_equality(self):
        plan = self.prepare()
        self.assertEqual(c.verify(self.frozen, REPO), plan)
        self.assertEqual((self.frozen / "selected-candidate.txt").read_bytes(),
            (REPO / "experiments/records/E027-sql-construction-continuation/mini-disabled/public-answer.txt").read_bytes())
        self.assertEqual(plan["candidate_sha256"], c.CANDIDATE_SHA256)
        self.assertEqual(c.base.sha((self.frozen / "system.txt").read_bytes()), plan["system_sha256"])
        self.assertEqual(plan["max_provider_calls"], 6)
        self.assertEqual(plan["max_aggregate_completion_tokens"], 49152)
        preflight = json.loads((self.frozen / "preflight.json").read_bytes())
        self.assertEqual(preflight["provider_calls"], 0)
        self.assertEqual(preflight["scripted_engine_calls"], 8)
        self.assertTrue(preflight["actual_prefix_requests_equal"])
        for stage in c.STAGES[:2]:
            paths = [self.frozen / "offline-probe" / arm / "routed" / (stage + ".json") for arm in c.ARMS]
            first, second = [json.loads(path.read_bytes()) for path in paths]
            self.assertEqual(first["request"], second["request"])
            self.assertEqual(first["mini_brief"], second["mini_brief"])

    def test_shared_actual_prefix_six_unique_calls_and_whole_prose(self):
        plan = self.prepare()
        summary = self.run_fake(plan)
        self.assertEqual(summary["status"], "COMPLETE")
        provider = FakeProvider.instances[0]
        self.assertEqual(provider.calls, 6)
        self.assertEqual(summary["provider_calls"], 6)
        self.assertEqual(summary["reused_prefix_responses"], 2)
        self.assertEqual(summary["recorded_successful_unique_usage"], {"prompt_tokens": 6, "completion_tokens": 6})
        self.assertEqual([request["coordinate"]["stage"] for request in provider.requests], list(c.STAGES) + list(c.STAGES[2:]))
        self.assertEqual([row["unique_provider_calls"] for row in summary["arms"]], [4, 2])
        for arm_row in summary["arms"]:
            self.assertEqual(arm_row["outcome"]["cycles_completed"], 1)
            self.assertEqual(arm_row["outcome"]["calls"], 4)
            self.assertEqual([row["stage"] for row in arm_row["custody"]], list(c.STAGES))
            for occurrence in arm_row["history"]:
                text = (self.output / arm_row["arm"] / (occurrence["stage"] + ".txt")).read_text()
                self.assertIn('π\n  Uncertainty remains.\n{"body":"quoted text only"}\n', text)
                self.assertEqual(occurrence["text_sha256"], c.base.sha(text.encode()))
        returned, archived = [row["history"] for row in summary["arms"]]
        for index in (0, 1):
            self.assertEqual(returned[index]["text_sha256"], archived[index]["text_sha256"])
            self.assertEqual(archived[index]["reuse_source_occurrence"], returned[index]["occurrence_id"])
            self.assertEqual(archived[index]["response_path"], returned[index]["response_path"])
            self.assertEqual(archived[index]["additional_provider_usage"], {"prompt_tokens": 0, "completion_tokens": 0})
        for history in (returned, archived):
            self.assertIn(history[0]["occurrence_id"], history[2]["parent_occurrences"])
            self.assertEqual(history[3]["parent_occurrences"], [history[2]["occurrence_id"]])

    def test_actual_requests_no_initialization_or_criticism_bypass(self):
        summary = self.run_fake(self.prepare())
        self.assertEqual(summary["status"], "COMPLETE")
        manifests = [json.loads((self.frozen / "manifests" / (arm + ".json")).read_bytes()) for arm in c.ARMS]
        apply_instructions = [next(kind["instruction"] for kind in value["kinds"] if kind["kind_id"] == c.KINDS["apply_return"]) for value in manifests]
        self.assertEqual(apply_instructions[0], apply_instructions[1])
        self.assertIn(json.dumps(c.BEFORE_EVENTS, ensure_ascii=False), apply_instructions[0])
        for arm in c.ARMS:
            raw = {stage: (self.output / arm / (stage + ".txt")).read_text() for stage in c.STAGES}
            routes = {stage: json.loads((self.output / arm / "routed" / (stage + ".json")).read_bytes()) for stage in c.STAGES}
            messages = {stage: json.dumps(routes[stage]["request"]["messages"], ensure_ascii=False) for stage in c.STAGES}
            self.assertEqual(routes["use_before"]["input_ports"], ["problem"])
            self.assertIn("Operator interpretation of candidate sections 2 and 3", messages["use_before"])
            for stage in c.STAGES[1:]:
                self.assertNotIn("Operator interpretation of candidate sections 2 and 3", messages[stage])
            self.assertIn(raw["use_before"], routes["apply_return"]["request"]["messages"][1]["content"])
            after = routes["use_after"]["request"]["messages"][1]["content"]
            self.assertIn(raw["apply_return"], after)
            self.assertNotIn(raw["use_before"], after)
            self.assertNotIn(raw["criticize_dependency"], after)
            self.assertEqual(routes["use_after"]["input_ports"], ["u1"])
            apply = routes["apply_return"]["request"]["messages"][1]["content"]
            if arm == c.ARMS[0]:
                self.assertIn(raw["criticize_dependency"], apply)
            else:
                self.assertNotIn(raw["criticize_dependency"], apply)
            self.assertEqual(routes["use_after"]["request"]["thinking"], {"type": "disabled"})
            self.assertNotIn("response_format", routes["use_after"]["request"])

    def test_each_operational_failure_is_fail_stop_no_retry(self):
        for fail_at in (1, 3, 5, 6):
            with self.subTest(fail_at=fail_at):
                self.frozen = self.root / f"frozen-{fail_at}"
                self.output = self.root / f"output-{fail_at}"
                FakeProvider.fail_at = fail_at
                result = self.run_fake(self.prepare())
                self.assertEqual(result["status"], "INTERRUPTED")
                self.assertEqual(result["provider_calls"], fail_at)
                self.assertEqual(result["arms"][-1]["error_code"], "INCOMPLETE_GENERATION")
                self.assertEqual(result["automatic_retries"], 0)
                self.assertFalse(result["automatic_successor_started"])
                self.assertTrue((self.output / "summary.json").exists())
                if fail_at < 5:
                    self.assertFalse((self.output / c.ARMS[1]).exists())

    def test_external_pin_and_overwrite_refuse_without_provider(self):
        plan = self.prepare()
        with patch.object(c, "DeepSeek", side_effect=AssertionError("Premature provider initialization")):
            with self.assertRaisesRegex(ValueError, "EXTERNALLY_PINNED_PLAN_ID_MISMATCH"):
                c.run(self.frozen, self.output, REPO, "wrong")
            self.assertFalse(self.output.exists())
            self.output.mkdir()
            (self.output / "sentinel").write_text("preserve")
            with self.assertRaises(FileExistsError):
                c.run(self.frozen, self.output, REPO, plan["plan_id"])
        self.assertEqual((self.output / "sentinel").read_text(), "preserve")
        with self.assertRaises(FileExistsError):
            self.prepare()

    def test_rehashed_contract_manifest_and_material_tampering(self):
        plan = self.prepare()
        for key, value in {"max_provider_calls": 8, "automatic_retries": 1,
                           "arms": list(reversed(c.ARMS)), "cycles_per_arm": 2,
                           "routing": {}, "initializer_sha256": "0" * 64}.items():
            with self.subTest(key=key):
                changed = copy.deepcopy(plan)
                changed[key] = value
                changed["plan_id"] = c.base.digest({key: value for key, value in changed.items() if key != "plan_id"})
                (self.frozen / "plan.json").write_bytes(c.base.encoded(changed))
                with self.assertRaises(ValueError):
                    c.verify(self.frozen, REPO)
        (self.frozen / "plan.json").write_bytes(c.base.encoded(plan))
        for name in ("selected-candidate.txt", "initializer.json", "participant-source.json", "system.txt", "manifests/criticism-archived.json"):
            path = self.frozen / name
            original = path.read_bytes()
            path.write_bytes(original + b" ")
            with self.assertRaises(ValueError):
                c.verify(self.frozen, REPO)
            path.write_bytes(original)

    def test_before_spend_reverification_stops_after_material_change(self):
        plan = self.prepare()
        def mutate(call):
            if call == 1:
                with (self.frozen / "selected-candidate.txt").open("a") as handle:
                    handle.write("changed")
        FakeProvider.after_response = mutate
        summary = self.run_fake(plan)
        self.assertEqual(summary["status"], "INTERRUPTED")
        self.assertEqual(summary["provider_calls"], 1)
        self.assertTrue((self.output / c.ARMS[0] / "use_before.txt").exists())

    def test_runtime_settings_mutation_refused_before_first_call(self):
        plan = self.prepare()
        FakeProvider.on_init = lambda: setattr(FakeProvider.instances[-1], "settings", c.Settings(thinking=True, reasoning_effort="low", max_tokens=c.CAP))
        result = self.run_fake(plan)
        self.assertEqual(result["status"], "INTERRUPTED")
        self.assertEqual(result["provider_calls"], 0)

    def test_route_suffix_coordinate_and_extra_port_refused(self):
        self.prepare()
        arm, stage = c.ARMS[0], c.STAGES[0]
        route = json.loads((self.frozen / "offline-probe" / arm / "routed" / (stage + ".json")).read_bytes())
        manifest = json.loads((self.frozen / "manifests" / (arm + ".json")).read_bytes())
        request = SimpleNamespace(stage_id=stage, kind_id=c.KINDS[stage], cycle=1, attempt=0,
                                  phase="both", optional_fields=(), brief=route["mini_brief"])
        c.routed_messages(request, manifest, arm, {}, (self.frozen / "system.txt").read_text())
        for field, value in (("phase", "body"), ("cycle", 2), ("attempt", 1), ("optional_fields", ("extra",)),
                             ("brief", route["mini_brief"] + "\nUNDECLARED_PORT")):
            bad = copy.copy(request)
            setattr(bad, field, value)
            with self.assertRaises(ValueError):
                c.routed_messages(bad, manifest, arm, {}, (self.frozen / "system.txt").read_text())

    def test_actual_prefix_mismatch_cannot_spend_archive_call(self):
        self.prepare()
        provider, prefix = c.OfflineProvider(), {}
        for arm in c.ARMS:
            path = self.frozen / "manifests" / (arm + ".json")
            responder = c.ProseRoute(provider, arm, json.loads(path.read_bytes()), self.root / arm, prefix, lambda: None,
                                      (self.frozen / "system.txt").read_text())
            compiled = c.base.compile_manifest(path)
            if arm == c.ARMS[0]:
                c.base.run_mini(compiled, self.root / arm / "mini", responder, responder_id="test-prefix")
                prefix["use_before"]["route"]["request"]["messages"][1]["content"] += " changed"
            else:
                with self.assertRaisesRegex(ValueError, "ACTUAL_PREFIX_REQUEST_NOT_IDENTICAL"):
                    c.base.run_mini(compiled, self.root / arm / "mini", responder, responder_id="test-prefix")
        self.assertEqual(provider.calls, 4)


if __name__ == "__main__":
    unittest.main()
