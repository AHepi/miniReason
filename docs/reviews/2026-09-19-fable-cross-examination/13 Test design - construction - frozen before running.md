# Test design: construction — can new machinery be built, and can we tell it was built rather than selected?

**Status: design, to be frozen after the section-6 checks. Fingerprints of this file and the code will be recorded in the results file (14) at freezing.**

---

## 1. The trap, faced first

Any process I can write has a fixed program. Whatever it produces was expressible by that program. So if "construction" meant "produces something not latent at any level," it could never be shown, and the regress would swallow every experiment. **That is not the claim.**

The claim from file 10 is about **provenance**, which is about the route, not the output:

- A **selected** piece of machinery was produced by variation and survival. Nothing inside the process represents *what went wrong*. The process receives, per candidate, a number.
- A **constructed** piece was produced by operating on a **representation of the defect** — which states, which predictions, what actually happened — and that representation lies on the route from failure to new machinery.

Two processes can produce the same rule. The semantics says they still differ, and that the difference is checkable: **remove or scramble the defect representation and the constructing process breaks, while the selecting process — which never read it — is unaffected.** That is the operational content of "the mapped objection is on an active dependency route."

So this experiment has two grammars, and it says so:

- **G0, the object grammar**: the 208 architectures of experiment 1. Closed. Selection in experiment 1 chose among them.
- **The meta-grammar**: a small fixed language of *rules* that can be added to an architecture. Construction adds rules to G0. Blind selection over the meta-grammar can add the same rules. The meta-grammar is fixed; the regress is not escaped and no one should read this as if it were.

What is tested: (i) whether G0 is genuinely closed to a new feature of the world, so that extending it is *needed*; (ii) whether a general-purpose process operating on defect records builds the extension; (iii) whether that extension is a faithful component with the world's kind-signature, not a patch; (iv) whether the defect representation is really on the route — the scramble test; (v) whether the built machinery then becomes latent for the next round.

## 2. The base organism

**A0** = `slots=2, persist(τ=∞, r=5, j=no)` — the architecture experiment 1's occlusion world selected. Its slots move by pass-through kinematics with reflecting walls and are independent of each other. A0 is held fixed; only rules are added to it.

## 3. The world with a new feature

Same line of 6 cells, 2 things, velocities in {−1, 0, +1}, same sensory field (occupancy, no identity, no velocity). Things always have **distinct positions**. One new law:

**Elastic collision.** Each step, first compute each thing's kinematic next-state (n_i, w_i) by the same reflect-and-move rule as before. Then, if n_1 = n_2 (would land on the same cell) or (n_1 = p_2 and n_2 = p_1) (would pass through each other), the two things **stay where they are and exchange outgoing velocities**: thing 1 takes w_2, thing 2 takes w_1. Otherwise each moves to its next-state. Head-on things bounce apart; a moving thing hitting a stationary one stops and sets it going (Newton's cradle). The world is therefore exactly "kinematics, then a pairwise rule on the kinematic next-states" — the same shape as the rule language.

This is a **pairwise interaction**. Nothing in G0 has one: every G0 slot updates independently. That is what makes G0 closed to it, if it is.

Changes (contract): identity, displace(thing, cell) where the cell is not the other thing's, set_velocity(thing, v). Applied at step 3. Run length 9, scored from time point 2. Configurations: unordered pairs of (cell, velocity) with distinct cells: **135**. Exposure/evaluation split by configuration index as before. Every fitness figure is on the evaluation half.

Phase 2 (section 8) adds a second new law to the same world: **sticky walls** — a thing whose kinematic next-state would flip its velocity (a wall hit) instead stays at its cell with velocity 0.

## 4. The meta-grammar: what a rule can be

A rule is `IF condition THEN action`, checked on the slot pair (i, j) in both orders, **before** kinematics on each step.

