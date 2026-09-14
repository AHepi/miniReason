> Published verbatim, body unedited: this document was written against the staging tree, so `NOTES.md`, `FIXES.md`, the staged `src`/`tests`/`tools` paths and the smoke-records directory it names are that scratchpad tree and not any path in this repository, where the files it describes are `src/minireason/provider_openai_compat.py`, `src/minireason/data/endpoints.json`, `tools/provider_smoke.py`, `tests/test_provider_openai_compat.py`, `docs/workflows/provider-openai-compat.md` and `docs/sources/provider-openai-compat-review-fixes.md`; the live smoke records stay outside the repository and are not published, and the staged `src/minireason/__init__.py` shim was not published.

# Staging notes — multi-endpoint transport and live smoke

Staged at `/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/provider/`
in repository layout. `/home/user/miniReason` was **not modified** (`git status --porcelain`
empty; HEAD `8a99d3f`). The staging tree reaches the existing packages through
symlinks into the repository, so `PYTHONPATH=<staging>/src` runs the new module
beside the untouched `minireason.provider`.

Files: `src/minireason/provider_openai_compat.py`, `src/minireason/data/endpoints.json`,
`tests/test_provider_openai_compat.py`, `tools/provider_smoke.py`,
`docs/workflows/provider-openai-compat.md`, this file.

## Offline tests

`PYTHONPATH=<staging>/src python3 -m unittest tests.test_provider_openai_compat`
— **59 tests, OK, 0.19 s, no socket opened.** Coverage: request record written
before the send (asserted from inside the transport seam), exact request bytes
hashed into that record, write-once (`"x"`) records, redaction on write,
`SECRET_IN_REQUEST` for a credential in the prompt or the coordinate (including
a credential belonging to a *different* endpoint), `CREDENTIAL_ECHO` in answer
and in metadata, `KEY_MISSING` at construction and at call time, `HTTP_<code>`
and `TRANSPORT_OR_RESPONSE_ERROR` recorded once with no retry, `CONTENT_TYPE`,
`INCOMPLETE_GENERATION`, `EMPTY_GENERATION`, `USAGE_UNAVAILABLE`, redirect
refusal (handler and opener wiring), native `/api/chat` request translation and
reply normalisation, DeepSeek thinking controls accepted only for
`family == "deepseek"`, DeepSeek JSON-mode prompt-keyword guard, per-key
semaphore sharing (eight providers on one `key_env` peak at exactly 5; four on
each of two `key_env`s peak at exactly 8), ceiling-conflict refusal,
`OfflineProvider` (records, status machinery, credential refusal, no socket even
with an empty environment), `endpoints.json` loads and every entry is
well-formed, registry declares keys by env name only, Mini responder parity, and
a full-exercise scrub asserting no sentinel credential or 6-character prefix
survives in any record.

## Live smoke

`python3 tools/provider_smoke.py <records dir> --env-file /home/user/miniReason/.env`

Records (outside the repository) under
`/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/provider-smoke/`:
`trial-deepseek-flash` (2 calls, wiring check), `run-01` (23 calls, the specified
probe), `run-02-ceiling-512` (15 calls), `run-03-native-512` (12 calls) — 52 in
total, 46 chat and 6 model-list. The 12th call of `run-03-native-512` was the
model-list request made by the **pre-fix** tool against the native base, which
is where finding 6's `HTTP_307` record comes from; the shipped tool asks only
the OpenAI-compatible base, so replaying that invocation now yields 11 calls
and no 307. A replay that comes back one call short is not a discrepancy.
Records are now written under `<records dir>/<endpoint>/<label>/`, one
directory per probe, so the tables above (written when every probe of an
endpoint shared one directory) describe the same calls at a slightly different
path. Every call has one `.request.json` written
before the send and exactly one `.response.json`; no record was rewritten. Concurrency was left to the per-key semaphores: at most 5
requests per credential at any moment, 10 across the two keys.

Prompt in every call: `Reply with a JSON object {"ok": true, "model": <your model name>}`,
JSON mode on (`response_format {"type":"json_object"}`, translated to `format: "json"`
on the native path), `seed 7` for the Ollama families, no seed for DeepSeek
(its API declares none and `docs/PROVIDER.md` claims no determinism there),
temperature left at the provider default.

`json` below is a strict `json.loads` of the returned content, so a fenced
```json block counts as **no**.

### Model lists (recorded)

* `GET https://api.deepseek.com/v1/models` → `COMPLETE`, 752–910 ms, 2 models:
  `deepseek-flash`, `deepseek-v4-pro`. Confirms `docs/PROVIDER.md`.
