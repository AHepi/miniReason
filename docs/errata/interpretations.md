# Interpretation errata

These are scoped findings from independent substantive review. Original model outputs remain unchanged. A disputed interpretation is not converted into a global model or language verdict, and a proposed corrective contrast is not recorded as an executed repair.

## INT-001 — Changed position reported as preservation of the earlier construct

In E015's matched condition, the construction proposed a new level-relation target. The criticism questioned why aggregation could not already be a rule target. The revision adopted the no-new-target conclusion while describing it as preservation of J and attributing that conclusion to J. The promotion carried the resulting account forward. This changes who committed to what; retaining each raw occurrence did not prevent the later reading from misdescribing it. See [the exact passages and rival readings in the E015 review](../reviews/E015-construction-review.md#matched-reversal-presented-as-preservation).

A supported successor compares the same fixed J and criticism under an explicit prior/new commitment comparison, or controlled criticism recoding, without changing either source. Whether such a comparison prevents the misreporting remains untested. A correction to a position may be justified even when its stated provenance is wrong; those are separate findings.

## INT-002 — Stating a conditional treated as necessarily strengthening its commitment

E015's Mini revision claimed that expressing a cross-booking presupposition as a stated rule adds stronger commitment than preserving it as an unresolved locus. The supplied reasoning does not establish that necessity: a stated conditional can retain its antecedent without asserting that an unnamed resource exists. The promotion questions an undefined cost but carries a vocabulary/status distinction that still needs a separating case. See [the E015 review](../reviews/E015-construction-review.md#mini-a-sound-challenge-followed-by-an-unsupported-strengthening-claim).

A supported contrast holds the conditional content fixed while varying its prose or rule presentation, then separately changes whether the antecedent is asserted. This targets inferred commitment under a named interpretation, not a hierarchy of formal and prose legitimacy. No such contrast has yet run.

## INT-003 — Current criticism attributed to a prior episode

