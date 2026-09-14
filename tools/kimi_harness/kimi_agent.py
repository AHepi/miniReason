"""kimi-k3 as a worker agent: an agentic loop with sandboxed tools.

One file, standard library only (``httpx`` is used when importable, ``urllib``
otherwise). It speaks to the ``ollama/kimi-k3`` entry of
``src/minireason/data/endpoints.json`` over the OpenAI-compatible surface
``https://ollama.com/v1/chat/completions`` with the repository's own auth
convention (``Authorization: Bearer $OLLAMA_API_KEY``, key read at call time,
never stored on an object and never written anywhere).

Why not ``minireason.provider_openai_compat.OpenAICompatProvider`` directly:
that transport normalises a reply to ``content``/``usage``/``finish_reason``
and *drops* ``message.tool_calls``, and it raises ``INCOMPLETE_GENERATION``
whenever ``finish_reason != "stop"`` — which is exactly what a tool-calling
turn returns. An agent loop cannot be built on it. Everything it guarantees is
kept here instead: request bytes hashed before the socket exists, no redirects,
no retries on HTTP errors, the key read from the environment at call time,
redaction on every byte that reaches disk, and native reasoning text never
persisted (only its sha256 and a token count).

Two differences from the repository transport, both deliberate and both stated
in the records this module writes:

* concurrency is a process-wide ceiling of **8** for ``OLLAMA_API_KEY`` (the
  owner authorises 10 on this key; 2 are held in reserve), not the transport's
  5. The semaphore lives in a module-level registry keyed by the env var name,
  so every agent in the process shares it.
* ``timeout_seconds`` is 600 and ``max_tokens`` is 32768 per call, matching the
  F001/C001 records already in the repository.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

__all__ = [
    "Endpoint", "TaskSpec", "TaskResult", "ChatResponse", "HarnessFailure",
    "Redactor", "Sandbox", "ToolBox", "KimiClient", "KimiAgent",
    "run_task", "load_endpoint", "load_key", "slots_for",
    "REDACTION", "MAX_CONCURRENCY", "MAX_TOKENS", "TIMEOUT_SECONDS",
]

REDACTION = "[REDACTED_CREDENTIAL]"

#: The owner authorises 10 concurrent requests on this key; 2 are kept back.
MAX_CONCURRENCY = 8
#: Per-call completion ceiling (F001/C001 records show 32768 is accepted).
# One turn's completion budget. 24576, not 32768: ruling 13 records a 300 s
# gateway wall on this host and ~90-100 tok/s, so ~25k tokens is the largest
# generation that can finish in time. 8192 is worse than useless on a
# reasoning model — PROBE-REASONING.md shows a single turn's native reasoning
# spending all 8192 and returning nothing.
MAX_TOKENS = 24576
#: Per-call wall clock ceiling in seconds.
TIMEOUT_SECONDS = 600
#: Nothing shorter than this is ever treated as a secret; see the repository
#: transport's docstring for why (a one-character value shreds every record).
_MIN_SECRET_LENGTH = 8

#: What a task may ask for per turn. ``default`` sends no control at all;
#: ``low`` and ``off`` are sent only on a surface that honours them.
REASONING_SETTINGS = ("default", "low", "off")

#: The cheapest setting, used for the one retry after a turn whose whole budget
#: went to reasoning.
LOWEST_REASONING = "off"

HERE = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = Path("/home/user/miniReason")
DEFAULT_ENDPOINTS_PATH = DEFAULT_REPO_ROOT / "src" / "minireason" / "data" / "endpoints.json"
DEFAULT_ENDPOINT_NAME = "ollama/kimi-k3"
#: Ollama's own surface. It is the default for worker tasks because it is the
#: only one that honours a reasoning control (PROBE-REASONING.md) while serving
#: the same tool round trip (probe-reasoning-native-tools.json).
NATIVE_ENDPOINT_NAME = "ollama/kimi-k3.native"
TRANSPORT_SURFACES = ("native", "v1")
#: A failure of the *surface* rather than of the request: fall back to /v1 once.
#: A provider 5xx is not in this set — that is a failure of the run, not proof
#: that this surface cannot serve it.
FALLBACK_CODES = ("TRANSPORT_OR_RESPONSE_ERROR", "HTTP_400", "HTTP_404", "HTTP_405")
DEFAULT_RUNS_DIR = HERE / "runs"

#: Never copied into a sandbox, whatever a task declares.
SANDBOX_EXCLUDES = (".env", ".env.local", ".git", "__pycache__", ".venv", "venv",
                    ".mypy_cache", ".pytest_cache")


class HarnessFailure(RuntimeError):
    """A loud harness-level failure with a stable code and a sanitised detail."""

    def __init__(self, code: str, detail: str = ""):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


# --------------------------------------------------------------------------
# Redaction
# --------------------------------------------------------------------------


class Redactor:
    """Replaces every known credential rendering with :data:`REDACTION`.

    Registered secrets are the key itself **and its first 12 characters**, in
    the raw form and in the JSON-escaped form, longest first so a prefix cannot
    leave a tail of the longer value behind. Values shorter than 8 characters
    are ignored, exactly as the repository transport documents.
    """

    def __init__(self, secrets: Iterable[str] = ()):
        self._lock = threading.Lock()
        self._renderings: list[str] = []
        self.add(secrets)

    def add(self, secrets: Iterable[str]) -> None:
        with self._lock:
            for secret in secrets:
                if not secret:
                    continue
                for value in (secret, secret[:12]):
                    if len(value) < _MIN_SECRET_LENGTH:
                        continue
                    escaped = json.dumps(value)[1:-1]
                    for rendering in {value, escaped}:
                        if rendering not in self._renderings:
                            self._renderings.append(rendering)
            self._renderings.sort(key=len, reverse=True)

    def scrub(self, text: str) -> str:
        if not isinstance(text, str):
            text = str(text)
        with self._lock:
            renderings = list(self._renderings)
        for rendering in renderings:
            if rendering in text:
                text = text.replace(rendering, REDACTION)
        return text

    def scrub_obj(self, value: Any) -> Any:
        """A JSON round-trip of ``value`` with every credential replaced."""

        return json.loads(self.scrub(json.dumps(value, ensure_ascii=False, default=str)))

    def clean(self, text: str) -> bool:
        """True when no known credential rendering is present."""

        with self._lock:
            return not any(r in text for r in self._renderings)


#: Process-wide redactor. Every persisted byte goes through it.
REDACTOR = Redactor()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()


def digest(value: Any) -> str:
    """Canonical sha256 of a JSON value (same convention as the repository)."""

    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


# --------------------------------------------------------------------------
# Endpoint and credential
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Endpoint:
    """One declared destination. The key appears only as an env var NAME."""

    name: str
    base_url: str
    model: str
    key_env: str
    family: str
    chat_path: str = "/chat/completions"
    timeout_seconds: int = TIMEOUT_SECONDS
    max_concurrency: int = MAX_CONCURRENCY
    #: True for Ollama's own ``/api/chat``, which is the only surface on this
    #: host that honours a reasoning control (see PROBE-REASONING.md).
    native: bool = False

    def __post_init__(self) -> None:
        if not self.base_url.startswith("https://"):
            raise ValueError("Endpoint base_url must be https")
        if self.base_url.endswith("/"):
            raise ValueError("Endpoint base_url must not end with '/'")
        if not self.chat_path.startswith("/"):
            raise ValueError("Endpoint chat_path must start with '/'")

    @property
    def chat_url(self) -> str:
        return self.base_url + self.chat_path

    def public(self) -> dict[str, Any]:
        return {"name": self.name, "base_url": self.base_url,
                "model": self.model, "family": self.family}


def load_endpoint(name: str = DEFAULT_ENDPOINT_NAME,
                  path: Path | str = DEFAULT_ENDPOINTS_PATH,
                  timeout_seconds: int = TIMEOUT_SECONDS) -> Endpoint:
    """The registry entry for ``name``, with this harness's timeout ceiling.

    The repository's registry declares ``timeout_seconds: 180`` and
    ``max_concurrency: 5``; the C001 records show the campaign ran kimi-k3 at
    600 s. This harness runs at 600 s and 8 slots, which is why the endpoint is
    rebuilt here rather than imported as-is.
    """

    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    for entry in raw["endpoints"]:
        if entry.get("name") == name:
            return Endpoint(name=entry["name"], base_url=entry["base_url"],
                            model=entry["model"], key_env=entry["key_env"],
                            family=entry["family"],
                            chat_path=entry.get("chat_path", "/chat/completions"),
                            timeout_seconds=timeout_seconds,
                            native=bool(entry.get("native", False)))
    raise HarnessFailure("ENDPOINT_UNKNOWN", f"no endpoint named {name!r} in {path}")


def load_key(key_env: str = "OLLAMA_API_KEY",
             env_file: Path | str | None = None) -> str:
    """The credential, from the process environment or the gitignored .env.

    Never printed, never returned to a record, never written. The value is
    registered with :data:`REDACTOR` on the way out, so anything that later
    quotes it is scrubbed before it reaches disk.
    """

    value = os.environ.get(key_env) or ""
    if not value:
        candidate = Path(env_file) if env_file else DEFAULT_REPO_ROOT / ".env"
        if candidate.is_file():
            for line in candidate.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                name, _, raw = line.partition("=")
                if name.strip() == key_env:
                    value = raw.strip().strip('"').strip("'")
                    break
    if not value:
        raise HarnessFailure("KEY_MISSING", f"{key_env} is not set and not in .env")
    REDACTOR.add([value])
    return value


# --------------------------------------------------------------------------
# Per-key concurrency
# --------------------------------------------------------------------------

_SLOT_LOCK = threading.Lock()
_SLOT_REGISTRY: dict[str, tuple[threading.BoundedSemaphore, int]] = {}


def slots_for(key_env: str, max_concurrency: int = MAX_CONCURRENCY) -> threading.BoundedSemaphore:
    """The semaphore every agent spending ``key_env`` in this process shares.

    The first caller fixes the ceiling; a later, different ceiling is refused
    rather than quietly changing an authorisation already in force. Same rule
    as ``provider_openai_compat.slots_for``, different number.
    """

    with _SLOT_LOCK:
        existing = _SLOT_REGISTRY.get(key_env)
        if existing is None:
            created = (threading.BoundedSemaphore(max_concurrency), max_concurrency)
            _SLOT_REGISTRY[key_env] = created
            return created[0]
        semaphore, limit = existing
        if limit != max_concurrency:
            raise HarnessFailure(
                "CONCURRENCY_LIMIT_CONFLICT",
                f"{key_env} is already held to {limit} concurrent requests in this process")
        return semaphore


def _reset_slot_registry() -> None:
    """Test seam only."""

    with _SLOT_LOCK:
        _SLOT_REGISTRY.clear()


# --------------------------------------------------------------------------
# Transport
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ChatResponse:
    """One provider answer, reduced to what the loop and the transcript need.

    ``reasoning_sha256`` / ``reasoning_chars`` / ``reasoning_tokens`` are the
    *only* trace of native reasoning text that ever leaves this object. The
    text itself is discarded before this dataclass is constructed.
    """

    content: str
    tool_calls: list[dict[str, Any]]
    finish_reason: str | None
    usage: dict[str, Any]
    returned_model: str | None
    response_id: str | None
    reasoning_present: bool
    reasoning_sha256: str | None
    reasoning_chars: int
    reasoning_tokens: int | None
    latency_ms: int
    request_sha256: str
    request_bytes: int
    response_sha256: str
    response_bytes: int
    http_status: int

    def assistant_message(self) -> dict[str, Any]:
        message: dict[str, Any] = {"role": "assistant", "content": self.content}
        if self.tool_calls:
            message["tool_calls"] = self.tool_calls
        return message


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Refuse every redirect: a credentialed request is never replayed elsewhere."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class KimiClient:
    """One endpoint, one credential, ``MAX_CONCURRENCY`` requests in flight.

    ``chat`` is one request on the wire or none. An HTTP error is recorded by
    the caller and raised; nothing is retried here.
    """

    def __init__(self, endpoint: Endpoint | None = None, *, key: str | None = None,
                 redactor: Redactor | None = None, surface: str = "native",
                 fallback_endpoint: Endpoint | None = None,
                 on_event: Callable[..., Any] | None = None):
        if surface not in TRANSPORT_SURFACES:
            raise HarnessFailure("TASK_SPEC_INVALID", f"unknown transport {surface!r}")
        if endpoint is None:
            endpoint = load_endpoint(NATIVE_ENDPOINT_NAME if surface == "native"
                                     else DEFAULT_ENDPOINT_NAME)
            if surface == "native" and fallback_endpoint is None:
                fallback_endpoint = load_endpoint(DEFAULT_ENDPOINT_NAME)
        self.endpoint = endpoint
        self.surface = "native" if self.endpoint.native else "v1"
        self.fallback_endpoint = fallback_endpoint
        self.on_event = on_event
        self.tool_calls_seen = False
        self.fallbacks = 0
        self.redactor = redactor or REDACTOR
        self._key = key if key is not None else load_key(self.endpoint.key_env)
        self.redactor.add([self._key])
        self._slots = slots_for(self.endpoint.key_env, self.endpoint.max_concurrency)

    # -- payload -------------------------------------------------------------

    def build_payload(self, messages: Sequence[Mapping[str, Any]], *,
                      tools: Sequence[Mapping[str, Any]] | None = None,
                      tool_choice: Any = None, max_tokens: int = MAX_TOKENS,
                      temperature: float | None = None, seed: int | None = None,
                      response_format: Mapping[str, Any] | None = None,
                      reasoning: str | None = None,
                      extra: Mapping[str, Any] | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.endpoint.model,
            "messages": [dict(message) for message in messages],
            "stream": False,
            "max_tokens": max_tokens,
        }
        if tools:
            payload["tools"] = [dict(tool) for tool in tools]
        if tool_choice is not None:
            payload["tool_choice"] = tool_choice
        if temperature is not None:
            payload["temperature"] = temperature
        if seed is not None:
            payload["seed"] = seed
        if response_format is not None:
            payload["response_format"] = dict(response_format)
        control = self.reasoning_parameter(reasoning)
        if control:
            payload.update(control)
        for key, value in (extra or {}).items():
            payload[key] = value
        return payload

    def build_native_payload(self, messages: Sequence[Mapping[str, Any]], *,
                             tools: Sequence[Mapping[str, Any]] | None = None,
                             tool_choice: Any = None, max_tokens: int = MAX_TOKENS,
                             temperature: float | None = None, seed: int | None = None,
                             response_format: Mapping[str, Any] | None = None,
                             reasoning: str | None = None,
                             extra: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """The same call, in Ollama's native shape.

        ``max_tokens`` is ``options.num_predict`` here; ``tool_choice`` has no
        native equivalent and is dropped (the tool list alone is what this
        surface takes). ``response_format`` maps to ``format``.
        """

        options: dict[str, Any] = {"num_predict": max_tokens}
        if temperature is not None:
            options["temperature"] = temperature
        if seed is not None:
            options["seed"] = seed
        payload: dict[str, Any] = {
            "model": self.endpoint.model,
            "messages": to_native_messages(messages),
            "stream": False,
            "options": options,
        }
        if tools:
            payload["tools"] = [dict(tool) for tool in tools]
        if response_format is not None:
            payload["format"] = dict(response_format)
        payload.update(self.reasoning_parameter(reasoning))
        for key, value in (extra or {}).items():
            payload[key] = value
        return payload

    def reasoning_parameter(self, reasoning: str | None) -> dict[str, Any]:
        """The request key that actually turns reasoning down on this endpoint.

        Measured, not assumed (``probes/run_reasoning_probes.py``, written up in
        ``PROBE-REASONING.md``): on Ollama's native ``/api/chat`` surface
        ``think: false`` removes the reasoning entirely and ``think: "low"``
        shortens it, while on the OpenAI-compatible ``/v1`` surface this host
        ignores ``reasoning_effort``, ``reasoning: {effort}`` **and** ``think``
        alike — all three come back 200 with reasoning no shorter than the
        control. So nothing is sent on ``/v1``: a parameter that changes
        nothing would only make the record look like a control was applied.
        """

        if reasoning in (None, "default"):
            return {}
        if reasoning not in REASONING_SETTINGS:
            raise HarnessFailure("TASK_SPEC_INVALID", f"unknown reasoning setting {reasoning!r}")
        if not self.endpoint.native:
            return {}
        return {"think": False if reasoning == "off" else reasoning}

    # -- the wire ------------------------------------------------------------

    def _post(self, url: str, body: bytes) -> tuple[bytes, int]:
        """One request on the wire or none. No retries live here."""

        request = urllib.request.Request(
            url, data=body, method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json",
                     "Authorization": "Bearer " + self._key})
        try:
            with self._slots:
                opener = urllib.request.build_opener(_NoRedirect())
                with opener.open(request, timeout=self.endpoint.timeout_seconds) as response:
                    return response.read(), response.status
        except urllib.error.HTTPError as error:
            detail = self.redactor.scrub(error.read(2000).decode(errors="replace"))
            raise HarnessFailure(f"HTTP_{error.code}", detail[:1000]) from None
        except Exception as error:  # transport, TLS, timeout
            raise HarnessFailure("TRANSPORT_OR_RESPONSE_ERROR",
                                 self.redactor.scrub(str(error))[:1000]) from None

    def _may_fall_back(self, error: HarnessFailure) -> bool:
        """Only before any tool call, only for a surface failure, only once."""

        return (self.fallback_endpoint is not None
                and not self.tool_calls_seen
                and error.code in FALLBACK_CODES)

    def reasoning_control(self) -> str | None:
        """The lowest setting this endpoint honours, or None if it honours none."""

        return LOWEST_REASONING if self.endpoint.native else None

    def refuse_credential_in_request(self, payload: Mapping[str, Any]) -> None:
        rendered = json.dumps(payload, ensure_ascii=False, default=str)
        if not self.redactor.clean(rendered):
            raise HarnessFailure("SECRET_IN_REQUEST", "credential found in outgoing payload")

    # -- the call ------------------------------------------------------------

    def chat(self, messages: Sequence[Mapping[str, Any]], **kwargs: Any) -> ChatResponse:
        """One turn, on this client's surface.

        The single exception to "one request on the wire or none": if the
        **native** surface fails as a transport before this run has seen any
        tool call, the same turn is sent once on ``/v1`` and the switch is
        recorded as ``transport_fallback``. After a tool call the conversation
        is surface-shaped and switching would silently change what the model
        was told, so the failure is raised instead.
        """

        try:
            return self._chat_once(messages, **kwargs)
        except HarnessFailure as error:
            if not self._may_fall_back(error):
                raise
            self._emit("transport_fallback", from_surface=self.surface, to_surface="v1",
                       code=error.code, detail=(error.detail or "")[:300],
                       tool_calls_seen=self.tool_calls_seen)
            self.endpoint = self.fallback_endpoint       # type: ignore[assignment]
            self.surface = "v1"
            self.fallback_endpoint = None
            self.fallbacks += 1
            return self._chat_once(messages, **kwargs)

    def _emit(self, event: str, **fields: Any) -> None:
        if callable(self.on_event):
            try:
                self.on_event(event, **fields)
            except Exception:
                pass

    def _chat_once(self, messages: Sequence[Mapping[str, Any]], **kwargs: Any) -> ChatResponse:
        native = self.endpoint.native
        payload = (self.build_native_payload(messages, **kwargs) if native
                   else self.build_payload(messages, **kwargs))
        self.refuse_credential_in_request(payload)
        body = json.dumps(payload).encode()
        request_sha = hashlib.sha256(body).hexdigest()
        started = time.monotonic()
        raw, status = self._post(self.endpoint.chat_url, body)
        latency_ms = int((time.monotonic() - started) * 1000)
        raw_text = raw.decode(errors="replace")
        if not self.redactor.clean(raw_text):
            raise HarnessFailure("CREDENTIAL_ECHO", "provider echoed a credential")
        try:
            result = json.loads(raw)
        except Exception:
            raise HarnessFailure("TRANSPORT_OR_RESPONSE_ERROR", "provider body was not JSON") from None
        if not isinstance(result, dict) or not (result.get("message") if native
                                                else result.get("choices")):
            raise HarnessFailure("TRANSPORT_OR_RESPONSE_ERROR",
                                 self.redactor.scrub(json.dumps(result))[:500])
        reduce = normalise_native if native else normalise
        response = reduce(result, raw_sha=hashlib.sha256(raw).hexdigest(), raw_bytes=len(raw),
                          latency_ms=latency_ms, request_sha=request_sha,
                          request_bytes=len(body), http_status=status,
                          redactor=self.redactor)
        if response.tool_calls:
            self.tool_calls_seen = True
        return response


def _native_arguments(arguments: Any) -> Any:
    """Native tool-call arguments are a JSON object; /v1 sends a JSON string."""

    if isinstance(arguments, str):
        try:
            parsed = json.loads(arguments or "{}")
        except Exception:
            return arguments          # unparseable: hand it on unchanged, visibly
        return parsed if isinstance(parsed, dict) else arguments
    return arguments


def to_native_messages(messages: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """The harness's internal (OpenAI-shaped) messages, in Ollama's native shape.

    Three differences, and they are the whole translation: a tool reply is
    addressed by ``tool_name`` rather than ``tool_call_id``; a tool call's
    arguments are a JSON **object**, not a JSON string; and there is no
    ``type: "function"`` wrapper on a call.
    """

    translated: list[dict[str, Any]] = []
    for message in messages:
        role = message.get("role")
        if role == "tool":
            translated.append({"role": "tool",
                               "tool_name": message.get("name") or "",
                               "content": message.get("content") or ""})
            continue
        entry: dict[str, Any] = {"role": role, "content": message.get("content") or ""}
        calls = message.get("tool_calls") or []
        if calls:
            entry["tool_calls"] = [
                {"id": call.get("id") or "",
                 "function": {"name": (call.get("function") or {}).get("name", ""),
                              "arguments": _native_arguments(
                                  (call.get("function") or {}).get("arguments"))}}
                for call in calls]
        translated.append(entry)
    return translated


def from_native_tool_calls(message: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Native ``message.tool_calls`` in the harness's internal shape."""

    calls: list[dict[str, Any]] = []
    for index, call in enumerate(message.get("tool_calls") or []):
        function = dict(call.get("function") or {})
        calls.append({"id": call.get("id") or f"call_native_{index}",
                      "type": "function",
                      "function": {"name": function.get("name", ""),
                                   "arguments": function.get("arguments")
                                   if function.get("arguments") is not None else {}}})
    return calls


