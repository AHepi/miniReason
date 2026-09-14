"""Offline checks for the second transport: records, redaction, per-key slots.

Every credential here is a synthetic sentinel. No test opens a socket: the
transport seam ``provider_openai_compat._open`` is replaced, and the one test
that reaches lower replaces ``http.client.HTTPSConnection`` itself so that a
regression which bypassed the seam would still be caught rather than dialling
out.
"""
from __future__ import annotations

import copy
import io
import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest import mock

from minireason import provider_openai_compat as compat


DEEPSEEK_KEY = "zqf7x2-deepseek-sentinel-credential-not-a-live-key"
OLLAMA_KEY = "wm4k9b-ollama-sentinel-credential-not-a-live-key"
MESSAGES = [{"role": "user", "content": "Reply with a JSON object."}]

COMPAT_ENDPOINT = compat.Endpoint(
    name="test/compat", base_url="https://example.invalid/v1", model="test-model",
    key_env="OLLAMA_API_KEY", family="ollama-cloud/test")
NATIVE_ENDPOINT = compat.Endpoint(
    name="test/native", base_url="https://example.invalid", model="test-model",
    key_env="OLLAMA_API_KEY", family="ollama-cloud/test",
    chat_path="/api/chat", native=True)
DEEPSEEK_ENDPOINT = compat.Endpoint(
    name="test/deepseek", base_url="https://example.invalid/v1", model="deepseek-flash",
    key_env="DEEPSEEK_API_KEY", family="deepseek")


