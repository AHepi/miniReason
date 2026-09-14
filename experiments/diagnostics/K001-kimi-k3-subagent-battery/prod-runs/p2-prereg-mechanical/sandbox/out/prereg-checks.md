# Mechanical consistency checks — L001 pre-registration bundle

All results below were produced by computation over the sandbox bytes (scripts under `check/`, raw per-check outputs alongside this file). Nothing is transcribed from memory; each section ends PASS, FAIL (with evidence) or NOT-CHECKABLE (with why). No overall score is given.

Sandbox contents checked: `loop-prereg/{PREREG.md, VALIDATION.md, config.json, obligations.json, reading_set.json, calibration.json, validate.py}`; `src/minireason/data/endpoints.json`; `evidence/repo-files.txt (7885 tracked paths)`; `AGENTS.md`.

## 1. `python3 loop-prereg/validate.py` — run the bundle validator

**Command (sandbox root, process CWD):** `python3 loop-prereg/validate.py` — **exit code 1**

Standard output, verbatim (empty):```

```
Standard error, verbatim:```
Traceback (most recent call last):
  File "/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/kimi/prod-runs/p2-prereg-mechanical/sandbox/loop-prereg/validate.py", line 8, in <module>
    from minireason.loop.types import LoopConfig, loop_plan_id, LoopError, CONFIG_SCHEMA
ModuleNotFoundError: No module named 'minireason.loop'
```
Retried from inside the bundle (`python3 validate.py (cwd=loop-prereg/)`) after the path-shaped failure: **exit code 1**, identical `ModuleNotFoundError` on the same line 8 before any path is touched:
```
Traceback (most recent call last):
  File "/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/kimi/prod-runs/p2-prereg-mechanical/sandbox/loop-prereg/validate.py", line 8, in <module>
    from minireason.loop.types import LoopConfig, loop_plan_id, LoopError, CONFIG_SCHEMA
ModuleNotFoundError: No module named 'minireason.loop'
```
**Why it cannot run in this sandbox (mechanically determined):**

- The sandbox's entire `src/` tree is: `['src/minireason/data/endpoints.json']` — there is no `minireason.loop` package (nor `minireason/__init__.py`), so the import at line 8 fails before any path argument matters.
- `validate.py` also hardcodes `REPO = Path("/home/user/miniReason")` and would additionally read these published files, none present in the sandbox:
  - `src/minireason/data/endpoints.json (present in sandbox)`
  - `experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14/use-table-golden/use_table.json (NOT in sandbox)`
  - `experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14/use-table-full/use_table.json (NOT in sandbox)`
  - `experiments/diagnostics/C001-contrast-triple/occurrence-02/comparison.json (NOT in sandbox)`
- It imports ``minireason.loop.types`, `minireason.loop.standard`, `minireason.loop.receipts`, `deepreason_core.canonical``; none is in the sandbox.

> **FAIL** (exit code 1; verifier does not run in this environment — reproduced from both working directories; verbatim output above and in `out/check1/`)

## 2. Bundle file sha256 vs every sha256-looking value in PREREG.md / VALIDATION.md / config.json

Actual sha256 of every bundle file (plus `validate.py`, `VALIDATION.md` for completeness), computed here:

| file | actual sha256 | pinned in VALIDATION.md §4 | match |
|---|---|---|---|
| `config.json` | `081dd939663156aa3969f3b000fcb0ca4b07086ab4340b0156057903b45b5110` | `46495a6fa0ee5667b6ba5128adbaee9062ed5b6637310bb44b12efdf14c0da90` | **NO — MISMATCH** |
| `obligations.json` | `2913693abce664af387f1683c7cbfd622043a697343a6d415d89a8179d3652d6` | `2913693abce664af387f1683c7cbfd622043a697343a6d415d89a8179d3652d6` | **yes** |
| `reading_set.json` | `ef8c62a5ad6148c4bf676fadabba1ae0504babef26b4f793cce7d80ff37c728e` | `ef8c62a5ad6148c4bf676fadabba1ae0504babef26b4f793cce7d80ff37c728e` | **yes** |
| `calibration.json` | `9ca9ad04672e99becc19096e3de4d4010d9f21c700a979695ef034f9c19aae95` | `9ca9ad04672e99becc19096e3de4d4010d9f21c700a979695ef034f9c19aae95` | **yes** |
| `PREREG.md` | `c04c2092f672b52572ea98a60575e3405c5072f6b381b9b55a30cb3f7dcd16d6` | `c04c2092f672b52572ea98a60575e3405c5072f6b381b9b55a30cb3f7dcd16d6` | **yes** |
| `validate.py` | `fd8015261e86cf34cf87f1fd576fd28fb98cc635a7889ee7cb63cb5dde41f25e` | `fd8015261e86cf34cf87f1fd576fd28fb98cc635a7889ee7cb63cb5dde41f25e` | **yes** |
| `VALIDATION.md` | `62f2b71a90488852ed1b4e4af17138e22b77f60c31c0fb222326b085d257c413` | — (no pin; VALIDATION.md pins no digest for itself) | n/a |

All 64-hex tokens found in the three documents: **9** distinct values. `config.json` contains **no** sha256-looking token at all. Tokens matching a bundle file's actual digest:

- `2913693abce664af387f1683c7cbfd622043a697343a6d415d89a8179d3652d6` — in VALIDATION.md line(s) [109] — matches **obligations.json** ✔
- `9ca9ad04672e99becc19096e3de4d4010d9f21c700a979695ef034f9c19aae95` — in VALIDATION.md line(s) [107] — matches **calibration.json** ✔
- `c04c2092f672b52572ea98a60575e3405c5072f6b381b9b55a30cb3f7dcd16d6` — in VALIDATION.md line(s) [106] — matches **PREREG.md** ✔
- `ef8c62a5ad6148c4bf676fadabba1ae0504babef26b4f793cce7d80ff37c728e` — in VALIDATION.md line(s) [110] — matches **reading_set.json** ✔
- `fd8015261e86cf34cf87f1fd576fd28fb98cc635a7889ee7cb63cb5dde41f25e` — in VALIDATION.md line(s) [111] — matches **validate.py** ✔

Tokens matching **no** file in the bundle (4), and what the surrounding text says each pins:

- `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927`
  - PREREG.md:150 (obligation p1): 'the H005 occurrence-01 `material_sha256` equals 24ca4552<...>' — pins published repo file experiments/diagnostics/H005-open-prose-commitments/occurrence-01/material.json; not in the sandbox, not verifiable here.
- `328b9452c66fed52203015c540652d3b8ad3107d44dece56b55ebe721da341c8`
  - PREREG.md:40: 'C001 (`plan_id 328b9452<...>`)' — pins the frozen C001 study plan_id; not a file of this bundle; not verifiable here (only 3/7885 tracked files are in the sandbox).
- `46495a6fa0ee5667b6ba5128adbaee9062ed5b6637310bb44b12efdf14c0da90`
  - VALIDATION.md:108, §4 table row '| `config.json` | `46495a6f<...>` |' — said to pin config.json; the sandbox copy hashes to 081dd939<...>, so the recorded digest does NOT match the file delivered with the bundle.
- `713119a7cd255296058b18084a40cbac7a3353903bbf8cd260b6e78c173e4302`
  - PREREG.md:105: 'obligations.json is pinned at sha256 713119a7<...> before cycle 1'; VALIDATION.md:65: same value as the digest that 'reproduces over canonical bytes'. It pins the CANONICAL STRUCTURE of obligations.json, not its raw bytes (raw bytes hash to 2913693a<...>). Recomputed over canonical bytes by computation: it does reproduce.

