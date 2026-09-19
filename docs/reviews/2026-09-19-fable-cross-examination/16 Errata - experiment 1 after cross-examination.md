# Errata: experiment 1 (files 11, 12) after adversarial cross-examination

**Why a separate file.** Files 11 and 12 were frozen and fingerprinted; they are not edited. Corrections go here, with the numbers that back them. Every item was raised by an external witness (file 15, sections B2, B4, B5) and checked by me against the frozen design, the frozen code, and the raw results (12c). Nothing here is a new experiment.

---

## 1. "Pre-registered" overstated what was done

Design §4 says the outcomes were "written before any code was run, and not changed after." That was true of the first draft and false of the frozen document. Three control runs were made before freezing, **on the same histories later used for the main run**, and outcomes and checks were amended after them (design §9, changes 8, 11, 13–19). The correct description is **frozen after pilots on the same data**. All changes were recorded, and the first pilot already showed the direction of the final result — but that is a weaker claim than pre-registration and should have been stated as such.

A referee's fair verdict on the 21 changes (file 15, B2.10): acceptable as design choices — 1, 3, 4, 5, 6, 9, 10, 12, 20, 21; acceptable only as pilot-informed — 7, 8, 13, 14, 15; **not acceptable as pre-registered** — 16, 17, 18, 19. (Changes 2 and 11 were left out of this list at first; both are design choices whose rationale later proved wrong — §12 and §13 — so they belong with the pilot-informed group.) Items 3–5 below give the numbers under the criteria as they stood before those three.

## 2. "τ = 0 winning H_neutral" (change 16) contradicts "tied exactly" (change 19)

They tied. The control's best-of returned the first maximum in enumeration order, which happened to be τ = 0. Wording error; the values were equal to the last digit (0.8930555…).

## 3. Neutrality under the original definition of the kind under test **fails**

Design §2.6 defined the kind under test as "the τ gene and the `rebind` rule." Change 19 restricted the neutrality check to the τ family after `rebind` sat below. Both results, from the raw table:

| Persistence value | Best fitness on H_neutral |
|---|---|
| rebind | 0.8667 |
| τ = 0 | 0.8931 |
| τ = 2 | 0.8931 |
| τ = 5 | 0.8931 |
| τ = ∞ | 0.8931 |

