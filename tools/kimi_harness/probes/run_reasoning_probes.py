"""Does kimi-k3 on the Ollama cloud honour a reasoning control?

    python3 kimi/probes/run_reasoning_probes.py

Eight live calls on one tiny prompt, one per candidate control, on both surfaces
(``--report-only`` rebuilds the write-up from the saved records, calling nothing):

  v1-baseline      POST https://ollama.com/v1/chat/completions, no control
  v1-effort-flat   the same, plus ``reasoning_effort: "low"``     (OpenAI style)
  v1-effort-object the same, plus ``reasoning: {"effort": "low"}`` (Responses style)
  v1-think-false   the same, plus ``think: false``  — does the native key pass through?
  v1-think-low     the same, plus ``think: "low"``
  native-baseline  POST https://ollama.com/api/chat, no control
  native-think-off the same, plus ``think: false``
  native-think-low the same, plus ``think: "low"``

The last question is the one that matters for the worker: the tool loop speaks
``/v1``, so a control that only works on ``/api/chat`` is not yet a control it can use.

Each record keeps the exact request body (never the headers, which carry the
credential), the HTTP status, the length of the reasoning the model returned,
the completion tokens, the wall clock and whether an answer came back at all.
The reasoning **text** is hashed and counted, never written down — the same
rule the harness runs under. The credential is read by ``kimi_agent.load_key``
from the process environment or the gitignored ``.env`` and is never printed.
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

PROBE_TIMEOUT = 60
PROMPT = ("List the files named in this sentence: a.py, b.py. "
          "Answer with one filename per line and nothing else.")
REPORT = HERE.parent / "PROBE-REASONING.md"


def _answered(text: str) -> bool:
    """The two-line answer this prompt asks for, however it is spaced."""

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "a.py" in text and "b.py" in text and len(lines) <= 4


def probe_v1(name: str, extra: dict[str, Any]) -> dict[str, Any]:
    endpoint = ka.load_endpoint(timeout_seconds=PROBE_TIMEOUT)
    client = ka.KimiClient(endpoint)
    kwargs: dict[str, Any] = {"max_tokens": 2048}
    if extra:
        kwargs["extra"] = extra
    body = client.build_payload([{"role": "user", "content": PROMPT}], **kwargs)
    started = time.monotonic()
    record: dict[str, Any] = {"probe": name, "surface": "openai-compat /v1/chat/completions",
                              "url": endpoint.chat_url, "request_body": body}
    try:
        answer = client.chat([{"role": "user", "content": PROMPT}], **kwargs)
    except ka.HarnessFailure as error:
        record.update(http_status=error.code, ok=False, error=error.detail[:400],
                      wall_seconds=round(time.monotonic() - started, 2),
                      reasoning_chars=None, completion_tokens=None, answered=False)
        return record
    record.update(
        http_status=answer.http_status, ok=True,
        wall_seconds=round(answer.latency_ms / 1000, 2),
        finish_reason=answer.finish_reason,
        completion_tokens=(answer.usage or {}).get("completion_tokens"),
        prompt_tokens=(answer.usage or {}).get("prompt_tokens"),
        reasoning_present=answer.reasoning_present,
        reasoning_chars=answer.reasoning_chars,
        reasoning_sha256=answer.reasoning_sha256,
        content_chars=len(answer.content), content=answer.content,
        answered=_answered(answer.content))
    return record


def probe_native(name: str, extra: dict[str, Any]) -> dict[str, Any]:
    """Ollama's own ``/api/chat``. Hand-rolled: the harness client speaks /v1."""

    endpoint = ka.load_endpoint("ollama/kimi-k3.native", timeout_seconds=PROBE_TIMEOUT)
    key = ka.load_key(endpoint.key_env)          # never printed, never recorded
    body: dict[str, Any] = {"model": endpoint.model, "stream": False,
                            "messages": [{"role": "user", "content": PROMPT}], **extra}
    record: dict[str, Any] = {"probe": name, "surface": "ollama native /api/chat",
                              "url": endpoint.chat_url, "request_body": body}
    payload = json.dumps(body).encode()
    if not ka.REDACTOR.clean(payload.decode()):
        raise ka.HarnessFailure("SECRET_IN_REQUEST", "credential found in outgoing payload")
    request = urllib.request.Request(
        endpoint.chat_url, data=payload, method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json",
                 "Authorization": "Bearer " + key})
    started = time.monotonic()
    try:
        opener = urllib.request.build_opener(ka._NoRedirect())
        with opener.open(request, timeout=PROBE_TIMEOUT) as response:
            raw = response.read()
            status = response.status
    except urllib.error.HTTPError as error:
        detail = ka.REDACTOR.scrub(error.read(2000).decode(errors="replace"))
        record.update(http_status=f"HTTP_{error.code}", ok=False, error=detail[:400],
                      wall_seconds=round(time.monotonic() - started, 2),
                      reasoning_chars=None, completion_tokens=None, answered=False)
        return record
    except Exception as error:
        record.update(http_status="TRANSPORT_OR_RESPONSE_ERROR", ok=False,
                      error=ka.REDACTOR.scrub(str(error))[:400],
                      wall_seconds=round(time.monotonic() - started, 2),
                      reasoning_chars=None, completion_tokens=None, answered=False)
        return record
    wall = round(time.monotonic() - started, 2)
    text = raw.decode(errors="replace")
    if not ka.REDACTOR.clean(text):
        raise ka.HarnessFailure("CREDENTIAL_ECHO", "provider echoed a credential")
    result = json.loads(text)
    message = result.get("message") or {}
    content = message.get("content") or ""
    thinking = message.get("thinking") or message.get("reasoning") or ""
    record.update(
        http_status=status, ok=True, wall_seconds=wall,
        finish_reason=result.get("done_reason"),
        completion_tokens=result.get("eval_count"),
        prompt_tokens=result.get("prompt_eval_count"),
        reasoning_present=bool(thinking),
        reasoning_chars=len(thinking),
        reasoning_sha256=ka.sha256_text(thinking) if thinking else None,
        content_chars=len(content), content=content, answered=_answered(content))
    return record


