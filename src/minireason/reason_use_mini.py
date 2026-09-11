"""Two-stage actual Mini route for response followed by reason use.

The response stage sees the frozen source, construction and criticism. The
use stage has only use data, use questions and, when the frozen return path is
enabled, the actual response artifact. Disabling it removes that Mini port.
No original source, construction or criticism port is available at use. Raw
prose is the model output; Mini's required wrapper is host transport only.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import re
import threading
from typing import Any, Mapping

from creib.forge.mini.common import MiniError, RUN_HEADER_DOMAIN, content_id
from creib.forge.mini.executor import Reply, Request
from creib.forge.mini.log import BlobStore, replay
from creib.forge.mini.manifest import RunPlan, compile_manifest
from creib.forge.mini.machines import (
    MachineContext, MachineSeat, register_machine_seat, resolve_machine_seat,
)
from creib.forge.mini.runner import run_mini

from minireason.provider import digest, write_new

RESPONSE = "minireason.reason-use-response.v1"
USE = "mini.verdict.v1"
STAGES = ("respond", "use")
_STAGE_KINDS = dict(zip(STAGES, (RESPONSE, USE)))
_SOURCE_SPECS = (
    ("source_text", "reason_use_source", "sources/source.txt", "minireason.reason-use-source.v1", "source", "Frozen source"),
    ("construction_text", "reason_use_construction", "sources/construction.txt", "minireason.reason-use-construction.v1", "construction", "Frozen construction"),
    ("criticism_text", "reason_use_criticism", "sources/criticism.txt", "minireason.reason-use-criticism.v1", "criticism", "Frozen criticism transport"),
    ("use_data_text", "reason_use_data", "sources/use-data.txt", "minireason.reason-use-data.v1", "use_data", "Use data"),
    ("use_questions_text", "reason_use_questions", "sources/use-questions.txt", "minireason.reason-use-questions.v1", "use_questions", "Use questions"),
)
_STAGE_PORTS = {
    "respond": ("source", "construction", "criticism"),
    "use": ("use_data", "use_questions", "actual_response"),
}
_RESPONSE_HEADER = "Actual response"
_SEED_LOCK = threading.Lock()
EMPTY_CRITICISM_TRANSPORT = "[HOST TRANSPORT ONLY: criticism_text is exactly the empty string.]"
RETURN_CONTRACT = (
    '## What to return\n'
    'A JSON object carrying "body" and "commitments". Both are strings and nothing else is required.'
)


class ReasonUseError(RuntimeError):
    def __init__(self, code: str, detail: str):
        self.code = code
        super().__init__(f"{code}: {detail}")


@dataclass(frozen=True)
class SourceFile:
    source_id: str
    path: str
    raw: bytes

    def summary(self) -> dict[str, Any]:
        return {"source_id": self.source_id, "path": self.path,
                "sha256": hashlib.sha256(self.raw).hexdigest(),
                "utf8_bytes": len(self.raw), "characters": len(self.raw.decode("utf-8"))}


@dataclass(frozen=True)
class PreparedReasonUse:
    manifest: dict[str, Any]
    plan: RunPlan
    material_digest: str
    manifest_bytes: bytes
    source_files: tuple[SourceFile, ...]
    plan_header_digest: str

    def summary(self) -> dict[str, Any]:
        return {"material_digest": self.material_digest,
                "manifest_sha256": hashlib.sha256(self.manifest_bytes).hexdigest(),
                "compiled_plan_sha256": self.plan.genesis,
                "compiled_header_sha256": self.plan_header_digest,
                "sources": [source.summary() for source in self.source_files],
                "empty_criticism_transport": EMPTY_CRITICISM_TRANSPORT,
                "empty_criticism_is_preserved_in_provider_prompt": True}


def _content(*, source_text: str, construction_text: str, criticism_text: str,
             use_data_text: str, use_questions_text: str,
             stage_instructions: Mapping[str, str], system_message: str,
             max_tokens: int, return_path: bool = True) -> dict[str, Any]:
    values = {"source_text": source_text, "construction_text": construction_text,
              "criticism_text": criticism_text, "use_data_text": use_data_text,
              "use_questions_text": use_questions_text, "system_message": system_message}
    for name, value in values.items():
        if type(value) is not str or (name != "criticism_text" and not value.strip()):
            raise ValueError(f"{name} must be text; only criticism_text may be empty")
    if criticism_text and not criticism_text.strip():
        raise ValueError("An omitted criticism must be exactly the empty string, not whitespace")
    if type(max_tokens) is not int or max_tokens < 1:
        raise ValueError("max_tokens must be a positive integer")
    if type(return_path) is not bool:
        raise ValueError("return_path must be a boolean")
    if (not isinstance(stage_instructions, Mapping) or set(stage_instructions) != set(STAGES)
            or any(type(stage_instructions[stage]) is not str or not stage_instructions[stage].strip()
                   for stage in STAGES)):
        raise ValueError("Exactly respond and use need nonempty stage instructions")
    return {**values, "stage_instructions": dict(stage_instructions), "max_tokens": max_tokens,
            "return_path": return_path}


def _stage_ports(content: Mapping[str, Any], stage: str) -> tuple[str, ...]:
    return tuple(port for port in _STAGE_PORTS[stage]
                 if port != "actual_response" or content["return_path"])


def _source_files(content: Mapping[str, Any]) -> tuple[SourceFile, ...]:
    # Retain the zero-byte criticism file as an explicit, identified source.
    return tuple(SourceFile(source_id, path, content[field].encode("utf-8"))
                 for field, source_id, path, _, _, _ in _SOURCE_SPECS)


def _transport_source(field: str, raw: str) -> str:
    return EMPTY_CRITICISM_TRANSPORT if field == "criticism_text" and raw == "" else raw


def _manifest_bytes(manifest: dict[str, Any]) -> bytes:
    return (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _copy_source(context: MachineContext) -> str:
    spec = next((spec for spec in _SOURCE_SPECS if spec[3] == context.stage.kind_id), None)
    sources = [source for source in context.plan.sources if spec and source.source_id == spec[1]]
    if spec is None or len(sources) != 1:
        raise ReasonUseError("REASON_USE_SOURCE_BINDING_MISSING", "Seed lacks its unique frozen source")
    raw = _transport_source(spec[0], sources[0].raw.decode("utf-8"))
    if not raw.strip():
        raise ReasonUseError("REASON_USE_SOURCE_EMPTY", "Only an explicitly empty criticism is allowed")
    return json.dumps({"body": raw, "commitments": raw}, ensure_ascii=False)


def _ensure_seed_seats() -> None:
    with _SEED_LOCK:
        for _, _, _, kind_id, _, _ in _SOURCE_SPECS:
            try:
                seat = resolve_machine_seat(kind_id)
            except MiniError as error:
                if error.code != "MINI_MACHINE_SEAT_UNKNOWN":
                    raise
                register_machine_seat(MachineSeat(
                    kind_id, "Copy exact frozen source; explicit empty criticism uses host transport marker", _copy_source))
            else:
                if seat.answer is not _copy_source:
                    raise ReasonUseError("REASON_USE_SEED_REGISTRY_MISMATCH", "Another seed handler is registered")


def make_manifest(**material: Any) -> dict[str, Any]:
    content = _content(**material)

    def kind(kind_id: str, title: str, instruction: str, ports: tuple[str, ...]) -> dict[str, Any]:
        return {"kind_id": kind_id, "title": title, "instruction": instruction,
                "commitment_call": "single",
                "input_ports": [{"port_id": name, "port_type": name, "window": "this_cycle"} for name in ports],
                "output_port": {"port_id": "out", "produces_kind": kind_id},
                "failure_policy": {"retries": 0, "tolerance": 0, "action": "stop"}}

    seeds = [kind(kind_id, "Frozen material: " + source_id,
                  "Copy exact frozen UTF-8 source; an empty criticism uses the declared host transport marker.", ())
             for _, source_id, _, kind_id, _, _ in _SOURCE_SPECS]
    models = [kind(_STAGE_KINDS[stage], title, content["stage_instructions"][stage], _stage_ports(content, stage))
              for stage, title in (("respond", "Respond to the frozen construction and criticism"),
                                   ("use", "Use the actual response (terminal kind is transport only)"))]
    ports = [(port, kind_id, header) for _, _, _, kind_id, port, header in _SOURCE_SPECS]
    ports.append(("actual_response", RESPONSE, _RESPONSE_HEADER))
    seed_stages = [{"stage_id": "seed_" + source_id, "kind_id": kind_id, "seat": "machine", "ports": []}
                   for _, source_id, _, kind_id, _, _ in _SOURCE_SPECS]
    return {"schema_version": "creib.mini.manifest.v1",
            "manifest_id": "minireason.reason-use.v1." + digest(content)[:24],
            "problem": "Respond to frozen material, then address use data and questions with the predeclared response return path; no standing or installation.",
            "sources": [{"source_id": source.source_id, "path": source.path} for source in _source_files(content)],
            "kinds": seeds + models,
            "port_types": [{"port_type": port, "draws_from": {"artifact_kinds": [kind_id]},
                            "render": {"rule": "list_bodies", "header": header}}
                           for port, kind_id, header in ports],
            "stages": seed_stages + [
                {"stage_id": stage, "kind_id": _STAGE_KINDS[stage], "ports": list(_stage_ports(content, stage))}
                for stage in STAGES] + [{"stage_id": "end", "end": True}],
            "cycles": {"max_cycles": 1, "max_calls": 2,
                       "completion_tokens_per_call": content["max_tokens"],
                       "max_completion_tokens": 2 * content["max_tokens"]}}


def _effective_header(plan: RunPlan) -> dict[str, Any]:
    """Reconstruct the compiler's header from the effective runtime fields."""
    return {"manifest_id": plan.manifest_id, "manifest_digest": plan.manifest_digest,
            "problem": plan.problem, "tiers": list(plan.tiers),
            "port_types": [plan.port_types[name].to_dict() for name in sorted(plan.port_types)],
            "kinds": [plan.kinds[name].to_dict() for name in sorted(plan.kinds)],
            "stages": [stage.to_dict() for stage in plan.stages],
            "routing": plan.routing.to_dict(), "cycles": plan.cycles.to_dict(),
            "policy": plan.policy.to_dict(), "attention": plan.attention.policy_id,
            "sources": [source.to_dict() for source in plan.sources],
            **({"endpoint": plan.endpoint.to_dict()} if plan.endpoint_declared else {})}


