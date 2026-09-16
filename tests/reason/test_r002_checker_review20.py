"""Review20 restricted-host containment regressions, no provider calls."""
import json
import os
from pathlib import Path
import unittest
from unittest import mock
import uuid
from tests.reason import artifact_root
from tests.reason import test_r002_checker as fixtures
from minireason.reason import checker


class CheckerReview20Tests(unittest.TestCase):
    def test_profiler_frame_access_is_refused_before_execution(self):
        for source in ("import sys\nsys.setprofile(lambda frame,event,arg: None)",
                       "value = frame.f_back.f_globals", "value = trace.tb_frame"):
            with self.subTest(source=source):
                result = checker.run_checker(fixtures.proposal(checker_source=source))
                self.assertEqual(result["status"], "REFUSED_POLICY")
                self.assertIsNone(result["exit_code"])

    def test_runtime_guard_blocks_profiler_even_without_ast(self):
        source = "import sys\nsys.setprofile(lambda frame,event,arg: None)"
        with mock.patch.object(checker, "_static_policy", return_value=([], [])):
            result = checker.run_checker(fixtures.proposal(checker_source=source))
        self.assertEqual(result["status"], "NONZERO_EXIT")
        self.assertIn("checker reflection denied", result["stderr_utf8"])

    def test_runtime_guard_blocks_outside_directory_mutation(self):
        sentinel = Path(os.environ["TMP"]) / ("review20-mkdir-" + uuid.uuid4().hex)
        child = checker._CHILD.replace(
            'scope = {"__builtins__": builtins.__dict__, "__name__": "__checker__"}',
            'scope = {"__builtins__": builtins.__dict__, "__name__": "__checker__", "host": os}')
        with mock.patch.object(checker, "_CHILD", child):
            result = checker.run_checker(fixtures.proposal(checker_source="host.mkdir(" + repr(str(sentinel)) + ")"))
        self.assertEqual(result["status"], "NONZERO_EXIT")
        self.assertIn("checker filesystem/process denied", result["stderr_utf8"])
        self.assertFalse(sentinel.exists())

    @unittest.skipUnless(os.name == "nt", "review qualification is Windows-specific")
    def test_reviewed_live_host_executes_without_provider(self):
        self.assertTrue(checker.host_qualified())
        evidence = artifact_root() / "qualified-host" / uuid.uuid4().hex[:8]
        result = checker.run_checker(fixtures.proposal(), mode="live", evidence_dir=evidence)
        self.assertEqual(result["status"], "COMPLETE")
        self.assertEqual(result["comparison"], "agrees")
        self.assertEqual(result["runtime_sha256"], checker.REVIEWED_RUNTIME_SHA256)

    def test_wrong_runtime_digest_remains_unqualified(self):
        self.assertFalse(checker.host_qualified("0" * 64))
