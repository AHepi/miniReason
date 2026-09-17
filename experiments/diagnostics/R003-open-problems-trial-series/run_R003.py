#!/usr/bin/env python3
"""Durable R003 occurrence launcher.

Freeze a numbered problem/condition matrix, delegate each cell to the strict
reason.py R003 profile, and record source, input, argv, and output hashes.
Plan mode is the default. Live mode additionally needs explicit dispatch
authorization, byte-verified sealed briefs, and reviewed qualification files.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Iterable


STUDY = Path(__file__).resolve().parent
ROOT = STUDY.parents[2]
PYTHON = Path(r"C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe")
DEFAULT_SERIES = ROOT / "runs" / "R003-open-v1"
PROFILE = "r003-open-v1"
MANIFEST_SCHEMA = "minireason.r003.matrix.v2"
SOURCE_SCHEMA = "minireason.r003.source-pins.v1"
SEAL_SCHEMA = "minireason.r003.brief-seal.v1"
CANONICAL_SCHEMA = "minireason.reason.r003-canonical-registry.v1"
CONDITIONS = ("NATIVE", "LOOP-CROSS", "LOOP-DECOMPOSED")
ALIASES = dict(zip(CONDITIONS, ("n", "x", "d")))
RECIPES = {
    "LOOP-CROSS": "r003-cross-v1.json",
    "LOOP-DECOMPOSED": "r003-decomposed-v1.json",
}
R3_A1_RECIPES = {key: value.replace("-v1.json", "-v2.json") for key, value in RECIPES.items()}
R3_A2_RECIPES = {key: value.replace("-v1.json", "-v3.json") for key, value in RECIPES.items()}
AMENDMENT_RECIPES = {"R3-A1": R3_A1_RECIPES, "R3-A2": R3_A2_RECIPES}
DEFAULT_PREFLIGHT = STUDY / "R003-input-preflight.json"
R3_A1_CONDITIONS = ("LOOP-CROSS", "LOOP-DECOMPOSED")
R3_A2_CONDITIONS = R3_A1_CONDITIONS
PROSE_AMENDMENTS = frozenset(AMENDMENT_RECIPES)

PROVIDER_KEY_NAMES = frozenset({"DEEPSEEK_API_KEY", "OLLAMA_API_KEY", "API_KEY",
                                "OPENAI_ACCESS_TOKEN"})
PARTICIPANT_LINEAGES = ("deepseek", "qwen", "glm")
R3_A1_PARTICIPANT_LINEAGES = ("deepseek", "qwen", "kimi")
MAX_DURABLE_PATH = 200
LONGEST_CHILD_SUFFIX = Path(
    "calls/c0003-decomposed-closing-return/a01/provider/call-0001.response.json"
)


class Refused(RuntimeError):
    """A fail-closed launcher refusal."""


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def value_digest(value: Any) -> str:
    return hashlib.sha256(_json_bytes(value)).hexdigest()


def read_json(path: Path) -> Any:
    try:
        with Path(path).open("r", encoding="utf-8", newline="") as handle:
            return json.load(handle)
    except (OSError, UnicodeError, ValueError) as error:
        raise Refused("JSON_INPUT_INVALID") from error


def _within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def allowed_write(path: Path) -> Path:
    resolved = Path(path).resolve()
    roots = (ROOT / "runs", ROOT / "work" / "w28", ROOT / "work" / "review28",
             Path(r"C:\tw28"), Path(r"C:\tr28"), Path(r"C:\tw30"), ROOT / "work" / "w30",
             Path(r"C:\tr30"), ROOT / "work" / "review30", Path(r"C:\tw32"), ROOT / "work" / "w32",
             Path(r"C:\tr32"), ROOT / "work" / "review32")
    if not any(resolved != root.resolve() and _within(resolved, root) for root in roots):
        raise Refused("WRITE_OUTSIDE_AUTHORIZED_SCOPE")
    return resolved


def put(path: Path, value: Any) -> None:
    target = allowed_write(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with target.open("x", encoding="utf-8", newline="") as handle:
            handle.write(_json_bytes(value).decode("utf-8"))
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as error:
        raise Refused("WRITE_ONCE_PATH_EXISTS") from error


def put_text(path: Path, value: str) -> None:
    target = allowed_write(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with target.open("x", encoding="utf-8", newline="") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as error:
        raise Refused("WRITE_ONCE_PATH_EXISTS") from error


def copy_bytes(source: Path, target: Path) -> None:
    raw = Path(source).read_bytes()
    destination = allowed_write(target)
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as error:
        raise Refused("WRITE_ONCE_PATH_EXISTS") from error
    if hashlib.sha256(raw).hexdigest() != digest(destination):
        raise Refused("COPY_HASH_MISMATCH")


@contextmanager
def lock(directory: Path):
    root = allowed_write(directory)
    root.mkdir(parents=True, exist_ok=True)
    marker = root / ".r003-launcher-lock"
    try:
        with marker.open("x", encoding="utf-8", newline="") as handle:
            handle.write(utc())
    except FileExistsError as error:
        raise Refused("LAUNCHER_BUSY_OR_STALE_LOCK") from error
    try:
        yield
    finally:
        marker.unlink()


def hash_tree(path: Path) -> dict[str, str]:
    root = Path(path)
    if not root.exists():
        return {}
    return {
        item.relative_to(root).as_posix(): digest(item)
        for item in sorted(root.rglob("*"))
        if item.is_file()
    }


def source_pins() -> dict[str, Any]:
    paths = [Path(__file__), ROOT / "tools" / "reason.py"]
    reason = ROOT / "src" / "minireason" / "reason"
    paths.extend(item for item in reason.rglob("*")
                 if item.is_file() and item.suffix in {".py", ".json"})
    paths.extend(item for item in (ROOT / "src" / "minireason").glob("provider*.py")
                 if item.is_file())
    paths.append(ROOT / "src" / "minireason" / "data" / "endpoints.json")
    for directory in (
        ROOT / "experiments" / "diagnostics" / "R002-episodes-under-calibrated-difficulty" / "contracts",
        STUDY / "contracts",
        STUDY / "recipes",
    ):
        if directory.is_dir():
            paths.extend(item for item in directory.rglob("*.json") if item.is_file())
    return {
        "schema": SOURCE_SCHEMA,
        "version": 1,
        "study_profile": PROFILE,
        "files": {
            item.relative_to(ROOT).as_posix(): digest(item)
            for item in sorted(set(paths))
        },
    }


def normalize_problem_ids(values: Iterable[str]) -> list[str]:
    normalized: list[str] = []
    for value in values:
        problem_id = value.upper()
        if not re.fullmatch(r"O0[1-8]", problem_id):
            raise Refused("INVALID_PROBLEM_ID")
        if problem_id in normalized:
            raise Refused("DUPLICATE_PROBLEM_ID")
        normalized.append(problem_id)
    if not normalized:
        raise Refused("EMPTY_PROBLEM_SELECTION")
    if normalized != sorted(normalized):
        raise Refused("PROBLEMS_MUST_REMAIN_ASCENDING")
    return normalized


def normalize_conditions(values: Iterable[str]) -> list[str]:
    result = list(values)
    if not result or any(value not in CONDITIONS for value in result):
        raise Refused("UNSUPPORTED_CONDITION")
    if len(set(result)) != len(result):
        raise Refused("DUPLICATE_CONDITION")
    if result != [value for value in CONDITIONS if value in result]:
        raise Refused("CONDITIONS_MUST_REMAIN_DECLARED_ORDER")
    return result


def _selected_registry(name: str, problem_ids: list[str]) -> dict[str, Any]:
    value = read_json(STUDY / "public" / name)
    candidates = value.get("candidates") if isinstance(value, dict) else None
    if not isinstance(candidates, list):
        raise Refused("PUBLIC_REGISTRY_INVALID")
    by_id = {
        row.get("candidate_id"): row
        for row in candidates
        if isinstance(row, dict) and isinstance(row.get("candidate_id"), str)
    }
    if len(by_id) != len(candidates):
        raise Refused("PUBLIC_REGISTRY_DUPLICATE_ID")
    if any(problem_id not in by_id for problem_id in problem_ids):
        raise Refused("PUBLIC_REGISTRY_INCOMPLETE")
    selected = {key: value[key] for key in value if key != "candidates"}
    selected["candidates"] = [by_id[problem_id] for problem_id in problem_ids]
    return selected


def _write_inputs(directory: Path, problem_ids: list[str], *, capability: Path | None,
                  tokenizer_pins: Path | None, amendment: str | None = None) -> None:
    canonical: list[dict[str, str]] = []
    for problem_id in problem_ids:
        source = STUDY / "problems" / f"{problem_id}.txt"
        if not source.is_file() or not source.read_bytes().strip():
            raise Refused("PROBLEM_MISSING_OR_EMPTY")
        destination = directory / "p" / f"{problem_id}.txt"
        copy_bytes(source, destination)
        canonical.append({
            "candidate_id": problem_id,
            "canonical_problem": f"p/{problem_id}.txt",
            "problem_sha256": digest(destination),
        })
    put(directory / "inputs" / "RELATIONS.json", _selected_registry("RELATIONS.json", problem_ids))
    put(directory / "inputs" / "FORKS.json", _selected_registry("FORKS.json", problem_ids))
    put(directory / "CANONICAL.json", {
        "schema_version": CANONICAL_SCHEMA,
        "study_profile": PROFILE,
        "candidates": canonical,
    })
    recipes = AMENDMENT_RECIPES.get(amendment, RECIPES)
    for name in sorted(set(recipes.values())):
        source = STUDY / "recipes" / name
        if not source.is_file():
            raise Refused("R003_RECIPE_NOT_INSTALLED")
        copy_bytes(source, directory / "inputs" / name)
    if capability is not None:
        copy_bytes(Path(capability), directory / "inputs" / "capability.json")
    if tokenizer_pins is not None:
        copy_bytes(Path(tokenizer_pins), directory / "inputs" / "tokenizer-pins.json")


def _resolve_seal_path(manifest: Path, value: Any, *, kind: str) -> Path:
    if not isinstance(value, str) or not value:
        raise Refused("SEALED_BRIEF_RECORD_INVALID")
    path = (manifest.parent / value).resolve()
    if kind == "brief":
        if not _within(path, manifest.parent) or path.is_symlink():
            raise Refused("SEALED_BRIEF_PATH_ESCAPE")
    elif not _within(path, STUDY):
        raise Refused("SEALED_PROBLEM_PATH_ESCAPE")
    if not path.is_file():
        raise Refused("SEALED_FILE_MISSING")
    return path


def _nonempty_metadata(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    return isinstance(value, (list, dict)) and bool(value)


def _seal_records(value: Any, manifest: Path) -> tuple[list, dict | None]:
    """Adapt the custodian's existing metadata without changing the sealed files."""
    if not isinstance(value, dict) or value.get("status") != "SEALED":
        raise Refused("SEALED_BRIEF_MANIFEST_INVALID")
    if value.get("schema") == SEAL_SCHEMA:
        rows = value.get("records", value.get("briefs"))
        if not isinstance(rows, list):
            raise Refused("SEALED_BRIEF_MANIFEST_INVALID")
        return rows, None
    if value.get("schema") != "minireason.r003.sealed-reader-briefs.v1":
        raise Refused("SEALED_BRIEF_MANIFEST_INVALID")
    if value.get("path_base") != STUDY.relative_to(ROOT).as_posix():
        raise Refused("SEALED_BRIEF_PATH_BASE_INVALID")
    author, original = value.get("author"), value.get("briefs")
    if not isinstance(author, dict) or not isinstance(original, list):
        raise Refused("SEALED_BRIEF_METADATA_MISSING")
    ids = [row.get("problem_id") for row in original if isinstance(row, dict)]
    if len(ids) != len(original) or value.get("selected_problem_ids") != ids:
        raise Refused("SEALED_BRIEF_SELECTION_MISMATCH")
    rows = []
    for row in original:
        pid = row["problem_id"]
        if (not isinstance(pid, str) or not re.fullmatch(r"O0[1-8]", pid)
                or row.get("problem_path") != f"problems/{pid}.txt"
                or row.get("brief_path") != f"briefs/{pid}.md"):
            raise Refused("SEALED_BRIEF_PATH_ESCAPE")
        rows.append({**row, "author": author,
                     **{key: author.get(key) for key in ("provider", "model", "lineage")},
                     "exposure": value.get("exposure"), "sealed_utc": value.get("sealed_utc"),
                     "problem_path": os.path.relpath(STUDY / row["problem_path"], manifest.parent),
                     "brief_path": os.path.relpath(STUDY / row["brief_path"], manifest.parent)})
    return rows, {key: item for key, item in value.items() if key != "briefs"}


