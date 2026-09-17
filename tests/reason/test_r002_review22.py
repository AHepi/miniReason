"""Review22 boundary regressions; no network, credentials or participant calls."""
import copy
import json
import unittest
from minireason.reason.adapter import Adapter
from minireason.reason.config import R002_DIR, load_endpoint_snapshot
from minireason.reason.r002_preflight import snapshot_tokenizers, token_preflight
from minireason.reason.types import ReasonFailure

class Review22TemplateAllowance(unittest.TestCase):
    def setUp(self):
        self.pins = snapshot_tokenizers(R002_DIR / "calibration/main-tokenizer-pins.json", "offline")
        self.adapter = Adapter("offline", {"data": load_endpoint_snapshot()["data"]})

    def wire(self, endpoint, size):
        messages = [{"role": "system", "content": "Return JSON."}, {"role": "user", "content": "x"}]
        def prepare():
            return self.adapter.prepare(seat=endpoint, messages=messages, max_tokens=16384,
                thinking="off", role="answer", coordinate={"condition": "LOOP-TESTED", "strict": True})
        prepared = prepare()
        messages[1]["content"] += "x" * (size - len(prepared["wire_body_text"].encode("utf-8")))
        wire = prepare()["wire_body_text"]
        self.assertEqual(len(wire.encode("utf-8")), size)
        return messages, wire

    def test_every_endpoint_exact_boundary_and_one_over(self):
        for endpoint, allowance in self.pins["template_overhead_tokens"].items():
            for extra in (0, 1):
                with self.subTest(endpoint=endpoint, extra=extra):
                    size = 32768 - allowance + extra
                    messages, wire = self.wire(endpoint, size)
                    def check():
                        return token_preflight(messages, endpoint, self.pins, "offline", wire_body_text=wire)
                    if extra:
                        with self.assertRaises(ReasonFailure) as caught:
                            check()
                        self.assertEqual(caught.exception.code, "PROMPT_TOKEN_CAP")
                        record = caught.exception.record
                        self.assertEqual(record["outcome"], "stop_no_truncate")
                    else:
                        record = check()
                        self.assertEqual(record["outcome"], "accepted")
                    self.assertEqual(record["counted_tokens"], 32768 + extra)
                    self.assertEqual(record["wire_utf8_bytes"], size)
                    self.assertEqual(record["template_overhead_tokens"], allowance)

    def test_missing_or_reduced_allowance_fails_closed(self):
        for endpoint in self.pins["template_overhead_tokens"]:
            bad = copy.deepcopy(self.pins)
            del bad["template_overhead_tokens"][endpoint]
            with self.assertRaises(ReasonFailure):
                snapshot_tokenizers(bad, "offline")
        bad = copy.deepcopy(self.pins)
        bad["template_overhead_tokens"]["ollama/qwen3.5-397b.native"] = 2047
        with self.assertRaises(ReasonFailure):
            snapshot_tokenizers(bad, "offline")

    def test_extra_tools_and_messages_do_not_inherit_template_assumption(self):
        endpoint = "ollama/qwen3.5-397b.native"
        messages, wire = self.wire(endpoint, 1000)
        payload = json.loads(wire)
        payload["tools"] = []
        with self.assertRaises(ReasonFailure):
            token_preflight(messages, endpoint, self.pins, "offline", wire_body_text=json.dumps(payload))
        messages.append({"role": "assistant", "content": "history"})
        payload.pop("tools"); payload["messages"] = messages
        with self.assertRaises(ReasonFailure):
            token_preflight(messages, endpoint, self.pins, "offline", wire_body_text=json.dumps(payload))


class Review22LauncherRoot(unittest.TestCase):
    def test_review22_root_accepts_only_strict_descendants(self):
        from pathlib import Path
        from minireason.reason.r002_launcher import validate_run_root, LauncherError
        repo = Path(__file__).resolve().parents[2]
        accepted = Path("C:/tr22/offline-proof")
        self.assertEqual(validate_run_root(repo, accepted), accepted.resolve())
        for rejected in ("C:/tr22", "C:/tr22/../escape", "C:/tr22-sibling/proof"):
            with self.subTest(path=rejected), self.assertRaises(LauncherError):
                validate_run_root(repo, Path(rejected))
