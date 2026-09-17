"""Strict, recoverable R002 reasoning episodes over frozen public contracts."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import time
import uuid
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from . import config, prompts
from .adapter import Adapter
from .r002_preflight import token_preflight, validate_capability, snapshot_tokenizers
from .storage import get, put, read, write, sha, guard, run_lock
from .types import ReasonFailure


R002_SCHEMA = "minireason.reason.r002.v1"
R002_STATE_SCHEMA = "minireason.reason.r002-state.v1"
CLAIM = "OFFLINE FIXTURE records are structural evidence only; no model result or correctness finding is implied."
ROLE_SCHEMAS = {
    "answer": "answer.schema.json",
    "initial_decompose": "initial-decompose.schema.json",
    "decomposed_step": "decomposed-step.schema.json",
    "decomposed_critic": "tested-objection.schema.json",
    "decomposed_return": "decomposed-return.schema.json",
    "decomposed_use": "decomposed-use.schema.json",
    "decomposed_synthesis": "answer.schema.json",
    "decomposed_closing": "decomposed-closing.schema.json",
    "prose_critic": "prose-objection.schema.json",
    "tested_critic": "tested-objection.schema.json",
    "prose_return": "prose-return.schema.json",
    "tested_return": "tested-return.schema.json",
    "propagation_use": "propagation-use.schema.json",
    "blind_coding_solve": "recoding-solve.schema.json",
    "native_match_note": "native-match-note.schema.json",
    "native_match_synthesis": "native-match-note.schema.json",
}
R3_A1_ROLE_SCHEMAS = {
    **ROLE_SCHEMAS,
    "initial_decompose": "initial-decompose-r3-a1.schema.json",
    "decomposed_step": "decomposed-step-r3-a1.schema.json",
    "decomposed_return": "decomposed-return-r3-a1.schema.json",
    "decomposed_synthesis": "decomposed-synthesis-r3-a1.schema.json",
    "decomposed_closing": "decomposed-closing-r3-a1.schema.json",
}
R3_A2_ROLE_SCHEMAS = {
    **R3_A1_ROLE_SCHEMAS,
    "prose_critic": "prose-objection-r3-a2.schema.json",
    "tested_critic": "tested-objection-r3-a2.schema.json",
    "decomposed_critic": "tested-objection-r3-a2.schema.json",
    "propagation_use": "propagation-use-r3-a2.schema.json",
    "initial_decompose": "initial-decompose-r3-a2.schema.json",
    "decomposed_step": "decomposed-step-r3-a2.schema.json",
    "decomposed_return": "decomposed-return-r3-a2.schema.json",
    "decomposed_synthesis": "decomposed-synthesis-r3-a2.schema.json",
    "decomposed_closing": "decomposed-closing-r3-a2.schema.json",
}


def _r3_commitment_contract(contract_version: str | None) -> bool:
    return contract_version in {prompts.R003_A1_CONTRACT, prompts.R003_A2_CONTRACT}


def _role_schema(role: str, contract_version: str | None = None) -> str | None:
    schemas = (R3_A2_ROLE_SCHEMAS if contract_version == prompts.R003_A2_CONTRACT else
               R3_A1_ROLE_SCHEMAS if contract_version == prompts.R003_A1_CONTRACT else
               ROLE_SCHEMAS)
    return schemas.get(role)


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _load_object(value, label: str, *, optional: bool = False):
    if value is None and optional:
        return None, None, None
    if isinstance(value, dict):
        text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        return deepcopy(value), text, None
    path = Path(value)
    text = read(path)
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise ReasonFailure("CONFIG_ERROR", f"{label} is not valid JSON") from exc
    return data, text, path


def _candidate(registry: dict, problem_id: str, label: str) -> dict:
    matches = [item for item in registry.get("candidates", [])
               if item.get("candidate_id") == problem_id]
    if len(matches) != 1:
        raise ReasonFailure("CONFIG_ERROR", f"{label} has no unique {problem_id} entry")
    return matches[0]


def _relation_entry(registry: dict, problem_id: str) -> dict:
    item = _candidate(registry, problem_id, "relation registry")
    relations = item.get("relations")
    if not isinstance(relations, list) or not relations:
        raise ReasonFailure("CONFIG_ERROR", "Problem has no declared public relations")
    ids = [r.get("relation_id") for r in relations]
    if any(not isinstance(x, str) or not x for x in ids) or len(set(ids)) != len(ids):
        raise ReasonFailure("CONFIG_ERROR", "Public relation IDs are invalid or duplicated")
    return item


def _infer_problem_id(problem_id, problem, registry):
    if isinstance(problem_id, str) and problem_id:
        return problem_id
    candidates = registry.get("candidates", [])
    if len(candidates) == 1:
        return candidates[0]["candidate_id"]
    raise ReasonFailure("CONFIG_ERROR", "problem_id is required for a multi-candidate registry")


class ContractSet:
    """Validate frozen schema bytes with their relative references."""

    def __init__(self, directory: str | Path):
        self.directory = Path(directory)
        self.schemas = {}
        resources = []
        for path in sorted(self.directory.glob("*.schema.json")):
            schema = get(path)
            self.schemas[path.name] = schema
            if "$id" in schema:
                resources.append((schema["$id"], Resource.from_contents(schema)))
        if not self.schemas:
            raise ReasonFailure("CONFIG_ERROR", "No R002 schemas found")
        self.registry = Registry().with_resources(resources)

    def validate(self, name: str, value: dict) -> dict:
        schema = self.schemas.get(name)
        if schema is None:
            raise ReasonFailure("CONFIG_ERROR", "Unknown R002 schema: " + name)
        errors = sorted(Draft202012Validator(schema, registry=self.registry).iter_errors(value),
                        key=lambda error: list(error.absolute_path))
        if errors:
            error = errors[0]
            location = ".".join(str(part) for part in error.absolute_path) or "$"
            raise ReasonFailure("SCHEMA_FAILURE", f"{name}:{location}: {error.message}")
        return value

    def closure(self, role: str, contract_version: str | None = None) -> list[tuple[str, dict]]:
        """Return the role schema and transitive local external-reference closure."""
        root = _role_schema(role, contract_version)
        if root is None:
            raise ReasonFailure("CONFIG_ERROR", "Unknown R002 schema role: " + role)
        ordered = []
        seen = set()

        def references(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    if key == "$ref" and isinstance(item, str) and not item.startswith("#"):
                        yield item.split("#", 1)[0].rsplit("/", 1)[-1]
                    else:
                        yield from references(item)
            elif isinstance(value, list):
                for item in value:
                    yield from references(item)

        def visit(name):
            if name in seen:
                return
            schema = self.schemas.get(name)
            if schema is None:
                raise ReasonFailure("CONFIG_ERROR", "Missing local schema dependency: " + name)
            seen.add(name)
            ordered.append((name, schema))
            for dependency in sorted(set(references(schema))):
                visit(dependency)

        visit(root)
        return ordered

    def prompt_blocks(self, role: str, contract_version: str | None = None) -> list[tuple[str, str]]:
        blocks = []
        for index, (name, schema) in enumerate(self.closure(role, contract_version)):
            label = "RESPONSE SCHEMA" if index == 0 else "RESPONSE SCHEMA DEPENDENCY"
            blocks.append((label + " " + name, _json(schema)))
        return blocks


def _response_object(content: str, *, contract_version: str | None = None) -> dict:
    if not isinstance(content, str):
        raise ReasonFailure("SCHEMA_FAILURE", "Public response must be text")
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                detail = "Duplicate JSON key: " + key
                if contract_version == prompts.R003_A2_CONTRACT:
                    detail += (". Keep exactly one occurrence of this key, using the intended value, "
                               "and remove every duplicate before returning the repaired object")
                raise ReasonFailure("SCHEMA_FAILURE", detail)
            result[key] = value
        return result
    def constant(value):
        raise ReasonFailure("SCHEMA_FAILURE", "Non-finite JSON number: " + value)
    try:
        value = json.loads(content, object_pairs_hook=pairs, parse_constant=constant)
        if not isinstance(value, dict):
            raise ReasonFailure("SCHEMA_FAILURE", "R002 response must be exactly one JSON object")
        return value
    except ReasonFailure:
        raise
    except (TypeError, ValueError) as exc:
        raise ReasonFailure("SCHEMA_FAILURE", str(exc)) from exc


def _validate_steps(steps: list[dict], label="derivation_steps"):
    indices = [step["step_index"] for step in steps]
    if indices != list(range(1, len(steps) + 1)):
        raise ReasonFailure("SCHEMA_FAILURE", f"{label} must be contiguous and start at 1")
    for step in steps:
        if any(parent >= step["step_index"] for parent in step["depends_on"]):
            raise ReasonFailure("SCHEMA_FAILURE", f"{label} dependencies must name earlier steps")


def _claim_map(claims: list[dict]) -> dict[str, Any]:
    result = {}
    for claim in claims:
        relation_id = claim["relation_id"]
        if relation_id in result:
            raise ReasonFailure("SCHEMA_FAILURE", "Duplicate relation ID: " + relation_id)
        try:
            _json(claim["value"])
        except (TypeError, ValueError) as exc:
            raise ReasonFailure("SCHEMA_FAILURE", "Claim value is not canonical JSON") from exc
        result[relation_id] = claim["value"]
    return result


def validate_answer(data: dict, relation: dict, *, study_profile=None) -> dict:
    _validate_steps(data["derivation_steps"])
    claims = _claim_map(data["claims"])
    expected = {item["relation_id"] for item in relation["relations"]}
    if data["decision"] == "answered" and set(claims) != expected:
        raise ReasonFailure("SCHEMA_FAILURE", "Answered relation IDs do not exactly cover the registry")
    for claim in data["claims"]:
        if claim["quote"] not in data["answer"]:
            raise ReasonFailure("SCHEMA_FAILURE", "Claim quote is absent from answer")
        if (study_profile == config.R003_PROFILE
                and claim["relation_id"] == "working_position"
                and not isinstance(claim["value"], str)):
            raise ReasonFailure("SCHEMA_FAILURE", "R003 working_position must be a prose string")
    return data


_QUOTE_FOLD = str.maketrans({
    "\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
    "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"',
})


def _normalized_locator_text(value: str) -> str:
    folded = value.translate(_QUOTE_FOLD).casefold()
    return re.sub(r"\s+", " ", folded).strip()


def _validate_r3_a2_locator(locator: dict, steps: dict[int, dict]) -> tuple[int, str]:
    index = locator["step_index"]
    step = steps.get(index)
    if step is None:
        raise ReasonFailure(
            "SCHEMA_FAILURE",
            f"R3-A2 fork locator check failed: step_index {index} does not name a real working-answer "
            "derivation step; candidate targeted step text: <missing>")
    target = step["statement"]
    quote = locator["step_quote"]
    if quote == "":
        return index, target
    normalized_quote = _normalized_locator_text(quote)
    normalized_target = _normalized_locator_text(target)
    if len(normalized_quote) < 40 or normalized_quote not in normalized_target:
        raise ReasonFailure(
            "SCHEMA_FAILURE",
            "R3-A2 fork locator check failed: nonempty step_quote must normalize to an exact "
            f"substring of at least 40 characters in step_index {index}; candidate targeted step "
            f"text: {target}")
    return index, target


def validate_objections(data: dict, answer: dict, fork: dict, *, tested: bool,
                        study_profile=None, prior_objections=(), contract_version=None) -> dict:
    steps = {step["step_index"]: step for step in answer.get("derivation_steps", [])}
    check_ids = []
    participant_labels = {}
    if study_profile == config.R003_PROFILE:
        for prior in prior_objections:
            locator = prior.get("fork", {})
            label = locator.get("branch_point_id")
            if isinstance(label, str):
                index = locator.get("step_index")
                step = steps.get(index)
                participant_labels[label] = ((index, step["statement"]) if
                                             contract_version == prompts.R003_A2_CONTRACT and step else
                                             (index, locator.get("step_quote")))
    for objection in data["objections"]:
        locator = objection["fork"]
        step = steps.get(locator["step_index"])
        if contract_version == prompts.R003_A2_CONTRACT:
            index, target = _validate_r3_a2_locator(locator, steps)
        elif step is None or locator["step_quote"] != step["statement"]:
            raise ReasonFailure("SCHEMA_FAILURE", "Fork locator does not quote the named derivation step exactly")
        if study_profile == config.R003_PROFILE:
            label = locator["branch_point_id"]
            bound = participant_labels.get(label)
            current = ((index, target) if contract_version == prompts.R003_A2_CONTRACT else
                       (locator["step_index"], locator["step_quote"]))
            if bound is not None and bound != current:
                raise ReasonFailure("SCHEMA_FAILURE", "Participant branch label has inconsistent locators")
            participant_labels[label] = current
        elif locator["branch_point_id"] != fork["branch_point_id"]:
            raise ReasonFailure("SCHEMA_FAILURE", "Fork locator names the wrong public branch")
        if tested:
            check_ids.append(objection["check"]["check_id"])
    if len(set(check_ids)) != len(check_ids):
        raise ReasonFailure("SCHEMA_FAILURE", "Duplicate check ID")
    return data


def validate_return(data: dict, before: dict, objections: list[dict], relation: dict,
                    *, tested: bool, study_profile=None) -> dict:
    validate_answer(data, relation, study_profile=study_profile)
    expected = [obj["id"] for obj in objections if obj.get("status") == "unresolved"]
    known = [obj["id"] for obj in objections]
    actual = [item["id"] for item in data["dispositions"]]
    if (len(set(actual)) != len(actual) or not set(expected) <= set(actual)
            or not set(actual) <= set(known)):
        raise ReasonFailure("SCHEMA_FAILURE", "Return must cover every open ID and may redispose only supplied resolved IDs")
    by_id = {obj["id"]: obj for obj in objections}
    final_steps = {step["step_index"]: step for step in data["derivation_steps"]}
    if data["decision"] == "cannot_decide":
        if data["claims"] != before.get("claims", []) or data["derivation_steps"] != before.get("derivation_steps", []):
            raise ReasonFailure("SCHEMA_FAILURE", "cannot_decide return must retain prior claims and derivation steps")
    for disposition in data["dispositions"]:
        objection = by_id[disposition["id"]]
        rederivation = disposition["rederivation"]
        fork_index = objection["fork"]["step_index"]
        if rederivation["objection_id"] != disposition["id"]:
            raise ReasonFailure("SCHEMA_FAILURE", "Rederivation names the wrong objection")
        if disposition["status"] == "taken-up":
            if rederivation["from_step_index"] != fork_index:
                raise ReasonFailure("SCHEMA_FAILURE", "Uptake must rederive from the challenged fork")
            steps = rederivation["steps"]
            if not steps or steps[0]["step_index"] != fork_index:
                raise ReasonFailure("SCHEMA_FAILURE", "Rederivation does not start at the challenged fork")
            indices = [step["step_index"] for step in steps]
            if indices != list(range(fork_index, max(final_steps) + 1)):
                raise ReasonFailure("SCHEMA_FAILURE", "Uptake must reconstruct the full derivation suffix")
            for step in steps:
                if final_steps.get(step["step_index"]) != step:
                    raise ReasonFailure("SCHEMA_FAILURE", "Rederivation is not the returned derivation suffix")
        if tested:
            redo = disposition["redo"]
            check = objection.get("check")
            if check is None or redo["check_id"] != check["check_id"]:
                raise ReasonFailure("SCHEMA_FAILURE", "Return redo does not bind the supplied check")
            if disposition["status"] in {"taken-up", "rejected-with-reason"} and redo["status"] != "redone":
                raise ReasonFailure("SCHEMA_FAILURE", "Substantive disposition requires a redone check")
            if redo["status"] == "cannot_redo" and disposition["status"] != "unresolved":
                raise ReasonFailure("SCHEMA_FAILURE", "cannot_redo permits only unresolved")
    return data


def validate_use(data: dict, before: dict, after: dict, relation: dict, fork: dict,
                 *, checker_eligible: bool, study_profile=None, prior_objections=(),
                 contract_version=None) -> dict:
    dependency = data["dependency"]
    known = {item["relation_id"] for item in relation["relations"]}
    if dependency["relation_id"] not in known:
        raise ReasonFailure("SCHEMA_FAILURE", "Use dependency relation is not in the registry")
    if dependency["before_quote"] not in before["answer"]:
        raise ReasonFailure("SCHEMA_FAILURE", "Before quote is absent from before answer")
    if dependency["after_quote"] not in after["answer"]:
        raise ReasonFailure("SCHEMA_FAILURE", "After quote is absent from after answer")
    before_claims, after_claims = _claim_map(before.get("claims", [])), _claim_map(after.get("claims", []))
    changed = {relation_id for relation_id in set(before_claims) & set(after_claims)
               if type(before_claims[relation_id]) is not type(after_claims[relation_id])
               or _json(before_claims[relation_id]) != _json(after_claims[relation_id])}
    if (study_profile != config.R003_PROFILE and changed
            and dependency["relation_id"] not in changed):
        raise ReasonFailure("SCHEMA_FAILURE", "Use must bind a changed relation when one exists")
    same_conclusion = (type(data["before"]["conclusion"]) is type(data["after"]["conclusion"])
                       and _json(data["before"]["conclusion"]) == _json(data["after"]["conclusion"]))
    if (study_profile != config.R003_PROFILE and dependency["result_depends_on_change"]
            and (same_conclusion or not changed)):
        raise ReasonFailure("SCHEMA_FAILURE", "Unchanged evaluations cannot claim dependence on change")
    if data["decision"] != "cannot_decide" and checker_eligible != (data["checker"] is not None):
        expected = "proposal" if checker_eligible else "null"
        raise ReasonFailure("SCHEMA_FAILURE", "Checker field must be " + expected)
    if data["checker"] is not None:
        if study_profile == config.R003_PROFILE:
            raise ReasonFailure("SCHEMA_FAILURE", "R003 disables checker proposals and execution")
        proposal = data["checker"]
        if proposal["query_id"] != data["query_id"] or proposal["question"] != data["question"]:
            raise ReasonFailure("SCHEMA_FAILURE", "Checker proposal changes the use query")
        if proposal["relation_id"] != dependency["relation_id"]:
            raise ReasonFailure("SCHEMA_FAILURE", "Checker proposal changes the use relation")
        if proposal["working_claim_quote"] != dependency["after_quote"]:
            raise ReasonFailure("SCHEMA_FAILURE", "Checker proposal does not quote the working claim")
        if dependency["relation_id"] not in after_claims or (
                type(proposal["working_value"]) is not type(after_claims[dependency["relation_id"]])
                or _json(proposal["working_value"]) != _json(after_claims[dependency["relation_id"]])):
            raise ReasonFailure("SCHEMA_FAILURE", "Checker working_value does not bind the returned claim")
    if data["objections"]:
        validate_objections({"objections": data["objections"]}, after, fork, tested=True,
                            study_profile=study_profile, prior_objections=prior_objections,
                            contract_version=contract_version)
    return data


def validate_recoding_solve(data: dict, relation: dict, coding_id: str) -> dict:
    _validate_steps(data["derivation_steps"])
    if data["coding_id"] != coding_id:
        raise ReasonFailure("SCHEMA_FAILURE", "Blind solve uses the wrong coding ID")
    claims = _claim_map(data["claims"])
    expected = {item["relation_id"] for item in relation["relations"]}
    if data["decision"] == "answered" and set(claims) != expected:
        raise ReasonFailure("SCHEMA_FAILURE", "Blind solve relation IDs do not exactly cover the registry")
    return data


def _r3_contract_label(contract_version: str | None) -> str:
    return "R3-A2" if contract_version == prompts.R003_A2_CONTRACT else "R3-A1"


def _validate_r3_commitment_step(data: dict, contract_version: str) -> dict:
    """Check commitment custody only; substantive refutability remains a reader judgment."""
    if data.get("cannot_decide") is not None or data.get("decision") == "cannot_decide":
        return data
    commitments = data.get("commitments", [])
    if not commitments:
        raise ReasonFailure(
            "SCHEMA_FAILURE",
            f"{_r3_contract_label(contract_version)} answered step requires a declared commitment")
    ending = "COMMITMENT: " + commitments[-1]["claim"]
    if not data.get("result", "").rstrip().endswith(ending):
        raise ReasonFailure(
            "SCHEMA_FAILURE",
            f"{_r3_contract_label(contract_version)} step result must end with the exact final "
            "commitment as 'COMMITMENT: <claim>'")
    return data


def validate_initial_decompose(data: dict, *, contract_version=None) -> dict:
    if data["cannot_decide"] is not None:
        return data
    plan = data["plan"]
    if [item["step"] for item in plan] != list(range(1, len(plan) + 1)):
        raise ReasonFailure("SCHEMA_FAILURE", "Decomposition plan steps must be contiguous and start at 1")
    for item in plan:
        if any(parent >= item["step"] for parent in item["depends_on"]):
            raise ReasonFailure("SCHEMA_FAILURE", "Decomposition dependencies must name earlier steps")
    if data["first_step"]["step"] != plan[0]["step"]:
        raise ReasonFailure("SCHEMA_FAILURE", "First decomposition result does not match plan step 1")
    if _r3_commitment_contract(contract_version):
        if data["decisive_step"] not in {item["step"] for item in plan}:
            raise ReasonFailure(
                "SCHEMA_FAILURE",
                f"{_r3_contract_label(contract_version)} decisive_step must name a planned step")
        _validate_r3_commitment_step(data["first_step"], contract_version)
    return data


def validate_decomposed_step(data: dict, expected_step: dict,
                             accepted_steps: list[dict], *, contract_version=None) -> dict:
    if data["step"] != expected_step["step"]:
        raise ReasonFailure("SCHEMA_FAILURE", "STEP response names the wrong plan step")
    accepted = {item["step"] for item in accepted_steps}
    missing = sorted(set(expected_step["depends_on"]) - accepted)
    if missing:
        raise ReasonFailure("SCHEMA_FAILURE", "STEP dependencies are not accepted: " + ",".join(map(str, missing)))
    if _r3_commitment_contract(contract_version):
        _validate_r3_commitment_step(data, contract_version)
    return data


def validate_decomposed_return(data: dict, before: dict,
                               objections: list[dict], *, contract_version=None) -> dict:
    if data["step"] != before["step"]:
        raise ReasonFailure("SCHEMA_FAILURE", "Decomposed return names the wrong step")
    expected = [item["id"] for item in objections]
    actual = [item["id"] for item in data["dispositions"]]
    if len(actual) != len(set(actual)) or set(actual) != set(expected):
        raise ReasonFailure("SCHEMA_FAILURE", "Decomposed return must dispose every current objection exactly once")
    by_id = {item["id"]: item for item in objections}
    for disposition in data["dispositions"]:
        redo = disposition["redo"]
        if redo["check_id"] != by_id[disposition["id"]]["check"]["check_id"]:
            raise ReasonFailure("SCHEMA_FAILURE", "Decomposed return redo names the wrong check")
        if disposition["status"] in {"taken-up", "rejected-with-reason"} and redo["status"] != "redone":
            raise ReasonFailure("SCHEMA_FAILURE", "Substantive decomposed disposition requires a redone check")
        if redo["status"] == "cannot_redo" and disposition["status"] != "unresolved":
            raise ReasonFailure("SCHEMA_FAILURE", "A check that cannot be redone must remain unresolved")
    if _r3_commitment_contract(contract_version):
        _validate_r3_commitment_step(data, contract_version)
    return data


def validate_decomposed_use(data: dict, expected_step: int) -> dict:
    if data["step"] != expected_step:
        raise ReasonFailure("SCHEMA_FAILURE", "Decomposed use names the wrong step")
    return data


def _decisive_commitments(accepted_steps: list[dict], decisive_step: int) -> list[str]:
    matched = [item for item in accepted_steps if item["step"] == decisive_step]
    if len(matched) != 1:
        return []
    return [item["claim"] for item in matched[0].get("commitments", [])]


def validate_decomposed_synthesis(data: dict, relation: dict, *, study_profile=None,
                                  contract_version=None, decisive_step=None,
                                  accepted_steps=()) -> dict:
    if not _r3_commitment_contract(contract_version):
        return validate_answer(data, relation, study_profile=study_profile)
    validate_answer({key: data[key] for key in
                    ("decision", "answer", "missing_derivation", "claims", "derivation_steps")},
                    relation, study_profile=study_profile)
    if data["decisive_step"] != decisive_step:
        raise ReasonFailure(
            "SCHEMA_FAILURE",
            f"{_r3_contract_label(contract_version)} synthesis names the wrong decisive step")
    commitments = _decisive_commitments(list(accepted_steps), decisive_step)
    if data["decisive_claim"] not in commitments:
        raise ReasonFailure(
            "SCHEMA_FAILURE",
            f"{_r3_contract_label(contract_version)} synthesis must copy an accepted decisive "
            "commitment exactly")
    if data["decision"] == "answered" and data["decisive_claim"] not in data["answer"]:
        raise ReasonFailure(
            "SCHEMA_FAILURE",
            f"{_r3_contract_label(contract_version)} answer does not contain its decisive claim")
    return data


def validate_decomposed_closing(data: dict, relation: dict,
                                objections: list[dict], *, contract_version=None,
                                decisive_step=None, accepted_steps=()) -> dict:
    validate_answer({key: data[key] for key in
                    ("decision", "answer", "missing_derivation", "claims", "derivation_steps")},
                    relation, study_profile=config.R003_PROFILE)
    expected = [item["id"] for item in objections if item.get("status") == "unresolved"]
    actual = [item["id"] for item in data["dispositions"]]
    if len(actual) != len(set(actual)) or set(actual) != set(expected):
        raise ReasonFailure("SCHEMA_FAILURE",
                            "Decomposed closing must dispose every remaining objection exactly once")
    if _r3_commitment_contract(contract_version):
        if data["decisive_step"] != decisive_step:
            raise ReasonFailure(
                "SCHEMA_FAILURE",
                f"{_r3_contract_label(contract_version)} closing names the wrong decisive step")
        commitments = _decisive_commitments(list(accepted_steps), decisive_step)
        if commitments:
            if data["decisive_claim"] not in commitments:
                raise ReasonFailure(
                    "SCHEMA_FAILURE",
                    f"{_r3_contract_label(contract_version)} closing must copy an accepted decisive "
                    "commitment exactly")
            if data["decision"] == "answered" and data["decisive_claim"] not in data["answer"]:
                raise ReasonFailure(
                    "SCHEMA_FAILURE",
                    f"{_r3_contract_label(contract_version)} closing answer omits its decisive claim")
        elif data["decision"] != "cannot_decide" or data["decisive_claim"]:
            raise ReasonFailure(
                "SCHEMA_FAILURE",
                f"{_r3_contract_label(contract_version)} closing cannot answer before the decisive "
                "step is accepted")
    return data


def parse_r002(role: str, content: str, contracts: ContractSet, *, relation: dict,
               answer=None, before=None, objections=(), fork=None,
               coding_id=None, checker_eligible=False, expected_step=None,
               accepted_steps=(), study_profile=None, prior_objections=(),
               contract_version=None, decisive_step=None) -> dict:
    schema_name = _role_schema(role, contract_version)
    if schema_name is None:
        raise ReasonFailure("CONFIG_ERROR", "Unknown R002 parse role: " + role)
    data = contracts.validate(schema_name, _response_object(content, contract_version=contract_version))
    if role == "answer":
        return validate_answer(data, relation, study_profile=study_profile)
    if role == "initial_decompose":
        return validate_initial_decompose(data, contract_version=contract_version)
    if role == "decomposed_step":
        return validate_decomposed_step(data, expected_step, list(accepted_steps),
                                        contract_version=contract_version)
    if role in {"prose_critic", "tested_critic", "decomposed_critic"}:
        return validate_objections(data, answer, fork, tested=role != "prose_critic",
                                   study_profile=study_profile,
                                   prior_objections=prior_objections or objections,
                                   contract_version=contract_version)
    if role in {"prose_return", "tested_return"}:
        return validate_return(data, before, list(objections), relation,
                               tested=role == "tested_return", study_profile=study_profile)
    if role == "propagation_use":
        return validate_use(data, before, answer, relation, fork,
                            checker_eligible=checker_eligible, study_profile=study_profile,
                            prior_objections=prior_objections,
                            contract_version=contract_version)
    if role == "decomposed_return":
        return validate_decomposed_return(data, before, list(objections),
                                          contract_version=contract_version)
    if role == "decomposed_use":
        return validate_decomposed_use(data, expected_step["step"])
    if role == "decomposed_synthesis":
        return validate_decomposed_synthesis(
            data, relation, study_profile=study_profile, contract_version=contract_version,
            decisive_step=decisive_step, accepted_steps=accepted_steps)
    if role == "decomposed_closing":
        return validate_decomposed_closing(
            data, relation, list(objections), contract_version=contract_version,
            decisive_step=decisive_step, accepted_steps=accepted_steps)
    if role == "blind_coding_solve":
        return validate_recoding_solve(data, relation, coding_id)
    return data


def claims_equal(a: dict, b: dict, relation_ids: list[str]) -> bool | None:
    try:
        left, right = _claim_map(a["claims"]), _claim_map(b["claims"])
    except (KeyError, ReasonFailure):
        return None
    if set(left) != set(relation_ids) or set(right) != set(relation_ids):
        return None
    for relation_id in relation_ids:
        x, y = left[relation_id], right[relation_id]
        if type(x) is not type(y) or _json(x) != _json(y):
            return False
    return True


def stall_switch_due(initial: dict, first: dict, second: dict,
                     open_objections: list[dict], relation_ids: list[str]) -> bool | None:
    if not open_objections:
        return False
    first_equal = claims_equal(initial, first, relation_ids)
    second_equal = claims_equal(first, second, relation_ids)
    if first_equal is None or second_equal is None:
        return None
    return first_equal and second_equal


def detect_tail_edit(before: dict, after: dict, disposition: dict) -> bool:
    if disposition.get("status") != "taken-up":
        return False
    old = before.get("derivation_steps", [])
    new = after.get("derivation_steps", [])
    if not old or len(old) != len(new):
        return False
    claims_changed = _json(before.get("claims", [])) != _json(after.get("claims", []))
    answer_changed = before.get("answer") != after.get("answer")
    # A conclusion can be patched outside the numbered derivation as well as
    # in its final step. This literal flag leaves substantive uptake to readers.
    if old == new:
        return claims_changed or answer_changed
    return len(old) >= 2 and old[:-1] == new[:-1] and claims_changed


def _host_objection_id(prefix: str, relation_id: str, number: int) -> str:
    safe = "".join(ch if ch.isalnum() else "-" for ch in relation_id).strip("-")
    return f"{prefix}-{number:03d}-{safe}"


def _fork_locator(answer: dict, fork: dict, relation_id: str) -> dict | None:
    claim = next((item for item in answer.get("claims", [])
                  if item["relation_id"] == relation_id), None)
    if claim is None:
        return None
    for step in answer.get("derivation_steps", []):
        if claim["quote"] in step["statement"] or relation_id in step["statement"]:
            return {"step_index": step["step_index"], "step_quote": step["statement"],
                    "branch_point_id": fork["branch_point_id"],
                    "earliest_reason": "Earliest public step explicitly supporting the discrepant relation."}
    return None


def construct_recoding_objections(canonical: dict, recoded: dict, working: dict,
                                  fork: dict, *, prefix="recoding", map_identity="identity") -> list[dict]:
    if canonical.get("decision") != "answered" or recoded.get("decision") != "answered":
        return []
    left, right = _claim_map(canonical["claims"]), _claim_map(recoded["claims"])
    objections = []
    for relation_id in sorted(set(left) & set(right)):
        if type(left[relation_id]) is type(right[relation_id]) and _json(left[relation_id]) == _json(right[relation_id]):
            continue
        locator = _fork_locator(working, fork, relation_id)
        if locator is None:
            continue
        check_id = _host_objection_id(prefix + "-check", relation_id, len(objections) + 1)
        objections.append({
            "target_claim": relation_id,
            "text": ("The canonical and transformed blind solves disagree after the declared inverse map: "
                     f"{_json(left[relation_id])} versus {_json(right[relation_id])}. No winner is declared."),
            "defeats": "The working value for " + relation_id,
            "check": {"check_id": check_id, "kind": "value",
                      "inputs": [{"name": "canonical", "value": left[relation_id],
                                  "source": "blind canonical solve: " + canonical.get("derivation", "")},
                                 {"name": "transformed", "value": right[relation_id],
                                  "source": "blind transformed solve: " + recoded.get("derivation", "")},
                                 {"name": "inverse_map", "value": map_identity,
                                  "source": "validated coding manifest"}],
                      "procedure": "Recompute both coded problems and apply the declared inverse output map.",
                      "claimed_result": {"canonical": left[relation_id], "transformed": right[relation_id]},
                      "falsifies_when": "The independently recomputed canonical values agree type-preservingly."},
            "fork": locator,
        })
    return objections


def construct_checker_objection(execution: dict, proposal: dict, working: dict,
                                 fork: dict, *, prefix="checker") -> dict | None:
    if execution.get("status") != "COMPLETE" or execution.get("comparison") != "disagrees":
        return None
    parsed = execution.get("parsed") or {}
    relation_id = proposal["relation_id"]
    locator = _fork_locator(working, fork, relation_id)
    if locator is None:
        return None
    check_id = _host_objection_id(prefix + "-check", relation_id, 1)
    return {"target_claim": relation_id,
            "text": ("The host-run bounded checker disagrees with the working claim: "
                     f"working {_json(proposal['working_value'])}; checker {_json(parsed.get('value'))}."),
            "defeats": "The working value for " + relation_id,
            "check": {"check_id": check_id, "kind": "value",
                      "inputs": [{"name": "stdin_json", "value": proposal["stdin_json"], "source": "use proposal"},
                                 {"name": "source", "value": proposal["source"], "source": "exact use proposal source"},
                                  {"name": "source_sha256", "value": sha(proposal["source"]), "source": "use proposal source"},
                                  {"name": "stdout_utf8", "value": execution.get("stdout_utf8", ""), "source": "exact host stdout"},
                                  {"name": "host_result", "value": parsed, "source": "parsed host result"},
                                 {"name": "stdout_sha256", "value": execution.get("stdout_sha256"), "source": "host execution"}],
                      "procedure": "Redo the proposed deterministic computation from its preserved source and input.",
                      "claimed_result": parsed.get("value"),
                      "falsifies_when": "The redone computation agrees type-preservingly with the working value."},
            "fork": locator}


def bind_checker_execution(execution: dict, proposal_bytes: bytes,
                           policy: dict, proposal: dict) -> dict:
    """Bind a schema-valid checker receipt to the exact current public inputs."""
    expected = {
        "proposal_sha256": hashlib.sha256(proposal_bytes).hexdigest(),
        "policy_sha256": hashlib.sha256((_json(policy) + "\n").encode("utf-8")).hexdigest(),
        "source_sha256": hashlib.sha256(proposal["source"].encode("utf-8")).hexdigest(),
        "stdin_sha256": hashlib.sha256((_json(proposal["stdin_json"]) + "\n").encode("utf-8")).hexdigest(),
    }
    mismatches = [key for key, value in expected.items() if execution.get(key) != value]
    if execution.get("status") == "COMPLETE":
        parsed = execution.get("parsed")
        if not isinstance(parsed, dict) or parsed.get("relation_id") != proposal["relation_id"]:
            mismatches.append("parsed.relation_id")
    if mismatches:
        raise ReasonFailure("RUN_INTEGRITY_ERROR",
                            "Checker execution does not bind current inputs: " + ", ".join(mismatches))
    return execution


def _mint(items: list[dict], prefix: str, cycle: int, source: str) -> list[dict]:
    result = []
    for number, item in enumerate(items, 1):
        saved = deepcopy(item)
        source_call = saved.pop("_source_call", None)
        source_lineage = saved.pop("_source_endpoint", None)
        saved.update(id=f"{prefix}-o{number:03d}", source=source, born_cycle=cycle,
                     status="unresolved", reason="Awaiting operative return.",
                     history=[{"cycle": cycle, "status": "unresolved",
                               "reason": "New objection awaiting operative return."}])
        if source_call:
            saved["source_call"] = source_call
        if source_lineage:
            saved["source_lineage"] = source_lineage
        result.append(saved)
    return result


def _check_unique_ids(existing: list[dict], new_items: list[dict]):
    ids = [obj.get("check", {}).get("check_id") for obj in [*existing, *new_items]
           if obj.get("check")]
    if len(ids) != len(set(ids)):
        raise ReasonFailure("SCHEMA_FAILURE", "Check IDs must be unique across the occurrence")


def _problem_paths(coding_path, coding, problem_id, problem=None, relation=None, fork=None):
    from .r002_custody import validate_coding
    return validate_coding(coding_path, coding, problem_id, problem, relation, fork)


def _create(problem: str, out, *, mode: str, condition: str, problem_id,
            relation_registry, recipe_path=None, cycles=3, attempt_policy="strict",
            prompt_token_cap=32768, tokenizer_pins=None, fork_registry=None,
            coding_manifest=None, checker_policy=None, capability=None,
            schema_path=None, completion_tokens=32768, study_profile=None,
            canonical_registry=None):
    if not isinstance(problem, str) or not problem.strip():
        raise ValueError("PROBLEM_EMPTY")
    if type(completion_tokens) is not int or completion_tokens != 32768:
        raise ReasonFailure("CONFIG_ERROR", "R002 native completion ceiling is exactly 32768")
    if mode not in {"offline", "live"} or attempt_policy != "strict":
        raise ReasonFailure("CONFIG_ERROR", "R002 requires offline/live mode and strict attempts")
    if type(cycles) is not int or not 1 <= cycles <= 3 or prompt_token_cap != 32768:
        raise ReasonFailure("CONFIG_ERROR", "R002 permits one to three cycles and a 32768 prompt cap")
    if study_profile not in {None, config.R003_PROFILE}:
        raise ReasonFailure("CONFIG_ERROR", "Unknown strict study profile")
    if study_profile is None and canonical_registry is not None:
        raise ReasonFailure("CONFIG_ERROR", "Canonical registry is specific to r003-open-v1")
    if study_profile == config.R003_PROFILE:
        if condition not in {"NATIVE", "LOOP-CROSS", "LOOP-DECOMPOSED"}:
            raise ReasonFailure("CONFIG_ERROR", "Condition is outside R003 occurrence 1")
        if coding_manifest is not None or checker_policy is not None:
            raise ReasonFailure("CONFIG_ERROR", "R003 occurrence 1 disables recoding and checker execution")
    relations, relations_text, _relations_path = _load_object(relation_registry, "relation registry")
    problem_id = _infer_problem_id(problem_id, problem, relations)
    relation = _relation_entry(relations, problem_id)
    if study_profile == config.R003_PROFILE:
        ContractSet(config.R003_DIR / "contracts").validate("r003-relations.schema.json", relations)
    else:
        ContractSet(config.R002_DIR / "contracts").validate("relations.schema.json", relations)
    cap = validate_capability(capability, condition, mode, study_profile)
    if condition == "LOOP-CHECKER" and mode == "live":
        from .checker import host_qualified
        if not host_qualified():
            raise ReasonFailure("CHECKER_UNQUALIFIED", "Checker host/runtime lacks this review qualification")
    tokenizers = snapshot_tokenizers(tokenizer_pins, mode)
    endpoints = config.load_endpoint_snapshot()
    recipe = recipe_text = recipe_source = None
    if recipe_path is not None:
        loaded = (config.load_r003_recipe(recipe_path) if study_profile == config.R003_PROFILE
                  else config.load_r002_recipe(recipe_path))
        recipe, recipe_text = loaded["data"], loaded["text"]
        recipe_source = Path(loaded["source"])
        if recipe["condition"] != condition:
            raise ReasonFailure("CONFIG_ERROR", "Condition does not match recipe")
        if cycles > recipe["cycles"]:
            raise ReasonFailure("CONFIG_ERROR", "Cycle request exceeds recipe")
        if recipe["condition"] == "LOOP-DECOMPOSED" and cycles != 3:
            raise ReasonFailure("CONFIG_ERROR", "LOOP-DECOMPOSED has exactly three one-step cycles")
    amendment = recipe.get("amendment") if recipe is not None else None
    if amendment not in {None, "R3-A1", "R3-A2"}:
        raise ReasonFailure("CONFIG_ERROR", "Unknown R003 amendment")
    if amendment in {"R3-A1", "R3-A2"} and study_profile != config.R003_PROFILE:
        raise ReasonFailure("CONFIG_ERROR", f"{amendment} is specific to r003-open-v1")
    if amendment in {"R3-A1", "R3-A2"} and mode == "live":
        expected_preflight = get(config.R003_DIR / "R003-input-preflight.json")
        if tokenizers != expected_preflight:
            raise ReasonFailure(
                "TOKENIZER_MISMATCH",
                f"{amendment} live runs require the exact registered R003 input-preflight descriptor")
    forks, forks_text, _forks_path = _load_object(fork_registry, "fork registry", optional=True)
    coding, coding_text, coding_path = _load_object(coding_manifest, "coding manifest", optional=True)
    if recipe is not None and forks is None:
        raise ReasonFailure("CONFIG_ERROR", "Loop conditions require the public fork registry")
    fork = _candidate(forks, problem_id, "fork registry") if forks else None
    coding_entry = _candidate(coding, problem_id, "coding manifest") if coding else None
    canonical = canonical_text = canonical_path = canonical_entry = canonical_custody = None
    if study_profile == config.R003_PROFILE:
        canonical, canonical_text, canonical_path = _load_object(
            canonical_registry, "canonical registry")
        ContractSet(config.R003_DIR / "contracts").validate(
            "canonical-registry.schema.json", canonical)
        if forks is not None:
            ContractSet(config.R003_DIR / "contracts").validate("forks.schema.json", forks)
        from .r002_custody import validate_r003_canonical
        canonical_entry, canonical_custody = validate_r003_canonical(
            canonical_path, canonical, problem_id, problem)
    if recipe is not None and study_profile != config.R003_PROFILE:
        ContractSet(config.R002_DIR / "contracts").validate("coding-manifest.schema.json", coding)
        coded = _problem_paths(coding_path, coding, problem_id, problem, relation, fork)
    else:
        coded = {}
    directory = Path(out)
    guard(directory / "calls" / "c0003-signal-a" / "a00" / "provider" / ("x" * 65))
    if directory.exists():
        raise ValueError("RUN_EXISTS")
    directory.mkdir(parents=True)
    contract_source = config.R002_DIR / "contracts"
    if schema_path is not None and (Path(schema_path).name != "answer.schema.json" or
            Path(schema_path).read_bytes() != (contract_source / "answer.schema.json").read_bytes()):
        raise ReasonFailure("CONFIG_ERROR", "Native schema differs from the published answer contract")
    for path in sorted(contract_source.glob("*.schema.json")):
        write(directory / "contracts" / path.name, read(path))
    if study_profile == config.R003_PROFILE:
        for path in sorted((config.R003_DIR / "contracts").glob("*.schema.json")):
            write(directory / "contracts" / path.name, read(path))
    write(directory / "problem.txt", problem)
    write(directory / "relations.json", relations_text)
    write(directory / "endpoints.json", endpoints["text"])
    if recipe_text:
        write(directory / "recipe.json", recipe_text)
    if forks_text:
        write(directory / "forks.json", forks_text)
    if coding_text:
        write(directory / "coding-manifest.json", coding_text)
    if canonical_text:
        write(directory / "canonical-registry.json", canonical_text)
        put(directory / "canonical-custody.json", canonical_custody)
    for key, text in coded.items():
        write(directory / "coded" / (key + ".txt"), text)
    if condition == "LOOP-CHECKER" and checker_policy is None:
        from .checker import DEFAULT_POLICY
        checker_policy = DEFAULT_POLICY
    if checker_policy is not None:
        if isinstance(checker_policy, dict):
            checker_text = json.dumps(checker_policy, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        else:
            checker_text = read(Path(checker_policy))
        write(directory / "checker-policy.json", checker_text)
    run_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + "-r002-" + uuid.uuid4().hex[:6]
    cfg = {"schema": R002_SCHEMA, "run_id": run_id, "created_epoch": time.time(),
           "mode": mode, "condition": condition, "problem_id": problem_id, "cycles": cycles,
           "attempt_policy": "strict", "prompt_token_cap": prompt_token_cap,
           "prompt_contract": (prompts.R003_A2_CONTRACT if amendment == "R3-A2" else
                                prompts.R003_A1_CONTRACT if amendment == "R3-A1" else
                                config.R003_PROFILE if study_profile == config.R003_PROFILE else
                                prompts.R002_CONTRACT),
           "completion_tokens": completion_tokens,
           "problem_sha256": sha(problem), "relations_sha256": sha(relations_text),
           "endpoints_sha256": endpoints["sha256"], "tokenizers": tokenizers,
           "capability": cap, "claim_ceiling": CLAIM,
           "checker_policy_sha256": sha(read(directory / "checker-policy.json"))
               if (directory / "checker-policy.json").exists() else None,
            "inputs": {"recipe": sha(recipe_text) if recipe_text else None,
                       "forks": sha(forks_text) if forks_text else None,
                       "coding": sha(coding_text) if coding_text else None}}
    if study_profile == config.R003_PROFILE:
        cfg["study_profile"] = study_profile
        cfg["amendment"] = amendment
        cfg["inputs"].update({
            "canonical_registry": sha(canonical_text),
            "canonical_custody": sha(read(directory / "canonical-custody.json")),
        })
    from .r002_custody import freeze_inputs
    freeze_inputs(directory, cfg)
    return directory


def create_r002_run(problem: str, recipe_path, out, *, mode="offline", cycles=3,
                    attempt_policy="strict", prompt_token_cap=32768, tokenizer_pins=None,
                    relation_registry=None, fork_registry=None, coding_manifest=None,
                    checker_policy=None, capability=None, problem_id=None,
                    study_profile=None, canonical_registry=None) -> Path:
    loaded = (config.load_r003_recipe(recipe_path) if study_profile == config.R003_PROFILE
              else config.load_r002_recipe(recipe_path))
    return _create(problem, out, mode=mode, condition=loaded["data"]["condition"],
                   problem_id=problem_id, relation_registry=relation_registry,
                   recipe_path=recipe_path, cycles=cycles, attempt_policy=attempt_policy,
                   prompt_token_cap=prompt_token_cap, tokenizer_pins=tokenizer_pins,
                   fork_registry=fork_registry, coding_manifest=coding_manifest,
                   checker_policy=checker_policy, capability=capability,
                   study_profile=study_profile, canonical_registry=canonical_registry)


def create_r002_native_run(problem: str, out, *, mode="offline", condition="NATIVE",
                           schema_path=None, completion_tokens=32768,
                           attempt_policy="strict", prompt_token_cap=32768,
                           tokenizer_pins=None, relation_registry=None, capability=None,
                           problem_id=None, study_profile=None, canonical_registry=None) -> Path:
    if condition not in {"NATIVE", "CAL-NATIVE"}:
        raise ReasonFailure("CONFIG_ERROR", "Native condition must be NATIVE or CAL-NATIVE")
    return _create(problem, out, mode=mode, condition=condition, problem_id=problem_id,
                   relation_registry=relation_registry, schema_path=schema_path,
                   cycles=1, attempt_policy=attempt_policy, prompt_token_cap=prompt_token_cap,
                   tokenizer_pins=tokenizer_pins, capability=capability,
                    completion_tokens=completion_tokens, study_profile=study_profile,
                    canonical_registry=canonical_registry)


def _validate_run(directory: Path):
    from .r002_custody import validate_frozen_inputs
    cfg = validate_frozen_inputs(directory)
    for name, key in (("problem.txt", "problem_sha256"), ("relations.json", "relations_sha256"),
                      ("endpoints.json", "endpoints_sha256")):
        if sha(read(directory / name)) != cfg[key]:
            raise ReasonFailure("RUN_INTEGRITY_ERROR", "Saved R002 input changed: " + name)
    for name, digest in cfg["inputs"].items():
        if digest is not None:
            actual_name = {"recipe": "recipe.json", "forks": "forks.json",
                           "coding": "coding-manifest.json", "canonical_registry": "canonical-registry.json",
                           "canonical_custody": "canonical-custody.json"}[name]
            if sha(read(directory / actual_name)) != digest:
                raise ReasonFailure("RUN_INTEGRITY_ERROR", "Saved R002 input changed: " + actual_name)
    recipe = get(directory / "recipe.json") if (directory / "recipe.json").exists() else None
    relations = get(directory / "relations.json")
    relation = _relation_entry(relations, cfg["problem_id"])
    fork = _candidate(get(directory / "forks.json"), cfg["problem_id"], "fork registry") \
        if (directory / "forks.json").exists() else None
    coding = _candidate(get(directory / "coding-manifest.json"), cfg["problem_id"], "coding manifest") \
        if (directory / "coding-manifest.json").exists() else None
    return cfg, recipe, read(directory / "problem.txt"), relation, fork, coding, get(directory / "endpoints.json")


def _offline(role, cycle, objections, context):
    missing = f"OFFLINE FIXTURE: {role} has no substantive derivation."
    if role == "answer":
        return {"decision": "cannot_decide", "answer": "", "missing_derivation": missing,
                "claims": [], "derivation_steps": []}
    if role == "initial_decompose":
        result = {"plan": [], "first_step": None, "cannot_decide": {"missing": missing}}
        if _r3_commitment_contract(context.get("contract_version")):
            result["decisive_step"] = None
        return result
    if role == "decomposed_step":
        result = {"step": context["expected_step"]["step"], "derivation": "", "result": "",
                  "cannot_decide": {"missing": missing}}
        if _r3_commitment_contract(context.get("contract_version")):
            result["commitments"] = []
        return result
    if role in {"prose_critic", "tested_critic", "decomposed_critic"}:
        return {"decision": "cannot_decide", "missing_derivation": missing,
                "working": "OFFLINE FIXTURE", "objections": []}
    if role in {"prose_return", "tested_return"}:
        dispositions = []
        for objection in objections:
            item = {"id": objection["id"], "status": "unresolved", "reason": missing,
                    "rederivation": {"from_step_index": None, "objection_id": objection["id"],
                                     "status": "cannot_decide", "steps": [],
                                     "missing_derivation": missing}}
            if role == "tested_return":
                item["redo"] = {"check_id": objection["check"]["check_id"],
                                "status": "cannot_redo", "method": missing, "result": None,
                                "comparison": "inconclusive"}
            dispositions.append(item)
        before = context["before"]
        return {"decision": "cannot_decide", "answer": before.get("answer") or "OFFLINE FIXTURE",
                "missing_derivation": missing, "claims": before.get("claims", []),
                "dispositions": dispositions, "changes": [],
                "derivation_steps": before.get("derivation_steps", [])}
    if role == "decomposed_return":
        dispositions = []
        for objection in objections:
            dispositions.append({"id": objection["id"], "status": "unresolved", "reason": missing,
                                 "redo": {"check_id": objection["check"]["check_id"],
                                          "status": "cannot_redo", "method": missing,
                                          "result": None, "comparison": "inconclusive"}})
        result = {"decision": "cannot_decide", "missing_derivation": missing,
                  "step": context["before"]["step"], "derivation": "", "result": "",
                  "dispositions": dispositions}
        if _r3_commitment_contract(context.get("contract_version")):
            result["commitments"] = []
        return result
    if role == "propagation_use":
        relation_id = context["relation"]["relations"][0]["relation_id"]
        return {"decision": "cannot_decide", "missing_derivation": missing,
                "query_id": f"fixture-{cycle}", "question": "", "problem_derivation": "",
                "before": {"answer_quote": "", "derivation": "", "conclusion": None},
                "after": {"answer_quote": "", "derivation": "", "conclusion": None},
                "dependency": {"relation_id": relation_id, "before_quote": "", "after_quote": "",
                               "result_depends_on_change": False, "explanation": missing},
                "objections": [], "checker": None}
    if role == "decomposed_use":
        return {"decision": "cannot_decide", "missing_derivation": missing,
                "step": context["expected_step"]["step"], "status": "inconclusive",
                "method": "", "result": None}
    if role == "blind_coding_solve":
        return {"decision": "cannot_decide", "missing_derivation": missing,
                "coding_id": context["coding_id"], "claims": [], "derivation": "",
                "derivation_steps": []}
    if role == "decomposed_synthesis":
        result = {"decision": "cannot_decide", "answer": "", "missing_derivation": missing,
                  "claims": [], "derivation_steps": []}
        if _r3_commitment_contract(context.get("contract_version")):
            commitments = _decisive_commitments(
                context.get("accepted_steps", []), context["decisive_step"])
            result.update(decisive_step=context["decisive_step"],
                          decisive_claim=commitments[0] if commitments else "")
        return result
    if role == "decomposed_closing":
        result = {"decision": "cannot_decide", "answer": "", "missing_derivation": missing,
                  "claims": [], "derivation_steps": [],
                  "dispositions": [{"id": item["id"], "status": "unresolved", "reason": missing}
                                   for item in objections if item.get("status") == "unresolved"]}
        if _r3_commitment_contract(context.get("contract_version")):
            commitments = _decisive_commitments(
                context.get("accepted_steps", []), context["decisive_step"])
            result.update(decisive_step=context["decisive_step"],
                          decisive_claim=commitments[0] if commitments else "")
        return result
    return {"decision": "cannot_decide", "missing_derivation": missing, "answer": "", "derivation": ""}


def _scripted_reply(scripted, role, cycle, objections, coordinate, context):
    if scripted is None:
        return _offline(role, cycle, objections, context)
    try:
        return scripted(role=role, cycle=cycle, objections=deepcopy(objections),
                        coordinate=deepcopy(coordinate), context=deepcopy(context))
    except TypeError:
        return scripted(role, cycle, deepcopy(objections))


def _repair_messages(role: str, contracts: ContractSet, content: str, detail: str, *,
                     study_profile=None, contract_version=None,
                     original_user_content: str | None = None) -> list[dict[str, str]]:
    """Render one bounded repair from the seat's own complete output and contract."""
    instruction = (
        "The preceding public response did not satisfy the response schema. Repair only its JSON "
        "structure and required fields under the exact same role contract. Preserve its substantive "
        "content and conclusions; do not solve again, introduce new evidence, drop a maintained "
        "objection, or otherwise reconsider the response. Return exactly one JSON object without "
        "markdown fences."
    )
    blocks = []
    if _r3_commitment_contract(contract_version):
        if not isinstance(original_user_content, str) or not original_user_content:
            raise ReasonFailure("CONFIG_ERROR", "R3 amendment repair requires the original public task context")
        blocks.append(("ORIGINAL PUBLIC TASK CONTEXT", original_user_content))
        if contract_version == prompts.R003_A2_CONTRACT:
            instruction += (
                " The original public task context and candidate targeted step text in the recorded "
                "failure remain authoritative. For a fork-locator failure, either use the real "
                "step_index with an empty step_quote, or copy at least 40 characters from that step; "
                "do not fabricate or paraphrase locator text."
            )
        else:
            instruction += (
                " The original public task context above remains authoritative. For an exact-quote failure, "
                "copy the required locator text exactly from that context; do not paraphrase it."
            )
    blocks.extend([
        ("YOUR OWN PRECEDING PUBLIC OUTPUT", content),
        ("RECORDED SCHEMA FAILURE", detail),
        ("SCHEMA REPAIR INSTRUCTION", instruction),
        *contracts.prompt_blocks(role, contract_version),
    ])
    return prompts.render_r002(role, blocks, study_profile=study_profile,
                               contract_version=contract_version)


