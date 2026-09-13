from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[1]


class ActivityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "tools").mkdir()
        (self.root / "docs").mkdir()
        self.script = self.root / "tools" / "repo_activity.py"
        shutil.copyfile(REPO / "tools" / "repo_activity.py", self.script)
        self.log = self.root / "docs" / "AGENT_ACTIVITY.jsonl"
        self.args = [
            sys.executable, str(self.script), "--agent", "test",
            "--decision", "offline-test", "--action", "exercise logger",
            "--why", "verify receipts", "--goal", "preserve activity",
            "--paths", "example.py",
        ]

    def read_events(self):
        raw = self.log.read_bytes()
        self.assertTrue(raw.endswith(b"\n"))
        return [json.loads(line) for line in raw.decode("utf-8").splitlines()]

    def load_logger(self):
        spec = importlib.util.spec_from_file_location("isolated_activity", self.script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def run_logger(self, *command):
        return subprocess.run(
            [*self.args, *command], capture_output=True, text=True, timeout=30,
        )

    def test_concurrent_processes_preserve_complete_utf8_records(self):
        worker = """
import sys
sys.path.insert(0, sys.argv[1])
import repo_activity
sys.stdin.readline()
for sequence in range(20):
    repo_activity.append({"worker": int(sys.argv[2]), "sequence": sequence,
                          "text": "\u03c0\U0001f680\u6f22\\n" * 8192})
"""
        processes = []
        try:
            for worker_id in range(6):
                processes.append(subprocess.Popen(
                    [sys.executable, "-c", worker, str(self.script.parent), str(worker_id)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True,
                ))
            for process in processes:
                process.stdin.write("\n")
                process.stdin.flush()
            for process in processes:
                stdout, stderr = process.communicate(timeout=45)
                self.assertEqual(process.returncode, 0, stdout + stderr)
        finally:
            for process in processes:
                if process.poll() is None:
                    process.kill()
                process.communicate()
        events = self.read_events()
        self.assertEqual(len(events), 120)
        self.assertEqual(
            {(event["worker"], event["sequence"]) for event in events},
            {(worker_id, sequence) for worker_id in range(6) for sequence in range(20)},
        )
        for event in events:
            self.assertEqual(event["text"], "\u03c0\U0001f680\u6f22\n" * 8192)
            self.assertTrue(event["timestamp_utc"].endswith("+00:00"))

    def test_native_lock_blocks_receipt_and_command_until_release(self):
        holder_code = """
import os
import sys
with open(sys.argv[1], "ab", buffering=0) as handle:
    handle.seek(0)
    if os.name == "nt":
        import msvcrt
        msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
    else:
        import fcntl
        fcntl.flock(handle, fcntl.LOCK_EX)
    print("locked", flush=True)
    sys.stdin.readline()
"""
        holder = subprocess.Popen(
            [sys.executable, "-c", holder_code, str(self.log)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        writer = None
        try:
            self.assertEqual(holder.stdout.readline().strip(), "locked")
            marker = self.root / "command-ran"
            writer = subprocess.Popen(
                [*self.args, "--", sys.executable, "-c",
                 "from pathlib import Path; import sys; Path(sys.argv[1]).touch()", str(marker)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            with self.assertRaises(subprocess.TimeoutExpired):
                writer.wait(timeout=0.25)
            self.assertFalse(marker.exists())
            holder.communicate(input="\n", timeout=30)
            stdout, stderr = writer.communicate(timeout=30)
            self.assertEqual(writer.returncode, 0, stdout + stderr)
            self.assertTrue(marker.exists())
            self.assertEqual([event["phase"] for event in self.read_events()], ["begin", "outcome"])
        finally:
            for process in (holder, writer):
                if process is not None:
                    if process.poll() is None:
                        process.kill()
                    process.communicate()

    def test_short_writes_finish_one_complete_record(self):
        logger = self.load_logger()
        with self.log.open("ab", buffering=0) as handle:
            writer = unittest.mock.Mock(wraps=handle)
            writer.write.side_effect = lambda data: handle.write(data[:7])
            with patch.object(logger, "LOG") as log:
                log.open.return_value.__enter__.return_value = writer
                logger.append({"text": "\u03c0\U0001f680\u6f22" * 20})
            self.assertGreater(writer.write.call_count, 1)
        self.assertEqual(self.read_events()[0]["text"], "\u03c0\U0001f680\u6f22" * 20)

    def test_write_failure_prevents_dispatch_and_releases_lock(self):
        logger = self.load_logger()
        with self.log.open("ab", buffering=0) as handle:
            writer = unittest.mock.Mock(wraps=handle)
            writer.write.side_effect = OSError("write failed")
            with patch.object(logger, "LOG") as log, \
                    patch.object(sys, "argv", self.args[1:] + ["--", "unused"]), \
                    patch.object(logger.subprocess, "run") as run:
                log.open.return_value.__enter__.return_value = writer
                with self.assertRaisesRegex(OSError, "write failed"):
                    logger.main()
            run.assert_not_called()
            # A separate process must acquire the released lock while this handle
            # remains open, so close-on-error cannot conceal a missing unlock.
            result = self.run_logger()
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(self.read_events()), 1)

    def test_event_mode_preserves_existing_bytes(self):
        existing = b'{"prior":true}\n'
        self.log.write_bytes(existing)
        result = self.run_logger("--phase", "outcome")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.log.read_bytes().startswith(existing))
        events = self.read_events()
        self.assertEqual(len(events), 2)
        self.assertEqual(events[1]["phase"], "outcome")
        self.assertEqual(events[1]["paths"], ["example.py"])

    def test_wrapper_returns_child_exit_and_records_both_phases(self):
        result = self.run_logger("--", sys.executable, "-c", "raise SystemExit(7)")
        self.assertEqual(result.returncode, 7, result.stderr)
        begin, outcome = self.read_events()
        self.assertEqual(begin["phase"], "begin")
        self.assertEqual(outcome["phase"], "outcome")
        self.assertEqual(outcome["returncode"], 7)
        self.assertEqual(begin["event_id"], outcome["event_id"])
        self.assertEqual(begin["command_sha256"], outcome["command_sha256"])
        self.assertNotIn("raise SystemExit", self.log.read_text(encoding="utf-8"))

    def test_wrapper_records_command_start_failure(self):
        result = self.run_logger("--", str(self.root / "missing-command"))
        self.assertNotEqual(result.returncode, 0)
        begin, outcome = self.read_events()
        self.assertEqual(begin["phase"], "begin")
        self.assertEqual(outcome["phase"], "outcome")
        self.assertEqual(outcome["error_type"], "FileNotFoundError")
        self.assertEqual(outcome["event_id"], begin["event_id"])

    def test_wrapper_records_interruption_and_reraises(self):
        logger = self.load_logger()
        with patch.object(sys, "argv", self.args[1:] + ["--", "unused"]), \
                patch.object(logger.subprocess, "run", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                logger.main()
        begin, outcome = self.read_events()
        self.assertEqual(outcome["error_type"], "KeyboardInterrupt")
        self.assertEqual(outcome["phase"], "outcome")
        self.assertEqual(outcome["event_id"], begin["event_id"])

    def test_unwritable_log_prevents_command_dispatch(self):
        self.log.mkdir()
        marker = self.root / "command-ran"
        result = self.run_logger(
            "--", sys.executable, "-c",
            "from pathlib import Path; import sys; Path(sys.argv[1]).touch()", str(marker),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(marker.exists())

    def test_lock_failure_prevents_write_and_command_dispatch(self):
        logger = self.load_logger()
        lock_module = logger.msvcrt if sys.platform == "win32" else logger.fcntl
        lock_name = "locking" if sys.platform == "win32" else "flock"
        with patch.object(sys, "argv", self.args[1:] + ["--", "unused"]), \
                patch.object(lock_module, lock_name, side_effect=OSError("lock failed")), \
                patch.object(logger.subprocess, "run") as run:
            with self.assertRaisesRegex(OSError, "lock failed"):
                logger.main()
        run.assert_not_called()
        self.assertEqual(self.log.read_bytes(), b"")


if __name__ == "__main__":
    unittest.main()
