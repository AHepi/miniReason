# R001 cross-problem reading

No observed occurrence shows a completed correct loop answer where a completed NATIVE answer is wrong, reached by the plan's critic-return-use route. P01-P07 have correct NATIVE answers; P08's NATIVE call ends CEILING_HIT with no public answer. Both current loop initial conjectures are already correct on every problem. The study is incomplete for the full native comparison, not a demonstrated universal failure of criticism.

## Current manifest-selected 8 x 4 verdicts

|Problem|BARE|NATIVE|LOOP-CROSS|LOOP-SINGLE|
|---|---|---|---|---|
|[P01](P01.md)|incorrect|correct|correct|correct|
|[P02](P02.md)|incorrect|correct|correct|correct|
|[P03](P03.md)|incorrect|correct|correct|correct|
|[P04](P04.md)|correct|correct|correct|correct|
|[P05](P05.md)|incorrect|correct|correct|correct|
|[P06](P06.md)|correct|correct|correct|correct|
|[P07](P07.md)|incorrect|correct|correct|correct|
|[P08](P08.md)|undecidable|undecidable|correct|correct|

These are bounded requested-fact verdicts. The independent judge upholds P07 BARE as incorrect: "2) d(x)=3x^2+8 nonzero at every allowed x? No." is an explicit false assertion that the later correct recap never explicitly withdraws. PLAN line82 requires no contradictory task-answer assertion. The prior implicit-retraction alternative is retained in the judge correction record. P06 BARE explicitly says its initial wrong order "was a mistake" and finalizes DAFECGB, so it is correct. P08's incomplete baseline streams are undecidable. Historical baselines remain separate observations.

## Named corrections, changes and falsifier bookkeeping

No current loop has an incorrect-to-correct requested-answer transition. No current or archived loop has an observed correct-to-incorrect requested-answer transition after objection uptake. Consequently there is no PLAN "criticism harmful" event to pair with the one historical helpful use event below; wrong-to-wrong advice is still documented.

The archived P02-SINGLE occurrence1 is the important local correction. Its off-fallback initial ends "Thus, I state the answer as 2 with uncertainty." The first critic correctly attacks the period-only argument but supplies the false replacement: "A correct Burnside count over the 24 dihedral symmetries gives 38." The off-fallback return states "The exact number of distinct necklaces is 38." Its use seat then objects: "The working answer's claim that the exact number is 38 is incorrect" and supplies the correct sum984/24=41. Cycle2 return says "The final answer is corrected to 41 and the corrected derivation is supplied." This names a real reflection/rotation-count error and visibly returns it to the answer. The run subsequently ends SCHEMA_FAILURE in cycle3; it has no completed loop answer. NATIVE from the corresponding historical CROSS occurrence was already41, and the decisive correct objection came from use, not critic. This event therefore fails the five-conjunct witness independently of the later failure. Exact quotes, requests, dispositions, both use derivations and source hashes: [P02 historical reading](P02.md), [archived TRACE](../runs/LOOP-SINGLE/P02/old1/TRACE.md).

P08-SINGLE repairs an explanation while keeping253. Initial: "This captures every feasible nonpreemptive schedule"; critic: "The DP enumerates schedules with no voluntary idle before a released job, not every feasible schedule." Return: "Any feasible schedule with the same order can be left-shifted to this earliest-start form; by induction each completion time is no later, so the positive-weight objective cannot increase." Both uses derive the A-last minimum253; cycle2 use expressly invokes left-shifting. This is a concrete improvement in the public justification, but neither a wrong-to-right schedule nor a native-incorrect comparison. [P08](P08.md), [SINGLE cycle1](../runs/LOOP-SINGLE/P08/cycles/c0001/CYCLE.md).

P08-CROSS also expands an asserted enumeration into a recurrence after a valid coverage criticism. It retains correct253, rejects a later false mixed-state objection, and clarifies the changed-F-release question. Its first return falsely explains that any longer wait would mean choosing a different next job; its final integrality assertion still omits the explicit fixed-order dominance argument supplied in SINGLE. A final rejection paragraph says40 where its own t=5 C-branch uses36; the actual recurrence table and required schedule remain correct. Correct endpoints do not certify every explanatory sentence. [P08](P08.md).

