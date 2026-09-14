# Wave 6 — the acceptance proof, and what the first live run must be told

Read `WAVE0-INTERFACE.md` … `WAVE5-INTERFACE.md` first; where they differ, the
later one governs. This is the wave-6 integrator's record of what
`tests/loop/test_dry_run_end_to_end.py` asserts and how, the disposition of the
Kimi K3 draft's six declared seam dependencies D1–D6, what was kept and what
was rewritten with the reason, the driver and module defects the proof found
and how each was closed, the pointer to the executed dry-run record, every
question still open before a live run, and the exact operator command sequence
for that run.

Clone: `scratchpad/loop-impl/repo`, branch cut at `9045a94`; the loop tree is
untracked there and **nothing was committed**.

Sources touched this wave:
`tests/loop/test_dry_run_end_to_end.py` (new, the acceptance proof),
`tools/auto_loop.py` (seven changes, §3), and
`src/minireason/loop/synthetic.py` (three changes, §3). Nothing else was
edited; nothing in `loop-prereg/` was edited; `loop-prereg/validate.py`,
re-run with `PYTHONPATH=$PWD/src` after the last edit, prints
**ALL CHECKS PASSED**.

No provider call was made, no credential was read, named or printed, and
nothing outside the clone and the session scratchpad was written.

---

## 0. Test lines, exactly as run

Every run is `PYTHONPATH=$PWD/src python3 -m unittest …` from the clone root;
the `PYTHONPATH` is load-bearing, because an editable install of `minireason`
points at the live checkout and wins otherwise.

| what | before | after |
|---|---|---|
| `tests.loop.test_dry_run_end_to_end` as delivered | `Ran 0 tests in 1.286s` `FAILED (errors=12)` | `Ran 51 tests in 11.520s` `OK` |
| loop suite, quiesced tree (`discover -s tests/loop -t .`) | `Ran 1611 tests` `OK (skipped=1)`, plus this module's twelve `setUpClass` errors and no tests † | `Ran 1662 tests in 167.856s` `OK (skipped=1)` |
| whole repository (`discover -s tests`) | `Ran 2854 tests` `OK (skipped=2)`, plus the same twelve † | `Ran 2905 tests in 331.202s` `OK (skipped=2)` |

The delivered module ran **no test at all**: all twelve of its classes raised
in `setUpClass` on `TypeError: Modules.__init__() got an unexpected keyword
argument 'publisher'`. The draft's `Modules` table had eleven slots and the
integrated one has three, so not one assertion in the file was ever reached
against the integrated driver. That single line is the whole reconciliation
problem, and §2 is its disposition.

† **The only before-line measured this pass is the module's own.** The two
suite before-cells are `WAVE5-INTERFACE.md`'s recorded after-lines
(`Ran 1611 tests in 162.593s` `OK (skipped=1)` and `Ran 2854 tests in
326.972s` `OK (skipped=2)`) with the delivered module's twelve `setUpClass`
errors and zero tests added; neither was re-measured before the edits, and the
cells say so rather than borrowing a measured duration for an unmeasured
status. Both after-lines were measured on the quiesced tree, in one sequence,
after the last edit. The arithmetic checks twice: 1662 − 1611 = 51 and
2905 − 2854 = 51, this module's own total.

---

## 1. What the acceptance proof asserts, and how

One walk, built once and read by every class, over **one run directory across
six invocations** — because that is the only honest way to prove a resumable
machine: a halt is recorded by the invocation it stops, and the closing receipt
is minted by a later one.

| inv | what it does | what it proves |
|---|---|---|
| 1 | `dry_run(config, out)` | S0 PREREGISTER, S1 PREFLIGHT, then S2 onward. The SEND body of the first wave outruns the `timeouts.step_seconds["SEND"]` deadline the **frozen config** declares; W1-STEPS records `STEP_TIMEOUT` on a spending step and leaves the open marker standing. |
| 2 | `run()` | the standing marker halts the resume with `UNRESOLVED_STEP`, and `send_round` — watched by a call-through spy — is never re-entered. `status` prints the step key `--acknowledge` takes. |
| 3 | `run --acknowledge <key> --reason …` | cycle 1 completes: one arm ended by a provider failure while the others reach their terminal nodes, the reading arm registers, the mark arm marks. A pinned source then changes under the running loop, and cycle 2's CYCLE_OPEN **halts** — `SOURCE_PIN_MISMATCH`, an erratum stub, exit 1, no dispatch step after it. |
| 4 | `run` with the bytes restored | still exit 1, still `SOURCE_PIN_MISMATCH`, and the message says *sticky*. Restoring the bytes is not enough. |
| 5 | `reopen --reason <not pre-registered>` | exit 1, `REOPEN_REFUSED`, and the refusal is filed on the run's own record. The appellate ruling is staged here against a ν_bearing **the loop itself registered**; a cold re-open of the graph shows staging alone moved nothing. |
| 6 | `run --acknowledge <halt key> --reason …` | the ruling is ingested at S3 before any receipt of the invocation, cycle 2 runs, S15 writes `CLOSING.md`, exit 0. |

