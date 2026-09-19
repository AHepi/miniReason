# 21 Adjudication — cross-examination of the revised semantics (file 20)

What this file is: the rulings on what two outside models found when set against file 20, the revised semantics, on a fresh battery of nine theory items (R1–R9: hidden primitives; derivations; sufficiency against the anchored grade; contract adequacy; the two sorts of kind; provenance and discrimination; questions and the stated limits; internal consistency; file 20 against file 10 and the revision ledger 20a). Rulings are grouped by defect, not by row, because the two witnesses and the three DeepSeek samples converge on the same defects from different items. The verdict is on the text as written; repairs go to the list in §4. Every "Valid" below has been checked against file 20's text by me; where I ran nothing, the verdict rests on reading.

## 0. The run, and its failure modes

| | deepseek-flash | Atria-Dawn-Preview |
|---|---|---|
| Calls | 27 (9 items × 3 samples, 131,072-token cap, 6 workers) | 9 (1 sample, 65,536-token cap, streamed, 9 workers) |
| Usable replies | 27 | 8 (R5, the two sorts of kind, returned no visible content) |
| Wall clock for the whole run | 13 minutes | 13 minutes |
| Reply length, median | 18,000 characters | 20,000 characters |

Failure modes of this run: (1) one Atria reply empty at the cap even with streaming, as before; (2) the DeepSeek R2 samples numbered their findings without titles, so they cannot be skimmed and had to be read in full; (3) both witnesses were given only file 20 for eight of the nine items, so any finding that turns on a definition file 20 inherits from nowhere is theirs to reconstruct — that is by design, since file 20 is meant to stand alone, and it is the point of R1; (4) the count of findings across the run is about 330, of which about 45 distinct defects survive below, so, as before, the count of findings overstates the count of defects by a factor of seven.

## 1. Defects both witnesses found, ruled Valid

**1.1 The conjunct count is wrong.** Part V says "the following five conditions" and displays six. Mine, cosmetic, everywhere at once (R3, R4, R8, R9, all samples). Valid.

**1.2 A cycle between ownership and capability.** Part X defines "owned" through Can (Part XII), and Can requires an *owned* retained realization. Valid, serious: the very kind of cycle the revision claimed to have removed. Fix: Can is the module-level fact that the substrate retains a realization; "owned" is then derived (the process occurrences are executions of realizations the substrate retains), and Can does not mention ownership.

**1.3 The active route uses "represented input", and the anchored grade uses the active route.** So representation (with its provenance condition) re-enters fidelity through condition 4 of the anchored grade, which contradicts Grievance 12's defence of the transport/component asymmetry and Part V's own summary that anchoring is "component fidelity on the full admitted contract". Valid, serious (R1, R5, R8, R9, both witnesses). Fix: define the active route on *instantiated* inputs (Inst), not represented ones; and move actuality of route out of the anchored grade into a separate **operative** condition that is openly historical. The asymmetry then holds: forward kinds and anchoring are history-free; the operative condition is not, and says so.

**1.4 Condition 3 of the anchored grade ("no component's relation is definable as Sol_D or a projection of it") excludes every faithful component.** (F1) requires each active component's relation to *equal* the projection of its anchor's solution set; for any component whose anchor's projection coincides with the projection of the whole target's, condition 3 forbids exactly what (F1) demands. "Definable" is intensional; every check the semantics allows is extensional. Valid, fatal to condition 3 (R3 both witnesses, R9). Fix: drop it. What it was for is handled by properness and by the honest statement in 1.5.

**1.5 The identity account and the modular lookup are anchored accounts.** E = D with the identity transport, and a modular table whose pieces carry each local anchor's signature on every admitted edit, satisfy every remaining condition. Both witnesses say so; Atria adds that this is the document's own kind-relativism and not a refutation of sufficiency *at the index*, but that the reclassification is fiat. Ruling: valid as a description; the semantics must say plainly that account-hood, at either grade, is an extensional fidelity fact, and that "this explains nothing" said of the target's own copy is a complaint about **origin and deployment** (New, Build, Deploy in Part X), not about account-hood. Attack (A) is restated accordingly: a candidate that is an anchored account *and* satisfies Origin while explaining nothing.

**1.6 Properness excludes every single-component target, and the non-circularity witness excludes every single-commitment candidate.** "No anchor is the whole target" forbids the honest account of a one-component target; "proper sub-block B ⊊ Γ" has no witness when |Γ| = 1. Together they also contradict the sentence that the one-component repackaging "satisfies (E)". Valid, serious (R3 Atria findings 1, 7; R8, R9). Fix: properness = the anchors of the active components refine a cover of D's components and the anchor map is injective on that cover, with the whole target allowed as an anchor exactly when D has one component; non-circularity's witness removes a nonempty sub-block, proper when |Γ| > 1.

