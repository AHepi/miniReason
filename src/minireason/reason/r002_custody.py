"""Input-byte custody for the R002 engine; sealed values never enter prompts."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from .storage import read, put, get, sha
from .types import ReasonFailure
from .r002_preflight import R002_SCHEMA_SHA256

ROLES = ("answer", "prose_critic", "tested_critic", "prose_return", "tested_return",
         "propagation_use", "blind_coding_solve", "native_match_note", "native_match_synthesis",
         "initial_decompose", "decomposed_step", "decomposed_critic",
         "decomposed_return", "decomposed_use", "decomposed_synthesis", "decomposed_closing")


def _refuse(detail):
    raise ReasonFailure("RUN_INTEGRITY_ERROR", detail)


def _scoped(base, name):
    if not isinstance(name, str) or "\\" in name:
        _refuse("Coding source needs a relative POSIX path")
    rel = PurePosixPath(name)
    if rel.is_absolute() or ".." in rel.parts or ":" in name:
        _refuse("Coding source escapes the study directory")
    path = base / name
    if path.is_symlink() or not path.resolve().is_relative_to(base.resolve()):
        _refuse("Coding source escapes the study directory")
    return path


def validate_coding(path, manifest, problem_id, problem, relation, fork):
    if path is None or manifest is None:
        raise ReasonFailure("CONFIG_ERROR", "Every R002 loop needs a file-backed coding manifest for stall routing")
    base = Path(path).resolve().parent.parent
    matches = [row for row in manifest.get("candidates", []) if row.get("candidate_id") == problem_id]
    if len(matches) != 1:
        _refuse("Coding manifest candidate is absent or duplicated")
    entry = matches[0]
    required = {"problem_path": f"problems/{problem_id}.txt",
                "recoded_problem_path": f"problems/recoded/{problem_id}.txt",
                "carrier_problem_path": f"problems/carrier/{problem_id}.txt",
                "answer_path": f"answers/{problem_id}.md", "oracle_path": f"oracle/{problem_id}.py"}
    texts = {}
    for key, expected in required.items():
        if entry.get(key) != expected:
            _refuse("Coding manifest changes a candidate source path")
        source = _scoped(base, entry[key])
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        if digest != entry.get("hashes", {}).get(key.replace("_path", "_sha256")):
            _refuse("Coding source hash mismatch: " + key)
        if key in {"problem_path", "recoded_problem_path", "carrier_problem_path"}:
            texts[key] = read(source)
    support = entry.get("oracle_support_paths")
    support_hashes = entry.get("oracle_support_sha256")
    if not isinstance(support, list) or not isinstance(support_hashes, dict) or set(support) != set(support_hashes) or len(support) != len(set(support)):
        _refuse("Oracle support path/hash binding is incomplete")
    for name in support:
        if not name.startswith("oracle/") or not name.endswith(".py"):
            _refuse("Unexpected oracle support source")
        if hashlib.sha256(_scoped(base, name).read_bytes()).hexdigest() != support_hashes[name]:
            _refuse("Oracle support source hash mismatch")
    original = texts["problem_path"]
    if original != problem:
        _refuse("Working problem does not equal its frozen canonical coding")
    expected_ids = [row["relation_id"] for row in relation["relations"]]
    if entry.get("relation_ids") != expected_ids:
        _refuse("Coding changes the public relation set or order")
    if entry.get("inverse_output_map") != {"type": "identity"} or entry.get("forward_notation_map") != {}:
        _refuse("Unreviewed nonidentity recoding map")
    lines = original.splitlines(keepends=True)
    positions = [i for i, line in enumerate(lines) if line.startswith("- ")]
    givens = [lines[i] for i in positions]
    forward, inverse = entry.get("forward_order_map"), entry.get("inverse_order_map")
    for order in (forward, inverse):
        if not isinstance(order, list) or any(type(i) is not int for i in order) or sorted(order) != list(range(len(givens))):
            _refuse("Coding order map is not a permutation")
    transformed = [givens[i] for i in forward]
    if [transformed[i] for i in inverse] != givens:
        _refuse("Coding inverse does not recover original givens")
    if forward != fork.get("recoding_order") or not transformed or fork.get("public_anchor", "") not in transformed[0]:
        _refuse("Recoding does not target the declared public branch")
    for index, value in zip(positions, transformed):
        lines[index] = value
    if "".join(lines) != texts["recoded_problem_path"]:
        _refuse("Recoding changes content outside the declared permutation")
    if texts["carrier_problem_path"] != entry.get("carrier_tag", "") + "\n" + original:
        _refuse("Carrier changes represented content")
    return texts


def validate_r003_canonical(path, manifest, problem_id, problem):
    """Bind an occurrence-local canonical problem copy without opening coded material."""
    if path is None or manifest is None:
        raise ReasonFailure("CONFIG_ERROR", "R003 requires a file-backed canonical registry")
    expected_keys = {"schema_version", "study_profile", "candidates"}
    if (not isinstance(manifest, dict) or set(manifest) != expected_keys
            or manifest.get("schema_version") != "minireason.reason.r003-canonical-registry.v1"
            or manifest.get("study_profile") != "r003-open-v1"):
        _refuse("R003 canonical registry header is invalid")
    candidates = manifest.get("candidates")
    if not isinstance(candidates, list) or not 1 <= len(candidates) <= 8:
        _refuse("R003 canonical registry must contain one to eight candidates")
    ids = [row.get("candidate_id") for row in candidates if isinstance(row, dict)]
    if (len(ids) != len(candidates) or len(ids) != len(set(ids))
            or any(not re.fullmatch(r"O0[1-8]", value or "") for value in ids)):
        _refuse("R003 canonical candidate IDs are invalid or duplicated")
    base = Path(path).resolve().parent
    for row in candidates:
        if set(row) != {"candidate_id", "canonical_problem", "problem_sha256"}:
            _refuse("R003 canonical candidate fields are incomplete or unexpected")
        row_id = row["candidate_id"]
        row_path = f"p/{row_id}.txt"
        digest = row.get("problem_sha256")
        if row.get("canonical_problem") != row_path:
            _refuse("R003 canonical problem path is not occurrence-local")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            _refuse("R003 canonical problem hash is invalid")
        if hashlib.sha256(_scoped(base, row_path).read_bytes()).hexdigest() != digest:
            _refuse("R003 canonical problem hash mismatch: " + row_id)
    matches = [row for row in candidates if row["candidate_id"] == problem_id]
    if len(matches) != 1:
        _refuse("R003 canonical registry candidate is absent or duplicated")
    entry = matches[0]
    expected_path = f"p/{problem_id}.txt"
    digest = entry.get("problem_sha256")
    source = _scoped(base, expected_path)
    if read(source) != problem:
        _refuse("Working problem differs from the occurrence canonical copy")
    return dict(entry), {
        "schema": "minireason.reason.r003-canonical-custody.v1",
        "study_profile": "r003-open-v1",
        "candidate_id": problem_id,
        "source_registry_sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        "source_problem_path": expected_path,
        "source_problem_sha256": digest,
        "run_problem_path": "problem.txt",
        "run_problem_sha256": digest,
    }


def prompt_snapshot(study_profile=None):
    from .prompts import R002_SYSTEM, R002_SUFFIXES, R003_SYSTEM, R003_SUFFIXES
    system = R003_SYSTEM if study_profile == "r003-open-v1" else R002_SYSTEM
    suffixes = R003_SUFFIXES if study_profile == "r003-open-v1" else R002_SUFFIXES
    roles = ROLES if study_profile == "r003-open-v1" else tuple(
        role for role in ROLES if role != "decomposed_closing")
    return {role: system + "\n" + suffixes[role] for role in roles}


def freeze_inputs(directory, cfg):
    directory = Path(directory)
    study_profile = cfg.get("study_profile")
    put(directory / "prompt-contract.json", prompt_snapshot(study_profile))
    cfg["frozen_inputs"] = {p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in sorted(directory.rglob("*")) if p.is_file()}
    expected_pins = dict(R002_SCHEMA_SHA256)
    if study_profile == "r003-open-v1":
        from .config import R003_SCHEMA_SHA256
        expected_pins.update(R003_SCHEMA_SHA256)
    expected = {"contracts/" + name for name in expected_pins}
    if {name for name in cfg["frozen_inputs"] if name.startswith("contracts/")} != expected:
        _refuse("Frozen schemas are missing or unexpected")
    for name, digest in expected_pins.items():
        if cfg["frozen_inputs"]["contracts/" + name] != digest:
            _refuse("Copied schema bytes differ from the published contract")
    put(directory / "config.json", cfg)
    put(directory / "config-seal.json", {"sha256": sha(read(directory / "config.json"))})


def validate_frozen_inputs(directory):
    directory = Path(directory)
    try:
        if sha(read(directory / "config.json")) != get(directory / "config-seal.json")["sha256"]:
            _refuse("Saved R002 configuration changed")
        cfg = get(directory / "config.json")
        for name, digest in cfg["frozen_inputs"].items():
            if hashlib.sha256(_scoped(directory, name).read_bytes()).hexdigest() != digest:
                _refuse("Saved R002 input changed: " + name)
        expected = set(R002_SCHEMA_SHA256)
        if cfg.get("study_profile") == "r003-open-v1":
            from .config import R003_SCHEMA_SHA256
            expected.update(R003_SCHEMA_SHA256)
        if {p.name for p in (directory / "contracts").glob("*.schema.json")} != expected:
            _refuse("Saved schema inventory changed")
        if get(directory / "prompt-contract.json") != prompt_snapshot(cfg.get("study_profile")):
            _refuse("R002 prompt implementation changed; create a separately identified occurrence")
        return cfg
    except ReasonFailure:
        raise
    except (OSError, KeyError, TypeError, ValueError) as exc:
        raise ReasonFailure("RUN_INTEGRITY_ERROR", "Saved R002 input custody is incomplete") from exc
