#!/usr/bin/env python3
"""Stage R002 calibration and main occurrences without weakening contract gates."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


STUDY_NAME = "R002-episodes-under-calibrated-difficulty"
SCHEMA = "minireason.r002.launcher.v1"
ADMISSION_SCHEMA = "minireason.r002.admission-reader.v1"
CAPABILITY_SCHEMA = "minireason.reason.engine-capability.v1"
CAPABILITY_NAME = "r002-contracts-v2"
PROBLEM_IDS = tuple(f"C{number:02d}" for number in range(1, 25))
ADMISSION_VERDICTS = {"incorrect", "no_answer"}
ALL_VERDICTS = ADMISSION_VERDICTS | {"correct", "unresolved"}
PROVIDER_KEYS = ("DEEPSEEK_API_KEY", "OLLAMA_API_KEY")
STRICT_CONDITIONS = ("LOOP-CROSS", "LOOP-TESTED", "LOOP-RECODED")
OPTIONAL_CONDITIONS = ("LOOP-CROSS-MATCH", "LOOP-CARRIER", "NATIVE-MATCH")
CONDITION_ORDER = ("NATIVE", *STRICT_CONDITIONS, "LOOP-CHECKER")
RECIPE_IDS = {
    "LOOP-CROSS": "r002-cross-v2", "LOOP-CROSS-MATCH": "r002-cross-match-v1",
    "LOOP-TESTED": "r002-tested-cross-v1", "LOOP-RECODED": "r002-recoded-v1",
    "LOOP-CARRIER": "r002-carrier-v1", "NATIVE-MATCH": "r002-native-match-v1",
    "LOOP-CHECKER": "r002-checker-v1",
}
class LauncherError(RuntimeError):
    pass


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def read_json(path: Path) -> Any:
    try:
        return json.loads(read_text(path))
    except (OSError, ValueError) as error:
        raise LauncherError(f"Could not read JSON: {path}") from error


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def proposed_artifact_hashes(study: Path) -> dict[str, dict[str, str]]:
    groups: dict[str, dict[str, str]] = {}
    for directory in ("contracts", "recipes"):
        root = study / directory
        groups[directory] = {
            path.relative_to(study).as_posix(): sha256(path)
            for path in sorted(root.glob("*.json"))
            if path.name != "ENGINE_CAPABILITY.json"
        }
    return groups


def capability_hash_maps(study: Path) -> dict[str, dict[str, str]]:
    artifacts = proposed_artifact_hashes(study)
    return {
        "schema_sha256": {Path(path).name: digest for path, digest in artifacts["contracts"].items()},
        "recipe_sha256": {Path(path).name: digest for path, digest in artifacts["recipes"].items()},
    }


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def write_json_once(path: Path, value: Any) -> None:
    """Create an immutable receipt; refuse an existing or partial occurrence."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    try:
        with path.open("x", encoding="utf-8", newline="") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as error:
        raise LauncherError(f"Write-once receipt already exists: {path}") from error


def normalize_problem_ids(values: list[str]) -> list[str]:
    normalized: list[str] = []
    for raw in values:
        candidate_id = raw.upper()
        if not re.fullmatch(r"C(?:0[1-9]|1[0-9]|2[0-4])", candidate_id):
            raise LauncherError("Candidate identifiers must be C01 through C24")
        if candidate_id in normalized:
            raise LauncherError("Duplicate candidate identifier: " + candidate_id)
        normalized.append(candidate_id)
    ordered = [candidate_id for candidate_id in PROBLEM_IDS if candidate_id in normalized]
    if ordered != normalized:
        raise LauncherError("Candidates must remain in ascending C01 through C24 order")
    return normalized


def within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def validate_run_root(repo: Path, run_root: Path) -> Path:
    resolved = run_root.resolve()
    allowed = [(repo / "work" / "w18").resolve(), (repo / "work" / "review16").resolve(), Path(r"C:/tr16").resolve()]
    if not any(within(resolved, root) and resolved != root for root in allowed):
        raise LauncherError("R002 output must be a subdirectory of work/w18, work/review16 or C:/tr16")
    return resolved


