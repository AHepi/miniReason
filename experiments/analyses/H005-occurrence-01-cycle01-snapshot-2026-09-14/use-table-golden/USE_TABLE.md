# Use-relation table - H005 occurrence-01

**The tool records juxtapositions; the reading is root's.** This table places each authored cross-document reference beside passages a root reader may find worth starting from - a finding aid, never a closed search space - and stops there. It scores nothing, ranks nothing, classifies nothing and mints no relation of its own; it has no `att`, no `dep`, no status and no label. **A lexical overlap is not evidence of use.** FCL-1's own rule is that `depends` and `mentions` are "not automatically inferred from citation or lexical overlap"; a witness of reason use "must preserve internal role bindings, not merely the endpoint string" (FW5:628); actual use is "not automatically machine-maintainable" while prompt appearance is only a delivery fact (FW5:640); and no function of an input-output projection agrees with the accounting predicate across models differing in active route (FW5:1218), "semantic use inferred from delivery logs" included (FW5:1222) - all as summarised in the FW5-versus-harness-spec review, `fw5-vs-harness-spec-review.md` §1 R2-R4, §3.1 and §5 P1/P6. Root fills the four empty cells by reading; `unresolved` is a legal value and stays unresolved (FW5:634). An empty cell is an **unread row**, not a reading of `unresolved`.

Instrument: `use_relation_h005/1`. Schema: `h005-use-relation.use-table.v1`.

## Scope

- `daily/mini_fcl/cycle01/account`
- `daily/mini_fcl/cycle01/objection`
- `daily/mini_fcl/cycle01/rival`
- `daily/mini_fcl/cycle01/response`
- `daily/mini_fcl/cycle01/carry`

## Custody

- `plan_id`: `21e3cf1dff73423785d2e6faab5d32971cd2295cb5ce7c5ca07bbd45eb2396a6`
- `material_sha256`: `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927`

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
| refs walked | 84 |
| cross document rows | 22 |
| intra document | 62 |
| refs to exposed task artifact | 0 |
| unresolved | 0 |
| importer resolved counter | 82 |
| importer extension counter | 2 |
| importer dangling counter | 0 |

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

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[31:688]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o1","type":"objection","text":"The account's reframing of the conflict as principally an ambiguity/specification problem is under-supported. The reported pattern - later disagreement about what an agreement meant - is equally consistent with a renegotiation problem or a legitimacy problem under changed schedules, and the account downweights those alternatives after naming them in its own o1.","target":["p.objection.0#c1","p.objection.0#c2"],"bearing":"If the driver is renegotiation or legitimacy rather than ambiguity, the specification move in c2 treats a symptom, and the account's sequencing (chores first, relationship later) is misplaced."}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[31:483]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c1","type":"claim","text":"A substantial part of the recurring chore friction is ambiguity in what spoken agreements specified, not disagreement about willingness to do chores.","scope":"This household, given the described pattern of later disagreement about what an agreement meant.","grounds":"The problem statement reports agreements that were later understood differently, plus changing schedules and one person avoiding the conversations."}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c1`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[231:284]` - distinctive tokens `reports`, `statement`
  ```text
  Consider what the problem statement actually reports.
  ```
- `body[330:425]` - distinctive tokens `agreement`
  ```text
  Sometimes they agree who will do something, then later disagree about what the agreement meant.
  ```
- `body[444:494]` - distinctive tokens `avoiding`, `person`
  ```text
  One person has started avoiding the conversations.
  ```
- `body[495:611]` - distinctive tokens `agreements`
  ```text
  The account reads the recurring "later disagreement about what it meant" as evidence of ambiguity in the agreements.
  ```
- `body[612:848]` - distinctive tokens `agreement`
  ```text
  But the same observation is equally consistent with a different reading: the agreement was clear enough, and the later dispute is about whether the terms still bind given changed circumstances, or about who has standing to enforce them.
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
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[31:688]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o1","type":"objection","text":"The account's reframing of the conflict as principally an ambiguity/specification problem is under-supported. The reported pattern - later disagreement about what an agreement meant - is equally consistent with a renegotiation problem or a legitimacy problem under changed schedules, and the account downweights those alternatives after naming them in its own o1.","target":["p.objection.0#c1","p.objection.0#c2"],"bearing":"If the driver is renegotiation or legitimacy rather than ambiguity, the specification move in c2 treats a symptom, and the account's sequencing (chores first, relationship later) is misplaced."}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[484:982]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c2","type":"claim","text":"Treating each recurring chore as a small specification problem (done, by when, fallback if unable) is more likely to reduce recurrence than a general conversation about fairness or effort.","scope":"Ordinary shared-household chores.","consequence":"If two or three concrete items stop recurring after being specified more tightly, this supports c1; if they keep recurring, c1 is weakened and the problem is more likely relational or about the living arrangement."}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c2`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[0:142]` - distinctive tokens `fairness`
  ```text
  I want to press on the account's central move: reframing the conflict as a specification problem rather than a motivation or fairness problem.
  ```
- `body[285:329]` - distinctive tokens `ordinary`
  ```text
  Three flatmates argue about ordinary chores.
  ```
- `body[1144:1441]` - distinctive tokens `concrete`, `reduce`
  ```text
  That is a defensible starting point if you have to pick one, but the account's own diagnostic step - try two or three concrete items and see if recurrence falls - is weaker than it looks, because a specification move can reduce friction while the underlying driver is load imbalance or resentment.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 3 - `daily/mini_fcl/cycle01/objection#o2` --target--> `daily/mini_fcl/cycle01/account#c2`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o2` (type `objection`) |
| ref field | `target` |
| ref verbatim | `p.objection.0#c2` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c2` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[689:1272]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o2","type":"objection","text":"The account's proposed test - see whether two or three concretely specified chores stop recurring - does not distinguish the ambiguity hypothesis from the alternatives. Load imbalance or resentment can coexist with reduced friction on specified items, and recurrence may reappear as new complaint items or after the next schedule change.","target":["p.objection.0#c2"],"bearing":"Weakens the claim that falling recurrence would confirm c1 and rising recurrence would refute it; the test has lower discriminating power than the account implies."}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[484:982]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c2","type":"claim","text":"Treating each recurring chore as a small specification problem (done, by when, fallback if unable) is more likely to reduce recurrence than a general conversation about fairness or effort.","scope":"Ordinary shared-household chores.","consequence":"If two or three concrete items stop recurring after being specified more tightly, this supports c1; if they keep recurring, c1 is weakened and the problem is more likely relational or about the living arrangement."}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c2`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[0:142]` - distinctive tokens `fairness`
  ```text
  I want to press on the account's central move: reframing the conflict as a specification problem rather than a motivation or fairness problem.
  ```
- `body[285:329]` - distinctive tokens `ordinary`
  ```text
  Three flatmates argue about ordinary chores.
  ```
- `body[1144:1441]` - distinctive tokens `concrete`, `reduce`
  ```text
  That is a defensible starting point if you have to pick one, but the account's own diagnostic step - try two or three concrete items and see if recurrence falls - is weaker than it looks, because a specification move can reduce friction while the underlying driver is load imbalance or resentment.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 4 - `daily/mini_fcl/cycle01/objection#o3` --target--> `daily/mini_fcl/cycle01/account#c2`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o3` (type `objection`) |
