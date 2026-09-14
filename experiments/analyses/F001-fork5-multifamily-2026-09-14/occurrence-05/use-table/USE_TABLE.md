# Use-relation table - H005 occurrence-05

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
- `daily/mini_prose/cycle01/response`

## Custody

- `plan_id`: `620ee8bc7e6653dde7b16c221d8c2e0e2ace4968acdad2eeb34c4925380d1e4c`
- `material_sha256`: `8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff`

| check | kind | result |
|---|---|---|
| `material_pin` | cross_file | verified (1/1 occurrence) |
| `manifest_pins` | cross_file | verified (3/3 manifests) |
| `receipt_present` | cross_file | verified (8/8 nodes) |
| `artifact_bytes_vs_receipt` | cross_file | verified (8/8 nodes) |
| `status_vs_receipt` | cross_file | verified (8/8 nodes) |
| `public_text` | cross_file | verified (8/8 nodes) |
| `attempt_vs_receipt` | cross_file | verified (8/8 nodes) |
| `request_record` | cross_file | verified (8/8 nodes) |
| `trace_pinned` | cross_file | verified (8/8 nodes) |
| `provider_bytes` | cross_file | verified (8/8 nodes) |
| `wave_placement` | cross_file | verified (8/8 nodes) |
| `projection_source` | cross_file | verified (7/9 projections; 2 projection(s) had no exposed source (the slot is absent): `daily/mini_fcl/cycle01/account#p.account.0`, `daily/mini_prose/cycle01/account#p.account.0`) |
| `plan_identity` | self_consistency | verified (1/1 occurrence) |
| `artifact_self_hash` | self_consistency | verified (8/8 nodes) |
| `artifact_coordinate` | self_consistency | verified (8/8 nodes) |
| `brief_pinned` | self_consistency | verified (8/8 nodes) |
| `brief_label_index` | self_consistency | verified (8/8 nodes) |
| `task_label` | self_consistency | verified (8/8 nodes) |

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
| refs walked | 34 |
| cross document rows | 12 |
| intra document | 22 |
| refs to exposed task artifact | 0 |
| unresolved | 0 |
| importer resolved counter | 34 |
| importer extension counter | 0 |
| importer dangling counter | 0 |

These are counts of authored refs, reported as information. No count here warrants anything (FW5:851: counts "are not outlawed as information"; what is forbidden is a count entering as an *automatic* warrant).

## Rows

### Row 1 - `daily/mini_fcl/cycle01/objection#c1` --mentions--> `daily/mini_fcl/cycle01/account#c2`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `c1` (type `claim`) |
| ref field | `mentions` |
| ref verbatim | `b825b2df18dab817#c2` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c2` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[31:467]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c1","type":"claim","text":"Scope note: every objection here is built from the same thin task text the account used, so each is as conjectural as what it targets; the criticisms bear on the recommendation layer and on completeness, and even where they land they reorder or extend the account rather than refute its core conjectures.","scope":"stance","mentions":["b825b2df18dab817#c2","b825b2df18dab817#c3","b825b2df18dab817#c4"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[651:988]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c2","type":"claim","text":"Conjecture: the recurring disputes over what an agreement meant are mainly underspecification — agreements leave open by-when, how-often, and what-counts-as-done — with an open alternative that ambiguity is being used to renegotiate silently when schedules change.","scope":"diagnosis","depends":["c1"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c2`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[204:318]` - distinctive tokens `conjecture`
  ```text
  So the objections below mostly strike at the recommendation layer and at the completeness of the conjecture space.
  ```
- `body[548:661]` - distinctive tokens `agreements`
  ```text
  Remedies (1)–(3) — written shared agreements, a standing review, a swap rule — are agreements about how to agree.
  ```
- `body[1304:1396]` - distinctive tokens `recurring`
  ```text
  The avoider is avoiding the conversations; the review is a recurring three-way conversation.
  ```
- `body[1687:1828]` - distinctive tokens `change`, `schedules`
  ```text
  Third, remedy (3) undercuts c3. Fixed zones are still allocations, and by the account's own analysis allocations decay when schedules change.
  ```
- `body[2063:2155]` - distinctive tokens `agreement`, `conjecture`, `meant`
  ```text
  Fourth, the conjecture space for 'we disagree about what the agreement meant' is incomplete.
  ```
- `body[2156:2387]` - distinctive tokens `ambiguity`, `change`, `underspecification`
  ```text
  Besides underspecification and quiet re-tailoring when circumstances change, retrospective excuse-manufacture after plain non-performance fits the text equally well — ambiguity produced on demand because producing it costs nothing.
  ```
- `body[2526:2778]` - distinctive tokens `agreement`, `agreements`, `ambiguity`, `change`, `disputes`
  ```text
  Written agreements still help under this reading (they raise the cost of on-demand ambiguity), but expectations change: disputes get relocated more than settled, and the account says nothing about what happens when a written agreement is still not met.
  ```
- `body[2871:3228]` - distinctive tokens `diagnosis`
  ```text
  Dissolving interdependence — each person handles their own dishes and mess, a paid clean of common areas split three ways if affordable, or a consciously lower shared standard — is never considered, though the account's own diagnosis (negotiation is expensive, one party opts out) fits shrink-the-surface remedies as well as or better than mechanism design.
  ```
- `body[3304:3478]` - distinctive tokens `disputes`
  ```text
  One open question: the task is a first-person participant's account — 'we keep arguing' — so the reporter is inside the disputes and could be part of what the avoider avoids.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 2 - `daily/mini_fcl/cycle01/objection#c1` --mentions--> `daily/mini_fcl/cycle01/account#c3`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `c1` (type `claim`) |
| ref field | `mentions` |
| ref verbatim | `b825b2df18dab817#c3` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c3` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[31:467]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c1","type":"claim","text":"Scope note: every objection here is built from the same thin task text the account used, so each is as conjectural as what it targets; the criticisms bear on the recommendation layer and on completeness, and even where they land they reorder or extend the account rather than refute its core conjectures.","scope":"stance","mentions":["b825b2df18dab817#c2","b825b2df18dab817#c3","b825b2df18dab817#c4"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[989:1266]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c3","type":"claim","text":"Conjecture: the deeper defect is a missing mechanism rather than a bad allocation — there is no routine, low-friction way to revise who does what, so every schedule change forces a fresh full negotiation.","scope":"diagnosis","depends":["c1"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c3`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[204:318]` - distinctive tokens `conjecture`
  ```text
  So the objections below mostly strike at the recommendation layer and at the completeness of the conjecture space.
  ```
- `body[517:547]` - distinctive tokens `defect`
  ```text
  First, a bootstrapping defect.
  ```
- `body[662:771]` - distinctive tokens `negotiation`
  ```text
  Installing them requires a negotiation of exactly the kind the account diagnoses as costly and dispute-prone.
  ```
- `body[1687:1828]` - distinctive tokens `change`
  ```text
  Third, remedy (3) undercuts c3. Fixed zones are still allocations, and by the account's own analysis allocations decay when schedules change.
  ```
- `body[2063:2155]` - distinctive tokens `conjecture`
  ```text
  Fourth, the conjecture space for 'we disagree about what the agreement meant' is incomplete.
  ```
- `body[2156:2387]` - distinctive tokens `change`
  ```text
  Besides underspecification and quiet re-tailoring when circumstances change, retrospective excuse-manufacture after plain non-performance fits the text equally well — ambiguity produced on demand because producing it costs nothing.
  ```
- `body[2388:2525]` - distinctive tokens `fresh`
  ```text
  And 'we wrote' is not innocent: written words still get interpreted, and control of the shared record becomes a fresh negotiable surface.
  ```
- `body[2526:2778]` - distinctive tokens `change`
  ```text
  Written agreements still help under this reading (they raise the cost of on-demand ambiguity), but expectations change: disputes get relocated more than settled, and the account says nothing about what happens when a written agreement is still not met.
  ```
- `body[2871:3228]` - distinctive tokens `diagnosis`, `mechanism`, `negotiation`
  ```text
  Dissolving interdependence — each person handles their own dishes and mess, a paid clean of common areas split three ways if affordable, or a consciously lower shared standard — is never considered, though the account's own diagnosis (negotiation is expensive, one party opts out) fits shrink-the-surface remedies as well as or better than mechanism design.
  ```
- `body[3600:3753]` - distinctive tokens `allocation`, `mechanism`
  ```text
  What survives all this: the three-fault separation, the mechanism-over-allocation framing, and the asynchronous, forward-looking outreach to the avoider.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 3 - `daily/mini_fcl/cycle01/objection#c1` --mentions--> `daily/mini_fcl/cycle01/account#c4`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `c1` (type `claim`) |
