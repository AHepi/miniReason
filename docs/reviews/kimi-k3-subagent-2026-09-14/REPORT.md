# Kimi K3 as a subagent: where it is strong, where it is weak

Owner's report, 2026-09-14. Authorised by ruling 11 (Kimi K3 deployed as a worker, not a study
subject) and written for ruling 16 (Kimi K3 as the default worker for mechanical work).

**How to read the evidence in this report.** Every count names the file it was computed in and what
it counts. Every quoted worker claim names the judgement file that carries it, and says whether the
Opus judge **reproduced** it by running something or only **read** it — the six judges were
instructed to execute before judging (`battery/rubric.md` §2), and each of them recorded which of
their own certifications they ran and which they did not. There is no score, no ranking and no
percentage verdict anywhere in this report, per `battery/README.md` §5. Statements about the worker
are about these occasions on this corpus, not about a model in general.

---

## 1. The answer, in one paragraph

Kimi K3 is strong at work that can be *computed*: it writes a script, runs it over the records,
re-runs it to check itself, and reports what the records say — including when what they say is
"nothing is wrong here", which it does plainly instead of manufacturing a finding. Its citations of
lines and symbols it actually opened are exact, it names the gap when the evidence runs out instead
of filling it, it diagnoses a broken environment precisely rather than faking an answer around it,
and it corrects itself within a turn when a tool call comes back wrong. It is weak wherever the
answer has to be *built and then checked by hand*: it writes a file and walks away without parsing,
importing or running it — in the four implementation tasks it never once invoked the test command
the prompts told it to iterate against — it states confidently that a symbol or line exists in code
it did not execute, it generalises a universal from a sample its own earlier probe had already
falsified, its prose drifts from figures its own checker got right, and it drops source material
when transcribing (four zeros reported as three, fourteen obligation members dropped). It attacks
functions one at a time and misses the seams where two documented calls compose, and its mistakes
cluster in extras nobody asked for. Dominating all of it is one infrastructure fact: the per-turn
generation ceiling. The battery's passes 2 and 3 ran with `max_tokens` 8,192 per turn, and this
model's native reasoning is billed against that budget — sixteen runs spent the **entire** 8,192
tokens on reasoning (27,777–36,797 characters of it) and returned no text and no tool call, which
the old harness recorded as `COMPLETE` with nothing written (`kimi/RUNS-RECLASSIFIED.md`). Fifteen of
twenty-six battery tasks therefore have no genuinely complete run, and most of what looks like
failure in families A, B and C is that ceiling, not the worker's judgement. With the ceiling raised
to 24,576 and the context cut to two or three files, the first production tasks completed and
delivered (§6); and since the battery closed, the harness has been ported to Ollama's native
endpoint, the one surface where a reasoning control is actually honoured — one smoke task ran four
turns on 28, 0, 0, 0 characters of reasoning against 27k–37k *per turn* on the old surface (§5.7).
That is one smoke task: the battery itself ran entirely on the old surface, and none of its
per-turn-ceiling losses had yet been re-tested under the new transport. **Section 8, added
2026-09-14, supersedes that last caveat:** pass 4 re-ran all fourteen ceiling losses on the native
transport and an Opus judge has read them, and fourteen of fourteen now deliver.

---

## 2. What was run

**The battery.** Twenty-six tasks: twenty-five across six families of this project's real work, plus
`b-004`, the harness's own packed-context self-check, which belongs to no family
(`battery/README.md` §3; family counts from `battery/evaluation.json`: A. CODE REVIEW 6, B. TEST
WRITING 4, C. IMPLEMENTATION 4, D. DOCUMENT WORK 4, E. ADVERSARIAL / VERIFICATION 4, F. DATA / TOOL
USE 3, G. HARNESS SELF-CHECK 1). Every task was phrased exactly as the orchestrator would phrase it
to an Opus subagent, ran against a frozen corpus (`battery/material`, 432 files pinned in
`MANIFEST.sha256`), and never read the live repository.

**The fifteen Opus controls.** `battery/evaluation.json` marks `opus_control: true` on fifteen task
ids — all six of family A, all four of C, all four of D, and `f-02-commit-tree` — and
`kimi/controls/` holds fifteen control directories with a `FINAL.md` each; ruling 15 records all
fifteen complete. *Documentation defect, named so the count carries its file:* `battery/README.md`
§4 and `battery/rubric.md` §1 both open "Ten tasks carry `opus_control: true`" and then enumerate
fifteen. The enumeration, `evaluation.json` and the directory agree; the word "ten" is wrong.

**The six Opus judges**, one per family, each instructed to re-execute the claims they certify
(`rubric.md` §2). They did: family A re-ran both sides' probes in throwaway copies at
`scratchpad/judgeA/`; family B re-ran the suite, applied both mutations and rebuilt a
dependency-complete sandbox; family C re-ran every control suite and both cross-run directions;
family D re-opened every source line and re-ran the arithmetic; family E re-derived each answer key
and re-ran each worker's scripts; family F wrote five fresh aggregation scripts of its own. Each
judge also names what it did **not** run — family A: "I executed four of its eleven findings;
SHOULD-FIX 5 and NOTE 6–11 I did not run and do not certify here" (`judgements/family-A.md`, a-01).

**The three passes, side by side.** Recorded labels from each pass's `SUMMARY.md`; reclassified
labels from `kimi/RUNS-RECLASSIFIED.md`, which re-read all 47 `result.json` / `transcript.jsonl`
pairs and altered no record.

| | pass 1 | pass 2 | pass 3 |
|---|---|---|---|
| tasks dispatched | 26 (all) | 17 (every pass-1 non-COMPLETE) | 4 (every pass-2 HTTP_500) |
| per-turn `max_tokens` | 32,768 | 8,192 | 8,192 |
| iteration cap | 3–40 per task | 80 | 80 |
| why this pass was run | the battery as designed | pass 1 lost 12 runs to the 300 s gateway wall; a tool-loop turn "rarely needs more than 8-16k" (ruling 13c, `PASS1-INTERIM.md`) | the four pass-2 runs that died on provider `HTTP_500` |
| recorded | COMPLETE 10, ITERATION_CAP 4, HARNESS_FAILURE 12 | COMPLETE 13, HARNESS_FAILURE 4 | COMPLETE 4 |
| reclassified | unchanged | COMPLETE 1, **INCOMPLETE_TURN 12**, HARNESS_FAILURE 4 | **INCOMPLETE_TURN 4**, COMPLETE 0 |
| tasks with a worker artifact | 15 | 2 (`a-02` review, `c-04` module) | 0 |
| dominant stop | `TRANSPORT_OR_RESPONSE_ERROR` at the 300 s wall (12 runs) | turn budget spent entirely on reasoning (12 runs) | turn budget spent entirely on reasoning (4 runs) |

Across all 47 runs the reclassified totals are COMPLETE 11, HARNESS_FAILURE 16, INCOMPLETE_TURN 16,
ITERATION_CAP 4; 16 rows changed label, all of them recorded `COMPLETE` and all of them delivering
nothing (`RUNS-RECLASSIFIED.md`).

**Honest artifact tally per family.** "Artifact" = at least one file the worker itself wrote at a
path the task declared in `expected_outputs`, on any pass, read off the `[+]` marks in
`RUNS-RECLASSIFIED.md`. "Full deliverable set" = every declared output present on some pass.