def candidate_record(study: Path, candidate_id: str) -> dict[str, Any]:
    problem = study / "problems" / f"{candidate_id}.txt"
    answer = study / "answers" / f"{candidate_id}.md"
    oracle = study / "oracle" / f"{candidate_id}.py"
    recoding_maps = study / "problems" / "RECODING_MAPS.json"
    missing = [path for path in (problem, answer, oracle, recoding_maps) if not path.is_file()]
    if missing:
        raise LauncherError("Candidate package incomplete: " + ", ".join(str(path) for path in missing))
    maps = read_json(recoding_maps)
    entries = maps.get("candidates", maps) if isinstance(maps, dict) else None
    if isinstance(entries, list):
        entry = next((item for item in entries if item.get("candidate_id") == candidate_id), None)
    elif isinstance(entries, dict):
        entry = entries.get(candidate_id)
    else:
        entry = None
    if not isinstance(entry, dict):
        raise LauncherError("Missing recoding/carrier declaration for " + candidate_id)
    recoded_value = entry.get("recoded_problem_path") or entry.get("recoded_path")
    carrier_value = entry.get("carrier_problem_path") or entry.get("carrier_path")
    if not isinstance(recoded_value, str) or not isinstance(carrier_value, str):
        raise LauncherError("Invalid recoding/carrier declaration for " + candidate_id)
    recoded = study / recoded_value if not Path(recoded_value).is_absolute() else Path(recoded_value)
    carrier = study / carrier_value if not Path(carrier_value).is_absolute() else Path(carrier_value)
    if not recoded.is_file() or not carrier.is_file():
        raise LauncherError("Recoded or carrier problem is missing for " + candidate_id)
    oracle_kind = entry.get("oracle_kind")
    checker_eligible = entry.get("checker_eligible")
    if oracle_kind not in {"computable", "derivation-only"} or type(checker_eligible) is not bool:
        raise LauncherError("Candidate oracle metadata is missing or invalid for " + candidate_id)
    if checker_eligible is not (oracle_kind == "computable"):
        raise LauncherError("Checker eligibility disagrees with oracle kind for " + candidate_id)
    declared_paths = {
        "problem_path": problem,
        "answer_path": answer,
        "oracle_path": oracle,
    }
    for key, actual in declared_paths.items():
        declared = entry.get(key)
        if not isinstance(declared, str):
            raise LauncherError(f"Candidate {key} is missing for {candidate_id}")
        declared_path = study / declared if not Path(declared).is_absolute() else Path(declared)
        if declared_path.resolve() != actual.resolve():
            raise LauncherError(f"Candidate {key} disagrees with sealed layout for {candidate_id}")
    declared_hashes = entry.get("hashes")
    if not isinstance(declared_hashes, dict):
        raise LauncherError("Candidate hashes object is missing for " + candidate_id)
    actual_hashes = {
        "problem_sha256": sha256(problem),
        "answer_sha256": sha256(answer),
        "oracle_sha256": sha256(oracle),
    }
    for key, actual_hash in actual_hashes.items():
        if declared_hashes.get(key) != actual_hash:
            raise LauncherError(f"Candidate {key} differs from the file for {candidate_id}")
    variant_hashes = {
        "recoded_problem_sha256": sha256(recoded),
        "carrier_problem_sha256": sha256(carrier),
    }
    for key, actual_hash in variant_hashes.items():
        if declared_hashes.get(key) != actual_hash:
            raise LauncherError(f"Candidate {key} differs from the file for {candidate_id}")
    supports = entry.get("oracle_support_paths", [])
    support_hashes = entry.get("oracle_support_sha256", {})
    if set(supports) != set(support_hashes):
        raise LauncherError("Oracle support hash keys differ")
    for support in supports:
        source = study / support
        if not within(source, study / "oracle") or not source.is_file() or sha256(source) != support_hashes[support]:
            raise LauncherError("Oracle support pin mismatch")
    return {
        "candidate_id": candidate_id,
        "problem_path": problem.relative_to(study).as_posix(),
        "problem_sha256": actual_hashes["problem_sha256"],
        "sealed_answer_path": answer.relative_to(study).as_posix(),
        "sealed_answer_sha256": actual_hashes["answer_sha256"],
        "oracle_path": oracle.relative_to(study).as_posix(),
        "oracle_sha256": actual_hashes["oracle_sha256"],
        "oracle_kind": oracle_kind,
        "checker_eligible": checker_eligible,
        "recoding_map_id": entry.get("recoding_map_id", candidate_id),
        "recoded_problem_path": recoded.relative_to(study).as_posix(),
        "recoded_problem_sha256": variant_hashes["recoded_problem_sha256"],
        "carrier_problem_path": carrier.relative_to(study).as_posix(),
        "carrier_problem_sha256": variant_hashes["carrier_problem_sha256"],
    }


