> Published verbatim, body unedited: this document was written against the staging tree, so `NOTES.md`, `FIXES.md`, `patches/` and the staged `src`/`tests`/`tools` paths it names are that scratchpad tree and not any path in this repository, where the files it describes are `src/minireason/use_relation_h005.py`, `tools/use_relation_h005.py`, `tests/test_use_relation_h005.py`, `docs/workflows/use-relation-h005.md` and `docs/sources/use-relation-h005-review-fixes.md`, and where the `iter_references` patch it depends on is already applied to `src/minireason/graph_import_h005.py` and `tests/test_graph_import_h005.py` by REC-20260914-Q.

# `use_relation_h005` — design notes

Proposal **P1** of the FW5-versus-harness-spec review, mechanical half only.
The review's P1 asks for an instrument that, for each cross-document
reference, "record[s] whether the later node's *content* re-deploys,
qualifies, rejects-with-reason, repairs or retains the earlier content, citing
the passage; record[s] declared `uptake` and its divergences separately", with
"no scoring", evidence being "a passage-level correspondence a reader can
check", and a ceiling of "a declared, witnessed-by-reading relation, never
FW5:628's witness". P1 is also marked **root-only to read**.

That splits cleanly. The recording of *whether* is root's; the *juxtaposition*
that makes the recording possible is mechanical and delegable. This module
builds the juxtaposition and leaves four empty cells where the recording goes.
It is the whole of the delegable half and deliberately not one step more.

## 1. What it is

`build_use_table(occurrence_dir, *, problems=None, arms=None, cycles=None) ->
UseTable`. One row per authored cross-document reference; one section per
FCL-1 document comparing declared `uptake` against the records present; one
per-occurrence residue of refs that resolve to nothing; a `method` block that
states every mechanical rule in words; and `files_read`, the sha256 of every
byte the instrument touched.

Standing invariants are U1–U7 in the module docstring. U6 and U7 are the ones
that make it P1 rather than something else: the tool classifies nothing, and
the reading is root's.

### The four empty cells

`root_reading`, `root_passage_cited`, `root_notes`, `root_initials_date`.
`ROOT_READING_VOCABULARY` publishes the six legal values of the first — the
five the review names, plus `unresolved`, which FW5:634 makes a legal value
rather than a failure to complete the form. No code path in the module writes
any of the four; a test asserts all four are `""` in every row of every
scope tested.

