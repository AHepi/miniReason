# R003 occurrence-1 commands

Current instrument instructions, REC-20260917-B, independent judge correction. These supersede the draft's unsupported-target commands (preserved in Git and work/review28/original). No live command was executed by the engineer or judge. Publish the reviewed delivery before the separately authorized live launch.

```powershell
Set-Location -LiteralPath 'C:/Dev/miniReason'
$env:PYTHONPATH='src;tests'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:GIT_OPTIONAL_LOCKS='0'
$env:TMP='C:/tr28'
$py='C:/Users/darre/AppData/Local/Programs/Python/Python311/python.exe'
$r003='experiments/diagnostics/R003-open-problems-trial-series'
& $py -B -X utf8 -c "from pathlib import Path; Path('C:/tr28').mkdir(exist_ok=True)"
```

## Offline qualification and staging

This exact two-problem matrix was run offline with zero failed cells. If repeated, numbering creates a new occurrence; it does not overwrite the recorded one.

```powershell
& $py -B -X utf8 "$r003/run_R003.py" new --series C:/tr28/direct-offline --problems O01 O02 --conditions NATIVE LOOP-CROSS LOOP-DECOMPOSED --question 'Do the exact six offline CLI cells terminate with preserved manifests and no key access?' --mode offline --env-file .env
& $py -B -X utf8 "$r003/run_R003.py" status --occurrence C:/tr28/direct-offline/o002
& $py -B -X utf8 "$r003/run_R003.py" resume --occurrence C:/tr28/direct-offline/o002
```

The printed occurrence path is authoritative. `.env` is an opaque argument in offline mode and is never read. Default canned fixtures return explicit inability to decide; full three-cycle routes, one same-seat prose repair, synthesis and closure are exercised separately by `tests.reason.test_r003_occurrence`. Neither fixture proves substantive reasoning success. Exact transcripts and limits are in VALIDATION.md and work/review28.

`new` defaults to `--mode plan` and all O01-O08/all three conditions. Use `--series C:/tr28/planned` for a reviewable plan without touching runs. Plan resume remains a plan and sends nothing. The obsolete `smoke` subcommand is no longer part of this launcher; use the explicit offline command above.

## Complete detached occurrence 1

Every required non-secret file is supplied with the reviewed delivery. No hand-written canonical registry, seal conversion or capability edit remains:

```powershell
& 'C:/Dev/miniReason/experiments/diagnostics/R003-open-problems-trial-series/launch-occurrence-1.ps1'
```

The script declares all eight problems, NATIVE, LOOP-CROSS and LOOP-DECOMPOSED, one occurrence question, `--mode live --env-file .env --authorize-live`, the existing R002 conservative tokenizer descriptor, `R003-CAPABILITY.json`, and the custodian's existing `briefs/MANIFEST.json`. It uses a hidden detached process and new UTC-labelled stdout/stderr paths, refuses an existing `runs/R003-open-v1/o001`, and prints the process identity. The complete command and exact file-presence/pin audit are also in work/review28/OCC1-LAUNCH.md. The ignored `.env` must supply the declared keys at the qualified call boundary; the judge checks only its existence/ignore status, never its contents.

The launcher creates numbered immutable matrix manifests, exact p/ONN.txt copies and CANONICAL.json automatically. Each cell delegates to the shared strict `tools/reason.py run-r002-native` or `run-r002` with `--study-profile r003-open-v1 --canonical-registry <occurrence>/CANONICAL.json`. Only the exact versioned `r003-cross-v1.json` and `r003-decomposed-v1.json` are admitted. No R002 admission, oracle, coding map or brief content enters the participant request. EC01 is deferred to the separately declared occurrence-2 engineering change.

The reviewed capability binds the profile, runtime/CLI, schemas, prompts, recipes, endpoints, R003 launcher and provider source bytes. The existing seal format is adapted in memory; author/lineage/exposure/UTC and exact problem/brief hashes are validated before dispatch, and source/input/argv/evidence drift refuses continuation. The seal discloses full PLAN exposure and a same-reader custodial process; neither the gate nor this qualification claims full blindness or independent staffing.

