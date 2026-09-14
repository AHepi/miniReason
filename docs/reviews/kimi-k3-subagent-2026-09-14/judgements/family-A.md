# Family A — adversarial code review of the six wave-0 modules

Judged per `battery/rubric.md` §2/§3A against the Opus control on identical bytes (`controls/<id>/FINAL.md`), with `reference/REVIEW-WAVE0.md` read only through `reference/A-CODE-staleness-note.md`. Every claim I call correct I re-executed myself, in throwaway copies of the control sandboxes at `scratchpad/judgeA/<task_id>/` with both sides' probe trees copied in beside them (`probe_opus/`, `probe_kimi1/`, `probe_kimi2/`). Nothing under `kimi/` or `/home/user/miniReason` was written except this file. No score, no rank, no total.

**src integrity, all 18 sandboxes (3 Kimi passes + control × 6 tasks):** no file under `src/` modified or added on either side — walked each sandbox's `src/` and sha256-compared against `battery/material`.

**What the three passes actually produced.** Kimi wrote a review file for two of six tasks. `status: COMPLETE` in pass 2/3 is not delivery: in `runs-pass2/{a-01-types,a-03-standard,a-05-receipts}` and `runs-pass3/a-06-publish` the last turn is `finish_reason: "length"`, `completion_tokens: 8192`, `content: ""`, no tool calls, `files_written: []`, with `reasoning_content_chars` 32,760 / 33,396 / 33,500 / 34,316 — the whole per-turn ceiling spent on reasoning, nothing emitted.

| task | pass 1 (32768 / 40 iters) | pass 2 (8192 / 80) | pass 3 | review file |
|---|---|---|---|---|
| a-01-types | ITERATION_CAP, 14 probes, no review | length-stall, nothing | — | none |
| a-02-contracts | ITERATION_CAP, 8 probes + review | COMPLETE, 15 probes + review | — | both passes |
| a-03-standard | ITERATION_CAP, 13 probes, no review | length-stall, nothing | — | none |
| a-04-custody | COMPLETE, 9 probes + review | not re-run | — | pass 1 |
| a-05-receipts | TRANSPORT error at 338 s, nothing | length-stall, nothing | — | none |
| a-06-publish | TRANSPORT error at 322 s, nothing | HTTP_500 at 184 s | length-stall, nothing | none |

Pass 3 for a-06 had finished before I judged it (`result.json` written 11:51:47, `files_written: []`); its status is recorded above, not left open.

---

## a-01-types

**KIMI** (pass 1 capped, primary; pass 2 stalled)
- *correct_claims:* none recorded — no review file on any pass, so no claim was put. Its 14 probes do run and do reach real behaviour: `probe_kimi1/p06_receipt_uniqueness_and_failurecode.py` prints `U3 invented-but-uppersnake failure_code ACCEPTED; in FAILURE_CODES? False` (reproduced by me) — a finding the control did not make, which no pass ever wrote down.
- *incorrect_claims / fabricated_apis_or_lines:* none (none made).
- *missed*, all reproduced by me: `_digests` folds `x` and `./x` into one key, so `loop_plan_id` is pin-order dependent and an added pin is silently dropped (`probe_opus/p01_pin_key_normalisation.py`: `two pins -> 48ca352b…` equals `one pin`; `order 1` ≠ `order 2`); `CustodyReport.from_mapping`/`from_findings` accept the bare string `"SOURCE_PIN_MISMATCH"` and publish 19 one-character checks into a step receipt (`p03_custody_checks_string.py`); `StepReceipt.key` refuses `cycle=0` under `CONFIG_INVALID_VALUE` where `RunPaths.cycle(0)` uses `CYCLE_OUT_OF_RANGE` (`p02_code_routing.py`); `is_stop_reason('preregistered_condition:exhaustion')` is `True` (my own `python3 -c`).
- *followed_house_rules:* no prose to breach; breaches: none.
- *verbosity:* worker_chars 0, reference_chars 37,883. The cap fell at iteration 40 while it was writing probe #14 (`write_file` was the last call); no finding was ever put in prose.
- *tool_use_reliability:* 52 calls (13 `run_command`), 0 malformed, 0 refused, no `src/` edit; `run_tests.py` reached (said so at iteration 39); probe-first discipline real, review never started.
- *overall_note:* a reviewer's raw material without the review — evidence that the module was probed, not an answer to the task.

