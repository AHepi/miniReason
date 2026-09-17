"""Immutable catalogue data and local schema validation for the Flash pilot."""

from __future__ import annotations

from copy import deepcopy
import json
from typing import Any, Mapping

from .inputs import INPUT_REF_SCHEMA

CATALOGUE_VERSION = "flash-pilot-v1/P-A4"
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


def prose_schema(kind: str, *, default: Any | None = None, nonempty: bool = False) -> dict[str, Any]:
    """Describe a delivery-tolerant prose field with one canonical host shape."""
    if kind not in {"string", "list"}:
        raise ValueError(f"unknown prose schema kind: {kind!r}")
    string_branch: dict[str, Any] = {"type": "string"}
    if nonempty:
        string_branch["minLength"] = 1
    nested = {"oneOf": [
        string_branch,
        {"type": "array"},
        {"type": "object"},
    ]}
    if kind == "string":
        schema: dict[str, Any] = deepcopy(nested)
    else:
        schema = {"oneOf": [
            {"type": "string"},
            {"type": "array", "items": deepcopy(nested)},
            {"type": "object"},
        ]}
    schema["x-pilot-prose"] = kind
    if default is not None:
        schema["default"] = deepcopy(default)
    return schema


_PROSE_STRING = prose_schema("string")
_PROSE_LIST = prose_schema("list", default=[])
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
SPAWN_INPUT_SCHEMA = {
    "oneOf": [deepcopy(COMMON_INPUT_SCHEMA), deepcopy(INPUT_REF_SCHEMA)],
}

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["complete", "partial", "cannot_decide", "failed"]},
        "answer": deepcopy(_PROSE_STRING),
        "source_refs": {**deepcopy(_STRING_ARRAY), "default": []},
        "unresolved": deepcopy(_PROSE_LIST),
        "verification_refs": {**deepcopy(_STRING_ARRAY), "default": []},
    },
    "required": ["status", "answer"],
    "additionalProperties": False,
}


def _extended_output(extra: Mapping[str, Any], *, required: tuple[str, ...] = ()) -> dict[str, Any]:
    schema = deepcopy(OUTPUT_SCHEMA)
    schema["properties"].update(deepcopy(dict(extra)))
    schema["required"].extend(required)
    return schema


EVIDENCE_SCHEMA = _extended_output({
    "quotes": {
        "type": "array",
        "default": [],
        "items": {
            "type": "object",
            "properties": {
                "claim": prose_schema("string", default=""),
                "source_id": {"type": "string"},
                "locator": prose_schema("string", default=""),
                "quote": {"type": "string"},
            },
            "required": ["source_id", "quote"],
            "additionalProperties": False,
        },
    },
    "contradictions": deepcopy(_PROSE_LIST),
    "not_found": deepcopy(_PROSE_LIST),
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
    "rationale": prose_schema("string", default=""),
    "test_claims": deepcopy(_PROSE_LIST),
}, required=("patches",))
CRITIC_SCHEMA = _extended_output({
    "objections": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "target": {"type": "string"},
                "grounds": deepcopy(_PROSE_STRING),
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
                "reason": deepcopy(_PROSE_STRING),
            },
            "required": ["id", "status", "reason"],
            "additionalProperties": False,
        },
    },
    "revision": deepcopy(_PROSE_STRING),
    "dependent_use": prose_schema("string", default=""),
}, required=("objections", "dispositions", "revision"))
DECOMPOSE_SCHEMA = _extended_output({
    "steps": deepcopy(_PROSE_LIST),
    "dependencies": deepcopy(_PROSE_LIST),
    "synthesis": deepcopy(_PROSE_STRING),
}, required=("synthesis",))


def validate(value: Any, schema: Mapping[str, Any], path: str = "$") -> None:
    """Validate the JSON-Schema subset used by this package, raising ValueError."""
    if "oneOf" in schema:
        matches = 0
        errors = []
        for candidate in schema["oneOf"]:
            try:
                validate(value, candidate, path)
                matches += 1
            except ValueError as error:
                errors.append(str(error))
        if matches != 1:
            raise ValueError(f"{path}: expected exactly one allowed input shape; matches={matches}; errors={errors!r}")
        return
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


def _prose_text(value: Any, path: str) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        if all(isinstance(item, str) for item in value):
            return "\n".join(value)
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    raise ValueError(f"{path}: prose must be a string, list, or object")


