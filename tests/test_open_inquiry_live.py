"""Offline live-responder regressions; no provider or socket is used."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest
import uuid
from unittest import mock

from creib.forge.mini.executor import Request
from creib.forge.mini.manifest import compile_manifest
from minireason import provider_openai_compat as provider
from minireason.open_inquiry import (
    ExecutionEnvelope, install_source_bridge, make_manifest, run_open_inquiry,
)
from minireason.open_inquiry_live import (
    LiveResponder,
    TextAdapter,
    load_env_file,
    validate_plan,
    verify_forge_storage,
)
from minireason.reason.types import ReasonFailure


ROOT = Path(__file__).resolve().parents[1]
SHORT_TEMP = Path(r"C:\tw13") if os.name == "nt" else Path(tempfile.gettempdir())
ENDPOINT = "deepseek-flash"
NATIVE_ENDPOINT = "ollama/qwen3.5-397b.native"


def _read_text(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return handle.read()


def _read_json(path: Path):
    return json.loads(_read_text(path))


def _write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def _write_manifest(path: Path, manifest: dict):
    _write_text(path, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return path


def _diagnostic_file_publish(path: Path, data: bytes):
    """Test seam only: exclusive file fsync, without Forge directory fsync."""
    text = data.decode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())


class ScriptedTextAdapter(TextAdapter):
    def __init__(self, responses):
        super().__init__(mode="offline")
        self.responses = iter(responses)
        self.calls = []

    def call(self, **kwargs):
        self.calls.append(kwargs)
        return super().call(scripted=next(self.responses), **kwargs)


class ReturningTextAdapter(TextAdapter):
    def __init__(self, result=None, failure=None):
        super().__init__(mode="offline")
        self.result = result
        self.failure = failure
        self.calls = []

    def call(self, **kwargs):
        self.calls.append(kwargs)
        if self.failure is not None:
            raise self.failure
        return self.result


class OpenInquiryLiveTests(unittest.TestCase):
    def setUp(self):
        install_source_bridge()
        SHORT_TEMP.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=SHORT_TEMP)
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        for patcher in (
            mock.patch.object(
                provider, "_open",
                side_effect=AssertionError("Network access forbidden in live-responder tests"),
            ),
            mock.patch.object(
                provider.OpenAICompatProvider, "__init__",
                side_effect=AssertionError("Live provider construction forbidden"),
            ),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def _request(self, *, cycle=1, stage="conjecture", kind="open.kind", attempt=0, phase="both"):
        return Request(
            stage_id=stage,
            kind_id=kind,
            attempt=attempt,
            brief="Exact public Forge prompt.",
            cycle=cycle,
            phase=phase,
            optional_fields=(),
        )

    def _compile(self, manifest: dict, name="manifest.json"):
        return compile_manifest(_write_manifest(self.base / name, manifest))

    def test_text_adapter_keeps_exact_prompt_and_caps_both_wire_shapes(self):
        messages = [{"role": "user", "content": "Exact raw public prompt."}]
        for endpoint, expected_key in (
            (ENDPOINT, "max_tokens"),
            (NATIVE_ENDPOINT, "num_predict"),
        ):
            with self.subTest(endpoint=endpoint):
                records = self.base / endpoint.replace("/", "_")
                adapter = TextAdapter(mode="offline")
                result = adapter.call(
                    seat=endpoint,
                    messages=messages,
                    records_dir=records,
                    max_tokens=37,
                    thinking="off",
                    role="conjecture",
                    coordinate={"cycle": 1, "stage_id": "conjecture"},
                    scripted={
                        "content": "Public reply.",
                        "usage": {
                            "prompt_tokens": 5,
                            "completion_tokens": 6,
                            "total_tokens": 11,
                        },
                    },
                )
                self.assertEqual(result["content"], "Public reply.")
                request = _read_json(records / "call-0001.request.json")
                wire = json.loads(request["wire_body_text"])
                self.assertEqual(wire["messages"], messages)
                self.assertNotIn("response_format", wire)
                self.assertNotIn("format", wire)
                if expected_key == "max_tokens":
                    self.assertEqual(wire["max_tokens"], 37)
                else:
                    self.assertEqual(wire["options"]["num_predict"], 37)
                self.assertEqual(request["settings"]["max_tokens"], 37)

    def test_two_cycle_critical_return_uses_real_forge_with_labelled_storage_seam(self):
        cap = 13
        manifest = make_manifest(
            "critical_return",
            [],
            ExecutionEnvelope(
                max_cycles=2,
                max_calls=8,
                max_completion_tokens=cap * 8,
                completion_tokens_per_call=cap,
            ),
        )
        plan = self._compile(manifest)
        responses = [
            {
                "content": f"PUBLIC-CALL-{index}",
                "usage": {
                    "prompt_tokens": 20 + index,
                    "completion_tokens": 7,
                    "total_tokens": 27 + index,
                },
            }
            for index in range(1, 9)
        ]
        run_root = self.base / "r"
        adapter = ScriptedTextAdapter(responses)
        responder = LiveResponder(ENDPOINT, run_root, cap, "off", adapter)
        with mock.patch(
            "creib.forge.mini.log.publish_no_clobber",
            side_effect=_diagnostic_file_publish,
        ):
            outcome = run_open_inquiry(
                plan,
                run_root,
                responder,
                responder_id=responder.responder_id,
            )

        self.assertEqual(outcome.stop_reason, "cycle_cap")
        self.assertEqual(outcome.cycles_completed, 2)
        self.assertEqual(outcome.calls, 8)
        self.assertEqual(outcome.completion_tokens, 56)
        self.assertEqual(len(adapter.calls), 8)
        self.assertEqual(
            [(item["coordinate"]["cycle"], item["coordinate"]["stage_id"]) for item in adapter.calls],
            [
                (1, "conjecture"),
                (1, "criticise"),
                (1, "return"),
                (1, "continue"),
                (2, "conjecture"),
                (2, "criticise"),
                (2, "return"),
                (2, "continue"),
            ],
        )
        self.assertEqual(responder.endpoint.to_dict()["name"], ENDPOINT)
        for index, call in enumerate(adapter.calls, 1):
            directory = run_root / "provider" / f"{index:06d}"
            request = _read_json(directory / "forge-request.json")
            response = _read_json(directory / "forge-response.json")
            transport_request = _read_json(directory / "transport" / "call-0001.request.json")
            transport_response = _read_json(directory / "transport" / "call-0001.response.json")
            exact_prompt = request["forge_request"]["brief"]
            self.assertEqual(call["messages"], [{"role": "user", "content": exact_prompt}])
            self.assertEqual(json.loads(transport_request["wire_body_text"])["messages"], call["messages"])
            self.assertIsInstance(request["started_epoch"], (int, float))
            self.assertEqual(request["wall_seconds"], 300)
            self.assertEqual(request["transport_retries"], 0)
            self.assertEqual(request["endpoint"]["timeout_seconds"], 300)
            self.assertIsInstance(response["finished_epoch"], (int, float))
            self.assertIsInstance(transport_request["recorded_epoch"], (int, float))
            self.assertIsInstance(transport_response["recorded_epoch"], (int, float))
            self.assertEqual(response["status"], "COMPLETE")
            self.assertEqual(response["content"], f"PUBLIC-CALL-{index}")
            self.assertEqual(response["usage"]["completion_tokens"], 7)
            self.assertEqual(transport_response["status"], "COMPLETE")
            self.assertFalse(response["native_reasoning_text_persisted"])

    def test_full_forge_failure_records_both_custody_layers_without_run_end(self):
        cap = 9
        plan = self._compile(
            make_manifest(
                "open_turn",
                [],
                ExecutionEnvelope(1, 2, cap * 2, cap),
            ),
            "failure-manifest.json",
        )
        run_root = self.base / "failed-run"
        adapter = ScriptedTextAdapter([
            {
                "content": "Public length-stopped prefix.",
                "finish_reason": "length",
                "usage": {
                    "prompt_tokens": 4,
                    "completion_tokens": cap,
                    "total_tokens": cap + 4,
                },
            }
        ])
        responder = LiveResponder(ENDPOINT, run_root, cap, "off", adapter)
        with mock.patch(
            "creib.forge.mini.log.publish_no_clobber",
            side_effect=_diagnostic_file_publish,
        ):
            with self.assertRaises(ReasonFailure) as caught:
                run_open_inquiry(
                    plan,
                    run_root,
                    responder,
                    responder_id=responder.responder_id,
                )
        self.assertEqual(caught.exception.code, "CEILING_HIT")
        self.assertEqual(len(adapter.calls), 1)
        provider_failure = _read_json(
            run_root / "provider/000001/forge-response.json"
        )
        delegate_failure = _read_json(
            run_root / "verbatim-transport/000001.json"
        )
        self.assertEqual(provider_failure["status"], "provider-exception")
        self.assertEqual(provider_failure["code"], "CEILING_HIT")
        self.assertEqual(delegate_failure["status"], "delegate-raised")
        self.assertEqual(delegate_failure["exception_type"], "ReasonFailure")
        events = [
            json.loads(line)
            for line in _read_text(run_root / "log.jsonl").splitlines()
            if line.strip()
        ]
        self.assertNotIn("RUN_ENDED", [event["type"] for event in events])
        self.assertFalse((run_root / "provider/000002").exists())

    def test_completion_cap_and_usage_fail_closed(self):
        for result, expected in (
            (
                {
                    "content": "Public overrun.",
                    "usage": {"prompt_tokens": 3, "completion_tokens": 12},
                },
                "COMPLETION_CEILING_VIOLATED",
            ),
            (
                {
                    "content": "Public reply with unknown prompt usage.",
                    "usage": {"completion_tokens": 2},
                },
                "USAGE_UNAVAILABLE",
            ),
        ):
            with self.subTest(expected=expected):
                root = self.base / expected.lower()
                adapter = ReturningTextAdapter(result=result)
                responder = LiveResponder(ENDPOINT, root, 11, "off", adapter)
                with self.assertRaises(ReasonFailure) as caught:
                    responder.reply(self._request())
                self.assertEqual(caught.exception.code, expected)
                custody = _read_json(root / "provider/000001/forge-response.json")
                self.assertEqual(custody["status"], "provider-exception")
                self.assertEqual(custody["code"], expected)
                self.assertEqual(len(adapter.calls), 1)

        for invalid in (None, 0, -1, True, "11"):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    LiveResponder(ENDPOINT, self.base / ("invalid-" + uuid.uuid4().hex[:6]), invalid)

    def test_transport_failure_is_recorded_without_detail_and_never_retried(self):
        root = self.base / "failure"
        adapter = ScriptedTextAdapter([
            {
                "content": "Public length-stopped prefix.",
                "finish_reason": "length",
                "usage": {
                    "prompt_tokens": 4,
                    "completion_tokens": 9,
                    "total_tokens": 13,
                },
            }
        ])
        responder = LiveResponder(ENDPOINT, root, 9, "off", adapter)
        request = self._request()
        with self.assertRaises(ReasonFailure) as caught:
            responder.reply(request)
        self.assertEqual(caught.exception.code, "CEILING_HIT")
        self.assertEqual(len(adapter.calls), 1)
        response_path = root / "provider/000001/forge-response.json"
        response_text = _read_text(response_path)
        response = json.loads(response_text)
        self.assertEqual(response["status"], "provider-exception")
        self.assertEqual(response["code"], "CEILING_HIT")
        self.assertNotIn("detail", response)
        self.assertTrue((root / "provider/000001/transport/call-0001.response.json").exists())
        with self.assertRaises(ReasonFailure) as replay:
            responder.reply(request)
        self.assertEqual(replay.exception.code, "NO_REPLAY")
        self.assertEqual(len(adapter.calls), 1)
        self.assertFalse((root / "provider/000002").exists())

    def test_private_exception_text_is_not_persisted(self):
        root = self.base / "safe-failure"
        adapter = ReturningTextAdapter(
            failure=ReasonFailure(
                "TRANSPORT_OR_RESPONSE_ERROR",
                "dummy private transport detail must not persist",
            )
        )
        responder = LiveResponder(ENDPOINT, root, 11, "off", adapter)
        with self.assertRaises(ReasonFailure):
            responder.reply(self._request())
        text = _read_text(root / "provider/000001/forge-response.json")
        self.assertNotIn("dummy private transport detail", text)
        self.assertEqual(json.loads(text)["code"], "TRANSPORT_OR_RESPONSE_ERROR")
        self.assertEqual(len(adapter.calls), 1)

    def test_non_single_coordinates_are_refused_before_dispatch(self):
        adapter = ReturningTextAdapter(
            result={
                "content": "Unused.",
                "usage": {"prompt_tokens": 1, "completion_tokens": 1},
            }
        )
        responder = LiveResponder(ENDPOINT, self.base / "coordinates", 5, "off", adapter)
        for request in (
            self._request(attempt=1),
            self._request(phase="body"),
        ):
            with self.subTest(attempt=request.attempt, phase=request.phase):
                with self.assertRaises(ValueError):
                    responder.reply(request)
        self.assertEqual(adapter.calls, [])
        self.assertFalse((self.base / "coordinates/provider").exists())

    def test_validate_plan_requires_finite_caps_zero_retries_and_single_call(self):
        good = make_manifest(
            "critical_return",
            [],
            ExecutionEnvelope(2, 8, 80, 10),
        )
        self.assertEqual(validate_plan(self._compile(good, "good.json")), 10)

        missing = make_manifest("critical_return", [], ExecutionEnvelope(2))
        with self.assertRaises(ValueError):
            validate_plan(self._compile(missing, "missing.json"))

        retry = make_manifest(
            "critical_return",
            [],
            ExecutionEnvelope(2, 8, 80, 10),
        )
        retry["kinds"][1]["failure_policy"]["retries"] = 1
        with self.assertRaises(ValueError):
            validate_plan(self._compile(retry, "retry.json"))

        split = make_manifest(
            "critical_return",
            [],
            ExecutionEnvelope(2, 8, 80, 10),
        )
        split["kinds"][1]["commitment_call"] = "two"
        with self.assertRaises(ValueError):
            validate_plan(self._compile(split, "split.json"))

    def test_actual_forge_storage_probe_refuses_windows_or_passes_unchanged(self):
        root = self.base / "storage"
        if os.name == "nt":
            with self.assertRaises(ReasonFailure) as caught:
                verify_forge_storage(root)
            self.assertEqual(caught.exception.code, "TARGET_FILESYSTEM_DURABILITY_UNAVAILABLE")
            receipt = _read_json(root / "durability.json")
            self.assertEqual(receipt["status"], "TARGET_FILESYSTEM_DURABILITY_UNAVAILABLE")
            self.assertEqual(receipt["provider_calls"], 0)
        else:
            verify_forge_storage(root)
            receipt = _read_json(root / "durability.json")
            self.assertEqual(receipt["status"], "passed")
            self.assertEqual(receipt["provider_calls"], 0)
            self.assertTrue((root / "durability-probe/probe.txt").exists())


class EnvironmentFileTests(unittest.TestCase):
    def setUp(self):
        self.directory = ROOT / "work/w13/live-env-fixtures" / uuid.uuid4().hex[:8]
        self.directory.mkdir(parents=True, exist_ok=False)
        self.environment = {"EXISTING_NAME": "dummy-existing"}
        self.environment_patch = mock.patch.object(os, "environ", self.environment)
        self.environment_patch.start()
        self.addCleanup(self.environment_patch.stop)

    def _fixture(self, text: str):
        path = self.directory / "dummy.env"
        _write_text(path, text)
        return path

    def test_only_two_dummy_provider_names_are_loaded(self):
        path = self._fixture(
            "# dummy fixture values only\r\n"
            "DEEPSEEK_API_KEY=dummy-deepseek\r\n"
            "OLLAMA_API_KEY='dummy-ollama=value'\r\n"
        )
        load_env_file(path)
        self.assertEqual(
            self.environment,
            {
                "EXISTING_NAME": "dummy-existing",
                "DEEPSEEK_API_KEY": "dummy-deepseek",
                "OLLAMA_API_KEY": "dummy-ollama=value",
            },
        )

    def test_invalid_name_is_transactionally_refused_without_value_disclosure(self):
        path = self._fixture(
            "DEEPSEEK_API_KEY=dummy-first\n"
            "UNADMITTED_KEY=dummy-private-value\n"
        )
        before = dict(self.environment)
        with self.assertRaises(ReasonFailure) as caught:
            load_env_file(path)
        self.assertEqual(caught.exception.code, "ENV_FILE_KEY_NOT_ALLOWED")
        self.assertEqual(self.environment, before)
        self.assertNotIn("dummy", str(caught.exception))
        self.assertNotIn("UNADMITTED_KEY", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
