"""Durable calibration and main-phase launcher for the published R002 design."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import platform
from typing import Any


SCHEMA = "minireason.r002.launcher.v2"
MANIFEST_SCHEMA = "minireason.r002.launcher-manifest.v1"
ADMISSION_SCHEMA = "minireason.r002.admission-reader.v1"
OPTIONAL_SCHEMA = "minireason.r002.optional-arm-receipt.v1"
PROBLEM_IDS = tuple(f"C{number:02d}" for number in range(1, 25))
ADMISSION_VERDICTS = {"incorrect", "no_answer"}
ALL_VERDICTS = ADMISSION_VERDICTS | {"correct", "unresolved"}
PROVIDER_KEYS = ("DEEPSEEK_API_KEY", "OLLAMA_API_KEY")
DEFAULT_CONDITIONS = (
    "NATIVE", "LOOP-CROSS", "LOOP-TESTED", "LOOP-RECODED", "LOOP-CHECKER",
    "LOOP-DECOMPOSED",
)
OPTIONAL_CONDITIONS = ("LOOP-CROSS-MATCH", "LOOP-CARRIER", "NATIVE-MATCH")
A2_ADMITTED = ("C05", "C06", "C09", "C12")
A2_CONDITIONS = ("LOOP-DECOMPOSED",)
A2_RECIPE_IDS = {"LOOP-DECOMPOSED": "r002-decomposed-v2"}
RECIPE_IDS = {
    "LOOP-CROSS": "r002-cross-v2",
    "LOOP-CROSS-MATCH": "r002-cross-match-v1",
    "LOOP-TESTED": "r002-tested-cross-v1",
    "LOOP-RECODED": "r002-recoded-v1",
    "LOOP-CARRIER": "r002-carrier-v1",
    "NATIVE-MATCH": "r002-native-match-v1",
    "LOOP-CHECKER": "r002-checker-v1",
    "LOOP-DECOMPOSED": "r002-decomposed-v1",
}
LOOP_GOOD_STOPS = {"cycle_budget", "no_new_objections"}
DECOMPOSED_GOOD_STOPS = {
    "complete", "step_budget", "step_unresolved", "initial_cannot_decide",
}
NATIVE_GOOD_STOPS = {"complete", "completed", "COMPLETE", "CEILING_HIT"}


class LauncherError(RuntimeError):
    """A fail-closed launcher refusal."""


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read_text(path: Path) -> str:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return handle.read()
    except (OSError, UnicodeError) as error:
        raise LauncherError("Could not read UTF-8 input: " + str(path)) from error


def read_json(path: Path) -> Any:
    try:
        return json.loads(read_text(path))
    except ValueError as error:
        raise LauncherError("Could not parse JSON: " + str(path)) from error


def write_json(path: Path, value: Any, *, replace: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if not replace:
        try:
            with path.open("x", encoding="utf-8", newline="") as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
        except FileExistsError as error:
            raise LauncherError("Write-once receipt already exists: " + str(path)) from error
        return
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def write_text_once(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as error:
        raise LauncherError("Write-once launcher log already exists: " + str(path)) from error


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def calibration_wire_bound(study: Path) -> dict[str, Any]:
    """Build the reviewed fixed-calibration input bound from exact child wires."""
    from . import config, prompts
    from .adapter import Adapter
    from .r002 import ContractSet, _answer_blocks, _relation_entry, _seat

    relations = read_json(study / "problems" / "RELATIONS.json")
    proof_path = Path(__file__).with_name("r002_calibration_bounds.json")
    proof = read_json(proof_path)
    if (not isinstance(proof, dict)
            or proof.get("schema") != "minireason.r002.calibration-input-bound.v1"
            or proof.get("endpoint") != "deepseek-flash" or proof.get("limit") != 32768
            or set(proof.get("rows", {})) != set(PROBLEM_IDS)):
        raise LauncherError("Reviewed calibration token proof is malformed")
    contracts = ContractSet(study / "contracts")
    adapter = Adapter("offline", {"data": config.load_endpoint_snapshot()["data"]})
    wires: dict[str, dict[str, Any]] = {}
    for candidate_id in PROBLEM_IDS:
        problem = read_text(study / "problems" / f"{candidate_id}.txt")
        relation = _relation_entry(relations, candidate_id)
        messages = prompts.render_r002(
            "answer", [*_answer_blocks(problem, relation), *contracts.prompt_blocks("answer")])
        prepared = adapter.prepare(
            seat=_seat("initial", None), messages=messages, max_tokens=32768,
            thinking="native", role="answer",
            coordinate={"call_id": "initial", "cycle": 0, "attempt": 0,
                        "condition": "CAL-NATIVE", "strict": True})
        raw = prepared["wire_body_text"].encode("utf-8")
        digest = prepared["wire_body_sha256"]
        proven = proof["rows"][candidate_id]
        if (proven.get("wire_sha256") != digest or proven.get("wire_utf8_bytes") != len(raw)
                or type(proven.get("prompt_tokens")) is not int
                or not 0 < proven["prompt_tokens"] <= 32768):
            raise LauncherError(f"Calibration wire differs from reviewed V4.1 token proof for {candidate_id}")
        if digest in wires:
            raise LauncherError("Calibration wires must be unique by candidate")
        wires[digest] = {"candidate_id": candidate_id, "wire_utf8_bytes": len(raw),
                         "prompt_tokens": proven["prompt_tokens"],
                         "rendered_sha256": proven["rendered_sha256"],
                         "rendered_utf8_bytes": proven["rendered_utf8_bytes"]}
    return {
        "schema": "minireason.r002.tokenizers.v1",
        "kind": "fixed-calibration-exact-wire-bound-v1",
        "endpoint": "deepseek-flash",
        "condition": "CAL-NATIVE",
        "role": "answer",
        "prompt_contract": "r002-episodes-v2",
        "limit": 32768,
        "proof_schema": proof["schema"],
        "proof_sha256": sha256(proof_path),
        "model_identity": proof["model_identity"],
        "deepseek_recipe_commit": proof["deepseek_recipe_commit"],
        "tokenizer_sha256": proof["tokenizer_sha256"],
        "tokenizers_package_version": proof["tokenizers_package_version"],
        "measurement_scope": (
            "Exact counts under the pinned public DeepSeek V4.1 serializer/tokenizer; "
            "not observed provider-runtime usage."),
        "review_receipt": "REC-20260917-A",
        "wires": wires,
    }


def normalize_problem_ids(values: list[str]) -> list[str]:
    normalized: list[str] = []
    for raw in values:
        candidate_id = raw.upper()
        if not re.fullmatch(r"C(?:0[1-9]|1[0-9]|2[0-4])", candidate_id):
            raise LauncherError("Candidate identifiers must be C01 through C24")
        if candidate_id in normalized:
            raise LauncherError("Duplicate candidate identifier: " + candidate_id)
        normalized.append(candidate_id)
    if normalized != [item for item in PROBLEM_IDS if item in normalized]:
        raise LauncherError("Candidates must remain in ascending C01 through C24 order")
    return normalized


def within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def validate_run_root(repo: Path, value: Path) -> Path:
    root = (repo / value).resolve() if not value.is_absolute() else value.resolve()
    allowed = ((repo / "runs").resolve(), (repo / "work" / "w20").resolve(),
               (repo / "work" / "review20").resolve(), (repo / "work" / "w28").resolve(),
               (repo / "work" / "review28").resolve(), Path(r"C:/tr28").resolve(),
               Path(r"C:/tw28").resolve(), Path(r"C:/tw20").resolve(),
               Path(r"C:/tr20").resolve(), Path(r"C:/tr21").resolve(),
               Path(r"C:/tw22").resolve(), Path(r"C:/tr22").resolve(),
               Path(r"C:/tw24").resolve(), Path(r"C:/tr24").resolve())
    if not any(root != parent and within(root, parent) for parent in allowed):
        raise LauncherError(
            "R002 output must be below runs/, work/w20/, work/review20/, work/w28/, work/review28/, C:/tr28, C:/tw28, "
            "C:/tw20, C:/tr20, C:/tr21, C:/tw22, C:/tr22, C:/tw24 or C:/tr24")
    if len(str(root)) >= 120:
        raise LauncherError("R002 run root is too long for durable nested evidence")
    return root


def _study_entries(study: Path) -> dict[str, dict[str, Any]]:
    data = read_json(study / "problems" / "RECODING_MAPS.json")
    entries = data.get("candidates") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        raise LauncherError("R002 recoding manifest lacks candidate records")
    result = {}
    for entry in entries:
        if isinstance(entry, dict) and entry.get("candidate_id") in PROBLEM_IDS:
            result[entry["candidate_id"]] = entry
    if set(result) != set(PROBLEM_IDS):
        raise LauncherError("R002 recoding manifest must cover all candidates exactly once")
    return result


def candidate_record(study: Path, candidate_id: str) -> dict[str, Any]:
    entry = _study_entries(study)[candidate_id]
    paths = {
        "problem": study / "problems" / f"{candidate_id}.txt",
        "answer": study / "answers" / f"{candidate_id}.md",
        "oracle": study / "oracle" / f"{candidate_id}.py",
    }
    for path in paths.values():
        if not path.is_file():
            raise LauncherError("Candidate package is incomplete: " + str(path))
    declared = {
        "problem": entry.get("problem_path"),
        "answer": entry.get("answer_path"),
        "oracle": entry.get("oracle_path"),
    }
    for key, relative in declared.items():
        if not isinstance(relative, str) or (study / relative).resolve() != paths[key].resolve():
            raise LauncherError(f"Candidate {candidate_id} has an invalid {key} path")
    recoded_value = entry.get("recoded_problem_path") or entry.get("recoded_path")
    carrier_value = entry.get("carrier_problem_path") or entry.get("carrier_path")
    if not isinstance(recoded_value, str) or not isinstance(carrier_value, str):
        raise LauncherError("Candidate recoding paths are invalid for " + candidate_id)
    recoded, carrier = study / recoded_value, study / carrier_value
    if not recoded.is_file() or not carrier.is_file():
        raise LauncherError("Candidate recoding files are missing for " + candidate_id)
    oracle_kind = entry.get("oracle_kind")
    checker_eligible = entry.get("checker_eligible")
    if oracle_kind not in {"computable", "derivation-only"} or type(checker_eligible) is not bool:
        raise LauncherError("Candidate oracle metadata is invalid for " + candidate_id)
    if checker_eligible is not (oracle_kind == "computable"):
        raise LauncherError("Checker eligibility disagrees with oracle kind for " + candidate_id)
    expected = entry.get("hashes")
    actual = {
        "problem_sha256": sha256(paths["problem"]),
        "answer_sha256": sha256(paths["answer"]),
        "oracle_sha256": sha256(paths["oracle"]),
        "recoded_problem_sha256": sha256(recoded),
        "carrier_problem_sha256": sha256(carrier),
    }
    if not isinstance(expected, dict) or any(expected.get(key) != value for key, value in actual.items()):
        raise LauncherError("Candidate package hashes differ for " + candidate_id)
    return {
        "candidate_id": candidate_id,
        "problem_path": paths["problem"].relative_to(study).as_posix(),
        "problem_sha256": actual["problem_sha256"],
        "sealed_answer_path": paths["answer"].relative_to(study).as_posix(),
        "sealed_answer_sha256": actual["answer_sha256"],
        "oracle_path": paths["oracle"].relative_to(study).as_posix(),
        "oracle_sha256": actual["oracle_sha256"],
        "oracle_kind": oracle_kind,
        "checker_eligible": checker_eligible,
        "recoded_problem_path": recoded.relative_to(study).as_posix(),
        "recoded_problem_sha256": actual["recoded_problem_sha256"],
        "carrier_problem_path": carrier.relative_to(study).as_posix(),
        "carrier_problem_sha256": actual["carrier_problem_sha256"],
    }


def validate_material_pins(study: Path) -> str:
    """Verify the published executable/sealed package without running its oracles."""
    pin_path = study / "MATERIAL_PINS-REVIEW16.json"
    data = read_json(pin_path)
    files = data.get("files") if isinstance(data, dict) else None
    if not isinstance(files, dict) or not files:
        raise LauncherError("Published R002 material pins are missing")
    prefixes = ("problems/", "answers/", "oracle/", "contracts/", "recipes/")
    names = {"PLAN.md", "INSTRUMENT.md", "CANDIDATES.md", "LAUNCHER.md"}
    selected = {name: digest for name, digest in files.items()
                if name.startswith(prefixes) or name in names}
    if not selected:
        raise LauncherError("Published R002 material pins contain no executable package")
    for name, digest in selected.items():
        path = study / name
        if not path.is_file() or not isinstance(digest, str):
            raise LauncherError("Published R002 material pin differs: " + name)
        raw = path.read_bytes()
        matches = hashlib.sha256(raw).hexdigest() == digest
        if not matches and name in {"PLAN.md", "LAUNCHER.md"}:
            marker = b"\n\n## CHANGES - review20 launcher implementation clarification - "
            prefix, separator, tail = raw.partition(marker)
            matches = (separator == marker and marker not in tail
                       and bool(tail.strip()) and hashlib.sha256(prefix).hexdigest() == digest)
        if not matches:
            raise LauncherError("Published R002 material pin differs: " + name)
    return sha256(pin_path)


def budget(admitted_count: int, computable_count: int, optional_case_occurrences: int = 0) -> dict[str, int]:
    if not 0 <= computable_count <= admitted_count <= 8:
        raise LauncherError("Invalid admitted or computable count")
    if not 0 <= optional_case_occurrences <= 3 * admitted_count:
        raise LauncherError("Invalid optional-arm count")
    main_attempts = 56 * admitted_count + 14 * computable_count + 14 * optional_case_occurrences
    main_completion = (
        1261568 * admitted_count
        + 311296 * computable_count
        + 311296 * optional_case_occurrences
    )
    attempts = 24 + main_attempts
    completion = 786432 + main_completion
    return {
        "calibration_candidates": 24,
        "admitted": admitted_count,
        "computable_admitted": computable_count,
        "optional_case_occurrences": optional_case_occurrences,
        "decomposed_calls_per_case": 13,
        "decomposed_completion_tokens_per_case": 294912,
        "main_phase_logical_calls": main_attempts,
        "main_phase_maximum_attempts": main_attempts,
        "main_phase_completion_token_ceiling": main_completion,
        "main_phase_prompt_token_ceiling": main_attempts * 32768,
        "main_phase_combined_token_ceiling": main_completion + main_attempts * 32768,
        "logical_calls": attempts,
        "maximum_attempts": attempts,
        "completion_token_ceiling": completion,
        "prompt_token_ceiling": attempts * 32768,
        "combined_token_ceiling": completion + attempts * 32768,
        "per_attempt_wall_seconds": 300,
        "aggregate_attempt_wall_seconds": attempts * 300,
    }


def a2_budget(case_count: int) -> dict[str, int]:
    if not 0 <= case_count <= len(A2_ADMITTED):
        raise LauncherError("Invalid A2 admitted count")
    logical_per_case = 13
    attempts_per_case = 26
    no_repair_completion_per_case = 344064
    maximum_completion_per_case = 688128
    no_repair_attempts = logical_per_case * case_count
    maximum_attempts = attempts_per_case * case_count
    return {
        "cases": case_count,
        "logical_calls": no_repair_attempts,
        "no_repair_attempts": no_repair_attempts,
        "maximum_attempts": maximum_attempts,
        "no_repair_completion_token_ceiling": no_repair_completion_per_case * case_count,
        "maximum_completion_token_ceiling": maximum_completion_per_case * case_count,
        "no_repair_prompt_token_ceiling": no_repair_attempts * 32768,
        "maximum_prompt_token_ceiling": maximum_attempts * 32768,
        "no_repair_combined_token_ceiling": (
            no_repair_completion_per_case * case_count + no_repair_attempts * 32768),
        "maximum_combined_token_ceiling": (
            maximum_completion_per_case * case_count + maximum_attempts * 32768),
        "no_repair_aggregate_attempt_wall_seconds": no_repair_attempts * 300,
        "maximum_aggregate_attempt_wall_seconds": maximum_attempts * 300,
        "over_three_step_maximum_logical_calls_per_case": 12,
        "over_three_step_maximum_attempts_per_case": 24,
        "over_three_step_maximum_completion_token_ceiling_per_case": 622592,
    }


def validate_admission_receipt(path: Path, study: Path, *, offline: bool) -> tuple[list[str], dict[str, Any]]:
    receipt = read_json(path)
    if not isinstance(receipt, dict) or receipt.get("schema") != ADMISSION_SCHEMA:
        raise LauncherError("Admission receipt has the wrong schema")
    evidence_kind = receipt.get("evidence_kind", "live-calibration")
    if evidence_kind == "offline-test-fixture" and not offline:
        raise LauncherError("Offline admission fixtures cannot authorize live main runs")
    if evidence_kind not in {"offline-test-fixture", "live-calibration"}:
        raise LauncherError("Admission receipt evidence kind is invalid")
    records = receipt.get("records")
    if not isinstance(records, list):
        raise LauncherError("Admission receipt records must be a list")
    by_id: dict[str, dict[str, Any]] = {}
    phase_by_id: dict[str, dict[str, Any]] = {}
    if evidence_kind == "live-calibration":
        phase_value = receipt.get("calibration_phase_receipt_path")
        phase_hash = receipt.get("calibration_phase_receipt_sha256")
        candidate_hash = receipt.get("candidate_manifest_sha256")
        if not all(isinstance(value, str) and value for value in (phase_value, phase_hash, candidate_hash)):
            raise LauncherError("Live admission lacks calibration receipt and candidate-manifest pins")
        phase_path = Path(phase_value)
        if not phase_path.is_absolute():
            phase_path = path.parent / phase_path
        if not phase_path.is_file() or sha256(phase_path) != phase_hash:
            raise LauncherError("Live admission calibration receipt hash differs")
        if sha256(study / "CANDIDATES.md") != candidate_hash:
            raise LauncherError("Live admission candidate manifest hash differs")
        phase_receipt = read_json(phase_path)
        if not isinstance(phase_receipt, dict):
            raise LauncherError("Linked live calibration phase is not an object")
        phase_records = phase_receipt.get("records")
        if (phase_receipt.get("phase") != "calibration" or phase_receipt.get("mode") != "live"
                or phase_receipt.get("scientific_evidence") is not True
                or phase_receipt.get("selected_candidates") != list(PROBLEM_IDS)
                or not isinstance(phase_records, list) or len(phase_records) != 24):
            raise LauncherError("Linked live calibration phase is incomplete")
        phase_by_id = {item.get("candidate_id"): item for item in phase_records if isinstance(item, dict)}
        if set(phase_by_id) != set(PROBLEM_IDS):
            raise LauncherError("Linked live calibration does not contain 24 unique trials")
    for record in records:
        if not isinstance(record, dict):
            raise LauncherError("Admission receipt records must be objects")
        candidate_id = record.get("candidate_id")
        verdict = record.get("verdict")
        if candidate_id not in PROBLEM_IDS or candidate_id in by_id or verdict not in ALL_VERDICTS:
            raise LauncherError("Admission receipt candidate or verdict is invalid")
        no_final = record.get("native_final_answer_path") is None
        if str(record.get("operational_status", "")).lower() == "ceiling_hit" and no_final and verdict != "no_answer":
            raise LauncherError("CEILING_HIT without a final answer must be no_answer")
        should_admit = verdict in ADMISSION_VERDICTS
        if record.get("admitted") is not should_admit:
            raise LauncherError("Admission flag disagrees with verdict for " + candidate_id)
        candidate = candidate_record(study, candidate_id)
        if evidence_kind == "live-calibration":
            required = {
                "calibration_attempt_id", "baseline_run_id", "oracle_result",
                "native_final_answer_path", "native_final_answer_sha256", "exclusion_reason",
                "reader_identity", "reader_lineage", "read_utc", "operational_status",
                "operational_failure_cause", "problem_sha256", "sealed_answer_sha256",
                "oracle_sha256", "oracle_kind", "no_answer_reason", "quoted_claims",
                "derivation_references",
            }
            if not required <= set(record):
                raise LauncherError("Live admission record is missing guarded-reader fields")
            for field in ("problem_sha256", "sealed_answer_sha256", "oracle_sha256", "oracle_kind"):
                if record[field] != candidate[field]:
                    raise LauncherError(f"Admission {field} differs for {candidate_id}")
            if not all(isinstance(record.get(field), str) and record[field].strip()
                       for field in ("calibration_attempt_id", "baseline_run_id", "reader_identity",
                                     "reader_lineage", "read_utc")):
                raise LauncherError("Live admission requires reader, lineage, UTC and attempt identity")
            if "deepseek" in record["reader_lineage"].strip().lower():
                raise LauncherError("Calibration reader must have a distinct non-DeepSeek lineage")
            try:
                read_time = dt.datetime.fromisoformat(record["read_utc"].replace("Z", "+00:00"))
            except ValueError as error:
                raise LauncherError("Calibration reader UTC is invalid") from error
            if read_time.tzinfo is None or read_time.utcoffset() != dt.timedelta(0):
                raise LauncherError("Calibration reader timestamp must be UTC")
            if not isinstance(record["quoted_claims"], list) or not isinstance(record["derivation_references"], list):
                raise LauncherError("Live admission quotations and derivation references must be lists")
            if any(not isinstance(item, str) or not item.strip()
                   for item in record["quoted_claims"] + record["derivation_references"]):
                raise LauncherError("Calibration quotations and derivation references must be nonempty strings")
            if not isinstance(record["oracle_result"], (dict, str)) or not record["oracle_result"]:
                raise LauncherError("Live admission requires the oracle comparison result")
            if verdict != "no_answer" and (not record["quoted_claims"] or not record["derivation_references"]):
                raise LauncherError("Answered calibration verdict requires quoted claims and derivation references")
            if should_admit and record["exclusion_reason"] is not None:
                raise LauncherError("Admitted calibration result may not carry an exclusion reason")
            if not should_admit and (not isinstance(record["exclusion_reason"], str)
                                     or not record["exclusion_reason"].strip()):
                raise LauncherError("Excluded calibration result requires an exclusion reason")
            operational = str(record["operational_status"]).lower()
            if operational not in {"completed", "ceiling_hit", "transport_error", "schema_failure"}:
                raise LauncherError("Calibration operational status is invalid")
            if operational == "completed" and record["operational_failure_cause"] is not None:
                raise LauncherError("Completed calibration may not name an operational failure")
            if operational != "completed" and not record["operational_failure_cause"]:
                raise LauncherError("Failed calibration requires its separate operational cause")
            if verdict == "no_answer" and not record["no_answer_reason"]:
                raise LauncherError("no_answer requires a reason")
            if verdict != "no_answer" and record["no_answer_reason"] is not None:
                raise LauncherError("Only no_answer may carry no_answer_reason")
            answer_value, answer_hash = record["native_final_answer_path"], record["native_final_answer_sha256"]
            if answer_value is None:
                if verdict != "no_answer" or answer_hash is not None:
                    raise LauncherError("Only no_answer may omit the final answer and its hash")
            else:
                if not isinstance(answer_value, str) or not isinstance(answer_hash, str):
                    raise LauncherError("Calibration final answer requires a path and hash")
                answer_path = Path(answer_value)
                if not answer_path.is_absolute():
                    answer_path = path.parent / answer_path
                if not answer_path.is_file() or sha256(answer_path) != answer_hash:
                    raise LauncherError("Calibration final answer hash differs for " + candidate_id)
        by_id[candidate_id] = record
    if evidence_kind == "live-calibration":
        if set(by_id) != set(PROBLEM_IDS):
            raise LauncherError("Live admission must cover all 24 calibration trials")
        for candidate_id, record in by_id.items():
            phase_record = phase_by_id[candidate_id]
            required_trial = {"condition": "CAL-NATIVE", "logical_calls": 1, "attempts": 1,
                              "completion_token_ceiling": 32768, "endpoint": "deepseek-flash",
                              "thinking": "native", "reasoning_effort": "medium", "wall_seconds": 300}
            if any(phase_record.get(key) != value for key, value in required_trial.items()):
                raise LauncherError("Calibration trial is not one strict native 32768/300 call")
            if record.get("calibration_attempt_id") != phase_record.get("occurrence_id"):
                raise LauncherError("Admission calibration identity differs for " + candidate_id)
            if record.get("baseline_run_id") != phase_record.get("baseline_run_id"):
                raise LauncherError("Admission baseline run identity differs for " + candidate_id)
    admitted = [candidate_id for candidate_id in PROBLEM_IDS
                if candidate_id in by_id and by_id[candidate_id]["verdict"] in ADMISSION_VERDICTS][:8]
    return admitted, receipt


def validate_optional_receipts(paths: list[Path], admitted: list[str]) -> tuple[str, ...]:
    enabled: list[str] = []
    for path in paths:
        data = read_json(path)
        condition = data.get("condition") if isinstance(data, dict) else None
        if data.get("schema") != OPTIONAL_SCHEMA or condition not in OPTIONAL_CONDITIONS or condition in enabled:
            raise LauncherError("Optional arm requires one valid, unique receipt")
        if data.get("candidate_ids") != admitted:
            raise LauncherError("Optional receipt candidates must equal the admitted set")
        if data.get("max_calls_per_case") != 14 or data.get("completion_tokens_per_case") != 311296:
            raise LauncherError("Optional receipt budget differs from the common envelope")
        if not all(isinstance(data.get(key), str) and data[key].strip()
                   for key in ("decision_receipt", "reason", "occurrence_id")):
            raise LauncherError("Optional receipt lacks decision, reason or occurrence identity")
        enabled.append(condition)
    return tuple(condition for condition in OPTIONAL_CONDITIONS if condition in enabled)


def _source_snapshot(repo: Path, study: Path) -> dict[str, str]:
    paths = [repo / "tools" / "reason.py", repo / "tools" / "run_R002.py",
             repo / "src" / "minireason" / "data" / "endpoints.json"]
    paths += [path for path in (repo / "src" / "minireason" / "reason").rglob("*")
              if path.is_file() and path.suffix in {".py", ".json"}]
    paths += list((repo / "src" / "minireason").glob("provider*.py"))
    paths.append(repo / "pyproject.toml")
    paths += [path for folder in ("problems", "answers", "oracle", "contracts", "recipes")
              for path in (study / folder).rglob("*")
              if path.is_file() and path.suffix in {".txt", ".md", ".json", ".py"}]
    paths += [study / name for name in ("PLAN.md", "INSTRUMENT.md", "LAUNCHER.md", "CANDIDATES.md")]
    return {path.relative_to(repo).as_posix(): sha256(path) for path in sorted(set(paths))}


def _runtime_identity() -> dict[str, Any]:
    packages = {}
    for name in ("jsonschema", "referencing", "pydantic"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    return {"python": sys.version, "implementation": platform.python_implementation(),
            "platform": platform.platform(), "packages": packages}


def _load_manifest(path: Path, repo: Path, study: Path, mode: str) -> dict[str, Any]:
    source = _source_snapshot(repo, study)
    runtime = _runtime_identity()
    if path.exists():
        manifest = read_json(path)
        if not isinstance(manifest, dict) or manifest.get("schema") != MANIFEST_SCHEMA:
            raise LauncherError("Existing R002 manifest has the wrong schema")
        if manifest.get("mode") != mode:
            raise LauncherError("Existing R002 manifest mode differs")
        versions = manifest.get("source_versions")
        if not isinstance(versions, list) or not versions:
            raise LauncherError("Existing R002 manifest lacks source versions")
        if (versions[-1].get("source_sha256") != source
                or versions[-1].get("runtime_identity") != runtime):
            number = max(int(item.get("version", 0)) for item in versions) + 1
            versions.append({"version": number, "created_utc": utc_now(),
                             "source_sha256": source, "runtime_identity": runtime})
            manifest["active_source_version"] = number
        return manifest
    return {
        "schema": MANIFEST_SCHEMA,
        "created_utc": utc_now(),
        "updated_utc": utc_now(),
        "mode": mode,
        "active_source_version": 1,
        "source_versions": [{"version": 1, "created_utc": utc_now(),
                             "source_sha256": source, "runtime_identity": runtime}],
        "phases": {},
    }


def _child_environment(repo: Path) -> dict[str, str]:
    child = os.environ.copy()
    for name in PROVIDER_KEYS:
        child.pop(name, None)
    child.update({
        "PYTHONUTF8": "1",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPATH": os.pathsep.join((str(repo / "src"), str(repo / "tests"))),
        "TMP": os.environ.get("TMP", r"C:\tr20"),
    })
    return child


def child_argv(repo: Path, study: Path, candidate_id: str, condition: str, out: Path,
               mode: str, *, env_file: Path | None = None, tokenizer_pins: Path | None = None,
               capability: Path | None = None, resume: bool = False,
               cycles: int = 3, recipe_id: str | None = None) -> list[str]:
    if resume:
        command = [sys.executable, str(repo / "tools" / "reason.py"), "resume", "--run", str(out)]
        if mode == "live" and env_file is not None:
            command += ["--env-file", str(env_file)]
        return command
    command = [sys.executable, str(repo / "tools" / "reason.py")]
    native = condition in {"CAL-NATIVE", "NATIVE"}
    command += ["run-r002-native" if native else "run-r002",
                "--problem", str(study / "problems" / f"{candidate_id}.txt"),
                "--out", str(out), "--mode", mode,
                "--relations", str(study / "problems" / "RELATIONS.json"),
                "--attempt-policy", "strict", "--prompt-token-cap", "32768",
                "--retry-transport", "0"]
    if tokenizer_pins is not None:
        command += ["--tokenizer-pins", str(tokenizer_pins)]
    if capability is not None:
        command += ["--capability", str(capability)]
    if native:
        command += ["--condition", condition,
                    "--schema", str(study / "contracts" / "answer.schema.json"),
                    "--thinking", "native", "--reasoning-effort", "medium",
                    "--completion-tokens", "32768"]
    else:
        selected_recipe = recipe_id or RECIPE_IDS[condition]
        command += ["--recipe", str(study / "recipes" / f"{selected_recipe}.json"),
                    "--cycles", str(cycles),
                    "--fork-registry", str(study / "problems" / "FORKS.json"),
                    "--coding-manifest", str(study / "problems" / "RECODING_MAPS.json")]
    if mode == "live" and env_file is not None:
        command += ["--env-file", str(env_file)]
    return command


def _good_stop(condition: str, stop: str) -> bool:
    if condition in {"CAL-NATIVE", "NATIVE"}:
        return stop in NATIVE_GOOD_STOPS
    if condition == "LOOP-DECOMPOSED":
        return stop in DECOMPOSED_GOOD_STOPS
    return stop in LOOP_GOOD_STOPS


def _archive(directory: Path) -> Path:
    source = directory.resolve(strict=True)
    parent = directory.parent.resolve(strict=True)
    if source.parent != parent or source != Path(os.path.abspath(directory)):
        raise LauncherError("Occurrence archive source resolves through a link")
    number = 1
    while True:
        target = directory.with_name(directory.name + f"-failed-{number}")
        if not target.exists():
            directory.rename(target)
            return target
        number += 1


def _attempt(record: dict[str, Any], condition: str, candidate_id: str, directory: Path,
             run_root: Path, source_version: int,
             occurrence_scope: str | None = None) -> dict[str, Any]:
    attempts = record.setdefault("attempts", [])
    number = len(attempts) + 1
    prefix = f"R002-{occurrence_scope}" if occurrence_scope else "R002"
    item = {
        "attempt_number": number,
        "occurrence_id": f"{prefix}-{candidate_id}-{condition}-attempt-{number:03d}",
        "directory": directory.relative_to(run_root).as_posix(),
        "source_version": source_version,
        "status": "allocated",
        "stop_reason": "not_started",
        "returncode": None,
        "updated_utc": utc_now(),
    }
    attempts.append(item)
    return item


def _verify_launcher_logs(run_root: Path, attempt: dict[str, Any]) -> None:
    for invocation in attempt.get("launcher_invocations", []):
        for kind in ("stdout", "stderr"):
            value, digest = invocation.get(kind + "_path"), invocation.get(kind + "_sha256")
            if not isinstance(value, str) or not isinstance(digest, str):
                raise LauncherError("Launcher invocation log receipt is incomplete")
            path = run_root / value
            if not path.is_file() or sha256(path) != digest:
                raise LauncherError("Launcher invocation log differs: " + str(path))


def _verify_active_sources(repo: Path, study: Path, manifest: dict[str, Any], phase: dict[str, Any],
                           args: argparse.Namespace) -> None:
    version = manifest["source_versions"][manifest["active_source_version"] - 1]
    if (version.get("source_sha256") != _source_snapshot(repo, study)
            or version.get("runtime_identity") != _runtime_identity()):
        raise LauncherError("R002 engineering source or runtime changed during the phase")
    expected = {
        "admission_sha256": sha256(args.admission_receipt.resolve()) if args.admission_receipt else None,
        "optional_receipt_sha256": [sha256(path.resolve()) for path in args.optional_receipt],
        "tokenizer_pins_sha256": sha256(args.tokenizer_pins.resolve()) if args.tokenizer_pins else None,
        "capability_sha256": sha256(args.capability.resolve()) if args.capability else None,
    }
    if any(phase.get(key) != value for key, value in expected.items()):
        raise LauncherError("R002 admission, optional, tokenizer or capability input changed during the phase")


def _run_occurrence(repo: Path, study: Path, run_root: Path, manifest_path: Path,
                    manifest: dict[str, Any], phase: dict[str, Any], candidate_id: str,
                    condition: str, directory: Path, args: argparse.Namespace,
                    *, cycles: int = 3) -> tuple[dict[str, Any], bool]:
    _verify_active_sources(repo, study, manifest, phase, args)
    candidates = phase.setdefault("candidates", {})
    conditions = candidates.setdefault(candidate_id, {}).setdefault("conditions", {})
    record = conditions.setdefault(condition, {"attempts": []})
    attempts = record["attempts"]
    resume = False
    if directory.exists():
        if not attempts:
            raise LauncherError("Unmanifested occurrence directory is preserved: " + str(directory))
        current = attempts[-1]
        _verify_launcher_logs(run_root, current)
        state_path = directory / "state.json"
        state = read_json(state_path) if state_path.is_file() else None
        stop = state.get("stop_reason", "partial") if isinstance(state, dict) else "partial"
        if args.rerun_failed:
            if args.phase == "calibration":
                raise LauncherError("Calibration is once-only; --rerun-failed is forbidden")
            if _good_stop(condition, stop):
                if current.get("evidence_sha256") != tree_hashes(directory):
                    raise LauncherError("Good-stop occurrence evidence differs: " + str(directory))
                return current, True
            archived = _archive(directory)
            current.update({"status": "archived-failed",
                            "directory": archived.relative_to(run_root).as_posix(),
                            "archived_utc": utc_now()})
            current = _attempt(
                record, condition, candidate_id, directory, run_root,
                manifest["active_source_version"],
                occurrence_scope=(
                    f"{args.phase}-occurrence-{args.occurrence:03d}"
                    if args.amendment_a2 else None),
            )
        elif args.resume:
            if _good_stop(condition, stop):
                hashes = tree_hashes(directory)
                if current.get("evidence_sha256") != hashes:
                    raise LauncherError("Completed occurrence evidence differs: " + str(directory))
                return current, True
            resume = True
            if current.get("source_version") != manifest["active_source_version"]:
                raise LauncherError("Changed sources cannot resume a partial occurrence; use --rerun-failed")
        else:
            raise LauncherError("Existing occurrence is preserved; use --resume or --rerun-failed")
    else:
        if args.resume and attempts and attempts[-1].get("status") != "allocated":
            raise LauncherError("Manifested occurrence directory is missing")
        current = attempts[-1] if attempts and attempts[-1].get("status") == "allocated" else _attempt(
            record, condition, candidate_id, directory, run_root,
            manifest["active_source_version"],
            occurrence_scope=(
                f"{args.phase}-occurrence-{args.occurrence:03d}"
                if args.amendment_a2 else None))
    current.update(status="running", updated_utc=utc_now())
    manifest["updated_utc"] = utc_now()
    write_json(manifest_path, manifest)
    command = child_argv(repo, study, candidate_id, condition, directory, args.mode,
                         env_file=args.env_file, tokenizer_pins=args.tokenizer_pins,
                         capability=args.capability, resume=resume, cycles=cycles,
                         recipe_id=A2_RECIPE_IDS.get(condition) if args.amendment_a2 else None)
    completed = subprocess.run(command, cwd=repo, env=_child_environment(repo),
                               capture_output=True, text=True, encoding="utf-8",
                               errors="strict", check=False)
    invocation = len(current.setdefault("launcher_invocations", [])) + 1
    log_root = directory.parent.parent / "_launcher-logs"
    stem = f"{candidate_id}-{condition}-a{current['attempt_number']:03d}-i{invocation:03d}"
    stdout_path, stderr_path = log_root / (stem + ".stdout.txt"), log_root / (stem + ".stderr.txt")
    write_text_once(stdout_path, completed.stdout)
    write_text_once(stderr_path, completed.stderr)
    current["launcher_invocations"].append({
        "invocation": invocation,
        "stdout_path": stdout_path.relative_to(run_root).as_posix(),
        "stdout_sha256": sha256(stdout_path),
        "stderr_path": stderr_path.relative_to(run_root).as_posix(),
        "stderr_sha256": sha256(stderr_path),
        "returncode": completed.returncode,
    })
    state_path = directory / "state.json"
    if not state_path.is_file():
        current.update(status="launch-refused", stop_reason="launch-refused",
                       returncode=completed.returncode, updated_utc=utc_now(),
                       stdout_sha256=sha256(stdout_path), stderr_sha256=sha256(stderr_path))
        write_json(manifest_path, manifest)
        raise LauncherError("Reason child refused before durable state: " + candidate_id + " " + condition)
    state = read_json(state_path)
    config = read_json(directory / "config.json")
    stop = state.get("stop_reason", "unknown") if isinstance(state, dict) else "unknown"
    good = _good_stop(condition, stop)
    current.update(status="complete" if good else "failed", stop_reason=stop,
                   run_id=config.get("run_id"), returncode=completed.returncode,
                   logical_calls=state.get("calls"), attempts_made=state.get("attempts"),
                   completion_token_ceiling=config.get("completion_tokens"),
                   endpoint="deepseek-flash" if condition in {"CAL-NATIVE", "NATIVE"} else None,
                   thinking="native" if condition in {"CAL-NATIVE", "NATIVE"} else None,
                   reasoning_effort="medium" if condition in {"CAL-NATIVE", "NATIVE"} else None,
                   wall_seconds=300,
                   evidence_sha256=tree_hashes(directory), updated_utc=utc_now(),
                   stdout_sha256=sha256(stdout_path), stderr_sha256=sha256(stderr_path))
    manifest["updated_utc"] = utc_now()
    write_json(manifest_path, manifest)
    return current, good


def _phase_receipt(run_root: Path, phase_root: Path, manifest: dict[str, Any], phase_key: str,
                   args: argparse.Namespace, admitted: list[str] | None,
                   optional: tuple[str, ...]) -> None:
    phase = manifest["phases"][phase_key]
    records = []
    for candidate_id, candidate in phase.get("candidates", {}).items():
        for condition, record in candidate.get("conditions", {}).items():
            if not record.get("attempts"):
                failure = record.get("dependency_failure")
                if failure:
                    records.append({"candidate_id": candidate_id, "condition": condition,
                                    "status": "dependency-failure", **failure})
                continue
            active = record["attempts"][-1]
            item = {"candidate_id": candidate_id, "condition": condition,
                            "occurrence_id": active["occurrence_id"],
                            "directory": active["directory"], "stop_reason": active["stop_reason"],
                            "status": active["status"], "source_version": active["source_version"],
                            "launcher_invocations": active.get("launcher_invocations", [])}
            if condition == "CAL-NATIVE":
                item.update({"logical_calls": active.get("logical_calls"),
                             "attempts": active.get("attempts_made"),
                             "completion_token_ceiling": active.get("completion_token_ceiling"),
                             "endpoint": active.get("endpoint"), "thinking": active.get("thinking"),
                             "reasoning_effort": active.get("reasoning_effort"),
                             "wall_seconds": active.get("wall_seconds"),
                             "baseline_run_id": active.get("run_id")})
            records.append(item)
    condition_order = {name: index for index, name in enumerate(
        ("CAL-NATIVE", *DEFAULT_CONDITIONS, *OPTIONAL_CONDITIONS))}
    records.sort(key=lambda item: (item["candidate_id"], condition_order.get(item["condition"], 999)))
    if args.amendment_a2:
        expected_projection = a2_budget(len(admitted or []))
        if (phase.get("resource_projection") != expected_projection
                or phase.get("selected_conditions") != list(A2_CONDITIONS)
                or phase.get("amendment") != "A2"):
            raise LauncherError("Saved A2 phase identity or resource projection differs")
        receipt_budget = expected_projection
    else:
        receipt_budget = None if admitted is None else budget(
            len(admitted),
            sum(candidate_record(_study_root(), item)["checker_eligible"] for item in admitted),
            len(admitted) * len(optional),
        )
    receipt = {
        "schema": SCHEMA,
        "phase": args.phase,
        "mode": args.mode,
        "occurrence": args.occurrence,
        "created_utc": phase["created_utc"],
        "selected_candidates": phase["selected_candidates"],
        "admitted": admitted,
        "optional_conditions": list(optional),
        "records": records,
        "scientific_evidence": args.mode == "live",
        "pilot_output_allowed_in_main_prompts": False,
        "budget": receipt_budget,
    }
    if args.amendment_a2:
        receipt.update({
            "amendment": "A2",
            "amendment_a2": True,
            "selected_conditions": list(A2_CONDITIONS),
        })
    base = phase_root / "phase-receipt.json"
    receipt_paths = phase.setdefault("phase_receipts", [])
    if not base.exists():
        write_json(base, receipt, replace=False)
        receipt_paths.append({"path": base.relative_to(run_root).as_posix(),
                              "sha256": sha256(base), "kind": "base"})
        return
    def comparable(value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        return {key: item for key, item in value.items()
                if key not in {"receipt_kind", "supplements"}}
    if comparable(read_json(base)) == receipt:
        if not receipt_paths:
            receipt_paths.append({"path": base.relative_to(run_root).as_posix(),
                                  "sha256": sha256(base), "kind": "base"})
        return
    supplements = sorted(phase_root.glob("phase-receipt-rerun-*.json"))
    if supplements and comparable(read_json(supplements[-1])) == receipt:
        return
    number = len(supplements) + 1
    supplement = phase_root / f"phase-receipt-rerun-{number:03d}.json"
    receipt["receipt_kind"] = "rerun-supplement"
    receipt["supplements"] = (supplements[-1] if supplements else base).name
    write_json(supplement, receipt, replace=False)
    receipt_paths.append({"path": supplement.relative_to(run_root).as_posix(),
                          "sha256": sha256(supplement), "kind": "rerun-supplement"})


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _study_root() -> Path:
    return _repo_root() / "experiments" / "diagnostics" / "R002-episodes-under-calibrated-difficulty"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("calibration", "main"), required=True)
    parser.add_argument("--mode", choices=("offline", "live"), default="offline")
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--occurrence", type=int, default=1)
    parser.add_argument("--problems", nargs="+", metavar="CNN")
    parser.add_argument("--admission-receipt", type=Path)
    parser.add_argument("--optional-receipt", type=Path, action="append", default=[])
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--rerun-failed", action="store_true")
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--tokenizer-pins", type=Path)
    parser.add_argument("--capability", type=Path)
    parser.add_argument(
        "--amendment-a2", action="store_true",
        help="Run the post-dispatch A2 occurrence-002 decomposed-only schedule")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo, study = _repo_root(), _study_root()
    for name in ("admission_receipt", "env_file", "tokenizer_pins", "capability"):
        value = getattr(args, name)
        if value is not None:
            setattr(args, name, (repo / value).resolve() if not value.is_absolute() else value.resolve())
    args.optional_receipt = [
        (repo / value).resolve() if not value.is_absolute() else value.resolve()
        for value in args.optional_receipt
    ]
    material_pins_sha256 = validate_material_pins(study)
    if args.occurrence < 1 or (args.resume and args.rerun_failed):
        raise LauncherError("Occurrence must be positive and resume/rerun-failed are exclusive")
    if args.amendment_a2:
        if args.phase != "main" or args.occurrence != 2:
            raise LauncherError("A2 is restricted to main occurrence-002")
        if args.optional_receipt:
            raise LauncherError("A2 occurrence-002 does not select optional arms")
        if args.rerun_failed:
            raise LauncherError("A2 occurrence-002 cannot rerun a failed occurrence")
    if args.mode == "live" and args.env_file is None:
        raise LauncherError("Live mode requires --env-file")
    if args.mode == "live" and args.capability is None:
        raise LauncherError("Live mode requires reviewed --capability")
    if args.mode == "live" and args.phase == "main" and args.tokenizer_pins is None:
        raise LauncherError("Live main requires reviewed --tokenizer-pins")
    selected = normalize_problem_ids(args.problems or list(PROBLEM_IDS))
    if args.phase == "calibration" and args.mode == "live" and selected != list(PROBLEM_IDS):
        raise LauncherError("Live calibration must run all 24 candidates exactly once")
    if args.phase == "calibration" and args.admission_receipt is not None:
        raise LauncherError("Calibration does not consume an admission receipt")
    run_root = validate_run_root(repo, args.run_root)
    run_root.mkdir(parents=True, exist_ok=True)
    manifest_path = run_root / "manifest.json"
    manifest = _load_manifest(manifest_path, repo, study, args.mode)
    phase_key = f"{args.phase}-occurrence-{args.occurrence:03d}"
    if args.phase == "calibration" and args.mode == "live":
        other_calibrations = [key for key in manifest["phases"]
                              if key.startswith("calibration-occurrence-") and key != phase_key]
        if other_calibrations:
            raise LauncherError("Live calibration is once-only; another calibration occurrence already exists")
    phase_root = run_root / phase_key
    if args.phase == "calibration" and args.mode == "live" and args.tokenizer_pins is None:
        generated_pins = phase_root / "calibration-input-bound.json"
        descriptor = calibration_wire_bound(study)
        if generated_pins.exists():
            if read_json(generated_pins) != descriptor:
                raise LauncherError("Saved calibration input-bound descriptor differs")
        else:
            write_json(generated_pins, descriptor, replace=False)
        args.tokenizer_pins = generated_pins.resolve()
    admitted: list[str] | None = None
    optional: tuple[str, ...] = ()
    if args.phase == "main":
        if args.admission_receipt is None:
            raise LauncherError("Main phase requires --admission-receipt")
        admitted, _receipt = validate_admission_receipt(args.admission_receipt.resolve(), study,
                                                         offline=args.mode == "offline")
        optional = validate_optional_receipts(args.optional_receipt, admitted)
        if args.amendment_a2 and tuple(admitted) != A2_ADMITTED:
            raise LauncherError(
                "A2 occurrence-002 requires admitted set C05 C06 C09 C12 exactly")
        if args.problems is not None and selected != admitted:
            raise LauncherError("Main --problems must equal the frozen admitted set")
        selected = admitted
    elif args.optional_receipt:
        raise LauncherError("Optional receipts belong only to main")
    saved_phase = manifest["phases"].get(phase_key)
    context = {"phase": args.phase, "mode": args.mode, "occurrence": args.occurrence,
               "selected_candidates": selected, "optional_conditions": list(optional),
               "admission_sha256": sha256(args.admission_receipt.resolve()) if args.admission_receipt else None,
               "optional_receipt_sha256": [sha256(path.resolve()) for path in args.optional_receipt],
               "tokenizer_pins_sha256": sha256(args.tokenizer_pins.resolve()) if args.tokenizer_pins else None,
               "capability_sha256": sha256(args.capability.resolve()) if args.capability else None,
               "material_pins_sha256": material_pins_sha256,
               "env_file_forwarded_path": str(args.env_file) if args.env_file else None,
               "env_file_read_by_launcher": False}
    if args.amendment_a2:
        context.update({
            "amendment": "A2",
            "selected_conditions": list(A2_CONDITIONS),
            "resource_projection": a2_budget(len(selected)),
        })
    if saved_phase is None:
        saved_phase = {**context, "created_utc": utc_now(), "candidates": {}}
        manifest["phases"][phase_key] = saved_phase
    elif any(saved_phase.get(key) != value for key, value in context.items()):
        raise LauncherError("Saved phase context differs; allocate a new occurrence")
    write_json(manifest_path, manifest)
    if args.phase == "main" and not selected:
        phase_root.mkdir(parents=True, exist_ok=True)
        _phase_receipt(run_root, phase_root, manifest, phase_key, args, admitted, optional)
        manifest["updated_utc"] = utc_now()
        write_json(manifest_path, manifest)
        print(json.dumps({"phase": "main", "status": "STOP_ZERO_ADMITTED", "calls": 0}, sort_keys=True))
        return 0
    overall_good = True
    for candidate_id in selected:
        candidate = candidate_record(study, candidate_id)
        if args.amendment_a2:
            conditions = list(A2_CONDITIONS)
        else:
            conditions = ["CAL-NATIVE"] if args.phase == "calibration" else list(DEFAULT_CONDITIONS)
        if not candidate["checker_eligible"] and "LOOP-CHECKER" in conditions:
            conditions.remove("LOOP-CHECKER")
        conditions += list(optional)
        for condition in conditions:
            directory = phase_root / candidate_id / condition
            cycles = 3
            if condition == "NATIVE-MATCH":
                tested_state_path = phase_root / candidate_id / "LOOP-TESTED" / "state.json"
                tested_state = read_json(tested_state_path) if tested_state_path.is_file() else {}
                completed = tested_state.get("completed_cycles") if isinstance(tested_state, dict) else None
                if type(completed) is not int or not 0 <= completed <= 3:
                    raise LauncherError("NATIVE-MATCH cannot establish the TESTED cycle count")
                if completed == 0:
                    condition_record = saved_phase.setdefault("candidates", {}).setdefault(
                        candidate_id, {}).setdefault("conditions", {}).setdefault(condition, {"attempts": []})
                    condition_record.setdefault("dependency_failure", {
                        "reason": "LOOP-TESTED completed zero cycles; no zero-cycle R002 occurrence is valid",
                        "tested_state_sha256": sha256(tested_state_path),
                        "recorded_utc": utc_now(),
                    })
                    manifest["updated_utc"] = utc_now()
                    write_json(manifest_path, manifest)
                    overall_good = False
                    continue
                cycles = completed
            _record, good = _run_occurrence(repo, study, run_root, manifest_path, manifest,
                                             saved_phase, candidate_id, condition, directory, args,
                                             cycles=cycles)
            overall_good = overall_good and good
    _phase_receipt(run_root, phase_root, manifest, phase_key, args, admitted, optional)
    manifest["updated_utc"] = utc_now()
    write_json(manifest_path, manifest)
    print(json.dumps({"schema": SCHEMA, "phase": args.phase, "mode": args.mode,
                      "status": "COMPLETE" if overall_good else "COMPLETED_WITH_FAILURES",
                      "selected_candidates": selected, "scientific_evidence": args.mode == "live"},
                     ensure_ascii=False, sort_keys=True))
    return 0 if overall_good else 2
