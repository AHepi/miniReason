"""P-A4 replay of the actual rejected worker replies, without provider calls."""
from __future__ import annotations
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import unittest
from unittest import mock
from minireason import provider_openai_compat as provider
from minireason.pilot.pilot import Pilot
from tests.pilot.test_live_delivery import ROOT, FIXTURES, TASK_PATHS, read_json, read_text, live_body

class AttemptTwoDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ["TMP"], prefix="pa4-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        patch = mock.patch.object(provider, "_open", side_effect=AssertionError("NETWORK_FORBIDDEN"))
        patch.start(); self.addCleanup(patch.stop)

    def test_every_rejected_evidence_reply_uses_exact_bytes_and_host_resolution(self):
        for uc in ("UC2", "UC3", "UC4"):
            for attempt in ("a00", "a01"):
                with self.subTest(uc=uc, attempt=attempt):
                    original = live_body(f"{uc}-attempt2-c0003-{attempt}")
                    repair = live_body(f"{uc}-attempt2-c0003-a01")
                    seen = []
                    def scripted(**context):
                        seen.append(context)
                        return {"content": original if context["attempt"] == 0 else repair}
                    pilot = Pilot(read_json(TASK_PATHS[uc]), self.root / (uc+attempt), scripted=scripted, repo_root=ROOT)
                    output = pilot.execute_template("evidence_read", pilot.inputs, 1)
                    raw = json.loads(original)
                    expected_attempts = 2 if raw["verification_refs"] else 1
                    self.assertEqual(pilot.calls.count, expected_attempts)
                    self.assertEqual(pilot.calls.logical_count, 1)
                    if expected_attempts == 2:
                        self.assertEqual(seen[1]["messages"][-2]["content"], original)
                        self.assertIn("UNAUTHORIZED_MODEL_REFERENCE", seen[1]["messages"][-1]["content"])
                    response = read_json(pilot.root / "calls/c0001/a00/provider/call-0001.response.json")
                    self.assertEqual(response["content"].encode("utf-8"), original.encode("utf-8"))
                    sources = pilot._quote_sources(pilot.inputs, [])
                    event = next(e for e in pilot.events if e["choice"] == "quote-locations-resolved")
                    self.assertEqual(len(event["evidence"]["locations"]), len(output["quotes"]))
                    delivered = json.loads(repair if expected_attempts == 2 else original)
                    for index, quote in enumerate(output["quotes"]):
                        loc = event["evidence"]["locations"][index]
                        self.assertEqual(loc["authored_locator_hint"], delivered["quotes"][index]["locator"])
                        for span in loc["resolved_spans"]:
                            self.assertEqual(sources[quote["source_id"]].encode("utf-8")[span["start"]:span["end"]], quote["quote"].encode("utf-8"))
                        self.assertEqual(quote["locator"], loc["canonical_locator"])
                    self.assertEqual(output["verification_refs"], [])

    def test_both_live_attempts_are_complete_hash_bound_and_secret_free(self):
        original = read_json(FIXTURES / "CUSTODY.json")
        second = read_json(FIXTURES / "ATTEMPT2-CUSTODY.json")
        self.assertEqual((len(original["entries"]), len(second["entries"])), (11, 19))
        names = re.compile(r"(?:DEEPSEEK_API_KEY|OLLAMA_API_KEY|OPENAI_API_KEY|ANTHROPIC_API_KEY)", re.I)
        secret = re.compile(r"(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")
        for row in original["entries"] + second["entries"]:
            with self.subTest(fixture=row["fixture"]):
                raw = (ROOT / row["fixture"]).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), row["fixture_sha256"])
                self.assertEqual(len(raw), row["byte_count"])
                self.assertEqual(hashlib.sha256(raw).hexdigest(), row["public_content_sha256"])
                self.assertFalse(names.search(raw.decode("utf-8")))
                self.assertFalse(secret.search(raw.decode("utf-8")))
                self.assertFalse(row["reasoning_content_persisted"])
        self.assertEqual(second["credential_scan"]["key_name_matches"], 0)
        self.assertEqual(second["credential_scan"]["secret_shaped_matches"], 0)

    def test_repeated_exact_quote_records_all_matches_without_claiming_unique_location(self):
        task = {"task":"Read the duplicate exact passages", "inputs": {"documents":[{"id":"source", "text":"same same"}], "requested_claims":["Find same"]}}
        body = {"status":"complete", "answer":{"prose":"Both occurrences are present"}, "quotes":[{"source_id":"source", "quote":"same", "locator":"bytes:99:100"}]}
        pilot = Pilot(task, self.root / "duplicates", scripted=[body], repo_root=ROOT)
        output = pilot.execute_template("evidence_read", pilot.inputs, 1)
        event = next(e for e in pilot.events if e["choice"] == "quote-locations-resolved")
        loc = event["evidence"]["locations"][0]
        self.assertEqual(loc["authored_locator_hint"], "bytes:99:100")
        self.assertEqual(loc["resolved_spans"], [{"start":0,"end":4},{"start":5,"end":9}])
        self.assertEqual(output["quotes"][0]["locator"], "bytes:0:4")
        self.assertEqual(json.loads(output["answer"]), body["answer"])

if __name__ == "__main__": unittest.main()
