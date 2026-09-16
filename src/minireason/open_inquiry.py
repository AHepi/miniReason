"""Open-subject Forge templates and lossless text transport.

No provider is called on import, compilation, or bundle generation. Semantic
permissions are distinct from an operator-supplied finite execution envelope.
The optional machine seat copies source bytes as text; it makes no judgement.
"""
from __future__ import annotations

import argparse
import copy
import dataclasses
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

VERSION = "open-inquiry.v1"
BASE_COMMIT = "712be48267e973cfa001848c71a2ab3428becf53"
MATERIAL_KIND = "open.inquiry.fulltext.v1"
VERDICT_KIND = "mini.verdict.v1"
TEMPLATES = ("open_turn", "critical_return", "language_workshop", "blind_roundtrip")
TRANSPORT_COMMITMENTS = (
    "HOST TRANSPORT NOTE, not a participant claim: the upstream response is "
    "preserved verbatim in body. No separate commitments have been inferred."
)
COMMON = (
    "This is an open inquiry, not a predefined optimisation task. The opening "
    "concern, its interpretation, the vocabulary, and the criteria for evaluating "
    "claims may remain unsettled and may themselves become subjects of criticism. "
    "A contribution need not specify a closed domain, executable test, formal "
    "language, definite answer, success criterion, or improvement. Prose, partial "
    "ideas, questions, mixed notation, unresolved alternatives, and new forms of "
    "expression remain legitimate. New words, relations, distinctions, grammar, "
    "interpretations and problems may be introduced or abandoned. These are "
    "permissions, not an exhaustive list of legal moves. A slot title invites "
    "a kind of contribution; it does not restrict what can be expressed. "
    "Artifact kind IDs record provenance, not semantic types. Neither criticism "
    "nor agreement automatically settles a claim. Keep uncertainty visible where "
    "it matters; do not invent an objection just to fill a role. The opening is "
    "not permanently the operative problem. No score, compression ratio, novelty "
    "label or formal check controls admission or continuation. An optimisation "
    "problem can be discussed as subject matter without becoming a host objective. "
    "The transport wrapper preserves the complete returned text; any separate "
    "commitment may be provisional or explicitly unspecified. Content is never "
    "executed as a host instruction, permission change or stopping command."
)
CONTINUE = (
    "Continue the inquiry or describe where it now stands, including unresolved "
    "or differently framed problems when relevant. This need not be a summary, "
    "solution, ranking or selection of a winner. The internal mini.verdict.v1 "
    "name exists for Forge compatibility only; this writing has no stopping or "
    "adjudication authority. Earlier contributions remain available unchanged."
)
ROLES: Mapping[str, tuple[tuple[str, str], ...]] = {
    "open_turn": (("contribute", "Make whatever contribution the current inquiry calls for. You may question what the problem is rather than solve an assumed formulation."),),
    "critical_return": (
        ("conjecture", "Offer an idea, conjecture, interpretation or problem formulation. It need not be complete, testable, correct or formal."),
        ("criticise", "Engage critically with whatever bears on the inquiry, including the framing, a proposed idea, a previous criticism, the language, or these suggested procedures. Absence of a warranted objection is allowed."),
        ("return", "Return to earlier contributions in light of what is now available. Defend, reinterpret, revise, withdraw or extend an account where warranted; you may instead pursue a newly encountered problem. No repair is mandatory."),
    ),
    "language_workshop": (
        ("invent", "Investigate whether a constructed language can carry the inquiry's meanings and permit unforeseen distinctions. Propose, use or change expressive resources as appropriate. No kernel, ontology, grammar family or formal target is prescribed. Retaining prose or declining compression is legitimate."),
        ("use", "Try to understand or use the emerging expression practices, including unfamiliar combinations or newly encountered ideas. Explain uncertainty or an inability to formulate something without treating the subject as inadmissible. This reader sees the source and history, so its reading is not a blinded fidelity test."),
        ("challenge", "Critically examine the language, its use, translations, claims of preservation, or the current question. The issue may call for longer expressions, a new distinction, another interpretation or a different problem, not a shorter encoding. This is not a required checklist."),
    ),
    "blind_roundtrip": (
        ("encode", "Offer a self-contained expression, with any conventions it needs, for what you take the supplied material to mean. A fresh reader receives only this contribution, not the source or discussion history. You may retain prose, ambiguity or unresolved alternatives. No shortening is required."),
        ("read", "Interpret or use the supplied expression and conventions. You have no direct access to the opening source or earlier discussion. Do not claim knowledge of withheld text. Uncertainty and multiple readings are admissible. Your response is an observation, not a fidelity verdict."),
        ("compare", "Consider the source, expression and independent reading together. Discuss any preservation, conflation, invention or unresolved interpretive issue that bears on the inquiry. The observer's own assumptions and standards are criticisable; no score or acceptance decision is required."),
    ),
}


