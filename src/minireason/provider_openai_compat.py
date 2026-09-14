"""A second transport: OpenAI-compatible and native-Ollama chat, same discipline.

``minireason.provider`` is the DeepSeek arm's transport and is not touched by
this module. This one speaks to any declared endpoint — DeepSeek's own
``/v1/chat/completions``, Ollama cloud's OpenAI-compatible ``/v1`` surface, or
Ollama cloud's native ``POST /api/chat`` — and keeps exactly the obligations
``provider.py`` keeps:

* the exact request bytes are hashed and recorded *before* the socket is
  touched, so a call that vanishes still left evidence of what was sent;
* every record file is opened ``"x"`` — write-once, never rewritten;
* every credential known to this process is replaced with
  ``[REDACTED_CREDENTIAL]`` on the way to disk, in its raw form *and* in its
  JSON-escaped rendering, and the record names the environment variables whose
  values were replaced (``credentials_redacted``). Two bounds on that promise,
  stated rather than implied: a value shorter than
  :data:`_MIN_SECRET_LENGTH` (8) characters is **not** treated as a credential
  at all - it is never redacted, never echo-checked and never a refusal,
  because a one- or two-character environment value would shred every record -
  and "known to this process" means the endpoint registry's own ``key_env``
  names, :data:`_ALWAYS_SECRET_ENVS`, and whatever names a caller registered
  through :func:`register_secret_envs`; it is not a scan of ``os.environ`` by
  name shape;
* a credential found in the outgoing payload is a refusal (``SECRET_IN_REQUEST``)
  and the call is never sent;
* a credential echoed back by a provider is a loud failure (``CREDENTIAL_ECHO``);
* redirects are refused, so a credentialed request cannot be replayed elsewhere;
* native reasoning text is read only to answer "was there any?" and is never
  persisted, never returned, and never fed to another call;
* nothing retries. One ``complete`` is one request on the wire or none.

The one thing this module adds over ``provider.py`` is *per-key* concurrency.
The owner's authorisation is five concurrent requests per credential, so the
semaphores live in a module-level registry keyed by ``key_env``: every provider
instance in the process that spends the same key competes for the same five
slots, and two different keys do not contend with each other.
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

__all__ = [
    "Endpoint",
    "ENDPOINTS",
    "ENDPOINTS_PATH",
    "CallResult",
    "ProviderFailure",
    "OpenAICompatProvider",
    "OfflineProvider",
    "CompatMiniResponder",
    "register_secret_envs",
    "registered_secret_envs",
    "responder_for",
    "digest",
    "write_new",
    "load_endpoints",
    "REDACTION",
]

REDACTION = "[REDACTED_CREDENTIAL]"

#: Key environment variables this module always considers credential-bearing,
#: whether or not an endpoint in the registry names them.
_ALWAYS_SECRET_ENVS = ("DEEPSEEK_API_KEY", "OLLAMA_API_KEY")

#: Anything shorter than this is not treated as a secret for redaction: a
#: one-character environment value would otherwise shred every record. This is
#: a documented floor, not an accident: a credential shorter than this is not
#: redacted on write, not detected by ``_echoes_credential`` and does not
#: trigger ``SECRET_IN_REQUEST``. Both credentials this transport is declared
#: against are far longer.
_MIN_SECRET_LENGTH = 8

_SECRET_ENV_LOCK = threading.Lock()
#: Names a caller declared credential-bearing at runtime. ``load_env_file`` in
#: ``tools/provider_smoke.py`` registers exactly the names it set, so the
#: redaction set tracks what was actually loaded rather than a name-shape
#: convention (a key in ``OLLAMA_TOKEN`` used to sit outside every check).
_REGISTERED_SECRET_ENVS: set[str] = set()


def register_secret_envs(names: Iterable[str]) -> tuple[str, ...]:
    """Declare environment variable NAMES whose values are credentials.

    Names only: no value is passed, returned, printed or stored. Returns the
    full registered set so a caller can assert what it declared.
    """

    with _SECRET_ENV_LOCK:
        _REGISTERED_SECRET_ENVS.update(str(name) for name in names if name)
        return tuple(sorted(_REGISTERED_SECRET_ENVS))


def registered_secret_envs() -> tuple[str, ...]:
    """The names registered through :func:`register_secret_envs`."""

    with _SECRET_ENV_LOCK:
        return tuple(sorted(_REGISTERED_SECRET_ENVS))


def _reset_registered_secret_envs() -> None:
    """Test seam only: forget the runtime-registered credential names."""

    with _SECRET_ENV_LOCK:
        _REGISTERED_SECRET_ENVS.clear()


class ProviderFailure(RuntimeError):
    """A loud operational failure with a stable code and a sanitised detail."""

    def __init__(self, code: str, detail: str, record: Mapping[str, Any] | None = None):
        self.code = code
        # The attached record goes through the same redaction as the record on
        # disk. Two paths would otherwise hand a caller a raw key: the
        # SECRET_IN_REQUEST refusal, whose ``request`` is by definition the
        # payload that carried one, and ``list_models``' CREDENTIAL_ECHO, whose
        # ``models`` is the one raw provider body this module keeps. Redacting
        # here rather than at each raise site means no future raise site can
        # reintroduce the exposure.
        self.record = _redacted_record(record) if record is not None else None
        super().__init__(f"{code}: {detail}")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Refuse every redirect: a credentialed request is never replayed elsewhere."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _open(request, *, timeout):
    return urllib.request.build_opener(_NoRedirect()).open(request, timeout=timeout)


def digest(value: Any) -> str:
    """The canonical sha256 of a JSON value, identical to ``provider.digest``."""

    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def _secret_env_names() -> list[str]:
    """The environment variable names this module treats as credential-bearing.

    Deliberately a declared set, not a name-shape scan of ``os.environ``: the
    registry's own ``key_env`` values, :data:`_ALWAYS_SECRET_ENVS`, and the
    names a caller registered through :func:`register_secret_envs`. A scan by
    suffix made redaction and refusal depend on ambient environment - an
    unrelated ``*_API_KEY`` holding an ordinary word would refuse legitimate
    prompts and rewrite record content - and left a real credential in a
    name outside the convention (``OLLAMA_TOKEN``) outside every check.
    """

    names = set(_ALWAYS_SECRET_ENVS)
    for endpoint in _REGISTRY.values():
        names.add(endpoint.key_env)
    names.update(registered_secret_envs())
    return sorted(names)


def _secret_items() -> list[tuple[str, str]]:
    """``(env name, value)`` for every credential visible now, longest first.

    Longest first so that a key which is a prefix of another key cannot leave a
    tail of the longer one behind after substitution. Values shorter than
    :data:`_MIN_SECRET_LENGTH` are excluded; see the module docstring.
    """

    items = [(name, os.environ.get(name, "")) for name in _secret_env_names()]
    return sorted(((name, value) for name, value in items
                   if len(value) >= _MIN_SECRET_LENGTH),
                  key=lambda item: len(item[1]), reverse=True)


def _secrets() -> list[str]:
    """Every credential value visible to this process, longest first."""

    values: list[str] = []
    for _name, value in _secret_items():
        if value not in values:
            values.append(value)
    return values


def _renderings(secret: str) -> tuple[str, ...]:
    """The secret as it can appear in an encoded record: raw and JSON-escaped.

    Redaction runs over already-encoded JSON text, so a key containing a
    character ``json.dumps`` escapes (a quote, a backslash, a control
    character) would never match its own raw form. Both renderings are
    replaced, so the guarantee holds for any key shape a provider might issue.
    """

    escaped = json.dumps(secret)[1:-1]
    return (escaped, secret) if escaped != secret else (secret,)


def redact_with_names(text: str) -> tuple[str, list[str]]:
    """Redact, and report the env var NAMES whose values were replaced.

    The names, never the values: a reader of a record can then tell a real
    credential hit from a false positive without seeing either.
    """

    hit: set[str] = set()
    for name, secret in _secret_items():
        for rendering in _renderings(secret):
            if rendering in text:
                text = text.replace(rendering, REDACTION)
                hit.add(name)
    return text, sorted(hit)


def redact(text: str) -> str:
    return redact_with_names(text)[0]


def _redacted_record(record: Mapping[str, Any]) -> dict[str, Any]:
    """A JSON round-trip of ``record`` with every credential replaced."""

    return json.loads(redact(json.dumps(dict(record), ensure_ascii=False, default=str)))


def write_new(path: Path, value: Any) -> None:
    """Write a record once, redacted. A second write to the same path refuses.

    When a credential was replaced, the written object gains a
    ``credentials_redacted`` list of the environment variable NAMES whose
    values were replaced, unless the caller already set that key.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    encoded, names = redact_with_names(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))
    if names and isinstance(value, Mapping) and "credentials_redacted" not in value:
        enriched = dict(value)
        enriched["credentials_redacted"] = names
        encoded, _ = redact_with_names(
            json.dumps(enriched, ensure_ascii=False, indent=2, sort_keys=True))
    with path.open("x", encoding="utf-8") as handle:
        handle.write(encoded + "\n")


