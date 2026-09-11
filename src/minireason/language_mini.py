"""Mini routing for frozen express/reinterpret/criticize probes.

The raw model answer is prose. A transparent adapter wraps it in Mini's transport
artifact with the same raw text in both fields; no compiler or semantic admission gate
is applied. The full source packet travels through a deterministic seed artifact
port that the reinterpretation stage never declares. An expression or source-conditioned language may still carry
source information: withholding the source port is not information independence.
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

from .provider import digest, write_new
from .language_data import RAW_SYSTEM

EXPRESSION = "minireason.language-expression.v1"
READING = "minireason.language-reading.v1"
CRITICISM = "mini.verdict.v1"
STAGES = ("express", "reinterpret", "criticize")
PACKET = "minireason.frozen-packet.v1"
LANGUAGE = "minireason.frozen-language.v1"
COMPILER = "minireason.compiler-observation.v1"
_SOURCE_SPECS = (
    ("packet_text", "frozen_packet", "sources/packet.txt", PACKET, "packet", "Frozen shared packet"),
    ("selected_language_text", "selected_language", "sources/selected-language.txt", LANGUAGE, "meaning", "Selected language meaning"),
    ("compiler_text", "compiler_observation", "sources/compiler.txt", COMPILER, "compiler", "External compiler observation"),
)
_SEED_LOCK = threading.Lock()
RETURN_CONTRACT = ('## What to return\n'
                   'A JSON object carrying "body" and "commitments". Both are strings and nothing else is required.')

class LanguageProbeError(RuntimeError):
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
class PreparedProbe:
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


def _content(*, packet_text: str, selected_language_text: str, carrier_directive: str,
             stage_instructions: Mapping[str, str], max_tokens: int,
             cycles: int = 1, compiler_text: str = "") -> dict[str, Any]:
    if type(packet_text) is not str or not packet_text:
        raise ValueError("A nonempty frozen packet is required")
    for name, value in (("selected_language_text", selected_language_text),
                        ("carrier_directive", carrier_directive), ("compiler_text", compiler_text)):
        if type(value) is not str:
            raise ValueError(f"{name} must be text")
    if type(cycles) is not int or not 1 <= cycles <= 20:
        raise ValueError("cycles must be an integer between 1 and 20")
    if type(max_tokens) is not int or max_tokens < 1:
        raise ValueError("max_tokens must be a positive integer")
    if any(type(stage_instructions.get(stage)) is not str or not stage_instructions[stage]
           for stage in STAGES):
        raise ValueError("Every stage needs a nonempty instruction")
    return {"packet_text": packet_text, "selected_language_text": selected_language_text,
            "carrier_directive": carrier_directive, "stage_instructions": dict(stage_instructions),
            "compiler_text": compiler_text, "cycles": cycles, "max_tokens": max_tokens}


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
        raise LanguageProbeError("PROBE_SOURCE_BINDING_MISSING", "The seed has no unique frozen source")
    raw = sources[0].raw.decode("utf-8")
    if not raw:
        raise LanguageProbeError("PROBE_SOURCE_EMPTY", "An optional empty source must not be seeded")
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
                    raise LanguageProbeError("PROBE_SEED_REGISTRY_MISMATCH", "A different source-seed implementation is registered")


def make_manifest(*, packet_text: str, selected_language_text: str, carrier_directive: str,
                  stage_instructions: Mapping[str, str], max_tokens: int,
                  cycles: int = 1, compiler_text: str = "") -> dict[str, Any]:
    """Build short instructions and lossless file-backed source-artifact routes.

    Write the sidecars and compile with ``prepare_probe`` before dispatching any
    experiment arm. Three model calls follow deterministic source-copy stages
    each cycle; repeat cycles do not install changes or consume earlier replies.
    """
    content = _content(packet_text=packet_text, selected_language_text=selected_language_text,
                       carrier_directive=carrier_directive, stage_instructions=stage_instructions,
                       max_tokens=max_tokens, cycles=cycles, compiler_text=compiler_text)
    instructions = {stage: stage_instructions[stage] + "\n\n## Selected carrier\n" + carrier_directive
                    for stage in STAGES}

    def kind(kind_id: str, instruction: str, title: str, ports: list[str]) -> dict[str, Any]:
        return {"kind_id": kind_id, "title": title, "instruction": instruction,
                "commitment_call": "single",
                "input_ports": [{"port_id": name, "port_type": name, "window": "this_cycle"} for name in ports],
                "output_port": {"port_id": "out", "produces_kind": kind_id},
                "failure_policy": {"retries": 0, "tolerance": 0, "action": "stop"}}

    sources = [spec for spec in _SOURCE_SPECS if content[spec[0]]]
    seeds = [kind(kind_id, "Copy the named frozen source unchanged; do not interpret or judge it.",
                  "Frozen material: " + source_id, []) for _, source_id, _, kind_id, _, _ in sources]
    models = [kind(EXPRESSION, instructions["express"], "Express the frozen material", ["packet"]),
              kind(READING, instructions["reinterpret"], "Reinterpret the actual expression",
                   (["meaning"] if selected_language_text else []) + ["expression"]),
              kind(CRITICISM, instructions["criticize"], "Criticize the expression and reading",
                   ["packet", "expression", "reading"] + (["compiler"] if compiler_text else []))]
    ports = [(port, kind_id, header) for _, _, _, kind_id, port, header in sources]
    ports += [("expression", EXPRESSION, "Actual expression"), ("reading", READING, "Independent reading")]
    stages = [{"stage_id": "seed_" + source_id, "kind_id": spec["kind_id"], "seat": "machine", "ports": []}
              for (_, source_id, _, _, _, _), spec in zip(sources, seeds)]
    stages += [{"stage_id": stage, "kind_id": spec["kind_id"],
                "ports": [entry["port_id"] for entry in spec["input_ports"]]}
               for stage, spec in zip(STAGES, models)]
    return {"schema_version": "creib.mini.manifest.v1",
            "manifest_id": "minireason.language-probe.v2." + digest(content)[:24],
            "problem": "Study the frozen material through the declared source-artifact ports; no semantic verdict is implied.",
            "sources": [{"source_id": source.source_id, "path": source.path} for source in _source_files(content)],
            "kinds": seeds + models,
            "port_types": [{"port_type": name, "draws_from": {"artifact_kinds": [kind_id]},
                            "render": {"rule": "list_bodies", "header": header}}
                           for name, kind_id, header in ports],
            "stages": stages + [{"stage_id": "end", "end": True}],
            "cycles": {"max_cycles": cycles, "max_calls": 3 * cycles,
                       "completion_tokens_per_call": max_tokens,
                       "max_completion_tokens": 3 * cycles * max_tokens}}


def _archive_prepared(root: Path, prepared: PreparedProbe) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for source in prepared.source_files:
        path = root / source.path
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(source.raw)
    with (root / "manifest.json").open("xb") as handle:
        handle.write(prepared.manifest_bytes)
    write_new(root / "material-bindings.json", prepared.summary())


def _validate_prepared(prepared: PreparedProbe, content: dict[str, Any]) -> None:
    expected = make_manifest(**content)
    if (prepared.material_digest != digest(content)
            or prepared.manifest != expected or prepared.manifest_bytes != _manifest_bytes(expected)
            or prepared.source_files != _source_files(content)):
        raise LanguageProbeError("PROBE_PREPARED_MATERIAL_MISMATCH", "Prepared manifest or source bytes differ from this frozen probe")
    if (prepared.plan.manifest_digest != hashlib.sha256(prepared.manifest_bytes).hexdigest()
            or digest(prepared.plan.header) != prepared.plan_header_digest
            or [(source.source_id, source.raw) for source in prepared.plan.sources]
            != [(source.source_id, source.raw) for source in prepared.source_files]):
        raise LanguageProbeError("PROBE_PREPARED_PLAN_MISMATCH", "Compiled plan no longer binds the exact prepared source bytes")
    _ensure_seed_seats()


def prepare_probe(root: Path, *, packet_text: str, selected_language_text: str,
                  carrier_directive: str, stage_instructions: Mapping[str, str], max_tokens: int,
                  cycles: int = 1, compiler_text: str = "") -> PreparedProbe:
    """Retain exact sidecars and compile once, before any provider is constructed.

    Raises on malformed configuration. The experiment runner owns the failed
    preflight's terminal record and errata; no provider exists at this boundary.
    """
    content = _content(packet_text=packet_text, selected_language_text=selected_language_text,
                       carrier_directive=carrier_directive, stage_instructions=stage_instructions,
                       max_tokens=max_tokens, cycles=cycles, compiler_text=compiler_text)
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
    prepared = PreparedProbe(manifest, plan, digest(content), manifest_bytes, source_files, digest(plan.header))
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
        if request.stage_id not in STAGES or request.phase != "both":
            raise LanguageProbeError("PROBE_COORDINATE_INVALID", "Unexpected stage or two-call phase")
        if request.kind_id != {"express": EXPRESSION, "reinterpret": READING, "criticize": CRITICISM}[request.stage_id]:
            raise LanguageProbeError("PROBE_COORDINATE_INVALID", "Unexpected kind for this stage")
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
                preceding = "express" if name == "expression" else "reinterpret"
                raw = self.answers.get((request.cycle, preceding))
                if raw is None:
                    raise LanguageProbeError("PROBE_HISTORY_MISSING", "A declared prior response was not obtained")
                history.append({"stage": preceding, "text": raw})
                header, source_kind = (("Actual expression", EXPRESSION) if name == "expression"
                                       else ("Independent reading", READING))
            sections.append(re.escape(f"## {header} ({name})\n[") + r"[0-9a-f]{16}" +
                            re.escape(f"] ({source_kind})\n" + raw))
        sections.append(re.escape(RETURN_CONTRACT))
        if re.fullmatch(r"\n\n".join(sections), request.brief) is None:
            raise LanguageProbeError("PROBE_ROUTING_MISMATCH", "Mini delivered unexpected, missing or changed stage material")
        # The direct comparator owns this same pure stage renderer. Lazy import
        # avoids importing its CLI while constructing the Mini manifest.
        from .language_study import stage_prompt
        prompt = stage_prompt(self.material, request.stage_id, history)
        exposure = {"stage": request.stage_id, "cycle": request.cycle,
                    "mini_brief_sha256": hashlib.sha256(request.brief.encode()).hexdigest(),
                    "sent_prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                    "mini_brief": request.brief, "sent_prompt": prompt,
                    "transport_transformation": "Validate complete routed brief, then use direct comparator stage renderer",
                    "complete_routed_brief_verified": True,
                    "source_packet_port_visible": request.stage_id != "reinterpret"}
        write_new(self.records / f"{request.cycle:03d}-{request.stage_id}.json", exposure)
        self.visibility.append({key: value for key, value in exposure.items()
                                if key not in {"mini_brief", "sent_prompt"}})
        response = self.provider.complete([
            {"role": "system", "content": RAW_SYSTEM},
            {"role": "user", "content": prompt}], json_output=False,
            coordinate={"stage": request.stage_id, "cycle": request.cycle,
                        "phase": "raw-prose", "mini_kind": request.kind_id})
        raw = response["content"]
        if type(raw) is not str:
            raise LanguageProbeError("PROBE_RESPONSE_TYPE", "Provider response content is not text")
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


def run_probe(provider: Any, root: Path, *, packet_text: str, selected_language_text: str,
              carrier_directive: str, stage_instructions: Mapping[str, str], max_tokens: int,
              cycles: int = 1, compiler_text: str = "",
              prepared: PreparedProbe | None = None) -> dict[str, Any]:
    """Run actual Mini and retain partial artifacts and all failure signals.

    Return status describes completion of the probe, never semantic adequacy.
    ``root`` may already be a directory but output filenames must be unused.
    Provider transport records are owned by the caller's provider instance.
    """
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    content = _content(packet_text=packet_text, selected_language_text=selected_language_text,
                       carrier_directive=carrier_directive, stage_instructions=stage_instructions,
                       max_tokens=max_tokens, cycles=cycles, compiler_text=compiler_text)
    manifest = make_manifest(**content)
    result: dict[str, Any] = {"schema": "minireason.language-mini.v1", "status": "RUNNING",
                              "history": [], "final": None, "mini_outcome": None, "alarms": [],
                              "manifest_sha256": hashlib.sha256(_manifest_bytes(manifest)).hexdigest(), "visibility": [],
                              "interpretation_status": "NOT_ADJUDICATED",
                              "transport": "Raw prose stored identically in body and commitments; duplication is transport only and ports render body alone",
                              "blinding_limit": "The source packet port is hidden from reinterpretation. The expression and source-conditioned language may carry source information."}
    write_new(root / "probe-started.json", result)
    material = {"packet_text": packet_text, "selected_language_text": selected_language_text,
                "carrier_directive": carrier_directive, "stage_instructions": dict(stage_instructions),
                "compiler_text": compiler_text}
    responder = _ProseResponder(provider, root / "requests", manifest, material)
    compiled = None
    try:
        if provider.settings.max_tokens != max_tokens:
            raise LanguageProbeError("PROBE_COMPLETION_CAP_MISMATCH", "Provider ceiling differs from frozen manifest")
        if prepared is None:
            prepared = prepare_probe(root, **content)
        else:
            _validate_prepared(prepared, content)
            _archive_prepared(root, prepared)
        compiled = prepared.plan
        result["prepared_bindings"] = prepared.summary()
        outcome = run_mini(compiled, root / "run", responder,
                           responder_id="deepseek:" + provider.settings.model, endpoint=provider.settings)
        result["mini_outcome"] = {**asdict(outcome), "root": "run", "stages_entered": list(outcome.stages_entered)}
        if outcome.cycles_completed != cycles or outcome.calls != 3 * cycles:
            raise LanguageProbeError("PROBE_ROUTE_INCOMPLETE", "Declared stages did not complete exactly once per cycle")
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
                if kind_id not in {EXPRESSION, READING, CRITICISM}:
                    continue
                raw = blobs.get(artifact["body_ref"]).decode("utf-8")
                stage = {EXPRESSION: "express", READING: "reinterpret", CRITICISM: "criticize"}[kind_id]
                row = {"stage": stage, "cycle": artifact["cycle"], "artifact_id": key,
                       "text": raw, "text_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                       "answer": {"body": raw, "commitments": raw}, "proposed_changes_installed": False}
                result["history"].append(row)
                if stage == "criticize":
                    result["final"] = row["answer"]
            for line in log_path.read_text().splitlines():
                event = json.loads(line)
                if event["type"] in {"FORMAT_FAILURE", "REFUSED", "SUBMISSION_DROPPED", "BUDGET_REFUSED", "PORT_EMPTY"}:
                    result["alarms"].append({"code": event["type"], "event_id": event["event_id"],
                                               "stage": event["stage_id"], "payload": event["payload"]})
        except Exception as error:
            result["alarms"].append({"code": "PROBE_LOG_UNREADABLE", "detail": str(error)})
    if result["alarms"]:
        result["status"] = "OPERATIONAL_FAILURE"
    write_new(root / "probe-result.json", result)
    write_new(root / "probe-errata.json", {"operational": result["alarms"],
                                            "content_appraisal": "No automatic adequacy, truth, Lean or creativity verdict"})
    return result
