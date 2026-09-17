"""OpenAI-compatible function tool manifest for the owner-operated pilot harness."""

from __future__ import annotations

from copy import deepcopy
from itertools import combinations
from typing import Any

from .templates import SPAWN_INPUT_SCHEMA, TEMPLATE_IDS, normalize_delivery, prose_schema, validate

_TEMPLATE_ENUM = {"type": "string", "enum": list(TEMPLATE_IDS)}
_STRING_LIST = {"type": "array", "items": {"type": "string"}}

ROUTE_PARAMETERS = {
    "type": "object",
    "properties": {
        "template_id": deepcopy(_TEMPLATE_ENUM),
        "reason": prose_schema("string", nonempty=True),
    },
    "required": ["template_id", "reason"],
    "additionalProperties": False,
}
SOURCE_READ_PARAMETERS = {
    "type": "object",
    "properties": {
        "unit_id": {"type": "string", "minLength": 64, "maxLength": 64},
        "start": {"type": "integer", "minimum": 0},
        "end": {"type": "integer", "minimum": 1},
        "limit": {"type": "integer", "minimum": 1, "maximum": 65536},
    },
    "required": ["unit_id", "start", "end", "limit"],
    "additionalProperties": False,
}
SOURCE_READ_ARRAY = {
    "type": "array", "maxItems": 8, "items": deepcopy(SOURCE_READ_PARAMETERS),
}
_LEGACY_SUBTASK = {
    "type": "object",
    "properties": {"template_id": deepcopy(_TEMPLATE_ENUM), "inputs": deepcopy(SPAWN_INPUT_SCHEMA)},
    "required": ["template_id", "inputs"],
    "additionalProperties": False,
}
_SOURCE_SUBTASK = {
    "type": "object",
    "properties": {"template_id": deepcopy(_TEMPLATE_ENUM), "inputs": deepcopy(SPAWN_INPUT_SCHEMA),
                   "source_reads": deepcopy(SOURCE_READ_ARRAY)},
    "required": ["template_id", "inputs", "source_reads"],
    "additionalProperties": False,
}
SPAWN_PARAMETERS = {
    "type": "object",
    "properties": {
        "subtasks": {
            "type": "array",
            "minItems": 1,
            "maxItems": 24,
            "items": {"oneOf": [deepcopy(_LEGACY_SUBTASK), deepcopy(_SOURCE_SUBTASK)]},
        },
    },
    "required": ["subtasks"],
    "additionalProperties": False,
}
ASSEMBLE_PARAMETERS = {
    "type": "object",
    "properties": {
        "result_refs": {"type": "array", "minItems": 1, "items": {"type": "string", "minLength": 1}},
        "answer": prose_schema("string"),
        "unresolved": prose_schema("list", default=[]),
    },
    "required": ["result_refs", "answer"],
    "additionalProperties": False,
}
READ_SOURCE_PARAMETERS = deepcopy(SOURCE_READ_PARAMETERS)

VERIFY_PARAMETERS = {
    "type": "object",
    "properties": {"artifact_ref": {"type": "string", "minLength": 1}},
    "required": ["artifact_ref"],
    "additionalProperties": False,
}


CONTINUE_PARAMETERS = {
    "type": "object", "additionalProperties": False,
    "required": ["decision", "reason", "stop_rule"],
    "properties": {
        "decision": {"type": "string", "enum": ["continue", "stop"]},
        "reason": prose_schema("string", nonempty=True),
        "what_changes_next": prose_schema("string", default=""),
        "stop_rule": prose_schema("string", nonempty=True),
    },
}


LOCAL_PARAMETERS = {
    "route": ROUTE_PARAMETERS,
    "spawn": SPAWN_PARAMETERS,
    "assemble": ASSEMBLE_PARAMETERS,
    "read_source": READ_SOURCE_PARAMETERS,
    "verify": VERIFY_PARAMETERS,
    "continue_or_stop": CONTINUE_PARAMETERS,
}


