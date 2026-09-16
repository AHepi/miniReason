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
RESILIENCE_POLICY = "reasoning-exposure-v2"
RESILIENT_POLICIES = {"native-off-v1", RESILIENCE_POLICY}
UNAVAILABLE_CODES = {"CEILING_HIT", "TRANSPORT_OR_RESPONSE_ERROR", "SCHEMA_FAILURE"}


def _completion_tokens(cfg, recipe, thinking):
    # Old runs reconstruct the exact ceilings frozen under their original policy.
    if cfg.get("resilience_policy") == RESILIENCE_POLICY:
        return config.completion_tokens_for(recipe, thinking)
    key = ("native_completion_tokens"
           if cfg.get("resilience_policy") == "native-off-v1" and thinking == "native"
           else "completion_tokens")
    return recipe["ceilings"][key]


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
    guard(directory / "calls" / "c9999-closing-return" / "a99" / "provider" / ("x" * 65))
    if directory.exists():
        raise ValueError("RUN_EXISTS")
    directory.mkdir(parents=True)
    write(directory / "problem.txt", problem)
    write(directory / "recipe.json", loaded["text"])
    write(directory / "endpoints.json", endpoints["text"])
    put(directory / "config.json", {"schema": "minireason.reason.v1", "run_id": rid,
        "created_epoch": time.time(), "mode": mode, "cycles": cycles,
        "baseline": baseline, "retry_transport": retry_transport,
        "resilience_policy": RESILIENCE_POLICY,
        "prompt_contract": prompts.CURRENT_CONTRACT,
        "closing_return": loaded["data"].get("closing_return", False),
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
    contract = cfg.get("prompt_contract", "legacy-v1")
    messages = prompts.render(role, problem, answer=answer, objections=objections,
                              rival=rival, history=history, contract_version=contract)
    resilient = cfg.get("resilience_policy") in RESILIENT_POLICIES
    cap = _completion_tokens(cfg, recipe, native)
    attempt, transport_retries, schema_repairs = 0, 0, 0
    ceiling_fallback = False

    def save_outcome(path, saved):
        if resilient:
            saved.update(thinking=native, max_tokens=cap,
                         ceiling_fallback=ceiling_fallback)
            if (saved["status"] == "CEILING_HIT" and role != "baseline"
                    and native == "native" and not ceiling_fallback):
                saved["next_attempt"] = "One native-to-off ceiling fallback; same context and ceiling."
        put(path, saved)
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
                    or intent.get("schema_repair", False) != bool(schema_repairs)
                    or intent.get("ceiling_fallback", False) != ceiling_fallback
                    or prepared["kwargs"].get("reasoning_effort", "high") != config.reasoning_effort_for(seat)):
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
                             "detail": exc.detail, "record": exc.record}
                    save_outcome(response_path, saved)
                    result = None
            else:
                prepared = adapter.prepare(seat=seat, messages=messages, max_tokens=cap,
                    thinking=native, role=role, coordinate={"call_id": call_id,
                    "cycle": cycle, "attempt": attempt, "schema_repair": bool(schema_repairs),
                    "ceiling_fallback": ceiling_fallback})
                put(request_path, {"epoch": time.time(), "role": role, "seat": seat,
                    "cycle": cycle, "attempt": attempt, "thinking": native,
                    "schema_repair": bool(schema_repairs), "ceiling_fallback": ceiling_fallback,
                    "prepared": prepared})
                try:
                    fixture = (scripted or offline_reply)(role, cycle, objections) if cfg["mode"] == "offline" else None
                    if isinstance(fixture, dict) and "content" not in fixture:
                        fixture = {"content": json.dumps(fixture, ensure_ascii=False)}
                    result = adapter.call(seat=seat, messages=messages, records_dir=folder / "provider",
                        max_tokens=cap, thinking=native, role=role,
                        coordinate={"call_id": call_id, "cycle": cycle, "attempt": attempt,
                                    "schema_repair": bool(schema_repairs),
                                    "ceiling_fallback": ceiling_fallback}, scripted=fixture)
                except ReasonFailure as exc:
                    saved = {"epoch": time.time(), "status": _code(exc),
                             "detail": exc.detail, "record": exc.record}
                    save_outcome(response_path, saved)
                    result = None
            if result is not None:
                try:
                    parsed = prompts.parse(role, result["content"], objections=objections,
                                           contract_version=contract)
                    saved = {"epoch": time.time(), "status": "COMPLETE", "result": result, "parsed": parsed,
                             "extra_keys": prompts.extra_keys(role, parsed, contract)}
                except (ReasonFailure, ValueError, TypeError, KeyError) as exc:
                    detail = exc.detail if isinstance(exc, ReasonFailure) else "ROLE_CONTRACT_INVALID: " + type(exc).__name__
                    record = result.get("record", {})
                    usage = result.get("usage") or {}
                    at_ceiling = (isinstance(usage.get("completion_tokens"), (int, float))
                                  and usage["completion_tokens"] >= cap)
                    truncated = isinstance(exc, ReasonFailure) and exc.record.get("json_truncated")
                    ceiling = (record.get("finish_reason") in {"length", "max_tokens"}
                               or (truncated and at_ceiling))
                    saved = {"epoch": time.time(), "status": "CEILING_HIT" if ceiling else "SCHEMA_FAILURE",
                             "result": result, "detail": detail + ("; completion ceiling reached" if ceiling else "")}
                save_outcome(response_path, saved)
            if after_call is not None:
                after_call(call_id, saved)
        if saved["status"] == "COMPLETE":
            return saved["parsed"]
        if ceiling_fallback:
            raise ReasonFailure(saved["status"], saved.get("detail", "Recorded ceiling fallback did not complete"))
        if (resilient and saved["status"] == "CEILING_HIT"
                and role != "baseline" and native == "native"):
            native = "off"
            ceiling_fallback = True
        elif (saved["status"] == "SCHEMA_FAILURE" and schema_repairs == 0
              and isinstance(saved.get("result", {}).get("content"), str)):
            messages = prompts.repair(messages, saved["result"]["content"], role,
                                      contract_version=contract, failure_reason=saved.get("detail"))
            schema_repairs = 1
        elif (saved["status"] == "TRANSPORT_OR_RESPONSE_ERROR" and schema_repairs == 0
              and transport_retries < cfg["retry_transport"]):
            transport_retries += 1
        else:
            raise ReasonFailure(saved["status"], saved.get("detail", "Recorded call did not complete"))
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


