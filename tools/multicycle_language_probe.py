"""H003: canonical Mini cycle/port fixture; never invokes the durable scheduler."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import getpass
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from creib.forge.mini.executor import Request
from creib.forge.mini.kinds import read_submission
from creib.forge.mini.log import ARTIFACT_SUBMITTED, MiniState, apply_event, build_event
from creib.forge.mini.manifest import compile_manifest
from creib.forge.mini.runner import _store_artifact, render_brief
from minireason.provider import DeepSeek, Settings, digest

ARMS = ("prose", "whl", "rss", "whl-roundtrip", "rss-roundtrip")
CYCLES, CAP = 20, 4096
TASK, REOPEN, MODEL = "h003.task.v1", "h003.reopen.v1", "mini.verdict.v1"
ENVELOPE = ('## What to return\nA JSON object carrying "body" and "commitments". '
            'Both are strings and nothing else is required.')
PUBLIC = "## What to return\nReturn your complete public answer as prose. Do not wrap it in a JSON envelope."
SETTINGS = Settings(thinking=False, reasoning_effort="low", max_tokens=CAP, timeout_seconds=180)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def load(path):
    return json.loads(Path(path).read_bytes())


def write_new(path, value):
    path = Path(path)
    raw = value if isinstance(value, bytes) else encoded(value)
    key = os.environ.get("DEEPSEEK_API_KEY")
    if key and key.encode() in raw:
        raise ValueError("CREDENTIAL_IN_OUTPUT")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(raw)


def utc():
    return datetime.now(timezone.utc).isoformat()


def at(output, category, arm, cycle, suffix="json"):
    return Path(output) / category / arm / f"{cycle:02d}.{suffix}"


def stopped(output, arm):
    return Path(output) / "stopped" / arm / "arm-stopped.json"


def check_cycle(cycle):
    if type(cycle) is not int or not 1 <= cycle <= CYCLES:
        raise ValueError("CYCLE_OUT_OF_RANGE")


def repo_path(repo, name):
    path = Path(name)
    resolved = (Path(repo) / path).resolve()
    if path.is_absolute() or ".." in path.parts or not resolved.is_relative_to(Path(repo).resolve()):
        raise ValueError("SOURCE_PIN_OUTSIDE_REPOSITORY")
    return resolved


def material(output):
    value = load(Path(output) / "material.json")
    if value.get("schema") != "minireason.language-error-material.v1":
        raise ValueError("MATERIAL_SCHEMA")
    cycles, arms = value.get("cycles"), value.get("arms")
    if not isinstance(cycles, list) or len(cycles) != CYCLES:
        raise ValueError("MATERIAL_CYCLES")
    for index, row in enumerate(cycles, 1):
        reopen = row.get("reopen_cycles")
        if (row.get("cycle") != index or not isinstance(row.get("task"), str)
                or not isinstance(reopen, list) or len(set(reopen)) != len(reopen)
                or any(type(c) is not int or not 1 <= c < index for c in reopen)):
            raise ValueError("MATERIAL_CYCLE_OR_REOPEN")
    if (not isinstance(arms, list) or [a.get("arm_id") for a in arms] != list(ARMS)
            or any(not isinstance(a.get("instruction"), str) for a in arms)
            or not isinstance(value.get("shared_system"), str)
            or not isinstance(value.get("source_pins"), dict)):
        raise ValueError("MATERIAL_ARMS_OR_SYSTEM")
    return value


def manifest_for(arm):
    def kind(identity, title, ports):
        return {"kind_id": identity, "title": title,
                "instruction": "Use only the declared material and identify the grounds of your answer.",
                "commitment_call": "single", "input_ports": ports,
                "output_port": {"port_id": "out", "produces_kind": identity},
                "failure_policy": {"retries": 0, "tolerance": 0, "action": "stop"}}
    ports = [{"port_id": name, "port_type": name, "window": window} for name, window in
             (("task", "this_cycle"), ("reopened", "this_cycle"), ("previous", "previous_cycle"))]
    return {"schema_version": "creib.mini.manifest.v1", "manifest_id": "h003." + arm,
            "problem": "H003 language/error continuation through declared ports.",
            "cycles": {"max_cycles": CYCLES, "max_calls": CYCLES,
                       "completion_tokens_per_call": CAP, "max_completion_tokens": CYCLES * CAP},
            "kinds": [kind(TASK, "Current task", []), kind(REOPEN, "Re-presented targets", []),
                      kind(MODEL, "Continue the inquiry", ports)],
            "port_types": [{"port_type": name, "draws_from": {"artifact_kinds": [identity]},
                            "render": {"rule": "list_bodies", "header": title}}
                           for name, identity, title in (("task", TASK, "Current task"),
                           ("reopened", REOPEN, "Explicitly re-presented targets"),
                           ("previous", MODEL, "Previous own-arm response"))],
            "stages": [{"stage_id": "task", "kind_id": TASK, "seat": "machine", "ports": []},
                       {"stage_id": "reopened", "kind_id": REOPEN, "seat": "machine", "ports": []},
                       {"stage_id": "inquire", "kind_id": MODEL, "ports": [p["port_id"] for p in ports]},
                       {"stage_id": "end", "end": True}]}


def runtime_pins(repo):
    # Pin the original compiler/reducer/rendering dependency tree and provider, without reading observations.
    paths = sorted((Path(repo) / "src" / "creib").rglob("*.py"))
    paths += [Path(repo) / "src/minireason/provider.py"]
    return {p.relative_to(repo).as_posix(): sha(p.read_bytes()) for p in paths}


def verify_source_pins(repo, source_pins):
    for name, expected in source_pins.items():
        if not isinstance(expected, str) or sha(repo_path(repo, name).read_bytes()) != expected:
            raise ValueError("MATERIAL_SOURCE_CHANGED")


def plan_body(repo, output, data):
    verify_source_pins(repo, data["source_pins"])
    return {"schema": "minireason.h003.plan.v1", "material_sha256": sha((Path(output) / "material.json").read_bytes()),
            "helper_sha256": sha(Path(__file__).read_bytes()), "runtime_pins": runtime_pins(repo),
            "source_pins": data["source_pins"], "arms": list(ARMS), "cycles": CYCLES,
            "max_provider_calls": CYCLES * len(ARMS), "max_completion_tokens_each": CAP,
            "max_aggregate_completion_tokens": CYCLES * len(ARMS) * CAP,
            "max_workers": 5, "automatic_retries": 0, "settings": SETTINGS.to_dict(),
            "manifests": {arm: sha(encoded(manifest_for(arm))) for arm in ARMS},
            "fixture": "Canonical reducer and renderer with deterministic machine artifacts; not complete scheduler logs or durable-runner qualification",
            "instruction_transform": {"original_suffix": ENVELOPE, "replacement_suffix": PUBLIC},
            "publication": "Caller publishes completed cycle before preparing dependent cycle; no automatic Git mutations"}


def initialize(repo, output):
    repo, output = Path(repo).resolve(), Path(output).resolve()
    if (output / "plan.json").exists():
        raise FileExistsError("PLAN_ALREADY_EXISTS")
    data = material(output)
    body = plan_body(repo, output, data)
    for arm in ARMS:
        write_new(output / "manifests" / (arm + ".json"), manifest_for(arm))
        compile_manifest(output / "manifests" / (arm + ".json"))
    write_new(output / "plan.json", {**body, "plan_id": digest(body)})
    return body


def verify(repo, output):
    repo, output = Path(repo).resolve(), Path(output).resolve()
    data, plan = material(output), load(output / "plan.json")
    expected = plan_body(repo, output, data)
    if plan != {**expected, "plan_id": digest(expected)}:
        raise ValueError("PLAN_MATERIAL_OR_RUNTIME_CHANGED")
    for arm, expected_sha in plan["manifests"].items():
        if sha((output / "manifests" / (arm + ".json")).read_bytes()) != expected_sha:
            raise ValueError("MANIFEST_CHANGED")
    return data, plan


class MemoryBlobs:
    def __init__(self):
        self.values = {}
    def put(self, raw):
        identity = sha(raw)
        self.values[identity] = raw
        return identity
    def get(self, identity):
        return self.values[identity]


def payload_for(messages):
    return {"model": SETTINGS.model, "messages": messages, "stream": False,
            "max_tokens": CAP, "thinking": {"type": "disabled"}}


def valid_response(response, payload):
    # Original public-response contract, with this occurrence's 4096 cap.
    raw, usage = response.get("content"), response.get("usage", {})
    if (response.get("request") != payload or response.get("request_sha256") != digest(payload)
            or response.get("status") != "COMPLETE" or response.get("finish_reason") != "stop"
            or not isinstance(raw, str) or not raw.strip() or not isinstance(usage, dict)
            or any(type(usage.get(k)) is not int or usage[k] < 0 for k in ("prompt_tokens", "completion_tokens"))
            or usage["completion_tokens"] > CAP or response.get("reasoning_content_present", False)
            or response.get("reasoning_content_persisted", False) or response.get("credential_redaction", False)):
        raise ValueError("PUBLIC_RESPONSE_CONTRACT_FAILED")
    return raw


def read_response(output, arm, cycle, request):
    receipt_path = at(output, "responses", arm, cycle)
    receipt, raw = load(receipt_path), at(output, "responses", arm, cycle, "txt").read_bytes()
    record_path = at(output, "provider", arm, cycle).with_suffix("") / "call-0001.response.json"
    provider_raw = record_path.read_bytes()
    response = json.loads(provider_raw)
    if (receipt.get("status") != "COMPLETE" or receipt.get("arm") != arm or receipt.get("cycle") != cycle
            or receipt.get("request_sha256") != digest(request)
            or receipt.get("text_sha256") != sha(raw) or receipt.get("provider_response_sha256") != sha(provider_raw)
            or valid_response(response, request["provider_payload"]).encode("utf-8") != raw
            or receipt.get("usage") != response.get("usage") or receipt.get("returned_model") != response.get("returned_model")):
        raise ValueError("RESPONSE_CUSTODY_CHANGED")
    return raw.decode("utf-8"), receipt


def render_arm(repo, output, arm, cycle, data=None):
    check_cycle(cycle)
    if arm not in ARMS:
        raise ValueError("UNKNOWN_ARM")
    if data is None:
        data, _ = verify(repo, output)
    compiled = compile_manifest(Path(output) / "manifests" / (arm + ".json"))
    state, blobs = MiniState(), MemoryBlobs()
    seq, previous_event = 0, compiled.genesis
    answers, bindings = {}, {}
    def add(stage_id, text, n):
        nonlocal seq, previous_event
        stage = compiled.stage(stage_id)
        kind = compiled.kinds[stage.kind_id]
        submission = read_submission(json.dumps({"body": text, "commitments": text}, ensure_ascii=False), kind, "both")
        artifact, body_ref, commitments_ref = _store_artifact(blobs, stage, submission, seq)
        event = build_event(seq=seq, prev=previous_event, type=ARTIFACT_SUBMITTED, cycle=n,
                            stage_id=stage_id, kind_id=stage.kind_id, artifact_id=artifact,
                            body_ref=body_ref, commitments_ref=commitments_ref,
                            payload={"seat": stage.seat, "completion_tokens": 0})
        apply_event(state, event)
        seq, previous_event = seq + 1, event.event_id
        if blobs.get(body_ref) != text.encode("utf-8") or blobs.get(commitments_ref) != text.encode("utf-8"):
            raise ValueError("ARTIFACT_CUSTODY_CHANGED")
        return artifact
    own = next(a for a in data["arms"] if a["arm_id"] == arm)
    for n in range(1, cycle + 1):
        task = data["cycles"][n - 1]
        add("task", task["task"], n)
        reopened = []
        for target in task["reopen_cycles"]:
            b = bindings[target]
            reopened.append(f"Original own-arm cycle {target}; artifact {b['artifact_id']}; response SHA256 {b['text_sha256']}\n" + answers[target])
        add("reopened", "\n\n".join(reopened) if reopened else "No earlier target is re-presented in this cycle.", n)
        brief, exposed = render_brief(compiled, state, blobs, compiled.stage("inquire"), n)
        if exposed or not brief.endswith(ENVELOPE):
            raise ValueError("UNEXPECTED_RENDER_CONTRACT")
        public_brief = brief[:-len(ENVELOPE)] + PUBLIC
        messages = [{"role": "system", "content": data["shared_system"] + "\n\n" + own["instruction"]},
                    {"role": "user", "content": public_brief}]
        parents = ([bindings[n - 1]] if n > 1 else [])
        trace = {"arm": arm, "cycle": n, "model_stage": "inquire", "model_kind": MODEL,
                 "input_ports": {"task": {"window": "this_cycle", "cycle": n},
                                 "reopened": {"window": "this_cycle", "targets": [bindings[t] for t in task["reopen_cycles"]]},
                                 "previous": {"window": "previous_cycle", "parents": parents}},
                 "original_brief": brief, "original_brief_sha256": sha(brief.encode()),
                 "transform": {"original_suffix": ENVELOPE, "replacement_suffix": PUBLIC},
                 "fixture": "Reducer reconstruction only; zero reducer counters are not provider usage"}
        request = {"schema": "minireason.h003.request.v1", "arm": arm, "cycle": n,
                   "messages": messages, "messages_sha256": digest(messages), "provider_payload": payload_for(messages),
                   "provider_payload_sha256": digest(payload_for(messages)), "trace_sha256": digest(trace)}
        if n == cycle:
            return request, trace
        if load(at(output, "requests", arm, n)) != request or load(at(output, "traces", arm, n)) != trace:
            raise ValueError("ANCESTOR_REQUEST_OR_TRACE_CHANGED")
        text, receipt = read_response(output, arm, n, request)
        answers[n] = text
        artifact_id = add("inquire", text, n)
        bindings[n] = {"arm": arm, "cycle": n, "artifact_id": artifact_id,
                       "text_sha256": receipt["text_sha256"], "request_sha256": digest(request),
                       "receipt_sha256": sha(at(output, "responses", arm, n).read_bytes())}


def prepare(repo, output, cycle):
    check_cycle(cycle)
    data, _ = verify(repo, output)
    prepared = {}
    for arm in ARMS:
        if stopped(output, arm).exists():
            continue
        if at(output, "attempts", arm, cycle).exists() or at(output, "responses", arm, cycle).exists():
            raise FileExistsError("NO_RETRY")
        request, trace = render_arm(repo, output, arm, cycle, data)
        if at(output, "requests", arm, cycle).exists() or at(output, "traces", arm, cycle).exists():
            raise FileExistsError("REQUEST_ALREADY_EXISTS")
        prepared[arm] = (request, trace)
    for arm, (request, trace) in prepared.items():
        write_new(at(output, "requests", arm, cycle), request)
        write_new(at(output, "traces", arm, cycle), trace)
    return list(prepared)


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE, timeout=90)


def check_published(repo, output, cycle, arms):
    repo, output = Path(repo).resolve(), Path(output).resolve()
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    remote = git(repo, "ls-remote", "--refs", "origin", "refs/heads/main").decode().split()
    if not remote or remote[0] != head:
        raise ValueError("REMOTE_MAIN_CHANGED")
    paths = [output / "plan.json", output / "material.json", Path(__file__).resolve()]
    data, plan = verify(repo, output)
    paths += [repo_path(repo, p) for p in {**plan["runtime_pins"], **data["source_pins"]}]
    paths += [output / "manifests" / (a + ".json") for a in ARMS]
    for arm in ARMS:
        if stopped(output, arm).exists():
            paths.append(stopped(output, arm))
    for arm in arms:
        for n in range(1, cycle + 1):
            paths += [at(output, "requests", arm, n), at(output, "traces", arm, n)]
            if n < cycle:
                paths += [at(output, "responses", arm, n), at(output, "responses", arm, n, "txt"),
                          at(output, "attempts", arm, n)]
                provider = at(output, "provider", arm, n).with_suffix("")
                paths += [provider / "call-0001.request.json", provider / "call-0001.response.json"]
    for path in paths:
        name = path.resolve().relative_to(repo).as_posix()
        if git(repo, "show", head + ":" + name) != path.read_bytes():
            raise ValueError("INPUT_NOT_PUBLISHED")
    return head


def send_cycle(repo, output, cycle, *, provider_factory=None, publication_check=None, notify=print):
    check_cycle(cycle)
    data, _ = verify(repo, output)
    provider_factory = provider_factory or DeepSeek
    publication_check = publication_check or check_published
    if not os.environ.get("DEEPSEEK_API_KEY"):
        raise ValueError("KEY_MISSING")
    pending = {}
    for arm in ARMS:
        if stopped(output, arm).exists():
            continue
        if at(output, "attempts", arm, cycle).exists() or at(output, "responses", arm, cycle).exists():
            raise FileExistsError("NO_RETRY")
        request, trace = render_arm(repo, output, arm, cycle, data)
        if load(at(output, "requests", arm, cycle)) != request or load(at(output, "traces", arm, cycle)) != trace:
            raise ValueError("REQUEST_OR_TRACE_CHANGED")
        pending[arm] = request
    head = publication_check(repo, output, cycle, list(pending))
    def send(arm):
        request = pending[arm]
        started = utc()
        # Exclusive claim is outside the catch: a competing process may not turn a collision into an arm stop.
        write_new(at(output, "attempts", arm, cycle), {"arm": arm, "cycle": cycle,
                  "started_at": started, "request_sha256": digest(request), "published_commit": head,
                  "automatic_retry": False})
        response = None
        provider_dir = at(output, "provider", arm, cycle).with_suffix("")
        try:
            provider = provider_factory(SETTINGS, provider_dir)
            response = provider.complete(request["messages"], json_output=False,
                                         coordinate={"harness": "H003", "arm": arm, "cycle": cycle, "stage": "inquire"})
            text = valid_response(response, request["provider_payload"])
            status = "COMPLETE"
        except (Exception, KeyboardInterrupt):
            # No exception text/code is copied: either may contain credential-bearing remote data.
            status, text = "OPERATIONAL_FAILURE", None
            record = provider_dir / "call-0001.response.json"
            if record.exists():
                try:
                    response = load(record)
                    text = response.get("content") if isinstance(response.get("content"), str) else None
                except (ValueError, OSError):
                    response = None
        finished = utc()
        response = response or {}
        provider_path = provider_dir / "call-0001.response.json"
        receipt = {"arm": arm, "cycle": cycle, "status": status, "started_at": started, "finished_at": finished,
                   "request_sha256": digest(request), "text_sha256": sha(text.encode()) if text is not None else None,
                   "provider_response_sha256": sha(provider_path.read_bytes()) if provider_path.exists() else None,
                   "usage": response.get("usage"), "finish_reason": response.get("finish_reason"),
                   "returned_model": response.get("returned_model"), "automatic_retry": False}
        if text is not None:
            write_new(at(output, "responses", arm, cycle, "txt"), text.encode("utf-8"))
        write_new(at(output, "responses", arm, cycle), receipt)
        if status != "COMPLETE":
            write_new(stopped(output, arm), {"arm": arm, "cycle": cycle, "status": status,
                                           "finished_at": finished, "automatic_retry": False})
        notify(json.dumps({"arm": arm, "cycle": cycle, "status": status, "usage": receipt["usage"]}))
        return receipt
    results = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(send, arm) for arm in pending]
        for future in as_completed(futures):
            results.append(future.result())
    return sorted(results, key=lambda r: ARMS.index(r["arm"]))


def checkpoint(repo, output, through):
    check_cycle(through)
    data, _ = verify(repo, output)
    receipts, intervals, arms = [], [], {}
    pending_attempts = 0
    for arm in ARMS:
        completed = 0
        for n in range(1, through + 1):
            path = at(output, "responses", arm, n)
            attempt_path = at(output, "attempts", arm, n)
            if not path.exists():
                if attempt_path.exists():
                    pending_attempts += 1
                break
            receipt = load(path)
            request, trace = render_arm(repo, output, arm, n, data)
            if load(at(output, "requests", arm, n)) != request or load(at(output, "traces", arm, n)) != trace:
                raise ValueError("REQUEST_OR_TRACE_CHANGED")
            if receipt["status"] == "COMPLETE":
                read_response(output, arm, n, request)
                completed += 1
            receipts.append(receipt)
            intervals.extend([(receipt["started_at"], 1), (receipt["finished_at"], -1)])
            if receipt["status"] != "COMPLETE":
                break
        arms[arm] = {"completed_cycles": completed, "stopped": stopped(output, arm).exists()}
    current, maximum = 0, 0
    for _, delta in sorted(intervals, key=lambda row: (row[0], row[1])):
        current += delta
        maximum = max(maximum, current)
    usage = {}
    for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
        values = [(r.get("usage") or {}).get(key) for r in receipts]
        usage[key] = sum(values) if not pending_attempts and values and all(type(v) is int and v >= 0 for v in values) else None
    attempts = [p for arm in ARMS for n in range(1, through + 1)
                if (p := at(output, "attempts", arm, n)).exists()]
    summary = {"schema": "minireason.h003.checkpoint.v1", "through": through, "arms": arms,
               "status": "COMPLETE" if through == CYCLES and all(a["completed_cycles"] == CYCLES for a in arms.values()) else "PARTIAL",
               "attempt_markers": len(attempts), "terminal_receipts": len(receipts),
               "pending_attempts": pending_attempts,
               "provider_request_records": sum((at(output, "provider", arm, n).with_suffix("") / "call-0001.request.json").exists()
                                               for arm in ARMS for n in range(1, through + 1)),
               "usage": usage,
               "observed_maximum_concurrency": maximum,
               "concurrency_basis": "Completed helper call intervals only; includes local overhead, not server-observed concurrency",
               "concurrency_intervals_complete": pending_attempts == 0,
               "route_checks": "Exact canonical requests, traces and successful response custody",
               "full_durable_scheduler": False, "semantic_verdict": None}
    write_new(Path(output) / f"checkpoint{through:02d}.json", summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("init", "prepare", "send-cycle", "checkpoint"))
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cycle", type=int)
    parser.add_argument("--through", type=int)
    args = parser.parse_args()
    if args.command == "init":
        result = initialize(args.repo, args.output)
    elif args.command == "prepare":
        result = prepare(args.repo, args.output, args.cycle)
    elif args.command == "checkpoint":
        result = checkpoint(args.repo, args.output, args.through)
    else:
        if not sys.stdin.isatty():
            raise ValueError("TTY_REQUIRED")
        key = getpass.getpass("DEEPSEEK_KEY_INPUT")
        try:
            if not key:
                raise ValueError("KEY_MISSING")
            os.environ["DEEPSEEK_API_KEY"] = key
            result = send_cycle(args.repo, args.output, args.cycle,
                                notify=lambda line: print(line, flush=True))
        finally:
            os.environ.pop("DEEPSEEK_API_KEY", None)
            key = ""
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
