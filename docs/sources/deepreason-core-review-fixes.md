> Published verbatim, body unedited: this document was written against the staging tree, so `<staging>`, "the staging root" and "the scratchpad" below name that scratchpad tree and not any path in this repository, where the files it describes are `src/deepreason_core/`, `tests/graph_core/` and `docs/sources/deepreason-core-provenance.json`.

# Review fixes applied to the staged vendored core

Staging tree only. `/home/user/miniReason` and the upstream clone
`/home/user/ahepi/deepreason` were not modified; no provider call was made.

`src/deepreason_core/harness.py` was **not touched** by this pass — a parallel
change is adding an optional `clock` constructor parameter to it — and its
`destination_sha256` in `provenance.json` is left exactly as it was. A top-level
`note` in `provenance.json` records that the publisher re-hashes every destination
after final assembly.

---

## 1. Test package renamed; the import shadow is gone

- `tests/deepreason_core/` → **`tests/graph_core/`**.
- The five helper imports (`from tests.deepreason_core.helpers import …` in
  `test_adjudication`, `test_blob_store_long_paths`, `test_p0_acceptance`,
  `test_persistence_invariants`, `test_torn_append`) are now **relative**:
  `from .helpers import …`. The package therefore loads identically whether
  discovery imports it as `graph_core.*` or as `tests.graph_core.*`.
- The `load_tests` hook is **deleted**. `tests/graph_core/__init__.py` is now a
  plain one-line docstring.
- `VENDOR_NOTES.md` §A is rewritten: it still explains the shadow (it is a real
  property of `unittest discover -s tests`), but records the rename as the shipped
  resolution and says why the hook was the wrong answer.

Verified in a throwaway overlay (`tar --exclude=.git` of the repository plus the
staged `src/deepreason_core` and `tests/graph_core`), deleted afterwards:

```
with .git     discover -s tests                     ->  Ran 747 tests in 83.317s, OK (skipped=1)
with .git     tests.graph_core.test_adjudication -v ->  Ran 11 tests, OK
no .git       discover -s tests                     ->  Ran 747 tests in 75.270s, FAILED (errors=11, skipped=1)
no .git       discover -s tests/graph_core -t .     ->  Ran 50 tests, OK
baseline (same copy, overlay removed)               ->  Ran 697 tests in 79.484s, OK (skipped=1)
```

747 = the repository's 697 baseline + the 50 vendored tests. The 11 errors in the
`.git`-less copy are pre-existing: those tests shell out to
`git -C <repo> rev-parse HEAD`. None is in `tests/graph_core`.

## 2. Packaging: declared floor, licence data, and a CI leg that exercises the floor

- **`pyproject.toml`** staged as a full modified copy of the repository's own:
  `dependencies = ["jsonschema==4.25.1", "referencing==0.37.0", "pydantic>=2.7"]`,
  and `[tool.setuptools.package-data]` gains `deepreason_core = ["LICENSE"]`.
  `>=2.7` is upstream DeepReason's own declared floor — confirmed by reading
  `/home/user/ahepi/deepreason/pyproject.toml`, whose `[project] dependencies`
  reads `"pydantic>=2.7"`.
- **`.github/workflows/tests.yml`** staged as a full modified copy with one extra
  matrix leg. The base matrix gains `pydantic-floor: [false]` and an `include:`
  entry `{python-version: '3.12', pydantic-floor: true}`, which (because it
  overrides an original matrix value) creates a **third job** rather than editing
  the existing 3.12 one. That job runs
  `python -m pip install "pydantic==2.7.*"` after `pip install -e .` and before the
  suite. SHA-pinned actions, `permissions: {}` at workflow level and
  `contents: read` at job level are unchanged; the pin is a literal string, not an
  interpolation into `run:`.
- **Verified locally.** A clean virtualenv under the scratchpad with
  `pip install "pydantic==2.7.*"` resolved **pydantic 2.7.4** (pydantic-core
  2.18.4, annotated-types 0.8.0, typing-extensions 4.16.0) on CPython 3.11.15, and
  the staged suite passes on it: `Ran 50 tests, OK`. 2.7 is therefore the real
  minimum and no higher floor was needed.

## 3. Licence

- `/home/user/ahepi/deepreason/LICENSE` copied **verbatim** to
  `src/deepreason_core/LICENSE` (sha256
  `772e479a9cf08762785c6d99da14d5266cafaff751a40cf097e52f9216874e86`, identical on
  both sides).
- **`THIRD_PARTY_NOTICES.md`** created (for the repository root): names
  AHepi/DeepReason, commit `9607fba6f0a3066fbcab282c9ae0fad823e52e0c`, MIT and the
  copyright line, every vendored library and test file with its upstream path,
  the spec file, which files are original to this repository, and points at
  `docs/sources/deepreason-core-provenance.json`. The full MIT text is included.
