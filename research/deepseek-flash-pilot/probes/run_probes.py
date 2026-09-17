#!/usr/bin/env python3
"""Prepare or run bounded DeepSeek Flash self-piloting capability probes.

The default mode performs the live probes.  ``--dry-run`` and ``--self-check``
never read credentials, open sockets, or write records.  Live mode makes at
most twelve HTTP requests, never retries, and writes each exact wire request
before touching the network.

Run from the repository root with ``PYTHONPATH=src;tests``.  This script never
loads an env file.  It reads only the environment variable name declared by
the repository endpoint (DEEPSEEK_API_KEY), and only immediately before a
socket attempt.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import replace
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from minireason import provider_openai_compat as compat


MAX_HTTP_CALLS = 12
ASSESSOR_CONTRACT_VERSION = "deepseek-flash-pilot.assessors.v1"
TEMPLATE_IDS = (
    "direct_answer",
    "evidence_read",
    "engineer_patch",
    "critic_return",
    "decompose_synthesize",
)
ROUTER_TASKS = (
    ("router-direct", "Compute 17 + 25 and return the answer.", "direct_answer"),
    (
        "router-evidence",
        "Read three saved experiment records, compare their token counts, and cite each record.",
        "evidence_read",
    ),
    (
        "router-engineer",
        "Patch a Python parser bug, add a focused offline test, and report the changed paths.",
        "engineer_patch",
    ),
    (
        "router-critic",
        "Judge a proposed answer against a JSON contract and return one targeted repair request.",
        "critic_return",
    ),
    (
        "router-decompose",
        "Compare two architectures using independent security, cost, and operability analyses, then synthesize.",
        "decompose_synthesize",
    ),
)


class ProbeError(RuntimeError):
    """A safe, credential-free probe error."""


def _json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _source_identity(path: Path | str) -> dict[str, Any]:
    resolved = Path(path).resolve()
    data = resolved.read_bytes()
    try:
        display = resolved.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        display = str(resolved)
    return {"path": display, "sha256": _sha256_bytes(data), "bytes": len(data)}


def _custody_identity(
    assessor: Callable[[Mapping[str, Any]], Mapping[str, Any]] | None,
) -> dict[str, Any]:
    qualified_name = None
    if assessor is not None:
        qualified_name = f"{assessor.__module__}.{assessor.__qualname__}"
    return {
        "runner": _source_identity(Path(__file__)),
        "transport_source": _source_identity(Path(compat.__file__)),
        "endpoint_registry": _source_identity(compat.ENDPOINTS_PATH),
        "assessor": {
            "qualified_name": qualified_name,
            "contract_version": ASSESSOR_CONTRACT_VERSION,
        },
    }


def _strict_json_loads(value: str | bytes) -> Any:
    def object_pairs(pairs):
        result = {}
        for key, item in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = item
        return result

    def reject_constant(value):
        raise ValueError(f"non-finite JSON number: {value}")

    return json.loads(value, object_pairs_hook=object_pairs, parse_constant=reject_constant)


def _key_renderings(key: str) -> tuple[bytes, ...]:
    rendered = {
        key,
        json.dumps(key)[1:-1],
        json.dumps(key, ensure_ascii=False)[1:-1],
    }
    return tuple(value.encode("utf-8") for value in rendered if value)


def _contains_key_rendering(blob: bytes, key: str) -> bool:
    return any(rendering in blob for rendering in _key_renderings(key))


def _write_new(path: Path, value: Any) -> None:
    """Write one UTF-8 JSON record, with newline translation disabled."""

    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    with path.open("x", encoding="utf-8", newline="") as handle:
        handle.write(encoded)
        handle.write("\n")


def _safe_text(value: bytes, key: str) -> str:
    text = value.decode("utf-8", errors="replace")
    if key:
        text = text.replace(key, compat.REDACTION)
        escaped = json.dumps(key, ensure_ascii=False)[1:-1]
        if escaped != key:
            text = text.replace(escaped, compat.REDACTION)
    return text[:2000]


def _read_key(name: str) -> str:
    """Read the declared credential at call time; never log or print it."""

    key = os.environ.get(name, "")
    if not key:
        raise ProbeError(f"{name} is not set")
    return key


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def _http_post(url: str, body: bytes, key: str, timeout: int) -> tuple[int, bytes]:
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        },
    )
    opener = urllib.request.build_opener(_NoRedirect())
    with opener.open(request, timeout=timeout) as response:
        return int(response.status), response.read()


def _public_message(message: Mapping[str, Any]) -> tuple[dict[str, Any], bool]:
    """Return public model output while dropping native hidden reasoning text."""

    reasoning_present = bool(message.get("reasoning_content") or message.get("reasoning"))
    public: dict[str, Any] = {}
    for key in ("role", "content", "tool_calls", "function_call", "refusal"):
        if key in message:
            public[key] = message[key]
    return public, reasoning_present


def _public_response(result: Mapping[str, Any]) -> tuple[dict[str, Any], bool]:
    public: dict[str, Any] = {}
    for key in ("id", "object", "created", "model", "system_fingerprint", "usage"):
        if key in result:
            public[key] = result[key]
    choices: list[dict[str, Any]] = []
    reasoning_present = False
    for choice in result.get("choices", []):
        if not isinstance(choice, Mapping):
            continue
        message = choice.get("message") or {}
        if not isinstance(message, Mapping):
            message = {}
        clean_message, has_reasoning = _public_message(message)
        reasoning_present = reasoning_present or has_reasoning
        choices.append(
            {
                key: value
                for key, value in {
                    "index": choice.get("index"),
                    "finish_reason": choice.get("finish_reason"),
                    "message": clean_message,
                }.items()
                if value is not None
            }
        )
    public["choices"] = choices
    return public, reasoning_present


def _choice(response_record: Mapping[str, Any]) -> Mapping[str, Any]:
    response = response_record.get("public_response") or {}
    choices = response.get("choices") or []
    return choices[0] if choices else {}


def _message(response_record: Mapping[str, Any]) -> Mapping[str, Any]:
    return _choice(response_record).get("message") or {}


def _parse_json_content(response_record: Mapping[str, Any]) -> tuple[Any, str | None]:
    content = _message(response_record).get("content")
    if not isinstance(content, str) or not content.strip():
        return None, "missing nonempty content"
    try:
        return _strict_json_loads(content), None
    except (json.JSONDecodeError, ValueError) as error:
        return None, f"invalid JSON content: {error}"


def _tool_schemas(*, strict: bool) -> list[dict[str, Any]]:
    schemas: list[dict[str, Any]] = [
        {
            "type": "function",
            "function": {
                "name": "choose_template",
                "description": "Choose exactly one named working template for a bounded task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "enum": ["tool-fixture"]},
                        "template_id": {"type": "string", "enum": list(TEMPLATE_IDS)},
                        "task_summary": {"type": "string"},
                    },
                    "required": ["task_id", "template_id", "task_summary"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "verify_contract",
                "description": "Report whether a supplied fixture satisfies its declared contract.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "candidate_id": {"type": "string", "enum": ["candidate-1"]},
                        "valid": {"type": "boolean"},
                        "issue": {
                            "type": "string",
                            "enum": ["none", "missing_field", "wrong_type", "out_of_enum"],
                        },
                    },
                    "required": ["candidate_id", "valid", "issue"],
                    "additionalProperties": False,
                },
            },
        },
    ]
    if strict:
        for tool in schemas:
            tool["function"]["strict"] = True
    return schemas


def _validate_tool_arguments(name: str, arguments: Any) -> tuple[dict[str, Any] | None, str | None]:
    if not isinstance(arguments, str):
        return None, "arguments is not a JSON string"
    try:
        parsed = _strict_json_loads(arguments)
    except (json.JSONDecodeError, ValueError) as error:
        return None, f"arguments is invalid JSON: {error}"
    if not isinstance(parsed, dict):
        return None, "arguments is not an object"
    if name == "choose_template":
        required = {"task_id", "template_id", "task_summary"}
        if set(parsed) != required:
            return None, "choose_template keys differ from the schema"
        if parsed["task_id"] != "tool-fixture":
            return None, "task_id is outside its enum"
        if parsed["template_id"] not in TEMPLATE_IDS:
            return None, "template_id is outside its enum"
        if not isinstance(parsed["task_summary"], str) or not parsed["task_summary"].strip():
            return None, "task_summary is not a nonempty string"
        return parsed, None
    if name == "verify_contract":
        required = {"candidate_id", "valid", "issue"}
        if set(parsed) != required:
            return None, "verify_contract keys differ from the schema"
        if parsed["candidate_id"] != "candidate-1":
            return None, "candidate_id is outside its enum"
        if type(parsed["valid"]) is not bool:
            return None, "valid is not boolean"
        if parsed["issue"] not in {"none", "missing_field", "wrong_type", "out_of_enum"}:
            return None, "issue is outside its enum"
        return parsed, None
    return None, f"unknown tool {name!r}"


def _validated_calls(
    response_record: Mapping[str, Any], expected_names: Sequence[str]
) -> tuple[list[tuple[Mapping[str, Any], dict[str, Any]]], list[str]]:
    calls = _message(response_record).get("tool_calls") or []
    errors: list[str] = []
    validated: list[tuple[Mapping[str, Any], dict[str, Any]]] = []
    seen_ids: set[str] = set()
    if not isinstance(calls, list):
        return [], ["tool_calls is not a list"]
    for index, call in enumerate(calls):
        if not isinstance(call, Mapping):
            errors.append(f"tool call {index} is not an object")
            continue
        if call.get("type") != "function":
            errors.append(f"tool call {index} type is not 'function'")
            continue
        function = call.get("function")
        if not isinstance(function, Mapping):
            errors.append(f"tool call {index} function is not an object")
            continue
        name = function.get("name")
        call_id = call.get("id")
        if not isinstance(call_id, str) or not call_id:
            errors.append(f"tool call {index} lacks an id")
            continue
        if call_id in seen_ids:
            errors.append(f"tool call {index} duplicates id {call_id!r}")
            continue
        seen_ids.add(call_id)
        parsed, error = _validate_tool_arguments(name, function.get("arguments"))
        if error:
            errors.append(f"tool call {index}: {error}")
        else:
            validated.append((call, parsed or {}))
    names = [str(call.get("function", {}).get("name")) for call, _ in validated]
    if sorted(names) != sorted(expected_names):
        errors.append(f"valid tool names {names!r} do not match expected {list(expected_names)!r}")
    return validated, errors


def _local_tool_result(call: Mapping[str, Any], arguments: Mapping[str, Any]) -> str:
    name = call["function"]["name"]
    if name == "choose_template":
        result = {
            "accepted": True,
            "template_id": arguments["template_id"],
            "task_summary_sha256": hashlib.sha256(
                arguments["task_summary"].encode("utf-8")
            ).hexdigest(),
        }
    elif name == "verify_contract":
        result = {
            "accepted": arguments["valid"] and arguments["issue"] == "none",
            "candidate_id": arguments["candidate_id"],
        }
    else:
        raise ProbeError(f"refusing to simulate unknown tool {name!r}")
    return json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _tool_initial_assessor(expected_names: Sequence[str]) -> Callable[[Mapping[str, Any]], Mapping[str, Any]]:
    def assess(record: Mapping[str, Any]) -> Mapping[str, Any]:
        validated, errors = _validated_calls(record, expected_names)
        finish_reason = _choice(record).get("finish_reason")
        if finish_reason != "tool_calls":
            errors.append(f"finish_reason is {finish_reason!r}, not 'tool_calls'")
        if record.get("reasoning_content_present"):
            errors.append("thinking-disabled tool turn returned hidden reasoning")
        return {
            "pass": not errors,
            "criterion": "tool_calls finish; exact requested functions; distinct ids; strict arguments; no hidden reasoning",
            "valid_call_count": len(validated),
            "finish_reason": finish_reason,
            "errors": errors,
        }

    return assess


def _tool_followup_assessor(record: Mapping[str, Any]) -> Mapping[str, Any]:
    choice = _choice(record)
    message = _message(record)
    calls = message.get("tool_calls", [])
    content = message.get("content")
    calls_valid = isinstance(calls, list) and len(calls) == 0
    reasoning_absent = not record.get("reasoning_content_present")
    passed = (
        choice.get("finish_reason") == "stop"
        and calls_valid
        and isinstance(content, str)
        and bool(content.strip())
        and reasoning_absent
    )
    return {
        "pass": passed,
        "criterion": "finish_reason stop, a valid empty tool-call list, nonempty public content, and no hidden reasoning",
        "finish_reason": choice.get("finish_reason"),
        "further_tool_calls": len(calls) if isinstance(calls, list) else None,
        "tool_calls_shape_valid": calls_valid,
        "reasoning_content_present": bool(record.get("reasoning_content_present")),
    }


def _one_sentence(text: Any) -> bool:
    if not isinstance(text, str) or not text.strip() or len(text) > 300:
        return False
    terminal_marks = (".", "!", chr(63))
    return sum(text.count(mark) for mark in terminal_marks) <= 1


def _router_assessor(expected: str) -> Callable[[Mapping[str, Any]], Mapping[str, Any]]:
    def assess(record: Mapping[str, Any]) -> Mapping[str, Any]:
        parsed, error = _parse_json_content(record)
        finish_reason = _choice(record).get("finish_reason")
        valid_shape = (
            isinstance(parsed, dict)
            and set(parsed) == {"template_id", "justification"}
            and parsed.get("template_id") in TEMPLATE_IDS
            and _one_sentence(parsed.get("justification"))
        )
        selected = parsed.get("template_id") if isinstance(parsed, dict) else None
        errors = ([error] if error else []) + ([] if valid_shape else ["router JSON shape/enum/sentence contract failed"])
        if selected != expected:
            errors.append(f"selected {selected!r}; expected {expected!r}")
        if finish_reason != "stop":
            errors.append(f"finish_reason is {finish_reason!r}, not 'stop'")
        if record.get("reasoning_content_present"):
            errors.append("thinking-disabled router turn returned hidden reasoning")
        return {
            "pass": not errors,
            "criterion": f"exact JSON contract and expected template {expected}",
            "selected_template": selected,
            "finish_reason": finish_reason,
            "errors": errors,
        }

    return assess


def _spawn_assessor(record: Mapping[str, Any]) -> Mapping[str, Any]:
    parsed, error = _parse_json_content(record)
    finish_reason = _choice(record).get("finish_reason")
    errors = [error] if error else []
    subtasks = parsed.get("subtasks") if isinstance(parsed, dict) else None
    if not isinstance(parsed, dict) or set(parsed) != {"subtasks"} or not isinstance(subtasks, list):
        errors.append("top level must be exactly {'subtasks': [...]} ")
        subtasks = []
    if not 2 <= len(subtasks) <= 4:
        errors.append("subtasks count is outside 2..4")
    seen: list[str] = []
    for index, item in enumerate(subtasks):
        if not isinstance(item, dict) or set(item) != {"id", "template_id", "input", "depends_on"}:
            errors.append(f"subtask {index} has the wrong fields")
            continue
        if not isinstance(item["id"], str) or not item["id"] or item["id"] in seen:
            errors.append(f"subtask {index} id is missing or duplicated")
        if item["template_id"] not in TEMPLATE_IDS:
            errors.append(f"subtask {index} template_id is outside the enum")
        if not isinstance(item["input"], str) or not item["input"].strip():
            errors.append(f"subtask {index} input is empty")
        dependencies = item["depends_on"]
        if not isinstance(dependencies, list) or any(dep not in seen for dep in dependencies):
            errors.append(f"subtask {index} dependencies are not prior task ids")
        seen.append(item.get("id"))
    if finish_reason != "stop":
        errors.append(f"finish_reason is {finish_reason!r}, not 'stop'")
    if record.get("reasoning_content_present"):
        errors.append("thinking-disabled spawn turn returned hidden reasoning")
    return {
        "pass": not errors,
        "criterion": "2..4 unique typed subtasks whose dependencies form an ordered DAG",
        "subtask_count": len(subtasks),
        "finish_reason": finish_reason,
        "errors": errors,
    }


def _thinking_assessor(expect_reasoning: bool) -> Callable[[Mapping[str, Any]], Mapping[str, Any]]:
    def assess(record: Mapping[str, Any]) -> Mapping[str, Any]:
        parsed, error = _parse_json_content(record)
        choice = _choice(record)
        reasoning_present = bool(record.get("reasoning_content_present"))
        usage = (record.get("public_response") or {}).get("usage") or {}
        completion_tokens = usage.get("completion_tokens")
        errors = [error] if error else []
        if (
            not isinstance(parsed, dict)
            or set(parsed) != {"input"}
            or type(parsed.get("input")) is not int
            or parsed.get("input") != 11
        ):
            errors.append("answer is not exactly the expected JSON object with integer input 11")
        if choice.get("finish_reason") != "stop":
            errors.append("generation did not finish with stop")
        if reasoning_present != expect_reasoning:
            errors.append("reasoning_content presence does not match requested thinking mode")
        if type(completion_tokens) is not int or completion_tokens < 0:
            errors.append("usable nonnegative integer completion_tokens is absent")
        elif completion_tokens >= 4096:
            errors.append("completion reached the 4096 ceiling")
        return {
            "pass": not errors,
            "criterion": "correct JSON answer, stop below ceiling, and requested reasoning presence",
            "reasoning_content_present": reasoning_present,
            "completion_tokens": completion_tokens,
            "errors": errors,
        }

    return assess


class ProbeClient:
    def __init__(self, out: Path):
        self.out = out
        self.endpoint = compat.ENDPOINTS["deepseek-flash"]
        self.http_calls = 0

    def call(
        self,
        name: str,
        payload: Mapping[str, Any],
        *,
        endpoint=None,
        assessor: Callable[[Mapping[str, Any]], Mapping[str, Any]] | None = None,
    ) -> dict[str, Any]:
        endpoint = endpoint or self.endpoint
        if self.http_calls >= MAX_HTTP_CALLS:
            raise ProbeError(f"refusing HTTP call {self.http_calls + 1}; ceiling is {MAX_HTTP_CALLS}")
        request_path = self.out / f"{name}.request.json"
        response_path = self.out / f"{name}.response.json"
        body = _json_bytes(payload)
        started_epoch = time.time()
        custody_identity = _custody_identity(assessor)
        settings = {
            "stream": payload.get("stream"),
            "max_tokens": payload.get("max_tokens"),
            "temperature": payload.get("temperature"),
            "response_format": payload.get("response_format"),
            "thinking": payload.get("thinking"),
            "reasoning_effort": payload.get("reasoning_effort"),
            "tool_choice": payload.get("tool_choice"),
            "strict_tools": all(
                bool(tool.get("function", {}).get("strict")) for tool in payload.get("tools", [])
            ) if payload.get("tools") else False,
            "retries": 0,
            "hidden_reasoning_persisted": False,
        }
        request_record = {
            "schema_version": "minireason.deepseek_pilot_probe.v1",
            "probe": name,
            "started_at_epoch": started_epoch,
            "endpoint": endpoint.public(),
            "url": endpoint.chat_url,
            "method": "POST",
            "request_header_names": ["Accept", "Authorization", "Content-Type"],
            "settings": settings,
            "request": dict(payload),
            "request_sha256": compat.digest(payload),
            "request_bytes": len(body),
            "request_bytes_sha256": _sha256_bytes(body),
            "request_serialization": "utf-8 JSON, ensure_ascii=false, sort_keys=true, compact separators",
            "custody_identity": custody_identity,
        }
        monotonic_start = time.monotonic()
        key = ""
        try:
            key = _read_key(endpoint.key_env)
        except ProbeError as error:
            _write_new(request_path, request_record)
            finished = time.time()
            record = {
                "schema_version": "minireason.deepseek_pilot_probe.v1",
                "probe": name,
                "status": "KEY_MISSING",
                "contacted": False,
                "started_at_epoch": started_epoch,
                "finished_at_epoch": finished,
                "latency_ms": int((time.monotonic() - monotonic_start) * 1000),
                "endpoint": endpoint.public(),
                "request_sha256": request_record["request_sha256"],
                "request_bytes_sha256": request_record["request_bytes_sha256"],
                "error": str(error),
                "hidden_reasoning_persisted": False,
                "custody_identity": custody_identity,
            }
            _write_new(response_path, record)
            raise
        if _contains_key_rendering(body, key):
            raise ProbeError("credential value appears in the prepared payload; refusing to write or send it")
        _write_new(request_path, request_record)
        self.http_calls += 1
        try:
            http_status, raw = _http_post(endpoint.chat_url, body, key, endpoint.timeout_seconds)
        except urllib.error.HTTPError as error:
            raw = error.read()
            finished = time.time()
            echoed = _contains_key_rendering(raw, key)
            record = {
                "schema_version": "minireason.deepseek_pilot_probe.v1",
                "probe": name,
                "status": f"HTTP_{error.code}",
                "contacted": True,
                "started_at_epoch": started_epoch,
                "finished_at_epoch": finished,
                "latency_ms": int((time.monotonic() - monotonic_start) * 1000),
                "endpoint": endpoint.public(),
                "request_sha256": request_record["request_sha256"],
                "request_bytes_sha256": request_record["request_bytes_sha256"],
                "provider_response_bytes": len(raw),
                "provider_response_sha256": _sha256_bytes(raw),
                "credential_echo": echoed,
                "error": "credential echo suppressed" if echoed else "provider returned HTTP error; body suppressed",
                "hidden_reasoning_persisted": False,
                "custody_identity": custody_identity,
            }
            _write_new(response_path, record)
            return record
        except Exception as error:
            finished = time.time()
            safe_error = _safe_text(str(error).encode("utf-8", errors="replace"), key)
            record = {
                "schema_version": "minireason.deepseek_pilot_probe.v1",
                "probe": name,
                "status": "TRANSPORT_OR_RESPONSE_ERROR",
                "contacted": True,
                "started_at_epoch": started_epoch,
                "finished_at_epoch": finished,
                "latency_ms": int((time.monotonic() - monotonic_start) * 1000),
                "endpoint": endpoint.public(),
                "request_sha256": request_record["request_sha256"],
                "request_bytes_sha256": request_record["request_bytes_sha256"],
                "error": safe_error,
                "hidden_reasoning_persisted": False,
                "custody_identity": custody_identity,
            }
            _write_new(response_path, record)
            return record
        finished = time.time()
        echoed = _contains_key_rendering(raw, key)
        response_record: dict[str, Any] = {
            "schema_version": "minireason.deepseek_pilot_probe.v1",
            "probe": name,
            "status": "CREDENTIAL_ECHO" if echoed else "RECEIVED",
            "contacted": True,
            "http_status": http_status,
            "started_at_epoch": started_epoch,
            "finished_at_epoch": finished,
            "latency_ms": int((time.monotonic() - monotonic_start) * 1000),
            "endpoint": endpoint.public(),
            "request_sha256": request_record["request_sha256"],
            "request_bytes_sha256": request_record["request_bytes_sha256"],
            "provider_response_bytes": len(raw),
            "provider_response_sha256": _sha256_bytes(raw),
            "credential_echo": echoed,
            "hidden_reasoning_persisted": False,
            "custody_identity": custody_identity,
        }
        if echoed:
            response_record["error"] = "provider response echoed the credential; content suppressed"
        else:
            try:
                parsed = _strict_json_loads(raw)
                if not isinstance(parsed, dict):
                    raise ValueError("provider body is not a JSON object")
                decoded_bytes = json.dumps(parsed, ensure_ascii=False, sort_keys=True).encode("utf-8")
                if _contains_key_rendering(decoded_bytes, key):
                    response_record["status"] = "CREDENTIAL_ECHO"
                    response_record["credential_echo"] = True
                    response_record["error"] = "decoded provider response echoed the credential; content suppressed"
                    _write_new(response_path, response_record)
                    return response_record
                public, reasoning_present = _public_response(parsed)
                public_bytes = json.dumps(public, ensure_ascii=False, sort_keys=True).encode("utf-8")
                if _contains_key_rendering(public_bytes, key):
                    response_record["status"] = "CREDENTIAL_ECHO"
                    response_record["credential_echo"] = True
                    response_record["error"] = "decoded provider response echoed the credential; content suppressed"
                    _write_new(response_path, response_record)
                    return response_record
                response_record["public_response"] = public
                response_record["usage"] = public.get("usage") or {}
                response_record["reasoning_content_present"] = reasoning_present
                if assessor is not None:
                    response_record["assessment"] = dict(assessor(response_record))
            except Exception as error:
                response_record["status"] = "RESPONSE_SHAPE_ERROR"
                response_record["error"] = _safe_text(
                    str(error).encode("utf-8", errors="replace"), key
                )
        _write_new(response_path, response_record)
        return response_record


def _base_payload(
    messages: Sequence[Mapping[str, Any]],
    max_tokens: int,
    *,
    endpoint=None,
    response_format: Mapping[str, Any] | None = None,
    thinking: bool | None = None,
    reasoning_effort: str = "high",
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build probe payloads through the repository's validated wire builder."""

    endpoint = endpoint or compat.ENDPOINTS["deepseek-flash"]
    builder = object.__new__(compat.OfflineProvider)
    builder.endpoint = endpoint
    builder._validate_call_args(
        max_tokens=max_tokens, reasoning_effort=reasoning_effort, extra=extra
    )
    builder._check_json_mode_prompt(messages, response_format)
    return builder._build_payload(
        messages,
        response_format=response_format,
        max_tokens=max_tokens,
        temperature=0,
        seed=None,
        thinking=thinking,
        reasoning_effort=reasoning_effort,
        extra=extra,
    )


