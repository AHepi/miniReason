> Published verbatim, body unedited: this document was written against the staging tree, so `<staging>`, "the staging root" and "the scratchpad" below name that scratchpad tree and not any path in this repository, where the files it describes are `src/deepreason_core/`, `tests/graph_core/` and `docs/sources/deepreason-core-provenance.json`.

# Vendor notes — DeepReason harness spec v1.3 P0 core

Source: **AHepi/DeepReason**, MIT, commit `9607fba6f0a3066fbcab282c9ae0fad823e52e0c`
(verified: `git rev-parse HEAD` matches and the working tree is clean).
Spec: `docs/harness-spec-v1.3.md`, sha256
`9116c8592387ce22d436cde600d77077d2b08176225f49d1c01613eb8dfb5ca8` — byte-identical
to this repository's `docs/sources/harness-spec-v1.3.md`.

Scope: **a subset of the P0 row** of spec §16 (line 566) —

> untyped schema; content=bytes+codec; event log; two-pass adjudicator; `dep`/`att`
> from interfaces (incl. case-law closure extension); Popper battery;
> isolation/integration driver stubbed w/ knobs; `why`/inspect CLI. No LLM.

Everything in that row is vendored **except the `why`/inspect CLI**, which is not
(§8). The Popper battery is vendored as a *mechanism*, not as content — see §F.

**Licence.** Upstream is MIT. `LICENSE` is copied verbatim to
`src/deepreason_core/LICENSE`; `THIRD_PARTY_NOTICES.md` at the repository root names
the source, the commit, the licence and every vendored file; and `pyproject.toml`
ships the licence inside the built package through
`[tool.setuptools.package-data]`.

Import name is `deepreason_core`; every `deepreason.` import was rewritten to
`deepreason_core.`. Each file carries a one-line header naming its upstream path,
the licence and `docs/sources/deepreason-core-provenance.json`.

Every cut below is a **deletion plus four comment/import-line rewrites**. The four
rewrite sites, with upstream line numbers at `9607fba`:

| Upstream | Vendored | Rewrite |
|---|---|---|
| `storage/objects.py` 210–219 | 46–49 | the `_SCHEMA_ID_FIELDS` comment is replaced when its four scratch/dossier rows go and the dict is left empty |
| `storage/objects.py` 236–244 | 66–68 | `_object_data`'s comment is replaced when the `exclude_none` branch goes |
| `harness.py` 183–186 | ~144 | the `_reset` derived-caches comment loses its three-line capture-detection anecdote, which describes a subsystem this vendoring cuts |
| `harness.py` 2201 | ~539–543 | `conn_map(dep, self.state.status)` becomes the zero map under a four-line comment saying why (§D) |

Everything else is a deletion. That includes five import statements that lose a
*name* while the statement is retained — `ontology/event.py` 10–11 and 13,
`harness.py` 10–11, 34 and 69–70 — and `register_batch`'s `*extra_inputs` splice
(`harness.py` 537). Two **additions** are documented separately and are not cuts,
so a normalised diff shows them too: the 33 inlined transcript lines in `harness.py`
(vendored 56–88, §6), and the optional deterministic `clock` constructor parameter,
which adds the parameter and its comment (upstream 88 and 97), rewrites the `ts=`
expression at upstream 2031, and adds `Callable` to the `collections.abc` import at
upstream line 10 — the one place where an import line gains a name instead of
losing one.

Reproduce the claim: for each file, strip the vendored header line, apply
`s/deepreason_core\./deepreason./`, and diff against the upstream file. Every
`insert`/`replace` hunk is one of the four rows above or one of the two named
additions; every other hunk is a `delete`.

Line numbers below are upstream line numbers at `9607fba`.

---

## 1. `src/deepreason/storage/objects.py` → `storage/objects.py` (409 → 234 lines)

