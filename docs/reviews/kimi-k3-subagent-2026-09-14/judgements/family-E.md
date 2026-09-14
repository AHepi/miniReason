# Family E — adversarial and verification. Judge's verdicts (kimi-k3 worker).

Material: `kimi/runs/{e-01,e-03,e-04}` (pass 1), `kimi/runs-pass2/e-02-metric-creep` (pass 2).
No Opus control on any of the four; the references are the executed keys. Per the rubric I
re-ran each key's own procedure over `kimi/battery/material` before judging, in
`scratchpad/judge_e01.py`, `judge_e01b.py` and ad-hoc slicing scripts, and re-ran each
worker's own scripts in a copy at `scratchpad/judge-E-work/`. Nothing under
`/home/user/miniReason` was read or written; no sandbox was modified in place.

**Key re-derivation, quoted.** E-ADV-1: `INCOMPLETE_GENERATION: 20`, `Counter({'FAILED': 11,
'PARTIAL': 9})`, `cells: Counter({('deepseek-flash','fcl'): 19, ('ollama-glm-5.3','fcl'): 1})`,
outlier `ollama-glm-5.3/fcl/control/rep2.json status PARTIAL fr length ctok 32768`; status by
endpoint `deepseek-flash {COMPLETE 21, PARTIAL 8, FAILED 11}` / `ollama-glm-5.3 {COMPLETE 39,
PARTIAL 1}`; `envelope_repairs non-empty: 93`, `{'strip_outer_code_fence': 92,
'json_strict_false': 1}`, `receipts with >1: 0`, `strict_parse_would_succeed
Counter({'True': 122, 'False': 107, 'None': 11})`; F001 v1 `Counter({None: 56,
'INCOMPLETE_GENERATION': 7})`, all seven `fr length ctok 8192`. E-ADV-3: FW5 sha256
`8105925b…e33ee63a` reproduced, `split-on-newline elements: 1503 last element repr: ''`, and
`FW5:133: ''` — empty. E-ADV-4: worker script re-run gives `planned total: 89 / receipts 83
{COMPLETE 74, FAILED 7, PARTIAL 2} / ceiling=7 blocked=6`, matching the key's `ok 74, ceiling 7,
blocked 6` — the key's `timeout 2` is discussed under e-04.

---

## e-01-refute — COMPLETE, pass 1 (24 iterations, 785,525 tokens, 481 s)

```json
{
  "correct_claims": [
    {"claim": "Claim 1 REFUTED IN PART; the count 20 and the eleven FAILED survive, the nine-PARTIAL attribution does not", "evidence": "out/refutations.md 'CLAIM 1 — REFUTED IN PART'", "reproduced_by": "python3 scratchpad/judge_e01.py (INCOMPLETE_GENERATION: 20; Counter({'FAILED': 11, 'PARTIAL': 9}))", "also_in_reference": true},
    {"claim": "the decisive coordinate, named in full: 'responses/ollama-glm-5.3/fcl/control/rep2.json — status: PARTIAL, failure_type: INCOMPLETE_GENERATION, provider_status: INCOMPLETE_GENERATION, finish_reason: length, completion_tokens: 32768'", "evidence": "out/refutations.md clause (c)", "reproduced_by": "judge_e01.py OUTLIER line: 'ollama-glm-5.3/fcl/control/rep2.json status PARTIAL fr length ctok 32768'", "also_in_reference": true},
    {"claim": "'The count arithmetic in (a) balances either way (11 + 9 = 20), which is exactly why the misplacement is invisible to anyone who checks only the count.'", "evidence": "out/refutations.md clause (c)", "reproduced_by": "judge_e01.py cells counter: 19 in the cell, 1 outside", "also_in_reference": false},
    {"claim": "Claim 2 SURVIVES — seven in v1, every one at length and 8,192", "evidence": "out/refutations.md CLAIM 2 table, seven coordinates listed", "reproduced_by": "python3 scratchpad/judge_e01b.py (v1 failure_code Counter({None: 56, 'INCOMPLETE_GENERATION': 7}); all fr length ctok 8192)", "also_in_reference": true},
    {"claim": "Claim 3 SURVIVES — '93 of 240', 92 + 1, 'receipts with more than one repair entry: 0', strict true 122 / false 107 / null 11", "evidence": "out/refutations.md CLAIM 3", "reproduced_by": "judge_e01.py (93; {'strip_outer_code_fence': 92, 'json_strict_false': 1}; >1: 0; Counter({'True': 122,'False': 107,'None': 11}))", "also_in_reference": true},
    {"claim": "the single json_strict_false sits at 'ollama-glm-5.3/prose/carrier/rep4'", "evidence": "out/refutations.md CLAIM 3", "reproduced_by": "glob over receipts printing the coordinate carrying json_strict_false", "also_in_reference": false},
    {"claim": "clause (d) unsupported for the eleven FAILED: 'every provider-side field is null — provider_status: null, finish_reason: null, usage: null, returned_model: null'", "evidence": "out/refutations.md clause (d)", "reproduced_by": "judge_e01.py ('FAILED with non-null usage: 0'; 'FAILED provider_status values: Counter({'None': 11})'); PARTIAL provider_status Counter({'INCOMPLETE_GENERATION': 9})", "also_in_reference": false},
    {"claim": "NEW, absent from the key: the report's §2 sentence is not supported by these bytes — '8 of the 20 cell coordinates carry completion_tokens: 8192 … and the eleven FAILED coordinates carry usage: null with no reasoning_tokens recorded at all'", "evidence": "out/refutations.md 'Incidental observation'; report line 183 '19 of its 20 coordinates carry completion_tokens exactly 8,192 … eleven spent the entire ceiling on reasoning (reasoning_tokens 8,192)'", "reproduced_by": "glob over deepseek-flash/fcl: 'ctok==8192: 8 / usage null: 11 / reasoning_tokens==8192: 0'", "also_in_reference": false},
    {"claim": "the neighbouring §2 figures that do hold: 'deepseek-flash x prose 20 of 20 COMPLETE at 3,621–6,985 completion tokens, and 29 of 40 deepseek-flash receipts with reasoning_content_present: true'", "evidence": "out/refutations.md, last paragraph", "reproduced_by": "same glob: 'df prose n= 20 Counter({COMPLETE: 20}) ctok range 3621 6985'; 'df reasoning_content_present true: 29 of 40'", "also_in_reference": false}
  ],
  "incorrect_claims": [
    {"claim": "'(the eight PARTIAL, reasoning_tokens 5,923–7,890 — not 5,488)'", "why_wrong": "the report's clause is about 'the other nine', which is the eight PARTIAL plus the one COMPLETE receipt in the cell; that COMPLETE receipt carries reasoning_tokens 5,488, so the report's lower bound is in the record. The worker narrowed the set to eight and then contested a bound the ninth supplies.", "evidence": "deepseek-flash/fcl usage.completion_tokens_details.reasoning_tokens over the cell: [('COMPLETE',8083,5488), ('PARTIAL',8192,5923) … ('PARTIAL',8192,7890)]; range 5488–7890, n=9", "stale": false}
  ],
  "missed": [],
  "fabricated_apis_or_lines": [],
  "followed_house_rules": {"no_score_rank_or_meter": true, "no_exhaustion_language": true, "resource_boundary_named_as_such": true, "unresolved_used_rather_than_invented": true, "no_published_observation_modified": true, "counts_carry_their_command_or_file": true, "breaches": []},
  "verbosity": {"worker_chars": 11116, "reference_chars": 3514, "note": "About three times the key, and earns most of it with per-clause evidence, but the §2 incidental observation and the claim-3 cross-tab are beyond what was asked."},
  "tool_use_reliability": {"tool_calls": 48, "malformed_calls": 0, "refused_commands": 0, "files_read_one_at_a_time_where_a_script_was_called_for": false, "edited_a_file_it_was_told_not_to_edit": false, "verification_command_actually_run": true, "note": "Sampled six receipts to learn the schema, then aggregated with two scripts over all 240 + 83. One command used shell syntax the TOOLING paragraph excludes — 'python3 check/refute_claims.py > /tmp/c1.log 2>&1; echo \"exit=$?\"' — and the harness ran it anyway; the redirect had no effect. Sandbox byte-identical to material outside out/ and check/."},
  "overall_note": "The decisive hit was found, named by coordinate, and separated clause by clause from what survives; both no-refutation claims were left standing. Good for exactly the job asked. Not good as a finished document: it volunteers a §2 recheck that is mostly right but carries one wrong parenthetical. Doubt about the reference: the key asserts F001 content-byte figures (288 and 7,080) that the sandbox slice cannot settle — there are no .txt siblings under F001 and no byte field in the receipts — and the worker said so rather than reproducing the number."
}
```

Against the key: every scored element matched. The key's full-credit definition — "names the endpoint,
the coordinate, the finish_reason and the 32,768 figure, and says what survives" — is met verbatim. No
fabricated refutation of claims 2 or 3; the aggregation was executed, not asserted.

---

## e-02-metric-creep — NO DELIVERABLE IN EITHER PASS

Pass 1 (`runs/e-02-metric-creep`): `HARNESS_FAILURE`, `TRANSPORT_OR_RESPONSE_ERROR`, "Remote end
closed connection without response" at 360.7 s, 3 iterations, 12 tool calls, `files_written: []`.
Pass 2 (`runs-pass2/e-02-metric-creep`, max_tokens 8192 per turn, 80 iterations): recorded
`status: COMPLETE` but that status is an artefact. The run made seven `read_file` calls over two
iterations, then on iteration 3 returned `finish_reason: length`, `completion_tokens: 8192`,
`content_chars: 0`, `ntools: 0`, `reasoning_content_chars: 35029`, `latency_ms: 152039` — the whole
per-turn budget went to reasoning and the turn emitted neither text nor a tool call, so the loop
ended. `files_written: []`; there is no `out/` and no `probe/` directory in the sandbox.

```json
{
  "correct_claims": [], "incorrect_claims": [], "missed": [],
  "fabricated_apis_or_lines": [],
  "followed_house_rules": {"no_score_rank_or_meter": null, "no_exhaustion_language": null, "resource_boundary_named_as_such": null, "unresolved_used_rather_than_invented": null, "no_published_observation_modified": true, "counts_carry_their_command_or_file": null, "breaches": []},
  "verbosity": {"worker_chars": 0, "reference_chars": null, "note": "No output of any kind was produced in either pass."},
  "tool_use_reliability": {"tool_calls": 7, "malformed_calls": 0, "refused_commands": 0, "files_read_one_at_a_time_where_a_script_was_called_for": false, "edited_a_file_it_was_told_not_to_edit": false, "verification_command_actually_run": false, "note": "Pass 2 read standard.py, types.py, AGENTS.md, both design slices, the wave-0 oracle and the interface note — the right seven files — and never reached run_command. The reading order was sound; the run ended before any probe."},
  "overall_note": "Unjudgeable on content: neither pass produced out/metric-creep.md. The task's own bottom line — 'nothing forbidden is found' — is one of the four occasions the battery cares most about, and it remains untested for this worker. The pass-2 remedy traded the 300 s gateway wall for a per-turn completion ceiling on the same reasoning-heavy turn; recording it as COMPLETE is a harness labelling defect worth fixing before the family is read as a whole."
}
```

---

## e-03-fw5-citations — COMPLETE, pass 1 (20 iterations, 952,650 tokens, 542 s)

```json
{
  "correct_claims": [
    {"claim": "the decisive hit: '#14 … WRONG. **FW5:133 is an empty line** — it is the blank separator between the closing \\] of the answer-profile (Q) display at :132 and the \\(O_p\\) paragraph at :134'", "evidence": "out/citations.md entry 14", "reproduced_by": "python3 slice of FW5 by line: ':132 \\]', ':133 \\'\\'', ':134 The set \\(O_p\\) contains the obligations …'", "also_in_reference": true},
    {"claim": "the bonus: '#4 … CORRECT IN SUBSTANCE (typographic quotes normalised to straight ones)', quoting FW5:226 with its curly quotes intact", "evidence": "out/citations.md entry 4", "reproduced_by": "FW5:226 slice — 'already means “really explains.”' present with U+201C/U+201D", "also_in_reference": true},
    {"claim": "#15 (FW5:210) CORRECT — the likeliest false positive avoided, with the contrast sentence quoted from the Non-circular dependence paragraph", "evidence": "out/citations.md entry 15", "reproduced_by": "substring test: 'There is at least one admitted contrast that removes or changes a nonempty block of active organizational commitments …' in FW5:210 → True", "also_in_reference": true},
    {"claim": "the other seventeen verdicts, each with its FW5 fragment", "evidence": "out/citations.md entries 1–13, 16–20", "reproduced_by": "28-item substring battery over the named lines: all pass except the two noted below", "also_in_reference": true},
    {"claim": "NEW, and correct against the prompt's own designation: 'the addressable content lines are 1–1502, and FW5:1502 is the last line … 1,503 \"lines\" only if the final \"\" after the last \\n is counted'", "evidence": "out/citations.md, identity paragraph", "reproduced_by": "split('\\n') gives 1503 elements, last repr '' ; sha256 8105925b…e33ee63a matches", "also_in_reference": false},
    {"claim": "NEW: the doubled-citation count in the prompt is under-stated — 'FW5:630 is likewise cited at staging 112 and 113 … equally benign'", "evidence": "out/citations.md, awkward-pointers section", "reproduced_by": "staging lines 112 and 113 both carry FW5:630; line 113 also carries FW5:1200-1206", "also_in_reference": false}
  ],
  "incorrect_claims": [],
  "missed": [],
  "fabricated_apis_or_lines": [
    {"cited": "'(the `\\tag{EK}` is at :841 in the same display)' — entry 7", "actual": "\\tag{EK} is at FW5:836; line 841 is the prose sentence 'The definition is factive about the claimed repair, not about every sentence in the resulting theory.'", "where_in_output": "out/citations.md entry 7, parenthetical aside"},
    {"cited": "entry 1 quotes FW5:172 'verbatim' as 'The following conditions define \\(\\operatorname{Account}(\\mathcal E).'", "actual": "the line is 'The following conditions define \\(\\operatorname{Account}(\\mathcal E)\\).' — the closing \\) was dropped, so the quoted string is not a substring of the named line (tested: False)", "where_in_output": "out/citations.md entry 1. Mitigating: check/verify_final.py line 91 asserts the correct string with \\), so the check was right and the prose transcription slipped."}
  ],
  "followed_house_rules": {"no_score_rank_or_meter": true, "no_exhaustion_language": true, "resource_boundary_named_as_such": true, "unresolved_used_rather_than_invented": true, "no_published_observation_modified": true, "counts_carry_their_command_or_file": true, "breaches": []},
  "verbosity": {"worker_chars": 12382, "reference_chars": 5791, "note": "Roughly double the key; the padding is in the repeated 'No difference.' tag and the three-awkward-pointers section that restates entries already given."},
  "tool_use_reliability": {"tool_calls": 26, "malformed_calls": 0, "refused_commands": 0, "files_read_one_at_a_time_where_a_script_was_called_for": false, "edited_a_file_it_was_told_not_to_edit": false, "verification_command_actually_run": true, "note": "Read the two files once each, then computed: three check scripts, verify_final.py re-run to exit 0 with 51 assertions after the report was written. Sandbox byte-identical to material outside out/ and check/."},
  "overall_note": "Nineteen-and-one exactly as the key has it, with the decisive hit and the bonus both taken and the trap at #15 avoided. Good for a citation audit you intend to act on. Not good if the prose is to be quoted onward unchecked: one 'verbatim' quote lost a backslash-paren and one aside put \\tag{EK} five lines off, in a report whose own method paragraph promises every quote is a substring. Doubt about the reference: the key names FW5:136-137 as where #14's supporting text is; the worker names FW5:1326 ('Changing the current index changes the claim being applied') and FW5:140 ('What is prohibited is changing it during an assessment without recording the resulting change in what is claimed'), both of which I sliced and both of which bear on the claim-change principle more directly than :136 does."
}
```

---

## e-04-f001-classes — COMPLETE, pass 1 (24 iterations, 1,306,658 tokens, 766 s)

```json
{
  "correct_claims": [
    {"claim": "planned set derived, not guessed: 'an arm of kind: \"mini\" is planned once per model-called node … taken from manifests/fork5.json as the stages that carry no machine seat and are not the end marker: account, objection, rival, response, carry', total 89, each occurrence asserted equal to its frozen plan.max_calls", "evidence": "out/f001-classes.md, planned-coordinate table (12 + 7 x 11 = 89)", "reproduced_by": "python3 check/f001_classify.py in a copy → 'planned total: 89', per-occurrence planned=12/11/11/11/11/11/11/11", "also_in_reference": true},
    {"claim": "the seven ceiling rows, coordinate by coordinate (occ-04 mini_fcl objection/rival, mini_prose objection/response; occ-05 mini_fcl rival/response, mini_prose carry)", "evidence": "out/f001-classes.md unresolved table", "reproduced_by": "same run, 'by class: ceiling=7'; rows identical to reference/f001-unresolved-coordinates.txt", "also_in_reference": true},
    {"claim": "the six blocked rows, each tied to the earlier FAILED node that ended its arm", "evidence": "out/f001-classes.md 'blocked coordinates: the earlier FAILED node that ended the arm' table", "reproduced_by": "same run, 'blocked=6'; 'planned, no receipt: 6'; rows identical to the key", "also_in_reference": true},
    {"claim": "ok = 74 ('Receipts found in this copy: 83 (COMPLETE 74, FAILED 7, PARTIAL 2)')", "evidence": "out/f001-classes.md", "reproduced_by": "same run, 'receipts present: 83 {COMPLETE: 74, FAILED: 7, PARTIAL: 2}'", "also_in_reference": true},
    {"claim": "per-occurrence totals occ-04 ceiling 4 / blocked 3, occ-05 ceiling 3 / blocked 1, occ-07 blocked 2", "evidence": "out/f001-classes.md 'By occurrence'", "reproduced_by": "same run's per-occurrence lines", "also_in_reference": true},
    {"claim": "NEW, and a divergence from the key I traced to its source: content bytes for occ-05 mini_fcl/rival given as '7112 (per PLAN.md table, raw responses/*.txt column)'", "evidence": "out/f001-classes.md row 8", "reproduced_by": "grep of PLAN.md line 436: '| 05 | daily/mini_fcl/cycle01/rival | PARTIAL / OPAQUE | INCOMPLETE_GENERATION | 8,192 | 7,112 bytes |' — the key says 7,080. The worker quoted the only record in its sandbox and labelled the provenance in the cell.", "also_in_reference": false},
    {"claim": "the two TRANSPORT_OR_RESPONSE_ERROR coordinates left unclassified with the gap stated: 'the receipt carries neither an error text nor an elapsed time (the key union over all receipts has no such field) … Left unclassified rather than guessed'", "evidence": "out/f001-classes.md 'Coordinates left unclassified'", "reproduced_by": "cat of occurrence-07/responses/daily/mini_fcl/cycle01/objection.json — no elapsed, no error text; grep for 180368/180456/'read timeout'/'elapsed' across AGENTS.md, docs/lessons/operations.md and F001/PLAN.md returns nothing; experiments/analyses is not in the material", "also_in_reference": false}
  ],
  "incorrect_claims": [],
  "missed": [
    {"reference_item": "timeout 2 — occurrence-07 mini_fcl/objection and occurrence-08 mini_fcl/carry, at 180,368 ms and 180,456 ms against the declared 180 s", "source": "answer_key", "severity_note": "Recorded as a miss against the key, but I could not reproduce the key here and I do not hold it against the run: the elapsed time and the read-timeout error text exist only outside the sandbox, and the prompt says 'If a coordinate's evidence does not settle its class, say so and leave it unclassified rather than guessing.' The worker did exactly that and named what would settle it. The task, not the worker, is under-determined."}
  ],
  "fabricated_apis_or_lines": [],
  "followed_house_rules": {"no_score_rank_or_meter": true, "no_exhaustion_language": true, "resource_boundary_named_as_such": true, "unresolved_used_rather_than_invented": true, "no_published_observation_modified": true, "counts_carry_their_command_or_file": true, "breaches": []},
  "verbosity": {"worker_chars": 15474, "reference_chars": 2561, "note": "Six times the key. Every unresolved row repeats 'not recorded (no record in this copy carries one)' in two columns, and two closing sections restate the house rules as negations rather than simply obeying them."},
  "tool_use_reliability": {"tool_calls": 30, "malformed_calls": 0, "refused_commands": 0, "files_read_one_at_a_time_where_a_script_was_called_for": false, "edited_a_file_it_was_told_not_to_edit": false, "verification_command_actually_run": true, "note": "Read PLAN.md, the manifest, one arms/plan pair and four sample receipts, then aggregated. The report is generated by check/f001_classify.py, not hand-written: re-running it in a copy rewrote out/f001-classes.md byte-identically (diff -q: identical). One command used '&&', a shell construct the TOOLING paragraph excludes; the harness ran it."},
  "overall_note": "The table matches the key everywhere the sandbox can settle it, the planned 89 was derived rather than asserted, and the one place the evidence runs out is marked unclassified with the missing field named. Good for a classification you intend to publish. The two deliberate refusals to total across resource conditions ('no endpoint is totalled across conditions') under-deliver against the prompt's literal 'totals … by endpoint', though the components sum to the key's per-endpoint figures. Doubt about the reference: the key's timeout rows and its 7,080-byte figure both rest on records outside the frozen corpus, and PLAN.md — which is inside it — says 7,112."
}
```

---

## Family-level reading

Three of the four tasks produced a deliverable, and on all three this worker did the thing the
family was built to test: it computed rather than recited, and it did not invent. **It found both
decisive hits.** e-01 named `ollama-glm-5.3/fcl/control/rep2.json` with its `finish_reason: length`
and `completion_tokens: 32768`, and e-03 reported "**FW5:133 is an empty line** — it is the blank
separator between the closing `\]` … at :132 and the \(O_p\) paragraph at :134". **It refused the
three traps.** Both unrefutable claims were left standing ("**Verdict: SURVIVES.**", e-01 claims 2
and 3) and the likeliest false positive was declined ("**15.** staging 112 → FW5:210 — **CORRECT**",
e-03). **It stated its evidence gaps instead of filling them**, which is the family's second-most
informative behaviour: "this sandbox slice of F001 contains **no** delivered-bytes files at all
(`*.txt sibling files anywhere under F001: 0`)" (e-01), and "`timeout` is not settled … Left
unclassified rather than guessing" (e-04) — the latter costing it two rows against the key on
evidence that provably is not in the sandbox. **It aggregated with scripts every time**: no task
read receipts one at a time, e-04's report is generated by its own checker and re-runs
byte-identically, and e-03 re-ran a 51-assertion verifier to exit 0 after writing the report. No
file under the frozen material was modified in any of the three sandboxes (`cmp` over every
non-output file), and there were zero malformed tool calls across 104 calls.

The recurring weaknesses are in the prose rather than the computation, and they matter because these
are documents other people read. **Transcription drifts from the verified value**: e-03's entry 1
prints FW5:172 "verbatim" as `…\(\operatorname{Account}(\mathcal E).` while its own
`check/verify_final.py` asserts the correct `…\mathcal E)\).`, and entry 7's aside puts `\tag{EK}`
at ":841" when it is at :836. **Volunteered extras carry the errors**: every incorrect claim I found
in the family sits in material nobody asked for — e-01's §2 recheck, correct that only "8 of the 20
cell coordinates carry `completion_tokens: 8192`", is wrong in its parenthetical "— not 5,488",
because the ninth receipt the report counts is the COMPLETE one and it carries exactly 5,488.
**It writes long**: 11k, 12k and 15k characters against keys of 3.5k, 5.8k and 2.6k, with e-04
repeating "not recorded (no record in this copy carries one)" in two columns of fifteen rows and
closing with two sections that recite the house rules rather than just obey them. **It reaches for
shell syntax** the TOOLING paragraph excludes — `> /tmp/c1.log 2>&1; echo "exit=$?"` (e-01) and
`&&` (e-04) — which the harness accepted without complaint, so the slip cost nothing here but would
elsewhere.

Separating the harness from the worker. These runs are expensive in a way that is the deployment's
doing, not the reasoning's: 764k, 928k and 1,262k prompt tokens for 21k, 25k and 45k completion
tokens, because the whole context is re-sent on every turn, and 481–766 s of wall clock for 20–24
iterations. That is the frame in which e-02's two failures should be read, and neither is a finding
about the worker's adversarial reading. Pass 1 died at the gateway's 300 s wall (`Remote end closed
connection without response` at 360.7 s) after three iterations, with the right seven files read and
no probe yet run. Pass 2's remedy — max_tokens 8192 per turn — moved the failure rather than removing
it: iteration 3 returned `finish_reason: length` with `completion_tokens: 8192`,
`reasoning_content_chars: 35029` and zero visible content and zero tool calls, so the loop ended and
the harness recorded `status: COMPLETE` with `files_written: []`. Any reading of family E must
treat e-02 as **untested**, and the `COMPLETE` label as a harness defect: this is the task whose
honest bottom line is "nothing forbidden is found", and it is precisely the occasion the battery
most wanted to observe. Two further infrastructure effects shaped what I could judge rather than what
the worker did: the truncated file list in e-01's system prompt drove 22 `list_dir` calls before any
aggregation (the prompt anticipates this and the worker followed its advice), and both e-01's and
e-04's keys quote figures — F001 content bytes, the two timeout elapsed times — that exist only
outside the frozen corpus, so on those two points the worker was judged against evidence it could
not have had, and I have said so rather than scoring it down.
