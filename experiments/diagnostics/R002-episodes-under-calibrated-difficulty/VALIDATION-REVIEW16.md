# R002 review16 validation supplement

**APPROVED-AS-CORRECTED for publication as a draft only.** No provider/model call, .env read, Git mutation or scientific episode. Original W18 VALIDATION.md and MATERIAL_PINS.json remain historical records; this supplement reports the corrected draft. Engineering/live qualification is still required.

## Independent mathematics and candidate reading

Independent computations and six universal proofs were saved before worker oracle execution. All24 sealed results agree; disagreements NOT FOUND; problems replaced0. Pool is mixed, not uniformly easy; exact scheduling/counting/state/interpolation tasks plausibly challenge native32768, while standard proof tasks are easy. No native pilot has measured this. Per-case ambiguity/leakage/difficulty and path:line evidence: work/review16/CANDIDATE-REVIEW.md.

## Oracle suite actual output

```json
{
  "status": "PASS",
  "candidate_count": 24,
  "computable_count": 18,
  "derivation_only_count": 6,
  "long_chain_count": 14
}
```

Full pasted output: work/review16/oracle-check/worker-suite-corrected-transcript.txt. One judge-introduced indentation error failed before computation; original failure transcript and erratum remain. It was not a mathematical disagreement.

## Contract and launcher checks

Twelve Draft2020-12 schemas and seven proposed recipes pass local schema/branch/matched-model checks. Cannot-decide branches, required fork target and fork-forward uptake syntax were exercised. These establish interface shape, not semantic uptake or sandbox containment. CHECKER's added host-execution limits are the intended difference.

```text
test_admission_is_first_eight_incorrect_or_no_answer_in_id_order (__main__.R002LauncherTests.test_admission_is_first_eight_incorrect_or_no_answer_in_id_order) ... ok
test_ceilings_admit_no_answer_without_mislabelling_wrong (__main__.R002LauncherTests.test_ceilings_admit_no_answer_without_mislabelling_wrong) ... ok
test_env_forwarding_does_not_open_file_or_expose_values (__main__.R002LauncherTests.test_env_forwarding_does_not_open_file_or_expose_values) ... ok
test_fewer_than_eight_and_zero_follow_stopping_rule (__main__.R002LauncherTests.test_fewer_than_eight_and_zero_follow_stopping_rule) ... ok
test_live_is_blocked_without_engineering_adapter (__main__.R002LauncherTests.test_live_is_blocked_without_engineering_adapter) ... ok
test_live_receipt_links_all_24_trials_and_sealed_hashes (__main__.R002LauncherTests.test_live_receipt_links_all_24_trials_and_sealed_hashes) ... ok
test_maximum_budget_matches_preregistration (__main__.R002LauncherTests.test_maximum_budget_matches_preregistration) ... ok
test_optional_gates_and_added_budget (__main__.R002LauncherTests.test_optional_gates_and_added_budget) ... ok
test_proposed_contract_artifacts_are_pinned (__main__.R002LauncherTests.test_proposed_contract_artifacts_are_pinned) ... ok
test_resume_accepts_only_exact_complete_custody (__main__.R002LauncherTests.test_resume_accepts_only_exact_complete_custody) ... ok
test_write_once_receipt_refuses_overwrite (__main__.R002LauncherTests.test_write_once_receipt_refuses_overwrite) ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.260s

OK

```

## Actual final-byte offline phase commands and results

Occurrence001 is preserved before final admission validation hardening. Occurrence002 is a separately named final offline fixture with175 source pins; no provider occurrence was retried.

```text
$ C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 C:\Dev\miniReason\experiments\diagnostics\R002-episodes-under-calibrated-difficulty\run_R002.py --mode offline --run-root C:/tr16/r002-review16 --problems C01 --occurrence 2 --env-file C:/tr16/nonexistent-forwarding-fixture.env --phase calibration
{"mode": "offline", "phase": "calibration", "schema": "minireason.r002.launcher.v1", "scientific_evidence": false, "status": "OFFLINE_COMPLETE"}
exit=0

$ C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 C:\Dev\miniReason\experiments\diagnostics\R002-episodes-under-calibrated-difficulty\run_R002.py --mode offline --run-root C:/tr16/r002-review16 --problems C01 --occurrence 2 --env-file C:/tr16/nonexistent-forwarding-fixture.env --phase calibration --resume
{"phase": "calibration", "mode": "offline", "status": "SKIPPED_VERIFIED_COMPLETE", "scientific_evidence": false}
exit=0

$ C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 C:\Dev\miniReason\experiments\diagnostics\R002-episodes-under-calibrated-difficulty\run_R002.py --mode offline --run-root C:/tr16/r002-review16 --problems C01 --occurrence 2 --env-file C:/tr16/nonexistent-forwarding-fixture.env --phase main --admission-receipt C:/tr16/admission-fixture.json
{"mode": "offline", "phase": "main", "schema": "minireason.r002.launcher.v1", "scientific_evidence": false, "status": "OFFLINE_COMPLETE"}
exit=0

$ C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 C:\Dev\miniReason\experiments\diagnostics\R002-episodes-under-calibrated-difficulty\run_R002.py --mode offline --run-root C:/tr16/r002-review16 --problems C01 --occurrence 2 --env-file C:/tr16/nonexistent-forwarding-fixture.env --phase main --admission-receipt C:/tr16/admission-fixture.json --resume
{"phase": "main", "mode": "offline", "status": "SKIPPED_VERIFIED_COMPLETE", "scientific_evidence": false}
exit=0

```

```json
[
  {
    "phase": "calibration",
    "occurrence": 2,
    "source_pins": 175,
    "evidence_pins": 2,
    "conditions": [
      "CAL-NATIVE"
    ],
    "env_file_read": false,
    "result": "PASS"
  },
  {
    "phase": "main",
    "occurrence": 2,
    "source_pins": 175,
    "evidence_pins": 6,
    "conditions": [
      "NATIVE",
      "LOOP-CROSS",
      "LOOP-TESTED",
      "LOOP-RECODED",
      "LOOP-CHECKER"
    ],
    "env_file_read": false,
    "result": "PASS"
  }
]
```

The synthetic env-file path does not exist and was never opened. Forwarding was verified in the prospective argv constructor and by a no-read unit test. Actual live child credential ingestion is NOT RUN. Resume verified exact source/context/evidence equality and skipped both completed fixtures. The admission validator rejects offline records as live evidence and rejects a pilot record with two attempts even if its phase hash matches. Both phases remain scientific_evidence:false.

## Scope of approval

All six binding amendments plus the realistic-budget/optional-arm addendum are in PLAN, INSTRUMENT, recipes, schemas and the episode reading template; CHANGES.md retains each judge round. Current R001 table and failure section are exact in the premise supplement. FW5 claim anchors were opened directly. The original source checkout outside the permitted paths and historical observations are not modified. Publication belongs to a separate publisher; no commit or push is claimed here.
