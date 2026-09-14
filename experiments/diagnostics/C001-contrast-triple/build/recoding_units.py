"""Hand-authored content-preserving recoding of the H005 fork5 `objection` documents.

Authored offline by the study designer before any dispatch. No model call produced
any entry here. Unit ids index the original document; `r` is the recoded counterpart;
`rules` names the declared operations applied.

Declared rules (see material.json -> arms.<arm>.recoding.rule):
  R1 SYNONYM      lexical substitution preserving reference and illocutionary force.
                  A contraction and its expansion ("I'd" / "I would", "can't" /
                  "cannot") are the same lexical items in the same order with the
                  same modal force; the alternation is orthographic and is recorded
                  under R1 rather than as an operation of its own.
  R2 CONSTITUENT-ORDER
                  reordering of constituents (clauses, phrases, adverbials) inside
                  one unit
  R3 VOICE        active/passive or verbal/nominal alternation
  R4 DEIXIS       demonstrative <-> explicit antecedent inside one unit. Applicable
                  ONLY where the demonstrative has a unique antecedent inside the
                  same paragraph, and the uniqueness argument is recorded in the unit
                  row. No unit of either document satisfies that restriction, so R4
                  is declared and NOT exercised (material.json -> not_exercised).
  R5 CONNECTIVE   substitution of an equivalent discourse connective

Operations deliberately NOT in the declared set and therefore NOT used anywhere:
  information structure BEYOND the topic/focus reassignment intrinsic to R3
  (active/passive alternation) - so no clefting, pseudo-clefting, topicalisation,
  equative inversion, existential-`there` insertion or deletion,
  subordination<->coordination, assertion<->presupposition - and no
  determiner/definiteness change (the<->a, the<->this/that, bare<->determined).
  The 2026-09-14 recoding re-read and the independent spot-check closure that
  followed it reverted every unit that had used one; material.json ->
  not_exercised lists them exhaustively.

Invariants (asserted in tools/contrast_triple_study.py `prepare`):
  - unit count, unit order and unit boundaries are preserved (no cross-unit move)
  - quoted material is reproduced verbatim
  - FCL-1 record ids, types, uptake and every reference array are unchanged
  - no proposition added, dropped, strengthened or weakened; hedge force preserved,
    checked per unit as an exact count of every declared hedge/modal marker. The
    counter reads markers only: evaluative and relational predicates are checked by
    reading (material.json -> hedge_marker_limits)
  - no information-structure operation beyond the topic/focus reassignment intrinsic
    to R3 (active/passive alternation), and no determiner or definiteness operation of
    its own - a determiner that an R1 paraphrase or an R3 verbal<->nominal alternation
    carries with it is part of that operation, not a separate one
  - the criticism's constituents keep their roles: represented target z, alleged
    defect delta, grounds g, bearing (FW5:609)
"""

