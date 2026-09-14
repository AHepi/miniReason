# Use-relation table - H005 occurrence-06

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

- `plan_id`: `84a5fea6e8ad6f3184874cfad980df348e5b65265818f132f52b9669a5634264`
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
| refs walked | 4 |
| cross document rows | 0 |
| intra document | 4 |
| refs to exposed task artifact | 0 |
| unresolved | 0 |
| importer resolved counter | 4 |
| importer extension counter | 0 |
| importer dangling counter | 0 |

These are counts of authored refs, reported as information. No count here warrants anything (FW5:851: counts "are not outlawed as information"; what is forbidden is a count entering as an *automatic* warrant).

## Rows

*No cross-document reference in scope.*

## Declared uptake versus records present

### `daily/mini_fcl/cycle01/account`

- commitment surface: `read_fcl1`
- records present (5): `rec1`, `rec2`, `rec3`, `rec4`, `rec5`
- declared `uptake` (2): `rec4`, `rec5`
- records in uptake (2): `rec4`, `rec5`
- records omitted from uptake (3): `rec1`, `rec2`, `rec3`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/rival`

- commitment surface: `read_fcl1`
- records present (4): `rec1`, `rec2`, `rec3`, `rec4`
- declared `uptake` (2): `rec2`, `rec4`
- records in uptake (2): `rec2`, `rec4`
- records omitted from uptake (2): `rec1`, `rec3`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

## Nodes whose commitment surface was not read

- `daily/bare/cycle01/answer` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_prose/cycle01/account` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_fcl/cycle01/objection` - commitment surface: schema_failure; references not extractable by this instrument
- `daily/mini_prose/cycle01/objection` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_prose/cycle01/rival` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_fcl/cycle01/response` - commitment surface: schema_failure; references not extractable by this instrument
- `daily/mini_prose/cycle01/response` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_fcl/cycle01/carry` - commitment surface: schema_failure; references not extractable by this instrument
- `daily/mini_prose/cycle01/carry` - commitment surface: prose (not parsed); references not extractable by this instrument

## Residue: refs that resolve to nothing

*No unresolved ref in this scope.*

## Files read

Every byte this instrument read, with its sha256. Nothing under the occurrence was written.

