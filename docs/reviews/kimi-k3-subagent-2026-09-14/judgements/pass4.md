# Pass 4 — the fourteen ceiling losses, re-run on the native Ollama transport

Judged 2026-09-14 from disk. All execution in copies under `judgements/scratch-pass4/<task>/`; no run
sandbox executed in place; `/home/user/miniReason` untouched; no API key read or printed. Method per
task is the method of that task's family judgement (`judgements/family-A.md`, `-B`, `-C`, `-D`, `-E`),
and their scratch scripts are reused where they exist: `scratch-C/wimport.py` (two-stage import),
`scratch-C/integrity.py` (sha256 walk), `scratch-C/iface.py`, `scratch-C/fields.py`.

`b-02-seats` under `runs-pass4` failed `CONTEXT_PATH_MISSING` by design, so `b-02-seats-fixed` is
judged in its place. `c-03-markprep` under `runs-pass4` failed as a transport error; the retry under
`runs-pass4-retry` finished at 15:57 UTC while this judgement was in progress and **is** judged.
`c-04-decide` had finished before judging began. No task is recorded as unfinished.

Every figure below carries the command or file that produced it. No scores, no ranks, no percentages.

---

## 1. Status table

Pass 1/2/3 status is the **reclassified** label from `RUNS-RECLASSIFIED.md`, not the recorded one.
"Artifact" means every declared `expected_output` exists. "Verif. run" means the verification command
the prompt named was found in the transcript's `run_command` calls. "Reasoning chars" is the sum of
`result.json.reasoning_chars`; "max turn" its largest single element, against a 24,576-token budget.

| task | p1 | p2 | p3 | pass 4 | artifact | verif. run | reasoning chars (max turn) | wall s |
|---|---|---|---|---|---|---|---|---|
| a-01-types | ITERATION_CAP | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 71,206 (23,066) | 760.0 |
| a-03-standard | ITERATION_CAP | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 47,417 (18,677) | 676.5 |
| a-05-receipts | HARNESS_FAILURE | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 85,587 (30,633) | 872.1 |
| a-06-publish | HARNESS_FAILURE | HARNESS_FAILURE | INCOMPLETE_TURN | COMPLETE | yes | yes | 67,589 (27,070) | 1112.1 |
| b-01-surface | HARNESS_FAILURE | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 12,484 (5,464) | 354.6 |
| b-02-seats-fixed | (b-02 ITERATION_CAP) | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 14,731 (12,048) | 366.2 |
| b-03-obligations | HARNESS_FAILURE | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 14,631 (6,702) | 406.2 |
| b-04-steps | HARNESS_FAILURE | HARNESS_FAILURE | INCOMPLETE_TURN | COMPLETE | yes | yes | 14,189 (4,201) | 598.4 |
| c-01-packs | HARNESS_FAILURE | HARNESS_FAILURE | INCOMPLETE_TURN | COMPLETE | yes | yes | 10,214 (6,499) | 607.1 |
| c-02-roles | HARNESS_FAILURE | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 22,220 (19,503) | 719.2 |
| c-03-markprep (1st) | HARNESS_FAILURE | INCOMPLETE_TURN | — | HARNESS_FAILURE | no | no | 16,776 (8,382) | 419.4 |
| c-03-markprep (retry) | " | " | — | COMPLETE | yes | yes | 56,539 (23,402) | 747.7 |
| c-04-decide | HARNESS_FAILURE | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 48,699 (13,422) | 986.9 |
| d-01-receipt | HARNESS_FAILURE | HARNESS_FAILURE | INCOMPLETE_TURN | COMPLETE | yes | n/a (no `run_tests.py` in sandbox; five own checkers run) | 1,217 (619) | 117.2 |
| e-02-metric-creep | HARNESS_FAILURE | INCOMPLETE_TURN | — | COMPLETE | yes | yes | 20,204 (11,007) | 244.7 |

Fourteen of fourteen tasks now have a run with every declared output present; before pass 4, none did
(`RUNS-RECLASSIFIED.md` final section: "latest genuinely COMPLETE pass: none" for all fourteen).

**Integrity, all fifteen pass-4 sandboxes** (`judgements/scratch-C/integrity.py` walking each `src/`
and sha256-comparing against `battery/MANIFEST.sha256`): **no material file modified anywhere**. The
only new paths are the declared outputs plus the probe trees the family-A and e-02 prompts ask for.
`malformed_tool_call_retries` is 0 in every run.

