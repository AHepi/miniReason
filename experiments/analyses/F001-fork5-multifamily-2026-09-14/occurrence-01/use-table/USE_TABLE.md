# Use-relation table - H005 occurrence-01

**The tool records juxtapositions; the reading is root's.** This table places each authored cross-document reference beside passages a root reader may find worth starting from - a finding aid, never a closed search space - and stops there. It scores nothing, ranks nothing, classifies nothing and mints no relation of its own; it has no `att`, no `dep`, no status and no label. **A lexical overlap is not evidence of use.** FCL-1's own rule is that `depends` and `mentions` are "not automatically inferred from citation or lexical overlap"; a witness of reason use "must preserve internal role bindings, not merely the endpoint string" (FW5:628); actual use is "not automatically machine-maintainable" while prompt appearance is only a delivery fact (FW5:640); and no function of an input-output projection agrees with the accounting predicate across models differing in active route (FW5:1218), "semantic use inferred from delivery logs" included (FW5:1222) - all as summarised in the FW5-versus-harness-spec review, `fw5-vs-harness-spec-review.md` §1 R2-R4, §3.1 and §5 P1/P6. Root fills the four empty cells by reading; `unresolved` is a legal value and stays unresolved (FW5:634). An empty cell is an **unread row**, not a reading of `unresolved`.

Instrument: `use_relation_h005/1`. Schema: `h005-use-relation.use-table.v1`.

## Scope

- `daily/bare/cycle01/answer`
- `daily/mini_fcl/cycle01/account`
- `daily/mini_prose/cycle01/account`
- `daily/native/cycle01/answer`
- `daily/mini_fcl/cycle01/objection`
- `daily/mini_prose/cycle01/objection`
- `daily/mini_fcl/cycle01/rival`
- `daily/mini_prose/cycle01/rival`
- `daily/mini_fcl/cycle01/response`
- `daily/mini_prose/cycle01/response`
- `daily/mini_fcl/cycle01/carry`
- `daily/mini_prose/cycle01/carry`

## Custody

- `plan_id`: `fd25a5a4ec8480b0aa9b29ba0d7ac771c16e32ce9d68709312b84c98296c3980`
- `material_sha256`: `8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff`

| check | kind | result |
|---|---|---|
| `material_pin` | cross_file | verified (1/1 occurrence) |
| `manifest_pins` | cross_file | verified (3/3 manifests) |
| `receipt_present` | cross_file | verified (12/12 nodes) |
| `artifact_bytes_vs_receipt` | cross_file | verified (12/12 nodes) |
| `status_vs_receipt` | cross_file | verified (12/12 nodes) |
| `public_text` | cross_file | verified (12/12 nodes) |
| `attempt_vs_receipt` | cross_file | verified (12/12 nodes) |
| `request_record` | cross_file | verified (12/12 nodes) |
| `trace_pinned` | cross_file | verified (12/12 nodes) |
| `provider_bytes` | cross_file | verified (12/12 nodes) |
| `wave_placement` | cross_file | verified (12/12 nodes) |
| `projection_source` | cross_file | verified (16/20 projections; 4 projection(s) had no exposed source (the slot is absent): `daily/mini_fcl/cycle01/account#p.account.0`, `daily/mini_prose/cycle01/account#p.account.0`, `daily/mini_fcl/cycle01/carry#p.carry.3`, `daily/mini_prose/cycle01/carry#p.carry.3`) |
| `plan_identity` | self_consistency | verified (1/1 occurrence) |
| `artifact_self_hash` | self_consistency | verified (12/12 nodes) |
| `artifact_coordinate` | self_consistency | verified (12/12 nodes) |
| `brief_pinned` | self_consistency | verified (12/12 nodes) |
| `brief_label_index` | self_consistency | verified (12/12 nodes) |
| `task_label` | self_consistency | verified (12/12 nodes) |

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
| refs walked | 80 |
| cross document rows | 28 |
| intra document | 38 |
| refs to exposed task artifact | 0 |
| unresolved | 14 |
| importer resolved counter | 66 |
| importer extension counter | 0 |
| importer dangling counter | 14 |

These are counts of authored refs, reported as information. No count here warrants anything (FW5:851: counts "are not outlawed as information"; what is forbidden is a count entering as an *automatic* warrant).

## Rows

### Row 1 - `daily/mini_fcl/cycle01/objection#o1` --target--> `daily/mini_fcl/cycle01/account#c1`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o1` (type `objection`) |
| ref field | `target` |
| ref verbatim | `p.objection.0#c1` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c1` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[31:622]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o1","type":"objection","text":"The selected account treats the disputes as mainly about what agreements mean, but the same described evidence is equally consistent with an unstated imbalance in who does what; the account does not exclude the simpler material-conflict reading before building a remedial program on the communication reading.","scope":"bearing on c1, c2, c3, c4 of p.objection.0","target":["p.objection.0#c1","p.objection.0#c2","p.objection.0#c3","p.objection.0#c4"],"bearing":"counters treating c1 and c2 as the frame rather than as one hypothesis among at least two"}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[31:345]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c1","type":"claim","text":"The recurring disputes are more likely about what an agreement was understood to cover than about willingness to do chores.","scope":"as a conjecture about the described situation","grounds":"the described pattern of agreeing and later disagreeing about what the agreement meant"}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c1`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[727:932]` - distinctive tokens `agreement`, `disputes`
  ```text
  Under that reading, disputes about 'what the agreement meant' are downstream of a disagreement the parties are not naming — who is carrying what, relative to what each thinks is fair given their schedules.
  ```
- `body[1607:1759]` - distinctive tokens `agreeing`, `agreement`, `disagreeing`
  ```text
  The account offers no reason to expect the first over the second, beyond the pattern of 'agreeing and later disagreeing about what the agreement meant.'
  ```
- `body[2079:2299]` - distinctive tokens `situation`
  ```text
  It could equally be read as exit from a situation the person believes is unfair and does not expect to win by arguing, or as exit from a role in which they are the one being asked for more than they think they agreed to.
  ```
- `body[2705:2802]` - distinctive tokens `agreement`, `disputes`
  ```text
  Not to settle fairness, but to see whether the 'agreement meaning' disputes have a stable object.
  ```
- `body[2803:2871]` - distinctive tokens `disputes`
  ```text
  If the tallies are close and the disputes persist, c1 gains support.
  ```
- `body[2872:3015]` - distinctive tokens `disputes`
  ```text
  If they diverge sharply and the disputes cluster around the divergence, the framing of the account is doing work the evidence has not licensed.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 2 - `daily/mini_fcl/cycle01/objection#o1` --target--> `daily/mini_fcl/cycle01/account#c2`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o1` (type `objection`) |
| ref field | `target` |
| ref verbatim | `p.objection.0#c2` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c2` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | false |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[31:622]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o1","type":"objection","text":"The selected account treats the disputes as mainly about what agreements mean, but the same described evidence is equally consistent with an unstated imbalance in who does what; the account does not exclude the simpler material-conflict reading before building a remedial program on the communication reading.","scope":"bearing on c1, c2, c3, c4 of p.objection.0","target":["p.objection.0#c1","p.objection.0#c2","p.objection.0#c3","p.objection.0#c4"],"bearing":"counters treating c1 and c2 as the frame rather than as one hypothesis among at least two"}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[346:587]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c2","type":"claim","text":"The third friend's withdrawal may be an exit from a conversation format that never converges rather than simple avoidance of responsibility.","scope":"as one plausible reading among others","depends":["c1"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c2`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[1949:2019]` - distinctive tokens `third`
  ```text
  The withdrawal of the third friend is the same evidence used two ways.
  ```
- `body[2501:2704]` - distinctive tokens `simple`
  ```text
  What I would add rather than replace: before or alongside the scope work, ask the simple question of what each person currently does in a typical fortnight, without framing it as an audit or a complaint.
  ```
- `body[3075:3211]` - distinctive tokens `third`
  ```text
  The account says the third friend may be avoiding 'a format that has felt like losing an argument' and suggests a shorter, written form.
  ```
- `body[3212:3230]` - distinctive tokens `plausible`
  ```text
  That is plausible.
  ```
- `body[3231:3454]` - distinctive tokens `plausible`
  ```text
  It is also plausible that the friend is avoiding any format in which they would have to say no to something, and a written form that invites edits could diffuse that refusal into small textual moves rather than a stated no.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 3 - `daily/mini_fcl/cycle01/objection#o1` --target--> `daily/mini_fcl/cycle01/account#c3`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o1` (type `objection`) |