Original definition (rebind included): spread 0.0264 — **fails** the 0.01 tolerance. Amended definition (τ only): spread 0.0000 — passes. The analysis behind the amendment (rebind's deficit is that it re-infers velocity from scratch every step and so cannot keep velocity through a teleport, which is not persistence) still seems right to me; but it was made after the number, and a reader is entitled to the failing figure.

## 4. Adequacy under the original criterion: the H_full grammar **failed** (first written as "underpowered"; the audit was right that this was a softer word)

Design §4 originally said: "No slot architecture reaches 0.95 × the sensory ceiling on H_full → the grammar cannot express an adequate predictor; record the attempt as failed." Change 18 dropped that criterion after the number was seen. The number: top architecture 0.8009, ceiling 0.9086, ratio **0.881 < 0.95**. Under the criterion as originally written, before the post-pilot changes, the H_full attempt is recorded as underpowered, and every H_full result in file 12 should be read with that. The diagnosis (the gap is the change step and co-located starts, invisible to any sensory predictor) may well be right; it should have led to a re-freeze, not a dropped threshold.

## 5. The exposure/evaluation split was added after seeing the lookup memorise

Change 17. Both figures: on train = test the k = 3 lookup scored 0.820 on H_full; held out, 0.656. The tracker scored 0.801 on both. The split is methodologically necessary and does not change which persistence value wins any history; it changes whether lookup tables compete at all. It is nonetheless post hoc and is recorded as such.

## 6. "Has thing-kind" was claimed on a conditional figure against an unconditional definition

Design §3: an architecture has thing-kind "when this holds for every configuration and every change." Results §4 reported the fraction *given bound*. The unconditional figures for the H_full winner: **0.801 passing over all 4,104 pairs; bind rate 0.801; given bound 1.000.** Under the frozen definition, **no architecture has thing-kind.** The honest reading (file 15, B5): M3 tests *preservation* of a binding through a change, not its acquisition; the two quantities are reported separately above and the unconditional one fails.

## 7. The headline must be conditional, and §7.3 was a retraction, not a footnote

Results: "History determined which kind got expressed, exactly as the diagnosis said." On H_neutral it did not: the four τ values tied and the evolutionary seeds landed on τ = 2, ∞, 2, 5, 2, 5 by drift. Corrected statement: **history determines the kind when it contains the discriminating change; when it does not, it underdetermines, and drift decides.** That is a correction to your point 3 as stated, and file 12's §7.3 ("a role for chance the diagnosis did not mention") should have said so.

## 8. The neutral tie is definitional; the against-selection is not

τ governs unconfirmed slots. H_neutral has one thing and nothing hidden, so every slot is confirmed every step and τ is inert — the tie was entailed by the definition of the history. And H_full is the only history with prolonged non-confirmation, and persistence the only mechanism in the grammar for it — "the required mechanism is selected when required." Both witnesses are right (file 15, B4.1–2).

What is *not* definitional and survives: on H_passive and H_kinematic — two visible things, nothing hidden — **persistence was selected against, strictly** (only τ = 0 in both selected sets). That is an empirical fact about phantoms at crossings, not a consequence of any definition. And among the tied H_neutral architectures, τ = ∞ scores 1.000 on occlusion it never saw and τ = 0 scores 0.535: what you happen to carry determines what you can later do. Those two are the content of experiment 1.

## 9. The rival was a strawman

Design §1: "Under the rival, [kind-preserving structure] appears regardless." A correspondence theorist can hold that kinds are prior *and* that a parsimonious predictor omits persistence when nothing is hidden. The experiment tested the diagnosis's positive prediction; it did not have a differential prediction against a well-formed rival. Experiment 1 is a relative-consistency witness for the diagnosis, which is what file 12 §8 already said, and nothing stronger.

## 10. Thing count and occlusion are confounded in the H_neutral-vs-H_full contrast

One thing / no occlusion against two things / occlusion. The clean contrast is **H_kinematic vs H_full** — same two-thing world, same change types except occlusion and the fitness-inert swap: H_kinematic selects only τ = 0, H_full selects only τ = ∞. The occlusion conclusion stands on that pair. A one-thing-with-occlusion history should have been included.

Consequently results §7.1 (the *j* gene "selected in opposite directions") is confounded by the same pair and is withdrawn as a finding; it stays as a hypothesis for a factorial design.

## 11. Search bias: inconclusive, not "did not fire"

Six seeds on H_neutral, none landing on τ = 0 although τ = 0 is one of four tied values. Chance of that under no bias ≈ 0.18. The run is underpowered to detect bias either way.

## 12. The occlusion rationale was wrong in the design

Change 2 says a 3-cell window "hides [a thing] for at least three steps, beyond k = 3." Computed over all configurations and windows, hidden spells last 1 step in 17% of cases, 2 in 20%, 3 in 34%, 4 in 5%, 5 in 10%, 7 in 15%. **71% of spells are three steps or fewer**, which a k = 3 lookup could in principle bridge. The lookups did in fact lose on occlusion (0.36–0.46 against 0.94 for τ = ∞), but not for the reason the design gave; the reason is that the sensory prefix at re-emergence is ambiguous across configurations, which a held-out split exposes.

## 13. Smaller corrections

- Change 6 still says "112 architectures"; it is 208 after change 14: lookup-only 3, slot-only 17 × 3 = 51, both 3 × 51 = 153, nothing 1.
- Change 11 calls the corrected ceiling "the true bound"; §2.5 correctly calls it in-sample. It is in-sample.
- Swap is fitness-inert (the sensory field and true occupancy are unchanged); it only matters for M3. Listing it among H_full's selective changes was misleading.
- "Selection with unlimited reach" (§2.8) is argmax over a fixed grammar, not variation and selection.
- Full M4 and per-change-type M3 are in the raw results (12c); the results document summarised.

## 14. What experiment 1 now claims — SUPERSEDED by §17 (kept because the audit in file 15 §E quotes it)

In one grammar of 208 predictors and four histories: a persistence parameter is inert where nothing is hidden (by definition), selected against where two visible things interact (empirically), and selected for where things are hidden (as the grammar's only mechanism for it). Tied architectures on the neutral history differ two-fold on occlusion never seen. Frozen after pilots on the same data, with three changes a referee would not allow as pre-registered. Underpowered on H_full under its own original criterion. A relative-consistency witness for the diagnosis, and not a differential test against a well-formed rival.

## 15. Is the H_full winner fragile? (checked after the B1 witness asked)

The tracker that never forgets (τ = ∞) beat the tracker that forgets after five steps (τ = 5) by 0.003 on the evaluation half of H_full, and a witness said selection by an exact maximum on one finite half could flip under a different half. Checked by `exp1/diagnostic_fragility.py` on the unchanged frozen code: score both trackers per configuration, count who wins where, bootstrap the configurations 2,000 times, and repeat on the other half of the split.

| Half | Configurations | τ = ∞ | τ = 5 | Gap | τ = ∞ better on | τ = 5 better on | Tied | Bootstrap share with τ = ∞ ahead |
|---|---|---|---|---|---|---|---|---|
| Evaluation half (as frozen) | 85 | 0.8009 | 0.7982 | 0.0027 | 38 | 14 | 33 | 0.999 |
| Exposure half (the other split) | 86 | 0.8012 | 0.7975 | 0.0038 | 40 | 10 | 36 | 1.000 |

The gap is small but systematic: never-forget wins on about three configurations for every one it loses, on both halves. The witness's concern was legitimate and the check should have been in the frozen design; the selection stands. Note that this does not touch the other B1 finding, that for slot architectures the evaluation half *is* the selection set — that remains true, which is why the other half was scored as well.

## 16. Five code findings from the cross-examination, checked on the frozen code — one of them changes the headline

The B3 witnesses read the code and made claims I could test. `exp1/diagnostic_code_findings.py` imports the frozen code unchanged and checks each (`exp1/results_out_code_findings.json`).

**(a) On the one-thing history the forgetting parameter can never act, so the four-way tie was forced by the code.** The trackers that tied on H_neutral all have search radius 5, which spans the whole six-cell line. With that radius the one thing is always re-bound in the same step it moves, the slot's "unconfirmed" count never rises above zero, and τ (which only acts when the count exceeds it) is never consulted. Count of steps with any unconfirmed slot on the evaluation half: radius 5 — **0 for every τ**; radius 2 — 28, 48 and 54 for τ = 2, 5, ∞. With radius 2 the τ family's predictions differ; with radius 5 they are byte-identical. So "history H_neutral cannot tell the trackers apart" was true, but for a reason in the code, not in the world: the best architecture on that history happens to be one where the kind under test is switched off. The tie is a consequence of the architecture grammar, which is a weaker thing than the design claimed.

**(b) The τ family's predictions are identical, not merely equal in score, on H_neutral at radius 5.** This is the one thing the tie was entitled to mean: on that history the four are one kind by the signature definition, because no admitted change separates their behaviour. It holds — for the reason in (a).

**(c) M2 on H_full is the same number as M1 on H_full for all 208 architectures.** The "full contract" for two things is built from exactly the change set of H_full, so the second measurement is the first one again. File 12 treated them as two lines of evidence for the two-thing case; they are one.

**(d) The swap change is bit-for-bit the same sequence as the identity change** in all 171 two-thing configurations. Swap exists only for the thing-signature test, where it is applied to the predictor's binding. In fitness it doubled the weight of "nothing happens".

**(e) A fair memoriser ties the tracker.** The frozen lookup baseline was crippled four ways: it used only the last k fields with no fall-back to shorter keys, predicted an all-zero field whenever the key was unseen, kept the last continuation seen rather than the commonest, and could not see a sequence's start. With fall-back, majority vote and the commonest field as default, built on the exposure half and scored on the evaluation half of H_full:

| Predictor | Prediction accuracy on H_full, evaluation half |
|---|---|
| Frozen lookup, k = 3 (as in file 12) | 0.656 |
| Fair lookup, k = 1 | 0.169 |
| Fair lookup, k = 2 | 0.764 |
| **Fair lookup, k = 3** | **0.801** |
| **Slot tracker, τ = ∞ (the winner in file 12)** | **0.801** |
| In-sample maximum from sensation | 0.909 |

The gap of 0.145 that file 12 reported between the tracker and the best memoriser is an artefact of the baseline. A three-field memoriser with ordinary fall-back predicts this world as well as the tracker that never forgets, on held-out configurations. **Consequences.** The adequacy check ("best slot-only beats best lookup-only") is not met against a fair baseline. The claim that H_full *selects* the thing-tracker over memorisation is withdrawn: on prediction alone, this world does not prefer a tracker to a memoriser. What survives is narrower: *among architectures that carry slots*, the history with occlusion selects the one that never forgets, and only the translated-edit test (M3), which a memoriser cannot even enter because it has no slots to bind, separates tracker from memoriser. Whether that survivor deserves the name "thing-kind" is then a question about M3, which §5 of this file already narrowed to preservation given binding.

Also confirmed from the code without running anything: the adequacy check was half-implemented (the 0.95-of-ceiling clause is computed but never enters the pass/fail); the thing-signature function returns passed over all pairs, while file 12 quoted the given-bound figure, which is not a number the code emits; and the exposure/evaluation split by configuration index is a parity checkerboard on (cell, velocity) for the one-thing world, not a random split.

## 17. What experiment 1 now claims (replaces §14; revised after the audit of this file, file 15 §E)

Every sentence below carries its concession.

- **Process.** The design was frozen after pilots on the same data, and the first pilot already showed the direction of the final result. Four of the twenty-one pre-freeze changes (16, 17, 18, 19) would not be allowed as pre-registered by a referee; the design and all figures are fingerprinted only at freezing, so the artefact cannot prove the timing of any change.
- **Neutrality.** Under the kind as originally defined (persistence, including the rebind rule) the one-thing history is *not* neutral: spread 0.026 against a tolerance of 0.01. Under the amended, τ-only definition the spread is exactly zero — and it is zero because, at the search radius that wins on that history, the persistence parameter is never consulted (§16(a)). The tie is a fact about the architecture grammar, not a finding about the world.
- **Adequacy.** Under the original criterion (best slot-only within 0.95 of the ceiling on H_full) the attempt **failed** (0.881 of an in-sample ceiling with unbounded memory); "underpowered" was a softer word for the same fact. Against a fair memoriser baseline the tracker does not win at all: 0.801 against 0.801 on held-out configurations (§16(e)). The frozen "slot beats lookup" result was an artefact of a crippled baseline.
- **What the exhaustive search found.** "Selected" throughout means *highest score under exhaustive search of 208 architectures*, not variation and selection. Among slot-carrying architectures, the history with two visible things scored the forgetting tracker highest (an empirical ordering), and the history with occlusion scored the never-forgetting tracker highest by a small, systematic margin (§15) — which is close to definitional, because persistence is the grammar's only mechanism for a hidden thing (§8). The clean contrast for occlusion is H_kinematic against H_full; the H_neutral-against-H_full contrast confounds thing count with occlusion (§10). The design's stated reason for why occlusion needs persistence was wrong: 71% of occlusion spells are three steps or shorter (§12); the crippled lookups lost on occlusion for a different reason (ambiguous re-emergence prefixes), and a fair lookup does not lose.
- **Thing-kind.** Under the frozen unconditional definition **no architecture has thing-kind** (§6). Under the conditional definition (tracking given binding), the never-forgetting tracker keeps its slots on their things through translated changes, and the test is a persistence test: it applies the change to the slots and asks whether the shared kinematics keep them aligned, which for τ = ∞ is close to a fixpoint (file 15 §B3.5). It says nothing about acquisition.
- **Headline, corrected.** History determines the kind when it contains the discriminating change; when it does not, it underdetermines, and drift decides — *within a grammar that already contains a perfect tracker, and only among architectures that carry slots*. On prediction alone this world does not prefer tracking to memorisation.
- **Not shown.** Search bias (the six-seed run is underpowered either way, §11). Any generalisation beyond persistence in this world. Anything about kinds being inputs or outputs. Any instantiation of a definition in file 10.
