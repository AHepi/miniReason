# Use-relation table - H005 occurrence-07

**The tool records juxtapositions; the reading is root's.** This table places each authored cross-document reference beside passages a root reader may find worth starting from - a finding aid, never a closed search space - and stops there. It scores nothing, ranks nothing, classifies nothing and mints no relation of its own; it has no `att`, no `dep`, no status and no label. **A lexical overlap is not evidence of use.** FCL-1's own rule is that `depends` and `mentions` are "not automatically inferred from citation or lexical overlap"; a witness of reason use "must preserve internal role bindings, not merely the endpoint string" (FW5:628); actual use is "not automatically machine-maintainable" while prompt appearance is only a delivery fact (FW5:640); and no function of an input-output projection agrees with the accounting predicate across models differing in active route (FW5:1218), "semantic use inferred from delivery logs" included (FW5:1222) - all as summarised in the FW5-versus-harness-spec review, `fw5-vs-harness-spec-review.md` §1 R2-R4, §3.1 and §5 P1/P6. Root fills the four empty cells by reading; `unresolved` is a legal value and stays unresolved (FW5:634). An empty cell is an **unread row**, not a reading of `unresolved`.

Instrument: `use_relation_h005/1`. Schema: `h005-use-relation.use-table.v1`.

## Scope

- `daily/bare/cycle01/answer`
- `daily/mini_fcl/cycle01/account`
- `daily/mini_prose/cycle01/account`
- `daily/mini_prose/cycle01/objection`
- `daily/mini_fcl/cycle01/rival`
- `daily/mini_prose/cycle01/rival`
- `daily/mini_prose/cycle01/response`
- `daily/mini_prose/cycle01/carry`

## Custody

- `plan_id`: `77aa01f46f57471838e6cb46c96eb3ad9adfc2c1053376051dc098edd58d306d`
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
| `projection_source` | cross_file | verified (9/12 projections; 3 projection(s) had no exposed source (the slot is absent): `daily/mini_fcl/cycle01/account#p.account.0`, `daily/mini_prose/cycle01/account#p.account.0`, `daily/mini_prose/cycle01/carry#p.carry.3`) |
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
| refs walked | 39 |
| cross document rows | 6 |
| intra document | 33 |
| refs to exposed task artifact | 0 |
| unresolved | 0 |
| importer resolved counter | 33 |
| importer extension counter | 6 |
| importer dangling counter | 0 |

These are counts of authored refs, reported as information. No count here warrants anything (FW5:851: counts "are not outlawed as information"; what is forbidden is a count entering as an *automatic* warrant).

## Rows

### Row 1 - `daily/mini_fcl/cycle01/rival#r4` --revises--> `daily/mini_fcl/cycle01/account` (whole contribution)

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/rival` |
| referring record | `r4` (type `commitment`) |
| ref field | `revises` |
| ref verbatim | `ad92700706f3372d` |
| ref grain | artifact |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | none - the ref names the owning contribution, not a record |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | n/a |

Resolver notes (from the importer, verbatim):

- `bare_label_ref`: bare exposed-artifact label with no '#LocalName'; local resolution was tried first, so it resolves to the owning artifact (deviation D2)

**Referring record, verbatim** (`daily/mini_fcl/cycle01/rival`, `commitments[1788:2318]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r4","type":"commitment","text":"Put the specification where the work happens rather than where the talk happens: a checklist inside the cupboard door, taped to the bin lid, on the bathroom mirror, plus one gap-filler rule agreed once — where nothing is written at the spot, the default standard is X.","consequence":"the standard is consultable by whoever is doing the task at the moment they do it, survives schedule changes, and does not require anyone to convene or attend a conversation","revises":["ad92700706f3372d"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`)

*(none: the ref names the owning contribution as a whole; the overlap subject below says what was compared)*

