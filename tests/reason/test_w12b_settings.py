"""Offline regressions for per-seat completion ceilings and reasoning effort."""
from pathlib import Path
import json
import os
import unittest
import uuid
from unittest import mock

from minireason import provider_openai_compat as provider
from minireason.reason import adapter, config
from minireason.reason.types import ReasonFailure

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "work/review12b/settings/fixtures"
MESSAGES = [{"role": "user", "content": "Return JSON for this public fixture problem."}]


def read_json(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return json.load(handle)


class PerSeatSettingsTests(unittest.TestCase):
    def setUp(self):
        self.case = ARTIFACTS / uuid.uuid4().hex[:8]
        self.case.mkdir(parents=True)
        for patcher in (
            mock.patch.object(os, "environ", {}),
            mock.patch.object(provider.OpenAICompatProvider, "__init__",
                              side_effect=AssertionError("Live provider forbidden")),
            mock.patch.object(provider, "_open", side_effect=AssertionError("Network forbidden")),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_shipped_per_mode_ceilings_reach_provider_wire(self):
        recipe = config.load_recipe("cross-family")["data"]
        for name, thinking, ceiling in (
            ("deepseek-flash", "native", 32768),
            ("deepseek-flash", "off", 8192),
            ("ollama/qwen3.5-397b", "gateway-default", 32768),
        ):
            with self.subTest(thinking=thinking):
                seat = {"endpoint": name, "thinking": thinking, "reasoning_effort": "medium"}
                maximum = config.completion_tokens_for(recipe, config.thinking_for(seat))
                self.assertEqual(maximum, ceiling)
                records = self.case / thinking
                prepared = adapter.Adapter().prepare(seat=seat, messages=MESSAGES,
                                                     max_tokens=maximum)
                adapter.Adapter().call(seat=seat, messages=MESSAGES, records_dir=records,
                                       max_tokens=maximum, scripted={"answer": "Fixture answer."})
                request = read_json(records / "call-0001.request.json")
                wire = json.loads(request["wire_body_text"])
                self.assertEqual(wire, prepared["payload"])
                self.assertEqual(request["wire_body_sha256"], prepared["wire_body_sha256"])
                self.assertEqual(request["settings"]["max_tokens"], ceiling)
                if config.endpoint_for(seat).native:
                    self.assertEqual(wire["options"]["num_predict"], ceiling)
                else:
                    self.assertEqual(wire["max_tokens"], ceiling)
                self.assertEqual(prepared["kwargs"]["reasoning_effort"], "medium")
                if thinking == "native":
                    self.assertEqual(wire["reasoning_effort"], "medium")
                    self.assertEqual(request["settings"]["reasoning_effort"], "medium")
                else:
                    self.assertNotIn("reasoning_effort", wire)

    def test_each_shipped_seat_declares_medium_and_split_ceilings(self):
        for name in ("single-family", "cross-family", "cross-family-rival"):
            recipe = config.load_recipe(name)["data"]
            self.assertEqual(recipe["ceilings"]["completion_tokens"], 8192)
            self.assertEqual(recipe["ceilings"]["native_completion_tokens"], 32768)
            seats = recipe["seats"]
            for seat in [seats["conjecture"], *seats["critics"], seats["use"], seats["rival"]]:
                if seat is not None:
                    self.assertEqual(seat["reasoning_effort"], "medium")

    def test_owner_high_override_reaches_native_wire(self):
        seat = {"endpoint": "deepseek-flash", "thinking": "native", "reasoning_effort": "high"}
        records = self.case / "owner-high"
        adapter.Adapter().call(seat=seat, messages=MESSAGES, records_dir=records,
                               max_tokens=32768, scripted={"answer": "Fixture answer."})
        request = read_json(records / "call-0001.request.json")
        self.assertEqual(request["request"]["reasoning_effort"], "high")
        self.assertEqual(request["settings"]["reasoning_effort"], "high")

    def test_legacy_seats_and_recipe_keep_high_and_saved_ceiling(self):
        recipe = config.load_recipe("single-family")["data"]
        seats = recipe["seats"]
        for seat in [seats["conjecture"], *seats["critics"], seats["use"]]:
            seat.pop("reasoning_effort")
        recipe["ceilings"]["native_completion_tokens"] = 8192
        config.validate_recipe(recipe)
        for seat in (seats["conjecture"], "deepseek-flash"):
            self.assertEqual(config.reasoning_effort_for(seat), "high")
            prepared = adapter.Adapter().prepare(
                seat=seat, messages=MESSAGES,
                max_tokens=config.completion_tokens_for(recipe, "native"))
            self.assertEqual(prepared["payload"]["max_tokens"], 8192)
            self.assertEqual(prepared["payload"]["reasoning_effort"], "high")

    def test_invalid_seat_effort_is_refused_before_provider_use(self):
        for effort in ("low", "max", "invalid", None, 1, []):
            with self.subTest(effort=effort):
                recipe = config.load_recipe("single-family")["data"]
                seat = recipe["seats"]["conjecture"]
                seat["reasoning_effort"] = effort
                with self.assertRaises(ReasonFailure) as caught:
                    config.validate_recipe(recipe)
                self.assertEqual(caught.exception.code, "CONFIG_ERROR")
                with self.assertRaises(ReasonFailure):
                    adapter.Adapter().prepare(seat=seat, messages=MESSAGES)

    def test_adapter_medium_compatibility_does_not_change_protected_validator(self):
        endpoint = config.endpoint_for("deepseek-flash")
        original = provider._RecordedCaller(endpoint, self.case)
        with self.assertRaises(ValueError):
            original._validate_call_args(max_tokens=32768, reasoning_effort="medium", extra=None)
        for cls in (adapter._PreparedCaller, adapter._OfflineProvider, adapter._LiveProvider):
            caller = object.__new__(cls)
            caller.endpoint = endpoint
            caller._validate_call_args(max_tokens=32768, reasoning_effort="medium", extra=None)
            payload = caller._build_payload(
                MESSAGES, max_tokens=32768, reasoning_effort="medium", thinking=True,
                response_format={"type": "json_object"}, temperature=None, seed=None, extra=None)
            self.assertEqual(payload["max_tokens"], 32768)
            self.assertEqual(payload["reasoning_effort"], "medium")
            with self.assertRaises(ValueError):
                caller._validate_call_args(max_tokens=0, reasoning_effort="medium", extra=None)
            with self.assertRaises(ValueError):
                caller._validate_call_args(max_tokens=32768, reasoning_effort="medium",
                                           extra={"max_tokens": 8192})


if __name__ == "__main__":
    unittest.main()