| ref field | `target` |
| ref verbatim | `p.objection.0#c2` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c2` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[1273:1790]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o3","type":"objection","text":"The account calls the material 'thin' and then licenses a fairly specific sequence (three-column spec, separate low-pressure approach, step-5 threshold for reconsidering the living arrangement). Thin material supports tentative probes; it does not support presenting that sequence as the natural order.","target":["p.objection.0#c2","p.objection.0#c3"],"bearing":"The ordering of the account's recommendations is doing prescriptive work that the stated evidence does not carry."}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[484:982]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c2","type":"claim","text":"Treating each recurring chore as a small specification problem (done, by when, fallback if unable) is more likely to reduce recurrence than a general conversation about fairness or effort.","scope":"Ordinary shared-household chores.","consequence":"If two or three concrete items stop recurring after being specified more tightly, this supports c1; if they keep recurring, c1 is weakened and the problem is more likely relational or about the living arrangement."}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c2`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[0:142]` - distinctive tokens `fairness`
  ```text
  I want to press on the account's central move: reframing the conflict as a specification problem rather than a motivation or fairness problem.
  ```
- `body[285:329]` - distinctive tokens `ordinary`
  ```text
  Three flatmates argue about ordinary chores.
  ```
- `body[1144:1441]` - distinctive tokens `concrete`, `reduce`
  ```text
  That is a defensible starting point if you have to pick one, but the account's own diagnostic step - try two or three concrete items and see if recurrence falls - is weaker than it looks, because a specification move can reduce friction while the underlying driver is load imbalance or resentment.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 5 - `daily/mini_fcl/cycle01/objection#o3` --target--> `daily/mini_fcl/cycle01/account#c3`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o3` (type `objection`) |
| ref field | `target` |
| ref verbatim | `p.objection.0#c3` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c3` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[1273:1790]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o3","type":"objection","text":"The account calls the material 'thin' and then licenses a fairly specific sequence (three-column spec, separate low-pressure approach, step-5 threshold for reconsidering the living arrangement). Thin material supports tentative probes; it does not support presenting that sequence as the natural order.","target":["p.objection.0#c2","p.objection.0#c3"],"bearing":"The ordering of the account's recommendations is doing prescriptive work that the stated evidence does not carry."}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[983:1319]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c3","type":"claim","text":"Approaching the avoiding flatmate one-to-one with a narrower ask is more likely to re-open the conversation than another group discussion.","grounds":"Avoidance is more plausibly about the form and stakes of the conversation than about any single chore; this is a conjecture, not an established fact."}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c3`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[444:494]` - distinctive tokens `avoiding`
  ```text
  One person has started avoiding the conversations.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 6 - `daily/mini_fcl/cycle01/rival#r1` --mentions--> `daily/mini_fcl/cycle01/account` (whole contribution)

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/rival` |
| referring record | `r1` (type `claim`) |
| ref field | `mentions` |
| ref verbatim | `e3647350a300c0ed#BODY` |
| ref grain | artifact |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | none - the ref names the owning contribution, not a record |
| declared_uptake_includes_referring_record | false |
| declared_uptake_includes_target_record | n/a |

Resolver notes (from the importer, verbatim):

- `qualified_ref_body_pseudo_local`: no local record is named BODY in the owning document, so the rendered section header is admitted by convention and resolves to the owning artifact (deviation D1)

**Referring record, verbatim** (`daily/mini_fcl/cycle01/rival`, `commitments[31:313]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r1","type":"claim","text":"The selected account frames the trouble as specification ambiguity under shifting schedules and proposes tightened, written criteria as the main remedy.","scope":"Reading of the supplied body e3647350a300c0ed.","mentions":["e3647350a300c0ed#BODY"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`)

*(none: the ref names the owning contribution as a whole; the overlap subject below says what was compared)*

