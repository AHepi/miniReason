# Test design: do kinds emerge from selection, or must they be supplied?

**Status: amended, then frozen. Fingerprints of this file and the code are recorded in the results file (12) at the moment of freezing. Nothing was run before that moment except the control check in section 8, step 2.**

---

## 1. The claim under test

**The diagnosis (yours):** the kinds that appear in an explanation — object, cause, rule, persistence — are *outputs* of variation and selection running beneath explanation, not *inputs* an explanation must be matched against. More precisely, in your three points:
1. Kind-preserving machinery must be latent (expressible) for kinds ever to be expressed.
2. The machinery does not determine *which* kinds are expressed; it is a necessary condition for any to be.
3. The machinery bounds the set of expressible kinds; **history determines which become expressed.**

**The rival (the correspondence view):** kinds are prior. A faithful predictor has kind-preserving structure regardless of history, because kinds are there to be matched.

**What separates them, operationally:** under the diagnosis, kind-preserving structure appears only when the history contains changes that demand it, and is absent when the history is indifferent. Under the rival, it appears regardless.

**A sharpening from the semantics (file 10, Derivation 2):** history does not choose from a fixed menu of kinds; it determines how fine the menu is. Two components no admitted change separates are one kind at that contract. So the experiment also asks: does the *distinction* between a cell-tracker and a thing-tracker exist at all under a history without occlusion?

## 2. What is built

Everything is small enough to enumerate exhaustively. No sampling; every number is exact.

### 2.1 The world (primitive layer)

- A line of **6 cells**, numbered 0–5.
- **2 things** (the main world) or **1 thing** (the neutral world, section 2.7).
- Each thing has a position and a velocity in {−1, 0, +1}. Each step: new position = position + velocity; if that leaves the line, velocity flips sign and the thing moves the other way instead.
- Things pass through each other and may share a cell.
- A run is **9 steps** after the initial configuration (time points 0–9).

### 2.2 The sensory field (what the thinker sees)

At each time point, a **6-bit occupancy pattern**: bit *i* is 1 if any thing is at cell *i*. No identity, no count, no velocity.

### 2.3 The admitted changes (the full contract)

Applied at **step 3** of the run (so the thinker has already seen three fields and could have inferred motion). Applied to the world state before the field at step 3 is recorded.

| Change | 2-thing count | 1-thing count | What it does |
|---|---|---|---|
| identity | 1 | 1 | no change |
| displace(thing, cell) | 12 | 6 | put that thing at that cell, velocity unchanged |
| set_velocity(thing, v) | 6 | 3 | set that thing's velocity |
| occlude(window) | 4 | 4 | a window of **3 contiguous cells** (0–2, 1–3, 2–4, 3–5) reads 0 in the sensory field from step 3 to the end, whatever is there |
| swap | 1 | 0 | exchange the two things' identities; the sensory field is unchanged at every step |

**24 changes** (2-thing), **14 changes** (1-thing).

### 2.4 Initial configurations

2-thing: unordered pairs of (position, velocity) with repetition: **171**. 1-thing: **18**.

### 2.5 The fitness target

The thinker sees the **sensory** field (with occlusion applied) and predicts the **true** occupancy at the next time point. Fitness is agreement with true occupancy, scored at time points 2–9 (8 predictions per run; time point 1 is unpredictable for any predictor from a single field). Rationale: selection pressure comes from the world, not from sensation matching itself — a thing you cannot see can still act on you.

**Exposure and evaluation halves.** Configurations are split by index: even-index configurations are the **exposure** half, odd-index the **evaluation** half. Lookup tables are filled from the exposure half only. **Every fitness figure is on the evaluation half.** This is fitness in the same environment on instances not seen — what selection actually acts on. Without it a bounded-memory table memorises the local patterns of the very sequences it is scored on, and is selected everywhere for that reason alone.

**The sensory ceiling.** Because a change lands at step 3 without warning, no predictor that sees only sensation can be right at the step where it first shows; and two things starting in one cell are one blob to sensation. Fitness is therefore reported alongside a **ceiling**: the best deterministic predictor from sensation on the evaluation half — for every sensory prefix, predict the most common continuation. It is an in-sample bound (it has seen the prefixes it predicts) and is reported for scale, not as a pass/fail threshold. "Reaches the top" below means: is fitness-maximal among architectures.