**Canonical-digest cross-check (by computation):** the obligations pin `713119a7cd255296058b18084a40cbac7a3353903bbf8cd260b6e78c173e4302` does **reproduce** over `json.dumps(document_without_the_two_digest_keys, ensure_ascii=False, sort_keys=True, separators=(",", ":"))` (recomputed: `713119a7cd255296058b18084a40cbac7a3353903bbf8cd260b6e78c173e4302` — equal), and the pin appears verbatim in PREREG.md (True) and VALIDATION.md (True). So PREREG's obligations pin is sound — it pins canonical structure, while VALIDATION's §4 table pins raw bytes; both pins are self-consistent for `obligations.json`.

**Forensics on the `config.json` mismatch (by computation):** valid UTF-8, LF-only (109 LF, 0 CR), ends with newline, 6362 bytes; json.loads round-trip is byte-identical to the sandbox copy. No tested byte-level variant (LF/CRLF/CR, trailing-newline on/off, reserialization, canonical form) reproduces the pinned digest — `False` — so the pinned value cannot be located from the sandbox copy alone. Corroboration from bytes, not inference: VALIDATION.md §2's transcript shows validate.py PASS lines referencing a run directory experiments/loops/L001-loop-first-live-2026-09-14/ and loop_plan_id values — and evidence/repo-files.txt contains no L001/loop-prereg path at all, and contains no src/minireason/loop/ module.

> **FAIL** — one of six pinned digests fails to match: `config.json` pins `46495a6f…` in VALIDATION.md §4 but the file delivered with the bundle hashes to `081dd939663156aa3969f3b000fcb0ca4b07086ab4340b0156057903b45b5110`. The other five pinned digests match; the four non-table tokens are accounted for above (2 external pins, 1 canonical-structure pin that reproduces, 1 mismatching raw-bytes pin).

## 3. Seats in config.json vs `src/minireason/data/endpoints.json`

Every seat in `config.json` looked up in the registry (config carries only the endpoint name; family/key_env/timeout read from the registry):

| role | endpoint `name` | in registry | registry `family` | registry `key_env` | `timeout_seconds` |
|---|---|---|---|---|---|
| critic | `ollama/kimi-k3` | True | `ollama-cloud/kimi` | `OLLAMA_API_KEY` | 180 |
| defender | `ollama/gemma4-31b` | True | `ollama-cloud/gemma` | `OLLAMA_API_KEY` | 180 |
| variator | `deepseek-flash` | True | `deepseek` | `DEEPSEEK_API_KEY` | 180 |
| judge-1 | `ollama/gpt-oss-120b` | True | `ollama-cloud/gpt-oss` | `OLLAMA_API_KEY` | 180 |
| judge-2 | `ollama/qwen3.5-397b` | True | `ollama-cloud/qwen` | `OLLAMA_API_KEY` | 180 |

- Mismatches (endpoint absent, or family/key_env differing): **[]** — none.
- PREREG.md's seat table (lines 64–68), extracted cell-by-cell, matches the registry on name/family/key_env/timeout: **True**.
- Two judge seats sharing a family: **False** — judge-1 `ollama/gpt-oss-120b` → `ollama-cloud/gpt-oss`, judge-2 `ollama/qwen3.5-397b` → `ollama-cloud/qwen` (distinct).
- Distinct families over the five seats: **5**; critic (`ollama-cloud/kimi`) in neither judge family; defender (`ollama-cloud/gemma`) ≠ critic and in neither judge family; variator (`deepseek`) ≠ all four.

> **PASS** — no seat/family/key_env mismatch; judge seats do not share a family.

## 4. `max_calls` arithmetic vs reading-set size and cycle budget

