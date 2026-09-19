# 23 Adjudication — second cross-examination round (file 22)

What this file is: the rulings on what the witnesses found in file 22, the second revision, on the nine-item battery adjusted to its text (S1–S9). Grouped by defect. The verdict is on the text as written. DeepSeek answered 26 of 27 calls with content in ten minutes; Atria's first attempt returned nothing on all nine items (see §0) and a rerun is recorded in §5 when it lands.

## 0. The run, and a new failure mode

| | deepseek-flash | Atria-Dawn-Preview |
|---|---|---|
| Calls | 27 (3 samples, 9 workers, 131,072 cap) | 9 (1 sample, 9 workers, streamed, 65,536 cap) |
| Usable | 26 (S4 sample 2 empty at the cap) | 0 on the first attempt |
| Wall clock | 10 minutes | 4 minutes to failure |

**New failure mode.** All nine Atria streams ended at 224 seconds (one at 186) with no finish marker and no usage, after 14,000 to 105,000 characters of reasoning: the provider closed the streams mid-generation. The harness treated a stream that ended without a finish marker as an empty reply; it now treats it as a connection error, so it retries. Whether the cut was caused by nine concurrent streamed requests or by something else is not resolved; the rerun uses three workers. In round one, nine concurrent streams succeeded, so concurrency alone is not the explanation.

## 1. My own misses in the second revision (ruled Valid without argument)

Four items from file 21 §4 were marked Done in 22a and are not done in file 22. These are errors of the revision process, not of the theory.

- **1.1** The non-circular-dependence witness still says "proper sub-block B ⊊ Γ", so a single-commitment candidate still has no witness, and Part V still says the one-component repackaging "satisfies (E)". The contradiction the first round found survives verbatim (S1, S3, S8, S9).
- **1.2** Part 0 (B) still says "four cases are open"; Part XV now sorts them as one open, one closable, one scoped, one relative. Part VII still says "two further families are not treated" (S7, S8, S9).
- **1.3** Part XII's selection paragraph still lists "causal responsibility", which Part IV replaced with the difference-making clause (S8, S9).
- **1.4** Grievance 4 still names an "adequacy condition" that no longer exists (S9).

## 2. Defects introduced or exposed by the second revision, ruled Valid

**2.1 A cycle through Build's repertoire clause.** Build's "nontrivial binding" is one "not already in the repertoire"; the repertoire is defined by Deploy; Deploy uses (R); (R) uses Con; Con uses Build. Derivation 6's three named non-cycles miss this one. Valid, serious (S1 all samples). Fix: define "already in the repertoire" for bindings by instantiation — a binding already carried by some occurrence of s before e, in the module's sense — not by Deploy.

**2.2 Silence is under the candidate's control, so the objectivity condition is vacuous for partial transports.** A candidate can leave τ undefined on the embarrassing pair and pass as "silent"; nothing prohibits partiality and nothing checks the stated reason for an exclusion. Valid, serious (S3, S4, S5, S8). Fix: silence must be structural, not declared: an admitted edit is one the candidate is silent about only when it acts on a component of D outside every anchor of the candidate; for an anchored account, properness's cover clause then makes silence impossible on any touched component, and the objectivity condition has teeth exactly where it should. For an account at C that is not anchored, silence is permitted and the objectivity claim is correspondingly weaker, which is the right result.

**2.3 The same "where the translation is defined" loophole sits in the anchored grade's world-kind condition.** Valid (S3, S5, S9). Fix: the same structural definition of silence; world-kind is required on every admitted pair that touches the anchor.

**2.4 The survival condition "holds exactly when a member is faithful on H" makes selection stipulative, and H can be chosen after the fact.** Valid on both (S6 all samples). Fix: H is *all* pairs occurring as events of Σ_h within C_t, not a chosen subset; the survival condition is whatever the environment enacted, and the witness records the physical fact that, in this population, survival coincided with fidelity on H — a checkable claim, and the hypothesis Derivation 3 needs, not a definition.

**2.5 The blindness/defect-record pair is a separator only if both routes are the same route.** Sel's blindness is on the route from failure to variation; Build's record is on the route to the binding; a process could carry a record on one and not the other. Valid (S6). Fix: both are stated on the route to the event that produced the transport's occurrence; then one process cannot satisfy both for the same transport.

**2.6 "Earliest witness" under a partial order.** ≺_h is partial; incomparable witnesses leave provenance undefined; and a later construction on selected material is misclassified as maintenance. Valid (S5, S6, S9). Fix: provenance is that of the ≺_h-minimal witnesses whose events produced the occurrence; if there are several and they disagree, the transport has **mixed** provenance, which is declared as such and does not count as constructed for (G). "Construction on selected material" produces a *new* transport with its own occurrence, whose earliest witness is the construction; the selected transport keeps its own.

