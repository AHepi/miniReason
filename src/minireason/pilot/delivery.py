"""P-A4 declared output exposure policy; no tokenization or semantic guarantee."""
from copy import deepcopy
from .util import encoded
from minireason.reason.types import ReasonFailure

CONTROL_ROLES = frozenset({"route", "spawn", "continue_or_stop"})
CONTROL_TOKENS = 4096
WORKER_TOKENS = 16384
OUTPUT_FRAMING_BYTES = 4096
# Conservative decimal interpretation of DeepSeek's official 384K max output.
# Qwen's host route cap is declared here, below its 256K context; the official
# Ollama model page does not give a separate output limit. It is not that claim.
ROUTE_LIMITS = {
    "deepseek-flash": {"maximum": 384000, "source": "https://api-docs.deepseek.com/quick_start/pricing/", "scope": "official 384K output, conservative decimal interpretation"},
    "ollama/qwen3.5-397b.native": {"maximum": 65536, "source": "https://ollama.com/library/qwen3.5:397b-cloud", "scope": "P-A4 host route maximum, within documented 256K total context; provider output maximum unspecified"},
}

def route_maximum(seat):
    if seat not in ROUTE_LIMITS:
        raise ReasonFailure("OUTPUT_ROUTE_UNKNOWN", "No reviewed output maximum for route " + str(seat))
    return ROUTE_LIMITS[seat]["maximum"]

def output_policy(role, packet, *, seat="deepseek-flash", task_inputs=None):
    entry = ROUTE_LIMITS.get(seat)
    maximum = route_maximum(seat)
    if role in CONTROL_ROLES:
        return {"role": role, "max_tokens": CONTROL_TOKENS, "maximum": maximum, "kind": "control", "ranges": []}
    refs = []
    inputs = packet.get("inputs", packet.get("resolved_inputs"))
    if isinstance(inputs, dict) and "unit_id" in inputs:
        refs.append({k: inputs[k] for k in ("unit_id", "start", "end")})
    elif isinstance(inputs, dict) and task_inputs is not None:
        ref = task_inputs.compact_inputs(inputs)
        refs.append({k: ref[k] for k in ("unit_id", "start", "end")})
    for value in packet.get("resolved_source_reads", []):
        ref = value["receipt"]
        refs.append({k: ref[k] for k in ("unit_id", "start", "end")})
    unique = {encoded(r): r for r in refs}
    refs = list(unique.values())
    range_bytes = sum(ref["end"] - ref["start"] for ref in refs)
    # Workers without an input unit (critics/assembly) bound their entire public
    # data packet. Otherwise include other work products in addition to ranges.
    extra = {k:v for k,v in packet.items() if k in {"candidate", "accepted_results", "returned", "judgments", "objections", "task"}}
    extra_bytes = len(encoded(extra).encode("utf-8")) if extra else 0
    if not refs:
        range_bytes = len(encoded(packet).encode("utf-8"))
        extra_bytes = 0
    needed = range_bytes + extra_bytes + OUTPUT_FRAMING_BYTES
    policy = {"kind": "worker", "role": role, "ranges": deepcopy(refs), "routed_bytes": range_bytes,
        "other_work_bytes": extra_bytes, "requested_output_bytes": needed,
        "output_token_upper_bound": needed, "default_tokens": WORKER_TOKENS,
        "max_tokens": WORKER_TOKENS if needed <= WORKER_TOKENS else maximum,
        "maximum": maximum, "route": seat, "source": entry["source"], "scope": entry["scope"],
        "checked_utc": "2026-09-17", "rule": "routed bytes + other work bytes + 4096 framing/prose bytes; tokens <= bytes",
        "limit": "Declared output envelope, not a prediction that arbitrary semantic work fits", "status": "accepted"}
    if needed > maximum:
        policy["status"] = "refused"
        raise ReasonFailure("OUTPUT_RANGE_TOO_LARGE", "Declared output byte bound exceeds route maximum before dispatch", policy)
    return policy

def half_ranges(body, start, end):
    """Two exact nonempty UTF-8 ranges; never replace or normalize a byte."""
    middle = (start + end) // 2
    while middle > start:
        try:
            body[start:middle].decode("utf-8"); body[middle:end].decode("utf-8")
            return [(start, middle), (middle, end)]
        except UnicodeDecodeError:
            middle -= 1
    raise ReasonFailure("WORKER_RANGE_UNSPLITTABLE", "Range has no two nonempty UTF-8 halves")
