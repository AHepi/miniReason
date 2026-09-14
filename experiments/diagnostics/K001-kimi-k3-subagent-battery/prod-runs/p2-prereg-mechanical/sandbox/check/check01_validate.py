"""Check 1: run loop-prereg/validate.py from the sandbox root, verbatim capture."""
import json
import subprocess
import sys
from pathlib import Path

OUT = Path("out/check1")
OUT.mkdir(parents=True, exist_ok=True)

res = subprocess.run(
    ["python3", "loop-prereg/validate.py"],
    capture_output=True, text=True, timeout=300,
)
(OUT / "validate.stdout.txt").write_text(res.stdout, encoding="utf-8")
(OUT / "validate.stderr.txt").write_text(res.stderr, encoding="utf-8")

report = {
    "cwd": "sandbox root (process CWD)",
    "command": "python3 loop-prereg/validate.py",
    "exit_code": res.returncode,
    "stdout_file": "out/check1/validate.stdout.txt",
    "stderr_file": "out/check1/validate.stderr.txt",
    "stdout": res.stdout,
    "stderr": res.stderr,
}
print(json.dumps({k: v for k, v in report.items() if k not in ("stdout", "stderr")},
                 indent=2))
print("--- STDOUT (verbatim) ---")
print(res.stdout)
print("--- STDERR (verbatim) ---")
print(res.stderr)
