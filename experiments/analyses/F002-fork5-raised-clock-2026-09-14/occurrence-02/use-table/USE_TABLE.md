# Use-relation table - H005 occurrence-02

**The tool records juxtapositions; the reading is root's.** This table places each authored cross-document reference beside passages a root reader may find worth starting from - a finding aid, never a closed search space - and stops there. It scores nothing, ranks nothing, classifies nothing and mints no relation of its own; it has no `att`, no `dep`, no status and no label. **A lexical overlap is not evidence of use.** FCL-1's own rule is that `depends` and `mentions` are "not automatically inferred from citation or lexical overlap"; a witness of reason use "must preserve internal role bindings, not merely the endpoint string" (FW5:628); actual use is "not automatically machine-maintainable" while prompt appearance is only a delivery fact (FW5:640); and no function of an input-output projection agrees with the accounting predicate across models differing in active route (FW5:1218), "semantic use inferred from delivery logs" included (FW5:1222) - all as summarised in the FW5-versus-harness-spec review, `fw5-vs-harness-spec-review.md` §1 R2-R4, §3.1 and §5 P1/P6. Root fills the four empty cells by reading; `unresolved` is a legal value and stays unresolved (FW5:634). An empty cell is an **unread row**, not a reading of `unresolved`.

Instrument: `use_relation_h005/1`. Schema: `h005-use-relation.use-table.v1`.

## Scope

- `daily/mini_fcl/cycle01/account`
- `daily/mini_fcl/cycle01/objection`
- `daily/mini_fcl/cycle01/rival`
- `daily/mini_fcl/cycle01/response`
- `daily/mini_fcl/cycle01/carry`

## Custody

- `plan_id`: `a59debaf6382ce7c01c4c07d14894890736e2a960b66d4323f9eb84ac72b1163`
- `material_sha256`: `aadea004b4722fb1b4878bc9c46e7ba8ef5883ff6bcbff4aac10020b6b017679`

| check | kind | result |
|---|---|---|
| `material_pin` | cross_file | verified (1/1 occurrence) |
| `manifest_pins` | cross_file | verified (3/3 manifests) |
| `receipt_present` | cross_file | verified (5/5 nodes) |
| `artifact_bytes_vs_receipt` | cross_file | verified (5/5 nodes) |
| `status_vs_receipt` | cross_file | verified (5/5 nodes) |
| `public_text` | cross_file | verified (5/5 nodes) |
| `attempt_vs_receipt` | cross_file | verified (5/5 nodes) |
| `request_record` | cross_file | verified (5/5 nodes) |
| `trace_pinned` | cross_file | verified (5/5 nodes) |
| `provider_bytes` | cross_file | verified (5/5 nodes) |
| `wave_placement` | cross_file | verified (5/5 nodes) |
| `projection_source` | cross_file | verified (8/10 projections; 2 projection(s) had no exposed source (the slot is absent): `daily/mini_fcl/cycle01/account#p.account.0`, `daily/mini_fcl/cycle01/carry#p.carry.3`) |
| `plan_identity` | self_consistency | verified (1/1 occurrence) |
| `artifact_self_hash` | self_consistency | verified (5/5 nodes) |
| `artifact_coordinate` | self_consistency | verified (5/5 nodes) |
| `brief_pinned` | self_consistency | verified (5/5 nodes) |
| `brief_label_index` | self_consistency | verified (5/5 nodes) |
| `task_label` | self_consistency | verified (5/5 nodes) |

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
| refs walked | 216 |
| cross document rows | 0 |
| intra document | 63 |
| refs to exposed task artifact | 0 |
| unresolved | 153 |
| importer resolved counter | 63 |
| importer extension counter | 0 |
| importer dangling counter | 153 |

These are counts of authored refs, reported as information. No count here warrants anything (FW5:851: counts "are not outlawed as information"; what is forbidden is a count entering as an *automatic* warrant).

## Rows

*No cross-document reference in scope.*

## Declared uptake versus records present

### `daily/mini_fcl/cycle01/account`

