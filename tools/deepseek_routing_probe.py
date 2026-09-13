"""H002: actual DeepSeek responses through the frozen pure routing boundary."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import getpass
import json
import os
from pathlib import Path
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import luna_routing_probe as p
from minireason.provider import DeepSeek


def initialize(repo, output):
    frozen = p.verified(repo)
    if output.exists():
        raise FileExistsError("H002_OUTPUT_EXISTS")
    p.write_new(output / "plan.json", {
        "schema": "minireason.harness.deepseek-routing.v1", "status": "PREPARED",
        "created_utc": datetime.now(timezone.utc).isoformat(), "frozen_plan_id": p.PLAN_ID,
        "source_commit": git(repo, "rev-parse", "HEAD").decode().strip(),
        "candidate_sha256": frozen["candidate_sha256"], "system_sha256": frozen["system_sha256"],
        "probe_sha256": p.digest_bytes(Path(p.__file__).read_bytes()),
        "deepseek_probe_sha256": p.digest_bytes(Path(__file__).read_bytes()),
        "settings": p.study.settings().to_dict(), "max_provider_calls": 6,
        "max_completion_tokens_each": 8192, "max_aggregate_completion_tokens": 49152,
        "automatic_retries": 0, "sequence": [1, 2, 3, 4, 5, 6],
        "classification": "Actual DeepSeek pure-routing harness exercise; not original E028 or full durable Mini execution",
        "root_is_only_reviewer": True,
        "exercised": ["frozen compilation", "submission parser", "artifact identity", "event reducer", "brief renderer", "E028 route validator", "original DeepSeek transport and response checks"],
        "not_exercised": ["durable Mini scheduler", "directory fsync", "native toggle", "matched Mini causal comparison"],
        "renderer_fixture": "In-memory blobs and reducer-built prior artifacts; original durable path is neither invoked nor patched",
        "publication": "Root verifies request on remote main before each call and publishes response before next call"})


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE, timeout=90)


def check_plan(output):
    plan = p.check_probe(output)
    if (plan["deepseek_probe_sha256"] != p.digest_bytes(Path(__file__).read_bytes())
            or plan["settings"] != p.study.settings().to_dict()):
        raise ValueError("H002_CONFIGURATION_CHANGED")
    return plan


def make_request(repo, output, call):
    check_plan(output)
    if (output / "stopped.json").exists():
        raise ValueError("H002_ALREADY_STOPPED")
    if call > 1:
        p.answer(output, call - 1)
    route, _ = p.render(repo, output, *p.COORDINATES[call])
    payload = p.study.base.payload_for(route["messages"], p.study.settings())
    p.write_new(output / f"requests/{call:04d}.json", {
        **route, "schema": "minireason.harness.deepseek-request.v1", "call_id": call,
        "messages_sha256": p.study.base.digest(route["messages"]),
        "provider_payload": payload, "provider_payload_sha256": p.study.base.digest(payload),
        "classification": "Prepared actual DeepSeek request for pure-routing harness"})
    p.write_new(output / f"packets/{call:04d}.json", {"messages": route["messages"]})


def check_published(repo, output, call):
    root = Path(output).resolve()
    prefix = root.relative_to(Path(repo).resolve()).as_posix()
    names = ["plan.json", f"requests/{call:04d}.json", f"packets/{call:04d}.json"]
    names += [f"responses/{prior:04d}.{suffix}" for prior in range(1, call) for suffix in ("txt", "json")]
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    remote = git(repo, "ls-remote", "--refs", "origin", "refs/heads/main").decode().split()
    if not remote or remote[0] != head:
        raise ValueError("REMOTE_MAIN_CHANGED")
    for name in names:
        if git(repo, "show", "HEAD:" + prefix + "/" + name) != (root / name).read_bytes():
            raise ValueError("INPUT_NOT_PUBLISHED")
    return head


def execute(repo, output, call):
    check_plan(output)
    if (output / "stopped.json").exists() or (output / f"attempts/{call:04d}.json").exists():
        raise ValueError("H002_NO_RETRY")
    if not os.environ.get("DEEPSEEK_API_KEY"):
        raise ValueError("KEY_MISSING")
    for prior in range(1, call):
        p.answer(output, prior)
    request = p.checked_request(output, call)
    route, _ = p.render(repo, output, *p.COORDINATES[call])
    payload = p.study.base.payload_for(route["messages"], p.study.settings())
    if request["messages"] != route["messages"] or request["provider_payload"] != payload:
        raise ValueError("H002_REQUEST_CHANGED")
    head = check_published(repo, output, call)
    p.write_new(output / f"attempts/{call:04d}.json", {
        "call_id": call, "verified_remote_commit": head,
        "started_utc": datetime.now(timezone.utc).isoformat(), "automatic_retry": False})
    try:
        provider = DeepSeek(p.study.settings(), output / f"provider/{call:04d}")
        response = provider.complete(route["messages"], json_output=False,
            coordinate={"harness": "H002-deepseek-routing", "global_call_id": call,
                        "arm": route["arm"], "stage": route["stage"], "cycle": 1})
        text = p.study.validate_response(response, payload)
        raw = text.encode("utf-8")
        p.write_new(output / f"responses/{call:04d}.txt", raw)
        p.write_new(output / f"responses/{call:04d}.json", {
            "schema": "minireason.harness.deepseek-response.v1", "call_id": call,
            "request_messages_sha256": request["messages_sha256"],
            "text_sha256": p.digest_bytes(raw), "utf8_bytes": len(raw),
            "provider_record": f"provider/{call:04d}/call-0001.response.json",
            "returned_model": response.get("returned_model"), "status": response["status"],
            "usage": response["usage"], "finish_reason": response["finish_reason"],
            "classification": "Actual DeepSeek public answer; root semantic review separate"})
        return {"call_id": call, "status": response["status"], "usage": response["usage"]}
    except (Exception, KeyboardInterrupt) as error:
        p.write_new(output / "stopped.json", {"call_id": call, "status": "INTERRUPTED",
            "error_code": getattr(error, "code", type(error).__name__), "automatic_retry": False})
        raise


def summarize(repo, output):
    check_plan(output)
    routing = p.check_all(repo, output)
    responses = [p.load_json(output / f"responses/{i:04d}.json") for i in range(1, 7)]
    return {"schema": "minireason.harness.deepseek-summary.v1", "status": "COMPLETE",
        "provider_calls": 6, "rendered_stage_deliveries": 8, "reused_prefix_deliveries": 2,
        "usage": {key: (sum(row["usage"][key] for row in responses) if all(type(row["usage"].get(key)) is int for row in responses) else None) for key in ("prompt_tokens", "completion_tokens", "total_tokens")},
        "settings": p.study.settings().to_dict(), "all_finish_stop": all(r["finish_reason"] == "stop" for r in responses),
        "routes": routing["routes"], "shared_prefix_messages_equal": routing["shared_prefix_messages_equal"],
        "full_durable_Mini_run": False, "original_E028_completed": False,
        "semantic_appraisal": "Requires separate root review", "automatic_retries": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("init", "request", "send", "check"))
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--call", type=int, choices=range(1, 7))
    args = parser.parse_args()
    repo = p.PortableRepositoryPath(args.repo.resolve())
    try:
        if args.action == "init":
            initialize(repo, args.output)
        elif args.action == "request":
            make_request(repo, args.output, args.call)
        elif args.action == "send":
            if not sys.stdin.isatty():
                raise ValueError("NON_ECHOING_TERMINAL_REQUIRED")
            os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("DEEPSEEK_KEY_INPUT: ")
            try:
                print(json.dumps(execute(repo, args.output, args.call)))
            finally:
                os.environ.pop("DEEPSEEK_API_KEY", None)
        else:
            result = summarize(repo, args.output)
            p.write_new(args.output / "summary.json", result)
            print(json.dumps(result))
    except (Exception, KeyboardInterrupt) as error:
        print(json.dumps({"status": "STOPPED", "error_code": getattr(error, "code", type(error).__name__)}))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
