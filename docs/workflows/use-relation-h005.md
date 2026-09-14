> Published verbatim, body unedited: written against the staging tree, so the `NOTES.md` it cites is published here as [`docs/design/use-relation-h005-notes-2026-09-14.md`](../design/use-relation-h005-notes-2026-09-14.md), its review closure as [`docs/sources/use-relation-h005-review-fixes.md`](../sources/use-relation-h005-review-fixes.md), the review it builds on as [`docs/reviews/fw5-vs-harness-spec-2026-09-14.md`](../reviews/fw5-vs-harness-spec-2026-09-14.md), and the `patches/graph_import_h005_iter_references.patch` prerequisite named under Tests is already applied in this repository by REC-20260914-Q -- run `PYTHONPATH=src python -X utf8 -m unittest tests.test_use_relation_h005` with no patch step.

# H005 use-relation table

> **The tool records juxtapositions; the reading is root's.** This table places each authored cross-document reference beside the passages a root reader needs and stops there. It scores nothing, ranks nothing, classifies nothing and mints no relation of its own; it has no `att`, no `dep`, no status and no label. **A lexical overlap is not evidence of use.** FCL-1's own rule is that `depends` and `mentions` are "not automatically inferred from citation or lexical overlap"; a witness of reason use "must preserve internal role bindings, not merely the endpoint string" (FW5:628); actual use is "not automatically machine-maintainable" while prompt appearance is only a delivery fact (FW5:640); and no function of an input-output projection agrees with the accounting predicate across models differing in active route (FW5:1218), "semantic use inferred from delivery logs" included (FW5:1222) - all as summarised in the FW5-versus-harness-spec review, `fw5-vs-harness-spec-review.md` §1 R2-R4, §3.1 and §5 P1/P6. Root fills the four empty cells by reading; `unresolved` is a legal value and stays unresolved (FW5:634).

Read [the decision ledger](../DECISION_LEDGER.md), [STATUS](../STATUS.md) and
[the experiment workflow](experiment.md) first. This route builds proposal P1
of the FW5-versus-harness-spec review: a **use-relation instrument** over one
frozen H005 occurrence. It adds no evidence and produces no finding. It
produces a worksheet, and the worksheet is only finished once root has read it.

## What it does

```
python tools/use_relation_h005.py <occurrence-dir> <out-dir> \
    [--problem daily] [--arm mini_fcl] [--cycle 1]
```

reads one occurrence directory and writes one **new** directory containing
`USE_TABLE.md` and `use_table.json`. The library entry point is
`minireason.use_relation_h005.build_use_table(occurrence_dir, *, problems=None,
arms=None, cycles=None) -> UseTable` (a frozen dataclass with `to_json()` and
`to_markdown()`); `write_use_table(table, out_dir)` is the writer.

For every FCL-1 document in scope, and for **each** reference that document
makes to another document's record — `target`, `depends`, `mentions`,
`revises`, `withdraws` and the document-level `uptake` list, including a bare
exposed-artifact label and the `#BODY` section header — the table emits one row
carrying:

- the referring coordinate, the referring record's id and type, and that
  record **verbatim**, as the exact byte span of the authored `commitments`
  string (`commitments[start:end]`, and the span is printed);
- the ref field and the ref exactly as written;
- the resolved target coordinate, record id and type, and that record verbatim
  on the same terms;
- the sentences of the **referring node's `body`** that carry at least one
  distinctive token of the target record's text, quoted verbatim with their
  character offsets into that body — or `no lexical overlap found`;
- `declared_uptake_includes_referring_record` and
  `declared_uptake_includes_target_record`, read off the two documents' own
  `uptake` lists;
- four **empty** cells: `root_reading`, `root_passage_cited`, `root_notes`,
  `root_initials_date`.

It also emits, per document, the declared `uptake` against the records
actually present — records in uptake, records omitted from uptake, uptake
entries naming nothing, uptake entries naming another document — and, per
occurrence, a residue listing every authored ref that resolves to nothing.

"Distinctive token" is mechanical and published in full in every
`USE_TABLE.md`: a token (a maximal run of ASCII letters/digits in the
lowercased string) of the target record's prose fields (`text`, `scope`,
`action`, `consequence`, `grounds`, `bearing`; `id`, `type` and ref arrays
excluded) that is at least 5 characters long, is not in the closed stopword
list frozen in the module, and occurs in the record prose of at most
`max(2, in_scope_FCL-1_documents // 2)` of the in-scope documents. Clause
three makes the criterion scope-dependent, and `use_table.json` names the
corpus it used so that a re-partition question (review §5 P5) is answerable
from the output. Sentences are cut at one published regular expression and
nowhere else — this is not linguistic segmentation: `"1."` does not split and
`"e.g."` does.

Parsing, schema validation, custody verification and two-hop reference
resolution are the importer's, imported from
`minireason.graph_import_h005` and driven no further than the point at which
the importer would begin building a graph. See NOTES.md.

## What it does NOT do

- **No reading.** The instrument records juxtapositions; the reading is root's.
  Every interpretive cell is emitted empty and no code path writes one.
