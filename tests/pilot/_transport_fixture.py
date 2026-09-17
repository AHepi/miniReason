"""Private fixture helpers for test_cli_transport.py.

The generated ``sitecustomize`` is visible only to the live
worker subprocesses launched by these tests.
"""
from __future__ import annotations

from pathlib import Path


DUMMY_VALUE = "pilot-transport-synthetic-credential"

SITECUSTOMIZE = r'''from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
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
    raw_wire = bytes(request.data)
    wire_sha256 = hashlib.sha256(raw_wire).hexdigest()
    capture_root = os.environ.get("MINIREASON_PILOT_TEST_CAPTURE_DIR")
    if not capture_root:
        raise AssertionError("transport capture directory missing")
    capture = Path(capture_root)
    capture.mkdir(parents=True, exist_ok=True)
    (capture / (wire_sha256 + "-" + str(os.getpid()) + ".wire")).write_bytes(raw_wire)
    payload = json.loads(raw_wire.decode("utf-8"))
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
            cards = user.get("task", {}).get("input_catalog", [])
            selected = "evidence_read" if any(card.get("role") == "public_source" for card in cards) else "direct_answer"
            public = {"template_id": selected, "reason": "Use the bounded fixture route."}
    elif "template_id" in user and "inputs" in user:
        inputs = json.loads(json.dumps(user["inputs"]))
        if user.get("pass_number", 1) > 1:
            inputs["overrides"] = {"premises": ["Transport fixture changed the later-pass premise mix."]}
        subtask = {"template_id": user["template_id"], "inputs": inputs}
        sources = [card for card in user.get("input_catalog", []) if card.get("role") == "public_source"]
        if sources:
            source = sources[0]
            subtask["source_reads"] = [{
                "unit_id": source["unit_id"], "start": 0,
                "end": source["byte_count"], "limit": source["byte_count"],
            }]
        public = {"subtasks": [subtask]}
    elif "pass_number" in user and "verification" in user:
        verification_ref = user["verification"]["verification_ref"]
        continuing = user["pass_number"] < int(os.environ.get("MINIREASON_PILOT_TEST_PASS_LIMIT", "1"))
        public = {
            "decision": "continue" if continuing else "stop",
            "reason": "The verification at " + verification_ref + (" supports a changed pass." if continuing else " supports stopping."),
            "what_changes_next": "Change the later-pass premise mix." if continuing else "",
            "stop_rule": user.get("stop_rule") or "Stop after the fixture answer is verified.",
        }
    elif user.get("resolved_source_reads"):
        resolved = user["resolved_source_reads"][0]
        source_ref = resolved["receipt"]["source_ref"]
        quote = resolved["content"].strip()
        public = {
            "status": "complete", "answer": "42", "source_refs": [source_ref],
            "unresolved": [], "verification_refs": [],
            "quotes": [{"claim": "The pinned value is 42.", "source_id": source_ref,
                        "locator": "exact selected byte range", "quote": quote}],
            "contradictions": [], "not_found": [],
        }
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
