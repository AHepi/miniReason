> Published verbatim, body unedited: this document was written against the staging tree `scratchpad/runner-multi/`, so `NOTES.md`, `FIXES.md` and the staged `src`/`tests`/`tools` paths it names are that scratchpad tree and not any path in this repository. Here the fork is `tools/multicycle_commitment_study_multi.py`, its suite is `tests/test_multicycle_commitment_study_multi.py`, the register it amends is `experiments/diagnostics/F001-fork5-multifamily/PLAN.md` with its six `occurrence-0N/arms.json` files, and the staging notes it corrects are `docs/design/multicycle-commitment-study-multi-notes-2026-09-14.md`. The suite line it quotes is the staging tree's 69 tests in isolation; in this repository the same tests run inside the whole offline suite as `PYTHONPATH=src python -X utf8 -m unittest discover -s tests`.

# Adversarial review of the multi-provider fork — every finding closed

Review: two lenses, 18 findings (3 high, 7 medium, 8 low), over the staged fork
at `scratchpad/runner-multi/`. This file maps **every** finding to the change
that closes it and to the test that pins it. Nothing in `/home/user/miniReason`
was modified; no socket was opened; no key value was read or displayed.

Suite, exactly as prescribed:

```
PYTHONPATH=<runner-multi>/src:<provider>/src:/home/user/miniReason/src \
  python3 -X utf8 -m unittest discover -s <runner-multi>/tests
Ran 69 tests in 14.7s — OK (0 failures, 0 errors, 0 skips)
```

42 before, 69 after: 27 new tests. Every fix below was additionally checked by
**mutation**: the change was reverted one edit at a time and the suite re-run.
**18 of 18 mutants fail, 0 survive.** Nine of the eighteen mutate code that
existed before this work and every one of those nine left the 42-test suite
green: the gate removed, widened to 500, or rebuilt per-wave (which is what it
was); the per-key admission widened to 50; the per-key clause of
`WAVE_SIZE_INVALID` deleted; `key_cap` hardcoded to 5 (which is what it was);
and each of the three wave-safety `raise`s replaced by `pass`.

One mutant from the review is **deliberately still green**, and B9 below says
why: swapping `ARM_COMPONENT` for `ID` inside `canonical_arm` changes nothing,
because by that line the only character the two disagree about has already been
folded. The rule is load-bearing in `at()`, and that is where the new test
puts it.

**Rulings → where each is closed.** 1 (per-key gate) → B1 + B2; 2 (untested
invariants) → B6; 3 (`registry=`) → B5; 4 (failure codes) → B4; 5(a)
(`lenient_control_chars` evidence) → A1; 5(b) (`native` arm, 66 → 67) → A2;
5(c) (`bare` is two controls) → A3; 5(d) (scope) → its own section; 5(e)
(dispatch cadence, `send-round`, rounds and pushes) → B3; 6 (the low items) →
the table at the end, plus A4, A5 and A6.

---

## The three high findings

### B1 — the per-key gate was dead code *(high)*

*Finding:* `send_wave` built `threading.BoundedSemaphore(5)` per key group
inside the call, where it could never block — `ready_coordinates` had already
capped the wave at five per `key_env`, so at most five threads ever contended
for a semaphore of five. NOTES.md:143-144 ("enforced twice") and §3.5
("load-bearing for an offline one") described a property the code did not have.

*Change* — `tools/multicycle_commitment_study_multi.py`:

* New module-level registry, mirroring `provider_openai_compat.slots_for`
  including its refusal to change a ceiling in force:
  `_GATE_LOCK`, `_GATES`, `key_gate(key_env, cap)` →
  `CONCURRENCY_LIMIT_CONFLICT`, plus a `_reset_gates()` test seam.
* `send_wave` now takes `gates = {key: key_gate(key, caps[key]) for key in groups}`,
  and the gate is acquired **before the attempt marker is written** — an attempt
  exists only for a call this process is about to make.
* Wave construction keeps its per-key cap and `WAVE_SIZE_INVALID` stays the
  first line (ruling 1), now derived from `key_cap` rather than a literal 5.
* New `key_caps` / `key_cap` / `MAX_PER_KEY`: the cap for a credential is
  `min(5, min(max_concurrency of the endpoints on that key))`.
* New `pending_wave` / `send_round` and the `send-round` CLI operation, which is
  what the process-wide gate makes safe (see B3).
