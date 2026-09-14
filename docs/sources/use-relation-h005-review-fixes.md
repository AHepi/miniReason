> Published verbatim, body unedited: this document was written against the staging tree, so `NOTES.md`, `FIXES.md`, `patches/` and the staged `src`/`tests`/`tools` paths it names are that scratchpad tree and not any path in this repository, where the files it describes are `src/minireason/use_relation_h005.py`, `tools/use_relation_h005.py`, `tests/test_use_relation_h005.py`, `docs/workflows/use-relation-h005.md` and `docs/design/use-relation-h005-notes-2026-09-14.md`, and where the `iter_references` patch it describes is already applied to `src/minireason/graph_import_h005.py` and `tests/test_graph_import_h005.py` by REC-20260914-Q.

# Review closure — H005 use-relation instrument (staging)

Every finding of the four-lens review that names this tree, at every severity,
with the change that closes it and the test that pins it. Lens 3 is FW5 fidelity
and owner acceptability; lens 4 is engineering and coupling.

Nothing was applied to `/home/user/miniReason`. The one change this tree needs
**in** the importer ships as a patch, not as an edit:
`patches/graph_import_h005_iter_references.patch`.

**Tests.** `PYTHONPATH=$U/src:<patched-repo>/src python3 -X utf8 -m unittest
discover -s $U/tests` → **Ran 54 tests, OK** (was 28). The instrument now
consumes `graph_import_h005.iter_references`, so the patch must be applied (or a
patched checkout put on `PYTHONPATH`) before the suite runs.

**Importer suite on the patched copy.** `PYTHONPATH=src python3 -X utf8 -m
unittest tests.test_graph_import_h005` → **Ran 85 tests, OK** (the 79 existing
tests unchanged and green, 6 added by the patch). A full-occurrence graph root
built with and without the patch is byte-identical (`diff -rq`: no differences),
so no golden label and no residue entry moves.

---

## The patch (finding 4.1's upstream fix, and 4.6 and 4.7 with it)

`patches/graph_import_h005_iter_references.patch` adds to
`src/minireason/graph_import_h005.py`, changing no importer output:

* `iter_references(occurrence_dir, *, problems=None, arms=None, cycles=None)` —
  a public generator yielding frozen `ReferenceRecord(coordinate, record_id,
  record_type, field, raw_ref, owner_coordinate, target_record_id, resolution,
  residue_code, notes)`, where `resolution` is `"resolved" | "extension" |
  "unresolved" | "task"`. It uses the importer's own custody, scope discovery,
  node loading, parsing and `resolve_ref`, and owns the wave-order availability
  set itself: **every** node becomes available when the walk reaches it, with or
  without a readable FCL-1 document, which is what `map_records` does through
  `_name_artifact` for every node in `self.order`.
* `_Importer.is_available` — an explicit availability predicate.
  `_projection_source`'s gate becomes `is_available(owner_node)` when one is
  supplied and stays `bool(owner_node.spec_id)` when it is not, so `map_records`
  is bit-for-bit unaffected and `spec_id` stops doubling as a registration proxy
  for anyone else.
* `REF_FIELDS`, `UNRESOLVED_RESIDUE_CODES`, `EXTENSION_RESIDUE_CODES`,
  `TASK_RESIDUE_CODE` — the walk order and the classification, published.
* `tests/test_graph_import_h005.py`: `IterReferencesTest`, six tests — the
  golden scope yields **84 records, 82 resolved / 2 extension / 0 unresolved /
  0 task**; the `(coordinate, record_id, field, ref) → (owner, record_id)` map
  equals the one spied off `_Importer.resolve_ref` through a real `map_records`,
  on the golden scope, on the full occurrence, and on the matched scope (which
  contains document-less in-scope nodes); the published code sets are disjoint
  and are ref-unit codes; and the walk writes nothing and mints no id.

---

## Lens 4 — engineering and coupling

### 4.1 (high) the `spec_id` sentinel did not reproduce the importer's registration

