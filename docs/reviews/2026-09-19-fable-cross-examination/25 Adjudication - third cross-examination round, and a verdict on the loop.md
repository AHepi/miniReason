# 25 Adjudication — third cross-examination round (file 24), and a verdict on the loop

What this file is: the rulings on what both witnesses found in file 24, the third revision, and a judgement about whether a fourth patch-revision is worth running. Short answer: no. The loop has reached the point where each round removes one layer of defects and my replacements add another, while a residue of structural problems survives every rewording because they are not wording problems. §3 says what should happen instead.

## 0. The run

| | deepseek-flash | Atria-Dawn-Preview |
|---|---|---|
| Calls | 27 (3 samples, 9 workers) | 9 (1 sample, 3 workers, streamed) |
| Usable | 27 | 9, after two stream cuts that the harness now retries |
| Wall clock | 12 minutes | 43 minutes |

Also recovered in this window: the two round-two Atria items (S7, S8) lost to gateway errors; their findings are folded in below. Failure modes new to this round: none; the stream cut recurred twice and was retried successfully, which is what the harness change was for.

## 1. My own slips in the third revision (Valid, no argument)

- **1.1** Part XV still lists the selection-artefact case under attack (B) while Part 0 and Part VII say it was moved to (D); 24a marks the move Done. False ledger row.
- **1.2** Part 0 (A) and Part XV say the target's own copy "fails Origin"; Part X now says New can hold for it when the target is not in the repertoire, and that building the mirror from error records is discovering it. The two places contradict each other, and the contradiction is on the central point.
- **1.3** Part VII now says (F2) is "the door" for symmetry explanation; Part XV (B)(i) still says nothing is known to follow from present machinery.
- **1.4** "Mixed provenance does not count as constructed for (G)" — (G) uses Build, not Con; the sentence enforces nothing.
- **1.5** Derivation 6 says "three places" and lists four; σ's typing was added to the transport tuple in Part IV but the four-tuple notation is used everywhere downstream; "the largest contract on which some transport is faithful" need not exist (fidelity on two contracts does not give fidelity on their union).

## 2. Defects that survived a third rewording, ruled Valid

**2.1 The dependence order still has cycles**, and Derivation 6's proof now names four "non-cycles" while the witnesses exhibit two live ones: Build → reason use (whose "represented objection" uses (R)) → Con → Build; and (R) → Con → Build → (E) → p, whose tuple contains ρ_p, defined through (R). Both witnesses, all samples. Each patch closed the cycle it aimed at and left the next. Ruling: the provenance of a question cannot sit inside the question tuple that Account takes as argument, and reason use cannot be stated through representation if construction depends on it. The fix is architectural, not lexical: provenance annotations must live outside every tuple that fidelity conditions take, and Parts IX–XI must be stated over instantiated occurrences only.

**2.2 The sufficiency attack and the extensional stance cannot both stand as written.** Part 0 asks for "a candidate that … plainly explains nothing"; Part V says the semantics has no predicate that separates a mechanism from its faithful copy and does not want one. Both witnesses built the "error-record mirror" — a system that, from itemised failures, constructs a faithful copy of the target, new to its repertoire, and deploys it — and it is anchored, originated, and, on the document's own terms, an explanation. Ruling: this is not a bug. It is a fork the document has refused to take. Either (a) the semantics bites the bullet: there is no fact of "explaining nothing" beyond its predicates, the mirror explains, and attack (A) is restated as "a candidate satisfying the predicates that can be shown, by a difference the semantics ought to but cannot represent, not to explain" — which is attack (C) — or (b) it adds a predicate, which is the very thing Part 0 says it will not do. I take (a), and the next version must say it in Part 0, not bury it in Part V.

**2.3 Silence and the objectivity condition.** "Extended to such pairs by λ" is ill-defined (λ maps components, not edits); "touches" is glossed, not defined; the condition is imposed on the first grade while its anti-silence defence works only for anchored accounts; τ is declared total in Part IV and needed partial here. Both witnesses. Ruling: the objectivity condition belongs to the anchored grade only; τ is total on A_D by definition, so "silence" is not about τ at all but about whether an admitted edit touches an anchored component — which is a condition on λ and D, definable, and I did not define it.

