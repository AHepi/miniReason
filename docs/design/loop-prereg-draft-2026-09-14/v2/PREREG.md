# L001 — pre-registration of the first live run of the automated end-to-end harness loop

*Written before any provider call. Nothing in this bundle has been dispatched. The run
directory `experiments/loops/L001-loop-first-live-2026-09-14/` does not yet exist; this
bundle is what will be copied into it at S0 PREREGISTER.*

| file | what it fixes |
|---|---|
| `config.json` | the frozen `minireason.loop.config.v1` document, validated against `types.LoopConfig.from_mapping` |
| `obligations.json` | the failed set **O** (7) and the protected set **P** (12), pinned by sha256 |
| `reading_set.json` | the 38 cells the run may read, in order, with the `max_calls` derivation |
| `calibration.json` | the 9 planted-flaw anchors whose ground truth is true by construction |
| `PREREG.md` | this document |
| `VALIDATION.md` | the exact validation commands and their output, regenerated wholesale at this review |
| `validate.py` | the offline validator; makes no provider call |
| `REVIEW-PREREG.md` | the adversarial review this revision answers, PR-01…PR-25 |
| `CHANGES-PREREG.md` | every edit made at this pre-registration review, with its justification |
| `CLONE-PATCH.md` | what the implementation clone must change for this bundle to validate |

---

## 1. The receipt paragraph (design §8, rendered)

The text below is `receipts.render_preregistration` output and contains every sentence of
`receipts.PREREGISTRATION_REQUIRED_SENTENCES` verbatim — the renderer refuses to return a
text that does not. **The receipt id and the timestamp shown are placeholders and are deliberately impossible.** `REC-20260914-Z` was used here in an earlier draft and is a live, published id - `docs/DECISION_LEDGER.md` already carries it for F002 occurrence-03 - so it is replaced by `REC-YYYYMMDD-X` and the literal `<minted at S0>`, which no ledger can ever carry (REVIEW-PREREG PR-18).
`receipts.open_preregistration` mints the real `REC-<YYYYMMDD>-<X>` under the ledger
append lock at S0, and the appended bytes differ from these only in that id and that
stamp. The `loop_plan_id` sentence is likewise absent here because the plan identity
cannot be computed until `CEILING.md`, the `STD_READING` body and the prompt templates
exist as files to pin; it is
`sha256(canonical({"schema": "minireason.loop.plan-id.v1", "config": <this config,
fully resolved>, "pins": <path -> sha256>}))` and is written into `plan.json` and
published before the first call.

---

**REC-YYYYMMDD-X opened at <minted at S0>: pre-register the automated end-to-end harness loop as a mechanism intervention with its own identity.**

**What this is.** A new instrument, not an observation and not an amendment. It automates three acts the published instruments reserve for root — the `use_relation_h005` reading cells, the C001 PLAN §8a contrast-register marks, and the continue/stop decision — together with the dispatch, import and publication that produce the material they read. It mints its own identity, `loop_plan_id = sha256(canonical(config ∪ pins))`, where the pins cover runner v2, the importer, the use-relation module, the contrast tool, the provider transport, `endpoints.json`, every prompt template, `obligations.json`, `CEILING.md` and the reading-rubric standard body. That identity is written to `experiments/loops/<RUN-ID>/plan.json` and published before the first provider call; the pre-registration timestamp precedes the first call and the record shows it.

Its run directory is `experiments/loops/L001-loop-first-live-2026-09-14/`.

**What it does not amend.** It does not amend, reopen, supersede or reinterpret C001 (`plan_id 328b9452c66fed52203015c540652d3b8ad3107d44dece56b55ebe721da341c8`) or H005, and it registers no finding on either. C001's material, its recoding table, its endpoint set, its replicate count, its §8a reading rule and its claim ceiling are consumed exactly as frozen and are not edited, reformatted or re-hashed. Any change to a frozen value would mint a new `plan_id` for that study under its own §13 and is out of scope here.

**Why a mechanism intervention rather than an experiment.** The object under change is the instrument, not the world: what this run produces is a table of guarded readings and a decision record, and its own claim ceiling states that a reading is a registered, attackable `judge`-role artifact and not a finding, not a merit assessment, and never FW5:628's witness of reason use. Success for this receipt is that the mechanism runs from a config to a closing receipt without a human step, publishes before it dispatches, resumes without re-sending a spent coordinate, and records honestly what it declined to read. It is not that any cell filled.

**Pre-registered before first look, and unchangeable inside this chain.** The cycle budget and `max_calls`; the stopping rule with its guard rails and its five O/P clauses; `obligations.json` with the failed set O and the protected set P, pinned by sha256; the reading set; the seat assignment with families and `key_env`; the audit schedule, `JUDGE_ERR_MAX` and `STREAK_MAX`; the planted-flaw calibration set; the guard parameters including `TRIAL_PARAPHRASE_N` and `schema_repair_budget`; the reopen-reason list; and `CEILING.md`. Changing any of them after first look mints a new `loop_plan_id` and is a new pre-registration, not an amendment to this one.

**Two declared narrowings of published instruments.** First, `use_relation_h005.ROOT_READING_VOCABULARY` is published as a suggestion a row may exceed and root may write outside; this run closes it to six values so the cell is machine-fillable, and routes anything outside to `unresolved:outside-vocabulary` with the text preserved. Second, where that instrument's banner says "the reading is root's", this run's table says the reading is a guarded judge-role artifact and root has not read it. Both narrowings are in the claim ceiling and in the rendered tables.

**Not authorised under this receipt.** Any edit to `src/creib/**`, to `src/minireason/provider.py`, to `src/deepreason_core/**` (including the one-line `ProvenanceRole` addition, which is declined as vendoring drift against `AHepi/DeepReason@9607fba`), to any published occurrence, or to any frozen plan. Any force push, amend, rebase, reset or history rewrite. Any credential written into any file, log, receipt or commit. Any retry of a spent provider call. Any averaging or majority vote over a judge disagreement. Any aggregate, weighted, ranked or summed field over the four registers or over any reading.

**Honest consequence, stated in advance.** The guard is strict enough that this run may return mostly `unresolved` and stop at the no-new-reading-changes clause having resolved little. That is the rule working and is reported as a result about the instrument's reach, never as evidence about the material. A run that reads few rows before the declared ceiling is reported as a resource boundary with the unreached rows named as unreached, never as unresolved by inquiry.

Pending until PREFLIGHT reports planned calls equal to dispatched with zero provider calls, the dry-run acceptance gate is green, and the plan is published and verified.

---

## 2. Seats

Every seat below exists in `src/minireason/data/endpoints.json`. No endpoint and no family
is invented. Key **names** only appear here; no key value appears in this bundle, in the
config, in any record the run writes, or in any commit.