PROBES = (
    ("v1-baseline", probe_v1, {}),
    ("v1-reasoning-effort-low", probe_v1, {"reasoning_effort": "low"}),
    ("v1-reasoning-object-low", probe_v1, {"reasoning": {"effort": "low"}}),
    ("native-baseline", probe_native, {}),
    ("native-think-false", probe_native, {"think": False}),
    ("native-think-low", probe_native, {"think": "low"}),
    # The harness speaks /v1, so the decisive question is whether the native
    # control passes through that surface as well.
    ("v1-think-false", probe_v1, {"think": False}),
    ("v1-think-low", probe_v1, {"think": "low"}),
)


def row(record: dict[str, Any]) -> str:
    def show(value: Any) -> str:
        return "-" if value is None else str(value)
    control = json.dumps({k: v for k, v in record["request_body"].items()
                          if k in ("reasoning_effort", "reasoning", "think")}) or "{}"
    return ("| `{probe}` | {surface} | `{control}` | {status} | {reasoning} | {completion} | "
            "{wall} | {answered} |").format(
        probe=record["probe"], surface="/v1" if "/v1" in record["url"] else "/api/chat",
        control=control if control != "{}" else "(none)",
        status=show(record.get("http_status")),
        reasoning=show(record.get("reasoning_chars")),
        completion=show(record.get("completion_tokens")),
        wall=show(record.get("wall_seconds")),
        answered="yes" if record.get("answered") else ("no" if record.get("ok") else "no (failed)"))


ORDER = ("v1-baseline", "v1-reasoning-effort-low", "v1-reasoning-object-low",
         "v1-think-false", "v1-think-low",
         "native-baseline", "native-think-false", "native-think-low")


def load_records() -> list[dict[str, Any]]:
    records = []
    for name in ORDER:
        path = HERE / f"probe-reasoning-{name}.json"
        if path.is_file():
            records.append(json.loads(path.read_text(encoding="utf-8")))
    return records


