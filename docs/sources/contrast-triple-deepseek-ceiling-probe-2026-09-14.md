> Published verbatim, body unedited: this document was written against the staging tree `scratchpad/contrast/occ02/`, so `probe/probe_ceiling.py`, `probe/records-32768/…`, `occ02/probe/` and “the staging tree” below name that scratchpad tree and not any path in this repository, where the script and the two records of the single probe call it reports are published unchanged at `experiments/diagnostics/C001-contrast-triple/probe-2026-09-14/probe_ceiling.py` and `experiments/diagnostics/C001-contrast-triple/probe-2026-09-14/records/deepseek-flash/ceiling-32768/call-0001.{request,response}.json`, and the files it otherwise describes are `tools/contrast_triple_study.py`, `tools/contrast_triple_study_v2.py`, `experiments/diagnostics/C001-contrast-triple/{PLAN.md,material.json,material-occurrence-02.json}` and `experiments/diagnostics/C001-contrast-triple/occurrence-01/`. It is carried under REC-20260914-V, which publishes C001 occurrence-02; this note is the only change made to it, and no figure, count or claim in the body below is edited.

# PROBE — what ceiling does `deepseek-flash` actually accept?

Staged 2026-09-14. Scratchpad only; nothing here is published.

## 1. Why the 8192 in occurrence-01 was there

Three candidate sources were checked and only one is real.

**Not the endpoint registry.** `src/minireason/data/endpoints.json` declares **no
`max_tokens` field at all** — for `deepseek-flash` or for any other row. Each row carries
only `name`, `base_url`, `model`, `key_env`, `family`, `chat_path`, `native`,
`max_concurrency` and `timeout_seconds` (180 on every row). The registry therefore imposes
no completion ceiling on anything.

**Not the transport.** `minireason.provider_openai_compat._RecordedCaller._validate_call_args`
admits `1 <= max_tokens <= 393216` and refuses anything else
(`provider_openai_compat.py:465`). 8192 appears there only as the *default* argument value
of `complete()` (`:839`, `:979`) and of `responder_for`'s settings (`:1053`) — a default
the driver never takes, because it always passes an explicit value.

**Not a driver default either, in effect.** `tools/contrast_triple_study.py:48` defines
`MAX_TOKENS_DEFAULT = 8192` with the comment *"the ceiling for an endpoint that sends no
reasoning"*, but the constant is dead: it is referenced nowhere else in the file. The
value that actually reached the wire came from the material.

**It was an explicit, recorded choice in the material and the register.** The number is
declared twice in `experiments/diagnostics/C001-contrast-triple/material.json` — in
`endpoints[0].max_tokens` and in `ceilings.max_tokens["deepseek-flash"]` — and `prepare`
refuses unless the two agree (`MATERIAL_ENDPOINT_MAX_TOKENS`). Its stated reason, in
`ceilings.max_tokens_policy` and again in PLAN.md §5 *The per-endpoint completion ceiling*:

> `deepseek-flash` keeps 8192: **it sends no reasoning on the wire**, and 8192 was ample
> for it.

Both halves of that reason are false of C001 as dispatched, and occurrence-01 is the
evidence:

* *"sends no reasoning on the wire"* — 29 of the 40 `deepseek-flash` receipts record
  `reasoning_content_present: true`, and every one that reports usage carries a
  `completion_tokens_details.reasoning_tokens` count. The probe below adds a 30th on a
  seven-word prompt (81 reasoning tokens for a 19-token answer). The other 11 report no
  usage at all because they returned nothing.
* *"8192 was ample for it"* — ample for the **prose** arm only. C001's briefs are far
  longer than the H005 briefs that reason was formed on, and the FCL-1 envelope is longer
  again than the prose one.

## 2. The finding, quantified from occurrence-01's own records

`experiments/diagnostics/C001-contrast-triple/occurrence-01`, endpoint `deepseek-flash`,
40 coordinates, all terminal:

| arm | COMPLETE | PARTIAL | FAILED | reasoning_tokens (min…max) | completion_tokens (min…max) |
|---|---|---|---|---|---|
| `fcl` | **1** | 8 | 11 | 5488 … 7890 (9 reporting) | 8083 … 8192 |
| `prose` | **20** | 0 | 0 | 2258 … 5416 | 3621 … 6985 |

Every one of the 8 PARTIALs is `finish_reason: "length"` at `completion_tokens` exactly
8192. Every one of the 11 FAILEDs is `failure_type: INCOMPLETE_GENERATION` with
`validation_failure_type: NO_PUBLIC_CONTENT`, `usage_status: UNKNOWN` and no
`finish_reason` — the ceiling consumed, nothing returned, no usage reported. The single
`fcl` COMPLETE (`carrier/rep1`) spent 5488 reasoning tokens and finished at 8083, i.e.
**109 tokens under the ceiling**. So 19 of 20 `fcl` nodes are unusable and the twentieth
survived by a hair, while the prose arm at the same ceiling is 20 of 20.

The whole `fcl` residue is the ceiling, not the transport: zero read timeouts, zero
`TRANSPORT_OR_RESPONSE_ERROR`, zero retries.

## 3. Evidence already in the repository about the true maximum — none above 8192

Every recorded `deepseek-flash` call in this repository was sent at 8192 or below:

* `experiments/diagnostics/F001-fork5-multifamily/occurrence-01/arms.json` — `max_tokens` **8192**.
* `experiments/diagnostics/C001-contrast-triple/occurrence-01/plan.json` — **8192**.
* `docs/sources/provider-openai-compat-smoke-notes-2026-09-14.md` — the published smoke
  runs probed `deepseek-flash` at **64** (`run-01`, truncated at 71/64) and at **512**
  (`run-02`, COMPLETE, 71/69). No higher ceiling was ever sent.