- commitment surface: `read_fcl1`
- records present (10): `c1`, `c2`, `c3`, `cm1`, `cm2`, `cm3`, `cm4`, `p1`, `p2`, `o1`
- declared `uptake` (9): `c1`, `c2`, `c3`, `cm1`, `cm2`, `cm3`, `cm4`, `p1`, `p2`
- records in uptake (9): `c1`, `c2`, `c3`, `cm1`, `cm2`, `cm3`, `cm4`, `p1`, `p2`
- records omitted from uptake (1): `o1`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/objection`

- commitment surface: `read_fcl1`
- records present (10): `n1`, `ob1`, `n2`, `ob2`, `ob3`, `ob4`, `ob5`, `u1`, `pr1`, `pr2`
- declared `uptake` (17): `n1`, `n2`, `ob1`, `ob2`, `ob3`, `ob4`, `ob5`, `u1`, `pr1`, `pr2`, `h005.fork5.p.objection.0#c1`, `h005.fork5.p.objection.0#c2`, `h005.fork5.p.objection.0#cm2`, `h005.fork5.p.objection.0#cm3`, `h005.fork5.p.objection.0#p1`, `h005.fork5.p.objection.0#p2`, `h005.fork5.p.objection.0#o1`
- records in uptake (10): `n1`, `ob1`, `n2`, `ob2`, `ob3`, `ob4`, `ob5`, `u1`, `pr1`, `pr2`
- records omitted from uptake (0): *none*
- uptake entries naming nothing (7): `h005.fork5.p.objection.0#c1`, `h005.fork5.p.objection.0#c2`, `h005.fork5.p.objection.0#cm2`, `h005.fork5.p.objection.0#cm3`, `h005.fork5.p.objection.0#p1`, `h005.fork5.p.objection.0#p2`, `h005.fork5.p.objection.0#o1`
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/rival`

- commitment surface: `read_fcl1`
- records present (7): `r1`, `r2`, `r3`, `r4`, `r5`, `r6`, `r7`
- declared `uptake` (7): `r1`, `r2`, `r3`, `r4`, `r5`, `r6`, `r7`
- records in uptake (7): `r1`, `r2`, `r3`, `r4`, `r5`, `r6`, `r7`
- records omitted from uptake (0): *none*
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/response`