def _call(directory: Path, adapter: Adapter, cfg: dict, contracts: ContractSet,
          *, role: str, seat: dict, call_id: str, cycle: int, blocks: list[tuple[str, str]],
          parse_context: dict, scripted, after_call, before_call, tokenizer_counter,
          max_tokens: int, schema_repair_budget: int = 0):
    contract_version = cfg.get("prompt_contract")
    messages = prompts.render_r002(
        role, [*blocks, *contracts.prompt_blocks(role, contract_version)],
        study_profile=cfg.get("study_profile"), contract_version=contract_version)
    original_user_content = messages[1]["content"]
    attempt = 0
    while True:
        coordinate = {"call_id": call_id, "cycle": cycle, "attempt": attempt,
                      "condition": cfg["condition"], "strict": True,
                      "schema_repair": bool(attempt)}
        prepared = adapter.prepare(seat=seat, messages=messages, max_tokens=max_tokens,
                                   thinking=seat["thinking"], role=role, coordinate=coordinate)
        if tokenizer_counter is None:
            preflight = token_preflight(
                messages, seat["endpoint"], pins=cfg["tokenizers"], mode=cfg["mode"],
                limit=cfg["prompt_token_cap"], wire_body_text=prepared["wire_body_text"],
                condition=cfg["condition"], role=role)
        else:
            preflight = tokenizer_counter(messages, seat["endpoint"], pins=cfg["tokenizers"],
                                          mode=cfg["mode"], limit=cfg["prompt_token_cap"])
        folder = directory / "calls" / call_id / f"a{attempt:02d}"
        request_path, response_path = folder / "request.json", folder / "response.json"
        if request_path.exists():
            intent = get(request_path)
            if (intent["role"] != role or intent["seat"] != seat or intent["cycle"] != cycle
                    or intent.get("attempt", 0) != attempt
                    or intent.get("schema_repair", False) != bool(attempt)
                    or intent["prepared"]["messages"] != messages
                    or intent["prepared"]["wire_body_sha256"] != prepared["wire_body_sha256"]
                    or intent["prepared"]["kwargs"]["max_tokens"] != max_tokens
                    or intent["preflight"] != preflight):
                raise ReasonFailure("RUN_INTEGRITY_ERROR", "Saved strict request differs from reconstruction")
        saved = None
        result = None
        wrote_response = False
        if response_path.exists():
            saved = get(response_path)
        elif request_path.exists():
            try:
                result = adapter.recover(folder / "provider")
                if result is None:
                    raise ReasonFailure("INTERRUPTED_CALL", "Dispatch outcome unknown; strict occurrence is not replayed")
            except ReasonFailure as exc:
                if exc.code == "INTERRUPTED_CALL":
                    raise
                saved = {"epoch": time.time(), "status": exc.code, "detail": exc.detail,
                         "record": exc.record}
                put(response_path, saved)
                wrote_response = True
                result = None
        else:
            if before_call is not None and cfg["mode"] == "live":
                before_call(coordinate)
            put(request_path, {"epoch": time.time(), "role": role, "seat": seat,
                               "cycle": cycle, "attempt": attempt,
                               "schema_repair": bool(attempt), "preflight": preflight,
                               "prepared": prepared})
            fixture_context = {**parse_context, "contract_version": contract_version}
            fixture = _scripted_reply(scripted, role, cycle, parse_context.get("objections", []),
                                      coordinate, fixture_context) if cfg["mode"] == "offline" else None
            try:
                result = adapter.call(seat=seat, messages=messages, records_dir=folder / "provider",
                                      max_tokens=max_tokens, thinking=seat["thinking"], role=role,
                                      coordinate=coordinate, scripted=fixture)
            except ReasonFailure as exc:
                saved = {"epoch": time.time(), "status": exc.code, "detail": exc.detail,
                         "record": exc.record}
                put(response_path, saved)
                wrote_response = True
                result = None
        if saved is None and result is not None:
            try:
                parsed = parse_r002(role, result["content"], contracts,
                                    contract_version=contract_version, **parse_context)
                saved = {"epoch": time.time(), "status": "COMPLETE", "result": result,
                         "parsed": parsed}
            except (ReasonFailure, TypeError, ValueError, KeyError) as exc:
                code = getattr(exc, "code", "SCHEMA_FAILURE")
                saved = {"epoch": time.time(), "status": code,
                         "detail": getattr(exc, "detail", type(exc).__name__), "result": result}
            put(response_path, saved)
            wrote_response = True
        if wrote_response and after_call is not None:
            after_call(call_id, deepcopy(saved))
        if saved["status"] == "COMPLETE":
            return saved["parsed"]
        if (saved["status"] == "SCHEMA_FAILURE" and attempt < schema_repair_budget
                and isinstance(saved.get("result", {}).get("content"), str)):
            messages = _repair_messages(role, contracts, saved["result"]["content"],
                                        saved.get("detail", "SCHEMA_FAILURE"),
                                        study_profile=cfg.get("study_profile"),
                                        contract_version=contract_version,
                                        original_user_content=original_user_content)
            attempt += 1
            continue
        raise ReasonFailure(saved["status"], saved.get("detail", "Strict R002 call failed"))

