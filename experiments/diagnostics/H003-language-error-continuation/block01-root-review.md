# H003 block 1: correct sets, defective explanations

Root review, 2026-09-13, REC-20260913-K. This is a continuation gate through cycle5, not the final twenty-cycle report.

## Evidence and execution

[checkpoint05.json](checkpoint05.json) preserves22 provider requests and22 terminal receipts:21 complete public answers and one truncated answer. Total reported usage is213865prompt +59867completion =273732tokens. All five arms overlapped at the start. WHL stopped on cycle2 with original provider status INCOMPLETE_GENERATION, finish reason length and4096completiontokens; its full available partial text is preserved. Four other arms completed cycles1–5. No request was retried.

Exact requests, full public responses, source hashes, canonical artifact/port routing and parent custody are published. The helper's concurrency statistic measures overlapping local call intervals, including overhead; it is not server-side telemetry. This remains the declared pure-routing fixture, without qualification of the unsupported Windows durable scheduler.

Root read all four fresh-use responses, the complete prose chain cycles1–5, and the WHL failure receipt. This gate makes the specific claims below; it is not a comprehensive semantic appraisal of every other intermediate response. Astra implemented and offline-tested the helper and drafted operational guidance. Root performed implementation, material and semantic reviews.

## Fresh case A

The operator contract was frozen before provider calls. Greatest-revision payloads give A:{0}, B:{3,8}, C:{0}; capacity6 therefore gives the exact availability set {-2,3}, minimum-2 and maximum3. The four intervening integers -1,0,1,2 are unavailable. All four continuing arms report the correct exact set and a correctly ordered interval somewhere, but none has an entirely sound explanation of its bounds.

| Arm | Observed finite use and explanatory defect |
|---|---|
| prose | Correct alternatives, effects and exact set. Its bounds section first calls capacity minus minimum reservation the lower availability bound, producing3, and calls-2 the upper. Later prose and the final summary give minimum-2 and maximum3 correctly. It also says interval replacement imports five values after listing the four missing integers. |
| rss | Correct exact set and interval. Calls3 the lower availability bound and-2 the upper. States the sum of upper reservations is11 while immediately computing6-8; the actual sum is8. |
| whl-roundtrip | Correct exact set and interval, but explicitly says the lower bound on availability is3 and the upper is-2, defending the frozen WHL function names as an orientation convention. A function's identifier does not make3 an ordinary lower bound on {-2,3}. |
| rss-roundtrip | Correct exact set. Repeats lower3/upper-2 even in its final summary. Its A6 discussion adds B's mutually exclusive alternatives3+8 when describing a cross-booking constraint; these are alternatives for one booking, not two bookings. |

Sources: [prose cycle5](responses/prose/05.txt), [RSS cycle5](responses/rss/05.txt), [WHL conversion cycle5](responses/whl-roundtrip/05.txt), [RSS conversion cycle5](responses/rss-roundtrip/05.txt).

The frozen WHL text already reverses its named availability-bound formulas. All arms receive both language specimens, including the prose arm. The common mistake is consistent with copying that defect, but this observation alone does not establish its causal route or a relative language advantage. A recoding/content-changing contrast is absent. Correct final endpoints do not erase contradictory explanatory commitments.

The converted answers also expose a provenance problem. WHL's actual reserves_effect uses expiry only after current time passes expiry, whereas the contract uses strict time<expiry. The WHL conversion answer presents the strict contract rule as the function's behavior without marking that interpretation change. Several answers repeat that expired_deletes_rule implements record deletion; its original function only returns an effect and does not change the greatest-revision selection route. These are differences between actual definitions and descriptions, not merely names.

## A criticism can introduce an error and receive further endorsement

The prose cycle1 answer correctly distinguishes the two-point set {-3,2} from its interval. [Cycle2](responses/prose/02.txt) challenges whether the memo intended an exact set, which can legitimately be discussed as an interpretive question. But the critic then asserts that interval substitution is harmless when {-3,2} is already the full admitted set, and adds nothing under that reading. This is false: the integer interval contains four additional values.

[Cycle3](responses/prose/03.txt) calls that correction valid and repeats the false conditional. [Cycle4](responses/prose/04.txt) carries it back into the original account as an endorsed improvement. The actual original response is available at both steps. This is a concrete adverse return route: an erroneous criticism becomes a revised operative statement despite access to its target.

Cycle5 nevertheless obtains the fresh exact set and again correctly distinguishes it from its interval. That later local success does not retrospectively make the earlier criticism valid, or show that its error was explicitly discovered and repaired. Root does not credit a criticism-induced repair merely because the last numerical answer is right.

Other cycle1 mistakes also remain available as targets: the prose arm attributes a WHL resource-limitation quotation to RSS, attributes R7's rejected-support distinction to R8, and overstates what the WHL deletion function represents. Its subsequent scrutiny largely concentrates on reconstructed intent and degrees of qualification rather than correcting those source attributions. Thus more criticism does not automatically mean better discrimination of errors.

## Continuity and next decision

The archive and actor context are distinct. Each continuing arm receives its actual previous response and only the explicitly re-presented earlier targets specified for that cycle. Nothing here requires perfect memory, and forgetting is not the reported defect. The adverse observation is that an available target can be miscriticized and that criticism can be endorsed on return.

Continue the four eligible arms through the frozen second block, cycles6–10. Memo B questions dependent evidence, visibility versus history, equality at expiry, conditional applicability, and whether bounds agreement answers exact-set criticism. Fresh case B and protected repeat case A are already frozen. These are grounded next probes of the observed difficulties, without adding root diagnoses to participant messages. WHL remains stopped; retain its failure and do not change its cap or replay it.

There is no language winner from this block. The candidate route remains supervised inquiry with criticism of criticism, explicit return and fresh use. Its plausible use is auditing fallible analytic prose under a declared contract, with human appraisal of source attribution and consequences. This block demonstrates why that appraisal remains necessary. It does not establish historical novelty, FW5 CreateEK or all finite target-chain capacity.
