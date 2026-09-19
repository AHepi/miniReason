# Results: construction — can new machinery be built, and can we tell it was built rather than selected?

**Status: run once, after freezing. Design and code fingerprinted together before the run; nothing changed afterwards. Two diagnostics were run on the frozen code afterwards to explain two failures; they changed nothing and are reported in section 8.**

| File | Fingerprint (SHA-256) |
|---|---|
| Design (13) | `d8815f55e1326a24730dc3455d3702158bbf1ba7fe8962d7341dff6e33546eb5` |
| Code (14a) | `156f3ec2089d902fd215f83065a4cd95ab2d3935987214866aadf08fdf3d4417` |
| Base code from experiment 1, unchanged | `54259a930169556686331c5b1fe50778cf346edab0dce4acfde674f2d22c6d6f` |
| Raw results (14c) | `a70cfb90b6eb35b5fbb39074b77fc9d4c4d96c2a173f983aebc40336ee7f7076` |

Frozen 2026-09-19 05:52 UTC after four recorded changes. Run took about 19 minutes. All figures on the evaluation half (938 held-out sequences); exposure half 951.

---

## The answer in one paragraph

**Phase 1 held on every supporting outcome but one clause, and the crack it exposed was pre-registered.** Starting from the organism experiment 1 selected, the constructing process C built exactly one rule — `IF n_i == n_j THEN swap_next_v + hold`, the same-target collision law, in its minimal form — from 2,830 itemised records of what went wrong, using no fitness number at all. That one rule takes collision-step fidelity from 0.352 to 0.906 (ceiling 0.923), beats the best the old closed grammar can do (0.819, and that by a memoriser; 0.366 for any structured architecture), costs nothing on non-collision steps (they *improve*, 0.702 → 0.819), and passes the thing-signature test on 97% of pairs — except pairs with a crossing after the change, where it scores **zero**, because C never built the crossing rule, because crossings are invisible to sensation, exactly as written down before running. Scrambling the defect records' outcomes while keeping their number destroys C (0.906 → 0.355 on collisions); the blind process B, which never reads them, is byte-for-byte unaffected and reaches the same fidelity in 6 of 6 seeds with the same law wrapped in vacuous extra atoms. So: **same machinery, two routes, and the route is detectable by ablation.** The one supporting clause that failed is an ablation of C's own bookkeeping (M6 ii), and it exposed a real weakness: C counts "new prediction equals target" as a fix without checking the old one differed. **Phase 2 is confounded by my own design** — the second law I chose contradicts the first world's walls instead of extending them — and also exposed two more weaknesses in C. All of it is in section 9.

---

## 1. Phase 1 — fidelity (M1) and protection (M2)

| Architecture | All | **Collision steps** | Non-collision steps |
|---|---|---|---|
| Sensory ceiling (in-sample, for scale) | 0.900 | 0.923 | 0.895 |
| A0 alone (no rules) | 0.637 | **0.352** | 0.702 |
| S0: best of old grammar G0, any kind — `lookup(k=2)` | 0.707 | 0.819 | 0.681 |
| S0: best *structured* G0 — `slots=2, persist(τ=0, r=5, j=yes)` | 0.626 | **0.366** | 0.686 |
| **A0 + C's one built rule** | **0.835** | **0.906** | **0.819** |
| A0 + B's rule (identical figures, all 6 seeds) | 0.835 | 0.906 | 0.819 |
| A0 + two hand-built rules (same + cross) | 0.835 | 0.906 | 0.819 |

Three things to read off. C's single rule reproduces the hand-built pair exactly, because the crossing rule adds nothing at the sensory level. The old grammar's memoriser gets four-fifths of the way on collision steps by pattern-matching "two adjacent blobs approaching → they stay," but no structured old-grammar architecture gets above a third. And adding the rule *raised* non-collision fidelity: slots that stay correctly bound through a collision are right afterwards too.

## 2. What C did, and at what cost (M7, M8)

Round 1: 2,830 defect records, 4,778 non-defect records. Condition induced: `n_i == n_j` (score 929). Action solved: `swap_next_v + hold` — fixed 820, broke 0. Round 2: 1,266 defects remain; **no condition–action pair has positive net; C stops.** Those residual defects are the change step itself and co-location ambiguities — no consistent pattern, and C correctly declines to invent one.

Zero fitness evaluations. B used 1,720–1,788 full-history fitness evaluations per seed to reach the same place.

## 3. What B found (M7)

All six seeds: same fidelity to 16 digits. Rules:

```
seed 0: IF (c_i == c_j) OR  (n_i == n_j) THEN swap_next_v + hold
seed 1: IF (n_i == n_j) AND (c_j != v_j) THEN swap_next_v + hold
seed 2: IF (c_i != w_i) AND (n_i == n_j) THEN swap_next_v + hold
seed 3: IF (c_i != v_j) AND (n_i == n_j) THEN swap_next_v + hold
seed 4: IF (v_i != n_i) AND (n_i == n_j) THEN swap_next_v + hold
seed 5: IF (n_i == n_j) AND (n_i != w_j) THEN swap_next_v + hold
```

