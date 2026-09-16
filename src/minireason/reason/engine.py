"""Recoverable conjecture, criticism, operative return and use over prose."""
from __future__ import annotations
import json
import os
from pathlib import Path
import time
import uuid
from . import config, prompts
from .adapter import Adapter
from .types import ReasonFailure
from .storage import get, put, read, write, sha, guard, run_lock

CLAIM = "This is a personal working tool. Its output is a working answer with its objections, not a finding."
GOOD_STOPS = {"cycle_budget", "no_new_objections"}


def create_run(problem, cycles, recipe="cross-family", out=None, mode="offline",
               baseline=False, retry_transport=0):
    if not isinstance(problem, str) or not problem.strip():
        raise ValueError("PROBLEM_EMPTY")
    if type(cycles) is not int or not 1 <= cycles <= 9999:
        raise ValueError("CYCLES_INVALID")
    if mode not in {"offline", "live"} or type(retry_transport) is not int or not 0 <= retry_transport <= 99:
        raise ValueError("CONFIG_INVALID")
    from minireason import provider_openai_compat as transport
    if transport.redact_with_names(problem)[1]:
        raise ReasonFailure("SECRET_IN_REQUEST", "Problem contains a declared credential")
    loaded = config.load_recipe(recipe)
    endpoints = config.load_endpoint_snapshot()
    if transport.redact_with_names(loaded["text"])[1]:
        raise ReasonFailure("SECRET_IN_REQUEST", "Recipe contains a declared credential")
    rid = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + "-" + loaded["sha256"][:10] + "-" + uuid.uuid4().hex[:6]
    directory = Path(out) if out is not None else Path("runs") / rid
    # Reserve more than the longest nested provider evidence filename.
    guard(directory / "calls" / "c9999-return" / "a99" / "provider" / ("x" * 65))
    if directory.exists():
        raise ValueError("RUN_EXISTS")
    directory.mkdir(parents=True)
    write(directory / "problem.txt", problem)
    write(directory / "recipe.json", loaded["text"])
    write(directory / "endpoints.json", endpoints["text"])
    put(directory / "config.json", {"schema": "minireason.reason.v1", "run_id": rid,
        "created_epoch": time.time(), "mode": mode, "cycles": cycles,
        "baseline": baseline, "retry_transport": retry_transport,
        "recipe_sha256": loaded["sha256"], "problem_sha256": sha(problem),
        "endpoints_sha256": endpoints["sha256"], "claim_ceiling": CLAIM})
    return directory


def offline_reply(role, cycle, objections):
    """Transparent plumbing fixture; contains no answer to the owner's problem."""
    answer = f"OFFLINE FIXTURE: working answer at cycle {cycle}; no model was contacted."
    if role in {"conjecture", "rival", "baseline"}:
        return {"answer": answer}
    if role == "critic":
        return {"objections": [{"text": f"Fixture objection in cycle {cycle}.",
                                "defeats": "The fixture working answer."}]}
    if role == "return":
        return {"answer": answer, "dispositions": [
            {"id": o["id"], "status": "taken-up", "reason": "Fixture correction incorporated."}
            for o in objections]}
    return {"question": "State the implication tested by this offline fixture.",
            "problem_derivation": "OFFLINE FIXTURE: no substantive derivation from the problem was performed.",
            "working_derivation": "The working answer identifies itself as a fixture; no substantive conclusion follows.",
            "objections": []}


def _validate(directory):
    cfg = get(directory / "config.json")
    for name, key in [("problem.txt", "problem_sha256"), ("recipe.json", "recipe_sha256"),
                      ("endpoints.json", "endpoints_sha256")]:
        if sha(read(directory / name)) != cfg[key]:
            raise ReasonFailure("RUN_INTEGRITY_ERROR", "Saved input hash changed")
    recipe = config.load_recipe(directory / "recipe.json")["data"]
    return cfg, recipe, read(directory / "problem.txt"), get(directory / "endpoints.json")


