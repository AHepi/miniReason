# Use-relation table - H005 occurrence-08

**The tool records juxtapositions; the reading is root's.** This table places each authored cross-document reference beside passages a root reader may find worth starting from - a finding aid, never a closed search space - and stops there. It scores nothing, ranks nothing, classifies nothing and mints no relation of its own; it has no `att`, no `dep`, no status and no label. **A lexical overlap is not evidence of use.** FCL-1's own rule is that `depends` and `mentions` are "not automatically inferred from citation or lexical overlap"; a witness of reason use "must preserve internal role bindings, not merely the endpoint string" (FW5:628); actual use is "not automatically machine-maintainable" while prompt appearance is only a delivery fact (FW5:640); and no function of an input-output projection agrees with the accounting predicate across models differing in active route (FW5:1218), "semantic use inferred from delivery logs" included (FW5:1222) - all as summarised in the FW5-versus-harness-spec review, `fw5-vs-harness-spec-review.md` §1 R2-R4, §3.1 and §5 P1/P6. Root fills the four empty cells by reading; `unresolved` is a legal value and stays unresolved (FW5:634). An empty cell is an **unread row**, not a reading of `unresolved`.

Instrument: `use_relation_h005/1`. Schema: `h005-use-relation.use-table.v1`.

## Scope

- `daily/bare/cycle01/answer`
- `daily/mini_fcl/cycle01/account`
- `daily/mini_prose/cycle01/account`
- `daily/mini_fcl/cycle01/objection`
- `daily/mini_prose/cycle01/objection`
- `daily/mini_fcl/cycle01/rival`
- `daily/mini_prose/cycle01/rival`
- `daily/mini_fcl/cycle01/response`
- `daily/mini_prose/cycle01/response`
- `daily/mini_prose/cycle01/carry`

## Custody

- `plan_id`: `04c26f24812a4e48d41cfd6f6ef16785ba25ea183894bfafe86d6eb0e35af8ee`
- `material_sha256`: `8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff`

| check | kind | result |
|---|---|---|
| `material_pin` | cross_file | verified (1/1 occurrence) |
| `manifest_pins` | cross_file | verified (3/3 manifests) |
| `receipt_present` | cross_file | verified (10/10 nodes) |
| `artifact_bytes_vs_receipt` | cross_file | verified (10/10 nodes) |
| `status_vs_receipt` | cross_file | verified (10/10 nodes) |
| `public_text` | cross_file | verified (10/10 nodes) |
| `attempt_vs_receipt` | cross_file | verified (10/10 nodes) |
| `request_record` | cross_file | verified (10/10 nodes) |
| `trace_pinned` | cross_file | verified (10/10 nodes) |
| `provider_bytes` | cross_file | verified (10/10 nodes) |
| `wave_placement` | cross_file | verified (10/10 nodes) |
| `projection_source` | cross_file | verified (13/16 projections; 3 projection(s) had no exposed source (the slot is absent): `daily/mini_fcl/cycle01/account#p.account.0`, `daily/mini_prose/cycle01/account#p.account.0`, `daily/mini_prose/cycle01/carry#p.carry.3`) |
| `plan_identity` | self_consistency | verified (1/1 occurrence) |
| `artifact_self_hash` | self_consistency | verified (10/10 nodes) |
| `artifact_coordinate` | self_consistency | verified (10/10 nodes) |
| `brief_pinned` | self_consistency | verified (10/10 nodes) |
| `brief_label_index` | self_consistency | verified (10/10 nodes) |
| `task_label` | self_consistency | verified (10/10 nodes) |

Custody is the importer's own check, reused unchanged; a self-consistency check cannot detect a coherent rewrite of the one file it reads.

## Method - exactly what the mechanical columns mean

