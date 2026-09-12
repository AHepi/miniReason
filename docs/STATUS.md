# Current research status

Updated 2026-09-12. The overarching goal is to explore Mini's configuration space and test ECS 2.0 to identify gaps that can be filled. Language expression, formal feedback and this distinct-template chain are subset tests. See [PURPOSE](../PURPOSE.md) and the append-only [ledger](DECISION_LEDGER.md).

## Current checkpoint and next action

E024 and its review are complete and published. C001's actual handoff and E025's plan/preflight are complete and published. E025 was attempted once, then interrupted by renewed automatic disclosure review: five request records, one zero-byte response file, zero complete public responses, no terminal summary, and unknown usage. Its [recovery evidence](../experiments/records/E025-chain-successor/RECOVERY.md) is published at 96dbd892c3f4b2c18e87f03a6e0a544e471d075b. All 31 original file hashes pass preservation verification.

The exact next live task is [E025-retry-02](../experiments/attempts/E025-retry-02.json), pending explicit approval of the declared experiment-payload disclosure to DeepSeek. Retry 01 was attempted after fresh independent preflight and the user's credential provision, but automatic review rejected process polling: it said supplying a credential does not explicitly authorize disclosure of this payload to this destination. No surviving exact runner was found. [Retry 01 recovery](../experiments/records/E025-chain-successor-retry-01/RECOVERY.md) preserves 32 original files, five requests, two empty response files, zero complete responses, absent summary and unknown usage. Both failed attempts remain immutable; no third episode has started.

The same frozen plan and handoff remain ready: independent actual-material preflight passed with all 78 source hashes unchanged and zero provider calls. Retry 02 names a separate absent output directory. Neither pending-attempt declaration is a completed experiment. Do not rerun E023/E024, replace the selected arm or overwrite either failed E025 attempt.

| Artifact | Verified state |
|---|---|
| [E023](../experiments/records/E023-reason-no-return-retry/REPORT.md) | Four arms, eight complete calls; [review](reviews/E023-no-return-review.md) published. Returned account unnecessary for the witnessed cued arithmetic; source/interpretation defects remain. Do not rerun. |
| [E024](../experiments/records/E024-chain-construction/REPORT.md) | Six arms, eighteen complete calls, 404,937 total tokens. Record remote 9c876cc21686bd0e309449a4ca7dcbd9b737539c; [review](reviews/E024-construction-review.md) remote 0d828bd7f7d4279ba6eef94682a6d0ba6f5c13fb. Do not rerun. |
| [C001 handoff](../experiments/materials/C001-handoff.json) | Actual whole selected A bundle; freeze/verification pass. Published at 90f0766dad2e9e578b50fc77b81957b2139df3cd. |
| [E025 plan](../experiments/plans/E025-chain-successor.json) | Plan fae51c195662a65dd70c7f096559c24c894e50567a41e30d8b955ab571e04727; published at c4dd5aa2dd7fc1dc8c0c1659aca9d14d94be709d. Six controls, ten calls, distinct locate/discriminate template, one cycle. |
| [E025 preflight](../experiments/preflights/E025-chain-successor) | Passed with actual source and handoff, zero provider calls; activation published at ecedc2e7489fd5f6d5d8f79a472df920e1ca35e1. |

R20260912-09 records earlier destination/material approval; REC-20260912-D records the current user's DeepSeek credential provision and the later automatic rejection. The current stopping boundary is that review's explicit payload-disclosure approval requirement. Its stated concern is transmission of repository-derived material to the external DeepSeek API. No alternative route or further attempt was used. The payload is the E024 source packet, selected public A outputs, frozen E025 instructions and intermediate B public outputs sent to https://api.deepseek.com/v1/chat/completions.

After explicit approval, fresh source/output checks and an activation receipt, the exact prepared command is:

```sh
python -m minireason.successor_study run --plan experiments/plans/E025-chain-successor.json --output experiments/records/E025-chain-successor-retry-02 --jobs 5
```

The runtime credential remains outside tracked files and enters only the child process environment. Retry 02 preserves the original ten-call allocation. No retry 02 has been dispatched.

The selected A proposed a contestable wording question. Its criticism and revision also carry source-attribution errors. B must be assessed for actual discrimination, added premises, preserved uncertainties and justified continuation/suspension/no-promotion; a queue entry is not a substantive result. This review is not supplied to the model.

## Research limits and preserved work

The [configuration-space and ECS-gap assessment](reviews/configuration-space-and-ecs-gaps-2026-09-12.md) is published at fb58b3fcca38e7f2d5126b518e4df5e4979300b7. It maps actual coverage versus untested engine controls. Independent challenge defeats the proposed P1 contradiction under a scoped-transition reading; only an optional wording clarification remains. Its 16-condition routing/deployment diagnostic is prospective, not a frozen experiment or evidence of criticism use, creativity or a filled semantic gap.

The [formal-feedback report](reviews/formal-feedback-research-2026-09-12.md), [protocol](FORMAL_FEEDBACK_PROTOCOL.md) and local diagnostic are complete. The prototype has eleven operator-authored fixtures, nineteen focused tests and chain-localization evidence. No live formal-feedback intervention exists; adapter/materials/frozen plan remain future work. These diagnostics do not establish semantic fidelity or creativity.

E019, E020 and E021 remain immutable interrupted records. E022 is complete and reviewed; original partial reviews remain unchanged. Existing source, frozen plans and observations are preserved. Normal/optimized integrated suites previously passed 569 tests; this continuation uses the specific actual-material preflight rather than repeating that suite.

The attached ECS 2.0 is byte-identical to [the stored source](sources/ECS-2.0.pdf), SHA256 67bcb9512dd0fe93f2768cc429e71a8c5579a6a52b098d62da82a2f45d62138b. Gaps in definitions, candidate semantic counterexamples and implementation limitations must be reported separately. New interpretations or proposed repairs are new claims, not silent changes to ECS.

## Recovery discipline

Use the installed minireason-progress-ledger skill, one publisher and atomic activity logging. During active work, independently check both five-minute deadlines, publish every completed document immediately, and preserve stable partial evidence during larger uploads. Earlier cadence misses remain ledgered; no inactive period is claimed as monitored work. Verify remote main and exact local/remote trees. The [template-chain workflow](workflows/template-chain.md) supplies commands, but its original prepared-state descriptions are historical; this status and the latest ledger receipts give the current state.