### 2.6 The hypothesis space (the latent machinery)

A predictor is an **architecture** with two optional pathways. Prediction = bitwise OR of the pathways in use.

**Lookup pathway:** a table from the last *k* sensory fields (*k* ∈ {1, 2, 3}; fewer if fewer have been seen, so it predicts from the first field like a slot does) to a predicted true field. The table is filled by **exposure**: one pass over the history, recording what actually followed each key (last-writer-wins). Unseen keys predict empty. This is the no-object-model alternative: memory without things.

**Slot pathway:** up to *M* ∈ {1, 2, 3} slots. Each slot, when bound, holds (cell, velocity) and advances each step by the same reflecting kinematics as the world. Slots are reconciled with each observed field by one **read-in rule** from this fixed grammar:

- **rebind**: discard all slots every step; bind one slot per occupied cell, velocity inferred from the previous field. (A cell-tracker.)
- **persist(τ, r, j)**: after advancing, a slot whose predicted cell is occupied is confirmed. Each occupied cell not matched by a confirmed slot re-binds the nearest unconfirmed slot within distance *r*, else binds a free slot with velocity inferred from the previous field. On re-binding, velocity is corrected from the slot's previous cell — unless *j* is set and the jump is more than one cell, in which case the old velocity is kept (a teleport preserves velocity; a one-cell mismatch means the velocity changed). An unconfirmed slot not re-bound persists, counting steps; it is dropped when its count exceeds τ. τ ∈ {0, 2, 5, ∞}, r ∈ {2, 5}, j ∈ {no, yes}. (τ = 0 is a cell-tracker with velocity; τ = ∞ is a thing-tracker that never forgets. *j* is latent machinery for telling a displacement from a change of direction.)

Seventeen read-in rules. With lookup on/off × *k* × slot count × rule, there are **208 distinct architectures**.

**The kind under test is persistence** — the τ gene and the `rebind` rule. A thing-tracker keeps a slot alive when nothing confirms it; a cell-tracker does not. The lookup pathway is a different axis (an object model versus none) and is reported separately.

### 2.7 Histories

| History | World | Changes included | Sequences |
|---|---|---|---|
| **H_neutral** | 1-thing | identity, displace, set_velocity | 180 |
| **H_passive** | 2-thing | identity only | 171 |
| **H_kinematic** | 2-thing | identity, displace, set_velocity | 3,249 |
| **H_full** | 2-thing | all 24 | 4,104 |

H_neutral is the kind-neutral history: one thing, never occluded, no crossings — nothing in its content distinguishes a thing-tracker from a cell-tracker. Whether H_passive is also content-neutral (whether crossings of two things already demand identity at *k* = 3) is an empirical question the controls answer.

### 2.8 Selection — primary: exhaustive

Because the architecture space is 208, selection is done **exhaustively**: every architecture is evaluated on every history. The selected set for a history is the set of architectures with maximal fitness on it. This is selection with unlimited reach, and removes the reachability confound (your point 2) from the primary result.

### 2.9 Selection — secondary: evolutionary, to measure search bias

A mutation-selection search over the same 208 architectures: population 32, elitism 4, one mutation per offspring, 40 generations, seeds 0–5, fitness memoised. Run on H_neutral, H_passive, and H_full. This measures which architectures a blind search actually lands on — the reachability and search-bias question — separately from which are best.

## 3. What is measured

**M1 — fitness on the evaluation half of own history**, after exposure to the exposure half, per architecture per history.

**M2 — fitness on the evaluation half of the full contract of its world**, after the same exposure, per architecture, broken down by change type. For architectures selected on a narrow history, this is fidelity on changes never seen.

**M3 — thing-signature** (2-thing world only), per slot architecture. For each (configuration, change): run the predictor to step 2 on the unchanged sequence; match its bound slots to the things by (cell, velocity); if a match exists, apply the **translated** change to the slot state (displace → set that slot's cell; set_velocity → set that slot's velocity; occlude → nothing, it is a sensor edit; swap → exchange the binding), then continue on the post-change sensory sequence and check at every later step that each bound slot's (cell, velocity) equals its bound thing's (position, velocity). A slot architecture **has thing-kind** when this holds for every configuration and every change. Reported as a fraction, by change type. This is component fidelity (F1) of file 10, computed directly.

