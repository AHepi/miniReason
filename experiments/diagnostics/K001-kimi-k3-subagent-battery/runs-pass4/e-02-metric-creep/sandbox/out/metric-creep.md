# Metric creep audit — `src/minireason/loop/standard.py` and `src/minireason/loop/types.py`

**Rule enforced.** No count, rate, rank, average, majority, "best" or optimisation
target may enter adjudication, a reading's standing, a rendered artifact, a data file,
a docstring promise or a test oracle. A bound on an instrument or on spend (panel
shape, call budget, wall clock, replicate floor) is allowed. The distinction is what
the number is allowed to decide. Checked against the bytes actually in this sandbox,
not against what these modules usually contain.

**Verdict key.** A — allowed instrument/spend bound. F — forbidden: reaches
adjudication or a reading's standing. C — allowed only under a condition not yet
enforced, with the condition named and the module that would have to enforce it.

## Findings table

| # | File · symbol | What the number is | Verdict |
|---|---------------|--------------------|---------|
| 1 | `standard.py` · `GUARD_PARAMETERS` (`critic_seats=1`, `defender_seats=1`, `judge_seats=2`, `variator_seats=1`, `min_judge_families=2`, `paraphrase_n=2`, `schema_repair_budget=0`, `min_resolved_replicates_per_case=3`) | Panel shape, replicate floor, a refused-repair budget, inside the pinned data file (`STANDARD_BODY` under `guard_parameters.`) | A in itself — these freeze a panel shape and a replicate floor, exactly the allowed category. The one risk is the dual ownership with `types.SeatsConfig`; see row 3. |
| 2 | `standard.py` · `_INT_PARAMS` (admissible ranges, e.g. `judge_seats` 2–8, `min_resolved_replicates_per_case` 3–16, `schema_repair_budget` 0–1) | Bounds on the bounds, enforced by `build_standard`'s `_validate_params` | A. A range check on a successor standard's panel parameters decides nothing about any reading. |
| 3 | `standard.py` · `assert_config_matches_standard` + `types.py` · `SeatsConfig.from_mapping` (`min_judge_families`, `paraphrase_n`, `schema_repair_budget` declared in both owners) | Two owners declare the same guard numbers; reconciliation is docstring-mandated ("**PREFLIGHT must call this** (W5)") but no module in this sandbox calls it | **C.** Condition: the PREFLIGHT step must call `standard.assert_config_matches_standard(config.seats.as_dict(), config.reopen_reasons)` before the first call. Module that must enforce it: the wave-1 PREFLIGHT step (W5) — absent from this sandbox. Probe `probe/probe_preflight_reconciliation.py` printed: no non-docstring call site for `assert_config_matches_standard` anywhere under `src/`; `SeatsConfig.from_mapping({"min_judge_families": 8, "paraphrase_n": 5})` loads without refusal while the standard freezes `min_judge_families=2, paraphrase_n=2`; calling the reconciliation by hand refuses with code `GUARD_PARAMETER_INVALID`. So the numbers respect the pinned standard only if a module not yet present makes the call. |
| 4 | `standard.py` · `WORD_LIMITS` and the `role_contracts.word_limits` section of the built body (`critic.case=400`, `defender.answer=400`, `judge.reading_note=120`, `marker.case=120`) | Prose bounds per seat per field | A. Exceeding one blocks the output with `blocked:schema` and registers nothing; the module's own `word_limits_read` states no two outputs' lengths are ever compared. The number decides whether prose is admitted, never what a reading is. (The oracle drift around these paths is row 10.) |
| 5 | `standard.py` · rubric prose `_MARK_BODY` M7 ("Fewer than three resolved replicates") and `_RELATION_BODY` R10 (judge seats, "Every judge seat") | A replicate floor (3) stated in prose; unanimity over an unnamed number of seats | A. A replicate floor is explicitly in the allowed category; M7 uses it to *withhold* a mark (unresolved), never to award one. The unanimity rule deliberately names no numeral, so no count does warrant work. |
| 6 | `standard.py` · `CEILING_REQUIRED_SENTENCES` clause 7 + `types.py` · `BLOCK_CODES` / `CEILING_BLOCK_REASONS` | Block registers "printed with counts on every table" — counts reach rendered artifacts | A. The same clause states "A high block rate is the instrument declining to read. It is never an absence of relations"; the count is information printed beside its own denial of warrant, which the rule and FW5:851 both permit. The test `TheCeilingAndTheBlockCodeTableAgree` pins the nine names against the ceiling bytes in both directions. |
| 7 | `types.py` · `AuditConfig.judge_err_max` (a rate, `0.0–1.0`) | A calibration error **rate** that names `instrument_fault` and stops the reading arm | **C.** A rate is in the forbidden vocabulary unless it stays a panel-level instrument signal that adjudicates no content. The docstring states the conditions: never computed per seat, never compared across seats, never a merit predicate; `instrument_fault` names the instrument. **But the conditions are prose-only in this sandbox.** Probe `probe/probe_audit_thresholds.py` printed: `judge_err_max`, `streak_max` and `instrument_fault` occur only in `types.py` (declaration, validation, docstrings); no module computes the rate, consumes the threshold, or stops an arm — the AUDIT/DECIDE wave is not present. Condition: the consumer (the wave implementing design §2.5/§5 clause 6: AUDIT and `decide()`) must compute the rate over the panel, never per seat, and must route it only to `instrument_fault`, never to any reading's standing. Module that must enforce it: that future AUDIT/DECIDE module; nothing here can. |
| 8 | `types.py` · `AuditConfig.streak_max` (whole 1–9999) and `AuditConfig.period` (whole 1–99) | A guard-block streak threshold; an audit cadence | **C**, same shape as row 7 (for `streak_max`): a count that may only fire `instrument_fault`. `period` is a plain cadence bound, A. Both are required-with-account, pre-registered, and folded into `loop_plan_id`, which is the right custody; the not-yet-enforced condition is in the absent consumer, as probed above. |
| 9 | `types.py` · `LoopConfig.cycle_budget` (1–99), `max_calls` (0–1_000_000), `max_per_key` (1–5), `TimeoutsConfig` (`step_seconds`, `git_seconds=90`), `STOP_REASONS` (`resource_boundary`), `assert_no_exhaustion_claim` in `standard.py` | Spend bounds and wall clocks, and the stop token that records one was reached | A. These are the paradigm allowed category. The exhaustion scan (`probe` of the shipped text passed: the test `TheExhaustionScanExemptsTheCeilingsOwnDenial` holds against the shipped bytes — the single `exhaustion` occurrence is the ceiling's own denial). |
| 10 | Test oracle · `docs/examples/test_standard_example.py` · `HouseRules.test_every_integer_in_the_body_is_a_declared_guard_parameter` | The oracle that is supposed to keep stray numbers out of the data file | **C.** The shipped body contradicts the shipped oracle: probe `probe/probe_integer_oracle.py` printed 12 integers in `STANDARD_BODY`, of which the four under `role_contracts.word_limits.*` fail the oracle's `startswith("guard_parameters.")` assertion. `python3 run_tests.py docs.examples.test_standard_example` confirms: those four subtests FAIL (three further ERRORs in this suite are sandbox absences — `experiments/diagnostics/C001-contrast-triple/PLAN.md` and `material.json` are not copied here — and are not drift). The module docstring (deviation 6, `_role_contracts_section`) documents the new integer home and calls the old exactness "worth more than… legible twice", i.e. the code changed and the oracle did not. The word-limit integers themselves are allowed (row 4), so this is not an F in the code; it is a C on the oracle: condition — wave-0 (the owner module of the standard, W0-STANDARD) must reconcile oracle and body, either moving the assertion to `guard_parameters. | role_contracts.word_limits.` or moving the integers, because an oracle left permanently red stops enforcing the rule it guards. |

## Was anything forbidden found?

**No.** No count, rate, rank, average, majority or "best" in these two modules reaches
adjudication, a reading's standing, or a rendered artifact as a warrant. The register
marks are never summed anywhere in these files; the unanimity rule ships no numeral;
the one rate (`judge_err_max`) and the one streak count (`streak_max`) have no consumer
in this sandbox at all, so as shipped they can decide nothing — which is why they are C
rather than F, with the consuming AUDIT/DECIDE wave named as the module that must keep
the docstring's promise.

## The live risk

The live risks are exactly the C rows:

- **Row 7 / row 8** are where a forbidden rate could be born: the first module that
  computes `errors / anchors` per seat, or reads `streak_max` as anything but
  `instrument_fault`, turns an allowed alarm into adjudication. Today there is no code
  to accuse; there is only a docstring to keep.
- **Row 3** is the quieter one: the panel-shape numbers are allowed, but their two
  owners (`SeatsConfig`, `GUARD_PARAMETERS`) are reconciled only by a call nobody in
  this sandbox makes, so a config can currently declare a different panel than the
  pinned standard with no refusal anywhere.
- **Row 10** is the enforcer's own health: the wave-0 oracle currently fails on the
  shipped body (probes `probe/probe_integer_oracle.py` and the run above), and a
  permanently red oracle is the creep vector the task names — an oracle that cannot
  pass is, in effect, an oracle that cannot fail informatively.

## Probes

- `probe/probe_audit_thresholds.py` — lexical reach of `judge_err_max` / `streak_max` /
  `instrument_fault` across the sandbox; printed: occurrences only in `types.py`.
- `probe/probe_integer_oracle.py` — walks `STANDARD_BODY`; printed: 12 integers, four
  under `role_contracts.word_limits.*` failing the oracle's `guard_parameters.` prefix.
- `probe/probe_preflight_reconciliation.py` — grep for callers of
  `assert_config_matches_standard` (printed: docstring mentions only) plus a live load
  of a contradicting `SeatsConfig` (accepted) and a manual reconciliation call
  (refused with `GUARD_PARAMETER_INVALID`, proving the guard works when called).

Oracle run: `python3 run_tests.py docs.examples.test_standard_example` — 4 subtests
FAIL (row 10's drift), 3 ERRORs from sandbox-absent C001 data files, all other tests
pass, exit code 1.