def _validate_prepared(prepared: PreparedReasonUse, content: dict[str, Any]) -> None:
    expected = make_manifest(**content)
    if (prepared.material_digest != digest(content) or prepared.manifest != expected
            or prepared.manifest_bytes != _manifest_bytes(expected)
            or prepared.source_files != _source_files(content)):
        raise ReasonUseError("REASON_USE_PREPARED_MATERIAL_MISMATCH", "Prepared material or manifest changed")
    plan = prepared.plan
    if (plan.manifest_digest != hashlib.sha256(prepared.manifest_bytes).hexdigest()
            or digest(plan.header) != prepared.plan_header_digest
            or _effective_header(plan) != plan.header
            or plan.genesis != content_id(RUN_HEADER_DOMAIN, plan.header)
            or plan.run_id != plan.genesis[:16]
            or set(plan.formats) != set(plan.kinds)
            or any(not compiled.freeform for compiled in plan.formats.values())
            or [(source.source_id, source.raw) for source in plan.sources]
            != [(source.source_id, source.raw) for source in prepared.source_files]):
        raise ReasonUseError("REASON_USE_PREPARED_PLAN_MISMATCH", "Compiled plan no longer binds the prepared route and sources")
    _ensure_seed_seats()


def _archive_prepared(root: Path, prepared: PreparedReasonUse) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for path, raw in [(root / source.path, source.raw) for source in prepared.source_files] + [
            (root / "manifest.json", prepared.manifest_bytes)]:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            if path.read_bytes() != raw:
                raise ReasonUseError("REASON_USE_ARCHIVE_MISMATCH", "Existing archive differs from prepared bytes")
        else:
            with path.open("xb") as handle:
                handle.write(raw)
    bindings = root / "material-bindings.json"
    if bindings.exists():
        if json.loads(bindings.read_text()) != prepared.summary():
            raise ReasonUseError("REASON_USE_ARCHIVE_MISMATCH", "Existing material bindings differ")
    else:
        write_new(bindings, prepared.summary())


