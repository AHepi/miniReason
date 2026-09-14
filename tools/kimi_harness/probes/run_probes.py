"""Live capability probes against ollama/kimi-k3. One call per probe, recorded.

Each probe writes ``kimi/probes/probe-NN-<slug>.json`` holding the exact request
shape that was sent and the provider's response, redacted, with any
``reasoning_content`` replaced by its sha256 and length before anything reaches
disk. Nothing is retried. Run one probe at a time:

    python3 run_probes.py 01
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from kimi_agent import (REDACTOR, HarnessFailure, KimiClient, load_endpoint,  # noqa: E402
                        load_key, sha256_text)

HERE = Path(__file__).resolve().parent


def strip_reasoning(body):
    """Replace every reasoning field by a digest and a length, in place."""

    notes = []
    if isinstance(body, dict):
        for choice in body.get("choices") or []:
            message = choice.get("message") or {}
            for field in ("reasoning_content", "reasoning", "thinking"):
                value = message.get(field)
                if isinstance(value, str) and value:
                    message[field] = {
                        "__not_persisted__": True,
                        "sha256": sha256_text(value),
                        "chars": len(value),
                        "estimated_tokens": max(1, len(value) // 4),
                    }
                    notes.append(field)
    return body, notes


def call(label, payload, *, timeout=600):
    endpoint = load_endpoint()
    key = load_key(endpoint.key_env)
    body = json.dumps(payload).encode()
    record = {
        "probe": label,
        "at": datetime.now(timezone.utc).isoformat(),
        "endpoint": endpoint.public(),
        "url": endpoint.chat_url,
        "method": "POST",
        "request_header_names": ["Accept", "Authorization", "Content-Type"],
        "request_bytes": len(body),
        "request_bytes_sha256": hashlib.sha256(body).hexdigest(),
        "request": payload,
        "timeout_seconds": timeout,
    }
    request = urllib.request.Request(
        endpoint.chat_url, data=body, method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json",
                 "Authorization": "Bearer " + key})
    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            record["http_status"] = response.status
    except urllib.error.HTTPError as error:
        detail = REDACTOR.scrub(error.read(4000).decode(errors="replace"))
        record.update({"http_status": error.code, "status": f"HTTP_{error.code}",
                       "error": detail[:2000],
                       "elapsed_ms": int((time.monotonic() - started) * 1000)})
        write(label, record)
        return record
    except Exception as error:
        record.update({"status": "TRANSPORT_OR_RESPONSE_ERROR",
                       "error": REDACTOR.scrub(str(error))[:1000],
                       "elapsed_ms": int((time.monotonic() - started) * 1000)})
        write(label, record)
        return record
    record["elapsed_ms"] = int((time.monotonic() - started) * 1000)
    record["response_bytes"] = len(raw)
    record["response_sha256"] = hashlib.sha256(raw).hexdigest()
    text = raw.decode(errors="replace")
    record["credential_echo"] = not REDACTOR.clean(text)
    parsed = json.loads(text)
    parsed, notes = strip_reasoning(parsed)
    record["reasoning_fields_seen"] = notes
    record["response"] = parsed
    record["status"] = "COMPLETE"
    write(label, record)
    return record


def write(label, record):
    path = HERE / f"probe-{label}.json"
    path.write_text(REDACTOR.scrub(json.dumps(record, ensure_ascii=False, indent=2,
                                              default=str)) + "\n", encoding="utf-8")
    print(f"wrote {path.name}: status={record.get('status')} "
          f"elapsed_ms={record.get('elapsed_ms')}")


MODEL = "kimi-k3"

WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current temperature for one city.",
        "parameters": {"type": "object",
                       "properties": {"city": {"type": "string",
                                               "description": "City name, e.g. Wellington"}},
                       "required": ["city"]},
    },
}


def probe_01():
    """Does the endpoint honour OpenAI tools/tool_choice and return tool_calls?"""

    return call("01-tools", {
        "model": MODEL, "stream": False, "max_tokens": 32768,
        "messages": [
            {"role": "system", "content": "You are a tool-using assistant. Use the tools you are given."},
            {"role": "user", "content": "What is the current temperature in Wellington? Call the tool."},
        ],
        "tools": [WEATHER_TOOL], "tool_choice": "auto",
    })


def probe_02():
    """Is response_format json_schema honoured (json_object is proven by C001)?"""

    return call("02-json-schema", {
        "model": MODEL, "stream": False, "max_tokens": 32768,
        "messages": [
            {"role": "system", "content": "Reply with one JSON object and nothing else."},
            {"role": "user", "content": "Return JSON with keys ok (boolean) and model (string, your model name)."},
        ],
        "response_format": {"type": "json_schema", "json_schema": {
            "name": "probe", "strict": True, "schema": {
                "type": "object",
                "properties": {"ok": {"type": "boolean"}, "model": {"type": "string"}},
                "required": ["ok", "model"], "additionalProperties": False}}},
    })


def probe_03():
    """Does reasoning_content come back, and does reasoning_effort change it?"""

    return call("03-reasoning-effort", {
        "model": MODEL, "stream": False, "max_tokens": 32768,
        "reasoning_effort": "low",
        "messages": [
            {"role": "user", "content": "A bat and a ball cost 1.10 in total. The bat costs 1.00 more "
                                        "than the ball. How much does the ball cost? Answer in one line."},
        ],
    })


def probe_04(tool_call_id="call_1", first_arguments='{"city": "Wellington"}'):
    """Multi-turn: feed a tool result back as role 'tool' and confirm the loop closes."""

    return call("04-tool-roundtrip", {
        "model": MODEL, "stream": False, "max_tokens": 32768,
        "messages": [
            {"role": "system", "content": "You are a tool-using assistant. Use the tools you are given."},
            {"role": "user", "content": "What is the current temperature in Wellington? Call the tool."},
            {"role": "assistant", "content": "",
             "tool_calls": [{"id": tool_call_id, "type": "function",
                             "function": {"name": "get_weather", "arguments": first_arguments}}]},
            {"role": "tool", "tool_call_id": tool_call_id, "name": "get_weather",
             "content": '{"city": "Wellington", "temperature_c": 13.5}'},
        ],
        "tools": [WEATHER_TOOL], "tool_choice": "auto",
    })


def probe_05():
    """How large a prompt is accepted? ~60k tokens of repository file contents."""

    root = Path("/home/user/miniReason")
    collected, total = [], 0
    target_chars = 240000  # ~60k tokens at 4 chars/token
    for path in sorted(root.rglob("*.py")):
        if any(part in {".git", "__pycache__", ".venv"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        collected.append(f"### {path.relative_to(root)}\n{text}")
        total += len(text)
        if total >= target_chars:
            break
    corpus = "\n\n".join(collected)[:target_chars]
    return call("05-context-60k", {
        "model": MODEL, "stream": False, "max_tokens": 4096,
        "messages": [
            {"role": "system", "content": "You are given a corpus of Python source files."},
            {"role": "user", "content": corpus +
             "\n\n---\nIn one short sentence: how many '### ' file headers appear above, "
             "and what is the name of the LAST file header?"},
        ],
    })


PROBES = {"01": probe_01, "02": probe_02, "03": probe_03, "04": probe_04, "05": probe_05}

if __name__ == "__main__":
    name = sys.argv[1]
    extra = sys.argv[2:]
    record = PROBES[name](*extra)
    summary = {"status": record.get("status"), "elapsed_ms": record.get("elapsed_ms")}
    response = record.get("response") or {}
    choice = (response.get("choices") or [{}])[0]
    message = choice.get("message") or {}
    summary.update({
        "finish_reason": choice.get("finish_reason"),
        "has_tool_calls": bool(message.get("tool_calls")),
        "tool_calls": message.get("tool_calls"),
        "content_head": (message.get("content") or "")[:400],
        "reasoning_fields": record.get("reasoning_fields_seen"),
        "usage": response.get("usage"),
        "error": record.get("error", "")[:600],
    })
    print(json.dumps(summary, indent=2, default=str))
