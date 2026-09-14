# Use-relation table - H005 occurrence-03

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
- `daily/mini_fcl/cycle01/carry`
- `daily/mini_prose/cycle01/carry`

## Custody

- `plan_id`: `52d7b596c10fcc194dc326d6a47addecda93eb604baf1ce1dbc4e594e8bdeba4`
- `material_sha256`: `8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff`

| check | kind | result |
|---|---|---|
| `material_pin` | cross_file | verified (1/1 occurrence) |
| `manifest_pins` | cross_file | verified (3/3 manifests) |
| `receipt_present` | cross_file | verified (11/11 nodes) |
| `artifact_bytes_vs_receipt` | cross_file | verified (11/11 nodes) |
| `status_vs_receipt` | cross_file | verified (11/11 nodes) |
| `public_text` | cross_file | verified (11/11 nodes) |
| `attempt_vs_receipt` | cross_file | verified (11/11 nodes) |
| `request_record` | cross_file | verified (11/11 nodes) |
| `trace_pinned` | cross_file | verified (11/11 nodes) |
| `provider_bytes` | cross_file | verified (11/11 nodes) |
| `wave_placement` | cross_file | verified (11/11 nodes) |
| `projection_source` | cross_file | verified (16/20 projections; 4 projection(s) had no exposed source (the slot is absent): `daily/mini_fcl/cycle01/account#p.account.0`, `daily/mini_prose/cycle01/account#p.account.0`, `daily/mini_fcl/cycle01/carry#p.carry.3`, `daily/mini_prose/cycle01/carry#p.carry.3`) |
| `plan_identity` | self_consistency | verified (1/1 occurrence) |
| `artifact_self_hash` | self_consistency | verified (11/11 nodes) |
| `artifact_coordinate` | self_consistency | verified (11/11 nodes) |
| `brief_pinned` | self_consistency | verified (11/11 nodes) |
| `brief_label_index` | self_consistency | verified (11/11 nodes) |
| `task_label` | self_consistency | verified (11/11 nodes) |

Custody is the importer's own check, reused unchanged; a self-consistency check cannot detect a coherent rewrite of the one file it reads.

## Method - exactly what the mechanical columns mean

**Sentence.** The referring node's `body` is cut at every match of the published boundary regular expression and nowhere else; leading and trailing whitespace is trimmed out of each span *and out of its offsets*, so `body[start:end]` is exactly the quoted sentence. The boundary is one or more of `.` `!` `?` preceded by a lowercase letter or a closing bracket/quote and followed by whitespace or end-of-string, together with any closing quotes that follow it; or a run of newlines. This is not linguistic sentence segmentation: a numbered list marker ("1. Separate ...") does not split, and an abbreviation such as "e.g." does.

**Token.** The string is lowercased and every maximal run of ASCII letters and digits is a token, in order of occurrence.

**The target record's text.** The concatenation, separated by single spaces, of the target record's prose fields in this order: `text`, `scope`, `action`, `consequence`, `grounds`, `bearing`. `id`, `type` and every ref array are excluded: they are names and pointers, not content. When the ref names the owning contribution as a whole rather than one of its records - a bare exposed-artifact label, or the `#BODY` section header - the subject is instead the same concatenation over **every** record of the owning document, in document order, and the row says so in `overlap_subject`.

**Distinctive token.** A token `t` of the target record's text is *distinctive* when all three hold: (1) `len(t) >= 5` characters after lowercasing; (2) `t` is not in the closed stopword list below; (3) `document_frequency(t) <= 2`, where `document_frequency(t)` is the number of in-scope FCL-1 documents whose record prose contains `t`, and the threshold is `max(2, number_of_in_scope_FCL-1_documents // 2)` - here `max(2, 5 // 2)`. Clause (3) makes the criterion **scope-dependent**: it is computed over the documents listed under `corpus_documents`, and re-running over a different scope can change which tokens count. That is stated rather than hidden, because a partition-invariance question about this instrument (review §5 P5) has to be answerable from its own output.

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
| refs walked | 36 |
| cross document rows | 0 |
| intra document | 14 |
| refs to exposed task artifact | 3 |
| unresolved | 19 |
| importer resolved counter | 17 |
| importer extension counter | 0 |
| importer dangling counter | 19 |

