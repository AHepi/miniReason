"""Construction-only SQL study. Prepare and preflight are strictly offline.

The runner is deliberately separate from E024/E025 and does not run a use bridge.
Public model output is opaque prose; the Mini envelope is added by this adapter.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from typing import Any

from creib.forge.mini.executor import Reply
from creib.forge.mini.log import BlobStore, replay
from creib.forge.mini.manifest import compile_manifest
from creib.forge.mini.runner import run_mini
from minireason.provider import DeepSeek, Settings, digest
from minireason import provider as provider_module
from creib.forge.mini import runner as mini_runner_module

TEST_ID = "E026-sql-construction"
KIND = "mini.verdict.v1"  # Mandatory terminal transport kind; no semantic standing.
TITLE = "Construct a retained-state update account"
INSTRUCTION = "Answer the supplied construction task. Preserve uncertainty, unsupported cases, and any finding of insufficiency in your account."
SYSTEM = "Produce an explanatory construction for the supplied SQL maintenance problem. Ordinary prose, mathematics and optional code are equally admissible. Return your complete account as text; there is no required answer vocabulary or executable form."
HOST_RETURN = '## What to return\nA JSON object carrying "body" and "commitments". Both are strings and nothing else is required.'
ARMS = ("direct-disabled", "direct-native", "prompt-control-disabled", "prompt-control-native", "mini-disabled", "mini-native")
SELECTED_ARM = "mini-disabled"
SOURCE_FIELDS = {"schema", "schema_sql", "query_sql", "task", "source_notes", "sources", "value_domain", "events", "constraints"}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def encoded(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_bytes(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(raw)


def write_json(path: Path, value: Any) -> None:
    # Offline paths must not inspect credential environment variables.
    write_bytes(path, encoded(value))


def read_source(path: Path) -> bytes:
    raw = path.read_bytes()
    value = json.loads(raw)
    if type(value) is not dict or set(value) != SOURCE_FIELDS or value["schema"] != "minireason.sql-construction-material.v1":
        raise ValueError("EXACT_PARTICIPANT_CONSTRUCTION_SCHEMA_REQUIRED")
    if any(type(value[key]) is not str or not value[key].strip() for key in ("task", "schema_sql", "query_sql", "source_notes")):
        raise ValueError("NONEMPTY_PUBLIC_SOURCE_REQUIRED")
    return raw


def runtime_files(repo: Path) -> dict[str, str]:
    # Bind local Python implementation and its packaged policies/schemas. External
    # runtime versions and provider aliases are reported, not called immutable.
    expected_modules = [(provider_module, "src/minireason/provider.py"), (mini_runner_module, "src/creib/forge/mini/runner.py")]
    if any(Path(module.__file__).resolve() != (repo / path).resolve() for module, path in expected_modules):
        raise ValueError("HASHED_CHECKOUT_IS_NOT_IMPORTED_RUNTIME")
    paths = [p for p in (repo / "src/creib").rglob("*") if p.suffix in {".py", ".json"}]
    paths.append(repo / "src/minireason/provider.py")
    if not paths or not all(p.is_file() for p in paths):
        raise ValueError("RUNTIME_SOURCE_MISSING")
    return {str(p.relative_to(repo)): sha(p.read_bytes()) for p in sorted(paths)}


def manifest_for(source: bytes, cap: int) -> dict[str, Any]:
    return {"schema_version": "creib.mini.manifest.v1", "manifest_id": "minireason.sql-construction.v1." + sha(source)[:16],
        "problem": source.decode("utf-8"),
        "kinds": [{"kind_id": KIND, "title": TITLE, "instruction": INSTRUCTION, "commitment_call": "single",
            "input_ports": [{"port_id": "problem", "port_type": "problem", "window": "all"}],
            "output_port": {"port_id": "out", "produces_kind": KIND},
            "failure_policy": {"retries": 0, "tolerance": 0, "action": "stop"}}],
        "stages": [{"stage_id": "construct", "kind_id": KIND, "ports": ["problem"]}, {"stage_id": "end", "end": True}],
        "cycles": {"max_cycles": 1, "max_calls": 1, "completion_tokens_per_call": cap, "max_completion_tokens": cap}}


def expected_brief(source: bytes) -> str:
    return "\n\n".join(["# " + TITLE, INSTRUCTION, "## The problem (problem)\n" + source.decode("utf-8"), HOST_RETURN])


def messages_for(source: bytes, arm: str) -> list[dict[str, str]]:
    if arm not in ARMS:
        raise ValueError("UNKNOWN_ARM")
    if arm.startswith("direct-"):
        user = source.decode("utf-8")
    else:
        # The exact engine-supplied JSON-return suffix belongs to host transport;
        # it is removed only after full routed-brief equality is established.
        user = expected_brief(source).removesuffix("\n\n" + HOST_RETURN)
    return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]


def settings_for(arm: str, cap: int) -> Settings:
    return Settings(thinking=arm.endswith("native"), reasoning_effort="low", max_tokens=cap)


def payload_for(messages: list[dict[str, str]], settings: Settings) -> dict[str, Any]:
    payload = {"model": settings.model, "messages": messages, "stream": False, "max_tokens": settings.max_tokens,
               "thinking": {"type": "enabled" if settings.thinking else "disabled"}}
    if settings.thinking:
        payload["reasoning_effort"] = settings.reasoning_effort
    return payload


def validate_coordinate(request: Any, source: bytes) -> None:
    if (request.stage_id, request.kind_id, request.cycle, request.attempt, request.phase, request.optional_fields) != ("construct", KIND, 1, 0, "both", ()):
        raise ValueError("UNEXPECTED_MINI_COORDINATE")
    if request.brief != expected_brief(source):
        raise ValueError("ROUTED_SOURCE_MISMATCH")


class Capture:
    def __init__(self, source: bytes, cap: int, raw: str):
        self.source, self.completion_cap, self.raw = source, cap, raw
        self.requests = []

    def reply(self, request: Any) -> Reply:
        validate_coordinate(request, self.source)
        self.requests.append({"stage": request.stage_id, "cycle": request.cycle, "phase": request.phase,
                              "brief": request.brief, "brief_sha256": sha(request.brief.encode("utf-8"))})
        return Reply(json.dumps({"body": self.raw, "commitments": self.raw}, ensure_ascii=False), 1, 1)


def artifact_prose(root: Path, compiled: Any) -> list[dict[str, str]]:
    state = replay(root / "log.jsonl", compiled.genesis)
    blobs = BlobStore(root / "blobs")
    rows = []
    for artifact_id in state.artifact_order:
        artifact = state.artifacts[artifact_id]
        if artifact["kind_id"] == KIND:
            rows.append({"artifact_id": artifact_id, "body": blobs.get(artifact["body_ref"]).decode("utf-8"),
                         "commitments": blobs.get(artifact["commitments_ref"]).decode("utf-8")})
    return rows


def probe(manifest_path: Path, source: bytes, cap: int, root: Path, raw: str = "Offline routing probe; no constructed SQL solution.") -> dict[str, Any]:
    compiled = compile_manifest(manifest_path)
    capture = Capture(source, cap, raw)
    outcome = run_mini(compiled, root, capture, responder_id="sql-construction-offline-capture")
    rows = artifact_prose(root, compiled)
    if len(capture.requests) != 1 or len(rows) != 1 or rows[0]["body"] != raw or rows[0]["commitments"] != raw:
        raise ValueError("OFFLINE_PROSE_CUSTODY_FAILURE")
    return {"status": "OFFLINE_PREFLIGHT_PASSED", "provider_calls": 0, "scripted_engine_calls": 1,
            "compiled_plan_id": compiled.genesis, "compiled_header_sha256": digest(compiled.header),
            "captured_requests": capture.requests, "opaque_prose_preserved": True,
            "run_outcome": {**asdict(outcome), "root": "offline-probe"}}


def effective_contract(cap: int) -> dict[str, Any]:
    settings_for(ARMS[0], cap)
    return {"schema": "minireason.sql-construction-plan.v1", "test_id": TEST_ID, "status": "FROZEN_PREPARATION_ONLY",
        "arms": list(ARMS), "selected_construction_arm": SELECTED_ARM,
        "selection_rule": "Fixed before all provider outputs; never substitute another arm after failure.",
        "max_tokens_per_call": cap, "max_provider_calls": len(ARMS), "max_aggregate_completion_tokens": cap * len(ARMS),
        "jobs": 1, "automatic_retries": 0, "native_reasoning_effort": "low",
        "endpoint": "https://api.deepseek.com/v1/chat/completions",
        "template": "construct_update_account_v1", "cycles_per_arm": 1, "model_stages_per_cycle": ["construct"],
        "terminal_kind_is_transport_only": True, "operator_input_files": [],
        "later_use_bridge": "UNIMPLEMENTED: freeze a separately reviewed bridge using the complete selected public occurrence.",
        "semantic_appraisal": "Unresolved; engine status and finite task checks confer no semantic standing.",
        "comparison_limit": "One-stage Mini versus its exact prompt control tests recording/routing custody, not multi-stage orchestration advantage. Single samples do not isolate chance or model drift."}


def prepare(source_path: Path, root: Path, repo: Path, cap: int = 8192) -> dict[str, Any]:
    source = read_source(source_path)
    settings_for(ARMS[0], cap)
    root.mkdir(parents=True, exist_ok=False)
    write_bytes(root / "participant-source.json", source)
    manifest = manifest_for(source, cap)
    write_json(root / "manifest.json", manifest)
    preflight = probe(root / "manifest.json", source, cap, root / "offline-probe")
    requests = {}
    for arm in ARMS:
        settings = settings_for(arm, cap)
        payload = payload_for(messages_for(source, arm), settings)
        requests[arm] = {"request_sha256": digest(payload), "request": payload, "settings": settings.to_dict()}
        write_json(root / "requests" / (arm + ".json"), requests[arm])
    plan = {**effective_contract(cap),
        "source_sha256": sha(source), "source_bytes": len(source), "manifest_sha256": sha(encoded(manifest)),
        "compiled_plan_id": preflight["compiled_plan_id"], "compiled_header_sha256": preflight["compiled_header_sha256"],
        "adapter_sha256": sha(Path(__file__).read_bytes()), "runtime_files": runtime_files(repo),
        "request_sha256": {arm: row["request_sha256"] for arm, row in requests.items()}}
    plan["plan_id"] = digest(plan)
    write_json(root / "plan.json", plan)
    write_json(root / "preflight.json", {**preflight, "plan_id": plan["plan_id"],
        "prompt_controls_equal_mini_payloads": all(requests["mini-" + mode]["request"] == requests["prompt-control-" + mode]["request"] for mode in ("disabled", "native")),
        "source_allowlist": ["participant-source.json"], "operator_material_read_by_adapter": False})
    return plan


def verify(root: Path, repo: Path) -> dict[str, Any]:
    plan = json.loads((root / "plan.json").read_bytes())
    body = {key: value for key, value in plan.items() if key != "plan_id"}
    if plan.get("plan_id") != digest(body):
        raise ValueError("PLAN_IDENTITY_MISMATCH")
    if plan["adapter_sha256"] != sha(Path(__file__).read_bytes()) or plan["runtime_files"] != runtime_files(repo):
        raise ValueError("RUNTIME_SOURCE_CHANGED")
    source = read_source(root / "participant-source.json")
    if (sha(source), len(source)) != (plan["source_sha256"], plan["source_bytes"]):
        raise ValueError("PARTICIPANT_SOURCE_CHANGED")
    cap = plan["max_tokens_per_call"]
    expected = effective_contract(cap)
    changed = [key for key, value in expected.items() if key not in plan or type(plan[key]) is not type(value) or plan[key] != value]
    if changed:
        raise ValueError("EFFECTIVE_CONTRACT_CHANGED: " + ", ".join(sorted(changed)))
    manifest = manifest_for(source, cap)
    if (root / "manifest.json").read_bytes() != encoded(manifest) or sha(encoded(manifest)) != plan["manifest_sha256"]:
        raise ValueError("MINI_MANIFEST_CHANGED")
    compiled = compile_manifest(root / "manifest.json")
    if compiled.genesis != plan["compiled_plan_id"] or digest(compiled.header) != plan["compiled_header_sha256"]:
        raise ValueError("COMPILED_PLAN_CHANGED")
    for arm in ARMS:
        settings = settings_for(arm, cap)
        payload = payload_for(messages_for(source, arm), settings)
        expected = {"request_sha256": digest(payload), "request": payload, "settings": settings.to_dict()}
        if json.loads((root / "requests" / (arm + ".json")).read_bytes()) != expected or plan["request_sha256"][arm] != digest(payload):
            raise ValueError("FROZEN_REQUEST_CHANGED")
    return plan


class LiveProse:
    def __init__(self, provider: Any, source: bytes, arm: str, output: Path):
        self.provider, self.source, self.arm, self.output = provider, source, arm, output
        self.completion_cap = provider.settings.max_tokens
        self.calls = 0
        self.response = None

    def reply(self, request: Any) -> Reply:
        validate_coordinate(request, self.source)
        if self.calls:
            raise ValueError("DUPLICATE_CONSTRUCTION_CALL")
        self.calls += 1
        write_json(self.output / "route.json", {"brief": request.brief, "transformation": "Remove only exact host JSON-return suffix; preserve all routed public source.",
            "messages": messages_for(self.source, self.arm)})
        self.response = self.provider.complete(messages_for(self.source, self.arm), json_output=False,
            coordinate={"arm": self.arm, "stage": "construct", "cycle": 1, "phase": "raw-prose"})
        raw = self.response["content"]
        write_bytes(self.output / "public-answer.txt", raw.encode("utf-8"))
        return Reply(json.dumps({"body": raw, "commitments": raw}, ensure_ascii=False),
                     self.response["usage"]["prompt_tokens"], self.response["usage"]["completion_tokens"])


def run(root: Path, output: Path, repo: Path, expected_plan_id: str) -> dict[str, Any]:
    # This is the only function that instantiates DeepSeek and therefore accesses
    # its credential. It is never entered by prepare, verify or offline tests.
    plan = verify(root, repo)
    if plan["plan_id"] != expected_plan_id:
        raise ValueError("EXTERNALLY_PINNED_PLAN_ID_MISMATCH")
    source = read_source(root / "participant-source.json")
    output.mkdir(parents=True, exist_ok=False)
    write_json(output / "plan.json", plan)
    rows = []
    for arm in ARMS:
        arm_root = output / arm
        provider = None
        try:
            # Recheck source and request identities before each new spending action.
            verify(root, repo)
            settings = settings_for(arm, plan["max_tokens_per_call"])
            provider = DeepSeek(settings, arm_root / "calls")
            if arm.startswith("mini-"):
                responder = LiveProse(provider, source, arm, arm_root)
                compiled = compile_manifest(root / "manifest.json")
                outcome = run_mini(compiled, arm_root / "mini", responder,
                    responder_id="deepseek-flash:sql-construction", endpoint=settings)
                response = responder.response
                custody = artifact_prose(arm_root / "mini", compiled)
                if response is None or len(custody) != 1 or any(custody[0][name] != response["content"] for name in ("body", "commitments")):
                    raise ValueError("MINI_PUBLIC_PROSE_CUSTODY_FAILED")
            else:
                response = provider.complete(messages_for(source, arm), json_output=False,
                    coordinate={"arm": arm, "stage": "construct", "cycle": 1, "phase": "raw-prose"})
                write_bytes(arm_root / "public-answer.txt", response["content"].encode("utf-8"))
            if response["request_sha256"] != plan["request_sha256"][arm]:
                raise ValueError("ACTUAL_WIRE_REQUEST_CHANGED")
            row = {"arm": arm, "status": "PUBLIC_RESPONSE_RECORDED", "answer_sha256": sha(response["content"].encode("utf-8")),
                   "usage": response["usage"], "request_sha256": response["request_sha256"], "content_appraisal": "Unresolved"}
        except Exception as error:
            # Provider stores sanitized error detail. Only a stable code is copied
            # here, never arbitrary exception text that could contain a credential.
            row = {"arm": arm, "status": "OPERATIONAL_FAILURE", "error_code": getattr(error, "code", type(error).__name__),
                   "content_appraisal": "Unresolved", "attempted_calls": provider.calls if provider else 0,
                   "usage_of_unreturned_calls": "Unknown"}
            write_json(arm_root / "result.json", row)
            rows.append(row)
            break
        write_json(arm_root / "result.json", row)
        rows.append(row)
    summary = {"plan_id": plan["plan_id"], "arms": rows, "status": "COMPLETE" if len(rows) == len(ARMS) and all(r["status"] == "PUBLIC_RESPONSE_RECORDED" for r in rows) else "INTERRUPTED",
               "selected_construction_arm": SELECTED_ARM, "automatic_successor_started": False,
               "semantic_appraisal": "Unresolved", "unattempted_arms": list(ARMS[len(rows):])}
    write_json(output / "summary.json", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("prepare", "verify", "run"))
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-tokens", type=int, default=8192)
    parser.add_argument("--expected-plan-id")
    args = parser.parse_args()
    if args.operation == "prepare":
        if args.source is None:
            parser.error("prepare requires --source")
        result = prepare(args.source, args.root, args.repo, args.max_tokens)
    elif args.operation == "verify":
        result = verify(args.root, args.repo)
    else:
        if args.output is None or args.expected_plan_id is None:
            parser.error("run requires --output and --expected-plan-id")
        result = run(args.root, args.output, args.repo, args.expected_plan_id)
    print(json.dumps({"plan_id": result.get("plan_id"), "status": result.get("status"), "provider_calls_in_prepare": 0 if args.operation != "run" else None}))


if __name__ == "__main__":
    main()