The E015 Mini-native promotion attributed the current objection about the asserted primary target to the selected E009 occurrence. Its own current criticism and revision support a narrower provenance account. The revision's useful conditional correction does not make the promotion's cross-episode attribution accurate. See [the complete E015 sequence](../reviews/E015-construction-review.md#mini-native-a-qualified-correction-followed-by-cross-episode-misattribution).

A later source-binding intervention could preserve exact quoted spans and origin coordinates through promotion. An identifier or source hash alone would establish carriage rather than the correctness of the attributed semantic dependency. That distinction must remain part of any claimed repair.

## INT-004 — Tightness gloss admits unattained endpoints

E013 matched-native corrects the reservation/availability endpoint reversal but defines tightness using a bound-or-attainment disjunction (and a lower-bound-only gloss). In its own excluded-high/high case, the bounds hold while the endpoints are unattained. The literal predicates therefore fail to express the stated distinction. See [E013 recovery review](../reviews/E013-recovery-review.md#matched-native-endpoint-polarity-corrected-tightness-still-misdefined). The review independently enumerated the finite case; no model repair was run. A successor must separately state enclosure, endpoint attainment and exact-set obligations.

## INT-005 — Criticism introduces an unsupported expressibility restriction

E013 Mini-native accepts its critic's claim that RSS projections cannot return intervals because they return a single answer. RSS gives a scalar as an example without making it an exhaustive codomain restriction; one interval can be one structured answer. The criticism does not establish the alleged limitation. The revision also mixes an exact feasible set with its convex envelope and says an interval can become non-convex. These claims have different failure conditions. See [E013 recovery review](../reviews/E013-recovery-review.md#mini-native-an-effective-distinction-and-an-unsupported-carrier-restriction). The source remains unchanged; this is a scoped criticism of the inferred restriction, not proof that every interval interpretation conforms to RSS.

## INT-006 — Generated occurrence identifier loses a digit

E013 matched-native promotion prints a 63-character P9 identifier where the source identifier has 64 characters. Host origin metadata and retained source bytes are correct. The malformed reference occurs in model prose, so valid machine provenance does not repair that textual attribution. The [recovery review](../reviews/E013-recovery-review.md#matched-native-endpoint-polarity-corrected-tightness-still-misdefined) records both exact strings. No original response was edited.

## INT-007 — Correct use answers coexist with inconsistent returned accounts

E016's native-family accounts introduce capacity as an admissibility filter while the source permits negative reported availability. Matched-native use still correctly reports -2 and separates arithmetic from physical planning. The correct table does not make the earlier filter formulation coherent. The [E016 review](../reviews/E016-reason-use-review.md) identifies precise passages and alternative readings; it also records inaccurate attribution of supplied distinctions and occasional claims that physical freedom licenses mere arithmetic enumeration. These are separately scoped defects. No earlier response was edited and no new criticism variant was constructed from this observation; E017–E020 remain as preregistered.


## INT-008 — Omission permits correct use while returned accounts still lose distinctions

E022 supplies no supplemental criticism occurrence, while J and common-source criticisms remain. All four staged use answers give the stipulated reporting/planning numbers, and several responses reconstruct the aggregation-as-rule rival. Yet bare and Mini later reinstate an unestablished exclusion from rule criticism; native and Mini-native display hard-capacity filters that exclude the source-permitted negative reporting case; several outputs misattribute P7's examples or overread the earlier modal warning. Mini-native use correctly follows the stipulated unfiltered reporting calculation without identifying its own parent's filter as the departure.

The [E022 completion review](../reviews/E022-completion-review.md) locates each passage, its competing reading and finite consequence. These defects are in proposed content, separate from verified wire/replay custody and correct numerical answers. E022 always returns the account; it does not establish that the account is unnecessary. E020 produced no complete response or use observation, and E023 is prepared only. No original source, account or response was amended.

## INT-009 — The FW5-versus-harness-spec review under-counts its own findings in its body text

**Observation.** `docs/reviews/fw5-vs-harness-spec-2026-09-14.md`, published under REC-20260914-P, opens its framing paragraph with "Six readers produced 39 findings; six refuters checked every citation at source". The mechanical count in its own supporting appendix, `docs/reviews/fw5-vs-harness-spec-findings-2026-09-14.md`, is **47** findings, of which **19** carry a refuter verdict of `stands: true`.

**What failed.** A count stated in prose disagrees with the count of the material it summarises, by eight findings. Nothing else in the sentence is at issue: six readers, six critics and six refuters did run, and every citation in the review was re-read at source.

**Impact.** A reader who takes the body sentence alone under-counts the raised findings by eight and may read the review as narrower than it is. No finding's content, its disposition in Appendix A, its citation or its refuter verdict is affected; no count anywhere in the review is a score, and nothing in it aggregates. The document's conclusions are unchanged.

**Cause — established.** The synthesizer's own miscount when writing the review body. It is established rather than suspected: the findings appendix is generated mechanically by `render_findings.py` from the critics' `critiques.json` and the refuters' `refutations.json`, none of which the synthesizer wrote, and an independent recount of those two files gives 47 findings across the six critic axes (8 + 7 + 8 + 8 + 8 + 8) and 47 refuter verdicts of which exactly 19 are `stands: true`.

**Competing explanations, and why they are rejected.** That the appendix over-counts by listing findings later split or struck; rejected, because both sentences claim the number *raised*, the appendix header states 47 raised and 19 standing, and Appendix A of the review itself dispositions 47. That "39" is the number surviving refutation rather than the number raised; rejected, because the number surviving is 19, and the same sentence separately reports the refutation pass. That a reader/critic distinction explains the gap — the findings were raised by six critics, not by the six readers the sentence names; rejected as an explanation of the *number*, since no count of critic output is 39 either, although the sentence does attribute the findings to the wrong one of the two delegated roles.

**Corrective action.** The review is published verbatim and is **not** edited: `AGENTS.md:17`, "Never modify a published observation", and a corrected interpretation goes in a separately named file. This erratum is that file. The correct figure already travels with the document in two places a reader meets before or beside the sentence — the four-line provenance banner prefixed at publication ("47 findings were raised; 19 stand unchanged after refutation") and the appendix's own header ("47 findings were raised across 6 axes; 19 carry a refuter verdict of `stands: true`"). No count in the review was recomputed, softened or restated to agree with the prose.

**Checked: yes.** The 47 and the 19 were recounted directly from the critics' `critiques.json` and the refuters' `refutations.json` in the session scratchpad, beside the `render_findings.py` that produced the appendix, without going through the appendix text. The two files are working material of the delegated review, not published evidence; the published appendix is their rendering and states the same two numbers.