**Sentence.** The referring node's `body` is cut at every match of the published boundary regular expression and nowhere else; leading and trailing whitespace is trimmed out of each span *and out of its offsets*, so `body[start:end]` is exactly the quoted sentence. The boundary is one or more of `.` `!` `?` preceded by a lowercase letter or a closing bracket/quote and followed by whitespace or end-of-string, together with any closing quotes that follow it; or a run of newlines. This is not linguistic sentence segmentation: a numbered list marker ("1. Separate ...") does not split, and an abbreviation such as "e.g." does.

**Token.** The string is lowercased and every maximal run of ASCII letters and digits is a token, in order of occurrence.

**The target record's text.** The concatenation, separated by single spaces, of the target record's prose fields in this order: `text`, `scope`, `action`, `consequence`, `grounds`, `bearing`. `id`, `type` and every ref array are excluded: they are names and pointers, not content. When the ref names the owning contribution as a whole rather than one of its records - a bare exposed-artifact label, or the `#BODY` section header - the subject is instead the same concatenation over **every** record of the owning document, in document order, and the row says so in `overlap_subject`.

**Distinctive token.** A token `t` of the target record's text is *distinctive* when all three hold: (1) `len(t) >= 5` characters after lowercasing; (2) `t` is not in the closed stopword list below; (3) `document_frequency(t) <= 2`, where `document_frequency(t)` is the number of in-scope FCL-1 documents whose record prose contains `t`, and the threshold is `max(2, number_of_in_scope_FCL-1_documents // 2)` - here `max(2, 3 // 2)`. Clause (3) makes the criterion **scope-dependent**: it is computed over the documents listed under `corpus_documents`, and re-running over a different scope can change which tokens count. That is stated rather than hidden, because a partition-invariance question about this instrument (review §5 P5) has to be answerable from its own output.

**A passage is listed** when the sentence contains at least one distinctive token of the target record's text. Passages are listed in body order, never ordered or selected by how many tokens they carry; `distinctive_tokens_present` is an audit aid so a reader can see *why* a sentence was listed, and is not a measure. When no sentence qualifies the row says `no lexical overlap found`.

**What a listed passage is not.** It is not evidence that the referring node used the target's content, and its absence is not evidence that it did not. Shared vocabulary is shared vocabulary. The relation columns of this table report what an author *wrote* in a ref-valued field; the passage columns report what a mechanical string comparison found; neither is a reading, and the four `root_*` cells are where a reading would go.

**Declared uptake columns.** `declared_uptake_includes_referring_record` is true when the referring record's local name is in its own document's `uptake` list; `declared_uptake_includes_target_record` is true when the target record's local name is in the *target* document's `uptake` list. `n/a` means the row has no such record to look up (a document-level `uptake` ref has no referring record; a ref to a whole contribution has no target record).

**What a blank root cell means.** An empty `root_reading`, `root_passage_cited`, `root_notes` or `root_initials_date` is an **unread row**: nobody has read it yet. It is *not* a reading of `unresolved`, and it is not a finding of indeterminacy. `unresolved` is a reading root may write, deliberately, and it then stays unresolved (FW5:634); a blank cell asserts nothing at all. Conflating the two would let an unfinished worksheet read as a finding, which is exactly the move FW5:688 forbids.

**What the listed passages are.** A finding aid, not a search space. The overlap rule is mechanical and shallow; root may cite **any** passage of either contribution, including one this rule did not surface, and a row with `no lexical overlap found` is not a row with nothing to read. `root_passage_cited` is free text for that reason.

**The `root_reading` vocabulary is a suggestion.** The six values below are published so that two readers of two tables mean the same thing by the same word, not to constrain root to one of them: a row may carry more than one, and root may write a reading the vocabulary does not cover and say so. Nothing about it is enforced in code.

Stopword list (closed, frozen in the module):

