"""Offline regression coverage for reasoning exposure rather than wire controls."""
import json
import os
from pathlib import Path
import unittest
import uuid
from unittest import mock

from minireason import provider_openai_compat as provider

from minireason.reason import adapter, config, engine
from minireason.reason.types import ReasonFailure


class ReasoningExposureCeilingTests(unittest.TestCase):
    def test_every_shipped_recipe_selects_ceiling_by_reasoning_exposure(self):
        for name in ("single-family", "cross-family", "cross-family-rival"):
            recipe = config.load_recipe(name)["data"]
            for thinking, expected in (("native", 32768), ("gateway-default", 32768), ("off", 8192)):
                with self.subTest(recipe=name, thinking=thinking):
                    self.assertEqual(config.completion_tokens_for(recipe, thinking), expected)

    def test_invalid_thinking_is_refused_without_defaulting_to_off(self):
        recipe = config.load_recipe("cross-family")["data"]
        for thinking in ("invalid", "", None, False, 1, [], {}):
            with self.subTest(thinking=thinking), self.assertRaises(ReasonFailure) as caught:
                config.completion_tokens_for(recipe, thinking)
            self.assertEqual(caught.exception.code, "CONFIG_ERROR")

    def test_reasoning_ceiling_cannot_be_lower_than_off_ceiling(self):
        recipe = config.load_recipe("cross-family")["data"]
        recipe["ceilings"]["native_completion_tokens"] = 4096
        with self.assertRaises(ReasonFailure) as caught:
            config.validate_recipe(recipe)
        self.assertEqual(caught.exception.code, "CONFIG_ERROR")

    def test_equal_frozen_ceilings_remain_valid(self):
        recipe = config.load_recipe("cross-family")["data"]
        recipe["ceilings"]["native_completion_tokens"] = 8192
        config.validate_recipe(recipe)
        for thinking in ("native", "gateway-default", "off"):
            self.assertEqual(config.completion_tokens_for(recipe, thinking), 8192)


