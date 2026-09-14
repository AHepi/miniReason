# Family C — IMPLEMENTATION (c-01-packs, c-02-roles, c-03-markprep, c-04-decide)

Judged 2026-09-14 from disk. Read first: `battery/README.md` §3C, `battery/rubric.md` §2/§3C,
`battery/evaluation.json`, the four prompts in `battery/tasks.json`, `controls/README.md` §4,
`kimi/RUNS-RECLASSIFIED.md`. All execution in copies under `judgements/scratch-C/`; no sandbox run in place;
`/home/user/miniReason` untouched.

## 0. What each side delivered

`RUNS-RECLASSIFIED.md` records **no genuinely COMPLETE pass for any of the four tasks**. I re-read the four
`result.json`/`transcript.jsonl` pairs and reproduce that: every pass-2/3 run labelled COMPLETE ends `finish_reason:
"length"`, `completion_tokens: 8192`, `content: ""`, `tool_calls: []`. c-01 pass 3 finished 11:53:46 (iteration 11,
same shape) and is not running.

| task | Kimi module | Kimi tests | Kimi final msg | Opus module | Opus tests |
|---|---|---|---|---|---|
| c-01-packs | **none** (3 passes) | none | none | `packs.py` 1456 L | `test_packs.py` 830 L |
| c-02-roles | `roles.py` 37,647 B (p1) | none | none | `roles.py` 1199 L | `test_roles.py` 719 L |
| c-03-markprep | **none** (2 passes) | none | none | `markprep.py` 1217 L | `test_markprep.py` 741 L |
| c-04-decide | `decide.py` 8,166 B (p2) | none | none | `decide.py` 1213 L | `test_decide.py` 1044 L |

Figures from `wc -l -c` and each run's `result.json.files_written[].bytes`.

**Integrity.** `judgements/scratch-C/integrity.py` against `battery/MANIFEST.sha256`: no material file modified on
either side, `types.py` included; new files are only those tabled. One empty `controls/c-04-decide/sandbox/.tmp` on
the Opus side.

**No battery defect here.** Each task's declared `depends_on` imports cleanly in its own worker sandbox — packs:
contracts/standard/surface/types; roles: contracts/types/seats; markprep: contracts/standard/custody/types; decide:
types/obligations/graph; plus `provider_openai_compat` in all four. An absent or red result is a worker result.

**Gate 1 cannot be run as worded.** `python3 -W error -c "…import minireason.loop.<m>"` fails on an *untouched*
sandbox: frozen `src/minireason/use_relation_h005.py:301` opens a docstring containing `"records"\s*:\s*[` in a
non-raw string and `-W error` promotes that SyntaxWarning to SyntaxError. I used `judgements/scratch-C/wimport.py`,
which imports the material closure with warnings ignored, then sets `warnings.simplefilter("error")` before importing
the module under judgement. "IMPORT OK (warnings=error for the new module)" below means that form.

---

## 1. c-01-packs

