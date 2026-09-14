# Use-relation table - H005 occurrence-03

**The tool records juxtapositions; the reading is root's.** This table places each authored cross-document reference beside passages a root reader may find worth starting from - a finding aid, never a closed search space - and stops there. It scores nothing, ranks nothing, classifies nothing and mints no relation of its own; it has no `att`, no `dep`, no status and no label. **A lexical overlap is not evidence of use.** FCL-1's own rule is that `depends` and `mentions` are "not automatically inferred from citation or lexical overlap"; a witness of reason use "must preserve internal role bindings, not merely the endpoint string" (FW5:628); actual use is "not automatically machine-maintainable" while prompt appearance is only a delivery fact (FW5:640); and no function of an input-output projection agrees with the accounting predicate across models differing in active route (FW5:1218), "semantic use inferred from delivery logs" included (FW5:1222) - all as summarised in the FW5-versus-harness-spec review, `fw5-vs-harness-spec-review.md` §1 R2-R4, §3.1 and §5 P1/P6. Root fills the four empty cells by reading; `unresolved` is a legal value and stays unresolved (FW5:634). An empty cell is an **unread row**, not a reading of `unresolved`.

Instrument: `use_relation_h005/1`. Schema: `h005-use-relation.use-table.v1`.

## Scope

- `daily/mini_fcl/cycle01/account`
- `daily/mini_fcl/cycle01/rival`

## Custody

- `plan_id`: `9aa92a837569bd56a86b172eb56dd80dbc69c519a86286d3387b020c2709a0d5`
- `material_sha256`: `aadea004b4722fb1b4878bc9c46e7ba8ef5883ff6bcbff4aac10020b6b017679`

| check | kind | result |
|---|---|---|
| `material_pin` | cross_file | verified (1/1 occurrence) |
| `manifest_pins` | cross_file | verified (3/3 manifests) |
| `receipt_present` | cross_file | verified (2/2 nodes) |
| `artifact_bytes_vs_receipt` | cross_file | verified (2/2 nodes) |
| `status_vs_receipt` | cross_file | verified (2/2 nodes) |
| `public_text` | cross_file | verified (2/2 nodes) |
| `attempt_vs_receipt` | cross_file | verified (2/2 nodes) |
| `request_record` | cross_file | verified (2/2 nodes) |
| `trace_pinned` | cross_file | verified (2/2 nodes) |
| `provider_bytes` | cross_file | verified (2/2 nodes) |
| `wave_placement` | cross_file | verified (2/2 nodes) |
| `projection_source` | cross_file | verified (1/2 projections; 1 projection(s) had no exposed source (the slot is absent): `daily/mini_fcl/cycle01/account#p.account.0`) |
| `plan_identity` | self_consistency | verified (1/1 occurrence) |
| `artifact_self_hash` | self_consistency | verified (2/2 nodes) |
| `artifact_coordinate` | self_consistency | verified (2/2 nodes) |
| `brief_pinned` | self_consistency | verified (2/2 nodes) |
| `brief_label_index` | self_consistency | verified (2/2 nodes) |
| `task_label` | self_consistency | verified (2/2 nodes) |

Custody is the importer's own check, reused unchanged; a self-consistency check cannot detect a coherent rewrite of the one file it reads.

## Method - exactly what the mechanical columns mean

**Sentence.** The referring node's `body` is cut at every match of the published boundary regular expression and nowhere else; leading and trailing whitespace is trimmed out of each span *and out of its offsets*, so `body[start:end]` is exactly the quoted sentence. The boundary is one or more of `.` `!` `?` preceded by a lowercase letter or a closing bracket/quote and followed by whitespace or end-of-string, together with any closing quotes that follow it; or a run of newlines. This is not linguistic sentence segmentation: a numbered list marker ("1. Separate ...") does not split, and an abbreviation such as "e.g." does.

**Token.** The string is lowercased and every maximal run of ASCII letters and digits is a token, in order of occurrence.

**The target record's text.** The concatenation, separated by single spaces, of the target record's prose fields in this order: `text`, `scope`, `action`, `consequence`, `grounds`, `bearing`. `id`, `type` and every ref array are excluded: they are names and pointers, not content. When the ref names the owning contribution as a whole rather than one of its records - a bare exposed-artifact label, or the `#BODY` section header - the subject is instead the same concatenation over **every** record of the owning document, in document order, and the row says so in `overlap_subject`.

**Distinctive token.** A token `t` of the target record's text is *distinctive* when all three hold: (1) `len(t) >= 5` characters after lowercasing; (2) `t` is not in the closed stopword list below; (3) `document_frequency(t) <= 2`, where `document_frequency(t)` is the number of in-scope FCL-1 documents whose record prose contains `t`, and the threshold is `max(2, number_of_in_scope_FCL-1_documents // 2)` - here `max(2, 2 // 2)`. Clause (3) makes the criterion **scope-dependent**: it is computed over the documents listed under `corpus_documents`, and re-running over a different scope can change which tokens count. That is stated rather than hidden, because a partition-invariance question about this instrument (review §5 P5) has to be answerable from its own output.

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
| refs walked | 52 |
| cross document rows | 0 |
| intra document | 48 |
| refs to exposed task artifact | 4 |
| unresolved | 0 |
| importer resolved counter | 52 |
| importer extension counter | 0 |
| importer dangling counter | 0 |