---

## 2. Per-task verdicts

The full verdict object in the rubric's shape is at
`judgements/scratch-pass4/<task>/verdict.json`, with the figures behind it in `figures.md` beside it.
What each one settles, in one or two sentences:

**a-01-types.** First family-A review this battery has produced for this task. B1 (`CustodyReport.from_mapping`
and `from_findings` shred the bare string `'SOURCE_PIN_MISSING'` into 18 one-character checks while the
constructor refuses it) and S1 (`_utc` is a shape check, not a timestamp check: `'2026-13-40T25:61:61Z'`
accepted) both reproduce under my own `python3 -c`. Its failed-attack section is real — eight of nine
probes re-run at exit 0 and every quoted block reproduces byte-for-byte. Against that: **not one of the
line numbers in B1, S1, S2 or N3 is where the symbol is** (`from_mapping` body cited `:1018`, a blank
line, actual `:980`; `reading_dir` cited `:1191-1201`, actual `:1323`; `SeatsConfig` cited `:678-698`,
which is `ContrastConfig`, actual `:606`). Misses the control's plan-identity blocker.

**a-03-standard.** The honest-negative case and it holds: "BLOCKER — None reproduced", with the seams
it attacked named. SF1 reproduces (`probe/guard_params.py` exits 1 on `TypeError: 'int' object is not
iterable` raised at `standard.py:1262` through `build_standard` at `:1294` — an undeclared escape).
**Every cited line I checked is exact** (`standard.py:217`, `:1008`, `:1242/1260`, `:1347`;
`types.py:606`), which makes a-01's and a-06's drift a per-run property, not a model constant.

**a-05-receipts.** B1 reproduces: with a flaky outcome logger the caller receives
`ReceiptError ACTIVITY_LOGGER_FAILED`, not its own `OriginalError`. One sentence inside it is wrong and
I pinned it — the review says the escaping error "carries no `__cause__`/`__context__`", but Python's
implicit chaining sets `__context__` to `OriginalError('the real failure')`. The costly item is a
**miss**: the control's B1 (`open_receipt(render=…)` hands two callers `REC-20260914-A`) is on the seam
Kimi attacked and cleared, because it minted through the default renderer only. I re-ran the control's
probe and it reproduces.

**a-06-publish.** Seventeen executed probes against a module that needs real `git`, and both blockers
reproduce. B1 is half-shared with the control (`git add -A`/`--all`/`-u`/`.` pass the guard) and half
new (`push origin :refs/heads/x`, a deletion refspec, passes while `push -d` is refused). B2 reproduces
with the push already landed. Two defects: **every** cited line is wrong while every symbol is right
(`_read_back` cited `:432-442`, actual `:720`; the guard cited `:269-289`, actual `:378`; the control's
citations for the same symbols are exact), and its "glob magic … refused" generalises from `*` to all
globs — the control publishes an unnamed neighbour through `report[1].md`, which I reproduced.

**b-01-surface.** `Ran 23 tests … OK`, exit 0, **zero skips**; six of six verbatim acceptance clauses,
one test class each. Both named mutations caught: M1 (`surface.py:750`, `len(starts) != 1` → `== 1`)
→ `FAILED (failures=3, errors=7)`; M2 (`surface.py:783-784`, `SIDE_FRAMING` `return False` → `True`)
→ `FAILED (failures=1)`.

**b-02-seats-fixed.** `Ran 28 … FAILED (failures=1, skipped=2)` — red **by design**, and the rubric's
gate-1 exemption applies: the red names a real module defect I confirmed. `notes/WAVE1-INTEGRATION-DECISIONS.md:5`
requires a `lineage` derivation stripping the `ollama-cloud/` prefix; `grep -n lineage
src/minireason/loop/seats.py` returns nothing, and the default judge pair is
`('deepseek', 'ollama-cloud/deepseek')`. The two skips carry a true stated reason (the runner file is
absent by design). M1 (`seats.py:695`) caught, 14 errors. **M2 (`seats.py:601-603`) not caught** — the
suite stays at exactly the baseline failure, because the one-family fixture is refused earlier at
`:575/:578`, so nothing pins the `_judges` exhaustion fallback. Its own citations of `_judges` (~460,
actual 566) and `require_cross_family_judges` (~570, actual 681) are each about 100 lines low.

