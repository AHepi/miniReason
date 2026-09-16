"""One recorded provider chat call per open-inquiry Forge request.

The unchanged Forge engine requires directory fsync. The CLI probes that
requirement before dispatch; Windows Python currently refuses it. No filesystem
shim, repair, retry, or automatic successor is installed by this module.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
from typing import Any, Sequence

from creib.forge.mini.common import MiniError
from creib.forge.mini.executor import Reply, Request
from creib.forge.mini.manifest import compile_manifest
from minireason import provider_openai_compat as provider
from minireason.open_inquiry import install_source_bridge, run_open_inquiry
from minireason.reason import adapter as recorded
from minireason.reason.config import load_endpoint_snapshot, thinking_for
from minireason.reason.types import ReasonFailure


class TextAdapter(recorded.Adapter):
    """Keep the existing worker and custody; remove its reason-loop JSON mode."""

    def prepare(self, *, seat: str | dict, messages: list, max_tokens: int = 8192,
                thinking: str | bool | None = None, role: str = "",
                coordinate: dict | None = None) -> dict:
        endpoint = self._endpoint(seat)
        snapshot = self.endpoint_snapshot
        if snapshot is not None and "data" in snapshot:
            snapshot = snapshot["data"]
        # Default to explicit off where supported; unsupported gateways retain
        # their declared default, never an invented off/native control.
        declared = thinking_for(seat, False if thinking is None else thinking, snapshot)
        wire_thinking = {"native": True, "off": False, "gateway-default": None}[declared]
        extra = None
        if endpoint.native and endpoint.family.startswith("ollama-cloud/"):
            if wire_thinking is not None:
                extra = {"think": wire_thinking}
            wire_thinking = None
        kwargs = {
            "max_tokens": max_tokens, "response_format": None,
            "temperature": None, "seed": None, "extra": extra,
            "thinking": wire_thinking, "reasoning_effort": "high",
        }
        caller = recorded._PreparedCaller(endpoint, Path("."))
        try:
            caller._validate_call_args(max_tokens=max_tokens, reasoning_effort="high", extra=extra)
            payload = caller._build_payload(messages, **kwargs)
        except (TypeError, ValueError):
            raise ReasonFailure("CONFIG_ERROR", "Provider settings are not supported") from None
        kwargs["coordinate"] = {**(coordinate or {}), "role": role}
        wire = json.dumps(payload)
        _, secrets = provider.redact_with_names(wire)
        if secrets:
            raise ReasonFailure("SECRET_IN_REQUEST", "Credential found in the proposed request")
        return {
            "endpoint": dataclasses.asdict(endpoint), "messages": messages,
            "kwargs": kwargs, "thinking": declared, "reasoning_effort": "high",
            "payload": payload, "wire_body_text": wire,
            "wire_body_sha256": hashlib.sha256(wire.encode("utf-8")).hexdigest(),
            "mode": self.mode, "prepared_epoch": time.time(),
            "wall_seconds": recorded.WALL_SECONDS,
        }


@dataclasses.dataclass(frozen=True)
class EndpointReceipt:
    """Forge expects to_dict; the shared transport endpoint uses a dataclass."""

    value: provider.Endpoint

    def to_dict(self) -> dict:
        return dataclasses.asdict(self.value)


class LiveResponder:
    """Public text and usage only; one attempt per Forge coordinate."""

    def __init__(self, endpoint_name: str, root: Path, completion_cap: int,
                 thinking: str | None = None, adapter: TextAdapter | None = None):
        if type(completion_cap) is not int or completion_cap < 1:
            raise ValueError("Declare a positive completion_tokens_per_call")
        if thinking not in {None, "native", "off"}:
            raise ValueError("thinking must be native or off")
        self.adapter = adapter if adapter is not None else TextAdapter(
            mode="live", endpoint_snapshot=load_endpoint_snapshot())
        endpoint = self.adapter._endpoint(endpoint_name)
        self.endpoint = EndpointReceipt(endpoint)
        self.responder_id = endpoint.name
        self.root = Path(root)
        self.completion_cap = completion_cap
        self.thinking = thinking
        self._sequence = 0
        self._seen: set[tuple] = set()
        self._failed = False
        # Validate controls/cap/path without constructing a live provider.
        self.adapter.prepare(seat=endpoint_name, messages=[{"role": "user", "content": ""}],
                             max_tokens=completion_cap, thinking=thinking)
        if len(str((self.root / "provider/000001/transport/call-0001.response.json").resolve())) >= 200:
            raise ReasonFailure("PATH_TOO_LONG", "Use a shorter run directory")

    def reply(self, request: Request) -> Reply:
        if request.phase != "both" or request.attempt != 0:
            raise ValueError("Open inquiry permits one both-phase call with no retry")
        coordinate = (request.cycle, request.stage_id, request.kind_id, request.phase)
        if self._failed or coordinate in self._seen:
            raise ReasonFailure("NO_REPLAY", "A failed responder or visited coordinate cannot be sent again")
        self._seen.add(coordinate)
        self._failed = True
        self._sequence += 1
        directory = self.root / "provider" / f"{self._sequence:06d}"
        directory.mkdir(parents=True, exist_ok=False)
        # Public wrapper receipts are redacted by the shared write-once hook.
        recorded._provider_write(directory / "forge-request.json", {
            "schema_version": "open-inquiry.live.call.v1",
            "sequence": self._sequence, "started_epoch": time.time(),
            "forge_request": dataclasses.asdict(request),
            "endpoint": self.endpoint.to_dict(), "completion_cap": self.completion_cap,
            "thinking_requested": self.thinking, "mode": self.adapter.mode,
            "wall_seconds": recorded.WALL_SECONDS, "transport_retries": 0,
        })
        try:
            result = self.adapter.call(
                seat=self.responder_id,
                messages=[{"role": "user", "content": request.brief}],
                records_dir=directory / "transport", max_tokens=self.completion_cap,
                thinking=self.thinking, role=request.stage_id,
                coordinate={"cycle": request.cycle, "stage_id": request.stage_id,
                            "kind_id": request.kind_id, "attempt": request.attempt,
                            "phase": request.phase})
            usage = result.get("usage", {})
            if any(type(usage.get(name)) is not int or usage[name] < 0
                   for name in ("prompt_tokens", "completion_tokens")):
                raise ReasonFailure("USAGE_UNAVAILABLE", "Provider did not report usable token counts")
            if usage["completion_tokens"] > self.completion_cap:
                raise ReasonFailure("COMPLETION_CEILING_VIOLATED",
                                    "Reported usage exceeded the declared cap; original evidence retained")
            if not isinstance(result.get("content"), str):
                raise ReasonFailure("CONTENT_TYPE", "Provider content was not text")
            recorded._provider_write(directory / "forge-response.json", {
                "status": "COMPLETE", "finished_epoch": time.time(),
                "content": result["content"], "usage": usage,
                "native_reasoning_text_persisted": False,
                "transport_response": "transport/call-0001.response.json",
            })
            self._failed = False
            return Reply(result["content"], usage["prompt_tokens"], usage["completion_tokens"])
        except BaseException as error:
            self._failed = True
            recorded._provider_write(directory / "forge-response.json", {
                "status": "provider-exception", "finished_epoch": time.time(),
                "exception_type": type(error).__name__,
                "code": error.code if isinstance(error, ReasonFailure) else "PROVIDER_EXCEPTION",
                "native_reasoning_text_persisted": False,
            })
            # Forge and the pack's VerbatimEnvelopeResponder receive the failure.
            # The current Forge engine propagates it; it does not emit RUN_STOPPED.
            raise


def validate_plan(plan: Any) -> int:
    cycles = plan.cycles
    cap = cycles.completion_tokens_per_call
    if type(cap) is not int or cap < 1 or type(cycles.max_completion_tokens) is not int:
        raise ValueError("Live use requires declared total and per-call completion-token limits")
    if cycles.max_completion_tokens < cap:
        raise ValueError("Total completion budget cannot be smaller than the per-call cap")
    for stage in plan.stages:
        if not stage.end and stage.seat == "model":
            kind = plan.kinds[stage.kind_id]
            if kind.commitment_call != "single" or kind.failure_policy.retries != 0:
                raise ValueError("Live open inquiry requires single-call model kinds with zero retries")
    return cap


def verify_forge_storage(root: Path) -> None:
    """Exercise the actual file+directory durability contract before any send."""
    from creib.errors import RecordError
    from creib.forge.conformance.common import publish_no_clobber

    target = Path(root) / "durability-probe" / "probe.txt"
    try:
        publish_no_clobber(target, b"open-inquiry durability preflight\n")
    except RecordError:
        recorded._provider_write(Path(root) / "durability.json", {
            "status": "TARGET_FILESYSTEM_DURABILITY_UNAVAILABLE", "provider_calls": 0,
            "requirement": "Unchanged Forge exclusive publication with file and directory fsync",
        })
        raise ReasonFailure("TARGET_FILESYSTEM_DURABILITY_UNAVAILABLE",
                        "Forge file and directory durability failed; no provider was called. "
                        "Use a filesystem/host supporting the unchanged Forge publisher.") from None
    recorded._provider_write(Path(root) / "durability.json", {
        "status": "passed", "provider_calls": 0,
        "requirement": "Unchanged Forge exclusive publication with file and directory fsync",
    })


def load_env_file(path: Path | None) -> None:
    """Reuse the CLI's two-name, ignored/untracked, transactional file loader."""
    if path is None:
        return
    tool = Path(__file__).resolve().parents[2] / "tools" / "reason.py"
    spec = importlib.util.spec_from_file_location("_open_inquiry_reason_cli", tool)
    if spec is None or spec.loader is None:
        raise ReasonFailure("ENV_FILE_UNREADABLE", "Cannot load the checkout environment-file helper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.load_env_file(path)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True, help="New run directory; never resumed or overwritten")
    parser.add_argument("--endpoint", required=True, help="Exact name from endpoints.json")
    parser.add_argument("--thinking", choices=("native", "off"), default=None)
    parser.add_argument("--env-file", type=Path, help="Ignored/untracked checkout file; two provider key names only")
    args = parser.parse_args(argv)
    root: Path | None = None
    try:
        install_source_bridge()
        plan = compile_manifest(args.config)
        cap = validate_plan(plan)
        # Snapshot endpoint configuration; all credentials remain environment-only.
        transport = TextAdapter(mode="live", endpoint_snapshot=load_endpoint_snapshot())
        responder = LiveResponder(args.endpoint, args.out, cap, args.thinking, transport)
        candidate = args.out.resolve()
        if candidate.exists():
            raise ReasonFailure("RUN_EXISTS", "Choose a new run directory")
        candidate.mkdir(parents=True, exist_ok=False)
        root = candidate
        print("Run directory: " + str(root))
        recorded._provider_write(root / "live-config.json", {
            "schema_version": "open-inquiry.live.v1", "manifest": dict(plan.header),
            "endpoint": responder.endpoint.to_dict(), "endpoint_snapshot": transport.endpoint_snapshot,
            "thinking_requested": args.thinking, "wall_seconds": recorded.WALL_SECONDS,
            "transport_retries": 0, "completion_cap": cap,
            "config_path": str(args.config.resolve()), "started_epoch": time.time(),
        })
        verify_forge_storage(root)
        load_env_file(args.env_file)
        outcome = run_open_inquiry(plan, root, responder, responder_id=responder.responder_id)
        summary = {"stop_reason": outcome.stop_reason, "cycles_completed": outcome.cycles_completed,
                   "calls": outcome.calls, "completion_tokens": outcome.completion_tokens,
                   "finished_epoch": time.time()}
        recorded._provider_write(root / "live-outcome.json", summary)
        print("Stop reason: " + outcome.stop_reason)
        return 0
    except Exception as error:
        code = error.code if isinstance(error, (ReasonFailure, MiniError)) else type(error).__name__
        if root is not None and not (root / "live-outcome.json").exists():
            recorded._provider_write(root / "live-outcome.json", {
                "stop_reason": code, "exception_type": type(error).__name__,
                "finished_epoch": time.time(), "state": "refused-or-interrupted",
            })
        print("Stop reason: " + code, file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Stop reason: interrupted; preserve this directory and do not replay it", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