def normalise_native(result: Mapping[str, Any], *, raw_sha: str, raw_bytes: int,
                     latency_ms: int, request_sha: str, request_bytes: int,
                     http_status: int, redactor: Redactor | None = None) -> ChatResponse:
    """An Ollama ``/api/chat`` body reduced to the same :class:`ChatResponse`.

    Everything downstream — the loop, the transcript, the status rules — sees
    one representation whichever surface answered. Native reasoning arrives as
    ``message.thinking``; it is hashed, counted and dropped here exactly as on
    the other surface.
    """

    redactor = redactor or REDACTOR
    message = result.get("message") or {}
    content = message.get("content") or ""
    if not isinstance(content, str):
        content = json.dumps(content, ensure_ascii=False)
    reasoning = message.get("thinking") or message.get("reasoning") or ""
    if not isinstance(reasoning, str):
        reasoning = json.dumps(reasoning, ensure_ascii=False)
    prompt_tokens = result.get("prompt_eval_count")
    completion_tokens = result.get("eval_count")
    usage: dict[str, Any] = {}
    if isinstance(prompt_tokens, int):
        usage["prompt_tokens"] = prompt_tokens
    if isinstance(completion_tokens, int):
        usage["completion_tokens"] = completion_tokens
    if usage.get("prompt_tokens") is not None and usage.get("completion_tokens") is not None:
        usage["total_tokens"] = usage["prompt_tokens"] + usage["completion_tokens"]
    if isinstance(result.get("prompt_eval_cached_count"), int):
        usage["prompt_tokens_details"] = {"cached_tokens": result["prompt_eval_cached_count"]}
    return ChatResponse(
        content=redactor.scrub(content),
        tool_calls=from_native_tool_calls(message),
        finish_reason=result.get("done_reason"),
        usage=usage,
        returned_model=result.get("model"),
        response_id=result.get("created_at"),
        reasoning_present=bool(reasoning),
        reasoning_sha256=sha256_text(reasoning) if reasoning else None,
        reasoning_chars=len(reasoning),
        reasoning_tokens=None,
        latency_ms=latency_ms,
        request_sha256=request_sha,
        request_bytes=request_bytes,
        response_sha256=raw_sha,
        response_bytes=raw_bytes,
        http_status=http_status,
    )


