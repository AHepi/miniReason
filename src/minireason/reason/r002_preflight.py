"""Fail-closed R002 gates. Offline byte counts are fixtures, never model tokens."""
from __future__ import annotations
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
from decimal import Decimal, ROUND_HALF_UP
from .config import R002_DIR, R002_RECIPE_SHA256
from .storage import get, sha
from .types import ReasonFailure


R002_SCHEMA_SHA256 = {'answer.schema.json': '8199ff49d7e0614ca55a92118c77818debb4034ffb2c3d1b5f5233eb0c3160a9', 'checker-execution.schema.json': '5be7f778a5b6fd5f7f0990c696b3885cc9e1b35bae5061b5aec3c2c661b698a2', 'checker-proposal.schema.json': '28ef41d4be24a3faa93c6fc8a6fa7d4e0f641050f47c49b6c485840525e3d4ad', 'coding-manifest.schema.json': 'f6a2deab8fa40b60a865d1911f3abb6a7d821aa1d6b55df5e5e09172f7d5e74c', 'native-match-note.schema.json': '78a6b008fec97c79455811c126ad8ba9fea206327ed3cc65a5dc4d4593077a25', 'propagation-use.schema.json': 'be9871db06e1562568f12b25f7a742bb565504e00eb763b29761fa7572034fe7', 'prose-objection.schema.json': '91ca729888b87f3e7ab1516c8d5fde59e668bc9fa9406eb8fe3f80089c8d0678', 'prose-return.schema.json': '64b71bb33090fdf08e0bbf4ca3bd99687c18f88e79c07ebcae0c6b840488aa56', 'recoding-solve.schema.json': '69502bdefd0e89671b63fd8992da42d0d76983c198fa51be764d6961675e6d26', 'relations.schema.json': 'e005b3b510b2a7027c89a166cdc2789388c4a54a9c6aa1d6da66f8c2dab88f13', 'tested-objection.schema.json': 'dcc8a626ae0a9cfa016c7699db200f500421a17a722b85bfc47ef083982d316f', 'tested-return.schema.json': 'cb97793248f4a7cfb84792a2a91de40afd34a0883ccda40a5e6ce64af2efdd39'}
R002_SCHEMA_SHA256.update({
    "initial-decompose.schema.json": "575656d141c52524cadc92cc0e1296708a8fabb221b8a8ad366e09c77badaaf7",
    "decomposed-step.schema.json": "47d1ac2722c2193d41bbc0bf1c9227757173f2924425eb1c35241dc2287cb1ae",
    "decomposed-return.schema.json": "765d6aec42cb4e9a8858e43455c0779f3f1b1ca1e6ce94d0d35627b6604cfcae",
    "decomposed-use.schema.json": "3fe116c02237f6270e3c4feafa1447d40102dfe62b4862089bff714bbfa68340",
})
CALIBRATION_WIRE_BOUND_KIND = "fixed-calibration-exact-wire-bound-v1"
CALIBRATION_PROOF_PATH = Path(__file__).with_name("r002_calibration_bounds.json")
CONSERVATIVE_BYTE_BOUND_KIND = "conservative-byte-bound-v1"
REPO_ROOT = R002_DIR.parents[2]
CONSERVATIVE_DESCRIPTOR_SEMANTICS = (
    "Conservative upper bound over the exact UTF-8 HTTP request-body serialization; "
    "this file is a bound descriptor, not a tokenizer or an exact token count."
)
CONSERVATIVE_BOUND_RULE = "prompt_tokens <= wire_utf8_bytes + template_overhead_tokens <= 32768"
CONSERVATIVE_TEMPLATE_OVERHEAD = {
    "deepseek-flash": 0,
    "ollama/qwen3.5-397b.native": 2048,
    "ollama/glm-5.3.native": 2048,
}
CONSERVATIVE_TEMPLATE_ASSUMPTION = (
    "For exactly two nonempty text messages (system, user), no tools, media or history, "
    "assume non-DeepSeek server rendering adds at most 2048 tokens beyond content bytes. "
    "Byte-level BPE begins with one symbol per UTF-8 byte and merges cannot increase the count. "
    "Public Qwen3.5 and GLM-5 lineage text-only templates insert fewer than 256 literal UTF-8 "
    "bytes of role/start/end/thinking markers on this route; 2048 is at least eight times "
    "that deliberately loose bound, including prefix-space/control-token allowance. "
    "This is an explicit conservative template assumption, not a measured GLM-5.3 server "
    "template pin. No content duplication or unadvertised system/tool injection is assumed. "
    "DeepSeek retains the reviewed wire-slack premise supported by all 24 calibration rows."
)
CONSERVATIVE_QUALIFICATION_SCOPE = (
    "For exact nonempty two-message R002 system/user wires, the first inequality relies on "
    "the declared byte-level-BPE premise and explicit template-overhead allowance. "
    "The 24 preserved DeepSeek observations are margin evidence only; they do not empirically "
    "establish Qwen or GLM behavior. The public GLM-5 source is a lineage exemplar, not "
    "endpoint-specific proof for GLM-5.3."
)
CONSERVATIVE_ENDPOINTS = {
    "deepseek-flash": {
        "model": "deepseek-flash",
        "family": "DeepSeek-V4.1-Flash",
        "tokenizer_premise": "byte-level BPE",
        "source_scope": "exact DeepSeek V4.1 tokenizer family artifact",
        "source": (
            "https://github.com/deepseek-ai/deepseek-recipe/tree/"
            "8cadfede7063c896b944e7bae05daa3549ae97ea/static/tokenizers/v41"
        ),
    },
    "ollama/qwen3.5-397b.native": {
        "model": "qwen3.5:397b",
        "family": "Qwen3.5-397B-A17B",
        "tokenizer_premise": "byte-level BPE",
        "source_scope": "exact named Qwen model-family artifact",
        "source": "https://huggingface.co/Qwen/Qwen3.5-397B-A17B/tree/main",
    },
    "ollama/glm-5.3.native": {
        "model": "glm-5.3",
        "family": "GLM-5.3",
        "tokenizer_premise": "byte-level BPE",
        "source_scope": "GLM-5 lineage exemplar; not endpoint-specific GLM-5.3 proof",
        "source": "https://huggingface.co/zai-org/GLM-5/tree/main",
    },
}

