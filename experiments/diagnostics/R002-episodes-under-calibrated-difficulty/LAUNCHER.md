# R002 launcher contract after judge corrections

DRAFT; no calibration/main participant call has run. `run_R002.py` always refuses live dispatch. Offline files are structural scheduling/custody fixtures, not model answers, engine qualification or scientific episodes. R001's shipped engine is not relabeled as the amended R002 instrument.

## Commands tested in review16

From C:/Dev/miniReason, using the specified Python 3.11 interpreter, PYTHONPATH=src;tests, PYTHONUTF8=1, PYTHONIOENCODING=utf-8 and TMP=C:/tr16:

```powershell
$python='C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe'
$launcher='experiments/diagnostics/R002-episodes-under-calibrated-difficulty/run_R002.py'
& $python -B -X utf8 $launcher --phase calibration --mode offline --run-root C:/tr16/r002-review16 --problems C01 --env-file C:/tr16/nonexistent-forwarding-fixture.env
& $python -B -X utf8 $launcher --phase calibration --mode offline --run-root C:/tr16/r002-review16 --problems C01 --env-file C:/tr16/nonexistent-forwarding-fixture.env --resume
& $python -B -X utf8 $launcher --phase main --mode offline --run-root C:/tr16/r002-review16 --admission-receipt C:/tr16/admission-fixture.json --problems C01 --env-file C:/tr16/nonexistent-forwarding-fixture.env
& $python -B -X utf8 $launcher --phase main --mode offline --run-root C:/tr16/r002-review16 --admission-receipt C:/tr16/admission-fixture.json --problems C01 --env-file C:/tr16/nonexistent-forwarding-fixture.env --resume
```

The env-file path is deliberately nonexistent. The launcher records a prospective child argv with the exact opaque `--env-file` argument and **never opens the file**. An offline test patches `Path.open` to fail if the argv builder attempts a read. Actual live credential ingestion is unimplemented/unqualified and NOT RUN. No value is printed or stored. The forwarding interface is for a later reviewed child adapter; it cannot unlock live mode. Credential values must be read by that child only at call time. All offline subprocess environments strip provider-key names without displaying values.

Each phase writes a write-once `phase-receipt.json`, per-condition fixtures and `manifest.json`. The manifest pins executable inputs, candidate/public/answer/oracle/recipe/schema hashes, admission and optional-receipt hashes, and every produced evidence file. `--resume` skips only a completed occurrence with exact context, source and evidence equality. A partial directory, added/missing/changed evidence or source drift refuses without replay. A new separately receipted occurrence is required to address a real incomplete/failed run; no retry is inferred from the flag. Output must be a subdirectory of work/w18, work/review16 or C:/tr16; these review commands use only C:/tr16.

## Calibration and admission

Future calibration: C01-C24 exactly once each, NATIVE DeepSeek Flash, requested native/medium, 32768 completion, 300-second outer wall, zero repairs/fallbacks/retries. The one-problem offline test is not permission for a partial live pilot. Every pilot call and no-answer is retained, never reused as a main input.

Admission receipt schema `minireason.r002.admission-reader.v1` covers all 24 live trials, exact calibration-manifest links, problem/answer/oracle hashes, reader identity/UTC, public answer path/hash or absence, verdict, no-answer cause and operational status. `incorrect` and `no_answer` alone are eligible. **CEILING_HIT with no final answer means "not answered" / no_answer and is admitted**; it is not an oracle-wrong answer. Take the first eight eligible IDs; use all one through seven if underfilled; zero stops main. Unresolved interpretations do not admit. Offline synthetic receipts must say `evidence_kind: offline-test-fixture`; they have no evidential standing.

## Default and optional main selection

Default: fresh NATIVE, amended LOOP-CROSS, LOOP-TESTED, LOOP-RECODED, and LOOP-CHECKER when computable. The four loop recipes share at most 14 calls and strict attempts; off ceiling 16384, native 32768, input 32768, wall 300 seconds. No-new/no-open stopping and the cycle-3 stall replacement follow PLAN section 3. No shipped legacy command substitutes for r002-cross-v2.

LOOP-CROSS-MATCH, LOOP-CARRIER and NATIVE-MATCH are optional. Each is enabled only by its own `--optional-receipt PATH`, whose JSON contains `schema: minireason.r002.optional-arm-receipt.v1`, one `condition`, `decision_receipt`, `reason`, `occurrence_id`, ordered `candidate_ids` equal to the admitted set, `max_calls_per_case:14`, and `completion_tokens_per_case:311296`. No receipt means no companion. Future live publication/authorization verification belongs to the reviewed adapter; a fabricated receipt does not authorize provider calls.

Default combined hard envelope is 24+43a+14c calls/attempts and 786432+966656a+311296c completion tokens; at a=c=8: 480 / 11010048. Every optional case adds 14 attempts / 311296 completion. PLAN section 6 states the realistic R001-derived forecast separately. `budget()` and focused tests recompute both default and all-optional maxima.

## Prospective engineering CLI

The pure `prospective_child_argv()` function constructs concrete argument vectors without executing them. Native uses `tools/reason.py run-r002-native` with condition CAL-NATIVE or NATIVE, the original problem, answer schema, native/medium/32768, strict attempts, tokenizer pins, relations and capability. Loop arms use `tools/reason.py run-r002` with the exact selected recipe path, three-cycle maximum, strict attempts, tokenizer pins, relations, public fork registry, coding manifest and capability; CHECKER adds CHECKER_POLICY.json. Both routes add `--retry-transport 0 --mode live --out PATH` and the opaque env-file argument if supplied. These commands currently fail: the CLI adapter and v2 capability do not exist.

Capability `r002-contracts-v2` must pin every recipe/schema basename/hash and advertise `prompt_contract:r002-episodes-v2`, strict attempts, maximum_cycles:3, no_new_objections_stop:true, stall_switch:true, off_completion_tokens:16384, unconditional_closing_return:true, prompt_token_cap:32768, reviewed identity and a qualified checker backend when selected. Capability presence alone never unlocks this staged launcher. Engineering must implement/qualify the actual prompt, fork, switch, deterministic sandbox and outer wall behavior before any live receipt.

## Evidence

Original W18 offline transcripts remain unchanged under work/w18. Current judge transcripts, unit checks, manifests and hashes are copied under work/review16/launcher and summarized in VALIDATION-REVIEW16.md. No provider/model calls, hidden reasoning, credential read, git change, completed scientific occurrence or episode is represented by these fixtures.