*Finding:* `_walk_refs` did `if node.document is None: continue` **before**
`node.spec_id = _IN_SCOPE_SENTINEL`, so a node whose commitment surface was
prose or undecodable never became available. A ref into such a node was reported
as `ref_to_unregistered_target_dropped`, "outside the imported scope or is not
registered yet in wave order" — which is false — where the import gives
`ref_unresolved`, "the owning artifact has no readable FCL-1 document". Secondary:
the instrument's field order was not the importer's.

*Change:* the sentinel is gone, `_walk_refs` and `_resolve` are gone, and
`_walk_references` consumes `iter_references`; it only re-attaches each yielded
ref to the parsed record it came from so the table can quote it, and makes no
resolution decision of its own. The field order is now the importer's, published
in the output as `ref_fields_resolution_order` beside this table's display order.

*Pinned by:* `ImporterEquivalenceTests` — the instrument's rows are a subset of
the map a real `map_records` produced, with the same owner and record id, and
are **exactly** its cross-document entries, on the golden scope and on the full
occurrence; the four `importer_*` counters equal the importer's own; and
`use-relation:in-scope` appears nowhere. `UnreadableSurfaceTests` is the
synthetic case the review asked for: one in-scope FCL node's surface is made
unreadable after parsing while it remains the projection source of four later
nodes, and the maps still agree exactly (both sides `{resolved 67, extensions 2,
dangling 7}`; the old instrument gave `{67, 1, 8}`), the residue carries the
importer's own reason text, and no residue line says "outside the imported
scope" or "not registered yet in wave order".

### 4.2 (high) the instrument would write inside the occurrence

*Finding:* U1 and `OutDirRefused`'s own docstring both promise it cannot;
neither `write_use_table` nor the CLI implemented a containment check, and
`use_relation_h005.py <occ> <occ>/INSIDE` exited 0.

*Change:* `UseTable` carries `occurrence_root` (the resolved root; deliberately
**not** serialised, since an absolute path would break byte-identity between two
checkouts), and `write_use_table` refuses `target.resolve() == root or root in
target.resolve().parents` with `OutDirRefused("OUT_DIR_INSIDE_OCCURRENCE:...")`,
checked before the existence check and before anything is created. The CLI
performs the same check before a single occurrence byte is read, and the exit-4
wording in the CLI docstring and the workflow doc now matches the importer's.

*Pinned by:* `OutputContainmentTests` — library-level refusal for a destination
inside the occurrence and for the occurrence itself (occurrence tree digest
unchanged, no directory created), the library-level `OUT_DIR_EXISTS` refusal the
suite never had, and a CLI run against a scratch copy asserting exit 4, the
`OUT_DIR_INSIDE_OCCURRENCE` message, and an unchanged tree digest.

### 4.3 (medium) spans were advertised as byte spans but are code point indices

*Change:* `record_source_spans`' docstring, the `method.span_offsets` field, the
Method block of `USE_TABLE.md` and every per-row span header now say **"code
point offsets into the decoded `commitments` string"** — matching
`split_sentences`' own wording — and say explicitly that these are not utf-8
byte offsets and not offsets into the artifact JSON file. NOTES.md's
`cut`/`sed` sentence is replaced by the check that actually works (decode the
artifact JSON, slice the `commitments` value by code point), with the two-line
recipe and with the `daily/mini_fcl/cycle01/carry` en dash named as the case
where the two kinds of offset already differ.

*Pinned by:* `RecordsArrayLocationTests.test_spans_are_code_point_offsets_not_utf8_byte_offsets`
— every published span's length equals the length of the verbatim string it
addresses (a byte span would not), and the markdown carries the wording.

### 4.4 (medium) two uptake buckets that could both be true at once

*Change:* extracted into a public `uptake_buckets(walked, coordinate)` returning
three **disjoint** tuples: naming nothing (gated on `owner is None`, not on the
record id), naming another document, and — new — naming this contribution rather
than one of its records. With the ordinary case (`records_in_uptake`) they are
exhaustive over `uptake_entries`, and `USE_TABLE.md` says so under the section.