| path | sha256 |
|---|---|
| `artifacts/daily/bare/cycle01/answer.json` | `705882f310a357815e8aa76b776b8bd0049cc5776a133f81451189d58b1119c3` |
| `artifacts/daily/mini_fcl/cycle01/account.json` | `a4d341fde4cc7ba67574b09e0720ba91aea9ec131f1189ae7a9f792651be9067` |
| `artifacts/daily/mini_fcl/cycle01/carry.json` | `fbb91d32d6173ccacdfc1f6bcb46cfde3e4eacfa895e4be54a4ebb3302015c7d` |
| `artifacts/daily/mini_fcl/cycle01/objection.json` | `1be20731a470709231d4fdff9cf062c3a1130c6fb0c2bea350346fc541e2753f` |
| `artifacts/daily/mini_fcl/cycle01/response.json` | `25f2997e8bd6433a485fffa01f76e8dcda794c29959e4f802429cf991b158e58` |
| `artifacts/daily/mini_fcl/cycle01/rival.json` | `043882fc7b920ac73f460f4309c7e19dcc8083551d961521c7955a7f1174062f` |
| `artifacts/daily/mini_prose/cycle01/account.json` | `3d7fc6ef6c8d4700a3ddb544651591f9b3624e33ddd405377c9a77d269fa97cd` |
| `artifacts/daily/mini_prose/cycle01/carry.json` | `e38ff0b8ca674e274e84b1df7e3117192777abeb815fadb840b71f88a102a586` |
| `artifacts/daily/mini_prose/cycle01/objection.json` | `314e3fb2551beb9682d90a2f9da1aee903613b8d6de18c91f1e994e912c7d23e` |
| `artifacts/daily/mini_prose/cycle01/response.json` | `c3e46a926e4a1f7e32ad4cd8b904b7278c5e5c42dfb44c9e97eb9692c00064f4` |
| `artifacts/daily/mini_prose/cycle01/rival.json` | `8ce7b1c63f0c77c9a5283a1c219610fdcd1ef487fcdec81b793269b01406a4ea` |
| `attempts/daily/bare/cycle01/answer.json` | `fec9790307ff9f3e09d6a30dd35438d0f12769f8b7e4bd00a2f31223bbeb6760` |
| `attempts/daily/mini_fcl/cycle01/account.json` | `66c897d83c6429b7b2860eb43bef6cd20ad80f1a289a076e49c5e4e9b39fc471` |
| `attempts/daily/mini_fcl/cycle01/carry.json` | `25c38e23eb1606859aa8ea2373e5147cd3829c798ab1ff360c9f0041c98fd089` |
| `attempts/daily/mini_fcl/cycle01/objection.json` | `d4281f250061897e18eafe62a15a14515308481e6daf6782b22726703e26fba4` |
| `attempts/daily/mini_fcl/cycle01/response.json` | `c0ae1b40751991eef1c00cb734c816e3c74a07af05ff512c469ec0952d25ad08` |
| `attempts/daily/mini_fcl/cycle01/rival.json` | `a4cafe5f974865b229a9331f86341f77892f00349c735392054799244ea0a6b5` |
| `attempts/daily/mini_prose/cycle01/account.json` | `8d3d7a0541122a2b0c69d2237e233b2ea8aed99b0c5e6d933c738dd78e2d7eb4` |
| `attempts/daily/mini_prose/cycle01/carry.json` | `951ab0e35c06353477ea06a8812da1c673ce9aa4bce8fd689560006bc732856f` |
| `attempts/daily/mini_prose/cycle01/objection.json` | `e3bcd881aa069092e16551303d096eefce7143661a5b1f8bd9e9cf46fd25fb6c` |
| `attempts/daily/mini_prose/cycle01/response.json` | `d145d23027e8bafe30e9f5cbdfa3685142444194e3fcb799a037c927281ff68e` |
| `attempts/daily/mini_prose/cycle01/rival.json` | `9670021214dcceb4481e323c5a850598d99b100e36e87495e98202b86cdb2518` |
| `manifests/fork5.json` | `f7e727daea6d3ba4353b1b2f93ae7e461a648c99877cf2ee97ca7653e30e1ee8` |
| `manifests/return6.json` | `f3ece835e680452807d9e0dd69232c34a452b67062cba75c4ba46bf87bb93951` |
| `manifests/weave7.json` | `ea8174af734dabde382a36cd85323a064ef9a8302490b9f85e1f9f360e7686df` |
| `material.json` | `8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff` |
| `plan.json` | `ee565d3fb40bf4c96c555dbb7994c09ce6e1899011d9b53c8b7bd8632f11e8ad` |
| `provider/daily/bare/cycle01/answer/call-0001.request.json` | `04d971f0317c42a1973d9cd13fb77f811f77a2df28d759be62d7dab743f16aca` |
| `provider/daily/bare/cycle01/answer/call-0001.response.json` | `ee0ed26d4c50798c5fd56d6cb372d4dfe841e3ffa901b6e99e7c2e74a44d4a2f` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | `a9905680f0a37c7e8ae20b49458ab93bc54163f54c7402f3272bf05037a54c78` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | `fc3349c581a7722ad1a308a66c9b86780da87a6a21b2190dc9b312e6ee2624b4` |
| `provider/daily/mini_fcl/cycle01/carry/call-0001.request.json` | `d565dec324a62d5beefd48dd226f4d3fd09cdd599b089a6fef2d016ae3793225` |
| `provider/daily/mini_fcl/cycle01/carry/call-0001.response.json` | `5da10ef4a08efbabfacfe5319125f971e422b8402d37d425cf2fe8240655107b` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.request.json` | `595179bcb1107fd11fe0a1bcbf7c1b4049106d1ae4cc8b39dd62c0b901f82bf6` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.response.json` | `7e58ab0e669d046b71112397d4305cacc42e5fa953d02c84a275fc356ef66bc5` |
| `provider/daily/mini_fcl/cycle01/response/call-0001.request.json` | `d955fa00f8e84b5830f387d374bc9beb5d3ded3d369e4a59e4d94603be54fd5c` |
| `provider/daily/mini_fcl/cycle01/response/call-0001.response.json` | `94555f1ebfdef7d0b2323feac97bf67fc7cbb267b874ab843e21c01cf043614c` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | `825fee46fe27854729d55e229dcb60e1ee187113eaf5a0ebac0d1185150d2077` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | `8863b3675b56dcc643bc4a0997100d56d07a97753d57509b3e21e844e7187d60` |
| `provider/daily/mini_prose/cycle01/account/call-0001.request.json` | `0790ec9a895f0ff56ceb4faa277ff9d6ee6bd1f92e9d9c08e3ca9844ab0d7942` |
| `provider/daily/mini_prose/cycle01/account/call-0001.response.json` | `344253eca1144addc497cb60332a027be9278da499c489b61b7fc9ed03baa2ba` |
| `provider/daily/mini_prose/cycle01/carry/call-0001.request.json` | `e04d99a7d36f88a42da388ee07bcec6dc1f86071ce31fecd5471c0ced3201bd1` |
| `provider/daily/mini_prose/cycle01/carry/call-0001.response.json` | `f59517f0356296cf29a1695eb0862c9dd0cd1c4bb1f9d720fea2acbbe1c62322` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.request.json` | `aa8948c5c9e978bb9e1ef9e969a0c27b2993204fc986120623fb484359451ee0` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.response.json` | `c246f091dead9c4df32068017849ca97fe5545d9e6d7cff2a6f80369c455cdd6` |
| `provider/daily/mini_prose/cycle01/response/call-0001.request.json` | `3dc3ddb148b6de88ea3cef1d5793f29e82629aa79e6e15d231c67a56a9291984` |
| `provider/daily/mini_prose/cycle01/response/call-0001.response.json` | `d7b72b07ed47647ebebdfe35dbfe75ad542d322cb304fc71a558c3863ff4a2ef` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.request.json` | `f777864b3e637d73280241facdb897de50aab7631a9600ea15aa0fbbe0e86a0a` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.response.json` | `17f0caffd4ec1a82c597273bb1e2c0b3de9838bb402d022122422fa547356c85` |
| `requests/daily/bare/cycle01/answer.json` | `d28dad56eba63168518e1e906c3ed968b248f6ffba38b66c220d1f9f0503d442` |
| `requests/daily/mini_fcl/cycle01/account.json` | `ebf95574730da158ee0f422b1bef2e293954423dea66405fcb45ec8ae4a7e400` |
| `requests/daily/mini_fcl/cycle01/carry.json` | `d3b4cd4d26f5507332496112ef459f65a2fbb7fcc08c95d9ffc195012b2cc17e` |
| `requests/daily/mini_fcl/cycle01/objection.json` | `d7bb7530bd6e7b43e88fb06c6074cba6c0780cb20bcce49854be8c4f3395b370` |
| `requests/daily/mini_fcl/cycle01/response.json` | `d077be9f964c6ddbfc9c447dbb13cad36856e463266f35b9a933494fd45c2ae2` |
| `requests/daily/mini_fcl/cycle01/rival.json` | `8e2547fd42f0314dd015eea8bc6e2f12650737a0ebe6ae84098e68a957469bf0` |
| `requests/daily/mini_prose/cycle01/account.json` | `ae05f4119ba31053fe1319dbab934d7ebb823afc97d31fa2e5d5cd82b53879a0` |
| `requests/daily/mini_prose/cycle01/carry.json` | `52a9e805b4c078a3f562a5108b122ac774e04f876bf95680805ad2a131fb9563` |
| `requests/daily/mini_prose/cycle01/objection.json` | `b969fe4607b15f15d9cc3c27d983701e3d995f01b4603d312272e8e0f1774311` |
| `requests/daily/mini_prose/cycle01/response.json` | `74dd03fadde0a2274b44905c6359bf03a1d1ed275a4033c125a90f3f2be7beee` |
| `requests/daily/mini_prose/cycle01/rival.json` | `86e67db296b2be011c09ff5dc33e943b32c6180d2a900330aed0773951170794` |
| `responses/daily/bare/cycle01/answer.json` | `b6b66213c85de525208b873ee7150a3373645d6653fd14704097dfac6575cae0` |
| `responses/daily/bare/cycle01/answer.txt` | `269fb1af17561478104c40a2d7168e76a54c4cc94d0d48e9c058af2c6d24df5e` |
| `responses/daily/mini_fcl/cycle01/account.json` | `a225e58a7c0c2041ebffc3a68fbcaa2c486cc44408c1699127c2d1d7bc42b3b4` |
| `responses/daily/mini_fcl/cycle01/account.txt` | `1b81871fdf2c2a70413b0105d96aa684e93efdc4c57c406d6ae8a00d3587220f` |
| `responses/daily/mini_fcl/cycle01/carry.json` | `8c066089fdeee724458a4ac68cbff2f438d3df3dffd4ba6fe46f5c8f9d6cfdef` |
| `responses/daily/mini_fcl/cycle01/carry.txt` | `e57b622511fbdb362ef5dfb9691cd1f41362d8cfe36b587a1bd8f502d438dc2d` |
| `responses/daily/mini_fcl/cycle01/objection.json` | `7bd2cc4e42468760ca3fe501825adf25433e99569102b11b3d7ef57ea8fa6ff6` |
| `responses/daily/mini_fcl/cycle01/objection.txt` | `a025f74c01019a48edfa76f06c970fefd39df2ccdf92334b1fd0d50c5c44d702` |
| `responses/daily/mini_fcl/cycle01/response.json` | `0d90969a34f8e5aede79b5e639b697bd4e127e2cdcc931f03a97f671d9466943` |
| `responses/daily/mini_fcl/cycle01/response.txt` | `b548f183c32c15285d29c65b984974bd5935f4193d559dbc35ea2abdb3224a85` |
| `responses/daily/mini_fcl/cycle01/rival.json` | `b94489d58ef5846ca3a8dd969c8afa2ee5cbb229018eada44b4d9805ac1b713e` |
| `responses/daily/mini_fcl/cycle01/rival.txt` | `8111ec5aa3667159c27dce704a6338718235595517590fb43274ed8f1a871bdf` |
| `responses/daily/mini_prose/cycle01/account.json` | `b840fe1a6ab3297a3d7c51aea4769769668aa42b988230053e0b15d30ae877bb` |
| `responses/daily/mini_prose/cycle01/account.txt` | `bac10e98745056ef58045efc1c9adce423268e523d6b1381771138669b17629b` |
| `responses/daily/mini_prose/cycle01/carry.json` | `fa185edd98a55870101c7dd318566ea3f3babe7aed29acf1da25241750b2bc6e` |
| `responses/daily/mini_prose/cycle01/carry.txt` | `173302f8b9824e8fc1ac8206be2ca23e12aec4674da12ca8b7140769e126e397` |
| `responses/daily/mini_prose/cycle01/objection.json` | `fd75e8da28dfe676ccc17092bff471064835f92a8291a10e3c5867dccf4f8c67` |
| `responses/daily/mini_prose/cycle01/objection.txt` | `b39add588ac9314729f7a2a566b1bb3c83ffd9bf1d6aed71abdf9b96bc1de6d9` |
| `responses/daily/mini_prose/cycle01/response.json` | `c53b593a0581ae1eb1d938b0b6398702ec20f7103adff0443add362eb81d13ad` |
| `responses/daily/mini_prose/cycle01/response.txt` | `0a9304aea1e2b3ecb1bf09e1ca071731463c3e5f5b53aea4a457bae1ef29df67` |
| `responses/daily/mini_prose/cycle01/rival.json` | `b9b7309c38e6a76f1af90fd59a70e1d9721c10f35cf162e79f6f24016e18536d` |
| `responses/daily/mini_prose/cycle01/rival.txt` | `e30bd7ad1644bc0b08e2cdbf5cefc22855581587531b2a6a0ffc56b080dc2218` |
| `traces/daily/bare/cycle01/answer.json` | `4ff68da01ac0c9cfd4c060d4a822f7ced327003f53e9e96f1e3fb08916a7fbab` |
| `traces/daily/mini_fcl/cycle01/account.json` | `f4790106152ef33f8f02cc8f182089bd4e99beb4f553144a79e51e2ec4f92f53` |
| `traces/daily/mini_fcl/cycle01/carry.json` | `8cb528dd8a04d015d9ef3fc0a996de7fedc7aacb6e98fa4cadb499e3c3a5c4c5` |
| `traces/daily/mini_fcl/cycle01/objection.json` | `ce5100891ed06e499d155c05c022d5558402c9f4e3f50c13bc4af6bea96345f9` |
| `traces/daily/mini_fcl/cycle01/response.json` | `c5c24e59c355ed7f81ebe0f2a36f9558619180be40e1ea8188bef4aaf2fbbb7f` |
| `traces/daily/mini_fcl/cycle01/rival.json` | `9e21bbe36e249ad52f9cef76623de7df6c6decfb90c91815b906ce5589ed4686` |
| `traces/daily/mini_prose/cycle01/account.json` | `5725e108b01c89983c73bc7e84268aa9bbf8b77d8b6fe57c79df1137bd5db455` |
| `traces/daily/mini_prose/cycle01/carry.json` | `a41493f9f66657b518c00b2e1709b80ed963b6d6fb475b9c753aeb01089fff6f` |
| `traces/daily/mini_prose/cycle01/objection.json` | `08caf59b316d05c2b2e081919ed5b8907f2c11f30f571e54ab11520966f31c17` |
| `traces/daily/mini_prose/cycle01/response.json` | `7eb1375612d821b90ccda7fe292e86704cd7c6e8464a3b66c6709cadfb9891d4` |
| `traces/daily/mini_prose/cycle01/rival.json` | `392c26ca520812bee00eeb5e920b407b31a58fb0f0372c72cc652dc8ca8a4e24` |
| `waves/wave0001.json` | `6a042f77b6665f012dafd35288460b75ec0b6e68df1cb3ab608cfc848b4d51cf` |
| `waves/wave0002.json` | `4ad9604b6a853bac17eb8afa717e7b2adf3c423550772de90b47f0aa18e5b161` |
| `waves/wave0003.json` | `f61e75299185b7896fe3697edcd16cc8eb9e453d19e99d406a3cdcbc865a0ecc` |
| `waves/wave0004.json` | `536e80f7c80857cc21a0782d0ed7beb9a48684c2811a609584ddf04c167bacd3` |

