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

## Occurrence-02: the successor driver v2, one cell at a raised ceiling

*Appended 2026-09-14 under REC-20260914-V. Same workflow, same page, no new row in
[`README.md`](README.md): occurrence-02 is C001 run again on one cell, not a second
study.*

`tools/contrast_triple_study_v2.py` is a **byte copy** of `tools/contrast_triple_study.py`
at `f5f9dfca…` with **eight differences, each marked `# V2:` in the source** and listed in
the file's own header: the docstring; `PARTIAL_UNRESOLVED` becoming
`partial_unresolved(ceiling)` over a template, because a constant naming 8192 is false on a
32768 PARTIAL; its one call site in `decode_contribution`; an **optional**
`dispatch_scope` block validated by `validate_material`; the three readers
`scoped_endpoints`, `scoped_arms` and `planned_call_count`; `all_coordinates` building over
the scope in the same iteration order; `plan_body` taking the scoped count and freezing the
scope into the plan; and `_offline_preflight` checking against the plan's own
`planned_calls`. The suite proves rather than asserts it: `V2DiffProof` normalises the
docstring away, diffs v2 against v1 and refuses any hunk not marked `# V2:`, and `V1Parity`
shows that on occurrence-01's own published material **v2's plan body differs from v1's in
exactly one field, `helper_sha256`** — which is precisely why the identity has to be a
successor, since `plan_body` folds the driver's own sha256 into every `plan_id` it mints.

**Why a fork and not a flag.** v1 cannot express this occurrence: `ENDPOINT_COUNT = 6`,
`sorted(material['arms']) != sorted(ARMS)` and the module constant `PLANNED_CALLS = 240`
each refuse a one-endpoint, one-arm, twenty-call plan; and editing v1 would change
`helper_sha256`, hence occurrence-01's published `plan_id` `328b9452…`, hence every later
`verify`, `audit` and `table` that re-derives it from those bytes. **The hazard the fork
exists for**: v1 does *not* refuse the occurrence-02 material, it silently widens it — with
no notion of `dispatch_scope` and no reading of the material's own `planned_calls`, v1
plans the full 240 coordinates at 32768, twelve times the authorisation. A test pins that,
and it is why the mandatory pre-dispatch check is `planned_calls == 20` read off a plan
built by **v2**.

The command sequence is the same as above with the v2 file and the occurrence-02 material,
`S=experiments/diagnostics/C001-contrast-triple`:

```
PYTHONPATH=src python3 -X utf8 tools/contrast_triple_study_v2.py prepare \
    --material $S/material-occurrence-02.json --output $S/occurrence-02
#   {"plan_id": "1d9f47ac…", "planned_calls": 20, "provider_calls": 0}
PYTHONPATH=src python3 -X utf8 tools/contrast_triple_study_v2.py verify  --output $S/occurrence-02
#   -> commit and push plan.json + preflight.json + the eight briefs, and verify the
#      remote, BEFORE dispatch
PYTHONPATH=src python3 -X utf8 tools/contrast_triple_study_v2.py run \
    --output $S/occurrence-02 --plan-id 1d9f47acdc692146792e354afdd9c6944036cb7d55bd83cc32c905e7c4ffeb83
PYTHONPATH=src python3 -X utf8 tools/contrast_triple_study_v2.py audit --output $S/occurrence-02
PYTHONPATH=src python3 -X utf8 tools/contrast_triple_study_v2.py table --output $S/occurrence-02
```

**Scope narrows dispatch, never the freeze.** All eight briefs are still written and
hashed into `plan_id`, both arms are still checked, and `occurrence-02/RECODING_TABLE.md`
still renders all 85 units byte-identically to the published
`dcaebaf8336c1943700a762b4836679307349d6ff8dfad082e4cd77e23fd7ae7`. **The prose arm of
occurrence-02 is therefore frozen and published but never dispatched** — four
`briefs/prose/*.json` files exist and no call is ever made against them — which is
deliberate, because the pre-registration is a claim about the whole correspondence table.
`table` renders **one** juxtaposition, `juxtaposition/deepseek-flash__fcl.md`, not twelve,
with root's six columns and the four-register mark grid rendered empty and left empty.

**The correction occurrence-02 carries, stated as a correction and not as an edit.**
Occurrence-01 gave `deepseek-flash` a ceiling of 8192 on the recorded ground that it
"sends no reasoning on the wire, and 8192 was ample for it"; **both halves are false of
C001 as dispatched** — 29 of that endpoint's 40 receipts record
`reasoning_content_present: true`, and 19 of its 20 `fcl` coordinates were consumed by the
ceiling while the prose arm at the same ceiling was 20 of 20. The published text is left
standing because it is the pre-registration a completed occurrence ran under; **no
occurrence-01 record is modified, relabelled, repaired, re-sent or superseded**, and
occurrence-02 is a second ceiling published beside the first, which is the rule
[`docs/lessons/operations.md`](../lessons/operations.md) already records from E001/E002:
"new budget conditions require separate freezing rather than retrospective repair".

* Occurrence-02 register: [`PLAN.md` §15](../../experiments/diagnostics/C001-contrast-triple/PLAN.md)
* The one ceiling-acceptance probe: [`docs/sources/contrast-triple-deepseek-ceiling-probe-2026-09-14.md`](../sources/contrast-triple-deepseek-ceiling-probe-2026-09-14.md)
* Suite: `PYTHONPATH=src python -X utf8 -m unittest tests.test_contrast_triple_study_v2`
