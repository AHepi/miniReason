# miniReason findings: September

## Abstract

We asked whether an explicit loop of conjecture, criticism, return and use could improve reasoning beyond a model answering directly with native thinking. The instrument was a personal prose reasoning CLI, exercised on checkable problems and then open inquiries. Completed native answers on the checkable comparisons contained no wrong required answers for criticism to repair. Harder cases exposed a shared initial generation bottleneck, with a repeated solving exception. Decomposition produced inspectable steps but no full synthesis. Critical episodes contained explanation and arithmetic repairs alongside withdrawn objections, invented errors and attacks on changed premises. Open inquiries produced concrete proposals and a potentially harmful restriction, without establishing propagated repair beyond native reasoning. Delivery contracts repeatedly prevented the intended comparisons. FW5 helped distinguish criticism, use and repair, while leaving substantial application evidence unspecified. These records identify mechanisms and failures worth investigating; they do not establish the requested reasoning advantage or exhaust the inquiry.

Evidence: [R001 report][R1], [R002 report][R2], [R003 published report][R3] and [derived properties][DP].

## The question and the standard

The owner's request for this paper was:

> it would be cool to see what has been discovered, if anything at all. Like a human readable paper or something.

This request comes from the current mandate; its verbatim REC-20260917-C receipt awaits safe append to [docs/DECISION_LEDGER.md][L]. The owner's standard, also preserved in the [R001 report][R1], is:

> it needs to work to improve reasoning in a substantive way that supports error correction and therefore a type of creativity. If you cannot find anything that is better than baseline with prose and an LLM native reasoning, then explain why. Even the failure is informative and worth documenting.

The unit of inquiry became the **critical episode**: a difficulty, its represented target, an objection, a content-sensitive response and the resulting situation. Seat names and completed cycles do not establish an episode. The study operationalised error correction through the following links; their joint effectiveness was a mechanism hypothesis, not a theorem supplied by FW5. [R002 PLAN][R2P]

| Element | Required evidence | Source |
|---|---|---|
| Critical episode | Target precedes criticism; response may retain, reject or suspend without solving | [FW5 lines 771-777][Fep] |
| Independence | Grounds accessible beyond the original error; distinct lineages or blind solves do not guarantee independent errors | [R002 PLAN][R2P]; [derived properties, GAP3][DP] |
| Decisiveness | A relevant, redoable check of the actual alleged defect | [FW5 lines 609-622][Fcrit]; [R002 PLAN][R2P] |
| Forced engagement | Study rule: reasoned disposition of each open objection, with disagreement permitted | [FW5 lines 626-634][Fuse]; [R002 PLAN][R2P] |
| Propagation | Changed content participates in later use; copying it into context is insufficient | [FW5 line 601][Froute]; [R002 PLAN][R2P] |
| Local repair | A fixed defect removed, protected successes preserved, and the contribution responsible | [FW5 lines 787-802][Frepair] |

FW5 distinguishes content-sensitive use from agreement; the mandatory disposition and redo procedures are study choices. [FW5 lines 626-634][Fuse]; [R002 PLAN][R2P]

The **commitment rule** responds to definition-only decomposition: an accepted step must assert a value, relation or decision and name a possible contradicting check or counterexample. The decisive claim must fit inside the plan; synthesis waits for accepted steps. This is an instrument contract, not a definition of creativity. R002's comparative correction predicate additionally required an oracle-wrong fresh native answer; native silence could establish only a completion difference. R003 did not import that gate into open inquiry. [R003 PLAN, R3-A1][R3P]; [R002 PLAN][R2P]

## The instrument

The personal reasoning CLI takes a prose problem and fixed recipe, obtains a working answer, asks a return seat to revise or defend it against objections, then asks a use seat to exercise it. A seat is a model assigned a role. It retains requests, public outputs, settings, usage, dispositions and failed attempts; hidden native reasoning is excluded. Optional closure disposes remaining objections without inventing later use. Its personal output is a working answer with objections, not itself a finding. Strict study profiles altered contracts and resource handling; failed delivery is distinct from an empty objection list. [docs/workflows/reason-cli.md][CLI]

