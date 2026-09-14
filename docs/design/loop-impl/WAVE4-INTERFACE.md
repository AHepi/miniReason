# Wave 4 — the integrated public interface

Read `WAVE0-INTERFACE.md`, `WAVE1-INTERFACE.md`, `WAVE2-INTERFACE.md` and
`WAVE3-INTERFACE.md` first; where they differ, the later one governs. This is
the wave-4 integrator's record of what the two wave-4 modules expose after
reconciliation with the **real** `trial.py`, the disposition of every
acceptance clause, what was kept from the Kimi K3 drafts and what was rewritten
with the reason, the bundle-facing consequences, and the questions W5-DRIVER
and W6-DRYRUN must answer.

Clone: `scratchpad/loop-impl/repo`, branch cut at `9045a94`; the loop tree is
untracked there and **nothing was committed**.
Sources: `src/minireason/loop/{reader,marker}.py`, with one edit in `types.py`
(the five folded codes); tests: `tests/loop/test_{reader,marker}.py` and
`tests/loop/test_{types,contracts}.py`.

Drafts: `loop-impl/wave4-drafts/{reader,marker}/`. The reader run was labelled
COMPLETE (its own suite green against a *fake* trial); the marker run was cut
by a ruling-13 gateway close after both files were written, so its suite state
was unknown. Both were drafted against the **declared** W3-TRIAL interface with
an injected runner, before `trial.py` existed (owner ruling 16).

**Test lines, exactly as run.** Every run is
`PYTHONPATH=$PWD/src python3 -m unittest …` from the clone root; the
`PYTHONPATH` is load-bearing, because an editable install of `minireason`
points at the live checkout and wins otherwise.

| what | before | after |
|---|---|---|
| `tests.loop.test_reader` as delivered | `Ran 41 tests in 0.567s` `FAILED (failures=1)` | `Ran 53 tests in 2.353s` `OK` |
| `tests.loop.test_marker` as delivered | `Ran 42 tests in 0.097s` `FAILED (failures=1)` | `Ran 58 tests in 3.139s` `OK` |
| loop suite, quiesced tree (`discover -s tests/loop -t .`) | `Ran 1428 tests in 24.777s` `OK (skipped=1)` | `Ran 1539 tests in 29.660s` `OK (skipped=1)` |
| whole repository (`discover -s tests`) | `Ran 2671 tests in 201.749s` `OK (skipped=2)` † | `Ran 2782 tests in 201.987s` `OK (skipped=2)` |

The two before-lines are the drafts **as delivered**, copied into the clone at
the design's paths and run before any edit. Each failed on exactly one test,
and both were the same reconciliation debt: the draft asserted that
`minireason.loop.trial` was *absent* (`ImportError not raised`;
`ModuleSpec(...) is not None`). Everything else in the reader draft passed —
against a fake whose shape the real class does not have, which is why a green
line said so little.

† The repository before-line is `WAVE3-INTERFACE.md`'s recorded after-line, not
one this pass re-measured; the loop-only before-line **was** measured here, on
the tree as it stood before the first copy. The arithmetic checks exactly:
2782 − 2671 = 111 = 53 + 58, and 1539 − 1428 = 111.

No provider call was made, no credential was read or printed, and nothing
outside the clone was written.

---

## 0. The map after wave 4

| module | imports (siblings only) |
|---|---|
| `reader` | `contracts`, `custody`, `graph`, `roles`, `standard`, `trial`, `types` |
| `marker` | `contracts`, `custody`, `graph`, `markprep`, `packs`, `roles`, `standard`, `trial`, `types` |

**No wave-4 module imports the other.** The exact edge set is asserted by
`tests/loop/test_contracts.py::WOneOwnerPerSharedConstant::test_the_import_graph_is_the_one_the_interface_documents`,
which now carries both stems with the reason for every edge beyond
`depends_on`.

Edges beyond the wave plan's `depends_on`, each because a spelling has one
owner:

* **`reader`** (`depends_on: [W1-GRAPH, W3-TRIAL]`) additionally reaches
  `types` (`LoopError`), `custody` (the fence and the write-once write),
  `standard` (the rubric's absolute mode and the `outside_vocabulary` field
  name), `contracts` (`assert_no_scoring_keys`, G12 over every record it
  emits), and `roles` (`RECORD_FIELD`/`RECORD_KIND` — how a claimed coordinate
  that answered is told from one that did not; see §8 question 2). It reaches
  `obligations` **not at all**: the disposition tokens are mirrored and the
  mirror is asserted by test, so W4 adds no edge to W1-OBLIGATIONS.
