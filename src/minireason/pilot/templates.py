"""Immutable catalogue data and local schema validation for the Flash pilot."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

CATALOGUE_VERSION = "flash-pilot-v1"
TEMPLATE_IDS = (
    "direct_answer",
    "evidence_read",
    "engineer_patch",
    "critic_return",
    "decompose_synthesize",
)

_STRING_ARRAY = {"type": "array", "items": {"type": "string"}}
_DOCUMENT_ARRAY = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {"id": {"type": "string"}, "text": {"type": "string"}},
        "required": ["id", "text"],
        "additionalProperties": False,
    },
}
COMMON_INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "task": {"type": "string"},
        "premises": deepcopy(_STRING_ARRAY),
        "documents": deepcopy(_DOCUMENT_ARRAY),
        "candidate": {"type": "string"},
        "allowed_files": deepcopy(_STRING_ARRAY),
        "answer_shape": {"type": "string"},
        "requested_claims": deepcopy(_STRING_ARRAY),
        "behavior_contract": {"type": "string"},
        "test_commands": deepcopy(_STRING_ARRAY),
        "objections": deepcopy(_STRING_ARRAY),
        "protected_obligations": deepcopy(_STRING_ARRAY),
        "decisive_question": {"type": "string"},
    },
    "required": [
        "task", "premises", "documents", "candidate", "allowed_files",
        "answer_shape", "requested_claims", "behavior_contract", "test_commands",
        "objections", "protected_obligations", "decisive_question",
    ],
    "additionalProperties": False,
}
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["complete", "partial", "cannot_decide", "failed"]},
        "answer": {"type": "string"},
        "source_refs": deepcopy(_STRING_ARRAY),
        "unresolved": deepcopy(_STRING_ARRAY),
        "verification_refs": deepcopy(_STRING_ARRAY),
    },
    "required": ["status", "answer", "source_refs", "unresolved", "verification_refs"],
    "additionalProperties": False,
}


def _extended_output(extra: Mapping[str, Any]) -> dict[str, Any]:
    schema = deepcopy(OUTPUT_SCHEMA)
    schema["properties"].update(deepcopy(dict(extra)))
    schema["required"].extend(extra)
    return schema


EVIDENCE_SCHEMA = _extended_output({
    "quotes": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "claim": {"type": "string"},
                "source_id": {"type": "string"},
                "locator": {"type": "string"},
                "quote": {"type": "string"},
            },
            "required": ["claim", "source_id", "locator", "quote"],
            "additionalProperties": False,
        },
    },
    "contradictions": deepcopy(_STRING_ARRAY),
    "not_found": deepcopy(_STRING_ARRAY),
})
ENGINEER_SCHEMA = _extended_output({
    "patches": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {"path": {"type": "string"}, "patch": {"type": "string"}},
            "required": ["path", "patch"],
            "additionalProperties": False,
        },
    },
    "rationale": {"type": "string"},
    "test_claims": deepcopy(_STRING_ARRAY),
})
CRITIC_SCHEMA = _extended_output({
    "objections": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "target": {"type": "string"},
                "grounds": {"type": "string"},
            },
            "required": ["id", "target", "grounds"],
            "additionalProperties": False,
        },
    },
    "dispositions": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "status": {"type": "string", "enum": ["taken-up", "rejected-with-reason", "unresolved"]},
                "reason": {"type": "string"},
            },
            "required": ["id", "status", "reason"],
            "additionalProperties": False,
        },
    },
    "revision": {"type": "string"},
    "dependent_use": {"type": "string"},
})
DECOMPOSE_SCHEMA = _extended_output({
    "steps": deepcopy(_STRING_ARRAY),
    "dependencies": deepcopy(_STRING_ARRAY),
    "synthesis": {"type": "string"},
})


def validate(value: Any, schema: Mapping[str, Any], path: str = "$") -> None:
    """Validate the JSON-Schema subset used by this package, raising ValueError."""
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError(f"{path}: expected one of {schema['enum']!r}")
    expected = schema.get("type")
    if expected == "object":
        if not isinstance(value, dict):
            raise ValueError(f"{path}: expected object")
        properties = schema.get("properties", {})
        missing = [name for name in schema.get("required", []) if name not in value]
        if missing:
            raise ValueError(f"{path}: missing required fields {missing!r}")
        if schema.get("additionalProperties") is False:
            extra = sorted(set(value) - set(properties))
            if extra:
                raise ValueError(f"{path}: unexpected fields {extra!r}")
        for name, item in value.items():
            if name in properties:
                validate(item, properties[name], f"{path}.{name}")
    elif expected == "array":
        if not isinstance(value, list):
            raise ValueError(f"{path}: expected array")
        if len(value) < schema.get("minItems", 0):
            raise ValueError(f"{path}: too few items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            raise ValueError(f"{path}: too many items")
        for index, item in enumerate(value):
            validate(item, schema.get("items", {}), f"{path}[{index}]")
    elif expected == "string":
        if not isinstance(value, str):
            raise ValueError(f"{path}: expected string")
        if len(value) < schema.get("minLength", 0):
            raise ValueError(f"{path}: string is too short")
    elif expected == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"{path}: expected integer")
        if "minimum" in schema and value < schema["minimum"]:
            raise ValueError(f"{path}: below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            raise ValueError(f"{path}: above maximum")
    elif expected == "boolean" and not isinstance(value, bool):
        raise ValueError(f"{path}: expected boolean")
    elif expected is not None and expected not in {"object", "array", "string", "integer", "boolean"}:
        raise ValueError(f"{path}: unsupported schema type {expected!r}")


def normalize_inputs(task: str, inputs: Mapping[str, Any] | None = None) -> dict[str, Any]:
    if not isinstance(task, str):
        raise ValueError("task must be a string")
    source = dict(inputs or {})
    defaults: dict[str, Any] = {
        "task": task,
        "premises": [],
        "documents": [],
        "candidate": "",
        "allowed_files": [],
        "answer_shape": "plain answer",
        "requested_claims": [],
        "behavior_contract": "",
        "test_commands": [],
        "objections": [],
        "protected_obligations": [],
        "decisive_question": task,
    }
    unknown = sorted(set(source) - set(defaults))
    if unknown:
        raise ValueError(f"inputs contain unknown fields: {unknown!r}")
    defaults.update(source)
    validate(defaults, COMMON_INPUT_SCHEMA)
    return defaults

TEMPLATES: dict[str, dict[str, Any]] = {
    "direct_answer": {
        "id": "direct_answer",
        "version": CATALOGUE_VERSION,
        "purpose": "Answer a short, self-contained closed task under an explicit answer shape.",
        "required_inputs": ["task", "answer_shape"],
        "input_schema": deepcopy(COMMON_INPUT_SCHEMA),
        "output_schema": deepcopy(OUTPUT_SCHEMA),
        "seats": [{"role": "answer", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 8192}],
        "ceilings": {"max_attempts": 2, "max_children": 0, "max_depth": 0},
        "thinking": "off",
        "repair_rule": "Allow one schema-only repair; correctness still requires an independent applicable check.",
        "failure_rules": ["Route substantial derivations elsewhere", "Do not treat valid JSON as correct arithmetic"],
        "cost_envelope": {"flash_attempt_units_max": 2, "conditional_on": "host-verified prompt tokens <=64000", "price_promise_without_bound": False},
        "evidence_refs": ["CAPABILITY.md#structured-output-reliability", "ROUTER-DESIGN.md#router-data", "R001 BARE/NATIVE", "R003 conjecture"],
    },
    "evidence_read": {
        "id": "evidence_read",
        "version": CATALOGUE_VERSION,
        "purpose": "Read sealed supplied material and locate exact support, contradictions, or absence.",
        "required_inputs": ["task", "documents", "requested_claims"],
        "input_schema": deepcopy(COMMON_INPUT_SCHEMA),
        "output_schema": deepcopy(EVIDENCE_SCHEMA),
        "seats": [{"role": "reader", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 8192}],
        "ceilings": {"max_attempts": 2, "max_children": 0, "max_depth": 0},
        "thinking": "off",
        "repair_rule": "One repair receives the exact sealed source and the failing locator; preserve the original output.",
        "failure_rules": ["Host verifies every quote and source ID", "Report absent support as NOT FOUND"],
        "cost_envelope": {"flash_attempt_units_max": 2, "conditional_on": "host-verified prompt tokens <=64000", "price_promise_without_bound": False},
        "evidence_refs": ["R003 propagation-use quote failures", "Dedicated reader competence NOT FOUND", "ROUTER-DESIGN.md#router-data"],
    },
    "engineer_patch": {
        "id": "engineer_patch",
        "version": CATALOGUE_VERSION,
        "purpose": "Propose a bounded source change and test claims inside a host-enforced allowlist.",
        "required_inputs": ["task", "allowed_files", "documents", "behavior_contract", "test_commands"],
        "input_schema": deepcopy(COMMON_INPUT_SCHEMA),
        "output_schema": deepcopy(ENGINEER_SCHEMA),
        "seats": [
            {"role": "proposer", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 8192},
            {"role": "critic", "model": "host-selected", "lineage": "different-from-proposer", "thinking": "off", "max_completion_tokens": 8192},
            {"role": "return", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 8192},
        ],
        "ceilings": {"max_attempts": 6, "max_children": 3, "max_depth": 2},
        "thinking": "off",
        "repair_rule": "Reject files and commands outside allowlists; one schema repair per seat does not establish execution success.",
        "failure_rules": ["Critic does not execute code", "Only host-run checks can support test claims"],
        "cost_envelope": {"flash_attempt_units_max": 4, "other_lineage_attempts_max": 2, "conditional_on": "provider-specific current prices and certified input count", "price_promise_without_bound": False},
        "evidence_refs": ["Reason CLI composition/checker mechanism", "Live Flash repository engineering success NOT FOUND", "ROUTER-DESIGN.md#router-data"],
    },
    "critic_return": {
        "id": "critic_return",
        "version": CATALOGUE_VERSION,
        "purpose": "Challenge a supplied candidate, disposition stable objections, revise it, and test dependent use.",
        "required_inputs": ["task", "candidate", "premises", "objections", "protected_obligations"],
        "input_schema": deepcopy(COMMON_INPUT_SCHEMA),
        "output_schema": deepcopy(CRITIC_SCHEMA),
        "seats": [
            {"role": "critic-1", "model": "host-selected", "lineage": "different-from-proposer", "thinking": "off", "max_completion_tokens": 8192},
            {"role": "critic-2", "model": "host-selected", "lineage": "different-from-proposer", "thinking": "off", "max_completion_tokens": 8192},
            {"role": "return", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 8192},
            {"role": "use", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 8192},
        ],
        "ceilings": {"max_attempts": 8, "max_children": 3, "max_depth": 2},
        "thinking": "off",
        "repair_rule": "Reject unknown or duplicate objection IDs; one schema repair per seat preserves rejected public text.",
        "failure_rules": ["An empty objection list is not proof", "Label reduced independence if only one critic lineage is available"],
        "cost_envelope": {"flash_attempt_units_max": 4, "other_lineage_attempts_max": 4, "conditional_on": "provider-specific current prices and certified input count", "price_promise_without_bound": False},
        "evidence_refs": ["R001 SINGLE/CROSS", "R002 return/use", "R003 return/use", "ROUTER-DESIGN.md#router-data"],
    },
    "decompose_synthesize": {
        "id": "decompose_synthesize",
        "version": CATALOGUE_VERSION,
        "purpose": "Resolve separable dependencies in at most three executable steps and synthesize accepted results.",
        "required_inputs": ["task", "decisive_question"],
        "input_schema": deepcopy(COMMON_INPUT_SCHEMA),
        "output_schema": deepcopy(DECOMPOSE_SCHEMA),
        "seats": [
            {"role": "plan", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 4096},
            {"role": "step", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 8192, "maximum_occurrences": 3},
            {"role": "critic", "model": "host-selected", "lineage": "different-from-proposer", "thinking": "off", "max_completion_tokens": 8192},
            {"role": "synthesis", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 8192},
        ],
        "ceilings": {"max_attempts": 12, "max_children": 3, "max_depth": 2},
        "thinking": "off",
        "repair_rule": "Reject an infeasible DAG before calls; one schema repair per seat, and a failed step prevents full synthesis.",
        "failure_rules": ["Definitions alone are not completed steps", "Require decisive work inside the three-step budget", "Never synthesize across a missing dependency"],
        "cost_envelope": {"flash_attempt_units_max": 10, "other_lineage_attempts_max": 2, "conditional_on": "provider-specific current prices and certified input count", "price_promise_without_bound": False},
        "evidence_refs": ["R002 eight plans", "R003 sixteen plans", "Requested-record synthesis evidence NOT FOUND", "ROUTER-DESIGN.md#router-data"],
    },
}


def validate_inputs(template_id: str, inputs: Mapping[str, Any]) -> None:
    if template_id not in TEMPLATES:
        raise ValueError(f"unknown template_id: {template_id!r}")
    validate(inputs, COMMON_INPUT_SCHEMA)
    missing: list[str] = []
    for field in TEMPLATES[template_id]["required_inputs"]:
        value = inputs[field]
        if isinstance(value, str) and not value.strip():
            missing.append(field)
        elif isinstance(value, list) and not value:
            missing.append(field)
    if missing:
        raise ValueError(f"{template_id} requires nonempty inputs: {missing!r}")
