"""DeepSeek transport with explicit thinking controls and redacted call records.

Native reasoning text is not persisted or fed to other calls. Public answer
content, usage, finish reason, request identity and provider identity are kept.
No automatic retry can silently spend another call.
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from creib.forge.mini.executor import Reply, Request, contract_for

_SLOTS = threading.BoundedSemaphore(5)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _open(request, *, timeout):
    return urllib.request.build_opener(_NoRedirect()).open(request, timeout=timeout)


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def write_new(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    key = os.environ.get("DEEPSEEK_API_KEY")
    if key:
        encoded = encoded.replace(key, "[REDACTED_CREDENTIAL]")
    with path.open("x", encoding="utf-8") as handle:
        handle.write(encoded + "\n")


class ProviderFailure(RuntimeError):
    def __init__(self, code: str, detail: str):
        self.code = code
        super().__init__(f"{code}: {detail}")


@dataclass(frozen=True)
class Settings:
    model: str = "deepseek-flash"
    base_url: str = "https://api.deepseek.com/v1"
    thinking: bool = False
    reasoning_effort: str = "high"
    max_tokens: int = 8192
    timeout_seconds: int = 180

    def __post_init__(self) -> None:
        if self.base_url != "https://api.deepseek.com/v1":
            raise ValueError("Only the declared DeepSeek credential destination is supported")
        if self.model != "deepseek-flash":
            raise ValueError("This campaign is bound to deepseek-flash (V4.1 Flash)")
        if type(self.thinking) is not bool or self.reasoning_effort not in {"low", "high", "max"}:
            raise ValueError("Invalid thinking controls")
        if type(self.max_tokens) is not int or not 1 <= self.max_tokens <= 393216:
            raise ValueError("Invalid completion ceiling")
        if type(self.timeout_seconds) is not int or not 1 <= self.timeout_seconds <= 600:
            raise ValueError("Invalid timeout")

    def to_dict(self) -> dict[str, Any]:
        return {"kind": "deepseek-chat", **asdict(self),
                "key_env": "DEEPSEEK_API_KEY", "seed": None,
                "temperature": "provider-default", "top_p": "provider-default",
                "native_reasoning_text_persisted": False}


class DeepSeek:
    def __init__(self, settings: Settings, records: Path):
        self.settings = settings
        self.records = Path(records)
        self.calls = 0
        self.completion_tokens = 0
        self.prompt_tokens = 0
        self._lock = threading.Lock()
        if not os.environ.get("DEEPSEEK_API_KEY"):
            raise ProviderFailure("KEY_MISSING", "DEEPSEEK_API_KEY is not set")

    def complete(self, messages: list[dict[str, str]], *, json_output: bool = True,
                 coordinate: dict[str, Any] | None = None) -> dict[str, Any]:
        with self._lock:
            self.calls += 1
            call_number = self.calls
        key = os.environ["DEEPSEEK_API_KEY"]
        payload: dict[str, Any] = {
            "model": self.settings.model, "messages": messages,
            "stream": False, "max_tokens": self.settings.max_tokens,
            "thinking": {"type": "enabled" if self.settings.thinking else "disabled"},
        }
        if self.settings.thinking:
            payload["reasoning_effort"] = self.settings.reasoning_effort
        if json_output:
            payload["response_format"] = {"type": "json_object"}
        # Refuse accidental credential carriage in public request content.
        request_hash = digest(payload)
        stem = f"call-{call_number:04d}"
        record: dict[str, Any] = {
            "schema_version": "minireason.call.v1", "request": payload,
            "request_sha256": request_hash, "settings": self.settings.to_dict(),
            "coordinate": coordinate or {},
            "started_at": datetime.now(timezone.utc).isoformat(),
        }
        write_new(self.records / (stem + ".request.json"), record)
        if key in json.dumps(payload) or key in json.dumps(coordinate or {}):
            record.update({"status": "SECRET_IN_REQUEST", "error": "Credential found in prompt content"})
            write_new(self.records / (stem + ".response.json"), record)
            raise ProviderFailure("SECRET_IN_REQUEST", "Credential found in prompt content")
        start = time.monotonic()
        request = urllib.request.Request(self.settings.base_url + "/chat/completions",
            data=json.dumps(payload).encode(), headers={"Content-Type": "application/json",
            "Authorization": "Bearer " + key}, method="POST")
        try:
            with _SLOTS:
                with _open(request, timeout=self.settings.timeout_seconds) as response:
                    raw = response.read()
            result = json.loads(raw)
            choice = result["choices"][0]
            message = choice["message"]
            answer = message.get("content")
            if answer is None:
                answer = ""
            if not isinstance(answer, str):
                raise ProviderFailure("CONTENT_TYPE", "Provider content was not text")
            echoed = key in json.dumps(result)
            answer = answer.replace(key, "[REDACTED_CREDENTIAL]")
            usage = result.get("usage", {})
            usage_valid = (type(usage) is dict and all(
                type(usage.get(k)) is int and usage[k] >= 0
                for k in ("completion_tokens", "prompt_tokens")))
            if usage_valid:
                with self._lock:
                    self.completion_tokens += usage["completion_tokens"]
                    self.prompt_tokens += usage["prompt_tokens"]
            record.update({"elapsed_ms": int((time.monotonic()-start)*1000),
                "provider_response_sha256": hashlib.sha256(raw).hexdigest(),
                "response_id": result.get("id"), "returned_model": result.get("model"),
                "system_fingerprint": result.get("system_fingerprint"),
                "provider_created": result.get("created"), "usage": usage,
                "finish_reason": choice.get("finish_reason"), "content": answer,
                "reasoning_content_present": bool(message.get("reasoning_content")),
                "reasoning_content_persisted": False, "credential_redaction": echoed})
            code = None
            if echoed:
                code = "CREDENTIAL_ECHO"
            elif choice.get("finish_reason") != "stop":
                code = "INCOMPLETE_GENERATION"
            elif not answer.strip():
                code = "EMPTY_GENERATION"
            elif not usage_valid:
                code = "USAGE_UNAVAILABLE"
            elif usage["completion_tokens"] > self.settings.max_tokens:
                code = "COMPLETION_CEILING_VIOLATED"
            elif bool(message.get("reasoning_content")) != self.settings.thinking:
                code = "THINKING_MODE_MISMATCH"
            record["status"] = code or "COMPLETE"
            write_new(self.records / (stem + ".response.json"), record)
            if code:
                raise ProviderFailure(code, f"Inspect {stem}.response.json")
            return record
        except urllib.error.HTTPError as error:
            detail = error.read(2000).decode(errors="replace").replace(key, "[REDACTED_CREDENTIAL]")
            code = f"HTTP_{error.code}"
        except ProviderFailure as error:
            response_path = self.records / (stem + ".response.json")
            if not response_path.exists():
                record.update({"status": error.code, "error": str(error),
                               "elapsed_ms": int((time.monotonic()-start)*1000)})
                write_new(response_path, record)
            raise
        except Exception as error:
            detail = str(error).replace(key, "[REDACTED_CREDENTIAL]")[:1000]
            code = "TRANSPORT_OR_RESPONSE_ERROR"
        record.update({"status": code, "error": detail,
                       "elapsed_ms": int((time.monotonic()-start)*1000)})
        write_new(self.records / (stem + ".response.json"), record)
        raise ProviderFailure(code, detail)


class MiniResponder:
    def __init__(self, provider: DeepSeek):
        self.provider = provider
        self.completion_cap = provider.settings.max_tokens

    def reply(self, request: Request) -> Reply:
        system, schema = contract_for(request.phase, request.optional_fields)
        system += "\nReturn one JSON object conforming to: " + json.dumps(schema, sort_keys=True)
        result = self.provider.complete([
            {"role": "system", "content": system},
            {"role": "user", "content": request.brief}], coordinate={
                "stage_id": request.stage_id, "kind_id": request.kind_id,
                "cycle": request.cycle, "attempt": request.attempt, "phase": request.phase})
        return Reply(result["content"], result["usage"]["prompt_tokens"],
                     result["usage"]["completion_tokens"])
