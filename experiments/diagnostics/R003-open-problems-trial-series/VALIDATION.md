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