| ref field | `mentions` |
| ref verbatim | `b825b2df18dab817#c4` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c4` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[31:467]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c1","type":"claim","text":"Scope note: every objection here is built from the same thin task text the account used, so each is as conjectural as what it targets; the criticisms bear on the recommendation layer and on completeness, and even where they land they reorder or extend the account rather than refute its core conjectures.","scope":"stance","mentions":["b825b2df18dab817#c2","b825b2df18dab817#c3","b825b2df18dab817#c4"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[1267:1555]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c4","type":"claim","text":"Conjecture: the friend's avoidance is information about the conversation's cost or format, not only about chores; remedies that require long three-way face-to-face sessions are structurally mismatched to this fault.","scope":"diagnosis","depends":["c1"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c4`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[204:318]` - distinctive tokens `conjecture`
  ```text
  So the objections below mostly strike at the recommendation layer and at the completeness of the conjecture space.
  ```
- `body[548:661]` - distinctive tokens `remedies`
  ```text
  Remedies (1)–(3) — written shared agreements, a standing review, a swap rule — are agreements about how to agree.
  ```
- `body[1304:1396]` - distinctive tokens `conversation`
  ```text
  The avoider is avoiding the conversations; the review is a recurring three-way conversation.
  ```
- `body[1397:1573]` - distinctive tokens `format`
  ```text
  'Short' is asserted as the fix, but nothing in the text or the account gives grounds that duration, rather than format, outcome, or anticipated blame, is what is being avoided.
  ```
- `body[1829:2005]` - distinctive tokens `avoidance`, `fault`, `remedies`
  ```text
  Zones only stay current if the review works — so the five points are not independent remedies, and nearly all the load lands on the element most exposed to the avoidance fault.
  ```
- `body[2063:2155]` - distinctive tokens `conjecture`
  ```text
  Fourth, the conjecture space for 'we disagree about what the agreement meant' is incomplete.
  ```
- `body[2871:3228]` - distinctive tokens `diagnosis`, `remedies`
  ```text
  Dissolving interdependence — each person handles their own dishes and mess, a paid clean of common areas split three ways if affordable, or a consciously lower shared standard — is never considered, though the account's own diagnosis (negotiation is expensive, one party opts out) fits shrink-the-surface remedies as well as or better than mechanism design.
  ```
- `body[3600:3753]` - distinctive tokens `fault`
  ```text
  What survives all this: the three-fault separation, the mechanism-over-allocation framing, and the asynchronous, forward-looking outreach to the avoider.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 4 - `daily/mini_fcl/cycle01/objection#o1` --target--> `daily/mini_fcl/cycle01/account#u1`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o1` (type `objection`) |
| ref field | `target` |
| ref verbatim | `b825b2df18dab817#u1` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `u1` (type `use`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[468:1230]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o1","type":"objection","text":"Bootstrapping defect: the remedy bundle (written shared agreements, standing review, swap rule) consists of agreements about how to agree, and installing it requires a negotiation of exactly the kind the account diagnoses as costly and dispute-prone. The account's own point that the asker's lever is only their own moves covers the one-on-one outreach but not the institutional pieces, which need buy-in from both other flatmates.","target":["b825b2df18dab817#u1"],"bearing":"If this holds, the recommendations need ordering by unilateral feasibility (personal record-keeping, a declared zone split, async outreach), with shared institutions treated as proposals contingent on that groundwork rather than as the core fix."}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[2599:3303]`, code point offsets into the decoded `commitments` string)

```json
{"id":"u1","type":"use","text":"Proposed direction for whoever continues: (1) treat meaning disputes as specification bugs and make future agreements written, shared, and checkable — what, by when, what done means; (2) replace one-off negotiation with a short standing review that absorbs schedule changes, plus a default swap rule for missed slots; (3) shrink the negotiable set by assigning zones or recurring ownership; (4) approach the avoider one-on-one and possibly asynchronously, asking what would make the exchanges easier rather than why they have been absent; (5) frame the asker's own proposed format changes, not control of the other two, as the available lever.","depends":["c2","c3","c4"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#u1`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[548:661]` - distinctive tokens `agreements`, `review`, `shared`, `standing`, `written`
  ```text
  Remedies (1)–(3) — written shared agreements, a standing review, a swap rule — are agreements about how to agree.
  ```
- `body[662:771]` - distinctive tokens `negotiation`
  ```text
  Installing them requires a negotiation of exactly the kind the account diagnoses as costly and dispute-prone.
  ```
- `body[772:967]` - distinctive tokens `asker`, `lever`
  ```text
  The account's own point (5) concedes the asker's only lever is their own moves, but that covers the one-on-one outreach, not the institutional pieces, which need buy-in from both other flatmates.
  ```
- `body[968:1238]` - distinctive tokens `asker`, `proposed`, `shared`
  ```text
  If this holds, the list needs ordering by unilateral feasibility — personal record-keeping, a proposed zone split the asker simply declares they will follow, async outreach — with the shared institutions treated as proposals contingent on that work, not as the core fix.
  ```
- `body[1240:1303]` - distinctive tokens `review`, `standing`
  ```text
  Second, an internal tension between c4 and the standing review.
  ```
- `body[1304:1396]` - distinctive tokens `avoider`, `recurring`, `review`
  ```text
  The avoider is avoiding the conversations; the review is a recurring three-way conversation.
  ```
- `body[1397:1573]` - distinctive tokens `format`, `short`
  ```text
  'Short' is asserted as the fix, but nothing in the text or the account gives grounds that duration, rather than format, outcome, or anticipated blame, is what is being avoided.
  ```
- `body[1687:1828]` - distinctive tokens `zones`
  ```text
  Third, remedy (3) undercuts c3. Fixed zones are still allocations, and by the account's own analysis allocations decay when schedules change.
  ```
- `body[1829:2005]` - distinctive tokens `review`, `zones`
  ```text
  Zones only stay current if the review works — so the five points are not independent remedies, and nearly all the load lands on the element most exposed to the avoidance fault.
  ```
- `body[2006:2061]` - distinctive tokens `review`
  ```text
  If the review is rejected, the account has no fallback.
  ```
- `body[2388:2525]` - distinctive tokens `control`, `negotiable`, `shared`, `written`
  ```text
  And 'we wrote' is not innocent: written words still get interpreted, and control of the shared record becomes a fresh negotiable surface.
  ```
- `body[2526:2778]` - distinctive tokens `agreements`, `disputes`, `written`
  ```text
  Written agreements still help under this reading (they raise the cost of on-demand ambiguity), but expectations change: disputes get relocated more than settled, and the account says nothing about what happens when a written agreement is still not met.
  ```
- `body[2780:2870]` - distinctive tokens `shared`
  ```text
  Fifth, the option space is tacitly limited to better governance of the shared chore stock.
  ```
- `body[2871:3228]` - distinctive tokens `negotiation`, `shared`, `shrink`
  ```text
  Dissolving interdependence — each person handles their own dishes and mess, a paid clean of common areas split three ways if affordable, or a consciously lower shared standard — is never considered, though the account's own diagnosis (negotiation is expensive, one party opts out) fits shrink-the-surface remedies as well as or better than mechanism design.
  ```
- `body[3304:3478]` - distinctive tokens `avoider`, `disputes`
  ```text
  One open question: the task is a first-person participant's account — 'we keep arguing' — so the reporter is inside the disputes and could be part of what the avoider avoids.
  ```
- `body[3479:3599]` - distinctive tokens `asker`
  ```text
  Neither the text nor the account can settle this, but the account treats the asker as a neutral repair agent throughout.
  ```
- `body[3600:3753]` - distinctive tokens `avoider`
  ```text
  What survives all this: the three-fault separation, the mechanism-over-allocation framing, and the asynchronous, forward-looking outreach to the avoider.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 5 - `daily/mini_fcl/cycle01/objection#o2` --target--> `daily/mini_fcl/cycle01/account#u1`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o2` (type `objection`) |
| ref field | `target` |
| ref verbatim | `b825b2df18dab817#u1` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `u1` (type `use`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[1231:1798]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o2","type":"objection","text":"Internal tension: the standing review is a recurring three-way conversation, and the avoider is avoiding the conversations. 'Short' is asserted as the fix, but neither the task text nor the account gives grounds that duration, rather than format, outcome, or anticipated blame, is what the avoider avoids.","target":["b825b2df18dab817#u1","b825b2df18dab817#c4"],"bearing":"Unless the one-on-one establishes what is being avoided, the review should be specified as asynchronous or opt-in, or dropped as the load-bearing element."}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[2599:3303]`, code point offsets into the decoded `commitments` string)

