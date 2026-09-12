"""One actual Mini episode locating and discriminating a frozen successor issue.

The complete verified handoff is visible at both stages. Only discriminate
also receives the exact actual locate artifact. Prose and no-promotion are
legitimate outputs; host terminal kinds assign no semantic standing.
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

LOCATE = "minireason.successor-locate.v1"
DISCRIMINATE = "mini.verdict.v1"
STAGES = ("locate", "discriminate")
_STAGE_KINDS = dict(zip(STAGES, (LOCATE, DISCRIMINATE)))
_SOURCE_SPECS = (
    ("handoff_text", "successor_handoff", "sources/handoff.txt", "minireason.successor-handoff.v1", "handoff", "Whole verified parent handoff"),
)
_STAGE_PORTS = {"locate": ("handoff",), "discriminate": ("handoff", "actual_locate")}
_LOCATE_HEADER = "Actual locate output"
_SEED_LOCK = threading.Lock()
RETURN_CONTRACT = (
    '## What to return\n'
    'A JSON object carrying "body" and "commitments". Both are strings and nothing else is required.'
)


class SuccessorError(RuntimeError):
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
class PreparedSuccessor:
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
                "sources": [source.summary() for source in self.source_files]}


def _content(*, handoff_text: str, stage_instructions: Mapping[str, str],
             system_message: str, max_tokens: int) -> dict[str, Any]:
    values = {"handoff_text": handoff_text, "system_message": system_message}
    if any(type(value) is not str or not value.strip() for value in values.values()):
        raise ValueError("SUCCESSOR_NONEMPTY_MATERIAL_REQUIRED")
    if type(max_tokens) is not int or max_tokens < 1:
        raise ValueError("SUCCESSOR_POSITIVE_COMPLETION_CAP_REQUIRED")
    if (not isinstance(stage_instructions, Mapping) or set(stage_instructions) != set(STAGES)
            or any(type(stage_instructions[stage]) is not str or not stage_instructions[stage].strip()
                   for stage in STAGES)):
        raise ValueError("SUCCESSOR_EXACT_STAGE_INSTRUCTIONS_REQUIRED")
    return {**values, "stage_instructions": dict(stage_instructions), "max_tokens": max_tokens}


def _stage_ports(content: Mapping[str, Any], stage: str) -> tuple[str, ...]:
    return _STAGE_PORTS[stage]


def _source_files(content: Mapping[str, Any]) -> tuple[SourceFile, ...]:
    return tuple(SourceFile(source_id, path, content[field].encode("utf-8"))
                 for field, source_id, path, _, _, _ in _SOURCE_SPECS)


def _manifest_bytes(manifest: dict[str, Any]) -> bytes:
    return (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _copy_source(context: MachineContext) -> str:
    spec = next((spec for spec in _SOURCE_SPECS if spec[3] == context.stage.kind_id), None)
    sources = [source for source in context.plan.sources if spec and source.source_id == spec[1]]
    if spec is None or len(sources) != 1:
        raise SuccessorError("SUCCESSOR_SOURCE_BINDING_MISSING", "Seed lacks its unique frozen source")
    raw = sources[0].raw.decode("utf-8")
    if not raw.strip():
        raise SuccessorError("SUCCESSOR_SOURCE_EMPTY", "Frozen handoff must be nonempty")
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
                    kind_id, "Copy the exact frozen handoff source", _copy_source))
            else:
                if seat.answer is not _copy_source:
                    raise SuccessorError("SUCCESSOR_SEED_REGISTRY_MISMATCH", "Another seed handler is registered")


def make_manifest(**material: Any) -> dict[str, Any]:
    content = _content(**material)

    def kind(kind_id: str, title: str, instruction: str, ports: tuple[str, ...]) -> dict[str, Any]:
        return {"kind_id": kind_id, "title": title, "instruction": instruction,
                "commitment_call": "single",
                "input_ports": [{"port_id": name, "port_type": name, "window": "this_cycle"} for name in ports],
                "output_port": {"port_id": "out", "produces_kind": kind_id},
                "failure_policy": {"retries": 0, "tolerance": 0, "action": "stop"}}

    seeds = [kind(kind_id, "Frozen material: " + source_id,
                  "Copy the exact frozen UTF-8 handoff source.", ())
             for _, source_id, _, kind_id, _, _ in _SOURCE_SPECS]
    models = [kind(_STAGE_KINDS[stage], title, content["stage_instructions"][stage], _stage_ports(content, stage))
              for stage, title in (("locate", "Locate the candidate issue in its actual sources"),
                                   ("discriminate", "Discriminate the live readings (terminal kind is transport only)"))]
    ports = [(port, kind_id, header) for _, _, _, kind_id, port, header in _SOURCE_SPECS]
    ports.append(("actual_locate", LOCATE, _LOCATE_HEADER))
    seed_stages = [{"stage_id": "seed_" + source_id, "kind_id": kind_id, "seat": "machine", "ports": []}
                   for _, source_id, _, kind_id, _, _ in _SOURCE_SPECS]
    return {"schema_version": "creib.mini.manifest.v1",
            "manifest_id": "minireason.successor.v1." + digest(content)[:24],
            "problem": "Locate and discriminate the issue in a whole verified handoff; no automatic promotion, standing or installation.",
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


def _validate_prepared(prepared: PreparedSuccessor, content: dict[str, Any]) -> None:
    expected = make_manifest(**content)
    if (prepared.material_digest != digest(content) or prepared.manifest != expected
            or prepared.manifest_bytes != _manifest_bytes(expected)
            or prepared.source_files != _source_files(content)):
        raise SuccessorError("SUCCESSOR_PREPARED_MATERIAL_MISMATCH", "Prepared material or manifest changed")
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
        raise SuccessorError("SUCCESSOR_PREPARED_PLAN_MISMATCH", "Compiled plan no longer binds the prepared route and sources")
    _ensure_seed_seats()


def _archive_prepared(root: Path, prepared: PreparedSuccessor) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for path, raw in [(root / source.path, source.raw) for source in prepared.source_files] + [
            (root / "manifest.json", prepared.manifest_bytes)]:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            if path.read_bytes() != raw:
                raise SuccessorError("SUCCESSOR_ARCHIVE_MISMATCH", "Existing archive differs from prepared bytes")
        else:
            with path.open("xb") as handle:
                handle.write(raw)
    bindings = root / "material-bindings.json"
    if bindings.exists():
        if json.loads(bindings.read_text()) != prepared.summary():
            raise SuccessorError("SUCCESSOR_ARCHIVE_MISMATCH", "Existing material bindings differ")
    else:
        write_new(bindings, prepared.summary())


def prepare_successor(root: Path, **material: Any) -> PreparedSuccessor:
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
    prepared = PreparedSuccessor(manifest, plan, digest(content), manifest_bytes, source_files, digest(plan.header))
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
            raise SuccessorError("SUCCESSOR_COORDINATE_INVALID", "Unexpected stage, cycle, kind or phase")
        if (request.cycle, request.stage_id) in self.answers:
            raise SuccessorError("SUCCESSOR_DUPLICATE_STAGE", "Each model stage may run only once")
        kind = next(kind for kind in self.manifest["kinds"] if kind["kind_id"] == request.kind_id)
        sections = [re.escape("# " + kind["title"]), re.escape(kind["instruction"])]
        history = []
        visible_sources = []
        for entry in kind["input_ports"]:
            name = entry["port_id"]
            source_spec = next((spec for spec in _SOURCE_SPECS if spec[4] == name), None)
            if source_spec is not None:
                field, _, _, source_kind, _, header = source_spec
                raw = self.material[field]
                visible_sources.append(field)
            else:
                if name != "actual_locate" or request.stage_id != "discriminate":
                    raise SuccessorError("SUCCESSOR_ROUTING_MISMATCH", "Unexpected history port")
                source_kind, header = LOCATE, _LOCATE_HEADER
                raw = self.answers.get((request.cycle, "locate"))
                if raw is None:
                    raise SuccessorError("SUCCESSOR_HISTORY_MISSING", "The actual locate output was not obtained")
                history.append({"stage": "locate", "text": raw})
            sections.append(re.escape(f"## {header} ({name})\n[") + r"[0-9a-f]{16}"
                            + re.escape(f"] ({source_kind})\n" + raw))
        sections.append(re.escape(RETURN_CONTRACT))
        if re.fullmatch(r"\n\n".join(sections), request.brief) is None:
            raise SuccessorError("SUCCESSOR_ROUTING_MISMATCH", "Mini delivered missing, changed or additional material")
        from .successor_study import stage_prompt, validate_response
        prompt = stage_prompt(self.material, request.stage_id, history)
        exposure = {"stage": request.stage_id, "cycle": request.cycle,
                    "mini_brief_sha256": hashlib.sha256(request.brief.encode()).hexdigest(),
                    "sent_prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                    "mini_brief": request.brief, "sent_prompt": prompt,
                    "transport_transformation": "Verify complete routed brief, then use the shared direct stage renderer",
                    "complete_routed_brief_verified": True,
                    "whole_handoff_port_visible": True,
                    "actual_locate_port_visible": request.stage_id == "discriminate",
                    "source_fields_visible": visible_sources,
                    "history_stages_visible": [row["stage"] for row in history],
                    "terminal_kind_is_transport_only": request.stage_id == "discriminate"}
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


def run_successor(provider: Any, root: Path, prepared: PreparedSuccessor | None = None,
                   **material: Any) -> dict[str, Any]:
    """Execute exactly locate/discriminate, retaining partial artifacts on failure."""
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    content = _content(**material)
    manifest = make_manifest(**content)
    result: dict[str, Any] = {"schema": "minireason.successor-mini.v1", "status": "RUNNING",
                             "history": [], "final": None, "mini_outcome": None, "alarms": [],
                             "manifest_sha256": hashlib.sha256(_manifest_bytes(manifest)).hexdigest(),
                             "visibility": [], "interpretation_status": "NOT_ADJUDICATED",
                             "transport": "Raw prose duplicated in host body/commitments wrapper; ports render body only",
                             "standing_effect": "none", "installation_policy": "none",
                             "automatic_successor_started": False,
                             "terminal_kind": {"kind_id": DISCRIMINATE, "stage": "discriminate", "transport_only": True,
                                               "semantic_verdict": False}}
    write_new(root / "successor-started.json", result)
    responder = _ProseResponder(provider, root / "requests", manifest, content)
    compiled = None
    try:
        if provider.settings.max_tokens != content["max_tokens"]:
            raise SuccessorError("SUCCESSOR_COMPLETION_CAP_MISMATCH", "Provider ceiling differs from frozen manifest")
        if prepared is None:
            prepared = prepare_successor(root, **content)
        else:
            _validate_prepared(prepared, content)
            _archive_prepared(root, prepared)
        compiled = prepared.plan
        result["prepared_bindings"] = prepared.summary()
        outcome = run_mini(compiled, root / "run", responder,
                           responder_id="deepseek:" + provider.settings.model, endpoint=provider.settings)
        result["mini_outcome"] = {**asdict(outcome), "root": "run", "stages_entered": list(outcome.stages_entered)}
        if outcome.cycles_completed != 1 or outcome.calls != 2:
            raise SuccessorError("SUCCESSOR_ROUTE_INCOMPLETE", "Both model stages must complete exactly once")
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
                    raise SuccessorError("SUCCESSOR_ARTIFACT_MISMATCH", "Stored artifact differs from actual provider prose")
                row = {"stage": stage, "cycle": artifact["cycle"], "artifact_id": artifact_id,
                       "text": raw, "text_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                       "answer": {"body": raw, "commitments": raw}, "proposed_changes_installed": False,
                       "semantic_verdict": False}
                result["history"].append(row)
                if stage == "discriminate":
                    result["final"] = row["answer"]
            for line in log_path.read_text().splitlines():
                event = json.loads(line)
                if event["type"] in {"FORMAT_FAILURE", "REFUSED", "SUBMISSION_DROPPED", "BUDGET_REFUSED", "PORT_EMPTY"}:
                    result["alarms"].append({"code": event["type"], "event_id": event["event_id"],
                                             "stage": event["stage_id"], "payload": event["payload"]})
        except Exception as error:
            result["alarms"].append({"code": getattr(error, "code", "SUCCESSOR_LOG_UNREADABLE"), "detail": str(error)})
    if result["status"] == "COMPLETE" and [row["stage"] for row in result["history"]] != list(STAGES):
        result["alarms"].append({"code": "SUCCESSOR_HISTORY_INCOMPLETE", "detail": "Expected exactly locate/discriminate artifacts"})
    if result["alarms"]:
        result["status"] = "OPERATIONAL_FAILURE"
    write_new(root / "successor-result.json", result)
    write_new(root / "successor-errata.json", {"operational": result["alarms"],
              "content_appraisal": "No automatic bearing, adequacy, creativity or success verdict"})
    return result
