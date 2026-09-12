"""Frozen, common-handoff comparison for successor_discrimination_v1.

Bare/native address the complete endpoint in one call. Matched/Mini locate the
issue and then discriminate its live readings in two calls, each within a
single episode. Custody checks do not adjudicate the resulting prose.
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
from minireason.campaign import source_identity as repository_source_identity
from minireason.provider import DeepSeek, Settings, digest, write_new
from .successor_data import STAGES, TEMPLATE_ID, template_contract

ARMS = ("bare", "native", "matched", "matched_native", "mini", "mini_native")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _signed(value: dict[str, Any], field: str) -> dict[str, Any]:
    return {**value, field: digest(value)}


def _verify(value: dict[str, Any], field: str) -> None:
    if type(value) is not dict or value.get(field) != digest({k:v for k,v in value.items() if k != field}):
        raise ValueError("SUCCESSOR_FROZEN_IDENTITY_CHANGED: " + field)


def load_frozen(path: Path) -> dict[str, Any]:
    value = loads_strict(Path(path).read_bytes().decode("utf-8"))
    if type(value) is not dict:
        raise ValueError("SUCCESSOR_FROZEN_OBJECT_REQUIRED")
    return value


def successor_source_identity() -> dict[str, Any]:
    files = {}
    for name in ("successor_data.py", "successor_study.py", "successor_mini.py", "template_chain.py"):
        path = Path(__file__).with_name(name)
        if not path.is_file():
            raise ValueError("SUCCESSOR_MODULE_MISSING: " + name)
        files[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"repository": repository_source_identity(), "probe_modules": files,
            "probe_sha256": digest(files)}


def _settings(raw: dict[str, Any], arm: str) -> Settings:
    if arm not in ARMS:
        raise ValueError("SUCCESSOR_UNKNOWN_ARM")
    base = Settings(model=raw["model"], base_url=raw["base_url"], thinking=False,
        reasoning_effort=raw["reasoning_effort"], max_tokens=raw["max_tokens"],
        timeout_seconds=raw["timeout_seconds"])
    if raw != base.to_dict():
        raise ValueError("SUCCESSOR_SETTINGS_UNSUPPORTED_OR_CHANGED")
    return Settings(model=base.model, base_url=base.base_url,
        thinking=arm in {"native", "matched_native", "mini_native"},
        reasoning_effort=base.reasoning_effort, max_tokens=base.max_tokens,
        timeout_seconds=base.timeout_seconds)


def _material(plan: dict[str, Any]) -> dict[str, Any]:
    return {"handoff_text":plan["handoff_text"], "stage_instructions":plan["stage_instructions"],
        "system_message":plan["system_message"], "max_tokens":plan["settings"]["max_tokens"]}


def make_plan(test_id: str, handoff: dict[str, Any], allocation_reason: str, *,
              arms: list[str] | None = None, settings: Settings | None = None) -> dict[str, Any]:
    """Derive B only from its verified handoff and pre-output chain allocation."""
    from .template_chain import verify_handoff, render_handoff
    verify_handoff(handoff)
    chain = handoff["chain_plan"]
    if type(test_id) is not str or not test_id.strip() or test_id != chain["b_test_id"]:
        raise ValueError("SUCCESSOR_PREDECLARED_TEST_ID_REQUIRED")
    if (type(allocation_reason) is not str or not allocation_reason.strip()
            or allocation_reason != chain["allocation_reason"]):
        raise ValueError("SUCCESSOR_PREDECLARED_ALLOCATION_REQUIRED")
    contract = template_contract()
    if chain["b_contract"] != contract:
        raise ValueError("SUCCESSOR_PREDECLARED_CONTRACT_CHANGED")
    chosen = list(chain["b_arms"] if arms is None else arms)
    if (not chosen or len(chosen) != len(set(chosen)) or not set(chosen) <= set(ARMS)
            or chosen != chain["b_arms"]):
        raise ValueError("SUCCESSOR_PREDECLARED_ARMS_REQUIRED")
    if type(chain["b_repetitions"]) is not int or chain["b_repetitions"] != 1:
        raise ValueError("SUCCESSOR_ONE_EPISODE_PER_ARM_REQUIRED")
    provider_settings = settings or _settings(chain["b_settings"], "bare")
    if provider_settings.to_dict() != chain["b_settings"]:
        raise ValueError("SUCCESSOR_PREDECLARED_SETTINGS_CHANGED")
    _settings(provider_settings.to_dict(), "bare")
    # Deep copy freezes caller-owned mutable objects independently of this plan.
    frozen_handoff = loads_strict(json.dumps(handoff, ensure_ascii=False))
    rendered = render_handoff(frozen_handoff)
    if type(rendered) is not str or not rendered.strip():
        raise ValueError("SUCCESSOR_HANDOFF_TEXT_REQUIRED")
    source = successor_source_identity()
    plan = {"schema":"minireason.successor-plan.v1", "test_id":test_id,
        "created_at":_now(), "template_id":TEMPLATE_ID, "template_contract":contract,
        "template_contract_id":digest(contract), "handoff":frozen_handoff,
        "handoff_id":handoff["handoff_id"], "handoff_text":rendered,
        "handoff_text_sha256":text_hash(rendered), "allocation_reason":allocation_reason,
        "arms":chosen, "repetitions":1, "cycles":1,
        "stage_instructions":dict(contract["stage_instructions"]),
        "baseline_instruction":contract["baseline_instruction"],
        "system_message":contract["system_message"], "settings":provider_settings.to_dict(),
        "max_concurrent_calls":5, "source":source, "content_appraisal":"unresolved",
        "standing_effect":"none", "proposed_changes_installed":False,
        "automatic_successor_started":False,
        "design_limits":[
            "Every B arm receives the same predeclared A mini-r01 whole-output handoff.",
            "Bare/native address the full followup endpoint once; matched/Mini locate then discriminate.",
            "Matched and Mini share actual conditional messages; routing alone identifies no reasoning advantage.",
            "Actual token costs and native reasoning differ; no scalar creativity or progress verdict is assigned.",
            "No-promotion and suspension prose are retained without automatic semantic adjudication or another episode."]}
    plan["prompt_policy_sha256"] = digest({"template_contract":contract,
        "renderer_source":source["probe_modules"]["successor_study.py"]})
    return _signed(plan, "plan_id")


def stage_prompt(material: dict[str, Any], stage: str, history: list[dict[str, Any]]) -> str:
    if stage in {"locate", "followup"}:
        if history:
            raise ValueError("SUCCESSOR_INITIAL_HISTORY_FORBIDDEN")
        instruction = material["baseline_instruction"] if stage == "followup" else material["stage_instructions"][stage]
    elif stage == "discriminate":
        if (len(history) != 1 or history[0].get("stage") != "locate"
                or type(history[0].get("text")) is not str or not history[0]["text"].strip()):
            raise ValueError("SUCCESSOR_EXACT_LOCATE_HISTORY_REQUIRED")
        instruction = material["stage_instructions"][stage]
    else:
        raise ValueError("SUCCESSOR_UNKNOWN_STAGE")
    parts = [instruction, "Whole verified parent handoff:\n" + material["handoff_text"]]
    if stage == "discriminate":
        parts.append("Actual preceding locate output:\n" + history[0]["text"])
    return "\n\n".join(parts)


def validate_response(answer: Any, max_tokens: int) -> str:
    if type(answer) is not dict or type(answer.get("content")) is not str or not answer["content"].strip():
        raise ValueError("SUCCESSOR_OUTPUT_UNAVAILABLE")
    usage = answer.get("usage")
    if type(usage) is not dict or any(type(usage.get(k)) is not int or usage[k] < 0 for k in ("prompt_tokens", "completion_tokens")):
        raise ValueError("SUCCESSOR_USAGE_UNAVAILABLE")
    if usage["completion_tokens"] > max_tokens:
        raise ValueError("SUCCESSOR_COMPLETION_CEILING_VIOLATED")
    if answer.get("finish_reason", "stop") != "stop":
        raise ValueError("SUCCESSOR_INCOMPLETE_GENERATION")
    if answer.get("status", "COMPLETE") != "COMPLETE":
        raise ValueError("SUCCESSOR_PROVIDER_REPORTED_FAILURE")
    return answer["content"]


def _output_occurrence(plan: dict[str, Any], arm: str, repeat: int, row: dict[str, Any],
                       previous: list[dict[str, Any]]) -> dict[str, Any]:
    stage = row["stage"]
    prompt = stage_prompt(plan, stage, previous)
    supplied = [plan["handoff_id"]]
    if stage == "discriminate":
        supplied.append(previous[0]["occurrence_id"])
    origin = {"test_id":plan["test_id"], "plan_id":plan["plan_id"], "template_id":TEMPLATE_ID,
        "arm":arm, "repeat":repeat, "stage":stage, "cycle":1,
        "mini_artifact_id":row.get("artifact_id"), "supplied_input_occurrence_ids":supplied,
        "input_provenance_meaning":"Exposure only; no semantic dependence, about or answers edge inferred",
        "prompt_sha256":text_hash(prompt), "system_sha256":text_hash(plan["system_message"])}
    return _signed({**row, "schema":"minireason.successor-occurrence.v1", "text_sha256":text_hash(row["text"]),
        "origin":origin, "content_appraisal":"unresolved", "standing_effect":"none",
        "proposed_changes_installed":False, "automatic_successor_started":False}, "occurrence_id")


def _resources(provider: Any) -> dict[str, int | None]:
    return {k:0 if provider is None else getattr(provider,k,None) for k in ("calls","prompt_tokens","completion_tokens")}


def _direct(provider: Any, plan: dict[str, Any], arm: str, repeat: int, root: Path,
            history: list[dict[str, Any]]) -> None:
    for stage in ("followup",) if arm in {"bare","native"} else STAGES:
        prompt = stage_prompt(plan,stage,history)
        write_new(root/(stage+".input.json"),{"stage":stage,"prompt":prompt,"prompt_sha256":text_hash(prompt),
            "system":plan["system_message"],"system_sha256":text_hash(plan["system_message"])})
        answer = provider.complete([{"role":"system","content":plan["system_message"]},
            {"role":"user","content":prompt}],json_output=False,
            coordinate={"stage":stage,"cycle":1,"phase":"raw-prose"})
        raw = validate_response(answer,plan["settings"]["max_tokens"])
        row = _output_occurrence(plan,arm,repeat,{"stage":stage,"cycle":1,"text":raw},history)
        write_new(root/(stage+".artifact.json"),row)
        history.append(row)


def _arm(plan: dict[str,Any],arm: str,repeat: int,root: Path,provider_factory: Callable[...,Any],prepared: Any) -> dict[str,Any]:
    root.mkdir(parents=True,exist_ok=False)
    settings = _settings(plan["settings"],arm)
    result = {"schema":"minireason.successor-arm.v1","arm":arm,"repeat":repeat,"plan_id":plan["plan_id"],
        "handoff_id":plan["handoff_id"],"started_at":_now(),"settings":settings.to_dict(),
        "status":"RUNNING","history":[],"alarms":[],"content_appraisal":"unresolved",
        "standing_effect":"none","proposed_changes_installed":False,"automatic_successor_started":False}
    write_new(root/"started.json",result)
    provider = None
    expected_stages = ["followup"] if arm in {"bare","native"} else list(STAGES)
    try:
        provider = provider_factory(settings,root/"calls")
        if provider.settings != settings:
            raise ValueError("SUCCESSOR_PROVIDER_SETTINGS_MISMATCH")
        if arm.startswith("mini"):
            from .successor_mini import run_successor
            routed = run_successor(provider,root,prepared=prepared,**_material(plan))
            result["route_schema"] = routed.get("schema")
            result["mini_route"] = {k:v for k,v in routed.items() if k != "history"}
            result["alarms"].extend(routed.get("alarms",[]))
            for row in routed["history"]:
                occurrence = _output_occurrence(plan,arm,repeat,row,result["history"])
                result["history"].append(occurrence)
                write_new(root/(row["stage"]+".artifact.json"),occurrence)
            if routed.get("status") != "COMPLETE":
                raise ValueError("SUCCESSOR_MINI_ROUTE_FAILURE")
        else:
            _direct(provider,plan,arm,repeat,root,result["history"])
        if [row["stage"] for row in result["history"]] != expected_stages:
            raise ValueError("SUCCESSOR_ROUTE_INCOMPLETE")
        result["status"] = "OBSERVATIONS_RECORDED" if not result["alarms"] else "OPERATIONAL_FAILURE"
    except Exception as error:
        result["status"] = "OPERATIONAL_FAILURE"
        result["alarms"].append({"code":getattr(error,"code",type(error).__name__),"detail":str(error)})
    resources = _resources(provider)
    if any(type(v) is not int or v < 0 for v in resources.values()):
        result["alarms"].append({"code":"SUCCESSOR_RESOURCE_ACCOUNTING_UNAVAILABLE","detail":"Missing counters are not zero cost"})
        result["status"] = "OPERATIONAL_FAILURE"
    elif result["status"] == "OBSERVATIONS_RECORDED" and resources["calls"] != len(expected_stages):
        result["alarms"].append({"code":"SUCCESSOR_CALL_ACCOUNTING_MISMATCH","detail":"Calls differ from declared stages"})
        result["status"] = "OPERATIONAL_FAILURE"
    result.update(resources=resources,ended_at=_now(),resource_accounting="Failed attempts count as calls; failed-delivery token cost may be unavailable. No retries.")
    write_new(root/"result.json",result)
    write_new(root/"errata.json",{"operational":result["alarms"],"semantic_findings":"Unadjudicated raw prose occurrences"})
    return result


def _preflight(plan: dict[str,Any],root: Path) -> tuple[Any,dict[str,Any]]:
    _verify(plan,"plan_id")
    rebuilt = make_plan(plan["test_id"],plan["handoff"],plan["allocation_reason"],
        arms=plan["arms"],settings=_settings(plan["settings"],"bare"))
    if set(plan) != set(rebuilt):
        raise ValueError("SUCCESSOR_PLAN_FIELDS_CHANGED")
    for key in set(rebuilt) - {"created_at","plan_id","source"}:
        if plan.get(key) != rebuilt[key]:
            raise ValueError("SUCCESSOR_PLAN_COMPONENT_MISMATCH: "+key)
    frozen, current = plan["source"], rebuilt["source"]
    if (frozen["probe_modules"] != current["probe_modules"] or frozen["probe_sha256"] != current["probe_sha256"]
            or frozen["repository"]["files"] != current["repository"]["files"]
            or frozen["repository"]["source_sha256"] != current["repository"]["source_sha256"]):
        raise ValueError("SUCCESSOR_SOURCE_CHANGED")
    for arm in plan["arms"]:
        _settings(plan["settings"],arm)
    stage_prompt(plan,"locate",[])
    stage_prompt(plan,"discriminate",[{"stage":"locate","text":"PREFLIGHT_LOCATE_PLACEHOLDER"}])
    stage_prompt(plan,"followup",[])
    prepared = None
    record = {"status":"CONFIGURATION_PREFLIGHT_PASSED","model_calls":0,"handoff_id":plan["handoff_id"],
        "handoff_text_sha256":plan["handoff_text_sha256"],"template_contract_id":plan["template_contract_id"],
        "content_appraisal":"unresolved","runtime_source":current,
        "publication_commit_change_permitted_if_source_bytes_unchanged":True}
    if any(arm.startswith("mini") for arm in plan["arms"]):
        from .successor_mini import prepare_successor
        prepared = prepare_successor(root/"preflight",**_material(plan))
        record["mini_prepared"] = prepared.summary()
    return prepared,record


def run_test(plan_path: Path,root: Path,*,jobs: int=5,provider_factory: Callable[...,Any]=DeepSeek) -> dict[str,Any]:
    if type(jobs) is not int or not 1 <= jobs <= 5:
        raise ValueError("JOBS_MUST_BE_ONE_TO_FIVE")
    plan = load_frozen(plan_path)
    root = Path(root)
    root.mkdir(parents=True,exist_ok=False)
    write_new(root/"plan.json",plan)
    prepared,rows = None,[]
    try:
        prepared,preflight = _preflight(plan,root)
    except Exception as error:
        preflight = {"status":"CONFIGURATION_PREFLIGHT_FAILED","model_calls":0,
            "alarm":{"code":getattr(error,"code",type(error).__name__),"detail":str(error)}}
    write_new(root/"preflight.json",preflight)
    if preflight["status"] == "CONFIGURATION_PREFLIGHT_PASSED":
        with ThreadPoolExecutor(max_workers=jobs) as pool:
            futures = [pool.submit(_arm,plan,arm,1,root/f"{arm}-r01",provider_factory,prepared) for arm in plan["arms"]]
            for future in as_completed(futures):
                rows.append(future.result())
    else:
        arms = [arm for arm in plan.get("arms",[]) if arm in ARMS] if isinstance(plan.get("arms"),list) else []
        for arm in dict.fromkeys(arms):
            row = {"schema":"minireason.successor-arm.v1","arm":arm,"repeat":1,"status":"OPERATIONAL_FAILURE",
                "history":[],"alarms":[preflight["alarm"]],"resources":_resources(None),
                "content_appraisal":"unresolved","standing_effect":"none","proposed_changes_installed":False,
                "automatic_successor_started":False}
            write_new(root/f"{arm}-r01/result.json",row)
            rows.append(row)
    summary = {"schema":"minireason.successor-test.v1","test_id":plan.get("test_id"),"plan_id":plan.get("plan_id"),
        "handoff_id":plan.get("handoff_id"),"preflight":preflight,
        "arms":[{key:row[key] for key in ("arm","repeat","status","resources")} for row in sorted(rows,key=lambda row:row["arm"])],
        "content_appraisal":"unresolved","standing_effect":"none","proposed_changes_installed":False,
        "automatic_successor_started":False,"completed_at":_now()}
    write_new(root/"summary.json",summary)
    write_new(root/"errata.json",{"operational":[{"arm":row["arm"],"repeat":row["repeat"],**alarm}
        for row in rows for alarm in row["alarms"]] or ([preflight["alarm"]] if "alarm" in preflight else []),
        "semantic_findings":"No automatic bearing, problem promotion, repair or creativity finding"})
    lines = ["# "+str(plan.get("test_id")),"","Frozen common-handoff successor-discrimination observations.","",
        "Preflight: "+preflight["status"]+".","","| Arm | Recording outcome | Calls | Completion tokens |",
        "|---|---|---:|---:|"]
    for row in summary["arms"]:
        lines.append(f"| {row['arm']} | {row['status']} | {row['resources']['calls']} | {row['resources']['completion_tokens']} |")
    lines += ["","Every arm receives the same predeclared complete A handoff. Bare/native address the full endpoint in one call; "
        "matched/Mini locate then discriminate in one separate episode. No-promotion is a legitimate prose result. "
        "No third episode starts and no semantic standing or language change is installed.",""]
    with (root/"REPORT.md").open("x",encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command",required=True)
    freeze = commands.add_parser("plan",help="Verify handoff and derive the predeclared B plan without calls")
    freeze.add_argument("--handoff",type=Path,required=True)
    freeze.add_argument("--output",type=Path,required=True)
    preflight = commands.add_parser("preflight",help="Reverify and compile exact B material without calls")
    preflight.add_argument("--plan",type=Path,required=True)
    preflight.add_argument("--output",type=Path,required=True)
    run = commands.add_parser("run")
    run.add_argument("--plan",type=Path,required=True)
    run.add_argument("--output",type=Path,required=True)
    run.add_argument("--jobs",type=int,default=5)
    args = parser.parse_args()
    if args.command == "plan":
        handoff = load_frozen(args.handoff)
        chain = handoff["chain_plan"]
        write_new(args.output,make_plan(chain["b_test_id"],handoff,chain["allocation_reason"]))
        print("Frozen B plan written. No model call was made.")
    elif args.command == "preflight":
        args.output.mkdir(parents=True,exist_ok=False)
        _,record = _preflight(load_frozen(args.plan),args.output)
        write_new(args.output/"preflight.json",record)
        print("Exact B material compiled and verified. No model call was made.")
    else:
        summary = run_test(args.plan,args.output,jobs=args.jobs)
        if summary["preflight"]["status"] != "CONFIGURATION_PREFLIGHT_PASSED" or any(row["status"] != "OBSERVATIONS_RECORDED" for row in summary["arms"]):
            raise SystemExit("Operational failure recorded; review and publish before successor work.")
        print("Observations recorded without semantic adjudication. Review and publish the record.")


if __name__ == "__main__":
    main()