### Clause by clause

| acceptance clause | how it is held | named test |
|---|---|---|
| zero provider network calls, asserted by a **provider-module counter** | a counter on `provider_openai_compat`'s own two classes and on `_open`, with `socket.socket`/`create_connection` replaced by refusals around the whole walk: zero live transports, zero opened requests, and a **positive** offline count so "nothing networked" cannot pass as "nothing ran" | `ZeroProviderNetworkCalls` (3) |
| every git operation through `publish()` against a real temp bare repo, so `VERIFIED` is exercised | every completed `PUBLISH_*` step has a `.verified` sidecar matching `VERIFIED <sha> …`; the bare remote's `refs/heads/main` is one of the receipts' `published_commit`; every subprocess spawned is `git` or the shelled `tools/repo_activity.py`, and that one carries no `--command` | `EveryGitOperationRanThroughPublish` (3) |
| a provider failure ended one arm while the others continued | `synthetic`'s `provider_arm_failure` empties one coordinate's script, `OfflineProvider` raises its own `TRANSPORT_OR_RESPONSE_ERROR`, runner v2 files the FAILED receipt and `arm_stopped`; the FCL arm reaches its terminal node in the same cycle, no reading names the prose arm, and `ARM_ENDED_TEXT` is printed | `AProviderFailureEndedOneArm` (3) |
| a custody mismatch halted with an erratum and a non-zero exit and stayed sticky on resume | above, inv 3 and 4 | `ACustodyMismatchHaltedAndStayedSticky` (4) |
| a step timeout | the **real** mechanism: a declared step deadline, a spending SEND body that outruns it, the marker kept (`STEP_TIMEOUT ∈ steps.MARKER_KEPT_CODES`), the resume halted, the acknowledgement on the record | `AStepTimeoutLeftItsMarkerStanding` (5) |
| an ensemble split resolved to unresolved and **not voted** | the block register names `ensemble-split` against its cell; that cell registered no reading; and no word of the vocabulary of voting (`majority`, `vote`, `average`, `mean`, `quorum`) appears in the record | `AnEnsembleSplitResolvedToUnresolved` (3) |
| a paraphrase flip that registered no warrant | `paraphrase-flip` in the register, and the row is absent from the registered readings | `AParaphraseFlipRegisteredNoWarrant` (1) |
| a non-unique offset that registered no warrant | `referential-integrity` in the register, the row absent from the registered readings, and the material half asserted: `synthetic.DUPLICATED_PHRASE` really stands more than once in the delivered arm | `ANonUniqueOffsetRegisteredNoWarrant` (2) |
| a baseline-kind collision the program forced to `same` | the mark row reads `mark: same`, `source: program`, `difference_kind: null`, a non-empty `forced_by`, `evidence.downgraded_from_kind` naming the kind, and `block: blocked:baseline-forced-same` — and the register prints it | `ABaselineKindCollisionWasForcedToSame` (4) |
| a re-read refused for want of a `reopen_reason` | the `reopen` entry exits 1 with `REOPEN_REFUSED`, the refusal is on the run state, and the later cycle re-read no spent row because no reason was in force | `AReReadWasRefusedForWantOfAReopenReason` (4) |
| an appellate ruling that flipped a label through pass 1 | staging alone moves nothing (cold re-open); the next invocation flips ν_bearing and the reading to `REFUTED` and the cell to `unresolved`; **and every other bearing the reading arm registered stands exactly where it stood** | `AnAppellateRulingFlippedALabelThroughPassOne` (4) |
| the closing receipt names each of the nine **by code** | every code is read back as a *membership* fact, not a substring guess: the block register's bare reason spelling is turned back into a code with `types.block_code`, and every other token is matched against `types.FAILURE_CODES` / `types.OUTCOME_CODES`. Each of the nine is checked to be in exactly one of the owner's three tables | `TheClosingReceiptNamesEveryInducedFailureByCode` (3) |
| every sentence of `CEILING_REQUIRED_SENTENCES` verbatim | all eleven, one subtest each, plus `standard.assert_no_exhaustion_claim` | `TheClosingReceiptCarriesTheCeilingVerbatim` (2) |
| the walk is S0 → S15 | the verdict records the staging, S0 and S1; the ledger's kinds run `PUBLISH_PLAN` … `CLOSE`; the run wrote nothing outside the temp tree | `TheDryRunWalksSZeroToSFifteen` (5) |
| the metric-creep lens (ruling 7) | the owner's own scans over the whole record, a word lens over **the two sections this wave's driver writes**, the only counts being the block register's, and the verdict carrying no measure | `TheMetricCreepLens` (5) |