def _seat(role, recipe):
    if recipe is None:
        return {"endpoint": "deepseek-flash", "thinking": "native",
                "reasoning_effort": "medium", "role": "answer"}
    return recipe["seats"][role]


def _answer_blocks(problem, relation):
    return [("PROBLEM", problem), ("PUBLIC RELATIONS", _json(relation))]


def _answer_text(answer):
    return _json(answer)


def _critic_blocks(problem, answer, objections, relation, fork):
    blocks = _answer_blocks(problem, relation)
    blocks += [("WORKING ANSWER", _answer_text(answer)), ("PUBLIC FORK", _json(fork))]
    if objections:
        blocks.append(("PRIOR OBJECTIONS", _json(objections)))
    return blocks


def _return_blocks(problem, before, objections, relation, fork, signals=None):
    blocks = _answer_blocks(problem, relation)
    blocks += [("BEFORE ANSWER", _answer_text(before)), ("PUBLIC FORK", _json(fork)),
               ("OPEN AND NEW OBJECTIONS", _json(objections))]
    if signals:
        blocks.append(("PUBLIC SIGNALS", _json(signals)))
    return blocks


def _coding_blocks(coded_problem, relation, fork, coding_entry, coding_id):
    public = {key: coding_entry[key] for key in ("candidate_id", "presentation_transform",
              "semantic_invariants", "relation_ids")}
    public["coding_id"] = coding_id
    return [("CODED PROBLEM", coded_problem), ("PUBLIC RELATIONS", _json(relation)),
            ("PUBLIC FORK", _json(fork)), ("CODING DECLARATION", _json(public))]


