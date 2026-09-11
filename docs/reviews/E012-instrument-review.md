# E012 completed instrument review

Read-only verification of `experiments/records/E012-joint-lean`. All six arms completed with `OBSERVATIONS_RECORDED`, no operational alarms and 18 complete response receipts with distinct provider response IDs. No calls were made and no source, tests or observations were changed during this review.

The complete instrument record verifies delivery and retention of the frozen Lean-oriented carrier. It does not establish that generated Lean text compiles, that its interpretation is adequate, or that either a formal or prose proposal has explanatory bearing. Bare/native arms constructed once; matched/Mini arms completed construct, criticize, revise and promote exactly once each.

## Frozen material and request identity

| Binding | Identity |
|---|---|
| Plan ID | `d2cf3cc284e751283e4d76f1c76932a24958fd081065ad22e024f32c157d7413` |
| Source SHA-256 | `38ed34a29ee4d5fc21abc03546a70df6066f482d6f28ab443f131dc41258d17d` |
| Packet ID | `85558cab828cc4f2ae010403169473ca56e6217526690587eb165b9f71555f09` |
| Selected Lean carrier SHA-256 | `e57dd2fda94cdfeaa6d82c77baa8c37bf80fe02cefaf0cbc36de6d004aaa46b7` |
| Initial thinking-disabled request digest | `3444ba1b775580702f083ad74d358eaddaab57226de82d536c4aba0e66296018` |
| Initial thinking-enabled request digest | `53d4279002ffda6ef1f6495ee6055244b66b8ec0720c8fed7802bac6e7447148` |

The plan, packet, corpus, issue and parent occurrence signatures verify. Current source matches the frozen source identity. The original E004 packet remains identical as a parsed object. The selected carrier equals its exact original Lean proposal: 12,170 UTF-8 bytes. Each compiled Mini source file matches its corresponding frozen plan field exactly, including the complete packet, carrier, selected issue/activation and parent material.

Initial payloads match exactly under canonical JSON serialization within bare/matched/Mini and within native/matched-native/Mini-native. Every one of the 18 request hashes verifies. Every system/user message pair reconstructs exactly from the frozen plan and that arm's actual prior occurrences. Later prompt differences reflect those different occurrences under the same conditional renderer.

Every response binds to its corresponding request hash and declared arm settings, reports model `deepseek-flash`, status `COMPLETE` and finish reason `stop`. All requests retain the 32768 completion ceiling, and none exceeds it. Thinking mode and reported presence of native reasoning agree with the declared arm.

## Reconciled resource use

| Arm | Calls | Prompt tokens | Completion tokens | Reported reasoning tokens | Cache-hit prompt tokens |
|---|---:|---:|---:|---:|---:|
| bare | 1 | 17,006 | 1,420 | 0 | 0 |
| native | 1 | 17,031 | 13,631 | 11,824 | 0 |
| matched | 4 | 79,503 | 8,140 | 0 | 0 |
| matched_native | 4 | 78,554 | 48,676 | 42,267 | 0 |
| mini | 4 | 80,455 | 9,052 | 0 | 0 |
| mini_native | 4 | 78,350 | 50,492 | 43,795 | 33,664 |
| Total | 18 | 350,899 | 131,411 | 97,886 | 33,664 |

All arm counters equal the sums of their response receipts, and the comparison summary agrees. Every response's total tokens equal prompt plus completion tokens. Total recorded use is 482,310 tokens. Reasoning tokens are already included in completion totals, and cache-hit tokens are already included in prompt totals. The different realized use and Mini-native cache reuse preclude treating equal ceilings as equal token, latency or billing conditions.

## Raw text, replay and queues

All 18 complete occurrence signatures and UTF-8 text hashes verify. Every occurrence's text exactly matches the corresponding provider public-content string. No normalization, question extraction or replacement of the initial carrier was found in the recorded route.

Both Mini logs replay through an ended state with one completed cycle. Each has 22 valid hash-chained events and 24 blob files whose content matches the SHA-256 filename. Each of the four model artifacts per arm has body bytes identical to the provider public response and the declared identical commitments transport copy. Each actual rendered-brief and provider-prompt hash verifies; complete-route validation is recorded for every stage.

| Mini arm | Log bytes | Log SHA-256 |
|---|---:|---|
| mini | 36,594 | `dfb21bc6c3871c84f5db48efceac45db3acc60133dada82710ab57d694ae3620` |
| mini_native | 36,600 | `624094743c347eb42666d3e730d2349614e0968cd876ee005074702b83cf9127` |

Both logs bind to compiled genesis `b8597370bf25ea486ff1e111cdf6609d76f0de493e5331e6111eecadb58718ef`. Model artifacts have empty `about` and `answers` arrays. Every host occurrence records no standing effect and no installed proposed changes.

Bare/native queues are empty. Each four-stage arm queues exactly its complete signed promotion occurrence, identical to the final corresponding history object. All queues retain unresolved appraisal, no standing effect and no automatically started successor. These queue records do not accept a diagnosis or execute a proposed language change.

All JSON records parse. No hidden-reasoning payload fields are present. Native reasoning presence and numeric token details remain as metadata, while hidden reasoning text is excluded.

## Disposition

The completed E012 instrument checks passed. All requested stages, exact material routes, response identities, raw outputs, replay bytes, resource totals and unresolved queues are accounted for. Interpret constructions across all six arms and revisions/promotions across the arms that requested those stages. This record supports a completed carrier comparison; novelty, repair quality, representational benefit and Mini's contribution remain substantive questions for a separate review.
