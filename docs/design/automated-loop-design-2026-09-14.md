# The automated end-to-end harness loop — FINAL design of record

Synthesis of `design-loop` (consensus winner, 28/30 from both judges), grafted with
`design-fw5`'s decision rule and write-time guards and `design-spec10`'s guard interior,
ceiling discipline and grounded-default artifact. Every fatal flaw the judges named is
fixed below, and every repo fact this design leans on was re-verified against the tree at
`865a800` before it was written.

Scope of the automated acts: the `use_relation_h005` reading cells (`root_reading`,
`root_passage_cited`, `root_notes`), the C001 contrast-register marks
(`differs`/`same`/`unresolved` on PLAN §8a's T/E/D/G), and the continue/stop decision —
plus the dispatch, import and publication that produce the material those readings read.
A human is available as an appellate at every point and is required at none.

---

## 1. Thesis and decision record

### 1.1 Thesis

**The loop automates the labour, never the authority, and the record is the product.**

Three instruments in this repository already stop exactly where interpretation begins.
`use_relation_h005` emits a juxtaposition table whose four `root_*` cells are
deliberately empty and whose banner says so: *"The tool records juxtapositions; the
reading is root's… An empty cell is an **unread row**, not a reading of `unresolved`."*
`contrast_triple_study` renders a C001 mark grid that "nothing in the driver fills"
(PLAN §8a). `multicycle_commitment_study_multi_v2` dispatches waves with
publication-before-dispatch, write-once records and no retries, and issues no verdict at
all. What is missing is not a fourth instrument. What is missing is a *reader* whose
output is criticisable rather than merely produced, and a *driver* that walks
pre-registration → dispatch → import → reading → marking → decision → publication with
nobody at any step.

The reading is built as what spec §3/§10 already provides for: a **rubric verdict**,
tried under a critic/defender/judge protocol, screened by thirteen program checks, and
registered as a warrant that **attacks a standing `unresolved` artifact**. Nothing new is
minted at the level of the ontology: no new relation, no new status, no `kind` field, no
score, no meter, no ranking of endpoints. What follows is problem criteria, content
conventions, a standard artifact, provenance and scheduler policy — spec §10's own
dispatch note.

Four consequences carry the whole design.

**Unresolved is the grounded default and it reinstates by computation.** Before any
provider call, every cell is registered as a tiny artifact meaning *this cell is
unresolved*. A reading attacks it. Refute the rubric, sustain an audit hit against the
seat's validity node, or enter an appellate ruling, and the reading's warrant is disabled
in adjudication pass 1 and the unresolved artifact reinstates — no delete, no curation,
no status rule outside `att`/`dep`. FW5:634 stops being a discipline the operator must
remember and becomes the fixpoint the graph computes.

**Every interpretive act is screened by a program before it is allowed to matter.** The
judge never answers *what relation is this?*. It answers *does the cited passage
establish the relation the critic claims?*, and its citation must resolve, by
`str.count == 1` and `str.index`, to a unique byte offset inside the frozen material —
not inside the prompt's framing. Cross-family unanimity, order-swap, paraphrase
invariance and the baseline seal are the rest. A blocked ruling registers nothing, the
cell stays unresolved, and the block is counted by reason code — which is FW5 R5
(non-evaluability is not refutation) made mechanical and, crucially, *visible*: a high
block rate is the instrument declining to read and must never be rendered as an absence
of relations.

**The only attacks automation is licensed to mint on the material are program-checked
attacks on the automation itself.** A reading never mints an `att` edge on a node under
study: `rejects-with-reason` is a reading of what a record's content does, not a
criticism landing, and promoting a declared relation into an adjudicative edge is the
error FW5:653 names and this programme has already made once. Judge audits — paraphrase
invariance, premise deletion, planted-flaw calibration against ground truth true by
construction — land as `eval:program` demonstrative warrants against the validity nodes
of the readings the audited seat issued. Formal machinery criticising informal
machinery, which is what spec §10.4 exists to preserve.

**Continuation is FW5 R8's repair condition, not a count.** Continue only when a
pre-registered *failed* obligation became satisfied and the artifacts that make it
satisfied were registered by this cycle (`ProducedBy` discharged, not temporal
succession), with every pre-registered *protected* obligation preserved and every loss
outside the protected set written down. No count of readings, marks, agreeing endpoints
or `differs` enters that rule.

### 1.2 Decision record

Eleven decisions, each with the repo fact that forced it. Every file, line number and
enum member below was re-read at `865a800`.

**D1 — `provenance.role` is `CRITIC`, never `judge`. (Fatal flaw in spec10 and fw5;
fixed.)** `src/deepreason_core/ontology/artifact.py:44-51` defines
`ProvenanceRole = {conjecturer, critic, variator, synthesizer, seed, import, user}` and
`Provenance.role` is pydantic-typed against it. There is no `judge` member, so
`provenance: {"role": "judge"}` raises on the first registration. The vendored enum is
**not** edited — that is vendoring drift against `AHepi/DeepReason@9607fba`. Instead:
`Provenance.role = CRITIC`, `Provenance.school = <seat family>`, and the literal role
name (`judge`, `critic`, `defender`, `variator`, `marker`) is carried in two honest
places — the artifact's own content, and `LLMCall.role` on the Register event, which
`ontology/event.py:32` types as a free-form `str`. Nothing is lost: `Provenance`'s own
docstring states that provenance "is never a warrant (D2): epistemically inert by
construction", so the role field was never doing adjudicative work.

**D2 — the reading warrant is DEMONSTRATIVE and carries a `rubric:` commitment. (Fatal
flaw in spec10; both judges' second shared finding; fixed.)** Both the transcript gate
and the case-law closure are conditional on a commitment whose `eval` starts with
`rubric:`, and — verified — **neither tests `WarrantType`**. `harness._validate_warrant`
(lines 379-401) fires `conforming_transcript` when `warrant.commitment` is set and
`self.commitments[warrant.commitment].eval.startswith("rubric:")`.
`adjudication/edges.build_att` resolves `kappa = commitments.get(w.commitment)` and runs
the case-law extension when `kappa.eval.startswith("rubric:")`. So the reading warrant
must carry commitment `rubric:reading-v1`, or *both* the "unbypassable guard" and the
"refute the standard and every cell reinstates" claims are false. `ontology/warrant.py`
marks `commitment`/`verdict`/`trace_ref` "Demonstrative-only fields" and its own header
says "for rubric warrants: trial transcript, §2"; `ontology/commitment.py` lists
`rubric:<spec-id>` beside `program:` and `predicate:` as an eval kind and requires the
spec-id to "resolve to a registered standard artifact (§10.3)". The consistent reading
is therefore: *demonstrative* here means "a declared commitment was evaluated on the
target and returned `fail`", and `rubric:` names the evaluator as a guarded trial rather
than a program. The reading warrant is `type: DEMONSTRATIVE`, `commitment:
rubric:reading-v1`, `verdict: "fail"`, `trace_ref: <transcript blob>` — exactly the shape
`harness.transcript_blob` already builds. spec10's "argumentative, because no program
computed the relation" is rejected as a category error about what `demonstrative` names
in this ontology; the honesty work it was doing is done instead by the claim ceiling and
by `Provenance.role = CRITIC`.

**D3 — the commitment that fails is on the cell, not on the material.** `κ_read`
(`eval: "rubric:reading-v1"`) is declared on the cell-open artifact and reads: *no
relation from the registered vocabulary is established for this cell by a guarded trial
over the frozen juxtaposition*. A sustained trial is a `fail` verdict on `κ_read`. This
is why the defender defends the null and why `unresolved` is the position that must be
beaten rather than the fallback — spec10's best local move, kept.

**D4 — the baseline rule is enforced at KIND grain by a program.** PLAN §8a, verbatim:
"A register is marked `differs` for a case pair only if the difference root reads between
the two cases is one root does **not** also read between at least one pair of replicates
inside ORIGINAL. Where the same **kind** of difference already appears inside ORIGINAL's
own five replicates, the register is `same` for that pair and the fact is recorded."
fw5's G11 delegated that certification to the marker while calling it program-certified
(its one honesty slip); spec10 coarsened it to register grain, which over-suppresses
`differs` and deviates from a frozen pre-registration. Adopted: `design-loop`'s closed
per-register `difference_kind` token set, compared by program against the sealed
baseline's kind set.

**D5 — the resolvable surface includes the body passages the instrument actually emits.**
`UseRow` (`src/minireason/use_relation_h005.py:425-461`) carries
`referring_body_passages`, `declared_uptake_includes_referring_record`,
`declared_uptake_includes_target_record` and `resolver_notes` alongside the two records.
spec10's `J` was REFERRING + TARGET only, which makes a reading grounded in an
overlapping body passage unresolvable by construction. The resolvable surface `M` is
referring record ∪ target record ∪ listed body passages; the uptake booleans and resolver
notes are framing, and a citation resolving into framing is void (G3).

**D6 — the reading vocabulary is being closed, and the ceiling says so.**
`ROOT_READING_VOCABULARY`'s own docstring: "It is not a closed single-valued enum… Root
may write more than one, and may write a reading this vocabulary does not cover — and say
so. The instrument never selects from it, and nothing here is enforced in code." The
machine cannot guard a relation its standard does not define, so the reader schema closes
the six values *and* carries an `outside_vocabulary` free-text field which, when
non-empty, forces the machine cell to `unresolved` with reason `outside-vocabulary` while
preserving the text for a human. Multiplicity is handled by trying each nominated
relation as its own trial. Both narrowings are named in the claim ceiling. None of the
three source designs said this.

**D7 — the runner is imported in-process, never shelled.**
`provider_openai_compat.slots_for` (line 350) is backed by a module-level
`_SLOT_REGISTRY` (line 347) and raises `CONCURRENCY_LIMIT_CONFLICT` rather than widening
a limit in force. `endpoints.json` carries **24 endpoints over 10 family labels but only
two `key_env` values** — `DEEPSEEK_API_KEY` (2 endpoints) and `OLLAMA_API_KEY` (22) —
each `max_concurrency: 5`, `timeout_seconds: 180`. A subprocess gets a fresh registry and
silently doubles the ceiling. The driver therefore imports
`multicycle_commitment_study_multi_v2` and calls `send_round` (line 1687, which takes an
injectable `provider_factory` and `publication_check`) in-process, and reuses its
`key_gate` (line 1339) rather than adding a third gate.

**D8 — cross-family is not independence, and the record says so.** Ten `family` labels
is a delivery fact. Twenty-two of twenty-four endpoints spend one credential and are
served by one host. Family distinctness is required (it is the only available lever) and
is never reported as evidential independence.

**D9 — the decision rule is fw5's O/P repair condition with loop's boundaries around it.**
`design-loop`'s C2 (`new_reading_changes > 0`) is the most count-shaped predicate in the
three designs. It is demoted to a boundary and the primary continue condition becomes
R8's: a failed obligation satisfied by *this* cycle's own registered artifacts, protected
set intact, losses outside P written every cycle even when empty.

**D10 — the appellate attacks the validity node, never the reading artifact.** Attacking
ν makes the reading `suspended`/its warrant disabled and reinstateable, which is what N1
wants, and the cell reinstates through `final_labels`' pass-2 cascade rather than through
a code path that rewrites a published record. Verified: `adjudication/support.py`
labels a dependent whose premise fell `SUSPENDED_UNSUPPORTED`, "orphaned != false".

**D11 — this is a mechanism intervention with its own identity.** It amends neither C001
(`plan_id 328b9452…41c8`) nor H005. It mints its own `loop_plan_id` and its own
pre-registration receipt (§8). No frozen plan, no published occurrence, no file under
`src/creib/**`, and no line of `src/minireason/provider.py` is touched.

---

## 2. Roles, prompt contracts, JSON schemas, the standard artifact, and the guard

### 2.1 The standard artifact — `std:reading-rubric/v1`

Registered under `Rule.REFL` at PREREGISTER, before any call, as a `codec: json`
artifact with `provenance.role = SEED`. Content:

- the rubric text for each question class, and its `mode`: `absolute` for relation
  trials, `pairwise` for contrast marks;
- the six-value vocabulary **with its published non-exclusivity note reproduced
  verbatim** from `ROOT_READING_VOCABULARY`'s docstring, plus the `outside_vocabulary`
  escape and what it forces;
- the four C001 registers T/E/D/G **mirrored byte-identically from PLAN §8a**, including
  the prefix-intact rule for T, the bare-token rule for E, the FCL field list for D
  (`type`, `uptake`, `revises`, `withdraws`, `action`), the grounds sources for G, the
  replicate-baseline rule, the order-of-reading rule, and the register-to-falsifier
  mapping (D1 only from T/E/D on ORIGINAL vs CONTROL — *G alone never carries D1*; F2
  from T/E/D on ORIGINAL vs RECODING; F3 on ORIGINAL vs CARRIER);
- the closed `difference_kind` token set per register;
- the guard parameters: seat counts, `TRIAL_PARAPHRASE_N = 2`, `schema_repair_budget = 0`,
  the unanimity rule, the reopen-reason list;
- anchor exemplars for the calibration set.

Its artifact id is pinned into `plan.json` and is the `<spec-id>` that
`rubric:reading-v1` resolves to (`commitment.py`: "rubric `<spec-id>` MUST resolve to a
registered standard artifact (§10.3)"). It is attackable, reinstateable and succeedable;
a revised rubric is a **successor artifact and a new `loop_plan_id`**, never an edit.

### 2.2 Seats

Drawn from `endpoints.json` by a deterministic rule pinned in `plan.json` before
dispatch: sort by `(family, name)`, then assign.

| role | seats | family constraint |
|---|---|---|
| `critic` | 1 | distinct from every judge seat |
| `defender` | 1 | distinct from the critic |
| `judge` | **2, from 2 distinct `family` values** | distinct from critic and defender where the registry allows; the record says when it could not |
| `variator` | 1 | any |
| `marker` | reuses the judge pair | as above |

Seat identity (endpoint name, model, family, `key_env`, `timeout_seconds`) is frozen into
the plan digest. Substituting an endpoint mints a new `loop_plan_id`: a new
pre-registration, never an amendment. No seat is ever compared with another for merit —
seats are occasions, not contestants (FW5:849, :851).

### 2.3 Prompt contracts and JSON schemas

Every pack is a pure deterministic render (`packs.render_*`), byte-stable across repeats,
containing only frozen material plus the rubric body plus the precedent slice. A pack
never contains a label, an `att`, a `dep`, a status, another cell's outcome, or another
seat's output. Schema-invalid output is `unresolved` at `schema_repair_budget = 0`; where
the config raises it to 1 the re-ask is a **new coordinate** (`…#repair1`), budgeted,
published, never a retry of a spent call.

**`critic`** — pack: rubric body, the resolvable surface `M`, the framing (uptake
booleans, resolver notes, the instrument's own lexical-overlap banner verbatim).
Instruction: *draft the strongest case that exactly one named relation holds, quoting a
passage of the material verbatim; or answer `none`.*

```json
{"relation": "re-deploys|qualifies|rejects-with-reason|repairs|retains|none",
 "passage_quote": "verbatim substring of the resolvable material",
 "role_bindings": {"target": "", "defect": "", "grounds": "", "bearing": ""},
 "case": "<=400 words",
 "outside_vocabulary": ""}
```

`relation: "none"` ends the row at one call: no trial, cell stays unresolved.
A non-empty `outside_vocabulary` forces `unresolved` with that reason and preserves the
text.

**`defender`** — pack: `M`, the critic's case. Instruction: *answer the case; the
position you defend is that the juxtaposition does not establish the claimed relation.*

```json
{"answer": "<=400 words", "concedes": false}
```

**`judge`** (×2, cross-family, identical packs) — pack: rubric body, `M`, case, answer,
and the **precedent slice**: top-K accepted precedent readings citing this standard,
appellate rulings ranked first, selected by a deterministic query whose text is logged.

```json
{"sustained": true, "decisive_point": "exact substring of case + \"\\n\" + answer",
 "reading_note": "<=120 words"}
```

**`marker`** — one call per (cell, comparison, register). Never sees more than one
register, so no call can trade registers off.

```json
{"mark": "differs|same|unresolved",
 "difference_kind": "<closed per-register token or null>",
 "left_quote": "", "right_quote": "", "case": "<=120 words"}
```

**`variator`** — `{"paraphrases": ["…", "…"]}` over the *exchange only*. The material is
never paraphrased: its bytes are what the offsets resolve against. Quoted spans are
extracted, held out of the paraphrase, re-inserted byte-identically, and their survival
asserted by program; on failure the spot-check itself is `unresolved` and the cell keeps
the unparaphrased outcome flagged `paraphrase_check: not_performed`.

**`decider`** — a program, not a model (§5).

### 2.4 The §10 guard procedure, step by step, and what the PROGRAM checks

Run in this order. The first failure blocks: **nothing is registered**, the cell stays
unresolved, and the block is logged with its reason code, the prompt blob ref and the raw
blob ref. Every check below is deterministic Python; none is an LLM call.

**G0 — constitution (pre-dispatch).** Assert ≥2 judge seats with distinct `family`
values, critic family ∉ judge families, defender family ≠ critic family. Unsatisfiable ⇒
the coordinates are `NOT_DISPATCHED` with an operational reason. *An operational reason
is never a semantic result.*

**G1 — schema.** Validate against §2.3. Invalid ⇒ `blocked:schema`.

**G2 — referential integrity, on two surfaces, by uniqueness.**
 (a) The critic's `passage_quote` must satisfy `M.count(q) == 1`; the program takes
 `M.index(q)`, maps `(start, end)` back through the offset table to the *occurrence-file*
 span, and writes `(surface, start, end, occurrence_path, file_start, file_end)` into the
 transcript. Zero occurrences, or more than one, ⇒ `blocked:referential-integrity`.
 (b) The judge's `decisive_point` must satisfy `E.count(d) == 1` where
 `E = case + "\n" + answer` — strictly stronger than, and a superset of, the vendored
 predicate `harness.conforming_transcript`, which requires only `decisive in exchange`.
 Both are asserted; the vendored one is asserted last so that the registration gate and
 the guard cannot diverge.
 This is the difference between a judge pointing at the material and a judge pointing at
 itself.

**G3 — operative target (R10).** The resolved span of `passage_quote` must lie inside the
declared referring record, the declared target record, or one of the listed
`referring_body_passages`. A span in the pack's headings, instruction, vocabulary list,
banner or resolver notes is void ⇒ `blocked:operative-target`. A reading grounded in the
prompt's own scaffolding is not a reading of the material.

**G4 — closed vocabulary.** Any token outside the six values ⇒ `unresolved`. A non-empty
`outside_vocabulary` ⇒ `unresolved:outside-vocabulary`, text preserved (D6).

**G5 — cross-family unanimity.** Both judge seats must return the same `sustained`. A
split ⇒ `blocked:ensemble-split`, a `Rule.MEASURE` event recording *both* rulings
verbatim, and a signal toward the `audit-the-critic` Spawn. **Never averaged, never
majority-voted** — a majority vote is an averaging device wearing a different hat
(FW5:634).

**G6 — order-swap.** Every pairwise judgement — the adjudication, and every contrast
comparison — is run in both presentation orders with labels reassigned. A different real
outcome ⇒ `blocked:order-swap`. The `decisive_point` of both orders is checked under G2b.

**G7 — paraphrase spot-check.** Only on a *sustained* ruling (a non-sustained ruling
registers nothing, so there is nothing to guard). `TRIAL_PARAPHRASE_N = 2` paraphrases of
case+answer, quoted spans held out and asserted to survive byte-identically. Any flip, or
any split on a paraphrase, ⇒ `blocked:paraphrase-flip`, no warrant, and the flip is
logged against that seat's reliability record for the audit arm.

**G8 — baseline seal (C001 only).** The marker refuses to render any cross-case pack for
a cell until that cell's within-ORIGINAL baseline grid exists and **its sha256 is pinned
into the call record** ⇒ `BASELINE_NOT_FIRST`. PLAN §8a's "the baseline note is written
first and is not revised afterwards" becomes physically irreversible: revising the
baseline changes a hash that every subsequent call record already carries.

**G9 — replicate baseline at kind grain (C001 only).** A `differs` mark is admissible
only if its `difference_kind` token is **absent** from the frozen baseline's kind set for
that register. If present, the **program writes `same`** and records the baseline
replicate pair that forced it (D4).

**G10 — program pre-empt (C001 only), in this order, before any marker call.**
 (a) *Byte-identity defeater.* A cell whose ORIGINAL and CONTROL `commitments` are
 byte-identical does not exhibit D1 there; computed first, recorded as a program finding,
 and the program finding stands in the falsifier evaluation.
 (b) *Under-replication.* Fewer than three resolved replicates of any case ⇒ no marker
 call for that case; `unresolved`, reported as **absent data, never as an absence of
 difference**.
 (c) *Register E bare tokens.* Prefix-qualified references are resolved by program; a
 bare id token shared with the account document (`o1 c1 c2 p1 u1`) is forced
 `unresolved`, is **never** `differs`, and never reaches a trial.
 (d) *Registers T and D on the FCL arm.* `target` arrays (prefix intact), `type`,
 `uptake`, `revises`, `withdraws` and `action` are parsed; where the parse succeeds the
 mark is **program-computed and no judge is called at all**. The trial runs only on the
 prose arm and on FCL rows the parser could not resolve. This is spec §9's own "prefer
 `program`/`predicate` over `rubric` wherever content is formal" used as load-bearing
 structure, and it removes the model from the hot path on the formal arm entirely.

**G11 — no re-reading for resolution.** A cell whose prior outcome was `unresolved` may
not be re-read unless the call record carries a `reopen_reason` from the pre-registered
list — *new material*, *repaired guard*, *appellate ruling*. **Enforced by refusing the
write**, not by a convention. This is the only mechanical defence against retrying until
something sticks.

**G12 — no scoring key.** `assert_no_scoring_keys` (the existing
`contrast_triple_study` guard, which raises `SCORING_KEY_FORBIDDEN`) is run over every
emitted artifact, every table header and every rendered file.

**Blocks are counted, published and named.** A streak of blocks on one role is a
`Rule.SPAWN` trigger — `audit-the-reader` — never a reason to loosen a check.

### 2.5 Judge audits (spec §10.4), on a schedule

Every `AUDIT_PERIOD` cycles, budgeted, over readings **already on record**:

- **paraphrase invariance** — re-rule logged exchanges on fresh variator paraphrases;
  flips are hits;
- **premise deletion** — delete the cited `decisive_point` from the exchange and re-rule;
  a ruling that survives the removal of its own stated grounds is easy to vary and is a
  hit;
- **planted-flaw calibration** — a constructed set built at PREREGISTER whose ground
  truth is true **by construction**: a row juxtaposed with itself ⇒ `retains`; two
  records with no shared reference ⇒ `none`; a record that quotes and rejects ⇒
  `rejects-with-reason`; plus clean controls that must *not* sustain. Error rate above
  `JUDGE_ERR_MAX` Spawns `audit-the-critic`;
- **ensemble disagreement** — logged as a Measure series, never as a verdict.

Each hit registers as an `eval:program` **demonstrative** warrant against the ν of every
reading that seat carried in the window. By D10's closure this collapses those readings
in pass 1 without anyone deciding to withdraw them. Audit outputs are themselves
artifacts with their own ν and are themselves attackable.

---

## 3. How readings and marks enter the graph

Six shapes, all ordinary artifacts, registered through `harness.register_batch` into a
`Harness` opened with the deterministic `clock` parameter so the log does not fork on
machine load.

**(a) `STD_READING` — the standard.** §2.1. `Rule.REFL`, `provenance.role = SEED`,
`mention` ref to the pre-registration text.

**(b) `E_row` / `E_cell` — the material.** The `UseRow` bytes exactly as the instrument
emitted them (root cells empty), or the frozen C001 delivery bytes.
`provenance.role = IMPORT`. Registered before any call.

**(c) `C_open` — the cell-open artifact.** For every row and every (cell, register,
comparison): `{"cell": <key>, "state": "unresolved"}`, `provenance.role = IMPORT`, its
interface declaring commitment `κ_read` (`eval: "rubric:reading-v1"`), and a `dependence`
ref on its `E_row`/`E_cell`. Registered before any provider call. Unattacked, therefore
`accepted`: **the table starts, correctly, entirely unresolved.**

**(d) `A_reading` — the reading.** `codec: json`. Content: cell key, relation or mark,
`difference_kind` where applicable, the resolved passage offsets *and* their
occurrence-file spans, the seat identities and families, the literal role names, prompt
and raw blob refs, and every guard result. `provenance.role = CRITIC`,
`provenance.school = <judge family pair>` (D1). Refs: `dependence` → `E_row`,
`mention` → `STD_READING`.

**(e) `ν` — the validity node, split in two.** Registered as *two* artifacts on the same
warrant path where the rubric distinguishes them:
 - `ν_soundness`: the guard as run is a sound procedure for deciding this relation on
   these bytes — panel was cross-family, offsets resolved uniquely inside the declared
   spans, transcript conformed, order-swap agreed, no paraphrase flip, these endpoints,
   these prompt digests, this audit record at ruling time;
 - `ν_bearing`: this relation, if read, bears on the claim it is offered for.
Each carries a `mention` ref to `STD_READING` (triggering the **case-law closure**) and
`evidence` refs to `E_row` and to the transcript artifact (triggering the **evidence
closure** through their dependence lineage). A criticism can then land on bearing alone,
which R2 requires.

**(f) `W_reading` — the warrant.** `type: DEMONSTRATIVE`, `target: C_open`,
`commitment: rubric:reading-v1`, `verdict: "fail"`, `trace_ref: <transcript blob>`,
`validity_node: ν_soundness`, carried by `A_reading` (D2/D3). The transcript blob holds
pack digests, both seats' raw record paths, case, answer, both rulings, the
`decisive_point` with resolved offsets, every check result and every paraphrase
re-ruling. `harness._validate_warrant` refuses registration if it is not a conforming
transcript — so the guard is unbypassable *because the commitment is rubric-typed*, which
is the precise condition spec10 asserted without meeting.

**What never registers.** No reading mints an `att` edge on any node under study. No
reading mints a `dep` edge between studied nodes. `re-deploys` creates no support edge
and `rejects-with-reason` creates no attack edge.

**Consequences, all computed by §4 with nothing added.**
 - A sustained reading refutes `C_open`: the cell reads.
 - Two rival readings of one cell both attack `C_open` and both survive ⇒ §3's "≥2
   surviving rivals for one π" Spawns a discrimination problem, resolved by a pairwise
   trial under the full guard or left standing. **Disagreement becomes a problem, never
   an average.**
 - Refute `STD_READING` ⇒ case-law closure attacks every ν citing it ⇒ validity-node
   closure disables every carrier ⇒ every reading falls and every `C_open` reinstates.
   Computed, not curated. This is the parallel-fifths reinstatement of §10.3.
 - Invalidate `E_row` (custody correction, re-import at a different grain) ⇒ the reading
   becomes `suspended_unsupported`, not `refuted`. **Orphaned is not false**
   (`adjudication/support.py`).
 - An audit hit against `ν_soundness` collapses that seat's window of readings the same
   way.

**Appellate.** A committed ruling file under `<run>/appeals/<id>.json` is ingested at the
top of the next cycle by `auto_loop appeal` / `adjudicate` as a precedent artifact,
`provenance.role = USER`, with a `mention` ref to the standard it calibrates and an
**argumentative** warrant against whichever node it names — `ν_bearing`, `ν_soundness`,
`STD_READING`, a register definition, or a marker's `difference_kind` set. Argumentative
warrants carry no commitment, so no trial transcript is demanded of a human. Exactly two
effects: pass 1 recomputes (the reading falls and the cell reinstates, or a rival reading
stands), and the precedent enters subsequent judge packs **ranked first**. Authority is
pack ordering, never status privilege; the ruling is itself attackable (N1). A ruling
arriving after the loop stopped is handled by `auto_loop reopen --ruling <path>`, which
replays the log with the ruling appended and re-emits the decision **under the same
pre-registered O and P**; a ruling that requires changing O or P is refused with
`NEW_PREREGISTRATION_REQUIRED`. **The loop never waits for a ruling.** Where none has
arrived the record says so, and never says *validated*, *checked* or *confirmed*.

---

## 4. The loop driver

### 4.1 State machine

One command — `python tools/auto_loop.py run --config <path>`.

```
S0  PREREGISTER   freeze config -> loop_plan_id; write preregistration.md, obligations.json
                  (O and P), CEILING.md; register STD_READING, kappa_read, GUARD_PROC,
                  DECISION_RULE, the calibration set and every C_open artifact
S1  PREFLIGHT     offline: render every planned call through OfflineProvider; assert
                  planned == expected and provider_calls == 0; verify every pin;
                  self-test offset resolution on every row; refuse if planned calls
                  exceed config.max_calls
S2  PUBLISH_PLAN  commit + push + verify + VERIFIED line + ledger receipt
---- per cycle n ----
S3  CYCLE_OPEN    budget check; ingest appellate rulings; cycle receipt
S4  PREPARE       runner v2 prepare_wave per occurrence
S5  PUBLISH_IN    commit + push + verify the prepared wave inputs   <- before any socket
S6  SEND          runner v2 send_round in-process over the occurrences, one published HEAD
S7  PUBLISH_EV    commit + push + verify the wave's records
                  (S4..S7 repeat until ready_coordinates is empty for this cycle)
S8  IMPORT        graph_import_h005 per occurrence -> graph, residue, report; verify_custody
S9  USE_TABLE     use_relation_h005 build -> table with empty root cells
S10 READ          critic/defender/judge trials + guard over the pre-registered reading set
S11 MARK          program pre-empt, sealed baseline, then marks (contrast leg only)
S12 ADJUDICATE    register artifacts / nu / warrants; run audits if due; recompute labels
S13 DECIDE        program decision -> decision.json
S14 PUBLISH_CY    commit + push + verify S8..S13 + CYCLE.md + ledger receipt
---- end ----
S15 CLOSE         closing receipt: what ran, what stopped it, what is unresolved, the
                  block register, the audit record, the claim ceiling verbatim, what
                  would reopen
```

### 4.2 CLI, config, directory layout

```
tools/auto_loop.py {preregister|preflight|run|status|adjudicate|appeal|reopen|close|dry-run}
  --config PATH          frozen loop config (required for all but status)
  --cycles N             override the declared budget DOWNWARD only; upward => BUDGET_RAISED
  --mode live|offline    offline forces OfflineProvider everywhere
  --acknowledge KEY --reason TEXT   resume past a sticky halt (itself recorded)
  --ruling PATH          reopen only
  --publish-ref REF      default: the branch's upstream
  --dry-run-out DIR      dry-run only
```

Config `minireason.loop.config.v1`: `run_id`, `study`, `occurrences[]`, `runner`,
`publish_ref`, `cycle_budget`, `max_calls`, `reading_set[]`, `obligations_path`,
`seats{critic, defender, judges[], variator, min_judge_families, paraphrase_n,
schema_repair_budget}`, `contrast{attached, study, occurrences[]}`, `audit{period,
judge_err_max, streak_max}`, `reopen_reasons[]`, `provider_mode`, `max_per_key`,
`timeouts{}`, `graph_root`.

`loop_plan_id = sha256(canonical(config ∪ pins))`, where `pins` are the sha256 of runner
v2, `graph_import_h005.py`, `use_relation_h005.py`, `contrast_triple_study.py`,
`provider_openai_compat.py`, `endpoints.json`, every prompt template, `obligations.json`,
`CEILING.md`, the `STD_READING` body, and each attached study's `PLAN.md` and
`material.json`.

```
experiments/loops/<RUN-ID>/
  config.json  preregistration.md  obligations.json  CEILING.md  plan.json
  preflight.json  run.lock
  steps/NNNN-KIND.json[.open]
  graph/                              deepreason_core harness root (log.jsonl, blobs, objects)
  cycles/cycle-NN/{import,use-table,readings,contrast,decision.json,CYCLE.md}
  readings/<row_key>/{requests,attempts,responses,provider}/...   write-once, per role
  audits/  appeals/  errata/  CLOSING.md  READING_TABLE.md  COMPARISON.md
```

Occurrence trees stay where runner v2 and the contrast tool own them: the loop
**references them and writes nothing inside them**.

### 4.3 Step receipts and resume

Every transition writes exactly one write-once receipt,
`<run>/steps/<NNNN>-<KIND>.json`:

```json
{"schema":"minireason.loop.step.v1","step_key":"<sha256>","index":12,"kind":"SEND",
 "cycle":2,"loop_plan_id":"...","inputs_sha256":{},"outputs_sha256":{},"spending":true,
 "started_utc":"...","finished_utc":"...","status":"COMPLETE|FAILED|HALTED",
 "custody":{"verified":true,"checks":[]},"failure_code":null,"published_commit":"..."}
```

`step_key = sha256(canonical(loop_plan_id, kind, cycle, wave, inputs_sha256))`. Resume is
`run` again: recompute `loop_plan_id` (mismatch ⇒ `PLAN_ID_MISMATCH`), replay the step
ledger, skip every `COMPLETE` step. Steps are classed:

- **Replayable** (PREFLIGHT, IMPORT, USE_TABLE, ADJUDICATE, DECIDE — offline,
  deterministic, pure): re-run on resume; outputs must be byte-identical to anything
  already written, else `STEP_NONDETERMINISTIC`. A live check, not a formality.
- **Spending** (SEND, READ, MARK, AUDIT, every PUBLISH): an `.open.json` marker is
  written before the step and resolved by the receipt. An unresolved marker on resume
  **halts** with `UNRESOLVED_STEP` — a call may have been billed. SEND, READ, MARK and
  AUDIT resume at **coordinate** grain, because runner v2's `NO_REPLAY` and the reader's
  own write-once request/attempt/response records make per-coordinate resumption safe:
  the step is re-entered, each already-terminal coordinate is skipped, and each
  coordinate with a request or attempt but no response refuses re-send and is reported
  `INDETERMINATE` — never as an absence.

### 4.4 Failure handling

**Provider failure ends an arm; it never mints a warrant.** No retries anywhere. A
`FAILED` receipt carries the provider's own stable code (`HTTP_429`, `KEY_MISSING`,
`TRANSPORT_OR_RESPONSE_ERROR`, `SECRET_IN_REQUEST`). Runner v2's `arm_stopped` already
implements the arm-ends rule and `ready_coordinates` then returns an empty queue for it;
the driver records `arm_ended{arm, cycle, node, failure_code}` and continues the other
arms. The renderer emits, as fixed text: *delivery ended this arm; no semantic verdict is
issued for its coordinates.* (spec §1 — a containment kill must not mint a warrant;
FW5 R5 — non-evaluability is not refutation.)

**Custody failure halts and records.** Any `CustodyError`, any `required_paths` byte
mismatch, `REQUEST_NOT_FROM_PLAN`, `ARTIFACT_NOT_DERIVED_FROM_DELIVERY`,
`TIMEOUT_NOT_APPLIED`, `PROVIDER_REQUEST_FILE_CHANGED`, `SOURCE_PIN_MISMATCH`,
`TRANSPORT_PIN_MISMATCH` ⇒ step `HALTED`, an erratum stub under `<run>/errata/`, a ledger
receipt, publication of the halt, exit non-zero. **The loop never works around custody.**
Resuming past a sticky halt requires `--acknowledge <step_key> --reason "<text>"`, itself
recorded.

**Timeouts, three layers.** (1) Provider wall clock: the endpoint's declared
`timeout_seconds` (180 for all 24 endpoints), re-read off the frozen plan before each
send and written into request and receipt; disagreement ⇒ `TIMEOUT_NOT_APPLIED`. A
timeout is a delivery failure, never an `overrun` verdict, and mints no warrant.
(2) Step: `timeouts.step_seconds` per kind; exceeding it marks the step `FAILED` with
`STEP_TIMEOUT`, which on a spending step leaves the open marker and therefore halts on
resume — deliberately. (3) Git: 90 s, runner v2's value; a timed-out push leaves
publication *pending*, which blocks every successor step.

**PARTIAL deliveries** at an endpoint's declared ceiling are `comparable: false`,
mechanical columns withheld, compared against nothing.

**Ensemble seat loss mid-cycle** makes unanimity unobtainable: every row in flight
blocks, the cycle closes early and says so.

**Stop vocabulary.** `stop_reason ∈ {protected_loss, obligations_discharged,
no_new_reading_changes, resource_boundary, custody_halt, all_arms_ended,
instrument_fault, preregistered_condition:<id>}`. The token **"exhaustion" is not in the
vocabulary** and a test asserts it never appears in a generated record.

### 4.5 Receipt, activity and publication automation

`src/minireason/loop/receipts.py` and `publish.py`:

- `activity(phase, action, why, goal, paths)` **shells** `tools/repo_activity.py` —
  never reimplements it — with `--agent auto_loop --decision <REC-id> --phase
  begin|outcome`, bracketing every search, read, modification, test and dispatch. Never
  raw command text.
- `ledger_append(text)` appends to `docs/DECISION_LEDGER.md` in **byte mode**:
  `open("ab", buffering=0)`, `flock(LOCK_EX)`, `seek(0, SEEK_END)`, short-write loop over
  a `memoryview`, flush, unlock — the exact discipline `repo_activity.append` already
  uses (lines 26-52), so a concurrent publisher's appends are never clobbered by a
  read-modify-write. The receipt id `REC-<YYYYMMDD>-<letter>` is minted by scanning the
  ledger tail for the highest existing suffix **under the same lock that performs the
  append**, so two concurrent agents cannot collide. A receipt body containing a
  registered secret is **refused**, not redacted.
- `publish(paths, message, ref)`: activity begin → `git add <explicit paths>` (never
  `-A`) → `provider_openai_compat.redact_with_names` over the staged diff, refusing on
  any hit → commit → **non-forcing** push → verify → emit
  `VERIFIED <utc> local=<sha> remote=<sha> tree=<sha> ref=<ref> paths=<n>` into both the
  ledger and the step receipt. Where the connector creates a different remote commit,
  publication succeeds only if `HEAD^{tree} == <ref>^{tree}` and both commit ids are
  recorded. A rejected push is re-fetched and re-attempted as a **new publish step**,
  never force-pushed; three non-converging attempts halt.
- Cadence: a `PROGRESS` receipt at any step boundary past 240 s. A missed deadline is
  recorded truthfully, **never backdated**.

### 4.6 Key handling and the 5-per-key gate

Keys are read from the environment **at call time only, by
`provider_openai_compat`** — never by the driver, never written into any record.
`write_new` already refuses credential-bearing output and the ledger writer refuses too.

The real process-wide ceiling is `provider_openai_compat.slots_for(key_env, cap)`, backed
by the module-level `_SLOT_REGISTRY`, acquired internally by every
`OpenAICompatProvider`; runner v2's `key_gate` is an outer mirror bounding attempt-marker
writes. **The loop adds no third gate.** Reader, defender, judge, variator and marker
calls acquire `slots_for` through the same provider module, and the loop's outer gate is
runner v2's `key_gate` *imported, not copied* — so a reading call and a dispatch call in
flight together are held to five per credential between them. `endpoints.json` has 24
endpoints but only two `key_env` values, so wave capacity is 5 × 2 = 10 and 22 endpoints
share one gate.

This holds only inside one process. Therefore the driver **imports** runner v2 and calls
`send_round` in-process rather than shelling it, and `run.lock` (pid, start time,
`loop_plan_id`) refuses a second concurrent driver on the same run. Advisory across runs
on different credentials; mandatory on the same. A cross-machine run is not covered and
the design does not claim it is.

### 4.7 Dry-run — the acceptance gate

`auto_loop dry-run` proves the whole machine offline and is the build's acceptance gate.
`loop/synthetic.py` generates a synthetic occurrence — two FCL-1 documents with one
cross-document reference and one objection record, plus, for the contrast leg, four cases
× three replicates of canned deliveries constructed so that exactly one register differs
at a known `difference_kind`. Every provider is `OfflineProvider`; **every git operation
runs against a real bare repo in a temp dir through the same `publish()` path**, so
`VERIFIED` is genuinely exercised rather than stubbed. The dry run walks S0→S15 and
additionally induces, and asserts the closing receipt names by code, each of: one
provider failure (an arm ends, others continue); one custody mismatch (halt, erratum,
non-zero exit, sticky on resume); one step timeout; one ensemble split (cell unresolved,
not voted); one paraphrase flip (no warrant registered); one unique-offset failure (no
warrant); one baseline-kind collision (a `differs` forced to `same` by program); one
re-read refused for want of a `reopen_reason`; and one appellate ruling (label flips
through pass 1). Zero network calls, asserted by a provider-module counter.

---

## 5. The decision rule — pre-registered, and not a scalar meter

`obligations.json` is published with the plan and pinned by sha256 **before cycle 1**
(FW5:787 — O and P may not shift inside an assessment). `decide.py`'s own digest is
inside `loop_plan_id`.

**O — failed obligations this chain exists to discharge.** Each is a prose predicate plus
a program check over readable artifacts.
*o1*: every row in the pre-registered reading set carries either a passage-witnessed
relation or a recorded reason it is unresolved.
*o2*: every C001 cell carries four register marks or a recorded reason per register.
*o3*: every mark and every relation carries a citation resolving under G2 and G3.
*o4*: every cell's block, where blocked, carries a reason code from the closed set.
*o5*: the audit record in force is not older than `AUDIT_PERIOD` cycles.

**P — protected obligations; preserved, or the chain stops.**
*p1* ORIGINAL bytes remain the occurrence's bytes.
*p2* the recoding correspondence table stays complete and published before dispatch.
*p3* no case's request differs outside the objection block.
*p4* no scoring key appears anywhere.
*p5* provider and study records stay write-once with no replay.
*p6* no reading is averaged or majority-voted; disagreement stays `unresolved`.
*p7* no reading mints an `att` or `dep` edge on any node under study.
*p8* the appellate remains optional — no state blocks on it.
*p9* the baseline of every marked cell is still at the sha pinned in its call records.

After each cycle `decide()` evaluates every *o* and every *p* by program against ξ′ (the
cycle-end situation) and ξ (the prior), and returns **exactly one** outcome:

1. Any *p* fails ⇒ **STOP `protected_loss`**, the loss named and exposed. No
   continuation, no repair claim.
2. Else, ≥1 *o* failed at ξ and satisfied at ξ′, **and** the artifacts making it
   satisfied were registered by this cycle (`ProducedBy` discharged, not temporal
   succession) ⇒ **CONTINUE**.
3. Else, all *o* satisfied ⇒ **STOP `obligations_discharged`**.
4. Else, this cycle's set of `(cell, register, mark)` triples is identical to the
   previous cycle's ⇒ **STOP `no_new_reading_changes`**.
5. Else, cycle index equals the declared budget, or `max_calls` is reached ⇒ **STOP
   `resource_boundary`**.
6. Guard rails, evaluated before 1-5 and stopping immediately: a `HALTED` step ⇒
   `custody_halt`; every arm ended ⇒ `all_arms_ended`; a guard-block streak above
   `STREAK_MAX` or a calibration error rate above `JUDGE_ERR_MAX` ⇒ `instrument_fault`,
   which stops the reading arm and Spawns `audit-the-reader`.

A mandatory **`losses_outside_P`** section is written every cycle, **present even when
empty** (FW5:802). A cycle may be net withdrawal — more cells moving to `unresolved` than
away from it — and still be recorded as progress if an *o* was discharged, or as no
progress if none was (FW5:810). Every stop carries a mandatory `would_reopen` prose
field.

**Why this is not a scalar meter.** No clause reads a quantity of readings, marks,
agreeing endpoints or `differs`. Clause 4 is a **set-identity** test, not a count.
Clause 5 is a declared budget, an attention-and-spend question, never an adjudication
(spec §0, §11 — attention is not status; FW5:851 — counts are information, never an
automatic warrant). The vocabulary has no order: `repairs` does not outrank `retains`,
the four registers are never summed, and `assert_no_scoring_keys` makes any aggregate
field unexpressible. Clause 3 is the only "all satisfied" clause and it terminates rather
than rewarding. `decision.json` is registered with `provenance.role = IMPORT` and a
`dependence` ref on every reading artifact it read, so refuting a reading leaves the
decision record `suspended_unsupported` rather than standing on withdrawn ground.
Changing any threshold after first look mints a new `loop_plan_id` and is a new
pre-registration.

---

## 6. The claim ceiling of a fully automated run

`CEILING.md` is frozen in the pre-registration, its sha pinned into `loop_plan_id`, and
the renderer **refuses to emit any table or report without it**. The closing record and
every rendered table must contain the following sentences verbatim; a test asserts their
presence.

> **What this run claims.** Under registered standard `std:reading-rubric/v1` (digest …),
> a cross-family judge ensemble unanimously sustained relation *r* for this cell, citing
> a passage that resolves by program to a unique byte offset [s,e) inside the declared
> referring record, target record or listed body passage; the ruling survived order-swap
> and *N* meaning-preserving paraphrases of the exchange; the seats' audit record at
> ruling time was *A*. The reading is a registered, attackable artifact of
> `provenance.role = critic` carrying the literal role name `judge`, and it falls
> automatically if the standard, the evidence, or the seats' reliability is successfully
> attacked.
>
> **This run cannot claim FW5:628's witness of reason use.** A transcript supplies no
> structural map from the represented objection organization into a response
> suborganization preserving internal role bindings on an active dependency route, and
> neither does an ensemble of readers of that transcript. The strongest positive outcome
> available is *consistent-with*.
>
> **A null on the recoding or the carrier leg leaves those rival explanations unrefuted
> and unsupported, not excluded.** At N = 5 this is a limit of the design, not a finding.
>
> **Agreement between two cross-family readers is agreement between two conditioned
> generators, not corroboration by two independent observers.** The guard measures
> behavioural stability under paraphrase, order and adversarial answer — not truth. Ten
> `family` labels over 24 endpoints and two credentials is a delivery fact, not an
> independence proof.
>
> **An unresolved cell proves neither presence nor absence** (FW5:634). Ended arms, guard
> blocks, PARTIAL deliveries, bare-token ambiguity and under-replication are silent about
> content; non-evaluability is not refutation.
>
> **Three cell states are distinct and are printed as three things.** An *unread* cell is
> one nobody and nothing has read. An *unresolved* cell is a deliberate reading that
> stays unresolved. A *machine-unresolved* cell is one the guard declined to resolve, and
> it names the block code that declined it. Conflating any two would let an unfinished
> worksheet read as a finding.
>
> **A high block rate is the instrument declining to read. It is never an absence of
> relations.** The block register by reason code — `ensemble-split`,
> `referential-integrity`, `operative-target`, `order-swap`, `paraphrase-flip`,
> `outside-vocabulary`, `schema`, `provider`, `baseline-forced-same` — is printed with
> counts on every table.
>
> **No count is an automatic warrant** (FW5:851). Marks are reported per register and are
> never summed, averaged, weighted or ranked. Endpoints are independent occasions to look
> for one pattern, never competitors (FW5:849).
>
> **A reached ceiling is a declared resource boundary, not exhaustion of the inquiry**,
> and this record states which was reached and what would reopen the question.
>
> **`appellate_rulings: N`.** Where N = 0, this record does not describe the run as
> validated, checked or confirmed. That the loop ran without a human is a fact about the
> loop, not a fact about the readings.
>
> **Two published instruments were narrowed to make these cells machine-fillable, and the
> narrowing is part of the claim.** `ROOT_READING_VOCABULARY` is published as a
> suggestion that a row may exceed and that root may write outside; this run closes it to
> six values and routes anything outside to `unresolved:outside-vocabulary` with the text
> preserved. And where the published instrument says "the reading is root's", this table
> says the reading is a guarded `judge`-role artifact and **root has not read it**.
>
> **What would reopen this:** an appellate ruling; a successful attack on
> `std:reading-rubric/v1` or on a register definition, which collapses every ν citing it
> in pass 1; a custody correction; a third judge family; more replicates; a raised budget
> under a new `loop_plan_id`.

Every published run must additionally record: the seat assignment with families and
`key_env`; the full block register with counts; the audit results in force; the stopping
condition that fired; `losses_outside_P`; the `INDETERMINATE` coordinate list; and the
`loop_plan_id` with a pre-registration timestamp preceding the first call.

---

## 7. WAVE PLAN

Waves are dependency-free internally: every module's `depends_on` lies in a strictly
earlier wave. Wave 0 is shared types, schemas and the standard artifact. Every module is
implementable by one agent from its `public_interface` alone. Nothing touches
`src/creib/**`, the owner runner, `src/minireason/provider.py`, `deepreason_core`, any
published occurrence, or any frozen plan.

```json
[
 {"id":"W0-TYPES","wave":0,"path":"src/minireason/loop/types.py","purpose":"Config schema, loop_plan_id, step-receipt schema, stop vocabulary, block reason codes, failure codes, run layout constants.","public_interface":"LoopConfig.load(path); loop_plan_id(config, pins); StepReceipt; STOP_REASONS; BLOCK_CODES; FAILURE_CODES; LoopError; run_paths(root, run_id)","depends_on":[],"tests":"tests/loop/test_types.py","acceptance":"Two loads of one config give the same plan_id; a changed pin changes it; an unknown config key is refused; the token 'exhaustion' appears in no vocabulary; every block code used anywhere in the package is a member of BLOCK_CODES.","est_size":340,"touches_frozen":false},
 {"id":"W0-CONTRACTS","wave":0,"path":"src/minireason/loop/contracts.py","purpose":"Closed vocabularies and strict JSON schemas for critic, defender, judge, marker and variator; REGISTERS and the closed per-register DIFFERENCE_KINDS; forbidden-key guard; banner constants imported not retyped.","public_interface":"READING_VOCABULARY; OUTSIDE_VOCABULARY_FIELD; REGISTERS; DIFFERENCE_KINDS; MARKS; CriticOutput; DefenderOutput; JudgeRuling; MarkerOutput; VariatorOutput; validate(role, raw); SchemaInvalid; assert_no_scoring_keys(value); READING_BANNER","depends_on":[],"tests":"tests/loop/test_contracts.py","acceptance":"READING_VOCABULARY is imported from use_relation_h005.ROOT_READING_VOCABULARY, not retyped; a scoring key nested anywhere raises SCORING_KEY_FORBIDDEN; no ordering is defined on the vocabulary and no aggregate field is expressible; every malformed fixture raises SchemaInvalid naming its reason; validators are pure.","est_size":380,"touches_frozen":false},
 {"id":"W0-STANDARD","wave":0,"path":"src/minireason/loop/standard.py","purpose":"The reading-rubric standard artifact body: rubric text per mode, the six-value vocabulary with its published non-exclusivity note verbatim, the four PLAN 8a registers mirrored byte-identically, the register-to-falsifier mapping, the guard parameters, the reopen-reason list, the calibration anchors.","public_interface":"RUBRIC_V1; SPEC_ID; build_standard(registers, vocabulary, params) -> bytes; standard_body(raw) -> dict; PLAN_8A_REGISTERS; FALSIFIER_MAP; REOPEN_REASONS","depends_on":[],"tests":"tests/loop/test_standard.py","acceptance":"Every PLAN 8a register definition appears byte-identically against the frozen PLAN.md; FALSIFIER_MAP encodes that G alone never carries D1 and that F2/F3 fire only on T, E or D; two builds from identical inputs are byte-identical; the body declares mode absolute for relation trials and pairwise for marks.","est_size":420,"touches_frozen":false},
 {"id":"W0-CUSTODY","wave":0,"path":"src/minireason/loop/custody.py","purpose":"Frozen-file pin computation and verification, digest helpers, write-once writes, path fencing to the run directory.","public_interface":"pins(repo, paths) -> dict; verify_pins(plan, repo) -> list; write_new(path, value); fenced(root, path) -> Path; CustodyMismatch","depends_on":[],"tests":"tests/loop/test_custody.py","acceptance":"A one-byte change to any pinned file is detected and named; a path escaping the run root is refused; write_new refuses an existing path and refuses credential-bearing content; verify_pins is pure and order-stable.","est_size":280,"touches_frozen":false},
 {"id":"W0-RECEIPTS","wave":0,"path":"src/minireason/loop/receipts.py","purpose":"Byte-mode locked ledger append with receipt-id minting under the same lock; repo_activity begin/outcome wrapper that shells tools/repo_activity.py; cadence timer.","public_interface":"mint_receipt_id(ledger_path) -> str; ledger_append(text); open_receipt(**kw) -> rec_id; close_receipt(rec_id, outcome, evidence); activity(phase, action, why, goal, paths); Cadence.check(now)","depends_on":[],"tests":"tests/loop/test_receipts.py","acceptance":"Concurrent appends from two threads interleave with no loss and no torn record under simulated short writes; id minting under contention never collides; a secret-bearing body is refused, not redacted; a missed cadence deadline is recorded and never backdated; activity records carry no raw command text.","est_size":320,"touches_frozen":false},
 {"id":"W0-PUBLISH","wave":0,"path":"src/minireason/loop/publish.py","purpose":"Explicit-path add, credential scan, commit, non-forcing push, remote and per-path byte verification, the VERIFIED line; LocalGit double over a real bare repo.","public_interface":"publish(repo, paths, message, ref) -> PublishResult; verify_published(repo, paths, commit, ref) -> bool; VERIFIED_LINE; LocalGit; PublishPending","depends_on":[],"tests":"tests/loop/test_publish.py","acceptance":"Against a temp bare repo: explicit paths only, never -A; push is non-forcing; an equal-tree remote commit is accepted with both commit ids recorded; a planted secret in the staged diff refuses the publish; a timed-out or rejected push returns PublishPending and is retried only as a new publish; three non-converging attempts raise.","est_size":340,"touches_frozen":false},

 {"id":"W1-SURFACE","wave":1,"path":"src/minireason/loop/surface.py","purpose":"The resolvable material surface M (referring record + target record + listed referring_body_passages) with a byte-offset map back to occurrence-file spans, and the unique-substring resolver implementing G2 and G3.","public_interface":"build_surface(use_row) -> Surface; Surface.text; Surface.digest; Surface.spans; resolve_unique(surface, quote) -> Offset|None; within_declared_span(surface, offset) -> bool; Offset(start, end, side, occurrence_path, file_start, file_end)","depends_on":["W0-TYPES","W0-CONTRACTS"],"tests":"tests/loop/test_surface.py","acceptance":"A quote occurring exactly once resolves to the correct occurrence-file span; zero or multiple occurrences return None; body passages are inside the resolvable surface and framing is not; offsets are byte offsets and are documented as such for non-ASCII; surface bytes are deterministic; nothing is written under the occurrence.","est_size":360,"touches_frozen":false},
 {"id":"W1-SEATS","wave":1,"path":"src/minireason/loop/seats.py","purpose":"Deterministic seat selection over data/endpoints.json with the cross-family and foreign-reviewer rules; seat pinning into the plan body; the imported outer key gate.","public_interface":"load_registry(path) -> Registry; select_seats(registry, config) -> SeatPlan; SeatPlan.pins() -> dict; require_cross_family_judges(plan); key_gate_for(seat); FAMILY_COUNT_INSUFFICIENT","depends_on":["W0-TYPES"],"tests":"tests/loop/test_seats.py","acceptance":"Two judge seats always carry distinct family labels; selection is a pure byte-stable function of (registry, config); a registry with one family raises FAMILY_COUNT_INSUFFICIENT rather than degrading silently; the gate is multicycle_commitment_study_multi_v2.key_gate imported, not reimplemented, and never admits a sixth concurrent call per key_env; the pins record key_env per seat.","est_size":300,"touches_frozen":false},
 {"id":"W1-OBLIGATIONS","wave":1,"path":"src/minireason/loop/obligations.py","purpose":"O and P as prose predicates plus program checks; pinning; evaluation at a situation; ProducedBy attribution; the losses_outside_P register.","public_interface":"load_obligations(path) -> Obligations; pin(obligations) -> str; evaluate(obligations, situation) -> Evaluation; produced_by(situation, obligation_id) -> set; losses_outside_p(prev, curr) -> list","depends_on":["W0-TYPES"],"tests":"tests/loop/test_obligations.py","acceptance":"An o satisfied by artifacts not registered this cycle does not count as discharged; losses_outside_p returns a list that is present and empty rather than absent when there are none; evaluation is pure and reads only artifacts, never counts; the pin changes on any byte change.","est_size":420,"touches_frozen":false},
 {"id":"W1-GRAPH","wave":1,"path":"src/minireason/loop/graph.py","purpose":"Artifact, split validity-node and warrant shapes and their registration into deepreason_core; the cell-open artifact and its rubric commitment; appellate ingestion; the refusal to mint att/dep from a reading.","public_interface":"register_standard(harness, body) -> str; register_kappa_read(harness, spec_id) -> str; open_cells(harness, keys) -> dict; register_material(harness, row) -> str; register_reading(harness, result, standard_id) -> ReadingIds; split_validity_nodes(harness, result, standard_id) -> tuple; register_audit_warrant(harness, finding) -> str; apply_appeal(harness, ruling) -> str; cell_state(harness, key) -> str","depends_on":["W0-TYPES","W0-STANDARD"],"tests":"tests/loop/test_graph.py","acceptance":"Provenance.role is CRITIC and the literal role name rides in content and in LLMCall.role; the vendored ProvenanceRole enum is unmodified; the reading warrant is DEMONSTRATIVE carrying commitment rubric:reading-v1 and a conforming transcript, and registration is refused without one; refuting the standard reinstates every cell-open in one adjudication pass; refuting E_row leaves the reading suspended_unsupported, not refuted; no reading mints an att or dep edge on any studied node; two rival readings both survive and leave the cell contested; an appeal against a validity node flips the label through pass 1 with no published record rewritten; with a deterministic clock the log replays byte-identically.","est_size":560,"touches_frozen":false},
 {"id":"W1-STEPS","wave":1,"path":"src/minireason/loop/steps.py","purpose":"The step ledger: step_key, write-once receipts, replayable/spending classification, open markers, halt and acknowledge semantics, resume planning, run.lock.","public_interface":"StepLedger(run_root, loop_plan_id); ledger.run_step(kind, cycle, inputs, fn, spending=False); ledger.resume_plan() -> list; ledger.acknowledge(step_key, reason); completed_coordinates(out_dir) -> set; RunLock; UnresolvedStep; StepNondeterministic","depends_on":["W0-TYPES","W0-CUSTODY","W0-RECEIPTS","W0-PUBLISH"],"tests":"tests/loop/test_steps.py","acceptance":"A COMPLETE step is skipped on resume; an open spending marker halts with UNRESOLVED_STEP; a replayable step re-run with different bytes raises STEP_NONDETERMINISTIC; a halt is sticky until acknowledged with a recorded reason; a PublishPending state blocks every successor step; a second driver on the same run is refused by RunLock; kill-and-resume at every state leaves no coordinate re-sent.","est_size":460,"touches_frozen":false},
 {"id":"W1-SYNTHETIC","wave":1,"path":"src/minireason/loop/synthetic.py","purpose":"Synthetic occurrence and canned offline deliveries for the dry run, including one induced variant per failure mode the acceptance gate must assert.","public_interface":"build_occurrence(dir, *, induce=()) -> paths; canned_responses(seed) -> dict; INDUCIBLE","depends_on":["W0-TYPES"],"tests":"tests/loop/test_synthetic.py","acceptance":"The occurrence imports cleanly and yields at least one cross-document reference row; the contrast leg differs on exactly one register at a known difference_kind; each token in INDUCIBLE produces exactly the intended failure and nothing else; generation is deterministic from the seed.","est_size":460,"touches_frozen":false},

 {"id":"W2-PACKS","wave":2,"path":"src/minireason/loop/packs.py","purpose":"Deterministic pack rendering for every role, including the precedent slice with appellate rulings ranked first by a logged deterministic query; refuses to render a cross-case pack without a sealed baseline sha.","public_interface":"render_row(surface, standard, framing) -> Pack; render_exchange(pack, critic, defender) -> Pack; render_register(cell, register, comparison, baseline_sha, standard) -> Pack; render_paraphrase_request(exchange) -> Pack; precedent_slice(harness, standard_id, k) -> list; pack_sha(pack) -> str; BaselineNotFirst","depends_on":["W0-CONTRACTS","W0-STANDARD","W1-SURFACE"],"tests":"tests/loop/test_packs.py","acceptance":"Identical inputs give identical bytes; no pack contains a label, att, dep, status, another cell's outcome or another seat's output; the lexical-overlap banner is present verbatim; a register pack without baseline_sha raises BaselineNotFirst; the precedent query text is recorded with the pack and ranks appellate rulings first.","est_size":480,"touches_frozen":false},
 {"id":"W2-ROLES","wave":2,"path":"src/minireason/loop/roles.py","purpose":"Role dispatch through provider_openai_compat: write-once request/attempt/response records, zero retries, schema-repair as a new coordinate, per-key slot acquisition through the existing registry.","public_interface":"ROLES; call_role(role, seat, pack, schema, records_dir, *, repair=0) -> RoleResult; RoleResult.raw_ref; RoleResult.prompt_ref; ProviderArmEnded; NO_REPLAY","depends_on":["W0-CONTRACTS","W0-TYPES","W1-SEATS"],"tests":"tests/loop/test_roles.py","acceptance":"Runs end to end on OfflineProvider with zero sockets; a second call on an existing coordinate raises NO_REPLAY; six concurrent calls on one key_env are impossible because slots_for is acquired, not reimplemented; at schema_repair_budget 0 an invalid output yields unresolved and no re-ask; a repair is a new coordinate with its own write-once record; every record carries seat, family, key_env, pack sha, prompt ref and raw ref.","est_size":440,"touches_frozen":false},
 {"id":"W2-MARKPREP","wave":2,"path":"src/minireason/loop/markprep.py","purpose":"The C001 program pre-pass and baseline seal: byte-identity defeater, under-replication rule, register E prefix resolution and bare-token forcing, registers T and D parsed on the FCL arm, the within-ORIGINAL baseline grid with its kind set, sealed by sha.","public_interface":"program_marks(cell) -> dict; write_baseline(cell, replicates, out_dir) -> str; baseline_kinds(cell) -> dict; byte_identity_defeater(cell) -> dict; under_replicated(cell) -> set; residue(cell) -> list","depends_on":["W0-CONTRACTS","W0-STANDARD","W0-CUSTODY"],"tests":"tests/loop/test_markprep.py","acceptance":"Baseline is written and sealed before any residue is offered for marking; a bare id token shared with the account document is forced unresolved and never appears in the residue; T and D are program-computed wherever the FCL parse succeeds and the residue names exactly the rows it could not; byte-identical ORIGINAL/CONTROL commitments record D1-not-exhibited before any call; fewer than three resolved replicates of a case yields no residue for that case; editing the baseline after sealing raises.","est_size":560,"touches_frozen":false},
 {"id":"W2-DECIDE","wave":2,"path":"src/minireason/loop/decide.py","purpose":"The pre-registered stop/continue program: guard rails, then the five O/P clauses, then the decision record with would_reopen and losses_outside_P.","public_interface":"situation(harness, cycle) -> Situation; mark_triples(harness) -> frozenset; decide(prev, curr, cycle_index, config, obligations) -> Decision; render_decision(d) -> str; Decision.stop; Decision.reason; Decision.record_sentences","depends_on":["W0-TYPES","W1-OBLIGATIONS","W1-GRAPH"],"tests":"tests/loop/test_decide.py","acceptance":"decide() is total and returns exactly one outcome; a protected loss stops and names the loss; an o satisfied without this cycle's own artifacts does not continue; identical mark-triple sets stop as a set identity and not as a count; a budget stop carries the boundary-not-exhaustion sentence and a would_reopen field; a block streak stops as instrument_fault and names it a fault in the instrument, not a finding about the material; no count of readings, marks, endpoints or differs appears in any clause; the module digest matches the one pinned in plan.json.","est_size":420,"touches_frozen":false},

 {"id":"W3-TRIAL","wave":3,"path":"src/minireason/loop/trial.py","purpose":"The guard procedure G0-G12 end to end: critic, defender, cross-family judge ensemble, then constitution, schema, uniqueness on both surfaces, operative target, vocabulary, unanimity, order-swap, paraphrase spot-check, no-re-read and no-scoring-key. Blocked outcomes register nothing and are logged by reason code.","public_interface":"run_trial(harness, surface, standard, seats, config, *, mode, reopen_reason=None) -> TrialResult; TrialResult.outcome; TrialResult.blocks; TrialResult.transcript; build_transcript(result) -> str; ReopenRefused","depends_on":["W0-CONTRACTS","W0-STANDARD","W1-SURFACE","W1-GRAPH","W2-PACKS","W2-ROLES"],"tests":"tests/loop/test_trial.py","acceptance":"Every block path yields no warrant, one Measure event and a reason code from BLOCK_CODES; an ensemble split blocks and records both rulings verbatim, never a majority; a quote occurring twice in the material blocks; a quote resolving only into the pack framing blocks; a decisive_point absent from case+newline+answer blocks and the emitted transcript satisfies deepreason_core.harness.conforming_transcript; an order-swap flip blocks; a paraphrase flip blocks and is logged against the seat; a paraphrase that does not preserve a quoted span marks the spot-check not_performed rather than passing it; re-reading an unresolved cell without a listed reopen_reason raises ReopenRefused at the write; the whole module runs on OfflineProvider fixtures with zero sockets.","est_size":680,"touches_frozen":false},
 {"id":"W3-AUDITS","wave":3,"path":"src/minireason/loop/audits.py","purpose":"Judge audits over readings already on record: paraphrase invariance, premise deletion, planted-flaw calibration on a constructed set, ensemble-disagreement series. Hits become eval:program demonstrative warrants against the validity nodes of that seat's readings.","public_interface":"build_calibration_set(standard) -> list; paraphrase_invariance(harness, judge_caller, readings) -> list; premise_deletion(harness, judge_caller, readings) -> list; planted_flaw_calibration(harness, judge_caller, set) -> float|None; run_audits(harness, judge_caller, readings, config) -> AuditReport","depends_on":["W0-CONTRACTS","W1-GRAPH","W2-PACKS","W2-ROLES"],"tests":"tests/loop/test_audits.py","acceptance":"Calibration rows are true by construction and a clean control that sustains is scored as an error; a seeded flipping judge produces a paraphrase hit whose warrant collapses that seat's readings on recompute; a ruling surviving deletion of its own decisive_point produces a premise hit; an error rate above JUDGE_ERR_MAX returns a Spawn signal; every audit call reaches the log exactly once; audit findings carry their own validity nodes and are themselves attackable.","est_size":540,"touches_frozen":false},
 {"id":"W3-REPORT","wave":3,"path":"src/minireason/loop/report.py","purpose":"Renderers for READING_TABLE.md, COMPARISON.md, CYCLE.md and CLOSING.md: the frozen ceiling block, the block register by reason code with counts, the audit record in force, the stopping sentence, losses_outside_P, the INDETERMINATE list, and the unread / unresolved / machine-unresolved trichotomy.","public_interface":"render_reading_table(harness, plan) -> str; render_comparison(harness, plan) -> str; render_cycle(decision, state) -> str; render_closing(run) -> str; CEILING_REQUIRED_SENTENCES; BLOCK_REGISTER_HEADINGS","depends_on":["W0-CONTRACTS","W1-GRAPH","W2-DECIDE"],"tests":"tests/loop/test_report.py","acceptance":"Rendering refuses without CEILING.md at its pinned sha; every required ceiling sentence appears verbatim in every table and in the closing record; blocks print with counts by reason code; an all-blocked run renders as declined-to-read and never as no relations found; unread, unresolved and machine-unresolved print as three distinct states; no rendered artifact contains a score, a rank, a combined register or the token 'exhaustion'; losses_outside_P is present when empty; appellate_rulings 0 renders the not-validated sentence.","est_size":520,"touches_frozen":false},

 {"id":"W4-READER","wave":4,"path":"src/minireason/loop/reader.py","purpose":"Drive the reading trials over the pre-registered reading set and register every surviving reading; carry blocks, residue and the indeterminate list.","public_interface":"read_table(harness, table, standard, seats, config, records_dir) -> Readings; Readings.blocks; Readings.registered; Readings.indeterminate","depends_on":["W1-GRAPH","W3-TRIAL"],"tests":"tests/loop/test_reader.py","acceptance":"Only guarded readings reach the graph; a critic answering none ends the row at one call; a non-empty outside_vocabulary forces unresolved with the text preserved; multiple nominated relations are tried as separate trials and two survivors leave the cell contested rather than averaged; the planned call count equals the dispatched count on the offline fixture.","est_size":420,"touches_frozen":false},
 {"id":"W4-MARKER","wave":4,"path":"src/minireason/loop/marker.py","purpose":"C001 register marking over the residue markprep leaves: sealed baseline first, pairwise trials with mandatory order-swap, the program downgrade of differs to same at kind grain, and the falsifier evaluation.","public_interface":"mark_cell(harness, cell, baseline_sha, standard, seats, config) -> CellMarks; falsifiers(marks, program_findings) -> dict; REGISTERS","depends_on":["W2-MARKPREP","W3-TRIAL"],"tests":"tests/loop/test_marker.py","acceptance":"No cross-case pack renders before the baseline sha exists and is pinned into the call record; a differs whose difference_kind is present in the baseline kind set is written same by the program with the forcing replicate pair recorded; order-swap failure yields unresolved; the four registers are marked separately and never combined; G alone never carries D1; F2 and F3 fire only on T, E or D; a program finding of byte identity stands in the falsifier evaluation alongside the marks.","est_size":580,"touches_frozen":false},

 {"id":"W5-DRIVER","wave":5,"path":"tools/auto_loop.py","purpose":"The CLI and the S0-S15 state machine: preregister, preflight, publish plan, per-cycle prepare/publish/send/publish, import, use-table, read, mark, adjudicate, decide, publish, close, reopen and appeal; runner v2 and the importer invoked in-process; run.lock.","public_interface":"main(argv); preregister(config); preflight(config); run(config); status(run); adjudicate(run); appeal(run, path); reopen(run, ruling); close(run); dry_run(config, out)","depends_on":["W1-STEPS","W1-SYNTHETIC","W2-DECIDE","W3-AUDITS","W3-REPORT","W4-READER","W4-MARKER"],"tests":"tests/loop/test_auto_loop.py","acceptance":"One command walks S0 to S15 offline with zero sockets; publication precedes every dispatch and a PublishPending blocks the next dispatch; runner v2 is imported and send_round called in-process, never shelled; a second driver on the same run is refused; --cycles may only lower the budget; a killed run resumes without re-sending any coordinate that already has a request or attempt; a custody mismatch halts before dispatch with an erratum and a non-zero exit and is sticky until acknowledged; a provider failure ends one arm, mints no warrant and leaves the other arms running; an appeal applied at the next invocation flips a label through pass 1.","est_size":860,"touches_frozen":false},

 {"id":"W6-DRYRUN","wave":6,"path":"tests/loop/test_dry_run_end_to_end.py","purpose":"The acceptance proof: the whole loop offline against a real bare git repo, with every induced failure asserted by name in the closing receipt.","public_interface":"-","depends_on":["W5-DRIVER"],"tests":"self","acceptance":"Zero provider network calls, asserted by a provider-module counter; every git operation runs through publish() against a real temp bare repo so VERIFIED is exercised; the closing receipt names, by code, a provider failure that ended one arm while others continued, a custody mismatch that halted with an erratum and a non-zero exit and stayed sticky on resume, a step timeout, an ensemble split resolved to unresolved and not voted, a paraphrase flip that registered no warrant, a non-unique offset that registered no warrant, a baseline-kind collision that the program forced to same, a re-read refused for want of a reopen_reason, and an appellate ruling that flipped a label through pass 1; the closing receipt carries every sentence of CEILING_REQUIRED_SENTENCES verbatim.","est_size":700,"touches_frozen":false},
 {"id":"W6-DOC","wave":6,"path":"docs/workflows/automated-loop.md","purpose":"Operator page: the command, the config, the directory layout, every failure and block code, the pre-registration template, the obligations template and the ceiling text.","public_interface":"-","depends_on":["W5-DRIVER"],"tests":"tests/loop/test_docs_pins.py","acceptance":"Every failure code and every block code the driver can emit appears on the page; the pre-registration template contains budget, stop conditions, reading set, O, P, falsifiers and would-reopen; the ceiling text on the page is byte-identical to CEILING.md; the page states the two narrowings of section 6 and the two-credential concurrency fact.","est_size":420,"touches_frozen":false}
]
```

Twenty-four modules, seven waves of 6 / 6 / 4 / 3 / 2 / 1 / 2. Every `depends_on` entry
names a module in a strictly earlier wave, so each wave can be handed to that many
parallel agents at once. `W0-RECEIPTS` and `W0-PUBLISH` are deliberately decoupled:
`publish()` returns the VERIFIED line rather than writing it, and the driver wires it to
the ledger.

---

## 8. Pre-registration text for the ledger receipt

To be appended to `docs/DECISION_LEDGER.md` by `receipts.open_receipt` before any module
is written and before any call is made. The id is minted under the append lock.

> **REC-\<YYYYMMDD\>-\<X\> opened at \<UTC\>: pre-register the automated end-to-end
> harness loop as a mechanism intervention with its own identity.**
>
> **What this is.** A new instrument, not an observation and not an amendment. It
> automates three acts the published instruments reserve for root — the
> `use_relation_h005` reading cells, the C001 PLAN §8a contrast-register marks, and the
> continue/stop decision — together with the dispatch, import and publication that
> produce the material they read. It mints its own identity, `loop_plan_id =
> sha256(canonical(config ∪ pins))`, where the pins cover runner v2, the importer, the
> use-relation module, the contrast tool, the provider transport, `endpoints.json`, every
> prompt template, `obligations.json`, `CEILING.md` and the reading-rubric standard body.
> That identity is written to `experiments/loops/<RUN-ID>/plan.json` and published before
> the first provider call; the pre-registration timestamp precedes the first call and the
> record shows it.
>
> **What it does not amend.** It does not amend, reopen, supersede or reinterpret C001
> (`plan_id 328b9452c66fed52203015c540652d3b8ad3107d44dece56b55ebe721da341c8`) or H005,
> and it registers no finding on either. C001's material, its recoding table, its
> endpoint set, its replicate count, its §8a reading rule and its claim ceiling are
> consumed exactly as frozen and are not edited, reformatted or re-hashed. Any change to
> a frozen value would mint a new `plan_id` for that study under its own §13 and is out
> of scope here.
>
> **Why a mechanism intervention rather than an experiment.** The object under change is
> the instrument, not the world: what this run produces is a table of guarded readings
> and a decision record, and its own claim ceiling states that a reading is a registered,
> attackable `judge`-role artifact and not a finding, not a merit assessment, and never
> FW5:628's witness of reason use. Success for this receipt is that the mechanism runs
> from a config to a closing receipt without a human step, publishes before it dispatches,
> resumes without re-sending a spent coordinate, and records honestly what it declined to
> read. It is not that any cell filled.
>
> **Pre-registered before first look, and unchangeable inside this chain.** The cycle
> budget and `max_calls`; the stopping rule with its guard rails and its five O/P clauses;
> `obligations.json` with the failed set O and the protected set P, pinned by sha256; the
> reading set; the seat assignment with families and `key_env`; the audit schedule,
> `JUDGE_ERR_MAX` and `STREAK_MAX`; the planted-flaw calibration set; the guard parameters
> including `TRIAL_PARAPHRASE_N` and `schema_repair_budget`; the reopen-reason list; and
> `CEILING.md`. Changing any of them after first look mints a new `loop_plan_id` and is a
> new pre-registration, not an amendment to this one.
>
> **Two declared narrowings of published instruments.** First,
> `use_relation_h005.ROOT_READING_VOCABULARY` is published as a suggestion a row may
> exceed and root may write outside; this run closes it to six values so the cell is
> machine-fillable, and routes anything outside to `unresolved:outside-vocabulary` with
> the text preserved. Second, where that instrument's banner says "the reading is root's",
> this run's table says the reading is a guarded judge-role artifact and root has not read
> it. Both narrowings are in the claim ceiling and in the rendered tables.
>
> **Not authorised under this receipt.** Any edit to `src/creib/**`, to
> `src/minireason/provider.py`, to `src/deepreason_core/**` (including the one-line
> `ProvenanceRole` addition, which is declined as vendoring drift against
> `AHepi/DeepReason@9607fba`), to any published occurrence, or to any frozen plan. Any
> force push, amend, rebase, reset or history rewrite. Any credential written into any
> file, log, receipt or commit. Any retry of a spent provider call. Any averaging or
> majority vote over a judge disagreement. Any aggregate, weighted, ranked or summed
> field over the four registers or over any reading.
>
> **Honest consequence, stated in advance.** The guard is strict enough that this run may
> return mostly `unresolved` and stop at the no-new-reading-changes clause having resolved
> little. That is the rule working and is reported as a result about the instrument's
> reach, never as evidence about the material. A run that reads few rows before the
> declared ceiling is reported as a resource boundary with the unreached rows named as
> unreached, never as unresolved by inquiry.
>
> Pending until PREFLIGHT reports planned calls equal to dispatched with zero provider
> calls, the dry-run acceptance gate is green, and the plan is published and verified.

---

## 9. Risks and non-goals

### 9.1 Risks

**The guard buys stability, not truth.** Two cross-family seats agreeing under paraphrase,
order swap and an adversarial answer may be stably wrong in the same direction; shared
pretraining lineage is a common cause the design cannot see from inside. Ten family
labels over 24 endpoints, two credentials and one dominant host is a delivery fact. The
only levers are the planted-flaw calibration set, whose ground truth is true by
construction, and the appellate — and the appellate is optional by design, so a run with
no ruling has no exogenous anchor beyond the calibration set. This is the largest risk,
it is not fixable from inside, and the ceiling says so rather than letting it be
discovered later.

**Sycophancy hidden by unanimity.** The critic drafts the case; the defender defends the
null; if both judge seats lean the same way, unanimity conceals it and only calibration
catches it. Premise deletion is the sharpest available probe — a ruling that survives the
removal of its own stated grounds is easy to vary — but the residual is real and stated.

**Uniqueness is satisfiable vacuously.** A judge can quote a long neutral span that
resolves cleanly and says nothing. `count == 1` plus G3 kills fabricated and ambiguous
citations, which is worth having, and nothing more. Partial mitigation: `ν_bearing` is a
separate artifact, so "the quote is real but does not bear" is a registrable criticism
rather than an unavailable one.

**The variator is unaudited in both directions.** A weak variator produces near-identical
paraphrases and G7 passes trivially; a strong one produces content-changing paraphrases
and G7 blocks everything. The span-survival assertion catches the second class only where
it disturbs a quote. The block register makes a suspiciously high flip rate visible; a
trivially passing screen is not detectable from inside and is declared.

**Unresolved-heavy runs look like failures and are not.** A chain that resolves nothing
stops at clause 4 having learned little about the material and something real about the
instrument. The pre-registration names the unresolved rate at which the instrument would
be judged not worth running again — **as information, not as a threshold that
adjudicates**.

**Cost.** A fully guarded row costs roughly nine calls, doubled for order-swap on marks,
plus audits. With 5 concurrent per credential over two credentials, the budget will
usually end the chain at clause 5. That stop is a declared resource boundary and the
record says so in those words; and a run that reads 40 of 400 rows must never render the
other 360 as unresolved by inquiry rather than unreached by spend. The renderer enforces
the distinction and `preflight` refuses a plan whose call count exceeds `max_calls`.

**The marker inherits C001's own confounds.** The fcl CARRIER block is +7.3 % on ORIGINAL
(PLAN §2); a length-sensitive judge can produce an ORIGINAL/CARRIER `differs` from block
size alone. The program cannot rule this out, so that rival stays registered as a live
alternative exactly as PLAN §11 L5 already requires.

**Single-process ceiling.** The five-per-key guarantee holds only inside one process.
Shelling the runner, or a second driver started by hand, silently doubles concurrency.
`run.lock` and in-process invocation address this; a cross-machine run does not, and the
design does not claim to cover it.

**Ledger contention.** Another agent publishes on this branch. Byte-mode locked appends
with in-lock id minting make the ledger safe; `git push` is not, and a rejected push must
be re-fetched and re-attempted as a new publish step, never force-pushed.

**Publication coupling.** Publication-before-dispatch makes every cycle depend on the
remote, so an unattended run can stall on an infrastructure fault. That is intended — a
run whose inputs are not durable should not spend credentials — and the state machine
records the stall truthfully and resumes without dispatching to catch up.

**Automation drift into adjudication.** The tempting next features are "let the panel
decide whether to continue" and "let the marks feed a score". Both are forbidden; the
tests asserting no aggregate key, no LLM in `decide.py`, and no scoring key in any
rendered header exist to make the drift fail loudly.

**Synthetic-only proof.** A green dry run proves the *loop*, not the readings. It says the
machine runs without a human; it says nothing about whether a reading it produces is any
good, and the closing receipt must not let the two be confused.

**Automation mistaken for authority.** The deepest risk is presentational: a filled table
looks more settled than an empty one. Every countermeasure is structural — the reading is
a `critic`-provenance artifact, the default is unresolved and reinstates by computation,
the ceiling block is unremovable from the renderer — but none prevents a later reader from
quoting a cell without its provenance. That is what the appellate channel is for, and why
it stays open forever.

### 9.2 Non-goals

This design does **not**: rank, score or compare endpoints, families or models for merit;
produce FW5:628's witness of reason use, or any structural map on an active dependency
route; establish repair, progress, historical newness, recursive critical capacity, an
`Account` predicate or a `ProducedBy` claim about any studied system; generalise beyond
one node, one problem and the one respect the material fixes; treat provenance as
evidence; make any count a warrant; amend C001 or H005; edit `deepreason_core`, extend
`ProvenanceRole`, or touch `src/creib/**`, the owner runner, `src/minireason/provider.py`,
any published occurrence or any frozen plan; require a human at any step; or claim that a
run without an appellate ruling has been validated, checked or confirmed.
