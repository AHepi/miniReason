"""End-to-end offline tests for the implemented R002 successor launcher."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import uuid
from unittest.mock import patch

from minireason.reason import r002_launcher as launcher


REPO = Path(__file__).resolve().parents[2]
STUDY = REPO / "experiments" / "diagnostics" / "R002-episodes-under-calibrated-difficulty"
PYTHON = Path(r"C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe")


def read_json(path: Path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return json.load(handle)


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class R002LauncherTests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        work_root = Path(os.environ.get(
            "MINIREASON_TEST_LAUNCHER_WORK", os.environ.get(
                "MINIREASON_TEST_WORK", str(REPO / "work" / "w20" / "l"))))
        cls.root = work_root / ("r2-" + uuid.uuid4().hex[:8])
        cls.tmp = Path(os.environ.get("TMP", r"C:\tr20"))
        cls.env = os.environ.copy()
        cls.env.pop("DEEPSEEK_API_KEY", None)
        cls.env.pop("OLLAMA_API_KEY", None)
        cls.env.update({
            "PYTHONPATH": os.pathsep.join((str(REPO / "src"), str(REPO / "tests"))),
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
            "TMP": str(cls.tmp),
        })

    def invoke(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        command = [str(PYTHON), "-B", "-X", "utf8", str(REPO / "tools" / "run_R002.py"), *arguments]
        return subprocess.run(command, cwd=REPO, env=self.env, capture_output=True, text=True,
                              encoding="utf-8", errors="strict", check=False)

    def test_budget_and_opaque_offline_env_path(self) -> None:
        envelope = launcher.budget(8, 8)
        self.assertEqual(envelope["maximum_attempts"], 584)
        self.assertEqual(envelope["completion_token_ceiling"], 13369344)
        self.assertEqual(envelope["decomposed_calls_per_case"], 13)
        self.assertEqual(envelope["decomposed_completion_tokens_per_case"], 294912)
        command = launcher.child_argv(
            REPO, STUDY, "C01", "CAL-NATIVE", self.root / "opaque", "offline",
            env_file=self.root / "does-not-exist.env",
        )
        self.assertNotIn("--env-file", command)
        self.assertIn("run-r002-native", command)
        matched = launcher.child_argv(
            REPO, STUDY, "C01", "NATIVE-MATCH", self.root / "matched", "offline", cycles=2,
        )
        self.assertEqual(matched[matched.index("--cycles") + 1], "2")

    def test_material_pins_allow_only_exact_review20_plan_launcher_append(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.tmp) as temporary:
            study = Path(temporary)
            original = {"PLAN.md": b"frozen plan\n", "LAUNCHER.md": b"frozen launcher\n"}
            for name, raw in original.items():
                (study / name).write_bytes(raw)
            write_json(study / "MATERIAL_PINS-REVIEW16.json", {
                "files": {name: hashlib.sha256(raw).hexdigest() for name, raw in original.items()}
            })
            launcher.validate_material_pins(study)
            marker = b"\n\n## CHANGES - review20 launcher implementation clarification - 2026-09-17\n"
            for name, raw in original.items():
                (study / name).write_bytes(raw + marker + b"authorized tail\n")
            launcher.validate_material_pins(study)
            (study / "PLAN.md").write_bytes(b"changed prefix\n" + marker + b"authorized tail\n")
            with self.assertRaisesRegex(launcher.LauncherError, "PLAN.md"):
                launcher.validate_material_pins(study)

    def test_live_calibration_generates_bound_but_main_still_requires_pins(self) -> None:
        descriptor = launcher.calibration_wire_bound(STUDY)
        self.assertEqual(len(descriptor["wires"]), 24)
        self.assertEqual(max(item["wire_utf8_bytes"] for item in descriptor["wires"].values()), 4706)
        self.assertEqual(max(item["prompt_tokens"] for item in descriptor["wires"].values()), 1192)

        gate_root = self.root / "live-gate"
        capability = self.root / "reviewed-capability.json"
        write_json(capability, {"review_receipt": "REC-20260917-A"})
        with patch.object(launcher.subprocess, "run",
                          return_value=subprocess.CompletedProcess([], 2, "refused fixture", "")):
            with self.assertRaisesRegex(launcher.LauncherError, "child refused"):
                launcher.main([
                    "--phase", "calibration", "--mode", "live", "--run-root", str(gate_root),
                    "--env-file", str(self.root / "not-read.env"),
                    "--capability", str(capability),
                ])
        generated = gate_root / "calibration-occurrence-001" / "calibration-input-bound.json"
        self.assertEqual(read_json(generated), descriptor)

        with self.assertRaisesRegex(launcher.LauncherError, "Live main requires reviewed --tokenizer-pins"):
            launcher.main([
                "--phase", "main", "--mode", "live", "--run-root", str(self.root / "main-gate"),
                "--env-file", str(self.root / "not-read.env"),
                "--capability", str(capability),
                "--admission-receipt", str(self.root / "missing-admission.json"),
            ])

    def test_two_candidate_calibration_main_resume_and_rerun(self) -> None:
        nonexistent_env = self.root / "never-read.env"
        calibration = self.invoke(
            "--phase", "calibration", "--mode", "offline", "--run-root", str(self.root),
            "--problems", "C01", "C02", "--env-file", str(nonexistent_env),
        )
        self.assertEqual(calibration.returncode, 0, calibration.stdout + calibration.stderr)
        calibration_root = self.root / "calibration-occurrence-001"
        for candidate_id in ("C01", "C02"):
            state = read_json(calibration_root / candidate_id / "CAL-NATIVE" / "state.json")
            self.assertEqual(state["calls"], 1)
            self.assertIn(state["stop_reason"], launcher.NATIVE_GOOD_STOPS)

        records = []
        for candidate_id, verdict, operational in (
            ("C01", "incorrect", "completed"),
            ("C02", "no_answer", "ceiling_hit"),
        ):
            candidate = launcher.candidate_record(STUDY, candidate_id)
            records.append({
                "candidate_id": candidate_id,
                "verdict": verdict,
                "admitted": True,
                "operational_status": operational,
                "native_final_answer_path": "fixture-answer.txt" if verdict == "incorrect" else None,
                "problem_sha256": candidate["problem_sha256"],
                "sealed_answer_sha256": candidate["sealed_answer_sha256"],
                "oracle_sha256": candidate["oracle_sha256"],
                "oracle_kind": candidate["oracle_kind"],
            })
        admission = self.root / "admission-fixture.json"
        write_json(admission, {
            "schema": launcher.ADMISSION_SCHEMA,
            "evidence_kind": "offline-test-fixture",
            "records": records,
        })
        main = self.invoke(
            "--phase", "main", "--mode", "offline", "--run-root", str(self.root),
            "--admission-receipt", str(admission), "--problems", "C01", "C02",
            "--env-file", str(nonexistent_env),
        )
        self.assertEqual(main.returncode, 0, main.stdout + main.stderr)
        main_root = self.root / "main-occurrence-001"
        phase_receipt_bytes = (main_root / "phase-receipt.json").read_bytes()
        for candidate_id in ("C01", "C02"):
            for condition in launcher.DEFAULT_CONDITIONS:
                occurrence = main_root / candidate_id / condition
                state = read_json(occurrence / "state.json")
                expected_stops = (launcher.NATIVE_GOOD_STOPS if condition == "NATIVE" else
                                  launcher.DECOMPOSED_GOOD_STOPS if condition == "LOOP-DECOMPOSED" else
                                  launcher.LOOP_GOOD_STOPS)
                self.assertIn(state["stop_reason"], expected_stops)
                for counter in ("tail_edits", "stall_switches", "checker_runs", "cannot_decide_responses"):
                    self.assertIn(counter, state)
                self.assertTrue((occurrence / "RUN.md").is_file())
                self.assertTrue((occurrence / "TRACE.md").is_file())

        before = {
            path.relative_to(self.root).as_posix(): tree_hashes(path)
            for path in sorted(main_root.glob("C*/LOOP-*"))
        }
        resumed_calibration = self.invoke(
            "--phase", "calibration", "--mode", "offline", "--run-root", str(self.root),
            "--problems", "C01", "C02", "--env-file", str(nonexistent_env), "--resume",
        )
        self.assertEqual(resumed_calibration.returncode, 0, resumed_calibration.stdout + resumed_calibration.stderr)
        resumed_main = self.invoke(
            "--phase", "main", "--mode", "offline", "--run-root", str(self.root),
            "--admission-receipt", str(admission), "--problems", "C01", "C02",
            "--env-file", str(nonexistent_env), "--resume",
        )
        self.assertEqual(resumed_main.returncode, 0, resumed_main.stdout + resumed_main.stderr)
        after = {
            path.relative_to(self.root).as_posix(): tree_hashes(path)
            for path in sorted(main_root.glob("C*/LOOP-*"))
        }
        self.assertEqual(before, after)
        self.assertEqual((main_root / "phase-receipt.json").read_bytes(), phase_receipt_bytes)

        failed = main_root / "C01" / "LOOP-TESTED"
        state = read_json(failed / "state.json")
        state["stop_reason"] = "SCHEMA_FAILURE"
        write_json(failed / "state.json", state)
        failed_hashes = tree_hashes(failed)
        rerun = self.invoke(
            "--phase", "main", "--mode", "offline", "--run-root", str(self.root),
            "--admission-receipt", str(admission), "--problems", "C01", "C02",
            "--env-file", str(nonexistent_env), "--rerun-failed",
        )
        self.assertEqual(rerun.returncode, 0, rerun.stdout + rerun.stderr)
        archived = failed.with_name("LOOP-TESTED-failed-1")
        self.assertEqual(tree_hashes(archived), failed_hashes)
        self.assertEqual((main_root / "phase-receipt.json").read_bytes(), phase_receipt_bytes)
        self.assertTrue((main_root / "phase-receipt-rerun-001.json").is_file())
        self.assertEqual([path.name for path in main_root.glob("phase-receipt-rerun-*.json")],
                         ["phase-receipt-rerun-001.json"])
        manifest = read_json(self.root / "manifest.json")
        attempts = manifest["phases"]["main-occurrence-001"]["candidates"]["C01"]["conditions"]["LOOP-TESTED"]["attempts"]
        self.assertEqual(len(attempts), 2)
        self.assertEqual(attempts[0]["status"], "archived-failed")
        self.assertEqual(attempts[1]["status"], "complete")
        self.assertGreaterEqual(len(manifest["source_versions"]), 1)
        source_pins = manifest["source_versions"][-1]["source_sha256"]
        self.assertIn("src/minireason/provider_openai_compat.py", source_pins)
        self.assertIn("runtime_identity", manifest["source_versions"][-1])


if __name__ == "__main__":
    unittest.main()
