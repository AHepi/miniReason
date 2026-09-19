# 26 Skill experiment — two method skills on file 20

What this file is: the results of running the file-20 cross-examination a second and a third time with a *method skill* pasted into the witnesses' instructions, and the comparison with the plain run that file 21 adjudicated. The first skill is the user's "hard-to-vary" skill (David Deutsch's test, written on top of file 10's terms). The second is the user's "story-critique" skill (a scene-by-scene method for stories, applied to a theory document on purpose, to see what a different style does to the thinking). Everything in file 21 is left as it was; this file compares against it and does not revise it. The question asked was: do the results change for the better, do the skills incapacitate the models, or neither.

Coverage of this file: both DeepSeek runs are complete (27 replies each). The Atria runs were still landing when this file was written (two hard-to-vary replies in, three items failed at the gateway after all their retries, none of the story-critique ones), so Atria is reported here only where a reply exists and the rest goes in a separately named supplement (26c). The design was frozen before any reply was read and is published on its own as file 26a; the per-reply working log is file 26b.

## 1. The short answer

The skills did not incapacitate either model. Both skills made the DeepSeek witness better than the plain prompt in three measurable ways and worse in none that matters:

- **Every one of file 21's defects was found again** under both skills (recall of the 27 known groups: 27 of 27 for hard-to-vary, 27 of 27 for story-critique, counting a group as found when any of the three samples states it).
- **About forty new defect groups were found that the plain run missed**, most of them by both skills independently, and the largest of them, a second definitional cycle, was found by eight of the fifty-four DeepSeek replies and by none of the thirty-six plain-run replies.
- **The false-finding rate stayed low and became visible**: three false textual claims in fifty-four replies, all three on one item (the transport-orientation candidate), two of them from the story-critique skill, and each caught by another sample of the same run that checked the passage and rejected the candidate.

The two skills differ in what they are good for, and the difference is the useful result. Hard-to-vary produces marks on parts ("held, loose, idle, borrowed, unknown") and forces the witness to build a rival or a counterexample, so it finds structural looseness and constructs cases. Story-critique forces a "corrections first" check of the item prompt against the page, a "planted and never collected" pass and a "cause versus label" pass, so it finds unkept promises, unmatched lists, and conditions that are stated and never used. Neither is a truth-meter, and both witnesses said so in nearly every reply, which was itself a change from the plain run.

## 2. The runs, and their failure modes

| Method | Model | Calls | Empty | Median reply | Longest | Median time | Median completion tokens (of which reasoning) | Carries the skill's report structure |
|---|---|---|---|---|---|---|---|---|
| plain (file 21) | deepseek-flash | 27 | 0 | 18,400 chars | 33,700 | 153 s | 35,200 (30,200) | not applicable |
| plain (file 21) | Atria-Dawn-Preview | 9 | 1 | 19,100 | 32,600 | 461 s | 38,100 (32,400) | not applicable |
| hard-to-vary | deepseek-flash | 27 | 0 | 28,700 | 45,900 | 207 s | 43,900 (37,200) | 26 of 27 |
| story-critique | deepseek-flash | 27 | 0 | 25,300 | 49,700 | 200 s | 41,400 (35,700) | 25 of 27 |
| hard-to-vary | Atria-Dawn-Preview | 2 of 9 at writing (3 items failed after retries) | 0 | 31,700 | 38,700 | 497 s | 41,200 (33,400) | 2 of 3 |
| story-critique | Atria-Dawn-Preview | not started at writing | | | | | | |

Numbers from `witness-replies/compare_runs.py` over the reply records. "Carries the skill's report structure" is a keyword check (frozen question, marks, next step, and so on), confirmed by reading: the one hard-to-vary reply without the full frame (R6 sample 2) still numbered its findings and gave marks, and the two story-critique replies without the full frame (R8 samples 1 and 2) still ran the passes.

Failure modes of these runs, in the order they matter:

1. **Atria's gateway is the bottleneck, not the skill.** With a 55,000-character system prompt on top of the 92,000-character document, Atria's streamed replies were cut at 159,000 reasoning characters, 83,000, 20,000 and 12,000, and returned 503 and 504 gateway errors, all retried by the harness. Three replies landed in the first 27 minutes; the plain run had all nine in 13 minutes. This is the same failure the operations lesson already records, made worse by the longer prompt.
2. **Longer replies, no empties.** DeepSeek's replies grew by half under both skills and none hit the 131,072-token cap; reasoning tokens grew by a fifth. The cost per reply rose from about 35,000 to about 43,000 completion tokens.
3. **Over-production in one reply.** Hard-to-vary R6 sample 2 produced fifty-six numbered findings, most of them restating a mark per clause; its useful content was a third of R6 sample 0's. The skill's own "no scores, no counting" warning did not prevent this.
4. **One skill defect surfaced.** Atria's hard-to-vary R2 reply reported that the skill's `word-list.md` attributes to "Derivation 2" a claim ("two candidates that no listed change can separate are one account") that file 20's Derivation 2 explicitly denies. The witness was right: the word list was written against file 10, and file 20's Derivation 2 was rewritten. Every reply of both skills also noted, unprompted, that the skill's vocabulary is the document's own and refused to use it as evidence, which is what the framing asked for.
5. **The story-critique frame made the witness re-derive the item prompt.** Its "corrections first" step turned every item prompt into a claim to be checked against the page. In twelve of twenty-seven replies that step corrected the prompt, and in nine of those the correction was right (for example, that blindness is not a conjunct of the selection witness, or that the "non-declared transport" clause of attack (A) bars nothing). In three it was wrong (the orientation candidate, §6).

## 3. Did the skills incapacitate the models? No.

Prediction (a) of file 26a said neither skill would empty more replies than the control. Confirmed for DeepSeek: zero empties in fifty-four calls against zero in twenty-seven. For Atria the answer is not yet in; the two replies that landed are as long and as structured as its plain-run replies, and the losses so far are gateway cuts, which the plain run also had.

The stronger form of the worry was that a method written for stories would make the witness talk about the method instead of the document. It did not. Every story-critique reply said in one line which passes did not transfer (bodies, meals, faces, camera versus prose, lucky meetings) and then ran the ones that did on the document's Parts as scenes, its definitions as characters, and its attack list as the promises of its type. The one place the frame visibly cost something was the "medium check", which several replies ran as a one-line formality.

## 4. Recall of the twenty-seven known defects

File 21 ruled twenty-seven defect groups Valid (1.1 to 1.27). Both skills found all twenty-seven with DeepSeek. The table gives, for each group, the item and sample that stated it most clearly under each skill; "all" means every sample of the item.

| File 21 group | Hard-to-vary | Story-critique |
|---|---|---|
| 1.1 five conditions, six conjuncts | R1 s0, R3 s2, R8 all, R9 all | R3 s1, R8 s0, R9 all |
| 1.2 owned ↔ Can cycle | R1 all, R9 s1 | R1 s1, R8 s0, R9 s0 |
| 1.3 active route carries (R) | R1 s2, R5 s0, R5 s2 | R5 s1, R5 s2 |
| 1.4 condition 3 "definable" | R3 all | R1 s2, R3 s0 |
| 1.5 identity copy and modular lookup are anchored | R3 all (worked out in full, twice) | R3 all (worked out in full, twice) |
| 1.6 properness and the singleton witness | R3 all, R9 all | R1 s2, R3 s1, R5 s0, R9 all |
| 1.7 contract adequacy: ill-defined, too strong, too weak, index | R4 all | R4 all |
| 1.8 baseline pairs excluded | R5 all | R5 all |
| 1.9 forward kind between a component and a subnetwork | R2 s1, R8 s2, R9 all | R1 s0, R2 s0, R9 all |
| 1.10 historical kinds borrow transport witnesses | R5 all | R5 all, R9 all |
| 1.11 the selection witness's clauses | R1 all, R6 all | R1 all, R6 all |
| 1.12 precedence is gerrymanderable | R6 all | R6 all |
| 1.13 the merit condition | R7 all (with a disagreement, §7) | R7 all (with the same disagreement) |
| 1.14 Derivation 5 | R2 all, R7 all | R2 all, R7 all |
| 1.15 surprise entails loss of (R) | R8 all | R8 all |
| 1.16 S and K "disjoint from each other's complements" | R1 s0, R1 s1, R2 s0 | R1 s1, R2 all, R4 s2, R9 all |
| 1.17 C_adm typed two ways | R1 s0, R1 s1 | R1 s2 |
| 1.18 Ans_E undefined | R1 s2, R4 s0, R9 s2 | R1 s1, R1 s2, R2 s2 |
| 1.19 arity slips: Account(c,p_c), "s instantiates a question" | R8 all, R9 all | R1 s1, R8 s0, R9 all |
| 1.20 the reversed-calculation parenthetical | R4 s0, R8 s1, R8 s2, R9 s0 | R1 s0, R8 s1 |
| 1.21 Derivation 6's undefined predicates | R1 all | R1 all |
| 1.22 Derivation 3's equivalence hypothesis and population | R2 all | R2 s0, R2 s2 |
| 1.23 Derivation 8's hypotheses | R2 all | R2 s0, R2 s2 |
| 1.24 grain admissibility and "realizes" | R1 s0, R1 s2, R8 s0 | R1 s1, R8 s0 |
| 1.25 the open cases mis-sorted | R7 all | R7 all |
| 1.26 Part 0 states the dichotomy of kinds as fact | R5 s0 (as two scopes) | R5 s1, R5 s2 (as two statements) |
| 1.27 the smaller items | R1, R2, R9 | R1, R9 |

