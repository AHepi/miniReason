# W2-DECIDE — `src/minireason/loop/decide.py`

Written: `src/minireason/loop/decide.py` (1213 lines) and `tests/loop/test_decide.py`
(1044 lines), both inside the sandbox. Nothing else under `src/` was edited; no
published occurrence, frozen plan or `src/creib/**` was touched; no network call and no
provider call was made; no credential was read or written anywhere.

    $ python3 run_tests.py tests.loop.test_decide
    Ran 68 tests in 0.216s
    OK

    $ python3 run_tests.py          # discovery over tests/
    Ran 68 tests in 0.190s
    OK

(The 68 is that command's own output. The test run creates and cleans a temporary
directory under `<sandbox>/.tmp`; it writes nothing outside the sandbox and reaches no
socket.)

---

## 1. New failure codes, and which table each belongs in

`src/minireason/loop/types.py` may not be edited in this sandbox, so the codes are
declared at the top of the module as `NEW_CODES: tuple[str, ...]`, with a companion
`NEW_CODE_REASONS` mapping giving the one-line reason for each (the shape
`obligations.py` and `graph.py` already use).

**All six belong in one table: `types.FAILURE_CODES`** — the single operational-code
table. None of them is a semantic result about any material under study, so none belongs
in `STOP_REASONS`, `BLOCK_CODES` or `contracts.SCHEMA_REASONS`.

| code | why it exists |
|---|---|
| `DECIDE_MODULE_PIN_MISMATCH` | the plan pins a different digest for this module than this file has |
| `DECIDE_MODULE_PIN_MISSING` | the plan carries no pin for this module, so the rule that ran is unpinned |
| `DECISION_INPUT_INVALID` | `decide()` was called with something other than the situations, index, config and obligations it reads |
| `GUARD_READING_INVALID` | a guard-rail reading is the wrong shape, or is a per-seat rate where only a panel-level one is admissible |
| `MARK_TRIPLE_MALFORMED` | a mark-triple set is not a set of `(cell, register, mark)` string triples |
| `WOULD_REOPEN_MISSING` | a stop was built without the mandatory `would_reopen` prose |

Per wave-1 integration decision 6 and O9 the integrator also needs a `TOKEN_ARGUMENT`
entry for `decide.DecideError` in `tests/loop/test_types.py::TheCodeTablesAreComplete`,
so the wave-0 scan can see them.

The module also **re-raises two codes that already exist** and must not be duplicated:
`STOP_REASON_UNKNOWN` (a `Decision` built with a token outside `types.STOP_REASONS`) and
`RESOURCE_BOUNDARY_MISDESCRIBED` (raised by `standard.assert_no_exhaustion_claim`, which
every emitted sentence passes through).
`tests/loop/test_decide.py::DeclaredCodes::test_every_new_code_the_module_raises_is_declared_in_new_codes`
walks this module's syntax tree, collects every literal handed to `DecideError`/`_refuse`,
and asserts the set is exactly `NEW_CODES` ∪ (what `types.FAILURE_CODES` already carries);
a second test asserts `NEW_CODES ∩ FAILURE_CODES` is empty, so nothing is added twice.

One integration point the driver owns: **design §5 puts `decide.py`'s own digest inside
`loop_plan_id`, and `types.PINNED_SOURCE_PATHS` is wave 0's fixed six and does not carry
it.** The module exposes `MODULE_PIN_KEY = "src/minireason/loop/decide.py"`,
`module_digest()` and `assert_module_pinned(plan)`; W5-DRIVER must add that key to the
plan's `pins` map at PREREGISTER, or the decision rule that ran is unpinned.

---

## 2. Acceptance clauses, and how each is tested

Every clause of the wave-plan entry has a test class named after it. All eight are
satisfied.