# --------------------------------------------------------------------------
# Endpoints
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Endpoint:
    """One declared destination. ``family`` is a free label, never a credential.

    ``key_env`` names the environment variable the credential is read from at
    call time. The key value itself never enters an ``Endpoint``, a record, or
    a log line.
    """

    name: str
    base_url: str
    model: str
    key_env: str
    family: str
    chat_path: str = "/chat/completions"
    native: bool = False
    max_concurrency: int = 5
    timeout_seconds: int = 180

    def __post_init__(self) -> None:
        for label, value in (("name", self.name), ("base_url", self.base_url),
                             ("model", self.model), ("key_env", self.key_env),
                             ("family", self.family), ("chat_path", self.chat_path)):
            if type(value) is not str or not value.strip():
                raise ValueError(f"Endpoint {label} must be a non-empty string")
        if not self.base_url.startswith("https://"):
            raise ValueError("Endpoint base_url must be https")
        if self.base_url.endswith("/"):
            raise ValueError("Endpoint base_url must not end with '/'")
        if not self.chat_path.startswith("/"):
            raise ValueError("Endpoint chat_path must start with '/'")
        if type(self.native) is not bool:
            raise ValueError("Endpoint native must be a bool")
        if type(self.max_concurrency) is not int or not 1 <= self.max_concurrency <= 5:
            raise ValueError("Endpoint max_concurrency must be a whole number from 1 to 5")
        if type(self.timeout_seconds) is not int or not 1 <= self.timeout_seconds <= 600:
            raise ValueError("Endpoint timeout_seconds must be a whole number of seconds from 1 to 600")

    @property
    def chat_url(self) -> str:
        return self.base_url + self.chat_path

    @property
    def models_url(self) -> str:
        return self.base_url + "/models"

    def public(self) -> dict[str, Any]:
        """What a record is allowed to say about a destination."""

        return {"name": self.name, "base_url": self.base_url,
                "model": self.model, "family": self.family}


