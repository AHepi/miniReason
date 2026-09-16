#!/usr/bin/env python3
"""Run the preregistered R001 conditions in problem-major order."""
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


PROBLEM_IDS = tuple(f"P{number:02d}" for number in range(1, 9))
RESUMABLE_STOPS = {"not_started", "running", "interrupted"}
GOOD_STOPS = {"cycle_budget", "no_new_objections"}
PROVIDER_KEYS = ("DEEPSEEK_API_KEY", "OLLAMA_API_KEY")
MANIFEST_SCHEMA = "minireason.r001.launcher.v2"
LEGACY_MANIFEST_SCHEMA = "minireason.r001.launcher.v1"
PINS_RELATIVE = "experiments/diagnostics/R001-reason-cli-vs-baselines/SOURCE_PINS.json"
LAUNCHER_RELATIVE = "experiments/diagnostics/R001-reason-cli-vs-baselines/run_R001.py"


class LauncherError(RuntimeError):
    pass


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def read_json(path: Path) -> dict:
    return json.loads(read_text(path))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("offline", "live"), default="offline")
    parser.add_argument(
        "--env-file",
        type=Path,
        help="Forward this path to tools/reason.py in live mode only",
    )
    parser.add_argument(
        "--problems",
        nargs="+",
        default=list(PROBLEM_IDS),
        metavar="PNN",
        help="Selected problem identifiers in study order",
    )
    parser.add_argument(
        "--run-root",
        type=Path,
        help="Launcher manifest directory; defaults to runs/R001-<mode>. Child runs always remain under runs/.",
    )
    rerun = parser.add_mutually_exclusive_group()
    rerun.add_argument(
        "--rerun-failed",
        action="store_true",
        help="Archive and rerun each existing occurrence whose stop is not a good stop",
    )
    rerun.add_argument(
        "--rerun",
        metavar="PNN:OCC",
        help="Archive and rerun one failed occurrence; OCC is cross or single",
    )
    return parser.parse_args(argv)


def normalized_problem_ids(values: list[str]) -> list[str]:
    result: list[str] = []
    for raw in values:
        value = raw.upper()
        if not re.fullmatch(r"P0[1-8]", value):
            raise LauncherError("Problem identifiers must be P01 through P08")
        if value in result:
            raise LauncherError("Duplicate problem identifier: " + value)
        result.append(value)
    expected = [problem_id for problem_id in PROBLEM_IDS if problem_id in result]
    if result != expected:
        raise LauncherError("Selected problems must remain in fixed P01 through P08 order")
    return result


def parse_rerun(value: str) -> tuple[str, str]:
    match = re.fullmatch(r"(P0[1-8]):(cross|single)", value, flags=re.IGNORECASE)
    if match is None:
        raise LauncherError("--rerun must be PNN:cross or PNN:single")
    return match.group(1).upper(), match.group(2).lower()


def prepared_pins(repo: Path) -> tuple[dict, str]:
    path = repo / PINS_RELATIVE
    pins = read_json(path)
    if not isinstance(pins.get("source_files"), dict):
        raise LauncherError("Prepared source pins are missing or invalid")
    if not isinstance(pins.get("sealed_task_files"), dict):
        raise LauncherError("Prepared task pins are missing or invalid")
    digest = hashlib.sha256(read_text(path).encode("utf-8")).hexdigest()
    return pins, digest


def source_hashes(repo: Path) -> dict[str, str]:
    pins, _ = prepared_pins(repo)
    paths = list(pins["source_files"])
    if LAUNCHER_RELATIVE not in paths:
        paths.append(LAUNCHER_RELATIVE)
    result: dict[str, str] = {}
    for relative in sorted(paths):
        path = repo / relative
        if not path.is_file():
            raise LauncherError("Current source file is missing: " + relative)
        result[relative] = hashlib.sha256(read_text(path).encode("utf-8")).hexdigest()
    return result


def source_version(
    version: int,
    hashes: dict[str, str],
    pins_hash: str,
    *,
    recorded_utc: str | None = None,
    basis: str,
) -> dict:
    return {
        "version": version,
        "recorded_utc": recorded_utc or utc_now(),
        "basis": basis,
        "source_sha256": hashes,
        "source_pins_path": PINS_RELATIVE,
        "source_pins_sha256": pins_hash,
    }


