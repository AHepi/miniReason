from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from minireason import provider_openai_compat as provider
from minireason.pilot.recording import RecordedCalls
from minireason.pilot.templates import OUTPUT_SCHEMA
from minireason.reason.types import ReasonFailure


def complete(answer: str = "42") -> dict:
    return {
        "status": "complete",
        "answer": answer,
        "source_refs": [],
        "unresolved": [],
        "verification_refs": [],
    }


class RecordedCallsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=os.environ["TMP"])
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        patcher = mock.patch.object(provider, "_open", side_effect=AssertionError("network forbidden"))
        patcher.start()
        self.addCleanup(patcher.stop)
        self.messages = [
            {"role": "system", "content": "Return one JSON object."},
            {"role": "user", "content": "Solve the public fixture."},
        ]

    @staticmethod
    def read(path: Path) -> dict:
        with path.open(encoding="utf-8", newline="") as handle:
            return json.load(handle)

    def test_offline_call_binds_decision_to_actual_transport_evidence(self) -> None:
        usage = {"prompt_tokens": 7, "completion_tokens": 5, "total_tokens": 12}
        calls = RecordedCalls(
            self.root / "run",
            scripted=[{"content": json.dumps(complete()), "usage": usage}],
        )
        result = calls.call("answer", self.messages, schema=OUTPUT_SCHEMA)

        self.assertEqual(result, complete())
        self.assertEqual(calls.count, 1)
        self.assertEqual(len(calls.receipts), 1)
        attempt = self.root / "run" / "calls" / "c0001" / "a00"
        decision = self.read(attempt / "decision.json")
        outcome = self.read(attempt / "outcome.json")
        request = self.read(attempt / "provider" / "call-0001.request.json")
        response = self.read(attempt / "provider" / "call-0001.response.json")
        wire_sha = hashlib.sha256(request["wire_body_text"].encode("utf-8")).hexdigest()

        self.assertEqual(decision["status"], "pending")
        self.assertEqual(decision["endpoint"]["name"], "deepseek-flash")
        self.assertEqual(decision["endpoint"]["lineage"], "deepseek")
        self.assertTrue(decision["endpoint"]["native_thinking_available"])
        self.assertEqual(decision["prepared_wire_sha256"], wire_sha)
        self.assertEqual(request["wire_body_sha256"], wire_sha)
        self.assertEqual(request["would_send_bytes_sha256"], wire_sha)
        self.assertIsNone(request["url"])
        self.assertEqual(request["request_header_names"], [])
        self.assertEqual(outcome["request_wire"]["actual_authority"], "would_send_bytes_sha256")
        self.assertEqual(outcome["started_epoch"], request["recorded_epoch"])
        self.assertEqual(outcome["finished_epoch"], response["recorded_epoch"])
        self.assertEqual(outcome["usage"], usage)
        self.assertEqual(outcome["status"], "accepted")
        self.assertFalse(response["reasoning_content_persisted"])
        self.assertNotIn("reasoning_content", response)

    def test_one_repair_preserves_public_rejection_and_checker_error(self) -> None:
        invalid = '{"status":"complete"}'
        seen: list[dict] = []

        def scripted(**context):
            seen.append(context)
            content = invalid if context["attempt"] == 0 else json.dumps(complete("repaired"))
            return {"content": content}

        calls = RecordedCalls(self.root / "repair", scripted=scripted)
        result = calls.call("answer", self.messages, schema=OUTPUT_SCHEMA)

        self.assertEqual(result["answer"], "repaired")
        self.assertEqual(calls.count, 2)
        self.assertEqual([item["status"] for item in calls.receipts], ["contract_rejected", "accepted"])
        self.assertEqual(seen[1]["messages"][-2], {"role": "assistant", "content": invalid})
        self.assertIn("missing required fields", seen[1]["messages"][-1]["content"])
        self.assertTrue((self.root / "repair" / "calls" / "c0001" / "a01" / "decision.json").is_file())
        self.assertFalse((self.root / "repair" / "calls" / "c0001" / "a02").exists())

    def test_fourth_contract_failure_stops_without_a_fifth_attempt(self) -> None:
        calls = RecordedCalls(
            self.root / "twice",
            scripted=[{"content": "{}"}] * 4,
        )
        with self.assertRaises(ReasonFailure) as caught:
            calls.call("answer", self.messages, schema=OUTPUT_SCHEMA)
        self.assertEqual(caught.exception.code, "SCHEMA_REJECTED")
        self.assertEqual(calls.count, 4)
        self.assertEqual(calls.logical_count, 1)
        self.assertFalse((self.root / "twice" / "calls" / "c0001" / "a04").exists())

    def test_repair_is_the_same_logical_call_but_a_second_attempt(self) -> None:
        calls = RecordedCalls(
            self.root / "budget",
            max_calls=1,
            scripted=[{"content": "{}"}, {"content": json.dumps(complete("repaired"))}],
        )
        self.assertEqual(calls.call("answer", self.messages, schema=OUTPUT_SCHEMA)["answer"], "repaired")
        self.assertEqual(calls.logical_count, 1)
        self.assertEqual(calls.count, 2)
        with self.assertRaises(ReasonFailure) as caught:
            calls.call("answer", self.messages, schema=OUTPUT_SCHEMA)
        self.assertEqual(caught.exception.code, "CALL_BUDGET")
        self.assertEqual(calls.count, 2)

    def test_fixture_failure_records_no_dispatch_without_exception_text(self) -> None:
        def stopped(**_context):
            raise RuntimeError("sensitive fixture detail")

        calls = RecordedCalls(self.root / "fixture-stop", scripted=stopped)
        with self.assertRaises(RuntimeError):
            calls.call("answer", self.messages, schema=OUTPUT_SCHEMA)
        attempt = self.root / "fixture-stop" / "calls" / "c0001" / "a00"
        outcome = self.read(attempt / "outcome.json")
        self.assertEqual(outcome["status"], "not_dispatched")
        self.assertEqual(outcome["failure_code"], "HOST_ERROR")
        self.assertNotIn("sensitive fixture detail", (attempt / "outcome.json").read_text(encoding="utf-8"))
        self.assertFalse((attempt / "provider" / "call-0001.request.json").exists())

    def test_mvp_rejects_native_thinking_and_larger_ceiling_before_attempt(self) -> None:
        calls = RecordedCalls(self.root / "controls", scripted=[])
        for kwargs in ({"thinking": "native"}, {"max_tokens": 384001}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                calls.call("answer", self.messages, schema=OUTPUT_SCHEMA, **kwargs)
        self.assertEqual(calls.count, 0)


if __name__ == "__main__":
    unittest.main()