| role | endpoint `name` | `family` | `key_env` | registry `timeout_seconds` | evidence from the published record |
|---|---|---|---|---|---|
| `critic` | `ollama/kimi-k3` | `ollama-cloud/kimi` | `OLLAMA_API_KEY` | 180 | C001 occurrence-01, both arms at `max_tokens` 32768 / `timeout_seconds` 600: 40/40 replicates `COMPLETE`, `unresolved_cells` empty |
| `defender` | `ollama/gemma4-31b` | `ollama-cloud/gemma` | `OLLAMA_API_KEY` | 180 | C001 occurrence-01, both arms at 32768/600: 40/40 `COMPLETE`, `unresolved_cells` empty |
| `judge` 1 | `ollama/gpt-oss-120b` | `ollama-cloud/gpt-oss` | `OLLAMA_API_KEY` | 180 | C001 occurrence-01, both arms at 32768/600: 40/40 `COMPLETE`, `unresolved_cells` empty |
| `judge` 2 | `ollama/qwen3.5-397b` | `ollama-cloud/qwen` | `OLLAMA_API_KEY` | 180 | C001 occurrence-01, both arms at 32768/600: 40/40 `COMPLETE`, `unresolved_cells` empty |
| `variator` | `deepseek-flash` | `deepseek` | `DEEPSEEK_API_KEY` | 180 | C001 occurrence-02, `fcl` arm at 32768/600: 20/20 `COMPLETE`, `unresolved_cells` empty. Its 19 PARTIALs in occurrence-01 were at that occurrence's 8192/180 ceiling — a parameter of that occurrence, not a property of the endpoint, and the record says so rather than ranking the endpoint |
| `marker` | reuses the judge pair | — | — | — | `standard.GUARD_PARAMETERS["marker_reuses_judge_seats"] is True` |

**G0, the constitution, is satisfiable and is asserted before dispatch.** Two judge seats
carry two distinct `family` values (`ollama-cloud/gpt-oss`, `ollama-cloud/qwen`); the
critic's family (`ollama-cloud/kimi`) is in neither; the defender's family
(`ollama-cloud/gemma`) differs from the critic's and is in neither judge family; the
variator's family (`deepseek`) differs from all four. Five distinct families over five
seats — the strictest assignment the registry allows, which is why it was taken.

**`ollama/glm-5.3` was available and was not taken.** Its C001 occurrence-01 `fcl` arm
carried one unresolved cell (19/20) against the other four endpoints' 20/20. That is a
recorded difference between occasions, not a ranking (FW5:849); it is written down here
because a seat choice made on evidence must show the evidence it was made on.

**Cross-family is not independence, and this record does not claim it is.** Four of the
five seats spend `OLLAMA_API_KEY` and are served by one host. Ten `family` labels over 24
endpoints and two credentials is a delivery fact. Family distinctness is the only lever
the registry offers and it is used to the limit; it is never reported as evidential
independence, and agreement between two cross-family seats is agreement between two
conditioned generators.

**Concurrency.** `provider_openai_compat.slots_for` holds five concurrent calls per
`key_env` process-wide; wave capacity is 5 × 2 = 10 and the four Ollama seats share one
gate. The driver imports runner v2 and calls `send_round` in-process rather than shelling
it, because a subprocess gets a fresh `_SLOT_REGISTRY` and silently doubles the ceiling.
`run.lock` refuses a second driver on this run.

**Substituting any seat mints a new `loop_plan_id`** and is a new pre-registration, never
an amendment to this one. No seat is ever compared with another for merit; seats are
occasions, not contestants.

**Seat selection on delivery evidence is a resource decision made once, here, and never
repeated.** The evidence column above is per-endpoint delivery completeness, and the paragraph
about `ollama/glm-5.3` is a difference between occasions written down because a choice made on
evidence must show the evidence it was made on. Under ruling 7 that is a bound on the
**instrument** — whether an endpoint returned complete responses is a delivery fact, not a
reading's standing — and it is not an optimisation target, because nothing inside the run
re-ranks, re-selects or re-compares any seat for any purpose. The precedent this could set is
the danger and not this run, so it is closed in terms: **a seat is never dropped, preferred or
compared for a delivery figure again inside this `loop_plan_id`**, no rendered file carries a
per-endpoint delivery comparison, and a future run that wanted to re-select would be a new
pre-registration doing it in the open (REVIEW-PREREG PR-14).

### 2a. Declared resource conditions

These are **bounds**, declared before the first call, machine-readable in
`reading_set.json:resource_conditions` and asserted by `validate.py` equal to the module constants
that will actually be sent. Design §8 fixes the guard parameters before first look and AGENTS.md
requires the comparison to be respected "under declared information and resource conditions" with
"settings, configurations" preserved; a per-call generation ceiling is such a condition and was
absent from this bundle until this review (REVIEW-PREREG PR-10). They live here and not in
`config.json` because `types.LoopConfig` accepts a closed key set and refuses an unknown one.

| bound | value | owner |
|---|---|---|
| `max_tokens`, per role | critic 2048, defender 1024, judge 2048, marker 1024, variator 4096 | `roles.ROLE_MAX_TOKENS`; the variator's is `seats.paraphrase_n` × `roles.VARIATOR_TOKENS_PER_PARAPHRASE` = 2 × 2048 |
| the wall in force | `min(seat.timeout_seconds, 300)` — **the smaller, never the larger** | `roles.GATEWAY_WALL_SECONDS` = 300; all 24 `endpoints.json` entries declare `timeout_seconds: 180`, so every seat's wall here is **180 s** and the gateway is never reached |
| wall ceiling | `floor(180 × 0.5 × 90)` = 8100 tokens | `roles.GENERATION_SHARE` = 0.5, `roles.OBSERVED_TOKENS_PER_SECOND` = 90 |
| the bound sent | `min(role_budget, wall_ceiling)` — here the role budget in every case | `roles.max_tokens_for`, every term recorded in the call record |
| floor | below `roles.MIN_MAX_TOKENS` = 256 the call is refused `ROLE_TOKEN_BUDGET_UNREACHABLE`, never dispatched to be truncated | `roles` |
| `thinking` | **off where the endpoint honours it**: `False` on the `deepseek`-family seat (the variator, `deepseek-flash`), never sent to any other family | `roles`; the control is DeepSeek's and the transport refuses it elsewhere |
| `temperature`, `seed` | 0.0; seed derived as `sha256(coordinate.token)[:8]`, declared and not a determinism guarantee | `roles` |
| gateway-wall block | a transport or response error at or past 295 s is recorded `PROVIDER_GATEWAY_WALL` under `blocked:provider` | `roles.GATEWAY_WALL_TOLERANCE_SECONDS` = 5 |
| concurrency | five per `key_env` process-wide; four seats share `OLLAMA_API_KEY`, one holds `DEEPSEEK_API_KEY`; wave capacity 5 × 2 = 10 | `provider_openai_compat.slots_for`; `config.max_per_key` = 5 mirrors it and adds no third gate |

**The 300 s wall is a gateway limit of the host, not a one-off** (rulings 13 and 14). Five closes
in a 183 ms band on 2026-09-14, across two families and two client processes, are the evidence:
F002 occurrence-01's `glm-5.3` at 300,270 ms, occurrence-03's at 300,453 ms, and three `kimi-k3`
worker calls closed 300–301 s after their requests. Neither `timeouts.step_seconds` nor any
config key may raise the layer-1 timeout, which stays the endpoint's own declaration and is what
`TIMEOUT_NOT_APPLIED` guards.