**OPUS control**
- *correct_claims:* BLOCKER 1, BLOCKER 2, SHOULD-FIX 3, SHOULD-FIX 4 all reproduced by me with the commands above; each pinned to a file and line range and quoting the docstring or design clause it contradicts.
- *incorrect_claims:* none among those four. *fabricated_apis_or_lines:* none — every line I sampled (pin/step paths, `_ID` at `types.py:482`) is where it says.
- *missed:* the accepted-but-undeclared `failure_code` Kimi's p06 exposes.
- *followed_house_rules:* no score/rank/meter; "exhaustion" appears only as the token under review; breaches: none.
- *verbosity:* 37,883 chars; 11 findings plus failed attacks plus unresolved items. Dense, not padded.
- *tool_use_reliability:* 9 probes, all runnable from a clean copy; no `src/` edit.
- *overall_note:* I executed four of its eleven findings; SHOULD-FIX 5 and NOTE 6–11 I did not run and do not certify here.

**Comparison.** One side produced a review, the other produced probes; nothing to overlap. The single Kimi-only item in the task sits in probe output no pass turned into a claim.

---

## a-02-contracts — the one task with Kimi output on both passes

**KIMI**, pass 2 primary (latest complete, 16,161 chars, 15 probes), pass 1 partial (19,793 chars, 8 probes) marked where it differs.
- *correct_claims:*
  * [pass 2 F1 = control S2] "the published, digest-pinned *same objects* are mutable in place … the pinned digest does not move" — `probe_kimi2/p06b_restore.py` reprints `mutated : check RAISED KeyError: 'answer'` and `recomputed digest == pinned digest: False`; the control reaches the same seam via `CRITIC_SCHEMA['properties']['relation']['enum'].append('outperforms')`. Hit.
  * [pass 1 S1 = control B1] "a deeply nested byte string escapes the contract layer as `RecursionError`" — `probe_opus/p02_not_json_depth.py`: `str depth=1000 (2000 chars): RAISED RecursionError`. Hit, found only by pass 1.
  * [pass 1 S2, Kimi-only] the judge schema admits an empty `reading_note`: `check('judge', {'sustained': True,'decisive_point':'p','reading_note':''})` → `ok=True` (my own `python3 -c`); `standard.py:831` is `_text_schema()` with no `min_length` against `:817`/`:830` which have one. The control never mentions `reading_note`.
  * [pass 1 N4, Kimi-only] `notes/WAVE0-INTERFACE.md:49` says "`FORBIDDEN_KEYS` (G12, 24 keys)"; `len(standard.FORBIDDEN_KEYS)` is 25. The control printed 25 and never compared it to the interface line.
  * [pass 2 F2] the variator schema is `minItems: 1` with no `maxItems` while `GUARD_PARAMETERS['paraphrase_n']` is 2; three paraphrases validate `ok=True` (my run).
  * [pass 2 F3, F5] the `AGGREGATE_KEYS` boundary and the O2 `verdict` collision reported as confirmations rather than defects — both reproduce exactly as printed.
- *incorrect_claims:*
  * [pass 2] "The one way `check` raises is the deliberate in-place schema mutation of F1" — false on these bytes and falsified by Kimi's own pass 1. A universal asserted where the probes covered a sample. Not stale: a fresh over-generalisation.
  * [pass 2] "`.as_dict()` round-trips through `check` for nominal, `none` and outside-vocabulary rows alike", offered as an attack that failed. The dict does round-trip, but Kimi's own `probe_kimi2/p03_outside_vocabulary.py` prints an `.as_dict()` with no `nominated_relation` in it — the control's S3 finding, in Kimi's own output, read past.