CONSERVATIVE_BOUND_SOURCES = [
    "https://huggingface.co/docs/tokenizers/api/pre-tokenizers#tokenizers.pre_tokenizers.ByteLevel",
    "https://huggingface.co/docs/tokenizers/components#models",
    "https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/chat_template.jinja",
    "https://huggingface.co/zai-org/GLM-5/raw/main/chat_template.jinja",
]


def _object(value):
    return get(value) if isinstance(value, (str, Path)) else value


def capability_snapshot(review_receipt="UNREVIEWED", *, checker_backend_qualified=False):
    for folder, pins in (("contracts", R002_SCHEMA_SHA256), ("recipes", R002_RECIPE_SHA256)):
        for name, digest in pins.items():
            if hashlib.sha256((R002_DIR / folder / name).read_bytes()).hexdigest() != digest:
                raise ReasonFailure("CAPABILITY_REFUSED", "Published " + folder + " bytes changed")
    return {"schema": "minireason.reason.engine-capability.v1",
            "capability": "r002-contracts-v2", "prompt_contract": "r002-episodes-v2",
            "strict_attempt_policy": True, "maximum_cycles": 3,
            "no_new_objections_stop": True, "stall_switch": True,
            "off_completion_tokens": 16384, "unconditional_closing_return": True,
            "decomposed_schedule": {
                "max_steps_per_cycle": 1,
                "max_cycles": 3,
                "max_calls": 13,
                "native_slots": 5,
                "off_slots": 8,
                "completion_ceiling": 294912,
                "synthesis_when_all_steps_accepted": True,
                "stall_switch": False,
            },
            "prompt_token_cap": 32768,
            "schema_sha256": dict(R002_SCHEMA_SHA256),
            "recipe_sha256": dict(R002_RECIPE_SHA256),
            "checker_backend_qualified": checker_backend_qualified,
            "review_receipt": review_receipt}