def normalise(result: Mapping[str, Any], *, raw_sha: str, raw_bytes: int, latency_ms: int,
              request_sha: str, request_bytes: int, http_status: int,
              redactor: Redactor | None = None) -> ChatResponse:
    """An OpenAI-shaped body reduced to :class:`ChatResponse`.

    Native reasoning text is read once, hashed, counted and dropped on the
    floor. It is never stored on the object, never returned and never fed back
    into another call.
    """

    redactor = redactor or REDACTOR
    choice = result["choices"][0]
    message = choice.get("message") or {}
    content = message.get("content") or ""
    if not isinstance(content, str):
        content = json.dumps(content, ensure_ascii=False)
    reasoning = message.get("reasoning_content") or message.get("reasoning") or ""
    if not isinstance(reasoning, str):
        reasoning = json.dumps(reasoning, ensure_ascii=False)
    usage = dict(result.get("usage") or {})
    details = usage.get("completion_tokens_details")
    reasoning_tokens = None
    if isinstance(details, Mapping) and isinstance(details.get("reasoning_tokens"), int):
        reasoning_tokens = details["reasoning_tokens"]
    tool_calls = message.get("tool_calls") or []
    if not isinstance(tool_calls, list):
        tool_calls = []
    return ChatResponse(
        content=redactor.scrub(content),
        tool_calls=[dict(call) for call in tool_calls],
        finish_reason=choice.get("finish_reason"),
        usage=usage,
        returned_model=result.get("model"),
        response_id=result.get("id"),
        reasoning_present=bool(reasoning),
        reasoning_sha256=sha256_text(reasoning) if reasoning else None,
        reasoning_chars=len(reasoning),
        reasoning_tokens=reasoning_tokens,
        latency_ms=latency_ms,
        request_sha256=request_sha,
        request_bytes=request_bytes,
        response_sha256=raw_sha,
        response_bytes=raw_bytes,
        http_status=http_status,
    )


