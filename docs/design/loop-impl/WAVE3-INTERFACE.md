# Wave 3 — the integrated public interface

Read `WAVE0-INTERFACE.md`, `WAVE1-INTERFACE.md` and `WAVE2-INTERFACE.md` first;
where they differ, the later one governs. This is the wave-3 integrator's
record of what the three wave-3 modules expose after reconciliation, what moved
in earlier waves to let them agree, the disposition of every acceptance clause,
what was kept from the Kimi K3 drafts and what was rewritten with the reason,
the bundle-facing consequences, and the questions W4-READER, W4-MARKER and
W5-DRIVER must answer.

Clone: `scratchpad/loop-impl/repo`, branch cut at `9045a94`; the loop tree is
untracked there and **nothing was committed**.
Sources: `src/minireason/loop/{trial,audits,report}.py`, with edits in
`{types,standard,graph}.py`; tests: `tests/loop/test_{trial,audits,report}.py`
and `tests/loop/test_{types,contracts}.py`.

Drafts: `loop-impl/wave3-drafts/{trial,audits,report}/` (the trial draft copied
there from `kimi/prod-runs-w3/w3-trial-retry/sandbox/`). All three Kimi runs
ended without a final message — two at the 90-iteration cap, the trial retry on
the ruling-13 gateway close at iteration 60 — so none was known to be green.

**Test lines, exactly as run.**

| what | before | after |
|---|---|---|
| `tests.loop.test_audits` as delivered | `Ran 42 tests` `OK` | `Ran 56 tests` `OK` |
| `tests.loop.test_report` as delivered | `Ran 50 tests` `OK` | `Ran 66 tests` `OK` |
| `tests.loop.test_trial` as delivered | `Ran 75 tests` `FAILED (failures=10, errors=15)` | `Ran 83 tests` `OK` |
| loop suite, quiesced tree (`discover -s tests/loop -t .`) | `Ran 1223 tests` `OK (skipped=1)` | `Ran 1428 tests` `OK (skipped=1)` |
| whole repository (`discover -s tests`) | `Ran 2466 tests` `OK (skipped=2)` † | `Ran 2671 tests` `OK (skipped=2)` |

† The repository before-line is `WAVE2-INTERFACE.md`'s recorded after-line, not
one this pass re-measured: reproducing it would mean removing the three modules
*and* reverting the `types`/`graph`/`standard` edits they required. The
arithmetic checks exactly — 2671 − 2466 = 205 = 83 + 56 + 66, the three wave-3
test files' own totals — and the loop-only before-line **was** measured here, on
the tree as it stood before the first copy. The one skip in the loop suite is
the PLAN-digest pin on a checkout that predates §15 (WAVE2 §9); the second
repository skip is outside the loop package.

No provider call was made, no credential was read or printed, and nothing
outside the clone was written. Files read read-only outside the clone: the
Kimi sandbox copies of the drafts, and
`docs/reviews/kimi-k3-subagent-2026-09-14/REPORT.md` in the live checkout.

---

## 0. The map after wave 3

```
types ──► standard ──► contracts ──┬──► surface ──┬──► packs ──┐
  │                                │              │            ├──► trial
  ├──► custody ──┐                 ├──► seats ────┴──► roles ───┘
  ├──► receipts ─┼──► steps        ├──► graph ──┬──► decide ──► report
  ├──► publish ──┘                 └──► synthetic│      ▲          ▲
  └──► obligations ────────────────────────────────────┘          │
                                                └──► audits       │
                                                custody, obligations
```

| module | imports (siblings only) |
|---|---|
| `trial` | `contracts`, `graph`, `packs`, `roles`, `seats`, `standard`, `surface`, `types` |
| `audits` | `contracts`, `graph`, `standard`, `types` |
| `report` | `contracts`, `custody`, `decide`, `graph`, `obligations`, `standard`, `types` |

**No wave-3 module imports another wave-3 module.** The exact edge set and the
acyclicity are asserted by
`tests/loop/test_contracts.py::WOneOwnerPerSharedConstant::test_the_import_graph_is_the_one_the_interface_documents`,
so a later wave that adds an edge has to record it here first.

Three classes of edge go beyond the wave plan's `depends_on`, and each is here
because a spelling has exactly one owner:

* **`trial`'s list is complete.** It additionally reaches `seats` for the
  `SeatPlan` type G0 reads, and `types` for `block_code`.
* **`audits` reaches W0-STANDARD** (the banner, the rubric body, the
  unresolved token) for the reason every wave-2 module does, and reaches
  **neither `packs` nor `roles`** though its `depends_on` names both: W2-PACKS
  renders the packs of the *trial* and has no shape for an audit re-ruling, and
  W2-ROLES sits behind the module's own `judge_caller` boundary. The one
  provider seam of the audit layer is that callable, which the driver binds to
  `roles.call_judge`.
* **`report` reaches `standard`** (the ceiling, its required sentences, its pin
  key, the two scans), **`custody`** (`CustodyMismatch` and the two pin
  refusals, so a ceiling refusal *is* the custody fact it already is rather than
  a private code), and **`obligations`** (`Loss`, and the `rendered_files`
  record name p4 reads).

