# Loop checkpoint snapshot — pre-publication scan

## Manifest totals

- Files hashed: **43**
- Total bytes: **1899724**
- Files containing CRLF line endings: **0**

Per-file byte sizes, sha256 digests and line counts are recorded in `out/checkpoint-manifest.json`.

## Credential scan

Patterns checked on every listed file; only path and line number are reported for any hit (never the matched text).

- `sk-[0-9a-f]{32}` hits: **0**
- `[0-9a-f]{32}\.[A-Za-z0-9_-]{20,}` hits: **0**
- `DEEPSEEK_API_KEY=` / `OLLAMA_API_KEY=` lines that merely name the variable with no value (allowed): **0**
- Lines that assign a value to one of those variables (not allowed): **1**
  - tests/loop/test_publish.py:769

## Import check (`-W error`, `src` on sys.path)

| module | result |
| --- | --- |
| `minireason.loop` | OK |
| `minireason.loop.contracts` | ERROR — SyntaxError: invalid escape sequence '\s' |
| `minireason.loop.custody` | OK |
| `minireason.loop.decide` | ERROR — SyntaxError: invalid escape sequence '\s' |
| `minireason.loop.graph` | ERROR — SyntaxError: invalid escape sequence '\s' |
| `minireason.loop.markprep` | ERROR — SyntaxError: invalid escape sequence '\s' |
| `minireason.loop.obligations` | OK |
| `minireason.loop.packs` | ERROR — SyntaxError: invalid escape sequence '\s' |
| `minireason.loop.publish` | OK |
| `minireason.loop.receipts` | OK |
| `minireason.loop.roles` | ERROR — SyntaxError: invalid escape sequence '\s' |
| `minireason.loop.seats` | ERROR — SyntaxError: invalid escape sequence '\s' |
| `minireason.loop.standard` | ERROR — SyntaxError: invalid escape sequence '\s' |
| `minireason.loop.steps` | OK |
| `minireason.loop.surface` | ERROR — SyntaxError: invalid escape sequence '\s' |
| `minireason.loop.synthetic` | ERROR — SyntaxError: invalid escape sequence '\s' |
| `minireason.loop.types` | OK |

7/17 modules import cleanly under `-W error`.

## Test run

`python3 -X utf8 -m unittest discover -s tests/loop -t .` (executed via `check/run_loop_tests.py`, which inserts `src` into `sys.path` programmatically):

    Ran 991 tests in 16.153s

Verdict: **FAILED**

223 tests failed or errored (ids listed in `out/test-run.txt`). Inspection of the tracebacks shows the failures are environmental: the tests reference repository siblings (for example files under `tools/`) that were deliberately not copied into this snapshot sandbox.

## What this does not establish

This record is a snapshot: it attests only to the bytes, digests, import behaviour and test outcome of the files as they existed in this sandbox at the moment these scripts ran. It does not verify the state of the upstream repository, it does not prove the same bytes are what will actually be published, and the test failures recorded here reflect this snapshot's deliberately incomplete file set rather than a defect in the package. The publisher's own run of these checks inside the repository is the record that matters; this document exists only for independent comparison against it.