**M4 — failure structure**: for every architecture on every history, which change types fail on M2.

## 4. Pre-registered outcomes

Written before any code was run, and not changed after.

### Supports the diagnosis (point 3)

- On **H_neutral**, the best architecture for every persistence value ties (within 0.01): the history cannot tell a thing-tracker from a cell-tracker.
- On **H_full**, the top architectures all have persisting slots (τ > 0), and those have thing-kind under M3.
- On **H_passive** and **H_kinematic**, the selected set includes non-persisting architectures, and those fail M2 on occlusion.
- That is: the thing-tracker / cell-tracker distinction is selected for only when the history contains occlusion; without it, the two are one kind for that history.

### Sinks the diagnosis (point 3)

- On **H_neutral**, the selected set (fitness-maximal) **excludes** all non-persisting architectures (rebind, τ = 0) — i.e. the content of a history with no occlusion and no crossings nonetheless requires persistence. Kinds would then be forced by the prediction task itself, not made by history.

### Search bias (a finding that qualifies point 3)

- Exhaustive selection on H_neutral yields a tie, but the **evolutionary** search converges on slot architectures (or on lookup) in most seeds. Then kind-structure can be expressed by the shape of the search alone, with no pressure from content. "History" in point 3 would then have to include search structure, not only exposure.

### Fidelity and kind come apart (a finding about contracts)

- The M2-maximal architecture on H_full is not M3-maximal, or vice versa. This would be a direct illustration of Derivation 2: prediction-from-sensation and component-fidelity-under-translated-edits are different contracts and can select different kinds. It is not a contradiction of Derivation 1, which is contract-relative.

### Finding either way

- An architecture with **no persisting slots** (lookup-only, or slots with τ = 0 / rebind) is fitness-maximal on **H_full** including occlusion. Pre-committed follow-up: evaluate the same architecture, with no further exposure, on a 7-cell or 3-thing world. If it stays at 1.0 it captured structure; if it collapses it was a table at this grain — correctly reported as adequate on this contract and correctly not generalising.

### Underpowered

- No slot architecture reaches 0.95 × the sensory ceiling on H_full. Then the grammar in 2.6 cannot express an adequate predictor for this world; the design is revised and re-frozen, and this attempt is recorded as failed.

### Out of scope, on purpose

- **Construction.** The machinery (the grammar of 2.6) is fixed for the whole experiment. This tests selection — the expression of latent kinds. It cannot test construction — the extension of what is latent — because that would require the grammar itself to change during the run. That is the next experiment.

## 5. Controls (as amended)

The kind under test is persistence (2.6). The two checks made before freezing:

- **Neutrality** (H_neutral): the best architecture for each persistence value τ = 0, 2, 5, ∞ all within 0.01 of each other. A history with nothing hidden should not select for persistence. (`rebind` is reported beside them but is not in the check: it differs from τ = 0 in re-inferring velocity from scratch every step, which is a velocity-memory difference, not a persistence difference.)
- **Adequacy** (H_full): best slot-only > best lookup-only on the evaluation half.

Also reported, not pass/fail: the best slot-only architecture's fraction of the ceiling; best lookup-only versus best slot-only on both histories (the object-model axis).

If neutrality fails, H_neutral is not neutral for the kind under test and the design is revised. If adequacy fails, the grammar is inadequate and the design is revised.

## 6. What this cannot show

- That any infant, animal, or program works this way. It is a relative-consistency witness for the two-layer picture.
- That the diagnosis holds for all worlds. One small world, one small grammar.
- Whether a faithful predictor without thing-kind slots "really explains." Only what it does under an extended contract.
- Anything about construction.

## 7. What is fixed and what is free

**Fixed by this document:** sections 2.1–2.9, 3, 4, 5.
**Free, fixed in code and hashed:** tie-breaking order in the lookup table's last-writer-wins; slot iteration order in reconciliation; the exact mutation operator in 2.9.
**Not permitted after freezing:** changing anything fixed; adding a measurement; reclassifying an outcome.

## 8. Order of work

1. Write the code with plain-word names and a note at the top.
2. Run the two named controls of section 5. If either fails its expectation, stop and revise this document.
3. Fingerprint this document and the code. Record both in the results file.
4. Run the exhaustive table on all four histories, M2 and M4 for all, M3 for all slot architectures, and the evolutionary secondary.
5. Write every number to a raw results file.
6. Classify against section 4.
7. Add to the project story.