```json
{"id":"u1","type":"use","text":"Proposed direction for whoever continues: (1) treat meaning disputes as specification bugs and make future agreements written, shared, and checkable — what, by when, what done means; (2) replace one-off negotiation with a short standing review that absorbs schedule changes, plus a default swap rule for missed slots; (3) shrink the negotiable set by assigning zones or recurring ownership; (4) approach the avoider one-on-one and possibly asynchronously, asking what would make the exchanges easier rather than why they have been absent; (5) frame the asker's own proposed format changes, not control of the other two, as the available lever.","depends":["c2","c3","c4"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#u1`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[548:661]` - distinctive tokens `agreements`, `review`, `shared`, `standing`, `written`
  ```text
  Remedies (1)–(3) — written shared agreements, a standing review, a swap rule — are agreements about how to agree.
  ```
- `body[662:771]` - distinctive tokens `negotiation`
  ```text
  Installing them requires a negotiation of exactly the kind the account diagnoses as costly and dispute-prone.
  ```
- `body[772:967]` - distinctive tokens `asker`, `lever`
  ```text
  The account's own point (5) concedes the asker's only lever is their own moves, but that covers the one-on-one outreach, not the institutional pieces, which need buy-in from both other flatmates.
  ```
- `body[968:1238]` - distinctive tokens `asker`, `proposed`, `shared`
  ```text
  If this holds, the list needs ordering by unilateral feasibility — personal record-keeping, a proposed zone split the asker simply declares they will follow, async outreach — with the shared institutions treated as proposals contingent on that work, not as the core fix.
  ```
- `body[1240:1303]` - distinctive tokens `review`, `standing`
  ```text
  Second, an internal tension between c4 and the standing review.
  ```
- `body[1304:1396]` - distinctive tokens `avoider`, `recurring`, `review`
  ```text
  The avoider is avoiding the conversations; the review is a recurring three-way conversation.
  ```
- `body[1397:1573]` - distinctive tokens `format`, `short`
  ```text
  'Short' is asserted as the fix, but nothing in the text or the account gives grounds that duration, rather than format, outcome, or anticipated blame, is what is being avoided.
  ```
- `body[1687:1828]` - distinctive tokens `zones`
  ```text
  Third, remedy (3) undercuts c3. Fixed zones are still allocations, and by the account's own analysis allocations decay when schedules change.
  ```
- `body[1829:2005]` - distinctive tokens `review`, `zones`
  ```text
  Zones only stay current if the review works — so the five points are not independent remedies, and nearly all the load lands on the element most exposed to the avoidance fault.
  ```
- `body[2006:2061]` - distinctive tokens `review`
  ```text
  If the review is rejected, the account has no fallback.
  ```
- `body[2388:2525]` - distinctive tokens `control`, `negotiable`, `shared`, `written`
  ```text
  And 'we wrote' is not innocent: written words still get interpreted, and control of the shared record becomes a fresh negotiable surface.
  ```
- `body[2526:2778]` - distinctive tokens `agreements`, `disputes`, `written`
  ```text
  Written agreements still help under this reading (they raise the cost of on-demand ambiguity), but expectations change: disputes get relocated more than settled, and the account says nothing about what happens when a written agreement is still not met.
  ```
- `body[2780:2870]` - distinctive tokens `shared`
  ```text
  Fifth, the option space is tacitly limited to better governance of the shared chore stock.
  ```
- `body[2871:3228]` - distinctive tokens `negotiation`, `shared`, `shrink`
  ```text
  Dissolving interdependence — each person handles their own dishes and mess, a paid clean of common areas split three ways if affordable, or a consciously lower shared standard — is never considered, though the account's own diagnosis (negotiation is expensive, one party opts out) fits shrink-the-surface remedies as well as or better than mechanism design.
  ```
- `body[3304:3478]` - distinctive tokens `avoider`, `disputes`
  ```text
  One open question: the task is a first-person participant's account — 'we keep arguing' — so the reporter is inside the disputes and could be part of what the avoider avoids.
  ```
- `body[3479:3599]` - distinctive tokens `asker`
  ```text
  Neither the text nor the account can settle this, but the account treats the asker as a neutral repair agent throughout.
  ```
- `body[3600:3753]` - distinctive tokens `avoider`
  ```text
  What survives all this: the three-fault separation, the mechanism-over-allocation framing, and the asynchronous, forward-looking outreach to the avoider.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 6 - `daily/mini_fcl/cycle01/objection#o2` --target--> `daily/mini_fcl/cycle01/account#c4`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o2` (type `objection`) |
| ref field | `target` |
| ref verbatim | `b825b2df18dab817#c4` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c4` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[1231:1798]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o2","type":"objection","text":"Internal tension: the standing review is a recurring three-way conversation, and the avoider is avoiding the conversations. 'Short' is asserted as the fix, but neither the task text nor the account gives grounds that duration, rather than format, outcome, or anticipated blame, is what the avoider avoids.","target":["b825b2df18dab817#u1","b825b2df18dab817#c4"],"bearing":"Unless the one-on-one establishes what is being avoided, the review should be specified as asynchronous or opt-in, or dropped as the load-bearing element."}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[1267:1555]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c4","type":"claim","text":"Conjecture: the friend's avoidance is information about the conversation's cost or format, not only about chores; remedies that require long three-way face-to-face sessions are structurally mismatched to this fault.","scope":"diagnosis","depends":["c1"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c4`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[204:318]` - distinctive tokens `conjecture`
  ```text
  So the objections below mostly strike at the recommendation layer and at the completeness of the conjecture space.
  ```