| family | tasks | any worker artifact | full deliverable set | what the judge could actually judge |
|---|---|---|---|---|
| A. code review | 6 | 4 (`a-01`, `a-03` probe trees only; `a-02`, `a-04` probes + review) | 2 (`a-02`, `a-04`) | two reviews; `a-05`, `a-06` produced nothing on any of five attempts |
| B. test writing | 4 | 1 (`b-02` test file) | 1 (`b-02`) | one suite, and it is vacuous — all 49 tests skip (battery defect, §5) |
| C. implementation | 4 | 2 (`c-02` `roles.py`, `c-04` `decide.py`) | 0 | two files, **both un-parseable**; no test file on any task on any pass |
| D. document work | 4 | 3 (`d-02`, `d-03`, `d-04`) | 3 | three documents; `d-01` failed twice for two different provider reasons |
| E. adversarial | 4 | 3 (`e-01`, `e-03`, `e-04`) | 3 | three; `e-02` — the task whose honest answer is "nothing forbidden found" — untested |
| F. data / tool use | 3 | 3 | 3 | three, the only family that survived pass 1 intact |
| G. self-check | 1 | 0 | 0 | none |

Sixteen of twenty-six tasks produced any artifact; twelve produced their full declared set; eleven
have a run that is genuinely COMPLETE (`RUNS-RECLASSIFIED.md` final section).

**Integrity, everywhere it was checked.** No worker edited a file it was told not to edit, on either
side, in any sandbox: 18 family-A sandboxes walked and sha256-compared against `battery/material`
(`family-A.md`), 9 family-B (`family-B.md`), family C by `scratch-C/integrity.py`, 7 family-D
against `MANIFEST.sha256`, and family E/F by `cmp` over every non-output file. `malformed_tool_call_retries`
is 0 in every Kimi run recorded.

---

## 3. Strengths

### 3.1 Scripted aggregation and computation

Judge F re-derived every figure independently before scoring, then re-ran the worker's own scripts in
fresh copies. On all three of its tasks Kimi opened a handful of records as schema samples and
computed the rest in code, and on two it wrote a second, independent pass.

* `f-01-c001-profile`: "the slug-to-family map is read at runtime: `slug_to_family = {e["name"].replace("/", "-"): e["family"] for e in registry}`" — judge **reproduced** by `grep -n family check/c001_profile.py`, and the whole table by `python3 scratchpad/judge-f/f01.py` (`judgements/family-F.md`). Method note in the same verdict: "five receipts opened as schema samples, then all 240 aggregated by `check/c001_profile.py`; a second, independently-written `check/check_c001_profile.py` recomputes and asserts. … Re-run in a fresh copy: both exit 0 and regenerate a byte-identical `out/c001-profile.md`."
* `e-04-f001-classes`: "The report is generated by `check/f001_classify.py`, not hand-written: re-running it in a copy rewrote `out/f001-classes.md` byte-identically (`diff -q`: identical)" — judge **reproduced** (`judgements/family-E.md`).
* `f-03-occ02-usage`: "per-call reasoning share reported as a range over the twenty, 0.6455 (original/rep5) to 0.8469 (recoding/rep1), with no average" — judge **reproduced** by `python3 scratchpad/judge-f/f03.py`, "min/max and both extremum holders match" (`family-F.md`). The rubric's own trap for this task was a mean creeping in; it did not.
* Judge F's family-level reading: "Every one of my fresh-copy re-runs regenerated the delivered file byte-identically, and no figure in any of the three outputs failed to reproduce."

### 3.2 Line-accurate citation and exact quoting

* Family A: "its line citations are exact — eighteen checked across `a-02` and `a-04`, none wrong, no invented function, line or code" and "every Kimi probe I re-ran printed the lines its review quotes, to the character (a-04, nine probes; a-02 pass 2, four re-run)" — judge **reproduced** (`judgements/family-A.md`, family-level reading). In the `a-04` verdict: "Every cited line (`:177`, `:368-371`, `:384-391`, `:427`) is exactly what the review says."
* Family D: "every citation I checked resolved to the construct named — `steps.py:465-466` for "held by pid `<pid>` since `<started_utc>`", `types.py:1095` for the `step_key` formula, `steps.py:624` for `check_deadline` (all d-02) — and I found **no fabricated code, line or figure in any of the three documents**" — judge **reproduced** each by `sed -n` / `grep -n` (`judgements/family-D.md`).
* `d-04`: "every figure I re-derived from the table matches exactly, including the three-way distinction between the applied 600 s clock, the 180 s registry row and the 300,270 ms close" — judge **reproduced** by cell-by-cell compare of all ten coordinate rows (`family-D.md`).

### 3.3 Finding the decisive hit

The battery planted one decisive hit in each of three tasks. Kimi took all three.

* `e-01-refute`: "Claim 1 REFUTED IN PART" with the coordinate named in full — "responses/ollama-glm-5.3/fcl/control/rep2.json — status: PARTIAL, failure_type: INCOMPLETE_GENERATION, provider_status: INCOMPLETE_GENERATION, finish_reason: length, completion_tokens: 32768" — judge **reproduced** by `python3 scratchpad/judge_e01.py` (`judgements/family-E.md`). Its own gloss on why the error was invisible: "The count arithmetic in (a) balances either way (11 + 9 = 20), which is exactly why the misplacement is invisible to anyone who checks only the count."
* `e-03-fw5-citations`: "#14 … WRONG. **FW5:133 is an empty line** — it is the blank separator between the closing `\]` of the answer-profile (Q) display at :132 and the `\(O_p\)` paragraph at :134" — judge **reproduced** by slicing FW5 (`family-E.md`). Nineteen-and-one, exactly as the key has it.
* `f-01`: "the twentieth coded receipt is `ollama-glm-5.3/fcl/control/rep2`, `finish_reason` length, `completion_tokens` 32768 — the decisive detail", judge **reproduced**; "the decisive f-01 trap was not taken: the twentieth `INCOMPLETE_GENERATION` is placed on `ollama-glm-5.3/fcl/control/rep2` at 32,768, not swept into deepseek" (`family-F.md`).
* Genuinely new findings the Opus control missed, each **reproduced** by the judge: the non-string pin key in `a-04` ("`_pin_key`'s `str(entry)` at `custody.py:427` … `verify_pins({'pins': {7: '0'*64}})` returns `SOURCE_PIN_MISSING` on path `'7'` … a custody *finding*, indistinguishable in the receipt from a real missing file", `family-A.md`); the empty `reading_note` and the interface note's "24 keys" against `len(standard.FORBIDDEN_KEYS)` = 25 in `a-02` (`family-A.md`); and in `d-02` "The five `NEW_CODES` are not yet in `types.FAILURE_CODES`" — the judge's note: "Kimi found it, the control did not; I reproduced it, so it is a genuinely new finding on the worker's side" (`family-D.md`).

### 3.4 Honest reporting of "nothing wrong", and of evidence gaps

`battery/rubric.md` §4.1 calls this "the single most informative thing in the run".

