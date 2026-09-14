# C001 — one responder node, four cases, six endpoints

> **Root reads the content.** This study delivers four codings of one criticism to one
> node and publishes what came back. It computes parse outcomes, reference resolution,
> record ids, byte hashes and counts — and **nothing else**. It marks no comparison, fills
> no reading column, and produces no score, rank or merit field anywhere: the driver
> refuses to write one (`SCORING_KEY_FORBIDDEN`). "Differs against control, not under
> recoding, not under carrier disturbance" is a pattern **root** reads off the published
> juxtapositions.

Read [the decision ledger](../DECISION_LEDGER.md), [STATUS](../STATUS.md), the
[experiment workflow](experiment.md) and the register itself —
[`experiments/diagnostics/C001-contrast-triple/PLAN.md`](../../experiments/diagnostics/C001-contrast-triple/PLAN.md)
— before running anything. Where this page is silent, the register governs.

## What C001 is

One node: the fork5 `response` node, its instruction and its `account`/`rival` inputs
frozen verbatim from H005's material and `H005-open-prose-commitments/occurrence-01`.
**Only the `objection` projection block varies**, across four cases — ORIGINAL (the
occurrence's own bytes), RECODING (a content-preserving rewrite authored offline, every
unit published in [`RECODING_TABLE.md`](../../experiments/diagnostics/C001-contrast-triple/RECODING_TABLE.md)),
CARRIER (same content, disturbed serialisation and layout), CONTROL (no objection at all).

**240 calls** = 4 cases × 5 replicates × 6 endpoints × 2 arms (FCL-1 and prose), in **47
deterministic waves**, each holding **at most five coordinates per credential**. Forty-six
are single-key and hold five; the one wave straddling the `deepseek-flash` / Ollama
boundary holds ten, five on each credential — inside the five-per-credential
authorisation, not an exception to it.

That one-varying-block guarantee is mechanical, not asserted: `prepare` computes the
shared prefix and suffix around the block per arm and refuses the plan unless all four
briefs equal `prefix + <this case's block> + suffix` (`SHARED_ENVELOPE_MISMATCH`), and
refuses unless the ORIGINAL case's bytes are the occurrence's own
(`ORIGINAL_CASE_NOT_THE_OCCURRENCE_BYTES`). Both hashes are frozen in `plan.json` and
copied into every request record, and `audit` re-checks them.

## The command sequence

`S=experiments/diagnostics/C001-contrast-triple`, and every command runs with
`PYTHONPATH=src python -X utf8 tools/contrast_triple_study.py`.

```
... prepare --material $S/material.json --output $S/occurrence-01   # 240 planned, 0 calls
#   -> commit and push plan.json + preflight.json, and verify the remote, BEFORE dispatch
... run     --output $S/occurrence-01 --plan-id <id>                 # 47 waves, <=5 per key
... run     --output $S/occurrence-01 --plan-id <id> --resume        # after an interruption
... audit   --output $S/occurrence-01
... table   --output $S/occurrence-01
```

**Publication before dispatch is the point, not a formality.** The correspondence table
is a claim about what the recoding preserves, and a claim published after the replies
exist is not a pre-registration. `material.json`, `PLAN.md`, `RECODING_TABLE.md`,
`plan.json` and `preflight.json` are pushed and the remote verified **before the first
call**.

## Per-endpoint ceilings and timeouts

Both are declared **per endpoint**, frozen twice (in `endpoints[]` and in `ceilings`),
carried into `plan.json`, and written into every request record and receipt.

| endpoint | credential | `max_tokens` | `timeout_seconds` |
|---|---|---|---|
| `deepseek-flash` | `DEEPSEEK_API_KEY` | 8192 | 180 |
| the five `ollama/*` endpoints | `OLLAMA_API_KEY` | 32768 | 600 |

The ceiling is raised on F001's evidence under REC-20260914-S (five nodes at 8192 whose
whole ceiling went to reasoning, returning no content). The timeout is raised on F001's
evidence under REC-20260914-T, where **both** failures of a 20-call run at 32768 were the
fixed 180-second read timeout — `TRANSPORT_OR_RESPONSE_ERROR`, "The read operation timed
out", at 180368 ms on `ollama/glm-5.3` and 180456 ms on `ollama/kimi-k3` — and
`finish_reason: "length"` occurred zero times. 600 is the transport's own validation
maximum, not a number this study chose.