def validate_capability(capability, condition, mode="live"):
    if capability is None and mode == "offline":
        return capability_snapshot("OFFLINE FIXTURE: unreviewed engineering")
    data = _object(capability)
    expected = capability_snapshot()
    if not isinstance(data, dict) or set(data) != set(expected):
        raise ReasonFailure("CAPABILITY_REFUSED", "Missing or extra capability fields")
    for key, value in expected.items():
        if key in {"review_receipt", "checker_backend_qualified"}:
            continue
        if json.dumps(data[key], sort_keys=True) != json.dumps(value, sort_keys=True):
            raise ReasonFailure("CAPABILITY_REFUSED", "Capability declaration or source digest mismatch: " + key)
    receipt = data["review_receipt"]
    if not isinstance(receipt, str) or not receipt.strip() or type(data["checker_backend_qualified"]) is not bool:
        raise ReasonFailure("CAPABILITY_REFUSED", "Review receipt or backend declaration absent")
    if mode == "live" and any(word in receipt.upper() for word in ("UNREVIEWED", "OFFLINE", "PLACEHOLDER", "PENDING")):
        raise ReasonFailure("CAPABILITY_REFUSED", "Offline evidence is not a published review receipt")
    if mode == "live" and condition == "LOOP-CHECKER" and not data["checker_backend_qualified"]:
        raise ReasonFailure("CHECKER_UNQUALIFIED", "Live checker requires the reviewed host backend")
    return data


def _conservative_evidence(data):
    evidence = data.get("calibration_evidence")
    evidence_keys = {
        "schema", "source_root", "row_count", "minimum_prompt_tokens_to_wire_bytes",
        "maximum_prompt_tokens_to_wire_bytes", "minimum_byte_margin", "rows",
    }
    if (not isinstance(evidence, dict) or set(evidence) != evidence_keys
            or evidence.get("schema") != "minireason.r002.conservative-byte-bound-evidence.v1"
            or evidence.get("source_root") != (
                "experiments/diagnostics/R002-episodes-under-calibrated-difficulty/"
                "runs/calibration")
            or evidence.get("row_count") != 24 or not isinstance(evidence.get("rows"), list)
            or len(evidence["rows"]) != 24):
        raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Malformed conservative byte-bound evidence")
    row_keys = {
        "candidate_id", "request_path", "request_file_sha256", "response_path",
        "response_file_sha256", "wire_body_sha256", "wire_utf8_bytes", "prompt_tokens",
        "prompt_tokens_to_wire_bytes", "byte_margin",
    }
    seen = set()
    ratios = []
    margins = []
    for row in evidence["rows"]:
        if not isinstance(row, dict) or set(row) != row_keys:
            raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Malformed conservative byte-bound row")
        candidate_id = row.get("candidate_id", "")
        if (not re.fullmatch(r"C(?:0[1-9]|1[0-9]|2[0-4])", candidate_id)
                or candidate_id in seen):
            raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Invalid conservative evidence candidate")
        seen.add(candidate_id)
        base = (
            "experiments/diagnostics/R002-episodes-under-calibrated-difficulty/"
            f"runs/calibration/{candidate_id}/"
            "calls/initial/a00/provider"
        )
        expected_request = base + "/call-0001.request.json"
        expected_response = base + "/call-0001.response.json"
        if row["request_path"] != expected_request or row["response_path"] != expected_response:
            raise ReasonFailure("TOKENIZER_MISMATCH", "Calibration evidence path differs from reviewed custody")
        request_path = (REPO_ROOT / row["request_path"]).resolve()
        response_path = (REPO_ROOT / row["response_path"]).resolve()
        try:
            if (not request_path.is_relative_to(REPO_ROOT) or not response_path.is_relative_to(REPO_ROOT)
                    or hashlib.sha256(request_path.read_bytes()).hexdigest() != row["request_file_sha256"]
                    or hashlib.sha256(response_path.read_bytes()).hexdigest() != row["response_file_sha256"]):
                raise ReasonFailure("TOKENIZER_MISMATCH", "Calibration evidence file hash mismatch")
            request = get(request_path)
            response = get(response_path)
        except ReasonFailure:
            raise
        except Exception as exc:
            raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Calibration evidence cannot be read") from exc
        wire = request.get("wire_body_text")
        if not isinstance(wire, str):
            raise ReasonFailure("TOKENIZER_MISMATCH", "Calibration request lacks exact wire text")
        raw = wire.encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        usage = response.get("usage", {})
        prompt_tokens = usage.get("prompt_tokens") if isinstance(usage, dict) else None
        try:
            ratio = (Decimal(prompt_tokens) / Decimal(len(raw))).quantize(
                Decimal("0.000000000"), rounding=ROUND_HALF_UP)
        except Exception as exc:
            raise ReasonFailure("TOKENIZER_MISMATCH", "Calibration usage is not numeric") from exc
        margin = len(raw) - prompt_tokens
        if (type(prompt_tokens) is not int or prompt_tokens <= 0 or prompt_tokens > len(raw)
                or response.get("usage_source") != "provider-reported"
                or response.get("wire_body_text") != wire
                or request.get("request") != json.loads(wire)
                or response.get("request") != json.loads(wire)
                or request.get("request_bytes") != len(raw)
                or response.get("request_bytes") != len(raw)
                or request.get("wire_body_sha256") != digest
                or response.get("wire_body_sha256") != digest
                or row["wire_body_sha256"] != digest
                or row["wire_utf8_bytes"] != len(raw)
                or row["prompt_tokens"] != prompt_tokens
                or row["prompt_tokens_to_wire_bytes"] != str(ratio)
                or row["byte_margin"] != margin):
            raise ReasonFailure("TOKENIZER_MISMATCH", "Calibration evidence row differs from preserved records")
        ratios.append(ratio)
        margins.append(margin)
    if (seen != {f"C{number:02d}" for number in range(1, 25)}
            or evidence["minimum_prompt_tokens_to_wire_bytes"] != str(min(ratios))
            or evidence["maximum_prompt_tokens_to_wire_bytes"] != str(max(ratios))
            or evidence["minimum_byte_margin"] != min(margins)):
        raise ReasonFailure("TOKENIZER_MISMATCH", "Conservative evidence summary mismatch")