* `f-02-commit-tree`: "every published pair verifies" — 8 commit+tree pairs, judge **reproduced** 8/8 by `judge-f/f02join.py`; "no MISMATCH_TREE, no COMMIT_NOT_IN_LOG, no AMBIGUOUS_SHORT_ID" **reproduced**. Judge's note: "The honest clean answer was given cleanly and the extraction set is itemised, including a pattern that hit zero — which is what lets a reader tell this from an incomplete check" (`family-F.md`).
* `e-01` claims 2 and 3: "**Verdict: SURVIVES.**" on both unrefutable claims, with the supporting aggregation **reproduced** by the judge; and the likeliest false positive declined in `e-03`: "**15.** staging 112 → FW5:210 — **CORRECT**" (`family-E.md`).
* Gaps named instead of filled: "this sandbox slice of F001 contains **no** delivered-bytes files at all (`*.txt sibling files anywhere under F001: 0`)" (`e-01`), and "`timeout` is not settled … Left unclassified rather than guessing" (`e-04`) — which **cost** it two rows against the answer key. Judge E: "I could not reproduce the key here and I do not hold it against the run: the elapsed time and the read-timeout error text exist only outside the sandbox … The task, not the worker, is under-determined" (`family-E.md`).
* `f-03`: "Failure codes: none present", stated plainly with the field list beside it; "no semantic gloss on the reasoning share, no family comparison" (`family-F.md`).
* House refusals held where they cost something: `a-04` declares "BLOCKER — none reproduced" rather than promoting a note, and names the credential scan's two-rendering bound "correctly reported as a documented bound and not a defect" (`family-A.md`); `d-03` and `d-04` carry the required phrasings rather than merely avoiding the forbidden ones — "a declared attention-and-spend boundary and never an exhaustion of the inquiry", "the single failure is NOT the clock and is not reported as one" (`family-D.md`).

### 3.5 Refusal to invent an oracle for a broken environment

`b-02-seats` shipped without the siblings its module imports. Kimi did not guess an oracle; it wrote
the reason into the file: "the wave-0 siblings `minireason.loop.types` / `minireason.loop.contracts`
are not copied here, so this oracle cannot run" (`test_seats.py:17-25`), and "the skip is the
unresolved outcome; the moment the siblings land, the same assertions run" (`:23-25`). Judge B
**reproduced** the exact `ModuleNotFoundError` and confirmed the diagnosis by importing the module,
then confirmed the task was unwinnable by running the project's own withheld suite in the same
sandbox: "`Ran 1 test / FAILED (errors=1)` on the same `ModuleNotFoundError`. **b-02 was not winnable
as delivered.**" (`judgements/family-B.md`).

### 3.6 Fast self-correction on tool errors

* `b-04` pass 2, iteration 12: it chained two commands with `;`, saw the refusal, and corrected in one
  turn — "No shell — each command runs alone. Let me run the probe separately" — then reissued the
  probe alone and it succeeded (`family-B.md`, read from the transcript).
* `b-01`: the first probe raised inside `surface.py:609` and it answered "My span arithmetic was off
  (len of the string, not a guess). Let me compute spans programmatically" — then did, producing the
  byte/code-point separation the judge **reproduced** (decoded index 91 against byte offset 101,
  `family-B.md`).
* `f-02`: "Four failing unittest runs worked through to a genuine regex bug (a lookahead written where
  a lookbehind was meant) and fixed" — judge **reproduced** by re-running: "script exit 0, 13 tests
  OK, `out/commit-tree.md` byte-identical" (`family-F.md`). `f-01` shows the same shape: "Two
  self-corrected script tracebacks (iterations 12, 20)".

### 3.7 Precise environment diagnosis

* `c-02`: ""`custody.py` isn't present." (pass 2 it9) — reproduced: c-02's `context_paths` lists no
  `custody.py`, and pass-1 it13's read returned `ERROR: NOT_A_FILE: src/minireason/loop/custody.py`"
  (`judgements/family-C.md`).
* `b-02`, above: the missing import named by module path, not by symptom.
* In production, the same behaviour on a live bundle: `p2-prereg-mechanical` ran the validator, got
  `ModuleNotFoundError: No module named 'minireason.loop'`, **re-ran it from inside the bundle
  directory to rule out a path-shaped cause**, got the identical traceback, then enumerated
  mechanically why it cannot run there (the sandbox's whole `src/` tree is one JSON file; four
  hard-coded published paths absent) and recorded **FAIL** with both verbatim outputs rather than a
  workaround (`prod-runs/p2-prereg-mechanical/sandbox/out/prereg-checks.md` §1). *Not yet checked by
  an independent judge* — see §6.

---

## 4. Weaknesses

### 4.1 Write-once-and-walk-away

The sharpest recurring failure, and it is what emptied family C. Judge C, family-level reading:
"**write-once-and-walk-away**: neither delivered file was ever parsed, imported or run by the worker
that wrote it, and `run_tests.py` — named in all four prompts as the thing to iterate against — was
never invoked in any pass of any task. Both delivered files are un-parseable, and one advertises it:
c-02 `roles.py:234-236`, a bare `"""` under `# (The module continues below; this header line is
closed by __doc__ surgery.)`" (`judgements/family-C.md`). The judge **reproduced** both failures:
`roles.py:295 SyntaxError: unterminated string literal`, and `decide.py:151` `Evalu ation,` — a token
split by a stray space — `SyntaxError: invalid syntax`. On `c-04` the judge establishes the cut was
the worker's own: "The `write_file` turn ended `finish_reason: "tool_calls"` at 2,037 completion
tokens, so the model closed the JSON itself: the truncated module is a worker decision, not a
transport cut." Consequence for the conformance gate: "Opus `test_roles.py` → Kimi `roles.py`:
**import error, every test**", and the Kimi→Opus direction has nothing to run, four times over.

### 4.2 Confident unchecked citation of symbols and lines it did not execute

* `c-02` `roles.py:134`: `from .types import UNRESOLVED_STEP  # noqa: F401 (table membership asserted
  by tests)` — "no such name; `UNRESOLVED_STEP` occurs in `types.py` only at line 371 as a string
  inside a tuple, so even with the syntax repaired this raises `ImportError`" (`family-C.md`,
  **reproduced**).
* `b-02` `test_seats.py:390`: `assertIn('importlib.import_module("tools.multicycle_commitment_study_multi_v2")', source)`
  — "that literal is absent from `seats.py`, which writes `importlib.import_module(_RUNNER_NAME)`.
  Reproduced: `grep -c` on material's `seats.py` returns 0"; and seven `Endpoint(...)` calls omitting
  the required `base_url` — "a constructor signature asserted without being run once"
  (`family-B.md`).
* `e-03` entry 7: "(the `\tag{EK}` is at :841 in the same display)" — "`\tag{EK}` is at FW5:836; line
  841 is the prose sentence" (`family-E.md`, **reproduced**).
* The pattern is specific: where it executed, it was right; where it asserted without executing, it
  was frequently wrong about the very bytes it names.

### 4.3 Generalising past its probes

`a-02` pass 2: "The one way `check` raises is the deliberate in-place schema mutation of F1" — judge A:
"false on these bytes and falsified by Kimi's own pass 1. A universal asserted where the probes
covered a sample. Not stale: a fresh over-generalisation." In the same review: "`.as_dict()`
round-trips through `check` for nominal, `none` and outside-vocabulary rows alike", offered as a
failed attack — "Kimi's own `probe_kimi2/p03_outside_vocabulary.py` prints an `.as_dict()` with no
`nominated_relation` in it — the control's S3 finding, in Kimi's own output, read past"
(`judgements/family-A.md`). Related, and worth watching: coverage is not monotone across passes —
"the run the harness called COMPLETE found the mutable-guard seam and lost the parse-path seam the
capped run had already found."

### 4.4 Prose transcription drift, and under-delivery against the source

* `e-03` entry 1 quotes FW5:172 "verbatim" as `The following conditions define \(\operatorname{Account}(\mathcal E).`
  — "the closing `\)` was dropped, so the quoted string is not a substring of the named line (tested:
  False)". Mitigating, and the diagnosis: "`check/verify_final.py` line 91 asserts the correct string
  with `\)`, so the check was right and the prose transcription slipped" (`family-E.md`).
