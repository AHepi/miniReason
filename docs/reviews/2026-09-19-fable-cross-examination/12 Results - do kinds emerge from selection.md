# Results: do kinds emerge from selection, or must they be supplied?

**Status: run once, after freezing. Design and code were fingerprinted together before this run; nothing in the design or code was changed afterwards.**

| File | Fingerprint (SHA-256) |
|---|---|
| Design (file 11) | `a7683c1c878c15f77e30db15ae55f9d80f94d2808992b28bbda50029b41566c1` |
| Code (12a) | `54259a930169556686331c5b1fe50778cf346edab0dce4acfde674f2d22c6d6f` |
| Raw results (12c) | `45ee13c703200bca67c99543d9bdf0bd827a89e7d7ec5b3ef2efed0f143d77cf` |

Frozen at 2026-09-18 15:55 UTC. Full run took 2 minutes 22 seconds. Every number below is exact — every configuration, every change, every architecture enumerated; no sampling in the primary result.

---

## The answer in one paragraph

**History determined which kind got expressed, exactly as the diagnosis said.** A world where nothing is ever hidden did not select for persistence at all — trackers that forget and trackers that never forget tied to the last decimal. A world with two visible things selected *against* persistence. Only the world with occlusion selected the tracker that keeps a thing alive when it can't see it — and that tracker, opened up and tested piece by piece, had components that respond to every allowed change exactly as a thing does, in every case where it had managed to lock on. The blind search landed in the same places the exhaustive table did. The sinking condition did not fire. One thing the design did not predict also showed up, twice: a *second* kind — whether a sudden jump means "teleported" or "changed direction" — was also selected by history, in opposite directions in the one-thing and two-thing worlds.

---

## 1. What was run

| History | World | Changes in it | Sequences (exposure / evaluation) |
|---|---|---|---|
| H_neutral | 1 thing | identity, displace, set_velocity | 90 / 90 |
| H_passive | 2 things | identity only | 86 / 85 |
| H_kinematic | 2 things | identity, displace, set_velocity | 1,634 / 1,615 |
| H_full | 2 things | all 24, including occlusion and swap | 2,064 / 2,040 |

208 architectures, each evaluated on all four histories and on the full contract of its world. 51 slot-only architectures put through the thing-signature test (4,104 configuration–change pairs each). Six evolutionary runs on each of three histories.

Sensory ceilings on the evaluation halves (best possible from sensation, in-sample): H_neutral 0.914, H_passive 0.997, H_kinematic 0.902, H_full 0.909.

## 2. What each history selected

"Selected" = fitness-maximal on the evaluation half of that history.

| History | Top fitness | Selected architectures | Persistence (τ) of the selected |
|---|---|---|---|
| **H_neutral** | 0.8931 (98% of ceiling) | 12: slots ∈ {1,2,3} × τ ∈ {0, 2, 5, ∞}, all r=5, all *j*=yes | **all four values tie exactly** |
| **H_passive** | 0.9735 (98%) | 8: slots ∈ {2,3}, τ=0, r ∈ {2,5}, *j*=no, with or without a lookup that adds nothing | **τ = 0 only** |
| **H_kinematic** | 0.8176 (91%) | 1: slots=3, τ=0, r=5, *j*=no | **τ = 0 only** |
| **H_full** | 0.8009 (88%) | 1: slots=2, τ=∞, r=5, *j*=no | **τ = ∞ only** |

Lookup-only architectures were never selected on any history. The best lookup-only on H_full scored 0.674 against the tracker's 0.801, on configurations neither had seen.

## 3. How the selected architectures do on changes they never saw

M2: fitness on the evaluation half of the full contract of their world, by change type. The occlusion column is the one that matters.