**1.7 Contract adequacy, as a conjunct of (E), is ill-defined, too strong, too weak, and collides with the frozen index.** Ill-defined: τ, σ and Q are not guaranteed defined off C, and "baseline value" is not fixed. Too strong: any out-of-scope dependence of the target that the candidate does not share fails it, so a legitimately scoped account (the shadow scoped to pole and angle, with the sun's position out of scope) is not an account. Too weak: it compares each side to its own baseline rather than the two to each other, and ignores K. Collides: it makes account-hood at C depend on the module in force, against Part VIII's historical index and Grievance 4's two-index treatment, and it collapses the two-grade architecture. Valid on every count (R4 all samples, both witnesses; R8; R9). Fix: remove adequacy from (E); (E) has five conjuncts again. Restate it as the second index of an *objectivity* claim, indexed to the module in force, and define "protective" as: there is an admitted pair outside C at which the candidate's translation and the query are both defined and the candidate's pulled-back answer differs from the target's. Silence about a change is a stated limit; being wrong about a change the scope hides is protection.

**1.8 Excluding all baseline pairs (1, b) from kind identity erases boundary-only dependence, and "state" is a category error for a relation.** The intent was to stop the identity edit at the question's baseline separating things that differ only in position. The text excludes the identity edit at *every* boundary, which removes a genuine response to a change of boundary. Valid (R5 all samples, R8, R9). Fix: exclude only (1, b₀); say "the relation at the baseline is the component's state" as a gloss, not a definition.

**1.9 Forward kind is defined for two components and then used between a component and an anchor subnetwork.** Valid, easy (R5, R8, R9, Atria R2). Fix: the relation is defined for any two subnetworks using the subnetwork signature already in Part II; a component is a one-element subnetwork with all ports visible.

**1.10 Historical kinds, and question provenance, borrow witnesses Part IV defines only for transports.** Valid (R1, R5, R7, R8, R9, both witnesses). Fix: the provenance of any content's occurrence is the provenance of the transport by which that occurrence represents it under (R); a component occurrence's history is the history of the binding that realizes it. One definition, then used for components and questions.

**1.11 The selection witness is still gerrymanderable, "causally responsible" is a primitive in disguise, the non-triviality clause is ill-typed ("no event is a faithful transport"), blindness is not a conjunct, and "no target instantiated before the variation" is false of ordinary selection.** Valid on all five (R6 both witnesses; R1; R9). Fix: replace causal responsibility with a difference-making clause stated in module terms — at least one eliminated member differs from t at some pair of H on which it failed the survival condition and t did not; type the non-triviality clause as "no event of Σ_h instantiates an organization held to t, to H, or to the survival condition by a faithful transport"; make blindness a conjunct of Sel; drop the "no target instantiated" separator and let blindness and the itemised defect representation be the *only* separator; and require the itemised defect representation on the route as a conjunct of Build, which Part X currently lacks (R8.24, R9.4).

**1.12 The precedence rule makes provenance reporter-relative.** "Constructed if a construction witness exists" lets a later gerrymandered witness reclassify a plainly selected transport. Valid (R6 both witnesses). Fix: provenance is that of the earliest witness in ≺_h whose events produced the transport's occurrence; later histories are maintenance and do not change it.

**1.13 The merit condition for found questions is dangling, ill-typed and trivial.** It is a conjunct of no defined predicate; "would repair under (P)" is a counterfactual (P) does not define; declaring O to fit the question satisfies it. Valid (R7 all samples, both witnesses). Ruling: withdrawn. The slot "what makes a found question worth finding" is empty again, as it was in file 10, and Part XV says so.

**1.14 Derivation 5's question-organization does not do what it claims.** Its solutions are not exactly the coherently posed questions (coherence is a global condition on Sol_D, not a local component); it omits b₀, O_p and ρ_p; "add a pair to K with a meaning" is not an edit in the sense of (O); "toggle" conflates membership in C with the S/K partition; and one organization whose solutions are *all* questions cannot make a particular question New. Valid (R7 all samples, both witnesses; R2). Ruling: Derivation 5 is downgraded to a construction sketch with these gaps listed; question-finding is representable *if* the sketch can be completed, and that is now an open point under attack (E).

**1.15 "Surprise on C entails loss of (R) and Deploy" has the wrong shape.** (R) is existential over organizations and transports; a violation of one transport does not remove representation by another. Valid (R8, R9, both witnesses). Fix: the surprised transport no longer witnesses (R); Deploy *through that transport* is lost.

**1.16 The coherence condition "S and K are disjoint from each other's complements" is malformed.** As written it forces S = K. Mine. Valid. Fix: S ⊆ C_adm and K ∩ C_adm = ∅.

**1.17 C_adm is typed as edits in one place and edit–boundary pairs in another.** Valid, easy. Fix: A_Θ(o) × B.

**1.18 Ans_E and Ans_S are used without definition; the transport carries no query translation.** Valid (R1, R4, R8, both witnesses). Fix: Ans_E(τ(a), σ(b)) := Q(E, τ(a), σ(b)) with Q read through π; the query is part of what the transport carries.

**1.19 (EK) applies Account to a content; Part VI's (S) needs the fixed t and Γ; Origin says a *system* instantiates a question.** All three are type slips from the arity change. Valid, easy (R8, R9, both witnesses). Fix: Account(E_c, p_c); use the four-place form in Part VI; "an occurrence of s instantiates".

**1.20 The reversed-calculation parenthetical is false.** I wrote that τ is undefined at the intervention; the reversed organization has a component assigning H (the calculation) and (F2) fails because the translated intervention on that component does not reproduce the target's change of L. Valid (R8, R9, Atria R1). Fix: delete the parenthetical; the original sentence was right.

**1.21 Derivation 6's "no predicate left undefined" is false.** The witnesses list: problem-directed activity, explanatory use, role bindings, operative deliberative rule, achievement predicate, continuing organization, Admit, Poss, realized transport, actually encountered, complete critical episode as a predicate, β and Ω. Valid (R1 both witnesses, R9). Ruling: Derivation 6's consequence is restricted to the dependence order among the *defined* predicates, and Part XIV carries an explicit list of the informal terms, each marked "declared with the use" or "not yet defined".

**1.22 Derivation 3 needs survival to be equivalent to fidelity on H, and its population differs from Part IV's.** Part IV makes fidelity on H necessary for survival; the proof needs sufficiency. Valid (R2 Atria, R8, R9). Fix: state the hypothesis; use one population type (realized organization–transport pairs) in both places.

**1.23 Derivation 8 assumes solution preservation and does not show provenance preservation.** Valid (R2 Atria). Fix: state solution preservation as a hypothesis on φ; provenance preservation follows only if φ carries histories with their events, which is then a hypothesis too.

**1.24 Grain admissibility uses "signature" without a contract and "realizes" without a definition; grain is both a declared index and constrained.** Valid (R8, R9). Fix: admissibility is relative to C_adm; "realizes" means the edit is in A_Θ(o) and changes the component's relation.

**1.25 The four open cases in Part XV are mis-sorted.** Both witnesses: symmetry is the only genuinely unclosable one with present machinery, because the missing thing is a constraint among E's components; the artefact case is the most closable (two targets are not forced; a provenance clause in (E) is what is missing); the impossibility case is already handled as far as it can be, with its force scoped by design; mathematics is closed relative to a declared admission relation and should not be listed under a quantifier the document itself declares inapplicable. Valid. The list is re-sorted accordingly.

**1.26 Part 0 asserts the two-sorts-of-kind dichotomy as fact where Part XV calls it a conjecture.** Valid, wording (R9 both witnesses).

**1.27 Smaller, all valid:** "relevant" survives once (in Attempt); β and Ω are never defined; (I3) is missing from Part XV's error list; "understanding" is listed as derived and never defined; Part IV's "the organization t targets" is ambiguous against the orientation rule; Part X's construction-witness list omits the two items Part IV says it contains; Derivation 10's "selected" tracker population does not satisfy the new Sel and its two stipulations about the population conflict; Derivation 10 cites Derivation 1 without injectivity; Grievance 2's "not a fact about the world" against Part V's "world-kind" needs the sentence that world-kind is a fact about (Θ, ℓ, C_adm), the module being the semantics' only access to the world; the sufficiency attack was moved to the anchored grade without saying that the target of the attack changed; 20a marks two rows Done that are not.

## 2. Findings ruled Invalid or Partly valid

| Finding | Ruling | Why |
|---|---|---|
| "The anchored grade carries no provenance condition, so a declared transport can be 'about the actual mechanism'." | **Partly valid.** | True as stated, and intended: anchoring is a fidelity grade; whether the carrier *represents* the mechanism is (R), which has the provenance condition. But "about the actual mechanism" should be reserved for the conjunction, and the text should say so. |
| "Selection provides only fidelity on H, so (R) — which needs fidelity on the content's contract — is generally unestablished for the primitive layer." (R8 Atria 11) | **Valid, and a consequence worth keeping.** | Not a defect: it says what a selected transport represents is the content on the contract it is actually faithful on, which can be smaller than the declared one. That is fallibility stated exactly, and it goes into Part IV as a consequence. |
| "A modular lookup is an anchored account, so sufficiency is refuted." | **Invalid as a refutation; valid as a description.** | See 1.5. The semantics is extensional and says so; the complaint is about origin, which Part X handles. |
| "Inst plus a new admissible grain already covers inventing a new dimension of variation." | **Partly valid.** | A dimension the module already licenses at some grain is representable by a new organization attribution (Build over a new D); a dimension the module does not license is not representable at all. The stated limit is relocated: it is the physical module's fixity, and Part X's sentence is corrected to say so. |
| "The adequacy condition is a cheap refutation instrument over an unbounded domain." | Valid against the conjunct form; moot once adequacy leaves (E). | — |
| "The scalar-summary exemption lets a scalar encode the defect." | **Partly valid.** | A scalar that is a sufficient statistic of the itemised records is not "how many failures, how badly"; the definition must say *aggregate* summary: a function of the multiset of failures that is invariant under permuting which record failed. |
| "Blindness is inconsistent with Part I's 'an idea may be entertained without justification'." | Invalid. | Different objects: blindness is about the route from defect to variation; Part I is about entertaining conjectures. |

## 3. What survived

The repairs that both witnesses attacked and did not break: the single transport orientation (R8 Atria: "consistent with Part IV's orientation"); Inst as a relation and the decomposition oracle named; the three layers; Derivation 4 as a remark; Derivation 1 with the injectivity hypothesis (once Part V cites it with the hypothesis); Derivation 3's closure hypothesis (once the equivalence hypothesis is added); the contract form with S and K, provided fidelity over K is defined (it is not yet: Sol_D is undefined on non-admitted edits, so K needs its own relation supplied with each meaning); the declared admission relation for mathematics; the discrimination requirement as an *idea* (its clauses need the fixes in 1.11); the withdrawal of the merit function; the open-limits list as a practice.

## 4. The second revision list (not started)

1. Five conjuncts; adequacy moved to a separate objectivity condition indexed to the module, with "protective" defined by disagreement where the candidate is evaluable (1.1, 1.7).
2. Ownership derived from Can; Can free of ownership (1.2).
3. Active route on instantiated inputs; actuality of route an openly historical *operative* condition outside the anchored grade (1.3).
4. Anchored grade: properness allowing whole-target anchors for one-component targets; condition 3 deleted; world-kind on (Θ, ℓ, C_adm) with the sentence that this is the module's world; the extensional statement about copies and modular tables, with origin as the place where "explains nothing" is adjudicated (1.4–1.6, 2).
5. Kind identity excludes only (1, b₀); forward kind defined for subnetworks (1.8, 1.9).
6. One provenance definition for contents via (R)'s transport; components and questions inherit it (1.10).
7. Sel: difference-making clause in module terms; typed non-triviality; blindness a conjunct with an aggregate-summary exemption; Build requires the itemised defect representation on the route; provenance by earliest producing witness (1.11, 1.12, 2).
8. Merit condition withdrawn; Derivation 5 a sketch with its gaps; question-finding open under (E) (1.13, 1.14).
9. Surprise consequence reshaped (1.15); coherence condition fixed (1.16); C_adm typed (1.17); Ans_E defined with a query translation (1.18); arity slips fixed (1.19); parenthetical deleted (1.20).
10. Derivation 6 restricted and the informal-term list added; β, Ω defined or removed; (I3) listed (1.21, 1.27).
11. Derivation 3's equivalence hypothesis and single population type; Derivation 8's solution-preservation hypothesis (1.22, 1.23).
12. Grain admissibility relative to C_adm with "realizes" defined (1.24).
13. Part XV's open cases re-sorted: symmetry open; artefact closable by a provenance clause; impossibility scoped; mathematics relative to a declared admission relation (1.25).
14. Fidelity over K defined: each counterfactual pair comes with the relation it imposes (§3).
15. The consequence in §2 row 2 added to Part IV.
16. Part 0 reworded so the dichotomy of kinds is a conjecture; the attack (A) restated for the anchored grade plus Origin; 20a's two rows corrected.

## 5. Failure modes of this adjudication

Grouping by defect risks folding a distinct finding into a neighbour; the per-row replies remain in the folder for anyone who wants to check. I did not run anything: every ruling here rests on reading file 20 against the witness's quotation, and the two places where that is least safe are 1.4 (whether condition 3 really collides with (F1) for *every* faithful component or only for those whose anchor projection equals the target's — it does for the latter, which is enough) and 1.6 (whether the singleton witness is unsatisfiable — it is, by the word "proper"). The witness count is again inflated by overlap; the list in §4 is the deliverable, and it has sixteen items where the first list had seven headings.
