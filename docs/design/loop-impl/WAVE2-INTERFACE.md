# Wave 2 — the integrated public interface

Read `WAVE0-INTERFACE.md` and `WAVE1-INTERFACE.md` first. This is the wave-2
integrator's record of what the four wave-2 modules expose after reconciliation,
what moved in waves 0 and 1 to let them agree, the disposition of every item the
orchestrator assigned, and what waves 3–6 must still settle.

Clone: `scratchpad/loop-impl/repo`, branch cut at `9045a94`; the loop tree is
untracked there and nothing was committed.
Sources: `src/minireason/loop/{packs,roles,markprep,decide}.py`, with edits in
`{types,standard,obligations,graph,seats,steps}.py`;
tests: `tests/loop/test_{packs,roles,markprep,decide}.py` and the same six.

Verified on the quiesced tree — loop-only
`PYTHONPATH=src python3 -X utf8 -m unittest discover -s tests/loop -t .`:
**before `Ran 1160 tests` OK; after `Ran 1223 tests` OK (skipped=1)**, the one
skip being the PLAN-digest pin on a checkout that predates §15 (§9).
Whole repository, `PYTHONPATH=src python3 -X utf8 -m unittest discover -s tests`
(the workflow's own command): **before `Ran 2403 tests` FAILED (failures=2,
skipped=1); after `Ran 2466 tests` OK (skipped=2)**. The two failures were
`tests/test_provider_openai_compat.py`'s no-network tests, killed by a socket
patch this package's own test file leaked (§9).

No provider call was made, no credential was read, and nothing outside the clone
was written. Two files outside the clone were **read** read-only, both named by
the coordinator: the live `experiments/diagnostics/C001-contrast-triple/PLAN.md`
and its `material.json`.

---

## 0. The one-page map

```
types ──► standard ──► contracts ──┬──► surface ──┬──► packs
  │   (LoopError)  (every vocabulary)│             └──► markprep (also ◄── custody, standard)
  ├──► custody ──┐                  ├──► seats ────────► roles   (also ◄── custody)
  ├──► receipts ─┼──► steps         ├──► graph ────────► decide  (also ◄── obligations, standard)
  ├──► publish ──┘                  └──► synthetic
  └──► obligations ──────────────────────────────────────┘
```

Exactly, as `tests/loop/test_contracts.py::…::test_the_import_graph_is_the_one_the_interface_documents`
now walks it (the walk used to read only absolute `minireason.loop.<x>` imports
and so missed every `from .types import`, which is how ten of the sixteen
modules import their siblings):

| module | imports (siblings only) |
|---|---|
| `packs` | `contracts`, `standard`, `surface`, `types` |
| `roles` | `contracts`, `custody`, `seats`, `types` |
| `markprep` | `contracts`, `custody`, `standard`, `surface`, `types` |
| `decide` | `graph`, `obligations`, `standard`, `types` |

**No wave-2 module imports another wave-2 module.** Two classes of edge go
beyond the wave plan's `depends_on` lists, and both are recorded here per
decision 54: every wave-2 module reaches **W0-STANDARD**, because the ceiling
sentences and `assert_no_exhaustion_claim` have exactly one owner and a module
that retyped either would be a second; and `markprep` reaches **W1-SURFACE**,
because the pairwise surface is built out of `Surface`/`Span` and resolved with
`resolve_unique` — one resolver, not two. The graph is acyclic and the test
asserts the exact edge set as well as the acyclicity, so a later wave that adds
an edge has to record it here first.

---

## 1. `packs.py` — W2-PACKS

**What it is.** The deterministic render of every role's pack, plus the
*exchange* surface `E` of G2(b). It calls no provider, opens no file, writes
nothing, reads no clock and draws no random number.

**Renderers.** `render_row(surface, standard, framing) -> Pack`;
`render_exchange(pack, critic, defender=None) -> Pack` (`defender=None` gives
the **defender** pack, a defender gives the **judge** pack — one renderer, two
packs, the role in `Pack.role`); `render_register(cell, register, comparison,
baseline_sha, standard) -> Pack`; `render_paraphrase_request(exchange) -> Pack`;
`both_orders(pack)` for G6.

**Exchange surface.** `exchange_surface(case, answer) -> Exchange`;
`Exchange.count` counts **overlapping** occurrences (strictly stronger than
`str.count`, which calls `aa` unique in `aaa`); `Exchange.resolve` gives the
unique span and which part it fell in; `Exchange.conforming` is the vendored
predicate kept beside it so W3-TRIAL asserts the stronger check first and the
vendored one last. `Exchange` offsets are **code-point** offsets into a `str`;
`surface.Offset` offsets are **utf-8 byte** offsets into frozen bytes. The two
coordinate systems never meet.

**Precedent.** `precedent_slice(harness, standard_id, k) -> PrecedentSlice`
(which *is* a `list`, carrying the query text that selected it);
`PRECEDENT_K`, `PRECEDENT_QUERY`, `PRECEDENT_KINDS`.

**Guards.** `pack_sha(pack)`, `assert_pack_clean(pack)`,
`assert_no_adjudication_keys(value)`, `FORBIDDEN_PACK_KEYS`.