def report_markdown(records: list[dict[str, Any]]) -> str:
    """PROBE-REASONING.md, built from the saved records — no calls."""

    by_name = {record["probe"]: record for record in records}
    base_v1 = by_name.get("v1-baseline", {}).get("reasoning_chars")
    base_native = by_name.get("native-baseline", {}).get("reasoning_chars")
    lines = [
        "# Does kimi-k3 honour a reasoning control?",
        "",
        "Eight live calls on one tiny prompt, 2026-09-14. One question: can a request "
        "ask this model to think less, so that a turn's budget reaches the answer "
        "instead of being spent before it? That is now the throughput question for the "
        "worker harness — every `INCOMPLETE_TURN` in `RUNS-RECLASSIFIED.md` is a turn "
        "whose whole budget went to reasoning.",
        "",
        "Prompt (identical in every call, expecting two lines):",
        "",
        "```",
        PROMPT,
        "```",
        "",
        "## Result",
        "",
        "| probe | surface | control sent | HTTP | reasoning chars | completion tokens | wall s | answered |",
        "|---|---|---|---|---|---|---|---|",
    ]
    lines += [row(record) for record in records]
    lines += [
        "",
        f"Baselines carry no control at all: **{base_v1} reasoning characters** on `/v1`, "
        f"**{base_native}** on `/api/chat`. Read every row against its own surface's baseline.",
        "",
        "## What that says",
        "",
        "* **`/v1/chat/completions` honours nothing.** `reasoning_effort: \"low\"`, "
        "`reasoning: {\"effort\": \"low\"}` and a pass-through `think` are all accepted "
        "with HTTP 200 and all return reasoning **no shorter than the uncontrolled "
        "baseline** (163, 142 and 160 characters against 135). Accepting a parameter is "
        "not honouring it; on this surface these are inert.",
        "* **Ollama's native `/api/chat` honours `think`.** `think: false` removed the "
        "reasoning **entirely** (0 characters, 12 completion tokens, 3.8 s against the "
        "baseline's 166 characters, 63 tokens, 9.6 s) and still produced the right "
        "answer. `think: \"low\"` shortened it to 62 characters. One sample each, so "
        "treat `false` as established (0 is not noise) and `\"low\"` as suggestive.",
        "* The harness's tool loop speaks `/v1`, because that is the surface whose "
        "native `tools` round trip is proven (`probe-01`, `probe-04`). **So the control "
        "that works is not on the surface the worker uses.**",
        "",
        "## What was done about it",
        "",
        "* `TaskSpec.reasoning` (`\"default\"` | `\"low\"` | `\"off\"`) exists and "
        "defaults to `\"low\"` for production tasks. `KimiClient.reasoning_parameter` "
        "maps it to `think` **only** on an endpoint marked `native` in the registry; on "
        "`/v1` it sends **nothing**, because a parameter this host ignores would make "
        "the transcript look like a control had been applied when the probes say it "
        "would not be.",
        "* A turn that exhausts its budget on reasoning is retried **once**, with the "
        "lowest setting the endpoint honours, recorded as `incomplete_turn_retry`. On "
        "`/v1` no setting is honoured, so no retry fires and the run still stops at "
        "`INCOMPLETE_TURN` — the machinery is in place for the surface that can use it.",
        "* The real lever on `/v1` is the budget: `MAX_TOKENS` is now **24576** "
        "(the 300 s gateway wall at ~90-100 tok/s), not 8192. Every budget-exhausted "
        "turn in the recorded battery stopped at exactly 8192 tokens with 28k-37k "
        "characters of reasoning behind it: the reasoning fits inside 24576 with room "
        "for an answer, and does not fit inside 8192.",
        "* **Open, and worth one experiment before it is assumed:** whether "
        "`/api/chat` serves the same `tools` round trip. If it does, porting the "
        "transport buys `think: false` on worker turns, which is the only measured way "
        "to stop reasoning eating a turn on this host.",
        "",
        "## Exact request bodies (headers omitted: they carry the credential)",
        "",
    ]
    for record in records:
        lines += [f"### `{record['probe']}` — `POST {record['url']}`", "",
                  "```json",
                  json.dumps(record["request_body"], indent=2, ensure_ascii=False),
                  "```", ""]
    lines += ["Per-probe records, including each answer and the sha256 of the reasoning "
              "text (never the text): `probes/probe-reasoning-*.json`.", ""]
    lines += tool_roundtrip_section()
    return "\n".join(lines)