| ref field | `target` |
| ref verbatim | `p.objection.0#c3` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c3` (type `commitment`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[31:622]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o1","type":"objection","text":"The selected account treats the disputes as mainly about what agreements mean, but the same described evidence is equally consistent with an unstated imbalance in who does what; the account does not exclude the simpler material-conflict reading before building a remedial program on the communication reading.","scope":"bearing on c1, c2, c3, c4 of p.objection.0","target":["p.objection.0#c1","p.objection.0#c2","p.objection.0#c3","p.objection.0#c4"],"bearing":"counters treating c1 and c2 as the frame rather than as one hypothesis among at least two"}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[588:927]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c3","type":"commitment","text":"If this account is taken up, the first move is to try naming the scope of each agreement at the moment it is made, distinguishing this-week instances from standing roles.","action":"name agreement scope explicitly when agreeing","consequence":"later memory disputes have a shared object to refer to"}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c3`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[727:932]` - distinctive tokens `agreement`, `disputes`, `naming`
  ```text
  Under that reading, disputes about 'what the agreement meant' are downstream of a disagreement the parties are not naming — who is carrying what, relative to what each thinks is fair given their schedules.
  ```
- `body[1607:1759]` - distinctive tokens `agreeing`, `agreement`
  ```text
  The account offers no reason to expect the first over the second, beyond the pattern of 'agreeing and later disagreeing about what the agreement meant.'
  ```
- `body[2705:2802]` - distinctive tokens `agreement`, `disputes`, `object`
  ```text
  Not to settle fairness, but to see whether the 'agreement meaning' disputes have a stable object.
  ```
- `body[2803:2871]` - distinctive tokens `disputes`
  ```text
  If the tallies are close and the disputes persist, c1 gains support.
  ```
- `body[2872:3015]` - distinctive tokens `disputes`
  ```text
  If they diverge sharply and the disputes cluster around the divergence, the framing of the account is doing work the evidence has not licensed.
  ```
- `body[3916:4025]` - distinctive tokens `naming`
  ```text
  The account's moves on naming scope and scheduling review are plausibly useful in many versions of this flat.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 4 - `daily/mini_fcl/cycle01/objection#o1` --target--> `daily/mini_fcl/cycle01/account#c4`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o1` (type `objection`) |
| ref field | `target` |
| ref verbatim | `p.objection.0#c4` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c4` (type `commitment`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | false |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[31:622]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o1","type":"objection","text":"The selected account treats the disputes as mainly about what agreements mean, but the same described evidence is equally consistent with an unstated imbalance in who does what; the account does not exclude the simpler material-conflict reading before building a remedial program on the communication reading.","scope":"bearing on c1, c2, c3, c4 of p.objection.0","target":["p.objection.0#c1","p.objection.0#c2","p.objection.0#c3","p.objection.0#c4"],"bearing":"counters treating c1 and c2 as the frame rather than as one hypothesis among at least two"}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[928:1235]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c4","type":"commitment","text":"Treat schedule change as normal input and give it a scheduled place, rather than treating a swap request as a breach.","action":"set a recurring short review of the coming week","consequence":"change has a landing place and does not have to be argued as an exception"}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c4`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[3916:4025]` - distinctive tokens `review`
  ```text
  The account's moves on naming scope and scheduling review are plausibly useful in many versions of this flat.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 5 - `daily/mini_fcl/cycle01/objection#o2` --target--> `daily/mini_fcl/cycle01/account#c6`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o2` (type `objection`) |
| ref field | `target` |
| ref verbatim | `p.objection.0#c6` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c6` (type `objection`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[623:1038]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o2","type":"objection","text":"The account states its own imbalance objection (c6) as caveat and then proceeds with the scope-and-review program as if the caveat did not apply; the objection is acknowledged but not carried into the proposal.","target":["p.objection.0#c6","p.objection.0#c3","p.objection.0#c4"],"bearing":"alleges an internal inconsistency between raising c6 and leaving c3 and c4 unchanged"}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[1513:1809]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c6","type":"objection","text":"The account risks treating a chore-distribution problem as primarily a communication-format problem, which could obscure an underlying imbalance in who actually does the work.","bearing":"counters any reading of c3 and c4 as sufficient","target":["c3","c4"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c6`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[1254:1385]` - distinctive tokens `problem`
  ```text
  If the problem is scoping ambiguity, then writing down categories, triggers, and announcement rules will converge the conversation.
  ```
- `body[1386:1606]` - distinctive tokens `problem`
  ```text
  If the problem is an imbalance the parties are avoiding, then formalizing scope will produce a document that records the imbalance in precise language, and the arguing will simply migrate to whether the document is fair.
  ```
- `body[4026:4233]` - distinctive tokens `communication`
  ```text
  My claim is narrower: the account leans on a communication-frame reading of the dispute more than the described evidence supports, and its own objection (c6) is not carried far enough to change the proposal.
  ```
- `body[4234:4430]` - distinctive tokens `actually`
  ```text
  The cheap diagnostic — what each person actually does in a typical fortnight, asked before the scope conversation — would either earn the frame or displace it, and the account does not propose it.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 6 - `daily/mini_fcl/cycle01/objection#o2` --target--> `daily/mini_fcl/cycle01/account#c3`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o2` (type `objection`) |
| ref field | `target` |
| ref verbatim | `p.objection.0#c3` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c3` (type `commitment`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[623:1038]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o2","type":"objection","text":"The account states its own imbalance objection (c6) as caveat and then proceeds with the scope-and-review program as if the caveat did not apply; the objection is acknowledged but not carried into the proposal.","target":["p.objection.0#c6","p.objection.0#c3","p.objection.0#c4"],"bearing":"alleges an internal inconsistency between raising c6 and leaving c3 and c4 unchanged"}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[588:927]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c3","type":"commitment","text":"If this account is taken up, the first move is to try naming the scope of each agreement at the moment it is made, distinguishing this-week instances from standing roles.","action":"name agreement scope explicitly when agreeing","consequence":"later memory disputes have a shared object to refer to"}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c3`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[727:932]` - distinctive tokens `agreement`, `disputes`, `naming`
  ```text
  Under that reading, disputes about 'what the agreement meant' are downstream of a disagreement the parties are not naming — who is carrying what, relative to what each thinks is fair given their schedules.
  ```
- `body[1607:1759]` - distinctive tokens `agreeing`, `agreement`
  ```text
  The account offers no reason to expect the first over the second, beyond the pattern of 'agreeing and later disagreeing about what the agreement meant.'
  ```
- `body[2705:2802]` - distinctive tokens `agreement`, `disputes`, `object`
  ```text
  Not to settle fairness, but to see whether the 'agreement meaning' disputes have a stable object.
  ```
- `body[2803:2871]` - distinctive tokens `disputes`
  ```text
  If the tallies are close and the disputes persist, c1 gains support.
  ```
- `body[2872:3015]` - distinctive tokens `disputes`
  ```text
  If they diverge sharply and the disputes cluster around the divergence, the framing of the account is doing work the evidence has not licensed.
  ```
- `body[3916:4025]` - distinctive tokens `naming`
  ```text
  The account's moves on naming scope and scheduling review are plausibly useful in many versions of this flat.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 7 - `daily/mini_fcl/cycle01/objection#o2` --target--> `daily/mini_fcl/cycle01/account#c4`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o2` (type `objection`) |
| ref field | `target` |
| ref verbatim | `p.objection.0#c4` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c4` (type `commitment`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | false |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[623:1038]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o2","type":"objection","text":"The account states its own imbalance objection (c6) as caveat and then proceeds with the scope-and-review program as if the caveat did not apply; the objection is acknowledged but not carried into the proposal.","target":["p.objection.0#c6","p.objection.0#c3","p.objection.0#c4"],"bearing":"alleges an internal inconsistency between raising c6 and leaving c3 and c4 unchanged"}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[928:1235]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c4","type":"commitment","text":"Treat schedule change as normal input and give it a scheduled place, rather than treating a swap request as a breach.","action":"set a recurring short review of the coming week","consequence":"change has a landing place and does not have to be argued as an exception"}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c4`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[3916:4025]` - distinctive tokens `review`
  ```text
  The account's moves on naming scope and scheduling review are plausibly useful in many versions of this flat.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 8 - `daily/mini_fcl/cycle01/objection#o3` --target--> `daily/mini_fcl/cycle01/account#c2`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o3` (type `objection`) |
| ref field | `target` |
| ref verbatim | `p.objection.0#c2` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c2` (type `claim`) |
| declared_uptake_includes_referring_record | false |
| declared_uptake_includes_target_record | false |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[1039:1500]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o3","type":"objection","text":"The account treats format change as a way to reach the withdrawing friend but does not treat the withdrawal as possibly the message itself; a gentler channel can lower the cost of silent non-participation as easily as the cost of participation, and the account only considers the second.","target":["p.objection.0#c2","p.objection.0#c5"],"bearing":"counters the choice architecture implied by the format-change suggestion"}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[346:587]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c2","type":"claim","text":"The third friend's withdrawal may be an exit from a conversation format that never converges rather than simple avoidance of responsibility.","scope":"as one plausible reading among others","depends":["c1"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c2`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[1949:2019]` - distinctive tokens `third`
  ```text
  The withdrawal of the third friend is the same evidence used two ways.
  ```
- `body[2501:2704]` - distinctive tokens `simple`
  ```text
  What I would add rather than replace: before or alongside the scope work, ask the simple question of what each person currently does in a typical fortnight, without framing it as an audit or a complaint.
  ```
- `body[3075:3211]` - distinctive tokens `third`
  ```text
  The account says the third friend may be avoiding 'a format that has felt like losing an argument' and suggests a shorter, written form.
  ```
- `body[3212:3230]` - distinctive tokens `plausible`
  ```text
  That is plausible.
  ```
- `body[3231:3454]` - distinctive tokens `plausible`
  ```text
  It is also plausible that the friend is avoiding any format in which they would have to say no to something, and a written form that invites edits could diffuse that refusal into small textual moves rather than a stated no.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 9 - `daily/mini_fcl/cycle01/objection#o3` --target--> `daily/mini_fcl/cycle01/account#c5`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o3` (type `objection`) |
| ref field | `target` |
| ref verbatim | `p.objection.0#c5` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c5` (type `problem`) |
| declared_uptake_includes_referring_record | false |
| declared_uptake_includes_target_record | false |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[1039:1500]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o3","type":"objection","text":"The account treats format change as a way to reach the withdrawing friend but does not treat the withdrawal as possibly the message itself; a gentler channel can lower the cost of silent non-participation as easily as the cost of participation, and the account only considers the second.","target":["p.objection.0#c2","p.objection.0#c5"],"bearing":"counters the choice architecture implied by the format-change suggestion"}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[1236:1512]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c5","type":"problem","text":"Whether shortening or restructuring the check-in will make the withdrawing friend more willing to participate is unknown, and if the withdrawal is about something other than chores, no scheduling change will reach it.","scope":"unresolved"}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c5`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[3569:3788]` - distinctive tokens `reach`
  ```text
  The account treats format change as a way to reach the withdrawn person, but does not treat the possibility that the withdrawal is itself the thing being communicated and would be obscured by making the channel gentler.
  ```
