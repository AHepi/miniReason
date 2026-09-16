"""R002 reading views and immutable custody links; no semantic adjudication."""
from pathlib import Path
import hashlib
import json
import time
from .storage import get, put, write
from .types import ReasonFailure


def _digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _ref(directory, path):
    return {"path": path.relative_to(directory).as_posix(), "sha256": _digest(path)} if path.is_file() else None


def _immutable(path, record):
    if path.exists():
        if get(path) != record:
            raise ReasonFailure("RUN_INTEGRITY_ERROR", "Immutable episode custody changed")
    else:
        put(path, record)


def _calls(directory):
    result = {}
    for path in sorted((directory / "calls").glob("*/a00/response.json")):
        response = get(path)
        request_path = path.with_name("request.json")
        result[path.parent.parent.name] = {"response": response, "parsed": response.get("parsed"),
            "request": get(request_path) if request_path.exists() else {},
            "response_ref": _ref(directory, path), "request_ref": _ref(directory, request_path)}
    return result


def write_episode_records(directory, cfg, objections):
    directory = Path(directory)
    calls = _calls(directory)
    before = (calls.get("initial") or {}).get("parsed") or {}
    returns = sorted(name for name in calls if name.endswith("-return") and name != "closing-return")
    if "closing-return" in calls:
        returns.append("closing-return")
    for call_id in returns:
        call = calls[call_id]
        after = call["parsed"]
        if not isinstance(after, dict):
            continue
        dispositions = {item["id"]: item for item in after.get("dispositions", [])}
        for objection in objections:
            ident = objection["id"]
            if ident not in dispositions:
                continue
            disposition = dispositions[ident]
            from .r002 import detect_tail_edit
            host_path = Path(objection["host_execution"]) / "execution.json" if objection.get("host_execution") else None
            relation_ids = [item["relation_id"] for item in before.get("claims", [])
                            if item["relation_id"] == objection["target_claim"] or
                            item.get("quote", "") in objection["fork"]["step_quote"]]
            record = {"schema": "minireason.r002.episode.v1",
                "episode_id": f"{cfg['problem_id']}/{cfg['condition']}/{cfg['run_id']}/{ident}",
                "record_id": call_id, "problem_id": cfg["problem_id"], "condition": cfg["condition"],
                "cycle": call["request"].get("cycle"), "objection_id": ident,
                "target_claim": objection["target_claim"], "relation_ids": relation_ids,
                "fork": objection["fork"], "objection_text": objection["text"],
                "source": objection["source"], "source_call": objection.get("source_call"),
                "source_lineage": objection.get("source_lineage"),
                "check": objection.get("check"), "redo": disposition.get("redo"),
                "disposition": disposition, "tail_edit": detect_tail_edit(before, after, disposition),
                "before": {key: before.get(key) for key in ("answer", "claims", "derivation_steps")},
                "after": {key: after.get(key) for key in ("answer", "claims", "derivation_steps")},
                "changes": after.get("changes", []), "return_request": call["request_ref"],
                "return_response": call["response_ref"],
                "host_check_execution": _ref(directory, host_path) if host_path else None,
                "assembly_status": "closed_without_propagation" if call_id == "closing-return" else "open",
                "semantic_reading": "unresolved; artifact custody does not establish bearing, validity, uptake or correctness"}
            folder = directory / "episodes" / ident
            _immutable(folder / (call_id + ".json"), record)
            use_id = call_id.removesuffix("-return") + "-use"
            use = calls.get(use_id)
            if call_id != "closing-return" and use and use.get("parsed"):
                parsed = use["parsed"]
                supplement = {"schema": "minireason.r002.episode-use.v1", "episode_id": record["episode_id"],
                    "disposition_record": _ref(directory, folder / (call_id + ".json")),
                    "use_request": use["request_ref"], "use_response": use["response_ref"],
                    "query_id": parsed.get("query_id"), "question": parsed.get("question"),
                    "problem_derivation": parsed.get("problem_derivation"),
                    "before_evaluation": parsed.get("before"), "after_evaluation": parsed.get("after"),
                    "dependency": parsed.get("dependency"),
                    "assembly_status": "incomplete" if parsed.get("decision") == "cannot_decide" else "slot_chain_present",
                    "semantic_reading": record["semantic_reading"]}
                _immutable(folder / (call_id + "-use.json"), supplement)
        before = after


def _usage(response):
    for container in (response.get("result", {}), response.get("record", {})):
        if isinstance(container, dict):
            value = container.get("usage")
            if isinstance(value, dict) and value:
                return value
    return {}


