"""Focused offline tests for the staged R002 launcher."""
from __future__ import annotations

import importlib.util
import hashlib
import json
from pathlib import Path
import tempfile
import unittest


LAUNCHER = Path(__file__).resolve().parents[1] / "run_R002.py"
SPEC = importlib.util.spec_from_file_location("run_R002", LAUNCHER)
assert SPEC is not None and SPEC.loader is not None
R002 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(R002)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(value)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def admission_record(candidate_id: str, verdict: str) -> dict[str, object]:
    return {
        "candidate_id": candidate_id,
        "calibration_attempt_id": "fixture-" + candidate_id,
        "baseline_run_id": "fixture-run-" + candidate_id,
        "oracle_result": "fixture",
        "native_final_answer_path": None,
        "native_final_answer_sha256": None,
        "verdict": verdict,
        "admitted": verdict in {"incorrect", "no_answer"},
        "exclusion_reason": None if verdict in {"incorrect", "no_answer"} else "fixture-correct",
        "reader_identity": "offline-test",
        "read_utc": "2026-09-17T00:00:00+00:00",
        "operational_status": "transport_error" if verdict == "no_answer" else "completed",
        "operational_failure_cause": "fixture-no-answer" if verdict == "no_answer" else None,
        "no_answer_reason": "fixture-no-answer" if verdict == "no_answer" else None,
        "problem_sha256": "fixture-problem",
        "sealed_answer_sha256": "fixture-answer",
        "oracle_sha256": "fixture-oracle",
        "oracle_kind": "computable",
    }