- `body[548:661]` - distinctive tokens `remedies`
  ```text
  Remedies (1)–(3) — written shared agreements, a standing review, a swap rule — are agreements about how to agree.
  ```
- `body[1304:1396]` - distinctive tokens `conversation`
  ```text
  The avoider is avoiding the conversations; the review is a recurring three-way conversation.
  ```
- `body[1397:1573]` - distinctive tokens `format`
  ```text
  'Short' is asserted as the fix, but nothing in the text or the account gives grounds that duration, rather than format, outcome, or anticipated blame, is what is being avoided.
  ```
- `body[1829:2005]` - distinctive tokens `avoidance`, `fault`, `remedies`
  ```text
  Zones only stay current if the review works — so the five points are not independent remedies, and nearly all the load lands on the element most exposed to the avoidance fault.
  ```
- `body[2063:2155]` - distinctive tokens `conjecture`
  ```text
  Fourth, the conjecture space for 'we disagree about what the agreement meant' is incomplete.
  ```
- `body[2871:3228]` - distinctive tokens `diagnosis`, `remedies`
  ```text
  Dissolving interdependence — each person handles their own dishes and mess, a paid clean of common areas split three ways if affordable, or a consciously lower shared standard — is never considered, though the account's own diagnosis (negotiation is expensive, one party opts out) fits shrink-the-surface remedies as well as or better than mechanism design.
  ```
- `body[3600:3753]` - distinctive tokens `fault`
  ```text
  What survives all this: the three-fault separation, the mechanism-over-allocation framing, and the asynchronous, forward-looking outreach to the avoider.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 7 - `daily/mini_fcl/cycle01/objection#o3` --target--> `daily/mini_fcl/cycle01/account#u1`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o3` (type `objection`) |