def budget(admitted_count: int, computable_count: int, optional_case_occurrences: int = 0) -> dict[str, int]:
    if not 0 <= computable_count <= admitted_count <= 8 or not 0 <= optional_case_occurrences <= 3 * admitted_count:
        raise LauncherError("Invalid admitted/computable/optional counts")
    completion = 786432 + 966656 * admitted_count + 311296 * computable_count + 311296 * optional_case_occurrences
    attempts = 24 + 43 * admitted_count + 14 * computable_count + 14 * optional_case_occurrences
    return {
        "calibration_candidates": 24, "admitted": admitted_count,
        "computable_admitted": computable_count, "optional_case_occurrences": optional_case_occurrences,
        "logical_calls": attempts, "maximum_attempts": attempts,
        "completion_token_ceiling": completion, "prompt_token_ceiling": 32768 * attempts,
        "combined_token_ceiling": completion + 32768 * attempts, "per_attempt_wall_seconds": 300,
        "aggregate_attempt_wall_seconds": 300 * attempts,
    }


def calibration_fixture(candidate: dict[str, Any], occurrence: int) -> dict[str, Any]:
    candidate_id = candidate["candidate_id"]
    return {
        "schema": SCHEMA,
        "occurrence_id": f"R002-{candidate_id}-CAL-NATIVE-attempt-{occurrence:03d}",
        "candidate_id": candidate_id,
        "condition": "CAL-NATIVE",
        "mode": "offline",
        "status": "OFFLINE_STRUCTURAL_FIXTURE",
        "calls_made": 0,
        "intended_live_calls": 1,
        "intended_live_attempts": 1,
        "endpoint": "deepseek-flash", "thinking": "native", "wall_seconds": 300,
        "completion_token_ceiling": 32768,
        "scientific_evidence": False,
        "admission_eligible": False,
        "main_input_eligible": False,
        "problem_path": candidate["problem_path"],
        "problem_sha256": candidate["problem_sha256"],
        "sealed_answer_sha256": candidate["sealed_answer_sha256"],
        "oracle_sha256": candidate["oracle_sha256"],
        "oracle_kind": candidate["oracle_kind"],
        "note": "No model ran. This checks orchestration only and cannot admit a problem.",
    }


