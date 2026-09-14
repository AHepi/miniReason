# Wave 5 — the integrated public interface

Read `WAVE0-INTERFACE.md`, `WAVE1-INTERFACE.md`, `WAVE2-INTERFACE.md`,
`WAVE3-INTERFACE.md` and `WAVE4-INTERFACE.md` first; where they differ, the
later one governs. This is the wave-5 integrator's record of what the driver
exposes after reconciliation with the **real** wave-0…4 modules and with runner
v2, the disposition of every acceptance clause, what was kept from the Kimi K3
draft and what was rewritten with the reason, the six CLONE-PATCH dispositions,
the answers this wave owes WAVE3 and WAVE4, and the questions W6-DRYRUN must
answer.

Clone: `scratchpad/loop-impl/repo`, branch cut at `9045a94`; the loop tree is
untracked there and **nothing was committed**.
Sources: `tools/auto_loop.py` (new), `docs/workflows/automated-loop.md` (new),
with edits in `src/minireason/loop/types.py` (eight folded codes,
`AuditConfig.period_account`) and `src/minireason/loop/roles.py` (one corrected
docstring, WAVE4 §8 item 2). Tests: `tests/loop/test_auto_loop.py` and
`tests/loop/test_docs_pins.py` (both new), with edits in
`tests/loop/test_types.py` (the scan now walks the driver).

Drafts: `loop-impl/wave5-drafts/driver/` (labelled COMPLETE, 18 tests green in
its sandbox against **injected fakes**) and `loop-impl/wave6-drafts/doc/`
(25 tests green in its sandbox, written before the driver existed). Both were
drafted against the **declared** wave-3/4 interfaces (owner ruling 16).

**Test lines, exactly as run.** Every run is
`PYTHONPATH=$PWD/src python3 -m unittest …` from the clone root; the
`PYTHONPATH` is load-bearing, because an editable install of `minireason`
points at the live checkout and wins otherwise.

| what | before | after |
|---|---|---|
| `tests.loop.test_auto_loop` as delivered | `Ran 18 tests in 8.798s` `FAILED (errors=1)` | `Ran 46 tests in 124.117s` `OK` |
| `tests.loop.test_docs_pins` as delivered | (not runnable: it reads `design/design-s6-claim-ceiling.md`, absent from this tree) | `Ran 26 tests in 0.017s` `OK` |
| loop suite, quiesced tree (`discover -s tests/loop -t .`) | `Ran 1557 tests in 46.084s` `FAILED (errors=1, skipped=1)` † | `Ran 1611 tests in 162.593s` `OK (skipped=1)` |
| whole repository (`discover -s tests`) | `Ran 2782 tests in 201.987s` `OK (skipped=2)` ‡ | `Ran 2854 tests in 326.972s` `OK (skipped=2)` |