* `max_workers` is now one thread per coordinate: the gate, not the pool, is the
  ceiling.
* NOTES.md §2(b) and §3.5 rewritten to say what is true: wave construction is
  the first line, the process-wide gate the second, `slots_for` the third; the
  fork's gate is the only one of the three that guards the *attempt marker*.

*Pinning tests* (`ProcessWideGateTests`):

| Test | What it forces |
|---|---|
| `test_the_gate_is_one_process_wide_registry_keyed_by_key_env` | one memoised semaphore per `key_env`; a changed ceiling is refused |
| `test_two_concurrent_send_waves_on_one_key_never_exceed_five_in_flight` | two occurrences, five coordinates each, one credential: the fixture holds the first five open and the settle window shows **5 active, 5 attempt markers, 5 calls** — with a per-wave gate all ten would have been admitted |
| `test_two_concurrent_send_waves_on_two_keys_reach_ten` | the gate does not over-constrain: `Barrier(10)` clears across two credentials |
| `test_send_round_sends_several_occurrences_against_one_commit` | the round command, an occurrence with nothing prepared, no replay on a second round, `OCCURRENCE_REPEATED` |

*Mutants now caught:* gate removed (`with gates[...]` → `if True:`); gate
replaced by a per-wave `BoundedSemaphore(500)`; gate replaced by a per-wave
`BoundedSemaphore(5)` (the exact code the review found). All three left the
suite green before.

### B2 — the per-key half of MULTI (b) had no coverage *(high)*

*Finding:* both concurrency tests used fixtures already holding exactly five per
key, so per-key in flight could not exceed five whatever the limiter did. Three
mutants survived: widening the admission in `ready_coordinates`, deleting the
per-key clause of `WAVE_SIZE_INVALID`, deleting the gate.

*Change:* the gate work above, plus a fixture that can actually over-subscribe a
credential — `LOPSIDED_ARMS`, seven arms on one key and three on the other, so
ten are ready while total capacity is ten and **only** the per-key admission can
truncate.

*Pinning tests* (`PerKeyAdmissionTests`):

* `test_more_than_five_ready_on_one_key_is_truncated_to_five` — the wave is
  5+3, not 7+3; the two held back are not lost (the occurrence drains to 50
  COMPLETE, 0 FAILED) and no wave ever exceeded five on a credential.
* `test_a_wave_carrying_six_coordinates_on_one_key_is_refused` — a hand-edited
  wave of 6+4 = ten, *within* total capacity, is `WAVE_SIZE_INVALID` with zero
  calls, zero provider constructions and no attempt written.
* `test_an_endpoint_asking_for_less_than_five_narrows_its_key` — an endpoint
  declaring `max_concurrency: 2` narrows `key_caps`, the plan and the wave.
* plus the two-concurrent-`send_wave` test above for the third layer.

*Mutants now caught:* `per_key.get(key, 0) < 5` → `< 50`; the per-key clause of
`WAVE_SIZE_INVALID` deleted; `key_cap` hardcoded back to 5.

### B3 — dispatch cadence, and the plan that understated it *(high)*

*Finding:* `check_published` byte-compares the transitive closure, which
includes the previous wave's receipts, so every `send-wave` needs its own
commit+push; the register implied a handful of pushes per occurrence and said
Ollama occurrences must run one at a time.

*Change* — PLAN.md **Operating sequence** replaced with the measured cadence,
and the runner gained the command that makes it possible:

* `send_round(repo, outputs, ...)` + `send-round --occurrences …` sends each
  occurrence's prepared wave concurrently **against one published commit**,
  under the shared per-key gate. Each occurrence still runs its own publication
  check, wave validation and `NO_REPLAY` refusal.
* PLAN now states plainly: **one process can drive all six occurrences**, the
  five Ollama ones sharing one gate of five on `OLLAMA_API_KEY` while
  occurrence-01 overlaps on `DEEPSEEK_API_KEY`; what is not authorised is two
  coordinator *processes* on one credential, because nothing here holds a
  ceiling across processes. The old "one Ollama occurrence at a time" rule is
  gone, replaced by the thing it was standing in for.
* **Measured, not estimated** (offline drive of all six occurrences over this
  exact material and these exact arms, `provider: offline`, no socket):

