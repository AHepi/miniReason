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


def source_hashes(repo: Path) -> dict[str, str]:
    paths = (
        "tools/reason.py",
        "src/minireason/provider_openai_compat.py",
        "src/minireason/data/endpoints.json",
        "src/minireason/reason/adapter.py",
        "src/minireason/reason/config.py",
        "src/minireason/reason/engine.py",
        "src/minireason/reason/prompts.py",
        "src/minireason/reason/storage.py",
        "src/minireason/reason/types.py",
        "src/minireason/reason/worker.py",
        "src/minireason/reason/recipes/cross-family.json",
        "src/minireason/reason/recipes/single-family.json",
    )
    return {
        relative: hashlib.sha256(read_text(repo / relative).encode("utf-8")).hexdigest()
        for relative in paths
    }


def validate_prepared_source_pins(repo: Path, hashes: dict[str, str]) -> str:
    relative = "experiments/diagnostics/R001-reason-cli-vs-baselines/SOURCE_PINS.json"
    path = repo / relative
    pins = read_json(path).get("source_files")
    if not isinstance(pins, dict):
        raise LauncherError("Prepared source pins are missing or invalid")
    for source, digest in hashes.items():
        record = pins.get(source)
        source_bytes = read_text(repo / source).encode("utf-8")
        if (not isinstance(record, dict) or record.get("sha256") != digest
                or record.get("bytes") != len(source_bytes)):
            raise LauncherError("Current reason source differs from prepared source pin: " + source)
    return hashlib.sha256(read_text(path).encode("utf-8")).hexdigest()


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


def initial_manifest(repo: Path, run_root: Path, mode: str) -> dict:
    hashes = source_hashes(repo)
    pins_hash = validate_prepared_source_pins(repo, hashes)
    return {
        "schema": "minireason.r001.launcher.v1",
        "study": "R001-reason-cli-vs-baselines",
        "mode": mode,
        "run_root": run_root.relative_to(repo).as_posix(),
        "source_sha256": hashes,
        "source_pins_path": "experiments/diagnostics/R001-reason-cli-vs-baselines/SOURCE_PINS.json",
        "source_pins_sha256": pins_hash,
        "updated_utc": utc_now(),
        "problems": {},
    }


def load_manifest(path: Path, repo: Path, run_root: Path, mode: str) -> dict:
    if not path.exists():
        return initial_manifest(repo, run_root, mode)
    manifest = read_json(path)
    if manifest.get("schema") != "minireason.r001.launcher.v1":
        raise LauncherError("Existing manifest has an unsupported schema")
    if manifest.get("mode") != mode:
        raise LauncherError("Existing manifest mode differs from requested mode")
    if manifest.get("run_root") != run_root.relative_to(repo).as_posix():
        raise LauncherError("Existing manifest run root differs from requested run root")
    hashes = source_hashes(repo)
    pins_hash = validate_prepared_source_pins(repo, hashes)
    if manifest.get("source_sha256") != hashes:
        raise LauncherError("Current reason sources differ from the manifest source pins")
    if (manifest.get("source_pins_path") != "experiments/diagnostics/R001-reason-cli-vs-baselines/SOURCE_PINS.json"
            or manifest.get("source_pins_sha256") != pins_hash):
        raise LauncherError("Prepared source pin record differs from the manifest")
    return manifest


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
    record = {
        "label": f"R001-{problem_id}-" + ("CROSS" if spec["kind"] == "cross" else "LOOP-SINGLE"),
        "directory": spec["directory"].relative_to(repo).as_posix(),
        "recipe": spec["recipe"],
        "cycles": 3,
        "baseline": spec["baseline"],
        "run_id": run_id,
        "stop_reason": stop_reason,
        "last_action": action,
        "returncode": returncode,
        "updated_utc": utc_now(),
    }
    problem["occurrences"][spec["kind"]] = record
    for condition, label in spec["labels"].items():
        relative_directory = spec["directory"].relative_to(repo).as_posix()
        alias = {
            "label": label,
            "mode": manifest["mode"],
            "occurrence": spec["kind"],
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
    manifest["updated_utc"] = utc_now()


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
) -> int:
    directory = spec["directory"]
    if directory.exists():
        verify_existing(repo, directory, problem_file, mode, spec["recipe"], spec["baseline"])
        stop, run_id = saved_status(directory)
        if stop not in RESUMABLE_STOPS:
            print(f"{problem_id} {spec['kind']}: skip terminal {stop} ({run_id})")
            update_occurrence(manifest, repo, problem_id, spec, "skipped-terminal", stop, run_id, None)
            write_json(manifest_path, manifest)
            return 0 if stop in GOOD_STOPS else 2
        action = "resume"
        resume = True
    else:
        stop, run_id = "not_started", None
        action = "run"
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
    problems = normalized_problem_ids(args.problems)
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
        for kind in ("cross", "single"):
            spec = occurrence_spec(problem_id, kind, run_root)
            code = run_occurrence(
                repo,
                manifest_path,
                manifest,
                problem_id,
                problem_file,
                spec,
                args.mode,
                args.env_file,
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

