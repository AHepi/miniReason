# Current recovery and research state

**Recovery and offline implementation are complete and published. E022 is complete and reviewed. E020 is preserved as interrupted. E023 is prepared for the owed no-return retry; E024/C001 are prepared for a later distinct-template chain. No live A-to-B chain has run.**

Updated 2026-09-12 UTC. Read [DECISION_LEDGER](DECISION_LEDGER.md), [AGENT_ACTIVITY](AGENT_ACTIVITY.jsonl), [PURPOSE](../PURPOSE.md) and [template-chain workflow](workflows/template-chain.md). Destination: AHepi/miniReason main. Source AHepi/h-EPI remains unchanged. One publisher owns main and the decision ledger. Every agent logs repository/staging searches, reads, edits and tests using tools/repo_activity.py. Publish each completed document immediately and each complete/partial configuration before successor work.

## Recovered stopping point

The failed window had completed E022's ten calls and made local commit b4c0ae2a8e87e57fdbf2b3b06651d4110de8ebdd. Upload stopped after batch 6 of 14 while main remained 0de446c9f90beeae2a8a510a576c47174dcaded4. Recovery finished that exact tree and verified remote 814649dba32264dddd7ccd466dbbd57e32c63bcb, shared tree ae6eb00407373a78b30337617c06cc7f71abbb6e. No completed call was repeated.

The recovered E022 review draft was preserved unchanged and published separately. Its [completion supplement](reviews/E022-completion-review.md) was published at 22924850b4094d34dbc92ee07799ac56954846de. It verifies all ten public outputs, exact wire/occurrence custody and two ended Mini cycles. All four use answers are numerically correct, while some accounts retain capacity, classification, attribution and modality defects. Correct use does not validate every account or show Mini advantage.

## Controlled block and the actual blocker

| Test | Actual state |
|---|---|
| E016 original supplemental criticism | Six arms / ten complete calls; published and reviewed |
| E017 recoded criticism | Six arms / ten complete calls; published and reviewed |
| E018 different criticism | Six arms / ten complete calls; published and reviewed |
| E019 omission | Preserved partial: nine attempts, seven complete public responses, two transport failures; no normal summary |
| E021 omission retry | Preserved partial: five requests, no complete public response; approval rejection and incomplete file |
| E022 public-payload omission retry | Six arms / ten complete calls; 102,272 prompt + 61,500 completion tokens; published and reviewed |
| E020 no returned account | Preserved partial: four initial requests, no complete public output, one tunnel-403 receipt, three absent initial responses and four unattempted use calls |
| E023 no-return retry | Prepared with identical E020 model-visible messages/settings/controls; zero-call preflight passes; not activated |

Automatic approval review rejected E020 execution polling because it judged the DeepSeek destination and project-data disclosure not explicitly authorized. Its tunnel-403 response is separate evidence; their causal relation is unknown. No live retry or alternate route followed. All 74 original E020 files are hashed in its [recovery record](../experiments/records/E020-reason-no-return/recovery.json), published at e589dacffe6aa36a68955d52a01a000d76a8d48b. Missing costs are unknown. No no-return observation or account-necessity conclusion exists.

Explicit approval to send published experiment material and generated outputs to https://api.deepseek.com/v1 is the live blocker. This status does not grant that approval. The existing credential is read only at runtime through DEEPSEEK_API_KEY. The current request for continuous logging does not change the disclosure boundary imposed by automatic review.

## Published implementation

Four new modules implement successor_discrimination_v1 and the external A-to-B coordinator; all existing source bytes are unchanged. The code checkpoint is remote d1b175e12c6b9f96ecf792d42752dd5f506574b8, local ed05c18fb7dbb998b50aea2cc4c460f0c9acfb7d, shared tree ccb19c391802e6761f749b2e02c33582d70d252f. The [independent implementation review](reviews/distinct-template-implementation-review.md) is published at ea1ce9a322c722d05b15609418ee781be1b0f55b.

Normal and optimized full suites each pass 569 tests; independent focused checks pass 27. The [verification record](sources/2026-09-12-template-chain-verification.json) pins the seven source/test files. Tests run the actual Mini engine with scripted provider responses. They verify exact source/output/tree/preflight custody, common downstream input, one-cycle distinct contracts, endpoint baselines, no-promotion, duplicate dispatch refusal and failure preservation. They establish no live chain result or semantic standing.

## Prepared exact continuation

| Prepared artifact | Identity and state |
|---|---|
| E023-reason-no-return-retry | Plan 8d21ad958acb05e7b9f0cd5eeeb86a69db32f49601533a227797d2a21de331cd; published fcf7c3315b1f1927eafdb5a9e5ea3114e64696d9; zero-call proof in docs/sources/E023-retry-preflight.json |
| E024-chain-construction | Plan d25198e56a22a3b7212136587a16a2002f70e73f1a0ea00c2c5ae636ee774568; published b421660ce78b41aabf5a2faf0e049a304a37a40d; zero-call actual-material preflight |
| C001-construction-to-successor | Plan f54fd564b5e0e2e283a8110a133e97b565b2729fb61ecf50a575091612d733f1; published c4f0ac3c5041f6c7eb41927779752042752c1bd0; freezes E024 mini-r01, both distinct contracts and B settings/controls before A |
| E025-chain-successor | Reserved identity only; no plan, handoff, output or live call exists because actual published A output is required |

After explicit disclosure approval, inspect the output path first and execute E023 once:

```sh
python -m minireason.reason_use_study run --plan experiments/plans/E023-reason-no-return-retry.json --output experiments/records/E023-reason-no-return-retry --jobs 5
```

Record and review its exact returned-account omission, then publish and verify the complete or partial record. Do not run E020 again. E023 preserves every old source byte and adds only the four new modules to the repository-wide identity. Old source-bound plans remain immutable.

Review E023 before activating the prospective E024/C001 allocation. The selected pair retains prose-capable joint construction once, then successor discrimination once. It shelves same-template repetition, additional carrier sweeps and reservation-program templates for this target, preserving their specimens and reopening conditions. E024 uses exact prior source/question material and the declared new allocation. All B controls receive the same preselected A mini-r01 whole-output bundle. If that arm fails, no substitution is permitted.

The [workflow](workflows/template-chain.md) gives A execution, actual A publication verification, handoff freeze, B plan/preflight publication and B execution commands. No placeholder handoff or automatic third episode is allowed. Promotion is optional; suspension or no-promotion can be the reasoned outcome. Source preservation and route parity are separate from explanatory merit.

## Publication and recovery mechanics

Git CLI lacks a write credential; the independently authenticated GitHub connector publishes reviewed blobs/trees with non-force main updates. Local/remote commit metadata can differ; verify exact shared tree and actual main. Each completed document in this continuation received its own immediate checkpoint, with supporting activity/decision receipts. The activity stream is continuously appended, including publication checks, so the final verification events may postdate its last published snapshot. A receipt cannot contain its own future commit identity; the publisher verifies that enclosing checkpoint externally and the next ledger entry records it.

All original observations, partial drafts and earlier sources remain unchanged. There is no unresolved code/test failure at this checkpoint. The remaining external blocker is explicit DeepSeek destination/disclosure approval. No additional full-suite run or live call is needed before asking for that approval.
