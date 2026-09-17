# Exact R003 command surface and its current limits

DRAFT, no live execution authorized. Start in C:/Dev/miniReason. Forward-slash Windows paths below are accepted by PowerShell/Python.

```powershell
$env:PYTHONPATH='src;tests'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:GIT_OPTIONAL_LOCKS='0'
$env:TMP='C:/tr25'
$py='C:/Users/darre/AppData/Local/Programs/Python/Python311/python.exe'
$r003='experiments/diagnostics/R003-open-problems-trial-series'
& $py -B -X utf8 -c "from pathlib import Path; Path('C:/tr25').mkdir(exist_ok=True)"
```

## Staging, resume and separate failed-cell selection

```powershell
& $py -B -X utf8 "$r003/run_R003.py" new --mode plan --problems O01 --question 'On O01, does criticism produce a usable reframing missing from fresh native reasoning?'
& $py -B -X utf8 "$r003/run_R003.py" status --occurrence work/review25/series/o001
& $py -B -X utf8 "$r003/run_R003.py" resume --occurrence work/review25/series/o001
```

Omit --problems O01 to stage all eight. The printed directory is authoritative; numbering increments and existing directories are never reused. A plan-mode resume remains a plan and sends nothing. MANIFEST.json freezes exact per-cell argv, input/source hashes, question and order; QUESTION.json precedes manifest/dispatch. CLI argv contains the literal .env filename, never its contents. This launcher does not read .env. Brief contents never enter an occurrence or command.

```powershell
& $py -B -X utf8 "$r003/run_R003.py" new --mode offline --problems O01 --question 'On O01, do the installed guards truthfully refuse the unsupported target conditions?'
& $py -B -X utf8 "$r003/run_R003.py" rerun-failed --occurrence work/review25/series/o002 --mode plan --question 'Which installed instrument defect would this successor address?' --reason 'Stage a separate successor for known refused cells; no retry is dispatched.'
```

Substitute the actual printed offline directory for o002. Offline target failures are expected and cause exit2; they are not successful R003 runs. Resume verifies source/input/output bytes and skips terminal cells, successful or failed. An intent without a result refuses automatic replay. Rerun-failed selects only known terminal failures, creates a new numbered matrix with parent/reason, and preserves successful cells and prior evidence. Changed source needs a new occurrence/design receipt rather than same-source resume. There is no automatic retry or plan-to-live conversion.

## Exact direct target commands (currently refused, not launch-ready)

These intended tools/reason.py subcommands reuse its dispatch interface directly. tools/run_R002.py hardcodes the old study/admission. The manifest resolves absolute argv and uses short output aliases n/x/d. work/review25/direct-O01 must be a fresh destination.

```powershell
& $py -B -X utf8 tools/reason.py run-r002-native --problem "$r003/problems/O01.txt" --out work/review25/direct-O01/n --mode live --relations "$r003/public/RELATIONS.json" --condition NATIVE --thinking native --reasoning-effort medium --completion-tokens 32768 --attempt-policy strict --prompt-token-cap 32768 --retry-transport 0 --env-file .env

& $py -B -X utf8 tools/reason.py run-r002 --problem "$r003/problems/O01.txt" --out work/review25/direct-O01/x --mode live --relations "$r003/public/RELATIONS.json" --recipe "$r003/recipes/r003-cross-a2-draft.json" --cycles 3 --fork-registry "$r003/public/FORKS.json" --coding-manifest "$r003/public/CODINGS.json" --attempt-policy strict --prompt-token-cap 32768 --retry-transport 0 --env-file .env

& $py -B -X utf8 tools/reason.py run-r002 --problem "$r003/problems/O01.txt" --out work/review25/direct-O01/d --mode live --relations "$r003/public/RELATIONS.json" --recipe "$r003/recipes/r003-decomposed-closing-draft.json" --cycles 3 --fork-registry "$r003/public/FORKS.json" --coding-manifest "$r003/public/CODINGS.json" --attempt-policy strict --prompt-token-cap 32768 --retry-transport 0 --env-file .env
```

**Do not run these live commands now.** Current native refuses O-ID/registry admission; both loops refuse unknown pinned recipe identities. There is no valid current command implementing all requested conditions. Once PLAN section8 is engineered and qualified, append --study-profile r003-open-v1 --tokenizer-pins ACTUAL_REVIEWED_FILE --capability ACTUAL_REVIEWED_FILE to each command, freeze their true paths/hashes, and verify the sealed-brief manifest before dispatch. The proposed --study-profile flag is NOT FOUND in the current CLI and must be implemented as specified in ENGINEERING-SPEC.md. Those qualification files cannot truthfully be invented here. Editing JSON or deleting the wrapper's live hold does not supply missing instrument support. A separately reviewed successor must enforce these gates before loading credentials.

The future published individual recovery interface is tools/reason.py resume --run ACTUAL_SAVED_CELL_DIRECTORY --env-file .env. The outer manifest must first verify sources/inputs and reconcile indeterminate intents. Direct resume is not permission to resend a timed-out request. This R003 wrapper never starts live mode, including on resume.

## Tested published-instrument smoke

```powershell
& $py -B -X utf8 "$r003/run_R003.py" smoke --out work/review25/smoke
```

That destination already exists from validation; any deliberate repeat needs a new named directory and receipt. Exact subprocess exercised:

```powershell
& $py -B -X utf8 tools/reason.py run --problem "$r003/problems/O01.txt" --cycles 3 --recipe cross-family --mode offline --out work/review25/smoke
```

This is the published legacy prose fixture, not the requested R003 conditions. Legacy run loads a supplied env-file even offline, so smoke omits --env-file. Strict run-r002/run-r002-native defer env loading until a live call boundary, making the literal offline .env argument opaque. Offline fixture text is not a model observation. VALIDATION.md pastes actual results and their limits.