# --------------------------------------------------------------------------
# Sandbox
# --------------------------------------------------------------------------


def _ignore_secrets(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in SANDBOX_EXCLUDES or name.endswith(".pyc")}


class Sandbox:
    """A copy of the paths a task declares. The live repository is never touched.

    Every tool path is resolved and checked against the sandbox root, so a
    ``..`` escape, an absolute path or a symlink pointing out of the tree is
    refused before any read or write happens.
    """

    def __init__(self, root: Path | str):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def populate(self, repo_root: Path | str, context_paths: Sequence[str]) -> list[str]:
        """Copy each declared repo-relative path in. ``.env`` is never copied."""

        repo_root = Path(repo_root).resolve()
        copied: list[str] = []
        for relative in context_paths:
            if Path(relative).is_absolute() or ".." in Path(relative).parts:
                raise HarnessFailure("CONTEXT_PATH_REFUSED", f"{relative!r} is not repo-relative")
            source = (repo_root / relative).resolve()
            if not str(source).startswith(str(repo_root)):
                raise HarnessFailure("CONTEXT_PATH_REFUSED", f"{relative!r} escapes the repo root")
            if not source.exists():
                raise HarnessFailure("CONTEXT_PATH_MISSING", f"{relative!r} does not exist")
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, target, ignore=_ignore_secrets,
                                symlinks=False, dirs_exist_ok=True)
            else:
                if source.name in SANDBOX_EXCLUDES:
                    raise HarnessFailure("CONTEXT_PATH_REFUSED", f"{relative!r} is excluded")
                shutil.copy2(source, target)
            copied.append(relative)
        return copied

    # -- confinement ---------------------------------------------------------

    def resolve(self, relative: str) -> Path:
        if not isinstance(relative, str) or not relative.strip():
            raise HarnessFailure("PATH_REFUSED", "path must be a non-empty string")
        candidate = Path(relative)
        if candidate.is_absolute():
            raise HarnessFailure("PATH_REFUSED", f"absolute path refused: {relative!r}")
        resolved = (self.root / candidate).resolve()
        if resolved != self.root and self.root not in resolved.parents:
            raise HarnessFailure("PATH_REFUSED", f"path escapes the sandbox: {relative!r}")
        return resolved

    def relative(self, path: Path) -> str:
        return str(Path(path).resolve().relative_to(self.root))

    # -- snapshots -----------------------------------------------------------

    def snapshot(self) -> dict[str, str]:
        state: dict[str, str] = {}
        for path in sorted(self.root.rglob("*")):
            if path.is_file() and not path.is_symlink():
                state[self.relative(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
        return state

    def diff(self, before: Mapping[str, str]) -> list[dict[str, Any]]:
        after = self.snapshot()
        changes: list[dict[str, Any]] = []
        for name in sorted(set(before) | set(after)):
            was, now = before.get(name), after.get(name)
            if was == now:
                continue
            change = "added" if was is None else ("removed" if now is None else "modified")
            entry: dict[str, Any] = {"path": name, "change": change, "sha256": now}
            if now is not None:
                entry["bytes"] = (self.root / name).stat().st_size
            changes.append(entry)
        return changes


# --------------------------------------------------------------------------
# Tools
# --------------------------------------------------------------------------

TOOL_SCHEMAS: list[dict[str, Any]] = [
    {"type": "function", "function": {
        "name": "read_file",
        "description": "Read a UTF-8 text file from the task sandbox. Paths are relative to the sandbox root.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string", "description": "Sandbox-relative file path."}},
            "required": ["path"]}}},
    {"type": "function", "function": {
        "name": "list_dir",
        "description": "List the entries of a directory in the task sandbox. Use '.' for the sandbox root.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string", "description": "Sandbox-relative directory path."}},
            "required": ["path"]}}},
    {"type": "function", "function": {
        "name": "grep",
        "description": "Search files under a sandbox path for a Python regular expression. Returns matching lines with line numbers.",
        "parameters": {"type": "object", "properties": {
            "pattern": {"type": "string", "description": "Python regular expression."},
            "path": {"type": "string", "description": "Sandbox-relative file or directory to search."}},
            "required": ["pattern", "path"]}}},
    {"type": "function", "function": {
        "name": "write_file",
        "description": "Write a UTF-8 text file in the task sandbox, creating parent directories. Overwrites.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string", "description": "Sandbox-relative file path."},
            "content": {"type": "string", "description": "Full new file content."}},
            "required": ["path", "content"]}}},
    {"type": "function", "function": {
        "name": "run_command",
        "description": ("Run one allow-listed command inside the sandbox. Allowed forms only: "
                        "'python3 -m unittest ...', 'python3 -m pytest ...', 'python3 -c ...', "
                        "'python3 <file.py> ...'. Anything else is refused."),
        "parameters": {"type": "object", "properties": {
            "command": {"type": "string", "description": "The command line to run."}},
            "required": ["command"]}}},
]

TOOL_NAMES = tuple(schema["function"]["name"] for schema in TOOL_SCHEMAS)

#: Environment variables stripped from every ``run_command`` subprocess, so
#: model-authored code can never read the credential this harness spends.
_SECRET_ENVS = ("OLLAMA_API_KEY", "DEEPSEEK_API_KEY", "ANTHROPIC_API_KEY",
                "OPENAI_API_KEY", "OLLAMA_TOKEN")


def check_command(command: str) -> list[str]:
    """Return the argv for an allow-listed command, or raise ``COMMAND_REFUSED``."""

    if not isinstance(command, str) or not command.strip():
        raise HarnessFailure("COMMAND_REFUSED", "empty command")
    try:
        argv = shlex.split(command)
    except ValueError as error:
        raise HarnessFailure("COMMAND_REFUSED", f"unparseable command: {error}") from None
    if not argv:
        raise HarnessFailure("COMMAND_REFUSED", "empty command")
    if argv[0] != "python3":
        raise HarnessFailure("COMMAND_REFUSED", f"only python3 is allowed, got {argv[0]!r}")
    if len(argv) >= 3 and argv[1] == "-m" and argv[2] in {"unittest", "pytest"}:
        return argv
    if len(argv) >= 3 and argv[1] == "-c":
        return argv
    if len(argv) >= 2 and not argv[1].startswith("-") and argv[1].endswith(".py"):
        return argv
    raise HarnessFailure(
        "COMMAND_REFUSED",
        "allowed: 'python3 -m unittest ...', 'python3 -m pytest ...', "
        "'python3 -c ...', 'python3 <file.py> ...'")