def validate_sealed_briefs(manifest_path: Path, problem_ids: list[str],
                           amendment: str | None = None) -> dict[str, Any]:
    """Verify exact problem/brief bytes without decoding or returning brief content."""
    participant_lineages = (R3_A1_PARTICIPANT_LINEAGES
                            if amendment in PROSE_AMENDMENTS else PARTICIPANT_LINEAGES)
    manifest = Path(manifest_path).resolve()
    value = read_json(manifest)
    rows, custodian_metadata = _seal_records(value, manifest)
    by_id: dict[str, dict[str, Any]] = {}
    seen: set[str] = set()
    summary: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            raise Refused("SEALED_BRIEF_RECORD_INVALID")
        problem_id = row.get("problem_id", row.get("candidate_id"))
        if (not isinstance(problem_id, str) or not re.fullmatch(r"O0[1-8]", problem_id)
                or problem_id in seen):
            raise Refused("SEALED_BRIEF_RECORD_INVALID")
        seen.add(problem_id)
        for field in ("author", "provider", "model", "lineage", "exposure"):
            if not _nonempty_metadata(row.get(field)):
                raise Refused("SEALED_BRIEF_METADATA_MISSING")
        timestamp = row.get("sealed_utc", row.get("utc"))
        try:
            parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except (AttributeError, ValueError):
            raise Refused("SEALED_BRIEF_UTC_INVALID") from None
        if parsed.tzinfo is None:
            raise Refused("SEALED_BRIEF_UTC_INVALID")
        if parsed.astimezone(timezone.utc) > datetime.now(timezone.utc):
            raise Refused("SEALED_BRIEF_UTC_FUTURE")
        identity = " ".join(str(row[field]) for field in ("provider", "model", "lineage")).lower()
        if any(name in identity for name in participant_lineages):
            raise Refused("SEALED_BRIEF_LINEAGE_NOT_INDEPENDENT")
        problem_path = _resolve_seal_path(manifest, row.get("problem_path"), kind="problem")
        brief_path = _resolve_seal_path(manifest, row.get("brief_path"), kind="brief")
        problem_hash = row.get("problem_sha256")
        brief_hash = row.get("brief_sha256")
        if problem_hash != digest(problem_path) or brief_hash != digest(brief_path):
            raise Refused("SEALED_BRIEF_HASH_MISMATCH")
        if problem_id not in problem_ids:
            continue
        expected_problem = (STUDY / "problems" / f"{problem_id}.txt").resolve()
        if problem_path != expected_problem:
            raise Refused("SEALED_PROBLEM_PATH_MISMATCH")
        by_id[problem_id] = row
        summary.append({
            "problem_id": problem_id,
            "problem_sha256": problem_hash,
            "brief_sha256": brief_hash,
            "author": row["author"], "provider": row["provider"], "model": row["model"],
            "lineage": row["lineage"], "exposure": row["exposure"], "sealed_utc": timestamp,
        })
    if list(by_id) != problem_ids:
        raise Refused("SEALED_BRIEF_SELECTION_MISMATCH")
    return {
        "schema": SEAL_SCHEMA,
        "manifest_path": str(manifest),
        "manifest_sha256": digest(manifest),
        "records": summary,
        **({"custodian_metadata": custodian_metadata} if custodian_metadata is not None else {}),
    }