ENDPOINTS_PATH = Path(__file__).resolve().parent / "data" / "endpoints.json"


def load_endpoints(path: Path | str = ENDPOINTS_PATH) -> dict[str, Endpoint]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if raw.get("schema_version") != "minireason.endpoints.v1":
        raise ValueError("Unknown endpoints schema_version")
    registry: dict[str, Endpoint] = {}
    for entry in raw["endpoints"]:
        if not isinstance(entry, dict):
            raise ValueError("Each endpoints.json entry must be an object")
        unknown = set(entry) - {"name", "base_url", "model", "key_env", "family",
                                "chat_path", "native", "max_concurrency", "timeout_seconds"}
        if unknown:
            raise ValueError(f"Unknown endpoint fields: {sorted(unknown)}")
        endpoint = Endpoint(**entry)
        if endpoint.name in registry:
            raise ValueError(f"Duplicate endpoint name: {endpoint.name}")
        registry[endpoint.name] = endpoint
    if not registry:
        raise ValueError("endpoints.json declares no endpoints")
    return registry


_REGISTRY: dict[str, Endpoint] = {}
_REGISTRY.update(load_endpoints())
#: The shipped registry, keyed by endpoint name.
ENDPOINTS: dict[str, Endpoint] = _REGISTRY


# --------------------------------------------------------------------------
# Per-key concurrency
# --------------------------------------------------------------------------

_SLOT_LOCK = threading.Lock()
_SLOT_REGISTRY: dict[str, tuple[threading.BoundedSemaphore, int]] = {}


def slots_for(key_env: str, max_concurrency: int) -> threading.BoundedSemaphore:
    """The semaphore every provider spending ``key_env`` in this process shares.

    The first caller fixes the ceiling for that credential. A later endpoint
    that asks for a different ceiling is refused rather than quietly widening
    or narrowing an authorisation already in force.
    """

    with _SLOT_LOCK:
        existing = _SLOT_REGISTRY.get(key_env)
        if existing is None:
            created = (threading.BoundedSemaphore(max_concurrency), max_concurrency)
            _SLOT_REGISTRY[key_env] = created
            return created[0]
        semaphore, limit = existing
        if limit != max_concurrency:
            raise ProviderFailure(
                "CONCURRENCY_LIMIT_CONFLICT",
                f"{key_env} is already held to {limit} concurrent requests in this process; "
                f"an endpoint asking for {max_concurrency} would change an authorisation in force",
            )
        return semaphore


def _reset_slot_registry() -> None:
    """Test seam only: forget the per-key semaphores of this process."""

    with _SLOT_LOCK:
        _SLOT_REGISTRY.clear()


