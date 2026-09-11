# E019 omitted criticism: interrupted-run review

E019 is incomplete. The inspected record contains nine attempted calls: seven complete public responses and two transport failures. Five respond occurrences and two use occurrences are available. Mini native has no complete respond occurrence, no use attempt and no terminal arm result; the root terminal summary is absent. This review preserves those limits rather than treating missing responses as negative content findings.

The actual-wire omission checks passed. The supplemental criticism field is exactly empty, the original R retained for audit is not rendered, and the host's empty-criticism transport marker is absent from provider requests. Common source, J and the earlier E009 criticism remain available as declared. This is omission of one additional criticism occurrence, not absence of all criticism or reasons.

The review follows the frozen [interpretation contract](../../experiments/materials/reason-use-v1/INTERPRETATION.md) and concerns [E019-reason-omitted](../../experiments/records/E019-reason-omitted/plan.json). It inspected all nine actual request/response receipts and all seven complete public responses. Verification was read-only except for this new review. It made no provider calls, retries, source changes or edits to observations.

## Decision receipts

| Receipt | Choice | Why | Contribution to the end goal |
|---|---|---|---|
| E019-REV-D1 | Check actual omission on the wire, including the host empty-field marker and the unrendered original-R audit field. | A declared empty condition is insufficient if another field delivers the withheld occurrence. | Establish what information the omission trial actually supplied before interpreting reconstruction or response differences. |
| E019-REV-D2 | Review every completed occurrence and preserve failed or absent stages separately. | Transport errors and missing responses cannot support judgements about a conjecture, criticism or model capability. | Retain unsuccessful experimental history without losing the usable partial evidence. |
| E019-REV-D3 | Stop verification at the observed interrupted state when the orchestrator reported execution approval cancellation. | The supervising session failed; waiting for a nonexistent terminal summary or rerunning calls would not recover this original record. | Leave an honest recovery point and avoid replacing failed observations with a successful successor. |
| E019-REV-D4 | Interpret any reconstructed argument relative to omission of R only, and keep original-versus-omitted contrasts descriptive. | J, the common source and earlier E009 criticism still contain relevant reasons, and each arm is a single sampled occurrence. | Distinguish a useful observed reconstruction from unsupported claims of reasoning without reasons, general invariance or a causal performance estimate. |

The orchestrator reported that session 22631 failed with “Unified exec process failed: network approval was cancelled before a decision was returned.” That supervising-session report is attributed to the orchestrator; this reviewer independently verified the filesystem receipts below. The orchestrator owns separate recovery documentation and any separately frozen future retry. This review does not manufacture a terminal summary or install a successor.

## Observed status and custody

| Binding | Verified value |
|---|---|
| Frozen plan ID | `a947af87f023579aefd14f98028f8e6a935f7e1fbfe2bcf5a2a1b8a861eea34b` |
| Supplemental criticism | Exactly zero UTF-8 bytes; relation `omitted` |
| Return path | Enabled; use receives that arm's exact returned response |
| Initial thinking-disabled request digest | `317e07ecd53719e9d06921d5f0a273c7fb22e440d1ac6f167914c9372a59349d` |
| Initial thinking-enabled request digest | `d69597ebdf587a31c724371c35a62448b6fc0864f695e688f85b838cfd4cb15e` |
| Inspected JSON snapshot | 69 record files parsed with the strict loader before separate recovery metadata was added |
| Complete provider responses | Seven distinct response IDs; all `COMPLETE`, finish reason `stop`, returned model `deepseek-flash` |
| Failed provider attempts | Two `TRANSPORT_OR_RESPONSE_ERROR` receipts, neither containing public content or usage |

The archived plan equals its preregistered plan as a parsed object, and its signature verifies. All input occurrence signatures and material snapshots verify. The current repository source-file mapping and all three reason-use module hashes matched the frozen identities during review. The common source text, fixed J, finite use data, use questions, stage instructions, system message, provider settings and return-path setting exactly match E016. The model-facing change at the initial respond stage is the removed supplemental R text.

