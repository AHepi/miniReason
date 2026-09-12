from __future__ import annotations
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from creib.forge.mini.executor import Request
from minireason import provider as existing_provider
try:
    from minireason import sql_construction_study as s
except ImportError:
    import sql_construction_study as s

REPO = Path(existing_provider.__file__).resolve().parents[2]
RAW_PROSE = 'No executable answer is justified.\n  Preserve this spacing. π\n{"body":"This is quoted data, not a submission."}\n'


class FakeProvider:
    total_calls = 0
    fail_at = None
    def __init__(self, settings, records):
        self.settings, self.records, self.calls = settings, records, 0
    def complete(self, messages, *, json_output=True, coordinate=None):
        if json_output:
            raise AssertionError("Construction must request arbitrary public prose")
        self.calls += 1
        type(self).total_calls += 1
        payload = s.payload_for(messages, self.settings)
        result = {"request": payload, "request_sha256": s.digest(payload), "content": RAW_PROSE,
                  "usage": {"prompt_tokens": 20, "completion_tokens": 10, "total_tokens": 30},
                  "status": "COMPLETE", "finish_reason": "stop"}
        s.write_json(self.records / "call-0001.request.json", {"request": payload, "coordinate": coordinate})
        if type(self).fail_at == type(self).total_calls:
            raise existing_provider.ProviderFailure("SCRIPTED_OFFLINE_FAILURE", "This is an instrument test")
        s.write_json(self.records / "call-0001.response.json", result)
        return result


class ConstructionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "participant/construction.json"
        source = {"schema": "minireason.sql-construction-material.v1", "schema_sql": "CREATE TABLE L(lid INTEGER PRIMARY KEY, k INTEGER);",
            "query_sql": "SELECT ALL lid,k FROM L", "task": "Give an account; unsupported cases may remain unresolved.",
            "source_notes": "An instrument fixture, not a new scientific task.", "sources": [], "value_domain": {}, "events": {}, "constraints": {"prose_admissible": True}}
        s.write_json(self.source, source)
        self.frozen = self.root / "frozen"
        FakeProvider.total_calls, FakeProvider.fail_at = 0, None

    def tearDown(self):
        self.temp.cleanup()

    def prepare(self):
        return s.prepare(self.source, self.frozen, REPO)

    def test_offline_preflight_never_instantiates_provider_and_requests_match(self):
        with patch.object(s, "DeepSeek", side_effect=AssertionError("Provider instantiated offline")):
            plan = self.prepare()
            self.assertEqual(s.verify(self.frozen, REPO)["plan_id"], plan["plan_id"])
        for mode in ("disabled", "native"):
            control = json.loads((self.frozen / "requests" / ("prompt-control-" + mode + ".json")).read_bytes())
            mini = json.loads((self.frozen / "requests" / ("mini-" + mode + ".json")).read_bytes())
            self.assertEqual(control, mini)
        preflight = json.loads((self.frozen / "preflight.json").read_bytes())
        self.assertEqual(preflight["provider_calls"], 0)
        self.assertEqual(preflight["scripted_engine_calls"], 1)
        self.assertTrue(preflight["opaque_prose_preserved"])

    def test_operator_sibling_never_read_or_rendered(self):
        secret = "OPERATOR_ONLY_UNPUBLISHED_WITNESS_9f2c"
        operator = self.root / "operator/oracle.json"
        s.write_json(operator, {"private_fixture_marker": secret})
        reads = []
        original = Path.read_bytes
        def track(path):
            reads.append(path.resolve())
            if path.resolve() == operator.resolve():
                raise AssertionError("Operator oracle read")
            return original(path)
        with patch.object(Path, "read_bytes", track):
            self.prepare()
        self.assertNotIn(operator.resolve(), reads)
        for path in (self.frozen / "requests").glob("*.json"):
            self.assertNotIn(secret, path.read_text())

    def test_exact_route_rejects_extra_source_or_wrong_coordinate(self):
        raw = self.source.read_bytes()
        request = Request("construct", s.KIND, 0, s.expected_brief(raw), cycle=1, phase="both")
        s.validate_coordinate(request, raw)
        with self.assertRaisesRegex(ValueError, "ROUTED_SOURCE_MISMATCH"):
            s.validate_coordinate(Request("construct", s.KIND, 0, request.brief + "\nAn extra rule", cycle=1, phase="both"), raw)
        with self.assertRaisesRegex(ValueError, "UNEXPECTED_MINI_COORDINATE"):
            s.validate_coordinate(Request("construct", s.KIND, 1, request.brief, cycle=1, phase="both"), raw)

    def test_rehashed_effective_metadata_tamper_is_refused(self):
        plan = self.prepare()
        changes = {"max_provider_calls": 8, "max_aggregate_completion_tokens": 1, "automatic_retries": 1,
                   "native_reasoning_effort": "max", "endpoint": "https://example.invalid/v1/chat/completions",
                   "template": "unimplemented_template", "cycles_per_arm": 2, "model_stages_per_cycle": ["construct", "use"],
                   "terminal_kind_is_transport_only": False, "jobs": 3, "operator_input_files": ["operator/oracle.json"],
                   "selected_construction_arm": "direct-native", "status": "COMPLETE", "test_id": "E025"}
        for key, value in changes.items():
            with self.subTest(field=key):
                tampered = {**plan, key: value}
                tampered["plan_id"] = s.digest({k: v for k, v in tampered.items() if k != "plan_id"})
                (self.frozen / "plan.json").write_bytes(s.encoded(tampered))
                with self.assertRaisesRegex(ValueError, "EFFECTIVE_CONTRACT_CHANGED"):
                    s.verify(self.frozen, REPO)
        (self.frozen / "plan.json").write_bytes(s.encoded(plan))

    def test_source_tamper_is_refused(self):
        self.prepare()
        path = self.frozen / "participant-source.json"
        value = json.loads(path.read_bytes()); value["task"] += " Changed"
        path.write_bytes(s.encoded(value))
        with self.assertRaisesRegex(ValueError, "PARTICIPANT_SOURCE_CHANGED"):
            s.verify(self.frozen, REPO)

    def test_request_tamper_is_refused(self):
        self.prepare()
        path = self.frozen / "requests/mini-disabled.json"
        value = json.loads(path.read_bytes()); value["request"]["messages"][1]["content"] += " Added"
        path.write_bytes(s.encoded(value))
        with self.assertRaisesRegex(ValueError, "FROZEN_REQUEST_CHANGED"):
            s.verify(self.frozen, REPO)

    def test_manifest_tamper_is_refused(self):
        self.prepare()
        path = self.frozen / "manifest.json"
        path.write_bytes(path.read_bytes() + b" ")
        with self.assertRaisesRegex(ValueError, "MINI_MANIFEST_CHANGED"):
            s.verify(self.frozen, REPO)

    def test_runtime_change_is_refused(self):
        self.prepare()
        runtime = s.runtime_files(REPO)
        runtime["src/minireason/provider.py"] = "0" * 64
        with patch.object(s, "runtime_files", return_value=runtime):
            with self.assertRaisesRegex(ValueError, "RUNTIME_SOURCE_CHANGED"):
                s.verify(self.frozen, REPO)

    def test_frozen_output_is_never_overwritten(self):
        self.prepare()
        with self.assertRaises(FileExistsError):
            self.prepare()

    def test_external_plan_pin_checked_before_provider(self):
        self.prepare()
        with patch.object(s, "DeepSeek", side_effect=AssertionError("Provider accessed before plan pin")):
            with self.assertRaisesRegex(ValueError, "EXTERNALLY_PINNED_PLAN_ID_MISMATCH"):
                s.run(self.frozen, self.root / "live-probe", REPO, "wrong")

    def test_mock_full_run_retains_arbitrary_prose_in_every_arm(self):
        plan = self.prepare()
        with patch.object(s, "DeepSeek", FakeProvider):
            summary = s.run(self.frozen, self.root / "mock-run", REPO, plan["plan_id"])
        self.assertEqual(summary["status"], "COMPLETE")
        self.assertEqual(FakeProvider.total_calls, 6)
        self.assertFalse(summary["automatic_successor_started"])
        for arm in s.ARMS:
            path = self.root / "mock-run" / arm / "public-answer.txt"
            self.assertEqual(path.read_bytes(), RAW_PROSE.encode("utf-8"))
        for mode in ("disabled", "native"):
            control = json.loads((self.root / "mock-run" / ("prompt-control-" + mode) / "calls/call-0001.request.json").read_bytes())
            mini = json.loads((self.root / "mock-run" / ("mini-" + mode) / "calls/call-0001.request.json").read_bytes())
            self.assertEqual(control["request"], mini["request"])

    def test_mock_failure_stops_and_preserves_partial_record(self):
        plan = self.prepare()
        FakeProvider.fail_at = 3
        with patch.object(s, "DeepSeek", FakeProvider):
            summary = s.run(self.frozen, self.root / "mock-run", REPO, plan["plan_id"])
        self.assertEqual(summary["status"], "INTERRUPTED")
        self.assertEqual(FakeProvider.total_calls, 3)
        self.assertEqual(summary["unattempted_arms"], list(s.ARMS[3:]))
        self.assertEqual(summary["arms"][-1]["error_code"], "SCRIPTED_OFFLINE_FAILURE")


if __name__ == "__main__":
    unittest.main()
