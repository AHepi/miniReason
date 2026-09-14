# Does kimi-k3 honour a reasoning control?

Eight live calls on one tiny prompt, 2026-09-14. One question: can a request ask this model to think less, so that a turn's budget reaches the answer instead of being spent before it? That is now the throughput question for the worker harness — every `INCOMPLETE_TURN` in `RUNS-RECLASSIFIED.md` is a turn whose whole budget went to reasoning.

Prompt (identical in every call, expecting two lines):

```
List the files named in this sentence: a.py, b.py. Answer with one filename per line and nothing else.
```

## Result

| probe | surface | control sent | HTTP | reasoning chars | completion tokens | wall s | answered |
|---|---|---|---|---|---|---|---|
| `v1-baseline` | /v1 | `(none)` | 200 | 135 | 54 | 8.19 | yes |
| `v1-reasoning-effort-low` | /v1 | `{"reasoning_effort": "low"}` | 200 | 163 | 59 | 7.78 | yes |
| `v1-reasoning-object-low` | /v1 | `{"reasoning": {"effort": "low"}}` | 200 | 142 | 48 | 8.04 | yes |
| `v1-think-false` | /v1 | `{"think": false}` | 200 | 160 | 62 | 2.32 | yes |
| `v1-think-low` | /v1 | `{"think": "low"}` | 200 | 108 | 45 | 2.76 | yes |
| `native-baseline` | /api/chat | `(none)` | 200 | 166 | 63 | 9.56 | yes |
| `native-think-false` | /api/chat | `{"think": false}` | 200 | 0 | 12 | 3.78 | yes |
| `native-think-low` | /api/chat | `{"think": "low"}` | 200 | 62 | 32 | 4.5 | yes |

Baselines carry no control at all: **135 reasoning characters** on `/v1`, **166** on `/api/chat`. Read every row against its own surface's baseline.

## What that says

* **`/v1/chat/completions` honours nothing.** `reasoning_effort: "low"`, `reasoning: {"effort": "low"}` and a pass-through `think` are all accepted with HTTP 200 and all return reasoning **no shorter than the uncontrolled baseline** (163, 142 and 160 characters against 135). Accepting a parameter is not honouring it; on this surface these are inert.
* **Ollama's native `/api/chat` honours `think`.** `think: false` removed the reasoning **entirely** (0 characters, 12 completion tokens, 3.8 s against the baseline's 166 characters, 63 tokens, 9.6 s) and still produced the right answer. `think: "low"` shortened it to 62 characters. One sample each, so treat `false` as established (0 is not noise) and `"low"` as suggestive.
* The harness's tool loop speaks `/v1`, because that is the surface whose native `tools` round trip is proven (`probe-01`, `probe-04`). **So the control that works is not on the surface the worker uses.**

## What was done about it

* `TaskSpec.reasoning` (`"default"` | `"low"` | `"off"`) exists and defaults to `"low"` for production tasks. `KimiClient.reasoning_parameter` maps it to `think` **only** on an endpoint marked `native` in the registry; on `/v1` it sends **nothing**, because a parameter this host ignores would make the transcript look like a control had been applied when the probes say it would not be.
* A turn that exhausts its budget on reasoning is retried **once**, with the lowest setting the endpoint honours, recorded as `incomplete_turn_retry`. On `/v1` no setting is honoured, so no retry fires and the run still stops at `INCOMPLETE_TURN` — the machinery is in place for the surface that can use it.
* The real lever on `/v1` is the budget: `MAX_TOKENS` is now **24576** (the 300 s gateway wall at ~90-100 tok/s), not 8192. Every budget-exhausted turn in the recorded battery stopped at exactly 8192 tokens with 28k-37k characters of reasoning behind it: the reasoning fits inside 24576 with room for an answer, and does not fit inside 8192.
* **Open, and worth one experiment before it is assumed:** whether `/api/chat` serves the same `tools` round trip. If it does, porting the transport buys `think: false` on worker turns, which is the only measured way to stop reasoning eating a turn on this host.

## Exact request bodies (headers omitted: they carry the credential)

### `v1-baseline` — `POST https://ollama.com/v1/chat/completions`

```json
{
  "model": "kimi-k3",
  "messages": [
    {
      "role": "user",
      "content": "List the files named in this sentence: a.py, b.py. Answer with one filename per line and nothing else."
    }
  ],
  "stream": false,
  "max_tokens": 2048
}
```

### `v1-reasoning-effort-low` — `POST https://ollama.com/v1/chat/completions`