@dataclass(frozen=True)
class ExecutionEnvelope:
    """Finite external resources, never a definition of an admissible problem."""
    max_cycles: int
    max_calls: int | None = None
    max_completion_tokens: int | None = None
    completion_tokens_per_call: int | None = None

    def to_dict(self) -> dict[str, Any]:
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if value is not None and (type(value) is not int or value < 1):
                raise ValueError(f"{field.name} must be a positive integer or None")
        if self.max_cycles is None:
            raise ValueError("An operator must supply a finite max_cycles")
        total, per_call = self.max_completion_tokens, self.completion_tokens_per_call
        if (total is None) != (per_call is None):
            raise ValueError("Declare total completion budget and per-call cap together")
        if total is not None and per_call is not None and per_call > total:
            raise ValueError("Per-call cap cannot exceed the total completion budget")
        return {**dataclasses.asdict(self), "stop_condition": "mini.stop.never"}


def _kind(kind_id: str, title: str, ports: list[dict[str, Any]], instruction: str) -> dict[str, Any]:
    return {
        "kind_id": kind_id, "title": title, "input_ports": copy.deepcopy(ports),
        "output_port": {"port_id": "out", "produces_kind": kind_id},
        "format": None, "optional_fields": [], "commitment_call": "single",
        "instruction": instruction,
        "failure_policy": {"retries": 0, "tolerance": None, "action": "drop", "skip_on_empty_port": False},
    }


def make_manifest(template: str, source_paths: Sequence[str], envelope: ExecutionEnvelope,
                  *, manifest_id: str | None = None) -> dict[str, Any]:
    """Build a real Forge manifest. Paths are relative to the manifest file.

    Source files are not interpreted or required to contain a well-posed task.
    The 64-source bound belongs to the inspected Forge schema, not to semantics.
    """
    if template not in TEMPLATES:
        raise ValueError(f"Unknown transport template: {template!r}")
    if len(source_paths) > 64:
        raise ValueError("This Forge transport supports at most 64 source files; this says nothing about the subject's admissibility")
    for path in source_paths:
        if not isinstance(path, str) or not path or len(path) > 256:
            raise ValueError("Each source path must fit Forge's 1..256 character transport field")
    identity = f"{VERSION}.{template}" if manifest_id is None else manifest_id
    if not isinstance(identity, str) or not 1 <= len(identity) <= 128:
        raise ValueError("manifest_id must fit Forge's 1..128 character transport field")
    ids = {role: f"open.inquiry.{template}.{role}.v1" for role, _ in ROLES[template]}
    discussion_ids = [*ids.values(), VERDICT_KIND]
    port_types = [
        {"port_type": "open.source-input", "draws_from": {"evidence_tiers": ["evidence"]}, "render": {"rule": "legend", "header": "Source intake for the verbatim machine bridge"}},
        {"port_type": "open.fulltext", "draws_from": {"artifact_kinds": [MATERIAL_KIND]}, "render": {"rule": "list_bodies", "header": "Full source text, without excerpt selection"}},
        {"port_type": "open.discussion", "draws_from": {"artifact_kinds": discussion_ids}, "render": {"rule": "list_bodies_and_commitments", "header": "Earlier contributions, not endorsed conclusions"}},
    ]
    shared_ports = [
        {"port_id": "opening-status", "port_type": "problem"},
        {"port_id": "materials", "port_type": "open.fulltext", "window": "this_cycle"},
        {"port_id": "discussion", "port_type": "open.discussion", "window": "all"},
    ]
    source_ports = [{"port_id": "source-input", "port_type": "open.source-input", "window": "all"}]
    kinds = [_kind(MATERIAL_KIND, "Verbatim source transport, not a reasoning participant", source_ports,
                   "A registered deterministic seat copies the permitted source files without semantic selection, scoring, summarisation or interpretation.")]
    stages: list[dict[str, Any]] = [{"stage_id": "materials", "kind_id": MATERIAL_KIND, "ports": ["source-input"], "seat": "machine"}]
    if template == "blind_roundtrip":
        port_types.append({"port_type": "open.current-encoding", "draws_from": {"artifact_kinds": [ids["encode"]]}, "render": {"rule": "list_bodies", "header": "Current expression and its supplied conventions"}})
    for role, invitation in ROLES[template]:
        ports = ([{"port_id": "expression", "port_type": "open.current-encoding", "window": "this_cycle"}]
                 if template == "blind_roundtrip" and role == "read" else shared_ports)
        kinds.append(_kind(ids[role], role.replace("_", " "), ports, COMMON + "\n\n" + invitation))
        stages.append({"stage_id": role, "kind_id": ids[role], "ports": [p["port_id"] for p in ports], "seat": "model"})
    kinds.append(_kind(VERDICT_KIND, "Unresolved continuation, not adjudication", shared_ports, COMMON + "\n\n" + CONTINUE))
    stages.extend([
        {"stage_id": "continue", "kind_id": VERDICT_KIND, "ports": [p["port_id"] for p in shared_ports], "seat": "model"},
        {"stage_id": "end", "end": True},
    ])
    return {
        "schema_version": "creib.mini.manifest.v1", "manifest_id": identity,
        "problem": ("The opening concern and supplied materials are carried in the full-text source artifact. "
                    "They need not define a problem, ontology or success condition. Their wording is preserved, "
                    "not installed as an immutable operative problem. Later contributions may change what is being investigated."),
        "kinds": kinds, "port_types": port_types, "stages": stages,
        "policy": {"base": "mini.policy.default.v1"},
        "attention": {"policy": "mini.attention.off"},
        "sources": [{"source_id": f"input-{i:04d}", "path": path, "tier": "evidence"} for i, path in enumerate(source_paths, 1)],
        "cycles": envelope.to_dict(),
    }