| Condition | Intended link or comparison | Where actually run and reached |
|---|---|---|
| BARE | Direct prose with thinking off | R001 |
| NATIVE | Direct native-thinking comparator | R001; R002 calibration and fresh main; R003 o001, retained for o002 |
| LOOP-SINGLE | Same-lineage criticism, return and use | R001, DeepSeek throughout |
| LOOP-CROSS | Cross-lineage criticism with compulsory dispositions and use | R001, Qwen/GLM critics; R002 main; R003 o001, then Qwen/Kimi in o002 |
| LOOP-TESTED | Add a concrete check and mandatory redo | R002 main; no completed error-correcting return |
| LOOP-RECODED | Blind canonical/recoded solving for independent access | R002 main; initial calls stopped before the paired solves |
| LOOP-CHECKER | Host-executed signal returned to reasoning | R002 main; no checker execution reached |
| LOOP-DECOMPOSED | Make bounded targets available, carry accepted steps toward synthesis | R002 occurrences 001/002; R003 o001/o002; no synthesis |

Sources: [R001 PLAN][R1P], [R001 report][R1], [R002 report][R2], [R003 report][R3]. These are intended contrasts with disclosed confounds. Neither a forced-engagement-off comparison nor neutral matched multi-call control ran; R003 has no BARE arm. R3-A1 changed several settings together and reused the earlier native answers. [R002 report][R2]; [R003 report][R3]

## Findings

### F1. Native answers left no wrong endpoint to correct

On the reported checkable comparisons, completed native answers satisfied the required facts; the failures were missing answers at the completion ceiling. In R001 the loop initials were already correct too. Consequently there was no native-incorrect endpoint available to support the requested comparative correction. [R001 report][R1]; [calibration admission][CAL]

| Observation | Count or setting | Evidence |
|---|---:|---|
| Native completion ceiling | 32,768 tokens, including reasoning | [Calibration admission][CAL]; [CLI][CLI] |
| R002 fixed calibration | 24 trials: 20 correct, 0 incorrect, 4 no-answer | [Calibration admission][CAL] |
| R001 selected native | 7 correct completed answers; 1 ceiling stop | [R001 report][R1] |

**Limit:** this finite record does not establish native infallibility or a fully observed null when answers are censored. [R001 report][R1]

### F2. A loop can inherit the initial seat's exhaustion

R002's undecomposed conditions all stopped initially on C05, C06 and C12. C09 was the exception: CROSS, TESTED and CHECKER already answered correctly in their native initial calls, while fresh NATIVE and RECODED exhausted. Their subsequent GLM critics failed. This was a completion difference before criticism, consistent with repeated solving or prompt differences, not correction caused by the loop. [R002 report][R2]

**Limit:** the study does not isolate the cause of C09's differing initial outcomes. [R002 report][R2]

### F3. Decomposition exposed work without completing it

In R002's amended occurrence, accepted formalisation consumed the permitted steps before the decisive calculation and synthesis; C12 instead declared missing computation. R003 later required refutable commitments and did obtain decisions and relations, including disputed causal claims, but still no full synthesis. R002 exposed formalisation without commitment; R003 exposed commitments whose critical routes still failed. [R002 report][R2]; [R003 report][R3]

| Decomposition observation | Recorded extent | Evidence |
|---|---|---|
| R002 A2, C05/C06/C09 | 3 accepted steps each; plans of 6/7/6 steps | [R002 report][R2] |
| R002 A2, C12 | 1 accepted step; STEP2 unresolved | [R002 report][R2] |
| R003 o001 | 15 completed step cycles; no full synthesis | [R003 report][R3] |
| R003 o002 | 1 accepted step, in O05; 6 first-critic locator stops; no synthesis | [R003 summary][R3S] |

**Limit:** partial access is not a completed reasoning benefit, and the amendments changed multiple conditions. [R002 report][R2]; [R003 report][R3]

### F4. Criticism included repair, false attacks and legitimate resistance

R001 critics manufactured objections that withdrew themselves, asserted false arithmetic, and treated changed premises as defects. Returns rejected the delivered false factual attacks. The archived P02 correction came from a use seat redoing the sum after a critic had supplied a false replacement. It remains a local correction in a later-failed run. [R001 report][R1]; [R001 summary][R1S]