All nine request hashes and adjacent response bindings verify. Every system/user message pair reconstructs exactly from the frozen conditional renderer and the available prior occurrence. Initial requests are identical within bare/matched/Mini and separately within native/matched-native/Mini-native. Each respond prompt ends with `Supplemental criticism:` followed by its final newline and no content. The complete original R audit text is absent from those rendered prompts, and the declared literal-exclusion guard verifies against its frozen checked fields. This guards defined field and literal exposure; it does not certify that related arguments are absent from the common material.

Both Mini routes preserve the zero-byte `sources/criticism.txt`. Their internal routed respond brief uses `[HOST TRANSPORT ONLY: criticism_text is exactly the empty string.]` to satisfy the engine's transport contract. The exact marker is absent from every actual provider request. Thus it is not an extra model-facing instruction to behave differently in the omission condition.

The three attempted use requests contain only the common finite task data, questions and the corresponding complete respond text. Matched native's use request is available and reconstructs even though its response failed. No separate common-source/J/R port is rendered at use. A returned response may itself quote or summarize prior material; that permitted mediated exposure is retained unchanged.

Every complete occurrence's signature and text hash verifies; its full object equals its arm history entry, and its text equals the provider's public response. Respond provenance names the source, construction and empty criticism occurrence. Successful use provenance names the finite data, questions and exact parent response. Recorded host results and occurrences make no standing change and install no proposed changes.

## Completion and failure accounting

| Arm | Respond | Use | Attempted calls | Arm terminal record |
|---|---|---|---:|---|
| bare | Complete | Not planned | 1 | `OBSERVATIONS_RECORDED` |
| native | Complete | Not planned | 1 | `OBSERVATIONS_RECORDED` |
| matched | Complete | Complete | 2 | `OBSERVATIONS_RECORDED` |
| matched_native | Complete | Transport failure | 2 | `OPERATIONAL_FAILURE` |
| mini | Complete | Complete | 2 | `OBSERVATIONS_RECORDED` |
| mini_native | Transport failure | Not attempted | 1 | Absent at interruption |

The [matched-native use failure](../../experiments/records/E019-reason-omitted/matched_native-r01/calls/call-0002.response.json) records `<urlopen error Tunnel connection failed: 403 Forbidden>` after 6,321 ms. Its complete respond occurrence survives. The [Mini-native respond failure](../../experiments/records/E019-reason-omitted/mini_native-r01/calls/call-0001.response.json) records `IncompleteRead(0 bytes read)` after 53,877 ms. It contains no public answer, and there is no Mini-native use request. These identify the observed failure surfaces; they do not establish a common cause or diagnose account permissions, quota, model behavior or source content.

The planned six-arm design contains ten calls if every stage completes. Nine were attempted, with two failed deliveries and one unattempted use. The four successful terminal arms are complete in their own scopes. The entire configuration does not have a normal terminal summary, and Mini native does not have a terminal arm or child-route result. A separate recovery receipt can document that interruption without retrospectively completing it.

### Reported resources

| Arm | Calls attempted | Reported prompt tokens | Reported completion tokens | Reported reasoning tokens | Cache-hit prompt tokens |
|---|---:|---:|---:|---:|---:|
| bare | 1 | 15,035 | 2,829 | 0 | 14,848 |
| native | 1 | 15,060 | 9,080 | 7,218 | 14,848 |
| matched | 2 | 18,061 | 5,434 | 0 | 15,360 |
| matched_native | 2 | 15,060 | 9,351 | 7,688 | 14,848 |
| mini | 2 | 18,619 | 6,292 | 0 | 15,488 |
| mini_native | 1 | No usage receipt | No usage receipt | No usage receipt | No usage receipt |
| Known reported totals | 9 | 81,835 | 32,986 | 14,906 | 75,392 |

Known reported use totals 114,821 tokens. Reasoning is included in completion totals, and cache hits are included in prompt totals. Existing arm counters reconcile with all available usage receipts. Matched native's numeric totals cover its completed respond call only; failed use has unknown token cost. Mini native has no usage receipt for its failed attempt. The absence of reported tokens is not a zero-cost claim, and the reported total need not equal actual billed use.

### Mini logs

Both log chains verify from genesis `c493dc1051ef4b8cc6e10bc68b93a7c75c89516456abe8a8dd1a4ac2962f7d22`. All source files match the frozen material, both manifest byte hashes and canonical header digests verify, and every stored brief and sent prompt matches its corresponding hash and recorded route. Every model artifact actually submitted has exact public-response body/commitments bytes, the matching host artifact ID, and empty `about` and `answers` arrays.