**Kimi.** *correct_claims:* the run's single executed probe (pass 2 it16) — `banner len 1251`, `registers ('T', 'E',
'D', 'G')`, `marks ('differs', 'same', 'unresolved')`, `std:reading-rubric/v1 reading-v1`; I reproduce all four.
*incorrect_claims:* none — none made. *missed:* the whole task; no `packs.py`, no `test_packs.py`, and none of
`render_row`, `render_exchange`, `render_register`, `render_paraphrase_request`, `precedent_slice`, `pack_sha`,
`BaselineNotFirst`; no acceptance mapping, stub list or unsettled-question list. *fabricated:* none. *house_rules:* no
breach observable; the only prose is narration ("One more check — the `Status` enum values, then I'll write the
module."). *verbosity:* 0 chars against the reference's 26,941 (`wc -c controls/c-01-packs/FINAL.md`) —
under-delivery. *tool_use:* pass 3, 26 calls (read_file 23, list_dir 2, grep 1), 0 malformed, 0 refused, **0
run_command**; pass 2, 33 calls with one. `python3 run_tests.py tests.loop.test_packs` never run in any pass. Nothing
edited. *overall:* three passes of competent orientation and no artifact; evidence about reading under a turn ceiling,
nothing about implementation.

**Opus.** *correct_claims:* (a) the banner is held by identity, not a copy — `standard.READING_BANNER is
USE_RELATION_BANNER` → `True`, and "A lexical overlap is not evidence of use" does not occur in `packs.py` (grep, 0
hits); (b) "`render_register` checks the seal **first** … `None` and `""` raise; so does a non-string, an uppercase
hex string, a 63- or 65-character string, an integer, a bytes object and `True`" — I called
`render_register(object(),'T',('a','b'),bad,object())` for `None, '', 'a'*63, 123, True`; all five raise
`BaselineNotFirst` / `BASELINE_NOT_FIRST`; (c) `python3 run_tests.py tests.loop.test_packs` → `Ran 61 tests in 0.211s
/ OK`. *incorrect_claims:* "`packs.py` (1457 lines)" and "`test_packs.py` (831 lines)"; `wc -l` gives 1456 and 830 — a
counting convention off by one, but the figures do not reproduce. *missed:* nothing; no answer key exists.
*fabricated:* none; `NEW_CODES` is a 13-tuple with no member already in `types.FAILURE_CODES`, and
`BASELINE_NOT_FIRST` is correctly absent from it because the table already carries it. *house_rules:* no score, rank
or meter; `unresolved` first-class across ten named open decisions D1-D10, each with "what would change if the
decision went the other way"; counts sit beside their command. *verbosity:* 26,941 chars, the longest of the four;
D5/D6 restate one ordering rule twice. *tool_use:* controls keep no transcript, so call and malformed-call figures are
**null**; verification command demonstrably run and reproduced; no `src/` edit. *overall:* a finished module whose
tests pin acceptance by identity rather than by restated strings; its D4 convention (`provenance.school ==
"appellate"`) is invented and declared as such, and needs W1-GRAPH's agreement.

**Comparison and cross-run.** Only one side produced a module, so nothing about packs can be compared; what the
pairing shows is that the same prompt and bytes yielded a deliverable on one side and three passes of reading on the
other. Opus `test_packs.py` → Kimi module: **not runnable, no Kimi module**. Kimi tests → Opus module: **not runnable,
no Kimi test file**. Both directions are empty because the Kimi side is empty, not because interfaces differ.

---

## 2. c-02-roles

**Kimi.** *correct_claims:* "`custody.py` isn't present." (pass 2 it9) — reproduced: c-02's `context_paths` lists no
`custody.py`, and pass-1 it13's read returned `ERROR: NOT_A_FILE: src/minireason/loop/custody.py`. Also correct by
static check: `ROLES: tuple[str, ...] = contracts.ROLE_NAMES` imports the role vocabulary from its owner, and
`Endpoint`, `ProviderFailure`, `slots_for`, `write_new`, `OfflineProvider`, `seats.Seat`, `seats.key_cap_for`,
`contracts.ROLE_NAMES`, `contracts.UNRESOLVED` all exist as spelled. *incorrect_claims:* the module docstring's
"``NO_REPLAY``, ``INDETERMINATE`` and ``CONFIG_INVALID_VALUE`` are already in the table and are raised, **imported,
never retyped**" — contradicted sixty lines later by `roles.py:170`, `NO_REPLAY = "NO_REPLAY"`. (The three codes are
in `types.FAILURE_CODES`; that half holds.) *missed:* `tests/loop/test_roles.py` entirely; the acceptance mapping; the
stub list; the unsettled questions; the statement of which table each new code belongs in. *fabricated:*
`roles.py:134`, `from .types import UNRESOLVED_STEP # noqa: F401 (table membership asserted by tests)` — no such name;
`UNRESOLVED_STEP` occurs in `types.py` only at line 371 as a string inside a tuple, so even with the syntax repaired
this raises `ImportError`. Also `NEW_CODES: Mapping[str, str] = MappingProxyType({…})` where the prompt says
`NEW_CODES: tuple[str, ...]`. *house_rules:* no scoring key, rank or meter; importable vocabularies imported;
`NEW_CODES` declared with a per-code reason but the wrong type; `types.py` untouched. Breach: the no-retyping rule is
claimed and broken in the same file. *verbosity:* 810 lines / 37,647 chars of module carrying long plausible
docstrings for machinery never executed once; final message 0 chars against 25,518. *tool_use:* 28 calls (read_file
18, list_dir 3, grep 5, write_file 1, run_command 1), 0 malformed, 0 refused; the one `run_command` was `python3 -c
"import jsonschema; print(jsonschema.__version__)"`. **The module was written and never imported, run or tested**;
`run_tests.py tests.loop.test_roles` appears in neither pass. *overall:* the only substantial Kimi artifact in the
family, and it does not compile — `roles.py:234` is a bare `"""` under `# (The module continues below; this header
line is closed by __doc__ surgery.)`, which re-opens a string and yields `SyntaxError: unterminated string literal
(detected at line 295)`. Useful as a design sketch, useless as code.