NATIVE has one native DeepSeek call at32768 completion and no repair. CROSS has native DeepSeek initial/return/closing32768, Qwen/GLM off critics16384 and DeepSeek off use16384. DECOMPOSED has Qwen/Qwen/Qwen off critics32768, native DeepSeek initial/return/synthesis/closing32768, and DeepSeek off STEP/use16384. Both loops permit one recorded same-seat schema repair per logical call, at most three cycles and14logical/28attempts. Second schema failure, input overflow, ceiling or transport failure stops without fallback/truncation. Partial semantic terminals are delivered with their exact stop reasons; fatal failures and zero completed cycles receive no closing call. The partial closing receives the latest delivered step without changing acceptance. No later use follows closure.

All eight:232logical calls,456maximum attempts,11272192completion and14942208input tokens; combined26214400. Without repairs:232attempts,5767168completion and7602176input. This is an allowance, not predicted spend. Attempt timeout is300seconds; no shorter whole-cell launcher timeout is imposed. Cells run sequentially.

## Recovery

```powershell
& $py -B -X utf8 "$r003/run_R003.py" status --occurrence runs/R003-open-v1/o001
& $py -B -X utf8 "$r003/run_R003.py" resume --occurrence runs/R003-open-v1/o001
```

Resume revalidates frozen source/input/argv/output and live seal/capability, skips every successful or failed terminal cell, and refuses an intent or output without a result. It cannot change mode or convert a plan to live. An indeterminate provider attempt requires reconciliation, never blind replay.

`rerun-failed --occurrence <printed-path> --question '<new one-line question>' --reason '<prospective reason>' --mode plan|offline|live` creates a separately numbered successor containing only known failed cells and a parent link. Live successors repeat all five live gates (`--env-file`, `--tokenizer-pins`, `--capability`, `--brief-manifest`, `--authorize-live`). Source changes require `new`. No automatic successor or retry is authorized.


## R3-A1 occurrence-2 commands (2026-09-17)

The historical occurrence-1 commands above retain their original meaning. Current CLI `new` defaults to amendment `R3-A1`, the two loop conditions and `R003-input-preflight.json`; use `--amendment occurrence-1` only for explicit historical offline fixtures. R3-A1 refuses a NATIVE selection because the reader reuses o001's eight completed answers. It selects the new v2 recipes, preserves canonical problems, and leaves EC01 deferred under the owner's separate instrument amendment.

```cmd
set PYTHONPATH=src;tests
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set TMP=C:\tw30
"C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe" -B -X utf8 experiments\diagnostics\R003-open-problems-trial-series\run_R003.py new --series C:\tw30\offline-r3-a1 --amendment R3-A1 --problems O01 O02 --conditions LOOP-CROSS LOOP-DECOMPOSED --question "Across O01-O08, does either loop yield a specific usable reframing absent from fresh native reasoning, and what losses accompany it?" --mode offline
```

The offline run has zero provider/model calls and never reads .env. Its printed numbered occurrence is authoritative. Status/resume only accept exact frozen input/source hashes. Completed or partial historical evidence is not overwritten. Qualification transcripts and the exact tested occurrence are appended to VALIDATION.

The full detached live command and all arguments are supplied in `work/w30/OCC2-LAUNCH.md` and `work/w30/run_r003_occ2.cmd`. It names `runs/R003-open-v1/o002`, explicitly guards the expected number, and uses `R003-CAPABILITY.R3-A1.json`. That file is an **UNREVIEWED engineering candidate**, so the separate judge's actual review receipt and publication are required before live dispatch. This fix-up does not launch it. The referenced existing sealed manifest is checked at future dispatch; no brief content is used by participants.

R3-A1 input caps: DeepSeek967232, Qwen221184, GLM965184, Kimi965184 wire bytes (descriptor coverage only for Kimi). See PLAN for documentation values, source URLs, reserve semantics and caveats. The legacy CLI scalar prompt cap remains32768 as an old API compatibility selector; **R3-A1 admission and per-attempt records use the descriptor's route-specific context budget**, not that scalar. CROSS critics32,768; other output allowances unchanged. Full selected occurrence:224logical/448maxattempts,12,582,912maxcompletion and361,895,936maxprompt tokens including reserve. These are loose ceilings, not predicted spend.


## Judged occurrence-2 command, 2026-09-17T06:46:17.532174+00:00

This supersedes the earlier work/w30 candidate command. Source/capability/descriptor/pins must be published and remotely verified before dispatch. The complete tracked command requires no handwritten conversion; no real launch was performed by the judge.

From `cmd.exe`, detach the complete checked command file:

```cmd
start "" /b cmd.exe /d /c "C:\Dev\miniReason\experiments\diagnostics\R003-open-problems-trial-series\launch-occurrence-2.cmd"
```

Complete command-file contents:

```cmd
@echo off
cd /d C:\Dev\miniReason
if not exist "C:\Dev\miniReason\work\review30" mkdir "C:\Dev\miniReason\work\review30"
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PYTHONDONTWRITEBYTECODE=1
set PYTHONPATH=src;tests
set GIT_OPTIONAL_LOCKS=0
set TMP=C:\tr30
set TEMP=C:\tr30
if not exist C:\tr30 mkdir C:\tr30
if not exist C:\tr30 ( echo exit=refused-tmp-unavailable > "C:\Dev\miniReason\work\review30\r003-occ2.exit" & exit /b 3 )
if not exist C:\Dev\miniReason\runs\R003-open-v1\o001\MANIFEST.json ( echo exit=refused-missing-o001 > "C:\Dev\miniReason\work\review30\r003-occ2.exit" & exit /b 3 )
if exist C:\Dev\miniReason\runs\R003-open-v1\o002 ( echo exit=refused-o002-exists > "C:\Dev\miniReason\work\review30\r003-occ2.exit" & exit /b 3 )
"C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe" -B -X utf8 experiments\diagnostics\R003-open-problems-trial-series\run_R003.py new --series C:\Dev\miniReason\runs\R003-open-v1 --amendment R3-A1 --expected-occurrence o002 --problems O01 O02 O03 O04 O05 O06 O07 O08 --conditions LOOP-CROSS LOOP-DECOMPOSED --question "Across O01-O08, does either loop yield a specific usable reframing absent from fresh native reasoning, and what losses accompany it?" --mode live --env-file C:\Dev\miniReason\.env --tokenizer-pins C:\Dev\miniReason\experiments\diagnostics\R003-open-problems-trial-series\R003-input-preflight.json --capability C:\Dev\miniReason\experiments\diagnostics\R003-open-problems-trial-series\R003-CAPABILITY.R3-A1.json --brief-manifest C:\Dev\miniReason\experiments\diagnostics\R003-open-problems-trial-series\briefs\MANIFEST.json --authorize-live > "C:\Dev\miniReason\work\review30\r003-occ2.log" 2>&1
echo exit=%ERRORLEVEL% > "C:\Dev\miniReason\work\review30\r003-occ2.exit"
```

The question is byte-for-byte the o001 question. Only `LOOP-CROSS` and `LOOP-DECOMPOSED` are selected; the reader reuses o001 NATIVE answers, and no NATIVE call is dispatched. `--expected-occurrence o002`, the prechecks, the series lock and create-only writes refuse overwrite or an unexpected successor number before any participant dispatch.

R3-A1 CROSS uses Qwen `ollama/qwen3.5-397b.native` as `signal_a` and Kimi `ollama/kimi-k3.native` as `signal_b`, each off at 32,768 completion tokens. This applies the root C03 ruling replacing GLM for occurrence 2. DECOMPOSED retains its Qwen critic seats. The reviewed descriptor caps are DeepSeek 967,232, Qwen 221,184, GLM 965,184 and Kimi 965,184 exact wire bytes; GLM remains descriptor coverage but is not selected by either occurrence-2 loop.

| Projection | CROSS/problem | DECOMPOSED/problem | Eight-problem occurrence |
|---|---:|---:|---:|
| Logical/base attempts | 14 | 14 | 224 |
| Maximum attempts including one repair each | 28 | 28 | 448 |
| Base completion allowance | 409,600 | 376,832 | 6,291,456 |
| Maximum completion allowance | 819,200 | 753,664 | 12,582,912 |
| Base prompt allowance including reserve | 11,309,248 | 11,309,248 | 180,947,968 |
| Maximum prompt allowance | 22,618,496 | 22,618,496 | 361,895,936 |

Combined maximum is 374,478,848 tokens. The sequential 448-attempt, 300-second envelope is 134,400 seconds (37h20m). These are loose authorization ceilings, not a spend or duration prediction. A schema repair consumes the same seat's ceiling; no transport retry, model fallback or ceiling retry is authorized.

The tracked executable `experiments/diagnostics/R003-open-problems-trial-series/launch-occurrence-2.cmd` exactly matches the command above and the review copy. Final source/capability verification is recorded in `FINAL-AUDIT.json`; `launch/SOURCE-PIN-REFRESH.md` retains the audit procedure. The required two-problem offline command and repeat-refusal proof are in `launch/READINESS.md`.