def prepare_reason_use(root: Path, **material: Any) -> PreparedReasonUse:
    """Compile and bind exact frozen material before any provider dispatch."""
    content = _content(**material)
    manifest = make_manifest(**content)
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    source_files = _source_files(content)
    for source in source_files:
        path = root / source.path
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(source.raw)
    manifest_bytes = _manifest_bytes(manifest)
    with (root / "manifest.json").open("xb") as handle:
        handle.write(manifest_bytes)
    _ensure_seed_seats()
    plan = compile_manifest(root / "manifest.json")
    prepared = PreparedReasonUse(manifest, plan, digest(content), manifest_bytes, source_files, digest(plan.header))
    _validate_prepared(prepared, content)
    write_new(root / "material-bindings.json", prepared.summary())
    return prepared


class _ProseResponder:
    def __init__(self, provider: Any, records: Path, manifest: dict[str, Any], material: dict[str, Any]):
        self.provider = provider
        self.completion_cap = provider.settings.max_tokens
        self.records = records
        self.manifest = manifest
        self.material = material
        self.answers: dict[tuple[int, str], str] = {}
        self.visibility: list[dict[str, Any]] = []

    def reply(self, request: Request) -> Reply:
        write_new(self.records / f"{request.cycle:03d}-{request.stage_id}-routed.json",
                  {"stage": request.stage_id, "cycle": request.cycle, "mini_brief": request.brief,
                   "mini_brief_sha256": hashlib.sha256(request.brief.encode()).hexdigest(),
                   "sent_to_provider": "Only if subsequent complete route validation succeeds"})
        if (request.stage_id not in STAGES or request.phase != "both" or request.cycle != 1
                or request.kind_id != _STAGE_KINDS[request.stage_id]):
            raise ReasonUseError("REASON_USE_COORDINATE_INVALID", "Unexpected stage, cycle, kind or phase")
        if (request.cycle, request.stage_id) in self.answers:
            raise ReasonUseError("REASON_USE_DUPLICATE_STAGE", "Each model stage may run only once")
        kind = next(kind for kind in self.manifest["kinds"] if kind["kind_id"] == request.kind_id)
        sections = [re.escape("# " + kind["title"]), re.escape(kind["instruction"])]
        history = []
        visible_sources = []
        for entry in kind["input_ports"]:
            name = entry["port_id"]
            source_spec = next((spec for spec in _SOURCE_SPECS if spec[4] == name), None)
            if source_spec is not None:
                field, _, _, source_kind, _, header = source_spec
                raw = _transport_source(field, self.material[field])
                visible_sources.append(field)
            else:
                if name != "actual_response" or request.stage_id != "use":
                    raise ReasonUseError("REASON_USE_ROUTING_MISMATCH", "Unexpected history port")
                source_kind, header = RESPONSE, _RESPONSE_HEADER
                raw = self.answers.get((request.cycle, "respond"))
                if raw is None:
                    raise ReasonUseError("REASON_USE_HISTORY_MISSING", "The actual response was not obtained")
                history.append({"stage": "respond", "text": raw})
            sections.append(re.escape(f"## {header} ({name})\n[") + r"[0-9a-f]{16}"
                            + re.escape(f"] ({source_kind})\n" + raw))
        sections.append(re.escape(RETURN_CONTRACT))
        if re.fullmatch(r"\n\n".join(sections), request.brief) is None:
            raise ReasonUseError("REASON_USE_ROUTING_MISMATCH", "Mini delivered missing, changed or additional material")
        from .reason_use_study import stage_prompt, validate_response
        prompt = stage_prompt(self.material, request.stage_id, history)
        is_respond = request.stage_id == "respond"
        exposure = {"stage": request.stage_id, "cycle": request.cycle,
                    "mini_brief_sha256": hashlib.sha256(request.brief.encode()).hexdigest(),
                    "sent_prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                    "mini_brief": request.brief, "sent_prompt": prompt,
                    "transport_transformation": "Verify complete routed brief, then use the shared direct stage renderer",
                    "complete_routed_brief_verified": True,
                    "source_packet_port_visible": is_respond,
                    "original_construction_port_visible": is_respond,
                    "criticism_port_visible": is_respond,
                    "use_data_port_visible": not is_respond,
                    "use_questions_port_visible": not is_respond,
                    "actual_response_port_visible": not is_respond and self.material["return_path"],
                    "return_path": self.material["return_path"],
                    "source_fields_visible": visible_sources,
                    "history_stages_visible": [row["stage"] for row in history],
                    "criticism_text_empty": self.material["criticism_text"] == "",
                    "terminal_kind_is_transport_only": not is_respond}
        write_new(self.records / f"{request.cycle:03d}-{request.stage_id}.json", exposure)
        self.visibility.append({key: value for key, value in exposure.items()
                                if key not in {"mini_brief", "sent_prompt"}})
        response = self.provider.complete([
            {"role": "system", "content": self.material["system_message"]},
            {"role": "user", "content": prompt}], json_output=False,
            coordinate={"stage": request.stage_id, "cycle": request.cycle,
                        "phase": "raw-prose", "mini_kind": request.kind_id})
        raw = validate_response(response, self.completion_cap)
        wrapped = json.dumps({"body": raw, "commitments": raw}, ensure_ascii=False)
        self.answers[request.cycle, request.stage_id] = raw
        write_new(self.records / f"{request.cycle:03d}-{request.stage_id}-transport.json",
                  {"raw_text_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                   "raw_utf8_bytes": len(raw.encode()), "wrapped_utf8_bytes": len(wrapped.encode()),
                   "wrapper_is_host_generated": True, "independent_commitment_call": False,
                   "wrapper_tokens": None, "wrapper_token_note": "Host serialization is not model output",
                   "provider_completion_tokens": response["usage"]["completion_tokens"]})
        return Reply(wrapped, response["usage"]["prompt_tokens"], response["usage"]["completion_tokens"])


