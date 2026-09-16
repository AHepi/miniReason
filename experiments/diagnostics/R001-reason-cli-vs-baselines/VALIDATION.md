# R001 offline validation

Draft pre-registration only. No R001 provider/model call or environment-file read occurred. These are deterministic oracle computations and CLI offline fixtures. They do not establish live answer quality.

## Oracle execution

The exact output below is copied from work/w14/oracle-validation.txt. Each PNN script computes its answer from the fixed premises; run_all.py compares the result with the sealed JSON in answers/PNN.md and retains oracle/PNN.output.json.

```text
COMMAND: C:/Users/darre/AppData/Local/Programs/Python/Python311/python.exe -B experiments/diagnostics/R001-reason-cli-vs-baselines/oracle/run_all.py
UTC: 2026-09-16T09:22:52.043977+00:00
EXIT: 0
P01 PASS "7/20"
P02 PASS "41"
P03 PASS "state=A; x=6; y=3; output=GETEEGEEEEEEEG"
P04 PASS [["Blue", 2, 1, 15], ["Gold", 1, 0, 4]]
P05 PASS {"pressure_kpa_absolute": 167.5, "rise_m": 1.028}
P06 PASS "DAFECGB"
P07 PASS {"derivative_nonzero_everywhere": true, "injective": false, "preimages_of_13": [3, 5, 11], "unattainable_outputs": [4, 7, 8, 11, 12, 15]}
P08 PASS {"idle_intervals": [[6, 7]], "minimum_weighted_completion_sum": 253, "order": ["E", "B", "D", "F", "C", "A"], "start_finish": [["E", 0, 3], ["B", 3, 5], ["D", 5, 6], ["F", 7, 9], ["C", 9, 13], ["A", 13, 18]]}
ALL 8 ORACLES AGREE WITH SEALED ANSWERS; no participant execution
```

All eight agree. P04 also agrees between a literal bag interpreter and SQLite; P02 agrees between canonical orbit enumeration and the fixed-point formula; P08 agrees between permutation enumeration and a separate dynamic program. P05 solves at Decimal precision 50 and checks equilibrium and the physical root. Root reviewed every participant task, sealed derivation and oracle for premise correspondence.

## Launcher command and actual output

