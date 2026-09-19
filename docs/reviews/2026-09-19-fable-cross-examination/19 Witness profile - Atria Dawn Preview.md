# 19 Witness profile — `Atria-Dawn-Preview` as a hostile referee

What this file is: the same record for the second witness. Same system prompt, same battery, same documents, one to two samples per item. Numbers from `witness-replies/usage_summary.json`; rulings from file 15 §F. Scope as in file 18. Final count: 25 of 26 items answered with content; one (D2, the experiment 2 code review) returned nothing even under streaming.

## 1. Throughput and cost of use — and a correction

| Condition | What happened |
|---|---|
| Output cap 24,000 | Every reply empty: all reasoning, no answer. |
| Output cap 100,000 | Rejected by the endpoint. |
| Output cap 65,536 (the model's maximum) | 22 usable replies of 25 attempted. Median reply 16,800 characters (max 30,500); median reasoning 15,500 tokens (max 26,000); median completion 18,800 tokens. |
| Time per successful attempt | Under 300 seconds in every case. Medians of 239 seconds include time lost to failed earlier attempts. |
| Failures | Three items failed four times each with "remote end closed connection without response". Each failed attempt lasted 306 seconds to within a tenth of a second, so a single attempt is cut at about 300 seconds, at the provider or at the gateway between us — not resolved. An item whose reply needs more than that fails deterministically; retrying does not help. |
| Concurrency | Four workers, then seven more in a second process after the user said the limit is 60 requests per minute; no rate errors. The earlier "invalid API key" errors were a burst limit at the first launch and did not recur. |

**Correction.** Earlier in this session I told the user that an Atria reply takes about thirty minutes. That was wrong. It was the visible wall-clock of a four-worker queue in which failed items each held a worker for 21 minutes (four attempts of 306 seconds plus back-off). A successful reply takes two to five minutes. The right way to run this model is all items at once, with streaming so that the connection is kept alive past the 300-second cut. Streaming was added to the harness after this was found: the eight items that had failed four times each came back in 9 to 10 minutes, all but one.

Reasoning is roughly one and a half times the visible answer — much less than Flash's ratio. Its cap is half of Flash's, and it needs about half of it.

## 2. Where it was strong, and under what conditions

**Constructing counterexamples inside the formalism, when given the semantics alone.** (F-A3, F-A5, F-A6.) It built the global-anchor exploit concretely — a one-component E whose relation is the target's own solution set, anchored to the whole target — and showed it passes every condition on every contract, so that "the anchor must be a decomposition" (my concession to Flash's read-only-memory case) is not enough. It showed that "selected" is satisfied by every transport (singleton population, identity operator, empty history), that requiring a non-empty history still admits the baseline pair, and that only a *discrimination* requirement fixes it. It noticed that the semantics individuates transports by history while refusing to individuate components by history, and that no reason is given. Condition: a document that is a formal system; the model treats it as one and looks for models of the axioms, where Flash looked for type errors.

**Finding what is absent.** (F-A4, F-A6.) Symmetry explanation is not in Part VII and cannot be anchored without importing the explanandum; selection-artefact explanation needs two targets; concept creation (a new dimension of variation) is outside question-finding as defined; "physically admitted" is undefined for the mathematical example. Flash attacked what was on the page; Atria attacked what was missing from it. Condition: prompts that asked "what cannot be represented" (A4, A6) — the same prompts on which Flash gave its least useful replies.