def validate_admission_receipt(
    path: Path,
    *,
    study: Path | None = None,
    allow_offline_fixture: bool,
) -> tuple[list[str], dict[str, Any]]:
    receipt = read_json(path)
    if not isinstance(receipt, dict) or receipt.get("schema") != ADMISSION_SCHEMA:
        raise LauncherError("Admission receipt has the wrong schema")
    evidence_kind = receipt.get("evidence_kind", "live-calibration")
    if evidence_kind == "offline-test-fixture" and not allow_offline_fixture:
        raise LauncherError("Offline admission fixtures are allowed only in offline validation")
    if evidence_kind not in {"live-calibration", "offline-test-fixture"}:
        raise LauncherError("Admission receipt evidence_kind is invalid")
    if evidence_kind == "live-calibration":
        if study is None:
            raise LauncherError("Live admission validation requires the study path")
        phase_value = receipt.get("calibration_phase_receipt_path")
        phase_hash = receipt.get("calibration_phase_receipt_sha256")
        manifest_hash = receipt.get("candidate_manifest_sha256")
        if not all(isinstance(value, str) and value for value in (phase_value, phase_hash, manifest_hash)):
            raise LauncherError("Live admission lacks calibration or candidate-manifest linkage")
        phase_path = Path(phase_value)
        if not phase_path.is_absolute():
            phase_path = path.parent / phase_path
        candidate_manifest = study / "CANDIDATES.md"
        if (not phase_path.is_file() or sha256(phase_path) != phase_hash
                or not candidate_manifest.is_file() or sha256(candidate_manifest) != manifest_hash):
            raise LauncherError("Live admission calibration or candidate-manifest hash differs")
        phase_receipt = read_json(phase_path)
        phase_records = phase_receipt.get("records") if isinstance(phase_receipt, dict) else None
        if (not isinstance(phase_receipt, dict)
                or phase_receipt.get("phase") != "calibration"
                or phase_receipt.get("mode") != "live"
                or phase_receipt.get("scientific_evidence") is not True
                or phase_receipt.get("selected_candidates") != list(PROBLEM_IDS)
                or not isinstance(phase_records, list)):
            raise LauncherError("Linked live calibration phase receipt is incomplete")
        phase_by_id = {
            item.get("candidate_id"): item for item in phase_records
            if isinstance(item, dict) and item.get("candidate_id") in PROBLEM_IDS
        }
        if len(phase_records) != 24 or set(phase_by_id) != set(PROBLEM_IDS):
            raise LauncherError("Linked live calibration phase does not contain 24 unique trials")
    else:
        phase_by_id = {}
    records = receipt.get("records")
    if not isinstance(records, list):
        raise LauncherError("Admission receipt records must be a list")
    by_id: dict[str, dict[str, Any]] = {}
    required = {
        "candidate_id", "calibration_attempt_id", "baseline_run_id", "oracle_result",
        "native_final_answer_path", "native_final_answer_sha256", "verdict", "admitted",
        "exclusion_reason", "reader_identity", "read_utc", "operational_status",
        "operational_failure_cause", "problem_sha256", "sealed_answer_sha256",
        "oracle_sha256", "oracle_kind", "no_answer_reason",
    }
    for record in records:
        if not isinstance(record, dict) or not required <= set(record):
            raise LauncherError("Admission receipt record is missing required fields")
        candidate_id = record["candidate_id"]
        if candidate_id not in PROBLEM_IDS or candidate_id in by_id:
            raise LauncherError("Admission receipt candidate IDs are invalid or duplicated")
        verdict = record["verdict"]
        if verdict not in ALL_VERDICTS:
            raise LauncherError("Admission verdict is invalid for " + candidate_id)
        if str(record.get("operational_status", "")).lower() == "ceiling_hit" and record.get("native_final_answer_path") is None and verdict != "no_answer":
            raise LauncherError("CEILING_HIT without final answer must be no_answer (not answered) and eligible")
        should_admit = verdict in ADMISSION_VERDICTS
        if record["admitted"] is not should_admit:
            raise LauncherError("Admission flag disagrees with verdict for " + candidate_id)
        if evidence_kind == "live-calibration" and not record["reader_identity"]:
            raise LauncherError("Live admission requires a reader identity")
        if evidence_kind == "live-calibration":
            candidate = candidate_record(study, candidate_id)
            for field in ("problem_sha256", "sealed_answer_sha256", "oracle_sha256", "oracle_kind"):
                if record[field] != candidate[field]:
                    raise LauncherError(f"Admission {field} differs for {candidate_id}")
            phase_record = phase_by_id[candidate_id]
            pilot_required = {"logical_calls": 1, "attempts": 1, "completion_token_ceiling": 32768,
                              "endpoint": "deepseek-flash", "thinking": "native", "wall_seconds": 300}
            if any(phase_record.get(key) != value for key, value in pilot_required.items()):
                raise LauncherError("Calibration trial must be exactly one native call/attempt at 32768 and 300 s")
            phase_attempt = phase_record.get("occurrence_id") or phase_record.get("calibration_attempt_id")
            if record["calibration_attempt_id"] != phase_attempt:
                raise LauncherError("Admission trial identity differs for " + candidate_id)
            if record["baseline_run_id"] != phase_record.get("baseline_run_id"):
                raise LauncherError("Admission baseline run identity differs for " + candidate_id)
            if verdict == "no_answer" and not record["no_answer_reason"]:
                raise LauncherError("no_answer requires a distinct no_answer_reason")
            if verdict != "no_answer" and record["no_answer_reason"] is not None:
                raise LauncherError("Only no_answer may carry no_answer_reason")
            operational_status = str(record["operational_status"]).lower()
            if operational_status not in {"completed", "ceiling_hit", "transport_error", "schema_failure"}:
                raise LauncherError("Operational status is invalid for " + candidate_id)
            if operational_status == "completed" and record["operational_failure_cause"] is not None:
                raise LauncherError("Completed calibration may not carry an operational failure cause")
            if operational_status != "completed" and not record["operational_failure_cause"]:
                raise LauncherError("Operational failure requires a separate cause")
            answer_value = record["native_final_answer_path"]
            answer_hash = record["native_final_answer_sha256"]
            if verdict == "no_answer" and answer_value is None:
                if answer_hash is not None:
                    raise LauncherError("Absent final answer may not carry an answer hash")
            else:
                if not isinstance(answer_value, str) or not isinstance(answer_hash, str):
                    raise LauncherError("Completed final answer lacks path/hash for " + candidate_id)
                answer_path = Path(answer_value)
                if not answer_path.is_absolute():
                    answer_path = path.parent / answer_path
                if not answer_path.is_file() or sha256(answer_path) != answer_hash:
                    raise LauncherError("Final answer hash differs for " + candidate_id)
        by_id[candidate_id] = record
    if evidence_kind == "live-calibration" and set(by_id) != set(PROBLEM_IDS):
        raise LauncherError("Live calibration receipt must cover all 24 candidates")
    admitted = [candidate_id for candidate_id in PROBLEM_IDS
                if candidate_id in by_id and by_id[candidate_id]["verdict"] in ADMISSION_VERDICTS][:8]
    return admitted, receipt