def _child_file(directory: Path, name: str) -> Path | None:
    path = directory / "inputs" / name
    return path if path.is_file() else None


def argv_for(directory: Path, problem_id: str, condition: str, mode: str,
             *, env_file: str | None) -> list[str]:
    command = [
        str(PYTHON), "-B", "-X", "utf8", str(ROOT / "tools" / "reason.py"),
        "run-r002-native" if condition == "NATIVE" else "run-r002",
        "--study-profile", PROFILE,
        "--problem", str(directory / "p" / f"{problem_id}.txt"),
        "--out", str(directory / "r" / problem_id / ALIASES[condition]),
        "--mode", mode, "--relations", str(directory / "inputs" / "RELATIONS.json"),
        "--canonical-registry", str(directory / "CANONICAL.json"),
        "--attempt-policy", "strict", "--prompt-token-cap", "32768",
        "--retry-transport", "0",
    ]
    amendment_file = _child_file(directory, "amendment.json")
    amendment = read_json(amendment_file)["amendment"] if amendment_file else None
    recipes = AMENDMENT_RECIPES.get(amendment, RECIPES)
    tokenizers = _child_file(directory, "tokenizer-pins.json")
    capability = _child_file(directory, "capability.json")
    if tokenizers is not None:
        command += ["--tokenizer-pins", str(tokenizers)]
    if capability is not None:
        command += ["--capability", str(capability)]
    if env_file is not None:
        command += ["--env-file", env_file]
    if condition == "NATIVE":
        command += ["--condition", "NATIVE", "--thinking", "native",
                    "--reasoning-effort", "medium", "--completion-tokens", "32768"]
    else:
        command += ["--cycles", "3", "--recipe", str(directory / "inputs" / recipes[condition]),
                    "--fork-registry", str(directory / "inputs" / "FORKS.json")]
    return command