- `body[3916:4025]` - distinctive tokens `scheduling`
  ```text
  The account's moves on naming scope and scheduling review are plausibly useful in many versions of this flat.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 10 - `daily/mini_fcl/cycle01/carry#r1` --mentions--> `daily/mini_fcl/cycle01/response#m1`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r1` (type `claim`) |
| ref field | `mentions` |
| ref verbatim | `f1ef33e958c98f67#m1` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/response` |
| resolved target record | `m1` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[31:535]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r1","type":"claim","text":"The prior carry's evidence claim (m1) is retained: the described pattern — agreement, later disagreement about what was agreed, changing schedules, one friend withdrawing — is consistent with the account's scoping reading, the objection's imbalance reading, and the rival's positional reading, and none of the three excludes the others.","scope":"the evidence given in the task description","mentions":["f1ef33e958c98f67#m1","f8f9363d4a950370#c1","f88ebb8732052cf6#c1"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[31:507]`, code point offsets into the decoded `commitments` string)

```json
{"id":"m1","type":"claim","text":"The three contributions disagree mainly about which hypothesis to lead with, not about the evidence; the described evidence is consistent with the account's scoping reading, the objection's imbalance reading, and the rival's positional reading, and none of the three excludes the others.","scope":"the evidence given in the task description","mentions":["h005.fork5.p.response.0#c1","h005.fork5.p.response.1#c1","h005.fork5.p.response.2#r1"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/response#m1`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[253:407]` - distinctive tokens `rival`
  ```text
  Three readings were on the table: the account's scoping/communication reading, the objection's imbalance reading, and the rival's positional-dyad reading.
  ```
- `body[2304:2526]` - distinctive tokens `rival`
  ```text
  Third, the prior carry treated the rival's conversation as "the most demanding and the most likely to be heard as a procedural move," but also endorsed (m5) that the rival's diagnostic may leave the flat with no next step.
  ```
- `body[2690:3131]` - distinctive tokens `rival`
  ```text
  What remains unresolved and should stay unresolved: whether the withdrawing friend is declining the chore conversations specifically or the flat's company more generally (prior m6); whether this flat's work is roughly even or uneven (prior m7, objection p2); whether the account's c6 was meant to bound or only annotate (objection p1); and whether the rival's diagnostic conversation produces actionable output rather than a preference list.
  ```
- `body[3190:3534]` - distinctive tokens `rival`
  ```text
  What I now propose to preserve as the carry's content: the prior carry's m1 (evidence is consistent with all three readings), m3 (tally cannot distinguish the positional reading), m4 (ask what the withdrawing person is declining, before format changes), m5 (objection to the rival's diagnostic as a complete first move), m6 and m7 (unresolved).
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 11 - `daily/mini_fcl/cycle01/carry#r1` --mentions--> `daily/mini_fcl/cycle01/account#c1`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r1` (type `claim`) |
| ref field | `mentions` |
| ref verbatim | `f8f9363d4a950370#c1` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c1` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[31:535]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r1","type":"claim","text":"The prior carry's evidence claim (m1) is retained: the described pattern — agreement, later disagreement about what was agreed, changing schedules, one friend withdrawing — is consistent with the account's scoping reading, the objection's imbalance reading, and the rival's positional reading, and none of the three excludes the others.","scope":"the evidence given in the task description","mentions":["f1ef33e958c98f67#m1","f8f9363d4a950370#c1","f88ebb8732052cf6#c1"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[31:345]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c1","type":"claim","text":"The recurring disputes are more likely about what an agreement was understood to cover than about willingness to do chores.","scope":"as a conjecture about the described situation","grounds":"the described pattern of agreeing and later disagreeing about what the agreement meant"}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c1`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[1041:1384]` - distinctive tokens `agreeing`
  ```text
  The account's c3/c4 (name scope when agreeing; schedule a weekly review) and the objection's u1 (fortnight tally first or alongside) and u2 (treat withdrawal as possibly the message) point in compatible practical directions, but the account's own c6 objection says naming scope and weekly review are not sufficient if the problem is imbalance.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 12 - `daily/mini_fcl/cycle01/carry#r1` --mentions--> `daily/mini_fcl/cycle01/objection#c1`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r1` (type `claim`) |
| ref field | `mentions` |
| ref verbatim | `f88ebb8732052cf6#c1` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/objection` |
| resolved target record | `c1` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | false |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[31:535]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r1","type":"claim","text":"The prior carry's evidence claim (m1) is retained: the described pattern — agreement, later disagreement about what was agreed, changing schedules, one friend withdrawing — is consistent with the account's scoping reading, the objection's imbalance reading, and the rival's positional reading, and none of the three excludes the others.","scope":"the evidence given in the task description","mentions":["f1ef33e958c98f67#m1","f8f9363d4a950370#c1","f88ebb8732052cf6#c1"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[1501:1793]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c1","type":"claim","text":"In many flats the described pattern of agree-then-disagree-about-meaning is also produced by an unstated imbalance in who carries the work, not only by scoping ambiguity.","scope":"as one competing reading of the described situation, not as the correct one"}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/objection#c1`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

*no lexical overlap found*

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 13 - `daily/mini_fcl/cycle01/carry#r2` --target--> `daily/mini_fcl/cycle01/response#m2`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r2` (type `claim`) |
| ref field | `target` |
| ref verbatim | `f1ef33e958c98f67#m2` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/response` |
| resolved target record | `m2` (type `commitment`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[536:1151]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r2","type":"claim","text":"The prior carry's recommendation should be stated without the condition it was given: the defensible rule is to run the cheapest diagnostic that discriminates among the currently live readings when only one can be run, not to run the tally whenever patience is short. The prior m2's condition (\"if the flat has one meeting's worth of patience\") was not licensed by the prior body, which said choose by cost.","scope":"revision of prior m2","target":["f1ef33e958c98f67#m2"],"bearing":"narrows the commitment to a cost rule with an explicit scope, rather than a trigger condition"}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[508:980]`, code point offsets into the decoded `commitments` string)

```json
{"id":"m2","type":"commitment","text":"Pick one diagnostic and run it before committing to a remedy, choosing by cost rather than by conviction; if the flat has one meeting's worth of patience, use the fortnight tally first.","action":"run one diagnostic before adopting a remedy","consequence":"the framing of the dispute is tested rather than assumed, at the lowest available cost","depends":["m1"],"mentions":["h005.fork5.p.response.1#u1","h005.fork5.p.response.0#c3"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/response#m2`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[110:252]` - distinctive tokens `dispute`
  ```text
  What survives, and should be retained: the flat's dispute is real and the evidence in the task is compatible with more than one reading of it.
  ```
- `body[408:517]` - distinctive tokens `conviction`
  ```text
  The prior carry's own move was to hold all three and to choose a first action by cost rather than conviction.
  ```
- `body[518:881]` - distinctive tokens `meeting`, `patience`, `worth`
  ```text
  That move still looks right, but the carry changed the object it was defending: the prior body argued for running one diagnostic chosen by cost, while the prior commitments made two things mandatory — run the tally first if there is only one meeting's worth of patience (m2), and ask the withdrawing person what they are declining before changing the format (m4).
  ```
- `body[912:1040]` - distinctive tokens `patience`
  ```text
  "Choose by cost" endorses the tally when patience is short; m4 then adds an obligation that does not depend on the tally at all.
  ```
- `body[1549:1708]` - distinctive tokens `meeting`, `patience`, `worth`
  ```text
  What I would revise from the prior carry: m2's condition ("if the flat has one meeting's worth of patience") is doing work that the prior body did not license.
  ```
- `body[1709:1786]` - distinctive tokens `patience`
  ```text
  The body said choose by cost, not "use the tally whenever patience is short."
  ```
- `body[2527:2688]` - distinctive tokens `meeting`, `patience`, `tested`, `worth`
  ```text
  Both can be true; neither was tested against the task, which gives only one meeting's worth of described patience in the form of a friend avoiding conversations.
  ```
- `body[4519:4767]` - distinctive tokens `worth`
  ```text
  If the next invocation finds the withdrawal is about the flat's company rather than chores, the imbalance and scoping readings both lose their grip and the positional reading gains; that contingency was not in the prior carry and is worth flagging.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 14 - `daily/mini_fcl/cycle01/carry#r3` --mentions--> `daily/mini_fcl/cycle01/response#m3`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r3` (type `claim`) |
| ref field | `mentions` |
| ref verbatim | `f1ef33e958c98f67#m3` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/response` |
| resolved target record | `m3` (type `claim`) |
| declared_uptake_includes_referring_record | false |
| declared_uptake_includes_target_record | false |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[1152:1618]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r3","type":"claim","text":"The fortnight tally cannot distinguish the positional reading from the scoping or imbalance readings, because a dyad can produce either a convergent or a divergent tally; it also already commits the flat to a partial move in the imbalance frame, by asking someone to record what they did.","scope":"limits of the tally as a diagnostic","depends":["r1"],"mentions":["f1ef33e958c98f67#m3","f88ebb8732052cf6#c2","f88ebb8732052cf6#p2"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[981:1360]`, code point offsets into the decoded `commitments` string)

```json
{"id":"m3","type":"claim","text":"The fortnight tally can discriminate between the scoping reading and the imbalance reading but cannot distinguish the positional reading from either, since a dyad can produce a convergent or a divergent tally.","scope":"limits of the tally as a diagnostic","depends":["m1"],"mentions":["h005.fork5.p.response.1#u1","h005.fork5.p.response.2#r3"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/response#m3`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

*no lexical overlap found*

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 15 - `daily/mini_fcl/cycle01/carry#r3` --mentions--> `daily/mini_fcl/cycle01/objection#c2`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r3` (type `claim`) |
| ref field | `mentions` |
| ref verbatim | `f88ebb8732052cf6#c2` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/objection` |
| resolved target record | `c2` (type `claim`) |
| declared_uptake_includes_referring_record | false |
| declared_uptake_includes_target_record | false |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[1152:1618]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r3","type":"claim","text":"The fortnight tally cannot distinguish the positional reading from the scoping or imbalance readings, because a dyad can produce either a convergent or a divergent tally; it also already commits the flat to a partial move in the imbalance frame, by asking someone to record what they did.","scope":"limits of the tally as a diagnostic","depends":["r1"],"mentions":["f1ef33e958c98f67#m3","f88ebb8732052cf6#c2","f88ebb8732052cf6#p2"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[1794:2075]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c2","type":"claim","text":"A cheap diagnostic exists that would help discriminate between the communication-frame reading and the imbalance reading: a non-punitive tally of what each person does in a typical fortnight, taken before the scope conversation.","depends":["c1"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/objection#c2`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[253:407]` - distinctive tokens `communication`
  ```text
  Three readings were on the table: the account's scoping/communication reading, the objection's imbalance reading, and the rival's positional-dyad reading.
  ```
- `body[1871:2209]` - distinctive tokens `frame`
  ```text
  Second, the prior body's line that the tally "discriminates between two of the three readings and does not require anyone to concede a frame" overstates: a tally requires someone to record what they did, which is already a move in the imbalance frame, and the objection's own p2 concedes it has no evidence about this flat's distribution.
  ```
- `body[3535:3820]` - distinctive tokens `cheap`
  ```text
  I would drop the prior m2's conditional and replace it with a claim of the form: if only one diagnostic can be run, run the cheapest that discriminates between the two human-relations readings currently live, and note that the positional reading is not reached by any cheap diagnostic.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 16 - `daily/mini_fcl/cycle01/carry#r3` --mentions--> `daily/mini_fcl/cycle01/objection#p2`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r3` (type `claim`) |
| ref field | `mentions` |
| ref verbatim | `f88ebb8732052cf6#p2` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/objection` |
| resolved target record | `p2` (type `problem`) |
| declared_uptake_includes_referring_record | false |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[1152:1618]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r3","type":"claim","text":"The fortnight tally cannot distinguish the positional reading from the scoping or imbalance readings, because a dyad can produce either a convergent or a divergent tally; it also already commits the flat to a partial move in the imbalance frame, by asking someone to record what they did.","scope":"limits of the tally as a diagnostic","depends":["r1"],"mentions":["f1ef33e958c98f67#m3","f88ebb8732052cf6#c2","f88ebb8732052cf6#p2"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[3027:3309]`, code point offsets into the decoded `commitments` string)

```json
{"id":"p2","type":"problem","text":"I do not have evidence about this specific flat's actual distribution of work; my objection rests on the account not excluding the imbalance reading, not on a claim that the imbalance reading is true here.","scope":"unresolved","mentions":["c1"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/objection#p2`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

*no lexical overlap found*

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 17 - `daily/mini_fcl/cycle01/carry#r4` --mentions--> `daily/mini_fcl/cycle01/response#m4`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r4` (type `commitment`) |
| ref field | `mentions` |
| ref verbatim | `f1ef33e958c98f67#m4` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/response` |
| resolved target record | `m4` (type `commitment`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[1619:2141]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r4","type":"commitment","text":"Ask the withdrawing friend what they are declining, not only whether the format is hard, and ask before changing the format; a gentler channel can lower the cost of silent non-participation as easily as the cost of participation.","action":"ask what is being declined, before any format change","consequence":"a refusal that is not about chores has a chance of being heard as a refusal","depends":["r1"],"mentions":["f1ef33e958c98f67#m4","f88ebb8732052cf6#u2","f88ebb8732052cf6#o3"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[1361:1868]`, code point offsets into the decoded `commitments` string)

```json
{"id":"m4","type":"commitment","text":"Ask the withdrawing person what they are declining, not whether the format is hard, and ask before changing the format, because a gentler channel can be the most effective way to keep a refusal from being heard.","action":"ask what is being declined, before format changes","consequence":"a no that is not about chores has a chance of being heard as a no","depends":["h005.fork5.p.response.1#u2"],"mentions":["h005.fork5.p.response.1#o3","h005.fork5.p.response.2#r2"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/response#m4`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[518:881]` - distinctive tokens `changing`
  ```text
  That move still looks right, but the carry changed the object it was defending: the prior body argued for running one diagnostic chosen by cost, while the prior commitments made two things mandatory — run the tally first if there is only one meeting's worth of patience (m2), and ask the withdrawing person what they are declining before changing the format (m4).
  ```
- `body[2304:2526]` - distinctive tokens `heard`
  ```text
  Third, the prior carry treated the rival's conversation as "the most demanding and the most likely to be heard as a procedural move," but also endorsed (m5) that the rival's diagnostic may leave the flat with no next step.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 18 - `daily/mini_fcl/cycle01/carry#r4` --mentions--> `daily/mini_fcl/cycle01/objection#u2`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r4` (type `commitment`) |
| ref field | `mentions` |
| ref verbatim | `f88ebb8732052cf6#u2` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/objection` |
| resolved target record | `u2` (type `use`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | false |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[1619:2141]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r4","type":"commitment","text":"Ask the withdrawing friend what they are declining, not only whether the format is hard, and ask before changing the format; a gentler channel can lower the cost of silent non-participation as easily as the cost of participation.","action":"ask what is being declined, before any format change","consequence":"a refusal that is not about chores has a chance of being heard as a refusal","depends":["r1"],"mentions":["f1ef33e958c98f67#m4","f88ebb8732052cf6#u2","f88ebb8732052cf6#o3"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[2472:2798]`, code point offsets into the decoded `commitments` string)

```json
{"id":"u2","type":"use","text":"Treat the withdrawal as possibly the message, not only as a signal about the channel, and test that explicitly rather than inferring channel-aversion from the withdrawal alone.","action":"ask the withdrawing friend what they are declining, not only whether the format is hard","depends":["o3"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/objection#u2`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[1041:1384]` - distinctive tokens `message`, `possibly`
  ```text
  The account's c3/c4 (name scope when agreeing; schedule a weekly review) and the objection's u1 (fortnight tally first or alongside) and u2 (treat withdrawal as possibly the message) point in compatible practical directions, but the account's own c6 objection says naming scope and weekly review are not sufficient if the problem is imbalance.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 19 - `daily/mini_fcl/cycle01/carry#r4` --mentions--> `daily/mini_fcl/cycle01/objection#o3`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r4` (type `commitment`) |
| ref field | `mentions` |
| ref verbatim | `f88ebb8732052cf6#o3` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/objection` |
| resolved target record | `o3` (type `objection`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | false |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[1619:2141]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r4","type":"commitment","text":"Ask the withdrawing friend what they are declining, not only whether the format is hard, and ask before changing the format; a gentler channel can lower the cost of silent non-participation as easily as the cost of participation.","action":"ask what is being declined, before any format change","consequence":"a refusal that is not about chores has a chance of being heard as a refusal","depends":["r1"],"mentions":["f1ef33e958c98f67#m4","f88ebb8732052cf6#u2","f88ebb8732052cf6#o3"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[1039:1500]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o3","type":"objection","text":"The account treats format change as a way to reach the withdrawing friend but does not treat the withdrawal as possibly the message itself; a gentler channel can lower the cost of silent non-participation as easily as the cost of participation, and the account only considers the second.","target":["p.objection.0#c2","p.objection.0#c5"],"bearing":"counters the choice architecture implied by the format-change suggestion"}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/objection#o3`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[1041:1384]` - distinctive tokens `message`, `possibly`
  ```text
  The account's c3/c4 (name scope when agreeing; schedule a weekly review) and the objection's u1 (fortnight tally first or alongside) and u2 (treat withdrawal as possibly the message) point in compatible practical directions, but the account's own c6 objection says naming scope and weekly review are not sufficient if the problem is imbalance.
  ```
- `body[1871:2209]` - distinctive tokens `second`
  ```text
  Second, the prior body's line that the tally "discriminates between two of the three readings and does not require anyone to concede a frame" overstates: a tally requires someone to record what they did, which is already a move in the imbalance frame, and the objection's own p2 concedes it has no evidence about this flat's distribution.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 20 - `daily/mini_fcl/cycle01/carry#r5` --target--> `daily/mini_fcl/cycle01/response#m5`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r5` (type `objection`) |
| ref field | `target` |
| ref verbatim | `f1ef33e958c98f67#m5` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/response` |
| resolved target record | `m5` (type `objection`) |
| declared_uptake_includes_referring_record | false |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[2142:2631]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r5","type":"objection","text":"The rival's \"what I do not want to lose is ___\" conversation risks producing a list of preferences with no procedure for acting on them, and the rival does not address what the flat does with three uncomfortable sentences if the chores turn out to have been the site of the conflict after all.","target":["f1ef33e958c98f67#m5"],"bearing":"counters treating the rival's diagnostic as a complete first move; it may leave the flat without a next step"}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[1869:2339]`, code point offsets into the decoded `commitments` string)

```json
{"id":"m5","type":"objection","text":"The rival's diagnostic conversation risks producing a list of preferences with no procedure for acting on them, and the rival does not address what the flat does with three uncomfortable sentences if the chores turn out to have been the site of the conflict after all.","target":["h005.fork5.p.response.2#r4"],"bearing":"counters treating r4 as a complete first move; it is a diagnostic that may leave the flat without a next step"}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/response#m5`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[253:407]` - distinctive tokens `rival`
  ```text
  Three readings were on the table: the account's scoping/communication reading, the objection's imbalance reading, and the rival's positional-dyad reading.
  ```
- `body[2304:2526]` - distinctive tokens `leave`, `rival`
  ```text
  Third, the prior carry treated the rival's conversation as "the most demanding and the most likely to be heard as a procedural move," but also endorsed (m5) that the rival's diagnostic may leave the flat with no next step.
  ```
- `body[2690:3131]` - distinctive tokens `rival`
  ```text
  What remains unresolved and should stay unresolved: whether the withdrawing friend is declining the chore conversations specifically or the flat's company more generally (prior m6); whether this flat's work is roughly even or uneven (prior m7, objection p2); whether the account's c6 was meant to bound or only annotate (objection p1); and whether the rival's diagnostic conversation produces actionable output rather than a preference list.
  ```
- `body[3190:3534]` - distinctive tokens `complete`, `rival`
  ```text
  What I now propose to preserve as the carry's content: the prior carry's m1 (evidence is consistent with all three readings), m3 (tally cannot distinguish the positional reading), m4 (ask what the withdrawing person is declining, before format changes), m5 (objection to the rival's diagnostic as a complete first move), m6 and m7 (unresolved).
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 21 - `daily/mini_fcl/cycle01/carry#r6` --target--> `daily/mini_fcl/cycle01/account#c3`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r6` (type `objection`) |
| ref field | `target` |
| ref verbatim | `f8f9363d4a950370#c3` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c3` (type `commitment`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[2632:3089]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r6","type":"objection","text":"The account states its own imbalance objection (c6) and then proceeds with c3 and c4 unchanged; the caveat is acknowledged but not carried into the proposal, so the account's program is not entitled to the scope of application c3 and c4 imply.","target":["f8f9363d4a950370#c3","f8f9363d4a950370#c4","f8f9363d4a950370#c6"],"bearing":"alleges an internal inconsistency between raising c6 and leaving c3 and c4 unchanged"}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[588:927]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c3","type":"commitment","text":"If this account is taken up, the first move is to try naming the scope of each agreement at the moment it is made, distinguishing this-week instances from standing roles.","action":"name agreement scope explicitly when agreeing","consequence":"later memory disputes have a shared object to refer to"}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c3`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[518:881]` - distinctive tokens `object`
  ```text
  That move still looks right, but the carry changed the object it was defending: the prior body argued for running one diagnostic chosen by cost, while the prior commitments made two things mandatory — run the tally first if there is only one meeting's worth of patience (m2), and ask the withdrawing person what they are declining before changing the format (m4).
  ```
- `body[1041:1384]` - distinctive tokens `agreeing`, `naming`
  ```text
  The account's c3/c4 (name scope when agreeing; schedule a weekly review) and the objection's u1 (fortnight tally first or alongside) and u2 (treat withdrawal as possibly the message) point in compatible practical directions, but the account's own c6 objection says naming scope and weekly review are not sufficient if the problem is imbalance.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 22 - `daily/mini_fcl/cycle01/carry#r6` --target--> `daily/mini_fcl/cycle01/account#c4`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r6` (type `objection`) |
| ref field | `target` |
| ref verbatim | `f8f9363d4a950370#c4` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c4` (type `commitment`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | false |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[2632:3089]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r6","type":"objection","text":"The account states its own imbalance objection (c6) and then proceeds with c3 and c4 unchanged; the caveat is acknowledged but not carried into the proposal, so the account's program is not entitled to the scope of application c3 and c4 imply.","target":["f8f9363d4a950370#c3","f8f9363d4a950370#c4","f8f9363d4a950370#c6"],"bearing":"alleges an internal inconsistency between raising c6 and leaving c3 and c4 unchanged"}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[928:1235]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c4","type":"commitment","text":"Treat schedule change as normal input and give it a scheduled place, rather than treating a swap request as a breach.","action":"set a recurring short review of the coming week","consequence":"change has a landing place and does not have to be argued as an exception"}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c4`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[518:881]` - distinctive tokens `argued`
  ```text
  That move still looks right, but the carry changed the object it was defending: the prior body argued for running one diagnostic chosen by cost, while the prior commitments made two things mandatory — run the tally first if there is only one meeting's worth of patience (m2), and ask the withdrawing person what they are declining before changing the format (m4).
  ```
- `body[1041:1384]` - distinctive tokens `review`, `schedule`
  ```text
  The account's c3/c4 (name scope when agreeing; schedule a weekly review) and the objection's u1 (fortnight tally first or alongside) and u2 (treat withdrawal as possibly the message) point in compatible practical directions, but the account's own c6 objection says naming scope and weekly review are not sufficient if the problem is imbalance.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 23 - `daily/mini_fcl/cycle01/carry#r6` --target--> `daily/mini_fcl/cycle01/account#c6`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r6` (type `objection`) |
| ref field | `target` |
| ref verbatim | `f8f9363d4a950370#c6` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c6` (type `objection`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[2632:3089]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r6","type":"objection","text":"The account states its own imbalance objection (c6) and then proceeds with c3 and c4 unchanged; the caveat is acknowledged but not carried into the proposal, so the account's program is not entitled to the scope of application c3 and c4 imply.","target":["f8f9363d4a950370#c3","f8f9363d4a950370#c4","f8f9363d4a950370#c6"],"bearing":"alleges an internal inconsistency between raising c6 and leaving c3 and c4 unchanged"}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[1513:1809]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c6","type":"objection","text":"The account risks treating a chore-distribution problem as primarily a communication-format problem, which could obscure an underlying imbalance in who actually does the work.","bearing":"counters any reading of c3 and c4 as sufficient","target":["c3","c4"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c6`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[253:407]` - distinctive tokens `communication`
  ```text
  Three readings were on the table: the account's scoping/communication reading, the objection's imbalance reading, and the rival's positional-dyad reading.
  ```
- `body[1041:1384]` - distinctive tokens `problem`, `sufficient`
  ```text
  The account's c3/c4 (name scope when agreeing; schedule a weekly review) and the objection's u1 (fortnight tally first or alongside) and u2 (treat withdrawal as possibly the message) point in compatible practical directions, but the account's own c6 objection says naming scope and weekly review are not sufficient if the problem is imbalance.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 24 - `daily/mini_fcl/cycle01/carry#r7` --mentions--> `daily/mini_fcl/cycle01/objection#p1`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r7` (type `problem`) |
| ref field | `mentions` |
| ref verbatim | `f88ebb8732052cf6#p1` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/objection` |
| resolved target record | `p1` (type `problem`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | false |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[3090:3361]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r7","type":"problem","text":"Whether the account's own c6 was meant to bound its proposal or only to annotate it is not determinable from the text; the answer changes whether r6 lands.","scope":"unresolved","mentions":["f88ebb8732052cf6#p1","f8f9363d4a950370#c6"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[2799:3026]`, code point offsets into the decoded `commitments` string)

```json
{"id":"p1","type":"problem","text":"Whether the account's own c6 was meant to bound the proposal or only to annotate it is not determinable from the text; the answer changes whether my objection o2 lands.","scope":"unresolved"}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/objection#p1`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[2690:3131]` - distinctive tokens `annotate`, `bound`
  ```text
  What remains unresolved and should stay unresolved: whether the withdrawing friend is declining the chore conversations specifically or the flat's company more generally (prior m6); whether this flat's work is roughly even or uneven (prior m7, objection p2); whether the account's c6 was meant to bound or only annotate (objection p1); and whether the rival's diagnostic conversation produces actionable output rather than a preference list.
  ```
- `body[3821:4074]` - distinctive tokens `lands`
  ```text
  I would also adopt the objection's o2 as a live criticism of the account's program, not as settled: the account raised c6 and did not revise c3/c4. And I would carry the objection's p1 forward as an open question, because it determines whether o2 lands.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 25 - `daily/mini_fcl/cycle01/carry#r7` --mentions--> `daily/mini_fcl/cycle01/account#c6`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r7` (type `problem`) |
| ref field | `mentions` |
| ref verbatim | `f8f9363d4a950370#c6` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c6` (type `objection`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[3090:3361]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r7","type":"problem","text":"Whether the account's own c6 was meant to bound its proposal or only to annotate it is not determinable from the text; the answer changes whether r6 lands.","scope":"unresolved","mentions":["f88ebb8732052cf6#p1","f8f9363d4a950370#c6"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[1513:1809]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c6","type":"objection","text":"The account risks treating a chore-distribution problem as primarily a communication-format problem, which could obscure an underlying imbalance in who actually does the work.","bearing":"counters any reading of c3 and c4 as sufficient","target":["c3","c4"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c6`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[253:407]` - distinctive tokens `communication`
  ```text
  Three readings were on the table: the account's scoping/communication reading, the objection's imbalance reading, and the rival's positional-dyad reading.
  ```
- `body[1041:1384]` - distinctive tokens `problem`, `sufficient`
  ```text
  The account's c3/c4 (name scope when agreeing; schedule a weekly review) and the objection's u1 (fortnight tally first or alongside) and u2 (treat withdrawal as possibly the message) point in compatible practical directions, but the account's own c6 objection says naming scope and weekly review are not sufficient if the problem is imbalance.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 26 - `daily/mini_fcl/cycle01/carry#r8` --mentions--> `daily/mini_fcl/cycle01/response#m6`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r8` (type `problem`) |
| ref field | `mentions` |
| ref verbatim | `f1ef33e958c98f67#m6` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/response` |
| resolved target record | `m6` (type `problem`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | false |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[3362:3753]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r8","type":"problem","text":"Whether the withdrawing friend is avoiding the chore conversations specifically or the flat's company more generally is not distinguishable from the task description, and the two call for different responses; the prior carry did not carry this contingency into its recommendation.","scope":"unresolved","depends":["r4"],"mentions":["f1ef33e958c98f67#m6"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[2340:2616]`, code point offsets into the decoded `commitments` string)

```json
{"id":"m6","type":"problem","text":"Whether the withdrawing friend is avoiding the chore conversations specifically or avoiding the flat's company more generally is not distinguishable from the task description, and the two call for different responses.","scope":"unresolved"}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/response#m6`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[2527:2688]` - distinctive tokens `avoiding`, `conversations`
  ```text
  Both can be true; neither was tested against the task, which gives only one meeting's worth of described patience in the form of a friend avoiding conversations.
  ```
- `body[2690:3131]` - distinctive tokens `company`, `conversations`, `generally`, `specifically`
  ```text
  What remains unresolved and should stay unresolved: whether the withdrawing friend is declining the chore conversations specifically or the flat's company more generally (prior m6); whether this flat's work is roughly even or uneven (prior m7, objection p2); whether the account's c6 was meant to bound or only annotate (objection p1); and whether the rival's diagnostic conversation produces actionable output rather than a preference list.
  ```
- `body[4519:4767]` - distinctive tokens `company`
  ```text
  If the next invocation finds the withdrawal is about the flat's company rather than chores, the imbalance and scoping readings both lose their grip and the positional reading gains; that contingency was not in the prior carry and is worth flagging.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 27 - `daily/mini_fcl/cycle01/carry#r9` --mentions--> `daily/mini_fcl/cycle01/response#m7`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r9` (type `problem`) |
| ref field | `mentions` |
| ref verbatim | `f1ef33e958c98f67#m7` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/response` |
| resolved target record | `m7` (type `problem`) |
| declared_uptake_includes_referring_record | false |
| declared_uptake_includes_target_record | false |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[3754:4069]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r9","type":"problem","text":"I have no evidence about this flat's actual distribution of work, and I will not convert the objection's point that the imbalance reading is not excluded into a claim that the imbalance is real here.","scope":"unresolved","mentions":["f1ef33e958c98f67#m7","f88ebb8732052cf6#p2"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[2617:2917]`, code point offsets into the decoded `commitments` string)

```json
{"id":"m7","type":"problem","text":"I have no evidence about this flat's actual distribution of work, and I will not convert the objection's point that the imbalance reading is not excluded into a claim that the imbalance is real here.","scope":"unresolved","mentions":["h005.fork5.p.response.1#p2"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/response#m7`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[1041:1384]` - distinctive tokens `point`
  ```text
  The account's c3/c4 (name scope when agreeing; schedule a weekly review) and the objection's u1 (fortnight tally first or alongside) and u2 (treat withdrawal as possibly the message) point in compatible practical directions, but the account's own c6 objection says naming scope and weekly review are not sufficient if the problem is imbalance.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 28 - `daily/mini_fcl/cycle01/carry#r9` --mentions--> `daily/mini_fcl/cycle01/objection#p2`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `r9` (type `problem`) |
| ref field | `mentions` |
| ref verbatim | `f88ebb8732052cf6#p2` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/objection` |
| resolved target record | `p2` (type `problem`) |
| declared_uptake_includes_referring_record | false |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[3754:4069]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r9","type":"problem","text":"I have no evidence about this flat's actual distribution of work, and I will not convert the objection's point that the imbalance reading is not excluded into a claim that the imbalance is real here.","scope":"unresolved","mentions":["f1ef33e958c98f67#m7","f88ebb8732052cf6#p2"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[3027:3309]`, code point offsets into the decoded `commitments` string)