**Referring BODY passages** (overlap subject: the prose fields of every record of `daily/mini_fcl/cycle01/account` (the ref names the contribution, not a record); offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[0:199]` - distinctive tokens `agreement`, `avoidant`, `friend`, `light`, `mostly`, `weekly`
  ```text
  The account on offer separates four features and then works on them mostly through talk and records: write the agreement down, hold a weekly look, ask the avoidant friend what is hard, keep it light.
  ```
- `body[200:352]` - distinctive tokens `asker`, `conversations`, `wrong`
  ```text
  Those moves are not wrong, but they share an assumption worth contesting — that the load should sit in conversations the asker convenes and administers.
  ```
- `body[383:548]` - distinctive tokens `arrangement`, `chore`, `holds`
  ```text
  In a flat of three, nobody holds authority over anybody; any chore arrangement one member designs, records and runs is experienced by the other two as being managed.
  ```
- `body[549:627]` - distinctive tokens `looking`
  ```text
  On that reading, the two headline symptoms stop looking like separate defects.
  ```
- `body[628:838]` - distinctive tokens `agreement`, `enforcement`, `objection`, `talks`
  ```text
  Reinterpreting an agreement later is what enforcement looks like when there is no authority to enforce with; withdrawing from the talks is what objection looks like when there is no comfortable way to voice it.
  ```
- `body[839:1009]` - distinctive tokens `written`
  ```text
  If that framing is even partly right, the goal is not clarity alone but legitimacy — and legitimacy is made by who owns the design, not by how well the design is written.
  ```
- `body[1050:1212]` - distinctive tokens `agree`, `contributions`, `disputes`
  ```text
  Most 'what did we agree' disputes attach to the seams between two people's contributions — I did the counters, you said you'd do the floor, whose job was the hob?
  ```
- `body[1213:1384]` - distinctive tokens `disagree`, `memories`
  ```text
  Give each common area a single owner, answerable end to end, and the seams vanish; inside someone's domain there is nothing left for two honest memories to disagree about.
  ```
- `body[1385:1615]` - distinctive tokens `avoidant`, `friend`
  ```text
  To allocate without a live negotiation the avoidant friend can simply not attend, collect private, asynchronous rankings — message everyone the list of areas and ask which they mind most and least — and match owners to tolerances.
  ```
- `body[1616:1806]` - distinctive tokens `person`, `standard`, `written`
  ```text
  Set one written floor for common areas at a level all three can genuinely accept, not at the cleanest person's preference: a floor set at the highest standard just reproduces the imposition.
  ```
- `body[1807:1904]` - distinctive tokens `answer`
  ```text
  Within a domain the owner may exceed the floor as they please; below it, they answer to the text.
  ```
- `body[1993:2245]` - distinctive tokens `confirmation`, `conversation`
  ```text
  A checklist inside the cupboard door, taped to the bin lid, on the bathroom mirror — counters cleared and wiped, floor swept, bin out — beats a confirmation posted after a conversation, because the artifact does not depend on anyone convening anything.
  ```
- `body[2246:2462]` - distinctive tokens `conversations`, `friend`, `moment`, `schedule`, `standard`
  ```text
  It survives schedule chaos, it can be consulted by whoever is actually doing the task at the moment they do it, and it gives the friend who avoids conversations a way to know and meet the standard without having one.
  ```
- `body[2463:2604]` - distinctive tokens `written`
  ```text
  Add a single gap-filler rule agreed once: where nothing is written at the spot, the default is X. After that, memory has nothing to be about.
  ```
- `body[2606:2635]` - distinctive tokens `third`
  ```text
  Third move: rotate the chair.
  ```
- `body[2636:2907]` - distinctive tokens `asker`, `avoidance`, `holds`, `system`
  ```text
  Whoever convenes, records and adjusts the arrangements holds a kind of office; if that is always the asker, then 'the system' and 'the asker's preferences' blur together, and both the reinterpretations and the avoidance become intelligible as resistance to being clerked.
  ```
- `body[3035:3290]` - distinctive tokens `avoidant`, `changes`, `conversation`, `friend`, `standard`
  ```text
  This changes the recommended conversation with the avoidant friend rather than replacing it: keep it one-on-one and non-accusing, but ask about stakes, not difficulty — do you want the flat at this standard at all, or is that our project being run on you?
  ```
- `body[3291:3390]` - distinctive tokens `lower`
  ```text
  The answers diverge usefully: someone who wants a lower floor needs a trade, not a better-run talk.
  ```
- `body[3463:3674]` - distinctive tokens `avoiding`, `changes`, `conversations`, `enforcement`, `person`, `record`, `started`
  ```text
  If one person simply cares less about cleanliness, no record and no rota changes that, and enforcement aimed at low stakes produces withdrawal — which may be exactly what 'started avoiding the conversations' is.
  ```
- `body[3675:3845]` - distinctive tokens `cleaning`, `lower`
  ```text
  Price the difference instead: a lower common floor; or cleaning load swapped against the admin nobody wants — bills, shopping, landlord calls; or a small rent adjustment.
  ```
- `body[3990:4136]` - distinctive tokens `costs`, `planning`, `schedules`, `weekly`
  ```text
  Honest costs, because the trade is real: whole-domain ownership is less flexible under shifting schedules than the account's weekly swap planning.
  ```
- `body[4137:4307]` - distinctive tokens `person`, `weekly`
  ```text
  Deputy defaults — if the owner is away, the area falls to a named person, never to nobody — and monthly rather than weekly adjustment are partial answers, not a full one.
  ```
- `body[4308:4625]` - distinctive tokens `cause`, `chores`, `conversation`, `friend`
  ```text
  And the rotation doubles as a diagnostic: if the friend re-engages when it is their week in the chair, the withdrawal tracked the structure; if they withdraw even while holding the chair, the cause probably is not the chores at all, and the one-on-one conversation becomes the necessary move rather than a supplement.
  ```
- `body[4627:4882]` - distinctive tokens `conversation`, `exits`, `question`, `record`, `structural`, `written`
  ```text
  What survives from the account on offer: the written record, relocated from the conversation to the site of the work; the periodic look, chaired in rotation; the one-on-one ask, question changed; the caution against over-engineering; the structural exits.
  ```
- `body[4883:5011]` - distinctive tokens `changes`, `convened`
  ```text
  What changes is where the load sits — in ownership, point-of-use specification and office — rather than in better-convened talk.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 2 - `daily/mini_fcl/cycle01/rival#r5` --target--> `daily/mini_fcl/cycle01/account` (whole contribution)

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/rival` |
| referring record | `r5` (type `objection`) |
| ref field | `target` |
| ref verbatim | `ad92700706f3372d` |
| ref grain | artifact |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | none - the ref names the owning contribution, not a record |
| declared_uptake_includes_referring_record | false |
| declared_uptake_includes_target_record | n/a |

Resolver notes (from the importer, verbatim):

- `bare_label_ref`: bare exposed-artifact label with no '#LocalName'; local resolution was tried first, so it resolves to the owning artifact (deviation D2)

**Referring record, verbatim** (`daily/mini_fcl/cycle01/rival`, `commitments[2319:2938]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r5","type":"objection","text":"The input account's standing unilateral confirmations (I've got X, you've got Y), useful as one-off corrections, consolidate the asker's clerk-of-record role when run as a habit; the device that fixes ambiguity can deepen the legitimacy problem that may be driving the withdrawal.","target":["ad92700706f3372d"],"bearing":"this objection is itself criticisable: if the friend's withdrawal has an unrelated cause, the clerk-role reading is wrong and the device is harmless; if the account's own caution about visible apparatus applies to its own records, the objection gains force"}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`)

*(none: the ref names the owning contribution as a whole; the overlap subject below says what was compared)*

**Referring BODY passages** (overlap subject: the prose fields of every record of `daily/mini_fcl/cycle01/account` (the ref names the contribution, not a record); offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[0:199]` - distinctive tokens `agreement`, `avoidant`, `friend`, `light`, `mostly`, `weekly`
  ```text
  The account on offer separates four features and then works on them mostly through talk and records: write the agreement down, hold a weekly look, ask the avoidant friend what is hard, keep it light.
  ```
- `body[200:352]` - distinctive tokens `asker`, `conversations`, `wrong`
  ```text
  Those moves are not wrong, but they share an assumption worth contesting — that the load should sit in conversations the asker convenes and administers.
  ```
- `body[383:548]` - distinctive tokens `arrangement`, `chore`, `holds`
  ```text
  In a flat of three, nobody holds authority over anybody; any chore arrangement one member designs, records and runs is experienced by the other two as being managed.
  ```
- `body[549:627]` - distinctive tokens `looking`
  ```text
  On that reading, the two headline symptoms stop looking like separate defects.
  ```
- `body[628:838]` - distinctive tokens `agreement`, `enforcement`, `objection`, `talks`
  ```text
  Reinterpreting an agreement later is what enforcement looks like when there is no authority to enforce with; withdrawing from the talks is what objection looks like when there is no comfortable way to voice it.
  ```
- `body[839:1009]` - distinctive tokens `written`
  ```text
  If that framing is even partly right, the goal is not clarity alone but legitimacy — and legitimacy is made by who owns the design, not by how well the design is written.
  ```
- `body[1050:1212]` - distinctive tokens `agree`, `contributions`, `disputes`
  ```text
  Most 'what did we agree' disputes attach to the seams between two people's contributions — I did the counters, you said you'd do the floor, whose job was the hob?
  ```
- `body[1213:1384]` - distinctive tokens `disagree`, `memories`
  ```text
  Give each common area a single owner, answerable end to end, and the seams vanish; inside someone's domain there is nothing left for two honest memories to disagree about.
  ```
- `body[1385:1615]` - distinctive tokens `avoidant`, `friend`
  ```text
  To allocate without a live negotiation the avoidant friend can simply not attend, collect private, asynchronous rankings — message everyone the list of areas and ask which they mind most and least — and match owners to tolerances.
  ```
- `body[1616:1806]` - distinctive tokens `person`, `standard`, `written`
  ```text
  Set one written floor for common areas at a level all three can genuinely accept, not at the cleanest person's preference: a floor set at the highest standard just reproduces the imposition.
  ```
- `body[1807:1904]` - distinctive tokens `answer`
  ```text
  Within a domain the owner may exceed the floor as they please; below it, they answer to the text.
  ```
- `body[1993:2245]` - distinctive tokens `confirmation`, `conversation`
  ```text
  A checklist inside the cupboard door, taped to the bin lid, on the bathroom mirror — counters cleared and wiped, floor swept, bin out — beats a confirmation posted after a conversation, because the artifact does not depend on anyone convening anything.
  ```
- `body[2246:2462]` - distinctive tokens `conversations`, `friend`, `moment`, `schedule`, `standard`
  ```text
  It survives schedule chaos, it can be consulted by whoever is actually doing the task at the moment they do it, and it gives the friend who avoids conversations a way to know and meet the standard without having one.
  ```
- `body[2463:2604]` - distinctive tokens `written`
  ```text
  Add a single gap-filler rule agreed once: where nothing is written at the spot, the default is X. After that, memory has nothing to be about.
  ```
- `body[2606:2635]` - distinctive tokens `third`
  ```text
  Third move: rotate the chair.
  ```
- `body[2636:2907]` - distinctive tokens `asker`, `avoidance`, `holds`, `system`
  ```text
  Whoever convenes, records and adjusts the arrangements holds a kind of office; if that is always the asker, then 'the system' and 'the asker's preferences' blur together, and both the reinterpretations and the avoidance become intelligible as resistance to being clerked.
  ```
- `body[3035:3290]` - distinctive tokens `avoidant`, `changes`, `conversation`, `friend`, `standard`
  ```text
  This changes the recommended conversation with the avoidant friend rather than replacing it: keep it one-on-one and non-accusing, but ask about stakes, not difficulty — do you want the flat at this standard at all, or is that our project being run on you?
  ```
- `body[3291:3390]` - distinctive tokens `lower`
  ```text
  The answers diverge usefully: someone who wants a lower floor needs a trade, not a better-run talk.
  ```
- `body[3463:3674]` - distinctive tokens `avoiding`, `changes`, `conversations`, `enforcement`, `person`, `record`, `started`
  ```text
  If one person simply cares less about cleanliness, no record and no rota changes that, and enforcement aimed at low stakes produces withdrawal — which may be exactly what 'started avoiding the conversations' is.
  ```
- `body[3675:3845]` - distinctive tokens `cleaning`, `lower`
  ```text
  Price the difference instead: a lower common floor; or cleaning load swapped against the admin nobody wants — bills, shopping, landlord calls; or a small rent adjustment.
  ```
- `body[3990:4136]` - distinctive tokens `costs`, `planning`, `schedules`, `weekly`
  ```text
  Honest costs, because the trade is real: whole-domain ownership is less flexible under shifting schedules than the account's weekly swap planning.
  ```
- `body[4137:4307]` - distinctive tokens `person`, `weekly`
  ```text
  Deputy defaults — if the owner is away, the area falls to a named person, never to nobody — and monthly rather than weekly adjustment are partial answers, not a full one.
  ```
- `body[4308:4625]` - distinctive tokens `cause`, `chores`, `conversation`, `friend`
  ```text
  And the rotation doubles as a diagnostic: if the friend re-engages when it is their week in the chair, the withdrawal tracked the structure; if they withdraw even while holding the chair, the cause probably is not the chores at all, and the one-on-one conversation becomes the necessary move rather than a supplement.
  ```
- `body[4627:4882]` - distinctive tokens `conversation`, `exits`, `question`, `record`, `structural`, `written`
  ```text
  What survives from the account on offer: the written record, relocated from the conversation to the site of the work; the periodic look, chaired in rotation; the one-on-one ask, question changed; the caution against over-engineering; the structural exits.
  ```
- `body[4883:5011]` - distinctive tokens `changes`, `convened`
  ```text
  What changes is where the load sits — in ownership, point-of-use specification and office — rather than in better-convened talk.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 3 - `daily/mini_fcl/cycle01/rival#r7` --target--> `daily/mini_fcl/cycle01/account` (whole contribution)

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/rival` |
| referring record | `r7` (type `use`) |
| ref field | `target` |
| ref verbatim | `ad92700706f3372d` |
| ref grain | artifact |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | none - the ref names the owning contribution, not a record |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | n/a |

Resolver notes (from the importer, verbatim):

- `bare_label_ref`: bare exposed-artifact label with no '#LocalName'; local resolution was tried first, so it resolves to the owning artifact (deviation D2)

**Referring record, verbatim** (`daily/mini_fcl/cycle01/rival`, `commitments[3431:3939]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r7","type":"use","text":"Take up the input account's one-on-one, non-accusing conversation with the avoidant friend, but change the question from difficulty to stakes: not what makes these conversations hard, but whether they want the flat at this standard at all or whether it is the other two's project being run on them.","target":["ad92700706f3372d"],"depends":["r1"],"consequence":"a stakes answer calls for a trade (r8); a difficulty answer calls for changes to the talk's format and character"}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`)

*(none: the ref names the owning contribution as a whole; the overlap subject below says what was compared)*

**Referring BODY passages** (overlap subject: the prose fields of every record of `daily/mini_fcl/cycle01/account` (the ref names the contribution, not a record); offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[0:199]` - distinctive tokens `agreement`, `avoidant`, `friend`, `light`, `mostly`, `weekly`
  ```text
  The account on offer separates four features and then works on them mostly through talk and records: write the agreement down, hold a weekly look, ask the avoidant friend what is hard, keep it light.
  ```
- `body[200:352]` - distinctive tokens `asker`, `conversations`, `wrong`
  ```text
  Those moves are not wrong, but they share an assumption worth contesting — that the load should sit in conversations the asker convenes and administers.
  ```
- `body[383:548]` - distinctive tokens `arrangement`, `chore`, `holds`
  ```text
  In a flat of three, nobody holds authority over anybody; any chore arrangement one member designs, records and runs is experienced by the other two as being managed.
  ```
- `body[549:627]` - distinctive tokens `looking`
  ```text
  On that reading, the two headline symptoms stop looking like separate defects.
  ```
- `body[628:838]` - distinctive tokens `agreement`, `enforcement`, `objection`, `talks`
  ```text
  Reinterpreting an agreement later is what enforcement looks like when there is no authority to enforce with; withdrawing from the talks is what objection looks like when there is no comfortable way to voice it.
  ```
- `body[839:1009]` - distinctive tokens `written`
  ```text
  If that framing is even partly right, the goal is not clarity alone but legitimacy — and legitimacy is made by who owns the design, not by how well the design is written.
  ```
- `body[1050:1212]` - distinctive tokens `agree`, `contributions`, `disputes`
  ```text
  Most 'what did we agree' disputes attach to the seams between two people's contributions — I did the counters, you said you'd do the floor, whose job was the hob?
  ```
- `body[1213:1384]` - distinctive tokens `disagree`, `memories`
  ```text
  Give each common area a single owner, answerable end to end, and the seams vanish; inside someone's domain there is nothing left for two honest memories to disagree about.
  ```
- `body[1385:1615]` - distinctive tokens `avoidant`, `friend`
  ```text
  To allocate without a live negotiation the avoidant friend can simply not attend, collect private, asynchronous rankings — message everyone the list of areas and ask which they mind most and least — and match owners to tolerances.
  ```
- `body[1616:1806]` - distinctive tokens `person`, `standard`, `written`
  ```text
  Set one written floor for common areas at a level all three can genuinely accept, not at the cleanest person's preference: a floor set at the highest standard just reproduces the imposition.
  ```
- `body[1807:1904]` - distinctive tokens `answer`
  ```text
  Within a domain the owner may exceed the floor as they please; below it, they answer to the text.
  ```
- `body[1993:2245]` - distinctive tokens `confirmation`, `conversation`
  ```text
  A checklist inside the cupboard door, taped to the bin lid, on the bathroom mirror — counters cleared and wiped, floor swept, bin out — beats a confirmation posted after a conversation, because the artifact does not depend on anyone convening anything.
  ```
- `body[2246:2462]` - distinctive tokens `conversations`, `friend`, `moment`, `schedule`, `standard`
  ```text
  It survives schedule chaos, it can be consulted by whoever is actually doing the task at the moment they do it, and it gives the friend who avoids conversations a way to know and meet the standard without having one.
  ```
- `body[2463:2604]` - distinctive tokens `written`
  ```text
  Add a single gap-filler rule agreed once: where nothing is written at the spot, the default is X. After that, memory has nothing to be about.
  ```
- `body[2606:2635]` - distinctive tokens `third`
  ```text
  Third move: rotate the chair.
  ```
- `body[2636:2907]` - distinctive tokens `asker`, `avoidance`, `holds`, `system`
  ```text
  Whoever convenes, records and adjusts the arrangements holds a kind of office; if that is always the asker, then 'the system' and 'the asker's preferences' blur together, and both the reinterpretations and the avoidance become intelligible as resistance to being clerked.
  ```
- `body[3035:3290]` - distinctive tokens `avoidant`, `changes`, `conversation`, `friend`, `standard`
  ```text
  This changes the recommended conversation with the avoidant friend rather than replacing it: keep it one-on-one and non-accusing, but ask about stakes, not difficulty — do you want the flat at this standard at all, or is that our project being run on you?
  ```
- `body[3291:3390]` - distinctive tokens `lower`
  ```text
  The answers diverge usefully: someone who wants a lower floor needs a trade, not a better-run talk.
  ```
- `body[3463:3674]` - distinctive tokens `avoiding`, `changes`, `conversations`, `enforcement`, `person`, `record`, `started`
  ```text
  If one person simply cares less about cleanliness, no record and no rota changes that, and enforcement aimed at low stakes produces withdrawal — which may be exactly what 'started avoiding the conversations' is.
  ```
- `body[3675:3845]` - distinctive tokens `cleaning`, `lower`
  ```text
  Price the difference instead: a lower common floor; or cleaning load swapped against the admin nobody wants — bills, shopping, landlord calls; or a small rent adjustment.
  ```
- `body[3990:4136]` - distinctive tokens `costs`, `planning`, `schedules`, `weekly`
  ```text
  Honest costs, because the trade is real: whole-domain ownership is less flexible under shifting schedules than the account's weekly swap planning.
  ```
- `body[4137:4307]` - distinctive tokens `person`, `weekly`
  ```text
  Deputy defaults — if the owner is away, the area falls to a named person, never to nobody — and monthly rather than weekly adjustment are partial answers, not a full one.
  ```
- `body[4308:4625]` - distinctive tokens `cause`, `chores`, `conversation`, `friend`
  ```text
  And the rotation doubles as a diagnostic: if the friend re-engages when it is their week in the chair, the withdrawal tracked the structure; if they withdraw even while holding the chair, the cause probably is not the chores at all, and the one-on-one conversation becomes the necessary move rather than a supplement.
  ```
- `body[4627:4882]` - distinctive tokens `conversation`, `exits`, `question`, `record`, `structural`, `written`
  ```text
  What survives from the account on offer: the written record, relocated from the conversation to the site of the work; the periodic look, chaired in rotation; the one-on-one ask, question changed; the caution against over-engineering; the structural exits.
  ```
- `body[4883:5011]` - distinctive tokens `changes`, `convened`
  ```text
  What changes is where the load sits — in ownership, point-of-use specification and office — rather than in better-convened talk.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 4 - `daily/mini_fcl/cycle01/rival#r8` --mentions--> `daily/mini_fcl/cycle01/account` (whole contribution)

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/rival` |
| referring record | `r8` (type `commitment`) |
| ref field | `mentions` |
| ref verbatim | `ad92700706f3372d` |
| ref grain | artifact |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | none - the ref names the owning contribution, not a record |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | n/a |

Resolver notes (from the importer, verbatim):

- `bare_label_ref`: bare exposed-artifact label with no '#LocalName'; local resolution was tried first, so it resolves to the owning artifact (deviation D2)

**Referring record, verbatim** (`daily/mini_fcl/cycle01/rival`, `commitments[3940:4468]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r8","type":"commitment","text":"Where tolerances genuinely differ, trade across domains rather than enforce uniform standards: a lower common floor; or cleaning load swapped against the admin nobody wants (bills, shopping, landlord calls); or a small rent adjustment.","consequence":"a low-stakes member stops being an enforcement target, which is one plausible reading of the withdrawal — though only a reading; the material does not say why the friend avoids the talks","depends":["r1"],"mentions":["ad92700706f3372d"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`)

*(none: the ref names the owning contribution as a whole; the overlap subject below says what was compared)*

**Referring BODY passages** (overlap subject: the prose fields of every record of `daily/mini_fcl/cycle01/account` (the ref names the contribution, not a record); offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[0:199]` - distinctive tokens `agreement`, `avoidant`, `friend`, `light`, `mostly`, `weekly`
  ```text
  The account on offer separates four features and then works on them mostly through talk and records: write the agreement down, hold a weekly look, ask the avoidant friend what is hard, keep it light.
  ```
- `body[200:352]` - distinctive tokens `asker`, `conversations`, `wrong`
  ```text
  Those moves are not wrong, but they share an assumption worth contesting — that the load should sit in conversations the asker convenes and administers.
  ```
- `body[383:548]` - distinctive tokens `arrangement`, `chore`, `holds`
  ```text
  In a flat of three, nobody holds authority over anybody; any chore arrangement one member designs, records and runs is experienced by the other two as being managed.
  ```
- `body[549:627]` - distinctive tokens `looking`
  ```text
  On that reading, the two headline symptoms stop looking like separate defects.
  ```
- `body[628:838]` - distinctive tokens `agreement`, `enforcement`, `objection`, `talks`
  ```text
  Reinterpreting an agreement later is what enforcement looks like when there is no authority to enforce with; withdrawing from the talks is what objection looks like when there is no comfortable way to voice it.
  ```
- `body[839:1009]` - distinctive tokens `written`
  ```text
  If that framing is even partly right, the goal is not clarity alone but legitimacy — and legitimacy is made by who owns the design, not by how well the design is written.
  ```
- `body[1050:1212]` - distinctive tokens `agree`, `contributions`, `disputes`
  ```text
  Most 'what did we agree' disputes attach to the seams between two people's contributions — I did the counters, you said you'd do the floor, whose job was the hob?
  ```
- `body[1213:1384]` - distinctive tokens `disagree`, `memories`
  ```text
  Give each common area a single owner, answerable end to end, and the seams vanish; inside someone's domain there is nothing left for two honest memories to disagree about.
  ```
- `body[1385:1615]` - distinctive tokens `avoidant`, `friend`
  ```text
  To allocate without a live negotiation the avoidant friend can simply not attend, collect private, asynchronous rankings — message everyone the list of areas and ask which they mind most and least — and match owners to tolerances.
  ```
- `body[1616:1806]` - distinctive tokens `person`, `standard`, `written`
  ```text
  Set one written floor for common areas at a level all three can genuinely accept, not at the cleanest person's preference: a floor set at the highest standard just reproduces the imposition.
  ```
- `body[1807:1904]` - distinctive tokens `answer`
  ```text
  Within a domain the owner may exceed the floor as they please; below it, they answer to the text.
  ```
- `body[1993:2245]` - distinctive tokens `confirmation`, `conversation`
  ```text
  A checklist inside the cupboard door, taped to the bin lid, on the bathroom mirror — counters cleared and wiped, floor swept, bin out — beats a confirmation posted after a conversation, because the artifact does not depend on anyone convening anything.
  ```
- `body[2246:2462]` - distinctive tokens `conversations`, `friend`, `moment`, `schedule`, `standard`
  ```text
  It survives schedule chaos, it can be consulted by whoever is actually doing the task at the moment they do it, and it gives the friend who avoids conversations a way to know and meet the standard without having one.
  ```
- `body[2463:2604]` - distinctive tokens `written`
  ```text
  Add a single gap-filler rule agreed once: where nothing is written at the spot, the default is X. After that, memory has nothing to be about.
  ```
- `body[2606:2635]` - distinctive tokens `third`
  ```text
  Third move: rotate the chair.
  ```
- `body[2636:2907]` - distinctive tokens `asker`, `avoidance`, `holds`, `system`
  ```text
  Whoever convenes, records and adjusts the arrangements holds a kind of office; if that is always the asker, then 'the system' and 'the asker's preferences' blur together, and both the reinterpretations and the avoidance become intelligible as resistance to being clerked.
  ```
- `body[3035:3290]` - distinctive tokens `avoidant`, `changes`, `conversation`, `friend`, `standard`
  ```text
  This changes the recommended conversation with the avoidant friend rather than replacing it: keep it one-on-one and non-accusing, but ask about stakes, not difficulty — do you want the flat at this standard at all, or is that our project being run on you?
  ```
- `body[3291:3390]` - distinctive tokens `lower`
  ```text
  The answers diverge usefully: someone who wants a lower floor needs a trade, not a better-run talk.
  ```
- `body[3463:3674]` - distinctive tokens `avoiding`, `changes`, `conversations`, `enforcement`, `person`, `record`, `started`
  ```text
  If one person simply cares less about cleanliness, no record and no rota changes that, and enforcement aimed at low stakes produces withdrawal — which may be exactly what 'started avoiding the conversations' is.
  ```
- `body[3675:3845]` - distinctive tokens `cleaning`, `lower`
  ```text
  Price the difference instead: a lower common floor; or cleaning load swapped against the admin nobody wants — bills, shopping, landlord calls; or a small rent adjustment.
  ```
- `body[3990:4136]` - distinctive tokens `costs`, `planning`, `schedules`, `weekly`
  ```text
  Honest costs, because the trade is real: whole-domain ownership is less flexible under shifting schedules than the account's weekly swap planning.
  ```
- `body[4137:4307]` - distinctive tokens `person`, `weekly`
  ```text
  Deputy defaults — if the owner is away, the area falls to a named person, never to nobody — and monthly rather than weekly adjustment are partial answers, not a full one.
  ```
- `body[4308:4625]` - distinctive tokens `cause`, `chores`, `conversation`, `friend`
  ```text
  And the rotation doubles as a diagnostic: if the friend re-engages when it is their week in the chair, the withdrawal tracked the structure; if they withdraw even while holding the chair, the cause probably is not the chores at all, and the one-on-one conversation becomes the necessary move rather than a supplement.
  ```
- `body[4627:4882]` - distinctive tokens `conversation`, `exits`, `question`, `record`, `structural`, `written`
  ```text
  What survives from the account on offer: the written record, relocated from the conversation to the site of the work; the periodic look, chaired in rotation; the one-on-one ask, question changed; the caution against over-engineering; the structural exits.
  ```
- `body[4883:5011]` - distinctive tokens `changes`, `convened`
  ```text
  What changes is where the load sits — in ownership, point-of-use specification and office — rather than in better-convened talk.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 5 - `daily/mini_fcl/cycle01/rival#r10` --target--> `daily/mini_fcl/cycle01/account` (whole contribution)

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/rival` |
| referring record | `r10` (type `use`) |
| ref field | `target` |
| ref verbatim | `ad92700706f3372d` |
| ref grain | artifact |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | none - the ref names the owning contribution, not a record |
| declared_uptake_includes_referring_record | true |
| declared_uptake_includes_target_record | n/a |

Resolver notes (from the importer, verbatim):

- `bare_label_ref`: bare exposed-artifact label with no '#LocalName'; local resolution was tried first, so it resolves to the owning artifact (deviation D2)

**Referring record, verbatim** (`daily/mini_fcl/cycle01/rival`, `commitments[4953:5317]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r10","type":"use","text":"Take up the input account's structural exits (a cleaner split three ways, shrinking the shared surface, renegotiating whether the living arrangement is working) as legitimate endpoints rather than failures, together with its caution against over-engineering; both stay live if the trades in r8 fail.","target":["ad92700706f3372d"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`)

*(none: the ref names the owning contribution as a whole; the overlap subject below says what was compared)*

**Referring BODY passages** (overlap subject: the prose fields of every record of `daily/mini_fcl/cycle01/account` (the ref names the contribution, not a record); offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[0:199]` - distinctive tokens `agreement`, `avoidant`, `friend`, `light`, `mostly`, `weekly`
  ```text
  The account on offer separates four features and then works on them mostly through talk and records: write the agreement down, hold a weekly look, ask the avoidant friend what is hard, keep it light.
  ```
- `body[200:352]` - distinctive tokens `asker`, `conversations`, `wrong`
  ```text
  Those moves are not wrong, but they share an assumption worth contesting — that the load should sit in conversations the asker convenes and administers.
  ```
- `body[383:548]` - distinctive tokens `arrangement`, `chore`, `holds`
  ```text
  In a flat of three, nobody holds authority over anybody; any chore arrangement one member designs, records and runs is experienced by the other two as being managed.
  ```
- `body[549:627]` - distinctive tokens `looking`
  ```text
  On that reading, the two headline symptoms stop looking like separate defects.
  ```
- `body[628:838]` - distinctive tokens `agreement`, `enforcement`, `objection`, `talks`
  ```text
  Reinterpreting an agreement later is what enforcement looks like when there is no authority to enforce with; withdrawing from the talks is what objection looks like when there is no comfortable way to voice it.
  ```
- `body[839:1009]` - distinctive tokens `written`
  ```text
  If that framing is even partly right, the goal is not clarity alone but legitimacy — and legitimacy is made by who owns the design, not by how well the design is written.
  ```
- `body[1050:1212]` - distinctive tokens `agree`, `contributions`, `disputes`
  ```text
  Most 'what did we agree' disputes attach to the seams between two people's contributions — I did the counters, you said you'd do the floor, whose job was the hob?
  ```
- `body[1213:1384]` - distinctive tokens `disagree`, `memories`
  ```text
  Give each common area a single owner, answerable end to end, and the seams vanish; inside someone's domain there is nothing left for two honest memories to disagree about.
  ```
- `body[1385:1615]` - distinctive tokens `avoidant`, `friend`
  ```text
  To allocate without a live negotiation the avoidant friend can simply not attend, collect private, asynchronous rankings — message everyone the list of areas and ask which they mind most and least — and match owners to tolerances.
  ```
- `body[1616:1806]` - distinctive tokens `person`, `standard`, `written`
  ```text
  Set one written floor for common areas at a level all three can genuinely accept, not at the cleanest person's preference: a floor set at the highest standard just reproduces the imposition.
  ```
- `body[1807:1904]` - distinctive tokens `answer`
  ```text
  Within a domain the owner may exceed the floor as they please; below it, they answer to the text.
  ```
- `body[1993:2245]` - distinctive tokens `confirmation`, `conversation`
  ```text
  A checklist inside the cupboard door, taped to the bin lid, on the bathroom mirror — counters cleared and wiped, floor swept, bin out — beats a confirmation posted after a conversation, because the artifact does not depend on anyone convening anything.
  ```
- `body[2246:2462]` - distinctive tokens `conversations`, `friend`, `moment`, `schedule`, `standard`
  ```text
  It survives schedule chaos, it can be consulted by whoever is actually doing the task at the moment they do it, and it gives the friend who avoids conversations a way to know and meet the standard without having one.
  ```
- `body[2463:2604]` - distinctive tokens `written`
  ```text
  Add a single gap-filler rule agreed once: where nothing is written at the spot, the default is X. After that, memory has nothing to be about.
  ```
- `body[2606:2635]` - distinctive tokens `third`
  ```text
  Third move: rotate the chair.
  ```
- `body[2636:2907]` - distinctive tokens `asker`, `avoidance`, `holds`, `system`
  ```text
  Whoever convenes, records and adjusts the arrangements holds a kind of office; if that is always the asker, then 'the system' and 'the asker's preferences' blur together, and both the reinterpretations and the avoidance become intelligible as resistance to being clerked.
  ```
- `body[3035:3290]` - distinctive tokens `avoidant`, `changes`, `conversation`, `friend`, `standard`
  ```text
  This changes the recommended conversation with the avoidant friend rather than replacing it: keep it one-on-one and non-accusing, but ask about stakes, not difficulty — do you want the flat at this standard at all, or is that our project being run on you?
  ```
- `body[3291:3390]` - distinctive tokens `lower`
  ```text
  The answers diverge usefully: someone who wants a lower floor needs a trade, not a better-run talk.
  ```
- `body[3463:3674]` - distinctive tokens `avoiding`, `changes`, `conversations`, `enforcement`, `person`, `record`, `started`
  ```text
  If one person simply cares less about cleanliness, no record and no rota changes that, and enforcement aimed at low stakes produces withdrawal — which may be exactly what 'started avoiding the conversations' is.
  ```
- `body[3675:3845]` - distinctive tokens `cleaning`, `lower`
  ```text
  Price the difference instead: a lower common floor; or cleaning load swapped against the admin nobody wants — bills, shopping, landlord calls; or a small rent adjustment.
  ```
- `body[3990:4136]` - distinctive tokens `costs`, `planning`, `schedules`, `weekly`
  ```text
  Honest costs, because the trade is real: whole-domain ownership is less flexible under shifting schedules than the account's weekly swap planning.
  ```
- `body[4137:4307]` - distinctive tokens `person`, `weekly`
  ```text
  Deputy defaults — if the owner is away, the area falls to a named person, never to nobody — and monthly rather than weekly adjustment are partial answers, not a full one.
  ```
- `body[4308:4625]` - distinctive tokens `cause`, `chores`, `conversation`, `friend`
  ```text
  And the rotation doubles as a diagnostic: if the friend re-engages when it is their week in the chair, the withdrawal tracked the structure; if they withdraw even while holding the chair, the cause probably is not the chores at all, and the one-on-one conversation becomes the necessary move rather than a supplement.
  ```
- `body[4627:4882]` - distinctive tokens `conversation`, `exits`, `question`, `record`, `structural`, `written`
  ```text
  What survives from the account on offer: the written record, relocated from the conversation to the site of the work; the periodic look, chaired in rotation; the one-on-one ask, question changed; the caution against over-engineering; the structural exits.
  ```
- `body[4883:5011]` - distinctive tokens `changes`, `convened`
  ```text
  What changes is where the load sits — in ownership, point-of-use specification and office — rather than in better-convened talk.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

### Row 6 - `daily/mini_fcl/cycle01/rival#r11` --mentions--> `daily/mini_fcl/cycle01/account` (whole contribution)

| field | value |
|---|---|
| referring coordinate | `daily/mini_fcl/cycle01/rival` |
| referring record | `r11` (type `problem`) |
| ref field | `mentions` |
| ref verbatim | `ad92700706f3372d` |
| ref grain | artifact |
| resolved target coordinate | `daily/mini_fcl/cycle01/account` |
| resolved target record | none - the ref names the owning contribution, not a record |
| declared_uptake_includes_referring_record | false |
| declared_uptake_includes_target_record | n/a |

Resolver notes (from the importer, verbatim):

- `bare_label_ref`: bare exposed-artifact label with no '#LocalName'; local resolution was tried first, so it resolves to the owning artifact (deviation D2)

**Referring record, verbatim** (`daily/mini_fcl/cycle01/rival`, `commitments[5318:5691]`, code point offsets into the decoded `commitments` string)

```json
{"id":"r11","type":"problem","text":"This design trades flexibility for clarity: whole-domain ownership is more brittle under shifting schedules than the input account's weekly swap planning. Deputy defaults (a named fallback per area when the owner is away) and monthly rather than weekly adjustment are partial answers, not a resolution.","mentions":["ad92700706f3372d"]}
```

**Resolved target record, verbatim** (`daily/mini_fcl/cycle01/account`)

*(none: the ref names the owning contribution as a whole; the overlap subject below says what was compared)*

**Referring BODY passages** (overlap subject: the prose fields of every record of `daily/mini_fcl/cycle01/account` (the ref names the contribution, not a record); offsets are code point offsets into the decoded `body` string). The listed passages are a finding aid, not a search space: root may cite any passage of either contribution, including one the rule did not surface.

- `body[0:199]` - distinctive tokens `agreement`, `avoidant`, `friend`, `light`, `mostly`, `weekly`
  ```text
  The account on offer separates four features and then works on them mostly through talk and records: write the agreement down, hold a weekly look, ask the avoidant friend what is hard, keep it light.
  ```
- `body[200:352]` - distinctive tokens `asker`, `conversations`, `wrong`
  ```text
  Those moves are not wrong, but they share an assumption worth contesting — that the load should sit in conversations the asker convenes and administers.
  ```
- `body[383:548]` - distinctive tokens `arrangement`, `chore`, `holds`
  ```text
  In a flat of three, nobody holds authority over anybody; any chore arrangement one member designs, records and runs is experienced by the other two as being managed.
  ```
- `body[549:627]` - distinctive tokens `looking`
  ```text
  On that reading, the two headline symptoms stop looking like separate defects.
  ```
- `body[628:838]` - distinctive tokens `agreement`, `enforcement`, `objection`, `talks`
  ```text
  Reinterpreting an agreement later is what enforcement looks like when there is no authority to enforce with; withdrawing from the talks is what objection looks like when there is no comfortable way to voice it.
  ```
- `body[839:1009]` - distinctive tokens `written`
  ```text
  If that framing is even partly right, the goal is not clarity alone but legitimacy — and legitimacy is made by who owns the design, not by how well the design is written.
  ```
- `body[1050:1212]` - distinctive tokens `agree`, `contributions`, `disputes`
  ```text
  Most 'what did we agree' disputes attach to the seams between two people's contributions — I did the counters, you said you'd do the floor, whose job was the hob?
  ```
- `body[1213:1384]` - distinctive tokens `disagree`, `memories`
  ```text
  Give each common area a single owner, answerable end to end, and the seams vanish; inside someone's domain there is nothing left for two honest memories to disagree about.
  ```
- `body[1385:1615]` - distinctive tokens `avoidant`, `friend`
  ```text
  To allocate without a live negotiation the avoidant friend can simply not attend, collect private, asynchronous rankings — message everyone the list of areas and ask which they mind most and least — and match owners to tolerances.
  ```
- `body[1616:1806]` - distinctive tokens `person`, `standard`, `written`
  ```text
  Set one written floor for common areas at a level all three can genuinely accept, not at the cleanest person's preference: a floor set at the highest standard just reproduces the imposition.
  ```
- `body[1807:1904]` - distinctive tokens `answer`
  ```text
  Within a domain the owner may exceed the floor as they please; below it, they answer to the text.
  ```
- `body[1993:2245]` - distinctive tokens `confirmation`, `conversation`
  ```text
  A checklist inside the cupboard door, taped to the bin lid, on the bathroom mirror — counters cleared and wiped, floor swept, bin out — beats a confirmation posted after a conversation, because the artifact does not depend on anyone convening anything.
  ```
- `body[2246:2462]` - distinctive tokens `conversations`, `friend`, `moment`, `schedule`, `standard`
  ```text
  It survives schedule chaos, it can be consulted by whoever is actually doing the task at the moment they do it, and it gives the friend who avoids conversations a way to know and meet the standard without having one.
  ```
- `body[2463:2604]` - distinctive tokens `written`
  ```text
  Add a single gap-filler rule agreed once: where nothing is written at the spot, the default is X. After that, memory has nothing to be about.
  ```
- `body[2606:2635]` - distinctive tokens `third`
  ```text
  Third move: rotate the chair.
  ```
- `body[2636:2907]` - distinctive tokens `asker`, `avoidance`, `holds`, `system`
  ```text
  Whoever convenes, records and adjusts the arrangements holds a kind of office; if that is always the asker, then 'the system' and 'the asker's preferences' blur together, and both the reinterpretations and the avoidance become intelligible as resistance to being clerked.
  ```
- `body[3035:3290]` - distinctive tokens `avoidant`, `changes`, `conversation`, `friend`, `standard`
  ```text
  This changes the recommended conversation with the avoidant friend rather than replacing it: keep it one-on-one and non-accusing, but ask about stakes, not difficulty — do you want the flat at this standard at all, or is that our project being run on you?
  ```
- `body[3291:3390]` - distinctive tokens `lower`
  ```text
  The answers diverge usefully: someone who wants a lower floor needs a trade, not a better-run talk.
  ```
- `body[3463:3674]` - distinctive tokens `avoiding`, `changes`, `conversations`, `enforcement`, `person`, `record`, `started`
  ```text
  If one person simply cares less about cleanliness, no record and no rota changes that, and enforcement aimed at low stakes produces withdrawal — which may be exactly what 'started avoiding the conversations' is.
  ```
- `body[3675:3845]` - distinctive tokens `cleaning`, `lower`
  ```text
  Price the difference instead: a lower common floor; or cleaning load swapped against the admin nobody wants — bills, shopping, landlord calls; or a small rent adjustment.
  ```
- `body[3990:4136]` - distinctive tokens `costs`, `planning`, `schedules`, `weekly`
  ```text
  Honest costs, because the trade is real: whole-domain ownership is less flexible under shifting schedules than the account's weekly swap planning.
  ```
- `body[4137:4307]` - distinctive tokens `person`, `weekly`
  ```text
  Deputy defaults — if the owner is away, the area falls to a named person, never to nobody — and monthly rather than weekly adjustment are partial answers, not a full one.
  ```
- `body[4308:4625]` - distinctive tokens `cause`, `chores`, `conversation`, `friend`
  ```text
  And the rotation doubles as a diagnostic: if the friend re-engages when it is their week in the chair, the withdrawal tracked the structure; if they withdraw even while holding the chair, the cause probably is not the chores at all, and the one-on-one conversation becomes the necessary move rather than a supplement.
  ```
- `body[4627:4882]` - distinctive tokens `conversation`, `exits`, `question`, `record`, `structural`, `written`
  ```text
  What survives from the account on offer: the written record, relocated from the conversation to the site of the work; the periodic look, chaired in rotation; the one-on-one ask, question changed; the caution against over-engineering; the structural exits.
  ```
- `body[4883:5011]` - distinctive tokens `changes`, `convened`
  ```text
  What changes is where the load sits — in ownership, point-of-use specification and office — rather than in better-convened talk.
  ```

**Reserved for root - left empty by the instrument**

An empty cell is an **unread row**, not a reading of `unresolved`. See the Method block for the suggested `root_reading` vocabulary, which is a suggestion and not a closed single-valued enum.

| root_reading | root_passage_cited | root_notes | root_initials_date |
|---|---|---|---|
|  |  |  |  |

## Declared uptake versus records present

### `daily/mini_fcl/cycle01/account`

- commitment surface: `read_fcl1`
- records present (12): `r1`, `r2`, `r3`, `r4`, `r5`, `r6`, `r7`, `r8`, `r9`, `r10`, `r11`, `r12`
- declared `uptake` (5): `r2`, `r4`, `r6`, `r8`, `r12`
- records in uptake (5): `r2`, `r4`, `r6`, `r8`, `r12`
- records omitted from uptake (7): `r1`, `r3`, `r5`, `r7`, `r9`, `r10`, `r11`
- uptake entries naming nothing (0): *none*
- uptake entries naming another document (0): *none*
- uptake entries naming this contribution, not one of its records (0): *none*

The three buckets above are disjoint and, together with the records of this document that the list does name, exhaust `uptake`: a ref resolves to nothing, to another document, to this contribution as a whole, or to one of this document's own records.
An omission from `uptake` is a fact about the declaration, not a defect and not a withdrawal. `uptake` "is a local claim about standing, not a harness verdict or a truth label" (FCL-1 proposition).

### `daily/mini_fcl/cycle01/rival`

- commitment surface: `read_fcl1`
- records present (13): `r1`, `r2`, `r3`, `r4`, `r5`, `r6`, `r7`, `r8`, `r9`, `r10`, `r11`, `r12`, `r13`
- declared `uptake` (7): `r3`, `r4`, `r6`, `r7`, `r8`, `r9`, `r10`
- records in uptake (7): `r3`, `r4`, `r6`, `r7`, `r8`, `r9`, `r10`
- records omitted from uptake (6): `r1`, `r2`, `r5`, `r11`, `r12`, `r13`
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

*No unresolved ref in this scope.*

## Files read

Every byte this instrument read, with its sha256. Nothing under the occurrence was written.

| path | sha256 |
|---|---|
| `artifacts/daily/bare/cycle01/answer.json` | `5d22c22df477cba40210537253c905b6d962b9d0a7c8c93589f3d8add529c64e` |
| `artifacts/daily/mini_fcl/cycle01/account.json` | `47f1448f11a7fe22af3d5ce14e965390b2ca6e0aff867962319f68acec12ee71` |
| `artifacts/daily/mini_fcl/cycle01/rival.json` | `2e6699a1fb6a43d2e024223f2a1b6fc0ac52292e221b9344648f12f42bccf64b` |
| `artifacts/daily/mini_prose/cycle01/account.json` | `d21296d960f2d1b8dd853299caba7bdcb816cc8612e02c11eca4ca35c16e9213` |
| `artifacts/daily/mini_prose/cycle01/carry.json` | `92bb3d68e3e8222a659321171608d2e480cd236cd078ace32da9ebeb9ca5e19a` |
| `artifacts/daily/mini_prose/cycle01/objection.json` | `cc83ca89e521eae8552f71f2519d9cd965f31ad3c6284b84790c374e3d3d6de5` |
| `artifacts/daily/mini_prose/cycle01/response.json` | `4bbdddeb83fab3257237d44bb2877df3efb21dec6efbc24b0e2fd825759e3611` |
| `artifacts/daily/mini_prose/cycle01/rival.json` | `ee88630a8354f99c95c5270bd499182db0bc72d34453f0ae565f5ca136ac4c41` |
| `attempts/daily/bare/cycle01/answer.json` | `9fe4b7f4dcdf19fa86cbf8074931a7178d11a1bb0d480208f7468ae98f2ad5de` |
| `attempts/daily/mini_fcl/cycle01/account.json` | `f4feb0a34503501d171e25103a7ee2190ddb458e86318527ba03da5c93c4fdb1` |
| `attempts/daily/mini_fcl/cycle01/rival.json` | `91a9f6c627c9bc8a7191dfa92895f93bcba8776283867814af9cbf096ea0061d` |
| `attempts/daily/mini_prose/cycle01/account.json` | `92bbab7376be0dfac3b3cd758c99052a5cd046b16b2710a939e3151d7a94534d` |
| `attempts/daily/mini_prose/cycle01/carry.json` | `c92d1fd717602ec99b7d4e3bac44ab2d2b5deccbb235b436628ccfd2a9284254` |
| `attempts/daily/mini_prose/cycle01/objection.json` | `415cf5532849caad5182a494177128d95c27b648f3f840aea185aeb17ad090da` |
| `attempts/daily/mini_prose/cycle01/response.json` | `889b437fd870b34e939337039b69fe5757a668fb4e8cc6d275eb739cfc9abaa6` |
| `attempts/daily/mini_prose/cycle01/rival.json` | `d5ed87140760180f9b11a72773330725106b4fa36bcb6729e87dccc330ac87c8` |
| `manifests/fork5.json` | `8f2d928b2f70298906b17d62e73b41804efa754d845f018d9eb312af7dcb536a` |
| `manifests/return6.json` | `bad1f6dc4ddda462f1b3acaa56a9e552eeb98255509cb4bfa3353c2305abb3b5` |
| `manifests/weave7.json` | `0b8a5f337f754b23fd51721ff287e25347af99648a7d2b00ad73b7baa571c2cb` |
| `material.json` | `8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff` |
| `plan.json` | `1e34079c4af43132440d131e5d7a480dabc4cc15fb501cd4c38eeb6d7f97fb3e` |
| `provider/daily/bare/cycle01/answer/call-0001.request.json` | `b7d9999fd53f2755436d67552717e326b159059b0e35e357a809aa519e1e146f` |
| `provider/daily/bare/cycle01/answer/call-0001.response.json` | `c04da850fbb4f1c01353b04f888f673c58bcb802946ec5a9c43f71ecdedba31d` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | `dbdffe06d56a5cb4df5e0538fc42cd6954871a2d4522450a209e54f7bb45c847` |
| `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | `47080f29d4b7b6b6018b4a4bcf4c6bff2797b834331c3932b184dd49fd1bc1cb` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | `881239bc7f75ccc7e905f7261c912d5cb0f6b8c3c028159d69b8f4de2ebe1385` |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | `dc453578ddd43ad6cbcdb9747b547bb2a2a5cc7ea323f4476fe2fe9754b2ec82` |
| `provider/daily/mini_prose/cycle01/account/call-0001.request.json` | `e5cf74ffe95f4aae021bc42ea4131aea64e7f17ec6422d13f1406952aca5652c` |
| `provider/daily/mini_prose/cycle01/account/call-0001.response.json` | `c531c435937663fee135943b9325c88716ca57891ac5ade146b88bb2c930e260` |
| `provider/daily/mini_prose/cycle01/carry/call-0001.request.json` | `6ed8bfae65ff68c607b1bb79d981d2e1ccefffb78466725079b5b3b2c0ab329d` |
| `provider/daily/mini_prose/cycle01/carry/call-0001.response.json` | `1361724ad67f15e15024e486b9a1510d6acc2f5cecd4eb39e34363ea12d9a930` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.request.json` | `48defcabb69e548322508d18b82ac7fd878a3159061f169263d9f0e8129ccfba` |
| `provider/daily/mini_prose/cycle01/objection/call-0001.response.json` | `32f331a5cda5dbd22ee61662f538e94c849d50ba3160df9a6aa5dba46d384bd4` |
| `provider/daily/mini_prose/cycle01/response/call-0001.request.json` | `63c9da8cefbc4b1f69e3d690691bcbb2b258b6f9953196ab0f46f06e4c6b94bf` |
| `provider/daily/mini_prose/cycle01/response/call-0001.response.json` | `b10fb0cfe95d52eb719c1cbb7670f439ed64597ad781bb7c5a94f64dbbe7c462` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.request.json` | `092e9cb37c6ced083946a90c19373693cd556658d85a565eab47b2ead748a187` |
| `provider/daily/mini_prose/cycle01/rival/call-0001.response.json` | `9efa63f21aa2fa8ff06ed9f5365ec09b9a56a51187a88c667cf449d4f6120c48` |
| `requests/daily/bare/cycle01/answer.json` | `6261a4844b8fe1ae2216b0ac8c62b6aedae95b49c8a7dab1953545f39f5389f0` |
| `requests/daily/mini_fcl/cycle01/account.json` | `e01b9c5414410e18cd6eace98cc626bc017379c8ffeb4af90b8577d05803c669` |
| `requests/daily/mini_fcl/cycle01/rival.json` | `ed50e44499fbc4afd4995201bbf489991e0d977c83758a6408c76c9f8a8c8759` |
| `requests/daily/mini_prose/cycle01/account.json` | `40fd10f3ad946fe96c4953cfc695e0a05cefa1531887eca377932241b60e73e1` |
| `requests/daily/mini_prose/cycle01/carry.json` | `ccc6fd1400281e237d32d7c67b5eef7a3ea41105b49d4509eb3e2747c457aa66` |
| `requests/daily/mini_prose/cycle01/objection.json` | `dec4b0559861d850f818d21d19447954660858cdd08ba8b92dd5b10b7e8bedfe` |
| `requests/daily/mini_prose/cycle01/response.json` | `b509d08616020c772a85e6db0806f15bf885a202a2cc7fc168408bdc3e3cc078` |
| `requests/daily/mini_prose/cycle01/rival.json` | `883efc661880455efbe93950a776fb75404fda09b7f8a561787e27432fdae552` |
| `responses/daily/bare/cycle01/answer.json` | `864063a9c106a47660ee34e3f2328ae471fe616c18732390c8b08bebc4c4457e` |
| `responses/daily/bare/cycle01/answer.txt` | `50ab84ee66d70a4850936ebe629593b6e1c88acced3b100ce96c0fa3829bca61` |
| `responses/daily/mini_fcl/cycle01/account.json` | `e648841806a41db5e61661f56fce49579e3dbed32657fb510a65de2de7426a2b` |
| `responses/daily/mini_fcl/cycle01/account.txt` | `a68a3032b1118e8f1b7d874f8c98d31f1fbb40fdc9df66c4a262b47d84688e29` |
| `responses/daily/mini_fcl/cycle01/rival.json` | `c6be9d3dfaa02616466d2201448419494a9b3c9051e75b402f314162507aecaa` |
| `responses/daily/mini_fcl/cycle01/rival.txt` | `6d50df4eda96f4739e48be29175dccf4c612b01a268378631d23c6573fc269aa` |
| `responses/daily/mini_prose/cycle01/account.json` | `a5b4fa5e4f1fa7249d5e0a847a3d2e8be8072082e5a46ca5115c30bcae3ecd3f` |
| `responses/daily/mini_prose/cycle01/account.txt` | `80d731b214deb7912a2f72ae3bb940000b9729b223036b1b8d15f33b7451a9e4` |
| `responses/daily/mini_prose/cycle01/carry.json` | `6548ddfd88433f952a6f1627eac312558cf3a9a058f0f221699fd196e1ea0865` |
| `responses/daily/mini_prose/cycle01/carry.txt` | `90800359ddc6ae22f740b6953b4bc549ee510c6bf0a8bbdaa26fdfcf35b2962a` |
| `responses/daily/mini_prose/cycle01/objection.json` | `fbc2bd3801f9512da480038562ce00fd15fdabd44701fcb17bcf37ce0d9b70fc` |
| `responses/daily/mini_prose/cycle01/objection.txt` | `7db71c7edd201687962d76a04022ec666aa712ccf341aaf367a4c9b9ac43768d` |
| `responses/daily/mini_prose/cycle01/response.json` | `790aaf1925790ea7adde9f87f6e7539dea6eb16cfeef49283884514a5b8f44d8` |
| `responses/daily/mini_prose/cycle01/response.txt` | `4b625e65782b6da646bff04a9042d246b2d2469d9789692c65dc37a88044800e` |
| `responses/daily/mini_prose/cycle01/rival.json` | `a471bd518451e21b35e0de406bfd6e4eee841ab4c43a2b3975d8d711bf286ff4` |
| `responses/daily/mini_prose/cycle01/rival.txt` | `dd250d42edab4ffab093d80bfa6bb671b7ef78c142ca951dd4db9d4725273b75` |
| `traces/daily/bare/cycle01/answer.json` | `4ff68da01ac0c9cfd4c060d4a822f7ced327003f53e9e96f1e3fb08916a7fbab` |
| `traces/daily/mini_fcl/cycle01/account.json` | `f4790106152ef33f8f02cc8f182089bd4e99beb4f553144a79e51e2ec4f92f53` |
| `traces/daily/mini_fcl/cycle01/rival.json` | `73b52169c195e57b9d96e9fea2373d40022ba4c5bdc35260a0e40bdec1f6c808` |
| `traces/daily/mini_prose/cycle01/account.json` | `5725e108b01c89983c73bc7e84268aa9bbf8b77d8b6fe57c79df1137bd5db455` |
| `traces/daily/mini_prose/cycle01/carry.json` | `4105b6b1a351feab78bf2286fcbbfa5b3d7bb0827f471cee01c3c19c62795a8f` |
| `traces/daily/mini_prose/cycle01/objection.json` | `bddda77c8e0e1a2121576d4d9341f065114cadd08700a8959b9539e50c2f7831` |
| `traces/daily/mini_prose/cycle01/response.json` | `cebb52924ebafd87f5833c3826c975d27f6715e65d7b918633ea095b06771fe4` |
| `traces/daily/mini_prose/cycle01/rival.json` | `dffbbaa541b26a80f7565bb1f56d78552e4025ff3f85d3f027a103fec6ad7b1e` |
| `waves/wave0001.json` | `e0bf128ec3a8ffeb11dfa534f48421d1877682757d9e643ae24ddbd62c39b482` |
| `waves/wave0002.json` | `1365f5025d6492d25b5ae47803a4cfb4edb695c9188583a38c2bdd358c0e2527` |
| `waves/wave0003.json` | `e3c25c5801cc124b8f9dcffb7330c3229962c87a4e5d1a2ae3400379aa16a8d6` |
| `waves/wave0004.json` | `8d0f554ee0438ad4131a96c5c73cdfddab7bd23555be074d4fcf720517e022e1` |