**Referring BODY passages** (overlap subject: the prose fields of every record of `daily/mini_fcl/cycle01/account` (the ref names the contribution, not a record); offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[63:114]` - distinctive tokens `agreements`
  ```text
  It is the question of what the agreements were for.
  ```
- `body[116:275]` - distinctive tokens `agreements`
  ```text
  The selected account treats the trouble as ambiguity in specifications: agreements lack criteria for done-ness and timing, schedules shift, so friction recurs.
  ```
- `body[276:364]` - distinctive tokens `hypothesis`
  ```text
  That is a good hypothesis as far as it goes, and I have no material that contradicts it.
  ```
- `body[489:726]` - distinctive tokens `conversation`, `person`
  ```text
  A person can stay away from a conversation not because the terms are vague but because any settled term would feel like a binding owed to people they live with, and that is a different problem from the one the selected account addresses.
  ```
- `body[1077:1225]` - distinctive tokens `person`
  ```text
  Shifting schedules are then not merely a complication; they are the fact that makes the unit-reading feel coercive to the person who is withdrawing.
  ```
- `body[1740:1802]` - distinctive tokens `differently`
  ```text
  Roughly what I would do differently from the selected account:
  ```
- `body[2093:2215]` - distinctive tokens `treat`
  ```text
  2. If the answers diverge, treat that as the actual dispute, and treat the chores as the surface where it keeps surfacing.
  ```
- `body[2359:2629]` - distinctive tokens `agreement`, `group`, `person`
  ```text
  3. Consider an arrangement that does not require agreement on meaning: individually-owned zones, or a rotation with a default outcome that nobody has to negotiate in the moment (for example, each person is responsible for a defined zone and the group does not audit it).
  ```
- `body[2925:3085]` - distinctive tokens `general`
  ```text
  What I am not claiming: that the withdrawing flatmate is the reasonable one, that written rules are coercive in general, or that the ambiguity reading is wrong.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 7 - `daily/mini_fcl/cycle01/response#k1` --target--> `daily/mini_fcl/cycle01/account#c2`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/response` |
| referring record | `k1` (type `claim`) |
| ref field | `target` |
| ref verbatim | `b5dbbb04b5acd035#c2` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c2` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[31:557]`, code point offsets into the decoded `commitments` string)

```json
{"id":"k1","type":"claim","text":"The objection is right that the account's recurrence test has low discriminating power: falling recurrence on specified items is compatible with the ambiguity reading, a renegotiation reading, and a load-imbalance reading.","scope":"The account's proposed probe.","grounds":"Reduced friction on specified items does not require that ambiguity was the driver; clearer paperwork on a lopsided arrangement is still a lopsided arrangement.","target":["b5dbbb04b5acd035#c2","bdbdf50a52b8b1fe#o2"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[484:982]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c2","type":"claim","text":"Treating each recurring chore as a small specification problem (done, by when, fallback if unable) is more likely to reduce recurrence than a general conversation about fairness or effort.","scope":"Ordinary shared-household chores.","consequence":"If two or three concrete items stop recurring after being specified more tightly, this supports c1; if they keep recurring, c1 is weakened and the problem is more likely relational or about the living arrangement."}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c2`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[247:487]` - distinctive tokens `concrete`, `fairness`, `general`
  ```text
  What I accept from the account: the recurring friction is plausibly fed by unspecified agreements under shifting schedules, and moving from "fairness in general" to two or three concrete, recurring items is a reasonable low-cost first move.
  ```
- `body[2513:2561]` - distinctive tokens `concrete`
  ```text
  1. Pick one concrete recurring chore, not three.
  ```
- `body[2562:2679]` - distinctive tokens `fallback`, `unable`
  ```text
  Do the smallest possible specification on it alone — done, by when, fallback if unable — and put it somewhere shared.
  ```
- `body[3852:4082]` - distinctive tokens `general`
  ```text
  What I am not claiming: that the withdrawing flatmate is in the right, that written arrangements are coercive in general, that the ambiguity reading is wrong, or that the unit-versus-privacy reading is established by the material.
  ```
- `body[4544:4752]` - distinctive tokens `conversation`
  ```text
  If two or three weeks of this produces no pattern on either axis, the honest move is to stop running household diagnostics and have the conversation about whether the three of you still want to live together.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 8 - `daily/mini_fcl/cycle01/response#k1` --target--> `daily/mini_fcl/cycle01/objection#o2`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/response` |
| referring record | `k1` (type `claim`) |
| ref field | `target` |
| ref verbatim | `bdbdf50a52b8b1fe#o2` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/objection` |
| resolved target record | `o2` (type `objection`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[31:557]`, code point offsets into the decoded `commitments` string)

```json
{"id":"k1","type":"claim","text":"The objection is right that the account's recurrence test has low discriminating power: falling recurrence on specified items is compatible with the ambiguity reading, a renegotiation reading, and a load-imbalance reading.","scope":"The account's proposed probe.","grounds":"Reduced friction on specified items does not require that ambiguity was the driver; clearer paperwork on a lopsided arrangement is still a lopsided arrangement.","target":["b5dbbb04b5acd035#c2","bdbdf50a52b8b1fe#o2"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[689:1272]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o2","type":"objection","text":"The account's proposed test - see whether two or three concretely specified chores stop recurring - does not distinguish the ambiguity hypothesis from the alternatives. Load imbalance or resentment can coexist with reduced friction on specified items, and recurrence may reappear as new complaint items or after the next schedule change.","target":["p.objection.0#c2"],"bearing":"Weakens the claim that falling recurrence would confirm c1 and rising recurrence would refute it; the test has lower discriminating power than the account implies."}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/objection#o2`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[621:817]` - distinctive tokens `falling`
  ```text
  Falling recurrence on specified items is compatible with ambiguity being the driver, with renegotiation under changed circumstances, and with a load imbalance that just acquired clearer paperwork.
  ```
- `body[818:908]` - distinctive tokens `power`
  ```text
  So the specification move is not a diagnosis; it is a probe with low discriminating power.
  ```
- `body[909:1149]` - distinctive tokens `alternatives`
  ```text
  The objection's own concession (o4) is also correct: if the flatmates genuinely cannot say what they agreed to, ambiguity is the plainest reading, and the alternatives are harder to establish from the material than the ambiguity reading is.
  ```
- `body[1150:1264]` - distinctive tokens `complaint`
  ```text
  The objection reduces, honestly, to a complaint about ordering and about test strength, and that complaint stands.
  ```
- `body[3647:3850]` - distinctive tokens `implies`
  ```text
  If neither, the problem is probably not chores and not specifications, and the living-arrangement question comes forward — earlier than the first account's step 5, later than the rival's framing implies.
  ```
- `body[4396:4543]` - distinctive tokens `distinguish`
  ```text
  The thing both prior accounts understate: a probe that is meant to distinguish readings has to leave room for the answer to be "none of the above."
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 9 - `daily/mini_fcl/cycle01/response#k2` --target--> `daily/mini_fcl/cycle01/rival#r7`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/response` |
| referring record | `k2` (type `claim`) |
| ref field | `target` |
| ref verbatim | `935f7779b91148f4#r7` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/rival` |
| resolved target record | `r7` (type `use`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[558:1035]`, code point offsets into the decoded `commitments` string)

```json
{"id":"k2","type":"claim","text":"The rival's distinguishing observation is the sharpest available move: watch whether the withdrawing flatmate engages with the *content* of a proposal or pulls back from the *form* of a written arrangement.","scope":"Diagnostic use of the next proposal, whatever it is.","grounds":"The two responses give different predictions about this behavior and neither prediction has been tested.","target":["935f7779b91148f4#r7","b5dbbb04b5acd035#c3"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/rival`, `commitments[1735:2157]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r7","type":"use","text":"Use reaction to the proposal itself, not only to its content, as a distinguishing observation.","action":"Notice whether the withdrawing flatmate engages with the proposed criteria or pulls back from the idea of a written arrangement.","consequence":"Content-engagement supports the ambiguity reading; pullback from the idea supports the unit-versus-privacy reading.","depends":["r2","r4"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/rival#r7`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[1613:1901]` - distinctive tokens `engages`, `proposal`, `pulls`, `written`
  ```text
  The rival's substitute observation — watch whether the withdrawing flatmate engages with the *content* of a proposal or pulls back from *the idea* of a written arrangement — is the sharpest thing on the table, because it distinguishes readings that the account's recurrence test does not.
  ```
- `body[2345:2428]` - distinctive tokens `distinguishing`
  ```text
  I would keep the rival's distinguishing observation (r7) and drop the opening move.
  ```
- `body[2707:2869]` - distinctive tokens `proposal`
  ```text
  2. Watch two things, not one: (a) does the item stop recurring, and (b) does the avoiding flatmate engage with the content or pull back from the proposal as such.
  ```
- `body[3314:3438]` - distinctive tokens `engages`
  ```text
  4. If the item stops recurring and the flatmate engages, the account's reading has some support and the sequence can extend.
  ```
- `body[3852:4082]` - distinctive tokens `written`
  ```text
  What I am not claiming: that the withdrawing flatmate is in the right, that written arrangements are coercive in general, that the ambiguity reading is wrong, or that the unit-versus-privacy reading is established by the material.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 10 - `daily/mini_fcl/cycle01/response#k2` --target--> `daily/mini_fcl/cycle01/account#c3`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/response` |
| referring record | `k2` (type `claim`) |
| ref field | `target` |
| ref verbatim | `b5dbbb04b5acd035#c3` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c3` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[558:1035]`, code point offsets into the decoded `commitments` string)

```json
{"id":"k2","type":"claim","text":"The rival's distinguishing observation is the sharpest available move: watch whether the withdrawing flatmate engages with the *content* of a proposal or pulls back from the *form* of a written arrangement.","scope":"Diagnostic use of the next proposal, whatever it is.","grounds":"The two responses give different predictions about this behavior and neither prediction has been tested.","target":["935f7779b91148f4#r7","b5dbbb04b5acd035#c3"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[983:1319]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c3","type":"claim","text":"Approaching the avoiding flatmate one-to-one with a narrower ask is more likely to re-open the conversation than another group discussion.","grounds":"Avoidance is more plausibly about the form and stakes of the conversation than about any single chore; this is a conjecture, not an established fact."}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c3`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[247:487]` - distinctive tokens `plausibly`
  ```text
  What I accept from the account: the recurring friction is plausibly fed by unspecified agreements under shifting schedules, and moving from "fairness in general" to two or three concrete, recurring items is a reasonable low-cost first move.
  ```
- `body[2016:2185]` - distinctive tokens `avoiding`
  ```text
  That is a large, loaded, identity-shaped question to put to a flatmate who is already avoiding conversations, and it invites the same withdrawal it is meant to diagnose.
  ```
- `body[2707:2869]` - distinctive tokens `avoiding`
  ```text
  2. Watch two things, not one: (a) does the item stop recurring, and (b) does the avoiding flatmate engage with the content or pull back from the proposal as such.
  ```
- `body[3003:3100]` - distinctive tokens `avoiding`
  ```text
  3. Approach the avoiding flatmate separately, but do not open with a household-ontology question.
  ```
- `body[3852:4082]` - distinctive tokens `established`
  ```text
  What I am not claiming: that the withdrawing flatmate is in the right, that written arrangements are coercive in general, that the ambiguity reading is wrong, or that the unit-versus-privacy reading is established by the material.
  ```
- `body[4544:4752]` - distinctive tokens `conversation`
  ```text
  If two or three weeks of this produces no pattern on either axis, the honest move is to stop running household diagnostics and have the conversation about whether the three of you still want to live together.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 11 - `daily/mini_fcl/cycle01/response#k3` --target--> `daily/mini_fcl/cycle01/rival#r6`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/response` |
| referring record | `k3` (type `objection`) |
| ref field | `target` |
| ref verbatim | `935f7779b91148f4#r6` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/rival` |
| resolved target record | `r6` (type `use`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[1036:1650]`, code point offsets into the decoded `commitments` string)

```json
{"id":"k3","type":"objection","text":"The rival's opening move (ask each flatmate what the flat is, as a real disagreement) is too large for a situation in which one participant is already avoiding conversations. It risks producing the withdrawal it is meant to diagnose, and the rival's own r9 names that risk without avoiding it.","scope":"The rival's r6.","bearing":"If the opening question itself triggers withdrawal, the rival's own distinguishing observation is contaminated: you cannot tell pullback-from-the-idea from pullback-from-a-heavy-question.","target":["935f7779b91148f4#r6","935f7779b91148f4#r9"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/rival`, `commitments[1283:1734]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r6","type":"use","text":"Ask the two flatmates separately what they take the flat to be, rather than starting with a shared specification document.","action":"Separate, content-permitting conversations about whether the flat carries mutual obligations or is three overlapping private lives.","consequence":"Surfaces the axis the selected account does not address, at the cost of delaying practical relief on recurring chores.","depends":["r2"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/rival#r6`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[1266:1450]` - distinctive tokens `address`, `lives`, `obligations`
  ```text
  What I accept from the rival: the frame "whose flat is this — a unit with obligations, or three lives sharing a kitchen" is the axis the first account's remedy does not address at all.
  ```
- `body[1903:2015]` - distinctive tokens `lives`, `private`
  ```text
  Where I part with the rival: r6 proposes opening with the question "is this flat a unit or three private lives."
  ```
- `body[2680:2705]` - distinctive tokens `document`
  ```text
  One item, not a document.
  ```
- `body[3003:3100]` - distinctive tokens `separately`
  ```text
  3. Approach the avoiding flatmate separately, but do not open with a household-ontology question.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 12 - `daily/mini_fcl/cycle01/response#k3` --target--> `daily/mini_fcl/cycle01/rival#r9`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/response` |
| referring record | `k3` (type `objection`) |
| ref field | `target` |
| ref verbatim | `935f7779b91148f4#r9` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/rival` |
| resolved target record | `r9` (type `objection`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[1036:1650]`, code point offsets into the decoded `commitments` string)

```json
{"id":"k3","type":"objection","text":"The rival's opening move (ask each flatmate what the flat is, as a real disagreement) is too large for a situation in which one participant is already avoiding conversations. It risks producing the withdrawal it is meant to diagnose, and the rival's own r9 names that risk without avoiding it.","scope":"The rival's r6.","bearing":"If the opening question itself triggers withdrawal, the rival's own distinguishing observation is contaminated: you cannot tell pullback-from-the-idea from pullback-from-a-heavy-question.","target":["935f7779b91148f4#r6","935f7779b91148f4#r9"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/rival`, `commitments[2523:2916]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r9","type":"objection","text":"The rival reading risks pathologizing any attempt to make expectations explicit, and can be used to shield a flatmate who simply does not want to do their share.","bearing":"Bears on r2, r3, r8, and on the selected account's remedies symmetrically: whichever reading is imposed, the remedy can be experienced by the other side as an unreasonable demand."}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/rival#r9`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[1266:1450]` - distinctive tokens `remedy`
  ```text
  What I accept from the rival: the frame "whose flat is this — a unit with obligations, or three lives sharing a kitchen" is the axis the first account's remedy does not address at all.
  ```
- `body[2186:2344]` - distinctive tokens `share`, `shield`
  ```text
  The rival's own r9 names this risk — the reading can be used to shield someone who simply does not want to do their share — but r6 steps into the risk anyway.
  ```
- `body[2870:2964]` - distinctive tokens `bears`
  ```text
  The first bears on the ambiguity reading; the second bears on the unit-versus-privacy reading.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 13 - `daily/mini_fcl/cycle01/response#k6` --target--> `daily/mini_fcl/cycle01/rival#r6`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/response` |
| referring record | `k6` (type `use`) |
| ref field | `target` |
| ref verbatim | `935f7779b91148f4#r6` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/rival` |
| resolved target record | `r6` (type `use`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[2635:3153]`, code point offsets into the decoded `commitments` string)

```json
{"id":"k6","type":"use","text":"When approaching the avoiding flatmate separately, do not open with a household-ontology question. Open with the observation that the problem is being misframed, and let them name the axis if there is one.","action":"Separate conversation framed as 'I've been treating this wrong', not as 'what kind of flat is this'.","consequence":"Lower risk of triggering the same withdrawal; higher chance the actual axis surfaces in their words rather than ours.","target":["935f7779b91148f4#r6"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/rival`, `commitments[1283:1734]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r6","type":"use","text":"Ask the two flatmates separately what they take the flat to be, rather than starting with a shared specification document.","action":"Separate, content-permitting conversations about whether the flat carries mutual obligations or is three overlapping private lives.","consequence":"Surfaces the axis the selected account does not address, at the cost of delaying practical relief on recurring chores.","depends":["r2"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/rival#r6`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[1266:1450]` - distinctive tokens `address`, `lives`, `obligations`
  ```text
  What I accept from the rival: the frame "whose flat is this — a unit with obligations, or three lives sharing a kitchen" is the axis the first account's remedy does not address at all.
  ```
- `body[1903:2015]` - distinctive tokens `lives`, `private`
  ```text
  Where I part with the rival: r6 proposes opening with the question "is this flat a unit or three private lives."
  ```
- `body[2680:2705]` - distinctive tokens `document`
  ```text
  One item, not a document.
  ```
- `body[3003:3100]` - distinctive tokens `separately`
  ```text
  3. Approach the avoiding flatmate separately, but do not open with a household-ontology question.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 14 - `daily/mini_fcl/cycle01/response#k7` --target--> `daily/mini_fcl/cycle01/rival#r9`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/response` |
| referring record | `k7` (type `objection`) |
| ref field | `target` |
| ref verbatim | `935f7779b91148f4#r9` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/rival` |
| resolved target record | `r9` (type `objection`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[3154:3669]`, code point offsets into the decoded `commitments` string)

```json
{"id":"k7","type":"objection","text":"My own two-track test inherits a version of the objection I am endorsing against the account: pullback-from-form is consistent both with the unit-versus-privacy reading and with simple avoidance of any obligation. The rival's r9 admits this and my k2 does not fully solve it.","bearing":"If pullback-from-form cannot distinguish those, the test is weaker than k2 suggests, and the honest state is that neither reading is being confirmed.","target":["k2","935f7779b91148f4#r9"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/rival`, `commitments[2523:2916]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r9","type":"objection","text":"The rival reading risks pathologizing any attempt to make expectations explicit, and can be used to shield a flatmate who simply does not want to do their share.","bearing":"Bears on r2, r3, r8, and on the selected account's remedies symmetrically: whichever reading is imposed, the remedy can be experienced by the other side as an unreasonable demand."}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/rival#r9`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[1266:1450]` - distinctive tokens `remedy`
  ```text
  What I accept from the rival: the frame "whose flat is this — a unit with obligations, or three lives sharing a kitchen" is the axis the first account's remedy does not address at all.
  ```
- `body[2186:2344]` - distinctive tokens `share`, `shield`
  ```text
  The rival's own r9 names this risk — the reading can be used to shield someone who simply does not want to do their share — but r6 steps into the risk anyway.
  ```
- `body[2870:2964]` - distinctive tokens `bears`
  ```text
  The first bears on the ambiguity reading; the second bears on the unit-versus-privacy reading.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 15 - `daily/mini_fcl/cycle01/carry#n1` --target--> `daily/mini_fcl/cycle01/response#k5`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `n1` (type `claim`) |
| ref field | `target` |
| ref verbatim | `b998d514348ed94e#k5` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/response` |
| resolved target record | `k5` (type `use`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[31:708]`, code point offsets into the decoded `commitments` string)

```json
{"id":"n1","type":"claim","text":"The carry's two-track probe has one track (does the item stop recurring) weak against three rival readings and one track (content vs. form) weak against at least two, and no refinement available from the current evidence closes both gaps. This is a limit of the material, not a design flaw to be fixed by a cleverer probe.","scope":"The carry's k5/k7 as stated.","grounds":"Recurrence reduction is compatible with ambiguity, renegotiation, and load imbalance (carry k1); pullback-from-form is compatible with unit-versus-privacy and with plain obligation-avoidance (carry k7, rival r9).","target":["b998d514348ed94e#k5","b998d514348ed94e#k7"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[2061:2634]`, code point offsets into the decoded `commitments` string)

```json
{"id":"k5","type":"use","text":"Run a two-track observation on one chore item before sequencing the prior accounts' remedies: does it stop recurring, and does the avoiding flatmate engage with content or pull back from form.","action":"Specify one recurring item only; record both observations across a short window.","consequence":"Content-engagement plus reduced recurrence supports the ambiguity reading; pullback-from-form alongside reduced recurrence supports the unit-versus-privacy axis; neither suggests the chore frame itself is wrong.","depends":["k1","k2","k4"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/response#k5`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[1005:1149]` - distinctive tokens `track`
  ```text
  So the proposed two-track observation has one track (recurrence falls) that is weak against three rival readings and a second track (content vs.
  ```
- `body[2601:2839]` - distinctive tokens `track`, `wrong`
  ```text
  If the one-item probe produces nothing on either track in two or three weeks, the honest reading is not 'the probe was badly designed' and not 'the ambiguity reading was wrong' — it is that the chore frame is not where the friction lives.
  ```
- `body[2982:3280]` - distinctive tokens `track`
  ```text
  So my contribution is: keep the carry's records as they stand, add the explicit concession that track (b) is weaker than the carry's k2 implies and weaker than the carry's k7 fully states, and add the constraint that no further refinement of the probe is available from the evidence in front of us.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 16 - `daily/mini_fcl/cycle01/carry#n1` --target--> `daily/mini_fcl/cycle01/response#k7`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `n1` (type `claim`) |
| ref field | `target` |
| ref verbatim | `b998d514348ed94e#k7` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/response` |
| resolved target record | `k7` (type `objection`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[31:708]`, code point offsets into the decoded `commitments` string)

```json
{"id":"n1","type":"claim","text":"The carry's two-track probe has one track (does the item stop recurring) weak against three rival readings and one track (content vs. form) weak against at least two, and no refinement available from the current evidence closes both gaps. This is a limit of the material, not a design flaw to be fixed by a cleverer probe.","scope":"The carry's k5/k7 as stated.","grounds":"Recurrence reduction is compatible with ambiguity, renegotiation, and load imbalance (carry k1); pullback-from-form is compatible with unit-versus-privacy and with plain obligation-avoidance (carry k7, rival r9).","target":["b998d514348ed94e#k5","b998d514348ed94e#k7"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[3154:3669]`, code point offsets into the decoded `commitments` string)

```json
{"id":"k7","type":"objection","text":"My own two-track test inherits a version of the objection I am endorsing against the account: pullback-from-form is consistent both with the unit-versus-privacy reading and with simple avoidance of any obligation. The rival's r9 admits this and my k2 does not fully solve it.","bearing":"If pullback-from-form cannot distinguish those, the test is weaker than k2 suggests, and the honest state is that neither reading is being confirmed.","target":["k2","935f7779b91148f4#r9"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/response#k7`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[0:93]` - distinctive tokens `honest`
  ```text
  This is a carry, and I want to be honest about what carrying at this point can and cannot do.
  ```
- `body[570:690]` - distinctive tokens `fully`, `solve`
  ```text
  What I can add is the one thing the carry's own k7 says it does not fully solve, plus a note on the source I was handed.
  ```
- `body[718:945]` - distinctive tokens `admits`, `consistent`
  ```text
  The carry says pullback-from-form supports the unit-versus-privacy reading, and then k7 admits pullback-from-form is *also* consistent with plain avoidance of any obligation — someone who simply does not want to be on the hook.
  ```
- `body[1005:1149]` - distinctive tokens `track`
  ```text
  So the proposed two-track observation has one track (recurrence falls) that is weak against three rival readings and a second track (content vs.
  ```
- `body[1511:1869]` - distinctive tokens `simple`
  ```text
  Rather than invent a cleverer test, I would state the limit plainly: run the one-item probe, watch the two tracks, and treat a pullback-from-form outcome as *raising* the unit-versus-privacy reading without confirming it, while noting that the same outcome is compatible with simple obligation-avoidance and with load resentment that has not yet been voiced.
  ```
- `body[1871:2068]` - distinctive tokens `version`
  ```text
  On the material I was handed: p.carry.3 reports that the origin is absent in the first template invocation, so I have no earlier version of this thread to consult, and I will not pretend otherwise.
  ```
- `body[2601:2839]` - distinctive tokens `honest`, `track`
  ```text
  If the one-item probe produces nothing on either track in two or three weeks, the honest reading is not 'the probe was badly designed' and not 'the ambiguity reading was wrong' — it is that the chore frame is not where the friction lives.
  ```
- `body[2982:3280]` - distinctive tokens `fully`, `track`, `weaker`
  ```text
  So my contribution is: keep the carry's records as they stand, add the explicit concession that track (b) is weaker than the carry's k2 implies and weaker than the carry's k7 fully states, and add the constraint that no further refinement of the probe is available from the evidence in front of us.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 17 - `daily/mini_fcl/cycle01/carry#n3` --target--> `daily/mini_fcl/cycle01/response#k2`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `n3` (type `objection`) |
| ref field | `target` |
| ref verbatim | `b998d514348ed94e#k2` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/response` |
| resolved target record | `k2` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[1263:1859]`, code point offsets into the decoded `commitments` string)

```json
{"id":"n3","type":"objection","text":"The carry's k2 asserts the discriminating value of watching content vs. form, but k7 already concedes that outcome does not separate unit-versus-privacy from obligation-avoidance. Stating k2 at that strength while keeping k7 in the record presents the track as sharper than the carry's own concession allows.","scope":"The carry's own record set.","bearing":"If a reader takes k2 at face value and does not read k7 as limiting it, the probe will be over-read as a test of the unit-versus-privacy axis.","target":["b998d514348ed94e#k2","b998d514348ed94e#k7"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[558:1035]`, code point offsets into the decoded `commitments` string)

```json
{"id":"k2","type":"claim","text":"The rival's distinguishing observation is the sharpest available move: watch whether the withdrawing flatmate engages with the *content* of a proposal or pulls back from the *form* of a written arrangement.","scope":"Diagnostic use of the next proposal, whatever it is.","grounds":"The two responses give different predictions about this behavior and neither prediction has been tested.","target":["935f7779b91148f4#r7","b5dbbb04b5acd035#c3"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/response#k2`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[1511:1869]` - distinctive tokens `watch`
  ```text
  Rather than invent a cleverer test, I would state the limit plainly: run the one-item probe, watch the two tracks, and treat a pullback-from-form outcome as *raising* the unit-versus-privacy reading without confirming it, while noting that the same outcome is compatible with simple obligation-avoidance and with load resentment that has not yet been voiced.
  ```
- `body[2069:2120]` - distinctive tokens `whatever`
  ```text
  Whatever the origin said, it is not in front of me.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 18 - `daily/mini_fcl/cycle01/carry#n3` --target--> `daily/mini_fcl/cycle01/response#k7`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `n3` (type `objection`) |
| ref field | `target` |
| ref verbatim | `b998d514348ed94e#k7` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/response` |
| resolved target record | `k7` (type `objection`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[1263:1859]`, code point offsets into the decoded `commitments` string)

```json
{"id":"n3","type":"objection","text":"The carry's k2 asserts the discriminating value of watching content vs. form, but k7 already concedes that outcome does not separate unit-versus-privacy from obligation-avoidance. Stating k2 at that strength while keeping k7 in the record presents the track as sharper than the carry's own concession allows.","scope":"The carry's own record set.","bearing":"If a reader takes k2 at face value and does not read k7 as limiting it, the probe will be over-read as a test of the unit-versus-privacy axis.","target":["b998d514348ed94e#k2","b998d514348ed94e#k7"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[3154:3669]`, code point offsets into the decoded `commitments` string)

```json
{"id":"k7","type":"objection","text":"My own two-track test inherits a version of the objection I am endorsing against the account: pullback-from-form is consistent both with the unit-versus-privacy reading and with simple avoidance of any obligation. The rival's r9 admits this and my k2 does not fully solve it.","bearing":"If pullback-from-form cannot distinguish those, the test is weaker than k2 suggests, and the honest state is that neither reading is being confirmed.","target":["k2","935f7779b91148f4#r9"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/response#k7`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[0:93]` - distinctive tokens `honest`
  ```text
  This is a carry, and I want to be honest about what carrying at this point can and cannot do.
  ```
- `body[570:690]` - distinctive tokens `fully`, `solve`
  ```text
  What I can add is the one thing the carry's own k7 says it does not fully solve, plus a note on the source I was handed.
  ```
- `body[718:945]` - distinctive tokens `admits`, `consistent`
  ```text
  The carry says pullback-from-form supports the unit-versus-privacy reading, and then k7 admits pullback-from-form is *also* consistent with plain avoidance of any obligation — someone who simply does not want to be on the hook.
  ```
- `body[1005:1149]` - distinctive tokens `track`
  ```text
  So the proposed two-track observation has one track (recurrence falls) that is weak against three rival readings and a second track (content vs.
  ```
- `body[1511:1869]` - distinctive tokens `simple`
  ```text
  Rather than invent a cleverer test, I would state the limit plainly: run the one-item probe, watch the two tracks, and treat a pullback-from-form outcome as *raising* the unit-versus-privacy reading without confirming it, while noting that the same outcome is compatible with simple obligation-avoidance and with load resentment that has not yet been voiced.
  ```
- `body[1871:2068]` - distinctive tokens `version`
  ```text
  On the material I was handed: p.carry.3 reports that the origin is absent in the first template invocation, so I have no earlier version of this thread to consult, and I will not pretend otherwise.
  ```
- `body[2601:2839]` - distinctive tokens `honest`, `track`
  ```text
  If the one-item probe produces nothing on either track in two or three weeks, the honest reading is not 'the probe was badly designed' and not 'the ambiguity reading was wrong' — it is that the chore frame is not where the friction lives.
  ```
- `body[2982:3280]` - distinctive tokens `fully`, `track`, `weaker`
  ```text
  So my contribution is: keep the carry's records as they stand, add the explicit concession that track (b) is weaker than the carry's k2 implies and weaker than the carry's k7 fully states, and add the constraint that no further refinement of the probe is available from the evidence in front of us.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 19 - `daily/mini_fcl/cycle01/carry#n4` --target--> `daily/mini_fcl/cycle01/response#k5`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `n4` (type `use`) |
| ref field | `target` |
| ref verbatim | `b998d514348ed94e#k5` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/response` |
| resolved target record | `k5` (type `use`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[1860:2422]`, code point offsets into the decoded `commitments` string)

```json
{"id":"n4","type":"use","text":"Treat a pullback-from-form outcome as *raising* the unit-versus-privacy reading, not as confirming it, and record the same outcome as also compatible with obligation-avoidance and with unvoiced load resentment.","action":"When reporting the probe's outcome, state the confirmatory ceiling explicitly rather than letting the outcome carry more weight than it can.","consequence":"Prevents the probe from being read as having settled the axis it was only meant to gesture at.","depends":["n1","n3"],"target":["b998d514348ed94e#k5"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[2061:2634]`, code point offsets into the decoded `commitments` string)