def openai_body(**changes):
    body = {
        "id": "probe-call-id",
        "model": "test-model",
        "created": 1,
        "choices": [{"message": {"content": '{"ok": true}'}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 11, "completion_tokens": 4, "total_tokens": 15},
    }
    body.update(changes)
    return body


def native_body(**changes):
    body = {
        "model": "test-model",
        "created_at": "2026-09-14T00:00:00Z",
        "message": {"role": "assistant", "content": '{"ok": true}'},
        "done": True,
        "done_reason": "stop",
        "prompt_eval_count": 11,
        "eval_count": 4,
    }
    body.update(changes)
    return body


class Response:
    def __init__(self, payload):
        self.raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.raw


class Base(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = mock.patch.dict(os.environ, {"DEEPSEEK_API_KEY": DEEPSEEK_KEY,
                                                "OLLAMA_API_KEY": OLLAMA_KEY})
        self.env.start()
        self.addCleanup(self.env.stop)
        compat._reset_slot_registry()
        self.addCleanup(compat._reset_slot_registry)
        compat._reset_registered_secret_envs()
        self.addCleanup(compat._reset_registered_secret_envs)

    def provider(self, endpoint=COMPAT_ENDPOINT, sub="a"):
        return compat.OpenAICompatProvider(endpoint, self.root / sub)

    def persisted(self):
        return "\n".join(path.read_text() for path in sorted(self.root.rglob("*.json")))

    def records(self, sub="a"):
        return [json.loads(path.read_text())
                for path in sorted((self.root / sub).glob("*.response.json"))]

    def requests(self, sub="a"):
        return [json.loads(path.read_text())
                for path in sorted((self.root / sub).glob("*.request.json"))]

    def assertNoCredentials(self):
        blob = self.persisted()
        for secret in (DEEPSEEK_KEY, OLLAMA_KEY):
            self.assertNotIn(secret, blob, "A credential reached a record")
            self.assertNotIn(secret[:12], blob, "A credential fragment reached a record")


class RequestRecordTests(Base):
    def test_request_record_is_written_before_the_socket_is_touched(self):
        seen = {}
        client = self.provider()

        def capture(request, *, timeout):
            seen["records"] = sorted(path.name for path in (self.root / "a").iterdir())
            seen["body"] = request.data
            return Response(openai_body())

        with mock.patch.object(compat, "_open", side_effect=capture):
            client.complete(MESSAGES, response_format={"type": "json_object"},
                            max_tokens=64, seed=7, temperature=0)
        self.assertEqual(seen["records"], ["call-0001.request.json"],
                         "The request record must exist before the request is sent")
        written = self.requests()[0]
        self.assertEqual(written["schema_version"], "minireason.call.v2")
        self.assertEqual(written["request"], json.loads(seen["body"]))
        self.assertEqual(written["request_sha256"], compat.digest(written["request"]))
        # The recorded byte hash is of the exact bytes that went out.
        import hashlib
        self.assertEqual(written["request_bytes_sha256"], hashlib.sha256(seen["body"]).hexdigest())
        self.assertEqual(written["endpoint"], {"name": "test/compat", "family": "ollama-cloud/test",
                                               "base_url": "https://example.invalid/v1",
                                               "model": "test-model"})
        self.assertIn("started_at", written)
        self.assertIn("settings", written)

    def test_endpoint_block_never_carries_the_key_or_its_env_value(self):
        with mock.patch.object(compat, "_open", return_value=Response(openai_body())):
            self.provider().complete(MESSAGES)
        written = self.requests()[0]
        self.assertEqual(set(written["endpoint"]), {"name", "base_url", "model", "family"})
        self.assertEqual(written["settings"]["key_env"], "OLLAMA_API_KEY")
        self.assertNoCredentials()

    def test_authorization_header_is_sent_but_never_recorded(self):
        with mock.patch.object(compat, "_open", return_value=Response(openai_body())) as opened:
            self.provider().complete(MESSAGES)
        request = opened.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer " + OLLAMA_KEY)
        self.assertEqual(self.requests()[0]["request_header_names"],
                         ["Accept", "Authorization", "Content-Type"])
        self.assertNoCredentials()

    def test_records_are_write_once(self):
        path = self.root / "a" / "call-0001.request.json"
        compat.write_new(path, {"first": True})
        with self.assertRaises(FileExistsError):
            compat.write_new(path, {"second": True})
        self.assertEqual(json.loads(path.read_text()), {"first": True})

    def test_redaction_happens_on_write(self):
        path = self.root / "a" / "leak.json"
        compat.write_new(path, {"note": "value is " + OLLAMA_KEY})
        self.assertEqual(json.loads(path.read_text())["note"], "value is [REDACTED_CREDENTIAL]")

    def test_settings_declare_that_reasoning_text_is_not_persisted(self):
        # Both assertions pin documented constants of the settings block; the
        # behavioural proof lives in TranslationTests' persisted() checks.
        with mock.patch.object(compat, "_open", return_value=Response(openai_body())):
            self.provider().complete(MESSAGES)
        self.assertFalse(self.requests()[0]["settings"]["native_reasoning_text_persisted"])
        self.assertEqual(self.requests()[0]["settings"]["retries"], 0)


class OutcomeTests(Base):
    def fail_with_record(self, payload, *, endpoint=COMPAT_ENDPOINT, **call):
        client = self.provider(endpoint)
        with mock.patch.object(compat, "_open", return_value=Response(payload)):
            with self.assertRaises(compat.ProviderFailure) as raised:
                client.complete(MESSAGES, **call)
        records = self.records()
        self.assertEqual(len(records), 1, "A failed call needs a durable failure record")
        self.assertEqual(records[0]["status"], raised.exception.code)
        self.assertNotEqual(records[0]["status"], "COMPLETE")
        self.assertNoCredentials()
        return raised.exception, records[0]

    def test_complete_call_returns_a_result_and_a_record(self):
        with mock.patch.object(compat, "_open", return_value=Response(openai_body())):
            result = self.provider().complete(MESSAGES)
        self.assertEqual(result.status, "COMPLETE")
        self.assertEqual(result.returned_model, "test-model")
        self.assertEqual(result.finish_reason, "stop")
        self.assertEqual(result.usage["completion_tokens"], 4)
        # Pins a documented constant, not behaviour: no code path assigns
        # reasoning_content_persisted. The assertions that actually prove
        # reasoning text is not persisted are the assertNotIn(...) checks in
        # TranslationTests over self.persisted().
        self.assertFalse(result.reasoning_content_persisted)
        self.assertEqual(result["status"], "COMPLETE")
        self.assertEqual(self.records()[0]["status"], "COMPLETE")

    def test_truncation_is_incomplete_generation(self):
        payload = openai_body()
        payload["choices"][0]["finish_reason"] = "length"
        error, _ = self.fail_with_record(payload)
        self.assertEqual(error.code, "INCOMPLETE_GENERATION")

    def test_empty_generation(self):
        payload = openai_body()
        payload["choices"][0]["message"]["content"] = "   "
        error, _ = self.fail_with_record(payload)
        self.assertEqual(error.code, "EMPTY_GENERATION")

    def test_missing_usage(self):
        payload = openai_body()
        del payload["usage"]
        error, _ = self.fail_with_record(payload)
        self.assertEqual(error.code, "USAGE_UNAVAILABLE")

    def test_boolean_usage_is_not_an_integer_count(self):
        error, _ = self.fail_with_record(
            openai_body(usage={"prompt_tokens": True, "completion_tokens": 4}))
        self.assertEqual(error.code, "USAGE_UNAVAILABLE")

    def test_nontext_content_is_a_content_type_failure(self):
        payload = openai_body()
        payload["choices"][0]["message"]["content"] = [{"type": "text", "text": "ok"}]
        error, _ = self.fail_with_record(payload)
        self.assertEqual(error.code, "CONTENT_TYPE")

    def test_no_choice_is_a_transport_or_response_error(self):
        error, _ = self.fail_with_record(openai_body(choices=[]))
        self.assertEqual(error.code, "TRANSPORT_OR_RESPONSE_ERROR")

    def test_malformed_body_is_a_transport_or_response_error(self):
        error, _ = self.fail_with_record(b"not JSON")
        self.assertEqual(error.code, "TRANSPORT_OR_RESPONSE_ERROR")

    def test_answer_credential_echo_is_redacted_and_rejected(self):
        payload = openai_body()
        payload["choices"][0]["message"]["content"] = "your key is " + OLLAMA_KEY
        error, record = self.fail_with_record(payload)
        self.assertEqual(error.code, "CREDENTIAL_ECHO")
        self.assertTrue(record["credential_redaction"])
        self.assertEqual(record["content"], "your key is [REDACTED_CREDENTIAL]")

    def test_metadata_credential_echo_is_rejected(self):
        error, _ = self.fail_with_record(openai_body(id=OLLAMA_KEY))
        self.assertEqual(error.code, "CREDENTIAL_ECHO")

    def test_credential_in_prompt_is_refused_before_any_send(self):
        client = self.provider()
        with mock.patch.object(compat, "_open") as opened:
            with self.assertRaises(compat.ProviderFailure) as raised:
                client.complete([{"role": "user", "content": "my key is " + OLLAMA_KEY}])
        opened.assert_not_called()
        self.assertEqual(raised.exception.code, "SECRET_IN_REQUEST")
        self.assertEqual(len(self.records()), 1, "A local refusal still needs sanitized evidence")
        self.assertNoCredentials()

    def test_any_process_credential_in_the_prompt_is_refused_not_only_this_endpoints_key(self):
        client = self.provider()
        with mock.patch.object(compat, "_open") as opened:
            with self.assertRaises(compat.ProviderFailure) as raised:
                client.complete([{"role": "user", "content": DEEPSEEK_KEY}])
        opened.assert_not_called()
        self.assertEqual(raised.exception.code, "SECRET_IN_REQUEST")
        self.assertNoCredentials()

    def test_credential_in_coordinate_is_refused(self):
        client = self.provider()
        with mock.patch.object(compat, "_open") as opened:
            with self.assertRaises(compat.ProviderFailure) as raised:
                client.complete(MESSAGES, coordinate={"stage_id": OLLAMA_KEY})
        opened.assert_not_called()
        self.assertEqual(raised.exception.code, "SECRET_IN_REQUEST")
        self.assertNoCredentials()

    def test_http_error_is_recorded_redacted_and_never_retried(self):
        client = self.provider()
        error = urllib.error.HTTPError("https://example.invalid/v1/chat/completions", 404,
                                       "not found", {}, io.BytesIO(OLLAMA_KEY.encode()))
        with mock.patch.object(compat, "_open", side_effect=error) as opened:
            with self.assertRaises(compat.ProviderFailure) as raised:
                client.complete(MESSAGES)
        self.assertEqual(raised.exception.code, "HTTP_404")
        self.assertEqual(opened.call_count, 1, "No automatic retry")
        self.assertEqual(self.records()[0]["status"], "HTTP_404")
        self.assertNotIn(OLLAMA_KEY, str(raised.exception))
        self.assertNoCredentials()

    def test_transport_error_is_recorded_redacted_and_never_retried(self):
        client = self.provider()
        with mock.patch.object(compat, "_open", side_effect=TimeoutError(OLLAMA_KEY)) as opened:
            with self.assertRaises(compat.ProviderFailure) as raised:
                client.complete(MESSAGES)
        self.assertEqual(raised.exception.code, "TRANSPORT_OR_RESPONSE_ERROR")
        self.assertEqual(opened.call_count, 1, "No automatic retry")
        self.assertNotIn(OLLAMA_KEY, str(raised.exception))
        self.assertNoCredentials()

    def test_missing_key_at_construction_is_key_missing(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            del os.environ["OLLAMA_API_KEY"]
            with self.assertRaises(compat.ProviderFailure) as raised:
                compat.OpenAICompatProvider(COMPAT_ENDPOINT, self.root / "a")
        self.assertEqual(raised.exception.code, "KEY_MISSING")

    def test_key_removed_between_construction_and_call_is_recorded_as_key_missing(self):
        client = self.provider()
        with mock.patch.object(compat, "_open") as opened:
            with mock.patch.dict(os.environ, {"OLLAMA_API_KEY": ""}):
                with self.assertRaises(compat.ProviderFailure) as raised:
                    client.complete(MESSAGES)
        opened.assert_not_called()
        self.assertEqual(raised.exception.code, "KEY_MISSING")
        self.assertEqual(self.records()[0]["status"], "KEY_MISSING")

    def test_redirects_are_refused(self):
        handler = compat._NoRedirect()
        self.assertIsNone(handler.redirect_request(
            None, None, 302, "Found", {}, "https://elsewhere.invalid/"))

    def test_no_redirect_handler_is_installed_on_the_opener(self):
        # A regression that dropped the handler would let a credentialed
        # request be replayed at another host; the seam is checked directly.
        with mock.patch.object(urllib.request, "build_opener") as build:
            build.return_value.open.return_value = Response(openai_body())
            compat._open(urllib.request.Request("https://example.invalid/"), timeout=1)
        self.assertIsInstance(build.call_args.args[0], compat._NoRedirect)


class TranslationTests(Base):
    def sent(self, endpoint, payload, **call):
        client = self.provider(endpoint)
        with mock.patch.object(compat, "_open", return_value=Response(payload)) as opened:
            result = client.complete(MESSAGES, **call)
        return json.loads(opened.call_args.args[0].data), opened.call_args, result

    def test_openai_compatible_payload_shape(self):
        sent, call, _ = self.sent(COMPAT_ENDPOINT, openai_body(),
                                  response_format={"type": "json_object"},
                                  max_tokens=64, seed=7, temperature=0)
        self.assertEqual(sent, {"model": "test-model", "messages": MESSAGES, "stream": False,
                                "max_tokens": 64, "temperature": 0, "seed": 7,
                                "response_format": {"type": "json_object"}})
        self.assertEqual(call.args[0].full_url, "https://example.invalid/v1/chat/completions")
        self.assertEqual(call.kwargs["timeout"], 180)

    def test_native_payload_is_translated(self):
        sent, call, result = self.sent(NATIVE_ENDPOINT, native_body(),
                                       response_format={"type": "json_object"},
                                       max_tokens=64, seed=7, temperature=0)
        self.assertEqual(sent, {"model": "test-model", "messages": MESSAGES, "stream": False,
                                "format": "json",
                                "options": {"num_predict": 64, "temperature": 0, "seed": 7}})
        self.assertEqual(call.args[0].full_url, "https://example.invalid/api/chat")
        self.assertEqual(result.status, "COMPLETE")
        self.assertEqual(result.usage, {"prompt_tokens": 11, "completion_tokens": 4,
                                        "total_tokens": 15})
        self.assertEqual(result.finish_reason, "stop")
        self.assertEqual(result.returned_model, "test-model")
        self.assertEqual(result.content, '{"ok": true}')

    def test_native_json_schema_becomes_an_ollama_format_object(self):
        schema = {"type": "object", "properties": {"ok": {"type": "boolean"}}}
        sent, _, _ = self.sent(NATIVE_ENDPOINT, native_body(),
                               response_format={"type": "json_schema",
                                                "json_schema": {"name": "x", "schema": schema}})
        self.assertEqual(sent["format"], schema)

    def test_native_done_without_done_reason_reads_as_stop(self):
        payload = native_body()
        del payload["done_reason"]
        _, _, result = self.sent(NATIVE_ENDPOINT, payload)
        self.assertEqual(result.finish_reason, "stop")

    def test_native_unfinished_response_is_incomplete_not_complete(self):
        payload = native_body(done=False)
        del payload["done_reason"]
        client = self.provider(NATIVE_ENDPOINT)
        with mock.patch.object(compat, "_open", return_value=Response(payload)):
            with self.assertRaises(compat.ProviderFailure) as raised:
                client.complete(MESSAGES)
        self.assertEqual(raised.exception.code, "INCOMPLETE_GENERATION")

    def test_native_thinking_is_detected_but_never_persisted(self):
        payload = native_body()
        payload["message"]["thinking"] = "SYNTHETIC PRIVATE REASONING"
        _, _, result = self.sent(NATIVE_ENDPOINT, payload)
        self.assertTrue(result.reasoning_content_present)
        self.assertFalse(result.reasoning_content_persisted)
        self.assertNotIn("SYNTHETIC PRIVATE REASONING", self.persisted())
        self.assertNotIn("SYNTHETIC PRIVATE REASONING", result.content)

    def test_openai_reasoning_content_is_detected_but_never_persisted(self):
        payload = openai_body()
        payload["choices"][0]["message"]["reasoning_content"] = "SYNTHETIC PRIVATE REASONING"
        _, _, result = self.sent(COMPAT_ENDPOINT, payload)
        self.assertTrue(result.reasoning_content_present)
        self.assertNotIn("SYNTHETIC PRIVATE REASONING", self.persisted())

    def test_deepseek_thinking_controls_are_sent_for_the_deepseek_family(self):
        # The body must carry reasoning text: with thinking enabled, a DeepSeek
        # answer that carries none is a THINKING_MODE_MISMATCH (provider.py:169).
        thinking_body = openai_body(model="deepseek-flash")
        thinking_body["choices"][0]["message"]["reasoning_content"] = "SYNTHETIC PRIVATE REASONING"
        sent, _, _ = self.sent(DEEPSEEK_ENDPOINT, thinking_body,
                               thinking=True, reasoning_effort="max")
        self.assertEqual(sent["thinking"], {"type": "enabled"})
        self.assertEqual(sent["reasoning_effort"], "max")
        self.assertNotIn("SYNTHETIC PRIVATE REASONING", self.persisted())

    def test_deepseek_thinking_disabled_sends_no_effort(self):
        sent, _, _ = self.sent(DEEPSEEK_ENDPOINT, openai_body(model="deepseek-flash"),
                               thinking=False)
        self.assertEqual(sent["thinking"], {"type": "disabled"})
        self.assertNotIn("reasoning_effort", sent)

    def test_thinking_controls_are_refused_for_other_families(self):
        client = self.provider(COMPAT_ENDPOINT)
        with mock.patch.object(compat, "_open") as opened:
            with self.assertRaises(ValueError):
                client.complete(MESSAGES, thinking=True)
        opened.assert_not_called()

    def test_no_thinking_control_is_sent_when_none_is_asked_for(self):
        sent, _, _ = self.sent(COMPAT_ENDPOINT, openai_body())
        self.assertNotIn("thinking", sent)
        self.assertNotIn("temperature", sent)
        self.assertNotIn("seed", sent)

    def test_deepseek_json_mode_requires_the_word_json_in_the_prompt(self):
        client = self.provider(DEEPSEEK_ENDPOINT)
        with mock.patch.object(compat, "_open") as opened:
            with self.assertRaises(ValueError):
                client.complete([{"role": "user", "content": "Reply with an object."}],
                                response_format={"type": "json_object"})
        opened.assert_not_called()
        self.assertEqual(client.calls, 0, "A refused call must not consume a call number")

    def test_extra_is_merged_into_the_payload(self):
        sent, _, _ = self.sent(NATIVE_ENDPOINT, native_body(), extra={"think": False})
        self.assertIs(sent["think"], False)


class ConcurrencyTests(Base):
    def test_two_providers_on_the_same_key_share_five_slots(self):
        peak = self.run_concurrent(
            [compat.Endpoint(name=f"test/shared-{i}", base_url="https://example.invalid/v1",
                             model="m", key_env="OLLAMA_API_KEY", family="f")
             for i in range(8)], expect_at_least=5)
        self.assertEqual(peak, 5, "Five concurrent requests per key, never a sixth")

    def test_different_keys_do_not_contend(self):
        endpoints = []
        for i in range(4):
            endpoints.append(compat.Endpoint(name=f"o-{i}", base_url="https://example.invalid/v1",
                                             model="m", key_env="OLLAMA_API_KEY", family="f"))
            endpoints.append(compat.Endpoint(name=f"d-{i}", base_url="https://example.invalid/v1",
                                             model="m", key_env="DEEPSEEK_API_KEY", family="deepseek"))
        peak = self.run_concurrent(endpoints, expect_at_least=8)
        self.assertEqual(peak, 8, "Two keys hold five slots each, so eight can be in flight")

    def test_a_second_ceiling_for_one_key_is_refused(self):
        compat.slots_for("OLLAMA_API_KEY", 5)
        with self.assertRaises(compat.ProviderFailure) as raised:
            compat.slots_for("OLLAMA_API_KEY", 2)
        self.assertEqual(raised.exception.code, "CONCURRENCY_LIMIT_CONFLICT")

    def test_registry_endpoints_all_declare_five_per_key(self):
        self.assertTrue(all(endpoint.max_concurrency == 5 for endpoint in compat.ENDPOINTS.values()))

    def run_concurrent(self, endpoints, *, expect_at_least):
        lock = threading.Lock()
        reached = threading.Event()
        release = threading.Event()
        count = {"active": 0, "peak": 0}

        class Blocking(Response):
            def read(self):
                with lock:
                    count["active"] += 1
                    count["peak"] = max(count["peak"], count["active"])
                    if count["active"] >= expect_at_least:
                        reached.set()
                try:
                    if not release.wait(10):
                        raise TimeoutError("Offline test barrier timed out")
                    return super().read()
                finally:
                    with lock:
                        count["active"] -= 1

        clients = [compat.OpenAICompatProvider(endpoint, self.root / endpoint.name)
                   for endpoint in endpoints]
        with mock.patch.object(compat, "_open",
                               side_effect=lambda *a, **k: Blocking(openai_body())):
            with ThreadPoolExecutor(max_workers=len(clients)) as pool:
                futures = [pool.submit(client.complete, copy.deepcopy(MESSAGES))
                           for client in clients]
                try:
                    self.assertTrue(reached.wait(10),
                                    f"{expect_at_least} calls should make concurrent progress")
                finally:
                    release.set()
                for future in futures:
                    self.assertEqual(future.result(timeout=10).status, "COMPLETE")
        return count["peak"]


class OfflineProviderTests(Base):
    def test_scripted_replies_are_recorded_like_live_ones(self):
        client = compat.OfflineProvider(COMPAT_ENDPOINT, self.root / "a", [
            {"content": '{"ok": true}',
             "usage": {"prompt_tokens": 3, "completion_tokens": 2, "total_tokens": 5}},
            "plain text answer",
        ])
        first = client.complete(MESSAGES, response_format={"type": "json_object"}, max_tokens=64)
        second = client.complete(MESSAGES)
        self.assertEqual((first.status, second.status), ("COMPLETE", "COMPLETE"))
        self.assertEqual(first.usage["completion_tokens"], 2)
        self.assertEqual(second.content, "plain text answer")
        self.assertEqual(len(self.requests()), 2)
        self.assertEqual(len(self.records()), 2)
        self.assertEqual(self.requests()[0]["schema_version"], "minireason.call.v2")
        self.assertTrue(self.requests()[0]["settings"]["offline"])
        self.assertEqual(client.prompt_tokens, 3)

    def test_offline_provider_opens_no_socket_even_without_a_key(self):
        with mock.patch.object(compat, "_open") as opened:
            with mock.patch.dict(os.environ, {}, clear=True):
                client = compat.OfflineProvider(COMPAT_ENDPOINT, self.root / "a", ["ok"])
                self.assertEqual(client.complete(MESSAGES).status, "COMPLETE")
        opened.assert_not_called()

    def test_offline_provider_still_refuses_a_credential_in_the_prompt(self):
        client = compat.OfflineProvider(COMPAT_ENDPOINT, self.root / "a", ["ok"])
        with self.assertRaises(compat.ProviderFailure) as raised:
            client.complete([{"role": "user", "content": OLLAMA_KEY}])
        self.assertEqual(raised.exception.code, "SECRET_IN_REQUEST")
        self.assertNoCredentials()

    def test_offline_status_machinery_matches_the_live_one(self):
        client = compat.OfflineProvider(COMPAT_ENDPOINT, self.root / "a",
                                        [{"content": "x", "finish_reason": "length"}])
        with self.assertRaises(compat.ProviderFailure) as raised:
            client.complete(MESSAGES)
        self.assertEqual(raised.exception.code, "INCOMPLETE_GENERATION")

    def test_exhausted_script_fails_loudly_with_a_record(self):
        client = compat.OfflineProvider(COMPAT_ENDPOINT, self.root / "a", [])
        with self.assertRaises(compat.ProviderFailure) as raised:
            client.complete(MESSAGES)
        self.assertEqual(raised.exception.code, "TRANSPORT_OR_RESPONSE_ERROR")
        self.assertEqual(len(self.records()), 1)

    def test_offline_provider_translates_native_payloads_too(self):
        client = compat.OfflineProvider(NATIVE_ENDPOINT, self.root / "a", ["ok"])
        client.complete(MESSAGES, response_format={"type": "json_object"}, max_tokens=32)
        self.assertEqual(self.requests()[0]["request"]["options"]["num_predict"], 32)
        self.assertEqual(self.requests()[0]["request"]["format"], "json")


class RegistryTests(Base):
    def test_endpoints_json_is_well_formed_as_shipped(self):
        # Asserted over the RAW JSON, before construction: Endpoint.__post_init__
        # already raises for a non-https base_url, a trailing slash and an
        # out-of-range timeout, so asserting those on constructed objects could
        # never fail. What is checked here is the shipped data itself.
        raw = json.loads(compat.ENDPOINTS_PATH.read_text())
        entries = raw["endpoints"]
        self.assertGreaterEqual(len(entries), 20)
        self.assertEqual(len({entry["name"] for entry in entries}), len(entries))
        for entry in entries:
            self.assertTrue(entry["base_url"].startswith("https://"), entry["name"])
            self.assertFalse(entry["base_url"].endswith("/"), entry["name"])
            self.assertIn(entry["key_env"], {"DEEPSEEK_API_KEY", "OLLAMA_API_KEY"})
            self.assertTrue(entry["family"])
            self.assertEqual(entry.get("max_concurrency", 5), 5, entry["name"])
            self.assertTrue(1 <= entry.get("timeout_seconds", 180) <= 600, entry["name"])
            self.assertEqual(entry.get("native", False),
                             entry.get("chat_path", "/chat/completions") == "/api/chat",
                             entry["name"])
        registry = compat.load_endpoints()
        self.assertEqual(sorted(registry), sorted(entry["name"] for entry in entries))

    def test_registry_declares_keys_by_env_name_only(self):
        raw = compat.ENDPOINTS_PATH.read_text()
        self.assertNotIn("sk-", raw)
        self.assertNotIn("Bearer", raw)
        for entry in json.loads(raw)["endpoints"]:
            self.assertEqual(set(entry) - {"chat_path", "native", "max_concurrency",
                                           "timeout_seconds"},
                             {"name", "base_url", "model", "key_env", "family"})

    def test_every_ollama_compat_endpoint_has_a_native_counterpart(self):
        registry = compat.ENDPOINTS
        compat_names = [name for name, endpoint in registry.items()
                        if endpoint.key_env == "OLLAMA_API_KEY" and not endpoint.native]
        self.assertTrue(compat_names)
        for name in compat_names:
            self.assertIn(name + ".native", registry)
            self.assertEqual(registry[name + ".native"].model, registry[name].model)

    def test_deepseek_entries_point_only_at_the_declared_destination(self):
        for endpoint in compat.ENDPOINTS.values():
            if endpoint.key_env == "DEEPSEEK_API_KEY":
                self.assertEqual(endpoint.base_url, "https://api.deepseek.com/v1")
                self.assertEqual(endpoint.family, "deepseek")

    def test_malformed_entries_are_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.json"
            path.write_text(json.dumps({"schema_version": "minireason.endpoints.v1", "endpoints": [
                {"name": "a", "base_url": "http://insecure.invalid", "model": "m",
                 "key_env": "OLLAMA_API_KEY", "family": "f"}]}))
            with self.assertRaises(ValueError):
                compat.load_endpoints(path)
            path2 = Path(temp) / "dup.json"
            entry = {"name": "a", "base_url": "https://x.invalid", "model": "m",
                     "key_env": "OLLAMA_API_KEY", "family": "f"}
            path2.write_text(json.dumps({"schema_version": "minireason.endpoints.v1",
                                         "endpoints": [entry, dict(entry)]}))
            with self.assertRaises(ValueError):
                compat.load_endpoints(path2)
            path3 = Path(temp) / "ver.json"
            path3.write_text(json.dumps({"schema_version": "other", "endpoints": []}))
            with self.assertRaises(ValueError):
                compat.load_endpoints(path3)

    def test_endpoint_is_frozen(self):
        with self.assertRaises(Exception):
            COMPAT_ENDPOINT.model = "other"  # type: ignore[misc]


class MiniAdapterTests(Base):
    def test_responder_mirrors_the_deepseek_mini_responder_interface(self):
        from creib.forge.mini.executor import Request
        from minireason import provider as deepseek_provider

        self.assertTrue(hasattr(deepseek_provider.MiniResponder, "reply"))
        responder = compat.responder_for(COMPAT_ENDPOINT, self.root / "a", {"max_tokens": 256})
        self.assertEqual(responder.completion_cap, 256)
        request = Request(stage_id="s1", kind_id="k1", attempt=0, brief="Do the thing.",
                          cycle=0, phase="body")
        with mock.patch.object(compat, "_open", return_value=Response(openai_body())) as opened:
            reply = responder.reply(request)
        self.assertEqual(reply.text, '{"ok": true}')
        self.assertEqual((reply.prompt_tokens, reply.completion_tokens), (11, 4))
        sent = json.loads(opened.call_args.args[0].data)
        self.assertEqual(sent["max_tokens"], 256)
        self.assertEqual(sent["response_format"], {"type": "json_object"})
        self.assertEqual(sent["messages"][1], {"role": "user", "content": "Do the thing."})
        self.assertIn("JSON object", sent["messages"][0]["content"])
        self.assertEqual(self.requests()[0]["coordinate"],
                         {"stage_id": "s1", "kind_id": "k1", "cycle": 0, "attempt": 0,
                          "phase": "body"})

    def test_responder_rejects_unknown_settings(self):
        with self.assertRaises(ValueError):
            compat.responder_for(COMPAT_ENDPOINT, self.root / "a", {"nonsense": 1})

    def test_responder_works_against_an_offline_provider(self):
        from creib.forge.mini.executor import Request

        offline = compat.OfflineProvider(NATIVE_ENDPOINT, self.root / "a", [
            {"content": '{"artifact": "x"}',
             "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}}])
        responder = compat.CompatMiniResponder(offline, {"max_tokens": 64})
        reply = responder.reply(Request(stage_id="s", kind_id="k", attempt=0, brief="b"))
        self.assertEqual(reply.text, '{"artifact": "x"}')


class NoNetworkTests(Base):
    def test_a_transport_that_bypassed_the_seam_would_still_not_dial_out(self):
        # The seam is NOT patched here: the call really goes through urllib, so
        # the connection guard is what stops it. Both connection classes are
        # guarded, because a proxy in the environment would route an https URL
        # through http.client.HTTPConnection.
        import http.client

        reached = []

        class Refuse(http.client.HTTPSConnection):
            # Subclassed, not replaced: urllib calls the class's own
            # _get_content_length before it constructs anything.
            def __init__(self, *args, **kwargs):
                reached.append(args[:1])
                raise AssertionError("A test tried to open a socket")

        with mock.patch.object(http.client, "HTTPSConnection", Refuse), \
                mock.patch.object(http.client, "HTTPConnection", Refuse):
            with self.assertRaises(compat.ProviderFailure) as raised:
                self.provider().complete(MESSAGES)
        self.assertTrue(reached, "the connection guard must be what stopped the call")
        self.assertEqual(raised.exception.code, "TRANSPORT_OR_RESPONSE_ERROR")
        self.assertIn("tried to open a socket", str(raised.exception))
        self.assertEqual(self.records()[0]["status"], "TRANSPORT_OR_RESPONSE_ERROR")


class ScrubTests(Base):
    def test_no_key_value_or_fragment_survives_a_full_exercise(self):
        client = self.provider()
        payload = openai_body(id=OLLAMA_KEY)
        with mock.patch.object(compat, "_open", return_value=Response(payload)):
            with self.assertRaises(compat.ProviderFailure):
                client.complete(MESSAGES)
        with mock.patch.object(compat, "_open", return_value=Response(openai_body())):
            client.complete(MESSAGES)
        with self.assertRaises(compat.ProviderFailure):
            client.complete([{"role": "system", "content": DEEPSEEK_KEY}])
        blob = self.persisted()
        self.assertTrue(blob)
        for secret in (OLLAMA_KEY, DEEPSEEK_KEY):
            for size in (6, 12, len(secret)):
                self.assertNotIn(secret[:size], blob)


class FailureRecordTests(Base):
    """A ProviderFailure's .record is a caller-facing surface: it is redacted."""

    def test_secret_in_request_failure_record_carries_no_key_fragment(self):
        client = self.provider()
        with mock.patch.object(compat, "_open") as opened:
            with self.assertRaises(compat.ProviderFailure) as raised:
                client.complete([{"role": "user", "content": "my key is " + OLLAMA_KEY}])
        opened.assert_not_called()
        failure = raised.exception
        self.assertEqual(failure.code, "SECRET_IN_REQUEST")
        blob = json.dumps(failure.record, ensure_ascii=False)
        self.assertIn("[REDACTED_CREDENTIAL]", blob, "the payload is still on the record")
        for secret in (OLLAMA_KEY, DEEPSEEK_KEY):
            for size in (6, 12, len(secret)):
                self.assertNotIn(secret[:size], blob)
                self.assertNotIn(secret[:size], str(failure))
        self.assertNoCredentials()

    def test_list_models_credential_echo_failure_record_carries_no_key_fragment(self):
        client = self.provider()
        body = {"data": [{"id": "m1"}], "leaked": OLLAMA_KEY}
        with mock.patch.object(compat, "_open", return_value=Response(body)):
            with self.assertRaises(compat.ProviderFailure) as raised:
                client.list_models()
        failure = raised.exception
        self.assertEqual(failure.code, "CREDENTIAL_ECHO")
        blob = json.dumps(failure.record, ensure_ascii=False)
        self.assertIn("models", failure.record)
        for secret in (OLLAMA_KEY, DEEPSEEK_KEY):
            for size in (6, 12, len(secret)):
                self.assertNotIn(secret[:size], blob)
        self.assertEqual(failure.record["models"]["leaked"], compat.REDACTION)
        self.assertNoCredentials()

    def test_chat_credential_echo_failure_record_carries_no_key_fragment(self):
        client = self.provider()
        with mock.patch.object(compat, "_open", return_value=Response(openai_body(id=OLLAMA_KEY))):
            with self.assertRaises(compat.ProviderFailure) as raised:
                client.complete(MESSAGES)
        blob = json.dumps(raised.exception.record, ensure_ascii=False)
        for size in (6, 12, len(OLLAMA_KEY)):
            self.assertNotIn(OLLAMA_KEY[:size], blob)

    def test_a_failure_raised_inside_a_normaliser_still_carries_the_closed_record(self):
        client = self.provider()
        with mock.patch.object(compat, "_open", return_value=Response(openai_body(choices=[]))):
            with self.assertRaises(compat.ProviderFailure) as raised:
                client.complete(MESSAGES)
        failure = raised.exception
        self.assertEqual(failure.code, "TRANSPORT_OR_RESPONSE_ERROR")
        self.assertIsNotNone(failure.record, "every failure of this module carries its record")
        self.assertEqual(failure.record["status"], "TRANSPORT_OR_RESPONSE_ERROR")
        self.assertIn("elapsed_ms", failure.record)
        self.assertEqual(failure.record["request_sha256"], self.records()[0]["request_sha256"])


class RedactionScopeTests(Base):
    def test_a_json_escaped_key_is_redacted_too(self):
        awkward = 'abc"def\\ghijklmnop'
        with mock.patch.dict(os.environ, {"WEIRD_API_KEY": awkward}):
            compat.register_secret_envs(["WEIRD_API_KEY"])
            encoded = json.dumps({"k": awkward})
            self.assertIn('abc\\"def', encoded, "the fixture really is escaped by json")
            cleaned = compat.redact(encoded)
        self.assertNotIn("abc", cleaned)
        self.assertEqual(json.loads(cleaned)["k"], compat.REDACTION)

    def test_redaction_names_the_env_vars_whose_values_it_replaced(self):
        path = self.root / "a" / "named.json"
        compat.write_new(path, {"note": "value is " + OLLAMA_KEY})
        written = json.loads(path.read_text())
        self.assertEqual(written["note"], "value is [REDACTED_CREDENTIAL]")
        self.assertEqual(written["credentials_redacted"], ["OLLAMA_API_KEY"])

    def test_a_record_with_no_credential_in_it_names_none(self):
        with mock.patch.object(compat, "_open", return_value=Response(openai_body())):
            self.provider().complete(MESSAGES)
        self.assertNotIn("credentials_redacted", self.records()[0])

    def test_the_secret_set_is_declared_not_discovered_by_name_shape(self):
        # An unrelated *_API_KEY holding an ordinary word used to refuse a
        # legitimate prompt and rewrite record content. The set is now the
        # registry's key_envs plus the always-secret names plus whatever a
        # caller registered.
        with mock.patch.dict(os.environ, {"INTERNAL_API_KEY": "reasoning-about-json"}):
            self.assertNotIn("INTERNAL_API_KEY", compat._secret_env_names())
            self.assertEqual(compat.redact("the reasoning-about-json was sound"),
                             "the reasoning-about-json was sound")
            client = compat.OfflineProvider(COMPAT_ENDPOINT, self.root / "a", ["ok"])
            self.assertEqual(
                client.complete([{"role": "user", "content": "reasoning-about-json"}]).status,
                "COMPLETE")
            # ... and a caller that declares the name gets it covered.
            compat.register_secret_envs(["INTERNAL_API_KEY"])
            self.assertIn("INTERNAL_API_KEY", compat._secret_env_names())
            self.assertEqual(compat.registered_secret_envs(), ("INTERNAL_API_KEY",))
            second = compat.OfflineProvider(COMPAT_ENDPOINT, self.root / "b", ["ok"])
            with self.assertRaises(compat.ProviderFailure) as raised:
                second.complete([{"role": "user", "content": "reasoning-about-json"}])
            self.assertEqual(raised.exception.code, "SECRET_IN_REQUEST")

    def test_a_value_under_the_documented_floor_is_not_a_secret(self):
        with mock.patch.dict(os.environ, {"SHORT_API_KEY": "abc123"}):
            compat.register_secret_envs(["SHORT_API_KEY"])
            self.assertEqual(compat.redact("value abc123"), "value abc123")
        self.assertEqual(compat._MIN_SECRET_LENGTH, 8)


class ThinkingModeTests(Base):
    def test_reasoning_text_where_thinking_was_disabled_is_a_mismatch(self):
        client = self.provider(DEEPSEEK_ENDPOINT)
        payload = openai_body(model="deepseek-flash")
        payload["choices"][0]["message"]["reasoning_content"] = "SYNTHETIC PRIVATE REASONING"
        with mock.patch.object(compat, "_open", return_value=Response(payload)):
            with self.assertRaises(compat.ProviderFailure) as raised:
                client.complete(MESSAGES, thinking=False)
        self.assertEqual(raised.exception.code, "THINKING_MODE_MISMATCH")
        record = self.records()[0]
        self.assertEqual(record["status"], "THINKING_MODE_MISMATCH")
        self.assertTrue(record["reasoning_content_present"])
        self.assertIs(record["settings"]["thinking"], False)
        self.assertNotIn("SYNTHETIC PRIVATE REASONING", self.persisted())

    def test_no_reasoning_text_where_thinking_was_enabled_is_a_mismatch(self):
        client = self.provider(DEEPSEEK_ENDPOINT)
        with mock.patch.object(compat, "_open",
                               return_value=Response(openai_body(model="deepseek-flash"))):
            with self.assertRaises(compat.ProviderFailure) as raised:
                client.complete(MESSAGES, thinking=True)
        self.assertEqual(raised.exception.code, "THINKING_MODE_MISMATCH")

    def test_a_matching_answer_is_complete(self):
        client = self.provider(DEEPSEEK_ENDPOINT)
        with mock.patch.object(compat, "_open",
                               return_value=Response(openai_body(model="deepseek-flash"))):
            self.assertEqual(client.complete(MESSAGES, thinking=False).status, "COMPLETE")

    def test_the_check_is_deepseek_only_and_needs_a_requested_value(self):
        # No thinking control was sent, so there is nothing to verify; and the
        # control is refused outright for a non-deepseek family.
        payload = openai_body()
        payload["choices"][0]["message"]["reasoning_content"] = "SYNTHETIC PRIVATE REASONING"
        with mock.patch.object(compat, "_open", return_value=Response(payload)):
            self.assertEqual(self.provider().complete(MESSAGES).status, "COMPLETE")

    def test_the_responder_defaults_deepseek_thinking_to_disabled(self):
        from creib.forge.mini.executor import Request

        responder = compat.responder_for(DEEPSEEK_ENDPOINT, self.root / "a", {"max_tokens": 64})
        self.assertIs(responder.settings["thinking"], False)
        request = Request(stage_id="s1", kind_id="k1", attempt=0,
                          brief="Do the thing, return json.", cycle=0, phase="body")
        with mock.patch.object(compat, "_open",
                               return_value=Response(openai_body(model="deepseek-flash"))) as opened:
            responder.reply(request)
        sent = json.loads(opened.call_args.args[0].data)
        self.assertEqual(sent["thinking"], {"type": "disabled"},
                         "provider.MiniResponder always disables thinking on the DeepSeek arm")

    def test_the_responder_sends_no_thinking_control_to_another_family(self):
        responder = compat.responder_for(COMPAT_ENDPOINT, self.root / "a", {"max_tokens": 64})
        self.assertNotIn("thinking", responder.settings)


class ExtraArgumentTests(Base):
    def test_extra_may_not_override_a_key_this_module_builds(self):
        client = self.provider()
        with mock.patch.object(compat, "_open") as opened:
            with self.assertRaises(ValueError) as raised:
                client.complete(MESSAGES, max_tokens=64, extra={"max_tokens": 1, "stream": True})
        opened.assert_not_called()
        self.assertIn("max_tokens", str(raised.exception))
        self.assertEqual(client.calls, 0, "A refused call must not consume a call number")
        self.assertEqual(list((self.root / "a").glob("*")) if (self.root / "a").exists() else [], [])

    def test_native_extra_options_is_deep_merged_and_keeps_the_ceiling(self):
        client = self.provider(NATIVE_ENDPOINT)
        with mock.patch.object(compat, "_open",
                               return_value=Response(native_body())) as opened:
            client.complete(MESSAGES, max_tokens=64,
                            extra={"options": {"temperature": 1.0}})
        sent = json.loads(opened.call_args.args[0].data)
        self.assertEqual(sent["options"], {"num_predict": 64, "temperature": 1.0})
        record = self.records()[0]
        self.assertEqual(record["settings"]["max_tokens"], 64)
        self.assertEqual(record["request"]["options"]["num_predict"], 64,
                         "the record and the wire must agree about the ceiling")

    def test_native_extra_options_must_be_a_mapping(self):
        client = self.provider(NATIVE_ENDPOINT)
        with self.assertRaises(ValueError):
            client.complete(MESSAGES, extra={"options": [1, 2]})

    def test_a_non_colliding_extra_key_still_passes_through(self):
        client = self.provider(NATIVE_ENDPOINT)
        with mock.patch.object(compat, "_open",
                               return_value=Response(native_body())) as opened:
            client.complete(MESSAGES, extra={"think": False})
        self.assertIs(json.loads(opened.call_args.args[0].data)["think"], False)

    def test_offline_and_live_refuse_exactly_the_same_arguments(self):
        live = self.provider()
        offline = compat.OfflineProvider(COMPAT_ENDPOINT, self.root / "b", ["ok", "ok", "ok"])
        bad = [
            {"reasoning_effort": "medium"},
            {"max_tokens": 0},
            {"max_tokens": "64"},
            {"extra": {"model": "other"}},
        ]
        for call in bad:
            with mock.patch.object(compat, "_open") as opened:
                with self.assertRaises(ValueError, msg=call):
                    live.complete(MESSAGES, **call)
                with self.assertRaises(ValueError, msg=call):
                    offline.complete(MESSAGES, **call)
            opened.assert_not_called()
        self.assertEqual((live.calls, offline.calls), (0, 0))


class NativeUsageTests(Base):
    def test_a_prompt_cache_hit_normalises_the_missing_prompt_count(self):
        body = native_body()
        del body["prompt_eval_count"]
        with mock.patch.object(compat, "_open", return_value=Response(body)):
            result = self.provider(NATIVE_ENDPOINT).complete(MESSAGES)
        self.assertEqual(result.status, "COMPLETE", "a finished answer is not a usage failure")
        self.assertEqual(result.content, '{"ok": true}')
        self.assertEqual(result.usage, {"prompt_tokens": 0, "completion_tokens": 4,
                                        "total_tokens": 4})
        record = self.records()[0]
        self.assertEqual(record["usage_source"], "native-normalised",
                         "the record must not claim a provider-reported prompt count")
        self.assertEqual(record["status"], "COMPLETE")

    def test_a_provider_reported_usage_says_so(self):
        with mock.patch.object(compat, "_open", return_value=Response(native_body())):
            self.provider(NATIVE_ENDPOINT).complete(MESSAGES)
        self.assertEqual(self.records()[0]["usage_source"], "provider-reported")

    def test_a_missing_completion_count_is_still_usage_unavailable(self):
        body = native_body()
        del body["eval_count"]
        with mock.patch.object(compat, "_open", return_value=Response(body)):
            with self.assertRaises(compat.ProviderFailure) as raised:
                self.provider(NATIVE_ENDPOINT).complete(MESSAGES)
        self.assertEqual(raised.exception.code, "USAGE_UNAVAILABLE")


class ListModelsTests(Base):
    """list_models spent six live calls in the recorded smoke and had no test."""

    def test_a_model_list_is_recorded_like_a_chat_call(self):
        client = self.provider()
        body = {"object": "list", "data": [{"id": "m2"}, {"id": "m1"}]}
        with mock.patch.object(compat, "_open", return_value=Response(body)) as opened:
            record = client.list_models(coordinate={"stage_id": "s1"})
        request = opened.call_args.args[0]
        self.assertEqual(request.get_method(), "GET")
        self.assertEqual(request.full_url, "https://example.invalid/v1/models")
        self.assertEqual(request.get_header("Authorization"), "Bearer " + OLLAMA_KEY)
        self.assertEqual(record["status"], "COMPLETE")
        self.assertEqual(record["models"], body)
        written = self.records()[0]
        self.assertEqual(written["status"], "COMPLETE")
        self.assertEqual(written["request_header_names"], ["Accept", "Authorization"])
        self.assertEqual(written["request"], {"method": "GET", "path": "/models"})
        self.assertEqual(written["settings"]["operation"], "list_models")
        self.assertEqual(written["coordinate"], {"stage_id": "s1"})
        self.assertIsNone(self.requests()[0]["request_bytes_sha256"])
        self.assertNoCredentials()

    def test_an_echoed_credential_in_a_model_list_is_a_loud_failure(self):
        client = self.provider()
        with mock.patch.object(compat, "_open",
                               return_value=Response({"data": [], "leaked": OLLAMA_KEY})):
            with self.assertRaises(compat.ProviderFailure) as raised:
                client.list_models()
        self.assertEqual(raised.exception.code, "CREDENTIAL_ECHO")
        written = self.records()[0]
        self.assertEqual(written["status"], "CREDENTIAL_ECHO")
        self.assertTrue(written["credential_redaction"])
        self.assertEqual(written["models"]["leaked"], compat.REDACTION)
        self.assertEqual(written["credentials_redacted"], ["OLLAMA_API_KEY"])
        self.assertNoCredentials()

    def test_a_redirect_refusal_is_recorded_as_http_307_and_never_retried(self):
        client = self.provider()
        error = urllib.error.HTTPError("https://example.invalid/v1/models", 307,
                                       "Temporary Redirect", {},
                                       io.BytesIO(b"moved; key=" + OLLAMA_KEY.encode()))
        with mock.patch.object(compat, "_open", side_effect=error) as opened:
            with self.assertRaises(compat.ProviderFailure) as raised:
                client.list_models()
        self.assertEqual(raised.exception.code, "HTTP_307")
        self.assertEqual(opened.call_count, 1, "No automatic retry")
        self.assertEqual(self.records()[0]["status"], "HTTP_307")
        self.assertNotIn(OLLAMA_KEY, str(raised.exception))
        self.assertNoCredentials()

    def test_a_missing_key_is_recorded_before_any_request(self):
        client = self.provider()
        with mock.patch.object(compat, "_open") as opened:
            with mock.patch.dict(os.environ, {"OLLAMA_API_KEY": ""}):
                with self.assertRaises(compat.ProviderFailure) as raised:
                    client.list_models()
        opened.assert_not_called()
        self.assertEqual(raised.exception.code, "KEY_MISSING")
        self.assertEqual(self.records()[0]["status"], "KEY_MISSING")


class OfflineRecordShapeTests(Base):
    def test_an_offline_record_names_the_request_it_did_not_make(self):
        client = compat.OfflineProvider(COMPAT_ENDPOINT, self.root / "a", ["ok"])
        client.complete(MESSAGES, max_tokens=64)
        written = self.requests()[0]
        self.assertIsNone(written["url"])
        self.assertEqual(written["not_contacted_url"],
                         "https://example.invalid/v1/chat/completions")
        self.assertEqual(written["request_header_names"], [],
                         "no header was formed, so none may be recorded")
        self.assertNotIn("Authorization", json.dumps(written))
        self.assertNotIn("request_bytes", written)
        self.assertNotIn("request_bytes_sha256", written)
        self.assertGreater(written["would_send_bytes"], 0)
        self.assertEqual(len(written["would_send_bytes_sha256"]), 64)
        self.assertTrue(written["settings"]["offline"])

    def test_the_live_record_still_names_the_request_it_did_make(self):
        with mock.patch.object(compat, "_open", return_value=Response(openai_body())):
            self.provider().complete(MESSAGES)
        written = self.requests()[0]
        self.assertEqual(written["url"], "https://example.invalid/v1/chat/completions")
        self.assertNotIn("not_contacted_url", written)
        self.assertEqual(written["request_header_names"],
                         ["Accept", "Authorization", "Content-Type"])


class RecordCollisionTests(Base):
    def test_a_second_provider_on_one_records_dir_fails_as_a_provider_failure(self):
        # A bare FileExistsError escapes every `except ProviderFailure` a caller
        # wrote, and does so after the call has already been spent.
        first = self.provider(sub="shared")
        second = self.provider(sub="shared")
        with mock.patch.object(compat, "_open", return_value=Response(openai_body())):
            self.assertEqual(first.complete(MESSAGES).status, "COMPLETE")
            with self.assertRaises(compat.ProviderFailure) as raised:
                second.complete(MESSAGES)
        self.assertEqual(raised.exception.code, "RECORD_EXISTS")
        self.assertIn("write-once", str(raised.exception))

    def test_the_smoke_tool_gives_every_probe_its_own_records_directory(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
        try:
            import provider_smoke
        finally:
            sys.path.pop(0)
        root = self.root / "run"
        first = provider_smoke.records_dir_for(root, COMPAT_ENDPOINT, "compat")
        headroom = provider_smoke.records_dir_for(root, COMPAT_ENDPOINT, "headroom-512")
        self.assertNotEqual(first, headroom)
        self.assertEqual(first.parent, headroom.parent)

    def test_the_smoke_tool_registers_the_names_its_env_file_loaded(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
        try:
            import provider_smoke
        finally:
            sys.path.pop(0)
        env_file = self.root / "env"
        env_file.write_text("# comment\nOLLAMA_TOKEN=not-a-real-credential-value\n")
        with mock.patch.dict(os.environ, {}, clear=False):
            names = provider_smoke.load_env_file(env_file)
            self.assertEqual(names, ["OLLAMA_TOKEN"])
            self.assertIn("OLLAMA_TOKEN", compat._secret_env_names())
            self.assertEqual(compat.redact("x not-a-real-credential-value y"),
                             "x [REDACTED_CREDENTIAL] y")
            del os.environ["OLLAMA_TOKEN"]



if __name__ == "__main__":
    unittest.main()
