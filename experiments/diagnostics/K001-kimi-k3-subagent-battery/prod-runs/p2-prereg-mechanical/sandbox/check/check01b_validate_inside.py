"""Check 1b: validate.py from inside loop-prereg/ (per task, since root run failed on paths);
corroborating evidence for why it fails anywhere in the sandbox."""
import json
import subprocess
from pathlib import Path

OUT = Path("out/check1")

res = subprocess.run(
    ["python3", "validate.py"],
    capture_output=True, text=True, timeout=300, cwd="loop-prereg",
)
(OUT / "validate.cwd-loop-prereg.stdout.txt").write_text(res.stdout, encoding="utf-8")
(OUT / "validate.cwd-loop-prereg.stderr.txt").write_text(res.stderr, encoding="utf-8")

sandbox_modules = sorted(str(p) for p in Path("src").rglob("*") if p.is_file())
repo_list = Path("evidence/repo-files.txt").read_text(encoding="utf-8")
needed_globs = ("minireason/loop", "deepreason_core", "RECODING_TABLE",
                "use-table-golden", "C001-contrast-triple/occurrence-02/comparison.json")
evidence_repo = {g: (g in repo_list) for g in needed_globs}

report = {
    "cwd": "loop-prereg/",
    "command": "python3 validate.py",
    "exit_code": res.returncode,
    "stdout": res.stdout,
    "stderr": res.stderr,
    "sandbox_files_under_src": sandbox_modules,
    "validate_py_hardcoded_repo_path": "/home/user/miniReason",
    "evidence_repo_files_contains_needed_paths": evidence_repo,
}
(OUT / "env-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