These are counts of authored refs, reported as information. No count here warrants anything (FW5:851: counts "are not outlawed as information"; what is forbidden is a count entering as an *automatic* warrant).

## Rows

*No cross-document reference in scope.*

## Declared uptake versus records present

### `daily/mini_fcl/cycle01/account`

- commitment surface: `read_fcl1`
- records present (11): `c1`, `c2`, `c3`, `c4`, `k1`, `k2`, `k3`, `o1`, `o2`, `p1`, `p2`
- declared `uptake` (11): `c1`, `c2`, `c3`, `c4`, `k1`, `k2`, `k3`, `o1`, `o2`, `p1`, `p2`
- records in uptake (11): `c1`, `c2`, `c3`, `c4`, `k1`, `k2`, `k3`, `o1`, `o2`, `p1`, `p2`
- records omitted from uptake (0): *none*
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/rival`

- commitment surface: `read_fcl1`
- records present (18): `c1`, `c2`, `c3`, `c4`, `c5`, `d1`, `r0`, `o1`, `o2`, `u1`, `p1`, `p2`, `p3`, `p4`, `p5`, `q1`, `q2`, `q3`
- declared `uptake` (6): `u1`, `p1`, `p2`, `p3`, `p4`, `p5`
- records in uptake (6): `u1`, `p1`, `p2`, `p3`, `p4`, `p5`
- records omitted from uptake (12): `c1`, `c2`, `c3`, `c4`, `c5`, `d1`, `r0`, `o1`, `o2`, `q1`, `q2`, `q3`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

## Nodes whose commitment surface was not read

*None in this scope.*

## Residue: refs that resolve to nothing

*No unresolved ref in this scope.*

## Files read

Every byte this instrument read, with its sha256. Nothing under the occurrence was written.

| path | sha256 |
|---|---|
| `artifacts/daily/mini_fcl/cycle01/account.json` | `c2fa20c2207f5101769613ac3f509a77fc29cac22ef1f6a65fd5f02e623e7834` |
| `artifacts/daily/mini_fcl/cycle01/rival.json` | `402e859a9e05056122a7342538b25a54fd17ab513cf1438ec35be272cd84babf` |
| `attempts/daily/mini_fcl/cycle01/account.json` | `802119c5790d2c264fd768450f4d4c80ee23f1ad230ab7c55d27a61adbfd48ab` |
| `attempts/daily/mini_fcl/cycle01/rival.json` | `3a0aa3bcf2f5e3babecd22e7a26b346ee1cdddbe2d29b3fdc2f69759b652a843` |
| `manifests/fork5.json` | `8f2d928b2f70298906b17d62e73b41804efa754d845f018d9eb312af7dcb536a` |
| `manifests/return6.json` | `bad1f6dc4ddda462f1b3acaa56a9e552eeb98255509cb4bfa3353c2305abb3b5` |
| `manifests/weave7.json` | `0b8a5f337f754b23fd51721ff287e25347af99648a7d2b00ad73b7baa571c2cb` |
| `material.json` | `aadea004b4722fb1b4878bc9c46e7ba8ef5883ff6bcbff4aac10020b6b017679` |
| `plan.json` | `bed7e150c5b116fcb60feaf1e9893f39d23c957af815e86c7c3400984f74e995` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | `bb60087d00a790b8bf7f07e65a3cd9f8a83efd7e895027e95913016052222112` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | `4f5f54030b593ee38c89a998ba068eff5c1990c865706eb6b35ed94d79a708ff` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | `de0af1cdf278c9cbb06b63f45eee333062adf86e2761481d14f57a8f869b8715` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | `ff5653e789ad7b50719ba15aa7003b31a3674b574f1bea3e9a2df4fb966e2070` |
| `requests/daily/mini_fcl/cycle01/account.json` | `4d9836af307533b79d05ab6654ad6578035463b8db43fb01cc71056f715f9e1f` |
| `requests/daily/mini_fcl/cycle01/rival.json` | `a4f41495f4f2a498505791af5584355c0248d687d36480255697057b7375184c` |
| `responses/daily/mini_fcl/cycle01/account.json` | `79a4f545e1fad4e5556dd8de8fe80b4d1826b2256feab527546dbda95f8acee3` |
| `responses/daily/mini_fcl/cycle01/account.txt` | `e39c114c2e7a25b1d320d70d528f72ca2c1de39dea7fc147d4deac9744cdfcb0` |
| `responses/daily/mini_fcl/cycle01/rival.json` | `a615ffd9ff81a0f33de2e7e1e2405315fdb86f2ed15fb515bae19f7bdc71844b` |
| `responses/daily/mini_fcl/cycle01/rival.txt` | `82719e25c2b7c66ef34c28a6b49e4fef673f604dbf6991192e15a0aa20c740f0` |
| `traces/daily/mini_fcl/cycle01/account.json` | `f4790106152ef33f8f02cc8f182089bd4e99beb4f553144a79e51e2ec4f92f53` |
| `traces/daily/mini_fcl/cycle01/rival.json` | `7c25d8128dda6536868fa3193ea0554fb8c9a9ff018f8f693364403b78454f63` |
| `waves/wave0001.json` | `811db21379fb35385cb377860b62f385de0cac9f425fdd188cc5a1b21883cadd` |
| `waves/wave0002.json` | `cfb4dd06c3035e8ce6cc30514265a62072f891794067df9aa39bac86135fd886` |