**A declared consequence of the ceiling, stated before it happens.** Four of the five seats —
`kimi-k3`, `gemma4-31b`, `gpt-oss-120b`, `qwen3.5-397b` — are reasoning models that receive no
`thinking` control, so reasoning tokens are generated inside a 2048-token judge or critic ceiling
and a 1024-token defender or marker ceiling. The foreseeable failure is a truncated JSON body
refused as `blocked:schema` at `schema_repair_budget` = 0 (ruling 13(c)). That is this run's own
declared budget choice and it is declared **here, before first look, so that it can never later be
read as the instrument declining on the material**: `blocked:schema` on those seats is a resource
fact about this ceiling and is never an absence of relations.

**The seat evidence above does not transfer to these conditions, and is not offered as if it
did.** Every figure in that column was gathered at `max_tokens` 32768 and `timeout_seconds` 600.
This run asks those seats at 1024–4096 tokens inside a 180 s wall. The column is therefore evidence
that these endpoints returned complete responses on a published occasion at a wider ceiling; it is
**not** evidence about delivery at this run's ceiling, and nothing in this bundle treats it as a
prediction. The confound is the one the variator's own row already names in the other direction —
its 19 PARTIALs in C001 occurrence-01 were a parameter of that occurrence, not a property of the
endpoint — and it applies to all five seats here.

### 2b. Publication target, and the declared deviation

`config.publish_ref` is **`origin/claude/project-state-direction-j5rbun`**, set explicitly rather
than left null: publication happens before dispatch at S2, S5, S7 and S14, so the ref is
load-bearing on every cycle, and a null ref makes the target a property of whatever checkout the
run starts in, which is neither repeatable nor resumable elsewhere (REVIEW-PREREG PR-11).

**Declared deviation (ruling 2).** The publication target for this session is the branch
`claude/project-state-direction-j5rbun` **by user mandate**, and not `main`. AGENTS.md's standing
instruction is to publish every completed document to `main`; this run publishes to the mandated
branch instead, every receipt this run writes records that as a deviation, and **publication to
`main` remains pending owner merge**. Nothing in this run merges, force-pushes, amends, rebases or
rewrites history.

---

## 3. The stop rule, as §5 writes it, restated for this run

`obligations.json` is pinned **by two digests of one document, and the record says which is
which** (REVIEW-PREREG PR-02). The **canonical-body digest** is
`3bda592108ac11aee8fe34da5b4317001156d18417af397ee6957f310ce55900`: canonical JSON over the document with its
two self-describing digest keys removed, the value written into
`obligations.json:obligations_sha256`, the value this prose publishes, and the value
`obligations.canonical_pin()` returns. The **file digest** is
`910282bb43de93bd9fdd1498ec279a177fcaee3b815ebdc8e8a6eea4a9179045`: the sha256 of the bytes on disk, the value
`obligations.pin()` returns, and **the one folded into `loop_plan_id`** and re-derived from the
tree by `custody.verify_pins`. They are different values over one document because whitespace and
key order move the file digest and not the canonical one, which is precisely why the identity
carries the file digest and why a record naming one and folding the other would leave a later
reader unable to tell whether the document shifted. Both are fixed before cycle 1 and neither may
shift inside this assessment (FW5:787). `decide.py`'s own
digest is inside `loop_plan_id`. After each cycle `decide()` evaluates every *o* and every
*p* by program against ξ′ (the cycle-end situation) and ξ (the prior), and returns
**exactly one** outcome:

**Guard rails, evaluated before clauses 1–5 and stopping immediately.** A `HALTED` step ⇒
`custody_halt`. Every arm ended ⇒ `all_arms_ended`. A guard-block streak above
`audit.streak_max` = 12 on one role, or a calibration error share above
`audit.judge_err_max` = 0.2, ⇒ `instrument_fault`, which stops the reading arm and Spawns
`audit-the-reader` — a fault in the instrument, never a finding about the material.

**All three guard-rail parameters are settled here and none is provisional.** Two of the accounts
are fields of the frozen config and are therefore inside `loop_plan_id`; a frozen document may not
contain a promise to change itself, and a stop paragraph interpolating the words "to be settled at
pre-registration review" would be a note that the parameter was never accounted for rather than an
account of why the rail fired (REVIEW-PREREG PR-09, §D(2)). In summary, with the full accounts in
`config.json` and `reading_set.json`:

- **`audit.judge_err_max` = 0.2** is a share over the **exercised** `(anchor, seat)` pairs of the
  planted-flaw leg — the five anchor kinds the frozen standard body carries, which is the set
  `audits.build_calibration_set` seeds and the only set the share reads, asked of both judge
  seats, so at most **ten** exercises. The rail fires on *strictly greater*, so with all ten
  exercised two disagreeing exercises give 0.2 and do not fire and three give 0.3 and do: the
  **third**, not the first. The earlier account said "five anchors, so the first anchor a seat
  gets wrong ends the reading arm"; over this denominator that is false and it is withdrawn. The
  share is **panel-level**: one share for the judging panel, never computed per seat, never
  compared between seats, never rendered as a per-endpoint rate (`decide.instrument_bound_crossed`:
  "neither is computed per seat"; FW5:849).
- **`audit.streak_max` = 12** counts consecutive guard blocks **per role, in dispatch order within
  the reading arm, reset by any trial of that role that is not blocked**. Its earlier premise —
  "longer than any block run the C001 and H005 published material produced" — is **withdrawn as
  false**: neither study ran this guard and neither emits a block register, so there is no
  published block run to compare against. Twelve is anchored instead to this bundle's own
  pre-registered set, where a reader can check it: the reading set is 38 cells — 4 baseline mark
  cells costing no call, 12 cross-case mark cells, 22 H005 rows — so twelve consecutive blocks on
  one role is that role declining an unbroken run as long as the **entire cross-case mark leg**, or
  more than half the row leg, without one intervening trial it did not decline.
- **`audit.period` = 2** is a cadence and fires no stop. Two rather than one because a window costs
  46 budgeted calls of a 396-call boundary; two rather than three because at three the only window
  would fall at cycle 3, after the last cycle that could act on it, and an audit nothing can
  respond to is a record rather than a repair. Its account lives in
  `reading_set.json:audit_schedule_declaration` and not in `config.json`, because
  `types.AuditConfig` accepts exactly five keys and refuses an unknown one — so until the clone
  carries a `period_account` field this account is pinned by `reading_set.json`'s sha256 rather
  than by the config block of `loop_plan_id`, and that difference is stated rather than hidden
  (CLONE-PATCH.md item 3).

**Neither rail carries an evidential reading.** Crossing one adjudicates no cell, discharges and
defeats no obligation of O or P, and says nothing about the material. `instrument_fault` names the
instrument. A stopped reading arm is the instrument declining to read.

