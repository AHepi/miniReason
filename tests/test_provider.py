"""Offline checks for transport controls, failure evidence, and secret handling.

Every credential in these tests is a synthetic sentinel. No test opens a socket.
"""
from __future__ import annotations

import copy
import io
import json
import os
import tempfile
import threading
import unittest
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest import mock

from minireason import provider


FAKE_KEY = "synthetic-provider-test-credential-not-a-live-key"
MESSAGES = [{"role": "user", "content": "Return a JSON object with an answer."}]


def good_response(**changes):
    result = {
        "id": "synthetic-call-id",
        "model": "deepseek-flash",
        "created": 1,
        "choices": [{"message": {"content": '{"answer": "ok"}'},
                     "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }
    result.update(changes)
    return result


class Response:
    def __init__(self, result):
        self.raw = result if isinstance(result, bytes) else json.dumps(result).encode()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.raw


class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = mock.patch.dict(os.environ, {"DEEPSEEK_API_KEY": FAKE_KEY})
        self.env.start()
        self.addCleanup(self.env.stop)

    def client(self, **settings):
        return provider.DeepSeek(provider.Settings(**settings), self.root)

    def records(self):
        return [json.loads(path.read_text()) for path in sorted(self.root.glob("*.response.json"))]

    def persisted(self):
        return "\n".join(path.read_text() for path in self.root.rglob("*.json"))

    def fail_with_record(self, result, *, client=None, messages=None, coordinate=None):
        client = client or self.client()
        with mock.patch.object(provider, "_open", return_value=Response(result)):
            with self.assertRaises(provider.ProviderFailure) as raised:
                client.complete(messages or MESSAGES, coordinate=coordinate)
        records = self.records()
        self.assertEqual(len(records), 1, "A failed call needs a durable failure record")
        self.assertNotEqual(records[0]["status"], "COMPLETE")
        self.assertEqual(records[0]["status"], raised.exception.code)
        self.assertNotIn(FAKE_KEY, self.persisted())
        return raised.exception, records[0]

    def test_disabled_thinking_and_json_controls_are_actually_sent(self):
        client = self.client(max_tokens=128, timeout_seconds=17)
        with mock.patch.object(provider, "_open", return_value=Response(good_response())) as opened:
            record = client.complete(MESSAGES)
        request = opened.call_args.args[0]
        sent = json.loads(request.data)
        self.assertEqual(request.full_url, "https://api.deepseek.com/v1/chat/completions")
        self.assertEqual(request.get_header("Authorization"), "Bearer " + FAKE_KEY)
        self.assertEqual(sent, {
            "model": "deepseek-flash", "messages": MESSAGES, "stream": False,
            "max_tokens": 128, "thinking": {"type": "disabled"},
            "response_format": {"type": "json_object"},
        })
        self.assertEqual(opened.call_args.kwargs["timeout"], 17)
        self.assertEqual(record["request"], sent)
        self.assertEqual(record["request_sha256"], provider.digest(sent))
        self.assertEqual((client.calls, client.prompt_tokens, client.completion_tokens), (1, 10, 5))
        self.assertNotIn(FAKE_KEY, self.persisted())

    def test_native_thinking_sends_effort_without_seed_or_temperature(self):
        result = good_response()
        result["choices"][0]["message"]["reasoning_content"] = "SYNTHETIC PRIVATE REASONING"
        with mock.patch.object(provider, "_open", return_value=Response(result)) as opened:
            record = self.client(thinking=True, reasoning_effort="max").complete(MESSAGES, json_output=False)
        sent = json.loads(opened.call_args.args[0].data)
        self.assertEqual(sent["thinking"], {"type": "enabled"})
        self.assertEqual(sent["reasoning_effort"], "max")
        self.assertNotIn("seed", sent)
        self.assertNotIn("temperature", sent)
        self.assertNotIn("response_format", sent)
        self.assertTrue(record["reasoning_content_present"])
        self.assertFalse(record["reasoning_content_persisted"])
        self.assertNotIn("SYNTHETIC PRIVATE REASONING", self.persisted())

    def test_truncation_is_failure_even_when_content_is_valid_json(self):
        result = good_response()
        result["choices"][0]["finish_reason"] = "length"
        error, _ = self.fail_with_record(result)
        self.assertEqual(error.code, "INCOMPLETE_GENERATION")

    def test_reported_completion_over_ceiling_fails(self):
        result = good_response(usage={"prompt_tokens": 10, "completion_tokens": 129})
        error, _ = self.fail_with_record(result, client=self.client(max_tokens=128))
        self.assertEqual(error.code, "COMPLETION_CEILING_VIOLATED")

    def test_missing_usage_fails(self):
        result = good_response()
        del result["usage"]
        error, _ = self.fail_with_record(result)
        self.assertEqual(error.code, "USAGE_UNAVAILABLE")

    def test_missing_prompt_usage_cannot_be_marked_complete(self):
        self.fail_with_record(good_response(usage={"completion_tokens": 5}))

    def test_negative_completion_usage_is_rejected(self):
        self.fail_with_record(good_response(usage={"prompt_tokens": 10, "completion_tokens": -1}))

    def test_boolean_completion_usage_is_rejected(self):
        self.fail_with_record(good_response(usage={"prompt_tokens": 10, "completion_tokens": True}))

    def test_negative_prompt_usage_is_rejected(self):
        self.fail_with_record(good_response(usage={"prompt_tokens": -1, "completion_tokens": 5}))

    def test_boolean_prompt_usage_is_rejected(self):
        self.fail_with_record(good_response(usage={"prompt_tokens": True, "completion_tokens": 5}))

    def test_nonnumeric_usage_has_failure_evidence(self):
        self.fail_with_record(good_response(usage={"prompt_tokens": 10, "completion_tokens": "unknown"}))

    def test_nontext_content_has_failure_evidence(self):
        result = good_response()
        result["choices"][0]["message"]["content"] = [{"type": "text", "text": "ok"}]
        self.fail_with_record(result)

    def test_empty_content_has_failure_evidence(self):
        result = good_response()
        result["choices"][0]["message"]["content"] = ""
        error, _ = self.fail_with_record(result)
        self.assertEqual(error.code, "EMPTY_GENERATION")

    def test_missing_choice_has_failure_evidence(self):
        self.fail_with_record(good_response(choices=[]))

    def test_malformed_json_has_failure_evidence(self):
        self.fail_with_record(b"not JSON")

    def test_thinking_mode_mismatch_has_failure_evidence(self):
        error, _ = self.fail_with_record(good_response(), client=self.client(thinking=True))
        self.assertEqual(error.code, "THINKING_MODE_MISMATCH")

    def test_answer_credential_echo_is_redacted_and_rejected(self):
        result = good_response()
        result["choices"][0]["message"]["content"] = FAKE_KEY
        error, record = self.fail_with_record(result)
        self.assertEqual(error.code, "CREDENTIAL_ECHO")
        self.assertNotIn(FAKE_KEY, record["content"])

    def test_metadata_credential_echo_is_redacted_and_rejected(self):
        self.fail_with_record(good_response(id=FAKE_KEY))

    def test_credential_in_coordinate_is_never_written_or_sent(self):
        client = self.client()
        with mock.patch.object(provider, "_open", return_value=Response(good_response())) as opened:
            with self.assertRaises(provider.ProviderFailure):
                client.complete(MESSAGES, coordinate={"stage_id": FAKE_KEY})
        opened.assert_not_called()
        self.assertNotIn(FAKE_KEY, self.persisted())
        self.assertEqual(len(self.records()), 1)

    def test_credential_in_prompt_is_refused_with_sanitized_failure_record(self):
        client = self.client()
        with mock.patch.object(provider, "_open") as opened:
            with self.assertRaises(provider.ProviderFailure) as raised:
                client.complete([{"role": "user", "content": FAKE_KEY}])
        opened.assert_not_called()
        self.assertEqual(raised.exception.code, "SECRET_IN_REQUEST")
        self.assertNotIn(FAKE_KEY, self.persisted())
        self.assertEqual(len(self.records()), 1, "Local credential refusal still needs sanitized evidence")

    def test_http_error_is_redacted_recorded_and_not_retried(self):
        client = self.client()
        error = urllib.error.HTTPError("https://api.deepseek.com/v1/chat/completions", 429,
                                       "rate limited", {}, io.BytesIO(FAKE_KEY.encode()))
        with mock.patch.object(provider, "_open", side_effect=error) as opened:
            with self.assertRaises(provider.ProviderFailure) as raised:
                client.complete(MESSAGES)
        self.assertEqual(raised.exception.code, "HTTP_429")
        self.assertEqual(opened.call_count, 1)
        self.assertEqual(self.records()[0]["status"], "HTTP_429")
        self.assertNotIn(FAKE_KEY, self.persisted())
        self.assertNotIn(FAKE_KEY, str(raised.exception))

    def test_transport_error_is_redacted_recorded_and_not_retried(self):
        client = self.client()
        with mock.patch.object(provider, "_open", side_effect=TimeoutError(FAKE_KEY)) as opened:
            with self.assertRaises(provider.ProviderFailure) as raised:
                client.complete(MESSAGES)
        self.assertEqual(opened.call_count, 1)
        self.assertEqual(len(self.records()), 1)
        self.assertNotIn(FAKE_KEY, self.persisted())
        self.assertNotIn(FAKE_KEY, str(raised.exception))

    def test_global_transport_concurrency_is_at_most_five(self):
        lock = threading.Lock()
        first_five = threading.Event()
        release = threading.Event()
        count = {"active": 0, "peak": 0}

        class BlockingResponse(Response):
            def read(self):
                with lock:
                    count["active"] += 1
                    count["peak"] = max(count["peak"], count["active"])
                    if count["active"] >= 5:
                        first_five.set()
                try:
                    if not release.wait(5):
                        raise TimeoutError("Offline test barrier timed out")
                    return super().read()
                finally:
                    with lock:
                        count["active"] -= 1

        clients = [provider.DeepSeek(provider.Settings(), self.root / str(i)) for i in range(8)]
        with mock.patch.object(provider, "_open", side_effect=lambda *args, **kwargs: BlockingResponse(good_response())):
            with ThreadPoolExecutor(max_workers=8) as pool:
                futures = [pool.submit(client.complete, copy.deepcopy(MESSAGES)) for client in clients]
                try:
                    self.assertTrue(first_five.wait(5), "Five calls should be able to make concurrent progress")
                finally:
                    release.set()
                for future in futures:
                    self.assertEqual(future.result(timeout=5)["status"], "COMPLETE")
        self.assertEqual(count["peak"], 5)


if __name__ == "__main__":
    unittest.main()
