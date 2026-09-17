"""OpenAI-compatible function tool manifest for the owner-operated pilot harness."""

from __future__ import annotations

from copy import deepcopy
from itertools import combinations
from typing import Any

from .templates import SPAWN_INPUT_SCHEMA, TEMPLATE_IDS, validate

_TEMPLATE_ENUM = {"type": "string", "enum": list(TEMPLATE_IDS)}
_STRING_LIST = {"type": "array", "items": {"type": "string"}}

ROUTE_PARAMETERS = {
    "type": "object",
    "properties": {
        "template_id": deepcopy(_TEMPLATE_ENUM),
        "reason": {"type": "string", "minLength": 1},
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
        "answer": {"type": "string"},
        "unresolved": deepcopy(_STRING_LIST),
    },
    "required": ["result_refs", "answer", "unresolved"],
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
    "required": ["decision", "reason", "what_changes_next", "stop_rule"],
    "properties": {
        "decision": {"type": "string", "enum": ["continue", "stop"]},
        "reason": {"type": "string", "minLength": 1},
        "what_changes_next": {"type": "string"},
        "stop_rule": {"type": "string", "minLength": 1},
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
        return {key: _strict_wire_schema(item) for key, item in value.items()
                if key not in {"minLength", "maxLength", "minItems", "maxItems"}}
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
    _tool("spawn", "Propose bounded child calls; the host mints IDs and enforces fan-out, depth, custody, and budget.", SPAWN_PARAMETERS),
    _tool("assemble", "Propose an answer from immutable accepted result references while exposing unresolved items.", ASSEMBLE_PARAMETERS),
    _tool("read_source", "Read an exact bounded byte range from one task-pinned source unit; arbitrary paths are never accepted.", READ_SOURCE_PARAMETERS),
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
    validate(args, get_host_schema(name))
    return deepcopy(args)
