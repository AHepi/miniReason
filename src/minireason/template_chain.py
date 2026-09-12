"""Freeze one construction episode's exact public outputs for a distinct inquiry.

This coordinator makes no provider calls. Its portable Git tree proof binds the
retained parent evidence to the publisher's independently verified tree. Hashes
establish byte custody, never semantic standing or the merit of a promotion.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import tempfile
from typing import Any

from creib.forge.mini.log import BlobStore, replay
from creib.strict_json import loads_strict
from minireason.inquiry_study import (ARMS, STAGES, _canonical, _material,
    _output_occurrence, _settings, _signed, _snapshots, _verify, _verify_occurrence,
    load_frozen, stage_prompt, text_hash, validate_response)
from minireason.inquiry_data import STAGE_INSTRUCTIONS
from minireason.language_data import RAW_SYSTEM, INSTRUCTIONS
from minireason.language_study import selected_language
from minireason.provider import digest, write_new
from minireason.successor_data import template_contract


def construction_contract() -> dict[str, Any]:
    return {"schema": "minireason.template-contract.v1",
        "template_id": "joint_construction_v1", "cycles": 1,
        "stages": list(STAGES), "stage_instructions": dict(STAGE_INSTRUCTIONS),
        "system_message": RAW_SYSTEM,
        "input_contract": "whole frozen packet, carrier, issue and parents; all actual earlier stage outputs",
        "automatic_successor_started": False}


def _semantic_contract(value: dict[str, Any]) -> dict[str, Any]:
    return {key: item for key, item in value.items() if key not in {"template_id", "contract_id"}}


def _mapping() -> list[dict[str, str]]:
    return ([{"source": key, "destination": "handoff", "meaning": "exact supplied bytes only"}
        for key in ("packet_text", "selected_language_text", "issue_text", "parent_material_text")]
        + [{"source": stage, "destination": "handoff", "meaning": "complete actual public occurrence"}
           for stage in STAGES])


def make_chain_plan(chain_id: str, a_plan: dict[str, Any], b_test_id: str,
                    allocation_reason: str, *, b_contract: dict[str, Any] | None = None,
                    b_settings: dict[str, Any] | None = None,
                    b_arms: list[str] | None = None) -> dict[str, Any]:
    value = {"schema": "minireason.template-chain-plan.v1", "chain_id": chain_id,
        "a_plan": a_plan, "a_contract": construction_contract(),
        "a_selection": {"arm": "mini", "repeat": 1}, "required_stages": list(STAGES),
        "b_contract": template_contract() if b_contract is None else b_contract,
        "b_test_id": b_test_id,
        "b_settings": a_plan["settings"] if b_settings is None else b_settings,
        "b_arms": list(ARMS) if b_arms is None else b_arms, "b_repetitions": 1,
        "b_input_mapping": _mapping(), "allocation_reason": allocation_reason,
        "automatic_successor_started": False, "standing_effect": "none"}
    signed = _signed(value, "chain_plan_id")
    verify_chain_plan(signed)
    return signed


def verify_chain_plan(chain: dict[str, Any]) -> None:
    _verify(chain, "chain_plan_id")
    if chain.get("schema") != "minireason.template-chain-plan.v1":
        raise ValueError("CHAIN_PLAN_REQUIRED")
    a, b, plan = chain["a_contract"], chain["b_contract"], chain["a_plan"]
    if a.get("template_id") == b.get("template_id") or _semantic_contract(a) == _semantic_contract(b):
        raise ValueError("DISTINCT_TEMPLATES_REQUIRED")
    if a != construction_contract() or b != template_contract():
        raise ValueError("UNREGISTERED_TEMPLATE_CONTRACT")
    _verify(plan, "plan_id")
    _verify(plan["packet"], "packet_id")
    _verify(plan["packet"]["corpus"], "corpus_id")
    if (plan.get("schema") != "minireason.inquiry-plan.v1"
            or plan.get("template_id") != a["template_id"]
            or plan.get("stage_instructions") != a["stage_instructions"]
            or plan.get("cycles") != 1 or plan.get("repetitions") != 1
            or "mini" not in plan.get("arms", []) or plan.get("carrier") != "prose"):
        raise ValueError("A_TEMPLATE_OR_EXECUTION_CONTRACT_CHANGED")
    packet_id = plan["packet"]["packet_id"]
    if plan["packet_id"] != packet_id:
        raise ValueError("A_PACKET_CHANGED")
    _verify_occurrence(plan["issue"], packet_id)
    for parent in plan["parents"]:
        _verify_occurrence(parent, packet_id)
    expected_material = {"packet_text": _canonical(plan["packet"]),
        "selected_language_text": selected_language(plan["packet"], plan["carrier"]),
        "issue_text": _canonical({"occurrence": plan["issue"], "activation": plan["activation"]}),
        "parent_material_text": _canonical(plan["parents"]),
        "carrier_directive": INSTRUCTIONS["carrier_directives"][plan["carrier"]]}
    if any(plan[key] != value for key, value in expected_material.items()):
        raise ValueError("A_MATERIAL_CHANGED")
    if (chain.get("a_selection") != {"arm": "mini", "repeat": 1}
            or chain.get("required_stages") != list(STAGES)
            or chain.get("b_input_mapping") != _mapping()
            or chain.get("b_repetitions") != 1
            or chain.get("automatic_successor_started") is not False
            or chain.get("standing_effect") != "none"):
        raise ValueError("CHAIN_SELECTION_OR_MAPPING_CHANGED")
    if any(type(chain.get(key)) is not str or not chain[key].strip()
           for key in ("chain_id", "b_test_id", "allocation_reason")):
        raise ValueError("CHAIN_ID_AND_ALLOCATION_REQUIRED")
    if chain["b_test_id"] == plan["test_id"]:
        raise ValueError("SEPARATE_EPISODE_IDS_REQUIRED")
    arms = chain["b_arms"]
    if not arms or len(arms) != len(set(arms)) or not set(arms) <= set(ARMS):
        raise ValueError("INVALID_B_ARMS")
    for arm in arms:
        _settings(chain["b_settings"], arm)
    # A default settings object describes disabled thinking; each arm controls its mode.
    if chain["b_settings"] != _settings(chain["b_settings"], "mini").to_dict():
        raise ValueError("B_SETTINGS_METADATA_CHANGED")


def _git(repo: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def _git_id(kind: str, raw: bytes) -> str:
    return hashlib.sha1(f"{kind} {len(raw)}\0".encode() + raw).hexdigest()


def _tree_entries(raw: bytes) -> dict[str, tuple[str, str]]:
    entries, pos = {}, 0
    while pos < len(raw):
        end = raw.index(b"\0", pos)
        mode, name = raw[pos:end].split(b" ", 1)
        if end + 21 > len(raw):
            raise ValueError("INVALID_GIT_TREE")
        decoded = name.decode("utf-8")
        if decoded in entries or decoded in {".", ".."} or "/" in decoded:
            raise ValueError("INVALID_GIT_TREE_ENTRY")
        entries[decoded] = (mode.decode("ascii"), raw[end + 1:end + 21].hex())
        pos = end + 21
    return entries


def _safe_path(path: str) -> tuple[str, ...]:
    value = PurePosixPath(path)
    if not path or not value.parts or value.is_absolute() or str(value) != path or any(p in {".", ".."} for p in value.parts):
        raise ValueError("UNSAFE_EVIDENCE_PATH")
    return value.parts


def _prove_file(repo: Path, tree: str, path: str, trees: dict[str, str]) -> str:
    parts = _safe_path(path)
    for index, part in enumerate(parts):
        raw = _git(repo, "cat-file", "tree", tree)
        if _git_id("tree", raw) != tree:
            raise ValueError("GIT_TREE_IDENTITY_CHANGED")
        trees[tree] = base64.b64encode(raw).decode("ascii")
        mode, child = _tree_entries(raw)[part]
        if index == len(parts) - 1:
            if mode not in {"100644", "100755"}:
                raise ValueError("REGULAR_EVIDENCE_FILE_REQUIRED")
            return child
        if mode != "40000":
            raise ValueError("GIT_TREE_PATH_REQUIRED")
        tree = child
    raise ValueError("EVIDENCE_PATH_REQUIRED")


def _verify_tree_file(trees: dict[str, str], tree: str, path: str, raw: bytes) -> None:
    parts = _safe_path(path)
    for index, part in enumerate(parts):
        obj = base64.b64decode(trees[tree], validate=True)
        if _git_id("tree", obj) != tree:
            raise ValueError("PUBLISHED_TREE_PROOF_CHANGED")
        mode, child = _tree_entries(obj)[part]
        if index == len(parts) - 1:
            if mode not in {"100644", "100755"} or child != _git_id("blob", raw):
                raise ValueError("PUBLISHED_FILE_PROOF_CHANGED")
        elif mode != "40000":
            raise ValueError("PUBLISHED_DIRECTORY_PROOF_CHANGED")
        tree = child


def _read(evidence: dict[str, str], path: str) -> dict[str, Any]:
    value = loads_strict(evidence[path])
    if type(value) is not dict:
        raise ValueError("EVIDENCE_OBJECT_REQUIRED")
    return value


def _inspect_parent(chain: dict[str, Any], files: dict[str, str]) -> dict[str, Any]:
    plan, arm = chain["a_plan"], "mini-r01"
    if _read(files, "plan.json") != plan:
        raise ValueError("PARENT_PLAN_CHANGED")
    summary, result = _read(files, "summary.json"), _read(files, arm + "/result.json")
    preflight = _read(files, "preflight.json")
    if (preflight != summary.get("preflight")
            or preflight.get("status") != "CONFIGURATION_PREFLIGHT_PASSED"
            or preflight.get("model_calls") != 0
            or preflight.get("material_snapshots") != _snapshots(plan)):
        raise ValueError("PARENT_PREFLIGHT_CHANGED")
    selected = [row for row in summary["arms"] if row["arm"] == "mini" and row["repeat"] == 1]
    if (summary.get("plan_id") != plan["plan_id"]
            or summary.get("test_id") != plan["test_id"]
            or summary["preflight"].get("status") != "CONFIGURATION_PREFLIGHT_PASSED"
            or len(selected) != 1 or selected[0]["status"] != "OBSERVATIONS_RECORDED"
            or result.get("status") != "OBSERVATIONS_RECORDED" or result.get("alarms") != []
            or result.get("plan_id") != plan["plan_id"] or result.get("packet_id") != plan["packet_id"]
            or result.get("arm") != "mini" or result.get("repeat") != 1
            or result.get("settings") != _settings(plan["settings"], "mini").to_dict()
            or result.get("resources", {}).get("calls") != 4
            or selected[0].get("resources") != result.get("resources")):
        raise ValueError("PARENT_COMPLETION_OR_COORDINATE_CHANGED")
    expected_calls = {f"{arm}/calls/call-{index:04d}.{kind}.json"
        for index in range(1, 5) for kind in ("request", "response")}
    if {path for path in files if path.startswith(arm + "/calls/")} != expected_calls:
        raise ValueError("PARENT_CALL_RECORD_SET_CHANGED")
    history = result["history"]
    if [row.get("stage") for row in history] != list(STAGES):
        raise ValueError("PARENT_REQUIRED_STAGES_CHANGED")
    route = _read(files, arm + "/inquiry-result.json")
    if (route.get("status") != "COMPLETE" or route.get("alarms") != []
            or route.get("mini_outcome", {}).get("cycles_completed") != 1
            or route.get("mini_outcome", {}).get("calls") != 4
            or [row.get("stage") for row in route["history"]] != list(STAGES)):
        raise ValueError("PARENT_MINI_ROUTE_INCOMPLETE")
    usage = {"calls": 4, "prompt_tokens": 0, "completion_tokens": 0}
    from minireason.inquiry_mini import _STAGE_KINDS, prepare_inquiry
    with tempfile.TemporaryDirectory(prefix="minireason-handoff-") as temp:
        root = Path(temp)
        prepared = prepare_inquiry(root / "prepared", **_material(plan))
        if (files[arm + "/manifest.json"].encode() != prepared.manifest_bytes
                or _read(files, arm + "/material-bindings.json") != prepared.summary()
                or result.get("prepared_bindings") != prepared.summary()
                or preflight.get("mini") != prepared.summary()):
            raise ValueError("PARENT_PREPARED_MATERIAL_CHANGED")
        for source in prepared.source_files:
            if files[arm + "/" + source.path].encode() != source.raw:
                raise ValueError("PARENT_MINI_SOURCE_CHANGED")
        for path, raw in files.items():
            if path.startswith(arm + "/run/"):
                destination = root / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(raw.encode("utf-8"))
        header = _read(files, arm + "/run/run-header.json")
        if header != prepared.plan.header:
            raise ValueError("PARENT_RUN_HEADER_CHANGED")
        state = replay(root / arm / "run/log.jsonl", prepared.plan.genesis)
        if not state.ended:
            raise ValueError("PARENT_MINI_LOG_NOT_ENDED")
        events = [loads_strict(line) for line in files[arm + "/run/log.jsonl"].splitlines()]
        stage_events = [event for event in events if event["type"] == "STAGE_ENTERED"]
        entered = [stage["stage_id"] for stage in prepared.manifest["stages"] if not stage.get("end")]
        if (events[0]["type"] != "RUN_STARTED" or events[-1]["type"] != "RUN_ENDED"
                or sum(event["type"] == "RUN_ENDED" for event in events) != 1
                or [event["stage_id"] for event in stage_events] != entered
                or any(event["cycle"] != 1 for event in stage_events)
                or route["mini_outcome"].get("stages_entered") != entered
                or route["mini_outcome"].get("genesis") != prepared.plan.genesis
                or route["mini_outcome"].get("state_digest") != state.digest()
                or any(event["type"] in {"FORMAT_FAILURE", "REFUSED", "SUBMISSION_DROPPED",
                    "BUDGET_REFUSED", "PORT_EMPTY"} for event in events)
                or sum(artifact["kind_id"] in _STAGE_KINDS.values() for artifact in state.artifacts.values()) != 4):
            raise ValueError("PARENT_MINI_EXECUTION_CHANGED")
        blobs = BlobStore(root / arm / "run/blobs")
        for artifact in state.artifacts.values():
            blobs.get(artifact["body_ref"])
            blobs.get(artifact["commitments_ref"])
        for index, row in enumerate(history):
            stage = STAGES[index]
            _verify_occurrence(row, plan["packet_id"])
            if (row != _read(files, f"{arm}/{stage}.artifact.json")
                    or row != _output_occurrence(plan, "mini", 1, route["history"][index], history[:index])):
                raise ValueError("PARENT_OCCURRENCE_CHANGED")
            artifact = state.artifacts[row["artifact_id"]]
            if (artifact["kind_id"] != _STAGE_KINDS[stage] or artifact["cycle"] != 1
                    or blobs.get(artifact["body_ref"]).decode("utf-8") != row["text"]
                    or blobs.get(artifact["commitments_ref"]).decode("utf-8") != row["text"]):
                raise ValueError("PARENT_MINI_ARTIFACT_CHANGED")
            stem = f"{arm}/calls/call-{index + 1:04d}"
            request, response = _read(files, stem + ".request.json"), _read(files, stem + ".response.json")
            expected_request = {"model": plan["settings"]["model"],
                "messages": [{"role": "system", "content": RAW_SYSTEM},
                             {"role": "user", "content": stage_prompt(plan, stage, history[:index])}],
                "stream": False, "max_tokens": plan["settings"]["max_tokens"],
                "thinking": {"type": "disabled"}}
            expected_coordinate = {"stage": stage, "cycle": 1, "phase": "raw-prose", "mini_kind": _STAGE_KINDS[stage]}
            if (request.get("request") != expected_request
                    or request.get("request_sha256") != digest(expected_request)
                    or request.get("coordinate") != expected_coordinate
                    or request.get("settings") != result["settings"]
                    or any(response.get(key) != value for key, value in request.items())
                    or response.get("status") != "COMPLETE" or response.get("finish_reason") != "stop"
                    or response.get("returned_model") != plan["settings"]["model"]
                    or response.get("reasoning_content_present") is not False
                    or response.get("reasoning_content_persisted") is not False
                    or validate_response(response, plan["settings"]["max_tokens"]) != row["text"]):
                raise ValueError("PARENT_PUBLIC_RESPONSE_OR_REQUEST_CHANGED")
            for key in ("prompt_tokens", "completion_tokens"):
                usage[key] += response["usage"][key]
    if usage != result["resources"]:
        raise ValueError("PARENT_RESOURCE_TOTALS_CHANGED")
    queue = _read(files, arm + "/inquiry-queue.json")
    if queue.get("occurrences") != [history[-1]] or queue.get("automatic_successor_started") is not False:
        raise ValueError("PARENT_PROMOTION_QUEUE_CHANGED")
    return {**{key: plan[key] for key in ("packet", "packet_text", "selected_language_text",
        "issue", "issue_text", "parents", "parent_material_text")}, "occurrences": history}


def freeze_handoff(chain_path: Path, parent_root: Path, repository: Path,
                   publication: dict[str, Any]) -> dict[str, Any]:
    """Create a self-contained handoff only from the exact published Git bytes.

    The caller/publisher has already verified remote_commit -> tree_sha. Local
    Git checks and the portable Merkle proof independently establish file bytes.
    This function cannot itself attest that a remote reference still points there.
    """
    repo, chain_path, parent_root = repository.resolve(), chain_path.resolve(), parent_root.resolve()
    chain = load_frozen(chain_path)
    verify_chain_plan(chain)
    _verify_publication(publication)
    if _git(repo, "rev-parse", publication["local_commit"] + "^{tree}").decode().strip() != publication["tree_sha"]:
        raise ValueError("LOCAL_PUBLICATION_TREE_CHANGED")
    chain_rel = chain_path.relative_to(repo).as_posix()
    parent_rel = parent_root.relative_to(repo).as_posix()
    paths = [parent_root / name for name in ("plan.json", "summary.json", "preflight.json")]
    paths += sorted(path for path in (parent_root / "mini-r01").rglob("*") if path.is_file())
    files, trees = {}, {}
    for path in [chain_path] + paths:
        if path.is_symlink():
            raise ValueError("REGULAR_EVIDENCE_FILE_REQUIRED")
        relative = path.relative_to(repo).as_posix()
        raw = path.read_bytes()
        blob = _prove_file(repo, publication["tree_sha"], relative, trees)
        if blob != _git_id("blob", raw):
            raise ValueError("UNPUBLISHED_PARENT_BYTES")
        if path != chain_path:
            files[path.relative_to(parent_root).as_posix()] = raw.decode("utf-8")
    source_files = {}
    for relative in chain["a_plan"]["source"]["files"]:
        _safe_path(relative)
        path = repo / relative
        if path.is_symlink() or not path.is_file():
            raise ValueError("REGULAR_SOURCE_FILE_REQUIRED")
        raw = path.read_bytes()
        if _prove_file(repo, publication["tree_sha"], relative, trees) != _git_id("blob", raw):
            raise ValueError("UNPUBLISHED_SOURCE_BYTES")
        source_files[relative] = raw.decode("utf-8")
    source_evidence = {"files": source_files,
        "sha256": {path: text_hash(raw) for path, raw in source_files.items()}}
    _verify_source_evidence(chain, source_evidence, trees, publication["tree_sha"])
    material = _inspect_parent(chain, files)
    value = {"schema": "minireason.template-handoff.v1", "chain_plan": chain,
        "chain_file": {"path": chain_rel, "text": chain_path.read_bytes().decode("utf-8")},
        "parent_record_path": parent_rel, "publication": publication, "git_tree_objects": trees,
        "evidence": {"files": files, "sha256": {path: text_hash(raw) for path, raw in files.items()}},
        "source_evidence": source_evidence, "material": material, "mapping": chain["b_input_mapping"],
        "automatic_successor_started": False, "content_appraisal": "unresolved", "standing_effect": "none"}
    result = _signed(value, "handoff_id")
    verify_handoff(result)
    return result


def _verify_publication(publication: dict[str, Any]) -> None:
    for key in ("remote_commit", "local_commit", "tree_sha"):
        raw = publication.get(key)
        if type(raw) is not str or len(raw) != 40 or any(char not in "0123456789abcdef" for char in raw):
            raise ValueError("PUBLICATION_GIT_ID_REQUIRED")
    if publication.get("remote_verified") is not True:
        raise ValueError("PUBLISHER_REMOTE_VERIFICATION_REQUIRED")


def _verify_source_evidence(chain: dict[str, Any], evidence: dict[str, Any],
                            trees: dict[str, str], tree: str) -> None:
    declared = chain["a_plan"]["source"]
    files = evidence["files"]
    actual = {path: text_hash(raw) for path, raw in files.items()}
    if (not files or actual != declared["files"] or evidence.get("sha256") != actual
            or declared.get("source_sha256") != digest(declared["files"])):
        raise ValueError("PARENT_DECLARED_SOURCE_CHANGED")
    for path, raw in files.items():
        _verify_tree_file(trees, tree, path, raw.encode("utf-8"))


def verify_handoff(handoff: dict[str, Any]) -> None:
    _verify(handoff, "handoff_id")
    if handoff.get("schema") != "minireason.template-handoff.v1":
        raise ValueError("HANDOFF_REQUIRED")
    verify_chain_plan(handoff["chain_plan"])
    _verify_publication(handoff["publication"])
    files, trees = handoff["evidence"]["files"], handoff["git_tree_objects"]
    if handoff["evidence"]["sha256"] != {path: text_hash(raw) for path, raw in files.items()}:
        raise ValueError("HANDOFF_EVIDENCE_CHANGED")
    tree, prefix = handoff["publication"]["tree_sha"], handoff["parent_record_path"]
    _safe_path(prefix)
    _verify_source_evidence(handoff["chain_plan"], handoff["source_evidence"], trees, tree)
    for path, raw in files.items():
        _safe_path(path)
        _verify_tree_file(trees, tree, prefix + "/" + path, raw.encode("utf-8"))
    chain_file = handoff["chain_file"]
    _verify_tree_file(trees, tree, chain_file["path"], chain_file["text"].encode("utf-8"))
    if loads_strict(chain_file["text"]) != handoff["chain_plan"]:
        raise ValueError("PUBLISHED_CHAIN_PLAN_CHANGED")
    if (handoff.get("mapping") != handoff["chain_plan"]["b_input_mapping"]
            or handoff.get("material") != _inspect_parent(handoff["chain_plan"], files)
            or handoff.get("automatic_successor_started") is not False
            or handoff.get("standing_effect") != "none"
            or handoff.get("content_appraisal") != "unresolved"):
        raise ValueError("HANDOFF_PARENT_OR_MAPPING_CHANGED")


def render_handoff(handoff: dict[str, Any]) -> str:
    """Render each original public text in full once; omit custody proof metadata."""
    material = handoff["material"]
    parts = ["Frozen original packet:\n" + material["packet_text"],
        "Selected frozen carrier:\n" + material["selected_language_text"],
        "Selected occurrence and original allocation:\n" + material["issue_text"],
        "Frozen original parent material:\n" + material["parent_material_text"]]
    for row in material["occurrences"]:
        parts.append(f"Actual A {row['stage']} occurrence [{row['occurrence_id']}]:\n" + row["text"])
    return "\n\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    declaration = commands.add_parser("plan")
    declaration.add_argument("--id", required=True)
    declaration.add_argument("--a-plan", type=Path, required=True)
    declaration.add_argument("--b-id", required=True)
    declaration.add_argument("--allocation-reason", required=True)
    declaration.add_argument("--output", type=Path, required=True)
    freeze = commands.add_parser("freeze-handoff")
    freeze.add_argument("--chain-plan", type=Path, required=True)
    freeze.add_argument("--parent-record", type=Path, required=True)
    freeze.add_argument("--repository", type=Path, required=True)
    freeze.add_argument("--publication", type=Path, required=True)
    freeze.add_argument("--output", type=Path, required=True)
    verify = commands.add_parser("verify-handoff")
    verify.add_argument("--handoff", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "plan":
        write_new(args.output, make_chain_plan(args.id, load_frozen(args.a_plan),
            args.b_id, args.allocation_reason))
    elif args.command == "freeze-handoff":
        write_new(args.output, freeze_handoff(args.chain_plan, args.parent_record,
            args.repository, load_frozen(args.publication)))
    else:
        verify_handoff(load_frozen(args.handoff))
    print("Offline custody operation completed; no model call or semantic standing change occurred.")


if __name__ == "__main__":
    main()