FCL_BODY = [
 ("B.P1.S1", ["R1"],
  "I want to push on the account's central move: recasting the conflict as a problem of specification rather than a problem of motivation or fairness."),
 ("B.P1.S2", ["R1"],
  "That recasting is doing a great deal of work, and the material does not obviously support it."),
 ("B.P2.S1", ["R1"],
  "Look at what the statement of the problem actually reports."),
 ("B.P2.S2", ["R1"],
  "Three people sharing a flat quarrel over routine chores."),
 ("B.P2.S3", ["R1", "R5"],
  "On occasion they agree who will do a task, and afterwards fall out over what the agreement meant."),
 ("B.P2.S4", ["R1"],
  "Timetables shift."),
 ("B.P2.S5", ["R1"],
  "One person has begun to steer clear of the conversations."),
 ("B.P2.S6", ["R3"],
  "The recurring \"later disagreement about what it meant\" is read by the account as evidence that the agreements were ambiguous."),
 ("B.P2.S7", ["R1", "R5"],
  "Yet the same observation is equally consistent with an alternative reading: the agreement was clear enough, and the later dispute is about whether the terms still bind given changed circumstances, or about who has standing to enforce them."),
 ("B.P2.S8", ["R1"],
  "\"You said you'd do the bins\" / \"yes, and then my shift changed\" is not necessarily a problem of semantics."),
 ("B.P2.S9", ["R1"],
  "It can be a problem of renegotiation, or one of legitimacy."),
 ("B.P3.S1", ["R1", "R2", "R5"],
  "In o1 the account acknowledges this, yet it then treats the ambiguity hypothesis as the working one and gives less weight to the alternatives."),
 ("B.P3.S2", ["R1", "R2", "R3", "R5"],
  "That is a defensible starting point if one has to be chosen, but the diagnostic step the account itself proposes - try two or three concrete items and see if recurrence falls - is weaker than it looks, since a specification move can lower friction while the driver underneath is load imbalance or resentment."),
 ("B.P3.S3", ["R1"],
  "Tighter specs on a lopsided arrangement are still a lopsided arrangement, only with clearer paperwork."),
 ("B.P3.S4", ["R1", "R3"],
  "A fall in recurrence would be consistent with the ambiguity hypothesis, but the rival hypotheses forecast a different pattern: recurrence might fall on the items specified and resurface as fresh complaint items, or fall for a time and then come back at the next change of circumstances."),
 ("B.P3.S5", ["R1", "R3"],
  "These are not told apart by the account's test."),
 ("B.P4.S1", ["R1"],
  "There is also an issue of phrasing worth flagging."),
 ("B.P4.S2", ["R1"],
  "The account states that the problem as posed is \"practical\" and the material is \"thin.\" Those are the author's characterizations, not features of the situation."),
 ("B.P4.S3", ["R1", "R2", "R3"],
  "As a caution, calling the material thin is fine, but the thinness is then used by the account to license a good deal of construction (the three-column spec, the low-pressure approach to the withdrawing friend, the step-5 threshold)."),
 ("B.P4.S4", ["R1"],
  "Thin material supports tentative proposals; it does not support ordering those proposals as if the ambiguity reading had already earned its place at the front."),
 ("B.P5.S1", ["R1", "R2"],
  "Probably the most useful move in the account is the one it treats as secondary: that the avoidance may concern the form of the conversations rather than the chores."),
 ("B.P5.S2", ["R5"],
  "That deserves to be nearer the front, since it is the part of the situation that is genuinely distinctive and that the specific-negotiation advice does not address."),
 ("B.P5.S3", ["R1"],
  "A tight spec on bins does not bring a withdrawn flatmate back into the room."),
 ("B.P5.S4", ["R2", "R5"],
  "At c3 and step 4 the account half-sees this, yet the overall frame still centers the chores."),
 ("B.P6.S1", ["R1"],
  "What I would not assert: that the ambiguity hypothesis is mistaken."),
 ("B.P6.S2", ["R1"],
  "I cannot judge from the material."),
 ("B.P6.S3", ["R1"],
  "My objection is to the ordering and to the strength of the test, not to the plausibility of the hypothesis."),
 ("B.P6.S4", ["R1"],
  "If the account were rewritten with the conversational-form reading as the first hypothesis and the spec move as one probe among several, I would have less to say against it."),
]