def child_environment() -> dict[str, str]:
    child = os.environ.copy()
    for name in PROVIDER_KEYS:
        child.pop(name, None)
    child.update({
        "PYTHONUTF8": "1",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPATH": os.pathsep.join(("src", "tests")),
        "TMP": os.environ.get("TMP", r"C:\tr16"),
    })
    return child


def run_legacy_cross_offline(repo: Path, problem: Path, out: Path) -> dict[str, Any]:
    if out.exists():
        marker = out / "state.json"
        if not marker.is_file():
            raise LauncherError("Existing LOOP-CROSS occurrence is partial; allocate a new occurrence")
        state = read_json(marker)
        return {
            "action": "preserved-existing",
            "returncode": None,
            "stop_reason": state.get("stop_reason", "unknown") if isinstance(state, dict) else "unknown",
            "run_directory": str(out),
        }
    command = [
        sys.executable, str(repo / "tools" / "reason.py"), "run",
        "--problem", str(problem), "--cycles", "3", "--recipe", "cross-family",
        "--out", str(out), "--mode", "offline", "--retry-transport", "0",
    ]
    completed = subprocess.run(
        command, cwd=repo, env=child_environment(), capture_output=True, text=True,
        encoding="utf-8", errors="strict", check=False,
    )
    if completed.returncode != 0:
        raise LauncherError(
            "Existing offline LOOP-CROSS engine failed; occurrence retained: "
            + str(out) + "\n" + completed.stderr
        )
    return {
        "action": "actual-existing-cli-offline",
        "returncode": completed.returncode,
        "stop_reason": read_json(out / "state.json").get("stop_reason", "unknown"),
        "run_directory": str(out),
        "stdout_sha256": hashlib.sha256(completed.stdout.encode("utf-8")).hexdigest(),
        "stderr_sha256": hashlib.sha256(completed.stderr.encode("utf-8")).hexdigest(),
    }


def structural_main_fixture(condition: str, candidate: dict[str, Any], occurrence: int) -> dict[str, Any]:
    candidate_id = candidate["candidate_id"]
    calls = 1 if condition == "NATIVE" else 14
    return {
        "schema": SCHEMA,
        "occurrence_id": f"R002-{candidate_id}-{condition}-attempt-{occurrence:03d}",
        "candidate_id": candidate_id,
        "condition": condition,
        "recipe_id": RECIPE_IDS.get(condition),
        "mode": "offline",
        "status": "OFFLINE_STRUCTURAL_FIXTURE",
        "calls_made": 0,
        "intended_live_calls_maximum": calls,
        "completion_token_ceiling": 32768 if condition == "NATIVE" else 311296,
        "attempts_maximum": calls,
        "scientific_evidence": False,
        "prompt_contract_validated": False,
        "strict_terminal_failure": "stop-occurrence",
        "problem_path": candidate["problem_path"],
        "problem_sha256": candidate["problem_sha256"],
        "recoded_problem_path": candidate["recoded_problem_path"] if condition == "LOOP-RECODED" else None,
        "carrier_problem_path": candidate["carrier_problem_path"] if condition == "LOOP-CARRIER" else None,
        "note": "No model ran. The engine lacks r002-contracts-v2; this fixture validates scheduling only.",
    }


def refuse_live(study: Path) -> None:
    capability = study / "contracts" / "ENGINE_CAPABILITY.json"
    if not capability.is_file():
        raise LauncherError(
            "Live R002 is blocked: engineering must add contracts/ENGINE_CAPABILITY.json "
            "and engine support for r002-contracts-v2; legacy recipes are not substitutes"
        )
    data = read_json(capability)
    hash_maps = capability_hash_maps(study)
    expected = {
        "schema": CAPABILITY_SCHEMA,
        "capability": CAPABILITY_NAME,
        "prompt_contract": "r002-episodes-v2",
        "strict_attempt_policy": True,
        "maximum_cycles": 3,
        "no_new_objections_stop": True, "stall_switch": True, "off_completion_tokens": 16384,
        "unconditional_closing_return": True,
        "prompt_token_cap": 32768,
    }
    if (not isinstance(data, dict)
            or any(data.get(key) != value for key, value in expected.items())
            or data.get("schema_sha256") != hash_maps["schema_sha256"]
            or data.get("recipe_sha256") != hash_maps["recipe_sha256"]
            or not isinstance(data.get("checker_backend_qualified"), bool)
            or not isinstance(data.get("review_receipt"), str)
            or not data["review_receipt"].strip()):
        raise LauncherError("Live R002 is blocked: engine capability does not match r002-contracts-v2")
    raise LauncherError(
        "Live R002 remains blocked in this staged launcher until the engineering run wires and tests "
        "the declared schema hashes, tokenizer pin, checker policy, and exact CLI adapter"
    )