**One deviation from the design's stop vocabulary, noted rather than left to a diff.**
`types.STOP_REASONS` carries seven tokens — `all_arms_ended`, `custody_halt`, `instrument_fault`,
`no_new_reading_changes`, `obligations_discharged`, `protected_loss`, `resource_boundary` — and
**omits design §4.4's `preregistered_condition:<id>`**. Nothing in this run declares such a
condition and `types.LoopConfig` has no field for one, so the omission is deliberate for L001;
`types.PREREGISTERED_CONDITION_PREFIX` exists and `is_stop_reason` accepts the prefixed form, so a
successor pre-registration that wanted one would declare it and would be a new `loop_plan_id`
(REVIEW-PREREG PR-24).

1. Any *p* that **held at ξ and does not hold at ξ′** ⇒ **STOP `protected_loss`**, the loss
   named and exposed. No continuation, no repair claim. This is FW5:787's conjunct
   `∀r∈P[r(ξ) ⇒ r(ξ′)]` and not the stricter "any *p* not satisfied at ξ′": a protection that
   never held cannot be lost, and reading it strictly would turn a never-held protection into a
   false `protected_loss` at cycle 1 — which is exactly how the old `p7` fired (REVIEW-PREREG
   PR-15, PR-03). `obligations.protected_losses` implements this transition test and nothing
   else, and before cycle 1 there is no prior situation, so the loss register is empty by
   construction. A *p* that became **unreadable** is not a loss: it prints as
   `protected_not_evaluable` beside the register and never terminates the chain (FW5 R5).
2. Else, ≥1 *o* failed at ξ and is satisfied at ξ′, **and** the artifacts making it
   satisfied were registered by this cycle (`ProducedBy` discharged, not temporal
   succession) ⇒ **CONTINUE**.
3. Else, all *o* satisfied ⇒ **STOP `obligations_discharged`**.
4. Else, this cycle's set of `(cell, register, mark)` triples is identical to the previous
   cycle's ⇒ **STOP `no_new_reading_changes`**. This is a **set-identity** test, not a
   count.
5. Else, cycle index equals `cycle_budget` = 3, or `max_calls` = 396 is reached ⇒ **STOP
   `resource_boundary`** — a declared attention-and-spend boundary, never an adjudication
   and never the inquiry running out of things to say.

A mandatory **`losses_outside_P`** section is written every cycle, **present even when
empty** (FW5:802). A cycle may be net withdrawal — more cells moving to `unresolved` than
away from it — and still be recorded as progress if an *o* was discharged, or as no
progress if none was (FW5:810). Every stop carries a mandatory `would_reopen` prose field.
The stop vocabulary carries **no token that would describe a reached boundary as the inquiry
running out of things to say** — `tests/loop/test_types.py` names the forbidden token and
asserts it appears in no vocabulary and in no generated record.

### O — the failed obligations this chain exists to discharge

- **o1** (O) — For every entry of `config.reading_set` beginning `h005-row/` - the 22 rows of the H005 occurrence-01 use-relation table, named one by one in `reading_set.json` - the graph holds either (a) one registered reading artifact `A_reading` whose `cell` is that row key, whose `relation` is a member of `standard.NOMINABLE_RELATIONS`, and whose recorded passage offset was produced by a `resolve_unique` that returned a span lying inside that row's declared referring record, declared target record, or one of its listed `referring_body_passages`; or (b) one registered disposition record for that row key whose `reason` is a member of the closed set {`critic-none`, `unresolved:outside-vocabulary`, a `block_code` that is a member of `types.BLOCK_CODES` (whose members already carry the `blocked:` prefix, so the code is written once and not twice), `NOT_DISPATCHED`, `INDETERMINATE`, `unreached`}.
- **o2** (O) — For every entry of `config.reading_set` beginning `c001-mark/` - the 16 cells of the C001 occurrence-02 `deepseek-flash`/`fcl` mark grid, four comparisons by the four PLAN §8a registers T, E, D, G - the graph holds either (a) one registered mark artifact carrying a `mark` from `standard.MARKS` and, where the mark is `differs`, a `difference_kind` token drawn from `standard.DIFFERENCE_KINDS[<register>]`; or (b) one registered per-register reason record whose `reason` is a member of the closed set {`program-computed`, `baseline-forced-same`, `under-replicated`, `bare-token-ambiguity`, `byte-identity-defeater`, a `block_code` that is a member of `types.BLOCK_CODES` (whose members already carry the `blocked:` prefix, so the code is written once and not twice), `unreached`}. The four registers are recorded separately; no record may carry a combined or reduced mark.
- **o3** (O) — Every registered reading and every registered mark carries a citation that re-resolves: the critic's `passage_quote` q satisfies `M.count(q) == 1` on the recorded resolvable surface M (referring record union target record union listed `referring_body_passages`) and `M.index(q)` maps to a span inside one of those three declared regions; and, for a reading, each judge's `decisive_point` d satisfies `E.count(d) == 1` on `E = case + "\n" + answer` as recorded in that reading's transcript blob. For a mark, the recorded `left_quote` and `right_quote` each re-resolve uniquely on their own side's commitment surface.
- **o4** (O) — Every cell of the reading set whose outcome is a block carries a `block_code` that is a member of `types.BLOCK_CODES`, a `prompt_blob_ref` and a `raw_blob_ref`, and appears in the rendered block register under that code. No cell carries a block without a code, and no rendered file names a block code outside `types.BLOCK_CODES`.
- **o5** (O) — An audit report artifact is in force: some registered `AuditReport` declares that its coverage includes the cycle under evaluation; it names both judge seats of `config.seats.judges` by endpoint name; and it carries a planted-flaw calibration result computed against the calibration rows pinned in `plan.json` at their recorded sha256. Absence of any audit report fails this obligation, which is its state at the opening situation. The cadence that mints records - `audit.period` = 2, phase `n mod period == 0`, so cycle 2 and only cycle 2 inside `cycle_budget` = 3 - is a declared attention-and-spend parameter, recorded in `reading_set.json:audit_schedule_declaration` and reported; it is **not read by this predicate**, which asks what the record declares it covers rather than recomputing the schedule. Discharging o5 is a **repair of the reader and never a repair concerning the material**: it says an audit of the instrument is on record and says nothing whatever about any cell, any relation or any mark. A cycle in which the only obligation discharged is o5 has repaired the instrument and read nothing new, and the cycle record says so in those words, so that 'an obligation was discharged, therefore progress' cannot be read across the two (FW5:785 - an obligation is not automatically appropriate because a participant adopts it; the legitimacy of the purpose can itself be a question).
- **o6** (O) — The within-ORIGINAL baseline for the C001 occurrence-02 juxtaposition exists, was written before any cross-case pack was rendered, and is pinned: a baseline grid artifact covering all four registers is registered, its sha256 is recorded in `plan.json`, and every marker call record for one of the twelve cross-case cells carries that same sha256.
- **o7** (O) — Every one of the 38 declared reading-set cells appears in the rendered record under exactly one of four printed states: a relation or a mark; `unresolved` (a deliberate reading that stays unresolved); `machine-unresolved:<block code>`; or `unread` (never dispatched, named as unreached by spend). No cell appears under two states and none is absent from the rendered record. The ceiling's **three** distinct cell states are the three non-resolved states of this clause - `unresolved`, `machine-unresolved:<block code>` and `unread`; the fourth printed state is the resolved one, a relation or a mark. o7's four and p12's three are therefore one enumeration counted from two ends and not two enumerations, and a reader checking p12 against o7 needs no reconstruction to see it.