| Deleted | What | Why |
|---|---|---|
| 14–47, 49, 54–102 | imports of `capabilities.models`, `bridge.{evidence_pack,ledger,models,retry}`, `evidence.models`, `scratch.models`, `workflow.{models,transaction,criticism}` | the model packages behind the registry rows below; none exists in P0 |
| 128–207 | ~75 `SCHEMAS` rows (`scratch-*`, `bridge-*`, `workflow-*`, `criticism-*`, `capability-*`, `dossier-pack-receipt`) | dead registry rows: no P0 code path can `put` or `get` any of them |
| 210–219 | the four `_SCHEMA_ID_FIELDS` entries and the comment explaining them | all four name schemas deleted above |
| 239–243 | the `exclude_none=schema.startswith(("scratch-","bridge-","workflow-","capability-"))` branch of `_object_data` | unreachable once those prefixes are gone; every remaining schema is formal and keeps its exact established byte representation |

`SCHEMAS` now holds exactly the four P0 records of spec §1 — `artifact`, `commitment`,
`warrant`, `problem`. `_SCHEMA_ID_FIELDS` is retained as an **empty dict** rather than
removed, so `_object_id`'s indirection and its two error messages stay upstream-identical
and a future row can be added without re-deriving the mechanism.

Restores: spec §1 "one schema" and §14 namespaced object storage, with no schema the
spec does not define.

## 2. `src/deepreason/ontology/event.py` → `ontology/event.py` (616 → 105 lines)

| Deleted | What | Why |
|---|---|---|
| 10, 11 (`Literal`), 13 (`model_validator`) | imports left unused by the deletions below | `re` and `Literal` were used only by `ConjectureContextCallReceiptV1` |
| 15–23, 25–26 | imports of `BridgeEventPayloadV1`, `CapabilityEventPayloadV1`, `ConjectureTurnEventPayloadV1`, `ControlEventPayloadV1/V2/V3`, `ModuleFingerprintsEventPayloadV1`, `ScratchEventPayloadV1`, `SeatBindingsEventPayloadV1` | the seven typed payloads, all v1.4+ |
| 40–44 | `Rule` members `Scratch`, `Bridge`, `ConjectureTurn`, `Control`, `Capability` | spec §1 fixes the rule alphabet at ten: `Conj\|Crit\|Adj\|Spawn\|Refl\|Register\|Merge\|Measure\|Reveal\|Reseed` |
| 47–286 | `LLMSplitLegV1`, `LLMAttempt`, `SchoolRouteReceiptV1`, `ConjectureContextCallReceiptV1` | split-budget seat protocol, repair ladder, v4 school routing and advisory-scratch receipts — none is in v1.3 |
| 297–387 | `LLMCall` fields `attempts`, `truncated`, `mean_surprisal`, `attempt_trace`, `school_route`, `conjecture_context`, `work_order_id`, `dispatch_authorization_ref`, `prompt_tokens`, `completion_tokens`, plus `_freeze_attempt_trace` and `_school_route_matches_attempts` | spec §1 line 148 fixes `llm` as the flat seven-key object `{role, model, endpoint, prompt_ref, raw_ref, tokens, ms}`. The remaining fields are §11.3 capture diagnostics, P6 valid-JSON accounting, and workflow authority |
| 434–457 | the seven optional typed payload fields on `Event` | same |
| 475–503 | `_deeply_revalidate_control_payload`, `_deeply_revalidate_capability_payload` | validate fields that no longer exist |
| 509–616 | `_process_payload_contract` | its entire body is rule↔payload coupling for the five deleted `Rule` members plus the two Measure-riding identity payloads |

**This cut is byte-neutral only for llm-free events.** Six of the ten deleted
`LLMCall` fields carry `exclude_if=lambda value: value is None`, so they never
reached the JSONL of an upstream event that left them unset — but `attempts`
(default `1`), `truncated` (default `False`), `mean_surprisal` (default `None`)
and `attempt_trace` (default `[]`) do **not**: upstream serialises all four
unconditionally on every `LLMCall`. An upstream event that carries an `llm`
record therefore writes four keys this vendored `Event` does not, and its bytes
differ. `Event.llm` itself is `LLMCall | None = None` with no `exclude_if` in
both trees, so `"llm":null` is written either way and every event *without* an
LLM call — which, P0 having no LLM at all, is every event this package can
produce — is byte-identical to upstream. Reading an upstream root that contains
llm-bearing events is a separate question: the extra keys are ignored on parse,
but re-serialising such an event here would not reproduce its original bytes.