> `about`, `above`, `across`, `after`, `again`, `against`, `almost`, `alone`, `along`, `already`, `also`, `although`, `always`, `among`, `another`, `anyone`, `anything`, `around`, `because`, `become`, `becomes`, `before`, `begin`, `behind`, `being`, `below`, `beside`, `better`, `between`, `beyond`, `cannot`, `could`, `does`, `doing`, `done`, `during`, `each`, `either`, `enough`, `equally`, `especially`, `even`, `every`, `everything`, `except`, `exist`, `exists`, `first`, `from`, `further`, `given`, `goes`, `going`, `gone`, `hardly`, `have`, `having`, `hence`, `here`, `however`, `inside`, `instead`, `into`, `itself`, `just`, `keep`, `kept`, `later`, `least`, `less`, `like`, `likely`, `made`, `make`, `makes`, `making`, `many`, `maybe`, `might`, `more`, `most`, `much`, `must`, `near`, `need`, `needs`, `neither`, `never`, `next`, `nobody`, `none`, `nothing`, `often`, `once`, `only`, `onto`, `other`, `others`, `ought`, `over`, `perhaps`, `quite`, `rather`, `really`, `same`, `seem`, `seems`, `seen`, `several`, `shall`, `should`, `simply`, `since`, `some`, `something`, `sometimes`, `still`, `such`, `take`, `taken`, `than`, `that`, `their`, `them`, `themselves`, `then`, `there`, `therefore`, `these`, `they`, `thing`, `things`, `think`, `this`, `those`, `though`, `three`, `through`, `thus`, `together`, `toward`, `under`, `unless`, `until`, `upon`, `very`, `well`, `were`, `what`, `when`, `where`, `whether`, `which`, `while`, `whole`, `whom`, `whose`, `will`, `with`, `within`, `without`, `would`, `your`, `yours`

The two regular expressions, verbatim, so this page alone is enough to re-derive every passage:

| rule | pattern |
|---|---|
| `token_regex` | `[a-z0-9]+` |
| `sentence_boundary_regex` | `(?<=[a-z\)\]’'"])[.!?]+["'\)\]”]*(?=\s|$)|
+` |

Offsets: code point offsets into the decoded `commitments` string (Python string indices), not utf-8 byte offsets and not offsets into the artifact JSON file. To check a quote: decode the artifact JSON, take the `commitments` (or `body`) string value, and slice it by code point - a byte tool pointed at the file will not agree wherever a non-ASCII character precedes the span.