### P — the protected obligations; preserved, or the chain stops

- **p1** (P) — The ORIGINAL bytes remain the occurrence's bytes. For the C001 occurrence-02 juxtaposition, each of the five ORIGINAL replicates' `public_text_sha256` and `commitments_sha256` in the published `comparison.json` equal the values pinned at PREREGISTER; and the sha256 of `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/material.json` equals `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927`. That file carries no `material_sha256` field - its top-level keys are `schema`, `system`, `prose_instruction`, `formal_instruction`, `bare_instruction`, `problems`, `templates` and `source_pins` - so the value is the digest of the file and is named as such.
- **p2** (P) — The recoding correspondence table stays complete and published before dispatch: `experiments/diagnostics/C001-contrast-triple/occurrence-02/RECODING_TABLE.md` and `experiments/diagnostics/C001-contrast-triple/RECODING_TABLE.md` are present at their pinned sha256, and every recoded unit named in the occurrence's `material.json` has a correspondence row in it.
- **p3** (P) — No case's request differs outside the objection block. Re-running C001's own envelope check over the occurrence's published request records raises neither `SHARED_ENVELOPE_MISMATCH` nor `ORIGINAL_CASE_NOT_THE_OCCURRENCE_BYTES` (PLAN §8 F4).
- **p4** (P) — No scoring key appears anywhere. `contracts.assert_no_scoring_keys` over every artifact the run registers, every table header and every file rendered under the run root returns no hit, and `SCORING_KEY_FORBIDDEN` is never suppressed. Two surfaces are read, and only what the loop itself wrote: the **keys** of every registered record, which is what a scoring key is when it is a field; and the **headings and table header rows** of every file named by the run's `rendered_files` record, which is what a scoring key is when it is a column. **Quoted passages of the material are exempt**: the material is a published record this run may not edit, so refusing a run because a passage it quotes carries a forbidden word would be the loop editing its own evidence, which is the boundary `graph.G12_EXEMPT` draws. The exemption narrows nothing in the first conjunct - a heading or a header row the loop wrote is scanned whether or not it quotes - and the witness list names the offending file and the tokens found in it.
- **p5** (P) — Provider and study records stay write-once with no replay. Every coordinate under `experiments/loops/L001-loop-first-live-2026-09-14/readings/` has at most one response record; no request, attempt or response file is ever rewritten; `NO_REPLAY` is never bypassed and no retry of a spent call is issued.
- **p6** (P) — No reading is averaged or majority-voted. No registered artifact and no rendered file carries a mean, median, majority, weighted, summed, ranked or otherwise aggregated field over rulings or marks; every judge split is recorded as `blocked:ensemble-split` with both rulings verbatim and leaves the cell unresolved.
- **p7** (P) — No reading mints an `att` edge on any node under study, and no node under study is the source of any edge. Two conjuncts, and they are not the same prohibition: the set of `att` edges whose target is an `E_row` or `E_cell` material artifact is empty; and the set of edges - `att` or `dep` - whose **source** is such an artifact is empty. Every reading's attack targets its own `C_open`. A reading's `dependence` ref onto its own `E_row`/`E_cell` is **required** by design 3(d) and is not an edge on a node under study in the sense this clause protects: it is exactly what makes an invalidated or re-imported material leave the reading `suspended_unsupported` rather than refuted - orphaned is not false. A declared `rejects-with-reason` relation creates no attack edge and a declared `re-deploys` relation creates no support edge.
- **p8** (P) — The appellate remains optional: no step's status depends on the presence of a file under `experiments/loops/L001-loop-first-live-2026-09-14/appeals/`, and a run whose appeals directory is empty reaches CLOSE and renders `appellate_rulings: 0` with the not-validated sentence.
- **p9** (P) — The baseline of every marked cell is still at the sha256 pinned in its call records: recomputing the baseline artifact's digest at cycle end reproduces the value every cross-case call record carries.
- **p10** (P) — Every C001 cell that is unresolved in the published record remains unresolved unless a guarded reading attacks it. For each of the 78 empty `root_reading` cells and the 208 empty register-mark cells across `experiments/diagnostics/C001-contrast-triple/occurrence-01/comparison.json` and `experiments/diagnostics/C001-contrast-triple/occurrence-02/comparison.json`, the corresponding `C_open` artifact carries the adjudicated label `accepted` - which means *unresolved* - unless there exists a registered warrant against that exact `C_open` which passed the whole guard G0-G12 and whose transcript conforms. In particular no published byte is edited: the published grids stay empty and the loop's readings live beside them.
- **p11** (P) — Nothing published is written. No file under `experiments/diagnostics/**` or `experiments/analyses/**` is created, modified, renamed or deleted by the run; the run writes only under `experiments/loops/L001-loop-first-live-2026-09-14/` plus append-only additions to `docs/DECISION_LEDGER.md` and the repo activity log.
- **p12** (P) — The claim ceiling is present and the three cell states are never collapsed. Every rendered table and the closing record contain each sentence of `standard.CEILING_REQUIRED_SENTENCES` verbatim and the ceiling body at its pinned sha256; and no rendered file describes an `unread` or a `machine-unresolved` cell as unresolved by inquiry, and no rendered file carries the one forbidden stop-vocabulary token outside the ceiling's own denial clause.

**Where a `blocked:constitution` outcome is printed.** The frozen ceiling below enumerates
**nine** bare reason codes in its block-register clause, and `types.BLOCK_CODES` has **ten**: the
tenth is `blocked:constitution`, the G0 outcome when the seat constitution is unsatisfiable and the
coordinates are `NOT_DISPATCHED` with an operational reason. The ceiling text is frozen and is not
edited here, so the reconciliation is stated beside it instead: **the rendered block register
prints ten rows, not nine** — `report.BLOCK_REGISTER_HEADINGS` is the ceiling's nine in the
ceiling's own order plus `constitution` as the tenth — so a constitution block has a printed home
under o4, and the non-evaluability channel FW5:688 requires kept open is kept open. *The inability
to evaluate a proposition is not a falsifying observation of the proposition* (FW5:688): a
constitution block is an operational reason and an operational reason is never a semantic result
(REVIEW-PREREG PR-12).

**The pinned calibration set extends the standard's anchor kinds, and the consequence is
declared.** `calibration.json` pins **nine** rows; the frozen standard body carries **five** anchor
kinds, and `audits.build_calibration_set` seeds the planted-flaw set from those five and from
nothing else. Rows cal-01 to cal-05 mirror the five. Rows cal-06 to cal-09 —
`fabricated-decisive-point`, `duplicated-passage-non-unique-offset`, `order-swap-sensitive-pair`,
`paraphrase-invariant-pair` — are guard probes and audit-arm exemplars the standard body does not
carry. They are therefore **not reachable by the case-law closure** that collapses every ν citing
`std:reading-rubric/v1`; they are pinned by `calibration.json`'s own sha256, recorded in
`plan.json`, and are attacked through that pin. They are deliberately not added to the standard
body, because adding them would move `standard.STANDARD_BODY_SHA256` and every pin derived from it
and no clone edit is authorised at this point of the recomputation order. None of the four enters
the `judge_err_max` share: cal-06 and cal-07 are program checks the guard must decline, and cal-08
and cal-09 register their disagreements as hits under the order-swap and paraphrase-invariance
audit arms (REVIEW-PREREG PR-21).