def _code(exc):
    return getattr(exc, "code", "SCHEMA_FAILURE")


def _call(directory, adapter, cfg, recipe, role, seat, call_id, cycle,
          problem, answer, objections, rival, history, scripted, after_call, native):
    messages = prompts.render(role, problem, answer=answer, objections=objections,
                              rival=rival, history=history)
    cap = recipe["ceilings"]["completion_tokens"]
    attempt, transport_retries, schema_repairs = 0, 0, 0
    while True:
        folder = directory / "calls" / call_id / f"a{attempt:02d}"
        response_path = folder / "response.json"
        request_path = folder / "request.json"
        if request_path.exists():
            intent = get(request_path)
            prepared = intent["prepared"]
            if (intent["role"] != role or intent["seat"] != seat
                    or prepared["messages"] != messages
                    or prepared["kwargs"]["max_tokens"] != cap
                    or intent.get("thinking", native) != native
                    or intent.get("schema_repair", False) != bool(schema_repairs)):
                raise ReasonFailure("RUN_INTEGRITY_ERROR", "Saved call input differs from reconstructed input")
        if response_path.exists():
            if not request_path.exists():
                raise ReasonFailure("RUN_INTEGRITY_ERROR", "Saved response has no request intent")
            saved = get(response_path)
        else:
            if request_path.exists():
                try:
                    recovered = adapter.recover(folder / "provider")
                    if recovered is None:
                        raise ReasonFailure("INTERRUPTED_CALL", "Dispatch outcome unknown; no replay permitted")
                    result = recovered
                except ReasonFailure as exc:
                    if exc.code == "INTERRUPTED_CALL":
                        raise
                    saved = {"epoch": time.time(), "status": _code(exc),
                             "detail": "Recovered provider failure.", "record": exc.record}
                    put(response_path, saved)
                    result = None
            else:
                prepared = adapter.prepare(seat=seat, messages=messages, max_tokens=cap,
                    thinking=native, role=role, coordinate={"call_id": call_id,
                    "cycle": cycle, "attempt": attempt, "schema_repair": bool(schema_repairs)})
                put(request_path, {"epoch": time.time(), "role": role, "seat": seat,
                    "cycle": cycle, "attempt": attempt, "thinking": native,
                    "schema_repair": bool(schema_repairs), "prepared": prepared})
                try:
                    fixture = (scripted or offline_reply)(role, cycle, objections) if cfg["mode"] == "offline" else None
                    if isinstance(fixture, dict) and "content" not in fixture:
                        fixture = {"content": json.dumps(fixture, ensure_ascii=False)}
                    result = adapter.call(seat=seat, messages=messages, records_dir=folder / "provider",
                        max_tokens=cap, thinking=native, role=role,
                        coordinate={"call_id": call_id, "cycle": cycle, "attempt": attempt,
                                    "schema_repair": bool(schema_repairs)}, scripted=fixture)
                except ReasonFailure as exc:
                    saved = {"epoch": time.time(), "status": _code(exc),
                             "detail": "Provider attempt stopped; inspect provider evidence.", "record": exc.record}
                    put(response_path, saved)
                    result = None
            if result is not None:
                try:
                    parsed = prompts.parse(role, result["content"], objections=objections)
                    saved = {"epoch": time.time(), "status": "COMPLETE", "result": result, "parsed": parsed}
                except (ReasonFailure, ValueError, TypeError, KeyError):
                    saved = {"epoch": time.time(), "status": "SCHEMA_FAILURE", "result": result}
                put(response_path, saved)
            if after_call is not None:
                after_call(call_id, saved)
        if saved["status"] == "COMPLETE":
            return saved["parsed"]
        if saved["status"] == "SCHEMA_FAILURE" and schema_repairs == 0:
            messages = prompts.repair(messages, saved["result"]["content"], role)
            schema_repairs = 1
        elif (saved["status"] == "TRANSPORT_OR_RESPONSE_ERROR" and schema_repairs == 0
              and transport_retries < cfg["retry_transport"]):
            transport_retries += 1
        else:
            raise ReasonFailure(saved["status"], "Recorded call did not complete")
        attempt += 1


