# Current recovery and research state

**Recovery and offline implementation are complete. All completed documents, code and prepared plans have been pushed to AHepi/miniReason main. The next live action is E023, blocked pending explicit DeepSeek destination/disclosure approval.**

Updated 2026-09-12 UTC. Read [DECISION_LEDGER](DECISION_LEDGER.md), [AGENT_ACTIVITY](AGENT_ACTIVITY.jsonl), [PURPOSE](../PURPOSE.md) and [the runnable continuation](workflows/template-chain.md). Every agent logs each repository/staging search, read, edit and test through tools/repo_activity.py. One publisher commits and verifies every completed document immediately. Source h-EPI remains unchanged.

## What recovery completed

E022 had ten complete responses and local commit b4c0ae2, but its upload stopped at batch 6 of 14. Recovery completed the exact tree and verified remote 814649dba32264dddd7ccd466dbbd57e32c63bcb, shared tree ae6eb00407373a78b30337617c06cc7f71abbb6e. The recovered partial review remains unchanged; the separate [completion review](reviews/E022-completion-review.md) is published at 22924850b4094d34dbc92ee07799ac56954846de.

The new successor data/driver/Mini adapter and template coordinator are integrated and published at d1b175e12c6b9f96ecf792d42752dd5f506574b8. All original source files remain unchanged. The [independent implementation review](reviews/distinct-template-implementation-review.md) is published at ea1ce9a322c722d05b15609418ee781be1b0f55b. Normal and optimized full suites each pass 569 tests; the independent focused suite passes 27. Tests use scripted provider responses with the actual Mini engine. There is no live A-to-B observation or problem-promotion result.

The user's latest requested activity checkpoint is verified at remote a2c7c8c7adb5ad70a47b88bbbc67c973eb58d5cd, local 5de75f089d903be3fab5d23f28240130e13c2b9a, shared tree f165e76aa30b698b7e71d0c364b6a43dadfa12ec. This enclosing handover is published separately. Connector commit metadata differ from local history; verify exact tree correspondence and fresh remote main rather than rewriting either history.

## Observations and limits

| Record | Actual state |
|---|---|
| E016/E017/E018 | Each six arms and ten complete calls; data and separate reviews published. |
| E019 | Preserved partial: nine attempts, seven complete responses, two transport failures; no normal summary. |
| E021 | Preserved partial after approval rejection: five requests, no complete response, one incomplete file. |
| E022 | Complete and reviewed: six arms, ten responses, 102,272 prompt + 61,500 completion tokens; all four use answers numerically correct. |
| E020 | Interrupted after renewed automatic approval rejection: four first-stage requests, zero complete public answers, one tunnel-403 receipt; no use call or normal summary. |

E020's 74 original files are hashed in its [recovery record](../experiments/records/E020-reason-no-return/recovery.json) and published with [RECOVERY.md](../experiments/records/E020-reason-no-return/RECOVERY.md) at e589dacffe6aa36a68955d52a01a000d76a8d48b. Missing costs are unknown. Do not rerun E020 or overwrite E019/E021. The approval rejection and tunnel error are distinct events with unknown causal relation.

E022's accounts still contain classification, capacity, attribution and modality defects; correct use does not validate the whole account. The omitted supplemental occurrence was absent, but common-source criticisms remained. No account-necessity, general Mini-advantage, language ranking or creativity verdict follows. All earlier observations and proposals remain unchanged.

## Prepared next steps

| Prepared artifact | Identity and state |
|---|---|
| E023-reason-no-return-retry | Plan 8d21ad958acb05e7b9f0cd5eeeb86a69db32f49601533a227797d2a21de331cd; published at fcf7c3315b1f1927eafdb5a9e5ea3114e64696d9; zero-call preflight passes. Same E020 model-visible prompts/settings/controls; source adds only four new modules. |
| E024-chain-construction | Plan d25198e56a22a3b7212136587a16a2002f70e73f1a0ea00c2c5ae636ee774568; published at b421660ce78b41aabf5a2faf0e049a304a37a40d; zero-call preflight passes. Exact original source/issue/parents, prose carrier, six controls and one cycle. |
| C001-construction-to-successor | Plan f54fd564b5e0e2e283a8110a133e97b565b2729fb61ecf50a575091612d733f1; published at c4f0ac3c5041f6c7eb41927779752042752c1bd0. Predeclares A mini-r01 and whole-output mapping into distinct B. |
| E025-chain-successor | Contract/settings/controls are fixed by C001. No B plan or handoff exists: both must be frozen from actual published A output. |

No E023, E024 or E025 run directory exists. Do not create fake completion or handoff records from the offline fixtures. The retained mechanisms and shelved alternatives, commands, publication boundaries and analysis obligations are in [template-chain.md](workflows/template-chain.md).

## Exact live blocker and continuation

Automatic approval review rejected E020 because it judged the external DeepSeek destination and project-data disclosure not explicitly authorized. No retry or workaround followed. Obtain explicit approval to send the published experiment material and generated outputs to https://api.deepseek.com/v1/chat/completions. Use the existing authorized credential only at runtime through DEEPSEEK_API_KEY; never store it in committed files.

After that approval, verify the prepared plan/source and absence of its output directory, then execute:

```sh
python -m minireason.reason_use_study run --plan experiments/plans/E023-reason-no-return-retry.json --output experiments/records/E023-reason-no-return-retry --jobs 5
```

Review and publish E023 before activating E024. If the control defeats the prospective allocation, supersede the plan with a separately identified decision. Otherwise run A once, publish/verify A, freeze/publish its exact handoff and B plan, then run distinct B once and analyze its actual output. A failure of the preselected A mini-r01 arm leaves the chain unavailable; do not substitute another arm. B may propose further investigation, suspend or conclude no promotion is warranted. No third episode is automatic. The inquiry is externally blocked, not exhausted.
