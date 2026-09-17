"""Focused offline launcher checks for the R002 A1 amendment."""
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


class R002LauncherW22Tests(unittest.TestCase):
    def test_decomposed_is_sixth_default_with_strict_terminal_stops(self) -> None:
        self.assertEqual(len(launcher.DEFAULT_CONDITIONS), 6)
        self.assertEqual(launcher.DEFAULT_CONDITIONS[-1], "LOOP-DECOMPOSED")
        self.assertEqual(launcher.RECIPE_IDS["LOOP-DECOMPOSED"], "r002-decomposed-v1")
        for stop in ("complete", "step_budget", "step_unresolved", "initial_cannot_decide"):
            with self.subTest(stop=stop):
                self.assertTrue(launcher._good_stop("LOOP-DECOMPOSED", stop))
        for stop in ("CEILING_HIT", "SCHEMA_FAILURE", "TRANSPORT_ERROR"):
            with self.subTest(stop=stop):
                self.assertFalse(launcher._good_stop("LOOP-DECOMPOSED", stop))

    def test_decomposed_child_uses_recipe_three_cycles_and_tokenizer_descriptor(self) -> None:
        command = launcher.child_argv(
            REPO,
            STUDY,
            "C05",
            "LOOP-DECOMPOSED",
            Path(r"C:\tw22\launcher-child"),
            "live",
            env_file=Path("opaque.env"),
            tokenizer_pins=TOKENIZER_PINS,
            cycles=3,
        )
        self.assertEqual(command[command.index("--recipe") + 1],
                         str(STUDY / "recipes" / "r002-decomposed-v1.json"))
        self.assertEqual(command[command.index("--cycles") + 1], "3")
        self.assertEqual(command[command.index("--tokenizer-pins") + 1], str(TOKENIZER_PINS))

    def test_main_budget_adds_thirteen_call_arm(self) -> None:
        envelope = launcher.budget(4, 4)
        self.assertEqual(envelope["main_phase_logical_calls"], 280)
        self.assertEqual(envelope["main_phase_maximum_attempts"], 280)
        self.assertEqual(envelope["main_phase_completion_token_ceiling"], 6291456)
        self.assertEqual(envelope["main_phase_prompt_token_ceiling"], 9175040)
        self.assertEqual(envelope["main_phase_combined_token_ceiling"], 15466496)
        self.assertEqual(envelope["logical_calls"], 304)
        self.assertEqual(envelope["completion_token_ceiling"], 7077888)

    @unittest.skipUnless(os.name == "nt", "Windows-specific absolute work root")
    def test_tw22_run_root_accepts_strict_descendants_only(self) -> None:
        accepted = Path(r"C:\tw22\launcher") / uuid.uuid4().hex[:8]
        self.assertEqual(launcher.validate_run_root(REPO, accepted), accepted.resolve())
        for refused in (
            Path(r"C:\tw22"),
            Path(r"C:\tw22\..\escape"),
            Path(r"C:\tw22-other\proof"),
        ):
            with self.subTest(path=refused), self.assertRaises(launcher.LauncherError):
                launcher.validate_run_root(REPO, refused)

    def test_actual_admission_dispatches_all_six_conditions_offline(self) -> None:
        admitted, _receipt = launcher.validate_admission_receipt(
            ADMISSION, STUDY, offline=True)
        self.assertEqual(admitted, ["C05", "C06", "C09", "C12"])
        self.assertTrue(TOKENIZER_PINS.is_file())
        self.assertEqual(launcher.read_json(TOKENIZER_PINS)["kind"],
                         "conservative-byte-bound-v1")
        dispatched: list[tuple[str, str]] = []

        def record_occurrence(*args, **kwargs):
            dispatched.append((args[6], args[7]))
            return {}, True

        with tempfile.TemporaryDirectory(dir=r"C:\tw22") as temporary:
            run_root = Path(temporary) / "main"
            with (
                patch.object(launcher, "_run_occurrence", side_effect=record_occurrence),
                patch.object(launcher, "_phase_receipt"),
            ):
                result = launcher.main([
                    "--phase", "main",
                    "--mode", "offline",
                    "--run-root", str(run_root),
                    "--admission-receipt", str(ADMISSION),
                    "--tokenizer-pins", str(TOKENIZER_PINS),
                    "--problems", *admitted,
                ])
        self.assertEqual(result, 0)
        self.assertEqual(
            dispatched,
            [(candidate_id, condition)
             for candidate_id in admitted
             for condition in launcher.DEFAULT_CONDITIONS],
        )

    def test_source_snapshot_covers_decomposed_contracts_and_recipe(self) -> None:
        snapshot = launcher._source_snapshot(REPO, STUDY)
        expected = {
            "experiments/diagnostics/R002-episodes-under-calibrated-difficulty/"
            "recipes/r002-decomposed-v1.json",
            "experiments/diagnostics/R002-episodes-under-calibrated-difficulty/"
            "contracts/initial-decompose.schema.json",
            "experiments/diagnostics/R002-episodes-under-calibrated-difficulty/"
            "contracts/decomposed-step.schema.json",
            "experiments/diagnostics/R002-episodes-under-calibrated-difficulty/"
            "contracts/decomposed-return.schema.json",
            "experiments/diagnostics/R002-episodes-under-calibrated-difficulty/"
            "contracts/decomposed-use.schema.json",
        }
        self.assertTrue(expected <= snapshot.keys())


if __name__ == "__main__":
    unittest.main()