def _new_objections(items, prefix, cycle, source, all_objections):
    added = []
    for number, item in enumerate(items, 1):
        obj = {"id": f"{prefix}-o{number:03d}", "text": item["text"],
               "defeats": item["defeats"], "source": config.seat_name(source), "born_cycle": cycle,
               "status": "unresolved", "reason": "Awaiting operative return.", "history": [{"cycle": cycle,
                    "status": "unresolved", "reason": "New objection awaiting operative return."}]}
        all_objections.append(obj)
        added.append(obj)
    return added


def _reports(directory, cfg, recipe, state, answer, objections, cycle_notes):
    attempts = sorted((directory / "calls").glob("*/a*")) if (directory / "calls").exists() else []
    state["calls"] = sum((p / "request.json").exists() for p in attempts)
    state["updated_epoch"] = time.time()
    state["objections"] = objections
    put(directory / "state.json", state, replace=True)
    banner = "OFFLINE FIXTURE: no model contacted.\n\n" if cfg["mode"] == "offline" else ""
    open_text = "\n\n## Open objections\n\n"
    pending = [obj for obj in objections if obj["status"] == "unresolved"]
    for obj in pending:
        open_text += f"### {obj['id']}\n\n{obj['text']}\n\nWould defeat: {obj['defeats']}\n\nDisposition: unresolved - {obj['reason']}\n\n"
    if not pending:
        open_text += "No open objection is recorded; this does not establish correctness.\n"
    write(directory / "ANSWER.md", "# Working answer\n\n" + banner +
          (answer or "No working answer was completed.") + open_text + "\n\n" + CLAIM +
          "\n\nStop reason: `" + state["stop_reason"] + "`. Read TRACE.md for open objections.\n", replace=True)
    trace = "# Objection trace\n\n" + CLAIM + "\n\n"
    for obj in objections:
        trace += f"## {obj['id']}\n\nSource: {obj['source']}; introduced cycle {obj['born_cycle']}.\n\n"
        trace += obj["text"] + "\n\nWould defeat: " + obj["defeats"] + "\n\n"
        for entry in obj["history"]:
            trace += f"Cycle {entry['cycle']}: **{entry['status']}** - {entry['reason']}\n\n"
        trace += f"Current disposition: **{obj['status']}** - {obj['reason']}\n\n"
    if not objections:
        trace += "No objection has been recorded. This does not establish correctness.\n"
    write(directory / "TRACE.md", trace, replace=True)
    cap = recipe["ceilings"]["completion_tokens"]
    per_cycle = len(recipe["seats"]["critics"]) + 2 + bool(recipe["seats"].get("rival"))
    bare_count = 1 + bool(config.native_thinking_available(recipe["seats"]["conjecture"])) if cfg["baseline"] else 0
    planned = 1 + cfg["cycles"] * per_cycle + bare_count
    maximum_attempts = planned * (2 + cfg["retry_transport"])
    schema_repairs = 0
    controls = []
    usage = []
    for path in attempts:
        if (path / "request.json").exists():
            intent = get(path / "request.json")
            schema_repairs += bool(intent.get("schema_repair"))
            controls.append({"call": str(path.relative_to(directory)), "seat": intent["seat"],
                             "thinking": intent.get("thinking", intent["prepared"].get("thinking")),
                             "schema_repair": bool(intent.get("schema_repair"))})
        if (path / "response.json").exists():
            try:
                item = get(path / "response.json")
            except ReasonFailure:
                item = {"status": "RUN_INTEGRITY_ERROR"}
            usage.append({"call": str(path.relative_to(directory)), "status": item["status"],
                          "usage": item.get("result", {}).get("usage", item.get("record", {}).get("usage"))})
    run = ("# Personal reasoning run\n\n" + banner + CLAIM + "\n\n" +
           f"Run ID: `{cfg['run_id']}`\n\nRecipe: `{recipe['name']}`; SHA-256 `{cfg['recipe_sha256']}`.\n\n" +
           f"Seats: `{json.dumps(recipe['seats'], ensure_ascii=False)}`\n\n" +
           f"Requested cycles: {cfg['cycles']}; completed cycles: {state['completed_cycles']}.\n\n" +
           f"Recorded call attempts: {state['calls']}; planned logical calls without early stop: {planned}. " +
           f"Completion ceiling per call: {cap}; completion allowance without repair/retry: {planned * cap}. " +
           "Input tokens are additional and depend on problem and growing objection history.\n\n" +
           f"Wall per attempt: 300 seconds; explicit transport retries: {cfg['retry_transport']}.\n\n" +
           f"Schema repair calls: {schema_repairs}; at most one per logical call. Repair attempts are not retried. " +
           f"Maximum attempts including repairs and configured transport retries: {maximum_attempts}; " +
           f"maximum completion allowance: {maximum_attempts * cap}.\n\n" +
           "Thinking and repair setting actually recorded for each attempt:\n\n```json\n" +
           json.dumps(controls, ensure_ascii=False, indent=2) + "\n```\n\n" +
           f"Stop reason: `{state['stop_reason']}`.\n\n" +
           "Baseline outputs, when requested, are in BASELINE.md. Extra loop calls are not matched multi-call controls. " +
           "No comparison is computed. Native support means locally implemented explicit control, not a fresh service capability check.\n\n" +
           "The use reader derives a dependent question separately from the problem and working answer; both derivations can be wrong. " +
           "Review its exact request and response alongside returned objections. Original observations are in calls/. " +
           "Custody checker: minireason.reason.prompts.parse (first JSON object with validated role fields); semantic use checker: the declared use seat. " +
           "JSON validation checks custody fields only and does not decide the legitimacy of prose criticism.\n\n" +
           "Reported usage by attempt (null means unknown):\n\n```json\n" + json.dumps(usage, indent=2) + "\n```\n")
    write(directory / "RUN.md", run, replace=True)
    for number, note in cycle_notes.items():
        write(directory / "cycles" / f"c{number:04d}" / "CYCLE.md", note, replace=True)