Fifty-one in all.

**Why the word lens is scoped.** A bare word lens over `CLOSING.md` fails on
`ranked`, `weighted`, `rate` and `exhaustion` — every one of them inside the
frozen ceiling's own *denial* of the thing. The scan that governs the rendered
body is its owner's (`assert_no_exhaustion_claim`,
`assert_no_scoring_headers`, `assert_no_scoring_keys`), and all three are run
here; the word lens belongs over the text this wave added, and that is where it
is run.

### The composed seams the task named

* **The sticky halt across a resume of the same run directory** — inv 3 → 4 →
  6, one run root, one `loop_plan_id`, the acknowledgement recorded and read
  back off the ledger.
* **The arm-ended path leaving the other arms' coordinates dispatched** — the
  surviving arm's terminal `response.json` is on disk in the same cycle, and
  `arms_ended` names exactly one arm.
* **The appeal changing a label through pass 1 on the next invocation and
  nothing else** — the before/after bearing map over every registered reading,
  with exactly one entry moved. (The bystander's *reading* also falls, through
  its ν_soundness and the cycle-2 audit — a different instrument, recorded in
  the audit register. The ruling moved one bearing, which is what a ruling may
  do.)

---

## 2. D1–D6, the draft's own declared seam dependencies, disposed

| seam | disposition |
|---|---|
| **D1 — the `Modules` dependency table as a whole; fakes injected through it** | **Deleted.** The integrated `Modules` has three fields and exactly one is a seam onto behaviour. Every fake is gone: the proof runs the real `trial`, `reader`, `marker`, `markprep`, `packs`, `audits`, `decide`, `report`, `graph`, `steps`, `publish`, `receipts` and `custody`, the real importer and use-table builder, and runner v2 in-process from the fixture checkout. |
| **D2 — the declared call shapes of nine callables** | **Deleted with D1.** Not one of the draft's declared signatures matched the real one (WAVE5-INTERFACE §5 rewrite 1 records the nine); the proof now calls only the driver's public entries and reads the modules' own written records. |
| **D3 — the `closing_names` hook, written into the private `_run.json`** | **Deleted, and the gap it papered over is closed in the driver.** The integrated `close()` mints the naming section from the run's **own** step ledger, run state and write-once records (`auto_loop.recorded_failures`), so a resumable run names the failures earlier invocations recorded. The test writes nothing into the run tree. |
| **D4 — `rulings_applied_this_run` re-salting, and ingest-at-cycle-open** | **Kept as a fact, not as a seam.** `_ingest_rulings` really does apply every staged ruling once, before this invocation's first cycle step, and really does salt the replayable steps with the applied ids, so the designed flip is not read as `STEP_NONDETERMINISTIC`. Nothing is staged to make it true; the proof asserts the flip and the `applied_rulings` outcome. |
| **D5 — `dry_run` as a thin gate entry with no body of its own** | **Deleted.** `dry_run` is now the full S0–S15 walk: it stages the synthetic material every occurrence the config names, walks S0 and S1 when the run carries no plan, walks S2–S15, and writes the verdict even when the run refuses. One operator command; §4 records it executed. |
| **D6 — the step timeout hand-staged as a `PREPARE` step with a jumped monotonic clock** | **Deleted.** The deadline is declared in the frozen config and hit **inside the spending SEND body**; W1-STEPS records `STEP_TIMEOUT`, the marker stands, the resume halts, and an acknowledgement with a reason is what gets past it. No clock is patched and no receipt is hand-written. |

