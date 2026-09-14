# F002 prospective study: the F001 cells the wall clock, not the ceiling, refused

Draft pre-registration, staged and **not run**. This is a **successor
pre-registration with its own identity**, not an amendment of F001. F001's
register (`experiments/diagnostics/F001-fork5-multifamily/PLAN.md`) is not
edited by one word, none of its eight occurrences is re-sent, relabelled,
repaired or superseded, and F002 writes nothing whatsoever inside
`F001-fork5-multifamily/`.

Participant material is [material.json](material.json): F001's material
(sha256 `8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff`,
itself the owner's H005 material verbatim plus one `study_id` key) with that one
key's **value** changed and nothing else, built by
[`build/build_f002_material.py`](build/build_f002_material.py) and
re-checkable with `--check`. A separate file exists only because the runner
refuses a material whose `study_id` is neither null nor the study directory's
own name (`STUDY_ID_MISMATCH`).

The runner is `tools/multicycle_commitment_study_multi_v3.py`, a successor
driver identity whose one behavioural difference from the published v2 is a
**per-arm wall clock**. This register follows H005's
[PROTOCOL.md](../H005-open-prose-commitments/PROTOCOL.md); where this file and
F001's are silent, that protocol governs.

## Motive — what F001's own records show

F001 planned 89 coordinates across eight occurrences. 74 are COMPLETE. The
residue is 15, and it falls into exactly three classes, read from the published
receipts (`responses/<problem>/<arm>/cycle01/<node>.json`, schema
`minireason.h005.receipt.v1`: `status`, `failure_code`, `finish_reason`,
`usage.completion_tokens`, `envelope_status`, `reasoning_content_present`), the
provider records (`provider/.../call-0001.response.json`, schema
`minireason.call.v2`: `status`, `content`, `elapsed_ms`, `error`,
`settings.timeout_seconds`, `request.max_tokens`), and the **absence** of an
`attempts/.../<node>.json` marker, which is how the no-retry truncation rule
records a coordinate it removed from the queue.

| occ | endpoint | ceiling | arm | cycle | node | class | `status` | `failure_code` | `finish_reason` | `completion_tokens` | content bytes | `elapsed_ms` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 04 | `ollama/glm-5.3` | 8192 | `mini_fcl` | 1 | objection | ceiling | FAILED | INCOMPLETE_GENERATION | length | 8192 | 0 | 94,230 |
| 04 | `ollama/glm-5.3` | 8192 | `mini_fcl` | 1 | rival | ceiling | FAILED | INCOMPLETE_GENERATION | length | 8192 | 0 | 96,915 |
| 04 | `ollama/glm-5.3` | 8192 | `mini_fcl` | 1 | response | blocked | — (no attempt) | — | — | — | — | — |
| 04 | `ollama/glm-5.3` | 8192 | `mini_fcl` | 1 | carry | blocked | — (no attempt) | — | — | — | — | — |
| 04 | `ollama/glm-5.3` | 8192 | `mini_prose` | 1 | objection | ceiling | PARTIAL | INCOMPLETE_GENERATION | length | 8192 | 288 | 100,226 |
| 04 | `ollama/glm-5.3` | 8192 | `mini_prose` | 1 | response | ceiling | FAILED | INCOMPLETE_GENERATION | length | 8192 | 0 | 98,020 |
| 04 | `ollama/glm-5.3` | 8192 | `mini_prose` | 1 | carry | blocked | — (no attempt) | — | — | — | — | — |
| 05 | `ollama/kimi-k3` | 8192 | `mini_fcl` | 1 | rival | ceiling | PARTIAL | INCOMPLETE_GENERATION | length | 8192 | 7,080 | 118,578 |
| 05 | `ollama/kimi-k3` | 8192 | `mini_fcl` | 1 | response | ceiling | FAILED | INCOMPLETE_GENERATION | length | 8192 | 0 | 134,736 |
| 05 | `ollama/kimi-k3` | 8192 | `mini_fcl` | 1 | carry | blocked | — (no attempt) | — | — | — | — | — |
| 05 | `ollama/kimi-k3` | 8192 | `mini_prose` | 1 | carry | ceiling | FAILED | INCOMPLETE_GENERATION | length | 8192 | 0 | 134,688 |
| 07 | `ollama/glm-5.3` | 32768 | `mini_fcl` | 1 | objection | **clock** | FAILED | TRANSPORT_OR_RESPONSE_ERROR | — | — | — | 180,368 |
| 07 | `ollama/glm-5.3` | 32768 | `mini_fcl` | 1 | response | blocked | — (no attempt) | — | — | — | — | — |
| 07 | `ollama/glm-5.3` | 32768 | `mini_fcl` | 1 | carry | blocked | — (no attempt) | — | — | — | — | — |
| 08 | `ollama/kimi-k3` | 32768 | `mini_fcl` | 1 | carry | **clock** | FAILED | TRANSPORT_OR_RESPONSE_ERROR | — | — | — | 180,456 |

**Ceiling-caused: 7.** `failure_code: INCOMPLETE_GENERATION` with
`finish_reason: "length"` and `usage.completion_tokens` exactly equal to the
arm's declared `max_tokens` (8,192). Five of the seven returned **zero bytes** of
`content` — the transport raises `INCOMPLETE_GENERATION` whenever
`finish_reason != "stop"`, and the runner's `decode_contribution` then refuses
empty text as `NO_PUBLIC_CONTENT`, so the receipt is FAILED with a null
`envelope_status`; two returned content and are PARTIAL. Every one of the seven
carries `reasoning_content_present: true`. Occurrences 01, 02, 03 and 06
(`deepseek-flash`, `ollama/gpt-oss-120b`, `ollama/qwen3.5-397b`,
`ollama/gemma4-31b`) have **no** ceiling-caused outcome at all. Per family:
`ollama/glm-5.3` 4, `ollama/kimi-k3` 3.

**Timeout-caused: 2.** `failure_code: TRANSPORT_OR_RESPONSE_ERROR` with
`error: "The read operation timed out"` at 180,368 ms and 180,456 ms against
`settings.timeout_seconds: 180`. No `finish_reason`, no `usage`, no content.
These are **not** ceiling truncations, and both are on occurrences that had
already raised `max_tokens` to 32,768 under runner v2.

**Blocked: 6.** Coordinates with no `attempts` marker, no `requests`, no
provider record and no receipt: the truncation rule removed them from the queue
after an upstream node of the same arm failed. They were never dispatched and
are not failures of anything.

The reading F002 is built on is therefore narrow and stated plainly: **at 8,192
the binding constraint on these two families was the ceiling; at 32,768 it is the
wall clock.** The 7 ceiling-caused cells of 04 and 05 were already re-asked at
32,768 by occurrences 07 and 08; what 07 and 08 could not answer is the four
`mini_fcl` cells the 180-second clock took. This is the same wall C001
occurrence-02 met on `deepseek-flash × fcl` and resolved with 32,768 at 600 s
(`experiments/diagnostics/C001-contrast-triple/PLAN.md` §15, receipt
REC-20260914-V), and REC-20260914-T already names it as an open follow-up in
those words: "the **fixed 180-second endpoint timeout**, which is not a per-arm
declaration and did not move with the ceiling, took both of this run's failures
and is the binding constraint at 32,768 on these two families".

## The coordinate set

Two occurrences, one arm each, five nodes each — **10 calls and no more**.

| | occurrence-01 | occurrence-02 |
|---|---|---|
| endpoint | `ollama/glm-5.3` | `ollama/kimi-k3` |
| arm | `mini_fcl` (surface `fcl`, kind `mini`) | `mini_fcl` |
| `max_tokens` | 32,768 | 32,768 |
| `timeout_seconds` | **600** | **600** |
| `seed` | 7 | 7 |
| scope | `{"problems": ["daily"], "cycles": [1]}` | same |
| planned calls | 5 | 5 |
| credential | `OLLAMA_API_KEY` | `OLLAMA_API_KEY` |

**Why the whole `mini_fcl` arm and not only the four unresolved nodes.** fork5 is
a dependency graph, not a bag of cells: `objection` and `rival` read `account`'s
artifact, `response` reads `objection`'s, `carry` reads the rest. A node cannot
be re-asked without its inputs, and F001's artifacts belong to F001's plan
identity — importing them into a differently-identified occurrence would put an
artifact produced under one frozen plan inside another, which no custody check in
this harness would accept and which this register will not do. The smallest unit
that can be re-dispatched honestly is therefore the arm chain from `account`
down, and that is what F002 dispatches. The two occurrences' `account` and
`rival` cells (on 07) and `account`, `objection`, `rival`, `response` cells (on
08) were resolved once already at the same ceiling and the same seed; asking them
again under a longer clock is the cost of reaching the cells that were not, and
the new answers do not replace the old ones — F001's records stand exactly as
published.

**What is not dispatched, and why.** `bare` and `mini_prose` are **not** declared
on either occurrence. Every one of their cells is resolved at 32,768 in
occurrences 07 and 08, and this register re-asks only what was unresolved. One
cost of that choice is named here rather than hidden: occurrence-07's
`mini_prose/response` completed in **175,006 ms**, within five seconds of the
180-second clock it ran under, so a prose control at the raised clock would not
have been redundant. The alternative — declaring all three arms on both
occurrences, 22 calls — was considered and **not taken**, because it spends 12
calls re-answering cells that are already answered. A reader who wants a
within-occurrence prose control at 600 s must read that as absent from F002, not
as reported null.

## Ceilings, clocks and concurrency

* `max_tokens` 32,768 on both arms. **32,768 is not predicted to be sufficient**
  and nothing here treats it as a fix; it is the figure occurrences 07 and 08
  already ran at, so F002 changes one thing and not two against them.
* `timeout_seconds` **600** on both arms. 600 is the transport's own validation
  maximum — `provider_openai_compat.Endpoint.__post_init__` admits 1…600 and
  refuses 601 — reached rather than invented, exactly as C001 occurrence-02
  reached it. It is applied to the resolved `Endpoint` **value** by
  `dataclasses.replace` at dispatch; `src/minireason/data/endpoints.json` is a
  pinned published file that other plans hash and is **never written**.
* **What 600 s rests on.** The rates F001 itself recorded at 32,768 on these two
  families are 77.9–151.0 completion tokens per second over 18 timed calls
  (mean 99.0). A call that spends the whole 32,768 therefore takes 217–421 s,
  which 600 s covers and 180 s did not. At the slower rates these families showed
  at 8,192 (60.3–71.5 tok/s on `kimi-k3`) a full-ceiling call would take up to
  543 s, still inside 600 but not by much. **600 s is not predicted to be
  sufficient either.** A call that reaches it is a `TRANSPORT_OR_RESPONSE_ERROR`
  refusal recorded with its code, ending that arm, and that outcome is reported
  exactly as any other.
* Concurrency: five per credential, process-wide. Both occurrences spend
  `OLLAMA_API_KEY`, so one `send-round` process drives them through **one**
  shared gate of five in flight between them — never five each. `retries` is 0 at
  every layer.

## What is compared

**The same falsifier as F001, re-evaluated only on the cells that were
previously unresolved.** F001's falsifier is quoted in full in its own register
and is not restated or weakened here. What F002 can contribute to it is exactly
this: the `mini_fcl` FCL-1 parse outcome (`commitment_surface_state` per node:
`read_fcl1` vs `parse_failure` / `schema_failure` / `unavailable_decode_failure`)
on the two families whose `mini_fcl` arm F001 could not complete, at a clock long
enough for the ceiling they already ran at. Nothing else in F001's fact table is
re-opened.

## What is not claimed

* **A difference read between F002 and any F001 occurrence is a resource
  observation, never a semantic one.** F002 differs from occurrences 07 and 08 in
  the wall clock *and* in the runner identity, and from 04 and 05 in the ceiling
  *and* the clock *and* the runner. More tokens and more seconds buy the model
  more room; they do not ask it to reason differently, and no claim that they do
  may be read off these records. Within F002 both occurrences share one ceiling
  and one clock, so the family-to-family comparison this study actually asks is
  unaffected.
* **No merit claim, no ranking, no "which family reasons better".** Parser
  success, more objections, longer documents, more refs, more ν nodes and a
  larger graph are not repair. A `refuted` label is bookkeeping over the attack
  relation the authors themselves declared. Transport status is never a verdict:
  a FAILED coordinate and a ceiling truncation are resource facts.
* **F002 is not a correction of F001.** Nothing from 04, 05, 07 or 08 is
  re-sent, relabelled, repaired or superseded. Two occurrences of one arm are two
  observations, not a sample.
* **No retries.** One `complete` is one request on the wire or none; an attempted
  coordinate with no terminal evidence is audited and never re-sent; one FAILED
  node still ends that arm for the rest of the occurrence.
* **A cell that hits the raised ceiling stays PARTIAL or unresolved.** A node
  returning `finish_reason: length` at 32,768 with non-empty content is recorded
  PARTIAL — OPAQUE too if its envelope does not parse after the one declared
  repair — preserved, usable, never retried and never relabelled. A node that
  returns zero bytes is FAILED with `INCOMPLETE_GENERATION` and ends its arm.
* **The declared asymmetries of F001 still hold.** Reasoning is emitted by
  default on both families, cannot be switched off through this surface, is
  billed against `max_tokens`, is recorded per node as
  `reasoning_content_present`, and is never persisted, returned or fed to another
  call (`reasoning_content_persisted` remains a hard refusal). `native` is
  unavailable on both (`ARM_NATIVE_WIRE_UNKNOWN` at plan time). An OPAQUE rate
  here is still not comparable with H005 occurrence-01;
  `strict_parse_would_succeed` is the comparable figure.

## Publication target — declared deviation

F001's and C001's deviation stands and is inherited: publication is to the
working branch `claude/project-state-direction-j5rbun`, and `send-round` is run
with `--publish-ref origin/claude/project-state-direction-j5rbun`. Publication to
`main` remains **pending owner merge**. No dispatch may be run against an
unpublished tree: `check_published` byte-compares the transitive closure of every
wave's inputs against the committed bytes, and `provider_pins` must be non-null.

## Operating sequence

The publication and dispatch sequence is recorded in this decision's opening
receipt in `docs/DECISION_LEDGER.md` and in the dated section appended to
[`docs/workflows/fork5-multifamily.md`](../../../docs/workflows/fork5-multifamily.md).
In outline, and identical to F001's sequence with `tools/multicycle_commitment_study_multi_v3.py`
in place of the v2 runner and `--occurrences occurrence-01 occurrence-02`:
`initialize` then `verify` for each occurrence at **zero provider calls**, one
publication of the frozen plans and manifests, then per round `prepare-wave` for
each occurrence with ready coordinates, **one** commit and push covering every
required input path, **one** `send-round` over both occurrences against that
published commit, and **one** commit and push of the new records before the next
round is prepared. Then `audit` per occurrence, then `tools/import_h005.py` and
`tools/use_relation_h005.py` at full scope.

**Measured cadence** (offline rehearsal over this exact material and these exact
arms): one node per occurrence per round except round 2, which carries
`objection` and `rival` on both — **2 / 4 / 2 / 2 = 10 calls in four rounds** if
no arm is truncated, and fewer if one is, the shortfall being the truncation rule
removing coordinates from the queue, never a refusal. Four rounds, four pushes
before dispatch plus one final push of round 4's records — five in all.

No step in this register runs anything live on its own authority; dispatch is the
operator's act, after publication.
