# C001 recoding correspondence table

Published before dispatch. Every unit of each original objection document is listed with its recoded counterpart and the declared rules applied. No model call produced any entry; the recoding was authored offline by the study designer.

## arm: fcl (source mini_fcl)

**Unit definition.** prose documents: sentences produced by re.split(r'(?<=[.!?])\\s+', paragraph.strip()), paragraphs split on '\n\n'; FCL-1 documents: the same sentence split applied to each string field (text, scope, grounds, bearing, action, consequence) of each record

**Reconstruction.** recoded document = paragraphs of units joined by ' ', paragraphs joined by '\n\n' (prose) / original record and key order re-serialised with separators (",",":") (FCL-1); the same reconstruction applied to the original units reproduces the original bytes

**Rules.**

- `R1` SYNONYM - lexical substitution preserving reference and illocutionary force. A contraction and its expansion ("I'd" / "I would", "can't" / "cannot") are the same lexical items in the same order with the same modal force; that alternation is orthographic and is recorded under R1 rather than as an operation of its own.
- `R2` CONSTITUENT-ORDER - reordering of constituents (clauses, phrases, adverbials) inside one unit. Broadened 2026-09-14 from "reordering of clauses": the label was already carried by units that front a PP or an adverbial, and the narrower wording made those labels false. The restriction is unchanged - the reordering stays inside one unit, and it may not be used for an operation on an NP head.
- `R3` VOICE - active/passive or verbal/nominal alternation
- `R4` DEIXIS - demonstrative <-> explicit antecedent inside one unit. Applicable ONLY where the demonstrative has a unique antecedent inside the same paragraph, and the uniqueness argument is recorded in the unit row. Re-checked 2026-09-14: no unit of either document satisfies that restriction, so R4 is declared and not exercised.
- `R5` CONNECTIVE - substitution of an equivalent discourse connective

**Declared hedge/modal marker families** (counted per unit by `prepare`; a change in any count is `RECODING_HEDGE_FORCE_CHANGED`).

| family | tokens |
|---|---|
| `IF` | `if` |
| `UNLESS` | `unless` |
| `WHETHER` | `whether` |
| `MAY` | `may` |
| `MIGHT` | `might` |
| `CAN` | `can` |
| `COULD` | `could` |
| `WILL` | `will` |
| `WOULD` | `would` |
| `SHALL` | `shall` |
| `SHOULD` | `should` |
| `MUST` | `must` |
| `OUGHT` | `ought` |
| `NEED` | `need`, `needs` |
| `DESERVE` | `deserve`, `deserves`, `deserved` |
| `NECESSARILY` | `necessarily` |
| `PROBABLY` | `probably` |
| `POSSIBLY` | `possible`, `possibly` |
| `PERHAPS` | `perhaps` |
| `MERELY` | `merely`, `just`, `simply`, `only` |
| `SEEM` | `seem`, `seems` |
| `APPEAR` | `appear`, `appears` |
| `NEGATION` | `not`, `never`, `no`, `nor`, `neither`, `none`, `nothing`, `nobody` |

Declared hedge/modal marker families. `prepare` counts each family in the original and in the recoded text of every unit, after expanding contractions, and refuses the material if any count differs (RECODING_HEDGE_FORCE_CHANGED). This is the mechanical half of the "hedge force preserved" invariant; the semantic half is the published unit table.


What the counter cannot see. The check refuses a change in the COUNT of a declared marker family inside a unit, and nothing else. It is blind to illocutionary and evaluative force carried by ordinary predicates, and blind to which constituent a preserved marker attaches to. The independent spot-check of 2026-09-14 found it passing all 85 units while missing: "consistent with" -> "fit" (a bare compatibility relation loosened into a confirmatory one); "downweight" -> "discount"; "issue" -> "point"; "fine" -> "unobjectionable" (an un- litotes is not in the NEGATION family); "or" -> "and" under a negation, which admits a not-both reading the original excludes; and get-passive -> be-passive. Changes of that kind are caught only by reading. The 85-row correspondence table is published so the reading can be disputed row by row, and the two-reviewer re-read recorded in FIXES.md - the 2026-09-14 constituent re-read and the independent spot-check that followed it - is the record of its having been done. Every case listed here was reverted, not licensed.


**Invariants.**

- unit count, unit order and unit boundaries preserved; no cross-unit move
- quoted material reproduced verbatim
- FCL-1 record ids, types, uptake and every reference array unchanged
- no proposition added, dropped, strengthened or weakened; hedge force preserved, checked per unit as an exact count of every declared hedge/modal marker family
- criticism constituents preserved: target z, alleged defect delta, grounds g, bearing (FW5:609)
- no information-structure operation beyond the topic/focus reassignment intrinsic to R3 (active/passive alternation): no clefting, pseudo-clefting, topicalisation, equative inversion, existential-`there` insertion or deletion, subordination<->coordination, assertion<->presupposition - and no determiner or definiteness operation of its own: no the<->a, the<->this/that or bare<->determined change to an otherwise unchanged referring expression. Neither is in the declared rule set, so a unit that needed one was reverted to the simplest declared operation instead. Two intrinsic consequences are excluded rather than denied, because the material exercises both: R3 itself reassigns topic and focus (16 fcl and 14 prose units apply a voice or nominal alternation), and an R1 lexical paraphrase or an R3 verbal<->nominal alternation carries its own determiner with it ("falling recurrence" -> "a fall in recurrence", "presenting that sequence" -> "the presentation of that sequence", "being able to hold" -> "the ability to hold"). 26 units show a determiner-token delta of that second kind; none is a determiner operation applied on its own, and every unit that had applied one was reverted