---

## 1. `trial.py` — W3-TRIAL

**What it is.** One guarded trial, G0–G12 in §2.4's order. It renders no pack
(W2-PACKS does), speaks to no model (W2-ROLES does) and registers no reading
(W1-GRAPH's door is W4-READER's). It owns the guard's sequencing and the
records the sequencing leaves.

**Entry points.** `run_trial(harness, surface, standard_body, seats, config, *,
mode, key, records_dir, provider_factory=None, reopen_reason=None) ->
TrialResult`; `build_transcript(result) -> str`;
`open_trial_harness(root, cell) -> PreparedTrial`.

**Records.** `TrialResult` carries `cell, mode, outcome, blocks, transcript,
checks, calls, standard_id, critic, defender, rulings, paraphrases,
paraphrase_rulings, reading, measures, reopen_reason, surface_digest,
exchange_digest, pack_digests`. `Block(code, check, detail, prompt_ref_path,
raw_ref_path, prompt_sha, raw_sha)`; `CallRecord(role, coordinate, seat_label,
result)`; `PreparedTrial(harness, standard_id, cell, material_id)`.

**Outcome vocabulary.** `OUTCOMES = ("blocked", "not-sustained", "sustained",
"no-trial", "unresolved")` — none of them a quantity, and none of them a
status on a cell: the cell's standing is W1-GRAPH's adjudication and nothing
here writes it.

**Guard checks.** `GUARD_CHECKS` names eleven: `G0-constitution`, `G1-schema`,
`G2a-uniqueness`, `G2b-uniqueness`, `G3-operative-target`, `G4-vocabulary`,
`G5-unanimity`, `G6-order-swap`, `G7-paraphrase-spot-check`, `G11-no-reread`,
`G12-no-scoring-key`. Every one prints on every transcript as `performed` or
`not_performed`; a check the run never reached is never omitted. **G8, G9 and
G10 are absent on purpose**: the baseline seal, the kind-grain replicate rule
and the C001 program pre-empt are W2-MARKPREP's and W4-MARKER's, and a second
implementation of them here would be a second owner. §5 records this as the
one unclosed half of the "every G0–G12 block path" clause.