FCL_FIELDS = [
 ("K.o1.text.S1", ["R1"],
  "The account's recasting of the dispute as chiefly a problem of ambiguity/specification is insufficiently supported."),
 ("K.o1.text.S2", ["R1", "R3"],
  "The reported pattern - later disagreement about what an agreement meant - is equally consistent with a renegotiation problem or a legitimacy problem under changed schedules, and those alternatives are given less weight by the account after it has named them in its own o1."),
 ("K.o1.bearing.S1", ["R1", "R3"],
  "If the driver is renegotiation or legitimacy instead of ambiguity, the specification move at c2 addresses a symptom, and the sequencing the account adopts (chores first, relationship later) is misplaced."),
 ("K.o2.text.S1", ["R1", "R2", "R3"],
  "The ambiguity hypothesis is not told apart from the alternatives by the test the account proposes - see whether two or three concretely specified chores stop recurring."),
 ("K.o2.text.S2", ["R1"],
  "Load imbalance or resentment can sit alongside reduced friction on specified items, and recurrence may come back as fresh complaint items or after the following schedule change."),
 ("K.o2.bearing.S1", ["R1", "R3"],
  "Weakens the claim that a fall in recurrence would confirm c1 and a rise in recurrence would refute it; the discriminating power of the test is lower than the account implies."),
 ("K.o3.text.S1", ["R1"],
  "The account describes the material as 'thin' and then licenses a fairly specific sequence (three-column spec, separate low-pressure approach, step-5 threshold for reconsidering the living arrangement)."),
 ("K.o3.text.S2", ["R3"],
  "Thin material supports tentative probes; it does not support the presentation of that sequence as the natural order."),
 ("K.o3.bearing.S1", ["R3"],
  "The order in which the account's recommendations are placed is doing prescriptive work that the stated evidence does not carry."),
 ("K.c1.text.S1", ["R1"],
  "The account's most distinctive observation - that avoidance may be about the form and stakes of the conversations rather than the chores - deserves to be closer to the front of the analysis, because the specific-negotiation advice does not address it."),
 ("K.c1.scope.S1", ["R1", "R5"],
  "This household, in view of the reported withdrawal from conversations."),
 ("K.c1.grounds.S1", ["R2", "R5"],
  "At c3 the account itself concedes this and at step 4 half-treats it, yet the overall frame still centers the chores."),
 ("K.c2.text.S1", ["R3"],
  "A lopsided or resented arrangement specified more tightly is still a lopsided or resented arrangement with clearer paperwork; specification alone does not address load imbalance or legitimacy."),
 ("K.c2.scope.S1", ["R1"],
  "Chore arrangements in shared households."),
 ("K.c2.consequence.S1", ["R1", "R3"],
  "A fall in recurrence on specified items is compatible with the ambiguity hypothesis and with the alternative hypotheses alike, so it should not be treated as confirmation of c1."),
 ("K.o4.text.S1", ["R1"],
  "My own objection may reach too far."),
 ("K.o4.text.S2", ["R1"],
  "If the flatmates genuinely cannot say what they agreed to, ambiguity is the plainest reading and the alternatives I am putting forward are harder to establish from the material than the account's reading is."),
 ("K.o4.bearing.S1", ["R1"],
  "If ambiguity is in fact the plainest reading, the objection comes down to a complaint about sequencing rather than about substance."),
 ("K.p1.text.S1", ["R1", "R3"],
  "Whether the later disagreements concern what the words meant, whether the agreement still binds after a schedule change, or who has standing to raise the issue is not stated by the material."),
 ("K.p1.text.S2", ["R1"],
  "These are distinguishable and the account does not tell them apart."),
 ("K.u1.text.S1", ["R1", "R3"],
  "Ask for the account to be read with its own o1 taken as a live competitor rather than a caveat: set out the alternative readings (ambiguity, renegotiation, legitimacy) as rival hypotheses and build the probe to tell them apart, not merely to measure recurrence."),
 ("K.u1.action.S1", ["R1", "R3", "R5"],
  "Rework the framing so that the conversational-form reading and the ambiguity reading stand side by side, the spec move being one probe among several."),
]