| R001 event | Exact evidence or count | Source |
|---|---|---|
| Self-withdrawing raw objections | 12 objects in 8 selected CROSS attempts; repaired to empty lists before return | [R001 summary][R1S] |
| False arithmetic rejected | "7^2 = 49 = 2*19 + 10" | [R001 report][R1] |
| Archived P02-SINGLE use repair | 38 corrected to 41 through 984/24; later return schema failure | [R001 report][R1] |
| Correct-to-incorrect requested-answer transitions | 0 observed in current or archived loops | [R001 summary][R1S] |

**Limit:** absence of observed harm applies to R001's requested answers, not every explanation or later study. [R001 summary][R1S]; [R003 report][R3]

### F5. Different lineages varied criticism without assuring decisive checks

Most selected SINGLE runs stopped at the first no-new-objection cycle. This silence was not demonstrated blindness: selected initials were already correct. P08-SINGLE supplies an explanation repair: criticism replaced an overclaim of exhaustive schedule coverage with a left-shifting argument, subsequently used while retaining the answer. CROSS produced different attacks, but recurrent GLM delivery failures prevented reading those missing seats as considered objections. [R001 report][R1]

| Scope and seat | Recorded delivery or stopping | Comparison / cause | Source |
|---|---|---|---|
| R001 SINGLE, derived from reported cycles, objections and stop rule | 7 runs stop after 1 cycle; P08 continues to cycle 2 | P08 supplies the explanation-repair exception | [R001 report][R1]; [R001 summary][R1S]; [R003 PLAN census][R3P]; [CLI][CLI] |
| R001 selected CROSS, GLM | 9/18 complete; 9 unavailable | Unavailable calls all length stops; Qwen 36/36 complete after repairs, including use | [R003 PLAN census][R3P] |
| R002 occurrence 001, GLM | 0/7 complete | 4 length, 3 schema; Qwen 7/7 complete | [R003 PLAN census][R3P] |
| R003 o001, GLM | 0/8 complete | 6 length, 2 non-JSON; Qwen 23/25 complete | [R003 PLAN census][R3P] |

**Limit:** lineages, critic multiplicity, modes, budgets and repairs differ; these delivery counts cannot identify a lineage-only reasoning effect. [R001 report][R1]; [R003 PLAN][R3P]

### F6. Instrument failures consumed the intended observations

The smoke runs and strict studies exposed constraints on obtaining readable episodes. The resulting rules address delivery, not truth. [Ledger REC-20260916-C/D and REC-20260917-A/B][L]; [CLI][CLI]

| Finding | Rule produced or justified | Evidence |
|---|---|---|
| Smoke-1 native reasoning consumed 8,192 tokens with empty public content | Budget for thinking plus answer; native ceiling became 32,768 | [Ledger REC-20260916-D][L]; [CLI][CLI] |
| Smoke-2 gateway critic length-stopped; gateway-default did not establish off control | Account for possible reasoning; explicit Ollama control uses /api/chat think:false, not an assumed /v1 switch | [Ledger REC-20260916-D][L]; [CLI][CLI] |
| Smoke-3 completed but exposed answer-envelope and objection/disposition defects | Preserve supplemental prose, separate working from final objections, carry resolved dispositions and close remaining use objections | [Ledger REC-20260916-D][L]; [CLI][CLI] |
| Strict R002 prohibited silent recovery; A2 separately amended delivery | Freeze envelopes; retain failures; declare each repair, ceiling and seat change | [R002 PLAN][R2P]; [R002 report][R2] |
| R003 o001 repair inputs refused before dispatch | Check exact request size before sending; prospectively replace the restrictive cap with route-specific documented allowances | [R003 report][R3]; [R003 PLAN][R3P] |
| Open prose failed exact locators, suffixes and partial-step checks | Preserve rejected content; make custody interfaces usable and judge the current step's obligation | [R003 report][R3]; [CLI][CLI] |

**Limit:** contract repair can admit mistaken content; delivery success is no semantic endorsement. [R003 report][R3]

### F7. Open problems yielded refutable proposals, not established propagated repair

For workshop allocation, native proposed approval by "a rotating peer panel"; the rejected CROSS return proposed "no discretionary approval." That is an inspectable rule change, but its caps could exclude legitimate long projects and its reserve could disadvantage newcomers. It never became accepted working state or reached use. [R003 report][R3]