def _tool_messages(two_tools: bool) -> list[dict[str, str]]:
    request = (
        "For task_id tool-fixture, inspect candidate-1, which is the JSON object "
        "{\"template_id\":\"evidence_read\",\"inputs\":{\"paths\":[\"a.json\"]}}. "
        "Call choose_template with evidence_read and a short task_summary. "
    )
    if two_tools:
        request += (
            "Also call verify_contract with candidate_id candidate-1, valid true, issue none. "
            "Make both independent tool calls in this turn."
        )
    else:
        request += "Call only choose_template in this turn."
    return [
        {
            "role": "system",
            "content": "Use the supplied tools exactly as requested. Do not invent arguments.",
        },
        {"role": "user", "content": request},
    ]


def _run_tool_probe(client: ProbeClient, *, strict: bool) -> list[dict[str, Any]]:
    prefix = "tool-strict" if strict else "tool-normal"
    expected_names = ["choose_template"] if strict else ["choose_template", "verify_contract"]
    tools = _tool_schemas(strict=strict)
    endpoint = client.endpoint
    if strict:
        endpoint = replace(endpoint, base_url="https://api.deepseek.com/beta")
    payload = _base_payload(
        _tool_messages(two_tools=not strict),
        2048,
        endpoint=endpoint,
        thinking=False,
        extra={"tools": tools, "tool_choice": "auto"},
    )
    initial = client.call(
        prefix + "-initial",
        payload,
        endpoint=endpoint,
        assessor=_tool_initial_assessor(expected_names),
    )
    outputs = [initial]
    validated, errors = _validated_calls(initial, expected_names)
    if errors or not initial.get("assessment", {}).get("pass"):
        return outputs
    assistant_message = dict(_message(initial))
    assistant_message.pop("reasoning_content", None)
    assistant_message.pop("reasoning", None)
    messages = list(payload["messages"]) + [assistant_message]
    for call, arguments in validated:
        messages.append(
            {
                "role": "tool",
                "tool_call_id": call["id"],
                "content": _local_tool_result(call, arguments),
            }
        )
    messages.append(
        {
            "role": "user",
            "content": "Using the local tool results, give one sentence and stop without another tool call.",
        }
    )
    followup = _base_payload(
        messages,
        1024,
        endpoint=endpoint,
        thinking=False,
        extra={"tools": tools, "tool_choice": "auto"},
    )
    outputs.append(
        client.call(
            prefix + "-followup",
            followup,
            endpoint=endpoint,
            assessor=_tool_followup_assessor,
        )
    )
    return outputs


