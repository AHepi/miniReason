# F001 prospective study: one fork5 invocation across six model families

Draft pre-registration, staged and **not run**. Participant material is
[material.json](material.json): the H005 material
(`experiments/diagnostics/H005-open-prose-commitments/material.json`,
sha256 `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927`)
verbatim, plus one added key, `study_id`. Nothing else in it is altered — not a
problem, not a template, not an instruction, not a source pin. The runner is
`tools/multicycle_commitment_study_multi.py`, a fork of the owner's H005 runner
whose differences are listed in its own header and in `NOTES.md`.

No provider output was produced *for* this study, and none of it is evidence
*in* it. Two existing records did motivate the two declared decode repairs, and
both are cited where the repairs are declared (Disclosure 1): the owner's own
frozen H005 occurrence-01 for the control-character repair, and the provider
module's staging smoke for the fence repair. They are transport observations,
they are named so the repairs can be checked against them, and nothing in
*What counts as evidence* draws on them.

This register follows H005's [PROTOCOL.md](../H005-open-prose-commitments/PROTOCOL.md);
where this file is silent, that protocol governs.

## Question

Do the **mechanism-level facts the published instruments report** — the facts
`minireason.graph_import_h005` computes and the use-relation instrument reads —
vary across model families under identical material, identical topology and
identical rendering?

The facts in question are exactly these, and only these:

| Fact | Where it is read |
|---|---|
| FCL‑1 parse rate on the `mini_fcl` arm | `commitment_surface_state` per node: `read_fcl1` vs `parse_failure` / `schema_failure` |
| Reference resolution | `report.resolution`: `refs`, `resolved`, `extensions`, `dangling`, `task` |
| Cross-document `depends` usage | residue code `depends_cross_document` (0 in H005 occurrence‑01) |
| OPAQUE rate | `envelope_status` per node — **see the comparability warning below** |
| ν-attacks (criticism of a criticism) | `validity_node_minted_unasserted`, `criticism_of_criticism_retargeted`, ν nodes in `att` |
| Reinstatement | the grounded labels: an artifact attacked and then restored by an attacker of its attacker |

This is a question about what a carrier makes *checkable*, not about which model
reasons better. Nothing in this study ranks families, and no count below is a
score.

## Arms — 19

Three arms on each of six families — four on the one family whose wire carries a
thinking control — all through the OpenAI-compatible path
(`chat_path: /chat/completions`), never the `.native` Ollama path:

| Occurrence | Endpoint | Family | Key | Arms |
|---|---|---|---|---|
| occurrence-01 | `deepseek-flash` | `deepseek` | `DEEPSEEK_API_KEY` | `bare`, **`native`**, `mini_prose`, `mini_fcl` |
| occurrence-02 | `ollama/gpt-oss-120b` (`gpt-oss:120b`) | `ollama-cloud/gpt-oss` | `OLLAMA_API_KEY` | `bare`, `mini_prose`, `mini_fcl` |
| occurrence-03 | `ollama/qwen3.5-397b` (`qwen3.5:397b`) | `ollama-cloud/qwen` | `OLLAMA_API_KEY` | `bare`, `mini_prose`, `mini_fcl` |
| occurrence-04 | `ollama/glm-5.3` | `ollama-cloud/glm` | `OLLAMA_API_KEY` | `bare`, `mini_prose`, `mini_fcl` |
| occurrence-05 | `ollama/kimi-k3` | `ollama-cloud/kimi` | `OLLAMA_API_KEY` | `bare`, `mini_prose`, `mini_fcl` |
| occurrence-06 | `ollama/gemma4-31b` (`gemma4:31b`) | `ollama-cloud/gemma` | `OLLAMA_API_KEY` | `bare`, `mini_prose`, `mini_fcl` |

`mini_prose` and `mini_fcl` are H005's arms unchanged: the same canonical Mini
compile/reduce/render fixture, the same topology, the same selected field views,
differing only in the commitment carrier. `bare` is H005's single direct call.
`matched` is out of scope for the first run; adding it later is a new
invocation, not a repair of this one.

**The `native` comparison, per family.** AGENTS.md requires the comparison
*bare, native reasoning and Mini*, and `docs/EXPERIMENT_METHOD.md` requires that
where native mode is unsupported the comparison be **marked unavailable** rather
than dropped. Stated family by family:

| Family | `native` on the wire | This register |
|---|---|---|
| `deepseek` (occurrence-01) | Supported: `thinking: {"type": "enabled"}` plus `reasoning_effort`, which `provider_openai_compat._build_payload` emits for this family and this family only | **Declared and run** — one call |
| `ollama-cloud/gpt-oss`, `/qwen`, `/glm`, `/kimi`, `/gemma` (occurrences 02–06) | **Unavailable.** The provider module refuses a `thinking=` control on any family but `deepseek`, and `Endpoint.native` is a different axis (Ollama's own `/api/chat`), not a thinking mode. These families emit reasoning by default with no switch | **Marked unavailable**, with the runner's own refusal code `ARM_NATIVE_WIRE_UNKNOWN` — declaring the arm is refused at plan time, before any call is spent |

So the native comparison is available on one of the six families and is run
there. It is not silently discharged for DeepSeek by a limitation that belongs
to the other five.

**`bare` is not the same control in every occurrence.** On occurrence-01 it is a
**reasoning-disabled direct baseline**: the DeepSeek arm carries
`thinking: {"type": "disabled"}` on the wire. On occurrences 02–06 it is a
**default direct baseline**: those families emit reasoning by default and it
cannot be switched off through this surface, exactly the case
`docs/EXPERIMENT_METHOD.md` covers with "if the endpoint cannot disable
reasoning, describe the bare arm as a default direct baseline". The two are not
the same control, and any cross-occurrence reading of `bare` PARTIAL rates or
token counts must say which one it is reading.

**Why one occurrence per family, and not one occurrence with 19 suffixed arms.**
The published importer decides whether to read a node's commitment surface as
FCL‑1 by exact membership: `graph_import_h005.FCL_SURFACE_ARMS == ("mini_fcl",)`.
An arm named `mini_fcl@gpt-oss-120b` — which the runner supports and
canonicalises to `mini_fcl__ollama_gpt-oss-120b` — would be read as a **prose**
arm, its FCL‑1 document would never be parsed, and the first fact this study
exists to measure would silently vanish. Keeping the canonical arm names and
putting the family in the occurrence costs nothing and keeps the instrument
honest. (The importer's own `_SAFE_COMPONENT` is `^[A-Za-z0-9_-]+$`, so a raw
`@` or `.` in an arm name would additionally be refused outright, after the
calls had been spent.)

## Scope of the first run — declared, frozen and enforced

Cycle 1 only — one complete `fork5` invocation — of the `daily` problem.

    12 multi-call arms x 5 nodes  = 60
     6 bare arms       x 1 node   =  6
     1 native arm      x 1 node   =  1   (occurrence-01 only)
                                   ---
                                    67 unique provider calls

| Occurrence | `bare` | `native` | `mini_fcl` | `mini_prose` | Calls |
|---|---|---|---|---|---|
| occurrence-01 (deepseek-flash) | 1 | 1 | 5 | 5 | **12** |
| occurrence-02 (gpt-oss:120b) | 1 | — | 5 | 5 | **11** |
| occurrence-03 (qwen3.5:397b) | 1 | — | 5 | 5 | **11** |
| occurrence-04 (glm-5.3) | 1 | — | 5 | 5 | **11** |
| occurrence-05 (kimi-k3) | 1 | — | 5 | 5 | **11** |
| occurrence-06 (gemma4:31b) | 1 | — | 5 | 5 | **11** |
| | | | | | **67** |

This is not left to the operator to remember. Each occurrence's `arms.json`
declares

```json
"scope": {"problems": ["daily"], "cycles": [1]}
```

which `verify` recomputes and `arms_sha256` pins, so a changed scope is
`IMMUTABLE_PLAN_MISMATCH`. The runner then enforces it:

* `ready_coordinates` — and therefore `prepare-wave` and `send-wave` — refuses
  any other problem or cycle with **`SCOPE_EXCLUDED`**. There is no path from
  this register to `physics`, `philosophy`, `sociology`, cycle 2 or cycle 3.
* `plan["max_calls"]` counts only what the scope admits, so it **is** the
  authorisation: 12 on occurrence-01 and 11 on each of 02–06, 67 in all. A test
  builds all six plans from the staged `arms.json` files and pins those numbers
  and that table.
* `plan["max_calls_envelope"]` records the full envelope of the material
  (156 per occurrence, 168 on occurrence-01 with its fourth arm) so the
  difference between "what the material could support" and "what is authorised"
  stays visible in the frozen plan rather than in prose.
* `audit` reads the same scope: anything found outside it is counted as
  `out_of_scope`, which must be 0.

The other three problems, the later cycles, and the `matched` arm are not
authorised by this register. If the cycle‑1 result makes a further invocation
informative, freeze that next template and its purpose prospectively, as H005
requires — a new scope in a new occurrence, not an edit to this one.

## Resource boundary and dispatch discipline

* `max_tokens` 8192 and `timeout_seconds` 180 for every arm, declared per arm in
  `plan.json` under `ceilings`.
* **No retries**, at any layer. One `complete` is one request on the wire or
  none. An attempted coordinate with no terminal evidence is audited before any
  new action; it is never re-sent.
* **Five concurrent requests per credential**, the owner's authorisation. Two
  credentials are in play, so a single coordinator process may hold up to ten in
  flight, never more than five per key. This is enforced in three places, and
  each is tested:
  1. **Wave construction.** `ready_coordinates` admits at most `key_cap` per
     `key_env` (five, or an endpoint's smaller `max_concurrency`), and
     `send-wave` re-refuses a wave that carries more with `WAVE_SIZE_INVALID`,
     before any attempt marker or provider object exists.
  2. **The runner's own per-key gate**, which is a **module-level registry keyed
     by `key_env`** — one semaphore per credential for the whole process,
     acquired *before* the attempt marker is written. Two `send-wave` calls
     sharing a credential therefore share one gate: five in flight *between*
     them, not five each.
  3. **`provider_openai_compat.slots_for`**, the transport's own process-wide
     per-key semaphore around the socket.
* **Several occurrences may be driven by one process, and only by one.** Because
  the gate in (2) is process-wide, the five Ollama occurrences may be prepared
  and sent together by a single coordinator (`send-round`) while
  `OLLAMA_API_KEY` stays at five in flight in total, and occurrence-01 (DeepSeek)
  overlaps them on its own credential. What is **not** permitted is two
  coordinator *processes* on one credential: nothing in this repository can hold
  a ceiling across processes, so the register authorises exactly one runner
  process at a time.
* **One `FAILED` node ends that arm for the rest of the occurrence.** `retries`
  is 0 by design, `arm_stopped` scans cycles 1..N, and `ready_coordinates` then
  returns an empty queue for that arm. The next `prepare-wave` simply returns
  **fewer coordinates** — it does not refuse, and nothing announces the
  truncation at dispatch time. The audit signal is: `audit.counts.FAILED` ≥ 1
  together with `audit.counts.unvisited` > 0, and the arm's row in
  `audit.invocations` reading `"complete": false`. Read it after every round.
  Each `FAILED` receipt records `failure_type` (the exception class) **and
  `failure_code`** — the transport's own `ProviderFailure.code`, so `HTTP_429`,
  `KEY_MISSING` and `TRANSPORT_OR_RESPONSE_ERROR` are distinguishable without
  opening the provider call records.
* `seed: 7` on every Ollama arm — Ollama honours it, and it is recorded in the
  plan, in every request record and in every provider call record. DeepSeek
  declares no seed, so it stays null there; that asymmetry is a property of the
  providers and is reported, not corrected.
* **Publication before dispatch.** `send-wave` refuses unless HEAD equals the
  configured publication ref (`--publish-ref`, default the current branch's
  upstream) *and* every required input path — plan, material, arms, manifests,
  the runner itself, the runtime pins, the provider module, the endpoint
  registry, and every request, trace, attempt, receipt, artifact, raw response
  text and provider call record a dependency reaches — is byte-identical to the
  committed bytes. A ref that has moved is `PUBLISH_REF_CHANGED`; a file that
  differs by one byte is `INPUT_NOT_PUBLISHED`. Neither constructs a provider.
* **`occurrence-0N` no-clobber.** An occurrence directory may pre-exist only
  with `material.json` and/or `arms.json` in it, and only with the exact bytes
  being frozen; anything else is `OCCURRENCE_EXISTS`, and differing bytes are
  `MATERIAL_EXISTS_DIFFERENT`. Every record file is opened write-once. A
  coordinate that already has an attempt or a receipt is `NO_REPLAY`.

## Two disclosures that change how the numbers may be read

**1. The OPAQUE rate of this study is NOT comparable with H005 occurrence‑01.**
Under H005's strict-only decode, an envelope that fails a strict `json.loads`
becomes OPAQUE and the commitments the author actually wrote are lost *in
decoding*. The fork declares **two repairs and no others**, applied before the
same strict shape check: strip **one** outer Markdown fence when the whole
trimmed content is a single fenced block, then re-parse with `strict=False` so a
raw control character inside a string does not fail the parse. Nothing is
reconstructed, no field is invented, the raw returned text is stored
byte-for-byte in `responses/<node>.txt` and hashed into `public_text_sha256`,
and an envelope no declared repair rescues is still OPAQUE.

Each repair is there because a record shows the loss it prevents. Both records
are named here, and both are transport observations, not evidence in this study:

* **`fence_stripped` — the provider module's staging smoke.** Ollama cloud
  accepts `response_format: {"type": "json_object"}` without enforcing it.
  `docs/sources/provider-openai-compat-smoke-notes-2026-09-14.md` §3 records it
  in those words and names the models: "`kimi-k3`, `gemma4:31b`,
  `mistral-large-3:675b` on the compatible path". The records behind that line
  are in the provider's staging smoke, `scratchpad/provider-smoke/run-02-ceiling-512/`:
  on the OpenAI-compatible path
  `ollama__kimi-k3/call-0001.response.json` returned
  ```` ```json\n{"ok": true, "model": "Kimi"}\n``` ```` and
  `ollama__gemma4-31b/call-0001.response.json` returned
  ```` ```json\n{"ok": true, "model": "gpt-4o"}\n``` ````. Both models are in
  this study's scope — `kimi-k3` is occurrence-05 and `gemma4:31b` is
  occurrence-06 — and `gemma4:31b` fenced in `run-01` as well. Ten of the thirty
  contentful responses across that smoke are fenced. The probe was a one-line
  "reply with `{"ok": true, "model": ...}`" request, not this study's material,
  so it evidences the *habit*, not a rate.
* **`lenient_control_chars` — the owner's own frozen H005 occurrence-01.**
  `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/responses/daily/matched/cycle01/response.txt`
  (7,732 bytes, sha256 `054b1c43c50e4d2a581023dc73cd08439665cf18b7663681559a8ab19345df3a`)
  and `.../carry.txt` (6,505 bytes, sha256
  `c61e45da74b50542ae5d07b2e4af9a18e0696c789981ca26b42c944ec3913c8e`) are JSON
  whose string values carry raw newline control characters — twelve and sixteen
  of them. Strict `json.loads` raises `Invalid control character at: line 1
  column 756 (char 755)` and `... column 727 (char 726)`; the same bytes parsed
  with `strict=False` yield exactly `{body, commitments}`, both strings, the
  commitments 2,346 and 2,363 characters. Both nodes are recorded COMPLETE with
  `finish_reason: stop` and `envelope_status: OPAQUE`, and their
  `commitments_sha256` is the sha256 of the empty string. Root's review of that
  asymmetry is
  `docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md`.
  **Stated exactly:** that record is DeepSeek's — the family occurrence-01 runs
  — not an Ollama family's, and no Ollama record in reach shows a
  control-character case: zero of the thirty contentful smoke responses are
  rescued by `strict=False` alone, the probe being far too short to contain a
  newline inside a string. The repair is declared for every family because the
  loss it prevents is a transport fault, not a family's property; whether any
  family in scope commits it is one of the things the run will show, and
  `audit.counts.lenient_control_chars` is where it will be counted.

Each receipt records `envelope_repairs` (which repairs were actually applied)
and `strict_parse_would_succeed` (the owner's strict-only outcome on the raw
text). **`strict_parse_would_succeed` is the figure comparable with H005
occurrence‑01. The OPAQUE rate is not.** Both are reported; neither is a merit
measure, and a fence is a formatting habit, not a reasoning failure.

**2. Reasoning tokens count against the ceiling on most Ollama families.**
Every Ollama model in scope except `gemma4:31b` emits reasoning by default, it
cannot be switched off through this surface, and it is billed against
`max_tokens`. Two consequences are declared in advance: a family may reach
`finish_reason: length` and be recorded PARTIAL where DeepSeek would not, and
that is a property of the transport budget, not of the contribution; and
`reasoning_content_present` is **recorded** per node rather than failing the
node — hidden reasoning is a custody failure only on DeepSeek, where the runner
set a thinking control and set it to disabled. `reasoning_content_persisted`
remains a hard refusal everywhere: no native reasoning text is ever stored,
returned, or fed to another call. PARTIAL is treated exactly as H005 treats it:
preserved, usable, never retried and never relabelled.

The third consequence is the one the Arms section states and that is repeated
here because it bears on every number in this disclosure: **`bare` is a
reasoning-disabled direct baseline on occurrence-01 and a default direct
baseline on occurrences 02–06.** The two are not the same control, so a `bare`
PARTIAL rate or token count read across occurrences is comparing a
reasoning-off arm with reasoning-on arms.

## What counts as evidence

Only the mechanism facts in the table above, as computed by the published
importer over each occurrence, plus the runner's own audit counts. Nothing else.

* No merit claim, no ranking, no "which family reasons better". A family whose
  FCL‑1 documents parse is not thereby correct, and a family whose documents do
  not parse has not thereby failed to reason.
* Parser success, more objections, longer documents, more refs, more ν nodes and
  a larger graph are **not** repair. A refuted label is bookkeeping over the
  attack relation the authors declared; invariant I7 of the importer says no
  label is a semantic attribution.
* An `accepted` label on an unattacked artifact is accept-by-position: this
  import reads criticism only from an FCL‑1 commitment surface, so on a prose
  arm no warrant, no attack edge and no refuted label can arise at all. Cross-arm
  status distributions are a property of the carrier this instrument reads.
* **Root alone reads the content.** Whether a criticism was any good, whether a
  dependence was real, whether the amendment repaired anything — none of that is
  in this study's output, and no count here may be offered as a substitute for
  reading the artifacts.
* Transport status is never a verdict. A `FAILED` coordinate, a timeout and a
  ceiling truncation are resource facts.

## Falsifier

The question is answered **no** — the mechanism facts do not vary by family —
if, across the six occurrences, on the same material and the same topology:

* every `mini_fcl` arm's FCL‑1 parse rate is the same (all 5/5, or all 0/5); and
* `resolution.resolved / resolution.refs` and `dangling` do not differ; and
* `depends_cross_document`, `criticism_of_criticism_retargeted` and the ν count
  are equal across families; and
* the grounded label multiset over the five `mini_fcl` node artifacts is the
  same in every occurrence, including whether any reinstatement occurs.

Any one of these differing is the positive result, and the positive result is
"this carrier is read differently by different families", not "family X is
better". If they do not differ, that is reported as the answer, with its limits:
one problem, one cycle, one template, one seed, one day.

## Claim ceiling

The most this study can support is a statement of the form: *under identical
frozen material and an identical rendered brief, the mechanism-level facts the
published instruments report did / did not vary across these six families, on
this one fork5 invocation of the `daily` problem, at these ceilings, on this
date.* It cannot support a claim about model capability, about FCL‑1's value,
about Mini's scheduler (which does not execute here), about any family's
behaviour on another problem or another cycle, or about any family not listed.
Six families with one invocation each is six observations, not a sample.

## Operating sequence — what publication actually costs

`send-wave` will not dispatch unless HEAD equals the publication ref **and every
path in the wave's transitive closure is byte-identical to the committed bytes**
(`check_published` → `required_paths`). That closure includes the *previous*
wave's receipts, artifacts, raw response texts and provider call records. So a
wave cannot be sent until the previous wave's results are committed and pushed:
**one push per round**, not one per occurrence and not one per call.

HEAD does not move between sends, so all six occurrences can be prepared against
the same commit and sent against it. That is what `send-round` is for, and what
the process-wide per-key gate makes safe: the five Ollama occurrences spend
`OLLAMA_API_KEY` through **one** shared gate of five, and occurrence-01 spends
`DEEPSEEK_API_KEY` alongside them. **One process drives all six.** (Two
coordinator processes on one credential would not be held by anything; that is
not authorised.)

Per round:

1. `prepare-wave --problem daily --cycle 1` for every occurrence whose next wave
   is ready. Each refuses while its own earlier wave is unresolved
   (`PREPARED_WAVE_PENDING`, `UNRESOLVED_ATTEMPT`).
2. **One** `git commit` + `git push` covering every required input path of every
   prepared wave.
3. `send-round --study experiments/diagnostics/F001-fork5-multifamily --occurrences occurrence-01 … occurrence-06 --publish-ref origin/<branch>`
   — each occurrence still runs its own publication check, its own wave
   validation and its own `NO_REPLAY` refusal; the gate is shared.
4. Read the audit signal before the next round: `FAILED` ≥ 1 with `unvisited` > 0
   and a `"complete": false` invocation row means an arm has been truncated for
   the rest of the occurrence.

Before all of it, once: `initialize` and `verify` for each occurrence, and a
first commit carrying the runner, `src/minireason/provider_openai_compat.py`,
`src/minireason/data/endpoints.json`, the material, the six `arms.json`, the
plans and the manifests — `provider_pins` must be non-null for a live send, and
the staged tree is not a git repository, so the runner must be committed into
`/home/user/miniReason` before any dispatch.

**Measured cadence** (offline drive of all six occurrences over this exact
material and these exact arms, `provider: offline`, no socket):

| Round | occurrence-01 wave | occurrences 02–06 wave | Calls in the round |
|---|---|---|---|
| 1 | 4 (`bare`, `native`, two `account`) | 3 (`bare`, two `account`) | 19 |
| 2 | 4 (`objection`, `rival` ×2 arms) | 4 | 24 |
| 3 | 2 (`response` ×2 arms) | 2 | 12 |
| 4 | 2 (`carry` ×2 arms) | 2 | 12 |
| | **12** | **11 each** | **67** |

**Four rounds. Four pushes before dispatch, plus one final push** of round 4's
records so the audit and the import read published bytes — five in all. Driving
the occurrences one at a time instead would be 24 prepare → push → send
round-trips for the same 67 calls.

`required_paths` per wave grows 64–66 → 82 → 110 → 126 as the closure takes in
each round's records, so a late `send-wave` runs ~126 `git show` comparisons.
In-flight work is bounded by the credential, not the round: round 2 asks for 20
Ollama calls at once and the shared gate admits five.

Then, per occurrence: `audit` (expect `max_calls` = COMPLETE + PARTIAL,
`unvisited` 0, `out_of_scope` 0), `tools/import_h005.py`, then the use-relation
instrument.

No step in this register runs anything live on its own authority; dispatch is
the operator's act, after publication.

## Successor occurrences 07 and 08 under runner v2 — appended 2026-09-14

**Appended after the first run; nothing above this line is altered.** Occurrences
01–06 were dispatched under `tools/multicycle_commitment_study_multi.py` (v1),
and their evidence, audits and analysis are published and closed. This section
pre-registers two further occurrences under a successor runner, and is written
and published before either occurrence is initialized.

### Why: what occurrence-04 and occurrence-05 actually recorded

Occurrences 04 (`ollama/glm-5.3`) and 05 (`ollama/kimi-k3`) are the two the
completion ceiling truncated. Their published audits —
`experiments/analyses/F001-fork5-multifamily-2026-09-14/occurrence-04/audit.json`
and `.../occurrence-05/audit.json` — record COMPLETE 4 / PARTIAL 1 / FAILED 3 /
OPAQUE 1 with `unvisited` 3, and COMPLETE 7 / PARTIAL 1 / FAILED 2 / OPAQUE 1
with `unvisited` 1, both with `unresolved_attempts` 0 and `out_of_scope` 0. All
seven non-COMPLETE terminal records of the whole six-occurrence run are on these
two occurrences, and every one of them carries the same `failure_code`,
`INCOMPLETE_GENERATION`, with `finish_reason: length` at exactly **8,192
completion tokens** and `reasoning_content_present: true`:

| Occurrence | Coordinate | Terminal | `failure_code` | completion tokens | raw `responses/*.txt` |
|---|---|---|---|---|---|
| 04 | `daily/mini_fcl/cycle01/objection` | FAILED | `INCOMPLETE_GENERATION` | 8,192 | **0 bytes** |
| 04 | `daily/mini_fcl/cycle01/rival` | FAILED | `INCOMPLETE_GENERATION` | 8,192 | **0 bytes** |
| 04 | `daily/mini_prose/cycle01/objection` | PARTIAL / OPAQUE | `INCOMPLETE_GENERATION` | 8,192 | 288 bytes |
| 04 | `daily/mini_prose/cycle01/response` | FAILED | `INCOMPLETE_GENERATION` | 8,192 | **0 bytes** |
| 05 | `daily/mini_fcl/cycle01/response` | FAILED | `INCOMPLETE_GENERATION` | 8,192 | **0 bytes** |
| 05 | `daily/mini_fcl/cycle01/rival` | PARTIAL / OPAQUE | `INCOMPLETE_GENERATION` | 8,192 | 7,112 bytes |
| 05 | `daily/mini_prose/cycle01/carry` | FAILED | `INCOMPLETE_GENERATION` | 8,192 | **0 bytes** |

Disclosure 2 declared in advance that reasoning tokens are billed against
`max_tokens` on these families. **Five of the seven spent the whole 8,192-token
ceiling on reasoning and returned zero bytes of public content**, so there was
nothing to record as a partial contribution and the arm ended for the rest of the
occurrence. That is a transport-budget fact and not a fact about the
contributions: on those coordinates these two families produced no observable
commitment surface at all, so nothing about their surfaces can be read off 04
and 05 — not that they parse, not that they fail to parse, not that they are
short, not that they are absent.

### What 07 and 08 are

The same frozen material, the same arms, the same scope, the same no-retry
discipline and the same per-key ceiling. Two things differ from 04 and 05: the
runner identity, and the completion ceiling.

| Occurrence | Endpoint | Key | Arms | `max_tokens` per arm | Calls |
|---|---|---|---|---|---|
| occurrence-07 | `ollama/glm-5.3` | `OLLAMA_API_KEY` | `bare`, `mini_fcl`, `mini_prose` | 32,768 | 11 |
| occurrence-08 | `ollama/kimi-k3` | `OLLAMA_API_KEY` | `bare`, `mini_fcl`, `mini_prose` | 32,768 | 11 |

**22 provider calls in all**, and `plan["max_calls"]` is the authorisation for
each occurrence exactly as it is for 01–06. `scope` is frozen at
`{"problems": ["daily"], "cycles": [1]}` and enforced as `SCOPE_EXCLUDED`; `seed`
is 7 on every arm, as on 04 and 05; `automatic_retries` is 0; `provider_mode` is
`live`; the timeout is the endpoint record's and no arm declares one.
`occurrence-07/arms.json` is `occurrence-04/arms.json` with `max_tokens` 32768 in
place of 8192 on each of its three arms, and `occurrence-08/arms.json` is
`occurrence-05/arms.json` under the same single substitution. Nothing else in
either declaration differs — not an endpoint, not a surface, not a kind, not a
seed, not the scope.

### The declared difference, and the proof that it is the only one

07 and 08 run under a successor runner,
`tools/multicycle_commitment_study_multi_v2.py`. They must: v1 refuses a per-arm
ceiling above 8,192 with `ARM_CEILING`, and v1's bytes may not be edited, because
v1 pins its own sha256 into every plan it has already written — as
`runner_sha256` and `helper_sha256`, both folded into `plan_id` — so one changed
byte would invalidate the six published plans and every custody check that reads
them.

v2 is a byte copy of v1 at sha256
`a56fed415bd72395470f40c18d9985ec6fcde8a851662006a9b6fecbfe57ec80` with four
differences, listed in its own header and each marked `# V2:` in its source:

* **(a)** the provenance header itself;
* **(b)** v1's `CAP = 8192` is replaced. The *bound* `validate_arms` enforces on
  a declared per-arm ceiling becomes `MAX_CEILING = 393216` — the provider's own
  bound, mirrored from
  `provider_openai_compat._RecordedCaller._validate_call_args`, which refuses any
  `max_tokens` outside `1 <= n <= 393216` — and `validate_arms` now accepts any
  per-arm ceiling in `1..MAX_CEILING`. The *default* an arm that declares no
  `max_tokens` receives keeps v1's value under the name `DEFAULT_CEILING = 8192`,
  so an undeclared arm is settled exactly as v1 settles it. (v1's
  `EndpointSettings.__post_init__` already admitted the provider bound;
  `validate_arms` was the only place that capped an arm at 8,192.) The two roles
  are separated by name deliberately: raising both would have moved the default
  as well, which is a behavioural change the ceiling question does not need and
  this register does not want.
* **(c)** `manifest_for` takes the occurrence's frozen arm mapping and derives
  `cycles.completion_tokens_per_call` and `cycles.max_completion_tokens` from the
  ceilings the arms actually declare instead of from the module constant. A
  manifest is per template and shared by every arm, so the derivation is the
  maximum declared per-arm ceiling of the occurrence: a pure function of
  `arms.json`, a true upper bound for every arm, and identical to v1's figure
  wherever every arm sits at the default. Without it, raising the bound alone
  would leave every manifest declaring 8,192 while its arms ran at 32,768, and
  raising the constant alone would write 393,216 into manifests no arm asked for.
* **(d)** the docstring says v2; `argparse` prints it as the tool description.

`tests/test_multicycle_commitment_study_multi_v2.py::V2DiffProofTests` **proves**
that list rather than asserting it. With the module docstring normalised away it
diffs v2 against v1 and asserts that the only hunks are exactly the ten the
header declares, that every hunk is marked `# V2:` in the source, that the only
definitions differing from v1 are the six the ceiling touches (`EndpointSettings`,
`validate_arms`, `settings_for`, `manifest_for`, `plan_body`, `initialize`), and
that where no arm declares a ceiling v2's frozen arm mapping and manifest bytes
are v1's to the byte. The rest of the v2 suite is the v1 suite re-pointed, so
node topologies, projection text, payload bytes, `write_new`, `plan_id`/`verify`,
waves, attempts, `NO_REPLAY`, artifacts, traces, the provider record layout, the
per-key gate and the publication check are all still under test and all still
v1's.

**So the declared difference between 04/05 and 07/08 is exactly two things — the
runner identity and the completion ceiling — and the runner identity carries no
behavioural difference beyond that ceiling. The ceiling is the only behavioural
difference.** v2 writes its own sha256 as `runner_sha256` and `helper_sha256`, so
no v2 `plan_id` can collide with a v1 `plan_id`: 07 and 08 are two new
occurrences with their own identities, not a re-run of 04 and 05.

### What is not changed, and what is not claimed

* **Reasoning is not manipulated.** No thinking control is set, requested or
  disabled on either family. `provider_openai_compat` refuses a thinking control
  anywhere but DeepSeek and `ARM_NATIVE_WIRE_UNKNOWN` still refuses a `native`
  arm here; reasoning is emitted by default on both families, billed against
  `max_tokens`, recorded per node as `reasoning_content_present`, and never
  persisted, returned or fed to another call (`reasoning_content_persisted`
  remains a hard refusal). A ceiling is a transport budget. Raising it buys the
  model more tokens; it does not ask it to reason differently, and no claim that
  it does may be read off these occurrences.
* **No retries.** `retries` is 0 at every layer, one `complete` is one request on
  the wire or none, an attempted coordinate with no terminal evidence is audited
  and never re-sent, and one FAILED node still ends that arm for the rest of the
  occurrence. Nothing from 04 or 05 is re-sent, relabelled, repaired or
  superseded; those records stand exactly as published.
* **A cell that hits the raised ceiling stays PARTIAL or unresolved.** A node
  returning `finish_reason: length` at 32,768 with non-empty content is recorded
  PARTIAL — OPAQUE too if its envelope does not parse after the one declared
  repair — preserved, usable, never retried and never relabelled. A node that
  returns zero bytes is FAILED with `INCOMPLETE_GENERATION` and ends its arm, and
  the audit signal is the same one this register already names: `FAILED` >= 1
  with `unvisited` > 0 and a `"complete": false` invocation row. **32,768 is not
  predicted to be sufficient and nothing here treats it as a fix.** The raised
  ceiling may change nothing at all; that outcome is reported exactly as any
  other, and an occurrence that truncates again is evidence, not a failed run.
* **07 and 08 are not a correction of 04 and 05.** They are the same two families
  at a second ceiling. Together the four occurrences are one frozen material run
  under two runner identities whose only behavioural difference is the ceiling
  bound, and the only comparison they license is *what these two families return
  at 8,192 completion tokens versus at 32,768*. Everything in *What counts as
  evidence*, *Falsifier* and *Claim ceiling* above applies to them unchanged: no
  merit claim, no ranking, no cross-family reading, and parser success, more
  objections, longer documents, more refs, more ν nodes and a larger graph are
  not repair.
* **The declared asymmetries still hold.** `bare` is a default direct baseline on
  both occurrences, reasoning-on, and is not the reasoning-disabled control
  occurrence-01 carries; `native` is unavailable on both; and an OPAQUE rate here
  is still not comparable with H005 occurrence-01, `strict_parse_would_succeed`
  being the comparable figure.

### Operating sequence

Identical to the sequence above, with
`tools/multicycle_commitment_study_multi_v2.py` in place of the v1 runner and
`--occurrences occurrence-07 occurrence-08`: `initialize` then `verify` for each
occurrence at zero provider calls, one publication of the frozen plans and
manifests, then per round `prepare-wave` for each occurrence with ready
coordinates, **one** commit and push covering every required input path, **one**
`send-round` over both occurrences against that published commit, and **one**
commit and push of the new records before the next round is prepared. Then
`audit` per occurrence, then `tools/import_h005.py` and
`tools/use_relation_h005.py` at full scope into
`experiments/analyses/F001-fork5-multifamily-2026-09-14/occurrence-07/` and
`.../occurrence-08/`.

Both occurrences spend `OLLAMA_API_KEY`, so one `send-round` process drives them
through one shared gate of five in flight. The measured cadence for a three-arm
occurrence is 3 / 4 / 2 / 2 = 11, so the two together are 6 / 8 / 4 / 4 = **22 in
four rounds** if no arm is truncated, and fewer if one is — the shortfall being
the truncation rule removing coordinates from the queue, never a refusal.