| Round | occurrence-01 | occurrences 02–06 | calls |
|---|---|---|---|
| 1 | 4 | 3 | 19 |
| 2 | 4 | 4 | 24 |
| 3 | 2 | 2 | 12 |
| 4 | 2 | 2 | 12 |
| | **12** | **11 each** | **67** |

  **Four rounds; four pushes before dispatch plus one final push** of round 4's
  records — five in all, against 24 prepare→push→send round-trips if the
  occurrences were driven one at a time. `required_paths` grows 64–66 → 82 →
  110 → 126 per wave, so a late `send-wave` runs ~126 `git show` comparisons.
  Round 2 asks for 20 Ollama calls at once and the shared gate admits five.

  (The reviewer's 60 waves and 360 round-trips were for the *unscoped* run —
  four problems × three cycles. Under the scope restriction of ruling 5(d) the
  authorised run is 4 rounds. Both numbers are now in the register: `max_calls`
  and `max_calls_envelope`.)

*Pinning test:* `test_send_round_sends_several_occurrences_against_one_commit`,
and `F001RegisterTests.test_each_occurrence_authorises_exactly_the_declared_calls`
for the call table. The cadence table itself came from an offline drive of the
six staged occurrences (`scratchpad/cadence.py`), which asserts every status is
COMPLETE and every audit ends `unvisited 0 / out_of_scope 0`.

---

## The mediums

### B6 — three declared invariants with no test *(medium)*

`PREPARED_WAVE_PENDING`, `UNRESOLVED_ATTEMPT` and `WAVE_NOT_DEPENDENCY_READY`
could each be deleted with the suite green. New `WaveSafetyInvariantTests`, all
three asserting **zero provider calls and zero provider constructions**:

* `test_a_prepared_wave_that_was_not_sent_blocks_the_next_prepare` — and that
  the next prepare succeeds once the wave is sent, so the refusal is not a
  deadlock.
* `test_an_attempt_with_no_receipt_stops_the_arm_before_any_new_wave` — plants
  an attempt with no receipt; `prepare_wave` raises `UNRESOLVED_ATTEMPT` (this
  is the invariant the ported "pending attempt marker" test never reached — that
  one exercises `NO_REPLAY`), and the audit reports `unresolved_attempts: 1`.
* `test_a_wave_whose_coordinates_drifted_is_refused_before_any_call` —
  substitutes a valid but not-yet-ready coordinate into the wave file.

*Mutants now caught:* each of the three `raise` statements replaced by `pass`.

### B5 — `registry=` plumbed inconsistently *(medium)*

*Ruling: pick the simpler.* The kwarg is **gone**; `set_registry` is the only
seam. Removed from `settings_for`, `read_arms`, `occurrence_arms`, `initialize`,
`verify`, `plan_body`, `read_terminal`, `read_artifact` and `send_wave`; every
function now resolves through `endpoints()`. `validate_arms(declared, registry,
mode)` keeps its **required** positional registry — it is the function that
freezes the mapping, and a required argument cannot be half-honoured.

*Pinning tests* (`RegistrySeamTests`): `test_no_public_function_takes_a_second_registry`
walks `inspect.signature` over eighteen public functions, so the trap cannot be
reintroduced; `test_every_resolution_follows_the_installed_registry` narrows the
registry and asserts that `settings_for`, `key_caps`, `wave_capacity`, `verify`,
`render_node`, `prepare_wave` and `audit` all refuse together.

### B4 — failure codes, and what one failure costs *(medium)*

* `send_wave` records `failure_code = getattr(exc, 'code', None)` beside
  `failure_type` in every receipt (`MULTI (k)` in the header and NOTES §2(k)).
* PLAN.md now states, under the resource boundary: **one `FAILED` node ends that
  arm for the rest of the occurrence**; the next `prepare-wave` returns *fewer
  coordinates* and refuses nothing; the audit signal is `counts.FAILED ≥ 1`
  together with `counts.unvisited > 0` and the arm's `invocations` row reading
  `"complete": false` — *read it after every round*.

*Pinning test:* `ProviderFailureTests.test_a_provider_failure_records_its_code_and_ends_that_arm`
drives a `ProviderFailure("HTTP_429")` and a `ProviderFailure("KEY_MISSING")`
through the real transport's offline path, asserts both codes in the receipts,
asserts neither arm appears in any later wave, and pins the audit signal
(`FAILED 4`, `unvisited 48`, two `"complete": false` rows, five cycle-1
coordinates never visited). *Mutant caught:* `failure_code` forced to `None`.