def initial_manifest(repo: Path, run_root: Path, mode: str) -> dict:
    hashes = source_hashes(repo)
    _, pins_hash = prepared_pins(repo)
    return {
        "schema": MANIFEST_SCHEMA,
        "study": "R001-reason-cli-vs-baselines",
        "mode": mode,
        "run_root": run_root.relative_to(repo).as_posix(),
        "source_sha256": hashes,
        "source_pins_path": PINS_RELATIVE,
        "source_pins_sha256": pins_hash,
        "source_versions": [source_version(1, hashes, pins_hash, basis="initial")],
        "active_source_version": 1,
        "updated_utc": utc_now(),
        "problems": {},
    }


def load_manifest(path: Path, repo: Path, run_root: Path, mode: str) -> dict:
    if not path.exists():
        return initial_manifest(repo, run_root, mode)
    manifest = read_json(path)
    schema = manifest.get("schema")
    if schema not in {LEGACY_MANIFEST_SCHEMA, MANIFEST_SCHEMA}:
        raise LauncherError("Existing manifest has an unsupported schema")
    if manifest.get("mode") != mode:
        raise LauncherError("Existing manifest mode differs from requested mode")
    if manifest.get("run_root") != run_root.relative_to(repo).as_posix():
        raise LauncherError("Existing manifest run root differs from requested run root")
    hashes = source_hashes(repo)
    _, pins_hash = prepared_pins(repo)
    if (manifest.get("source_pins_path") != PINS_RELATIVE
            or manifest.get("source_pins_sha256") != pins_hash):
        raise LauncherError("Prepared source/task pin record differs from the manifest")
    if schema == LEGACY_MANIFEST_SCHEMA:
        old_hashes = manifest.get("source_sha256")
        if not isinstance(old_hashes, dict):
            raise LauncherError("Legacy manifest source pins are invalid")
        manifest["schema"] = MANIFEST_SCHEMA
        manifest["source_versions"] = [source_version(
            1, old_hashes, pins_hash,
            recorded_utc=manifest.get("updated_utc"),
            basis="migrated-v1",
        )]
        manifest["active_source_version"] = 1
        for problem in manifest.get("problems", {}).values():
            if not isinstance(problem, dict):
                continue
            for record in problem.get("occurrences", {}).values():
                if isinstance(record, dict):
                    record.setdefault("source_version", 1)
    versions = manifest.get("source_versions")
    if not isinstance(versions, list) or not versions:
        raise LauncherError("Existing manifest source history is invalid")
    latest = versions[-1]
    if not isinstance(latest, dict) or not isinstance(latest.get("version"), int):
        raise LauncherError("Existing manifest source history is invalid")
    if latest.get("source_pins_sha256") != pins_hash:
        raise LauncherError("Prepared source/task pin record differs from source history")
    if latest.get("source_sha256") != hashes:
        number = latest["version"] + 1
        versions.append(source_version(number, hashes, pins_hash, basis="engineering-update"))
        manifest["active_source_version"] = number
    else:
        manifest["active_source_version"] = latest["version"]
    reconcile_pending_archives(manifest, repo)
    manifest["updated_utc"] = utc_now()
    return manifest

def validate_problem_pin(repo: Path, problem_id: str, problem_file: Path) -> dict[str, object]:
    pins_path = repo / "experiments" / "diagnostics" / "R001-reason-cli-vs-baselines" / "SOURCE_PINS.json"
    sealed = read_json(pins_path).get("sealed_task_files")
    relative = "problems/" + problem_id + ".txt"
    record = sealed.get(relative) if isinstance(sealed, dict) else None
    problem_bytes = read_text(problem_file).encode("utf-8")
    digest = hashlib.sha256(problem_bytes).hexdigest()
    if (not isinstance(record, dict) or record.get("sha256") != digest
            or record.get("bytes") != len(problem_bytes)):
        raise LauncherError("Selected problem differs from prepared task pin: " + problem_id)
    return {"path": relative, "sha256": digest, "bytes": len(problem_bytes)}


