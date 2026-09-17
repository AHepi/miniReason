"""Focused lifecycle and custody tests for the R003 occurrence launcher."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import uuid
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "experiments" / "diagnostics" / "R003-open-problems-trial-series" / "run_R003.py"
SPEC = importlib.util.spec_from_file_location("r003_launcher", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
launcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(launcher)


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class R003LauncherTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        fixture_root = Path(os.environ.get("TMP", "C:/tr28"))
        fixture_root.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="r3-", dir=fixture_root)
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _fake_child(self, command, **_kwargs):
        output = Path(command[command.index("--out") + 1])
        condition = "NATIVE" if "run-r002-native" in command else (
            "LOOP-CROSS" if "r003-cross-v1.json" in " ".join(command) else "LOOP-DECOMPOSED")
        failed = output.parts[-4] == "o001" and condition == "LOOP-CROSS"
        write_json(output / "state.json", {
            "study_profile": launcher.PROFILE,
            "stop_reason": "SCHEMA_FAILURE" if failed else "complete",
            "calls": 1,
        })
        return subprocess.CompletedProcess(command, 2 if failed else 0,
            "fixture child\n", "fixture failure\n" if failed else "")

    def _seal(self, problem_ids=("O01", "O02")) -> Path:
        seal_root = self.root / "seal"
        rows = []
        for problem_id in problem_ids:
            brief = seal_root / f"{problem_id}.md"
            brief.parent.mkdir(parents=True, exist_ok=True)
            with brief.open("w", encoding="utf-8", newline="") as handle:
                handle.write(f"Fixture brief {problem_id}\n")
            problem = launcher.STUDY / "problems" / f"{problem_id}.txt"
            rows.append({
                "problem_id": problem_id,
                "problem_path": os.path.relpath(problem, seal_root).replace("\\", "/"),
                "problem_sha256": sha256(problem),
                "brief_path": brief.name,
                "brief_sha256": sha256(brief),
                "author": "fixture reader",
                "provider": "OpenAI",
                "model": "fixture-model",
                "lineage": "OpenAI distinct fixture lineage",
                "exposure": "fixture problem only",
                "sealed_utc": "2026-09-17T00:00:00+00:00",
            })
        manifest = seal_root / "seal.json"
        write_json(manifest, {"schema": launcher.SEAL_SCHEMA, "status": "SEALED", "records": rows})
        return manifest

    def test_two_problem_matrix_resume_rerun_and_manifests(self) -> None:
        series = self.root / "series"
        directory = launcher.create(series, ["O01", "O02"], launcher.CONDITIONS,
            "Does the offline fixture exercise all occurrence-one lifecycle paths?", "offline",
            env_file=Path("fixture.env"))
        manifest = launcher.read_json(directory / "MANIFEST.json")
        self.assertEqual(manifest["schema"], launcher.MANIFEST_SCHEMA)
        self.assertEqual(len(manifest["matrix"]), 6)
        self.assertEqual(manifest["source_versions"][0]["version"], 1)
        self.assertLess(manifest["path_length"]["maximum_projected_absolute"], 200)
        canonical = launcher.read_json(directory / "CANONICAL.json")
        self.assertEqual(canonical["schema_version"], launcher.CANONICAL_SCHEMA)
        self.assertEqual([row["candidate_id"] for row in canonical["candidates"]], ["O01", "O02"])
        for row in manifest["matrix"]:
            self.assertIn("--study-profile", row["argv"])
            self.assertIn("--canonical-registry", row["argv"])
            self.assertIn("--env-file", row["argv"])
            self.assertNotIn("--coding-manifest", row["argv"])

        calls = []
        def invoke(command, **kwargs):
            self.assertNotIn("timeout", kwargs)
            calls.append(command)
            return self._fake_child(command, **kwargs)

        with patch.object(launcher.subprocess, "run", side_effect=invoke):
            first = launcher.execute(directory)
            self.assertEqual(first, {"status": "FINISHED", "rows": 6, "failed": 2})
            before = len(calls)
            resumed = launcher.execute(directory)
            self.assertEqual(resumed, {"status": "FINISHED", "rows": 6, "failed": 2})
            self.assertEqual(len(calls), before)
            successor = launcher.rerun(directory,
                "Does a separately numbered fixture successor clear the known failed cells?",
                "Exercise failed-cell selection without replaying successful cells.", "offline")
            self.assertEqual(successor.name, "o002")
            successor_manifest = launcher.read_json(successor / "MANIFEST.json")
            self.assertEqual([(row["problem"], row["condition"]) for row in successor_manifest["matrix"]],
                             [("O01", "LOOP-CROSS"), ("O02", "LOOP-CROSS")])
            second = launcher.execute(successor)
            self.assertEqual(second, {"status": "FINISHED", "rows": 2, "failed": 0})

        self.assertEqual(len(list((directory / "results").glob("*.json"))), 6)
        launcher.verify(directory)
        launcher.verify(successor)
        self.assertTrue(all(len(str(path.resolve())) < 200 for path in series.rglob("*") if path.is_file()))

        tampered = launcher.create(self.root / "pins", ["O01"], launcher.CONDITIONS,
            "Does the source manifest reject omission of a required execution source?", "plan")
        tampered_manifest = launcher.read_json(tampered / "MANIFEST.json")
        provider_pin = next(name for name in tampered_manifest["source_versions"][0]["files"]
                            if name.startswith("src/minireason/provider"))
        del tampered_manifest["source_versions"][0]["files"][provider_pin]
        write_json(tampered / "MANIFEST.json", tampered_manifest)
        with (tampered / "MANIFEST.sha256").open("w", encoding="utf-8", newline="") as handle:
            handle.write(sha256(tampered / "MANIFEST.json") + "\n")
        with self.assertRaisesRegex(launcher.Refused, "SOURCE_CHANGED"):
            launcher.verify(tampered)

    def test_seal_byte_gate_and_live_arguments_are_explicit(self) -> None:
        seal = self._seal()
        summary = launcher.validate_sealed_briefs(seal, ["O01", "O02"])
        self.assertEqual([row["problem_id"] for row in summary["records"]], ["O01", "O02"])
        capability = self.root / "capability.json"
        tokenizers = self.root / "tokenizers.json"
        write_json(capability, {"schema": "fixture-capability"})
        write_json(tokenizers, {"schema": "fixture-tokenizers"})

        with self.assertRaisesRegex(launcher.Refused, "LIVE_DISPATCH_AUTHORIZATION_REQUIRED"):
            launcher.create(self.root / "refused", ["O01"], launcher.CONDITIONS,
                "A live occurrence needs a separate dispatch decision.", "live",
                env_file=Path(".env"), capability=capability, tokenizer_pins=tokenizers,
                brief_manifest=seal)

        with patch("minireason.reason.r002_preflight.validate_r003_launch_inputs",
                   return_value={"capability": {}, "tokenizers": {}}):
            directory = launcher.create(self.root / "live", ["O01", "O02"], launcher.CONDITIONS,
                "Does the authorized qualified occurrence improve the selected open problems?", "live",
                env_file=Path(".env"), capability=capability, tokenizer_pins=tokenizers,
                brief_manifest=seal, authorize_live=True)
        manifest = launcher.read_json(directory / "MANIFEST.json")
        self.assertTrue(manifest["live_authorized"])
        self.assertFalse(manifest["env_file_read_by_launcher"])
        for row in manifest["matrix"]:
            self.assertEqual(row["argv"][row["argv"].index("--env-file") + 1], ".env")
            self.assertIn("--capability", row["argv"])
            self.assertIn("--tokenizer-pins", row["argv"])
        self.assertNotIn("dummy-secret-value", (directory / "MANIFEST.json").read_text(encoding="utf-8"))
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "dummy-secret-value"}, clear=False):
            child_environment = launcher._subprocess_environment()
        self.assertNotIn("DEEPSEEK_API_KEY", child_environment)
        self.assertNotIn("dummy-secret-value", json.dumps(child_environment, sort_keys=True))

        brief = seal.parent / "O01.md"
        with brief.open("a", encoding="utf-8", newline="") as handle:
            handle.write("changed\n")
        with self.assertRaisesRegex(launcher.Refused, "SEALED_BRIEF_HASH_MISMATCH"):
            launcher.verify(directory)


if __name__ == "__main__":
    unittest.main()
