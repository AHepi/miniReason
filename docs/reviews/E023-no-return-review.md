# E023: what the model can do without the returned account

Completed 2026-09-12 UTC. Frozen plan `8d21ad958acb05e7b9f0cd5eeeb86a69db32f49601533a227797d2a21de331cd`; complete record published at remote `4033a17a7f86bc5926ffc6cd469689a2ef62f7ce`, local `44fa2879b17aa888e94331c74ca2308facdc1c09`, shared tree `87887d057428b203b66e6f22790fe88dad415c1c`.

The returned account was unnecessary for the numerical answers and reporting/planning distinction witnessed in these four use responses. Each use call received the fixed use packet and an empty account field. All four reached the expected final numerical results. This closes the missing no-return control; it does not establish that accounts never help, that these distinctions transferred spontaneously, or that Mini improves the model.

## Actual execution and custody

[E023](../../experiments/records/E023-reason-no-return-retry) completed all four arms and eight calls. Every call returned `deepseek-flash`, `COMPLETE` and `finish_reason=stop`. Every public response equals its stage artifact text and recorded text hash. Native hidden reasoning was not persisted. The earlier E020 interruption remains unchanged; E023 is its separately identified retry, not a replacement observation.

| Arm | Prompt tokens | Completion tokens | Calls |
|---|---:|---:|---:|
| matched | 17,029 | 4,691 | 2 |
| matched_native | 17,079 | 18,546 | 2 |
| mini | 17,029 | 4,444 | 2 |
| mini_native | 17,079 | 17,199 | 2 |
| Total | 68,216 | 44,880 | 8 |

Total recorded use of the provider was 113,096 tokens, including all four archived first responses even though they were not returned to use. The thinking conditions retain their declared settings and actual costs; these token differences are not equalized or converted into a merit score.

All use requests consist of exactly the frozen system message and `stage_prompt(plan,"use",[])`. Their user text ends with an empty `Returned account:` field. The common user-prompt SHA-256 is `8ad36bb8cc464a81bc23de96a6daff59a731a02e78598e2413612228eed2b090`. Complete payloads match between matched/Mini and matched-native/Mini-native. Their request hashes are respectively `f325f8afd35e31b8b96159b08da7fc71e2a68618b0d1478a003cad484bb89478` and `72e781cc0fa2af157033df40ccf688ed3b0a45eefd9924eba9ef6d379ebc1ec8`.

These receipts establish actual omission and request parity. They do not establish semantic dependence or causal invariance. All use prompts are independently issued; cross-stage agreement cannot show carriage of an account that was withheld.

## Numerical and operational answers

Every [use response](../../experiments/records/E023-reason-no-return-retry/summary.json) gives Case A as 9−6−5=−2 and retains both reporting entries. Numerical excess alone is not treated as proof of corruption or inadmissibility.

For Case B, the reporting pairs `(0,0)`, `(8,0)`, `(0,11)` and `(8,11)` give 23, 15, 12 and 4. The separately supplied inspection excludes `(8,11)` from planning, leaving `{23,15,12}`. The snapshot alone does not identify joint physical feasibility. All four responses acknowledge that no account was supplied and distinguish the reporting calculation from the feasibility restriction.

There is one concrete pair-label defect in [matched use](../../experiments/records/E023-reason-no-return-retry/matched-r01/use.artifact.json). Its first reporting table labels the U=0, V=11 row `(0,8)` while correctly displaying the value 12. The later planner table and snapshot list use `(0,11)`. Thus the final numerical answer is correct, but not every pair-level statement is correct.

The use packet itself supplies the relevant data and reporting/planning distinction. The result concerns these cued obligations. This one no-return block is shared across the reason-treatment study; it must not be multiplied into independent new baselines for every earlier treatment.

## Interpretation and account defects

All four use responses present later inspection as distinguishing a weaker cautionary reading from stronger warning or existence readings of an earlier modal remark. Inspection establishes that the conflict actually occurs. It does not by itself establish what the earlier remark meant: a cautious warning and a stronger reading can both accommodate a later real conflict. The native variants also entertain an existence assertion not established by the remark alone. Preserve linguistic discrimination as unresolved rather than treating this as a new successful inference.

The archived first responses do address the aggregation-as-rule objection and offer reasons to qualify or resist the construction's necessary-new-target claim. Agreement with the criticism is not a success criterion. Their collateral defects remain consequential even though these outputs were withheld from use.

| Account evidence | Finding |
|---|---|
| [Mini response](../../experiments/records/E023-reason-no-return-retry/mini-r01/respond.artifact.json), “My own addition, distinguished from the sources” | Says the construction does not name the reporting-versus-planner distinction. The frozen construction explicitly contrasts what the bag supports with what a downstream planner can use. This is false contribution attribution, independently of any useful further organization under the response's new terminology. |
| [Matched response](../../experiments/records/E023-reason-no-return-retry/matched-r01/respond.artifact.json), self-contained aggregation positions | Allows negative reporting availability but says capacity can forbid otherwise independent composition. If this filters the same reporting choices, negative results become unavailable. A separate feasibility scope could reconcile the statements, but that scope is not specified there. Matched-native states the report-threshold/hard-capacity distinction more clearly. |
| [Mini-native response](../../experiments/records/E023-reason-no-return-retry/mini_native-r01/respond.artifact.json), interval discussion | Says the min/max interval is valid only under independence. An outer enclosure over the full product remains valid for every feasible subset; tightness or endpoint attainability can fail. The Case B interval `[4,23]` still contains all inspection-feasible values `{12,15,23}`. |
| Same Mini-native response, language-specific qualification | Attributes reversed WHL bound names to supplemental R. That observation is in the common-source E009 selected-criticism occurrence, not the supplied supplemental R. Source access does not justify misattributing which occurrence supplied a criticism. |

The exact frozen source and construction are retained in the [plan](../../experiments/plans/E023-reason-no-return-retry.json). These are content findings, not parser failures. Because the accounts were omitted from use, correct later numerical answers do not demonstrate repair of an exposed account or integration of its criticism.

## Bearing on the next experiment

E023 defeats the claim that this returned account is needed to perform these supplied use calculations and distinctions. It supplies no positive account-necessity result and no general route advantage. Correct arithmetic therefore remains unsuitable as the endpoint for establishing the proposed account's explanatory contribution.

That does not defeat the predeclared construction-to-successor allocation. Its distinct question is whether a subsequent inquiry identifies and discriminates a real unresolved issue in the complete construction/criticism/revision bundle. The remaining attribution, modality, capacity and interval defects give reasons to examine that mechanism, while leaving failure or no promotion legitimate. The preselected source arm must remain fixed before A is generated.

The next activation decision must retain one A construction episode, verified publication of its complete record, an exact handoff from the preselected A Mini arm, and one different B successor-discrimination episode. Do not repeat the arithmetic block without a new distinguishing rationale. Do not substitute a more appealing A arm after seeing its output. C001 remains prospective until actual A output exists and its publication is verified.

## Operational recovery note

The user's explicit DeepSeek disclosure approval enabled this run. No repeated approval for the same authorized destination/material scope is needed. A publisher read initially exceeded the local tool-output limit; bounded base64 reads recovered the identical Git blobs. The complete E023 publication then took the interval between verified pushes beyond five minutes. The ledger records that miss rather than counting in-flight uploads as publication. Subsequent large uploads require a small verified checkpoint first, and the progress skill is being updated with an independent publication clock.
