"""Run unittest discovery over tests/loop with src on sys.path.

Writes the full output, the final "Ran N tests in Xs" line, the verdict
and any failure/error test ids to out/test-run.txt.
"""
import io
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
os.chdir(ROOT)

buf = io.StringIO()
suite = unittest.TestLoader().discover(
    start_dir=os.path.join(ROOT, "tests", "loop"),
    pattern="test*.py",
    top_level_dir=ROOT,
)
runner = unittest.TextTestRunner(stream=buf, verbosity=1)
result = runner.run(suite)
output = buf.getvalue()

ran_line = ""
for line in output.splitlines():
    if line.startswith("Ran "):
        ran_line = line
verdict = "OK" if result.wasSuccessful() else "FAILED"

problem_ids = [test.id() for test, _ in result.failures]
problem_ids += [test.id() for test, _ in result.errors]

os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
with open(os.path.join(ROOT, "out", "test-run.txt"), "w", encoding="utf-8") as fh:
    fh.write("command: python3 -X utf8 -m unittest discover -s tests/loop -t . "
             "(via check/run_loop_tests.py with src on sys.path)\n")
    fh.write("\n--- unittest output ---\n")
    fh.write(output)
    fh.write("\n--- summary ---\n")
    fh.write(ran_line + "\n")
    fh.write(verdict + ("\n" if not problem_ids else
             " ({} failures/errors)\n".format(len(problem_ids))))
    if problem_ids:
        fh.write("\nfailed/errored test ids:\n")
        for tid in problem_ids:
            fh.write(tid + "\n")

with open(os.path.join(ROOT, "check", "_test_summary.json"), "w", encoding="utf-8") as fh:
    json.dump({"ran_line": ran_line, "verdict": verdict,
               "problem_ids": problem_ids}, fh, indent=2)
    fh.write("\n")

print(ran_line)
print(verdict, "problems:", len(problem_ids))
sys.exit(0 if result.wasSuccessful() else 1)
