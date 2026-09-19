# Adversarial cross-examination: findings and adjudication

**What this is.** Two external models were given the semantics (file 10), both experiment designs and results (11–14), and both code files, with 26 hostile prompts, three samples each. Their replies are witness statements. Every finding below was checked by me against the text and, where it concerns code, against the code; the verdict is mine. The models are not authorities; neither am I beyond what the check shows.

**Witnesses.** `deepseek-flash` (DeepSeek, reasoning model) — battery completed. `Atria-Dawn-Preview` (Atria ASI) — see section 0.

**Verdicts.** *Valid* — the finding is correct as stated and something must change. *Partly valid* — correct in substance, wrong in scope or severity. *Invalid* — the finding rests on a misreading, and I say which. *Duplicate* — already covered above.

**Status: in progress.** Sections are added as replies land and are checked. Nothing here has yet been carried into files 10–14; the change list at the end is what will be carried.

---

## 0. Failure modes of the cross-examination itself

1. **Network.** Both hosts were policy-denied at the egress gateway on first attempt; you opened them.
2. **Reasoning models eat their own budget.** `deepseek-flash` spent all 6,000 output tokens thinking and returned nothing on the first launch; raised to 24,000 and the reasoning saved alongside. Several replies still hit the length limit mid-answer (one reply: 99,000 characters of reasoning, 4,400 of answer). Truncated replies are used for what they contain and marked.
3. **Atria 401.** The key lists models and answers small requests; every harness call returned "Invalid API key." Diagnosed as a burst-rate limit mislabelled as an authentication error; retried with back-off (see item 6 for the second Atria problem).
4. **Self-kill.** Two attempts to stop a stale run used `pkill -f` with the script's name, which matched the shell running the command and killed it. Replaced by a `/proc` scan that only touches processes whose argv is exactly the harness.
5. **The keys were pasted into a chat transcript.** Rotate them after this.
6. **Atria's output cap.** Atria-Dawn-Preview accepts at most 65,536 output tokens (100,000 is rejected) and at 24,000 it spent everything on reasoning and returned no answer for every item. Relaunched at the cap. Every Atria reply that exists was produced at 65,536.
7. **A 600-second read timeout in the harness** would have cut off long Atria generations and silently retried them (the retry path printed nothing). Raised to 40 minutes and made the retries print; the Atria run was restarted, so its first 14 minutes were lost.
8. **One battery item was assembled without the design it asks about.** D8 (does experiment 2 test file 10's definitions) was given files 10 and 14 but not 13, where S1–S6 are defined. One of three samples noticed and said its mappings were reconstruction. The verdict survives because the mapping to the definitions is absent from file 13 as well — that is the finding — but the item was badly built.
9. **DeepSeek empties.** Of 78 first-pass replies, 33 were empty (all reasoning, no answer) at 24,000 tokens. Rerun at 131,072, the model's cap; at the time of writing 25 were still outstanding.
10. **Duplication across items.** Items were written to overlap on purpose (C1–C3 and D3, D6 all attack the scramble test). Witnesses repeat the same point across items, so the count of findings overstates the count of distinct findings. Duplicates are marked as such in the tables.
11. **The witnesses had no code execution.** Every claim about what the code does was checked by me, by reading or running it. Their guesses about numbers (for example "B would likely also score zero on crossing") were right in every case checked, but were guesses until run.
12. **Witness errors.** The witnesses were wrong or overreaching in a minority of rows (marked Invalid or Partly valid) — and the E1 audit then showed that a good share of my "Partly valid" rows were leniency towards myself, not witness error. The one error type actually exhibited in the tables: asserting a numeric effect that did not occur (the given-bound conditioning, the bucket definition, the fragile winner).

---

## A. The semantics (file 10)

### A1 — Hidden primitives (three samples; sample 0 complete, 1 and 2 truncated)

The document claims two primitives and no predicate that secretly means "explains", "represents", "is a cause" or "is knowledge". The witness found 19 candidates. Deduplicated across samples and adjudicated:

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **Γ, the "active commitments", is an undefined selector** that (F1) and non-circular dependence quantify over; it can be gamed by including or excluding components. | **Valid.** | Γ is part of the candidate's *claim* — the candidate says which commitments it stands on — and (F1) then tests each. That is a defensible design (FW5 had it too) but file 10 never says Γ is declared by the candidate, and never says what stops a candidate declaring a convenient Γ. Fix: state that Γ is declared as part of 𝓔 and that non-circular dependence must be witnessed by a contrast *in C* that removes a block of Γ — so a gamed Γ fails the test rather than passing it. |
| 2 | **"Stated scope, not silently" is a record-keeping condition inside a semantic definition.** | **Valid.** | It is a condition on the modeller's honesty, not on the structures. Fix: scope is an index S with C = C_phys ∩ S; "stated" belongs in the record, not in Account. |
| 3 | **"Nontrivial binding construction" is undefined and is the whole discriminator between construction and relay.** | **Valid, serious.** | This is the hidden creativity predicate. Experiment 2 gave it an operational form — a new rule not composed of existing ones — but file 10 does not. Fix: a binding construction is a new component whose footprint joins ports from distinct incoming carriers and whose relation is not a composition of prior component relations; "nontrivial" = not so decomposable under C. |
| 4 | **"Content-preserving recoding" presupposes content identity.** | **Valid.** | Derivation 8 has the right notion (structure-preserving bijection) but it is used in Parts IX and X before it is defined. Fix: define it at first use as a bijection preserving (F1), (F2), (A) at the same grain. |
| 5 | **Grain is an unconstrained truth-changing index.** | **Partly valid.** | The document is explicit that every claim is relative to ℓ, which is honest scoping. But the witness is right that nothing constrains *admissible* grains, so a claim can be rescued by grain-shopping — the very thing file 10 forbids in Derivation 7 for contracts. Fix: admissible grains are coarsenings under which components keep signatures that Θ's admitted edits realise. |
| 6 | **Org_ℓ is a third primitive dressed as physics.** "Which organization a lump of matter instantiates" is an implementation relation, not something physics supplies. | **Valid, serious.** | This is the strongest hit. File 10 moved FW5's representation primitive from "Rep" to "Org_ℓ" and then claimed to derive representation. What is actually derived is the carrier→content link's *provenance*; that a physical state has a given structure at a grain is still taken as given — and implementation relations are famously not free (a wall implements every automaton if you let the grain do the work). Fix: either count three primitives, or constrain Org_ℓ by the document's own idea: an occurrence instantiates D at ℓ only if D's components have signatures realised by Θ's admitted edits — implementation is itself change-fidelity. That is the honest repair and it keeps the spirit. |
| 7 | **"Relevant" does undefined work.** | **Partly valid, minor.** | "Question-relevant" in the opening is informal; the formal content is Account. Fix: say so at first use. |
| 8 | **O_p appears in every question, so the normative primitive is pervasive, not occasional.** | **Partly valid.** | Conflates two things: obligations (declared predicates on situations, e.g. "an adequate account is deployable") and the normative relation 𝒩 (reasons in a respect). O_p is an index; 𝒩 is a primitive. Fix: say O_p is declared data and that an obligation invokes 𝒩 only when its predicate does. |
| 9 | **ProducedBy / ProducesVia / Result are undefined causal-production predicates** — exactly what the document says it has none of. | **Valid, serious.** | Carried over from FW5 without definition. Fix: define via Part IX's active route — Δ produces the change iff the change lies on an active route from Δ's binding under the declared contrasts. Result(Δ) = the contents on that route. |
| 10 | **"Owned" is undefined** and central to Build, Can, and (RC). | **Valid, serious.** | FW5 had Owned_Ω as a physical-organizational fact; file 10 dropped the definition. Fix: owned = within boundary β and reachable by the system's own intervention repertoire in Θ. |
| 11 | **Circularity: Rep is defined via Sel/Con, and Sel/Con are defined using "represents".** | **Valid, serious — the definition of representation is not well-founded as written.** | Sel says "no member of the history *represents* t, H, or the survival condition"; Con says "available as a *represented* target"; (R) then defines Rep from Sel ∨ Con. Fix by stratification: Sel is defined with no use of "represents" — "no member of the history is a transport to t, H, or the survival condition that is faithful on C" — which grounds representation at the primitive layer; Con may then use representation at the layer below. This is the two-layer picture of Part IV made into a well-founded recursion rather than a circle. |
| 12 | **Declared provenance is meta-linguistic, not physical.** | **Valid, minor.** | Dec is an annotation meaning "no selected or constructed witness". Say so. |
| 13 | **"A survival condition requiring fidelity" assumes selection tracks fidelity.** | **Valid.** | Survival is physical; that it selects for fidelity is a claim about the environment. Both experiments *built* fitness = fidelity, so they assume it too. Fix: state it as a premise of the selected provenance. Note this for the experiments' limits. |
| 14 | **Active route uses "represented input" before (R).** | **Valid.** | Same stratification fix as 11. |
| 15 | **Lic, Scope, Live are undefined.** | **Partly valid, minor.** | They are the appraisal's declared data (FW5: "enacted license"). Say so. |
| 16 | **"Controlled-action interpretation" and "resources" in Θ smuggle agency.** | **Partly valid.** | Constructor theory defines tasks and resources physically; "controlled action" is an interpretation. Fix: control = an intervention repertoire in Θ. |
| 17 | **Observation role defined via "reporting".** | **Valid, minor.** | Fix structurally as the witness suggests. |
| 18 | **Restriction operation and "named background" undefined.** | **Valid, minor.** | Fix: restriction deletes components in Γ holding b fixed. |
| 19 | **"Independent boundary conditions" not formalised.** | **Valid, minor.** | Fix: no faithful transport from the answer ports into the boundary ports. |
| 20 | (sample 2) **(O) and (Q) "depend on nothing" so they are primitives too.** | **Invalid.** | (O) and (Q) are definitions of a schema, not predicates about the world; a definition that depends on nothing is not a primitive in the sense the document means (a relation taken as true without derivation). The count of primitives is about what is *asserted*, not what is *defined*. But the document should say this. |

**What changes in file 10 from A1:** three primitives or a constrained Org_ℓ (6); stratify Sel/Con/Rep (11, 14); define binding construction (3), ProducedBy (9), owned (10), recoding (4), restriction (18), observation (17), independence (19); state Γ, O_p, Lic/Scope/Live, scope S as declared data (1, 2, 8, 15); state the fidelity-selection premise (13); constrain grains (5).

### A2 — The derivations (sample 0, truncated after Derivation 2; samples 1–2 pending)

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **Derivation 1 has a type error: (K) defines signatures for components; λ(k) is a subnetwork.** | **Valid.** | The proof's first line writes sig_C(λ(k)) which (K) never defined. Fix: define the signature of a subnetwork as the projected relation family, which is what (F1) already computes — then the proof goes through *for that notion*. |
| 2 | **Equal projections on visible ports do not give equal signatures on full footprints; hidden ports can differ.** | **Valid, and the important one.** | This is exactly where "same kind" and "same anchor" come apart. (F1) checks the projected relation; a subnetwork with hidden structure can match a component's projection while having a different full signature. The corollary "kind preservation adds nothing to F1" is therefore true only *at the projected grain* — which is, on reflection, the correct claim: kinds at the contract's grain are preserved; kinds at a finer grain involving the hidden ports are not tested and are not claimed. Fix: state Derivation 1 as kind-preservation *at the grain of the declared ports*, and say explicitly that hidden-port structure is outside the contract. |
| 3 | τ[C] undefined; should be (τ,σ)[C]. | Valid, cosmetic. | Fix notation. |
| 4 | The corollary overreaches for subnetwork anchors. | **Valid.** | Follows from 1–2. |
| 5 | Nothing says τ(a), σ(b) land in E's admitted pairs. | Valid, minor. | Add the typing condition. |
| 6 | **Derivation 2 claims components "pairwise of one kind" with no bijection between the two candidates' decompositions.** One component encoding a conjunction vs two encoding the conjuncts both satisfy F1, F2, A and are not pairwise anything. | **Valid, and the claim as stated is false.** | My error. The correct statement: two candidates faithful on C have the same *anchored relations* on C and the same answer profile pulled back to C — not the same decomposition. "One account at grain C" must be defined as that, and it is weaker than what I wrote. This weakens the consequence used in experiments 1 and 2 ("indistinguishable is identical") to "indistinguishable have identical anchored relations on C" — which is all the experiments actually used. |
| 7 | "One account at grain C" is undefined. | Valid. | Define as in 6. |
| 8 | Answer profiles coincide only as pullbacks to C. | Valid, technical. | Say so. |

**What changes in file 10 from A2:** Derivation 1 restated at the projected grain with a subnetwork signature; Derivation 2 restated as equality of anchored relations and pulled-back profiles, with account-equivalence defined; the word "identical" in its title goes.


### A3 — Sufficiency: a candidate that passes all four conditions and explains nothing (sample 1 substantive; samples 0 and 2 empty — reasoning budget exhausted)

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **A ROM passes (E).** Target: a pendulum with three inputs and one output. E: one component per output *bit*, each with footprint {inputs, that bit}, each anchored to the *whole* target, λ(kᵢ) = D. Then proj[Sol_D] onto {inputs, bitᵢ} is exactly that bit's table, so (F1) holds; the assembly is the same singleton, so (F2) holds; (A) holds; removing a bit component changes the answer, so non-circular dependence holds; non-vacuity holds. It is a lookup table with a selected provenance. | **Valid, serious.** | This is a real hole and it is in (F1) as written: nothing stops λ from sending every component to the entire target, and projecting the whole target onto (inputs, one output bit) *is* that bit's relation. Fix: λ must be a **decomposition** — each anchor a proper subnetwork, the anchors jointly covering D's active components, and every component surgery in C translating to a *distinct* edit on E (τ injective on surgeries). Under that, a bit-ROM fails: its "components" all anchor to everything and no surgery on D maps to an edit on one bit alone. The witness's warning is fair and stays: this must be re-checked against holistic explanations, where one component legitimately anchors to a large subnetwork — the condition must forbid *everything anchoring to everything*, not large anchors. |
| 2 | The document's reply ("a table that genuinely encodes the organization's response to every admitted change is not excluded") is a concession, not a rebuttal. | **Valid.** | It concedes exactly the counterexample and supplies no condition. Replaced by the decomposition condition above. |
| 3 | "(F1) prevents an assembled match from hiding a wrong decomposition" is false. | **Valid.** | (F1) checks per-component signature matching; it does not check that the decomposition is proper. Qualify it. |
| 4 | Non-circular dependence forbids the *answer* as an input or a component but not the whole target relation spread across components. | **Valid.** | The informal clause ("moving an assertion into a component named 'law'") describes the ROM exactly and is not formalised. The decomposition condition is the formalisation. |
| 5 | Non-vacuity is satisfied trivially. | Partly valid. | It was never meant to catch this; the decomposition condition is where it belongs. |

This is the anchoring steelman (A7) made concrete: dropping the kind-label lost a *decomposition* constraint that the label had been carrying informally ("a cause must anchor to a cause" forbade anchoring a lookup bit to a causal whole). The constraint comes back as structure, not as a label.

### A4 — Necessity: eliminative and impossibility explanations (sample 0 substantive, truncated; 1 and 2 empty)

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **Absence is not deletion.** A deleted component imposes the full relation; a rival structure is a *non-full* constraint. Anchoring the rival to a "deleted subnetwork" forces its relation to be full, so it cannot carry the specific effect the eliminative explanation excludes. | **Valid.** | Part VII's treatment is wrong as written. Fix: eliminative explanation compares two organizations, D and an extension D^X with the rival present with its specific relation; the account is a transport on the extended contract whose restriction to D is the original. |
| 2 | Part II has no edit that adds ports or components, so "edits that would introduce them" are not edits. | **Valid.** | Add an organization-extension operation to Part II, or (as in 1) treat eliminative explanation as a comparison between organizations. |
| 3 | **Impossibility explanations need contracts that are not physically admitted.** "Why is there no photon mass?" — the edit that adds the mass term is forbidden by gauge invariance; "why no perpetual motion?" — the edit is not physically admitted. Non-vacuity requires C ⊆ physically admitted edits, so no contract can contain the contrast. | **Valid, and a regression.** | FW5 allowed this explicitly ("the contrast may concern a counterfactual law or rule rather than a physically executable intervention; its formal meaning must still be stated"). File 10 tightened non-vacuity to physically admitted edits to close the "could matter" loophole, and in doing so broke impossibility explanations. Fix: a contract's edits must be *declared and formally specified*; each is either physically admitted or explicitly counterfactual with its meaning stated. The anti-gerrymandering job is done by the declaration and by criticism supplying an excluded edit, not by physical admissibility. |

### A5 — Kinds: can a kind-label do work no admitted change can? (three complete samples)

The witness produced the same family of cases in all three samples: perfect forgery vs authentic; homology vs analogy; stolen vs donated; tempered vs untempered glass; mechanical vs quartz; "which mechanism actually did it" when no finer contract is available; and — sharpest — file 10's *own* selected/constructed distinction, which is individuated by history and not by forward response.

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **Historical kinds are real and are not edit-signatures**: forgery vs authentic, homology vs analogy, stolen vs donated. | **Valid, serious — and it changes the document's central sentence.** | "A kind is nothing over and above how a component responds to the changes that level admits" is false for historical kinds. But the witness's proposed fix (add provenance to the signature) is not needed, because file 10 already has the machinery: a history *h* with its causal precedence, receipts, and the provenance of transports. A historical kind is a **predicate on h**, checked by the record, not by edits. The repair: there are two checkable kinds of kind — **forward kinds** (edit-signatures, contract-relative, checked by changes) and **historical kinds** (predicates on h, checked by records). A declared kind-label must cash out as one or the other. What remains forbidden — and this was the original crack — is a label that is *neither*: not a response to any change and not a fact of any record. FW5's "a cause must anchor to a cause" was ambiguous between the two, which is exactly why it could not be checked. |
| 2 | **The document's own selected/constructed distinction is a historical kind.** | **Valid, and the best finding in the set.** | It is. Provenance of a transport is a predicate on h. The document should say so, and then it has no reason to deny the same to components. |
| 3 | Dispositions (fragile, tempered, soluble, irritable) are not captured when C excludes the trigger. | **Partly valid; invalid as a refutation.** | A disposition's trigger is a physically admitted edit even when the chosen C omits it, so a disposition is a forward kind at a finer contract — and FW5's rule, which file 10 keeps, is that the contract ranges over *unperformed* admitted changes. If the question is about the disposition, C must contain the trigger; the witness's own fix. What file 10 must add is one sentence saying so. |
| 4 | "Which mechanism actually produced it" when no finer contract exists (astronomy, history). | **Partly valid.** | Actual cause is a historical kind — a predicate on h — so the fix in 1 covers it where a record exists. Where neither a separating change nor a record exists, "underdetermined" is the correct answer, not an evasion: a label with no route to check it is the thing the whole document is against. |
| 5 | "There is no third case" is a false dichotomy; the third case is history. | **Valid.** | Withdraw the sentence. |
| 6 | Derivation 1 proves that a same-kind *anchoring condition* is redundant for (F1), not that kind-talk is eliminable. | **Valid.** | Correct and precise. The corollary equivocates. Narrow it. |
| 7 | Derivation 10's "identity at this grain is exhausted by trajectory" is a metaphysical assumption. | **Valid, as scoping.** | It is true at the sensory contract and false of the history: the world model's things are identity-indexed and the swap is a fact of h. Say "at the sensory contract"; the history distinguishes them. This is also exactly what experiment 2's M3 found (F3): the crossing is invisible to sensation and visible to the identity-indexed record. |
| 8 | A kind-label is needed to choose the anchor λ (a heart vs a heart-shaped rock under a contract without blood flow). | Partly valid. | On that contract they are one forward kind; "heart" is a claim about a finer contract (blood flow) or about history (evolved to pump). Either cashes out. Not an evasion once both routes exist. |
| 9 | Contract-relative kinds conflict with explanatory realism. | Partly valid. | Forward kinds are contract-relative *and* realist: whether a signature matches on C is a fact. Historical kinds are realist about h. What is not claimed is a contract-independent forward kind, and that is right. |
| 10 | Non-circular dependence and non-vacuity rule out historical questions by fiat. | **Valid.** | As written they presume every commitment is a change-response commitment. For a historical question the contrast is a counterfactual history (a different h), which is the same repair as A4.3: contracts may contain declared counterfactuals with stated meaning. |
| 11 | (K) ignores causal history. | Duplicate of 1. | — |
| 12 | Recorded exclusion is not an answer. | Partly valid. | If the question requires a distinction the contract cannot see and no record supplies it, the candidate is not an account *of that question* — which the document already says ("an answer to one is not an answer to the other"). Say it at this spot. |

**What changes in file 10 from A3–A5:** λ must be a decomposition (A3); eliminative explanation as a comparison of organizations, with an extension operation (A4.1–2); contracts may contain declared counterfactual edits with stated meaning, restoring FW5's rule (A4.3, A5.10); two kinds of kind, forward and historical, and the withdrawal of "nothing over and above" and "no third case" (A5.1, 2, 5); Derivation 1's corollary narrowed to the anchoring condition (A5.6); Derivation 10 scoped to the sensory contract (A5.7); dispositions as finer forward contracts (A5.3).


### A6 — Genesis (D) and question-finding (E) (three samples; one truncated)

**(D) Provenance**

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | Rep is defined via Sel/Con; Sel and Con use "represents"; Build uses "represented organization". Two cycles, no base case. | Duplicate of A1.11 — **valid, serious.** | Fix by stratification: Sel defined with no use of "represents" (no event in the selection process is a faithful transport to t, to H, or to the survival condition); that grounds representation at the bottom layer; Con and Build may then use representation one layer down. |
| 2 | **Sel is trivialisable.** Singleton population, identity variation, empty history, vacuous survival: any transport is "selected." | **Valid, serious.** | Add to Sel: H non-empty; the survival condition eliminates at least one candidate on H; t is produced by iterated variation from an initial population that does not contain it. |
| 3 | **"Blind" is never formalised**, so variation could be construction in disguise. | **Valid, serious — and experiment 2 supplies the definition.** | Blindness = the variation operator's route contains no representation of the target or of the defect; operationally, its output is unchanged when the defect records are scrambled or removed. That is the ablation test of file 14 section 5, stated as a definition. |
| 4 | "Exactly one of three provenances" contradicts "construction may operate on selected material." | **Valid.** | Provenance is per transport and per layer, with precedence: a transport with a construction witness is constructed even if selection also acted on it; selected iff no construction witness and a non-vacuous selection history; declared iff neither is claimed. |
| 5 | The clause "no member of the history represents t, H, or the survival condition" is ill-typed: H's members are edit–boundary pairs. | **Valid.** | Distinguish H (the encountered pairs) from the selection history (the events of variation and survival). The condition is on the events. |
| 6 | **The primitive layer P is defined as already containing persistent things with identity — so selection cannot be what produces objecthood; it presupposes it.** | **Valid, serious.** | Part IV contradicts Part 0. Fix with three layers, which is what experiment 1 actually built: a raw **sensory field** (occupancy, no identity); the **primitive layer** of things-with-persistence, produced by *selected* transports from the field; the **simulation layer**, constructed on things. Selection makes objects out of sensation; construction makes dependencies out of objects. |
| 7 | The Derivation 10 episode's "constructed persistence" is already in P; and its claim that the selection response fails structurally is contradicted by experiment 1, where persistence was *selected*. | **Valid.** | Derivation 10 stipulated a population with no latent persistence and then said selection fails; experiment 1's population had it latent and selection found it. Both are consistent with the semantics but Derivation 10 must say what it assumed. Rewrite: if the needed component is latent in the population, selection expresses it (experiment 1); if it is not, only construction can supply it (experiment 2). That is your three points, and the semantics should say them. |
| 8 | **Derivation 3's proof alters a component relation of the organization, not the transport, and ignores whether the altered thing is in the population or reachable by variation.** | **Valid as a proof defect.** | The claim survives in corrected form: the *organization–transport pair* is underdetermined by H within any population closed under the alteration. State it that way. |
| 9 | The survival condition's "fidelity" names no target; physical survival cannot enact a relation between abstract organizations. | **Valid.** | State the map: a carrier persists iff its prediction of the world port matches under the encountered edit. Both experiments defined fitness exactly so; the semantics should. |
| 10 | Populations, variation operators, survival events and histories are not in Θ's list of primitives. | Valid, bookkeeping. | Add them to Part XIV's physical module. |
| 11 | The prose "a selected transport has no represented target" is stronger than the formal Sel. | Valid. | Add the clause once stratification makes it well-typed. |
| 12 | Account has no provenance condition; (EK) should require every transport in the account to be non-declared. | **Valid.** | Add to (EK). |
| 13 | Declared provenance is meta-linguistic. | Duplicate of A1.12. | — |

**(E) Question-finding**

| # | Finding | Verdict | Why |
|---|---|---|---|
| 14 | Derivation 5 says a contract is "a set of edits with a query"; Part III separates C from 𝒬. The proof is about the wrong object. | **Valid.** | The content that can be found is the *question* (at least the pair (C, 𝒬), better the whole tuple). Define D_p explicitly with ports, domains, components, boundary, edits, relations — Derivation 5 as written is stipulation, not construction (also finding 17). |
| 15 | **Origin presupposes the question it is meant to represent as found**: Attempt(s, c, p, h, e) requires c to be used to address p; if c is the question, p must already exist. | **Valid, sharp.** | For a question-content, Attempt must be relative to the *recognised difficulty* — the defect in the prior question or the unresolved problem situation — not to the question itself. Define Attempt_Q(s, p′, δ, h, e): p′ is used to address difficulty δ. |
| 16 | D and 𝒬 have no provenance; only C does. | **Valid.** | Give the whole question tuple provenance. |
| 17 | "Give it ports … it is then a D" supplies none of (O)'s data. | **Valid.** | Supply the tuple. |
| 18 | ≡_ℓ is undefined, so New is trivial or arbitrary; any re-parameterisation becomes a found question. | **Valid, serious.** | Define ≡_ℓ as structure-preserving bijection at grain ℓ (Derivation 8's notion) — for questions, equivalence of (C, 𝒬) up to recoding *and* of answer profiles. A threshold tweak is then a content-preserving recoding: not New, and not Built once binding construction is defined (A1.3). |
| 19 | Build is defined for "explanatory use"; a question is used to ask. | Valid, minor. | Generalise Build to use. |
| 20 | "Finding" a question is never distinguished from stipulating a new contract; defect-driven question construction is asserted, not given. | **Valid.** | Require the episode structure of Part X: a recognised difficulty, a criticism of the prior question with Bearing, and the new question on the active route from that criticism. Experiment 2's constructor is the template: the new rule was built *from* the defect records. |
| 21 | No notion of a *good* question, so random new contracts count. | Partly valid. | The document has no merit function on purpose; "good" here means: a question whose answer repairs an obligation under (P). Say that, and it is not random. |
| 22 | Contract provenance inherits every transport-provenance defect. | Valid, follows from 1–5. | Fixed when they are. |

### A7 — The steelman of anchoring (three complete samples)

All three samples converge on one point and it is correct: **the "Why there is no anchoring condition" section refutes a strawman.** It attacks "a declared kind-label" and shows a label is redundant with (K)-kind on C. The real position is correspondence to the *world's mechanism* — a world-kind fixed by Θ, not by the declared contract — and that is neither a label nor unevaluable.

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | The section equivocates on "kind": (K)-kind is signature on C; the anchoring condition's kind is the mechanism in Θ. "No separating change in C" does not mean "no separating change in the world," because C is a *declared subset* of the physically admitted edits. | **Valid — the central finding, and it has a clean repair.** | The repair keeps the no-label principle. Define **C_phys** = all physically admitted edits, and **world-kind** = signature on C_phys. Then the anchoring condition *is* (F1) evaluated on C_phys instead of C. It is stronger than account-on-C, evaluable in principle by physics, fallible in practice (the edits may not have been performed), and contains no label. "Correct at C but anchored to the wrong mechanism" = faithful on C, unfaithful on C_phys. Two grades of adequacy: **account at C** and **anchored account**. FW5 demanded the second and stated it as a label; file 10 wrongly said the second was empty. |
| 2 | **Composite-anchor counterexample.** D has j₁: x = 0 and j₂: y = 0; E has one component with relation x = 0 ∧ y = 0 anchored to {j₁, j₂}. (F1) holds; no D-component has that kind. So component-level anchoring is not redundant with (F1). | **Valid.** | (F1) permits coarsening. That is not always wrong — a component "the conjunction" is legitimate at a coarser grain — but Derivation 1's corollary claimed more than (F1) gives. With A3's decomposition condition and finding 1's C_phys, the corollary becomes: (F1) on C_phys with a proper decomposition entails world-kind correspondence at the declared ports. |
| 3 | (F1) does not catch a wrong anchor even when C separates kinds: a decoy with a different signature but the same effect on the queried answer under C passes (F1), (F2), (A). | **Partly valid.** | If the decoy and the real producer differ in their effect on the answer under *some* physically admitted edit, the account fails (A) on C_phys — caught by finding 1's repair. If they differ under *no* physically admitted edit, they are interchangeable for the answer in every possible test, and the remaining difference is historical (A5) or nothing. |
| 4 | "Correct at C, wrong mechanism" is a real loss without anchoring. | **Valid; repaired by 1.** | — |
| 5 | Pole and shadow when the production contract is unavailable: the reversed calculation is faithful at identification; the document can only say "different question." | **Partly valid; repaired by 1.** | Building a taller pole is physically admitted whether or not the question declared it. On C_phys the reversed calculation fails (F1). So: an account at the identification contract, and *not anchored* as a production account. The document can now say that rather than only "different question." |
| 6 | Scientific realism about mechanisms is not representable if kinds are contract-relative. | **Partly valid; repaired by 1 and A5.** | World-kind on C_phys *is* realism about mechanisms to the extent that mechanisms differ under any possible intervention; historical kinds cover differences of provenance; what is left is a difference that shows up under no intervention and in no record — and the document is right to decline that. |
| 7 | (K) requires a footprint bijection, so components of different arity are not one kind even when no change separates their shared behaviour — the section's "no change ⇒ one kind" is false under the document's own (K). | Valid, minor inconsistency. | Define kind on the projected shared ports, or say the footprint bijection is part of the criterion. |
| 8 | Scope-honesty and non-vacuity do not substitute for anchoring: a stated exclusion leaves a wrong mechanism standing until a criticism supplies the edit. | **Valid.** | That was the whole crack, from the other side. C_phys is the answer: the exclusion is stated *and* the account's grade is reported as at-C, not anchored, until the excluded edits are covered. |
| 9 | Derivation 1 is circular as an answer to the steelman. | Valid. | Duplicate of A5.6 in effect; narrowed as there. |
| 10 | Derivation 2 collapses distinct mechanisms. | Duplicate of A5.4 / A2.6. | Repaired as there: "one account at C" is contract-relative by definition and now says so; anchored accounts are compared on C_phys. |

**What changes in file 10 from A6–A7:** C_phys and world-kind; two grades of adequacy (account at C, anchored); the "Why there is no anchoring condition" section rewritten to say what the anchoring condition *is* rather than that it is empty; three layers (sensory field, primitive, simulation) with selection between the first two; Sel made non-trivialisable and blindness defined by ablation; provenance with precedence; Derivation 3 restated for the pair; Derivation 10 restated with its population assumption; the question tuple as content with Attempt relative to a difficulty and ≡_ℓ defined.


---

## B. Experiment 1 (files 11, 12, 12a)

### B2 — The 21 pre-freeze changes, audited (two substantive samples, one empty)

The witness treats "before freezing" as irrelevant if results were seen before freezing, and asks of each change: did it alter what an outcome *means*, and was it made after seeing numbers that pointed a particular way. That is the right audit and I did not run it on myself.

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **"Pre-registered … written before any code was run, and not changed after" (design §4) is false.** Change 8 says the outcomes were rewritten; changes 11, 13, 16–19 cite run results. | **Valid, and the most important process finding in this file.** | The original draft's outcomes were written before code. The amended outcomes were fixed after three control runs *on the same histories used for the main run*. That is design-level contamination, exactly as the witness says. The correct label is **frozen after pilots**, with the pilot numbers reported. Every change is recorded, which is better than hiding them, and the first pilot already showed the direction — but "pre-registered" claimed more than was done. Corrected in the errata (file 16). |
| 2 | Change 16 says τ=0 was "winning" H_neutral; change 19 says the τ values "tied exactly." | **Valid.** | Sloppy wording. The control's `best_of` returned the first maximum in enumeration order, which was τ=0; the values tied. Corrected in the errata. |
| 3 | **Change 18 dropped the 0.95-of-ceiling adequacy threshold after seeing 0.88.** The diagnosis explains why 0.95 was mis-specified, but that is grounds to re-freeze, not to drop the criterion after seeing the number. The replacement (slot > lookup) is weaker: both could be poor. | **Valid — a moved goalpost.** | Under the original criterion, the H_full grammar is **underpowered** (0.881 of ceiling). The H_full results should be read with that stated. I should have kept the threshold and reported the attempt as failed on it, then revised in a new attempt. |
| 4 | **Change 19 excluded `rebind` from the neutrality check after it sat 0.026 below**, although §2.6 defined the kind under test as "the τ gene and the `rebind` rule." | **Valid — a redefinition after the fact.** | The reason (rebind lacks velocity memory, not persistence) is logically sound and I still think it is the right analysis — but it was made after the number. Under the *original* definition, neutrality **fails** by 0.026. Under the narrowed one it passes exactly. Both are now reported. |
| 5 | Change 17 (exposure/evaluation split) was introduced after observing the lookup memorising, and it changes every fitness figure. | **Valid as post hoc; the method is necessary.** | Report both: on train = test the lookup reached 0.820 on H_full; held out, 0.656; the tracker 0.801 on both. The split does not change which persistence value wins any history; it changes whether lookups compete. |
| 6 | Change 6 still says "112 architectures" after change 14 made it 208. | Valid, cosmetic. | Errata. |
| 7 | Change 11 calls the corrected ceiling "the true bound" while §2.5 calls it in-sample. | Valid, wording. | It is an in-sample bound. Errata. |
| 8 | "A 3-cell window hides it for at least three steps" is false: a thing at the window's edge moving outward leaves in one step. | **Valid.** | The hidden-duration distribution is computed in the errata. |
| 9 | Fitness against true occupancy "makes persistence beneficial under occlusion by construction" and is a normative choice, not a measurement fix. | **Partly valid.** | It is a choice about what selection acts on — the world, not sensation — and the design says why. But the witness is right that it should be stated as the choice that sets the direction of the result. |
| 10 | Which changes a referee would accept: 1, 3, 4, 5 (as scope), 6 (count fixed), 9, 10, 12, 20, 21; conditionally 7, 8, 13, 14, 15 if timestamped before the first run; **not** 16 as pre-registered, **not** 18, **not** 19. | **Accepted as the fair verdict.** | 13, 14, 15 were after the first control run (the transcript shows it). So the referee's list stands: three changes I would not be allowed as pre-registered, and three more only as pilot-informed. |

### B4 — Is the headline trivial? (two substantive samples, one empty)

Both samples reach the same verdict: **the triviality argument wins on the headline as written.**

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **H_neutral is defined so that τ cannot matter**: τ governs unconfirmed slots; with one thing and nothing hidden every slot is confirmed every step; the tie is mechanical. | **Valid.** | The tie was entailed by the definition of the history, not discovered. |
| 2 | **H_full selecting τ=∞ is "the required mechanism is selected when required."** Occlusion is the only change that produces prolonged non-confirmation and persistence the only mechanism in the grammar for it. | **Valid.** | Yes. |
| 3 | **The headline is contradicted by §7.3.** On H_neutral history did *not* determine the kind; drift did. "A role for chance the diagnosis did not mention" is a retraction of point 3 as stated, not a footnote. | **Valid.** | Point 3 must be conditional: history determines the kind when it contains the discriminating change; otherwise it underdetermines, and what you get is drift. I wrote that as a charming observation; it is a correction. |
| 4 | **The rival is a strawman.** A correspondence theorist can hold kinds are prior *and* that a parsimonious predictor omits persistence when nothing is hidden. The rival is not forced to predict persistence under H_neutral. | **Valid.** | The design did not have a differential prediction between the diagnosis and a well-formed rival; it tested the diagnosis's positive prediction only. |
| 5 | **"The kind is just a parameter value."** The grammar supplies the kind; the experiment shows fitness selecting a parameter. It cannot bear on whether kinds are inputs or outputs. | **Valid for the headline; already conceded by your point 1.** | Experiment 1 shows point 3 in its weakest sense — history picks among latent kinds — and nothing about kinds not being inputs. That question is experiment 2's. |
| 6 | **"Has thing-kind" was claimed on a given-bound figure when the design's definition (§3) was "for every configuration and every change."** Unconditional, τ=∞ scores 0.801 and fails the definition. | **Valid.** | Under the frozen definition no architecture has thing-kind. The conditional figure is a post-hoc relaxation, and the honest reading is that M3 tests *preservation* of a binding, not its acquisition (B5). |
| 7 | **Search bias misclassified.** Six seeds on H_neutral landed on τ = 2, ∞, 2, 5, 2, 5 and none on τ=0, which is a quarter of the tied set. "No bias" is an overclaim. | **Valid: inconclusive, not "did not fire."** | Probability of 0 of 6 by chance if τ=0 is one in four ≈ 0.18. Underpowered to detect bias either way. |
| 8 | **Thing count and occlusion are confounded** in the H_neutral-vs-H_full contrast (one thing / no occlusion vs two things / occlusion). H_kinematic vs H_full isolates occlusion within two-thing worlds. | **Valid; the occlusion conclusion survives via H_kinematic vs H_full.** | The design should have included one-thing-with-occlusion. §7.1's *j*-gene story is confounded by the same pair and is post hoc; withdrawn as a finding, kept as a hypothesis. |
| 9 | What is genuinely non-trivial: persistence is selected *against* in visible two-thing worlds (phantoms at crossings — not a definition), and tied H_neutral architectures differ two-fold on occlusion never seen. | **Agreed, and that is what remains of the headline.** | Restated in the errata. |
| 10 | §7.3's "what you could later do" was not run as a transfer test. | **Invalid.** | M2 is exactly that: fitness on the full contract after exposure to H_neutral. Slot architectures do not learn, so the number is the transfer. |
| 11 | The frozen date "is in the future." | **Invalid.** | The witness's own clock is wrong. |
| 12 | Exhaustive selection is argmax, not variation and selection. | Valid, wording. | "Selection with unlimited reach" was a euphemism. |
| 13 | 208 is not verifiable from the text. | Valid, minor. | Lookup-only 3; slot-only 17 rules × 3 counts = 51; both 3 × 51 = 153; nothing 1. Total 208. |
| 14 | Swap is fitness-inert. | Valid, minor. | It only matters for M3; say so. |
| 15 | Full M4 and per-change-type M3 not in the results document. | Valid, minor. | They are in the raw JSON; the document summarised. |

### B5 — Is the thing-signature test circular? (one substantive sample, truncated; two empty)

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | Binding at step 2 requires exact (cell, velocity) equality, which is the very property then tested; "given bound" discards the cases where it fails. | **Partly valid, and the fix is right.** | Two quantities must be reported separately: *bind rate* (did the tracker lock on) and *tracking given bound* (did it stay locked through the change). M3 tests preservation, not acquisition, and must not be cited for "has thing-kind" under an unconditional definition. The results file did report unbound counts but drew the conclusion from the conditional figure. |
| 2 | For displace and set_velocity the translated edit plants the slot where the thing is, so tracking afterwards is near-tautological; the discriminating column is occlusion, where nothing is translated. | **Valid, and already the results' reading.** | The occlusion column is the content of M3. |

**What changes because of B2–B5:** an errata file (16) correcting the pre-registration claim, the "winning/tied" wording, the counts and the "true bound" phrase; reporting neutrality under the original definition (fails by 0.026) and the amended one (ties exactly); reporting adequacy under the original 0.95 criterion (underpowered at 0.881); reporting unconditional M3; reclassifying search bias as inconclusive; restating the headline conditionally and withdrawing §7.1 and §7.3 as findings; and stating the H_kinematic-vs-H_full pair as the clean occlusion contrast. The frozen files 11 and 12 are not edited.


---

## C. The construction experiment's design (file 13)

### C1 — Is the scramble test trivial? (two substantive samples, one empty)

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **M4 tests data flow, not provenance.** C is *defined* to read V; B is *defined* not to. Scrambling V can only affect C. The outcome is entailed by the implementations. | **Valid — fatal to "this is the test that distinguishes the provenances."** | My sentence in file 14 §5 denying this was wrong. What M4 *does* show: C's output depends on the state–outcome *pairing*, not on counts — a check that C is a genuine supervised learner and not a fitness function in disguise. That is a content-dependence check on one program, not a discrimination between kinds of process. |
| 2 | B's byte-identical clause is analytic. | **Valid.** | Reclassified as an implementation sanity check. |
| 3 | The scramble perturbs only the action-fitting stage; condition induction reads states, which were not scrambled. | **Valid.** | The results already showed this (the condition survived, the action broke). M4 is narrower than claimed. |
| 4 | B is not defect-blind: its scalar is an aggregate of the same true fields. The contrast is itemised versus scalar, not representation versus none. | **Valid, and it reaches file 10.** | File 10's "a selected process has nothing inside that represents the defect" must become "receives the defect only as a scalar." The distinction is *granularity and route of the error signal*. Blindness (A6.3) then means: variation is independent of the itemised records given the scalar. |
| 5 | C and B differ in search operator, population, budget and input format; any difference is confounded with algorithm. | **Valid.** | — |
| 6 | A non-trivial version: equal access (both get V), same search operator and budget, one uses per-record credit and the other must collapse V to a scalar; scramble for both; predict the constructor changes and the scalar-user does not. Or a deceptive landscape where scalar search fails and itemised credit succeeds at matched budget. | **Accepted as the design of experiment 3.** | Neither exists in file 13. |
| 7 | M6 is equally a code check. | **Valid.** | And it caught a bug (file 14 §8), which is what code checks are for. |
| 8 | "Checked before kinematics" conflicts with terms n, w being kinematic next-states. | Partly valid, cosmetic. | n, w are *predicted* next-states computed from the current (c, v); the rule fires before the slot moves. Wording. |
| 9 | S4 and §12.2 conflict if "collision steps" includes crossings. | Valid, minor. | Crossings are a sixth of collision steps and unaffected either way; S4 passed by 0.55 regardless. Should have been stated. |

### C2 — Is C fitness in disguise? (two substantive samples, one empty)

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **"C never computes an aggregate fitness" is false.** tp − fp over conditions and fixed − broken over actions are sums over records used to rank and select. | **Valid.** | The sentence was doing illegitimate work. The true contrast: **local component-level scores from per-record labels** (C) versus **one global architecture-level scalar** (B). |
| 2 | "Nothing inside B represents what went wrong" is false; a per-candidate fitness is a coarse representation. | **Valid.** | Same as C1.4. |
| 3 | The C/B contrast collapses to informed local search versus mutation search; S5 (B reaches the same fidelity) confirms the difference is efficiency and inductive bias, not kind. | **Valid for what the experiment showed.** | The provenance distinction in file 10 is a *definition*; the experiment instantiated it, it did not test it. To show more than efficiency: a budget-matched case where scalar search fails and itemised credit succeeds. Not pre-registered, not run. |
| 4 | C's action score is myopic (one step) and ignores rule interactions. | **Valid.** | Already found as failure mode 1 in file 14. |
| 5 | "No V remain" is an aggregate stopping rule. | Valid. | — |

### C3 — Does the regress concession gut the experiment? (two substantive samples, one empty)

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **"G0 grew" is false indexed to the program (every rule was in the fixed meta-grammar from t = 0) and vacuous indexed to G0 (defined to exclude pairwise rules). No third index is supplied.** | **Valid — fatal to the framing.** | The concession in §1 did not leave a narrowed claim standing; it removed the distinction the experiment was named for. |
| 2 | "Construction extends what is latent" is true of B as well (B adds the same rules), so it distinguishes neither. | **Valid.** | — |
| 3 | G0's closedness to pairwise rules is analytic; S1 ("needed") restates the definition. Closedness should be measured against the world (the ceiling), or by M3, not against hand-built rules from the same meta-grammar. | **Valid.** | The lookup's 0.819 against the ceiling's 0.923 is the honest closedness figure: the old grammar gets 89% of the way by memorising local patterns. |
| 4 | The hand-built rules were authored by me before the run; the "growth" was pre-authored and merely rediscovered. | **Valid.** | They were meant as an expressibility check and were then used as the object whose growth was measured. |
| 5 | **The world was fitted to the meta-grammar** (change 3: "the same shape as the rule language"), so expressibility was guaranteed by construction. | **Valid, serious.** | I did it to remove an artefact; the effect is that the experiment discovers the language can express a law written to its shape. A fair design fixes the world's law before the language is finalised. |
| 6 | §12.2 pre-registers that C will build only half the law and carves crossings out of S3; "faithful with the world's kind-signature" is then an overclaim. | **Partly valid.** | The prediction was correct and stated in advance, which is worth something. But all fidelity language must read "on the sensory-visible sub-contract." |
| 7 | §12.4 excluded the lookup from the structural threshold after it scored 0.819; the overall numbers were not printed. | **Valid.** | Same pattern as experiment 1's changes 18 and 19. The overall figures: best-of-G0 0.707, hand 0.835, gap 0.128 (in the controls output, not the design). |
| 8 | Phase 2's "latent" is retention; the wall rule was in the meta-grammar already. | **Valid.** | Phase 2 was a retention test and a confounded one. |
| 9 | S5/F1 tension: if C and B are one kind on this contract, the experiment cannot support "distinct from selection." | **Valid.** | Strike "distinct" from what the experiment supports. |
| 10 | S4's 0.1 threshold has no derivation. | Valid, minor. | It passed by 0.55; the number was arbitrary. |
| 11 | What a substantive "grew" would need: (a) the extension unreachable by G0's own composition, with closure established independently of G0's definition; or (b) an input class fixed in advance that no G0 architecture matches; or (c) the extension usable as a primitive for further extensions that compound beyond enumeration. None shown. | **Accepted.** | (c) is what a real phase 2 would test. |

**What changes because of C1–C3:** an errata file (17) for experiment 2; file 14's §5 claim withdrawn; "needed", "grew", "distinct" withdrawn from what the experiment supports; the provenance distinction in file 10 restated as granularity and route of the error signal; and experiment 3 designed as the equal-access, budget-matched test with a world law fixed before the language.


### C4 — Was the world tailored to the language? (three samples, one truncated)

All three: **the defence is inadequate, and the tailoring is documented in the design itself.** Most findings restate C3 (see there); the ones that add something:

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | The world was redefined after the language failed an edge case (change 3), and the language changed in the same step. The §6.1 check "if the language cannot express the law, revise" cannot fail. | **Valid.** | Duplicate of C3.5, sharpened: an expressibility check with a revision clause is a guarantee, not a check. |
| 2 | **`swap_next_v` is the law's action as a primitive; `n_i, w_i` are the world's intermediate variables; the collision antecedent is one atom of equality over them.** The language hands the constructor the world's hidden ontology and bypasses the binding problem. | **Valid, with one qualification.** | The slots' (c, v) are the organism's own latent representation, bound by A0 from sensation — that part is legitimate and is what experiment 1 built. But the slot kinematics equal the world's kinematics by design, so `n, w` are the world's next-states, and the action set contains the law's exact operation. The meta-grammar was written by someone who knew the law. A fair design derives the action set from principles fixed before the world, or requires C to compose the action from lower-level operations. |
| 3 | The target's depth (two rules) was matched to K = 3. | **Valid.** | Design §4 says so ("that is deliberate"). Another alignment between world, language and success criterion. |
| 4 | B searches one rule per round greedily; if the first rule alone is not beneficial, B could fail on an expressible law. | Valid as an asymmetry; did not bite here. | The same-target rule is beneficial alone. Note for experiment 3: give both processes the same sequential protocol. |
| 5 | The overall closedness check is dominated by non-collision steps; a lookup could pass it without representing the law. | Valid. | Confirms C3.3: closedness belongs on collision steps against the ceiling. |
| 6 | Phase 2's law was also checked for expressibility before being used. | Valid. | Accumulation was tested only on a pre-fitted feature. |
| 7 | Tie-breaking on record order could break M5. | Invalid here. | M5 passed (reversed order gave the identical rule). |

### C5 — Were changes 2 and 4 pre-registration or rationalisation? (two substantive samples, one empty)

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | "Before any code ran" is unsupported: the file is fingerprinted only at freezing, after the §6 runs, so nothing in the artefact dates change 2 relative to execution. | **Valid as a process finding.** | Change 2 *was* written before the code (same turn, before the first control) — but the artefact cannot prove it, and a claim of timing that the artefact cannot support should not be made. Fix for every future design: hash and timestamp the design at each change (a commit per change would do it). |
| 2 | **Change 2 amends S3's scope while §10 declares §9 fixed.** The frozen document is internally inconsistent. | **Valid.** | §9's S3 text still reads "on collision-containing pairs" with no exclusion; change 2 narrows it without editing it. |
| 3 | The crossing prediction is analytically entailed by C's algorithm (no defects → no rule), so it was not a risky prediction. | **Valid.** | Downgraded from "pre-registered expectation" to "known limitation stated in advance." It was still right to state it before running. |
| 4 | Change 4 is a goalpost move by its own numbers: the original check applied 0.1 to any G0 architecture on collision steps; the lookup was 0.087 below; the check was split after that score. | **Valid.** | Duplicate of C3.7; conceded. |
| 5 | "Memoriser, not machinery" assumes the conclusion that G0 is closed. | **Valid.** | The lookup is a G0 architecture. |
| 6 | The overall-check numbers were never printed. | Valid. | 0.707 vs 0.835; now in file 17. |
| 7 | The principled line: would the same change have been made if the data had come out the other way? Change 2, yes (it was reasoning); change 4, no. | **Accepted as the criterion.** | Applied to experiment 1's changes in file 16 it gives the same verdict the B2 witness gave: 18 and 19 fail it, 16 arguably, 17 is method. |

**What changes because of C4–C5:** added to file 17; and a process rule for every future design — a hash and timestamp per change, not one at freezing.


---

## D. The construction results (file 14)

### D3 — Does the scramble test mean anything about the concepts? (three complete samples)

All three: only a stipulative reading, under which the concepts are replaced by the operationalisation. Mostly confirms C1–C2; what is new:

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | The sentence "not a claim about the code's data flow" is self-defeating: its own evidence is that B was passed "an argument its code never reads." | **Valid.** | Withdrawn in file 17 §1. |
| 2 | **The scramble may have turned some defect records into non-defects** (a permuted outcome can equal the record's prediction), so "same number of defects" was asserted, not checked. | **Valid.** | Counted in the diagnostic below. |
| 3 | No placebo scramble: a column C should ignore, scrambled, to show no effect and rule out generic corruption. | **Valid.** | Run in the diagnostic below (the predicted-field column is read only to classify records, never in scoring). |
| 4 | M6(ii)'s accounting bug undermines M4: if C can build from no-defect records, its collapse under scrambled ones may be the same bug, not loss of defect content. Fix the accounting and rerun both. | **Valid, and done** — file 17 §8b. | With the fix, M6(ii) passes and the placebo passes; but the scramble effect turned out to be **seed-dependent** (2 of 5 permutations gave no degradation), because states recur across records. The witness's suspicion that the scramble did not destroy what it claimed to was right for a different reason than the bug. |
| 5 | Cross-classification controls are needed: a selection process that reads itemised records; a construction process that does not. Scramble sensitivity must cluster by concept, not by implementation. | **Accepted for experiment 3.** | One C and one B cannot support a taxonomy. |
| 6 | Mediation, not input-dependence: instrument C, delete individual records, show specific rule changes. | **Accepted for experiment 3.** | — |
| 7 | Only seed 0 of B was rerun under the scramble. | Valid, trivial. | The code fact applies to every seed; it should not have been listed as evidence at all. |
| 8 | C itself scores and ranks — it is selection over hypotheses with itemised scores. | **Valid.** | Duplicate of C2.3; conceded. The contrast is itemised versus scalar feedback. |
| 9 | Process boundaries unspecified: is the fitness evaluator inside B? If so B reads outcomes in aggregate; if not, C's record collector is outside C too. | **Valid.** | Boundaries must be declared in experiment 3. |

### D4 — Failure modes the results file missed (one complete sample, two empty; the complete one was cut off at its eighth finding)

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **B's "byte-identical" rerun is vacuous**: the argument is never read and is a string literal, not the scrambled records. | **Valid.** | Duplicate of D3.1 and D3.7; conceded in file 17 §1. Should never have been listed as evidence. |
| 2 | C builds and accepts on the same exposure records with no internal validation split; a small positive net by chance can be accepted. | **Valid as a risk; did not bite in phase 1.** | The one rule built has net in the thousands. But the rule is right: phase 2's wrong action (net 2 on a tie) is exactly this risk biting. Experiment 3: hold out a validation subset of the exposure half. |
| 3 | Condition scoring is raw `tp − fp`, which ignores base rates (V = 2,830, N = 4,778) and is neither precision nor a likelihood. | **Valid.** | Confirmed in `construct_round`. It worked here because the target condition is both frequent and near-perfect. A rare perfect condition would lose to a common sloppy one. |
| 4 | Only the top 20 conditions by that score are ever paired with actions (`top_m = 20`). A hard, unlisted cap on the hypothesis space. | **Valid.** | Confirmed. Not in file 14 §10. The right condition ranked first, so the cap did not bite; the cap should have been declared and its effect reported. |
| 5 | The rule language is hardcoded to two slots (`for i, j in ((0, 1), (1, 0))`); with three slots, no rule ever fires on slot 2. | **Valid.** | Confirmed at two places in the code. The experiment declares A0 as a two-slot architecture, so it is not wrong here, but any generality claim is limited to two things. |
| 6 | Given-bound fractions condition on a post-treatment variable (binding at step 2 depends on the rules); unbound pairs are dropped rather than counted as failures. | **Valid; now checked.** | Unconditional rates computed in file 17 §8c: A0+C same-target 0.935 unconditional (0.973 given bound), still above the 0.9 threshold and against 0.000 for A0. The conditioning hid nothing material, but the unconditional figure should have been reported. |
| 7 | The crossing bucket tags any post-change crossing, not the first collision, so an earlier same-target failure could be counted as a crossing failure. | **Valid as code; no effect here.** | Re-bucketed by first collision after the change in file 17 §8c: every bucket count is identical (230 / 541 / 167), so in this world the two classifications coincide. |
| 8 | (cut off) B's fitness optimises overall accuracy, not collision-step fidelity. | Valid as far as it goes. | B's fitness is the overall exposure fitness; C's records are collision-dominated. Another asymmetry for experiment 3's equal-access design. |

### D5 — Is F3 (the invisible law) a result, a triviality, or a design confound? (three complete samples)

All three: **(b) a triviality dressed up, with (c) as the mechanism** — the learner was trained on occupancy and judged on hidden identities. I accept the core of this.

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **F3 follows deductively from the setup**: no sensory defect, no defect record, no rule. A pre-registered prediction entailed by the definitions is a consistency check, not a discovery. | **Valid.** | Reclassified: F3 is a known limitation stated in advance (already conceded at C5.3), not a finding about construction. |
| 2 | **M3 uses the simulator's hidden identities**; the "gap" is a contract mismatch, not something C missed. | **Valid, with one qualification.** | M3 was designed as the finer contract on purpose — the point of a translated-edit test is to ask more than the sensory contract can. But then the result reads "the sensory contract underdetermines identity through crossings", not "C failed." |
| 3 | The given-bound denominators differ between architectures (A0 alone has 99 unbound; A0+C has 21), so fractions are not comparable. | **Valid.** | Unconditional figures now in file 17 §8c; the ranking is unchanged. |
| 4 | S3 was narrowed from "collision-containing pairs" to "no crossing after the change" (change 2), so the failing subset was removed from the threshold. | **Valid.** | Duplicate of C5.2; S3 is reported as **partly failed** from now on: passes on same-target pairs (0.935 unconditional), fails on crossing pairs (0.000), the original S3 text covered both. |
| 5 | **B also fails crossings and M3 was never run for B**, so F3 cannot be about construction. | **Valid, and now run.** | File 17 §8c: B's rule from every seed gives the same M3 figures as C (five seeds identical, seed 3 differs by two pairs), including 0.000 on crossings. F3 is a property of the sensory contract, shared by both processes. |
| 6 | "Invisible law" privileges the simulator's hidden identity as the real law; under the contract, bounce and pass-through are gauge-equivalent. | **Partly valid.** | The world does have identities and the translated-edit test is exactly how file 10 says a finer contract shows up. But "invisible law" should read "identity is underdetermined by occupancy"; C's rule is a correct representative of the equivalence class. |
| 7 | The crossing condition *is* expressible (`n_i == c_j and n_j == c_i`); the limit is C's objective (crossing steps are non-defects, so the condition is penalised), not the contract's representational capacity. | **Valid and sharper than my own statement.** | The language can say it; the error signal cannot select it. So the limit is in the defect-driven criterion. File 14 §10.4 should say so. |
| 8 | "Kind" is never defined in the experiment, so "builds exactly the kinds its contract can see" is unfalsifiable. | **Valid.** | The experiment should define kind as file 10 does (an edit-signature) and show the built rule's signature. It did not. |
| 9 | One world and one contract cannot support a general claim about contracts and kinds. | **Valid.** | Restrict to this world. |
| 10 | "C's single rule reproduces the hand-built pair exactly" is false on M3 crossings. | **Valid.** | Should read "on the sensory metrics; not on identity tracking through crossings." |
| 11 | What would make F3 genuine: make identity observable (or add a cue that breaks the symmetry) and test whether C then builds the crossing rule from the new defects without losing the same-target rule. | **Accepted for experiment 3.** | That is the risky prediction; the one made was not risky. |

### D6 — Construction versus informed search (three complete samples)

All three converge on one deflation: **C and B are two searches over the same fixed meta-grammar; the scramble test shows C reads itemised outcome pairings and B reads a scalar; that is the difference between informed search and blind search, and nothing about construction, creativity or explanation follows.** Most rows duplicate C1–C3 and D3; what is new or sharpened:

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | The provenance test is circular: C is defined as reading V, so scrambling V breaks it; B is defined as not reading V. | **Valid.** | Duplicate of C1/D3, restated as circularity. Conceded. |
| 2 | "C never computes an aggregate fitness" is false — `tp − fp` and `fixed − broken` are aggregates over records. | **Valid.** | File 17 §2. Withdrawn. The honest statement: C uses a defect-local surrogate score. |
| 3 | "Zero fitness evaluations" is a unit mismatch: C scored 3,136 conditions over 7,608 records plus up to 320 condition–action pairs; it simply never called the world's fitness function. | **Valid.** | The cost comparison in file 14 §3 is withdrawn; experiment 3 reports record checks and candidate evaluations for both. |
| 4 | **S6 did not hold (M6(ii) ✗) and phase 2 was run anyway, violating the frozen rule "Phase 2 only if S1–S6 hold" (design §11 step 5).** | **Valid — a protocol breach.** | I read S6 as "content, not carrier ⚠️" and went on. The frozen text says hold, not mostly hold. Phase 2 is out of contract and is reclassified as exploratory. (The patched accounting later passes M6(ii), but that is a post-hoc fix and does not retroactively license phase 2.) |
| 5 | "Wall rule built ✓ (right condition, wrong action)" is false; a rule with the wrong action is not the wall rule. | **Valid.** | S7's first clause is ❌, not ✓. |
| 6 | The collision-step metric cannot see the crossing error (the sensory fields agree at the collision step), so S1's metric is blind to exactly the failure that matters. | **Valid.** | M1 collision-step fidelity was the wrong metric for the crossing half of the law. Only M3 sees it. |
| 7 | M3 not measured for B. | **Valid, now done** — file 17 §8c. | Identical to C. |
| 8 | "Same machinery, two routes" equivocates between same solution and same process. | **Valid.** | Should read: same rule, two algorithms; the algorithms differ in what they read. |
| 9 | C's heuristics (one-step lookahead, first-index tie-break, positive-net stopping) are search biases; phase 2's wrong action is the tie-break biting. | **Valid.** | Already in file 14 §10 as limitations; the witness is right that they are the construction process's *content*, not incidental. |
| 10 | The sensory ceiling is in-sample. | Valid, minor. | It is computed on the evaluation half from the evaluation half's own majority continuation. It is an upper bound, marked as such. |
| 11 | "C correctly declines to invent one" (scramble case) is contradicted by the scrambled run building junk in some seeds. | **Valid.** | The patched-accounting diagnostic (file 17 §8b) shows the scramble is seed-dependent. Withdrawn. |
| 12 | What resists the deflation: only M3's thing-tracking (A0+C 0.973 vs A0 0.000) — and that is rule-added versus no-rule, not construction versus selection, and B is now known to match. | **Accepted.** | This is the residue: the built rule is a component that changes internal tracking, not a surface patch. It is true of B's rule equally. |

### D8 — Does experiment 2 test file 10's definitions? (three complete samples)

One witness (sample 2) noticed that **the design file was not among the documents it was given** and said the S1–S6 mappings were therefore reconstruction. That is a cross-examination failure mode (§0, item added): the D8 item was assembled with files 10 and 14 only. The other two samples reconstructed the mapping from file 14 and reached the same place. The verdict on the mapping does not depend on file 13, because the mapping is not in file 13 either — that is the finding.

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **The experiment never instantiates file 10's formal objects** — no D, E, p, t = (π, τ, σ, λ), Γ, contract C as a set of edit–boundary pairs, no (F1), (F2), (A), no non-circular dependence, no non-vacuity. S1–S6 are loose analogies to Account, Repair, (K), provenance and Build. | **Valid.** | Both experiments were built as operational proxies. The honest statement is that they test proxies the semantics motivates, and that no result so far is a test of any file 10 definition as stated. |
| 2 | S4 misdefines provenance as data-flow ablation; file 10 defines it by physical history (population, variation, survival history H for Sel; episode, construction witness, represented target for Con). | **Valid.** | Duplicate of C1/D3; the file 10 definitions were not instantiated. |
| 3 | C is not shown to satisfy Con (no owned subhistory, no binding construction, no represented target); B is not shown to satisfy Sel (fitness evaluations in a search are not a population with a survival history). | **Valid.** | Follows from 1. |
| 4 | "No fitness number" is not file 10's criterion for construction. | **Valid.** | Duplicate of C2. |
| 5 | "Needed" and "protected" are not file 10 predicates; S1 measures accuracy against an old grammar, S2 measures non-regression. | **Valid.** | The words were chosen for the design and should not have suggested semantic content. |
| 6 | Derivation 3 (underdetermination of selected transports on finite H ⊊ C) is misapplied to construction; the exposure/evaluation split is not H ⊊ C (sequences are not edit–boundary pairs). | **Valid.** | File 14's remark that "Derivation 3 applies to construction too" is withdrawn; a separate statement is needed for constructed transports. |
| 7 | Derivation 5, the Part IX reason-use witness, and Part X's Build are not tested by anything in S1–S6. | **Valid.** | Correct; the experiment claimed at most to bear on Derivation 2 and on D (genesis). |
| 8 | **"Fidelity" in the results means prediction accuracy, not file 10's fidelity (component signatures under translated edits).** | **Valid.** | M1/M2 figures are renamed **prediction accuracy** in file 17. Only M3 is a (partial) fidelity test in file 10's sense. |
| 9 | The experiment's F1/F2/F3 labels collide with file 10's (F1)/(F2) conditions. | **Valid, cosmetic but real.** | Renamed in file 17: the findings are now **Finding-1, Finding-2, Finding-3**. |
| 10 | "Thing identities through translated edits" are not translated edits in file 10's sense (no transport t, no τ). | **Partly valid.** | M3 does apply the same change to world and predictor, which is the operational core of a translated edit; but no transport was written down, so the τ is implicit. |
| 11 | S5 (same output) cannot test "provenance is not output"; it needs two independently verified provenances. | **Valid.** | S5 shows only convergence. |
| 12 | The physical module and admitted edits (Part XIV) are never stated, so no scope claim can be checked. | **Valid.** | The world's admitted edits (displace, set_velocity) are in the code but were never related to a contract C. |
| 13 | "C correctly declines" overclaims; closing an episode is "a decision, not a proof" by file 10's own words. | **Valid.** | Withdrawn with D6.11. |

**What changes because of D4–D8:** phase 2 reclassified as exploratory (protocol breach); S3 partly failed; S7 first clause ❌; F1–F3 renamed; M1/M2 renamed prediction accuracy; M3 run for B; unconditional M3 rates reported; the top-20 cap, the base-rate-blind score and the two-slot hardcoding added to the failure-mode list; and a standing statement that neither experiment instantiates a file 10 definition.

### A8 — Internal contradictions in file 10 (three complete samples, rerun at the model's full budget)

The three samples overlap heavily and between them list about forty tensions. Grouped, with duplicates merged. Rows already conceded under A1–A7 are marked as such.

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **Transport direction is inverted between (R) and Account.** (R) needs a transport from the carrier's organisation *to* the content; Account's transport runs from the target D *to* the explanation E. If the explanation is the carrier and the target the content, Account makes the target represent the explanation. | **Valid.** | Checked against the text: (R) is `Org(o) → c`; Account is `t: D → E` with λ anchoring E's components in D. One convention must be fixed. The natural fix: state that "a transport from D to E" is the map by which E is *held to* D (π, τ, σ go D→E; λ goes E→D), and define (R) with the same orientation, `t: c → Org(o)`, so that "o represents c" and "E accounts for D" have the same shape. As written it is inconsistent. |
| 2 | **Account has no provenance condition, so a declared transport can satisfy (E); but Part IV says a declared transport represents nothing, and Part XI's Deploy requires selected or constructed.** | **Valid.** | The intended structure: Account is a predicate on a *modelled* candidate (any provenance, including declared, because a modeller must be able to assess an account without settling its history); representation and (EK) add the provenance condition. The text never says this. Add one sentence to Part V and require Sel/Con in (EK) explicitly. |
| 3 | Non-vacuity says the contract is a "declared subset" of the admitted edits, while Part III allows selected and constructed contracts. Equivocation on "declared" (provenance term versus "stated"). | **Valid.** | Replace with "a stated subset"; the honesty condition is about the record, not the provenance. |
| 4 | Account's arity and type are inconsistent: one-place on a tuple in Part V; two-place (content, question) in Parts IX and XI. | **Valid.** | Type error. Define `Account(E, p)` with t and Γ existentially quantified, or write the tuple everywhere. |
| 5 | Grievance 4's objectivity is undercut by Derivation 7: a criticism that supplies an excluded change is a *new* claim at a new index and cannot refute the original claim on C; so scope-honesty does not stop protective narrowing. | **Valid, serious.** | The text conflates "faithful on C" with "C is not protective." The second is a claim about the *choice* of C and needs its own condition — for instance that C be maximal among stated contracts the physics admits, or that a narrowing after a failed criticism be flagged as such by the provenance record. Without it the objectivity claim is contract-relative only, which is exactly Grievance 4's complaint. |
| 6 | Grain ℓ is a declared index that determines Org_ℓ(o) and hence which components exist; but (K) indexes kinds to the contract only. Kinds are therefore grain-relative too, and grain is free. | **Valid.** | Duplicate of A1's hidden-primitive finding, restated as an inconsistency. (K) must be indexed to (ℓ, C), or grain must be fixed by the physical module. |
| 7 | "Exactly one of three provenances" versus "selection may continue to operate beneath construction": Sel and Con are not defined to be disjoint. | **Valid.** | Define provenance as *originating* history with a priority rule (constructed if a construction witness exists; else selected; else declared), and treat maintenance histories separately. |
| 8 | Derivation 3 assumes the component relations are supplied independently per edit–boundary pair; Part II never states that. | **Valid.** | Duplicate of A2's Derivation 3 defect; sharpened. State it as a hypothesis of the theorem. |
| 9 | "Two primitives" is contradicted by the organisation data (V, X, J, B, A, L) and by the supplied L_j, which are neither derived from Θ nor from N; and "(O) and (Q) depend on nothing" is false since both take that data. | **Valid.** | Duplicate of A1. The honest statement: two primitives *plus* the organisation interpretation as a parameter. |
| 10 | Derivation 1 applies a component-only notion (signature) to a subnetwork λ(k). | **Valid.** | Duplicate of A2 (Derivation 1 type error). |
| 11 | Derivation 2 ignores Γ: two candidates with different active commitments can satisfy (F1), (F2), (A) and be different accounts. | **Valid.** | Adds to A2's finding that Derivation 2 is false as stated: it fails for different decompositions *and* for different Γ. |
| 12 | Derivation 10 claims (EK) without the critical-episode conditions (recognised difficulty, conjectural objection, content-sensitive response). | **Valid.** | The example has surprise and construction only. Weaken to (G)/(P). |
| 13 | (EK) is factive (actual repair, actual account) while Part I insists systems can be wrong about all of this; and "nothing depends on 'is knowledge'" sits oddly beside a predicate named CreateEK. | **Partly valid.** | (EK) is an external success predicate; that is deliberate and consistent with fallibilism (a system can create knowledge without knowing it did). But the text should say so, and "created knowledge" must be distinguished from "claims to have." The naming point is cosmetic. |
| 14 | Derivation 8 (equivariance under structure-preserving bijections) is overbroad: it must also preserve physical admission, scope records, obligations and N. | **Valid.** | Restrict the bijections. |
| 15 | Declared provenance is not a physical history, yet the scope sentence says all three are "determined by history in the physical module." | **Valid, minor.** | Wording. |
| 16 | Question-finding provenance is attached to the contract, but a question can be new by changing the respect Q with the contract unchanged; Derivation 5 then treats the contract as (C, Q), contradicting Part III. | **Valid.** | Duplicate of A2's Derivation 5 finding; the fix is to attach provenance to the whole question p. |
| 17 | Grievance 1's cause/correlation criterion (response to an intervention on the *input*) does not match Part II's formal causal signature (change under intervention on the *output* port and under replacement). | **Valid.** | Align the intro with (K). |
| 18 | Derivation 7's frozen assessment conflicts with Part III's prohibition of changing C during an assessment "if recorded" — the recording clause lets a change in mid-assessment count. | **Partly valid.** | Part III's sentence is ambiguous; the intent is that any change ends the assessment and starts a new one, and the record is what shows that. Reword. |
| 19 | Non-circular dependence removes a block of Γ in E using an edit from C, which is a contract on D. | **Valid.** | Type error: the removing edit must be an edit on E (or τ of an edit on D). |
| 20 | Smaller items: "four conditions" but five conjuncts in Account; Non-vacuity's last sentence describes a non-circular-dependence failure; Bearing's parameters mismatch; RetReal is vacuous on empty execution families; (EK) has free variables; the identification example names the wrong feature. | **Valid, cosmetic to minor.** | All go on the revision list. |

**What changes because of A8:** the file 10 revision list gains the direction fix (1), the provenance clause on Account (2), the objectivity condition on contract choice (5), a priority rule for provenance (7), and the type fixes (4, 10, 19). With A1–A7 this is now a complete list; the revision is the next thing to do and has not been started.

---

### B1 — Confounds in experiment 1's design and interpretation (two complete samples after rerun, one still empty at the time of writing)

Most rows duplicate B2, B4 and B5 (neutrality, pre-registration, the 0.95 criterion, the M3 oracle, occlusion rationale) and are already conceded in file 16. What is new:

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **For slot architectures the exposure/evaluation split does nothing**: they have nothing to learn from exposure, selection is exhaustive on the evaluation half, so their reported fitness is the selection criterion, not held-out performance. | **Valid.** | Correct and not noticed by me. The split defends against the lookup's memorisation only. A three-way split (exposure, selection, test) or cross-validation over configurations is needed to report generalisation for the selected architecture. |
| 2 | The split guarantees unseen *configurations*, not unseen *sensory prefixes*; many configurations share prefixes, so the held-out lookup score (0.656) is partly shared-prefix transfer. | **Valid.** | "Instances not seen" overstated. Report prefix overlap. |
| 3 | **The sensory ceiling is a full-prefix memoriser** (unbounded memory) computed on the same history it bounds; it is strictly more powerful than any k ≤ 3 architecture and is an in-sample maximum, not a bound on what can be learned. | **Valid.** | Checked in the code: the key is the whole prefix. Rename "in-sample maximum from sensation"; compute per-k ceilings for a fair comparison. The first ceiling being exceeded (change 11) shows it was used as a benchmark before it was defined properly. |
| 4 | **Selection on H_full is fragile**: τ = ∞ beats τ = 5 by 0.003 (0.801 vs 0.798), with no variance estimate. | **Valid; now checked** — see file 16 §15. | A per-configuration comparison between the two on the evaluation half is run below. |
| 5 | The last-writer-wins lookup is order-dependent, so the lookup-versus-slot comparison is confounded by the memory update rule. | **Valid, minor.** | Majority continuation would be the fair table. It does not change the conclusion (the held-out lookup collapses for a different reason) but it should be fixed in experiment 3's baseline. |
| 6 | Swap is a sensory no-op and dilutes the change set in M1/M2. | Valid, minor. | It contributes identity-like sequences; harmless to the ranking, should be excluded from fitness. |
| 7 | "No sampling; every number is exact" is misleading: exact on this finite evaluation half, and a different split could select a different architecture. | **Valid.** | Duplicate of 1 and 4 in substance; the sentence should say what "exact" means. |
| 8 | The post-hoc j-gene finding (teleport versus turn) lacks support beyond one table. | Partly valid. | It was labelled as unplanned in file 12; it should also be labelled as unreplicated. |
| 9 | The rival correspondence view is not tested. | Valid. | Duplicate of B4's strawman finding. |
| 10 | The conclusion generalises from one kind to all kinds. | Valid. | Restrict to persistence in this world. |

**B2 — third sample (rerun).** The third witness ran the same change-by-change audit as the first two and reached the same verdicts, rating changes 8, 16, 18 and 19 fatal to the pre-registration claim, and adding that change 14 (the j gene) *expanded the hypothesis space after a control run* and so is construction by the experimenter, not selection. Accepted; already in file 16 §1 and §13.

### B3 — Bugs in experiment 1's code (two complete samples after rerun, one still empty)

The witnesses read the code and made claims about it that I could test. Checked on the frozen code in file 16 §16.

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **The four-way τ tie on H_neutral is a necessity of the code**: at search radius 5 (which spans the line, and is the radius of every tied winner), the one thing is re-bound in the same step it moves, the unconfirmed count never exceeds 0, and τ is never consulted. | **Valid, and fatal to the tie as a finding.** | Instrumented: zero count events at radius 5 for every τ; 28–54 at radius 2, where the τ values then differ. The tie is a fact about the grammar, not about the world. |
| 2 | **The lookup baseline is crippled four ways** (no fall-back to shorter keys, all-zero default on unseen keys, last-writer table, sees only the last k fields), so "slot beats lookup" was guaranteed. | **Valid, and it changes the headline.** | A fair k = 3 memoriser scores 0.801 on held-out H_full; the tracker scores 0.801. File 16 §16(e) and §17. |
| 3 | M2 on H_full is literally M1 on H_full (same change set, same table). | **Valid.** | 208 of 208 rows equal. Double-counted in file 12. |
| 4 | Swap is observationally identical to identity; a whole condition tests nothing in fitness and doubles the weight of "nothing happens". | **Valid.** | 171 of 171 configurations bit-identical. |
| 5 | The thing-signature test injects the change into the predictor's slots, so for τ = ∞ tracking afterwards is a fixpoint of the shared kinematics; the test's only discriminating power is persist versus rebind and τ versus gap length. | **Valid as a description; partly valid as a criticism.** | Injecting the change into the representation is what a translated edit *is* (the edit is carried across the transport), so this is the intended design, not a bug. But the witness is right about what the test can discriminate: preservation under persistence, nothing more. Already narrowed in file 16 §5; M3 is a persistence test and should be named one. |
| 6 | Binding at step 2 is a precondition that guarantees the pass; unbound pairs leave the denominator. | **Valid.** | Duplicate of B5.1; verdict there raised to Valid, serious (see E below). |
| 7 | The function returns passed / total, not the given-bound figure file 12 quotes; that number is not emitted by the code. | **Valid.** | A reporting defect: the quoted figure was computed by hand from the emitted counts. Every future run emits both. |
| 8 | The adequacy check is half-implemented: the 0.95-of-ceiling clause is computed but never enters the boolean. | **Valid.** | Confirmed at the line. The design's criterion was loosened in code without saying so; file 16 §3 already withdrew the 0.95 claim, but the code should have failed loudly. |
| 9 | The neutrality check drops `rebind` while its own docstring includes it. | Valid. | Duplicate of B2's change 19; conceded. |
| 10 | The sensory ceiling is an in-sample oracle on the evaluation half with unbounded memory. | Valid. | Duplicate of B1.3. |
| 11 | Model selection and the evolutionary confirmation both maximise the same evaluation-half number, so "the search lands on the same architecture" is the same statistic twice; the evolutionary run is a near-exhaustive search of 208 points. | **Valid.** | Duplicate of B1.1 for the first part; the second part is new and right: ≥ 1,280 evaluations over 208 points with elitism is not a reachability test. |
| 12 | The "unique win" of τ = ∞ over τ = 5 rests on a one-step margin set by run length and occlusion timing. | **Valid on the mechanism; the direction survives.** | The margin is small and systematic (file 16 §15). "Uniquely" should read "by a margin that the run length caps at one prediction per sequence." Add τ = 10 to the grid in any rerun. |
| 13 | The split by configuration index is a parity checkerboard on (cell, velocity) for the one-thing world. | Valid, moderate. | Not random; report composition or stratify. |
| 14 | The prediction for the change step is unpredictable for every architecture and deflates all scores by a constant. | Valid, moderate. | Report per-step accuracy; exclude the step or report it separately. |
| 15 | The world's dynamics and the model's dynamics are the same function, so the grammar contains a perfect tracker and "emergence" is close to analytic. | **Valid.** | Already conceded under B4 (the kind is a parameter value); restated with the mechanism. The honest sentence is "the grammar contains a perfect tracker and occlusion selects it, if you exclude memorisers." |
| 16 | `mutate` can be a no-op. | Valid, minor. | — |

**What changes because of B3:** file 16 §16–17; the neutral-world tie is no longer a finding; the adequacy claim and "history selects tracking over memorisation" are withdrawn; M3 is renamed a persistence test; every run emits both M3 denominators.

---

## E. Audit of this adjudication (three DeepSeek passes over file 15 as it stood at D8)

I asked the witness to find where my verdicts were too soft on myself. The three passes agree on one pattern and list about thirty rows. **The pattern is real and I accept it:** wherever I had a repair in mind, I marked the finding "Partly valid" although it was valid against the text as written, and I used non-verdicts ("Accepted for experiment 3", "did not bite here", "Valid as far as it goes") that defer a ruling on the current claim. The rule from here on: **the verdict is on the text as written; the repair goes in the change list; a finding accepted for a future experiment is Valid against the current one.**

Verdicts restated under that rule (row → new verdict). I have not rewritten the tables above; this list overrides them where they differ.

| Row | Was | Now | Note |
|---|---|---|---|
| A1.5 (grain unconstrained) | Partly valid | **Valid, serious** | The constraint is a proposal, not a defence. |
| A1.7 ("relevant" undefined) | Partly valid, minor | **Valid, serious** | Checked: "relevant" occurs inside the formal Build predicate (Part X) and inside the barrier condition (Part XIII), not only in the informal opening. |
| A1.8 (O_p in every question) | Partly valid | **Valid** | The normative apparatus is pervasive; the O_p/𝒩 distinction does not change that. |
| A1.12 (declared provenance not physical) | Valid, minor | **Valid, serious** | It matters for the taxonomy that experiment 2 leaned on. |
| A1.15 (Lic, Scope, Live undefined) | Partly valid, minor | **Valid** | "Declared data" is not a definition. |
| A1.16 (controlled action smuggles agency) | Partly valid | **Valid** | The replacement concedes it. |
| A1.18–19 (restriction, independent boundary undefined) | Valid, minor | **Valid, serious** | They carry non-circular dependence and (A). |
| A1.20 ((O), (Q) depend on nothing) | Invalid | **Partly valid** | Schemata over supplied data; the document must say so. |
| A2.6 (Derivation 2 weakened; "all the experiments used" the weak form) | asserted | **Audited** | Experiment 1's tie was read as "one kind on that contract" — the weak form, and on H_neutral at radius 5 it holds byte-for-byte (file 16 §16(b)). No conclusion used the strong form. |
| A3.5 (non-vacuity trivially satisfied) | Partly valid | **Valid, serious** | It does no work against the counterexample. |
| A5.3 (dispositions) | Partly valid; invalid as refutation | **Valid (gap)** | The refutation reading was a strawman of the finding. |
| A5.8 (kind-label needed to choose the anchor) | Partly valid | **Valid** | "Once both routes exist" assumes a route the question may not contain. |
| A5.12 (recorded exclusion not an answer) | Partly valid | **Valid** | And the case where a record exists remains: a historical record is not a forward answer. |
| A6.E.21 (no notion of a good question) | Partly valid | **Valid** | The merit criterion does not exist in the text. |
| A6.D.8 (Derivation 3 proof defect) | Valid as proof defect | **Valid, serious; original withdrawn** | The corrected claim is a new claim. |
| A7.3, A7.5, A7.6 (decoy; pole and shadow; realism) | Partly valid, repaired | **Valid** | The repair (C_phys, historical kinds) is new machinery. |
| A7.9 (Derivation 1 circular against the steelman) | Duplicate | **Valid, distinct** | Circularity is a separate charge from scope. |
| B2.9 (fitness target is a normative choice) | Partly valid | **Valid, serious** | It sets the direction of the result. |
| B4.10 (§7.3 not run as a transfer test) | Invalid | **Valid** | My own reason refuted my verdict: if slot architectures do not learn, M2 is zero-shot evaluation, not transfer. |
| B4.12 (argmax is not selection) | Valid, wording | **Valid, serious** | It bears on whether "selected" provenance was instantiated at all. |
| B5.1 (M3 conditions on the property it tests) | Partly valid | **Valid, serious** | The conclusion was drawn from the conditional figure. |
| C1.6, D3.5, D3.6, D5.11 ("accepted for experiment 3") | non-verdicts | **Valid against the current experiment** | The current claims (M4 as a provenance test; the taxonomy; mediation; F3 as a result) are withdrawn now, not deferred. |
| C2.3 (C/B collapse) | Valid for what was shown | **Valid, fatal to the advertised claim** | Already the effect of file 17 §1–3; the verdict should say so. |
| C3.6 (fidelity overclaim) | Partly valid | **Valid** | Pre-registration mitigates the honesty charge, not the overclaim. |
| C4.1 (revision clause cannot fail) | Duplicate of C3.5 | **Valid, distinct** | A process defect, not the tailoring itself. |
| C4.4 (B's greedy protocol) | did not bite | **Valid, serious for general claims** | — |
| D3.4 (scramble undermined by its own diagnostic) | Valid, and done | **Valid, serious; M4 conditioned** | Two of five permutations did nothing; M4 holds only for permutations that break the state→outcome map. |
| D4.2 (no validation split) | did not bite in phase 1 | **Valid, serious; it bit in phase 2** | — |
| D4.8 (B's objective mismatch) | as far as it goes | **Valid, serious for every C/B comparison** | Matched objectives in experiment 3. |
| D5.6 (gauge equivalence) | Partly valid | **Valid** | The wording is withdrawn. |
| D8.10 (translated edits) | Partly valid | **Valid** | No transport was written down; M3 is an operational proxy. |
| B4.5 (kind as parameter value; deferred to experiment 2) | Valid for the headline | **Valid; neither experiment tests it** | D8.1 rules that experiment 2 does not either. |

Rejected or qualified audit findings: (i) "the adjudication is prospective, so the original overclaims survive in files 10–14" — files 11–14 are frozen artefacts with recorded hashes and will not be edited; files 16 and 17 are the authoritative statements of what those experiments show, and file 10 is to be revised, not patched. The audit is right that this must be said in the files themselves; it is said here and in the project story. (ii) "Section 0.1 is promised and never delivered" — correct; the reference is removed and the Atria diagnosis is item 6 of §0. (iii) "A2 and D4 verdicts rest on truncated evidence" — correct at the time; A2's remaining samples and D4's remaining samples are ruled on as they land, and D8 was rerun with the design file supplied.

### E2 — Audit of the errata (three passes over files 16 and 17)

All three passes reached the same verdict: **the "what the experiment now claims" paragraphs survived by omission.** Each was written before the concessions in the same file were complete, and each kept a flattering word ("underpowered" for failed, "selected" for scored highest under exhaustive search, "stopped correctly", "local-credit-assignment", "no global evaluations", "exactly the same", "three weaknesses … one confound") that the file's own sections had already undercut. I accept every one of these rows; the two claim paragraphs are rewritten (file 16 §17, file 17 §9) so that every sentence carries its concession, and the old paragraph in file 16 is marked superseded.

Specific rows accepted beyond the pattern: four changes not three (16 §1 vs §14); changes 2 and 11 omitted from the verdict list; "frozen-before-pilots" wording contradicts §1; the in-sample ceiling under the 0.881 ratio; the thing-kind unconditional failure and the corrected conditional headline absent from the claims; "B does exactly the same" ignores seed 3 and is a diagnostic, not the frozen run; "with the defect accounting fixed" imported a patched diagnostic into the frozen claim; the scramble claim stronger than three-of-five weak permutations support; the closedness figures absent from the "built" claim; the proxy caveat absent. Rejected: none. Qualified: "label all experiment 1 results exploratory and rerun on fresh histories" — accepted as the description (pilot-contaminated), and the rerun belongs to experiment 3's protocol rather than to a repeat of experiment 1, which the fair-memoriser result has made moot.

### E3 — Audit of over-concession (three passes)

The opposite audit: where did I concede what was wrong, or more than the finding warranted? This is the audit that matters most for "you are the authority", so each row is ruled, not waved through.

| # | Audit finding | Ruling | Why |
|---|---|---|---|
| 1 | **My change list is internally inconsistent about the contract.** A1.2 fixes C = C_phys ∩ S (so C ⊆ C_phys); A4.3 requires contracts that contain explicitly counterfactual edits (for impossibility explanations); A5.3 says file 10 *kept* FW5's rule while A4.3 says it *tightened* it. | **Accepted.** | Real. File 10's non-vacuity says "a declared subset of the physically admitted edits", so file 10 tightened; A5.3's "keeps" was wrong. The single repair: C = (C_phys ∩ S) ∪ K, K a declared set of counterfactual edits each with its stated meaning; fidelity tests run on C; world-kind is signature on C_phys; K enters non-vacuity only through its stated meaning. |
| 2 | Two mutually inconsistent repairs to Sel's "no member of the history represents…" clause (A1.11 versus A6.5/A6.1). | **Accepted.** | Adopt A6.1's wording: the condition is on the events of the selection process, not on H. A1.11 marked superseded. A6.2's non-triviality conditions are likewise rewritten over the selection history, not over H. |
| 3 | A1.6's repair for Org_ℓ and A7.1's C_phys both quantify over "Θ's admitted edits", which D8.12 (accepted) says file 10 never states. | **Accepted.** | The repairs are promissory until file 10 states Θ's admitted edit set. First item on the revision list. |
| 4 | A6.3 defines blindness by the scramble test that section C declares vacuous, and contradicts C1.4 (B does receive the defect, as a scalar). | **Accepted.** | Blindness = no *itemised* representation of the defect on the route, the scalar explicitly allowed; tested by scrambling both the record channel and the scalar channel. |
| 5 | A6.9 turns B2.9's normative fitness choice into a semantic premise. | **Accepted.** | It is a stipulated survival criterion and must be labelled one, with its direction noted. |
| 6 | **C3.1 "G0 grew" is not fatal**: index "grew" to the candidate's mutable rule set at t and it is true. | **Rejected as to the verdict; accepted as to the wording.** | Under that index "grew" is true of B as well (C3.2), so it cannot do what the design wanted — distinguish construction from selection. The verdict stands as "fatal to growth as a discriminator"; the sentence "false or vacuous" is replaced by "true under the only index on which it is true of both processes." |
| 7 | C3.9: S5 (same output) does not license striking "distinct from selection", because provenance is history, not output. | **Partly accepted.** | Right that same output does not refute distinct provenance. But the experiment offered nothing else in favour, so "distinct" is *not shown*, which is what striking it from the supported claims means. Reworded so. |
| 8 | D6.4 "protocol breach" overstates: S6 was recorded as a warning. | **Rejected.** | The frozen rule had no warning category; "⚠️" was my gloss on a clause that was ✗. Breach stands. |
| 9 | D8.1 ("never instantiates any definition") contradicts D8.10 (M3 partially instantiates translated-edit fidelity). | **Accepted as a wording fix.** | Neither experiment instantiates a definition *as stated* (the formal tuple); M3 is a partial operational proxy for translated-edit fidelity with the transport implicit. Both rows now say this. |
| 10 | A1.6: Org_ℓ is underconstrained, not yet a third primitive; do the derivation before conceding the count. | **Partly accepted.** | "Hidden parameter until the constraint in A1.6 is shown to derive it from Θ" replaces "third primitive". Whether it derives is open, and the burden is on file 10. |
| 11 | B2.4: change 19 may be a clarification, since rebind lacks the mechanism under test. | **Rejected.** | Design §2.6 named rebind as part of the kind under test; the exclusion came after the number. Both figures are reported; the verdict stands. |
| 12 | A1.8, A1.12, A1.15, A1.16 are documentation notes rated as defects. | **Rejected**, with the disagreement noted. | The E1 audit argued the opposite on the same rows. My ruling: an undefined term inside a formal predicate is a defect, whatever the intended reading; a term that only needs a sentence of gloss is cosmetic. A1.15 is the first kind (Lic, Scope, Live appear in the appraisal conditions); A1.12 and A1.16 are the second and are downgraded to cosmetic; A1.8 stays Valid (the normative apparatus is pervasive; that is a fact to state, not a defect to fix). |
| 13 | §0.8's defence of the badly built D8 item is circular; §0.12's "commonest error" is asserted, not exhibited. | **Accepted.** | D8 was rerun with the design file (D8b, below). §0.12's sentence is deleted. |
| 14 | A1.4's "Why" answers a definition-order complaint, not the presupposition complaint. | Accepted, minor. | Folded into A1.11: content identity at the primitive layer is the primitive-layer notion, not Rep. |
| 15 | C2.1 / C2.2 / C2.3: "aggregate" over-conceded; a scalar is not yet a representation; same fidelity does not mean same process. | **Partly accepted.** | The word "aggregate" was wrong in file 14 and the concession stands. The substantive contrast — per-record credit versus one global scalar — survives, and that is exactly what file 17 §9 now says. Same fidelity does not show same process; the experiment did not show a *different* process either, which is what "collapses to efficiency" meant. |

Net effect of E1 and E3 together: the verdicts move against the text as written (E1), and the *repairs* in the change list are now checked against each other for consistency (E3). Four inconsistencies in the change list are fixed above (rows 1–4). The file 10 revision must start from the consolidated list, not from the per-section change lists.

### D1 — Does the results file overclaim against its own design? (three complete samples after rerun)

Most rows duplicate D3–D6 (byte-identical vacuous; "no aggregate fitness" false; phase 2 breach; S6 and S7 should be ❌; "same machinery" trivial; given-bound conditioning). New and ruled:

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **The two post-freeze diagnostics in file 14 violate the design's own rule that no measurement is added after freezing.** | **Valid.** | Design §10 forbids it; I ran them to explain two failures and said so. They are labelled diagnostics but should have been labelled breaches. Every post-hoc diagnostic in files 16–17 is now labelled as such and none is used to support a frozen claim (file 15 §E2). |
| 2 | "Phase 1 held on every supporting outcome but one clause" is false: S6 is an outcome and it failed. | **Valid.** | File 17 §9 and §11. |
| 3 | "The crack it exposed was pre-registered" conflates having a pre-registered test with having predicted its failure. | **Valid.** | Withdrawn. |
| 4 | "Using no fitness number at all" hides that C also read 4,778 non-defect records to score conditions. | **Valid.** | File 17 §9 now says so. |
| 5 | S1's margin (0.087) is below the 0.1 threshold the design uses elsewhere; S1 ✅ is not earned. | **Valid.** | S1 is reclassified: not shown against the memoriser. |
| 6 | "Vacuous in this world" overclaims for B's extra atoms; the example of where a junk atom would matter is wrong. | Valid, minor. | Seed 3's atom costs two M3 pairs (file 17 §8c). |
| 7 | "938 + 951 = 1,889 sequences does not match 135 configurations." | **Invalid.** | 135 configurations × 14 changes = 1,890, less one inadmissible sequence. |
| 8 | C stops on "no positive net", not on the design's "until no defects remain or 3 rules". | Partly valid. | The design's round description includes the positive-net acceptance; the stopping sentence should have said so. |
| 9 | The API-key note in file 14 §10 treats a security incident as a footnote; rotate now. | **Valid.** | The keys never entered any deliverable (checked by search); they are in the chat transcript, which I cannot edit. Rotation is the user's action and is the first line of the next step. |

### D8b — D8 rerun with the design file supplied (three complete samples)

The verdict does not change with file 13 in hand: S1–S6 are loose analogies to file 10's predicates, the mapping is absent from the design as well as the results, and nothing in either experiment instantiates a definition as stated. New in D8b: the hand-built rules are *declared* provenance and cannot serve as a test of non-declared transport (valid); S5's output equality is already predicted by Derivation 2 and says nothing about provenance (valid); the best-of-G0 "memoriser" distinction is extra-theoretic (valid — file 10 has no memoriser predicate). The process defect in §0.8 is closed.

### E4 — Attack on experiment 3's design before it is built (three passes)

Accepted almost whole. The sketch in file 17 §10 had the same flaw as experiment 2: **"itemised versus scalar" is under-defined and can be analytic.** A scalar can be a sufficient statistic of the records (a likelihood), in which case the scalar process has all the information and the contrast is about credit *route*, not information; or the scalar can be invariant to the scramble by choice, in which case "only the per-record process changes" is entailed. "Equal access" and "must collapse to a scalar" contradict each other unless the process boundary is declared. "Same search operator" is ill-defined across different credit signals. "A world law fixed before the language" cannot be met by an author who knows the law. The witness's sharpest version — a matched-information, cross-classified, held-out-law test of **credit granularity**, with a sufficient-statistic scalar as the critical control, a blinded law generator, within-state scrambles verified by mutual information, mediation by record deletion, unconditional metrics, and a power plan — replaces §10 of file 17. Its name changes accordingly: it is not a construction-versus-selection experiment; it is a test of whether per-record credit buys anything that a sufficient scalar does not. That is a smaller question, and it is the one the evidence so far actually raises.

---

## F. The second witness (Atria-Dawn-Preview, one sample per item after the restart; A1 and A2 with two)

Atria's replies are longer, more formal and less repetitive than DeepSeek's, and on the semantics they converge with DeepSeek on every major hit while adding a few. Rows already conceded under A1–A8 are not repeated.

### F-A1 — Hidden primitives (two samples)

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | Sel is stated using "represents" ("no member of the history represents t…") while (R) is stated using Sel: the dependence order is circular or the clause is informal. | **Valid.** | Adds to A1.11/A6.5: adopt A6.1's event-level wording without the word "represents". |
| 2 | Org_ℓ(o) is used as a function ("the organisation that o instantiates") but a physical occurrence can instantiate several organisations at one grain; (R) is ill-posed without a uniqueness axiom or a relation. | **Valid, serious.** | New. Make Org a relation and (R) existential over it, or state uniqueness as an axiom of Θ. |
| 3 | Org_ℓ must return a full organisation (ports, domains, components, relations) — a decomposition oracle dressed as physics. | **Valid.** | Sharpens A1.6: the burden is on file 10 to show the task-based Θ yields decompositions, or to count the decomposition as a declared index. |
| 4 | "Non-question-begging" (Part XIII, barriers) is an undefined epistemic-adequacy predicate — the forbidden kind. | **Valid.** | New. Replace with a structural condition. |
| 5 | Undefined relation symbols used in formal clauses: ProducedBy, ProducesVia, Result, Lic, Scope, Live, Enable, ≡_ℓ, Exec. | **Valid.** | Consolidates A1.15/18/19 and adds Result, Enable, Exec. Define or count as primitives. |
| 6 | Non-circular dependence catches only *total* protection; a contract that excludes only the embarrassing edits passes (E); the document's remedy is external (Grievance 4). | **Valid, serious.** | Duplicate of A8.5 from the other side; the contract-adequacy condition is needed. |
| 7 | ≺_h is called causal precedence and is not shown to come from Θ. | Valid, minor. | State it is Θ's admitted-process dependency order. |
| 8 | Derivation 4 conflates the transport's contract with the world's. | Valid, minor. | Distinguish C_t from C_world; out-of-contract surprise has no place in the semantics. |
| 9 | Part XIV's index list omits C's provenance; C is an index with provenance, and a content when constructed. | Valid, cosmetic. | — |
| 10 | (I3) missing from the labels; notation Org_ℓ / Org_l varies. | Cosmetic. | — |

### F-A2 — The derivations (two samples)

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | Derivation 1 extends (K) from components to subnetworks without defining subnetwork signature; "up to the port translation" needs (τ, σ) injective on C. | **Valid.** | Same as DeepSeek A2 with the missing hypothesis named. |
| 2 | **Derivation 1's corollary is question-begging**: "kind" is defined by signature, so "(F1) ⇒ same kind" is analytic, and the dichotomy it offers restates the definition. The opponent's claim — a kind-label can discriminate where no admitted change does — is foreclosed by fiat. | **Valid, serious.** | This is the load-bearing move for "no anchoring condition", and A7's steelman already showed the opponent wins on C_phys. The corollary must be presented as the *analysis-of-kinds conjecture* that Part XV already lists, not as a theorem that "loses no case". |
| 3 | Derivation 3 assumes a richness condition on the population (the altered transport must be *in* T); "admitted relation" and "value at (a,b)" are undefined; the finiteness of H is never used. | **Valid.** | Duplicate of A2/A6/A8 with the exact hypothesis named. |
| 4 | Derivation 3's consequence slides from underdetermination (no guarantee) to fallibility (actual failure) and to surprise. | **Valid.** | "Selection provides no guarantee of fidelity off H" is what was shown. |
| 5 | **Derivation 4 is vacuous**: surprise is *defined* as a violation off H, so "surprise requires H ⊊ C" unpacks the definition; "derived, not assumed" is false. | **Valid, serious.** | New. Retract "derived, not assumed" or prove something non-trivial (conditions under which a violation actually occurs). |
| 6 | Derivation 6 lists undefined symbols (as F-A1.5) and slides from "no undefined vocabulary" to "no residual predicate meaning explains": adequacy is a conjecture, not a theorem. | **Valid.** | Restrict the consequence to the formal property. |
| 7 | Derivation 10's example asserts (F1) for the extended transport without exhibiting ports, components or relations for P or S_1; "they are objects" reintroduces the unqualified kind-claim the semantics forbids; Derivation 2 is mis-cited for two components of one organisation; (EK) is claimed without the critical-episode constituents; the "structural, not parametric" failure is a stipulation on T. | **Valid on every point.** | The two-layer episode is an illustrative scenario, not a consistency witness, until it is formalised enough to check the axioms. Relabel. |
| 8 | Derivation 5's proof is a sketch: the contract-as-organisation is not built, and the level of the construction is unclear. | Valid. | Duplicate of A2/A8. |

**What changes because of the second witness:** three new items on the revision list — Org as a relation or a uniqueness axiom; "non-question-begging" replaced; Derivation 4 retracted as a derivation — and two upgrades: Derivation 1's corollary is reclassified from theorem to conjecture, and Derivation 10 from witness to scenario. The rest confirms the first witness, which is itself worth having: two models with different training reached the same holes independently.

### Addendum from the rerun samples of B5, C1, C3, C5 (all complete now)

The extra samples repeat the rulings above with four additions on the thing-tracking test (B5), all accepted: (1) reconcile cannot fail for four of the five change types, so the only content of M3 is the occlusion row, which restates the τ gene; (2) M3 has no negative control and no baseline, so a fraction of 1.0 was uninterpretable on its own — the diagnostic in file 16 §16 and the A0 rows in file 17 §8c now supply them; (3) the check at the change step itself is tautological, since the slot has just been set to the world's value, which inflates the fraction with trivial passes — every future M3 scores from the step after the change; (4) design §4's criterion "τ > 0 ⇒ thing-kind" contradicts M3's own occlusion row for τ = 2 and τ = 5, so the criterion was never the one the code evaluated. With B3.5, the honest name for M3 is **a persistence test under injected changes**, and its evidential value in experiment 1 is confined to the occlusion row.

---

## G. Consolidated revision list for file 10

The per-section change lists above conflict in four places (E3 rows 1–4); this list supersedes them. It is a list, not the revision. The revision has not been started.

**G1. Primitives and parameters (A1, A8, F-A1).** Two primitive packages (Θ, 𝒩) *plus* the organisation interpretation (V, X, J, B, A, L) as a declared parameter, *plus* the declared indices (ℓ, β, Ω, C with its provenance). State Θ's admitted edit set explicitly before anything quantifies over it. Org_ℓ becomes a relation between occurrences and organisations at a grain, with (R) existential over it, or a uniqueness axiom is stated; the burden of showing the task-based Θ yields decompositions stays with the text. Admissible grains are constrained (coarsenings under which components keep signatures Θ's admitted edits realise). Define or count as primitive: ProducedBy, ProducesVia, Result, Lic, Scope, Live, Enable, ≡_ℓ, Exec, restriction, observation edit, independent boundary, nontrivial binding construction, content-preserving recoding, owned, relevant (in Build and in barriers), non-question-begging (replaced by a structural condition), ≺_h (Θ's process order). "(O) and (Q) depend on nothing" becomes "are schemata over the supplied organisation and query."

**G2. Contracts (A1.2, A4.3, A5.10, E3.1).** One definition: C = (C_phys ∩ S) ∪ K, where S is a declared scope and K a declared set of counterfactual edits, each with a stated meaning. Fidelity conditions run on C; world-kind is signature on C_phys; K enters non-vacuity only through its stated meaning. Non-vacuity says "a stated subset", not "declared". Add a contract-adequacy condition for objectivity claims (A8.5, F-A1.6): a contract that excludes a physically admitted edit separating two components distinguished by Γ is *protective*, and a narrowing after a failed criticism is flagged by the provenance record. Objectivity is then "faithful on C, and C not protective," two claims with two indices.

**G3. Representation, provenance, layers (A1.11, A6, A8.1–2, A8.7, E3.2, E3.4, F-A1.1).** Fix one transport orientation: E is held to D by t: D → E (π, τ, σ forward; λ back), and (R) uses the same orientation, t: c → Org(o). Stratify: primitive layer (selected, from the sensory field), simulation layer (constructed, over the primitive layer), with content identity at the primitive layer the primitive-layer notion, not Rep. Sel's non-triviality is stated over the *events* of the selection process (A6.1 wording; A1.11 superseded): the history is non-empty, the survival condition eliminates at least one candidate, t is produced by iterated variation from a population not containing it, and no event is a faithful transport to t, to H or to the survival condition — without the word "represents". Blindness = no itemised representation of the defect on the route, a scalar summary explicitly allowed; tested by scrambling both channels. Provenance has a precedence rule (constructed if a construction witness exists; else selected; else declared), and "declared" is a model-level status, not a physical history. Account carries no provenance condition (any modelled candidate can be assessed); (R), Deploy and (EK) add Sel ∨ Con explicitly. Account's arity is fixed everywhere as Account(E, p) with t, Γ existentially quantified. The survival criterion (a carrier persists iff its prediction of the world port matches under the encountered edit) is a stipulation and is labelled one.

**G4. Kinds and anchoring (A5, A7, A8.6, A8.17, F-A2.2).** (K) indexed to (ℓ, C). Two kinds of kind: forward (signature on C) and historical (predicates on h); "nothing over and above" and "no third case" withdrawn; dispositions as finer forward contracts, with the sentence that a disposition's trigger must be in C. Two grades of adequacy: *account at C* and *anchored* (account at C whose components are of one world-kind with their anchors on C_phys). The section "Why there is no anchoring condition" is rewritten to say what the anchoring condition is. Grievance 1's cause/correlation criterion aligned with the formal causal signature. λ must be a decomposition (the read-only-memory counterexample).

**G5. Account conditions (A8.3, A8.19–20, F-A1.5).** Five conjuncts, not "four conditions". Non-circular dependence removes a block of Γ by an edit on E (τ of an edit on D). Non-vacuity's last sentence moved to non-circular dependence. Bearing's parameters and (EK)'s free variables fixed; RetReal excludes empty execution families; the identification example corrected.

**G6. Derivations (A2, A6, A8, F-A2).** Derivation 1: subnetwork signature defined; (τ, σ) injective on C as a hypothesis; the corollary reclassified from theorem to the analysis-of-kinds *conjecture* of Part XV, "loses no case" deleted. Derivation 2: restated as equality of anchored relations and pulled-back answer profiles, with Γ included and account-equivalence defined; "identical" removed from its title. Derivation 3: stated for the organisation–transport pair under an explicit richness hypothesis on the population (closed under pointwise alteration of component relations off H), "admitted relation" and "differs at (a, b)" defined, and the consequence restricted to "no guarantee of fidelity off H" — not fallibility, not surprise. Derivation 4: retracted as a derivation; presented as an unpacking of the definition of surprise, relative to C_t, with out-of-contract surprise named as a limitation. Derivation 5: provenance attached to the whole question p; the contract-as-organisation built, not sketched; Attempt relative to a difficulty. Derivation 6: the consequence restricted to "no predicate left undefined apart from Θ and 𝒩"; adequacy stays a conjecture. Derivation 7: Part III's "during an assessment" clause reworded so any change ends the assessment. Derivation 8: restricted to bijections that preserve physical admission, scope records, obligations and 𝒩. Derivation 10: relabelled an illustrative scenario; its population assumption stated; "they are objects" replaced by the grain-relative claim; (EK) not claimed without the four constituents of a critical episode; Derivation 2 not cited for two components of one organisation. (EK) labelled an external success predicate, distinct from a system's claim to have created knowledge. A merit condition for questions stated under (P).

**G7. What the semantics may cite from the experiments (D8, F, files 16–17).** Nothing as a test of a definition. Experiment 1: among slot-carrying predictors in a grammar that contains a perfect tracker, occlusion scores the never-forgetting one highest, and a fair memoriser matches it on prediction. Experiment 2: per-record credit and a global scalar reach the same rule over one law-aware language; the scramble contrast is trivial; identity through crossings is underdetermined by occupancy for both. Experiment 3 (file 17 §10) is a test of credit granularity, and its name should not say "construction".

*(Remaining Atria items are ruled on as they land; the DeepSeek rerun's last empties (D2, D7, two of D4, one of B1, one of D6) likewise.)*