PROSE_BODY = [
 ("B.P1.S1", ["R1"],
  "The account I am objecting to is the one that makes the verbal-agreement memory gap the central mechanism, with the written record plus weekly check-in as the natural remedy."),
 ("B.P1.S2", ["R1", "R3"],
  "My grounds lie inside the material rather than in facts brought in from elsewhere."),
 ("B.P2.S1", ["R1", "R3"],
  "Three elements are named in the stated problem: agreements that later mean different things, work schedules that change, and one friend who has begun avoiding the conversations."),
 ("B.P2.S2", ["R3"],
  "Under the account's reading the first element is made primary and the third is demoted to a symptom — 'avoidance is a symptom worth understanding before it's treated as a problem to correct.' That ordering is not forced by the material."),
 ("B.P2.S3", ["R1"],
  "Taken the other way round, the avoidance is the load-bearing fact and the chore disputes are where an already-shifting household keeps failing to talk."),
 ("B.P2.S4", ["R1"],
  "On that reading, the memory-gap conjecture is a description of the surface, and a written record may simply give the same unresolved conversation a fresh medium."),
 ("B.P3.S1", ["R1"],
  "There is a second difficulty."),
 ("B.P3.S2", ["R1", "R2"],
  "A memory gap is not the same thing as a genuine disagreement about terms, and the account slips between them."),
 ("B.P3.S3", ["R1"],
  "'I'll do the dishes' standing for different amounts of work under different schedules is not a case of forgetting; it is a case of ambiguity together with changed circumstances."),
 ("B.P3.S4", ["R3"],
  "A written record settles what was said by whom."),
 ("B.P3.S5", ["R1", "R5"],
  "It does not settle what 'this week' or 'done' should mean while schedules keep shifting, since that is a normative question each person answers differently and no note adjudicates."),
 ("B.P3.S6", ["R2", "R5"],
  "The proposed test — watch whether 'what was agreed' disputes fall — can therefore show a drop in memory disputes while leaving the substantive disagreement untouched, or can show no drop because the disputes were never memorial ones."),
 ("B.P3.S7", ["R1", "R3"],
  "Either outcome is readable as support for the account, which is a weakness rather than a strength."),
 ("B.P4.S1", ["R1"],
  "The account also names its own unresolved dependency without settling it: the proposal assumes all three flatmates can talk without a mediator, 'which the avoidance itself puts in question.' That is not a peripheral caveat."),
 ("B.P4.S2", ["R1", "R3"],
  "If the avoidance is the mechanism by which the group has lost the ability to hold the conversation, then a weekly check-in is a proposal to do more of the thing that already failed, addressed to the person who withdrew from it."),
 ("B.P4.S3", ["R3"],
  "The separate approach to that friend is the part of the account most responsive to the material, and it is flagged by the account as most contestable."),
 ("B.P4.S4", ["R1"],
  "I would turn that ordering round: the approach, or something that names the avoidance as the problem, is the load-bearing move, and the record is optional."),
 ("B.P5.S1", ["R1"],
  "I cannot make out from the material which reading is right, and I am not claiming the memory-gap account is false."),
 ("B.P5.S2", ["R1", "R3"],
  "What I have grounds for objecting to is order of operations and the diagnostic confidence that rests on a conjecture the account itself calls a conjecture."),
 ("B.P5.S3", ["R1", "R5"],
  "The clean version of the account would keep the retrospective possibility (agreements drifted because nobody recorded them) apart from the prospective one (record them now and drift will stop), since the material supports the former and not the latter."),
]

PROSE_COMMITMENTS = [
 ("C.P1.S1", ["R1", "R3"],
  "To take this objection up is chiefly to commit to holding two readings side by side rather than defending one."),
 ("C.P1.S2", ["R1"],
  "If the continuation treats the memory-gap reading as primary, I would want the avoidance-as-central reading set out in the same breath so the household's own account can discriminate between them, rather than one reading being quietly assumed."),
 ("C.P2.S1", ["R1"],
  "I am proposing a sharpened test, and it can fail in a direction that tells against me."),
 ("C.P2.S2", ["R1", "R3", "R5"],
  "If agreements are written down, 'done' is defined, and the recurring arguments nevertheless continue or intensify, that supports the account I am objecting to and tells against my ordering."),
 ("C.P2.S3", ["R1"],
  "I would sooner state that in advance than leave it implicit."),
 ("C.P2.S4", ["R1", "R2"],
  "At present I cannot say which reading is right; that gap forms part of what the objection asserts, not something I am concealing."),
 ("C.P3.S1", ["R1"],
  "I am also asserting a distinction the original account blurs — between memorial and normative disagreement — and the distinction is contestable."),
 ("C.P3.S2", ["R1"],
  "If someone demonstrates that in this kind of household the two are not separable in practice, that the act of writing something down does shift the norms, my criticism loses some of its bite."),
 ("C.P3.S3", ["R3"],
  "I would want that counted as a revision of the objection rather than as noise."),
 ("C.P4.S1", ["R1", "R5"],
  "As to the local trial: if a written record or check-in is attempted, I would want the result reported as the household describes it, including the case where the avoiding friend reads the note as surveillance."),
 ("C.P4.S2", ["R1", "R3"],
  "That would be evidence about the social cost of the intervention, not merely about whether it works, and that risk is already flagged by the account's own framing."),
 ("C.P4.S3", ["R1"],
  "I would treat a quiet week as uninformative in either direction."),
 ("C.P5.S1", ["R1", "R3"],
  "What I am not committing to: I have no basis on which to propose a mediator, a reassignment of chores, or a formalization of the household, and I make no claim that any of those improves on what the original account proposes."),
 ("C.P5.S2", ["R3"],
  "To name alternatives as possible better routes is not to endorse them, and I cannot rank them from the material shown."),
 ("C.P6.S1", ["R1"],
  "If this is continued, the piece of work I would actually take on is setting out the two readings so the difference becomes testable, and then specifying what observation would separate them rather than trying to settle the reading now."),
]
