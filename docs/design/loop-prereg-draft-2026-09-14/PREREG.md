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
| `VALIDATION.md` | the exact validation commands and their output |

---

## 1. The receipt paragraph (design §8, rendered)

The text below is `receipts.render_preregistration` output and contains every sentence of
`receipts.PREREGISTRATION_REQUIRED_SENTENCES` verbatim — the renderer refuses to return a
text that does not. **The receipt id and the timestamp shown are placeholders.**
`receipts.open_preregistration` mints the real `REC-<YYYYMMDD>-<X>` under the ledger
append lock at S0, and the appended bytes differ from these only in that id and that
stamp. The `loop_plan_id` sentence is likewise absent here because the plan identity
cannot be computed until `CEILING.md`, the `STD_READING` body and the prompt templates
exist as files to pin; it is
`sha256(canonical({"schema": "minireason.loop.plan-id.v1", "config": <this config,
fully resolved>, "pins": <path -> sha256>}))` and is written into `plan.json` and
published before the first call.

---

**REC-20260914-Z opened at 2026-09-14T00:00:00Z: pre-register the automated end-to-end harness loop as a mechanism intervention with its own identity.**

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

---

## 3. The stop rule, as §5 writes it, restated for this run

`obligations.json` is pinned at sha256
`713119a7cd255296058b18084a40cbac7a3353903bbf8cd260b6e78c173e4302`
before cycle 1 and may not shift inside this assessment (FW5:787). `decide.py`'s own
digest is inside `loop_plan_id`. After each cycle `decide()` evaluates every *o* and every
*p* by program against ξ′ (the cycle-end situation) and ξ (the prior), and returns
**exactly one** outcome:

**Guard rails, evaluated before clauses 1–5 and stopping immediately.** A `HALTED` step ⇒
`custody_halt`. Every arm ended ⇒ `all_arms_ended`. A guard-block streak above
`audit.streak_max` = 12 on one role, or a calibration error rate above
`audit.judge_err_max` = 0.2, ⇒ `instrument_fault`, which stops the reading arm and Spawns
`audit-the-reader` — a fault in the instrument, never a finding about the material.

1. Any *p* fails ⇒ **STOP `protected_loss`**, the loss named and exposed. No continuation,
   no repair claim.
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

