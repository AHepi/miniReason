"""Original comparison driver. A campaign is a declared experiment, not a search loop."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import traceback
from typing import Any

from creib.forge.mini.executor import contract_for
from creib.forge.mini.log import BlobStore, replay
from creib.forge.mini.manifest import compile_manifest
from creib.forge.mini.runner import run_mini
from creib.strict_json import loads_strict

from .provider import DeepSeek, MiniResponder, ProviderFailure, Settings, digest, write_new
from .tasks import evaluate, private_cases, task_prompt
from .templates import FINAL, PROPOSAL, TEMPLATES, manifest_for, register_task_seats

ARMS = {"bare", "native", "matched", "matched_native", "mini", "mini_native"}


def _load_answer(content: str) -> dict[str, str]:
    value = loads_strict(content)
    if type(value) is not dict or any(type(value.get(k)) is not str for k in ("body", "commitments")):
        raise ValueError("ANSWER_CONTRACT_INVALID: body and commitments must be strings")
    return value


def source_identity() -> dict[str, Any]:
    root = Path(__file__).resolve().parents[2]
    paths = sorted(p for p in (root / "src").rglob("*")
                   if p.is_file() and p.suffix in {".py", ".json"} and "__pycache__" not in p.parts)
    if (root / "pyproject.toml").is_file():
        paths.append(root / "pyproject.toml")
    files = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True,
                                         stderr=subprocess.DEVNULL).strip()
    except subprocess.CalledProcessError:
        commit = None
    return {"git_commit": commit, "files": files, "source_sha256": digest(files)}


def make_plan(test_id: str, template_id: str, rationale: str, *, repetitions: int = 1,
              cycles: int = 1, max_tokens: int = 8192, arms: list[str] | None = None,
              parent: str | None = None, feedback: bool = True,
              return_path: bool = True) -> dict[str, Any]:
    chosen = arms or ["bare", "native", "matched", "matched_native", "mini", "mini_native"]
    if not set(chosen) <= ARMS or len(set(chosen)) != len(chosen):
        raise ValueError("Invalid or duplicate arms")
    if type(repetitions) is not int or not 1 <= repetitions <= 20:
        raise ValueError("Repetitions must be between 1 and 20")
    manifest = manifest_for(template_id=template_id, cycles=cycles, feedback=feedback,
                            return_path=return_path, completion_tokens_per_call=max_tokens)
    return {"schema": "minireason.plan.v1", "test_id": test_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "template_id": template_id, "rationale": rationale, "parent": parent,
            "arms": chosen, "repetitions": repetitions, "cycles": cycles,
            "max_tokens_per_call": max_tokens, "max_concurrent_calls": 5,
            "task_id": "reservation_replay_v1", "feedback": feedback, "return_path": return_path,
            "manifest": manifest, "manifest_sha256": digest(manifest),
            "task_prompt_sha256": hashlib.sha256(task_prompt().encode()).hexdigest(),
            "holdout_sha256": digest(private_cases()), "source": source_identity(),
            "output_rule": "last completed revise artifact for Mini; last answer for direct arms",
            "interpretation": "Task behavior under explicit conditions; no automatic ECS or creativity verdict",
            "design_limit": "Bare/native are one-call practical baselines. Matched controls have equal stage counts and public feedback but different prompt serialization. Actual tokens are not matched."}


def _system() -> str:
    system, schema = contract_for("both")
    return system + "\nReturn one JSON object conforming to: " + json.dumps(schema, sort_keys=True)


def _direct(provider: DeepSeek, arm: str, plan: dict[str, Any], root: Path,
            history: list[dict[str, Any]] | None = None) -> tuple[dict[str, str], list[dict[str, Any]]]:
    template = TEMPLATES[plan["template_id"]]
    if history is None:
        history = []
    if arm in {"bare", "native"}:
        result = provider.complete([{"role": "system", "content": _system()},
                                    {"role": "user", "content": task_prompt()}])
        final = _load_answer(result["content"])
        history.append({"stage": "direct", "answer": final, "public": evaluate(final["commitments"])})
        return final, history
    previous = None
    for cycle in range(1, plan["cycles"] + 1):
        prompt = task_prompt() + "\n" + template["proposal"]
        if previous is not None and plan["return_path"]:
            prompt += "\nPrevious completed revision:\n" + json.dumps(previous)
        raw = provider.complete([{"role": "system", "content": _system()},
                                 {"role": "user", "content": prompt}], coordinate={"stage": "conjecture", "cycle": cycle})
        candidate = _load_answer(raw["content"])
        observed = evaluate(candidate["commitments"])
        history.append({"stage": "conjecture", "cycle": cycle, "answer": candidate, "public": observed})
        context = task_prompt() + "\nCandidate and operative program:\n" + json.dumps(candidate)
        feedback = "\nRecorded executable observations:\n" + json.dumps(observed)
        raw = provider.complete([{"role": "system", "content": _system()},
            {"role": "user", "content": context + (feedback if plan["feedback"] else "") + "\n" + template["critic"]}],
            coordinate={"stage": "criticise", "cycle": cycle})
        criticism = _load_answer(raw["content"])
        history.append({"stage": "criticise", "cycle": cycle, "answer": criticism})
        if plan["return_path"]:
            context += "\nCriticism and its grounds:\n" + json.dumps(criticism)
            if plan["feedback"]:
                context += feedback
        raw = provider.complete([{"role": "system", "content": _system()},
            {"role": "user", "content": context + "\n" + template["revision"]}], coordinate={"stage": "revise", "cycle": cycle})
        previous = _load_answer(raw["content"])
        history.append({"stage": "revise", "cycle": cycle, "answer": previous,
                        "public": evaluate(previous["commitments"])})
    return previous, history


def run_arm(plan: dict[str, Any], arm: str, repeat: int, root: Path) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=False)
    settings = Settings(thinking=arm in {"native", "matched_native", "mini_native"},
                        max_tokens=plan["max_tokens_per_call"])
    record: dict[str, Any] = {"schema": "minireason.arm.v1", "arm": arm, "repeat": repeat,
        "plan_sha256": digest(plan), "started_at": datetime.now(timezone.utc).isoformat(),
        "settings": settings.to_dict(), "status": "RUNNING", "alarms": [], "history": []}
    write_new(root / "started.json", record)
    provider = None
    try:
        provider = DeepSeek(settings, root / "calls")
        if arm.startswith("mini"):
            path = root / "manifest.json"
            write_new(path, plan["manifest"])
            compiled = compile_manifest(path)
            outcome = run_mini(compiled, root / "mini", MiniResponder(provider),
                               responder_id="deepseek:deepseek-flash", endpoint=settings)
            state = replay(root / "mini" / "log.jsonl", compiled.genesis)
            blobs = BlobStore(root / "mini" / "blobs")
            final = None
            for key in state.artifact_order:
                artifact = state.artifacts[key]
                kind = artifact["kind_id"]
                if kind not in {PROPOSAL, FINAL}:
                    continue
                answer = {name: blobs.get(artifact[name + "_ref"]).decode()
                          for name in ("body", "commitments")}
                record["history"].append({"stage": "conjecture" if kind == PROPOSAL else "revise",
                    "artifact_id": key, "answer": answer, "public": evaluate(answer["commitments"])})
                if kind == FINAL:
                    final = answer
            record["mini_outcome"] = {**asdict(outcome), "root": "mini"}
            if final is None or outcome.cycles_completed != plan["cycles"]:
                raise ValueError("MINI_INCOMPLETE_ROUTE: no complete final revision for each declared cycle")
            events = [json.loads(line) for line in (root / "mini" / "log.jsonl").read_text().splitlines()]
            for event in events:
                if event["type"] in {"FORMAT_FAILURE", "REFUSED", "SUBMISSION_DROPPED", "BUDGET_REFUSED"}:
                    record["alarms"].append({"code": event["type"], "event_id": event["event_id"], "payload": event["payload"]})
        else:
            final, history = _direct(provider, arm, plan, root, record["history"])
            record["history"] = history
        record["final"] = final
        record["public"] = evaluate(final["commitments"])
        record["holdout"] = evaluate(final["commitments"], holdout=True)
        record["status"] = "TASK_SURVIVED" if record["public"]["all_pass"] and record["holdout"]["all_pass"] else "TASK_FAILURE"
        if not record["public"]["runnable"] or not record["holdout"]["runnable"]:
            record["status"] = "CANDIDATE_EXECUTION_FAILURE"
        if record["alarms"]:
            record["status"] = "OPERATIONAL_ALARM"
    except Exception as error:
        record["status"] = "OPERATIONAL_FAILURE"
        record["alarms"].append({"code": getattr(error, "code", type(error).__name__), "detail": str(error)})
        record["exception_class"] = type(error).__name__
    record["resources"] = {"calls": provider.calls if provider else 0,
                            "prompt_tokens": provider.prompt_tokens if provider else 0,
                            "completion_tokens": provider.completion_tokens if provider else 0}
    record["ended_at"] = datetime.now(timezone.utc).isoformat()
    write_new(root / "result.json", record)
    failures = []
    for index, history in enumerate(record["history"]):
        evaluation = history.get("public")
        if evaluation and not evaluation["all_pass"]:
            failures.append({"stage_index": index, "stage": history["stage"], "evaluation": evaluation,
                             "loci": ["candidate program", "DSL translation", "checker", "task interpretation"]})
    for label in ("public", "holdout"):
        evaluation = record.get(label)
        if evaluation and not evaluation["all_pass"]:
            failures.append({"final_partition": label, "evaluation": evaluation,
                             "loci": ["candidate program", "DSL translation", "checker", "task interpretation"]})
    write_new(root / "errata.json", {"arm": arm, "repeat": repeat, "operational": record["alarms"], "candidate_failures": failures})
    return record


def run_test(plan_path: Path, root: Path, *, jobs: int = 5) -> dict[str, Any]:
    if not 1 <= jobs <= 5:
        raise ValueError("Concurrency must be between one and five")
    plan = json.loads(plan_path.read_text())
    current = source_identity()
    if current["source_sha256"] != plan["source"]["source_sha256"]:
        raise ValueError("SOURCE_CHANGED_SINCE_PLAN: write a new plan before calling")
    if digest(plan["manifest"]) != plan["manifest_sha256"]:
        raise ValueError("MANIFEST_CHANGED_SINCE_PLAN")
    if digest(private_cases()) != plan["holdout_sha256"]:
        raise ValueError("HOLDOUT_CHANGED_SINCE_PLAN")
    root.mkdir(parents=True, exist_ok=False)
    write_new(root / "plan.json", plan)
    register_task_seats()
    # Compile in the actual process before any provider is constructed.
    manifest_path = root / "manifest.json"
    write_new(manifest_path, plan["manifest"])
    compile_manifest(manifest_path)
    results = []
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        pending = {pool.submit(run_arm, plan, arm, repeat, root / f"{arm}-r{repeat:02d}"): (arm, repeat)
                   for repeat in range(1, plan["repetitions"] + 1) for arm in plan["arms"]}
        for future in as_completed(pending):
            results.append(future.result())
    summary = {"schema": "minireason.test.v1", "test_id": plan["test_id"],
               "plan_sha256": digest(plan), "completed_at": datetime.now(timezone.utc).isoformat(),
               "interpretation_status": "PENDING_SUBSTANTIVE_REVIEW",
               "arms": [{k: row[k] for k in ("arm", "repeat", "status", "resources")} for row in results]}
    write_new(root / "holdout-cases.json", private_cases())
    write_new(root / "summary.json", summary)
    lines = [f"# {plan['test_id']}", "", plan["rationale"], "",
             "These are finite task observations. Explanation quality, reason use and creativity require separate review.", "",
             "| Arm | Repeat | Outcome | Calls | Prompt tokens | Completion tokens |",
             "|---|---:|---|---:|---:|---:|"]
    for row in sorted(results, key=lambda x: (x["repeat"], x["arm"])):
        usage = row["resources"]
        lines.append(f"| {row['arm']} | {row['repeat']} | {row['status']} | {usage['calls']} | {usage['prompt_tokens']} | {usage['completion_tokens']} |")
    lines += ["", "Inspect each arm's result.json, errata.json, calls, and Mini log where applicable. Complete requests and public answer text are retained. Native hidden reasoning text is omitted.", ""]
    (root / "REPORT.md").write_text("\n".join(lines))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan")
    plan.add_argument("--id", required=True)
    plan.add_argument("--template", choices=TEMPLATES, required=True)
    plan.add_argument("--rationale", required=True)
    plan.add_argument("--output", type=Path, required=True)
    plan.add_argument("--parent")
    plan.add_argument("--repetitions", type=int, default=1)
    plan.add_argument("--cycles", type=int, default=1)
    plan.add_argument("--max-tokens", type=int, default=8192)
    plan.add_argument("--arms", nargs="+", choices=sorted(ARMS))
    plan.add_argument("--no-feedback", action="store_true")
    plan.add_argument("--no-return", action="store_true")
    run = commands.add_parser("run")
    run.add_argument("--plan", type=Path, required=True)
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--jobs", type=int, default=5)
    args = parser.parse_args()
    if args.command == "plan":
        value = make_plan(args.id, args.template, args.rationale, repetitions=args.repetitions,
                          cycles=args.cycles, max_tokens=args.max_tokens, arms=args.arms,
                          parent=args.parent, feedback=not args.no_feedback, return_path=not args.no_return)
        write_new(args.output, value)
        print(f"Prepared {args.output}; commit and publish before calling")
    else:
        result = run_test(args.plan, args.output, jobs=args.jobs)
        print(f"Completed {result['test_id']}; records ready for immediate publication")


if __name__ == "__main__":
    main()