# --------------------------------------------------------------------------
# Results
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class CallResult:
    """One completed call. ``record`` is exactly what was written to disk."""

    status: str
    endpoint: str
    family: str
    requested_model: str
    returned_model: str | None
    content: str
    usage: dict[str, Any]
    finish_reason: str | None
    elapsed_ms: int
    reasoning_content_present: bool
    credential_redaction: bool
    request_sha256: str
    provider_response_sha256: str | None
    request_path: str
    response_path: str
    record: dict[str, Any] = field(default_factory=dict)
    #: Native reasoning text is never persisted by this transport. The field is
    #: a constant so that a record, a result and the documentation cannot drift.
    reasoning_content_persisted: bool = False

    def __getitem__(self, key: str) -> Any:
        """Dict access, so call sites written against ``provider.py`` port over."""

        return self.record[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.record.get(key, default)


# --------------------------------------------------------------------------
# Providers
# --------------------------------------------------------------------------


class _RecordedCaller:
    """Shared record discipline for the live and the offline provider."""

    kind = "recorded"

    def __init__(self, endpoint: Endpoint, records_dir: Path | str):
        if not isinstance(endpoint, Endpoint):
            raise TypeError("endpoint must be an Endpoint")
        self.endpoint = endpoint
        self.records = Path(records_dir)
        self.calls = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self._lock = threading.Lock()

    # -- argument validation -------------------------------------------------

    #: Payload keys this module builds itself. ``extra`` may not override one:
    #: the record's ``settings`` block asserts these values, so a caller that
    #: replaced one would leave two fields of the same record disagreeing about
    #: what went out. On a native endpoint ``options`` is absent from this set
    #: because ``extra["options"]`` is deep-merged into the built options
    #: rather than replacing them.
    _COMPAT_BUILT_KEYS = frozenset({"model", "messages", "stream", "max_tokens",
                                    "temperature", "seed", "response_format",
                                    "thinking", "reasoning_effort"})
    _NATIVE_BUILT_KEYS = frozenset({"model", "messages", "stream", "format",
                                    "thinking", "reasoning_effort"})

    def _built_payload_keys(self) -> frozenset[str]:
        return self._NATIVE_BUILT_KEYS if self.endpoint.native else self._COMPAT_BUILT_KEYS

    def _validate_call_args(self, *, max_tokens: Any, reasoning_effort: Any,
                            extra: Mapping[str, Any] | None) -> None:
        """The argument checks every caller of this class performs, in one place.

        Offline and live must refuse exactly the same argument sets, or a
        preflight passes a plan the first live call rejects. Raised before a
        call number is spent and before any record exists.
        """

        if type(max_tokens) is not int or not 1 <= max_tokens <= 393216:
            raise ValueError("Invalid completion ceiling")
        if reasoning_effort not in {"low", "high", "max"}:
            raise ValueError("Invalid reasoning effort")
        if extra:
            collisions = sorted(key for key in extra if key in self._built_payload_keys())
            if collisions:
                raise ValueError(
                    "extra may not override a payload key this module builds: "
                    f"{collisions}. The record's settings block asserts these, so an "
                    "override would leave the record contradicting the wire; on a native "
                    "endpoint pass extra={'options': {...}} instead, which is deep-merged.")
            if "options" in extra and not isinstance(extra["options"], Mapping):
                raise ValueError("extra['options'] must be a mapping")

    # -- payload construction ------------------------------------------------

    def _settings_view(self, **call: Any) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "endpoint_name": self.endpoint.name,
            "base_url": self.endpoint.base_url,
            "chat_path": self.endpoint.chat_path,
            "model": self.endpoint.model,
            "family": self.endpoint.family,
            "native": self.endpoint.native,
            "key_env": self.endpoint.key_env,
            "timeout_seconds": self.endpoint.timeout_seconds,
            "max_concurrency": self.endpoint.max_concurrency,
            "retries": 0,
            "native_reasoning_text_persisted": False,
            **call,
        }

    def _build_payload(self, messages: Sequence[Mapping[str, Any]], *, response_format: Any,
                       max_tokens: int, temperature: float | None, seed: int | None,
                       thinking: bool | None, reasoning_effort: str,
                       extra: Mapping[str, Any] | None) -> dict[str, Any]:
        messages = [dict(message) for message in messages]
        if self.endpoint.native:
            payload: dict[str, Any] = {
                "model": self.endpoint.model, "messages": messages, "stream": False,
                "options": {"num_predict": max_tokens},
            }
            if temperature is not None:
                payload["options"]["temperature"] = temperature
            if seed is not None:
                payload["options"]["seed"] = seed
            native_format = _native_format(response_format)
            if native_format is not None:
                payload["format"] = native_format
        else:
            payload = {"model": self.endpoint.model, "messages": messages,
                       "stream": False, "max_tokens": max_tokens}
            if temperature is not None:
                payload["temperature"] = temperature
            if seed is not None:
                payload["seed"] = seed
            if response_format is not None:
                payload["response_format"] = dict(response_format)
        if thinking is not None:
            # DeepSeek's thinking controls are DeepSeek's. Sending them to
            # another family would either be ignored silently or mean something
            # else; either way the record would claim a control that was not
            # exercised.
            if self.endpoint.family != "deepseek":
                raise ValueError(
                    "thinking controls are DeepSeek-specific; this endpoint's family is "
                    f"{self.endpoint.family!r}. Use extra={{...}} for this provider's own control.")
            payload["thinking"] = {"type": "enabled" if thinking else "disabled"}
            if thinking:
                payload["reasoning_effort"] = reasoning_effort
        if extra:
            for key, value in extra.items():
                if key == "options" and self.endpoint.native:
                    # Deep-merge, so a caller-supplied option cannot silently
                    # delete the completion ceiling the record still claims.
                    merged = dict(payload.get("options") or {})
                    merged.update(dict(value))
                    payload["options"] = merged
                else:
                    payload[key] = value
        return payload

    def _check_json_mode_prompt(self, messages: Sequence[Mapping[str, Any]], response_format: Any) -> None:
        if response_format is None or self.endpoint.family != "deepseek":
            return
        if not isinstance(response_format, Mapping) or response_format.get("type") != "json_object":
            return
        joined = " ".join(str(message.get("content", "")) for message in messages).lower()
        if "json" not in joined:
            raise ValueError(
                "DeepSeek JSON mode requires the word 'json' in the prompt; refusing to send a "
                "request the provider would reject or answer with an empty stream")

    # -- record lifecycle ----------------------------------------------------

    def _note_redactions(self, record: dict[str, Any]) -> None:
        """Name, in the record, the env vars whose values redaction replaced."""

        names = redact_with_names(json.dumps(record, ensure_ascii=False, default=str))[1]
        if names:
            record["credentials_redacted"] = names

    def _open_record(self, payload: Mapping[str, Any], settings: Mapping[str, Any],
                     coordinate: Mapping[str, Any] | None, *, url: str, method: str,
                     body: bytes | None, contacted: bool = True) -> tuple[str, dict[str, Any]]:
        with self._lock:
            self.calls += 1
            call_number = self.calls
        stem = f"call-{call_number:04d}"
        record: dict[str, Any] = {
            "schema_version": "minireason.call.v2",
            "call_number": call_number,
            "request": dict(payload),
            "request_sha256": digest(payload),
            "endpoint": self.endpoint.public(),
            "settings": dict(settings),
            "coordinate": dict(coordinate or {}),
            "started_at": datetime.now(timezone.utc).isoformat(),
        }
        if contacted:
            record.update({
                # The literal bytes handed to the socket, hashed before the
                # socket exists. ``request_sha256`` is the canonical-JSON
                # identity used for comparison across runs; this one proves
                # what actually went out.
                "request_bytes_sha256": hashlib.sha256(body).hexdigest() if body is not None else None,
                "request_bytes": len(body) if body is not None else 0,
                "url": url,
                "method": method,
                # Header *names* only. The Authorization value is never recorded.
                "request_header_names": ["Accept", "Authorization", "Content-Type"]
                if body is not None else ["Accept", "Authorization"],
            })
        else:
            # Nothing was formed, addressed or transmitted. The would-be values
            # are still recorded, under names that cannot be read as evidence
            # that a credentialed request existed.
            record.update({
                "url": None,
                "not_contacted_url": url,
                "method": method,
                "request_header_names": [],
                "would_send_bytes": len(body) if body is not None else 0,
                "would_send_bytes_sha256": hashlib.sha256(body).hexdigest()
                if body is not None else None,
                "would_send_header_names": ["Accept", "Content-Type"] if body is not None
                else ["Accept"],
            })
        self._note_redactions(record)
        path = self.records / (stem + ".request.json")
        try:
            write_new(path, record)
        except FileExistsError:
            # Two callers sharing one records directory, or one re-used stem.
            # A bare OSError here would escape every `except ProviderFailure`
            # a caller wrote, and would do so after the call was already spent.
            raise ProviderFailure(
                "RECORD_EXISTS",
                f"{path} already exists; records are write-once, so this call has no "
                "place to leave evidence. Give each caller its own records directory.",
                record=record) from None
        return stem, record

    def _close_record(self, stem: str, record: dict[str, Any], *, status: str,
                      started: float, **fields: Any) -> None:
        """Write the one response record for this call. A second close is a no-op.

        The in-memory record is only updated when it is the record that reaches
        disk, so the two can never disagree about what happened.
        """

        path = self.records / (stem + ".response.json")
        if path.exists():
            return
        record.update({"status": status,
                       "elapsed_ms": int((time.monotonic() - started) * 1000), **fields})
        self._note_redactions(record)
        write_new(path, record)

    def _refuse_credential_in_request(self, stem: str, record: dict[str, Any], payload: Any,
                                      coordinate: Any, started: float) -> None:
        rendered = json.dumps(payload, ensure_ascii=False) + json.dumps(coordinate or {}, ensure_ascii=False)
        for secret in _secrets():
            if secret in rendered:
                self._close_record(stem, record, status="SECRET_IN_REQUEST", started=started,
                                   error="Credential found in prompt content")
                # ``record["request"]`` on this path is, by definition, the
                # payload that carried the credential. ProviderFailure redacts
                # what it is handed, so the copy a caller can log carries the
                # marker and not the key.
                raise ProviderFailure("SECRET_IN_REQUEST", "Credential found in prompt content",
                                      record=record)

    def _finish(self, stem: str, record: dict[str, Any], started: float, normalised: "_Normalised",
                raw_len: int, raw_sha: str | None, *, thinking: bool | None = None) -> CallResult:
        answer = normalised.content
        if not isinstance(answer, str):
            self._close_record(stem, record, status="CONTENT_TYPE", started=started,
                               error="Provider content was not text",
                               provider_response_sha256=raw_sha)
            raise ProviderFailure("CONTENT_TYPE", f"Inspect {stem}.response.json", record=record)
        echoed = normalised.credential_echo
        answer = redact(answer)
        usage = normalised.usage
        usage_valid = (type(usage) is dict and all(
            type(usage.get(key)) is int and usage[key] >= 0
            for key in ("completion_tokens", "prompt_tokens")))
        if usage_valid:
            with self._lock:
                self.completion_tokens += usage["completion_tokens"]
                self.prompt_tokens += usage["prompt_tokens"]
        code = None
        if echoed:
            code = "CREDENTIAL_ECHO"
        elif normalised.finish_reason != "stop":
            code = "INCOMPLETE_GENERATION"
        elif not answer.strip():
            code = "EMPTY_GENERATION"
        elif not usage_valid:
            code = "USAGE_UNAVAILABLE"
        elif (self.endpoint.family == "deepseek" and thinking is not None
              and normalised.reasoning_present != thinking):
            # provider.py:169-170. The presence or absence of reasoning text is
            # the only evidence that the thinking control was honoured; a
            # record that carries `reasoning_content_present` and
            # `settings.thinking` side by side without comparing them lets a
            # provider that ignored the control report COMPLETE.
            code = "THINKING_MODE_MISMATCH"
        status = code or "COMPLETE"
        self._close_record(
            stem, record, status=status, started=started,
            provider_response_sha256=raw_sha, provider_response_bytes=raw_len,
            response_id=normalised.response_id, returned_model=normalised.returned_model,
            system_fingerprint=normalised.system_fingerprint, provider_created=normalised.created,
            usage=usage, usage_source=normalised.usage_source,
            finish_reason=normalised.finish_reason, content=answer,
            reasoning_content_present=normalised.reasoning_present,
            reasoning_content_persisted=False, credential_redaction=echoed)
        result = CallResult(
            status=status, endpoint=self.endpoint.name, family=self.endpoint.family,
            requested_model=self.endpoint.model, returned_model=normalised.returned_model,
            content=answer, usage=usage if isinstance(usage, dict) else {},
            finish_reason=normalised.finish_reason, elapsed_ms=record.get("elapsed_ms", 0),
            reasoning_content_present=normalised.reasoning_present, credential_redaction=echoed,
            request_sha256=record["request_sha256"], provider_response_sha256=raw_sha,
            request_path=str(self.records / (stem + ".request.json")),
            response_path=str(self.records / (stem + ".response.json")),
            record=dict(record))
        if code:
            raise ProviderFailure(code, f"Inspect {stem}.response.json", record=record)
        return result


