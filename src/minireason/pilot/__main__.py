"""Harness-facing CLI. Offline mode never opens an env file."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
from datetime import datetime, timezone
from uuid import uuid4
from .pilot import Pilot
from .util import strict_loads

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run")
    run.add_argument("--task", required=True, type=Path)
    run.add_argument("--env-file", type=Path)
    run.add_argument("--max-calls", type=int, default=None)
    run.add_argument("--mode", choices=["offline", "live"], default="offline")
    run.add_argument("--scripted", type=Path)
    run.add_argument("--out", type=Path)
    run.add_argument("--fanout", type=int, default=24)
    args = parser.parse_args(argv)
    try:
        with args.task.open(encoding="utf-8", newline="") as handle:
            task = strict_loads(handle.read())
        scripted = None
        if args.mode == "offline":
            if args.scripted is None:
                parser.error("offline mode requires --scripted; no automatic fabricated task answers")
            with args.scripted.open(encoding="utf-8", newline="") as handle:
                scripted = strict_loads(handle.read())
            if not isinstance(scripted, list):
                raise ValueError("SCRIPTED_MUST_BE_ARRAY")
        elif args.scripted is not None:
            raise ValueError("SCRIPTED_FOR_OFFLINE_ONLY")
        if args.mode == "live" and args.env_file is not None:
            # Reuse the explicit, ignored/untracked provider-key loader. No value is logged.
            loader = Path(__file__).resolve().parents[3] / "tools" / "reason.py"
            spec = importlib.util.spec_from_file_location("pilot_reason_env", loader)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.load_env_file(args.env_file)
        out = args.out or Path("work/w34/runs") / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:6])
        result = Pilot(task, out, mode=args.mode, max_calls=args.max_calls, scripted=scripted, fanout=args.fanout).run()
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result["status"] == "complete" else 2
    except Exception as error:
        # Never interpolate raw exception content from a secret-bearing input file.
        print(json.dumps({"status": "refused", "code": getattr(error, "code", type(error).__name__)}))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