### The one condition still built by the fixture, and why

**The baseline-kind collision's material half.** `synthetic.contrast_leg()`
*declares* a colliding case in its `baseline_kinds` block, but
`markprep.baseline_kinds` computes an **empty** set for every register of every
case from the replicates it actually writes — so no canned marker answer can
collide with anything and G9 is unreachable from the canned material. The proof
states that finding as its own test
(`test_the_canned_leg_declares_a_collision_its_own_replicates_do_not_bear`),
then builds the material half by the recipe `tests/loop/test_marker.py` already
carries (two of three ORIGINAL replicates gain a `revises` the first does not)
and supplies **one** seat answer — `differs` at the kind that baseline really
exhibits, quoting two spans computed from the cell's own pairwise surface.
Design §4.7 assigns the contrast material to the fixture, and WAVE5-INTERFACE
§9 item 5 routed the choice here explicitly ("`loop/synthetic.py` should grow
it as an `INDUCIBLE` token, or W6-DRYRUN must build it and say that it did").
**It was built here, and this says so.** The downgrade itself is entirely the
program's: the seat says `differs`, and G9 writes `same`.

---

## 3. What the proof found, and what was changed to close it

Seven changes in `tools/auto_loop.py` and three in
`src/minireason/loop/synthetic.py`. Each is a defect the acceptance proof could
not have been written around.

1. **The closing receipt could name no failure at all.** `preregister` seeded
   `_run.json["closing_names"] = []` and nothing ever wrote or read it;
   `close()` rendered the body and the ended arms and stopped. New:
   `recorded_failures(drv)` reads the run's own step ledger (every `FAILED` or
   `HALTED` receipt and its code), the run state's refusals, and the applied
   rulings' outcomes; `close()` prints them under
   `RECORDED_FAILURES_HEADING` with `RECORDED_FAILURES_SENTENCE`, files them
   on the CLOSE receipt and back into `closing_names`. No line carries a
   number.
2. **The closing block register was one cycle's, not the run's.**
   `ClosingRun`'s own docstring says the register is the run's; `close()`
   passed the *last* cycle's `CycleState.blocks`, so on a resumed run every
   block an earlier invocation wrote was silently absent. New: `_run_blocks`
   reads W4-READER's write-once `block-NN.json` records and W4-MARKER's
   `marks.json` out of the run tree, which survive every invocation.
3. **A heading the register could never fill.** `baseline-forced-same` is a
   `BLOCK_REGISTER_HEADINGS` row that only a **mark** row can fill, and the
   register was fed by the reading arm alone. New: `_mark_blocks` feeds the
   mark leg's blocks into `_cycle_state` and `_run_blocks`, spelled with
   W1-GRAPH's own `<cell>|<register>|<comparison>` key so one thing has one
   name in one record. One cell declined for one reason is one entry however
   many cycles re-met it.
4. **`reopen()` refused and recorded nothing.** A refusal no record carries is
   a refusal no closing receipt can name. It is now filed in the run state's
   `refusals` *before* the `LoopError` is raised — an act of the instrument,
   filed beside the halts and never in the block register.
5. **`dry_run` could not dispatch the occurrence it built** (WAVE5 §9 item 2)
   and did not walk S0 or S1. New: `_stage_dry_run_material` writes
   `material.json` and `arms.json` for every occurrence the config names that
   the tree does not carry and freezes the plan through runner v2's own
   `initialize` with **nothing delivered**, so S4…S7 produce every delivery
   through the runner; an occurrence or a contrast leg already on disk is left
   exactly as it stands. `dry_run` then preregisters and preflights when there
   is no plan, and writes the verdict with the refusal on it when the run
   refuses.
6. **A contrast-leg cell computed an empty baseline for every register.**
   `_mark_cells` called `cell_from_contrast_leg(leg, case)` with no address
   space, so `markprep` read no reference as engaging a criticism. The leg now
   declares its own `addresses` and `objection_ids` and the driver passes them;
   a leg declaring neither behaves exactly as before.
7. **`--acknowledge` takes a step key an operator had no way to read**
   (WAVE5 §9 item 10). `status` now prints each action's `step_key` and, beside
   `blocking`, an `acknowledge` field carrying the key of the blocking action.