**Opus.** *correct_claims:* `Ran 45 tests in 0.637s / OK`, one test per acceptance clause and named after it —
`test_runs_end_to_end_on_offline_provider_with_zero_sockets`,
`test_a_second_call_on_an_existing_coordinate_raises_no_replay`,
`test_at_schema_repair_budget_zero_an_invalid_output_yields_unresolved`,
`test_a_repair_is_a_new_coordinate_with_its_own_write_once_record`; "slots_for is acquired, not reimplemented"
reproduced at `roles.py:910`, `return slots_for(seat.key_env, seat.max_concurrency)`; module imports with
warnings-as-errors. *incorrect_claims:* none; line counts exact. *missed:* nothing. *fabricated:* none; every imported
name resolves; `NEW_CODES` is a 13-tuple with no member already in the table and `FINAL.md` §4 says which table each
belongs in. *house_rules:* no network name (`urllib`, `requests.`, `socket.socket`, `http.client`, `urlopen`) in the
module; `types.py` untouched. *verbosity:* 25,518 chars; §3 runs to nineteen unsettled questions, thorough and
repetitive at 3.14-3.19. *tool_use:* null; verification command reproduced; no forbidden edit. *overall:* holds the
declared interface — `ROLES`, `call_role`, `RoleResult` with `raw_ref` and `prompt_ref` as dataclass fields,
`ProviderArmEnded`, `NO_REPLAY`. One deviation: like Kimi it writes `NO_REPLAY = "NO_REPLAY"` (`roles.py:286`),
because `types.py` exposes the code only inside the `FAILURE_CODES` tuple; its test pins it by membership instead
(`test_no_replay_is_a_declared_failure_code`).

**Comparison and cross-run.** Both reached the same architecture — a coordinate keyed by role/seat/pack/repair, one
write-once record per coordinate, `slots_for` acquired rather than reimplemented — and both retyped `NO_REPLAY` for
the same structural reason. They part on delivery: Opus wrote, tested, ran and reported; Kimi wrote a longer module in
one shot, never parsed it, and left "imported, never retyped" standing over a file that retypes. Opus `test_roles.py`
→ Kimi `roles.py`: **import error, every test**, one reason — `test_roles.py:43 from minireason.loop import contracts,
roles` → `roles.py:295 SyntaxError`. No test reaches a verdict, so the not-applicable bucket cannot be measured here.
Kimi tests → Opus module: **not runnable, no Kimi test file**.

---

## 3. c-03-markprep

**Kimi.** *correct_claims:* none — none made, and **zero** `run_command` calls in either pass. *incorrect_claims:*
none. *missed:* the whole task — `markprep.py`, `test_markprep.py`, and all six of `program_marks`, `write_baseline`,
`baseline_kinds`, `byte_identity_defeater`, `under_replicated`, `residue`. *fabricated:* none. *house_rules:* no
breach observable. *verbosity:* 0 chars against 23,046. *tool_use:* pass 1, 18 calls; pass 2, 17 calls (read_file 15,
list_dir 1, grep 1), 0 malformed, 0 refused, 0 run_command; verification command never run; nothing edited. *overall:*
the thinnest run in the family — two passes that read `types.py`, `standard.py`, `custody.py` and the two design
slices and stopped.

**Opus.** *correct_claims:* `Ran 56 tests in 0.109s / OK`, with a test class per acceptance clause, all green —
`test_baseline_is_written_and_sealed_before_any_residue_is_offered`, `test_editing_the_baseline_after_sealing_raises`,
`test_a_bare_shared_id_token_is_forced_unresolved_and_never_differs`,
`test_the_forced_row_never_appears_in_the_residue`, `test_byte_identical_commitments_record_d1_not_exhibited`; all six
declared names exist with the declared arity; module imports with warnings-as-errors. *incorrect_claims:* none; line
counts exact. *missed:* nothing. *fabricated:* none; `NEW_CODES = ('BASELINE_ALREADY_SEALED',
'BASELINE_REPLICATE_UNKNOWN', 'CELL_MALFORMED')`, none already in the table. *house_rules:* the module states the rule
rather than assuming it — `markprep.py:60`, marks are "never summed, averaged, weighted, ranked or reduced to one";
the one count-shaped phrase (`markprep.py:1027`, "the cases carrying fewer than the pre-registered replicate minimum")
is the design's own under-replication rule, rendered beside `MIN_RESOLVED_REPLICATES`. *verbosity:* 23,046 chars, the
least repetitive of the four. *tool_use:* null; verification reproduced. *overall:* the cleanest control —
seal-before-residue tested as an ordering, not just a return value, and "What I could not determine" names the real
gap (no C001 commitments in the sandbox, so the FCL parse runs on constructed rows).