def _normalize_node(value: Any, schema: Mapping[str, Any], path: str) -> Any:
    prose_kind = schema.get("x-pilot-prose")
    if prose_kind == "string":
        return _prose_text(value, path)
    if prose_kind == "list":
        if isinstance(value, str):
            return [] if not value else [value]
        if isinstance(value, dict):
            return [_prose_text(value, path)]
        if isinstance(value, list):
            return [item if isinstance(item, str) else _prose_text(item, f"{path}[{index}]")
                    for index, item in enumerate(value)]
        raise ValueError(f"{path}: prose list must be a string, list, or object")
    if "oneOf" in schema:
        matches = []
        for candidate in schema["oneOf"]:
            try:
                normalized = _normalize_node(value, candidate, path)
                validate(normalized, candidate, path)
                matches.append(normalized)
            except (TypeError, ValueError):
                continue
        return matches[0] if len(matches) == 1 else deepcopy(value)
    if schema.get("type") == "object" and isinstance(value, dict):
        result = deepcopy(value)
        properties = schema.get("properties", {})
        for name, child_schema in properties.items():
            child_path = f"{path}.{name}"
            if name in result:
                result[name] = _normalize_node(result[name], child_schema, child_path)
            elif "default" in child_schema:
                result[name] = deepcopy(child_schema["default"])
        return result
    if schema.get("type") == "array" and isinstance(value, list):
        child_schema = schema.get("items", {})
        return [_normalize_node(item, child_schema, f"{path}[{index}]")
                for index, item in enumerate(value)]
    return deepcopy(value)


def normalize_delivery(value: Any, schema: Mapping[str, Any]) -> dict[str, Any]:
    """Canonicalize only declared prose/default variations before validation.

    Exact identifiers, references, quotes, paths, ranges, enums, and unknown
    fields are copied without alteration so existing host custody checks remain
    authoritative. The caller retains the original provider bytes separately.
    """
    normalized = _normalize_node(value, schema, "$")
    if not isinstance(normalized, dict):
        raise ValueError("$: provider public content must be a JSON object")
    return normalized


def _task_context(packet: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any] | None]:
    candidates = [packet.get("resolved_inputs"), packet.get("inputs")]
    task_packet = packet.get("task")
    if isinstance(task_packet, dict):
        candidates.extend([task_packet, task_packet.get("inputs")])
    inputs = next((dict(item) for item in candidates
                   if isinstance(item, dict) and isinstance(item.get("task"), str)), {})
    input_ref = next((dict(item) for item in candidates
                      if isinstance(item, dict) and "unit_id" in item), None)
    return inputs, input_ref


def _utf8_prefix(text: str, limit: int = 96) -> str:
    raw = text.encode("utf-8")[:limit]
    while raw:
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            raw = raw[:-1]
    return ""


def _example_context(packet: Mapping[str, Any]) -> dict[str, Any]:
    inputs, input_ref = _task_context(packet)
    task_value = packet.get("task")
    task_packet = task_value if isinstance(task_value, dict) else {}
    task = (inputs.get("task") or task_packet.get("task")
            or (task_value if isinstance(task_value, str) else None)
            or packet.get("original_task") or "the supplied task")
    documents = list(inputs.get("documents", [])) if isinstance(inputs.get("documents", []), list) else []
    reads = packet.get("resolved_source_reads", [])
    if not documents and isinstance(reads, list):
        for item in reads:
            if not isinstance(item, dict):
                continue
            receipt = item.get("receipt", {}) if isinstance(item.get("receipt", {}), dict) else {}
            source_id = receipt.get("source_ref") or item.get("source_ref") or item.get("source_id") or item.get("unit_id")
            text = item.get("text") or item.get("content")
            if isinstance(source_id, str) and isinstance(text, str):
                documents.append({"id": source_id, "text": text})
    source = documents[0] if documents else None
    quote = _utf8_prefix(source["text"]) if source and isinstance(source.get("text"), str) else ""
    refs = []
    for item in packet.get("accepted_results", []) if isinstance(packet.get("accepted_results", []), list) else []:
        if isinstance(item, dict) and isinstance(item.get("result_ref"), str):
            refs.append(item["result_ref"])
    bounded_input_ref = deepcopy(input_ref)
    if bounded_input_ref is not None and isinstance(packet.get("resolved_inputs"), dict):
        bounded_input_ref["overrides"] = {
            "task": f"Resolve one bounded decisive part of: {_utf8_prefix(str(task), 160)}"
        }
    verification = packet.get("verification") if isinstance(packet.get("verification"), dict) else {}
    return {"inputs": inputs, "input_ref": input_ref, "bounded_input_ref": bounded_input_ref,
            "task": str(task), "source": source, "quote": quote, "result_refs": refs,
            "template_id": packet.get("template_id"),
            "verification_ref": verification.get("verification_ref"),
            "stop_rule": packet.get("stop_rule")}


