"""Render out/prereg-checks.json + out/prereg-checks.md from the per-check outputs."""
import json
from pathlib import Path

def L(name):
    return json.loads(Path(name).read_text(encoding="utf-8"))

d2 = L("out/check2-digests.json")
d2c = L("out/check2c-config-diff.json")
tok = L("out/sha-token-map.json")
env = L("out/check1/env-report.json")
d3 = L("out/check3-seats.json")
d4 = L("out/check4-maxcalls.json")
d5 = L("out/check5-obligations.json")
d6 = L("out/check6-paths.json")
d7 = L("out/check7-vocab.json")
d8 = L("out/check8-credentials.json")
d9 = L("out/check9-dates.json")

stdout_root = Path("out/check1/validate.stdout.txt").read_text(encoding="utf-8")
stderr_root = Path("out/check1/validate.stderr.txt").read_text(encoding="utf-8")

checks = {}

checks["1_validate_py_run"] = {
    "status": "FAIL",
    "what": "Run python3 loop-prereg/validate.py; record exit code and verbatim output.",
    "command_from_sandbox_root": "python3 loop-prereg/validate.py",
    "exit_code_root": 1,
    "stdout_root_verbatim": stdout_root,
    "stderr_root_verbatim": stderr_root,
    "command_from_inside_bundle": "python3 validate.py (cwd=loop-prereg/)",
    "exit_code_inside": env["exit_code"],
    "stdout_inside_verbatim": env["stdout"],
    "stderr_inside_verbatim": env["stderr"],
    "failure_analysis": {
        "first_failing_line": "validate.py line 8: from minireason.loop.types import LoopConfig, loop_plan_id, LoopError, CONFIG_SCHEMA",
        "sandbox_src_files": env["sandbox_files_under_src"],
        "hardcoded_repo_path_in_validate_py": env["validate_py_hardcoded_repo_path"],
        "modules_validate_py_imports": ["minireason.loop.types", "minireason.loop.standard",
                                        "minireason.loop.receipts", "deepreason_core.canonical"],
        "those_modules_in_sandbox": False,
        "published_files_validate_py_would_read": [
            "src/minireason/data/endpoints.json (present in sandbox)",
            "experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14/use-table-golden/use_table.json (NOT in sandbox)",
            "experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14/use-table-full/use_table.json (NOT in sandbox)",
            "experiments/diagnostics/C001-contrast-triple/occurrence-02/comparison.json (NOT in sandbox)",
        ],
    },
}

c2 = {
    "status": "FAIL",
    "files_hashed": d2["files_hashed"],
    "comparison_vs_VALIDATION_md_table": d2["validation_md_pin_table"],
    "n_mismatched": sum(1 for r in d2["validation_md_pin_table"] if r["match"] is False),
    "sha256_tokens_in_documents": {
        "files_scanned": ["loop-prereg/PREREG.md", "loop-prereg/VALIDATION.md", "loop-prereg/config.json"],
        "n_distinct_64hex_tokens": tok["n_distinct_tokens"],
        "prefix_only_mentions": tok["prefix_mentions"],
        "tokens_matching_a_bundle_file": d2["token_matches_bundle_file"],
        "tokens_matching_no_bundle_file": d2["tokens_matching_no_bundle_file"],
        "config_json_contains_no_sha256_token": True,
        "what_each_unmatched_token_is_said_to_pin": {
            "24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927":
                "PREREG.md:150 (obligation p1): 'the H005 occurrence-01 `material_sha256` equals 24ca4552<...>' — pins published repo file experiments/diagnostics/H005-open-prose-commitments/occurrence-01/material.json; not in the sandbox, not verifiable here.",
            "328b9452c66fed52203015c540652d3b8ad3107d44dece56b55ebe721da341c8":
                "PREREG.md:40: 'C001 (`plan_id 328b9452<...>`)' — pins the frozen C001 study plan_id; not a file of this bundle; not verifiable here (only 3/7885 tracked files are in the sandbox).",
            "46495a6fa0ee5667b6ba5128adbaee9062ed5b6637310bb44b12efdf14c0da90":
                "VALIDATION.md:108, §4 table row '| `config.json` | `46495a6f<...>` |' — said to pin config.json; the sandbox copy hashes to 081dd939<...>, so the recorded digest does NOT match the file delivered with the bundle.",
            "713119a7cd255296058b18084a40cbac7a3353903bbf8cd260b6e78c173e4302":
                "PREREG.md:105: 'obligations.json is pinned at sha256 713119a7<...> before cycle 1'; VALIDATION.md:65: same value as the digest that 'reproduces over canonical bytes'. It pins the CANONICAL STRUCTURE of obligations.json, not its raw bytes (raw bytes hash to 2913693a<...>). Recomputed over canonical bytes by computation: it does reproduce.",
        },
    },
    "obligations_canonical_digest": d2["obligations_canonical"],
    "config_mismatch_forensics": {
        "sandbox_copy": "valid UTF-8, LF-only (109 LF, 0 CR), ends with newline, 6362 bytes; json.loads round-trip is byte-identical to the sandbox copy",
        "pinned_digest_reproduced_by_no_tested_variant": not d2c["any_variant_reproduces_pin"],
        "variants_tested": {k: v["sha256"] for k, v in d2c["variants"].items()},
        "conclusion": "the pinned value cannot be located from the sandbox copy alone; the two differ by unknown content",
        "corroboration": "VALIDATION.md §2's transcript shows validate.py PASS lines referencing a run directory experiments/loops/L001-loop-first-live-2026-09-14/ and loop_plan_id values — and evidence/repo-files.txt contains no L001/loop-prereg path at all, and contains no src/minireason/loop/ module",
    },
}
checks["2_sha256_vs_pins"] = c2

