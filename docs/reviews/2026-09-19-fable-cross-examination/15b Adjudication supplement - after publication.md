# 15b Adjudication supplement — sections added after publication

What this file is: the parts of files 15, 16, 17 and the project story that were written after the folder was published (commit c6c663d8). The published files are not edited; this supplement holds the additions verbatim, so the folder as a whole is current while the published observations stay as they were. Source of every section: the same session, the same witnesses.

## Part 1 — New sections of file 15 (the adjudication)

### D2 — Bugs in experiment 2's code (three complete samples after rerun)

Checked against the frozen code. Rows already ruled under D3–D6 (byte-identical vacuous; top-20 cap; base-rate-blind score; two-slot hardcoding; no held-out check; given-bound conditioning; tie-break; wall-stop bucket in phase 2) are not repeated.

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **The scramble (and every ablation transform) is re-applied each round**, so under M4 the corrupted objective is non-stationary and the later rounds see a fresh permutation. | **Valid.** | Confirmed: `construct` applies the transform after every collection. For M4 only round 1 mattered in the reported run, but the design should transform once. |
| 2 | M4 and M6(ii) permute or replace labels without reclassifying records as defects or non-defects, so the record sets no longer mean what their names say. | **Valid.** | The patched diagnostic (file 17 §8b) counts the reclassification; the frozen run did not. |
| 3 | **S0 ("best of G0") and the best slot-only architecture are selected on the evaluation half**, so S1 compares against a baseline chosen on the test set. | **Valid.** | Confirmed in `g0_best`. Same defect as experiment 1's B1.1. In this direction it favours the baseline, not C, so S1's gap is if anything understated — but a test-set selection is a test-set selection. |
| 4 | "A0's original slot rule is ignored by the rule predictor, so every A0 comparison is against the wrong baseline." | **Invalid.** | `RulePredictor` inherits `observe`, which calls A0's reconcile rule; only the kinematics are replaced. Checked. |
| 5 | The hand-built pair can double-fire (each rule loops over both orientations independently). | Valid as code; no effect. | The same-target and crossing conditions are mutually exclusive on any state, so it never fired twice here. Add a fired-set guard in any rerun. |
| 6 | `is_collision_step` counts wall stops as collisions. | Valid; no effect in phase 1 (no wall-stop events exist without the sticky law); phase 2 already conceded. | — |
| 7 | Phase 2's rule language computes next-states with reflecting kinematics while the world is sticky, so the language's `n`, `w` terms disagree with the world in exactly the steps the new rule must handle. | **Valid as a description; it was the design.** | The rule was supposed to build the sticky effect on top of reflecting slot kinematics, which is what "extend" meant. The witness is right that this makes the wall condition expressible only through `v_i != w_i`, and the wrong action was then a coin toss. |
| 8 | Condition terms for a new rule are computed from states without the holds already imposed by earlier rules. | Valid, minor. | Only bites with two or more rules; phase 2 is the only multi-rule case and is exploratory. |
| 9 | Defect records are generated from the predictor's own, possibly misbound, slot states. | Valid, by design. | The learner works from its own representation; that is the point. It must be said in the design. |
| 10 | The split by configuration is a deterministic parity split over a canonical ordering that breaks exchangeability of the two things. | Valid, moderate. | Stratify or shuffle with a recorded seed. |
| 11 | Duplicate rules are not prevented; M5's reverse-order control is a no-op for the constructor; `enumerate_changes` includes no-op velocity changes; baseline evaluations are not counted in B's total. | Valid, minor to cosmetic. | — |

### D7 — Can phase 2 be rescued with a law that extends the world? (three complete samples)

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **Under the frozen language no genuinely extending second law exists.** The world's laws are a total function on a finite state space; a consistent, behaviour-changing second law needs a new entity or state variable, hence a language extension; so phase 2 as conceived cannot test pure accumulation — it tests accumulation *under a declared extension*. | **Valid, and it ends phase 2 as designed.** | This is sharper than my "contradictory second law" concession: the problem is not the law I chose but the concept. Accumulation must be tested by transfer — carry A0 plus the phase-1 rule into a world that already contains the new entity, so the old rule stays valid and only the new one must be built — and the language extension must be declared as part of the design. |
| 2 | The minimal extension: a fixed absorbing obstacle at a cell, with the confound stated. | Accepted as the candidate for a rerun. | — |
| 3 | S7's collision-fidelity threshold and K4's are inconsistent (0.013 fails "within 0.01" and passes "drops by more than 0.05"). | Valid. | One threshold, one bucket, stated once. |
| 4 | Original phase 2 is not salvageable by reinterpretation. | **Accepted.** | Exploratory only, as already reclassified. |
| 5 | S0's selection half unspecified in the design; selected on evaluation in the code. | Valid. | Duplicate of D2.3. |
| 6 | The design's "building it takes two rounds" conflates the full law with the sensorily equivalent law. | Valid, minor. | — |

**What changes because of D2 and D7:** file 17 gains the transform-per-round and test-set-selection items; phase 2's concept is withdrawn, not just its instance, and any accumulation test becomes a transfer test under a declared language extension.

### Addendum from the remaining rerun samples (D4 ×2, D6 ×1)

Nothing new beyond the rulings above; the samples repeat the top-20 cap, the base-rate-blind score, the given-bound subsets, the in-sample ceiling and the reclassification point. One DeepSeek sample (B1 s2) never returned content at the model's cap and is recorded as such.

