# Use-relation table - H005 occurrence-02

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

- `plan_id`: `951ad3c58cb341f12ac922cab580e02879138d5d6cc626a0f9825af3ed29b3db`
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
| refs walked | 15 |
| cross document rows | 0 |
| intra document | 4 |
| refs to exposed task artifact | 0 |
| unresolved | 11 |
| importer resolved counter | 4 |
| importer extension counter | 0 |
| importer dangling counter | 11 |

These are counts of authored refs, reported as information. No count here warrants anything (FW5:851: counts "are not outlawed as information"; what is forbidden is a count entering as an *automatic* warrant).

## Rows

*No cross-document reference in scope.*

## Declared uptake versus records present

### `daily/mini_fcl/cycle01/account`

- commitment surface: `read_fcl1`
- records present (7): `r1`, `r2`, `r3`, `r4`, `r5`, `r6`, `r7`
- declared `uptake` (0): *none*
- records in uptake (0): *none*
- records omitted from uptake (7): `r1`, `r2`, `r3`, `r4`, `r5`, `r6`, `r7`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/objection`

- commitment surface: `read_fcl1`
- records present (5): `r8`, `r9`, `r10`, `r11`, `r12`
- declared `uptake` (7): `r1`, `r2`, `r3`, `r4`, `r5`, `r6`, `r7`
- records in uptake (0): *none*
- records omitted from uptake (5): `r8`, `r9`, `r10`, `r11`, `r12`
- uptake entries naming nothing (7): `r1`, `r2`, `r3`, `r4`, `r5`, `r6`, `r7`
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/rival`

