"""Offline H003 fixture checks. No provider network or operator contract access."""
from pathlib import Path
import json
import os
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
from tools import multicycle_language_probe as h


class FakeProvider:
    lock = threading.Lock()
    active = peak = calls = 0
    failure = None
    barrier = None
    gate = False

    def __init__(self, settings, records):
        self.settings, self.records = settings, records

    def complete(self, messages, *, json_output, coordinate):
        cls = type(self)
        if not cls.gate:
            raise AssertionError("Publication preflight must precede dispatch")
        with cls.lock:
            cls.calls += 1
            cls.active += 1
            cls.peak = max(cls.peak, cls.active)
        try:
            if cls.barrier:
                cls.barrier.wait(timeout=10)
            time.sleep(0.002)
            arm, cycle = coordinate["arm"], coordinate["cycle"]
            payload = h.payload_for(messages)
            record = {"request": payload, "request_sha256": h.digest(payload),
                      "content": f"opaque-public[{arm}|{cycle}] Unicode π. No semantic admission.",
                      "status": "COMPLETE", "finish_reason": "stop", "returned_model": "offline-fixture",
                      "usage": {"prompt_tokens": 7, "completion_tokens": 3, "total_tokens": 10},
                      "reasoning_content_present": False, "reasoning_content_persisted": False}
            h.write_new(self.records / "call-0001.request.json", {"request": payload, "coordinate": coordinate})
            if arm == cls.failure:
                record.update(status="INCOMPLETE_GENERATION", finish_reason="length")
            h.write_new(self.records / "call-0001.response.json", record)
            if arm == cls.failure:
                raise RuntimeError("Do not publish arbitrary exception text")
            return record
        finally:
            with cls.lock:
                cls.active -= 1


class MultiCycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.output = Path(self.temp.name) / "H003"
        self.repo = Path(h.__file__).resolve().parents[1]
        self.output.mkdir()
        self.data = {"schema": "minireason.language-error-material.v1",
                     "shared_system": "Stable common contract π and original language specimens.",
                     "arms": [{"arm_id": arm, "instruction": "SELECT " + arm} for arm in h.ARMS],
                     "source_pins": {},
                     "cycles": [{"cycle": c, "task": f"Only task marker {c}",
                                 "reopen_cycles": [1] if c in (5, 10, 15, 20) else []}
                                for c in range(1, 21)]}
        h.write_new(self.output / "material.json", self.data)
        h.initialize(self.repo, self.output)
        FakeProvider.active = FakeProvider.peak = FakeProvider.calls = 0
        FakeProvider.failure = FakeProvider.barrier = None
        FakeProvider.gate = False
        self.env = patch.dict(os.environ, {"DEEPSEEK_API_KEY": "synthetic-offline-credential"})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.temp.cleanup()

    def published(self, *args):
        FakeProvider.gate = True
        return "offline-verified-publication"

    def send(self, cycle):
        return h.send_cycle(self.repo, self.output, cycle, provider_factory=FakeProvider,
                            publication_check=self.published, notify=lambda line: None)

    def test_twenty_cycles_windows_reopen_arm_isolation_and_full_custody(self):
        for cycle in range(1, 21):
            h.prepare(self.repo, self.output, cycle)
            for arm in h.ARMS:
                request = h.load(h.at(self.output, "requests", arm, cycle))
                trace = h.load(h.at(self.output, "traces", arm, cycle))
                user = request["messages"][1]["content"]
                self.assertEqual(request["messages"][0]["content"], self.data["shared_system"] + "\n\nSELECT " + arm)
                self.assertIn(f"Only task marker {cycle}\n", user)
                self.assertNotIn(h.ENVELOPE, user)
                self.assertTrue(trace["original_brief"].endswith(h.ENVELOPE))
                visible = {cycle - 1} if cycle > 1 else set()
                if cycle in (5, 10, 15, 20):
                    visible.add(1)
                    self.assertEqual(trace["input_ports"]["reopened"]["targets"][0]["cycle"], 1)
                for prior in range(1, cycle):
                    self.assertEqual(f"opaque-public[{arm}|{prior}]" in user, prior in visible)
                for other in h.ARMS:
                    if other != arm:
                        self.assertNotIn(f"opaque-public[{other}|", user)
                parents = trace["input_ports"]["previous"]["parents"]
                self.assertEqual([p["cycle"] for p in parents], [cycle - 1] if cycle > 1 else [])
            self.send(cycle)
        summary = h.checkpoint(self.repo, self.output, 20)
        self.assertEqual(summary["status"], "COMPLETE")
        self.assertEqual(summary["attempt_markers"], 100)
        self.assertEqual(summary["terminal_receipts"], 100)
        self.assertEqual(summary["usage"], {"prompt_tokens": 700, "completion_tokens": 300, "total_tokens": 1000})
        self.assertEqual(FakeProvider.calls, 100)
        self.assertFalse(summary["full_durable_scheduler"])
        with self.assertRaises(FileExistsError):
            h.checkpoint(self.repo, self.output, 20)

    def test_pool_starts_five_together_and_publication_precedes_any_attempt(self):
        h.prepare(self.repo, self.output, 1)
        def publication(*args):
            self.assertEqual(FakeProvider.calls, 0)
            self.assertFalse((self.output / "attempts").exists())
            return self.published(*args)
        FakeProvider.barrier = threading.Barrier(5)
        rows = h.send_cycle(self.repo, self.output, 1, provider_factory=FakeProvider,
                            publication_check=publication, notify=lambda line: None)
        self.assertEqual(len(rows), 5)
        self.assertEqual(FakeProvider.peak, 5)
        summary = h.checkpoint(self.repo, self.output, 1)
        self.assertEqual(summary["observed_maximum_concurrency"], 5)
        self.assertEqual(summary["status"], "PARTIAL")

    def test_publication_failure_starts_nothing(self):
        h.prepare(self.repo, self.output, 1)
        def denied(*args):
            raise ValueError("UNPUBLISHED")
        with self.assertRaisesRegex(ValueError, "UNPUBLISHED"):
            h.send_cycle(self.repo, self.output, 1, provider_factory=FakeProvider, publication_check=denied)
        self.assertEqual(FakeProvider.calls, 0)
        self.assertFalse((self.output / "attempts").exists())

    def test_failed_arm_stops_alone_and_original_partial_public_text_is_preserved(self):
        FakeProvider.failure = "rss"
        h.prepare(self.repo, self.output, 1)
        rows = self.send(1)
        self.assertEqual(sum(r["status"] == "COMPLETE" for r in rows), 4)
        self.assertTrue(h.stopped(self.output, "rss").exists())
        self.assertIn("opaque-public[rss|1]", h.at(self.output, "responses", "rss", 1, "txt").read_text(encoding="utf-8"))
        self.assertEqual(h.prepare(self.repo, self.output, 2), [a for a in h.ARMS if a != "rss"])
        self.send(2)
        self.assertEqual(FakeProvider.calls, 9)
        self.assertFalse(h.at(self.output, "attempts", "rss", 2).exists())
        summary = h.checkpoint(self.repo, self.output, 2)
        self.assertEqual(summary["arms"]["rss"], {"completed_cycles": 0, "stopped": True})

    def test_no_clobber_missing_parents_and_no_retry(self):
        with self.assertRaises(FileExistsError):
            h.initialize(self.repo, self.output)
        with self.assertRaises(FileNotFoundError):
            h.prepare(self.repo, self.output, 2)
        self.assertFalse((self.output / "requests").exists())
        h.prepare(self.repo, self.output, 1)
        with self.assertRaisesRegex(FileExistsError, "REQUEST_ALREADY_EXISTS"):
            h.prepare(self.repo, self.output, 1)
        self.send(1)
        with self.assertRaisesRegex(FileExistsError, "NO_RETRY"):
            self.send(1)
        self.assertEqual(FakeProvider.calls, 5)

    def test_request_material_and_runtime_mutation_refused(self):
        h.prepare(self.repo, self.output, 1)
        path = h.at(self.output, "requests", "whl", 1)
        raw = path.read_bytes()
        value = h.load(path)
        value["messages"][1]["content"] += "UNDECLARED INPUT"
        path.write_bytes(h.encoded(value))
        with self.assertRaisesRegex(ValueError, "REQUEST_OR_TRACE_CHANGED"):
            self.send(1)
        path.write_bytes(raw)
        material_path = self.output / "material.json"
        material_raw = material_path.read_bytes()
        material_path.write_bytes(material_raw + b" ")
        with self.assertRaisesRegex(ValueError, "PLAN_MATERIAL_OR_RUNTIME_CHANGED"):
            self.send(1)
        material_path.write_bytes(material_raw)
        with patch.object(h, "runtime_pins", return_value={"changed-runtime": "changed"}):
            with self.assertRaisesRegex(ValueError, "PLAN_MATERIAL_OR_RUNTIME_CHANGED"):
                self.send(1)
        self.assertEqual(FakeProvider.calls, 0)

    def test_own_helper_pin_and_ancestor_response_mutation_refused(self):
        plan_path = self.output / "plan.json"
        raw = plan_path.read_bytes()
        plan = h.load(plan_path)
        plan["helper_sha256"] = "changed-helper"
        plan_path.write_bytes(h.encoded(plan))
        with self.assertRaisesRegex(ValueError, "PLAN_MATERIAL_OR_RUNTIME_CHANGED"):
            h.prepare(self.repo, self.output, 1)
        plan_path.write_bytes(raw)
        h.prepare(self.repo, self.output, 1)
        self.send(1)
        h.at(self.output, "responses", "prose", 1, "txt").write_text("changed observation", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "RESPONSE_CUSTODY_CHANGED"):
            h.prepare(self.repo, self.output, 2)
        self.assertFalse(h.at(self.output, "requests", "prose", 2).exists())

    def test_pending_attempt_does_not_become_zero_usage_or_completed_call(self):
        h.prepare(self.repo, self.output, 1)
        h.write_new(h.at(self.output, "attempts", "prose", 1), {"started_at": h.utc()})
        summary = h.checkpoint(self.repo, self.output, 1)
        self.assertEqual(summary["pending_attempts"], 1)
        self.assertEqual(summary["provider_request_records"], 0)
        self.assertIsNone(summary["usage"]["completion_tokens"])
        self.assertFalse(summary["concurrency_intervals_complete"])

    def test_real_publication_preflight_rejects_remote_or_exact_byte_mismatch(self):
        # Use a temporary checkout boundary and mocked read-only Git responses, not Git mutations.
        h.prepare(self.repo, self.output, 1)
        with patch.object(h, "git", side_effect=[b"local\n", b"different refs/heads/main\n"]):
            with self.assertRaisesRegex(ValueError, "REMOTE_MAIN_CHANGED"):
                h.check_published(self.repo, self.output, 1, list(h.ARMS))
        # The real output must be inside the checkout for Git evidence. Copy this temporary
        # fixture under an independently temporary repo and use the actual path mapping.
        fake_repo = Path(self.temp.name)
        pins = {"source.txt": "irrelevant"}
        (fake_repo / "source.txt").write_text("source", encoding="utf-8")
        def fake_git(repo, *args):
            if args[0] == "rev-parse":
                return b"same\n"
            if args[0] == "ls-remote":
                return b"same refs/heads/main\n"
            return b"wrong published bytes"
        with patch.object(h, "git", side_effect=fake_git), patch.object(h, "verify", return_value=({"source_pins": {}}, {"runtime_pins": pins})):
            with self.assertRaisesRegex(ValueError, "INPUT_NOT_PUBLISHED"):
                h.check_published(fake_repo, self.output, 1, list(h.ARMS))

    def test_unknown_usage_stays_unknown_after_transport_failure(self):
        class NoReceiptProvider:
            def __init__(self, *args):
                pass
            def complete(self, *args, **kwargs):
                raise RuntimeError("secret-looking error must not escape")
        h.prepare(self.repo, self.output, 1)
        h.send_cycle(self.repo, self.output, 1, provider_factory=NoReceiptProvider,
                     publication_check=self.published, notify=lambda line: None)
        summary = h.checkpoint(self.repo, self.output, 1)
        self.assertEqual(summary["usage"], {"prompt_tokens": None, "completion_tokens": None, "total_tokens": None})
        self.assertEqual(summary["status"], "PARTIAL")
        self.assertNotIn("secret-looking", h.at(self.output, "responses", "prose", 1).read_text())


if __name__ == "__main__":
    unittest.main()
