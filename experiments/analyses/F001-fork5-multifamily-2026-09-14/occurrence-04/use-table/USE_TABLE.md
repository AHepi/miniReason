# Use-relation table - H005 occurrence-04

**The tool records juxtapositions; the reading is root's.** This table places each authored cross-document reference beside passages a root reader may find worth starting from - a finding aid, never a closed search space - and stops there. It scores nothing, ranks nothing, classifies nothing and mints no relation of its own; it has no `att`, no `dep`, no status and no label. **A lexical overlap is not evidence of use.** FCL-1's own rule is that `depends` and `mentions` are "not automatically inferred from citation or lexical overlap"; a witness of reason use "must preserve internal role bindings, not merely the endpoint string" (FW5:628); actual use is "not automatically machine-maintainable" while prompt appearance is only a delivery fact (FW5:640); and no function of an input-output projection agrees with the accounting predicate across models differing in active route (FW5:1218), "semantic use inferred from delivery logs" included (FW5:1222) - all as summarised in the FW5-versus-harness-spec review, `fw5-vs-harness-spec-review.md` §1 R2-R4, §3.1 and §5 P1/P6. Root fills the four empty cells by reading; `unresolved` is a legal value and stays unresolved (FW5:634). An empty cell is an **unread row**, not a reading of `unresolved`.

Instrument: `use_relation_h005/1`. Schema: `h005-use-relation.use-table.v1`.

## Scope

- `daily/bare/cycle01/answer`
- `daily/mini_fcl/cycle01/account`
- `daily/mini_prose/cycle01/account`
- `daily/mini_prose/cycle01/objection`
- `daily/mini_prose/cycle01/rival`

## Custody

- `plan_id`: `e2e3357ef2d67dda270a53f65151c6b1e94265000d487876e0cad735a9cc83c1`
- `material_sha256`: `8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff`

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
| `projection_source` | cross_file | verified (2/4 projections; 2 projection(s) had no exposed source (the slot is absent): `daily/mini_fcl/cycle01/account#p.account.0`, `daily/mini_prose/cycle01/account#p.account.0`) |
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

**Distinctive token.** A token `t` of the target record's text is *distinctive* when all three hold: (1) `len(t) >= 5` characters after lowercasing; (2) `t` is not in the closed stopword list below; (3) `document_frequency(t) <= 2`, where `document_frequency(t)` is the number of in-scope FCL-1 documents whose record prose contains `t`, and the threshold is `max(2, number_of_in_scope_FCL-1_documents // 2)` - here `max(2, 0 // 2)`. Clause (3) makes the criterion **scope-dependent**: it is computed over the documents listed under `corpus_documents`, and re-running over a different scope can change which tokens count. That is stated rather than hidden, because a partition-invariance question about this instrument (review §5 P5) has to be answerable from its own output.

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
| refs walked | 0 |
| cross document rows | 0 |
| intra document | 0 |
| refs to exposed task artifact | 0 |
| unresolved | 0 |
| importer resolved counter | 0 |
| importer extension counter | 0 |
| importer dangling counter | 0 |

These are counts of authored refs, reported as information. No count here warrants anything (FW5:851: counts "are not outlawed as information"; what is forbidden is a count entering as an *automatic* warrant).

## Rows

*No cross-document reference in scope.*

## Declared uptake versus records present

## Nodes whose commitment surface was not read

- `daily/bare/cycle01/answer` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_fcl/cycle01/account` - commitment surface: schema_failure; references not extractable by this instrument
- `daily/mini_prose/cycle01/account` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_prose/cycle01/objection` - commitment surface: unavailable_decode_failure; references not extractable by this instrument
- `daily/mini_prose/cycle01/rival` - commitment surface: prose (not parsed); references not extractable by this instrument

## Residue: refs that resolve to nothing

*No unresolved ref in this scope.*

## Files read

Every byte this instrument read, with its sha256. Nothing under the occurrence was written.

