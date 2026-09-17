"""Private fixture helpers for test_cli_transport.py.

The generated ``sitecustomize`` is visible only to the live
worker subprocesses launched by these tests.
"""
from __future__ import annotations

from pathlib import Path


DUMMY_VALUE = "pilot-transport-synthetic-credential"

SITECUSTOMIZE = r'''from __future__ import annotations
import json
import os
import socket
def _deny_socket(*_args, **_kwargs):
    raise AssertionError("pilot transport test forbids real sockets")

socket.create_connection = _deny_socket
from minireason import provider_openai_compat as compat

class _Response:
    def __init__(self, body):
        self._body = body
    def __enter__(self):
        return self
    def __exit__(self, *_args):
        return False
    def read(self):
        return self._body

def _fake_open(request, *, timeout):
    del timeout
    if request.full_url != "https://api.deepseek.com/v1/chat/completions":
        raise AssertionError("unexpected transport destination")
    payload = json.loads(request.data.decode("utf-8"))
    user = None
    for message in payload["messages"]:
        if message.get("role") != "user":
            continue
        try:
            candidate = json.loads(message["content"])
        except (TypeError, ValueError):
            continue
        if isinstance(candidate, dict):
            user = candidate
            break
    if user is None:
        raise AssertionError("public user packet not found")
    if "catalogue" in user:
        repairing = any(message.get("role") == "assistant" for message in payload["messages"])
        if os.environ.get("MINIREASON_PILOT_TEST_FORCE_ROUTE_REPAIR") == "1" and not repairing:
            public = {}
        else:
            public = {"template_id": "direct_answer", "reason": "Short closed fixture."}
    elif "template_id" in user and "inputs" in user:
        public = {"subtasks": [{"template_id": user["template_id"], "inputs": user["inputs"]}]}
    else:
        public = {"status": "complete", "answer": "42", "source_refs": [], "unresolved": [], "verification_refs": []}
    body = {
        "id": "pilot-http-double", "created": 0, "model": "deepseek-flash",
        "choices": [{"index": 0, "finish_reason": "stop", "message": {
            "role": "assistant", "content": json.dumps(public, ensure_ascii=False)}}],
        "usage": {"prompt_tokens": 11, "completion_tokens": 7, "total_tokens": 18},
    }
    return _Response(json.dumps(body, ensure_ascii=False).encode("utf-8"))

compat._open = _fake_open
'''


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def install_transport_double(directory: Path) -> Path:
    path = directory / "sitecustomize.py"
    write_text(path, SITECUSTOMIZE)
    return path


def write_synthetic_env(path: Path) -> None:
    write_text(path, "DEEPSEEK_API_KEY=" + DUMMY_VALUE + "\n")
