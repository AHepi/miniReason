"""Fail-closed R002 gates. Offline byte counts are fixtures, never model tokens."""
from __future__ import annotations
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
from .config import R002_DIR, R002_RECIPE_SHA256
from .storage import get, sha
from .types import ReasonFailure


R002_SCHEMA_SHA256 = {'answer.schema.json': '8199ff49d7e0614ca55a92118c77818debb4034ffb2c3d1b5f5233eb0c3160a9', 'checker-execution.schema.json': '5be7f778a5b6fd5f7f0990c696b3885cc9e1b35bae5061b5aec3c2c661b698a2', 'checker-proposal.schema.json': '28ef41d4be24a3faa93c6fc8a6fa7d4e0f641050f47c49b6c485840525e3d4ad', 'coding-manifest.schema.json': 'f6a2deab8fa40b60a865d1911f3abb6a7d821aa1d6b55df5e5e09172f7d5e74c', 'native-match-note.schema.json': '78a6b008fec97c79455811c126ad8ba9fea206327ed3cc65a5dc4d4593077a25', 'propagation-use.schema.json': 'be9871db06e1562568f12b25f7a742bb565504e00eb763b29761fa7572034fe7', 'prose-objection.schema.json': '91ca729888b87f3e7ab1516c8d5fde59e668bc9fa9406eb8fe3f80089c8d0678', 'prose-return.schema.json': '64b71bb33090fdf08e0bbf4ca3bd99687c18f88e79c07ebcae0c6b840488aa56', 'recoding-solve.schema.json': '69502bdefd0e89671b63fd8992da42d0d76983c198fa51be764d6961675e6d26', 'relations.schema.json': 'e005b3b510b2a7027c89a166cdc2789388c4a54a9c6aa1d6da66f8c2dab88f13', 'tested-objection.schema.json': 'dcc8a626ae0a9cfa016c7699db200f500421a17a722b85bfc47ef083982d316f', 'tested-return.schema.json': 'cb97793248f4a7cfb84792a2a91de40afd34a0883ccda40a5e6ce64af2efdd39'}
CALIBRATION_WIRE_BOUND_KIND = "fixed-calibration-exact-wire-bound-v1"
CALIBRATION_PROOF_PATH = Path(__file__).with_name("r002_calibration_bounds.json")


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
    if data.get("kind") != "huggingface-local-chat-template-v1" or not isinstance(data.get("endpoints"), dict):
        raise ReasonFailure("TOKENIZER_UNAVAILABLE", "Require pinned local tokenizer and chat template")
    return data


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
    else:
        count, identity = _local_counter(messages, endpoint_name, data)
    record = {"tokenizer_identity": identity, "tokenizer_pins_sha256": sha(json.dumps(data, sort_keys=True)),
              "counted_tokens": count, "limit": limit, "truncated": False,
              "evidence_kind": ("offline-test-fixture" if mode == "offline" else
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
    if count > limit:
        raise ReasonFailure("PROMPT_TOKEN_CAP", "Prompt exceeds frozen tokenizer cap; no intent or truncation", record)
    return record