8. **`synthetic`'s script could not be addressed by the loop's coordinates.**
   `ScriptedProviders.provider` was handed W2-ROLES' `judge#1@<key>` seat label
   and raised `SYNTHETIC_COORDINATE_UNSCRIPTED`. New `seat_key` accepts that
   spelling and returns `JUDGE_SEATS`' own.
9. **…and could not be addressed by the driver's folded row coordinates.** New
   `ScriptedProviders.address` resolves a caller-declared alias (longest prefix
   first, keeping the derived `#reread` / `#paraphrase-N` / `#order-swapped`
   suffix) and translates a marker's `contrast/<case>/<comparison>/<register>`
   into this module's own `mark/…` key; `provider_factory(..., aliases=)`
   carries the map and `auto_loop._dry_run_aliases` mints it from the config's
   own reading set.
10. **The loose fallback handed the second judge seat an empty script**
    (WAVE5 §9 item 1) — and an empty script is how a *provider failure* is
    expressed, so every derived coordinate read as a delivery failure it never
    had. The fallback is now built for the seat it is asked about and is not
    then sliced by seat index.

**Did a pin move?** **No.** `loop-prereg/validate.py` prints ALL CHECKS
PASSED after the last edit; `standard.STANDARD_BODY_SHA256`,
`standard.CEILING_SHA256`, `audits.CALIBRATION_EXCHANGES_SHA256` and
`decide.DECIDE_SHA256` are unchanged, and no bundle document pins
`synthetic.py` or `tools/auto_loop.py`.

---

## 4. The executed dry run

`loop-impl/DRYRUN-RECORD.md` — the command, its exit code, the same command
under a provider-module counter, the `dry-run.json` verdict, the whole
`CLOSING.md` verbatim, and a metric-creep lens over both.

In one line: `python3 tools/auto_loop.py dry-run --config dry-run-config.json
--dry-run-out <dir>` from a throwaway checkout with a temp bare remote, exit
**0**, three cycles, forty-three step receipts, ten `VERIFIED` publications
whose last commit is the remote's `HEAD`, `stop_reason`
**`no_new_reading_changes`** under `clause_four_set_identity`,
`planned_calls 232` inside the pre-registered `max_calls 396`, and
**zero live transports, zero opened requests, 218 offline providers**. No key
name was present in the environment and none was needed.

---

## 5. Every question still open before a live run

**What the first live run must be told, because the dry run could not exercise
it.**

1. **The 300 s wall is the effective per-call wall on this host** (rulings 13
   and 14: five closes in a 183 ms band across two families and two client
   processes). The frozen config declares `timeouts` per step and
   `endpoints.json` declares `timeout_seconds` per endpoint; neither is that
   wall. Nothing offline can reach it, so the first live run is the first
   occasion on which a request still open at 300 s is seen, and the operator
   must read a `TRANSPORT_OR_RESPONSE_ERROR` at ~300 s as the host's gateway
   closing the arm — **not** as a model refusing, and never as a verdict.
2. **The key gates were never contended.** `provider_openai_compat.slots_for`
   and runner v2's `key_gate` are imported and never copied, and the loop adds
   no third gate; but with every provider offline no credential was ever
   acquired, so 5-per-key and "a reading call and a dispatch call in flight
   together are held to five per credential between them" are untested by
   execution. `endpoints.json` has 24 endpoints and two `key_env` values, so
   the live capacity is 5 × 2.
3. **The two key names must be in the environment of the process that runs the
   driver, and nowhere else.** They are read by `provider_openai_compat` at
   call time only — never by the driver, never written into any record; the
   ledger writer and `write_new` both refuse credential-bearing output. The
   dry run proves the driver needs **no** key name in offline mode: the run
   completed with no `SYNTHETIC_*`/`DRYRUN_*` name set at all.
4. **`publish_ref` is a branch, and it is not `main`.** L001 declares
   `origin/claude/project-state-direction-j5rbun` (ruling 2). The dry run
   published to `origin/main` of a temp bare repository. The live run's first
   publication is the first test of a non-forcing push onto a shared branch,
   of the re-fetch-and-republish path when the ref has moved, and of the
   three-non-converging-attempts halt.
5. **The repository's own decision ledger under contention.** Receipts are
   appended to `docs/DECISION_LEDGER.md` in byte mode under `flock`, with the
   receipt id minted under the same lock. The dry run appended to a throwaway
   copy with no concurrent writer.