*Pinned by:* `RowOrderAndUptakeBucketTests.test_the_three_uptake_buckets_are_disjoint_and_exhaustive`
(on every document of the golden scope) and
`.test_a_ref_naming_a_whole_contribution_is_not_a_ref_naming_nothing`, which
feeds `uptake_buckets` the four genuine cases directly, including the one
occurrence-01 does not contain.

### 4.5 (medium) nothing in the suite pinned the coupling the design rests on

*Change:* (a) the equivalence test, via a spy on `_Importer.resolve_ref` through
a real `map_records` — `ImporterEquivalenceTests`, golden scope and full
occurrence; (b) the synthetic unreadable-surface case —
`UnreadableSurfaceTests`; (c) the CLI's `BUILD_FAILED` path, reached in-process
with `build_use_table` raising `MappingError("EMPTY_SCOPE")` —
`CliFailureMappingTests.test_a_mapping_error_is_exit_three`; (d) library-level
`write_use_table` refusals, both classes — `OutputContainmentTests`; (e) the
hash-seed claim made explicit — `HashSeedDeterminismTests` runs the CLI under
`PYTHONHASHSEED=0` and `=12345` and compares both files' digests. Also added:
the three `record_source_spans` failure branches now have coverage through
`RecordsArrayLocationTests`, and the two ways of counting unresolved refs are
asserted equal (see 4.6).

### 4.6 (low) a hand-copied classification of the importer's residue codes

*Change:* `_UNRESOLVED_CODES` / `_EXTENSION_CODES` / `_TASK_CODE` are now
aliases of the importer's own published `UNRESOLVED_RESIDUE_CODES`,
`EXTENSION_RESIDUE_CODES` and `TASK_RESIDUE_CODE`, and the `resolution` verdict
on each row is the importer's, not this module's reading of the notes.

*Pinned by:* `RowOrderAndUptakeBucketTests.test_the_two_ways_of_counting_unresolved_refs_agree_on_the_golden_scope`
and `UnreadableSurfaceTests.test_the_two_ways_of_counting_unresolved_refs_agree`
— `len(unresolved_refs) == reference_totals["unresolved"]`, on a scope where
that number is not zero. Upstream, `IterReferencesTest.test_the_published_residue_classification_partitions_the_ref_codes`.

### 4.7 (low) the sentinel leaked into `residue[*].carrier.spec_artifact_id`

*Change:* removed with the sentinel (4.1); nothing of this module's is ever
written into an importer structure.

*Pinned by:* `ImporterEquivalenceTests.test_the_instrument_writes_nothing_into_the_importers_structures`
and the patch's `IterReferencesTest.test_the_walk_writes_nothing_and_mints_no_artifact_id`.

### 4.8 (low) two robustness gaps

*Change:* (a) the records array is located by walking the **top-level object's**
key/value pairs (`_records_array_start`), not by the first textual match of
`"records"\s*:\s*\[` anywhere in the string, so a prose field containing that
literal no longer refuses a legal document. (b) the CLI catches `OSError` around
`write_use_table` and maps it to the documented exit 4
(`OUT_DIR_UNWRITABLE`), and `write_use_table` removes whatever it created before
re-raising, so no half-written output directory is left behind.

*Pinned by:* `RecordsArrayLocationTests.test_a_prose_field_that_looks_like_the_records_array_does_not_mislocate_it`
and `.test_a_commitments_string_with_no_top_level_records_array_is_refused`;
`CliFailureMappingTests.test_an_oserror_while_writing_is_exit_four_not_a_traceback`.

---

## Lens 3 — FW5 fidelity and owner acceptability

### 3.1 (medium) the two caveats did not travel with the artifact

*Change:* both are now emitted by the instrument. The Method block carries
"**What a blank root cell means**" (an empty cell is an unread row, not a
reading of `unresolved`; conflating them is the FW5:688 move) and "**What the
listed passages are**" (a finding aid, not a search space; root may cite any
passage of either contribution, including one the rule did not surface; a
`no lexical overlap found` row is not a row with nothing to read). The same
blank-cell sentence is repeated above every per-row "Reserved for root" table,
and the passage header repeats the finding-aid sentence. The banner's
"beside the passages a root reader needs" is softened to "beside passages a root
reader may find worth starting from — a finding aid, never a closed search
space", and the banner now ends with the blank-cell caveat.