* `GET https://ollama.com/v1/models` → `COMPLETE`, 511–563 ms, 20 models:
  `deepseek-v4-flash:0731`, `deepseek-v4-pro:0813`, `deepseek-v4.1-flash`,
  `gemma4:31b`, `glm-5.1`, `glm-5.2`, `glm-5.3`, `glm-5.3-flash`, `gpt-oss:120b`,
  `gpt-oss:20b`, `kimi-k2.6`, `kimi-k2.7-code`, `kimi-k3`, `minimax-m2.7`,
  `minimax-m3`, `mistral-large-3:675b`, `nemotron-3-nano:30b`, `nemotron-3-super`,
  `nemotron-3-ultra`, `qwen3.5:397b`. **All 11 names in the brief exist**; nine
  further models are offered and are not in `endpoints.json`.

### run-01 — the specified probe, `max_tokens 64`

| endpoint | path | status | returned_model | finish | ms | json | reasoning | usage p/c |
|---|---|---|---|---|---|---|---|---|
| `deepseek-flash` | openai-compat | INCOMPLETE_GENERATION | `deepseek-flash` | length | 1605 | no | yes | 71/64 |
| `deepseek-v4-pro` | openai-compat | INCOMPLETE_GENERATION | `deepseek-v4-pro` | length | 1926 | no | yes | 122/64 |
| `ollama/deepseek-v4.1-flash` | openai-compat | INCOMPLETE_GENERATION | `deepseek-v4.1-flash` | length | 2545 | no | yes | 49/64 |
| `ollama/deepseek-v4.1-flash.native` | native | INCOMPLETE_GENERATION | `deepseek-v4.1-flash` | length | 2036 | no | yes | 49/64 |
| `ollama/gemma4-31b` | openai-compat | COMPLETE | `gemma4:31b` | stop | 1205 | no | no | 31/20 |
| `ollama/glm-5.3` | openai-compat | INCOMPLETE_GENERATION | `glm-5.3` | length | 1217 | yes | yes | 30/64 |
| `ollama/glm-5.3-flash` | openai-compat | INCOMPLETE_GENERATION | `glm-5.3-flash` | length | 1441 | no | yes | 30/64 |
| `ollama/glm-5.3-flash.native` | native | INCOMPLETE_GENERATION | `glm-5.3-flash` | length | 2075 | no | yes | 30/64 |
| `ollama/glm-5.3.native` | native | INCOMPLETE_GENERATION | `glm-5.3` | length | 1170 | no | yes | 30/64 |
| `ollama/gpt-oss-120b` | openai-compat | INCOMPLETE_GENERATION | `gpt-oss:120b` | length | 1009 | no | yes | 85/64 |
| `ollama/gpt-oss-120b.native` | native | INCOMPLETE_GENERATION | `gpt-oss:120b` | length | 714 | no | yes | 85/64 |
| `ollama/gpt-oss-20b` | openai-compat | INCOMPLETE_GENERATION | `gpt-oss:20b` | length | 1586 | no | yes | 85/64 |
| `ollama/gpt-oss-20b.native` | native | INCOMPLETE_GENERATION | `gpt-oss:20b` | length | 1170 | no | yes | 85/64 |
| `ollama/kimi-k3` | openai-compat | INCOMPLETE_GENERATION | `kimi-k3` | length | 2508 | no | yes | 160/64 |
| `ollama/kimi-k3.native` | native | COMPLETE | `kimi-k3` | stop | 1425 | yes | yes | 160/63 |
| `ollama/minimax-m3` | openai-compat | COMPLETE | `minimax-m3` | stop | 2552 | yes | yes | 194/38 |
| `ollama/mistral-large-3-675b` | openai-compat | COMPLETE | `mistral-large-3:675b` | stop | 1665 | no | no | 22/24 |
| `ollama/nemotron-3-super` | openai-compat | INCOMPLETE_GENERATION | `nemotron-3-super` | length | 1993 | no | yes | 35/64 |
| `ollama/nemotron-3-super.native` | native | INCOMPLETE_GENERATION | `nemotron-3-super` | length | 7251 | no | yes | 35/64 |
| `ollama/qwen3.5-397b` | openai-compat | INCOMPLETE_GENERATION | `qwen3.5:397b` | length | 2267 | no | yes | 28/66 |
| `ollama/qwen3.5-397b.native` | native | INCOMPLETE_GENERATION | `qwen3.5:397b` | length | 1825 | no | yes | 28/66 |

Native rows appear only for the eight Ollama models whose OpenAI-compatible call
did not come back `COMPLETE`; that fallback is one call on a separately declared
path, never a second attempt at the same one.

### run-02 — a second declared ceiling, `max_tokens 512`, compatible path