- Every vendored file header extended to
  `# Vendored from AHepi/DeepReason@9607fba <upstream path> (MIT, see src/deepreason_core/LICENSE); see docs/sources/deepreason-core-provenance.json`
  — **except `harness.py`**, left at its first-pass header for the publisher to
  finish after the parallel clock change lands. `provenance.json` records that
  explicitly in `harness.py`'s `header_rewritten` field.
- `provenance.json` gains a `license_file` block (source, destination, both
  digests, SPDX, copyright, how it is packaged, where the notices live).

## 4. `SpawnTrigger`: `RESEARCH` kept, the documentation corrected

`RESEARCH` is kept. What changed is the claim made about it.

- `VENDOR_NOTES.md` §4 now says the enum is **"the eight v1.3 §1:125 members plus
  `research`, a deliberate minimal superset required to represent the
  research-problem Spawn that §12 mandates but §1's enum omits"**, cites §12 (spec
  line 486) and §1 line 91, and states plainly that **nine is not the v1.3 count**.
- The paragraph headed *"Correction to the pre-analysis"*, which said the brief's
  count of 8 was wrong and that re-reading the spec "gives 9", is **retracted in
  place** — the retraction is written into the notes, not silently deleted.
- `provenance.json`'s `cut_summary` for `ontology/problem.py` carries the same
  wording.

## 5. Golden test: two interpreters, two hash seeds

`test_two_independent_builds_are_byte_identical_and_replay_alike` built both roots
in one process, so a hash-seed-dependent iteration order leaking into the written
bytes would have agreed with itself. Replaced by
**`test_two_interpreters_build_byte_identical_roots`**:

- the reference builder moved to **`tests/graph_core/golden_build.py`**, a module
  that imports `deepreason_core` and the standard library only (never `unittest` or
  `helpers`) so it can be launched as a plain second process;
- the second root is built by `python -m tests.graph_core.golden_build <root>` in a
  **separate interpreter** with a **different `PYTHONHASHSEED`** (the child's seed
  is chosen to differ from the parent's; the test asserts the child's pid and
  reported seed really differ);
- **both builds take the same frozen clock** — `golden_build.frozen_clock()`, moved
  out of `helpers.py`, patches the module-level `datetime` the harness stamps
  `Event.ts` with, so it holds regardless of the parallel `clock` parameter;
- the parent compares `log.jsonl` bytes, then the sorted `(relative path, sha256)`
  maps of `objects/` and of `blobs/`, then every file in the root, then that both
  roots replay to the same state;
- **before any equality**, non-emptiness and shape are asserted on both sides —
  9 events, 6 artifacts, 10 objects, 1 blob — so two empty or truncated trees
  cannot pass by agreeing about nothing.

The in-process replay test is **kept** as
`test_two_in_process_builds_replay_alike`, so a cross-process failure localises to
seed dependence rather than to the construction.

## 6. New tests — `tests/graph_core/test_closures_and_fences.py` (9 tests)

