"""Mini adapter for frozen-issue constructive inquiry.

Adapted from the calibrated frozen source-artifact route in language_mini.py.
Four model calls construct, criticize, revise and propose a successor question.
Every stage receives the full frozen material; no semantic admission gate,
standing update, inferred answer edge or language installation is performed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import re
import threading
from typing import Any, Mapping

from creib.forge.mini.executor import Reply, Request
from creib.forge.mini.log import BlobStore, replay
from creib.forge.mini.manifest import RunPlan, compile_manifest
from creib.forge.mini.machines import MachineContext, MachineSeat, register_machine_seat, resolve_machine_seat
from creib.forge.mini.common import MiniError
from creib.forge.mini.runner import run_mini

from minireason.provider import digest, write_new
from minireason.language_data import RAW_SYSTEM

CONSTRUCTION = "minireason.inquiry-construction.v1"
CRITICISM = "minireason.inquiry-criticism.v1"
REVISION = "minireason.inquiry-revision.v1"
PROMOTION = "mini.verdict.v1"
STAGES = ("construct", "criticize", "revise", "promote")
_STAGE_KINDS = dict(zip(STAGES, (CONSTRUCTION, CRITICISM, REVISION, PROMOTION)))
_ARTIFACT_PORTS = (
    ("construct", CONSTRUCTION, "construction", "Actual construction"),
    ("criticize", CRITICISM, "criticism", "Actual criticism"),
    ("revise", REVISION, "revision", "Actual proposed revision"),
)
_SOURCE_SPECS = (
    ("packet_text", "inquiry_packet", "sources/packet.txt", "minireason.inquiry-packet.v1", "packet", "Frozen shared packet"),
    ("selected_language_text", "inquiry_language", "sources/selected-language.txt", "minireason.inquiry-language.v1", "meaning", "Selected language meaning"),
    ("issue_text", "inquiry_issue", "sources/issue.txt", "minireason.inquiry-issue.v1", "issue", "Frozen selected issue"),
    ("parent_material_text", "inquiry_parents", "sources/parents.txt", "minireason.inquiry-parents.v1", "parents", "Frozen parent material"),
)
_SEED_LOCK = threading.Lock()
RETURN_CONTRACT = ('## What to return\n'
                   'A JSON object carrying "body" and "commitments". Both are strings and nothing else is required.')

class InquiryError(RuntimeError):
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
                "sha256": hashlib.sha256(self.raw).hexdigest(), "utf8_bytes": len(self.raw),
                "characters": len(self.raw.decode("utf-8"))}


@dataclass(frozen=True)
class PreparedInquiry:
    """Compiled once, with exact material files available to each isolated arm."""
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


def _content(*, packet_text: str, selected_language_text: str, issue_text: str,
             parent_material_text: str, carrier_directive: str,
             stage_instructions: Mapping[str, str], max_tokens: int) -> dict[str, Any]:
    for name, value in (("packet_text", packet_text), ("selected_language_text", selected_language_text),
                        ("issue_text", issue_text), ("parent_material_text", parent_material_text),
                        ("carrier_directive", carrier_directive)):
        if type(value) is not str or not value:
            raise ValueError(f"{name} must be nonempty text; missing material requires an explicit occurrence")
    if type(max_tokens) is not int or max_tokens < 1:
        raise ValueError("max_tokens must be a positive integer")
    if any(type(stage_instructions.get(stage)) is not str or not stage_instructions[stage]
           for stage in STAGES):
        raise ValueError("Every stage needs a nonempty instruction")
    return {"packet_text": packet_text, "selected_language_text": selected_language_text,
            "issue_text": issue_text, "parent_material_text": parent_material_text,
            "carrier_directive": carrier_directive, "stage_instructions": dict(stage_instructions),
            "max_tokens": max_tokens}


def _source_files(content: Mapping[str, Any]) -> tuple[SourceFile, ...]:
    return tuple(SourceFile(source_id, path, content[field].encode("utf-8"))
                 for field, source_id, path, _, _, _ in _SOURCE_SPECS if content[field])


def _manifest_bytes(manifest: dict[str, Any]) -> bytes:
    return (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _copy_source(context: MachineContext) -> str:
    """Copy one named frozen source, without model work or content appraisal."""
    source_id = next((source_id for _, source_id, _, kind_id, _, _ in _SOURCE_SPECS
                      if kind_id == context.stage.kind_id), None)
    sources = [source for source in context.plan.sources if source.source_id == source_id]
    if source_id is None or len(sources) != 1:
        raise InquiryError("INQUIRY_SOURCE_BINDING_MISSING", "The seed has no unique frozen source")
    raw = sources[0].raw.decode("utf-8")
    if not raw:
        raise InquiryError("INQUIRY_SOURCE_EMPTY", "An optional empty source must not be seeded")
    return json.dumps({"body": raw, "commitments": raw}, ensure_ascii=False)


def _ensure_seed_seats() -> None:
    # Register before concurrent arms begin; never replace an existing handler.
    with _SEED_LOCK:
        for _, _, _, kind_id, _, _ in _SOURCE_SPECS:
            try:
                seat = resolve_machine_seat(kind_id)
            except MiniError as error:
                if error.code != "MINI_MACHINE_SEAT_UNKNOWN":
                    raise
                register_machine_seat(MachineSeat(kind_id, "Copy exact frozen UTF-8 source; no model or judgment", _copy_source))
            else:
                if seat.answer is not _copy_source:
                    raise InquiryError("INQUIRY_SEED_REGISTRY_MISMATCH", "A different source-seed implementation is registered")


def make_manifest(*, packet_text: str, selected_language_text: str, issue_text: str,
                  parent_material_text: str, carrier_directive: str,
                  stage_instructions: Mapping[str, str], max_tokens: int) -> dict[str, Any]:
    """Four calls and complete frozen sources, without installing proposals."""
    content = _content(packet_text=packet_text, selected_language_text=selected_language_text,
                       issue_text=issue_text, parent_material_text=parent_material_text,
                       carrier_directive=carrier_directive, stage_instructions=stage_instructions,
                       max_tokens=max_tokens)
    instructions = {stage: stage_instructions[stage] + "\n\n## Selected carrier\n" + carrier_directive
                    for stage in STAGES}

    def kind(kind_id: str, instruction: str, title: str, ports: list[str]) -> dict[str, Any]:
        return {"kind_id": kind_id, "title": title, "instruction": instruction,
                "commitment_call": "single",
                "input_ports": [{"port_id": name, "port_type": name, "window": "this_cycle"} for name in ports],
                "output_port": {"port_id": "out", "produces_kind": kind_id},
                "failure_policy": {"retries": 0, "tolerance": 0, "action": "stop"}}

    seeds = [kind(kind_id, "Copy the named frozen source unchanged; do not interpret or judge it.",
                  "Frozen material: " + source_id, []) for _, source_id, _, kind_id, _, _ in _SOURCE_SPECS]
    source_ports = [spec[4] for spec in _SOURCE_SPECS]
    titles = ("Construct in response to the frozen issue", "Criticize the actual construction",
              "Propose a response to the criticism", "Propose a successor question or suspension")
    models = [kind(_STAGE_KINDS[stage], instructions[stage], titles[index],
                   source_ports + [spec[2] for spec in _ARTIFACT_PORTS[:index]])
              for index, stage in enumerate(STAGES)]
    ports = [(port, kind_id, header) for _, _, _, kind_id, port, header in _SOURCE_SPECS]
    ports += [(port, kind_id, header) for _, kind_id, port, header in _ARTIFACT_PORTS]
    stages = [{"stage_id": "seed_" + source_id, "kind_id": spec["kind_id"], "seat": "machine", "ports": []}
              for (_, source_id, _, _, _, _), spec in zip(_SOURCE_SPECS, seeds)]
    stages += [{"stage_id": stage, "kind_id": spec["kind_id"],
                "ports": [entry["port_id"] for entry in spec["input_ports"]]}
               for stage, spec in zip(STAGES, models)]
    return {"schema_version": "creib.mini.manifest.v1",
            "manifest_id": "minireason.frozen-issue-inquiry.v1." + digest(content)[:24],
            "problem": "Investigate the frozen issue through declared material ports; promotion allocates inquiry and establishes no standing.",
            "sources": [{"source_id": source.source_id, "path": source.path} for source in _source_files(content)],
            "kinds": seeds + models,
            "port_types": [{"port_type": name, "draws_from": {"artifact_kinds": [kind_id]},
                            "render": {"rule": "list_bodies", "header": header}}
                           for name, kind_id, header in ports],
            "stages": stages + [{"stage_id": "end", "end": True}],
            "cycles": {"max_cycles": 1, "max_calls": 4,
                       "completion_tokens_per_call": max_tokens,
                       "max_completion_tokens": 4 * max_tokens}}


def _archive_prepared(root: Path, prepared: PreparedInquiry) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for source in prepared.source_files:
        path = root / source.path
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(source.raw)
    with (root / "manifest.json").open("xb") as handle:
        handle.write(prepared.manifest_bytes)
    write_new(root / "material-bindings.json", prepared.summary())


def _validate_prepared(prepared: PreparedInquiry, content: dict[str, Any]) -> None:
    expected = make_manifest(**content)
    if (prepared.material_digest != digest(content)
            or prepared.manifest != expected or prepared.manifest_bytes != _manifest_bytes(expected)
            or prepared.source_files != _source_files(content)):
        raise InquiryError("INQUIRY_PREPARED_MATERIAL_MISMATCH", "Prepared manifest or source bytes differ from this frozen probe")
    if (prepared.plan.manifest_digest != hashlib.sha256(prepared.manifest_bytes).hexdigest()
            or digest(prepared.plan.header) != prepared.plan_header_digest
            or [(source.source_id, source.raw) for source in prepared.plan.sources]
            != [(source.source_id, source.raw) for source in prepared.source_files]):
        raise InquiryError("INQUIRY_PREPARED_PLAN_MISMATCH", "Compiled plan no longer binds the exact prepared source bytes")
    _ensure_seed_seats()


def prepare_inquiry(root: Path, *, packet_text: str, selected_language_text: str,
                    issue_text: str, parent_material_text: str, carrier_directive: str,
                    stage_instructions: Mapping[str, str], max_tokens: int) -> PreparedInquiry:
    """Retain exact material and compile before constructing any provider.

    The experiment runner owns a failed preflight's terminal record and errata.
    """
    content = _content(packet_text=packet_text, selected_language_text=selected_language_text,
                       issue_text=issue_text, parent_material_text=parent_material_text,
                       carrier_directive=carrier_directive, stage_instructions=stage_instructions,
                       max_tokens=max_tokens)
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
    prepared = PreparedInquiry(manifest, plan, digest(content), manifest_bytes, source_files, digest(plan.header))
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
                  {"stage": request.stage_id, "cycle": request.cycle,
                   "mini_brief": request.brief,
                   "mini_brief_sha256": hashlib.sha256(request.brief.encode()).hexdigest(),
                   "sent_to_provider": "Only if subsequent route validation succeeds"})
        if request.stage_id not in STAGES or request.phase != "both" or request.cycle != 1:
            raise InquiryError("INQUIRY_COORDINATE_INVALID", "Unexpected stage or two-call phase")
        if request.kind_id != _STAGE_KINDS[request.stage_id]:
            raise InquiryError("INQUIRY_COORDINATE_INVALID", "Unexpected kind for this stage")
        # Validate the complete actual Mini brief, not a mere substring assertion.
        # Only content-addressed artifact identifiers are variable framing.
        kind = next(k for k in self.manifest["kinds"] if k["kind_id"] == request.kind_id)
        sections = [re.escape("# " + kind["title"]), re.escape(kind["instruction"])]
        history = []
        for entry in kind["input_ports"]:
            name = entry["port_id"]
            source_spec = next((spec for spec in _SOURCE_SPECS if spec[4] == name), None)
            if source_spec is not None:
                field, _, _, source_kind, _, header = source_spec
                raw = self.material[field]
            else:
                preceding, source_kind, _, header = next(spec for spec in _ARTIFACT_PORTS if spec[2] == name)
                raw = self.answers.get((request.cycle, preceding))
                if raw is None:
                    raise InquiryError("INQUIRY_HISTORY_MISSING", "A declared prior response was not obtained")
                history.append({"stage": preceding, "text": raw})
            sections.append(re.escape(f"## {header} ({name})\n[") + r"[0-9a-f]{16}" +
                            re.escape(f"] ({source_kind})\n" + raw))
        sections.append(re.escape(RETURN_CONTRACT))
        if re.fullmatch(r"\n\n".join(sections), request.brief) is None:
            raise InquiryError("INQUIRY_ROUTING_MISMATCH", "Mini delivered unexpected, missing or changed stage material")
        # The direct comparator owns this same pure stage renderer. Lazy import
        # avoids importing its CLI while constructing the Mini manifest.
        from .inquiry_study import stage_prompt, validate_response
        prompt = stage_prompt(self.material, request.stage_id, history)
        exposure = {"stage": request.stage_id, "cycle": request.cycle,
                    "mini_brief_sha256": hashlib.sha256(request.brief.encode()).hexdigest(),
                    "sent_prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                    "mini_brief": request.brief, "sent_prompt": prompt,
                    "transport_transformation": "Validate complete routed brief, then use direct comparator stage renderer",
                    "complete_routed_brief_verified": True,
                    "source_packet_port_visible": True, "all_frozen_source_ports_visible": True}
        write_new(self.records / f"{request.cycle:03d}-{request.stage_id}.json", exposure)
        self.visibility.append({key: value for key, value in exposure.items()
                                if key not in {"mini_brief", "sent_prompt"}})
        response = self.provider.complete([
            {"role": "system", "content": RAW_SYSTEM},
            {"role": "user", "content": prompt}], json_output=False,
            coordinate={"stage": request.stage_id, "cycle": request.cycle,
                        "phase": "raw-prose", "mini_kind": request.kind_id})
        raw = validate_response(response, self.completion_cap)
        # Mini requires both fields nonempty. Duplication is transport only, not extraction of semantic commitments.
        wrapped = json.dumps({"body": raw, "commitments": raw}, ensure_ascii=False)
        self.answers[request.cycle, request.stage_id] = raw
        write_new(self.records / f"{request.cycle:03d}-{request.stage_id}-transport.json",
                  {"raw_text_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                   "raw_utf8_bytes": len(raw.encode()), "wrapped_utf8_bytes": len(wrapped.encode()),
                   "wrapper_is_host_generated": True, "independent_commitment_call": False,
                   "wrapper_tokens": None, "wrapper_token_note": "Host serialization is not model output; no tokenizer estimate is made",
                   "provider_completion_tokens": response["usage"]["completion_tokens"]})
        return Reply(wrapped, response["usage"]["prompt_tokens"], response["usage"]["completion_tokens"])


def run_inquiry(provider: Any, root: Path, *, packet_text: str, selected_language_text: str,
                issue_text: str, parent_material_text: str, carrier_directive: str,
                stage_instructions: Mapping[str, str], max_tokens: int,
                prepared: PreparedInquiry | None = None) -> dict[str, Any]:
    """Run the actual four-stage Mini episode, retaining all partial artifacts."""
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    content = _content(packet_text=packet_text, selected_language_text=selected_language_text,
                       issue_text=issue_text, parent_material_text=parent_material_text,
                       carrier_directive=carrier_directive, stage_instructions=stage_instructions,
                       max_tokens=max_tokens)
    manifest = make_manifest(**content)
    result: dict[str, Any] = {"schema": "minireason.inquiry-mini.v1", "status": "RUNNING",
                              "history": [], "final": None, "mini_outcome": None, "alarms": [],
                              "manifest_sha256": hashlib.sha256(_manifest_bytes(manifest)).hexdigest(), "visibility": [],
                              "interpretation_status": "NOT_ADJUDICATED",
                              "transport": "Raw prose stored identically in body and commitments; duplication is transport only and ports render body alone",
                              "standing_effect": "NONE",
                              "installation_policy": "Proposed language or issue amendments remain proposals; initial sources stay frozen"}
    write_new(root / "inquiry-started.json", result)
    material = content
    responder = _ProseResponder(provider, root / "requests", manifest, material)
    compiled = None
    try:
        if provider.settings.max_tokens != max_tokens:
            raise InquiryError("INQUIRY_COMPLETION_CAP_MISMATCH", "Provider ceiling differs from frozen manifest")
        if prepared is None:
            prepared = prepare_inquiry(root, **content)
        else:
            _validate_prepared(prepared, content)
            _archive_prepared(root, prepared)
        compiled = prepared.plan
        result["prepared_bindings"] = prepared.summary()
        outcome = run_mini(compiled, root / "run", responder,
                           responder_id="deepseek:" + provider.settings.model, endpoint=provider.settings)
        result["mini_outcome"] = {**asdict(outcome), "root": "run", "stages_entered": list(outcome.stages_entered)}
        if outcome.cycles_completed != 1 or outcome.calls != 4:
            raise InquiryError("INQUIRY_ROUTE_INCOMPLETE", "Declared stages did not complete exactly once per cycle")
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
            for key in state.artifact_order:
                artifact = state.artifacts[key]
                kind_id = artifact["kind_id"]
                if kind_id not in set(_STAGE_KINDS.values()):
                    continue
                raw = blobs.get(artifact["body_ref"]).decode("utf-8")
                stage = next(stage for stage, stage_kind in _STAGE_KINDS.items() if stage_kind == kind_id)
                row = {"stage": stage, "cycle": artifact["cycle"], "artifact_id": key,
                       "text": raw, "text_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                       "answer": {"body": raw, "commitments": raw}, "proposed_changes_installed": False}
                result["history"].append(row)
                if stage == "promote":
                    result["final"] = row["answer"]
            for line in log_path.read_text().splitlines():
                event = json.loads(line)
                if event["type"] in {"FORMAT_FAILURE", "REFUSED", "SUBMISSION_DROPPED", "BUDGET_REFUSED", "PORT_EMPTY"}:
                    result["alarms"].append({"code": event["type"], "event_id": event["event_id"],
                                               "stage": event["stage_id"], "payload": event["payload"]})
        except Exception as error:
            result["alarms"].append({"code": "INQUIRY_LOG_UNREADABLE", "detail": str(error)})
    if result["alarms"]:
        result["status"] = "OPERATIONAL_FAILURE"
    write_new(root / "inquiry-result.json", result)
    write_new(root / "inquiry-errata.json", {"operational": result["alarms"],
                                            "content_appraisal": "No automatic adequacy, truth, Lean or creativity verdict; promotion does not establish bearing"})
    return result