| Mini arm | Events | Blobs checked | Replay ended | Completed cycles | Log SHA-256 |
|---|---:|---:|---|---:|---|
| mini | 21 | 22 | True | 1 | `99cde95d97c84f4242aa30857f37946eea1b7dd4a165dfaf27d340c01a0964fe` |
| mini_native | 17 | 16 | False | 0 | `810fed3c0f60706d7957395f1faf73ef3efa9bfcc882c60196eba73c44d4a18b` |

All 38 inspected blobs match their SHA-256 filenames. Mini native's valid partial log stops at `STAGE_ENTERED` for respond. A valid chain with no completed model stage is partial custody evidence, not successful execution or a completed replay.

## What the omitted condition actually produced

The available native replies explicitly recognize that no supplemental criticism was supplied. Both independently articulate, relative to that omitted R occurrence, the competing aggregation-as-rule reading. [Native](../../experiments/records/E019-reason-omitted/native-r01/respond.artifact.json) says P7's list can accommodate an aggregation rule, source assumption or snapshot-wide objection. [Matched native](../../experiments/records/E019-reason-omitted/matched_native-r01/respond.artifact.json) qualifies the claim that the objection cannot be located in P7 and explains that a broad reconstruction-rule reading suffices. Both retain locus as a diagnostic while denying that a wholly new target is strictly necessary.

This is a concrete counterexample to a local claim that delivery of the additional E015 R occurrence is necessary for those two sampled arms to state the rule-target alternative. It is not evidence that they reasoned without source criticism, generated the argument independently of training, or received no relevant reason. J displays its contested exclusion claim, and the full common source, P7/P9 passages and E009 criticism remain present. The record supports reconstruction under those available resources.

The nonnative replies follow a different observed direction. [Bare](../../experiments/records/E019-reason-omitted/bare-r01/respond.artifact.json) largely retains the claim that P9 lands on an aggregation assumption rather than a rule. [Matched](../../experiments/records/E019-reason-omitted/matched-r01/respond.artifact.json) locates P9 under snapshot-as-a-whole while continuing to exclude composition operators from rule criticism. [Mini](../../experiments/records/E019-reason-omitted/mini-r01/respond.artifact.json) treats the concern as a new species of snapshot-wide criticism and preserves a strong distinction from rule criticism. Their adjustments do not supply an argument that P7's broad reconstruction-rule category cannot contain a composition rule.

E016's three nonnative responses more directly qualify J through the aggregation-as-rule rival, whereas these E019 nonnative occurrences retain more of J's exclusion. This is a descriptive difference under exactly matched common initial fields and different supplemental content. It is compatible with an effect of R, but one sampled response per arm and different realized resource/cache conditions do not establish a general causal mechanism. The two native reconstructions show why absence of an explicit supplemental occurrence must not be equated with inability to reach the same objection.

## Finite substantive findings

### E019-INT-1: attribution of the absent supplemental criticism

Bare includes a section titled “Where the supplemental criticism bites” and discusses WHL defects from the already supplied E009 criticism. It even correctly says that criticism addresses a different artifact. The source of those points is recoverable, but calling them the supplemental criticism blurs the experimental distinction between the preserved common occurrence and the deliberately empty new field. Actual request reconstruction rules out delivery of the withheld complete R through that field. This is a generated attribution problem, not an omission-guard failure.

Native, matched native and Mini explicitly distinguish the empty supplemental slot from the earlier E009 material. Mini says it has not been given the supplemental text and does not invent one. Those statements agree with the wire record; they do not establish absence of earlier source criticism.

### E019-INT-2: exclusion from the rule category remains unsupported in several replies

Matched says a composition operator is not a rule because P7's vocabulary does not name composition operators. Absence of a separately enumerated name does not demonstrate exclusion from the broader reconstruction-rule category. It also locates the objection under snapshot-as-a-whole, so its own account supplies a P7 location while retaining a claim of vocabulary insufficiency. A narrower claim that different descriptions highlight different consequences remains available, but is distinct from proving that rule redescription loses the objection.