**Exceptions and codes.** `PackError(code, detail="")`;
`BaselineNotFirst(detail="")` carrying `BASELINE_NOT_FIRST` (wave 0's code, not
new). New: `PACK_INPUT_INVALID`, `PACK_ADJUDICATION_KEY`, `EXCHANGE_MALFORMED`,
`PRECEDENT_QUERY_INVALID`.

---

## 2. `roles.py` — W2-ROLES

**What it is.** The one place the loop speaks to a model. One `call_role` is one
`provider.complete`. **No retry anywhere.**

**Callers.** `call_role(role, seat, pack, schema, records_dir, *, coordinate,
register=None, repair=0, provider_factory=None)` and the five thin wrappers
`call_critic` / `call_defender` / `call_judge` / `call_variator` / `call_marker`.
Helpers: `role_pack`, `seed_for`, `max_tokens_for`, `response_format_for`,
`provider_reason`, `default_provider_factory`.

**Result.** `RoleResult` with `status` (`STATUS_OK` / `STATUS_BLOCKED`),
`output`, `block`, `reason`, `transport_code`, `prompt_ref`, `raw_ref`,
`record_path`, `record`, `arm_ended`, and `raise_if_arm_ended()`.

**Gates.** `GATE_ORDER = ("seats.key_gate_for",
"provider_openai_compat.slots_for")`, outer first, and **new in this
integration** `GATE_HELD_BY`, which names what acquires each. Every call record
now carries `settings.gates` with `outer_held_by` and `inner_held_by`;
`inner_held_by` is `null` for a provider that holds no inner gate (the offline
one), so a reader can tell *not held* from *not recorded* (decision 42(c)). A
test asserts that this module never calls `slots_for` or constructs a semaphore.

**Exceptions and codes.** `RoleRefused(code, detail="")` — plan errors only;
`ProviderArmEnded(code, detail, *, result=None)`, raised only by
`RoleResult.raise_if_arm_ended`. A provider failure is **returned**, never
raised: a route that did not answer is a delivery fact, not a reading.
New codes: `PROVIDER_GATEWAY_WALL` (a *reason* on a result, never raised),
`ROLE_UNKNOWN`, `ROLE_SEAT_MISMATCH`, `ROLE_COORDINATE_INVALID`,
`ROLE_PACK_INVALID`, `ROLE_PACK_NOT_JSON_MODE_READY`,
`ROLE_SCHEMA_NOT_THE_CONTRACT`, `ROLE_REGISTER_REQUIRED`, `ROLE_REPAIR_REFUSED`,
`ROLE_TOKEN_BUDGET_UNREACHABLE`. `NO_REPLAY` is **imported from `types`**, not
retyped (§6, judge finding 2).

---

## 3. `markprep.py` — W2-MARKPREP

**What it is.** Everything the *program* can settle about a C001 contrast cell
before any marker call, and nothing else. No provider, no socket, no warrant, no
registration, no pack.

**Loading and shapes.** `load_occurrence(dir) -> Occurrence`;
`Occurrence.cell_keys`, `Occurrence.cell(endpoint, arm)`;
`cell_from_contrast_leg(leg) -> Cell`.

**The pre-pass.** `byte_identity_defeater(cell)`, `under_replicated(cell)`,
`build_baseline(cell, replicates=None) -> Baseline`, `baseline_kinds(cell)`,
`write_baseline(cell, replicates, out_dir) -> sha256`, `read_baseline(out_dir)`,
`verify_baseline(out_dir, sha256)`, `program_marks(cell)`, `residue(cell)`.

**The pairwise surface.** `pairwise_surface(cell, left, right, register)` and
`resolve_pair(...)`, built on `surface.Surface`/`Span` and resolved with
`surface.resolve_unique` / `within_declared_span`.

**Exceptions and codes.** `MarkprepError(code, detail="")` (also a
`ValueError`), `BaselineNotFirst`, `BaselineSealBroken`. New codes:
`MARKPREP_INPUT_MALFORMED`, `COMPARISON_SCHEMA_UNKNOWN`, `CELL_NOT_IN_OCCURRENCE`,
`REPLICATE_BYTES_DISAGREE`, `BASELINE_RESEALED`, `BASELINE_SEAL_BROKEN`,
`REGISTER_UNKNOWN`, `REPLICATE_UNKNOWN`, `REPLICATE_NOT_READABLE`.
`BASELINE_NOT_FIRST` is wave 0's, shared with `packs`.

### 3.1 The shared cell shape (decision 52 / 27(g)) — **markprep owns it**

W2-PACKS and W4-MARKER read these and define none of them.

