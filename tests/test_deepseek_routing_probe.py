"""Offline qualification of the DeepSeek harness bridge; no network calls."""
from pathlib import Path
import os
import tempfile
import unittest
from unittest.mock import patch
from tools import deepseek_routing_probe as d


class FakeProvider:
    calls = 0
    failure = False
    def __init__(self, settings, records):
        self.settings, self.records = settings, records
    def complete(self, messages, *, json_output, coordinate):
        type(self).calls += 1
        if type(self).failure:
            raise RuntimeError("scripted failure")
        payload = d.p.study.base.payload_for(messages, self.settings)
        return {"request": payload, "request_sha256": d.p.study.base.digest(payload),
                "content": "Opaque Unicode public answer π / " + str(coordinate["global_call_id"]),
                "status": "COMPLETE", "finish_reason": "stop", "returned_model": "scripted-offline-provider",
                "usage": {"prompt_tokens": 2, "completion_tokens": 3, "total_tokens": 5}}


class DeepSeekRoutingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.output = self.root / "H002"
        self.repo = d.p.PortableRepositoryPath(Path(d.__file__).resolve().parents[1])
        FakeProvider.calls, FakeProvider.failure = 0, False
        d.initialize(self.repo, self.output)

    def tearDown(self):
        self.temp.cleanup()

    def run_one(self, call):
        d.make_request(self.repo, self.output, call)
        with patch.object(d, "DeepSeek", FakeProvider), patch.object(d, "check_published", return_value="scripted-remote"), patch.dict(os.environ, {"DEEPSEEK_API_KEY": "synthetic-test-only"}):
            return d.execute(self.repo, self.output, call)

    def test_real_routes_original_response_validator_and_reported_usage(self):
        for call in range(1, 7):
            self.run_one(call)
        result = d.summarize(self.repo, self.output)
        self.assertEqual(result["provider_calls"], 6)
        self.assertEqual(FakeProvider.calls, 6)
        self.assertEqual(result["usage"], {"prompt_tokens": 12, "completion_tokens": 18, "total_tokens": 30})
        self.assertTrue(result["shared_prefix_messages_equal"])
        self.assertFalse(result["original_E028_completed"])
        self.assertFalse(result["full_durable_Mini_run"])
        self.assertEqual(d.p.load_json(self.output / "plan.json")["settings"]["model"], "deepseek-flash")

    def test_publication_failure_prevents_attempt_and_provider(self):
        d.make_request(self.repo, self.output, 1)
        with patch.object(d, "DeepSeek", FakeProvider), patch.object(d, "check_published", side_effect=ValueError("REMOTE_MAIN_CHANGED")), patch.dict(os.environ, {"DEEPSEEK_API_KEY": "synthetic-test-only"}):
            with self.assertRaisesRegex(ValueError, "REMOTE_MAIN_CHANGED"):
                d.execute(self.repo, self.output, 1)
        self.assertEqual(FakeProvider.calls, 0)
        self.assertFalse((self.output / "attempts/0001.json").exists())

    def test_provider_failure_stops_following_requests_without_retry(self):
        FakeProvider.failure = True
        with self.assertRaises(RuntimeError):
            self.run_one(1)
        self.assertEqual(FakeProvider.calls, 1)
        self.assertTrue((self.output / "stopped.json").exists())
        with self.assertRaisesRegex(ValueError, "H002_ALREADY_STOPPED"):
            d.make_request(self.repo, self.output, 2)
        with self.assertRaisesRegex(ValueError, "H002_NO_RETRY"):
            d.execute(self.repo, self.output, 1)
        self.assertEqual(FakeProvider.calls, 1)

    def test_tampered_packet_blocks_provider_and_response_metadata_is_real_contract(self):
        d.make_request(self.repo, self.output, 1)
        (self.output / "packets/0001.json").write_text('{"messages":[]}', encoding="utf-8")
        with patch.object(d, "DeepSeek", FakeProvider), patch.dict(os.environ, {"DEEPSEEK_API_KEY": "synthetic-test-only"}):
            with self.assertRaisesRegex(ValueError, "PARTICIPANT_PACKET_CHANGED"):
                d.execute(self.repo, self.output, 1)
        self.assertEqual(FakeProvider.calls, 0)


if __name__ == "__main__":
    unittest.main()
