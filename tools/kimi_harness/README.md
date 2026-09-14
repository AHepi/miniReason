# kimi-k3 worker harness

**Where this lives now.** This harness was written and run in an ephemeral session scratchpad
at `<scratchpad>/kimi/`, and the README below is that document unchanged. It is published here
as `tools/kimi_harness/` under REC-20260914-AC because owner ruling 16 made Kimi K3 the default
worker for mechanical tasks, which makes the harness an instrument of record rather than a
scratch script. Read every `kimi/...` path below as `tools/kimi_harness/...`; the run records,
the battery and the Opus controls are published separately, under
[`experiments/diagnostics/K001-kimi-k3-subagent-battery/`](../../experiments/diagnostics/K001-kimi-k3-subagent-battery/),
and the owner's report is
[`docs/reviews/kimi-k3-subagent-2026-09-14/REPORT.md`](../../docs/reviews/kimi-k3-subagent-2026-09-14/REPORT.md).
The battery's frozen corpus (`battery/material/`) and the transcripts are **not** published; the
K001 README and `TRANSCRIPTS.md` there say why and record what would prove a recovered copy.

**Running its tests from the repository root** — the 49 offline tests need no network and no
credential, and the suite adds its own parent directory to `sys.path`:

```bash
python3 -m unittest discover -s tools/kimi_harness/tests -t tools/kimi_harness
```

---

# kimi-k3 as a worker agent

A subagent harness that gives **`ollama/kimi-k3`** (Ollama cloud, OpenAI-compatible
`https://ollama.com/v1/chat/completions`) real tools against a sandboxed copy of
declared repository paths, and records everything it did.

Everything here lives in the session scratchpad. `/home/user/miniReason` is
read-only to this harness: a task's declared paths are **copied** into a
per-task sandbox and the agent can only ever write there.

```
kimi/
  kimi_agent.py           the harness: transport, sandbox, tools, loop, transcript
  run_battery.py          runs battery/tasks.json concurrently and writes runs/SUMMARY.md
  battery/tasks.json      the TaskSpec list
  probes/                 run_probes.py + one JSON record per live capability probe
  runs/<task id>/         transcript.jsonl, result.json, sandbox/
  reclassify.py           re-reads runs/, runs-pass2/, runs-pass3/ under the
                          current statuses (read-only) and writes
  RUNS-RECLASSIFIED.md    one row per (pass, task): recorded vs reclassified
  smoke/                  hello.py and task.json for the live smoke run
  tests/test_kimi_agent.py  49 offline tests (fake transport, no network, no key)
  prod-runs-smoke/        the first live run on the native transport
  probes/probe_native_tools.py    the native tool round trip that decided the port
  probes/run_reasoning_probes.py  the reasoning-control probes, written up in
  PROBE-REASONING.md      does kimi-k3 honour a reasoning control? (measured)
  PRODUCTION.md           how to author a task now that this is a production worker
```

## How to run

```bash
cd kimi

# offline tests (no network, no credential)
python3 -m unittest discover -s tests -t .

# one task
python3 kimi_agent.py smoke/task.json

# the battery, up to 8 concurrent
python3 run_battery.py                          # all tasks in battery/tasks.json
python3 run_battery.py --only b-001 b-004       # a subset
python3 run_battery.py --tasks battery/tasks.json --runs-dir runs --workers 8
```

The credential is read at call time from `OLLAMA_API_KEY` in the process
environment, or from the gitignored `/home/user/miniReason/.env` if the
environment does not carry it. Nothing else needs to be set.

A `TaskSpec` is: `id`, `title`, `prompt`, `context_paths` (repo-relative, copied
into the sandbox), `expected_outputs`, `evaluation`, and optionally `mode`
(`tools` | `packed`), `max_iterations` (default 40), `max_tokens` (24576),
`command_timeout` (120 s), `verify_command` (packed mode), `repo_root`,
`reasoning` (`default` | `low` | `off`, default `low`) and `transport`
(`native` | `v1`, default `native`).

## Two surfaces, one representation

The loop speaks Ollama's native `/api/chat` by default, because that surface
**honours `think`** — `"low"` on the smoke task left 28, 0, 0, 0 characters of
reasoning across four turns, against 27k-37k characters *per turn* on `/v1` —
and serves the same tool round trip (`PROBE-REASONING.md`). The OpenAI-compatible
`/v1` surface remains selectable per task (`"transport": "v1"`).

Only the transport knows which surface answered. `to_native_messages` and
`normalise_native` translate in one place, so the loop, the transcript, the
status rules and every test see one message-and-tool-call representation. The
three differences that translation covers: a tool call carries no `type` wrapper
and its arguments are a JSON **object**, a tool reply is addressed by `tool_name`
rather than `tool_call_id`, and the per-turn budget is `options.num_predict`.