def occurrence_spec(problem_id: str, kind: str, run_root: Path) -> dict:
    if kind == "cross":
        return {
            "kind": kind,
            "directory": run_root / f"R001-{problem_id}-cross",
            "recipe": "cross-family",
            "baseline": True,
            "labels": {
                "BARE": f"R001-{problem_id}-BARE",
                "NATIVE": f"R001-{problem_id}-NATIVE",
                "LOOP-CROSS": f"R001-{problem_id}-LOOP-CROSS",
            },
        }
    return {
        "kind": kind,
        "directory": run_root / f"R001-{problem_id}-single",
        "recipe": "single-family",
        "baseline": False,
        "labels": {"LOOP-SINGLE": f"R001-{problem_id}-LOOP-SINGLE"},
    }


def saved_status(directory: Path) -> tuple[str, str | None]:
    config_path = directory / "config.json"
    if not config_path.exists():
        raise LauncherError("Existing occurrence lacks config.json: " + str(directory))
    config = read_json(config_path)
    calls = directory / "calls"
    unmatched = (
        request
        for request in sorted(calls.glob("*/a*/request.json"))
        if not request.with_name("response.json").exists()
    ) if calls.is_dir() else ()
    if next(iter(unmatched), None) is not None:
        stop = "INTERRUPTED_CALL"
    else:
        state_path = directory / "state.json"
        stop = read_json(state_path).get("stop_reason", "running") if state_path.exists() else "not_started"
    if not isinstance(stop, str) or not stop:
        raise LauncherError("Existing occurrence has an invalid stop reason: " + str(directory))
    run_id = config.get("run_id")
    if not isinstance(run_id, str) or not run_id:
        raise LauncherError("Existing occurrence has an invalid run id: " + str(directory))
    return stop, run_id


def verify_existing(
    repo: Path,
    directory: Path,
    problem_file: Path,
    mode: str,
    recipe: str,
    baseline: bool,
) -> None:
    config = read_json(directory / "config.json")
    if config.get("mode") != mode:
        raise LauncherError("Existing occurrence mode differs from requested mode: " + str(directory))
    if config.get("cycles") != 3 or config.get("baseline") is not baseline:
        raise LauncherError("Existing occurrence configuration differs from R001: " + str(directory))
    if config.get("retry_transport") != 0 or config.get("closing_return") is not True:
        raise LauncherError("Existing occurrence recovery policy differs from R001: " + str(directory))
    problem_hash = hashlib.sha256(read_text(problem_file).encode("utf-8")).hexdigest()
    if config.get("problem_sha256") != problem_hash:
        raise LauncherError("Existing occurrence problem differs from selected problem: " + str(directory))
    saved_recipe_text = read_text(directory / "recipe.json")
    shipped_recipe_text = read_text(repo / "src" / "minireason" / "reason" / "recipes" / (recipe + ".json"))
    shipped_recipe_hash = hashlib.sha256(shipped_recipe_text.encode("utf-8")).hexdigest()
    if (config.get("recipe_sha256") != shipped_recipe_hash
            or hashlib.sha256(saved_recipe_text.encode("utf-8")).hexdigest() != shipped_recipe_hash):
        raise LauncherError("Existing occurrence recipe bytes differ from the shipped recipe: " + str(directory))
    recipe_data = json.loads(saved_recipe_text)
    if recipe_data.get("name") != recipe or recipe_data.get("closing_return") is not True:
        raise LauncherError("Existing occurrence recipe differs from R001: " + str(directory))
    saved_endpoints_text = read_text(directory / "endpoints.json")
    current_endpoints_text = read_text(repo / "src" / "minireason" / "data" / "endpoints.json")
    current_endpoints_hash = hashlib.sha256(current_endpoints_text.encode("utf-8")).hexdigest()
    if (config.get("endpoints_sha256") != current_endpoints_hash
            or hashlib.sha256(saved_endpoints_text.encode("utf-8")).hexdigest() != current_endpoints_hash):
        raise LauncherError("Existing occurrence endpoints differ from current data: " + str(directory))