**No clause is a count.** Every clause above is a universal or existential over a fixed,
pre-registered, named key set; a set-membership test against a closed vocabulary; a byte
or digest equality; a uniqueness predicate (`str.count(q) == 1`); a span-containment test;
an emptiness assertion on a set defined by kind; a verbatim substring presence; or a
recency comparison on a cycle index. No clause reads a quantity of readings, marks,
agreeing endpoints, `differs` marks, blocks, rows resolved or calls spent, and none
compares such a quantity against a threshold.

---

## 4. The claim ceiling, verbatim — with the symbols it is written against

The text below is `standard.CEILING_TEXT` byte-for-byte. It is frozen into the
pre-registration, its sha256 is pinned into `loop_plan_id`, and `report.py` refuses to
emit any table or any report without it.

### 4a. The pins these words resolve to

Until this review no bundle file named any of them, so the ceiling's "the narrowing is part of the
claim" named a narrowing a later reader could not check against the record (REVIEW-PREREG PR-25).
These three live in the implementation clone, not in the bundle, and the clone is still moving:

| pin | value as read at this review | status |
|---|---|---|
| `standard.STANDARD_BODY_SHA256` | `a9007dc73c748cfff974a1a3d77098d380ec153b1b8cf93f513cafa3ea0572d7` | **to be re-read at PREFLIGHT after the clone freezes** |
| `standard.CEILING_SHA256` | `1e26be087483fd1b9c8e2c403cfae646fb07ebc773f23434a0c4dfab3ed04c1e` | **to be re-read at PREFLIGHT after the clone freezes** (unmoved across the wave-2 and wave-3 edits that moved the body) |
| `audits.CALIBRATION_EXCHANGES_SHA256` | `91c29e1e71719d815c21c2697f4aa68a7c983be21df945ad6b1e5042183981e5` | **to be re-read at PREFLIGHT after the clone freezes** — the five constructed anchor exchanges. Design §2.1 says the standard carries "anchor exemplars" but `standard.CalibrationAnchor` carries a construction and a ground-truth reason and **no exchange bytes**, so the ground-truth bytes are pinned separately here rather than moving the standard body a further time; `plan.json` must pin this digest as well |

`loop_plan_id` is minted at S0 over all of them plus the six `types.PINNED_SOURCE_PATHS`,
`CEILING.md`, every prompt template, `obligations.json` and each attached study's `PLAN.md` and
`material.json`. If `STANDARD_BODY_SHA256` moves between the freeze and S0, the plan identity is
for a body that no longer exists and `PLAN_ID_MISMATCH` on the next resume is the good outcome.

### 4b. The narrowed vocabularies, enumerated

Reproduced from the module constants, printed here for a human reader, mirrored machine-readably in
`reading_set.json:vocabularies`, and asserted equal to those constants by `validate.py`:

- **the six reading values** (`standard.READING_VOCABULARY`, byte-identical to
  `use_relation_h005.ROOT_READING_VOCABULARY`): `re-deploys`, `qualifies`, `rejects-with-reason`, `repairs`, `retains`, `unresolved`. The first
  five are `standard.NOMINABLE_RELATIONS`, the relations a critic may name; `unresolved` is the
  sixth. A critic's `none` is an **answer**, not a member of the vocabulary. This is the first of
  the two declared narrowings: the published instrument offers the list as a suggestion a row may
  exceed and root may write outside, and this run closes it, routing anything outside to
  `unresolved:outside-vocabulary` with the text preserved.
- **the three marks** (`standard.MARKS`): `differs`, `same`, `unresolved`.
- **the closed `difference_kind` sets, per register** (`standard.DIFFERENCE_KINDS`) — a `differs`
  mark must carry a token from its own register's set and from no other's, and the four registers
  are never summed: **T** `target_set_membership`, `target_prefix_source`; **E** `record_engaged`, `engagement_form`; **D** `disposition_value`, `disposition_carrier_field`; **G** `grounds_source`.
- **the ten block codes** (`types.BLOCK_CODES`): `blocked:baseline-forced-same`, `blocked:constitution`, `blocked:ensemble-split`, `blocked:operative-target`, `blocked:order-swap`, `blocked:outside-vocabulary`, `blocked:paraphrase-flip`, `blocked:provider`, `blocked:referential-integrity`, `blocked:schema`.
  The ceiling's clause names the nine bare reasons of `types.CEILING_BLOCK_REASONS`; the rendered
  register prints those nine plus `constitution`, as §3 records.
- **the four printed cell states** (`obligations.CELL_STATES`): `read`, `unresolved`, `machine-unresolved`, `unread` — the
  resolved one and the ceiling's three.
- **the three reopen reasons** (`standard.REOPEN_REASONS`): `new-material`, `repaired-guard`, `appellate-ruling`.
- **the five calibration anchor kinds the standard body carries**:
  `self-juxtaposition`, `no-shared-reference`, `quotes-and-rejects`, `clean-control-lexical-overlap-only`, `clean-control-framing-only-passage`.

---

**What this run claims.** Under registered standard `std:reading-rubric/v1` (digest …), a cross-family judge ensemble unanimously sustained relation *r* for this cell, citing a passage that resolves by program to a unique byte offset [s,e) inside the declared referring record, target record or listed body passage; the ruling survived order-swap and *N* meaning-preserving paraphrases of the exchange; the seats' audit record at ruling time was *A*. The reading is a registered, attackable artifact of `provenance.role = critic` carrying the literal role name `judge`, and it falls automatically if the standard, the evidence, or the seats' reliability is successfully attacked.

**This run cannot claim FW5:628's witness of reason use.** A transcript supplies no structural map from the represented objection organization into a response suborganization preserving internal role bindings on an active dependency route, and neither does an ensemble of readers of that transcript. The strongest positive outcome available is *consistent-with*.

**A null on the recoding or the carrier leg leaves those rival explanations unrefuted and unsupported, not excluded.** At N = 5 this is a limit of the design, not a finding.

**Agreement between two cross-family readers is agreement between two conditioned generators, not corroboration by two independent observers.** The guard measures behavioural stability under paraphrase, order and adversarial answer — not truth. Ten `family` labels over 24 endpoints and two credentials is a delivery fact, not an independence proof.

**An unresolved cell proves neither presence nor absence** (FW5:634). Ended arms, guard blocks, PARTIAL deliveries, bare-token ambiguity and under-replication are silent about content; non-evaluability is not refutation.

