# E013 recovery: completed instrument review and native substantive supplement

E013 completed all six arms and all 18 provider calls. This recovery review finds no missing delivery, broken request binding, changed source specimen, corrupted Mini blob or implicit installation. It also identifies substantive local improvements and surviving defects in the native arms. Instrument completion does not validate those proposals.

This is a new review of [E013-joint-nonlean](../../experiments/records/E013-joint-nonlean/plan.json), prepared during recovery of the second interrupted window. The earlier [partial construction review](E013-construction-review.md) is preserved unchanged: SHA-256 `77457192da78008662284657e40edd928ba97c2b5fffdc1174cbab729ca1ea2f`, 12,988 bytes. Its statement that the run was still in progress records its earlier review state. The terminal E013 summary now supplies completion evidence. This supplement completes instrument review of every arm and substantive reading of the nine native public responses that the partial review had not covered. It does not overwrite or retrospectively complete the earlier draft.

## Decision receipts

| Receipt | Choice | Why this choice | Contribution to the end goal |
|---|---|---|---|
| E013-REC-D1 | Add this separately identified review and preserve the partial draft and all original observations. | Recovery must distinguish what the earlier window finished from what this window added. | A future agent can recover the evidence and interpretation chronology without relying on a chat transcript. |
| E013-REC-D2 | Verify recorded inputs, outputs, source identities, accounting and Mini replay without another provider call. | E013 already has terminal observations; repeating it would create new samples rather than recover the existing experiment. | Establish whether the frozen non-Lean trial actually ran and retained the material needed to study expression and criticism. |
| E013-REC-D3 | Read all native constructions and each requested native criticism, revision and promotion against the exact RSS and P7/P9 texts. | The unfinished draft covered nonnative arms; native output length and a successful record do not establish substantive adequacy. | Complete the existing carrier comparison while separating resource differences from content findings. |
| E013-REC-D4 | Use finite, explicitly attributed arithmetic cases to test endpoint and exact-set claims; keep those cases separate from provider observations. | Several proposals conflate bounds, attainment and feasible sets. A concrete case can expose the difference without a creativity score or a new live experiment. | Identify precise mechanisms that a separately frozen successor could investigate. |
| E013-REC-D5 | Reject neither an entire criticism nor an entire revision when one part fails. | The same occurrence can contain a supported correction and an unsupported restriction. | Preserve legitimate prose criticism while identifying exactly which commitments help or obstruct inquiry. |
| E013-REC-D6 | Correct the review script's header-hash interpretation and rerun the verification. | The first script incorrectly compared the canonical JSON header digest with the hash of serialized file bytes. The implementation explicitly uses `digest(plan.header)`. | Keep a reviewer mistake from becoming a false run-corruption finding and leave the correction recoverable. |

The review agent changed only this file and made no live calls, commits or publication. Publication and recovery of the already committed E013 record belong to the orchestrator's separately recorded receipts.

## Instrument identity and completion

Verification ran against the retained repository with `PYTHONPATH=src python`, using strict JSON loading, independent file SHA-256 checks, the declared canonical digest function, exact conditional prompt reconstruction, occurrence signature verification, and Mini's validating log reader/replay. The final verification passed. The initial header-digest assertion failure was a review-method error, explained below; it did not identify damaged experiment data.

| Binding | Verified identity or result |
|---|---|
| Plan ID | `3af9a0dce49e0671c4cf9288be4dbf03ffc3e6eecc3e18707aabc4eec3d720ea` |
| Frozen plan file SHA-256 | `7670335e0a6d01af90f16aa63c795e99e70ea79674728f722b9d48f89197c582` |
| Terminal summary file SHA-256 | `df1d2c5056885ac6d605df406c5825001d9059e1a39f2632d8d05dcaf9607552` |
| Source identity | `38ed34a29ee4d5fc21abc03546a70df6066f482d6f28ab443f131dc41258d17d`; all 71 frozen files matched at review time |
| Packet ID | `85558cab828cc4f2ae010403169473ca56e6217526690587eb165b9f71555f09` |
| RSS carrier | 8,227 UTF-8 bytes; SHA-256 `710391b80e9385673ba9e5143ea066b75146ebf28af2f78d72c8c9fa20a30e4a` |
| Initial thinking-disabled request digest | `d39a538c257879df339c436a6d5cf25f4eb43fae46b49565f0f7d9db4f341972` |
| Initial thinking-enabled request digest | `8629cd23d4a21ceb472ac76883720205249ff1b5349c07ae56ea8571e54f894e` |
| Strict JSON records | All 135 `.json` files in the E013 record parsed without duplicate-key normalization |
| Provider receipts | 18 complete responses with 18 distinct response IDs; every finish reason `stop` and returned model `deepseek-flash` |
| Terminal arm state | All six `OBSERVATIONS_RECORDED`; no operational alarms |