```json
{"id":"p2","type":"problem","text":"I do not have evidence about this specific flat's actual distribution of work; my objection rests on the account not excluding the imbalance reading, not on a claim that the imbalance reading is true here.","scope":"unresolved","mentions":["c1"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/objection#p2`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

*no lexical overlap found*

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

## Declared uptake versus records present

### `daily/mini_fcl/cycle01/account`

- commitment surface: `read_fcl1`
- records present (6): `c1`, `c2`, `c3`, `c4`, `c5`, `c6`
- declared `uptake` (3): `c1`, `c3`, `c6`
- records in uptake (3): `c1`, `c3`, `c6`
- records omitted from uptake (3): `c2`, `c4`, `c5`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/objection`

- commitment surface: `read_fcl1`
- records present (9): `o1`, `o2`, `o3`, `c1`, `c2`, `u1`, `u2`, `p1`, `p2`
- declared `uptake` (4): `o1`, `o2`, `u1`, `p2`
- records in uptake (4): `o1`, `o2`, `u1`, `p2`
- records omitted from uptake (5): `o3`, `c1`, `c2`, `u2`, `p1`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/rival`

- commitment surface: `read_fcl1`
- records present (7): `r1`, `r2`, `r3`, `r4`, `r5`, `r6`, `r7`
- declared `uptake` (4): `r1`, `r3`, `r4`, `r6`
- records in uptake (4): `r1`, `r3`, `r4`, `r6`
- records omitted from uptake (3): `r2`, `r5`, `r7`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/response`

- commitment surface: `read_fcl1`
- records present (7): `m1`, `m2`, `m3`, `m4`, `m5`, `m6`, `m7`
- declared `uptake` (4): `m1`, `m2`, `m4`, `m5`
- records in uptake (4): `m1`, `m2`, `m4`, `m5`
- records omitted from uptake (3): `m3`, `m6`, `m7`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/carry`