**Three cell states are distinct and are printed as three things.** An *unread* cell is one nobody and nothing has read. An *unresolved* cell is a deliberate reading that stays unresolved. A *machine-unresolved* cell is one the guard declined to resolve, and it names the block code that declined it. Conflating any two would let an unfinished worksheet read as a finding.

**A high block rate is the instrument declining to read. It is never an absence of relations.** The block register by reason code — `ensemble-split`, `referential-integrity`, `operative-target`, `order-swap`, `paraphrase-flip`, `outside-vocabulary`, `schema`, `provider`, `baseline-forced-same` — is printed with counts on every table.

**No count is an automatic warrant** (FW5:851). Marks are reported per register and are never summed, averaged, weighted or ranked. Endpoints are independent occasions to look for one pattern, never competitors (FW5:849).

**A reached ceiling is a declared resource boundary, not exhaustion of the inquiry**, and this record states which was reached and what would reopen the question.

**`appellate_rulings: N`.** Where N = 0, this record does not describe the run as validated, checked or confirmed. That the loop ran without a human is a fact about the loop, not a fact about the readings.

**Two published instruments were narrowed to make these cells machine-fillable, and the narrowing is part of the claim.** `ROOT_READING_VOCABULARY` is published as a suggestion that a row may exceed and that root may write outside; this run closes it to six values and routes anything outside to `unresolved:outside-vocabulary` with the text preserved. And where the published instrument says "the reading is root's", this table says the reading is a guarded `judge`-role artifact and **root has not read it**.

**What would reopen this:** an appellate ruling; a successful attack on `std:reading-rubric/v1` or on a register definition, which collapses every ν citing it in pass 1; a custody correction; a third judge family; more replicates; a raised budget under a new `loop_plan_id`.

---

## 5. What would reopen this

- an appellate ruling committed under `experiments/loops/L001-loop-first-live-2026-09-14/appeals/`, ingested at the top of the next cycle, ranked first in every subsequent judge pack, and itself attackable;
- a successful attack on `std:reading-rubric/v1`, which collapses every ν citing it through the case-law closure in adjudication pass 1, so every reading falls and every cell reinstates — computed, not curated;
- a successful attack on any one of the four PLAN §8a register definitions, or on a register's closed `difference_kind` set;
- a custody correction or a re-import of `E_row`/`E_cell` at a different grain, which leaves the readings `suspended_unsupported` rather than refuted — orphaned is not false;
- a third judge family, which is available in the registry and was not taken inside this budget;
- more replicates, or the twelve C001 occurrence-01 juxtapositions this run names `unread`;
- a raised `cycle_budget` or `max_calls`, which is a new `loop_plan_id` and a new pre-registration, never an amendment;
- a `reopen_reason` from the pre-registered list — `new-material`, `repaired-guard`, `appellate-ruling` — which is the only thing that lets an `unresolved` cell be read again at all; G11 enforces this by refusing the write, not by convention.

---

## 6. Honest expectation, stated in advance

**This run may resolve very little, and that is the instrument's reach, not evidence about
the material.** The guard is strict by design and every one of its refusals costs cells.
G2 requires a citation that resolves by `str.count == 1` to a unique byte offset; G3 voids
any span that lands in the pack's own scaffolding; G5 blocks on any split between the two
judge seats rather than voting; G6 blocks on any order-swap flip; G7 blocks on any
paraphrase flip; G4 routes anything outside the six-value vocabulary to
`unresolved:outside-vocabulary`. A high block rate is the instrument declining to read. It
is never an absence of relations, and the block register prints each refusal under its own
reason code with counts so that the declining is visible rather than inferred.

The most likely shape of this run, written down before it happens so that it cannot be
narrated as a success afterwards: cycle 1 reads the reading set and discharges some of
o1–o4 and o6; cycle 2 runs the one audit window and discharges o5 by its own artifacts;
cycle 3 has nothing new to read — G11 forbids re-reading an `unresolved` cell without a
`reopen_reason` — so the mark-triple set is identical to cycle 2's. A table that is mostly
`unresolved` and `machine-unresolved` at the end of that is the rule working.

**Which clause is most likely to fire at cycle 3, and what separates it from the other.** The
earlier draft of this paragraph predicted clause 4, `no_new_reading_changes`. That prediction is
corrected here (REVIEW-PREREG PR-19): **clause 3, `obligations_discharged`, is the more likely
stop**, because clause 3 is evaluated *before* clause 4 and because o1, o2, o3, o4, o6 and o7 are
all satisfiable by **recorded reasons** — a `critic-none`, a block code, an `unreached`, a
per-register `program-computed` — and not only by filled cells. If every declared cell carries
either an outcome or a legal recorded reason at the end of cycle 1, and o5 is discharged by the
cycle-2 audit window, then every *o* is satisfied at cycle 3 and clause 3 fires first. Clause 4 is
the live alternative and fires only if at least one *o* is still unsatisfied at cycle 3 — the
readable case being an `INDETERMINATE` coordinate (a request or attempt with no response) that o1
admits as a reason only where it is recorded as one, or a rendered-record gap under o7 — while the
triple set has stopped moving. Both clauses are named here so that whichever fires is the one this
document predicted, and **neither is a result about the material**: clause 3 says the repair
conditions this chain declared are all answered, most of them by recorded refusals to read; clause
4 says the instrument has stopped producing new marks. A stop under either is compatible with a
table in which almost nothing was read.

**`obligations_discharged` at cycle 3 would not mean the run learned anything, and o5 is the
clearest case.** o5 is an obligation about the **instrument** — that an audit record is in force —
and it is discharged by the loop's own audit artifacts, so cycle 2 can always manufacture that
CONTINUE independently of anything read. That is legitimate: the audit genuinely is a repair, and
the design wants the instrument under repair. But it is a **repair of the reader and never a repair
concerning the material** (FW5:785 — an obligation is not automatically appropriate because a
participant adopts it, and the legitimacy of the purpose can itself be a question). The cycle
record says so in those words, so that "an obligation was discharged, therefore progress" cannot be
read across from the instrument to the material (REVIEW-PREREG PR-16).

**The C001 contrast leg's shape is largely fixed before any call, and that is stated in advance
rather than discovered afterwards** (REVIEW-PREREG PR-20). Four guards decide most of that leg
without a model: G10(d) program-computes the T and D marks on the FCL arm wherever the parse
succeeds and **calls no judge at all**; G9 forces a `differs` to `same` wherever the mark's
`difference_kind` token is already present in the frozen within-ORIGINAL baseline's kind set for
that register; G10(c) forces register E to `unresolved` on any row whose reference is a bare id
token shared with the account document; and `standard.FALSIFIER_MAP` excludes G from D1, F2 and F3
alike, so G is residue that carries no falsifier. An offline program pass over the published
occurrence-02 bytes, recorded as wave-1 integration decision 53, reported that shape: the T and D
kind-rows G9-forced to `same`, no admissible program `differs`, E forced by shared bare tokens on
several rows, G prose-only. **Its figures are not re-asserted here**: occurrence-02 was published
after the implementation clone was cut, that pass is not reproducible inside the clone, and the
first run must recompute them from the published bytes rather than inherit them. What is
pre-registered is the reading of whatever it recomputes. A `same` written by G9 is the
replicate-baseline rule firing and is **not a reading that the cases do not differ**. An
`unresolved` written by G10(c) is bare-token ambiguity and is **absent data, never an absence of
difference**. A leg that returns no admissible `differs` at all is a fact about the guard's own
pre-emption rules at N = 5 replicates, and leaves the recoding and carrier rivals **unrefuted and
unsupported, not excluded**. None of it is evidence about C001's material, and no rendered file may
present it as such.

