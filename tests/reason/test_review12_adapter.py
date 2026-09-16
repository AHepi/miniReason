"""Judge regressions: explicit control and real Windows worker lifecycle."""
from pathlib import Path
from tests.reason import artifact_root
import json
import os
import subprocess
import sys
import time
import unittest
import uuid
from unittest import mock
from minireason import provider_openai_compat as provider
from minireason.reason import adapter, config, storage
from minireason.reason.types import ReasonFailure

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = artifact_root() / "adapter-test-runs"
PROBE_CODE = '"""Offline subprocess probe, never creates a provider."""\nimport sys, time\nfrom pathlib import Path\nfrom minireason.reason import worker\nfrom minireason.reason.adapter import _write\nfrom minireason.reason.storage import run_lock\nmode = sys.argv[1]\nif mode == "lock":\n    with run_lock(sys.argv[2]):\n        with Path(sys.argv[3]).open("w", encoding="utf-8", newline="") as f:\n            f.write("lock acquired\\n")\n        time.sleep(30)\nelse:\n    def execute(prepared, records):\n        if mode == "sleep":\n            time.sleep(5)\n        elif mode == "large":\n            print("X" * 2097152)\n            print("Y" * 2097152, file=sys.stderr)\n            _write(records / "call-0001.response.json", {\n                "status": "COMPLETE", "content": "X" * 2097152,\n                "usage": {"prompt_tokens": 1, "completion_tokens": 1}})\n        else:\n            raise AssertionError("Unknown offline probe mode")\n    worker._execute = execute\n    sys.argv = [sys.argv[0], *sys.argv[2:]]\n    raise SystemExit(worker.main())\n'
MESSAGES = [{"role": "user", "content": "Return JSON for a public test problem."}]


