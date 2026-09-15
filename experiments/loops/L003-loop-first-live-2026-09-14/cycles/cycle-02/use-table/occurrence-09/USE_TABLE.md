# Use-relation table - H005 occurrence-09

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

- `plan_id`: `04c26f24812a4e48d41cfd6f6ef16785ba25ea183894bfafe86d6eb0e35af8ee`
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
| refs walked | 117 |
| cross document rows | 0 |
| intra document | 54 |
| refs to exposed task artifact | 0 |
| unresolved | 63 |
| importer resolved counter | 54 |
| importer extension counter | 0 |
| importer dangling counter | 63 |

These are counts of authored refs, reported as information. No count here warrants anything (FW5:851: counts "are not outlawed as information"; what is forbidden is a count entering as an *automatic* warrant).

## Rows

*No cross-document reference in scope.*

## Declared uptake versus records present

### `daily/mini_fcl/cycle01/account`

- commitment surface: `read_fcl1`
- records present (13): `n1`, `c1`, `c2`, `c3`, `a1`, `a2`, `a3`, `a4`, `a5`, `o1`, `p1`, `p2`, `u1`
- declared `uptake` (12): `c1`, `c2`, `c3`, `a1`, `a2`, `a3`, `a4`, `a5`, `o1`, `p1`, `p2`, `u1`
- records in uptake (12): `c1`, `c2`, `c3`, `a1`, `a2`, `a3`, `a4`, `a5`, `o1`, `p1`, `p2`, `u1`
- records omitted from uptake (1): `n1`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/objection`

- commitment surface: `read_fcl1`
- records present (9): `sc1`, `ob1`, `ob2`, `ob3`, `ob4`, `ob5`, `ob6`, `pr1`, `use1`
- declared `uptake` (7): `ob1`, `ob2`, `ob3`, `ob4`, `ob5`, `ob6`, `use1`
- records in uptake (7): `ob1`, `ob2`, `ob3`, `ob4`, `ob5`, `ob6`, `use1`
- records omitted from uptake (2): `sc1`, `pr1`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/carry`

- commitment surface: `read_fcl1`
- records present (11): `k1`, `k2`, `k3`, `k4`, `k5`, `k6`, `k7`, `k8`, `k9`, `k10`, `k11`
- declared `uptake` (11): `k1`, `k2`, `k3`, `k4`, `k5`, `k6`, `k7`, `k8`, `k9`, `k10`, `k11`
- records in uptake (11): `k1`, `k2`, `k3`, `k4`, `k5`, `k6`, `k7`, `k8`, `k9`, `k10`, `k11`
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
- `daily/mini_prose/cycle01/rival` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_fcl/cycle01/response` - commitment surface: schema_failure; references not extractable by this instrument
- `daily/mini_prose/cycle01/response` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_prose/cycle01/carry` - commitment surface: prose (not parsed); references not extractable by this instrument

## Residue: refs that resolve to nothing