class R002LauncherTests(unittest.TestCase):
    def test_maximum_budget_matches_preregistration(self) -> None:
        self.assertEqual(R002.budget(8, 8), {
            "calibration_candidates": 24,
            "admitted": 8,
            "computable_admitted": 8,
            "optional_case_occurrences": 0,
            "logical_calls": 480,
            "maximum_attempts": 480,
            "completion_token_ceiling": 11010048,
            "prompt_token_ceiling": 15728640,
            "combined_token_ceiling": 26738688,
            "per_attempt_wall_seconds": 300,
            "aggregate_attempt_wall_seconds": 144000,
        })

    def test_admission_is_first_eight_incorrect_or_no_answer_in_id_order(self) -> None:
        with tempfile.TemporaryDirectory(dir=r"C:\tr16") as raw:
            path = Path(raw) / "admission.json"
            records = [admission_record(candidate_id, "correct") for candidate_id in R002.PROBLEM_IDS]
            for candidate_id in ("C19", "C02", "C11", "C03", "C14", "C05", "C22", "C07", "C09"):
                records[int(candidate_id[1:]) - 1] = admission_record(candidate_id, "incorrect")
            write_json(path, {
                "schema": R002.ADMISSION_SCHEMA,
                "evidence_kind": "offline-test-fixture",
                "records": list(reversed(records)),
            })
            admitted, _ = R002.validate_admission_receipt(path, allow_offline_fixture=True)
            self.assertEqual(admitted, ["C02", "C03", "C05", "C07", "C09", "C11", "C14", "C19"])

    def test_fewer_than_eight_and_zero_follow_stopping_rule(self) -> None:
        with tempfile.TemporaryDirectory(dir=r"C:\tr16") as raw:
            path = Path(raw) / "few.json"
            write_json(path, {
                "schema": R002.ADMISSION_SCHEMA,
                "evidence_kind": "offline-test-fixture",
                "records": [admission_record("C04", "no_answer"), admission_record("C01", "incorrect")],
            })
            admitted, _ = R002.validate_admission_receipt(path, allow_offline_fixture=True)
            self.assertEqual(admitted, ["C01", "C04"])
            write_json(Path(raw) / "zero.json", {
                "schema": R002.ADMISSION_SCHEMA,
                "evidence_kind": "offline-test-fixture",
                "records": [admission_record("C01", "correct")],
            })
            admitted, _ = R002.validate_admission_receipt(
                Path(raw) / "zero.json", allow_offline_fixture=True,
            )
            self.assertEqual(admitted, [])

    def test_live_receipt_links_all_24_trials_and_sealed_hashes(self) -> None:
        with tempfile.TemporaryDirectory(dir=r"C:\tr16") as raw:
            study = Path(raw) / "study"
            write_text(study / "CANDIDATES.md", "# fixture candidate manifest\n")
            entries = []
            phase_records = []
            admission_records = []
            for number, candidate_id in enumerate(R002.PROBLEM_IDS, start=1):
                problem = study / "problems" / f"{candidate_id}.txt"
                answer = study / "answers" / f"{candidate_id}.md"
                oracle = study / "oracle" / f"{candidate_id}.py"
                recoded = study / "codings" / f"{candidate_id}-recoded.txt"
                carrier = study / "codings" / f"{candidate_id}-carrier.txt"
                native = study / "pilot" / f"{candidate_id}.txt"
                for path, text in (
                    (problem, f"problem {candidate_id}\n"),
                    (answer, f"answer {candidate_id}\n"),
                    (oracle, f"print('{candidate_id}')\n"),
                    (recoded, f"recoded {candidate_id}\n"),
                    (carrier, f"carrier {candidate_id}\n"),
                    (native, f"native {candidate_id}\n"),
                ):
                    write_text(path, text)
                oracle_kind = "computable" if number <= 18 else "derivation-only"
                entries.append({
                    "candidate_id": candidate_id,
                    "problem_path": f"problems/{candidate_id}.txt",
                    "answer_path": f"answers/{candidate_id}.md",
                    "oracle_path": f"oracle/{candidate_id}.py",
                    "oracle_kind": oracle_kind,
                    "checker_eligible": number <= 18,
                    "recoding_map_id": candidate_id,
                    "recoded_problem_path": f"codings/{candidate_id}-recoded.txt",
                    "carrier_problem_path": f"codings/{candidate_id}-carrier.txt",
                    "hashes": {
                        "problem_sha256": digest(problem),
                        "answer_sha256": digest(answer),
                        "oracle_sha256": digest(oracle),
                        "recoded_problem_sha256": digest(recoded),
                        "carrier_problem_sha256": digest(carrier),
                    },
                })
                phase_records.append({
                    "candidate_id": candidate_id,
                    "occurrence_id": "cal-" + candidate_id,
                    "logical_calls": 1, "attempts": 1, "completion_token_ceiling": 32768,
                    "endpoint": "deepseek-flash", "thinking": "native", "wall_seconds": 300,
                    "baseline_run_id": "run-" + candidate_id,
                })
                record = admission_record(candidate_id, "incorrect" if number <= 9 else "correct")
                record.update({
                    "calibration_attempt_id": "cal-" + candidate_id,
                    "baseline_run_id": "run-" + candidate_id,
                    "native_final_answer_path": str(native),
                    "native_final_answer_sha256": digest(native),
                    "problem_sha256": digest(problem),
                    "sealed_answer_sha256": digest(answer),
                    "oracle_sha256": digest(oracle),
                    "oracle_kind": oracle_kind,
                })
                admission_records.append(record)
            write_json(study / "problems" / "RECODING_MAPS.json", {
                "schema_version": "fixture",
                "candidates": entries,
            })
            phase = Path(raw) / "phase.json"
            write_json(phase, {
                "phase": "calibration", "mode": "live", "scientific_evidence": True,
                "selected_candidates": list(R002.PROBLEM_IDS),
                "records": phase_records,
            })
            receipt = Path(raw) / "admission.json"
            write_json(receipt, {
                "schema": R002.ADMISSION_SCHEMA,
                "evidence_kind": "live-calibration",
                "calibration_phase_receipt_path": str(phase),
                "calibration_phase_receipt_sha256": digest(phase),
                "candidate_manifest_sha256": digest(study / "CANDIDATES.md"),
                "records": admission_records,
            })
            admitted, _ = R002.validate_admission_receipt(
                receipt, study=study, allow_offline_fixture=False,
            )
            self.assertEqual(admitted, list(R002.PROBLEM_IDS[:8]))
            phase_data = json.loads(phase.read_text(encoding="utf-8"))
            phase_data["records"][0]["attempts"] = 2
            write_json(phase, phase_data)
            receipt_data = json.loads(receipt.read_text(encoding="utf-8"))
            receipt_data["calibration_phase_receipt_sha256"] = digest(phase)
            write_json(receipt, receipt_data)
            with self.assertRaisesRegex(R002.LauncherError, "exactly one native call"):
                R002.validate_admission_receipt(receipt, study=study, allow_offline_fixture=False)


    def test_write_once_receipt_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(dir=r"C:\tr16") as raw:
            path = Path(raw) / "receipt.json"
            R002.write_json_once(path, {"first": True})
            with self.assertRaisesRegex(R002.LauncherError, "Write-once"):
                R002.write_json_once(path, {"second": True})
            self.assertEqual(json.loads(R002.read_text(path)), {"first": True})

    def test_live_is_blocked_without_engineering_adapter(self) -> None:
        with self.assertRaisesRegex(R002.LauncherError, "Live R002 is blocked"):
            R002.refuse_live(Path(__file__).resolve().parents[1])

    def test_proposed_contract_artifacts_are_pinned(self) -> None:
        hashes = R002.proposed_artifact_hashes(Path(__file__).resolve().parents[1])
        self.assertEqual(len(hashes["recipes"]), 7)
        self.assertGreaterEqual(len(hashes["contracts"]), 12)
        self.assertTrue(all(len(digest) == 64 for group in hashes.values() for digest in group.values()))

    def test_ceilings_admit_no_answer_without_mislabelling_wrong(self):
        with tempfile.TemporaryDirectory(dir=r"C:/tr16") as raw:
            path = Path(raw) / "admit.json"
            row = admission_record("C01", "no_answer")
            row.update(operational_status="CEILING_HIT", no_answer_reason="not answered")
            write_json(path, {"schema": R002.ADMISSION_SCHEMA, "evidence_kind": "offline-test-fixture", "records": [row]})
            self.assertEqual(R002.validate_admission_receipt(path, allow_offline_fixture=True)[0], ["C01"])
            row.update(verdict="incorrect", admitted=True)
            write_json(path, {"schema": R002.ADMISSION_SCHEMA, "evidence_kind": "offline-test-fixture", "records": [row]})
            with self.assertRaisesRegex(R002.LauncherError, "must be no_answer"):
                R002.validate_admission_receipt(path, allow_offline_fixture=True)

    def test_optional_gates_and_added_budget(self):
        self.assertEqual(R002.validate_optional_receipts([]), ())
        self.assertEqual(R002.budget(8, 8, 24)["maximum_attempts"], 816)
        self.assertEqual(R002.budget(8, 8, 24)["completion_token_ceiling"], 18481152)
        with tempfile.TemporaryDirectory(dir=r"C:/tr16") as raw:
            path = Path(raw) / "optional.json"
            write_json(path, {"condition": "LOOP-CARRIER"})
            with self.assertRaisesRegex(R002.LauncherError, "own receipt"):
                R002.validate_optional_receipts([path])
            write_json(path, {"schema": "minireason.r002.optional-arm-receipt.v1", "condition": "LOOP-CARRIER",
                             "decision_receipt": "OFFLINE-ONLY", "reason": "test gate", "occurrence_id": "fixture",
                             "candidate_ids": ["C01"], "max_calls_per_case": 14, "completion_tokens_per_case": 311296})
            self.assertEqual(R002.validate_optional_receipts([path]), ("LOOP-CARRIER",))

    def test_env_forwarding_does_not_open_file_or_expose_values(self):
        from unittest.mock import patch
        study = LAUNCHER.parent
        missing = Path(r"C:/tr16/nonexistent-forwarding-fixture.env")
        with patch.object(Path, "open", side_effect=AssertionError("env-file must never be opened by argv builder")):
            argv = R002.prospective_child_argv(study.parents[2], study, "C01", "LOOP-TESTED", Path(r"C:/tr16/future"), missing)
        self.assertEqual(argv[argv.index("--env-file") + 1], str(missing))
        self.assertEqual(argv[argv.index("--mode") + 1], "live")
        self.assertEqual(argv[argv.index("--attempt-policy") + 1], "strict")

    def test_resume_accepts_only_exact_complete_custody(self):
        with tempfile.TemporaryDirectory(dir=r"C:/tr16") as raw:
            root = Path(raw); artifact = root / "fixture.json"; manifest = root / "manifest.json"
            write_json(artifact, {"fixture": True})
            context = {"source": "frozen"}
            write_json(manifest, {"schema": "minireason.r002.offline-manifest.v2", "state": "COMPLETE", "context": context,
                                  "evidence_sha256": {"fixture.json": digest(artifact)}})
            R002.verify_completed_manifest(manifest, root, context)
            with self.assertRaisesRegex(R002.LauncherError, "context/source mismatch"):
                R002.verify_completed_manifest(manifest, root, {"source": "changed"})
            write_json(artifact, {"fixture": False})
            with self.assertRaisesRegex(R002.LauncherError, "evidence mismatch"):
                R002.verify_completed_manifest(manifest, root, context)
            with self.assertRaisesRegex(R002.LauncherError, "Partial occurrence"):
                R002.verify_completed_manifest(root / "absent.json", root, context)


if __name__ == "__main__":
    unittest.main()