```json
{"id":"k5","type":"use","text":"Run a two-track observation on one chore item before sequencing the prior accounts' remedies: does it stop recurring, and does the avoiding flatmate engage with content or pull back from form.","action":"Specify one recurring item only; record both observations across a short window.","consequence":"Content-engagement plus reduced recurrence supports the ambiguity reading; pullback-from-form alongside reduced recurrence supports the unit-versus-privacy axis; neither suggests the chore frame itself is wrong.","depends":["k1","k2","k4"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/response#k5`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[1005:1149]` - distinctive tokens `track`
  ```text
  So the proposed two-track observation has one track (recurrence falls) that is weak against three rival readings and a second track (content vs.
  ```
- `body[2601:2839]` - distinctive tokens `track`, `wrong`
  ```text
  If the one-item probe produces nothing on either track in two or three weeks, the honest reading is not 'the probe was badly designed' and not 'the ambiguity reading was wrong' — it is that the chore frame is not where the friction lives.
  ```
- `body[2982:3280]` - distinctive tokens `track`
  ```text
  So my contribution is: keep the carry's records as they stand, add the explicit concession that track (b) is weaker than the carry's k2 implies and weaker than the carry's k7 fully states, and add the constraint that no further refinement of the probe is available from the evidence in front of us.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 20 - `daily/mini_fcl/cycle01/carry#n5` --target--> `daily/mini_fcl/cycle01/response#k9`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `n5` (type `claim`) |
| ref field | `target` |
| ref verbatim | `b998d514348ed94e#k9` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/response` |
| resolved target record | `k9` (type `problem`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[2423:2915]`, code point offsets into the decoded `commitments` string)

