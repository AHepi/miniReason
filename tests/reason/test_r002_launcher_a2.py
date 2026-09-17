"""Focused offline launcher checks for the post-dispatch R002 amendment A2."""
from __future__ import annotations

import os
from pathlib import Path
import tempfile
import unittest
import uuid
from unittest.mock import patch

from minireason.reason import r002_launcher as launcher


REPO = Path(__file__).resolve().parents[2]
STUDY = REPO / "experiments" / "diagnostics" / "R002-episodes-under-calibrated-difficulty"
ADMISSION = STUDY / "calibration" / "admission.json"
TOKENIZER_PINS = STUDY / "calibration" / "main-tokenizer-pins.json"


class R002LauncherA2Tests(unittest.TestCase):
    def test_review24_root_is_bounded(self) -> None:
        self.assertEqual(
            launcher.validate_run_root(REPO, Path("C:/tr24/review-offline")),
            Path("C:/tr24/review-offline").resolve(),
        )
        for path in ("C:/tr24", "C:/tr24-sibling/run", "C:/tr24/../escape"):
            with self.subTest(path=path), self.assertRaises(launcher.LauncherError):
                launcher.validate_run_root(REPO, Path(path))

    def test_a2_budget_projection(self) -> None:
        projection = launcher.a2_budget(4)
        self.assertEqual(projection["logical_calls"], 52)
        self.assertEqual(projection["no_repair_attempts"], 52)
        self.assertEqual(projection["maximum_attempts"], 104)
        self.assertEqual(projection["no_repair_completion_token_ceiling"], 1376256)
        self.assertEqual(projection["maximum_completion_token_ceiling"], 2752512)
        self.assertEqual(projection["no_repair_prompt_token_ceiling"], 1703936)
        self.assertEqual(projection["maximum_prompt_token_ceiling"], 3407872)
        self.assertEqual(projection["no_repair_combined_token_ceiling"], 3080192)
        self.assertEqual(projection["maximum_combined_token_ceiling"], 6160384)
        self.assertEqual(projection["no_repair_aggregate_attempt_wall_seconds"], 15600)
        self.assertEqual(projection["maximum_aggregate_attempt_wall_seconds"], 31200)
        self.assertEqual(
            projection["over_three_step_maximum_completion_token_ceiling_per_case"],
            622592,
        )

    def test_a2_phase_receipt_uses_a2_budget_and_identity(self) -> None:
        with tempfile.TemporaryDirectory(dir=r"C:\tw24") as temporary:
            run_root = Path(temporary) / "run"
            phase_root = run_root / "main-occurrence-002"
            phase_key = "main-occurrence-002"
            projection = launcher.a2_budget(len(launcher.A2_ADMITTED))
            manifest = {
                "phases": {
                    phase_key: {
                        "phase": "main",
                        "mode": "offline",
                        "occurrence": 2,
                        "created_utc": "2026-09-17T00:00:00+00:00",
                        "selected_candidates": list(launcher.A2_ADMITTED),
                        "selected_conditions": list(launcher.A2_CONDITIONS),
                        "amendment": "A2",
                        "resource_projection": projection,
                        "candidates": {},
                    }
                }
            }
            args = launcher.argparse.Namespace(
                phase="main",
                mode="offline",
                occurrence=2,
                amendment_a2=True,
            )
            launcher._phase_receipt(
                run_root,
                phase_root,
                manifest,
                phase_key,
                args,
                list(launcher.A2_ADMITTED),
                (),
            )
            receipt = launcher.read_json(phase_root / "phase-receipt.json")

        self.assertEqual(receipt["occurrence"], 2)
        self.assertEqual(receipt["amendment"], "A2")
        self.assertIs(receipt["amendment_a2"], True)
        self.assertEqual(receipt["selected_conditions"], ["LOOP-DECOMPOSED"])
        self.assertEqual(receipt["budget"], projection)
        self.assertNotIn("calibration_candidates", receipt["budget"])

    def test_a2_attempt_identity_is_occurrence_scoped_and_legacy_is_unchanged(self) -> None:
        run_root = Path(r"C:\tw24\identity-fixture")
        directory = run_root / "main-occurrence-002" / "C05" / "LOOP-DECOMPOSED"
        a2 = launcher._attempt(
            {},
            "LOOP-DECOMPOSED",
            "C05",
            directory,
            run_root,
            2,
            occurrence_scope="main-occurrence-002",
        )
        legacy = launcher._attempt(
            {},
            "LOOP-DECOMPOSED",
            "C05",
            directory,
            run_root,
            1,
        )
        self.assertEqual(
            a2["occurrence_id"],
            "R002-main-occurrence-002-C05-LOOP-DECOMPOSED-attempt-001",
        )
        self.assertEqual(
            legacy["occurrence_id"],
            "R002-C05-LOOP-DECOMPOSED-attempt-001",
        )

    def test_a2_child_uses_v2_recipe(self) -> None:
        command = launcher.child_argv(
            REPO,
            STUDY,
            "C05",
            "LOOP-DECOMPOSED",
            Path(r"C:\tw24\launcher-child"),
            "offline",
            tokenizer_pins=TOKENIZER_PINS,
            cycles=3,
            recipe_id=launcher.A2_RECIPE_IDS["LOOP-DECOMPOSED"],
        )
        self.assertEqual(
            command[command.index("--recipe") + 1],
            str(STUDY / "recipes" / "r002-decomposed-v2.json"),
        )

    def test_a2_rejects_calibration_optional_receipts_and_rerun(self) -> None:
        cases = (
            (
                "calibration",
                [
                    "--phase", "calibration",
                    "--occurrence", "2",
                ],
                "restricted to main occurrence-002",
            ),
            (
                "optional",
                [
                    "--phase", "main",
                    "--occurrence", "2",
                    "--optional-receipt", str(Path(r"C:\tw24") / "unused.json"),
                ],
                "does not select optional arms",
            ),
            (
                "rerun",
                [
                    "--phase", "main",
                    "--occurrence", "2",
                    "--rerun-failed",
                ],
                "cannot rerun a failed occurrence",
            ),
        )
        with tempfile.TemporaryDirectory(dir=r"C:\tw24") as temporary:
            for label, prefix, message in cases:
                with self.subTest(case=label), self.assertRaisesRegex(
                    launcher.LauncherError, message
                ):
                    launcher.main([
                        *prefix,
                        "--mode", "offline",
                        "--run-root", str(Path(temporary) / label),
                        "--amendment-a2",
                        "--admission-receipt", str(ADMISSION),
                        "--tokenizer-pins", str(TOKENIZER_PINS),
                    ])

    def test_a2_rejects_wrong_admitted_set(self) -> None:
        with tempfile.TemporaryDirectory(dir=r"C:\tw24") as temporary:
            with (
                patch.object(
                    launcher,
                    "validate_admission_receipt",
                    return_value=(["C05", "C06", "C09"], {}),
                ),
                self.assertRaisesRegex(
                    launcher.LauncherError,
                    "requires admitted set C05 C06 C09 C12 exactly",
                ),
            ):
                launcher.main([
                    "--phase", "main",
                    "--mode", "offline",
                    "--run-root", str(Path(temporary) / "wrong-admission"),
                    "--occurrence", "2",
                    "--amendment-a2",
                    "--admission-receipt", str(ADMISSION),
                    "--tokenizer-pins", str(TOKENIZER_PINS),
                ])

    def test_changed_sources_append_version_without_changing_occurrence_one_phase(self) -> None:
        with tempfile.TemporaryDirectory(dir=r"C:\tw24") as temporary:
            manifest_path = Path(temporary) / "manifest.json"
            manifest = launcher._load_manifest(manifest_path, REPO, STUDY, "offline")
            historical_phase = {
                "phase": "main",
                "mode": "live",
                "occurrence": 1,
                "selected_candidates": list(launcher.A2_ADMITTED),
                "terminal_status": "COMPLETED_WITH_FAILURES",
            }
            manifest["phases"]["main-occurrence-001"] = historical_phase
            manifest["source_versions"][-1]["source_sha256"] = {
                "historical/source.py": "0" * 64
            }
            launcher.write_json(manifest_path, manifest)
            loaded = launcher._load_manifest(manifest_path, REPO, STUDY, "offline")

        self.assertEqual(
            loaded["phases"]["main-occurrence-001"],
            historical_phase,
        )
        self.assertEqual(len(loaded["source_versions"]), 2)
        self.assertEqual(loaded["active_source_version"], 2)
        self.assertNotEqual(
            loaded["source_versions"][0]["source_sha256"],
            loaded["source_versions"][1]["source_sha256"],
        )

    def test_a2_requires_occurrence_two(self) -> None:
        with tempfile.TemporaryDirectory(dir=r"C:\tw24") as temporary:
            with self.assertRaisesRegex(
                launcher.LauncherError, "restricted to main occurrence-002"
            ):
                launcher.main([
                    "--phase", "main",
                    "--mode", "offline",
                    "--run-root", str(Path(temporary) / "main"),
                    "--occurrence", "1",
                    "--amendment-a2",
                    "--admission-receipt", str(ADMISSION),
                    "--tokenizer-pins", str(TOKENIZER_PINS),
                ])

    def test_a2_dispatches_only_decomposed_and_preserves_occurrence_one(self) -> None:
        admitted, _receipt = launcher.validate_admission_receipt(
            ADMISSION, STUDY, offline=True)
        self.assertEqual(tuple(admitted), launcher.A2_ADMITTED)
        dispatched: list[tuple[str, str, Path, bool]] = []

        def record_occurrence(*args, **kwargs):
            dispatched.append((args[6], args[7], args[8], args[9].amendment_a2))
            return {}, True

        with tempfile.TemporaryDirectory(dir=r"C:\tw24") as temporary:
            run_root = Path(temporary) / "main"
            occurrence_one = run_root / "main-occurrence-001"
            occurrence_one.mkdir(parents=True)
            sentinel = occurrence_one / "preserve.txt"
            sentinel.write_text("occurrence-001 evidence\n", encoding="utf-8", newline="")
            before = sentinel.read_bytes()
            with (
                patch.object(launcher, "_run_occurrence", side_effect=record_occurrence),
                patch.object(launcher, "_phase_receipt"),
            ):
                result = launcher.main([
                    "--phase", "main",
                    "--mode", "offline",
                    "--run-root", str(run_root),
                    "--occurrence", "2",
                    "--amendment-a2",
                    "--admission-receipt", str(ADMISSION),
                    "--tokenizer-pins", str(TOKENIZER_PINS),
                    "--problems", *admitted,
                ])
            self.assertEqual(sentinel.read_bytes(), before)
            self.assertFalse(any(path.is_relative_to(occurrence_one)
                                 for _candidate, _condition, path, _a2 in dispatched))

        self.assertEqual(result, 0)
        self.assertEqual(
            [(candidate, condition) for candidate, condition, _path, _a2 in dispatched],
            [(candidate, "LOOP-DECOMPOSED") for candidate in admitted],
        )
        self.assertTrue(all(path.parts[-3] == "main-occurrence-002"
                            for _candidate, _condition, path, _a2 in dispatched))
        self.assertTrue(all(a2 for _candidate, _condition, _path, a2 in dispatched))

    @unittest.skipUnless(os.name == "nt", "Windows-specific absolute work root")
    def test_tw24_run_root_accepts_strict_descendants_only(self) -> None:
        accepted = Path(r"C:\tw24\launcher") / uuid.uuid4().hex[:8]
        self.assertEqual(launcher.validate_run_root(REPO, accepted), accepted.resolve())
        for refused in (
            Path(r"C:\tw24"),
            Path(r"C:\tw24\..\escape"),
            Path(r"C:\tw24-other\proof"),
        ):
            with self.subTest(path=refused), self.assertRaises(launcher.LauncherError):
                launcher.validate_run_root(REPO, refused)


if __name__ == "__main__":
    unittest.main()