If the native surface fails **as a transport** (`TRANSPORT_OR_RESPONSE_ERROR`,
`HTTP_400/404/405`) *before the run has seen any tool call*, the same turn is
sent once on `/v1` and the switch is recorded as `transport_fallback`. After a
tool call it is not: the conversation is surface-shaped by then, and switching
would quietly change what the model was told. A provider `HTTP_500` is not a
fallback trigger — that is a failure of the run, not evidence against the
surface.

## Run statuses

A run ends with exactly one status. **`COMPLETE` is the only one that claims the
work was done**, and it has to earn both halves of that claim: the final turn
finished on its own *and* every declared `expected_output` exists in the
sandbox. The other four each name a different way a run stopped short, so that
"the loop ended" is never recorded as "the task was delivered".

| status | when | `harness_failure` | what it means |
|---|---|---|---|
| `COMPLETE` | last turn `finish_reason: stop`, no tool call, and **every** `expected_output` exists | – | the run finished and delivered |
| `INCOMPLETE_TURN` | last turn had a **non-`stop`** finish (`length` in practice), **no** tool call and **no** content | `TURN_BUDGET_EXHAUSTED_BY_REASONING` | a resource boundary on the turn: the whole per-turn `max_tokens` budget went to native reasoning, so the turn produced neither an action nor an answer. Not a completion |
| `NO_DELIVERABLE` | last turn `finish_reason: stop`, but at least one `expected_output` is missing | – (not a harness fault) | the model talked its way to a stop without writing what the task asked for |
| `ITERATION_CAP` | `max_iterations` reached while still calling tools | `ITERATION_CAP` | ran out of turns, not out of budget |
| `HARNESS_FAILURE` | the harness or the provider failed the call | `HTTP_500`, `MALFORMED_TOOL_CALL_JSON`, `SECRET_IN_REQUEST`, … | no usable run |

`result.json` carries the two lists the deliverable check is made from —
`expected_outputs_present` and `expected_outputs_missing` — so the verdict can
be re-derived without re-reading the sandbox. An `expected_output` written with
a trailing `/` (or naming a directory) counts as present only when the
directory exists **and** holds at least one file; an empty directory is not a
deliverable.

A turn that exhausts its budget is retried **once** at the lowest reasoning
setting the endpoint honours (`think: false` on the native surface), recorded as
`incomplete_turn_retry`; on `/v1`, which honours none, nothing is retried and the
run stops as before.

On an `INCOMPLETE_TURN` the transcript gains an `incomplete_turn` event
recording, for that turn, its `finish_reason`, its `completion_tokens` against
the `max_tokens` budget, and the reasoning that consumed them as
`reasoning_content_sha256` / `reasoning_content_chars` /
`reasoning_tokens_estimated`. The reasoning **text** is still never persisted.

Recorded runs under `runs/`, `runs-pass2/` and `runs-pass3/` predate these two
statuses and were written by the old rule, under which any turn without a tool
call ended the loop as `COMPLETE`. They are left exactly as recorded;
`reclassify.py` re-reads them under the rules above and writes
`RUNS-RECLASSIFIED.md` beside them (`python3 reclassify.py`).

## Probe findings (capabilities)