**b-03-obligations.** `Ran 28 … OK`, zero skips. M1 (`obligations.py:1734`) caught, one failure;
M2 (`obligations.py:1841`, `return losses` → `return losses or None`) caught, three failures. One
refused command at it10 — a heredoc against the `python3`-only tool layer — re-expressed in the next turn.

**b-04-steps.** `Ran 18 … OK`, zero skips, eleven classes named after the acceptance clauses. M1
(`steps.py:911`) caught, four failures; M2 (`steps.py:934-938`, the sticky-halt `ResumeAction` replaced
with `pass`) caught, one failure. Three earlier passes produced no file at all.

**c-01-packs.** Imports under warnings-as-errors; `Ran 26 tests … OK`. All seven declared
`public_interface` names present with the declared arity; `NEW_CODES` declared. Module 28,941 bytes
against the control's 62,488. Three earlier passes produced nothing.

**c-02-roles.** Imports; `Ran 25 tests … OK`. Holds the two declared `RoleResult.raw_ref` /
`.prompt_ref` field names **that the control renames** to `request_path`/`response_path`/… — a point
where the worker held to the declared interface and the reference did not. In pass 1 this task
delivered a `roles.py` that would not parse.

**c-03-markprep.** Judged on the retry. Imports; `Ran 22 tests … OK`; all six declared names present;
a class per acceptance clause including the ordering clause (`BaselineSealedBeforeResidue`). Declares
`NEW_CODES = ('CELL_MALFORMED',)` where the control declares three, so its seal-after-edit refusal is
raised under a code it did not add to its own list. Two earlier passes read four files, made **zero**
`run_command` calls and stopped.

**c-04-decide.** Imports; `Ran 28 tests … OK`. The two house constraints this task exists to test hold
*inside the code*: the boundary sentence is present at `decide.py:261` and routed through
`standard.assert_no_exhaustion_claim`, and no clause counts readings, marks, endpoints or differs — the
only `len()` in a clause body is the calibration-anchor margin at `:745-750`, which is
`design/design-s5-decision-rule.md:42`'s pre-registered `JUDGE_ERR_MAX` rule rendered beside its own
account. In pass 2 this task delivered a `decide.py` whose bytes were corrupt at line 151.

**d-01-receipt.** The task that yielded no evidence about the worker at all across three passes, for
three different infrastructure reasons. It now delivers one paragraph, one line, opening stamp
byte-identical to the gold's; all 17 hex digests and every 2-6 digit numeral trace to the fact sheet
with zero misses; all four AGENTS.md elements labelled (`Choice`, `Reason`, `Contribution`, `State:
PENDING`) plus a `Publication evidence:` clause; three suites each beside its own invocation; and the
house refusals held in one explicit denial sentence. 6,870 characters against the gold paragraph's
**4,879** (`evaluation.json` states 4,901 — the known reference defect, confirmed again here).

**e-02-metric-creep.** The fourth of the battery's four honest-negative tasks, produced for the first
time. Bottom line "**No.** … nothing forbidden" matches `evaluation.json`'s expected bottom line, with
the live risks named as the C rows. **No stale claim in any row** — and row 2 reads `_INT_PARAMS`
`judge_seats (2,8)` as A where lens-1 row 4 says C-see-S7, which is the correct reading of the frozen
bytes because S7 is repaired. Two overstatements I pinned: "a config can declare a different panel …
with no refusal anywhere" holds only when no judges are named (`types.py:665` refuses otherwise), and
"3 further ERRORs" is four. Misses two in-scope lens-1 rows entirely: `CALIBRATION_ANCHORS`
(`standard.py:1136`) and `FORBIDDEN_KEYS` (`standard.py:217`).

---

## 3. What changed with the transport

### Infrastructure

**The mechanism §5.2 describes is gone from these runs.** Across all fifteen pass-4 runs there is
**not one turn with `finish_reason: "length"`**, and the largest single turn anywhere is 13,567
completion tokens against a 24,576 budget, so well under half of it
(`judgements/scratch-pass4/lengthturns.py` over every `transcript.jsonl`). Before, each of these
fourteen tasks ended on a turn of exactly 8,192 completion tokens against an 8,192 ceiling with
27,777–36,797 reasoning characters behind it and nothing emitted (`RUNS-RECLASSIFIED.md`). Peak
per-turn reasoning fell on all fourteen: the largest is a-05's 30,633 characters against its old
33,500, and the smallest is d-01's 619 against its old 32,229.