def _router_prompt(task: str) -> list[dict[str, str]]:
    catalogue = ", ".join(TEMPLATE_IDS)
    return [
        {
            "role": "system",
            "content": (
                "You are a bounded router. Choose exactly one template. Return a JSON object "
                "with exactly template_id and justification. template_id must be one of: "
                f"{catalogue}. justification must be one sentence."
            ),
        },
        {"role": "user", "content": task + " Return JSON only."},
    ]


def _run_router_probes(client: ProbeClient) -> list[dict[str, Any]]:
    outputs = []
    for name, task, expected in ROUTER_TASKS:
        payload = _base_payload(
            _router_prompt(task),
            1024,
            thinking=False,
            response_format={"type": "json_object"},
        )
        outputs.append(client.call(name, payload, assessor=_router_assessor(expected)))
    return outputs


def _run_spawn_probe(client: ProbeClient) -> dict[str, Any]:
    catalogue = ", ".join(TEMPLATE_IDS)
    messages = [
        {
            "role": "system",
            "content": (
                "You are a bounded task decomposer. Return JSON with exactly one key, subtasks. "
                "subtasks must contain 2 to 4 objects with exactly id, template_id, input, depends_on. "
                f"template_id must be one of: {catalogue}. depends_on is a list of earlier ids only. "
                "Example: {\"subtasks\":[{\"id\":\"s1\",\"template_id\":\"evidence_read\","
                "\"input\":\"read A\",\"depends_on\":[]},{\"id\":\"s2\","
                "\"template_id\":\"decompose_synthesize\",\"input\":\"synthesize\","
                "\"depends_on\":[\"s1\"]}]}"
            ),
        },
        {
            "role": "user",
            "content": (
                "Plan a comparison of two saved agent runs: independently read evidence and assess "
                "contract compliance, then synthesize a verdict. Emit JSON only; do not perform the work."
            ),
        },
    ]
    payload = _base_payload(
        messages,
        2048,
        thinking=False,
        response_format={"type": "json_object"},
    )
    return client.call("spawn", payload, assessor=_spawn_assessor)