### F-A3 — Sufficiency (one sample)

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **The global-anchor exploit.** Build E with one component whose relation is Sol_D(a, b) for every (a, b) in C and whose anchor λ(k) is the whole target. (F1) becomes Sol_D = Sol_D, (F2) and (A) hold, non-circular dependence is witnessed by the disabling edit, non-vacuity holds, and "selected" is satisfiable by a singleton population. It is faithful on *every* contract, so contract refinement cannot separate it from the mechanism. | **Valid, fatal to sufficiency as stated — and sharper than A3's read-only-memory case.** | The ROM concession (λ must be a decomposition) is not enough: this candidate *is* a decomposition with one part. Needed: a properness condition (every anchor a proper subnetwork; E's components refine a cover of D's) *and* a resolution condition relative to Q (E's decomposition at least as fine as the dependencies the question asks about), *and* a ban on a component whose relation is definable as Sol_D or its projection. Added to G4. |
| 2 | "Why there is no anchoring condition" argues only against a *same-kind* condition; it never considers whether an anchor may be the whole target. There is a third case and it is the one that matters. | **Valid.** | Duplicate of 1 in effect; the section is rewritten under G4. |
| 3 | "Selected" is trivially satisfiable (singleton population, identity variation, H = {baseline}), so "non-declared transport" filters nothing; "constructed" likewise by stipulating an episode. | Valid. | Duplicate of A6.2/F-A6.1; the non-triviality conditions in G3. |

### F-A5 — Kinds as edit-signatures (one sample)

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **Etiological kinds enter through Org_ℓ, not through signatures.** If the physical module instantiates a lineage-history port, an original and a molecule-for-molecule forgery are different kinds, but the "separating change" is the identity edit, which separates any two things with different port values and so discriminates nothing; if it does not, the question "is this a Vermeer?" is unrepresentable. Kind-elimination is conditional on a choice the semantics declares primitive and does not argue for. | **Valid, serious.** | The A5 concession (two kinds of kind, forward and historical) is the right shape, but this shows where the historical kind lives: in the port values Θ supplies, and (K) counts port-value differences at the identity edit as separations, which trivialises it. (K) must exclude the identity edit from "separating changes", and historical kinds must be predicates on h, not port values. Added to G4. |
| 2 | **The framework individuates transports by history (selected versus declared, same π, τ, σ, λ) while denying that history individuates components.** The asymmetry is asserted, not defended. | **Valid, serious.** | New. Either defend it (transports are occurrences in a physical history; components are slots in an organisation) or admit etiological component-kinds alongside provenance. The first is the intended answer and must be written. |
| 3 | Part IX's **active route** is a third case from inside the document: two redundant mechanisms, one operative and one a backup with the same signature; (F1), (A) and Derivation 2 cannot tell the anchors apart, but Part IX's "actual occurrences" condition can. | **Valid.** | Duplicate of A7's decoy in mechanism, but it shows the document already contains the discriminating condition and does not use it in Account. G4: an actuality-of-route condition for the *anchored* grade. |
| 4 | "One kind at that contract" is a fact about the pair (Θ, C), not about the world; where the question fixes the contract and asks which mechanism produced the effect, there is no finer contract to retreat to. | **Valid.** | Index every kind-claim to (Θ, ℓ, C); etiological questions require Θ-supplied history or are declared unrepresentable. |
| 5 | Derivation 1's proof equivocates on (K); the Part 0 slogan is vacuous; dispositions expose that the work is done by contract choice. | Valid. | Duplicates of A2, A5, F-A2. |

### F-A6 — Genesis: the three provenances and question-finding (one sample)

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | Sel is satisfiable by every transport (singleton, identity operator, empty history); requiring H non-empty still admits H = {baseline}, which (R) already demands; only a *discrimination* requirement (at least one candidate fails the survival condition) fixes it. | **Valid, fatal as stated; the fix is in G3.** | Sharper than A6.2: non-empty H is not enough. G3 now requires a failing candidate and that the filtering be causally responsible for t's presence. |
| 2 | Every construction witness can be rewritten as a selection history, so Part XV's defeat condition is met trivially — until Sel is made non-trivial. | Valid, conditional on 1. | Falls with 1's fix. |
| 3 | The negative clause of Sel is circular through (R) and ill-typed; Con and Build are also circular with (R). | Valid. | Duplicates of A1.11, A6.5, F-A1.1. |
| 4 | **Part IV and Part XII give inequivalent definitions of Sel.** | **Valid, new.** | One definition, in Part IV, with Part XII's physical reading derived from it. |
| 5 | Contract provenance ρ_p has no witness, so "found a question" has no satisfaction condition; every re-parameterisation becomes a found question; a question is not its contract (targets, baselines and obligations are not representable as found); concept creation (new dimensions of variation) is outside question-finding as defined; creative reframing and goalpost-moving differ only by bookkeeping and timing. | **Valid, serious, and beyond what DeepSeek raised.** | Question-finding needs: provenance attached to the whole question tuple (already in G6), a witness for it, a merit condition under (P) (already in G6), and an honest statement that concept creation — a new port, a new dimension — is *not* representable in this semantics as it stands. That last is a real limit and goes in Part XV's attack list as an open point, not a solved one. |
| 6 | ≡_ℓ is undefined; C is both a declared index and a buildable content; meta-contract regress. | Valid. | Duplicates (A1, A8, F-A1). |

### F-A7 — The steelman for anchoring (one sample)

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | "Unevaluable" contradicts the document's own primitive: anchoring claims *are* evaluable (λ is transport data; Org_ℓ says what the target instantiates); only their kind-status under (K) is not. The section misstates the opponent. | **Valid.** | Replace "unevaluable" with "not evaluable by the changes in C", and then say why C should be the court of appeal — which, after A7.1, it is not: C_phys is. |
| 2 | Derivation 8 either transports λ (and says nothing about a swap that changes λ) or does not (and then licenses the pole/shadow recoding as a permitted bijection). | **Valid.** | State that λ is transported and that the pole/shadow map is not structure-preserving with respect to D. Added to G6. |
| 3 | Relocating how-possibly versus how-actually to Part IX is a category error: two models adopted through identical critical episodes can differ in anchoring, and nothing in Part IX inspects λ. | **Valid.** | The anchored grade of adequacy (G4) is where this belongs; Part IX is not. |
| 4 | A stated exclusion can still be protective; stating it does not make it legitimate. | Valid. | Duplicate of A8.5 and F-A1.6; the contract-adequacy condition in G2. |
| 5 | What the document loses by dropping an anchoring condition: how-possibly/how-actually at a fixed contract; direction of explanation when interventions are unavailable; component-level model–world correspondence as a semantic fact; mechanism identification as an achievement; use of its own primitive. | **Accepted as the statement of the cost.** | All five are recovered by the two-grade structure in G4, or else the loss is stated as a limit. |

