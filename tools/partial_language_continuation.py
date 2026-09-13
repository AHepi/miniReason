"""H004: separate continuation from immutable H003 full and length-limited text."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import getpass
import json
import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import multicycle_language_probe as h

FRONTIERS = dict(zip(h.ARMS, (11, 2, 8, 7, 7)))
DELIVERY = "h004.delivery.v1"
CATEGORIES = ("requests", "traces", "attempts", "provider", "responses", "manifests", "stopped")


def seed_path(output, plan):
    return (Path(output) / plan["seed_relative"]).resolve()


def provider_dir(root, arm, cycle):
    return h.at(root, "provider", arm, cycle).with_suffix("")


def classify(record, payload):
    """Classify delivery only; public prose is never semantically parsed."""
    usage, text = record.get("usage"), record.get("content")
    if (record.get("request") != payload or record.get("request_sha256") != h.digest(payload)
            or record.get("settings") != h.SETTINGS.to_dict()
            or not isinstance(text, str) or not text.strip() or not isinstance(usage, dict)
            or any(type(usage.get(k)) is not int or usage[k] < 0 for k in ("prompt_tokens", "completion_tokens"))
            or usage["completion_tokens"] > h.CAP
            or record.get("reasoning_content_present", False) or record.get("reasoning_content_persisted", False)
            or record.get("credential_redaction", False)):
        return "STOPPED"
    pair = (record.get("status"), record.get("finish_reason"))
    if pair == ("COMPLETE", "stop"):
        return "COMPLETE"
    if pair == ("INCOMPLETE_GENERATION", "length") and usage["completion_tokens"] == h.CAP:
        return "PARTIAL"
    return "STOPPED"


def read_contribution(root, arm, cycle, *, seed=False):
    request = h.load(h.at(root, "requests", arm, cycle))
    receipt = h.load(h.at(root, "responses", arm, cycle))
    attempt = h.load(h.at(root, "attempts", arm, cycle))
    raw = h.at(root, "responses", arm, cycle, "txt").read_bytes()
    directory = provider_dir(root, arm, cycle)
    provider_raw = (directory / "call-0001.response.json").read_bytes()
    record, sent = json.loads(provider_raw), h.load(directory / "call-0001.request.json")
    status = classify(record, request["provider_payload"])
    expected_coordinate = {"harness": "H003" if seed else "H004", "arm": arm, "cycle": cycle, "stage": "inquire"}
    if (status == "STOPPED" or request.get("arm") != arm or request.get("cycle") != cycle
            or attempt.get("arm") != arm or attempt.get("cycle") != cycle
            or receipt.get("arm") != arm or receipt.get("cycle") != cycle
            or attempt.get("request_sha256") != h.digest(request)
            or receipt.get("request_sha256") != h.digest(request)
            or sent.get("request") != request["provider_payload"]
            or sent.get("request_sha256") != h.digest(request["provider_payload"])
            or sent.get("settings") != h.SETTINGS.to_dict()
            or sent.get("coordinate") != expected_coordinate or record.get("coordinate") != expected_coordinate
            or receipt.get("text_sha256") != h.sha(raw) or receipt.get("provider_response_sha256") != h.sha(provider_raw)
            or record["content"].encode("utf-8") != raw or receipt.get("usage") != record.get("usage")
            or receipt.get("returned_model") != record.get("returned_model")
            or receipt.get("finish_reason") != record.get("finish_reason")
            or (seed and receipt.get("status") != ("COMPLETE" if status == "COMPLETE" else "OPERATIONAL_FAILURE"))
            or (not seed and receipt.get("status") != status)):
        raise ValueError("CONTRIBUTION_CUSTODY_CHANGED")
    return raw.decode("utf-8"), {"origin": "H003" if seed else "H004", "arm": arm, "cycle": cycle,
            "delivery_status": status, "text_sha256": h.sha(raw), "request_sha256": h.digest(request),
            "receipt_sha256": h.sha(h.at(root, "responses", arm, cycle).read_bytes()),
            "provider_response_sha256": h.sha(provider_raw)}


def seed_files(seed):
    seed = Path(seed)
    paths = [seed / "material.json", seed / "plan.json"]
    for category in CATEGORIES:
        paths.extend(p for p in (seed / category).rglob("*") if p.is_file())
    return {p.relative_to(seed).as_posix(): h.sha(p.read_bytes()) for p in sorted(paths)}


def inspect_seed(repo, seed):
    data, _ = h.verify(repo, seed)
    for arm, frontier in FRONTIERS.items():
        actual = sorted(int(p.stem) for p in (Path(seed) / "attempts" / arm).glob("*.json"))
        if actual != list(range(1, frontier + 1)):
            raise ValueError("SEED_FRONTIER_CHANGED")
        for cycle in actual:
            request, trace = h.render_arm(repo, seed, arm, cycle, data)
            if h.load(h.at(seed, "requests", arm, cycle)) != request or h.load(h.at(seed, "traces", arm, cycle)) != trace:
                raise ValueError("SEED_ROUTE_CHANGED")
            _, binding = read_contribution(seed, arm, cycle, seed=True)
            if binding["delivery_status"] != ("PARTIAL" if cycle == frontier else "COMPLETE"):
                raise ValueError("SEED_EXPECTED_FINAL_PARTIAL")
        marker = h.load(h.stopped(seed, arm))
        if marker.get("arm") != arm or marker.get("cycle") != frontier or marker.get("status") != "OPERATIONAL_FAILURE":
            raise ValueError("SEED_STOP_CHANGED")
    return data


def manifest_for(arm):
    manifest = h.manifest_for(arm)
    manifest["manifest_id"] = "h004.partial-continuation." + arm
    template = dict(manifest["kinds"][0])
    template.update(kind_id=DELIVERY, title="Delivery status and provenance",
                    output_port={"port_id": "out", "produces_kind": DELIVERY})
    manifest["kinds"].insert(2, template)
    manifest["kinds"][-1]["input_ports"].insert(0, {"port_id": "delivery", "port_type": "delivery", "window": "this_cycle"})
    manifest["port_types"].append({"port_type": "delivery", "draws_from": {"artifact_kinds": [DELIVERY]},
                                   "render": {"rule": "list_bodies", "header": "Delivery status and provenance"}})
    manifest["stages"].insert(2, {"stage_id": "delivery", "kind_id": DELIVERY, "seat": "machine", "ports": []})
    manifest["stages"][-2]["ports"].insert(0, "delivery")
    return manifest


def plan_body(repo, output, seed, data):
    h.verify_source_pins(repo, data["source_pins"])
    return {"schema": "minireason.h004.plan.v1", "seed_relative": os.path.relpath(seed, output),
            "seed_frontiers": FRONTIERS, "seed_calls": 35, "max_new_calls": 65, "max_combined_calls": 100,
            "max_completion_tokens_each": h.CAP, "max_new_completion_tokens": 65 * h.CAP,
            "max_combined_completion_tokens": 100 * h.CAP, "cycles": h.CYCLES, "arms": list(h.ARMS),
            "max_workers": 5, "automatic_retries": 0, "settings": h.SETTINGS.to_dict(),
            "material_sha256": h.sha((Path(seed) / "material.json").read_bytes()),
            "seed_execution_files": seed_files(seed), "source_pins": data["source_pins"],
            "runtime_pins": h.runtime_pins(repo), "helper_sha256": h.sha(Path(__file__).read_bytes()),
            "h003_helper_sha256": h.sha(Path(h.__file__).read_bytes()),
            "manifests": {a: h.sha(h.encoded(manifest_for(a))) for a in h.ARMS},
            "admissible_contributions": ["COMPLETE/stop", "INCOMPLETE_GENERATION/length with exactly 4096 reported completion tokens and valid nonempty public text"],
            "classification": "Separate H004 continuation; H003 stays stopped. Canonical reducer/render fixture, not full durable scheduler",
            "working_context": "Stable system and own policy, current task, previous own contribution and declared reopened targets only",
            "partial_annotation": "Length-limited prefix, missing ending unavailable; exact public text remains criticizable material"}


def initialize(repo, output, seed):
    repo, output, seed = Path(repo).resolve(), Path(output).resolve(), Path(seed).resolve()
    if output == seed or output.is_relative_to(seed):
        raise ValueError("OUTPUT_MUST_BE_SEPARATE")
    if (output / "plan.json").exists():
        raise FileExistsError("PLAN_ALREADY_EXISTS")
    data = inspect_seed(repo, seed)
    body = plan_body(repo, output, seed, data)
    h.write_new(output / "material.json", (seed / "material.json").read_bytes())
    for arm in h.ARMS:
        h.write_new(output / "manifests" / (arm + ".json"), manifest_for(arm))
        h.compile_manifest(output / "manifests" / (arm + ".json"))
    h.write_new(output / "plan.json", {**body, "plan_id": h.digest(body)})
    return body


def verify(repo, output):
    repo, output = Path(repo).resolve(), Path(output).resolve()
    plan = h.load(output / "plan.json")
    seed = seed_path(output, plan)
    data, _ = h.verify(repo, seed)
    expected = plan_body(repo, output, seed, data)
    if plan != {**expected, "plan_id": h.digest(expected)}:
        raise ValueError("PLAN_SEED_SOURCE_OR_RUNTIME_CHANGED")
    if (output / "material.json").read_bytes() != (seed / "material.json").read_bytes():
        raise ValueError("MATERIAL_CHANGED")
    for arm, identity in plan["manifests"].items():
        if h.sha((output / "manifests" / (arm + ".json")).read_bytes()) != identity:
            raise ValueError("MANIFEST_CHANGED")
    return data, plan


def delivery(binding):
    status = "complete public contribution" if binding["delivery_status"] == "COMPLETE" else "length-limited prefix; the missing ending is unavailable and must not be invented"
    return (f"{binding['origin']} own-arm {binding['arm']} cycle {binding['cycle']}: {status}. "
            f"Original public-text SHA256 {binding['text_sha256']}; receipt SHA256 {binding['receipt_sha256']}.")


def render_arm(repo, output, arm, cycle, context=None):
    h.check_cycle(cycle)
    data, plan = context or verify(repo, output)
    if arm not in FRONTIERS or cycle <= FRONTIERS[arm]:
        raise ValueError("SEED_COORDINATE_CANNOT_RERUN")
    seed = seed_path(output, plan)
    compiled = h.compile_manifest(Path(output) / "manifests" / (arm + ".json"))
    state, blobs, texts, bindings = h.MiniState(), h.MemoryBlobs(), {}, {}
    seq, previous = 0, compiled.genesis
    def add(stage_id, text, n):
        nonlocal seq, previous
        stage = compiled.stage(stage_id)
        kind = compiled.kinds[stage.kind_id]
        submission = h.read_submission(json.dumps({"body": text, "commitments": text}, ensure_ascii=False), kind, "both")
        identity, body, commitments = h._store_artifact(blobs, stage, submission, seq)
        event = h.build_event(seq=seq, prev=previous, type=h.ARTIFACT_SUBMITTED, cycle=n,
                    stage_id=stage_id, kind_id=stage.kind_id, artifact_id=identity, body_ref=body,
                    commitments_ref=commitments, payload={"seat": stage.seat, "completion_tokens": 0})
        h.apply_event(state, event)
        seq, previous = seq + 1, event.event_id
        if blobs.get(body) != text.encode() or blobs.get(commitments) != text.encode():
            raise ValueError("ARTIFACT_CUSTODY_CHANGED")
        return identity
    own = next(a for a in data["arms"] if a["arm_id"] == arm)
    for n in range(1, cycle + 1):
        task = data["cycles"][n - 1]
        prior = [bindings[n - 1]] if n > 1 else []
        reopened = [bindings[t] for t in task["reopen_cycles"]]
        add("task", task["task"], n)
        add("reopened", "\n\n".join(delivery(b) + "\n" + texts[b["cycle"]] for b in reopened)
            if reopened else "No earlier target is re-presented in this cycle.", n)
        add("delivery", "\n".join(["Delivery annotations identify observations, not semantic adequacy."]
            + ["Previous: " + delivery(b) for b in prior] + ["Reopened: " + delivery(b) for b in reopened]), n)
        if n <= FRONTIERS[arm]:
            text, binding = read_contribution(seed, arm, n, seed=True)
        else:
            brief, exposed = h.render_brief(compiled, state, blobs, compiled.stage("inquire"), n)
            if exposed or not brief.endswith(h.ENVELOPE):
                raise ValueError("UNEXPECTED_RENDER_CONTRACT")
            user = brief[:-len(h.ENVELOPE)] + h.PUBLIC
            messages = [{"role": "system", "content": data["shared_system"] + "\n\n" + own["instruction"]},
                        {"role": "user", "content": user}]
            trace = {"schema": "minireason.h004.trace.v1", "arm": arm, "cycle": n,
                     "original_brief": brief, "original_brief_sha256": h.sha(brief.encode()),
                     "transform": {"original_suffix": h.ENVELOPE, "replacement_suffix": h.PUBLIC},
                     "previous": prior, "reopened": reopened,
                     "windows": {"task": "this_cycle", "delivery": "this_cycle", "reopened": "this_cycle", "previous": "previous_cycle"},
                     "fixture": "Canonical reducer reconstruction; H004-specific artifact identities, zero fixture counters are not provider usage"}
            request = {"schema": "minireason.h004.request.v1", "arm": arm, "cycle": n,
                       "messages": messages, "messages_sha256": h.digest(messages),
                       "provider_payload": h.payload_for(messages), "provider_payload_sha256": h.digest(h.payload_for(messages)),
                       "trace_sha256": h.digest(trace)}
            if n == cycle:
                return request, trace
            if h.load(h.at(output, "requests", arm, n)) != request or h.load(h.at(output, "traces", arm, n)) != trace:
                raise ValueError("ANCESTOR_REQUEST_OR_TRACE_CHANGED")
            text, binding = read_contribution(output, arm, n)
        binding["h004_artifact_id"] = add("inquire", text, n)
        texts[n], bindings[n] = text, binding

def wave_path(output, wave):
    return Path(output) / "waves" / f"wave{wave:02d}.json"


def read_terminal(output, arm, cycle):
    request = h.load(h.at(output, "requests", arm, cycle))
    receipt = h.load(h.at(output, "responses", arm, cycle))
    attempt = h.load(h.at(output, "attempts", arm, cycle))
    if (receipt.get("arm") != arm or receipt.get("cycle") != cycle
            or receipt.get("request_sha256") != h.digest(request) or attempt.get("request_sha256") != h.digest(request)
            or attempt.get("arm") != arm or attempt.get("cycle") != cycle
            or receipt.get("started_at") != attempt.get("started_at")
            or not isinstance(receipt.get("finished_at"), str)):
        raise ValueError("TERMINAL_CUSTODY_CHANGED")
    if receipt["status"] in ("COMPLETE", "PARTIAL"):
        read_contribution(output, arm, cycle)
    elif receipt["status"] == "STOPPED":
        path = provider_dir(output, arm, cycle) / "call-0001.response.json"
        if path.exists():
            record = h.load(path)
            if (receipt.get("provider_response_sha256") != h.sha(path.read_bytes())
                    or classify(record, request["provider_payload"]) != "STOPPED"
                    or receipt.get("usage") != record.get("usage")):
                raise ValueError("STOPPED_RECEIPT_CHANGED")
        elif receipt.get("provider_response_sha256") is not None or receipt.get("usage") is not None:
            raise ValueError("STOPPED_RECEIPT_CHANGED")
        text = h.at(output, "responses", arm, cycle, "txt")
        if receipt.get("text_sha256") is not None and (not text.exists() or h.sha(text.read_bytes()) != receipt["text_sha256"]):
            raise ValueError("STOPPED_TEXT_CHANGED")
        marker = h.load(h.stopped(output, arm))
        if marker != {"arm": arm, "cycle": cycle, "status": "STOPPED", "reason": "NON_ADMISSIBLE_DELIVERY", "automatic_retry": False}:
            raise ValueError("STOP_MARKER_CHANGED")
    else:
        raise ValueError("UNKNOWN_TERMINAL_STATUS")
    return receipt


def coordinates(output, wave):
    if type(wave) is not int or not 1 <= wave <= 18:
        raise ValueError("WAVE_OUT_OF_RANGE")
    if wave > 1:
        previous = h.load(wave_path(output, wave - 1))
        if previous["wave"] != wave - 1:
            raise ValueError("WAVE_HISTORY_CHANGED")
        for arm, cycle in previous["coordinates"].items():
            read_terminal(output, arm, cycle)
    result = {}
    for arm, frontier in FRONTIERS.items():
        cycle = frontier + wave
        if cycle > h.CYCLES:
            continue
        marker_path = h.stopped(output, arm)
        if marker_path.exists():
            marker = h.load(marker_path)
            read_terminal(output, arm, marker["cycle"])
            if marker["cycle"] < cycle:
                continue
        result[arm] = cycle
    return result


def prepared_wave(output, wave, plan, selected):
    return {"schema": "minireason.h004.wave.v1", "wave": wave, "plan_id": plan["plan_id"],
            "coordinates": selected, "automatic_retry": False}


def prepare_wave(repo, output, wave):
    context = verify(repo, output)
    selected = coordinates(output, wave)
    if wave_path(output, wave).exists():
        raise FileExistsError("WAVE_ALREADY_PREPARED")
    requests = {}
    for arm, cycle in selected.items():
        if any(h.at(output, cat, arm, cycle).exists() for cat in ("attempts", "responses", "requests", "traces")):
            raise FileExistsError("NO_CLOBBER_OR_RETRY")
        requests[arm] = render_arm(repo, output, arm, cycle, context)
    for arm, (request, trace) in requests.items():
        cycle = selected[arm]
        h.write_new(h.at(output, "requests", arm, cycle), request)
        h.write_new(h.at(output, "traces", arm, cycle), trace)
    value = prepared_wave(output, wave, context[1], selected)
    h.write_new(wave_path(output, wave), value)
    return value


def check_published(repo, output, wave, selected):
    repo, output = Path(repo).resolve(), Path(output).resolve()
    data, plan = verify(repo, output)
    seed = seed_path(output, plan)
    head = h.git(repo, "rev-parse", "HEAD").decode().strip()
    remote = h.git(repo, "ls-remote", "--refs", "origin", "refs/heads/main").decode().split()
    if not remote or remote[0] != head:
        raise ValueError("REMOTE_MAIN_CHANGED")
    paths = [output / "plan.json", output / "material.json", Path(__file__).resolve(), Path(h.__file__).resolve()]
    paths += [seed / name for name in plan["seed_execution_files"]]
    paths += [h.repo_path(repo, name) for name in {**plan["runtime_pins"], **data["source_pins"]}]
    for category in (*CATEGORIES, "waves"):
        paths += [p for p in (output / category).rglob("*") if p.is_file()]
    for path in paths:
        name = path.resolve().relative_to(repo).as_posix()
        if h.git(repo, "show", head + ":" + name) != path.read_bytes():
            raise ValueError("INPUT_NOT_PUBLISHED")
    return head


def send_wave(repo, output, wave, *, provider_factory=None, publication_check=None, notify=print):
    context = verify(repo, output)
    selected = coordinates(output, wave)
    if h.load(wave_path(output, wave)) != prepared_wave(output, wave, context[1], selected):
        raise ValueError("WAVE_CHANGED")
    provider_factory, publication_check = provider_factory or h.DeepSeek, publication_check or check_published
    if not os.environ.get("DEEPSEEK_API_KEY"):
        raise ValueError("KEY_MISSING")
    pending = {}
    for arm, cycle in selected.items():
        if h.at(output, "attempts", arm, cycle).exists() or h.at(output, "responses", arm, cycle).exists():
            raise FileExistsError("NO_RETRY")
        request, trace = render_arm(repo, output, arm, cycle, context)
        if h.load(h.at(output, "requests", arm, cycle)) != request or h.load(h.at(output, "traces", arm, cycle)) != trace:
            raise ValueError("REQUEST_OR_TRACE_CHANGED")
        pending[arm] = request
    head = publication_check(repo, output, wave, selected)
    def send(arm):
        cycle, request = selected[arm], pending[arm]
        started = h.utc()
        h.write_new(h.at(output, "attempts", arm, cycle), {"arm": arm, "cycle": cycle, "wave": wave,
                    "started_at": started, "request_sha256": h.digest(request), "published_commit": head, "automatic_retry": False})
        directory = provider_dir(output, arm, cycle)
        try:
            provider = provider_factory(h.SETTINGS, directory)
            provider.complete(request["messages"], json_output=False,
                              coordinate={"harness": "H004", "arm": arm, "cycle": cycle, "stage": "inquire"})
        except (Exception, KeyboardInterrupt):
            # Original provider persists complete/partial/failure evidence; never retry or copy exception text.
            pass
        finished = h.utc()
        path = directory / "call-0001.response.json"
        try:
            record = h.load(path) if path.exists() else {}
        except (ValueError, OSError):
            record = {}
        status = classify(record, request["provider_payload"])
        text = record.get("content") if isinstance(record.get("content"), str) else None
        receipt = {"arm": arm, "cycle": cycle, "wave": wave, "status": status,
                   "started_at": started, "finished_at": finished, "request_sha256": h.digest(request),
                   "text_sha256": h.sha(text.encode()) if text is not None else None,
                   "provider_response_sha256": h.sha(path.read_bytes()) if path.exists() else None,
                   "usage": record.get("usage"), "finish_reason": record.get("finish_reason"),
                   "returned_model": record.get("returned_model"), "automatic_retry": False,
                   "answer_complete": status == "COMPLETE"}
        if text is not None:
            h.write_new(h.at(output, "responses", arm, cycle, "txt"), text.encode("utf-8"))
        h.write_new(h.at(output, "responses", arm, cycle), receipt)
        if status == "STOPPED":
            h.write_new(h.stopped(output, arm), {"arm": arm, "cycle": cycle, "status": status,
                        "reason": "NON_ADMISSIBLE_DELIVERY", "automatic_retry": False})
        notify(json.dumps({"arm": arm, "cycle": cycle, "wave": wave, "status": status, "usage": receipt["usage"]}))
        return receipt
    results = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(send, arm) for arm in selected]
        for future in as_completed(futures):
            results.append(future.result())
    return sorted(results, key=lambda r: h.ARMS.index(r["arm"]))


def totals(receipts, pending=0):
    usage = {}
    for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
        values = [(r.get("usage") or {}).get(key) for r in receipts]
        usage[key] = sum(values) if not pending and values and all(type(v) is int and v >= 0 for v in values) else None
    return usage


def checkpoint(repo, output, through_wave):
    data, plan = verify(repo, output)
    if type(through_wave) is not int or not 1 <= through_wave <= 18:
        raise ValueError("WAVE_OUT_OF_RANGE")
    seed = seed_path(output, plan)
    seed_receipts, new_receipts, intervals, arms = [], [], [], {}
    attempts = provider_calls = pending = 0
    for arm, frontier in FRONTIERS.items():
        seed_rows = [h.load(h.at(seed, "responses", arm, n)) for n in range(1, frontier + 1)]
        seed_receipts.extend(seed_rows)
        covered, full, partial, reason = frontier, frontier - 1, 1, None
        for n in range(frontier + 1, min(frontier + through_wave, h.CYCLES) + 1):
            attempt = h.at(output, "attempts", arm, n)
            path = h.at(output, "responses", arm, n)
            if attempt.exists():
                attempts += 1
            if (provider_dir(output, arm, n) / "call-0001.request.json").exists():
                provider_calls += 1
            if not path.exists():
                if attempt.exists():
                    pending += 1
                break
            request, trace = render_arm(repo, output, arm, n, (data, plan))
            if h.load(h.at(output, "requests", arm, n)) != request or h.load(h.at(output, "traces", arm, n)) != trace:
                raise ValueError("REQUEST_OR_TRACE_CHANGED")
            receipt = read_terminal(output, arm, n)
            new_receipts.append(receipt)
            intervals.extend([(receipt["started_at"], 1), (receipt["finished_at"], -1)])
            if receipt["status"] == "STOPPED":
                reason = "NON_ADMISSIBLE_DELIVERY"
                break
            covered = n
            full += receipt["status"] == "COMPLETE"
            partial += receipt["status"] == "PARTIAL"
        arms[arm] = {"covered_through": covered, "full_contributions": full, "partial_contributions": partial, "stopped_reason": reason}
    current = maximum = 0
    for _, delta in sorted(intervals, key=lambda item: (item[0], item[1])):
        current += delta
        maximum = max(maximum, current)
    complete = all(row["covered_through"] == h.CYCLES for row in arms.values())
    value = {"schema": "minireason.h004.checkpoint.v1", "through_wave": through_wave,
             "status": "TWENTY_COORDINATES_COVERED" if complete else "PARTIAL_COVERAGE", "arms": arms,
             "seed_calls": 35, "new_provider_request_records": provider_calls, "combined_provider_request_records": 35 + provider_calls,
             "new_attempt_markers": attempts, "pending_attempts": pending, "new_terminal_receipts": len(new_receipts),
             "seed_full": 30, "seed_partial": 5,
             "new_full": sum(r["status"] == "COMPLETE" for r in new_receipts),
             "new_partial": sum(r["status"] == "PARTIAL" for r in new_receipts),
             "new_stopped": sum(r["status"] == "STOPPED" for r in new_receipts),
             "seed_usage": totals(seed_receipts), "new_usage": totals(new_receipts, pending),
             "combined_usage": totals(seed_receipts + new_receipts, pending),
             "observed_maximum_concurrency": maximum, "concurrency_intervals_complete": pending == 0,
             "concurrency_basis": "Completed H004 helper intervals, including overhead; not server-observed overlap",
             "twenty_full_answers_each": all(row["full_contributions"] == h.CYCLES for row in arms.values()),
             "h003_resumed": False, "full_durable_scheduler": False, "semantic_verdict": None}
    h.write_new(Path(output) / f"checkpoint-wave{through_wave:02d}.json", value)
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("init", "prepare-wave", "send-wave", "checkpoint"))
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=Path)
    parser.add_argument("--wave", type=int)
    parser.add_argument("--through-wave", type=int)
    args = parser.parse_args()
    if args.command == "init":
        if args.seed is None:
            parser.error("init requires --seed")
        result = initialize(args.repo, args.output, args.seed)
    elif args.command == "prepare-wave":
        result = prepare_wave(args.repo, args.output, args.wave)
    elif args.command == "checkpoint":
        result = checkpoint(args.repo, args.output, args.through_wave)
    else:
        if not sys.stdin.isatty():
            raise ValueError("TTY_REQUIRED")
        key = getpass.getpass("DEEPSEEK_KEY_INPUT")
        try:
            if not key:
                raise ValueError("KEY_MISSING")
            os.environ["DEEPSEEK_API_KEY"] = key
            result = send_wave(args.repo, args.output, args.wave, notify=lambda line: print(line, flush=True))
        finally:
            os.environ.pop("DEEPSEEK_API_KEY", None)
            key = ""
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
