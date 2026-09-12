"""E027: separately frozen continuation of two unattempted E026 requests.

Preparation and verification are offline. Original E026 files remain unchanged.
Public construction text is opaque; this adapter makes no semantic judgement.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from minireason import sql_construction_study as base
from minireason.provider import DeepSeek, ProviderFailure

TEST_ID = "E027-sql-construction-continuation"
ARMS = ("mini-disabled", "prompt-control-disabled")
CAP = 8192
PARENT_PLAN_ID = "f8c3ab9ecb3285ea3d1d167427e413be2a30a1583a05fd5a411210430390a197"
PARENT_RECORD_ID = "c8d9bae1b7aa0ebb785d1ef310ebbb6d3abfd204233643fb5def30b4f30d08f0"
PARENT_SUMMARY_SHA256 = "e33857e308249edc4ce957163a7b1c41d0173d73b8a92d989ecc458e05909668"
PARENT_PUBLICATION = {
    "remote_commit": "da9158fbbc05258ec128861e4124c34fefed2057",
    "local_commit": "d534d4f0b573a46eecbfd420b187badfd857c961",
    "tree": "4f0c1444eb7d06f90e6e15a3b0b154733ea69069",
    "verification_authority": "REC-20260912-H publication at 2026-09-12T21:05:35.492Z; offline checks verify local bytes, not remote availability.",
}


def parent_paths(repo: Path, parent_root: Path | None, parent_record: Path | None) -> tuple[Path, Path]:
    return (parent_root if parent_root is not None else repo / "experiments/plans/E026-sql-construction",
            parent_record if parent_record is not None else repo / "experiments/records/E026-sql-construction")


def parent_identity(repo: Path, parent_root: Path, parent_record: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    parent = base.verify(parent_root, repo)
    if parent["plan_id"] != PARENT_PLAN_ID or parent["max_tokens_per_call"] != CAP:
        raise ValueError("ORIGINAL_PARENT_PLAN_REQUIRED")
    summary_raw = (parent_record / "summary.json").read_bytes()
    summary = json.loads(summary_raw)
    observed = summary.get("arms", [])
    attempted = [row.get("arm") for row in observed]
    unattempted = summary.get("unattempted_arms", [])
    if (any(arm in attempted or arm not in unattempted or (parent_record / arm).exists() for arm in ARMS)
            or unattempted != list(base.ARMS[2:])):
        raise ValueError("CONTINUATION_ARM_NOT_UNATTEMPTED")
    if (summary.get("status") != "INTERRUPTED" or summary.get("plan_id") != PARENT_PLAN_ID
            or summary.get("selected_construction_arm") != base.SELECTED_ARM
            or attempted != ["direct-disabled", "direct-native"]
            or [row.get("status") for row in observed] != ["PUBLIC_RESPONSE_RECORDED", "OPERATIONAL_FAILURE"]):
        raise ValueError("ORIGINAL_INTERRUPTED_PARENT_REQUIRED")
    record_files = {str(path.relative_to(parent_record)): base.sha(path.read_bytes())
                    for path in sorted(parent_record.rglob("*")) if path.is_file()}
    if base.sha(summary_raw) != PARENT_SUMMARY_SHA256 or base.digest(record_files) != PARENT_RECORD_ID:
        raise ValueError("ORIGINAL_PARENT_RECORD_CHANGED")
    parent_plan_raw = (parent_root / "plan.json").read_bytes()
    if (parent_record / "plan.json").read_bytes() != parent_plan_raw:
        raise ValueError("PARENT_OBSERVATION_PLAN_CHANGED")
    for row in observed:
        if json.loads((parent_record / row["arm"] / "result.json").read_bytes()) != row:
            raise ValueError("PARENT_RESULT_SUMMARY_MISMATCH")
    identity = {"parent_plan_id": PARENT_PLAN_ID, "parent_plan_sha256": base.sha(parent_plan_raw),
                "parent_summary_sha256": PARENT_SUMMARY_SHA256, "parent_record_id": PARENT_RECORD_ID,
                "parent_record_files": record_files, "publication": PARENT_PUBLICATION,
                "verified_unattempted_arms": list(ARMS)}
    return parent, identity


def effective_contract() -> dict[str, Any]:
    return {"schema": "minireason.sql-construction-continuation-plan.v1", "test_id": TEST_ID,
            "status": "FROZEN_PREPARATION_ONLY", "arms": list(ARMS), "jobs": 1,
            "selected_construction_arm": base.SELECTED_ARM,
            "selected_occurrence": TEST_ID + "/mini-disabled",
            "selection_rule": "Original mini-disabled label retained; E026 occurrence remains missing. Use the complete new E027 occurrence or preserve its insufficiency; never substitute another arm.",
            "max_tokens_per_call": CAP, "max_provider_calls": 2, "max_aggregate_completion_tokens": 2 * CAP,
            "automatic_retries": 0, "thinking": "disabled", "endpoint": "https://api.deepseek.com/v1/chat/completions",
            "cycles_per_arm": 1, "model_stages_per_cycle": ["construct"],
            "terminal_kind_is_transport_only": True, "parent_outputs_in_prompts": False,
            "operator_input_files": [], "deferred_parent_arms": ["prompt-control-native", "mini-native"],
            "parent_failed_arm_not_retried": "direct-native", "automatic_successor_started": False,
            "semantic_appraisal": "Unresolved; engine status and finite checks confer no semantic standing.",
            "comparison_limit": "Two new disabled samples with identical original Mini/control requests; changed occurrence and order. Native comparison remains incomplete; no multistage orchestration or stochastic advantage claim."}


def prepare(root: Path, repo: Path, *, parent_root: Path | None = None,
            parent_record: Path | None = None) -> dict[str, Any]:
    parent_root, parent_record = parent_paths(repo, parent_root, parent_record)
    parent, identity = parent_identity(repo, parent_root, parent_record)
    root.mkdir(parents=True, exist_ok=False)
    for name in ("participant-source.json", "manifest.json"):
        base.write_bytes(root / name, (parent_root / name).read_bytes())
    base.write_bytes(root / "parent-summary.json", (parent_record / "summary.json").read_bytes())
    base.write_json(root / "parent-provenance.json", identity)
    for arm in ARMS:
        base.write_bytes(root / "requests" / (arm + ".json"), (parent_root / "requests" / (arm + ".json")).read_bytes())
    source = base.read_source(root / "participant-source.json")
    preflight = base.probe(root / "manifest.json", source, CAP, root / "offline-probe")
    plan = {**effective_contract(), "parent": identity, "adapter_sha256": base.sha(Path(__file__).read_bytes()),
            "source_sha256": parent["source_sha256"], "source_bytes": parent["source_bytes"],
            "manifest_sha256": parent["manifest_sha256"], "compiled_plan_id": parent["compiled_plan_id"],
            "compiled_header_sha256": parent["compiled_header_sha256"],
            "request_sha256": {arm: parent["request_sha256"][arm] for arm in ARMS},
            "request_file_sha256": {arm: base.sha((root / "requests" / (arm + ".json")).read_bytes()) for arm in ARMS}}
    plan["plan_id"] = base.digest(plan)
    base.write_json(root / "plan.json", plan)
    base.write_json(root / "preflight.json", {**preflight, "plan_id": plan["plan_id"],
        "parent_plan_id": PARENT_PLAN_ID, "parent_record_id": PARENT_RECORD_ID,
        "requests_byte_identical_to_parent": True, "both_requests_equal": True,
        "provider_calls": 0, "source_allowlist": ["participant-source.json"],
        "parent_outputs_in_prompts": False, "operator_material_read_by_adapter": False})
    verify(root, repo, parent_root=parent_root, parent_record=parent_record)
    return plan


def verify(root: Path, repo: Path, *, parent_root: Path | None = None,
           parent_record: Path | None = None) -> dict[str, Any]:
    plan = json.loads((root / "plan.json").read_bytes())
    if plan.get("plan_id") != base.digest({key: value for key, value in plan.items() if key != "plan_id"}):
        raise ValueError("PLAN_IDENTITY_MISMATCH")
    if (Path(__file__).resolve() != (repo / "src/minireason/sql_construction_continuation.py").resolve()
            or plan["adapter_sha256"] != base.sha(Path(__file__).read_bytes())):
        raise ValueError("CONTINUATION_ADAPTER_CHANGED")
    for key, value in effective_contract().items():
        if key not in plan or base.encoded(plan[key]) != base.encoded(value):
            raise ValueError("EFFECTIVE_CONTRACT_CHANGED")
    parent_root, parent_record = parent_paths(repo, parent_root, parent_record)
    parent, identity = parent_identity(repo, parent_root, parent_record)
    if plan["parent"] != identity or (root / "parent-provenance.json").read_bytes() != base.encoded(identity):
        raise ValueError("PARENT_PROVENANCE_CHANGED")
    if (root / "parent-summary.json").read_bytes() != (parent_record / "summary.json").read_bytes():
        raise ValueError("PARENT_SUMMARY_COPY_CHANGED")
    for name in ("participant-source.json", "manifest.json"):
        if (root / name).read_bytes() != (parent_root / name).read_bytes():
            raise ValueError("FROZEN_PARENT_INPUT_CHANGED")
    for key in ("source_sha256", "source_bytes", "manifest_sha256", "compiled_plan_id", "compiled_header_sha256"):
        if type(plan[key]) is not type(parent[key]) or plan[key] != parent[key]:
            raise ValueError("PARENT_INPUT_IDENTITY_CHANGED")
    source = base.read_source(root / "participant-source.json")
    compiled = base.compile_manifest(root / "manifest.json")
    if compiled.genesis != plan["compiled_plan_id"] or base.digest(compiled.header) != plan["compiled_header_sha256"]:
        raise ValueError("COMPILED_PLAN_CHANGED")
    request_files = []
    for arm in ARMS:
        raw = (root / "requests" / (arm + ".json")).read_bytes()
        original = (parent_root / "requests" / (arm + ".json")).read_bytes()
        settings = base.settings_for(arm, CAP)
        payload = base.payload_for(base.messages_for(source, arm), settings)
        expected = {"request_sha256": base.digest(payload), "request": payload, "settings": settings.to_dict()}
        if (raw != original or json.loads(raw) != expected
                or plan["request_sha256"].get(arm) != base.digest(payload)
                or plan["request_file_sha256"].get(arm) != base.sha(raw)):
            raise ValueError("FROZEN_REQUEST_CHANGED")
        request_files.append(raw)
    if request_files[0] != request_files[1]:
        raise ValueError("PROMPT_CONTROL_NOT_EXACT")
    return plan


class CheckedProvider:
    """Compose the unchanged provider with verification at its spending boundary."""
    def __init__(self, provider: Any, arm: str, root: Path, repo: Path, expected_plan_id: str,
                 parent_root: Path, parent_record: Path):
        self.provider, self.arm, self.root, self.repo = provider, arm, root, repo
        self.expected_plan_id = expected_plan_id
        self.parent_root, self.parent_record = parent_root, parent_record
        self.settings = provider.settings
        self.entered = False

    @property
    def calls(self) -> int:
        return self.provider.calls

    def complete(self, messages: list[dict[str, str]], *, json_output: bool = True,
                 coordinate: dict[str, Any] | None = None) -> dict[str, Any]:
        if self.entered:
            raise ValueError("DUPLICATE_CONTINUATION_CALL")
        self.entered = True
        plan = verify(self.root, self.repo, parent_root=self.parent_root, parent_record=self.parent_record)
        if plan["plan_id"] != self.expected_plan_id:
            raise ValueError("EXTERNALLY_PINNED_PLAN_ID_MISMATCH")
        frozen = json.loads((self.root / "requests" / (self.arm + ".json")).read_bytes())
        payload = base.payload_for(messages, self.settings)
        if (json_output is not False or payload != frozen["request"]
                or self.settings.to_dict() != frozen["settings"]
                or coordinate != {"arm": self.arm, "stage": "construct", "cycle": 1, "phase": "raw-prose"}):
            raise ValueError("PENDING_WIRE_REQUEST_CHANGED")
        response = self.provider.complete(messages, json_output=False, coordinate=coordinate)
        if (response["request_sha256"] != plan["request_sha256"][self.arm]
                or response.get("request") != frozen["request"]):
            raise ValueError("ACTUAL_WIRE_REQUEST_CHANGED")
        return response


def safe_error_code(error: BaseException) -> str:
    # Never copy arbitrary exception messages or an untrusted .code value.
    known = {"KEY_MISSING", "SECRET_IN_REQUEST", "CONTENT_TYPE", "CREDENTIAL_ECHO", "INCOMPLETE_GENERATION",
             "EMPTY_GENERATION", "USAGE_UNAVAILABLE", "COMPLETION_CEILING_VIOLATED", "THINKING_MODE_MISMATCH",
             "TRANSPORT_OR_RESPONSE_ERROR"}
    if isinstance(error, ProviderFailure):
        code = error.code
        if isinstance(code, str) and (code in known or (len(code) == 8 and code.startswith("HTTP_") and code[5:].isdigit())):
            return code
        return "PROVIDER_FAILURE"
    if isinstance(error, KeyboardInterrupt):
        return "INTERRUPTED_BY_OPERATOR"
    return "CONTINUATION_OPERATIONAL_FAILURE"


def run(root: Path, output: Path, repo: Path, expected_plan_id: str, *,
        parent_root: Path | None = None, parent_record: Path | None = None) -> dict[str, Any]:
    parent_root, parent_record = parent_paths(repo, parent_root, parent_record)
    plan = verify(root, repo, parent_root=parent_root, parent_record=parent_record)
    if plan["plan_id"] != expected_plan_id:
        raise ValueError("EXTERNALLY_PINNED_PLAN_ID_MISMATCH")
    source = base.read_source(root / "participant-source.json")
    output.mkdir(parents=True, exist_ok=False)
    base.write_json(output / "plan.json", plan)
    rows, calls_by_arm = [], {arm: 0 for arm in ARMS}
    for arm in ARMS:
        arm_root = output / arm
        provider = None
        try:
            current = verify(root, repo, parent_root=parent_root, parent_record=parent_record)
            if current["plan_id"] != expected_plan_id:
                raise ValueError("EXTERNALLY_PINNED_PLAN_ID_MISMATCH")
            settings = base.settings_for(arm, CAP)
            provider = DeepSeek(settings, arm_root / "calls")
            checked = CheckedProvider(provider, arm, root, repo, expected_plan_id, parent_root, parent_record)
            if arm == "mini-disabled":
                responder = base.LiveProse(checked, source, arm, arm_root)
                compiled = base.compile_manifest(root / "manifest.json")
                base.run_mini(compiled, arm_root / "mini", responder,
                              responder_id="deepseek-flash:sql-construction-continuation", endpoint=settings)
                response = responder.response
                custody = base.artifact_prose(arm_root / "mini", compiled)
                if (response is None or responder.calls != 1 or len(custody) != 1
                        or any(custody[0][field] != response["content"] for field in ("body", "commitments"))):
                    raise ValueError("MINI_PUBLIC_PROSE_CUSTODY_FAILED")
            else:
                response = checked.complete(base.messages_for(source, arm), json_output=False,
                    coordinate={"arm": arm, "stage": "construct", "cycle": 1, "phase": "raw-prose"})
                base.write_bytes(arm_root / "public-answer.txt", response["content"].encode("utf-8"))
            if provider.calls != 1:
                raise ValueError("ONE_CALL_PER_ARM_REQUIRED")
            calls_by_arm[arm] = provider.calls
            row = {"arm": arm, "occurrence": TEST_ID + "/" + arm, "status": "PUBLIC_RESPONSE_RECORDED",
                   "answer_sha256": base.sha(response["content"].encode("utf-8")), "usage": response["usage"],
                   "request_sha256": response["request_sha256"], "attempted_calls": provider.calls,
                   "content_appraisal": "Unresolved"}
        except (Exception, KeyboardInterrupt) as error:
            calls_by_arm[arm] = provider.calls if provider is not None else 0
            row = {"arm": arm, "occurrence": TEST_ID + "/" + arm, "status": "OPERATIONAL_FAILURE",
                   "error_code": safe_error_code(error), "attempted_calls": calls_by_arm[arm],
                   "usage_of_unreturned_calls": "Unknown", "content_appraisal": "Unresolved"}
            base.write_json(arm_root / "result.json", row)
            rows.append(row)
            break
        base.write_json(arm_root / "result.json", row)
        rows.append(row)
    summary = {"plan_id": plan["plan_id"], "parent_plan_id": PARENT_PLAN_ID, "parent_record_id": PARENT_RECORD_ID,
               "arms": rows, "status": "COMPLETE" if len(rows) == len(ARMS) and all(row["status"] == "PUBLIC_RESPONSE_RECORDED" for row in rows) else "INTERRUPTED",
               "selected_construction_arm": base.SELECTED_ARM, "selected_occurrence": plan["selected_occurrence"],
               "provider_calls": sum(calls_by_arm.values()), "automatic_successor_started": False,
               "semantic_appraisal": "Unresolved", "unattempted_arms": [arm for arm in ARMS if calls_by_arm[arm] == 0],
               "deferred_parent_arms": plan["deferred_parent_arms"]}
    base.write_json(output / "summary.json", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("prepare", "verify", "run"))
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--parent-root", type=Path)
    parser.add_argument("--parent-record", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expected-plan-id")
    args = parser.parse_args()
    kwargs = {"parent_root": args.parent_root, "parent_record": args.parent_record}
    if args.operation == "prepare":
        result = prepare(args.root, args.repo, **kwargs)
    elif args.operation == "verify":
        result = verify(args.root, args.repo, **kwargs)
    else:
        if args.output is None or args.expected_plan_id is None:
            parser.error("run requires --output and --expected-plan-id")
        result = run(args.root, args.output, args.repo, args.expected_plan_id, **kwargs)
    print(json.dumps({"plan_id": result.get("plan_id"), "status": result.get("status"),
                      "provider_calls": result.get("provider_calls", 0)}))
    if args.operation == "run" and result["status"] != "COMPLETE":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