**1. `decide()` is total and returns exactly one outcome.**
`DecideIsTotalAndReturnsExactlyOneOutcome`. A sweep over 2×2×2×2×2×2 = 64 combinations of
the material every clause reads (halted steps, declared arms, block streak, cycle index,
supplied mark sets, this cycle's registration record) asserts each call returns a
`Decision`, that its `clause` is a member of `CLAUSES`, and that `stop` is the exact
complement of `continues`; the sweep reaches more than one clause, so the totality is not
the totality of one branch. A second test fires four scenarios in which several clauses
would all answer and asserts the *first* in the declared order wins each time
(custody halt > all arms ended > instrument fault > protected loss). A third shows the
last clause always answers, so nothing falls off the end. A fourth asserts a malformed
argument is a coded refusal (`DECISION_INPUT_INVALID`, `GUARD_READING_INVALID`,
`MARK_TRIPLE_MALFORMED`) and never a returned outcome; a fifth asserts two situations
pinned to different obligations documents raise `OBLIGATIONS_PIN_SHIFTED` (FW5:787).

**2. A protected loss stops and names the loss.**
`AProtectedLossStopsAndNamesTheLoss`. `p8` ("the appellate remains optional") goes from
satisfied to not-satisfied; the decision stops as `protected_loss`, `named == ("p8",)`,
and the record carries the obligation id, its statement, the artifact that witnessed the
loss and the sentence "no repair is claimed". Further tests: clause 1 pre-empts a
discharge that would otherwise continue; *every* failing `p` is named, not only the
first; a protected obligation that became **unreadable** is exposed on
`Evaluation.protected_not_evaluable` and in the record and does **not** stop the chain
(FW5 R5); and a `p` already failing before cycle 1 still stops, because the clause is
"any *p* fails", not "any *p* changed".

**3. An `o` satisfied without this cycle's own artifacts does not continue.**
`AnOSatisfiedWithoutThisCyclesOwnArtifactsDoesNotContinue`. The same audit record makes
`o5` hold in two situations that differ only in whether it is in
`Situation.registered`: with an empty registration record `Evaluation.discharged` is
empty and the decision falls through to the default continuation; with the artifact in
this cycle's record it continues on clause 2 and names the artifact. Two more tests cover
the other half of `ProducedBy`: an `o` that already held at ξ is not a discharge however
recently an artifact appeared, and a `not_evaluable` `o` never makes "all satisfied" true.

**4. Identical mark-triple sets stop as a set identity and not as a count.**
`IdenticalMarkTripleSetsStopAsASetIdentityAndNotAsACount`. Equal sets stop as
`no_new_reading_changes`; two sets **of the same size** over the same cells do not stop;
a cell moving to contested drops its triple and changes the set; two empty sets are
identical and stop; an unsupplied set is recorded as *clause 4 not evaluated* and never
as no change. The identity compared is asserted to be W1-GRAPH's own object
(`assertIs(decide.mark_triples, graph.mark_triples)`, wave-1 decision 4), and one test
builds a **real harness**, opens two register cells, registers two rival marks, and
asserts the emitted set carries `unresolved` for a defaulted cell and drops a contested
one.

**5. A budget stop carries the boundary-not-exhaustion sentence and a `would_reopen`
field.** `ABudgetStopCarriesTheBoundarySentenceAndAWouldReopenField`. The stop carries
`standard.CEILING_REQUIRED_SENTENCES`' own boundary clause **verbatim** (selected out of
that tuple by the phrase `CEILING_EXHAUSTION_DENIAL` rather than retyped or indexed by
position), the boundary reached is named (`cycle_budget`, `max_calls`, or both),
`would_reopen` is non-empty and appears as its own section of the rendered record, and
the whole rendered text is re-scanned: with the ceiling's own denial removed, the stem
`exhaust` does not occur. A stop whose reopen prose is supplied empty is refused with
`WOULD_REOPEN_MISSING`, and every member of `types.STOP_REASONS` plus the parameterised
`preregistered_condition:` prefix is asserted to have reopen prose.

**6. A block streak stops as `instrument_fault` and names it a fault in the instrument,
not a finding about the material.**
`ABlockStreakStopsAsInstrumentFaultAndNamesItAFaultInTheInstrument`. A streak above
`config.audit.streak_max` stops as `instrument_fault`; a streak *at* the threshold does
not. The record says "fault in the instrument, not a finding about the material" and "no
cell is re-labelled by it", and a test asserts that **no member of
`standard.READING_VOCABULARY` or `standard.MARKS` and no seat name appears anywhere in
what this rail writes**. The stop carries `spawn == ("audit-the-reader",)` and
`stops_arm == "reading"`, and the rendered record says the other arms are untouched. The
threshold is printed beside the account `AuditConfig` requires of it, so the margin is
attackable. The calibration error rate reaches the same rail; a **per-seat** rate is
refused with `GUARD_READING_INVALID` naming "merit predicate over endpoints" (ceiling
clause 8, FW5:849); an unmeasured rate never fires the rail.

