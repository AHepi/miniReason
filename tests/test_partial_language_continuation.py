"""Offline H004 partial-continuation tests; no actual keys or network."""
import json
import os
from pathlib import Path
import shutil
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
from tools import partial_language_continuation as p
h = p.h


class FakeProvider:
    lock = threading.Lock()
    active = peak = calls = 0
    barrier = None
    failure_arm = None
    partial_targets = set()
    gate = False
    coordinates = []

    def __init__(self, settings, records):
        self.settings, self.records = settings, records

    def complete(self, messages, *, json_output, coordinate):
        cls = type(self)
        if not cls.gate:
            raise AssertionError("publication must precede provider")
        with cls.lock:
            cls.active += 1
            cls.peak = max(cls.peak, cls.active)
            cls.calls += 1
            cls.coordinates.append(dict(coordinate))
        try:
            if cls.barrier:
                cls.barrier.wait(timeout=10)
            time.sleep(0.001)
            arm, cycle, origin = coordinate["arm"], coordinate["cycle"], coordinate["harness"]
            partial = ((origin == "H003" and cycle == p.FRONTIERS[arm]) or (arm, cycle) in cls.partial_targets)
            payload = h.payload_for(messages)
            record = {"request": payload, "request_sha256": h.digest(payload),
                      "settings": self.settings.to_dict(), "coordinate": coordinate,
                      "content": f"opaque[{origin}/{arm}/{cycle}] π public text" + (" trailing prefix" if partial else " full"),
                      "status": "INCOMPLETE_GENERATION" if partial else "COMPLETE",
                      "finish_reason": "length" if partial else "stop", "returned_model": "offline-fixture",
                      "usage": {"prompt_tokens": 7, "completion_tokens": h.CAP if partial else 3,
                                "total_tokens": 7 + (h.CAP if partial else 3)},
                      "reasoning_content_present": False, "reasoning_content_persisted": False,
                      "credential_redaction": False}
            if origin == "H004" and arm == cls.failure_arm:
                record.update(status="THINKING_MODE_MISMATCH", reasoning_content_present=True)
            h.write_new(self.records / "call-0001.request.json", {k: record[k] for k in ("request", "request_sha256", "settings", "coordinate")})
            h.write_new(self.records / "call-0001.response.json", record)
            if record["status"] != "COMPLETE":
                raise RuntimeError("Persisted partial or operational failure; never retry")
            return record
        finally:
            with cls.lock:
                cls.active -= 1


class PartialContinuationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = tempfile.TemporaryDirectory()
        cls.repo = Path(p.__file__).resolve().parents[1]
        cls.seed_template = Path(cls.base.name) / "seed"
        cls.seed_template.mkdir()
        data = {"schema": "minireason.language-error-material.v1", "shared_system": "fixed contract and language text",
                "source_pins": {}, "arms": [{"arm_id": a, "instruction": "SELECT " + a} for a in h.ARMS],
                "cycles": [{"cycle": n, "task": f"TASK_{n}", "reopen_cycles": [1] if n % 5 == 0 else []}
                           for n in range(1, 21)]}
        h.write_new(cls.seed_template / "material.json", data)
        h.initialize(cls.repo, cls.seed_template)
        FakeProvider.gate = True
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "synthetic-offline-only"}):
            for cycle in range(1, 12):
                h.prepare(cls.repo, cls.seed_template, cycle)
                h.send_cycle(cls.repo, cls.seed_template, cycle, provider_factory=FakeProvider,
                             publication_check=lambda *args: "offline-seed-publication", notify=lambda line: None)

    @classmethod
    def tearDownClass(cls):
        cls.base.cleanup()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.seed = Path(self.temp.name) / "H003"
        self.output = Path(self.temp.name) / "H004"
        shutil.copytree(self.seed_template, self.seed)
        p.initialize(self.repo, self.output, self.seed)
        FakeProvider.active = FakeProvider.peak = FakeProvider.calls = 0
        FakeProvider.failure_arm = FakeProvider.barrier = None
        FakeProvider.partial_targets = set()
        FakeProvider.coordinates = []
        FakeProvider.gate = False
        self.env = patch.dict(os.environ, {"DEEPSEEK_API_KEY": "synthetic-offline-only"})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.temp.cleanup()

    def published(self, *args):
        FakeProvider.gate = True
        return "offline-published-inputs"

    def send(self, wave):
        return p.send_wave(self.repo, self.output, wave, provider_factory=FakeProvider,
                           publication_check=self.published, notify=lambda line: None)

    def test_uneven_seed_sixtyfive_new_calls_cover_twenty_no_old_reruns_and_partial_continues(self):
        FakeProvider.partial_targets = {("whl", 3), ("prose", 12)}
        for wave in range(1, 19):
            value = p.prepare_wave(self.repo, self.output, wave)
            expected = {a: frontier + wave for a, frontier in p.FRONTIERS.items() if frontier + wave <= 20}
            self.assertEqual(value["coordinates"], expected)
            for arm, cycle in expected.items():
                request = h.load(h.at(self.output, "requests", arm, cycle))
                trace = h.load(h.at(self.output, "traces", arm, cycle))
                user = request["messages"][1]["content"]
                self.assertIn(f"TASK_{cycle}\n", user)
                self.assertEqual([b["cycle"] for b in trace["previous"]], [cycle - 1])
                visible = {cycle - 1} | ({1} if cycle % 5 == 0 else set())
                for n in range(1, cycle):
                    origin = "H003" if n <= p.FRONTIERS[arm] else "H004"
                    self.assertEqual(f"opaque[{origin}/{arm}/{n}]" in user, n in visible)
                for other in h.ARMS:
                    if other != arm:
                        self.assertNotIn(f"opaque[H003/{other}/", user)
                        self.assertNotIn(f"opaque[H004/{other}/", user)
                if wave == 1:
                    self.assertIn("length-limited prefix", user)
                    self.assertEqual(trace["previous"][0]["origin"], "H003")
                    self.assertEqual(trace["previous"][0]["delivery_status"], "PARTIAL")
            self.send(wave)
        value = p.checkpoint(self.repo, self.output, 18)
        self.assertEqual(FakeProvider.calls, 65)
        self.assertEqual(value["combined_provider_request_records"], 100)
        self.assertEqual(value["new_partial"], 2)
        self.assertEqual(value["new_full"], 63)
        self.assertEqual(value["status"], "TWENTY_COORDINATES_COVERED")
        self.assertFalse(value["twenty_full_answers_each"])
        self.assertTrue(all(c["cycle"] > p.FRONTIERS[c["arm"]] for c in FakeProvider.coordinates))
        self.assertFalse(value["h003_resumed"])

    def test_pool_five_and_published_before_any_attempt(self):
        p.prepare_wave(self.repo, self.output, 1)
        def published(*args):
            self.assertFalse((self.output / "attempts").exists())
            self.assertEqual(FakeProvider.calls, 0)
            return self.published(*args)
        FakeProvider.barrier = threading.Barrier(5)
        p.send_wave(self.repo, self.output, 1, provider_factory=FakeProvider,
                    publication_check=published, notify=lambda line: None)
        self.assertEqual(FakeProvider.peak, 5)
        self.assertEqual(p.checkpoint(self.repo, self.output, 1)["observed_maximum_concurrency"], 5)

    def test_nonlength_failure_stops_only_affected_arm(self):
        FakeProvider.failure_arm = "rss"
        p.prepare_wave(self.repo, self.output, 1)
        rows = self.send(1)
        self.assertEqual(sum(r["status"] == "STOPPED" for r in rows), 1)
        selected = p.prepare_wave(self.repo, self.output, 2)["coordinates"]
        self.assertNotIn("rss", selected)
        self.send(2)
        self.assertEqual(FakeProvider.calls, 9)
        value = p.checkpoint(self.repo, self.output, 2)
        self.assertEqual(value["arms"]["rss"]["covered_through"], 8)
        self.assertEqual(value["arms"]["rss"]["stopped_reason"], "NON_ADMISSIBLE_DELIVERY")

    def test_no_clobber_no_retry_missing_parents_and_seed_coordinate_refusal(self):
        with self.assertRaises(FileExistsError):
            p.initialize(self.repo, self.output, self.seed)
        with self.assertRaisesRegex(ValueError, "SEED_COORDINATE_CANNOT_RERUN"):
            p.render_arm(self.repo, self.output, "prose", 11)
        with self.assertRaises(FileNotFoundError):
            p.prepare_wave(self.repo, self.output, 2)
        p.prepare_wave(self.repo, self.output, 1)
        with self.assertRaises(FileExistsError):
            p.prepare_wave(self.repo, self.output, 1)
        with self.assertRaises(FileNotFoundError):
            p.prepare_wave(self.repo, self.output, 2)
        self.send(1)
        with self.assertRaisesRegex(FileExistsError, "NO_RETRY"):
            self.send(1)
        self.assertEqual(FakeProvider.calls, 5)

    def test_seed_and_runtime_source_mutations_refused(self):
        path = h.at(self.seed, "responses", "whl", 2, "txt")
        raw = path.read_bytes()
        path.write_bytes(raw + b"changed")
        with self.assertRaisesRegex(ValueError, "PLAN_SEED_SOURCE_OR_RUNTIME_CHANGED"):
            p.prepare_wave(self.repo, self.output, 1)
        path.write_bytes(raw)
        with patch.object(h, "runtime_pins", return_value={"runtime": "changed"}):
            with self.assertRaises(ValueError):
                p.prepare_wave(self.repo, self.output, 1)
        self.assertEqual(FakeProvider.calls, 0)

    def test_request_and_ancestor_mutations_refused(self):
        p.prepare_wave(self.repo, self.output, 1)
        path = h.at(self.output, "requests", "whl", 3)
        raw = path.read_bytes()
        value = h.load(path)
        value["messages"][1]["content"] += "undeclared content"
        path.write_bytes(h.encoded(value))
        with self.assertRaisesRegex(ValueError, "REQUEST_OR_TRACE_CHANGED"):
            self.send(1)
        self.assertEqual(FakeProvider.calls, 0)
        path.write_bytes(raw)
        self.send(1)
        h.at(self.output, "responses", "whl", 3, "txt").write_bytes(b"changed public text")
        with self.assertRaisesRegex(ValueError, "CONTRIBUTION_CUSTODY_CHANGED"):
            p.prepare_wave(self.repo, self.output, 2)

    def test_publication_rejection_starts_nothing_and_remote_check_is_real(self):
        p.prepare_wave(self.repo, self.output, 1)
        def fail(*args):
            raise ValueError("UNPUBLISHED")
        with self.assertRaisesRegex(ValueError, "UNPUBLISHED"):
            p.send_wave(self.repo, self.output, 1, provider_factory=FakeProvider, publication_check=fail)
        self.assertFalse((self.output / "attempts").exists())
        with patch.object(h, "git", side_effect=[b"local\n", b"other refs/heads/main\n"]):
            with self.assertRaisesRegex(ValueError, "REMOTE_MAIN_CHANGED"):
                p.check_published(self.repo, self.output, 1, {})

    def test_unknown_usage_after_failure_and_partial_usage_contract(self):
        class Broken:
            def __init__(self, *args):
                pass
            def complete(self, *args, **kwargs):
                raise RuntimeError("untrusted error should not be copied")
        p.prepare_wave(self.repo, self.output, 1)
        p.send_wave(self.repo, self.output, 1, provider_factory=Broken,
                    publication_check=self.published, notify=lambda line: None)
        value = p.checkpoint(self.repo, self.output, 1)
        self.assertIsNone(value["new_usage"]["total_tokens"])
        self.assertIsNone(value["combined_usage"]["total_tokens"])
        self.assertEqual(value["new_provider_request_records"], 0)
        record = h.load(p.provider_dir(self.seed, "whl", 2) / "call-0001.response.json")
        self.assertEqual(p.classify(record, record["request"]), "PARTIAL")
        short_length = {**record, "usage": {**record["usage"], "completion_tokens": 4095}}
        self.assertEqual(p.classify(short_length, record["request"]), "STOPPED")
        for key, changed in (("usage", {}), ("content", ""), ("settings", {}), ("credential_redaction", True)):
            altered = {**record, key: changed}
            self.assertEqual(p.classify(altered, record["request"]), "STOPPED")


if __name__ == "__main__":
    unittest.main()
