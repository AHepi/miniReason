# E015 completed instrument review

Read-only review of `experiments/records/E015-joint-prose-retry`, completed on 2026-09-11 UTC. All six arms finished with `OBSERVATIONS_RECORDED` and no operational alarms. The record contains 18 complete response receipts with 18 distinct provider response IDs. This review made no calls and changed no source, tests or observation files.

The verified result is a completed instrument run: one construction in each bare/native arm and construct, criticize, revise and promote in each matched/Mini arm. It does not establish substantive novelty, successful repair, explanatory bearing, creativity or a Mini advantage. Those questions require separate reading of the actual occurrences.

## Frozen inputs and conditional requests

| Binding | Identity |
|---|---|
| Plan ID | `ed740c8440e110b812cf69940ea140dd350e754a6693ba1d0d02f2b8d625b399` |
| Source SHA-256 | `38ed34a29ee4d5fc21abc03546a70df6066f482d6f28ab443f131dc41258d17d` |
| Packet ID | `85558cab828cc4f2ae010403169473ca56e6217526690587eb165b9f71555f09` |
| Initial thinking-disabled request digest | `232282430b5b9632fb3e531279ebf92bf2de94e6135cb5f8c098f78f80e2dd8e` |
| Initial thinking-enabled request digest | `37ad734eadd14dcf53697a4514f1e3b2086b259ea82957c61c8ea538d92191bf` |

The plan, packet, corpus, issue and parent signatures verify. Current executable source matches the plan's frozen source identity. The packet is exactly the E004 packet as a parsed object, preserving its initial corpus and both language proposals.

All six initial request envelopes are present. Bare, matched and Mini initial payloads are identical under canonical JSON serialization; native, matched-native and Mini-native initial payloads are likewise identical. Every request hash verifies against its recorded payload. The full system/user message pair for every one of the 18 calls reconstructs exactly from the frozen plan and that arm's actual preceding occurrences. No stage silently substitutes an output from another arm.

Each response binds to its corresponding request hash. Every response reports `COMPLETE`, finish reason `stop`, returned model `deepseek-flash` and the declared arm settings. The explicit completion ceiling is 32768 throughout; no call exceeds it. Recorded presence of native reasoning agrees with each arm's thinking mode. Different later outputs naturally cause different later requests under the same conditional renderer, so later literal prompt equality is neither expected nor claimed.

## Actual resources

| Arm | Calls | Prompt tokens | Completion tokens | Reported reasoning tokens | Cache-hit prompt tokens |
|---|---:|---:|---:|---:|---:|
| bare | 1 | 13,961 | 1,590 | 0 | 0 |
| native | 1 | 13,986 | 10,302 | 8,708 | 0 |
| matched | 4 | 66,318 | 5,678 | 0 | 0 |
| matched_native | 4 | 65,357 | 28,414 | 22,690 | 0 |
| mini | 4 | 63,868 | 5,126 | 0 | 0 |
| mini_native | 4 | 64,582 | 49,455 | 43,921 | 55,040 |
| Total | 18 | 288,072 | 100,565 | 75,319 | 55,040 |

Each arm's counters equal the sums of its individual response receipts, and the comparison summary agrees with those counters. Each response's total tokens equal prompt plus completion tokens. Reported reasoning tokens are included within completion totals; they are not an additional expenditure to add again. Cache-hit tokens are included within prompt totals.

The total recorded use is 388,637 tokens. Mini-native's substantial cache reuse and the differing native reasoning expenditure mean that equal settings and ceilings do not equalize realized token use, latency or billing conditions. No cost-equivalent or timing-equivalent comparison is inferred from these records.

## Raw occurrences, replay and standing

All 18 stage occurrences have valid complete-object signatures and exact UTF-8 text hashes. Each raw occurrence equals the corresponding provider public-content string without trimming, question extraction or rewritten prose. Stage order matches the declared one/four-call arms.

Both Mini logs replay to an ended state with one completed cycle. Each contains 22 valid hash-chained events and has 24 blob files whose bytes match their SHA-256 filenames. Each of the four model artifacts per Mini arm has a body identical to the provider public text; its commitments are the declared identical transport copy. Each stage's recorded rendered-brief and provider-prompt hashes verify, and the complete-route validation flag is true.

| Mini arm | Log bytes | Log SHA-256 |
|---|---:|---|
| mini | 16,957 | `d9fbecf0e752a311ee54c3d7d1ddd63bf0d9aa7a1070dba743120a9e31b131ca` |
| mini_native | 16,965 | `0a092bfc0ce53513434291874a39c759e21049911737d8b5fedcd98551c88930` |

Both logs bind to compiled genesis `2119cae1bb740682b785f96a07bbdd68ca0648dc0308de14d6b76f11fe6fbc35`. Model artifacts have empty `about` and `answers` arrays. Every host occurrence retains `standing_effect = none` and `proposed_changes_installed = false`.

Bare and native queues are empty. Each four-stage arm queues exactly its complete signed promotion occurrence, with no extracted or improved question. Every queue reports no automatically started successor, unresolved content appraisal and no standing effect. Queue contents equal the corresponding final history objects exactly. Language changes expressed by an output remain proposals; no initial carrier bytes were replaced.

Every nonempty JSON file parses successfully. No hidden-reasoning payload fields are present. Provider records preserve numeric reasoning-token counts and presence metadata while excluding hidden reasoning text. Public answer text remains available in the original receipts, occurrences and Mini blobs.

## Disposition

Instrument integrity checks passed for the complete E015 record. The frozen material reached the declared requests, all requested stages completed, raw outputs and replay bytes agree, resource totals reconcile, and promotion produced unresolved queued occurrences without automatic installation or semantic standing changes. Publish this complete record before starting a successor configuration. Interpretation should compare initial constructions across all six arms and revisions or promotions only across arms that were asked to produce those stages.