- **A lexical overlap is not evidence of use**, and the absence of one is not
  evidence of non-use. FCL-1's own rule is that `depends` and `mentions` are
  "not automatically inferred from citation or lexical overlap"; the review's
  R3 reads FW5:628 as requiring a witness that "must preserve internal role
  bindings, not merely the endpoint string"; R4 reads FW5:640 as saying actual
  use is "not automatically machine-maintainable" while prompt appearance is
  only a delivery fact; R10 reads FW5:1218 as denying that any function of an
  input–output projection agrees with the accounting predicate across models
  differing in active route, "semantic use inferred from delivery logs"
  included (FW5:1222). A transcript supplies no active-route map.
- **No scoring, ranking or classification.** There is no score, rank, merit,
  status or label anywhere in the output, and a test asserts that no key with
  any of those names exists in `use_table.json`. Rows are in document order,
  never ordered by overlap. `distinctive_tokens_present` is an audit aid so a
  reader can see why a sentence was listed; nothing is selected by it.
- **No `att`, no `dep`, no graph, no adjudicator, no provider.** Nothing is
  registered, no edge is minted, no label is computed and no network call is
  made.
- **Nothing is inferred.** A relation appears only because an author wrote a
  ref in a ref-valued FCL-1 field.
- **Prose is never mined.** A node whose commitment surface is prose is listed
  as `commitment surface: prose (not parsed); references not extractable by
  this instrument`, and no extraction is attempted. A node whose commitments
  string failed to decode is listed the same way under its own surface state,
  which is **unavailable, not absent** — see the importer's workflow doc.
- **No writes into the occurrence.** The occurrence is opened through the
  importer's path-confined reader; the output directory is created with
  `exist_ok=False`. Every file read is listed with its sha256 in the output.

## How root fills the four cells

Read the row: the referring record, the target record, and the passages. Then
write, in the row's own four cells (in `USE_TABLE.md`, or in the JSON if the
table is being annotated in place):

| cell | what goes in it |
|---|---|
| `root_reading` | one or more of the suggested vocabulary — `re-deploys`, `qualifies`, `rejects-with-reason`, `repairs`, `retains`, `unresolved`. It is a **suggested range**, not a closed single-valued enum: review §5 P1 names five relations without saying a row carries only one, and a record can concede one point while repairing another. `unresolved` is legal and stays unresolved (FW5:634). Root may also write a reading the vocabulary does not cover, and should say so. Nothing about this is enforced in code. |
| `root_passage_cited` | the passage the reading rests on, cited as `body[start:end]` of a named coordinate, or `<coordinate>#<record>` — a citation a second reader can check |
| `root_notes` | why that reading and not the neighbouring one; what would change it |
| `root_initials_date` | who read it, and when |

The passages the instrument lists are a starting point, not the search space:
root may cite any passage of either contribution, including one the overlap
rule did not surface. A cell left blank is not an `unresolved` verdict — it is
an unread row, and the two must not be conflated.

**Both of these now travel with the artifact.** They are emitted into
`USE_TABLE.md`'s Method block and repeated above every per-row "Reserved for
root" table, because they are load-bearing for a reader who has the table and
not this page.

Offsets in the table — record spans and passage spans alike — are **code point
offsets into the decoded `commitments` (or `body`) string**, not utf-8 byte
offsets and not offsets into the artifact JSON file. To check a quote: decode
the artifact JSON, take the string value, slice it by code point. The Method
block says so and prints the two regular expressions verbatim, so the markdown
alone is enough to re-derive every passage.

## Claim ceiling

What a completed row can support is **a declared, witnessed-by-reading
relation between two authored passages** — and nothing more. It is never
FW5:628's witness of reason use: a transcript supplies no active-route map, no
role-binding correspondence and no three-case contrast (FW5:630), and this
instrument runs none. `unresolved` is a legal value of `root_reading` and an
unresolved cell **stays** unresolved (FW5:634); the absence of data is not a
negative finding, and "non-evaluability is not refutation" (FW5:688, review
R5). Counts in the table's totals section are information, never a warrant:
FW5:851 outlaws a count entering as an *automatic* warrant, not counts as
information. Nothing here bears on FCL-1's merit, on Mini, or on any
contribution's value; that reading is root's alone (PROTOCOL.md
§Interpretation: "Root alone reviews substantive outputs").

## Exit codes

| code | meaning |
|---|---|
| 0 | the table was written |
| 2 | `CUSTODY_REFUSED` — the occurrence failed a custody check (a missing or malformed occurrence file included); nothing was written |
| 3 | `BUILD_FAILED` — well-custodied, but the table could not be built (`EMPTY_SCOPE` is one of these) |
| 4 | `OUT_DIR_REFUSED` — the destination is inside the occurrence, or already exists, or could not be written (an `OSError`: permissions, ENOSPC); name a different one. Nothing under the occurrence is ever written (U1), and a failed write leaves no partial output directory behind |
| 5 | `SELECTOR_MATCHED_NOTHING` — `--problem/--arm/--cycle` matched none of the occurrence's coordinates; stderr lists what it holds |

## Tests

The instrument consumes the importer's **public** reference walk,
`graph_import_h005.iter_references`, which ships as
`patches/graph_import_h005_iter_references.patch` in this staging tree. Apply
that patch (or put a patched checkout first on `PYTHONPATH`) before running:

```
PYTHONPATH=<use-relation>/src:<patched-repo>/src \
  python -X utf8 -m unittest discover -s <use-relation>/tests -v
```

The suite runs against the in-repo occurrence and **fails** if it is absent;
`H005_IMPORT_ALLOW_SKIP=1` skips it deliberately, with a message saying that a
skipped run has checked nothing. `H005_OCCURRENCE` overrides the location.