def _apply_dispositions(objections, dispositions, cycle, *, carry=False, phase=None):
    explicit = {d["id"]: d for d in dispositions}
    entries = []
    for obj in objections:
        disposition = explicit.get(obj["id"])
        if disposition is None:
            if not carry:
                continue
            # The parser already required every open objection. Retain both
            # original status and reason rather than inventing a new decision.
            disposition = {"id": obj["id"], "status": obj["status"],
                           "reason": obj["reason"], "carried": True}
        else:
            obj.update(status=disposition["status"], reason=disposition["reason"])
        entry = {"cycle": cycle, **disposition}
        if phase:
            entry["phase"] = phase
        obj["history"].append(entry)
        entries.append(dict(disposition))
    return entries


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
            phase = " closing return" if entry.get("phase") == "closing_return" else ""
            carried = " (carried)" if entry.get("carried") else ""
            trace += f"Cycle {entry['cycle']}{phase}: **{entry['status']}**{carried} - {entry['reason']}\n\n"
        trace += f"Current disposition: **{obj['status']}** - {obj['reason']}\n\n"
    if not objections:
        trace += "No objection has been recorded. This does not establish correctness.\n"
    resilient = cfg.get("resilience_policy") in RESILIENT_POLICIES
    seats = recipe["seats"]
    planned_seats = [("conjecture", seats["conjecture"], 1),
                     ("return", seats["conjecture"], cfg["cycles"]),
                     ("use", seats["use"], cfg["cycles"])]
    planned_seats += [(f"critic-{i}", seat, cfg["cycles"])
                      for i, seat in enumerate(seats["critics"], 1)]
    if seats.get("rival"):
        planned_seats.append(("rival", seats["rival"], cfg["cycles"]))
    if cfg.get("closing_return", False):
        planned_seats.append(("closing-return (conditional)", seats["conjecture"], 1))
    seat_controls = []
    for role, seat, count in planned_seats:
        thinking = config.thinking_for(seat)
        seat_controls.append({"role": role, "seat": config.seat_name(seat), "thinking": thinking,
            "reasoning_effort": config.reasoning_effort_for(seat), "logical_calls": count,
            "completion_tokens": _completion_tokens(cfg, recipe, thinking),
            "fallback_allowed": resilient and thinking == "native"})
    if cfg["baseline"]:
        for label, thinking in [("bare", "off"), ("native", "native")]:
            if thinking == "native" and not config.native_thinking_available(seats["conjecture"]):
                continue
            seat_controls.append({"role": "baseline-" + label,
                "seat": config.seat_name(seats["conjecture"]), "thinking": thinking,
                "reasoning_effort": config.reasoning_effort_for(seats["conjecture"]), "logical_calls": 1,
                "completion_tokens": _completion_tokens(cfg, recipe, thinking), "fallback_allowed": False})
    planned = sum(item["logical_calls"] for item in seat_controls)
    allowance = sum(item["logical_calls"] * item["completion_tokens"] for item in seat_controls)
    fallback_count = sum(item["logical_calls"] for item in seat_controls if item["fallback_allowed"])
    fallback_allowance = sum(item["logical_calls"] * item["completion_tokens"]
                             for item in seat_controls if item["fallback_allowed"])
    maximum_attempts = planned * (2 + cfg["retry_transport"]) + fallback_count
    maximum_allowance = allowance * (2 + cfg["retry_transport"]) + fallback_allowance
    repaired_calls = set()
    fallbacks = []
    controls = []
    usage = []
    cycle_working = {}
    diagnostics = []
    for path in attempts:
        intent = None
        if (path / "request.json").exists():
            intent = get(path / "request.json")
            if intent.get("schema_repair"):
                repaired_calls.add(path.parent.name)
            if intent.get("ceiling_fallback"):
                fallbacks.append(str(path.relative_to(directory)))
            controls.append({"call": str(path.relative_to(directory)), "seat": intent["seat"],
                             "thinking": intent.get("thinking", intent["prepared"].get("thinking")),
                             "schema_repair": bool(intent.get("schema_repair")),
                             "ceiling_fallback": bool(intent.get("ceiling_fallback")),
                             "max_tokens": intent["prepared"]["kwargs"]["max_tokens"],
                             "reasoning_effort": intent["prepared"]["kwargs"].get("reasoning_effort"),
                             "wire_reasoning_effort": intent["prepared"]["payload"].get("reasoning_effort"),
                             "wire_think": intent["prepared"]["payload"].get("think")})
        if (path / "response.json").exists():
            try:
                item = get(path / "response.json")
            except ReasonFailure:
                item = {"status": "RUN_INTEGRITY_ERROR"}
            if item.get("detail") or item.get("extra_keys"):
                diagnostics.append({"call": str(path.relative_to(directory)), "status": item["status"],
                                    "detail": item.get("detail", ""), "extra_keys": item.get("extra_keys", [])})
            working = item.get("parsed", {}).get("working")
            if intent and intent["cycle"] and working:
                cycle_working.setdefault(intent["cycle"], []).append(
                    (path.parent.name + "/" + path.name, working))
            usage.append({"call": str(path.relative_to(directory)), "status": item["status"],
                          "usage": item.get("result", {}).get("usage", item.get("record", {}).get("usage"))})
    schema_repairs = len(repaired_calls)
    if fallbacks:
        trace += "\n## Ceiling fallbacks\n\n"
        for path in fallbacks:
            trace += f"`{path}`: native-to-off fallback after CEILING_HIT; same context and completion ceiling.\n\n"
    unavailable = state.get("unavailable_seats", [])
    unavailable_critics = sum(item["role"] == "critic" for item in unavailable)
    unavailable_use = sum(item["role"] == "use" for item in unavailable)
    if unavailable:
        trace += "\n## Unavailable seats\n\n"
        for item in unavailable:
            trace += (f"Cycle {item['cycle']}, {item['call_id']} ({item['seat']}): "
                      f"{item['role']} unavailable: {item['code']}\n\n")
    diagnostic_text = ""
    if diagnostics:
        diagnostic_text = "\n## Attempt diagnostics\n\n" + "\n".join(
            f"{item['call']}: {item['status']}: {item['detail']}; extra keys {item['extra_keys']}\n"
            for item in diagnostics)
        trace += diagnostic_text
    if state.get("stop_detail"):
        trace += "\nStop detail: " + state["stop_detail"] + "\n"
    write(directory / "TRACE.md", trace, replace=True)
    run = ("# Personal reasoning run\n\n" + banner + CLAIM + "\n\n" +
           f"Run ID: `{cfg['run_id']}`\n\nRecipe: `{recipe['name']}`; SHA-256 `{cfg['recipe_sha256']}`.\n\n" +
           f"Seats: `{json.dumps(recipe['seats'], ensure_ascii=False)}`\n\n" +
           f"Requested cycles: {cfg['cycles']}; completed cycles: {state['completed_cycles']}.\n\n" +
           f"Recorded call attempts: {state['calls']}; planned logical calls without early stop: {planned}. " +
           ("Includes one conditional closing return allowance. " if cfg.get("closing_return", False) else "") +
           f"Completion allowance without repair/retry/fallback: {allowance}. " +
           "Input tokens are additional and depend on problem and growing objection history.\n\n" +
           f"Closing return enabled: {cfg.get('closing_return', False)}; outcome: {state.get('closing_return', 'not required')}. "
           "When enabled, one extra logical return follows cycle_budget if any use objection remains open; "
           "it supplies a final disposition for all open objections and preserves cycle_budget on success.\n\n" +
           f"Wall per attempt: 300 seconds; explicit transport retries: {cfg['retry_transport']}.\n\n" +
           f"Schema repair calls: {schema_repairs}; at most one per logical call. Repair transport errors are not retried; a native ceiling may use the declared fallback. " +
           f"Maximum attempts including repairs, fallbacks and configured transport retries: {maximum_attempts}; " +
           f"maximum completion allowance: {maximum_allowance}.\n\n" +
           f"Native-to-off ceiling fallback calls: {len(fallbacks)}; allowance: {fallback_count}. " +
           "Each allowed fallback keeps the same context and ceiling; failure ends that logical call. "
           "Under reasoning-exposure-v2, named critic/use failures are recorded as unavailable.\n\n" +
           f"Unavailable critic seats: {unavailable_critics}; Unavailable use seats: {unavailable_use}. "
           "Counts are logical seat occurrences across cycles, not failed attempts.\n\n" +
           "Declared ceilings and reasoning effort per seat (effort is sent only when the provider builder supports it):\n\n```json\n" +
           json.dumps(seat_controls, ensure_ascii=False, indent=2) + "\n```\n\n" +
           "Thinking, ceiling, effort, repair and fallback actually recorded for each attempt:\n\n```json\n" +
           json.dumps(controls, ensure_ascii=False, indent=2) + "\n```\n\n" +
           f"Stop reason: `{state['stop_reason']}`.\n\n" +
           "Baseline outcomes: `" + json.dumps(state.get("baselines", {}), sort_keys=True) + "`.\n\n" +
           ("Baselines run first; named ceiling, transport and schema failures are nonfatal under the saved resilience policy. "
            if resilient else "Legacy baseline failures retain their original terminal behavior. ") +
           "Baseline outputs, when requested, are in BASELINE.md. Extra loop calls are not matched multi-call controls. " +
           "No comparison is computed. Native support means locally implemented explicit control, not a fresh service capability check.\n\n" +
           "The use reader derives a dependent question separately from the problem and working answer; both derivations can be wrong. " +
           "Review its exact request and response alongside returned objections. Original observations are in calls/. " +
           "Custody checker: minireason.reason.prompts.parse (first JSON object with validated role fields); semantic use checker: the declared use seat. " +
           "JSON validation checks custody fields only and does not decide the legitimacy of prose criticism.\n\n" +
           "Reported usage by attempt (null means unknown):\n\n```json\n" + json.dumps(usage, indent=2) + "\n```\n")
    run += diagnostic_text
    if state.get("stop_detail"):
        run += "\nStop detail: " + state["stop_detail"] + "\n"
    write(directory / "RUN.md", run, replace=True)
    for number in sorted(set(cycle_notes) | set(cycle_working) | {item["cycle"] for item in unavailable}):
        note = cycle_notes.get(number, f"# Cycle {number} incomplete\n\n")
        for cid, working in cycle_working.get(number, []):
            note += f"\n## Visible working: {cid}\n\n{working}\n\n"
        for item in unavailable:
            if item["cycle"] == number:
                note += (f"\n{item['call_id']} ({item['seat']}): "
                         f"{item['role']} unavailable: {item['code']}\n")
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
        optional_recovery = cfg.get("resilience_policy") == RESILIENCE_POLICY
        carry = cfg.get("prompt_contract") == prompts.CURRENT_CONTRACT

        def record_unavailable(role, seat, cid, error):
            state.setdefault("unavailable_seats", []).append({
                "cycle": cycle, "call_id": cid, "role": role,
                "seat": config.seat_name(seat), "code": error.code, "detail": error.detail})

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
                baseline_text = "# Baseline readings\n\nSame problem and conjecturer; one logical call per mode, with recorded attempts. No computed comparison.\n\n"
                for label, native in [("bare", "off"), ("native", "native")]:
                    if native == "native" and not config.native_thinking_available(seats["conjecture"]):
                        baseline_text += "Native baseline unavailable through the declared adapter control.\n"
                        continue
                    try:
                        result = call("baseline", seats["conjecture"], "base-" + label, native=native)
                        outcome, body = "COMPLETE", result["answer"]
                    except ReasonFailure as exc:
                        if (cfg.get("resilience_policy") not in RESILIENT_POLICIES
                                or exc.code not in UNAVAILABLE_CODES):
                            raise
                        outcome, body = exc.code, "Baseline did not complete; loop execution continues."
                    state.setdefault("baselines", {})[label] = outcome
                    cap = _completion_tokens(cfg, recipe, native)
                    baseline_text += ("## " + label + "\n\nOutcome: `" + outcome + "`.\n\n" +
                        f"Thinking: {native}; completion ceiling: {cap}; declared reasoning effort: " +
                        config.reasoning_effort_for(seats["conjecture"]) + ".\n\n" + body + "\n\n")
                    write(directory / "BASELINE.md", baseline_text, replace=True)
            answer = call("conjecture", seats["conjecture"], "initial")["answer"]
            for cycle in range(1, cfg["cycles"] + 1):
                prefix = f"c{cycle:04d}"
                rival = ""
                if seats.get("rival"):
                    rival = call("rival", seats["rival"], prefix + "-rival", cycle, objections)["answer"]
                prior_objections = list(objections)
                new_critic = []
                returned_critics = 0
                last_critic_failure = None
                for index, seat in enumerate(seats["critics"], 1):
                    cid = prefix + f"-k{index:02d}"
                    try:
                        result = call("critic", seat, cid, cycle, prior_objections, rival=rival)
                    except ReasonFailure as exc:
                        if not optional_recovery or exc.code not in UNAVAILABLE_CODES:
                            raise
                        record_unavailable("critic", seat, cid, exc)
                        last_critic_failure = exc
                        continue
                    returned_critics += 1
                    new_critic.extend(_new_objections(result["objections"], cid, cycle, seat, objections))
                if not returned_critics:
                    raise last_critic_failure
                pending = list(objections) if carry else [o for o in objections if o["status"] == "unresolved"]
                result = call("return", seats["conjecture"], prefix + "-return", cycle, pending, rival)
                answer = result["answer"]
                cycle_dispositions = _apply_dispositions(pending, result["dispositions"], cycle, carry=carry)
                try:
                    used = call("use", seats["use"], prefix + "-use", cycle, objections)
                except ReasonFailure as exc:
                    if not optional_recovery or exc.code not in UNAVAILABLE_CODES:
                        raise
                    record_unavailable("use", seats["use"], prefix + "-use", exc)
                    used = {"unavailable": exc.code}
                new_use = _new_objections(used.get("objections", []), prefix + "-use", cycle, seats["use"], objections)
                for obj in new_use:
                    obj["history"].append({"cycle": cycle, "status": "unresolved",
                                           "reason": "Use objection awaiting the next operative return."})
                for obj in objections:
                    if not any(entry["cycle"] == cycle for entry in obj["history"]):
                        obj["history"].append({"cycle": cycle, "status": obj["status"],
                                               "reason": "Carried disposition: " + obj["reason"]})
                history.append({"cycle": cycle, "answer": answer,
                                "dispositions": cycle_dispositions if carry else result["dispositions"],
                                "use": {k: v for k, v in used.items() if k != "working"},
                                "objections": [{k: o[k] for k in ("id", "text", "defeats", "status", "reason")} for o in objections]})
                state["completed_cycles"] = cycle
                use_note = ("Use derivation unavailable; inspect the recorded seat outcome.\n\n"
                            if "unavailable" in used else
                            "Use question:\n\n" + used["question"] +
                            "\n\nIndependent derivation from PROBLEM:\n\n" + used["problem_derivation"] +
                            "\n\nDerivation from WORKING ANSWER:\n\n" + used["working_derivation"] + "\n\n")
                cycle_notes[cycle] = (f"# Cycle {cycle}\n\nWorking answer after return:\n\n{answer}\n\n" +
                    use_note +
                    "Dispositions and new use objections:\n\n```json\n" +
                    json.dumps({"dispositions": cycle_dispositions, "use_objections": new_use}, ensure_ascii=False, indent=2) +
                    "\n```\n\nExact requests and responses: ../../calls/" + prefix + "-*\n")
                if (returned_critics == len(seats["critics"]) and "unavailable" not in used
                        and not new_critic and not new_use
                        and not any(o["status"] == "unresolved" for o in objections)):
                    state["stop_reason"] = "no_new_objections"
                    break
                _reports(directory, cfg, recipe, state, answer, objections, cycle_notes)
            else:
                state["stop_reason"] = "cycle_budget"
            if (state["stop_reason"] == "cycle_budget" and cfg.get("closing_return", False)
                    and any(o["status"] == "unresolved" and "-use-o" in o["id"] for o in objections)):
                state["closing_return"] = "pending"
                pending = list(objections) if carry else [o for o in objections if o["status"] == "unresolved"]
                closed = call("return", seats["conjecture"], f"c{cycle:04d}-closing-return",
                              cycle, pending)
                answer = closed["answer"]
                closing_dispositions = _apply_dispositions(
                    pending, closed["dispositions"], cycle, carry=carry, phase="closing_return")
                state["closing_return"] = "complete"
                cycle_notes[cycle] += ("\n## Closing return\n\nWorking answer after final disposition:\n\n" +
                    answer + "\n\n" +
                    "Final dispositions:\n\n" + chr(96) * 3 + "json\n" +
                    json.dumps(closing_dispositions, ensure_ascii=False, indent=2) + "\n" + chr(96) * 3 + "\n")
        except ReasonFailure as exc:
            state["stop_reason"] = _code(exc)
            state["failed_cycle"] = cycle
            state["stop_detail"] = exc.detail
            if state.get("closing_return") == "pending":
                state["closing_return"] = "failed: " + state["stop_reason"]
                cycle_notes[cycle] += f"\nClosing return failed: {state['stop_reason']}: {exc.detail}; open objections remain.\n"
            elif cycle:
                cycle_notes[cycle] = f"# Cycle {cycle} stopped\n\nReason: `{state['stop_reason']}`: {exc.detail}. Partial call evidence is retained in calls/.\n"
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