```json
{"id":"n5","type":"claim","text":"No further refinement of the probe is available from the material in front of me. Adding a third observation track would be invention, not inference.","scope":"My contribution to this carry.","grounds":"The carry's k9 lists the missing facts (what the chores are, how long this has run, whether the withdrawing flatmate has stated a reason, whether the other two agree) and none of them are supplied by p.carry.0–p.carry.2.","target":["b998d514348ed94e#k9"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[4189:4539]`, code point offsets into the decoded `commitments` string)

```json
{"id":"k9","type":"problem","text":"The material still does not say what the recurring chores are, how long the pattern has run, whether the withdrawing flatmate has stated a reason, or whether the two remaining flatmates agree with each other. Any probe design has to accept that its first outcome may be uninformative.","mentions":["k5","k6","k8"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/response#k9`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[506:569]` - distinctive tokens `reason`
  ```text
  That is a defensible position and I see no reason to revise it.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 21 - `daily/mini_fcl/cycle01/carry#n6` --mentions--> `daily/mini_fcl/cycle01/response` (whole contribution)

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `n6` (type `problem`) |
| ref field | `mentions` |
| ref verbatim | `b998d514348ed94e` |
| ref grain | artifact |
| resolved target coordinate | `daily/mini_fcl/cycle01/response` |
| resolved target record | none - the ref names the owning contribution, not a record |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | n/a |