Five live calls, one per question, each recorded under `probes/probe-*.json`
(request shape, response, usage, latency; any reasoning text replaced by its
sha256 and length before the record was written).

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1 | OpenAI `tools` / `tool_choice`, does it return `tool_calls`? | **Yes.** `finish_reason: "tool_calls"`, `message.content` empty, `tool_calls[0].function.arguments` a JSON **string**; a non-standard `index` field rides along. 2.2 s | `probe-01-tools.json` |
| 2 | `response_format` JSON mode | **Yes**, `{"type":"json_schema", strict}` accepted and honoured (reply was exactly the declared object). `{"type":"json_object"}` is already proven in-repo by the C001 kimi-k3 records (`status: COMPLETE`) | `probe-02-json-schema.json`, `experiments/diagnostics/C001-.../ollama-kimi-k3/` |
| 3 | `max_tokens` | **32768 accepted** on every probe; no ceiling error at any point. But a 300 s gateway wall at ~90-100 tok/s puts the *reachable* ceiling near 25k, so the harness default is **24576** | all probes; ruling 13 |
| 4 | Reasoning fields | Native reasoning arrives as **`message.reasoning`** (not `reasoning_content`) on the `/v1` surface, on **every** probe. `usage` carries **no** `completion_tokens_details`, so a reasoning token count has to be derived (4 chars/token) — the harness records it as `reasoning_tokens_estimated`. `reasoning_effort: "low"` is **accepted and ignored** on this surface — the eight-call follow-up in `PROBE-REASONING.md` finds `reasoning_effort`, `reasoning: {effort}` and `think` all returning reasoning no shorter than the uncontrolled baseline on `/v1`, while Ollama's native `/api/chat` honours `think: false` (0 characters) and `think: "low"` (62 against 166). The earlier single-sample "suggestive" reading is **withdrawn** | `PROBE-REASONING.md`, `probe-03-reasoning-effort.json` |
| 5 | Multi-turn tool round trip | **Yes.** An assistant turn carrying `tool_calls` plus a `role: "tool"` reply is accepted and the model answers from the tool result (`finish_reason: "stop"`) | `probe-04-tool-roundtrip.json` |
| 6 | Context size reached | **56,197 prompt tokens accepted** (240,117 characters of repository Python), answered in 10.6 s, `finish_reason: "stop"`, and the answer was **correct about the tail of the prompt** (24 `###` headers, last file `src/creib/forge/conformance/corpus.py`) — so the long prompt was genuinely read, not truncated. The upper bound was not probed | `probe-05-context-60k.json` |

Also observed: `usage.prompt_tokens_details.cached_tokens` is reported;
`system_fingerprint` is `fp_ollama`; responses are `chatcmpl-*`.