Restores: spec §1's Event object exactly — `seq`, `ts`, `rule`, `inputs`, `outputs`,
`llm`, `state_diff` — and §1's ten-rule alphabet.

**Kept deliberately:** `Event._deeply_revalidate_llm_call` (459–473). Its docstring cites
the work-order validator, which this vendoring cuts, so the guard is now defensive rather
than load-bearing. Keeping it is the minimal-deletion choice: it still round-trips a
preconstructed `LLMCall` through validation and costs nothing.

## 3. `src/deepreason/ontology/__init__.py` → `ontology/__init__.py` (56 → 39 lines)

Deleted the payload re-exports: imports at 9 and 10–14 (`ConjectureTurnEventPayloadV1`,
`ControlEventPayloadV1/V2/V3`), the names `ConjectureContextCallReceiptV1` (17),
`LLMAttempt` (19), `LLMSplitLegV1` (20) and `SchoolRouteReceiptV1` (23) from the
`ontology.event` import, and the eight corresponding `__all__` rows (34–38, 43, 44, 50).

## 4. Ontology enums and state

**`ontology/artifact.py`** (106 → 97): deleted 51–60, the `CONTROLLER` and `EXPERIMENTER`
members of `ProvenanceRole` (self-calibration controller, experiment-design generators).
Neither string appears anywhere in v1.3. `ProvenanceRole` is now the seven v1.3 members:
`conjecturer, critic, variator, synthesizer, seed, import, user`.

**`ontology/problem.py`** (69 → 64): deleted 39–44, the `PROMOTION` member and its §9.4
comment. v1.3 §9 is the LLM adapter and has no §9.4; "promotion", "frame assertion" and
"Def 9.2" appear nowhere in the spec.

> **`SpawnTrigger` is a deliberate minimal superset — and nine is not the v1.3 count.**
> The vendored enum is **the eight v1.3 §1:125 members plus `research`, a deliberate
> minimal superset required to represent the research-problem Spawn that §12 mandates
> but §1's enum omits.** The eight are the ones §1 line 125 actually writes out:
> `seed|successor|discrimination|remove-arbitrariness|explanation-debt|audit-critic|
> connection|integration`. The ninth, `research`, appears nowhere in that enum; it is
> required because §12 (spec line 486) mandates the Spawn it names — "`observation_valued`
> commitment with no covering evidence artifact ⇒ Spawn research problem" — restated at
> §1 line 91. Dropping it would make a spec-mandated Spawn unrepresentable, so `RESEARCH`
> is kept and marked here as this vendoring's own addition rather than as v1.3 content.
>
> **Retracted.** An earlier draft of these notes carried a paragraph headed "Correction
> to the pre-analysis" which said the brief's count of **8** was wrong and that
> "re-reading the spec gives **9**". That is withdrawn: the brief's 8 was right for
> v1.3, and the 9th member is an addition, not a reading of the spec. `PROMOTION` was
> cut because no section of v1.3 mandates it at all.

**`ontology/state.py`** (71 → 39): deleted 41–71, `is_import_admission` and
`counts_as_survivor`. Both are evidence-admission survivor bookkeeping for auto-accepted
import-role records — a v1.4+ concept; nothing in the P0 closure calls either.

## 5. `src/deepreason/adjudication/edges.py` → `adjudication/edges.py` (189 → 171 lines)

Deleted the **source-artifact closure**: its docstring clause (16–23) and its body
(171–180). It lifts attackers of a `budget.extra["source_artifact"]` onto the ν of every
warrant under that commitment — accountability for LLM-*proposed* property checkers, which
P0 cannot produce (P0 has no LLM at all).

Kept intact and exercised by the suite: the validity-node closure, the case-law (standard)
closure extension, the evidence closure, and the fixpoint loop that composes them.
Restores spec §1/§2: "the validity-node closure (including case-law and evidence
extensions) holds".

