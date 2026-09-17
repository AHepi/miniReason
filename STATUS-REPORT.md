# Status report for workmates

## What this project is

miniReason tests FW5 explanatory construction against bare/native reasoning ([purpose](PURPOSE.md)). Standard: substantive reasoning improvement through error correction; explain failures.

## Findings paper

[Human-readable findings paper](docs/reports/findings-2026-09.md), published (REC-20260917-C). Abstract:

> We asked whether an explicit loop of conjecture, criticism, return and use could improve reasoning beyond a model answering directly with native thinking. The instrument was a personal prose reasoning CLI, exercised on checkable problems and then open inquiries. Completed native answers on the checkable comparisons contained no wrong required answers for criticism to repair. Harder cases exposed a shared initial generation bottleneck, with a repeated solving exception. Decomposition produced inspectable steps but no full synthesis. Critical episodes contained explanation and arithmetic repairs alongside withdrawn objections, invented errors and attacks on changed premises. Open inquiries produced concrete proposals and a potentially harmful restriction, without establishing propagated repair beyond native reasoning. Delivery contracts repeatedly prevented the intended comparisons. FW5 helped distinguish criticism, use and repair, while leaving substantial application evidence unspecified. These records identify mechanisms and failures worth investigating; they do not establish the requested reasoning advantage or exhaust the inquiry.

## deepseek-flash pilot plugin

[Feasibility](research/deepseek-flash-pilot/FEASIBILITY.md): **POSSIBLE WITH PROBED FEATURES**; [probes](research/deepseek-flash-pilot/PROBE-RESULTS.md): **12/12**. The published plugin routes, spawns, assembles, verifies and decides continuation; no model filesystem/shell powers.

[Amendments](research/deepseek-flash-pilot/AMENDMENTS.md): P-A1 self-continuation, 300 logical calls, USD 6 estimated-spend guard, up to 24 branches, three levels deep; P-A2 content-addressed inputs and scoped source reads from MIT-licensed AHepi/DeepReason `9607fba6`; P-A3 repaired input/quote delivery; P-A4 added output handling and three recorded repairs; P-A5 added exact reference menus and partial carry-forward. Earlier failed attempts remain preserved.

[Four-attempt reading](research/deepseek-flash-pilot/REPORT-usecases.md): attempts 1-3 stopped on host checks at calls 2-10. Attempt 4:

|Task|Passes|Logical calls|Decisions|Usability|
|---|---|---|---|---|
|Blender blocking|4|13 reserved; 12 dispatched|CONTINUE x3; host input-window stop|Useful shot specification; defective script|
|Hard-to-vary story parts|1|4|STOP|Usable; overstrong separation claim|
|Reading user intent|1|4|STOP|Partly usable; unsupported alternatives/missing planning implication|
|FW5 adversarial mapping|3|12|CONTINUE x2, STOP|Preliminary mapping; stopping premise disputed|

The reader finds real decisions after verification, but no full Astra replacement. The host overrode every first route; successful nested work remains unproved. No later pass repaired a final artifact; none finished COMPLETE.

[Run instructions](research/deepseek-flash-pilot/README.md): `python -m minireason.pilot run --task TASK.json --mode live --out NEW_DIRECTORY`.

## What exists and works today

[CLI/evidence](docs/workflows/reason-cli.md); [L003 closed](experiments/loops/L003-loop-first-live-2026-09-14/CLOSING.md); [append-only records](docs/workflows/continue.md).

## Latest result: R001

The [published R001 report](experiments/diagnostics/R001-reason-cli-vs-baselines/REPORT.md) answers the owner's question directly:

> No: this occurrence does not show the loop producing a completed correct answer where completed native thinking was wrong through a visible criticism-return-use route. Native thinking already answers P01-P07 correctly, and the P08 native call hits its completion ceiling without a public answer; both loop initial conjectures already have the correct answers on all eight. There is a real explanation repair in P08-SINGLE and a local use-seat correction from38 to41 in an archived, later-failed P02-SINGLE run, but neither establishes the owner's requested advantage over NATIVE.

|Problem|BARE|NATIVE|LOOP-CROSS|LOOP-SINGLE|
|---|---|---|---|---|
|[P01](experiments/diagnostics/R001-reason-cli-vs-baselines/readings/P01.md)|incorrect|correct|correct|correct|
|[P02](experiments/diagnostics/R001-reason-cli-vs-baselines/readings/P02.md)|incorrect|correct|correct|correct|
|[P03](experiments/diagnostics/R001-reason-cli-vs-baselines/readings/P03.md)|incorrect|correct|correct|correct|
|[P04](experiments/diagnostics/R001-reason-cli-vs-baselines/readings/P04.md)|correct|correct|correct|correct|
|[P05](experiments/diagnostics/R001-reason-cli-vs-baselines/readings/P05.md)|incorrect|correct|correct|correct|
|[P06](experiments/diagnostics/R001-reason-cli-vs-baselines/readings/P06.md)|correct|correct|correct|correct|
|[P07](experiments/diagnostics/R001-reason-cli-vs-baselines/readings/P07.md)|incorrect|correct|correct|correct|
|[P08](experiments/diagnostics/R001-reason-cli-vs-baselines/readings/P08.md)|undecidable|undecidable|correct|correct|