| referring coordinate | record | field | ref | code | reason |
|---|---|---|---|---|---|
| `daily/mini_fcl/cycle01/objection` | `sc1` | `mentions` | `h005.fork5.p.objection.0#c1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `sc1` | `mentions` | `h005.fork5.p.objection.0#c2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob3` | `mentions` | `h005.fork5.p.objection.0#c2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `pr1` | `mentions` | `h005.fork5.p.objection.0#p1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `use1` | `mentions` | `h005.fork5.p.objection.0#a1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `use1` | `mentions` | `h005.fork5.p.objection.0#a2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `use1` | `mentions` | `h005.fork5.p.objection.0#a3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `use1` | `mentions` | `h005.fork5.p.objection.0#a4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob1` | `target` | `h005.fork5.p.objection.0#a1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob1` | `target` | `h005.fork5.p.objection.0#a4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob1` | `target` | `h005.fork5.p.objection.0#c3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob2` | `target` | `h005.fork5.p.objection.0#u1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob2` | `target` | `h005.fork5.p.objection.0#p1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob3` | `target` | `h005.fork5.p.objection.0#a3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob4` | `target` | `h005.fork5.p.objection.0#a2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob4` | `target` | `h005.fork5.p.objection.0#o1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob5` | `target` | `h005.fork5.p.objection.0#a4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob6` | `target` | `h005.fork5.p.objection.0#a1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob6` | `target` | `h005.fork5.p.objection.0#a2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob6` | `target` | `h005.fork5.p.objection.0#a3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob6` | `target` | `h005.fork5.p.objection.0#a5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob6` | `target` | `h005.fork5.p.objection.0#u1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k1` | `mentions` | `h005.fork5.p.carry.0` | `ref_unresolved` | neither a local record name nor an exposed-artifact label; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k1` | `mentions` | `h005.fork5.p.carry.1` | `ref_unresolved` | neither a local record name nor an exposed-artifact label; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k1` | `mentions` | `h005.fork5.p.carry.2` | `ref_unresolved` | neither a local record name nor an exposed-artifact label; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k2` | `mentions` | `h005.fork5.p.carry.2#ob1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k2` | `depends` | `h005.fork5.p.carry.0#b-c1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k3` | `depends` | `h005.fork5.p.carry.0#b-c2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k3` | `depends` | `h005.fork5.p.carry.0#b-o3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k3` | `depends` | `h005.fork5.p.carry.0#b-a7` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k4` | `mentions` | `h005.fork5.p.carry.2#sc1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k4` | `revises` | `h005.fork5.p.carry.1#c1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k4` | `depends` | `h005.fork5.p.carry.0#b-c2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k5` | `mentions` | `h005.fork5.p.carry.0#b-a1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k5` | `revises` | `h005.fork5.p.carry.1#a4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k5` | `depends` | `h005.fork5.p.carry.2#ob5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k6` | `mentions` | `h005.fork5.p.carry.0#b-a3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k6` | `mentions` | `h005.fork5.p.carry.0#b-a4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k6` | `mentions` | `h005.fork5.p.carry.0#b-a5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k6` | `mentions` | `h005.fork5.p.carry.0#b-a6` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k6` | `mentions` | `h005.fork5.p.carry.0#b-a7` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k6` | `mentions` | `h005.fork5.p.carry.2#ob1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k7` | `depends` | `h005.fork5.p.carry.0#b-p1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k8` | `depends` | `h005.fork5.p.carry.0#b-p2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k9` | `mentions` | `h005.fork5.p.carry.2#pr1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k9` | `depends` | `h005.fork5.p.carry.0#b-p3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k10` | `depends` | `h005.fork5.p.carry.0#b-p4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k11` | `target` | `h005.fork5.p.carry.0#b-a1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k11` | `target` | `h005.fork5.p.carry.0#b-a2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k11` | `target` | `h005.fork5.p.carry.0#b-a3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k11` | `target` | `h005.fork5.p.carry.0#b-a4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k11` | `target` | `h005.fork5.p.carry.0#b-a5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k11` | `target` | `h005.fork5.p.carry.0#b-a6` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k11` | `target` | `h005.fork5.p.carry.0#b-a7` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k11` | `target` | `h005.fork5.p.carry.0#b-a8` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k11` | `target` | `h005.fork5.p.carry.0#b-c1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k11` | `target` | `h005.fork5.p.carry.0#b-c2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k11` | `target` | `h005.fork5.p.carry.0#b-c3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k11` | `target` | `h005.fork5.p.carry.0#b-c4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k11` | `target` | `h005.fork5.p.carry.0#b-o1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k11` | `target` | `h005.fork5.p.carry.0#b-o2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k11` | `target` | `h005.fork5.p.carry.0#b-o3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `k6` | `target` | `h005.fork5.p.carry.0#b-a2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |

## Files read

Every byte this instrument read, with its sha256. Nothing under the occurrence was written.