def _path_budget(rows: list[dict[str, Any]], directory: Path) -> dict[str, int]:
    longest = max(len(str((directory / row["output"] / LONGEST_CHILD_SUFFIX).resolve())) for row in rows)
    if longest >= MAX_DURABLE_PATH:
        raise Refused("DURABLE_PATH_BOUND_EXCEEDED")
    return {"strictly_less_than": MAX_DURABLE_PATH, "maximum_projected_absolute": longest}


def create(series: Path, problems: Iterable[str], conditions: Iterable[str], question: str,
           mode: str, *, env_file: Path | str | None = None,
           tokenizer_pins: Path | None = None, capability: Path | None = None,
           brief_manifest: Path | None = None, authorize_live: bool = False,
           parent: Path | None = None, reason: str | None = None,
           cells: list[tuple[str, str]] | None = None,
           amendment: str | None = None, expected_occurrence: str | None = None) -> Path:
    if amendment not in {None, *PROSE_AMENDMENTS}:
        raise Refused("UNSUPPORTED_AMENDMENT")
    if expected_occurrence is not None and not re.fullmatch(r"o[0-9]{3,}", expected_occurrence):
        raise Refused("INVALID_EXPECTED_OCCURRENCE")
    if amendment in PROSE_AMENDMENTS and tokenizer_pins is None:
        tokenizer_pins = DEFAULT_PREFLIGHT
    if (amendment in PROSE_AMENDMENTS
            and read_json(Path(tokenizer_pins)).get("amendment") != "R3-A1"):
        if amendment == "R3-A1":
            raise Refused("R3_A1_INPUT_DESCRIPTOR_REQUIRED")
        raise Refused("R3_A2_INHERITED_INPUT_DESCRIPTOR_REQUIRED")
    if mode not in {"plan", "offline", "live"}:
        raise Refused("INVALID_MODE")
    if not question.strip() or "\n" in question or "\r" in question:
        raise Refused("ONE_LINE_OCCURRENCE_QUESTION_REQUIRED")
    problem_ids = normalize_problem_ids(problems)
    condition_ids = normalize_conditions(conditions)
    if amendment in PROSE_AMENDMENTS and any(c not in R3_A1_CONDITIONS for c in condition_ids):
        raise Refused(amendment.replace("-", "_") + "_REUSES_NATIVE_FROM_O001")
    if mode == "live":
        if not authorize_live:
            raise Refused("LIVE_DISPATCH_AUTHORIZATION_REQUIRED")
        if env_file is None:
            raise Refused("LIVE_ENV_FILE_REQUIRED")
        if tokenizer_pins is None or capability is None:
            raise Refused("LIVE_QUALIFICATION_FILES_REQUIRED")
        if brief_manifest is None:
            raise Refused("LIVE_SEALED_BRIEF_MANIFEST_REQUIRED")
        try:
            from minireason.reason.r002_preflight import validate_r003_launch_inputs
        except (ImportError, AttributeError) as error:
            raise Refused("R003_QUALIFICATION_VALIDATOR_UNAVAILABLE") from error
        for condition in condition_ids:
            try:
                validate_r003_launch_inputs(Path(capability), Path(tokenizer_pins), condition)
            except Exception as error:
                raise Refused("R003_QUALIFICATION_INVALID") from error
    for problem_id in problem_ids:
        source = STUDY / "problems" / f"{problem_id}.txt"
        if not source.is_file() or not source.read_bytes().strip():
            raise Refused("PROBLEM_MISSING_OR_EMPTY")
    for name in set(AMENDMENT_RECIPES.get(amendment, RECIPES).values()):
        if not (STUDY / "recipes" / name).is_file():
            raise Refused("R003_RECIPE_NOT_INSTALLED")
    seal = validate_sealed_briefs(Path(brief_manifest), problem_ids, amendment) if brief_manifest else None
    selected = cells or [(problem_id, condition) for problem_id in problem_ids for condition in condition_ids]
    if any(problem_id not in problem_ids or condition not in condition_ids for problem_id, condition in selected):
        raise Refused("CELL_OUTSIDE_MATRIX")
    series = allowed_write(series)
    with lock(series):
        numbers = [int(item.name[1:]) for item in series.iterdir()
                   if item.is_dir() and re.fullmatch(r"o\d{3,}", item.name)]
        directory = series / f"o{max(numbers, default=0) + 1:03d}"
        if expected_occurrence is not None and directory.name != expected_occurrence:
            raise Refused("OCCURRENCE_NUMBER_CHANGED")
        directory.mkdir()
        if amendment is not None:
            amendment_record = {"amendment": amendment,
                "native_reuse": "Reader reuses o001 NATIVE answers; no new NATIVE dispatch"}
            if amendment == "R3-A2":
                amendment_record["resource_inheritance"] = (
                    "Exact R3-A1 input descriptor, routes and allowances; only prose-seat contracts change"
                )
            put(directory / "inputs" / "amendment.json", amendment_record)
        put(directory / "QUESTION.json", {"utc": utc(), "question": question,
            "state": "declared_before_dispatch", "parent": str(parent) if parent else None,
            "reason": reason})
        _write_inputs(directory, problem_ids, capability=capability, tokenizer_pins=tokenizer_pins, amendment=amendment)
        child_mode = "live" if mode in {"live", "plan"} else "offline"
        env_literal = str(env_file) if env_file is not None else None
        rows = []
        for problem_id, condition in selected:
            argv = argv_for(directory, problem_id, condition, child_mode, env_file=env_literal)
            rows.append({"problem": problem_id, "condition": condition, "alias": ALIASES[condition],
                "output": f"r/{problem_id}/{ALIASES[condition]}", "argv": argv,
                "argv_sha256": value_digest(argv)})
        source = source_pins()
        manifest = {"schema": MANIFEST_SCHEMA, "study_profile": PROFILE,
            "occurrence": directory.name, "created_utc": utc(), "mode": mode,
            "amendment": amendment,
            "question": question, "matrix": rows,
            "order": "problem then condition; declared order; no random seed",
            "source_versions": [source], "active_source_version": source["version"],
            "input_sha256": {
                **{f"p/{name}": value for name, value in hash_tree(directory / "p").items()},
                **{f"inputs/{name}": value for name, value in hash_tree(directory / "inputs").items()},
                "CANONICAL.json": digest(directory / "CANONICAL.json")},
            "sealed_briefs": seal, "env_file_forwarded_path": env_literal,
            "env_file_read_by_launcher": False, "live_authorized": bool(authorize_live),
            "path_length": _path_budget(rows, directory),
            "parent": str(parent) if parent else None, "reason": reason}
        put(directory / "MANIFEST.json", manifest)
        put_text(directory / "MANIFEST.sha256", digest(directory / "MANIFEST.json") + "\n")
    return directory