def _evidence_targets(routing: Any, tier: str) -> tuple[Any, ...]:
    """Support the route APIs encountered during the pinned Forge review."""
    if callable(getattr(routing, "for_kind", None)):
        return tuple(routing.for_kind(f"evidence.{tier}"))
    if callable(getattr(routing, "for_evidence", None)):
        return tuple(routing.for_evidence(tier))
    raise TypeError("Unsupported Forge routing API; refusing to bypass source routes")


def _target_matches_port(target: Any, port: Any) -> bool:
    tag = getattr(target, "tag", getattr(target, "target", None))
    return ((tag == "port_type" and target.port_type == port.port_type)
            or (tag == "pid" and target.port_id == port.port_id))


def _source_visible(context: Any, source: Any) -> bool:
    """Respect declared evidence ports, windows, permissions and explicit routes."""
    from creib.forge.mini.ports import port_draws_tiers
    plan, stage = context.plan, context.stage
    kind = plan.kinds[str(stage.kind_id)]
    for port_id in stage.ports:
        port = kind.port(port_id)
        port_type = plan.port_types[port.port_type]
        if port_type.source != "evidence" or not port.window.admits(0, context.cycle):
            continue
        if not plan.policy.may_read(kind.kind_id, port.port_type):
            continue
        if source.tier not in port_draws_tiers(port_type, port.params):
            continue
        routes = _evidence_targets(plan.routing, source.tier)
        if not routes or any(_target_matches_port(target, port) for target in routes):
            return True
    return False


def _fulltext_answer(context: Any) -> str:
    pieces = ["HOST COPY OF SUPPLIED TEXT. Source labels record provenance, not truth or priority."]
    for source in context.plan.sources:
        if not _source_visible(context, source):
            continue
        text = source.raw.decode("utf-8")
        digest = hashlib.sha256(source.raw).hexdigest()
        pieces.extend([f"SOURCE {source.source_id}; UTF-8 bytes={len(source.raw)}; sha256={digest}", text,
                       f"END SOURCE {source.source_id}"])
    if len(pieces) == 1:
        pieces.append("No source text is supplied at this port. An unspecified problem is not a semantic failure.")
    return json.dumps({"body": "\n\n".join(pieces),
                       "commitments": "Host transport only: permitted source bytes are copied without judging their meaning."}, ensure_ascii=False)


def install_source_bridge() -> None:
    """Register the additive full-text seat without replacing an existing plugin."""
    from creib.forge.mini.machines import MachineSeat, register_machine_seat, registered_machine_seats
    for seat in registered_machine_seats():
        if seat.kind_id == MATERIAL_KIND:
            if seat.answer is not _fulltext_answer:
                raise RuntimeError(f"Another plugin already owns {MATERIAL_KIND}")
            return
    register_machine_seat(MachineSeat(MATERIAL_KIND, "Verbatim permitted-source transport; no semantic judgement", _fulltext_answer))


def _write_json_exclusive(path: Path, payload: Any) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