- *missed*, reproduced by me: control B2 — `assert_no_aggregate_fields({'type':'object'})` passes, because the closure check is gated on `properties` being a Mapping (`contracts.py:618-623`), the exact case its docstring names; Kimi's `p12_aggregate.py` tested an object *with* `properties`, where the guard holds. Control S3 (`nominated_relation` dropped from the record). Control N2 — `assert_no_scoring_keys` passes a `memoryview`, a `set` and a tuple-of-pairs in silence while `str`/`bytes` now raise. Not run by me: S1, S4, S5, N1, N3–N6.
- *fabricated_apis_or_lines:* none. I checked 13 cited lines in `contracts.py` and 5 in `standard.py` from the pass-2 review; each is what it says.
- *followed_house_rules:* no score, rank or meter; resource boundary named as such; counts carry their command ("`python3 run_tests.py` → `Ran 0 tests … OK`"). breaches: one borderline word, pass 1 line 79 — "so I rank only the `check` escape as a published-seam violation" — used to mean *classify*, not to order.
- *verbosity:* pass 2 16,161 chars against the control's 47,359; pass 1 19,793. Compact and mostly load-bearing; the cost of the compression is coverage, not padding.
- *tool_use_reliability:* pass 2 — 68 calls, 28 `run_command`, 0 malformed, 0 refused, no `src/` edit, `run_tests.py` run and its emptiness reported, 56 iterations. Pass 1 — 58 calls, review written before the cap fell.
- *overall_note:* the pass-2 review is honest about method and exact about lines, and its one blocker-grade seam is real; it under-attacks the parse path, and its two "could not break" sentences are stronger than what it executed.