For microbial recovery, native proposed "cross-incubate cells in filter-sterilized spent medium from each history"; CROSS ended with "a replicated, controlled experiment that randomizes prior heat exposure". Prospective assignment is concrete, but it arose without a critic objection, had no subsequent use, and dropped the explicit medium contrast. The original causal account remained unestablished. [R003 report][R3]

For library-based invention, CROSS accepted "withholding/ablation/provenance/transfer tests count for neither account there". If matching meant only unperturbed outputs, that discarded potentially informative interventions; if it meant every intervention matched, it restated scope discipline. No accepted later use resolved the dispute. [R003 report][R3]

The sealed briefs anticipated missing-history, generic-transfer, decorative-log and prose-equivalence flaws that appeared in raw decomposed criticism. Several mappings were only partial or adjacent; the history-assignment flaw remained unchallenged. Naming these flaws did not repair them. The FW5 lenses exposed episode gaps and protected losses, but the published reading found no separate added measurement beyond its existing target/check/response/use/loss fields. [R003 summary][R3S]

**Limit:** this compares retained o001 native answers with amended o002 loops; rejected proposals and closing edits cannot be counted as propagated corrections. [R003 report][R3]

### F8. FW5 constrained attribution but did not supply the missing evidence

The derivation memorandum supplies conditional properties, not a forecast that criticism will improve an answer. Its measurement contribution is to distinguish the following claims. [FW5-DERIVED-PROPERTIES.md][DP]

| Properties | What can be examined here | FW5 source |
|---|---|---|
| EC01-EC02: active content dependence and reason contrasts | Route intervention and defended recodings still needed | [601][Froute], [626-634][Fuse] |
| EC03-EC04: permission to reuse premises and limits of refutation | Explicit withdrawn-premise conflicts and invalid inferences from defeated arguments | [638-676][Fstanding] |
| EC05-EC07: binding construction, historical novelty, attempted origin | Attempts are readable; full provenance/repertoire claims remain unsupported | [714-767][Forigin] |
| EC08-EC09: complete critical episodes and repair | Bounded target/response and loss readings, with causal qualifications | [771-802][FepisodeRepair] |
| EC10-EC11: created knowledge and recursive return | Created knowledge needs origin evidence; prior-step return needs another route | [814-839][Fknowledge], [1050-1062][Frecursive] |
| EC12: enabling conditions | Exposure, selection and resource audit | [1095-1101][Fenabling] |

The published open-problem reading used the applicable trace lenses and reported the scoped null in F7. The planned active-versus-archived objection comparison was deferred until the use route survives. Neither missing outputs nor renamed fields establish that null. [R003 report][R3]; [R003 PLAN][R3P]

| Application or evidence gap | What remains to be supplied |
|---|---|
| GAP1 | Defensible identity across prose recodings |
| GAP2 | Concrete use for a terminal prose conclusion |
| GAP3 | Critic independence beyond labels |
| GAP4 | Independently identified operative rule and contrasts |
| GAP5 | Actual standing and essential premises |
| GAP6 | Case-specific nontrivial binding construction |
| GAP7 | Historical deployable repertoire |
| GAP8 | Justified obligations and the significance of local repair |
| GAP9 | True anchoring and relevance of the check |
| GAP10 | Evidence connecting an episode to retained or recursive capability |

Source: [derived properties, gap analysis][DP]. These are missing application criteria or evidence, not uniformly absent mathematical definitions.

**Limit:** this local absence of added measurement neither refutes FW5 nor verifies its constitutive account. [R003 report][R3]

## The direct answer

The studies found explanation repair, a local arithmetic correction, concrete proposals and recurring failures. They did **not establish the requested substantive reasoning advantage beyond native thinking through propagated error correction**. On checkable tasks, native answers were already correct or missing; useful changes lacked completed comparative routes; extra solving and altered resources remained alternatives. This is an informative failure to demonstrate the requested mechanism, not evidence that it is impossible. [R001 report][R1]; [R002 report][R2]; [R003 report][R3]

## What the evidence points to next

These directions follow from named failures; none is reported here as a completed test.