The stored plan equals the preregistered plan as a parsed object. Plan, packet, corpus, selected issue and parent occurrence signatures verify. The packet remains identical to the original E004 packet. The exact canonical packet text, selected RSS text, issue/allocation text and parent text match the plan and its material snapshots. The selected RSS matches its original E004 proposal, without a repair to its declared meanings or limitations.

Every one of the 18 actual request hashes verifies. Each response contains the same request and settings as its adjacent request record. Reconstructed system and user messages equal the recorded messages for the exact stage and that arm's actual earlier outputs. Initial requests are identical within bare/matched/Mini, and separately within native/matched-native/Mini-native. Later divergence is explained by their different preceding sampled outputs under the same conditional renderer; this is not a comparison with different model-facing Mini instructions.

All requests retain the 32,768 completion ceiling. Thinking mode and reported reasoning presence match each arm. The frozen provider settings record `reasoning_effort = high`, provider-default temperature/top-p, and no seed; this review did not change those settings. Every response has complete numeric usage, and none exceeds the ceiling. Provider metadata reports reasoning presence without retaining the hidden reasoning text. No hidden-reasoning payload keys were present in the inspected JSON structures. The stored provider raw-response digest is retained metadata: because the original raw transport body is intentionally not retained, this review does not claim to recompute that digest from the redacted public response record.

## Resource reconciliation

| Arm | Calls | Prompt tokens | Completion tokens | Reported reasoning tokens | Cache-hit prompt tokens |
|---|---:|---:|---:|---:|---:|
| bare | 1 | 15,596 | 1,872 | 0 | 0 |
| native | 1 | 15,621 | 10,618 | 9,372 | 0 |
| matched | 4 | 71,655 | 6,528 | 0 | 0 |
| matched_native | 4 | 71,012 | 42,310 | 36,869 | 0 |
| mini | 4 | 72,285 | 6,616 | 0 | 0 |
| mini_native | 4 | 69,295 | 41,418 | 36,574 | 61,567 |
| Total | 18 | 315,464 | 109,362 | 82,815 | 61,567 |

Every arm counter equals the sum of its response receipts and its entry in the terminal comparison summary. Each response's total equals prompt plus completion tokens. Recorded total use is 424,826 tokens. Reasoning tokens are already included in completion tokens; cache-hit tokens are already included in prompt tokens. Equal ceilings therefore did not produce equal realized resources, latency or billing conditions. This review makes no claim that the native and nonnative arms had equal effective deliberation budgets.

## Raw occurrences, Mini routing and replay

All 18 stage occurrence signatures and text hashes verify. Every raw occurrence text equals its corresponding provider public-content string, and every complete occurrence object equals the corresponding history entry. There is no replacement of the model's prose by an extracted diagnosis or cleaned question.

Both Mini arms' source files equal the complete frozen packet, RSS carrier, issue and parents. Manifest file hashes and canonical header digests agree with their material-binding records. Every stored routed brief matches its routed receipt and hash; every sent prompt matches its hash and the reconstructed direct prompt. Each stage records complete routed-brief validation and visibility of all frozen source ports. These are checks of the recorded route and declared validator; they do not turn material delivery into semantic endorsement.