def run_calibration(study: Path, run_root: Path, selected: list[str], occurrence: int) -> dict[str, Any]:
    phase_root = run_root / f"calibration-occurrence-{occurrence:03d}"
    receipt_path = phase_root / "phase-receipt.json"
    if receipt_path.exists():
        raise LauncherError("Calibration occurrence already exists; allocate a new --occurrence")
    records = []
    for candidate_id in selected:
        candidate = candidate_record(study, candidate_id)
        path = phase_root / candidate_id / "CAL-NATIVE" / "fixture.json"
        fixture = calibration_fixture(candidate, occurrence)
        write_json_once(path, fixture)
        records.append({
            "candidate_id": candidate_id,
            "occurrence_id": fixture["occurrence_id"],
            "baseline_run_id": None,
            "problem_sha256": candidate["problem_sha256"],
            "sealed_answer_sha256": candidate["sealed_answer_sha256"],
            "oracle_sha256": candidate["oracle_sha256"],
            "oracle_kind": candidate["oracle_kind"],
            "fixture_path": path.relative_to(run_root).as_posix(),
        })
    candidate_manifest = study / "CANDIDATES.md"
    receipt = {
        "schema": SCHEMA,
        "phase": "calibration",
        "mode": "offline",
        "occurrence": occurrence,
        "created_utc": utc_now(),
        "selected_candidates": selected,
        "candidate_manifest_path": "CANDIDATES.md",
        "candidate_manifest_sha256": sha256(candidate_manifest) if candidate_manifest.is_file() else None,
        "proposed_artifact_sha256": proposed_artifact_hashes(study),
        "records": records,
        "scientific_evidence": False,
        "admission_eligible": False,
        "pilot_output_allowed_in_main_prompts": False,
        "export_allowlist": [item["fixture_path"] for item in records] + [
            receipt_path.relative_to(run_root).as_posix()
        ],
    }
    write_json_once(receipt_path, receipt)
    return receipt


def run_main(
    repo: Path,
    study: Path,
    run_root: Path,
    receipt_path: Path,
    occurrence: int,
    optional_conditions: tuple[str, ...] = (),
) -> dict[str, Any]:
    admitted, admission = validate_admission_receipt(
        receipt_path, study=study, allow_offline_fixture=True,
    )
    if not admitted:
        result = {
            "schema": SCHEMA,
            "phase": "main",
            "mode": "offline",
            "status": "STOP_ZERO_ADMITTED",
            "admitted": [],
            "scientific_evidence": False,
        }
        write_json_once(run_root / f"main-occurrence-{occurrence:03d}" / "phase-receipt.json", result)
        return result
    phase_root = run_root / f"main-occurrence-{occurrence:03d}"
    phase_receipt = phase_root / "phase-receipt.json"
    if phase_receipt.exists():
        raise LauncherError("Main occurrence already exists; allocate a new --occurrence")
    records: list[dict[str, Any]] = []
    export_allowlist: list[str] = []
    main_input_allowlist: list[str] = []
    computable = 0
    for candidate_id in admitted:
        candidate = candidate_record(study, candidate_id)
        if candidate["checker_eligible"]:
            computable += 1
        conditions = (CONDITION_ORDER if candidate["checker_eligible"] else CONDITION_ORDER[:-1]) + optional_conditions
        main_input_allowlist.extend([
            candidate["problem_path"],
            candidate["recoded_problem_path"],
            *([candidate["carrier_problem_path"]] if "LOOP-CARRIER" in optional_conditions else []),
        ])
        for condition in conditions:
            target = phase_root / candidate_id / condition
            fixture_path = target / "fixture.json"
            record = structural_main_fixture(condition, candidate, occurrence)
            write_json_once(fixture_path, record)
            evidence_path = fixture_path.relative_to(run_root).as_posix()
            export_allowlist.append(evidence_path)
            records.append({
                "candidate_id": candidate_id,
                "condition": condition,
                "status": record.get("status", record.get("action")),
                "evidence_path": evidence_path,
            })
    result = {
        "schema": SCHEMA,
        "phase": "main",
        "mode": "offline",
        "occurrence": occurrence,
        "created_utc": utc_now(),
        "admission_receipt_path": str(receipt_path.resolve()),
        "admission_receipt_sha256": sha256(receipt_path),
        "admission_evidence_kind": admission.get("evidence_kind", "live-calibration"),
        "admitted": admitted,
        "stopping_rule": "first eight incorrect/no_answer in ascending candidate ID; all 1-7 if fewer; stop at zero",
        "records": records,
        "budget": budget(len(admitted), computable, len(admitted) * len(optional_conditions)),
        "optional_conditions": list(optional_conditions),
        "proposed_artifact_sha256": proposed_artifact_hashes(study),
        "scientific_evidence": False,
        "pilot_output_allowed_in_main_prompts": False,
        "main_input_allowlist": sorted(set(main_input_allowlist)),
        "credential_name_allowlist": list(PROVIDER_KEYS),
        "export_allowlist": export_allowlist + [phase_receipt.relative_to(run_root).as_posix()],
    }
    write_json_once(phase_receipt, result)
    return result