def _example_value(schema: Mapping[str, Any], name: str, context: Mapping[str, Any]) -> Any:
    if name == "inputs" and context.get("input_ref") is not None:
        candidate = deepcopy(context.get("bounded_input_ref") or context["input_ref"])
        try:
            validate(candidate, schema)
            return candidate
        except ValueError:
            pass
    if "enum" in schema:
        if name == "template_id" and context.get("template_id") in schema["enum"]:
            return context["template_id"]
        if name == "status" and "partial" in schema["enum"]:
            return "partial"
        if name == "decision" and "stop" in schema["enum"]:
            return "stop"
        return deepcopy(schema["enum"][0])
    prose_kind = schema.get("x-pilot-prose")
    task_excerpt = _utf8_prefix(context["task"], 120)
    if prose_kind == "list":
        if name in {"steps", "dependencies"}:
            return [f"Address the supplied task: {task_excerpt}"]
        return []
    if prose_kind == "string":
        if name == "locator":
            quote = context.get("quote", "")
            return f"bytes:0:{len(quote.encode('utf-8'))}" if quote else ""
        if name == "claim" and context.get("source"):
            return f"Exact opening bytes from {context['source']['id']}."
        if name in {"revision", "synthesis", "answer", "dependent_use"}:
            return f"Provisional response for the supplied task: {task_excerpt}"
        if name == "what_changes_next":
            return ""
        if name == "stop_rule":
            return context.get("stop_rule") or "Stop when the supplied task is verified or a recorded guard stops the run."
        if name == "reason" and context.get("verification_ref"):
            return f"{context['verification_ref']}: the recorded verification determines whether another changed pass is useful."
        return f"Reason grounded in the supplied task: {task_excerpt}"
    if "oneOf" in schema:
        for candidate in schema["oneOf"]:
            value = _example_value(candidate, name, context)
            try:
                validate(value, candidate)
                return value
            except ValueError:
                continue
    expected = schema.get("type")
    if expected == "object":
        return {key: _example_value(child, key, context)
                for key, child in schema.get("properties", {}).items()}
    if expected == "array":
        if name in {"source_refs"}:
            return [context["source"]["id"]] if context.get("source") else []
        if name in {"verification_refs", "unresolved", "contradictions", "not_found",
                    "test_claims", "depends_on", "source_reads"}:
            return []
        if name == "result_refs":
            return deepcopy(context.get("result_refs") or ["recorded-result-ref"])
        if name == "quotes":
            if not context.get("source") or not context.get("quote"):
                return []
            quote = context["quote"]
            return [{"claim": f"Exact opening bytes from {context['source']['id']}.",
                     "source_id": context["source"]["id"],
                     "locator": f"bytes:0:{len(quote.encode('utf-8'))}", "quote": quote}]
        count = max(1, schema.get("minItems", 0))
        return [_example_value(schema.get("items", {}), name.rstrip("s"), context)
                for _ in range(count)]
    if expected == "string":
        if name == "template_id" and context.get("template_id"):
            return context["template_id"]
        if name == "unit_id" and context.get("input_ref"):
            return context["input_ref"]["unit_id"]
        if name == "encoding":
            return "json"
        if name == "quote":
            return context.get("quote", "")
        if name == "source_id" and context.get("source"):
            return context["source"]["id"]
        if name == "id":
            return "step-1"
        if name == "path":
            files = context.get("inputs", {}).get("allowed_files", [])
            return files[0] if files else "allowed-file"
        return f"Supplied-task {name}: {task_excerpt}"
    if expected == "integer":
        if name == "start":
            return 0
        if name == "end" and context.get("input_ref"):
            return context["input_ref"]["end"]
        if name == "limit":
            return min(65536, context.get("input_ref", {}).get("end", 65536))
        return max(1, schema.get("minimum", 0))
    if expected == "boolean":
        return False
    return ""


def response_example(schema: Mapping[str, Any], packet: Mapping[str, Any]) -> dict[str, Any]:
    """Build a schema-valid response example from the call's supplied task units."""
    example = _example_value(schema, "$", _example_context(packet))
    normalized = normalize_delivery(example, schema)
    validate(normalized, schema)
    return normalized