def _step_answer(step: dict, plan_step: dict) -> dict:
    return {"decision": "answered", "answer": step["result"], "missing_derivation": "",
            "claims": [], "derivation_steps": [{"step_index": step["step"],
                "statement": step["derivation"], "depends_on": list(plan_step["depends_on"])}]}


def _decomposed_step_blocks(problem: str, plan: list[dict], plan_step: dict,
                            accepted_steps: list[dict]) -> list[tuple[str, str]]:
    return [("PROBLEM", problem), ("DECOMPOSITION PLAN", _json(plan)),
            ("CURRENT PLAN STEP", _json(plan_step)),
            ("ACCEPTED PRIOR STEPS", _json(accepted_steps))]


def _decomposed_critic_blocks(problem: str, plan_step: dict, current: dict,
                              accepted_steps: list[dict], fork: dict) -> list[tuple[str, str]]:
    return [("PROBLEM", problem), ("CURRENT PLAN STEP", _json(plan_step)),
            ("ACCEPTED DEPENDENCIES", _json(accepted_steps)),
            ("CURRENT STEP", _json(current)), ("PUBLIC FORK", _json(fork))]


def _decomposed_return_blocks(problem: str, plan_step: dict, current: dict,
                              accepted_steps: list[dict], objections: list[dict]) -> list[tuple[str, str]]:
    return [("PROBLEM", problem), ("CURRENT PLAN STEP", _json(plan_step)),
            ("ACCEPTED DEPENDENCIES", _json(accepted_steps)),
            ("CURRENT STEP", _json(current)), ("TESTED OBJECTIONS", _json(objections))]


