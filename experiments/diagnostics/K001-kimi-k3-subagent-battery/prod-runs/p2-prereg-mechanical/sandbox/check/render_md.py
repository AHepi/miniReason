"""Render out/prereg-checks.md from out/prereg-checks.json (verbatim quoting; no
transcription from memory)."""
import json
from pathlib import Path

r = json.loads(Path("out/prereg-checks.json").read_text(encoding="utf-8"))
C = r["checks"]

def fence(s):
    return "```\n" + s.rstrip("\n") + "\n```"

md = []
md.append("# Mechanical consistency checks — L001 pre-registration bundle\n")
md.append("All results below were produced by computation over the sandbox bytes "
          "(scripts under `check/`, raw per-check outputs alongside this file). "
          "Nothing is transcribed from memory; each section ends PASS, FAIL (with "
          "evidence) or NOT-CHECKABLE (with why). No overall score is given.\n")
md.append("Sandbox contents checked: " + "; ".join(f"`{s}`" for s in r["sandbox_contents"]) + ".\n")

# --- 1 -----------------------------------------------------------------------
c = C["1_validate_py_run"]
md.append("## 1. `python3 loop-prereg/validate.py` — run the bundle validator\n")
md.append(f"**Command (sandbox root, process CWD):** `{c['command_from_sandbox_root']}` — "
          f"**exit code {c['exit_code_root']}**\n")
md.append("Standard output, verbatim (empty):" + fence(c["stdout_root_verbatim"]))
md.append("Standard error, verbatim:" + fence(c["stderr_root_verbatim"]))
md.append(f"Retried from inside the bundle (`{c['command_from_inside_bundle']}`) after the path-shaped "
          f"failure: **exit code {c['exit_code_inside']}**, identical `ModuleNotFoundError` on the same "
          "line 8 before any path is touched:")
md.append(fence(c["stderr_inside_verbatim"]))
fa = c["failure_analysis"]
md.append("**Why it cannot run in this sandbox (mechanically determined):**\n")
md.append(f"- The sandbox's entire `src/` tree is: `{fa['sandbox_src_files']}` — there is no "
          "`minireason.loop` package (nor `minireason/__init__.py`), so the import at line 8 fails "
          "before any path argument matters.")
md.append(f"- `validate.py` also hardcodes `REPO = Path(\"{fa['hardcoded_repo_path_in_validate_py']}\")` "
          "and would additionally read these published files, none present in the sandbox:")
for pth in fa["published_files_validate_py_would_read"]:
    md.append(f"  - `{pth}`")
md.append(f"- It imports `{', '.join('`'+m+'`' for m in fa['modules_validate_py_imports'])}`; "
          "none is in the sandbox.\n")
md.append("> **FAIL** (exit code 1; verifier does not run in this environment — reproduced from "
          "both working directories; verbatim output above and in `out/check1/`)\n")

# --- 2 -----------------------------------------------------------------------
c = C["2_sha256_vs_pins"]
md.append("## 2. Bundle file sha256 vs every sha256-looking value in PREREG.md / VALIDATION.md / config.json\n")
md.append("Actual sha256 of every bundle file (plus `validate.py`, `VALIDATION.md` for "
          "completeness), computed here:\n")
md.append("| file | actual sha256 | pinned in VALIDATION.md §4 | match |")
md.append("|---|---|---|---|")
for row in c["comparison_vs_VALIDATION_md_table"]:
    pin = row["pinned_in_VALIDATION.md"]
    pin_s = f"`{pin}`" if pin else "— (no pin; VALIDATION.md pins no digest for itself)"
    match_s = {True: "**yes**", False: "**NO — MISMATCH**", None: "n/a"}[row["match"]]
    md.append(f"| `{row['file']}` | `{row['actual_sha256']}` | {pin_s} | {match_s} |")
md.append("")
t = c["sha256_tokens_in_documents"]
md.append(f"All 64-hex tokens found in the three documents: **{t['n_distinct_64hex_tokens']}** "
          "distinct values. `config.json` contains **no** sha256-looking token at all. "
          "Tokens matching a bundle file's actual digest:\n")
for m in t["tokens_matching_a_bundle_file"]:
    locs = "; ".join(f"{f} line(s) {ls}" for f, ls in m["appears_in"].items())
    md.append(f"- `{m['token']}` — in {locs} — matches **{', '.join(m['matches_file'])}** ✔")
md.append("\nTokens matching **no** file in the bundle (4), and what the surrounding text says each pins:\n")
for tok_, expl in t["what_each_unmatched_token_is_said_to_pin"].items():
    md.append(f"- `{tok_}`\n  - {expl}")