**Not exercised.**

- cross-unit sentence re-ordering: available but deliberately unused, because unit order can carry argumentative dependence and its preservation makes the correspondence table checkable unit by unit. Recorded as an open question for root.
- R4 DEIXIS: declared, and not exercised anywhere. Under its uniqueness restriction no demonstrative in either document has a unique antecedent inside its own paragraph, so every unit that had applied a deixis operation was reverted at the 2026-09-14 re-read.
- information structure and determiner/definiteness: not declared as rules (no R6, no R7) and not used. This list is exhaustive as of the 2026-09-14 spot-check closure, which is what the earlier version of it was not. Reverted in the fcl document: B.P1.S1, B.P2.S3, B.P2.S7, B.P3.S2, B.P3.S3, B.P4.S1, B.P4.S2, B.P4.S4, B.P5.S2, B.P6.S3, K.o1.text.S1, K.o3.text.S1, K.o3.text.S2, K.o3.bearing.S1, K.c2.text.S1. Reverted in the prose document: B.P1.S1, B.P2.S2, B.P2.S3, B.P2.S4, B.P3.S1, B.P3.S4, B.P3.S7, B.P4.S1, B.P4.S2, B.P4.S3, B.P4.S4, B.P5.S1, B.P5.S3, C.P2.S1, C.P3.S1, C.P3.S2, C.P4.S1, C.P4.S3, C.P5.S2. The three units the spot-check recorded as outright violations of the declared rule set are inside that list - fcl K.o1.text.S1 (existential-`there` inserted, in record o1's own `text` field), fcl B.P4.S1 (existential-`there` deleted) and fcl B.P4.S2 (definite possessive predicate nominal turned into a bare plural, plus an equative->predicational shift) - as are the fronted-frame-adjunct (fcl B.P3.S2), NP-head-switch (fcl B.P3.S3), coordinated-definite-NP (fcl B.P5.S2) and cataphor (prose B.P4.S1) cases. Each was reverted to the simplest declared operation rather than licensed by a new rule, because the content-preservation argument for each is not clear-cut.
- evaluative and relational predicate substitution: not licensed by R1, which is restricted to substitutions preserving reference AND illocutionary force, and not declared as a rule of its own. Reverted at the spot-check closure: fcl B.P2.S7 ("hold" restored to "bind"), B.P3.S1 ("adopts"/"discounts" restored to "treats"/"gives less weight to"), B.P3.S4 ("fit" restored to "be consistent with"), B.P4.S1 ("point" restored to "issue"), B.P4.S3 ("unobjectionable" restored to "fine"), B.P5.S1 ("relegates to second place" restored to "treats as secondary"), K.o1.text.S2 ("discounted" restored to "given less weight"), K.c2.text.S1 ("and" restored to "or" under the negation, by leaving the clause active), and prose B.P2.S4 ("describes" restored to "is a description of"). None of these is visible to the hedge/modal counter; see hedge_marker_limits.

**Units: 50.**

| unit | location | rules | original | recoded |
|---|---|---|---|---|
| `B.P1.S1` | B | R1 | I want to press on the account's central move: reframing the conflict as a specification problem rather than a motivation or fairness problem. | I want to push on the account's central move: recasting the conflict as a problem of specification rather than a problem of motivation or fairness. |
| `B.P1.S2` | B | R1 | That reframing is doing a lot of work, and the material does not obviously support it. | That recasting is doing a great deal of work, and the material does not obviously support it. |
| `B.P2.S1` | B | R1 | Consider what the problem statement actually reports. | Look at what the statement of the problem actually reports. |
| `B.P2.S2` | B | R1 | Three flatmates argue about ordinary chores. | Three people sharing a flat quarrel over routine chores. |
| `B.P2.S3` | B | R1 R5 | Sometimes they agree who will do something, then later disagree about what the agreement meant. | On occasion they agree who will do a task, and afterwards fall out over what the agreement meant. |
| `B.P2.S4` | B | R1 | Schedules change. | Timetables shift. |
| `B.P2.S5` | B | R1 | One person has started avoiding the conversations. | One person has begun to steer clear of the conversations. |
| `B.P2.S6` | B | R3 | The account reads the recurring "later disagreement about what it meant" as evidence of ambiguity in the agreements. | The recurring "later disagreement about what it meant" is read by the account as evidence that the agreements were ambiguous. |
| `B.P2.S7` | B | R1 R5 | But the same observation is equally consistent with a different reading: the agreement was clear enough, and the later dispute is about whether the terms still bind given changed circumstances, or about who has standing to enforce them. | Yet the same observation is equally consistent with an alternative reading: the agreement was clear enough, and the later dispute is about whether the terms still bind given changed circumstances, or about who has standing to enforce them. |
| `B.P2.S8` | B | R1 | "You said you'd do the bins" / "yes, and then my shift changed" is not necessarily a semantics problem. | "You said you'd do the bins" / "yes, and then my shift changed" is not necessarily a problem of semantics. |
| `B.P2.S9` | B | R1 | It can be a renegotiation problem, or a legitimacy problem. | It can be a problem of renegotiation, or one of legitimacy. |
| `B.P3.S1` | B | R1 R2 R5 | The account acknowledges this in o1 but then treats the ambiguity hypothesis as the working one and downweights the alternatives. | In o1 the account acknowledges this, yet it then treats the ambiguity hypothesis as the working one and gives less weight to the alternatives. |
| `B.P3.S2` | B | R1 R2 R3 R5 | That is a defensible starting point if you have to pick one, but the account's own diagnostic step - try two or three concrete items and see if recurrence falls - is weaker than it looks, because a specification move can reduce friction while the underlying driver is load imbalance or resentment. | That is a defensible starting point if one has to be chosen, but the diagnostic step the account itself proposes - try two or three concrete items and see if recurrence falls - is weaker than it looks, since a specification move can lower friction while the driver underneath is load imbalance or resentment. |
| `B.P3.S3` | B | R1 | Tighter specs on a lopsided arrangement are still a lopsided arrangement, just with clearer paperwork. | Tighter specs on a lopsided arrangement are still a lopsided arrangement, only with clearer paperwork. |
| `B.P3.S4` | B | R1 R3 | Falling recurrence would be consistent with the ambiguity hypothesis, but the alternative hypotheses predict a different pattern: recurrence might drop on the specified items and reappear as new complaint items, or drop for a while and then return when circumstances change again. | A fall in recurrence would be consistent with the ambiguity hypothesis, but the rival hypotheses forecast a different pattern: recurrence might fall on the items specified and resurface as fresh complaint items, or fall for a time and then come back at the next change of circumstances. |
| `B.P3.S5` | B | R1 R3 | The account's test does not distinguish these. | These are not told apart by the account's test. |
| `B.P4.S1` | B | R1 | There is also a phrasing issue worth flagging. | There is also an issue of phrasing worth flagging. |
| `B.P4.S2` | B | R1 | The account says the problem as posed is "practical" and the material is "thin." Those are the author's characterizations, not features of the situation. | The account states that the problem as posed is "practical" and the material is "thin." Those are the author's characterizations, not features of the situation. |
| `B.P4.S3` | B | R1 R2 R3 | Calling the material thin is fine as a caution, but the account then uses the thinness to license a fair bit of construction (the three-column spec, the low-pressure approach to the withdrawing friend, the step-5 threshold). | As a caution, calling the material thin is fine, but the thinness is then used by the account to license a good deal of construction (the three-column spec, the low-pressure approach to the withdrawing friend, the step-5 threshold). |
| `B.P4.S4` | B | R1 | Thin material supports tentative proposals; it does not support sequencing those proposals as if the ambiguity reading had already earned its place at the front. | Thin material supports tentative proposals; it does not support ordering those proposals as if the ambiguity reading had already earned its place at the front. |
| `B.P5.S1` | B | R1 R2 | The account's most useful move is probably the one it treats as secondary: that the avoidance may be about the form of the conversations rather than the chores. | Probably the most useful move in the account is the one it treats as secondary: that the avoidance may concern the form of the conversations rather than the chores. |
| `B.P5.S2` | B | R5 | That deserves to be nearer the front, because it is the part of the situation that is genuinely distinctive and that the specific-negotiation advice does not address. | That deserves to be nearer the front, since it is the part of the situation that is genuinely distinctive and that the specific-negotiation advice does not address. |
| `B.P5.S3` | B | R1 | A tight spec on bins does not get a withdrawn flatmate back into the room. | A tight spec on bins does not bring a withdrawn flatmate back into the room. |
| `B.P5.S4` | B | R2 R5 | The account half-sees this in c3 and step 4, but the overall frame still centers the chores. | At c3 and step 4 the account half-sees this, yet the overall frame still centers the chores. |
| `B.P6.S1` | B | R1 | What I would not claim: that the ambiguity hypothesis is wrong. | What I would not assert: that the ambiguity hypothesis is mistaken. |
| `B.P6.S2` | B | R1 | I cannot tell from the material. | I cannot judge from the material. |
| `B.P6.S3` | B | R1 | My objection is to the ordering and to the test's strength, not to the hypothesis's plausibility. | My objection is to the ordering and to the strength of the test, not to the plausibility of the hypothesis. |
| `B.P6.S4` | B | R1 | If the account were rewritten with the conversational-form reading as the first hypothesis and the spec move as one of several probes, I would have less to say against it. | If the account were rewritten with the conversational-form reading as the first hypothesis and the spec move as one probe among several, I would have less to say against it. |
| `K.o1.text.S1` | commitments/o1/text | R1 | The account's reframing of the conflict as principally an ambiguity/specification problem is under-supported. | The account's recasting of the dispute as chiefly a problem of ambiguity/specification is insufficiently supported. |
| `K.o1.text.S2` | commitments/o1/text | R1 R3 | The reported pattern - later disagreement about what an agreement meant - is equally consistent with a renegotiation problem or a legitimacy problem under changed schedules, and the account downweights those alternatives after naming them in its own o1. | The reported pattern - later disagreement about what an agreement meant - is equally consistent with a renegotiation problem or a legitimacy problem under changed schedules, and those alternatives are given less weight by the account after it has named them in its own o1. |
| `K.o1.bearing.S1` | commitments/o1/bearing | R1 R3 | If the driver is renegotiation or legitimacy rather than ambiguity, the specification move in c2 treats a symptom, and the account's sequencing (chores first, relationship later) is misplaced. | If the driver is renegotiation or legitimacy instead of ambiguity, the specification move at c2 addresses a symptom, and the sequencing the account adopts (chores first, relationship later) is misplaced. |
| `K.o2.text.S1` | commitments/o2/text | R1 R2 R3 | The account's proposed test - see whether two or three concretely specified chores stop recurring - does not distinguish the ambiguity hypothesis from the alternatives. | The ambiguity hypothesis is not told apart from the alternatives by the test the account proposes - see whether two or three concretely specified chores stop recurring. |
| `K.o2.text.S2` | commitments/o2/text | R1 | Load imbalance or resentment can coexist with reduced friction on specified items, and recurrence may reappear as new complaint items or after the next schedule change. | Load imbalance or resentment can sit alongside reduced friction on specified items, and recurrence may come back as fresh complaint items or after the following schedule change. |
| `K.o2.bearing.S1` | commitments/o2/bearing | R1 R3 | Weakens the claim that falling recurrence would confirm c1 and rising recurrence would refute it; the test has lower discriminating power than the account implies. | Weakens the claim that a fall in recurrence would confirm c1 and a rise in recurrence would refute it; the discriminating power of the test is lower than the account implies. |
| `K.o3.text.S1` | commitments/o3/text | R1 | The account calls the material 'thin' and then licenses a fairly specific sequence (three-column spec, separate low-pressure approach, step-5 threshold for reconsidering the living arrangement). | The account describes the material as 'thin' and then licenses a fairly specific sequence (three-column spec, separate low-pressure approach, step-5 threshold for reconsidering the living arrangement). |
| `K.o3.text.S2` | commitments/o3/text | R3 | Thin material supports tentative probes; it does not support presenting that sequence as the natural order. | Thin material supports tentative probes; it does not support the presentation of that sequence as the natural order. |
| `K.o3.bearing.S1` | commitments/o3/bearing | R3 | The ordering of the account's recommendations is doing prescriptive work that the stated evidence does not carry. | The order in which the account's recommendations are placed is doing prescriptive work that the stated evidence does not carry. |
| `K.c1.text.S1` | commitments/c1/text | R1 | The account's most distinctive observation - that avoidance may be about the form and stakes of the conversations rather than the chores - deserves to be nearer the front of the analysis, because the specific-negotiation advice does not address it. | The account's most distinctive observation - that avoidance may be about the form and stakes of the conversations rather than the chores - deserves to be closer to the front of the analysis, because the specific-negotiation advice does not address it. |
| `K.c1.scope.S1` | commitments/c1/scope | R1 R5 | This household, given the reported withdrawal from conversations. | This household, in view of the reported withdrawal from conversations. |
| `K.c1.grounds.S1` | commitments/c1/grounds | R2 R5 | The account itself concedes this in c3 and half-treats it in step 4, but the overall frame still centers the chores. | At c3 the account itself concedes this and at step 4 half-treats it, yet the overall frame still centers the chores. |
| `K.c2.text.S1` | commitments/c2/text | R3 | A tighter specification of a lopsided or resented arrangement is still a lopsided or resented arrangement with clearer paperwork; specification alone does not address load imbalance or legitimacy. | A lopsided or resented arrangement specified more tightly is still a lopsided or resented arrangement with clearer paperwork; specification alone does not address load imbalance or legitimacy. |
| `K.c2.scope.S1` | commitments/c2/scope | R1 | Shared-household chore arrangements. | Chore arrangements in shared households. |
| `K.c2.consequence.S1` | commitments/c2/consequence | R1 R3 | Falling recurrence on specified items is compatible with both the ambiguity hypothesis and the alternative hypotheses, so it should not be treated as confirmation of c1. | A fall in recurrence on specified items is compatible with the ambiguity hypothesis and with the alternative hypotheses alike, so it should not be treated as confirmation of c1. |
| `K.o4.text.S1` | commitments/o4/text | R1 | My own objection may over-reach. | My own objection may reach too far. |
| `K.o4.text.S2` | commitments/o4/text | R1 | If the flatmates genuinely cannot say what they agreed to, ambiguity is the plainest reading and the alternatives I am raising are harder to establish from the material than the account's reading is. | If the flatmates genuinely cannot say what they agreed to, ambiguity is the plainest reading and the alternatives I am putting forward are harder to establish from the material than the account's reading is. |
| `K.o4.bearing.S1` | commitments/o4/bearing | R1 | If ambiguity is in fact the plainest reading, the objection reduces to a complaint about sequencing rather than about substance. | If ambiguity is in fact the plainest reading, the objection comes down to a complaint about sequencing rather than about substance. |
| `K.p1.text.S1` | commitments/p1/text | R1 R3 | The material does not say whether the later disagreements are about what the words meant, about whether the agreement still binds after a schedule change, or about who has standing to raise the issue. | Whether the later disagreements concern what the words meant, whether the agreement still binds after a schedule change, or who has standing to raise the issue is not stated by the material. |
| `K.p1.text.S2` | commitments/p1/text | R1 | These are distinguishable and the account does not distinguish them. | These are distinguishable and the account does not tell them apart. |
| `K.u1.text.S1` | commitments/u1/text | R1 R3 | Ask that the account be read with its own o1 treated as a live competitor rather than a caveat: state the alternative readings (ambiguity, renegotiation, legitimacy) as rival hypotheses and design the probe to distinguish them, not just to measure recurrence. | Ask for the account to be read with its own o1 taken as a live competitor rather than a caveat: set out the alternative readings (ambiguity, renegotiation, legitimacy) as rival hypotheses and build the probe to tell them apart, not merely to measure recurrence. |
| `K.u1.action.S1` | commitments/u1/action | R1 R3 R5 | Revise the framing so the conversational-form reading and the ambiguity reading sit side by side, with the spec move as one probe among several. | Rework the framing so that the conversational-form reading and the ambiguity reading stand side by side, the spec move being one probe among several. |

**Carrier variant (same content, disturbed carrier).**

- body: paragraphs hard-wrapped to 72 columns (whitespace only)
- commitments: FCL-1 document re-serialised with indent=2, keys sorted alphabetically, records array reversed, uptake array reversed

**Grain declaration.** FCL-1 content is the set of records keyed by id (each a field->value map), the set of uptake ids and the language tag; array order, key order and whitespace are carrier. Prose content is the sequence of whitespace-separated word tokens; line breaks, indentation and bullet markers are carrier. This declaration is itself a criticisable interpretation claim (SEMANTIC_GUIDE, "Declare the interpretation before the evidence").

**Normalisation proof.**

| quantity | value |
|---|---|
| body_bytes_differ | `True` |
| body_carrier_normalised_sha256 | `4b999291a3e55e18bb0c547585508fa22f059b1268de995ca5529618ca1aa2b9` |
| body_equal | `True` |
| body_original_normalised_sha256 | `4b999291a3e55e18bb0c547585508fa22f059b1268de995ca5529618ca1aa2b9` |
| commitments_bytes_differ | `True` |
| commitments_carrier_normalised_sha256 | `afc365628d1aaae3bf593cf17511fa1efa7a7ebe7ceff66ac5f3cfb46cb879fd` |
| commitments_equal | `True` |
| commitments_original_normalised_sha256 | `afc365628d1aaae3bf593cf17511fa1efa7a7ebe7ceff66ac5f3cfb46cb879fd` |

## arm: prose (source mini_prose)

**Unit definition.** prose documents: sentences produced by re.split(r'(?<=[.!?])\\s+', paragraph.strip()), paragraphs split on '\n\n'; FCL-1 documents: the same sentence split applied to each string field (text, scope, grounds, bearing, action, consequence) of each record

**Reconstruction.** recoded document = paragraphs of units joined by ' ', paragraphs joined by '\n\n' (prose) / original record and key order re-serialised with separators (",",":") (FCL-1); the same reconstruction applied to the original units reproduces the original bytes

**Rules.**

- `R1` SYNONYM - lexical substitution preserving reference and illocutionary force. A contraction and its expansion ("I'd" / "I would", "can't" / "cannot") are the same lexical items in the same order with the same modal force; that alternation is orthographic and is recorded under R1 rather than as an operation of its own.
- `R2` CONSTITUENT-ORDER - reordering of constituents (clauses, phrases, adverbials) inside one unit. Broadened 2026-09-14 from "reordering of clauses": the label was already carried by units that front a PP or an adverbial, and the narrower wording made those labels false. The restriction is unchanged - the reordering stays inside one unit, and it may not be used for an operation on an NP head.
- `R3` VOICE - active/passive or verbal/nominal alternation
- `R4` DEIXIS - demonstrative <-> explicit antecedent inside one unit. Applicable ONLY where the demonstrative has a unique antecedent inside the same paragraph, and the uniqueness argument is recorded in the unit row. Re-checked 2026-09-14: no unit of either document satisfies that restriction, so R4 is declared and not exercised.
- `R5` CONNECTIVE - substitution of an equivalent discourse connective

**Declared hedge/modal marker families** (counted per unit by `prepare`; a change in any count is `RECODING_HEDGE_FORCE_CHANGED`).

| family | tokens |
|---|---|
| `IF` | `if` |
| `UNLESS` | `unless` |
| `WHETHER` | `whether` |
| `MAY` | `may` |
| `MIGHT` | `might` |
| `CAN` | `can` |
| `COULD` | `could` |
| `WILL` | `will` |
| `WOULD` | `would` |
| `SHALL` | `shall` |
| `SHOULD` | `should` |
| `MUST` | `must` |
| `OUGHT` | `ought` |
| `NEED` | `need`, `needs` |
| `DESERVE` | `deserve`, `deserves`, `deserved` |
| `NECESSARILY` | `necessarily` |
| `PROBABLY` | `probably` |
| `POSSIBLY` | `possible`, `possibly` |
| `PERHAPS` | `perhaps` |
| `MERELY` | `merely`, `just`, `simply`, `only` |
| `SEEM` | `seem`, `seems` |
| `APPEAR` | `appear`, `appears` |
| `NEGATION` | `not`, `never`, `no`, `nor`, `neither`, `none`, `nothing`, `nobody` |

Declared hedge/modal marker families. `prepare` counts each family in the original and in the recoded text of every unit, after expanding contractions, and refuses the material if any count differs (RECODING_HEDGE_FORCE_CHANGED). This is the mechanical half of the "hedge force preserved" invariant; the semantic half is the published unit table.


What the counter cannot see. The check refuses a change in the COUNT of a declared marker family inside a unit, and nothing else. It is blind to illocutionary and evaluative force carried by ordinary predicates, and blind to which constituent a preserved marker attaches to. The independent spot-check of 2026-09-14 found it passing all 85 units while missing: "consistent with" -> "fit" (a bare compatibility relation loosened into a confirmatory one); "downweight" -> "discount"; "issue" -> "point"; "fine" -> "unobjectionable" (an un- litotes is not in the NEGATION family); "or" -> "and" under a negation, which admits a not-both reading the original excludes; and get-passive -> be-passive. Changes of that kind are caught only by reading. The 85-row correspondence table is published so the reading can be disputed row by row, and the two-reviewer re-read recorded in FIXES.md - the 2026-09-14 constituent re-read and the independent spot-check that followed it - is the record of its having been done. Every case listed here was reverted, not licensed.


**Invariants.**

- unit count, unit order and unit boundaries preserved; no cross-unit move
- quoted material reproduced verbatim
- FCL-1 record ids, types, uptake and every reference array unchanged
- no proposition added, dropped, strengthened or weakened; hedge force preserved, checked per unit as an exact count of every declared hedge/modal marker family
- criticism constituents preserved: target z, alleged defect delta, grounds g, bearing (FW5:609)
- no information-structure operation beyond the topic/focus reassignment intrinsic to R3 (active/passive alternation): no clefting, pseudo-clefting, topicalisation, equative inversion, existential-`there` insertion or deletion, subordination<->coordination, assertion<->presupposition - and no determiner or definiteness operation of its own: no the<->a, the<->this/that or bare<->determined change to an otherwise unchanged referring expression. Neither is in the declared rule set, so a unit that needed one was reverted to the simplest declared operation instead. Two intrinsic consequences are excluded rather than denied, because the material exercises both: R3 itself reassigns topic and focus (16 fcl and 14 prose units apply a voice or nominal alternation), and an R1 lexical paraphrase or an R3 verbal<->nominal alternation carries its own determiner with it ("falling recurrence" -> "a fall in recurrence", "presenting that sequence" -> "the presentation of that sequence", "being able to hold" -> "the ability to hold"). 26 units show a determiner-token delta of that second kind; none is a determiner operation applied on its own, and every unit that had applied one was reverted

**Not exercised.**

- cross-unit sentence re-ordering: available but deliberately unused, because unit order can carry argumentative dependence and its preservation makes the correspondence table checkable unit by unit. Recorded as an open question for root.
- R4 DEIXIS: declared, and not exercised anywhere. Under its uniqueness restriction no demonstrative in either document has a unique antecedent inside its own paragraph, so every unit that had applied a deixis operation was reverted at the 2026-09-14 re-read.
- information structure and determiner/definiteness: not declared as rules (no R6, no R7) and not used. This list is exhaustive as of the 2026-09-14 spot-check closure, which is what the earlier version of it was not. Reverted in the fcl document: B.P1.S1, B.P2.S3, B.P2.S7, B.P3.S2, B.P3.S3, B.P4.S1, B.P4.S2, B.P4.S4, B.P5.S2, B.P6.S3, K.o1.text.S1, K.o3.text.S1, K.o3.text.S2, K.o3.bearing.S1, K.c2.text.S1. Reverted in the prose document: B.P1.S1, B.P2.S2, B.P2.S3, B.P2.S4, B.P3.S1, B.P3.S4, B.P3.S7, B.P4.S1, B.P4.S2, B.P4.S3, B.P4.S4, B.P5.S1, B.P5.S3, C.P2.S1, C.P3.S1, C.P3.S2, C.P4.S1, C.P4.S3, C.P5.S2. The three units the spot-check recorded as outright violations of the declared rule set are inside that list - fcl K.o1.text.S1 (existential-`there` inserted, in record o1's own `text` field), fcl B.P4.S1 (existential-`there` deleted) and fcl B.P4.S2 (definite possessive predicate nominal turned into a bare plural, plus an equative->predicational shift) - as are the fronted-frame-adjunct (fcl B.P3.S2), NP-head-switch (fcl B.P3.S3), coordinated-definite-NP (fcl B.P5.S2) and cataphor (prose B.P4.S1) cases. Each was reverted to the simplest declared operation rather than licensed by a new rule, because the content-preservation argument for each is not clear-cut.
- evaluative and relational predicate substitution: not licensed by R1, which is restricted to substitutions preserving reference AND illocutionary force, and not declared as a rule of its own. Reverted at the spot-check closure: fcl B.P2.S7 ("hold" restored to "bind"), B.P3.S1 ("adopts"/"discounts" restored to "treats"/"gives less weight to"), B.P3.S4 ("fit" restored to "be consistent with"), B.P4.S1 ("point" restored to "issue"), B.P4.S3 ("unobjectionable" restored to "fine"), B.P5.S1 ("relegates to second place" restored to "treats as secondary"), K.o1.text.S2 ("discounted" restored to "given less weight"), K.c2.text.S1 ("and" restored to "or" under the negation, by leaving the clause active), and prose B.P2.S4 ("describes" restored to "is a description of"). None of these is visible to the hedge/modal counter; see hedge_marker_limits.

**Units: 35.**

| unit | location | rules | original | recoded |
|---|---|---|---|---|
| `B.P1.S1` | B | R1 | The account I'm objecting to is the one that treats the verbal-agreement memory gap as the central mechanism, with the written record plus weekly check-in as the natural remedy. | The account I am objecting to is the one that makes the verbal-agreement memory gap the central mechanism, with the written record plus weekly check-in as the natural remedy. |
| `B.P1.S2` | B | R1 R3 | My grounds are internal to the material rather than imported facts. | My grounds lie inside the material rather than in facts brought in from elsewhere. |
| `B.P2.S1` | B | R1 R3 | The stated problem has three named elements: agreements that later mean different things, work schedules that change, and one friend who has started avoiding the conversations. | Three elements are named in the stated problem: agreements that later mean different things, work schedules that change, and one friend who has begun avoiding the conversations. |
| `B.P2.S2` | B | R3 | The account's reading makes the first element primary and demotes the third to a symptom — 'avoidance is a symptom worth understanding before it's treated as a problem to correct.' That ordering is not forced by the material. | Under the account's reading the first element is made primary and the third is demoted to a symptom — 'avoidance is a symptom worth understanding before it's treated as a problem to correct.' That ordering is not forced by the material. |
| `B.P2.S3` | B | R1 | Read the other way, the avoidance is the load-bearing fact and the chore disputes are where an already-shifting household keeps failing to talk. | Taken the other way round, the avoidance is the load-bearing fact and the chore disputes are where an already-shifting household keeps failing to talk. |
| `B.P2.S4` | B | R1 | On that reading, the memory-gap conjecture is a description of the surface, and a written record may simply give the same unresolved conversation a new medium. | On that reading, the memory-gap conjecture is a description of the surface, and a written record may simply give the same unresolved conversation a fresh medium. |
| `B.P3.S1` | B | R1 | There's a second difficulty. | There is a second difficulty. |
| `B.P3.S2` | B | R1 R2 | A memory gap and a genuine disagreement about terms are not the same thing, and the account slides between them. | A memory gap is not the same thing as a genuine disagreement about terms, and the account slips between them. |
| `B.P3.S3` | B | R1 | 'I'll do the dishes' meaning different amounts of work under different schedules is not a case of forgetting; it's a case of ambiguity plus changed circumstances. | 'I'll do the dishes' standing for different amounts of work under different schedules is not a case of forgetting; it is a case of ambiguity together with changed circumstances. |
| `B.P3.S4` | B | R3 | A written record settles who said what. | A written record settles what was said by whom. |
| `B.P3.S5` | B | R1 R5 | It does not settle what 'this week' or 'done' should mean when schedules keep shifting, because that is a normative question each person answers differently and no note adjudicates. | It does not settle what 'this week' or 'done' should mean while schedules keep shifting, since that is a normative question each person answers differently and no note adjudicates. |
| `B.P3.S6` | B | R2 R5 | So the proposed test — watch whether 'what was agreed' disputes fall — can show a drop in memory disputes while leaving the substantive disagreement untouched, or can show no drop because the disputes were never memorial ones. | The proposed test — watch whether 'what was agreed' disputes fall — can therefore show a drop in memory disputes while leaving the substantive disagreement untouched, or can show no drop because the disputes were never memorial ones. |
| `B.P3.S7` | B | R1 R3 | Either outcome is readable as supporting the account, which is a weakness rather than a strength. | Either outcome is readable as support for the account, which is a weakness rather than a strength. |
| `B.P4.S1` | B | R1 | The account also names its own unresolved dependency without resolving it: the proposal assumes all three flatmates can talk without a mediator, 'which the avoidance itself puts in question.' That is not a peripheral caveat. | The account also names its own unresolved dependency without settling it: the proposal assumes all three flatmates can talk without a mediator, 'which the avoidance itself puts in question.' That is not a peripheral caveat. |
| `B.P4.S2` | B | R1 R3 | If the avoidance is the mechanism by which the group has stopped being able to hold the conversation, then a weekly check-in is a proposal to do more of the thing that already failed, addressed to the person who withdrew from it. | If the avoidance is the mechanism by which the group has lost the ability to hold the conversation, then a weekly check-in is a proposal to do more of the thing that already failed, addressed to the person who withdrew from it. |
| `B.P4.S3` | B | R3 | The separate approach to that friend is the part of the account most responsive to the material, and the account flags it as most contestable. | The separate approach to that friend is the part of the account most responsive to the material, and it is flagged by the account as most contestable. |
| `B.P4.S4` | B | R1 | I'd reverse that ranking: the approach, or something that names the avoidance as the problem, is the load-bearing move, and the record is optional. | I would turn that ordering round: the approach, or something that names the avoidance as the problem, is the load-bearing move, and the record is optional. |
| `B.P5.S1` | B | R1 | I can't establish from the material which reading is right, and I'm not claiming the memory-gap account is false. | I cannot make out from the material which reading is right, and I am not claiming the memory-gap account is false. |
| `B.P5.S2` | B | R1 R3 | What I have grounds to object to is order of operations and the diagnostic confidence that rides on a conjecture the account itself calls a conjecture. | What I have grounds for objecting to is order of operations and the diagnostic confidence that rests on a conjecture the account itself calls a conjecture. |
| `B.P5.S3` | B | R1 R5 | The clean version of the account would separate the retrospective possibility (agreements drifted because nobody recorded them) from the prospective one (record them now and drift will stop), because the material supports the first and not the second. | The clean version of the account would keep the retrospective possibility (agreements drifted because nobody recorded them) apart from the prospective one (record them now and drift will stop), since the material supports the former and not the latter. |
| `C.P1.S1` | C | R1 R3 | Taking this objection up is mainly a commitment to hold two readings side by side rather than to defend one. | To take this objection up is chiefly to commit to holding two readings side by side rather than defending one. |
| `C.P1.S2` | C | R1 | If the continuation treats the memory-gap reading as primary, I'd want the avoidance-as-central reading stated in the same breath so the household's own account can discriminate between them, rather than one reading being quietly assumed. | If the continuation treats the memory-gap reading as primary, I would want the avoidance-as-central reading set out in the same breath so the household's own account can discriminate between them, rather than one reading being quietly assumed. |
| `C.P2.S1` | C | R1 | I'm proposing a sharpened test, and it can fail in a direction that counts against me. | I am proposing a sharpened test, and it can fail in a direction that tells against me. |
| `C.P2.S2` | C | R1 R3 R5 | If agreements get written down, 'done' is defined, and the recurring arguments nonetheless continue or intensify, that supports the account I'm objecting to and argues against my ranking. | If agreements are written down, 'done' is defined, and the recurring arguments nevertheless continue or intensify, that supports the account I am objecting to and tells against my ordering. |
| `C.P2.S3` | C | R1 | I'd rather say that in advance than leave it implicit. | I would sooner state that in advance than leave it implicit. |
| `C.P2.S4` | C | R1 R2 | I can't currently say which reading is right; that gap is part of what the objection asserts, not something I'm hiding. | At present I cannot say which reading is right; that gap forms part of what the objection asserts, not something I am concealing. |
| `C.P3.S1` | C | R1 | I'm also claiming a distinction the original account blurs — between memorial and normative disagreement — and the distinction is contestable. | I am also asserting a distinction the original account blurs — between memorial and normative disagreement — and the distinction is contestable. |
| `C.P3.S2` | C | R1 | If someone shows that in this kind of household the two are not separable in practice, that the act of writing something down does shift the norms, my criticism loses some of its bite. | If someone demonstrates that in this kind of household the two are not separable in practice, that the act of writing something down does shift the norms, my criticism loses some of its bite. |
| `C.P3.S3` | C | R3 | I'd want that to count as a revision of the objection rather than as noise. | I would want that counted as a revision of the objection rather than as noise. |
| `C.P4.S1` | C | R1 R5 | On the local trial: if a written record or check-in is attempted, I'd want the result reported as the household describes it, including the case where the avoiding friend reads the note as surveillance. | As to the local trial: if a written record or check-in is attempted, I would want the result reported as the household describes it, including the case where the avoiding friend reads the note as surveillance. |
| `C.P4.S2` | C | R1 R3 | That would be evidence about the intervention's social cost, not merely about whether it works, and the account's own framing already flags that risk. | That would be evidence about the social cost of the intervention, not merely about whether it works, and that risk is already flagged by the account's own framing. |
| `C.P4.S3` | C | R1 | I'd treat a quiet week as uninformative either way. | I would treat a quiet week as uninformative in either direction. |
| `C.P5.S1` | C | R1 R3 | What I'm not committing to: I have no basis for proposing a mediator, a reassignment of chores, or a formalization of the household, and I'm not claiming any of those are better than what the original account proposes. | What I am not committing to: I have no basis on which to propose a mediator, a reassignment of chores, or a formalization of the household, and I make no claim that any of those improves on what the original account proposes. |
| `C.P5.S2` | C | R3 | Naming alternatives as possible better routes is not the same as endorsing them, and I can't rank them from the material shown. | To name alternatives as possible better routes is not to endorse them, and I cannot rank them from the material shown. |
| `C.P6.S1` | C | R1 | If this is continued, the piece of work I'd actually take on is writing out the two readings so the difference becomes testable, and then specifying what observation would separate them rather than trying to settle the reading now. | If this is continued, the piece of work I would actually take on is setting out the two readings so the difference becomes testable, and then specifying what observation would separate them rather than trying to settle the reading now. |

**Carrier variant (same content, disturbed carrier).**

- body: paragraphs hard-wrapped to 72 columns (whitespace only)
- commitments: each paragraph rendered as one "- " bullet item, hard-wrapped to 68 columns with two-space continuation indent; sentence order unchanged

**Grain declaration.** FCL-1 content is the set of records keyed by id (each a field->value map), the set of uptake ids and the language tag; array order, key order and whitespace are carrier. Prose content is the sequence of whitespace-separated word tokens; line breaks, indentation and bullet markers are carrier. This declaration is itself a criticisable interpretation claim (SEMANTIC_GUIDE, "Declare the interpretation before the evidence").

**Normalisation proof.**

| quantity | value |
|---|---|
| body_bytes_differ | `True` |
| body_carrier_normalised_sha256 | `7ef63adfcfaab53c4a33606dc5e98410ffbb821b61bb2ea92b64874131116187` |
| body_equal | `True` |
| body_original_normalised_sha256 | `7ef63adfcfaab53c4a33606dc5e98410ffbb821b61bb2ea92b64874131116187` |
| commitments_bytes_differ | `True` |
| commitments_carrier_normalised_sha256 | `a4eca70ef37ea482633ba3fdbb54ac0c55c46a58f9965f67f0dfafd010394df3` |
| commitments_equal | `True` |
| commitments_original_normalised_sha256 | `a4eca70ef37ea482633ba3fdbb54ac0c55c46a58f9965f67f0dfafd010394df3` |

