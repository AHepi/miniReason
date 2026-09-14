"""Does Ollama's native /api/chat serve the tool round trip the harness needs?

    python3 kimi/probes/probe_native_tools.py

Two live calls with ``think: "low"``:

  1. one tool declared, one question that cannot be answered without it —
     does the reply carry ``message.tool_calls``, and in what shape?
  2. the tool result sent back as a ``role: "tool"`` message — does a final
     answer come back that used it?

The record keeps both request bodies and both response shapes (reasoning text
hashed and counted, never stored). The credential is read by
``kimi_agent.load_key`` and never printed.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import kimi_agent as ka  # noqa: E402

TIMEOUT = 60
RECORD = HERE / "probe-reasoning-native-tools.json"

TOOL = {
    "type": "function",
    "function": {
        "name": "lookup_build_number",
        "description": "Return the current build number for a project.",
        "parameters": {
            "type": "object",
            "properties": {"project": {"type": "string", "description": "project name"}},
            "required": ["project"],
        },
    },
}
QUESTION = ("What is the current build number of project alpha? "
            "Use the lookup_build_number tool, then state the number and nothing else.")
BUILD_NUMBER = "4821"


def post(url: str, body: dict[str, Any], key: str) -> tuple[int, dict[str, Any], float]:
    payload = json.dumps(body).encode()
    if not ka.REDACTOR.clean(payload.decode()):
        raise ka.HarnessFailure("SECRET_IN_REQUEST", "credential found in outgoing payload")
    request = urllib.request.Request(
        url, data=payload, method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json",
                 "Authorization": "Bearer " + key})
    started = time.monotonic()
    opener = urllib.request.build_opener(ka._NoRedirect())
    with opener.open(request, timeout=TIMEOUT) as response:
        raw = response.read()
        status = response.status
    wall = round(time.monotonic() - started, 2)
    text = raw.decode(errors="replace")
    if not ka.REDACTOR.clean(text):
        raise ka.HarnessFailure("CREDENTIAL_ECHO", "provider echoed a credential")
    return status, json.loads(text), wall


def summarise(result: dict[str, Any]) -> dict[str, Any]:
    """The response, with the reasoning text replaced by its digest and length."""

    shape = json.loads(json.dumps(result))
    message = shape.get("message") or {}
    thinking = message.pop("thinking", "") or message.pop("reasoning", "") or ""
    message["thinking_sha256"] = ka.sha256_text(thinking) if thinking else None
    message["thinking_chars"] = len(thinking)
    return shape


def main() -> int:
    endpoint = ka.load_endpoint("ollama/kimi-k3.native", timeout_seconds=TIMEOUT)
    key = ka.load_key(endpoint.key_env)
    messages: list[dict[str, Any]] = [{"role": "user", "content": QUESTION}]
    first_body = {"model": endpoint.model, "stream": False, "think": "low",
                  "messages": messages, "tools": [TOOL]}
    status, first, wall_one = post(endpoint.chat_url, first_body, key)
    message = first.get("message") or {}
    calls = message.get("tool_calls") or []
    print(f"turn 1: HTTP {status} in {wall_one}s, tool_calls={len(calls)}, "
          f"content_chars={len(message.get('content') or '')}, "
          f"thinking_chars={len(message.get('thinking') or '')}", flush=True)

    record: dict[str, Any] = {
        "probe": "native-tools-roundtrip", "surface": "ollama native /api/chat",
        "url": endpoint.chat_url, "think": "low",
        "turn_1": {"request_body": first_body, "http_status": status,
                   "wall_seconds": wall_one, "response": summarise(first),
                   "tool_calls_returned": len(calls)},
    }
    if not calls:
        record["verdict"] = "no tool_calls in the native reply; the port is not viable"
        RECORD.write_text(ka.REDACTOR.scrub(json.dumps(record, ensure_ascii=False, indent=2)) + "\n",
                          encoding="utf-8")
        print("NO TOOL CALLS — stopping.")
        return 1

    call = calls[0]
    function = call.get("function") or {}
    arguments = function.get("arguments")
    record["call_shape"] = {
        "keys_on_call": sorted(call),
        "keys_on_function": sorted(function),
        "arguments_type": type(arguments).__name__,
        "has_id": "id" in call,
    }
    print(f"  call keys={sorted(call)} function keys={sorted(function)} "
          f"arguments is a {type(arguments).__name__}", flush=True)

    # Turn 2: the assistant turn is echoed back verbatim, then the tool reply.
    messages = messages + [
        {k: v for k, v in message.items() if k in ("role", "content", "tool_calls")},
        {"role": "tool", "tool_name": function.get("name", ""), "content": BUILD_NUMBER},
    ]
    second_body = {"model": endpoint.model, "stream": False, "think": "low",
                   "messages": messages, "tools": [TOOL]}
    status_two, second, wall_two = post(endpoint.chat_url, second_body, key)
    answer = (second.get("message") or {}).get("content") or ""
    used = BUILD_NUMBER in answer
    print(f"turn 2: HTTP {status_two} in {wall_two}s, done_reason={second.get('done_reason')}, "
          f"answer_used_the_tool_result={used}, answer={answer.strip()[:80]!r}", flush=True)

    record["turn_2"] = {"request_body": second_body, "http_status": status_two,
                        "wall_seconds": wall_two, "response": summarise(second),
                        "answer_used_the_tool_result": used}
    record["verdict"] = ("native /api/chat serves the same round trip"
                         if used else "tool result did not reach the answer")
    RECORD.write_text(ka.REDACTOR.scrub(json.dumps(record, ensure_ascii=False, indent=2)) + "\n",
                      encoding="utf-8")
    print(f"wrote {RECORD}")
    return 0 if used else 1


if __name__ == "__main__":
    raise SystemExit(main())