**The three cell states are printed as three things and must not be conflated.** The
**twelve** C001 occurrence-01 juxtapositions and everything past the declared boundary are
**unread** — unreached by spend. Twelve, recounted from the published bytes at this review:
`experiments/diagnostics/C001-contrast-triple/occurrence-01/comparison.json` carries twelve
entries in its `tables` array — six endpoint slugs (`deepseek-flash`, `ollama-gemma4-31b`,
`ollama-glm-5.3`, `ollama-gpt-oss-120b`, `ollama-kimi-k3`, `ollama-qwen3.5-397b`) by two arms
(`fcl`, `prose`), twelve distinct `(endpoint_slug, arm)` pairs and no repeats — against
occurrence-02's single `deepseek-flash`/`fcl` table, which is the one this run reads. The earlier
"eleven" counted the eleven that remain after setting aside the `deepseek-flash`/`fcl`
juxtaposition G10(b) pre-empts, and that is not the unread inventory: a pre-empted juxtaposition
this run never reads is unread too. The trichotomy clause of the claim ceiling rests on this
inventory being complete, so it is counted here and the count is shown (REVIEW-PREREG PR-13). A cell the guard declined is **machine-unresolved** and
carries the block code that declined it. A cell a guarded trial left open is
**unresolved**. Rendering any of the first two as unresolved-by-inquiry would let an
unfinished worksheet read as a finding, and `report.py` refuses to.

**This run tests no clause of Account (𝓔), and is not a partial run of A001.** Nothing in
this bundle references `Account(𝓔)`, anchoring, fidelity, question fidelity, non-circular
dependence or non-vacuity, and that absence is deliberate rather than an oversight: the FW5
Account sufficiency-or-necessity challenge is a **separately identified study** (ruling 9(b),
staged as A001) with its own claim, dependencies, grain, boundary, contrasts and relinquishment
fixed before evidence, and the design's own non-goals include establishing an `Account` predicate.
Nothing L001 produces bears on A001, no outcome of this run may be cited for or against any Account
condition, and a reader of the published run should take this sentence as the record saying so
(REVIEW-PREREG PR-17).

**Success for this pre-registration is not that any cell filled.** It is that the
mechanism ran from this config to a closing receipt with no human step, published before
it dispatched, resumed without re-sending a spent coordinate, and recorded honestly what
it declined to read. A green run says the loop works. It says nothing whatever about
whether a reading the loop produced is any good, and with `appellate_rulings: 0` this
record does not describe itself as validated, checked or confirmed. That the loop ran
without a human is a fact about the loop, not a fact about the readings.

---

## 7. What was changed at this pre-registration review, and why it is named

Every edit below was made **at** the pre-registration review of 2026-09-14, **before** S0
PREREGISTER and before any provider call, against `REVIEW-PREREG.md`. None was made silently, and
none may be made again: after S0 each of them mints a new `loop_plan_id` and is a new
pre-registration, never an amendment to this one. The full record, item by item with the bytes
replaced, is `CHANGES-PREREG.md`; the clone-side half is `CLONE-PATCH.md`.

Two of them change a clause of a document whose digest enters the plan identity, and the review
required both to be named here rather than applied quietly:

- **`p7` was rewritten** from "no reading mints an `att` or `dep` edge on any node under study …
  the set of `att` and `dep` edges whose target is an `E_row` or `E_cell` material artifact is
  empty" to the two-conjunct form the implementation evaluates: no `att` edge may target a node
  under study, and no node under study may be the **source** of any edge. The old sentence forbade
  the `dependence` ref from `A_reading` to `E_row` that design §3(d) **mandates**, so the loop's
  first correct registration would have failed a protected obligation; it was also silent about
  edges whose source is a studied node, which the new form refuses. **This differs from design §5's
  compressed sentence** — §5 writes "no `att` or `dep` edge on any node under study" where §3
  writes the precise "no `dep` edge *between* studied nodes" — and the difference is recorded here
  because the design is the document of record. The protection is not weakened: both directions
  that could hide a change to the material are refused.
- **`o5` was rewritten** from the recency comparison `current_cycle - n < audit.period` to the
  coverage-declaration membership test `audit_in_force` evaluates, keeping the bundle's two genuine
  strengthenings (both judge seats named by endpoint name; a planted-flaw result against the pinned
  rows) and keeping the cadence declared in the bundle and reported rather than read by the
  predicate. A pre-registration fixes O by its text and the run discharges O by its program; where
  they differed, nothing was fixed.

The remaining edits, in one line each: the forbidden `scoring` key in `calibration.json` renamed to
`error_rule`, with the rule stated in prose and `assert_no_scoring_keys` added to `validate.py`
(PR-01); both obligations digests published and attributed (PR-02); `p4` given the
quoted-material exemption so its prose and its predicate are one obligation (PR-05); `cal-01`
rebuilt with the referring region alone (PR-06); `validate.py` given all six
`types.PINNED_SOURCE_PATHS` (PR-07); `VALIDATION.md` regenerated wholesale rather than patched
(PR-08); both guard-rail accounts settled and a third written for `audit.period`, with one false
premise withdrawn and one wrong denominator corrected (PR-09); the resource conditions declared as
bounds in §2a (PR-10); `publish_ref` set explicitly with the ruling-2 deviation paragraph in §2b
(PR-11); the block-code spelling reconciled in `o1` and `o2` and `blocked:constitution` given its
printed home (PR-12); the unread inventory recounted from the published bytes, eleven to twelve
(PR-13); the seat-selection sentence added (PR-14); clause 1 stated once in FW5's held-then-failed
form (PR-15); o5's discharge named a repair of the reader (PR-16); the Account (𝓔) non-goal stated
(PR-17); the live receipt id replaced by an impossible placeholder (PR-18); the predicted stop
clause corrected to clause 3 with clause 4 named as the live alternative (PR-19); the C001 leg's
known-in-advance shape carried without asserting its figures (PR-20); the four extra calibration
anchors declared as pinned by the bundle rather than by the standard body (PR-21); `p1`'s file
digest named as a file digest (PR-22); `o7` given the clause that reconciles its four states with
p12's three (PR-23); the `preregistered_condition:<id>` omission noted (PR-24); and the six values,
three marks, per-register difference-kind sets and block codes enumerated in §4b beside
`STANDARD_BODY_SHA256` (PR-25).

**Nothing in this bundle mints an identifier.** The receipt id, its timestamp and the
`loop_plan_id` are placeholders and are minted at S0: `receipts.open_preregistration` mints the
receipt id under the ledger append lock, and the plan identity is computed over the resolved config
and the frozen pins and written into `plan.json` before the first call.