| Mini arm | Events | Blobs | Log bytes | Log SHA-256 |
|---|---:|---:|---:|---|
| mini | 22 | 24 | 25,453 | `16c45dd7cb59f9d217289de1cdbf7884b981f8d10f9443a6e09a101ab1e51590` |
| mini_native | 22 | 24 | 25,455 | `c6664276d744a5760910085d3855df46a9ec2e1de5dec0c2a281368c19e9d6b1` |

Both logs verify against genesis `27b4c0413ada4ceba2bf31e403711a8afdcf174cc8144348f1c301fc49936d72` and replay to an ended state with one completed cycle. All 48 blob files match the SHA-256 names. Every model artifact ID matches the corresponding host occurrence's Mini artifact ID; its body and commitments blobs both contain the exact public response bytes. Those identical fields are transport copies, not two independently generated semantic commitments. All model artifacts have empty `about` and `answers` arrays.

Bare/native queues are empty. Each four-stage arm queues exactly its complete signed promotion occurrence. All queues retain unresolved appraisal and `automatic_successor_started = false`; host results and occurrences retain no standing effect and no installed proposed changes. E013 therefore produced proposed revisions and queued questions, not an executed later problem episode or installed language repair.

### Review-method erratum E013-REC-M1

The first verification script asserted that `compiled_header_sha256` equals the SHA-256 of the literal `run-header.json` file. That assertion failed on Mini. Inspection of `prepare_inquiry` in `src/minireason/inquiry_mini.py` shows that this field is `digest(plan.header)`, a canonical JSON object digest. For Mini, the literal file hash is `5768105c766aa049e91a9bee3279b39bb6f66ac48fad91f42f382a6f5cc3e857`, while the canonical object digest is `1c3c4bd3efd207fe52ea8eb618c083966da3d75ea211d7807863a44bdbc3ae13`, exactly the declared binding. The script was corrected to compare the canonical object digest, then the entire verification completed successfully. No experiment field was modified. This failure was in the review's assumption about hash domain, not in custody of the run.

## Native construction: a useful account distinction with an overstrong boundary

The [native construction](../../experiments/records/E013-joint-nonlean/native-r01/construct.artifact.json) uses RSS account/conjecture vocabulary to distinguish an enclosing interval from a stronger claim about realized global availabilities. It locates the conditional compatibility concern in a reconstruction rule, an assumption or snapshot completeness, while preserving criticism of records and supersession as different questions. Those are inspectable organizational uses of the supplied carrier. P7, P9 and RSS already supply the target and compatibility material; the particular account organization is the response's proposal.

Its completeness claim is stronger than compatibility closure warrants. It says every value in the interval is realized by a compatible profile. With two bookings each having reservation alternatives `{0,10}` and capacity 30, even the unrestricted product has exactly the availability values `{10,20,30}`. The interval `[10,30]` contains 15, which no choice realizes. Thus absence of a hidden resource constraint does not establish this completeness claim. This is a reviewer-constructed finite case, not an extra provider observation. It distinguishes the exact feasible set from its convex envelope even when every local choice combines freely.

The construction also makes unrestricted compatibility sound necessary for an outer bound. If the compatible profiles are a subset of the local product, the interval obtained from local minima and maxima still encloses every compatible profile's availability. Compatibility can affect attainment or the exact set without invalidating that enclosing inequality. The answer partly recognizes this in its later prose, but its initial closure-dependent formulation leaves the necessity claim unclear.

The final assertion that the pair forces change only for an account claiming completeness while lacking a resource model is consequently too narrow. A complete resource model can reveal unattained values in an interval, and exact-set failure can already occur under a completely unrestricted product. What needs changing depends on the actual claim and its interpretation, not merely presence or absence of a resource-model field. RSS's own description of an optional resource model remains internally underspecified; this trial does not resolve that declaration by calling the addition optional.

## Matched native: endpoint polarity corrected, tightness still misdefined

The [construction](../../experiments/records/E013-joint-nonlean/matched_native-r01/construct.artifact.json) defines a projection by subtracting reservations from capacity, then speaks of its interval as feasible reservations and asks about its upper endpoint. The [critic](../../experiments/records/E013-joint-nonlean/matched_native-r01/criticize.artifact.json) correctly identifies the resulting reversal: an excluded high-reservation combination threatens the upper reservation endpoint and the lower availability endpoint. It does not automatically threaten the upper availability endpoint.