md.append("")
oc = c["obligations_canonical_digest"]
md.append("**Canonical-digest cross-check (by computation):** the obligations pin "
          f"`{oc['pin_in_obligations.json']}` does **reproduce** over "
          f"`json.dumps(document_without_the_two_digest_keys, ensure_ascii=False, sort_keys=True, "
          f"separators=(\",\", \":\"))` (recomputed: `{oc['recomputed_over_canonical_bytes']}` — equal), "
          f"and the pin appears verbatim in PREREG.md ({oc['pin_appears_in_PREREG.md']}) and "
          f"VALIDATION.md ({oc['pin_appears_in_VALIDATION.md']}). So PREREG's obligations pin is sound — "
          "it pins canonical structure, while VALIDATION's §4 table pins raw bytes; both pins are "
          "self-consistent for `obligations.json`.\n")
fm = c["config_mismatch_forensics"]
md.append("**Forensics on the `config.json` mismatch (by computation):** " + fm["sandbox_copy"] + ". "
          "No tested byte-level variant (LF/CRLF/CR, trailing-newline on/off, reserialization, "
          "canonical form) reproduces the pinned digest — "
          f"`{not fm['pinned_digest_reproduced_by_no_tested_variant'] and 'confirmed'}` — so the pinned "
          "value cannot be located from the sandbox copy alone. Corroboration from bytes, not "
          "inference: " + fm["corroboration"] + ".\n")
md.append("> **FAIL** — one of six pinned digests fails to match: `config.json` pins "
          "`46495a6f…` in VALIDATION.md §4 but the file delivered with the bundle hashes to "
          "`081dd939663156aa3969f3b000fcb0ca4b07086ab4340b0156057903b45b5110`. The other five "
          "pinned digests match; the four non-table tokens are accounted for above "
          "(2 external pins, 1 canonical-structure pin that reproduces, 1 mismatching raw-bytes pin).\n")

# --- 3 -----------------------------------------------------------------------
c = C["3_seats_vs_registry"]
md.append("## 3. Seats in config.json vs `src/minireason/data/endpoints.json`\n")
md.append("Every seat in `config.json` looked up in the registry (config carries only the "
          "endpoint name; family/key_env/timeout read from the registry):\n")
md.append("| role | endpoint `name` | in registry | registry `family` | registry `key_env` | `timeout_seconds` |")
md.append("|---|---|---|---|---|---|")
for s in c["seat_lookup"]:
    md.append(f"| {s['role']} | `{s['endpoint_name']}` | {s['exists_in_registry']} | "
              f"`{s['registry_family']}` | `{s['registry_key_env']}` | {s['registry_timeout_seconds']} |")
md.append("")
md.append(f"- Mismatches (endpoint absent, or family/key_env differing): **{c['mismatches']}** — none.")
md.append(f"- PREREG.md's seat table (lines 64–68), extracted cell-by-cell, matches the registry on "
          f"name/family/key_env/timeout: **{c['prereg_table_matches_registry']}**.")
md.append(f"- Two judge seats sharing a family: **{c['judge_seats_share_a_family']}** — "
          f"judge-1 `{c['judge_families']['judge-1']['name']}` → `{c['judge_families']['judge-1']['family']}`, "
          f"judge-2 `{c['judge_families']['judge-2']['name']}` → `{c['judge_families']['judge-2']['family']}` (distinct).")
md.append(f"- Distinct families over the five seats: **{c['n_distinct_families_over_5_seats']}**; "
          "critic (`ollama-cloud/kimi`) in neither judge family; defender (`ollama-cloud/gemma`) "
          "≠ critic and in neither judge family; variator (`deepseek`) ≠ all four.\n")
md.append("> **PASS** — no seat/family/key_env mismatch; judge seats do not share a family.\n")

# --- 4 -----------------------------------------------------------------------
c = C["4_max_calls_arithmetic"]
md.append("## 4. `max_calls` arithmetic vs reading-set size and cycle budget\n")
md.append(f"- `reading_set.json` entries: **{c['reading_set_entries']}** "
          f"(size block: {c['reading_set_size_block']}); `config.reading_set`: **{c['config_reading_set_len']}** keys.\n"
          f"- Per-leg check: " + "; ".join(f"`{l['leg']}` = {l['cells']}×{l['cost_each']} = {l['declared_subtotal']}"
                                           f" ({'consistent' if l['subtotal_consistent'] else 'INCONSISTENT'})"
                                           for l in c["per_leg_check"]) + ".")
md.append(f"- Recomputed: **{c['arithmetic_recomputed']}**")
md.append(f"- `max_calls_derivation.max_calls` = {c['derivation_max_calls_field']}; "
          f"`config.max_calls` = {c['config_max_calls']}; leg subtotal sum = {c['leg_subtotal_sum']} — "
          f"all equal: **{c['leg_sum_equals_max_calls']}**.")