These are counts of authored refs, reported as information. No count here warrants anything (FW5:851: counts "are not outlawed as information"; what is forbidden is a count entering as an *automatic* warrant).

## Rows

*No cross-document reference in scope.*

## Declared uptake versus records present

### `daily/mini_fcl/cycle01/account`

- commitment surface: `read_fcl1`
- records present (4): `loc-001`, `loc-002`, `loc-003`, `loc-004`
- declared `uptake` (1): `h005.task.v1#aceac4253907a8e6`
- records in uptake (0): *none*
- records omitted from uptake (4): `loc-001`, `loc-002`, `loc-003`, `loc-004`
- uptake entries naming nothing (1): `h005.task.v1#aceac4253907a8e6`
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/objection`

- commitment surface: `read_fcl1`
- records present (3): `crit-001`, `crit-002`, `crit-003`
- declared `uptake` (1): `h005.task.v1#aceac4253907a8e6`
- records in uptake (0): *none*
- records omitted from uptake (3): `crit-001`, `crit-002`, `crit-003`
- uptake entries naming nothing (1): `h005.task.v1#aceac4253907a8e6`
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/rival`

- commitment surface: `read_fcl1`
- records present (4): `r1`, `r2`, `r3`, `r4`
- declared `uptake` (4): `r1`, `r2`, `r3`, `r4`
- records in uptake (4): `r1`, `r2`, `r3`, `r4`
- records omitted from uptake (0): *none*
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/response`

- commitment surface: `read_fcl1`
- records present (5): `syn-001`, `syn-002`, `syn-003`, `syn-004`, `syn-005`
- declared `uptake` (5): `syn-001`, `syn-002`, `syn-003`, `syn-004`, `syn-005`
- records in uptake (5): `syn-001`, `syn-002`, `syn-003`, `syn-004`, `syn-005`
- records omitted from uptake (0): *none*
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/carry`

- commitment surface: `read_fcl1`
- records present (5): `carry-001`, `carry-002`, `carry-003`, `carry-004`, `carry-005`
- declared `uptake` (5): `carry-001`, `carry-002`, `carry-003`, `carry-004`, `carry-005`
- records in uptake (5): `carry-001`, `carry-002`, `carry-003`, `carry-004`, `carry-005`
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
- `daily/mini_prose/cycle01/rival` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_prose/cycle01/response` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_prose/cycle01/carry` - commitment surface: prose (not parsed); references not extractable by this instrument

## Residue: refs that resolve to nothing

| referring coordinate | record | field | ref | code | reason |
|---|---|---|---|---|---|
| `daily/mini_fcl/cycle01/objection` | `crit-001` | `target` | `h005.fork5.p.objection.0#loc-003` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `crit-002` | `target` | `h005.fork5.p.objection.0#loc-004` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `syn-001` | `depends` | `h005.fork5.p.response.0#loc-001` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `syn-001` | `depends` | `h005.fork5.p.response.2#r1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `syn-002` | `depends` | `h005.fork5.p.response.1#crit-001` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `syn-002` | `depends` | `h005.fork5.p.response.1#crit-003` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `syn-003` | `depends` | `h005.fork5.p.response.2#r3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `syn-004` | `depends` | `h005.fork5.p.response.1#crit-003` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `syn-005` | `depends` | `h005.fork5.p.response.0#loc-004` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `syn-005` | `depends` | `h005.fork5.p.response.2#r4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `carry-001` | `depends` | `h005.fork5.p.carry.0#syn-001` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `carry-001` | `depends` | `h005.fork5.p.carry.2#crit-001` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `carry-002` | `depends` | `h005.fork5.p.carry.0#syn-003` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `carry-003` | `depends` | `h005.fork5.p.carry.0#syn-004` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `carry-003` | `depends` | `h005.fork5.p.carry.2#crit-003` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `carry-004` | `depends` | `h005.fork5.p.carry.1#loc-002` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `carry-004` | `depends` | `h005.fork5.p.carry.2#crit-002` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `carry-005` | `revises` | `h005.fork5.p.carry.1#loc-004` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `carry-005` | `depends` | `h005.fork5.p.carry.0#syn-005` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |

## Files read

Every byte this instrument read, with its sha256. Nothing under the occurrence was written.

| path | sha256 |
|---|---|
| `artifacts/daily/bare/cycle01/answer.json` | `1a0cfda179d837a427ad9e8091c7e658fad96abe9ae98f95d0a8f81c74915d8b` |
| `artifacts/daily/mini_fcl/cycle01/account.json` | `68a181ab635859cb21020a95e9700bd056509d44160b42fa4b8c8cfbe417d55a` |
| `artifacts/daily/mini_fcl/cycle01/carry.json` | `60f477a1782e760594c15b58ee4386121adb0bd3564d4e5e4d578ca890cdb486` |
| `artifacts/daily/mini_fcl/cycle01/objection.json` | `905de875e846cd93b026129e0fa7e41c18a4db0a5e9ccb55192a7518b8746edc` |
| `artifacts/daily/mini_fcl/cycle01/response.json` | `70e09e1f5bdc914237e2a46b33aed70c19277c0ee243f7a2a4e6fce16008c4f4` |
| `artifacts/daily/mini_fcl/cycle01/rival.json` | `4eaf7b12319d74d5a28c22e73a7f13c0248709f9da767fb8832486b0396e4f47` |
| `artifacts/daily/mini_prose/cycle01/account.json` | `9dd02cbe27cab440bd2028bec2ad7a5bb2cdae2ce8589b93d185a670148cc308` |
| `artifacts/daily/mini_prose/cycle01/carry.json` | `cece31dd208559941fd2a735da8e80b11bcb3e66947430bd3a5dac0d524a2e76` |
| `artifacts/daily/mini_prose/cycle01/objection.json` | `5f8b6117dde25213c9e334d9d8f62d1d7cbc93bea1ddf9017f4813e5538c1ad7` |
| `artifacts/daily/mini_prose/cycle01/response.json` | `f89710455a6ee4f231c0db223a63678c2bf18f28d4b80a4916aee596413003dd` |
| `artifacts/daily/mini_prose/cycle01/rival.json` | `ad617038191076557d0caa100fe1c2c808252c72aab8751c11bcde744a2edded` |
| `attempts/daily/bare/cycle01/answer.json` | `7a3d94acd3d191b2937f875c715221522afed399fa3999a5400a34e2d9f5353e` |
| `attempts/daily/mini_fcl/cycle01/account.json` | `311b9cabefc4fc29f8c912cc8a4bb91d852eacae626974acc0afb92bd0f33880` |
| `attempts/daily/mini_fcl/cycle01/carry.json` | `59c55dcfbf02f14135bd3401eb27e80da229158a5bb10359a3dea84cf024a490` |
| `attempts/daily/mini_fcl/cycle01/objection.json` | `3a4e10eae938ed596a652fb691ebb791b9cd90c218122df6962103138a76f67c` |
| `attempts/daily/mini_fcl/cycle01/response.json` | `bbcc5c1c41c69177181c63bc08ed5ee31f39f1b7c9ebb03239ac7a98279adc7e` |
| `attempts/daily/mini_fcl/cycle01/rival.json` | `1d820bdaf1ddaf19169b0bec36a8e37c05f0d019b0caf6106a13001ff95c39de` |
| `attempts/daily/mini_prose/cycle01/account.json` | `324db2a3d96f8fd2da01c229eeb10bd0172ca12b486977cc7d1738188c53baa5` |
| `attempts/daily/mini_prose/cycle01/carry.json` | `9fdf9acb7f0c68bfd467f5f3a795129eb87e72ba91de1f72bd4d99e26568ad7f` |
| `attempts/daily/mini_prose/cycle01/objection.json` | `ec02a3c6bf358be3ead91cef5cae6b8f58736dde74d3b818bdde0efd30a07442` |
| `attempts/daily/mini_prose/cycle01/response.json` | `d795610989c8074c4b7330677d3f7ff096485cc99777b1afa90f3ec0430f17bb` |
| `attempts/daily/mini_prose/cycle01/rival.json` | `b91059a5412983b74cdc6e1008df996624709e84b1fd504f9732db8d6262382f` |
| `manifests/fork5.json` | `f7e727daea6d3ba4353b1b2f93ae7e461a648c99877cf2ee97ca7653e30e1ee8` |
| `manifests/return6.json` | `f3ece835e680452807d9e0dd69232c34a452b67062cba75c4ba46bf87bb93951` |
| `manifests/weave7.json` | `ea8174af734dabde382a36cd85323a064ef9a8302490b9f85e1f9f360e7686df` |
| `material.json` | `8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff` |
| `plan.json` | `5d3d2cd0a6d342f9ef8ea11a4c7e3b26b6ec311af4c835c9cb682a847be86e2d` |
| `provider/daily/bare/cycle01/answer/call-0001.request.json` | `286cb5b3c03db5a29f3848784f81870ddfa8179e8a7c4eee0db930ed2f05b30d` |
| `provider/daily/bare/cycle01/answer/call-0001.response.json` | `e3b9d66e54f6d159dfce7829a4aeb85e4ed3979bfb502cd32d5d8ea80237fd46` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | `0bd1e47c74dad1d69bc1e347f522ab9c44eb9261a00661712282c940e365d5d0` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | `3b6a27b91fb16fc673fa1429a16bba9c66c112dc00231d34c160ae9e5d08808b` |
| `provider/daily/mini_fcl/cycle01/carry/call-0001.request.json` | `93b3502f849e41f359f11664dda070f80299eebccdca26d943bd3076fdd893cc` |
| `provider/daily/mini_fcl/cycle01/carry/call-0001.response.json` | `ec1def6e861d877264c47f475adcd624bebdc0718b0ad95a26ee8c2da777bd75` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.request.json` | `ede3fb831b1fe69c91584e2ff1c1e594d488c2537774fa2db2cdfc51a5f30773` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.response.json` | `e830c450b8d62fa3661092907c4e5b34052ef311f75640f5ada16b004e9a7e1d` |
| `provider/daily/mini_fcl/cycle01/response/call-0001.request.json` | `c9e94285a99a1ca08dc4e5d274a1c829eabf63abbdcafbf101dee3e6ed6aaa33` |
| `provider/daily/mini_fcl/cycle01/response/call-0001.response.json` | `48665bc4e655208b6a464d59c5d91fce3a7bba1ec6c013630bd2c3adbd36de6a` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | `e1c2c7a6e6326c88544c64ab3e3b3c9fb439b4a129d9f8d1912dedab549fc09b` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | `02a265a8c58a6bb4e60b6b2d41e684c9667824b188b29ee97df4dc1263263be8` |
| `provider/daily/mini_prose/cycle01/account/call-0001.request.json` | `a1b0af4f07535c7d729cee273a7269377b802ca4d400820add49dd2d6a51b601` |
| `provider/daily/mini_prose/cycle01/account/call-0001.response.json` | `bb97b63fca95e97542255885cb787a8337f944ed1a00217a476e522b6b1b8b61` |
| `provider/daily/mini_prose/cycle01/carry/call-0001.request.json` | `66c1768bc81caf180345f2015e9814221595307afdac83d96d42ed469503674f` |
| `provider/daily/mini_prose/cycle01/carry/call-0001.response.json` | `a3512b6ad8ef044f7ffe761afd012928afd0bb7362a372cc4bdf3dc1a60eb7ff` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.request.json` | `5671f6e4c17d05f89943e6b5a2a8ed8e13a148105e7063dd295135ba9ab74023` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.response.json` | `52dcce40a812b064f32b5fac7c8b0d97322d343411e147a282b5f644500d2544` |
| `provider/daily/mini_prose/cycle01/response/call-0001.request.json` | `19aa0d038a1a488738f86c0d3319b107b5e0226546ff4c4040305d752582d1f1` |
| `provider/daily/mini_prose/cycle01/response/call-0001.response.json` | `8f143f416c713df8d4d639b47a895036336dc118ca94475013e4a423045ef032` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.request.json` | `232acc030efd398448407d14ca4e84102fdf8fee106a5c8a655c3ba696a522b9` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.response.json` | `6bbcc4b1e3c3ef42bb96872e8821a48295093cb13a9e69d29d4b8464acf3e2ca` |
| `requests/daily/bare/cycle01/answer.json` | `dd0df5289402cbbafda0a9e7b32ac25c3dae3c428398411d70a94649880dcc85` |
| `requests/daily/mini_fcl/cycle01/account.json` | `cecb3574527de1622aca467d0a54177d7176a8b3f98142d6157eeeb45c533027` |
| `requests/daily/mini_fcl/cycle01/carry.json` | `8d3e02825df4b569995205404063d4a24f03e3df5e534494778f39ad65172954` |
| `requests/daily/mini_fcl/cycle01/objection.json` | `57814dde16c368ddd6f3492afaec2989729463cf8de6090d78888ef9249627b9` |
| `requests/daily/mini_fcl/cycle01/response.json` | `b0caa4195209e1ecd0dd5a5c992618ff302173b53f14b23b330230398f0afe07` |
| `requests/daily/mini_fcl/cycle01/rival.json` | `f40a0d2fc70bb7dc397faaf6d0b51d90150026d4c68e25ab79e2cd60ed94e2c5` |
| `requests/daily/mini_prose/cycle01/account.json` | `084e1ec20262c2d65533d92d03b3e86f0532667e4a4f2235b107f09f753fee66` |
| `requests/daily/mini_prose/cycle01/carry.json` | `f470d8d4af3a33dce40dc6c02b0b75cdafaabb4d71db40d47ccba1f561bbe616` |
| `requests/daily/mini_prose/cycle01/objection.json` | `3eabfd45543818b62204d362f32da70193bb7f77f0889d47974d17da98b0b1c9` |
| `requests/daily/mini_prose/cycle01/response.json` | `b0c759345591be3bcabbf49a1e86e548f539f490eb7332c34136a9a230d5fe35` |
| `requests/daily/mini_prose/cycle01/rival.json` | `ce4da18b3cbe3f84977c241c50c4d5cbe9917cfe47e48d70eed65c53126ed1cd` |
| `responses/daily/bare/cycle01/answer.json` | `4bed30fe6fe041bc5dd153c0394813af1319394cc4f72d84e4919965b740674a` |
| `responses/daily/bare/cycle01/answer.txt` | `6c1f9ec71c6098528d82c2cc72bcb51c83d38a2d3bf019e18534c975a5d8c363` |
| `responses/daily/mini_fcl/cycle01/account.json` | `5a68424a35b0c1603d372f78cdeeb6941be0abfdf4f0cfa0d0c34f450f4691ec` |
| `responses/daily/mini_fcl/cycle01/account.txt` | `7de552c3f54290fd5fd5c73541ea573842acd263bf324810dac9b0547a98b753` |
| `responses/daily/mini_fcl/cycle01/carry.json` | `1441201b11de0c16a2cbac60b07d51bb4cc1b378ab068f9d96c6140374ecbeb2` |
| `responses/daily/mini_fcl/cycle01/carry.txt` | `637c08b4a97c489e0d223c56090901d0575fec96e46a803cda437795adc661f1` |
| `responses/daily/mini_fcl/cycle01/objection.json` | `a1d8f50470dca2e8b375f5717a2123ad4a1fd2b1f9e414a6017246da127585b3` |
| `responses/daily/mini_fcl/cycle01/objection.txt` | `5630410f72a8b488c38cf7ca5be08474e065449a8d9a779e7f58201296d10856` |
| `responses/daily/mini_fcl/cycle01/response.json` | `95b63d583e3b41afe1992a6c9c56da36265335003245f85f9dcea34adcfcb7e1` |
| `responses/daily/mini_fcl/cycle01/response.txt` | `116c4ac3372a32672631e6778e7c46402d51aab11945caec51b32272618e770e` |
| `responses/daily/mini_fcl/cycle01/rival.json` | `e7badf341b25736b2762fa6449c72d82025366b95fd72d07035508a4254a9829` |
| `responses/daily/mini_fcl/cycle01/rival.txt` | `17bae4d69bca90355d4ebdc831ae74cef4733a02576229725f30ff507dd43492` |
| `responses/daily/mini_prose/cycle01/account.json` | `6dd12223eed42d6fee96599a5900706d0363c77196556911033d7a17935bc67e` |
| `responses/daily/mini_prose/cycle01/account.txt` | `2f8b3b96199a89a7ce815ac4d418a54d8880017c119f67afacb9742bc3716c00` |
| `responses/daily/mini_prose/cycle01/carry.json` | `11ee352180417a5dee5d60309e825eea47940df264a8ddcd9d95774d04835a75` |
| `responses/daily/mini_prose/cycle01/carry.txt` | `491e20da7c9918a69d2ee94d9983cbe1fb5f34023d639f2288768d332b69be98` |
| `responses/daily/mini_prose/cycle01/objection.json` | `bf6829c41c2b070de68048ee76f68e50282438fe9c6ddf982c9a4fc9297557bd` |
| `responses/daily/mini_prose/cycle01/objection.txt` | `523fd1aff39434ef4c3556686624c565e5b7115981a06467b5db355d82176e16` |
| `responses/daily/mini_prose/cycle01/response.json` | `ad584b9c57876aee36095c049bc4dec795d820ecf25836910ee538564814e294` |
| `responses/daily/mini_prose/cycle01/response.txt` | `6910aff4f8d4c2b0c133f1479bbf7a941cdb0053e1a96faa9284cabb9ad6fea9` |
| `responses/daily/mini_prose/cycle01/rival.json` | `8c0abfa5ee62f8c370e70d9cb7b2b298dc749ad0d5fb7727c20dd90fb40c8a58` |
| `responses/daily/mini_prose/cycle01/rival.txt` | `0809ed0a15e57c979922f902853c0423dfe27d722d7424e4c489e97516f4148a` |
| `traces/daily/bare/cycle01/answer.json` | `4ff68da01ac0c9cfd4c060d4a822f7ced327003f53e9e96f1e3fb08916a7fbab` |
| `traces/daily/mini_fcl/cycle01/account.json` | `f4790106152ef33f8f02cc8f182089bd4e99beb4f553144a79e51e2ec4f92f53` |
| `traces/daily/mini_fcl/cycle01/carry.json` | `0a2fbbe516eb911d332c787010742e0e6b86b1692b369ae3910048a1fd5c1671` |
| `traces/daily/mini_fcl/cycle01/objection.json` | `04259d03e9d7331d255f673c044a4191319669e3b5a41687f020a4d7557e6829` |
| `traces/daily/mini_fcl/cycle01/response.json` | `a40c0ef79630c99a109aa156816671fab1b9545ca0589a15dc7de5d3ef72928a` |
| `traces/daily/mini_fcl/cycle01/rival.json` | `dc8308098af580b45567d2baa1908b601bb0bb69c02339b7bd22556927e64d55` |
| `traces/daily/mini_prose/cycle01/account.json` | `5725e108b01c89983c73bc7e84268aa9bbf8b77d8b6fe57c79df1137bd5db455` |
| `traces/daily/mini_prose/cycle01/carry.json` | `bd87750253e9b8a658ed033a0aad82ace879ff92d39ccbfd0f9ea262c09dae9a` |
| `traces/daily/mini_prose/cycle01/objection.json` | `ee6fbeaee7be52697b8537e2dcb7335c98268da421a3ea652565a734b5fa779d` |
| `traces/daily/mini_prose/cycle01/response.json` | `818a949ae6dcc779a3c751ff4a6f8c5f8cf18ec989c7e3133c97f33746bbacb5` |
| `traces/daily/mini_prose/cycle01/rival.json` | `8cd06f547e84904c55decf7d567b443f7cd1f32dbca19df64bd1ecc2038c1237` |
| `waves/wave0001.json` | `5cdef2281ccbcc726d04e88b5428938d184949186ccc5b2bd601223a4cdd7de3` |
| `waves/wave0002.json` | `6ad2760a38dc945ef8a49c11750153a6880190fa0e2bd0b4b2a28f190d6bdb1a` |
| `waves/wave0003.json` | `7f8e531d94f623478acd3f9a3f4eedfe34ec57e9b78a9095b80b16176d7f024e` |
| `waves/wave0004.json` | `a253a005da45f11f9e73a6c9c1e023971f42a0c99a12f26bc940fa4ca1538eb2` |