A **blank cell is an unread row**, not an `unresolved` verdict. The workflow
doc says so, because conflating the two would let an unfinished worksheet read
as a finding of indeterminacy — exactly the move FW5:688 ("non-evaluability is
not refutation") forbids in the other direction.

### Why the lexical column exists at all, given that it proves nothing

Because root has to find the passage. The review's P1 wants "a passage-level
correspondence a reader can check", and a 4,000-character body is not a
passage. The overlap rule is a *finding aid*: it narrows ~30 sentences to a
handful and quotes them with offsets so that root can read the candidates and
then cite whatever passage actually matters, including one the rule missed.
Its output is labelled in the table, twice, as not being evidence of use —
FCL-1's own "not automatically inferred from citation or lexical overlap",
plus FW5:628, :640, :1218/:1222 as summarised in review §1 R3–R4. The rule is
published in full (regexes, stopword list, thresholds) in every `USE_TABLE.md`
so that a reader can see exactly what was and was not searched — review §5 P7
("every negative finding states the set it was searched over") applied to the
instrument itself.

`distinctive_tokens_present` is per-sentence audit data, not a measure:
passages are listed in body order and nothing is selected, ordered or
thresholded by how many tokens a sentence carries.

### Verbatim means verbatim

`referring_record_verbatim` and `target_record_verbatim` are spans of the
authored `commitments` string, not re-serialisations: `record_source_spans()`
walks the top-level `records` array with `json.JSONDecoder.raw_decode`, and
every recovered span is verified to re-parse *equal* to the parsed record
before it is used. A disagreement raises `MappingError`; it never silently
falls back to `json.dumps`.

The offsets are **code point offsets into the decoded `commitments` string**
(Python string indices), which is what `split_sentences` says about its own
offsets and what the table now says in every header. They are *not* utf-8 byte
offsets, and they are *not* offsets into the artifact JSON file — `commitments`
is itself a JSON-escaped string *value* inside that file. `daily/mini_fcl/
cycle01/carry` already contains an en dash at code point 2869, so the two kinds
of offset differ by two for every later span, and a byte tool aimed at the file
would quote a plausible-looking but wrong slice.

The check that actually works, with the standard library and nothing of ours:

```python
import json
document = json.loads(open(ARTIFACT_JSON, encoding="utf-8").read())
print(document["commitments"][start:end])       # code points, not bytes
```

Equivalently in a shell, `python3 -c` around the same two lines. The
`method.span_offsets` line of `use_table.json` and the Method block of
`USE_TABLE.md` both say this.

## 2. What was reused from the importer

Nothing in parsing, schema validation, custody or reference resolution is
reimplemented. `minireason.graph_import_h005` is imported and driven up to —
and not past — the point at which it would start building a graph.

**Public API, used as published:**

| symbol | use |
|---|---|
| `verify_custody(reader, ledger)` | the whole custody gate; its return is the `plan`/`material` the scope discovery needs, and its ledger is rendered into `USE_TABLE.md` |
| `Coordinate` | the coordinate type, including its `key` spelling |
| `CustodyError`, `MappingError`, `SelectorMatchedNothing` | re-exported, so the CLI maps the same failure classes to the same exit codes |
| `parse_fcl1_document` / `fcl1_validator` | reached through `_Importer.parse_documents`; the FCL-1 schema and its out-of-schema local-name uniqueness rule are the importer's |

**Private API, wrapped — this is the disclosure the task asks for.** The
importer exposes its FCL-1 pipeline only as methods of the private
`_Importer`; there is no public "parse and resolve, don't build" entry point.
So this module constructs an `_Importer` and calls four private methods, in
the importer's own order:

| wrapped | why it is needed |
|---|---|
| `_Importer(occurrence_dir, problems, arms, cycles)` | owns the `_Reader` (path-confined, sha256-recording) and the `_CustodyLedger` |
| `_Importer.discover_scope(material, plan)` | the selector semantics, including `SelectorMatchedNothing` and its "what the occurrence actually holds" message |
| `_Importer.load_nodes(scope, plan)` | per-node custody, the brief/projection label index, and the hop-2 projection-source check |
| `_Importer.parse_documents()` | dispatch on the commitment surface: FCL-1 parsed, prose never parsed, empty/undecodable left opaque |
| `_Node` | the per-node record used by all of the above |

**Reference resolution is no longer wrapped at all.** It is the importer's own
**public** walk, added by `patches/graph_import_h005_iter_references.patch`:

| symbol | use |
|---|---|
| `iter_references(occurrence_dir, *, problems, arms, cycles)` | every authored ref in scope, resolved by the import's own custody, scope discovery, node loading, parsing, field order, wave-order availability and `resolve_ref`; yields frozen `ReferenceRecord`s |
| `UNRESOLVED_RESIDUE_CODES` / `EXTENSION_RESIDUE_CODES` | the import's own classification of what a residue code means for a ref, consumed rather than copied |
| `REF_FIELDS` | the import's own field order, printed in the output beside this table's display order |

The `_Node.spec_id` sentinel is **gone**. The resolver's hop-2 step
(`_projection_source`) used to gate on `_Node.spec_id` being non-empty — the
importer's proxy for "this owning node was already registered, in wave order" —
and this module used to write `"use-relation:in-scope"` into that field to keep
the gate meaningful. Two things were wrong with it. First, it was written
*after* the `document is None` check, so a node whose commitment surface was
prose or undecodable never got it, and a ref into such a node resolved
differently here than under the import: `ref_to_unregistered_target_dropped`
with the reason "outside the imported scope or is not registered yet in wave
order", which is false, where the import gives `ref_unresolved` with "the
owning artifact has no readable FCL-1 document". Second, the sentinel leaked:
`_Importer.add_residue` copies `node.spec_id or None` into every later residue
entry's `carrier.spec_artifact_id`, a field that everywhere else holds a
content-addressed spec artifact id. The patch replaces the gate with an
explicit availability predicate that `iter_references` fills in wave order for
every node, document or not; nothing of this module's is ever written into an
importer structure, and `tests/test_use_relation_h005.py` pins the equivalence
against a real `map_records` on the golden scope, the full occurrence, and a
synthetic scope in which an in-scope FCL node's surface does not decode while
it remains a projection source.

Every note the resolver attaches to a ref is carried through verbatim into the
row (`resolver_notes`) and into the residue, so the two extension-admitted
refs in the golden scope — the `#BODY` pseudo-local and the bare
exposed-artifact label — arrive with the importer's own reason text rather
than a restatement of it.

**Deliberately not used:** `import_occurrence`, `_Importer.map_records`,
`_map_content`, `_map_objections`, `_map_commitment`, `_mint_warrant`,
`_map_depends_refs`, `register`, `adjudicate_offline`, `build_att`,
`build_dep`, `label0`, `final_labels`, `Harness`, and every residue code that
describes a mapping decision. `map_records()` would have been the shortest
route to a full resolution pass, and it is exactly the wrong one: it mints
`_PlannedWarrant`s (att) and dependence edges as a side effect, which P1
forbids. Walking the refs directly costs ~40 lines and keeps the ban honest.

## 3. The row count, derived

The golden scope is `daily/mini_fcl/cycle01` — the five FCL-1 documents. Over
it, the resolver walks **84** authored refs and reports `82` under its
`resolved` counter, `2` admitted by extension, `0` dangling (the importer's
own `REPORT.md` prints "references: 82/84 resolved, 2 admitted by extension, 0
dangling"). Of the 84:

- **62** resolve to a record of the referring document itself — intra-document,
  no row;
- **0** resolve to the exposed task artifact — no row (that is a resolution to
  something that is not a contribution);
- **0** resolve to nothing;
- **22** resolve to another document — one row each.

`84 − 62 − 0 − 0 = 22`. Equivalently `82 − 62 = 20` strictly-resolved
cross-document refs, plus the 2 the resolver admitted by extension
(`rival.r1.mentions[0] = "e3647350a300c0ed#BODY"` and
`carry.n6.mentions[0] = "b998d514348ed94e"`), which the row spec includes
because both name another document. **22 rows.** By field: 20 `target`, 2
`mentions`. By referring node: objection 5, rival 1, response 8, carry 8.

`depends` contributes **zero** rows: all 17 `depends` refs in occurrence-01
are intra-document. `uptake` contributes zero rows for the same reason — all
of it is local. Both columns exist and are walked; neither is exercised by
this occurrence's data, which is itself worth knowing (review §3.1 reads the
same fact as "zero cross-document dependence in occurrence-01").

Declared uptake against records present: account 5/6 (`p1` omitted),
objection 6/8 (`o4`, `p1`), rival 4/11, response 9/9, carry 8/8 — the same
five ratios the review's §3.1 reports, recomputed here from the bytes.

## 4. Open questions

1. ~~**The `spec_id` sentinel is a shim.**~~ **Closed.** It was not merely a
   future risk: `_walk_refs` skipped `document is None` nodes *before* writing
   the sentinel, so the instrument and the import already resolved a ref into
   an unreadable-surface node differently, and the sentinel leaked into
   `residue[*].carrier.spec_artifact_id`. Both are gone. The fix is the one
   this entry asked for — an upstream walk taking an explicit "already
   available" predicate, which both callers use — and it ships as
   `patches/graph_import_h005_iter_references.patch` (`iter_references`), with
   no change to any importer output: the 79 existing importer tests stay green,
   six more are added, and a full-occurrence graph root built with and without
   the patch is byte-identical.

2. **The distinctive-token rule is scope-dependent** — clause (3) counts
   document frequency over the in-scope FCL-1 documents. Re-running over a
   different partition can change which tokens count, and therefore which
   passages are surfaced. `use_table.json` names its corpus so the question is
   answerable, but review §5 P5 asks for more than answerability: it asks
   whether *root's reading* survives re-partition. That comparison needs two
   grain variants and a second reading, and is not this deliverable.

3. **Whether the threshold is the right one is untested.** `max(2, N // 2)`
   was chosen after measuring: over the golden scope it surfaces 1–14
   sentences per row (mean ≈ 4.6) out of bodies of 20–37 sentences, with no
   empty row. A length-and-stopword rule alone surfaced ≈ 14 of ~30, which is
   not a finding aid. That is a usability argument, not a principled one, and
   it is recorded as such.

4. **A `#BODY` or bare-label ref has no target record**, so the overlap
   subject falls back to the prose of *every* record of the owning document.
   The `#BODY` header arguably names the owning artifact's `body`, not its
   commitments; comparing against that instead would be equally mechanical and
   would give a different passage set. The row states which subject was used;
   the choice is open.

5. **No read-back.** Once root fills the cells, nothing validates them — that
   `root_reading` is in the vocabulary, that `root_passage_cited` resolves to
   a real offset in a named coordinate, that a filled row is signed. A small
   validator that checks the form of a completed table *without interpreting
   it* would be a natural follow-up and would keep the ban intact.

6. **Record grain, not spec grain.** This table addresses records
   (`<coordinate>#<record>`), which review §CU-4 notes the spec has no address
   for and the repo's import discarded. The instrument shows that the
   record-grain relation is present in the material; it proposes no spec
   change, and it should not be read as one.

7. **Nothing here approaches FW5:630.** There is no content-changing case, no
   content-preserving recoding and no carrier disturbance, because a frozen
   transcript contains none. That is P2/P3 and needs new runs; a completed row
   is "consistent-with", never a witness.

## 5. Layout

```
src/minireason/use_relation_h005.py   library
tools/use_relation_h005.py            CLI
tests/test_use_relation_h005.py       unittest, against the in-repo occurrence
docs/workflows/use-relation-h005.md   workflow doc, with the banner
NOTES.md                              this file
```

`src/minireason/__init__.py` in this staging tree is a **shim** (`pkgutil.
extend_path`) and must not be published: it exists only so the tree can run
with `PYTHONPATH=<use-relation>/src:<importer>/src:/home/user/miniReason/src`
while `graph_import_h005` lives in the repository package. When
`use_relation_h005.py` moves into `src/minireason/`, the shim is dropped and
the repository's own `__init__.py` is kept unchanged.

Run:

```
PYTHONPATH=<use-relation>/src:/home/user/miniReason/src \
  python -X utf8 -m unittest discover -s <use-relation>/tests -v
```

(The `<importer>/src` entry is unnecessary while the repository copy of
`graph_import_h005.py` is byte-identical to the staged one, which it is; add
it first if the two ever diverge and the staged copy is the one under test.)

## 6. Review closure (2026-09-14)

`FIXES.md` maps every finding of the four-lens review — all severities — to the
change that closes it and the test that pins it. Three of them move the
artifact root reads: the two caveats (a blank cell is an unread row, not an
`unresolved` reading; the listed passages are a finding aid, not a search
space) are now emitted into `USE_TABLE.md`'s Method block and beside every
per-row root table rather than living only in the workflow doc; the span
offsets are described as code point offsets everywhere, with a verification
recipe that works; and `root_reading`'s vocabulary is published as a suggestion
rather than as a closed single-valued enum.

The instrument also no longer writes into the occurrence: `write_use_table`
refuses a destination that is the occurrence or inside it
(`OUT_DIR_INSIDE_OCCURRENCE`), as U1 always said and as the published importer
already did, and the CLI refuses it before a single occurrence byte is read.