| endpoint | path | status | returned_model | finish | ms | json | reasoning | usage p/c |
|---|---|---|---|---|---|---|---|---|
| `deepseek-flash` | openai-compat | COMPLETE | `deepseek-flash` | stop | 1787 | yes | yes | 71/69 |
| `deepseek-v4-pro` | openai-compat | COMPLETE | `deepseek-v4-pro` | stop | 4520 | yes | yes | 122/262 |
| `ollama/deepseek-v4.1-flash` | openai-compat | COMPLETE | `deepseek-v4.1-flash` | stop | 5776 | yes | yes | 49/404 |
| `ollama/gemma4-31b` | openai-compat | COMPLETE | `gemma4:31b` | stop | 1794 | no | no | 31/20 |
| `ollama/glm-5.3` | openai-compat | COMPLETE | `glm-5.3` | stop | 1834 | yes | yes | 30/184 |
| `ollama/glm-5.3-flash` | openai-compat | COMPLETE | `glm-5.3-flash` | stop | 1844 | yes | yes | 30/26 |
| `ollama/gpt-oss-120b` | openai-compat | COMPLETE | `gpt-oss:120b` | stop | 1208 | yes | yes | 85/101 |
| `ollama/gpt-oss-20b` | openai-compat | COMPLETE | `gpt-oss:20b` | stop | 2894 | yes | yes | 85/267 |
| `ollama/kimi-k3` | openai-compat | COMPLETE | `kimi-k3` | stop | 2216 | no | yes | 160/112 |
| `ollama/minimax-m3` | openai-compat | COMPLETE | `minimax-m3` | stop | 2337 | yes | yes | 194/52 |
| `ollama/mistral-large-3-675b` | openai-compat | COMPLETE | `mistral-large-3:675b` | stop | 1958 | no | no | 22/24 |
| `ollama/nemotron-3-super` | openai-compat | COMPLETE | `nemotron-3-super` | stop | 2944 | yes | yes | 35/69 |
| `ollama/qwen3.5-397b` | openai-compat | COMPLETE | `qwen3.5:397b` | stop | 3994 | yes | yes | 28/187 |

### run-03 — native `POST /api/chat`, `max_tokens 512`

| endpoint | path | status | returned_model | finish | ms | json | reasoning | usage p/c |
|---|---|---|---|---|---|---|---|---|
| `ollama/deepseek-v4.1-flash.native` | native | INCOMPLETE_GENERATION | `deepseek-v4.1-flash` | length | 8475 | no | yes | 49/512 |
| `ollama/gemma4-31b.native` | native | COMPLETE | `gemma4:31b` | stop | 1767 | no | no | 31/20 |
| `ollama/glm-5.3-flash.native` | native | COMPLETE | `glm-5.3-flash` | stop | 1236 | no | yes | 30/70 |
| `ollama/glm-5.3.native` | native | COMPLETE | `glm-5.3` | stop | 1681 | no | yes | 30/67 |
| `ollama/gpt-oss-120b.native` | native | COMPLETE | `gpt-oss:120b` | stop | 809 | yes | yes | 85/94 |
| `ollama/gpt-oss-20b.native` | native | COMPLETE | `gpt-oss:20b` | stop | 2349 | yes | yes | 85/153 |
| `ollama/kimi-k3.native` | native | COMPLETE | `kimi-k3` | stop | 2789 | yes | yes | 160/123 |
| `ollama/minimax-m3.native` | native | COMPLETE | `minimax-m3` | stop | 3198 | no | yes | 194/59 |
| `ollama/mistral-large-3-675b.native` | native | COMPLETE | `mistral-large-3:675b` | stop | 2690 | no | no | 22/24 |
| `ollama/nemotron-3-super.native` | native | COMPLETE | `nemotron-3-super` | stop | 6694 | yes | yes | 35/107 |
| `ollama/qwen3.5-397b.native` | native | COMPLETE | `qwen3.5:397b` | stop | 3529 | no | yes | 28/172 |

## Findings

1. **Both credentials are live and both Ollama chat paths work.** 52 live calls
   were made: 46 chat calls and 6 model-list calls. Across them there was not a
   single authentication, routing or transport failure — no `HTTP_401/403/404`,
   no `TRANSPORT_OR_RESPONSE_ERROR`. Status tally over all 52 records:
   `COMPLETE` 32, `INCOMPLETE_GENERATION` 19, `HTTP_307` 1 (finding 6). The Ollama
   OpenAI-compatible `/v1/chat/completions` path — flagged as unverified in the
   brief — **is verified live** for all 11 models, and the native `/api/chat`
   path works too. All 13 compatible-path endpoints returned `COMPLETE` at a
   512-token ceiling; 10 of 11 native endpoints did.
2. **The only failure class observed was `INCOMPLETE_GENERATION`, and it is a
   ceiling effect, not an endpoint fault.** Every one of these models except
   `gemma4:31b` and `mistral-large-3:675b` emits native reasoning by default,
   which counts against `max_tokens`; at 64 tokens 17 of 21 calls truncated.
   At 512 all but `deepseek-v4.1-flash.native` (which spent the whole 512 on
   reasoning) finished. An emergency ceiling is a resource boundary, not a
   statement about the model.
