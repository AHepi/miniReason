#!/usr/bin/env python3
"""Run an inspectable personal prose reasoning loop."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from minireason.reason.engine import create_run, execute, status, GOOD_STOPS
from minireason.reason.storage import read
from minireason.reason.types import ReasonFailure


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
    for name in ("status", "resume"):
        commands.add_parser(name).add_argument("--run", type=Path, required=True)
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "run":
            directory = create_run(read(args.problem), args.cycles, args.recipe,
                args.out, args.mode, args.baseline, args.retry_transport)
            print("Run directory: " + str(directory.resolve()))
            result = execute(directory)
        elif args.command == "resume":
            result = execute(args.run)
        else:
            result = status(args.run)
        print(json.dumps({key: result[key] for key in
                         ("run_id", "stop_reason", "completed_cycles", "calls")}, ensure_ascii=False))
        return 0 if args.command == "status" or result["stop_reason"] in GOOD_STOPS else 2
    except ReasonFailure as exc:
        print(exc.code, file=sys.stderr)
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