**Mode implemented: `tools`** (native tool calling), because probe 1 and probe 5
show it works end to end. The **packed-context fallback is implemented as well**
(`mode: "packed"`): the declared files are inlined into one prompt, fenced
blocks tagged ` ```path=relative/file.py ` are parsed into sandbox writes, and
an optional `verify_command` failure is fed back for one more turn. Task
`b-004` exercises that path.

## What the harness guarantees about the credential

* The key is read at call time from the environment or the gitignored `.env`,
  is never stored on a record, and never appears in any argument list.
* Every byte that reaches disk — transcripts, `result.json`, `SUMMARY.md`,
  probe records — passes through `Redactor.scrub`, which replaces **the key and
  its first 12 characters**, in raw form *and* in JSON-escaped form, with
  `[REDACTED_CREDENTIAL]`. Longest rendering first, so a prefix cannot leave a
  tail behind. Values shorter than 8 characters are never treated as secrets
  (the repository transport's documented floor).
* An outgoing payload containing a credential is refused (`SECRET_IN_REQUEST`)
  before the socket is touched; a credential echoed in a provider body is
  `CREDENTIAL_ECHO` and the call fails.
* `run_command` subprocesses are given an environment **with the key removed**,
  so model-authored code cannot read it even though it runs locally.
* `.env` (and `.git`, `__pycache__`, virtualenvs) are never copied into a
  sandbox, and declaring `.env` as a context path is refused.
* **Native reasoning text is never persisted.** The transcript records
  `reasoning_content_present`, `reasoning_content_sha256`,
  `reasoning_content_chars`, `reasoning_tokens_estimated` and a constant
  `reasoning_content_persisted: false`. The text is dropped before the response
  object is constructed and is never fed into another call.
* A scan of every file under `kimi/` after the probes and the smoke run found
  no occurrence of the key or its 12-character prefix.

## Limits, stated rather than implied

* **Concurrency**: a process-wide `BoundedSemaphore(8)` keyed by
  `OLLAMA_API_KEY` (the owner authorises 10 on this key; 2 are held in reserve).
  The repository transport's own ceiling is 5 per key and is untouched — this
  harness does not import it, so the two limits cannot be conflated in one
  process. A second, different ceiling for the same key is refused
  (`CONCURRENCY_LIMIT_CONFLICT`).
* **No retries on HTTP errors.** One `chat` is one request on the wire or none;
  an HTTP error is recorded and fails the task (`harness_failure: HTTP_429`,
  etc.). The **only** retry is one per task on malformed tool-call JSON: the
  unusable assistant turn is dropped, the event is recorded
  (`malformed_tool_call` + `retry`), and a second malformed call fails the task
  with `MALFORMED_TOOL_CALL_JSON`. Two further single-shot exceptions, each
  recorded: the `transport_fallback` above, and the one `incomplete_turn_retry`
  a budget-exhausted turn earns at the lowest reasoning setting the endpoint
  honours (now `think: false`, since the default surface honours it).
* **Iteration cap** 40 by default; hitting it ends the task with
  `status: ITERATION_CAP` and `harness_failure: ITERATION_CAP`.
* **Per-turn token budget.** `max_tokens` bounds *one* turn, and on this
  provider native reasoning is billed against it. A turn that spends the whole
  budget on reasoning comes back `finish_reason: length` with empty content and
  no tool call; that ends the run as `INCOMPLETE_TURN` /
  `TURN_BUDGET_EXHAUSTED_BY_REASONING`. The harness does **not** retry it or
  raise the budget — it records the boundary and stops.
* **Per call**: `max_tokens` 24576 (the 300 s wall, not the model's ceiling),
  timeout 600 s — which the gateway never lets you reach.
* **`run_command` allow-list**: `python3 -m unittest …`, `python3 -m pytest …`,
  `python3 -c …`, `python3 <file>.py …`. Nothing else runs — no shell, no pip,
  no network tooling. Be clear-eyed about what this is: `python3 -c` is
  arbitrary Python. It is confined by *cwd inside the sandbox*, a scrubbed
  environment, a 120 s timeout and a 20,000-character output cap — not by a
  syscall sandbox. Do not point a task at material you would not let arbitrary
  Python touch.
* **Path confinement** is by resolved-path containment: absolute paths, `..`
  escapes and symlink escapes are refused with `PATH_REFUSED`, and the refusal
  is handed back to the model as a tool result rather than killing the run.
* **The sandbox is a copy.** Nothing the worker writes reaches
  `/home/user/miniReason`. `result.json` lists every changed file with its
  sha256 and whether it was added, modified or removed; applying any of it is a
  separate, human decision.
* **Transcripts keep full message text** (system prompt, task prompt, tool
  results, final answer) — redacted, but complete. Do not put anything in a
  task prompt that should not be written down.
* `httpx` is not installed in this environment, so the transport uses
  `urllib.request` with a no-redirect opener (a credentialed request is never
  replayed at another host). It honours the session's `HTTPS_PROXY` and
  `SSL_CERT_FILE`.
* Not probed: the true context ceiling above ~56k tokens, streaming, parallel
  tool calls in one turn (the loop handles a list, but no probe produced one),
  and whether the native `/api/chat` surface serves the same `tools` round trip
  (the one experiment that would buy a working reasoning control on worker turns).

## Verification performed

* `python3 -m unittest discover -s tests -t .` — **49 tests, OK**. They cover
  tool dispatch, the tool round trip and transcript shape, sandbox confinement
  (a `../` write is refused and recorded), `.env` never copied, the command
  allow-list (7 refusals, 4 acceptances), the subprocess not seeing the key,
  command timeout and output cap, redaction (raw, prefix, JSON-escaped, the
  8-character floor, transcript lines), the iteration cap, the single malformed
  tool-call retry and the failure on a second one, HTTP failure without retry,
  packed-mode fence writes and the feedback turn, the concurrency ceiling, and
  the two status rules added after the labelling defect: a budget-exhausted
  final turn recorded as `INCOMPLETE_TURN` (with the completion-token count and
  the reasoning digest in the transcript, and the reasoning text still absent),
  a non-`stop` finish that *did* say something staying `COMPLETE`, a `stop`
  with no expected output recorded as `NO_DELIVERABLE`, and `COMPLETE`
  surviving only when every declared output exists; and the reasoning control:
  `/v1` sending no control at all while a `native` endpoint sends `think`, the
  one retry a budget-exhausted turn earns where a control exists, and no retry
  (the previous stop) where none does; and the native transport: messages and
  tool calls translated both ways, a full native round trip driving the loop
  offline, the fallback firing once and being recorded, and the fallback
  refused after a tool call and for a provider 500.
* One **live** task on the ported transport, `prod-runs-smoke/smoke-native-001`:
  `COMPLETE` in 11.3 s, 4 turns, 3 tool calls, 5,693 tokens, both expected
  outputs written, and the sha256 in `out/sha.md` equal to `sha256sum`'s.
* One **live** end-to-end smoke run, `runs/smoke-001/`: 6 iterations, 8 tool
  calls (2 read, 4 write, 2 run), 12,939 tokens, 34.0 s, `finish_reason: stop`,
  no harness failure. kimi-k3 added `twice(x)`, wrote a four-case unittest, hit
  `Start directory is not importable`, added `smoke/__init__.py`, re-ran, and
  finished with `Ran 4 tests ... OK` — a real read-edit-run-repair loop.
* `run_battery.py` was exercised offline against all four battery tasks with a
  fake transport (real sandboxes, real `SUMMARY.md`); the battery has **not**
  been run live.

A note on housekeeping: another agent in this session is writing under
`kimi/probe/` and `kimi/battery/material/`. Those paths are not part of this
harness; everything listed in the tree at the top of this file is.
