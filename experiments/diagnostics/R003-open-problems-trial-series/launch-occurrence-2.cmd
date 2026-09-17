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