```
Occurrence  .root .schema .cell_keys[(endpoint, arm)] .cell(endpoint, arm)
Cell        .cell_id .endpoint .arm .source .cases .comparisons
            .replicates[case] -> tuple[Replicate, ...]
            .resolved(case)   -> replicates with delivered bytes
            .readable(case)   -> resolved replicates the FCL parse read
            .seal(sha)/.require_seal(where)   # G8: the baseline sha, once
Replicate   .key .case .ordinal .commitments .sha256 .resolved .read (FclRead)
Baseline    .cell .case .replicates .readable .kinds{register: tuple}
            .undecided_kinds{register: tuple} .pairs[BaselinePair]
            .min_resolved_replicates .sufficient .note .exhibits(register, kind)
BaselinePair .left .right .kinds
ResidueRow  the register, the kinds left open, and the rows that defeated the program
```

**Pairwise convention.** `SIDE_LEFT = surface.SIDE_REFERRING_RECORD`,
`SIDE_RIGHT = surface.SIDE_TARGET_RECORD`. On a C001 pairwise surface the
`ref_*` slots carry the *comparison*, not a cross-document reference:
`ref_field` is `commitments` (the field both sides are read out of), `ref_grain`
is `artifact`, `ref_verbatim` is the comparison label.

**Alias map.** `packs` shows the two sides as `A` and `B` in the pack *text* — a
seat told which side is ORIGINAL is being told half the answer — and the
alias→arm map lives in the pack *record* under
`parts["presentation"]["side_aliases"]`. W4-MARKER de-aliases through that and
passes `register=` to `contracts.check`.

---

## 4. `decide.py` — W2-DECIDE

**What it is.** The pre-registered stop/continue program. Total, pure, and it
computes no arithmetic: a hardened AST guard in `tests/loop/test_decide.py`
refuses every binary operator, every numeric literal outside a subscript, `len`
/ `sum` / `min` / `max` / `abs` / `round`, `statistics` / `Counter`, and — new
here — every ordering comparison outside the two functions the pre-registration
names as instrument bounds.

**Entry points.** `situation(harness, cycle, obligations, *, registered=())`
(see §6), `mark_triples(harness)`, `decide(prev, curr, cycle_index, config,
obligations, *, instrument=None, prev_triples=None, curr_triples=None)`,
`render_decision(d)`, `instrument_bound_crossed(instrument, config)`,
`declared_boundary_reached(cycle_index, config, instrument)`.

**Order of evaluation** (`CLAUSE_ORDER`): three guard rails — `custody_halt`,
`all_arms_ended`, `instrument_fault` — then clause 1 `protected_loss`, clause 2
`obligation_discharged` (a CONTINUE), clause 3 `obligations_discharged`, clause
4 `no_new_reading_changes` (set identity), clause 5 `resource_boundary`, then
**new here** the declared-condition clause, then the open continuation.

