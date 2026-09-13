"""H001: a Codex-Luna exercise of Mini's pure rendering/routing boundary.

This does not execute the durable scheduler or the DeepSeek provider contract.
"""
from __future__ import annotations
import argparse
from dataclasses import replace
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.run_sql_use_return import PortableRepositoryPath, study
from creib.forge.mini.common import digest_bytes
from creib.forge.mini.executor import Request
from creib.forge.mini.kinds import read_submission
from creib.forge.mini.log import ARTIFACT_SUBMITTED, MiniState, apply_event, build_event
from creib.forge.mini.runner import _store_artifact, empty_artifact_ports, render_brief

FROZEN = Path("experiments/plans/E028-sql-use-return")
PLAN_ID = "0e7ada3e11b348b7c3ea46805910ece3e14fdb700975e6a22b58b44c82569b5f"
MODEL = "gpt-5.6-luna"
COORDINATES = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3), 5: (1, 2), 6: (1, 3)}
SOURCE_CALLS = ({0: 1, 1: 2, 2: 3, 3: 4}, {0: 1, 1: 2, 2: 5, 3: 6})


def write_new(path, value):
    raw = value if isinstance(value, bytes) else study.base.encoded(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(raw)


def load_json(path):
    return json.loads(path.read_bytes())


class MemoryBlobs:
    """Only a renderer fixture; no filesystem durability is being exercised."""
    def __init__(self):
        self.values = {}
    def put(self, raw):
        key = digest_bytes(raw)
        self.values[key] = raw
        return key
    def get(self, key):
        return self.values[key]


def verified(repo):
    plan = study.verify(repo / FROZEN, repo)
    if plan["plan_id"] != PLAN_ID:
        raise ValueError("FROZEN_PLAN_CHANGED")
    return plan


def initialize(repo, output):
    plan = verified(repo)
    if output.exists():
        raise FileExistsError("HARNESS_OUTPUT_EXISTS")
    source = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    write_new(output / "plan.json", {
        "schema": "minireason.harness.luna-routing.v1", "status": "PREPARED",
        "created_utc": datetime.now(timezone.utc).isoformat(), "source_commit": source,
        "frozen_plan_id": PLAN_ID, "candidate_sha256": plan["candidate_sha256"],
        "system_sha256": plan["system_sha256"], "requested_model": MODEL,
        "probe_sha256": digest_bytes(Path(__file__).read_bytes()),
        "max_participant_sessions": 6, "internal_model_calls": None, "usage": None,
        "session_waves": [[1], [2], [3, 5], [4, 6]], "automatic_retries": 0,
        "root_is_only_reviewer": True, "participant_context": "fresh, no inherited turns",
        "exercised": ["frozen compilation", "submission parser", "artifact identity", "event reducer", "brief renderer", "E028 routed_messages"],
        "not_exercised": ["durable scheduler", "filesystem durability", "DeepSeek provider", "native toggle", "matched scientific comparison"],
        "host_differences": "Codex instructions/tools remain; original manifest budgets are not enforced by the subagent interface; unknown usage is not zero",
        "classification": "Harness exercise only; not an E028 continuation or semantic certificate"})


def check_probe(output):
    plan = load_json(output / "plan.json")
    if plan["probe_sha256"] != digest_bytes(Path(__file__).read_bytes()):
        raise ValueError("PROBE_CHANGED_AFTER_PREPARATION")
    return plan


def checked_request(output, call):
    request = load_json(output / f"requests/{call:04d}.json")
    packet = load_json(output / f"packets/{call:04d}.json")
    if (request["messages_sha256"] != study.base.digest(request["messages"])
            or packet != {"messages": request["messages"]}):
        raise ValueError("PARTICIPANT_PACKET_CHANGED")
    return request

def answer(output, call):
    raw = (output / f"responses/{call:04d}.txt").read_bytes()
    receipt = load_json(output / f"responses/{call:04d}.json")
    request = checked_request(output, call)
    if receipt["request_messages_sha256"] != request["messages_sha256"]:
        raise ValueError("RESPONSE_REQUEST_CHANGED")
    if digest_bytes(raw) != receipt["text_sha256"]:
        raise ValueError("RESPONSE_BYTES_CHANGED")
    text = raw.decode("utf-8")
    if not text.strip():
        raise ValueError("EMPTY_PUBLIC_RESPONSE")
    return text


def render(repo, output, arm_index, stage_index):
    verified(repo)
    arm = study.ARMS[arm_index]
    manifest_path = repo / FROZEN / "manifests" / (arm + ".json")
    manifest = load_json(manifest_path)
    compiled = study.base.compile_manifest(manifest_path)
    state, blobs, answers = MiniState(), MemoryBlobs(), {}
    previous = compiled.genesis
    for prior_index in range(stage_index):
        prior = study.STAGES[prior_index]
        text = answer(output, SOURCE_CALLS[arm_index][prior_index])
        stage = compiled.stage(prior)
        kind = compiled.kinds[stage.kind_id]
        submission = read_submission(json.dumps({"body": text, "commitments": text}, ensure_ascii=False), kind, "both")
        if compiled.formats[kind.kind_id].failures(submission.as_fields(), ("body", "commitments")):
            raise ValueError("SUBMISSION_FORMAT_FAILED")
        artifact, body, commitments = _store_artifact(blobs, stage, submission, prior_index)
        event = build_event(seq=prior_index, prev=previous, type=ARTIFACT_SUBMITTED,
            payload={"seat": "model", "completion_tokens": 0}, cycle=1,
            stage_id=prior, kind_id=stage.kind_id, artifact_id=artifact,
            body_ref=body, commitments_ref=commitments)
        # Zero is only a reducer-fixture counter, never a participant usage receipt.
        apply_event(state, event)
        previous = event.event_id
        if blobs.get(body) != text.encode("utf-8") or blobs.get(commitments) != text.encode("utf-8"):
            raise ValueError("PUBLIC_PROSE_CUSTODY_FAILED")
        answers[prior] = text
    stage = compiled.stage(study.STAGES[stage_index])
    if empty_artifact_ports(compiled, state, stage, 1):
        raise ValueError("MISSING_RENDERED_PARENT")
    brief, exposed = render_brief(compiled, state, blobs, stage, 1)
    if exposed:
        raise ValueError("UNEXPECTED_EVIDENCE_EXPOSURE")
    request = Request(stage.stage_id, stage.kind_id, 0, brief, 1, "both", ())
    system = (repo / FROZEN / "system.txt").read_bytes().decode("utf-8")
    messages, parents = study.routed_messages(request, manifest, arm, answers, system)
    return {"arm": arm, "stage": stage.stage_id, "messages": messages,
            "mini_brief": brief, "parent_stages": parents,
            "input_ports": study.stage_ports(arm, stage.stage_id)}, (request, manifest, answers, system)


def make_request(repo, output, call):
    check_probe(output)
    arm_index, stage_index = COORDINATES[call]
    route, _ = render(repo, output, arm_index, stage_index)
    record = {**route, "call_id": call, "schema": "minireason.harness.request.v1",
        "messages_sha256": study.base.digest(route["messages"]),
        "requested_model": MODEL, "classification": "Codex participant packet; not a DeepSeek request"}
    write_new(output / f"requests/{call:04d}.json", record)
    write_new(output / f"packets/{call:04d}.json", {"messages": route["messages"]})
    return output / f"packets/{call:04d}.json"


def record_answer(output, call, source, agent_id):
    check_probe(output)
    request = checked_request(output, call)
    raw = source.read_bytes()
    if not raw.decode("utf-8").strip():
        raise ValueError("EMPTY_PUBLIC_RESPONSE")
    if any((output / f"responses/{call:04d}.{ext}").exists() for ext in ("txt", "json")):
        raise FileExistsError("RESPONSE_ALREADY_EXISTS")
    write_new(output / f"responses/{call:04d}.txt", raw)
    write_new(output / f"responses/{call:04d}.json", {
        "schema": "minireason.harness.response.v1", "call_id": call,
        "agent_id": agent_id, "requested_model": MODEL,
        "received_utc": datetime.now(timezone.utc).isoformat(),
        "request_messages_sha256": request["messages_sha256"],
        "text_sha256": digest_bytes(raw), "utf8_bytes": len(raw),
        "usage": None, "internal_model_calls": None, "provider_finish_reason": None,
        "classification": "Public answer from a fresh Codex subagent; semantic appraisal belongs to root"})


def check_all(repo, output):
    check_probe(output)
    routes = {(arm, stage): render(repo, output, arm, stage)[0] for arm in (0, 1) for stage in range(4)}
    for call, coordinate in COORDINATES.items():
        request = checked_request(output, call)
        route = routes[coordinate]
        if request["messages"] != route["messages"] or request["mini_brief"] != route["mini_brief"]:
            raise ValueError("REQUEST_OR_PARENT_CHANGED")
        answer(output, call)
    if any(routes[(0, stage)]["messages"] != routes[(1, stage)]["messages"] for stage in (0, 1)):
        raise ValueError("SHARED_PREFIX_CHANGED")
    return {"schema": "minireason.harness.summary.v1", "status": "ROUTING_EXERCISE_COMPLETE",
            "participant_sessions": 6, "rendered_stage_deliveries": 8, "reused_prefix_deliveries": 2,
            "shared_prefix_messages_equal": True, "actual_internal_model_calls": None, "usage": None,
            "full_scheduler_qualified": False, "DeepSeek_experiment_completed": False,
            "semantic_appraisal": "Separate root review required",
            "routes": [{"arm": arm, "stage": stage, "ports": route["input_ports"],
                        "messages_sha256": study.base.digest(route["messages"])} for (arm, stage), route in routes.items()]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("init", "request", "record", "check"))
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--call", type=int, choices=range(1, 7))
    parser.add_argument("--answer", type=Path)
    parser.add_argument("--agent-id")
    args = parser.parse_args()
    repo = PortableRepositoryPath(args.repo.resolve())
    if args.action == "init":
        initialize(repo, args.output)
    elif args.action == "request":
        print(make_request(repo, args.output, args.call))
    elif args.action == "record":
        record_answer(args.output, args.call, args.answer, args.agent_id)
    else:
        result = check_all(repo, args.output)
        write_new(args.output / "summary.json", result)
        print(json.dumps(result))


if __name__ == "__main__":
    main()