Bare and Mini make related strong statements about the independence commitment being outside P7's vocabulary or any single target without establishing the relevant exclusion. Their later snapshot-wide classifications are useful qualifications, not evidence that every rule-target reading fails. This reproduces the substantive issue R attacks while the supplemental R is absent.

Native's own alternative has one residual error: it says an exhaustive P7 list would require adding aggregation rule as a target. An exhaustive list of broad categories can still contain aggregation rules within its reconstruction-rule category. Exhaustiveness alone does not settle membership. Its earlier broad-category reading is better supported than this later enumeration inference.

### E019-INT-3: possible incompatibility, asserted independence and established defeat

Several returned accounts say that a conditional incompatibility claim defeats an assertion of free composition, then elsewhere say that no account is refuted until the condition is observed. These statements need a fixed claim boundary. A hypothetical example can criticize an account's entitlement to make an unrestricted inference or establish a conditional limitation. It does not, without the needed premise, establish that a particular physical pair actually fails. Conversely, labeling an assumption defeasible does not make its false application immune to criticism when a case is supplied.

Mini's returned account retains both “a conditional claim defeats an assertion” and an absent-case qualification. Its use response correctly distinguishes the modal reviewer from the inspection and gives the right planner exclusion, but endorses the parent sentence as a fair summary rather than explicitly repairing its scope. The finite task behavior is sound on that distinction; a fully consistent general account is not established by that success.

Matched native's proposed account additionally says a numerical projection discards information unless it carries a label naming compatibility assumptions. A label can disclose the projection's conditions and limit its claim. It does not by itself restore omitted combinations or correlations. No use output exists for this arm, so the trial supplies no downstream test of that sentence.

## The two completed use responses

Both [matched use](../../experiments/records/E019-reason-omitted/matched-r01/use.artifact.json) and [Mini use](../../experiments/records/E019-reason-omitted/mini-r01/use.artifact.json) satisfy the stipulated numerical and information-state obligations. Case A returns -2. Case B reporting retains all four pairs and outputs `{23,12,15,4}`. The inspection-informed planner excludes only `(8,11)` and returns `{23,12,15}`. Both require extra premises for a stronger conclusion that Case A entries are invalid or physically infeasible, and both attribute the Case B exclusion to the inspection rather than the earlier modal remark.

Both explain that a snapshot-only reader can calculate the full product report without certifying physical performability. Both say the earlier remark alone requires no change to a listed quantity or arithmetic operation, and locate its possible force in an implied feasibility or sufficiency claim. Thus these answers do not need to accept R's preferred wording to preserve the finite task's distinctions.

Mini use makes one concrete refinement of its returned account: the parent says the two account purposes are reader-supplied, but the finite use task explicitly supplies a reporting procedure and a separate planner request. Mini identifies that change of context and declines to import the parent's claim that the source leaves the jobs unspecified. That is a located qualification grounded in the actual new material.

Mini also observes that the excluded pair happens to have the smallest reporting value but is excluded because of the jig, not a minimum-value rule. This correctly preserves the causal role of the stipulated inspection rather than inferring an undeclared threshold from the coincident ordering.

Matched use takes the assert-independence/decline-dependence distinction from its account and labels that origin. It still leaves the reporting-purpose interpretation broadly unresolved despite the procedure's explicit arithmetic specification; the distinction may be relevant to a further physical interpretation, but must not change the four results already stipulated. Its actual numbers remain correct. Mini's late open question about what to do with the reporting output similarly concerns an additional reporting policy: the planner's requested exclusion is already determined and was correctly supplied.

No matched-native use, Mini-native respond or Mini-native use content can be assessed. These unavailable stages must not be counted as conceptual failures or filled in from neighboring arms. Bare/native had no use stage by design.

## Recovery disposition

The partial records support exact omission custody, five inspectable responses, two successful finite uses and two explicit transport failures. They support no normal completed-configuration claim, no complete native use comparison and no account-absent comparison. The existing public artifacts and valid partial Mini log remain unchanged.

Publish the interrupted record and separate recovery receipt before any separately identified retry. A future retry must not erase these failures or retroactively complete E019. Later interpretation should retain the native reconstruction finding, the nonnative differences, the two successful use observations and the unavailable stages as distinct evidence.
