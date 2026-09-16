"""R002 CLI interfaces remain strict and offline env paths are inert."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
from tests.reason import artifact_root
from minireason.reason.storage import write
from minireason.reason.types import ReasonFailure

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("r002_cli_fixture", ROOT / "tools/reason.py")
cli = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cli)


class R002CliTests(unittest.TestCase):
    def test_flags_bind_without_reading_env_path(self):
        parsed = cli.parser().parse_args(["run-r002-native", "--problem", "C01.txt",
            "--relations", "registry.json", "--out", "out", "--env-file", "does-not-exist.env"])
        self.assertEqual(parsed.completion_tokens, 32768)
        self.assertEqual(parsed.prompt_token_cap, 32768)
        self.assertEqual(parsed.attempt_policy, "strict")
        self.assertEqual(parsed.mode, "offline")
        self.assertEqual(parsed.retry_transport, 0)

    def test_run_refuses_retry_before_reading_problem_or_env(self):
        with patch.object(cli, "load_env_file", side_effect=AssertionError("credential read")):
            self.assertEqual(cli.main(["run-r002-native", "--problem", "absent.txt",
                "--relations", "absent.json", "--out", "unused", "--env-file", ".env",
                "--retry-transport", "1"]), 2)

    def test_offline_native_ignores_nonexistent_env(self):
        from minireason.reason.config import R002_DIR
        import uuid
        out = artifact_root() / "cli" / uuid.uuid4().hex[:8]
        with patch.object(cli, "load_env_file", side_effect=AssertionError("credential read")):
            result = cli.main(["run-r002-native", "--problem", str(R002_DIR / "problems/C01.txt"),
                "--relations", str(R002_DIR / "problems/RELATIONS.json"), "--out", str(out),
                "--env-file", str(out / "does-not-exist.env")])
            self.assertEqual(result, 0)
            self.assertEqual(cli.main(["resume", "--run", str(out), "--env-file", ".env"]), 0)
        self.assertTrue((out / "RUN.md").is_file())