checks["3_seats_vs_registry"] = {
    "status": "PASS",
    "seat_lookup": d3["seat_lookup"],
    "all_five_seats_exist_in_endpoints_json": d3["all_seats_exist"],
    "mismatches": d3["mismatches"],
    "prereg_table_rows_extracted": d3["prereg_seat_table_rows"],
    "prereg_table_matches_registry": True,
    "judge_seats_share_a_family": d3["judge_seats_share_a_family"],
    "judge_families": d3["judge_family_check"],
    "n_distinct_families_over_5_seats": d3["n_distinct_families_over_5_seats"],
    "note": ("config.json expresses seats by endpoint name only; family and key_env were "
             "read from the registry and match PREREG.md's table (lines 64-68) cell for "
             "cell, including registry timeout_seconds=180 for all five."),
}

c4 = dict(d4)
c4["status"] = "PASS"
c4["derivation_sentence_in_PREREG_md"] = (
    "PREREG.md clause 5 (lines 126-128): '5. Else, cycle index equals `cycle_budget` = 3, or "
    "`max_calls` = 396 is reached ⇒ STOP `resource_boundary` — a declared attention-and-spend "
    "boundary, never an adjudication and never the inquiry running out of things to say.'")
c4["derivation_lives_in"] = ("reading_set.json max_calls_derivation block (per-entry "
                             "budgeted_calls and per-leg subtotals); PREREG.md states the "
                             "result values but no derivation sentence of its own")
c4["arithmetic_recomputed"] = "4x0 + 12x9 + 22x11 + 1x46 + 0 = 0 + 108 + 242 + 46 + 0 = 396 == config.max_calls == 396; cycle_budget 3 == PREREG clause 5's 3 and reading_set audit-window cycle (2) satisfies 2 mod audit.period(2) == 0 within cycles 1..3"
checks["4_max_calls_arithmetic"] = c4

c5 = dict(d5)
c5["status"] = "PASS"
c5["counts_match_prereg"] = (d5["O_count_actual"] == 7 and d5["P_count_actual"] == 12)
c5["prereg_claim_line"] = ("PREREG.md line 10: '| `obligations.json` | the failed set **O** (7) "
                           "and the protected set **P** (12), pinned by sha256 |'")
checks["5_obligations"] = c5

c6 = dict(d6)
c6["status"] = "PASS"
checks["6_referenced_paths_tracked"] = c6

checks["7_vocabulary"] = {
    "status": "NOT-CHECKABLE",
    "prereg_claim": ("PREREG.md lines 46 and 201: the run closes "
                     "`use_relation_h005.ROOT_READING_VOCABULARY` 'to six values'; "
                     "obligations o1 names the member set only as `standard.NOMINABLE_RELATIONS`."),
    "vocabulary_list_found_in_bundle_json": d7["vocabulary_keys_found_in_bundle_json"],
    "vocabulary_key_in_config_json": False,
    "config_json_top_level_keys": d7["config_json_keys"],
    "relation_strings_present_anywhere_in_bundle": {
        "calibration_ground_truth": d7["relation_strings_used_in_calibration_ground_truth"],
        "note": "only 2 of the promised 6 values appear anywhere in the bundle, as calibration ground-truth strings",
    },
    "where_the_list_actually_lives": ("src/minireason/use_relation_h005.py is a tracked repo "
                                      "file (evidence/repo-files.txt line 7684) but is not in "
                                      "the sandbox; standard.NOMINABLE_RELATIONS lives in "
                                      "src/minireason/loop/standard.py which is absent from the "
                                      "tracked file list entirely (grep of evidence/repo-files.txt)."),
    "why": ("No file in the sandbox carries the six-value list, so bytes cannot be compared "
            "against bytes. The claim that the closed vocabulary has exactly six values is "
            "asserted in prose in three places and enumerable in none."),
}

