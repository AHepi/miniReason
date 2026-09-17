# Port provenance: https://github.com/AHepi/DeepReason @ 9607fba6f0a3066fbcab282c9ae0fad823e52e0c
# Upstream: src/deepreason/llm/adapter.py:156-177; MIT, Copyright (c) 2026 Aaron Hepi; see LICENSE.
"""P-A2 complete-wire preflight, adapted from DeepReason llm/adapter.py:156-177.
Provenance: AHepi/DeepReason @ 9607fba6f0a3066fbcab282c9ae0fad823e52e0c (MIT).
The byte-token premise and hidden rendering reserve remain declared assumptions.
No tokenizer estimate or live reliability claim is made by this guard.
"""
import hashlib
import json

WINDOW_SOURCE = "https://api-docs.deepseek.com/quick_start/pricing/"
WINDOW_CHECKED_UTC = "2026-09-17"
DEFAULT_CONTEXT_WINDOW = 1_000_000  # conservative decimal interpretation of 1M
DEFAULT_TEMPLATE_RESERVE = 8192

class InputError(ValueError):
    def __init__(self, code, message, receipt=None):
        self.code = code
        self.receipt = receipt or {}
        super().__init__(f"{code}: {message}")

def preflight_prepared(prepared, max_tokens, *, context_window=DEFAULT_CONTEXT_WINDOW,
                       template_reserve=DEFAULT_TEMPLATE_RESERVE):
    for name, value in (("max_tokens", max_tokens), ("context_window", context_window),
                        ("template_reserve", template_reserve)):
        if type(value) is not int or value < (0 if name == "template_reserve" else 1):
            raise InputError("INPUT_WINDOW_UNKNOWN", f"{name} must be a finite integer")
    wire = prepared.get("wire_body_text")
    if not isinstance(wire, str):
        raise InputError("INPUT_WIRE_MISSING", "exact prepared wire text is required")
    raw = wire.encode("utf-8")
    wire_hash = hashlib.sha256(raw).hexdigest()
    if wire_hash != prepared.get("wire_body_sha256"):
        raise InputError("INPUT_WIRE_MISMATCH", "prepared wire hash does not match")
    try:
        payload = json.loads(wire)
    except (TypeError,ValueError) as error:
        raise InputError("INPUT_WIRE_INVALID", "prepared wire is not one JSON object") from error
    if not isinstance(payload,dict):
        raise InputError("INPUT_WIRE_INVALID", "prepared wire is not a JSON object")
    if payload != prepared.get("payload") or payload.get("max_tokens",payload.get("options",{}).get("num_predict")) != max_tokens:
        raise InputError("INPUT_WIRE_MISMATCH", "payload or completion cap differs from exact wire")
    messages = payload.get("messages")
    if not isinstance(messages, list) or any(not isinstance(m,dict) or
        not isinstance(m.get("content"),str) for m in messages):
        raise InputError("INPUT_WINDOW_UNQUALIFIED", "P-A2 byte rule covers text messages only")
    if any(key in payload for key in ("tools", "attachments", "files")):
        raise InputError("INPUT_WINDOW_UNQUALIFIED", "native attachments/tools need separate rendering qualification")
    receipt = {"schema":"pilot.input-preflight.pa2.v1", "wire_sha256":wire_hash,
               "wire_bytes":len(raw), "prompt_token_upper_bound":len(raw),
               "completion_reserve":max_tokens, "template_reserve":template_reserve,
               "context_window":context_window, "total_bound":len(raw)+max_tokens+template_reserve,
               "window_source":WINDOW_SOURCE, "window_checked_utc":WINDOW_CHECKED_UTC,
               "premise":"each rendered text token consumes at least one UTF-8 byte; hidden rendering fits template reserve",
               "qualification":"conditional-documentation-derived-not-measured", "status":"accepted"}
    if receipt["total_bound"] > context_window:
        receipt["status"] = "refused"
        raise InputError("INPUT_WINDOW_EXCEEDED", "complete request exceeds byte-bound window", receipt)
    return receipt

# Routes used by the four staged use cases; unknown routes fail closed.
# Qwen identity convention is the same declared hosted suffixless alias used
# by R003-input-preflight.json, not a model-weight or tokenizer measurement.
_ROUTE_WINDOWS = {
    "deepseek-flash": {"model":"deepseek-flash","family":"deepseek",
        "base_url":"https://api.deepseek.com/v1","context_window":1000000,
        "source_url":WINDOW_SOURCE,"identity_scope":"official DeepSeek Flash alias; decimal 1M"},
    "ollama/qwen3.5-397b.native": {"model":"qwen3.5:397b","family":"ollama-cloud/qwen",
        "base_url":"https://ollama.com","context_window":256000,
        "source_url":"https://ollama.com/library/qwen3.5:397b-cloud",
        "identity_scope":"hosted cloud tag 256K; registry suffixless qwen3.5:397b is an explicit alias assumption; https://docs.ollama.com/api/authentication"},
}

def preflight_for_endpoint(prepared,max_tokens,endpoint_metadata):
    entry = _ROUTE_WINDOWS.get(endpoint_metadata.get("name"))
    endpoint = prepared.get("endpoint",{})
    if entry is None or any(endpoint_metadata.get(key)!=entry[key] for key in ("model","family")):
        raise InputError("INPUT_WINDOW_UNKNOWN", "route identity has no reviewed P-A2 window declaration")
    if endpoint.get("base_url") != entry["base_url"] or endpoint.get("model") != entry["model"]:
        raise InputError("INPUT_WINDOW_UNKNOWN", "prepared endpoint differs from its reviewed window identity")
    try:
        receipt = preflight_prepared(prepared,max_tokens,context_window=entry["context_window"])
    except InputError as error:
        if error.receipt:
            error.receipt.update(window_source=entry["source_url"],endpoint=endpoint_metadata,
                                 identity_scope=entry["identity_scope"])
        raise
    return {**receipt,"window_source":entry["source_url"],"endpoint":endpoint_metadata,
            "identity_scope":entry["identity_scope"]}