class AdapterJudgeTests(unittest.TestCase):
    def setUp(self):
        self.case = ARTIFACTS / uuid.uuid4().hex[:8]
        self.case.mkdir(parents=True)
        self.probe = self.case / "child.py"
        storage.write(self.probe, PROBE_CODE)
        # Replace rather than copy the ambient environment: real keys are never read.
        safe_env = {"PYTHONPATH": str(ROOT / "src"), "PYTHONUTF8": "1",
                    "TMP": r"C:\tr12", "TEMP": r"C:\tr12",
                    "SYSTEMROOT": r"C:\Windows"}
        patcher = mock.patch.object(os, "environ", safe_env)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.live_guard = mock.patch.object(provider.OpenAICompatProvider, "__init__",
                                             side_effect=AssertionError("Live provider forbidden"))
        self.network_guard = mock.patch.object(provider, "_open",
                                              side_effect=AssertionError("Network forbidden"))
        self.live_guard.start()
        self.network_guard.start()
        self.addCleanup(self.live_guard.stop)
        self.addCleanup(self.network_guard.stop)

    def test_shipped_seats_declare_supported_native_thinking(self):
        for name in ("single-family", "cross-family", "cross-family-rival"):
            recipe = config.load_recipe(name)["data"]
            seats = recipe["seats"]
            for seat in [seats["conjecture"], *seats["critics"], seats["use"], seats["rival"]]:
                if seat is None:
                    continue
                endpoint = config.endpoint_for(seat)
                self.assertEqual(endpoint.timeout_seconds, 300)
                expected = "native" if endpoint.family == "deepseek" else "off"
                self.assertEqual(config.thinking_for(seat), expected)
                prepared = adapter.Adapter().prepare(seat=seat, messages=MESSAGES)
                self.assertEqual(prepared["thinking"], expected)
                self.assertEqual(prepared["payload"]["model"], endpoint.model)
                if expected == "native":
                    self.assertEqual(prepared["payload"]["thinking"], {"type": "enabled"})
                    self.assertEqual(prepared["payload"]["reasoning_effort"], "medium")
                else:
                    self.assertTrue(endpoint.native)
                    self.assertIs(prepared["payload"]["think"], False)
                    self.assertEqual(prepared["kwargs"]["extra"], {"think": False})
                    self.assertNotIn("thinking", prepared["payload"])
                    self.assertNotIn("reasoning_effort", prepared["payload"])

    def test_legacy_name_and_boolean_override_still_have_honest_control(self):
        direct = adapter.Adapter().prepare(seat="deepseek-flash", messages=MESSAGES)
        self.assertEqual(direct["thinking"], "native")
        for setting in (False, "off"):
            bare = adapter.Adapter().prepare(seat="deepseek-flash", messages=MESSAGES, thinking=setting)
            self.assertEqual(bare["payload"]["thinking"], {"type": "disabled"})
            self.assertEqual(bare["thinking"], "off")
        with self.assertRaises(ReasonFailure) as error:
            adapter.Adapter().prepare(seat="ollama/qwen3.5-397b", messages=MESSAGES, thinking="native")
        self.assertEqual(error.exception.code, "CONFIG_ERROR")

    def test_native_schema_repair_keeps_public_messages_and_controls(self):
        from minireason.reason import prompts
        original = prompts.render("conjecture", "A public difficult problem.")
        repaired = prompts.repair(original, "Malformed public answer", "conjecture")
        first = adapter.Adapter().prepare(seat="deepseek-flash", messages=original)
        second = adapter.Adapter().prepare(seat="deepseek-flash", messages=repaired)
        self.assertEqual(first["kwargs"], second["kwargs"])
        self.assertEqual(second["messages"][:len(original)], original)
        self.assertEqual(second["messages"][-2], {"role": "assistant", "content": "Malformed public answer"})
        self.assertEqual(second["payload"]["thinking"], {"type": "enabled"})
        self.assertEqual(json.loads(second["wire_body_text"]), second["payload"])
        self.assertNotIn("reasoning_content", second["wire_body_text"])

    def test_bad_recipe_thinking_refused(self):
        data = config.load_recipe("cross-family")["data"]
        data["seats"]["conjecture"]["thinking"] = "invalid"
        with self.assertRaises(ReasonFailure):
            config.validate_recipe(data)
        data["seats"]["conjecture"].pop("thinking")
        with self.assertRaises(ReasonFailure):
            config.validate_recipe(data)

    def test_missing_keys_refuse_before_spawn_or_socket(self):
        for seat in ("deepseek-flash", "ollama/qwen3.5-397b"):
            with mock.patch.object(adapter.subprocess, "Popen") as spawn:
                with self.assertRaises(ReasonFailure) as error:
                    adapter.Adapter("live").call(seat=seat, messages=MESSAGES, records_dir=self.case / seat.replace("/", "_"))
                self.assertEqual(error.exception.code, "KEY_MISSING")
                spawn.assert_not_called()

    def _run_worker_probe(self, mode, wall):
        os.environ["DEEPSEEK_API_KEY"] = "offline-placeholder"
        original = subprocess.Popen
        children = []
        def start(command, **kwargs):
            self.assertEqual(command[3:5], ["-m", "minireason.reason.worker"])
            self.assertIs(kwargs["stdout"], subprocess.DEVNULL)
            self.assertIs(kwargs["stderr"], subprocess.DEVNULL)
            child = original([sys.executable, str(self.probe), mode, *command[-2:]], **kwargs)
            children.append(child)
            return child
        started = time.monotonic()
        with mock.patch.object(adapter.subprocess, "Popen", side_effect=start):
            with mock.patch.object(adapter, "WALL_SECONDS", wall):
                try:
                    result = adapter.Adapter("live").call(seat="deepseek-flash", messages=MESSAGES, records_dir=self.case / mode)
                except ReasonFailure as error:
                    result = error
        elapsed = time.monotonic() - started
        self.assertEqual(len(children), 1)
        self.assertIsNotNone(children[0].poll())
        storage.write(self.case / "process-evidence.json", json.dumps({"mode": mode, "elapsed_seconds": elapsed, "wall_seconds": wall, "child_returncode": children[0].returncode}) + "\n")
        return result, elapsed

    def test_real_sleeping_worker_killed_at_short_wall(self):
        result, elapsed = self._run_worker_probe("sleep", 0.75)
        self.assertIsInstance(result, ReasonFailure)
        self.assertEqual(result.code, "TRANSPORT_OR_RESPONSE_ERROR")
        self.assertLess(elapsed, 3)
        self.assertTrue((self.case / "sleep" / "worker-failure.json").exists())

    def test_large_child_output_has_no_pipe_deadlock(self):
        result, elapsed = self._run_worker_probe("large", 5)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["status"], "COMPLETE")
        self.assertEqual(len(result["content"]), 2097152)
        self.assertLess(elapsed, 5)

    def test_actual_module_entry_imports_and_refuses_offline_spec(self):
        spec = self.case / "spec.json"
        storage.put(spec, {"mode": "offline"})
        completed = subprocess.run([sys.executable, "-X", "utf8", "-m", "minireason.reason.worker", str(spec), str(self.case / "module")],
                                   stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                   env=os.environ, timeout=5)
        self.assertEqual(completed.returncode, 1)
        failure = storage.get(self.case / "module" / "worker-failure.json")
        self.assertEqual(failure["code"], "CONFIG_ERROR")

    def test_process_lock_releases_after_forced_crash(self):
        locked = self.case / "locked"
        locked.mkdir()
        marker = self.case / "acquired.txt"
        child = subprocess.Popen([sys.executable, str(self.probe), "lock", str(locked), str(marker)],
                                 stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                 env=os.environ)
        try:
            deadline = time.monotonic() + 5
            while not marker.exists() and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertTrue(marker.exists())
            with self.assertRaises(RuntimeError):
                with storage.run_lock(locked):
                    pass
            child.kill()
            child.wait(timeout=5)
            with storage.run_lock(locked):
                storage.write(self.case / "lock-reacquired.txt", "Lock reacquired after child crash.\n")
        finally:
            if child.poll() is None:
                child.kill()
                child.wait(timeout=5)


if __name__ == "__main__":
    unittest.main()
