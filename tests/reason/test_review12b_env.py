"""Dummy-key-only CLI credential tests; fixtures remain under ignored review12b."""
from __future__ import annotations
from tests.reason import artifact_root
import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import unittest
from unittest import mock
import uuid

from minireason.reason.types import ReasonFailure

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("review12b_reason_cli", ROOT / "tools/reason.py")
cli = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cli)


class EnvironmentFileTests(unittest.TestCase):
    def setUp(self):
        self.directory = artifact_root() / "env-cli/fixtures" / uuid.uuid4().hex[:8]
        self.directory.mkdir(parents=True)
        self.environment = {"EXISTING_NAME": "dummy-existing"}
        self.environment_patch = mock.patch.object(cli.os, "environ", self.environment)
        self.environment_patch.start()
        self.addCleanup(self.environment_patch.stop)

    def fixture(self, text):
        path = self.directory / "dummy.env"
        with path.open("w", encoding="utf-8", newline="") as handle:
            handle.write(text)
        return path

    def refusal(self, path, expected):
        before = dict(self.environment)
        with self.assertRaises(ReasonFailure) as caught:
            cli.load_env_file(path)
        self.assertEqual(caught.exception.code, expected)
        self.assertEqual(self.environment, before)
        return caught.exception

    def test_parser_run_resume_option_defaults_to_none(self):
        run = cli.parser().parse_args(["run", "--problem", "problem.txt", "--cycles", "2"])
        resume = cli.parser().parse_args(["resume", "--run", "runs/example"])
        self.assertIsNone(run.env_file)
        self.assertIsNone(resume.env_file)
        for command in (["run", "--problem", "problem.txt", "--cycles", "2"],
                        ["resume", "--run", "runs/example"]):
            args = cli.parser().parse_args(command + ["--env-file", "keys.local"])
            self.assertEqual(args.env_file, Path("keys.local"))

    def test_none_leaves_environment_unchanged(self):
        cli.load_env_file(None)
        self.assertEqual(self.environment, {"EXISTING_NAME": "dummy-existing"})

    def test_real_git_ignored_file_accepts_only_declared_names(self):
        path = self.fixture("# dummy credentials only\r\nDEEPSEEK_API_KEY=dummy-deepseek\r\n\r\n OLLAMA_API_KEY = 'dummy-ollama=a'\r\n")
        cli.load_env_file(path)
        self.assertEqual(self.environment, {"EXISTING_NAME": "dummy-existing",
                         "DEEPSEEK_API_KEY": "dummy-deepseek", "OLLAMA_API_KEY": "dummy-ollama=a"})

    def test_values_are_literal_without_expansion(self):
        path = self.fixture('DEEPSEEK_API_KEY="dummy-${EXISTING_NAME}=suffix"\n')
        cli.load_env_file(path)
        self.assertEqual(self.environment["DEEPSEEK_API_KEY"], "dummy-${EXISTING_NAME}=suffix")

    def test_tracked_file_is_refused_before_open(self):
        with mock.patch.object(Path, "open", side_effect=AssertionError("Tracked file opened")):
            self.refusal(ROOT / ".gitignore", "ENV_FILE_TRACKED")

    def test_unknown_name_is_atomic_and_value_free(self):
        path = self.fixture("DEEPSEEK_API_KEY=dummy-first\nUNADMITTED_KEY=dummy-forbidden\n")
        failure = self.refusal(path, "ENV_FILE_KEY_NOT_ALLOWED")
        self.assertNotIn("dummy", str(failure))
        self.assertNotIn("UNADMITTED_KEY", str(failure))

    def test_malformed_values_are_atomic(self):
        for final_line in ("bad-line", "OLLAMA_API_KEY=", "OLLAMA_API_KEY='unclosed",
                           "OLLAMA_API_KEY=dummy\x00value", "DEEPSEEK_API_KEY=dummy-duplicate"):
            with self.subTest(kind=final_line.split("=", 1)[0]):
                self.refusal(self.fixture("DEEPSEEK_API_KEY=dummy-first\n" + final_line + "\n"),
                             "ENV_FILE_INVALID")

    def test_unignored_file_is_refused(self):
        path = self.fixture("DEEPSEEK_API_KEY=dummy-only\n")
        with mock.patch.object(cli.subprocess, "run", side_effect=[
                subprocess.CompletedProcess([], 1), subprocess.CompletedProcess([], 1)]):
            self.refusal(path, "ENV_FILE_NOT_IGNORED")

    def test_git_check_failures_are_refused(self):
        path = self.fixture("DEEPSEEK_API_KEY=dummy-only\n")
        for side_effect in ([subprocess.CompletedProcess([], 128)], [OSError("dummy-error")],
                            [subprocess.CompletedProcess([], 1), subprocess.CompletedProcess([], 128)]):
            with mock.patch.object(cli.subprocess, "run", side_effect=side_effect):
                self.refusal(path, "ENV_FILE_GIT_CHECK_FAILED")

    def test_symlink_resolved_tracked_target_is_refused(self):
        path = self.fixture("DEEPSEEK_API_KEY=dummy-only\n")
        with mock.patch.object(Path, "resolve", return_value=ROOT / ".gitignore"):
            self.refusal(path, "ENV_FILE_TRACKED")

    def test_symlink_resolved_outside_target_is_refused(self):
        path = self.fixture("DEEPSEEK_API_KEY=dummy-only\n")
        with mock.patch.object(Path, "resolve", return_value=ROOT.parent / "dummy-outside.env"):
            self.refusal(path, "ENV_FILE_OUTSIDE_REPOSITORY")

    def test_missing_file_is_refused(self):
        self.refusal(self.directory / "missing.env", "ENV_FILE_UNREADABLE")

    def test_run_loads_before_create_and_passes_no_environment_values(self):
        path = self.fixture("DEEPSEEK_API_KEY=dummy-before-create\n")
        def create(*args):
            self.assertEqual(self.environment["DEEPSEEK_API_KEY"], "dummy-before-create")
            self.assertNotIn("dummy-before-create", repr(args))
            return self.directory / "run"
        result = {"run_id": "dummy-run", "stop_reason": "cycle_budget", "completed_cycles": 1, "calls": 1}
        output = io.StringIO()
        with mock.patch.object(cli, "read", return_value="dummy problem"), \
             mock.patch.object(cli, "create_run", side_effect=create) as create_mock, \
             mock.patch.object(cli, "execute", return_value=result), contextlib.redirect_stdout(output):
            code = cli.main(["run", "--problem", "dummy.txt", "--cycles", "1", "--env-file", str(path)])
        self.assertEqual(code, 0)
        self.assertEqual(create_mock.call_count, 1)
        self.assertNotIn("dummy-before-create", output.getvalue())

    def test_resume_loads_before_execute(self):
        path = self.fixture("OLLAMA_API_KEY=dummy-before-resume\n")
        def execute(directory):
            self.assertEqual(self.environment["OLLAMA_API_KEY"], "dummy-before-resume")
            return {"run_id": "dummy-run", "stop_reason": "cycle_budget", "completed_cycles": 1, "calls": 1}
        output = io.StringIO()
        with mock.patch.object(cli, "execute", side_effect=execute), contextlib.redirect_stdout(output):
            code = cli.main(["resume", "--run", "runs/dummy", "--env-file", str(path)])
        self.assertEqual(code, 0)
        self.assertNotIn("dummy-before-resume", output.getvalue())

    def test_cli_refusal_never_calls_engine_or_prints_values(self):
        path = self.fixture("DEEPSEEK_API_KEY=dummy-first\nNOT_ALLOWED=dummy-second\n")
        output = io.StringIO()
        with mock.patch.object(cli, "execute") as execute, mock.patch.object(cli, "create_run") as create, \
             contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code = cli.main(["run", "--problem", "dummy.txt", "--cycles", "1", "--env-file", str(path)])
        self.assertEqual(code, 2)
        self.assertEqual(output.getvalue(), "ENV_FILE_KEY_NOT_ALLOWED\n")
        execute.assert_not_called()
        create.assert_not_called()


if __name__ == "__main__":
    unittest.main()