def verify(directory: Path) -> dict[str, Any]:
    directory = allowed_write(directory)
    checksum_path = directory / "MANIFEST.sha256"
    try:
        with checksum_path.open("r", encoding="utf-8", newline="") as handle:
            checksum = handle.read()
    except (OSError, UnicodeError) as error:
        raise Refused("MANIFEST_CHECKSUM_MISSING") from error
    if checksum != digest(directory / "MANIFEST.json") + "\n":
        raise Refused("MANIFEST_CHECKSUM_MISMATCH")
    manifest = read_json(directory / "MANIFEST.json")
    if not isinstance(manifest, dict) or manifest.get("schema") != MANIFEST_SCHEMA:
        raise Refused("MANIFEST_SCHEMA")
    versions = manifest.get("source_versions")
    if not isinstance(versions, list) or len(versions) != 1:
        raise Refused("SOURCE_VERSION_INVALID")
    source = versions[0]
    if (not isinstance(source, dict) or source.get("schema") != SOURCE_SCHEMA
            or source.get("version") != manifest.get("active_source_version")):
        raise Refused("SOURCE_VERSION_INVALID")
    current_source = source_pins()
    if source != current_source or not isinstance(source.get("files"), dict) or not source["files"]:
        raise Refused("SOURCE_CHANGED")
    for relative, expected in source["files"].items():
        target = (ROOT / relative).resolve()
        if not _within(target, ROOT) or not target.is_file() or digest(target) != expected:
            raise Refused("SOURCE_CHANGED")
    for relative, expected in manifest.get("input_sha256", {}).items():
        target = (directory / relative).resolve()
        if not _within(target, directory) or not target.is_file() or digest(target) != expected:
            raise Refused("INPUT_CHANGED")
    child_mode = "live" if manifest["mode"] in {"live", "plan"} else "offline"
    for row in manifest.get("matrix", []):
        expected = argv_for(directory, row["problem"], row["condition"], child_mode,
                            env_file=manifest.get("env_file_forwarded_path"))
        if row.get("argv") != expected or row.get("argv_sha256") != value_digest(expected):
            raise Refused("COMMAND_CHANGED")
        output = f"r/{row['problem']}/{ALIASES[row['condition']]}"
        if row.get("output") != output:
            raise Refused("OUTPUT_CHANGED")
        result_path = directory / "results" / f"{row['problem']}-{row['alias']}.json"
        if result_path.exists():
            result = read_json(result_path)
            if result.get("evidence_sha256") != hash_tree(directory / output):
                raise Refused("SAVED_EVIDENCE_CHANGED")
            if result.get("argv_sha256") != row["argv_sha256"]:
                raise Refused("SAVED_ARGV_CHANGED")
    if manifest["mode"] == "live":
        if not manifest.get("live_authorized"):
            raise Refused("LIVE_DISPATCH_AUTHORIZATION_REQUIRED")
        seal = manifest.get("sealed_briefs")
        if not isinstance(seal, dict):
            raise Refused("LIVE_SEALED_BRIEF_MANIFEST_REQUIRED")
        selected = [row["problem_id"] for row in seal.get("records", [])]
        if validate_sealed_briefs(Path(seal["manifest_path"]), selected,
                                  manifest.get("amendment")) != seal:
            raise Refused("SEALED_BRIEF_MANIFEST_CHANGED")
    return manifest