**Pins.** `DECIDE_SHA256` is this file's own sha256 and `MODULE_PIN_KEY =
"src/minireason/loop/decide.py"` is the key the driver folds it in under at
PREREGISTER (decision 28(h)). It is a *run-specific* pin of design §4.2's list;
`types.PINNED_SOURCE_PATHS` is the fixed six and does not carry it.

**Exceptions and codes.** `DecisionRefused(code, detail="")`. New codes:
`DECISION_SITUATION_INVALID`, `DECISION_CYCLE_INVALID`, `DECISION_CONFIG_INVALID`,
`DECISION_INSTRUMENT_INVALID`, `DECISION_WOULD_REOPEN_MISSING`,
`DECISION_REASON_UNKNOWN`.

---

## 5. The code tables after wave 2

`types.FAILURE_CODES` now carries **201** members and is complete for all
sixteen modules; `tests/loop/test_types.py`'s `FRONTIER` is **empty** and
`FOLDED_IN` names all sixteen. Twenty-nine codes were folded in this pass
(packs 4, roles 10, markprep 9, decide 6) with a `TOKEN_ARGUMENT` entry per
exception constructor, and the scan's four "a new code is one the table does not
carry" tests were restated as their fold-in contract: every `NEW_CODES` key is a
member of `FAILURE_CODES` and of neither other table.

Two allow-list entries were added, each with the reason it is unraisable:
`PROVIDER_GATEWAY_WALL` (roles records it on a result, never raises it) and a
reworded `NO_REPLAY` (types owns the spelling; roles imports it, so the
literal scan no longer sees it at the raise site).

**One parameterised failure family is now declared** (decision 42(b)):
`types.is_failure_code` admits `HTTP_<status>` for a three-digit status in
classes 1–5, as it already admitted `preregistered_condition:<id>` in
`STOP_REASONS`. The transport raises one code per HTTP status, not only the
`HTTP_429` the table names, and a receipt carrying `HTTP_503` was carrying a
code no table declared. `HTTP_429` stays an explicit member.

`types.BLOCK_CODES` is unchanged at ten; `types.OUTCOME_CODES` at one.

---

## 6. The two judge findings of family C

### Finding 1 — `situation()` drifted from the declared entry. **Recorded, not restored.**

The wave plan declares `situation(harness, cycle)`. What is implemented is
`situation(harness, cycle, obligations, *, registered=())`, and the third
argument is required rather than optional for three reasons, now written into
`decide.py` deviation 3 and pinned by
`tests/loop/test_decide.py::TheDeclaredEntryPoints`:

1. **`obligations` is a field of `Situation`, not an argument of a later call
   on it.** `Situation.verdict(o)` and `Situation.check(o)` evaluate the
   predicates O and P name; a situation built without them carries no predicates
   and answers `not_evaluable` to every question.
2. **The obligations document is not in the graph.** W1-GRAPH registers the
   standard, the material, the cell-opens, the readings, the validity nodes, the
   warrants, the audits and the appeals. It has no obligations artifact and
   `obligations.RECORD_KINDS` has no token for one, so `harness` cannot supply
   what the two-argument entry would have to find. The test asserts this
   directly: no name in `graph` contains "obligation".
3. **An empty default would be worse than the deviation.** A caller using the
   declared spelling would get a well-formed `Situation` that discharges
   nothing; `decide` would read "no `o` was discharged this cycle" off it and
   clause 2 would silently never fire. A missing argument is a `TypeError` at
   the call; a silently empty O is a wrong decision in a published record. The
   test builds exactly that situation and shows clause 2 does not fire.

   Re-binding O onto a situation inside `decide` was also rejected: it would
   make the prior situation and the current one evaluable under *different*
   documents, which is what FW5:787 forbids inside one assessment.

A wave-3 or wave-5 caller that wants the declared spelling gets it by partial
application at the driver, where the pinned obligations are already in hand.

### Finding 2 — `NO_REPLAY` had two spellings. **One owner: `types`.**

`roles.py` carried `NO_REPLAY = "NO_REPLAY"` because `types` exposed the code
only inside `FAILURE_CODES`. `types` now declares the module-level constant,
builds `FAILURE_CODES` from it, and exports it; `roles` does
`from .types import NO_REPLAY` and keeps the name in its own `__all__`, so
`roles.NO_REPLAY` still works for every caller and test. Runner v2 raises
`FileExistsError('NO_REPLAY')` as a bare literal and is frozen, so it is not a
candidate owner. Pinned by
`test_roles.py::…::test_no_replay_is_imported_from_types_and_never_retyped_here`,
which also asserts the literal is absent from the roles source.
The `roles.py` literal scan was widened to treat an *imported* string constant
as a named constant, so importing a code is not mistaken for raising a literal.

---

## 7. Disposition of items 24–28, 42, 48–54

| item | disposition |
|---|---|
| **24** marker packs offer only their register's kinds | **Already held.** `_contract_block` narrows `difference_kind.enum` to `difference_kinds_for(register)` and `render_register` records the same tuple; the pinned `MARKER_SCHEMA` and its digest are untouched. Verified, not changed. |
| **25** appellate recognition for precedent ordering | **Already held and tested.** `graph.apply_appeal` writes `record: "appellate_ruling"`; `packs.precedent_slice` reads that token (not `provenance.school`). `test_packs.py::…::test_an_appellate_ruling_ranks_first_even_when_registered_last` registers one through `graph.apply_appeal` and asserts it ranks first. |
| **26** §2.3 tension: precedent slice vs "no other cell's outcome" | **Applied as ruling, documented.** New deviation 10 in `packs.py`: the slice is the explicit exception, narrowed to the precedent's relation and cited passage; no status, label, standing, `att`, `dep` or `sustained` value is rendered; the query text that names `accepted` rides on the pack *record*, never in the prompt; authority is pack ordering and nothing else. |
| **27** markprep reconciliation (a)–(g) | **(a)** byte identity is a *finding*, not a call pre-empt — held, docstring §1. **(b)** E is program-*resolved* and never program-*marked*; G neither — held, `NOT_PROGRAM_READ` carries the reason for each of the three kinds. **(c)** *reconciled differently and recorded*: the **baseline** is at replicate-pair grain and the forcing pairs are recorded in `forced_by.pairs`; the **cross-case** read is the union over a case's resolved readable replicates. Union-differs implies some-pair-differs but not conversely, so the union read is the *conservative* one — it withholds where an existential would produce a `differs` from one unreadable replicate. **(d)** `baseline_kinds` for an unreadable register is carried in `undecided_kinds`, never as `()` — held. **(e)** under-replication is measured against the cell's own resolved replicates — held. **(f)** settled from the material: the importer's ref fields are `target/depends/mentions/revises/withdraws`, there is no `engages`, and register E's "takes up" reading is therefore `record_engaged`, listed in `NOT_PROGRAM_READ` because §8a admits engagement by quotation and quotation is not a formal field. **(g)** the shared cell shape is published above, §3.1. |
| **28** decide reconciliation (a)–(i) | **(a)** clause 1 fires on any `p` not satisfied at ξ′ — held. **(b)** `prev=None` counts every `o` as failed at ξ — held, `_failed_at_prior`. **(c)** clause 2 before clause 3, consequence documented: the cycle that discharges the last `o` **continues**, and the chain stops as `obligations_discharged` on the next cycle. **(d)** **applied**: `preregistered_condition:<id>` is now a clause, evaluated *after* clause 5 so it masks nothing; it arrives on `Instrument.preregistered_condition` as a bare id, `types.is_stop_reason` refuses an id containing `exhaust`, and the two prose tables are keyed by the prefix. **(e)** `max_calls` reached enters as `Instrument.calls_reached`, a declared boolean — held. **(f)** only a panel-level fraction is read; no per-seat rate — held. **(g)** strict `>` at both bounds — held. **(h)** **applied**: `MODULE_PIN_KEY`. **(i)** the definition of "guard-block streak" is W3-TRIAL's and is listed in §10 below. |
| **42** roles reconciliation (a)–(h) | **(a)** budget 0, repair machinery unreachable from a loaded config — held. **(b)** **applied**: the `HTTP_<status>` family, §5. **(c)** **applied**: `GATE_HELD_BY` and `settings.gates.inner_held_by`. **(d)** the coordinate is `(role, seat label, endpoint, pack sha)` plus `#repair<n>` — held. **(e)** `raw_ref` present and null until the response — held. **(f)** a transport-refused argument closes the coordinate as a blocked result, not an ended arm: `ARM_ENDING_CODES` carries four codes and no argument refusal is among them. **(g)** `thinking=False` only for the `deepseek` family — held (`ollama-cloud/deepseek` gets nothing). **(h)** the exhaustion scan is not run over delivery error strings — held; an observation is never rewritten. |
| **48** REVIEW-WAVE1 S1–S7 | **S1 applied**: `graph.APPEALABLE_RECORDS` and `_appealable` refuse an appeal whose target is not a validity node, the standard or a prior ruling; four tests, including the one that stopped the chain (an appeal on the material). **S2** held: the surface's "a region the row does not carry is absent, not empty" already gives an artifact-grain row no target region. **S3 applied**: `_resolves_uniquely` is now *exactly one start offset* (a zero-width lookahead walked twice, no tally) — it read `aa` as unique in `aaa`; and `_citation_resolves` refuses a citation whose recorded `side` is outside the new `obligations.DECLARED_SIDES`, which is G3's half. **S4** held: `validity_nodes_for_seat` is all-time by construction and `register_audit_warrant` refuses unregistered targets. **S5 applied**: the count-free guard is hardened in both `test_obligations.py` and `test_decide.py` — ordering comparisons, `statistics`/`Counter`/`collections` imports, a case-folded token scan, and a numeric exemption that covers only a constant that *is* the slice (a literal buried in a call inside a slice was exempt before). **S6** held: `test_synthetic` uses the surface API. **S7 not applicable here**: the pre-registration bundle is not in this clone, so `.gitattributes` cannot name its path; it is a publication prerequisite, §9. |
| **49** cheap notes | All applied. `seats.require_cross_family_judges` refuses a `str` (and any non-sequence) for `judge_families` — `tuple("ollama")` was six one-character families, two of them distinct. `graph._cell_index` refuses a duplicate `C_open` key instead of letting the last registration win. `graph._standing` uses `accepted[1:]` rather than `len(accepted) > 1`. `seats.key_gate_for` is documented as source-checkout-only. `RunLock.release` clears the holder record inside the flock, so a released lock no longer says "held by pid N". `obligations.production_of` / `Production` record the R5 distinction: withholding this cycle's records made the obligation *stop holding* (attribution) or *become unreadable* (an absence of evidence, never the stronger claim); `produced_by` is unchanged and delegates. |
| **50** fold-in | Applied, §5. `__init__.py` gained a wave-2 section and the two cross-wave edges. |
| **51** markprep tests must not read outside the clone | **Already held.** `REPO = Path(__file__).resolve().parents[2]` and `published_occurrences()` globs inside it; the newest present occurrence is the primary fixture. This clone carries `occurrence-01` only. |
| **52** shared cell shape | Published, §3.1. |
| **53** program finding for the C001 record | Carried, with the number this clone can verify: on **occurrence-01**, `program_marks` decides 68 kind-rows, of which **28 are G9-forced to `same`** by the within-ORIGINAL replicate spread and **2** are admissible program `differs`; register E forces nothing unresolved on this occurrence (its bare-token collisions are the occurrence-02 finding). The decision's occurrence-02 numbers (ten T/D rows all forced, zero admissible `differs`, six E rows forced by shared bare tokens) are **not** reproducible here — occurrence-02 was published after the clone was cut — and must be recomputed by the loop's first run rather than asserted by hand. The marker's own baseline for E and G must be a **second sealed artifact**, never a revision of the program's. |
| **54** cross-wave import edges | Recorded, §0, and asserted as an exact edge set plus acyclicity. |