def _decomposed_use_blocks(problem: str, plan_step: dict, returned: dict,
                           accepted_steps: list[dict], *,
                           contract_version: str | None = None) -> list[tuple[str, str]]:
    returned_keys = ["step", "derivation", "result"]
    if contract_version == prompts.R003_A2_CONTRACT:
        returned_keys.append("commitments")
    return [("PROBLEM", problem), ("CURRENT PLAN STEP", _json(plan_step)),
            ("ACCEPTED DEPENDENCIES", _json(accepted_steps)),
             ("RETURNED STEP", _json({key: returned[key] for key in returned_keys}))]


def _decomposed_closing_blocks(problem: str, plan: list[dict], accepted_steps: list[dict],
                               answer: dict | None, objections: list[dict],
                               stop_reason: str, stop_detail: str,
                               decisive_step: int | None = None,
                               include_decisive: bool = False) -> list[tuple[str, str]]:
    blocks = [("PROBLEM", problem), ("DECOMPOSITION PLAN", _json(plan))]
    if include_decisive:
        blocks.append(("DECLARED DECISIVE STEP", _json(decisive_step)))
    blocks.extend([
            ("IMMUTABLE ACCEPTED STEPS", _json(accepted_steps)),
            ("CURRENT ANSWER", _json(answer)),
            ("FULL OBJECTION AND DISPOSITION HISTORY", _json(objections)),
            ("SEMANTIC STOP REASON", _json({"reason": stop_reason, "detail": stop_detail}))])
    return blocks