| path | sha256 |
|---|---|
| `artifacts/daily/bare/cycle01/answer.json` | `caf27324cf87d3e3f7a5999d35c6035545c5cb0c88297c062dbb474fd9ebb242` |
| `artifacts/daily/mini_fcl/cycle01/account.json` | `f34da0cb4b9a31c5b4072596258b04eb94849fd08380b1899a5cad1e14bc09a6` |
| `artifacts/daily/mini_prose/cycle01/account.json` | `561294d73c77e7778ab70f3fe86033bbda54b3c34b58d31eb401f1928031725a` |
| `artifacts/daily/mini_prose/cycle01/objection.json` | `2896cf1b3bda4e1423c637c05c4197003982e162c63ca06d005cbd81f3675354` |
| `artifacts/daily/mini_prose/cycle01/rival.json` | `09e9828de01550b78b05073041beb53ba1088c6f9708848882740576a60002f5` |
| `attempts/daily/bare/cycle01/answer.json` | `2049bee56a72dc767c38c3bf08fbaaea1cd0121c2d31bea0e7f979c7da513604` |
| `attempts/daily/mini_fcl/cycle01/account.json` | `a0ec87d46cca9519d52c2b957974dea803a21636ab18aa3bf3e45495f47f6980` |
| `attempts/daily/mini_prose/cycle01/account.json` | `f46dc2a428984415340448844424df26d8f1ac1a73d6e6f6b83150d2222fc023` |
| `attempts/daily/mini_prose/cycle01/objection.json` | `f9a2ad95441f8ff39b5b76049ea6008a2e226d838e1cfdfbe893c7a0a95d8c8d` |
| `attempts/daily/mini_prose/cycle01/rival.json` | `9b70bffabe83f3bb26d909d45ac21a6f2be4884ccf46869858669b2aebeff605` |
| `manifests/fork5.json` | `f7e727daea6d3ba4353b1b2f93ae7e461a648c99877cf2ee97ca7653e30e1ee8` |
| `manifests/return6.json` | `f3ece835e680452807d9e0dd69232c34a452b67062cba75c4ba46bf87bb93951` |
| `manifests/weave7.json` | `ea8174af734dabde382a36cd85323a064ef9a8302490b9f85e1f9f360e7686df` |
| `material.json` | `8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff` |
| `plan.json` | `7d06bdaae719af403cf1df715cee213e87ca310ebaf71a85a92ab5f9ba9ffc1f` |
| `provider/daily/bare/cycle01/answer/call-0001.request.json` | `34f7863f8de4df6beec51d8cc377ca097dc177040fe6886baf76aa0926d13f03` |
| `provider/daily/bare/cycle01/answer/call-0001.response.json` | `c7362cbfea1092abbb8903e2f217320736ed4dea29bb62efb29d1a40853d8155` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | `9542a2ee60a9755658234457073f0850f1878f966f779f9f9aed8647caea1fb2` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | `51aa4b7d7a71aa4d91ca4afc3e7516a189f78f4bb7ddac4e6d6a790f91860ff1` |
| `provider/daily/mini_prose/cycle01/account/call-0001.request.json` | `70e863c8fc8b24358051b50416a77734594766fe825460c3c28cbccc82ee9f00` |
| `provider/daily/mini_prose/cycle01/account/call-0001.response.json` | `373f5bcbdd4a3eb6be4f881719cfe91f8182ad21194881a022862c6439dc658e` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.request.json` | `9ffc3d2d09a5e7578232ab36ba2540cd5de3895b6d6df245908488f18669a205` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.response.json` | `ee1df90b05361f0537213e80f05e433d2f60afd1b0bef355c5a4b8550f3df502` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.request.json` | `de4eb440ccc239a9faf6f215ed18f5d53287cb3004c8e56ae094fc92f0d6bdc6` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.response.json` | `1c32e613312b6439c83ba991438a0853a694a85292f824485b110f15a0010e02` |
| `requests/daily/bare/cycle01/answer.json` | `a97b3c0fe6ca5fed4d530fda2866011f5cc81e727c438f30522b1d3cd38f246f` |
| `requests/daily/mini_fcl/cycle01/account.json` | `ab4f587a944e3ba378e813d1bb3552bb4dc586914ef0d88b7b0f54f7c289f4b2` |
| `requests/daily/mini_prose/cycle01/account.json` | `2cf23803ffdf899d4b70304879a6c7a60f4e91cb840f4562aa3b4e6084492341` |
| `requests/daily/mini_prose/cycle01/objection.json` | `dfa9663f43573ad4a1c7069b707bbd35ff86a70847545b6909eca9112022a0b0` |
| `requests/daily/mini_prose/cycle01/rival.json` | `47b72a451476ecec5b18a85b4e0d66bc138d495e24d4f8bcfd2c1d2d32017582` |
| `responses/daily/bare/cycle01/answer.json` | `e0385b7721a1da523b87b8b6f1ae6bbc62180c1a84eb69cfca36485c2281c69a` |
| `responses/daily/bare/cycle01/answer.txt` | `32eb2260eb171fce2866cd2c4e332dca82fb675a50ac4680dc66625876ee0e2d` |
| `responses/daily/mini_fcl/cycle01/account.json` | `8e5f276e4e7995882ae8057e67baf3476fb1b415443a655d43012e05a46890a9` |
| `responses/daily/mini_fcl/cycle01/account.txt` | `f74d74e6d6238a11c8de6d80d0a64c1b2908161f026e0492032d6137a7e117fd` |
| `responses/daily/mini_prose/cycle01/account.json` | `424b90c27c11fbe6a91113222c40a10b204e893fdac2895c93f7a4ae30381c2b` |
| `responses/daily/mini_prose/cycle01/account.txt` | `617ac46b19414a96239e2723aca727458c4cd80a307269f713c04f69b5976824` |
| `responses/daily/mini_prose/cycle01/objection.json` | `8e2f612fd181c5a0a29d3976f664d866f89b1a4835f28700002328efd105a478` |
| `responses/daily/mini_prose/cycle01/objection.txt` | `ba463a76efc70fdf99cf6c9c2c9ffc5f3a24a8af1e59fed6ca9303d769ba0c9e` |
| `responses/daily/mini_prose/cycle01/rival.json` | `3af8b73b59ef50ce6939951234517d2a4dc4cae45739ad994657ec5e1438ee5b` |
| `responses/daily/mini_prose/cycle01/rival.txt` | `30bdf4de45500870eab88b0c7b9796a5f2354f1308a56a595e06fb6f9164b498` |
| `traces/daily/bare/cycle01/answer.json` | `4ff68da01ac0c9cfd4c060d4a822f7ced327003f53e9e96f1e3fb08916a7fbab` |
| `traces/daily/mini_fcl/cycle01/account.json` | `f4790106152ef33f8f02cc8f182089bd4e99beb4f553144a79e51e2ec4f92f53` |
| `traces/daily/mini_prose/cycle01/account.json` | `5725e108b01c89983c73bc7e84268aa9bbf8b77d8b6fe57c79df1137bd5db455` |
| `traces/daily/mini_prose/cycle01/objection.json` | `035d8191d2e1de7379d69af14238f70ca674729f883b4e4161c3de0aab45b313` |
| `traces/daily/mini_prose/cycle01/rival.json` | `b7fc440d6bcc585505058030694859fd840b4f80b045b4dc110784e2e0b82e92` |
| `waves/wave0001.json` | `d0d352601d9e8304ae68bc7bd3c017b733a8db669aae06473ce8b03644ccdbba` |
| `waves/wave0002.json` | `c2195939b9aa16f3e409e5760f200cc795bdf524df8e0dceb64ead8d88336e2b` |
| `waves/wave0003.json` | `f83162c1b8bd9eddb614e6510b2a928b2a6e27c9536616c41707b49f620951bb` |