class ToolBox:
    """The five tools, all confined to one :class:`Sandbox`."""

    def __init__(self, sandbox: Sandbox, *, command_timeout: int = 120,
                 output_cap: int = 20000, read_cap: int = 200000,
                 write_cap: int = 1000000, redactor: Redactor | None = None):
        self.sandbox = sandbox
        self.command_timeout = command_timeout
        self.output_cap = output_cap
        self.read_cap = read_cap
        self.write_cap = write_cap
        self.redactor = redactor or REDACTOR
        self.counts: dict[str, int] = {name: 0 for name in TOOL_NAMES}
        self.files_written: list[str] = []

    def dispatch(self, name: str, arguments: Mapping[str, Any]) -> str:
        if name not in TOOL_NAMES:
            return f"ERROR: unknown tool {name!r}. Available: {', '.join(TOOL_NAMES)}"
        self.counts[name] = self.counts.get(name, 0) + 1
        handler = getattr(self, "_" + name)
        try:
            result = handler(**dict(arguments))
        except HarnessFailure as error:
            return f"ERROR: {error.code}: {error.detail}"
        except TypeError as error:
            return f"ERROR: BAD_ARGUMENTS: {error}"
        except Exception as error:  # a tool must never kill the loop
            return f"ERROR: {type(error).__name__}: {error}"
        return self.redactor.scrub(result)

    # -- the tools -----------------------------------------------------------

    def _read_file(self, path: str) -> str:
        target = self.sandbox.resolve(path)
        if not target.is_file():
            return f"ERROR: NOT_A_FILE: {path}"
        data = target.read_text(encoding="utf-8", errors="replace")
        if len(data) > self.read_cap:
            return data[:self.read_cap] + f"\n... [truncated at {self.read_cap} characters]"
        return data

    def _list_dir(self, path: str = ".") -> str:
        target = self.sandbox.resolve(path)
        if not target.is_dir():
            return f"ERROR: NOT_A_DIRECTORY: {path}"
        lines = []
        for entry in sorted(target.iterdir()):
            kind = "dir " if entry.is_dir() else "file"
            size = entry.stat().st_size if entry.is_file() else 0
            lines.append(f"{kind} {self.sandbox.relative(entry)} ({size} bytes)")
        return "\n".join(lines) or "(empty directory)"

    def _grep(self, pattern: str, path: str = ".") -> str:
        target = self.sandbox.resolve(path)
        try:
            regex = re.compile(pattern)
        except re.error as error:
            return f"ERROR: BAD_PATTERN: {error}"
        files = [target] if target.is_file() else sorted(
            p for p in target.rglob("*") if p.is_file() and not p.is_symlink())
        hits: list[str] = []
        for candidate in files:
            try:
                text = candidate.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for number, line in enumerate(text.splitlines(), 1):
                if regex.search(line):
                    hits.append(f"{self.sandbox.relative(candidate)}:{number}: {line.rstrip()[:400]}")
                    if len(hits) >= 400:
                        hits.append("... [truncated at 400 matches]")
                        return "\n".join(hits)
        return "\n".join(hits) or "(no matches)"

    def _write_file(self, path: str, content: str) -> str:
        target = self.sandbox.resolve(path)
        if not isinstance(content, str):
            content = json.dumps(content, ensure_ascii=False)
        if len(content) > self.write_cap:
            return f"ERROR: CONTENT_TOO_LARGE: {len(content)} > {self.write_cap}"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        relative = self.sandbox.relative(target)
        if relative not in self.files_written:
            self.files_written.append(relative)
        return (f"wrote {relative} ({len(content)} characters, "
                f"sha256 {sha256_text(content)[:16]})")

    def _run_command(self, command: str) -> str:
        argv = check_command(command)
        environment = {k: v for k, v in os.environ.items() if k not in _SECRET_ENVS}
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        try:
            completed = subprocess.run(
                argv, cwd=str(self.sandbox.root), env=environment, capture_output=True,
                text=True, timeout=self.command_timeout, check=False)
        except subprocess.TimeoutExpired:
            return f"ERROR: TIMEOUT after {self.command_timeout}s: {command}"
        except FileNotFoundError:
            return f"ERROR: NOT_FOUND: {argv[0]}"
        half = self.output_cap // 2
        out = completed.stdout[:half]
        err = completed.stderr[:half]
        parts = [f"exit_code: {completed.returncode}"]
        if out:
            parts.append("stdout:\n" + out + ("\n... [truncated]" if len(completed.stdout) > half else ""))
        if err:
            parts.append("stderr:\n" + err + ("\n... [truncated]" if len(completed.stderr) > half else ""))
        return "\n".join(parts)


# --------------------------------------------------------------------------
# Task specification and result
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class TaskSpec:
    """One unit of work handed to the worker."""

    id: str
    title: str
    prompt: str
    context_paths: tuple[str, ...] = ()
    expected_outputs: tuple[str, ...] = ()
    evaluation: str = ""
    mode: str = "tools"             # "tools" or "packed"
    max_iterations: int = 40
    max_tokens: int = MAX_TOKENS
    command_timeout: int = 120
    verify_command: str | None = None   # packed mode second turn
    repo_root: str = str(DEFAULT_REPO_ROOT)
    #: "default" | "low" | "off" — production tasks run "low", which the native
    #: surface honours (PROBE-REASONING.md) and /v1 ignores.
    reasoning: str | None = "low"
    #: "native" (Ollama /api/chat, the default) or "v1" (OpenAI-compatible).
    transport: str = "native"

    def __post_init__(self) -> None:
        if self.reasoning not in REASONING_SETTINGS and self.reasoning is not None:
            raise HarnessFailure("TASK_SPEC_INVALID",
                                 f"reasoning must be one of {REASONING_SETTINGS}, "
                                 f"not {self.reasoning!r}")
        if self.transport not in TRANSPORT_SURFACES:
            raise HarnessFailure("TASK_SPEC_INVALID",
                                 f"transport must be one of {TRANSPORT_SURFACES}, "
                                 f"not {self.transport!r}")

    @staticmethod
    def from_mapping(raw: Mapping[str, Any]) -> "TaskSpec":
        known = {f for f in TaskSpec.__dataclass_fields__}
        unknown = set(raw) - known
        if unknown:
            raise HarnessFailure("TASK_SPEC_INVALID", f"unknown fields: {sorted(unknown)}")
        data = dict(raw)
        for key in ("context_paths", "expected_outputs"):
            if key in data:
                data[key] = tuple(data[key])
        return TaskSpec(**data)

    def public(self) -> dict[str, Any]:
        return asdict(self)


#: Every status a run can end with, and what each one claims.
#:
#: ``COMPLETE`` is the only one that claims the work was done: the final turn
#: finished on its own (``finish_reason: stop``) *and* every declared expected
#: output exists in the sandbox. The other four each name a different way a run
#: stopped short, so that "it ended" is never read as "it delivered".
STATUSES = {
    "COMPLETE": "final turn finished and every expected output exists",
    "INCOMPLETE_TURN": "final turn hit a non-stop boundary with no tool call and no content",
    "NO_DELIVERABLE": "final turn finished but an expected output is missing",
    "ITERATION_CAP": "the iteration cap was reached without a final answer",
    "HARNESS_FAILURE": "the harness or the provider failed the run",
}

#: The harness failure recorded on an ``INCOMPLETE_TURN``: the per-turn token
#: budget was spent, and on this provider it was spent on native reasoning that
#: produced neither a tool call nor visible content. A resource boundary on the
#: turn, not a completion.
TURN_BUDGET_EXHAUSTED = "TURN_BUDGET_EXHAUSTED_BY_REASONING"


def is_stop_finish(finish_reason: str | None) -> bool:
    """True only for ``stop``. Every other finish reason ended at a boundary.

    ``length`` is the one seen in practice (the turn ran out of tokens), but
    ``content_filter``, a provider-specific reason and a missing reason are all
    treated the same way: the turn did not finish on its own terms.
    """

    return finish_reason == "stop"


def expected_output_state(sandbox: "Sandbox", expected_outputs: Sequence[str]) -> tuple[list[str], list[str]]:
    """Split ``expected_outputs`` into (present, missing) inside ``sandbox``.

    A declared output ending in ``/`` — or naming a directory — counts as
    present only when the directory exists *and* holds at least one file: an
    empty directory is not a deliverable.
    """

    present: list[str] = []
    missing: list[str] = []
    for declared in expected_outputs:
        try:
            path = sandbox.resolve(declared.rstrip("/") or ".")
        except HarnessFailure:
            missing.append(declared)
            continue
        if path.is_dir():
            found = any(child.is_file() for child in path.rglob("*"))
        else:
            found = path.is_file()
        (present if found else missing).append(declared)
    return present, missing