**2.7 The provenance of a content's occurrence is not well-defined when several transports witness (R) on different contracts, and is silent about declared provenance.** Valid (S5). Fix: the provenance of an occurrence's representing of c on contract C is that of the earliest transport witnessing (R) on C; declared provenance is the case where none does and the modeller has entered one.

**2.8 The aggregate-summary exemption is not well-defined ("invariant under permuting which record failed" is incoherent as written), and "how badly" can leak the itemised content.** Valid (S6). Fix: an aggregate is a function of the multiset of failure magnitudes only, with no access to which state failed; "how badly" is a magnitude per failure, not a state.

**2.9 Query translation contradicts (A) unless π is injective on solutions.** Ans_E is defined through π⁻¹ of E's solutions; where π is not injective, the pulled-back query is multi-valued. Valid (S8 all samples). Fix: (A) is stated with the transported query, and the transport carries the query as a fifth datum \(\mathcal Q_E\) with the condition that it agrees with \(\mathcal Q\) through π on C; no inverse is taken.

**2.10 Bearing ignores the criticism's target, defect, grounds and connection; it is Account of E_c and nothing else.** Valid (S1, S3, S8). Fix: Bearing requires Account(E_c, p_δ) *and* that p_δ's target is z and that E_c's boundary conditions are the grounds g — the named data do work.

**2.11 Non-vacuity looks at S and C_adm, so "none looks outside C" is false as stated.** Valid, wording (S8, S9). Fix: "none evaluates fidelity outside C; non-vacuity inspects the record of how C was drawn."

**2.12 The informal-term list is incomplete, and "understanding" is still listed as derived and never defined.** Valid (S1). The missing items: nontrivial use respect; the physical interpretation of histories; carriers and physical location; admitted target chains and owned enabling continuation (RC); the model M in (U3); J_p and "record fixed before"; "description" and "operative use" in scrutinizability; "bypass" and "independently characterized" in barriers; \(\mathcal Rsn\), \(\mathcal V_A\). Fix: list them; delete "understanding" from the derived list or define it as Deploy.

**2.13 Build's defect record need not be relevant to the binding, and "deleting the binding breaks (F1)" is trivial because deleting it makes (F1) undefined.** Valid (S3, S6). Fix: the record must lie on the active route *to the binding constructed* (2.5 fixes the first); "required" means that replacing the binding by any other binding available in the repertoire fails (F1) or (F2), which is defined.

**2.14 The Part XV attack "a protective contract the objectivity condition admits" is impossible by definition.** Valid (S4, S8, S9). Fix: restate as "a scope that excludes an admitted change on which the candidate is *structurally* silent, where the silence is itself the protection" — which 2.2's fix addresses — or delete.

**2.15 Derivation 5's sketch has the wrong gaps.** The witnesses' list: a solution of D_p is a valuation, not a content, so New and Build do not apply to it as written; the component relations of D_p are never given; the target D in the boundary of D_p is a type error; the closure condition is an extra axiom. Valid (S2, S7). Ruling: the sketch is re-labelled as *not yet a construction*; question-finding is representable *conditionally* on a construction that does not exist here.

**2.16 The withdrawal of the merit condition is overstated: Attempt and coherence already filter ("some obligation in O_p fails"; "coherently posed"), and a random new contract does not satisfy (G) as written because Attempt requires a failing obligation.** Valid (S7). Fix: say exactly what filtering remains (coherence; a failing obligation; Newness) and that no condition beyond these separates a finding from a re-parameterisation.

**2.17 Part 0's "matches the mechanism" and "the mechanism" language against Part V's extensional stance.** Valid, wording (S3, S8). Fix: "matches the mechanism at the module's index".

**2.18 The operative condition individuates anchors by history, so Grievance 12's asymmetry is overstated as "denies that a component's history makes any difference".** Valid (S5, S8). Fix: Grievance 12 says the difference history makes is to the *operative* status of an account, never to its fidelity or its kind.

**2.19 Derivation 10's tracker population's survival condition is "prediction of the field", not fidelity on H; it also omits Build's new defect-record clause.** Valid (S8, S9). Fix: scenario wording.

**2.20 Smaller, valid:** Ownership invokes RetReal without its arguments; the transport tuple does not include the query it is said to carry; Part I says "two provenances" and Part IV "three"; "globally indispensable" is used and not defined; Derivation 7 cites Derivation 5 as if it were a construction; Part XIII's question-begging condition ignores (R)'s provenance requirement; the finite monotone theorem's conditions limit its use to the upward-closed case, which should be said where it is applied.