**Block codes are imported, never retyped** (PR-12's rule, held):
`BLOCK_CODES = types.BLOCK_CODES`; `SCHEMA_BLOCK`/`PROVIDER_BLOCK` come from
`roles`, `REFERENTIAL_INTEGRITY_BLOCK`/`OPERATIVE_TARGET_BLOCK` from `surface`,
and the remaining four are built through `types.block_code`.
`test_trial.py::TheModuleItself::test_no_code_is_raised_as_a_bare_literal`
asserts no `_refuse("…")` or `TrialRefused("…")` call site exists.

**Exceptions and codes.** `TrialRefused(code, detail="")` — a trial that could
not be *formed*, so no Measure event and no block. `ReopenRefused(detail)` —
raises `REOPEN_REFUSED`, which `types` already owned and which is deliberately
**not** in `NEW_CODES`.

| code | table | raised where |
|---|---|---|
| `TRIAL_ARGUMENT_INVALID` | `types.FAILURE_CODES` (new, folded in) | a surface, config, harness, key or transcript input that is not the shape |
| `TRIAL_MODE_UNEXPECTED` | `types.FAILURE_CODES` (new, folded in) | a mode that is not the standard's absolute rubric, or a register cell |
| `TRIAL_SEAT_PLAN_INVALID` | `types.FAILURE_CODES` (new, folded in) | the `seats` argument is not a `seats.SeatPlan` |
| `TRIAL_PRIOR_STATE_UNREADABLE` | `types.FAILURE_CODES` (new, folded in) | G11 could not read the cell's prior state, or the config widened the reopen list |
| `REOPEN_REFUSED` | `types.FAILURE_CODES` (already there) | G11, at the write |
| the ten `blocked:*` | `types.BLOCK_CODES` | returned on `TrialResult.blocks`, never raised |

---

## 2. `audits.py` — W3-AUDITS

**What it is.** The four §2.5 audits over readings *already on record*. It
imports no provider module and opens no connection: the one provider seam is
`judge_caller(seat_label, pack, coordinate) -> JudgeRuling | None`, and `None`
is a delivery fact about the route, never a reading.

**Entry points.** `build_calibration_set(standard) -> list[CalibrationCase]`;
`paraphrase_invariance(harness, judge_caller, readings) -> list[AuditHit]`;
`premise_deletion(harness, judge_caller, readings) -> list[AuditHit]`;
`planted_flaw_calibration(harness, judge_caller, calibration_set, *, panel=None,
bound=None, account="") -> CalibrationOutcome`;
`disagreement_series(harness, judge_caller, readings, *, panel=None)`;
`run_audits(harness, judge_caller, readings, config, *, panel=None) ->
AuditReport`; `render_ruling_pack(...) -> bytes`.

**Records.** `CalibrationCase`, `AuditHit(kind, seat, coordinate, detail,
finding_id, targets)`, `Disagreement`, `SpawnSignal(trigger, observed, bound,
account, anchors)`, `CalibrationOutcome(share, errors, exercised, spawn, hits)`,
`AuditReport(schema, findings, series, calibration, collapsed, logs)`.

**`planted_flaw_calibration` keeps the design's declared `float|None`** as
`CalibrationOutcome.share`, with `__float__` and equality against a float, so a
caller written to the wave plan's signature reads the bare float. **The float
adjudicates nothing**: it does not enter a reading's standing, it is never
compared between seats, and the only consequence it may have is crossing a
pre-registered instrument bound (ruling 7). What collapses a reading is the
per-error demonstrative warrant in `CalibrationOutcome.hits`, which is a warrant
against a validity node and not a rate. Nothing in `report.py` renders a share.

**The panel has no spelling here.** `PANEL_ON_RECORD = "graph.seats_on_record"`.
An explicit `panel=` is the driver's (the labels the pinned seat plan froze);
without one the panel is the seats that carry a `ν_soundness` in this graph —
exactly the seats whose readings a hit can collapse.

**The margin is the config's.** `judge_err_max` and `judge_err_max_account` are
read off `config.audit` and **there is no fallback for either**: an absent bound
is `CONFIG_MISSING_KEY`, an empty account is `CONFIG_INVALID_VALUE`.

**Exceptions and codes.** `AuditError(code, detail="")`. `NEW_CODES` is
**empty**: both refusals are codes `types` already owns
(`CONFIG_MISSING_KEY`, `CONFIG_INVALID_VALUE`). `SPAWN_AUDIT_THE_CRITIC =
"audit-the-critic"` is a signal token on a report — not a failure code, not a
stop reason, not a status;
`test_audits.py::TheSpawnSignal::test_a_spawn_is_a_returned_signal_and_never_a_raised_code`
asserts it is in neither table.

**New pin.** `CALIBRATION_EXCHANGES_SHA256 =
91c29e1e71719d815c21c2697f4aa68a7c983be21df945ad6b1e5042183981e5` over the five
constructed anchor exchanges. See §6 for why they live here and what the bundle
reviser must decide.

---

## 3. `report.py` — W3-REPORT

**What it is.** Four pure functions onto Markdown. No renderer reads a clock,
writes a file, or decides anything.

**Entry points.** `render_reading_table(harness, plan, *, state=None)`;
`render_comparison(harness, plan, *, state=None)`;
`render_cycle(decision, state)`; `render_closing(run)`;
`ceiling_key_of(plan)`; `block_line(cell, reason)`; `audit_line(finding)`;
`rendered_files_record(files)`.

**Records.** `ReportPlan(loop_plan_id, pins, reading_set, ceiling_text)`,
`CycleState(standings, blocks, indeterminate, unread)`,
`ClosingRun(plan, decision, blocks, standings, indeterminate, unread,
audit_findings, appellate_rulings, state)`, `RegisterRow`.

**Re-exports, not definitions.** `CEILING_REQUIRED_SENTENCES` **is**
`standard.CEILING_REQUIRED_SENTENCES`; `BLOCK_REGISTER_HEADINGS` is built from
`types.CEILING_BLOCK_REASONS` in the ceiling's own order plus `constitution`
as the tenth row; `PROTECTED_LOSS_SENTENCE` is `decide.PROTECTED_LOSS_SENTENCE`
and `LOSSES_OUTSIDE_P_SENTENCE` is `decide.NET_WITHDRAWAL_SENTENCE`;
`TRICHOTOMY_WORDS` is derived at import from the frozen ceiling's own sixth
clause; the ceiling's pin key is `standard.CEILING_PIN_KEY`.

**The `rendered_files` record has an owner: this module** (WAVE2 open question
3). `RENDERED_FILES_RECORD = "rendered_files"` and
`rendered_files_record({path: text})` builds it; `files` holds the **rendered
bytes**, not a summary of them, because `obligations.no_scoring_key` (p4)
tokenises headings and table header rows out of the text. Every renderer builds
one over its own output and runs `contracts.assert_no_scoring_keys` across it
before returning, so a renderer cannot emit what the obligation would refuse.
The driver registers the run's whole map through W1-GRAPH.

**Exceptions and codes.** `ReportRefused(code, detail="")`, a
`custody.CustodyMismatch`, so one `except` catches a ceiling refusal beside
every pin refusal. `NEW_CODES` is **empty**; the four codes it can name —
`SOURCE_PIN_MISSING`, `SOURCE_PIN_MISMATCH`, `PIN_MAP_MISSING`,
`STANDARD_DATA_MALFORMED`, plus `CEILING_TEXT_MALFORMED` on
`standard.StandardInvalid` — are all `types.FAILURE_CODES` members already.

---

## 4. The code tables after wave 3

`types.FAILURE_CODES` now carries **205** members. Four were folded in this
pass, all `trial`'s; `audits` and `report` declare an empty `NEW_CODES` and
raise nothing the table did not already name.
`tests/loop/test_types.py`'s `FOLDED_IN` now names **nineteen** modules and
`FRONTIER` is empty; `TOKEN_ARGUMENT` gained seven entries
(`audits._fail`, `audits.AuditError`, `report.ReportRefused`,
`report.StandardInvalid`, `trial._refuse`, `trial.TrialRefused`, and
`trial.ReopenRefused` as a literal-in-body).

`types.BLOCK_CODES` is unchanged at **ten**; `types.OUTCOME_CODES` at **one**;
`types.CEILING_BLOCK_REASONS` unchanged at nine.

**One code the draft declared was dropped, and one was repointed.**
`TRIAL_PARAPHRASE_SPAN_LOST` was removed from `NEW_CODES` and never entered
`FAILURE_CODES`: its own declared reason described a *non-raise* (the
spot-check is recorded `not_performed`), so nothing in the package could reach
it, and a code no call site reaches is a code no register prints.
`TRIAL_SEAT_PLAN_INVALID` was declared for G0's family rules — which the
module's own deviation 5 settles as a **block**, not an exception — and was
therefore also unreachable; it now names the one seat-plan refusal that really
is a form error (the `seats` argument is not a `SeatPlan`) and its reason was
rewritten to say so.
`test_types.py::test_every_declared_code_is_reached_by_the_package_or_allow_listed`
is what caught both.

**The `NEW_CODES` tests were restated as the fold-in contract**, in wave 2's own
spelling: every `NEW_CODES` key is a member of `FAILURE_CODES` and of neither
other table. As written by the drafts they asserted the table did *not* carry
the code — true only until the module lands.

---

## 5. Disposition of every acceptance clause

### W3-TRIAL

| clause | disposition | test |
|---|---|---|
| every G0–G12 block path yields no warrant, one Measure event and a `BLOCK_CODES` reason | **Held for the ten block codes `trial` can emit.** G8/G9/G10 are W2-MARKPREP's and W4-MARKER's and are out of this module's scope, stated in §1. The `blocked:provider` path was **added**: the draft asserted the constant equalled `roles.PROVIDER_BLOCK` and never ran a trial through it. | `EveryBlockPathYieldsNoWarrantOneMeasureAndAReasonCode` (8 tests incl. `test_a_provider_failure_is_the_tenth_block_path_and_mints_no_warrant`, `test_a_constitution_block_dispatches_nothing_and_names_no_ref`) |
| an ensemble split blocks and records both rulings verbatim, never a majority | **Rewritten.** The draft's G5 took the union of both presentation orders, so every G6 flip was published under the split code. | `AnEnsembleSplitBlocksAndRecordsBothRulingsVerbatim` (6 tests incl. the added `test_one_seat_moving_with_the_order_is_an_order_swap_not_a_split`) |
| a quote occurring twice in the material blocks | **Rewritten (fixture).** The draft asserted `"carries its terms"` occurred twice without running the count; it occurs once, so the class exercised nothing. | `AQuoteOccurringTwiceInTheMaterialBlocks` (4 tests incl. the added `test_the_fixture_really_carries_the_quote_twice`) |
| a quote resolving only into the pack framing blocks | Kept. | `AQuoteResolvingOnlyIntoThePackFramingBlocks` |
| a `decisive_point` absent from case+newline+answer blocks, and the transcript satisfies `conforming_transcript` | Kept. | `ADecisivePointAbsentFromTheExchangeBlocks::test_the_emitted_transcript_satisfies_the_vendored_gate` |
| an order-swap flip blocks | **Rewritten** (see G5 above). | `AnOrderSwapFlipBlocks` |
| a paraphrase flip blocks and is logged against the seat | Kept; only the fixture was repaired. | `AParaphraseFlipBlocksAndIsLoggedAgainstTheSeat` |
| a paraphrase that lost a quoted span marks the spot-check `not_performed` | Kept. | `AParaphraseThatLostASpanMarksTheSpotCheckNotPerformed` (4 tests) |
| re-reading an unresolved cell without a listed `reopen_reason` raises `ReopenRefused` **at the write** | **Extended.** Held for every prior outcome the draft logged; a critic answering `none` logged nothing, so that one cell could be re-read freely. | `ReReadWithoutAListedReasonRaisesReopenRefused` (6 tests) and the added `ACriticAnsweringNoneEndsTheRowAtOneCall::test_a_re_read_after_none_is_refused_without_a_reopen_reason` |
| zero sockets on OfflineProvider | Kept. Every trial in the file runs inside `no_sockets()`, which replaces `socket.socket`, `socket.create_connection` and `transport._open`. | `TheWholeModuleRunsOnOfflineProviderFixturesWithZeroSockets` (5 tests) |

### W3-AUDITS

| clause | disposition | test |
|---|---|---|
| calibration rows are true by construction, and a clean control that sustains is scored as an error | Kept. | `TrueByConstruction` (7 tests) |
| a seeded flipping judge produces a paraphrase hit whose warrant collapses that seat's readings on recompute | Kept in the module; the **fixture's seat spelling was rewritten** (§6). | `ASeededFlippingJudge` (6 tests) |
| a ruling surviving deletion of its own `decisive_point` produces a premise hit | Kept. | `PremiseDeletion` (4 tests) |
| an error rate above `JUDGE_ERR_MAX` returns a Spawn signal | **Rewritten.** The draft read an invented `0.2` inside `planted_flaw_calibration` and relabelled the signal with the config's values afterwards, so a config bound *below* 0.2 could be crossed with no signal at all. | `TheDeclaredMargin` (6 tests, added) and `TheSpawnSignal` (4 tests) |
| every audit call reaches the log exactly once | Kept. | `EveryCallLoggedOnce` (3 tests) |
| audit findings carry their own validity nodes and are themselves attackable | Kept; **the calibration arm's hits now reach the report**, so a collapse the report could not name no longer happens. | `FindingsAreAttackable` (2 tests) and `TheCalibrationHitsAttachToRealSeats` (4 tests, added), incl. `test_every_calibration_hit_is_named_on_the_report` |

### W3-REPORT

| clause | disposition | test |
|---|---|---|
| rendering refuses without CEILING.md at its pinned sha | Kept; the pin **key** moved to one owner (§6). | `RenderingRefusesWithoutThePinnedCeiling` (9 tests) |
| every required ceiling sentence appears verbatim in every table and the closing record | Kept. | `EveryRequiredCeilingSentenceAppearsVerbatim` (6 tests) |
| blocks print with counts by reason code | **Extended.** Held for `CYCLE.md` and `CLOSING.md`; `READING_TABLE.md` built an empty block list it never filled and `COMPARISON.md` printed no register at all while its docstring said it did. | `BlocksPrintWithCountsByReasonCode` (6 tests) and `TheReadingTableCarriesItsOwnBlockRegister` (10 tests, added) |
| an all-blocked run renders as declined-to-read and never as no relations found | **Rewritten.** The draft's condition fired on any run with nothing read, so a run whose cells were *deliberately read* and stayed unresolved claimed "every reading cell was blocked". | `AnAllBlockedRunRendersAsDeclinedToRead` (4 tests) and `TheReadingTableCarriesItsOwnBlockRegister::test_a_deliberate_unresolved_run_does_not_claim_the_instrument_declined` |
| unread, unresolved and machine-unresolved print as three distinct states | **Extended.** A blocked cell that never opened printed as `unread` in the table *and* in the machine-unresolved list — one cell in two of the three states. | `TheThreeCellStatesPrintAsThreeThings` (6 tests) and `test_a_blocked_cell_that_never_opened_prints_in_exactly_one_state` |
| no rendered artifact contains a score, a rank, a combined register or the token "exhaustion" | Kept. | `NoRenderedArtifactCarriesAProhibitedToken` (6 tests) |
| `losses_outside_P` is present when empty | Kept; **`would_reopen` now prints on every stop**, a protected loss included (design §5). | `LossesOutsidePIsPresentWhenEmpty` (3 tests) and `AProtectedLossStillSaysWhatWouldReopenIt` (2 tests, added) |
| `appellate_rulings: 0` renders the not-validated sentence | Kept. | `AppellateRulingsZeroRendersNotValidated` (3 tests) |

---

## 6. Kept versus rewritten, with the reason

### `trial.py`

**Kept.** The whole guard sequence and its order; the eleven-check record and
its `performed`/`not_performed` vocabulary; the Measure-on-block discipline with
the spent prompt and raw refs beside it; the G11 gate reading a prior attempt
off the Measure log rather than a side table; the block-code imports; the
transcript renderer; the deviation record. The module was, structurally, sound.

**Rewritten — 1. G5's scope.** The draft computed unanimity over
`{(seat, order): sustained}` — the union of both presentation orders — so a seat
that moved *with the order* was reported as a disagreement *between the two
families*. Two different findings about two different things, routing to two
different Spawns. G5 now compares the two seats at the as-declared
presentation, and G6 compares each seat's two presentations; §2.4's own order
(G5 then G6) is why each can name its own fact.

**Rewritten — 2. the exhaustion scan over a transport's words.** `build_transcript`
ran `standard.assert_no_exhaustion_claim` over the whole text including a
block's `detail`. The transport spells an empty offline script "offline script
exhausted", so a provider block raised `RESOURCE_BOUNDARY_MISDESCRIBED` and
**could not be rendered at all** — the tenth block path was unreachable. W2-ROLES
already ruled (wave-2 item 42(h)) that the scan is not run over delivery error
strings, because an observation is never rewritten. The quoted details are
lifted out and the module's own prose is scanned;
`_assert_this_module_claims_no_exhaustion` carries the reason, and a test shows
a claim this module itself made still fails the scan.

**Rewritten — 3. `none` left no trace.** Deviation 6 argued that a `none`
answer is not a block and so logs no Measure. True about blocks — but G11 reads
a cell's prior attempt off exactly those events, so a `none` was the one outcome
a caller could re-read freely, on the answer most likely to invite a retry. A
Measure is information and not a verdict (the module already writes one for a
not-sustained ruling, which is also not a block), so a `none` now writes one
naming the cell's default and the critic's spent call. `blocks` stays empty and
the outcome is still `no-trial`.

**Rewritten — 4. two unreachable codes**, §4.

**Fixture rewrites (the draft's tests, not its module).** The `Scripted`
provider factory handed every call a provider over the *whole* reply list, and
W2-ROLES builds a fresh provider per call, so each replayed from index 0: both
judge seats got the *first* reply and no scripted dissent ever reached a second
seat. That single defect is why ten tests and fifteen errors stood against a
module that was mostly right — the split, order-swap and paraphrase-flip
clauses all read as "no block". The factory now consumes a queue per
`(role, coordinate)` across calls. Also: `P` (`packs`) was used and never
imported; `self.scripts(**overrides)` passed tuple keys as keywords; `override`
was defined twice with the first shadowed; the doubled-quote fixture asserted a
count it never ran; the "unanimous no" fixture declined in one order only and so
built an order-swap flip; and `test_every_call_coordinate_was_spent_exactly_once`
compared `(role, key)` pairs when a coordinate is `(role, seat, key)`.

### `audits.py`

**Kept.** The four arms and their shapes; the re-ruling pack renderer with the
banner and rubric body imported; the `judge_caller` boundary and its treatment
of `None` as a delivery fact; `CalibrationOutcome` as the design's `float|None`
plus what a bare float cannot carry; the recompute read off a *reopened*
harness; the per-coordinate log; `graph.register_audit_warrant` /
`graph.validity_nodes_for_seat` as the only way a hit reaches a validity node.

**Rewritten — 1. the invented panel (the composed seam).** The draft declared
`_PANEL = ("judge-1", "judge-2")` with a comment claiming that is what W2-ROLES
writes on a call record. It is not: `roles.Coordinate.seat_label` is `judge#1`,
and `judge-1` is only the directory *slug* tail. Probed on the integrated tree,
a reading registered by `judge#1` left
`graph.validity_nodes_for_seat(harness, "judge-1") == ()` while **six
calibration errors registered warrants against that empty window** — hits that
read as hits and collapse nothing. The draft's own fixture registered its
reading under `judge-1`, so no test could see it. The panel is now the driver's
explicit `panel=` or `graph.seats_on_record`, and the tests register under the
real spelling.

**Rewritten — 2. the invented margin and its account.** `planted_flaw_calibration`
read a hard-coded `0.2` with a hard-coded account, minted the Spawn against
*that*, and `run_audits` then relabelled the signal with the config's bound. Two
consequences, both probed: a config bound of `0.05` against an observed share of
`0.1` produced **no signal at all**, and a signal minted against 0.2 could be
published naming a bound it had not crossed. Worse, the invented account was
REVIEW-PREREG PR-09's own defect retyped — "the calibration set is five anchors,
so the margin is one anchor of five", which misstates its denominator against a
nine-row `calibration.json`. Ruling 7 admits `judge_err_max` as a bound on the
instrument *on condition that its firing carries an account*; an account the
module wrote accounts for nothing. Both now come from the frozen config, with no
fallback, and `test_no_margin_and_no_account_is_spelled_in_this_module` asserts
the string `0.2` is absent from the source.

**Rewritten — 3. calibration hits vanished.** The draft registered each
calibration error's warrant and then executed `del hit`, so the finding
collapsed readings but never reached `AuditReport.findings`. A collapse the
report cannot name is a collapse nobody can attack. The hits ride on
`CalibrationOutcome.hits` and `run_audits` extends `findings` with them.

**Rewritten — 4. a fabricated ensemble.** `disagreement_series` fell back to the
module's panel whenever a reading named fewer than two seats, so one seat's two
answers could be printed as a variance between two seats — the module's own
stated rule, broken by its own fallback. A reading for which no pair can be
named now contributes **no row**.

**Rewritten — 5. two private seams.** `graph._decode` and
`harness.state.artifacts` were read directly; `graph` now publishes
`reading_bodies`, `reading_transcript` and `seats_on_record`, and `audits` uses
them. One owner for the reading body's shape.

**Added.** `CALIBRATION_EXCHANGES_SHA256`, so "the set is fixed at pin time" is
checkable rather than promised.

### `report.py`

**Kept.** The four renderers and their section structure; the ceiling block
printed as plain unwrapped paragraphs with the verbatim check; the block
register printing every heading every time with its tally; the trichotomy's
three sections; the `CycleState`/`ClosingRun` declared-record deviation; the
four gates every artifact passes before it leaves; the closed block-reason
vocabulary with `constitution` as the register's tenth row; the refusal of an
open chain at CLOSE.

**Rewritten — 1. `READING_TABLE.md` had no blocks.** `render_reading_table`
built `machine: list[tuple] = []` and never filled it, so the table printed `x0`
against every reason on a run that had been entirely blocked and its
machine-unresolved section was always empty. Both table renderers now take a
keyword-only `state`; the wave plan's declared two-argument call still renders.

**Rewritten — 2. `COMPARISON.md` promised a register it did not print** (the
docstring said "the block register prints with counts beside the rows"). It
prints one now.

**Rewritten — 3. declined-to-read fired on the wrong run.** Three different runs
answer "nothing was read" and only two of them are the instrument declining.
`_declined_to_read` now prints the sentence for a run with blocks and no
reading, and for a table with no cells at all, and never for a run whose cells
were deliberately read and stayed at the grounded default.

**Rewritten — 4. one cell in two states.** A blocked cell that never opened
printed as `unread` in the trichotomy table while also appearing under
machine-unresolved.

**Rewritten — 5. three retyped spellings.** `PROTECTED_LOSS_SENTENCE` and
`LOSSES_OUTSIDE_P_SENTENCE` were *paraphrases* of `decide`'s own sentences —
worse than a retype, because the record would have carried two statements of one
rule in two forms beside `decision.record_sentences`. The ceiling's pin key was
rebuilt from `types.PINNED_SOURCE_PATHS[0].split("/")[0]` plus a retyped path,
and the test file retyped it a third time; `standard.CEILING_PIN_KEY` is now the
one owner. `render_comparison` split the cell key on `"|"` rather than using
`graph.CellKey.coerce`.

**Rewritten — 6. `would_reopen` was dropped on a protected loss.** Design §5:
"Every stop carries a mandatory `would_reopen` prose field." The draft printed
the protected-loss sentence *instead of* the field, on the one stop that most
needs to say what would reopen the question.

**Added.** `RENDERED_FILES_RECORD` / `rendered_files_record`, answering WAVE2
open question 3.

### Declined, with the reason

* **Moving the calibration exemplar bytes into `standard.py`.** Design §2.1 says
  the standard artifact carries "anchor exemplars for the calibration set", and
  `standard.CalibrationAnchor` carries a construction and a ground-truth reason
  but **no exchange**, so the ground-truth bytes the panel is asked about are
  not inside `STANDARD_BODY_SHA256`. Moving them is the right end state and it
  moves the standard's digest a fourth time, which `VALIDATION.md`'s
  `calibration.json` digest and the bundle's PR-06 rewording both depend on.
  It is one edit to make with the bundle revision, not before it. Pinned here
  as `CALIBRATION_EXCHANGES_SHA256` and listed in §8 as a question for the
  bundle reviser.
* **Implementing G8/G9/G10 in `trial.py`.** They are W2-MARKPREP's seal and
  kind-grain rule and W4-MARKER's caller. A second implementation would be a
  second owner of the baseline discipline, which is the one discipline the
  design makes physically irreversible.
* **Defining the guard-block streak in code.** `trial` carries no state across
  trials by construction, so the counter is the driver's. §8 publishes the
  definition as a ruling for W5-DRIVER to implement; it is not implemented here.

---

## 7. Bundle-facing consequences (REVIEW-PREREG.md)

| item | what wave 3 changes |
|---|---|
| **PR-01** — `calibration.json` carries the forbidden key `scoring` | **Unchanged and still a blocker.** Nothing in wave 3 reads that field: `audits.build_calibration_set` reads the *standard's* anchors (`id`, `must_sustain`, `expected_relation`, `construction`, `ground_truth_reason`) and never `calibration.json`. The bundle's own file still fails `assert_no_scoring_keys` and would stop the first run at S0. The fix is the bundle's: rename the key to `error_rule`, and add the scan to `validate.py`. |
| **PR-05** — `p4` unfalsifiable on rendered files | **Resolved on the writer's side.** W3-REPORT owns the `rendered_files` record, its `files` values are the rendered bytes, and every renderer runs `standard.assert_no_scoring_headers` and `contracts.assert_no_scoring_keys` over its own output before returning — so the loop cannot emit an artifact p4 would then refuse. The bundle half stands: `p4`'s wording should carry the quoted-material exemption in the same sentence. |
| **PR-09** — provisional guard-rail accounts, one factually wrong | **Sharpened, and now enforced.** `audits` refuses an empty `judge_err_max_account` outright, and it no longer carries an account of its own — the draft had retyped PR-09's wrong "five anchors, so one anchor of five" arithmetic into the module. The **bundle must still settle both accounts before S0**: a `judge_err_max_account` reading "PROVISIONAL, to be settled at pre-registration review" is non-empty, so the program will accept it and publish it verbatim when the rail fires. That is a prose obligation the program cannot check. PR-09's arithmetic point stands: the account must state the denominator the run actually uses (anchors × exercised seats), and the module computes the share over the *exercised* set, which the account should name. |
| **PR-12** — block-code spelling, and the tenth code | **Resolved on the module side, both halves.** No wave-3 module writes the `blocked:` prefix in a string literal; `trial` imports or builds every code through `types.block_code`. And `report.BLOCK_REGISTER_HEADINGS` prints the ceiling's nine **plus `constitution`** as the register's tenth row, so `blocked:constitution` — the G0 non-evaluability channel FW5:688 needs kept open — has a printed home. The bundle half stands: `obligations.json` o1/o2 must be reworded to o4's spelling, and the ceiling's own prose must either name the tenth reason or say where a constitution block is reported. |
| **PR-13** — the unread inventory, eleven against twelve | **The renderer no longer depends on the reading set being the whole inventory.** `render_reading_table` unions the plan's undelivered `reading_set` rows with the caller's own `state.unread`, minus whatever opened, so a cell the reading set never named can still be printed unread. That is a mechanism, not a fix: **the inventory is still the bundle's to state correctly**, and the trichotomy clause of the ceiling rests on it being complete. `PREREG.md`'s "eleven" must become twelve, or say which twelfth it excludes and why. W5-DRIVER must be the thing that supplies the complete list. |
| **PR-02 / PR-06 / PR-07 / PR-08** | Unchanged by wave 3; see WAVE2-INTERFACE §10. PR-06's anchor repair is the one wave 3 leans on — `build_calibration_set` takes its ground truth from the repaired `cal-01`, so a bundle that does not carry the referring-region-only construction would charge the panel an error it did not make. |

---

## 8. What W4-READER, W4-MARKER and W5-DRIVER must answer

Carried forward from WAVE2-INTERFACE §11 where still open, and new where wave 3
opened one.

1. **The guard-block streak, settled as a ruling, unimplemented by design.**
   `trial` emits at most one `Block` per trial and carries no state between
   trials, so the counter cannot live here. The definition:
   **per role, over consecutive trials in dispatch order within the reading arm,
   reset by any trial of that role whose outcome is not `blocked`.** Per role
   rather than per run because §2.4's Spawn is `audit-the-reader` — a fault
   attributed to an instrument, and the roles are the instruments; consecutive
   in *dispatch* order rather than cell order because the fault it detects is
   temporal. `decide.Instrument.block_streak` is the declared integer; **W5-DRIVER
   must implement this counter and PREFLIGHT must assert it is this definition.**
2. **Who carries `INDETERMINATE` to a reader.** W3-REPORT now *prints* the list
   and owns the sentence, but it does not *compute* it: `CycleState.indeterminate`
   and `ClosingRun.indeterminate` arrive from the caller.
   `steps.scan_coordinates` returns the frozensets. **W5-DRIVER is the record
   that names a request-or-attempt-without-response**, and must say so.
3. **Who supplies the complete unread inventory** (PR-13). `render_reading_table`
   unions the plan's reading set with `state.unread`; **W4-READER must produce
   `state.unread` as every cell nothing read**, including cells the reading set
   never named, or the trichotomy's completeness is a matter of the bundle's
   prose alone.
4. **Which seat spelling W4-READER writes into `ReadingResult.seat`.** Everything
   in the audit layer hangs on this: `graph.validity_nodes_for_seat`,
   `graph.seats_on_record` and every audit warrant target read the string
   W4-READER stored. `roles.Coordinate.seat_label` (`judge#1`) is the candidate
   with an owner. **W4-READER must declare it, and must fill
   `ReadingResult.roles` with the judging pair**, which is what lets
   `audits.disagreement_series` name a pair without a panel argument.
5. **Does W4-MARKER seal a second baseline for E and G?** Still open, unchanged:
   wave-1 decision 53 says it must, as a *second sealed artifact* and never a
   revision of the program's.
6. **How a pre-registered condition is declared.** Still open, unchanged: the
   clause exists in `decide` and `LoopConfig` has no field for one.
7. **Whether the loop runs from a wheel.** Still open, unchanged;
   `seats.key_gate_for` imports runner v2 from `tools/`. Note that
   `test_trial.py` patches `roles.key_gate_for` for exactly this reason and says
   so at the patch site.
8. **The calibration exemplar bytes** (§6, declined). The bundle reviser must
   decide whether the five constructed exchanges move into the standard body —
   design §2.1 says they belong there — and accept that it moves
   `STANDARD_BODY_SHA256` a fourth time, or record that the calibration set's
   ground-truth bytes are pinned separately as
   `audits.CALIBRATION_EXCHANGES_SHA256` and that the plan must pin that too.
9. **Where the `rendered_files` record is registered.** W3-REPORT builds it;
   nothing registers it yet. `obligations.no_scoring_key` (p4) and p12 read it
   off the graph, so **W5-DRIVER must register the run's map at the end of every
   cycle**, after the renderers have run and before `decide()` reads the
   situation — otherwise p4 evaluates against an absent record, which is not the
   same thing as a satisfied one.
10. **`report`'s `harness` argument is untyped and its `plan` may be a mapping.**
    Both renderers accept a raw plan body carrying `pins`; W5-DRIVER should pass
    a `ReportPlan` so `loop_plan_id`, `reading_set` and `ceiling_text` are all
    in one record and the closing header is not `(plan unpinned)`.
