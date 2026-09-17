"""OpenAI-compatible function tool manifest for the owner-operated pilot harness."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .templates import COMMON_INPUT_SCHEMA, TEMPLATE_IDS, validate

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
SPAWN_PARAMETERS = {
    "type": "object",
    "properties": {
        "subtasks": {
            "type": "array",
            "minItems": 1,
            "maxItems": 8,
            "items": {
                "type": "object",
                "properties": {
                    "template_id": deepcopy(_TEMPLATE_ENUM),
                    "inputs": deepcopy(COMMON_INPUT_SCHEMA),
                },
                "required": ["template_id", "inputs"],
                "additionalProperties": False,
            },
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
VERIFY_PARAMETERS = {
    "type": "object",
    "properties": {"artifact_ref": {"type": "string", "minLength": 1}},
    "required": ["artifact_ref"],
    "additionalProperties": False,
}


LOCAL_PARAMETERS = {
    "route": ROUTE_PARAMETERS,
    "spawn": SPAWN_PARAMETERS,
    "assemble": ASSEMBLE_PARAMETERS,
    "verify": VERIFY_PARAMETERS,
}


def _strict_wire_schema(value: Any) -> Any:
    """Export the documented beta subset; retain stronger bounds at the host."""
    if isinstance(value, dict):
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
    _tool("verify", "Request verification of one recorded artifact reference under the host checker policy.", VERIFY_PARAMETERS),
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