- commitment surface: `read_fcl1`
- records present (11): `k1`, `k2`, `k3`, `k4`, `k5`, `k6`, `j1`, `j2`, `pA`, `pB`, `pC`
- declared `uptake` (33): `k1`, `k2`, `k3`, `k4`, `k5`, `k6`, `j1`, `j2`, `pA`, `pB`, `pC`, `h005.fork5.p.response.0#c1`, `h005.fork5.p.response.0#c2`, `h005.fork5.p.response.0#cm2`, `h005.fork5.p.response.0#cm3`, `h005.fork5.p.response.0#cm4`, `h005.fork5.p.response.0#p1`, `h005.fork5.p.response.0#p2`, `h005.fork5.p.response.0#o1`, `h005.fork5.p.response.1#n1`, `h005.fork5.p.response.1#n2`, `h005.fork5.p.response.1#ob1`, `h005.fork5.p.response.1#ob2`, `h005.fork5.p.response.1#ob3`, `h005.fork5.p.response.1#ob4`, `h005.fork5.p.response.1#ob5`, `h005.fork5.p.response.1#u1`, `h005.fork5.p.response.1#pr1`, `h005.fork5.p.response.1#pr2`, `h005.fork5.p.response.2#r2`, `h005.fork5.p.response.2#r4`, `h005.fork5.p.response.2#r6`, `h005.fork5.p.response.2#r7`
- records in uptake (11): `k1`, `k2`, `k3`, `k4`, `k5`, `k6`, `j1`, `j2`, `pA`, `pB`, `pC`
- records omitted from uptake (0): *none*
- uptake entries naming nothing (22): `h005.fork5.p.response.0#c1`, `h005.fork5.p.response.0#c2`, `h005.fork5.p.response.0#cm2`, `h005.fork5.p.response.0#cm3`, `h005.fork5.p.response.0#cm4`, `h005.fork5.p.response.0#p1`, `h005.fork5.p.response.0#p2`, `h005.fork5.p.response.0#o1`, `h005.fork5.p.response.1#n1`, `h005.fork5.p.response.1#n2`, `h005.fork5.p.response.1#ob1`, `h005.fork5.p.response.1#ob2`, `h005.fork5.p.response.1#ob3`, `h005.fork5.p.response.1#ob4`, `h005.fork5.p.response.1#ob5`, `h005.fork5.p.response.1#u1`, `h005.fork5.p.response.1#pr1`, `h005.fork5.p.response.1#pr2`, `h005.fork5.p.response.2#r2`, `h005.fork5.p.response.2#r4`, `h005.fork5.p.response.2#r6`, `h005.fork5.p.response.2#r7`
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/carry`

- commitment surface: `read_fcl1`
- records present (4): `d1`, `d2`, `d3`, `d4`
- declared `uptake` (34): `d1`, `d2`, `d3`, `d4`, `h005.fork5.p.carry.0#k1`, `h005.fork5.p.carry.0#k2`, `h005.fork5.p.carry.0#k3`, `h005.fork5.p.carry.0#k4`, `h005.fork5.p.carry.0#k5`, `h005.fork5.p.carry.0#k6`, `h005.fork5.p.carry.0#j1`, `h005.fork5.p.carry.0#j2`, `h005.fork5.p.carry.0#pA`, `h005.fork5.p.carry.0#pB`, `h005.fork5.p.carry.0#pC`, `h005.fork5.p.carry.1#c1`, `h005.fork5.p.carry.1#c2`, `h005.fork5.p.carry.1#c3`, `h005.fork5.p.carry.1#cm2`, `h005.fork5.p.carry.1#cm3`, `h005.fork5.p.carry.1#cm4`, `h005.fork5.p.carry.1#p1`, `h005.fork5.p.carry.1#p2`, `h005.fork5.p.carry.1#o1`, `h005.fork5.p.carry.2#n1`, `h005.fork5.p.carry.2#n2`, `h005.fork5.p.carry.2#ob1`, `h005.fork5.p.carry.2#ob2`, `h005.fork5.p.carry.2#ob3`, `h005.fork5.p.carry.2#ob4`, `h005.fork5.p.carry.2#ob5`, `h005.fork5.p.carry.2#u1`, `h005.fork5.p.carry.2#pr1`, `h005.fork5.p.carry.2#pr2`
- records in uptake (4): `d1`, `d2`, `d3`, `d4`
- records omitted from uptake (0): *none*
- uptake entries naming nothing (30): `h005.fork5.p.carry.0#k1`, `h005.fork5.p.carry.0#k2`, `h005.fork5.p.carry.0#k3`, `h005.fork5.p.carry.0#k4`, `h005.fork5.p.carry.0#k5`, `h005.fork5.p.carry.0#k6`, `h005.fork5.p.carry.0#j1`, `h005.fork5.p.carry.0#j2`, `h005.fork5.p.carry.0#pA`, `h005.fork5.p.carry.0#pB`, `h005.fork5.p.carry.0#pC`, `h005.fork5.p.carry.1#c1`, `h005.fork5.p.carry.1#c2`, `h005.fork5.p.carry.1#c3`, `h005.fork5.p.carry.1#cm2`, `h005.fork5.p.carry.1#cm3`, `h005.fork5.p.carry.1#cm4`, `h005.fork5.p.carry.1#p1`, `h005.fork5.p.carry.1#p2`, `h005.fork5.p.carry.1#o1`, `h005.fork5.p.carry.2#n1`, `h005.fork5.p.carry.2#n2`, `h005.fork5.p.carry.2#ob1`, `h005.fork5.p.carry.2#ob2`, `h005.fork5.p.carry.2#ob3`, `h005.fork5.p.carry.2#ob4`, `h005.fork5.p.carry.2#ob5`, `h005.fork5.p.carry.2#u1`, `h005.fork5.p.carry.2#pr1`, `h005.fork5.p.carry.2#pr2`
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

## Nodes whose commitment surface was not read

*None in this scope.*

## Residue: refs that resolve to nothing

