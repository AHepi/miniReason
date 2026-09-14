from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools import run_e028_checkpointed as runner
from tests.test_sql_use_return_study import FakeProvider
from minireason.provider import ProviderFailure


class RecordingPublisher:
    def __init__(self, root, fail_on=None):
        self.root, self.fail_on, self.events = root, fail_on, []

    def publish(self, label):
        self.events.append((label, sorted(path.name for path in self.root.rglob("*.json"))))
        if len(self.events) == self.fail_on:
            raise RuntimeError("untrusted command error must not escape")
        return {"commit": "test", "tree": "test"}


class CheckpointProviderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        FakeProvider.instances = []
        FakeProvider.fail_at = FakeProvider.after_response = FakeProvider.on_init = None
        self.provider = FakeProvider(runner.study.settings(), self.root / "calls")
        self.messages = [{"role": "user", "content": "Exact public text \u03c0\n  retained."}]
        self.coordinate = {"arm": "criticism-returned", "stage": "use_before", "cycle": 1}

    def tearDown(self):
        self.temp.cleanup()

    def complete(self, wrapped):
        return wrapped.complete(self.messages, json_output=False, coordinate=self.coordinate)

    def test_argument_response_parity_and_before_after_evidence(self):
        (self.root / "routed.json").write_text(json.dumps(self.messages), encoding="utf-8")
        publisher = RecordingPublisher(self.root)
        wrapped = runner.CheckpointProvider(self.provider, publisher)
        with patch.object(self.provider, "complete", wraps=self.provider.complete) as complete:
            response = self.complete(wrapped)
        self.assertIs(complete.call_args.args[0], self.messages)
        self.assertIs(complete.call_args.kwargs["coordinate"], self.coordinate)
        self.assertFalse(complete.call_args.kwargs["json_output"])
        self.assertIs(wrapped.settings, self.provider.settings)
        self.assertEqual(wrapped.calls, 1)
        self.assertEqual([event[0] for event in publisher.events], ["before-call-0001", "after-call-0001"])
        self.assertEqual(publisher.events[0][1], ["routed.json"])
        self.assertIn("call-0001.response.json", publisher.events[1][1])
        self.assertEqual(response, json.loads((self.root / "calls/call-0001.response.json").read_bytes()))

    def test_before_publication_failure_latches_without_provider_call(self):
        publisher = RecordingPublisher(self.root, fail_on=1)
        wrapped = runner.CheckpointProvider(self.provider, publisher)
        with self.assertRaisesRegex(runner.CheckpointError, "CHECKPOINT_PUBLICATION_FAILED"):
            self.complete(wrapped)
        with self.assertRaisesRegex(runner.CheckpointError, "PUBLICATION_FAILURE_LATCHED"):
            self.complete(wrapped)
        self.assertEqual(self.provider.calls, 0)
        self.assertEqual(len(publisher.events), 1)

    def test_provider_failure_is_recorded_and_published_without_retry(self):
        FakeProvider.fail_at = 1
        publisher = RecordingPublisher(self.root)
        wrapped = runner.CheckpointProvider(self.provider, publisher)
        with self.assertRaises(ProviderFailure):
            self.complete(wrapped)
        self.assertEqual(self.provider.calls, 1)
        self.assertEqual([event[0] for event in publisher.events], ["before-call-0001", "after-failed-call-0001"])
        response = json.loads((self.root / "calls/call-0001.response.json").read_bytes())
        self.assertEqual(response["status"], "SCRIPTED_OFFLINE_FAILURE")
        self.assertIn("call-0001.response.json", publisher.events[-1][1])

    def test_after_publication_failure_preserves_response_and_blocks_next_call(self):
        publisher = RecordingPublisher(self.root, fail_on=2)
        wrapped = runner.CheckpointProvider(self.provider, publisher)
        with self.assertRaisesRegex(runner.CheckpointError, "CHECKPOINT_PUBLICATION_FAILED"):
            self.complete(wrapped)
        self.assertTrue((self.root / "calls/call-0001.response.json").exists())
        with self.assertRaisesRegex(runner.CheckpointError, "PUBLICATION_FAILURE_LATCHED"):
            self.complete(wrapped)
        self.assertEqual(self.provider.calls, 1)
        self.assertEqual(len(publisher.events), 2)

    def test_existing_output_refuses_before_git_or_provider(self):
        output = self.root / runner.OUTPUT
        output.mkdir(parents=True)
        (output / "preserve").write_bytes(b"unchanged")
        with patch.object(runner, "GitPublisher") as publisher, patch.object(runner.study, "DeepSeek") as provider:
            with self.assertRaisesRegex(runner.CheckpointError, "RECOVERY_OUTPUT_ALREADY_EXISTS"):
                runner.live(self.root, self.root / "work", {})
        publisher.assert_not_called()
        provider.assert_not_called()
        self.assertEqual((output / "preserve").read_bytes(), b"unchanged")

    @unittest.skipUnless(os.name == "posix", "Original Mini directory durability requires POSIX")
    def test_original_six_call_flow_has_twelve_checkpoints(self):
        repo = runner.PortableRepositoryPath(Path(runner.study.__file__).resolve().parents[2])
        publisher = RecordingPublisher(self.root)
        wrapped = runner.CheckpointProvider(self.provider, publisher)
        with patch.object(runner.study, "DeepSeek", return_value=wrapped):
            summary = runner.study.run(repo / runner.PLAN, self.root / "output", repo, runner.PLAN_ID)
        self.assertEqual(summary["status"], "COMPLETE")
        self.assertEqual(summary["provider_calls"], 6)
        self.assertEqual(summary["reused_prefix_responses"], 2)
        self.assertEqual(len(publisher.events), 12)
        self.assertEqual(publisher.events[-1][0], "after-call-0006")

    @unittest.skipUnless(os.name == "posix", "Original preflight and Mini durability require POSIX")
    def test_entrypoint_preflight_then_live_preserves_distinct_real_receipts(self):
        source = Path(runner.study.__file__).resolve().parents[2]
        checkout = self.root / "entrypoint-checkout"
        subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", "--no-local", str(source), str(checkout)],
                       capture_output=True, check=True)
        # Include the implementation under test even before its review commit.
        for name in runner.EXTERNAL_FILES:
            destination = checkout / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / name, destination)
        code = r'''
import json
import os
from pathlib import Path
import subprocess
from unittest.mock import patch
from tools import run_e028_checkpointed as runner
from tests.test_sql_use_return_study import FakeProvider
class OfflinePublisher:
    def __init__(self, repo, source_sha):
        self.repo = repo
    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], text=True).strip()
    def check_source(self):
        pass
    def publish(self, label):
        return {"commit": "scripted-commit", "tree": "scripted-tree"}
repo = Path.cwd()
workspace = repo / "work/e028-preflight"
runner.OUTPUT = Path("work/entrypoint-scripted-recovery")
source_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
FakeProvider.instances = []
FakeProvider.fail_at = FakeProvider.after_response = FakeProvider.on_init = None
with patch.object(runner, "GitPublisher", OfflinePublisher), patch.object(runner.study, "DeepSeek", FakeProvider):
    assert runner.main(["--mode", "preflight", "--repo", str(repo)]) == 0
    first = {path.name: path.read_bytes() for path in workspace.glob("preflight*.json")}
    assert len(first) == 1
    assert FakeProvider.instances == []
    with patch.dict(os.environ, {"GITHUB_REF": "refs/heads/main", "GITHUB_RUN_ATTEMPT": "1",
                                 "GITHUB_SHA": source_sha, "DEEPSEEK_API_KEY": "synthetic-offline-only"}):
        assert runner.main(["--mode", "live", "--repo", str(repo)]) == 0
receipts = {path.name: path.read_bytes() for path in workspace.glob("preflight*.json")}
assert len(receipts) == 2
assert all(receipts[name] == original for name, original in first.items())
assert all(json.loads(raw)["status"] == "OFFLINE_PREFLIGHT_PASSED" for raw in receipts.values())
assert len(FakeProvider.instances) == 1 and FakeProvider.instances[0].calls == 6
summary = json.loads((repo / runner.OUTPUT / "summary.json").read_bytes())
assert summary["status"] == "COMPLETE" and summary["provider_calls"] == 6
assert (workspace / "remote-acknowledgement.json").is_file()
'''
        result = subprocess.run([sys.executable, "-B", "-X", "utf8", "-c", code],
                                cwd=checkout, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class GitPublisherTests(unittest.TestCase):
    def git(self, repo, *args):
        result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=True)
        return result.stdout.decode("utf-8").strip()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.remote, self.repo = self.root / "remote.git", self.root / "checkout"
        self.git(self.root, "init", "--bare", str(self.remote))
        self.git(self.root, "init", "--initial-branch=main", str(self.repo))
        self.git(self.repo, "config", "core.autocrlf", "false")
        self.git(self.repo, "config", "user.name", "Scratch Test Author")
        self.git(self.repo, "config", "user.email", "scratch@example.invalid")
        (self.repo / "docs").mkdir()
        (self.repo / runner.LEDGER).write_bytes(b"Initial ledger\n")
        (self.repo / runner.ACTIVITY).write_bytes(b"")
        self.git(self.repo, "add", "docs")
        self.git(self.repo, "commit", "-m", "Initial scratch source")
        self.git(self.repo, "remote", "add", "origin", str(self.remote))
        self.git(self.repo, "push", "origin", "HEAD:main")
        self.source = self.git(self.repo, "rev-parse", "HEAD")
        self.publisher = runner.GitPublisher(self.repo, self.source)
        self.output = self.repo / runner.OUTPUT
        self.output.mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def test_real_remote_checkpoint_bytes_tree_and_distinct_bot_identity(self):
        evidence = b'{"public":"exact UTF-8 \xcf\x80"}\n'
        (self.output / "response.json").write_bytes(evidence)
        with patch.dict(os.environ, {"GIT_AUTHOR_NAME": "Inherited User", "GIT_AUTHOR_EMAIL": "inherited@example.invalid",
                                     "GIT_COMMITTER_NAME": "Inherited User", "GIT_COMMITTER_EMAIL": "inherited@example.invalid"}):
            acknowledgement = self.publisher.publish("after-call-0001")
        self.assertEqual(self.git(self.remote, "rev-parse", "refs/heads/main"), acknowledgement["commit"])
        self.assertEqual(self.git(self.remote, "rev-parse", "refs/heads/main^{tree}"), acknowledgement["tree"])
        stored = subprocess.check_output(["git", "-C", str(self.remote), "show",
                                          "refs/heads/main:" + runner.OUTPUT.as_posix() + "/response.json"])
        self.assertEqual(stored, evidence)
        self.assertEqual(self.git(self.repo, "log", "-1", "--format=%an <%ae>"),
                         "miniReason Recovery Bot <minireason-recovery@users.noreply.github.com>")
        (self.output / "summary.json").write_bytes(b'{"status":"COMPLETE"}\n')
        second = self.publisher.publish("terminal-complete")
        self.assertNotEqual(acknowledgement["commit"], second["commit"])
        self.assertEqual(self.git(self.remote, "rev-parse", "refs/heads/main"), second["commit"])

    def test_concurrent_remote_advance_refuses_without_overwriting_it(self):
        other = self.root / "other"
        self.git(self.root, "clone", "--branch", "main", str(self.remote), str(other))
        (other / "other.txt").write_bytes(b"concurrent source\n")
        self.git(other, "add", "other.txt")
        self.git(other, "-c", "user.name=Other Bot", "-c", "user.email=other@example.invalid",
                 "commit", "-m", "Concurrent remote advancement")
        self.git(other, "push", "origin", "HEAD:main")
        advanced = self.git(other, "rev-parse", "HEAD")
        (self.output / "response.json").write_bytes(b"preserved locally\n")
        with self.assertRaisesRegex(runner.CheckpointError, "SOURCE_OR_REMOTE_CHANGED"):
            self.publisher.publish("before-call-0001")
        self.assertEqual(self.git(self.remote, "rev-parse", "refs/heads/main"), advanced)
        self.assertEqual(self.git(self.repo, "rev-parse", "HEAD"), self.source)

    def test_unexpected_staged_file_refuses_publication(self):
        (self.repo / "outside.txt").write_bytes(b"outside scope\n")
        self.git(self.repo, "add", "outside.txt")
        with self.assertRaisesRegex(runner.CheckpointError, "UNEXPECTED_STAGED_FILES"):
            self.publisher.publish("before-call-0001")
        self.assertEqual(self.git(self.remote, "rev-parse", "refs/heads/main"), self.source)

    def test_previously_published_output_cannot_be_changed(self):
        record = self.output / "response.json"
        record.write_bytes(b"original\n")
        acknowledged = self.publisher.publish("after-call-0001")
        record.write_bytes(b"changed\n")
        with self.assertRaisesRegex(runner.CheckpointError, "PUBLISHED_OUTPUT_CHANGED"):
            self.publisher.publish("before-call-0002")
        self.assertEqual(self.git(self.remote, "rev-parse", "refs/heads/main"), acknowledged["commit"])

    def test_only_exact_event_log_prefix_appends_are_publishable(self):
        log = self.output / "criticism-returned/mini/log.jsonl"
        log.parent.mkdir(parents=True)
        log.write_bytes(b'{"event":1}\n')
        self.publisher.publish("after-call-0001")
        log.write_bytes(b'{"event":1}\n{"event":2}\n')
        accepted = self.publisher.publish("before-call-0002")
        log.write_bytes(b'{"event":"rewritten"}\n{"event":2}\n')
        with self.assertRaisesRegex(runner.CheckpointError, "PUBLISHED_OUTPUT_CHANGED"):
            self.publisher.publish("before-call-0003")
        self.assertEqual(self.git(self.remote, "rev-parse", "refs/heads/main"), accepted["commit"])

    def test_synthetic_staged_credential_prevents_commit(self):
        synthetic = "synthetic-test-key-do-not-publish-9c17"
        (self.output / "response.json").write_text(synthetic, encoding="utf-8")
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": synthetic}):
            with self.assertRaisesRegex(runner.CheckpointError, "STAGED_CREDENTIAL_DETECTED"):
                self.publisher.publish("after-call-0001")
        self.assertEqual(self.git(self.repo, "rev-parse", "HEAD"), self.source)
        self.assertEqual(self.git(self.remote, "rev-parse", "refs/heads/main"), self.source)

    @unittest.skipUnless(os.name == "posix", "Original Mini directory durability requires POSIX")
    def test_original_full_flow_with_real_verified_git_checkpoints(self):
        self.output.rmdir()
        FakeProvider.instances = []
        FakeProvider.fail_at = FakeProvider.after_response = FakeProvider.on_init = None
        repo = runner.PortableRepositoryPath(Path(runner.study.__file__).resolve().parents[2])
        def factory(settings, records):
            return runner.CheckpointProvider(FakeProvider(settings, records), self.publisher)
        with patch.object(runner.study, "DeepSeek", side_effect=factory):
            summary = runner.study.run(repo / runner.PLAN, self.output, repo, runner.PLAN_ID)
        self.assertEqual((summary["status"], summary["provider_calls"]), ("COMPLETE", 6))
        self.assertEqual(summary["reused_prefix_responses"], 2)
        acknowledgement = self.publisher.publish("terminal-complete")
        self.assertEqual(self.git(self.remote, "rev-parse", "refs/heads/main^{tree}"), acknowledgement["tree"])
        count = self.git(self.repo, "rev-list", "--count", self.source + "..HEAD")
        self.assertEqual(count, "13")
        remote_summary = self.git(self.remote, "show", "refs/heads/main:" + runner.OUTPUT.as_posix() + "/summary.json")
        # Both sides are normalized through JSON: the certified property is that the published
        # remote bytes equal the returned summary as serialized, and the frozen adapter's
        # in-memory stages_entered tuple is unrepairable under its pin (OPS-20260914-STAGES).
        self.assertEqual(json.loads(remote_summary), json.loads(json.dumps(summary)))


if __name__ == "__main__":
    unittest.main()
