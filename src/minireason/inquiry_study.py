"""Bounded inquiry with frozen material, matched controls and unresolved promotion.

Freeze a supplied occurrence and material, then compare one construction call
with construct/criticize/revise/promote workflows. No model answer is graded,
installed, parsed into a clean issue, or assigned semantic standing by this host.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

from minireason.campaign import source_identity as repository_source_identity
from minireason.language_data import RAW_SYSTEM, INSTRUCTIONS
from minireason.language_study import selected_language
from minireason.provider import DeepSeek, Settings, digest, write_new
from creib.strict_json import loads_strict

from .inquiry_data import STAGE_INSTRUCTIONS

STAGES = ("construct", "criticize", "revise", "promote")
ARMS = ("bare", "native", "matched", "matched_native", "mini", "mini_native")
CARRIERS = ("prose", "lean_candidate", "nonlean_candidate")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _signed(value: dict[str, Any], field: str) -> dict[str, Any]:
    return {**value, field: digest(value)}


def _verify(value: dict[str, Any], field: str) -> None:
    if value.get(field) != digest({key: item for key, item in value.items() if key != field}):
        raise ValueError(f"FROZEN_IDENTITY_CHANGED: {field}")


def load_frozen(path: Path) -> dict[str, Any]:
    result = loads_strict(path.read_bytes().decode("utf-8"))
    if type(result) is not dict:
        raise ValueError("FROZEN_OBJECT_REQUIRED")
    return result


def inquiry_source_identity() -> dict[str, Any]:
    """Bind the installed inquiry modules along with the engine and provider."""
    return repository_source_identity()


def freeze_occurrence(text: str, origin: dict[str, Any], packet_id: str) -> dict[str, Any]:
    """Preserve an entire supplied occurrence without guessing its semantic role."""
    if type(text) is not str or not text.strip():
        raise ValueError("NONEMPTY_OCCURRENCE_REQUIRED")
    if type(origin) is not dict or not origin:
        raise ValueError("ORIGIN_METADATA_REQUIRED")
    if type(packet_id) is not str or len(packet_id) != 64:
        raise ValueError("PACKET_ID_REQUIRED")
    return _signed({"schema": "minireason.inquiry-occurrence.v1", "text": text,
                    "text_sha256": text_hash(text), "origin": origin, "packet_id": packet_id,
                    "content_appraisal": "unresolved", "standing_effect": "none",
                    "disposition": "queued"}, "occurrence_id")


def _verify_occurrence(occurrence: dict[str, Any], packet_id: str) -> None:
    _verify(occurrence, "occurrence_id")
    if occurrence.get("packet_id") != packet_id:
        raise ValueError("OCCURRENCE_PACKET_MISMATCH")
    raw = occurrence.get("text")
    if type(raw) is not str or not raw.strip() or occurrence.get("text_sha256") != text_hash(raw):
        raise ValueError("OCCURRENCE_TEXT_MISMATCH")
    if type(occurrence.get("origin")) is not dict or not occurrence["origin"]:
        raise ValueError("ORIGIN_METADATA_REQUIRED")


def _settings(raw: dict[str, Any], arm: str) -> Settings:
    return Settings(model=raw["model"], base_url=raw["base_url"],
                    thinking=arm in {"native", "matched_native", "mini_native"},
                    reasoning_effort=raw["reasoning_effort"], max_tokens=raw["max_tokens"],
                    timeout_seconds=raw["timeout_seconds"])


def _snapshots(plan: dict[str, Any]) -> dict[str, Any]:
    return {key: {"sha256": text_hash(plan[key]), "utf8_bytes": len(plan[key].encode("utf-8")),
                  "characters": len(plan[key])}
            for key in ("packet_text", "selected_language_text", "issue_text", "parent_material_text")}


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)


def make_plan(test_id: str, packet: dict[str, Any], issue: dict[str, Any], carrier: str,
              allocation_reason: str, *, parents: list[dict[str, Any]] | None = None,
              arms: list[str] | None = None, max_tokens: int = 16384,
              repetitions: int = 1, parent_test: str | None = None) -> dict[str, Any]:
    _verify(packet, "packet_id")
    _verify(packet["corpus"], "corpus_id")
    _verify_occurrence(issue, packet["packet_id"])
    if type(test_id) is not str or not test_id.strip():
        raise ValueError("TEST_ID_REQUIRED")
    if carrier not in CARRIERS:
        raise ValueError("UNKNOWN_CARRIER")
    if issue["packet_id"] != packet["packet_id"]:
        raise ValueError("ISSUE_PACKET_MISMATCH")
    if type(allocation_reason) is not str or not allocation_reason.strip():
        raise ValueError("ALLOCATION_REASON_REQUIRED")
    chosen = list(ARMS) if arms is None else list(arms)
    if not chosen or not set(chosen) <= set(ARMS) or len(chosen) != len(set(chosen)):
        raise ValueError("INVALID_OR_DUPLICATE_ARMS")
    if type(repetitions) is not int or not 1 <= repetitions <= 20:
        raise ValueError("INVALID_REPETITIONS")
    frozen_parents = [] if parents is None else parents
    for parent in frozen_parents:
        _verify_occurrence(parent, packet["packet_id"])
    activation = {"occurrence_id": issue["occurrence_id"], "allocation_reason": allocation_reason,
                  "successor_test_id": test_id, "disposition": "selected_for_inquiry",
                  "content_appraisal": "unresolved", "standing_effect": "none"}
    settings = Settings(max_tokens=max_tokens)
    plan = {"schema": "minireason.inquiry-plan.v1", "test_id": test_id,
            "created_at": _now(), "parent_test": parent_test,
            "template_id": "joint_construction_v1", "packet": packet,
            "packet_id": packet["packet_id"], "issue": issue, "activation": activation,
            "parents": frozen_parents, "carrier": carrier,
            "packet_text": _canonical(packet),
            "selected_language_text": selected_language(packet, carrier),
            "issue_text": _canonical({"occurrence": issue, "activation": activation}),
            "parent_material_text": _canonical(frozen_parents),
            "carrier_directive": INSTRUCTIONS["carrier_directives"][carrier],
            "stage_instructions": dict(STAGE_INSTRUCTIONS), "settings": settings.to_dict(),
            "arms": chosen, "repetitions": repetitions, "cycles": 1,
            "max_concurrent_calls": 5, "source": inquiry_source_identity(),
            "interpretation": "Bounded construction inquiry; no automatic bearing, repair, adequacy or creativity finding",
            "protected_specimens": {"corpus_id": packet["corpus"]["corpus_id"], "packet_id": packet["packet_id"],
                "installation_policy": "C0 and L0 remain unchanged; every new output is a separate occurrence"},
            "design_limits": ["Bare/native construct once; matched/Mini make four calls under identical conditional request policy.",
                "The same frozen issue and reason are supplied to every arm; this does not test which issue a promotion policy would select.",
                "A promoted occurrence is retained whole and queued unresolved; no successor episode starts automatically.",
                "Input provenance records exposure only. No about or answers edges are inferred.",
                "Native reasoning and actual token use are not equalized; resource ceilings and usage are recorded."]}
    plan["material_snapshots"] = _snapshots(plan)
    return _signed(plan, "plan_id")


def stage_prompt(plan: dict[str, Any], stage: str, history: list[dict[str, Any]]) -> str:
    if stage not in STAGES:
        raise ValueError("UNKNOWN_INQUIRY_STAGE")
    parts = [plan["carrier_directive"], plan["stage_instructions"][stage],
             "Frozen original packet:\n" + plan["packet_text"],
             "Selected frozen carrier:\n" + plan["selected_language_text"],
             "Selected occurrence and allocation record:\n" + plan["issue_text"],
             "Frozen parent material:\n" + plan["parent_material_text"]]
    for earlier in STAGES[:STAGES.index(stage)]:
        matches = [row["text"] for row in history if row["stage"] == earlier]
        if len(matches) != 1:
            raise ValueError("INQUIRY_HISTORY_MISSING_OR_DUPLICATE: " + earlier)
        parts.append(f"Actual {earlier} occurrence:\n" + matches[0])
    return "\n\n".join(parts)


def _material(plan: dict[str, Any]) -> dict[str, Any]:
    return {**{key: plan[key] for key in ("packet_text", "selected_language_text", "issue_text",
             "parent_material_text", "carrier_directive", "stage_instructions")},
             "max_tokens": plan["settings"]["max_tokens"]}


def _resources(provider: Any) -> dict[str, int | None]:
    # Missing accounting is unavailable, never a reported zero-cost run.
    return {key: 0 if provider is None else getattr(provider, key, None)
            for key in ("calls", "prompt_tokens", "completion_tokens")}


def validate_response(answer: Any, max_tokens: int) -> str:
    """Enforce only transport and resource observations, never prose semantics."""
    if type(answer) is not dict or type(answer.get("content")) is not str or not answer["content"].strip():
        raise ValueError("INQUIRY_OUTPUT_UNAVAILABLE: provider record retained")
    usage = answer.get("usage")
    if type(usage) is not dict or any(type(usage.get(key)) is not int or usage[key] < 0
                                    for key in ("prompt_tokens", "completion_tokens")):
        raise ValueError("INQUIRY_USAGE_UNAVAILABLE: provider record retained")
    if usage["completion_tokens"] > max_tokens:
        raise ValueError("INQUIRY_COMPLETION_CEILING_VIOLATED: provider record retained")
    return answer["content"]


def _output_occurrence(plan: dict[str, Any], arm: str, repeat: int,
                       row: dict[str, Any], preceding: list[dict[str, Any]]) -> dict[str, Any]:
    origin = {"test_id": plan["test_id"], "arm": arm, "repeat": repeat,
              "stage": row["stage"], "cycle": 1, "plan_id": plan["plan_id"],
              "mini_artifact_id": row.get("artifact_id"),
              "supplied_input_occurrence_ids": [plan["issue"]["occurrence_id"]]
                  + [parent["occurrence_id"] for parent in plan["parents"]]
                  + [previous["occurrence_id"] for previous in preceding],
              "input_provenance_meaning": "Supplied material only; no semantic dependency, about or answers edge implied"}
    occurrence = freeze_occurrence(row["text"], origin, plan["packet_id"])
    # The queued object is the full artifact record, including route metadata.
    # Sign that complete object so it can be selected unchanged in a later plan.
    return _signed({**row, **{key: value for key, value in occurrence.items() if key != "occurrence_id"}}, "occurrence_id")


def _direct(provider: Any, plan: dict[str, Any], arm: str, repeat: int,
            root: Path, history: list[dict[str, Any]]) -> None:
    stages = STAGES[:1] if arm in {"bare", "native"} else STAGES
    for stage in stages:
        prompt = stage_prompt(plan, stage, history)
        write_new(root / f"{stage}.input.json", {"stage": stage, "prompt": prompt,
                  "prompt_sha256": text_hash(prompt), "system": RAW_SYSTEM})
        answer = provider.complete([{"role": "system", "content": RAW_SYSTEM},
                  {"role": "user", "content": prompt}], json_output=False,
                  coordinate={"stage": stage, "carrier": plan["carrier"], "phase": "raw-prose"})
        raw = validate_response(answer, plan["settings"]["max_tokens"])
        row = {"stage": stage, "text": raw, "text_sha256": text_hash(raw),
               "proposed_changes_installed": False}
        row.update(_output_occurrence(plan, arm, repeat, row, history))
        write_new(root / f"{stage}.artifact.json", row)
        history.append(row)


def _arm(plan: dict[str, Any], arm: str, repeat: int, root: Path,
         provider_factory: Callable[..., Any], prepared: Any) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=False)
    settings = _settings(plan["settings"], arm)
    result: dict[str, Any] = {"schema": "minireason.inquiry-arm.v1", "arm": arm,
        "repeat": repeat, "plan_id": plan["plan_id"], "packet_id": plan["packet_id"],
        "started_at": _now(), "settings": settings.to_dict(), "history": [], "alarms": [],
        "status": "RUNNING", "content_appraisal": "unresolved", "standing_effect": "none",
        "proposed_changes_installed": False, "activation": plan["activation"]}
    write_new(root / "started.json", result)
    provider = None
    try:
        provider = provider_factory(settings, root / "calls")
        if provider.settings != settings:
            raise ValueError("INQUIRY_PROVIDER_SETTINGS_MISMATCH")
        if arm.startswith("mini"):
            from .inquiry_mini import run_inquiry
            routed = run_inquiry(provider, root, **_material(plan), prepared=prepared)
            result.update({key: value for key, value in routed.items()
                           if key not in {"schema", "history", "content_appraisal", "standing_effect", "proposed_changes_installed"}})
            result["route_schema"] = routed.get("schema")
            for row in routed["history"]:
                decorated = {**row, **_output_occurrence(plan, arm, repeat, row, result["history"])}
                result["history"].append(decorated)
                write_new(root / f"{row['stage']}.artifact.json", decorated)
        else:
            _direct(provider, plan, arm, repeat, root, result["history"])
        expected = 1 if arm in {"bare", "native"} else 4
        if len(result["history"]) != expected:
            raise ValueError("INQUIRY_ROUTE_INCOMPLETE")
        result["status"] = "OBSERVATIONS_RECORDED" if not result["alarms"] else "OPERATIONAL_FAILURE"
    except Exception as error:
        result["status"] = "OPERATIONAL_FAILURE"
        result["alarms"].append({"code": getattr(error, "code", type(error).__name__), "detail": str(error)})
    queued = [row for row in result["history"] if row["stage"] == "promote"]
    write_new(root / "inquiry-queue.json", {"schema": "minireason.inquiry-queue.v1",
        "occurrences": queued, "automatic_successor_started": False,
        "content_appraisal": "unresolved", "standing_effect": "none",
        "interpretation": "The entire promotion output is queued. Whether it identifies a useful inquiry remains a question."})
    resources = _resources(provider)
    if any(type(value) is not int or value < 0 for value in resources.values()):
        result["alarms"].append({"code": "INQUIRY_RESOURCE_ACCOUNTING_UNAVAILABLE",
                                "detail": "Provider counters are missing or malformed; unknown costs are not zero."})
        result["status"] = "OPERATIONAL_FAILURE"
    elif result["status"] == "OBSERVATIONS_RECORDED" and resources["calls"] != expected:
        result["alarms"].append({"code": "INQUIRY_CALL_ACCOUNTING_MISMATCH",
                                "detail": "Reported provider calls differ from the declared completed stages."})
        result["status"] = "OPERATIONAL_FAILURE"
    result.update({"resources": resources, "ended_at": _now(),
        "resource_accounting": "Calls include failed attempts; tokens are provider-reported totals only. Failed deliveries may have unknown cost."})
    write_new(root / "result.json", result)
    write_new(root / "errata.json", {"operational": result["alarms"],
        "semantic_findings": "Unadjudicated; inspect exact constructions, criticisms, proposals and queued occurrences"})
    return result


def _preflight(plan: dict[str, Any], root: Path) -> tuple[Any, dict[str, Any]]:
    _verify(plan["packet"], "packet_id")
    _verify(plan["packet"]["corpus"], "corpus_id")
    if plan["packet_id"] != plan["packet"]["packet_id"]:
        raise ValueError("PACKET_ID_MISMATCH")
    _verify_occurrence(plan["issue"], plan["packet_id"])
    for parent in plan["parents"]:
        _verify_occurrence(parent, plan["packet_id"])
    arms = plan["arms"]
    if not arms or not set(arms) <= set(ARMS) or len(arms) != len(set(arms)):
        raise ValueError("INVALID_OR_DUPLICATE_ARMS")
    if type(plan["repetitions"]) is not int or not 1 <= plan["repetitions"] <= 20:
        raise ValueError("INVALID_REPETITIONS")
    if plan["cycles"] != 1 or plan["max_concurrent_calls"] != 5:
        raise ValueError("INQUIRY_RESOURCE_CONTRACT_MISMATCH")
    if plan["carrier"] not in CARRIERS:
        raise ValueError("UNKNOWN_CARRIER")
    if plan["carrier_directive"] != INSTRUCTIONS["carrier_directives"][plan["carrier"]]:
        raise ValueError("CARRIER_DIRECTIVE_MISMATCH")
    activation = plan["activation"]
    if (activation.get("occurrence_id") != plan["issue"]["occurrence_id"]
            or activation.get("successor_test_id") != plan["test_id"]
            or activation.get("disposition") != "selected_for_inquiry"
            or activation.get("standing_effect") != "none"
            or activation.get("content_appraisal") != "unresolved"
            or type(activation.get("allocation_reason")) is not str
            or not activation["allocation_reason"].strip()):
        raise ValueError("INQUIRY_ACTIVATION_MISMATCH")
    for arm in arms:
        _settings(plan["settings"], arm)
    if plan["packet_text"] != _canonical(plan["packet"]):
        raise ValueError("PACKET_TEXT_MISMATCH")
    if plan["selected_language_text"] != selected_language(plan["packet"], plan["carrier"]):
        raise ValueError("LANGUAGE_TEXT_MISMATCH")
    if plan["issue_text"] != _canonical({"occurrence": plan["issue"], "activation": plan["activation"]}):
        raise ValueError("ISSUE_TEXT_MISMATCH")
    if plan["parent_material_text"] != _canonical(plan["parents"]):
        raise ValueError("PARENT_TEXT_MISMATCH")
    if plan["material_snapshots"] != _snapshots(plan):
        raise ValueError("MATERIAL_SNAPSHOT_MISMATCH")
    placeholders = [{"stage": stage, "text": f"PREFLIGHT_{stage}"} for stage in STAGES]
    for stage in STAGES:
        stage_prompt(plan, stage, placeholders)
    prepared = None
    record: dict[str, Any] = {"status": "CONFIGURATION_PREFLIGHT_PASSED", "model_calls": 0,
        "material_snapshots": plan["material_snapshots"], "content_appraisal": "unresolved"}
    if any(arm.startswith("mini") for arm in plan["arms"]):
        from .inquiry_mini import prepare_inquiry
        prepared = prepare_inquiry(root / "preflight", **_material(plan))
        record["mini"] = prepared.summary()
    return prepared, record


def run_test(plan_path: Path, root: Path, *, jobs: int = 5,
             provider_factory: Callable[..., Any] = DeepSeek) -> dict[str, Any]:
    if type(jobs) is not int or not 1 <= jobs <= 5:
        raise ValueError("CONCURRENCY_MUST_BE_ONE_TO_FIVE")
    plan = load_frozen(plan_path)
    _verify(plan, "plan_id")
    if plan["source"]["source_sha256"] != inquiry_source_identity()["source_sha256"]:
        raise ValueError("SOURCE_CHANGED_SINCE_PLAN")
    if plan["schema"] != "minireason.inquiry-plan.v1":
        raise ValueError("INQUIRY_PLAN_REQUIRED")
    root.mkdir(parents=True, exist_ok=False)
    write_new(root / "plan.json", plan)
    write_new(root / "packet.json", plan["packet"])
    write_new(root / "selected-occurrence.json", plan["issue"])
    write_new(root / "activation.json", plan["activation"])
    write_new(root / "parents.json", plan["parents"])
    write_new(root / "started.json", {"test_id": plan["test_id"], "status": "CONFIGURATION_PREFLIGHT", "started_at": _now()})
    rows = []
    try:
        prepared, preflight = _preflight(plan, root)
    except Exception as error:
        alarm = {"code": "CONFIGURATION_PREFLIGHT_FAILED", "cause_code": getattr(error, "code", type(error).__name__), "detail": str(error)}
        preflight = {"status": "CONFIGURATION_PREFLIGHT_FAILED", "alarms": [alarm], "model_calls": 0}
        for repeat in range(1, plan["repetitions"] + 1):
            for arm in plan["arms"]:
                row = {"schema": "minireason.inquiry-arm.v1", "arm": arm, "repeat": repeat,
                    "status": "CONFIGURATION_PREFLIGHT_FAILED", "plan_id": plan["plan_id"], "history": [],
                    "alarms": [alarm], "resources": {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0}}
                write_new(root / f"{arm}-r{repeat:02d}/result.json", row)
                write_new(root / f"{arm}-r{repeat:02d}/errata.json", {"operational": [alarm]})
                rows.append(row)
    write_new(root / "preflight.json", preflight)
    if preflight["status"] == "CONFIGURATION_PREFLIGHT_PASSED":
        with ThreadPoolExecutor(max_workers=jobs) as pool:
            futures = [pool.submit(_arm, plan, arm, repeat, root / f"{arm}-r{repeat:02d}", provider_factory, prepared)
                for repeat in range(1, plan["repetitions"] + 1) for arm in plan["arms"]]
            for future in as_completed(futures):
                rows.append(future.result())
    summary = {"schema": "minireason.inquiry-test.v1", "test_id": plan["test_id"],
        "plan_id": plan["plan_id"], "packet_id": plan["packet_id"], "preflight": preflight,
        "arms": [{key: row[key] for key in ("arm", "repeat", "status", "resources")}
                 for row in sorted(rows, key=lambda row: (row["repeat"], row["arm"]))],
        "content_appraisal": "unresolved", "standing_effect": "none", "proposed_changes_installed": False,
        "completed_at": _now()}
    write_new(root / "summary.json", summary)
    write_new(root / "errata.json", {"operational": [{"arm": row["arm"], "repeat": row["repeat"], **alarm}
        for row in rows for alarm in row["alarms"]], "semantic_findings": "No automatic bearing, repair or creativity finding"})
    lines = [f"# {plan['test_id']}", "", "Bounded joint-construction inquiry; no proposal was installed.", "",
             f"Configuration preflight: {preflight['status']}.", "", plan["activation"]["allocation_reason"], "",
             "| Arm | Repeat | Recording outcome | Calls | Completion tokens |", "|---|---:|---|---:|---:|"]
    for row in summary["arms"]:
        lines.append(f"| {row['arm']} | {row['repeat']} | {row['status']} | {row['resources']['calls']} | {row['resources']['completion_tokens']} |")
    lines += ["", "C0, L0 and the selected occurrence remain unchanged. Every new output is a separate occurrence. "
              "The whole promotion output is queued unresolved; no successor is automatically activated, and no about/answers edges or semantic standing changes are inferred. "
              "Inspect the original artifacts and input provenance before choosing a subsequent inquiry.", ""]
    (root / "REPORT.md").write_text("\n".join(lines))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    freeze = commands.add_parser("freeze-occurrence")
    freeze.add_argument("--text", type=Path, required=True)
    freeze.add_argument("--origin", type=Path, required=True)
    freeze.add_argument("--packet", type=Path, required=True)
    freeze.add_argument("--output", type=Path, required=True)
    plan = commands.add_parser("plan")
    plan.add_argument("--id", required=True)
    plan.add_argument("--packet", type=Path, required=True)
    plan.add_argument("--issue", type=Path, required=True)
    plan.add_argument("--carrier", choices=CARRIERS, required=True)
    plan.add_argument("--allocation-reason", required=True)
    plan.add_argument("--parents", type=Path, nargs="*", default=[])
    plan.add_argument("--arms", choices=ARMS, nargs="+")
    plan.add_argument("--max-tokens", type=int, default=16384)
    plan.add_argument("--repetitions", type=int, default=1)
    plan.add_argument("--parent-test")
    plan.add_argument("--output", type=Path, required=True)
    run = commands.add_parser("run")
    run.add_argument("--plan", type=Path, required=True)
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--jobs", type=int, default=5)
    args = parser.parse_args()
    if args.command == "freeze-occurrence":
        packet = load_frozen(args.packet)
        _verify(packet, "packet_id")
        write_new(args.output, freeze_occurrence(args.text.read_bytes().decode("utf-8"),
                  load_frozen(args.origin), packet["packet_id"]))
    elif args.command == "plan":
        write_new(args.output, make_plan(args.id, load_frozen(args.packet), load_frozen(args.issue),
                  args.carrier, args.allocation_reason, parents=[load_frozen(path) for path in args.parents],
                  arms=args.arms, max_tokens=args.max_tokens, repetitions=args.repetitions, parent_test=args.parent_test))
    else:
        summary = run_test(args.plan, args.output, jobs=args.jobs)
        if (summary["preflight"]["status"] != "CONFIGURATION_PREFLIGHT_PASSED"
                or any(row["status"] != "OBSERVATIONS_RECORDED" for row in summary["arms"])):
            print("Operational failure recorded. Review and publish its evidence before any successor.")
            raise SystemExit(1)
        print("Recording complete. Review and publish the record before starting a successor.")
        return
    print("Frozen input written; no model call was made.")


if __name__ == "__main__":
    main()