- `reading_set.json` entries: **38** (size block: {'total': 38, 'c001_mark_cells': 16, 'h005_rows': 22}); `config.reading_set`: **38** keys.
- Per-leg check: `c001-mark (baseline)` = 4×0 = 0 (consistent); `c001-mark (cross-case)` = 12×9 = 108 (consistent); `h005-row` = 22×11 = 242 (consistent); `audit window` = 1×46 = 46 (consistent); `dispatch (S4-S7 runner v2)` = 0×0 = 0 (consistent).
- Recomputed: **4x0 + 12x9 + 22x11 + 1x46 + 0 = 0 + 108 + 242 + 46 + 0 = 396 == config.max_calls == 396; cycle_budget 3 == PREREG clause 5's 3 and reading_set audit-window cycle (2) satisfies 2 mod audit.period(2) == 0 within cycles 1..3**
- `max_calls_derivation.max_calls` = 396; `config.max_calls` = 396; leg subtotal sum = 396 — all equal: **True**.
- Per-entry `budgeted_calls` sums: 16 c001-mark entries → 108; 22 h005-row entries → 242 (total 350, the remaining 46 being the audit-window leg with no reading-set entry).
- Component check: guarded h005 row 1+1+2+2+1+4 = 11 (declared worst case 11); c001 mark 2+2+1+4 = 9 (declared 9); audit window components recomputed {'calibration_9x2': 18, 'paraphrase_4_plus_2x2x4': 20, 'premise_deletion_2x4': 8, 'ensemble_disagreement': 0} → 46 (declared 46).
- Cycle budget: `config.cycle_budget` = 3; the audit-window leg's own "why" declares the single due cycle as cycle 2 (2 mod `audit.period`=2 == 0 within cycles 1..3).
- The sentence in PREREG.md that gives the derivation's result (quoted, lines 126–128):
  > '5. Else, cycle index equals `cycle_budget` = 3, or `max_calls` = 396 is reached ⇒ STOP `resource_boundary` — a declared attention-and-spend boundary, never an adjudication and never the inquiry running out of things to say.'
- The derivation itself lives in reading_set.json max_calls_derivation block (per-entry budgeted_calls and per-leg subtotals); PREREG.md states the result values but no derivation sentence of its own. Its stated `arithmetic` string: "0 + 108 + 242 + 46 + 0 = 396". A deliberate deviation from the design's prose is declared in the same block (§9.1's 'roughly nine calls' vs the strict 11): "§9.1 estimates 'roughly nine calls' for a fully guarded row. That prose estimate does not say whether each paraphrase is re-ruled by both judge seats. This pre-registration declares the strict reading - both seats re-rul…"

> **PASS** — 0 + 108 + 242 + 46 + 0 = 396 == `config.max_calls`; `cycle_budget` = 3 matches PREREG clause 5; entry counts 38 = 16 + 22 match the size block.

## 5. Obligations: O/P counts, id uniqueness, cross-references