def occurrence_identity(problem_id: str, kind: str, number: int) -> str:
    return f"R001-{problem_id}-{kind}-attempt-{number:03d}"


def ensure_attempts(
    record: dict,
    problem_id: str,
    kind: str,
    source_version_number: int,
) -> list[dict]:
    attempts = record.get("attempts")
    if isinstance(attempts, list) and attempts:
        return attempts
    number = 1
    attempt = {
        "attempt_number": number,
        "occurrence_id": occurrence_identity(problem_id, kind, number),
        "directory": record.get("directory"),
        "run_id": record.get("run_id"),
        "stop_reason": record.get("stop_reason", "not_started"),
        "returncode": record.get("returncode"),
        "source_version": record.get("source_version", source_version_number),
        "status": "active",
        "updated_utc": record.get("updated_utc", utc_now()),
    }
    record["attempts"] = [attempt]
    record["occurrence_id"] = attempt["occurrence_id"]
    record["source_version"] = attempt["source_version"]
    return record["attempts"]


def reconcile_pending_archives(manifest: dict, repo: Path) -> None:
    for problem_id, problem in manifest.get("problems", {}).items():
        if not isinstance(problem, dict):
            continue
        for kind, record in problem.get("occurrences", {}).items():
            if not isinstance(record, dict) or "pending_archive" not in record:
                continue
            pending = record["pending_archive"]
            if not isinstance(pending, dict) or not isinstance(pending.get("directory"), str):
                raise LauncherError("Manifest pending archive record is invalid")
            canonical_value = record.get("directory")
            if not isinstance(canonical_value, str):
                raise LauncherError("Manifest occurrence directory is invalid")
            canonical = repo / canonical_value
            archive = repo / pending["directory"]
            if canonical.exists() and not archive.exists():
                record.pop("pending_archive")
                continue
            if canonical.exists() or not archive.exists():
                raise LauncherError("Cannot reconcile pending occurrence archive: " + str(canonical))
            source_number = int(record.get("source_version", 1))
            attempts = ensure_attempts(record, problem_id, kind, source_number)
            old = attempts[-1]
            old.update({
                "directory": pending["directory"],
                "status": "archived-failed",
                "archived_utc": utc_now(),
            })
            number = max(int(item.get("attempt_number", 0)) for item in attempts) + 1
            fresh_source = int(pending.get("fresh_source_version", manifest["active_source_version"]))
            fresh = {
                "attempt_number": number,
                "occurrence_id": occurrence_identity(problem_id, kind, number),
                "directory": canonical_value,
                "run_id": None,
                "stop_reason": "not_started",
                "returncode": None,
                "source_version": fresh_source,
                "status": "active",
                "updated_utc": utc_now(),
            }
            attempts.append(fresh)
            record.pop("pending_archive")
            record.update({
                "run_id": None,
                "stop_reason": "not_started",
                "returncode": None,
                "last_action": "rerun-archive-recovered",
                "updated_utc": fresh["updated_utc"],
                "occurrence_id": fresh["occurrence_id"],
                "source_version": fresh["source_version"],
            })