* `d-04`: "'occurrence-02 had 5 reach it with read_fcl1 5 of 5 and the same three zeros'" — "The sheet
  states four zeros on each occurrence — parse_failure, schema_failure, unavailable_decode_failure
  AND opaque_envelope. The paragraph lists three" (`judgements/family-D.md`, **reproduced** at
  fact-sheet `:87-90`).
* `d-03` drops all fourteen obligation members, including p4's "no scoring key appears anywhere" and
  p6's "no reading is averaged or majority-voted" — "the house's own refusals written into P, and the
  paragraph loses them" (`family-D.md`). `d-04` drops four figure-groups, including the usage totals.
  Judge D's family reading: "The recurring weakness is **under-delivery against the source**" —
  3,307 characters against a 5,148-character control on `d-03`, 6,844 against a 10,635-character gold
  on `d-04`. Every drop was declared with a reason, which is the mitigating half; one of those reasons
  "describes wording the paragraph does not contain".
* Loose adherence to a literal instruction, same family: `d-02`'s prompt says "every code you name
  must be one you found in `steps.py`", and "roughly thirty of the codes it names live in
  `publish.py`, `receipts.py` and `types.py` instead — labelled honestly as pass-through, but named
  all the same" (`family-D.md`).

### 4.5 Errors concentrated in volunteered extras

Judge E, family-level reading: "**Volunteered extras carry the errors**: every incorrect claim I found
in the family sits in material nobody asked for — e-01's §2 recheck, correct that only "8 of the 20
cell coordinates carry `completion_tokens: 8192`", is wrong in its parenthetical "— not 5,488",
because the ninth receipt the report counts is the COMPLETE one and it carries exactly 5,488"
(`judgements/family-E.md`, **reproduced** over the cell: range 5,488–7,890, n=9). The same shape
appears in `f-02`: the one claim beyond what the text settles — "so the sentence's 'seven' is the
start commit plus those six" — is an unasked-for reading the Opus control deliberately left
unresolved (`family-F.md`; the judge reproduced the arithmetic but not the intent).

### 4.6 A blanket skip reported as OK

`b-02`'s prompt says that if a test fails because the module is wrong, leave it red and say so. Judge
B: "**Breach:** … the worker converted an environment failure into a blanket skip that reports OK,
and, cut off at the iteration cap, never said so anywhere but inside the file it wrote"
(`family-B.md`). The run reports `Ran 49 tests … OK (skipped=49)`, exit 0 — green, and vacuously so.
Under both judge mutations (a guard inverted at `seats.py:695`, a refusal weakened at `:601-603`) the
delivered suite "stays green": "The suite as delivered pins nothing anywhere."

### 4.7 Suspecting the environment before its own command form

`b-02` iteration 19 ran `python3 run_tests.py tests.loop.test_seats 2>&1 | tail -30`; there is no
shell, so "`2>&1`, `|`, `tail` and `-30` were passed to `run_tests.py` as four extra test names". Judge
B **reproduced** the exact argv: `Ran 53 tests … FAILED (errors=4, skipped=49)`, and concludes: "The
`exit_code: 1` the worker then saw came from its own command form, not its tests — and it spent
iterations 20-40, over half its budget, building `_scratch/` to chase it, never running the clean
command once" (`family-B.md`).

### 4.8 Shell-syntax habits against a `python3`-only tool layer

`e-01` used `python3 check/refute_claims.py > /tmp/c1.log 2>&1; echo "exit=$?"` and `e-04` used `&&`;
"the harness ran it anyway; the redirect had no effect" (`family-E.md`). `b-02` drew two refusals:
`ERROR: PATH_REFUSED: absolute path refused` and `ERROR: COMMAND_REFUSED: only python3 is allowed,
got 'PYTHONPATH_X=$(python3'` (`family-B.md`). Judge E: "the slip cost nothing here but would
elsewhere" — and in `b-02` it cost half the run. This is now an authoring rule (`PRODUCTION.md` rule 2).

### 4.9 Attacking functions singly, missing the composed seam

Judge A, on `a-04`, the one task where both sides answered: "The finding sets barely intersect: Kimi
attacked each function alone and found two real weaknesses in the pin key space and the write
ordering; the control attacked the pairs the docstrings tell callers to use (`fenced`+`write_new`,
digest-string+tree-statement) and found three. Kimi's probes reproduce to the character; its reach is
one seam short." The missed blocker, **reproduced** by the judge: "the documented pairing
`write_new(fenced(root, rel), value)` writes *through* an in-root symlink, so the record lands at
`cycles/0/decision.json` while the caller named `steps/0001-S0.json`". Family-level: "it tests
functions one at a time and rarely tests the *composition* the docstring recommends, which is where
all three a-04 blockers and the a-06 pathspec blocker live" (`judgements/family-A.md`).

### 4.10 Length: long where a key is short, short where a gold is long

Family E: "**It writes long**: 11k, 12k and 15k characters against keys of 3.5k, 5.8k and 2.6k, with
e-04 repeating "not recorded (no record in this copy carries one)" in two columns of fifteen rows and
closing with two sections that recite the house rules rather than just obey them" (`family-E.md`).
Family D is the mirror: `d-03` and `d-04` come in under their reference and drop source material
(§4.4), while `d-02` runs longer than the control and the judge finds the length earned — "the length
is spent on real coverage … not on padding" (`family-D.md`). Both directions are recorded; neither is
scored.

---

## 5. Infrastructure, kept separate from worker behaviour

Nothing in this section is evidence about the worker's judgement. All four judges say so explicitly
and separate it out.

**1. The 300 s gateway wall.** Ruling 13 records three Kimi calls ending "Remote end closed connection
without response" 300–301 s after their request began, the same signature as F002 occurrence-01's
300,270 ms close; ruling 14 confirms it as a host gateway wall — five closes in a 183 ms band across
two families, two client processes and different nodes. In pass 1 it ended twelve battery runs. It
also bounds generation: at ~90–100 tok/s the largest reachable generation is roughly 25–30k tokens
including reasoning, so a 32,768 ceiling is not reachable in time on these endpoints (ruling 13b).

**2. The 8,192 per-turn ceiling, and the sixteen mislabelled runs.** Passes 2 and 3 lowered
`max_tokens` to 8,192 per turn. Sixteen runs ended on a turn of **exactly** 8,192 completion tokens,
`finish_reason: "length"`, `content: ""`, `tool_calls: []`, with 27,777–36,797 characters of native
reasoning behind them and `files_written: []` (`RUNS-RECLASSIFIED.md`, with a per-run digest table).
The old harness ended its loop on any assistant turn with no tool call and called that `COMPLETE`.
Judge B: "`COMPLETE` here means "the model stopped", not "the task was done"." Judge E: "recording it
as COMPLETE is a harness labelling defect worth fixing before the family is read as a whole." The
reasoning text itself was never persisted; only its digest, character count and derived token count
survive, so what those turns concluded is unrecoverable. Note the trade this hid: "The runs are cheap
and fast *and* they deliver nothing."