checks["8_credential_scan"] = {
    "status": "PASS",
    "patterns": d8["patterns"],
    "files_scanned": d8["files_scanned"],
    "hit_count": d8["hit_count"],
    "hits": d8["hits"],
    "policy": "only path + line number would be reported; zero hits, so nothing withheld",
}

values_detail = {t: {f: w for f, w in wheres.items()} for t, wheres in d9["values"].items()}
checks["9_dates_and_run_ids"] = {
    "status": "PASS",
    "distinct_calendar_dates": d9["distinct_calendar_dates"],
    "n_distinct_strings": d9["n_distinct_strings"],
    "values_with_locations": values_detail,
    "run_id_consistency": ("single run id L001-loop-first-live-2026-09-14 in all 6 files that "
                           "carry one; every date-like string in the bundle is the single "
                           "calendar date 2026-09-14; declared placeholder REC-20260914-Z at "
                           "2026-09-14T00:00:00Z (PREREG.md §1 declares both as placeholders); "
                           "no stale or second run id / date found"),
    "out_of_bundle_note": ("AGENTS.md outside the bundle references REC-20260913 (2026-09-13) "
                           "in an erratum filename — unrelated to the L001 run, listed for "
                           "completeness only"),
}

cannot_establish = [
    "Anything requiring the absent repository tree: the full validate.py run, its PASS transcript in VALIDATION.md (reproducibility claim), the content of the six-value vocabulary, BLOCK_CODES, MARKS, the frozen CEILING_TEXT/PREREGISTRATION_REQUIRED_SENTENCES, and every pinned digest of a published file (C001 plan_id, material_sha256, calibration source bytes). The tracked file list shows the pins' targets exist in the repo; nothing here can verify their bytes.",
    "Whether experiments/loops/L001-loop-first-live-2026-09-14/ was ever created in the real repository — evidence/repo-files.txt contains no L001 path, but this bundle describes itself as pre-dispatch ('the run directory ... does not yet exist'), and a git ls-files snapshot cannot distinguish 'run never executed' from 'run executed but outputs not committed'. VALIDATION.md's own transcript, however, references the run directory and minted plan artifacts.",
    "Which of the two config.json byte strings is authentic, or where the divergence entered (staging clone vs copy step); the sandbox holds one side only.",
    "Whether the stated canonicalization recipe equals deepreason_core.canonical.canonical_json / minireason.provider.digest byte-for-byte (the modules are absent); only the equivalence of the recipe as written with the recorded obligations digest was recomputed.",
    "Whether the sandbox copy itself is byte-identical to what an external reviewer received via any other channel (no second copy is available to compare); all claims here are internal to the sandbox.",
    "Intent, motivation, or provenance of the mismatch — only that the bytes differ from the recorded digest.",
    "The semantic adequacy of the design (guard soundness, clause meanings, whether obligations say what the prose claims they mean). Only stated mechanical relations were checked, per the task's instruction to check bytes against bytes, not judge the design.",
    "Credential hygiene outside the sandbox, key validity, or whether names DEEPSEEK_API_KEY/OLLAMA_API_KEY resolve to anything.",
]

report = {
    "task": "Mechanical consistency checks of the L001 pre-registration bundle (computation only)",
    "sandbox_contents": [
        "loop-prereg/{PREREG.md, VALIDATION.md, config.json, obligations.json, reading_set.json, calibration.json, validate.py}",
        "src/minireason/data/endpoints.json",
        "evidence/repo-files.txt (7885 tracked paths)",
        "AGENTS.md",
    ],
    "checks": checks,
    "no_overall_score": True,
    "what_these_checks_cannot_establish": cannot_establish,
}
Path("out/prereg-checks.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print("json written,", len(json.dumps(report)), "chars")