## 6. `src/deepreason/harness.py` → `harness.py` (2201 upstream lines → the P0 slice below, plus 33 inserted lines)

Kept only the P0 slice: upstream **~1–133, 155–208, 353–578 and 1979–2201** (measured by
normalised diff against upstream, not estimated — an earlier draft of these notes said
155–**209** and **358**–578, which overstated the kept region at both boundaries: upstream
208 is the last line of `_ensure_writable`, and 353 is the blank line before the
registration banner). Everything in the gaps — **209–352** authority reload and workflow
checkpointing; 579–1978 measures, capture detection, scratch/bridge/workflow/capability
surfaces, semantic clock, transcript shadow — is P1–P6 machinery outside the P0 row.

On top of that slice the file carries **33 inserted lines** (vendored 56–88): the banner
and the two `informal/trial.py` helpers inlined below ("Inlined, not imported"). The
optional deterministic `clock` constructor parameter is a second, separately recorded
insertion. Inside the kept ranges:

| Deleted | What | Why |
|---|---|---|
| 27–33, 35–43, 45, 49, 61–63 | imports of `bridge.{events,state}`, `capabilities.{events,state}`, `control_events`, `conjecture_turn`, `module_events`, `ConjectureTurnEventPayloadV1`, `scratch.{events,models,state}` | v1.4+ subsystems |
| 10 (`Mapping`), 11, 14, 17, 69 (`SCHEMAS`), 70 | `Mapping`, `bisect_left`, `os`, `BaseModel`, `SCHEMAS`, `unification.isolation.conn_map` | left unused by the deletions (verified: the vendored tree has zero unused imports). `json` (13) is kept — the inlined `conforming_transcript` uses it |
| 103, 113–120, 122–123, 134–154 | `_load_workflow_manifest`, the terminal-commitment storage validation, `_verify_workflow_checkpoint`, `bind_transaction_manifest` | RunManifest/terminal-authority, v1.4+ |
| 157–178 | `scratch_state`, `bridge_state`, `workflow_state`, `capability_state` in `_reset` | same |
| 188–198 | `_trans_shadow`, `_trans_out`, `_embed_cache`, `_verdict_cache`, `_semantic_*`, `_oracle_pending` | §11 capture-control and oracle caches (P2+). `_tail` (187) is kept — `_commit` writes through it; 183–186 is the comment rewrite listed in the preamble, not a deletion |
| 447, 532–534, 537 | the `process_inputs` parameter of `register_batch`, its validation, and its splice into `Event.inputs` | process-event plumbing for the deleted payload rules |
| 1994 | `from deepreason.informal.trial import conforming_transcript` | `informal/` (§10, P5) is not vendored — see below |
| 2018–2026, 2038–2044 | the seven typed payload parameters of `_commit` and their `Event(...)` kwargs | the fields no longer exist on `Event` |
| 2070–2114 | in `_apply_event`: `workflow_state.observe_event`, the `control`/`capability` object-resolution loops, `scratch_state.apply`, `bridge_state.apply` | same |
| 2162 | `self._advance_semantic_event_clock(event)` | §11 semantic-age bookkeeping keyed on `Rule.CONTROL` and split-call carriers |
| 2201 | `self.state.conn = conn_map(dep, self.state.status)` | replaced by the zero map — see below |

**Inlined, not imported.** `conforming_transcript` and `transcript_blob` (upstream
`informal/trial.py` ~295–322) are copied verbatim into `harness.py` as module-level
functions. They are the §2/§3 rubric-verdict guard that `_validate_warrant` calls, and they
are the only thing the P0 closure needs from `informal/`. Tests import `transcript_blob`
from `deepreason_core.harness`.

**Isolation stubbed.** `unification/isolation.py` is not vendored. `_adjudicate` sets
`state.conn` to the zero map with a comment, per the P0 row's "isolation/integration driver
stubbed w/ knobs". This is safe by construction: adjudication's only inputs are `att` and
`dep` (§0, §4), so `conn` could never have reached a label.