## R3-A2 occurrence-3 command (2026-09-17)

R3-A2 selects `r003-open-v1-r3-a2` and the versioned v3 CROSS and DECOMPOSED
recipes. It reuses occurrence-1 NATIVE answers and inherits the exact R3-A1
input descriptor, routes and allowances. It does not rewrite occurrence 1 or 2.
The candidate capability and source-pin identities are
`R003-CAPABILITY.R3-A2.json` and `SOURCE_PINS.R3-A2.json`; the judge must create
and review them from the final source snapshot before dispatch.

From `cmd.exe`, detach the complete command file:

```cmd
start "" /b cmd.exe /d /c "C:\Dev\miniReason\experiments\diagnostics\R003-open-problems-trial-series\launch-occurrence-3.cmd"
```

The command guards the presence of `o001` and `o002`, refuses any existing
`o003`, and passes `--expected-occurrence o003`. Its exact contents and resource
projection are recorded in `work/w32/OCC3-LAUNCH.md`. No command in this section
was executed live during the fix-up.


### Independent judge complete occurrence-3 command (2026-09-17T08:20:08.604931+00:00)

The following supersedes the engineer scratch paths and pending-capability wording above. Reviewed capability/source pins are exact; publish and verify the exact tree before live dispatch.

# Complete occurrence-3 command and projection

From cmd.exe, detached:

```cmd
start "" /b cmd.exe /d /c "C:\Dev\miniReason\experiments\diagnostics\R003-open-problems-trial-series\launch-occurrence-3.cmd"
```

Complete command file (exact tracked candidate content):

```cmd
@echo off
cd /d C:\Dev\miniReason
if not exist "C:\Dev\miniReason\work\review32" mkdir "C:\Dev\miniReason\work\review32"
if not exist C:\tr32 mkdir C:\tr32
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PYTHONDONTWRITEBYTECODE=1
set PYTHONPATH=src;tests
set GIT_OPTIONAL_LOCKS=0
set TMP=C:\tr32
set TEMP=C:\tr32
if not exist C:\tr32 ( echo exit=refused-tmp-unavailable > "C:\Dev\miniReason\work\review32\r003-occ3.exit" & exit /b 3 )
if not exist C:\Dev\miniReason\runs\R003-open-v1\o001\MANIFEST.json ( echo exit=refused-missing-o001 > "C:\Dev\miniReason\work\review32\r003-occ3.exit" & exit /b 3 )
if not exist C:\Dev\miniReason\runs\R003-open-v1\o002\MANIFEST.json ( echo exit=refused-missing-o002 > "C:\Dev\miniReason\work\review32\r003-occ3.exit" & exit /b 3 )
if exist C:\Dev\miniReason\runs\R003-open-v1\o003 ( echo exit=refused-o003-exists > "C:\Dev\miniReason\work\review32\r003-occ3.exit" & exit /b 3 )
"C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe" -B -X utf8 experiments\diagnostics\R003-open-problems-trial-series\run_R003.py new --series C:\Dev\miniReason\runs\R003-open-v1 --amendment R3-A2 --expected-occurrence o003 --problems O01 O02 O03 O04 O05 O06 O07 O08 --conditions LOOP-CROSS LOOP-DECOMPOSED --question "Across O01-O08, does either loop yield a specific usable reframing absent from fresh native reasoning, and what losses accompany it?" --mode live --env-file C:\Dev\miniReason\.env --tokenizer-pins C:\Dev\miniReason\experiments\diagnostics\R003-open-problems-trial-series\R003-input-preflight.json --capability C:\Dev\miniReason\experiments\diagnostics\R003-open-problems-trial-series\R003-CAPABILITY.R3-A2.json --brief-manifest C:\Dev\miniReason\experiments\diagnostics\R003-open-problems-trial-series\briefs\MANIFEST.json --authorize-live > "C:\Dev\miniReason\work\review32\r003-occ3.log" 2>&1
echo exit=%ERRORLEVEL% > "C:\Dev\miniReason\work\review32\r003-occ3.exit"
```