- `obligations.json` carries **19** obligations: **|O| = 7** (o1, o2, o3, o4, o5, o6, o7), **|P| = 12** (p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12).
- PREREG.md states (line 10): “the failed set **O** (7) and the protected set **P** (12)” — match: **True**. (VALIDATION.md §2's validator output independently claims `|O|=7 |P|=12`, consistent but not independently re-runnable — see check 1.)
- Duplicate ids: **none**; ids unique: **True**.
- Obligation-id tokens referenced from `config.json`: ['o1', 'o2', 'o3'] — all exist: True. (Those three hits are the `h005-row/`/`c001-mark/` row keys inside its `reading_set` list, not obligation references; config.json names no obligation id field. It points at the obligations file via `obligations_path` ending in `/obligations.json`.)
- Obligation-id tokens in PREREG.md: all of o1–o7 and p1–p12 occur; every one exists in obligations.json — missing: **[]**; obligation ids not referenced by token anywhere in PREREG.md: **[]**.
- The `obligations_sha256` self-digest is present and reproduces over canonical bytes (check 2); PREREG.md §3 pins `obligations.json` with that same digest (line 105).

> **PASS** — |O|=7, |P|=12 exactly as stated; all 19 ids unique; every referenced id exists.

## 6. File paths referenced by calibration.json / reading_set.json vs the tracked-file list

`evidence/repo-files.txt` has **7885** tracked paths (stated in AGENTS-adjacent tooling as read-only `git ls-files` output). Every path appearing in a `file` / `source_file` / `rendered_in` field of `calibration.json` and `reading_set.json` was looked up exactly:

| referenced path | where | in repo-files.txt |
|---|---|---|
| `experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14/use-table-golden/use_table.json` | calibration.json | True |
| `experiments/diagnostics/C001-contrast-triple/occurrence-02/comparison.json` | calibration.json | True |
| `experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14/use-table-golden/USE_TABLE.md` | reading_set.json | True |
| `experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14/use-table-golden/use_table.json` | reading_set.json | True |
| `experiments/diagnostics/C001-contrast-triple/occurrence-02/COMPARISON.md` | reading_set.json | True |
| `experiments/diagnostics/C001-contrast-triple/occurrence-02/comparison.json` | reading_set.json | True |

Missing paths: **none**. (Their bytes are not in the sandbox — listing only; content verification is check-1-blocked. The four `source_file` sha256 values in calibration.json's rows and the record/banner digests cannot be re-verified here.)

> **PASS** — all 4 distinct referenced paths are tracked files; zero missing.

## 7. The six-value reading vocabulary

- Claim: PREREG.md lines 46 and 201: the run closes `use_relation_h005.ROOT_READING_VOCABULARY` 'to six values'; obligations o1 names the member set only as `standard.NOMINABLE_RELATIONS`.
- A vocabulary list in any bundle JSON (`*.vocab*` key): **[]** — none. `config.json`'s top-level keys are: `audit`, `contrast`, `cycle_budget`, `graph_root`, `max_calls`, `max_per_key`, `obligations_path`, `occurrences`, `provider_mode`, `publish_ref`, `reading_set`, `reopen_reasons`, `run_id`, `runner`, `schema`, `seats`, `study`, `timeouts`.
- Relation strings present anywhere in the bundle: ['rejects-with-reason', 'retains'] (only 2 of the promised 6 values appear anywhere in the bundle, as calibration ground-truth strings).
- Where the enumerated list actually lives: src/minireason/use_relation_h005.py is a tracked repo file (evidence/repo-files.txt line 7684) but is not in the sandbox; standard.NOMINABLE_RELATIONS lives in src/minireason/loop/standard.py which is absent from the tracked file list entirely (grep of evidence/repo-files.txt).
- Why not checkable: No file in the sandbox carries the six-value list, so bytes cannot be compared against bytes. The claim that the closed vocabulary has exactly six values is asserted in prose in three places and enumerable in none.

> **NOT-CHECKABLE** — PREREG.md asserts 'closes it to six values' but no file in the bundle (or sandbox) enumerates the six values; the defining modules are absent, so bytes cannot be compared against the claim.

## 8. Credential scan over every file in the sandbox

- Patterns: `sk-[0-9a-f]{32}` and `[0-9a-f]{32}\.[A-Za-z0-9_-]{20,}`.
- Files scanned: **34** (every regular file in the sandbox, including this task's own `check/` scripts and `out/` products, which are where the pattern strings themselves live).
- Hits: **0** → [] (only path + line number would be reported; zero hits, so nothing withheld).
- Separately, endpoint key names appear only as names: `DEEPSEEK_API_KEY` and `OLLAMA_API_KEY` occur only in `key_env` fields / prose; no `=`-assignment or `sk-`-prefixed value accompanies them (no line in any file matches either pattern).

> **PASS** — zero credential-shaped hits over all 34 files.

## 9. Every date / run-id string in the bundle (stale-run-id sweep)

Distinct calendar dates across the seven bundle files: **['2026-09-14']**. Distinct date/run-id–shaped strings: **5**.

| string | appears in |
|---|---|
| `2026-09-14` | `PREREG.md` lines [4, 38, 154, 157, 160, 209]; `VALIDATION.md` lines [21, 45]; `calibration.json` lines [3, 6, 46, 67, 73, 94, 100, 131]…; `config.json` lines [3, 52, 53]; `obligations.json` lines [3, 9, 10, 32, 33, 46, 47, 60]…; `reading_set.json` lines [3, 379, 381, 408, 410, 437, 439, 466]…; `validate.py` lines [105, 152] |
| `2026-09-14T00:00:00Z` | `PREREG.md` lines [34] |
| `L001-loop-first-live-2026-09-14` | `PREREG.md` lines [4, 38, 154, 157, 160, 209]; `VALIDATION.md` lines [21, 45]; `calibration.json` lines [3]; `config.json` lines [3, 52, 53]; `obligations.json` lines [3, 32, 33, 46, 47, 60, 61, 74]…; `reading_set.json` lines [3] |
| `REC-20260914-Z` | `PREREG.md` lines [34] |
| `snapshot-2026-09-14` | `calibration.json` lines [6, 46, 67, 73, 94, 100, 131, 137]…; `obligations.json` lines [9, 10]; `reading_set.json` lines [379, 381, 408, 410, 437, 439, 466, 468]…; `validate.py` lines [105, 152] |

- single run id L001-loop-first-live-2026-09-14 in all 6 files that carry one; every date-like string in the bundle is the single calendar date 2026-09-14; declared placeholder REC-20260914-Z at 2026-09-14T00:00:00Z (PREREG.md §1 declares both as placeholders); no stale or second run id / date found.
- AGENTS.md outside the bundle references REC-20260913 (2026-09-13) in an erratum filename — unrelated to the L001 run, listed for completeness only.

> **PASS** — one run id and one calendar date throughout; the only deviant strings are the self-declared placeholders; no stale run id or date in the bundle.

## What these checks cannot establish

- Anything requiring the absent repository tree: the full validate.py run, its PASS transcript in VALIDATION.md (reproducibility claim), the content of the six-value vocabulary, BLOCK_CODES, MARKS, the frozen CEILING_TEXT/PREREGISTRATION_REQUIRED_SENTENCES, and every pinned digest of a published file (C001 plan_id, material_sha256, calibration source bytes). The tracked file list shows the pins' targets exist in the repo; nothing here can verify their bytes.
- Whether experiments/loops/L001-loop-first-live-2026-09-14/ was ever created in the real repository — evidence/repo-files.txt contains no L001 path, but this bundle describes itself as pre-dispatch ('the run directory ... does not yet exist'), and a git ls-files snapshot cannot distinguish 'run never executed' from 'run executed but outputs not committed'. VALIDATION.md's own transcript, however, references the run directory and minted plan artifacts.
- Which of the two config.json byte strings is authentic, or where the divergence entered (staging clone vs copy step); the sandbox holds one side only.
- Whether the stated canonicalization recipe equals deepreason_core.canonical.canonical_json / minireason.provider.digest byte-for-byte (the modules are absent); only the equivalence of the recipe as written with the recorded obligations digest was recomputed.
- Whether the sandbox copy itself is byte-identical to what an external reviewer received via any other channel (no second copy is available to compare); all claims here are internal to the sandbox.
- Intent, motivation, or provenance of the mismatch — only that the bytes differ from the recorded digest.
- The semantic adequacy of the design (guard soundness, clause meanings, whether obligations say what the prose claims they mean). Only stated mechanical relations were checked, per the task's instruction to check bytes against bytes, not judge the design.
- Credential hygiene outside the sandbox, key validity, or whether names DEEPSEEK_API_KEY/OLLAMA_API_KEY resolve to anything.

---
*Generated by `check/render_md.py` from `out/prereg-checks.json`, which was assembled by `check/render_json.py` from the raw outputs of `check/check01…check09`. Raw evidence preserved under `out/` (per-check JSON) and `out/check1/` (verbatim validator output). No overall score, per task.*
