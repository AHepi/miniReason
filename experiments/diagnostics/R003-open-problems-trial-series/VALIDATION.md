# R003 offline validation - DRAFT, staged and not run

No provider/model call, .env content read, git mutation or src edit occurred. Exact Python3.11 path, PYTHONPATH=src;tests, UTF-8 mode, no bytecode and TMP=C:/tw25 were used. Validation originals and script are under work/w25; source/recipe identities are frozen in each matrix manifest.

## Actual result

18 checks passed. One O01 matrix contains NATIVE/CROSS/DECOMPOSED. The target commands were actually invoked only in offline mode; all three refused before creating a run/provider intent. This is expected incompatibility evidence, not a successful test of R003's requested semantic conditions:

- O01-d: exit2, stderr `CONFIG_ERROR`; no run directory created.
- O01-n: exit2, stderr `SCHEMA_FAILURE: relations.schema.json:candidates: [{'candidate_id': 'O01', 'relations': [{'relation_id': 'working_position', 'type': 'string', 'description': "The answer's present substantive position, including an explicit inability to settle it."}]}, {'candidate_id': 'O02', 'relations': [{'relation_id': 'working_position', 'type': 'string', 'description': "The answer's present substantive position, including an explicit inability to settle it."}]}, {'candidate_id': 'O03', 'relations': [{'relation_id': 'working_position', 'type': 'string', 'description': "The answer's present substantive position, including an explicit inability to settle it."}]}, {'candidate_id': 'O04', 'relations': [{'relation_id': 'working_position', 'type': 'string', 'description': "The answer's present substantive position, including an explicit inability to settle it."}]}, {'candidate_id': 'O05', 'relations': [{'relation_id': 'working_position', 'type': 'string', 'description': "The answer's present substantive position, including an explicit inability to settle it."}]}, {'candidate_id': 'O06', 'relations': [{'relation_id': 'working_position', 'type': 'string', 'description': "The answer's present substantive position, including an explicit inability to settle it."}]}] is too short`; no run directory created.
- O01-x: exit2, stderr `CONFIG_ERROR`; no run directory created.

The installed relation contract rejects the native O-ID/six-entry registry, and exact recipe pins reject both target recipe derivatives. No dummy C IDs, invented oracle, contract mutation or source patch was used to bypass those guards. See PLAN, Instrument changes required.

The actual published legacy prose CLI smoke on the exact O01 file completed three cycles and13 fixture logical calls, exit0, cycle_budget. Its recipe has conditional closing_return enabled, but this fixture required no extra closing call. It is not NATIVE, CROSS+A2 or DECOMPOSED+closing qualification and supplies no reasoning-performance observation. The legacy smoke omits --env-file because legacy run would load it even offline. The strict R002 offline argv contains the literal --env-file .env but defers env loading until a live call boundary, which was never reached.

Resume made no new subprocess and preserved every existing occurrence byte. Known failed cells were selected into a separate plan-only o003, retaining their parent and reason. A synthetic interrupted-intent fixture in o004 refused resend. Source-drift denial was tested through an injected digest mismatch without mutating any source or occurrence. Missing O07, duplicates and live mode were refused. O02 bytes equal the source exactly. These are bounded lifecycle tests, not exhaustive concurrency/security qualification. The launcher serializes its own runs and uses a stale-lock refusal after interruption.

## Exact paste

Command executed: the specified Python with -B -X utf8 work/w25/validate_launcher.py. Its script calls the launcher API and actual tools/reason.py subprocesses; exact argv/stdout/stderr are in the numbered immutable result records and smoke-receipt.json.

