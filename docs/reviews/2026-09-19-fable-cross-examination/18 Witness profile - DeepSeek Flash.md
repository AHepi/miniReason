# 18 Witness profile — DeepSeek `deepseek-flash` as a hostile referee

What this file is: an exact record of where this model was strong and where it was weak when used as a witness against files 10–17, with the conditions under which each behaviour appeared. Every claim names its evidence. The numbers come from the saved receipts (`witness-replies/usage_summary.json`) and the adjudication (file 15). Scope: one endpoint, one system prompt (hostile referee, numbered findings, quote the passage), temperature 0.7, documents of 20–60 thousand words each, 26 attack items plus 5 audit items, September 2026.

## 1. Throughput and cost of use

| Condition | What happened |
|---|---|
| Output cap 6,000 tokens (first launch) | Every reply empty. The model spends its allowance on reasoning first and returns nothing when the allowance ends there. |
| Output cap 24,000 | 53 usable replies, 16 of them cut off mid-answer (finish reason "length"); 33 empty. Median reply 12,000 characters; median reasoning 18,000 tokens; median 100 seconds. |
| Output cap 131,072 (the model's maximum) | 24 of the 25 reruns usable, none cut off, one still empty at the cap (B1, sample 2). Median reasoning 39,000 tokens (max 62,000); median 193 seconds; max 315. |
| Audits of the adjudication (E1–E4, D8b) at the cap | 15 of 15 usable; median reply 18,500 characters, one of 38,600. |
| Concurrency | Four workers, then three more in a second process; no rate errors at any point. |

Rule from this: run this model only at its cap, and count an empty reply with finish reason "length" as a resource failure, not a verdict. Reasoning is roughly two to three times the length of the visible answer.

## 2. Where it was strong, and under what conditions

**Reading code for defects, when given the code file and a short list of reported results to attack.** (B3, D2, D4, D3.) It found, and I confirmed by running the code: the crippled memoriser baseline (no fall-back, empty-field default, last-writer table) that turned a 0.145 gap into a tie (file 16 §16e); the radius-5 mechanism that made the four-way "neutral" tie a fact about the grammar (§16a); the duplicated metric (M2 on H_full = M1 on H_full, 208 of 208); the no-op swap condition (171 of 171); the half-implemented adequacy check; the top-20 condition cap and the base-rate-blind score; the two-slot hardcoding; the defect-accounting bug in M6(ii). Condition: the prompt named the reported results the code was supposed to produce. Without that anchor (A-items) it did not read code.

**Auditing the adjudicator, when given the adjudication itself and asked for leniency.** (E1, three passes.) The single most useful output of the exercise. It found a pattern rather than a list: every "Partly valid" that existed only because I had a repair in mind; the non-verdicts ("accepted for experiment 3", "did not bite here"); the change lists that omitted ruled findings; the promised section 0.1 that did not exist. About thirty verdicts were restated. Condition: the object under audit was a table with a verdict column; the model excels at checking a stated rule against its own application.

**Attacking a design before it is built, when given the sketch and told to make it fail.** (E4.) It produced the sufficient-statistic scalar control — the one idea that changes what experiment 3 is — and a ten-point design with a power plan. Condition: asked for "the sharpest version that could actually fail", not for defects.

**Formal reading of a semantics for type errors and circularity, at three samples.** (A1, A2, A8.) The Rep/Con cycle, Org_ℓ as hidden parameter, the Account arity mismatch, the transport-direction inversion, the "exactly one of three provenances" contradiction, Derivation 1's type error, Derivation 2's failure for different decompositions and different Γ. Condition: three samples; single samples missed about a third of what the union found, and the union was what the second witness independently confirmed.

**Naming the experimenter's own goalpost moves, when given the change log.** (B2, C5.) It ran the audit I had not run on myself: for each pre-freeze change, did it alter what an outcome means, and was it made after seeing numbers pointing a particular way. Its criterion ("would the same change have been made had the data come out the other way") is now the standing rule.

## 3. Where it was weak, and under what conditions

**Repetition across items.** The battery overlapped on purpose (C1–C3, D3, D6 all attack the scramble test). The model restated the same three findings in every one of them, in every sample. About 41 of roughly 390 ruled rows are duplicates, most of them from this model. Condition: overlapping prompts; it does not notice that it has made the point already, because each call is fresh. Cost: reading time, and a count of findings that overstates distinct findings.

**Truncation hides the tail.** At 24,000 tokens, 16 replies ended mid-finding (D4 stopped at its eighth, A2 after Derivation 2). The visible findings were fine; what was lost is unknown. Condition: long documents plus long reasoning; fixed only at the cap.

**Numeric assertions without the numbers.** It asserted effects that did not occur: that the given-bound conditioning biased M3 materially (unconditional 0.935 against 0.973, same conclusion); that the "any crossing" bucket mixed in earlier failures (identical counts under the first-collision bucket); that a 0.003 winning margin was fragile (38 configurations won to 14, both halves); that 938 + 951 sequences did not match 135 configurations (it does: 1,890 less one). Condition: whenever a claim required arithmetic on the data rather than reading of the code. It reasons well about what *could* be wrong and does not check whether it *is*.

**Overreach toward "fatal".** Eight rows ruled Invalid, and the over-concession audit (E3) found further places where its "fatal" was a wording issue ("G0 grew" is fatal only as a discriminator). Condition: the hostile system prompt rewards severity; the model obliges. The E3 audit — this model auditing its own kind's overreach — corrected part of this, which is the best argument for running both audits.

**It cannot see what it was not given.** One item (D8) was built without the design file it was asked to map; two of three samples reconstructed the mapping from the results file without saying so. Only the third said its mapping was reconstruction. Condition: a missing document. The rerun with the file supplied (D8b) reached the same verdict, but the item's first verdict was unsupported at the time.

**Its clock is wrong.** One finding declared the freeze date "in the future" (B4.11). Cosmetic, but a reminder that it has no access to the present.

## 4. Errors it did not make

It never leaked or invented a number from the raw results that was not there; where it quoted, it quoted exactly. It never claimed to have run anything. When it did not know something (which half S0 was selected on), it said so and gave both readings.

## 5. How to use it next time

Three samples per item at the model's cap; batteries written to *not* overlap, or overlaps marked so the duplicates can be discarded unread; code items always anchored to a list of reported results; an audit pass of the adjudicator after every adjudication, in both directions (leniency and over-concession); every numeric assertion treated as a hypothesis to run, never as a finding.