**2.4 The selection witness now excludes ordinary natural selection.** Requiring that survivors coincide exactly with the members faithful on H is what Derivation 3 needs and what no real population does. Both witnesses. Ruling: Derivation 3 must be weakened to what selection data actually give — the survivors are a subset of the members faithful on H, up to a stated error — and the witness records that; the theorem then says the data constrain the survivor only up to that error off H, which is still the point.

**2.5 "Used at the acceptance of the binding" is defined through Part IX's reason use, which is informal**, so the construction/selection separator rests on an undefined term. Both witnesses. Ruling: valid; the separator must be stated in Part IV's own terms (an itemised record instantiated on the route to the event that produced the transport's occurrence), and the finer "used in criticism" reading left to Part IX as commentary.

**2.6 Parts IX–XIII are informal, and every round finds twenty more undefined terms in them.** The list in Part XIV grew from ten to thirty entries in two rounds and is still called incomplete by both witnesses (they are right: "acceptance", "kept", "operative result", "declared contrasts", "evidence leaf", "argument form", "law-imposed limit", "recognised difficulty"…). Ruling: these parts will not become formal by listing their terms. They should be declared what they are — commentary that names the shape of predicates a full theory would need — and removed from every dependence claim, so that Derivation 6 is a claim about Parts II–V and the provenance clauses of Part IV only.

**2.7 The anchored grade's properness and world-kind conditions exclude idealised, partial and coarse-grained mechanisms** — the witnesses' best philosophical point in this round, made independently by both. An idealised model (frictionless, point-mass) is not of one forward kind with its anchor on every admitted pair; a partial mechanism does not cover; a coarse grain does not decompose. Ruling: valid, and it means "anchored" as written is the grade of an *exact* mechanism, which almost nothing is. A useful grade needs an approximation index (Part VIII's (T2) is the tool), and the semantics does not have one. Listed as open.

**2.8 Mixed provenance has no place in ρ_p's codomain or in (R); minimal witnesses may yield none; "the largest contract" may not exist.** Valid; consequences of introducing partial orders without saying what happens at their boundaries.

## 3. Verdict on the loop

Three rounds, thirty-six calls each, about 1,000 findings, about 130 distinct defects ruled Valid, three revisions of 65, 69 and 43 exact replacements. What the rounds show:

- Each revision fixed what it aimed at. The witnesses confirm, round by round, that the named repairs are present and mostly do what they say.
- Each revision introduced a handful of new errors of its own (the count of conditions; a false ledger row; two places saying opposite things about the copy), because replacements were made in one place and not in the three others that said the same thing. That is a property of patching a 100,000-character document by string replacement, and it will recur at every round.
- A residue of about six structural problems survived every rewording (§2.1–2.6), because they are not wording problems. They are choices the document has not made: where provenance lives; whether "explains nothing" is a fact; what the anchored grade is a grade of; how formal Parts IX–XIII are meant to be.

So a fourth round of the same kind would cost another hour of replacements and find another forty defects, a third of them mine. **What is warranted instead is a rewrite from the core outward**: Parts II–V and the provenance clauses of Part IV written as a closed formal system — every symbol declared, every predicate defined only from earlier ones, provenance kept outside every tuple fidelity takes as argument, the extensional stance stated in Part 0 with the mirror as its example, the anchored grade given an approximation index or renamed the exact grade — and Parts VI–XIII rewritten as commentary that makes no dependence claims and is exempt from Derivation 6. That is a different document, not a fourth revision, and it is the next thing to do if the semantics is to be built on. The witnesses can then be run on the core alone, which they can hold whole.

## 4. What holds after three rounds

For the record, what no round broke: the one transport orientation; Inst as a relation and the decomposition oracle named; the three layers; kinds as signatures at a grain and a contract, with the baseline as state; two sorts of kind; account-hood as an extensional fidelity fact; the withdrawal of the merit function, of Derivation 4 as a derivation, of Derivation 10 as a witness; the contract form with a stated scope and declared counterfactuals; the open-limits practice; blindness as the absence of an itemised defect record as the *idea* separating selection from construction. That is the core the rewrite would start from.
