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
    """Return each logical call's latest attempt, preferring a completed repair."""
    result = {}
    for path in sorted((directory / "calls").glob("*/a*/response.json")):
        response = get(path)
        request_path = path.with_name("request.json")
        call_id = path.parent.parent.name
        attempt = {"response": response, "parsed": response.get("parsed"),
                   "request": get(request_path) if request_path.exists() else {},
                   "response_ref": _ref(directory, path), "request_ref": _ref(directory, request_path),
                   "attempt": path.parent.name}
        prior = result.get(call_id)
        if prior is None or response.get("status") == "COMPLETE" or prior["response"].get("status") != "COMPLETE":
            result[call_id] = attempt
    return result

def write_episode_records(directory, cfg, objections):
    directory = Path(directory)
    calls = _calls(directory)
    if cfg["condition"] == "LOOP-DECOMPOSED":
        initial = (calls.get("initial") or {}).get("parsed") or {}
        plan = {item["step"]: item for item in initial.get("plan", [])}
        for cycle in range(1, cfg["cycles"] + 1):
            return_id = f"c{cycle:04d}-return"
            returned = calls.get(return_id)
            critic_id, use_id = f"c{cycle:04d}-critic", f"c{cycle:04d}-use"
            step_id = "initial" if cycle == 1 else f"c{cycle:04d}-step"
            started = [calls.get(name) for name in (step_id, critic_id, return_id, use_id)]
            if not plan.get(cycle) or not any(started):
                continue
            step_number = cycle
            use = calls.get(use_id)
            parsed_return = returned.get("parsed") if returned else None
            step_call, critic_call = calls.get(step_id), calls.get(critic_id)
            parsed_step = ((step_call or {}).get("parsed") or {}).get("first_step") if cycle == 1 \
                else (step_call or {}).get("parsed")
            accepted = bool(parsed_return and parsed_return.get("decision") == "answered" and use
                            and use.get("parsed", {}).get("decision") == "answered"
                            and use.get("parsed", {}).get("status") == "agrees")
            step_record = {"schema": "minireason.r002.decomposed-step-custody.v1",
                "step_record_id": f"{cfg['problem_id']}/{cfg['condition']}/{cfg['run_id']}/step-{step_number}",
                "problem_id": cfg["problem_id"],
                "condition": cfg["condition"], "cycle": cycle, "step": step_number,
                "plan_step": plan.get(step_number),
                "step_request": (step_call or {}).get("request_ref"),
                "step_response": (step_call or {}).get("response_ref"),
                "critic_request": (critic_call or {}).get("request_ref"),
                "critic_response": (critic_call or {}).get("response_ref"),
                "return_request": returned.get("request_ref") if returned else None,
                "return_response": returned.get("response_ref") if returned else None,
                "step_status": (step_call or {}).get("response", {}).get("status"),
                "critic_status": (critic_call or {}).get("response", {}).get("status"),
                "return_status": (returned or {}).get("response", {}).get("status"),
                "before_step": parsed_step,
                "returned_step": ({key: parsed_return.get(key)
                                   for key in ("decision", "missing_derivation", "derivation", "result")}
                                  if parsed_return else None),
                "status": "returned" if parsed_return else "incomplete",
                "semantic_reading": "structural acceptance does not establish bearing, validity or correctness"}
            step_folder = directory / "steps" / f"step-{step_number:04d}"
            _immutable(step_folder / "record.json", step_record)
            if use:
                step_supplement = {"schema": "minireason.r002.decomposed-step-use.v1",
                    "step_record": _ref(directory, step_folder / "record.json"),
                    "use_request": use.get("request_ref"), "use_response": use.get("response_ref"),
                    "use_status": use.get("response", {}).get("status"), "use": use.get("parsed"),
                    "accepted_step": ({"step": step_number, "goal": plan[step_number]["goal"],
                        "depends_on": plan[step_number]["depends_on"],
                        "derivation": parsed_return["derivation"], "result": parsed_return["result"]}
                        if accepted else None),
                    "assembly_status": "step_chain_present" if accepted else "incomplete",
                    "semantic_reading": step_record["semantic_reading"]}
                _immutable(step_folder / "use.json", step_supplement)

            dispositions = {item["id"]: item for item in (parsed_return or {}).get("dispositions", [])}
            for objection in [item for item in objections
                              if item.get("born_cycle") == cycle and item.get("source") == "decomposed-critic"]:
                ident = objection["id"]
                disposition = dispositions.get(ident)
                record = {"schema": "minireason.r002.decomposed-episode.v1",
                    "episode_id": f"{cfg['problem_id']}/{cfg['condition']}/{cfg['run_id']}/{ident}",
                    "record_id": return_id, "problem_id": cfg["problem_id"],
                    "condition": cfg["condition"], "cycle": cycle, "step": step_number,
                    "objection_id": ident, "target_claim": objection["target_claim"],
                    "fork": objection["fork"], "objection_text": objection["text"],
                    "source": objection["source"], "source_call": objection.get("source_call"),
                    "source_lineage": objection.get("source_lineage"), "check": objection.get("check"),
                    "redo": disposition.get("redo") if disposition else None,
                    "disposition": disposition, "before_step": parsed_step,
                    "after_step": ({key: parsed_return.get(key) for key in ("step", "derivation", "result")}
                                   if parsed_return else None),
                    "return_request": returned.get("request_ref") if returned else None,
                    "return_response": returned.get("response_ref") if returned else None,
                    "assembly_status": "closed_without_use" if disposition else "incomplete",
                    "semantic_reading": "artifact custody does not establish bearing, validity, uptake or correctness"}
                folder = directory / "episodes" / ident
                _immutable(folder / (return_id + ".json"), record)
                if use:
                    supplement = {"schema": "minireason.r002.decomposed-episode-use.v1",
                        "episode_id": record["episode_id"],
                        "disposition_record": _ref(directory, folder / (return_id + ".json")),
                        "use_request": use.get("request_ref"), "use_response": use.get("response_ref"),
                        "use": use.get("parsed"),
                        "assembly_status": "step_chain_present" if accepted else "incomplete",
                        "semantic_reading": record["semantic_reading"]}
                    _immutable(folder / (return_id + "-use.json"), supplement)
        return
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
    requests = sorted((directory / "calls").glob("*/a*/request.json"))
    logical_calls = len({path.parent.parent.name for path in requests})
    state.update(run_id=cfg["run_id"], calls=logical_calls, attempts=len(requests),
                 objections=objections, updated_epoch=time.time())
    if "detail" in state:
        state["stop_detail"] = state["detail"]
    usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "unknown_attempts": 0,
             "unknown_by_field": {key: 0 for key in ("prompt_tokens", "completion_tokens", "total_tokens")}}
    settings = []
    for path in requests:
        intent = get(path); prepared = intent["prepared"]
        call_id = path.parent.parent.name
        response_path = path.with_name("response.json")
        attempt_response = get(response_path) if response_path.exists() else {}
        reported = _usage(attempt_response)
        if not reported:
            usage["unknown_attempts"] += 1
        for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
            if type(reported.get(key)) is int:
                usage[key] += reported[key]
            else:
                usage["unknown_by_field"][key] += 1
        settings.append({"call": call_id, "attempt": path.parent.name,
                         "schema_repair": bool(intent.get("schema_repair")), "seat": intent["seat"],
                         "thinking": prepared["thinking"], "reasoning_effort": prepared["reasoning_effort"],
                         "completion_tokens": prepared["kwargs"]["max_tokens"], "wall_seconds": prepared["wall_seconds"],
                         "endpoint": prepared["endpoint"], "status": attempt_response.get("status"),
                         "usage": reported or None, "request": _ref(directory, path),
                         "response": _ref(directory, response_path)})
    state["usage"] = usage
    write_episode_records(directory, cfg, objections)
    state["episode_records"] = len(list((directory / "episodes").glob("*/*.json"))) if (directory / "episodes").exists() else 0
    put(directory / "state.json", state, replace=True)
    banner = "OFFLINE FIXTURE: no model contacted.\n\n" if cfg["mode"] == "offline" else ""
    public_answer = (answer or {}).get("answer")
    if not public_answer and cfg["condition"] == "LOOP-DECOMPOSED" and state.get("accepted_steps"):
        public_answer = "Accepted partial steps (no synthesis):\n\n" + "\n".join(
            f"{item['step']}. {item['result']}" for item in state["accepted_steps"])
    text = "# Working answer\n\n" + banner + (public_answer or "No public answer was completed.")
    open_items = [obj for obj in objections if obj["status"] == "unresolved"]
    if open_items:
        text += "\n\nOpen objections:\n\n" + "\n".join("- " + obj["id"] + ": " + obj["text"] for obj in open_items)
    write(directory / "ANSWER.md", text + f"\n\nStop reason: `{state['stop_reason']}`.\n", replace=True)
    study_label = "R003" if cfg.get("study_profile") == "r003-open-v1" else "R002"
    trace = f"# {study_label} objection trace\n\n" + banner
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
    recipe = get(directory / "recipe.json") if (directory / "recipe.json").exists() else {}
    ceilings = recipe.get("ceilings", {})
    default_call_ceiling = 1 if not recipe else (13 if cfg["condition"] == "LOOP-DECOMPOSED" else 14)
    call_ceiling = ceilings.get("logical_calls", default_call_ceiling)
    attempt_ceiling = ceilings.get("attempts", call_ceiling)
    default_allowance = 32768 if not recipe else None
    base_allowance = ceilings.get("base_completion_tokens_total",
                                  ceilings.get("completion_tokens_total", default_allowance))
    maximum_allowance = ceilings.get("completion_tokens_total", base_allowance)
    critic_ceiling = ceilings.get("critic_completion_tokens", ceilings.get("off_completion_tokens", 16384))
    ceiling_text = (f"native 32768; STEP/use 16384; critics {critic_ceiling}"
                    if cfg["condition"] == "LOOP-DECOMPOSED" else "native 32768; off 16384")
    attempted_repair_calls = sorted({path.parent.parent.name for path in requests
                                       if get(path).get("schema_repair")})
    complete_calls = sorted(call_id for call_id, item in calls.items()
                            if item.get("response", {}).get("status") == "COMPLETE")
    successful_repaired_calls = sorted(call_id for call_id, item in calls.items()
                                       if item.get("response", {}).get("status") == "COMPLETE"
                                       and item.get("attempt") != "a00")
    failed_repair_calls = sorted(set(attempted_repair_calls) - set(successful_repaired_calls))
    without_repair = sorted(set(complete_calls) - set(successful_repaired_calls))
    repairs = len(attempted_repair_calls)
    policy = ("one initial attempt plus at most one schema repair per logical call; zero fallbacks/transport retries; "
              "CEILING_HIT receives no repair" if recipe.get("attempt_policy", {}).get("schema_repairs") == 1
              else "one attempt, zero repairs/fallbacks/retries")
    run = (f"# {study_label} run\n\n" + banner + f"Run: `{cfg['run_id']}`. Condition: `{cfg['condition']}`.\n\n"
           f"Calls/attempts: {state['calls']}/{state['attempts']}. Schema repairs: {repairs}. Strict policy: {policy}.\n\n"
           f"Ceilings: {ceiling_text}; prompt 32768; wall 300 seconds per attempt; "
           f"at most {call_ceiling} logical calls and {attempt_ceiling} attempts. "
           f"Base/max completion allowance: {base_allowance}/{maximum_allowance}.\n\n"
           f"Reached by repair: `{json.dumps(successful_repaired_calls)}`. "
           f"Reached without repair: `{json.dumps(without_repair)}`. "
           f"Repair attempted but not completed: `{json.dumps(failed_repair_calls)}`.\n\n"
           f"Completed cycles: {state['completed_cycles']}. Closing return: {state['closing_return']}.\n\n"
           f"Tail edits: {state['tail_edits']}. Stall switches: {state['stall_switches']}. Checker runs: {state['checker_runs']}. "
           f"Cannot-decide responses: {state['cannot_decide_responses']}.\n\n"
           f"Episode records/supplements: {state['episode_records']}.\n\n"
           f"Reported usage (known portions only): `{json.dumps(usage, sort_keys=True)}`. Unknown usage is not zero.\n\n"
           f"Stop reason: `{state['stop_reason']}`. {state.get('stop_detail', '')}\n\n"
           "Schema, counter and episode assembly success is custody evidence, not a score or correctness verdict.\n\n"
           "## Actual request controls and reported usage\n\n```json\n" + json.dumps(settings, ensure_ascii=False, indent=2, sort_keys=True) + "\n```\n")
    write(directory / "RUN.md", run, replace=True)
