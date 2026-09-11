"""Candidate fixed-construction reason response and isolated account-use probe.

No experiment variants are selected here. Plans carry exact attributed inputs,
critic relation declarations, minimal use data and questions supplied separately.
The second request gets declared use material and a predeclared present or empty
returned-account field. The prior response is always retained in the archive.
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
from .reason_use_data import SYSTEM_MESSAGE, STAGE_INSTRUCTIONS

STAGES = ("respond", "use")
ARMS = ("bare", "native", "matched", "matched_native", "mini", "mini_native")
INPUTS = ("source", "construction", "original_criticism", "criticism", "use_data", "use_questions")
MATERIAL_FIELDS = ("source_text", "construction_text", "criticism_text", "use_data_text", "use_questions_text")
RELATIONS = ("original", "recoded", "different", "omitted")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _signed(value: dict[str, Any], field: str) -> dict[str, Any]:
    return {**value, field: digest(value)}


def _verify(value: dict[str, Any], field: str) -> None:
    if type(value) is not dict or value.get(field) != digest({k:v for k,v in value.items() if k != field}):
        raise ValueError("FROZEN_IDENTITY_CHANGED: " + field)


def load_frozen(path: Path) -> dict[str, Any]:
    value = loads_strict(Path(path).read_bytes().decode("utf-8"))
    if type(value) is not dict:
        raise ValueError("FROZEN_OBJECT_REQUIRED")
    return value


def freeze_occurrence(text: str, origin: dict[str, Any], *, allow_empty: bool = False) -> dict[str, Any]:
    if type(text) is not str or (not text.strip() and not (allow_empty and text == "")):
        raise ValueError("NONEMPTY_OCCURRENCE_REQUIRED")
    if type(origin) is not dict or not origin:
        raise ValueError("ORIGIN_METADATA_REQUIRED")
    return _signed({"schema": "minireason.reason-use-occurrence.v1", "text": text,
        "text_sha256": text_hash(text), "origin": origin, "content_appraisal": "unresolved",
        "standing_effect": "none", "proposed_changes_installed": False}, "occurrence_id")


def _verify_occurrence(value: dict[str, Any], *, allow_empty: bool = False) -> None:
    _verify(value, "occurrence_id")
    reconstructed = freeze_occurrence(value.get("text"), value.get("origin"), allow_empty=allow_empty)
    for field in ("schema", "text_sha256", "content_appraisal", "standing_effect", "proposed_changes_installed"):
        if value.get(field) != reconstructed[field]:
            raise ValueError("OCCURRENCE_BINDING_MISMATCH: " + field)


def reason_use_source_identity() -> dict[str, Any]:
    """Include overlay modules while staged, and all repository engine/provider sources."""
    files = {}
    for name in ("reason_use_data.py", "reason_use_study.py", "reason_use_mini.py"):
        path = Path(__file__).with_name(name)
        if not path.is_file():
            raise ValueError("REASON_USE_MODULE_MISSING: " + name)
        files[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"repository": repository_source_identity(), "probe_modules": files,
            "probe_sha256": digest(files)}


def _settings(raw: dict[str, Any], arm: str) -> Settings:
    base = Settings(model=raw["model"], base_url=raw["base_url"], thinking=False,
        reasoning_effort=raw["reasoning_effort"], max_tokens=raw["max_tokens"],
        timeout_seconds=raw["timeout_seconds"])
    if raw != base.to_dict():
        raise ValueError("REASON_USE_SETTINGS_UNSUPPORTED_OR_CHANGED")
    return Settings(model=base.model, base_url=base.base_url,
        thinking=arm in {"native", "matched_native", "mini_native"},
        reasoning_effort=base.reasoning_effort, max_tokens=base.max_tokens,
        timeout_seconds=base.timeout_seconds)


def _text_views(text: str) -> list[str]:
    """Literal and recursively JSON-decoded strings, without semantic inference."""
    views = [text]
    try:
        value = json.loads(text, object_pairs_hook=list)
    except Exception:
        return views
    def visit(item: Any) -> None:
        if isinstance(item, str):
            views.append(item)
        elif isinstance(item, (list, tuple)):
            for child in item:
                visit(child)
        elif isinstance(item, dict):
            for key, child in item.items():
                views.append(key)
                visit(child)
    visit(value)
    return views


def audit_leakage(inputs: dict[str, Any], instructions: dict[str, str], system: str,
                  exclusions: list[dict[str, str]], *, return_path: bool = True) -> dict[str, Any]:
    """Refuse declared literal leakage; shared meanings remain a reviewer question."""
    original = inputs["original_criticism"]["text"]
    changed = inputs["criticism"]["text"]
    construction = inputs["construction"]["text"]
    checked = {name: inputs[name]["text"] for name in ("source", "construction", "use_data", "use_questions")}
    checked.update({"system": system, **{"instruction_" + k:v for k,v in instructions.items()}})
    needles = [("whole_original_criticism", original)]
    for item in exclusions:
        if (type(item) is not dict or set(item) != {"name", "text"}
                or type(item["name"]) is not str or not item["name"].strip()
                or type(item["text"]) is not str or len(item["text"]) < 32):
            raise ValueError("INVALID_LITERAL_LEAKAGE_EXCLUSION")
        needles.append((item["name"], item["text"]))
    findings = []
    for name, text in checked.items():
        for label, needle in needles:
            if any(needle in view for view in _text_views(text)):
                findings.append({"field": name, "forbidden_occurrence": label})
    # Use material cannot smuggle in either the original construction or the selected critic.
    for name in ("use_data", "use_questions", "system", "instruction_use"):
        for label, needle in (("whole_construction", construction), ("whole_selected_criticism", changed)):
            if needle and any(needle in view for view in _text_views(checked[name])):
                findings.append({"field": name, "forbidden_occurrence": label})
    if findings:
        raise ValueError("REASON_USE_INPUT_LEAKAGE: " + json.dumps(findings, sort_keys=True))
    return {"status": "DECLARED_LITERAL_EXCLUSIONS_PASSED", "checked_fields": list(checked),
        "excluded_identities": {label:text_hash(needle) for label,needle in needles},
        "selected_criticism_supplied_only_in": "respond.criticism_text",
        "use_ports": ["use_data_text", "use_questions_text"] + (["actual_respond_output"] if return_path else []),
        "return_path": return_path,
        "inspection_limit": "Exact whole-occurrence and declared literal exclusions, including decoded JSON strings; no guarantee against paraphrase, quotation of undeclared excerpts, or arguments already present in the common source.",
        "output_echo_policy": "The exact produced account may itself repeat source, construction or criticism; it is not censored, and such carriage remains attributable to the response."}


def _material(plan: dict[str, Any]) -> dict[str, Any]:
    return {**{key:plan[key] for key in MATERIAL_FIELDS},
        "stage_instructions": plan["stage_instructions"], "system_message": plan["system_message"],
        "max_tokens": plan["settings"]["max_tokens"], "return_path": plan["return_path"]}


def _snapshots(plan: dict[str, Any]) -> dict[str, Any]:
    return {key:{"sha256":text_hash(plan[key]), "utf8_bytes":len(plan[key].encode("utf-8"))}
            for key in MATERIAL_FIELDS}


def make_plan(test_id: str, inputs: dict[str, dict[str, Any]], criticism_relation: str,
              allocation_reason: str, *, arms: list[str] | None = None, max_tokens: int = 32768,
              repetitions: int = 1, parent_test: str | None = None,
              stage_instructions: dict[str, str] | None = None, system_message: str = SYSTEM_MESSAGE,
              literal_exclusions: list[dict[str, str]] | None = None,
              settings: Settings | None = None, return_path: bool = True) -> dict[str, Any]:
    if type(inputs) is not dict or set(inputs) != set(INPUTS):
        raise ValueError("EXACT_REASON_USE_INPUT_SET_REQUIRED")
    for key,value in inputs.items():
        _verify_occurrence(value, allow_empty=key == "criticism")
    if type(test_id) is not str or not test_id.strip():
        raise ValueError("TEST_ID_REQUIRED")
    if type(allocation_reason) is not str or not allocation_reason.strip():
        raise ValueError("ALLOCATION_REASON_REQUIRED")
    if type(return_path) is not bool:
        raise ValueError("RETURN_PATH_MUST_BE_BOOLEAN")
    if criticism_relation not in RELATIONS:
        raise ValueError("UNKNOWN_CRITICISM_RELATION")
    chosen = list(ARMS) if arms is None else list(arms)
    if not chosen or len(chosen) != len(set(chosen)) or not set(chosen) <= set(ARMS):
        raise ValueError("INVALID_OR_DUPLICATE_ARMS")
    if type(repetitions) is not int or not 1 <= repetitions <= 20:
        raise ValueError("INVALID_REPETITIONS")
    raw, original = inputs["criticism"]["text"], inputs["original_criticism"]["text"]
    if (criticism_relation == "omitted") != (raw == ""):
        raise ValueError("CRITICISM_OMISSION_MISMATCH")
    if criticism_relation == "original" and raw != original:
        raise ValueError("ORIGINAL_CRITICISM_MISMATCH")
    if criticism_relation in {"recoded", "different"} and raw == original:
        raise ValueError("CHANGED_CRITICISM_BYTES_REQUIRED")
    instructions = dict(STAGE_INSTRUCTIONS if stage_instructions is None else stage_instructions)
    if set(instructions) != set(STAGES) or any(type(v) is not str or not v.strip() for v in instructions.values()):
        raise ValueError("EXACT_STAGE_INSTRUCTIONS_REQUIRED")
    if type(system_message) is not str or not system_message.strip():
        raise ValueError("SYSTEM_MESSAGE_REQUIRED")
    exclusions = [] if literal_exclusions is None else literal_exclusions
    audit = audit_leakage(inputs, instructions, system_message, exclusions, return_path=return_path)
    provider_settings = settings or Settings(max_tokens=max_tokens)
    if provider_settings.thinking or provider_settings.max_tokens != max_tokens:
        raise ValueError("BASE_SETTINGS_MISMATCH")
    plan = {"schema":"minireason.reason-use-plan.v1", "test_id":test_id, "parent_test":parent_test,
        "created_at":_now(), "inputs":inputs, "criticism_relation":criticism_relation,
        "relation_status":"Operator-declared relation; semantic equivalence or relevance is not certified",
        "allocation_reason":allocation_reason, "arms":chosen, "repetitions":repetitions,
        "return_path":return_path,
        "source_text":inputs["source"]["text"], "construction_text":inputs["construction"]["text"],
        "criticism_text":raw, "use_data_text":inputs["use_data"]["text"],
        "use_questions_text":inputs["use_questions"]["text"],
        "stage_instructions":instructions, "system_message":system_message,
        "literal_exclusions":exclusions, "leakage_audit":audit,
        "settings":provider_settings.to_dict(), "max_concurrent_calls":5,
        "source":reason_use_source_identity(), "content_appraisal":"unresolved",
        "standing_effect":"none", "proposed_changes_installed":False,
        "design_limits":["Bare/native respond once; matched/Mini respond then use under identical conditional prompts.",
            "Use receives minimal use material and the produced account only when return_path is true; the identical account field is empty when false. Original J, source packet and supplemental critic are not separate use inputs.",
            "Both return-path settings retain the response call and archive. This holds stage counts and response instructions fixed; it does not equalize prompt or completion tokens.",
            "The produced account may quote or carry prior material; preserving it is not censorship or proof of reason use.",
            "Shared source can already contain reasons; omission removes the supplemental occurrence only.",
            "Native reasoning and actual tokens are not equalized; finite controls establish no universal creativity finding."]}
    plan["material_snapshots"] = _snapshots(plan)
    plan["prompt_policy_sha256"] = digest({"system":system_message,"instructions":instructions,
        "renderer_source":plan["source"]["probe_modules"]["reason_use_study.py"]})
    return _signed(plan, "plan_id")


def stage_prompt(material: dict[str, Any], stage: str, history: list[dict[str, Any]]) -> str:
    if stage == "respond":
        if history:
            raise ValueError("REASON_USE_RESPOND_HISTORY_FORBIDDEN")
        parts = [material["stage_instructions"][stage], "Frozen common source:\n" + material["source_text"],
            "Fixed construction:\n" + material["construction_text"],
            "Supplemental criticism:\n" + material["criticism_text"]]
    elif stage == "use":
        if material.get("return_path", True):
            if len(history) != 1 or history[0].get("stage") != "respond" or type(history[0].get("text")) is not str:
                raise ValueError("REASON_USE_EXACT_RESPONSE_HISTORY_REQUIRED")
            account = history[0]["text"]
        else:
            if history:
                raise ValueError("REASON_USE_NO_RETURN_HISTORY_FORBIDDEN")
            account = ""
        parts = [material["stage_instructions"][stage], "Use-domain data:\n" + material["use_data_text"],
            "Use questions:\n" + material["use_questions_text"],
            "Returned account:\n" + account]
    else:
        raise ValueError("UNKNOWN_REASON_USE_STAGE")
    return "\n\n".join(parts)


def validate_response(answer: Any, max_tokens: int) -> str:
    if type(answer) is not dict or type(answer.get("content")) is not str or not answer["content"].strip():
        raise ValueError("REASON_USE_OUTPUT_UNAVAILABLE")
    usage = answer.get("usage")
    if type(usage) is not dict or any(type(usage.get(k)) is not int or usage[k] < 0 for k in ("prompt_tokens", "completion_tokens")):
        raise ValueError("REASON_USE_USAGE_UNAVAILABLE")
    if usage["completion_tokens"] > max_tokens:
        raise ValueError("REASON_USE_COMPLETION_CEILING_VIOLATED")
    if answer.get("finish_reason", "stop") != "stop":
        raise ValueError("REASON_USE_INCOMPLETE_GENERATION")
    if answer.get("status", "COMPLETE") != "COMPLETE":
        raise ValueError("REASON_USE_PROVIDER_REPORTED_FAILURE")
    return answer["content"]


def _output_occurrence(plan: dict[str, Any], arm: str, repeat: int, row: dict[str, Any],
                       previous: list[dict[str, Any]]) -> dict[str, Any]:
    stage = row["stage"]
    if stage == "respond":
        supplied = [plan["inputs"][key]["occurrence_id"] for key in ("source", "construction", "criticism")]
    elif stage == "use":
        supplied = [plan["inputs"][key]["occurrence_id"] for key in ("use_data", "use_questions")]
        if plan["return_path"]:
            supplied += [item["occurrence_id"] for item in previous if item["stage"] == "respond"]
    else:
        raise ValueError("UNKNOWN_OUTPUT_STAGE")
    origin = {"test_id":plan["test_id"],"plan_id":plan["plan_id"],"arm":arm,"repeat":repeat,
        "stage":stage,"mini_artifact_id":row.get("artifact_id"),"supplied_input_occurrence_ids":supplied,
        "input_provenance_meaning":"Exposure only; no semantic dependence, about or answers edge inferred",
        "prompt_sha256":text_hash(stage_prompt(plan,stage,previous if stage == "use" and plan["return_path"] else [])),
        "system_sha256":text_hash(plan["system_message"])}
    occurrence = freeze_occurrence(row["text"],origin)
    return _signed({**row,**{k:v for k,v in occurrence.items() if k != "occurrence_id"}},"occurrence_id")


def _resources(provider: Any) -> dict[str, int | None]:
    return {k:0 if provider is None else getattr(provider,k,None) for k in ("calls","prompt_tokens","completion_tokens")}


def _direct(provider: Any, plan: dict[str, Any], arm: str, repeat: int, root: Path,
            history: list[dict[str, Any]]) -> None:
    for stage in STAGES[:1] if arm in {"bare","native"} else STAGES:
        prompt = stage_prompt(plan,stage,history if stage != "use" or plan["return_path"] else [])
        write_new(root/(stage+".input.json"),{"stage":stage,"prompt":prompt,"prompt_sha256":text_hash(prompt),
            "system":plan["system_message"],"system_sha256":text_hash(plan["system_message"])})
        answer = provider.complete([{"role":"system","content":plan["system_message"]},
            {"role":"user","content":prompt}],json_output=False,
            coordinate={"stage":stage,"cycle":1,"phase":"raw-prose"})
        raw = validate_response(answer,plan["settings"]["max_tokens"])
        row = _output_occurrence(plan,arm,repeat,{"stage":stage,"text":raw,"text_sha256":text_hash(raw)},history)
        write_new(root/(stage+".artifact.json"),row)
        history.append(row)


def _arm(plan: dict[str,Any],arm: str,repeat: int,root: Path,provider_factory: Callable[...,Any],prepared: Any) -> dict[str,Any]:
    root.mkdir(parents=True,exist_ok=False)
    settings = _settings(plan["settings"],arm)
    result = {"schema":"minireason.reason-use-arm.v1","arm":arm,"repeat":repeat,"plan_id":plan["plan_id"],
        "started_at":_now(),"settings":settings.to_dict(),"return_path":plan["return_path"],"status":"RUNNING","history":[],"alarms":[],
        "content_appraisal":"unresolved","standing_effect":"none","proposed_changes_installed":False}
    write_new(root/"started.json",result)
    provider = None
    expected = 1 if arm in {"bare","native"} else 2
    try:
        provider = provider_factory(settings,root/"calls")
        if provider.settings != settings:
            raise ValueError("REASON_USE_PROVIDER_SETTINGS_MISMATCH")
        if arm.startswith("mini"):
            from .reason_use_mini import run_reason_use
            routed = run_reason_use(provider,root,prepared=prepared,**_material(plan))
            result["route_schema"] = routed.get("schema")
            result["mini_route"] = {k:v for k,v in routed.items() if k != "history"}
            result["alarms"].extend(routed.get("alarms",[]))
            for row in routed["history"]:
                occurrence = _output_occurrence(plan,arm,repeat,row,result["history"])
                result["history"].append(occurrence)
                write_new(root/(row["stage"]+".artifact.json"),occurrence)
            if routed.get("status") != "COMPLETE":
                raise ValueError("REASON_USE_MINI_ROUTE_FAILURE")
        else:
            _direct(provider,plan,arm,repeat,root,result["history"])
        if [row["stage"] for row in result["history"]] != list(STAGES[:expected]):
            raise ValueError("REASON_USE_ROUTE_INCOMPLETE")
        result["status"] = "OBSERVATIONS_RECORDED" if not result["alarms"] else "OPERATIONAL_FAILURE"
    except Exception as error:
        result["status"] = "OPERATIONAL_FAILURE"
        result["alarms"].append({"code":getattr(error,"code",type(error).__name__),"detail":str(error)})
    resources = _resources(provider)
    if any(type(v) is not int or v < 0 for v in resources.values()):
        result["alarms"].append({"code":"REASON_USE_RESOURCE_ACCOUNTING_UNAVAILABLE","detail":"Missing counters are not zero cost"})
        result["status"] = "OPERATIONAL_FAILURE"
    elif result["status"] == "OBSERVATIONS_RECORDED" and resources["calls"] != expected:
        result["alarms"].append({"code":"REASON_USE_CALL_ACCOUNTING_MISMATCH","detail":"Calls differ from declared stages"})
        result["status"] = "OPERATIONAL_FAILURE"
    result.update(resources=resources,ended_at=_now(),resource_accounting="Failed attempts count as calls; failed-delivery token cost may be unavailable. No retries.")
    write_new(root/"result.json",result)
    write_new(root/"errata.json",{"operational":result["alarms"],"semantic_findings":"Unadjudicated raw prose occurrences"})
    return result


def _preflight(plan: dict[str,Any],root: Path) -> tuple[Any,dict[str,Any]]:
    _verify(plan,"plan_id")
    rebuilt = make_plan(plan["test_id"],plan["inputs"],plan["criticism_relation"],plan["allocation_reason"],
        arms=plan["arms"],max_tokens=plan["settings"]["max_tokens"],repetitions=plan["repetitions"],
        parent_test=plan["parent_test"],stage_instructions=plan["stage_instructions"],
        system_message=plan["system_message"],literal_exclusions=plan["literal_exclusions"],
        settings=_settings(plan["settings"],"bare"),return_path=plan["return_path"])
    for key in set(rebuilt) - {"created_at","plan_id","source"}:
        if plan.get(key) != rebuilt[key]:
            raise ValueError("REASON_USE_PLAN_COMPONENT_MISMATCH: "+key)
    frozen_source, current_source = plan["source"], rebuilt["source"]
    if (frozen_source["probe_modules"] != current_source["probe_modules"]
            or frozen_source["probe_sha256"] != current_source["probe_sha256"]
            or frozen_source["repository"]["files"] != current_source["repository"]["files"]
            or frozen_source["repository"]["source_sha256"] != current_source["repository"]["source_sha256"]):
        raise ValueError("REASON_USE_SOURCE_CHANGED")
    for arm in plan["arms"]:
        _settings(plan["settings"],arm)
    stage_prompt(plan,"respond",[])
    stage_prompt(plan,"use",[{"stage":"respond","text":"PREFLIGHT_ACCOUNT_PLACEHOLDER"}] if plan["return_path"] else [])
    prepared = None
    record = {"status":"CONFIGURATION_PREFLIGHT_PASSED","model_calls":0,"leakage_audit":plan["leakage_audit"],
        "material_snapshots":plan["material_snapshots"],"content_appraisal":"unresolved",
        "runtime_source":current_source,"publication_commit_change_permitted_if_source_bytes_unchanged":True}
    if any(arm.startswith("mini") for arm in plan["arms"]):
        from .reason_use_mini import prepare_reason_use
        prepared = prepare_reason_use(root/"preflight",**_material(plan))
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
    # A malformed plan still receives a terminal root record; never dispatch its arbitrary arm names.
    if preflight["status"] == "CONFIGURATION_PREFLIGHT_PASSED":
        with ThreadPoolExecutor(max_workers=jobs) as pool:
            futures = [pool.submit(_arm,plan,arm,repeat,root/f"{arm}-r{repeat:02d}",provider_factory,prepared)
                for repeat in range(1,plan["repetitions"]+1) for arm in plan["arms"]]
            for future in as_completed(futures):
                rows.append(future.result())
    else:
        arms = [arm for arm in plan.get("arms",[]) if arm in ARMS] if isinstance(plan.get("arms"),list) else []
        declared_repeats = plan.get("repetitions",1)
        repeats = declared_repeats if type(declared_repeats) is int and 1 <= declared_repeats <= 20 else 1
        for arm,repeat in ((arm,repeat) for repeat in range(1,repeats+1) for arm in dict.fromkeys(arms)):
            row = {"schema":"minireason.reason-use-arm.v1","arm":arm,"repeat":repeat,"status":"OPERATIONAL_FAILURE",
                "history":[],"alarms":[preflight["alarm"]],"resources":_resources(None),
                "content_appraisal":"unresolved","standing_effect":"none","proposed_changes_installed":False}
            write_new(root/f"{arm}-r{repeat:02d}/result.json",row)
            rows.append(row)
    summary = {"schema":"minireason.reason-use-test.v1","test_id":plan.get("test_id"),"plan_id":plan.get("plan_id"),
        "preflight":preflight,"return_path":plan.get("return_path"),"arms":[{key:row[key] for key in ("arm","repeat","status","resources")}
            for row in sorted(rows,key=lambda row:(row["repeat"],row["arm"]))],
        "content_appraisal":"unresolved","standing_effect":"none","proposed_changes_installed":False,"completed_at":_now()}
    write_new(root/"summary.json",summary)
    write_new(root/"errata.json",{"operational":[{"arm":row["arm"],"repeat":row["repeat"],**alarm}
        for row in rows for alarm in row["alarms"]] or ([preflight["alarm"]] if "alarm" in preflight else []),
        "semantic_findings":"No automatic reason-use, repair or creativity finding"})
    lines = ["# "+str(plan.get("test_id")),"","Frozen construction response and isolated account-use observations.","",
        "Preflight: "+preflight["status"]+".","","| Arm | Repeat | Recording outcome | Calls | Completion tokens |",
        "|---|---:|---|---:|---:|"]
    for row in summary["arms"]:
        lines.append(f"| {row['arm']} | {row['repeat']} | {row['status']} | {row['resources']['calls']} | {row['resources']['completion_tokens']} |")
    lines += ["","Declared return path: "+str(plan.get("return_path"))+". The use request carries its declared minimal data and questions; the account field contains the exact response when true and is empty when false. "
        "Original inputs remain archived but are not additional use-stage ports. Output copying is permitted and visible. "
        "Bare/native have no use observation. Proposals are neither semantically adjudicated nor installed.",""]
    with (root/"REPORT.md").open("x",encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command",required=True)
    freeze = commands.add_parser("freeze-occurrence")
    freeze.add_argument("--text",type=Path,required=True)
    freeze.add_argument("--origin",type=Path,required=True)
    freeze.add_argument("--allow-empty",action="store_true")
    freeze.add_argument("--output",type=Path,required=True)
    plan = commands.add_parser("plan")
    plan.add_argument("--id",required=True)
    plan.add_argument("--inputs",type=Path,required=True,help="JSON object with the six signed input occurrences")
    plan.add_argument("--relation",choices=RELATIONS,required=True)
    plan.add_argument("--allocation-reason",required=True)
    plan.add_argument("--max-tokens",type=int,default=32768)
    plan.add_argument("--arms",nargs="+",choices=ARMS)
    plan.add_argument("--repetitions",type=int,default=1)
    plan.add_argument("--parent-test")
    plan.add_argument("--no-return-path",action="store_true",help="Keep both calls, but omit the response from the use request under an identical empty account field")
    plan.add_argument("--literal-exclusions",type=Path)
    plan.add_argument("--output",type=Path,required=True)
    run = commands.add_parser("run")
    run.add_argument("--plan",type=Path,required=True)
    run.add_argument("--output",type=Path,required=True)
    run.add_argument("--jobs",type=int,default=5)
    args = parser.parse_args()
    if args.command == "freeze-occurrence":
        write_new(args.output,freeze_occurrence(args.text.read_bytes().decode("utf-8"),load_frozen(args.origin),allow_empty=args.allow_empty))
    elif args.command == "plan":
        exclusions = None if args.literal_exclusions is None else loads_strict(args.literal_exclusions.read_bytes().decode("utf-8"))
        write_new(args.output,make_plan(args.id,load_frozen(args.inputs),args.relation,args.allocation_reason,
            arms=args.arms,max_tokens=args.max_tokens,repetitions=args.repetitions,parent_test=args.parent_test,literal_exclusions=exclusions,return_path=not args.no_return_path))
    else:
        summary = run_test(args.plan,args.output,jobs=args.jobs)
        if summary["preflight"]["status"] != "CONFIGURATION_PREFLIGHT_PASSED" or any(row["status"] != "OBSERVATIONS_RECORDED" for row in summary["arms"]):
            raise SystemExit("Operational failure recorded; review and publish the evidence before successor work.")
        print("Observations recorded without semantic adjudication. Review and publish the record.")
        return
    print("Frozen input written. No model call was made.")


if __name__ == "__main__":
    main()