| Selected on | Architecture | identity | displace | set_velocity | **occlude** | swap |
|---|---|---|---|---|---|---|
| H_neutral | τ=0 (any slots) | 1.000 | 0.861 | 0.921 | **0.535** | — |
| H_neutral | τ=2 | 1.000 | 0.861 | 0.921 | **0.760** | — |
| H_neutral | τ=5 | 1.000 | 0.861 | 0.921 | **0.979** | — |
| H_neutral | τ=∞ | 1.000 | 0.861 | 0.921 | **1.000** | — |
| H_passive | τ=0 (all 8) | 0.974 | 0.76–0.78 | 0.87–0.88 | **0.361–0.362** | 0.974 |
| H_kinematic | τ=0 | 0.974 | 0.776 | 0.875 | **0.362** | 0.974 |
| H_full | τ=∞ | 0.968 | 0.708 | 0.838 | **0.941** | 0.968 |

On H_neutral the four τ values are indistinguishable to the history that selected them and then differ by a factor of two on occlusion, which that history never contained.

## 4. Thing-signature (M3): do the selected slots respond like things?

For each slot-only architecture: bind slots to things at step 2, apply each change in *translated* form to the slot state, and check the slot's (cell, velocity) tracks its thing's (position, velocity) at every later step. "Unbound" = the predictor was not tracking both things exactly at step 2 (mostly two things starting in one cell — one blob to sensation — so no binding could be made). The conditional column is the fraction passing among pairs where a binding existed.

| Architecture | Passing, all pairs | Unbound | **Passing, given bound** | occlude (given bound) |
|---|---|---|---|---|
| slots=2, **τ=∞**, r=5, *j*=no *(selected on H_full)* | 0.801 | 816 / 4,104 | **1.000** | **1.000** |
| slots=2, τ=5, r=5, *j*=no | 0.750 | 816 | 0.936 | 0.61 |
| slots=2, τ=2, r=5, *j*=no | 0.676 | 816 | 0.844 | 0.06 |
| slots=2, **τ=0**, r=5, *j*=no *(selected on H_passive, H_kinematic)* | 0.710 | 624 | 0.837 | **0.02** |
| slots=2, rebind | 0.020 | 1,488 | 0.03 | 0.01 |
| any 1-slot architecture | — | all | — | — |

The architecture H_full selected is the only one that passes the thing-signature test on every pair it could be tested on, including every occlusion. The architectures H_passive and H_kinematic selected fail the thing-signature test on essentially every occlusion: their slots stop being the thing the moment the thing is hidden. `rebind` has no persistent identity at all and fails everything — correctly, since it re-creates its slots from scratch every step.

## 5. The blind search (secondary)

Six seeds, 40 generations, population 32, on three histories.

| History | Seeds converging to | Note |
|---|---|---|
| H_neutral | τ = 2, ∞, 2, 5, 2, 5 (all at the tied maximum 0.8931) | spread across the tie; final populations mixed; **no bias toward or away from persistence** |
| H_passive | τ = 0 in **6 of 6** | matches exhaustive |
| H_full | τ = ∞ in **6 of 6** | matches exhaustive; final populations 8–13 of 32 on the exact selected architecture |

The search found what the table found. Reachability (your point 2) did not bite in this world, and there is no search-bias finding.

## 6. Classification against the pre-registered outcomes (design section 4)

**Supports the diagnosis** — all three bullets hit:
- ✅ On H_neutral, the best architecture for every persistence value ties (within 0.01). *They tie exactly.*
- ✅ On H_full, the top architectures all have persisting slots, and those have thing-kind under M3. *The single top architecture is τ=∞ and passes M3 on 100% of bound pairs.*
- ✅ On H_passive and H_kinematic, the selected set includes non-persisting architectures, and those fail M2 on occlusion. *The selected sets are entirely non-persisting (τ=0) and score 0.36 on occlusion.*

**Sinks the diagnosis** — did not fire:
- ❌ H_neutral's selected set does not exclude non-persisting architectures; τ=0 is in it.

**Search bias** — did not fire: evolution on H_neutral drifted across the tie with no preference.