**`Rule.REVEAL` kept.** `Reveal` is one of the ten v1.3 rule names, and the read-only
holdout fence (`FencedBlobStore`, `historical_sealed_refs` in `storage/blobs.py`) is what
makes a time-travel view physically read-only (§1). Both are vendored verbatim.

## 7. Vendored verbatim (header comment and `deepreason.` → `deepreason_core.` only)

`__init__.py`, `canonical.py`, `frozen.py`, `ontology/frozen.py`, `ontology/commitment.py`,
`ontology/warrant.py`, `adjudication/__init__.py`, `adjudication/grounded.py`,
`adjudication/support.py`, `log/__init__.py`, `log/event_log.py`, `storage/__init__.py`,
`storage/blobs.py`.

`src/deepreason/__init__.py` was not in the brief's vendor set but is required for
`deepreason_core` to be a package; it is 10 lines of docstring and `__version__` with no
imports.

## 8. Not vendored

| Upstream | Why |
|---|---|
| `storage/merge.py` | P3, outside the P0 row — and **it cannot be vendored verbatim**: it reads `Rule.CONTROL` (line 78) and `event.llm.work_order_id` (line 84), both cut here. Vendoring it would have meant rewriting logic, which this vendoring does not do. The single test assertion that used it was dropped instead (see below). |
| `unification/isolation.py` | §7 driver; P0 stubs it. |
| `informal/trial.py` | §10 (P5). Two functions inlined; the rest is the trial/judge protocol. |
| `invariants.py` | Not reachable from the P0 closure. |
| `src/deepreason/cli/` (`main.py`, `doctor.py`, `bridge.py`, `scratch.py`) | **The `why`/inspect CLI named in the P0 row.** Not vendored, which is why the scope line above says *a subset of* the P0 row. Three reasons: `cli/main.py` is a single dispatcher over the whole upstream surface (bridge, scratch, workflow, capability subcommands) and cannot be taken verbatim once those subsystems are cut; `cli/bridge.py` and `cli/scratch.py` are v1.4+ outright; and the repository has its own entry points (`pyproject.toml` declares `minireason`), so a second console script would be a new public surface, not a vendored one. Everything the `why` view reads — `state.status`, `state.att`, `state.dep`, `EventLog.read`, `Harness.at` — is vendored, so the view can be written here against the vendored API without copying the dispatcher. |

---

## Tests

They live in **`tests/graph_core/`**, not `tests/deepreason_core/` — see §A.

Converted from pytest to `unittest.TestCase`, preserving every assertion's meaning.
`tests/conftest.py` became `tests/graph_core/helpers.py`: the `harness` fixture is
`HarnessTestCase`, `tmp_path` is `TempDirTestCase` (`tempfile.mkdtemp` + `addCleanup`), and
`art()`/`attack()` are verbatim. `pytest.raises(X, match=…)` → `assertRaisesRegex`,
`pytest.warns` → `assertWarnsRegex`, `monkeypatch.setattr` → `unittest.mock.patch.object`,
`@pytest.mark.parametrize` → two named methods. The five cross-module helper imports are
**relative** (`from .helpers import …`), so the package loads identically whether discovery
imports it as `graph_core.*` (`unittest discover -s tests`) or as `tests.graph_core.*`
(running a module by its dotted name).

| Module | Tests | Changes beyond the mechanical conversion |
|---|---|---|
| `test_adjudication.py` | 11 | `transcript_blob` imported from `deepreason_core.harness` instead of `deepreason.informal.trial`. |
| `test_ontology.py` | 7 | none |
| `test_persistence_invariants.py` | 10 | two deletions, below |
| `test_torn_append.py` | 3 | none |
| `test_blob_store_long_paths.py` | 2 | none |
| `test_p0_acceptance.py` | 8 | **new** |
| `test_closures_and_fences.py` | 9 | **new** |
| `golden_build.py` | — | **new**, and not a test module: the standalone builder the byte-identity golden runs in a second interpreter |

**50 tests in all.**

**Two deletions in `test_persistence_invariants.py`** (upstream had 10 functions / 11 tests;
9 functions / 10 tests remain):