| referring coordinate | record | field | ref | code | reason |
|---|---|---|---|---|---|
| `daily/mini_fcl/cycle01/objection` | `n1` | `mentions` | `h005.fork5.p.objection.0#c1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `n2` | `mentions` | `h005.fork5.p.objection.0#cm2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `n2` | `mentions` | `h005.fork5.p.objection.0#p1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob2` | `mentions` | `h005.fork5.p.objection.0#o1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob2` | `mentions` | `h005.fork5.p.objection.0#p1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob4` | `mentions` | `h005.fork5.p.objection.0#c3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob4` | `mentions` | `h005.fork5.p.objection.0#p1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `u1` | `mentions` | `h005.fork5.p.objection.0#cm2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `u1` | `mentions` | `h005.fork5.p.objection.0#cm4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `u1` | `mentions` | `h005.fork5.p.objection.0#p2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `pr1` | `mentions` | `h005.fork5.p.objection.0#c1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `pr2` | `mentions` | `h005.fork5.p.objection.0#cm4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `-` | `uptake` | `h005.fork5.p.objection.0#c1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `-` | `uptake` | `h005.fork5.p.objection.0#c2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `-` | `uptake` | `h005.fork5.p.objection.0#cm2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `-` | `uptake` | `h005.fork5.p.objection.0#cm3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `-` | `uptake` | `h005.fork5.p.objection.0#p1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `-` | `uptake` | `h005.fork5.p.objection.0#p2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `-` | `uptake` | `h005.fork5.p.objection.0#o1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob1` | `target` | `h005.fork5.p.objection.0#c1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob1` | `target` | `h005.fork5.p.objection.0#cm2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob2` | `target` | `h005.fork5.p.objection.0#cm2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob2` | `target` | `h005.fork5.p.objection.0#cm3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob3` | `target` | `h005.fork5.p.objection.0#cm2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob3` | `target` | `h005.fork5.p.objection.0#cm4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob4` | `target` | `h005.fork5.p.objection.0#cm1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob5` | `target` | `h005.fork5.p.objection.0#cm1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `ob5` | `target` | `h005.fork5.p.objection.0#cm2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k1` | `mentions` | `h005.fork5.p.response.0#p1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k1` | `mentions` | `h005.fork5.p.response.0#cm1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k1` | `mentions` | `h005.fork5.p.response.1#ob4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k1` | `mentions` | `h005.fork5.p.response.1#ob5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k1` | `mentions` | `h005.fork5.p.response.2#r4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k1` | `mentions` | `h005.fork5.p.response.2#r5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k2` | `revises` | `h005.fork5.p.response.0#cm3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k2` | `depends` | `h005.fork5.p.response.1#n1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k2` | `depends` | `h005.fork5.p.response.1#ob1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k3` | `mentions` | `h005.fork5.p.response.1#pr2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k3` | `revises` | `h005.fork5.p.response.0#cm4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k3` | `depends` | `h005.fork5.p.response.1#ob3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k3` | `depends` | `h005.fork5.p.response.1#u1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k4` | `mentions` | `h005.fork5.p.response.0#p2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k4` | `mentions` | `h005.fork5.p.response.0#o1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k4` | `revises` | `h005.fork5.p.response.0#cm2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k4` | `depends` | `h005.fork5.p.response.1#ob2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k4` | `depends` | `h005.fork5.p.response.1#n2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k4` | `depends` | `h005.fork5.p.response.1#u1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k5` | `mentions` | `h005.fork5.p.response.0#p1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k5` | `mentions` | `h005.fork5.p.response.0#c3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k5` | `mentions` | `h005.fork5.p.response.2#r5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k5` | `revises` | `h005.fork5.p.response.0#cm1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k5` | `depends` | `h005.fork5.p.response.1#ob4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k5` | `depends` | `h005.fork5.p.response.1#ob5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k5` | `depends` | `h005.fork5.p.response.2#r4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k6` | `mentions` | `h005.fork5.p.response.1#pr1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k6` | `mentions` | `h005.fork5.p.response.2#r5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k6` | `mentions` | `h005.fork5.p.response.2#r3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k6` | `mentions` | `h005.fork5.p.response.0#c3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k6` | `depends` | `h005.fork5.p.response.2#r6` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `k6` | `depends` | `h005.fork5.p.response.2#r7` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `j1` | `mentions` | `h005.fork5.p.response.1#ob5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `j1` | `mentions` | `h005.fork5.p.response.2#r3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `j1` | `mentions` | `h005.fork5.p.response.2#r6` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `j2` | `mentions` | `h005.fork5.p.response.2#r5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `j2` | `mentions` | `h005.fork5.p.response.0#c2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `j2` | `mentions` | `h005.fork5.p.response.2#r2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `pA` | `mentions` | `h005.fork5.p.response.0#p1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `pB` | `mentions` | `h005.fork5.p.response.0#c1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `pB` | `mentions` | `h005.fork5.p.response.2#r1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.0#c1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.0#c2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.0#cm2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.0#cm3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.0#cm4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.0#p1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.0#p2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.0#o1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.1#n1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.1#n2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.1#ob1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.1#ob2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.1#ob3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.1#ob4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.1#ob5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.1#u1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.1#pr1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.1#pr2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.2#r2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.2#r4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.2#r6` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `-` | `uptake` | `h005.fork5.p.response.2#r7` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `j1` | `target` | `h005.fork5.p.response.2#r5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d1` | `mentions` | `h005.fork5.p.carry.0#k1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d1` | `mentions` | `h005.fork5.p.carry.1#c1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d1` | `mentions` | `h005.fork5.p.carry.1#cm2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d1` | `mentions` | `h005.fork5.p.carry.2#ob1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d1` | `mentions` | `h005.fork5.p.carry.2#ob4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d1` | `mentions` | `h005.fork5.p.carry.2#ob5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d2` | `mentions` | `h005.fork5.p.carry.2#pr2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d2` | `mentions` | `h005.fork5.p.carry.0#k4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d2` | `mentions` | `h005.fork5.p.carry.0#k2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d2` | `revises` | `h005.fork5.p.carry.0#k3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d2` | `depends` | `h005.fork5.p.carry.0#k3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d2` | `depends` | `h005.fork5.p.carry.0#k5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d2` | `depends` | `h005.fork5.p.carry.2#ob3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d2` | `depends` | `h005.fork5.p.carry.1#cm3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d3` | `mentions` | `h005.fork5.p.carry.0#k1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d3` | `mentions` | `h005.fork5.p.carry.0#k2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d3` | `mentions` | `h005.fork5.p.carry.0#k3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d3` | `mentions` | `h005.fork5.p.carry.0#k4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d3` | `mentions` | `h005.fork5.p.carry.0#k5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d3` | `mentions` | `h005.fork5.p.carry.0#k6` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d3` | `mentions` | `h005.fork5.p.carry.0#j1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d3` | `mentions` | `h005.fork5.p.carry.0#j2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d3` | `mentions` | `h005.fork5.p.carry.0#pA` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d3` | `mentions` | `h005.fork5.p.carry.0#pB` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d3` | `mentions` | `h005.fork5.p.carry.0#pC` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d3` | `mentions` | `h005.fork5.p.carry.1#cm1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d4` | `mentions` | `h005.fork5.p.carry.0#k1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d4` | `mentions` | `h005.fork5.p.carry.0#k5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d4` | `mentions` | `h005.fork5.p.carry.0#k6` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d4` | `mentions` | `h005.fork5.p.carry.0#j1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `d4` | `mentions` | `h005.fork5.p.carry.0#pB` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.0#k1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.0#k2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.0#k3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.0#k4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.0#k5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.0#k6` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.0#j1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.0#j2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.0#pA` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.0#pB` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.0#pC` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.1#c1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.1#c2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.1#c3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.1#cm2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.1#cm3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.1#cm4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.1#p1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.1#p2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.1#o1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.2#n1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.2#n2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.2#ob1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.2#ob2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.2#ob3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.2#ob4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.2#ob5` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.2#u1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.2#pr1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/carry` | `-` | `uptake` | `h005.fork5.p.carry.2#pr2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |

## Files read

Every byte this instrument read, with its sha256. Nothing under the occurrence was written.

| path | sha256 |
|---|---|
| `artifacts/daily/mini_fcl/cycle01/account.json` | `968aa1c41706a929e97b35590df51f4f6f9b8228b33e3accf9ee4b6e582a2e51` |
| `artifacts/daily/mini_fcl/cycle01/carry.json` | `aff3f6ca406a47739ae38526ef96ad601840e2ff6a3af7d5c5a7ae3b7e5b28c1` |
| `artifacts/daily/mini_fcl/cycle01/objection.json` | `5d5b6e79dee79b52281c4d166d415e64e4dfef0c28f2956ef60b42518f7d59e2` |
| `artifacts/daily/mini_fcl/cycle01/response.json` | `ad579ff00b132485b97455fa171c86b35f1158712bae6ef9fa41bb4b594d42e0` |
| `artifacts/daily/mini_fcl/cycle01/rival.json` | `f18b99266bacec85a48c89bee4496f971be0265a7115361cb9ffc69917ab1a8b` |
| `attempts/daily/mini_fcl/cycle01/account.json` | `5624baaf47e6e69b73243c907d8221522bb23007964712434bfe5b9f564c7a76` |
| `attempts/daily/mini_fcl/cycle01/carry.json` | `c4b29373340531802d8b564df6e054852831f58171aa3036f67f3051306b4cd3` |
| `attempts/daily/mini_fcl/cycle01/objection.json` | `31f1c7b6af5ae047407259db24909074b20795d6b6f11543cc68ab757c6b08a5` |
| `attempts/daily/mini_fcl/cycle01/response.json` | `7820843b8e040b888e640e11f4c376a04a392b19c6f4c702bc15f9d436c0378b` |
| `attempts/daily/mini_fcl/cycle01/rival.json` | `623b715be2b2d422b66616279a3c3e910e57e86dfe48a3d8066e89218867620b` |
| `manifests/fork5.json` | `8f2d928b2f70298906b17d62e73b41804efa754d845f018d9eb312af7dcb536a` |
| `manifests/return6.json` | `bad1f6dc4ddda462f1b3acaa56a9e552eeb98255509cb4bfa3353c2305abb3b5` |
| `manifests/weave7.json` | `0b8a5f337f754b23fd51721ff287e25347af99648a7d2b00ad73b7baa571c2cb` |
| `material.json` | `aadea004b4722fb1b4878bc9c46e7ba8ef5883ff6bcbff4aac10020b6b017679` |
| `plan.json` | `a4420dfbaff1ea9f5a3971be1f2b2ac9396e7edca7fde70daec9a49a39c7ef54` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | `76ef5edd5d1f3f36e537a085cd977072e2fd91247e2d7d81e4900feb694c61c4` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | `d5c5075b59fd1c599d26e237a8caed94afeb3c5afcb6261622f5a260f274b76a` |
| `provider/daily/mini_fcl/cycle01/carry/call-0001.request.json` | `7ddc4d7c6e00c50d702326bb093722bb1446f3a0e217d56230d4cfb442b8015a` |
| `provider/daily/mini_fcl/cycle01/carry/call-0001.response.json` | `8a12bb5447f1b6fea89fb325f359bc841358b615f735c397b81dcbd969973548` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.request.json` | `fc834104d86d012cf4aafe30f86b7f2d95b04ec1a7d816dd8b8b14ea12de5312` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.response.json` | `a80309b9f784f339d8d7cd1ad42aada658787a1fe5f7d27e35080d2450d81975` |
| `provider/daily/mini_fcl/cycle01/response/call-0001.request.json` | `30bbd1203dd9112ba7e3f660fe5d23115e46fe113c11eae6bd47a8f22e90403b` |
| `provider/daily/mini_fcl/cycle01/response/call-0001.response.json` | `44504da99e7ba7b7a5fbaff4aed96dbb23d531893b91779b174c9721776c3cd4` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | `63b6e7502133cd1b40d5b7e959b9ac5e7de873966bbd776153d6c2938a00b89b` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | `cb34667256f179b2df128f5815d7d5afa8c388700fae18d8fd3c6ed72e598b3f` |
| `requests/daily/mini_fcl/cycle01/account.json` | `fb3f0aaa79e3f036b9b992ec4644dd637344502057837ea12060ee0e743fe720` |
| `requests/daily/mini_fcl/cycle01/carry.json` | `0e2961c5eb70670da4def8a4e6b3d543c69e476d6261b3ff496219ed8a8a8764` |
| `requests/daily/mini_fcl/cycle01/objection.json` | `3268a066b48b4e7a35b84a4df1dffd0da86ded54d4a8593e1bbdfeeb3ac16dbe` |
| `requests/daily/mini_fcl/cycle01/response.json` | `e5b47c0ead2e3552ba17646ef341eb3dfbdaa42e1def2a7dd5da2c443bfbaf0c` |
| `requests/daily/mini_fcl/cycle01/rival.json` | `bf9d85fe9a1e90e218b146e1e1a8c001ad8ae9a9adea8445eb07ff38a346fb18` |
| `responses/daily/mini_fcl/cycle01/account.json` | `35242bad7cf6e82c7a148cddda1256fce226ab06cddc8b03c1e0bdb39c080c26` |
| `responses/daily/mini_fcl/cycle01/account.txt` | `e7bd8672abee3460471194a1a3065a5b87ca655b787508693a367db1d73f9dd1` |
| `responses/daily/mini_fcl/cycle01/carry.json` | `6031aae11595f7527a552d46a32677bb8a9cdcd8eb0c8366a893a6647297c527` |
| `responses/daily/mini_fcl/cycle01/carry.txt` | `a4662a89cd02b3a767bf708e7f8feb72b66637e7753b948ac1cae36663f3aea1` |
| `responses/daily/mini_fcl/cycle01/objection.json` | `c4b0c2934232c0f873fe50b2c1f0e8e46d071fe7661153bd7967a8a5ccd45352` |
| `responses/daily/mini_fcl/cycle01/objection.txt` | `105c9afe90b1e09192262a63f8480dafb794372e73d3484fdaf6eb85ba929fcf` |
| `responses/daily/mini_fcl/cycle01/response.json` | `3515f29d751c20021171bbfc7d6d6c4179e32b94385eba3b2585eccee80c3942` |
| `responses/daily/mini_fcl/cycle01/response.txt` | `97b610e08a1f41a7b3e8a7c43940c947ca84828eaa67b42f34e420e407016c27` |
| `responses/daily/mini_fcl/cycle01/rival.json` | `f564fb728cb5016aa0b85a25df479ff99c81ecbec39700f96a91a29df7a4a3d7` |
| `responses/daily/mini_fcl/cycle01/rival.txt` | `7b65fccfa2e3bcc58b5ea73475eb3b8c4d79eff2a244095929ed014738eeb1c0` |
| `traces/daily/mini_fcl/cycle01/account.json` | `f4790106152ef33f8f02cc8f182089bd4e99beb4f553144a79e51e2ec4f92f53` |
| `traces/daily/mini_fcl/cycle01/carry.json` | `569787c26f109beefd3434ade9cd4800d407751dc4089d9f95f0a07512c2ca3f` |
| `traces/daily/mini_fcl/cycle01/objection.json` | `333713cdc14311614bac2b4cc6f86ca92d7b7a133c770f224f96cb8e3999658b` |
| `traces/daily/mini_fcl/cycle01/response.json` | `afb13ce83e1e885a0d1e840344f6a6f8bdcf3d253ba489f2bca30fe18bcd3db7` |
| `traces/daily/mini_fcl/cycle01/rival.json` | `3912ba306f34e65a76b3e209e5d7b4dc9b522bf5260e8f6a2561e8f43f843f71` |
| `waves/wave0001.json` | `e048b42bf69236bf32fd8c31f3a1b41c0d511e92f5ead634fab667d4d1a03ab5` |
| `waves/wave0002.json` | `c80c5c9f8111df0502e8bce18d898462cc47a0ab9cd68dacd2c35ed3539b2d86` |
| `waves/wave0003.json` | `205b23346724b057cb12d71ffc4b516222258d0084fa7548455d040062ca2f87` |
| `waves/wave0004.json` | `193faa973d6342fe5a523b1ccd510a0312d893a53fb5e3b1b8264181182cf4fb` |