def _strict_wire_schema(value: Any) -> Any:
    """Export the documented beta subset; retain stronger bounds at the host."""
    if isinstance(value, dict):
        # P-A2 references have optional overrides. Strict wire objects must
        # require every declared property; closed alternatives preserve the
        # host's exact omission semantics without admitting nullable values.
        if value.get("type") == "object":
            properties = value.get("properties", {})
            required = value.get("required", [])
            if not properties:
                return {"type": "object", "properties": {}, "required": [], "additionalProperties": False}
            optional = sorted(set(properties) - set(required))
            if optional:
                variants = []
                for count in range(len(optional) + 1):
                    for selected in combinations(optional, count):
                        keys = [*required, *selected]
                        variant = deepcopy(value)
                        variant["properties"] = {key: properties[key] for key in keys}
                        variant["required"] = keys
                        variants.append(_strict_wire_schema(variant))
                return {"oneOf": variants}
        if value.get("type") == "array" and "items" not in value:
            return {"type": "array", "items": {"type": "string"}}
        return {key: _strict_wire_schema(item) for key, item in value.items()
                if key not in {"minLength", "maxLength", "minItems", "maxItems", "default", "x-pilot-prose"}}
    if isinstance(value, list):
        return [_strict_wire_schema(item) for item in value]
    return deepcopy(value)


def get_host_schema(name: str) -> dict[str, Any]:
    if name not in LOCAL_PARAMETERS:
        raise ValueError(f"unknown pilot tool: {name!r}")
    return deepcopy(LOCAL_PARAMETERS[name])


def _tool(name: str, description: str, parameters: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "strict": True,
            "parameters": _strict_wire_schema(parameters),
        },
    }


TOOLS = [
    _tool("route", "Propose one registered template and a concise reason; the host validates suitability before dispatch.", ROUTE_PARAMETERS),
    _tool("spawn", "Propose bounded child calls. Copy the provided inputs {unit_id,start:0,end:<complete JSON byte count>,encoding:json} reference exactly for a first-pass single child; do not reconstruct sources. Optional source_reads belongs inside each subtask, never at top level; each read has unit_id,start,end,limit using pinned hashes and zero-based end-exclusive UTF-8 byte ranges. The host enforces fan-out, depth, custody and budget, and up to three repairs include each rejected response and precise failure.", SPAWN_PARAMETERS),
    _tool("assemble", "Propose an answer from immutable accepted result references while exposing unresolved items.", ASSEMBLE_PARAMETERS),
    _tool("read_source", "Read a task-pinned unit with {unit_id:<64-character catalogue hash>,start:0,end:<exclusive byte offset>,limit:65536}. Offsets are UTF-8 bytes within byte_count; do not split a character. Quote returned content exactly, preserving Unicode, whitespace and newlines; cite receipt.source_ref, never a filename or an unpinned id. Arbitrary paths are never accepted.", READ_SOURCE_PARAMETERS),
    _tool("verify", "Request verification of one recorded artifact reference under the host checker policy.", VERIFY_PARAMETERS),
    _tool("continue_or_stop", "After verification, decide whether to stop or change the next full pass, citing verification and carrying forward the stop rule under remaining calls and estimated dollars.", CONTINUE_PARAMETERS),
]
TOOL_BY_NAME = {item["function"]["name"]: item for item in TOOLS}


def get_tool(name: str) -> dict[str, Any]:
    """Return a defensive copy of one tool definition; unknown names fail closed."""
    try:
        return deepcopy(TOOL_BY_NAME[name])
    except KeyError as exc:
        raise ValueError(f"unknown pilot tool: {name!r}") from exc


def validate_tool_args(name: str, args: Any) -> dict[str, Any]:
    """Validate tool arguments and return a defensive copy suitable for dispatch."""
    schema = get_host_schema(name)
    normalized = normalize_delivery(args, schema)
    validate(normalized, schema)
    return normalized