1. `test_replay_verification_does_not_repair_a_torn_tail` (170–181) is deleted whole. Its
   only assertion is that `deepreason.invariants.verify_root` does not repair a torn tail,
   and `invariants.py` is not in the vendor set. The property it guards — read-only replay
   never repairs a torn tail — is still covered by
   `test_time_travel_does_not_create_or_repair_storage`, which asserts the same bytes-unchanged
   outcome through `Harness.at`.
2. The `merge(past, root)` read-only assertion inside
   `test_time_travel_harness_rejects_every_write_and_changes_no_bytes` (147–148) is deleted,
   because `storage/merge.py` is not vendored. The other five read-only assertions in that
   test are unchanged.

**New `test_p0_acceptance.py`** (8 tests) states each of the six spec §16 P0 acceptance
items as a named test (`test_p0_item_1_grounded_extension_correctness` …
`test_p0_item_6_replay_from_log_reproduces_state_byte_for_byte`), reusing the vendored
scenarios, plus two determinism tests:

- `test_two_interpreters_build_byte_identical_roots` is the golden. The first root is built
  in this process; the **second root is built by a separate interpreter**, launched as
  `python -m tests.graph_core.golden_build <root>` with a **different `PYTHONHASHSEED`**,
  and the comparison is made from the parent — `log.jsonl` bytes, then the sorted
  `(relative path, sha256)` maps of `objects/` and of `blobs/`, then every file in the root,
  then that both roots replay to the same state. Before any equality it asserts
  non-emptiness and the expected shape on both sides (9 events, 6 artifacts, 10 objects,
  1 blob), so two empty or truncated trees cannot pass by agreeing about nothing; it also
  asserts the child's pid and hash seed really differ from the parent's. An in-process
  "second build" cannot catch a hash-seed-dependent iteration order leaking into the written
  bytes, because it reuses one interpreter's seed — that is the failure mode this test
  exists for, and the reason the first draft's same-process golden was not enough.
- `test_two_in_process_builds_replay_alike` keeps the original in-process check, so a
  failure of the cross-process golden localises to seed dependence rather than to the
  construction itself.

Both builds take the same frozen clock (`golden_build.frozen_clock()` pins `Event.ts`, the
only nondeterministic input to the log); everything else — ids, object bytes, edge sets — is
content-addressed or sorted and is left alone. `golden_build.py` imports `deepreason_core`
and the standard library only, never `unittest` or `helpers`, which is what lets it be
launched as a plain second process.

**New `test_closures_and_fences.py`** (9 tests) pins five properties the vendored core
claims but the converted suite did not exercise:

- the **evidence closure** (spec §1 lines 109-114) — the third of the three closures §5
  calls "kept intact and exercised by the suite", which nothing exercised. Registering
  evidence `E`, a ν carrying `Ref(target=E, role="evidence")`, and a warrant under that ν
  against `T` carried by critic `C` refutes `T`; attacking `E` from an unattacked artifact
  then refutes the ν, drops `C`, and reinstates `T` — with `(x → ν)` and `(x → C)` asserted
  in `state.att`, because the spec makes this an attack-graph derivation, never a hidden
  status check. A second test attacks an artifact in the evidence's transitive **dependence
  lineage** instead;
- the **trial guard** (§2/§3): a rubric-derived demonstrative warrant is refused with
  `WellFormednessError` in both branches of the guard — no `trace_ref` at all, and a
  `trace_ref` whose blob is well-formed JSON but not a conforming transcript — with the log
  bytes unchanged and no edge landing. A positive control registers the same warrant with a
  conforming transcript, so the guard is shown to refuse content rather than rubric warrants;
- the **time-travel fence**: opening `Harness.at(root, seq)` at every seq leaves the tree
  listing — files *and* directories — identical, and creates nothing whatever for a root
  with no storage yet; and a blob with an unrevealed `holdout/` marker is refused by the
  view's `FencedBlobStore` (`is_grounding_available` false, `get` raises) while the live
  store still serves it, becoming readable only at a fence after its `Reveal`;