* **`marker`** (`depends_on: [W2-MARKPREP, W3-TRIAL]`) reaches the same owners
  the *relation* trial is built out of, because it owns the **pairwise** guard:
  `packs` (the register pack and its two presentation orders), `roles` (the
  call and its write-once record), `markprep` (the cell shape, the seal, the
  pairwise surface, the baseline, `resolve_pair`), `graph` (the mark's door),
  `contracts` (G12 and the closed kind sets), `standard` (the registers, the
  marks, the falsifier map), `custody` (the write-once marks record), and
  `trial` (the **block vocabulary and the guard-check names**, imported and
  never retyped — which is what makes the declared W3-TRIAL edge real).

---

## 1. `reader.py` — W4-READER

**What it is.** One pass over the pre-registered reading set. It speaks to no
model (W3-TRIAL does, through W2-ROLES), builds no reading (W3-TRIAL does) and
adjudicates nothing (W1-GRAPH does). It owns the *row* bookkeeping: one trial
per row, the coordinate-grain resume rule, the write-once row records, the
planned/dispatched accounting, and the decision to open the graph's door on a
survivor.

**Entry points.** `read_table(harness, table, standard_body, seats, config,
records_dir, *, trial_runner=trial.run_trial,
registered_by=graph.register_reading, provider_factory=None,
reopen_reason=None, framing=None) -> Readings`;
`unanswered_coordinates(records_dir) -> tuple[str, ...]`;
`ReadingRow.coerce(value)`.

**Records.** `Readings(blocks, registered, indeterminate, dispositions, unread,
planned, dispatched)`; `ReadingRow(row_key, surface, cell=None)`;
`BlockRecord(row_key, cell, code, check, detail, prompt_ref_path,
raw_ref_path, prompt_sha, raw_sha)`; `IndeterminateRecord(row_key, coordinate,
detail)`; `RowDisposition(row_key, cell, reason, text)`;
`RegisteredReading(row_key, cell, relation, seat, roles, ids)`.

**The five registers are kept separate and never combined.** `blocks` is what
o4's `blocks_named` reads; `dispositions` is what o1's closed reason set
reads; `indeterminate` is §4.3's own list; `registered` is what reached the
graph; `unread` is every open cell nothing read. A row can appear in two of
them — an `outside_vocabulary` row is both a disposition o1 reads **and** a
`blocked:outside-vocabulary` o4 counts — and neither stands in for the other.

**What it reads off a `TrialResult`, and nothing else.**
`outcome` (a **string** in `trial.OUTCOMES`), `blocks` (a tuple of
`trial.Block`), `critic.outside_vocabulary`, `reading` (the
`graph.ReadingResult` a sustained trial built) and `standard_id`. It builds no
`ReadingResult` of its own — asserted by execution and by
`OnlyGuardedReadingsReachTheGraph::test_the_registered_reading_is_the_trials_own_not_a_rebuild`.

**Outcome mapping.**

| `TrialResult.outcome` | reader's registers |
|---|---|
| `sustained` | `registered` (through `registered_by`), cell read/contested |
| `blocked` | `blocks`, one `BlockRecord` per `trial.Block` |
| `unresolved` (G4/D6) | `dispositions` (`unresolved:outside-vocabulary`, text verbatim) **and** `blocks` (`blocked:outside-vocabulary`) |
| `no-trial` (critic `none`) | `dispositions` (`critic-none`); `blocks` empty |
| `not-sustained` | `dispositions` (`not-sustained`); nothing registered |
| a claimed-and-unanswered coordinate | `indeterminate`; the row is **not dispatched** |

**Exceptions and codes.** `ReaderError(code, detail="")`, a `types.LoopError`.

| code | table | raised where |
|---|---|---|
| `READER_ROW_INVALID` | `types.FAILURE_CODES` (new, folded in) | a row with no `row_key` or no surface, or a cell key `graph` refuses |
| `READER_ROW_DUPLICATE` | `types.FAILURE_CODES` (new, folded in) | two rows of one table carry one `row_key` |
| `READER_OUTCOME_UNKNOWN` | `types.FAILURE_CODES` (new, folded in) | an outcome outside `trial.OUTCOMES`, or a `sustained` carrying no `ReadingResult` |

---

## 2. `marker.py` — W4-MARKER

**What it is.** C001 register marking over the residue W2-MARKPREP leaves, and
the falsifier evaluation. It owns the **pairwise** guard and the G8/G9/G10
ordering; it decides nothing about a cell's standing (W1-GRAPH does).

**Entry points.** `mark_cell(harness, cell, baseline_sha, standard, seats,
config, *, records_dir, residue=None, marker_caller=roles.call_marker,
registered_by=graph.register_mark, provider_factory=None, out_dir=None) ->
CellMarks`; `falsifiers(marks, program_findings=None) -> dict`; `REGISTERS`.

**Records.** `CellMarks(cell, endpoint, arm, baseline_sha256, comparisons,
program_findings, calls)`; `RegisterMarks(comparison, left_case, right_case,
rows)`; `MarkRow(comparison, left_case, right_case, register, mark,
difference_kind, source, block, forced_by, checks, evidence, baseline_sha256,
registered)`.

**Guard checks.** `GUARD_CHECKS` names nine, in §2.4's order:
`G8-baseline-seal`, `G10-program-pre-empt`, then `G1-schema`,
`G2a-uniqueness`, `G3-operative-target`, `G5-unanimity`, `G6-order-swap`,
`G9-replicate-baseline`, `G12-no-scoring-key`. Every one prints on every row as
`performed` or `not_performed`. The seven that are not G8/G9/G10 are
**`trial`'s own constants**, imported.

**Why it does not call `trial.run_trial` — verified by execution.** The draft
called it with `mode="pairwise"`. The trial as built refuses that call twice
over, and
`tests/loop/test_marker.py::TheRelationTrialRefusesAPairwiseCall` demonstrates
both refusals: `mode != standard.MODE_ABSOLUTE` raises
`TRIAL_MODE_UNEXPECTED`, and a `graph.CellKey` naming a register raises the
same code with the message *"marks run pairwise through W4-MARKER's caller,
not through the relation trial"*. W3-TRIAL's own record says the same in three
places (module docstring; deviation 2; WAVE3-INTERFACE §1, which records
G8/G9/G10 as absent on purpose). So the pairwise leg is this module's, built
out of the same owners, and the W3-TRIAL edge the wave plan declares is the
block vocabulary and the guard-check names.

**The pairwise leg, step by step.** Per residue row: pick the first *readable*
replicate on each side (`markprep`); build the pairwise surface (which
re-asserts G8); render the register pack through `packs.render_register`
(**where G8 lives**, and where the seal is pinned into the pack record);
`packs.both_orders`; then each of the **two judge seats** (§2.2, "the marker
reuses the judge pair") × **both** presentations through `roles.call_marker`;
then G1 (a blocked call ends the row), G2/G3 (`markprep.resolve_pair` on the
two citations, against the material), G5 (the two seats at the as-declared
presentation, on `(mark, difference_kind)`), G6 (each seat's two
presentations), then G9. Every failure leaves the row `unresolved` with its
block code; a split records **both rulings verbatim** and is never averaged or
voted.

**A mark's transcript.** The marker contract carries no `decisive_point` — no
seat picks one — but W1-GRAPH's rubric-typed warrant demands a conforming
transcript. The program composes one and asserts by program that it resolves
exactly once in `case + "\n" + answer`:

* a **trial** mark: the exchange is the two seats' cases at the as-declared
  presentation, and the point is the program's framing of the two citations G2
  already resolved against the material (`CITATION_FRAME`);
* a **program** mark (G9's downgrade, G10's pre-empt): there are no seat cases,
  so the exchange is the program's own verdict line (`PROGRAM_POINT`) and the
  kind-grain evidence behind it, and the reading's `seat` is `"program"`.

Where the point does not resolve exactly once the row becomes `unresolved`
under `blocked:referential-integrity` — W1-SURFACE's own code, not a private
one.

**Registration.** `differs` and `same` enter through
`graph.register_mark`, one register at a time; `unresolved` registers nothing,
because `unresolved` **is** the cell's standing and
`graph.ReadingResult.validated` refuses it as a mark. Every register cell the
pass could register into is named **before any call is spent**.

**Exceptions and codes.** `MarkerRefused(code, detail="")`, a
`types.LoopError` and a `ValueError`.

| code | table | raised where |
|---|---|---|
| `MARKER_INPUT_MALFORMED` | `types.FAILURE_CODES` (new, folded in) | a cell, seal, seat plan, config, records dir, residue row, mark row or marks value that is not the record it names; a register cell that was never opened |
| `MARKER_RESIDUE_CONTRADICTED` | `types.FAILURE_CODES` (new, folded in) | a row offered that the program already decided; a side with no readable replicate |
| `BASELINE_NOT_FIRST` | `types.FAILURE_CODES` (already there) | G8, on an unsealed cell or a sha the cell does not carry |
| the ten `blocked:*` | `types.BLOCK_CODES` | **returned on `MarkRow.block`**, never raised |

---

## 3. The code tables after wave 4

`types.FAILURE_CODES` now carries **210** members; five were folded in this
pass (three `reader`'s, two `marker`'s). `types.BLOCK_CODES` is unchanged at
**ten**, `types.OUTCOME_CODES` at **one**, `types.CEILING_BLOCK_REASONS` at
**nine**. `tests/loop/test_types.py`'s `FOLDED_IN` now names **twenty-one**
modules and `FRONTIER` is empty; `TOKEN_ARGUMENT` gained three entries
(`reader.ReaderError`, `marker._refuse`, `marker.MarkerRefused`).

**Three codes the reader draft declared were dropped, with the reason**, under
wave 3's own rule that a code no call site reaches is a code no register
prints:

* `READER_RELATION_UNKNOWN` — the draft's rows *declared* the relation under
  trial and refused a token outside the vocabulary. The critic nominates the
  relation (§2.3) and G4 is its only gate; `graph.ReadingResult.validated`
  refuses an unknown token at the door. Two owners, so the reader's went.
* `READER_UNRESOLVED_NOT_A_READING` — the same: `graph` already refuses
  `unresolved` as a reading with `READING_TOKEN_UNRESOLVED`, and the draft's
  own deviation 4 admitted it "decides nothing the graph would not have
  refused".
* `MARKER_STANDARD_MISMATCH` — the draft parsed the standard itself to check
  it carried `registers`/`falsifiers`. `packs.render_register` parses it and
  refuses; the marker now passes the body through untouched.

One code was **added** that the draft did not declare: `READER_ROW_DUPLICATE`.
Two rows with one key collide in the write-once records tree *and* on one
trial coordinate, and the honest place to say so is before the second trial.

---

## 4. Disposition of every acceptance clause

### W4-READER

| clause | disposition | test |
|---|---|---|
| only guarded readings reach the graph | **Rewritten.** The draft never ran a guard: it read a fake six-token `outcome.status`, rebuilt a `ReadingResult` from attributes the real class does not publish, and coerced a `transcript` record the real class spells as text. The module now registers the trial's own `ReadingResult` and nothing else. | `OnlyGuardedReadingsReachTheGraph` (7 tests, incl. `test_a_referential_integrity_block_registers_nothing`, `test_an_ensemble_split_blocks_and_registers_nothing`, `test_a_not_sustained_trial_registers_nothing_and_says_it_was_read`) |
| a critic answering `none` ends the row at one call | **Kept in shape, rewritten in fact.** The draft matched a `critic-none` status the trial does not emit; the real outcome is `no-trial`, and the "one call" is now counted off the provider factory rather than asserted. | `ACriticAnsweringNoneEndsTheRowAtOneCall` (4 tests, incl. `test_exactly_one_call_is_dispatched`) |
| a non-empty `outside_vocabulary` forces `unresolved` with the text preserved | **Rewritten.** The real trial returns `OUTCOME_UNRESOLVED` **with a block attached**, and the draft's `if status == BLOCKED or trial_blocks: continue` swallowed the row into the block register, so the disposition and the preserved text were unreachable on a real result. Both registers now carry it. | `OutsideVocabularyForcesUnresolvedWithTheTextPreserved` (5 tests, incl. `test_the_text_is_preserved_verbatim_on_disk` and `test_the_guards_own_block_is_kept_beside_the_disposition`) |
| multiple nominated relations are separate trials; two survivors leave the cell contested, never averaged | **Rewritten.** The draft's two "trials" shared one records directory, which the real W2-ROLES refuses as `NO_REPLAY`; each row now spends its own. Two rows on one cell, two real guarded trials, two registrations, `graph.CONTESTED`. | `MultipleNominationsAreSeparateTrialsAndTwoSurvivorsAreContested` (6 tests, incl. `test_each_trial_spends_its_own_records_directory` and `test_a_survivor_and_a_block_leave_the_cell_read_not_contested`) |
| the planned call count equals the dispatched count on the offline fixture | Kept, and **made falsifiable**: the identity can now differ, because a claimed-and-unanswered coordinate refuses a re-send, so "equal" is a fact about this pass and not a tautology. | `PlannedEqualsDispatchedOnTheOfflineFixture` (5 tests) and `AClaimedCoordinateThatNeverAnsweredIsIndeterminate::test_the_row_is_not_dispatched` |

### W4-MARKER

| clause | disposition | test |
|---|---|---|
| no cross-case pack renders before the baseline sha exists and is pinned into the call record | **Extended.** The draft asserted the refusal; the second half — *pinned into the call record* — was never checked. Now every call record is opened and read back. | `NoCrossCasePackRendersBeforeTheBaselineShaIsPinned` (5 tests, incl. `test_the_sha_is_pinned_into_every_call_record`) |
| a `differs` whose `difference_kind` is in the baseline kind set is written `same` by the program with the forcing replicate pair recorded | **Kept in shape, rewritten in fact.** The draft's fixture cells had an **empty** baseline kind set for every register, so the branch it tested never ran; `baseline_exhibiting_cell()` builds one whose within-ORIGINAL replicates really do differ on D's two kinds, and the test asserts that first. | `ADiffersInTheBaselineKindSetIsWrittenSameByTheProgram` (5 tests, incl. `test_the_baseline_really_exhibits_the_kind`, `test_the_forcing_replicate_pair_is_recorded`, `test_a_kind_absent_from_the_baseline_stands_as_differs`) |
| order-swap failure yields `unresolved` | **Rewritten.** The draft delegated the order swap to the trial's acceptance and ran **one** call per row; the marker now runs both orders for both seats and adjudicates the flip itself. | `AnOrderSwapFailureYieldsUnresolved` (5 tests, incl. `test_both_orders_are_always_run` and `test_two_seats_disagreeing_at_one_presentation_is_a_split_not_a_vote`) |
| the four registers are marked separately and never combined | Kept; **extended** to the call record (one register per call, and the record says which) and to the two program pre-empts. | `TheFourRegistersAreMarkedSeparatelyAndNeverCombined` (7 tests, incl. `test_a_register_the_program_settled_is_never_put_to_a_seat` and `test_register_e_forced_unresolved_by_a_bare_token_reaches_no_seat`) |
| G alone never carries D1 | Kept; **extended** with a run in which G really is marked `differs` and D1 still does not fire. | `TheFalsifierMapIsReadAndNeverRestated::test_a_differs_on_g_alone_never_fires_d1`, `::test_g_is_excluded_from_every_falsifier` |
| F2 and F3 fire only on T, E or D | Kept; read off `standard.FALSIFIER_MAP` and asserted equal to the frozen map's own bytes. | `TheFalsifierMapIsReadAndNeverRestated` (7 tests) |
| a program finding of byte identity stands in the falsifier evaluation alongside the marks | Kept; **extended** so the finding rides *on* the entry (`program_finding`) and the carried marks stand beside it rather than being replaced. | `AProgramFindingOfByteIdentityStandsInTheFalsifierEvaluation` (6 tests) |

---

## 5. Kept versus rewritten, with the reason

### `reader.py`

**Kept.** The five-register shape and the refusal to combine them; the
row-disposition vocabulary and its mirror of `obligations.DISPOSITION_REASONS`
asserted by test rather than imported; the write-once row records through
W0-CUSTODY; the `planned`/`dispatched` identity as an identity and never a
ratio; the injection points as *seams* (now defaulting to the real functions);
the module's refusal to average, merge, rank or vote; most of the prose.

**Rewritten — 1. the fake `TrialResult`.** Four spellings, none of them the
real class's: `outcome` as an object with a `.status` in **six** tokens
(`sustained`, `blocked`, `not-sustained`, `critic-none`, `outside-vocabulary`,
`indeterminate`) where the real one is a **string** in **five**
(`OUTCOME_NO_TRIAL` and `OUTCOME_UNRESOLVED` replace three of the six, and
`indeterminate` is not a trial outcome at all); `blocks` as records with
`reason`/`prompt_ref`/`raw_ref`/`coordinate` where `trial.Block` publishes
`code`/`check`/`detail`/`prompt_ref_path`/`raw_ref_path`/`prompt_sha`/`raw_sha`;
`transcript` as a record coerced field-by-field where the real one is the
emitted transcript **text**; and no use of `TrialResult.reading` at all.
Read against the real class, the draft would have raised
`READER_OUTCOME_UNKNOWN` on every row.

**Rewritten — 2. the reading was rebuilt rather than carried.** The draft
assembled its own `graph.ReadingResult` from `outcome.seat`, `outcome.roles`,
`outcome.school` and `outcome.body`. That is a second owner of the seat
spelling — the exact defect WAVE3-INTERFACE §6 found in the audit layer's
invented `judge-1` panel, which attached six warrants to an empty window. The
module now carries `TrialResult.reading` through untouched, which answers
WAVE3 question 4 by removing the question.

**Rewritten — 3. the row declared the relation.** `ReadingRow` required a
`relation` in `standard.NOMINABLE_RELATIONS` and passed it to no one; the
critic nominates it and G4 is its only gate. A row that declared one would be
the reader telling the guard what it must find.

**Rewritten — 4. `run_trial` was called with the wrong arguments.** The draft
omitted `key=` and `records_dir=`, both of which the real `run_trial` requires
and refuses without (`TRIAL_ARGUMENT_INVALID`) — *"a trial that cannot name its
cell cannot refuse a re-read"*. It also passed no `provider_factory`, so
W6-DRYRUN could not have run the reading arm offline through it.

**Rewritten — 5. two trials of one cell shared one records directory.** Which
W2-ROLES refuses as `NO_REPLAY` on the second critic call. Each row now gets
`<records_dir>/<row_key>/`, which is also design §4.2's own layout.

**Added — the `INDETERMINATE` scan and the `unread` inventory.** §8 questions 2
and 3.

**Fixture rewrites (the draft's tests, not its module).** The whole file was
rebuilt on the house `OfflineProvider` fixture (`tests/loop/test_roles.py`'s,
as `test_trial.py` uses it), with the socket layer removed, so every test drives
the real guard. Two tests still inject a runner: one watches the keyword set
reaching `run_trial` (the dry run's seam), and one replaces the `outcome` field
of a **real** `TrialResult` to reach `READER_OUTCOME_UNKNOWN`. Neither bypasses
a guard.

### `marker.py`

**Kept.** The G9/G10 precedence and the rule that where the program decided no
seat is asked; the residue-contradiction refusal; the `MarkRow`/`RegisterMarks`/
`CellMarks` shape with no aggregate view and no `combined` property; the
per-register `__post_init__` validation against the closed kind sets; the
falsifier evaluation's structure, its reading of `carrying_registers` /
`excluded_registers` off the frozen map, and its refusal to merge `fired` with
`defeated`; the `REGISTERS = standard.REGISTER_IDS` import; most of the prose.

**Rewritten — 1. the trial it called does not exist.** See §2. The pairwise
guard is now the module's own, over `packs` + `roles` + `markprep` +
`trial`'s block vocabulary.

**Rewritten — 2. one call where the design requires four.** The draft made
**one** `run_trial` call per residue row and relied on the trial to run both
orders. A mark is one call per (cell, comparison, register) **per seat per
presentation**: two seats × two orders. The draft could not have produced an
order-swap block or an ensemble split at all, which is why its "order-swap
failure yields unresolved" clause passed against a fake that simply returned a
block code.

**Rewritten — 3. a sustained trial's mark was `differs` by fiat.** The draft
wrote `mark = differs` whenever the outcome was `sustained` and the row had
exactly one open kind, and `unresolved` whenever it had more than one. The
marker contract returns the mark and the kind; a seat answering `same` on a
residue row is an answer, not a blank, and the draft could not express it.

**Rewritten — 4. four corrupted `raise` sites.** `MarkerRefused(FRONTIER,\n
MARKER_INPUT_MALFORMED, …)` appears four times in the draft — the module's
`FRONTIER` tuple pushed in front of the code by an editing slip, so the
refusals would have carried a tuple where a receipt token belongs. None was on
a path the draft's own suite executed, and its 42-test run failed on exactly
one assertion — that `trial.py` was absent. (Kimi report §4.1,
*write-once-and-walk-away*: the file was never exercised along those
branches.)

**Rewritten — 5. `FRONTIER` as a module attribute.** The draft published
`FRONTIER = ("marker",)` so that `test_types.py` would admit an unfolded
module. `FRONTIER` is the **test's** table, not a module's claim about itself;
the wave-4 integrator folds the codes and moves the stem, which is what
happened here.

**Rewritten — 6. no pack was ever rendered, so G8's own enforcement point was
never reached.** The draft imports neither `packs` nor `roles` nor `graph`
(checked: zero occurrences of `render_register`, `roles.`, `call_marker`,
`register_mark` or `graph.` in `wave4-drafts/marker/marker.py`). G8 is enforced
in `packs.render_register` **and nowhere else**, so the draft's clause-1 test
asserted `markprep`'s seal and could not assert *"the sha is pinned into the
call record"* — there was no pack and no call record to pin it into. The
integrated module renders through `packs.render_register`, which also exposed
a second spelling: `markprep.Cell` spells its id `cell_id` while
`packs._cell_id` reads a string, a mapping or `.cell` (`graph.CellKey`'s
spelling), so the id is handed over rather than the record.

**Added — registration.** The draft returned `CellMarks` and registered
nothing, so no mark reached `graph.mark_triples` and decide's clause 4 would
have compared an empty set every cycle. Marks now enter through
`graph.register_mark`, one register at a time.

### Declined, with the reason

* **Sealing a second baseline for E and G** (WAVE3 question 5, wave-1 decision
  53). Verified by execution: `markprep.NOT_PROGRAM_READ` names
  `record_engaged`, `engagement_form` and `grounds_source`, so **the program's
  sealed baseline can only ever carry kinds for T and D**, and G9's downgrade
  can never fire on E or G. Decision 53's second sealed artifact is therefore
  still needed and is still missing. It is declined here because sealing it
  means putting every within-ORIGINAL replicate *pair* to the seats on E and G
  under the same pairwise guard — on a three-replicate case that is 3 pairs ×
  2 registers × 2 seats × 2 orders = **24 further calls per cell**, which
  `reading_set.json`'s `max_calls_derivation` (`0+108+242+46+0`) does not
  carry. That is a pre-registration change, not an implementation choice. §8
  question 1.
* **Computing the guard-block streak.** WAVE3 §8 question 1 settled the
  definition and assigned the counter to W5-DRIVER; the reader returns the
  per-row block records in dispatch order, which is exactly what that counter
  consumes, and implements no counter of its own.
* **Registering the `rendered_files` record** (WAVE3 question 9). W3-REPORT
  builds it; W5-DRIVER registers it. Nothing in wave 4 renders a file.

---

## 6. The metric-creep lens (ruling 7)

Run over both modules by AST and by reading every emitted record.

* **No score, rank, rate, average, mean, majority, vote, aggregate, combined or
  total** appears as a string constant, a field name or a computation in either
  module. `sum`, `max`, `min`, `round` and `abs` are called nowhere;
  `statistics` and `Counter` are imported nowhere. The only binary operators
  are string concatenation and set union/intersection.
* **`planned` / `dispatched`** are the one pair of integers either module
  carries. They are class (i) of the REVIEW-PREREG audit — a **spend** boundary,
  the PREFLIGHT identity of design §4.1 S1 — and they are reported as an
  identity (`planned_equals_dispatched`), never as a ratio. A test asserts the
  module contains no division.
* **Block counts** are the report's (design §2.4: "Blocks are counted,
  published and named"); the reader returns block *records*, not a count, and
  the count is W3-REPORT's per reason code.
* **`"exhaustion"`** appears in neither module, asserted by test in both.
* **No ordering** is defined on marks, registers or falsifiers; a test parses
  `falsifiers` and refuses `<`, `>`, `<=`, `>=` and every arithmetic operator
  inside it.
* `contracts.assert_no_scoring_keys` (G12) runs over **every** record either
  module emits before it is written or returned.

---

## 7. Bundle-facing consequences (REVIEW-PREREG.md)

| item | what wave 4 changes |
|---|---|
| **PR-13** — the unread inventory, eleven against twelve | **The program half is now supplied.** `Readings.unread` is every cell open in the graph that this pass registered no reading for, read off the graph's own cell-open artifacts and **not** off the reading set, so a cell the reading set never named is still named unread. W3-REPORT unions it with the plan's rows. The bundle half stands unchanged: `PREREG.md`'s "eleven" must become **twelve**, or say which twelfth it excludes and why; the program can supply the inventory but cannot supply the prose that says the inventory is complete. |
| **PR-05** — `p4` unfalsifiable on rendered files | **Unchanged by wave 4, and the writer's side is still W3-REPORT's.** Wave 4 renders no file. What it adds is that G12 now runs over the reader's and the marker's own records too, so nothing either module hands the driver can carry a scoring key into `rendered_files`. |
| **the six-value vocabulary (PR-25)** | **Unchanged and still unverifiable from the bundle.** W4-READER imports `standard.MODE_ABSOLUTE` and nothing else of the vocabulary — the relation is the critic's and G4's — and W4-MARKER imports `standard.MARKS`, `standard.REGISTER_IDS` and `standard.FALSIFIER_MAP` by reference. Every one is a symbol in `loop-impl/repo/src/minireason/loop/`, which is not a bundle file. PR-25's remedy stands: enumerate the six values, the three marks, the per-register difference-kind sets and the block-code set in `PREREG.md`, and name `STANDARD_BODY_SHA256` beside the ceiling digest. |
| **PR-12** — block-code spelling | **Held on the wave-4 side.** Neither module writes the `blocked:` prefix in a string literal; the marker imports all six spellings it can emit from `trial`, which imports or builds each through `types.block_code`. Asserted by test in both files. |
| **PR-20 / decision 53** — the known-in-advance shape of the contrast leg | **Sharpened into a mechanical fact.** Because the program's baseline can carry kinds only for T and D (§5, declined), a `differs` on **E or G can never be downgraded by G9**, while a `differs` on T or D can. §6's honest expectation should say so in those terms, so the run's C001 output cannot later read as a finding about the material. |
| **PR-01 / PR-06 / PR-07 / PR-08 / PR-09** | Unchanged by wave 4; see WAVE3-INTERFACE §7 and WAVE2-INTERFACE §10. |

---

## 8. What W5-DRIVER and W6-DRYRUN must answer

Carried forward from WAVE3-INTERFACE §8 where still open, and new where wave 4
opened one. WAVE3 questions **2, 3 and 4** are closed by §1 above.

1. **The second sealed baseline for E and G** (WAVE3 question 5, still open and
   now measured). The program's baseline is empty for E and G *by
   construction*, so either (a) the pre-registration accepts that G9 bites only
   on T and D and says so in `CEILING.md` and §6's expectation, or (b) a second
   sealed artifact is added and `max_calls` is re-derived with 24 further calls
   per cell. **This cannot be settled in code**: it is a bundle decision, and
   whichever is chosen must be in the plan before S0.
2. **`steps.scan_coordinates` does not read the reading arm's records.** It
   reads `requests/`, `attempts/` and `responses/` — runner v2's dispatch tree —
   while W2-ROLES claims a coordinate as `<records_dir>/<key>/<role>/` with a
   `provider/` subdirectory and a `call.json`. `roles._claim`'s own docstring
   says *"`scan_coordinates` reads it as started"*, and on these bytes it does
   not: `tests/loop/test_reader.py::AClaimedCoordinateThatNeverAnsweredIsIndeterminate::test_the_scan_reads_the_roles_layout_not_the_steps_one`
   shows `scan_coordinates(...).indeterminate == frozenset()` where
   `reader.unanswered_coordinates(...)` finds the claim. W4-READER supplies the
   reading arm's list; **W5-DRIVER must decide** whether the SEND arm keeps
   `steps.scan_coordinates`, whether the two layouts converge, and it must
   correct the `roles._claim` docstring either way.
3. **Who opens the register cells.** `mark_cell` refuses, before any call, if a
   `(cell, register, comparison)` default is not open (§3(c) puts that at
   PREREGISTER). W5-DRIVER must open every register cell of every attached
   contrast occurrence at S0, and PREFLIGHT must assert the set it opened is the
   set `markprep.program_marks` will produce.
4. **The seat spelling of a program-written mark is `"program"`.** It is the
   `seat` on the `ν_soundness` of every G9/G10 mark, so it appears in
   `graph.seats_on_record`. W5-DRIVER must pass an explicit `panel=` to
   `audits.run_audits` (WAVE3 §2 already provides for it) rather than letting
   the panel default to the seats on record, or the audit layer will try to
   paraphrase-audit the program.
5. **The guard-block streak counter** — WAVE3 question 1, unchanged.
   `reader.Readings.blocks` is in dispatch order and is what the counter reads;
   the counter, and PREFLIGHT's assertion that it is WAVE3's definition, are
   W5-DRIVER's.
6. **`marker_caller` and `trial_runner` are the dry run's only seams.** W6-DRYRUN
   binds `provider_factory` and leaves both defaults in place; a dry run that
   replaced either with something that does not run the guard would prove
   nothing. The acceptance's *baseline-kind collision forced to `same`* is
   producible from `synthetic.contrast_leg()` by the recipe in
   `tests/loop/test_marker.py::baseline_exhibiting_cell`, and
   `loop/synthetic.py` should grow that shape as an `INDUCIBLE` token so the
   dry run does not have to build it by hand.
7. **A pre-registered condition has no config field** — WAVE3 question 6,
   unchanged.
8. **Whether the loop runs from a wheel** — WAVE3 question 7, unchanged. Note
   that in the integrated clone `seats.key_gate_for` *does* import runner v2 and
   returns a real gate, which is why the wave-4 test fixtures use their own
   `key_env` **names** (`W4_ALPHA_KEY`, …): runner v2's `key_gate` registry is
   process-wide and raises `CONCURRENCY_LIMIT_CONFLICT` if one credential is
   registered at two caps, so a fixture reusing `SYNTHETIC_ALPHA_KEY` at cap 5
   made `tests/loop/test_roles.py` fail depending on discovery order. W5-DRIVER
   should assume the same about any two studies sharing a credential in one
   process.
9. **Where the `rendered_files` record is registered** — WAVE3 question 9,
   unchanged.
10. **`report`'s `plan` argument** — WAVE3 question 10, unchanged.