def _validate_conservative_descriptor(data):
    required = {
        "schema", "kind", "limit", "descriptor_semantics", "bound_rule",
        "qualification_scope", "endpoints", "transport_serialization",
        "calibration_evidence", "review_receipt", "template_overhead_tokens",
        "template_overhead_assumption", "bound_sources",
    }
    transport = data.get("transport_serialization")
    expected_sources = {
        "src/minireason/reason/adapter.py": hashlib.sha256(
            (REPO_ROOT / "src/minireason/reason/adapter.py").read_bytes()).hexdigest(),
        "src/minireason/provider_openai_compat.py": hashlib.sha256(
            (REPO_ROOT / "src/minireason/provider_openai_compat.py").read_bytes()).hexdigest(),
    }
    expected_transport = {
        "description": (
            "Adapter.prepare and OpenAICompatProvider/OfflineProvider each call the same "
            "_build_payload implementation and serialize exactly json.dumps(payload).encode('utf-8')."
        ),
        "encoding": "utf-8",
        "json_profile": "python-json-defaults-v1",
        "source_sha256": expected_sources,
    }
    receipt = data.get("review_receipt")
    if (set(data) != required or data.get("limit") != 32768
            or data.get("descriptor_semantics") != CONSERVATIVE_DESCRIPTOR_SEMANTICS
            or data.get("bound_rule") != CONSERVATIVE_BOUND_RULE
            or data.get("qualification_scope") != CONSERVATIVE_QUALIFICATION_SCOPE
            or data.get("endpoints") != CONSERVATIVE_ENDPOINTS
            or data.get("template_overhead_tokens") != CONSERVATIVE_TEMPLATE_OVERHEAD
            or data.get("template_overhead_assumption") != CONSERVATIVE_TEMPLATE_ASSUMPTION
            or data.get("bound_sources") != CONSERVATIVE_BOUND_SOURCES
            or transport != expected_transport
            or not isinstance(receipt, str) or not receipt.strip()
            or any(word in receipt.upper() for word in ("UNREVIEWED", "PLACEHOLDER", "PENDING"))):
        raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Malformed conservative byte-bound descriptor")
    _conservative_evidence(data)
    return data