| path | sha256 |
|---|---|
| `artifacts/daily/bare/cycle01/answer.json` | `551361881720df6f0e7050f209263500ca8e4ec36e1260f005a1c7f18dac1d03` |
| `artifacts/daily/mini_fcl/cycle01/account.json` | `56d1c8289e65ab5440f5a0c0956e20140e17a7a0c7b27a2f576bd216cfe57c6a` |
| `artifacts/daily/mini_fcl/cycle01/carry.json` | `eff01bac13dff59c6ecac3766bb3740e7cf59444cb774859133624b3d5c92eae` |
| `artifacts/daily/mini_fcl/cycle01/objection.json` | `8943af3ad4db43bb29876a67e43e07945a6dc6ccee44fa3488c2855ccbc2061d` |
| `artifacts/daily/mini_fcl/cycle01/response.json` | `8b3f9b02bfb0f94dbb40298c86ba6a2052a064e0a391d952a93d88a5730e3a65` |
| `artifacts/daily/mini_fcl/cycle01/rival.json` | `a6a2baa8db897b14a96ce59d7eead93b393e426199e5d0f982555b4557665d97` |
| `artifacts/daily/mini_prose/cycle01/account.json` | `e97a627fab2ee94eef3f7b187d78c4f4c98e2b1abd379bb13110b860385e862a` |
| `artifacts/daily/mini_prose/cycle01/carry.json` | `0a88772d77e9b52a153abf04bb3403ed1ae9f038d3f996f5b372415bf2d1c6dd` |
| `artifacts/daily/mini_prose/cycle01/objection.json` | `cc3f7215b0eb99b6ec73eb0703e4b66107ac04ccb003a630e69d57cc9131fdb3` |
| `artifacts/daily/mini_prose/cycle01/response.json` | `6887668044a1934d6ec9b18d940b5e8014270abf5a731f25a2ea0ef01de6fb22` |
| `artifacts/daily/mini_prose/cycle01/rival.json` | `d74a0505197368257d1aab9f15bf60985c3459809417b8cc46eabdde386bc7df` |
| `attempts/daily/bare/cycle01/answer.json` | `5b98b54ad72b4da8588ab946fe38cc486f7391ef63c89b8a1e1cd7e00a68e4b8` |
| `attempts/daily/mini_fcl/cycle01/account.json` | `ce3318270dcd088819e5b8f94cae4a7de380a53452f0c7ffe1ef3edc74f9006c` |
| `attempts/daily/mini_fcl/cycle01/carry.json` | `2a4d3e406c7ba1d668d3703083eb637c4e6119d023ee11a6001128bb590dc790` |
| `attempts/daily/mini_fcl/cycle01/objection.json` | `f0bef4d59adaad2f03579f558682ca5f67aced799109ffd99f523c9ef686b137` |
| `attempts/daily/mini_fcl/cycle01/response.json` | `84f404265276511a349f2839c54e13c2351dd8105d04649154d3aaa3d59fff40` |
| `attempts/daily/mini_fcl/cycle01/rival.json` | `37e27ced4ac777166a42cb3207280aa1e7d583a1577ca345c557ca90e4ece0df` |
| `attempts/daily/mini_prose/cycle01/account.json` | `c291e04a960bac05ad022f3dcfc41512fbcba38f6d4c7d18e578a2a4db0e4315` |
| `attempts/daily/mini_prose/cycle01/carry.json` | `2c0d7f37da50df69a3fb2587fb0bb34194aabf063cf7e19ed42c3776e65ee516` |
| `attempts/daily/mini_prose/cycle01/objection.json` | `927547f7f7709825bd44e6af3b9357a06c1878aa64c76cdd1289528ca6f2e907` |
| `attempts/daily/mini_prose/cycle01/response.json` | `eedb6fd18173eb2326bf3916c7e71743543734446edd18ae9ffc292304daeb31` |
| `attempts/daily/mini_prose/cycle01/rival.json` | `345027d5452e840b737e208b0aa11357badb4583426e4ec2b2bbf06fb8085f49` |
| `manifests/fork5.json` | `8f2d928b2f70298906b17d62e73b41804efa754d845f018d9eb312af7dcb536a` |
| `manifests/return6.json` | `bad1f6dc4ddda462f1b3acaa56a9e552eeb98255509cb4bfa3353c2305abb3b5` |
| `manifests/weave7.json` | `0b8a5f337f754b23fd51721ff287e25347af99648a7d2b00ad73b7baa571c2cb` |
| `material.json` | `8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff` |
| `plan.json` | `028c551106cc37c6f568fe559c79e784abe7c849f5372447291e22216e61a5f2` |
| `provider/daily/bare/cycle01/answer/call-0001.request.json` | `d8a111956bdd0e8ea27160a756ce496c2a60e640c0317f5ee42143896cbcf743` |
| `provider/daily/bare/cycle01/answer/call-0001.response.json` | `8361ebf00923d8d18badc1b1b1dfa7a85442c99328a4eeff2e416648583e824b` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | `f3c87e82cf2fcd355b45c0baadd18e3a7f25a1595644884553208d84abd4a80e` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | `e5bd571bddbfa3666040d65e9c3092e04b1fc3a098d1aba03079f2fdbdbed1cc` |
| `provider/daily/mini_fcl/cycle01/carry/call-0001.request.json` | `2891dc1fd84d57ed808af5ca83404ecc31dcaddefee6c5cf7995e28e7a6401fa` |
| `provider/daily/mini_fcl/cycle01/carry/call-0001.response.json` | `fede7f11807bd43d25be4fc826663d5038cf425db1e87920fd8eb3310b5b3192` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.request.json` | `b290f24fb3dadd635c2a82258be3095603d6c918d63e0d8437578bffd255e6e7` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.response.json` | `fa9b7db80f93081363d48e01c8a566e00fb888a2aef125b170e0ef029175e35f` |
| `provider/daily/mini_fcl/cycle01/response/call-0001.request.json` | `db06bd12f060bfa1c983b99a0cce12d6880e3b847484fde9b03412abd4440c00` |
| `provider/daily/mini_fcl/cycle01/response/call-0001.response.json` | `7050d4e1b47678dd81645c6a7c493f987e53c38229a37494afca589a62ea7453` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | `7ec21dcdc28b460be520c19ba9973ea1084c7f0d80f8a8756031cbcd96c1da7d` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | `c65409ee4b76ad4ad96f85bbc3cf5b2d79f9800f0f815ba7595b230e018b3905` |
| `provider/daily/mini_prose/cycle01/account/call-0001.request.json` | `f479b55b9b6898a1e624e567b2087fa0e300d30989724e6ca9ad71d4bb2707ea` |
| `provider/daily/mini_prose/cycle01/account/call-0001.response.json` | `a4f425fb19ddcdbfe4cea3b8a53bd21406325b8998ab183a7ac433a4ec085b3d` |
| `provider/daily/mini_prose/cycle01/carry/call-0001.request.json` | `1b47bb6f37df72e919f811eedd57b16f1c645d24163784e4ca88e020665c8764` |
| `provider/daily/mini_prose/cycle01/carry/call-0001.response.json` | `e253078d0e868f7cfbef728e875313b70358acaceff8fdfa79f4509853ade925` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.request.json` | `c3a21f0954567cdbf303c26ce46d539906ea63944a87d6b5e51ed3c2adfd74ec` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.response.json` | `80e4bdef4c94e4ad3868d2577b7449ce29adabf4dd552c319e23ff2d12f22800` |
| `provider/daily/mini_prose/cycle01/response/call-0001.request.json` | `128b058cb4bdea011e381684077f4827b36cee6125a30acfcb4811de336a1bb6` |
| `provider/daily/mini_prose/cycle01/response/call-0001.response.json` | `74107982381d9c362e4faede9aff4e65b8f59d9fc7b00d87c7619b8f82f4ea09` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.request.json` | `8c3ae7c207f25da07ed256e2af4b1c26abcca5a08aa556fc79cb5c0a9e0192d0` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.response.json` | `d97f10047f88eb9b0df7abc8bd6ffa49a956910a33e3d969a9abf26be89c280d` |
| `requests/daily/bare/cycle01/answer.json` | `479d34455e3d75bb6216877f331c0ba1812fd02c09e5791ef68270f20a6af582` |
| `requests/daily/mini_fcl/cycle01/account.json` | `2329b42d7cce7611339aa5b757816e68c6dd35aaad2fbbeb9c5734fce38f059d` |
| `requests/daily/mini_fcl/cycle01/carry.json` | `e1dee93938431a82f4ecd589ddf8f4e0cc45497c4f69c0d72fd0c67e9f1fcc50` |
| `requests/daily/mini_fcl/cycle01/objection.json` | `571ae2910c3d6ad481e26d1340585cad8abbedecae3c2f0498613d4bd98f22dc` |
| `requests/daily/mini_fcl/cycle01/response.json` | `f6af45ac69754b73db30f57c04a0eaf2f07a991c1c832510b095326839d6edf3` |
| `requests/daily/mini_fcl/cycle01/rival.json` | `f3f94b1eb0905d99a9e8f096cb0aaa2984915b94ee2603cba9b7095ab696cb77` |
| `requests/daily/mini_prose/cycle01/account.json` | `b454c2fbe8f4c71bf8ff23b2978795e8c4276f8e620cf633118c945614921b84` |
| `requests/daily/mini_prose/cycle01/carry.json` | `880a635ebedfc83f9da28c525926d146efae3ef6e5c779222e5fd62589cb440a` |
| `requests/daily/mini_prose/cycle01/objection.json` | `28001cfc581c2e31907f55936f15de7d37d5b33cdb73a2f0c5f41648c6836c1d` |
| `requests/daily/mini_prose/cycle01/response.json` | `a989f373c224e8473ff445b90d1162b83a91402b0304a3b1e008948c9f9dbf0c` |
| `requests/daily/mini_prose/cycle01/rival.json` | `7bbe840d4b4fc8c0dff20d833478172e0a582b43bfc472b85a743df210e725d3` |
| `responses/daily/bare/cycle01/answer.json` | `e332f842651eae970ac764db7d2ea1eddaf3ef55243158ea73ca63187806f569` |
| `responses/daily/bare/cycle01/answer.txt` | `eed03a7e920670d87457e5799dcb74d68275d59a1ed2a3023eb7ef8d7c494abd` |
| `responses/daily/mini_fcl/cycle01/account.json` | `c4a6b49115d3e5d0f7152b8392ff5c2d24e6a1b73fa7e8b8b08c268aaa434411` |
| `responses/daily/mini_fcl/cycle01/account.txt` | `99898955b3fd54aa752fa69f40ac2345406a52aa6a9afdc1b245672350ed31e0` |
| `responses/daily/mini_fcl/cycle01/carry.json` | `2a5c75c86de264ed22f57ff2bbb14f75bff4aa048406d67cd5be549599b4b6cc` |
| `responses/daily/mini_fcl/cycle01/carry.txt` | `1a65133de286ca7965432737629509208c7cc633731f72da1112334e3c442f0f` |
| `responses/daily/mini_fcl/cycle01/objection.json` | `af63e4c36495713945b745d1e7b2e5a1ae7e8bb955ddeb8370226054b08415af` |
| `responses/daily/mini_fcl/cycle01/objection.txt` | `9d772aa809dd796d0981c61de7a1c09175c24443ef7d4b7d64d9744800123ada` |
| `responses/daily/mini_fcl/cycle01/response.json` | `4061c20a5dd7cf16b0d7f4d3b1b0c22d5ce6619ad5be1616b02e65282523abcd` |
| `responses/daily/mini_fcl/cycle01/response.txt` | `67c1d2143984ed129b68d7e5929ab865d03e17febad3bc9c404bc1a9cc7ab3ef` |
| `responses/daily/mini_fcl/cycle01/rival.json` | `a4689487a0ced07590fb37e4c4df34919eff582b48663b3a538f2a7d4f9fb42f` |
| `responses/daily/mini_fcl/cycle01/rival.txt` | `59045f3300319955d05b23883aea12e7d90343b2db85aa0ca887451f8a3f547f` |
| `responses/daily/mini_prose/cycle01/account.json` | `bedb170cf407dd1c6120692619630b80a4b87b33da1f37c24bebdc32d1d3d3b9` |
| `responses/daily/mini_prose/cycle01/account.txt` | `50be8a6447810c567c1f0947c515dc063eaf9c0e38c199b09ce832f8093116ad` |
| `responses/daily/mini_prose/cycle01/carry.json` | `44a531f7be6ab062bffe58e2cd19de03692b59f44a074e9b2b3e130caf8421d1` |
| `responses/daily/mini_prose/cycle01/carry.txt` | `4139d9202e9f54c04dd22e1456ef66bcb4bd94eb41acc24ea89781d799d863d4` |
| `responses/daily/mini_prose/cycle01/objection.json` | `9ca3ec0a86bbc754308e6d125aee3b8183b0a3b6682435cc4ac98a5383b4b5ca` |
| `responses/daily/mini_prose/cycle01/objection.txt` | `6ba2118d6a9e29b41ebd3e8eb34c7e0d66e02f78291e10c8633fedafa35ba284` |
| `responses/daily/mini_prose/cycle01/response.json` | `26d9ffe876b899d4da3746344d7d60d604793f802831a92632d9da20bab194bf` |
| `responses/daily/mini_prose/cycle01/response.txt` | `aaf80e0cec9b3800fbfd78292415d9e3e821711c2c68d15e47dbb0dc9ab61946` |
| `responses/daily/mini_prose/cycle01/rival.json` | `7c4809c5f78ea345e26eee5533d646e0f963801340c93e1649c9bac0c98d25f0` |
| `responses/daily/mini_prose/cycle01/rival.txt` | `12c8aed83e60465e8d1e35aa8e6c5475c0fc3f021cddd7484169198e8337fd69` |
| `traces/daily/bare/cycle01/answer.json` | `4ff68da01ac0c9cfd4c060d4a822f7ced327003f53e9e96f1e3fb08916a7fbab` |
| `traces/daily/mini_fcl/cycle01/account.json` | `f4790106152ef33f8f02cc8f182089bd4e99beb4f553144a79e51e2ec4f92f53` |
| `traces/daily/mini_fcl/cycle01/carry.json` | `8c5ebbcacef5e8f923fb5511c4d0486bc0c5f15793a96ef892971ded31248dfa` |
| `traces/daily/mini_fcl/cycle01/objection.json` | `58d06845a04f6c568ff6afd9798f41622496398852d7bb05cc1c1b5ed8ad446d` |
| `traces/daily/mini_fcl/cycle01/response.json` | `39d0057462189fd0379e8238a46df1c0468f2f15fa331af948bbe09d120c294a` |
| `traces/daily/mini_fcl/cycle01/rival.json` | `f1c8e8726237f993ba9a41a4df4a05e2d8390fee93c1e4e3b43553a3c2928604` |
| `traces/daily/mini_prose/cycle01/account.json` | `5725e108b01c89983c73bc7e84268aa9bbf8b77d8b6fe57c79df1137bd5db455` |
| `traces/daily/mini_prose/cycle01/carry.json` | `c3d0338e95f502f4de34abfc4d2e0552596d191e64e92e5e35fe37c9176876a9` |
| `traces/daily/mini_prose/cycle01/objection.json` | `82c9696517a03a9d09f4314a0b9ba2c70c56dabaefc8b2f8e1b318a019125ab0` |
| `traces/daily/mini_prose/cycle01/response.json` | `38bdb543f19f8d6b2eb79cfa503cfa11faf0007c6c3d2feba7ebcd99fc636b59` |
| `traces/daily/mini_prose/cycle01/rival.json` | `dd00b890d1cf82e091d0e50f87fda91e62b46d572e9d21336d795e69e5a45937` |
| `waves/wave0001.json` | `74c380d579b03ae1ee861954b64b785d3bca0e563a69a66e808ebda3b98778fd` |
| `waves/wave0002.json` | `0d47c0fb8eec3e34faab74d12677abe7d6d858e9086497789f5133b80fdbcd58` |
| `waves/wave0003.json` | `69c4a4e35d1c6ee9c814bb223ae0e60a80c99a19438cb7b4d6decfd3c3927a07` |
| `waves/wave0004.json` | `de7959a74506235246f65047ea2135715740d1223c9b1696a533d08f08c3828d` |