**`transport_used: "native"`, `transport_fallbacks: 0` on all fifteen runs.** The `/v1` fallback never
fired. `malformed_tool_call_retries` is 0 everywhere, as on `/v1`.

**The 300 s gateway wall is not a `/v1` phenomenon.** `runs-pass4/c-03-markprep` ended
`TRANSPORT_OR_RESPONSE_ERROR`, `harness_detail: "Remote end closed connection without response"` — the
ruling-13 signature — at 419.4 s wall on the **native** surface, with `transport_fallbacks: 0`. The
automatic fallback did not fire because it is armed only before the first tool call and that run had
made 15. One occurrence in fifteen runs, and the retry succeeded; the largest successful single call
in the set is 239,976 ms (`c-04-decide` it7), so the headroom is real but not large.

**`reasoning: "low"` reached the wire and did something.** `PROBE-REASONING.md` had this as one sample
and "suggestive". Fourteen tasks that previously spent 27,777–36,797 characters on a single turn now
peak between 619 and 30,633, and `reasoning_retries` is 0 in every run — no budget-exhausted turn
needed retrying, because there were none.

### Worker behaviour

**The write-once-and-walk-away pattern did not survive the budget change** (§4.1). In every pass-4 run
that had a suite to run, the worker wrote, ran the verification command, read the failure and edited:
`b-01-surface` ran `run_tests.py tests.loop.test_surface` at it8, it10, it15 and it17 with edits
between; `c-02-roles` ran its suite five times over it14–it25, red to green, editing both its own
module and its own tests; `c-04-decide` four times plus the whole suite at it22; `c-01-packs` three
times. This is the single largest behavioural difference in the set, and it is what the family-C and
family-B results rest on.

**The family-C modules now compile and run their tests — all four.** Gate 1 (`scratch-C/wimport.py`,
the two-stage import that works around the `-W error` battery defect) passes on `packs`, `roles`,
`markprep` and `decide`. Gate 2 passes on all four: `Ran 26 … OK`, `Ran 25 … OK`, `Ran 22 … OK`,
`Ran 28 … OK`. Against `family-C.md`'s "0 of 4 tasks produced a compiling module, both delivered files
un-parseable, `run_tests.py` never invoked in any pass", this is a different result on the same prompts
and the same bytes.

**Gate 3 remains unreachable in both directions on all four tasks — and that is a property of the
gate, not of one side.** Every cross-run fails at module import on a helper name outside the declared
`public_interface`: the control's tests on `CELL_KEYS` / `ABSENT` / `ARM_FCL` /
`BOUNDARY_NOT_EXHAUSTION`, Kimi's on `PRECEDENT_QUERY` / `RolesRefused` /
`BARE_TOKEN_TOKENS_DEFAULT` / `BOUNDARY_SENTENCE` (`judgements/scratch-pass4/ximports.py` counts, per
test file, how many imported module names lie outside the declared interface: control 20/27, 29/34,
29/35, 12/17; Kimi 7/14, 6/11, 6/12, 8/13). Every declared interface name is present on the Kimi side
in all four tasks.

**The family-B suites became non-vacuous and do catch mutations.** Three of four are green with
**zero** skips (23, 28, 18 tests); the fourth is deliberately red on one test naming a real module
defect, with two declared skips carrying a true reason — against pass 1's one artifact, a 49-test suite
in which all 49 skipped. Of the eight mutations `family-B.md` named, **seven turn the suite red**. The
one that does not is `b-02`'s M2 (`seats.py:601-603`), and the unpinned clause is nameable: the
`_judges` exhaustion fallback, unreached by the one-family fixture because `:575/:578` refuse first.

**Two weaknesses did not move.** §4.2's confident unchecked citation is now visible at scale because
the reviews exist: in `a-01` and `a-06` every symbol named is correct and almost no line number is
(`a-06`: guard `:269-289` vs `:378`, `_read_back` `:432-442` vs `:720`, `verify_published` `:454-476`
vs `:848`), while the Opus control's citations for the same symbols are exact, and `a-03`'s are exact
too. And §4.9's composed seam: `a-06` attacked `_explicit_paths` with `*.txt`, cleared "glob magic",
and missed the bracketed pathspec the control publishes an unnamed file through. §4.8's shell-syntax
habit also survived — `sed` at `b-01` it3, a heredoc at `b-03` it10, `2>/dev/null` and a `for` loop at
`a-06` it40–41 — but each cost one turn, not a run.