**`src/minireason/data/endpoints.json` is never edited.** It is pinned by this material
*and* by the F001 plans; rewriting it would invalidate theirs. The declared timeout is
applied instead to the resolved `Endpoint` **value** by `dataclasses.replace` at provider
construction, and every disagreement between the plan, the material, the call spec, the
written record and the transport's own settings view is one refusal,
**`TIMEOUT_NOT_APPLIED`**.

Neither raise manipulates reasoning: `temperature`, `thinking` and `reasoning_effort` are
never sent, and a timeout is a socket deadline, not a payload field — the request bytes
are identical at either value. **Neither rescues a cell.** A PARTIAL at the raised
ceiling, or a refusal at the raised timeout, is read exactly as it would have been at the
old one.

## Custody

`run` writes an attempt marker **before** the send, then the raw reply bytes, then the
receipt; every record is opened `x`, write-once, and a coordinate with an existing
request, attempt or response refuses with `NO_REPLAY`. `--resume` skips a coordinate that
already has a receipt and **still refuses** one with a request or attempt and no receipt:
that call may have reached the provider and been billed, and it is never silently
re-sent. `retries` is 0 everywhere.

`audit` goes beyond internal consistency. It ties each request back to the frozen plan —
`messages_sha256`, `brief_sha256`, `objection_projection_sha256`, the arm's shared
prefix/suffix hashes, the `plan_id`, and the declared timeout — and **re-derives** each
artifact's content digests from the delivered bytes. The two custody checks that matter
are **`REQUEST_NOT_FROM_PLAN`** and **`ARTIFACT_NOT_DERIVED_FROM_DELIVERY`**: without
them a record set can be perfectly self-consistent about a brief that was never planned,
or carry an artifact body no model ever returned.

At most **five concurrent requests per credential**, held twice — by the transport's
process-wide per-key semaphore and by the driver's own `KeyGate`. Keys are read from the
environment at call time only; `write_new` refuses any record containing one.

## What `table` produces, and what root does with it

* `COMPARISON.md` and `comparison.json` — the mechanical columns (FCL-1 parse outcome,
  records by type, record ids, targets named, prefix-resolved references in four separate
  columns, bare-token occurrences, `uptake`, byte hashes and lengths; for the prose arm,
  **hashes and lengths only** — there is no parse to perform and this study invents none).
* `juxtaposition/<endpoint>__<arm>.md` — all twenty delivered texts of a cell, as
  delivered, nothing computed over them. A delivery the decoder refused is printed too,
  under a heading naming the refusal code.
* Root's six columns and the four-register mark grid are rendered **empty** and stay
  empty. Root reads the juxtapositions and fills them; no agent fills them and no agent
  proposes a reading in them.

The four registers — **T** target named, **E** objection record engaged (prefix-resolved),
**D** proposed action, **G** grounds cited — are pre-declared in PLAN §8a and mirrored
into `material.json.reading_rule`, so they are inside the frozen identity. They are marked
`differs` / `same` / `unresolved` separately and are **never** summed, averaged, weighted
or reduced to one mark.

## Design record

* Register and pre-registration: [`PLAN.md`](../../experiments/diagnostics/C001-contrast-triple/PLAN.md)
* Design notes and open questions: [`NOTES.md`](../../experiments/diagnostics/C001-contrast-triple/NOTES.md)
* The 85-row correspondence table: [`RECODING_TABLE.md`](../../experiments/diagnostics/C001-contrast-triple/RECODING_TABLE.md)
* Material provenance scripts: `experiments/diagnostics/C001-contrast-triple/build/`
* Adversarial review closure: [`docs/sources/contrast-triple-review-fixes.md`](../sources/contrast-triple-review-fixes.md)
* Transport: [provider-openai-compat](provider-openai-compat.md)
* The evidence the two raises rest on: [fork5-multifamily](fork5-multifamily.md)
* Suite: `PYTHONPATH=src python -X utf8 -m unittest tests.test_contrast_triple_study`