## 9. Changes made before freezing, and why

1. **Changes applied at step 3, not step 0.** A change at step 0 is indistinguishable from a different initial configuration, and all configurations were already enumerated; step-0 changes added nothing.
2. **Occlusion is a 3-cell window, not a single cell.** A single occluded cell hides a moving thing for one step, which a lookup with *k* ≥ 2 can learn as a pattern. A 3-cell window hides it for at least three steps, beyond *k* = 3.
3. **Fitness is against true occupancy, not the sensory field.** Under occlusion, predicting "nothing there" would be *correct* against sensation and a persisting slot would be *penalised* for tracking the hidden thing. Selection pressure must come from the world.
4. **Run length 9, scored from time point 2.** Enough steps after the change for occlusion effects and for τ = 5 to matter.
5. **The hypothesis space is a grammar of architectures, not free-form tables and rules.** Lookup tables learn by exposure; slot rules are fixed and enumerated. This is the concrete form of your point 1: the machinery is latent, and only which of it is used is selected.
6. **Primary selection is exhaustive, not evolutionary.** 112 architectures can be enumerated. This removes the reachability confound (your point 2) from the primary result and isolates it in the secondary evolutionary run.
7. **H_neutral added: one thing, no occlusion.** The previous sinking condition ("kinds under pure watching") was wrong: pure watching of two things contains crossings, which may already demand identity. The neutral world has no crossings.
8. **Pre-registered outcomes rewritten** to match, with two added: search bias, and fidelity-kind dissociation.
9. **Construction declared out of scope**, with the reason.
10. **Change counts corrected** (24 and 14, not 26).
11. **Fitness reported against a sensory ceiling** (2.5). A first version of the ceiling counted every ambiguous prefix as unachievable and was exceeded by real architectures; it was corrected to the majority-continuation predictor, which is the true bound.
12. **"Expected 1.0" replaced throughout.** No sensory predictor can be right at the step where an invisible change first shows.
13. **Persist rules infer a fresh slot's velocity from the previous field**, as rebind already did. Diagnosis from the first control run: a fresh slot bound with velocity 0 lost the first prediction after a co-located start.
14. **Gene added: jump-keeps-velocity** (*j* in 2.6). Grammar now 208 architectures.
15. **Lookup predicts from the first field**, using the longest available prefix up to *k*. It was handicapped by needing *k* fields before its first prediction.
16. **The neutrality control compared the wrong pair** — lookup-only against slot-only. The kind under test was always persistence (section 2.6 says so; the wrong-kind control was τ = 0 / rebind). The check now compares best-per-persistence-value. Lookup versus slots is reported separately as the object-model axis. Recorded honestly: the first control run had already shown τ = 0 winning H_neutral and τ = ∞ winning H_full, which is the supporting outcome; this change does not create that result, it stops the check from asking a different question.
17. **Exposure/evaluation split by configuration index.** Diagnosis: on train = test the *k* = 3 lookup scored 0.820 on H_full and 0.656 on held-out configurations, while the tracker scored 0.801 on both. The lookup was memorising 2,398 local patterns. All fitness is now on the held-out half.
18. **The 0.95-of-ceiling adequacy threshold is dropped.** It was a guess, and the diagnosis showed the ceiling is an in-sample bound: the tracker's gap to it is the change step itself and co-located starts, which no sensory predictor without a thing-count prior can see. Adequacy is now the ordering, slot-only > lookup-only, on held-out configurations. The fraction of ceiling is still reported (it was 0.88 at this point).
19. **Neutrality check restricted to the τ family.** Under the amended check τ = 0, 2, 5, ∞ tied *exactly* on H_neutral and rebind sat 0.026 below; rebind's deficit is that it cannot keep velocity through a teleport, which is not the kind under test.
20. **A thing-count prior was considered and not added.** It would let a lone blob bind two slots and would close part of the co-location gap. It is a further piece of latent machinery and a candidate for a follow-up, not a change made after seeing results.
21. **Revision stops here.** Three rounds before freezing. If the two checks do not pass under these criteria, the attempt is recorded as failed and reported, not revised again.