**What changes because of F-A3, F-A5, F-A6, F-A7:** G3 gains the discrimination requirement on Sel and a single definition of Sel; G4 gains the properness and resolution conditions on anchors, the exclusion of the identity edit from separating changes, historical kinds as predicates on h rather than port values, the defended asymmetry between transports and components, and an actuality-of-route condition for the anchored grade; G6 gains the λ clause for Derivation 8; Part XV gains "concept creation is not representable" as an open attack point.

### F-A4 — Necessity: what the semantics cannot represent (one sample)

Most rows duplicate A4 (eliminative anchor ill-typed; no admissible Γ; Derivation 2 collapses the eliminative account; contract provenance unchecked). New and ruled:

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | Eliminative explanations by *impossibility* are unrepresentable either way: if the introducing edit must be physically admitted, no contract contains it; if impossible edits are admitted, "physically admitted" means nothing. | **Valid.** | This is the reason G2 has the declared counterfactual set K with stated meaning: K is exactly the class of well-defined-but-impossible edits, and Grievance 4's objectivity claim is restricted to C_phys ∩ S. The class must be named as such in Part VII. |
| 2 | **Symmetry explanation is absent**, and the entailment from invariance to outcome-independence is a relation *among* E's components that neither (F1) (per component) nor (F2) (assembly) constrains; anchoring it in D imports the explanandum. | **Valid, serious; a live instance of attack (B).** | New. Part VII needs a symmetry case, or Part XV lists symmetry explanation as an open attack point. Listed as open in G7. |
| 3 | Statistical / selection-artefact explanation is untreated; the artefact component is either anchored as genuine structure (if D is the data) or has no ports (if D is the population). | **Valid.** | New. A two-target treatment (data organisation and population organisation, one transport each) is required; not designed. Open point. |
| 4 | Question-changing explanation is forbidden by (A) (the query is held fixed), so a reframe's force — that p was the wrong question — is never assessed for fit, only for novelty. | **Valid.** | Duplicate in substance of F-A6.5; the semantics assesses reframes for construction and novelty, not adequacy, and must say so. |
| 5 | "Physically admitted" is undefined for the flagship mathematical example (the odd-order determinant), so the strongest worked example does not fall under the quantifier of attack (B). | **Valid.** | An admission relation for mathematical organisations must be defined (via a realisation of the proof object, or separately) before that example counts. |

### F-B2 — The pre-freeze changes (one sample)