def update_occurrence(
    manifest: dict,
    repo: Path,
    problem_id: str,
    spec: dict,
    action: str,
    stop_reason: str,
    run_id: str | None,
    returncode: int | None,
) -> None:
    problem = manifest["problems"].setdefault(problem_id, {"occurrences": {}, "conditions": {}})
    occurrences = problem.setdefault("occurrences", {})
    record = occurrences.get(spec["kind"])
    if not isinstance(record, dict):
        record = {}
        occurrences[spec["kind"]] = record
    source_number = manifest["active_source_version"]
    attempts = ensure_attempts(record, problem_id, spec["kind"], source_number)
    active = attempts[-1]
    if returncode is None:
        returncode = active.get("returncode")
    now = utc_now()
    values = {
        "label": f"R001-{problem_id}-" + ("CROSS" if spec["kind"] == "cross" else "LOOP-SINGLE"),
        "directory": spec["directory"].relative_to(repo).as_posix(),
        "recipe": spec["recipe"],
        "cycles": 3,
        "baseline": spec["baseline"],
        "run_id": run_id,
        "stop_reason": stop_reason,
        "last_action": action,
        "returncode": returncode,
        "updated_utc": now,
        "occurrence_id": active["occurrence_id"],
        "source_version": active["source_version"],
    }
    record.update(values)
    active.update({
        "directory": values["directory"],
        "run_id": run_id,
        "stop_reason": stop_reason,
        "returncode": returncode,
        "status": "active",
        "updated_utc": now,
    })
    for condition, label in spec["labels"].items():
        relative_directory = values["directory"]
        alias = {
            "label": label,
            "mode": manifest["mode"],
            "occurrence": spec["kind"],
            "occurrence_id": record["occurrence_id"],
            "source_version": record["source_version"],
            "run_directory": relative_directory,
            "evidence_path": relative_directory,
            "run_id": run_id,
            "stop_reason": stop_reason,
        }
        if condition == "BARE":
            alias["call_id"] = "base-bare"
            alias["evidence_path"] = relative_directory + "/calls/base-bare"
        elif condition == "NATIVE":
            alias["call_id"] = "base-native"
            alias["evidence_path"] = relative_directory + "/calls/base-native"
        problem["conditions"][condition] = alias
    manifest["updated_utc"] = now


def next_archive_directory(directory: Path) -> Path:
    number = 1
    while True:
        candidate = directory.with_name(directory.name + f"-failed-{number}")
        if not candidate.exists():
            return candidate
        number += 1


def guarded_archive_move(repo: Path, directory: Path, archive: Path) -> None:
    runs_root = (repo / "runs").resolve(strict=True)
    lexical_source = Path(os.path.abspath(directory))
    lexical_archive = Path(os.path.abspath(archive))
    resolved_source = directory.resolve(strict=True)
    resolved_parent = directory.parent.resolve(strict=True)
    if os.path.normcase(str(resolved_source)) != os.path.normcase(str(lexical_source)):
        raise LauncherError("Occurrence archive source resolves through a link: " + str(directory))
    if resolved_source.parent != resolved_parent:
        raise LauncherError("Occurrence archive source parent is inconsistent: " + str(directory))
    try:
        resolved_source.relative_to(runs_root)
        resolved_parent.relative_to(runs_root)
    except ValueError as exc:
        raise LauncherError("Occurrence archive source is outside repository runs: " + str(directory)) from exc
    if lexical_archive.parent != lexical_source.parent:
        raise LauncherError("Occurrence archive target must have the same parent")
    if archive.exists():
        raise LauncherError("Occurrence archive target already exists: " + str(archive))
    lexical_source.rename(lexical_archive)


def archive_for_rerun(
    manifest_path: Path,
    manifest: dict,
    repo: Path,
    problem_id: str,
    spec: dict,
) -> Path:
    directory = spec["directory"]
    record = manifest["problems"][problem_id]["occurrences"][spec["kind"]]
    attempts = ensure_attempts(record, problem_id, spec["kind"], manifest["active_source_version"])
    archive = next_archive_directory(directory)
    record["pending_archive"] = {
        "directory": archive.relative_to(repo).as_posix(),
        "fresh_source_version": manifest["active_source_version"],
    }
    manifest["updated_utc"] = utc_now()
    write_json(manifest_path, manifest)
    guarded_archive_move(repo, directory, archive)
    old = attempts[-1]
    old.update({
        "directory": archive.relative_to(repo).as_posix(),
        "status": "archived-failed",
        "archived_utc": utc_now(),
    })
    number = max(int(attempt.get("attempt_number", 0)) for attempt in attempts) + 1
    fresh = {
        "attempt_number": number,
        "occurrence_id": occurrence_identity(problem_id, spec["kind"], number),
        "directory": directory.relative_to(repo).as_posix(),
        "run_id": None,
        "stop_reason": "not_started",
        "returncode": None,
        "source_version": manifest["active_source_version"],
        "status": "active",
        "updated_utc": utc_now(),
    }
    attempts.append(fresh)
    record.pop("pending_archive", None)
    record.update({
        "directory": fresh["directory"],
        "run_id": None,
        "stop_reason": "not_started",
        "returncode": None,
        "last_action": "rerun-archived",
        "updated_utc": fresh["updated_utc"],
        "occurrence_id": fresh["occurrence_id"],
        "source_version": fresh["source_version"],
    })
    manifest["updated_utc"] = fresh["updated_utc"]
    write_json(manifest_path, manifest)
    return archive