The critic gives capacity 10, alternatives `{0,10}` for A and B, and a stipulated exclusion of `(10,10)`. The independent reservation bounds are `[0,20]`, and availability bounds are `[-10,10]`. Admissible totals become `{0,10}` and availabilities `{0,10}`. Upper availability 10 remains attained while lower availability -10 is not. The stipulated exclusion is a conditional case, not evidence that an unnamed physical resource actually exists in the source warehouse.

The [revision](../../experiments/records/E013-joint-nonlean/matched_native-r01/revise.artifact.json) accepts this reason, separates reservation and availability notation, and writes the correct endpoint map `A_min = C - R_max`, `A_max = C - R_min`. It describes this as a proposed successor and accurately retains the earlier construction. This witnesses a real, located textual correction.

The revised claim definitions nevertheless reintroduce the central distinction incorrectly. `K_exh_R_upper` is glossed as tight or exhaustive with “no feasible global reservation exceeds it, or it is attained by some feasible combination.” The first disjunct merely states an upper bound. `K_exh_A_lower` is glossed as tight or exhaustive with “no feasible availability is below it,” which merely states a lower bound. In the critic's own case, all reservations are at most 20 and all availabilities are at least -10, yet neither endpoint is attained. Hence the literal revised predicates can remain true precisely where the revision claims the high/high case defeats tightness.

| Reviewer check using the critic's exact finite case | Result |
|---|---|
| Every admissible reservation total is at most 20 | True |
| Some admissible reservation total equals 20 | False |
| Every admissible availability is at least -10 | True |
| Some admissible availability equals -10 | False |

Enumerating the four product choices and removing `(10,10)` verified these results. If the revision intended “tight” to retain an independent attainment requirement despite its subsequent gloss, that intended conjunction needs stating; the current prose supplies conflicting conditions. Prose remains legitimate, and the ambiguity itself is the criticism. The construction was not rejected for lacking a formal type.

The critic and revision additionally describe the two-point feasible set as “i.e. interval `[0,10]`.” That interval is its hull, not the exact set. The same answer can therefore correct endpoint polarity while leaving exact-set versus enclosure distinctions unstable.

The [promotion](../../experiments/records/E013-joint-nonlean/matched_native-r01/promote.artifact.json) asks a legitimate further question: whether P9's high/high case exhausts its general correlation concern, and whether whole-set claims must accompany endpoint claims. That question is relevant even after the polarity correction. Its statement that the endpoint account suffices for the narrow high/high case is premature under the weak definitions above.

The promotion also quotes the P9 occurrence ID as `6742a2a1b2f6e87cdfa889eed495f44a504365c1db35ef1e7d3fa6068e2cac4`, a 63-character string. The frozen P9 occurrence ID is `6742a2a12b2f6e87cdfa889eed495f44a504365c1db35ef1e7d3fa6068e2cac4`. One digit was lost in the generated prose. The host parent occurrence and origin metadata remain correct, and the quoted P9 sentence is recognizable. This is a model-authored attribution defect, not corruption of the retained source or host queue.

## Mini native: an effective distinction and an unsupported carrier restriction

The [construction](../../experiments/records/E013-joint-nonlean/mini_native-r01/construct.artifact.json) separates bound, envelope and decision claims, then describes them as strengths targeted by the compatibility objection. The [critic](../../experiments/records/E013-joint-nonlean/mini_native-r01/criticize.artifact.json) correctly objects to treating decision adequacy as a stronger form of the same exactness issue. P9's downstream-policy criticism can arise without hidden cross-booking incompatibility. Conversely, a conservative interval can be adequate for a coarse decision even when it overstates exact possibilities. A particular task and threshold must be specified before decision adequacy follows or fails.

The [revision](../../experiments/records/E013-joint-nonlean/mini_native-r01/revise.artifact.json) explicitly abandons a single claim-strength ladder and separates claim content from criticism target. It preserves the compatibility objection as conditional and the downstream-policy question as distinct. This is a reason-linked change in the proposed organization, not merely a new label. Its claim to add the independence of the two objections “beyond the packet and C” overstates attribution: the supplied critic C already argues that independence explicitly. The revision uses and organizes that criticism; it does not establish that it first introduced its content.