Resolution order (the importer's own): `mentions`, `revises`, `withdraws`, `target`, `depends`, `uptake`, `target (objection, pass 2)`. Display order in this table: `target`, `depends`, `mentions`, `revises`, `withdraws`, `uptake`.

`root_reading` has a suggested vocabulary: `re-deploys`, `qualifies`, `rejects-with-reason`, `repairs`, `retains`, `unresolved`. A row may carry more than one, and root may write a reading this vocabulary does not cover and say so; `unresolved` is legal and stays unresolved. The instrument never selects one.

## Reference totals

| quantity | count |
|---|---|
| refs walked | 66 |
| cross document rows | 0 |
| intra document | 30 |
| refs to exposed task artifact | 0 |
| unresolved | 36 |
| importer resolved counter | 30 |
| importer extension counter | 0 |
| importer dangling counter | 36 |

These are counts of authored refs, reported as information. No count here warrants anything (FW5:851: counts "are not outlawed as information"; what is forbidden is a count entering as an *automatic* warrant).

## Rows

*No cross-document reference in scope.*

## Declared uptake versus records present

### `daily/mini_fcl/cycle01/account`

- commitment surface: `read_fcl1`
- records present (8): `a1`, `a2`, `a3`, `a4`, `a5`, `a6`, `a7`, `a8`
- declared `uptake` (4): `a4`, `a5`, `a6`, `a7`
- records in uptake (4): `a4`, `a5`, `a6`, `a7`
- records omitted from uptake (4): `a1`, `a2`, `a3`, `a8`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/objection`

- commitment surface: `read_fcl1`
- records present (7): `b1`, `b2`, `b3`, `b4`, `b5`, `b6`, `b7`
- declared `uptake` (6): `b1`, `b2`, `b3`, `b4`, `b5`, `b7`
- records in uptake (6): `b1`, `b2`, `b3`, `b4`, `b5`, `b7`
- records omitted from uptake (1): `b6`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/response`

- commitment surface: `read_fcl1`
- records present (9): `d1`, `d2`, `d3`, `d4`, `d5`, `d6`, `d7`, `d8`, `d9`
- declared `uptake` (9): `d1`, `d2`, `d3`, `d4`, `d5`, `d6`, `d7`, `d8`, `d9`
- records in uptake (9): `d1`, `d2`, `d3`, `d4`, `d5`, `d6`, `d7`, `d8`, `d9`
- records omitted from uptake (0): *none*
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

## Nodes whose commitment surface was not read

- `daily/bare/cycle01/answer` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_prose/cycle01/account` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_prose/cycle01/objection` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_fcl/cycle01/rival` - commitment surface: schema_failure; references not extractable by this instrument
- `daily/mini_prose/cycle01/rival` - commitment surface: unavailable_decode_failure; references not extractable by this instrument
- `daily/mini_prose/cycle01/response` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_prose/cycle01/carry` - commitment surface: prose (not parsed); references not extractable by this instrument

## Residue: refs that resolve to nothing

| referring coordinate | record | field | ref | code | reason |
|---|---|---|---|---|---|
| `daily/mini_fcl/cycle01/objection` | `b7` | `target` | `h005.fork5.p.objection.0#a4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `b7` | `target` | `h005.fork5.p.objection.0#a5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `b1` | `target` | `h005.fork5.p.objection.0#a1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `b1` | `target` | `h005.fork5.p.objection.0#a4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `b2` | `target` | `h005.fork5.p.objection.0#a5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `b2` | `target` | `h005.fork5.p.objection.0#a3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `b3` | `target` | `h005.fork5.p.objection.0#a4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `b3` | `target` | `h005.fork5.p.objection.0#a5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `b3` | `target` | `h005.fork5.p.objection.0#a6` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `b4` | `target` | `h005.fork5.p.objection.0#a4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `b5` | `target` | `h005.fork5.p.objection.0#a1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `b5` | `target` | `h005.fork5.p.objection.0#a4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d1` | `revises` | `h005.fork5.p.response.0#a4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d1` | `depends` | `h005.fork5.p.response.1#b4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d1` | `depends` | `h005.fork5.p.response.1#b5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d1` | `depends` | `h005.fork5.p.response.2#m2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d1` | `depends` | `h005.fork5.p.response.2#o1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d3` | `depends` | `h005.fork5.p.response.1#b1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d3` | `depends` | `h005.fork5.p.response.1#b6` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d4` | `mentions` | `h005.fork5.p.response.0#a7` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d4` | `depends` | `h005.fork5.p.response.2#c2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d4` | `depends` | `h005.fork5.p.response.2#c3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d4` | `depends` | `h005.fork5.p.response.1#b7` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d4` | `depends` | `h005.fork5.p.response.2#q2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d5` | `revises` | `h005.fork5.p.response.0#a5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d5` | `depends` | `h005.fork5.p.response.1#b2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d5` | `depends` | `h005.fork5.p.response.2#o2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d6` | `depends` | `h005.fork5.p.response.1#b3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d6` | `depends` | `h005.fork5.p.response.2#c1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d8` | `mentions` | `h005.fork5.p.response.2#u1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d8` | `target` | `h005.fork5.p.response.0#a6` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d8` | `target` | `h005.fork5.p.response.0#a8` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d9` | `depends` | `h005.fork5.p.response.2#q1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d9` | `depends` | `h005.fork5.p.response.2#q2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d9` | `depends` | `h005.fork5.p.response.1#b6` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `d7` | `target` | `h005.fork5.p.response.2#m1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |

## Files read

Every byte this instrument read, with its sha256. Nothing under the occurrence was written.

| path | sha256 |
|---|---|
| `artifacts/daily/bare/cycle01/answer.json` | `2b9d51b870073f2fd1395027af01eb466207db016ac475e55ccdbcb73df50a32` |
| `artifacts/daily/mini_fcl/cycle01/account.json` | `1c9c81fec4eaecb74a13684d92293a1a8b7fb1c545195e525982045d920d2a75` |
| `artifacts/daily/mini_fcl/cycle01/objection.json` | `b74c3351c02ee4f98590cce6cd984be6d87d88e370dde7d778921a6fe2b87907` |
| `artifacts/daily/mini_fcl/cycle01/response.json` | `2324e79a0a3739e2d57691df66124b9f64444b0c27192b4f15a6c4d7647e3770` |
| `artifacts/daily/mini_fcl/cycle01/rival.json` | `313c6e0876cb4be25b9b0c8b76fcabfc825d0c3ee56b9264d4bda6acac6f58ad` |
| `artifacts/daily/mini_prose/cycle01/account.json` | `e91563ae39a2679e03342edbb5d6d13cc8da753cbcc3a17e3a93cfdd8ef0b46d` |
| `artifacts/daily/mini_prose/cycle01/carry.json` | `a92dec0e7cf88e32694d11395eb2669550f999875cae0d3d0bfccc6ecc7820d8` |
| `artifacts/daily/mini_prose/cycle01/objection.json` | `f4918bfbc72a19806a8fee7b4b8389a6d8e27b8db0c1f438848b2efa702ee306` |
| `artifacts/daily/mini_prose/cycle01/response.json` | `8d72427bb0cc42f61db62dfd6e263c6ab73db6c95525a589b052cf6095a72c49` |
| `artifacts/daily/mini_prose/cycle01/rival.json` | `b7fd76b43708ffbf5419a1db7d65c4e302d5ff37505157655cff10134252bcd7` |
| `attempts/daily/bare/cycle01/answer.json` | `be9f6d1970c3be87c7c03a6f6b89dd93647901a530362c8c6b06ea76bc76206e` |
| `attempts/daily/mini_fcl/cycle01/account.json` | `c5a307a6afcaa5a3bc239e0902ef95acc1b72eec628542af03c4be0bf3e2e2f1` |
| `attempts/daily/mini_fcl/cycle01/objection.json` | `47d9a95378b3ef64cca29e45adef5bdbd2b0a7e9821a154f7284ec2d0b168b64` |
| `attempts/daily/mini_fcl/cycle01/response.json` | `285f01efbd69ee918943fd6086b09a1f6917d1f9122d184fb80b7fb0f49725e3` |
| `attempts/daily/mini_fcl/cycle01/rival.json` | `2bee06b9f2df1e8ec74f8d00315e319fa30aeba24f2cb48d24219d5a20e1c625` |
| `attempts/daily/mini_prose/cycle01/account.json` | `820356e66eddc99616a907ae73195f910feeabcdfb38d36c2794d9eb6acb5add` |
| `attempts/daily/mini_prose/cycle01/carry.json` | `2021c5c9381a8fc0649c96bf9c3abf162c34a3d30a4ecdb2094d11b7d753c363` |
| `attempts/daily/mini_prose/cycle01/objection.json` | `3ab78fb28ebb9c0021a86c40266f6bebeb036b4aa9bddbb2d2b79717fa81d57c` |
| `attempts/daily/mini_prose/cycle01/response.json` | `abe6dbdd468755d642715523c528764e1590d725d816a5698c4dd0e66b81fba4` |
| `attempts/daily/mini_prose/cycle01/rival.json` | `cd8bf6ff85b9a0b34a8541e8f2d006fe252ac160622d28677a30cdea6a0258b2` |
| `manifests/fork5.json` | `8f2d928b2f70298906b17d62e73b41804efa754d845f018d9eb312af7dcb536a` |
| `manifests/return6.json` | `bad1f6dc4ddda462f1b3acaa56a9e552eeb98255509cb4bfa3353c2305abb3b5` |
| `manifests/weave7.json` | `0b8a5f337f754b23fd51721ff287e25347af99648a7d2b00ad73b7baa571c2cb` |
| `material.json` | `8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff` |
| `plan.json` | `028c551106cc37c6f568fe559c79e784abe7c849f5372447291e22216e61a5f2` |
| `provider/daily/bare/cycle01/answer/call-0001.request.json` | `d5fc7cba5cc2231b7cb63800e22fc10a135298348c8368f50152decc7bf90687` |
| `provider/daily/bare/cycle01/answer/call-0001.response.json` | `8422ab5bab4eb48b58aa88cca9d1d8415c7c99c2186a2f105855b421e2581819` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | `04e4321a4458b2c27090148e3e17d5adce7f3492bb1d9444ae67408bef36d5cd` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | `506e6a0fa9bfab632526f631922f69ce9440bb5d22c7515f4694788f1a660c24` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.request.json` | `369192df0f7c12e8ea0f1cc5e10ae5208f9fd0b339e52932d1e2668e94c161f0` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.response.json` | `2ff8e680eb38360670b8bbf3f95fba756dfc37080a2d9f28530cb40200e821d8` |
| `provider/daily/mini_fcl/cycle01/response/call-0001.request.json` | `2eff0bcd4acf2e3ecc630c41822a21ae04a96f8623f15ebec05b526650ac15a5` |
| `provider/daily/mini_fcl/cycle01/response/call-0001.response.json` | `0a4115d9a2e36e70d862d36f80e23252870426d2993966cc50563c0293a849ff` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | `77bd2d703b772bcdacd3f5f09da9bd5f6dc132b0f5c93ad9009cf4d4b03cf687` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | `87bddf601599f498bc27b70f3846d3b6cac8cb3f5a9bc68e3faed6f8c13c0d01` |
| `provider/daily/mini_prose/cycle01/account/call-0001.request.json` | `ca735a2efb615b2e34f647e80d5a22213690f9591928288cf06cf52a47629c2d` |
| `provider/daily/mini_prose/cycle01/account/call-0001.response.json` | `52645df30c9b35325d46ab2f5c914a930716189e301b3d1d035e61cca3c99acc` |
| `provider/daily/mini_prose/cycle01/carry/call-0001.request.json` | `f50577b7bc2c66cc7fb05465340c6ce0aaeb4dc2677d47220f5cb51e047ad2f7` |
| `provider/daily/mini_prose/cycle01/carry/call-0001.response.json` | `79d7974ec8a67f77be6a58789d6b1f4ff8439a219ccd0add9dcc4d8ec6b570f3` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.request.json` | `534dbc6431b0526a7c44ff8241ee5e090fa56d6b87acb0bf78d0450183be413d` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.response.json` | `c77d0b18c9a2c4979242b71f457703ec6c67fb22054033c4e17fed46cae17d33` |
| `provider/daily/mini_prose/cycle01/response/call-0001.request.json` | `ab9ccc4c76bbf2852a1c8a0c89a66f4542b058b958e0ea6b8ae58cea0b220b78` |
| `provider/daily/mini_prose/cycle01/response/call-0001.response.json` | `d3f037f6c85c7bb31aa0b0f39ec5e50c57e6f6abef752f7874cdceb8f7d42110` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.request.json` | `ce1b6844be4b306ac048179bf374678becb01515759db43dae391ceb104b0395` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.response.json` | `f683dcad9d862180e0184e7df6c4c1fa3041812319f7e04ed5b6aeeeb53e6c79` |
| `requests/daily/bare/cycle01/answer.json` | `479d34455e3d75bb6216877f331c0ba1812fd02c09e5791ef68270f20a6af582` |
| `requests/daily/mini_fcl/cycle01/account.json` | `2329b42d7cce7611339aa5b757816e68c6dd35aaad2fbbeb9c5734fce38f059d` |
| `requests/daily/mini_fcl/cycle01/objection.json` | `0d34c42c6214d45d07859b2e6ddbcb26e0f11e33f3646802ab93ff5dbcf2610d` |
| `requests/daily/mini_fcl/cycle01/response.json` | `2e456ea5e4911d48751e70569c09127556436bd0814f91b6d76c3f07881e5006` |
| `requests/daily/mini_fcl/cycle01/rival.json` | `297a0f277b7d2bfb6423d8fdddef057e08f4ba35f05536cd20e0f181f5990d01` |
| `requests/daily/mini_prose/cycle01/account.json` | `b454c2fbe8f4c71bf8ff23b2978795e8c4276f8e620cf633118c945614921b84` |
| `requests/daily/mini_prose/cycle01/carry.json` | `de45fb82b0b6c8c066ab075ae97db75162ff274880025b61d25336b1bad3e52e` |
| `requests/daily/mini_prose/cycle01/objection.json` | `fe689b0d89a6bc1d8fc013ec05700adba58d68773fe0a12e22779a6147da92b6` |
| `requests/daily/mini_prose/cycle01/response.json` | `c6ad43ed2f126bf5f78f6312593067d0dbae70e94772d7b71cec1d27d3e42dd4` |
| `requests/daily/mini_prose/cycle01/rival.json` | `c39145dc7c40a71c108b643a84ffb8268a9148795c029e84bfd78b3907ebba53` |
| `responses/daily/bare/cycle01/answer.json` | `2d326604ef20bf8b2d017586e2c113e10dfbb2afabaed7c2d934042bf74fa570` |
| `responses/daily/bare/cycle01/answer.txt` | `1ee1dbcdc4fa29ed1f619572a08c48f7394fed5e010035ccbd15f1bc92517c57` |
| `responses/daily/mini_fcl/cycle01/account.json` | `9c1ba6c920b1e2cf01234fdce3f2a1626989ac7d4f779f4b003239e574283d01` |
| `responses/daily/mini_fcl/cycle01/account.txt` | `52e2331006bb8df83975fa5b92c3995334e8bf8b631e36b45bbccef6eee6f0f7` |
| `responses/daily/mini_fcl/cycle01/objection.json` | `4cd1a05567c9d061ab4f147ecfb43fc31a1c96c4bff3a655c25de0086be62fac` |
| `responses/daily/mini_fcl/cycle01/objection.txt` | `f42e686bca1850f4df6db631ec0994da3fd07ecf863a02f570902bed15c1d78f` |
| `responses/daily/mini_fcl/cycle01/response.json` | `af6e8d6a7f434c050fbbbc4eddb64f54261493ba56a6f6ec3f909ff9b75ee646` |
| `responses/daily/mini_fcl/cycle01/response.txt` | `94dbbc8bde9dcf7c9649f9b62b803525ca71bc4a2861abc186f9afb815b3c8be` |
| `responses/daily/mini_fcl/cycle01/rival.json` | `ec5615f24b76db5842afaa5afce41f8ff0f30e0c6f32244c557110127d0ed63b` |
| `responses/daily/mini_fcl/cycle01/rival.txt` | `b94dfa6a978c9b59e05409e3465fd9538b35672629c98c00367102afa4d7c98d` |
| `responses/daily/mini_prose/cycle01/account.json` | `b64a0ecc45499a1b833abd87edb6e5e62cfefec2fddfe422fde811a2b32d133a` |
| `responses/daily/mini_prose/cycle01/account.txt` | `429d4568955bbfdcd6872fbef2eb5a71fe9d381110924499e13d8d92c2b2d748` |
| `responses/daily/mini_prose/cycle01/carry.json` | `a482a3fdcb2e6fd10dee106222925832686773aa9067f06256611bf532541c62` |
| `responses/daily/mini_prose/cycle01/carry.txt` | `034f2746c631accc6d12a3952e6e19d0d2e62924fbe7ee2e7670a4bb7da978f7` |
| `responses/daily/mini_prose/cycle01/objection.json` | `46945d78ed771b3c8732be0f7aa9c1099ae2e05f297fc7f511e5d8c361e2c91d` |
| `responses/daily/mini_prose/cycle01/objection.txt` | `820aee83c74e86fad226efae8b41fe3e33cad78a4b67e9d3f524d69357d0ce21` |
| `responses/daily/mini_prose/cycle01/response.json` | `d8b6337225e62439933dbed7785329b58f416f74ec1b95cfdce55aa601ea80ad` |
| `responses/daily/mini_prose/cycle01/response.txt` | `0b6d7174d3dbf663abae71594873bcc58b1324a5d463507cd4340c43810f792e` |
| `responses/daily/mini_prose/cycle01/rival.json` | `d996799dfd01c8d3344e87af7d4133e2dd5f7f822aec5160d5b1ce1549f41ebc` |
| `responses/daily/mini_prose/cycle01/rival.txt` | `57eaffc8a25e29d4d1c8afabf246e0ceb57a2caec9d393cafc00cb5de767db71` |
| `traces/daily/bare/cycle01/answer.json` | `4ff68da01ac0c9cfd4c060d4a822f7ced327003f53e9e96f1e3fb08916a7fbab` |
| `traces/daily/mini_fcl/cycle01/account.json` | `f4790106152ef33f8f02cc8f182089bd4e99beb4f553144a79e51e2ec4f92f53` |
| `traces/daily/mini_fcl/cycle01/objection.json` | `7499ce1faa2212013e5c63cbdf82ee8fee3be0bea18f5f59af99251199d0dab3` |
| `traces/daily/mini_fcl/cycle01/response.json` | `15f56e279c0d23789ea865e3fe94abb57d45749c0c485dc162f09904b4fd6f42` |
| `traces/daily/mini_fcl/cycle01/rival.json` | `257f1b66d474d890eb608c7e7d5c54f63d4dba677fdc969575a963c18d0d65d6` |
| `traces/daily/mini_prose/cycle01/account.json` | `5725e108b01c89983c73bc7e84268aa9bbf8b77d8b6fe57c79df1137bd5db455` |
| `traces/daily/mini_prose/cycle01/carry.json` | `3748e47eb0239579e5c2b2d2b97315bdf6ca1837b7df8ebad2ebeb1c97cc7f45` |
| `traces/daily/mini_prose/cycle01/objection.json` | `9f3ff5234a34dece133f8eb5daf73f97d8509e4de8996646b7f19a1b9bdcb30d` |
| `traces/daily/mini_prose/cycle01/response.json` | `9bcd9cbe2c5b529483241697cae884e1b87fcf0823b5e0117ac311c663df8db8` |
| `traces/daily/mini_prose/cycle01/rival.json` | `ce2fe52ac41bfec9f4c1a590d8549ca4b8c66427dadbc5b73e916ffc405e4402` |
| `waves/wave0001.json` | `74c380d579b03ae1ee861954b64b785d3bca0e563a69a66e808ebda3b98778fd` |
| `waves/wave0002.json` | `51cb4a32693d23eef6ca0189d680ae38ea86c7a9710191dd7070b71ccaa30e07` |
| `waves/wave0003.json` | `c83a37ea2a012e1de4c7d16adb705ce6e60cced5f71375244733de3104fc5490` |
| `waves/wave0004.json` | `f40e4e9ef185521c785f6e91a001e3fb68c88f56435ec76029c79173c0f2f3b0` |