- **o1** (O) — For every entry of `config.reading_set` beginning `h005-row/` - the 22 rows of the H005 occurrence-01 use-relation table, named one by one in `reading_set.json` - the graph holds either (a) one registered reading artifact `A_reading` whose `cell` is that row key, whose `relation` is a member of `standard.NOMINABLE_RELATIONS`, and whose recorded passage offset was produced by a `resolve_unique` that returned a span lying inside that row's declared referring record, declared target record, or one of its listed `referring_body_passages`; or (b) one registered disposition record for that row key whose `reason` is a member of the closed set {`critic-none`, `unresolved:outside-vocabulary`, `blocked:<code>` for a `code` in `types.BLOCK_CODES`, `NOT_DISPATCHED`, `INDETERMINATE`, `unreached`}.
- **o2** (O) — For every entry of `config.reading_set` beginning `c001-mark/` - the 16 cells of the C001 occurrence-02 `deepseek-flash`/`fcl` mark grid, four comparisons by the four PLAN §8a registers T, E, D, G - the graph holds either (a) one registered mark artifact carrying a `mark` from `standard.MARKS` and, where the mark is `differs`, a `difference_kind` token drawn from `standard.DIFFERENCE_KINDS[<register>]`; or (b) one registered per-register reason record whose `reason` is a member of the closed set {`program-computed`, `baseline-forced-same`, `under-replicated`, `bare-token-ambiguity`, `byte-identity-defeater`, `blocked:<code>` for a `code` in `types.BLOCK_CODES`, `unreached`}. The four registers are recorded separately; no record may carry a combined or reduced mark.
- **o3** (O) — Every registered reading and every registered mark carries a citation that re-resolves: the critic's `passage_quote` q satisfies `M.count(q) == 1` on the recorded resolvable surface M (referring record union target record union listed `referring_body_passages`) and `M.index(q)` maps to a span inside one of those three declared regions; and, for a reading, each judge's `decisive_point` d satisfies `E.count(d) == 1` on `E = case + "\n" + answer` as recorded in that reading's transcript blob. For a mark, the recorded `left_quote` and `right_quote` each re-resolve uniquely on their own side's commitment surface.
- **o4** (O) — Every cell of the reading set whose outcome is a block carries a `block_code` that is a member of `types.BLOCK_CODES`, a `prompt_blob_ref` and a `raw_blob_ref`, and appears in the rendered block register under that code. No cell carries a block without a code, and no rendered file names a block code outside `types.BLOCK_CODES`.
- **o5** (O) — An audit report artifact is in force: one registered `AuditReport` whose `cycle` index n satisfies `current_cycle - n < audit.period` (= 2 for this run), which covers both judge seats named in `config.seats.judges` by endpoint name, and which carries a planted-flaw calibration result computed against the nine calibration rows pinned in `calibration.json` at the sha256 recorded in `plan.json`.
- **o6** (O) — The within-ORIGINAL baseline for the C001 occurrence-02 juxtaposition exists, was written before any cross-case pack was rendered, and is pinned: a baseline grid artifact covering all four registers is registered, its sha256 is recorded in `plan.json`, and every marker call record for one of the twelve cross-case cells carries that same sha256.
- **o7** (O) — Every one of the 38 declared reading-set cells appears in the rendered record under exactly one of four printed states: a relation or a mark; `unresolved` (a deliberate reading that stays unresolved); `machine-unresolved:<block code>`; or `unread` (never dispatched, named as unreached by spend). No cell appears under two states and none is absent from the rendered record.

### P — the protected obligations; preserved, or the chain stops

- **p1** (P) — The ORIGINAL bytes remain the occurrence's bytes. For the C001 occurrence-02 juxtaposition, each of the five ORIGINAL replicates' `public_text_sha256` and `commitments_sha256` in the published `comparison.json` equal the values pinned at PREREGISTER; and the H005 occurrence-01 `material_sha256` equals `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927`.
- **p2** (P) — The recoding correspondence table stays complete and published before dispatch: `experiments/diagnostics/C001-contrast-triple/occurrence-02/RECODING_TABLE.md` and `experiments/diagnostics/C001-contrast-triple/RECODING_TABLE.md` are present at their pinned sha256, and every recoded unit named in the occurrence's `material.json` has a correspondence row in it.
- **p3** (P) — No case's request differs outside the objection block. Re-running C001's own envelope check over the occurrence's published request records raises neither `SHARED_ENVELOPE_MISMATCH` nor `ORIGINAL_CASE_NOT_THE_OCCURRENCE_BYTES` (PLAN §8 F4).
- **p4** (P) — No scoring key appears anywhere. `contracts.assert_no_scoring_keys` over every artifact the run registers, every table header and every file rendered under the run root returns no hit, and `SCORING_KEY_FORBIDDEN` is never suppressed.
- **p5** (P) — Provider and study records stay write-once with no replay. Every coordinate under `experiments/loops/L001-loop-first-live-2026-09-14/readings/` has at most one response record; no request, attempt or response file is ever rewritten; `NO_REPLAY` is never bypassed and no retry of a spent call is issued.
- **p6** (P) — No reading is averaged or majority-voted. No registered artifact and no rendered file carries a mean, median, majority, weighted, summed, ranked or otherwise aggregated field over rulings or marks; every judge split is recorded as `blocked:ensemble-split` with both rulings verbatim and leaves the cell unresolved.
- **p7** (P) — No reading mints an `att` or `dep` edge on any node under study. The set of `att` and `dep` edges whose target is an `E_row` or `E_cell` material artifact is empty; every reading's attack targets its own `C_open`, and a declared `rejects-with-reason` relation creates no attack edge while a `re-deploys` relation creates no support edge.
- **p8** (P) — The appellate remains optional: no step's status depends on the presence of a file under `experiments/loops/L001-loop-first-live-2026-09-14/appeals/`, and a run whose appeals directory is empty reaches CLOSE and renders `appellate_rulings: 0` with the not-validated sentence.
- **p9** (P) — The baseline of every marked cell is still at the sha256 pinned in its call records: recomputing the baseline artifact's digest at cycle end reproduces the value every cross-case call record carries.
- **p10** (P) — Every C001 cell that is unresolved in the published record remains unresolved unless a guarded reading attacks it. For each of the 78 empty `root_reading` cells and the 208 empty register-mark cells across `experiments/diagnostics/C001-contrast-triple/occurrence-01/comparison.json` and `experiments/diagnostics/C001-contrast-triple/occurrence-02/comparison.json`, the corresponding `C_open` artifact carries the adjudicated label `accepted` - which means *unresolved* - unless there exists a registered warrant against that exact `C_open` which passed the whole guard G0-G12 and whose transcript conforms. In particular no published byte is edited: the published grids stay empty and the loop's readings live beside them.
- **p11** (P) — Nothing published is written. No file under `experiments/diagnostics/**` or `experiments/analyses/**` is created, modified, renamed or deleted by the run; the run writes only under `experiments/loops/L001-loop-first-live-2026-09-14/` plus append-only additions to `docs/DECISION_LEDGER.md` and the repo activity log.
- **p12** (P) — The claim ceiling is present and the three cell states are never collapsed. Every rendered table and the closing record contain each sentence of `standard.CEILING_REQUIRED_SENTENCES` verbatim and the ceiling body at its pinned sha256; and no rendered file describes an `unread` or a `machine-unresolved` cell as unresolved by inquiry, and no rendered file carries the one forbidden stop-vocabulary token outside the ceiling's own denial clause.