### A1 — the `lenient_control_chars` premise *(medium)*

*Finding:* the repair rested on an uncited empirical claim, beside a sentence
saying no provider output informed the design.

*Change* — PLAN.md:

* The false sentence ("No provider output existed when this design was written,
  and none was requested for it") is replaced by an accurate one: no provider
  output was produced *for* this study and none is evidence *in* it, but two
  existing records motivated the two repairs and both are cited where the
  repairs are declared.
* **`fence_stripped`** now cites
  `docs/sources/provider-openai-compat-smoke-notes-2026-09-14.md` §3 ("`kimi-k3`,
  `gemma4:31b`, `mistral-large-3:675b` on the compatible path") and the records
  behind it: `scratchpad/provider-smoke/run-02-ceiling-512/ollama__kimi-k3/call-0001.response.json`
  and `.../ollama__gemma4-31b/call-0001.response.json`, both returning a
  ```` ```json ```` block; both models are in scope (occurrence-05 and
  occurrence-06). Ten of the thirty contentful smoke responses are fenced; the
  probe was a one-line request, so it evidences the habit, not a rate.
* **`lenient_control_chars`** now cites the owner's own frozen records —
  `H005-open-prose-commitments/occurrence-01/responses/daily/matched/cycle01/response.txt`
  (7,732 bytes, `054b1c43…`) and `carry.txt` (6,505 bytes, `c61e45da…`): raw
  newlines inside JSON strings, strict `json.loads` raising at char 755 and 726,
  the same bytes yielding `{body, commitments}` under `strict=False`, both nodes
  recorded COMPLETE/OPAQUE with `commitments_sha256` the empty-string hash;
  root's review is `docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md`.
* And the limit is stated in the register rather than left to a reader: that
  record is **DeepSeek's**, not an Ollama family's; **zero** of the thirty
  contentful smoke responses are rescued by `strict=False` alone. The repair is
  declared for every family because the loss is a transport fault, and
  `audit.counts.lenient_control_chars` is where the run will say whether any
  family in scope commits it.

*Pinning test:* `EnvelopeUnwrapTests.test_the_declared_control_character_repair_rescues_the_records_it_cites`
reads both cited files, checks their sha256s, asserts the strict parse fails,
asserts `envelope_unwrap` rescues them with exactly `["lenient_control_chars"]`,
and asserts the owner's frozen receipts record OPAQUE/COMPLETE. The citation is
executable.

### A2 — the `native` arm *(medium)*

*Change:* `occurrence-01/arms.json` gains a `native` arm on `deepseek-flash`
(DeepSeek supports thinking on the wire). PLAN.md's Arms section now states the
comparison **per family** in a table: available and run on `deepseek`;
**unavailable** on the five Ollama families (`ollama-cloud/gpt-oss`, `/qwen`,
`/glm`, `/kimi`, `/gemma`) with the runner's own refusal code
`ARM_NATIVE_WIRE_UNKNOWN`, which is what `docs/EXPERIMENT_METHOD.md` requires
("mark that comparison unavailable"). Arms 18 → 19; calls 66 → **67**.

*Pinning test:* `F001RegisterTests.test_the_native_arm_is_declared_only_where_the_wire_supports_it`
— for each of the six staged occurrences, `"native" in arms` iff the family is in
`THINKING_WIRE`, with `thinking=True` on the native arm, `thinking=False` on
`bare` (DeepSeek) or `None` (Ollama), and an explicit `ARM_NATIVE_WIRE_UNKNOWN`
on every Ollama declaration attempt.

### A3 — `bare` is not the same control *(medium)*

*Change:* stated twice, in the Arms section and in Disclosure 2: **a
reasoning-disabled direct baseline on occurrence-01** (`thinking: {"type":
"disabled"}` on the wire) and **a default direct baseline on occurrences 02–06**
(reasoning on by default, no switch through this surface — the case
`docs/EXPERIMENT_METHOD.md` names), so a `bare` PARTIAL rate or token count read
across occurrences compares a reasoning-off arm with reasoning-on arms.

*Pinning test:* the same `F001RegisterTests` test asserts
`settings_for("bare", …).thinking is False` on occurrence-01 and `is None` on
02–06 — the asymmetry the sentence describes.

---

## Ruling 5(d) — scope, declared and enforced

The plan's `max_calls: 156` was the whole material envelope and authorised
nothing by itself. New in the runner (`MULTI (j)`):

* `validate_scope` / `in_scope` / `call_count`; `arms.json` may declare
  `"scope": {"problems": [...], "cycles": [...]}`, recomputed by `verify` and
  pinned by `arms_sha256`.
* `ready_coordinates` — and therefore `prepare-wave` and `send-wave` — refuses
  any other problem or cycle with **`SCOPE_EXCLUDED`**.
* `plan["max_calls"]` counts only what the scope admits, so it **is** the
  authorisation; `plan["max_calls_envelope"]` keeps the material figure.
* `audit` reads the same scope and counts anything outside it as
  `out_of_scope`.
* All six `arms.json` files now declare `{"problems": ["daily"], "cycles": [1]}`.
* With no scope declared, every one of these behaves exactly as before.

**Per-occurrence call table, verified:**

| Occurrence | endpoint | `bare` | `native` | `mini_fcl` | `mini_prose` | `max_calls` | envelope |
|---|---|---|---|---|---|---|---|
| occurrence-01 | `deepseek-flash` | 1 | 1 | 5 | 5 | **12** | 168 |
| occurrence-02 | `ollama/gpt-oss-120b` | 1 | — | 5 | 5 | **11** | 156 |
| occurrence-03 | `ollama/qwen3.5-397b` | 1 | — | 5 | 5 | **11** | 156 |
| occurrence-04 | `ollama/glm-5.3` | 1 | — | 5 | 5 | **11** | 156 |
| occurrence-05 | `ollama/kimi-k3` | 1 | — | 5 | 5 | **11** | 156 |
| occurrence-06 | `ollama/gemma4-31b` | 1 | — | 5 | 5 | **11** | 156 |
| | | | | | | **67** | |

*Pinning tests:* `F001RegisterTests.test_each_occurrence_authorises_exactly_the_declared_calls`
(the table above, built from the staged `arms.json` files against the shipped
24-endpoint registry, total pinned at 67) and `ScopeTests` (bounded plan,
`SCOPE_EXCLUDED` on every other cycle including a hand-written wave file, a
drained occurrence ending `unvisited 0 / out_of_scope 0`, eight malformed scopes
and an unknown problem refused). *Mutants caught:* `in_scope` forced true;
`max_calls` counting the envelope; `audit` ignoring the scope.

---

## The lows

| # | Finding | Change | Pinning test |
|---|---|---|---|
| A4 | Six changed definitions carried no `# MULTI` marker while the docstring claimed all do | Markers added to `arm_stopped`, `final_coordinate`, `prepare_wave`, `read_artifact`, `source_coordinate`, and to `project` (whose only difference *is* a comment, now marked `# MULTI: comment only, and this is the whole of it`) | `ForkHygieneTests.test_every_changed_definition_carries_a_multi_marker` — re-derives the census from both files' ASTs, pins the sixteen byte-identical names and the 25 changed, and fails if any changed definition lacks a marker. *Mutant caught:* one marker removed |
| A5 | NOTES §2 census missed `prepare_wave` and `key_environment_names` | Both named in §2(a); the registry-seam removal documented there too | Same AST census test (it would now fail on any *new* undeclared definition) |
| A6 | The end-to-end summary omitted the error-severity residue | NOTES §4 now quotes `ERROR-SEVERITY RESIDUE FIRED: ref_through_unexposed_view (1)` and says why it is the fixture's: the scripted `rival` document depends on `p.rival.0#c1`, a commitment-surface record reached through a **body**-only projection | `EndToEndImportTests.test_the_import_fires_one_error_severity_residue_from_the_fixture` |
| B7 | `write_new`'s credential guard was an unbounded substring scan with no minimum length; the final receipt write sat outside any guard | `MIN_CREDENTIAL_LENGTH = 16`; a shorter value is not searched for. The receipt write is now guarded: a `ValueError` refusal is rewritten once as a coordinates-and-hashes-only `FAILED` receipt with `validation_failure_type: RECEIPT_REFUSED`, so no spent call is stranded | `ForkHygieneTests.test_a_credential_too_short_to_be_one_is_not_a_leak` (a 1-char key writes; a 16-char key still refuses) and `test_a_refused_receipt_never_strands_a_spent_attempt` (audit `unresolved_attempts: 0`). *Mutants caught:* length guard removed; the refusal handler narrowed |
| B8 | `or ''` and `if key and …` described an unkeyed group that cannot exist | Both dropped; `arm_key_env`'s docstring now says every endpoint names a credential, and the same in `main`'s key prompt | `ForkHygieneTests.test_every_endpoint_names_a_credential_so_no_unkeyed_group_exists` — `endpoint_record` refuses an empty `key_env` (`ENDPOINT_FIELD_INVALID`), `EndpointSettings` refuses it (`INVALID_ENDPOINT_SETTINGS`), and all 24 shipped endpoints name one |
| B9 | `canonical_arm`'s "stricter of the two" rationale is vacuous at that call site | Docstring rewritten: the match there is a post-fold assertion; the strictness is load-bearing in `at()`, where the arm arrives unfolded. Same correction in the `ARM_COMPONENT` comment and NOTES §2(a) | `ForkHygieneTests.test_the_arm_component_rule_bites_where_an_arm_is_not_folded` — `at()` refuses `mini.prose` with `INVALID_COORDINATE` although `ID` admits it |
| B10 | `declared_name` accepted any JSON value into a pinned, published plan | Validated in `validate_arms`: printable non-empty `str` whose `canonical_arm()` equals the canonical key, else `ARM_DECLARED_NAME` | `ForkHygieneTests.test_a_declared_name_must_fold_to_the_arm_it_names` (one good spelling, seven bad). *Mutant caught:* the fold check disabled |
| B11 | `provider_mode` reduced a mixed set by alphabetic minimum (`live` wins); `max_concurrent_requests_per_key_env` was a hardcoded 5 ignoring `max_concurrency` | New `provider_mode(arms)` raises `PROVIDER_MODE_MIXED`; the plan field is now a mapping `key_env -> cap` derived from `key_caps`, and `max_concurrent_requests_total` is its sum — `wave_capacity`, `ready_coordinates`, `WAVE_SIZE_INVALID` and the gate all read the same caps | `ForkHygieneTests.test_a_mixed_provider_mode_is_refused_not_reduced`; `PerKeyAdmissionTests.test_an_endpoint_asking_for_less_than_five_narrows_its_key`. *Mutants caught:* the reduction restored; `key_cap` hardcoded |
| B12 | NOTES §(h) and the docstring called the timeout a per-arm declaration | Both corrected: `max_tokens` and `seed` are per-arm (`ARM_OPTIONAL`); `timeout_seconds` is surfaced per arm in `plan['ceilings']` but **read from the endpoint**, and an arm that declares one is `ARM_FIELDS` | `ForkHygieneTests.test_the_timeout_is_the_endpoints_and_no_arm_may_declare_one` |

---

## Two things that moved under the fork during this work

Both were re-synced and re-proved rather than pinned to a stale copy; both are
build inputs, not deliverables, and the staged tree only ever reads them.

1. **The published importer** went `fc9f4a76…` → `e5bd327a…`
   (`/home/user/miniReason` advanced from HEAD `8a99d3fb` through several
   commits, `d0e5d343` at the final run; the new importer bytes are committed
   there, and the staged copy is byte-identical to them). The
   end-to-end test asserts byte-identity by hash, so it caught the drift; the
   staged copy was re-synced from the owner's tree and the whole import proof
   re-run against it — 24 events, custody verified on every node, labels, edges
   and residues unchanged.
2. **The provider module** went `3cbdd566…` → `cdc4b571…`. It now refuses a
   DeepSeek call whose reasoning presence disagrees with the thinking control
   (`THINKING_MODE_MISMATCH`) — which is *why* the `native` arm added under A2
   is meaningful: a native arm that silently ran without reasoning is now a
   `FAILED` node, not a mislabelled COMPLETE. The offline fixture was corrected
   to script reasoning presence that matches the control, since scripting
   otherwise scripts a response the wire cannot produce. Recorded as assumption
   §3.8 in NOTES.md.

If either source moves again the suite will say so, which is the point of
asserting the equality in a test rather than in a sentence.

## Choices taken where the ruling offered one

* **Ruling 3 (`registry=`)**: removed the kwarg rather than threading it through
  five more functions — the simpler of the two, and it leaves one seam
  (`set_registry`) instead of eleven optional ones.
* **Ruling 6 (MULTI markers)**: added the six markers rather than softening the
  docstring, and then made the docstring's claim a test.
* **Ruling 1 (gate)**: made it real rather than deleting it. Deleting it would
  have left `send-round` unsafe, and `send-round` is what turns 24 push cycles
  into 4.
