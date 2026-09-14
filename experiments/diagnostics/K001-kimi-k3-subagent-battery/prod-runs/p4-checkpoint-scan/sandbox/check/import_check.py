"""Import every src/minireason/loop/*.py module with warnings-as-errors.

Runs each import in a subprocess equivalent to
python3 -W error -c "import sys; sys.path.insert(0,'src'); import minireason.loop.<name>"
and records OK or the first line of the error. Writes check/_imports.json.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOOP_DIR = os.path.join(ROOT, "src", "minireason", "loop")

modules = sorted(
    name[:-3]
    for name in os.listdir(LOOP_DIR)
    if name.endswith(".py") and name != "__init__.py"
)
modules = ["__init__"] + modules  # package itself first

results = []
for mod in modules:
    target = "minireason.loop" if mod == "__init__" else "minireason.loop." + mod
    code = "import sys; sys.path.insert(0, 'src'); import " + target
    proc = subprocess.run(
        [sys.executable, "-W", "error", "-c", code],
        cwd=ROOT, capture_output=True, text=True,
    )
    if proc.returncode == 0:
        results.append({"module": target, "status": "OK"})
    else:
        err = (proc.stderr or proc.stdout or "").strip().splitlines()
        first = err[-1] if err else "unknown error"
        results.append({"module": target, "status": "ERROR", "error": first})

with open(os.path.join(ROOT, "check", "_imports.json"), "w", encoding="utf-8") as fh:
    json.dump(results, fh, indent=2)
    fh.write("\n")

ok = sum(1 for r in results if r["status"] == "OK")
print("imported OK:", ok, "/", len(results))
for r in results:
    if r["status"] != "OK":
        print(r["module"], "->", r["error"])