---

## 8. The twelve hardening behaviour changes, reconciled against wave-2 callers

| # | change | wave-2 consequence |
|---|---|---|
| 1 | `loop_plan_id` requires all six `PINNED_SOURCE_PATHS`, else `PIN_INVALID` | No wave-2 module mints a plan id. `decide.MODULE_PIN_KEY` is a *seventh, run-specific* pin the driver adds, not a member of the six (28(h)). |
| 2 | two spellings of one path refused; `_relative` refuses `"."` and padded components | No wave-2 caller builds a pin map. |
| 3 | refusal codes moved (`PIN_INVALID`, `CYCLE_OUT_OF_RANGE`, `STEP_RECEIPT_INVALID`) | No wave-2 caller catches by the old codes. |
| 4 | `STANDARD_BODY_SHA256` moved to `6c894deb…`; ceiling digest unchanged | **It moved twice more in this pass** — see §9. |
| 5 | `build_standard` refuses any non-default argument; `standard_body` re-validates | No wave-2 module calls `build_standard`; `packs` reads `standard_body(registered)`. |
| 6 | `assert_config_matches_standard` gained `guard_parameters=` | Driver-side (PREFLIGHT); no wave-2 caller. |
| 7 | `custody.fenced` returns the caller's coordinate | `markprep.write_baseline` and `roles._claim` both use the documented `write_new(fenced(root, rel), value)` pairing and are unaffected. |
| 8 | `write_new` refuses `CREDENTIAL_SCAN_INCOMPLETE`, writes temp+link, new codes | `roles` writes every `call.json` through it and `markprep` every baseline: both now inherit the atomic write and the three new refusals, which are `LoopError`s and reach a caller as such. |
| 9 | `contracts.check` refuses an unknown register for every role; `SchemaInvalid.detail` composed; `assert_no_scoring_keys` refuses opaque leaves and descends dataclasses | `roles.call_marker` always passes `register=`; `packs` and `markprep` run `assert_no_scoring_keys` over plain dict records only, so the opaque-leaf refusal cannot fire on them. `markprep` calls `difference_kinds_for(register)`, which is the same closed set. |
| 10 | publish: PENDING on first push timeout; `as_receipt` gained `remote_commit`/`pending_detail`; `[ ] \` are `PATH_NOT_EXPLICIT`; three subcommands dropped | No wave-2 module publishes. Recorded for W5-DRIVER; §9 carries the `WAVE0-INTERFACE §6` supplement. |
| 11 | `publish_step` writes its COMPLETE receipt before the ledger append | Driver-side; no wave-2 caller. |
| 12 | receipts: `open_receipt` refusals, forward-only moment per ledger, four new codes folded into `FAILURE_CODES` | No wave-2 module opens a receipt. The four codes are in the table this pass extends. |

---

## 9. Dated supplement to `WAVE0-INTERFACE.md` — 2026-09-14, wave-2 integration

`WAVE0-INTERFACE.md` is a published observation and is **not edited**. What
follows supplements it.

**§5 / O3 — `receipts.py` has moved since that section was written.**
`open_receipt` now takes `create: bool = False`; `ledger_path` is
`Path | str | None` with a repository-root default; a missing ledger is
`LEDGER_NOT_FOUND` rather than an `OSError`; `assert_explicit_paths` is public.
Four codes joined `types.FAILURE_CODES` under hardening —
`LEDGER_APPEND_REENTERED`, `ACTIVITY_PATH_INVALID`, `CADENCE_THRESHOLD_INVALID`,
`CONFIG_NOT_FOUND` — and are in the table this pass extends.

**§6 — `publish.py` names three things that section omits.**
`ALLOWED_SUBCOMMANDS`, `GitSubcommandNotAllowed` and
`GIT_SUBCOMMAND_NOT_ALLOWED` are part of the public surface. The allow-list
currently holds `add, commit, diff, fetch, ls-files, ls-remote, ls-tree,
merge-base, push, rev-parse, show`; `cat-file`, `rev-list` and `status` were
dropped under hardening because nothing emits them.

**§ standard — `STANDARD_BODY_SHA256` moved twice in this pass; the ceiling did not.**

| when | value | why |
|---|---|---|
| before hardening | *(superseded)* | — |
| hardening item 41 | `6c894deb851982bf7b5e7317066896a36c4b5898308519c012a3cd1ef5100fcb` | two `plan_grounding` strings that paraphrased the plan replaced with the plan's own bytes |
| wave 2, PR-06 | `742c2a0bb239781102a063fcbeae3bbea4c9193e0f78e0310536424c52add839` | the `self-juxtaposition` calibration anchor rebuilt with the referring region alone |
| wave 2, mirror re-pin | **`a9007dc73c748cfff974a1a3d77098d380ec153b1b8cf93f513cafa3ea0572d7`** | `plan_8a_mirror.json` re-derived against the live `PLAN.md` |

`CEILING_SHA256` is unchanged at
`1e26be087483fd1b9c8e2c403cfae646fb07ebc773f23434a0c4dfab3ed04c1e`.
`decide.DECIDE_SHA256` is `e08d40adcda10e5412b945453fe09bb25030c59e9310d66b43a89cc3ffb18f29`.
**No plan was ever minted from any of these values, so nothing published moved.**

**The PLAN §8a mirror pin moved, and why.**
`src/minireason/loop/data/plan_8a_mirror.json` pinned C001's `PLAN.md` at
`601a0adc274f269f96c503e7336dc1df5e1386242569919459374f5714acadf5`. The live
file on the branch hashes to
`a27fe94a0d04bcf549a4752243e3f34a9a945697e0354d445122755ba9327235`: commit
`2d7239a` appended **§15** ("Successor occurrence-02 under driver v2"), 88 lines
added and none edited, after this clone was cut. Re-derived against the live
bytes: the live file **starts with** the clone's bytes exactly, all four register
definitions and all five mirrored §8a blocks are present byte-identically in it,
and `material.json` is unchanged at `94edfe61…`. The pin now names the live file.
A checkout that predates `2d7239a` carries the old bytes, so the digest
assertion in `test_standard.py` **skips with that reason** while the byte-identity
assertions run in both — wave-1 integration decision 51's precedent, applied to
the plan. The `loop_plan_id` demonstration value changes as a consequence; no
plan was ever minted.

**A repository-level defect, for the SRC-003 erratum — not fixed here.**
On a cold `.pyc` cache:

```
$ cp -r src $TMP/src && find $TMP -name __pycache__ -type d -exec rm -rf {} +
$ cd $TMP && PYTHONPATH=$TMP/src PYTHONDONTWRITEBYTECODE=1 \
    python3 -W error -c "import minireason.loop.contracts"
  File ".../src/minireason/use_relation_h005.py", line 301
