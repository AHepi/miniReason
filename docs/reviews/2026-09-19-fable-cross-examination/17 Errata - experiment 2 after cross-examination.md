# Errata: experiment 2 (files 13, 14) after adversarial cross-examination

**Why a separate file.** Files 13 and 14 were frozen and fingerprinted; they are not edited. Corrections go here. Every item was raised by an external witness (file 15, sections C1–C3) and checked by me against the frozen design, code and raw results. Nothing here is a new experiment.

## 1. The scramble test does not distinguish provenances

File 13 §7 (M4) and file 14 §5 call the scramble "the test that distinguishes the provenances," and file 14 adds that this "is not a claim about the code's data flow." Withdrawn. C was defined to read the defect records and B was defined not to; scrambling the records can only affect C, and B's byte-identical output is a consequence of its definition. M4 is a **content-dependence check on one program**: it shows C's output depends on the state–outcome pairing rather than on counts (the condition induction, which reads only states, survived the scramble; the action solving, which reads outcomes, broke). That is worth knowing about C. It says nothing about construction versus selection as kinds of process.

## 2. "C never computes an aggregate fitness" is false

File 13 §5. C ranks conditions by (defects covered − non-defects covered) and actions by (defects fixed − non-defects broken); both are sums over records used to select the best. The true contrast between C and B is the **granularity of the error signal** — per-record labels versus one scalar per candidate — and its route. A scalar fitness is itself a coarse representation of what went wrong, so file 13 §1's "nothing inside the process represents what went wrong" is false of B as well. This reaches file 10 (see file 15, A6.3 and C1.4).

## 3. "The object grammar grew" is withdrawn

Every rule C can append was a member of the fixed meta-grammar of 50,176 before the run. Indexed to the program, nothing grew. Indexed to G0 — the 208 slot-independent architectures — "grew" is true only because G0 was defined to have no pairwise rules, and B "grows" it in exactly the same way. The word "needed" in S1 and "distinct from selection" in the §9 header are likewise withdrawn: S1 restates the definition of G0, and S5 (B reaches the same fidelity) shows the experiment could not support "distinct."

## 4. The world was fitted to the language

Design change 3 redefined the world so that it has "the same shape as the rule language," and added an action (`swap_next_v`) to the language in the same change. This was done to remove a wall artefact, and it is recorded — but its effect is that expressibility was guaranteed by construction. A fair design fixes the world's law before the language is finalised. The §6.1 expressibility check therefore checked something that could not fail.

## 5. Closedness was measured against hand-built rules, and the lookup was excluded after its score

Design §6.2 as first written applied a 0.1 margin to any G0 architecture on collision steps; the lookup scored 0.819 against hand-built 0.906 (gap 0.087) and was then moved out of the thresholded comparison as "a memoriser, not machinery." That is a reclassification after the number, of the same pattern as experiment 1's changes 18 and 19. The honest closedness figure is the lookup against the ceiling: **0.819 of 0.923** — the old grammar gets 89% of the way on collision steps by memorising local sensory patterns, and the structured part of the old grammar gets 38%. The overall-fidelity numbers §12.4 said "pass" without printing: best-of-G0 0.707, hand-built 0.835.

The hand-built rules were written by me from knowledge of the law before either process ran. They were intended as an expressibility check and were then used as the ceiling against which "growth" was measured.

## 6. Fidelity claims apply to the sensory-visible sub-contract only

C built the same-target rule and not the crossing rule, as pre-registered (change 2). The M3 thing-signature figures for A0+C (0.974, 0.973 given bound) are on pairs without a post-change crossing; on pairs with one, 0.000. Everywhere file 14 says the built rule is "a faithful component with the world's kind-signature," read "faithful on the sub-contract sensation can see; the world's law has a second half that the sensory contract cannot see and C did not build."

## 7. Phase 2 tested retention, and was confounded

"Does what was built become latent" reduces to "are retained rules still used and not broken" — the wall rule was in the meta-grammar already. And the second law contradicted the first world's walls (file 14 §7). Phase 2 established nothing about accumulation.

## 8a. Further, from C4–C5

- The action set contains the law's exact operation (`swap_next_v`) and the terms include the world's next-states (`n, w`); the antecedent of the same-target law is a single equality atom. The meta-grammar was written by someone who knew the law.
- The two-rule depth of the target was matched to the K = 3 budget by design.
- Change 2 narrowed S3's scope while §10 declared §9 fixed: the frozen design is internally inconsistent on that point.
- The crossing prediction was entailed by C's algorithm and was not a risky prediction; it is a limitation stated in advance.
- No hash or timestamp exists for any individual change; only for the frozen whole. Every future design gets a hash per change.

## 8. Smaller corrections