Every one is `n_i == n_j` plus one atom that is vacuous in this world (`c_i == c_j` is never true — positions are distinct; the rest are almost never false). B has no simplicity pressure, so it keeps whatever junk arrived with the law. **F1, as pre-registered:** structurally different rules, one kind on this contract, and they would come apart on a contract where the junk atom matters (allow co-location, or a thing at cell 1 with velocity 1).

## 4. Thing-signature through collisions (M3)

Given-bound fractions (unbound = the predictor was not tracking both things exactly at step 2; shown as count).

| | No collision after change | Same-target collision after | **Crossing after** |
|---|---|---|---|
| A0 alone | 0.946 (18 unbound) | **0.000** (99) | 0.000 (21) |
| **A0 + C** | **0.974** (13) | **0.973** (21) | **0.000** (9) |
| A0 + hand-built pair | 1.000 (13) | 1.000 (21) | **1.000** (9) |

A0's slots stop being the thing at the first collision. C's rule makes them the thing through every same-target collision. And on the 230 pairs with a crossing after the change, C's slots pass through while the things bounce — zero — while the hand-built crossing rule gets all 221 bound pairs. **This is F3, the invisible law:** the constructor built exactly the kinds its sensory contract could see, and the finer contract of M3 (which uses thing identities through translated edits) reveals what it could not.

## 5. The scramble test (M4) — the test that distinguishes the provenances

Defect records handed to C with the *outcome* column permuted among them: same states, same 2,830 records, wrong pairings.

| | Rules built | All | Collision | Other |
|---|---|---|---|---|
| C, unscrambled | 1 rule (the law) | 0.835 | **0.906** | 0.819 |
| C, scrambled | 3 rules: `(c_i == c_j) OR (n_i == n_j) → swap_next_v` (no hold) ×2, then a patch | 0.659 | **0.355** | 0.728 |

Under the scramble C still *induced* a near-right condition (that step reads only states, which were not scrambled) but *solved* the wrong action (that step reads outcomes, which were) — it dropped the `hold`. Collision fidelity fell by 0.55; the requirement was 0.1.

B, seed 0, re-run with the scrambled records passed in as an argument its code never reads: **byte-identical output.** The defect representation is on C's route and not on B's. That is not a claim about the code's data flow — it is a demonstration that the two processes' outputs depend on different things, which is what "provenance" means in file 10.

## 6. Content, not carrier (M5, M6)

- Records in reverse order → identical rule. Slots relabelled i↔j throughout → identical rule. **M5 ✓.**
- Empty defect set → builds nothing. **M6(i) ✓.**
- Defect records with the outcome replaced by the prediction (no defect content) → **built** `IF (n_i == n_j) AND (c_j != n_j) THEN reverse_i`, three times, claiming "fixed 671, broken 0." **M6(ii) ✗.** Section 8 diagnoses it.

## 7. Phase 2 — does what was built become latent?

Second law added: sticky walls (a wall hit stops the thing instead of reflecting it). C continued from its phase-1 rule.

| | Sticky world, all | Sticky, collision-type steps* | Sticky, wall-stop steps only | **Back on the original world, all** |
|---|---|---|---|---|
| A0 + phase-1 rule | 0.712 | 0.436 | 0.234 | 0.835 |
| **A0 + phase-1 + 2 built rules** | 0.773 | 0.716 | 0.627 | **0.431** |
| A0 + phase-1 + hand-built wall rule | 0.808 | 0.769 | — | **0.636** |

\*In phase 2 this bucket includes wall-stop steps, so it is not comparable to phase 1's collision column.

C built `IF v_j != w_j THEN swap_next_v + hold` (condition right: a wall hit; action wrong) and then a patch. Total on the sticky world improved (0.712 → 0.773); wall-stop steps went from a quarter right to five-eighths. The collision rule still fires: on the original world's collision steps, 0.893 against 0.906 before.

But the new rules **collapse everything else on the original world** (0.835 → 0.431). And so does the *hand-built* wall rule (0.636). That is not a failure of construction. A sticky wall and a reflecting wall are contradictory laws about the same event, so any rule correct for one is wrong for the other. **I chose a second law that fights the first world rather than extending it. Phase 2 is confounded by the design and must be rerun with a compatible second law.**

## 8. Two diagnostics on the frozen code

**Why M6(ii) built a rule.** The rule fires on 929 no-content records and leaves the prediction unchanged on 671 of them — exactly the 671 it counted as fixed. With the outcome set equal to the prediction, "new prediction equals outcome" is true whenever the rule does nothing. C's accounting never checks that the old prediction differed. In the real run that invariant is guaranteed by how records are collected, so the phase-1 result stands; but the accounting is fragile and the stopping rule can be fooled.

**Why C picked the wrong wall action.** On the phase-2 records, `stop_both + hold` and `swap_next_v + hold` tie at net 952 (fixed 979, broke 27); the tie is broken by enumeration order and `swap_next_v` comes first. Both give the same *next field*; they leave different *velocities* behind, which only shows up a step later — C looks one step ahead. The natural per-slot rule `stop_i + hold` scores only 540 because a rule fires once per step in the first matching order, so when both things hit walls at once it can stop only one.

