# F001-fork5-multifamily — classification of unresolved coordinates

Computed by `check/f001_classify.py` (run: `python3 check/f001_classify.py`)
from the records under `experiments/diagnostics/F001-fork5-multifamily/`.
Every value below traces to a named record; the same command prints its
integrity cross-checks and totals to stdout.

This is a classification, not a comparison. A completion-token ceiling,
a wall clock and the no-retry truncation rule are resource boundaries;
none of them is exhaustion of the inquiry, and none of them says
anything about how any family reasons. No ordering of endpoints, no
reliability claim and no failure rate is made or implied by these rows.
Endpoints and occurrences are independent occasions.

## Planned coordinate set (derived)

Derivation. Each occurrence's `plan.json` freezes the scope
`{"problems": ["daily"], "cycles": [1]}`. For every arm in its
`arms.json`: an arm of `kind: "mini"` is planned once per model-called
node of the fork5 template; `kind: "bare"` and `kind: "native"` are
single calls (node `answer`). The model-called node sequence is taken
from `manifests/fork5.json` as the stages that carry no machine `seat`
and are not the `end` marker: `account`, `objection`, `rival`, `response`, `carry`. The same sequence is confirmed by the receipts themselves (every
mini-arm receipt node is one of these five). A planned coordinate with
no receipt at `responses/daily/<arm>/cycle01/<node>.json` was never
dispatched.

| Occurrence | Runner (sha256 prefix) | Arms | Coordinates per arm | Planned | `plan.max_calls` | Receipts present | No receipt |
|---|---|---|---|---|---|---|---|
| occurrence-01 | a56fed41 | 4 | bare ×1, mini_fcl ×5, mini_prose ×5, native ×1 | 12 | 12 | 12 | 0 |
| occurrence-02 | a56fed41 | 3 | bare ×1, mini_fcl ×5, mini_prose ×5 | 11 | 11 | 11 | 0 |
| occurrence-03 | a56fed41 | 3 | bare ×1, mini_fcl ×5, mini_prose ×5 | 11 | 11 | 11 | 0 |
| occurrence-04 | a56fed41 | 3 | bare ×1, mini_fcl ×5, mini_prose ×5 | 11 | 11 | 8 | 3 |
| occurrence-05 | a56fed41 | 3 | bare ×1, mini_fcl ×5, mini_prose ×5 | 11 | 11 | 10 | 1 |
| occurrence-06 | a56fed41 | 3 | bare ×1, mini_fcl ×5, mini_prose ×5 | 11 | 11 | 11 | 0 |
| occurrence-07 | 8f7eb9d7 | 3 | bare ×1, mini_fcl ×5, mini_prose ×5 | 11 | 11 | 9 | 2 |
| occurrence-08 | 8f7eb9d7 | 3 | bare ×1, mini_fcl ×5, mini_prose ×5 | 11 | 11 | 11 | 0 |
| **total** |  |  |  | **89** | **89** | **83** | **6** |

Total planned coordinates: **89** = 12 (occurrence-01: `bare`, `native`,
plus two 5-node mini arms) + 7 × 11 (occurrences 02–08: `bare` plus two
5-node mini arms) — the script asserts each equals the frozen
`plan.max_calls` of its occurrence. This agrees with the register's own
arithmetic in `PLAN.md`: 67 for occurrences 01–06 under runner v1
(sha256 prefix `a56fed41`, arm ceiling 8,192) plus 22 for occurrences
07–08 under runner v2 (`8f7eb9d7`, arm ceiling 32,768). A coordinate's
declared ceiling and timeout below are the arm's `max_tokens` and
`timeout_seconds` from its occurrence's `plan.json` ceilings; the
timeout is 180 s on every arm of every occurrence.

## The three classes and their evidence

* `ceiling` — the call met its declared completion-token ceiling:
  `finish_reason` is `length` at exactly the arm's `max_tokens`. A
  partial delivery still counts as `ceiling` if that is what ended it.
* `timeout` — the call was refused by the wall clock: a transport
  failure whose error is a read timeout, at an elapsed time at the
  declared `timeout_seconds` (180 s on every arm here).
* `blocked` — the coordinate was never dispatched: the no-retry
  truncation rule ended its arm at an earlier node. There is no receipt
  at all.

A coordinate whose record does not settle one of these is left
unclassified, with the gap stated — it is not guessed.