| Projection | CROSS/problem | DECOMPOSED/problem | Eight-problem occurrence |
|---|---:|---:|---:|
| Logical/base attempts | 14 | 14 | 224 |
| Maximum attempts with one repair each | 28 | 28 | 448 |
| Base completion allowance | 409,600 | 376,832 | 6,291,456 |
| Maximum completion allowance | 819,200 | 753,664 | 12,582,912 |
| Base prompt allowance including reserve | 11,309,248 | 11,309,248 | 180,947,968 |
| Maximum prompt allowance | 22,618,496 | 22,618,496 | 361,895,936 |

Combined maximum: 374,478,848 tokens. Sequential attempt envelope: 448 x 300 seconds = 134,400 seconds (37h20m). These are loose authorization ceilings, not predicted cost/duration. No transport retry, fallback or ceiling retry. Same eight problems/question; o001 NATIVE reused only by the reader. No live run was performed by this judge. Publication and exact remote/local tree verification must precede launch.


## R3-A3 occurrence-4 EC01 command (declared 2026-09-17)

This command is prospective and unexecuted. The exact R3-A3 source, tests, source pins and independently reviewed `R003-CAPABILITY.R3-A3.json` must be published and remotely verified before the external command file is installed or launched. This engineering task made no provider/model call and did not read `.env`.

From `cmd.exe`, after installing the reviewed command file at the shown external path, detach it with:

```cmd
start "" /b cmd.exe /d /c "C:\Dev\minireason-launch\run_r003_occ4.cmd"
```

Complete command-file contents:

```cmd
@echo off
cd /d C:\Dev\miniReason
if not exist C:\tw36 mkdir C:\tw36
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PYTHONDONTWRITEBYTECODE=1
set PYTHONPATH=src;tests
set GIT_OPTIONAL_LOCKS=0
set TMP=C:\tw36
set TEMP=C:\tw36
if not exist C:\tw36 ( echo exit=refused-tmp-unavailable > "C:\Dev\minireason-launch\r003-occ4.exit" & exit /b 3 )
if not exist C:\Dev\miniReason\runs\R003-open-v1\o001\MANIFEST.json ( echo exit=refused-missing-o001 > "C:\Dev\minireason-launch\r003-occ4.exit" & exit /b 3 )
if not exist C:\Dev\miniReason\runs\R003-open-v1\o002\MANIFEST.json ( echo exit=refused-missing-o002 > "C:\Dev\minireason-launch\r003-occ4.exit" & exit /b 3 )
if not exist C:\Dev\miniReason\runs\R003-open-v1\o003\MANIFEST.json ( echo exit=refused-missing-o003 > "C:\Dev\minireason-launch\r003-occ4.exit" & exit /b 3 )
if exist C:\Dev\miniReason\runs\R003-open-v1\o004 ( echo exit=refused-o004-exists > "C:\Dev\minireason-launch\r003-occ4.exit" & exit /b 3 )
"C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe" -B -X utf8 experiments\diagnostics\R003-open-problems-trial-series\run_R003.py new --series C:\Dev\miniReason\runs\R003-open-v1 --amendment R3-A3 --expected-occurrence o004 --problems O01 O02 O03 O04 O05 O06 O07 O08 --conditions LOOP-CROSS --question "On the same initial proposal, does delivering cycle-1 objections change a response and later use on a flaw named in the sealed brief, compared with generating and archiving those same objections?" --mode live --env-file C:\Dev\miniReason\.env --tokenizer-pins C:\Dev\miniReason\experiments\diagnostics\R003-open-problems-trial-series\R003-input-preflight.json --capability C:\Dev\miniReason\experiments\diagnostics\R003-open-problems-trial-series\R003-CAPABILITY.R3-A3.json --brief-manifest C:\Dev\miniReason\experiments\diagnostics\R003-open-problems-trial-series\briefs\MANIFEST.json --authorize-live > "C:\Dev\minireason-launch\r003-occ4.log" 2>&1
echo exit=%ERRORLEVEL% > "C:\Dev\minireason-launch\r003-occ4.exit"
```

The presence guards require all prior occurrence manifests and refuse any existing o004. `--expected-occurrence o004`, the series lock and create-only writes refuse an unexpected allocation or overwrite. Explicit `--conditions LOOP-CROSS` selects the only R3-A3 condition. The reader may reuse o001 NATIVE later; no participant sees that baseline.