- **Evidence closure** (spec §1 lines 109-114): evidence `E`, a ν carrying
  `Ref(target=E, role="evidence")`, a warrant under ν against `T` carried by critic
  `C` ⇒ `T` refuted; then `E` is attacked by a new warrant/ν from an unattacked
  artifact ⇒ ν refuted, `C` refuted (the carrier's attack falls), `T` reinstated
  (accepted). `(x → ν)` and `(x → C)` are asserted present in `state.att`, since
  the spec makes this an attack-graph derivation and not a status check; the result
  is also asserted to survive replay. A second test does the same through the
  evidence's **transitive dependence lineage**.
- **Rubric trial guard**: both demonstrative-rubric refusal cases raise
  `WellFormednessError` — no `trace_ref` at all, and a `trace_ref` whose blob is
  well-formed JSON but not a conforming transcript — with the log bytes unchanged
  and no warrant registered. Plus a positive control that registers with a
  conforming transcript.
- **`Harness.at(root, seq)` creates nothing**: the tree listing (files *and*
  directories) is identical before and after opening a view at every seq, and a
  root with no storage yet stays empty.
- **Sealed holdout blob**: with a `holdout/<ref>` marker present, the view's
  `FencedBlobStore` reports `is_grounding_available(ref) is False` and `get(ref)`
  raises, while the live store still serves the bytes; after a `Reveal` event a
  later fence reads it and the earlier fence stays sealed.
- **`carry_add`**: an already-registered warrant carried by a second artifact
  through `register_batch` (warrant not re-provided) records the pair in the
  event's `carry_add`, lands in `state.carries`, produces the attack edge, disables
  both carriers when the shared ν is attacked, and survives replay.
- **`state.conn`**: every artifact mapped, every value `0`, key still present in
  the serialized state, unchanged by replay and by a time-travel view.

## 7. `VENDOR_NOTES.md` accuracy

- **Preamble** now reads "every cut is a **deletion plus four comment/import-line
  rewrites**" and tables the four sites with upstream line numbers, re-derived by
  normalised diff (strip the header line, `s/deepreason_core\./deepreason./`, diff
  against upstream): `storage/objects.py` 210–219 (the `_SCHEMA_ID_FIELDS` comment,
  vendored 46–49), `storage/objects.py` 236–244 (`_object_data`'s comment),
  `harness.py` 183–186 (the `_reset` derived-caches comment) and `harness.py` 2201
  (the `conn_map` → zero-map line). It also names the five import statements that
  lose a *name* while the statement is retained (`ontology/event.py` 10–11 and 13;
  `harness.py` 10–11, 34, 69–70) and the two insertions that are not cuts, and
  states the reproduction recipe.
- **`harness.py` kept ranges corrected by measurement**: `~1–133, 155–208,
  353–578, 1979–2201` (was `155–209` and `358–578`), gap `209–352` (was
  `210–357`), plus the note that the file carries **33 inserted lines** (vendored
  56–88) of inlined `informal/trial.py` helpers. Two stale row line numbers in the
  same table fixed: `123` → `122–123`, `134–153` → `134–154`, `182–198` → `188–198`
  (183–186 being the comment rewrite, not a deletion).
- **Cut #2** now states that the `LLMCall` cut is **byte-neutral only for llm-free
  events**: `attempts`, `truncated`, `mean_surprisal` and `attempt_trace` carry no
  `exclude_if` and were serialised unconditionally upstream, so an llm-bearing
  event's bytes differ; `Event.llm` has no `exclude_if` in either tree, so
  `"llm":null` is written either way and every P0 event is byte-identical.
- **§8** gains a `src/deepreason/cli/` row (the `why`/inspect CLI is not vendored,
  with the three reasons), and the scope line is softened from "the P0 row of spec
  §16 and nothing else" to **"a subset of the P0 row"**.
- **§D** reworded: `conn` is **"computed as zero and persisted into every
  materialized state"** — every artifact mapped, every value 0, key present — not
  merely "uncomputed".
- **New §F**: `POPPER_BATTERY` is an **empty tuple upstream at `9607fba`** — the
  pinning mechanism is vendored, the battery is not populated.
- **§C** rewritten: upstream declares `>=2.7`, we declare `>=2.7`, tested at 2.13.5
  and at 2.7.4, with the CI floor leg named. The old `>=2.11` rationale is kept as
  a rejected alternative, with `>=2.0`.
- Tests section updated for the new paths, the two new modules and the 50-test
  total; a **Verification log** section added at the end with every command and
  summary line.

## 8. `provenance.json`

- Top-level **`note`**: *"destination hashes to be recomputed by the publisher
  after final assembly"*, with a `note_detail` saying why every
  `destination_sha256` below is now stale. **`harness.py`'s `destination_sha256` is
  untouched.**
- **`license_file`** block added (§3 above).
- **`new_files`** added: `THIRD_PARTY_NOTICES.md`, `tests/graph_core/__init__.py`,
  `tests/graph_core/golden_build.py`, `tests/graph_core/test_p0_acceptance.py`,
  `tests/graph_core/test_closures_and_fences.py`, and the two staged modified
  copies (`pyproject.toml`, `.github/workflows/tests.yml`) marked as such.
- **`modified": []`** with a `modified_note` explaining that it is empty by
  construction: nothing pre-existing is edited in place, and the two repository
  files that must change are staged as full modified copies.
- **`dependencies_added: ["pydantic>=2.7"]`** with an accurate
  `dependencies_note`: upstream's own floor, why `>=2.11` and `>=2.0` were both
  rejected, and the two versions the suite was actually run against.
- Every **test file re-declared under its new `tests/graph_core/…` path**, with the
  relative-import change recorded; `helpers.py`'s summary notes that
  `frozen_clock()` moved to `golden_build.py`.
- `ontology/problem.py`'s `cut_summary` carries the corrected `SpawnTrigger`
  wording (§4 above); `spec.scope` softened to "a subset of the … P0 row".
- Each file entry gains a `header_rewritten` field recording the new header, with
  `harness.py`'s marked **PENDING** for the publisher.
- `verification` block replaced with this revision's runs.

## 9. Bytecode stripped

Every `__pycache__` directory and `.pyc` file removed from the staging tree with:

```
find <staging> -name '__pycache__' -type d -prune -exec rm -rf {} +
find <staging> -name '*.pyc' -delete
```

recorded in `VENDOR_NOTES.md` under **Verification log → Bytecode hygiene**. Every
test run sets `PYTHONDONTWRITEBYTECODE=1`, which the workflow already sets in
`env:`.