**3. Context re-send cost.** The whole sandbox context is re-sent every turn, so an iteration cap is a
reading budget as much as a thinking budget. Figures the judges cite: `a-02` pass 1 sent **3,698,138**
prompt tokens for 52,581 completion tokens, pass 2 **5,199,979** for 29,243 (`family-A.md`); `c-04`
pass 2 **1,298,991** for 14,171 and `c-01` pass 2 **1,241,207** (`family-C.md`); `d-02` **772,986**
for 39,684 over 14 iterations and `e-04` **1,262,135** for 44,523 (`family-D.md`, `family-E.md`).
Judge D adds the correction that matters: "it is not the worker re-reading, and
`files_read_one_at_a_time_where_a_script_was_called_for` is false on all three completed tasks."

**4. HTTP 500s.** Four pass-2 runs died on provider `Internal Server Error` — `a-06`, `b-04`, `c-01`,
`d-01` — at 151–207 s, well inside the wall. `d-01` is the instructive case: it produced nothing in
pass 1 at the wall (313.151 s) and nothing in pass 2 for a different reason (`HTTP_500` at 151.714 s),
so, as judge D puts it, "the pass-2 retry does not confirm the pass-1 diagnosis" and "**d-01 yields no
evidence about the worker at all**".

**5. The two battery defects.**
* *`b-02`'s missing sibling imports.* `seats.py:102-103` imports `.contracts` and `.types`; neither is
  in the task's `context_paths`, nor is `tools/multicycle_commitment_study_multi_v2.py`. Judge B
  proved the task unwinnable by running the project's own withheld suite in the same sandbox and
  getting the identical `ModuleNotFoundError` (`family-B.md`). The one family-B task that produced an
  artifact is the one that could not have produced a green non-vacuous suite.
* *The gate-1 warnings-as-errors form.* `evaluation.json`'s family-C gate 1,
  `python3 -W error -c "…import minireason.loop.<m>"`, fails on an **untouched** sandbox: frozen
  `src/minireason/use_relation_h005.py:301` opens a docstring containing `"records"\s*:\s*[` in a
  non-raw string and `-W error` promotes the SyntaxWarning to SyntaxError. Judge C: "A judge who runs
  that form will read a material defect as a worker defect on both sides at once" (`family-C.md`), and
  used a two-stage import instead.

**6. Reference defects the judges found while judging** (recorded because they bear on how the battery
should be read, not on the worker): `evaluation.json[d-01-receipt]` states the gold at 4,901
characters where the paragraph measures 4,879 (`family-D.md`); the staleness note's row N2 calls
`custody.write_new`'s missing parent-directory fsync *live* when the frozen bytes call
`_fsync_directory(target.parent)` at `custody.py:400` — "Anyone scored against that row would be
scored against a stale row *in the staleness note*" (`family-A.md`); and two answer keys quote figures
that exist only outside the frozen corpus (F001 content bytes 288 / 7,080, and the two 180 s timeout
elapsed times), so on those points the worker "was judged against evidence it could not have had"
(`family-E.md`). The "ten controls" wording in `README.md` §4 / `rubric.md` §1 against fifteen actual
controls is the fourth (§2).

**7. Reasoning controls, and the transport port that landed after the battery closed.** Eight live
calls on one tiny prompt (`kimi/PROBE-REASONING.md`): on the `/v1/chat/completions` surface the
battery's harness spoke, `reasoning_effort: "low"`, `reasoning: {"effort": "low"}` and a pass-through
`think` are all accepted with HTTP 200 and all return reasoning **no shorter** than the uncontrolled
baseline (163, 142 and 160 characters against 135) — "Accepting a parameter is not honouring it; on
this surface these are inert." On Ollama's native `/api/chat`, `think: false` removed the reasoning
entirely (0 characters, 12 completion tokens, 3.8 s against the baseline's 166 characters, 63 tokens,
9.6 s) and `think: "low"` shortened it to 62. One sample each, treated as established for `false` and
suggestive for `"low"`. At battery time the conclusion was: **the control that works is not on the
surface the worker uses.**

That is no longer the state of the instrument. The open question — whether `/api/chat` serves the
same `tools` round trip — was answered with two calls (`probes/probe_native_tools.py`): turn 1 came
back HTTP 200 in 2.12 s carrying `message.tool_calls`, turn 2 used the tool result
(`answer_used_the_tool_result: True`, `done_reason: stop`). The translation is three shape
differences (the tool-call envelope, arguments as an object rather than a JSON string, `tool_name`
instead of `tool_call_id`), plus `options.num_predict` for the budget, `prompt_eval_count` /
`eval_count` for usage, `done_reason` for the finish reason — which leaves the `INCOMPLETE_TURN` rule
reading `length` unchanged — and `message.thinking` for reasoning. **The port was made**:
`TaskSpec.transport` defaults to `"native"`, with `"v1"` selectable per task and used as an automatic
one-time fallback if the native surface fails as a transport before any tool call. The first live
task on it, `prod-runs-smoke/smoke-native-001` at `think: "low"`: `status: COMPLETE`,
`transport_requested: "native"`, `transport_used: "native"`, `transport_fallbacks: 0`, 4 iterations,
3 tool calls, 11.301 s, both declared outputs written, `reasoning_chars: [28, 0, 0, 0]` — against
27,777–36,797 characters *per turn* on `/v1`, which is what had been eating the budget. Its
deliverable checks out independently: `out/sha.md` records
`e0bd1321e9a097651d9128f3e0c3503738bcedbdde05255af933ee05876fc40f`, 114 bytes, for `smoke/hello.py`,
and I recomputed both from the sandbox bytes and got the same digest and the same length. **The
caveat is the size of that evidence.** One smoke task, three tool calls, a sandbox of a few files.
The whole 47-run battery ran on `/v1`, so every `INCOMPLETE_TURN` in §2 and every ceiling-driven
absence in families A, B, C and `e-02` remains untested under the new transport: the port removes the
mechanism that caused those losses, it does not retroactively tell us what those runs would have
produced.

**8. What the harness now does about each.**
* *Relabelling.* `COMPLETE` survives only when the final turn finished **and** every declared
  `expected_output` exists; a budget-exhausted turn is `INCOMPLETE_TURN` /
  `TURN_BUDGET_EXHAUSTED_BY_REASONING`, a finished turn with nothing written is `NO_DELIVERABLE`
  (`RUNS-RECLASSIFIED.md`; `PRODUCTION.md` "Before you dispatch").
* *Budget.* Default `MAX_TOKENS` is now **24,576** — it fits the observed 28k–37k characters of
  reasoning with room for an answer and still lands inside the 300 s wall at ~90–100 tok/s. Not to be
  raised past ~25k: past that the wall closes the connection mid-generation and the whole turn is lost
  (`PROBE-REASONING.md`, `PRODUCTION.md` rule 6).
* *Reasoning control.* `TaskSpec.reasoning` (`"default" | "low" | "off"`, default `"low"`) is declared
  per task and reaches the wire **only** on an endpoint that honours it; on `/v1` it sends nothing, so
  the transcript never looks like a control was applied when it was not. A budget-exhausted turn is
  retried once at the lowest setting the endpoint honours — on `/v1` no retry fires.
* *Transport.* `TaskSpec.transport` now defaults to `"native"` (`/api/chat`, where `think` is
  honoured), with `"v1"` selectable per task and as the one-time automatic fallback, recorded as
  `transport_fallback`. `PRODUCTION.md` rule 7 is now "Leave `reasoning` at `"low"` and `transport`
  at `"native"`". This landed after the battery and after the five production audits in §6.
