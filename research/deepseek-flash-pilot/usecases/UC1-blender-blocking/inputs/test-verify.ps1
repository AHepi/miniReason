$ErrorActionPreference = 'Stop'
$py = 'C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$cases = @(
  @('positive', "$root\shot-spec-positive.json", "$root\blender-blocking-positive.py", 0),
  @('reject-file-access', "$root\shot-spec-positive.json", "$root\negative-file-access.py", 1),
  @('reject-unknown-api', "$root\shot-spec-positive.json", "$root\negative-unknown-api.py", 1),
  @('reject-render-write', "$root\shot-spec-positive.json", "$root\negative-render-write.py", 1),
  @('reject-context-attribute', "$root\shot-spec-positive.json", "$root\negative-context-attribute.py", 1),
  @('reject-fake-receiver', "$root\shot-spec-positive.json", "$root\negative-fake-receiver.py", 1),
  @('reject-shot-constraint', "$root\negative-shot-constraint.json", "$root\blender-blocking-positive.py", 1),
  @('reject-duplicate-subject', "$root\negative-duplicate-subject.json", "$root\blender-blocking-positive.py", 1),
  @('reject-contradictory-motion', "$root\negative-contradictory-motion.json", "$root\blender-blocking-positive.py", 1),
  @('reject-unknown-field', "$root\negative-unknown-field.json", "$root\blender-blocking-positive.py", 1),
  @('reject-wrong-type', "$root\negative-wrong-type.json", "$root\blender-blocking-positive.py", 1),
  @('reject-nonfinite', "$root\negative-nonfinite.json", "$root\blender-blocking-positive.py", 1)
)
foreach ($case in $cases) {
  & $py -B -X utf8 "$root\verify_uc1.py" $case[1] $case[2]
  $actual = $LASTEXITCODE
  if ($actual -ne [int]$case[3]) { throw "$($case[0]) expected exit $($case[3]) got $actual" }
  Write-Output "$($case[0]): expected exit $actual"
}
exit 0