---

## 4. Routing table rows to change

Three rows in §6's right-hand column were justified by absences that pass 4 has now filled. The
left-hand column's authoring conditions are unchanged and every pass-4 task met them.

**Row: "Module implementation — family C: 0 of 4 tasks produced a compiling module".** *Change.* The
sentence is no longer true of the instrument. All four modules import under warnings-as-errors and all
four own-test suites are green (26, 25, 22, 28 tests), with a test class per acceptance clause and the
declared `public_interface` present in all four. *Evidence:* `scratch-C/wimport.py` plus
`python3 run_tests.py tests.loop.test_<m>` in fresh copies; `scratch-pass4/iface.py`. *What the row
should say instead:* Kimi can now deliver a compiling, self-tested wave-2 module from a design entry;
what pass 4 does **not** establish is conformance to another implementer's interface, because gate 3
fails in both directions on every task for reasons that are the gate's, not the worker's. Each module
is roughly half the control's size.

**Row: "Test writing / oracle design — family B: 1 artifact of 4, and it is vacuous".** *Change.* Four
of four artifacts; three green with zero skips; seven of the eight judge-named mutations caught; and
the fourth suite is deliberately red on a defect I confirmed against `WAVE1-INTEGRATION-DECISIONS.md:5`
and the frozen `seats.py`. *Evidence:* the eight mutation runs in
`judgements/scratch-pass4/b-0*/b0*-M[12]/`, each a fresh copy, recorded in §2 above. *Condition to keep
on the row:* one mutation went uncaught, and the clause it failed to pin is a fallback path a fixture
never reaches — so a suite that is green under mutation still needs the judge's mutation step, not the
suite's own green.

**Row: "Claim checks whose honest answer may be 'nothing'" (left column).** *Strengthen.* `e-02` was
the one of the battery's four honest-negative tasks that had never run; it now reports "nothing
forbidden", names the live risks, and passes the staleness test — including reading `_INT_PARAMS` as A
where the reference's C rested on a row since repaired. `a-03` does the same at the family-A blocker
level ("None reproduced"). *Evidence:* `out/metric-creep.md` against the lens-1 table read through
`reference/A-CODE-staleness-note.md`; `review/standard.md:17-22`. *Add the condition:* both overstate
somewhere — `e-02` on the panel-declaration claim and an error count off by one — so the negative is
trustworthy and the supporting prose still needs checking.

**Row: "Adversarial review of composed seams — family A: reviews on 2 of 6 tasks, and its misses are
precisely the compositions".** *Do not change the finding; change the count.* Reviews now exist on
6 of 6 (the four here plus `a-02`, `a-04`), and the blockers in `a-05` and `a-06` reproduce. But the
second half of the row is confirmed rather than refuted: `a-05` cleared the receipt-id seam the control
broke, and `a-06` cleared the pathspec seam the control broke, each after attacking the component in
isolation. *Evidence:* I re-ran both control probes and both reproduce. *What the row should say:* Kimi
now delivers adversarial reviews with executed probes; the composed seam is still where its
"could not break" section is wrong, and its line citations should not be relied on without checking.

**Rows that pass 4 leaves alone.** Publication, semantic argument over FW5, long-form transcription,
and independent judging of Kimi's own output are untouched by these fourteen tasks — nothing here tests
them. `d-01`'s success moves nothing on the transcription row, because `d-01` is a one-paragraph
receipt from a fact sheet, not the fourteen-member `d-03` list or the `d-04` gold.

---

## 5. What this pass does not establish

One run per task. `b-02-seats` is judged through a repaired variant of its own task file, so it is
evidence about the worker under a corrected battery, not about the battery as it shipped.
`c-03-markprep`'s figure is a retry after a native-transport gateway close, so the task cost two
dispatches. The family-A comparisons here re-execute each review's own claims and the control blockers
that bear on them; they are not a full re-judgement of every control finding, and `a-03` in particular
is judged against its own claims only. Gate 3 is unrun on every family-C task, so nothing in this pass
says how close either implementation is to the other's interface. And the §5 caveat's own words still
apply in one direction: the port removed the mechanism that caused these losses, and pass 4 now says
what these runs produce once it is removed — for these fourteen tasks, on one attempt each.
