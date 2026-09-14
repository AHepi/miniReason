> Published verbatim, body unedited: this document was written against the staging tree, so `NOTES.md`, `FIXES.md`, `<importer>`, the staged `src` and the staged `vendor-core` below name that scratchpad tree and not any path in this repository, where the files it describes are `src/minireason/graph_import_h005.py`, `src/minireason/data/fcl1.schema.json`, `tools/import_h005.py`, `tests/test_graph_import_h005.py`, `tests/data/h005_import_pins.json`, `docs/workflows/graph-import-h005.md` and `docs/design/h005-import-notes-2026-09-14.md`; the staging tree's `src/minireason/__init__.py` shim was not published.

# `import_h005` — adversarial-review fixes, 2026-09-14

One entry per named review finding: what the finding was, what changed, what it
cost, and what now pins it. Staging only — nothing under
`/home/user/miniReason` and nothing under the staged `vendor-core` was touched.
The design notes are now `docs/design/h005-import-notes-2026-09-14.md` (linked
from the workflow doc); `NOTES.md` is a pointer to it.

Suite: **60 tests, OK**, over the real occurrence
`experiments/diagnostics/H005-open-prose-commitments/occurrence-01` (read-only).

> A second adversarial round followed this one. Where a section below is now
> out of date, it carries a pointer; the full record is
> **[Recheck closures](#recheck-closures)** at the end of this file, and the
> suite is **79 tests, OK** as of that round. `deepreason_core` is no longer a
> separate staged `vendor-core`: it is published in the repository at
> `src/deepreason_core`, and the staged suite runs against it.

---

## A. Residue completeness (blocker)

**Finding.** The claim that everything unmapped is reported was false. An FCL
`claim` record maps to no spec construct and raised no residue code, and the
reasoning that `uptake_refs_unmapped` covered it fails for any claim the author
left out of `uptake` — occurrence-01 has three: `daily/mini_fcl/cycle01/rival`
declares `uptake = ["r2","r6","r7","r9"]`, so claims `r1`, `r3`, `r4` were
reported by nothing at all.

**Changed.**
* New code `claim_record_unmapped` (severity `unmapped`, unit `record`), emitted
  once per `claim` record with the verbatim record JSON, exactly like
  `use_record_unmapped`. **15** in the golden scope.
* Its reason states the coverage relation explicitly: a claim inside `uptake` is
  additionally covered by `uptake_refs_unmapped`; a claim outside it is covered
  by nothing else, which is why the code exists.
* Notes §6.6 rewritten from an open question into a resolved false claim, naming
  `r1`/`r3`/`r4`.
* Invariant **I5** narrowed in the module docstring: unmapped constructs are
  reported *at the granularities the closed vocabulary names*, and every FCL
  record is either mapped or coded — record-level completeness, not semantic
  completeness.
* `REPORT.md`'s "Nothing was dropped silently." deleted and replaced by a
  paragraph, **"What this table does and does not claim"**, that states
  record-level completeness and explicitly disclaims the stronger reading.
* Workflow doc: the "everything unmapped is reported" line replaced by the same
  bounded claim, with the `r1`/`r3`/`r4` example.
* `EXPECTED_RESIDUE` updated (`claim_record_unmapped: 15`).

**Cost.** The residue table is longer and `claim_record_unmapped` is the second
largest record-unit code. That is the honest size of the loss.

**Pinned by.** `test_every_claim_record_is_reported_as_unmapped` (count, unit,
severity, and that `r1`/`r3`/`r4` are absent from `rival`'s `uptake`);
`test_residue_totals_match_the_corrected_contract`.

---

## B. Trace pinning (blocker)

**Finding.** The trace was read and used — for the label index and the
projection resolver — with nothing pinning it. A rewritten `selected_source`
could steer a reference, and was caught only lazily, if some ref happened to
travel through that slot.

**Changed.** `_verify_node_custody` now reads `requests/<coord>.json` and, per
node, **before the trace is handed to anything**:
* `study_digest(request) == attempt['request_sha256'] == receipt['request_sha256']`
  → `REQUEST_RECORD_MISMATCH` (plus `REQUEST_COORDINATE_MISMATCH`);
* `request['trace_sha256'] == study_digest(trace)` → `TRACE_NOT_PINNED`;
* `sha256(provider/<problem>/<arm>/cycle<NN>/<node>/call-0001.{request,response}.json)`
  against the receipt's `provider_{request,response}_sha256` →
  `PROVIDER_BYTES_CHANGED`, skipped only when `receipt['status'] == "FAILED"`,
  mirroring `tools/multicycle_commitment_study.py::read_terminal`.

The trace read itself moved into `_verify_node_custody`, so `load_nodes` cannot
obtain an unpinned trace. The redundant per-ref hash comparison in
`_projection_source` was removed (§K replaces it with a custody pass over every
projection of every node).

**Cost.** 34 more files read per full-occurrence import (17 requests, 17×2
provider calls); `files read and hashed` rises from 20 to 51 on the golden
scope. Worth it.

> **Recheck closures §1-§3 tighten this.** `trace_pinned` counts as *run* only
> where the request record is itself pinned by an attempt or a receipt; a
> coordinate with **no** request record is now refused outright
> (`REQUEST_RECORD_MISSING`) rather than admitted with an unpinned trace; and
> the provider check no longer lets an absent hash and an absent file compare
> equal (`PROVIDER_HASH_MISSING`).

**Pinned by.** `TracePinningTest.test_one_tampered_selected_source_field_is_
refused_before_any_write` (one field flipped in a trace copy → `TRACE_NOT_PINNED`,
nothing written), `..._a_tampered_request_record_is_refused`,
`..._tampered_provider_bytes_are_refused`, and the `(5/5 nodes)` assertions in
`test_custody_is_split_and_counted_per_check`.

---

## C. Honest custody table (blocker)

**Finding.** `REPORT.md` printed a static list of checks, each rendered
`verified`, whether or not the check had run over every coordinate — and
self-consistency checks were listed beside cross-file ones as if worth the same.

**Changed.**
* New `_CustodyLedger`/`_Check`: every check declares a `kind`
  (`cross_file` | `self_consistency`), a `unit`, and accumulates `ran`/`total`
  plus the subjects skipped with the input that was missing.
* Rendering: `verified (n/n nodes)`, or
  `verified (n/m nodes; k coordinate(s) had no receipt: …)` naming them, or
  `not applicable in this scope (0 …)`. No bare "verified" is reachable for a
  check that did not run everywhere.
* `REPORT.md` splits them under **"### Cross-file custody"** and
  **"### Internal consistency only"**, the second carrying the sentence that
  such a check cannot detect a coherent rewrite.
* New rows: **"per node: receipt present"** (naming absent coordinates) and
  **"event ts nondecreasing | yes/no"**, the `no` case carrying the
  declared-deviation wording.
* Mirrored in `report.json` as `custody.cross_file` / `custody.self_consistency`,
  each entry `{key, kind, check, unit, ran, total, skipped[], result}`.
* Workflow doc: a receipt-less coordinate is **admitted with its absent inputs
  recorded, not refused**; and a new paragraph states exactly which links of
  `read_terminal()` are reproduced and which are not (the ones needing
  `payload_for`/`settings_for`/`decode_contribution` from the repository, which
  I1 forbids importing).

> **Recheck closures §1, §3 and §8 amend this.** A *receipt*-less coordinate is
> still admitted; a *request-record*-less one is refused. `trace_pinned` and
> `request_record` are counted as not run where nothing pins the request
> record, and `projection_source` counts projections rather than nodes.

**Cost.** The custody section is longer and two of its rows now say less than
they used to. That is the point.

**Pinned by.** `test_custody_is_split_and_counted_per_check`;
`ReceiptlessCoordinateTest.test_a_missing_receipt_is_recorded_not_refused`
asserts the exact `verified (4/5 nodes; 1 node(s) had no receipt: …)` string and
that **no** custody row in the rendered table ends in a plain `| verified |`;
`FullOccurrenceTest.test_custody_ran_for_every_node_not_only_the_parsed_ones`.

---

## D. Multi-arm framing (blocker)

**Finding.** A multi-arm report invites a cross-arm reading it cannot support.

**Changed.** `ImportReport.multi_arm_framing` returns a fixed paragraph whenever
the scope spans more than one arm, counting prose arms and FCL-1 arms. It is
emitted **twice** in `REPORT.md` — in "What this is, and what it is not", and
immediately above the labels table — printed by the CLI before the labels, and
carried in `report.json`. The text is a module-level template, not a per-run
sentence, so it cannot be softened:

> **Superseded by Recheck closures §7.** The two parenthetical lists were
> hard-coded to the occurrence's five arms, so a narrower scope was told it
> contained arms it had not read. They now come from `arm_surfaces()`; every
> *claim* the paragraph makes is still a module constant
> (`MULTI_ARM_FRAMING_TAIL`).

> This scope contains N arms whose declared commitment surface is prose (bare,
> native, matched, mini_prose) and M whose surface is FCL-1 (mini_fcl). A prose
> commitment surface is never parsed, so no warrant, no attack edge and no
> refuted label can arise from a prose arm under this import. The distribution
> of statuses across arms is therefore a property of the carrier this importer
> reads, not a comparison between the arms. Any cross-arm reading is root's, not
> this instrument's.

**Cost.** None. Single-arm scopes are unaffected (`multi_arm_framing is None`).

**Pinned by.** `FullOccurrenceTest.test_the_multi_arm_framing_paragraph_is_
emitted_twice` (exact text, count of 2, and both positions relative to the
section heading and the labels table header);
`CommandLineTest.test_the_multi_arm_framing_is_printed_when_the_scope_spans_arms`;
`test_report_files_are_written_and_self_consistent` asserts a single-arm report
contains none of it.

---

## E. Wording: "nothing criticised it" (blocker)

**Finding.** "accept-by-position … nothing criticised it" is false as written.
Nothing criticised it *in this import*, which reads only an FCL-1 commitment
surface and cannot see criticism carried any other way.

**Changed.** One module constant, `ACCEPT_BY_POSITION`, replaces every
occurrence — the `opaque_envelope` and `parse_failure`/`schema_failure` residue
reasons, every `why` chain, `REPORT.md`, and the workflow doc:

> accept-by-position: no warrant in this import targets it. This import reified
> criticism only from an FCL-1 commitment surface, so the absence of an attacker
> is not evidence that the contribution was uncriticised.

The `why` chain of any artifact whose surface was **not** read now ends with that
artifact's specific `commitment_surface_state` and what it does and does not
mean (four distinct notes: `unavailable_decode_failure`, `prose_not_parsed`,
`parse_failure`, `schema_failure`).

**Cost.** None.

**Pinned by.** `test_accept_by_position_never_says_nothing_criticised_it`
asserts the new wording is present and that neither "nothing criticised it" nor
"nothing criticises it" appears anywhere in `REPORT.md` or `report.json`;
`FullOccurrenceTest.test_the_opaque_nodes_why_chain_names_the_surface_state`.

---

## F. Opaque attribution (blocker)

**Finding.** The `opaque_envelope` reason left the empty commitments string
unattributed, which lets a reader score an encoding fault as an arm that
declined to commit — precisely the misreading root's review warns against. The
`prose_commitment_surface` reason additionally claimed the artifact "is not
adjudicated", which is false.

**Changed.**
* `OPAQUE_ENVELOPE_REASON` attributes the empty string to the study harness's
  strict JSON decode failure and `decode_contribution`'s failure branch, cites
  `docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md` **by path**,
  states the commitment surface is **UNAVAILABLE, not absent**, and says in
  terms that this is **not evidence that the author declined to commit**.
* Same wording in the workflow doc's "What it does NOT do" list and in
  `REPORT.md` wherever the count is nonzero (a dedicated paragraph under the
  framing).
* Side-table field `opaque_reason` → **`commitment_surface_state`**, closed
  values `read_fcl1 | prose_not_parsed | unavailable_decode_failure |
  parse_failure | schema_failure`, exported as `COMMITMENT_SURFACE_STATES` and
  mirrored in `report.json` as `commitment_surface_states`.
* `PROSE_SURFACE_REASON` corrected: the artifact **IS** adjudicated — registered,
  in the graph, labelled; with no surface read it has no attacker, so grounded
  semantics labels it accepted by position, **and that label carries no
  information about the arm**.

**Cost.** `side_table.json` consumers reading `opaque_reason` must move to
`commitment_surface_state`. The old key is gone rather than aliased, so a stale
reader fails loudly.

**Pinned by.** `FullOccurrenceTest.test_opaque_and_prose_surfaces_are_counted_
and_attributed` (the two matched nodes, the review path, "UNAVAILABLE, not
absent", "declined to commit", and the three prose-reason clauses);
`test_report_files_are_written_and_self_consistent` asserts `opaque_reason` is
absent from every side-table row.

---

## G. Provenance role (major)

**Finding.** Validity nodes were minted with `ProvenanceRole.CRITIC`, which says
this process produced a criticism of its own. It did not; it transcribed one the
authors wrote.

**Changed.** Every artifact this import creates — node, FCL-1 document, ν —
carries `ProvenanceRole.IMPORT`, in both the written path and
`adjudicate_offline`. Notes §6.5 corrected: the earlier warning that `IMPORT`
"excludes these artifacts from survivor sets" via `state.counts_as_survivor()`
was invented — **the staged core has no survivor machinery at all**
(`grep -rn "survivor\|counts_as" src/deepreason_core/` returns nothing). `IMPORT`
is chosen because it is true, and it is a **forward guard** for a fuller core
that may later distinguish imported material.

**Cost.** None; `Artifact.compute_id` does not read provenance, so no id moved.

**Pinned by.** `test_every_artifact_in_the_written_root_has_provenance_role_
import` (the role set of the written root is exactly `{"import"}`, ν included).

---

## H. Criticism-of-criticism exception (major)

**Finding.** §2(7) says criticism of a reified criticism retargets onto the
warrant's validity node. `objection.o4` against `o1`/`o2` does not, and nothing
said so or counted it.

**Changed.**
* Stated explicitly in the notes §2(7) and in the deviation text: retargeting an
  **intra-document** criticism of a criticism would become a **self-attack
  through the carrier closure** — spec §1 lifts an attack on a ν onto every
  carrier of the warrant, and here that carrier is the objector itself, which
  would make the artifact self-defeating. That is not what an author asserts by
  qualifying their own earlier objection.
* New code `criticism_of_criticism_intra_document_dropped` (severity `lossy`,
  unit `ref`), emitted alongside the existing `objection_target_self_ref_dropped`
  whenever a dropped self-target names a record this import reified. **2** in the
  golden scope (o4 → o1, o4 → o2); o4 → c2 is not one, because `c2` is a claim
  and minted nothing.
* New `DEVIATIONS` entry, so `REPORT.md` and `report.json` carry the exception.

**Cost.** `objection_target_self_ref_dropped` stays at 4 and the new code adds 2
entries that describe the same two refs from a different angle. Deliberate: the
first records *that* a self-target was dropped, the second records *what kind*
of loss that was.

**Pinned by.** `test_intra_document_criticism_of_criticism_is_a_declared_
exception` — the two entries, their record ids, the "SELF-attack"/"carrier
closure" reasoning in the detail, that o4 minted no warrant, that no self-edge
exists on the objection artifact, and that the deviation text names it as the
one exception.

---

## I. CLI (major)

**Finding.** No I7 banner on the terminal output; a typo in `--why` threw a
`KeyError` traceback after a successful import; exit code 2 conflated custody
refusal with everything else including a refused out-root.

**Changed.**
* The I7 banner (plain text) prints before the `LABELS` header, with an
  error-severity banner under it when any `error`-severity code fired, and the
  multi-arm paragraph under that when the scope spans arms.
* `--why` is resolved **after** the import; `KeyError` prints
  `WHY_UNRESOLVED: <name>` plus the closest candidate names
  (`difflib.get_close_matches`, then substring) and the line "the import itself
  succeeded; only this selector did not resolve." to stderr — and **returns 0**.
* Exit codes: **2** custody (`CustodyError`, now including
  `OCCURRENCE_FILE_MISSING` and `OCCURRENCE_FILE_MALFORMED_JSON`, which `_Reader`
  raises instead of letting `OSError`/`ValueError` escape), **3** mapping
  (`MappingError`), **4** out-root refused via the new `OutRootRefused` class
  (both `OUT_ROOT_INSIDE_OCCURRENCE` and the write-once collision; it inherits
  `ValueError` *and* `FileExistsError` so existing callers of either keep
  working). argparse keeps its own usage-error behaviour and is not remapped;
  the workflow doc documents the table and how to tell a usage error apart (the
  `usage:` line, and no `CUSTODY_REFUSED:`).

**Cost.** `import_occurrence` now raises `OutRootRefused` where it raised bare
`ValueError`/`FileExistsError`. Subclassing keeps that source-compatible.

> **Extended by Recheck closures §4 and §9.** Exit **5**
> (`SELECTOR_MATCHED_NOTHING`) was added for selectors that match none of the
> coordinates the occurrence holds, and the out-root existence check moved
> ahead of all work; exit 3 now leaves nothing written, as exit 2 always did.

**Pinned by.** `CommandLineTest`, all via `subprocess`: success (banner before
LABELS, report written), `--dry-run` (exit 0, no out-root, empty parent
directory), tampered occurrence (exit 2 + `CUSTODY_REFUSED` + the specific code
on stderr, nothing written), bad `--why` (exit 0 + `WHY_UNRESOLVED` + the close
candidate on stderr + the report still written), good `--why` (empty stderr),
existing out-root (exit 4 + `OUT_ROOT_REFUSED`).

---

## J. Residue carrier ids (major)

**Finding.** `carrier.spec_artifact_id` was null for most entries, because most
residue is raised before the carrier is named — and the id depends on the
interface, which depends on the refs, which is what the residue is about. So
`residue.json` could not be joined to `side_table.json` for exactly the codes
that matter.

**Changed.** `backfill_residue_carriers()` runs after `map_records` (and after
`plan_events`/`report_edge_dedupe`, so nothing is missed) and fills
`carrier.spec_artifact_id` from `node.spec_id`. `ImportReport.residue` entries
gained a `spec_artifact_id` field.

**Cost.** None.

**Pinned by.** `test_every_residue_carrier_in_scope_names_its_spec_artifact` —
every entry with a carrier coordinate in scope has a non-null id, that id is in
the spec-id table, and it is the id for that coordinate; checked on both
`report.residue` and the written `residue.json` (>100 entries).

---

## K. Custody for every node (major)

**Finding.** `_build_label_index` did real custody — brief hash, projection id
shape, brief/index agreement, task label — and ran only for a node whose FCL-1
document parsed. A whole prose arm went uncustodied. Projection residue was
likewise document-gated.

**Changed.**
* Split. `_verify_projection_custody` (the custody half) runs for **every** node
  from `load_nodes`; only the *use* of the index by `resolve_ref` is gated on a
  parsed document.
* New `_verify_projection_sources` checks every projection's `selected_source`
  hashes against the authored record, for every node, in one pass after loading —
  replacing the lazy per-ref check.
* `_record_projection_residue` runs for every node. Its
  `projection_exposed_unreferenced` reason branches: for an unread surface it
  says the commitment surface was not read, so no ref *could* cite the slot, and
  that nothing is implied about whether the author used the material.

**Cost.** Full-occurrence counts rise: `projection_absent` 2 → 4,
`projection_exposed_unreferenced` 2 → 10. Those were always true; they were
simply not being looked for.

> **Recheck closures §8 finishes this.** `_verify_projection_sources` ran for
> every node but *counted* per node, so one checkable slot made a whole node
> read as verified. Its unit is now the projection, and every slot the check
> could not run over is named.

**Pinned by.** `FullOccurrenceTest.test_custody_ran_for_every_node_not_only_the_
parsed_ones` (17/17 on `brief_pinned`, `brief_label_index`, `task_label`,
`artifact_self_hash`, `receipt_present`, `request_record`, `trace_pinned`,
`provider_bytes`) and `..._test_projection_residue_runs_for_every_node`.

---

## L. Fixture (major, both lenses agree)

**Finding.** `tests/fixtures/h005_daily_mini_fcl_cycle01/` was a partial copy
that could drift from the thing under test — and did: it shipped the matched arm
without `responses/` or `attempts/`, so the tests exercised a receipt-less path
that **does not exist** in the occurrence, and the golden numbers were a
property of the copy.

**Changed.**
* `tests/fixtures/` **deleted**. `OCCURRENCE` is located by walking up from
  `__file__`, then from the installed `minireason` package, then from the cwd,
  honouring `H005_OCCURRENCE_ROOT` — so the same test file works in staging and
  after publication.
* New `tests/data/h005_import_pins.json`: occurrence-relative path → sha256 for
  all **162** files, regenerated from the real occurrence. `setUpModule`
  re-hashes every one: `unittest.SkipTest` if the occurrence is absent, and a
  refusal naming each differing path if a pin no longer matches — the same
  posture as the importer's own custody, refuse rather than adapt.
  *(**Recheck closures §11**: the absent-occurrence branch now **fails** unless
  `H005_IMPORT_ALLOW_SKIP=1` — a skip is a green run that tested nothing.)*
* Tamper tests `shutil.copytree` the occurrence into a `TemporaryDirectory`,
  narrowed to the arms the test needs by an `ignore` callable.
* The fixture-manifest machinery (`_verify_fixture_manifest`,
  `FIXTURE_MANIFEST_SCHEMA`, the `custody.fixture_manifest` field, the workflow
  doc row) is **removed** as dead code: the occurrence carries no `MANIFEST.json`.
* Golden labels **verified unchanged** against the real occurrence — 14 accepted,
  3 refuted, `|att| = 4`, 7 warrants, 82/84 refs, event count 38.
* The receipt-less path is now exercised only synthetically, by removing a
  receipt from a temp copy.

**Cost.** The suite needs the occurrence present; without it, it skips rather
than passing on a copy. That is the correct failure mode.

**Pinned by.** `setUpModule`; `ReceiptlessCoordinateTest` (both halves);
`GoldenImportTest` and `FullOccurrenceTest` as a whole.

---

## M. Report wording (majors/minors)

1. **`dep` "the finding".** Workflow doc line replaced with: "`att` is the
   criticism the authors declared; `dep` is empty here because every `depends`
   ref in this occurrence is document-local and node granularity would turn it
   into a self-loop. That is a property of the mapping, not a result about the
   occurrence."
2. **dep-empty branches on observed counts.** `REPORT.md` now distinguishes *no
   `depends` ref authored at all* ("`dep` is empty because the authors declared
   no dependence at all, not because the mapping dropped anything") from *all
   document-local* (naming the count and the self-loop reason) from the mixed
   case with rejections.
3. **DEVIATIONS filtered.** Each row carries `(N in this scope)` or
   **(not triggered in this scope)**. Pinned by a loop in
   `test_report_files_are_written_and_self_consistent` over every declared
   deviation.
4. **Error-severity banner** under the I7 banner in `REPORT.md` and under the I7
   line in the CLI whenever any `error`-severity code fired, naming the codes and
   counts and saying to read the residue first. `report.json` gains
   `error_severity_residue`.
5. **Notes §3 closure paragraph corrected.** It named a source-artifact closure
   that **is not in the vendored slice**. Replaced by an enumeration of the three
   closures `build_att` actually implements — validity-node (active here),
   case-law (inert: every imported warrant has `commitment = None`), evidence
   (inert: every ν ref is a `mention`) — and a note that the prefixed
   `h005_source_artifact` key is still right to write but must not be described
   as neutralising a closure that is not there.
6. **Notes §2(5) POPPER_BATTERY.** `register_problem` does run the battery line,
   but `POPPER_BATTERY` is the **empty tuple** in the vendored slice, so nothing
   is pinned and `criteria` stays `[]`. The empty-criteria argument rests on the
   schema-id point alone.
7. **Notes published** as `docs/design/h005-import-notes-2026-09-14.md`, staged
   under `$I/docs/design/`, linked twice from the workflow doc. `NOTES.md` is now
   a pointer, so the two cannot drift.
8. **`clock` dependency stated.** The workflow doc has a "Core dependency"
   paragraph, and `import_occurrence` raises
   `MappingError("CORE_CLOCK_UNSUPPORTED: …")` if `Harness` rejects the
   parameter, rather than writing a root it cannot reproduce. Pinned by
   `CoreDependencyTest`.
9. **`_BODY` under `view == "commitments"`** now also emits
   `ref_through_unexposed_view`: under that view no BODY section was rendered at
   all, so the pseudo-local header was never readable through the projection. Not
   triggered in occurrence-01 (the one `#BODY` ref goes through a `view ==
   "body"` projection), but the asymmetry with the real-local-name case was
   arbitrary.
10. **`NO_LEADING_RECEIPT`.** A receipt-less coordinate inherits the *previous*
    coordinate's `finished_utc`. The first coordinate has no previous one, and
    the old code fell back to `min(stamps)` — back-dating the leading node to a
    time belonging to some later node. A scope whose first coordinate has no
    receipt is now refused with `NO_LEADING_RECEIPT:<coordinate>`, documented in
    the workflow doc and the notes, pinned by
    `test_a_scope_whose_first_coordinate_has_no_receipt_is_refused`.

---

## N. Tests

* **Determinism across processes.** `test_two_imports_are_byte_identical_across_
  hash_seeds` builds the second root in a `subprocess` with
  `PYTHONHASHSEED=12345`. Two imports inside one interpreter share a string-hash
  seed, so the old test could not have caught an output that depended on
  set-iteration order.
* **Synthetic depends mapper.** `SyntheticDependenceTest` drives `map_records`
  over hand-built two-node scopes with no occurrence on disk:
  - cross-document `depends` → a `dependence` ref in the interface, a `dep` edge,
    `depends_cross_document` residue, and — with the premise refuted by the same
    node's objection — a **`suspended_unsupported`** label whose `why` says
    "Orphaned != false";
  - the cycle guard, reached by seeding the mapper's edge accumulator →
    `dependence_cycle_rejected`, no dependence ref in the interface, `dep` empty.
  - A third test records *why* the guard cannot fire naturally: refs resolve
    through projections whose source must already be registered, so every `dep`
    edge points backwards in registration order and the relation is acyclic by
    construction; the other half of a mutual dependence is dropped earlier as
    `ref_to_unregistered_target_dropped`. This is now stated in the notes
    (§5.11) rather than left as an implied capability.
* **Prose dispatch.** `SyntheticProseDispatchTest` gives a *prose* arm a
  commitments string that **is** valid FCL-1 (asserted by calling
  `parse_fcl1_document` on it directly) and asserts the importer still does not
  parse it: `document is None`, `commitment_surface_state == "prose_not_parsed"`,
  empty `Interface`, no warrant, no att edge, `prose_commitment_surface` 1,
  `parse_failure`/`schema_failure` 0 — dispatch is on the declared surface, never
  on whether the string happens to parse.

---

## O. Engineering hygiene

* **`attack_index(att_edges)`** — target → sorted attackers, now the single
  spelling used by `ImportReport.labels_table`, `_Importer.build_why` and
  `_report_markdown`. Three renderings of the same relation can no longer
  disagree about it.
* **`label_order(labels, names)`** — the one display order (readable name, then
  id), used by the same three.
* **Dead code removed**: `_verify_fixture_manifest` and `FIXTURE_MANIFEST_SCHEMA`
  (no occurrence carries a `MANIFEST.json`, and the fixture is gone); the
  duplicated hop-2 hash loop inside `_projection_source` (the custody pass covers
  exactly the same comparisons for exactly the same owners); `_Node.artifact`
  (assigned in `register`, never read); `custody["plan_verified"]` (a constant
  `True` duplicating the ledger's `plan_identity` row).
* **Public API unchanged.** `import_occurrence(occurrence_dir, out_root, *,
  problems, arms, cycles, dry_run)` is identical. `ImportReport` grew
  `multi_arm_framing`, `commitment_surface_states` and the
  `error_severity_totals` property, and its `residue` entries grew
  `spec_artifact_id`; nothing was removed or renamed.
* One small helper added for tests and internal use:
  `_Importer.residue_code_count(code)`.

---

## Results

Staged suite: **Ran 60 tests — OK**.

| run | scope | artifacts | accepted | refuted | suspended | suspended_unsupported | `\|att\|` | `\|dep\|` | warrants | events |
|---|---|---|---|---|---|---|---|---|---|---|
| golden | `daily/mini_fcl/cycle01` (5 coordinates) | 17 | 14 | 3 | 0 | 0 | 4 | 0 | 7 | 38 |
| full | whole occurrence (17 coordinates, 5 arms) | 29 | 26 | 3 | 0 | 0 | 4 | 0 | 7 | 50 |

The golden labels are identical to the pre-fix run against the real occurrence;
nothing in this round moved a label, an id or an edge. What moved is what the
report says about them.

---

# Recheck closures

The adversarial recheck of the round above. Twelve findings, all closed in
staging; nothing under `/home/user/miniReason` was touched. The vendored core
is now published in the repository at `src/deepreason_core` (with the `clock`
parameter of notes §4), so the staged suite runs against it directly:

```
PYTHONPATH=<importer>/src:/home/user/miniReason/src \
  python -X utf8 -m unittest discover -s <importer>/tests -v
```

Suite: **79 tests, OK** (60 before). No label, id, edge, warrant, event or
residue count moved; everything that moved is what the instrument says about
what it checked.

---

## 1. Custody ledger honesty — `trace_pinned` (major)

**Finding.** `trace_pinned` counted as *run* whenever a request record existed,
including when nothing pinned that request record. With no attempt and no
receipt, `request.trace_sha256 == digest(trace)` is one file agreeing with
another file that nothing independent fixes — exactly the self-consistency the
ledger split (§C) exists to distinguish — and the row still rendered
`verified (n/n nodes)`.

**Changed.** `_verify_node_custody` still performs the comparison (a mismatch is
still `TRACE_NOT_PINNED`, whatever pins the request record), but the ledger now
counts `trace_pinned` as run **only where `pinned_by` is non-empty** — i.e.
where the request record's own digest matched an `attempt.request_sha256`
and/or a `receipt.request_sha256`. Otherwise it is recorded skipped with the
absent input named, `attempt or receipt`, alongside `request_record`, and the
row renders `verified (4/5 nodes; 1 node(s) had no attempt or receipt: …)`.
The declared check text says so: "counted as run only where the request record
is itself pinned by an attempt or a receipt".

**Cost.** None on `occurrence-01` (every node has both), and on a receipt-less
coordinate the ledger now says less than it used to. That is the point.

**Pinned by.** `ReceiptlessCoordinateTest.test_a_missing_receipt_is_recorded_
not_refused` — `(ran, total) == (4, 5)` and the exact `skipped` entry and
rendered string for **both** `trace_pinned` and `request_record`;
`GoldenImportTest.test_custody_is_split_and_counted_per_check` — `5/5` with an
empty `skipped` list and the qualification present in the check text.

---

## 2. Provider bytes: `None == None` was a pass (major)

**Finding.** For a non-`FAILED` receipt the check read

```python
actual = sha256(...) if reader.exists(relative) else None
if actual != receipt.get(f"provider_{part}_sha256"): raise ...
```

so a deleted call file beside an absent (or nulled) hash compared `None` to
`None` and **verified**. The one custody row that reaches the provider's own
bytes could be switched off by deleting them.

**Changed.** Both halves must be present before any comparison: the receipt's
`provider_{request,response}_sha256` must be a non-empty `str` **and** the call
file must exist, or `CustodyError("PROVIDER_HASH_MISSING:<coordinate>:<part>")`
is raised — before any write. Only then is the hash compared
(`PROVIDER_BYTES_CHANGED`). `FAILED` receipts are still skipped, as in
`read_terminal`, and recorded as skipped.

**Cost.** None; every non-FAILED receipt in `occurrence-01` carries both.

**Pinned by.** `ProviderBytesTest.test_a_deleted_provider_call_file_is_refused`
(delete `provider/…/rival/call-0001.response.json` in a temp copy →
`PROVIDER_HASH_MISSING:daily/mini_fcl/cycle01/rival:response`, nothing written)
and `..._test_a_nulled_provider_hash_is_refused` (null
`provider_request_sha256` in the receipt, leave the file in place →
`PROVIDER_HASH_MISSING:…:request`). The second is the case the old code could
not distinguish from a pass.

---

## 3. A missing request record is refused (major)

**Finding.** A coordinate with no `requests/<coord>.json` was *admitted* with
`trace_pinned` and `request_record` marked skipped — and then its trace was
handed to the label index, the projection index and every two-hop reference
anyway. The trace is the most load-bearing input this import reads; admitting an
unpinned one is the failure §B was written to close, reopened by a deletion.

**Changed.** `CustodyError("REQUEST_RECORD_MISSING:<coordinate>")`, raised in
`_verify_node_custody` before the record is read — the same posture as
`NO_LEADING_RECEIPT`: refuse rather than proceed on an input that cannot be
checked. A missing *receipt* or *attempt* is still admitted (it costs
bookkeeping, not integrity). The workflow doc's pin-chain paragraph is
qualified accordingly, with the three cases spelled out: no request record →
refused; request record pinned by neither attempt nor receipt → admitted but
counted as not run (§1 above); non-`FAILED` receipt → provider hashes and files
both required (§2 above).

**Cost.** None: all 22 request records exist in `occurrence-01` (17 artifacts
⊂ 22 requests), so the refusal is unreachable on the real occurrence.

**Pinned by.** `RequestRecordTest.test_a_missing_request_record_is_refused`
(delete one in a temp copy → refused, `root` absent, the parent holds only the
occurrence copy) and `..._test_every_coordinate_in_the_occurrence_has_one`
(22 request records, and every artifact coordinate has one — the refusal costs
this occurrence nothing).

---

## 4. No partial roots (major)

**Finding.** "Nothing was written" held for a custody refusal (exit 2) and not
for a mapping failure (exit 3): the out-root was `mkdir`ed, the harness wrote
`log.jsonl`, `objects/` and `blobs/`, and only then were the four report files
written. A `MappingError` from `_verify_event_log` — or from anything after the
`mkdir` — left a graph root with a log and no report, which the write-once guard
then made unrepeatable.

**Changed.** The whole root is built in a uniquely named temporary **sibling**
directory (`tempfile.mkdtemp(prefix=f".{out_root.name}.importing-",
dir=out_root.parent)`) and `rename`d into place only after the last of the four
files is written and `_verify_event_log` has passed. Any exception removes the
temporary directory before re-raising. Write-once is unchanged and now
*earlier*: `out_root` must not already exist, checked **before a single
occurrence byte is read**, so an operator learns the destination is refused
immediately rather than after a full import (`OutRootRefused`, exit 4); the
existence check is repeated immediately before the rename.

**Cost.** The root appears atomically rather than incrementally, so a watcher
cannot observe a half-built root — which is the fix, not a cost. `import_
occurrence` grew one helper, `_build_report`, so the report can be assembled
before the files are written.

**Pinned by.** `AtomicOutRootTest.test_a_late_mapping_error_leaves_no_out_root_
and_no_temp_directory` (monkeypatches `_verify_event_log` to raise after the
log, objects and blobs are all written: `MappingError` propagates, `out_root`
does not exist, and the parent directory is **empty** — no leftover temp dir);
`..._test_a_successful_import_leaves_only_the_root` (the parent holds exactly
`graph`, with all five expected files in it); `..._test_an_existing_out_root_is_
refused_before_any_work` (monkeypatches `verify_custody` to fail the test if it
runs at all).

---

## 5. `material.json` and the wave files go through the wrapping reader (major)

**Finding.** `verify_custody` read `material.json` with `reader.read_bytes` and
then `json.loads` **directly**, so a truncated `material.json` escaped as a bare
`ValueError` — not a `CustodyError`, not exit 2. `load_waves` used the wrapping
reader but then did `int(wave["wave_id"][4:])` unguarded, so a wave file whose
`wave_id` was not `wave<digits>` raised `ValueError`/`KeyError` out of custody.

**Changed.** `_Reader.read_json` is split into `read_bytes` +
`_Reader.parse_json(relative, raw)`, and `verify_custody` decodes the material
bytes it already has through `parse_json` — one read, one wrapped decode
(`OCCURRENCE_FILE_MALFORMED_JSON:material.json`), plus an `isinstance` guard
before the schema check. `load_waves` validates the wave id's shape
(`^wave[0-9]+$`) before using it, as
`CustodyError("WAVE_ID_MALFORMED:<file>:<value>")`, and the ordinal is parsed
only after that; the id is then used in place of the repeated
`wave["wave_id"]` lookups.

**Cost.** None.

**Pinned by.** `CustodyRefusalTest.test_a_malformed_material_file_is_a_custody_
error_not_a_valueerror` (truncate `material.json` in a temp copy),
`..._test_a_malformed_wave_file_is_a_custody_error` (truncated wave JSON),
`PathContainmentTest.test_a_wave_id_that_is_not_a_wave_id_is_refused`
(`wave_id = "not-a-wave"` → `WAVE_ID_MALFORMED`, checked *before* the
filename-agreement rule so the more specific code is the one raised).

---

## 6. Path containment (moderate)

**Finding.** Coordinates arrive from files — `waves/*.json`, `material.json`,
`plan.json`, each record's own `coordinate` block — and every one of them is
concatenated into a read path by `Coordinate.key`, `wave_label` and
`occurrence_path`. Nothing checked them. A `"problem": "../.."` in a wave file
addressed bytes outside the occurrence, which invariant I1 forbids.

**Changed.** Two gates, at the boundary and at the read:

* `safe_component(value, what)` refuses anything that is not
  `^[A-Za-z0-9_-]+$` with `CustodyError("COORDINATE_COMPONENT_UNSAFE:<what>:
  <value>")`, and is applied to **every** component: `problem`, `arm`, `node`
  and `cycle` in `Coordinate.from_dict`; `problem`, `arm`, the cycle digits
  (which must also be a number) and `node` in `discover_scope`; the wave id in
  `load_waves`.
* `_Reader._inside(relative)` asserts that `(root / relative).resolve()` **is**
  `root.resolve()` or a descendant of it, and both `read_bytes` and `exists` go
  through it — `CustodyError("PATH_ESCAPES_OCCURRENCE:<relative>")`. That is
  unconditional and independent of what composed the path.

**Cost.** None; every component in `occurrence-01` is alphanumeric.

**Pinned by.** `PathContainmentTest.test_an_unsafe_coordinate_component_is_
refused` (four shapes — `../../etc` as a problem, `..` as an arm, `a/b` and
`rival.json` as a node — each naming its component, and a real coordinate still
building); `..._test_the_reader_refuses_a_path_that_escapes_the_occurrence`
(`../outside.json`, `artifacts/../../outside.json`, `/etc/hostname`, on both
`read_bytes` and `exists`, and nothing outside is hashed into `custody.files`).

---

## 7. Multi-arm framing named arms it had not read (moderate)

**Finding.** The paragraph's two parentheticals were hard-coded to the five arms
of the whole occurrence: `(bare, native, matched, mini_prose)` and `(mini_fcl)`.
A two-arm scope was therefore told it contained four prose arms and named three
that were not in it — a framing paragraph that misreports its own scope.

**Changed.** The counts and both lists come from `arm_surfaces()`, i.e. the arms
actually in the scope, sorted; `arm(s)` is pluralised, and an empty side reads
`no arms`. Everything the paragraph *claims* is now the module constant
`MULTI_ARM_FRAMING_TAIL`, so the §D property survives: only the inventory is
per-run, and no run can soften the claim. Full occurrence:

> This scope contains 4 arms (bare, matched, mini_prose, native) whose declared
> commitment surface is prose and 1 arm (mini_fcl) whose surface is FCL-1. …

**Cost.** The order is now sorted (`bare, matched, mini_prose, native`) rather
than the old hand-written order.

**Pinned by.** `FullOccurrenceTest.test_the_multi_arm_framing_paragraph_is_
emitted_twice` (the new sentence, `MULTI_ARM_FRAMING_TAIL` present, still twice
and still in both positions) and `FullOccurrenceTest.test_a_narrowed_scope_
names_only_the_arms_it_read` (`--arm matched --arm mini_fcl`: the paragraph is
exactly "1 arm (matched) … and 1 arm (mini_fcl) …" and contains none of `bare`,
`native`, `mini_prose`).

---

## 8. `projection_source` counted nodes, not projections (minor)

**Finding.** One checkable projection made a whole node count as
`projection_source: verified`, so a node with three out-of-scope sources and one
in-scope source rendered exactly like a node with four in-scope sources.

**Changed.** The check's unit is `projection`. Every slot is counted:
verified when its owner is in scope, or recorded skipped — with the slot named
as `<coordinate>#<brief alias>` — when the owner is out of scope
(`in-scope owner (<coordinate>)`) or the slot exposed nothing
(`exposed source (the slot is absent)`). The alias spelling is factored into
`_Importer.projection_subject`, which `_record_projection_residue` now also
uses, so the residue and the ledger cannot name the same slot differently.
Golden scope: `verified (8/10 projections; 2 projection(s) had no exposed
source (the slot is absent): …)`; full occurrence: 16/20 with all four absent
slots named.

**Cost.** Two custody rows now say less than they used to (8/10 and 16/20 in
place of 5/5 and 17/17). Those were always the true numbers.

**Pinned by.** `GoldenImportTest.test_custody_is_split_and_counted_per_check`
(unit, `(8, 10)`, and the exact rendered string);
`FullOccurrenceTest.test_custody_ran_for_every_node_not_only_the_parsed_ones`
(`(16, 20)` and the four named subjects with their `missing` reason);
`SyntheticProjectionSourceTest.test_an_out_of_scope_owner_is_a_named_skip_not_a_
silent_pass` — the out-of-scope branch is unreachable on `occurrence-01` (every
projection names an owner inside its own arm), so it is driven synthetically.

---

## 9. A selector that matches nothing is not `EMPTY_SCOPE` (minor)

**Finding.** `--arm mini_fcl_typo` produced `MappingError("EMPTY_SCOPE")` and
exit 3 — "the occurrence could not be mapped" — for what is an operator typo,
with nothing said about what the occurrence does hold.

**Changed.** `discover_scope` now builds the full coordinate list first and
filters second. No coordinates at all is still `MappingError("EMPTY_SCOPE")`
(exit 3). Coordinates present but no selector match raises the new
`SelectorMatchedNothing` — a subclass of `MappingError`, so library callers keep
working — whose message lists the selectors given and the problems, arms and
cycles that exist. The CLI catches it **before** `MappingError` and exits **5**,
printing the message (which carries its own `SELECTOR_MATCHED_NOTHING:` code)
with neither `CUSTODY_REFUSED:` nor `IMPORT_FAILED:`. The workflow doc's
exit-code table and the tool docstring both carry the new row.

**Cost.** One new exit code. `EMPTY_SCOPE` keeps its meaning and its code.

**Pinned by.** `SelectorTest.test_selectors_that_match_nothing_name_what_the_
occurrence_holds` (the selectors echoed, `arms: bare, matched, mini_fcl,
mini_prose, native`, `cycles: 1`, and `isinstance(exc, MappingError)`);
`..._test_an_occurrence_with_no_coordinate_at_all_is_still_empty_scope`
(emptied `artifacts/` → exactly `EMPTY_SCOPE`, and *not* a
`SelectorMatchedNothing`); `CommandLineTest.test_a_selector_that_matches_
nothing_exits_five`.

---

## 10. A `surface` column in the labels table (minor; the declined-or-done decision — done)

**Finding.** The labels table printed a status with no indication of the
commitment surface it was computed over, so `accepted` on a node whose
commitments string was lost in decoding sat in the same column as `accepted` on
a node whose FCL-1 document was read and attacked. The surface state was in the
side table, one file away from the thing it qualifies.

**Changed.** A `surface` column in both renderings — `REPORT.md`'s
`| artifact | id | status | surface | attacked by | carries |` and the CLI's
plain-text table — fed by `commitment_surface_states` through
`ImportReport.surface_of` and the module constant `SURFACE_COLUMN`:
`read` · `NOT READ (prose)` · `UNAVAILABLE (decode)` · `PARSE FAILURE` ·
`SCHEMA FAILURE`, and `n/a` for an artifact that has no commitment surface at
all (a validity node, an FCL-1 document artifact). `REPORT.md` carries a
paragraph above the table saying what the column means and that a status
computed over a surface that was not read carries no information about the
contribution.

**Cost.** One more column in two tables. Consumers parsing the markdown table by
position must move.

**Pinned by.** `FullOccurrenceTest.test_the_labels_table_names_the_commitment_
surface` — the two matched-arm nodes (`daily/matched/cycle01/response` and
`…/carry`) render `**accepted**` **and** `UNAVAILABLE (decode)`, a `mini_prose`
node renders `NOT READ (prose)`, a `mini_fcl` node `read`, and a ν and a
`#commitments` document both `n/a`, in the markdown *and* in the CLI table;
`CommandLineTest.test_the_labels_table_carries_a_surface_column`.

---

## 11. `setUpModule` failed open (minor)

**Finding.** With the occurrence absent the module raised `unittest.SkipTest` —
a green run that tested nothing, in a suite whose entire subject is that
occurrence.

**Changed.** It now raises `AssertionError("OCCURRENCE_ABSENT: …")` unless
`H005_IMPORT_ALLOW_SKIP=1` is set, in which case it skips and says so. The
message names both escape hatches (`H005_IMPORT_ALLOW_SKIP`,
`H005_OCCURRENCE_ROOT`). The workflow doc gained a **Tests** section stating
that CI runs on a full checkout, so the module never skips there and an absent
occurrence means a broken checkout; the publication checklist in the notes (§7)
is corrected to match.

**Cost.** A partial checkout must now opt into skipping explicitly. That is the
intended direction.

**Pinned by.** `setUpModule` itself — it is the code under discussion, and every
one of the 79 tests runs behind it.

---

## 12. Hygiene

* Every `__pycache__` under the staging tree deleted.
* The documented run command — `NOTES.md`, notes §0 and §8, and the staging
  shim's own docstring — now puts the **staged `src` first** and drops the
  separate `vendor-core` entry, because `deepreason_core` is published in the
  repository: `PYTHONPATH=<importer>/src:/home/user/miniReason/src`. With the
  repository's `src` first, `minireason.graph_import_h005` would resolve to the
  published package and the staged module under test would never be imported.
* Notes §4's publication dependency is restated against the published core: the
  `clock` parameter is present in `/home/user/miniReason/src/deepreason_core/
  harness.py`, which is what the staged suite now runs against.
* **`src/minireason/__init__.py` is not published.** It is a
  `pkgutil.extend_path` shim that exists only so the staged tree can be run
  ahead of `graph_import_h005.py` moving into the repository's own
  `src/minireason/` package, which already has an `__init__.py`. Publication
  moves `graph_import_h005.py` and `data/fcl1.schema.json` and discards the
  shim; notes §7 and §8 say so, and the file's own docstring says so in its
  first line.

---

## Recheck results

Staged suite: **Ran 79 tests — OK**.

| run | scope | artifacts | accepted | refuted | `\|att\|` | `\|dep\|` | warrants | events | refs | files hashed |
|---|---|---|---|---|---|---|---|---|---|---|
| golden | `daily/mini_fcl/cycle01` (5 coordinates) | 17 | 14 | 3 | 4 | 0 | 7 | 38 | 82/84 | 51 |
| full | whole occurrence (17 coordinates, 5 arms) | 29 | 26 | 3 | 4 | 0 | 7 | 50 | 82/84 | 51 + 96 = 147 |

**No residue total changed**, in either scope: golden is byte-for-byte the
`EXPECTED_RESIDUE` table above (153 entries over 25 nonzero codes) and full is
unchanged at 175 entries (the same 25 plus `opaque_envelope` 2,
`prose_commitment_surface` 10, and `projection_absent` 2 → 4 /
`projection_exposed_unreferenced` 2 → 10, which are §K's numbers, not this
round's). Every label, id, attack edge, warrant, validity node and event count
is identical to the run before this round. What moved is the custody ledger's
arithmetic, four new refusals, one new exit code, one new table column, and the
guarantee that a failed import leaves nothing behind.