## 3. Findings ruled Invalid or Partly valid

| Finding | Ruling | Why |
|---|---|---|
| "A built, deployed modular table is the sufficiency counterexample." | **Invalid as a counterexample; valid as the statement of the position.** | A process that builds, from itemised defect records, a modular table whose every piece carries its anchor's signature on every admitted edit, has found the mechanism at that grain, and the semantics says it explains. Anyone who holds that it does not must say what more a mechanism is than its responses to every admitted change, and that is attack (C). |
| "Non-circular dependence looks outside C." | Invalid. | The witness edit is τ(a) for (a,b) ∈ C. |
| "Selection and construction can overlap." | **Partly valid.** | Once routes are unified (2.5), a single transport cannot satisfy both; a *system* may hold transports of both kinds, which is what Part IV says. |
| "(F2) already constrains inter-component entailments, so symmetry may be representable." | **Partly valid, and useful.** | (F2) constrains the *assembled* solution set, which does carry some entailments; whether it carries the entailment from invariance to independence depends on the edit set. Symmetry stays open, but the door is (F2), and Part XV should say so. |
| "The artefact case is misclassified as a necessity counterexample." | Valid. | It is a case where the semantics lacks a *condition* (provenance of the target's components), not a transport. Re-sorted under attack (D)/(E) rather than (B). |
| "The analysis-of-kinds conjecture is not refutable as stated." | **Partly valid.** | "No history distinguishes" is operational only relative to the witnesses the module supplies; the conjecture is refutable relative to a stated module and stated grains, and must be indexed so. |

## 4. The third revision list (not started)

1. Apply the four missed items of §1.
2. Repertoire for bindings by instantiation (2.1).
3. Structural silence: an edit is silent for a candidate only when it acts on a component outside every anchor; objectivity and world-kind both quantify over touched components (2.2, 2.3).
4. H = all encountered pairs; survival as an enacted condition whose coincidence with fidelity on H is the recorded fact (2.4).
5. One route for blindness and for the defect record: the route to the event that produced the transport's occurrence (2.5, 2.13).
6. Minimal witnesses under ≺_h; mixed provenance declared; construction on selected material yields a new transport (2.6, 2.7).
7. Aggregate = function of the multiset of failure magnitudes (2.8).
8. Query as transport datum; (A) restated without π⁻¹ (2.9).
9. Bearing with its named data (2.10).
10. Wording of "none looks outside C" (2.11); the extended informal-term list; "understanding" (2.12).
11. "Required" binding defined by replacement (2.13).
12. Part XV's protective-contract attack restated or deleted (2.14); Part XV's artefact case moved (§3).
13. Derivation 5 marked not yet a construction (2.15); the exact statement of what filters remain in (G) (2.16).
14. Wording: "at the module's index"; Grievance 12; Part I's "two"; Derivation 10; the small items (2.17–2.20).

## 5. The second witness (Atria, rerun with three workers: 7 of 9 items answered; S7 lost to repeated 503 errors from the provider's gateway, S8 lost to a stream cut after 116,000 characters of reasoning)

**Failure modes added by this rerun:** the provider returned 502 and 503 "Bad Gateway / Service Temporarily Unavailable" pages for several minutes; streams were again cut mid-reasoning, one after 261,000 characters, so the cut is not a fixed idle timeout; successful replies took 3 to 15 minutes. Atria is usable for this work only with retries, streaming, low concurrency and patience.

Rows duplicating §1–§2 (the singleton witness; "causal responsibility" in Part XII; Part VII against Part XV; "understanding" undefined; the informal-term list; the earliest rule under a partial order; the silence loophole; Derivation 1's injectivity dropped in Part V; the query pull-back; Bearing's idle data) are confirmed by the second witness and not repeated. Additions, ruled:

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **Survival "necessary and sufficient for fidelity on H" makes Sel unsatisfiable by realistic selection**: real filtering is noisy, and the equality was added for Derivation 3's sake. | **Valid, serious; my over-correction.** | Fix: the witness records that, *in this population and history*, the survivors were exactly the members faithful on H — a fact about the run, checkable, and enough for Derivation 3 (which quantifies over that population). No claim that survival is fidelity in general. |
| 2 | **Build's defect record on the route to the binding is instructivist** and in tension with Part I's conjecture-first commitment: it makes construction error-driven, when the position is that conjectures come first and error selects among them. | **Valid, and the best finding of the round.** | The record must lie on the route to the *acceptance* of the binding — its survival of criticism within the episode (Part IX reason use) — not on the route to its generation. A binding may be conjectured blindly; what makes the episode construction rather than selection is that the defect record is *used* in criticising the conjecture, itemised, on an active route to the decision to keep it. Selection's blindness is then the absence of any such use. |
| 3 | Build's non-triviality and "required" clauses are near-vacuous for a system with an empty prior repertoire, so (G) is satisfiable by a one-shot error fix; "not a composition of content-preserving transfers" leaves single relay satisfiable. | **Valid.** | Fix: "not a content-preserving transfer or a composition of them"; and non-triviality measured against the repertoire *and* the incoming carriers, so that an empty repertoire does not make every binding nontrivial. A one-shot error fix that constructs a genuinely new binding is, however, construction, and the semantics should not be embarrassed by that. |
| 4 | Route granularity is undeclared, so "lies on an active route" cannot separate itemised from aggregate; blindness and the record run through Inst, which is many-to-one, so provenance is grain-relative. | **Valid.** | Provenance is indexed to the grain at which the route is described; say so. It is not a defect that provenance is grain-relative; it is a defect that the text did not say it. |
| 5 | The population, history and survival condition are not required to be fixed in advance, so the selection witness can be assembled after the fact. | **Valid.** | Fix: the witness's population, operator and survival condition are the ones the module identifies as *enacted* in Σ_h before the survivor's occurrence; a witness is a description of events, not a choice among descriptions. |
| 6 | The anchored grade's world-kind "has no baseline to exclude" on C_adm (the exclusion is question-relative), and the port bijection in forward kind is not required to agree with λ. | **Valid.** | Fix: world-kind on C_adm excludes the question's baseline pair, since the question fixes it; and the bijection is the one λ supplies. |
| 7 | "Descended from, copied from" are named as historical kinds but are not defined provenances. | Valid, minor. | Either define them (copying is a content-preserving transfer with a witness; descent is a chain of selections) or drop the examples. |
| 8 | The two identity relations in force — kind identity (signatures) and content identity (≡_ℓ, structure-preserving bijection) — are never reconciled; the "definitional mirror" (a built, originated copy) exploits the gap. | **Valid, serious.** | Fix: state the relation between them: ≡_ℓ is the identity of contents as wholes; forward kind is the identity of parts under a contract; a content-preserving recoding preserves every forward kind of every part, and the converse fails. The mirror is then an anchored, originated account that is ≡_ℓ to the target, and Newness — which uses ≡_ℓ — fails for it if the target is in the repertoire, and holds if it is not, in which case building the target's mirror from error records *is* discovering it. |
| 9 | Properness is ambiguous about overlapping anchors; single-component targets still cannot be accounts at all under the singleton witness. | Valid. | Overlap is permitted; injectivity forbids identical anchors only. The singleton fix is §1.1. |
| 10 | The objectivity condition is ill-typed (two-place conjoined with four-place); σ has no declared domain; "the candidate being better" counts as protection. | Valid. | Four-place throughout; σ: B_D → B_E declared with the transport; protection is disagreement with the *target*, and the target is by definition right about itself, so "better" is not a case. |
| 11 | Attack (F) redirects the decoy case to (C), "the wrong court". | **Partly valid.** | The decoy that matches on every admitted edit is, at the module's index, the mechanism; the only way it could fail to explain where the mechanism succeeds is by a difference no admitted change shows — which is what (C) is about. The redirection stands; the sentence must say why. |
| 12 | The consequence "a selected representation is representation of less than was claimed" does not follow from (R) as written, because (R) quantifies over the content's declared contract. | Valid. | Fix: (R) is indexed to a contract; a selected transport witnesses (R) for the content on any contract on which it is faithful, and the largest such is what it represents. Write it as a definition, not a consequence. |
| 13 | "Fidelity is well-defined on K" is asserted but the declared relations for K-pairs are not related to the transport's τ, which is typed on admitted edits. | Valid. | τ must be extended to K by the question's declaration: each K-pair is declared together with its translation. |

**Additions to the third revision list from the second witness:** 15. Survival recorded as coincidence in the run, not equivalence (row 1). 16. The defect record on the route to the *acceptance* of the binding, via reason use (row 2). 17. Non-triviality against repertoire and carriers; single relay excluded (row 3). 18. Provenance indexed to the grain of the route (row 4). 19. Enacted witness, not assembled (row 5). 20. World-kind excludes the question's baseline; λ's bijection (row 6). 21. Copying and descent defined or dropped (row 7). 22. The relation between ≡_ℓ and forward kind stated; the mirror case adjudicated by Newness (row 8). 23. Four-place objectivity; σ typed; "better" excluded (row 10). 24. Attack (F)'s sentence (row 11). 25. (R) indexed to a contract; the "less than claimed" point as a definition (row 12). 26. τ extended to K by declaration (row 13).