Resolver notes (from the importer, verbatim):

- `bare_label_ref`: bare exposed-artifact label with no '#LocalName'; local resolution was tried first, so it resolves to the owning artifact (deviation D2)

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[2916:3297]`, code point offsets into the decoded `commitments` string)

```json
{"id":"n6","type":"problem","text":"The origin (p.carry.3) reports itself absent in the first template invocation, so the relation of the carry's records to any earlier version is not assessable from what I have. Whether the carry revises, retains, or contradicts an origin I cannot see is unknown to me and I will not assert one way or the other.","mentions":["b998d514348ed94e"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/response`)

*(none: the ref names the owning contribution as a whole; the overlap subject below says what was compared)*

**Referring BODY passages** (overlap subject: the prose fields of every record of `daily/mini_fcl/cycle01/response` (the ref names the contribution, not a record); offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[0:93]` - distinctive tokens `honest`
  ```text
  This is a carry, and I want to be honest about what carrying at this point can and cannot do.
  ```
- `body[94:505]` - distinctive tokens `diagnostics`, `opening`, `question`, `signal`
  ```text
  The previous invocation already did the discriminating work: it kept the objection's ordering correction (specification is a probe, not a diagnosis), kept the rival's axis (the withdrawing flatmate may be pulling back from the *form* of an arrangement rather than from any chore), dropped the rival's loaded opening question, and bound itself to stopping household diagnostics if neither axis produces a signal.
  ```
- `body[506:569]` - distinctive tokens `reason`
  ```text
  That is a defensible position and I see no reason to revise it.
  ```
- `body[570:690]` - distinctive tokens `fully`, `solve`
  ```text
  What I can add is the one thing the carry's own k7 says it does not fully solve, plus a note on the source I was handed.
  ```
- `body[718:945]` - distinctive tokens `admits`, `consistent`
  ```text
  The carry says pullback-from-form supports the unit-versus-privacy reading, and then k7 admits pullback-from-form is *also* consistent with plain avoidance of any obligation — someone who simply does not want to be on the hook.
  ```
- `body[946:1004]` - distinctive tokens `names`
  ```text
  The rival's r9 names the same problem from the other side.
  ```
- `body[1005:1149]` - distinctive tokens `track`
  ```text
  So the proposed two-track observation has one track (recurrence falls) that is weak against three rival readings and a second track (content vs.
  ```
- `body[1511:1869]` - distinctive tokens `simple`, `watch`
  ```text
  Rather than invent a cleverer test, I would state the limit plainly: run the one-item probe, watch the two tracks, and treat a pullback-from-form outcome as *raising* the unit-versus-privacy reading without confirming it, while noting that the same outcome is compatible with simple obligation-avoidance and with load resentment that has not yet been voiced.
  ```
- `body[1871:2068]` - distinctive tokens `version`
  ```text
  On the material I was handed: p.carry.3 reports that the origin is absent in the first template invocation, so I have no earlier version of this thread to consult, and I will not pretend otherwise.
  ```
- `body[2069:2120]` - distinctive tokens `whatever`
  ```text
  Whatever the origin said, it is not in front of me.
  ```
- `body[2306:2600]` - distinctive tokens `changed`, `conversation`, `ontology`, `question`, `right`
  ```text
  The other thing worth saying: nothing in the prior material has changed my judgment that the carry's k6 (do not open the separate conversation with a household-ontology question) is right, and that k8 (if neither axis moves, name the living-arrangement question) is the load-bearing commitment.
  ```
- `body[2601:2839]` - distinctive tokens `honest`, `track`, `wrong`
  ```text
  If the one-item probe produces nothing on either track in two or three weeks, the honest reading is not 'the probe was badly designed' and not 'the ambiguity reading was wrong' — it is that the chore frame is not where the friction lives.
  ```
- `body[2840:2980]` - distinctive tokens `sequence`
  ```text
  That is the outcome the whole sequence is built to be able to reach, and reaching it should be treated as success of the probe, not failure.
  ```
- `body[2982:3280]` - distinctive tokens `fully`, `track`, `weaker`
  ```text
  So my contribution is: keep the carry's records as they stand, add the explicit concession that track (b) is weaker than the carry's k2 implies and weaker than the carry's k7 fully states, and add the constraint that no further refinement of the probe is available from the evidence in front of us.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 22 - `daily/mini_fcl/cycle01/carry#n7` --target--> `daily/mini_fcl/cycle01/response#k8`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/carry` |
| referring record | `n7` (type `use`) |
| ref field | `target` |
| ref verbatim | `b998d514348ed94e#k8` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/response` |
| resolved target record | `k8` (type `commitment`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/carry`, `commitments[3298:3847]`, code point offsets into the decoded `commitments` string)

```json
{"id":"n7","type":"use","text":"Keep the carry's records as they stand and add n1, n3, n4, n5 alongside them, rather than revising the carry's k2 or k5. The carry's commitments remain the operative surface; my additions narrow their claims rather than replace them.","action":"Carry the prior record set forward with the confirmatory-ceiling constraint attached.","consequence":"Preserves the sequencing and the stopping condition (k8) without strengthening claims the carry already weakened.","depends":["n1","n3"],"target":["b998d514348ed94e#k8"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/response`, `commitments[3670:4188]`, code point offsets into the decoded `commitments` string)