3. **JSON mode is accepted but not enforced on Ollama cloud.** Several models
   returned a fenced ```json block rather than a bare object despite
   `response_format {"type":"json_object"}` (compat) / `format: "json"`
   (native): `kimi-k3`, `gemma4:31b`, `mistral-large-3:675b` on the compatible
   path; `qwen3.5:397b`, `glm-5.3`, `glm-5.3-flash`, `gemma4:31b`,
   `mistral-large-3:675b` on the native path. `minimax-m3.native` returned
   syntactically invalid JSON (`{"ok": true, "model": MiniMax-M3}`). Anything
   built on these endpoints needs its own JSON extraction; the transport records
   the content verbatim and does not repair it.
4. **`returned_model` always equalled the requested model**, on both paths and
   both providers. Several models misreported their own *name* in the answer
   body (`gemma4:31b` and `mistral-large-3:675b` both said `gpt-4o`,
   `glm-5.3-flash` said `claude-sonnet-4-5`). Self-reported identity in content
   is not evidence of weights; the recorded `returned_model` and
   `system_fingerprint` (`fp_ollama` on the compat path) are the transport's
   only identity claims, and an alias is still not an immutable weight identity.
5. **A reported completion count can exceed the requested ceiling.**
   `qwen3.5:397b` reported `completion_tokens 66` against `max_tokens 64`, on
   both paths. The record keeps the reported usage as returned; this module's
   status set (as specified) has no ceiling-violation code, so it surfaces as
   `INCOMPLETE_GENERATION` with the usage visible in the record.
6. **The redirect refusal fired live.** An early run asked
   `https://ollama.com/models` (the native base has no `/models` surface) and
   got `HTTP_307` — `_NoRedirect` refused to follow it rather than replaying a
   credentialed request at a new location. The tool now asks only the
   OpenAI-compatible base for its model list; the refusal record remains in
   `run-03-native-512/models__ollama.com/` as evidence.
7. **Native reasoning text was never persisted.** 40 of the 46 chat calls had
   `reasoning_content_present: true`; every record carries
   `reasoning_content_persisted: false`, stores only the sha256 of the provider
   body, and no `reasoning`, `reasoning_content` or `thinking` field.

## Dependencies

**None beyond the standard library.** `provider_openai_compat.py` imports only
`hashlib`, `json`, `os`, `threading`, `time`, `urllib.error`, `urllib.request`,
`dataclasses`, `datetime`, `pathlib`, `typing`. `tools/provider_smoke.py` adds
`argparse` and `concurrent.futures`. No `pydantic`, no `jsonschema`, no
`requests`, no `httpx`. The Mini adapter imports
`creib.forge.mini.executor` (already a repository dependency, and therefore
pydantic transitively) **lazily inside `reply`**, so the transport itself
imports and runs without it. The offline suite uses `unittest` and `mock` only.
TLS goes through the preconfigured proxy with the preconfigured CA bundle;
verification was never disabled and no TLS setting is touched by this code.

## Scrub confirmation

A scanner loaded both keys into its own process (printing nothing) and searched
every real file — symlinks skipped — in the staging tree and in the smoke
records for the first 6 characters, the first 12 characters, and the full value
of each key.

```
files scanned (real files, symlinks skipped): 118
DEEPSEEK_API_KEY: first-6 chars -> 0 match(es), first-12 chars -> 0 match(es), first-35 chars -> 0 match(es)
OLLAMA_API_KEY:  first-6 chars -> 0 match(es), first-12 chars -> 0 match(es), first-57 chars -> 0 match(es)
```

**0 matches at every length.** No key value or fragment was printed, echoed,
logged, returned or written anywhere. `git status --porcelain` in
`/home/user/miniReason` is empty: the repository is untouched.

## Review closure (2026-09-14)

The four-lens review of this staging tree is answered in `FIXES.md`: every
finding of every severity, the change that closes it and the test that pins it.
Two things a reader of the tables above should carry forward:

* `THINKING_MODE_MISMATCH` is back (finding 2.2). `provider.py:169-170`'s check
  is the only evidence that a thinking control was honoured, and the smoke runs
  above were taken **without** it — `deepseek-flash` and `deepseek-v4-pro` both
  showing `reasoning yes` in run-01/run-02 is exactly the situation it now
  fails. `COMPLETION_CEILING_VIOLATED` is still absent, as finding 5 above says.
* `CompatMiniResponder` now defaults `thinking` to `False` for the `deepseek`
  family (finding 2.3), so a Mini manifest ported from `provider.MiniResponder`
  keeps its reasoning behaviour instead of silently inheriting the provider's.
  `tools/provider_smoke.py` still passes no thinking value, so the smoke tables
  above remain a faithful record of what the *tool* sends.