Per problem the shared prefix is initial + Qwen critic + Kimi critic. Cycle 1 then runs `c0001-R-return`, `c0001-R-use`, `c0001-A-return`, `c0001-A-use`, in that order. ARCHIVED ends there. Cycles 2-3 and closing continue only from RETURNED under existing early-stop rules.

| Projection | Per problem | Eight problems |
|---|---:|---:|
| Logical/base attempts | 16 | 128 |
| Maximum attempts with one repair each | 32 | 256 |
| Base completion allowance | 458,752 | 3,670,016 |
| Maximum completion allowance | 917,504 | 7,340,032 |
| Base prompt allowance including reserve | 13,243,712 | 105,949,696 |
| Maximum prompt allowance | 26,487,424 | 211,899,392 |

Combined maximum allowance is 219,239,424 tokens. The sequential 256-attempt, 300-second envelope is 76,800 seconds (21h20m). These are loose authorization ceilings, not predicted spend or duration. No transport retry, fallback or ceiling retry is authorized. A branch failure is preserved; an independently viable sibling may complete, but cycles 2-3/closing require the RETURNED return/use gate.

Status and recovery after a separately authorized launch use the normal commands:

```cmd
"C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe" -B -X utf8 experiments\diagnostics\R003-open-problems-trial-series\run_R003.py status --occurrence C:\Dev\miniReason\runs\R003-open-v1\o004
"C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe" -B -X utf8 experiments\diagnostics\R003-open-problems-trial-series\run_R003.py resume --occurrence C:\Dev\miniReason\runs\R003-open-v1\o004
```

Resume verifies the frozen occurrence manifest/source custody before execution and skips cells with terminal launcher result records. It does not reconstruct every internal archive in those already terminal cells, and never replays unknown or indeterminate delivery. `work/w36/OCC4-LAUNCH.md` preserves the same command and projection for the judge/publisher handoff.


### Judge36 complete occurrence-4 command and projection - 2026-09-17T10:28:07.400650+00:00

# R003 occurrence 4 detached command and projection

Prospective only. Do not create or run the external command file until the exact R3-A3 source, tests, source pins and independently reviewed `R003-CAPABILITY.R3-A3.json` have been published and remotely verified. This judge task made no provider/model call and did not read actual `.env` content.

From `cmd.exe`, detached:

```cmd
start "" /b cmd.exe /d /c "C:\Dev\minireason-launch\run_r003_occ4.cmd"
```

Complete `C:\Dev\minireason-launch\run_r003_occ4.cmd` contents:

```cmd
@echo off
cd /d C:\Dev\miniReason
if not exist C:\tr36 mkdir C:\tr36
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PYTHONDONTWRITEBYTECODE=1
set PYTHONPATH=src;tests
set GIT_OPTIONAL_LOCKS=0
set TMP=C:\tr36
set TEMP=C:\tr36
if not exist C:\tr36 ( echo exit=refused-tmp-unavailable > "C:\Dev\minireason-launch\r003-occ4.exit" & exit /b 3 )
if not exist C:\Dev\miniReason\runs\R003-open-v1\o001\MANIFEST.json ( echo exit=refused-missing-o001 > "C:\Dev\minireason-launch\r003-occ4.exit" & exit /b 3 )
if not exist C:\Dev\miniReason\runs\R003-open-v1\o002\MANIFEST.json ( echo exit=refused-missing-o002 > "C:\Dev\minireason-launch\r003-occ4.exit" & exit /b 3 )
if not exist C:\Dev\miniReason\runs\R003-open-v1\o003\MANIFEST.json ( echo exit=refused-missing-o003 > "C:\Dev\minireason-launch\r003-occ4.exit" & exit /b 3 )
if exist C:\Dev\miniReason\runs\R003-open-v1\o004 ( echo exit=refused-o004-exists > "C:\Dev\minireason-launch\r003-occ4.exit" & exit /b 3 )
"C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe" -B -X utf8 experiments\diagnostics\R003-open-problems-trial-series\run_R003.py new --series C:\Dev\miniReason\runs\R003-open-v1 --amendment R3-A3 --expected-occurrence o004 --problems O01 O02 O03 O04 O05 O06 O07 O08 --conditions LOOP-CROSS --question "On the same initial proposal, does delivering cycle-1 objections change a response and later use on a flaw named in the sealed brief, compared with generating and archiving those same objections?" --mode live --env-file C:\Dev\miniReason\.env --tokenizer-pins C:\Dev\miniReason\experiments\diagnostics\R003-open-problems-trial-series\R003-input-preflight.json --capability C:\Dev\miniReason\experiments\diagnostics\R003-open-problems-trial-series\R003-CAPABILITY.R3-A3.json --brief-manifest C:\Dev\miniReason\experiments\diagnostics\R003-open-problems-trial-series\briefs\MANIFEST.json --authorize-live > "C:\Dev\minireason-launch\r003-occ4.log" 2>&1
echo exit=%ERRORLEVEL% > "C:\Dev\minireason-launch\r003-occ4.exit"
```