**Comparison and cross-run.** Nothing to compare: a tested module against nothing on two passes. Both cross-run
directions **not runnable — no Kimi module and no Kimi test file**.

---

## 4. c-04-decide

**Kimi.** *correct_claims:* the imports it wrote are all real — `obligations.{BLOCK_CODE_PREFIX, CELL_MARK,
DISPOSITION, Evaluation, Loss, Obligations, Situation, Verdict}` and `deepreason_core.canonical.{canonical_json,
sha256_hex}` (checked by `hasattr` in the run's own sandbox); three executed probes are sound, e.g. it15 recovered
`evaluate(obligations, situation) -> Evaluation` by `inspect.signature` and it13 printed real `mark_triples` output
from a temp harness. *incorrect_claims:* none stated. *missed:* `test_decide.py`; the acceptance mapping; stubs;
unsettled questions; `NEW_CODES` (absent — `grep -n NEW_CODES` returns nothing); and every one of `situation`,
`mark_triples`, `decide`, `render_decision`, `Decision.stop`, `Decision.reason`, `Decision.record_sentences`. The file
is a docstring plus an import block. *fabricated:* nothing semantic, but the bytes are corrupt at `decide.py:151`, `
Evalu ation,` — a token split by a stray space inside an otherwise well-formed `write_file` argument; `SyntaxError:
invalid syntax`. *house_rules:* the docstring it did write is house-shaped and correct ("evaluate the guard rails
first, then the five O/P clauses in order, and return **exactly one** outcome … the mandatory ``would_reopen`` prose
on every stop"); no scoring key or count-shaped clause, but there are no clauses; `NEW_CODES` not declared; `types.py`
untouched. *verbosity:* 154 lines / 8,166 chars, ~140 of them docstring; final message 0 against 21,919. *tool_use:*
27 calls (read_file 18, grep 5, write_file 1, run_command 3), 0 malformed, 0 refused — three real probes, the best
tool discipline Kimi showed here. The `write_file` turn ended `finish_reason: "tool_calls"` at 2,037 completion
tokens, so the model closed the JSON itself: the truncated module is a worker decision, not a transport cut.
`run_tests.py tests.loop.test_decide` never run. *overall:* the run understood the task — its docstring names design
§5, the five clauses, `would_reopen`, `losses_outside_P` and FW5:802 correctly — and then emitted a file with no
executable body. Comprehension and delivery came apart.

**Opus.** *correct_claims:* `Ran 68 tests in 0.198s / OK`; "identical mark-triple sets stop as a set identity and not
as a count" reproduced at `_clause_4_set_identity` (`decide.py:795-823`), which compares two `frozenset`s with `==`
and records "The test is set identity and not a count: no quantity of readings, …"; the budget stop emits
`BOUNDARY_NOT_EXHAUSTION` (imported from `standard`) plus "It is an attention-and-spend question that was declared
before cycle 1, never an adjudication of anything read."; the streak stop records "This is a fault in the instrument,
not a finding about the material." *incorrect_claims:* none I could not reproduce. *missed:* nothing. *fabricated:*
none; `NEW_CODES` is a 6-tuple, none already in the table, and `mark_triples` is re-exported from `graph`
(`decide.py:147`), not reimplemented — the correct reading of wave-1 decision 4. *house_rules:* "no count of readings,
marks, endpoints or differs appears in any clause" holds; the only `len(...)` in a decision path is `len(parts) != 3`,
a triple-shape validation. Clause 8 is handled honestly: `assert_module_pinned(plan_8a_mirror)` raises
`DECIDE_MODULE_PIN_MISSING: the plan pins no src/minireason/loop/decide.py` (I reproduce it) and `FINAL.md` §5 says
"*'the module digest matches the one pinned in plan.json'* is **unresolved** as a fact about a real plan file: there
is no such file to match against." *verbosity:* 21,919 chars, the shortest FINAL.md; §5 names seven distinct gaps.
*tool_use:* null; verification reproduced; no forbidden edit, one empty `.tmp/` left behind. *overall:* one real
interface deviation — the entry declares `situation(harness, cycle)`, the control writes `situation(harness, cycle, *,
obligations, …)`, and `situation(None, 1)` → `TypeError: situation() missing 1 required keyword-only argument:
'obligations'`. Any caller written to the design entry breaks. `decide`, `render_decision` and `mark_triples` match.

**Comparison and cross-run.** Both read the sources to the same conclusions in prose — five clauses after guard rails,
set identity not a count, `would_reopen` on every stop. Opus turned that into 1,213 lines and 68 tests and reported
one clause unresolved for a stated reason; Kimi turned it into 140 lines of docstring and stopped mid-import. The one
place Opus is weaker is fidelity: it widened `situation()` past an interface it was told it could not negotiate, and
its own tests call the widened form, so nothing caught it. Opus `test_decide.py` → Kimi `decide.py`: **import error,
every test** — `test_decide.py:43 from minireason.loop import decide as decide_module` → `decide.py:151 SyntaxError:
invalid syntax`. Kimi tests → Opus module: **not runnable, no Kimi test file**.

---

## 5. Family-level reading

**Recurring Kimi behaviours.** The strength is orientation: reading order was sensible on all four tasks and the few
executed probes were accurate — c-01's single probe returned `banner len 1251 / registers ('T', 'E', 'D', 'G')`, which
I reproduce exactly, and c-04's three probes recovered real signatures instead of guessing. It imports shared
vocabulary from the owner where an importable name exists (c-02: `ROLES: tuple[str, ...] = contracts.ROLE_NAMES`). The
first weakness is **write-once-and-walk-away**: neither delivered file was ever parsed, imported or run by the worker
that wrote it, and `run_tests.py` — named in all four prompts as the thing to iterate against — was never invoked in
any pass of any task. Both delivered files are un-parseable, and one advertises it: c-02 `roles.py:234-236`, a bare
`"""` under `# (The module continues below; this header line is closed by __doc__ surgery.)`. The second is
**confident unchecked citation**: c-02 `roles.py:134`, `from .types import UNRESOLVED_STEP # noqa: F401 (table
membership asserted by tests)`, names a symbol that exists only as a string inside a tuple at `types.py:371`. The
third: **no test file on any task in any pass**, so the Kimi→Opus direction of the conformance gate has nothing to
run, four times over.

**Recurring Opus behaviours.** All four modules import under warnings-as-errors and all four suites run green (61, 45,
56, 68 tests, each reproduced with `python3 run_tests.py tests.loop.test_<m>`); every acceptance clause carries a test
class named after it; and the no-retyping rule is pinned by identity rather than copied strings — c-01's
`self.assertIs(READING_BANNER, USE_RELATION_BANNER)`, reproduced as `True`, with the banner sentence absent from
`packs.py` altogether. It reports a clause it cannot satisfy as unresolved rather than faking it (c-04's
`DECIDE_MODULE_PIN_MISSING: the plan pins no src/minireason/loop/decide.py`). Two weaknesses: **interface drift under
no pressure to drift** — c-04's `situation(harness, cycle, *, obligations, …)` is not the declared `situation(harness,
cycle)` and raises `TypeError` when called as the entry writes it — and **long unsettled-question sections that
repeat** (c-02 §3 has nineteen entries, 3.14-3.19 circling one question). One figure does not reproduce: c-01's
"`packs.py` (1457 lines)" against `wc -l`'s 1456.

## 6. Infrastructure effects, separated from worker behaviour

1. **The 300 s gateway wall (pass 1).** All four family-C pass-1 runs ended `TRANSPORT_OR_RESPONSE_ERROR: Remote end
closed connection without response` at 343-561 s. c-02's module survives only because its write landed at iteration 15
before the wall; c-01, c-03 and c-04 were cut mid-reading. No worker property is visible in those terminations.
2. **The per-turn reasoning ceiling (passes 2-3).** `max_tokens` was 8192. Four family-C turns — c-01 p3 t11, c-02 p2
t14, c-03 p2 t8, c-04 p2 t17 — each spent the full 8192 on native reasoning (27.8-36.8 k chars; digests in
`RUNS-RECLASSIFIED.md`) and returned empty content with no tool call. The old harness read that as COMPLETE. The
reasoning text was never persisted, so what those turns concluded is unrecoverable; only that they put nothing on the
wire is known.
3. **Context re-send cost.** c-04 p2 sent 1,298,991 prompt tokens over 17 turns against 14,171 completion tokens; c-01
p2 sent 1,241,207 over 17. Each turn re-sends the whole transcript, so reading many files early makes every later turn
dearer. That shapes how far a run gets and is not a judgement about the worker.

A fourth, recorded so it is not repeated: gate 1 exactly as `evaluation.json` words it, with warnings promoted, fails
on an untouched sandbox because of `use_relation_h005.py:301` in the frozen material. A judge who runs that form will
read a material defect as a worker defect on both sides at once.
