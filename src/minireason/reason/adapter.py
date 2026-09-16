"""Reuse the recorded provider with one subprocess per live call and no retry."""
from __future__ import annotations
import hashlib
import json
import os
from dataclasses import asdict
from pathlib import Path
import subprocess
import sys
import time
from typing import Any
from minireason import provider_openai_compat as provider
from .config import endpoint_for, thinking_for, reasoning_effort_for
from .types import ReasonFailure

WALL_SECONDS = 300


class _ReasoningEffortCompatibility:
    def _validate_call_args(self, *, max_tokens, reasoning_effort, extra):
        # The protected transport validator predates DeepSeek's medium alias.
        # Validate its other controls unchanged; builder and wire retain medium.
        super()._validate_call_args(
            max_tokens=max_tokens,
            reasoning_effort="high" if reasoning_effort == "medium" else reasoning_effort,
            extra=extra)


class _PreparedCaller(_ReasoningEffortCompatibility, provider._RecordedCaller):
    pass


class _OfflineProvider(_ReasoningEffortCompatibility, provider.OfflineProvider):
    pass


class _LiveProvider(_ReasoningEffortCompatibility, provider.OpenAICompatProvider):
    pass

def _read(path: Path) -> Any:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            return json.load(handle)
    except (OSError, ValueError, UnicodeError) as error:
        raise ReasonFailure("INTERRUPTED_CALL", "Existing call evidence is incomplete or unreadable; no replay") from error

def _write(path: Path, value: Any) -> None:
    if len(str(path.resolve())) >= 200:
        raise ReasonFailure("PATH_TOO_LONG", "Run record path must be shorter than 200 characters")
    encoded = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())
    with path.open(encoding="utf-8", newline="") as handle:
        if handle.read() != encoded:
            raise ReasonFailure("RECORD_ERROR", "Written record failed exact reread")

def _provider_write(path: Path, value: Any) -> None:
    # The existing transport calls this write-once hook. The adapter adds the
    # required newline discipline and epoch receipts without editing its source.
    clean = dict(value)
    clean["recorded_epoch"] = time.time()
    if "request" in clean:
        wire = json.dumps(clean["request"])
        clean["wire_body_text"] = wire
        clean["wire_body_sha256"] = hashlib.sha256(wire.encode("utf-8")).hexdigest()
    encoded, names = provider.redact_with_names(json.dumps(clean, ensure_ascii=False))
    clean = json.loads(encoded)
    if names:
        clean["credentials_redacted"] = names
    _write(Path(path), clean)

def _normalise(record: dict, records_dir: Path) -> dict:
    code = record.get("status", "TRANSPORT_OR_RESPONSE_ERROR")
    result = {"status": code, "content": record.get("content", ""),
              "usage": record.get("usage", {}), "record": record,
              "request_path": str(records_dir / "call-0001.request.json"),
              "response_path": str(records_dir / "call-0001.response.json"),
              "finished_epoch": record.get("recorded_epoch", time.time())}
    if code in {"COMPLETE", "INCOMPLETE_GENERATION"} and record.get("finish_reason") in {"length", "max_tokens"}:
        raise ReasonFailure("CEILING_HIT", "Provider finish_reason=" + record["finish_reason"], result)
    if code != "COMPLETE":
        raise ReasonFailure(code, "Provider call stopped; inspect its recorded public evidence", result)
    return result

def recover(records_dir: str | Path) -> dict | None:
    records = Path(records_dir)
    response = records / "call-0001.response.json"
    if response.exists():
        return _normalise(_read(response), records)
    failure = records / "worker-failure.json"
    if failure.exists():
        record = _read(failure)
        raise ReasonFailure(record["code"], record["detail"], record)
    return None

