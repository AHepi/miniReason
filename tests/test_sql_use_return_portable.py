from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools import run_sql_use_return as entrypoint
from tests.test_sql_use_return_study import FakeProvider

study = entrypoint.study
REPO = Path(study.__file__).resolve().parents[2]
FROZEN = REPO / "experiments/plans/E028-sql-use-return"
PLAN_ID = "0e7ada3e11b348b7c3ea46805910ece3e14fdb700975e6a22b58b44c82569b5f"


class PortableUseReturnTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.output = self.root / "output"
        FakeProvider.instances = []
        FakeProvider.fail_at = FakeProvider.after_response = FakeProvider.on_init = None

    def tearDown(self):
        self.temp.cleanup()

    def call_cli(self, operation, *, root=FROZEN, extra=()):
        argv = [operation, "--repo", str(REPO), "--root", str(root), *extra]
        with redirect_stdout(io.StringIO()) as stdout:
            code = entrypoint.main(argv)
        return code, json.loads(stdout.getvalue())

    def run_cli(self, *, plan_id=PLAN_ID):
        return self.call_cli("run", extra=("--output", str(self.output),
                                          "--expected-plan-id", plan_id))

    def test_original_frozen_identity_verifies_without_provider(self):
        with patch.object(study, "DeepSeek") as provider:
            code, result = self.call_cli("verify")
        provider.assert_not_called()
        self.assertEqual(code, 0)
        self.assertEqual(result["plan_id"], PLAN_ID)
        self.assertEqual(result["provider_calls"], 0)

    def test_native_absolute_equality_and_relative_metadata(self):
        portable = entrypoint.PortableRepositoryPath(REPO)
        self.assertEqual(portable, REPO)
        self.assertEqual(hash(portable), hash(REPO))
        path = portable / "src/minireason/provider.py"
        self.assertEqual(path.resolve(), (REPO / "src/minireason/provider.py").resolve())
        self.assertEqual(str(path.relative_to(portable)), "src/minireason/provider.py")
        self.assertIsInstance(path.relative_to(portable), Path)
        self.assertTrue(all(isinstance(item, entrypoint.PortableRepositoryPath)
                            for item in (portable / "src/creib").rglob("*.py")))

    @unittest.skipUnless(os.name == "posix", "Frozen directory fsync requires a POSIX host")
    def test_prepare_keeps_original_identity_and_offline_preflight(self):
        frozen = self.root / "prepared"
        with patch.object(study, "DeepSeek") as provider:
            code, result = self.call_cli("prepare", root=frozen)
        provider.assert_not_called()
        self.assertEqual((code, result["plan_id"]), (0, PLAN_ID))
        preflight = json.loads((frozen / "preflight.json").read_bytes())
        self.assertEqual(preflight["provider_calls"], 0)
        self.assertEqual(preflight["scripted_engine_calls"], 8)
        self.assertEqual(preflight["scripted_unique_responses"], 6)

    @unittest.skipUnless(os.name == "posix", "Frozen directory fsync requires a POSIX host")
    def test_eight_stages_six_unique_calls_and_unicode_request_parity(self):
        with patch.object(study, "DeepSeek", FakeProvider):
            code, result = self.run_cli()
        self.assertEqual((code, result["status"]), (0, "COMPLETE"))
        summary = json.loads((self.output / "summary.json").read_bytes())
        self.assertEqual(len(FakeProvider.instances), 1)
        provider = FakeProvider.instances[0]
        self.assertEqual((provider.calls, summary["provider_calls"]), (6, 6))
        self.assertEqual(summary["reused_prefix_responses"], 2)
        self.assertEqual(sum(row["outcome"]["calls"] for row in summary["arms"]), 8)
        self.assertEqual([row["unique_provider_calls"] for row in summary["arms"]], [4, 2])
        self.assertEqual([row["coordinate"]["stage"] for row in provider.requests],
                         list(study.STAGES) + list(study.STAGES[2:]))
        system = (FROZEN / "system.txt").read_bytes().decode("utf-8")
        self.assertTrue(any(ord(character) > 127 for character in system))
        for request in provider.requests:
            coordinate = request["coordinate"]
            self.assertEqual(request["messages"][0]["content"], system)
            route_path = self.output / coordinate["arm"] / "routed" / (coordinate["stage"] + ".json")
            route = json.loads(route_path.read_bytes())
            self.assertEqual(route["request"], study.base.payload_for(request["messages"], study.settings()))
        for arm in summary["arms"]:
            self.assertEqual([row["stage"] for row in arm["custody"]], list(study.STAGES))
            for occurrence in arm["history"]:
                raw = (self.output / arm["arm"] / (occurrence["stage"] + ".txt")).read_bytes()
                self.assertIn("\u03c0\n  Uncertainty remains.", raw.decode("utf-8"))
                self.assertEqual(study.base.sha(raw), occurrence["text_sha256"])
        for stage in study.STAGES[:2]:
            routes = [json.loads((self.output / arm / "routed" / (stage + ".json")).read_bytes())
                      for arm in study.ARMS]
            self.assertEqual(routes[0]["request"], routes[1]["request"])
            self.assertEqual(routes[0]["mini_brief"], routes[1]["mini_brief"])
        self.assertIn("\u03c0", provider.requests[1]["messages"][1]["content"])

    def test_wrong_pin_rejects_before_provider_or_output(self):
        with patch.object(study, "DeepSeek") as provider:
            with self.assertRaisesRegex(ValueError, "EXTERNALLY_PINNED_PLAN_ID_MISMATCH"):
                self.run_cli(plan_id="wrong")
        provider.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_scratch_material_tampering_rejected_without_provider(self):
        frozen = self.root / "tampered"
        shutil.copytree(FROZEN, frozen)
        with patch.object(study, "DeepSeek") as provider:
            for name in ("selected-candidate.txt", "system.txt", "initializer.json"):
                with self.subTest(name=name):
                    path = frozen / name
                    original = path.read_bytes()
                    path.write_bytes(original + b" changed")
                    with self.assertRaisesRegex(ValueError, "FROZEN_PARENT_OR_INITIALIZER_CHANGED"):
                        self.call_cli("verify", root=frozen)
                    path.write_bytes(original)
        provider.assert_not_called()

    @unittest.skipUnless(os.name == "posix", "Frozen directory fsync requires a POSIX host")
    def test_interrupted_run_returns_nonzero_without_retry_or_successor(self):
        FakeProvider.fail_at = 3
        with patch.object(study, "DeepSeek", FakeProvider):
            code, result = self.run_cli()
        self.assertEqual((code, result["status"], result["provider_calls"]), (2, "INTERRUPTED", 3))
        summary = json.loads((self.output / "summary.json").read_bytes())
        self.assertEqual(summary["automatic_retries"], 0)
        self.assertFalse(summary["automatic_successor_started"])
        self.assertFalse((self.output / study.ARMS[1]).exists())
        self.assertEqual(FakeProvider.instances[0].calls, 3)

    def test_existing_output_is_preserved_before_provider(self):
        self.output.mkdir()
        sentinel = self.output / "sentinel.txt"
        sentinel.write_bytes(b"preserve")
        with patch.object(study, "DeepSeek") as provider:
            with self.assertRaises(FileExistsError):
                self.run_cli()
        provider.assert_not_called()
        self.assertEqual(sentinel.read_bytes(), b"preserve")

    def test_run_requires_explicit_output_and_pin(self):
        with patch.object(study, "DeepSeek") as provider:
            for extra in (("--output", str(self.output)), ("--expected-plan-id", PLAN_ID)):
                with self.subTest(extra=extra), redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as error:
                        self.call_cli("run", extra=extra)
                    self.assertEqual(error.exception.code, 2)
        provider.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_prepare_and_run_refuse_non_utf8_mode_before_adapter_or_provider(self):
        disabled = SimpleNamespace(flags=SimpleNamespace(utf8_mode=0))
        with patch.object(entrypoint, "sys", disabled), patch.object(study, "run") as run:
            with patch.object(study, "prepare") as prepare, patch.object(study, "DeepSeek") as provider:
                for operation in ("prepare", "run"):
                    with self.subTest(operation=operation), redirect_stderr(io.StringIO()) as stderr:
                        with self.assertRaises(SystemExit) as error:
                            if operation == "run":
                                self.run_cli()
                            else:
                                self.call_cli("prepare", root=self.root / "prepared")
                        self.assertEqual(error.exception.code, 2)
                        self.assertIn("requires Python UTF-8 mode", stderr.getvalue())
        run.assert_not_called()
        prepare.assert_not_called()
        provider.assert_not_called()
        self.assertFalse(self.output.exists())

    @unittest.skipUnless(os.name == "nt", "Exercises actual Windows directory publication rejection")
    def test_windows_filesystem_rejection_precedes_provider_and_experiment_creation(self):
        with patch.object(study, "DeepSeek") as provider:
            for operation in ("prepare", "run"):
                with self.subTest(operation=operation), redirect_stderr(io.StringIO()) as stderr:
                    with self.assertRaises(SystemExit) as error:
                        if operation == "run":
                            self.run_cli()
                        else:
                            self.call_cli("prepare", root=self.root / "prepared")
                    self.assertEqual(error.exception.code, 2)
                    self.assertIn("TARGET_FILESYSTEM_DURABILITY_UNAVAILABLE", stderr.getvalue())
                    self.assertIn("No provider was initialized", stderr.getvalue())
        provider.assert_not_called()
        self.assertFalse(self.output.exists())
        self.assertFalse((self.root / "prepared").exists())
        self.assertEqual(list(self.root.glob(".sql-use-return-preflight-*")), [])


if __name__ == "__main__":
    unittest.main()
