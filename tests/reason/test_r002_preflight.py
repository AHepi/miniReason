"""Offline-only gates: malformed declarations never become live capability."""
import copy
import hashlib
import json
import unittest
from unittest.mock import patch
from minireason.reason import config, prompts
from minireason.reason.adapter import Adapter
from minireason.reason.r002 import ContractSet, _answer_blocks, _relation_entry, _seat
from minireason.reason.r002_preflight import (capability_snapshot, validate_capability,
                                             token_preflight, snapshot_tokenizers)
from minireason.reason import r002_launcher
from minireason.reason.types import ReasonFailure


class R002PreflightTests(unittest.TestCase):
    def test_every_frozen_recipe_loads_with_16384_off_and_no_recovery(self):
        for filename in config.R002_RECIPE_SHA256:
            recipe = config.load_recipe(filename[:-5])["data"]
            self.assertEqual(config.completion_tokens_for(recipe, "off"), 16384)
            self.assertEqual(config.completion_tokens_for(recipe, "native"), 32768)
            self.assertEqual(set(recipe["attempt_policy"].values()), {0})
            mutated = copy.deepcopy(recipe)
            mutated["ceilings"]["off_completion_tokens"] = 8192
            with self.assertRaises(ReasonFailure):
                config.validate_recipe(mutated)

    def test_pins_accept_exact_cap_but_stop_without_truncation_next_byte(self):
        overhead = len(json.dumps([{"role": "user", "content": ""}], separators=(",", ":")))
        messages = [{"role": "user", "content": "x" * (32768 - overhead)}]
        passed = token_preflight(messages, "deepseek-flash")
        self.assertEqual(passed["counted_tokens"], 32768)
        self.assertFalse(passed["truncated"])
        self.assertEqual(passed["evidence_kind"], "offline-test-fixture")
        messages[0]["content"] += "x"
        with self.assertRaises(ReasonFailure) as error:
            token_preflight(messages, "deepseek-flash")
        self.assertEqual(error.exception.code, "PROMPT_TOKEN_CAP")
        self.assertEqual(error.exception.record["counted_tokens"], 32769)
        self.assertEqual(error.exception.record["outcome"], "stop_no_truncate")

    def test_fixture_or_absent_tokenizer_refuses_live(self):
        for pins in (None, snapshot_tokenizers(None)):
            with self.assertRaises(ReasonFailure) as error:
                token_preflight([], "deepseek-flash", pins, "live")
            self.assertEqual(error.exception.code, "TOKENIZER_UNAVAILABLE")

    def test_capability_maps_are_exact_not_partial_or_supersets(self):
        capability = capability_snapshot("published-review-reference")
        self.assertEqual(validate_capability(capability, "NATIVE"), capability)
        for key in ("schema_sha256", "recipe_sha256"):
            for mutation in ("missing", "extra", "wrong"):
                changed = copy.deepcopy(capability)
                name = next(iter(changed[key]))
                if mutation == "missing": del changed[key][name]
                elif mutation == "extra": changed[key]["surprise.json"] = "0" * 64
                else: changed[key][name] = "0" * 64
                with self.assertRaises(ReasonFailure):
                    validate_capability(changed, "NATIVE")
        for key, value in (("strict_attempt_policy", False), ("maximum_cycles", 4),
                           ("off_completion_tokens", 8192), ("review_receipt", "")):
            changed = copy.deepcopy(capability); changed[key] = value
            with self.assertRaises(ReasonFailure):
                validate_capability(changed, "NATIVE")

    def test_offline_success_cannot_unlock_checker_or_live(self):
        for capability in (None, capability_snapshot(), validate_capability(None, "NATIVE", "offline")):
            with self.assertRaises(ReasonFailure):
                validate_capability(capability, "NATIVE", "live")
        with self.assertRaises(ReasonFailure) as error:
            validate_capability(capability_snapshot("published-review-reference"), "LOOP-CHECKER")
        self.assertEqual(error.exception.code, "CHECKER_UNQUALIFIED")

    def test_local_tokenizer_missing_directory_fails_before_import_or_network(self):
        pins = {"schema": "minireason.r002.tokenizers.v1", "kind": "huggingface-local-chat-template-v1",
                "endpoints": {"deepseek-flash": {"directory": "C:/tw20/nonexistent-tokenizer",
                               "files": {"tokenizer.json": "0" * 64}}}}
        with patch("socket.socket", side_effect=AssertionError("network forbidden")):
            with self.assertRaises(ReasonFailure) as error:
                token_preflight([], "deepseek-flash", pins, "live")
        self.assertEqual(error.exception.code, "TOKENIZER_MISMATCH")

    def test_fixed_calibration_bound_accepts_only_an_exact_reviewed_wire(self):
        study = config.R002_DIR
        descriptor = r002_launcher.calibration_wire_bound(study)
        self.assertEqual(len(descriptor["wires"]), 24)
        self.assertEqual(max(item["wire_utf8_bytes"] for item in descriptor["wires"].values()), 4706)
        self.assertEqual(max(item["prompt_tokens"] for item in descriptor["wires"].values()), 1192)

        wire = '{"fixed":"calibration-wire"}'
        digest = hashlib.sha256(wire.encode("utf-8")).hexdigest()
        original = next(key for key, item in descriptor["wires"].items()
                        if item["candidate_id"] == "C01")
        descriptor["wires"].pop(original)
        size = len(wire.encode("utf-8"))
        proof = json.loads(r002_launcher.Path(r002_launcher.__file__).with_name(
            "r002_calibration_bounds.json").read_text(encoding="utf-8"))
        proven = proof["rows"]["C01"]
        descriptor["wires"][digest] = {
            "candidate_id": "C01", "wire_utf8_bytes": size,
            "prompt_tokens": proven["prompt_tokens"],
            "rendered_sha256": proven["rendered_sha256"],
            "rendered_utf8_bytes": proven["rendered_utf8_bytes"],
        }
        with self.assertRaises(ReasonFailure):
            snapshot_tokenizers(descriptor, "live")

        descriptor = r002_launcher.calibration_wire_bound(study)
        original_wire = next(key for key, item in descriptor["wires"].items()
                             if item["candidate_id"] == "C01")
        relations = json.loads((study / "problems" / "RELATIONS.json").read_text(encoding="utf-8"))
        problem = (study / "problems" / "C01.txt").read_text(encoding="utf-8")
        relation = _relation_entry(relations, "C01")
        contracts = ContractSet(study / "contracts")
        messages = prompts.render_r002(
            "answer", [*_answer_blocks(problem, relation), *contracts.prompt_blocks("answer")])
        adapter = Adapter("offline", {"data": config.load_endpoint_snapshot()["data"]})
        prepared = adapter.prepare(
            seat=_seat("initial", None), messages=messages, max_tokens=32768,
            thinking="native", role="answer",
            coordinate={"call_id": "initial", "cycle": 0, "attempt": 0,
                        "condition": "CAL-NATIVE", "strict": True})
        wire = prepared["wire_body_text"]
        self.assertEqual(prepared["wire_body_sha256"], original_wire)
        record = token_preflight(messages, "deepseek-flash", descriptor, "live",
                                 wire_body_text=wire, condition="CAL-NATIVE", role="answer")
        self.assertEqual(record["wire_body_sha256"], original_wire)
        self.assertEqual(record["counted_tokens"], 1050)
        self.assertEqual(record["evidence_kind"], "pinned-public-serializer-token-count")
        with self.assertRaises(ReasonFailure) as error:
            token_preflight(messages, "deepseek-flash", descriptor, "live",
                            wire_body_text=wire + " ", condition="CAL-NATIVE", role="answer")
        self.assertEqual(error.exception.code, "TOKENIZER_MISMATCH")
        with self.assertRaises(ReasonFailure):
            token_preflight(messages, "deepseek-flash", descriptor, "live",
                            wire_body_text=wire, condition="NATIVE", role="answer")
