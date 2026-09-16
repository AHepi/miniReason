"""Explicit recipes and the existing declared endpoint registry."""
from __future__ import annotations
import hashlib
import json
from dataclasses import replace
from pathlib import Path
from typing import Any
from minireason import provider_openai_compat as provider
from .types import ReasonFailure

RECIPES_DIR = Path(__file__).resolve().parent / "recipes"
ENDPOINTS_PATH = Path(__file__).resolve().parents[1] / "data" / "endpoints.json"

def _read(path: Path) -> str:
    with path.open(encoding="utf-8", newline="") as handle:
        return handle.read()

def load_endpoint_snapshot() -> dict[str, Any]:
    text = _read(ENDPOINTS_PATH)
    return {"data": json.loads(text), "text": text,
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}

def seat_name(seat: str | dict) -> str:
    name = seat.get("endpoint") if isinstance(seat, dict) else seat
    if not isinstance(name, str) or not name.strip():
        raise ReasonFailure("CONFIG_ERROR", "Seat needs a declared endpoint name")
    return name


def endpoint_for(name: str | dict, endpoints_data: dict | None = None) -> provider.Endpoint:
    name = seat_name(name)
    data = endpoints_data if endpoints_data is not None else load_endpoint_snapshot()["data"]
    entries = [entry for entry in data["endpoints"] if entry["name"] == name]
    if len(entries) != 1:
        raise ReasonFailure("CONFIG_ERROR", "Recipe seat is not a declared endpoint")
    endpoint = provider.Endpoint(**entries[0])
    if endpoint.key_env not in {"DEEPSEEK_API_KEY", "OLLAMA_API_KEY"}:
        raise ReasonFailure("CONFIG_ERROR", "Endpoint uses an undeclared credential environment name")
    return replace(endpoint, timeout_seconds=300)

def native_thinking_available(seat: str | dict | provider.Endpoint) -> bool:
    endpoint = seat if isinstance(seat, provider.Endpoint) else endpoint_for(seat)
    # Ollama native /api/chat accepts its existing provider-specific think
    # extra; the compatibility /v1 route has no supported thinking control.
    return endpoint.family == "deepseek" or (
        endpoint.native and endpoint.family.startswith("ollama-cloud/"))

def thinking_for(seat: str | dict, setting: str | bool | None = None,
                 endpoints_data: dict | None = None) -> str:
    endpoint = endpoint_for(seat, endpoints_data)
    supported = native_thinking_available(endpoint)
    if setting is None:
        setting = seat.get("thinking") if isinstance(seat, dict) else (
            "native" if supported else "gateway-default")
    # Bool overrides retain the old call interface; false on an unsupported
    # gateway means no wire control, and is recorded honestly as its default.
    if type(setting) is bool:
        setting = "native" if setting else ("off" if supported else "gateway-default")
    if setting not in {"native", "off", "gateway-default"}:
        raise ReasonFailure("CONFIG_ERROR", "Thinking must be native, off or gateway-default")
    if not supported and setting != "gateway-default":
        raise ReasonFailure("CONFIG_ERROR", "Endpoint has no declared explicit thinking control")
    return setting


def reasoning_effort_for(seat: str | dict) -> str:
    # Frozen recipes without this optional field keep their original high effort.
    effort = seat.get("reasoning_effort", "high") if isinstance(seat, dict) else "high"
    if not isinstance(effort, str) or effort not in {"medium", "high"}:
        raise ReasonFailure("CONFIG_ERROR", "Reasoning effort must be medium or high")
    return effort


def completion_tokens_for(recipe: dict, thinking: str) -> int:
    if not isinstance(thinking, str) or thinking not in {"native", "off", "gateway-default"}:
        raise ReasonFailure("CONFIG_ERROR", "Thinking must be native, off or gateway-default")
    # Keep the saved key name; both explicit native and gateway-default routes
    # may spend their completion allowance on hidden reasoning.
    key = "completion_tokens" if thinking == "off" else "native_completion_tokens"
    return recipe["ceilings"][key]


def lineage(seat: str | dict, endpoints_data: dict | None = None) -> str:
    return endpoint_for(seat, endpoints_data).family.rsplit("/", 1)[-1]

def validate_recipe(data: dict[str, Any]) -> None:
    def refuse(detail: str) -> None:
        raise ReasonFailure("CONFIG_ERROR", detail)
    if not isinstance(data, dict) or data.get("schema_version") != "minireason.reason.recipe.v1":
        refuse("Unsupported recipe schema")
    if not isinstance(data.get("name"), str) or not data["name"].strip():
        refuse("Recipe needs a name")
    if "closing_return" in data and type(data["closing_return"]) is not bool:
        refuse("closing_return must be a boolean")
    seats = data.get("seats", {})
    if not isinstance(seats, dict) or not {"conjecture", "critics", "use", "rival"} <= seats.keys():
        refuse("Recipe must declare conjecture, critics, use and optional rival seats")
    critics = seats["critics"]
    if not isinstance(critics, list) or not critics:
        refuse("Recipe needs at least one critic endpoint")
    names = [seats["conjecture"], seats["use"], *critics]
    if seats["rival"] is not None:
        names.append(seats["rival"])
    for name in names:
        if isinstance(name, dict) and (not {"endpoint", "thinking"} <= name.keys()
                                      or set(name) - {"endpoint", "thinking", "reasoning_effort"}):
            refuse("Seat objects must declare endpoint, thinking and optional reasoning_effort")
        endpoint_for(name)
        thinking_for(name)
        reasoning_effort_for(name)
    if data.get("cross_family") is True:
        family = lineage(seats["conjecture"])
        if any(lineage(name) == family for name in critics):
            refuse("Cross-family recipe places a critic in the conjecturer lineage")
    if "lineages" in data:
        declared = data["lineages"]
        actual = {seat_name(name): lineage(name) for name in names}
        if declared != actual:
            refuse("Declared lineages differ from the endpoint registry")
    ceilings = data.get("ceilings", {})
    if not isinstance(ceilings, dict):
        refuse("Recipe ceilings must be an object")
    for key in ("completion_tokens", "native_completion_tokens"):
        if type(ceilings.get(key)) is not int or not 1 <= ceilings[key] <= 32768:
            refuse("Completion ceiling must be an integer between 1 and 32768")
    if ceilings["native_completion_tokens"] < ceilings["completion_tokens"]:
        refuse("Reasoning-exposed completion ceiling must be at least the off ceiling")
    if ceilings.get("wall_seconds") != 300:
        refuse("The personal harness requires a 300 second call wall")
    components = data.get("components")
    if not isinstance(components, dict) or not all(
        isinstance(components.get(key), str) and components[key].strip()
        for key in ("conjecture", "criticism", "return", "use", "stop", "baseline")
    ):
        refuse("Recipe must explain every required component")
    if not isinstance(data.get("inventory"), list) or not data["inventory"]:
        refuse("Recipe needs inventory references")

def load_recipe(name_or_path: str | Path) -> dict[str, Any]:
    candidate = Path(name_or_path)
    path = candidate if candidate.is_file() else RECIPES_DIR / (str(name_or_path) + ".json")
    try:
        text = _read(path)
        data = json.loads(text)
        validate_recipe(data)
    except ReasonFailure:
        raise
    except (OSError, ValueError, TypeError, KeyError) as error:
        raise ReasonFailure("CONFIG_ERROR", "Recipe could not be read or validated") from error
    return {"data": data, "text": text,
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "source": str(path)}