**No clause is a count.** Every clause above is a universal or existential over a fixed,
pre-registered, named key set; a set-membership test against a closed vocabulary; a byte
or digest equality; a uniqueness predicate (`str.count(q) == 1`); a span-containment test;
an emptiness assertion on a set defined by kind; a verbatim substring presence; or a
recency comparison on a cycle index. No clause reads a quantity of readings, marks,
agreeing endpoints, `differs` marks, blocks, rows resolved or calls spent, and none
compares such a quantity against a threshold.

---

## 4. The claim ceiling, verbatim

The text below is `standard.CEILING_TEXT` byte-for-byte. It is frozen into the
pre-registration, its sha256 is pinned into `loop_plan_id`, and `report.py` refuses to
emit any table or any report without it.

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
- more replicates, or the eleven C001 occurrence-01 juxtapositions this run names `unread`;
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
`reopen_reason` — so the mark-triple set is identical to cycle 2's and the run stops at
clause 4, `no_new_reading_changes`. A table that is mostly `unresolved` and
`machine-unresolved` at the end of that is the rule working.

**The three cell states are printed as three things and must not be conflated.** The
eleven C001 occurrence-01 juxtapositions and everything past the declared boundary are
**unread** — unreached by spend. A cell the guard declined is **machine-unresolved** and
carries the block code that declined it. A cell a guarded trial left open is
**unresolved**. Rendering any of the first two as unresolved-by-inquiry would let an
unfinished worksheet read as a finding, and `report.py` refuses to.

**Success for this pre-registration is not that any cell filled.** It is that the
mechanism ran from this config to a closing receipt with no human step, published before
it dispatched, resumed without re-sending a spent coordinate, and recorded honestly what
it declined to read. A green run says the loop works. It says nothing whatever about
whether a reading the loop produced is any good, and with `appellate_rulings: 0` this
record does not describe itself as validated, checked or confirmed. That the loop ran
without a human is a fact about the loop, not a fact about the readings.