def execute(run_dir, *, scripted=None, after_call=None):
    directory = Path(run_dir)
    with run_lock(directory):
        cfg, recipe, problem, endpoints = _validate(directory)
        adapter = Adapter(mode=cfg["mode"], endpoint_snapshot=endpoints)
        seats = recipe["seats"]
        state = {"stop_reason": "running", "completed_cycles": 0, "calls": 0,
                 "mode": cfg["mode"], "run_id": cfg["run_id"]}
        answer, objections, history, cycle_notes = "", [], [], {}
        cycle = 0
        def call(role, seat, cid, current=0, pending=(), rival="", native=None):
            if native is None:
                native = config.thinking_for(seat)
            return _call(directory, adapter, cfg, recipe, role, seat, cid, current,
                         problem, answer, pending, rival, history, scripted, after_call, native)
        try:
            if cfg["mode"] == "live":
                required_seats = [seats["conjecture"], seats["use"], *seats["critics"]]
                if seats.get("rival"):
                    required_seats.append(seats["rival"])
                if any(not os.environ.get(config.endpoint_for(seat, endpoints).key_env) for seat in required_seats):
                    raise ReasonFailure("KEY_MISSING", "One or more required environment keys are absent")
            if cfg["baseline"]:
                baseline_text = "# Baseline readings\n\nSame problem and conjecturer; one call per mode. No computed comparison.\n\n"
                for label, native in [("bare", "off"), ("native", "native")]:
                    if native == "native" and not config.native_thinking_available(seats["conjecture"]):
                        baseline_text += "Native baseline unavailable through the declared adapter control.\n"
                        continue
                    result = call("baseline", seats["conjecture"], "base-" + label, native=native)
                    baseline_text += "## " + label + "\n\n" + result["answer"] + "\n\n"
                    write(directory / "BASELINE.md", baseline_text, replace=True)
            answer = call("conjecture", seats["conjecture"], "initial")["answer"]
            for cycle in range(1, cfg["cycles"] + 1):
                prefix = f"c{cycle:04d}"
                rival = ""
                if seats.get("rival"):
                    rival = call("rival", seats["rival"], prefix + "-rival", cycle, objections)["answer"]
                prior_objections = list(objections)
                new_critic = []
                for index, seat in enumerate(seats["critics"], 1):
                    cid = prefix + f"-k{index:02d}"
                    result = call("critic", seat, cid, cycle, prior_objections, rival=rival)
                    new_critic.extend(_new_objections(result["objections"], cid, cycle, seat, objections))
                pending = [o for o in objections if o["status"] == "unresolved"]
                result = call("return", seats["conjecture"], prefix + "-return", cycle, pending, rival)
                answer = result["answer"]
                lookup = {o["id"]: o for o in pending}
                for disposition in result["dispositions"]:
                    obj = lookup[disposition["id"]]
                    obj.update(status=disposition["status"], reason=disposition["reason"])
                    obj["history"].append({"cycle": cycle, **disposition})
                used = call("use", seats["use"], prefix + "-use", cycle,
                            objections)
                new_use = _new_objections(used["objections"], prefix + "-use", cycle, seats["use"], objections)
                for obj in new_use:
                    obj["history"].append({"cycle": cycle, "status": "unresolved",
                                           "reason": "Use objection awaiting the next operative return."})
                for obj in objections:
                    if not any(entry["cycle"] == cycle for entry in obj["history"]):
                        obj["history"].append({"cycle": cycle, "status": obj["status"],
                                               "reason": "Carried disposition: " + obj["reason"]})
                history.append({"cycle": cycle, "answer": answer,
                                "dispositions": result["dispositions"], "use": used,
                                "objections": [{k: o[k] for k in ("id", "text", "defeats", "status", "reason")} for o in objections]})
                state["completed_cycles"] = cycle
                cycle_notes[cycle] = (f"# Cycle {cycle}\n\nWorking answer after return:\n\n{answer}\n\n" +
                    "Use question:\n\n" + used["question"] + "\n\nIndependent derivation from PROBLEM:\n\n" + used["problem_derivation"] +
                    "\n\nDerivation from WORKING ANSWER:\n\n" + used["working_derivation"] + "\n\n" +
                    "Dispositions and new use objections:\n\n```json\n" +
                    json.dumps({"dispositions": result["dispositions"], "use_objections": new_use}, ensure_ascii=False, indent=2) +
                    "\n```\n\nExact requests and responses: ../../calls/" + prefix + "-*\n")
                if not new_critic and not new_use and not any(o["status"] == "unresolved" for o in objections):
                    state["stop_reason"] = "no_new_objections"
                    break
                _reports(directory, cfg, recipe, state, answer, objections, cycle_notes)
            else:
                state["stop_reason"] = "cycle_budget"
        except ReasonFailure as exc:
            state["stop_reason"] = _code(exc)
            state["failed_cycle"] = cycle
            if cycle:
                cycle_notes[cycle] = f"# Cycle {cycle} stopped\n\nReason: `{state['stop_reason']}`. Partial call evidence is retained in calls/.\n"
        except (KeyboardInterrupt, SystemExit):
            state["stop_reason"] = "interrupted"
            _reports(directory, cfg, recipe, state, answer, objections, cycle_notes)
            raise
        _reports(directory, cfg, recipe, state, answer, objections, cycle_notes)
        return state


def status(run_dir):
    directory = Path(run_dir)
    if (directory / "state.json").exists():
        return get(directory / "state.json")
    cfg = get(directory / "config.json")
    return {"run_id": cfg["run_id"], "stop_reason": "not_started", "completed_cycles": 0, "calls": 0}
