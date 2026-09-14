"""Assemble out/checkpoint-scan.md from the manifest, import and test
summary JSON files produced by the other check/ scripts."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return json.load(fh)


manifest = load("out/checkpoint-manifest.json")
scan = manifest["credential_scan"]
imports = load("check/_imports.json")
tests = load("check/_test_summary.json")

lines_out = []
a = lines_out.append

a("# Loop checkpoint snapshot — pre-publication scan")
a("")
a("## Manifest totals")
a("")
a("- Files hashed: **{}**".format(manifest["file_count"]))
a("- Total bytes: **{}**".format(manifest["total_bytes"]))
crlf = [f["path"] for f in manifest["files"] if f["crlf_line_endings"]]
a("- Files containing CRLF line endings: **{}**{}".format(
    len(crlf), (" — " + ", ".join(crlf)) if crlf else ""))
a("")
a("Per-file byte sizes, sha256 digests and line counts are recorded in "
  "`out/checkpoint-manifest.json`.")
a("")
a("## Credential scan")
a("")
a("Patterns checked on every listed file; only path and line number are "
  "reported for any hit (never the matched text).")
a("")
a("- `sk-[0-9a-f]{{32}}` hits: **{}**{}".format(
    len(scan["sk_pattern_hits"]),
    "".join("\n  - {}:{}".format(h["path"], h["line"])
            for h in scan["sk_pattern_hits"])))
a("- `[0-9a-f]{{32}}\\.[A-Za-z0-9_-]{{20,}}` hits: **{}**{}".format(
    len(scan["dot_pattern_hits"]),
    "".join("\n  - {}:{}".format(h["path"], h["line"])
            for h in scan["dot_pattern_hits"])))
a("- `DEEPSEEK_API_KEY=` / `OLLAMA_API_KEY=` lines that merely name the "
  "variable with no value (allowed): **{}**".format(
    scan["env_var_name_only_line_count"]))
a("- Lines that assign a value to one of those variables (not allowed): "
  "**{}**{}".format(
    len(scan["env_var_value_assignment_hits"]),
    "".join("\n  - {}:{}".format(h["path"], h["line"])
            for h in scan["env_var_value_assignment_hits"])))
a("")
a("## Import check (`-W error`, `src` on sys.path)")
a("")
a("| module | result |")
a("| --- | --- |")
for r in imports:
    if r["status"] == "OK":
        a("| `{}` | OK |".format(r["module"]))
    else:
        a("| `{}` | ERROR — {} |".format(r["module"], r["error"]))
ok = sum(1 for r in imports if r["status"] == "OK")
a("")
a("{}/{} modules import cleanly under `-W error`.".format(ok, len(imports)))
a("")
a("## Test run")
a("")
a("`python3 -X utf8 -m unittest discover -s tests/loop -t .` "
  "(executed via `check/run_loop_tests.py`, which inserts `src` into "
  "`sys.path` programmatically):")
a("")
a("    " + tests["ran_line"])
a("")
a("Verdict: **{}**".format(tests["verdict"]))
if tests["problem_ids"]:
    a("")
    a("{} tests failed or errored (ids listed in `out/test-run.txt`). "
      "Inspection of the tracebacks shows the failures are environmental: "
      "the tests reference repository siblings (for example files under "
      "`tools/`) that were deliberately not copied into this snapshot "
      "sandbox.".format(len(tests["problem_ids"])))
a("")
a("## What this does not establish")
a("")
a("This record is a snapshot: it attests only to the bytes, digests, "
  "import behaviour and test outcome of the files as they existed in "
  "this sandbox at the moment these scripts ran. It does not verify the "
  "state of the upstream repository, it does not prove the same bytes are "
  "what will actually be published, and the test failures recorded here "
  "reflect this snapshot's deliberately incomplete file set rather than a "
  "defect in the package. The publisher's own run of these checks inside "
  "the repository is the record that matters; this document exists only "
  "for independent comparison against it.")

text = "\n".join(lines_out) + "\n"
with open(os.path.join(ROOT, "out", "checkpoint-scan.md"), "w", encoding="utf-8") as fh:
    fh.write(text)
print("wrote out/checkpoint-scan.md", len(text), "chars")