**OPUS control**
- *correct_claims:* B1 (RecursionError at ~1000 levels), B2 (open object admitted), S2 (guard content editable, digest unmoved), S3 (`nominated_relation` absent from `as_dict()`), N2 (five container shapes silent) — all reproduced by me.
- *incorrect_claims:* none reproduced. One heading over-reaches its body: "the `not-json` reason the module promises never appears" reads as general, and `check('defender','{not json')` does return `not-json`; the body correctly says it is *this input* that never reaches it.
- *missed:* the empty `reading_note`; the interface's 24-vs-25 count.
- *fabricated_apis_or_lines:* none (`_as_object` at 658–667, `check` at 793–796 verified).
- *followed_house_rules:* clean; breaches: none. *verbosity:* 47,359 chars, 13 findings, five failed attacks, five unresolved items. *tool_use_reliability:* 16 probes, no `src/` edit, `run_tests.py` run and reported as `Ran 0 tests`.
- *overall_note:* the strongest of the six controls, and the only one whose unresolved section names a limit of its own probes (B2's nine schemas are its own; no shipped schema exhibits the hole).

**Comparison.** Two hits, arriving on different Kimi passes — the run the harness called COMPLETE found the mutable-guard seam and lost the parse-path seam the capped run had already found. Kimi contributes two small verified items the control missed, both in the module's *declared* surface (a missing floor, a wrong count in the interface note); the control contributes the two seams that would break a cell at run time.

---

## a-03-standard

**KIMI** (pass 1 capped, 13 probes, no review; pass 2 stalled)
- *correct_claims:* none recorded. The probes reach the right neighbourhood — `probe_kimi1/p08_reconciliation.py` reproduces the repaired `assert_config_matches_standard` refusals, and `p04_scoring_headers.py` probes the pipe-table header rule one character away from the control's S6 construction and reports its own hypothesis as not reproduced — but no claim was written.
- *incorrect_claims / fabricated_apis_or_lines:* none (none made).
- *missed*, reproduced by me: B1 — `build_standard` emits a body whose `guard_parameters.reopen_reasons` and top-level `reopen_reasons` disagree, and a config matching the registered body is refused (`GUARD_PARAMETER_INVALID`) while one contradicting it is admitted (`probe_opus/p02_successor_body.py`); B2 — a truncated `ceiling_v1.md` publishes `CEILING_REQUIRED_SENTENCES = ()` and the body still builds, and a widened `marks` list puts `'better'` into the mark vocabulary unrefused (`p10_import_time_reads.py`); S5 — the exhaustion exemption survives a 50-column blockquote wrap and is refused at 60/70/80 (`p03_exhaustion_scan.py`); S6 — a prose line ending in `|` hides the next table's header from G12, which I reproduced with my own two-file `python3 -c` (backtick REFUSED, pipe ADMITTED). Not run by me: S3, S4, N7–N13.
- *followed_house_rules:* no prose; breaches: none. *verbosity:* 0 chars against 44,597.
- *tool_use_reliability:* 51 calls pass 1, 0 malformed, no `src/` edit; pass 2 stalled after 8 `read_file` calls and one 8192-token reasoning turn.
- *overall_note:* probes without a verdict. The pass-2 ceiling cost everything here: 6 iterations, 8 reads, no probe, no text.

**OPUS control**
- *correct_claims:* B1, B2, S5, S6 reproduced by me as above. *incorrect_claims:* none reproduced; S5's heading ("does not survive a blockquote") is wider than its own evidence, which shows one wrap width admitted.
- *missed:* nothing I can name — Kimi put no claim on this task. *fabricated_apis_or_lines:* none (`_is_pipe_row` at 241–254, the `continue` at 296–297 are where it says).
- *followed_house_rules:* clean; breaches: none. *verbosity:* 44,597 chars, 13 findings. *tool_use_reliability:* 12 probes, no `src/` edit, `run_tests.py` run.
- *overall_note:* S6 is the sharpest finding in the family — one character changes the verdict of a pre-registered guard — and it is stated as a rendering rule, not a curiosity.

---

## a-04-custody — the one task Kimi completed

**KIMI** (pass 1 COMPLETE, 20,939 chars, 9 probes; not re-run later)
- *correct_claims:*
  * SHOULD-FIX 2, Kimi-only: `_pin_key`'s `str(entry)` at `custody.py:427` coerces a non-string pin key, so `verify_pins({'pins': {7: '0'*64}})` returns `SOURCE_PIN_MISSING` on path `'7'` instead of naming the malformation — "a custody *finding*, indistinguishable in the receipt from a real missing file". Reproduced by `probe_kimi1/p08_nonstring_key.py`, and independently by the control's own `probe_opus/p04_pins.py` (`integer pin key returned [('SOURCE_PIN_MISSING','1')]`), which the control printed and did not report.
  * SHOULD-FIX 1, ordering half: in `write_new` the credential scan (`:386`) runs before the existence check (`:389`) — verified against the frozen source.
  * NOTE 3: `pins` canonicalises `./src/a.py` to `src/a.py` and collapses two spellings of one file into one pin with no signal (my `python3 -c`: `pins(repo, ['./src/a.py'])` → `{'src/a.py': …}`).
  * NOTE 4: the credential scan is a two-rendering substring scan; base64 and a split value are written to disk (`probe_kimi1/p04_credential_scan.py`, both `RESULT FAIL` lines reproduced), correctly reported as a documented bound and not a defect, with O8 quoted for the boundary.
- *incorrect_claims:*
  * SHOULD-FIX 1's contradiction half over-reads its own evidence: the bytes left on disk are the intruder's, created by the probe's caller-level wrapper, not bytes `write_new` wrote, so `CustodyMismatch`'s "nothing was written or accepted" is not falsified. The ordering fact stands; the docstring contradiction does not.
  * NOTE 3's probe label "verify_pins accepts the './' spelling pins() refuses" is false as written — `pins` accepts it too (my run). The review's prose avoids the error ("pins would emit only the bare key"); the probe line does not.
  * "BLOCKER — none reproduced … a path escaping the run root is refused, including the symlink … constructions a text-prefix fence would miss" — true for symlinks leaving the root, and the control's B1 breaks the same guard from inside it.
- *missed*, reproduced by me: B1 — the documented pairing `write_new(fenced(root, rel), value)` writes *through* an in-root symlink, so the record lands at `cycles/0/decision.json` while the caller named `steps/0001-S0.json` (`probe_opus/p12_fence_disarms_symlink_refusal.py`: `write_new(raw path)` refuses, `write_new(fenced(...))` writes); B2 — a pin digest with a trailing newline is reported as `SOURCE_PIN_MISMATCH` with `expected='…806\n'`, a false statement about the tree, because `_SHA256 = re.compile(r"^[0-9a-f]{64}$")` at `:174` matches before a trailing newline (`probe_opus/p04_pins.py`); B3 — `ValueError`, `RuntimeError` and a raw `FileExistsError` escape `pins`/`fenced`/`write_new` uncoded on NUL keys, symlink loops and a file-as-parent (`probe_opus/p06_verify_pins_escapes.py`). Not run by me: control SF1–SF3, N1–N5.
- *fabricated_apis_or_lines:* none. Every cited line (`:177`, `:368-371`, `:384-391`, `:427`) is exactly what the review says.
- *followed_house_rules:* no score, rank or meter; "Rank nothing" honoured; resource boundaries named; the acceptance clause quoted verbatim before use; counts carry their command ("`python3 run_tests.py` → Ran 0 tests in 0.000s, OK"); every probe scrubs its environment and says so. breaches: none.
- *verbosity:* 20,939 chars against 44,229 — four findings and seven failed attacks against the control's twelve findings.
- *tool_use_reliability:* 69 calls, 33 `run_command`, 0 malformed, 0 refused, no `src/` edit, verification command run. Every probe I re-ran printed exactly the lines the review quotes; the quoted-verbatim rule was kept, not approximated.
- *overall_note:* the best Kimi artifact in the family, and a fair one — it declares "BLOCKER — none reproduced" rather than promoting a note, and names the credential scan's bound instead of selling it as a detector. What it does not do is attack the *documented composition* of two functions, which is where all three control blockers live.

**OPUS control**
- *correct_claims:* B1, B2, B3 reproduced by me with the commands above. *incorrect_claims:* none reproduced among the three. *fabricated_apis_or_lines:* none.
- *missed:* the non-string pin key (its own probe printed the evidence); the `./`-collapse note.
- *followed_house_rules:* clean; the BLOCKER/SHOULD-FIX/NOTE order is stated as a kind, not a rank. breaches: none. *verbosity:* 44,229 chars, 12 findings, a failed-attack section and a "Suspected and could not reproduce" section. *tool_use_reliability:* 13 probes, no `src/` edit.
- *overall_note:* I executed three of its twelve findings; SF1–SF3 and N1–N5 I did not run and do not certify.

**Comparison.** The only task where both sides answered. The finding sets barely intersect: Kimi attacked each function alone and found two real weaknesses in the pin key space and the write ordering; the control attacked the pairs the docstrings tell callers to use (`fenced`+`write_new`, digest-string+tree-statement) and found three. Kimi's probes reproduce to the character; its reach is one seam short.

---

## a-05-receipts and a-06-publish

**KIMI — nothing, on every pass.** a-05: pass 1 died at 338 s on `TRANSPORT_OR_RESPONSE_ERROR` after 12 tool calls; pass 2 stalled at 8192 reasoning tokens after 4 reads. a-06: pass 1 died at 322 s after 7 reads; pass 2 returned `HTTP_500` at 184 s; pass 3 stalled the same way as pass 2. No probe, no review, no claim, no house-rule surface, no `src/` edit; verbosity 0 chars against 45,471 and 46,080; `malformed_tool_call_retries` 0 in all five attempts. The runs ended before method could be observed.

**OPUS control, a-05.** *correct_claims* reproduced by me: B1 — `open_receipt(render=…)` hands `REC-20260914-A` to two different callers when the rendered paragraph omits the id (`probe_opus/p09_render_id.py`; the control quotes the `collision : False` line that softens its own headline); B2 — `DEFAULT_LEDGER_PATH` resolves by walking for `tools/repo_activity.py`, and a default-path receipt appended into another checkout's ledger (`p14_default_root.py`); S5 — plainly credential-bearing command text walks through `_COMMAND_TEXT_MARKERS` (`p11_command_text.py`: `psql postgres://loop:hunter2…`, `ssh -i …id_ed25519`, `X-Api-Key:sk-live-…` all ACCEPTED while `export DEEPSEEK_API_KEY=…` is refused). Not run by me: S1–S4, S6, S7, N1–N7. No fabrication found; house rules clean; 45,471 chars, 17 probes, no `src/` edit.

**OPUS control, a-06.** *correct_claims* reproduced by me: B1 — a bracketed path name reaches git as a pathspec glob and publishes `report1.md`, a file the caller never named and the scan never walked, carrying the synthetic credential (`p02_bracket_defeats_credential_scan.py`: `scan 1 walked ('report[1].md',)`, `publish files ('report1.md','report[1].md')`, `remote blob carries value True`); B2 — the history-rewrite guard matches flags by exact token, so `push --force-with-lease=<ref>:<sha>`, `commit --amen`, `add -A` and `commit -a` get through and a published ref is force-updated (`p03_guard_argv_escapes.py`). Not run by me: S1–S5, N1–N5. No fabrication found; house rules clean; 46,080 chars, 17 probes, no `src/` edit. Method note: its probes drive a real `git` binary from inside `python3`, which the TOOLING paragraph excludes at the `run_command` layer; the control names its ground (design §4.7, "every git operation runs against a real bare repo in a temp dir through the same `publish()` path") and `publish.py` cannot be executed at all otherwise. Recorded, not scored.

**Staleness, both directions.** No stale finding on either side: nothing either side wrote restates a row the note marks repaired, and both went the other way where it counted — the control's a-06 B2 prints the eight previously-destructive argvs being *refused* before showing four new spellings that are not, and its a-02 N2 shows `str`/`bytes` now raising before naming `memoryview`/`set`/tuple as still silent; Kimi's pass-2 a-02 reports the repaired `VALIDATORS[…]` register forwarding and the repaired `assert_no_scoring_headers` as working, and its a-03 probes reprint the repaired config reconciliation. Both sides reproduce the still-live row N4 (`_read_back` at `publish.py:720`, used at `:878`). **One doubt about the reference itself:** the note's row N2 says `custody.write_new` does not fsync the parent directory and calls it *live*. On the frozen bytes it does — `_fsync_directory(target.parent)` at `custody.py:400`, with the promise in the docstring at `:374-379`. Anyone scored against that row would be scored against a stale row *in the staleness note*.

---

## Family-level reading

**Kimi, recurring.** Where it produced a review it probed rather than recited, and its quoted evidence is trustworthy: every Kimi probe I re-ran printed the lines its review quotes, to the character (a-04, nine probes; a-02 pass 2, four re-run). Its line citations are exact — eighteen checked across a-02 and a-04, none wrong, no invented function, line or code. It holds the house line unprompted: "No published seam was reproduced as unsound … The four findings below are weaknesses around the seams" (a-04) is a refusal to promote a note into a blocker. The recurring weakness is the shape of the attack, not its honesty: it tests functions one at a time and rarely tests the *composition* the docstring recommends, which is where all three a-04 blockers and the a-06 pathspec blocker live. Second, and more expensive: it generalises past its probes — "The one way `check` raises is the deliberate in-place schema mutation of F1" (a-02 pass 2) is false, and its own pass 1 had already found the counterexample; in the same review it printed an `.as_dict()` with the nomination missing and wrote "round-trips … alike" underneath it. Third, coverage is not monotone across passes: the capped pass-1 run found a seam the completed pass-2 run lost.

**Opus, recurring.** All fourteen control findings I executed reproduced, across six modules, and the controls consistently separate a repaired behaviour from a live one before claiming anything (a-06 section D; a-02 N2). The "What I could not determine" sections are real limits — a-02's names that B2's nine schemas are its own invention and that no shipped schema has the hole. The recurring weakness is headline compression: "the `not-json` reason … never appears" (a-02 B1) and "does not survive a blockquote" (a-03 S5) both read wider than the accurate bodies beneath them. Volume is the other cost: 37–47 KB per review, where the load-bearing content of a-04 is perhaps half that.

**Harness and infrastructure, separated from worker behaviour.** Four of six tasks produced no Kimi artifact for reasons that are not review quality. (1) The 40-iteration cap truncated a-01 and a-03 mid-probe in pass 1 — a-01's fortieth call was a `write_file` of probe #14, a-03's a `run_command`; both had material, neither had begun the review. (2) The 300 s gateway wall killed a-05 at 338 s and a-06 at 322 s in pass 1, before either wrote anything. (3) The 8192-token per-turn ceiling in pass 2/3 is decisive: four runs spent the entire turn budget on `reasoning_content` (32.7k–34.3k chars) and returned empty content with no tool call, recorded as `status: COMPLETE, files_written: []`. That status must not be read as delivery. (4) `HTTP_500` ended pass 2 of a-06 at 184 s. (5) Context re-sending is the mechanism behind the cap: a-02 pass 1 sent 3,698,138 prompt tokens to produce 52,581 completion tokens, pass 2 sent 5,199,979 to produce 29,243 — the sandbox is re-sent every iteration, so an iteration cap is a reading budget as much as a thinking budget, and Kimi's one-probe-per-iteration rhythm (write, run, read, write) spends it fastest. (6) Tool hygiene was never the limiter: `malformed_tool_call_retries` is 0 in all eleven Kimi runs, no command was refused, and neither side edited anything under `src/` in any of the eighteen sandboxes. Family A's sandboxes were all importable — the missing-sibling-import defect found in family B does not occur here; every probe I ran on either side imported `minireason.loop.*` cleanly.
