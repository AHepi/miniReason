# H002 DeepSeek routing exercise — completed root review

Reviewed by root on 2026-09-13. **Candidate template: `use_and_return_v1`. Its strongest current use case is maintaining and revising a stateful procedure while preserving earlier successful behavior.** The demonstrated instance is incremental SQL LEFT JOIN maintenance. Broader applications such as workflow or code-maintenance procedures are proposed uses, not tested results.

All six actual DeepSeek calls completed. Both branches retained the correct state and output at every tested event. Criticism produced changes in the returned explanation, including acceptance of unsupported claims; no improvement in finite correctness was demonstrated. This is a useful candidate workflow with a still-fallible critic and continuation interpretation.

## What ran

H002 is a separately identified pure-routing harness exercise using the unchanged [E028 plan](../../plans/E028-sql-use-return/plan.json) and selected [E027 account](../../plans/E028-sql-use-return/selected-candidate.txt). It used the original compiler, submission parser, artifact identity, event reducer, brief renderer, E028 route validator and DeepSeek provider. In-memory blobs and reducer-built fixture state replace no production code: the durable Mini scheduler is not invoked.

The source remains the designated FW5 reading edition; ECS2 additions remain separate hypotheses. The earlier [trajectory assessment](../../../docs/reviews/trajectory-assessment-2026-09-13.md) still governs the research questions. Its proposed Luna execution was superseded by the user's DeepSeek selection. H001 remains prepared and unrun.

| Call | Actual stage | Prompt tokens | Completion tokens | Total |
|---|---|---:|---:|---:|
| 1 | Shared initial use U0 | 5,989 | 2,269 | 8,258 |
| 2 | Shared criticism | 7,856 | 1,540 | 9,396 |
| 3 | Apply returned criticism | 9,453 | 2,504 | 11,957 |
| 4 | Fresh use of returned U1 | 8,133 | 4,200 | 12,333 |
| 5 | Apply without criticism | 7,879 | 3,059 | 10,938 |
| 6 | Fresh use of archived-condition U1 | 8,686 | 4,576 | 13,262 |
| Total | Six unique calls | 47,996 | 18,148 | 66,144 |

Actual returned model: `deepseek-flash`; thinking disabled, effort low, 8,192 completion ceiling per call, 180-second timeout, provider-default sampling, no seed and no retry. All finish reasons were `stop`. [Summary](summary.json), [frozen harness plan](plan.json), exact requests, original provider records and whole public answers are preserved. No hidden reasoning text or credential was stored.

Both arms share exactly the same actual U0 and criticism: eight rendered stage deliveries required six calls, not eight. Only the returned apply port receives criticism; each fresh use receives its own U1. Full original source and candidate remain available in every call. Initial state is separately supplied only to initial use. The oracle and root appraisal are absent from participant inputs.

**Concurrency correction:** H002 ran two arms sequentially under its frozen harness plan. The two apply/use branches could have overlapped after their shared prefix; global serialization was an implementation choice, not a scientific dependency. The user clarified that future work should run up to five independent arms concurrently, with at most five active DeepSeek requests and only actual dependencies ordered. One publisher serializes commits, not all model execution.

## Finite evidence

The [post-observation checker](operator_check.py) independently recomputed the preserved SQLite oracle, checked exact provider/public-answer custody, and compared full retained rows, both indexes and output bags. It records source-fence line numbers and its own hash in [operator-check.json](operator-check.json). It checks only extracted finite fields; root separately read all prose.

All ten event occurrences matched: the two shared initial events and four fresh events in each branch. Both U1 endpoint states also matched. These are six distinct authored events, not ten independent test cases. [Negative controls](operator-check-verification.json) detected a removed duplicate output, a missing index ID and a reintroduced deleted left row without changing observations.

Initial use correctly removed the NULL-key left row from both output and retained rows, then removed exactly one duplicate-producing right row. Both fresh uses correctly reinserted left ID1 under key7, deleted the last matching right row, inserted a matched NULL value with unchanged visible output but changed retained state, and added a second right match. Key9 remained intact at every step. Final output in both branches was the bag:
`(1,7,NULL), (1,7,"c"), (2,7,NULL), (2,7,"c"), (3,9,NULL)`.

## Interpretation findings and errata