SyntaxError: invalid escape sequence (backslash-s)
```

The offending line is `use_relation_h005.py:304`, a docstring writing a regex in
a non-raw string. Ten loop modules reach it through the import chain —
`contracts`, `standard`, `surface`, `seats`, `graph`, `synthetic`, `packs`,
`roles`, `markprep`, `decide`; `types`, `custody`, `receipts`, `obligations`,
`publish` and `steps` import clean. **`use_relation_h005.py` is a published
instrument**: editing it bumps its `source_identity` and invalidates every
frozen plan that pins it, so the repair belongs to the SRC-003 erratum and not
to this integration. Nothing in the loop package runs under `-W error`, and no
loop check depends on it; a new test,
`test_types.py::…::test_no_module_of_this_package_carries_an_invalid_escape_sequence`,
asserts that this package adds nothing to the pile. A publisher's `-W error`
gate that passes is passing on a warm cache and should be run with
`PYTHONDONTWRITEBYTECODE=1` on a cleared tree.

**Test credential literals.** Three synthetic values in `tests/loop/` that were
spelled `sk-…` are now spelled `SYNTHETIC-…-NOT-A-CREDENTIAL`: no `sk-` prefix,
no hex run, no digit run. `publish`'s scanner compares the environment's real
values and never a shape, so nothing depended on the old spelling, and a test
file carrying a key-shaped literal is a file every future credential gate has to
be told to ignore.

---

## 10. The pre-registration review items, and what the bundle reviser must do

Five REVIEW-PREREG items had a half that lives in the modules. That half is
applied here; the bundle half is listed as a consequence for its reviser.

### PR-02 — two digests of one document

**Applied.** `obligations.pin()` keeps the **file** sha256 — it is the only one
`custody.pins`/`verify_pins` can re-derive from the tree — and a new
`obligations.canonical_pin()` returns the **canonical-body** digest the bundle's
prose publishes, so neither value is anonymous. Deviation 1 of `obligations.py`
records the ruling; five tests pin it, including one showing that a whitespace
reformat moves the file digest and not the canonical one, which is exactly why
the identity carries the file digest.

**Bundle consequence.** `PREREG.md` §3 must state **both** — the canonical-body
digest `713119a7…` and the file digest that enters `loop_plan_id` — and say
which is which. Leaving one unnamed is what the review refused.

### PR-05 — `p4` was unfalsifiable on rendered files

**Applied.** `obligations.no_scoring_key` now reads two surfaces: the **keys** of
every registered record (as before) and the **headings and table header rows**
of every file named by the `rendered_files` record. The tokeniser is local —
`obligations` may not import `standard`, and the forbidden vocabulary reaches it
through the graph. The witness list names the offending file and the tokens found
in it. A table header is "the line immediately above a delimiter row", GFM's
rule, so a prose line ending in a pipe no longer hides the next table's header.
Seven tests, including the `| cell | rank |` fixture that used to pass.

**Scope, stated rather than assumed.** Only what the loop *wrote* is read. A
rendered artifact **quotes the material**, and the material is a published record
this loop may not edit: refusing a run because a quoted passage carries a
forbidden word would be the loop editing its own evidence, which is the boundary
`graph.G12_EXEMPT` draws for the same reason. `p4` is therefore falsifiable on
headings and header rows and is *declared not to scan quoted body text*.

**Bundle consequence.** `p4`'s wording may keep "every table header and every
file rendered under the run root" — that is now the program — but it should add
the quoted-material exemption in the same sentence, so the prose and the
predicate are one obligation.

### PR-06 — calibration anchor `cal-01` was unsatisfiable

**Confirmed open, then fixed here.** The B3 anchor repair had **not** landed
under hardening: `standard.CALIBRATION_ANCHORS[0].construction` still read "the
referring record and the target record are the same bytes", and a probe against
a published row with the target side set to the referring side's bytes gives
`count == 2` and `resolve_unique == None` at 20, 40, 80 and full-record windows.
The anchor is now built **with the referring region alone** — W1-SURFACE's own
rule, "a region the row does not carry is absent, not empty" — and the same
probe resolves every window uniquely, on `side = referring_record`, inside a
declared span. Five tests, including both directions of the probe.
This moved `STANDARD_BODY_SHA256` (§9); the ceiling did not move.

**Bundle consequence.** `calibration.json` cal-01 must be re-worded to the
referring-region-only construction and its `true_by_construction` clause
corrected; `cal-07` keeps the two-copy construction and its `must block` ground
truth, and the two are then no longer the same construction with opposite
declared outcomes. `VALIDATION.md`'s `calibration.json` digest moves with it.

### PR-07 — `validate.py` against the six-entry `PINNED_SOURCE_PATHS`

**Applied on the module side.** The refusal now names what a caller must supply:
`PIN_INVALID: the plan identity is fixed by 6 source pins and pins supplies no
digest for N of them: <paths>`. The old wording ("the plan identity pins […],
which pins names none of") listed them but read as though they were the ones
supplied.

**Bundle consequence.** `validate.py` must supply all six pins (the bundle's
content is sound on this point; only its harness is stale), and `VALIDATION.md`
must be regenerated **before** publication, never after — its `config.json`
digest, its `audit={…}` line and its demonstration `loop_plan_id` are all stale,
and a published observation is never modified.

### PR-12 — one owner, one spelling for block codes

**Module side: `types` is the sole owner and there is now one spelling.**
`types.BLOCK_CODES` holds the ten codes **with** the `blocked:` prefix;
`types.CEILING_BLOCK_REASONS` holds the nine **bare** reasons the frozen ceiling
prints, in the ceiling's own order; `types.block_code(reason)` is the only way to
build a member and refuses a reason the table does not carry. `surface`,
`roles` and `markprep` already built theirs that way; **`synthetic` retyped six
`"blocked:…"` literals** in `INDUCED_CODES` and `_AGGREGATE_CODES` and now builds
all six through `block_code`, so a mis-spelled reason is an error at import
rather than a closing receipt naming a code no register prints. Two new tests
pin it: no module but `types` writes the prefix in a string literal, and the two
block tables agree except for the one extra.

**Bundle consequence, both halves.** (a) `obligations.json` o1 and o2 admit
`"blocked:<code> for a code in types.BLOCK_CODES"`, which read literally admits
`blocked:blocked:schema`; they must be reworded to o4's spelling — "a
`block_code` that is a member of `types.BLOCK_CODES`". (b) The ceiling
enumerates nine bare reasons and `BLOCK_CODES` has ten:
**`blocked:constitution` has no printed home in the register the ceiling
promises**. That is the G0 non-evaluability channel FW5:688 needs kept open, so
the fix is to the *register*, not to the table: the bundle must either add the
tenth reason to the printed register or state, in the ceiling's own words, that
a constitution block is reported outside it and where. It may not be dropped
from `BLOCK_CODES`: `G0` can fire.

---

## 11. Open questions waves 3–6 must answer

1. **What is a "guard-block streak"?** Per cell, per row, or per run. `decide`
   reads `Instrument.block_streak` as a single declared integer and compares it
   with `audit.streak_max`; the *definition* is W3-TRIAL's and must be published
   in `WAVE3-INTERFACE.md`, because the three readings stop the reading arm at
   very different points.
2. **Who carries `INDETERMINATE` to a reader?** `steps.scan_coordinates` returns
   frozensets and writes nothing; the word is promised by its docstrings. W3-REPORT
   or W5-DRIVER must be the record that names a request-or-attempt-without-response.
3. **Which module owns the `rendered_files` record?** `p4` and `p12` both read it
   and nothing writes it yet. W3-REPORT is the natural writer; its shape is
   `{"record": "rendered_files", "files": {path: text}}` and `p4` now depends on
   the text being the rendered bytes, not a summary of them.
4. **Does W4-MARKER seal a second baseline for E and G?** Decision 53 says it
   must, and that it is a *second sealed artifact* and never a revision of the
   program's. The seal discipline is `markprep`'s; the second artifact is
   W4-MARKER's to design.
5. **What does the driver report on `Instrument`?** Four of its fields are facts
   no artifact carries (`custody_halted`, `arms_ended`, `block_streak`,
   `judge_err_observed`) and one is new (`preregistered_condition`). W5-DRIVER
   must state where each is read from, and W6-DOC must give every code in
   `steps`' eight halting custody codes a per-code operator action sourced from
   its raise site, not a family action.
6. **How is a pre-registered condition declared?** The clause exists; the
   *config* has no field for one, so no condition can currently fire. If the
   pre-registration declares any, `LoopConfig` needs a `preregistered_conditions`
   list and PREFLIGHT must assert the driver reports only ids from it.
7. **Does the loop run from a wheel?** `seats.key_gate_for` imports runner v2
   from `tools/`, which no wheel ships. PREFLIGHT must assert a source checkout,
   or the gate must be declared unavailable and the run refused.
8. **When the bundle lands, `.gitattributes` must gain its path with `-text`**
   (REVIEW-WAVE1 S7). The exact-set assertion in `test_standard.py` must be
   updated in the same commit.