| ref field | `target` |
| ref verbatim | `b825b2df18dab817#u1` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `u1` (type `use`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[1799:2449]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o3","type":"objection","text":"Remedy (3), fixed zones or recurring ownership, is itself an allocation and by the account's own c3 allocations decay when schedules change; zones stay current only if the standing review works. The five-point list is therefore less a set of independent remedies than it appears, with nearly all the load on the element most exposed to the avoidance fault.","target":["b825b2df18dab817#u1","b825b2df18dab817#c3"],"bearing":"If the review fails or is rejected, zones and written agreements decay on schedule and the account has no fallback; the effective remedy set is smaller and more fragile than u1 presents."}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[2599:3303]`, code point offsets into the decoded `commitments` string)

```json
{"id":"u1","type":"use","text":"Proposed direction for whoever continues: (1) treat meaning disputes as specification bugs and make future agreements written, shared, and checkable — what, by when, what done means; (2) replace one-off negotiation with a short standing review that absorbs schedule changes, plus a default swap rule for missed slots; (3) shrink the negotiable set by assigning zones or recurring ownership; (4) approach the avoider one-on-one and possibly asynchronously, asking what would make the exchanges easier rather than why they have been absent; (5) frame the asker's own proposed format changes, not control of the other two, as the available lever.","depends":["c2","c3","c4"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#u1`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[548:661]` - distinctive tokens `agreements`, `review`, `shared`, `standing`, `written`
  ```text
  Remedies (1)–(3) — written shared agreements, a standing review, a swap rule — are agreements about how to agree.
  ```
- `body[662:771]` - distinctive tokens `negotiation`
  ```text
  Installing them requires a negotiation of exactly the kind the account diagnoses as costly and dispute-prone.
  ```
- `body[772:967]` - distinctive tokens `asker`, `lever`
  ```text
  The account's own point (5) concedes the asker's only lever is their own moves, but that covers the one-on-one outreach, not the institutional pieces, which need buy-in from both other flatmates.
  ```
- `body[968:1238]` - distinctive tokens `asker`, `proposed`, `shared`
  ```text
  If this holds, the list needs ordering by unilateral feasibility — personal record-keeping, a proposed zone split the asker simply declares they will follow, async outreach — with the shared institutions treated as proposals contingent on that work, not as the core fix.
  ```
- `body[1240:1303]` - distinctive tokens `review`, `standing`
  ```text
  Second, an internal tension between c4 and the standing review.
  ```
- `body[1304:1396]` - distinctive tokens `avoider`, `recurring`, `review`
  ```text
  The avoider is avoiding the conversations; the review is a recurring three-way conversation.
  ```
- `body[1397:1573]` - distinctive tokens `format`, `short`
  ```text
  'Short' is asserted as the fix, but nothing in the text or the account gives grounds that duration, rather than format, outcome, or anticipated blame, is what is being avoided.
  ```
- `body[1687:1828]` - distinctive tokens `zones`
  ```text
  Third, remedy (3) undercuts c3. Fixed zones are still allocations, and by the account's own analysis allocations decay when schedules change.
  ```
- `body[1829:2005]` - distinctive tokens `review`, `zones`
  ```text
  Zones only stay current if the review works — so the five points are not independent remedies, and nearly all the load lands on the element most exposed to the avoidance fault.
  ```
- `body[2006:2061]` - distinctive tokens `review`
  ```text
  If the review is rejected, the account has no fallback.
  ```
- `body[2388:2525]` - distinctive tokens `control`, `negotiable`, `shared`, `written`
  ```text
  And 'we wrote' is not innocent: written words still get interpreted, and control of the shared record becomes a fresh negotiable surface.
  ```
- `body[2526:2778]` - distinctive tokens `agreements`, `disputes`, `written`
  ```text
  Written agreements still help under this reading (they raise the cost of on-demand ambiguity), but expectations change: disputes get relocated more than settled, and the account says nothing about what happens when a written agreement is still not met.
  ```
- `body[2780:2870]` - distinctive tokens `shared`
  ```text
  Fifth, the option space is tacitly limited to better governance of the shared chore stock.
  ```
- `body[2871:3228]` - distinctive tokens `negotiation`, `shared`, `shrink`
  ```text
  Dissolving interdependence — each person handles their own dishes and mess, a paid clean of common areas split three ways if affordable, or a consciously lower shared standard — is never considered, though the account's own diagnosis (negotiation is expensive, one party opts out) fits shrink-the-surface remedies as well as or better than mechanism design.
  ```
- `body[3304:3478]` - distinctive tokens `avoider`, `disputes`
  ```text
  One open question: the task is a first-person participant's account — 'we keep arguing' — so the reporter is inside the disputes and could be part of what the avoider avoids.
  ```
- `body[3479:3599]` - distinctive tokens `asker`
  ```text
  Neither the text nor the account can settle this, but the account treats the asker as a neutral repair agent throughout.
  ```
- `body[3600:3753]` - distinctive tokens `avoider`
  ```text
  What survives all this: the three-fault separation, the mechanism-over-allocation framing, and the asynchronous, forward-looking outreach to the avoider.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 8 - `daily/mini_fcl/cycle01/objection#o3` --target--> `daily/mini_fcl/cycle01/account#c3`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o3` (type `objection`) |
| ref field | `target` |
| ref verbatim | `b825b2df18dab817#c3` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c3` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[1799:2449]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o3","type":"objection","text":"Remedy (3), fixed zones or recurring ownership, is itself an allocation and by the account's own c3 allocations decay when schedules change; zones stay current only if the standing review works. The five-point list is therefore less a set of independent remedies than it appears, with nearly all the load on the element most exposed to the avoidance fault.","target":["b825b2df18dab817#u1","b825b2df18dab817#c3"],"bearing":"If the review fails or is rejected, zones and written agreements decay on schedule and the account has no fallback; the effective remedy set is smaller and more fragile than u1 presents."}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[989:1266]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c3","type":"claim","text":"Conjecture: the deeper defect is a missing mechanism rather than a bad allocation — there is no routine, low-friction way to revise who does what, so every schedule change forces a fresh full negotiation.","scope":"diagnosis","depends":["c1"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c3`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[204:318]` - distinctive tokens `conjecture`
  ```text
  So the objections below mostly strike at the recommendation layer and at the completeness of the conjecture space.
  ```
- `body[517:547]` - distinctive tokens `defect`
  ```text
  First, a bootstrapping defect.
  ```
- `body[662:771]` - distinctive tokens `negotiation`
  ```text
  Installing them requires a negotiation of exactly the kind the account diagnoses as costly and dispute-prone.
  ```
- `body[1687:1828]` - distinctive tokens `change`
  ```text
  Third, remedy (3) undercuts c3. Fixed zones are still allocations, and by the account's own analysis allocations decay when schedules change.
  ```
- `body[2063:2155]` - distinctive tokens `conjecture`
  ```text
  Fourth, the conjecture space for 'we disagree about what the agreement meant' is incomplete.
  ```
- `body[2156:2387]` - distinctive tokens `change`
  ```text
  Besides underspecification and quiet re-tailoring when circumstances change, retrospective excuse-manufacture after plain non-performance fits the text equally well — ambiguity produced on demand because producing it costs nothing.
  ```
- `body[2388:2525]` - distinctive tokens `fresh`
  ```text
  And 'we wrote' is not innocent: written words still get interpreted, and control of the shared record becomes a fresh negotiable surface.
  ```
- `body[2526:2778]` - distinctive tokens `change`
  ```text
  Written agreements still help under this reading (they raise the cost of on-demand ambiguity), but expectations change: disputes get relocated more than settled, and the account says nothing about what happens when a written agreement is still not met.
  ```
- `body[2871:3228]` - distinctive tokens `diagnosis`, `mechanism`, `negotiation`
  ```text
  Dissolving interdependence — each person handles their own dishes and mess, a paid clean of common areas split three ways if affordable, or a consciously lower shared standard — is never considered, though the account's own diagnosis (negotiation is expensive, one party opts out) fits shrink-the-surface remedies as well as or better than mechanism design.
  ```
- `body[3600:3753]` - distinctive tokens `allocation`, `mechanism`
  ```text
  What survives all this: the three-fault separation, the mechanism-over-allocation framing, and the asynchronous, forward-looking outreach to the avoider.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 9 - `daily/mini_fcl/cycle01/objection#o4` --target--> `daily/mini_fcl/cycle01/account#c2`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o4` (type `objection`) |
| ref field | `target` |
| ref verbatim | `b825b2df18dab817#c2` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c2` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[2450:3304]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o4","type":"objection","text":"The conjecture space for 'we disagree about what the agreement meant' is incomplete: besides underspecification and quiet re-tailoring when schedules change, retrospective excuse-manufacture after plain non-performance fits the text equally well — ambiguity produced on demand because producing it costs nothing. Relatedly, 'we wrote' is not innocent: written words still require interpretation and control of the shared record becomes a new negotiable surface.","target":["b825b2df18dab817#c2"],"bearing":"Writing agreements down still helps under this reading because it raises the cost of on-demand ambiguity, but expectations shift: disputes relocate more than settle, and what happens when a written agreement is still not met is a question the task text gives no leverage on and the account leaves untouched."}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[651:988]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c2","type":"claim","text":"Conjecture: the recurring disputes over what an agreement meant are mainly underspecification — agreements leave open by-when, how-often, and what-counts-as-done — with an open alternative that ambiguity is being used to renegotiate silently when schedules change.","scope":"diagnosis","depends":["c1"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c2`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[204:318]` - distinctive tokens `conjecture`
  ```text
  So the objections below mostly strike at the recommendation layer and at the completeness of the conjecture space.
  ```
- `body[548:661]` - distinctive tokens `agreements`
  ```text
  Remedies (1)–(3) — written shared agreements, a standing review, a swap rule — are agreements about how to agree.
  ```
- `body[1304:1396]` - distinctive tokens `recurring`
  ```text
  The avoider is avoiding the conversations; the review is a recurring three-way conversation.
  ```
- `body[1687:1828]` - distinctive tokens `change`, `schedules`
  ```text
  Third, remedy (3) undercuts c3. Fixed zones are still allocations, and by the account's own analysis allocations decay when schedules change.
  ```
- `body[2063:2155]` - distinctive tokens `agreement`, `conjecture`, `meant`
  ```text
  Fourth, the conjecture space for 'we disagree about what the agreement meant' is incomplete.
  ```
- `body[2156:2387]` - distinctive tokens `ambiguity`, `change`, `underspecification`
  ```text
  Besides underspecification and quiet re-tailoring when circumstances change, retrospective excuse-manufacture after plain non-performance fits the text equally well — ambiguity produced on demand because producing it costs nothing.
  ```
- `body[2526:2778]` - distinctive tokens `agreement`, `agreements`, `ambiguity`, `change`, `disputes`
  ```text
  Written agreements still help under this reading (they raise the cost of on-demand ambiguity), but expectations change: disputes get relocated more than settled, and the account says nothing about what happens when a written agreement is still not met.
  ```
- `body[2871:3228]` - distinctive tokens `diagnosis`
  ```text
  Dissolving interdependence — each person handles their own dishes and mess, a paid clean of common areas split three ways if affordable, or a consciously lower shared standard — is never considered, though the account's own diagnosis (negotiation is expensive, one party opts out) fits shrink-the-surface remedies as well as or better than mechanism design.
  ```
- `body[3304:3478]` - distinctive tokens `disputes`
  ```text
  One open question: the task is a first-person participant's account — 'we keep arguing' — so the reporter is inside the disputes and could be part of what the avoider avoids.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 10 - `daily/mini_fcl/cycle01/objection#o5` --target--> `daily/mini_fcl/cycle01/account#u1`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o5` (type `objection`) |
| ref field | `target` |
| ref verbatim | `b825b2df18dab817#u1` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `u1` (type `use`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[3305:4076]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o5","type":"objection","text":"The option space is tacitly limited to better governance of the shared chore stock; dissolving interdependence — each person handles their own dishes and mess, a paid clean of common areas split three ways if affordable, or a consciously lower shared standard — is never considered, though the account's own diagnosis (costly negotiation, one party opting out) fits shrink-the-surface remedies as well as or better than mechanism design.","target":["b825b2df18dab817#u1","b825b2df18dab817#c1"],"bearing":"If a large share of chores can be de-collectivized, the allocation mechanism may be over-engineering for a residual that zones plus a simple rota cover; at minimum the account should say why governance rather than dissolution."}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[2599:3303]`, code point offsets into the decoded `commitments` string)

```json
{"id":"u1","type":"use","text":"Proposed direction for whoever continues: (1) treat meaning disputes as specification bugs and make future agreements written, shared, and checkable — what, by when, what done means; (2) replace one-off negotiation with a short standing review that absorbs schedule changes, plus a default swap rule for missed slots; (3) shrink the negotiable set by assigning zones or recurring ownership; (4) approach the avoider one-on-one and possibly asynchronously, asking what would make the exchanges easier rather than why they have been absent; (5) frame the asker's own proposed format changes, not control of the other two, as the available lever.","depends":["c2","c3","c4"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#u1`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[548:661]` - distinctive tokens `agreements`, `review`, `shared`, `standing`, `written`
  ```text
  Remedies (1)–(3) — written shared agreements, a standing review, a swap rule — are agreements about how to agree.
  ```
- `body[662:771]` - distinctive tokens `negotiation`
  ```text
  Installing them requires a negotiation of exactly the kind the account diagnoses as costly and dispute-prone.
  ```
- `body[772:967]` - distinctive tokens `asker`, `lever`
  ```text
  The account's own point (5) concedes the asker's only lever is their own moves, but that covers the one-on-one outreach, not the institutional pieces, which need buy-in from both other flatmates.
  ```
- `body[968:1238]` - distinctive tokens `asker`, `proposed`, `shared`
  ```text
  If this holds, the list needs ordering by unilateral feasibility — personal record-keeping, a proposed zone split the asker simply declares they will follow, async outreach — with the shared institutions treated as proposals contingent on that work, not as the core fix.
  ```
- `body[1240:1303]` - distinctive tokens `review`, `standing`
  ```text
  Second, an internal tension between c4 and the standing review.
  ```
- `body[1304:1396]` - distinctive tokens `avoider`, `recurring`, `review`
  ```text
  The avoider is avoiding the conversations; the review is a recurring three-way conversation.
  ```
- `body[1397:1573]` - distinctive tokens `format`, `short`
  ```text
  'Short' is asserted as the fix, but nothing in the text or the account gives grounds that duration, rather than format, outcome, or anticipated blame, is what is being avoided.
  ```
- `body[1687:1828]` - distinctive tokens `zones`
  ```text
  Third, remedy (3) undercuts c3. Fixed zones are still allocations, and by the account's own analysis allocations decay when schedules change.
  ```
- `body[1829:2005]` - distinctive tokens `review`, `zones`
  ```text
  Zones only stay current if the review works — so the five points are not independent remedies, and nearly all the load lands on the element most exposed to the avoidance fault.
  ```
- `body[2006:2061]` - distinctive tokens `review`
  ```text
  If the review is rejected, the account has no fallback.
  ```
- `body[2388:2525]` - distinctive tokens `control`, `negotiable`, `shared`, `written`
  ```text
  And 'we wrote' is not innocent: written words still get interpreted, and control of the shared record becomes a fresh negotiable surface.
  ```
- `body[2526:2778]` - distinctive tokens `agreements`, `disputes`, `written`
  ```text
  Written agreements still help under this reading (they raise the cost of on-demand ambiguity), but expectations change: disputes get relocated more than settled, and the account says nothing about what happens when a written agreement is still not met.
  ```
- `body[2780:2870]` - distinctive tokens `shared`
  ```text
  Fifth, the option space is tacitly limited to better governance of the shared chore stock.
  ```
- `body[2871:3228]` - distinctive tokens `negotiation`, `shared`, `shrink`
  ```text
  Dissolving interdependence — each person handles their own dishes and mess, a paid clean of common areas split three ways if affordable, or a consciously lower shared standard — is never considered, though the account's own diagnosis (negotiation is expensive, one party opts out) fits shrink-the-surface remedies as well as or better than mechanism design.
  ```
- `body[3304:3478]` - distinctive tokens `avoider`, `disputes`
  ```text
  One open question: the task is a first-person participant's account — 'we keep arguing' — so the reporter is inside the disputes and could be part of what the avoider avoids.
  ```
- `body[3479:3599]` - distinctive tokens `asker`
  ```text
  Neither the text nor the account can settle this, but the account treats the asker as a neutral repair agent throughout.
  ```
- `body[3600:3753]` - distinctive tokens `avoider`
  ```text
  What survives all this: the three-fault separation, the mechanism-over-allocation framing, and the asynchronous, forward-looking outreach to the avoider.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 11 - `daily/mini_fcl/cycle01/objection#o5` --target--> `daily/mini_fcl/cycle01/account#c1`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `o5` (type `objection`) |
| ref field | `target` |
| ref verbatim | `b825b2df18dab817#c1` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c1` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[3305:4076]`, code point offsets into the decoded `commitments` string)

```json
{"id":"o5","type":"objection","text":"The option space is tacitly limited to better governance of the shared chore stock; dissolving interdependence — each person handles their own dishes and mess, a paid clean of common areas split three ways if affordable, or a consciously lower shared standard — is never considered, though the account's own diagnosis (costly negotiation, one party opting out) fits shrink-the-surface remedies as well as or better than mechanism design.","target":["b825b2df18dab817#u1","b825b2df18dab817#c1"],"bearing":"If a large share of chores can be de-collectivized, the allocation mechanism may be over-engineering for a residual that zones plus a simple rota cover; at minimum the account should say why governance rather than dissolution."}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[316:650]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c1","type":"claim","text":"The flat's trouble is three separable faults braided together: agreements whose meaning drifts, an allocation that decays as schedules change, and one flatmate withdrawing from the conversations. Each fault needs different handling, so a fix aimed at only one will disappoint.","grounds":"task text"}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c1`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[0:203]` - distinctive tokens `faults`
  ```text
  This account is unusually careful: it separates the three faults, tags conjectures as conjectures, flags its own weakest move (o1 against the speculative psychology of c5), and holds open questions open.
  ```
- `body[548:661]` - distinctive tokens `agreements`
  ```text
  Remedies (1)–(3) — written shared agreements, a standing review, a swap rule — are agreements about how to agree.
  ```
- `body[1304:1396]` - distinctive tokens `conversations`
  ```text
  The avoider is avoiding the conversations; the review is a recurring three-way conversation.
  ```
- `body[1687:1828]` - distinctive tokens `change`, `schedules`
  ```text
  Third, remedy (3) undercuts c3. Fixed zones are still allocations, and by the account's own analysis allocations decay when schedules change.
  ```
- `body[1829:2005]` - distinctive tokens `fault`
  ```text
  Zones only stay current if the review works — so the five points are not independent remedies, and nearly all the load lands on the element most exposed to the avoidance fault.
  ```
- `body[2156:2387]` - distinctive tokens `change`
  ```text
  Besides underspecification and quiet re-tailoring when circumstances change, retrospective excuse-manufacture after plain non-performance fits the text equally well — ambiguity produced on demand because producing it costs nothing.
  ```
- `body[2526:2778]` - distinctive tokens `agreements`, `change`
  ```text
  Written agreements still help under this reading (they raise the cost of on-demand ambiguity), but expectations change: disputes get relocated more than settled, and the account says nothing about what happens when a written agreement is still not met.
  ```
- `body[3600:3753]` - distinctive tokens `allocation`, `fault`
  ```text
  What survives all this: the three-fault separation, the mechanism-over-allocation framing, and the asynchronous, forward-looking outreach to the avoider.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 12 - `daily/mini_fcl/cycle01/objection#p1` --mentions--> `daily/mini_fcl/cycle01/account#c4`

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/objection` |
| referring record | `p1` (type `problem`) |
| ref field | `mentions` |
| ref verbatim | `b825b2df18dab817#c4` |
| ref grain | record |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | `c4` (type `claim`) |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | true |

**Referring record, verbatim** (`daily/mini_fcl/cycle01/objection`, `commitments[4077:4428]`, code point offsets into the decoded `commitments` string)

```json
{"id":"p1","type":"problem","text":"The task is a first-person participant's account ('we keep arguing'), so the reporter is inside the disputes and may be part of what the avoider avoids; neither the task text nor the account can settle this, yet the account treats the asker as a neutral repair agent throughout.","mentions":["b825b2df18dab817#c4"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`, `commitments[1267:1555]`, code point offsets into the decoded `commitments` string)

