"""Prospective R3-A3 paired route custody; no semantic verdict or extra source."""
from copy import deepcopy
import difflib
import hashlib
import html
import json
from pathlib import Path

from . import prompts
from .storage import get, put, read, write, sha
from .types import ReasonFailure

BRANCHES = (("RETURNED", "R"), ("ARCHIVED", "A"))
PORT_LABELS = {"OPEN AND NEW OBJECTIONS", "PUBLIC SIGNALS"}
LIMIT = "Mechanical field differences are not semantic dependence or a correctness verdict."


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def immutable(path, value):
    if path.exists():
        if canonical(get(path)) != canonical(value):
            raise ReasonFailure("RUN_INTEGRITY_ERROR", "EC01 immutable custody changed: " + path.name)
    else:
        put(path, value)


def ref(directory, path):
    return {"path": path.relative_to(directory).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def envelope(prepared, cfg, recipe):
    return {"endpoint": prepared["endpoint"], "thinking": prepared["thinking"],
            "reasoning_effort": prepared["reasoning_effort"],
            "kwargs": {k: v for k, v in prepared["kwargs"].items() if k != "coordinate"},
            "wall_seconds": prepared["wall_seconds"], "tokenizers": cfg["tokenizers"],
            "prompt_token_cap": cfg["prompt_token_cap"], "attempt_policy": recipe["attempt_policy"]}


def shared_use_task(before):
    claims = [item for item in before.get("claims", [])
              if item.get("relation_id") == "working_position"]
    if len(claims) != 1 or not isinstance(claims[0].get("quote"), str) or not claims[0]["quote"]:
        raise ReasonFailure(
            "RUN_INTEGRITY_ERROR", "EC01 requires one quoted initial working_position claim")
    return {
        "query_id": "ec01-shared-use",
        "question": (
            "Should the original task proceed on this proposed commitment, and what specific "
            "investigation, explanation, or practical decision follows?\n\n"
            "Initial proposed commitment (quoted, not assumed true):\n" + claims[0]["quote"]),
    }


def freeze(directory, cfg, recipe, state, before, objections, signals,
           return_role, blocks, use_template, contracts, adapter, tokenizer_counter):
    """Freeze the complete common parent before either branch's first intent."""
    archived_blocks = [item for item in blocks if item[0] not in PORT_LABELS]
    def render(items):
        return prompts.render_r002(return_role,
            [*items, *contracts.prompt_blocks(return_role, cfg["prompt_contract"])],
            study_profile=cfg["study_profile"], contract_version=cfg["prompt_contract"])
    returned, archived = render(blocks), render(archived_blocks)
    port = "".join("\n\n" + prompts.r002_quote(label, body)
                   for label, body in blocks if label in PORT_LABELS)
    body, empty = returned[1]["content"], archived[1]["content"]
    start = body.find(port)
    if (not port or start < 0 or body[:start] + body[start + len(port):] != empty
            or returned[0] != archived[0]):
        raise ReasonFailure("RUN_INTEGRITY_ERROR", "EC01 prompts are not one exact objection-port deletion")
    removed = port.encode("utf-8")
    difference = {"schema": "minireason.r003.ec01-prompt-difference.v1",
        "removed_block": port, "removed_labels": [label for label, _ in blocks if label in PORT_LABELS],
        "utf8_start": len(body[:start].encode("utf-8")),
        "utf8_end": len(body[:start].encode("utf-8")) + len(removed),
        "removed_utf8_bytes": len(removed), "removed_sha256": sha(port),
        "returned_user_sha256": sha(body), "archived_user_sha256": sha(empty),
        "system_sha256": sha(returned[0]["content"]),
        "declaration": "ARCHIVED = RETURNED with this single UTF-8 span deleted; no replacement text."}
    prepared = {}
    wires = {}
    for branch, messages in (("RETURNED", returned), ("ARCHIVED", archived)):
        seat = recipe["seats"]["return"]
        request = adapter.prepare(seat=seat, messages=messages, max_tokens=32768,
                                  thinking=seat["thinking"], role=return_role)
        from .r002_preflight import token_preflight
        if tokenizer_counter is None:
            admission = token_preflight(messages, seat["endpoint"], pins=cfg["tokenizers"],
                mode=cfg["mode"], limit=cfg["prompt_token_cap"],
                wire_body_text=request["wire_body_text"], condition=cfg["condition"], role=return_role)
        else:
            admission = tokenizer_counter(messages, seat["endpoint"], pins=cfg["tokenizers"],
                mode=cfg["mode"], limit=cfg["prompt_token_cap"])
        wires[branch] = request["wire_body_text"]
        prepared[branch] = {"messages": messages, "wire_body_sha256": request["wire_body_sha256"],
                            "envelope": envelope(request, cfg, recipe), "preflight": admission}
    wire_port = json.dumps(port)[1:-1]
    wire_start = wires["RETURNED"].find(wire_port)
    if (wire_start < 0 or wires["RETURNED"][:wire_start]
            + wires["RETURNED"][wire_start + len(wire_port):] != wires["ARCHIVED"]):
        raise ReasonFailure("RUN_INTEGRITY_ERROR", "EC01 wire differs beyond escaped objection span")
    difference["wire"] = {"removed_block": wire_port,
        "utf8_start": len(wires["RETURNED"][:wire_start].encode("utf-8")),
        "removed_utf8_bytes": len(wire_port.encode("utf-8")), "removed_sha256": sha(wire_port),
        "returned_sha256": sha(wires["RETURNED"]), "archived_sha256": sha(wires["ARCHIVED"])}
    if prepared["RETURNED"]["envelope"] != prepared["ARCHIVED"]["envelope"]:
        raise ReasonFailure("RUN_INTEGRITY_ERROR", "EC01 return envelopes differ")
    custody = []
    for call_id in ("initial", "c0001-signal-a", "c0001-signal-b"):
        call_root = directory / "calls" / call_id
        for path in sorted(item for item in call_root.rglob("*") if item.is_file()):
            item = {"source": ref(directory, path)}
            if call_id != "initial":
                copy = directory / "archive" / call_id / path.relative_to(call_root)
                original = read(path)
                if copy.exists():
                    if copy.read_bytes() != path.read_bytes():
                        raise ReasonFailure("RUN_INTEGRITY_ERROR", "EC01 archive bytes changed")
                else:
                    write(copy, original)
                item["archive"] = ref(directory, copy)
            custody.append(item)
    immutable(directory / "archive/c0001-objections.json", objections)
    task = shared_use_task(before)
    common = {"before_answer": before, "shared_use_task": task,
              "shared_use_task_sha256": sha(canonical(task)), "use_template": use_template,
              "return_without_objections": archived, "seats": recipe["seats"],
              "resource_envelope": prepared["RETURNED"]["envelope"]}
    parent = {"schema": "minireason.r003.ec01-parent.v1", "cycle": 1,
        "run_id": cfg["run_id"], "problem_id": cfg["problem_id"], "state": deepcopy(state),
        "inputs": cfg["inputs"], "before_answer": before, "objections": objections,
        "critic_outputs": signals, "source_custody": custody, "identical_inputs": common,
        "identical_inputs_sha256": sha(canonical(common)), "return_requests": prepared,
        "objection_archive": ref(directory, directory / "archive/c0001-objections.json"),
        "shared_use_task": task, "shared_use_task_sha256": sha(canonical(task)),
        "branch_order": [item[0] for item in BRANCHES],
        "continuation_branch": "RETURNED", "semantic_limit": LIMIT}
    immutable(directory / "ec01/parent.json", parent)
    immutable(directory / "ec01/prompt-difference.json", difference)
    return parent, archived_blocks


def call_record(directory, call_id, parsed=None):
    attempts = []
    for path in sorted((directory / "calls" / call_id).glob("a*/request.json")):
        response_path = path.with_name("response.json")
        response = get(response_path) if response_path.exists() else {}
        request = get(path)
        attempts.append({"attempt": path.parent.name, "request": ref(directory, path),
            "response": ref(directory, response_path) if response_path.exists() else None,
            "wire_body_sha256": request["prepared"]["wire_body_sha256"],
            "status": response.get("status", "INTERRUPTED_CALL")})
    return {"call_id": call_id, "status": attempts[-1]["status"] if attempts else "not-run",
            "parsed": parsed, "attempts": attempts,
            "request": attempts[-1]["request"] if attempts else None,
            "response": attempts[-1]["response"] if attempts else None}


def compare(directory, records):
    projections = {}
    for branch, record in records.items():
        returned = record["return"]["parsed"]
        used = record["use"]["parsed"]
        projections[branch] = {
            "return": {key: returned.get(key) for key in
                ("decision", "answer", "claims", "derivation_steps", "changes")} if returned else None,
            "use": {key: used.get(key) for key in
                ("decision", "question", "before", "after", "dependency")} if used else None}
    complete = all(r["status"] == "COMPLETE" for r in records.values())
    left, right = (json.dumps(projections[b], ensure_ascii=False, sort_keys=True, indent=2)
                   for b, _ in BRANCHES)
    difference = {"schema": "minireason.r003.ec01-comparison.v1",
        "parent_state_sha256": records["RETURNED"]["parent_state_sha256"],
        "identical_inputs_sha256": records["RETURNED"]["identical_inputs_sha256"],
        "paired_delivery_complete": complete,
        "shared_use_task": records["RETURNED"]["shared_use_task"],
        "shared_use_task_sha256": records["RETURNED"]["shared_use_task_sha256"],
        "projections": projections,
        "mechanical_decisive_commitment_diff": "".join(difflib.unified_diff(
            left.splitlines(keepends=True), right.splitlines(keepends=True),
            fromfile="RETURNED", tofile="ARCHIVED")),
        "fields_equal": projections["RETURNED"] == projections["ARCHIVED"] if complete else None,
        "semantic_limit": LIMIT + " Claims and derivation steps are a declared projection; which commitments are decisive requires reading."}
    immutable(directory / "ec01/comparison.json", difference)
    return difference


def execute_pair(directory, cfg, recipe, state, before, active, signals,
                 return_role, return_blocks, use_blocks, contracts, adapter,
                 tokenizer_counter, call, relation, fork):
    from .r002 import _apply_dispositions, _mint, _check_unique_ids, detect_tail_edit
    task = shared_use_task(before)
    template = use_blocks(None, task)
    parent, archived_blocks = freeze(directory, cfg, recipe, state, before, active, signals,
        return_role, return_blocks, template, contracts, adapter, tokenizer_counter)
    parent_hash = ref(directory, directory / "ec01/parent.json")["sha256"]
    records = {}
    for branch, short in BRANCHES:
        supplied = deepcopy(active) if branch == "RETURNED" else []
        returned = used = None
        failure = None
        return_id, use_id = f"c0001-{short}-return", f"c0001-{short}-use"
        try:
            returned = call(return_role, recipe["seats"]["return"], return_id, 1,
                return_blocks if branch == "RETURNED" else archived_blocks,
                before=deepcopy(before), objections=supplied)
            _apply_dispositions(supplied, returned["dispositions"], 1)
            used = call("propagation_use", recipe["seats"]["use"], use_id, 1,
                use_blocks(returned, task), before=deepcopy(before), answer=returned,
                objections=[], checker_eligible=False, fork=fork,
                prior_objections=deepcopy(supplied), expected_use_task=deepcopy(task))
            new_items = deepcopy(used["objections"])
            for item in new_items:
                item["_source_call"] = use_id
                item["_source_endpoint"] = recipe["seats"]["use"]["endpoint"]
            minted = _mint(new_items, use_id, 1, "use")
            _check_unique_ids(supplied, minted)
            supplied.extend(minted)
        except ReasonFailure as exc:
            failure = {"code": exc.code, "detail": exc.detail}
        record = {"schema": "minireason.r003.ec01-branch.v1", "branch_id": branch,
            "cycle": 1, "parent_state_sha256": parent_hash,
            "parent": ref(directory, directory / "ec01/parent.json"),
            "identical_inputs_sha256": parent["identical_inputs_sha256"],
            "shared_use_task": task, "shared_use_task_sha256": parent["shared_use_task_sha256"],
            "delivered_objection_ids": [o["id"] for o in active] if branch == "RETURNED" else [],
            "archived_objection_ids": [o["id"] for o in active] if branch == "ARCHIVED" else [],
            "archive": parent["objection_archive"],
            "return": call_record(directory, return_id, returned),
            "use": call_record(directory, use_id, used),
            "status": failure["code"] if failure else "COMPLETE", "failure": failure,
            "objections": supplied,
            "tail_edits": sum(detect_tail_edit(before, returned, d)
                              for d in returned["dispositions"]) if returned else 0,
            "continuation": "main cycles 2-3 and closing under existing stop rules" if branch == "RETURNED"
                            else "ends after cycle-1 use", "semantic_limit": LIMIT}
        immutable(directory / "ec01" / (branch + ".json"), record)
        immutable(directory / "episodes/ec01" / (branch + ".json"), record)
        records[branch] = record
    difference = compare(directory, records)
    immutable(directory / "episodes/ec01/comparison.json", difference)
    state["ec01"] = {"parent_state_sha256": parent_hash,
        "identical_inputs_sha256": parent["identical_inputs_sha256"],
        "branches": {b: records[b]["status"] for b, _ in BRANCHES},
        "comparison": ref(directory, directory / "ec01/comparison.json")}
    if records["RETURNED"]["failure"]:
        failure = records["RETURNED"]["failure"]
        raise ReasonFailure(failure["code"], failure["detail"])
    return records["RETURNED"]


def reading_view(directory):
    """Same custody-only paired view for TRACE, RUN and EPISODES."""
    parent_path = directory / "ec01/parent.json"
    if not parent_path.exists():
        return ""
    parent = get(parent_path)
    values = {branch: get(directory / "ec01" / (branch + ".json"))
              if (directory / "ec01" / (branch + ".json")).exists() else {"status": "pending"}
              for branch, _ in BRANCHES}
    comparison = directory / "ec01/comparison.json"
    def cell(value):
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False, sort_keys=True)
        return html.escape(str(value if value is not None else "")).replace("|", "&#124;").replace("\n", "<br>")

    def parsed(branch, stage):
        return values[branch].get(stage, {}).get("parsed") or {}

    def ref_hash(branch, stage, kind):
        return (values[branch].get(stage, {}).get(kind) or {}).get("sha256", "")

    returned_use, archived_use = parsed("RETURNED", "use"), parsed("ARCHIVED", "use")
    body = ("\n## EC01 cycle-1 paired route\n\n"
        "| Field | RETURNED | ARCHIVED |\n|---|---|---|\n"
        f"| Parent state SHA-256 | {ref(directory, parent_path)['sha256']} | same |\n"
        f"| Identical inputs SHA-256 | {parent['identical_inputs_sha256']} | same |\n"
        f"| Shared use task SHA-256 | {parent['shared_use_task_sha256']} | same |\n"
        f"| Shared use question | {cell(parent['shared_use_task']['question'])} | same |\n"
        f"| Status | {values['RETURNED']['status']} | {values['ARCHIVED']['status']} |\n"
        f"| Delivered objection IDs | {cell(values['RETURNED'].get('delivered_objection_ids', []))} | {cell(values['ARCHIVED'].get('delivered_objection_ids', []))} |\n"
        f"| Archived objection IDs | {cell(values['RETURNED'].get('archived_objection_ids', []))} | {cell(values['ARCHIVED'].get('archived_objection_ids', []))} |\n"
        "| Objection port | delivered | absent; records in archive/ |\n"
        f"| Return answer | {cell(parsed('RETURNED', 'return').get('answer'))} | {cell(parsed('ARCHIVED', 'return').get('answer'))} |\n"
        f"| Use question | {cell(returned_use.get('question'))} | {cell(archived_use.get('question'))} |\n"
        f"| Use after conclusion | {cell((returned_use.get('after') or {}).get('conclusion'))} | {cell((archived_use.get('after') or {}).get('conclusion'))} |\n"
        f"| Use dependency | {cell((returned_use.get('dependency') or {}).get('explanation'))} | {cell((archived_use.get('dependency') or {}).get('explanation'))} |\n"
        f"| Return request SHA-256 | {ref_hash('RETURNED', 'return', 'request')} | {ref_hash('ARCHIVED', 'return', 'request')} |\n"
        f"| Return response SHA-256 | {ref_hash('RETURNED', 'return', 'response')} | {ref_hash('ARCHIVED', 'return', 'response')} |\n"
        f"| Use request SHA-256 | {ref_hash('RETURNED', 'use', 'request')} | {ref_hash('ARCHIVED', 'use', 'request')} |\n"
        f"| Use response SHA-256 | {ref_hash('RETURNED', 'use', 'response')} | {ref_hash('ARCHIVED', 'use', 'response')} |\n"
        "| Continuation | main schedule | ends after cycle-1 use |\n\n"
        "Order: RETURNED then ARCHIVED. Exact removed UTF-8 span: `ec01/prompt-difference.json`. "
        + LIMIT + "\n\nFull branch results and request/response custody:\n\n```json\n"
        + json.dumps(values, ensure_ascii=False, sort_keys=True, indent=2) + "\n```\n")
    if comparison.exists():
        body += "\nMechanical comparison:\n\n```json\n" + read(comparison) + "```\n"
    return body