def reports(directory, cfg, state, answer, objections, events):
    directory = Path(directory)
    calls = _calls(directory)
    requests = sorted((directory / "calls").glob("*/a00/request.json"))
    state.update(run_id=cfg["run_id"], calls=len(requests), attempts=len(requests),
                 objections=objections, updated_epoch=time.time())
    if "detail" in state:
        state["stop_detail"] = state["detail"]
    usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "unknown_attempts": 0,
             "unknown_by_field": {key: 0 for key in ("prompt_tokens", "completion_tokens", "total_tokens")}}
    settings = []
    for path in requests:
        intent = get(path); prepared = intent["prepared"]
        call_id = path.parent.parent.name
        reported = _usage(calls.get(call_id, {}).get("response", {}))
        if not reported:
            usage["unknown_attempts"] += 1
        for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
            if type(reported.get(key)) is int:
                usage[key] += reported[key]
            else:
                usage["unknown_by_field"][key] += 1
        settings.append({"call": call_id, "seat": intent["seat"],
                         "thinking": prepared["thinking"], "reasoning_effort": prepared["reasoning_effort"],
                         "completion_tokens": prepared["kwargs"]["max_tokens"], "wall_seconds": prepared["wall_seconds"],
                         "endpoint": prepared["endpoint"],
                         "usage": reported or None, "request": _ref(directory, path)})
    state["usage"] = usage
    write_episode_records(directory, cfg, objections)
    state["episode_records"] = len(list((directory / "episodes").glob("*/*.json"))) if (directory / "episodes").exists() else 0
    put(directory / "state.json", state, replace=True)
    banner = "OFFLINE FIXTURE: no model contacted.\n\n" if cfg["mode"] == "offline" else ""
    text = "# Working answer\n\n" + banner + ((answer or {}).get("answer") or "No public answer was completed.")
    open_items = [obj for obj in objections if obj["status"] == "unresolved"]
    if open_items:
        text += "\n\nOpen objections:\n\n" + "\n".join("- " + obj["id"] + ": " + obj["text"] for obj in open_items)
    write(directory / "ANSWER.md", text + f"\n\nStop reason: `{state['stop_reason']}`.\n", replace=True)
    trace = "# R002 objection trace\n\n" + banner
    for obj in objections:
        fork = obj["fork"]
        trace += (f"## {obj['id']}\n\nTarget step: {fork['step_index']} - {fork['step_quote']}\n\n"
                  f"Source: {obj['source']}; lineage: {obj.get('source_lineage', 'see call records')}.\n\n"
                  f"Check carried: {'yes' if obj.get('check') else 'no'}; check redone: {obj.get('check_redone', 'not-redone')}; "
                  f"host run: {'yes' if obj.get('host_execution') else 'no'}.\n\n"
                  f"Disposition: **{obj['status']}** - {obj['reason']}\n\n")
        for item in obj.get("history", []):
            phase = item.get("phase", "cycle " + str(item["cycle"]))
            trace += f"- {phase}: **{item['status']}**" + (" (carried)" if item.get("carried") else "") + ": " + item["reason"] + "\n"
        trace += "\n"
    for event in events:
        trace += f"## {event['event']}\n\n```json\n{json.dumps(event, ensure_ascii=False, indent=2, sort_keys=True)}\n```\n\n"
    if not objections and not events:
        trace += "No objection or stall-switch event was recorded.\n"
    write(directory / "TRACE.md", trace, replace=True)
    run = ("# R002 run\n\n" + banner + f"Run: `{cfg['run_id']}`. Condition: `{cfg['condition']}`.\n\n"
           f"Calls/attempts: {state['calls']}/{state['attempts']}. Strict policy: one attempt, zero repairs/fallbacks/retries.\n\n"
           "Ceilings: native 32768; off 16384; prompt 32768; wall 300 seconds per call; at most 14 loop calls.\n\n"
           f"Completed cycles: {state['completed_cycles']}. Closing return: {state['closing_return']}.\n\n"
           f"Tail edits: {state['tail_edits']}. Stall switches: {state['stall_switches']}. Checker runs: {state['checker_runs']}. "
           f"Cannot-decide responses: {state['cannot_decide_responses']}.\n\n"
           f"Episode records/supplements: {state['episode_records']}.\n\n"
           f"Reported usage (known portions only): `{json.dumps(usage, sort_keys=True)}`. Unknown usage is not zero.\n\n"
           f"Stop reason: `{state['stop_reason']}`. {state.get('stop_detail', '')}\n\n"
           "Schema, counter and episode assembly success is custody evidence, not a score or correctness verdict.\n\n"
           "## Actual request controls and reported usage\n\n```json\n" + json.dumps(settings, ensure_ascii=False, indent=2, sort_keys=True) + "\n```\n")
    write(directory / "RUN.md", run, replace=True)
