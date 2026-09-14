> Published verbatim, body unedited: written against the staging tree, so the `NOTES.md` it cites is published here as [`docs/sources/provider-openai-compat-smoke-notes-2026-09-14.md`](../sources/provider-openai-compat-smoke-notes-2026-09-14.md), and its per-finding review closure as [`docs/sources/provider-openai-compat-review-fixes.md`](../sources/provider-openai-compat-review-fixes.md).

# Multi-endpoint transport (OpenAI-compatible and native Ollama)

`src/minireason/provider_openai_compat.py` is a second transport beside
`src/minireason/provider.py`. `provider.py` is the DeepSeek arm's transport and
is not changed by this work; it stays the single place the DeepSeek campaign
speaks through. The new module exists so a Mini manifest or a probe can be run
against *any* declared endpoint — DeepSeek's own `/v1/chat/completions`, Ollama
cloud's OpenAI-compatible `/v1/chat/completions`, or Ollama cloud's native
`POST /api/chat` — without a second set of habits about credentials and records.

## The discipline it mirrors

Every obligation `provider.py` carries, this module carries, and the offline
suite checks each one:

| Obligation | How |
|---|---|
| Exact request bytes recorded before the send | The payload is serialised once; `call-NNNN.request.json` carries the payload, its canonical `request_sha256` and the `request_bytes_sha256` of the literal bytes, and is written before the socket exists |
| Write-once records | Every record file is opened `"x"`; a second write to a path raises `FileExistsError` |
| Redaction on write | `write_new` replaces every credential visible to the process with `[REDACTED_CREDENTIAL]`, longest value first, in the raw value **and** in its JSON-escaped rendering, and names the environment variables it replaced under `credentials_redacted`. Two stated bounds: a value shorter than **8 characters** is not treated as a credential at all — it is never redacted, never echo-checked and never a refusal, because a one-character environment value would shred every record — and "visible to the process" means the registry's own `key_env` names, `DEEPSEEK_API_KEY`/`OLLAMA_API_KEY`, and any name a caller declared through `register_secret_envs` (which `tools/provider_smoke.py` calls with every name its env file loaded). It is **not** a scan of `os.environ` by name shape |
| Credential never sent in content | A credential found in the payload or the coordinate is `SECRET_IN_REQUEST`; the request is never sent and a sanitised failure record is still written |
| Credential echo is loud | A credential anywhere in the provider's body is `CREDENTIAL_ECHO`; the answer is redacted and the call fails |
| No redirects | `_NoRedirect` refuses every 3xx, so a credentialed request cannot be replayed at another host |
| No reasoning text persisted | `reasoning_content` / `reasoning` / native `thinking` are read only to set `reasoning_content_present`; `reasoning_content_persisted` is always `false`, and the raw chat body is never stored — only its sha256. The single exception is `list_models`, whose (redacted) model list is kept under `models` |
| Thinking control verified, not just requested | For `family == "deepseek"`, when a `thinking` value was sent, `reasoning_content_present != thinking` is `THINKING_MODE_MISMATCH` — `provider.py:169-170`'s check, kept |
| No retries of any kind | One `complete` is one request or none. A failure is recorded and raised |
| Key read at call time | The key is read from `os.environ[endpoint.key_env]` inside `complete`, never stored on the object, never placed in a record |

A record never contains the key, the `Authorization` value, or the raw provider
chat body; nor does the `record` attached to a `ProviderFailure`, which is
redacted the same way before a caller can log it. The model list `list_models`
returns is the one provider body a record keeps, after redaction. It does contain: the request, both request hashes, the URL and method, the
request *header names*, the endpoint's public identity (`name`, `base_url`,
`model`, `family`), the settings (including `key_env`, a name), `started_at`,
`elapsed_ms`, `provider_response_sha256`, `returned_model`, `usage`,
`finish_reason`, the public answer `content`, `reasoning_content_present`,
`reasoning_content_persisted: false`, `credential_redaction`, `usage_source`
(`provider-reported`, or `native-normalised` when this module supplied a count
Ollama omitted) and `status`, plus `credentials_redacted` when a credential was
replaced on the way to disk.

An **offline** record says so in its own field names: `url` is `null`, the
destination that was *not* contacted is `not_contacted_url`,
`request_header_names` is empty, and the size and digest of the body that would
have gone out are `would_send_bytes` / `would_send_bytes_sha256`. No offline
record can be read as evidence that a credentialed request was formed.

Status codes: `COMPLETE`, `INCOMPLETE_GENERATION`, `EMPTY_GENERATION`,
`USAGE_UNAVAILABLE`, `THINKING_MODE_MISMATCH`, `CREDENTIAL_ECHO`,
`SECRET_IN_REQUEST`, `CONTENT_TYPE`, `KEY_MISSING`, `RECORD_EXISTS`,
`HTTP_<code>`, `TRANSPORT_OR_RESPONSE_ERROR`. `COMPLETION_CEILING_VIOLATED` is
the one `provider.py` code this module does **not** carry; see NOTES.md
finding 5.

`extra={...}` may not carry a key this module builds (`model`, `messages`,
`stream`, `max_tokens`/`format`, `temperature`, `seed`, `response_format`,
`thinking`, `reasoning_effort`): overriding one would leave the record's
`settings` block contradicting the wire, so it is a `ValueError` before a call
number is spent. On a native endpoint `extra={"options": {...}}` is **deep
merged** into the built options, so a caller-supplied option cannot silently
delete `options.num_predict` while the record still claims a ceiling.