def validate_optional_receipts(paths: list[Path]) -> tuple[str, ...]:
    enabled: list[str] = []
    for path in paths:
        data = read_json(path)
        if not isinstance(data, dict) or data.get("schema") != "minireason.r002.optional-arm-receipt.v1":
            raise LauncherError("Optional arm requires its own receipt")
        condition = data.get("condition")
        if condition not in OPTIONAL_CONDITIONS or condition in enabled:
            raise LauncherError("Invalid or duplicate optional condition")
        if not all(isinstance(data.get(k), str) and data[k].strip() for k in ("decision_receipt", "reason", "occurrence_id")):
            raise LauncherError("Optional receipt lacks decision, reason or occurrence identity")
        if data.get("max_calls_per_case") != 14 or data.get("completion_tokens_per_case") != 311296:
            raise LauncherError("Optional receipt budget does not match the common envelope")
        if not isinstance(data.get("candidate_ids"), list) or not data["candidate_ids"]:
            raise LauncherError("Optional receipt must name candidate IDs")
        normalize_problem_ids(data["candidate_ids"])
        enabled.append(condition)
    return tuple(c for c in OPTIONAL_CONDITIONS if c in enabled)


def prospective_child_argv(repo: Path, study: Path, candidate_id: str, condition: str,
                           out: Path, env_file: Path | None) -> list[str]:
    # Pure command construction. Never opens env_file or dispatches a provider.
    args = [sys.executable, str(repo / "tools" / "reason.py")]
    native = condition in {"CAL-NATIVE", "NATIVE"}
    args += ["run-r002-native" if native else "run-r002", "--problem", str(study / "problems" / (candidate_id + ".txt"))]
    if native:
        args += ["--condition", condition, "--schema", str(study / "contracts" / "answer.schema.json"),
                 "--thinking", "native", "--reasoning-effort", "medium", "--completion-tokens", "32768"]
    else:
        args += ["--recipe", str(study / "recipes" / (RECIPE_IDS[condition] + ".json")), "--cycles", "3"]
    args += ["--attempt-policy", "strict", "--prompt-token-cap", "32768", "--retry-transport", "0",
             "--tokenizer-pins", str(study / "TOKENIZER_PINS.json"),
             "--relations", str(study / "problems" / "RELATIONS.json"),
             "--capability", str(study / "contracts" / "ENGINE_CAPABILITY.json"),
             "--mode", "live", "--out", str(out)]
    if not native:
        args += ["--fork-registry", str(study / "problems" / "FORKS.json"),
                 "--coding-manifest", str(study / "problems" / "RECODING_MAPS.json")]
    if condition == "LOOP-CHECKER":
        args += ["--checker-policy", str(study / "CHECKER_POLICY.json")]
    if env_file is not None:
        args += ["--env-file", str(env_file)]
    return args


def frozen_context(study: Path, args: argparse.Namespace, optional: tuple[str, ...]) -> dict[str, Any]:
    # Freeze executable inputs, public registries, sealed hashes and recipes. No env-file read.
    source = [study / n for n in ("run_R002.py", "PLAN.md", "INSTRUMENT.md", "CANDIDATES.md")]
    source += [p for folder in ("problems", "answers", "oracle", "contracts", "recipes")
               for p in (study / folder).rglob("*") if p.is_file() and p.suffix in {".txt", ".md", ".json", ".py"}]
    context = {"phase": args.phase, "mode": args.mode, "occurrence": args.occurrence,
               "selected_candidates": normalize_problem_ids(args.problems), "optional_conditions": list(optional),
               "source_sha256": {p.relative_to(study).as_posix(): sha256(p) for p in sorted(source)},
               "admission_sha256": sha256(args.admission_receipt) if args.admission_receipt else None,
               "optional_receipt_sha256": [sha256(p) for p in args.optional_receipt],
               "env_file_forwarded_path": str(args.env_file) if args.env_file else None,
               "env_file_read": False}
    condition = "CAL-NATIVE" if args.phase == "calibration" else "LOOP-TESTED"
    context["prospective_child_argv_example"] = prospective_child_argv(
        study.parents[2], study, normalize_problem_ids(args.problems)[0], condition,
        args.run_root / "future-live-occurrence-NOT-RUN", args.env_file)
    return context