```text
PASS one-problem matrix has all three conditions
PASS plan executes no process
PASS live held before dispatch
PASS reserved O07 cannot run without owner input
PASS duplicate cells refused
O01-n: OFFLINE_REFUSED_OR_FAILED rc=2
O01-x: OFFLINE_REFUSED_OR_FAILED rc=2
O01-d: OFFLINE_REFUSED_OR_FAILED rc=2
PASS real target CLI detects all three installed-instrument refusals
PASS NATIVE refused before run/provider intent
PASS LOOP-CROSS refused before run/provider intent
PASS LOOP-DECOMPOSED refused before run/provider intent
PASS resume preserves every occurrence byte and makes no new subprocess
PASS rerun-failed creates next numbered occurrence and keeps parent
PASS failed predecessor unchanged after successor stage
PASS source drift refuses resume without file mutation
PASS indeterminate intent is never resent
PASS all target offline commands declare env-file without loading it
Run directory: C:\Dev\miniReason\work\w25\smoke
{"run_id": "20260917T032310Z-04bf836ad4-a27700", "stop_reason": "cycle_budget", "completed_cycles": 3, "calls": 13}
PASS actual published prose CLI O01 offline smoke returns 0
PASS smoke has saved final answer and state
PASS O02 exact verbatim bytes
ALL 18 CHECKS PASSED; target R003 live readiness: BLOCKED; provider calls: 0
```

## Staged handoff and limits

work/w25/series/o001 is the full six-problem/three-condition plan,18 intended CLI runs, no dispatch. Each question, command and source/input hash is frozen before any run. The live hold cannot be lifted by supplying an arbitrary manifest. Briefs remain unwritten for the later Astra worker; PENDING hashes are null, never fabricated. Future engine admission, repair/closure support, exact input-bound/capability qualification and reviewed seal enforcement remain necessary before a separate live authorization.

A draft syntax check caught a path-string quoting error before execution; a later document-writer stdin quoting error also occurred before any writes. Both were corrected before this validation/handoff and have dated receipts under work/w25. Historical source/instrument observations were never modified. A static UTF-8/JSON/link/resource/scope check follows in work/w25/FINAL-AUDIT.json; it cannot establish semantic correctness or provider behavior.


## Independent review supplement — 2026-09-17T03:56:02.398408+00:00

The preceding validation is retained as historical evidence of the original six-problem draft. Its missing-O07 check and work/w25 manifests are not current inputs. No original observation was rewritten. Corrected draft uses eight inputs, TMP C:/tr25 and work/review25.

16/16 new lifecycle/custody checks pass (work/review25/offline/SUMMARY.json and TESTS.md). The actual one-problem target commands still refuse unsupported instruments: NATIVE SCHEMA_FAILURE, CROSS/DECOMPOSED CONFIG_ERROR, all before child run/provider intent. Separately the actual legacy fixture completes3cycles/13calls/exit0; it does not qualify R003 conditions. Root independently matched98source hashes, copied inputs, all three result records and the full smoke evidence tree (work/review25/ROOT-OFFLINE-VERIFICATION.json). Provider/model calls0; .env not read; no Git mutation. Independent network-isolation enforcement was NOT TESTED; the commands were offline.

O02 exact bytes, FW5 source SHA and verbatim O07 L601/O08 L626-L634 quotations verified. All public registries have eight unique problems; five adopted lenses and verbatim null fallback present; JSON/UTF-8 and budget arithmetic checks pass (work/review25/STATIC-CHECKS.json).

### New actual command/output paste