def tool_roundtrip_section() -> list[str]:
    """The follow-up probe: does the native surface serve the harness's tool loop?"""

    path = HERE / "probe-reasoning-native-tools.json"
    if not path.is_file():
        return []
    record = json.loads(path.read_text(encoding="utf-8"))
    one, two = record["turn_1"], record["turn_2"]
    shape = record.get("call_shape", {})
    return [
        "## Follow-up: does `/api/chat` serve the tool round trip?",
        "",
        "The control that works is on the surface the harness did **not** speak, so the "
        "question that decides the port is whether that surface serves tools. Two calls, "
        f"`think: \"{record['think']}\"`, one tool declared and one question that cannot be "
        "answered without it (`probes/probe_native_tools.py`, recorded in "
        "`probes/probe-reasoning-native-tools.json`).",
        "",
        f"* **Turn 1** — HTTP {one['http_status']} in {one['wall_seconds']} s: the reply carries "
        f"`message.tool_calls` ({one['tool_calls_returned']} call), content empty, "
        f"{one['response']['message']['thinking_chars']} characters of thinking.",
        f"* **Turn 2** — HTTP {two['http_status']} in {two['wall_seconds']} s: with the tool "
        "result sent back as a `role: \"tool\"` message, the final answer used it "
        f"(`answer_used_the_tool_result: {two['answer_used_the_tool_result']}`), "
        f"`done_reason: {two['response'].get('done_reason')}`.",
        "",
        "The native shape differs from `/v1` in exactly three places, which is the whole of "
        "the translation now in `kimi_agent.to_native_messages` / `normalise_native`:",
        "",
        "| | `/v1` | native `/api/chat` |",
        "|---|---|---|",
        "| a tool call | `{id, type:\"function\", function:{name, arguments}}` | "
        f"`{{{', '.join(shape.get('keys_on_call', []))}}}`, function keys "
        f"`{{{', '.join(shape.get('keys_on_function', []))}}}`, no `type` |",
        "| its arguments | a JSON **string** | a JSON **object** "
        f"(`{shape.get('arguments_type')}`) |",
        "| a tool reply | `{role:\"tool\", tool_call_id, name, content}` | "
        "`{role:\"tool\", tool_name, content}` |",
        "",
        "Also: the per-turn budget is `options.num_predict`, not `max_tokens`; usage is "
        "`prompt_eval_count` / `eval_count`; the finish reason is `done_reason` (`length` on "
        "a truncated turn, so the `INCOMPLETE_TURN` rule reads it unchanged); reasoning "
        "arrives as `message.thinking`.",
        "",
        "**Verdict: the port is viable, and it was made.** `TaskSpec.transport` is "
        "`\"native\"` by default, `\"v1\"` is selectable per task and is the automatic "
        "one-time fallback if the native surface fails as a transport before any tool call "
        "(recorded as `transport_fallback`). First live task on the ported transport "
        "(`prod-runs-smoke/smoke-native-001`, `think: \"low\"`): COMPLETE in 11.3 s over 4 "
        "turns with **28, 0, 0, 0** characters of reasoning — against 27,000-37,000 "
        "characters *per turn* on `/v1`, which is what had been eating the budget.",
        "",
    ]


def main() -> int:
    if "--report-only" in sys.argv:       # rebuild the write-up from saved records
        REPORT.write_text(report_markdown(load_records()), encoding="utf-8")
        print(f"wrote {REPORT}")
        return 0
    records = []
    for name, runner, extra in PROBES:
        print(f"probing {name} ...", flush=True)
        record = runner(name, extra)
        records.append(record)
        (HERE / f"probe-reasoning-{name}.json").write_text(
            ka.REDACTOR.scrub(json.dumps(record, ensure_ascii=False, indent=2)) + "\n",
            encoding="utf-8")
        print(f"  status={record.get('http_status')} reasoning_chars={record.get('reasoning_chars')} "
              f"completion_tokens={record.get('completion_tokens')} "
              f"wall={record.get('wall_seconds')}s answered={record.get('answered')}", flush=True)
    (HERE / "probe-reasoning-INDEX.json").write_text(
        ka.REDACTOR.scrub(json.dumps(records, ensure_ascii=False, indent=2)) + "\n",
        encoding="utf-8")
    REPORT.write_text(report_markdown(load_records()), encoding="utf-8")
    print("\n".join(row(record) for record in records))
    print(f"wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