* *Task authoring.* `PRODUCTION.md`'s eight rules, each of which "cost a run": sibling imports in
  `context_paths` with an import check before dispatch; `verify_command` as one `python3` invocation
  with no shell syntax; `expected_outputs` as paths; name the output file and the `check/` script and
  say "do it by computation"; keep the context to the two or three files the task needs; budget the
  turn, not the task; set `reasoning` deliberately; caps of 30–40.

---

## 6. Routing recommendation under ruling 16

Ruling 16: Kimi K3 via `kimi_agent.py` for every mechanical or scripted task; Opus for semantic
argument over FW5, design decisions, independent judging of Kimi's own battery, and the one
publisher. The table below is that ruling made specific, with the family evidence for each row.

**The authoring conditions that made the left-hand column work** — all four present in every
production task that delivered: (a) **small context** — two to four `context_paths`, because the whole
context is re-sent each turn (`PRODUCTION.md` rule 5; family F, "the only family that survived pass 1
intact … a tool loop that writes one script and runs it produces short turns", `family-F.md`);
(b) **explicit output files** declared as sandbox-relative paths plus a `check/` directory, so
delivery is checkable and not inferred from a label; (c) **do it by computation** — the deliverable
generated by a script the worker writes, re-run before finishing (the byte-identical regeneration in
`e-04`, `f-01`, `f-02`, `f-03`); (d) **a single `python3` verify command** with no shell syntax
(`PRODUCTION.md` rule 2, bought by `b-02`'s lost twenty iterations). Per-turn budget 24,576, caps
30–40.

| Give to Kimi | Keep on Opus |
|---|---|
| **Aggregation over many records** — counts, profiles, usage ranges from receipts or JSONL. `f-01` every cell reproduced by the judge's own script; `f-03` a range reported with no mean; production `p1-ledger-audit` and `p2-activity-log-audit`, below. | ~~**Module implementation**~~ — **moved 2026-09-14 (§8)**: pass 4 delivered four compiling, self-tested modules from the same prompts and the same bytes, so the absence this cell rested on is gone. The class now reads *give to Kimi as a draft, Opus integrates and reviews* — new row below. |
| **Identity joins against a frozen extract** — commit/tree, digest-to-file. `f-02`: 8/8 pairs joined, "no MISMATCH_TREE, no COMMIT_NOT_IN_LOG, no AMBIGUOUS_SHORT_ID", plus 13 of its own unit tests (`family-F.md`). | ~~**Test writing / oracle design**~~ — **moved 2026-09-14 (§8)**: pass 4 delivered four suites, three green with zero skips and one deliberately red on a confirmed module defect. The class now reads *give to Kimi as a draft, Opus integrates and reviews* — new row below. |
| **Citation-at-line audits** — `e-03`: nineteen-and-one against the key, the decisive `FW5:133` empty line found, the likeliest false positive declined (`family-E.md`). *Condition:* take the quoted text from the checker's output, not from the prose (§4.4). | **Semantic argument over FW5** — ruling 16. No battery family tested it; `e-03` tested citation mechanics, and even there the model's prose drifted from its own verified strings. |
| **Classification against a derived set** — `e-04`: the planned 89 derived from the arms and node sequence, ceiling 7 / blocked 6 / ok 74 matching the project's own file, the under-determined rows left unclassified (`family-E.md`). | **Adversarial review of composed seams** — *count corrected 2026-09-14 (§8)*: reviews now exist on **6 of 6** family-A tasks, with executed probes and reproducing blockers, so the old "2 of 6" is wrong. The finding is unchanged and confirmed: `a-05` cleared the receipt-id seam and `a-06` the bracketed-pathspec seam that the control broke, each after attacking the component alone (`family-A.md`, `pass4.md` §2/§4). Keep the composed-seam verdict, and the "could not break" section, on Opus — and check every line citation (§8). |
| **Claim checks whose honest answer may be "nothing"** — `e-01` left both unrefutable claims standing while finding the real one; `f-02` reported a clean result cleanly with its extraction set itemised. *Strengthened 2026-09-14 (§8):* `e-02`, the last of the battery's four honest-negative tasks and the one that had never run, now reports "**No.** … nothing forbidden" with the live risks named and **no stale row** — it reads `_INT_PARAMS` as A where the reference's C rests on a since-repaired row; `a-03` does the same at blocker level ("BLOCKER — None reproduced"). *Condition:* the negative is trustworthy, the supporting prose is not — `e-02` overstates the panel-declaration claim (`types.py:665` refuses when judges are named) and writes "3 further ERRORs" for four (`pass4.md` §2/§4). | **Long-form transcription where every source figure must survive** — `d-04` "the same three zeros" for four; `d-03` dropped all fourteen obligation members including the house's own refusals (`family-D.md`). |
| **Mechanical consistency checks of a bundle** — production `p2-prereg-mechanical`: 12 check scripts, 32 files, a real digest mismatch found, a validator failure diagnosed from two working directories and reported FAIL. | **Publication** — git push, ledger appends with CRLF preservation, publish-and-verify. The tool layer refuses `git`, a shell and the network, and "no amount of prompting changes it" (`PRODUCTION.md`). |
| **Operator-facing documentation from one module** — `d-02`: every line citation verified, the pass-through code families and the ledger-refusal state the control missed, its own page checked by program for over-long blocks (`family-D.md`). | **Independent judging of Kimi's own output** — ruling 16: "a Kimi judge of Kimi is not independent". All six battery judges were Opus and each re-executed what it certified. |
| **Wave-2 module implementation, as a draft** — *added 2026-09-14 (§8)*. All four family-C modules import under warnings-as-errors and all four own-suites run green (26, 25, 22, 28 tests), a test class per acceptance clause, every declared `public_interface` name present, each roughly half the control's size; the worker ran its suite and edited against the failures instead of writing once and walking away (`pass4.md` §2/§3). | **Integrating that draft, and judging its interface** — gate 3 (each side's tests against the other's module) fails in both directions on all four tasks, at helper names outside the declared interface, so nothing yet says how close a Kimi module is to another implementer's; the integration and that judgement stay here (`pass4.md` §3). |
| **Unit-test suites, as a draft** — *added 2026-09-14 (§8)*. Four of four artifacts; three green with **zero skips** (23, 28, 18 tests); the fourth deliberately red on a real module defect the judge confirmed (`WAVE1-INTEGRATION-DECISIONS.md:5` requires a `lineage` derivation that `seats.py` does not contain), with two declared skips carrying a true reason (`pass4.md` §2). | **The mutation step on any Kimi suite** — seven of the eight judge-named mutations turn the suite red; the eighth, `b-02` M2 at `seats.py:601-603`, does not, and the clause it fails to pin — the `_judges` exhaustion fallback, unreached because `:575/:578` refuse first — was nameable only by applying the mutation. A suite's own green is not the check (`pass4.md` §2/§4). |

**The first production results, as evidence** (read from disk at ~15:06 UTC on 2026-09-14; two runs
were still in flight and are reported as such).

| run | status | wall | tool calls | deliverables | note |
|---|---|---|---|---|---|
| `p1-ledger-audit` | COMPLETE | 274.7 s | 30, 0 malformed | **13** files; `expected_outputs_missing: []` | 8 item scripts + an independent `check/verify_outputs.py` that "does not import `common.py`"; its own final line: "PASS: out/ledger-audit.json matches an independent recomputation; credential scans clean (counts only)" |
| `p2-activity-log-audit` | COMPLETE | 340.7 s | 18, 0 malformed | 4 files; none missing | 2,097 JSONL lines, all parsing; per-key record counts |
| `p2-prereg-mechanical` | COMPLETE | 413.3 s | 52, 0 malformed | 32 files; none missing | nine checks, each PASS / FAIL / NOT-CHECKABLE with evidence; found a `config.json` sha256 mismatch against VALIDATION.md §4 |
| `p1-ledger-verified-join` | ITERATION_CAP (30) | 590.7 s | 34, 0 malformed | all three declared outputs present; `final_text` empty | delivered but did not close; 3,420,290 prompt tokens for 26,563 completion — the re-send cost at full size |
| `p1-a001v3-citations` | in flight | — | — | `out/extracted.json`, `out/verdicts-raw.json`, `out/diagnostics.txt` present | first attempt `HARNESS_FAILURE / CONTEXT_PATH_MISSING`: "'staging/STAGING-v3.md' does not exist" — an authoring defect, caught by the harness before any call |

**All five of those runs used the old `/v1` transport** — they started before the port — so they say
nothing about it; four of them nonetheless delivered every declared output (three COMPLETE, one at
the iteration cap), which is evidence about small-context, script-shaped tasks, not about the new
surface. The one
native-transport datum is the smoke task in §5.7.

Four things in that table matter for routing. Three of five production tasks completed with every
declared output present and zero malformed tool calls, at 24,576 per turn with two to four context
paths — the shape §6's conditions describe. The one that hit the iteration cap **still delivered its
files**, which is why `PRODUCTION.md` says to read `files_written` and `expected_outputs_missing`
rather than the status word. The context-path failure was caught by the harness, not by the model, and
cost nothing. And **none of these five has been through an independent Opus verification yet**; ruling
11 requires one for anything that touches the record, so they are reported here as delivered work, not
as certified work.

---

## 7. What this battery cannot establish

**Sample size, per family, as occasions rather than trials.** A task is one occasion
(`battery/README.md` §5). After reclassification the judgeable occasions are: **A** two reviews
(`a-02`, `a-04`) out of six tasks, plus two probe trees with no verdict; **B** one artifact out of
four, and that one unwinnable as delivered; **C** two files out of four, both un-parseable, and no
test file at all; **D** three documents out of four; **E** three out of four — with `e-02`, the task
whose honest answer is "nothing forbidden is found", never tested; **F** three out of three. Nothing
here supports a statement about "Kimi in general", and several families support only a statement about
what the ceiling did to them.

**One model version, one host, one tool layer.** All runs are `kimi-k3` on the Ollama cloud endpoint
through `/v1/chat/completions`, inside a harness whose `run_command` admits `python3` only — no shell,
no `git`, no network. The 300 s wall and the reasoning-control behaviour are properties of that
deployment, not of the model; the probes show a different surface on the same host behaves differently
(`PROBE-REASONING.md`). Passes 2 and 3 confound the worker with an 8,192-token turn budget that
consumed itself, so those passes measure the harness far more than the model.

**The judges' own limits, as each stated them.** Judge A certifies fourteen control findings it
executed and names the rest as uncertified — "SF1–SF3 and N1–N5 I did not run and do not certify" —
and reports one row of the staleness note as itself stale. Judge B had no Opus control in its family
at all (`opus_control: false` on all four) and so judged against the prompts' acceptance lists and its
own two mutations. Judge C could not run gate 1 as `evaluation.json` words it and substituted a
two-stage import. Judge D found the gold's character count wrong in `evaluation.json` and used the
file. Judge E could not reproduce two of the key's rows because the evidence lies outside the frozen
corpus, and declined to score the worker down for them. Judge F re-derived every figure with scripts
it wrote fresh, and notes that `f-02` finished at iteration 29 of a 30 cap — "one more regex
correction and this run would have been an ITERATION_CAP with no final answer". Across every family,
the Opus controls kept **no transcript**, so `tool_calls`, `malformed_calls` and `refused_commands`
are null on every control verdict and the two sides' tool discipline cannot be set side by side.

**What a second battery would change.**
1. Re-run families A, B, C and `e-02` — the ones the ceiling emptied — on the native transport that
   has now landed, at 24,576 per turn with `think` set. This is the single change that would alter
   most of this report: at present the port rests on one smoke task, and every ceiling loss in the
   battery is untested under it.
2. Ship two or three files per task, not the directory that contains them; resolve every module's
   imports and prove the sandbox imports before dispatch (`b-02`).
3. Declare `expected_outputs` as paths on every task, including the prose ones, so delivery is
   checkable; keep the new `INCOMPLETE_TURN` / `NO_DELIVERABLE` labels.
4. Give every task a single `python3` verify command in the exact allow-list form, and require the
   deliverable to be generated by a `check/` script and re-run before finishing.
5. More than one occasion per task, so a finding can be distinguished from a run — `a-02` alone shows
   two passes finding different seams.
6. Record control transcripts, so tool discipline is comparable rather than one-sided.
7. Compute every answer key entirely inside the frozen corpus, and add at least one
   honest-answer-is-nothing task per family, since that is the behaviour the battery most wanted to
   observe and got only three chances to see.

---

## 8. Pass 4 on the native transport (2026-09-14)

Drawn from `kimi/judgements/pass4.md` only — one Opus judge, per-task verdict objects at
`judgements/scratch-pass4/<task>/verdict.json` with the figures beside them, all execution in copies,
no run sandbox executed in place. Pass 4 re-ran the fourteen tasks the 8,192-token ceiling had emptied,
on the native transport (§5.7). `b-02-seats` failed `CONTEXT_PATH_MISSING` by design and was judged
through `b-02-seats-fixed`; `c-03-markprep`'s first pass-4 run died as a transport error and its retry
is what is judged.

### 8.1 The fourteen tasks

Pass 1/2/3 are the **reclassified** labels of §2. "Artifact" = every declared `expected_output` exists.
"Verif." = the verification command the prompt named appears in the transcript's `run_command` calls.
Reasoning characters are the sum of `result.json.reasoning_chars` with the largest single turn in
brackets, against a 24,576-token budget.

| task | p1 | p2 | p3 | pass 4 | artifact | verif. | reasoning chars (max turn) |
|---|---|---|---|---|---|---|---|
| `a-01-types` | ITER_CAP | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 71,206 (23,066) |
| `a-03-standard` | ITER_CAP | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 47,417 (18,677) |
| `a-05-receipts` | HARNESS_FAIL | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 85,587 (30,633) |
| `a-06-publish` | HARNESS_FAIL | HARNESS_FAIL | INCOMPLETE_TURN | COMPLETE | yes | yes | 67,589 (27,070) |
| `b-01-surface` | HARNESS_FAIL | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 12,484 (5,464) |
| `b-02-seats-fixed` | (b-02 ITER_CAP) | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 14,731 (12,048) |
| `b-03-obligations` | HARNESS_FAIL | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 14,631 (6,702) |
| `b-04-steps` | HARNESS_FAIL | HARNESS_FAIL | INCOMPLETE_TURN | COMPLETE | yes | yes | 14,189 (4,201) |
| `c-01-packs` | HARNESS_FAIL | HARNESS_FAIL | INCOMPLETE_TURN | COMPLETE | yes | yes | 10,214 (6,499) |
| `c-02-roles` | HARNESS_FAIL | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 22,220 (19,503) |
| `c-03-markprep` (1st) | HARNESS_FAIL | INCOMPLETE_TURN | — | HARNESS_FAILURE | no | no | 16,776 (8,382) |
| `c-03-markprep` (retry) | " | " | — | COMPLETE | yes | yes | 56,539 (23,402) |
| `c-04-decide` | HARNESS_FAIL | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 48,699 (13,422) |
| `d-01-receipt` | HARNESS_FAIL | HARNESS_FAIL | INCOMPLETE_TURN | COMPLETE | yes | n/a — no `run_tests.py` in the sandbox; five own checkers run | 1,217 (619) |
| `e-02-metric-creep` | HARNESS_FAIL | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 20,204 (11,007) |

"Fourteen of fourteen tasks now have a run with every declared output present; before pass 4, none
did" — against §2's "latest genuinely COMPLETE pass: **none**" for all fourteen. Integrity holds
across all fifteen pass-4 sandboxes: no material file modified anywhere (sha256 walk against
`MANIFEST.sha256`), the only new paths being the declared outputs and the probe trees the prompts ask
for, and `malformed_tool_call_retries` 0 in every run.

### 8.2 What changed with the transport — infrastructure

* **No turn was length-capped.** Across all fifteen runs "there is **not one turn with
  `finish_reason: "length"`**, and the largest single turn anywhere is 13,567 completion tokens
  against a 24,576 budget" (judge's own `scratch-pass4/lengthturns.py` over every `transcript.jsonl`).
  Before, each of these fourteen ended on a turn of exactly 8,192 of 8,192 with 27,777–36,797
  reasoning characters behind it and nothing emitted. Peak per-turn reasoning fell on all fourteen —
  the largest is `a-05`'s 30,633 against its old 33,500, the smallest `d-01`'s 619 against its old
  32,229 — and `reasoning_retries` is 0 everywhere, because no turn needed one.
* **`transport_used: "native"`, `transport_fallbacks: 0` on all fifteen runs.** The `/v1` fallback
  never fired. This upgrades §5.7's `think: "low"` evidence from one smoke task to fourteen.
* **The 300 s gateway wall is not specific to the old surface.** `runs-pass4/c-03-markprep` ended
  `TRANSPORT_OR_RESPONSE_ERROR`, `harness_detail: "Remote end closed connection without response"` —
  the ruling-13 signature — at 419.4 s on the **native** transport with `transport_fallbacks: 0`; the
  fallback is armed only before the first tool call and that run had made fifteen. One occurrence in
  fifteen runs, the retry succeeded, and the largest successful single call in the set is 239,976 ms
  (`c-04-decide` it7), so "the headroom is real but not large". Ruling 13's wall stands as a host
  property, not a `/v1` property.

### 8.3 What changed in worker behaviour

* **Write-once-and-walk-away (§4.1) did not survive the budget change.** "In every pass-4 run that had
  a suite to run, the worker wrote, ran the verification command, read the failure and edited":
  `b-01-surface` ran its suite at it8, it10, it15 and it17 with edits between; `c-02-roles` five times
  over it14–it25, red to green, editing both module and tests; `c-04-decide` four times plus the whole
  suite at it22; `c-01-packs` three times. The judge calls this "the single largest behavioural
  difference in the set, and it is what the family-C and family-B results rest on".
* **Family C: all four modules now import under warnings-as-errors with green own-suites** — `Ran 26 …
  OK`, `Ran 25 … OK`, `Ran 22 … OK`, `Ran 28 … OK`, run by the judge in fresh copies through the
  two-stage import that works around the gate-1 battery defect (§5.5). "Against `family-C.md`'s '0 of
  4 tasks produced a compiling module, both delivered files un-parseable, `run_tests.py` never invoked
  in any pass', this is a different result on the same prompts and the same bytes." Gate 3 is still
  unreachable **in both directions on all four tasks**, and the judge attributes that to the gate: every
  cross-run fails at module import on helper names outside the declared `public_interface` (counts of
  imported names lying outside it: control 20/27, 29/34, 29/35, 12/17; Kimi 7/14, 6/11, 6/12, 8/13),
  while every declared interface name is present on the Kimi side in all four.
* **Family B: the suites became non-vacuous and do catch mutations.** Three of four green with **zero
  skips** (23, 28, 18 tests) against pass 1's single artifact in which all 49 tests skipped; the fourth
  (`b-02-seats-fixed`) deliberately red on a defect the judge confirmed —
  `WAVE1-INTEGRATION-DECISIONS.md:5` requires a `lineage` derivation stripping the `ollama-cloud/`
  prefix and `grep -n lineage src/minireason/loop/seats.py` returns nothing. **Seven of the eight
  mutations `family-B.md` named turn the suite red.** The one that does not is `b-02`'s M2 at
  `seats.py:601-603`, and the unpinned clause is nameable: "the `_judges` exhaustion fallback,
  unreached by the one-family fixture because `:575/:578` refuse first".
* **Family A: reviews now exist on six of six tasks**, with executed probes, and the blockers
  reproduce — `a-01` B1/S1, `a-03` SF1 (whose bottom line is the honest "BLOCKER — None reproduced"),
  `a-05` B1, `a-06` B1/B2, each re-run by the judge. §4.9 is **confirmed, not refuted**: "`a-05`
  cleared the receipt-id seam the control broke, and `a-06` cleared the pathspec seam the control
  broke, each after attacking the component in isolation".
* **Supporting prose still overstates, and line citations still drift.** `e-02`: "a config can declare
  a different panel … with no refusal anywhere" holds only when no judges are named (`types.py:665`
  refuses otherwise), "3 further ERRORs" is four, and two in-scope lens-1 rows are missed
  (`CALIBRATION_ANCHORS` at `standard.py:1136`, `FORBIDDEN_KEYS` at `standard.py:217`). `a-05`: the
  escaping error "carries no `__cause__`/`__context__`" is wrong, since implicit chaining sets
  `__context__`. On citations, §4.2 is now visible at scale: in `a-01` and `a-06` "every symbol named
  is correct and almost no line number is" (`a-06`: guard `:269-289` vs `:378`, `_read_back`
  `:432-442` vs `:720`, `verify_published` `:454-476` vs `:848`) while the control's citations for the
  same symbols are exact — and `a-03`'s are exact too, "which makes a-01's and a-06's drift a per-run
  property, not a model constant". §4.8's shell-syntax habit also survived (`sed` at `b-01` it3, a
  heredoc at `b-03` it10, `2>/dev/null` and a `for` loop at `a-06` it40–41) "but each cost one turn,
  not a run".