| Wiring variation | Why this finding motivates it | Status and source |
|---|---|---|
| Route intervention | Separate an objection being generated from its operative use, using a shared parent and matched RETURNED/ARCHIVED return/use branches | Planned, deferred until use works; F4/F7; [R003 PLAN][R3P], [R003 report][R3] |
| Problem-critic-first | Criticise framing and allocation of decisive work before an exhausted whole-answer initial or definition-only plan blocks inquiry | Proposed here from F2/F3; not a named frozen condition in these sources; [R002 report][R2] |
| Rivals by test | Compare named counter-derivations through a relevant check instead of increasing pressure to object | Proposed wiring from F4/F5; the plan supplies named-method-rival and fixed-counter-derivation rationales; [R002 PLAN][R2P] |
| Return to an accepted step | Let the detected C05 dependency error alter its earlier accepted target and subsequent work | Explicitly deferred route; F3; [R002 report][R2], [R003 PLAN][R3P] |

Any claimed criticism-specific benefit also needs a neutral continuation receiving matched information and resources. [R003 PLAN][R3P]

## Limits and claim ceiling

These are finite, selected occurrences with preserved failures and changing instruments. DeepSeek Flash supplied the conjectures; critic diversity is not independent replication, and host labels do not establish distinct lineage. The readings are guarded, attackable judge-role artifacts; disagreement remains a substantive question. Counts describe outcomes and resources only. [R001 report][R1]; [R002 report][R2]; [R003 report][R3]; [rulings, including lineage and measurement rules][RULES]

FW5 is the sole semantic target under the current source ruling. Prose remains legitimate when a contract fails, and an executable check does not settle relevance. Historical novelty, general creativity and recursive capacity remain unestablished. Completing this paper is a reporting boundary; concrete counterexamples, disputed mappings or separately declared interventions can reopen the inquiry. [PURPOSE.md][PURPOSE]; [docs/SEMANTIC_GUIDE.md][SG]; [R003 report][R3]

[R1]: ../../experiments/diagnostics/R001-reason-cli-vs-baselines/REPORT.md
[R1P]: ../../experiments/diagnostics/R001-reason-cli-vs-baselines/PLAN.md
[R1S]: ../../experiments/diagnostics/R001-reason-cli-vs-baselines/readings/SUMMARY.md
[R2]: ../../experiments/diagnostics/R002-episodes-under-calibrated-difficulty/REPORT.md
[R2P]: ../../experiments/diagnostics/R002-episodes-under-calibrated-difficulty/PLAN.md
[CAL]: ../../experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/ADMISSION.md
[R3]: ../../experiments/diagnostics/R003-open-problems-trial-series/reports/o001-o002-REPORT.md
[R3P]: ../../experiments/diagnostics/R003-open-problems-trial-series/PLAN.md
[R3S]: ../../experiments/diagnostics/R003-open-problems-trial-series/readings/o001-o002/SUMMARY.md
[DP]: ../../experiments/diagnostics/R003-open-problems-trial-series/FW5-DERIVED-PROPERTIES.md
[CLI]: ../workflows/reason-cli.md
[L]: ../DECISION_LEDGER.md
[RULES]: ../reviews/session-rulings-2026-09-14.md
[PURPOSE]: ../../PURPOSE.md
[SG]: ../SEMANTIC_GUIDE.md
[Fep]: ../sources/FW5-explanatory-construction.md#L771-L777
[Fcrit]: ../sources/FW5-explanatory-construction.md#L609-L622
[Fuse]: ../sources/FW5-explanatory-construction.md#L626-L634
[Froute]: ../sources/FW5-explanatory-construction.md#L601
[Frepair]: ../sources/FW5-explanatory-construction.md#L787-L802
[Fstanding]: ../sources/FW5-explanatory-construction.md#L638-L676
[Forigin]: ../sources/FW5-explanatory-construction.md#L714-L767
[FepisodeRepair]: ../sources/FW5-explanatory-construction.md#L771-L802
[Fknowledge]: ../sources/FW5-explanatory-construction.md#L814-L839
[Frecursive]: ../sources/FW5-explanatory-construction.md#L1050-L1062
[Fenabling]: ../sources/FW5-explanatory-construction.md#L1095-L1101