```json
{"id":"k8","type":"commitment","text":"If no pattern emerges on either axis within a short window, stop running household diagnostics and name the living-arrangement question directly.","scope":"Contingent on k5 producing no discriminating signal.","action":"Shift the conversation from chores and specifications to whether the three flatmates still want to share the flat.","consequence":"Prevents an indefinite sequence of probes from becoming an avoidance of the larger decision by another route.","depends":["k5"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/response#k8`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[94:505]` - distinctive tokens `diagnostics`, `question`, `signal`
  ```text
  The previous invocation already did the discriminating work: it kept the objection's ordering correction (specification is a probe, not a diagnosis), kept the rival's axis (the withdrawing flatmate may be pulling back from the *form* of an arrangement rather than from any chore), dropped the rival's loaded opening question, and bound itself to stopping household diagnostics if neither axis produces a signal.
  ```
- `body[2306:2600]` - distinctive tokens `conversation`, `question`
  ```text
  The other thing worth saying: nothing in the prior material has changed my judgment that the carry's k6 (do not open the separate conversation with a household-ontology question) is right, and that k8 (if neither axis moves, name the living-arrangement question) is the load-bearing commitment.
  ```
- `body[2840:2980]` - distinctive tokens `sequence`
  ```text
  That is the outcome the whole sequence is built to be able to reach, and reaching it should be treated as success of the probe, not failure.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

## Declared uptake versus records present

### `daily/mini_fcl/cycle01/account`

- commitment surface: `read_fcl1`
- records present (6): `c1`, `c2`, `c3`, `o1`, `u1`, `p1`
- declared `uptake` (5): `c1`, `c2`, `c3`, `o1`, `u1`
- records in uptake (5): `c1`, `c2`, `c3`, `o1`, `u1`
- records omitted from uptake (1): `p1`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/objection`

- commitment surface: `read_fcl1`
- records present (8): `o1`, `o2`, `o3`, `c1`, `c2`, `o4`, `p1`, `u1`
- declared `uptake` (6): `o1`, `o2`, `o3`, `c1`, `c2`, `u1`
- records in uptake (6): `o1`, `o2`, `o3`, `c1`, `c2`, `u1`
- records omitted from uptake (2): `o4`, `p1`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/rival`

- commitment surface: `read_fcl1`
- records present (11): `r1`, `r2`, `r3`, `r4`, `r5`, `r6`, `r7`, `r8`, `r9`, `r10`, `r11`
- declared `uptake` (4): `r2`, `r6`, `r7`, `r9`
- records in uptake (4): `r2`, `r6`, `r7`, `r9`
- records omitted from uptake (7): `r1`, `r3`, `r4`, `r5`, `r8`, `r10`, `r11`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/response`

- commitment surface: `read_fcl1`
- records present (9): `k1`, `k2`, `k3`, `k4`, `k5`, `k6`, `k7`, `k8`, `k9`
- declared `uptake` (9): `k1`, `k2`, `k3`, `k4`, `k5`, `k6`, `k7`, `k8`, `k9`
- records in uptake (9): `k1`, `k2`, `k3`, `k4`, `k5`, `k6`, `k7`, `k8`, `k9`
- records omitted from uptake (0): *none*
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/carry`