def _apply_dispositions(all_objections, dispositions, cycle, phase=None):
    by_id = {item["id"]: item for item in dispositions}
    for objection in all_objections:
        if objection["id"] in by_id:
            item = by_id[objection["id"]]
            objection["status"], objection["reason"] = item["status"], item["reason"]
            history = {"cycle": cycle, "status": item["status"], "reason": item["reason"]}
            if "redo" in item:
                history["redo"] = deepcopy(item["redo"])
                history["check_redone"] = (
                    "agrees" if item["redo"]["comparison"] == "supports_objection"
                    else "disagrees" if item["redo"]["comparison"] == "opposes_objection"
                    else "inconclusive") if item["redo"]["status"] == "redone" else "not-redone"
            if "rederivation" in item:
                history["rederivation"] = deepcopy(item["rederivation"])
            if phase:
                history["phase"] = phase
            objection["history"].append(history)
        else:
            history = {"cycle": cycle, "status": objection["status"], "reason": objection["reason"],
                       "carried": True}
            if phase:
                history["phase"] = phase
            objection["history"].append(history)


def _write_episode_records(directory: Path, cfg: dict, objections: list[dict]):
    from .r002_reports import write_episode_records
    return write_episode_records(directory, cfg, objections)


def _reports(directory, cfg, state, answer, objections, events):
    from .r002_reports import reports
    return reports(directory, cfg, state, answer, objections, events)


def _state(condition):
    return {"schema": R002_STATE_SCHEMA, "condition": condition, "stop_reason": "pending",
            "completed_cycles": 0, "calls": 0, "attempts": 0, "tail_edits": 0,
            "stall_switches": 0, "checker_runs": 0, "cannot_decide_responses": 0,
            "closing_return": "not-run", "objections": []}


def _finish_decomposed(directory, cfg, state, answer, objections, events):
    state["answer"], state["events"] = answer, events
    _write_episode_records(directory, cfg, objections)
    _reports(directory, cfg, state, answer, objections, events)
    return state


