"""Recordable model-language setup and expressibility probes; no automatic semantic verdict.

Every command that calls a model consumes a previously frozen plan. Publication is
handled by the operator after each setup or carrier test. Prose artifacts survive
without JSON, Lean, or semantic-ontology admission gates.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

from creib.strict_json import loads_strict

from .campaign import source_identity
from .language_data import INSTRUCTIONS, PROBLEM_CONTEXT, RAW_SYSTEM
from .provider import DeepSeek, Settings, digest, write_new

ARMS = {"bare", "native", "matched", "matched_native", "mini", "mini_native"}
CARRIERS = {"prose", "lean_candidate", "nonlean_candidate"}
STAGES = ("express", "reinterpret", "criticize")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _signed(value: dict[str, Any], field: str) -> dict[str, Any]:
    return {**value, field: digest(value)}


def _verify_signed(value: dict[str, Any], field: str) -> None:
    if value.get(field) != digest({k: v for k, v in value.items() if k != field}):
        raise ValueError(f"FROZEN_IDENTITY_CHANGED: {field}")


def load_frozen(path: Path) -> dict[str, Any]:
    value = loads_strict(path.read_text())
    if not isinstance(value, dict):
        raise ValueError("FROZEN_DOCUMENT_NOT_OBJECT")
    return value


def make_preparation_plan(test_id: str, stage: str, *, corpus: dict[str, Any] | None = None,
                          problem: str = PROBLEM_CONTEXT, max_tokens: int = 16384,
                          thinking: bool = False) -> dict[str, Any]:
    if stage not in {"corpus", "languages"}:
        raise ValueError("Preparation stage must be corpus or languages")
    settings = Settings(thinking=thinking, max_tokens=max_tokens)
    if stage == "corpus":
        prompt = problem + "\n\n" + INSTRUCTIONS["corpus_freeze_v1"]["instruction"]
        system = RAW_SYSTEM
    else:
        if corpus is None:
            raise ValueError("FROZEN_CORPUS_REQUIRED")
        _verify_signed(corpus, "corpus_id")
        prompt = INSTRUCTIONS["paired_language_invention_v1"]["instruction"] + "\n\nFrozen original material:\n" + json.dumps(corpus, ensure_ascii=False, sort_keys=True, indent=2)
        system = ("Return one JSON object with exactly two fields: lean and nonlean, each a string "
                  "containing the complete proposed language and its explanation. These are transport "
                  "boundaries, not semantic types. Lean source may appear in fenced blocks inside lean. "
                  "No correctness, compilation, novelty or semantic-adequacy gate is imposed.")
    return _signed({"schema": "minireason.language-preparation-plan.v1", "test_id": test_id,
                    "stage": stage, "created_at": _now(), "corpus": corpus, "problem": problem,
                    "settings": settings.to_dict(), "prompt": prompt, "system": system,
                    "prompt_sha256": digest({"system": system, "prompt": prompt}),
                    "source": source_identity(), "max_model_calls": 1,
                    "interpretation": "Model-origin setup material; no adequacy verdict"}, "plan_id")


def _check_plan(plan: dict[str, Any]) -> None:
    _verify_signed(plan, "plan_id")
    if plan["source"]["source_sha256"] != source_identity()["source_sha256"]:
        raise ValueError("SOURCE_CHANGED_SINCE_PLAN")


def _settings(raw: dict[str, Any], *, thinking: bool | None = None) -> Settings:
    return Settings(model=raw["model"], base_url=raw["base_url"],
                    thinking=raw["thinking"] if thinking is None else thinking,
                    reasoning_effort=raw["reasoning_effort"], max_tokens=raw["max_tokens"],
                    timeout_seconds=raw["timeout_seconds"])


def _resources(provider: Any) -> dict[str, int]:
    return {key: int(getattr(provider, key, 0)) for key in ("calls", "prompt_tokens", "completion_tokens")}


def run_preparation(plan_path: Path, root: Path, *, provider_factory: Callable[..., Any] = DeepSeek) -> dict[str, Any]:
    plan = load_frozen(plan_path)
    _check_plan(plan)
    if plan["schema"] != "minireason.language-preparation-plan.v1":
        raise ValueError("PREPARATION_PLAN_REQUIRED")
    root.mkdir(parents=True, exist_ok=False)
    write_new(root / "plan.json", plan)
    record: dict[str, Any] = {"schema": "minireason.language-preparation-result.v1", "test_id": plan["test_id"],
        "stage": plan["stage"], "plan_id": plan["plan_id"], "started_at": _now(),
        "status": "RUNNING", "alarms": [], "interpretation_status": "UNADJUDICATED"}
    write_new(root / "started.json", record)
    provider = None
    try:
        provider = provider_factory(_settings(plan["settings"]), root / "calls")
        answer = provider.complete([{"role": "system", "content": plan["system"]},
                                    {"role": "user", "content": plan["prompt"]}],
                                   json_output=plan["stage"] == "languages",
                                   coordinate={"stage": "prepare_" + plan["stage"]})
        raw = answer["content"]
        write_new(root / "raw-artifact.json", {"text": raw, "origin": "calls/call-0001.response.json",
                                               "sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest()})
        if plan["stage"] == "corpus":
            corpus = _signed({"schema": "minireason.language-corpus.v1", "problem": plan["problem"],
                               "text": raw, "origin_plan_id": plan["plan_id"],
                               "model": plan["settings"]["model"]}, "corpus_id")
            write_new(root / "corpus.json", corpus)
            record["corpus_id"] = corpus["corpus_id"]
        else:
            languages = loads_strict(raw)
            if type(languages) is not dict or set(languages) != {"lean", "nonlean"} or any(type(languages[k]) is not str or not languages[k].strip() for k in languages):
                raise ValueError("LANGUAGE_PACKET_BOUNDARIES_UNRESOLVED: paired nonempty language texts required; raw retained")
            packet = _signed({"schema": "minireason.language-packet.v1", "corpus": plan["corpus"],
                               "languages": languages, "origin_plan_id": plan["plan_id"],
                               "model": plan["settings"]["model"],
                               "status": "FROZEN_UNADJUDICATED"}, "packet_id")
            write_new(root / "packet.json", packet)
            record["packet_id"] = packet["packet_id"]
        record["status"] = "PREPARATION_RECORDED"
    except Exception as error:
        record["status"] = "PREPARATION_INCOMPLETE"
        record["alarms"].append({"code": getattr(error, "code", type(error).__name__), "detail": str(error)})
    record.update({"resources": _resources(provider), "ended_at": _now()})
    write_new(root / "result.json", record)
    write_new(root / "errata.json", {"operational": record["alarms"],
                                     "semantic_status": "No adequacy assessment; raw response retained even if packet extraction failed"})
    (root / "REPORT.md").write_text(
        f"# {plan['test_id']}\n\nSetup stage: {plan['stage']}. Recording outcome: {record['status']}.\n\n"
        "This setup preserves model-origin material without an adequacy or creativity verdict. "
        "Inspect raw-artifact.json and calls for the original public answer; corpus.json or packet.json "
        "is produced only when its transport boundaries can be identified. A failed extraction retains the raw prose.\n\n"
        f"Calls used: {record['resources']['calls']}. Completion tokens: {record['resources']['completion_tokens']}. "
        "Inspect errata.json for operational failures.\n")
    return record


def selected_language(packet: dict[str, Any], carrier: str) -> str:
    if carrier == "prose":
        return "Unconstrained ordinary prose; neither candidate language is obligatory."
    return packet["languages"]["lean" if carrier == "lean_candidate" else "nonlean"]


def _material_snapshots(plan: dict[str, Any]) -> dict[str, Any]:
    """Bind the exact source bytes, independently of filesystem location."""
    snapshots = {}
    for name in ("packet_text", "selected_language_text", "compiler_text"):
        text = plan[name]
        if type(text) is not str:
            raise ValueError(f"MATERIAL_NOT_TEXT: {name}")
        raw = text.encode("utf-8")
        snapshots[name] = {"encoding": "utf-8", "sha256": hashlib.sha256(raw).hexdigest(),
                           "bytes": len(raw), "characters": len(text)}
    return snapshots


def _probe_material(plan: dict[str, Any]) -> dict[str, Any]:
    return {"packet_text": plan["packet_text"],
            "selected_language_text": plan["selected_language_text"],
            "carrier_directive": plan["carrier_directive"],
            "stage_instructions": plan["stage_instructions"],
            "max_tokens": plan["settings"]["max_tokens"],
            "cycles": plan["cycles"], "compiler_text": plan["compiler_text"]}


def make_probe_plan(test_id: str, packet: dict[str, Any], carrier: str, rationale: str, *,
                    arms: list[str] | None = None, repetitions: int = 1, max_tokens: int = 16384,
                    parent: str | None = None, compiler_text: str = "") -> dict[str, Any]:
    _verify_signed(packet, "packet_id")
    _verify_signed(packet["corpus"], "corpus_id")
    if carrier not in CARRIERS:
        raise ValueError("UNKNOWN_CARRIER")
    chosen = arms if arms is not None else ["bare", "native", "matched", "matched_native", "mini", "mini_native"]
    if not chosen or not set(chosen) <= ARMS or len(set(chosen)) != len(chosen):
        raise ValueError("INVALID_OR_DUPLICATE_ARMS")
    if type(repetitions) is not int or not 1 <= repetitions <= 20:
        raise ValueError("INVALID_REPETITIONS")
    settings = Settings(max_tokens=max_tokens)
    plan = {"schema": "minireason.language-probe-plan.v1", "test_id": test_id,
                   "created_at": _now(), "parent": parent, "rationale": rationale,
                   "carrier": carrier, "packet": packet, "packet_id": packet["packet_id"],
                   "packet_text": json.dumps(packet, ensure_ascii=False, sort_keys=True, indent=2),
                   "selected_language_text": selected_language(packet, carrier),
                   "carrier_directive": INSTRUCTIONS["carrier_directives"][carrier],
                   "stage_instructions": dict(INSTRUCTIONS["express_reinterpret_criticize_v1"]),
                   "single_instruction": INSTRUCTIONS["frozen_single_call_control_v1"]["instruction"],
                   "compiler_text": compiler_text, "settings": settings.to_dict(),
                   "arms": chosen, "repetitions": repetitions, "max_concurrent_calls": 5,
                   "cycles": 1, "source": source_identity(),
                   "interpretation": "Frozen expression/reading/criticism observations; no automatic adequacy or creativity verdict",
                   "packet_review_status": "Inspect actual proposed languages for embedded source quotations and translations before running; no automatic adequacy gate",
                   "design_limits": ["One-shot arms use one intervention call; matched and Mini use three.",
                                     "Matched and Mini use the same outgoing renderer after Mini's actual port visibility is checked. This calibrates routing and recording, not a difference in conditional prompt content.",
                                     "Native completion tokens include hidden reasoning; actual use is not equalized.",
                                     "Original corpus field is omitted from reinterpretation, but source-conditioned languages and expressions may themselves quote it.",
                                     "Unconstrained prose may copy source text; this is a fidelity control, not evidence of creativity.",
                                     "No proposed language or conjecture successor is installed."]}
    plan["material_snapshots"] = _material_snapshots(plan)
    plan["preflight_policy"] = "Verify frozen material and compile actual Mini routes before constructing any provider; failure blocks every arm with recorded zero-call results."
    return _signed(plan, "plan_id")


def stage_prompt(plan: dict[str, Any], stage: str, history: list[dict[str, Any]]) -> str:
    selected = plan["selected_language_text"]
    directive = plan["carrier_directive"]
    if stage == "express":
        context = "Frozen shared packet:\n" + plan["packet_text"]
    elif stage == "reinterpret":
        expression = next(row["text"] for row in history if row["stage"] == "express")
        context = "Selected language's stated meaning:\n" + selected + "\n\nActual expression:\n" + expression
    elif stage == "criticize":
        expression = next(row["text"] for row in history if row["stage"] == "express")
        reading = next(row["text"] for row in history if row["stage"] == "reinterpret")
        context = "Frozen shared packet:\n" + plan["packet_text"] + "\n\nActual expression:\n" + expression + "\n\nSource-text-withheld reading:\n" + reading
        if plan["compiler_text"]:
            context += "\n\nOptional compiler observations (conditional, no semantic privilege):\n" + plan["compiler_text"]
    else:
        raise ValueError("UNKNOWN_PROBE_STAGE")
    return directive + "\n\n" + plan["stage_instructions"][stage] + "\n\n" + context


def _direct_probe(provider: Any, arm: str, plan: dict[str, Any], root: Path,
                  *, history: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    if history is None:
        history = []
    stages = ("express",) if arm in {"bare", "native"} else STAGES
    for stage in stages:
        prompt = stage_prompt(plan, stage, history)
        if arm in {"bare", "native"}:
            prompt += "\n\n" + plan["single_instruction"]
        write_new(root / f"{stage}.input.json", {"stage": stage, "prompt": prompt,
                                                  "raw_source_corpus_field_visible": stage != "reinterpret"})
        answer = provider.complete([{"role": "system", "content": RAW_SYSTEM},
                                    {"role": "user", "content": prompt}], json_output=False,
                                   coordinate={"stage": stage, "carrier": plan["carrier"]})
        row = {"stage": stage, "text": answer["content"], "text_sha256": hashlib.sha256(answer["content"].encode("utf-8")).hexdigest(),
               "source_packet_id": plan["packet_id"], "proposed_changes_installed": False}
        write_new(root / f"{stage}.artifact.json", row)
        history.append(row)
    return {"history": history, "final": history[-1], "alarms": [],
            "visibility": {"reinterpret_raw_source_field_visible": False,
                           "scope": "Source-derived expression and selected language remain visible"}}


def run_probe_arm(plan: dict[str, Any], arm: str, repeat: int, root: Path, *,
                  provider_factory: Callable[..., Any] = DeepSeek,
                  prepared: Any = None) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=False)
    settings = _settings(plan["settings"], thinking=arm in {"native", "matched_native", "mini_native"})
    record = {"schema": "minireason.language-arm.v1", "arm": arm, "repeat": repeat,
              "carrier": plan["carrier"], "plan_id": plan["plan_id"], "packet_id": plan["packet_id"],
              "started_at": _now(), "settings": settings.to_dict(), "status": "RUNNING",
              "history": [], "alarms": [], "interpretation_status": "PENDING_SUBSTANTIVE_REVIEW"}
    write_new(root / "started.json", record)
    provider = None
    try:
        if arm.startswith("mini") and prepared is None:
            from .language_mini import prepare_probe
            prepared = prepare_probe(root / "preflight", **_probe_material(plan))
        provider = provider_factory(settings, root / "calls")
        if arm.startswith("mini"):
            from .language_mini import run_probe
            observation = run_probe(provider, root, **_probe_material(plan), prepared=prepared)
        else:
            observation = _direct_probe(provider, arm, plan, root, history=record["history"])
        record.update({key: value for key, value in observation.items() if key != "schema"})
        if "schema" in observation:
            record["route_schema"] = observation["schema"]
        expected = 1 if arm in {"bare", "native"} else 3
        if len(record["history"]) != expected:
            raise ValueError("PROBE_ROUTE_INCOMPLETE: expected every declared artifact")
        record["status"] = "OBSERVATIONS_RECORDED" if not record["alarms"] else "OPERATIONAL_ALARM"
    except Exception as error:
        record["status"] = "OPERATIONAL_FAILURE"
        record["alarms"].append({"code": getattr(error, "code", type(error).__name__), "detail": str(error)})
    record.update({"resources": _resources(provider), "ended_at": _now()})
    write_new(root / "result.json", record)
    write_new(root / "errata.json", {"operational": record["alarms"],
                                     "semantic_findings": "Unadjudicated; inspect original expressions, readings and criticisms"})
    return record


def _preflight_probe(plan: dict[str, Any], root: Path) -> tuple[Any, dict[str, Any]]:
    """Check the actual frozen material before any arm can construct a provider."""
    _verify_signed(plan["packet"]["corpus"], "corpus_id")
    if plan["packet_id"] != plan["packet"]["packet_id"]:
        raise ValueError("PACKET_ID_MISMATCH")
    expected_packet = json.dumps(plan["packet"], ensure_ascii=False, sort_keys=True, indent=2)
    if plan["packet_text"] != expected_packet:
        raise ValueError("PACKET_TEXT_MISMATCH: exact canonical packet text required")
    if plan["selected_language_text"] != selected_language(plan["packet"], plan["carrier"]):
        raise ValueError("SELECTED_LANGUAGE_MISMATCH")
    snapshots = _material_snapshots(plan)
    if plan.get("material_snapshots") != snapshots:
        raise ValueError("MATERIAL_SNAPSHOT_MISMATCH: regenerate and freeze the plan with exact source snapshots")
    if not plan["arms"] or not set(plan["arms"]) <= ARMS or len(set(plan["arms"])) != len(plan["arms"]):
        raise ValueError("INVALID_OR_DUPLICATE_ARMS")
    if type(plan["repetitions"]) is not int or not 1 <= plan["repetitions"] <= 20:
        raise ValueError("INVALID_REPETITIONS")
    if plan["cycles"] != 1:
        raise ValueError("FROZEN_PROBE_REQUIRES_ONE_CYCLE")
    # Exercise every declared prompt path without producing model artifacts.
    sentinel_history = [{"stage": "express", "text": "PREFLIGHT_EXPRESSION_PLACEHOLDER"},
                        {"stage": "reinterpret", "text": "PREFLIGHT_READING_PLACEHOLDER"}]
    for stage in STAGES:
        stage_prompt(plan, stage, sentinel_history)
    _settings(plan["settings"])
    prepared = None
    summary = {"status": "CONFIGURATION_PREFLIGHT_PASSED", "material_snapshots": snapshots,
               "provider_constructions": 0, "model_calls": 0,
               "scope": "Exact material identities, prompt construction, and declared Mini manifest compilation; no semantic assessment"}
    if any(arm.startswith("mini") for arm in plan["arms"]):
        from .language_mini import prepare_probe
        prepared = prepare_probe(root / "preflight", **_probe_material(plan))
        summary["mini"] = prepared.summary()
    else:
        summary["mini"] = {"status": "NOT_DECLARED"}
    return prepared, summary


def _blocked_probe_arm(plan: dict[str, Any], arm: str, repeat: int, root: Path,
                       alarm: dict[str, Any]) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=False)
    record = {"schema": "minireason.language-arm.v1", "arm": arm, "repeat": repeat,
              "carrier": plan["carrier"], "plan_id": plan["plan_id"], "packet_id": plan["packet_id"],
              "status": "CONFIGURATION_PREFLIGHT_FAILED", "history": [], "alarms": [alarm],
              "resources": {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0},
              "ended_at": _now(), "interpretation_status": "NOT_RUN_CONFIGURATION_FAILURE"}
    write_new(root / "result.json", record)
    write_new(root / "errata.json", {"operational": [alarm],
        "semantic_findings": "No model call or semantic assessment occurred; configuration failure blocked the complete comparison"})
    return record


def run_probe_test(plan_path: Path, root: Path, *, jobs: int = 5,
                   provider_factory: Callable[..., Any] = DeepSeek) -> dict[str, Any]:
    if type(jobs) is not int or not 1 <= jobs <= 5:
        raise ValueError("CONCURRENCY_MUST_BE_ONE_TO_FIVE")
    plan = load_frozen(plan_path)
    _check_plan(plan)
    if plan["schema"] != "minireason.language-probe-plan.v1":
        raise ValueError("PROBE_PLAN_REQUIRED")
    _verify_signed(plan["packet"], "packet_id")
    root.mkdir(parents=True, exist_ok=False)
    write_new(root / "plan.json", plan)
    write_new(root / "packet.json", plan["packet"])
    write_new(root / "started.json", {"test_id": plan["test_id"], "plan_id": plan["plan_id"],
                                     "started_at": _now(), "status": "CONFIGURATION_PREFLIGHT"})
    results = []
    try:
        prepared, preflight = _preflight_probe(plan, root)
    except Exception as error:
        alarm = {"code": "CONFIGURATION_PREFLIGHT_FAILED",
                 "cause_code": getattr(error, "code", type(error).__name__), "detail": str(error)}
        preflight = {"status": "CONFIGURATION_PREFLIGHT_FAILED", "alarms": [alarm],
                     "provider_constructions": 0, "model_calls": 0}
        for repeat in range(1, plan["repetitions"] + 1):
            for arm in plan["arms"]:
                results.append(_blocked_probe_arm(plan, arm, repeat, root / f"{arm}-r{repeat:02d}", alarm))
    write_new(root / "preflight.json", preflight)
    if preflight["status"] == "CONFIGURATION_PREFLIGHT_PASSED":
        with ThreadPoolExecutor(max_workers=jobs) as pool:
            futures = [pool.submit(run_probe_arm, plan, arm, repeat, root / f"{arm}-r{repeat:02d}",
                                   provider_factory=provider_factory, prepared=prepared)
                       for repeat in range(1, plan["repetitions"] + 1) for arm in plan["arms"]]
            for future in as_completed(futures):
                results.append(future.result())
    summary = {"schema": "minireason.language-test.v1", "test_id": plan["test_id"],
               "carrier": plan["carrier"], "plan_id": plan["plan_id"], "packet_id": plan["packet_id"],
               "completed_at": _now(), "preflight": preflight,
               "interpretation_status": "PENDING_SUBSTANTIVE_REVIEW" if preflight["status"] == "CONFIGURATION_PREFLIGHT_PASSED" else "NOT_RUN_CONFIGURATION_FAILURE",
               "arms": [{k: row[k] for k in ("arm", "repeat", "status", "resources")} for row in sorted(results, key=lambda row: (row["repeat"], row["arm"]))]}
    write_new(root / "summary.json", summary)
    write_new(root / "errata.json", {"configuration": preflight.get("alarms", []),
        "operational": [{"arm": row["arm"], "repeat": row["repeat"], **alarm}
                        for row in results for alarm in row["alarms"]],
        "semantic_findings": "Unadjudicated; configuration and transport outcomes are not semantic scores"})
    lines = [f"# {plan['test_id']}", "", plan["rationale"], "",
             "These are expression, reading and criticism records. No automated adequacy or creativity verdict has been issued.", "",
             f"Configuration preflight: {preflight['status']}. Inspect preflight.json and errata.json for material identities and failures.", "",
             "| Arm | Repeat | Recording outcome | Calls | Completion tokens |", "|---|---:|---|---:|---:|"]
    for row in summary["arms"]:
        lines.append(f"| {row['arm']} | {row['repeat']} | {row['status']} | {row['resources']['calls']} | {row['resources']['completion_tokens']} |")
    if preflight["status"] == "CONFIGURATION_PREFLIGHT_FAILED":
        lines.extend(["", "The actual configuration failed before any provider was constructed. Every declared arm was blocked, and no model calls were made. This is a harness configuration failure; it supplies no evidence about model reasoning or the proposed languages.", ""])
    else:
        lines.extend(["", "Original conjectures and languages remain frozen. Inspect actual stage inputs to assess visibility and the artifact texts to assess expressive effects.", ""])
    (root / "REPORT.md").write_text("\n".join(lines))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prep = commands.add_parser("prepare-plan")
    prep.add_argument("--id", required=True)
    prep.add_argument("--stage", choices=["corpus", "languages"], required=True)
    prep.add_argument("--corpus", type=Path)
    prep.add_argument("--problem", type=Path)
    prep.add_argument("--max-tokens", type=int, default=16384)
    prep.add_argument("--thinking", action="store_true")
    prep.add_argument("--output", type=Path, required=True)
    perform = commands.add_parser("prepare")
    perform.add_argument("--plan", type=Path, required=True)
    perform.add_argument("--output", type=Path, required=True)
    plan = commands.add_parser("plan")
    plan.add_argument("--id", required=True)
    plan.add_argument("--packet", type=Path, required=True)
    plan.add_argument("--carrier", choices=sorted(CARRIERS), required=True)
    plan.add_argument("--rationale", required=True)
    plan.add_argument("--parent")
    plan.add_argument("--arms", nargs="+", choices=sorted(ARMS))
    plan.add_argument("--repetitions", type=int, default=1)
    plan.add_argument("--max-tokens", type=int, default=16384)
    plan.add_argument("--compiler-observations", type=Path)
    plan.add_argument("--output", type=Path, required=True)
    run = commands.add_parser("run")
    run.add_argument("--plan", type=Path, required=True)
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--jobs", type=int, default=5)
    args = parser.parse_args()
    if args.command == "prepare-plan":
        corpus = load_frozen(args.corpus) if args.corpus else None
        value = make_preparation_plan(args.id, args.stage, corpus=corpus,
                 problem=args.problem.read_text() if args.problem else PROBLEM_CONTEXT,
                 max_tokens=args.max_tokens, thinking=args.thinking)
        write_new(args.output, value)
    elif args.command == "prepare":
        run_preparation(args.plan, args.output)
    elif args.command == "plan":
        value = make_probe_plan(args.id, load_frozen(args.packet), args.carrier, args.rationale,
                 arms=args.arms, repetitions=args.repetitions, max_tokens=args.max_tokens,
                 parent=args.parent, compiler_text=args.compiler_observations.read_text() if args.compiler_observations else "")
        write_new(args.output, value)
    else:
        run_probe_test(args.plan, args.output, jobs=args.jobs)
    print("Complete; inspect and publish this record before the next test.")


if __name__ == "__main__":
    main()