def _validate_live_qualification(directory: Path, conditions: Iterable[str]) -> None:
    try:
        from minireason.reason.r002_preflight import validate_r003_launch_inputs
    except (ImportError, AttributeError) as error:
        raise Refused("R003_QUALIFICATION_VALIDATOR_UNAVAILABLE") from error
    capability = directory / "inputs" / "capability.json"
    tokenizers = directory / "inputs" / "tokenizer-pins.json"
    for condition in conditions:
        try:
            validate_r003_launch_inputs(capability, tokenizers, condition)
        except Exception as error:
            raise Refused("R003_QUALIFICATION_INVALID") from error


def _subprocess_environment() -> dict[str, str]:
    result: dict[str, str] = {}
    for name in os.environ.keys():
        if name in PROVIDER_KEY_NAMES or name.endswith("_API_KEY"):
            continue
        result[name] = os.environ[name]
    result.update({"PYTHONPATH": "src;tests", "PYTHONUTF8": "1",
        "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1",
        "TMP": os.environ.get("TMP", r"C:\tr28"), "GIT_OPTIONAL_LOCKS": "0"})
    return result


def execute(directory: Path) -> dict[str, Any]:
    manifest = verify(directory)
    directory = allowed_write(directory)
    if manifest["mode"] == "plan":
        return {"status": "STAGED_NOT_RUN", "rows": len(manifest["matrix"]), "failed": 0}
    if manifest["mode"] == "live":
        _validate_live_qualification(directory, (row["condition"] for row in manifest["matrix"]))
    with lock(directory):
        for row in manifest["matrix"]:
            key = f"{row['problem']}-{row['alias']}"
            result_path = directory / "results" / f"{key}.json"
            intent_path = directory / "intents" / f"{key}.json"
            output = directory / row["output"]
            if result_path.exists():
                continue
            if intent_path.exists() or output.exists():
                raise Refused("INDETERMINATE_ATTEMPT")
            put(intent_path, {"utc": utc(), "argv": row["argv"],
                "argv_sha256": row["argv_sha256"], "mode": manifest["mode"],
                "question": manifest["question"]})
            try:
                completed = subprocess.run(row["argv"], cwd=ROOT, env=_subprocess_environment(),
                    capture_output=True, text=True, encoding="utf-8", errors="strict",
                    check=False)
            except (OSError, subprocess.TimeoutExpired, UnicodeError):
                raise Refused("DISPATCH_INDETERMINATE") from None
            state = read_json(output / "state.json") if (output / "state.json").is_file() else {}
            status = "COMPLETE" if completed.returncode == 0 else "FAILED"
            put(result_path, {"utc": utc(), "status": status,
                "returncode": completed.returncode, "stdout": completed.stdout,
                "stderr": completed.stderr,
                "stop_reason": state.get("stop_reason") if isinstance(state, dict) else None,
                "evidence_sha256": hash_tree(output), "argv_sha256": row["argv_sha256"],
                "claim": ("Participant evidence" if manifest["mode"] == "live"
                          else "Offline fixture only; no participant/model evidence"),
                "provider_calls": None if manifest["mode"] == "live" else 0})
            print(f"{key}: {status} rc={completed.returncode}")
    failed = sum(
        read_json(directory / "results" / f"{row['problem']}-{row['alias']}.json")["returncode"] != 0
        for row in manifest["matrix"]
    )
    return {"status": "FINISHED", "rows": len(manifest["matrix"]), "failed": failed}