* **Two tasks worth naming individually.** `e-02` is the last of the battery's four honest-negative
  occasions and had never run: it now reports "**No.** … nothing forbidden" with the live risks as C
  rows and **no stale claim in any row**. `d-01`, which across three passes "yielded no evidence about
  the worker at all", delivers one paragraph on one line with the opening stamp byte-identical to the
  gold's, all 17 hex digests and every numeral traced to the fact sheet with zero misses, and all four
  AGENTS.md elements labelled — at 6,870 characters against the gold's 4,879 (and `evaluation.json`'s
  4,901 confirmed again as the known reference defect, §5.6).

### 8.4 What pass 4 does not establish

One run per task. `b-02-seats` is judged through a repaired variant of its own task file, so it is
evidence about the worker under a corrected battery rather than about the battery as it shipped.
`c-03-markprep`'s figures are a retry after a native-transport gateway close, so that task cost two
dispatches. The family-A comparisons re-execute each review's own claims and the control blockers that
bear on them — they are not a full re-judgement of every control finding, and `a-03` is judged against
its own claims only. Gate 3 is unrun on every family-C task. And the direction of the §5.7 caveat is
now this: the port removed the mechanism that caused these losses, and pass 4 says what these fourteen
tasks produce once it is removed — on one attempt each.