**7. No count of readings, marks, endpoints or differs appears in any clause.**
`NoCountOfReadingsMarksEndpointsOrDiffersAppearsInAnyClause` parses this module's own
syntax tree — the discipline `obligations.py` set — isolates the nine functions
implementing the three guard rails and the six clause positions, and asserts: no clause
calls `len`, `sum`, `min`, `max`, `abs`, `round` or `.count`; no numeric literal appears
in a clause outside a subscript; **every ordered comparison in a clause has an operand
that is one of the three declared thresholds** (`cycle_budget`, `streak_max`,
`judge_err_max`) and nothing else is ordered; clause 4's body is `curr_marks !=
prev_marks` with no `len`, `sorted`, `<` or `>` in it; the arms rail is `issubset`; and no
clause reads a name containing `readings`, `endpoints`, `agreeing` or a differs tally.

**8. The module digest matches the one pinned in `plan.json`.**
`TheModuleDigestMatchesTheOnePinnedInPlanJson`. `module_digest()` is asserted equal to an
independently computed `hashlib.sha256` of the file's bytes; a plan pinning that digest is
accepted; a plan pinning a different one is refused with `DECIDE_MODULE_PIN_MISMATCH`
naming both digests; four shapes of plan that pin no decision rule are refused with
`DECIDE_MODULE_PIN_MISSING`; and a one-byte flip of a copy of the module changes the
digest, is refused against the old pin, **and changes `types.loop_plan_id`** — which is
the point of design §5. See §5 below for what I could *not* check here.

Beyond the eight: `SituationReadsTheCycleEndGraph` covers `situation()` against a real
harness, `TheDecisionRecord` covers `losses_outside_P` (present when empty, written on a
stop as well as on a continuation, JSON-ready), `render_decision`, the declared
pre-registered condition, and the refusal of a decision sentence that describes a
boundary as the inquiry running out; `TheWavePlanPublicInterface` asserts every name of
the wave-plan entry is exported and that the shared vocabularies are the owners' own
objects.

---

## 3. What I implemented as a stub, and why

**Nothing in the public interface is a stub.** `situation`, `mark_triples`, `decide`,
`render_decision`, `Decision.stop`, `Decision.reason` and `Decision.record_sentences` are
all implemented and exercised.

Two things are deliberately *not* implemented here because they belong to another module,
and saying so is not a stub:

* **`mark_triples` is W1-GRAPH's function, re-exported, not a re-implementation.** Wave-1
  decision 4 fixes the identity W2-DECIDE compares as "the set as `graph.py` emits it", so
  a copy here would be a second thing to drift. `decide.mark_triples is graph.mark_triples`
  is asserted by test.
* **`decision.json` is not registered.** Design §5 says the decision record is registered
  with `provenance.role = IMPORT` and a `dependence` ref on every reading artifact it read,
  so that refuting a reading leaves it `suspended_unsupported`. This module holds no state
  and writes nothing; it returns a `Decision` whose `as_dict()` is that body. The
  registration is W5-DRIVER's, using `graph.py`'s registration path.

---

## 4. Where the sources did not settle a question: what I decided, and what changes if it
goes the other way

**(a) `situation(harness, cycle)` cannot be two-argument.**
`obligations.Situation` refuses to exist without the pinned document it is read under.
*Decided:* keep the positional shape and require `obligations=` as a keyword, adding
`since_seq=` (the log position `graph.produced` hands back) and `registered=`.
*Other way:* a module-level pinned document, or a `Situation` that carries none — then
`evaluate` could no longer refuse a shifted pin, and FW5:787 would stop being enforced at
the type level rather than by convention.

**(b) Where the mark sets and guard readings enter `decide`.** The entry's signature is
`(prev, curr, cycle_index, config, obligations)`, and a situation carries neither the
`(cell, register, mark)` set nor the step ledger, arm register or audit report.
*Decided:* keyword-only `marks=`, `prev_marks=`, `guards=`, each defaulting to "not
supplied", and a clause whose material was not supplied is **recorded as not evaluated**.
*Other way:* `decide` takes the harness and computes them — then it would depend on a live
harness (so a replayed or reconstructed situation pair could not be decided) and would
have to reach W1-STEPS and W3-AUDITS, neither of which is a declared dependency.

**(c) Clause 1: "any *p* fails" or "a *p* transitioned".** `obligations.protected_losses`
reports only satisfied → not_satisfied, which is empty before cycle 1.
*Decided:* the clause fires on any `p` reading `not_satisfied` at ξ′; both registers are
carried (`Decision.named` = every failing `p`, `Decision.protected_losses` = the
transitions). *Other way:* transitions only — a `p` already failing at cycle 1 would never
stop the chain, and `decide(None, curr, 1, …)` could never report a protected loss.

**(d) `prev=None` before cycle 1.** *Decided:* every `o` counts as failed at ξ, so a cycle-1
discharge is expressible. *Other way:* cycle 1 could never continue on clause 2; the
outcome would usually be the same (the default continuation) but the record would no
longer say that the cycle discharged anything.

**(e) Clause 2 is evaluated before clause 3, exactly as pre-registered.** The consequence
is that the cycle discharging the last outstanding `o` **continues**, and the chain stops
as `obligations_discharged` on the next cycle. *Decided:* implement the pre-registered
order literally and document the consequence; a test pins both cycles. *Other way:* 3
before 2 stops one cycle earlier — and would be an amendment to the pre-registered order
after first look, which mints a new `loop_plan_id` and is a new pre-registration.

**(f) Where `preregistered_condition:<id>` is evaluated.** `types.STOP_REASONS` carries
the parameterised member; the design entry does not place it among the five clauses.
*Decided:* after clause 5 and before the default continuation, so a declared convenience
condition can mask neither a protected loss nor a discharge nor the mark-set identity; a
test asserts it does not mask a protected loss. *Other way:* with the guard rails or before
clause 1 — a declared condition could then stop the chain while a protected loss went
unnamed.

**(g) The continue vocabulary.** No wave-0 module owns one (`STOP_REASONS` has no
continuation member). *Decided:* a two-member `CONTINUE_REASONS` local to this module
(`obligation_discharged`, `no_stop_condition_met`), asserted disjoint from
`STOP_REASONS`. *Other way:* leave `reason` empty on a continuation — the record could
then not say why the chain went on, and the two continuations would be indistinguishable
to W3-REPORT.

**(h) "`max_calls` is reached".** Only the driver holds the call ledger.
*Decided:* `Guards.calls_reached: bool`, a declared fact, so no call tally enters clause 5.
*Other way:* pass the tally and compare it here — a count would enter a clause, and the
"no count" acceptance clause would be much harder to defend.

**(i) The grain of `judge_error_rate`.** *Decided:* one **panel-level** fraction; a Mapping
is refused with `GUARD_READING_INVALID`. *Other way:* accept per-seat rates — an
`errors / anchors` per seat is a merit predicate over endpoints, which ceiling clause 8
forbids in as many words, and `instrument_fault` would start naming a losing seat.

**(j) `>` or `>=` at the instrument thresholds.** Design §5 says "*above* `STREAK_MAX`" and
"*above* `JUDGE_ERR_MAX`". *Decided:* strict `>`; a test pins that a streak *at*
`streak_max` does not fire. *Other way:* the rail fires one block (or one calibration
anchor) earlier, which at a five-anchor calibration set is a whole grain of the rate.

**(k) The module's own pin.** `types.PINNED_SOURCE_PATHS` is wave 0's fixed six and does
not carry `decide.py`, and I may not edit `types.py` here. *Decided:* expose
`MODULE_PIN_KEY`, `module_digest()` and `assert_module_pinned(plan)` and make it W5's job
to add the key at PREREGISTER. *Other way:* extend `PINNED_SOURCE_PATHS` — every existing
`loop_plan_id` changes, which is by design a new pre-registration for every run already
declared.

**(l) `cycle_index` versus `curr.cycle`.** Two names for one number. *Decided:* a
disagreement is refused (`DECISION_INPUT_INVALID`). *Other way:* silently prefer one — and
the audit obligation (which reads `situation.cycle_token`) and the budget clause could
then be evaluated at two different cycles in one call.

**(m) Importing `standard` although the entry lists only W0-TYPES, W1-OBLIGATIONS and
W1-GRAPH.** *Decided:* import `assert_no_exhaustion_claim`, `CEILING_REQUIRED_SENTENCES`,
`CEILING_EXHAUSTION_DENIAL` and `REOPEN_REASONS`, following W1-GRAPH's deviation 5 and the
instruction never to retype a shared vocabulary; the edge already exists transitively
through `graph`, so it adds no cycle. *Other way:* mirror them (W1-OBLIGATIONS' deviation 8
choice) — a second copy of the frozen ceiling's text, which is exactly the drift the
one-owner rule exists to prevent.

**(n) Who writes `would_reopen`.** The design makes the field mandatory and does not say
who supplies it. *Decided:* a per-reason default in `REOPEN_ACCOUNTS` (each naming
something a reader could go and do, and each drawing the reopen tokens from
`standard.REOPEN_REASONS` rather than retyping them), overridable per call, with an empty
override refused. *Other way:* require the caller always — `decide()` would no longer be
total without a caller-supplied string, which contradicts acceptance clause 1.

---

## 5. What I could not determine

* **`plan.json` is not in this sandbox, so I could not compare the module digest against a
  digest that is actually pinned anywhere.** The only `plan*.json` here is
  `src/minireason/loop/data/plan_8a_mirror.json`, which is the PLAN §8a register mirror — a
  different document. I implemented and tested the comparison in both directions
  (accepted, mismatched, missing, and a one-byte change moving both the digest and
  `loop_plan_id`), but *"the module digest matches the one pinned in plan.json"* is
  **unresolved** as a fact about a real plan file: there is no such file to match against.
* **Wave-1 integration decision 2 has not been carried out in this sandbox.** `graph.py`
  writes a `schema` field into every body it authors; `obligations.py` dispatches on a
  `record` field. So every predicate evaluated over a `Situation` read off a real harness
  is `not_evaluable` or `not_satisfied`, and I could **not** exercise the O/P clauses
  end-to-end against a real graph. I tested them against `Situation`s built from
  W1-OBLIGATIONS' own public constructors — which is the module's supported way to put a
  predicate into a known verdict — and recorded the gap in the test module's docstring
  rather than papering over it. When the reconciliation lands, the `SituationReadsTheCycleEndGraph`
  class is where the harness-backed verdict assertions belong.
* **Whether `decide.py` should itself join `types.PINNED_SOURCE_PATHS`** I could not settle:
  the file is not editable here, and the answer changes every existing `loop_plan_id`. I
  left it to the integrator and named it as an integration point above.
* **What shape W3-REPORT and W5-DRIVER want.** `report.py` and `tools/auto_loop.py` are not
  in this sandbox, so I could not check that `Decision.as_dict()`, `render_decision()` and
  the `CLAUSES`/`CONTINUE_REASONS` vocabularies are what their consumers expect. I chose
  the shapes the design entry names and kept everything else on the record object.
* **The `audit-the-reader` Spawn.** Design §5 says `instrument_fault` "Spawns
  `audit-the-reader`"; `deepreason_core` has `register_problem` under `Rule.SPAWN`, but the
  wave-plan entry does not make `decide.py` a writer and gives no spawn shape. I return the
  name on `Decision.spawn` and the arm on `Decision.stops_arm` and leave the registration to
  the driver. I could not determine the intended problem record, so I did not invent one.
* **What the guard-block streak is a streak *over*.** Design §5 says "a guard-block streak
  above `STREAK_MAX`" without saying whether it counts consecutive blocked trials per cell,
  per row or per run. W3-TRIAL owns the definition. I take whatever the driver hands in and
  call it "the guard-block streak" in the record; if W3-TRIAL settles it differently, only
  the prose in `_guard_instrument_fault` needs to change, not the rail.
* **Which `preregistered_condition:<id>` identifiers a real bundle declares.** No
  pre-registration bundle is in the sandbox. `Guards.conditions_met` accepts whatever the
  driver declares and validates only that the composed token is a legal stop reason under
  `types.is_stop_reason`.
* **Not covered at all, and not asked for:** the registration of `decision.json` into the
  graph with its `dependence` refs (W5), the rendering of the cycle record into
  `CYCLE.md` (W3-REPORT), and any interaction with the step ledger, publication or the
  cadence clock — `steps.py`, `publish.py`, `receipts.py` and `custody.py` are not in this
  sandbox, so nothing here was tested against them.