@dataclass
class TaskResult:
    """What one run of one task produced."""

    task_id: str
    title: str
    status: str                      # see STATUSES
    mode: str
    final_text: str
    files_written: list[dict[str, Any]] = field(default_factory=list)
    expected_outputs_present: list[str] = field(default_factory=list)
    expected_outputs_missing: list[str] = field(default_factory=list)
    tool_calls: dict[str, int] = field(default_factory=dict)
    tool_call_total: int = 0
    iterations: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    wall_seconds: float = 0.0
    finish_reason: str | None = None
    harness_failure: str | None = None
    harness_detail: str | None = None
    malformed_tool_call_retries: int = 0
    reasoning_calls: int = 0
    #: Characters of native reasoning per turn, in order. The text is never kept.
    reasoning_chars: list[int] = field(default_factory=list)
    reasoning_retries: int = 0
    transport_requested: str = ""
    transport_used: str = ""
    transport_fallbacks: int = 0
    transcript_path: str = ""
    sandbox_dir: str = ""

    def to_json(self) -> dict[str, Any]:
        return asdict(self)


# --------------------------------------------------------------------------
# Transcript
# --------------------------------------------------------------------------


class Transcript:
    """Append-only JSONL. Every line is redacted before it reaches disk."""

    def __init__(self, path: Path | str, redactor: Redactor | None = None):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.redactor = redactor or REDACTOR
        self._lock = threading.Lock()
        self._sequence = 0

    def write(self, event: str, **fields: Any) -> dict[str, Any]:
        with self._lock:
            self._sequence += 1
            record = {"seq": self._sequence, "event": event,
                      "at": datetime.now(timezone.utc).isoformat(), **fields}
            line = self.redactor.scrub(json.dumps(record, ensure_ascii=False, default=str))
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")
        return json.loads(line)


# --------------------------------------------------------------------------
# Prompts
# --------------------------------------------------------------------------

SYSTEM_PROMPT_TOOLS = """\
You are a software engineering worker agent. You are working inside a sandbox \
directory that holds a copy of the files this task declares. The real \
repository is not reachable from here and nothing you do can touch it.

Task: {title}

Tools available to you (call them; do not describe calling them):
  read_file(path)            read a sandbox file
  list_dir(path)             list a sandbox directory ('.' is the sandbox root)
  grep(pattern, path)        search for a Python regex under a sandbox path
  write_file(path, content)  write a whole sandbox file (overwrites)
  run_command(command)       run one of: 'python3 -m unittest ...',
                             'python3 -m pytest ...', 'python3 -c ...',
                             'python3 <file.py> ...'   (nothing else is allowed)

Rules:
* All paths are relative to the sandbox root. Absolute paths and '..' are refused.
* Inspect before you edit: read a file before rewriting it.
* write_file replaces the whole file, so include the complete new content.
* Verify your work by running the tests with run_command before you finish.
* You have at most {max_iterations} turns. Work steadily; do not stall.
* When the work is done, reply with a final message (no tool calls) that states
  what you changed, which files you wrote, and the result of the last test run.

Files copied into the sandbox for this task:
{file_list}

Expected outputs:
{expected_outputs}
"""

SYSTEM_PROMPT_PACKED = """\
You are a software engineering worker agent. You cannot call tools in this \
mode. The contents of every file this task declares are inlined below.

Task: {title}

To change or create a file, emit a fenced code block whose info string is \
`path=<relative/path>`, containing the COMPLETE new content of that file:

```path=example/module.py
def twice(x):
    return 2 * x
```

Rules:
* One fenced block per file. The whole file, not a diff, not an excerpt.
* Paths are relative to the sandbox root; absolute paths and '..' are refused.
* Outside the fenced blocks, explain briefly what you changed and why.

Expected outputs:
{expected_outputs}
"""


def _render_file_list(sandbox: Sandbox, limit: int = 200) -> str:
    names = [name for name in sorted(sandbox.snapshot())][:limit]
    return "\n".join("  " + name for name in names) or "  (none)"


def _render_expected(task: TaskSpec) -> str:
    return "\n".join("  " + item for item in task.expected_outputs) or "  (none declared)"


FENCE_RE = re.compile(r"```path=(?P<path>[^\s`]+)\n(?P<body>.*?)```", re.DOTALL)


def parse_path_fences(text: str) -> list[tuple[str, str]]:
    """``[(path, content)]`` for every ```` ```path=... ```` block in ``text``."""

    return [(match.group("path").strip(), match.group("body"))
            for match in FENCE_RE.finditer(text or "")]


# --------------------------------------------------------------------------
# The agent
# --------------------------------------------------------------------------