The critic's second argument is less secure. It correctly quotes RSS's declared account components as viewpoint, reading and accepted conjectures; J's four-component presentation needs to identify whether it is a derived representation or an extension. But it then asserts that an interval cannot be a single RSS projection answer. RSS defines a projection as producing a “single answer” and gives a single availability number as an example. That wording does not prove the output must be a scalar or that one interval cannot be a single structured answer. A tuple, interval or set can be one function value. The supplied specimen leaves the codomain underspecified; no exhaustive exclusion argument is supplied.

The revision accepts this unsupported restriction as an established carrier defect and repeatedly says interval-valued projections require a separate extension. It sensibly places bound/exactness/decision commitments in the account's conjectures, but that organizational move does not establish that the projection cannot return an interval. This is a concrete route by which a criticism can narrow perceived expressive resources without demonstrating their absence. It is not evidence that RSS itself necessarily forbids the route.

The revision also retains “exactly the jointly possible availability set, or its convex envelope” in one claim. Those alternatives have different failure conditions. The unrestricted capacity-30 example above has exact set `{10,20,30}` and convex envelope `[10,30]`: the envelope assertion holds while exact equality with the interval fails. Treating them as one undifferentiated target makes it unclear what a criticism refutes. Describing an interval as becoming “non-convex” is likewise incorrect for the ordinary interval meaning used in the arithmetic; the feasible set can be non-convex while its interval enclosure remains convex.

The response further says that without a resource model in the viewpoint no internal refutation of exactness is available. That is too strong for the exact-set reading: the finite unrestricted product already supplies unattained intermediate interval values. For claims about an actual unobserved resource, absence of evidence remains a genuine limitation; it is not a general reason that no criticism can bear. RSS also allows criticism of account assumptions without requiring that every disagreement first be encoded as a physical resource primitive.

The [promotion](../../experiments/records/E013-joint-nonlean/mini_native-r01/promote.artifact.json) preserves a useful inquiry into whether invisibility concerns missing observations, assumptions or overclaims. It allows both model incompleteness and claim overstatement to be present. Its final alternative, where an unresolved conditional caution is “not a criticism target at all,” makes too strong a closure claim: an unresolved objection can still name a target without proving its diagnosis. The queue correctly supplies no such closure. The promotion also repeats the scalar-only projection interpretation inherited from the critic and revision; a successor using it should preserve that interpretation as a criticizable premise.

## What this completes and what remains open

Together with the preserved partial draft, all six constructions and every requested E013 criticism, revision and promotion have now received a substantive reading. The native paths show both local improvements and error propagation. Matched native corrects endpoint polarity but leaves its tightness predicates insufficient. Mini native separates decision adequacy from compatibility but accepts an unproved codomain restriction and leaves exact-set/envelope ambiguity. These findings permit scoped criticisms of actual passages; they establish no intrinsic carrier ranking or general creativity verdict.

Both original language proposals remain in the common packet, and the whole E009 criticism already supplies candidate distinctions and repairs. The selected RSS is additionally presented as the carrier. The study therefore concerns carrier-conditioned work under common supplied resources, not exclusive access to a semantic vocabulary. Matched and Mini share the same initial provider payload in each mode; later differences follow sampled histories. E013 alone cannot attribute a substantive advantage to Mini-specific model-facing information or infer novel pretraining capabilities.

Concrete successor choices include freezing the matched-native revised endpoint claims and checking whether their literal commitments discriminate the critic's own case; freezing the Mini-native scalar-only criticism and asking for an explicit codomain argument or a structured-answer interpretation; and separating exact feasible set, convex envelope, endpoint attainment and decision adequacy under a stated finite case. Each would need its own allocation receipt, unchanged parent bytes, compared input route and preregistered interpretation boundary. None is activated by this review, and none silently repairs RSS, C0 or E013.

The remaining work is publication of the recovered E013 record and completed reviews, then an explicit successor decision. The experiments are complete as recorded; the inquiry is not exhausted.