These corrections concern unchanged participant observations; they do not rewrite those observations.

**H002-INT-001 — correct first use with inaccurate source attribution.** [U0](responses/0001.txt) implements the omitted NULL-key left-row deletion coherently before criticism. This cannot count as criticism-induced repair. Yet U0 calls single-occurrence deletion and empty-bucket cleanup inferred or missing although candidate §4.4 states both. The candidate permits optional matchCount; the initializer chooses not to cache it. U0 also says all initial-event keys are non-NULL despite the first NULL-key deletion. Right-ID sets preserve projected multiplicity under unique IDs; sets of projected values need not. The candidate's own bag/set discussion also blurs this distinction.

**H002-INT-002 — criticism exceeds its visibility and propagates error.** The [critic](responses/0002.txt) correctly notices that U0 does not reproduce the complete pre-event initializer. Its own prompt expressly withholds that separate initializer. It incorrectly attributes the sentence “The initial state is not separately supplied here” to U0; that sentence belongs to the critic's task instruction. The original initializer is public in request1, so limited critic visibility does not establish absence from the public record. The critic also treats single-occurrence removal as not fixed while quoting the candidate's explicit requirement, and incorrectly makes a multiset of unique right IDs necessary.

[Returned U1](responses/0003.txt) accepts these criticisms as provenance/interpretation limitations and reproduces them while retaining correct numerical state. This is observed uptake of particular claims, including false ones. It is not evidence that the criticism was sound or that stronger FW5 reason-use conditions were satisfied.

**H002-INT-003 — correct endpoint conceals a parent-position error.** [Archived-condition U1](responses/0005.txt) names U0's actual identifier but adopts a reconstructed pre-event parent and replays the old events in prose. U0 explicitly ended after two consumed events; the apply task asked for a return to that parent. The response's reconstructed starting snapshot was not actually printed in U0 as claimed. Its resulting endpoint is correct, and it warns against deleting those rows again from that endpoint. No extra model calls or actual database operations occurred, but endpoint equality does not validate this continuation account. The returned branch also loosely calls U0 an initialized snapshot in its opening while later retaining the correct position.

**H002-INT-004 — fresh-use prose contradicts correct event states.** [Returned fresh use](responses/0004.txt) initially says event3 inserts into a bucket still containing rid11, although event2 deleted it. Its event3 body correctly starts from an empty bucket. [Archived fresh use](responses/0006.txt) correctly keeps the matched NULL when event4 adds "c", but its preceding prose says a subsequent non-NULL insertion must remove a no-match triple. It also claims set semantics would collapse the distinct triples (1,7,NULL) and (1,7,"c"), which is false. Preserve these errors alongside the correct tables and JSON.

## Candidate boundary and next question

The useful template shape is **use → criticize that actual use → return to the same parent → fresh use**, with retention, revision, withdrawal and suspension all legitimate. Preserve the selected account, interpretation, current event position, retained state and previous achievements at every handoff. The existing [returned manifest](../../plans/E028-sql-use-return/manifests/criticism-returned.json) is the concrete SQL instantiation.

This candidate currently suits supervised investigation of stateful procedures. It is not qualified for unattended changes with irreversible side effects. The critic and parent-position interpretation need substantive checking; numerical output checks alone miss the observed defects.

No finite accuracy advantage of criticism appeared: U0 was already correct and both branches remained correct. Equal endpoints do not prove criticism was inactive or unnecessary in every respect. Both arms retained the full account/source, and no matched staged no-Mini control, native completion, content-preserving recoding or relevant-content intervention ran. No causal Mini advantage, historical novelty, CreateEK or FW5 confirmation follows.

The smallest useful next scientific question is whether a return stage can distinguish warranted criticism from the actual unsupported claims here while preserving the real parent position. Freeze that intervention and its content-preserving control before collecting new answers, with equal declared source access and budget. Independent arms can run concurrently. Keep broader native/matched-workflow comparisons and the theory-side Account challenge separate.

This checkpoint completes H002 and its root review. Original E028 remains an unavailable interrupted occurrence with unknown final outcome and usage; the user says its workspace cannot be exported. H002 neither completes nor overwrites it. Full durable Linux qualification remains unrun. No new paid experiment was automatically started.