def _run_thinking_pair(client: ProbeClient) -> list[dict[str, Any]]:
    messages = [
        {
            "role": "system",
            "content": (
                "Solve the short task. Return JSON with exactly one integer field named input. "
                "Example shape: {\"input\":0}."
            ),
        },
        {
            "role": "user",
            "content": "A machine triples an integer input and subtracts 4. Its output is 29. Find the input. Return JSON only.",
        },
    ]
    outputs = []
    for name, enabled in (("thinking-on", True), ("thinking-off", False)):
        payload = _base_payload(
            messages,
            4096,
            thinking=enabled,
            response_format={"type": "json_object"},
            reasoning_effort="high",
        )
        outputs.append(client.call(name, payload, assessor=_thinking_assessor(enabled)))
    return outputs


def _plan_summary() -> dict[str, Any]:
    names = [
        "tool-normal-initial",
        "tool-normal-followup",
        "tool-strict-initial",
        "tool-strict-followup",
        *(name for name, _task, _expected in ROUTER_TASKS),
        "spawn",
        "thinking-on",
        "thinking-off",
    ]
    return {
        "mode": "dry-run",
        "endpoint": compat.ENDPOINTS["deepseek-flash"].public(),
        "strict_endpoint_base_url": "https://api.deepseek.com/beta",
        "maximum_http_calls": MAX_HTTP_CALLS,
        "planned_call_count": len(names),
        "planned_names": names,
        "retries": 0,
        "credential_env_name": compat.ENDPOINTS["deepseek-flash"].key_env,
        "credential_read": False,
        "network_used": False,
        "records_written": False,
    }