- The S4 threshold of 0.1 had no derivation (it passed by 0.55).
- M4 perturbs only the action-fitting stage; the design should have said so.
- "Rules are checked before kinematics" while terms n, w are next-states: the terms are *predicted* next-states computed from the current slot state; the rule fires before the slot moves. Wording, not a bug.
- The design's text under-specified how a condition is evaluated on a record (which slot ordering; what counts as a record fixed); the hashed code defines it (either ordering; the whole field must be right).

## 8b. A diagnostic on patched code, run after the cross-examination (not the frozen experiment)

The witnesses (file 15, D3.2–4) asked for three things: fix the defect-accounting bug and rerun M6(ii); rerun the scramble on several permutations and count whether scrambled records are still defects; and run a placebo scramble on a column C never scores on. Done, on a copy of the code with one change — a record counts as fixed only if its old prediction was wrong *and* its new prediction is right. Raw output in `diagnostic_patched_accounting.json`.

| Run | Rules built | Collision-step fidelity |
|---|---|---|
| Patched C, unscrambled | `IF n_i == n_j THEN swap_next_v + hold` | 0.906 (unchanged) |
| Patched M6(ii), no-content records | **nothing** | — |
| Placebo: predicted-field column scrambled | `IF n_i == n_j THEN swap_next_v + hold` | 0.906 |
| Scramble, seed 0 | three rules, the correct one third | 0.424 |
| Scramble, seed 1 | `IF n_i == n_j THEN swap_next_v + hold` | **0.906** |
| Scramble, seed 2 | `IF n_i == n_j THEN swap_next_v + hold` | **0.906** |
| Scramble, seed 3 | three rules, the correct one third | 0.424 |
| Scramble, seed 4 | three rules, the correct one last, without hold | 0.421 |

Records still defects after scrambling: 2,658–2,692 of 2,830 (94–95%), so "same number of defects" was approximately true, not exactly.

Three conclusions. **The accounting bug was real and the fix works**: M6(ii) now passes. **C is not sensitive to generic corruption**: the placebo leaves the rule untouched. **The scramble effect is seed-dependent**: two of five permutations produced no degradation at all, because many records share a state, so permuting outcomes among records leaves the state→outcome mapping largely intact for those states. The original result (0.906 → 0.355 on one seed) was partly luck. S4 as pre-registered (a drop of at least 0.1) holds in 3 of 5 permutations. A scramble that actually destroys the mapping must permute outcomes *within* groups of identical states or replace each outcome with a different wrong field — which is what the witnesses proposed and what experiment 3 will use.

## 8c. A second diagnostic, run after D4–D6: the thing-tracking test for B, unconditional rates, first-collision buckets

The frozen run measured M3 (does each slot keep tracking its thing through a translated change) for A0, A0 + C and A0 + hand-built rules — never for A0 + B. Three witnesses (D5, D6) pointed out that without B, F3 could not be called a result about construction. Also unreported were the unconditional pass rates (unbound pairs counted as failures, not dropped) and a bucket by the *first* collision after the change rather than "any crossing after the change". All three are now computed by `diagnostic_m3_for_B.py` on top of the unchanged frozen code (`exp2/results_out/diagnostic_m3_for_B.json`).

| Architecture | Same-target pairs, given bound | Same-target, unconditional | Crossing pairs, given bound | Crossing, unconditional |
|---|---|---|---|---|
| A0 alone | 0.000 (99 of 541 unbound) | 0.000 | 0.000 | 0.000 |
| A0 + C | 0.973 (21 unbound) | **0.935** | 0.000 | 0.000 |
| A0 + B, seeds 0, 1, 2, 4, 5 | 0.973 | 0.935 | 0.000 | 0.000 |
| A0 + B, seed 3 | 0.969 | 0.932 | 0.000 | 0.000 |
| A0 + hand-built pair | 1.000 | 0.961 | 1.000 | 0.961 |