def rerun(directory: Path, question: str, reason: str, mode: str, **gate: Any) -> Path:
    if not reason.strip():
        raise Refused("RERUN_REASON_REQUIRED")
    prior = verify(directory)
    failed: list[tuple[str, str]] = []
    for row in prior["matrix"]:
        result_path = directory / "results" / f"{row['problem']}-{row['alias']}.json"
        if not result_path.is_file():
            raise Refused("UNRESOLVED_OR_UNSTARTED_CELL")
        if read_json(result_path).get("returncode") != 0:
            failed.append((row["problem"], row["condition"]))
    if not failed:
        raise Refused("NO_KNOWN_FAILED_CELLS")
    problems = list(dict.fromkeys(problem_id for problem_id, _condition in failed))
    conditions = [condition for condition in CONDITIONS
                  if any(row_condition == condition for _problem, row_condition in failed)]
    return create(directory.parent, problems, conditions, question, mode,
                  parent=directory, reason=reason, cells=failed, amendment=prior.get("amendment"), **gate)


def _add_gate_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--tokenizer-pins", type=Path)
    parser.add_argument("--capability", type=Path)
    parser.add_argument("--brief-manifest", type=Path)
    parser.add_argument("--authorize-live", action="store_true")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new")
    new.add_argument("--series", type=Path, default=DEFAULT_SERIES)
    new.add_argument("--problems", nargs="+", default=[f"O{number:02d}" for number in range(1, 9)])
    new.add_argument("--conditions", nargs="+", choices=CONDITIONS)
    new.add_argument("--amendment", choices=["R3-A2", "R3-A1", "occurrence-1"], default="R3-A1")
    new.add_argument("--expected-occurrence")
    new.add_argument("--question", required=True)
    new.add_argument("--mode", choices=["plan", "offline", "live"], default="plan")
    _add_gate_arguments(new)
    for name in ("resume", "status"):
        command = sub.add_parser(name)
        command.add_argument("--occurrence", type=Path, required=True)
    retry = sub.add_parser("rerun-failed")
    retry.add_argument("--occurrence", type=Path, required=True)
    retry.add_argument("--question", required=True)
    retry.add_argument("--reason", required=True)
    retry.add_argument("--mode", choices=["plan", "offline", "live"], default="plan")
    _add_gate_arguments(retry)
    args = parser.parse_args(argv)
    try:
        if args.command == "new":
            amendment = None if args.amendment == "occurrence-1" else args.amendment
            conditions = args.conditions or (R3_A1_CONDITIONS if amendment in PROSE_AMENDMENTS else CONDITIONS)
            directory = create(args.series, args.problems, conditions, args.question, args.mode,
                env_file=args.env_file, tokenizer_pins=args.tokenizer_pins,
                capability=args.capability, brief_manifest=args.brief_manifest,
                authorize_live=args.authorize_live, amendment=amendment,
                expected_occurrence=args.expected_occurrence)
            result = execute(directory)
        else:
            directory = allowed_write(args.occurrence)
            if args.command == "rerun-failed":
                directory = rerun(directory, args.question, args.reason, args.mode,
                    env_file=args.env_file, tokenizer_pins=args.tokenizer_pins,
                    capability=args.capability, brief_manifest=args.brief_manifest,
                    authorize_live=args.authorize_live)
                result = execute(directory)
            elif args.command == "resume":
                result = execute(directory)
            else:
                result = verify(directory)
        print(json.dumps({"occurrence": str(directory), "result": result}, ensure_ascii=False))
        return 2 if result.get("failed", 0) else 0
    except (Refused, OSError, KeyError, TypeError) as error:
        detail = str(error) if isinstance(error, Refused) else type(error).__name__
        print("R003_REFUSED: " + detail, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