def run_reason_use(provider: Any, root: Path, prepared: PreparedReasonUse | None = None,
                   **material: Any) -> dict[str, Any]:
    """Execute exactly respond/use, retaining partial artifacts on failure."""
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    content = _content(**material)
    manifest = make_manifest(**content)
    result: dict[str, Any] = {"schema": "minireason.reason-use-mini.v1", "status": "RUNNING",
                             "return_path": content["return_path"],
                             "history": [], "final": None, "mini_outcome": None, "alarms": [],
                             "manifest_sha256": hashlib.sha256(_manifest_bytes(manifest)).hexdigest(),
                             "visibility": [], "interpretation_status": "NOT_ADJUDICATED",
                             "transport": "Raw prose duplicated in host body/commitments wrapper; ports render body only",
                             "standing_effect": "NONE", "installation_policy": "NONE",
                             "terminal_kind": {"kind_id": USE, "stage": "use", "transport_only": True,
                                               "semantic_verdict": False}}
    write_new(root / "reason-use-started.json", result)
    responder = _ProseResponder(provider, root / "requests", manifest, content)
    compiled = None
    try:
        if provider.settings.max_tokens != content["max_tokens"]:
            raise ReasonUseError("REASON_USE_COMPLETION_CAP_MISMATCH", "Provider ceiling differs from frozen manifest")
        if prepared is None:
            prepared = prepare_reason_use(root, **content)
        else:
            _validate_prepared(prepared, content)
            _archive_prepared(root, prepared)
        compiled = prepared.plan
        result["prepared_bindings"] = prepared.summary()
        outcome = run_mini(compiled, root / "run", responder,
                           responder_id="deepseek:" + provider.settings.model, endpoint=provider.settings)
        result["mini_outcome"] = {**asdict(outcome), "root": "run", "stages_entered": list(outcome.stages_entered)}
        if outcome.cycles_completed != 1 or outcome.calls != 2:
            raise ReasonUseError("REASON_USE_ROUTE_INCOMPLETE", "Both model stages must complete exactly once")
        result["status"] = "COMPLETE"
    except Exception as error:
        result["status"] = "OPERATIONAL_FAILURE"
        result["alarms"].append({"code": getattr(error, "code", type(error).__name__), "detail": str(error)})
    result["visibility"] = responder.visibility
    log_path = root / "run/log.jsonl"
    if compiled is not None and log_path.exists():
        try:
            state = replay(log_path, compiled.genesis)
            blobs = BlobStore(root / "run/blobs")
            for artifact_id in state.artifact_order:
                artifact = state.artifacts[artifact_id]
                if artifact["kind_id"] not in _STAGE_KINDS.values():
                    continue
                raw = blobs.get(artifact["body_ref"]).decode("utf-8")
                stage = next(stage for stage, kind_id in _STAGE_KINDS.items() if kind_id == artifact["kind_id"])
                if raw != responder.answers.get((artifact["cycle"], stage)):
                    raise ReasonUseError("REASON_USE_ARTIFACT_MISMATCH", "Stored artifact differs from actual provider prose")
                row = {"stage": stage, "cycle": artifact["cycle"], "artifact_id": artifact_id,
                       "text": raw, "text_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                       "answer": {"body": raw, "commitments": raw}, "proposed_changes_installed": False,
                       "semantic_verdict": False}
                result["history"].append(row)
                if stage == "use":
                    result["final"] = row["answer"]
            for line in log_path.read_text().splitlines():
                event = json.loads(line)
                if event["type"] in {"FORMAT_FAILURE", "REFUSED", "SUBMISSION_DROPPED", "BUDGET_REFUSED", "PORT_EMPTY"}:
                    result["alarms"].append({"code": event["type"], "event_id": event["event_id"],
                                             "stage": event["stage_id"], "payload": event["payload"]})
        except Exception as error:
            result["alarms"].append({"code": getattr(error, "code", "REASON_USE_LOG_UNREADABLE"), "detail": str(error)})
    if result["status"] == "COMPLETE" and [row["stage"] for row in result["history"]] != list(STAGES):
        result["alarms"].append({"code": "REASON_USE_HISTORY_INCOMPLETE", "detail": "Expected exactly respond/use artifacts"})
    if result["alarms"]:
        result["status"] = "OPERATIONAL_FAILURE"
    write_new(root / "reason-use-result.json", result)
    write_new(root / "reason-use-errata.json", {"operational": result["alarms"],
              "content_appraisal": "No automatic bearing, adequacy, creativity or success verdict"})
    return result