class Adapter:
    def __init__(self, mode: str = "offline", endpoint_snapshot: dict | None = None):
        if mode not in {"offline", "live"}:
            raise ReasonFailure("CONFIG_ERROR", "Mode must be live or offline")
        self.mode = mode
        self.endpoint_snapshot = endpoint_snapshot

    def _endpoint(self, seat: str | dict):
        data = self.endpoint_snapshot
        if data is not None and "data" in data:
            data = data["data"]
        return endpoint_for(seat, data)

    def prepare(self, *, seat: str | dict, messages: list, max_tokens: int = 8192,
                thinking: str | bool | None = None, role: str = "", coordinate: dict | None = None) -> dict:
        endpoint = self._endpoint(seat)
        snapshot = self.endpoint_snapshot
        if snapshot is not None and "data" in snapshot:
            snapshot = snapshot["data"]
        declared_thinking = thinking_for(seat, thinking, snapshot)
        thinking = {"native": True, "off": False, "gateway-default": None}[declared_thinking]
        extra = None
        if endpoint.native and endpoint.family.startswith("ollama-cloud/"):
            if thinking is not None:
                extra = {"think": thinking}
            # The transport thinking parameter is DeepSeek-specific. Preserve
            # Ollama control in actual extra/settings/wire evidence instead.
            thinking = None
        effort = reasoning_effort_for(seat)
        caller = _PreparedCaller(endpoint, Path("."))
        kwargs = {"max_tokens": max_tokens, "response_format": {"type": "json_object"},
                  "temperature": None, "seed": None, "extra": extra,
                  "thinking": thinking, "reasoning_effort": effort}
        try:
            caller._validate_call_args(max_tokens=max_tokens, reasoning_effort=effort, extra=extra)
            caller._check_json_mode_prompt(messages, kwargs["response_format"])
            payload = caller._build_payload(messages, **kwargs)
        except (TypeError, ValueError) as error:
            raise ReasonFailure("CONFIG_ERROR", "Provider settings are not supported") from error
        kwargs["coordinate"] = {**(coordinate or {}), "role": role}
        wire = json.dumps(payload)
        _redacted, credentials = provider.redact_with_names(wire)
        if credentials:
            raise ReasonFailure("SECRET_IN_REQUEST", "Credential found in the proposed request")
        return {"endpoint": asdict(endpoint), "messages": messages, "kwargs": kwargs,
                "thinking": declared_thinking, "reasoning_effort": effort,
                "payload": payload, "wire_body_text": wire,
                "wire_body_sha256": hashlib.sha256(wire.encode("utf-8")).hexdigest(),
                "mode": self.mode, "prepared_epoch": time.time(), "wall_seconds": WALL_SECONDS}

    def recover(self, records_dir: str | Path) -> dict | None:
        return recover(records_dir)

    def call(self, *, seat: str | dict, messages: list, records_dir: str | Path,
             max_tokens: int = 8192, thinking: str | bool | None = None, role: str = "",
             coordinate: dict | None = None, scripted: dict | str | None = None) -> dict:
        endpoint = self._endpoint(seat)
        # Refuse before either provider construction or spawning a worker.
        if self.mode == "live" and not os.environ.get(endpoint.key_env):
            raise ReasonFailure("KEY_MISSING", endpoint.key_env + " is not set")
        records = Path(records_dir)
        prior = recover(records)
        if prior is not None:
            return prior
        if records.exists() and any(records.iterdir()):
            raise ReasonFailure("INTERRUPTED_CALL", "Existing nonterminal call evidence cannot be replayed")
        prepared = self.prepare(seat=seat, messages=messages, max_tokens=max_tokens,
                                thinking=thinking, role=role, coordinate=coordinate)
        if len(str((records / "call-0001.response.json").resolve())) >= 200:
            raise ReasonFailure("PATH_TOO_LONG", "Run record path must be shorter than 200 characters")
        if self.mode == "offline":
            if scripted is None:
                raise ReasonFailure("CONFIG_ERROR", "Offline call needs an explicit scripted response")
            if isinstance(scripted, dict) and "content" not in scripted:
                scripted = {"content": json.dumps(scripted, ensure_ascii=False)}
            if isinstance(scripted, dict) and prepared["kwargs"]["thinking"] is True:
                scripted = {"reasoning_content_present": True, **scripted}
            return _execute(prepared, records, scripted=scripted)
        # Input has no credential values; inherited environment is read by the
        # existing provider only at the actual call. Never read a dotenv file.
        clean, redactions = provider.redact_with_names(json.dumps(prepared, ensure_ascii=False))
        if redactions:
            raise ReasonFailure("SECRET_IN_REQUEST", "Credential found in the proposed request")
        spec_path = records / "worker-input.json"
        _write(spec_path, json.loads(clean))
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        started = time.monotonic()
        worker_env = dict(os.environ)
        worker_env["PYTHONPATH"] = str(Path(__file__).resolve().parents[2]) + os.pathsep + worker_env.get("PYTHONPATH", "")
        worker_env["PYTHONUTF8"] = "1"
        try:
            process = subprocess.Popen(
                [sys.executable, "-X", "utf8", "-m", "minireason.reason.worker", str(spec_path.resolve()), str(records.resolve())],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=flags, env=worker_env)
            try:
                process.wait(timeout=max(0.01, WALL_SECONDS - (time.monotonic() - started)))
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
                terminal = recover(records)
                if terminal is not None:
                    return terminal
                failure = {"code": "TRANSPORT_OR_RESPONSE_ERROR", "detail": "300 second wall reached; call is not replayed", "recorded_epoch": time.time()}
                _write(records / "worker-failure.json", failure)
                raise ReasonFailure(failure["code"], failure["detail"], failure)
        except OSError as error:
            raise ReasonFailure("TRANSPORT_OR_RESPONSE_ERROR", "Live worker could not start") from error
        except BaseException:
            if "process" in locals() and process.poll() is None:
                process.kill()
                process.wait()
            raise
        terminal = recover(records)
        if terminal is None:
            failure = {"code": "TRANSPORT_OR_RESPONSE_ERROR", "detail": "Worker stopped without a terminal provider record", "recorded_epoch": time.time()}
            _write(records / "worker-failure.json", failure)
            raise ReasonFailure(failure["code"], failure["detail"], failure)
        return terminal


# The legacy provider exposes its writer as a module hook. A lock confines the
# replacement to one adapter call in this process; live calls are isolated.
import threading
_WRITER_LOCK = threading.RLock()

def _execute(prepared: dict, records: Path, scripted: dict | str | None = None) -> dict:
    endpoint = provider.Endpoint(**prepared["endpoint"])
    with _WRITER_LOCK:
        original_writer = provider.write_new
        provider.write_new = _provider_write
        try:
            if prepared["mode"] == "offline":
                caller = _OfflineProvider(endpoint, records, [scripted])
            else:
                caller = _LiveProvider(endpoint, records)
            caller.complete(prepared["messages"], **prepared["kwargs"])
        except provider.ProviderFailure as error:
            # The durable terminal record, when present, preserves public
            # content/usage and identifies the precise provider failure.
            terminal = recover(records)
            if terminal is not None:
                return terminal
            raise ReasonFailure(error.code, "Provider refused the call", error.record or {}) from None
        finally:
            provider.write_new = original_writer
    terminal = recover(records)
    if terminal is None:
        raise ReasonFailure("RECORD_ERROR", "Provider returned without durable terminal evidence")
    return terminal