The preregistered supportive pattern requires at least one five-conjunct witness and readable NATIVE on all eight. Neither requirement is met. The seven completed native comparisons have no loop-correct/native-incorrect event. P08 is censored, so PLAN forbids declaring the fully observed null. Historical use-only improvement and proof repair are preserved without being relabeled as support or hidden because they miss the endpoint predicate.

## What critics and returns actually did

In the selected current runs, eight delivered critic objections are identified, with no objection naming an actual wrong required loop answer: P01-CROSS c0001-k01-o001; P04-CROSS c0002-k01-o001; P05-CROSS c0001-k01-o001; P07-CROSS c0001-k01-o001/o002; P08-CROSS c0001-k01-o001 and c0002-k01-o001; P08-SINGLE c0001-k01-o001. This is an occurrence list, not a quality statistic. Five are false factual attacks (P01, P05, both P07, P08 cycle2). P04 is a valid attack on a preceding use objection. Both P08 cycle1 objections identify explanation gaps; the CROSS objection also suggests a generally invalid dynamic-WSPT proof route. Returns reject the five false factual attacks, accept the criticism of criticism, and expand both P08 explanations.

Two additional delivered use objections manufacture robustness demands about changed premises. P04 asks what happens if (3,ok,6) is added; both derivations correctly exclude Blue in that changed table, yet the objection says original inclusion is "fragile and dependent on the exact input sparsity rather than a robust property of the team itself." Return rejects it: "The working answer does not claim Blue would satisfy HAVING under a different table." P08 argues the idle interval might be "an artifact of the specific release time"; return accepts clarification but keeps the original schedule. Dependence on the stated data is not itself a defect. [P04](P04.md), [P08](P08.md).

Twelve self-defeating raw objection objects occur in eight selected CROSS critic attempts, before repair: P01 c0002-k01/a00 object1; P02 c0001-k01/a00 objects1,3,4,5,6 and c0002/c0003-k01/a00 object1 each; P03 c0001-k01/a00 object1; P04 c0001-k01/a00 object1; P05 c0002-k01/a00 object1; P06 c0001-k01/a00 object1. Examples: P01 "I will return an empty list as no valid objection exists" while inside an objection object; P02 "The working answer's 24 is CORRECT. Objection withdrawn"; P06 "The working answer is logically sound. No objections found." Every named attempt repairs to an empty delivered list, so return never receives these raw objects. P02's additional raw object2 doubts24 without a counter-enumeration; it is an unsupported verification demand, listed separately rather than counted as a self-withdrawal. The eight case readings quote all these texts and separate delivery from existence.

A further archived P02-CROSS malformed object concludes no objection; see [P02-SUPPLEMENT](P02-SUPPLEMENT.md). It is outside the current-only twelve-object list. Historical P01-CROSS also delivers two caveat/rigor objections that acknowledge the reasoning holds under the given symmetry; return expands exposition without changing7/20. Historical P02-CROSS demands explicit counts that are actually correct. Historical P03-CROSS invents a step1 value y=7 and return rejects it using the actual simultaneous y=5. No wrong answer is silently replaced in this account. Malformed or truncated critic prefixes retain their raw bytes and unavailable status; they are not imputed considered-and-rejected objections.

Returns can use criticism to retain, clarify, reject another criticism, or change an answer; the operative target is not fixed by seat name. Validity and use remain distinct under [FW5](../../../../docs/sources/FW5-explanatory-construction.md) lines622-634. The false38 in historical P02 was taken up, while the true41 entered through a different seat. That is informative about this occurrence, not evidence for a universal or isolated lineage mechanism.

## Use-seat contribution, episodes and basins