def _self_check() -> dict[str, Any]:
    global _http_post, _read_key, _write_new
    original_http_post = _http_post
    original_read_key = _read_key
    original_write_new = _write_new

    def forbidden(*_args, **_kwargs):
        raise AssertionError("self-check touched a credential or the network")

    _http_post = forbidden
    _read_key = forbidden
    checks: list[str] = []
    try:
        plan = _plan_summary()
        assert plan["planned_call_count"] == MAX_HTTP_CALLS
        assert len(set(plan["planned_names"])) == MAX_HTTP_CALLS
        checks.append("twelve unique bounded call names")
        for strict in (False, True):
            schemas = _tool_schemas(strict=strict)
            assert len(schemas) == 2
            for tool in schemas:
                function = tool["function"]
                parameters = function["parameters"]
                assert parameters["additionalProperties"] is False
                assert set(parameters["required"]) == set(parameters["properties"])
                assert bool(function.get("strict")) is strict
            checks.append(f"tool schemas strict={strict}")
        choose = {
            "task_id": "tool-fixture",
            "template_id": "evidence_read",
            "task_summary": "read records",
        }
        parsed, error = _validate_tool_arguments(
            "choose_template", json.dumps(choose, separators=(",", ":"))
        )
        assert error is None and parsed == choose
        _, error = _validate_tool_arguments(
            "choose_template", json.dumps({**choose, "extra": True})
        )
        assert error is not None
        _, error = _validate_tool_arguments(
            "choose_template",
            '{"task_id":"tool-fixture","template_id":"evidence_read",'
            '"task_summary":"first","task_summary":"duplicate"}',
        )
        assert error is not None and "duplicate JSON key" in error
        try:
            _strict_json_loads('{"value":NaN}')
            raise AssertionError("NaN passed strict JSON parsing")
        except ValueError:
            pass
        checks.append("host tool argument allowlist and strict JSON parser")
        fake = {
            "public_response": {
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {
                            "role": "assistant",
                            "content": json.dumps(
                                {"template_id": "direct_answer", "justification": "The task is atomic."}
                            ),
                        },
                    }
                ]
            }
        }
        assert _router_assessor("direct_answer")(fake)["pass"] is True
        checks.append("router contract parser")
        public, reasoning = _public_response(
            {
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {
                            "role": "assistant",
                            "content": "ok",
                            "reasoning_content": "must disappear",
                        },
                    }
                ],
                "usage": {"prompt_tokens": 1, "completion_tokens": 1},
            }
        )
        assert reasoning is True
        assert "reasoning_content" not in public["choices"][0]["message"]
        assert "must disappear" not in json.dumps(public)
        checks.append("hidden reasoning stripping")

        tool_arguments = json.dumps(
            {
                "task_id": "tool-fixture",
                "template_id": "evidence_read",
                "task_summary": "read the saved records",
            },
            separators=(",", ":"),
        )
        tool_record = {
            "reasoning_content_present": False,
            "public_response": {
                "choices": [
                    {
                        "finish_reason": "tool_calls",
                        "message": {
                            "tool_calls": [
                                {
                                    "id": "call-1",
                                    "type": "function",
                                    "function": {
                                        "name": "choose_template",
                                        "arguments": tool_arguments,
                                    },
                                }
                            ]
                        },
                    }
                ]
            },
        }
        assert _tool_initial_assessor(["choose_template"])(tool_record)["pass"] is True
        duplicate_record = _strict_json_loads(json.dumps(tool_record))
        duplicate_record["public_response"]["choices"][0]["message"]["tool_calls"].append(
            duplicate_record["public_response"]["choices"][0]["message"]["tool_calls"][0]
        )
        assert _tool_initial_assessor(["choose_template"])(duplicate_record)["pass"] is False
        reasoning_record = _strict_json_loads(json.dumps(tool_record))
        reasoning_record["reasoning_content_present"] = True
        assert _tool_initial_assessor(["choose_template"])(reasoning_record)["pass"] is False
        checks.append("tool finish, id, type, function, and hidden-reasoning gates")

        router_reasoning = _strict_json_loads(json.dumps(fake))
        router_reasoning["reasoning_content_present"] = True
        assert _router_assessor("direct_answer")(router_reasoning)["pass"] is False
        followup_record = {
            "reasoning_content_present": False,
            "public_response": {
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {"role": "assistant", "content": "The tools succeeded."},
                    }
                ]
            },
        }
        assert _tool_followup_assessor(followup_record)["pass"] is True
        malformed_calls = _strict_json_loads(json.dumps(followup_record))
        malformed_calls["public_response"]["choices"][0]["message"]["tool_calls"] = {}
        assert _tool_followup_assessor(malformed_calls)["pass"] is False
        empty_followup = _strict_json_loads(json.dumps(followup_record))
        empty_followup["public_response"]["choices"][0]["message"]["content"] = ""
        assert _tool_followup_assessor(empty_followup)["pass"] is False
        reasoning_followup = _strict_json_loads(json.dumps(followup_record))
        reasoning_followup["reasoning_content_present"] = True
        assert _tool_followup_assessor(reasoning_followup)["pass"] is False
        spawn_record = {
            "reasoning_content_present": False,
            "public_response": {
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {
                            "content": json.dumps(
                                {
                                    "subtasks": [
                                        {
                                            "id": "s1",
                                            "template_id": "evidence_read",
                                            "input": "read A",
                                            "depends_on": [],
                                        },
                                        {
                                            "id": "s2",
                                            "template_id": "decompose_synthesize",
                                            "input": "synthesize",
                                            "depends_on": ["s1"],
                                        },
                                    ]
                                }
                            )
                        },
                    }
                ]
            },
        }
        assert _spawn_assessor(spawn_record)["pass"] is True
        spawn_reasoning = _strict_json_loads(json.dumps(spawn_record))
        spawn_reasoning["reasoning_content_present"] = True
        assert _spawn_assessor(spawn_reasoning)["pass"] is False
        thinking_record = {
            "reasoning_content_present": False,
            "public_response": {
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {"content": '{"input":11}'},
                    }
                ],
                "usage": {"prompt_tokens": 20, "completion_tokens": 8, "total_tokens": 28},
            },
        }
        assert _thinking_assessor(False)(thinking_record)["pass"] is True
        float_answer = _strict_json_loads(json.dumps(thinking_record))
        float_answer["public_response"]["choices"][0]["message"]["content"] = '{"input":11.0}'
        assert _thinking_assessor(False)(float_answer)["pass"] is False
        missing_usage = _strict_json_loads(json.dumps(thinking_record))
        del missing_usage["public_response"]["usage"]["completion_tokens"]
        assert _thinking_assessor(False)(missing_usage)["pass"] is False
        negative_usage = _strict_json_loads(json.dumps(thinking_record))
        negative_usage["public_response"]["usage"]["completion_tokens"] = -1
        assert _thinking_assessor(False)(negative_usage)["pass"] is False
        checks.append("negative reasoning, malformed followup, integer, and usage fixtures")

        events: list[str] = []
        memory_records: dict[str, Any] = {}
        fake_key = 'offline-"slash\\-κ-key'

        def fake_read_key(name: str) -> str:
            assert name == "DEEPSEEK_API_KEY"
            events.append("key")
            return fake_key

        def fake_write_new(path: Path, value: Any) -> None:
            assert path.name not in memory_records
            memory_records[path.name] = _strict_json_loads(json.dumps(value))
            events.append("write:" + path.name)

        def fake_http_post(url: str, body: bytes, key: str, timeout: int) -> tuple[int, bytes]:
            assert url == "https://api.deepseek.com/v1/chat/completions"
            assert key == fake_key
            assert timeout == 180
            assert _strict_json_loads(body)["model"] == "deepseek-flash"
            events.append("http")
            response = {
                "id": "offline-response",
                "model": "deepseek-flash",
                "choices": [
                    {
                        "index": 0,
                        "finish_reason": "stop",
                        "message": {
                            "role": "assistant",
                            "content": json.dumps(
                                {"template_id": "direct_answer", "justification": "The task is atomic."}
                            ),
                        },
                    }
                ],
                "usage": {"prompt_tokens": 9, "completion_tokens": 4, "total_tokens": 13},
            }
            return 200, _json_bytes(response)

        _read_key = fake_read_key
        _write_new = fake_write_new
        _http_post = fake_http_post
        client = ProbeClient(Path("memory-records"))
        payload = _base_payload(
            _router_prompt("Compute 1 + 1."),
            128,
            thinking=False,
            response_format={"type": "json_object"},
        )
        record = client.call("offline", payload, assessor=_router_assessor("direct_answer"))
        assert record["assessment"]["pass"] is True
        assert events.index("write:offline.request.json") < events.index("http")
        request_identity = memory_records["offline.request.json"]["custody_identity"]
        response_identity = memory_records["offline.response.json"]["custody_identity"]
        assert request_identity == response_identity
        assert request_identity["runner"]["sha256"] == _sha256_bytes(Path(__file__).read_bytes())
        assert request_identity["transport_source"]["sha256"] == _sha256_bytes(
            Path(compat.__file__).read_bytes()
        )
        assert request_identity["endpoint_registry"]["sha256"] == _sha256_bytes(
            Path(compat.ENDPOINTS_PATH).read_bytes()
        )
        assert request_identity["assessor"]["contract_version"] == ASSESSOR_CONTRACT_VERSION
        assert request_identity["assessor"]["qualified_name"].endswith(
            "._router_assessor.<locals>.assess"
        )
        checks.append("runner, transport, registry, and assessor custody identity")

        def fake_echo_http(url: str, body: bytes, key: str, timeout: int) -> tuple[int, bytes]:
            events.append("http-echo")
            response = {
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {"role": "assistant", "content": fake_key},
                    }
                ],
                "usage": {"prompt_tokens": 1, "completion_tokens": 1},
            }
            return 200, json.dumps(response, ensure_ascii=True).encode("utf-8")

        _http_post = fake_echo_http
        echo_record = client.call("offline-echo", payload)
        assert echo_record["status"] == "CREDENTIAL_ECHO"
        assert "public_response" not in echo_record

        def fake_http_error(url: str, body: bytes, key: str, timeout: int):
            events.append("http-error")
            raise urllib.error.HTTPError(
                url, 400, "bad request", {}, io.BytesIO(b"private provider error body")
            )

        _http_post = fake_http_error
        error_record = client.call("offline-error", payload)
        assert error_record["status"] == "HTTP_400"
        assert "private provider error body" not in json.dumps(error_record)
        assert set(memory_records) == {
            "offline.request.json",
            "offline.response.json",
            "offline-echo.request.json",
            "offline-echo.response.json",
            "offline-error.request.json",
            "offline-error.response.json",
        }
        for prefix in ("offline", "offline-echo", "offline-error"):
            assert (
                memory_records[prefix + ".request.json"]["custody_identity"]
                == memory_records[prefix + ".response.json"]["custody_identity"]
            )
        encoded_records = json.dumps(memory_records, ensure_ascii=False)
        assert fake_key not in encoded_records
        assert "must never be recorded" not in encoded_records
        assert "private provider error body" not in encoded_records
        escaped_key = json.dumps(fake_key)[1:-1].encode("utf-8")
        assert _contains_key_rendering(escaped_key, fake_key)
        checks.append("mocked request, escaped-key echo, and HTTP-error custody")
        try:
            _prepare_live_out(Path("work") / "w33" / "forbidden-probe-output")
            raise AssertionError("output allowlist admitted a work directory")
        except ProbeError as error:
            assert "output must be below" in str(error)
        checks.append("live output-root allowlist")
    finally:
        _http_post = original_http_post
        _read_key = original_read_key
        _write_new = original_write_new
    return {
        "mode": "self-check",
        "pass": True,
        "checks": checks,
        "credential_read": False,
        "network_used": False,
        "records_written": False,
    }