- **explicit carriage**: `register_batch` carrying an already-registered warrant on a second
  artifact, without re-providing the warrant record, records the pair in the event's
  `carry_add`, materialises it in `state.carries`, produces the attack edge, and survives
  replay — the property that lets identical criticism prose attack twice without changing
  its content-addressed id;
- **`state.conn`**: every artifact mapped, every value 0, field still serialized (§D).

---

## Things that could not be cut cleanly — read these

### A. The test package is `tests/graph_core/`, and that is load-bearing

`python -m unittest discover -s tests` makes `tests/` the discovery **top-level directory**
and inserts it at `sys.path[0]` (`unittest/loader.py`, `TestLoader.discover`; there is no
walk-up to the repository root). A directory named `tests/deepreason_core/` therefore
imports under the top-level name `deepreason_core` and **shadows the vendored package it
tests**, so every `from deepreason_core.harness import …` in the suite fails with
`ModuleNotFoundError`. The repository's own gate (`.github/workflows/tests.yml`) runs
exactly that command, so this was a red CI, not a cosmetic issue.

**Resolution shipped: the directory is named `tests/graph_core/`** — a name that is not
also an importable package here — and its `__init__.py` is a plain one-line docstring. The
five cross-module helper imports are relative (`from .helpers import …`), so nothing in the
suite depends on the package's absolute dotted name, and the identical 50 tests pass under
both spellings (see the verification log at the end).

An earlier pass kept the name `tests/deepreason_core/` and defended it with a
`load_tests(loader, standard_tests, pattern)` hook in the package `__init__.py`: it dropped
the shadowing `sys.modules` entry, removed the `tests/` `sys.path` entry, loaded the six
modules under their true dotted names, and restored `sys.path` in a `finally` so the sibling
packages discovered afterwards still saw `tests/` as top level. **That hook is deleted.** It
worked, but it made correct discovery depend on a thirty-line manipulation of the import
system that runs before any test, that no other package in this repository needs, and whose
failure mode is a silently partial suite rather than an error. Renaming removes the shadow
instead of routing around it.

### B. Stale upstream comment kept verbatim

`ontology/problem.py`'s `SUCCESSOR` member carries a long upstream comment citing
`successor/mint.py`, `scan_spawns`, `easy.py::seed_component` and
`tests/test_decommissioned_pipeline_stays_out.py` — none of which is vendored. It records an
operator ruling about *where* successor problems may be minted, which is design rationale
the brief asked to preserve, so it was kept rather than trimmed. Read it as upstream history,
not as a description of this package.

### C. pydantic: upstream declares `>=2.7`, and so do we

Upstream `pyproject.toml` at `9607fba` declares **`pydantic>=2.7`**. This repository
declares the same floor, **`pydantic>=2.7`**, in `[project] dependencies` — the only
dependency the vendoring adds.

Two other numbers were in circulation and both were wrong for this tree. `>=2.11` (what the
vendoring brief pinned) is the floor for `Field(exclude_if=…)` — but every `exclude_if` in
the vendor set sits inside code this vendoring **cuts** (the seven `Event` payload fields,
the extra `LLMCall` fields, `ConjectureContextCallReceiptV1`), so nothing here needs it, and
declaring a floor *above* upstream's would have been a restriction with no cause.
`>=2.0` is the bare API floor of the surviving code (`BaseModel`, `ConfigDict(frozen=True)`,
`field_validator`, `model_validate_json`, `model_dump(mode="json", by_alias=True)`) but sits
below what upstream itself supports and is not tested, so declaring it would be an unchecked
claim.

Tested at **pydantic 2.13.5** and at **pydantic 2.7.4** (the newest 2.7.x), both on CPython
3.11.15, in a clean virtualenv: 50 tests, OK, on both. The declared floor is exercised in
CI by a third matrix leg in `.github/workflows/tests.yml` (python 3.12) that runs
`python -m pip install "pydantic==2.7.*"` after the editable install and before the suite,
so the floor is a tested claim and not an assertion. The base legs (3.11, 3.12) still
resolve pydantic freely, so both ends of the supported range are covered.

### D. `state.conn` is a zero map, not an absent field

