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
    key = ("off_completion_tokens" if "off_completion_tokens" in recipe["ceilings"] else "completion_tokens") if thinking == "off" else "native_completion_tokens"
    return recipe["ceilings"][key]


def lineage(seat: str | dict, endpoints_data: dict | None = None) -> str:
    return endpoint_for(seat, endpoints_data).family.rsplit("/", 1)[-1]

def validate_recipe(data: dict[str, Any]) -> None:
    if isinstance(data, dict) and data.get("schema_version") == "minireason.reason.recipe.r003-open-v1":
        validate_r003_recipe(data)
        return
    if isinstance(data, dict) and data.get("schema_version") == "minireason.reason.recipe.r002-proposed.v1":
        validate_r002_recipe(data)
        return
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
    if not path.is_file() and (str(name_or_path) + ".json") in R002_RECIPE_SHA256:
        path = R002_DIR / "recipes" / (str(name_or_path) + ".json")
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


# The published draft is immutable input; R002 activation is a separate gate.
R002_DIR = Path(__file__).resolve().parents[3] / "experiments" / "diagnostics" / "R002-episodes-under-calibrated-difficulty"
R002_RECIPE_SHA256 = {'r002-carrier-v1.json': '56529db41ba2ae8bd16bc0440bbabd39450bd3c584a15b7be603b2b909a3af92', 'r002-checker-v1.json': 'dc89e15b9643ec7962da2906fb2f82e830a56b510400ac846f849289121c78f4', 'r002-cross-match-v1.json': '38616a0aaf40ce2f58cb117266fc8dbe08b7d5b5551a52c1efae5d86acb26c91', 'r002-cross-v2.json': '87c0eae4fdc72af755f9532d1dfe2e857a854e1e8589feb3a7c5c239f0e4361f', 'r002-decomposed-v1.json': '30826917e8c80958098c2b5773c3a0cbe229ef02fc1e0cf53c83664ffa54ed8c', 'r002-decomposed-v2.json': '0ea36902417fa00bbf85ac98b10a0b4bd0b94319a3807235b924e14fa654bf01', 'r002-native-match-v1.json': '3a75c0a3560ed09e3321c61f5c28f6b34cf215dbdcc4eb65ace885ab02136b8e', 'r002-recoded-v1.json': 'ddae570a2b68373c6cf5e6f30d17f9c97ed874577c066be3b3155bc3e215f3fd', 'r002-tested-cross-v1.json': 'dc1fc3c1f0bfe28ec320c9ad40f038bc7565f1d27f2d97c30454863b03441fec'}

R003_PROFILE = "r003-open-v1"
R003_DIR = Path(__file__).resolve().parents[3] / "experiments" / "diagnostics" / "R003-open-problems-trial-series"
R003_RECIPE_SHA256 = {
    "r003-cross-v1.json": "c1c259b3ac2dd9604e54bf45dcda283921d6526e788fa44be6485d3e0a84b3ab",
    "r003-decomposed-v1.json": "78bd32b6e3c0f018e936b42e97279c49ad09068fd16878d562755c0f53af8e26",
}
R003_RECIPE_SHA256.update({
    'r003-cross-v2.json': '800fabaafa1f4a82a476bcf85177359a2a004ac49f4fb64d9a17a7beb2d4aa00',
    'r003-decomposed-v2.json': '208b3b34ac669b7a91642f6ffb33fadb8a21f70f7d87406ac5f6c67beb9451ab',
})
R003_SCHEMA_SHA256 = {
    "canonical-registry.schema.json": "b5c7f53888ba2bdbf9eb9f66240fe3ce68e066bdeb128eddf203c6b0e725d9e2",
    "decomposed-closing.schema.json": "8656aef5ee7f03c2333abb7bf5b08a72b2b74cbe640faf8931cdbc2e7f65a67b",
    "forks.schema.json": "add7e5f12e6cd314ede05d0b0cd8924d3f5e7a35e0ede6470d136c7f08f3eed0",
    "r003-relations.schema.json": "643777658c0bb2f2dca9966e59af8a947b6dae0b53d79ed5e7b7a584f5ae9e94",
}


R003_SCHEMA_SHA256.update({
    'decomposed-closing-r3-a1.schema.json': 'e76806312961ceb9ed3af823e78d8ce1ab3001aad8b7e37e29b61276adb6aa4a',
    'decomposed-return-r3-a1.schema.json': 'da244c23157a212402871c56b27008068fc62a9dfcf21bd608644e6cb513896c',
    'decomposed-step-r3-a1.schema.json': '5c238e1b3863fee29bb094d40367deb3bb578aebdf8aef0ed4d50c92934a7d6c',
    'decomposed-synthesis-r3-a1.schema.json': 'd894ed9a01661474eb5688d895bf561a240e80f3750df1c3d5e55a55070f1fe6',
    'initial-decompose-r3-a1.schema.json': 'df27ab9a2e10dae983f253d8d939d1b6d779b49bf71380f7637c80b2e45500cd',
    'r3-a1-commitment.schema.json': '40f5fcdf4c668e17f47abb8b9ed486e633c07bf62ad4c06d32ce48a292dce51b',
})

def validate_r002_recipe(data: dict[str, Any]) -> None:
    """Accept exactly a judged recipe, never silently adapt a historical one."""
    filename = str(data.get("name", "")) + ".json"
    if filename not in R002_RECIPE_SHA256:
        raise ReasonFailure("CONFIG_ERROR", "Unknown R002 recipe identity")
    path = R002_DIR / "recipes" / filename
    if hashlib.sha256(path.read_bytes()).hexdigest() != R002_RECIPE_SHA256[filename]:
        raise ReasonFailure("CONFIG_ERROR", "Published R002 recipe bytes changed")
    if data != json.loads(_read(path)):
        raise ReasonFailure("CONFIG_ERROR", "R002 recipe differs from the judged condition")
    for seat in data["seats"].values():
        endpoint_for(seat)
        thinking_for(seat)
        reasoning_effort_for(seat)


def load_r002_recipe(name_or_path):
    snapshot = load_recipe(name_or_path)
    validate_r002_recipe(snapshot["data"])
    return snapshot


def validate_r003_recipe(data: dict[str, Any]) -> None:
    """Accept only pinned R003 recipes, including the separately declared R3-A1 successor."""
    filename = str(data.get("name", "")) + ".json"
    if data.get("study_profile") != R003_PROFILE or filename not in R003_RECIPE_SHA256:
        raise ReasonFailure("CONFIG_ERROR", "Unknown R003 recipe identity")
    path = R003_DIR / "recipes" / filename
    if hashlib.sha256(path.read_bytes()).hexdigest() != R003_RECIPE_SHA256[filename]:
        raise ReasonFailure("CONFIG_ERROR", "Versioned R003 recipe bytes changed")
    if data != json.loads(_read(path)):
        raise ReasonFailure("CONFIG_ERROR", "R003 recipe differs from the versioned condition")
    if data.get("condition") not in {"LOOP-CROSS", "LOOP-DECOMPOSED"}:
        raise ReasonFailure("CONFIG_ERROR", "R003 occurrence 1 admits only CROSS and DECOMPOSED loops")
    for seat in data["seats"].values():
        endpoint_for(seat)
        thinking_for(seat)
        reasoning_effort_for(seat)


def load_r003_recipe(name_or_path):
    snapshot = load_recipe(name_or_path)
    validate_r003_recipe(snapshot["data"])
    return snapshot