## 9. Classification against the pre-registered outcomes (design section 9)

**Supports:**
- ✅ **S1 needed** — 0.906 > 0.819 (best G0, a memoriser) > 0.366 (best structured G0).
- ✅ **S2 protected** — non-collision 0.819 ≥ 0.702.
- ✅ **S3 faithful** — 0.974 and 0.973 given bound on non-crossing pairs (threshold 0.9), from 0.000 for A0. Crossing pairs 0.000, as pre-registered under F3.
- ✅ **S4 on the route** — scrambled C worse by 0.55 (threshold 0.1); B byte-identical.
- ✅ **S5 provenance is not output** — B within 0.05 of C in 6 of 6 (identical).
- ⚠️ **S6 content, not carrier** — M5 ✓, M6(i) ✓, **M6(ii) ✗**: C built a no-op rule from records with no defect content. Failure mode 3 below.
- ⚠️ **S7 accumulates** — wall rule built ✓ (right condition, wrong action); sticky-world total beats phase-1 ✓ (0.773 > 0.712); collision fidelity within 0.01 ✗ (0.013). And the un-pre-registered collapse on the original world, which is a design confound (failure mode 10).

**Sinks:** K1 no. K2 no. K3 no. K4 by its letter no (0.013 < 0.05) — but see S7.

**Findings either way:** F1 ✓ (section 3). F2 — C stopped at one rule with 1,266 residual defects, all of them the change step or co-location ambiguity; report, no more rules warranted. F3 ✓ (section 4).

## 10. Failure modes — all of them

You asked for every one. Grouped by what fails.

**Of the constructing process C**
1. **One-step lookahead.** Action solving compares only the next field; two actions that agree on it but leave different internal state (velocities) are indistinguishable, and the wrong one can be chosen (phase 2).
2. **Arbitrary tie-break.** Ties among equal-net actions go to enumeration order. In phase 2 that picked `swap_next_v` over `stop_both`.
3. **Fragile defect accounting.** "Fixed" means "new prediction equals outcome," never re-checking that the old prediction differed. Records that are not real defects are counted as fixed by any rule that does nothing to them (M6 ii). The stopping rule "positive net" is fooled the same way (the scrambled run built three junk rules with small positive nets).
4. **Builds only what its contract can see.** No sensory defect, no rule: the crossing law is never built (F3). Correct behaviour, and a limit — kinds visible only at a finer contract are unreachable from sensory defects.
5. **Underdetermined on unseen cases.** A rule built from one world's records can be wrong in cases those records never contained; the wall rule fires on ordinary reflections because the sticky world never showed it one. File 10's Derivation 3 applies to construction, not only selection.
6. **Never checks its conjecture on the evaluation half.** C accepts every rule with positive net on exposure records. A critical step — try the rule and look at the new defects — is only implicit (the next round's records).

**Of the rule language**
7. **Fires once per step, first matching order.** Cannot express "apply to each slot independently"; a symmetric per-thing law must be written as a both-holding pairwise action.
8. **Depth-two conditions.** The crossing law needs a second rule by design.
9. **`swap_next_v` is in the action set.** A tailoring concern, noted in the design; mitigated only by B having the same actions and by the data having to choose it over `swap_v`.

**Of the design**
10. **Phase 2's second law contradicts the base world** (sticky vs reflecting walls). The collapse on the original world is guaranteed for any correct sticky rule, hand-built included. The accumulation question was not actually tested. Needs a second law that *extends* (e.g. a third thing, or a one-way gate).
11. **Phase 2's "collision" bucket mixes wall-stop steps in**, so its figures are not comparable to phase 1's.
12. **Four pre-freeze changes**, two of which (2 and 4) a hostile reviewer should probe: an expectation added after thinking the world through, and a closedness check split after seeing the memoriser's number. Both recorded with numbers.
13. **"Given bound" conditioning** discards 2–18% of pairs in M3 (mostly two things that started adjacent and ambiguous).

**Of the blind process B**
14. **No simplicity pressure.** Finds the law with vacuous atoms attached; would misfire on a contract where they bite.

**Carried over from experiment 1**
15. Twenty-one pre-freeze changes there.
16. No thing-count prior; 20% of M3 pairs unbound.
17. The lookup's train-equals-test memorisation was caught only at the third revision.

**Of the process around the experiments**
18. External adversarial cross-examination was blocked by the session's network policy at first attempt (both hosts 403 at the egress gateway); harness and battery were ready and unrun at the time of writing this file.
19. API keys were pasted into a chat transcript; they should be rotated when the work is done.

**Of the theory (file 10)** — attack points A–E remain open. Experiments 1 and 2 bear only on D, and support it in one small world each.

## 11. What this does not show

One world, one rule language, one constructor. Nothing about brains. Not an escape from the regress — the design says so in its first section, and nothing here changes that. Phase 2 does not test accumulation. And the constructor is a version-space learner with a small grammar, not a theory of conjecture; what it shows is that a process whose only inputs are itemised defects builds the right law, and that a process whose only input is a number builds the same law by a route that ablation can tell apart.