- commitment surface: `read_fcl1`
- records present (8): `n1`, `n2`, `n3`, `n4`, `n5`, `n6`, `n7`, `n8`
- declared `uptake` (8): `n1`, `n2`, `n3`, `n4`, `n5`, `n6`, `n7`, `n8`
- records in uptake (8): `n1`, `n2`, `n3`, `n4`, `n5`, `n6`, `n7`, `n8`
- records omitted from uptake (0): *none*
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
| `artifacts/daily/mini_fcl/cycle01/account.json` | `b8de6a8d579c358cade3296a7e8260a03c6e80269cd0486aae43c134999732e6` |
| `artifacts/daily/mini_fcl/cycle01/carry.json` | `cfd3844e4207455171e31093b1f0c57ca0ca11ce1e456d0639b34d62a3401e79` |
| `artifacts/daily/mini_fcl/cycle01/objection.json` | `810913b5c31f94a4d697da0e90e74205ac6b7abc7b217d44188852f2562110db` |
| `artifacts/daily/mini_fcl/cycle01/response.json` | `a1d4f48d5246608ade51b63604beafc82de9770465d2a7fd7c2340ee8a4e55d3` |
| `artifacts/daily/mini_fcl/cycle01/rival.json` | `b0b15d8d44c7dcd706879a9ced41e3f26a592ec5a25c2a961e01e32ea748e8cd` |
| `attempts/daily/mini_fcl/cycle01/account.json` | `d0a342e45e8a6228fb3e0b8e609616e9f125eb3505733cb6c759de9c2135896c` |
| `attempts/daily/mini_fcl/cycle01/carry.json` | `72a7636ecfd253f6d18203a412810dcde9601b477361747451c69ff520f94bf8` |
| `attempts/daily/mini_fcl/cycle01/objection.json` | `0c3e58de82892d77ea57d59f649ba3b59edb03832278a730258904d086a52c1f` |
| `attempts/daily/mini_fcl/cycle01/response.json` | `7a4279d6bfdcf5960ca9de1544fc9f5dab41fe64ff886abe47b2c366ae915022` |
| `attempts/daily/mini_fcl/cycle01/rival.json` | `5290ea81ad554cd3cab774c1256a87e8e7fcb94475c2c8015a1c1b4d998bed3e` |
| `manifests/fork5.json` | `f7e727daea6d3ba4353b1b2f93ae7e461a648c99877cf2ee97ca7653e30e1ee8` |
| `manifests/return6.json` | `f3ece835e680452807d9e0dd69232c34a452b67062cba75c4ba46bf87bb93951` |
| `manifests/weave7.json` | `ea8174af734dabde382a36cd85323a064ef9a8302490b9f85e1f9f360e7686df` |
| `material.json` | `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927` |
| `plan.json` | `99cda29f3c6788d564448f7587c7448a6542d30a9bd5e48dc219925e2cc464c3` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | `789df5c749c0bc555582c72a5cb71b1ed1aae72b9c7ff34cce6aca5a9a7a51d9` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | `5fdc449bb02388d6eb89a00e1ea27c6372a075fd6c421aa6f102e69d37cacb17` |
| `provider/daily/mini_fcl/cycle01/carry/call-0001.request.json` | `e599ddd817fd80c0b0035cc8fa8ad8cc85e318707217e52bd9607ff97b13e0c0` |
| `provider/daily/mini_fcl/cycle01/carry/call-0001.response.json` | `6cc961726d6780f7b186a7ca6e38c314bd3c77a4be54bb860a2e3449e2c92899` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.request.json` | `dc6f354fea4a0039fe89a85b21556ae19436dc1e097ec3192ed9950de720f363` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.response.json` | `3154df0185e8ca502bcb627dd8a9e9f8d8997f61fc3f08e31916488b7f570b8b` |
| `provider/daily/mini_fcl/cycle01/response/call-0001.request.json` | `afc14692393bb8d4e11ae864c9de50a2c8b0d0a0579b73cb2b553e65d9fa50d1` |
| `provider/daily/mini_fcl/cycle01/response/call-0001.response.json` | `1235667af246002b3017288aad37a721283ee869dff842146fc1ff4501fdf68b` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | `7a71b713c61ddc6d63f02ef525e1f9fac56591d042c75d338357dc348709e0a8` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | `69bb769803e7bdd8bc9131016f54e4f519a9e88e0535137af85316da61e2c6ea` |
| `requests/daily/mini_fcl/cycle01/account.json` | `55be2b61dce40bd2db18c5b811b436b08b3c32fca1e4ad27ca102a48efb66c71` |
| `requests/daily/mini_fcl/cycle01/carry.json` | `0360de2a09a9a886305108a5b26cbb97eca88874740338be7b884a15fce172bd` |
| `requests/daily/mini_fcl/cycle01/objection.json` | `b5762304ecf9d4ebe1901fdfac19efe855966b42a260c7e4afd1b5f431095643` |
| `requests/daily/mini_fcl/cycle01/response.json` | `7d4fefab8d566c1e36222d3e52f5568b6ae6f223689163a8938632ba2238b614` |
| `requests/daily/mini_fcl/cycle01/rival.json` | `c9ab8dee599c0ec8a5febeeaf163eed08bfa2edaaf2e2c2b6f26a2b9d50b975e` |
| `responses/daily/mini_fcl/cycle01/account.json` | `633d9dc348b7275ab09b366750de9c34ce31965039411815b99f0a379e4426ed` |
| `responses/daily/mini_fcl/cycle01/account.txt` | `539a93fabf07fed8eae75caa5751403b9c7e2dfaadf7c5735d816fcd24f7611d` |
| `responses/daily/mini_fcl/cycle01/carry.json` | `d62c73656cffdd5d3e98efd36c90e7cc98ead2ceb4030e2270fd545cac8cd1f6` |
| `responses/daily/mini_fcl/cycle01/carry.txt` | `526c499457e517b76921fa606632dd2f0b27842ed5b479e67361714934eb8223` |
| `responses/daily/mini_fcl/cycle01/objection.json` | `c75d97346a0215e7b9683be563411cf2dd5fe038ce5cb8408858de7dcc7930f8` |
| `responses/daily/mini_fcl/cycle01/objection.txt` | `f7f80a13c9d319cbb366a33029a4d9e24fecfa221e9e31b13fde00c751acbca1` |
| `responses/daily/mini_fcl/cycle01/response.json` | `cb2bf55bcb9ac54a2caec8075bf9c4698543224455e87474d48f2add55d8334f` |
| `responses/daily/mini_fcl/cycle01/response.txt` | `fc915cff6f13c290a0b438e866b04fe1557d3f55c62e0e5871e90604daaf1e8e` |
| `responses/daily/mini_fcl/cycle01/rival.json` | `75c0350fcda1efd071ed8e1053443ccf09067d3af4c0a75e607805e53fb95f47` |
| `responses/daily/mini_fcl/cycle01/rival.txt` | `f3353d2ca683ef0f88109f18a6e458fa1507727b790abd4b20dd7564e17ff3a1` |
| `traces/daily/mini_fcl/cycle01/account.json` | `f4790106152ef33f8f02cc8f182089bd4e99beb4f553144a79e51e2ec4f92f53` |
| `traces/daily/mini_fcl/cycle01/carry.json` | `280e043d65157175dee6a9e5a5d6455da319eb39c1da39e660fa95cd9b3d940b` |
| `traces/daily/mini_fcl/cycle01/objection.json` | `68f54165906e979ac09f52c63befd0d128d5ed5271518d96ad0b15e697da5391` |
| `traces/daily/mini_fcl/cycle01/response.json` | `4b93806957ee28362fa075b7eee6f385e2737749db020809b801933172501647` |
| `traces/daily/mini_fcl/cycle01/rival.json` | `2e39e17fc98c35c11e2f1d0994e57dcb582f6e8d1c9cee273edfab5d14f95062` |
| `waves/wave0001.json` | `f1ec44d49306ae28903c1875aefc4e4a7b210c8d26d70210438cb5537e1a8faa` |
| `waves/wave0002.json` | `47bfddaaeb4fa9557bad1eec815023a0392f41d67e03e2e4ad3acc4c7aad5522` |
| `waves/wave0003.json` | `cc46ad22810292820d616c9a8d8140e7a212ba72292eaf510b6a50a5fac7a35b` |
| `waves/wave0004.json` | `dbe8dac6e378dbbaf78f153cea905526a83a9520727f4efbcecdd3fb8a5627b3` |
| `waves/wave0005.json` | `efa97d4c982cc867b5a5b9b24862fd238e4f63992def0475033d615bd68ca8b2` |
| `waves/wave0006.json` | `6b5803ce31c3c66ecc8f2c94dacc33ca12183f51db60606177e99826c9999296` |

