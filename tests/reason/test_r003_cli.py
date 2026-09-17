"""R003 strict CLI plumbing stays additive and keeps credentials at the call boundary."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import unittest
import uuid
from unittest import mock

from minireason.reason import engine
from minireason.reason.types import ReasonFailure
from tests.reason import artifact_root


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("r003_reason_cli", ROOT / "tools/reason.py")
cli = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cli)


class R003CliTests(unittest.TestCase):
    def base(self, command="run-r002"):
        args = [command, "--problem", "O01.txt", "--relations", "relations.json",
                "--out", "out"]
        if command == "run-r002":
            args += ["--recipe", "recipe.json", "--fork-registry", "forks.json"]
        return args

    def invoke(self, argv):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code = cli.main(argv)
        return code, output.getvalue()

    def test_parser_adds_profile_and_registry_without_changing_r002_defaults(self):
        legacy = cli.parser().parse_args(self.base())
        self.assertIsNone(legacy.study_profile)
        self.assertIsNone(legacy.canonical_registry)
        self.assertIsNone(legacy.coding_manifest)
        selected = cli.parser().parse_args(self.base() + [
            "--study-profile", "r003-open-v1", "--canonical-registry", "canonical.json"])
        self.assertEqual(selected.study_profile, "r003-open-v1")
        self.assertEqual(selected.canonical_registry, Path("canonical.json"))

    def test_offline_loop_forwards_r003_profile_and_opaque_env_path(self):
        run = artifact_root() / "r003-cli" / uuid.uuid4().hex[:8]
        captured = {}

        def create(*args, **kwargs):
            captured.update(kwargs)
            return run

        complete = {"run_id": "fixture", "stop_reason": "complete", "completed_cycles": 3, "calls": 14}
        with mock.patch.object(cli, "read", return_value="offline prose problem"), \
             mock.patch.object(cli, "load_env_file", side_effect=AssertionError("env file read offline")), \
             mock.patch.object(engine, "create_r002_run", side_effect=create), \
             mock.patch.object(engine, "execute_r002", return_value=complete):
            code, output = self.invoke(self.base() + ["--study-profile", "r003-open-v1",
                "--canonical-registry", "canonical.json", "--env-file", "missing.env"])
        self.assertEqual(code, 0, output)
        self.assertEqual(captured["study_profile"], "r003-open-v1")
        self.assertEqual(captured["canonical_registry"], Path("canonical.json"))
        self.assertIsNone(captured["coding_manifest"])

    def test_offline_native_forwards_r003_profile_and_registry(self):
        run = artifact_root() / "r003-cli" / uuid.uuid4().hex[:8]
        captured = {}

        def create(*args, **kwargs):
            captured.update(kwargs)
            return run

        complete = {"run_id": "fixture", "stop_reason": "complete", "completed_cycles": 1, "calls": 1}
        with mock.patch.object(cli, "read", return_value="offline prose problem"), \
             mock.patch.object(engine, "create_r002_native_run", side_effect=create), \
             mock.patch.object(engine, "execute_r002", return_value=complete):
            code, output = self.invoke(self.base("run-r002-native") + [
                "--study-profile", "r003-open-v1", "--canonical-registry", "canonical.json"])
        self.assertEqual(code, 0, output)
        self.assertEqual(captured["study_profile"], "r003-open-v1")
        self.assertEqual(captured["canonical_registry"], Path("canonical.json"))

    def test_legacy_r002_forwards_none_and_leaves_core_to_require_coding(self):
        def create(*args, **kwargs):
            self.assertIsNone(kwargs["study_profile"])
            self.assertIsNone(kwargs["canonical_registry"])
            self.assertIsNone(kwargs["coding_manifest"])
            raise ReasonFailure("CONFIG_ERROR", "legacy coding manifest is required")

        with mock.patch.object(cli, "read", return_value="legacy problem"), \
             mock.patch.object(cli, "load_env_file", side_effect=AssertionError("credential read")), \
             mock.patch.object(engine, "create_r002_run", side_effect=create), \
             mock.patch.object(engine, "execute_r002") as execute:
            code, output = self.invoke(self.base())
        self.assertEqual((code, output), (2, "CONFIG_ERROR\n"))
        execute.assert_not_called()

    def test_live_r003_missing_env_refuses_before_problem_core_or_provider(self):
        with mock.patch.object(cli, "read", side_effect=AssertionError("problem read")), \
             mock.patch.object(cli, "load_env_file", side_effect=AssertionError("credential read")), \
             mock.patch.object(engine, "create_r002_native_run") as create, \
             mock.patch.object(engine, "execute_r002") as execute:
            code, output = self.invoke(self.base("run-r002-native") + [
                "--study-profile", "r003-open-v1", "--canonical-registry", "canonical.json",
                "--mode", "live", "--capability", "capability.json",
                "--tokenizer-pins", "tokenizers.json"])
        self.assertEqual((code, output), (2, "CONFIG_ERROR\n"))
        create.assert_not_called()
        execute.assert_not_called()

    def test_live_core_gates_precede_env_read_and_provider(self):
        for failure in ("CAPABILITY_REFUSED", "TOKENIZER_UNAVAILABLE"):
            with self.subTest(failure=failure), \
                 mock.patch.object(cli, "read", return_value="live prose problem"), \
                 mock.patch.object(cli, "load_env_file", side_effect=AssertionError("credential read")), \
                 mock.patch.object(engine, "create_r002_native_run",
                                   side_effect=ReasonFailure(failure, "fixture gate")), \
                 mock.patch.object(engine, "execute_r002") as execute:
                code, output = self.invoke(self.base("run-r002-native") + [
                    "--study-profile", "r003-open-v1", "--canonical-registry", "canonical.json",
                    "--mode", "live", "--env-file", "named.env"])
            self.assertEqual((code, output), (2, failure + "\n"))
            execute.assert_not_called()

    def test_live_r003_clears_inherited_keys_then_loads_named_file_at_callback(self):
        run = artifact_root() / "r003-cli" / uuid.uuid4().hex[:8]
        environment = {"DEEPSEEK_API_KEY": "dummy-inherited", "UNRELATED": "dummy-kept"}
        events = []

        def load(path):
            self.assertEqual(path, Path("named.env"))
            self.assertNotIn("DEEPSEEK_API_KEY", environment)
            self.assertNotIn("OLLAMA_API_KEY", environment)
            environment["DEEPSEEK_API_KEY"] = "dummy-from-named-file"
            events.append("loaded")

        def execute(directory, before_call):
            self.assertEqual(events, [])
            before_call()
            self.assertEqual(events, ["loaded"])
            return {"run_id": "fixture", "stop_reason": "complete", "completed_cycles": 1, "calls": 1}

        with mock.patch.object(cli, "read", return_value="live prose problem"), \
             mock.patch.object(cli.os, "environ", environment), \
             mock.patch.object(cli, "load_env_file", side_effect=load), \
             mock.patch.object(engine, "create_r002_native_run", return_value=run), \
             mock.patch.object(engine, "execute_r002", side_effect=execute):
            code, output = self.invoke(self.base("run-r002-native") + [
                "--study-profile", "r003-open-v1", "--canonical-registry", "canonical.json",
                "--mode", "live", "--env-file", "named.env", "--capability", "capability.json",
                "--tokenizer-pins", "tokenizers.json"])
        self.assertEqual(code, 0, output)
        self.assertNotIn("dummy-inherited", output)
        self.assertNotIn("dummy-from-named-file", output)
        self.assertEqual(environment["UNRELATED"], "dummy-kept")

    def test_resume_recognizes_saved_r003_profile_and_prompt_contract(self):
        for identity in ({"study_profile": "r003-open-v1", "prompt_contract": "future-contract"},
                         {"prompt_contract": "r003-open-v1"}):
            with self.subTest(identity=identity):
                run = artifact_root() / "r003-cli-resume" / uuid.uuid4().hex[:8]
                run.mkdir(parents=True)
                config = {**identity, "mode": "offline"}
                with (run / "config.json").open("w", encoding="utf-8", newline="") as handle:
                    json.dump(config, handle)
                complete = {"run_id": "fixture", "stop_reason": "complete",
                            "completed_cycles": 1, "calls": 1}
                with mock.patch.object(cli, "load_env_file",
                                       side_effect=AssertionError("env file read offline")), \
                     mock.patch.object(engine, "execute_r002", return_value=complete) as strict, \
                     mock.patch.object(cli, "execute") as legacy:
                    code, output = self.invoke(["resume", "--run", str(run),
                                                "--env-file", "missing.env"])
                self.assertEqual(code, 0, output)
                strict.assert_called_once()
                legacy.assert_not_called()

    def test_live_r003_resume_requires_env_before_engine_or_load(self):
        run = artifact_root() / "r003-cli-resume" / uuid.uuid4().hex[:8]
        run.mkdir(parents=True)
        with (run / "config.json").open("w", encoding="utf-8", newline="") as handle:
            json.dump({"study_profile": "r003-open-v1", "mode": "live"}, handle)
        with mock.patch.object(cli, "load_env_file", side_effect=AssertionError("credential read")), \
             mock.patch.object(engine, "execute_r002") as execute:
            code, output = self.invoke(["resume", "--run", str(run)])
        self.assertEqual((code, output), (2, "CONFIG_ERROR\n"))
        execute.assert_not_called()


if __name__ == "__main__":
    unittest.main()