Legend: BARE is a direct answer without native thinking; NATIVE enables it; LOOP-CROSS uses critics from different model families; LOOP-SINGLE uses one family. Correct/incorrect concern the requested answer facts; undecidable means the baseline stopped at its output limit without a complete answer. P07 BARE retains a contradictory claim despite its correct recap.

Three local episodes remain informative:

- **P08-SINGLE:** criticism repaired the scheduling explanation by showing why starting each job as early as possible cannot worsen a fixed order, while the already-correct answer stayed 253.
- **Archived P02-SINGLE:** a use check corrected 38 to 41 after a critic had proposed 38, but native thinking already gave 41 and the run later failed its response contract.
- **P04-CROSS:** a critic challenged an earlier criticism for changing the problem's premises, and the return retained the correct SQL answer.

Operationally, twelve raw objections across eight attempts withdrew themselves or concluded there was no error; repaired responses delivered empty lists. Nine GLM critic turns were unavailable because they hit 8,192 output tokens, not because of transport or response-format failures. Most use checks confirmed narrow consequences instead of independently solving the whole problem; P08-CROSS repeatedly failed its own changed-release-time check ([reading summary](experiments/diagnostics/R001-reason-cli-vs-baselines/readings/SUMMARY.md)).

The report's main reason is that native thinking already solved every completed comparison, and the loops started correct. P08's missing native answer limits the conclusion; it is not evidence of a native mistake. Different call allowances and roles also prevent attributing trace differences to model family alone.

## R002 calibration result

[Admission](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/ADMISSION.md): twenty of twenty-four native answers correct; four exhausted without answering. C05/C06/C09/C12 admitted; none wrong. All computable.

[Domains](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/CANDIDATES.md):

|Candidate|Domain|Verdict|
|---|---|---|
|[C01](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C01.md)|Selected-evidence Bayesian chain|correct|
|[C02](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C02.md)|Balanced proper bracelets|correct|
|[C03](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C03.md)|Synchronous register machine|correct|
|[C04](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C04.md)|Outer-join aggregate ledger|correct|
|[C05](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C05.md)|Release/setup weighted schedule|not answered|
|[C06](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C06.md)|Constrained monotone grid paths|not answered|
|[C07](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C07.md)|Exact stopping time in a Markov chain|correct|
|[C08](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C08.md)|Spanning trees with a required edge|correct|
|[C09](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C09.md)|Weighted finite transducer|not answered|
|[C10](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C10.md)|Composite-modulus affine observations|correct|
|[C11](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C11.md)|Precedence-constrained slot assignment|correct|
|[C12](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C12.md)|Adaptive urn after six draws|not answered|
|[C13](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C13.md)|Cyclic constrained multiset words|correct|
|[C14](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C14.md)|Prime-index floored recurrence|correct|
|[C15](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C15.md)|Parity-state shortest route|correct|
|[C16](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C16.md)|Poison-total minimax game|correct|
|[C17](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C17.md)|Degree-nine interpolation|correct|
|[C18](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C18.md)|Preemptive queue boundary order|correct|
|[C19](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C19.md)|Telescoping rational identity|correct|
|[C20](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C20.md)|Rank-one determinant identity without invertibility|correct|
|[C21](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C21.md)|Parameterized recurrence identity|correct|
|[C22](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C22.md)|Finite-difference polynomial characterization|correct|
|[C23](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C23.md)|Alternating binomial reciprocal identity|correct|
|[C24](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/C24.md)|Matrix-polynomial reduction|correct|

## R002 result

[Published report](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/REPORT.md):

> On this calibrated set, no loop produced a correct answer through a visible critical episode where fresh native thinking produced none: C09 CROSS, TESTED and CHECKER retained correct answers, but those answers were already present in their independent native initial calls, before criticism. The attempted improvement failed mainly at access to a public target, critic delivery, and getting from accepted steps to the decisive calculation and synthesis; no objection-driven changed relation reached a later use. Calibration established 20 correct answers in 24 fixed native trials and 4 ceiling stops with no answer, never a wrong native answer; all 4 were admitted. The finite, selected-on-pilot-failure pool and one new occurrence per condition cannot establish general superiority, model standing, historical novelty, a pretraining repertoire, general creativity, all protected-use repair, full reason-use causal identification, recursive capacity or an infallible checker. Positive findings are scoped episodes and bounded task outcomes under explicitly unequal baseline/legacy conditions and matched common envelopes, with conditional switches read separately. Negative cases, false objections, legitimate rejections, missing answers and operational failure remain part of the record. The evidence points to a separately registered plan contract that puts the decisive computation and all outputs inside its declared step budget, with an explicit route for challenging accepted dependencies; a larger budget or tools would be declared resource/information changes and need matched controls.