Three conclusions. **B's rule tracks things exactly as C's does**, including the zero on crossings: F3 is a property of the occupancy-only sensory contract shared by both processes, not of construction (seed 3's vacuous extra atom `c_i != v_j` costs it two pairs). **The given-bound conditioning hid nothing material**: the unconditional same-target rate for A0 + C is 0.935, still above the 0.9 threshold and against 0.000 for A0, but the unconditional figure is the one to report. **The bucket definition made no difference here**: classifying by the first post-change collision gives the identical counts (167 / 541 / 230), so no crossing failure was really an earlier same-target failure; the code concern stands for other worlds.

## 11. A protocol breach: phase 2 should not have run

The frozen design (file 13, §11 step 5) says "Phase 2 only if S1–S6 hold." S6 did not hold: M6(ii) failed. I recorded S6 as "⚠️ content, not carrier" and ran phase 2 anyway. That is a breach of the pre-registered stopping rule, and it means phase 2 is out of contract whatever its numbers. Phase 2 is reclassified as **exploratory**, and its S7 line is reclassified: "wall rule built ✓ (right condition, wrong action)" becomes **❌** — a rule with the wrong action is not the wall rule. The patched accounting in §8b makes M6(ii) pass, but a fix applied after the run does not license a phase that the frozen rule forbade.

## 12. Renamings, so the words stop doing work the results did not do

- The results file's **F1, F2, F3** (findings) collide with the semantics' **(F1), (F2)** (fidelity conditions). The findings are now **Finding-1** (minimal rule), **Finding-2** (B's vacuous atoms), **Finding-3** (identity underdetermined by occupancy).
- "Fidelity" in M1 and M2 means **prediction accuracy** on held-out sequences. Only M3 is a fidelity test in the semantics' sense (component behaviour under translated edits), and even that is operational: no transport was written down.
- "The invisible law" becomes **"identity is underdetermined by occupancy."** The rule language can express the crossing condition (`n_i == c_j and n_j == c_i`); what cannot select it is the defect-driven criterion, because crossing steps produce no sensory defects. The limit is in the error signal, not in what the language can say.
- **"Needed", "protected", "provenance", "on the route"** are the design's words for accuracy against the old grammar, non-regression, input-dependence and code path. None is a predicate of the semantics as written.
- S3 is now reported as **partly failed**: passes on same-target pairs (0.935 unconditional), fails on crossing pairs (0.000); the original S3 text covered all collision-containing pairs.
- A standing statement: **neither experiment instantiates a definition of file 10 as stated** (no target organisation, transport, contract as a set of edit–boundary pairs, active commitments, or the two fidelity conditions). Both test proxies that the semantics motivates. The witnesses of D8 are right that the mapping from S1–S6 to the definitions was never written, and that where it can be reconstructed it is a loose analogy.

## 13. Failure modes of the code found by the witnesses and confirmed (not in file 14 §10)

1. Condition score is raw `true-on-defects − true-on-non-defects`; it ignores base rates (2,830 versus 4,778 records). A rare perfect condition would lose to a common sloppy one. Did not bite: the target condition is frequent and near-perfect.
2. Only the top 20 conditions by that score are ever paired with actions. A hard cap on the hypothesis space, undeclared. Did not bite: the right condition ranked first.
3. Rules only ever fire on slots 0 and 1; the code is written for exactly two things. A0 is declared as a two-slot architecture, so this is a scope limit, not an error, but any generality claim is limited to two things.
4. C builds and accepts rules on the same records, with no held-out check inside the process. Phase 2's wrong action (net 2 on a tie) is this biting.
5. The collision-step accuracy metric (M1) cannot see a crossing error at the collision step — the sensory fields agree there and diverge only later. M3 is the only measurement that sees it.
6. "Zero fitness evaluations" compared C's cost to B's in different units. C scored 3,136 conditions over 7,608 records and up to 320 condition–action pairs; it never called the world's fitness function. Experiment 3 reports record checks and candidate evaluations for both.
7. B's fitness is overall exposure accuracy; C's records are collision-dominated. Another asymmetry to remove in experiment 3.

## 9. What experiment 2 now claims (revised after the audit of this file, file 15 §E)

Every sentence below carries its concession.

- **Setting.** A world whose collision law was rewritten to the shape of the rule language after the language failed an edge case (§4), a rule language whose action set contains the law's exact operation and whose terms are the world's next-states (§8a), a target depth matched to the search budget, and a hand-built version of the law written by me before either process ran. Expressibility was therefore guaranteed by design, and no result here is evidence that the language discovers laws.
- **Closedness.** The old grammar was *not* shown closed to the law: its best member, a memoriser, reaches 0.819 of the ceiling's 0.923 on collision steps (89% of the way); the structured part of the old grammar reaches 38%. The closedness check was split after that number was seen (§5). "Needed" and "grew" are withdrawn (§3).
- **Construction.** A supervised learner with per-record credit, over the fixed rule language, given 2,830 labelled error records, built a rule of the pre-designed minimal depth in one round, using internal aggregate scores over records (condition and action nets) but no call to the world's global fitness function (§2, §13.6). It stopped by its internal criterion at the boundary of what the sensory contract can show; whether that was "correct" is unverified, because it has no held-out check (§13.4) and the residual law (crossing) was invisible to its error signal (§12). Its known weaknesses: one-step lookahead, arbitrary tie-break, fragile defect accounting, no held-out check, a base-rate-blind condition score, a top-20 cap on conditions (§13).
- **Content-dependence.** Under the frozen code S6 **failed** (M6(ii) built a rule from no-content records). On patched code, as a post-hoc diagnostic and not the frozen experiment, the accounting fix makes M6(ii) pass and a placebo scramble leaves the rule untouched (§8b). The scramble test itself is seed-dependent: three of five permutations degrade the rule, two do nothing, because states recur across records; the original one-seed result was partly luck, and a scramble that destroys the state→outcome map was not run (§8b). So the claim is: the learner's output depends on the pairing of states with outcomes, shown on three of five permutations of a scramble that did not reliably break the pairing.
- **Fidelity.** M1/M2 are prediction accuracy, not fidelity in file 10's sense (§12). M3 (an operational translated-edit test with no transport written down) shows the rule keeps the slots on their things through same-target collisions (0.935 of pairs unconditional, from 0.000 without it) and fails through crossings (0.000): S3 **partly failed** against its original text (§8c, §12). B's rule gives the same figures in a post-hoc diagnostic (five seeds identical; seed 3 loses two pairs to a vacuous atom), so identity-through-crossing is underdetermined by occupancy for both processes, and Finding-3 is a limitation stated in advance, not a result.
- **The comparison.** A mutation search with a global scalar reached the same rule wrapped in vacuous atoms in about 1,750 evaluations, measured against a hand-built ceiling written with knowledge of the law and under an objective (overall accuracy) that differs from the learner's (collision-dominated records) (§13.7). The scramble test does not distinguish provenances (§1). Neither "distinct from selection" nor any provenance claim survives; the contrast is itemised versus scalar feedback over one language.
- **Phase 2.** Run in breach of the frozen stopping rule, with a second law that contradicts the first; exploratory only; the wall rule was not built (§7, §11).
- **Standing.** Neither experiment instantiates a definition of file 10 as stated (§12); every experimental predicate ("needed", "protected", "provenance", "on the route") is the design's word for accuracy, non-regression, input-dependence and code path.

## 10. What would test the claim (rewritten after the E4 attack on the first sketch, file 15 §E4)

The first sketch ("equal access, same operator, one process collapses the records to a scalar, scramble both") had the flaw of experiment 2 built in: the contrast was under-defined and could be analytic. The question is not construction versus selection. It is **whether per-record credit buys anything that a sufficient scalar summary of the same records does not.** The design that could actually fail:

1. **Law family and blinding.** A pre-registered law generator over worlds with at least three slots, hidden identities, collision and crossing events, and a sensory map. Target laws are generated and hashed before the language is finalised, by a process the language designer cannot see (a seeded generator committed first, or a second party). No revision after an expressibility failure; failures are recorded as results.
2. **Language.** A grammar frozen from primitive operations and generic combinators, with the action set, term set, depth limit, proposal distribution, scoring function, validation split, tie-break and stopping rule all fixed and hashed before any law is seen.
3. **Processes — four cells, one factor.** Common candidate representation and proposal distribution; the credit signal is the only factor: (i) per-record credit with local component updates; (ii) per-record credit aggregated before selection; (iii) a simple scalar (net defect count or accuracy); (iv) a **sufficient-statistic scalar** (likelihood of the records under the candidate). Matched on candidate evaluations, record accesses, proposals and wall clock; all four reported.
4. **Primary prediction.** On held-out laws, (i) recovers the law or generalises to unseen changes better than (iii) by a pre-registered margin. **The critical control is (iv):** if it matches (i), the advantage is information, not credit route, and the construction story is dead as a route story.
5. **Manipulations.** Scramble the raw records before either process sees them, with several pre-registered permutations — within-state permutations where they are not no-ops, and outcome replacements — each verified by state→outcome mutual information and defect counts, with a placebo column and a known-corruption positive control. Every permutation reported.
6. **Mediation.** Delete the individual records that support the true rule and check which process's *specific* rule changes.
7. **Metrics.** Primary: held-out law recovery and generalisation to unseen changes, including crossings. Secondary: collision-step accuracy, closedness against a pre-registered ceiling family (true law; exhaustive best-in-language; best held-out predictor under the same sensory contract; best architecture under the same budget), component signature under translated edits with the transport written down, all rates unconditional. All architectures reported, memorisers included, none excluded after scores are seen.
8. **Power.** Number of worlds, seeds and permutations fixed in advance; paired seeds; a smallest effect of interest and an equivalence region.
9. **Process rule.** Hash and timestamp the design at every change; a diagnostic run after freezing is labelled a breach of the frozen protocol and cannot support a frozen claim.
10. **What counts as failure.** (iv) matches (i); (i) fails to recover crossings when the records contain crossing residuals; the scramble leaves both unchanged or changes both generically; the advantage disappears under matched information; the effect is world-, seed- or hyperparameter-specific.