- commitment surface: `read_fcl1`
- records present (9): `r1`, `r2`, `r3`, `r4`, `r5`, `r6`, `r7`, `r8`, `r9`
- declared `uptake` (6): `r1`, `r2`, `r4`, `r6`, `r7`, `r8`
- records in uptake (6): `r1`, `r2`, `r4`, `r6`, `r7`, `r8`
- records omitted from uptake (3): `r3`, `r5`, `r9`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

## Nodes whose commitment surface was not read

- `daily/bare/cycle01/answer` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_prose/cycle01/account` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/native/cycle01/answer` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_prose/cycle01/objection` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_prose/cycle01/rival` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_prose/cycle01/response` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_prose/cycle01/carry` - commitment surface: prose (not parsed); references not extractable by this instrument

## Residue: refs that resolve to nothing

| referring coordinate | record | field | ref | code | reason |
|---|---|---|---|---|---|
| `daily/mini_fcl/cycle01/rival` | `r1` | `target` | `c091ef6622b07600dcc83ac1d7c293f1393890e566ce9712883a548a770d7316#body` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/rival` | `r6` | `mentions` | `c091ef6622b07600dcc83ac1d7c293f1393890e566ce9712883a548a770d7316#body` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `m1` | `mentions` | `h005.fork5.p.response.0#c1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `m1` | `mentions` | `h005.fork5.p.response.1#c1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `m1` | `mentions` | `h005.fork5.p.response.2#r1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `m2` | `mentions` | `h005.fork5.p.response.1#u1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `m2` | `mentions` | `h005.fork5.p.response.0#c3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `m3` | `mentions` | `h005.fork5.p.response.1#u1` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `m3` | `mentions` | `h005.fork5.p.response.2#r3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `m4` | `mentions` | `h005.fork5.p.response.1#o3` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `m4` | `mentions` | `h005.fork5.p.response.2#r2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `m4` | `depends` | `h005.fork5.p.response.1#u2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `m7` | `mentions` | `h005.fork5.p.response.1#p2` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |
| `daily/mini_fcl/cycle01/response` | `m5` | `target` | `h005.fork5.p.response.2#r4` | `ref_unresolved` | exposed-artifact label is not in this node's projection index; dropped, never invented |