@dataclass(frozen=True)
class _Normalised:
    """A provider answer reduced to the fields every family shares."""

    content: Any
    finish_reason: str | None
    usage: Any
    returned_model: str | None
    reasoning_present: bool
    credential_echo: bool
    response_id: str | None = None
    system_fingerprint: str | None = None
    created: Any = None
    #: ``"provider-reported"`` when every token count came from the provider;
    #: ``"native-normalised"`` when this module supplied one the provider
    #: omitted. Recorded so a count can never be read as reported when it was
    #: derived here.
    usage_source: str = "provider-reported"


def _native_format(response_format: Any) -> Any:
    """Translate an OpenAI ``response_format`` into Ollama's ``format``."""

    if response_format is None:
        return None
    if not isinstance(response_format, Mapping):
        raise ValueError("response_format must be a mapping")
    kind = response_format.get("type")
    if kind == "json_object":
        return "json"
    if kind == "json_schema":
        schema = response_format.get("json_schema", {})
        if isinstance(schema, Mapping) and "schema" in schema:
            return schema["schema"]
        return schema
    if kind == "text":
        return None
    raise ValueError(f"Unsupported response_format type for a native endpoint: {kind!r}")


def _echoes_credential(blob: str) -> bool:
    return any(secret in blob for secret in _secrets())