Prediction (b) of file 26a said hard-to-vary would find fewer typing slips because it does not read clause by clause. Wrong: it found them all, because its "hunt the answer in the starting points" and "look inside" tests sent it clause by clause anyway.

## 5. New findings, ruled

Everything below is a defect of file 20 that file 21 does not contain, ruled against the text as file 21's rules require. "Verified" means I checked the passage in file 20 myself; "reading" means the ruling rests on the witnesses' quotations and my reading of them. Where a finding extends a file 21 group, the group is named. The witnesses that found each are listed so the two skills can be compared; "htv" is hard-to-vary, "sc" is story-critique.

**Structural (would survive a rewording)**

1. **A second definitional cycle through the repertoire.** Verified. Build's nontriviality clause says a binding is nontrivial when it is "neither a relabelling of a binding already in the repertoire" nor obtainable by ≡_ℓ; the repertoire is "the set of contents deployable in some nontrivial use respect"; Deploy requires (R); (R) requires Sel ∨ Con; Con requires a construction witness, which is Build's. So (R) → Con → Build → repertoire → Deploy → (R), and Part XIV's sentence "Part X's witnesses … depend on Inst and ≡_ℓ but not on (R)" is false as written. The cycle the document says it broke (through the represented target) is broken; this one is not. Two repairs were offered: index the repertoire to before e, as (N) already does with R_<e, or replace the repertoire by a declared binding store. Also a type slip: the repertoire is a set of contents and the clause speaks of a binding in it. Found by htv R1 s0, s1, s2, R2 s1, R6 s0; sc R1 s0, s1, s2, R2 s0. Not found by Atria's htv R1 reply, which marked "no cycle" as held; Atria's htv R2 reply found a different second path, through the critical episode's "content-sensitive response", reason use, active route and "represented input". Valid, serious; the strongest finding of the experiment.
2. **Part VI's support machinery is broken by the singleton witness, and by the two-place Account.** Verified. S_{E,p} = {W ⊆ Γ : Account(E|W, p)}; a one-component E|W cannot satisfy non-circular dependence (file 21's 1.6), so S can contain no singleton and Part VI's own examples ("Redundant routes: S = {{a},{b},{a,b}}", "Interference: S = {{a}}") are impossible as written. Separately, Account(E|W, p) re-quantifies t and Γ existentially, so W need not be the active set of E|W, and the finite monotone theorem then assumes an upward closure Part VI says it does not assume. Found by sc R1 s2 (the singleton consequence); htv R8 s0, R8 s1, R8 s2, R9 s0 and sc R8 s0 (the re-quantification). Valid, serious.
3. **One question-organization per target makes every question on that target a recoding of every other, so New fails and Part III is contradicted.** Reading, on the construction as quoted. Derivation 5's D_p has ports for all of A×B, for Q, for S and for K, with D and b₀ as its fixed boundary; a particular question is a valuation of those ports. Part X's ≡_ℓ compares organizations up to a bijection of ports, domains, components and boundaries, and never mentions valuations. So two questions differing only in scope or query are one organization up to valuation, hence content-preserving recodings, hence a second question on D is never New, against Part III's "Two questions with the same D and different (C, Q) are different questions". Repair: put (C, Q, S, K) in the boundary, or define newness for questions over their tuple. Found by htv R2 s1, R7 s0; sc R7 s1. Valid, serious; it puts one horn of attack (E) on the page.
4. **The anchored grade extends only (F1) to C_adm, not (F2).** Verified ("Anchoring is therefore component fidelity on the full admitted contract"). A candidate whose components each track their anchors on every admitted change while its assembly misfits on an admitted change outside C is anchored. Found by htv R3 s2; sc R4 s1 (as the unstated division of labour between adequacy and condition 4). Valid.
5. **The contract is defined as a set of admitted pairs and then made to contain K, "pairs the module does not admit".** Verified (Part III's opening sentence; Part II's "a contract C ⊆ A×B"). Fidelity over K is therefore undefined at the level of types, not only of relations, which sharpens file 21 §3's item 14. Found by htv R9 s1; sc R8 s1, R9 s0, R9 s1, R9 s2. Valid.
6. **Condition 4's kind comparison discards the identity-edit pairs of C_adm too.** Verified by the definition of forward kind. A decoy that differs from its anchor only at an admitted identity-edit pair outside C is of one forward kind with its anchor on (ℓ, C_adm) and so anchored, while Part V's gloss says such a decoy "fails 4". Found by htv R5 s2. Valid; extends 1.8.
7. **The two attack lists do not match.** Verified. Part 0's (F) has no entry in Part XV; Part XV's "protective contract" and "mathematical error" entries have no letter in Part 0; (D)'s third disjunct (the layers) is never collected. Found by sc R3 s2, R5 s0, R8 s0; htv R8 s0. Valid.
8. **"The discrimination requirement of Part IV" has no referent.** Verified by search: the phrase occurs in Parts 0, III and XV and never in Part IV. Part XV's collapse test therefore cannot be run. Found by htv R1 s0, R6 s0; sc R6 s1, R6 s2, R7 s2. Valid.
9. **The selection/construction separation is prose only.** Extends 1.11. The selection witness is signed with five parameters; blindness and causal responsibility sit outside the tuple; the itemised defect representation is a conjunct of neither Con nor Build; and blindness is stated route-relative in one sentence and absolute in the next. Found by htv R6 all, R8 s1; sc R6 all, R8 s0. Valid.
10. **The precedence order is idle.** Verified by reading (R), Deploy and (EK): every use of provenance is the disjunction Sel ∨ Con, so which of the two wins changes no truth value; only Part III's found-question clause and Part XV's refutation conditions read "constructed" on its own. Found by htv R6 s0; sc R6 s0, R6 s2. Valid.
11. **A relay of a selected transport falls to "declared" and represents nothing.** Reading. Relay has no construction witness and no selection history of its own, so the precedence rule sends it to declared, and "a declared transport does not make an occurrence represent anything". Found by htv R6 s0; sc R6 s0. Valid; a false consequence the document does not notice.
12. **Condition 3 excludes explanations by a global principle, by shape.** Extends 1.4. A variational or equilibrium explanation has a component whose relation is a projection of the target's solution set and a change-response of its own; condition 3 discards it "by name", while the document advertises that no conjunct inspects a label. Found by htv R3 s2; sc R3 s0, R4 s2. Valid.
13. **The active-route clause excludes eliminative, dispositional and effective-theory accounts, and can be jointly unsatisfiable with the coverage clause.** Reading. A deleted subnetwork is not an actual occurrence; a capacity explanation names parts not on the run; resolution forbids the lumped account; and a touched-but-inactive component (Part VI's redundant route) is required inside an anchor by condition 1 and excluded from the active route by condition 4. Found by sc R3 s0, R3 s2; htv R3 s2. Valid as a set of cases; each needs a carve-out or a concession.
14. **Contract adequacy, five more ways.** Extends 1.7. (i) Part 0's and Part I's definitions of the first grade omit it, and Part V's preamble "under the changes in C" is false of it (verified). (ii) Narrowing the scope enlarges C_adm∖C, so Part XI's sentence about "a later narrowing to rescue adequacy" describes a move that cannot rescue it. (iii) The choice of b₀, a declared parameter, can defeat it. (iv) Under the strict reading of an undefined τ, Part VII's verdict that the reversed calculation "is an account at the identification contract" is false; under the lenient reading, adequacy is blind at exactly the pair it exists to catch. (v) An anchored account cannot fail it, so its only work is at the weak grade; no worked case anywhere lets it decide. Found by htv R4 all; sc R4 all. Valid.
15. **Derivation 3 needs two hypotheses it does not state, and one reading of it makes Part XV's attack (D) impossible.** Reading, confirmed on the proof text. The altered pair "agrees with (E, t) on H" only if (τ, σ) is injective and the survival condition is exactly fidelity on H; Derivation 1 states injectivity and Derivation 3 does not. Under the proof's reading a survivor "determined on C∖H" cannot exist, so exactly one of Derivation 3 and Part XV's (D) can be right as worded. Found by htv R2 s1, R9 s0; Atria htv R2; sc R2 s2. Valid.
16. **Injectivity in Derivation 1 is idle for the set-equality reading.** Checked by me: (F1) equates third coordinates pointwise, and if two pairs collapse the two anchored relations are forced equal, so the image of the anchor's signature is k's whole signature without injectivity; injectivity only makes the index sets correspond one to one. This downgrades file 21's remark that Part V cites Derivation 1 without injectivity to cosmetic. Found by sc R2 s0, R2 s2; Atria htv R2. Valid.
17. **Derivation 7's consequence overclaims adequacy.** Reading. Adequacy catches a scope change where one side stays at baseline; it cannot catch a change through the module or through K, nor a pair where both answers move differently; and Part XV's own "protective contract" item says so. Found by htv R2 s0, R2 s1; sc R2 s0, R4 s1. Valid.
18. **Derivation 2 has no consumer and its (F2) hypothesis is idle.** Reading. Found by htv R2 s1, R8 s0; Atria htv R2; sc R2 s0, R2 s2. Valid, minor.
19. **Derivation 8's restriction lives in the proof, ≡_ℓ cites a narrower map, and 𝒩 is an idle conjunct.** Extends 1.23. Found by htv R2 all; sc R2 s0, R2 s2. Valid.
20. **Γ and the transport data are in none of Part XIV's three boxes; "occurrence" is presupposed and never listed; B is declared, so world-kind is not a module-only claim; A and A_Θ(o) are never related and the occurrence index is dropped in Part III.** Verified for the lists. Found by htv R1 s1, R1 s2, R8 s0; sc R1 s0, R1 s1, R8 s2, R9 s2; Atria htv R1. Valid.
21. **The historical kind, four more ways.** Extends 1.10. It carries no index though Grievance 2 promises every kind-claim does; "descended from, copied from" are idle; the conjecture's second disjunct "no history distinguishes" is trivially false (the predicate "produced by exactly this history") or unadjudicable; the two history notions (the producing history and the active route) are never bridged; attack (C) is stated at two scopes (Part 0 "physically admitted", Part XV "C_adm"); attack (F) never names the actuality clause. Found by htv R5 all; sc R5 all. Valid.
22. **"An edit that sets a port replaces the component assigning that port" makes two assigners of different constants one forward kind.** Reading. A deleted component imposes the full relation, so two constant-assigners differ only at the identity edit, which the kind relation discards; the exclusion's stated reason ("different positions, one kind") does not describe this case. Found by sc R5 s0. Valid; the sharpest counter-case to the exclusion's reason.
23. **The merit condition, five more ways.** Extends 1.13 and 1.14. It swings between trivial (O is declared; "p′ is accounted for" is an obligation any account repairs) and too strong (O fixed; a question that creates its obligation is rejected; evaluated prospectively no deployable account exists yet); it uses (P) counterfactually though (P) is an actual-history predicate over an episode; it quantifies over O where Attempt quantifies over O_p; its trigger "when it is a question" is not well-founded once a question is itself an organization-content; and it makes (G) depend on (P) where Part XIV's order says (P) depends on (G). The document already has the guard it needs ("a record fixed before the candidate is assessed") and does not apply it here. Found by htv R7 all; sc R7 all, R8 s2; Atria htv R1 (the (P)/(G) reversal). Valid; and it changes file 21's ruling from "trivial" to "declaration-relative, unguarded".
24. **Derivation 5's edits are valuations, not edits.** Extends 1.14. Toggling a port changes a value, not a component relation, and no component assigning u_(a,b) is supplied for the edit to replace; "add a pair to K with a meaning" sets u_K and thereby replaces the consistency component it was meant to act under; the edit is one-way in a two-way list; the construction adds three ports the target lacks, which undercuts the "existing A×B" reason for the concept-creation limit. Found by htv R7 s0, R7 s2; sc R7 all. Valid.
25. **The concept-creation limit is a limit on Derivation 5's device, not on the class.** Refines file 21's partly-valid row. Inst is a relation, a finer admissible grain is a recorded new index, and a question about a new target D′ gets the same construction; the flat claim in Part 0 is stated at three widths across Parts 0, X and XV. Found by htv R7 all; sc R7 all. Valid.
26. **Grievance 1 argues from an input-port intervention while (K)'s causal signature is defined by output-port intervention and observation edits.** Verified by the two quotations. The ledger row "Grievance 1 aligned with the formal causal signature" is not done. Found by sc R9 s0, R9 s1, R9 s2. Valid.
27. **Pres(F) applies Account to an explanatory job, and "explanatory jobs" is undefined.** Verified. Found by htv R8 s0, R8 s1, R9 s2. Valid; surviving from file 10.
28. **Bearing declares grounds g and never uses them; (K1) is a condition on the criticism's quality, not on the target's having the defect; and no episode clause ever consults Bearing.** Reading. Found by htv R9 s0, R9 s1; sc R8 s1, R8 s2. Valid; surviving from file 10.
29. **The simulation layer is defined over P, but Derivation 10's S₀ predicts occupancy, which is the field F.** Reading. Found by htv R9 s0. Valid; surviving from file 10 and unnoticed by every earlier round.
30. **Non-vacuity's "excluded by the stated scope S, not silently" is tautological given C's form, and file 10's substantive sentence was dropped, not moved; ledger row G5.3 is false.** Verified by the two texts. Found by htv R9 s0, R9 s1, R9 s2; sc R9 s2. Valid.
31. **Part XV's mathematical-error list omits Derivations 5, 6, 7 and 9, and the case (i) description misdescribes Part VII's two sub-cases.** Verified. Found by sc R1 s1, R2 s0, R2 s2, R8 s0; htv R7 s1. Valid.
32. **Derivation 10's "then (G) holds" omits Attempt, which the scenario itself lists as unsupplied; the swap is an edit, not the footprint bijection (K) needs; and "one forward kind on any contract containing the swap" is over-broad.** Reading. Found by htv R2 s1, R8 s0, R8 s1; sc R2 s2, R5 s1, R8 s0. Valid.
33. **Part 0's "fidelity is over component structure, not over outputs" is true of (F1) and false of (F2), which is an output-projection equality.** Reading. Found by sc R8 s2. Valid.
34. **(EK)'s account transport and deployment transport need not be the same, so a declared transport can do the repair, and (EK) does not state Sel ∨ Con "explicitly".** Reading. Found by sc R8 s0. Valid.
35. **Attack (B) in Part 0 says "any admitted contract" without "physically", so the exclusion of the mathematical case (iv) is not licensed by (B) as stated.** Verified. Found by htv R7 s0. Valid.
36. **For mathematical questions the objectivity guard is the questioner's own declaration, against Part 0's "a claim about representation or creativity cannot rest on it".** Reading. Found by htv R4 s0, R4 s2, R8 s1; sc R4 s2, R7 s2, R8 s0. Valid; the document half-concedes it.

**Smaller (a word or a sentence each), all ruled Valid on reading unless marked**

37. The five statements of what selection needs (Part 0, Part IV twice, Grievance 9, Part XII) are not coextensive while Part XII says there is "no second definition". (htv R6 s0)
38. The non-trivial-pair clause is entailed by the elimination clause and idle. (htv R6 s0; sc R6 s2)
39. The variation operator need only be applied, not responsible; a two-copy population with one discarded variant satisfies every clause; nothing requires H, T or the survival condition to be fixed before the survivor is known. (htv R6 s0, R6 s2; sc R6 s1, R6 s2)
40. Transport identity (type versus token) and "origination" are undefined, so the maintenance clause cannot be applied. (htv R6 s2; sc R6 s2)
41. The scalar-summary permission is idle and licenses the construction-to-selection rewrite that Part XV says would collapse the provenances. (sc R6 s0; htv R6 s0)
42. Con's nontriviality is relative to the system's repertoire, so provenance is not "a fact about events alone". (sc R6 s0)
43. The Part 0 sentence "Anything else is a detail" dismisses the class of items the lists then fail to collect. (sc R5 s0)
44. The anchored grade is summarised as four, three and two conditions in four places. (htv R8 s1, R5 s0; sc R5 s1)
45. "Two provenances" (Part I) against "three provenances" (Part IV) against "distinguished by their histories" while declared has no history; Part XIV gives the contract "its provenance", which Part III denies. (sc R8 s0; htv R8 s0)
46. The question-begging clause's second disjunct fires on a declared transport that (R) says represents nothing. (htv R8 s0, R8 s1)
47. Part VII's background components "anchored to themselves" do not fit properness. (htv R8 s0, R8 s1, R9 s2)
48. Derivation 4 says nothing cites it and Part IV cites it. (htv R8 s1; sc R8 s0)
49. The observation-edit definition never states that the value of the reported port is unchanged. (sc R9 s2)
50. Part 0's disclaimer now admits "one condition under (P)" as a merit function, against file 10's disclaimer. (sc R9 s2)
51. The constitutive conjecture's four items name neither adequacy, the anchored grade nor the merit condition. (htv R9 s1; sc R9 s1)
52. "The proxies are named where they are cited" cites nothing. (htv R9 s0, R9 s2; sc R1 s1)
53. Ans_S is unbound; ρ_p "attaches to the whole tuple" that contains ρ_p; the CT3/CT4 inclusion is unstated; UECS imports an undefined satisfaction relation; Part XIV's package list drops the per-occurrence index. (htv R8 s0, R9 s2; sc R8 s0, R8 s2)
54. Label overloading: (K), (B), (D), (E), (O), (P) each name two things and the document cites labels. (sc R8 s0; htv R1 s2)
55. Part VII asserts that the Leibniz expansion satisfies (F1) and (F2) without writing the components, against the standard Derivation 10 applies to itself. (sc R7 s2)
56. No case is run anywhere in files 10 or 20; the loss of Derivation 10 as a witness leaves the class with no checked instance, and no ledger row prices that as a defect of the system. (sc R9 s1, R5 s0, R6 s2; htv R9 s0)

**Ruled Partly valid or Invalid**

| Finding | Ruling | Why |
|---|---|---|
| "The content-identity clause 'which is defined in terms of it' misdescribes (R)." (htv R9 s0, R9 s1; sc R8 s0) | Partly valid | The antecedent is ambiguous; if "it" is fidelity the sentence is harmless, if content identity it is false. |
| "The odd-order non-circular witnesses are target contrasts, not removals of a sub-block of Γ." (htv R9 s0) | Partly valid | Removing the skewness constraint is an edit of the target family that removes a constraint component; the phrasing invites the misreading. |
| "Part 0's 'beyond one condition under (P)' mis-cites the merit condition." (htv R8 s2) | Invalid | The merit condition is stated "under (P)". |
| "Deploy can be satisfied by a representation of a coarsening of c." (sc R8 s2) | Unverified | Plausible on (R)'s existential; no clause fixes which organization the use task names; not checked further. |
| "(T2)'s exponent should be L^{n−1−k}." (sc R8 s2) | Invalid | The two sums have the same terms. |

## 6. False findings

Three textual claims in fifty-four DeepSeek replies were false on checking, all on the same candidate of item R8 (the item prompt asked whether the transport orientation in Part IV collides with its use in (R)):

- **sc R8 s1** and **sc R8 s2** ruled that Part IV's orientation slogan and (R)'s arrow "cannot both stand", and sc R8 s2 ranked it its first fault. The passage reads "a carrier's organization D is held to the content c it represents by t: c → D", which is the stated rule ("a transport from X to Y is the relation by which Y is held to X") with X = c and Y = D. Consistent.
- **sc R8 s0**, **htv R8 s0** and **htv R8 s1** checked the same passage and rejected the candidate, two of them saying explicitly that the direction is consistent and only the lettering of D clashes.
- sc R8 s1 also claimed that a one-component E|W "gives (F1) and (F2) trivially and S ∋ W for arbitrary W", which ignores the non-circularity witness that no singleton can supply; the opposite of finding 2, and wrong.

Beyond these: one Invalid finding of the "mis-citation" kind (§5's table), two Partly valid, one unverified. Atria's htv R1 reply marked "no cycle" as held on the text, which is false given finding 1, and is the one Atria error so far.

What this shows about the methods: the false findings came from the story-critique frame on the one item whose prompt supplied a false candidate, and two of three samples accepted the candidate while the third ran "corrections first" properly and refused it. The hard-to-vary frame's "flip" and "swap" steps sent all three of its samples to check the passage, and all three got it right. So the story-critique method's own "check the writer's facts first" step is the guard, and it worked two thirds of the time on the one item that tested it.

## 7. Where the witnesses disagreed with file 21, and with each other

- **The merit condition is not trivial.** File 21's 1.13 ruled it "trivial: declaring O to fit the question satisfies it". Hard-to-vary R7 s1 showed that with a nontrivial O a bit-flip in S must be aimed at a failing obligation, and story-critique R7 s2 gave the honest form: the condition is not automatic but its only free input is declared and unguarded, and the document has the "fixed before e" guard one Part away. Ruling changed: the condition is declaration-relative and unguarded, and swings to too strong when O is fixed. File 21's withdrawal of the merit condition stands, for a better reason.
- **Injectivity in Derivation 1.** Hard-to-vary R2 s0 marked it "held"; story-critique R2 s0 and R2 s2 and Atria's R2 showed it is idle for the set-equality reading. My check agrees with the latter (§5, finding 16).
- **The orientation candidate.** Split as in §6.
- **Whether the anchored grade's sufficiency is definitional.** Every R3 sample of both methods reached the same place file 21 did (the identity copy passes everything; "faithful decomposition … in which case it is an account"), and both methods went one step further than file 21: the story-critique replies called the sufficiency claim "definitional, not demonstrable" and moved the decoy question to attack (C); the hard-to-vary replies built the two-component candidate in full and showed the "non-declared transport" clause is what blocks it, not the four conditions.

## 8. Kind of finding: local or structural

Prediction (b) said hard-to-vary would raise the share of structural findings; prediction (c) said story-critique's useful output would be about the order of exposition. Both were half right. Counting the fifty-six new groups above by the method that found them first or most clearly:

| Kind | Hard-to-vary only | Story-critique only | Both |
|---|---|---|---|
| Structural (a condition does not do its job, a cycle, an exclusion of a genuine case) | 6 (findings 4, 6, 10, 11, 12, 15 in part) | 5 (3 in part, 13, 22, 26, 33) | 12 |
| Exposition (unkept promises, unmatched lists, unused definitions, uncollected plants) | 3 | 9 (7, 8 in part, 31, 43, 45, 48, 52, 55, 56) | 5 |
| Wording and typing | 6 | 3 | 7 |

The story-critique frame's distinctive yield is the exposition column: the two attack lists that do not match, the discrimination requirement with no referent, the mathematical-error list that omits the derivations under attack, the definitions that are never consumed, and the observation that no case has been run anywhere. None of that is in file 21, and it is the kind of thing a reviser needs before a rewrite. The hard-to-vary frame's distinctive yield is the constructed case: the product target that condition 3 excludes, the two-component split worked through every condition, the two-copy selection witness, the decoy at an identity-edit pair, and the rival criteria ("a nontrivial binding for D_p" for merit; a declared binding store for the repertoire).

Both methods found file 25's six structural survivors again: the provenance cycles (finding 1 and the Part IX path), the sufficiency-versus-extensional-stance question (§7), the silence-and-objectivity problem (finding 14), the selection witness that excludes natural selection (findings 9, 39), the separator resting on an informal term (findings 8, 9), and the informality of Parts IX to XIII (findings 27, 28, 53). They did so against file 20, where those problems were first stated, which is one more piece of evidence that the loop of files 21 to 25 was patching words while the choices stayed.

## 9. The predictions of file 26a, checked

- (a) No more empties than the control: **confirmed** for DeepSeek; open for Atria.
- (b) Hard-to-vary lowers the raw count and raises the structural share: **half**. The count of numbered items per reply fell (median 14 against 20) while the count of distinct defects rose; the structural share rose. It recovered 1.5 and the provenance cycle more often, as predicted; it did not find fewer typing slips, contrary to the prediction.
- (c) Story-critique produces the fewest defects and the most text about its own limits, with its useful output about exposition: **the first clause was wrong**. It produced as many distinct defects as hard-to-vary; its text about its own limits was one line per reply as the framing asked; its distinctive output was about exposition, as predicted, and also about conditions never used.
- (d) Atria follows the report format more closely: **not decidable yet**; both of its two replies carry the full frame.

## 10. Verdict on the user's question

Better, not incapacitated, on the DeepSeek witness, under both skills, by the three measures in §1. The improvement is not that the skills make the witness cleverer; it is that they make it do two things the plain prompt lets it skip: check the item prompt against the page before attacking, and say for each part what holds it in place. The first produced the corrections-first refusals and the three false findings; the second produced the constructed cases and the "idle" and "never collected" verdicts.

What this does not show. One run per method per model against one control run, at temperature 0.7, on one document, adjudicated by the author of the document. The recall figures are against a list of defects I wrote; a defect the plain run and both skill runs all missed is invisible here. The count of new defects is inflated by the same overlap factor file 21 reported (the fifty-four replies contain about 1,200 numbered findings, of which fifty-six groups survive), and my grouping of them is a judgement. The skills were written by the user on top of the theory under test, and every reply of both skills said so and refused the word list as evidence; whether the shared vocabulary still shaped what the witnesses looked for I cannot tell from the replies. The Atria half of the experiment is not in this file.

## 11. One next step

Do not start a fourth patch round. File 25 already recommended a rewrite from a closed formal core, and the two skill runs sharpened what that core must settle before anything else: where the repertoire and the provenance witnesses sit in the dependence order (finding 1 and Part IX's path), what Account is a predicate of (finding 2, the four-place form throughout Part VI), whether a question is an organization-content or a tuple (finding 3), and whether the anchored grade is fidelity, definability and history together or fidelity alone (findings 4, 12, 13, 44). When the Atria replies are in, the supplement 26c will say whether the same picture holds for the second witness.
