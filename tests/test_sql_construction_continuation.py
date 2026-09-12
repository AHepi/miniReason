from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from minireason import sql_construction_continuation as c
from minireason import sql_construction_study as base
from minireason.provider import ProviderFailure

REPO = Path(base.__file__).resolve().parents[2]
RAW = 'Unsupported cases remain unresolved.  π\n  Preserve spaces.\n{"body":"Quoted data only"}\n'


class FakeProvider:
    total_calls = 0
    fail_at = None
    after_response = None
    on_init = None
    failure_code = "INCOMPLETE_GENERATION"

    def __init__(self, settings, records):
        self.settings, self.records, self.calls = settings, records, 0
        if type(self).on_init:
            type(self).on_init()

    def complete(self, messages, *, json_output=True, coordinate=None):
        if json_output:
            raise AssertionError("Prose must remain admissible")
        self.calls += 1
        type(self).total_calls += 1
        payload = base.payload_for(messages, self.settings)
        response = {"request": payload, "request_sha256": base.digest(payload), "content": RAW,
                    "usage": {"prompt_tokens": 20, "completion_tokens": 10, "total_tokens": 30},
                    "status": "COMPLETE", "finish_reason": "stop"}
        base.write_json(self.records / "call-0001.request.json", {"request": payload, "coordinate": coordinate})
        if type(self).fail_at == type(self).total_calls:
            base.write_json(self.records / "call-0001.response.json", {"status": "SCRIPTED_OFFLINE_FAILURE"})
            raise ProviderFailure(type(self).failure_code, "Untrusted exception detail must never be copied")
        base.write_json(self.records / "call-0001.response.json", response)
        if type(self).after_response:
            type(self).after_response()
        return response


class ContinuationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.parent_root = self.root / "parent-plan"
        self.parent_record = self.root / "parent-record"
        shutil.copytree(REPO / "experiments/plans/E026-sql-construction", self.parent_root)
        shutil.copytree(REPO / "experiments/records/E026-sql-construction", self.parent_record)
        self.frozen = self.root / "e027"
        self.output = self.root / "mock-record"
        self.kwargs = {"parent_root": self.parent_root, "parent_record": self.parent_record}
        FakeProvider.total_calls = 0
        FakeProvider.fail_at = FakeProvider.after_response = FakeProvider.on_init = None
        FakeProvider.failure_code = "INCOMPLETE_GENERATION"

    def tearDown(self):
        self.tmp.cleanup()

    def prepare(self):
        return c.prepare(self.frozen, REPO, **self.kwargs)

    def run_fake(self, plan):
        with patch.object(c, "DeepSeek", FakeProvider):
            return c.run(self.frozen, self.output, REPO, plan["plan_id"], **self.kwargs)

    def test_actual_source_offline_prepare_and_exact_parent_bytes(self):
        with patch.object(c, "DeepSeek", side_effect=AssertionError("Offline provider instantiated")), patch.object(base, "DeepSeek", side_effect=AssertionError("Parent provider instantiated")):
            plan = self.prepare()
            self.assertEqual(c.verify(self.frozen, REPO, **self.kwargs), plan)
        self.assertEqual(plan["max_provider_calls"], 2)
        self.assertEqual(plan["max_aggregate_completion_tokens"], 16384)
        self.assertEqual(plan["parent"]["parent_plan_id"], c.PARENT_PLAN_ID)
        for name in ("participant-source.json", "manifest.json", "requests/mini-disabled.json", "requests/prompt-control-disabled.json"):
            self.assertEqual((self.frozen / name).read_bytes(), (self.parent_root / name).read_bytes())
        self.assertEqual((self.frozen / "requests/mini-disabled.json").read_bytes(), (self.frozen / "requests/prompt-control-disabled.json").read_bytes())
        preflight = json.loads((self.frozen / "preflight.json").read_bytes())
        self.assertEqual(preflight["provider_calls"], 0)
        self.assertEqual(preflight["scripted_engine_calls"], 1)
        self.assertTrue(preflight["opaque_prose_preserved"])
        answer = (self.parent_record / "direct-disabled/public-answer.txt").read_text()
        for path in (self.frozen / "requests").glob("*.json"):
            self.assertNotIn(answer, path.read_text())

    def test_two_call_order_settings_and_opaque_custody(self):
        plan = self.prepare()
        summary = self.run_fake(plan)
        self.assertEqual(summary["status"], "COMPLETE")
        self.assertEqual(FakeProvider.total_calls, 2)
        self.assertEqual([row["arm"] for row in summary["arms"]], list(c.ARMS))
        self.assertEqual(summary["selected_occurrence"], c.TEST_ID + "/mini-disabled")
        self.assertFalse(summary["automatic_successor_started"])
        self.assertEqual(summary["unattempted_arms"], [])
        for arm in c.ARMS:
            self.assertEqual((self.output / arm / "public-answer.txt").read_bytes(), RAW.encode())
            request = json.loads((self.output / arm / "calls/call-0001.request.json").read_bytes())["request"]
            original = json.loads((self.parent_root / "requests" / (arm + ".json")).read_bytes())["request"]
            self.assertEqual(request, original)
            self.assertEqual(request["max_tokens"], 8192)
            self.assertEqual(request["thinking"], {"type": "disabled"})
        rows = base.artifact_prose(self.output / "mini-disabled/mini", base.compile_manifest(self.frozen / "manifest.json"))
        self.assertEqual([(row["body"], row["commitments"]) for row in rows], [(RAW, RAW)])

    def test_first_call_failure_stops_without_control(self):
        plan = self.prepare()
        FakeProvider.fail_at = 1
        summary = self.run_fake(plan)
        self.assertEqual(summary["status"], "INTERRUPTED")
        self.assertEqual(FakeProvider.total_calls, 1)
        self.assertEqual(summary["unattempted_arms"], ["prompt-control-disabled"])
        self.assertFalse((self.output / "prompt-control-disabled").exists())
        self.assertTrue((self.output / "mini-disabled/calls/call-0001.request.json").is_file())
        self.assertTrue((self.output / "summary.json").is_file())

    def test_second_call_failure_preserves_selected_public_occurrence(self):
        plan = self.prepare()
        FakeProvider.fail_at = 2
        summary = self.run_fake(plan)
        self.assertEqual(summary["status"], "INTERRUPTED")
        self.assertEqual(FakeProvider.total_calls, 2)
        self.assertEqual((self.output / "mini-disabled/public-answer.txt").read_bytes(), RAW.encode())
        self.assertEqual(summary["unattempted_arms"], [])

    def test_external_pin_and_existing_output_refuse_before_provider(self):
        plan = self.prepare()
        with patch.object(c, "DeepSeek", side_effect=AssertionError("Premature provider initialization")):
            with self.assertRaisesRegex(ValueError, "EXTERNALLY_PINNED_PLAN_ID_MISMATCH"):
                c.run(self.frozen, self.output, REPO, "wrong", **self.kwargs)
            self.assertFalse(self.output.exists())
            self.output.mkdir()
            (self.output / "sentinel").write_text("preserve")
            with self.assertRaises(FileExistsError):
                c.run(self.frozen, self.output, REPO, plan["plan_id"], **self.kwargs)
        self.assertEqual((self.output / "sentinel").read_text(), "preserve")
        with self.assertRaises(FileExistsError):
            self.prepare()

    def test_rehashed_metadata_changes_are_refused(self):
        plan = self.prepare()
        changes = {"arms": list(reversed(c.ARMS)), "max_tokens_per_call": 16384,
                   "automatic_retries": 1, "selected_construction_arm": "prompt-control-disabled",
                   "parent_outputs_in_prompts": True, "thinking": "enabled", "jobs": 2,
                   "max_provider_calls": 3, "selected_occurrence": "E026/mini-disabled"}
        for key, value in changes.items():
            with self.subTest(field=key):
                altered = {**plan, key: value}
                altered["plan_id"] = base.digest({k: v for k, v in altered.items() if k != "plan_id"})
                (self.frozen / "plan.json").write_bytes(base.encoded(altered))
                with self.assertRaisesRegex(ValueError, "EFFECTIVE_CONTRACT_CHANGED"):
                    c.verify(self.frozen, REPO, **self.kwargs)
        (self.frozen / "plan.json").write_bytes(base.encoded(plan))

    def test_parent_unattempted_claim_cannot_hide_an_attempt(self):
        self.prepare()
        summary_path = self.parent_record / "summary.json"
        summary = json.loads(summary_path.read_bytes())
        summary["arms"].append({"arm": "mini-disabled", "status": "OPERATIONAL_FAILURE"})
        summary_path.write_bytes(base.encoded(summary))
        with self.assertRaisesRegex(ValueError, "CONTINUATION_ARM_NOT_UNATTEMPTED"):
            c.verify(self.frozen, REPO, **self.kwargs)

    def test_unlisted_parent_attempt_directory_is_refused(self):
        (self.parent_record / "mini-disabled").mkdir()
        with self.assertRaisesRegex(ValueError, "CONTINUATION_ARM_NOT_UNATTEMPTED"):
            self.prepare()
        self.assertFalse(self.frozen.exists())

    def test_parent_record_mutation_is_refused(self):
        self.prepare()
        path = self.parent_record / "direct-disabled/public-answer.txt"
        path.write_bytes(path.read_bytes() + b"changed")
        with self.assertRaisesRegex(ValueError, "ORIGINAL_PARENT_RECORD_CHANGED"):
            c.verify(self.frozen, REPO, **self.kwargs)

    def test_tampering_all_frozen_input_routes_is_refused(self):
        self.prepare()
        changes = {"participant-source.json": "FROZEN_PARENT_INPUT_CHANGED",
                   "manifest.json": "FROZEN_PARENT_INPUT_CHANGED",
                   "requests/mini-disabled.json": "FROZEN_REQUEST_CHANGED",
                   "parent-summary.json": "PARENT_SUMMARY_COPY_CHANGED",
                   "parent-provenance.json": "PARENT_PROVENANCE_CHANGED"}
        for name, code in changes.items():
            with self.subTest(path=name):
                path = self.frozen / name
                original = path.read_bytes()
                path.write_bytes(original + b" ")
                with self.assertRaisesRegex(ValueError, code):
                    c.verify(self.frozen, REPO, **self.kwargs)
                path.write_bytes(original)

    def test_original_parent_freeze_is_reverified(self):
        self.prepare()
        path = self.parent_root / "requests/mini-disabled.json"
        data = json.loads(path.read_bytes())
        data["request"]["messages"][0]["content"] += "changed"
        path.write_bytes(base.encoded(data))
        with self.assertRaisesRegex(ValueError, "FROZEN_REQUEST_CHANGED"):
            c.verify(self.frozen, REPO, **self.kwargs)

    def test_change_after_provider_initialization_blocks_first_spending_call(self):
        plan = self.prepare()
        path = self.frozen / "participant-source.json"
        FakeProvider.on_init = lambda: path.write_bytes(path.read_bytes() + b" ")
        summary = self.run_fake(plan)
        self.assertEqual(summary["status"], "INTERRUPTED")
        self.assertEqual(FakeProvider.total_calls, 0)
        self.assertEqual(summary["unattempted_arms"], list(c.ARMS))

    def test_change_between_arms_blocks_next_spending_call(self):
        plan = self.prepare()
        path = self.parent_record / "direct-disabled/public-answer.txt"
        FakeProvider.after_response = lambda: path.write_bytes(path.read_bytes() + b" ")
        summary = self.run_fake(plan)
        self.assertEqual(summary["status"], "INTERRUPTED")
        self.assertEqual(FakeProvider.total_calls, 1)
        self.assertEqual(summary["unattempted_arms"], ["prompt-control-disabled"])
        self.assertEqual((self.output / "mini-disabled/public-answer.txt").read_bytes(), RAW.encode())

    def test_changed_outbound_messages_refused_before_provider(self):
        plan = self.prepare()
        provider = FakeProvider(base.settings_for("mini-disabled", c.CAP), self.output / "calls")
        checked = c.CheckedProvider(provider, "mini-disabled", self.frozen, REPO, plan["plan_id"], self.parent_root, self.parent_record)
        source = base.read_source(self.frozen / "participant-source.json")
        messages = base.messages_for(source, "mini-disabled")
        messages[1]["content"] += "extra source"
        with self.assertRaisesRegex(ValueError, "PENDING_WIRE_REQUEST_CHANGED"):
            checked.complete(messages, json_output=False, coordinate={"arm": "mini-disabled", "stage": "construct", "cycle": 1, "phase": "raw-prose"})
        self.assertEqual(FakeProvider.total_calls, 0)

    def test_cli_failure_is_nonzero_and_does_not_copy_arbitrary_error_code(self):
        plan = self.prepare()
        FakeProvider.fail_at = 1
        FakeProvider.failure_code = "secret-bearing-untrusted-code"
        argv = ["continuation", "run", "--repo", str(REPO), "--root", str(self.frozen),
                "--parent-root", str(self.parent_root), "--parent-record", str(self.parent_record),
                "--output", str(self.output), "--expected-plan-id", plan["plan_id"]]
        with patch("sys.argv", argv), patch.object(c, "DeepSeek", FakeProvider), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                c.main()
        self.assertEqual(caught.exception.code, 2)
        summary = json.loads((self.output / "summary.json").read_bytes())
        self.assertEqual(summary["arms"][0]["error_code"], "PROVIDER_FAILURE")
        self.assertNotIn("secret-bearing", json.dumps(summary))


if __name__ == "__main__":
    unittest.main()