## Unresolved coordinates — one row per coordinate not in state `ok`

`ok` is read as receipt status `COMPLETE`. Unresolved therefore means:
a receipt with status `PARTIAL` or `FAILED`, or a planned coordinate
with no receipt. Receipts found in this copy: 83 (COMPLETE 74, FAILED 7, PARTIAL 2). Unresolved: **15**.

Every populated cell is taken from the record named. `no receipt` /
`no record` / `not recorded` means the field does not exist in this
copy of the study; nothing is inferred into it. `null` is the receipt's
own JSON null, quoted literally. Receipts carry no elapsed-time field
and no content-byte count; the seven `ceiling` rows' content bytes are
quoted from the published raw-`responses/*.txt` table in the register's
appendix (`PLAN.md`, "Why: what occurrence-04 and occurrence-05
actually recorded"), the only record of those bytes in this copy, and
each such cell says so.

| occurrence | endpoint | ceiling (max_tokens) | arm | cycle | node | class | status | failure_code | finish_reason | completion tokens | content bytes | elapsed ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| occurrence-04 | ollama/glm-5.3 | 8192 | mini_fcl | 1 | objection | ceiling | FAILED | INCOMPLETE_GENERATION | length | 8192 | 0 (per PLAN.md table, raw `responses/*.txt` column) | not recorded (no record in this copy carries one) |
| occurrence-04 | ollama/glm-5.3 | 8192 | mini_fcl | 1 | rival | ceiling | FAILED | INCOMPLETE_GENERATION | length | 8192 | 0 (per PLAN.md table, raw `responses/*.txt` column) | not recorded (no record in this copy carries one) |
| occurrence-04 | ollama/glm-5.3 | 8192 | mini_fcl | 1 | response | blocked | no receipt | no record | no record | no record | no record | not recorded (no record in this copy carries one) |
| occurrence-04 | ollama/glm-5.3 | 8192 | mini_fcl | 1 | carry | blocked | no receipt | no record | no record | no record | no record | not recorded (no record in this copy carries one) |
| occurrence-04 | ollama/glm-5.3 | 8192 | mini_prose | 1 | objection | ceiling | PARTIAL | INCOMPLETE_GENERATION | length | 8192 | 288 (per PLAN.md table, raw `responses/*.txt` column) | not recorded (no record in this copy carries one) |
| occurrence-04 | ollama/glm-5.3 | 8192 | mini_prose | 1 | response | ceiling | FAILED | INCOMPLETE_GENERATION | length | 8192 | 0 (per PLAN.md table, raw `responses/*.txt` column) | not recorded (no record in this copy carries one) |
| occurrence-04 | ollama/glm-5.3 | 8192 | mini_prose | 1 | carry | blocked | no receipt | no record | no record | no record | no record | not recorded (no record in this copy carries one) |
| occurrence-05 | ollama/kimi-k3 | 8192 | mini_fcl | 1 | rival | ceiling | PARTIAL | INCOMPLETE_GENERATION | length | 8192 | 7112 (per PLAN.md table, raw `responses/*.txt` column) | not recorded (no record in this copy carries one) |
| occurrence-05 | ollama/kimi-k3 | 8192 | mini_fcl | 1 | response | ceiling | FAILED | INCOMPLETE_GENERATION | length | 8192 | 0 (per PLAN.md table, raw `responses/*.txt` column) | not recorded (no record in this copy carries one) |
| occurrence-05 | ollama/kimi-k3 | 8192 | mini_fcl | 1 | carry | blocked | no receipt | no record | no record | no record | no record | not recorded (no record in this copy carries one) |
| occurrence-05 | ollama/kimi-k3 | 8192 | mini_prose | 1 | carry | ceiling | FAILED | INCOMPLETE_GENERATION | length | 8192 | 0 (per PLAN.md table, raw `responses/*.txt` column) | not recorded (no record in this copy carries one) |
| occurrence-07 | ollama/glm-5.3 | 32768 | mini_fcl | 1 | objection | unclassified | FAILED | TRANSPORT_OR_RESPONSE_ERROR | null | null (usage is null) | not recorded (the receipt schema carries no such field) | not recorded (no record in this copy carries one) |
| occurrence-07 | ollama/glm-5.3 | 32768 | mini_fcl | 1 | response | blocked | no receipt | no record | no record | no record | no record | not recorded (no record in this copy carries one) |
| occurrence-07 | ollama/glm-5.3 | 32768 | mini_fcl | 1 | carry | blocked | no receipt | no record | no record | no record | no record | not recorded (no record in this copy carries one) |
| occurrence-08 | ollama/kimi-k3 | 32768 | mini_fcl | 1 | carry | unclassified | FAILED | TRANSPORT_OR_RESPONSE_ERROR | null | null (usage is null) | not recorded (the receipt schema carries no such field) | not recorded (no record in this copy carries one) |

Receipt paths: `responses/daily/<arm>/cycle01/<node>.json` under the
row's occurrence directory. The two `PARTIAL` rows carry
`envelope_status: OPAQUE`; per the register, a partial delivery is
preserved, usable, never retried and never relabelled.

## `blocked` coordinates: the earlier FAILED node that ended the arm

The truncation rule is declared in the register (`PLAN.md`, "Resource
boundary and dispatch discipline"): one FAILED node ends that arm for
the rest of the occurrence, and every node's failure policy in
`manifests/fork5.json` is `action: stop, retries: 0, tolerance: 0`.
Each blocked coordinate below has no receipt, and an earlier node of
the same arm carries a FAILED receipt. Round-mates in one wave are
dispatched together (PLAN.md's measured cadence puts `objection` and
`rival` of both mini arms in one round, `response` and `carry` in
later rounds), which is why an arm can hold more than one FAILED
receipt — e.g. occurrence-04 `mini_fcl` objection and rival.

| occurrence | blocked coordinate | arm | earliest earlier FAILED node | its receipt | that receipt's failure_code / finish_reason | its class above |
|---|---|---|---|---|---|---|
| occurrence-04 | mini_fcl/cycle01/response | mini_fcl | objection | responses/daily/mini_fcl/cycle01/objection.json | INCOMPLETE_GENERATION / length | ceiling |
| occurrence-04 | mini_fcl/cycle01/carry | mini_fcl | objection | responses/daily/mini_fcl/cycle01/objection.json | INCOMPLETE_GENERATION / length | ceiling |
| occurrence-04 | mini_prose/cycle01/carry | mini_prose | response | responses/daily/mini_prose/cycle01/response.json | INCOMPLETE_GENERATION / length | ceiling |
| occurrence-05 | mini_fcl/cycle01/carry | mini_fcl | response | responses/daily/mini_fcl/cycle01/response.json | INCOMPLETE_GENERATION / length | ceiling |
| occurrence-07 | mini_fcl/cycle01/response | mini_fcl | objection | responses/daily/mini_fcl/cycle01/objection.json | TRANSPORT_OR_RESPONSE_ERROR / null | unclassified |
| occurrence-07 | mini_fcl/cycle01/carry | mini_fcl | objection | responses/daily/mini_fcl/cycle01/objection.json | TRANSPORT_OR_RESPONSE_ERROR / null | unclassified |

On occurrence-07 the ending node is itself unclassified (see below):
the truncation evidence there is a FAILED receipt with
`failure_code: TRANSPORT_OR_RESPONSE_ERROR`, not a ceiling hit. The
`blocked` class does not depend on *why* the earlier node failed — only
on the recorded FAILED terminal and the declared no-retry rule.

## Coordinates left unclassified — the evidence gap, stated

These do not meet `ceiling` (their `finish_reason` is null and
`usage` is null) and the record in this copy does not settle
`timeout`. They are reported unresolved, not guessed:

* `occurrence-07` `daily/mini_fcl/cycle01/objection` (endpoint `ollama/glm-5.3`, ceiling 32768,
  timeout 180 s): FAILED with failure_type=ProviderFailure, failure_code=TRANSPORT_OR_RESPONSE_ERROR, finish_reason=null, usage=null. `ceiling` is excluded: finish_reason is null and usage is null (nothing shows the declared ceiling of 32768 was met). `timeout` is not settled: the class requires an error that is a read timeout at an elapsed time of 180 s, and the receipt carries neither an error text nor an elapsed time (the key union over all receipts has no such field). Left unclassified rather than guessed.
* `occurrence-08` `daily/mini_fcl/cycle01/carry` (endpoint `ollama/kimi-k3`, ceiling 32768,
  timeout 180 s): FAILED with failure_type=ProviderFailure, failure_code=TRANSPORT_OR_RESPONSE_ERROR, finish_reason=null, usage=null. `ceiling` is excluded: finish_reason is null and usage is null (nothing shows the declared ceiling of 32768 was met). `timeout` is not settled: the class requires an error that is a read timeout at an elapsed time of 180 s, and the receipt carries neither an error text nor an elapsed time (the key union over all receipts has no such field). Left unclassified rather than guessed.

What would settle them is a record carrying the error text and the
elapsed time — e.g. the provider call record or the attempt log.
Those records are not part of this copy of the study (only the
receipts, arms, plans and manifest are), so the class stays
unresolved. The `timeout` class total is zero not because the clock
was shown to be uninvolved, but because the evidence that would
establish either verdict is not in the records at hand.

## Totals

Counts and their provenance: every table above is emitted by
`python3 check/f001_classify.py` from the receipt files, the plans and
the manifest; the same run asserts the cross-checks (planned = receipts
+ receipt-less; every ceiling row sits exactly at its arm's declared
ceiling; every `finish_reason: length` receipt in the study is a
ceiling row — 7 of 7).

### By class

| class | total | occurrences |
|---|---|---|
| ceiling | 7 | occurrence-04: 4, occurrence-05: 3 |
| blocked | 6 | occurrence-04: 3, occurrence-05: 1, occurrence-07: 2 |
| timeout | 0 | — (no coordinate's record settles this class) |
| unclassified | 2 | occurrence-07: 1, occurrence-08: 1 |
| **unresolved total** | **15** |  |

### By occurrence

| occurrence | endpoint | arm ceiling | ceiling | timeout | blocked | unclassified | unresolved |
|---|---|---|---|---|---|---|---|
| occurrence-01 | deepseek-flash | 8192 | 0 | 0 | 0 | 0 | 0 |
| occurrence-02 | ollama/gpt-oss-120b | 8192 | 0 | 0 | 0 | 0 | 0 |
| occurrence-03 | ollama/qwen3.5-397b | 8192 | 0 | 0 | 0 | 0 | 0 |
| occurrence-04 | ollama/glm-5.3 | 8192 | 4 | 0 | 3 | 0 | 7 |
| occurrence-05 | ollama/kimi-k3 | 8192 | 3 | 0 | 1 | 0 | 4 |
| occurrence-06 | ollama/gemma4-31b | 8192 | 0 | 0 | 0 | 0 | 0 |
| occurrence-07 | ollama/glm-5.3 | 32768 | 0 | 0 | 2 | 1 | 3 |
| occurrence-08 | ollama/kimi-k3 | 32768 | 0 | 0 | 0 | 1 | 1 |

### By endpoint

Occurrences 04/07 and 05/08 share an endpoint each but run under
different resource conditions (arm ceilings 8,192 then 32,768; runner v1
then v2 — `PLAN.md`, successor section). They are kept on separate lines
so that no resource condition is conflated; no endpoint is totalled
across conditions, and none are ordered.

| endpoint | occurrence (arm ceiling) | ceiling | timeout | blocked | unclassified | unresolved |
|---|---|---|---|---|---|---|
| deepseek-flash | occurrence-01 (8192) | 0 | 0 | 0 | 0 | 0 |
| ollama/gpt-oss-120b | occurrence-02 (8192) | 0 | 0 | 0 | 0 | 0 |
| ollama/qwen3.5-397b | occurrence-03 (8192) | 0 | 0 | 0 | 0 | 0 |
| ollama/glm-5.3 | occurrence-04 (8192) | 4 | 0 | 3 | 0 | 7 |
| ollama/kimi-k3 | occurrence-05 (8192) | 3 | 0 | 1 | 0 | 4 |
| ollama/gemma4-31b | occurrence-06 (8192) | 0 | 0 | 0 | 0 | 0 |
| ollama/glm-5.3 | occurrence-07 (32768) | 0 | 0 | 2 | 1 | 3 |
| ollama/kimi-k3 | occurrence-08 (32768) | 0 | 0 | 0 | 1 | 1 |

## What this table is not

These rows classify how each unresolved coordinate ended against the
declared boundaries — a completion-token ceiling, a wall clock, or the
no-retry truncation rule. They are resource-boundary facts. Nothing
here ranks endpoints or families, calls any of them less reliable,
measures anyone's reasoning, or treats a boundary as exhaustion of the
inquiry. No failure rate is computed; a count is information, not a
warrant.