def snapshot_tokenizers(pins, mode="offline"):
    if pins is None:
        if mode == "live":
            raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Live R002 requires endpoint tokenizer pins")
        return {"schema": "minireason.r002.tokenizers.v1", "kind": "offline-utf8-byte-fixture-v1"}
    data = _object(pins)
    if not isinstance(data, dict) or data.get("schema") != "minireason.r002.tokenizers.v1":
        raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Unsupported tokenizer pin format")
    if data.get("kind") == "offline-utf8-byte-fixture-v1":
        if mode != "offline":
            raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Fixture counter cannot count live model tokens")
        return data
    if data.get("kind") == CALIBRATION_WIRE_BOUND_KIND:
        required = {
            "schema", "kind", "endpoint", "condition", "role", "prompt_contract",
            "limit", "proof_schema", "proof_sha256", "model_identity",
            "deepseek_recipe_commit", "tokenizer_sha256", "tokenizers_package_version",
            "measurement_scope", "review_receipt", "wires",
        }
        proof = _object(CALIBRATION_PROOF_PATH)
        proof_digest = hashlib.sha256(CALIBRATION_PROOF_PATH.read_bytes()).hexdigest()
        if (set(data) != required or data["endpoint"] != "deepseek-flash"
                or data["condition"] != "CAL-NATIVE" or data["role"] != "answer"
                or data["prompt_contract"] != "r002-episodes-v2" or data["limit"] != 32768
                or not isinstance(proof, dict) or proof.get("schema") != data["proof_schema"]
                or data["proof_sha256"] != proof_digest
                or data["model_identity"] != proof.get("model_identity")
                or data["deepseek_recipe_commit"] != proof.get("deepseek_recipe_commit")
                or data["tokenizer_sha256"] != proof.get("tokenizer_sha256")
                or data["tokenizers_package_version"] != proof.get("tokenizers_package_version")
                or not isinstance(data["measurement_scope"], str) or not data["measurement_scope"].strip()
                or not isinstance(data["review_receipt"], str) or not data["review_receipt"].strip()
                or not isinstance(data["wires"], dict) or len(data["wires"]) != 24):
            raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Malformed fixed calibration wire-bound descriptor")
        candidates = set()
        for digest, entry in data["wires"].items():
            if (not re.fullmatch(r"[0-9a-f]{64}", digest) or not isinstance(entry, dict)
                    or set(entry) != {"candidate_id", "wire_utf8_bytes", "prompt_tokens",
                                      "rendered_sha256", "rendered_utf8_bytes"}
                    or not re.fullmatch(r"C(?:0[1-9]|1[0-9]|2[0-4])", entry.get("candidate_id", ""))
                    or type(entry.get("wire_utf8_bytes")) is not int
                    or type(entry.get("prompt_tokens")) is not int
                    or type(entry.get("rendered_utf8_bytes")) is not int
                    or not re.fullmatch(r"[0-9a-f]{64}", entry.get("rendered_sha256", ""))
                    or entry["wire_utf8_bytes"] <= 0 or entry["rendered_utf8_bytes"] <= 0
                    or not 0 < entry["prompt_tokens"] <= data["limit"]):
                raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Invalid fixed calibration wire-bound entry")
            proven = proof.get("rows", {}).get(entry["candidate_id"])
            if (not isinstance(proven, dict) or proven.get("wire_sha256") != digest
                    or any(proven.get(key) != entry[key] for key in
                           ("wire_utf8_bytes", "prompt_tokens", "rendered_sha256", "rendered_utf8_bytes"))):
                raise ReasonFailure("TOKENIZER_MISMATCH", "Calibration descriptor differs from reviewed token proof")
            candidates.add(entry["candidate_id"])
        if candidates != {f"C{number:02d}" for number in range(1, 25)}:
            raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Fixed calibration wire bound must cover C01-C24")
        return data
    if data.get("kind") == CONSERVATIVE_BYTE_BOUND_KIND:
        return _validate_conservative_descriptor(data)
    if data.get("kind") != "huggingface-local-chat-template-v1" or not isinstance(data.get("endpoints"), dict):
        raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Require pinned local tokenizer and chat template")
    return data