Prospective live command, not executed here; the separate publisher opens REC-20260916-F before operation:

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONPATH='src;tests'
$env:TMP='C:\tw14'
& 'C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe' -B experiments/diagnostics/R001-reason-cli-vs-baselines/run_R001.py --mode live --env-file .env --run-root work/w14/live
```

The tested final offline command:

```text
C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe C:\Dev\miniReason\experiments\diagnostics\R001-reason-cli-vs-baselines\run_R001.py --mode offline --problems P01 --run-root work/w14/ofpin-final
```

First invocation, exit 0:

```text
P01 cross: run
Run directory: C:\Dev\miniReason\work\w14\ofpin-final\R001-P01-cross
{"run_id": "20260916T092923Z-04bf836ad4-d2a117", "stop_reason": "cycle_budget", "completed_cycles": 3, "calls": 15}
P01 single: run
Run directory: C:\Dev\miniReason\work\w14\ofpin-final\R001-P01-single
{"run_id": "20260916T092924Z-833948efc8-d9c4ba", "stop_reason": "cycle_budget", "completed_cycles": 3, "calls": 10}
```

Repeated invocation, exit 0:

```text
P01 cross: skip terminal cycle_budget (20260916T092923Z-04bf836ad4-d2a117)
P01 single: skip terminal cycle_budget (20260916T092924Z-833948efc8-d9c4ba)
```

Both ran three cycles. The CROSS occurrence provides BARE, NATIVE and LOOP-CROSS; SINGLE provides LOOP-SINGLE. There were 15+10=25 scripted logical/attempt records and zero provider requests. The offline fixture raised no final use objection, so the conditional closing-return call was not triggered; the frozen true setting and full allowance were verified, not newly demonstrated with live data.

The repeat skips both terminal occurrences. 108 frozen configuration/input/call-evidence file hashes are unchanged. Original first-draft tests under work/w14/offline-launcher-test remain preserved and distinct from this final fixture.

Recovery and refusal probe evidence is under work/w14/launcher: terminal failure is skipped, interrupted evidence resumes with the same run ID, problem-hash mismatch refuses before dispatch, forbidden output roots and reordered problem subsets refuse, and a child without a terminal record blocks its successor. These probes use copied or synthetic offline evidence only. Actual .env was neither opened nor passed in offline mode. The launcher strips inherited provider variables from child environment and forwards only the --env-file path in live mode.

## Resource verification

The frozen CLI formula is maximum attempts = 2L+K and maximum completion allowance = 2S+32768K at zero transport retries. CROSS with baselines has L16, K5, S278528: maximum37 attempts and720896 completion tokens. SINGLE has L11, K11, S360448: maximum33 attempts and1081344 tokens. Across eight problems:216 logical allowances,560 maximum attempts,14417920 maximum completion tokens. The216 includes16 conditional closings. A 300-second wall applies per attempt; no monetary estimate or limit on input-token consumption is implied.

## Custody and scope

SOURCE_PINS.json identifies the inspected instrument and sealed task/oracle bytes. The launcher also verifies the prepared instrument and selected problem pins before use and stores source hashes in its manifest; it refuses incompatible saved occurrences. Conditions are aliases over their exact call streams, never repeated baseline runs.

This preparation changed only the R001 study directory and work/w14, apart from creating the user-requested C:/tw14 directory. It made no Git index/reference change and wrote nothing to docs. Concurrent changes elsewhere in the checkout belong to other work and were left untouched. The final local handoff is work/w14/INDEX.md; publication remains separate.

There is no live comparative result. The next substantive action is the separately receipted operator run, followed by the cross-lineage reading fixed in PLAN.md.


## Independent JUDGE correction and validation - 2026-09-16T09:49:53.295788+00:00

REC-20260916-F is now open. The preceding w14 observations remain historical and unchanged. The corrected launcher accepts --run-root as the manifest directory, including outside the repository; child occurrences deterministically live under runs/R001-<mode>-<pathhash>. It now respects the operator's TMP and uses the platform path separator. Current live invocation, not executed by this review:

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONPATH='src;tests'
$env:TMP='C:\tr13'
& 'C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe' -B experiments/diagnostics/R001-reason-cli-vs-baselines/run_R001.py --mode live --env-file .env
```

Independent scripts recomputed all eight problems before opening the worker oracles or answers. Mathematical disagreements: NOT FOUND. The exact answer facts and oracle programs remain unchanged. P03 now fixes canonical residues, P04 states bag multiplicity, P05 omits the redundant oracle-tolerance aside, and P07 neutrally asks for both polynomial facts without naming the false implication. SOURCE_PINS.json records the corrected unrun task bytes. PLAN adds measured smoke-3 usage and an explicitly uncertain role-based forecast. Evidence and old-to-new diffs are under work/review13.

Fresh actual oracle command/output:

```text
COMMAND: ['C:\\Users\\darre\\AppData\\Local\\Programs\\Python\\Python311\\python.exe', '-B', 'experiments/diagnostics/R001-reason-cli-vs-baselines/oracle/run_all.py']
RETURN CODE: 0
STDOUT:
P01 PASS "7/20"
P02 PASS "41"
P03 PASS "state=A; x=6; y=3; output=GETEEGEEEEEEEG"
P04 PASS [["Blue", 2, 1, 15], ["Gold", 1, 0, 4]]
P05 PASS {"pressure_kpa_absolute": 167.5, "rise_m": 1.028}
P06 PASS "DAFECGB"
P07 PASS {"derivative_nonzero_everywhere": true, "injective": false, "preimages_of_13": [3, 5, 11], "unattainable_outputs": [4, 7, 8, 11, 12, 15]}
P08 PASS {"idle_intervals": [[6, 7]], "minimum_weighted_completion_sum": 253, "order": ["E", "B", "D", "F", "C", "A"], "start_finish": [["E", 0, 3], ["B", 3, 5], ["D", 5, 6], ["F", 7, 9], ["C", 9, 13], ["A", 13, 18]]}
ALL 8 ORACLES AGREE WITH SEALED ANSWERS; no participant execution

STDERR:
```

Two-problem offline command/output (manifest in C:/tr13/r001-offline; child records under runs/):