def _execute_decomposed(directory, cfg, recipe, problem, relation, fork,
                        state, events, objections, call):
    initial = call("initial_decompose", _seat("initial", recipe), "initial", 0,
                   _answer_blocks(problem, relation))
    state["decomposition_plan"] = initial["plan"]
    state["accepted_steps"] = []
    if initial["cannot_decide"] is not None:
        state["cannot_decide_responses"] += 1
        state["stop_reason"] = "initial_cannot_decide"
        state["stop_detail"] = initial["cannot_decide"]["missing"]
        return _finish_decomposed(directory, cfg, state, None, objections, events)

    plan = initial["plan"]
    decisive_step = initial.get("decisive_step")
    r3_commitment = _r3_commitment_contract(cfg.get("prompt_contract"))
    if r3_commitment:
        state["decisive_step"] = decisive_step
    accepted_steps = state["accepted_steps"]
    current = initial["first_step"]
    latest_step = deepcopy(current)

    def semantic_finish(stop_reason, stop_detail, answer=None):
        state["stop_reason"], state["stop_detail"] = stop_reason, stop_detail
        if cfg.get("study_profile") == config.R003_PROFILE and state["completed_cycles"] > 0:
            closing_answer = answer if answer is not None else {
                "kind": "latest_decomposed_step",
                "accepted": any(item["step"] == latest_step["step"] for item in accepted_steps),
                "value": deepcopy(latest_step),
            }
            closing = call(
                "decomposed_closing", _seat("closing", recipe), "closing-return",
                state["completed_cycles"],
                _decomposed_closing_blocks(problem, plan, accepted_steps, closing_answer, objections,
                                           stop_reason, stop_detail, decisive_step, r3_commitment),
                answer=closing_answer, objections=list(objections), accepted_steps=list(accepted_steps),
                decisive_step=decisive_step)
            _apply_dispositions(objections, closing["dispositions"],
                                state["completed_cycles"], "decomposed_closing")
            state["closing_return"] = "complete"
            answer = closing
            _write_episode_records(directory, cfg, objections)
        return _finish_decomposed(directory, cfg, state, answer, objections, events)

    for cycle, plan_step in enumerate(plan[:cfg["cycles"]], 1):
        if cycle > 1:
            current = call("decomposed_step", _seat("step", recipe), f"c{cycle:04d}-step", cycle,
                           _decomposed_step_blocks(problem, plan, plan_step, accepted_steps),
                           expected_step=plan_step, accepted_steps=accepted_steps)
            latest_step = deepcopy(current)
            if current["cannot_decide"] is not None:
                state["cannot_decide_responses"] += 1
                return semantic_finish("step_unresolved", current["cannot_decide"]["missing"])

        current_answer = _step_answer(current, plan_step)
        critic_slot = f"critic_cycle_{cycle}"
        critic_id = f"c{cycle:04d}-critic"
        critic = call("decomposed_critic", _seat(critic_slot, recipe), critic_id, cycle,
                      _decomposed_critic_blocks(problem, plan_step, current, accepted_steps, fork),
                      answer=current_answer, fork=fork, objections=[],
                      prior_objections=list(objections))
        if critic["decision"] == "cannot_decide":
            return semantic_finish("step_unresolved", critic["missing_derivation"])

        new_items = []
        for item in critic["objections"]:
            item = deepcopy(item)
            item["_source_call"] = critic_id
            item["_source_endpoint"] = _seat(critic_slot, recipe)["endpoint"]
            new_items.append(item)
        _check_unique_ids(objections, new_items)
        minted = _mint(new_items, f"c{cycle:04d}-critic", cycle, "decomposed-critic")
        objections.extend(minted)

        returned = call("decomposed_return", _seat("return", recipe), f"c{cycle:04d}-return", cycle,
                        _decomposed_return_blocks(problem, plan_step, current, accepted_steps, minted),
                        before=current, objections=minted)
        latest_step = deepcopy(returned)
        for item in minted:
            item["return_call"] = f"c{cycle:04d}-return"
        if (returned["decision"] == "answered" and returned["result"] != current["result"]
                and returned["derivation"] == current["derivation"]):
            state["tail_edits"] += 1
            events.append({"event": "decomposed_step_tail_edit", "cycle": cycle,
                           "step": plan_step["step"],
                           "reason": "result changed while the bounded public derivation was unchanged",
                           "semantic_reading": "mechanical flag only"})
        _apply_dispositions(objections, returned["dispositions"], cycle)
        for disposition in returned["dispositions"]:
            obj = next(item for item in minted if item["id"] == disposition["id"])
            obj["check_redone"] = (
                "agrees" if disposition["redo"]["comparison"] == "supports_objection"
                else "disagrees" if disposition["redo"]["comparison"] == "opposes_objection"
                else "inconclusive") if disposition["redo"]["status"] == "redone" else "not-redone"
        return_complete = (returned["decision"] == "answered" and
                           all(item["status"] != "unresolved" and item["redo"]["status"] == "redone"
                               for item in returned["dispositions"]))
        if not return_complete:
            return semantic_finish("step_unresolved",
                                   returned["missing_derivation"] or
                                   "A tested objection remains unresolved")

        use = call("decomposed_use", _seat("use", recipe), f"c{cycle:04d}-use", cycle,
                   _decomposed_use_blocks(
                       problem, plan_step, returned, accepted_steps,
                       contract_version=cfg.get("prompt_contract")),
                   expected_step=plan_step, before=current, answer=returned, objections=[])
        for item in minted:
            item["use_call"] = f"c{cycle:04d}-use"
        if use["decision"] != "answered" or use["status"] != "agrees":
            return semantic_finish("step_unresolved", use["missing_derivation"] or (
                "Use check " + use["status"] + " with the returned step result"))

        accepted = {"step": plan_step["step"], "goal": plan_step["goal"],
                    "depends_on": list(plan_step["depends_on"]),
                    "derivation": returned["derivation"], "result": returned["result"]}
        if r3_commitment:
            accepted["commitments"] = deepcopy(returned["commitments"])
        accepted_steps.append(accepted)
        state["completed_cycles"] = cycle
        events.append({"event": "decomposed_step_accepted", "cycle": cycle,
                       "step": plan_step["step"], "critic": critic_id,
                       "structural_only": True})

    if len(accepted_steps) != len(plan):
        return semantic_finish(
            "step_budget", f"Accepted {len(accepted_steps)} of {len(plan)} planned steps; "
            "three one-step cycles permit no synthesis")

    synthesis_blocks = _answer_blocks(problem, relation) + [
        ("DECOMPOSITION PLAN", _json(plan))]
    if r3_commitment:
        synthesis_blocks.append(("DECLARED DECISIVE STEP", _json(decisive_step)))
    synthesis_blocks.append(("ACCEPTED STEPS", _json(accepted_steps)))
    answer = call("decomposed_synthesis", _seat("synthesis", recipe), "synthesis",
                  state["completed_cycles"], synthesis_blocks,
                  decisive_step=decisive_step, accepted_steps=list(accepted_steps))
    if cfg.get("study_profile") == config.R003_PROFILE:
        return semantic_finish("complete", "All planned steps were accepted and synthesized", answer)
    state["closing_return"] = "not-applicable"
    state["stop_reason"] = "complete"
    return _finish_decomposed(directory, cfg, state, answer, objections, events)