**Recomputing the arithmetic before ruling.** (F-B2 F18, F-B4 #18.) It recomputed the change counts, sequence counts, split sizes and weighted averages from the tables and reported that they reconciled, then said its problems were "in design, inference and reporting". Flash never did this. Condition: numeric tables in the document; Atria checks them, Flash reasons about them.

**Re-attributing a result from the document's own data.** (F-B4 #8.) File 12 §7.1 said the jump-versus-turn kind was decided by thing count. Atria pointed out that H_passive — two things, identity changes only — already selects the same value, so the variable is the source of jumps, not thing count, and the document's own table shows it. This was checkable and right, and more informative than the sentence it replaced. Condition: it reads the whole results table against each claim, not only the quoted passage.

**Precision of wording about what a result is.** "The selecting factor is a property of the sensor, not of the world's history" (F-B4 #4) replaced my headline wording. "Not evaluable by the changes in C" for "unevaluable" (F-A7 #1). "Biased by design" for "guaranteed to succeed" (F-C4 #9). Condition: it corrects overstatement in both directions, including the referee's own.

**Less repetition.** With one sample per item and longer, structured replies (part A audit, part B findings, part C verdicts), it repeated less across items than Flash did across samples. It also marked when a finding was "the sharpest" and when a finding was "no finding here".

## 3. Where it was weak, and under what conditions

**It fails on the longest items unless streamed.** Eight items (A8, B1, B3, D1, D2, D4, D7, and D8 on one of two runs) needed more than the 300-second window and died four times each under a plain request. Condition: two long documents, or a task that needs the whole document held at once — exactly the items where its style is most valuable. With streaming, seven of the eight came back (9 to 10 minutes each). The fix was on our side; the one remaining loss (D2) was the model's: no visible content at its cap.

**Code claims that are right in the letter and wrong in effect.** (F-B5 #10.) It read that the forgetting counter is reset only on re-binding, never on confirmation in place, and concluded the τ = 2 and τ = 5 results were perturbed. The reading was correct — the implemented rule is cumulative-since-snap, not consecutive — and its own scenario (a slot confirmed with the counter already above τ) cannot occur, because the drop runs every step. Patched and rerun: nothing moved by more than 0.0035. Condition: reasoning about dynamic behaviour from static code; it does not simulate.

**One sample is one sample.** Where I have two Atria samples (A1, A2), the second added real findings the first did not (Org_ℓ as relation; ≺_h; Derivation 4's contract slip). Every single-sample item is therefore probably incomplete. Condition: budget; a second sample costs another five minutes of generation but, at the 300-second cut, also another chance to fail.

**Long formal replies cost reading time.** A 30,000-character reply with LaTeX in every line took me longer to adjudicate than three Flash replies. The density is real, but so is the cost.

**On the experiment code it is Flash's equal on facts and weaker on effect.** B3 (recovered) found the same crippled lookup, the half-implemented adequacy check and the code-forced tie that Flash found, plus the order-dependent tie-break in the controls. But two of its code claims that sounded decisive were right in the letter and wrong in effect (the cumulative counter; the 'dropped sequences', which are the per-configuration change rule), and D2 was lost. Flash's code claims were more often right in effect; Atria's were more often stated with the mechanism.

## 4. Errors it did not make

It made two numeric assertions that turned out false, both on the experiment items and both late: that the "needed" margin rests on about eight predictions (it rests on about 121), and that the M3 crossing denominators do not reconcile (it read the wrong column). On the semantics it made none. It did not misread a pre-registered narrowing as concealment. It did not repeat the "byte-identical B" point more than once per reply. When it built a counterexample it wrote it out in full so it could be checked (F-A3 #1 is a page of construction).

## 5. Agreement with the first witness, which is the point

On the semantics the two witnesses reached the same list independently: the representation/construction cycle, the hidden decomposition parameter, the anchoring steelman winning on the full physical contract, Derivation 1's corollary as question-begging, Derivation 2 false as stated, Derivation 3's missing richness hypothesis, the contract needing declared counterfactuals, Sel trivialisable. Two models with different training and different styles converging on the same holes is evidence about the text. Where only one found something, it was Atria on the formal counterexamples and the absences, and Flash on the code and on the adjudicator.

## 6. How to use it next time

All items launched at once (the limit is 60 requests per minute, not four workers); streaming to survive the 300-second cut; two samples on theory items, one on experiment items; the "what is absent" and "build a counterexample" prompts given to this model first; its numeric claims trusted more than Flash's but its dynamic-behaviour claims about code run before they are believed.