```text
R003 REVIEW25 OFFLINE COMMAND PASTE
UTC 2026-09-17

Environment and mandated Python:
$env:PYTHONPATH='src;tests'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:GIT_OPTIONAL_LOCKS='0'
$env:TMP='C:/tr25'
$py='C:/Users/darre/AppData/Local/Programs/Python/Python311/python.exe'
$r003='experiments/diagnostics/R003-open-problems-trial-series/run_R003.py'

Actual target command:
& $py -B -X utf8 $r003 new --series work/review25/offline/series --mode offline --problems O01 --question 'On O01, do the installed guards truthfully refuse the unsupported target conditions?'

Actual target output:
O01-n: OFFLINE_REFUSED_OR_FAILED rc=2
O01-x: OFFLINE_REFUSED_OR_FAILED rc=2
O01-d: OFFLINE_REFUSED_OR_FAILED rc=2
{"occurrence": "C:\\Dev\\miniReason\\work\\review25\\offline\\series\\o001", "result": {"status": "OFFLINE_FINISHED", "rows": 3, "failed": 3}}

Per-cell refusal details:
O01-n: SCHEMA_FAILURE: relations.schema.json:candidates ... is too short
O01-x: CONFIG_ERROR
O01-d: CONFIG_ERROR
All three immutable result records: provider_calls=0, status=OFFLINE_REFUSED_OR_FAILED, returncode=2.

Actual published legacy smoke command:
& $py -B -X utf8 $r003 smoke --out work/review25/offline/smoke

Actual smoke output:
Run directory: C:\Dev\miniReason\work\review25\offline\smoke
{"run_id": "20260917T035042Z-04bf836ad4-f8f814", "stop_reason": "cycle_budget", "completed_cycles": 3, "calls": 13}
Process exit: 0

Actual lifecycle and custody verifier command:
& $py -B -X utf8 work/review25/offline/verify_offline.py

Actual verifier output:
PASS source snapshot matches occurrence before lifecycle tests
PASS resume returns terminal failed summary without replay
PASS resume skip terminal preserves every occurrence byte
PASS rerun-failed creates separate o002 plan occurrence
PASS rerun-failed preserves parent and selects three failed cells
PASS failed predecessor remains byte-identical after successor
PASS occurrence numbering is sequential and never overwrites
PASS source hash mismatch is rejected
PASS input hash mismatch is rejected
PASS saved output hash mismatch is rejected
PASS indeterminate intent refuses resend before subprocess
PASS live hard hold refuses before occurrence creation
PASS all target commands name env file only through --env-file
PASS legacy smoke proves published three-cycle prose fixture
PASS actual target run records three expected refusals and zero providers
PASS instrument sources stayed unchanged throughout verification
{"checks_passed": 16, "checks_total": 16, "provider_calls": 0, "source_edits_detected": false}
Process exit: 0

Resume subprocess captured by verifier:
& $py -B -X utf8 $r003 resume --occurrence C:/Dev/miniReason/work/review25/offline/series/o001
{"occurrence": "C:\\Dev\\miniReason\\work\\review25\\offline\\series\\o001", "result": {"status": "OFFLINE_FINISHED", "rows": 3, "failed": 3}}
Process exit: 2

Rerun-failed subprocess captured by verifier:
& $py -B -X utf8 $r003 rerun-failed --occurrence C:/Dev/miniReason/work/review25/offline/series/o001 --mode plan --question 'Which installed instrument defect would this successor address?' --reason 'Stage a separate successor for known refused cells; no retry is dispatched.'
{"occurrence": "C:\\Dev\\miniReason\\work\\review25\\offline\\series\\o002", "result": {"status": "STAGED_NOT_RUN", "rows": 3}}
Process exit: 0

No provider/model call was made. No .env content was read. No real network/prohibited command was used to test a guard.
```

Current verdict is draft-publication approval only, subject to REPORT.md in work/review25. ENGINEERING-SPEC.md names absent support; briefs and valid seals remain NOT FOUND. No participant occurrence is minted by these isolated offline verification fixtures.


## W28 occurrence-1 instrument qualification - 2026-09-17T04:49:36.484823+00:00

REC-20260917-B. This separately dated supplement preserves every earlier validation byte. It reports offline engineering observations only, not participant findings or semantic improvement. HEAD found and retained: `40e2ff3c729e9961db88c8112a851ec1ca7f968e`, branch `claude/project-state-direction-j5rbun`. No provider/model API call, actual `.env` read, Git mutation, `runs/` write or actual brief access occurred. Existing docs were left to the concurrent reader; the requested workflow append and ledger/STATUS text are staged under `work/w28` for the judge.

Implemented the additive `r003-open-v1` profile using shared strict R002 calls/storage/preflight and the published A2 one-repair mechanism. New independently pinned recipes are `r003-cross-v1.json` and `r003-decomposed-v1.json`; the earlier draft recipes/plans/source pins remain unchanged. Canonical-only O01-O08 registry custody uses exact occurrence-local `p/ONN.txt` hashes, with participant step/quote labels, prose check contents, no oracle/admission/recoding/checker route and no string-equality semantic gate. Native has no repair; both loops have at most14 logical calls/28 attempts. Decomposition has a distinct closing response after completed-cycle semantic terminals, preserves accepted steps, and never closes after zero-cycle or fatal delivery/resource failure. Its partial/suspended stop reasons remain visible and are not classified as failed delivery.