```json
{
  "model": "kimi-k3",
  "messages": [
    {
      "role": "user",
      "content": "List the files named in this sentence: a.py, b.py. Answer with one filename per line and nothing else."
    }
  ],
  "stream": false,
  "max_tokens": 2048,
  "reasoning_effort": "low"
}
```

### `v1-reasoning-object-low` — `POST https://ollama.com/v1/chat/completions`

```json
{
  "model": "kimi-k3",
  "messages": [
    {
      "role": "user",
      "content": "List the files named in this sentence: a.py, b.py. Answer with one filename per line and nothing else."
    }
  ],
  "stream": false,
  "max_tokens": 2048,
  "reasoning": {
    "effort": "low"
  }
}
```

### `v1-think-false` — `POST https://ollama.com/v1/chat/completions`

```json
{
  "model": "kimi-k3",
  "messages": [
    {
      "role": "user",
      "content": "List the files named in this sentence: a.py, b.py. Answer with one filename per line and nothing else."
    }
  ],
  "stream": false,
  "max_tokens": 2048,
  "think": false
}
```

### `v1-think-low` — `POST https://ollama.com/v1/chat/completions`

```json
{
  "model": "kimi-k3",
  "messages": [
    {
      "role": "user",
      "content": "List the files named in this sentence: a.py, b.py. Answer with one filename per line and nothing else."
    }
  ],
  "stream": false,
  "max_tokens": 2048,
  "think": "low"
}
```

### `native-baseline` — `POST https://ollama.com/api/chat`

```json
{
  "model": "kimi-k3",
  "stream": false,
  "messages": [
    {
      "role": "user",
      "content": "List the files named in this sentence: a.py, b.py. Answer with one filename per line and nothing else."
    }
  ]
}
```

### `native-think-false` — `POST https://ollama.com/api/chat`

```json
{
  "model": "kimi-k3",
  "stream": false,
  "messages": [
    {
      "role": "user",
      "content": "List the files named in this sentence: a.py, b.py. Answer with one filename per line and nothing else."
    }
  ],
  "think": false
}
```

### `native-think-low` — `POST https://ollama.com/api/chat`

```json
{
  "model": "kimi-k3",
  "stream": false,
  "messages": [
    {
      "role": "user",
      "content": "List the files named in this sentence: a.py, b.py. Answer with one filename per line and nothing else."
    }
  ],
  "think": "low"
}
```

Per-probe records, including each answer and the sha256 of the reasoning text (never the text): `probes/probe-reasoning-*.json`.

## Follow-up: does `/api/chat` serve the tool round trip?

The control that works is on the surface the harness did **not** speak, so the question that decides the port is whether that surface serves tools. Two calls, `think: "low"`, one tool declared and one question that cannot be answered without it (`probes/probe_native_tools.py`, recorded in `probes/probe-reasoning-native-tools.json`).

* **Turn 1** — HTTP 200 in 2.12 s: the reply carries `message.tool_calls` (1 call), content empty, 163 characters of thinking.
* **Turn 2** — HTTP 200 in 1.48 s: with the tool result sent back as a `role: "tool"` message, the final answer used it (`answer_used_the_tool_result: True`), `done_reason: stop`.

The native shape differs from `/v1` in exactly three places, which is the whole of the translation now in `kimi_agent.to_native_messages` / `normalise_native`:

| | `/v1` | native `/api/chat` |
|---|---|---|
| a tool call | `{id, type:"function", function:{name, arguments}}` | `{function, id}`, function keys `{arguments, index, name}`, no `type` |
| its arguments | a JSON **string** | a JSON **object** (`dict`) |
| a tool reply | `{role:"tool", tool_call_id, name, content}` | `{role:"tool", tool_name, content}` |

Also: the per-turn budget is `options.num_predict`, not `max_tokens`; usage is `prompt_eval_count` / `eval_count`; the finish reason is `done_reason` (`length` on a truncated turn, so the `INCOMPLETE_TURN` rule reads it unchanged); reasoning arrives as `message.thinking`.

**Verdict: the port is viable, and it was made.** `TaskSpec.transport` is `"native"` by default, `"v1"` is selectable per task and is the automatic one-time fallback if the native surface fails as a transport before any tool call (recorded as `transport_fallback`). First live task on the ported transport (`prod-runs-smoke/smoke-native-001`, `think: "low"`): COMPLETE in 11.3 s over 4 turns with **28, 0, 0, 0** characters of reasoning — against 27,000-37,000 characters *per turn* on `/v1`, which is what had been eating the budget.