- commitment surface: `read_fcl1`
- records present (4): `r1`, `r2`, `r3`, `r4`
- declared `uptake` (0): *none*
- records in uptake (0): *none*
- records omitted from uptake (4): `r1`, `r2`, `r3`, `r4`
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
- `daily/mini_fcl/cycle01/response` - commitment surface: parse_failure; references not extractable by this instrument
- `daily/mini_prose/cycle01/response` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_fcl/cycle01/carry` - commitment surface: parse_failure; references not extractable by this instrument
- `daily/mini_prose/cycle01/carry` - commitment surface: prose (not parsed); references not extractable by this instrument

## Residue: refs that resolve to nothing

| referring coordinate | record | field | ref | code | reason |
|---|---|---|---|---|---|
| `daily/mini_fcl/cycle01/objection` | `r8` | `depends` | `r1` | `ref_unresolved` | neither a local record name nor an exposed-artifact label; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `r9` | `depends` | `r5` | `ref_unresolved` | neither a local record name nor an exposed-artifact label; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `r10` | `depends` | `r3` | `ref_unresolved` | neither a local record name nor an exposed-artifact label; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `r11` | `depends` | `r4` | `ref_unresolved` | neither a local record name nor an exposed-artifact label; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `-` | `uptake` | `r1` | `ref_unresolved` | neither a local record name nor an exposed-artifact label; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `-` | `uptake` | `r2` | `ref_unresolved` | neither a local record name nor an exposed-artifact label; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `-` | `uptake` | `r3` | `ref_unresolved` | neither a local record name nor an exposed-artifact label; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `-` | `uptake` | `r4` | `ref_unresolved` | neither a local record name nor an exposed-artifact label; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `-` | `uptake` | `r5` | `ref_unresolved` | neither a local record name nor an exposed-artifact label; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `-` | `uptake` | `r6` | `ref_unresolved` | neither a local record name nor an exposed-artifact label; dropped, never invented |
| `daily/mini_fcl/cycle01/objection` | `-` | `uptake` | `r7` | `ref_unresolved` | neither a local record name nor an exposed-artifact label; dropped, never invented |

## Files read

Every byte this instrument read, with its sha256. Nothing under the occurrence was written.

| path | sha256 |
|---|---|
| `artifacts/daily/bare/cycle01/answer.json` | `f9fccbf0829879365eb9e2590482cd77b1dc21dbb9a89be7446d5e4ce1496843` |
| `artifacts/daily/mini_fcl/cycle01/account.json` | `d42bb4fe95dd750a782409ea27b0967442f841a050b54e9f103a6e314d255931` |
| `artifacts/daily/mini_fcl/cycle01/carry.json` | `b65a344869c39a49b162ebdb68790d44faa606865cef4b62111ee2ac22a31ba0` |
| `artifacts/daily/mini_fcl/cycle01/objection.json` | `de866de7fdbadea24291ecfa6a74027fa6d6b95620005e38752612c3a20cbb09` |
| `artifacts/daily/mini_fcl/cycle01/response.json` | `213d67082128cd0e13fda2b39c45b6f2aa67e863f57a9f0e2b388ecffdeb2d4b` |
| `artifacts/daily/mini_fcl/cycle01/rival.json` | `0ada966d21486a6952db0eeeff99d233246021acc53248eaa7c5f5e651e5d515` |
| `artifacts/daily/mini_prose/cycle01/account.json` | `f464fa0feb6c4cf9d08b43ec65cd7874bf1f07d856690a1bda83b3fb9c265f57` |
| `artifacts/daily/mini_prose/cycle01/carry.json` | `7f9fabdf5fa0a7b12f3545eff8744d3031c2febc55a9289ec0a0a415aadb31cf` |
| `artifacts/daily/mini_prose/cycle01/objection.json` | `02c4d8e4fea7d1c605754c7755eadf6507040dc5961b17c89fca8d9de722556f` |
| `artifacts/daily/mini_prose/cycle01/response.json` | `ba8a3d41440cce94aee5d864bb7e68380f49ab8f91abd4b6f05b0e280b83cf66` |
| `artifacts/daily/mini_prose/cycle01/rival.json` | `84c2c602b38c22ce1f3d3457bd1dac50617f976a088c8d5f5eea065d05cda66f` |
| `attempts/daily/bare/cycle01/answer.json` | `2ae27bf2087f6cceaf9ce8ee49d8042b27706748cb5390e7994c23c6a165dc88` |
| `attempts/daily/mini_fcl/cycle01/account.json` | `c221faacb57f4f1c88ac448cc45fde364e552b6cf93cc5e6e8e7f7c85117945c` |
| `attempts/daily/mini_fcl/cycle01/carry.json` | `3a6545823efc68473e47f8ff465684fe580575a77fc3c5b8cb9ad6bc7bdb8c99` |
| `attempts/daily/mini_fcl/cycle01/objection.json` | `e37a821a3164a468bd85d780e94e4aacc4ef28b79a840494ebcf9f883782e386` |
| `attempts/daily/mini_fcl/cycle01/response.json` | `4be592d6fd1e685d96966a3c3d30c28707df066aebbfb8a179da47995fdcb7d1` |
| `attempts/daily/mini_fcl/cycle01/rival.json` | `32d4672da14968edb2073e165e22deb64bbcd49972c97c8fe65054d5abcb96cf` |
| `attempts/daily/mini_prose/cycle01/account.json` | `0d0b5c15b4595dfd13680bded0ee46ef566f0a20330a17c6514b8978c94a5edb` |
| `attempts/daily/mini_prose/cycle01/carry.json` | `dc75ccc33fd7df978562758bc1d42f13d50fb123d1f57356d9ec3bc21f0d8108` |
| `attempts/daily/mini_prose/cycle01/objection.json` | `17778742f207de5fc3c865a53bb8cb1eaca5a3815c017289e8a82d9638b172b4` |
| `attempts/daily/mini_prose/cycle01/response.json` | `76d9fa49a0348ba4cf10d5fa1ad1e1b0ddf3fbe5dc3cda86a9e7cae1fde265fa` |
| `attempts/daily/mini_prose/cycle01/rival.json` | `f05860c676eed5210440ffd1ea75b4ab38f578e24e82ed22f415788281506b20` |
| `manifests/fork5.json` | `f7e727daea6d3ba4353b1b2f93ae7e461a648c99877cf2ee97ca7653e30e1ee8` |
| `manifests/return6.json` | `f3ece835e680452807d9e0dd69232c34a452b67062cba75c4ba46bf87bb93951` |
| `manifests/weave7.json` | `ea8174af734dabde382a36cd85323a064ef9a8302490b9f85e1f9f360e7686df` |
| `material.json` | `8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff` |
| `plan.json` | `6609038beaa616d7c27467470dde0cb842071c9ec7006530c3f49ffab13ee58e` |
| `provider/daily/bare/cycle01/answer/call-0001.request.json` | `0bb891e109ce6fb99a38ff50b5b44b27978961c25fafc4ff755be470ddc998c9` |
| `provider/daily/bare/cycle01/answer/call-0001.response.json` | `7a692cb8887bb2811fd0706778a52c59f35f3d6d1de331aacdd59b59ca57ac92` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | `146120fb9348bdfa1153e4069a0cc611baa37c7ebda1f11a2f2a267ee698b737` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | `527b2d1163adc6b0b4221d9bb7f9fb00b596920747303307cbaa03ec5937e9cc` |
| `provider/daily/mini_fcl/cycle01/carry/call-0001.request.json` | `312633518f980074f00be3c5ef1ac78831ae196de406b88366d3f02f4bdc823d` |
| `provider/daily/mini_fcl/cycle01/carry/call-0001.response.json` | `80de0f94a709a92301efdbd99186e241120fea77e2158ff862b1158a5921912c` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.request.json` | `fa7157e88ceb2f514f3a9ca8b0aebdb59b464d27ea65dcf2e1a2745b7684333f` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.response.json` | `1742b65d5e414573bf94d8c71da26e4177edc4543ebf7ce9918e26be5fad64c2` |
| `provider/daily/mini_fcl/cycle01/response/call-0001.request.json` | `7dc134607ed8fa11fae0fa4a04bb7dc462d56783484bca8a1a86c11fcb5d9c5f` |
| `provider/daily/mini_fcl/cycle01/response/call-0001.response.json` | `5e92aefa33bf3f6329733fdc7b11893890cfa03eb27d5250183d14abb4df39a1` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | `2b95edad937cd3d498578327cdc840bb44065cc0981b0850b0498d7a18c2f09a` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | `5cf39468942dc3a93359b07801cb323631eac815283c0c6524ff0f5aeb663f0c` |
| `provider/daily/mini_prose/cycle01/account/call-0001.request.json` | `82499ab89f8003af48fb1b66f84e5ddda513b9b0b41cbae60d1d1ef6bd4cc153` |
| `provider/daily/mini_prose/cycle01/account/call-0001.response.json` | `ce2374165ae315d2c3e61d952628e6545c98ef15ba53a3999cc64a2770bd09ee` |
| `provider/daily/mini_prose/cycle01/carry/call-0001.request.json` | `7984bdddefaf16c5e2bacfd7de37e365c841cc80fb0869870f589f38e62e3e6c` |
| `provider/daily/mini_prose/cycle01/carry/call-0001.response.json` | `5fa42e89ed6ce2c3cf74d6364ad94f3f7a3798fc6daa7c137c82c24130b855ab` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.request.json` | `34a5a141fdc71bfc7a3c9d9e51004148e627d7ffc523107c3117a51b8642bdee` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.response.json` | `abd94abdb02353c404f673a5672269d4b9f0cf06f65ea4f499781feb3a7bf5dd` |
| `provider/daily/mini_prose/cycle01/response/call-0001.request.json` | `12406dc04c2acf260bf7705512dca8950024c08b47b3f1062f4b7edcd9500e90` |
| `provider/daily/mini_prose/cycle01/response/call-0001.response.json` | `fb1a8f27e1eca5f75c24b1be3456a09aeed273648e6d9f1ca26e3bc8043b7d5e` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.request.json` | `0e4f1eff5f5437feb944f93ab4a73c70de7d37d58e3be7cf5c5d931ed968010a` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.response.json` | `6d34e9be4de4043cab39c565f15dfbeebe7c574a5e4d370f28fdd873c98f6e5f` |
| `requests/daily/bare/cycle01/answer.json` | `e56a4718c33796f7de5718492d7c7cdd3bddefa84ab1cd37b85f7fa5813ff604` |
| `requests/daily/mini_fcl/cycle01/account.json` | `8fbb7de9c878c51a82b915e8875371759ef3d0c62e9fba4d8252d41a38603a54` |
| `requests/daily/mini_fcl/cycle01/carry.json` | `c2195bb0ce649eaddcf16256f1e212967d6c7dec22f33681c59c5eddda61d30a` |
| `requests/daily/mini_fcl/cycle01/objection.json` | `cbfec6a3701b146647c3bf9ec65c07cbe0357311f1d571d08cea6546f13ea75d` |
| `requests/daily/mini_fcl/cycle01/response.json` | `9083ce00ec5b9a1a99bdf110b79f67732d843c9934d9fd9b047ea1d5f398dee6` |
| `requests/daily/mini_fcl/cycle01/rival.json` | `de1fb208d4db0b70b3b545cb8d612536f1210373e853d66d9197aaf66db77aaf` |
| `requests/daily/mini_prose/cycle01/account.json` | `ad0e60b8dc7bf07b68bd06a7267a3c75b27d3b65d4e07ea3675c016e68ace649` |
| `requests/daily/mini_prose/cycle01/carry.json` | `062521fc5305b6153bd0674eb06ad8a99c715ef4ae93aa1348a3c9f2280f797a` |
| `requests/daily/mini_prose/cycle01/objection.json` | `e0b32295f9723ad04b98e032d8284f7289e597de681b1a7b61704b6359694566` |
| `requests/daily/mini_prose/cycle01/response.json` | `23ec74dc940d968c9d53d854cddbf82c0da865a44cd2dd1a8faf381d8249a755` |
| `requests/daily/mini_prose/cycle01/rival.json` | `519a68192ce95f4a4d6367fd9319b1e5493ac40c00c8048b601c4986ab284022` |
| `responses/daily/bare/cycle01/answer.json` | `61e8a1fac56d64ee2770f762bac99dfce77b7eeea60836b9ee1bdfeb3b904f48` |
| `responses/daily/bare/cycle01/answer.txt` | `08518a860455178b01889f99b0a751cf846f67ce3b4b0f4be9d15026cdc4f0ce` |
| `responses/daily/mini_fcl/cycle01/account.json` | `a8928afc409133dff82ff09f900ccb035d0fac2a5350fd6c9ad25ecb09c6593b` |
| `responses/daily/mini_fcl/cycle01/account.txt` | `1837333a321e7a428651b4d9a998b4ff31bda53194d17b36de223878beeaad07` |
| `responses/daily/mini_fcl/cycle01/carry.json` | `143ce05027fd467c4b5e7ef8b1214aae1bc8b1fa9bc92bb8cd1a3c25e8bdb167` |
| `responses/daily/mini_fcl/cycle01/carry.txt` | `39430f227f9356ead8a90cdae49d298b0465077487156e21f29e3a3d7cca8e95` |
| `responses/daily/mini_fcl/cycle01/objection.json` | `c3023a66d20e018ffd9f92ee5a333ca2b26c4971d3c00246b93173eddff36e51` |
| `responses/daily/mini_fcl/cycle01/objection.txt` | `72920999de94c685d3af8ee10282dd51c79947fbba9c7b00a9d4ce3190a206cc` |
| `responses/daily/mini_fcl/cycle01/response.json` | `a3372c91e28e5b292fd905ed9ce177439087df3146dc297b9c49e43f49393396` |
| `responses/daily/mini_fcl/cycle01/response.txt` | `55b30127711a475d129fb88c2b2b5f2b10b5a513445bf173875946ebf8e02963` |
| `responses/daily/mini_fcl/cycle01/rival.json` | `7a32cfa1a606fd1756e2af013e7fe1d109fbbcc542f4097dee010ac3cf44a0cb` |
| `responses/daily/mini_fcl/cycle01/rival.txt` | `68b50ead0793040130982191c9f31ce36a513a35378c26c2dfdfcf1726dba749` |
| `responses/daily/mini_prose/cycle01/account.json` | `5b295a04bc042f48f182dbdbbfd873377796b21c76b3bb6d5bc9f23239432ff6` |
| `responses/daily/mini_prose/cycle01/account.txt` | `66a444cb4dbeb6531ca9487a3f50cbd843447921b6f2471a2eb9e52297d07167` |
| `responses/daily/mini_prose/cycle01/carry.json` | `55f1c587c62feee9fb2862831916f7a06460240e610c58472eb7c1e03a0a8dd6` |
| `responses/daily/mini_prose/cycle01/carry.txt` | `873c76fce4267cc7cdc0a8084644114c0b64e6327d9e93bf0e08f625c7f730e4` |
| `responses/daily/mini_prose/cycle01/objection.json` | `a1843425e5ae4107d932b9b488bbc8889c59e604183cf1b796671667cfe7808e` |
| `responses/daily/mini_prose/cycle01/objection.txt` | `194ca476fb327b0f8fa2641b35852809642bff9fa29de8aa78e239012d8dd132` |
| `responses/daily/mini_prose/cycle01/response.json` | `6656d954d6053259707ae175efaa4178d931bf692fc341d6f8452c44b617f0fa` |
| `responses/daily/mini_prose/cycle01/response.txt` | `9b41e50e99bbdaea1c2face7afa2a047a65b75a11c7e65582f08d26849f3e449` |
| `responses/daily/mini_prose/cycle01/rival.json` | `fd1a2486cd2ffa64bb848937fa05a189c5df7c53ab612e4ace157cb2a47886bf` |
| `responses/daily/mini_prose/cycle01/rival.txt` | `2b2e62acc1304406d852e592d54cc343d7d414e31b26329a9eef687a0515c1fe` |
| `traces/daily/bare/cycle01/answer.json` | `4ff68da01ac0c9cfd4c060d4a822f7ced327003f53e9e96f1e3fb08916a7fbab` |
| `traces/daily/mini_fcl/cycle01/account.json` | `f4790106152ef33f8f02cc8f182089bd4e99beb4f553144a79e51e2ec4f92f53` |
| `traces/daily/mini_fcl/cycle01/carry.json` | `b14fa40295ee5c7bec9c30212ce3f49636c0b4bce0c24db25e49e56985eddf7e` |
| `traces/daily/mini_fcl/cycle01/objection.json` | `cd5dee741c8df663a6459f32b25eb1f6967ba779d5b96a3cc106351c2004f253` |
| `traces/daily/mini_fcl/cycle01/response.json` | `218c3677f2103196a82ef35e1b8131d5b6addc25cab181b646c72441613c7a29` |
| `traces/daily/mini_fcl/cycle01/rival.json` | `4b5461756a4c4c0ae05e956ef591c1260ac40cf81bc3df6afb29bc15676c4a68` |
| `traces/daily/mini_prose/cycle01/account.json` | `5725e108b01c89983c73bc7e84268aa9bbf8b77d8b6fe57c79df1137bd5db455` |
| `traces/daily/mini_prose/cycle01/carry.json` | `cc02d278e3c8bf130ccf6e99fb5b30cd69137b716d4400060e3b6b0fc1a124e0` |
| `traces/daily/mini_prose/cycle01/objection.json` | `c87fec2445182313b042c2e70640af076cf643130b3d61ba1b686cbc4acc4d4e` |
| `traces/daily/mini_prose/cycle01/response.json` | `80604ff32bf82a36dc98d4dcd70fec9c8e102f09b65016d5f4ecf82d45f7d3b4` |
| `traces/daily/mini_prose/cycle01/rival.json` | `7c021587cea826026d78716ed0adc17004650aa1bfbc7be6093ef164ebf57996` |
| `waves/wave0001.json` | `796c4e0e3a8ca0e86782f2bc760307b77963cae603c05199709273f5257c0235` |
| `waves/wave0002.json` | `02e8219cbeda89e442d3542451eddb6ddc92cccd575339cb66b3c6b9e577605b` |
| `waves/wave0003.json` | `30b85c6a8e0fc5a7c6adca2e16f3f436069da70393fa3d12c3f24948aa3ab2b9` |
| `waves/wave0004.json` | `523cf0f373bd1cf3cca512e8ac2c1faf9695347084cb2cb16643d2ff9942b499` |