## The per-key concurrency rule

The owner's authorisation for this work is **five concurrent requests per
credential**. `provider.py` holds one process-wide `BoundedSemaphore(5)`; this
module holds a module-level registry of semaphores keyed by `key_env`, so every
`OpenAICompatProvider` in the process that spends `OLLAMA_API_KEY` competes for
the same five slots, and `DEEPSEEK_API_KEY` has its own five. Eleven Ollama
models probed at once are therefore still five requests on the wire.

The first provider to claim a `key_env` fixes its ceiling. An endpoint that
later asks for a different ceiling for that same credential is refused with
`CONCURRENCY_LIMIT_CONFLICT` rather than quietly widening or narrowing an
authorisation already in force.

## `endpoints.json`

`src/minireason/data/endpoints.json` is the registry, loaded into
`ENDPOINTS: dict[str, Endpoint]` at import. Each entry declares
`name`, `base_url`, `model`, `key_env`, `family` and optionally `chat_path`,
`native`, `max_concurrency`, `timeout_seconds`. **Credentials appear only as an
environment variable name.** `family` is a free label (`deepseek`,
`ollama-cloud/gpt-oss`, …); DeepSeek's thinking controls (`thinking`,
`reasoning_effort`) are only accepted when `family == "deepseek"`, and asking
for them elsewhere is a `ValueError` before any call number is spent.

Each Ollama model ships twice: `ollama/<model>` on the OpenAI-compatible base
`https://ollama.com/v1`, and `ollama/<model>.native` on `https://ollama.com`
with `chat_path: /api/chat` and `native: true`. The native provider translates
the request (`max_tokens` → `options.num_predict`, `temperature`/`seed` →
`options`, `response_format` → `format`) and normalises the reply
(`done_reason` → `finish_reason`, `prompt_eval_count`/`eval_count` → `usage`,
`message.thinking` → `reasoning_content_present`) into the same `CallResult`.
Ollama omits `prompt_eval_count` when the prompt was served entirely from its
prompt cache; that is read as `prompt_tokens: 0` — Ollama's own semantics for a
full cache hit — and the record carries `usage_source: "native-normalised"` so
the count is never mistaken for a provider-reported one. A missing
`eval_count` is still `USAGE_UNAVAILABLE`.

## Running against a Mini manifest

`responder_for(endpoint, records_dir, settings)` returns a responder with
`provider.MiniResponder`'s interface (`reply(Request) -> Reply`, plus
`completion_cap`), so a manifest can be executed against any endpoint. Native
reasoning text never reaches the Mini run, exactly as in the DeepSeek arm.
For an endpoint whose `family` is `deepseek` the responder defaults `thinking`
to `False`, mirroring `provider.Settings.thinking`, so a manifest ported from
`provider.MiniResponder` keeps sending `thinking: {"type": "disabled"}` rather
than inheriting the provider's own default. For every other family no thinking
control is sent at all.
`OfflineProvider(endpoint, records_dir, script)` is the zero-network stand-in:
same interface, same records, same status machinery, no key read, so a plan's
record discipline and credential refusal can be preflighted before a token is
spent. It accepts and refuses **exactly** the argument sets the live provider
does (one `_validate_call_args`), so a plan that passes the preflight cannot
die on its first live call over an argument.

## Running the smoke

```
python3 tools/provider_smoke.py RECORDS_DIR --env-file /path/to/.env
```

`RECORDS_DIR` must be new or empty — records are write-once. Every probe gets
its own `RECORDS_DIR/<endpoint>/<label>/` directory, so two probes of one
endpoint (the `--headroom` probe in particular) cannot collide on
`call-0001.request.json`. The tool loads
`NAME=value` lines into this process's environment (it never prints, echoes or
returns any part of a value), then for every registry endpoint whose key is
present sends **one** small call:
`Reply with a JSON object {"ok": true, "model": <your model name>}`, JSON mode
on, `max_tokens 64` by default, `seed 7` where the family supports it. It asks
each OpenAI-compatible base for `/models` once. It prints status, returned
model, finish reason, latency, whether the answer parsed as JSON, whether
native reasoning was present, and usage, and writes `smoke-summary.json`.

For an Ollama model the OpenAI-compatible path is tried first; **only if that
call does not come back `COMPLETE`** does the tool send one call to that
model's declared native endpoint. That is a second declared path recorded as
its own call, not a retry: neither path is attempted twice. `--headroom N`
likewise sends one further call at a different declared ceiling to endpoints
that ran out of tokens — a separate probe with different settings, printed
under its own label, never a silent second attempt at the same configuration.

Useful flags: `--max-tokens`, `--only NAME …` (taken literally, so a native
entry can be addressed directly), `--workers` (the per-key semaphores still cap
each credential at five).

## What is never recorded

Key values or any fragment of one; the `Authorization` header value; the raw
provider **chat** response body; native reasoning / thinking text. The one
carve-out is `list_models`, which keeps the parsed (and redacted) model list
under `models`, because a model list carries no reasoning text and its whole
point is to be read later. The offline suite asserts that no sentinel
credential or six-character prefix of one survives in any record written during
a full exercise of the transport, **and** that no fragment survives on the
`record` attached to a `ProviderFailure` on either of the two paths that carry a
provider- or caller-supplied body (`SECRET_IN_REQUEST` and `list_models`'
`CREDENTIAL_ECHO`).