The Atria audit reaches the same verdicts as the two DeepSeek audits change by change (F1–F10 duplicate B2 and file 16 §1, §13), and adds: change 15 (the lookup allowed to predict from the first field) is the strongest evidence the process was not purely self-serving, since it strengthened the rival (accepted, and noted in file 16 §1); the j gene and the rebind exclusion were tuned against the same deficit (duplicate of B2's third sample); H_neutral is declared neutral by construction (duplicate of B1.1/B3.1 — and file 16 §16(a) shows the mechanism); M3 is vacuous on swap (duplicate of B3.4); round labels are missing so blindness cannot be checked (valid — the process rule in G: a hash per change); the arithmetic (change counts, sequence counts, 208) verified independently (noted).

### F-B4 — Is experiment 1's headline trivial? (one sample)

Same verdict as DeepSeek's B4 ("near-tautological with respect to the operationalisation"), with three additions:

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **The selecting factor is a property of the sensor, not of the world's history**: occlusion is a sensor edit, converted into selection by the world-facing fitness target; "history" is the wrong word. | **Valid, and better than my wording.** | File 16 §17's headline now reads: the sensory interface's occlusions, scored against world state, selected persistence among slot-carrying architectures. |
| 2 | §7.1 misattributes its own cause: H_passive (two things, identity changes only) already selects j = no, so the variable is the *source of jumps* (admitted displacement versus crossing-induced misbinding), which correlates with thing count here but is not it. The document's own data refute its stated explanation. | **Valid, and checkable from the frozen results.** | The corrected statement is more informative; added to file 16 as §18. A discriminating rerun (one thing with occlusion; two things barred from sharing a cell) belongs to experiment 3's world family. |
| 3 | Two unrelated quantities both round to 0.801 (H_full top fitness 0.8009; M3 all-pairs 0.80117); the witness recomputed every weighted average and split count and found them consistent. | Cosmetic; the verification is noted. | One more decimal place. |

### F-B5, F-C1, F-C2, F-C4 — the second witness on the experiment items (one sample each)

All four reach the rulings already recorded (M3 conditions on what it tests and is a persistence test; the scramble contrast is trivial and the B half unfalsifiable; "no aggregate fitness" is false; the world was fitted to the language; construction was partial by design). Additions, ruled:

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **The forgetting counter is never reset when a hidden slot re-emerges in place**, so the implemented rule is "cumulative unconfirmed steps since the last re-bind", not "consecutive unconfirmed steps" as the design says. | **Partly valid; no effect on the result.** | The witness's exact scenario (confirmed with count already above τ) cannot occur, because the drop runs every step before that. But the semantics is cumulative-since-snap, not consecutive, which deviates from the design. Patched in a diagnostic (file 16 §19): every score moves by at most 0.0035 and the ordering on H_full is unchanged. |
| 2 | **The scramble cannot touch the condition-induction stage** (conditions are scored on defect/non-defect membership, which the permutation preserves), so M4 probes only the action-selection half of the route. | **Valid, and it explains the seed-dependence.** | With conditions untouched, the permutation degrades only the action net, and only where states do not recur. Added to file 17 §8b's explanation. |
| 3 | The C-versus-B contrast is a 2 × 2 design with two cells missing (a selection process over itemised records; a construction process over a scalar), so nothing can be attributed to the defect representation; no double dissociation. | Valid. | Duplicate of D3.5 / E4; the four-cell design in file 17 §10. |
| 4 | **The language anticipated phase 2 as well**: the removal of constants was justified by the fact that the *next* law was expressible without them — forward tailoring, one experiment ahead. | **Valid, minor and telling.** | Design §4 says so. A blinded law generator (file 17 §10) is the only fix. |
| 5 | "Guaranteed to succeed" overstates the tailoring charge; the accurate charge is "biased by design". | Accepted as wording. | — |
| 6 | The kind-signature test excludes the one case (crossings) that distinguishes a component from a patch. | Valid. | Duplicate of D5.4 / C5.2. |

### F-C3, F-C5, F-D3, F-D5, F-D6 — the second witness on the construction experiment (one sample each)

All five reach the standing rulings (growth withdrawn; the scramble's B half tautological; "no aggregate fitness" false; S3 narrowed; phase 2 a breach; M3 conditions on a post-treatment variable; the ceiling in-sample; unit-mismatched cost comparison). Additions, ruled:

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **Crossings are not unseen; they are recorded as correct.** At a crossing the pass-through prediction matches the field, so the record lands in N, the crossing condition is true on it and scores −1. C is not blind to crossings; it is trained to treat pass-through as correct and penalised for the condition that would handle them. | **Valid, and the sharpest statement of Finding-3 yet.** | Replaces "invisible to sensation" and my "the error signal cannot select it" (file 17 §12): the error signal selects *against* it. Moving crossing records from N to V (a velocity-level defect) would flip the sign — which is the concrete form of the experiment 3 test. |
| 2 | The "all crossings are invisible" claim is generalised from the adjacent head-on case to all 230 pairs without the covering lemma (multiset invariance of identical things under elastic collision and reflecting walls). | Valid. | The lemma is true and easy; it is not in either file. State it. |
| 3 | The "needed" margin rests on "roughly eight predictions" with no variance model. | **Invalid on the number; valid on the absence of a variance model.** | Counted: the evaluation half has 938 sequences and 1,396 collision-step predictions, so the 0.087 gap is about 121 predictions, not 8 (the witness assumed one sequence per configuration). But there is one split, one run of C, and no interval anywhere; S2's "within 0.01" and S5's "within 0.05" were never checked against a noise floor. Bootstrap over configurations in experiment 3. |
| 4 | The hand-built reference (0.906) sits below the ceiling (0.923) with no explanation, and every threshold is calibrated against those two numbers. | **Valid.** | The ceiling is the in-sample majority continuation and can exceed any rule that generalises; the gap should have been explained and the ceiling labelled. |
| 5 | No bridge from tokens to types: six seeds of B vary the random number generator, not the regime; one implementation per class licenses no type-level claim. | Valid. | Duplicate of D3.5 / E4, sharpened: the four-cell design must vary the *algorithm* within each regime (a tree learner and a Bayesian updater on records; an evolution strategy and a gradient surrogate on scalars). Added to file 17 §10. |
| 6 | The vacuity argument for B's junk atoms used the world's distinctness condition; the rules read slot terms, and A0's slots can coincide. The claim survives by data (identical predictions), not by the stated reason. | Valid, minor. | Corrected in file 17. |
| 7 | F3 was never an outcome; it was an amendment with no failure condition, and "a finding either way" misdescribes a directional entailment. | Valid. | Duplicate of C5.3 / D5.1. |
| 8 | M3's finer contract is the world's implementation ontology, which no agent in the experiment could access. | Valid. | Duplicate of D5.2. |
| 9 | The record format — the object of the central claim — is not pre-registered in the design. | Valid. | It is in the code only; a design must state what a "defect record" contains. |
| 10 | Self-scoring is generous in both directions (⚠️ where ❌ was earned; "K4 by its letter no"). | Valid. | Conceded under D6/E1. |

### F-A8, F-B1, F-B3, F-D8 — the items recovered by streaming (one sample each; the connection cut at 300 seconds had killed them, and streaming kept it open for 9–10 minutes)

Rows that duplicate A8, B1, B3, D8 and the file 16 §16 diagnostics are not repeated. Additions, ruled:

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | (A8) "Its truth is fixed at that index" confuses the identity of a claim with the fixity of its truth value; (EK) never says at which world-state Account is evaluated; surprise entails failure of (R) and hence loss of Deploy, which the text never remarks. | **Valid.** | Three precise gaps in Parts VIII, XI and IV; added to G5/G6. The Deploy point matters: a surprised system has, by the semantics' own definitions, stopped representing on the contract where it was surprised. |
| 2 | (A8) The sufficiency claim is stated in three non-equivalent ways, and Part XV's test adds a condition ("non-declared transport") that (E) does not contain. | **Valid.** | Duplicate of A8.2 from the other side; one statement, in G3. |
| 3 | (A8) NonCircular's formal witness does not detect circularity: removing the whole block Γ changes the profile for any account, circular or not. | **Valid, serious.** | New. The witness must be a *proper* sub-block removal that preserves the answer's boundary conditions and still changes the profile — or the condition is renamed to what it tests (dependence, not non-circularity). Added to G5. |
| 4 | (B1) **Table 4 of file 12 labels the two-slot τ = 0 architecture as "selected on H_passive, H_kinematic", but H_kinematic selected a three-slot architecture**; the claim about H_kinematic's winner is asserted, not shown. | **Valid; no effect on the numbers.** | Checked in the raw results: the three-slot winner's row is 0.710 overall, 624 unbound, 0.018 on occlusion — the same figures as the row shown. File 16 gains the correction (§20). |
| 5 | (B1) M4 (failure structure by change type) is declared in the design, promised in the protocol, and never reported; §7.1's mechanism story needs it. | **Valid.** | The by-type figures exist in the raw results (per architecture, per history) and were never tabulated. A display omission, not a data omission; recorded. |
| 6 | (B1) The full τ × history M2 matrix — how a never-forgetting tracker trained without occlusion does on occlusion — was computed and not shown; without it "selected only when the history contains occlusion" is partly trivial. | **Valid.** | Same: in the raw results, not in the tables. |
| 7 | (B1) H_neutral is not neutral: it selects strictly on radius and on the jump gene; the purest cell-tracker (rebind) is strictly worse there. | Valid. | Duplicate of B2/B3 and file 16 §3, §16(a), with the radius observation now explained. |
| 8 | (B3) The counter is a cumulative lifetime budget, which inflates τ = ∞'s margin. | Partly valid; checked. | Duplicate of F-B5.1: patched, nothing moved (file 16 §19). |
| 9 | (B3) `best_of` in the controls keeps the *first* maximum under strict `>`, so on H_neutral, where many architectures tie exactly, the named "best" per persistence value is the earliest in enumeration order. | **Valid, minor.** | The main table lists every tied architecture; the controls' one-name-per-value display did not. |
| 10 | (B3) `thing_signature` hand-rolls the observe step instead of calling it, and the rebind rule's M3 rows are meaningless because rebinding discards the binding. | Valid, minor. | Both true; rebind's M3 rows were never used for a claim. |
| 11 | (D8) "The M3 crossing numbers do not reconcile: hand-built has 230 − 13 = 217 bound pairs, not 221." | **Invalid.** | The witness read the no-collision column's unbound count (13) into the crossing column; the crossing row says 9, and 230 − 9 = 221 as printed. |
| 12 | (D8) "The residual-defect arithmetic does not close: 2,830 − 820 ≠ 1,266." | **Invalid as arithmetic; valid as a reporting gap.** | Round 2's records are re-collected under the new rule, whose effect on later trajectories changes which steps are defects; the counts are not meant to subtract. File 14 should have said so and printed the ledger. |
| 13 | (D8) S3 is the only substantially faithful operationalisation and it substitutes a frequency for relation equality; its pass is earned on the coarse contract where Derivation 2 makes it near-vacuous; thresholds are indices whose provenance is unrecorded. | Valid. | Consistent with D8/D8b; the threshold-provenance point is new and goes in the process rules. |
| 14 | (D8) The results file inverts file 10's account of provenance (history versus output). | Valid. | Duplicate of C1/D3. |

### F-D1, F-D4, F-D7 — the last of the second witness (one sample each; D2 returned empty even under streaming and is recorded as lost)

Rows duplicating the rulings above (phase 2 breach; S6 and S7 ❌; byte-identical tautology; "no fitness number"; S0 selected on the test half; base-rate-blind score; two-slot hardcoding; change 4 a moved goalpost; co-designed grammar) are not repeated. Additions, ruled:

| # | Finding | Verdict | Why |
|---|---|---|---|
| 1 | **No correct wall rule exists in the language**: the hand-built reference is the handicapped `stop_i` (fires once per step, so cannot stop two things hitting walls at once), and `stop_both` zeroes a thing that hit nothing. "Right condition, wrong action" understated a language limit; phase 2 was confounded twice. | **Valid.** | The design's own §6 expressibility check was skipped for phase 2's law (the hand-built wall rule reached 0.808, not the ceiling, and nobody asked why). Added to file 17 §11. |
| 2 | The remedies file 14 proposed for phase 2 (a third thing; a one-way gate) are not expressible in the frozen language either: a third thing is an architecture change, a gate needs the constants that change 3 removed. | **Valid.** | The witness then supplies a candidate that is expressible and consistent with every existing law — a "no-draft" rule, `IF n_i == c_j THEN reverse_i + move`, whose trigger is disjoint from every event class an existing law governs and which is visible in occupancy. Recorded in file 17 §10 as the candidate for an accumulation-by-transfer rerun, with its gate checks. Not run. |
| 3 | Under pre-computed-`n` move semantics the achievable next fields per step are four patterns, so the velocity operation is never identifiable in one step and every action choice is a tie; the rerun needs post-rule-velocity move semantics or a two-step lookahead, decided before the law is chosen. | **Valid, and it explains phase 2's coin-toss action.** | Same root as D6.9 and D4.2 (one-step lookahead), now with the mechanism. |
| 4 | "The reported sequence counts (1,889) do not match the enumeration (135 × 15 = 2,025); ~136 sequences may be silently dropped." | **Invalid on the count; the check was worth asking for.** | Run: 135 configurations, 13 to 15 admissible changes each (the change set depends on the configuration), 1,889 sequences, none dropped by the None filter. The design should state the per-configuration rule. |
| 5 | S3's sentence "0.974 and 0.973 … from 0.000 for A0" cites one baseline for two columns; A0 is 0.946 on the no-collision column and 0.000 only on the collision columns. | Valid, minor. | Sloppy sentence; per-column baselines are in file 17 §8c. |
| 6 | The scramble permutes only the outcome column, so states and defect-set membership are preserved and the induced condition is logically unchanged. | Valid. | Duplicate of F-C1/C2's condition-induction point, confirmed by the patched diagnostic. |
| 7 | The 0.013 collision-fidelity drop was measured back on the original world, an unregistered measurement used as a defence; K4's "by its letter no" took the favourable reading. | Valid. | Phase 2 is exploratory; nothing in it is cited. |
| 8 | Half of the action space was never exercised; the phase-1 action choice was itself a silent tie between `swap_next_v` and `stop_both` at the same net, and phase 2's failure is the same bug surfacing later. | Valid. | Checked in D2/D6 already for phase 2; the phase-1 tie is new and is in the rounds log (net 952, 27 broken for both). The tie-break rule must be pre-registered and, in a rerun, resolved by held-out validation. |
| 9 | B's evaluation count cannot be reconstructed from the design; the phase-2 rule listing is incomplete ("and then a patch"). | Valid, reporting. | Both belong in the ledger file 17 §9 now asks for. |
| 10 | "Needed" is partly definitional (no G0 architecture can *represent* a pairwise law); the empirical content is the margin over the memoriser, which is below the design's own 0.1. | Valid. | Duplicate of C3/D1.5. |

**Closing count for the second witness:** 25 of 26 items answered with content (one, D2, returned empty under streaming); 7 of the 8 items the 300-second cut had killed were recovered by streaming, in 9–10 minutes each.






## Part 2 — Additions to file 15 §0 (failure modes of the cross-examination)

14. **Streaming recovers what the cut kills.** With `stream: true` the connection stays open; the eight items that had failed four times each came back in 9–10 minutes, all but one (D2, which returned no visible content — the reasoning consumed the cap). The harness now has a streaming mode; it should have been the default from the first Atria launch.

13. **Atria attempts are cut at 300 seconds, and I misread the queue as slowness.** Three items (A8, B1, B3) failed four times each with the connection closed by the remote end; every failed attempt lasted 306 seconds to within a tenth of a second, so a single attempt is cut at about five minutes, at the provider or at the gateway. Every successful Atria attempt finished inside that window (two to five minutes). The "thirty minutes per reply" I reported to the user was the wall-clock of a four-worker queue in which each failing item held a worker for 21 minutes; it was wrong, and the user's note that the limit is 60 requests per minute exposed it. Fix: launch everything at once, and stream so long replies survive the cut.


## Part 3 — Amended paragraphs of file 15 §G (the consolidated revision list)

The following paragraphs replace their published versions.

**G3. Representation, provenance, layers (A1.11, A6, A8.1–2, A8.7, E3.2, E3.4, F-A1.1).** Fix one transport orientation: E is held to D by t: D → E (π, τ, σ forward; λ back), and (R) uses the same orientation, t: c → Org(o). Stratify: primitive layer (selected, from the sensory field), simulation layer (constructed, over the primitive layer), with content identity at the primitive layer the primitive-layer notion, not Rep. Sel's non-triviality is stated over the *events* of the selection process (A6.1 wording; A1.11 superseded): the history is non-empty and contains a pair at which fidelity is non-trivial, at least one candidate *fails* the survival condition (selection discriminates), the variation operator was physically applied, the filtering is causally responsible for t's presence, and no event is a faithful transport to t, to H or to the survival condition — without the word "represents". One definition of Sel (Part IV), with Part XII's physical reading derived from it (F-A6.4). Blindness = no itemised representation of the defect on the route, a scalar summary explicitly allowed; tested by scrambling both channels. Provenance has a precedence rule (constructed if a construction witness exists; else selected; else declared), and "declared" is a model-level status, not a physical history. Account carries no provenance condition (any modelled candidate can be assessed); (R), Deploy and (EK) add Sel ∨ Con explicitly. Account's arity is fixed everywhere as Account(E, p) with t, Γ existentially quantified. The survival criterion (a carrier persists iff its prediction of the world port matches under the encountered edit) is a stipulation and is labelled one.

**G4. Kinds and anchoring (A5, A7, A8.6, A8.17, F-A2.2).** (K) indexed to (ℓ, C). Two kinds of kind: forward (signature on C) and historical (predicates on h); "nothing over and above" and "no third case" withdrawn; dispositions as finer forward contracts, with the sentence that a disposition's trigger must be in C. Two grades of adequacy: *account at C* and *anchored* (account at C whose components are of one world-kind with their anchors on C_phys). The section "Why there is no anchoring condition" is rewritten to say what the anchoring condition is. Grievance 1's cause/correlation criterion aligned with the formal causal signature. λ must be a decomposition (the read-only-memory counterexample), *proper* (no anchor is the whole target; E's components refine a cover of D's), at a resolution at least as fine as the dependencies Q asks about, and no component's relation may be definable as Sol_D or its projection (the global-anchor exploit, F-A3.1). (K) excludes the identity edit from the separating changes; historical kinds are predicates on h, not port values (F-A5.1). The asymmetry — transports individuated by history, components by signature — is stated and defended (F-A5.2). The anchored grade adds an actuality-of-route condition (F-A5.3, Part IX's active route).

**G5. Account conditions (A8.3, A8.19–20, F-A1.5, F-A8.3).** Five conjuncts, not "four conditions". Non-circular dependence's witness must be a proper sub-block removal that preserves the boundary conditions and changes the profile, or the condition is renamed to what it tests. State at which world-state (EK) evaluates Account, and note that surprise on C entails loss of (R) and Deploy on C. Non-circular dependence removes a block of Γ by an edit on E (τ of an edit on D). Non-vacuity's last sentence moved to non-circular dependence. Bearing's parameters and (EK)'s free variables fixed; RetReal excludes empty execution families; the identification example corrected.

**G6. Derivations (A2, A6, A8, F-A2).** Derivation 1: subnetwork signature defined; (τ, σ) injective on C as a hypothesis; the corollary reclassified from theorem to the analysis-of-kinds *conjecture* of Part XV, "loses no case" deleted. Derivation 2: restated as equality of anchored relations and pulled-back answer profiles, with Γ included and account-equivalence defined; "identical" removed from its title. Derivation 3: stated for the organisation–transport pair under an explicit richness hypothesis on the population (closed under pointwise alteration of component relations off H), "admitted relation" and "differs at (a, b)" defined, and the consequence restricted to "no guarantee of fidelity off H" — not fallibility, not surprise. Derivation 4: retracted as a derivation; presented as an unpacking of the definition of surprise, relative to C_t, with out-of-contract surprise named as a limitation. Derivation 5: provenance attached to the whole question p; the contract-as-organisation built, not sketched; Attempt relative to a difficulty. Derivation 6: the consequence restricted to "no predicate left undefined apart from Θ and 𝒩"; adequacy stays a conjecture. Derivation 7: Part III's "during an assessment" clause reworded so any change ends the assessment. Derivation 8: restricted to bijections that preserve physical admission, scope records, obligations and 𝒩, with λ among the transported data, so that the pole/shadow recoding is excluded as not structure-preserving with respect to D (F-A7.2). Derivation 10: relabelled an illustrative scenario; its population assumption stated; "they are objects" replaced by the grain-relative claim; (EK) not claimed without the four constituents of a critical episode; Derivation 2 not cited for two components of one organisation. (EK) labelled an external success predicate, distinct from a system's claim to have created knowledge. A merit condition for questions stated under (P).

**G7. What the semantics may cite from the experiments (D8, F, files 16–17).** Nothing as a test of a definition. Experiment 1: among slot-carrying predictors in a grammar that contains a perfect tracker, occlusion scores the never-forgetting one highest, and a fair memoriser matches it on prediction. Experiment 2: per-record credit and a global scalar reach the same rule over one law-aware language; the scramble contrast is trivial; identity through crossings is underdetermined by occupancy for both. Experiment 3 (file 17 §10) is a test of credit granularity, and its name should not say "construction". Open attack points for Part XV, from the second witness: symmetry explanation (an entailment among E's components that (F1)/(F2) do not constrain), selection-artefact explanation (two targets), concept creation (a new dimension of variation), and an admission relation for mathematical organisations.


## Part 4 — New sections of file 16 (experiment 1 errata)

## 18. Two corrections of wording from the second witness (file 15 §F-B4)

The selecting factor was the sensor, not history: occlusion is a sensor edit, turned into selection by the world-facing fitness target. The headline in §17 should be read with "the sensory interface's occlusions, scored against world state" in place of "the history with occlusion". And §7.1 of file 12 misattributed its own cause: H_passive (two things, identity changes only, no displacement) already selects "a jump does not keep velocity", so the variable is the source of jumps — admitted displacement versus crossing-induced misbinding — which correlates with thing count in this design but is not thing count. The corrected statement is checkable from the frozen results and is more informative than the one it replaces.

## 19. The forgetting counter is cumulative, not consecutive (file 15 §F-B5)

A witness read the code and found that the unconfirmed-step counter is reset only when a slot is re-bound by snapping, never when a hidden slot re-emerges in place and is confirmed. So the implemented rule drops a slot when its unconfirmed steps *since the last snap* exceed τ, not after τ consecutive unconfirmed steps as the design says. `exp1/diagnostic_count_reset.py` patches the reset in and re-scores the persistence family on the evaluation half of H_full:

| Architecture (two slots, radius 5) | Frozen | Counter reset on confirmation |
|---|---|---|
| τ = 0 | 0.7434 | 0.7434 |
| τ = 2 | 0.7624 | 0.7659 |
| τ = 5 | 0.7982 | 0.7980 |
| τ = ∞ | 0.8009 | 0.8009 |

No score moves by more than 0.0035 and the ordering is unchanged. The design's description of the rule is corrected; the result is not affected.

## 20. Three reporting defects in file 12 found by the second witness (file 15 §F-B1)

The thing-signature table in file 12 §4 labels its two-slot τ = 0 row as "selected on H_passive, H_kinematic"; H_kinematic in fact selected a three-slot architecture. The three-slot winner's own row, from the raw results, is 0.710 overall with 624 unbound pairs and 0.018 on occlusion — the same figures — so nothing turns on it, but the label was wrong. M4 (which change types fail, per architecture) was declared in the design and never tabulated, though the numbers are in the raw results. The full persistence × history matrix on the full contract, which the "selected only when the history contains occlusion" claim needs, was likewise computed and not shown. All three are display omissions; the raw file 12c contains the data.


## Part 5 — Amended lines of file 17 (experiment 2 errata)

Lines added or changed since publication, as a unified-diff excerpt (a leading `+` marks the current text):

```
+Three conclusions. **The accounting bug was real and the fix works**: M6(ii) now passes. **C is not sensitive to generic corruption**: the placebo leaves the rule untouched. **The scramble effect is seed-dependent**: two of five permutations produced no degradation at all, because many records share a state — and, as the second witness pointed out, because the permutation preserves which records are defects, so condition induction is untouched and only the action scoring can be disturbed; so permuting outcomes among records leaves the state→outcome mapping largely intact for those states. The original result (0.906 → 0.355 on one seed) was partly luck. S4 as pre-registered (a drop of at least 0.1) holds in 3 of 5 permutations. A scramble that actually destroys the mapping must permute outcomes *within* groups of identical states or replace each outcome with a different wrong field — which is what the witnesses proposed and what experiment 3 will use.
+Three conclusions. **B's rule tracks things exactly as C's does**, including the zero on crossings: F3 is a property of the occupancy-only sensory contract shared by both processes, not of construction (seed 3's extra atom `c_i != v_j` costs it two pairs — "vacuous" was argued from the world's distinctness of positions, but the rules read slot terms and A0's slots can coincide; the atoms are inert by the data, not by that argument). **The given-bound conditioning hid nothing material**: the unconditional same-target rate for A0 + C is 0.935, still above the 0.9 threshold and against 0.000 for A0, but the unconditional figure is the one to report. **The bucket definition made no difference here**: classifying by the first post-change collision gives the identical counts (167 / 541 / 230), so no crossing failure was really an earlier same-target failure; the code concern stands for other worlds.
+The frozen design (file 13, §11 step 5) says "Phase 2 only if S1–S6 hold." S6 did not hold: M6(ii) failed. I recorded S6 as "⚠️ content, not carrier" and ran phase 2 anyway. That is a breach of the pre-registered stopping rule, and it means phase 2 is out of contract whatever its numbers. Phase 2 is reclassified as **exploratory**, and its S7 line is reclassified: "wall rule built ✓ (right condition, wrong action)" becomes **❌** — a rule with the wrong action is not the wall rule. Worse (file 15 §F-D4): no correct wall rule exists in the language at all — `stop_i` fires once per step and cannot stop two things hitting walls together, and `stop_both` stops a thing that hit nothing — so the hand-built reference (0.808) was itself compromised and the §6 expressibility check, which would have shown this, was never run for phase 2's law. The patched accounting in §8b makes M6(ii) pass, but a fix applied after the run does not license a phase that the frozen rule forbade.
+- "The invisible law" becomes **"identity is underdetermined by occupancy."** The rule language can express the crossing condition (`n_i == c_j and n_j == c_i`); what cannot select it is the defect-driven criterion — and, as the second witness put it more exactly, the criterion selects *against* it: at a crossing the pass-through prediction matches the field, the record is filed as a non-defect, and the crossing condition scores −1 on it. C is trained to treat pass-through as correct. The limit is in the error signal, not in what the language can say.
+8. Every ablation transform (scramble, no-content, reorder) is re-applied in each round, so a multi-round run under M4 sees a fresh permutation each time. Transform once.
+9. The best-of-G0 baseline and the best slot-only architecture were selected on the evaluation half, i.e. on the test set. It favours the baseline here, but it is a test-set selection.
+10. The remedies file 14 proposed for phase 2 (a third thing, a one-way gate) are not expressible in the frozen language either; the second witness's candidate is: a "no-draft" law — after kinematics and the collision law, if one thing's next cell is the other's current cell (a trailer about to move into the leader's cell) the trailer's velocity is reversed — with hand-built rule `IF n_i == c_j THEN reverse_i + move`, one atom, one action, one firing per step, trigger disjoint from every event an existing law governs, visible in occupancy. Its gate checks (expressibility against the ceiling on draft steps; hand-built rule on all buckets including the original world) come before any construction run. Move semantics (post-rule velocity, or a two-step lookahead) must be fixed before the law is chosen, because under pre-computed next-cells every action is a tie. Not run.
+11. Phase 2's concept, not only its instance, fails: under a frozen language no consistent behaviour-changing second law exists without a new entity or state variable, so accumulation can only be tested as transfer into a world that already contains the new entity, under a declared language extension (file 15 §D7).
+3. **Processes — four cells, one factor, two algorithms per cell.** Within each regime vary the algorithm (for records: a version-space learner and a tree or Bayesian learner; for scalars: an evolution strategy and a gradient surrogate), so that a sensitivity profile can be shown to track the regime and not the implementation. Common candidate representation and proposal distribution; the credit signal is the only factor: (i) per-record credit with local component updates; (ii) per-record credit aggregated before selection; (iii) a simple scalar (net defect count or accuracy); (iv) a **sufficient-statistic scalar** (likelihood of the records under the candidate). Matched on candidate evaluations, record accesses, proposals and wall clock; all four reported.
```

## Part 6 — Project story, log entries 32–35

32. **You asked whether I was writing lessons. I was not.** The repository
    keeps lessons by subject (docs/lessons/: method, semantics, expression,
    operations), each naming its evidence and scope. Written now under
    2026-09-19 headings, with the whole review thread (files 10-17, the
    diagnostics, the harness and every public witness reply, no hidden
    reasoning, no keys) placed in docs/reviews/2026-09-19-fable-cross-
    examination/, a ledger receipt, and a short status note. Committed to the
    working branch and opened as draft pull request #1, not pushed to main.
33. **More of the second witness landed (file 15, section F).** Two sharp new
    holes: a one-part "explanation" whose only part is the target's own
    answer table passes every test on every contract (so "the anchor must be
    a decomposition" is not enough; it must be a proper one, fine enough for
    the question); and the theory tells transports apart by their history
    while refusing to tell components apart by theirs, without saying why.
    Also: "selected" was satisfiable by every transport until selection is
    required to have eliminated something; and inventing a new dimension of
    variation is not representable as question-finding at all - an open
    limit, now listed as one. The experiment items from this witness were
    still arriving. (I said "half an hour each" here and to you; that was
    wrong - see entry 34.)

34. **You asked whether Atria's 60 requests per minute would help, and it
    exposed a mistake of mine.** I had been running four Atria calls at a time
    and reporting "half an hour per reply". The receipts say otherwise: every
    successful reply took two to five minutes, and the three that failed were
    each cut off after exactly 306 seconds, four times over, holding a worker
    for 21 minutes each. The slowness was my queue, not the model. Launched the
    remaining items all at once. Corrected in file 15, section 0, and in the
    repository lesson. Wrote two witness profiles (files 18 and 19): where
    each model was strong and weak, under what conditions, with the evidence.

35. **The second witness is complete: 25 of 26 items.** Streaming rescued
    seven of the eight items the five-minute cut had killed; one (the
    experiment 2 code review) came back empty and is recorded as lost. Last
    additions: no correct wall rule exists in the rule language at all, so
    phase 2's "hand-built reference" was itself compromised; the remedies I
    had proposed for phase 2 are not expressible either, and the witness
    supplied one that is (a "no-draft" rule), now the candidate for a rerun;
    and two of its numeric claims were wrong (checked). The profile in file
    19 is corrected accordingly.