class NativeOllamaControlTests(unittest.TestCase):
    def setUp(self):
        self.case = Path(__file__).resolve().parents[2] / "work/review12b/settings/fixtures" / uuid.uuid4().hex[:8]
        self.case.mkdir(parents=True)
        for patcher in (
            mock.patch.object(os, "environ", {"PYTHONUTF8": "1"}),
            mock.patch.object(provider.OpenAICompatProvider, "__init__",
                              side_effect=AssertionError("Live provider forbidden")),
            mock.patch.object(provider, "_open", side_effect=AssertionError("Network forbidden")),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)
        self.messages = [{"role": "user", "content": "Return JSON for this public fixture problem."}]

    @staticmethod
    def read_json(path):
        with path.open(encoding="utf-8", newline="") as handle:
            return json.load(handle)

    def test_native_ollama_modes_reach_prepared_wire_actual_records_and_recovery(self):
        for mode, think, cap in (("off", False, 8192), ("native", True, 32768),
                                 ("gateway-default", None, 32768)):
            with self.subTest(mode=mode):
                seat = {"endpoint": "ollama/qwen3.5-397b.native", "thinking": mode,
                        "reasoning_effort": "medium"}
                prepared = adapter.Adapter().prepare(seat=seat, messages=self.messages, max_tokens=cap)
                self.assertEqual(prepared["thinking"], mode)
                self.assertIsNone(prepared["kwargs"]["thinking"])
                self.assertEqual(prepared["payload"]["options"]["num_predict"], cap)
                self.assertNotIn("thinking", prepared["payload"])
                if think is None:
                    self.assertIsNone(prepared["kwargs"]["extra"])
                    self.assertNotIn("think", prepared["payload"])
                else:
                    self.assertEqual(prepared["kwargs"]["extra"], {"think": think})
                    self.assertIs(prepared["payload"]["think"], think)
                records = self.case / mode
                result = adapter.Adapter().call(
                    seat=seat, messages=self.messages, max_tokens=cap, records_dir=records,
                    scripted={"content": '{"answer": "Fixture answer."}',
                              "reasoning_content_present": mode == "native"})
                request = self.read_json(records / "call-0001.request.json")
                self.assertEqual(json.loads(request["wire_body_text"]), prepared["payload"])
                self.assertEqual(request["settings"]["extra"], prepared["kwargs"]["extra"] or {})
                self.assertIsNone(request["settings"]["thinking"])
                self.assertEqual(result["record"]["reasoning_content_present"], mode == "native")
                self.assertIs(result["record"]["reasoning_content_persisted"], False)
                with mock.patch.object(adapter, "_execute", side_effect=AssertionError("No replay")):
                    resumed = adapter.Adapter().call(seat=seat, messages=self.messages, records_dir=records)
                self.assertEqual(resumed, result)

    def test_off_request_keeps_observed_hidden_presence_without_new_status(self):
        result = adapter.Adapter().call(
            seat={"endpoint": "ollama/qwen3.5-397b.native", "thinking": "off"},
            messages=self.messages, records_dir=self.case / "presence",
            scripted={"content": '{"answer": "Fixture answer."}', "reasoning_content_present": True})
        self.assertEqual(result["status"], "COMPLETE")
        self.assertIs(result["record"]["reasoning_content_present"], True)
        self.assertIs(result["record"]["reasoning_content_persisted"], False)

    def test_native_extra_is_validated_and_shipped_ollama_seats_request_off(self):
        seen = []
        original = adapter._PreparedCaller._validate_call_args
        def validate(caller, **kwargs):
            seen.append(kwargs["extra"])
            return original(caller, **kwargs)
        with mock.patch.object(adapter._PreparedCaller, "_validate_call_args", validate):
            for name in ("single-family", "cross-family", "cross-family-rival"):
                recipe = config.load_recipe(name)["data"]
                seats = recipe["seats"]
                for seat in [seats["conjecture"], *seats["critics"], seats["use"], seats["rival"]]:
                    if seat is None or not seat["endpoint"].startswith("ollama/"):
                        continue
                    self.assertTrue(seat["endpoint"].endswith(".native"))
                    self.assertEqual(seat["thinking"], "off")
                    self.assertTrue(config.native_thinking_available(seat))
                    prepared = adapter.Adapter().prepare(seat=seat, messages=self.messages)
                    self.assertIs(prepared["payload"]["think"], False)
        self.assertTrue(seen)
        self.assertTrue(all(extra == {"think": False} for extra in seen))

    def test_compatibility_gateway_keeps_large_ceiling_and_refuses_explicit_control(self):
        seat = {"endpoint": "ollama/qwen3.5-397b", "thinking": "gateway-default"}
        recipe = config.load_recipe("cross-family")["data"]
        cap = config.completion_tokens_for(recipe, config.thinking_for(seat))
        prepared = adapter.Adapter().prepare(seat=seat, messages=self.messages, max_tokens=cap)
        self.assertEqual(prepared["payload"]["max_tokens"], 32768)
        self.assertNotIn("think", prepared["payload"])
        self.assertFalse(config.native_thinking_available(seat))
        for mode in ("off", "native"):
            with self.assertRaises(ReasonFailure) as caught:
                adapter.Adapter().prepare(seat=seat, messages=self.messages, thinking=mode)
            self.assertEqual(caught.exception.code, "CONFIG_ERROR")

    def test_native_ollama_critic_ceiling_falls_back_to_off_at_same_cap(self):
        from tests.reason import test_engine as fixture
        recipe = config.load_recipe("cross-family")["data"]
        recipe["seats"]["critics"][0]["thinking"] = "native"
        recipe_path = self.case / "recipe.json"
        with recipe_path.open("w", encoding="utf-8", newline="") as handle:
            handle.write(json.dumps(recipe) + "\n")
        run = engine.create_run(problem="Preserve a public invariant.", recipe=recipe_path,
                                cycles=1, out=self.case / "r", mode="offline")
        original = adapter.Adapter.call
        def inject(caller, **kwargs):
            if kwargs["coordinate"]["call_id"] == "c0001-k01" and kwargs["thinking"] == "native":
                kwargs["scripted"] = {"content": "", "finish_reason": "length",
                                      "reasoning_content_present": True}
            return original(caller, **kwargs)
        with mock.patch.object(adapter.Adapter, "call", inject):
            state = engine.execute(run, scripted=fixture.scripted_reply)
        self.assertEqual(state["completed_cycles"], 1)
        self.assertEqual(state["stop_reason"], "cycle_budget")
        first = self.read_json(run / "calls/c0001-k01/a00/provider/call-0001.request.json")
        fallback = self.read_json(run / "calls/c0001-k01/a01/provider/call-0001.request.json")
        self.assertIs(first["request"]["think"], True)
        self.assertIs(fallback["request"]["think"], False)
        self.assertEqual(first["request"]["options"]["num_predict"], 32768)
        self.assertEqual(fallback["request"]["options"]["num_predict"], 32768)
        self.assertEqual(first["request"]["messages"], fallback["request"]["messages"])


if __name__ == "__main__":
    unittest.main()