class VerbatimEnvelopeResponder:
    """Preserve *any* public textual reply, including non-JSON and partial prose.

    The delegate sees the unchanged Forge request. Its entire public response
    becomes body, even when that response happens to be JSON. The host does not
    parse it, infer commitments, repair its argument, or claim it is complete.
    Native provider failures still propagate. A sidecar records the delegate's
    request and response, not an invented claim of complete HTTP-wire custody.
    """
    def __init__(self, delegate: Any, record_dir: Path) -> None:
        self.delegate = delegate
        self.record_dir = Path(record_dir)
        self.record_dir.mkdir(parents=True, exist_ok=False)
        self._sequence = 0

    @property
    def completion_cap(self) -> int | None:
        return getattr(self.delegate, "completion_cap", None)

    def reply(self, request: Any) -> Any:
        if request.phase != "both":
            raise ValueError("These open-inquiry templates use single-call/both-phase transport")
        self._sequence += 1
        destination = self.record_dir / f"{self._sequence:06d}.json"
        record: dict[str, Any] = {"schema_version": VERSION + ".transport", "sequence": self._sequence,
                                  "request": dataclasses.asdict(request)}
        try:
            response = self.delegate.reply(request)
        except Exception as error:
            record.update(status="delegate-raised", exception_type=type(error).__name__)
            _write_json_exclusive(destination, record)
            raise
        if not isinstance(response.text, str):
            record.update(status="non-text-response")
            _write_json_exclusive(destination, record)
            raise TypeError("Forge Responder.reply must return a textual Reply")
        raw = response.text
        # An empty provider response is preserved but never called a reasoning contribution.
        body = raw if raw.strip() else "HOST TRANSPORT NOTE: the upstream text was empty or whitespace-only; its exact bytes are in the sidecar. No participant contribution is inferred."
        framed = json.dumps({"body": body, "commitments": TRANSPORT_COMMITMENTS}, ensure_ascii=False)
        record.update(status="text-returned", raw_text=raw, framed_text=framed,
                      raw_sha256=hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                      framed_sha256=hashlib.sha256(framed.encode("utf-8")).hexdigest(),
                      prompt_tokens=response.prompt_tokens, completion_tokens=response.completion_tokens,
                      empty_or_whitespace=not bool(raw.strip()))
        _write_json_exclusive(destination, record)
        return dataclasses.replace(response, text=framed)


def run_open_inquiry(plan: Any, root: Path, responder: Any, *, responder_id: str) -> Any:
    """Run an explicitly supplied responder. Calling this may call that provider."""
    from creib.forge.mini.runner import run_mini
    if not responder_id.strip():
        raise ValueError("Record the actual responder identity")
    if any(not stage.end and stage.seat == "model" and plan.kinds[stage.kind_id].commitment_call != "single" for stage in plan.stages):
        raise ValueError("Verbatim envelope transport requires the supplied single-call templates")
    install_source_bridge()
    wrapped = VerbatimEnvelopeResponder(responder, Path(root) / "verbatim-transport")
    endpoint = getattr(responder, "endpoint", None)
    return run_mini(plan, Path(root), wrapped, responder_id=f"{VERSION}.verbatim|{responder_id}", endpoint=endpoint)


def write_bundle(opening: bytes, destination: Path, envelope: ExecutionEnvelope,
                 extra_sources: Iterable[bytes] = ()) -> tuple[Path, ...]:
    """Create new files only. UTF-8 input bytes, including CRLF, are retained."""
    envelope.to_dict()
    sources = [opening, *extra_sources]
    if len(sources) > 64:
        raise ValueError("The current Forge source-count transport bound is 64")
    for raw in sources:
        if not isinstance(raw, bytes):
            raise TypeError("Supply source bytes so newline conversion cannot alter them")
        raw.decode("utf-8")
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    inputs, configs = destination / "inputs", destination / "configs"
    inputs.mkdir()
    configs.mkdir()
    paths: list[str] = []
    receipts = []
    for index, raw in enumerate(sources, 1):
        path = inputs / f"input-{index:04d}.txt"
        path.write_bytes(raw)
        paths.append(f"../inputs/{path.name}")
        receipts.append({"path": f"inputs/{path.name}", "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    _write_json_exclusive(destination / "execution-envelope.json", dataclasses.asdict(envelope))
    _write_json_exclusive(destination / "input-receipts.json", receipts)
    written = []
    for template in TEMPLATES:
        path = configs / f"{template}.json"
        _write_json_exclusive(path, make_manifest(template, paths, envelope))
        written.append(path)
    return tuple(written)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate open-subject Forge templates. This command never calls a provider.")
    parser.add_argument("--opening", required=True, type=Path, help="UTF-8 file; may contain an ill-defined concern or be empty")
    parser.add_argument("--source", action="append", default=[], type=Path, help="Additional complete source; repeatable")
    parser.add_argument("--out", required=True, type=Path, help="New output directory; existing directories are not overwritten")
    parser.add_argument("--cycles", required=True, type=int, help="External execution envelope, not a semantic stopping claim")
    parser.add_argument("--max-calls", type=int)
    parser.add_argument("--max-completion-tokens", type=int)
    parser.add_argument("--completion-tokens-per-call", type=int)
    args = parser.parse_args(argv)
    try:
        envelope = ExecutionEnvelope(args.cycles, args.max_calls, args.max_completion_tokens, args.completion_tokens_per_call)
        paths = write_bundle(args.opening.read_bytes(), args.out, envelope, (p.read_bytes() for p in args.source))
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        parser.error(str(error))
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
