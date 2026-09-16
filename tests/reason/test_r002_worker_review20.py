"""Real Windows worker supervision using a replaced offline child executor."""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock
import uuid
from tests.reason import artifact_root
from tests.reason import test_review12_adapter as legacy_fixtures
from minireason.reason import adapter, storage
from minireason.reason.types import ReasonFailure


@unittest.skipUnless(os.name == "nt", "reviewed Windows job backend")
class StrictWorkerReview20Tests(unittest.TestCase):
    def test_timeout_owns_worker_job_and_retains_actual_elapsed(self):
        case = artifact_root() / "strict-worker" / uuid.uuid4().hex[:8]
        case.mkdir(parents=True)
        probe = case / "child.py"
        storage.write(probe, legacy_fixtures.PROBE_CODE)
        actual_popen = subprocess.Popen
        children = []
        def start(command, **kwargs):
            child = actual_popen([sys.executable, "-B", str(probe), "sleep", *command[-2:]], **kwargs)
            children.append(child)
            return child
        safe_env = {"PYTHONPATH": str(Path(__file__).resolve().parents[2] / "src"),
                    "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8",
                    "PYTHONDONTWRITEBYTECODE": "1", "SYSTEMROOT": "C:/Windows",
                    "TMP": "C:/tr20", "TEMP": "C:/tr20", "DEEPSEEK_API_KEY": "offline-placeholder"}
        with mock.patch.object(os, "environ", safe_env), mock.patch.object(adapter.subprocess, "Popen", side_effect=start), mock.patch.object(adapter, "WALL_SECONDS", 0.25):
            with self.assertRaises(ReasonFailure):
                adapter.Adapter("live").call(seat="deepseek-flash", messages=legacy_fixtures.MESSAGES,
                    records_dir=case / "call", coordinate={"strict": True}, role="answer")
        self.assertEqual(len(children), 1)
        self.assertIsNotNone(children[0].poll())
        record = json.loads((case / "call/supervision.json").read_text(encoding="utf-8"))
        self.assertEqual(record["requested_wall_seconds"], 0.25)
        self.assertGreaterEqual(record["elapsed_ms"], 250)
        self.assertLess(record["elapsed_ms"], 3000)
        self.assertEqual(record["limit_breaches"], ["wall_seconds"])
        self.assertEqual(record["termination_backend"], "windows-job-kill-on-close-single-process")
        self.assertIsNotNone(record["exit_code"])
        self.assertTrue((case / "call/worker-failure.json").exists())
