# R003 occurrence 1; run only after the separate publication and live-dispatch decision.
$ErrorActionPreference='Stop'
Set-Location -LiteralPath 'C:\Dev\miniReason'
$env:PYTHONPATH='src;tests'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:GIT_OPTIONAL_LOCKS='0'
$env:TMP='C:\tr28'
$py='C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe'
$r003='C:\Dev\miniReason\experiments\diagnostics\R003-open-problems-trial-series'
$series='C:\Dev\miniReason\runs\R003-open-v1'
$tokenizers='C:\Dev\miniReason\experiments\diagnostics\R002-episodes-under-calibrated-difficulty\calibration\main-tokenizer-pins.json'
$required=@($py,"$r003\run_R003.py","$r003\R003-CAPABILITY.json","$r003\SOURCE_PINS.instrument-v2.json","$r003\briefs\MANIFEST.json",$tokenizers,'C:\Dev\miniReason\.env')
foreach ($number in 1..8) {
    $problemId='O{0:D2}' -f $number
    $required += "$r003\problems\$problemId.txt"
    $required += "$r003\briefs\$problemId.md"
}
foreach ($requiredFile in $required) {
    if (-not (Test-Path -LiteralPath $requiredFile -PathType Leaf)) { throw 'A required occurrence-1 file is missing; inspect OCC1-LAUNCH.md.' }
}
if (Test-Path -LiteralPath $series) { throw 'Occurrence-1 series already exists; inspect it and use the documented recovery command.' }
& $py -B -X utf8 -c "from pathlib import Path; Path('C:/tr28').mkdir(exist_ok=True); Path('C:/Dev/miniReason/work/review28').mkdir(parents=True, exist_ok=True)"
if ($LASTEXITCODE -ne 0) { throw 'Could not prepare temporary/log directories.' }
$stamp=[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')
$stdout="C:\Dev\miniReason\work\review28\occ1-$stamp.stdout.txt"
$stderr="C:\Dev\miniReason\work\review28\occ1-$stamp.stderr.txt"
if ((Test-Path -LiteralPath $stdout) -or (Test-Path -LiteralPath $stderr)) { throw 'Launch log already exists.' }
$launchArgs=@(
    '-B','-X','utf8',"$r003\run_R003.py",'new',
    '--series',$series,
    '--problems','O01','O02','O03','O04','O05','O06','O07','O08',
    '--conditions','NATIVE','LOOP-CROSS','LOOP-DECOMPOSED',
    '--question','"Across O01-O08, does either loop yield a specific usable reframing absent from fresh native reasoning, and what losses accompany it?"',
    '--mode','live','--env-file','C:\Dev\miniReason\.env',
    '--tokenizer-pins',$tokenizers,
    '--capability',"$r003\R003-CAPABILITY.json",
    '--brief-manifest',"$r003\briefs\MANIFEST.json",'--authorize-live'
)
Start-Process -FilePath $py -ArgumentList $launchArgs -WorkingDirectory 'C:\Dev\miniReason' -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru
