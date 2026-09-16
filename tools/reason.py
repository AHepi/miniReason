#!/usr/bin/env python3
"""Run an inspectable personal prose reasoning loop."""
from __future__ import annotations
import argparse
import json
import os
import subprocess
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from minireason.reason.engine import create_run, execute, status, GOOD_STOPS
from minireason.reason.storage import read
from minireason.reason.types import ReasonFailure


ENV_KEYS = frozenset({"DEEPSEEK_API_KEY", "OLLAMA_API_KEY"})


def load_env_file(path):
    """Admit only provider keys from an ignored local file, without recording values."""
    if path is None:
        return
    supplied = Path(os.path.abspath(path))
    try:
        resolved = supplied.resolve(strict=True)
    except (OSError, RuntimeError):
        raise ReasonFailure("ENV_FILE_UNREADABLE", "Cannot resolve environment file") from None
    for candidate in dict.fromkeys((supplied, resolved)):
        try:
            relative = candidate.relative_to(ROOT).as_posix()
        except ValueError:
            raise ReasonFailure("ENV_FILE_OUTSIDE_REPOSITORY", "Environment file must be inside this checkout") from None
        try:
            tracked = subprocess.run(
                ["git", "-C", str(ROOT), "ls-files", "--error-unmatch", "--", relative],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            if tracked.returncode == 0:
                raise ReasonFailure("ENV_FILE_TRACKED", "Tracked environment files are refused")
            if tracked.returncode != 1:
                raise ReasonFailure("ENV_FILE_GIT_CHECK_FAILED", "Cannot establish environment file tracking")
            ignored = subprocess.run(
                ["git", "-C", str(ROOT), "check-ignore", "--no-index", "--quiet", "--", relative],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        except OSError:
            raise ReasonFailure("ENV_FILE_GIT_CHECK_FAILED", "Cannot check environment file tracking") from None
        if ignored.returncode == 1:
            raise ReasonFailure("ENV_FILE_NOT_IGNORED", "Environment file must be gitignored")
        if ignored.returncode != 0:
            raise ReasonFailure("ENV_FILE_GIT_CHECK_FAILED", "Cannot establish environment file ignore policy")
    try:
        with resolved.open(encoding="utf-8", newline="") as handle:
            text = handle.read()
    except (OSError, UnicodeError):
        raise ReasonFailure("ENV_FILE_UNREADABLE", "Cannot read UTF-8 environment file") from None
    values = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ReasonFailure("ENV_FILE_INVALID", "Expected KEY=VALUE assignments")
        name, value = (part.strip() for part in line.split("=", 1))
        if name not in ENV_KEYS:
            raise ReasonFailure("ENV_FILE_KEY_NOT_ALLOWED", "Only declared provider key names are allowed")
        if name in values:
            raise ReasonFailure("ENV_FILE_INVALID", "Duplicate environment key")
        if value.startswith(("'", '"')):
            if len(value) < 2 or value[-1] != value[0]:
                raise ReasonFailure("ENV_FILE_INVALID", "Unclosed quoted value")
            value = value[1:-1]
        if not value or "\x00" in value:
            raise ReasonFailure("ENV_FILE_INVALID", "Empty or invalid environment value")
        values[name] = value
    # Parse and validate the whole file first, so a refused file changes no keys.
    os.environ.update(values)


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="Start a new personal run")
    run.add_argument("--problem", type=Path, required=True)
    run.add_argument("--cycles", type=int, required=True)
    run.add_argument("--recipe", default="cross-family")
    run.add_argument("--baseline", action="store_true")
    run.add_argument("--out", type=Path)
    run.add_argument("--mode", choices=["live", "offline"], default="offline")
    run.add_argument("--retry-transport", type=int, default=0)
    run.add_argument("--env-file", type=Path, help="Load provider keys from a gitignored file inside this checkout")
    for name in ("run-r002", "run-r002-native"):
        command = commands.add_parser(name, help="Run the strict published R002 contract")
        command.add_argument("--problem", type=Path, required=True)
        command.add_argument("--out", type=Path, required=True)
        command.add_argument("--mode", choices=["live", "offline"], default="offline")
        command.add_argument("--relations", type=Path, required=True)
        command.add_argument("--tokenizer-pins", type=Path)
        command.add_argument("--capability", type=Path)
        command.add_argument("--attempt-policy", choices=["strict"], default="strict")
        command.add_argument("--prompt-token-cap", type=int, default=32768)
        command.add_argument("--retry-transport", type=int, default=0)
        command.add_argument("--env-file", type=Path, help="Opaque in offline mode; live load only at the call boundary")
        if name == "run-r002":
            command.add_argument("--recipe", required=True)
            command.add_argument("--cycles", type=int, default=3)
            command.add_argument("--fork-registry", type=Path, required=True)
            command.add_argument("--coding-manifest", type=Path, required=True)
            command.add_argument("--checker-policy", type=Path)
        else:
            command.add_argument("--condition", choices=["CAL-NATIVE", "NATIVE"], default="NATIVE")
            command.add_argument("--schema", type=Path)
            command.add_argument("--thinking", choices=["native"], default="native")
            command.add_argument("--reasoning-effort", choices=["medium"], default="medium")
            command.add_argument("--completion-tokens", type=int, default=32768)
    for name in ("status", "resume"):
        command = commands.add_parser(name)
        command.add_argument("--run", type=Path, required=True)
        if name == "resume":
            command.add_argument("--env-file", type=Path, help="Load provider keys from a gitignored file inside this checkout")
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        r002_resume = False
        if args.command == "resume":
            config_path = args.run / "config.json"
            if config_path.is_file():
                r002_resume = json.loads(read(config_path)).get("prompt_contract") == "r002-episodes-v2"
        if args.command == "run" or (args.command == "resume" and not r002_resume):
            load_env_file(args.env_file)
        if args.command in {"run-r002", "run-r002-native"}:
            from minireason.reason.engine import create_r002_run, create_r002_native_run, execute_r002
            if args.retry_transport != 0:
                raise ReasonFailure("CONFIG_ERROR", "R002 permits no retry")
            common = dict(mode=args.mode, attempt_policy=args.attempt_policy,
                          prompt_token_cap=args.prompt_token_cap, tokenizer_pins=args.tokenizer_pins,
                          relation_registry=args.relations, capability=args.capability,
                          problem_id=args.problem.stem)
            if args.command == "run-r002-native":
                directory = create_r002_native_run(read(args.problem), args.out,
                    condition=args.condition, schema_path=args.schema,
                    completion_tokens=args.completion_tokens, **common)
            else:
                directory = create_r002_run(read(args.problem), args.recipe, args.out,
                    cycles=args.cycles, fork_registry=args.fork_registry,
                    coding_manifest=args.coding_manifest, checker_policy=args.checker_policy, **common)
            print("Run directory: " + str(directory.resolve()))
            loaded = False
            def before_call(*_args, **_kwargs):
                nonlocal loaded
                if args.mode == "live" and not loaded:
                    load_env_file(args.env_file)
                    loaded = True
            result = execute_r002(directory, before_call=before_call)
        elif args.command == "run":
            directory = create_run(read(args.problem), args.cycles, args.recipe,
                args.out, args.mode, args.baseline, args.retry_transport)
            print("Run directory: " + str(directory.resolve()))
            result = execute(directory)
        elif args.command == "resume":
            if r002_resume:
                from minireason.reason.engine import execute_r002
                cfg = json.loads(read(args.run / "config.json"))
                loaded = False
                def before_resume_call(*_args, **_kwargs):
                    nonlocal loaded
                    if cfg["mode"] == "live" and not loaded:
                        load_env_file(args.env_file)
                        loaded = True
                result = execute_r002(args.run, before_call=before_resume_call)
            else:
                result = execute(args.run)
        else:
            result = status(args.run)
        print(json.dumps({key: result[key] for key in
                         ("run_id", "stop_reason", "completed_cycles", "calls", "stop_detail") if key in result}, ensure_ascii=False))
        return 0 if args.command == "status" or result["stop_reason"] in GOOD_STOPS or (
            (args.command.startswith("run-r002") or r002_resume) and result["stop_reason"] == "complete") else 2
    except ReasonFailure as exc:
        print(str(exc) if exc.code == "SCHEMA_FAILURE" else exc.code, file=sys.stderr)
        return 2
    except (ValueError, OSError, RuntimeError) as exc:
        # Never print problem, response, environment values or raw transport exceptions.
        known = str(exc) if str(exc) in {"PATH_TOO_LONG", "RUN_EXISTS", "RUN_BUSY",
            "PROBLEM_EMPTY", "CYCLES_INVALID", "CONFIG_INVALID"} else type(exc).__name__
        print("REFUSED: " + known, file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("interrupted: inspect the run before resume", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