def worker_response_contract(
    template_id: str,
    stage: str,
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    """Return the worker schema and a copyable task-derived response form."""
    if template_id not in TEMPLATES:
        raise ValueError(f"unknown template_id: {template_id!r}")
    schema = deepcopy(TEMPLATES[template_id]["output_schema"])
    packet = {"inputs": deepcopy(dict(inputs)), "template_id": template_id}
    example = response_example(schema, packet)
    return {
        "schema": schema,
        "response_example": example,
        "instruction": (
            f"For stage {stage}, return exactly one JSON object in response_example form. "
            "Prose may be a string or prose list; nested prose is retained as text. "
            "Copy every source_id and quote exactly. locator is only a claimed hint; "
            "the host resolves the exact quote bytes. Never invent result, verification, "
            "source, action, path, input-reference, or dependency identifiers."
        ),
    }


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
        "seats": [{"role": "answer", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 16384}],
        "ceilings": {"max_attempts": 4, "max_children": 0, "max_depth": 0},
        "thinking": "off",
        "repair_rule": "Allow up to three schema-only repairs per logical call; correctness still requires an independent applicable check.",
        "failure_rules": ["Route substantial derivations elsewhere", "Do not treat valid JSON as correct arithmetic"],
        "cost_envelope": {"flash_attempt_units_max": 4, "conditional_on": "host-verified prompt tokens <=64000", "price_promise_without_bound": False},
        "evidence_refs": ["CAPABILITY.md#structured-output-reliability", "ROUTER-DESIGN.md#router-data", "R001 BARE/NATIVE", "R003 conjecture"],
    },
    "evidence_read": {
        "id": "evidence_read",
        "version": CATALOGUE_VERSION,
        "purpose": "Read sealed supplied material and locate exact support, contradictions, or absence.",
        "required_inputs": ["task", "documents", "requested_claims"],
        "input_schema": deepcopy(COMMON_INPUT_SCHEMA),
        "output_schema": deepcopy(EVIDENCE_SCHEMA),
        "seats": [{"role": "reader", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 16384}],
        "ceilings": {"max_attempts": 4, "max_children": 0, "max_depth": 0},
        "thinking": "off",
        "repair_rule": "Up to three repairs receive the exact sealed source, rejected public bytes, and validator reason; preserve the original output.",
        "failure_rules": ["Host verifies every quote and source ID", "Report absent support as NOT FOUND"],
        "cost_envelope": {"flash_attempt_units_max": 4, "conditional_on": "host-verified prompt tokens <=64000", "price_promise_without_bound": False},
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
            {"role": "proposer", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 16384},
            {"role": "critic", "model": "host-selected", "lineage": "different-from-proposer", "thinking": "off", "max_completion_tokens": 16384},
            {"role": "return", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 16384},
        ],
        "ceilings": {"max_attempts": 12, "max_children": 3, "max_depth": 2},
        "thinking": "off",
        "repair_rule": "Reject files and commands outside allowlists; up to three schema repairs per logical call do not establish execution success.",
        "failure_rules": ["Critic does not execute code", "Only host-run checks can support test claims"],
        "cost_envelope": {"flash_attempt_units_max": 8, "other_lineage_attempts_max": 4, "conditional_on": "provider-specific current prices and certified input count", "price_promise_without_bound": False},
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
            {"role": "critic-1", "model": "host-selected", "lineage": "different-from-proposer", "thinking": "off", "max_completion_tokens": 16384},
            {"role": "critic-2", "model": "host-selected", "lineage": "different-from-proposer", "thinking": "off", "max_completion_tokens": 16384},
            {"role": "return", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 16384},
            {"role": "use", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 16384},
        ],
        "ceilings": {"max_attempts": 16, "max_children": 3, "max_depth": 2},
        "thinking": "off",
        "repair_rule": "Reject unknown or duplicate objection IDs; up to three schema repairs per logical call preserve every rejected public response.",
        "failure_rules": ["An empty objection list is not proof", "Label reduced independence if only one critic lineage is available"],
        "cost_envelope": {"flash_attempt_units_max": 8, "other_lineage_attempts_max": 8, "conditional_on": "provider-specific current prices and certified input count", "price_promise_without_bound": False},
        "evidence_refs": ["R001 SINGLE/CROSS", "R002 return/use", "R003 return/use", "ROUTER-DESIGN.md#router-data"],
    },
    "decompose_synthesize": {
        "id": "decompose_synthesize",
        "version": CATALOGUE_VERSION,
        "purpose": "Resolve separable dependencies in at most 24 executable steps per decomposition level and synthesize accepted results.",
        "required_inputs": ["task", "decisive_question"],
        "input_schema": deepcopy(COMMON_INPUT_SCHEMA),
        "output_schema": deepcopy(DECOMPOSE_SCHEMA),
        "seats": [
            {"role": "plan", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 16384},
            {"role": "step", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 16384, "maximum_occurrences": 24},
            {"role": "critic", "model": "host-selected", "lineage": "different-from-proposer", "thinking": "off", "max_completion_tokens": 16384},
            {"role": "synthesis", "model": "deepseek-flash", "lineage": "deepseek", "thinking": "off", "max_completion_tokens": 16384},
        ],
        "ceilings": {"max_attempts": 2604, "max_children": 24, "max_depth": 3, "global_budget_applies": True},
        "thinking": "off",
        "repair_rule": "Reject an infeasible DAG before calls; up to three schema repairs per logical call, and a failed step prevents full synthesis.",
        "failure_rules": ["Definitions alone are not completed steps", "Require decisive work inside the remaining global logical-call and spend budget", "Never synthesize across a missing dependency"],
        "cost_envelope": {"flash_attempt_units_max": 2504, "other_lineage_attempts_max": 100, "conditional_on": "provider-specific current prices and certified input count", "price_promise_without_bound": False},
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