def execute_r002(run_dir, *, scripted=None, after_call=None, checker_runner=None,
                 tokenizer_counter=None, before_call=None) -> dict:
    directory = Path(run_dir)
    with run_lock(directory):
        try:
            cfg, recipe, problem, relation, fork, coding, endpoints = _validate_run(directory)
            if (directory / "state.json").exists():
                prior = get(directory / "state.json")
                if prior.get("stop_reason") != "pending":
                    return prior
            state, events, objections = _state(cfg["condition"]), [], []
            contracts = ContractSet(directory / "contracts")
            adapter = Adapter(cfg["mode"], {"data": endpoints})
            relation_ids = [item["relation_id"] for item in relation["relations"]]

            def call(role, seat, call_id, cycle, blocks, **context):
                default_ceiling = 32768 if seat["thinking"] == "native" else 16384
                critic_ceiling = (role == "decomposed_critic" or (
                    recipe is not None and recipe.get("amendment") in {"R3-A1", "R3-A2"}
                    and role in {"prose_critic", "tested_critic"}))
                max_tokens = (recipe.get("ceilings", {}).get("critic_completion_tokens", default_ceiling)
                              if recipe is not None and critic_ceiling else default_ceiling)
                repair_budget = (recipe.get("attempt_policy", {}).get("schema_repairs", 0)
                                 if recipe is not None and (
                                     recipe.get("condition") == "LOOP-DECOMPOSED"
                                     or cfg.get("study_profile") == config.R003_PROFILE) else 0)
                parsed = _call(directory, adapter, cfg, contracts, role=role, seat=seat,
                               call_id=call_id, cycle=cycle, blocks=blocks,
                                parse_context={"relation": relation,
                                               "study_profile": cfg.get("study_profile"), **context},
                                scripted=scripted,
                                after_call=after_call, before_call=before_call,
                               tokenizer_counter=tokenizer_counter, max_tokens=max_tokens,
                               schema_repair_budget=repair_budget)
                if parsed.get("decision") == "cannot_decide":
                    state["cannot_decide_responses"] += 1
                return parsed

            if recipe is None:
                answer = call("answer", _seat("initial", None), "initial", 0,
                              _answer_blocks(problem, relation))
                state.update(stop_reason="complete", answer=answer)
                _reports(directory, cfg, state, answer, objections, events)
                return state

            if recipe["condition"] == "LOOP-DECOMPOSED":
                answer = None
                return _execute_decomposed(directory, cfg, recipe, problem, relation, fork,
                                           state, events, objections, call)

            answer = call("answer", _seat("initial", recipe), "initial", 0,
                          _answer_blocks(problem, relation))
            initial = deepcopy(answer)
            prior_answers = [deepcopy(answer)]
            stopped_early = False
            for cycle in range(1, cfg["cycles"] + 1):
                open_before = [obj for obj in objections if obj["status"] == "unresolved"]
                switch = False
                if (cfg.get("study_profile") != config.R003_PROFILE
                        and cycle == 3 and len(prior_answers) >= 3):
                    stall = stall_switch_due(prior_answers[0], prior_answers[1], prior_answers[2],
                                             open_before, relation_ids)
                    switch = stall is True
                    if stall is None and open_before:
                        events.append({"event": "stall_unknown", "cycle": 3,
                                       "open_ids": [obj["id"] for obj in open_before],
                                       "reason": "required canonical relation map missing or unparseable"})
                    if switch:
                        selected = sorted(open_before, key=lambda obj: (obj["fork"]["step_index"], obj["id"]))[0]
                        event = {"event": "stall switch", "cycle": 3,
                                 "old_instrument": recipe["seats"]["signal_a"]["role"],
                                 "new_instrument": "blind_coding_solve" if recipe["condition"] not in {"LOOP-RECODED", "LOOP-CARRIER"} else "tested_critic",
                                 "open_ids": [obj["id"] for obj in open_before], "selected_id": selected["id"],
                                 "selected_fork": selected["fork"],
                                 "trigger_hashes": [sha(_json(_claim_map(item["claims"]))) for item in prior_answers[:3]],
                                 "check_outcome": "pending-return-redo" if selected.get("check") else "absent"}
                        events.append(event)
                        state["stall_switches"] += 1
                selected_objection = selected if switch else None
                signal_items = []
                new_items = []
                if recipe["condition"] == "NATIVE-MATCH":
                    for slot in ("signal_a", "signal_b"):
                        result = call("native_match_note", _seat(slot, recipe), f"c{cycle:04d}-{slot.replace('_','-')}", cycle,
                                      _answer_blocks(problem, relation), objections=[], before=answer)
                        signal_items.append(result)
                elif (recipe["condition"] in {"LOOP-RECODED", "LOOP-CARRIER"} and not switch) or (
                        recipe["condition"] in {"LOOP-CROSS", "LOOP-CROSS-MATCH", "LOOP-TESTED", "LOOP-CHECKER"} and switch):
                    if coding is None:
                        raise ReasonFailure("CONFIG_ERROR", "Coding manifest required by recoding signal")
                    if switch and recipe["condition"] not in {"LOOP-RECODED", "LOOP-CARRIER"}:
                        first_key, second_key = "recoded_problem_path", "carrier_problem_path"
                    else:
                        first_key = "problem_path"
                        second_key = "carrier_problem_path" if recipe["condition"] == "LOOP-CARRIER" else "recoded_problem_path"
                    canonical = read(directory / "coded" / (first_key + ".txt"))
                    second_text = read(directory / "coded" / (second_key + ".txt"))
                    ids = (f"{cfg['problem_id']}-" + ("canonical" if first_key == "problem_path" else "recoded"),
                           f"{cfg['problem_id']}-" + ("carrier" if "carrier" in second_key else "recoded"))
                    a = call("blind_coding_solve", {**_seat("signal_a", recipe), "endpoint": "deepseek-flash"},
                             f"c{cycle:04d}-signal-a", cycle, _coding_blocks(canonical, relation, fork, coding, ids[0]),
                             coding_id=ids[0], objections=[])
                    b = call("blind_coding_solve", {**_seat("signal_b", recipe), "endpoint": "deepseek-flash"},
                             f"c{cycle:04d}-signal-b", cycle, _coding_blocks(second_text, relation, fork, coding, ids[1]),
                             coding_id=ids[1], objections=[])
                    signal_items = [a, b]
                    new_items = construct_recoding_objections(
                        a, b, answer, fork, prefix=f"c{cycle:04d}-coding",
                        map_identity=_json(coding.get("inverse_output_map", {})))
                    for item in new_items:
                        item["_source_call"] = f"c{cycle:04d}-coding-host"
                        item["_source_endpoint"] = "host recoding comparison"
                else:
                    tested = recipe["condition"] in {"LOOP-TESTED", "LOOP-CHECKER"} or switch
                    role = "tested_critic" if tested else "prose_critic"
                    for slot in ("signal_a", "signal_b"):
                        seat = _seat(slot, recipe)
                        if switch:
                            seat = {**seat, "endpoint": "ollama/qwen3.5-397b.native" if slot == "signal_a" else "ollama/glm-5.3.native"}
                        delivered = [selected_objection] if switch else list(objections)
                        call_id = f"c{cycle:04d}-{slot.replace('_','-')}"
                        result = call(role, seat, call_id, cycle,
                                      _critic_blocks(problem, answer, delivered, relation, fork),
                                      answer=answer, fork=fork, objections=delivered)
                        signal_items.append(result)
                        for item in result["objections"]:
                            item = deepcopy(item)
                            item["_source_call"] = call_id
                            item["_source_endpoint"] = seat["endpoint"]
                            new_items.append(item)
                _check_unique_ids(objections, new_items)
                minted = _mint(new_items, f"c{cycle:04d}-signal", cycle, "signals")
                objections.extend(minted)
                active = list(objections)
                if recipe["condition"] == "NATIVE-MATCH":
                    synthesized = call("native_match_synthesis", _seat("return", recipe), f"c{cycle:04d}-return", cycle,
                                       _answer_blocks(problem, relation) + [("INDEPENDENT NOTES", _json(signal_items)),
                                       ("PRIOR ANSWER", _answer_text(answer))], objections=[], before=answer)
                    answer = {"decision": synthesized["decision"], "answer": synthesized["answer"],
                              "missing_derivation": synthesized["missing_derivation"], "claims": [], "derivation_steps": []}
                    call("native_match_note", _seat("use", recipe), f"c{cycle:04d}-use", cycle,
                         _answer_blocks(problem, relation) + [("SYNTHESIS", _json(synthesized))], objections=[], before=answer)
                else:
                    return_role = "prose_return" if recipe["seats"]["return"]["role"].startswith("prose") else "tested_return"
                    before_answer = deepcopy(answer)
                    answer = call(return_role, _seat("return", recipe), f"c{cycle:04d}-return", cycle,
                                  _return_blocks(problem, before_answer, active, relation, fork, signal_items),
                                  before=before_answer, objections=active)
                    if any(detect_tail_edit(before_answer, answer, disposition)
                           for disposition in answer["dispositions"]):
                        state["tail_edits"] += 1
                    for disposition in answer["dispositions"]:
                        obj = next(item for item in active if item["id"] == disposition["id"])
                        if disposition.get("redo"):
                            obj["check_redone"] = ("agrees" if disposition["redo"]["comparison"] == "supports_objection"
                                                   else "disagrees" if disposition["redo"]["comparison"] == "opposes_objection"
                                                   else "inconclusive") if disposition["redo"]["status"] == "redone" else "not-redone"
                    _apply_dispositions(objections, answer["dispositions"], cycle)
                    _write_episode_records(directory, cfg, objections)
                    use = call("propagation_use", _seat("use", recipe), f"c{cycle:04d}-use", cycle,
                               _answer_blocks(problem, relation) + [("BEFORE ANSWER", _answer_text(before_answer)),
                               ("AFTER ANSWER", _answer_text(answer)),
                               ("PUBLIC TASK MODE", _json({"candidate_id": cfg["problem_id"],
                                  "checker_eligible": bool(coding and coding.get("checker_eligible")),
                                  "oracle_kind": coding.get("oracle_kind") if coding else "unknown"}))],
                                before=before_answer, answer=answer,
                                objections=[], checker_eligible=bool(coding and coding.get("checker_eligible")),
                                fork=fork, prior_objections=list(objections))
                    for item in use["objections"]:
                        item["_source_call"] = f"c{cycle:04d}-use"
                        item["_source_endpoint"] = _seat("use", recipe)["endpoint"]
                    use_minted = _mint(use["objections"], f"c{cycle:04d}-use", cycle, "use")
                    _check_unique_ids(objections, use_minted)
                    objections.extend(use_minted)
                    proposal = use.get("checker")
                    if recipe["condition"] == "LOOP-CHECKER" and proposal is not None:
                        policy = get(directory / "checker-policy.json")
                        evidence_dir = directory / "checker" / f"c{cycle:04d}"
                        proposal_bytes = (_json(proposal) + "\n").encode("utf-8")
                        execution_path = evidence_dir / "execution.json"
                        if execution_path.exists():
                            execution = get(execution_path)
                        else:
                            if checker_runner is None:
                                from .checker import CheckerRunner
                                checker_runner = CheckerRunner(mode=cfg["mode"])
                            execution = checker_runner.run(proposal_bytes, policy, evidence_dir)
                            evidence_dir.mkdir(parents=True, exist_ok=True)
                            runner_result = evidence_dir / "runner-result.json"
                            if not runner_result.exists():
                                put(runner_result, execution)
                            if execution_path.exists():
                                if get(execution_path) != execution:
                                    raise ReasonFailure("RUN_INTEGRITY_ERROR", "Checker returned bytes differ from its saved execution")
                            else:
                                put(execution_path, execution)
                        contracts.validate("checker-execution.schema.json", execution)
                        bind_checker_execution(execution, proposal_bytes, policy, proposal)
                        state["checker_runs"] += 1
                        objection = construct_checker_objection(execution, proposal, answer, fork,
                                                                 prefix=f"c{cycle:04d}-checker")
                        if objection is not None:
                            objection["_source_call"] = f"c{cycle:04d}-checker-host"
                            objection["_source_endpoint"] = "host checker"
                            host = _mint([objection], f"c{cycle:04d}-checker", cycle, "host-checker")
                            _check_unique_ids(objections, host)
                            host[0]["host_execution"] = str(evidence_dir)
                            objections.extend(host)
                    _write_episode_records(directory, cfg, objections)
                state["completed_cycles"] = cycle
                prior_answers.append(deepcopy(answer))
                open_after = [obj for obj in objections if obj["status"] == "unresolved"]
                if not minted and not open_after and recipe["condition"] != "NATIVE-MATCH":
                    stopped_early = True
                    break

            active = list(objections)
            if recipe["condition"] == "NATIVE-MATCH":
                closing = call("native_match_synthesis", _seat("return", recipe), "closing-return",
                               state["completed_cycles"], _answer_blocks(problem, relation) + [("PRIOR ANSWER", _answer_text(answer))],
                               objections=[], before=answer)
                answer = {"decision": closing["decision"], "answer": closing["answer"],
                          "missing_derivation": closing["missing_derivation"], "claims": [], "derivation_steps": []}
            else:
                return_role = "prose_return" if recipe["seats"]["return"]["role"].startswith("prose") else "tested_return"
                before_answer = deepcopy(answer)
                answer = call(return_role, _seat("return", recipe), "closing-return", state["completed_cycles"],
                              _return_blocks(problem, before_answer, active, relation, fork),
                              before=before_answer, objections=active)
                if any(detect_tail_edit(before_answer, answer, disposition)
                       for disposition in answer["dispositions"]):
                    state["tail_edits"] += 1
                for disposition in answer["dispositions"]:
                    obj = next(item for item in active if item["id"] == disposition["id"])
                    if disposition.get("redo"):
                        obj["check_redone"] = ("agrees" if disposition["redo"]["comparison"] == "supports_objection"
                                               else "disagrees" if disposition["redo"]["comparison"] == "opposes_objection"
                                               else "inconclusive") if disposition["redo"]["status"] == "redone" else "not-redone"
                _apply_dispositions(objections, answer["dispositions"], state["completed_cycles"], "closing_return")
                _write_episode_records(directory, cfg, objections)
            state["closing_return"] = "complete"
            state["stop_reason"] = "no_new_objections" if stopped_early else "cycle_budget"
            state["answer"], state["events"] = answer, events
            _write_episode_records(directory, cfg, objections)
            _reports(directory, cfg, state, answer, objections, events)
            return state
        except ReasonFailure as exc:
            try:
                cfg = get(directory / "config.json")
                state = locals().get("state", _state(cfg.get("condition", "UNKNOWN")))
                state["stop_reason"] = exc.code
                state["detail"] = exc.detail
                state["events"] = locals().get("events", [])
                state["answer"] = locals().get("answer")
                _reports(directory, cfg, state, state.get("answer"), locals().get("objections", []), state["events"])
                return state
            except Exception:
                raise exc


def status_r002(run_dir) -> dict:
    directory = Path(run_dir)
    return get(directory / "state.json") if (directory / "state.json").exists() else {
        "schema": R002_STATE_SCHEMA, "stop_reason": "not_started", "calls": 0, "attempts": 0}