def child_environment() -> dict[str, str]:
    child = os.environ.copy()
    for name in PROVIDER_KEYS:
        child.pop(name, None)
    child["PYTHONUTF8"] = "1"
    child["PYTHONDONTWRITEBYTECODE"] = "1"
    child["PYTHONPATH"] = os.pathsep.join(("src", "tests"))
    # Respect the operator's temporary directory; do not redirect to another worker.
    return child


def command_for(
    repo: Path,
    problem_file: Path,
    spec: dict,
    mode: str,
    env_file: Path | None,
    resume: bool,
) -> list[str]:
    if resume:
        command = [
            sys.executable,
            str(repo / "tools" / "reason.py"),
            "resume",
            "--run",
            str(spec["directory"]),
        ]
    else:
        command = [
            sys.executable,
            str(repo / "tools" / "reason.py"),
            "run",
            "--problem",
            str(problem_file),
            "--cycles",
            "3",
            "--recipe",
            spec["recipe"],
            "--out",
            str(spec["directory"]),
            "--mode",
            mode,
            "--retry-transport",
            "0",
        ]
        if spec["baseline"]:
            command.append("--baseline")
    if mode == "live":
        command.extend(("--env-file", str(env_file)))
    return command


def run_occurrence(
    repo: Path,
    manifest_path: Path,
    manifest: dict,
    problem_id: str,
    problem_file: Path,
    spec: dict,
    mode: str,
    env_file: Path | None,
    rerun_mode: str | None,
) -> int:
    directory = spec["directory"]
    if directory.exists():
        verify_existing(repo, directory, problem_file, mode, spec["recipe"], spec["baseline"])
        stop, run_id = saved_status(directory)
        existing = (manifest.get("problems", {}).get(problem_id, {})
                    .get("occurrences", {}).get(spec["kind"]))
        attempt_source = (existing.get("source_version")
                          if isinstance(existing, dict) else manifest["active_source_version"])
        if (rerun_mode is None and stop in RESUMABLE_STOPS
                and attempt_source != manifest["active_source_version"]):
            raise LauncherError(
                "Refusing to resume an occurrence under changed sources; use --rerun-failed: "
                + str(directory)
            )
        if rerun_mode is not None:
            if stop in GOOD_STOPS:
                if rerun_mode == "specific":
                    raise LauncherError("Refusing to rerun a good-stop occurrence: " + str(directory))
                print(f"{problem_id} {spec['kind']}: skip good stop {stop} ({run_id})")
                update_occurrence(manifest, repo, problem_id, spec, "skipped-good", stop, run_id, None)
                write_json(manifest_path, manifest)
                return 0
            update_occurrence(manifest, repo, problem_id, spec, "rerun-archive-starting", stop, run_id, None)
            write_json(manifest_path, manifest)
            archive = archive_for_rerun(manifest_path, manifest, repo, problem_id, spec)
            print(f"{problem_id} {spec['kind']}: archived {archive.relative_to(repo).as_posix()}")
            stop, run_id = "not_started", None
            action = "rerun"
            resume = False
        elif stop not in RESUMABLE_STOPS:
            print(f"{problem_id} {spec['kind']}: skip terminal {stop} ({run_id})")
            update_occurrence(manifest, repo, problem_id, spec, "skipped-terminal", stop, run_id, None)
            write_json(manifest_path, manifest)
            return 0 if stop in GOOD_STOPS else 2
        else:
            action = "resume"
            resume = True
    else:
        existing = (manifest.get("problems", {}).get(problem_id, {})
                    .get("occurrences", {}).get(spec["kind"]))
        attempts = existing.get("attempts") if isinstance(existing, dict) else None
        recovered = (isinstance(attempts, list) and len(attempts) >= 2
                     and attempts[-1].get("status") == "active"
                     and attempts[-1].get("directory") == directory.relative_to(repo).as_posix()
                     and attempts[-1].get("stop_reason") == "not_started")
        if rerun_mode == "specific" and not recovered:
            raise LauncherError("Selected rerun occurrence does not exist: " + str(directory))
        stop, run_id = "not_started", None
        action = "rerun" if recovered else "run"
        if recovered:
            # No run directory or dispatch exists for this allocated attempt.
            # Pin the implementation used now, even if code changed after rename.
            existing["source_version"] = manifest["active_source_version"]
            attempts[-1]["source_version"] = manifest["active_source_version"]
        resume = False

    update_occurrence(manifest, repo, problem_id, spec, action + "-starting", stop, run_id, None)
    write_json(manifest_path, manifest)
    command = command_for(repo, problem_file, spec, mode, env_file, resume)
    print(f"{problem_id} {spec['kind']}: {action}")
    try:
        completed = subprocess.run(
            command,
            cwd=repo,
            env=child_environment(),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            check=False,
        )
    except KeyboardInterrupt:
        if directory.exists():
            stop, run_id = saved_status(directory)
            update_occurrence(manifest, repo, problem_id, spec, "launcher-interrupted", stop, run_id, 130)
            write_json(manifest_path, manifest)
        raise

    if completed.stdout:
        print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    if completed.stderr:
        print(completed.stderr, end="" if completed.stderr.endswith("\n") else "\n", file=sys.stderr)

    if directory.exists() and (directory / "config.json").exists():
        stop, run_id = saved_status(directory)
    else:
        stop, run_id = "launch-refused", None
    update_occurrence(manifest, repo, problem_id, spec, action + "-complete", stop, run_id, completed.returncode)
    write_json(manifest_path, manifest)
    if stop == "launch-refused":
        raise LauncherError("Child refused before creating a recoverable occurrence: " + str(directory))
    if stop in RESUMABLE_STOPS:
        raise LauncherError("Child left a nonterminal occurrence; successor launch is refused: " + str(directory))
    return completed.returncode


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo = Path(__file__).resolve().parents[3]
    study = Path(__file__).resolve().parent
    selected_rerun = parse_rerun(args.rerun) if args.rerun else None
    problems = ([selected_rerun[0]] if selected_rerun is not None
                else normalized_problem_ids(args.problems))
    if args.mode == "live" and args.env_file is None:
        raise LauncherError("--env-file is required in live mode")
    manifest_root = args.run_root or repo / "runs" / ("R001-" + args.mode)
    manifest_root = (repo / manifest_root).resolve() if not manifest_root.is_absolute() else manifest_root.resolve()
    # Stable mapping supports resume from the same manifest location. The short
    # occurrence root stays in runs/ even when the manifest is outside the repo.
    root_identity = os.path.normcase(str(manifest_root))
    suffix = hashlib.sha256(root_identity.encode("utf-8")).hexdigest()[:10]
    run_root = repo / "runs" / ("R001-" + args.mode + "-" + suffix)
    manifest_root.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_root / "manifest.json"
    manifest = load_manifest(manifest_path, repo, run_root, args.mode)

    result = 0
    for problem_id in problems:
        problem_file = study / "problems" / (problem_id + ".txt")
        if not problem_file.is_file():
            raise LauncherError("Problem file is missing: " + str(problem_file))
        problem_pin = validate_problem_pin(repo, problem_id, problem_file)
        manifest.setdefault("problem_pins", {})[problem_id] = problem_pin
        manifest["updated_utc"] = utc_now()
        write_json(manifest_path, manifest)
        kinds = ((selected_rerun[1],) if selected_rerun is not None
                 else ("cross", "single"))
        for kind in kinds:
            spec = occurrence_spec(problem_id, kind, run_root)
            rerun_mode = ("specific" if selected_rerun is not None
                          else "failed" if args.rerun_failed else None)
            code = run_occurrence(
                repo,
                manifest_path,
                manifest,
                problem_id,
                problem_file,
                spec,
                args.mode,
                args.env_file,
                rerun_mode,
            )
            if code != 0:
                result = 2
    return result


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LauncherError as exc:
        print("R001_LAUNCHER_REFUSED: " + str(exc), file=sys.stderr)
        raise SystemExit(2)