The case readings quote every use question and both derivations and supply separate checks for changed questions. Most selected uses confirm a narrow consequence already present: P01 likelihood1/3 or position2 probability27/40; P02 reflection parity or fixed count24; P03 step12 A(0,3),E; P04 a counterfactual table or Red/Blue filtering; P05 residual about166Pa or root inadmissibility; P06 an impossible B=6 placement or span6; P07 derivative3 or fiber{0,7,12}; P08-SINGLE A-last253. The use prompt contains both problem and working answer; labeling a derivation independent is not evidence of causal independence. P08-CROSS repeatedly refuses the release6 hypothetical in problem_derivation even while working_derivation answers it; no successful independent counterfactual check by that seat is claimed. Reader arithmetic with the altered premise givesF at6, residual cost147 instead of actual-release160; this was not supplied to participants.

Episode boundaries are target-dependent: P04's use criticism becomes the critic's next target, and P08-SINGLE shifts from the answer to the claimed exhaustiveness of a method. FW5 lines771-777 permits critical episodes to close in retention, rejection, suspension or changed understanding; closure alone is not solution. The case readings preserve proposals, particular challenged claims, each return and the subsequent use. They do not identify creativity from a fixed conjecture/critic/return seat sequence.

|Problem|Basin sensitivity of BARE, NATIVE, CROSS initial, SINGLE initial|
|---|---|
|P01|85/224 versus7/20,7/20,7/20|
|P02|6 versus41,41,41|
|P03|B,6,0 and GETEEGEEEEETGG versusA,6,3 and GETEEGEEEEEEEG in the other three|
|P04|All give Blue,2,1,15 then Gold,1,0,4|
|P05|2.473m/2074.0kPa versus1.028m/167.5kPa in the other three|
|P06|All final commitments DAFECGB; BARE retracts its initial slip within its own call|
|P07|Correct four-fact recap in all, with BARE's contradictory No adjudicated incorrect under PLAN|
|P08|BARE/NATIVE incomplete; both loop initials already253 withE-B-D-idle-F-C-A|

Every decisive sentence is quoted in its case's basin section. No case exhibits "attractor signature: shared wrong answer" across all four required answers, and none exhibits an empty same-lineage critic on an oracle-wrong presented answer. No "same-lineage blind" event is claimed. Historical P02-SINGLE initially disagrees with already-correct historical NATIVE/CROSS, and its wrong38 receives nonempty criticism plus a true use objection. These observations do not rule out shared-prior failure elsewhere.

GLM unavailability is operational: nine current critic occurrences, all three cycles in P02/P05/P08, end `CEILING_HIT` because provider records report `INCOMPLETE_GENERATION/length` at8192 completion tokens with `think:false`. No one of these nine is a transport or schema failure. Preserve their public prefixes as unavailable; test any prospective output allowance or contract change with declared matching resources before drawing a content inference.

## Comparison and recurrent limits

CROSS and SINGLE have the same correct selected endpoints. CROSS supplies more false numerical attacks, schema repairs and GLM unavailability; SINGLE's P08 criticism provides an explicit fixed-order dominance repair. This is a witnessed trace difference, not a lineage-only effect: two versus one critics, identity, thinking controls, allowances, fallback opportunities and total calls all change. Matched multi-call and content contrasts are absent.

The main limit on the owner's endpoint question is baseline sufficiency, followed by P08 censoring, not observed refusal to accept a true endpoint correction. Recurrent local problems include self-defeating objection packaging, invented arithmetic, and treating changed premises as evidence against a correct answer. Non-return is visible as persistent failure of P08-CROSS's use seat to derive its own hypothetical, not rejection of a valid wrong-to-right answer correction. Historical operational failures and the use-seat-only correction remain independently visible.

Inspect [inventory](../runs/INVENTORY.md), [custody](../runs/CUSTODY.md), [provider operations](../runs/OPERATIONS.json), all eight case files and their linked requests/TRACE/CYCLE records. The report carries the verbatim PLAN ceiling and successor proposal. No provider call, key-value read or git state change occurred in this reading.