Actual scripted launcher-to-CLI-to-engine integration ran O01 and O02 across NATIVE, LOOP-CROSS and LOOP-DECOMPOSED. Each native delivered1call/1attempt; each CROSS delivered14calls/15attempts including one prose critic repaired once on the same seat/ceiling; each decomposition delivered14calls/14attempts with3accepted steps and separate synthesis/closing. Total58logical calls/60offline attempts. Criticism contents remain fallible prose; passing schema/custody never adjudicates them. The fixture also proves zero-repair native failure, preserved failed-cell evidence and separately numbered successor, exact resume skipping, semantic partial/zero-cycle terminal handling, and no network/env-file access through these integrated paths. Additional focused tests cover second schema failure, fatal/no-close paths, canonical path/hash drift, capability gates, missing/malformed/future seals using fixture files only, source/input/argv/output drift and indeterminate-intent refusal. The projected longest actual evidence path under the default `C:/Dev/miniReason/runs/R003-open-v1/o001` is106characters, strictly below200.

Final requested qualification: **290/290 reason tests pass;26/26 docs-pin tests pass**. Final focused changed-surface suite passes20/20 (included in the290); a subsequent selected-row canonical hardening passed its6/6 engine tests and is included in the290. The `FAILED rc=2` and `CONFIG_ERROR` messages below are deliberate negative fixtures inside passing tests. Earlier preparatory interface/path/seal fixture failures were corrected and retained in `work/w28/ERRATA-AND-LESSONS.md` and linked agent transcripts. Nothing failing is omitted or relabelled as a live observation.

Exact requested command/output transcript:

```text
2026-09-17T04:43:49.383913+00:00
C:/Users/darre/AppData/Local/Programs/Python/Python311/python.exe -B -X utf8 -m unittest discover -s tests/reason -t .
...............................................................CONFIG_ERROR
...................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 290 tests in 116.326s

OK
Run directory: C:\Dev\miniReason\work\w28\evidence\cli\a9652ebd
{"run_id": "20260917T044412Z-r002-e8f414", "stop_reason": "complete", "completed_cycles": 0, "calls": 1}
{"run_id": "20260917T044412Z-r002-e8f414", "stop_reason": "complete", "completed_cycles": 0, "calls": 1}
{"mode": "offline", "phase": "main", "schema": "minireason.r002.launcher.v2", "scientific_evidence": false, "selected_candidates": ["C05", "C06", "C09", "C12"], "status": "COMPLETE"}
{"mode": "offline", "phase": "main", "schema": "minireason.r002.launcher.v2", "scientific_evidence": false, "selected_candidates": ["C05", "C06", "C09", "C12"], "status": "COMPLETE"}
O01-n: COMPLETE rc=0
O01-x: FAILED rc=2
O01-d: COMPLETE rc=0
O02-n: COMPLETE rc=0
O02-x: FAILED rc=2
O02-d: COMPLETE rc=0
O01-x: COMPLETE rc=0
O02-x: COMPLETE rc=0
O01-n: FAILED rc=2
O01-n: COMPLETE rc=0
O01-d: COMPLETE rc=0
O01-d: COMPLETE rc=0
O01-d: COMPLETE rc=0
O01-n: COMPLETE rc=0
O01-x: COMPLETE rc=0
O01-d: COMPLETE rc=0
O02-n: COMPLETE rc=0
O02-x: COMPLETE rc=0
O02-d: COMPLETE rc=0

EXIT_CODE=0

2026-09-17T04:24:23.803522+00:00
C:/Users/darre/AppData/Local/Programs/Python/Python311/python.exe -B -X utf8 -m unittest tests.loop.test_docs_pins
..........................
----------------------------------------------------------------------
Ran 26 tests in 0.023s

OK

EXIT_CODE=0
```

Separate read-only internal engineering acceptance found no remaining actionable issue; it is not the following user's judge or a live dispatch approval. Exact source/test/problem/public-registry pins are in `SOURCE_PINS.instrument-v1.json`; `work/w28/R003-CAPABILITY-CANDIDATE.json` matches those current runtime bytes and is deliberately live-refused pending independent review. The actual brief seal was not opened or qualified. The complete detached eight-problem/three-condition command, required judged files and budget projection are in `work/w28/OCC1-LAUNCH.md`; no live command was executed. EC01 remains deferred. Protected-byte audit and full handoff index: `work/w28/INDEX.md`.


## Independent instrument judge, REC-20260917-B - 2026-09-17T05:13:12.468879+00:00