The command refuses a missing o001/o002/o003 manifest, existing o004, unexpected occurrence number, unsupported condition, unreviewed capability or source/input drift. It selects LOOP-CROSS only and creates o004 without modifying earlier occurrences.

Per problem:

1. Shared cycle 1: initial + Qwen critic + Kimi critic.
2. RETURNED then ARCHIVED: `c0001-R-return`, `c0001-R-use`, `c0001-A-return`, `c0001-A-use`.
3. ARCHIVED ends after its use. RETURNED alone may run cycles 2-3 (two critics + return + use per cycle) and closing, subject to existing stops.

That is 16 logical calls and at most 32 attempts per problem. Across eight problems it is 128 logical calls and at most 256 attempts.

| Allowance | Per problem | Eight problems |
|---|---:|---:|
| Base completion | 458,752 | 3,670,016 |
| All-repair completion | 917,504 | 7,340,032 |
| Base prompt including reserve | 13,243,712 | 105,949,696 |
| All-repair prompt | 26,487,424 | 211,899,392 |

Combined maximum allowance: 219,239,424 tokens. Sequential wall envelope: 256 x 300 seconds = 76,800 seconds (21h20m). These are ceilings, not forecasts. No transport retry, fallback or ceiling retry.

The exact return prompt declaration is `ARCHIVED = RETURNED` with one contiguous UTF-8 span deleted and no replacement: the rendered `OPEN AND NEW OBJECTIONS` block, separators and `PUBLIC SIGNALS` block. System, role and schema bytes are unchanged. The occurrence records rendered start/end and the JSON-escaped wire start plus length, exact removed spans and SHA-256 values; all bytes outside the span are identical. Empty critic objection arrays establish only that no explicit objection items exist because `PUBLIC SIGNALS` can still contain substantive working/missing-derivation content. Inspect the removed signals before calling the difference metadata-only, and never infer nonconstant objection-content dependence from metadata alone.

After a separately authorized launch:

```cmd
"C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe" -B -X utf8 experiments\diagnostics\R003-open-problems-trial-series\run_R003.py status --occurrence C:\Dev\miniReason\runs\R003-open-v1\o004
"C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe" -B -X utf8 experiments\diagnostics\R003-open-problems-trial-series\run_R003.py resume --occurrence C:\Dev\miniReason\runs\R003-open-v1\o004
```

Resume verifies the frozen occurrence manifest/source custody before execution and skips cells with terminal launcher result records. It does not reconstruct every internal archive in those already terminal cells. Unknown or indeterminate delivery is never replayed.

A reviewable copy of those exact command-file contents is prepared at `C:/Dev/miniReason/work/review36/run_r003_occ4.cmd`. It has not been executed. After judge/publisher completion, the detached invocation can use this existing copy:

```cmd
start "" /b cmd.exe /d /c "C:\Dev\miniReason\work\review36\run_r003_occ4.cmd"
```


Judge correction accepted 2026-09-17T10:28:07.400650+00:00: the paired uses now freeze one concrete question/query ID from the initial working_position claim before either return. Final-source qualification:346reason+26docs-pin tests and both O01/O02 paired fixtures PASS. Reviewed capability and70source pins exact; pure input gate PASS. Earlier independent-question wording in engineer documents is superseded by the dated judge supplement, not silently rewritten.

Approval for publication and occurrence-4 engineering launch: APPROVED-AS-CORRECTED, subject to the final review36 scope audit. Actual execution still requires publication and remote/local equal-tree verification. This file and run_r003_occ4.cmd were not executed.



Final judge36 acknowledgement 2026-09-17T10:32:54.794457+00:00: the final scope/document audit referenced above PASSED. Publication and occurrence4 engineering launch readiness are APPROVED-AS-CORRECTED. The command remains unexecuted; publication and remote/local equal-tree verification still precede dispatch.