def _normalise_openai(result: Mapping[str, Any], raw_text: str) -> _Normalised:
    choices = result["choices"]
    if not choices:
        raise ProviderFailure("TRANSPORT_OR_RESPONSE_ERROR", "Provider returned no choice")
    choice = choices[0]
    message = choice.get("message") or {}
    content = message.get("content")
    if content is None:
        content = ""
    reasoning = message.get("reasoning_content") or message.get("reasoning")
    return _Normalised(
        content=content, finish_reason=choice.get("finish_reason"),
        usage=result.get("usage", {}), returned_model=result.get("model"),
        reasoning_present=bool(reasoning), credential_echo=_echoes_credential(raw_text),
        response_id=result.get("id"), system_fingerprint=result.get("system_fingerprint"),
        created=result.get("created"))


def _normalise_native(result: Mapping[str, Any], raw_text: str) -> _Normalised:
    """Ollama's ``POST /api/chat`` shape, reduced to the same fields.

    ``done_reason`` is Ollama's finish reason; when it is absent a finished
    response is read as ``stop`` and an unfinished one keeps ``None`` so that
    it fails as ``INCOMPLETE_GENERATION`` rather than passing quietly.
    """

    message = result.get("message") or {}
    content = message.get("content")
    if content is None:
        content = ""
    finish_reason = result.get("done_reason")
    if finish_reason is None and result.get("done") is True:
        finish_reason = "stop"
    prompt_tokens = result.get("prompt_eval_count")
    completion_tokens = result.get("eval_count")
    usage: dict[str, Any] = {}
    usage_source = "provider-reported"
    if type(completion_tokens) is int and type(prompt_tokens) is not int:
        # Ollama omits prompt_eval_count when the prompt was served entirely
        # from its prompt cache - the normal outcome for a repeated system
        # prompt, which is exactly the Mini workload. Zero prompt tokens were
        # evaluated, so zero is Ollama's own semantics here, not a guess; but
        # the record says the count was normalised rather than reported, so no
        # reader can mistake it for a provider-supplied figure.
        prompt_tokens = 0
        usage_source = "native-normalised"
    if type(prompt_tokens) is int:
        usage["prompt_tokens"] = prompt_tokens
    if type(completion_tokens) is int:
        usage["completion_tokens"] = completion_tokens
    if usage.keys() == {"prompt_tokens", "completion_tokens"}:
        usage["total_tokens"] = prompt_tokens + completion_tokens
    return _Normalised(
        content=content, finish_reason=finish_reason, usage=usage,
        returned_model=result.get("model"),
        reasoning_present=bool(message.get("thinking") or message.get("reasoning")),
        credential_echo=_echoes_credential(raw_text), response_id=None,
        system_fingerprint=None, created=result.get("created_at"),
        usage_source=usage_source)