| Problem | NATIVE | CROSS | TESTED | RECODED | CHECKER | DECOMPOSED 001 |
|---|---|---|---|---|---|---|
| C05 | not answered | not answered | not answered | not answered | not answered | not answered (1 step) |
| C06 | not answered | not answered | not answered | not answered | not answered | not answered (1 step) |
| C09 | not answered | correct | correct | not answered | correct | not answered (1 step) |
| C12 | not answered | not answered | not answered | not answered | not answered | not answered (1 step) |

Legend: not answered = no complete answer; C09 correct initials preceded criticism. [A2](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/DECOMPOSED-A2.md) added JSON enforcement, one recorded repair and Qwen criticism; three accepted steps on C05/C06/C09, one on C12, no synthesis or decomposition escape.

[A1](experiments/diagnostics/R002-episodes-under-calibrated-difficulty/PLAN.md): conservative byte preflight (measured tokens/byte 0.235968765-0.266547406; non-DeepSeek reserve 2,048 tokens); decomposition exposed steps despite exhaustion. Escape required correct full synthesis.

## R003: open problems, trial-and-error

[Occurrence 3](experiments/diagnostics/R003-open-problems-trial-series/reports/o003-REPORT.md): CROSS use survived, 9/11 calls. Retained NATIVE/CROSS answered 7/8; DECOMPOSED synthesised 1/8. O04 repaired a loop-introduced omission; no improvement over native thinking found.

[Open problems](experiments/diagnostics/R003-open-problems-trial-series/PLAN.md) followed native's never-wrong completed checkable answers:

- O01: criticism/repeated solving.
- O02: unclear-problem language.
- O03: construction/library reuse.
- O04: workshop allocation.
- O05: microbial recovery.
- O06: conflicting curriculum purposes.
- O07: FW5 narrowing, reason-use.
- O08: FW5 narrowing, combined objections.

Published instruments; sealed withheld briefs, manifest `e63a8ec9555dcaeac6255b2be400e03b11e1627433ad8b2c5f3f053bd2030caf`; NATIVE/CROSS/DECOMPOSED.

[FW5 lenses](experiments/diagnostics/R003-open-problems-trial-series/FW5-DERIVED-PROPERTIES.md): EC03 withdrawn-premise reuse; EC04 failed arguments/opposites; EC08 episodes; EC09 protected successes; EC12 outcome-independent conditions. [Earlier readings](experiments/diagnostics/R003-open-problems-trial-series/reports/o001-o002-REPORT.md) remain.

## What comes next

[R3-A3/EC01](experiments/diagnostics/R003-open-problems-trial-series/PLAN.md): returned/archived objections from identical parents. Owner update: occurrence 4 ran all eight problems; its reading is NOT yet done and is on hold by the owner's decision.

[Pilot proposal](research/deepseek-flash-pilot/REPORT-usecases.md): host-validated executable repair actions; no successor launched.

## What was learned this week

[Lessons](docs/lessons/harness-lessons-2026-09.md): 53 plus three live-round entries, published standing pre-build reading.

[Receipts](docs/DECISION_LEDGER.md): REC-20260915-A/B/C; REC-20260916-A/B/C/D/E/F; REC-20260917-A R002, B R003, C paper, D pilot/live `7fffb64e`, F lessons `2ef26b2d`.

## What is blocked or awaiting the owner

Owner update: unpublished `research/provider-fallback` survey awaits choice; OpenRouter prepaid needs transport changes and offers Kimi K2.5/GLM 4.7, not K3/5.3.

[F003](experiments/diagnostics/F003-operative-return/PLAN.md)/[L004](docs/design/loop-prereg-draft-2026-09-14/v6/REVIEW-PREREG.md): registration; [Forge](research/open_language_2026_09/VALIDATION.md): durability; [C001](docs/STATUS.md): reading-delegation; [long paths](docs/design/loop-prereg-draft-2026-09-14/v6/CHANGES-PREREG.md): qualification.

## How to read the repository

[README](README.md)/[PURPOSE](PURPOSE.md), then [STATUS](docs/STATUS.md)/[ledger](docs/DECISION_LEDGER.md). Refresh after results.

## Honesty notes

Claims remain challengeable; [matched controls](experiments/diagnostics/R001-reason-cli-vs-baselines/PLAN.md#comparison-limits-fixed-before-results) remain necessary.

Updated 2026-09-17 UTC, branch status/2026-09-17, based on commit 7bf2ef67e7f37d3f3efd88865f7f0d467d758dcd.