**Fidelity and kind come apart** — did not fire as stated: M2-best and M3-best on H_full are the same architecture (τ=∞). *But see 7.2.*

**Finding either way** — did not fire: no non-persisting architecture is maximal on H_full. Lookup-only was never selected anywhere.

**Underpowered** — did not fire: adequacy passed before freezing.

## 7. Observations that were not pre-registered

These are post hoc. They are reported because they are in the data, not because they were predicted; treat them as candidates for a future frozen test, not as findings.

**7.1 A second kind was selected by history, in opposite directions.** Every architecture selected on the one-thing world has *j*=yes (a large jump keeps the old velocity: "it teleported"). Every architecture selected on the two-thing worlds has *j*=no (a large jump means new velocity: "it changed direction"). With one thing, a big unexplained jump can only be a displacement. With two things, a big mismatch is usually a slot that lost track across a crossing, and keeping the old velocity is wrong. So whether "displacement" exists as a kind distinct from "velocity change" was decided by how many things there were. Nobody declared that; the history did.

**7.2 Prediction fitness is a coarse signal for kind; component-fidelity is sharp.** On H_full, τ=5 and τ=∞ are separated by 0.003 in prediction fitness (0.798 vs 0.801), but by 0.39 on the thing-signature occlusion test (0.61 vs 1.00, given bound). A history has to be quite demanding before it can *see* the difference between "persists for five steps" and "persists" — but the difference is fully there in the components. This is Derivation 2 of file 10 in action: how fine the menu of kinds is depends on the contract.

**7.3 Object permanence by drift.** On H_neutral, τ=0 and τ=∞ tie, so nothing chooses between them; the evolutionary seeds landed on τ = 2, 5, ∞ by drift. A thinker from that world that happened to drift to τ=∞ generalises perfectly to occlusion (1.000) though it never saw one; one that drifted to τ=0 scores 0.535. The latent machinery was present in both; history did not select between them; which one you got was luck; and it determined what you could later do. That is points 1 and 3 together, with a role for chance the diagnosis did not mention.

**7.4 Persistence was selected against, not merely not-for, when two visible things interact.** H_passive and H_kinematic selected τ=0 *strictly* — persisting slots did worse. With two things crossing and sharing cells, a slot that persists through non-confirmation is usually a slot that has lost its thing, and dropping it is right. So persistence is not a free good that history merely fails to reward; in some worlds it costs.

## 8. What this does not show

- Anything about infants, animals, or programs other than this one. It is a relative-consistency witness: the two-layer picture can be built in exact form and behaves as file 10 predicts.
- That the diagnosis holds in other worlds or with other grammars. One world, one grammar of 208.
- Anything about **construction**. The grammar was fixed throughout. Every kind that appeared was latent in it from the start. The experiment shows history choosing among latent kinds; it cannot show new machinery being built.
- The thing-signature test could only be applied where the tracker had locked on (80% of pairs for two-slot architectures). The remaining 20% are mostly two things starting in one cell, which is one blob to sensation. A thing-count prior would close part of that and was deliberately not added (design change 20).

## 9. Revisions before freezing

Three rounds, all recorded in design section 9 (changes 1–21). In short: the first controls failed because I expected fitness 1.0 from predictors that cannot see a change before it lands; the yardstick was corrected to a sensory ceiling, and then corrected again when real architectures exceeded the first version of it. The lookup pathway was found to be memorising the sequences it was scored on, so an exposure/evaluation split was added. The neutrality check was found to be comparing the wrong pair (object-model vs none, instead of persisting vs not) and was corrected. Two grammar deficiencies exposed by the first run were fixed and one gene was added. A guessed numerical threshold was dropped. Then the design was frozen and run once.

None of the revisions touched what the pre-registered outcomes are about — which persistence value each history selects, and whether the selected one has thing-kind. The first control run, before any of the revisions, already showed τ=0 winning H_neutral and τ=∞ winning H_full.