class OpenAICompatProvider(_RecordedCaller):
    """One declared endpoint, one credential, five concurrent requests per key."""

    kind = "openai-compat-chat"

    def __init__(self, endpoint: Endpoint, records_dir: Path | str):
        super().__init__(endpoint, records_dir)
        self.kind = "ollama-native-chat" if endpoint.native else "openai-compat-chat"
        # Held for this credential across every provider instance in the process.
        self._slots = slots_for(endpoint.key_env, endpoint.max_concurrency)
        if not os.environ.get(endpoint.key_env):
            raise ProviderFailure("KEY_MISSING", f"{endpoint.key_env} is not set")

    def complete(self, messages: Sequence[Mapping[str, Any]], *, response_format: Any = None,
                 max_tokens: int = 8192, temperature: float | None = None,
                 seed: int | None = None, extra: Mapping[str, Any] | None = None,
                 thinking: bool | None = None, reasoning_effort: str = "high",
                 coordinate: Mapping[str, Any] | None = None) -> CallResult:
        self._validate_call_args(max_tokens=max_tokens, reasoning_effort=reasoning_effort,
                                 extra=extra)
        self._check_json_mode_prompt(messages, response_format)
        payload = self._build_payload(
            messages, response_format=response_format, max_tokens=max_tokens,
            temperature=temperature, seed=seed, thinking=thinking,
            reasoning_effort=reasoning_effort, extra=extra)
        settings = self._settings_view(
            max_tokens=max_tokens, temperature=temperature, seed=seed,
            response_format=dict(response_format) if isinstance(response_format, Mapping) else response_format,
            thinking=thinking, reasoning_effort=reasoning_effort if thinking else None,
            extra=dict(extra) if extra else {})
        # Serialise once. These are the bytes hashed into the record and the
        # bytes handed to the socket; nothing re-encodes between the two.
        body = json.dumps(payload).encode()
        stem, record = self._open_record(payload, settings, coordinate,
                                         url=self.endpoint.chat_url, method="POST", body=body)
        started = time.monotonic()
        key = os.environ.get(self.endpoint.key_env)
        if not key:
            self._close_record(stem, record, status="KEY_MISSING", started=started,
                               error=f"{self.endpoint.key_env} is not set")
            raise ProviderFailure("KEY_MISSING", f"{self.endpoint.key_env} is not set", record=record)
        self._refuse_credential_in_request(stem, record, payload, coordinate, started)
        request = urllib.request.Request(
            self.endpoint.chat_url, data=body, method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json",
                     "Authorization": "Bearer " + key})
        try:
            with self._slots:
                with _open(request, timeout=self.endpoint.timeout_seconds) as response:
                    raw = response.read()
            raw_sha = hashlib.sha256(raw).hexdigest()
            raw_text = raw.decode(errors="replace")
            result = json.loads(raw)
            if not isinstance(result, dict):
                raise ProviderFailure("TRANSPORT_OR_RESPONSE_ERROR", "Provider body was not a JSON object")
            normalised = (_normalise_native if self.endpoint.native else _normalise_openai)(result, raw_text)
            return self._finish(stem, record, started, normalised, len(raw), raw_sha,
                                thinking=thinking)
        except urllib.error.HTTPError as error:
            detail = redact(error.read(2000).decode(errors="replace"))
            code = f"HTTP_{error.code}"
        except ProviderFailure as error:
            self._close_record(stem, record, status=error.code, started=started,
                               error=redact(str(error)))
            if error.record is None:
                # A failure raised inside a normaliser carries no record; every
                # other failure class does. A caller reading failure.record
                # must not lose elapsed_ms, usage and request_sha256 for this
                # one class while a complete record sits on disk.
                error.record = _redacted_record(record)
            raise
        except Exception as error:  # transport, decode, or shape
            detail = redact(str(error))[:1000]
            code = "TRANSPORT_OR_RESPONSE_ERROR"
        self._close_record(stem, record, status=code, started=started, error=detail)
        raise ProviderFailure(code, detail, record=record)

    def list_models(self, *, coordinate: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """GET ``<base_url>/models``, recorded under the same discipline.

        A model list carries no reasoning text and no credential, so unlike a
        completion its body is kept in the record — after redaction. That is
        the one documented exception to "the raw provider response body is
        never recorded"; ``docs/workflows/provider-openai-compat.md`` carries
        the same carve-out. When the body did echo a credential the record
        handed to the caller through :class:`ProviderFailure` is redacted like
        the one on disk.
        """

        settings = self._settings_view(operation="list_models")
        stem, record = self._open_record({"method": "GET", "path": "/models"}, settings, coordinate,
                                         url=self.endpoint.models_url, method="GET", body=None)
        started = time.monotonic()
        key = os.environ.get(self.endpoint.key_env)
        if not key:
            self._close_record(stem, record, status="KEY_MISSING", started=started,
                               error=f"{self.endpoint.key_env} is not set")
            raise ProviderFailure("KEY_MISSING", f"{self.endpoint.key_env} is not set", record=record)
        request = urllib.request.Request(
            self.endpoint.models_url, method="GET",
            headers={"Accept": "application/json", "Authorization": "Bearer " + key})
        try:
            with self._slots:
                with _open(request, timeout=self.endpoint.timeout_seconds) as response:
                    raw = response.read()
            raw_text = raw.decode(errors="replace")
            echoed = _echoes_credential(raw_text)
            body = json.loads(raw)
            self._close_record(stem, record, status="CREDENTIAL_ECHO" if echoed else "COMPLETE",
                               started=started, provider_response_sha256=hashlib.sha256(raw).hexdigest(),
                               provider_response_bytes=len(raw), credential_redaction=echoed,
                               models=body)
            if echoed:
                raise ProviderFailure("CREDENTIAL_ECHO", f"Inspect {stem}.response.json", record=record)
            return dict(record)
        except urllib.error.HTTPError as error:
            detail = redact(error.read(2000).decode(errors="replace"))
            code = f"HTTP_{error.code}"
        except ProviderFailure:
            raise
        except Exception as error:
            detail = redact(str(error))[:1000]
            code = "TRANSPORT_OR_RESPONSE_ERROR"
        self._close_record(stem, record, status=code, started=started, error=detail)
        raise ProviderFailure(code, detail, record=record)


class OfflineProvider(_RecordedCaller):
    """A scripted stand-in with the same interface and the same records.

    It opens no socket and reads no credential, so a preflight can exercise the
    record discipline, the credential refusal and the status machinery of a plan
    before a single token is spent. The scripted replies are consumed in order;
    each is a string (the answer) or a mapping overriding the normalised fields.

    Its records say so. ``url`` is ``null`` and the destination that was *not*
    contacted appears as ``not_contacted_url``; ``request_header_names`` is
    empty, because no header was ever formed, and the byte count and digest of
    the body that would have been sent appear as ``would_send_bytes`` /
    ``would_send_bytes_sha256``. No offline record can be read as evidence that
    a credentialed request existed. It accepts and refuses exactly the argument
    sets the live provider does (``_validate_call_args``), so a plan that
    passes the preflight cannot die on its first live call for an argument.
    """

    kind = "offline-scripted"

    def __init__(self, endpoint: Endpoint, records_dir: Path | str,
                 script: Iterable[Any] = ()):
        super().__init__(endpoint, records_dir)
        self._script = list(script)
        self._used = 0

    def complete(self, messages: Sequence[Mapping[str, Any]], *, response_format: Any = None,
                 max_tokens: int = 8192, temperature: float | None = None,
                 seed: int | None = None, extra: Mapping[str, Any] | None = None,
                 thinking: bool | None = None, reasoning_effort: str = "high",
                 coordinate: Mapping[str, Any] | None = None) -> CallResult:
        self._validate_call_args(max_tokens=max_tokens, reasoning_effort=reasoning_effort,
                                 extra=extra)
        self._check_json_mode_prompt(messages, response_format)
        payload = self._build_payload(
            messages, response_format=response_format, max_tokens=max_tokens,
            temperature=temperature, seed=seed, thinking=thinking,
            reasoning_effort=reasoning_effort, extra=extra)
        settings = self._settings_view(
            max_tokens=max_tokens, temperature=temperature, seed=seed,
            response_format=dict(response_format) if isinstance(response_format, Mapping) else response_format,
            thinking=thinking, reasoning_effort=reasoning_effort if thinking else None,
            extra=dict(extra) if extra else {}, offline=True)
        body = json.dumps(payload).encode()
        stem, record = self._open_record(payload, settings, coordinate,
                                         url=self.endpoint.chat_url, method="POST(offline)",
                                         body=body, contacted=False)
        started = time.monotonic()
        self._refuse_credential_in_request(stem, record, payload, coordinate, started)
        with self._lock:
            index = self._used
            self._used += 1
        if index >= len(self._script):
            detail = "offline script exhausted"
            self._close_record(stem, record, status="TRANSPORT_OR_RESPONSE_ERROR",
                               started=started, error=detail)
            raise ProviderFailure("TRANSPORT_OR_RESPONSE_ERROR", detail, record=record)
        scripted = self._script[index]
        if isinstance(scripted, str):
            scripted = {"content": scripted}
        scripted = dict(scripted)
        content = scripted.get("content", "")
        usage = scripted.get("usage", {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0})
        normalised = _Normalised(
            content=content, finish_reason=scripted.get("finish_reason", "stop"),
            usage=usage, returned_model=scripted.get("returned_model", self.endpoint.model),
            reasoning_present=bool(scripted.get("reasoning_content_present", False)),
            credential_echo=_echoes_credential(json.dumps(scripted, ensure_ascii=False, default=str)),
            response_id=scripted.get("response_id", f"offline-{stem}"))
        rendered = json.dumps(scripted, ensure_ascii=False, default=str).encode()
        return self._finish(stem, record, started, normalised, len(rendered), None,
                            thinking=thinking)


# --------------------------------------------------------------------------
# Mini adapter
# --------------------------------------------------------------------------


class CompatMiniResponder:
    """``provider.MiniResponder``'s interface, against any declared endpoint.

    A Mini manifest asks a stage through ``reply``; this hands that stage's
    brief and the phase's own contract to whichever endpoint it was built for,
    and returns the public answer with the provider's own token counts. Native
    reasoning text never reaches the Mini run, exactly as with the DeepSeek arm.

    Defaults mirror ``provider.Settings`` where the two can be compared: for an
    endpoint whose ``family`` is ``deepseek`` this defaults ``thinking`` to
    ``False``, so a manifest ported from ``provider.MiniResponder`` keeps
    sending ``thinking: {"type": "disabled"}``. For every other family the
    thinking controls are DeepSeek-specific and none is sent.
    """

    def __init__(self, provider: _RecordedCaller, settings: Mapping[str, Any] | None = None):
        self.provider = provider
        settings = dict(settings or {})
        unknown = set(settings) - {"max_tokens", "temperature", "seed", "response_format",
                                   "thinking", "reasoning_effort", "extra"}
        if unknown:
            raise ValueError(f"Unknown responder settings: {sorted(unknown)}")
        settings.setdefault("max_tokens", 8192)
        settings.setdefault("response_format", {"type": "json_object"})
        if provider.endpoint.family == "deepseek":
            # provider.Settings.thinking defaults to False and provider.py
            # always sends the control, so the DeepSeek arm's every call
            # explicitly disables thinking. Leaving it unset here would hand a
            # ported Mini manifest the provider's own default instead, turning
            # native reasoning on and changing token spend, latency and
            # truncation behaviour with nothing to flag it.
            settings.setdefault("thinking", False)
        self.settings = settings
        self.completion_cap = settings["max_tokens"]

    def reply(self, request: Any) -> Any:
        from creib.forge.mini.executor import Reply, contract_for

        system, schema = contract_for(request.phase, request.optional_fields)
        system += "\nReturn one JSON object conforming to: " + json.dumps(schema, sort_keys=True)
        result = self.provider.complete(
            [{"role": "system", "content": system},
             {"role": "user", "content": request.brief}],
            coordinate={"stage_id": request.stage_id, "kind_id": request.kind_id,
                        "cycle": request.cycle, "attempt": request.attempt,
                        "phase": request.phase},
            **self.settings)
        return Reply(result.content, result.usage["prompt_tokens"], result.usage["completion_tokens"])


def responder_for(endpoint: Endpoint, records_dir: Path | str,
                  settings: Mapping[str, Any] | None = None) -> CompatMiniResponder:
    """A Mini responder bound to one endpoint, writing its records under ``records_dir``."""

    return CompatMiniResponder(OpenAICompatProvider(endpoint, records_dir), settings)