```json
{"id":"c4","type":"claim","text":"Conjecture: the friend's avoidance is information about the conversation's cost or format, not only about chores; remedies that require long three-way face-to-face sessions are structurally mismatched to this fault.","scope":"diagnosis","depends":["c1"]}
```

**Referring BODY passages** (overlap subject: the prose fields of `daily/mini_fcl/cycle01/account#c4`; offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[204:318]` - distinctive tokens `conjecture`
  ```text
  So the objections below mostly strike at the recommendation layer and at the completeness of the conjecture space.
  ```
- `body[548:661]` - distinctive tokens `remedies`
  ```text
  Remedies (1)–(3) — written shared agreements, a standing review, a swap rule — are agreements about how to agree.
  ```
- `body[1304:1396]` - distinctive tokens `conversation`
  ```text
  The avoider is avoiding the conversations; the review is a recurring three-way conversation.
  ```
- `body[1397:1573]` - distinctive tokens `format`
  ```text
  'Short' is asserted as the fix, but nothing in the text or the account gives grounds that duration, rather than format, outcome, or anticipated blame, is what is being avoided.
  ```
- `body[1829:2005]` - distinctive tokens `avoidance`, `fault`, `remedies`
  ```text
  Zones only stay current if the review works — so the five points are not independent remedies, and nearly all the load lands on the element most exposed to the avoidance fault.
  ```
- `body[2063:2155]` - distinctive tokens `conjecture`
  ```text
  Fourth, the conjecture space for 'we disagree about what the agreement meant' is incomplete.
  ```
- `body[2871:3228]` - distinctive tokens `diagnosis`, `remedies`
  ```text
  Dissolving interdependence — each person handles their own dishes and mess, a paid clean of common areas split three ways if affordable, or a consciously lower shared standard — is never considered, though the account's own diagnosis (negotiation is expensive, one party opts out) fits shrink-the-surface remedies as well as or better than mechanism design.
  ```
- `body[3600:3753]` - distinctive tokens `fault`
  ```text
  What survives all this: the three-fault separation, the mechanism-over-allocation framing, and the asynchronous, forward-looking outreach to the avoider.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

## Declared uptake versus records present

### `daily/mini_fcl/cycle01/account`

- commitment surface: `read_fcl1`
- records present (10): `c0`, `c1`, `c2`, `c3`, `c4`, `c5`, `o1`, `p1`, `p2`, `u1`
- declared `uptake` (7): `c1`, `c2`, `c3`, `c4`, `u1`, `p1`, `o1`
- records in uptake (7): `c1`, `c2`, `c3`, `c4`, `o1`, `p1`, `u1`
- records omitted from uptake (3): `c0`, `c5`, `p2`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/objection`

- commitment surface: `read_fcl1`
- records present (7): `c1`, `o1`, `o2`, `o3`, `o4`, `o5`, `p1`
- declared `uptake` (7): `c1`, `o1`, `o2`, `o3`, `o4`, `o5`, `p1`
- records in uptake (7): `c1`, `o1`, `o2`, `o3`, `o4`, `o5`, `p1`
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
- `daily/mini_fcl/cycle01/rival` - commitment surface: unavailable_decode_failure; references not extractable by this instrument
- `daily/mini_prose/cycle01/rival` - commitment surface: prose (not parsed); references not extractable by this instrument
- `daily/mini_prose/cycle01/response` - commitment surface: prose (not parsed); references not extractable by this instrument

## Residue: refs that resolve to nothing

*No unresolved ref in this scope.*

## Files read

Every byte this instrument read, with its sha256. Nothing under the occurrence was written.

| path | sha256 |
|---|---|
| `artifacts/daily/bare/cycle01/answer.json` | `5f8649f563fa59dba1f9e507130ee0470ba3afe7e22127921fe641ccba0d95df` |
| `artifacts/daily/mini_fcl/cycle01/account.json` | `199fdfce722f92d5341a2b28b03c95856bced948fe10704985fd6caeff313ebf` |
| `artifacts/daily/mini_fcl/cycle01/objection.json` | `68257ce650e37d87cc23869e7793e10282aba93bc37c59e8d9d4922b2747ba9e` |
| `artifacts/daily/mini_fcl/cycle01/rival.json` | `7fa39b7cb4264888b550828e662b0127e6b97f0fc62bd704c06cc7fc40795741` |
| `artifacts/daily/mini_prose/cycle01/account.json` | `399e611599467995f5a3fa41c772b23ddc49be66f362aaf9181cdf4285ed4ce3` |
| `artifacts/daily/mini_prose/cycle01/objection.json` | `3796177d5680ea1913ee8eb939fcbc7a755e97204a99926735161dc5e879a53c` |
| `artifacts/daily/mini_prose/cycle01/response.json` | `3066b5652c09dab4fde54829d2dcf7c36f181058f8b62fd3402ab2d7ba3e194b` |
| `artifacts/daily/mini_prose/cycle01/rival.json` | `8872042f76fa0e877e0369decd8b48ec89f38b54a3a05e54907e895352463950` |
| `attempts/daily/bare/cycle01/answer.json` | `7b631103ba0bdf4422a23b44fd4c4d39a0ac3022fec4cee17d4796f0cad92b97` |
| `attempts/daily/mini_fcl/cycle01/account.json` | `fbba2aac8900f266ae06c374eabcaa92e3b0a8758815da15ac9d67b250aecaf6` |
| `attempts/daily/mini_fcl/cycle01/objection.json` | `3ec900860ed3e3f901c2ec1e4aee4dda006bcc11a1369e23978cf35c53f969ab` |
| `attempts/daily/mini_fcl/cycle01/rival.json` | `0641393ab443ea33ebf7fc97e7baf00b4dd61c739650c38f85f672c29885acb6` |
| `attempts/daily/mini_prose/cycle01/account.json` | `1105d0772c7b932332e42a6a8dadc429ff458f9f06ea31c18cb3f88a400e2782` |
| `attempts/daily/mini_prose/cycle01/objection.json` | `f5328624ee22d6f739103303a8219108009b8d7b079c995f7e42aec03fbc7120` |
| `attempts/daily/mini_prose/cycle01/response.json` | `2cc015834612197e7aa58833b577e098f559d7d337c19953ef7fe1fbe1f7f5bd` |
| `attempts/daily/mini_prose/cycle01/rival.json` | `8989c51a856173ec69a7072d5263a60b689e2bcf60081d06b1bb0a3e8f80feb9` |
| `manifests/fork5.json` | `f7e727daea6d3ba4353b1b2f93ae7e461a648c99877cf2ee97ca7653e30e1ee8` |
| `manifests/return6.json` | `f3ece835e680452807d9e0dd69232c34a452b67062cba75c4ba46bf87bb93951` |
| `manifests/weave7.json` | `ea8174af734dabde382a36cd85323a064ef9a8302490b9f85e1f9f360e7686df` |
| `material.json` | `8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff` |
| `plan.json` | `4a756b51d9ceb45b787b9741b025104caa5e8e2627bea0d94c85e48622956342` |
| `provider/daily/bare/cycle01/answer/call-0001.request.json` | `f249cc67679bc5661683e69836c01b416adfe55514e676906fadbe8c0b12fd20` |
| `provider/daily/bare/cycle01/answer/call-0001.response.json` | `8e776c57f70a1e7cf06f6e8ccffddaec32fa54a125692dfc69204daad01bea5a` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | `3834e60c3dedb7fd817457e8b778005149ed0a1ab83fef3635f94a3fa19d6c0e` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | `6a3e628116bfc5da381f9343d73f675bb93b299adebfc9af06c4eb30ae767f77` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.request.json` | `ab155588e7bcf32e4c29f88527a4e1970ad026f41172babb836300f2521f2267` |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.response.json` | `72e34dbc9be3897097f2948bce69503167cfbdf3d97f5e89179d048783224449` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | `79c688b3996f897bbaeba48d7937df4ec2d8e4444022e15dac902680bc78d5e0` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | `4e6e865cbf1a397f8536f30ff0f5bb37adb667f7acb3452f1023f40069b7890c` |
| `provider/daily/mini_prose/cycle01/account/call-0001.request.json` | `5855061f9b1ce0d84cc8cf178551c5465ada25aae2e902df33d2b99a594d8cdc` |
| `provider/daily/mini_prose/cycle01/account/call-0001.response.json` | `a9d4607827616681409362841e039a394ba310cf1abad43b9813c1535bbaf28a` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.request.json` | `14a6e8a83fb25922271a5cc76b91b27b6e0e4d5378b7875b4b5379bbb6111cae` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.response.json` | `321e2022572beb380e642cfd96792c69c90332db4ebcee0188996c2400d7e1ea` |
| `provider/daily/mini_prose/cycle01/response/call-0001.request.json` | `ef08eb2c2bd429a781be0674921792b2af206353436da01b71e039c2509fd4a8` |
| `provider/daily/mini_prose/cycle01/response/call-0001.response.json` | `608b3ea0099fc8b17a5b10123f5bae75ea055ed9038d6d0d0af13483f93538c2` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.request.json` | `1ed1cf36141d46a2af6c57d80656f88ec90174b45ac13ef480370502ff80c949` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.response.json` | `a3a9964860c9218389ef75334fb8f783dbbf9a1631e3c0f61ab477ca8ffd7e1f` |
| `requests/daily/bare/cycle01/answer.json` | `ede0a4cfd3296d41c6d30850e6875d855badb82ba85e101c2c6000b38fd004b0` |
| `requests/daily/mini_fcl/cycle01/account.json` | `ccb45382acf61a3ec6c0a7fb2344271c2e3c83ee2a3e4e5a6da118a09752d7d5` |
| `requests/daily/mini_fcl/cycle01/objection.json` | `e5943043b43114c08e99e555b52eb39dae5151ce89d97591ff455ad233dda9fb` |
| `requests/daily/mini_fcl/cycle01/rival.json` | `dd8805a0dc98263af8bdc65687382264b6906b5d426c19f312ba815069cc8a20` |
| `requests/daily/mini_prose/cycle01/account.json` | `6e63c8e3f80953621e3188d1cf3062ad574856766510d8818e55e8fe30220220` |
| `requests/daily/mini_prose/cycle01/objection.json` | `ffd4ba700d199ea598e296a4047e56e40c6657e9fa47aeb474fa7decda9b950a` |
| `requests/daily/mini_prose/cycle01/response.json` | `2b08d4702f37389c52322b7d99c48fcf2f91a698585869c918cd0b47b3090155` |
| `requests/daily/mini_prose/cycle01/rival.json` | `f0b0119ae1fb570ca2fd7bdf1ac7413dab8a1073cacabcaab5384d0489c182f3` |
| `responses/daily/bare/cycle01/answer.json` | `453730edc500fc5fd58e5d491dfeaf71d11019449c9f529e093fa1198b4f07d7` |
| `responses/daily/bare/cycle01/answer.txt` | `5d10d81f761ec16d0299f6fa440ce34110ebf53dcd450f1311bc5ffe5138cd4a` |
| `responses/daily/mini_fcl/cycle01/account.json` | `7676ce6e4aac785a2203fc3977d677d8f9eb7d55e25e4b9ffb27bec678f0eb0d` |
| `responses/daily/mini_fcl/cycle01/account.txt` | `cfd108866b6b35d61428b358bb31578e916ee2000821b570597915660f99b6f7` |
| `responses/daily/mini_fcl/cycle01/objection.json` | `2bf843f277435fd136b1343d535806ed94a353e6bd589674a42d5307702f34eb` |
| `responses/daily/mini_fcl/cycle01/objection.txt` | `ba0acc61c02ef86708c7106eebdc40cd0c5f26a9e7820ff42dc354b3ffb65abc` |
| `responses/daily/mini_fcl/cycle01/rival.json` | `89ee231489ee673f1b8f6730c7013ce6dff807b47b3167c8d92d1cbc79d7e7c1` |
| `responses/daily/mini_fcl/cycle01/rival.txt` | `a013725a7d4e87b5af96edf712895a31c38025544875506c4691d736f7ff4a11` |
| `responses/daily/mini_prose/cycle01/account.json` | `2d4ad8ae5bd7832530570ae2696d74fc5694c87bbc1e7e28d27efa5d538f57b6` |
| `responses/daily/mini_prose/cycle01/account.txt` | `c375eacdc84980cf922677a3a66a650ef43922888db63ba7d3e6ecfd4698179b` |
| `responses/daily/mini_prose/cycle01/objection.json` | `c9a04cd24836abc188f13a9885a16889e7f58ff5a2f92e6a45ecfbb56ecbbb20` |
| `responses/daily/mini_prose/cycle01/objection.txt` | `e7babcd58a8117f861ea476aeea8a9dab78c1f53bdb4f1edb5a876067fc7f2ae` |
| `responses/daily/mini_prose/cycle01/response.json` | `ea9d610c3ed5819180f368bb0de823ef083fcf60dd7b620ca29d904ba2ba299b` |
| `responses/daily/mini_prose/cycle01/response.txt` | `edf3d5b2985433aec3ee605860c1c21d99ce33d68b1e949e9e3fb53c09a2569a` |
| `responses/daily/mini_prose/cycle01/rival.json` | `6272b7e5b4a62b4d81c02555e674d4c250531852c895c77fdc70443dfeaf86d9` |
| `responses/daily/mini_prose/cycle01/rival.txt` | `d2c2fe1cb53d7e20520ea74e7d4c374702c57abfceabbdd251b16b55430d45aa` |
| `traces/daily/bare/cycle01/answer.json` | `4ff68da01ac0c9cfd4c060d4a822f7ced327003f53e9e96f1e3fb08916a7fbab` |
| `traces/daily/mini_fcl/cycle01/account.json` | `f4790106152ef33f8f02cc8f182089bd4e99beb4f553144a79e51e2ec4f92f53` |
| `traces/daily/mini_fcl/cycle01/objection.json` | `ebeb44b61d39a103e9cc85b67d4203098425cd32883eef6cfb23545ca6d28de0` |
| `traces/daily/mini_fcl/cycle01/rival.json` | `75beee6bc0501968f5bcb94f73c1b0197af2a017421682afb69de64c5977a019` |
| `traces/daily/mini_prose/cycle01/account.json` | `5725e108b01c89983c73bc7e84268aa9bbf8b77d8b6fe57c79df1137bd5db455` |
| `traces/daily/mini_prose/cycle01/objection.json` | `1f70c81fc2a4aa5fdb5470fa2c75cca0d5c2a2ae4f28dde426577a222f946765` |
| `traces/daily/mini_prose/cycle01/response.json` | `ad320bc23381168ea9512eb2801e9af70d764d14cbd0de1a4a0a662c2a1f76f8` |
| `traces/daily/mini_prose/cycle01/rival.json` | `e4e3f246b335b3b6247905d24000870409300a33a412afb9e472492c1678a05c` |
| `waves/wave0001.json` | `78c98d402f066cf2835c2a75fdeebc7b13ab3ac82924dead8a39f1d498e8acda` |
| `waves/wave0002.json` | `908a20cd5eac2d745e54fccbe3bd63e88e7f58e5baa40743b8bb92042b5a41b3` |
| `waves/wave0003.json` | `1946457f4bdb598d670e14063f681c835b5f2fefdf59021e57c69e30b3b737b4` |
| `waves/wave0004.json` | `c2a89d6741d85558395f20191f828b7270657c3ccff2e1aabdbc3c125666f59e` |