`EpistemicState.conn` is kept in the schema (spec §1 Def 3.3 lists it in
`S = (A, Π, carry, att, dep, addr, status, hv, reach, conn)`) and is **computed as zero and
persisted into every materialized state**: `_adjudicate` ends with
`self.state.conn = {aid: 0 for aid in self.state.artifacts}`, so every artifact has an
entry, every entry is `0`, and the key is present in every serialization. It is not an
absent field, not an empty dict, and not a partial map — saying it is merely "uncomputed"
understates what is written to disk. Removing the field would have changed the serialized
state shape; filling it with zeros matches the P0 row's "isolation/integration driver
stubbed w/ knobs". Nothing in P0 reads it, and adjudication never could: its only inputs
are `att` and `dep` (§0, §4). Pinned by
`test_closures_and_fences.py::ConnZeroMapTests`.

### E. `Budget.extra` still accepts a `source_artifact` key

Cut 5 removes the closure that *consumes* `budget.extra["source_artifact"]`, but
`Budget.extra` is a generic `Mapping[str, int | str]` and needed no change. A commitment
carrying that key is simply inert here.

### F. The Popper battery is a mechanism here, not a battery

`POPPER_BATTERY` is **an empty tuple upstream at `9607fba`**: the pinning mechanism is
implemented, the battery is not populated. `register_problem` runs the auto-pinning spec §1
requires — every problem's `criteria` gains the battery's commitment-schema ids at
registration, before id computation — and pins nothing, because there is nothing to pin;
upstream's own comment says the contents "land with P1/P2". The vendored file is verbatim,
empty tuple included. So "Popper battery" in the P0 scope line above is satisfied
*structurally*: a reader expecting demarcation checks to actually run should read it as a
no-op until the battery is populated.

---

## Verification log

Python: CPython 3.11.15. Every command below was run for this revision; the
`<staging>` root is the staged vendor tree, and the overlay copies were deleted
afterwards.

**Staged tree** (`PYTHONPATH=src`, from the staging root):

```
python -X utf8 -m unittest discover -s tests -v   ->  Ran 50 tests, OK      (pydantic 2.13.5)
python -X utf8 -m unittest discover -s tests      ->  Ran 50 tests, OK      (pydantic 2.7.4)
```

The 2.7.4 run used a clean virtualenv holding only pydantic 2.7.4, pydantic-core
2.18.4, annotated-types 0.8.0 and typing-extensions 4.16.0 — the declared floor,
actually installed. See §C.

**Overlay** — a throwaway copy of the repository with the staged
`src/deepreason_core` and `tests/graph_core` laid over it:

```
with .git:            python -X utf8 -m unittest discover -s tests
                      ->  Ran 747 tests in 83.317s, OK (skipped=1)
same copy, overlay removed (baseline):
                      ->  Ran 697 tests in 79.484s, OK (skipped=1)
                      747 = 697 baseline + 50 vendored.

with .git:            python -X utf8 -m unittest tests.graph_core.test_adjudication -v
                      ->  Ran 11 tests, OK

tar --exclude=.git:   python -X utf8 -m unittest discover -s tests
                      ->  Ran 747 tests in 75.270s, FAILED (errors=11, skipped=1)
```

The 11 errors in the last run are **pre-existing and not ours**: a copy made
without `.git` breaks the tests that shell out to `git -C <repo> rev-parse HEAD`
(`tools/luna_routing_probe.py` and friends). None is in `tests/graph_core`, and the
same `.git`-less copy runs the vendored package clean —
`python -X utf8 -m unittest discover -s tests/graph_core -t .` → Ran 50 tests, OK —
while the copy *with* `.git` is green end to end. That is why the two overlay rows
above are both recorded.

**Bytecode hygiene.** No `__pycache__` directory or `.pyc` file is shipped. The
staging tree was stripped with:

```
find <staging> -name '__pycache__' -type d -prune -exec rm -rf {} +
find <staging> -name '*.pyc' -delete
```

Every test run above sets `PYTHONDONTWRITEBYTECODE=1` (as
`.github/workflows/tests.yml` already does in `env:`), so the strip is a belt-and-
braces measure rather than the only defence.