## Files read

Every byte this instrument read, with its sha256. Nothing under the occurrence was written.

| path | sha256 |
|---|---|
| `artifacts/daily/bare/cycle01/answer.json` | `44e1de8ffb17a5a986483e84209f3b988c69a0c83f1df63f25f20e9ac0018dbb` |
| `artifacts/daily/mini_fcl/cycle01/account.json` | `61016c4955d08a97f30d21c69d8cd8d7c0af0ba16b5fe61a7aa162bba0bcd6f0` |
| `artifacts/daily/mini_fcl/cycle01/carry.json` | `ece57747fc6f573aedc0695d22c0492864c820b753f3fe82ee47c1597292e587` |
| `artifacts/daily/mini_fcl/cycle01/objection.json` | `837afc39f263be01471367b9c4bae44ce248960e4ebfe48b7e9436cd0d7c5bdf` |
| `artifacts/daily/mini_fcl/cycle01/response.json` | `2fb7525c7ed516096e6c19db528c12372d7edbaf9c9a68dfa7c1bb9f0eeaa3f5` |
| `artifacts/daily/mini_fcl/cycle01/rival.json` | `d2731fe88de3f53a3656f983c75814f8168281edc218cf7fec7c3db7758ebd69` |
| `artifacts/daily/mini_prose/cycle01/account.json` | `6c31a55824b06279f5e11564b47d3688f44b4d32a449708a79a33e979f89c8df` |
| `artifacts/daily/mini_prose/cycle01/carry.json` | `29d1d9caa299708e852e694aaec603e12b80592d1e5af84222685d48bd3b8b3f` |
| `artifacts/daily/mini_prose/cycle01/objection.json` | `16b96dba473d9469946e99533396add0b80118f8cf4eb543862f8140c9da1288` |
| `artifacts/daily/mini_prose/cycle01/response.json` | `9cafb0718055c4c02209978851b3e3dc73274e96f2be2781cb63a92febb970ba` |
| `artifacts/daily/mini_prose/cycle01/rival.json` | `115093ff57135d44019e0bb7a6ee764562c0f7a7ea0677e06f8691e16fd37297` |
| `artifacts/daily/native/cycle01/answer.json` | `c584244b1b1b3e5118367f6892a7a65a1dafdeda4cd80db93fe2eca8bf5bd4d3` |
| `attempts/daily/bare/cycle01/answer.json` | `8d2bc09eea514cc5b4a153319c3d32502ed3b2cdc5de50a799416945678f8040` |
| `attempts/daily/mini_fcl/cycle01/account.json` | `2a5dbea8e3bbe1f4b79ff9a85c87e929a5d9bbe9f54f8910c3a8838b3f478277` |
| `attempts/daily/mini_fcl/cycle01/carry.json` | `eaea9ddc8161379e04954f2e051d2dbc2354cb13dd96e412f78f300dcff4b94d` |
| `attempts/daily/mini_fcl/cycle01/objection.json` | `c162172e3f57f68de3d1bf6f52c93b37d2cd2cc3b8ab49558f25f92cb9b49ae2` |
| `attempts/daily/mini_fcl/cycle01/response.json` | `df06585484561633969c8db877ee5d2025afb6ecfcc40ef176aea84b76e7eabd` |
| `attempts/daily/mini_fcl/cycle01/rival.json` | `35ae9d2bbfb9c1f80174313e5365a3d0b19a7707dcab8bca9655cc9f2fb20114` |
| `attempts/daily/mini_prose/cycle01/account.json` | `f3add7b992d79b92b2fa05625ceb874a1d7d4df353daa28735840e51deae0105` |
| `attempts/daily/mini_prose/cycle01/carry.json` | `8954b3f17f33c432cfba0e3112acb44cac439b216a5273d219ad4f2dda4eee5e` |
| `attempts/daily/mini_prose/cycle01/objection.json` | `dffdce333f04e013b2ece38cf039d7c3b2c901a9219464476c09835f5a32af7d` |
| `attempts/daily/mini_prose/cycle01/response.json` | `05f02a5775b72c201cf46699fa8b66e311780ce292282586ddeb265d3a1c7be2` |
| `attempts/daily/mini_prose/cycle01/rival.json` | `e5e5cee8554f783571f37a17fb732cfb6f984b0b6c4b74b6680747dfa32d35e9` |
| `attempts/daily/native/cycle01/answer.json` | `cedf0ab5a38eef93f4485f10c0c27b628b79beb4d680e323c5782830ee3a70ed` |
| `manifests/fork5.json` | `f7e727daea6d3ba4353b1b2f93ae7e461a648c99877cf2ee97ca7653e30e1ee8` |
| `manifests/return6.json` | `f3ece835e680452807d9e0dd69232c34a452b67062cba75c4ba46bf87bb93951` |
| `manifests/weave7.json` | `ea8174af734dabde382a36cd85323a064ef9a8302490b9f85e1f9f360e7686df` |
| `material.json` | `8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff` |
| `plan.json` | `6992988f7c70c6af9e1df91c5bd30c676ed2bbd1f4cf23ff707489e82b6f7d55` |
| `provider/daily/bare/cycle01/answer/call-0001.request.json` | `7dd4b29a63278567c8e92e490e27b505fbacf650080266787659e4af9a070bce` |
| `provider/daily/bare/cycle01/answer/call-0001.response.json` | `6a828c8f521cc2321fec9a03c9e5864f9987254b5be0045818d979fd8f12490a` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | `c6dfca2727fd060234c9050a7122247394ef1008005448213dcc37ccc801ae37` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | `cd29bc943fea0bf5b4ca31daff34200081897bcd6663c96753102f9f7b8cae03` |
| `provider/daily/mini_fcl/cycle01/carry/call-0001.request.json` | `7399ee2364081d32a4eb5028cfad9111c749bdb6df5cd2a7c4c9837a0e90a843` |
| `provider/daily/mini_fcl/cycle01/carry/call-0001.response.json` | `df1b1f6e9b7b329325238630611246a8fac4ed947a820fe9fab19601c4335707` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.request.json` | `742bb37fe458d99476184098592d9395269be1df8655de9099198249c1ed19db` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.response.json` | `47cdabab4413b65cbad8269a741607c277fe013dd0f1567daa37e9681271cc4c` |
| `provider/daily/mini_fcl/cycle01/response/call-0001.request.json` | `cd2e1dd8dcc8f381f21bdab90b099ce6e9dbcf1e4e1ca5235637141054c197a3` |
| `provider/daily/mini_fcl/cycle01/response/call-0001.response.json` | `8498c1802b085f8a2cd01814bef56ad19e5ed5094f1868726f1ad335a94adee1` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | `f4f2cabb63e14563a114e9bd8cee0ef1bebf769c32d4b24a7abaf39176075a7a` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | `05e17982538f5dda63dba49bfcd0ab3ac6d9b765611bba35c7656e139b50b90f` |
| `provider/daily/mini_prose/cycle01/account/call-0001.request.json` | `46f95d2d1e4c8f7682bf02c6bc60d55214bc58a96698dd97fef87cabaa17b74f` |
| `provider/daily/mini_prose/cycle01/account/call-0001.response.json` | `f2cd98150e8bb6f759a3e02dbbffdf6f392be7f67c98df4d201825ac376f7a24` |
| `provider/daily/mini_prose/cycle01/carry/call-0001.request.json` | `d1b7c55f5377adeadd57a2fd1d3daf21ffa9e70326de4c55fc221d2e72c86a98` |
| `provider/daily/mini_prose/cycle01/carry/call-0001.response.json` | `d65c82cdadd591405978ec21b594346d39735ce164a2930d64be1068b3b799cc` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.request.json` | `facdacc6c70280ed6f6f85285ed3e8737a0c44887b4e3b8ae0887253e04fc3dd` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.response.json` | `b021bf6a9fedb1169e8c00edde39d28343666b5b2da69aac0a170875629d8cbd` |
| `provider/daily/mini_prose/cycle01/response/call-0001.request.json` | `2b179f12608a660cc6a010e56228ac9cb8f3b8a6aa1067962ca1bebd5ba685e2` |
| `provider/daily/mini_prose/cycle01/response/call-0001.response.json` | `9a62d5ea7cecda37b10d957f80f47bb16df966143aeb3a4602432d68d9a30052` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.request.json` | `6a3ff53bbc0aba60d11d24c4350e29753c72034c2998942c966a20297dee12b4` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.response.json` | `500aa4232eb84f2c2caa6508a0c451cc26e2a2409bacdea696e65a482532f399` |
| `provider/daily/native/cycle01/answer/call-0001.request.json` | `9e99b456aa7bdd2c419e0d0bfaabc87e5cf7a193e1832a8f5955a200d5df8a38` |
| `provider/daily/native/cycle01/answer/call-0001.response.json` | `1b876425716ac1fe9f6f3b6aaf7545224de3d7b4bfd4bc104fab2ad3e724135a` |
| `requests/daily/bare/cycle01/answer.json` | `729fe8de96360799e81c87c91366ffbfdf24638b830a02caae2ca199a92511bc` |
| `requests/daily/mini_fcl/cycle01/account.json` | `f7f794347b735fba301ab0a9b05f9770b5f8791f72325fbd8a7b9cf517b0fff8` |
| `requests/daily/mini_fcl/cycle01/carry.json` | `292363bba5121f5404c5d7e5c02f09cf42c5d407f9574c24c6133d9bfdc0252f` |
| `requests/daily/mini_fcl/cycle01/objection.json` | `eb16c0d83f9e9b053c85fe6c3417f99b5c11a504ef614666c7369ad7f7fae41a` |
| `requests/daily/mini_fcl/cycle01/response.json` | `1569f26fc79d0dca1bf48e9d04a995d027f2bab467f5d25c6f756451e0b15461` |
| `requests/daily/mini_fcl/cycle01/rival.json` | `e9c01575a7a1d3b4fce5aaa2fc291e3d10bfe6f51b562a9ecc2f0c913084c6a6` |
| `requests/daily/mini_prose/cycle01/account.json` | `1a2e2673546562c087038d075ceeebca4e1783756fcdb5ca72ad3ac6aced6be2` |
| `requests/daily/mini_prose/cycle01/carry.json` | `0fc8253fa954c192e61ff32e62d72af013eb26de5d8870b78db3dc9becc9453f` |
| `requests/daily/mini_prose/cycle01/objection.json` | `7b918c6847d9beb22d8124913fd1538774578e32e20a3ca98bd1994d580453c8` |
| `requests/daily/mini_prose/cycle01/response.json` | `a9fefb24cdfac2824053bf4aafd6759d4569c696b53775a7b44469f17fbbc31c` |
| `requests/daily/mini_prose/cycle01/rival.json` | `3a59d64bb331834523eb2e462c06f619bb774fff140f2efee1536b5ab8f5bae1` |
| `requests/daily/native/cycle01/answer.json` | `c90468349b1bc1358ccc6801fd19cd0a097bb054b6d461b0c6a60aa392397d49` |
| `responses/daily/bare/cycle01/answer.json` | `6f8b11e4877b9e848bfe7d23781de1a23299ef2c23953aa6fee42c43be54ec1a` |
| `responses/daily/bare/cycle01/answer.txt` | `47b7a7b1c86c3c0cb9341058856da9fef8994fb47688194ec951b97b76451019` |
| `responses/daily/mini_fcl/cycle01/account.json` | `c7192efbae8dcb9008dc641bbb155c95ae2231ce156efeaa15c6f7d18f1fa1b9` |
| `responses/daily/mini_fcl/cycle01/account.txt` | `57c827f00407519e040b5e5cdfbb2d90e8c93f7d5d545593a530f9ab75cdf628` |
| `responses/daily/mini_fcl/cycle01/carry.json` | `b51d520b0727c7841746725345959e4bbe64f9701751307c9f12b2d808ae1835` |
| `responses/daily/mini_fcl/cycle01/carry.txt` | `eaaa75ee9746e6dfeb90f84097be7d0e94cc0589a6fd4726bcef5b5864122c18` |
| `responses/daily/mini_fcl/cycle01/objection.json` | `0461f3a6bb321ec3dbf156249d0993fd3e9bcfbb5c28ad6455fbd0bc61feb6a2` |
| `responses/daily/mini_fcl/cycle01/objection.txt` | `8a1301958eeb9f0f6c5b37c87dede039aeb30e871e135664673fb70f3c09807f` |
| `responses/daily/mini_fcl/cycle01/response.json` | `8da3444596bdba1b4a7c275557a3b7f1372c913354a5fc1720ef370ca1d98331` |
| `responses/daily/mini_fcl/cycle01/response.txt` | `15c59e62efe88d53cc4279b47a8221f3ae2e9f50a9ad1d64f473d50e0447d004` |
| `responses/daily/mini_fcl/cycle01/rival.json` | `bbe23e7db27476bea9ce283e8d737732c383a8eb9b0362bfab718b415ab025bd` |
| `responses/daily/mini_fcl/cycle01/rival.txt` | `20c2bfa4ca68a12166dcbc71cc257b9e6f57c8d937c0bfc0c4b90565fdfe5a93` |
| `responses/daily/mini_prose/cycle01/account.json` | `c4022694009f75d098affc4ea3c35cb9f16a94ebea8ba8c8357a3a1246d5120e` |
| `responses/daily/mini_prose/cycle01/account.txt` | `06842c495dc485a08dedbeca52b1c7f46ef18558c3f4c2ac7f60c880bb684a62` |
| `responses/daily/mini_prose/cycle01/carry.json` | `aaab2c5f01102c5e3d2055ef2a0ecde8771209124b359ef6f78ae1f3db6d0499` |
| `responses/daily/mini_prose/cycle01/carry.txt` | `d70bcc4264185630765027ddaa463ebe97f3d87100e325e07f25df76d5f1513b` |
| `responses/daily/mini_prose/cycle01/objection.json` | `54e6a0f612a1bad627c6a959bd4678838ba066c2b2284e25bc508c7b6b8481a0` |
| `responses/daily/mini_prose/cycle01/objection.txt` | `bd88b2b98fb3c2b9393d2fe3323b4ee32111063bd30cbc5f82ee5304d5dbf29f` |
| `responses/daily/mini_prose/cycle01/response.json` | `00a8804395e6606d831b669f67550917946b64fb7b93992bf3d155178cd072f6` |
| `responses/daily/mini_prose/cycle01/response.txt` | `474c2d9cae612f359c4e4f1ee2d1f4a572842451acdf6e27b116ad5e6229309b` |
| `responses/daily/mini_prose/cycle01/rival.json` | `6f0c9c45b0096f5c5e1ea4923a80456891157ec7e6e37b26e49833e2712e869f` |
| `responses/daily/mini_prose/cycle01/rival.txt` | `65ec668e7bb4b82d1a8ab64974c321505d76809f64a7d4c8f3726f0eaded22d5` |
| `responses/daily/native/cycle01/answer.json` | `1ffceb5cc99327401559c8e374e262eed670ce390898b54d041039d983dcdf8e` |
| `responses/daily/native/cycle01/answer.txt` | `81d1527fe1e4f1d948bf107ca71a740e561007401dc809716c4a4288e85ee8a2` |
| `traces/daily/bare/cycle01/answer.json` | `4ff68da01ac0c9cfd4c060d4a822f7ced327003f53e9e96f1e3fb08916a7fbab` |
| `traces/daily/mini_fcl/cycle01/account.json` | `f4790106152ef33f8f02cc8f182089bd4e99beb4f553144a79e51e2ec4f92f53` |
| `traces/daily/mini_fcl/cycle01/carry.json` | `a115672341784dcfb07fb085e785a6d3414a2cdca39e4a45a83de153eeb89dc6` |
| `traces/daily/mini_fcl/cycle01/objection.json` | `050a347f8c237860fabfc3c2795b2c475084469df906b249fc86cbd2cd009205` |
| `traces/daily/mini_fcl/cycle01/response.json` | `9fe8e9120cc280bd2be3233960833630398b23e1e7c775016e64871c7b459dd8` |
| `traces/daily/mini_fcl/cycle01/rival.json` | `3abca4580072fbb6de300284f6dafd160a131ed12c9513a791249dc8bdf901c0` |
| `traces/daily/mini_prose/cycle01/account.json` | `5725e108b01c89983c73bc7e84268aa9bbf8b77d8b6fe57c79df1137bd5db455` |
| `traces/daily/mini_prose/cycle01/carry.json` | `77a34f9a5fb411589dc9ae93538174b8faf34d56745810be51262582e4062029` |
| `traces/daily/mini_prose/cycle01/objection.json` | `fe929ce1ce7a345dd800f9e6668341f2af5bb132418e3ab088b90610b95dde64` |
| `traces/daily/mini_prose/cycle01/response.json` | `9669c1bccaeac2938fa8b968d5f94a94965bae61a3a005bde40fd56051b1ed55` |
| `traces/daily/mini_prose/cycle01/rival.json` | `434a7d7add9573eb4f62b035acf82b4eefbf958fe2ab0d09cafdac08a5ffbc52` |
| `traces/daily/native/cycle01/answer.json` | `f7e80c4687cd0fe8f1ccf9e2f0771ee482e70f4e01943c83e447f33c78e8c418` |
| `waves/wave0001.json` | `8093996572d9f22dda6946b0db52fa7c8985a9b3c3e0c0976b7d9d807f9feee0` |
| `waves/wave0002.json` | `fadbae0bebdeae31bd1903093e68285cccda0752c36a710e1c78cba26ba4e22b` |
| `waves/wave0003.json` | `52f450487a06ad79cce0702055f09e2f88afa180a374f6e43056e1001dea11c8` |
| `waves/wave0004.json` | `d788e2fcdde7f957b507af1e06914d7e736edcc21e3a8fa82ac70759975764c6` |