*Pinned by:* `PublishedCaveatTests` — both caveats present in the rendered
markdown, and the old banner phrase absent.

### 3.2 (medium) `_walk_refs` did not mark document-less nodes

Same finding as 4.1, from the FW5 side (an unavailable surface reported as an
out-of-scope coordinate is the reconstruction PROTOCOL.md:62-64 forbids). Closed
by the same change, pinned by the same tests — in particular
`UnreadableSurfaceTests.test_the_residue_carries_the_importers_own_reason_not_an_out_of_scope_one`
and `.test_the_unreadable_node_is_listed_and_never_reconstructed`.

### 3.3 (low) `_display_key` contradicted its own docstring

*Change:* the uptake sub-key is `len(node.records)` — one past the last record
index — so an uptake-derived row sorts after every record row of its document,
as the docstring says.

*Pinned by:* `RowOrderAndUptakeBucketTests.test_an_uptake_row_sorts_after_every_record_row_of_its_document`,
which compares the key against every (record index, field) pair directly, so the
choice is pinned even though occurrence-01 contains no cross-document uptake ref.

### 3.4 (low) the sentence rule was reproducible only from the JSON

*Change:* the Method block of `USE_TABLE.md` prints `token_regex` and
`sentence_boundary_regex` verbatim, in a two-row table, next to the prose — the
same standard the stopword list was already held to — so the markdown alone is
sufficient for a re-derivation.

*Pinned by:* `PublishedCaveatTests.test_both_regexes_are_printed_verbatim`,
which compares against the compiled patterns themselves.

### 3.5 (low) `root_reading` was published as a closed single-valued enum

*Change:* it is now a **suggested** vocabulary, in the module docstring on
`ROOT_READING_VOCABULARY`, in the Method block and in the workflow doc's table:
a row may carry more than one, root may write a reading the vocabulary does not
cover and say so, `unresolved` is legal and stays unresolved, and nothing about
it is enforced in code. "The instrument never selects one." is unchanged.

*Pinned by:* `PublishedCaveatTests.test_the_root_vocabulary_is_offered_not_imposed`
— "suggested vocabulary" and the may-write-something-else sentence present,
"may take exactly one of" absent.

---

## What the output did and did not gain

Regenerated over the golden scope and over the full occurrence and compared with
the staged samples: `rows`, `reference_totals`, `unresolved_refs`,
`nodes_not_read`, `scope`, `custody` and `files_read` are **identical**, and the
row headings are identical in order and content. The only differences are the
intended ones: the softened banner, three new Method paragraphs, the two new
Method fields (`ref_fields_resolution_order`, `span_offsets`), the printed
regexes, the code-point wording in every span header, the per-row blank-cell
note, and one new (empty, on this occurrence) uptake bucket.

## What changed, by file

| file | change |
|---|---|
| `patches/graph_import_h005_iter_references.patch` | **new** — the public `iter_references` walk, the availability predicate, the published code sets, and six importer tests |
| `src/minireason/use_relation_h005.py` | consumes `iter_references`; `_walk_refs`/`_resolve`/`_IN_SCOPE_SENTINEL` deleted; `uptake_buckets`; `_records_array_start`; `_display_key` fixed; code-point wording; two caveats + both regexes + the resolution order in the Method block; `occurrence_root` and the containment refusal in `write_use_table`; partial-output cleanup |
| `tools/use_relation_h005.py` | containment pre-check; `OSError` → exit 4; exit-code docstring |
| `tests/test_use_relation_h005.py` | 8 new classes (26 tests): importer equivalence, the synthetic unreadable surface, row order and uptake buckets, output containment, CLI failure mapping, hash-seed determinism, records-array location and span kind, published caveats |
| `docs/workflows/use-relation-h005.md` | `root_reading` as a suggested range; the caveats now travel with the artifact; span offsets; exit-4 wording; the patch prerequisite in the test command |
| `NOTES.md` | the span verification recipe that works; the reuse table rewritten around the public walk; open question 1 closed; a review-closure section |