def _conservative_wire(messages, endpoint_name, wire_body_text, data):
    if endpoint_name not in data["endpoints"] or not isinstance(wire_body_text, str):
        raise ReasonFailure("TOKENIZER_MISMATCH", "Conservative bound used outside its reviewed endpoints")
    if (not isinstance(messages, list) or len(messages) != 2
            or [message.get("role") if isinstance(message, dict) else None for message in messages]
            != ["system", "user"]
            or any(set(message) != {"role", "content"}
                   or not isinstance(message["content"], str) or not message["content"]
                   for message in messages)):
        raise ReasonFailure("TOKENIZER_MISMATCH", "Conservative bound requires the exact R002 message shape")
    try:
        payload = json.loads(wire_body_text)
    except (TypeError, ValueError) as exc:
        raise ReasonFailure("TOKENIZER_MISMATCH", "Conservative bound requires a serialized JSON wire") from exc
    endpoint = data["endpoints"][endpoint_name]
    if (not isinstance(payload, dict) or payload.get("model") != endpoint["model"]
            or payload.get("messages") != messages or json.dumps(payload) != wire_body_text):
        raise ReasonFailure("TOKENIZER_MISMATCH", "Wire differs from the reviewed transport serialization")
    if endpoint_name == "deepseek-flash":
        base = {"model", "messages", "stream", "max_tokens", "response_format", "thinking"}
        allowed_shapes = {frozenset(base), frozenset({*base, "reasoning_effort"})}
    else:
        allowed_shapes = {
            frozenset({"model", "messages", "stream", "options", "format", "think"})
        }
    if frozenset(payload) not in allowed_shapes or payload.get("stream") is not False:
        raise ReasonFailure("TOKENIZER_MISMATCH", "Wire fields differ from the reviewed endpoint shape")
    raw = wire_body_text.encode("utf-8")
    return len(raw), hashlib.sha256(raw).hexdigest()


def _local_counter(messages, endpoint, data):
    entry = data["endpoints"].get(endpoint)
    if not isinstance(entry, dict) or not isinstance(entry.get("files"), dict) or not entry["files"]:
        raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Endpoint tokenizer pins absent")
    root = Path(entry.get("directory", "")).resolve()
    try:
        # Pin the entire local tokenizer directory, including chat template/config.
        files = {p.relative_to(root).as_posix(): p for p in root.rglob("*") if p.is_file()}
        if set(files) != set(entry["files"]) or any(
                p.is_symlink() or p.suffix not in {".json", ".txt", ".model", ".tiktoken", ".jinja"}
                or ".env" in p.name.lower() for p in files.values()):
            raise ReasonFailure("TOKENIZER_MISMATCH", "Tokenizer paths must exactly match allowed data-file pins")
        actual = {name: hashlib.sha256(p.read_bytes()).hexdigest() for name, p in files.items()}
        if actual != entry["files"] or not {"tokenizer.json", "tokenizer_config.json"} <= actual.keys():
            raise ReasonFailure("TOKENIZER_MISMATCH", "Local tokenizer directory differs from frozen pins")
        for package in ("transformers", "tokenizers"):
            if importlib.metadata.version(package) != data.get("package_versions", {}).get(package):
                raise ReasonFailure("TOKENIZER_MISMATCH", "Tokenizer package version differs from frozen pins")
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(str(root), local_files_only=True, trust_remote_code=False)
        encoded = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True)
        if not isinstance(encoded, list) or any(type(token) is not int for token in encoded):
            raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Tokenizer did not return token IDs")
        return len(encoded), entry.get("identity", endpoint)
    except ReasonFailure:
        raise
    except Exception as exc:
        raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Pinned local tokenizer cannot be loaded") from exc