def verify_completed_manifest(path: Path, phase_root: Path, expected: dict[str, Any]) -> None:
    if not path.is_file():
        raise LauncherError("Partial occurrence has no complete manifest; preserve it without replay")
    manifest = read_json(path)
    if (not isinstance(manifest, dict) or manifest.get("schema") != "minireason.r002.offline-manifest.v2"
            or manifest.get("state") != "COMPLETE" or manifest.get("context") != expected):
        raise LauncherError("Resume context/source mismatch; saved occurrence is preserved")
    recorded = manifest.get("evidence_sha256")
    if not isinstance(recorded, dict) or not recorded:
        raise LauncherError("Resume manifest lacks evidence")
    actual = {p.relative_to(phase_root).as_posix(): sha256(p) for p in sorted(phase_root.rglob("*"))
              if p.is_file() and p != path}
    if recorded != actual:
        raise LauncherError("Resume evidence mismatch; never silently replay or repair")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("calibration", "main"), required=True)
    parser.add_argument("--mode", choices=("offline", "live"), default="offline")
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--occurrence", type=int, default=1)
    parser.add_argument("--problems", nargs="+", default=list(PROBLEM_IDS), metavar="CNN")
    parser.add_argument("--admission-receipt", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--optional-receipt", type=Path, action="append", default=[])
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo = Path(__file__).resolve().parents[3]
    study = Path(__file__).resolve().parent
    if args.occurrence < 1:
        raise LauncherError("--occurrence must be a positive integer")
    selected = normalize_problem_ids(args.problems)
    run_root = validate_run_root(repo, args.run_root if args.run_root.is_absolute() else repo / args.run_root)
    if args.mode == "live":
        refuse_live(study)
    optional = validate_optional_receipts(args.optional_receipt)
    if args.phase == "calibration" and optional:
        raise LauncherError("Optional arms belong only to main")
    if args.phase == "main" and args.admission_receipt is None:
        raise LauncherError("--admission-receipt is required for the main phase")
    if args.phase == "main":
        admitted, _ = validate_admission_receipt(args.admission_receipt.resolve(), study=study, allow_offline_fixture=True)
        for optional_path in args.optional_receipt:
            if read_json(optional_path)["candidate_ids"] != admitted:
                raise LauncherError("Optional receipt candidate IDs must equal this admitted set")
        if selected != list(PROBLEM_IDS) and selected != admitted:
            raise LauncherError("Main --problems must equal the frozen admission selection; no silent subset")
    phase_root = run_root / f"{args.phase}-occurrence-{args.occurrence:03d}"
    manifest_path = phase_root / "manifest.json"
    context = frozen_context(study, args, optional)
    if phase_root.exists():
        if args.resume:
            verify_completed_manifest(manifest_path, phase_root, context)
            print(json.dumps({"phase": args.phase, "mode": args.mode, "status": "SKIPPED_VERIFIED_COMPLETE", "scientific_evidence": False}))
            return 0
        raise LauncherError("Existing/partial occurrence is preserved; use --resume only for verified completion")
    if args.phase == "calibration":
        result = run_calibration(study, run_root, selected, args.occurrence)
    else:
        result = run_main(repo, study, run_root, args.admission_receipt.resolve(), args.occurrence, optional)
    evidence = {p.relative_to(phase_root).as_posix(): sha256(p) for p in sorted(phase_root.rglob("*")) if p.is_file()}
    write_json_once(manifest_path, {"schema": "minireason.r002.offline-manifest.v2", "context": context,
                                  "evidence_sha256": evidence, "state": "COMPLETE", "scientific_evidence": False})
    print(json.dumps({
        "schema": SCHEMA,
        "phase": result["phase"],
        "mode": result["mode"],
        "status": result.get("status", "OFFLINE_COMPLETE"),
        "scientific_evidence": False,
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LauncherError as error:
        print("R002_LAUNCHER_REFUSED: " + str(error), file=sys.stderr)
        raise SystemExit(2)