- Terms: for each slot, its cell `c`, velocity `v`, and its own kinematic next cell `n` and next velocity `w`: `c_i, v_i, n_i, w_i, c_j, v_j, n_j, w_j`. Eight terms; no constants. (A wall hit is `v_i != w_i`, so phase 2's law is expressible without constants.)
- Atom: `T1 == T2` or `T1 != T2` over unordered term pairs: 56 atoms.
- Condition: an atom, or two atoms joined by AND or OR: **3,136 conditions.** Depth two — no deeper.
- Action: one of `swap_next_v` (take the other's outgoing velocity), `swap_v`, `reverse_both`, `reverse_i`, `reverse_j`, `stop_both`, `stop_i`, `stop_j`, each with `hold` (do not move this step) or `move`: **16 actions.** `swap_next_v` and `swap_v` differ only when a wall bounce and a collision coincide; the data must choose between them.
- **50,176 rules.** An architecture may carry up to **K = 3** rules, applied in order.

The world's collision law needs two rules in this language (same-target and crossing are different conditions, and the language cannot OR three atoms). That is deliberate: building it takes two rounds.

## 5. Three processes

All three start from A0 and may add up to 3 rules. All three see the exposure half. All fitness is on the evaluation half.

**C — construction.** Round *r*: run the current architecture on the exposure half; collect **defect records** V = {(slot state before the step, predicted field, true field)} for every wrong prediction and **non-defect records** N for every right one. Induce a condition: score every condition in the language by (number of V states it is true on) − (number of N states it is true on); keep the top 20. Solve an action: for each kept condition and each action, count the V records it fixes (apply action to the state, run kinematics, prediction now equals the true field) minus the N records it breaks. Take the best (condition, action); ties to the fewer-atom condition. Append. Repeat until no V remain or 3 rules. **C never computes an aggregate fitness. Its only inputs are itemised records.**

**B — blind selection over the meta-grammar.** Round *r*: mutation–selection over single rules (population 32, elitism 4, 60 generations, seeds 0–5); fitness = **exposure-half** fitness of the current architecture plus the candidate rule. Append the best. Repeat for 3 rounds. **B never reads a defect record. Its only input is a number per candidate.**

**S0 — selection within the closed grammar.** Every G0 architecture evaluated on the collision world. Best of 208. No rules. This is what experiment 1's process can do when the world has a feature its grammar lacks.

## 6. Checks before freezing

1. **Expressibility.** Hand-build the two collision rules in the language, add them to A0, and confirm fidelity on collision-type steps is at or near the sensory ceiling for those steps. If the language cannot express the law, revise.
2. **Closedness**, in two parts. *Structural:* the best slot-only architecture in G0 is below A0 + hand-built rules on collision steps by at least 0.1 — no G0 machinery can do what a pairwise rule does. *Overall:* the best G0 architecture of any kind is below A0 + hand-built rules overall by at least 0.1. G0's lookup pathway is reported on collision steps but not thresholded there: it memorises local sensory patterns ("two adjacent blobs approaching → they stay") and can approximate the law's visible effects without representing it.

## 7. What is measured (phase 1)

Every measurement on the evaluation half.

**M1 — fidelity.** For A0, best-of-G0, A0+C, A0+B (each seed), A0+hand-built: overall, and split into **collision steps** (a collision occurred in the true world at that step) and **non-collision steps**.

**M2 — protected obligation.** Non-collision fidelity of A0+C versus A0. Adding rules must not cost what A0 already had.

**M3 — kind-signature of the built component.** Experiment 1's translated-edit test on the collision world: bind slots to things at step 2, apply the translated change, and check every slot tracks its thing's (position, velocity) through every later step *including through collisions*. For A0 alone and A0+C. Reported as fraction passing given bound.

**M4 — the scramble test.** Give C the exposure half's defect records with the **true-field column permuted** among the V records (same states, same number of defects, same aggregate; wrong pairings). Build. Measure M1. Give B the same world — it never reads V — and confirm its output is byte-identical to the unscrambled run. **This is the test that distinguishes the provenances.**

**M5 — recoding invariance of C.** (a) Reverse the order of V and N records. (b) Relabel slots i↔j throughout. Build. The rules must be identical (up to the relabel).

**M6 — route ablation of C.** Give C an empty V. It must build nothing. Give C V with the true field replaced by the predicted field (no defect content). It must build nothing or rules with zero net.

**M7 — structure.** The actual rules C builds and B finds, written out. Whether they are the world's law, an equivalent, or something else that fits this contract.

**M8 — cost.** Rounds and records C used; evaluations B used to reach comparable fidelity.

## 8. Phase 2 — does what was built become latent?

Run only if phase 1's supporting outcomes hold. A second new law is added to the world: **sticky walls** — a thing that would leave the line stops at its current cell with velocity 0, instead of reflecting. Collisions remain.

Start from **A0 + C's phase-1 rules** (kept, not rebuilt). Run C for up to 2 further rounds on the new world. Measure: does it build a wall rule; are the collision rules still firing correctly (collision fidelity unchanged); does total fidelity beat A0 + phase-1 rules on the new world.

## 9. Pre-registered outcomes

### Supports (construction is real, needed, and distinct from selection)

- **S1 — needed.** A0+C > best-of-G0 on collision steps. The closed grammar could not do it; extending it did.
- **S2 — protected.** Non-collision fidelity of A0+C ≥ A0's, within 0.01.
- **S3 — faithful.** M3 given-bound for A0+C ≥ 0.9 on collision-containing pairs, and far above A0 alone. The built rules are components with the collision's signature, not a fix for the observed cases.
- **S4 — on the route.** Scrambled-V construction is worse than unscrambled on collision steps by at least 0.1, and B's output under the scramble is byte-identical to B's without it.
- **S5 — provenance is not output.** B reaches collision fidelity within 0.05 of C in at least 4 of 6 seeds. Same machinery, different route.
- **S6 — content, not carrier.** M5 rules identical; M6 builds nothing.
- **S7 (phase 2) — accumulates.** A wall rule is built; collision fidelity after phase 2 within 0.01 of before; total fidelity on the sticky world beats A0 + phase-1 rules.

### Sinks

- **K1.** Best-of-G0 ≥ A0+C on collision steps. G0 was not closed; nothing was extended. Kills "needed" for this world.
- **K2.** Scrambled-V construction within 0.05 of unscrambled. The constructor is not using defect content; the witness is fake. Kills the provenance distinction as modelled.
- **K3.** C's collision fidelity stays below 0.7 × the collision-step ceiling while B's reaches it. The defect-driven route is inferior to blind search. Kills this constructor, not the concept.
- **K4 (phase 2).** Building the wall rule drops collision fidelity by more than 0.05. Construction does not accumulate.

### Findings either way

- **F1.** C and B reach the same fidelity with structurally different rules. By Derivation 2 they are one kind on this contract; extending to 7 cells or 3 things says whether they come apart.
- **F2.** C needs more rounds than K = 3. Report residual defects by cause.

### Out of scope, on purpose

- Escaping the regress. The meta-grammar is fixed. What grew is G0.
- Constructing new **representations** (the binding of sensation to slots is fixed) or new **questions** (Derivation 5). Those are the next experiments, if this one holds.
- Anything about a brain.

## 10. What is fixed and what is free

**Fixed:** sections 2–5, 7, 8, 9. **Free, fixed in code and hashed:** tie-breaking order among equal-score conditions; the mutation operator of B; the record format. **Not permitted after freezing:** changing anything fixed; adding a measurement; reclassifying an outcome.

## 11. Order of work

1. Code, with plain-word names and a note at the top.
2. Section 6 checks. Stop and revise if either fails.
3. Fingerprint this file and the code together; record in file 14.
4. Phase 1: all of section 7.
5. Classify against section 9. Phase 2 only if S1–S6 hold.
6. Raw results to file; add to the project story.

## 12. Changes before freezing

1. **B's fitness is on the exposure half, not the evaluation half.** As first written, blind selection would have been scored on the same configurations it is later measured on — peeking at the test set — while construction only ever saw exposure records. Both processes now see only the exposure half; both are measured only on the evaluation half.
2. **A pre-registered expectation added after thinking the world through, before any code ran.** When two things meet head-on in adjacent cells, "they bounce" and "they pass through each other" produce the *same* occupancy fields at every step — the identity swap is invisible to sensation. So C, which builds from sensory defects, is **expected not to build the crossing rule**, because there are no defects from crossings; only same-target collisions (things would land on one cell) produce visible defects. This is Derivation 2 in the construction setting: the constructor should build exactly the kinds its contract can see. Consequences for the outcomes: S3's threshold applies to pairs with **no crossing after the change step**; pairs with a post-change crossing are reported separately as **F3 — the invisible law**, and are expected to fail M3 for A0+C while passing for A0 + hand-built rules. Had this not been written down now it would have looked like an excuse later.
3. **The world's walls redefined.** As first coded, a thing reflecting off a wall into its neighbour's cell was handled by a special "hold" clause. The section-6 check showed this edge case was 16% of all collision-type events, inexpressible in the rule language, and left two slots on one cell so that the next several predictions failed — while the hand-built rules were 100% correct on every collision that occurred before any such event. The world is now defined as kinematics first, then the pairwise law on the kinematic next-states; the edge case is then just a same-target collision. The rule language's terms are the slots' own kinematic next-states, so world and language have the same shape. One action added (`swap_next_v`); the two constants removed. 50,176 rules instead of 43,904.
4. **Closedness check split.** As first written it applied a 0.1 margin to *any* G0 architecture on collision steps. The best G0 architecture on collision steps turned out to be the lookup table at 0.819 (hand-built rules: 0.906; ceiling: 0.923) — a memoriser of local patterns, not machinery. The margin was meant for machinery. The check now has a structural part (slot-only G0 on collision steps) and an overall part (any G0, all steps); the lookup's collision figure is reported as is. Recorded with the numbers so the reader can judge whether this is a fair restatement or a moved goalpost: A0 alone 0.352; best slot-only G0 0.366; lookup 0.819; hand 0.906. Both parts pass.