6. **The reading arm on published H005 material.** The dry run read
   `synthetic`'s eight rows; L001 declares twenty-two H005 rows and sixteen
   C001 register cells. `cell_key_for` is self-tested at PREFLIGHT for
   admissibility and injectivity over the whole declared set, and
   `READING_ROW_UNRESOLVED` fires if a declared row names no row of the use
   table this cycle built — which is the first thing a live PREFLIGHT/READ can
   discover about the real material.
7. **A pre-registered condition still has no declaration**
   (WAVE3 §8 6 / WAVE4 §8 7 / WAVE5 §9 3). `decide.Instrument.preregistered_condition`
   exists and no config key names one; `stop_reason:preregistered_condition:<id>`
   is therefore unreachable in this plan. Either `LoopConfig` grows the block
   before S0 — a new `loop_plan_id` — or the live run records the clause as
   unreachable.
8. **The cadence receipt is still unwired** (design 4.5; WAVE5 §9 11).
   `receipts.Cadence` and `checkpoint_receipt` are built and the driver calls
   neither, because the only clock this wave could drive is a fixture's. **The
   dry run's answer to the question WAVE5 asked: leave it to the first live
   run.** An injected clock would have proved that a fixture can move a
   counter, not that a 240 s boundary is noticed; the live run is where a step
   really takes longer than four minutes.
9. **Two occurrences sharing one credential in one process** (WAVE5 §9 7) is
   still unexercised: the dry run drives one occurrence.
10. **The audit window's real cost.** PREFLIGHT reports the two derivable legs
    and names the remainder of `max_calls` as the window's allowance
    (`audit_allowance: 164` in the recorded verdict). The live run is the first
    occasion on which `reading_set.json`'s `46` can be checked against what a
    window actually spends.
11. **`synthetic` should grow the baseline-kind collision as material** (§2's
    last paragraph). Until it does, the acceptance proof owns that one
    fixture-built condition and says so in its own docstring.

---

## 6. The operator command sequence for the first live run, S0 to S15

Zero human steps in the walk itself. Three commands, from the repository root,
with the two credential names present in the environment of that shell and
nowhere else (ruling 4: the process environment or the gitignored root `.env`;
never a tracked file, log, receipt or report).

```sh
cd /home/user/miniReason
git switch claude/project-state-direction-j5rbun      # ruling 2's branch
git pull --ff-only

# S0 — freeze the config, mint loop_plan_id, open every cell, seal every
#      contrast baseline, write plan.json.
PYTHONPATH=$PWD/src python3 tools/auto_loop.py preregister \
    --config loop-prereg/config.json

# S1 — offline, zero calls: verify every pin, build the seat plan off the
#      pinned endpoints.json, self-test every reading coordinate and the
#      block-streak counter, compare the opened register cells with what
#      markprep will produce, refuse a planned figure past max_calls.
PYTHONPATH=$PWD/src python3 tools/auto_loop.py preflight \
    --config loop-prereg/config.json

# S2 … S15 — publication, dispatch, import, use table, read, mark, audit,
#      adjudicate, decide, publish, close.  Resume is this same command.
PYTHONPATH=$PWD/src python3 tools/auto_loop.py run \
    --config loop-prereg/config.json
```

**If it stops.** Exit is non-zero and the code is on stderr. One read-only
command says what is in the way and what the acknowledgement flag takes:

```sh
PYTHONPATH=$PWD/src python3 tools/auto_loop.py status \
    --run experiments/loops/L001-loop-first-live-2026-09-14
```

`blocking` names the code and `acknowledge` carries the step key. A custody
halt is **never** worked around: re-verify the tree, and only if the finding is
explained does an operator record the explanation —

```sh
PYTHONPATH=$PWD/src python3 tools/auto_loop.py run \
    --config loop-prereg/config.json \
    --acknowledge <the step key status printed> \
    --reason "<what was checked, and what it showed>"
```

which is itself written into the ledger. `--cycles N` lowers the declared
budget and may never raise it (`BUDGET_RAISED` before anything is written);
`--mode` and `--publish-ref` are inside `loop_plan_id` and are refused on
disagreement rather than applied. An appellate ruling is staged with
`appeal --run <run> --path <ruling.json>` and applies at the next `run`;
`reopen --run <run> --reason <one of the plan's reopen_reasons>` is what lets a
spent row be read again, and any other reason is refused and recorded.