```text
COMMAND: ['C:\\Users\\darre\\AppData\\Local\\Programs\\Python\\Python311\\python.exe', '-B', 'experiments/diagnostics/R001-reason-cli-vs-baselines/run_R001.py', '--mode', 'offline', '--problems', 'P01', 'P02', '--run-root', 'C:/tr13/r001-offline']
RETURN CODE: 0
STDOUT:
P01 cross: run
Run directory: C:\Dev\miniReason\runs\R001-offline-56441e0ecd\R001-P01-cross
{"run_id": "20260916T094421Z-04bf836ad4-0e051e", "stop_reason": "cycle_budget", "completed_cycles": 3, "calls": 15}
P01 single: run
Run directory: C:\Dev\miniReason\runs\R001-offline-56441e0ecd\R001-P01-single
{"run_id": "20260916T094422Z-833948efc8-889695", "stop_reason": "cycle_budget", "completed_cycles": 3, "calls": 10}
P02 cross: run
Run directory: C:\Dev\miniReason\runs\R001-offline-56441e0ecd\R001-P02-cross
{"run_id": "20260916T094423Z-04bf836ad4-427290", "stop_reason": "cycle_budget", "completed_cycles": 3, "calls": 15}
P02 single: run
Run directory: C:\Dev\miniReason\runs\R001-offline-56441e0ecd\R001-P02-single
{"run_id": "20260916T094424Z-833948efc8-aa5ff3", "stop_reason": "cycle_budget", "completed_cycles": 3, "calls": 10}

STDERR:
```

Actual rerun:

```text
COMMAND: ['C:\\Users\\darre\\AppData\\Local\\Programs\\Python\\Python311\\python.exe', '-B', 'experiments/diagnostics/R001-reason-cli-vs-baselines/run_R001.py', '--mode', 'offline', '--problems', 'P01', 'P02', '--run-root', 'C:/tr13/r001-offline']
RETURN CODE: 0
STDOUT:
P01 cross: skip terminal cycle_budget (20260916T094421Z-04bf836ad4-0e051e)
P01 single: skip terminal cycle_budget (20260916T094422Z-833948efc8-889695)
P02 cross: skip terminal cycle_budget (20260916T094423Z-04bf836ad4-427290)
P02 single: skip terminal cycle_budget (20260916T094424Z-833948efc8-aa5ff3)

STDERR:
```

The manifest correctly maps eight condition aliases to four occurrences; BARE/NATIVE select base-bare/base-native in the cross occurrence. All four skips preserved every one of 250 record files byte-for-byte; maximum actual path length is 118 characters. Separate nonterminal resume and command forwarding probe:

```text
COMMAND: ['C:\\Users\\darre\\AppData\\Local\\Programs\\Python\\Python311\\python.exe', '-B', 'C:\\Dev\\miniReason\\work\\review13\\launcher_probe.py']
RETURN CODE: 0
STDOUT:
Prepared empty offline occurrence; launcher must choose resume.
P01 cross: resume
{"run_id": "20260916T094630Z-04bf836ad4-b85725", "stop_reason": "cycle_budget", "completed_cycles": 3, "calls": 15}
P01 single: run
Run directory: C:\Dev\miniReason\runs\R001-offline-7bfa0641dd\R001-P01-single
{"run_id": "20260916T094632Z-833948efc8-d0612b", "stop_reason": "cycle_budget", "completed_cycles": 3, "calls": 10}
PASS: actual nonterminal resume, terminal completion, live run/resume env forwarding, parser agreement, inherited-key removal and TMP retention.

STDERR:
```

The forwarding check passed both run and resume arguments through the published tools/reason.py parser. Its env path was an unopened nonexistent probe path; no env-file contents were read. The launcher removes inherited provider-key values from child environments, forwards only the env-file path in live mode, and never prints environment values. All actual subprocesses in this validation were offline fixtures, not participant observations. Published-source comparison found all 18 pinned source files equal to c1463e0a. The hard budget independently recomputes to 216 logical allowances, 560 maximum attempts and 14,417,920 completion tokens; smoke-3 sums to 111,752 tokens, and the stated approximate planning scenario is 2.50 million total tokens across eight problems. No price is inferred.