def _prepare_live_out(out: Path) -> None:
    allowed_root = (Path.cwd() / "research" / "deepseek-flash-pilot" / "probes").resolve()
    resolved = out.resolve()
    try:
        resolved.relative_to(allowed_root)
    except ValueError:
        raise ProbeError(f"output must be below {allowed_root}") from None
    if resolved == allowed_root:
        raise ProbeError("output must be a records directory below the probes directory")
    if resolved.exists() and not resolved.is_dir():
        raise ProbeError(f"output exists and is not a directory: {resolved}")
    if resolved.exists() and any(resolved.iterdir()):
        raise ProbeError(f"output directory is not empty; refusing to clobber records: {out}")
    resolved.mkdir(parents=True, exist_ok=True)


def _live(out: Path) -> dict[str, Any]:
    _prepare_live_out(out)
    client = ProbeClient(out)
    records: list[dict[str, Any]] = []
    records.extend(_run_tool_probe(client, strict=False))
    records.extend(_run_tool_probe(client, strict=True))
    records.extend(_run_router_probes(client))
    records.append(_run_spawn_probe(client))
    records.extend(_run_thinking_pair(client))
    if client.http_calls > MAX_HTTP_CALLS:
        raise AssertionError("HTTP call ceiling invariant failed")
    passed = sum(bool(record.get("assessment", {}).get("pass")) for record in records)
    return {
        "mode": "live",
        "http_calls": client.http_calls,
        "maximum_http_calls": MAX_HTTP_CALLS,
        "records": len(records),
        "assessments_passed": passed,
        "assessment_total": sum("assessment" in record for record in records),
        "output_directory": str(out),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="write-once record directory")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="show the plan without key, network, or writes")
    mode.add_argument("--self-check", action="store_true", help="run offline parser and custody checks only")
    args = parser.parse_args(argv)
    try:
        if args.dry_run:
            summary = _plan_summary()
        elif args.self_check:
            summary = _self_check()
        else:
            summary = _live(args.out)
    except ProbeError as error:
        print(json.dumps({"status": "REFUSED", "error": str(error)}, ensure_ascii=False))
        return 2
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