def token_preflight(messages, endpoint_name, pins=None, mode="offline", limit=32768, *,
                    wire_body_text=None, condition=None, role=None):
    if type(limit) is not int or limit != 32768:
        raise ReasonFailure("CONFIG_ERROR", "R002 prompt cap is exactly 32768")
    data = snapshot_tokenizers(pins, mode)
    if data["kind"] == "offline-utf8-byte-fixture-v1":
        # Deliberately does not claim to approximate any provider tokenizer.
        payload = json.dumps(messages, ensure_ascii=False, separators=(",", ":"))
        count, identity = len(payload.encode("utf-8")), "offline-utf8-byte-fixture-v1"
    elif data["kind"] == CALIBRATION_WIRE_BOUND_KIND:
        if (mode != "live" or endpoint_name != data["endpoint"]
                or condition != data["condition"] or role != data["role"]
                or not isinstance(wire_body_text, str)):
            raise ReasonFailure("TOKENIZER_MISMATCH", "Fixed calibration wire bound used outside its reviewed route")
        raw = wire_body_text.encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        entry = data["wires"].get(digest)
        if entry is None or entry["wire_utf8_bytes"] != len(raw):
            raise ReasonFailure("TOKENIZER_MISMATCH", "Exact calibration wire is absent from the reviewed bound")
        count = entry["prompt_tokens"]
        identity = data["model_identity"] + ":" + data["tokenizer_sha256"]
    elif data["kind"] == CONSERVATIVE_BYTE_BOUND_KIND:
        wire_bytes, wire_digest = _conservative_wire(messages, endpoint_name, wire_body_text, data)
        overhead = data["template_overhead_tokens"][endpoint_name]
        count = wire_bytes + overhead
        identity = CONSERVATIVE_BYTE_BOUND_KIND + ":" + endpoint_name
    else:
        count, identity = _local_counter(messages, endpoint_name, data)
    record = {"tokenizer_identity": identity, "tokenizer_pins_sha256": sha(json.dumps(data, sort_keys=True)),
              "counted_tokens": count, "limit": limit, "truncated": False,
              "evidence_kind": ("conservative-exact-wire-byte-bound" if
                                data["kind"] == CONSERVATIVE_BYTE_BOUND_KIND else
                                "offline-test-fixture" if mode == "offline" else
                                "pinned-public-serializer-token-count" if data["kind"] == CALIBRATION_WIRE_BOUND_KIND
                                else "tokenizer-preflight"),
              "outcome": "accepted" if count <= limit else "stop_no_truncate"}
    if data["kind"] == CALIBRATION_WIRE_BOUND_KIND:
        record.update({"wire_body_sha256": hashlib.sha256(wire_body_text.encode("utf-8")).hexdigest(),
                       "wire_utf8_bytes": len(wire_body_text.encode("utf-8")),
                       "rendered_sha256": entry["rendered_sha256"],
                       "rendered_utf8_bytes": entry["rendered_utf8_bytes"],
                       "proof_sha256": data["proof_sha256"],
                       "measurement_scope": data["measurement_scope"],
                       "review_receipt": data["review_receipt"]})
    if data["kind"] == CONSERVATIVE_BYTE_BOUND_KIND:
        record.update({
            "wire_body_sha256": wire_digest,
            "wire_utf8_bytes": wire_bytes,
            "template_overhead_tokens": overhead,
            "counted_tokens_semantics": "conservative-upper-bound-not-tokenizer-count",
            "bound_rule": data["bound_rule"],
            "qualification_scope": data["qualification_scope"],
            "calibration_ratio_minimum": data["calibration_evidence"][
                "minimum_prompt_tokens_to_wire_bytes"],
            "calibration_ratio_maximum": data["calibration_evidence"][
                "maximum_prompt_tokens_to_wire_bytes"],
            "review_receipt": data["review_receipt"],
        })
    if count > limit:
        raise ReasonFailure("PROMPT_TOKEN_CAP", "Prompt exceeds frozen tokenizer cap; no intent or truncation", record)
    return record
