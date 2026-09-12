#!/usr/bin/env python3
"""Append atomic activity receipts; optionally wrap one repository command.

Describe the action and paths rather than recording raw command arguments,
which can contain credentials. This log is operational evidence, not a content
verdict. Decisions remain explained in docs/DECISION_LEDGER.md.
"""
from __future__ import annotations
import argparse
import datetime
import fcntl
import hashlib
import json
from pathlib import Path
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "docs" / "AGENT_ACTIVITY.jsonl"

def append(event):
    event = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), **event}
    with LOG.open("a", encoding="utf-8") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        handle.flush()
        fcntl.flock(handle, fcntl.LOCK_UN)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", required=True)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--action", required=True)
    parser.add_argument("--why", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--paths", nargs="*", default=[])
    parser.add_argument("--phase", choices=["begin", "outcome", "event"], default="event")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    event = {"event_id": uuid.uuid4().hex, "agent": args.agent, "decision": args.decision,
             "action": args.action, "why": args.why, "goal": args.goal, "paths": args.paths}
    if not command:
        append({**event, "phase": args.phase})
        return
    event["command_sha256"] = hashlib.sha256(json.dumps(command).encode()).hexdigest()
    append({**event, "phase": "begin"})
    try:
        result = subprocess.run(command)
    except BaseException as error:
        append({**event, "phase": "outcome", "outcome": "command interrupted or could not start", "error_type": type(error).__name__})
        raise
    append({**event, "phase": "outcome", "returncode": result.returncode})
    raise SystemExit(result.returncode)

if __name__ == "__main__":
    main()