class KimiAgent:
    """The agentic loop. ``transport`` is anything with ``chat(messages, **kw)``."""

    def __init__(self, task: TaskSpec, *, transport: Any, sandbox: Sandbox,
                 transcript: Transcript, redactor: Redactor | None = None):
        self.task = task
        self.transport = transport
        self.sandbox = sandbox
        self.transcript = transcript
        self.redactor = redactor or REDACTOR
        self.tools = ToolBox(sandbox, command_timeout=task.command_timeout, redactor=self.redactor)
        self.messages: list[dict[str, Any]] = []
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.iterations = 0
        self.malformed_retries = 0
        self.reasoning_calls = 0
        self.incomplete_turn: dict[str, Any] | None = None
        self.reasoning_retries = 0
        self.reasoning_chars_per_turn: list[int] = []

    # -- bookkeeping ---------------------------------------------------------

    def _account(self, response: ChatResponse) -> None:
        usage = response.usage or {}
        if isinstance(usage.get("prompt_tokens"), int):
            self.prompt_tokens += usage["prompt_tokens"]
        if isinstance(usage.get("completion_tokens"), int):
            self.completion_tokens += usage["completion_tokens"]
        if response.reasoning_present:
            self.reasoning_calls += 1
        self.reasoning_chars_per_turn.append(response.reasoning_chars)

    def _record_request(self, payload_messages: Sequence[Mapping[str, Any]], **settings: Any) -> None:
        self.transcript.write(
            "request", iteration=self.iterations,
            messages=[_message_summary(m) for m in payload_messages],
            message_count=len(payload_messages), settings=settings)

    def _record_response(self, response: ChatResponse) -> None:
        self.transcript.write(
            "response", iteration=self.iterations, content=response.content,
            tool_calls=response.tool_calls, finish_reason=response.finish_reason,
            usage=response.usage, returned_model=response.returned_model,
            response_id=response.response_id, latency_ms=response.latency_ms,
            http_status=response.http_status,
            request_sha256=response.request_sha256, request_bytes=response.request_bytes,
            response_sha256=response.response_sha256, response_bytes=response.response_bytes,
            reasoning_content_present=response.reasoning_present,
            reasoning_content_sha256=response.reasoning_sha256,
            reasoning_content_chars=response.reasoning_chars,
            reasoning_tokens=response.reasoning_tokens,
            # Ollama's kimi-k3 does not report completion_tokens_details, so the
            # count below is derived here (4 characters per token) and labelled
            # as derived. The text itself is never written: only this digest.
            reasoning_tokens_estimated=(max(1, response.reasoning_chars // 4)
                                        if response.reasoning_chars else 0),
            reasoning_content_persisted=False)

    @staticmethod
    def _incomplete(response: ChatResponse) -> bool:
        """True when this turn stopped at a boundary having produced nothing.

        Pure: it decides, it does not record. The recording happens once, in
        :meth:`_record_incomplete_turn`, so that a turn which is retried and a
        turn which ends the run are each written down exactly once.
        """

        if response.tool_calls or (response.content or "").strip():
            return False
        return not is_stop_finish(response.finish_reason)

    def _record_incomplete_turn(self, response: ChatResponse) -> bool:
        """Write the evidence for one budget-exhausted turn. Returns True.

        A non-``stop`` finish reason with no tool call and no visible content is
        not a completion: the whole per-turn budget was spent somewhere the
        harness cannot see — on this provider, on native reasoning. The
        evidence is recorded here (completion tokens for the turn, the digest
        and size of the reasoning that consumed them) so the boundary stays
        legible in the transcript without the reasoning text ever being kept.
        """

        usage = response.usage or {}
        completion_tokens = usage.get("completion_tokens")
        estimated = max(1, response.reasoning_chars // 4) if response.reasoning_chars else 0
        self.incomplete_turn = {
            "iteration": self.iterations,
            "finish_reason": response.finish_reason,
            "completion_tokens": completion_tokens,
            "max_tokens": self.task.max_tokens,
            "reasoning_content_sha256": response.reasoning_sha256,
            "reasoning_content_chars": response.reasoning_chars,
            "reasoning_tokens": response.reasoning_tokens,
            "reasoning_tokens_estimated": estimated,
        }
        self.transcript.write(
            "incomplete_turn", iteration=self.iterations,
            code=TURN_BUDGET_EXHAUSTED,
            finish_reason=response.finish_reason,
            completion_tokens=completion_tokens,
            max_tokens=self.task.max_tokens,
            tool_calls=0, content_chars=len(response.content or ""),
            reasoning_content_present=response.reasoning_present,
            reasoning_content_sha256=response.reasoning_sha256,
            reasoning_content_chars=response.reasoning_chars,
            reasoning_tokens=response.reasoning_tokens,
            reasoning_tokens_estimated=estimated,
            reasoning_calls=self.reasoning_calls,
            reasoning_content_persisted=False)
        return True

    def _reasoning_control(self) -> str | None:
        """The lowest reasoning setting this transport honours, if any.

        Duck-typed on purpose: a transport that cannot turn reasoning down
        simply does not offer ``reasoning_control``, and the loop keeps its
        current behaviour (record the boundary and stop).
        """

        control = getattr(self.transport, "reasoning_control", None)
        if not callable(control):
            return None
        try:
            return control()
        except Exception:
            return None

    def _turn(self, settings: Mapping[str, Any]) -> ChatResponse:
        """One model turn, with the single retry a budget-exhausted turn earns.

        A turn that spends its whole budget on reasoning produced nothing to
        act on. Where the endpoint honours a reasoning control, the *same* turn
        is asked again once at the lowest setting; where it does not, the
        boundary is recorded and the run stops, exactly as before. One retry
        per run, never two.
        """

        response = self.transport.chat(self.messages, tools=TOOL_SCHEMAS, tool_choice="auto",
                                       max_tokens=self.task.max_tokens,
                                       reasoning=self.task.reasoning)
        self._account(response)
        self._record_response(response)
        if not self._incomplete(response):
            return response
        lowest = self._reasoning_control()
        if lowest is None or self.reasoning_retries:
            return response
        self._record_incomplete_turn(response)
        self.reasoning_retries += 1
        self.transcript.write("incomplete_turn_retry", iteration=self.iterations,
                              reason=TURN_BUDGET_EXHAUSTED, attempt=1,
                              reasoning_from=self.task.reasoning, reasoning_to=lowest,
                              max_tokens=self.task.max_tokens)
        self._record_request(self.messages, **{**dict(settings), "reasoning": lowest,
                                               "retry_of": "incomplete_turn"})
        retried = self.transport.chat(self.messages, tools=TOOL_SCHEMAS, tool_choice="auto",
                                      max_tokens=self.task.max_tokens, reasoning=lowest)
        self._account(retried)
        self._record_response(retried)
        return retried

    def incomplete_turn_detail(self) -> str:
        """One line naming the boundary, for ``TaskResult.harness_detail``."""

        evidence = self.incomplete_turn or {}
        return ("turn {iteration} finished as {finish_reason} with no tool call and no content: "
                "{completion_tokens} completion tokens of a {max_tokens} budget, "
                "reasoning {reasoning_content_chars} chars "
                "(sha256 {sha}, ~{reasoning_tokens_estimated} tokens)").format(
                    sha=str(evidence.get("reasoning_content_sha256"))[:16], **evidence)

    # -- tools mode ----------------------------------------------------------

    def run_tools_mode(self) -> tuple[str, str, str | None]:
        system = SYSTEM_PROMPT_TOOLS.format(
            title=self.task.title, max_iterations=self.task.max_iterations,
            file_list=_render_file_list(self.sandbox),
            expected_outputs=_render_expected(self.task))
        self.messages = [{"role": "system", "content": system},
                         {"role": "user", "content": self.task.prompt}]
        settings = {"max_tokens": self.task.max_tokens, "tool_choice": "auto",
                    "reasoning": self.task.reasoning,
                    "tools": [schema["function"]["name"] for schema in TOOL_SCHEMAS]}
        final_text = ""
        finish_reason = None
        retry_used = False
        while self.iterations < self.task.max_iterations:
            self.iterations += 1
            checkpoint = len(self.messages)
            self._record_request(self.messages, **settings)
            response = self._turn(settings)
            finish_reason = response.finish_reason
            if not response.tool_calls:
                final_text = response.content
                if self._incomplete(response):
                    self._record_incomplete_turn(response)
                    return final_text, "INCOMPLETE_TURN", finish_reason
                return final_text, "COMPLETE", finish_reason
            self.messages.append(response.assistant_message())
            malformed = False
            for call in response.tool_calls:
                function = call.get("function") or {}
                name = function.get("name", "")
                raw_arguments = function.get("arguments")
                if isinstance(raw_arguments, Mapping):
                    arguments: Any = dict(raw_arguments)
                else:
                    try:
                        arguments = json.loads(raw_arguments or "{}")
                        if not isinstance(arguments, dict):
                            raise ValueError("arguments were not a JSON object")
                    except Exception as error:
                        malformed = True
                        self.transcript.write(
                            "malformed_tool_call", iteration=self.iterations,
                            tool=name, tool_call_id=call.get("id"),
                            arguments_sha256=sha256_text(str(raw_arguments)),
                            arguments_chars=len(str(raw_arguments or "")),
                            error=str(error), retry_used=retry_used)
                        break
                started = time.monotonic()
                self.transcript.write("tool_call", iteration=self.iterations, tool=name,
                                      tool_call_id=call.get("id"), arguments=arguments)
                output = self.tools.dispatch(name, arguments)
                self.transcript.write(
                    "tool_result", iteration=self.iterations, tool=name,
                    tool_call_id=call.get("id"), ok=not output.startswith("ERROR:"),
                    elapsed_ms=int((time.monotonic() - started) * 1000),
                    output_chars=len(output), output=output[:8000])
                self.messages.append({"role": "tool", "tool_call_id": call.get("id", ""),
                                      "name": name, "content": output})
            if malformed:
                if retry_used:
                    raise HarnessFailure("MALFORMED_TOOL_CALL_JSON",
                                         "tool-call arguments were not JSON twice")
                retry_used = True
                self.malformed_retries += 1
                # The one retry this harness allows: drop the unusable assistant
                # turn and every tool reply it produced, and ask again from the
                # exact message list that preceded it.
                del self.messages[checkpoint:]
                self.transcript.write("retry", iteration=self.iterations,
                                      reason="MALFORMED_TOOL_CALL_JSON", attempt=1)
        return final_text, "ITERATION_CAP", finish_reason

    # -- packed-context mode -------------------------------------------------

    def _packed_context(self) -> str:
        blocks = []
        for name in sorted(self.sandbox.snapshot()):
            path = self.sandbox.root / name
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                blocks.append(f"### {name}\n(binary or unreadable, skipped)")
                continue
            blocks.append(f"### {name}\n```\n{text}\n```")
        return "\n\n".join(blocks) or "(no files)"

    def _apply_fences(self, text: str) -> list[str]:
        written: list[str] = []
        for path, content in parse_path_fences(text):
            self.transcript.write("tool_call", iteration=self.iterations,
                                  tool="write_file", arguments={"path": path,
                                                                "content_chars": len(content)})
            output = self.tools.dispatch("write_file", {"path": path, "content": content})
            self.transcript.write("tool_result", iteration=self.iterations, tool="write_file",
                                  ok=not output.startswith("ERROR:"), output=output)
            if not output.startswith("ERROR:"):
                written.append(path)
        return written

    def run_packed_mode(self) -> tuple[str, str, str | None]:
        system = SYSTEM_PROMPT_PACKED.format(title=self.task.title,
                                             expected_outputs=_render_expected(self.task))
        user = (self.task.prompt + "\n\n## Files\n\n" + self._packed_context())
        self.messages = [{"role": "system", "content": system},
                         {"role": "user", "content": user}]
        self.iterations += 1
        self._record_request(self.messages, max_tokens=self.task.max_tokens, mode="packed")
        response = self.transport.chat(self.messages, max_tokens=self.task.max_tokens,
                                       reasoning=self.task.reasoning)
        self._account(response)
        self._record_response(response)
        final_text = response.content
        self._apply_fences(final_text)
        if self.task.verify_command:
            output = self.tools.dispatch("run_command", {"command": self.task.verify_command})
            self.transcript.write("tool_result", iteration=self.iterations, tool="run_command",
                                  ok=not output.startswith("ERROR:"), output=output[:8000])
            if "exit_code: 0" not in output and self.iterations < self.task.max_iterations:
                self.messages.append({"role": "assistant", "content": final_text})
                self.messages.append({"role": "user", "content":
                                      "The verification command did not pass. Output:\n\n"
                                      + output[:8000] +
                                      "\n\nFix the files. Emit complete ```path=... blocks again."})
                self.iterations += 1
                self._record_request(self.messages, max_tokens=self.task.max_tokens, mode="packed")
                response = self.transport.chat(self.messages, max_tokens=self.task.max_tokens,
                                       reasoning=self.task.reasoning)
                self._account(response)
                self._record_response(response)
                final_text = response.content
                self._apply_fences(final_text)
                output = self.tools.dispatch("run_command", {"command": self.task.verify_command})
                self.transcript.write("tool_result", iteration=self.iterations, tool="run_command",
                                      ok=not output.startswith("ERROR:"), output=output[:8000])
        status = ("INCOMPLETE_TURN" if (self._incomplete(response)
                                        and self._record_incomplete_turn(response))
                  else "COMPLETE")
        return final_text, status, response.finish_reason

    def run(self) -> tuple[str, str, str | None]:
        if self.task.mode == "packed":
            return self.run_packed_mode()
        return self.run_tools_mode()


def _message_summary(message: Mapping[str, Any]) -> dict[str, Any]:
    """A transcript-safe view of one message: full text, plus its digest."""

    content = message.get("content")
    text = content if isinstance(content, str) else json.dumps(content, ensure_ascii=False, default=str)
    summary: dict[str, Any] = {"role": message.get("role"), "chars": len(text or ""),
                               "sha256": sha256_text(text or "")}
    if message.get("tool_calls"):
        summary["tool_calls"] = message["tool_calls"]
    if message.get("tool_call_id"):
        summary["tool_call_id"] = message["tool_call_id"]
    if message.get("name"):
        summary["name"] = message["name"]
    summary["content"] = text
    return summary


# --------------------------------------------------------------------------
# run_task
# --------------------------------------------------------------------------


def run_task(task: TaskSpec, *, transport: Any = None, runs_dir: Path | str | None = None,
             repo_root: Path | str | None = None, redactor: Redactor | None = None,
             reuse_sandbox: bool = False) -> TaskResult:
    """Run one task end to end and return its :class:`TaskResult`.

    ``transport`` defaults to a live :class:`KimiClient`; tests pass a fake.
    Every message, tool call, tool result, usage figure and latency lands in
    ``runs/<task id>/transcript.jsonl``; the sandbox lives beside it.
    """

    redactor = redactor or REDACTOR
    runs_dir = Path(runs_dir) if runs_dir else DEFAULT_RUNS_DIR
    run_dir = runs_dir / task.id
    run_dir.mkdir(parents=True, exist_ok=True)
    sandbox_dir = run_dir / "sandbox"
    if sandbox_dir.exists() and not reuse_sandbox:
        shutil.rmtree(sandbox_dir)
    sandbox = Sandbox(sandbox_dir)
    transcript = Transcript(run_dir / "transcript.jsonl", redactor)
    started = time.monotonic()
    transcript.write("task_start", task=task.public(), harness={
        "max_concurrency": MAX_CONCURRENCY, "max_tokens": task.max_tokens,
        "timeout_seconds": TIMEOUT_SECONDS, "mode": task.mode,
        "transport": task.transport, "reasoning": task.reasoning,
        "reasoning_content_persisted": False})
    result = TaskResult(task_id=task.id, title=task.title, status="HARNESS_FAILURE",
                        mode=task.mode, final_text="",
                        transcript_path=str(transcript.path), sandbox_dir=str(sandbox.root))
    agent = None
    try:
        sandbox.populate(repo_root or task.repo_root, task.context_paths)
        before = sandbox.snapshot()
        if transport is None:
            transport = KimiClient(redactor=redactor, surface=task.transport,
                                   on_event=transcript.write)
        agent = KimiAgent(task, transport=transport, sandbox=sandbox,
                          transcript=transcript, redactor=redactor)
        final_text, status, finish_reason = agent.run()
        result.final_text = final_text
        result.status = status
        result.finish_reason = finish_reason
        if status == "ITERATION_CAP":
            result.harness_failure = "ITERATION_CAP"
            result.harness_detail = f"reached {task.max_iterations} iterations without a final answer"
        elif status == "INCOMPLETE_TURN":
            result.harness_failure = TURN_BUDGET_EXHAUSTED
            result.harness_detail = agent.incomplete_turn_detail()
        result.files_written = sandbox.diff(before)
        present, missing = expected_output_state(sandbox, task.expected_outputs)
        result.expected_outputs_present = present
        result.expected_outputs_missing = missing
        # COMPLETE claims the work was done, so it survives only when every
        # declared output is actually there. A run that talked its way to
        # ``stop`` without writing one is NO_DELIVERABLE, not a completion.
        if result.status == "COMPLETE" and missing:
            result.status = "NO_DELIVERABLE"
            result.harness_detail = ("expected outputs missing: " + ", ".join(missing))[:1000]
    except HarnessFailure as error:
        result.status = "HARNESS_FAILURE"
        result.harness_failure = error.code
        result.harness_detail = redactor.scrub(error.detail)[:1000]
        transcript.write("harness_failure", code=error.code,
                         detail=redactor.scrub(error.detail)[:1000])
        try:
            result.files_written = sandbox.diff(before)  # type: ignore[possibly-undefined]
            (result.expected_outputs_present,
             result.expected_outputs_missing) = expected_output_state(sandbox, task.expected_outputs)
        except Exception:
            pass
    except Exception as error:  # never let an agent take the battery down
        result.status = "HARNESS_FAILURE"
        result.harness_failure = "UNEXPECTED_" + type(error).__name__
        result.harness_detail = redactor.scrub(str(error))[:1000]
        transcript.write("harness_failure", code=result.harness_failure,
                         detail=result.harness_detail)
    if agent is not None:
        result.tool_calls = {name: count for name, count in agent.tools.counts.items() if count}
        result.tool_call_total = sum(agent.tools.counts.values())
        result.iterations = agent.iterations
        result.prompt_tokens = agent.prompt_tokens
        result.completion_tokens = agent.completion_tokens
        result.total_tokens = agent.prompt_tokens + agent.completion_tokens
        result.malformed_tool_call_retries = agent.malformed_retries
        result.reasoning_calls = agent.reasoning_calls
        result.reasoning_chars = list(agent.reasoning_chars_per_turn)
        result.reasoning_retries = agent.reasoning_retries
    result.transport_requested = task.transport
    result.transport_used = getattr(transport, "surface", "") or task.transport
    result.transport_fallbacks = int(getattr(transport, "fallbacks", 0) or 0)
    result.wall_seconds = round(time.monotonic() - started, 3)
    transcript.write("task_end", status=result.status, iterations=result.iterations,
                     tool_calls=result.tool_calls, total_tokens=result.total_tokens,
                     wall_seconds=result.wall_seconds, finish_reason=result.finish_reason,
                     harness_failure=result.harness_failure,
                     expected_outputs_present=result.expected_outputs_present,
                     expected_outputs_missing=result.expected_outputs_missing,
                     transport_used=result.transport_used,
                     transport_fallbacks=result.transport_fallbacks,
                     reasoning_chars=result.reasoning_chars,
                     files_written=result.files_written)
    (run_dir / "result.json").write_text(
        redactor.scrub(json.dumps(result.to_json(), ensure_ascii=False, indent=2)) + "\n",
        encoding="utf-8")
    return result


def run_tasks(tasks: Sequence[TaskSpec], *, workers: int = MAX_CONCURRENCY,
              runs_dir: Path | str | None = None,
              transport_factory: Callable[[], Any] | None = None) -> list[TaskResult]:
    """Run tasks concurrently, at most ``workers`` at a time (ceiling 8)."""

    workers = max(1, min(workers, MAX_CONCURRENCY))
    results: list[TaskResult] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(run_task, task, runs_dir=runs_dir,
                               transport=transport_factory() if transport_factory else None): task
                   for task in tasks}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    order = {task.id: index for index, task in enumerate(tasks)}
    results.sort(key=lambda r: order.get(r.task_id, 0))
    return results


if __name__ == "__main__":  # a one-task command line, for the smoke run
    import argparse

    parser = argparse.ArgumentParser(description="Run one kimi-k3 worker task.")
    parser.add_argument("task_json", help="path to a JSON file holding one TaskSpec")
    parser.add_argument("--runs-dir", default=str(DEFAULT_RUNS_DIR))
    arguments = parser.parse_args()
    spec = TaskSpec.from_mapping(json.loads(Path(arguments.task_json).read_text(encoding="utf-8")))
    outcome = run_task(spec, runs_dir=arguments.runs_dir)
    print(json.dumps({k: v for k, v in outcome.to_json().items() if k != "final_text"}, indent=2))