APPROVED-AS-CORRECTED for publication and occurrence-1 engineering launch readiness. No live provider/model call, actual .env content read, actual sealed ONN.md brief open, Git mutation or runs write occurred. Frozen PLAN, historical validation prefix, R001/R002 recipes and published R002 evidence remain unchanged. The R002 launcher changes only by additive fixture roots/error text; existing experimental behavior is preserved.

Corrections: admit the requested judge fixture paths and preserve TMP; accept the existing immutable custodian seal schema without a hand-made replacement; carry the latest delivered disputed step into partial decomposed closure with explicit acceptance status; bind the R003 launcher/provider sources in the reviewed capability; apply the staged engineer workflow and replace stale refused-target command documentation. Detailed path:line findings, exact old -> new patches and all probes: work/review28/INDEX.md and REPORT.md. The original engineering source pins remain untouched; SOURCE_PINS.instrument-v2.json and R003-CAPABILITY.json describe the final judged bytes. launch-occurrence-1.ps1 is complete and parsed without execution.

Required suites (Python3.11, PYTHONPATH=src;tests, UTF8, TMP=C:/tr28, MINIREASON_TEST_WORK=work/review28/evidence):

```text
-m unittest discover -s tests/reason -t .
Ran 295 tests in 109.887s
OK (exit 0)

-m unittest tests.loop.test_docs_pins -v
Ran 26 tests in 0.018s
OK (exit 0)
```

Full transcripts: work/review28/reason-full-final.txt and docs-pins.txt. Five new judge regressions are included in295. Negative fixtures intentionally record failed cells inside passing no-replay tests. One earlier full-suite run failed12assertions and2errors because the judge incorrectly placed legacy dummy env-file fixtures outside the repository; production correctly refused that path. Correcting the test environment, not weakening credential admission, yielded the passing suite. The earlier transcript and all pre-fix probes remain preserved.

Exact final direct launcher invocation:

```powershell
$env:PYTHONPATH='src;tests'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
$env:TMP='C:/tr28'
& 'C:/Users/darre/AppData/Local/Programs/Python/Python311/python.exe' -B -X utf8 experiments/diagnostics/R003-open-problems-trial-series/run_R003.py new --series C:/tr28/direct-offline --problems O01 O02 --conditions NATIVE LOOP-CROSS LOOP-DECOMPOSED --question 'Do the exact six offline CLI cells terminate with preserved manifests and no key access?' --mode offline --env-file .env
```

```text
O01-n: COMPLETE rc=0
O01-x: COMPLETE rc=0
O01-d: COMPLETE rc=0
O02-n: COMPLETE rc=0
O02-x: COMPLETE rc=0
O02-d: COMPLETE rc=0
occurrence=C:/tr28/direct-offline/o002; FINISHED; rows=6; failed=0
status and terminal resume: exit0; entire occurrence byte-identical
```

This is the default cannot-decide fixture, not a substantive answer. Earlier o001 is retained under its earlier source identity. Full scripted launcher/CLI/shared-engine qualification separately created C:/tr28/scripted-final/o001: each native1logical/1attempt, each CROSS14/15 with one same-seat prose-critic repair, each decomposed14/14 with three accepted steps, synthesis and closing. Total58logical/60attempts, zero checker/stall, all6cells complete, terminal resume byte-identical, maximum projected default-run path106characters. Full transcript and hashes: work/review28/scripted-matrix-final-qualified.txt and SCRIPTED-MATRIX.json.

Legacy-v1, public-working-v2 and all R002 prompt maps/render/repair probes match HEAD byte for byte. R003 continues to call shared r002._call for A2 repair and transport/preflight; it does not duplicate those mechanisms. EC01 is NOT FOUND by design: ENGINEERING-SPEC.md explicitly defers it to occurrence2.

The existing seal metadata hash matches seal-001.json and the custodian's ledger record; all8problem hashes and brief file-presence/sizes match. The judge did not reopen actual brief bytes; the live gate will hash them before dispatch. Exposure and same-reader custody limitations remain declared. Capability and conservative tokenizer validation pass for all3conditions without provider initialization. All launch inputs now exist; .env presence/ignore status was checked without inspecting credentials. This establishes instrument readiness, not valid credentials, provider availability, independent-staffed custody or scientific success. Publication and actual dispatch remain separate and unperformed.