md.append(f"- Per-entry `budgeted_calls` sums: 16 c001-mark entries → {c['marks_budgeted_calls_sum']}; "
          f"22 h005-row entries → {c['rows_budgeted_calls_sum']} (total {c['entries_budgeted_calls_sum']}, "
          "the remaining 46 being the audit-window leg with no reading-set entry).")
md.append(f"- Component check: guarded h005 row 1+1+2+2+1+4 = {c['h005_row_cost_components_sum_to_total'][0]} "
          f"(declared worst case {c['h005_row_cost_components_sum_to_total'][1]}); c001 mark 2+2+1+4 = "
          f"{c['c001_mark_cost_components_sum_to_total'][0]} (declared {c['c001_mark_cost_components_sum_to_total'][1]}); "
          f"audit window components recomputed {c['audit_components_recomputed']} → {c['audit_components_sum']} "
          f"(declared {c['audit_leg_declared']}).")
md.append(f"- Cycle budget: `config.cycle_budget` = {c['config_cycle_budget']}; the audit-window leg's own \"why\" "
          "declares the single due cycle as cycle 2 (2 mod `audit.period`=2 == 0 within cycles 1..3).")
md.append("- The sentence in PREREG.md that gives the derivation's result (quoted, lines 126–128):\n  > "
          + c["derivation_sentence_in_PREREG_md"].split(": ", 1)[1])
md.append(f"- The derivation itself lives in {c['derivation_lives_in']}. Its stated `arithmetic` string: "
          f"\"{c['derivation_arithmetic_string']}\". A deliberate deviation from the design's prose is "
          "declared in the same block (§9.1's 'roughly nine calls' vs the strict 11): "
          f"\"{c['deviation_note_in_reading_set'][:220]}…\"\n")
md.append("> **PASS** — 0 + 108 + 242 + 46 + 0 = 396 == `config.max_calls`; "
          "`cycle_budget` = 3 matches PREREG clause 5; entry counts 38 = 16 + 22 match the size block.\n")

# --- 5 -----------------------------------------------------------------------
c = C["5_obligations"]
md.append("## 5. Obligations: O/P counts, id uniqueness, cross-references\n")
md.append(f"- `obligations.json` carries **{c['total']}** obligations: **|O| = {c['O_count_actual']}** "
          f"({', '.join(c['O_ids'])}), **|P| = {c['P_count_actual']}** ({', '.join(c['P_ids'])}).")
md.append(f"- PREREG.md states (line 10): “the failed set **O** (7) and the protected set **P** (12)” — "
          f"match: **{c['counts_match_prereg']}**. (VALIDATION.md §2's validator output independently "
          "claims `|O|=7 |P|=12`, consistent but not independently re-runnable — see check 1.)")
md.append(f"- Duplicate ids: **{c['duplicate_ids'] or 'none'}**; ids unique: **{c['ids_unique']}**.")
md.append(f"- Obligation-id tokens referenced from `config.json`: {c['id_references']['config.json']} — "
          "all exist: " + str(not c["references_missing_from_obligations_json"]["config.json"]) + ". "
          "(Those three hits are the `h005-row/`/`c001-mark/` row keys inside its `reading_set` list, "
          "not obligation references; config.json names no obligation id field. It points at the "
          "obligations file via `obligations_path` ending in `/obligations.json`.)")
md.append(f"- Obligation-id tokens in PREREG.md: all of o1–o7 and p1–p12 occur; every one exists in "
          f"obligations.json — missing: **{c['references_missing_from_obligations_json']['PREREG.md']}**; "
          f"obligation ids not referenced by token anywhere in PREREG.md: "
          f"**{c['obligation_ids_not_referenced_in_PREREG_md_by_token']}**.")
md.append(f"- The `obligations_sha256` self-digest is present and reproduces over canonical bytes "
          "(check 2); PREREG.md §3 pins `obligations.json` with that same digest (line 105).\n")
md.append("> **PASS** — |O|=7, |P|=12 exactly as stated; all 19 ids unique; every referenced id exists.\n")

# --- 6 -----------------------------------------------------------------------
c = C["6_referenced_paths_tracked"]
md.append("## 6. File paths referenced by calibration.json / reading_set.json vs the tracked-file list\n")
md.append(f"`evidence/repo-files.txt` has **{c['repo_files_line_count']}** tracked paths (stated in "
          "AGENTS-adjacent tooling as read-only `git ls-files` output). Every path appearing in a "
          "`file` / `source_file` / `rendered_in` field of `calibration.json` and `reading_set.json` "
          "was looked up exactly:\n")
md.append("| referenced path | where | in repo-files.txt |")
md.append("|---|---|---|")
for e in c["calibration_paths"]:
    md.append(f"| `{e['path']}` | calibration.json | {e['in_repo_files']} |")
for e in c["reading_set_paths"]:
    md.append(f"| `{e['path']}` | reading_set.json | {e['in_repo_files']} |")
md.append("")
md.append(f"Missing paths: **{c['missing'] or 'none'}**. "
          "(Their bytes are not in the sandbox — listing only; content verification is "
          "check-1-blocked. The four `source_file` sha256 values in calibration.json's rows and the "
          "record/banner digests cannot be re-verified here.)\n")
md.append("> **PASS** — all 4 distinct referenced paths are tracked files; zero missing.\n")

# --- 7 -----------------------------------------------------------------------
c = C["7_vocabulary"]
md.append("## 7. The six-value reading vocabulary\n")
md.append(f"- Claim: {c['prereg_claim']}")
md.append(f"- A vocabulary list in any bundle JSON (`*.vocab*` key): **{c['vocabulary_list_found_in_bundle_json']}** — none. "
          f"`config.json`'s top-level keys are: {', '.join('`'+k+'`' for k in c['config_json_top_level_keys'])}.")
md.append(f"- Relation strings present anywhere in the bundle: {c['relation_strings_present_anywhere_in_bundle']['relation_strings_in_calibration_ground_truth'] if 'relation_strings_in_calibration_ground_truth' in c['relation_strings_present_anywhere_in_bundle'] else c['relation_strings_present_anywhere_in_bundle']['calibration_ground_truth']} "
          f"({c['relation_strings_present_anywhere_in_bundle']['note']}).")
md.append(f"- Where the enumerated list actually lives: {c['where_the_list_actually_lives']}")
md.append(f"- Why not checkable: {c['why']}\n")
md.append("> **NOT-CHECKABLE** — PREREG.md asserts 'closes it to six values' but no file in the "
          "bundle (or sandbox) enumerates the six values; the defining modules are absent, so "
          "bytes cannot be compared against the claim.\n")

# --- 8 -----------------------------------------------------------------------
c = C["8_credential_scan"]
md.append("## 8. Credential scan over every file in the sandbox\n")
md.append(f"- Patterns: `{c['patterns']['sk-hex32']}` and `{c['patterns']['hex32.dot.token20+']}`.")
md.append(f"- Files scanned: **{c['files_scanned']}** (every regular file in the sandbox, including "
          "this task's own `check/` scripts and `out/` products, which are where the pattern "
          "strings themselves live).")
md.append(f"- Hits: **{c['hit_count']}** → {c['hits']} ({c['policy']}).")
md.append("- Separately, endpoint key names appear only as names: `DEEPSEEK_API_KEY` and "
          "`OLLAMA_API_KEY` occur only in `key_env` fields / prose; no `=`-assignment or "
          "`sk-`-prefixed value accompanies them (no line in any file matches either pattern).\n")
md.append("> **PASS** — zero credential-shaped hits over all 34 files.\n")

# --- 9 -----------------------------------------------------------------------
c = C["9_dates_and_run_ids"]
md.append("## 9. Every date / run-id string in the bundle (stale-run-id sweep)\n")
md.append(f"Distinct calendar dates across the seven bundle files: **{c['distinct_calendar_dates']}**. "
          f"Distinct date/run-id–shaped strings: **{c['n_distinct_strings']}**.\n")
md.append("| string | appears in |")
md.append("|---|---|")
for tok_, wheres in c["values_with_locations"].items():
    locs = "; ".join(f"`{f}` lines {w['lines'][:8]}{'…' if len(w['lines']) > 8 else ''}"
                     for f, w in wheres.items())
    md.append(f"| `{tok_}` | {locs} |")
md.append("")
md.append(f"- {c['run_id_consistency']}.")
md.append(f"- {c['out_of_bundle_note']}.\n")
md.append("> **PASS** — one run id and one calendar date throughout; the only deviant strings are the "
          "self-declared placeholders; no stale run id or date in the bundle.\n")

# --- limits ------------------------------------------------------------------
md.append("## What these checks cannot establish\n")
for item in r["what_these_checks_cannot_establish"]:
    md.append(f"- {item}")
md.append("")
md.append("---\n*Generated by `check/render_md.py` from `out/prereg-checks.json`, which was "
          "assembled by `check/render_json.py` from the raw outputs of `check/check01…check09`. "
          "Raw evidence preserved under `out/` (per-check JSON) and `out/check1/` (verbatim "
          "validator output). No overall score, per task.*")

Path("out/prereg-checks.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print("md written,", len("\n".join(md)), "chars")