* `docs/workflows/provider-openai-compat.md` and `docs/PROVIDER.md` state the ceiling
  discipline but assert no provider-side maximum.

So the repository contains **no evidence of what `deepseek-flash` accepts above 8192**,
and the 32768 that the five Ollama endpoints carry was never tested on the DeepSeek base.
One probe was therefore run.

## 4. The probe — one call, 2026-09-14 08:34:23 UTC

Script: `probe/probe_ceiling.py`. It imports `tools/provider_smoke.py` and calls that
tool's own `load_env_file` and `probe`, so the call goes through the study's transport,
record discipline and credential redaction unchanged. Exactly **one** `complete()` was
sent: no `/models` call, no fallback path, no retry, no second attempt at the same
configuration. Prompt is `provider_smoke.PROMPT`, the trivial
`Reply with a JSON object {"ok": true, "model": <your model name>}`. Seed is not sent
(`supports_seed` is false for `family == "deepseek"`). Records:
`probe/records-32768/deepseek-flash/ceiling-32768/`.

```
python3 probe/probe_ceiling.py probe/records-32768 32768
```

**Result — 32768 was ACCEPTED. No error, no ceiling refusal, no second probe needed.**

| field | value |
|---|---|
| `max_tokens` sent | **32768** |
| `status` | **COMPLETE** |
| `finish_reason` | `stop` |
| `returned_model` | `deepseek-flash` |
| `elapsed_ms` | 1837 |
| `json_parsed` | true (42 content chars) |
| `usage.completion_tokens` | 100 |
| `usage.completion_tokens_details.reasoning_tokens` | **81** |
| `usage.prompt_tokens` | 71 |
| `reasoning_content_present` | **true** |
| `reasoning_content_persisted` | false |
| `request_sha256` | `6c7c1bd0c5df9a54c9f9a80cd5a2e85d39a566874aa8453c6abaa66693ce7680` |
| `provider_response_sha256` | `e83520468b59fcd1f900b904a3d5c209e94cb26acaf104640c7652537afb6472` |

The written request record confirms the ceiling reached the wire rather than being
clipped client-side: `request.max_tokens` **32768**, `settings.max_tokens` **32768**,
`url` `https://api.deepseek.com/v1/chat/completions`, `retries` 0, `seed` null,
`request_bytes` 225.

The probe also settles the "sends no reasoning on the wire" claim on its own:
`reasoning_content_present: true` and 81 of 100 completion tokens were reasoning tokens,
on a seven-word prompt.

Because 32768 was accepted, the fallback probe at 16384 was **not** run. One call was
spent in total.

**Credential safety.** Scanned every file under `occ02/probe/`: zero occurrences of the
`DEEPSEEK_API_KEY` value at full, 12-character or 6-character length, and zero `Bearer `
followed by a token. The request record stores `request_header_names`
(`Accept`, `Authorization`, `Content-Type`) and no header value. No key value or fragment
is printed by the script, and none appears in this document.

## 5. What the probe does and does not establish

It establishes one thing precisely: the DeepSeek chat endpoint **accepts** `max_tokens
32768` for `deepseek-flash` on the OpenAI-compatible path. The request record carries
32768, the request was not rejected with an invalid-parameter error, no ceiling-conflict
refusal was raised at either end, and a normal `stop` completion came back in 1.8 s.

It does **not** show that the endpoint will actually generate more than 8192 tokens: the
probe's answer was 100 tokens long, so nothing above 8192 was exercised. A provider that
silently clamps generation at some lower internal bound would look exactly like this
probe. What the probe removes is the one failure that would have stopped occurrence-02
before it started — an argument the endpoint refuses — and occurrence-02's own receipts
will report the completion counts actually delivered.

It does **not** establish the endpoint's true provider-side maximum. 32768 is the highest
value this study is authorised to send (`MAX_TOKENS_AUTHORISED = 32768`,
`ceilings.max_tokens_authorised_maximum`), so nothing above it was tried and nothing above
it may be planned without a separate authorisation. It does not establish that 32768 is
*sufficient* for the FCL-1 envelope beside this model's reasoning — that is exactly the
open question occurrence-02 is dispatched to answer, and a cell that hits even 32768 stays
PARTIAL or a refusal and is compared against nothing.

## 6. Wall-clock consequence, from occurrence-01's own timings

The probe is a trivial prompt and says nothing about long generations, but occurrence-01's
40 `deepseek-flash` provider records do. Their observed generation rate:

| set | n | tokens/s min | median | max |
|---|---|---|---|---|
| `fcl` only | 20 | 179.2 | 202.2 | 227.5 |
| all 40 | 40 | 152.6 | 190.9 | 227.5 |

At 8192 the `fcl` calls took **36.0 s … 45.7 s** wall clock (median 40.4 s). Extrapolated
at the *same observed rates*, a call that spends the whole 32768 ceiling takes
**144 s (fastest) … 183 s (`fcl` slowest) … 215 s (slowest of all 40)**. Two of those
three exceed the 180-second wall clock `deepseek-flash` carries in occurrence-01, so at
32768 the fixed 180 s becomes the binding constraint and a would-be delivery is converted
into a `TRANSPORT_OR_RESPONSE_ERROR` read timeout — the exact failure REC-20260914-T
recorded on `ollama/glm-5.3` and `ollama/kimi-k3` at the same ceiling. Occurrence-02
therefore carries **600 s**, which is the transport's own validation maximum
(`Endpoint.__post_init__` admits 1…600 and refuses 601), a bound reached rather than
invented, and the same value the five Ollama endpoints already carry.