† Measured on the tree with the **draft** copied in at the design's two paths
and before any edit: 1557 = 1539 (WAVE4's after-line) + the draft's 18. The one
error is the reconciliation debt in one sentence: the only test in the draft
that did **not** inject a fake runner reached the real `send_round` and raised
`TypeError: send_round() got an unexpected keyword argument 'records_root'`.

‡ The repository before-line is `WAVE4-INTERFACE.md`'s recorded after-line, not
one this pass re-measured. The arithmetic checks exactly, twice:
1611 − 1539 = 72 = 46 + 26, the two new files' own totals, and
2854 − 2782 = 72 as well. Both after-lines were measured on the quiesced tree,
after the last edit, in one sequence, and `loop-prereg/validate.py` was re-run
in the same sequence and printed **ALL CHECKS PASSED**.

No provider call was made, no credential was read or printed, and nothing
outside the clone was written. The suite opens **no socket**: `socket.socket`,
`socket.create_connection` and `provider_openai_compat._open` are replaced with
refusals around every driver call, and a counter on the provider module's own
two classes asserts that zero `OpenAICompatProvider` objects were constructed
and more than zero `OfflineProvider` objects were.

---

## 0. The map after wave 5

```
                       tools/auto_loop.py  (W5-DRIVER)
                                 │
   ┌────────────┬──────────┬─────┴─────┬───────────┬──────────┬──────────┐
 steps       publish     graph      reader      marker     decide     report
 receipts    custody   markprep     trial       audits     seats      roles
 standard   contracts  surface    synthetic    obligations    types
                                 │
              tools/multicycle_commitment_study_multi_v2  (runner v2, imported)
              minireason.graph_import_h005  minireason.use_relation_h005
```

`tools/auto_loop.py` imports **every** module of the loop package except
`packs` (W4-MARKER and W3-TRIAL own the packs) and `obligations`' internals; it
imports runner v2 lazily through `seats.runner_module()` — one process, one
gate registry — and the importer and use-table builder lazily inside their own
steps, because importing them at module scope inserts repository paths into
`sys.path`.

**Nothing in the package imports the driver.** The driver is the only thing in
the loop that holds state across steps and across cycles; every act it performs
belongs to a module that owns it, and it retypes no code, sentence or
spelling that another module owns.

---

## 1. `tools/auto_loop.py` — W5-DRIVER

### Entry points

```
main(argv=None, *, modules=None) -> int
preregister(config, *, modules=None, budget_override=None) -> Mapping
preflight(config, *, modules=None) -> Mapping
run(config, *, modules=None, budget_override=None, acknowledge=None, reason=None) -> Mapping
adjudicate(run_ref=None, *, modules=None) -> Situation
close(run_ref=None, *, modules=None) -> Mapping
status(run_ref=None, *, modules=None) -> Mapping
reopen(run_ref, ruling=None, *, modules=None, reason=None) -> Mapping
appeal(run_ref=None, path=None, *, modules=None) -> Mapping
dry_run(config=None, out=None, *, modules=None, seed=…, induce=()) -> Mapping
```

Beside them, the facts the driver owns and publishes for other waves:
`cell_key_for(row_key)`, `row_identity(row_key)`, `block_streak(blocks, outcomes)`,
`planned_calls(config, mark_cells)`, `effective_budget(config, override)`,
`seal_baselines(driver, cells)`, `runner_v2()`, and the constants
`ARM_ENDED_TEXT`, `BLOCK_STREAK_DEFINITION`, `MODULE_PIN_KEYS`,
`LOOP_SOURCE_PINS`, `MAX_WAVES_PER_CYCLE`, `LEG_READING`, `LEG_MARK`,
`STATE_RESPONSIBILITIES`, `NEW_CODES`.

### The S0–S15 states, and the function that runs each

| state | step kind | function | what it does |
|---|---|---|---|
| S0 | `PREREGISTER` | `preregister` | freeze the config; stage `obligations.json`, `CEILING.md` and `calibration.json` under the run root; mint `loop_plan_id`; open the pre-registration receipt; register the standard and κ; **seal every contrast baseline (G8)**; open every reading cell, every register cell and every juxtaposition cell; write `plan.json` |
| S1 | `PREFLIGHT` | `preflight` | offline, zero calls: re-verify every path pin and every named module pin; build the seat plan off the **pinned** `endpoints.json` and require cross-family judges; self-test every reading key's coordinate for admissibility and injectivity; self-test the guard-block streak against its declared definition; compare the opened register cells with the set `markprep.program_marks` will produce; refuse a missing `calibration.json`; refuse a planned-call figure past `max_calls` |
| S2 | `PUBLISH_PLAN` | `run/_publish_plan` | `publish()` the run's plan files; the `VERIFIED` line goes into the receipt, a write-once sidecar and the ledger |
| S3 | `CYCLE_OPEN` | `run/_cycle_open` | **the custody check** (`custody.verify_pins` against the plan's tree pins, recorded through `record_custody`), the budget check, the appellate rulings already ingested, the cycle receipt |
| S4 | `PREPARE` | `run/_prepare` | runner v2 `prepare_wave(repo, occurrence, problem, cycle)` in-process, per occurrence and problem; a cycle outside the occurrence's frozen scope is recorded `SCOPE_EXCLUDED` and dispatches nothing |
| S5 | `PUBLISH_IN` | `run/_publish_in` | `publish()` the occurrence trees runner v2 just wrote requests and traces into — before any socket |
| S6 | `SEND` | `run/_send` | refuse unless `publish.check_published` says the plan's bytes are on the ref; runner v2 `send_round(repo, occurrences, provider_factory=…)` in-process; then read runner v2's own `arm_stopped` and file `arm_ended{occurrence, arm, cycle, node, failure_code, text}` |
| S7 | `PUBLISH_EV` | `run/_publish_ev` | `publish()` the wave's records |
| — | — | `run/_dispatch` | S4…S7 **repeat** until `ready_coordinates` is empty for the cycle; the wave label is read off the occurrence's own wave files, so a resumed cycle re-enters at the wave the tree is at |
| S8 | `IMPORT` | `run/_import` | `graph_import_h005.import_occurrence(occurrence, <cycle>/import/<name>)`, then `custody.verify_pins` again; the receipt digests the **importer's own `report.json`**, so a replay reproduces it |
| S9 | `USE_TABLE` | `run/_use_table` | `use_relation_h005.build_use_table` + `write_use_table`; the rows are read back out of `use_table.json`, which is the shape `surface.build_surface` takes |
| S10 | `READ` | `run/_read` | build the `ReadingRow`s, file both indeterminate lists, run `reader.read_table` with the real guard, file the five registers and the streak |
| S11 | `MARK` | `run/_mark` | `marker.mark_cell` per contrast cell against the baseline sealed at S0 |
| — | `AUDIT` | `run/_audit` | the §2.5 audits when `cycle % audit.period == 0`, as their **own spending step** |
| S12 | `ADJUDICATE` | `adjudicate` | render `READING_TABLE.md` and `COMPARISON.md` through W3-REPORT, register the `rendered_files` record, read `decide.situation` over `graph.produced(since_seq=…)` |
| S13 | `DECIDE` | `run/_decide` | `decide.decide` — exactly one outcome — and the write-once `decision.json` |
| S14 | `PUBLISH_CY` | `run/_publish_cycle` | `report.render_cycle` into `CYCLE.md`, then `publish()` the cycle |
| S15 | `CLOSE` | `close` | `report.render_closing` over a real `ClosingRun`, the ceiling verbatim, the ended arms named with `ARM_ENDED_TEXT`, then published |

**The activity log (design 4.5).** Every **publication** and the **dispatch**
are bracketed with `receipts.bracket`, which *shells* `tools/repo_activity.py`
and never reimplements it; `receipts.DEFAULT_AGENT` is already `auto_loop`,
which is this caller. Design 4.5's list is "every search, read, modification,
test and dispatch", and those are the two acts this driver performs on the
repository: every other step writes inside the run's own tree and its own
write-once receipt is the record of it, so a second record of one act in another
log would be two statements of one fact. No command text is ever forwarded — the
wrapper has no command channel at all — and each record is addressed to the
run's own pre-registration receipt, minted at S0 and carried in `_run.json`. A
tree carrying no decision ledger mints no receipt and brackets nothing;
`plan.json["activity"]` says which of the two this run is, so the absence is a
stated fact rather than a silence.

### The one injection seam

`Modules(provider_factory=None, repo_root=None, sleep=None)` — three fields and
exactly one of them is a seam onto behaviour.

* **`provider_factory`** is W6-DRYRUN's own seam and the only provider seam in
  the loop. It is handed unchanged to W2-ROLES (through W3-TRIAL, W4-READER and
  W4-MARKER) **and** to runner v2's `send_wave`, because
  `synthetic.ScriptedProviders` answers both call shapes. Binding it replaces
  the transport and nothing else: every guard, pack, write-once record and
  custody check runs exactly as it does live. `trial_runner`, `registered_by`,
  `marker_caller` and `judge_caller` are left at their defaults everywhere,
  which is what WAVE4 §8 item 6 asks.
* **`repo_root`** is the tree paths resolve against (wave-0 open question O3),
  not a behaviour.
* **`sleep`** is the publisher's backoff clock; it changes how long a rejected
  push waits and nothing about whether it succeeded.

### Codes

`NEW_CODES` carries **eight**, all folded into `types.FAILURE_CODES` (now
**218** members) and into none of the other tables.

| code | raised where |
|---|---|
| `RUN_NOT_FOUND` | `status`/`adjudicate`/`appeal`/`reopen`/`close`/`run`/`preflight` cannot find a written plan, or no repository root is discoverable, or a closing record is asked for with no DECIDE step |
| `APPEAL_PATH_INVALID` | `appeal()` was given no ruling path, or one that is not a readable document |
| `APPEAL_TARGET_INVALID` | the staged ruling is not a mapping, or names no target |
| `READING_ROW_UNRESOLVED` | a pre-registered `h005-row/` key names no row of the use table this cycle built |
| `READING_KEY_INADMISSIBLE` | a reading key folds to a coordinate W2-ROLES refuses, or two keys fold to one |
| `BLOCK_STREAK_DEFINITION_MISMATCH` | PREFLIGHT's self-test of `block_streak` did not reproduce `BLOCK_STREAK_DEFINITION` |
| `REGISTER_CELLS_DISAGREE` | the register cells opened at S0 are not the set `markprep.program_marks` will produce |
| `CALIBRATION_NOT_FOUND` | an audit schedule is declared and the run root carries no `calibration.json` |

Every other code it raises is imported: `BUDGET_RAISED`, `CONFIG_*`,
`PLAN_ID_MISMATCH`, `SOURCE_PIN_MISMATCH`, `CUSTODY_MISMATCH`,
`INPUT_NOT_PUBLISHED`, `REOPEN_REFUSED`, `STEP_NOT_HALTED`, `STEP_BODY_FAILED`
and `types.OUTCOME_CODES`' `APPELLATE_RULING_APPLIED`.

**How the fold test treats a file outside the package.** `tests/loop/test_types.py`
scans `PACKAGE.rglob("*.py")`, and `tools/auto_loop.py` is outside it by the
wave plan's own path. Leaving it there would have let eight codes into
`FAILURE_CODES` unreached and unchecked, so `collect()` now walks
`DRIVER_SOURCE` **beside** the package — the one file outside it this scan
reads, named rather than globbed so a second tool cannot join it silently —
`FOLDED_IN` gains the stem `auto_loop`, `TOKEN_ARGUMENT` gains three entries
(`auto_loop._fail`, `auto_loop.CustodyMismatch`, `auto_loop.refuse`), and the
eight codes are **reached**, not allow-listed. `tests/loop/test_auto_loop.py`
runs the same scan over the driver independently and asserts each declared code
is raised there and is in exactly one table.

---

## 2. The reading-set key is not a coordinate — the finding that forced a design decision

`roles.Coordinate` admits `[A-Za-z0-9][A-Za-z0-9._#-]*` per `/` segment. The
pre-registered reading set of `loop-prereg/config.json` spells its H005 rows

```
h005-row/daily/mini_fcl/cycle01/objection#o1/target/p.objection.0#c1->daily/mini_fcl/cycle01/account#c1
```

and `->` is not in that alphabet. `reader.read_table` passes `row.key` to
`trial.run_trial(key=…)`, which passes `cell.token` to `roles.call_critic`, so
read raw **every one of the twenty-two H005 rows of the frozen reading set
would have raised `ROLE_COORDINATE_INVALID` on its first critic call** —
after S0, after publication, at the first spend of the live run.

`cell_key_for(row_key)` folds each `/` segment to the coordinate alphabet and
appends a twelve-character digest of the exact key, so the fold is a pure,
injective function of the plan's own spelling; the correspondence is written
into `plan.json` under `reading_cells`; PREFLIGHT asserts admissibility and
injectivity over the whole declared set before anything is published; and the
plan's own spelling stays the `row_key` on every record the reader writes, so
each record reads both ways. `row_identity(row_key)` is the matching parse:
`h005-row/<referring_coordinate_key>#<record_id>/<ref_field>/<ref_verbatim>` →
the four-field identity `use_relation_h005` gives each row, which is how a
declared key finds its row in the use table.

---

## 3. The guard-block streak (WAVE3 §8 item 1; CLONE-PATCH item 5)

`BLOCK_STREAK_DEFINITION` is the string WAVE3 settled and
`config.audit.streak_max_account` states:

> consecutive guard blocks per role, over that role's trials in dispatch order
> within the reading arm, reset by any trial of that role whose outcome is not
> a block

`block_streak(blocks, outcomes)` consumes `reader.Readings.blocks` — the block
records in dispatch order, which is exactly what WAVE4 §5 says the counter
reads — and `(row_key, outcome)` pairs in the same order. The **role** is read
off the block's own `prompt_ref_path` / `raw_ref_path`, whose tail is W2-ROLES'
claim layout `<key>/<role>[-<seat>]/provider/call-NNNN.<part>.json`; a block
that dispatched nothing (`blocked:constitution`) names no ref, belongs to no
role, and neither extends nor resets a streak. PREFLIGHT runs `_streak_self_test`
over a fixed four-row probe and refuses `BLOCK_STREAK_DEFINITION_MISMATCH` if
the counter answers anything but the definition; the definition is also written
into `plan.json` and `preflight.json`, so the account beside the number is
checkable against the program that produces it.

The **outcomes matter as much as the blocks**: a counter handed only the block
register can count upward and never reset, which is not the definition. `READ`
therefore hands `block_streak` this pass's `(row_key, outcome)` pairs in the
order the rows were dispatched, so a trial that did not block resets the roles
that answered it; the number is filed on the `READ` receipt as `block_streak`,
carried per cycle on the driver, and `decide.Instrument.block_streak` is the
largest of them. `instrument_fault` therefore fires on the definition the
account states and on no other. It is a bound on the instrument and never on a
reading's standing: crossing it stops the reading arm and adjudicates no cell.

---

## 4. Disposition of every acceptance clause

| clause | disposition | test |
|---|---|---|
| one command walks S0 to S15 offline with zero sockets | **Held, over the real modules.** The walk is `preregister` → `preflight` → `run` inside a socket guard; two cycles, every publication verified against a real bare repository. Zero sockets is asserted by a **provider-module counter**: zero `OpenAICompatProvider` constructions, zero `_open` entries, and a positive `OfflineProvider` count so "nothing ran" cannot pass as "nothing networked". | `OneCommandWalksSZeroToSFifteenOffline` (5 tests, incl. `test_the_walk_reaches_s15_and_the_provider_module_opened_nothing`, `test_every_state_s2_to_s15_filed_exactly_one_receipt_in_order`, `test_the_closing_record_carries_every_required_ceiling_sentence`) |
| publication precedes every dispatch, and a `PublishPending` blocks the next dispatch | **Held, with a real rejected push.** A second clone advances the ref, so the driver's non-forcing push is refused and `publish()` returns `PENDING`; nothing is stubbed and no publisher is injected. The ledger then carries exactly one receipt and every successor step raises `PublishBlocked`. | `PublicationPrecedesEveryDispatch` (2 tests: `test_every_send_is_preceded_by_a_verified_publication`, `test_a_publish_pending_blocks_the_next_dispatch`) |
| runner v2 is imported and `send_round` is called in-process, never shelled | **Held.** `send_round` is wrapped with a call-through spy and `subprocess.run`/`Popen`/`check_output` are all watched: every subprocess that ran is `git`, through `publish()`, and none of them is an interpreter. | `RunnerV2IsImportedAndSendRoundIsCalledInProcess` (2 tests) |
| a second driver on the same run is refused | **Held.** `steps.RunLock` on `run.lock`; a held lock makes `run()` raise `RUN_LOCKED`, and the lock is released when the run ends. | `ASecondDriverOnTheSameRunIsRefused` (2 tests) |
| `--cycles` may only lower the budget | **Held, and made load-bearing.** Upward is `BUDGET_RAISED` before anything is written; a lowered budget is written into `overrides.json` and into `plan.json`, **and is the budget `decide()` reads**, so clause 5 fires at the cycle the override declares rather than at the config's. | `CyclesMayOnlyLowerTheBudget` (4 tests, incl. `test_a_lowered_budget_is_the_budget_the_run_honours`) |
| a killed run resumes without re-sending any coordinate that already has a request or attempt | **Held, at both grains.** A `SEND` killed mid-step leaves its `.open` marker; the resume raises `UnresolvedStep` and the body is **never re-entered** (asserted off a spy on `send_round`); after `--acknowledge <key> --reason "…"` the run completes and no coordinate is left asked-and-unanswered. At the reading grain, a hand-made claim with no call record is what `reader.unanswered_coordinates` reports and what `steps.scan_coordinates` cannot see. | `ResumeNeverResendsAnAskedCoordinate` (2 tests) |
| a custody mismatch halts before dispatch with an erratum and a non-zero exit and is sticky until acknowledged | **Held, inside a step.** The check is `CYCLE_OPEN`'s, the cycle's first step and before `PREPARE`/`SEND`: a moved pin makes the receipt `HALTED` with `SOURCE_PIN_MISMATCH`, W1-STEPS writes the erratum stub under `<run>/errata/`, `main` exits 1, no dispatch step exists, and **restoring the bytes is not enough** — the next run is still refused as sticky until an acknowledgement with a reason is recorded. | `ACustodyMismatchHaltsBeforeDispatch` (1 test, nine assertions) |
| a provider failure ends one arm, mints no warrant, and leaves the other arms running | **Held, from runner v2's own record.** `synthetic`'s `provider_arm_failure` empties the script for one coordinate, `OfflineProvider` raises its own `TRANSPORT_OR_RESPONSE_ERROR`, runner v2 writes the FAILED receipt, and `arm_stopped` is what the driver reads. The other arm reaches its terminal node in the same cycle, the closing record prints `ARM_ENDED_TEXT`, no reading names the ended arm, and `Instrument.arms_ended` stays **false** while one arm still runs. | `AProviderFailureEndsOneArm` (3 tests) |
| an appeal applied at the next invocation flips a label through pass 1 | **Held.** `appeal()` stages the ruling write-once under `<run>/appeals/`; staging alone moves nothing (asserted on a cold re-open of the graph); the next `run()` ingests it at S3 before any receipt of the invocation, and the bearing and the reading both read `REFUTED` while the cell reads `unresolved`. | `AnAppealAppliedAtTheNextInvocationFlipsALabel` (2 tests) |

Beside the nine clauses, four classes hold what the wave-5 integration added:
`PreflightSelfTestsWhatTheRunLeansOn` (7), `TheRegisterCellsAreOpenedBeforeAnyCall`
(3), `TheDriverKeepsItsOwnRules` (10, including the metric-creep lens and the
fold-in contract) and `TheStatusAndReopenEntries` (2). Forty-six in all; the
first clause's class carries six because the activity log is bracketed there
too.

---

## 5. Kept versus rewritten, with the reason

**Kept.** The module's shape and most of its prose: the `Modules` injection
table as a *named* seam rather than an ambient import; `STATE_RESPONSIBILITIES`
as a published table of state → function; `NEW_CODES` as a mapping of code to
one line of reason; `ARM_ENDED_TEXT` as this module's own fixed sentence;
the `_Driver` object holding one invocation's config, paths, plan id, ledger
and lock; the step wiring through `StepLedger.run_step` / `publish_step` with
every git operation inside `publish()`; the `argparse` CLI and its nine
subcommands; `effective_budget`'s downward-only rule; the resume story told
entirely by W1-STEPS; the appeal staging and the ruling-salted step inputs; and
four of the draft's own deviations (the injectable repo root, S0/S1 as public
functions, `SOURCE_PIN_MISMATCH` rather than `PLAN_ID_MISMATCH` for a moved
pin, and `dry_run` as a gate entry rather than a battery).

**Rewritten — 1. every declared interface was the wrong one.** The draft's
`MODULE_SOURCES` table named nine callables and **not one of its call sites
matched the real signature**: `send_round(occurrences, records_root=…,
on_arm_ended=…)` against the real `send_round(repo, outputs, *,
provider_factory=…, publication_check=…, notify=…, publish_ref=…)`;
`prepare_wave(occurrence)` against `prepare_wave(repo, output, problem_id,
cycle)`; `ready_coordinates(occurrences)` against six arguments;
`import_occurrence(occurrence)` against `(occurrence_dir, out_root, …)`;
`build_use_table(import_dir)` against `(occurrence, …)` plus a separate
`write_use_table`; `read_table(harness, table, standard, None, config_dict,
records)` with `seats=None` and a mapping where a `LoopConfig` goes;
`mark_cell(harness, cell, None, standard, None, config_dict)` with no
`records_dir` and no baseline; `run_audits(harness, None, None, config_dict)`
with no judge caller, no readings and no panel; `render_cycle(decision, {})`
and `render_closing({…})` where `CycleState` and `ClosingRun` are required
records. The draft's own suite could not see any of it, because every one of
those calls went to a fake the draft had written to match its own declaration —
and the single test that did not inject a fake is the single test that failed.

**Rewritten — 2. the dispatch chain was one wave, and the design says
"repeat".** The draft ran `PREPARE → PUBLISH_IN → SEND → PUBLISH_EV` once per
cycle. Design §4.1 says S4…S7 repeat until `ready_coordinates` is empty, and
runner v2 prepares at most `wave_capacity` coordinates per wave, so a
three-node template would have left two thirds of its coordinates undispatched
with the cycle recorded as complete. `_dispatch` now loops, with the wave label
read off the occurrence's own wave files so a resumed cycle re-enters at the
wave the tree is at rather than at a counter this process kept.

**Rewritten — 3. the audit rode inside a replayable step.** The draft called
`run_audits` inside `ADJUDICATE`. `ADJUDICATE` is in `types.REPLAYABLE_STEPS`
and is re-entered on every resume, while the audit **spends judge calls**:
probed on the integrated tree, the second invocation of `run()` raised
`NO_REPLAY` at `judge#1@audit-cal/self-juxtaposition`, W2-ROLES refusing to
re-enter a spent coordinate. `types.STEP_KINDS` already carries `AUDIT` as a
spending kind for exactly this reason, and the audit is now its own step.

**Rewritten — 4. `_value_tag` digested a projection of an object.** The draft
filed a "one-line projection" of `Readings`/`Situation` into the receipt —
`{name: str(getattr(value, name))}` over `__dataclass_fields__` — and called it
stable bytes. It is not: it digests the `repr` of every field, including paths
that carry a temporary directory. Every receipt now files **named records** the
step body builds (row keys, codes, digests, the importer's own `report.json`
sha), so a replay reproduces bytes rather than reprs.

**Rewritten — 5. the plan identity and the tree were one check.** The draft
re-derived the pins from the tree inside `_load_config_frozen`, so a moved
pinned file changed the minted id and surfaced as `PLAN_ID_MISMATCH` **before
any step**, which is neither the code design §4.4 names nor a halt anything can
acknowledge. `_frozen_plan_id` now mints over the plan's **frozen** pins — so
the identity answers "did the config change?" — and the tree is checked by
`custody.verify_pins` inside `CYCLE_OPEN`, where a finding halts the step,
writes the erratum and stays sticky. The draft's own test asserted that the
pre-dispatch path wrote **no** erratum; the acceptance clause requires one.

**Rewritten — 6. `Instrument` was half-filled.** `block_streak` was never
computed (WAVE3 §8 item 1 assigns it here), `arms_ended` was read off a
driver-kept list rather than runner v2's `arm_stopped`, and the declared arm set
was the *occurrence* names rather than the arms. `all_arms_ended` is now true
only when every `(occurrence, arm)` runner v2 declares has ended.

**Rewritten — 7. the readings were re-read every cycle.** The reading tree is
the **run's**, not the cycle's (design §4.2), so a row a previous cycle spent is
a spent coordinate: the draft's cycle 2 raised `NO_REPLAY` on the first critic
call. A later cycle now reads what is left, and a spent row is re-read only when
a reopen reason this plan declared is in force — which is G11's rule and
W2-ROLES' `NO_REPLAY` agreeing rather than colliding.

**Rewritten — 8. `_load_driver_from_run` was unreachable code.** The draft's
version contained `drv.paths = run_paths(...) if False else drv.paths`, rebuilt
a `RunPaths` by calling `type(drv.paths)(...)` with three of its fields, and
rebuilt `Modules` by splatting `MODULE_SOURCES`' keys. It is now nine lines that
load the config beside the run root and open the ledger.

**Rewritten — 9. `dry_run` built an occurrence nothing could dispatch.** It
called `synthetic.build_occurrence` with no `freeze`, so the plan was
`synthetic`'s own rather than runner v2's, and it bound no provider. It now
freezes through runner v2 when a repository root is given and binds
`synthetic.provider_factory` when the caller bound none.

**Rewritten — 10. the CLI's `status`/`adjudicate`/`appeal`/`reopen`/`close`
took `--config` and passed it as a run root**, and `--publish-ref`, `--mode`
and `--reason` were parsed and dropped. The five after-the-fact entries take
`--run`; `--mode` and `--publish-ref` are both inside `loop_plan_id`, so a mode
that disagrees with the frozen one is refused rather than applied and a ref is
accepted only where the config declares none.

### Declined, with the reason

* **A second sealed baseline for E and G** (WAVE4 §8 item 1, wave-1 decision
  53). Unchanged: the program's baseline can carry kinds only for T and D, so
  G9 bites only there. Sealing a second artifact is 24 further calls per cell
  and `reading_set.json:max_calls_derivation` does not carry them. It is a
  pre-registration change and it is the bundle's to make; the driver seals the
  one baseline `markprep` builds and records its `undecided_kinds` for E and G
  untouched.
* **Forcing `OfflineProvider` from `--mode offline`.** `provider_mode` is
  inside `loop_plan_id` and `roles.default_provider_factory` is the live
  transport; a flag that swapped the transport would make the record's declared
  mode and its actual one two different things. `--mode` is checked against the
  frozen value and refused on disagreement; binding the seam is `dry-run`'s.
* **A third concurrency gate.** Design §4.6: the loop adds none. `roles` and
  runner v2 both acquire through `provider_openai_compat.slots_for` and runner
  v2's `key_gate`, imported and never copied; the driver's only contribution is
  `run.lock` and the in-process `send_round`.
* **The cadence receipt** (design 4.5: "a `PROGRESS` receipt at any step
  boundary past 240 s"). `receipts.Cadence` / `checkpoint_receipt` are built and
  nothing calls them. The driver does not, because a cadence receipt is an
  append to the repository's ledger on a wall clock, and every clock this wave
  could test it against is a fixture's. It is the first live run's, and §9
  item 11 says so.
* **Computing an audit window's planned calls at PREFLIGHT.** The window's cost
  depends on the readings already on record, which do not exist before cycle 1.
  PREFLIGHT reports the two legs it can derive with their arithmetic and names
  the remainder of `max_calls` as the window's declared allowance; §8 item 4
  routes the arithmetic to the bundle, which already carries it.

---

## 6. The metric-creep lens (ruling 7)

Run over `tools/auto_loop.py` by AST and by reading every record it writes.

* **No `majority`, `average`, `mean`, `percent`, `ratio`, `score`, `rank`,
  `ranking`, `weighted`, `aggregate`, `vote`, `tally` or `exhaustion`** appears
  as a word anywhere in the module — asserted by word-boundary regex, one
  subtest each, because `operation` contains `ratio` and a substring test reads
  as a finding it is not.
* **No division is arithmetic.** Every `/` in the module joins a path; a test
  walks every `BinOp(Div)` node, refuses a numeric operand on either side, and
  requires the expression to name a path. The one place a share could have
  entered — the calibration error rate — is `audits`', is never recomputed
  here, and is never rendered.
* **The integers the module carries are spend boundaries.** `planned_calls`
  returns `row_cost`, `mark_cost` and their sum with the arithmetic beside them,
  and PREFLIGHT compares the sum with `max_calls` and nothing else. `block_streak`
  returns a count of consecutive blocks, which is the instrument's own register
  and a bound on the instrument, never on a reading's standing: crossing it
  names `instrument_fault`, which stops the reading arm and adjudicates no cell.
  Neither number is compared between seats, between arms or between cycles.
* **Every stop is a member of `types.STOP_REASONS`.** The driver names none of
  them itself: `decide` returns the `Decision` and the driver records it.
  `standard.assert_no_exhaustion_claim` runs over `preregistration.md`,
  `decision.json`, every `CYCLE.md` and `CLOSING.md` before they are written.
* **The activity log carries no quantity and no command.** The bracket records
  a phase, an action naming the step kind, a why, a goal and the run root; the
  logger refuses a field carrying a registered credential and has no command
  channel at all.
* **Nothing the driver renders is its own.** `READING_TABLE.md`,
  `COMPARISON.md`, `CYCLE.md` and `CLOSING.md` all come out of W3-REPORT, which
  runs `contracts.assert_no_scoring_keys` and `standard.assert_no_scoring_headers`
  over its own output before returning; the driver registers the
  `rendered_files` record W3-REPORT builds and asserts the scan again before it
  enters the graph.

---

## 7. The six CLONE-PATCH dispositions

| item | disposition |
|---|---|
| **1 — something must read `calibration.json`** (REQUIRED) | **Applied.** S0 stages `calibration.json` into the run root beside the config, digests it, and writes `plan.json["calibration_sha256"]`. Every `AuditReport` body the driver registers carries `calibration_sha256`, `covers: [cycle]` and `seats: list(config.seats.judges)`, which is what `obligations.audit_in_force` reads. PREFLIGHT refuses `CALIBRATION_NOT_FOUND` when a schedule is declared and the file is absent, so o5 cannot be silently unsatisfiable. |
| **2 — `plan.json` must pin `audits.CALIBRATION_EXCHANGES_SHA256`** (REQUIRED) | **Applied**, with three more: `MODULE_PIN_KEYS` pins the exchanges digest, `standard.STANDARD_BODY_SHA256`, `standard.CEILING_SHA256` and `decide.DECIDE_SHA256` as **named** pins (constants, not paths), plus the ceiling under its own `standard.CEILING_PIN_KEY` — which W3-REPORT refuses to render without. `custody.verify_pins` is given only the path-shaped subset that exists in the tree, so it is never asked to find a file named after a constant. |
| **3 — `types.AuditConfig` has no `period_account`** (declared gap) | **Applied as an OPTIONAL key, and here is why not as the diff writes it.** CLONE-PATCH's own diff puts `period_account` in `_REQUIRED`; the L001 `config.json` does not declare it, so a required field makes `LoopConfig.load(loop-prereg/config.json)` raise `CONFIG_MISSING_KEY` at `validate.py`'s **first** check — and the same document requires that `validate.py` still print ALL CHECKS PASSED. The field is therefore accepted, validated as non-empty prose when present, and **omitted from `as_dict()` when empty**, so a config that does not declare it mints the identity it minted before the field existed. The clone now carries the field `PREREG.md` §3 says it lacks; L001's account stays pinned by `reading_set.json` and PREREG's stated difference stays true. |
| **4 — `types.LoopConfig` cannot carry the resource conditions** (declared gap) | **Neither of the two named options; the bundle's own preference kept, and the intent met another way.** (a) Adding a seventh member to `types.PINNED_SOURCE_PATHS` breaks `validate.py`'s `assert len(pins) == 6 and set(pins) == set(PINNED_SOURCE_PATHS)`, and the path it would name (`src/minireason/loop/roles.py`) is read from `/home/user/miniReason`, where the loop tree is still untracked — a pin that cannot be computed is the one thing a pin must never be. (b) Adding resource-condition keys to `LoopConfig` breaks the closed key set that `PREREG.md` §2a explicitly relies on ("They live here and not in `config.json` because `types.LoopConfig` accepts a closed key set and refuses an unknown one"). So: `PINNED_SOURCE_PATHS` stays six, `LoopConfig`'s key set stays closed, the declaration stays in `reading_set.json` where the bundle put it — **and the driver pins `src/minireason/loop/roles.py` by path in the run-specific half of the pin map**, which `types.loop_plan_id`'s own docstring says "stays the caller's to supply". `ROLE_MAX_TOKENS`, the `min(timeout, 300)` wall and the `thinking` rule are therefore inside `loop_plan_id` **by the bytes that implement them**, which is what item 4 wanted, without moving anything the bundle pins. `decide.py`, `standard.py` and `audits.py` are pinned the same way. |
| **5 — the guard-block streak counter is unimplemented** (declared gap) | **Applied.** §3 above: `block_streak` is WAVE3's definition, `BLOCK_STREAK_DEFINITION` is the string, PREFLIGHT self-tests the counter against it and refuses `BLOCK_STREAK_DEFINITION_MISMATCH`, and the definition is written into `plan.json` and `preflight.json` so the account beside `streak_max` can be checked against the program. |
| **6 — the complete `unread` inventory must be twelve** (declared gap) | **Applied as a mechanism; the count is the occurrence's.** S0 opens three families of cell: one per pre-registered reading row, one per `(cell, register, comparison)` the marker may write into, and **one per juxtaposition of every occurrence of the attached contrast study**, read off each `comparison.json`'s own `tables` array. `reader.Readings.unread` is every open cell nothing read, so for L001 that is C001 occurrence-01's twelve — six endpoint slugs × two arms — whether or not this run marks them, plus occurrence-02's. `plan.json["opened_cells"]["juxtaposition_cells"]` names them, so the inventory is readable before the first call rather than inferred after the last. |

**Did a pin move?** **No.** `standard.STANDARD_BODY_SHA256` is still
`a9007dc73c748cfff974a1a3d77098d380ec153b1b8cf93f513cafa3ea0572d7`,
`standard.CEILING_SHA256` still
`1e26be087483fd1b9c8e2c403cfae646fb07ebc773f23434a0c4dfab3ed04c1e`,
`audits.CALIBRATION_EXCHANGES_SHA256` still
`91c29e1e71719d815c21c2697f4aa68a7c983be21df945ad6b1e5042183981e5`, and
`decide.DECIDE_SHA256` still
`e08d40adcda10e5412b945453fe09bb25030c59e9310d66b43a89cc3ffb18f29`. This wave
edited `types.py` and `roles.py`; no bundle document pins either file's digest,
and `roles.py`'s edit is a docstring, so nothing the bundle publishes changed.
`loop-prereg/validate.py`, re-run with `PYTHONPATH=$PWD/src` after every edit,
prints **ALL CHECKS PASSED**. Nothing in `loop-prereg/` was edited.

---

## 8. What WAVE3 and WAVE4 asked W5, answered

1. **The guard-block streak** (WAVE3 1 / WAVE4 5) — §3. Implemented and
   self-tested at PREFLIGHT.
2. **Who carries `INDETERMINATE`** (WAVE3 2 / WAVE4 2) — the driver, and it
   files **both** lists rather than choosing one. The `READ` receipt carries
   `indeterminate.dispatch_tree` (`steps.scan_coordinates` over runner v2's
   `requests/`-`attempts/`-`responses/` tree) and `indeterminate.roles_layout`
   (`reader.unanswered_coordinates` over W2-ROLES' `<key>/<role>/provider/`
   claims) as two named facts about two trees. **The SEND arm keeps
   `steps.scan_coordinates`** — it is the arm whose tree that function reads —
   and the two layouts are **not** converged: converging them would mean one of
   runner v2 and W2-ROLES writing the other's record shape, and both are
   write-once records of already-published discipline. The `roles._claim`
   docstring has been corrected in this pass to say so (it claimed
   `scan_coordinates` reads its claim as started; it cannot).
3. **Who opens the register cells** (WAVE4 3) — the driver, at S0, and
   PREFLIGHT asserts the opened set equals the set `markprep.program_marks`
   produces, refusing `REGISTER_CELLS_DISAGREE` otherwise. Opening them needs
   the baseline sealed first (`program_marks` refuses on an unsealed cell), so
   S0 also seals every contrast baseline — which is the right order anyway:
   G8 wants the baseline written before anything else for that cell.
4. **The panel of a program-written mark** (WAVE4 4) — the driver always passes
   an explicit `panel=` to `audits.run_audits`, built from the pinned judge
   seats as `roles.Coordinate.seat_label` spells them (`judge#1`, `judge#2`),
   so the audit layer is never handed the `program` seat that G9/G10 marks
   carry.
5. **`marker_caller` and `trial_runner` are the dry run's only seams**
   (WAVE4 6) — the driver leaves both at their defaults and binds
   `provider_factory` alone. `Modules` has exactly three fields and a test
   asserts it.
6. **A pre-registered condition has no config field** (WAVE3 6 / WAVE4 7) —
   **still open.** `decide.Instrument.preregistered_condition` exists and
   nothing sets it, because no config key declares a condition and this wave
   invented none. §9 item 3.
7. **Whether the loop runs from a wheel** (WAVE3 7 / WAVE4 8) — **answered: it
   cannot, while runner v2 publishes its own source.** `required_paths`
   includes `Path(__file__).resolve()` and resolves it *inside the repository
   being dispatched for*, so a runner imported from anywhere but the tree it is
   sending for raises before the first request. The driver therefore imports
   runner v2 through the one canonical name (`seats.runner_module()`), and the
   gate installs the fixture checkout's own copy under that name and restores
   the previous module afterwards. WAVE4 8's other half also holds: two studies
   sharing a credential in one process must agree on its cap, so this wave's
   fixtures use their own `W5_*_KEY` names.
8. **The calibration exemplar bytes** (WAVE3 8) — settled by the bundle, not
   here: the exchanges stay in `audits` and `plan.json` pins their digest
   (CLONE-PATCH item 2, applied).
9. **Where `rendered_files` is registered** (WAVE3 9 / WAVE4 —) — in
   `ADJUDICATE`, after the renderers have run and **before** `decide.situation`
   reads the graph, through `graph.register_material` over
   `report.rendered_files_record`, with `contracts.assert_no_scoring_keys` run
   over it first. p4 therefore evaluates against a present record.
10. **`report`'s `plan` argument** (WAVE3 10) — the driver passes a real
    `report.ReportPlan(loop_plan_id, pins, reading_set, ceiling_text)`, so the
    closing header is never `(plan unpinned)`.

---

## 9. What W6-DRYRUN must answer

1. **`synthetic.canned_responses` scripts no `#order-swapped` coordinate**, and
   its loose fallback slices a judge script by seat index, so the **second**
   judge seat receives an empty script and every swapped ruling reads
   `blocked:provider` with the detail *"offline script exhausted"*. The gate
   answers the swapped presentation from the seat's own script and says so; a
   dry run that wants a *sustained* reading, an order-swap flip or an ensemble
   split at the swapped presentation needs `synthetic` to script
   `coordinate + "#order-swapped"` per seat. **This is a W1-SYNTHETIC change,
   not a driver one**, and the acceptance clause "an order-swap flip blocks"
   cannot be induced from the canned script until it lands.
2. **`synthetic` writes an occurrence runner v2 cannot re-read.**
   `build_occurrence` writes its own `requests/` records, which carry no
   `provider_payload`; runner v2's `read_terminal` reads that field, so
   `arm_stopped` — and therefore `ready_coordinates` and `prepare_wave` — raise
   `KeyError` on a delivery-complete synthetic occurrence. The gate stages the
   occurrence the other way round (material and arms written, the plan frozen by
   `runner.initialize`, **nothing delivered**) and lets S4…S7 produce every
   delivery through the same runner, which is the more faithful walk. W6-DRYRUN
   must either do the same or have `synthetic` write runner-v2-shaped requests.
3. **A pre-registered condition still has no declaration.**
   `Instrument.preregistered_condition` is the driver's to fill and no config
   key names one. Either `LoopConfig` grows a `preregistered_conditions[]` block
   (a new `loop_plan_id`, so it must land before S0) or the clause is recorded
   as unreachable in this plan and the dry run asserts that it is.
4. **The audit window's call budget is the bundle's arithmetic, not the
   program's.** PREFLIGHT derives the reading and mark legs and reports the
   remainder of `max_calls` as the window's allowance. The dry run should assert
   that the window it actually spends is inside that allowance, which is the
   first occasion on which `reading_set.json`'s `46` can be checked.
5. **The baseline-kind collision forced to `same`** (WAVE4 6's other half) is
   still producible only by hand: `synthetic.contrast_leg()` plus the recipe in
   `tests/loop/test_marker.py::baseline_exhibiting_cell`. `loop/synthetic.py`
   should grow it as an `INDUCIBLE` token, or W6-DRYRUN must build it and say
   that it did.
6. **The mark leg of the gate blocks rather than sustains.** The driver drives
   `markprep` + `packs` + `roles` + `marker` for real, but the canned marker
   script's quotes (`"ORIGINAL <case> <register>"`) do not resolve on the
   pairwise surface, so every row ends `unresolved` under
   `blocked:referential-integrity`. That is the guard working; it is **not** a
   demonstration that a mark can be sustained, and the dry run owes that
   demonstration.
7. **Two occurrences sharing one credential in one process.** The gate runs one
   occurrence. `send_round` drives occurrences concurrently under the
   process-wide key gate, and the design's "a reading call and a dispatch call
   in flight together are held to five per credential between them" has not been
   exercised by anything yet.
8. **A step timeout has no test here.** `timeouts.step_seconds` is passed to the
   `StepLedger` and W1-STEPS enforces it; `synthetic` can induce one
   (`step_timeout`), and §4.7's list names it. The gate's config declares no step
   deadline, so the driver's behaviour under `STEP_TIMEOUT` — the marker kept,
   the resume halting — is W1-STEPS-tested and not W5-tested.
9. **The live ledger.** `receipts.open_preregistration` and
   `steps.publish_step`'s `ledger_append` write into
   `docs/DECISION_LEDGER.md`; the gate gives the fixture its own one-line
   ledger. A live run appends to the repository's, under the lock
   `repo_activity.append` uses, and the first live run is the first test of that
   contention.
10. **`--acknowledge` takes a step key, and an operator will not have one to
    hand.** `status` prints the resume plan with each action's index and kind but
    not its `step_key`; the key is in the receipt. Either `status` should print
    it or the erratum should, and W6-DRYRUN is the first thing to need it.
11. **The cadence receipt is unwired.** Design 4.5 asks for a `PROGRESS` receipt
    at any step boundary past 240 s, never backdated. `receipts.Cadence` and
    `receipts.checkpoint_receipt` are built; the driver calls neither, because
    the only clocks this wave can drive are fixtures'. The dry run should decide
    whether it wants the cadence exercised against an injected clock or left to
    the first live run, and say which.
