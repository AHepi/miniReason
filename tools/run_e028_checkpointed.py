"""Run one fixed E028 recovery occurrence with verified Git call checkpoints."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.run_sql_use_return import PortableRepositoryPath, probe_output_filesystem, study

PLAN_ID = "0e7ada3e11b348b7c3ea46805910ece3e14fdb700975e6a22b58b44c82569b5f"
PLAN = Path("experiments/plans/E028-sql-use-return")
OUTPUT = Path("experiments/records/E028-sql-use-return-recovery-01")
LEDGER = "docs/DECISION_LEDGER.md"
ACTIVITY = "docs/AGENT_ACTIVITY.jsonl"
APPEND_LOGS = {(OUTPUT / arm / "mini/log.jsonl").as_posix()
               for arm in ("criticism-returned", "criticism-archived")}
EXTERNAL_FILES = ("tools/run_e028_checkpointed.py", "tools/run_sql_use_return.py",
                  ".github/workflows/e028-recovery.yml")


class CheckpointError(RuntimeError):
    """A stable operational error; command output and credentials are omitted."""


class GitPublisher:
    def __init__(self, repo: Path, source_sha: str):
        self.repo, self.expected = repo, source_sha

    def git(self, *args: str, binary=False):
        identity = None
        if "commit" in args:
            identity = dict(os.environ, GIT_AUTHOR_NAME="miniReason Recovery Bot",
                            GIT_COMMITTER_NAME="miniReason Recovery Bot",
                            GIT_AUTHOR_EMAIL="minireason-recovery@users.noreply.github.com",
                            GIT_COMMITTER_EMAIL="minireason-recovery@users.noreply.github.com")
            identity.pop("DEEPSEEK_API_KEY", None)
        try:
            result = subprocess.run(["git", "-C", str(self.repo), *args],
                                    capture_output=True, text=not binary, encoding=None if binary else "utf-8",
                                    timeout=90, env=identity)
        except (OSError, subprocess.SubprocessError):
            raise CheckpointError("GIT_OPERATION_FAILED") from None
        if result.returncode:
            raise CheckpointError("GIT_OPERATION_FAILED")
        return result.stdout if binary else result.stdout.strip()

    def remote_head(self) -> str:
        rows = self.git("ls-remote", "--refs", "origin", "refs/heads/main").splitlines()
        if len(rows) != 1 or rows[0].split()[1] != "refs/heads/main":
            raise CheckpointError("REMOTE_MAIN_UNAVAILABLE")
        return rows[0].split()[0]

    def check_source(self) -> None:
        if (self.git("branch", "--show-current") != "main"
                or self.git("rev-parse", "HEAD") != self.expected
                or self.remote_head() != self.expected):
            raise CheckpointError("SOURCE_OR_REMOTE_CHANGED")

    def publish(self, label: str) -> dict[str, str]:
        self.check_source()
        staged = self.git("diff", "--cached", "--name-only", "-z").split("\0")
        if any(name and name not in (LEDGER, ACTIVITY) and not name.startswith(OUTPUT.as_posix() + "/")
               for name in staged):
            raise CheckpointError("UNEXPECTED_STAGED_FILES")
        timestamp = datetime.now(timezone.utc).isoformat()
        event = {"timestamp_utc": timestamp, "event_id": uuid.uuid4().hex,
                 "agent": "e028-checkpoint-runner", "decision": "REC-20260913-I",
                 "action": label, "why": "Publish actual evidence before further provider dispatch",
                 "goal": "Preserve one bounded E028 recovery occurrence", "phase": "event",
                 "paths": [OUTPUT.as_posix(), LEDGER, ACTIVITY], "previous_remote_commit": self.expected}
        receipts = {LEDGER: f"\nREC-20260913-I E028 recovery checkpoint at {timestamp}: {label}; "
                    f"previous verified remote {self.expected}; occurrence {OUTPUT.name}; no automatic retry.\n",
                    ACTIVITY: json.dumps(event, sort_keys=True) + "\n"}
        for name, text in receipts.items():
            with (self.repo / name).open("a", encoding="utf-8") as handle:
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
        self.git("add", "--", OUTPUT.as_posix(), LEDGER, ACTIVITY)
        changed = self.git("diff", "--cached", "--diff-filter=MDTR", "--name-only", "-z", "--", OUTPUT.as_posix())
        for name in filter(None, changed.split("\0")):
            if name not in APPEND_LOGS:
                raise CheckpointError("PUBLISHED_OUTPUT_CHANGED")
            previous = self.git("show", "HEAD:" + name, binary=True)
            current = self.git("show", ":" + name, binary=True)
            if not current.startswith(previous) or not current.endswith(b"\n"):
                raise CheckpointError("PUBLISHED_OUTPUT_CHANGED")
        key = os.environ.get("DEEPSEEK_API_KEY")
        if key:
            names = self.git("diff", "--cached", "--diff-filter=ACMRT", "--name-only", "-z")
            if any(key.encode("utf-8") in self.git("show", ":" + name, binary=True)
                   for name in filter(None, names.split("\0"))):
                raise CheckpointError("STAGED_CREDENTIAL_DETECTED")
        self.git("-c", "user.name=miniReason Recovery Bot", "-c",
                 "user.email=minireason-recovery@users.noreply.github.com",
                 "commit", "-m", "Record E028 recovery checkpoint: " + label)
        commit, tree = self.git("rev-parse", "HEAD"), self.git("rev-parse", "HEAD^{tree}")
        self.git("push", "--porcelain", "origin", "HEAD:main")
        if self.remote_head() != commit:
            raise CheckpointError("REMOTE_COMMIT_NOT_CONFIRMED")
        self.git("fetch", "--no-tags", "origin", "refs/heads/main")
        if self.git("rev-parse", "FETCH_HEAD") != commit or self.git("rev-parse", "FETCH_HEAD^{tree}") != tree:
            raise CheckpointError("REMOTE_TREE_NOT_CONFIRMED")
        self.expected = commit
        return {"commit": commit, "tree": tree}


class CheckpointProvider:
    def __init__(self, provider, publisher):
        self.provider, self.publisher, self.blocked = provider, publisher, False

    @property
    def settings(self):
        return self.provider.settings

    @property
    def calls(self):
        return self.provider.calls

    def checkpoint(self, label):
        try:
            self.publisher.publish(label)
        except (Exception, KeyboardInterrupt):
            self.blocked = True
            raise CheckpointError("CHECKPOINT_PUBLICATION_FAILED") from None

    def complete(self, *args, **kwargs):
        if self.blocked:
            raise CheckpointError("PUBLICATION_FAILURE_LATCHED")
        number = self.calls + 1
        self.checkpoint(f"before-call-{number:04d}")
        try:
            response = self.provider.complete(*args, **kwargs)
        except (Exception, KeyboardInterrupt):
            self.checkpoint(f"after-failed-call-{number:04d}")
            raise
        self.checkpoint(f"after-call-{number:04d}")
        return response


def metadata(repo: Path, plan: dict, source_sha: str) -> dict:
    return {"plan_id": PLAN_ID, "source_commit": source_sha, "occurrence": OUTPUT.name,
            "original_occurrence_status": "Records unavailable; prior ledger reported four responses; actual calls and usage remain unknown.",
            "external_wrapper": "Original provider and adapter with transparent Git publication observer",
            "external_files_sha256": {name: study.base.sha((repo / name).read_bytes()) for name in EXTERNAL_FILES},
            "participant_source_sha256": plan["source_sha256"],
            "plan_file_sha256": study.base.sha((repo / PLAN / "plan.json").read_bytes()),
            "runtime_files_sha256": study.base.digest(plan["runtime_files"]),
            "python": sys.version, "platform": platform.platform(), "utf8_mode": sys.flags.utf8_mode,
            "automatic_retries": 0, "automatic_successor_started": False}


def preflight(repo: Path, workspace: Path) -> dict:
    if not sys.flags.utf8_mode or os.name != "posix":
        raise CheckpointError("UTF8_AND_POSIX_REQUIRED")
    plan = study.verify(repo / PLAN, repo)
    if plan["plan_id"] != PLAN_ID:
        raise CheckpointError("PINNED_PLAN_CHANGED")
    workspace.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="scripted-", dir=workspace) as name:
        scratch = Path(name).resolve()
        scratch.relative_to(workspace.resolve())
        prepared = scratch / "prepared"
        probe_output_filesystem(prepared)
        if study.prepare(prepared, repo)["plan_id"] != PLAN_ID:
            raise CheckpointError("SCRIPTED_PREPARATION_CHANGED")
        scripted = json.loads((prepared / "preflight.json").read_bytes())
        if (scripted["provider_calls"], scripted["scripted_engine_calls"], scripted["scripted_unique_responses"]) != (0, 8, 6):
            raise CheckpointError("SCRIPTED_CALL_COUNTS_CHANGED")
    source = GitPublisher(repo, "").git("rev-parse", "HEAD")
    report = {**metadata(repo, plan, source), "status": "OFFLINE_PREFLIGHT_PASSED",
              "provider_calls": 0, "scripted_engine_calls": 8, "scripted_unique_responses": 6}
    study.base.write_json(workspace / ("preflight-" + uuid.uuid4().hex + ".json"), report)
    return report


def live(repo: Path, workspace: Path, report: dict) -> dict:
    output = repo / OUTPUT
    if output.exists():
        raise CheckpointError("RECOVERY_OUTPUT_ALREADY_EXISTS")
    if (os.environ.get("GITHUB_REF") != "refs/heads/main"
            or os.environ.get("GITHUB_RUN_ATTEMPT") != "1"
            or os.environ.get("GITHUB_SHA") != report["source_commit"]):
        raise CheckpointError("MAIN_FIRST_ATTEMPT_SOURCE_REQUIRED")
    publisher = GitPublisher(repo, report["source_commit"])
    publisher.check_source()
    if not os.environ.get("DEEPSEEK_API_KEY"):
        raise CheckpointError("KEY_MISSING")
    if not sys.flags.utf8_mode or os.name != "posix":
        raise CheckpointError("UTF8_AND_POSIX_REQUIRED")
    if study.verify(repo / PLAN, repo)["plan_id"] != PLAN_ID:
        raise CheckpointError("PINNED_PLAN_CHANGED")
    probe_output_filesystem(output)
    original_provider = study.DeepSeek

    def factory(settings, records):
        study.base.write_json(output / "execution-metadata.json", {
            "schema": "minireason.e028-recovery-execution.v1", "occurrence": OUTPUT.name,
            "plan_id": PLAN_ID, "preflight": report})
        return CheckpointProvider(original_provider(settings, records), publisher)

    study.DeepSeek = factory
    try:
        summary = study.run(repo / PLAN, output, repo, PLAN_ID)
    finally:
        study.DeepSeek = original_provider
    acknowledgement = publisher.publish("terminal-" + summary["status"].lower())
    study.base.write_json(workspace / "remote-acknowledgement.json", acknowledgement)
    return {"status": summary["status"], "provider_calls": summary["provider_calls"], **acknowledgement}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("preflight", "live"), required=True)
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    repo = PortableRepositoryPath(args.repo.resolve())
    workspace = Path(repo) / "work/e028-preflight"
    try:
        report = preflight(repo, workspace)
        result = live(repo, workspace, report) if args.mode == "live" else report
        print(json.dumps(result, sort_keys=True))
        return 0 if result["status"] in ("COMPLETE", "OFFLINE_PREFLIGHT_PASSED") else 2
    except (Exception, KeyboardInterrupt) as error:
        result = {"status": "OPERATIONAL_FAILURE",
                  "error_code": str(error) if isinstance(error, CheckpointError) else type(error).__name__}
        workspace.mkdir(parents=True, exist_ok=True)
        failure = workspace / ("failure-" + uuid.uuid4().hex + ".json")
        study.base.write_json(failure, result)
        print(json.dumps(result))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
