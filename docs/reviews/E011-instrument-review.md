# E011 instrument review after external interruption

Reviewed the preserved `experiments/records/E011-joint-prose` files on 2026-09-11 UTC without changing source, tests or observations and without making provider calls. This review concerns instrument integrity and available receipts. It cannot assess construction, criticism, revision or promotion quality because no completed model output is preserved.

E011 is externally interrupted, not a completed six-arm comparison. The parent operator reports that automatic approval review rejected polling of the live execution and that a subsequent poll returned an unknown process identifier. Those runtime events are the operator's separate recovery account. The repository itself establishes one recorded native-arm tunnel failure, four other prepared request envelopes without usable response receipts, an unfinished Mini run, and two zero-byte files.

## Frozen input identity and request parity

The plan, packet, corpus, selected issue and all supplied parent occurrence signatures verify. The selected issue and parents retain their original raw-text identities. The current source identity still matches the frozen plan, so this review found no source drift.

| Binding | Identity |
|---|---|
| Plan ID | `e9795fa894cc537e76fae4c6a482b5e2a19dae2b857c996de91f9e745cc95f6b` |
| Packet ID | `85558cab828cc4f2ae010403169473ca56e6217526690587eb165b9f71555f09` |
| Source SHA-256 | `38ed34a29ee4d5fc21abc03546a70df6066f482d6f28ab443f131dc41258d17d` |
| Shared initial message digest | `b5911f4f3e763414feee2f85e9d30242698997bff9de183d4714ed027688217a` |
| Initial thinking-disabled request digest | `166bca593ba21b4eb731dd4e94c68ba744fb1bbd3f8880ecf583d0a647329b9f` |
| Initial thinking-enabled request digest | `6650573b7db8f852b41d458f3f2bc9be045cc912b8f90c31148e90f8f4f23df1` |

Every available request hash matches its recorded payload. Bare, matched and Mini initial request payloads are identical after canonical JSON serialization. Native and matched-native initial payloads are likewise identical. All five requests contain the exact system message and initial construction prompt reconstructed from the frozen plan. Their explicit completion ceiling is 32768; thinking mode matches the arm, with the declared reasoning setting present for native requests. No mini-native request envelope exists, so parity for that arm is unobserved. The request files prove what was prepared for dispatch, not acceptance by DeepSeek.

## What each arm actually records

| Arm | Available request envelopes | Available response evidence | Completed model stages | Terminal arm record |
|---|---:|---|---:|---|
| bare | 1 | No response receipt | 0 | Absent |
| native | 1 | `TRANSPORT_OR_RESPONSE_ERROR`: tunnel connection failed, 403 Forbidden | 0 | `OPERATIONAL_FAILURE` |
| matched | 1 | Zero-byte response file; unreadable and not a receipt | 0 | Absent |
| matched_native | 1 | No response receipt | 0 | Absent |
| mini | 1 | No response receipt | 0 | Absent |
| mini_native | 0 | No response receipt | 0 | Absent |

Configuration preflight passed before provider construction. It is a preparation result, not evidence that any model stage completed. No construction, criticism, revision or promotion artifact is preserved in any arm. The four-stage completion requirement therefore remains unobserved. No comparison-level terminal `summary.json` was present at review time.

The zero-byte files are `matched-r01/calls/call-0001.response.json` and `mini_native-r01/inquiry-started.json`. They remain original interruption evidence. Their existence cannot be promoted into either a successful observation or a complete operational failure record; this review did not fill them in.

## Mini log, source material and routing

The non-native Mini log is 10,881 bytes, SHA-256 `c93303da90941f01f822ef3af575fd7eb46d7f30f58713f3ebd2e7fb6defea52`. Its complete hash chain replays against the compiled manifest genesis `c93fe0de9b9e8bc3844d1b21131fda9c4f806e8c987c81b6da529bc6a77ca399`. Its 14 events contain one run start, four evidence batches, five stage entries and four deterministic source-copy artifacts. The last event is entry into `construct`. There is no model artifact or run-ended event.

All 12 existing Mini blob files match their SHA-256 filenames. Each of the four copied source artifacts has identical body and transport-duplicated commitments, with no inferred `about` or `answers` relationship. Their exact source material is preserved as follows.

| Source | UTF-8 bytes | SHA-256 |
|---|---:|---|
| Frozen packet | 34,096 | `28c70c2428e8e3d1fc435ef4f1c0f1586fff49f25e216f6d1bcf5b9f4602406a` |
| Selected prose carrier | 71 | `091bc8bede5b5a6f845a0d86463de58f9e364d0a8f0da36d85017a9d08634a50` |
| Selected issue and activation | 18,206 | `dbf2b0b3d0c0556cbce2c2b4bb042438cc56bd90f9aa6e0c711c73112afdfd93` |
| Parent material | 6,729 | `f3eabe124ce06b36d81e28fe0726627713509b391986710fc9537a84f4529b1a` |

The initial Mini route-visibility record has valid rendered-brief and provider-prompt hashes. Its recorded prompt equals the shared initial construction renderer, and its complete-route validation flag is true. This verifies the available initial material route. No later stage history was produced, so live cumulative-history routing and final queue integrity cannot be verified in E011.

## Resource and queue accounting

Only the native arm has a terminal resource record: one attempted call, zero reported prompt tokens and zero reported completion tokens. Its failure receipt contains no usage report. These zeros are absence of provider-reported token usage, not evidence of zero actual billed cost. Five prepared request envelopes exist overall; four have no usable receipt. Total accepted calls, total provider work and campaign token cost are unknown. The single native failed attempt must not be generalized to every other prepared request.

The native arm's queue is present and empty, with `automatic_successor_started = false`, `content_appraisal = unresolved` and `standing_effect = none`. No promotion occurrence exists to verify or select. Other arm queues were not completed. Source-copy artifacts have no standing effects, and the records provide no evidence of installed language changes or a successor activation.

Inspection of every nonempty JSON record found no hidden-reasoning payload fields. The only nonempty response is a transport error without model content. No claim is made about data that was never returned or persisted.

## Review disposition

The available frozen identities, initial conditional requests, source copies and partial Mini hash chain are internally consistent. The completed-comparison, four-stage-output, resource-total and promotion-queue checks are unavailable because execution was interrupted. The tunnel rejection is an operational failure, and missing receipts are unknown observations. Neither supplies a result about the prose carrier, Mini's contribution or creative inquiry.

Preserve the partial record with a separate interruption account and publish it before any separately identified recovery run. A resumed or repeated comparison requires a new record identity rather than fabricated completion of the missing files. Source changes are unnecessary to establish the observed interruption and would invalidate the already frozen remaining plans.
