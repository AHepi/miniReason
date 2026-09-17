"""R3-A1 context-derived input budgets; no tokenizer or provider measurement."""
from __future__ import annotations
from copy import deepcopy
import json
from .types import ReasonFailure

AMENDMENT = "R3-A1"
BOUND_RULE = "wire_utf8_bytes <= context_window_tokens - completion_ceiling_tokens - reserve_tokens"
QUALIFICATION = (
    "R3-A1 documentation-derived context budgets, not measured context windows or token counts. "
    "The exact two-message byte-level-BPE and no-content-duplication premises remain; "
    "non-DeepSeek server-template reserve is 2048 tokens. Calibration ratios are DeepSeek "
    "margin evidence only, not a tokenizer for any route. Kimi inherits this declared "
    "byte-level-BPE/template assumption without endpoint-specific calibration."
)

def validate_descriptor(data):
    from . import r002_preflight as old
    extra = {"amendment", "context_windows", "input_caps"}
    if data.get("amendment") != AMENDMENT or not extra <= data.keys():
        raise ReasonFailure("TOKENIZER_UNAVAILABLE", "R3-A1 descriptor fields absent")
    windows, caps = data["context_windows"], data["input_caps"]
    expected_routes = {*old.CONSERVATIVE_ENDPOINTS, "ollama/kimi-k3.native"}
    if (not isinstance(windows, dict) or set(windows) != expected_routes
            or not isinstance(caps, dict) or set(caps) != expected_routes
            or data.get("limit") != "per-route-context-window"
            or data.get("bound_rule") != BOUND_RULE
            or data.get("qualification_scope") != QUALIFICATION
            or set(data.get("endpoints", {})) != expected_routes
            or data.get("template_overhead_tokens") != {
                key: 0 if key == "deepseek-flash" else 2048 for key in expected_routes}):
        raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Malformed R3-A1 context budgets")
    for route, entry in windows.items():
        if (not isinstance(entry, dict) or set(entry) != {
                "context_window_tokens", "completion_ceiling_tokens", "reserve_tokens",
                "documentation_value", "source_url", "accessed_utc", "value_kind", "identity_scope"}
                or entry.get("value_kind") != "provider-documentation-not-measured"
                or any(type(entry.get(k)) is not int for k in (
                    "context_window_tokens", "completion_ceiling_tokens", "reserve_tokens"))
                or not 32768 < entry["context_window_tokens"] <= 2097152
                or entry["completion_ceiling_tokens"] != 32768
                or entry["reserve_tokens"] != (0 if route == "deepseek-flash" else 2048)
                or any(not isinstance(entry.get(k), str) or not entry[k].strip() for k in (
                    "documentation_value", "source_url", "accessed_utc", "identity_scope"))
                or not entry["source_url"].startswith("https://")
                or type(caps[route]) is not int
                or caps[route] != entry["context_window_tokens"] - entry["completion_ceiling_tokens"] - entry["reserve_tokens"]):
            raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Invalid context window, completion ceiling, reserve or cap")
    if any(data["endpoints"].get(k) != v for k,v in old.CONSERVATIVE_ENDPOINTS.items()):
        raise ReasonFailure("TOKENIZER_MISMATCH", "R3-A1 endpoint bound premises changed")
    kimi = data["endpoints"]["ollama/kimi-k3.native"]
    if kimi != {"model": "kimi-k3", "family": "Kimi-K3", "tokenizer_premise": "byte-level BPE",
                "source_scope": "declared assumption; no endpoint-specific tokenizer measurement",
                "source": "https://ollama.com/library/kimi-k3"}:
        raise ReasonFailure("TOKENIZER_MISMATCH", "Kimi bound premise differs")
    # Reuse the exact calibration custody and transport checks, retaining R002's
    # immutable descriptor validator and its strict legacy cap.
    base = deepcopy(data)
    for key in extra:
        del base[key]
    base.update(limit=32768, bound_rule=old.CONSERVATIVE_BOUND_RULE,
                qualification_scope=old.CONSERVATIVE_QUALIFICATION_SCOPE,
                endpoints=old.CONSERVATIVE_ENDPOINTS,
                template_overhead_tokens=old.CONSERVATIVE_TEMPLATE_OVERHEAD)
    old._validate_conservative_descriptor(base)
    return data

def wire_budget(data, endpoint_name, wire_body_text):
    entry = data["context_windows"].get(endpoint_name)
    if entry is None:
        raise ReasonFailure("TOKENIZER_MISMATCH", "No context window for route")
    payload = json.loads(wire_body_text)
    requested = (payload.get("max_tokens") if endpoint_name == "deepseek-flash"
                 else payload.get("options", {}).get("num_predict"))
    if type(requested) is not int or not 0 < requested <= entry["completion_ceiling_tokens"]:
        raise ReasonFailure("TOKENIZER_MISMATCH", "Wire completion allowance exceeds reserved ceiling")
    return {**entry, "input_cap_tokens": data["input_caps"][endpoint_name],
            "requested_completion_tokens": requested}
