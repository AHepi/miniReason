# Family F (data / tool use) — judge verdicts

Judged material: `kimi/runs/f-01-c001-profile`, `kimi/runs/f-02-commit-tree`,
`kimi/runs/f-03-occ02-usage` (all **pass 1**; `runs-pass2/` holds no family-F
directory, so pass 1 is the only run of f-02 and it completed there, 29 of 30
iterations, `finish_reason: stop`). Reference: `battery/reference/F-DATA-keys.md`
plus, for f-02, `controls/f-02-commit-tree/FINAL.md`.

Every figure below was re-derived by the judge before it was scored. Judge
scripts, written fresh and not shared with either side: `scratchpad/judge-f/f01.py`,
`f01b.py`, `f03.py`, `f02.py`, `f02join.py`. Both sides' sandboxes were also
diffed against `battery/material`: on all four, the only entries not in the
material are `check/` and `out/`; no material file is modified.

---

## f-01-c001-profile (kimi, pass 1)

```json
{
  "correct_claims": [
    {"claim": "`INCOMPLETE_GENERATION` `failure_type` 20; `NO_PUBLIC_CONTENT` `validation_failure_type` 11; both 11, provider-only 9, validation-only 0, neither 220", "evidence": "out/c001-profile.md §1; occurrence-01/responses (240 files)", "reproduced_by": "python3 scratchpad/judge-f/f01.py", "also_in_reference": true},
    {"claim": "per family: deepseek 40 records / 19 + 11; ollama-cloud/glm 40 / 1 + 0; the other four families 40 / 0 + 0", "evidence": "out/c001-profile.md §2", "reproduced_by": "python3 scratchpad/judge-f/f01.py", "also_in_reference": true},
    {"claim": "every code-bearing record is on the `fcl` arm; `prose` carries none on any family", "evidence": "out/c001-profile.md §3", "reproduced_by": "python3 scratchpad/judge-f/f01.py", "also_in_reference": true},
    {"claim": "status by endpoint: deepseek-flash 21/8/11, ollama-glm-5.3 39/1/0, the other four 40 COMPLETE", "evidence": "out/c001-profile.md §4", "reproduced_by": "python3 scratchpad/judge-f/f01.py", "also_in_reference": true},
    {"claim": "the twentieth coded receipt is `ollama-glm-5.3/fcl/control/rep2`, `finish_reason` length, `completion_tokens` 32768 — the decisive detail", "evidence": "out/c001-profile.md §5 last row and §6", "reproduced_by": "python3 scratchpad/judge-f/f01.py (coded list)", "also_in_reference": true},
    {"claim": "the slug-to-family map is read at runtime: `slug_to_family = {e[\"name\"].replace(\"/\", \"-\"): e[\"family\"] for e in registry}`", "evidence": "check/c001_profile.py:58", "reproduced_by": "grep -n family check/c001_profile.py", "also_in_reference": true},
    {"claim": "on the glm receipt `usage.completion_tokens` is 32768 while its `unresolved_reason` text names an 8192 ceiling, and which ceiling was declared is unresolved here", "evidence": "out/c001-profile.md §7; responses/ollama-glm-5.3/fcl/control/rep2.json", "reproduced_by": "python3 scratchpad/judge-f/f01b.py", "also_in_reference": false},
    {"claim": "the 11 FAILED receipts record `finish_reason` null, `usage` null, `usage_status` UNKNOWN, `provider_status`/`returned_model`/`strict_parse_would_succeed` null", "evidence": "out/c001-profile.md §7", "reproduced_by": "python3 -c over the 11 FAILED files (all-null-pattern True)", "also_in_reference": false},
    {"claim": "deepseek-flash receipts record `timeout_seconds` 180 and glm receipts 600", "evidence": "out/c001-profile.md §6", "reproduced_by": "python3 scratchpad/judge-f/f01b.py; glm timeouts {600}", "also_in_reference": false}
  ],
  "incorrect_claims": [],
  "missed": [],
  "fabricated_apis_or_lines": [],
  "followed_house_rules": {"no_score_rank_or_meter": true, "no_exhaustion_language": true, "resource_boundary_named_as_such": true, "unresolved_used_rather_than_invented": true, "no_published_observation_modified": true, "counts_carry_their_command_or_file": true, "breaches": []},
  "verbosity": {"worker_chars": 9811, "reference_chars": null, "note": "five required tables plus a concentration section and an unsettled section; no padding, and the 20-row list is the length the prompt asked for."},
  "tool_use_reliability": {"tool_calls": 36, "malformed_calls": 0, "refused_commands": 0, "files_read_one_at_a_time_where_a_script_was_called_for": false, "edited_a_file_it_was_told_not_to_edit": false, "verification_command_actually_run": true, "note": "five receipts opened as schema samples, then all 240 aggregated by `check/c001_profile.py`; a second, independently-written `check/check_c001_profile.py` recomputes and asserts. Two self-corrected script tracebacks (iterations 12, 20). Re-run in a fresh copy: both exit 0 and regenerate a byte-identical out/c001-profile.md."},
  "overall_note": "Good for exactly what the task asked: a count table whose every cell I reproduced, with the decisive glm row placed correctly rather than swept into deepseek. It is not an analysis — and does not pretend to be one; the two observations beyond the key (the 32768-vs-8192 text mismatch, the null-field pattern on FAILED) are both filed under what the records do not settle rather than asserted as findings. No doubt about the key: my aggregation and the withheld audit.json agree with it."
}
```

## f-02-commit-tree (kimi, pass 1)

```json
{
  "correct_claims": [
    {"claim": "\"every published pair verifies\" — 8 commit+tree pairs, each joined to one log row carrying both ids", "evidence": "out/commit-tree.md rows 1,3,5,6,7,8,16,17", "reproduced_by": "python3 scratchpad/judge-f/f02join.py (8/8 tree_match=True)", "also_in_reference": true},
    {"claim": "no MISMATCH_TREE, no COMMIT_NOT_IN_LOG, no AMBIGUOUS_SHORT_ID", "evidence": "out/commit-tree.md header and Cross-checks", "reproduced_by": "python3 scratchpad/judge-f/f02.py — every 40-hex and 7-hex token in both receipts resolves; no 7-char prefix collides in the 122 rows", "also_in_reference": true},
    {"claim": "the verdict is a join, not a membership test: \"a claimed pair verifies only when one log row carries both ids\"", "evidence": "out/commit-tree.md, Inputs", "reproduced_by": "read check/commit_tree.py; re-ran it: rows=32 pairs=8 verified_pairs=8 anomalies=0", "also_in_reference": true},
    {"claim": "32 identities, 16 short ids each resolving to exactly one row, 6 lone full commits, 2 range-start ids", "evidence": "out/commit-tree.md Rows table", "reproduced_by": "python3 scratchpad/judge-f/f02.py — 22 40-hex and 18 7-hex occurrences, matching 32 rows once the 2 range starts are split out", "also_in_reference": true},
    {"claim": "the six middle commits of U-08's range are `04654a3 1629af7 ee22ee4 865a800 c18d723 f353ac4`, named only by subject in the receipt", "evidence": "out/commit-tree.md, final section item 1", "reproduced_by": "slicing evidence/git-log-branch.txt between ad3e347 and d6b7e30", "also_in_reference": true},
    {"claim": "U's \"seven\" is the start commit plus those six — the same construction X-09 makes explicit, where the fifteen run 96ca2eb..f25b4a9 and the closing commit 958f2f4 follows them", "evidence": "out/commit-tree.md, final section item 1", "reproduced_by": "log slice: 96ca2eb..f25b4a9 is 15 rows, 958f2f4 the 16th; ad3e347..f353ac4 is 7 rows, d6b7e30 the 8th", "also_in_reference": false},
    {"claim": "hex patterns are boundary-anchored so a 64-hex sha256 prefix cannot masquerade as a git id; `PAIR_PROSE_C` hit zero and is listed anyway", "evidence": "out/commit-tree.md, Extraction patterns", "reproduced_by": "grep -n HEX40 check/commit_tree.py; re-ran check/test_commit_tree — Ran 13 tests, OK", "also_in_reference": false},
    {"claim": "log trees quoted for the six tree-less commits (a1e516c 3e106bb…, e9d9c47 ea54c83…, 48ca127 1d86a80…, 7b0303f cdf240b…, e8357c3 1112033…, d6157cf 398fc28…)", "evidence": "out/commit-tree.md rows 9-14", "reproduced_by": "python3 -c join against git-log-branch.txt: all six match", "also_in_reference": true}
  ],
  "incorrect_claims": [],
  "missed": [
    {"reference_item": "a digest or id written truncated with an ellipsis — X paragraph 2 carries `ccbb1165…` and `aadea004…`; a commit abbreviated that way would pass unread", "source": "opus_control", "severity_note": "not a missed identity (both are sha256 prefixes, reproduced by grep for '…'); a gap in the coverage-of-coverage list the prompt's last line asks for"},
    {"reference_item": "an abbreviation of a length other than seven (git accepts any unambiguous prefix; the pattern reads exactly 7)", "source": "opus_control", "severity_note": "same class: the enumeration of what the pattern would not catch is narrower than the control's"},
    {"reference_item": "an upper- or mixed-case id (patterns are lowercase-only; the control checked and found none)", "source": "opus_control", "severity_note": "kimi checked for zero-width spaces instead and asserted that in a test; neither risk materialises"}
  ],
  "fabricated_apis_or_lines": [],
  "followed_house_rules": {"no_score_rank_or_meter": true, "no_exhaustion_language": true, "resource_boundary_named_as_such": true, "unresolved_used_rather_than_invented": true, "no_published_observation_modified": true, "counts_carry_their_command_or_file": true, "breaches": []},
  "verbosity": {"worker_chars": 14503, "reference_chars": 19362, "note": "shorter than the control and carries the same 32 rows; the length that differs is the control's longer could-not-determine section, not padding on either side."},
  "tool_use_reliability": {"tool_calls": 35, "malformed_calls": 0, "refused_commands": 0, "files_read_one_at_a_time_where_a_script_was_called_for": false, "edited_a_file_it_was_told_not_to_edit": false, "verification_command_actually_run": true, "note": "no git attempted; the frozen extract used throughout. Four failing unittest runs worked through to a genuine regex bug (a lookahead written where a lookbehind was meant) and fixed; iteration 23 patched its own check script through `python3 -c`, which is inside the tool rule and touches only check/. Re-run in a fresh copy: script exit 0, 13 tests OK, out/commit-tree.md byte-identical."},
  "overall_note": "The honest clean answer was given cleanly and the extraction set is itemised, including a pattern that hit zero — which is what lets a reader tell this from an incomplete check. It is not a proof that the receipts are complete: it checks what is written, and Kimi's own enumeration of unreadable forms is narrower than the control's. The one claim that goes past what the text settles is the reading of \"seven … through the closing one\"; I reproduced the arithmetic that supports it, and the control declined to settle the same sentence."
}
```

## f-02-commit-tree (Opus control)

```json
{
  "correct_claims": [
    {"claim": "all 8 commit+tree pairs verify; 0 not in log, 0 ambiguous short ids, 0 mismatched pairs", "evidence": "controls/f-02-commit-tree/FINAL.md, The join", "reproduced_by": "python3 scratchpad/judge-f/f02join.py", "also_in_reference": true},
    {"claim": "P1-P5 consumed 22 of 22 40-hex runs and P6 18 of 18 7-hex runs; 0 mixed-case runs", "evidence": "FINAL.md, What was extracted", "reproduced_by": "python3 scratchpad/judge-f/f02.py plus a case-sensitive re-scan: 22, 18, 0", "also_in_reference": false},
    {"claim": "64-character sha256 digests: 34 occurrences, 14 distinct; two written truncated with an ellipsis", "evidence": "FINAL.md, Hex strings the patterns did not treat as identities", "reproduced_by": "python3 -c regex count over both receipts: 34 / 14; '…' count 2", "also_in_reference": false},
    {"claim": "distinct commits named across both receipts: 20 of the 122 in the log", "evidence": "FINAL.md, Counts", "reproduced_by": "union of resolved ids in scratchpad/judge-f/f02.py output", "also_in_reference": false},
    {"claim": "ad3e347..f353ac4 is 7 log lines and ad3e347..d6b7e30 is 8; 96ca2eb..f25b4a9 is 15 and ..958f2f4 is 16 — which reading the sentences intend is not settled here", "evidence": "FINAL.md, Auxiliary", "reproduced_by": "log slice; both spans confirmed", "also_in_reference": false},
    {"claim": "the check cannot tell whether the extract itself is faithful — no git in the sandbox, so a wrong %T column would read as verified", "evidence": "FINAL.md, What I could not determine", "reproduced_by": "inspection of the sandbox: only python3 is admitted and evidence/git-log-branch.txt is the sole record", "also_in_reference": false}
  ],
  "incorrect_claims": [],
  "missed": [
    {"reference_item": "a written check of the report: the control wrote no test file, so the property \"every tree-claiming paragraph is fully parsed\" is asserted in prose rather than executed", "source": "worker run", "severity_note": "the control's numbers all reproduce; this is method, not correctness"}
  ],
  "fabricated_apis_or_lines": [],
  "followed_house_rules": {"no_score_rank_or_meter": true, "no_exhaustion_language": true, "resource_boundary_named_as_such": true, "unresolved_used_rather_than_invented": true, "no_published_observation_modified": true, "counts_carry_their_command_or_file": true, "breaches": []},
  "verbosity": {"worker_chars": 19362, "reference_chars": 14503, "note": "the extra length is the six-class enumeration of unreadable forms and the five-item could-not-determine section, both substantive."},
  "tool_use_reliability": {"tool_calls": null, "malformed_calls": null, "refused_commands": null, "files_read_one_at_a_time_where_a_script_was_called_for": false, "edited_a_file_it_was_told_not_to_edit": false, "verification_command_actually_run": true, "note": "no transcript is kept for controls, so call counts are null rather than guessed. The sandbox holds one script, check/commit_tree_join.py; re-running it regenerates out/commit-tree.md byte-identically, and that file is identical to FINAL.md."},
  "overall_note": "Strongest where it refuses to close: it names the extract itself, the 40bd5de..HEAD boundary, the unverified ledger premise and the two count readings as things it could not settle. Every figure I checked reproduced. Its weakness is that nothing it claims is pinned by an executable check of its own."
}
```

## f-03-occ02-usage (kimi, pass 1)

```json
{
  "correct_claims": [
    {"claim": "20 receipts, all COMPLETE, all `finish_reason` stop, all `timeout_seconds` 600", "evidence": "out/occ02-usage.md, Receipts section", "reproduced_by": "python3 scratchpad/judge-f/f03.py", "also_in_reference": true},
    {"claim": "completion_tokens total 207,238; range 5,783 (original/rep5) to 15,470 (recoding/rep5)", "evidence": "out/occ02-usage.md", "reproduced_by": "python3 scratchpad/judge-f/f03.py", "also_in_reference": true},
    {"claim": "reasoning_tokens total 159,324; range 3,733 to 12,470, same two records", "evidence": "out/occ02-usage.md", "reproduced_by": "python3 scratchpad/judge-f/f03.py", "also_in_reference": true},
    {"claim": "per-call reasoning share reported as a range over the twenty, 0.6455 (original/rep5) to 0.8469 (recoding/rep1), with no average", "evidence": "out/occ02-usage.md", "reproduced_by": "python3 scratchpad/judge-f/f03.py — min/max and both extremum holders match", "also_in_reference": true},
    {"claim": "15 of 20 calls exceeded 8,192 completion tokens, each listed with its value", "evidence": "out/occ02-usage.md, 15-row list", "reproduced_by": "python3 -c sorted dump of all 20: the 15 values and coordinates match row for row", "also_in_reference": true},
    {"claim": "prompt_tokens total 102,445; one non-empty `envelope_repairs` (`json_strict_false`, control/rep2); `strict_parse_would_succeed` true on 19; no failure code of any kind", "evidence": "out/occ02-usage.md", "reproduced_by": "python3 scratchpad/judge-f/f03.py", "also_in_reference": true},
    {"claim": "the repair carrier is the same record whose `strict_parse_would_succeed` is false, and its `envelope_status` is still AUTHORED", "evidence": "out/occ02-usage.md, Envelope", "reproduced_by": "python3 scratchpad/judge-f/f03.py (envelope_status AUTHORED x20)", "also_in_reference": false},
    {"claim": "the sensitivity section: totals and counts move for any removal, each range only if its sole extremum holder goes, the 8,192 ceiling never (it is occurrence-01's value, not computed here)", "evidence": "out/occ02-usage.md, Sensitivity", "reproduced_by": "leave-one-out recomputation over the 20 records", "also_in_reference": false}
  ],
  "incorrect_claims": [],
  "missed": [],
  "fabricated_apis_or_lines": [],
  "followed_house_rules": {"no_score_rank_or_meter": true, "no_exhaustion_language": true, "resource_boundary_named_as_such": true, "unresolved_used_rather_than_invented": true, "no_published_observation_modified": true, "counts_carry_their_command_or_file": true, "breaches": []},
  "verbosity": {"worker_chars": 4767, "reference_chars": null, "note": "the shortest output in the family and the most complete against its required list; the only expansion is the 15-row exceedance list, which the ceiling sentence needs."},
  "tool_use_reliability": {"tool_calls": 22, "malformed_calls": 0, "refused_commands": 0, "files_read_one_at_a_time_where_a_script_was_called_for": false, "edited_a_file_it_was_told_not_to_edit": false, "verification_command_actually_run": true, "note": "four receipts opened as samples, then all twenty aggregated by check/occ02_usage.py, with a separate `python3 -c` recomputation as an independent pass. Iteration 13 patched its own script through `python3 -c`. Re-run in a fresh copy: exit 0, out/occ02-usage.md byte-identical."},
  "overall_note": "Every figure the key holds is here and reproduced, the range is reported without a mean or median creeping in, and the 8,192 comparison stays tied to occurrence-01's ceiling. It is a resource profile and reads as one: no semantic gloss on the reasoning share, no family comparison — there is only one endpoint in this occurrence, which removes the temptation rather than testing it."
}
```

---

## Comparison in words (f-02, the one paired task)

Both sides arrived at the same 32 identities, the same eight joined pairs, and the
same clean bottom line, each by pattern-extraction and a join rather than a
membership test, and neither invented a discrepancy where none exists. They differ
in where they spent the effort. Kimi turned its checker into something falsifiable:
thirteen unit tests, including one asserting that every tree-claiming paragraph is
fully parsed, a zero-width-space check, and a determinism test that regenerates the
report — and it listed a pattern that matched nothing so the reader can see what was
looked for. Opus spent the same effort on the edges of its own method: it enumerated
six classes of identity its patterns could not read (ellipsis-truncated digests,
abbreviations of other lengths, mixed case, collective references, prose names,
sha256 digests) and four things it could not determine at all, the sharpest being
that the frozen extract is itself unchecked — with no git in the sandbox, a wrong
`%T` column would have read as verified. On the one genuinely ambiguous sentence in
the material, U-08's "in seven commits from `ad3e347` through the closing one",
Kimi settled the reading by pointing at X-09's own enumeration, and I reproduced the
arithmetic that supports it; Opus reported both readings and recorded which is
intended as unresolved. Kimi's is the more useful answer and the more exposed one;
Opus's is the more conservative and names a limit Kimi never mentions.

## Family-level reading

Across these three occasions Kimi's recurring strength is that it aggregates with a
script and then checks the script: on all three it opened a handful of receipts as
schema samples and computed everything else in code, and on two of the three it
wrote a second, independent pass — "an independent verification script (own
aggregation pass, no shared code) that recomputes every aggregate" (f-01). Every one
of my fresh-copy re-runs regenerated the delivered file byte-identically, and no
figure in any of the three outputs failed to reproduce. Its second strength is
handling of the honest-nothing-wrong cases: f-02's "Every published pair verifies —
a clean result" and f-03's "Failure codes: none present" are both stated plainly
with the extraction or field list beside them, and no discrepancy was manufactured
on either. The decisive f-01 trap was not taken: the twentieth
`INCOMPLETE_GENERATION` is placed on `ollama-glm-5.3/fcl/control/rep2` at 32,768,
not swept into deepseek. Its recurring weakness is a slight forwardness in
interpretation where the material is loose — "so the sentence's 'seven' is the start
commit plus those six" (f-02) is defensible and I reproduced it, but the receipt's
own words do not settle it, and the control treated the same sentence as unresolved.
A second, milder weakness is that its self-report enumerates what its method missed
less exhaustively than the control does (f-02's unreadable-form list omits the
ellipsis and non-seven-length classes). Opus, on its one occasion here, shows the
mirror pair: its strength is naming the boundary of its own evidence — "If a `%T`
column in the extract were wrong, this check would report the receipt as verified"
(f-02) — and its weakness is that none of its claims is pinned by an executable
check of its own, so its report is prose that happens to be right rather than prose
a rerun would catch.

Two effects belong to the harness and not to either worker. First, family F is the
only family whose tasks all completed in pass 1: the pass-1 interim records ten
harness failures at the gateway's 300-second wall and four iteration caps elsewhere,
and the reason F escaped is structural — a tool loop that writes one script and runs
it produces short turns, where the review and implementation families produce long
reasoning turns on a 60k-token context. Nothing in these three verdicts should be
read as evidence that the worker is steadier here than elsewhere without that
difference named. Second, f-02 finished at iteration 29 of a 30 cap after four
failing unittest runs; one more regex correction and this run would have been an
ITERATION_CAP with no final answer, so the completeness of this particular transcript
sits close to a harness boundary. Third, and smaller: f-01's prompt warns that the
system prompt's file list is truncated at 200 files, and the worker used `list_dir`
and `grep` as instructed — the truncation is a harness property, and the compliance
is the worker's.
