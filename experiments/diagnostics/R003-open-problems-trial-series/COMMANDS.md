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
