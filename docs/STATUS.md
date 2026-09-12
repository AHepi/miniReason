# Current research status

Updated 2026-09-12. The overarching goal is to explore Mini's configuration space and test ECS 2.0 to identify gaps that can be filled. Language expression, formal feedback and this distinct-template chain are subset tests. See [PURPOSE](../PURPOSE.md) and the append-only [ledger](DECISION_LEDGER.md).

## Current checkpoint and next action

E024 and its review are complete and published. C001's actual handoff and E025's plan/preflight are complete and published. E025 was attempted once, then interrupted by renewed automatic disclosure review: five request records, one zero-byte response file, zero complete public responses, no terminal summary, and unknown usage. Its [recovery evidence](../experiments/records/E025-chain-successor/RECOVERY.md) is published at 96dbd892c3f4b2c18e87f03a6e0a544e471d075b. All 31 original file hashes pass preservation verification.

The current live task is [E025-retry-02](../experiments/attempts/E025-retry-02.json). The user explicitly answered **Yes** to the exact request to send the E024 source packet and selected outputs, E025 instructions and intermediate outputs to https://api.deepseek.com/v1/chat/completions for this prepared ten-call retry. REC-20260912-E records this fresh approval; the prior pending declaration remains historical and unchanged.

Fresh actual-material preflight passes with zero provider calls, frozen source/handoff identities unchanged, and retry-02 output absent at activation. Both interrupted records pass original-file preservation checks (31 and 32 files). Publish this activation, then dispatch once. Six arms and ten calls remain fixed; no third episode is allocated.

| Artifact | Verified state |
|---|---|
| [E023](../experiments/records/E023-reason-no-return-retry/REPORT.md) | Four arms, eight complete calls; [review](reviews/E023-no-return-review.md) published. Returned account unnecessary for the witnessed cued arithmetic; source/interpretation defects remain. Do not rerun. |
| [E024](../experiments/records/E024-chain-construction/REPORT.md) | Six arms, eighteen complete calls, 404,937 total tokens. Record remote 9c876cc21686bd0e309449a4ca7dcbd9b737539c; [review](reviews/E024-construction-review.md) remote 0d828bd7f7d4279ba6eef94682a6d0ba6f5c13fb. Do not rerun. |
| [C001 handoff](../experiments/materials/C001-handoff.json) | Actual whole selected A bundle; freeze/verification pass. Published at 90f0766dad2e9e578b50fc77b81957b2139df3cd. |
| [E025 plan](../experiments/plans/E025-chain-successor.json) | Plan fae51c195662a65dd70c7f096559c24c894e50567a41e30d8b955ab571e04727; published at c4dd5aa2dd7fc1dc8c0c1659aca9d14d94be709d. Six controls, ten calls, distinct locate/discriminate template, one cycle. |
| [E025 preflight](../experiments/preflights/E025-chain-successor) | Passed with actual source and handoff, zero provider calls; activation published at ecedc2e7489fd5f6d5d8f79a472df920e1ca35e1. |

The first attempt and retry 01 remain immutable operational interruptions, with zero complete public responses and unknown usage. [Retry 01 recovery](../experiments/records/E025-chain-successor-retry-01/RECOVERY.md) explains the automatic rejection after credential provision. The user has now supplied the explicit payload/destination approval requested by that review. This authorization persists for the exact frozen attempt; do not ask again merely because the credential or repo content is involved. Honor any genuinely new runtime rejection.

The approved command, after this activation publication, is:

```sh
python -m minireason.successor_study run --plan experiments/plans/E025-chain-successor.json --output experiments/records/E025-chain-successor-retry-02 --jobs 5
```

The runtime credential remains outside tracked files and enters only the child process environment. No native hidden reasoning or operator review is sent as model input. Preserve actual public outputs and usage, publish the full complete or interrupted record, then review its substance.

The selected A proposed a contestable wording question. Its criticism and revision also carry source-attribution errors. B must be assessed for actual discrimination, added premises, preserved uncertainties and justified continuation/suspension/no-promotion; a queue entry is not a substantive result. This review is not supplied to the model.

## Research limits and preserved work

The [configuration-space and ECS-gap assessment](reviews/configuration-space-and-ecs-gaps-2026-09-12.md) is published at fb58b3fcca38e7f2d5126b518e4df5e4979300b7. It maps actual coverage versus untested engine controls. Independent challenge defeats the proposed P1 contradiction under a scoped-transition reading; only an optional wording clarification remains. Its 16-condition routing/deployment diagnostic is prospective, not a frozen experiment or evidence of criticism use, creativity or a filled semantic gap.

The [formal-feedback report](reviews/formal-feedback-research-2026-09-12.md), [protocol](FORMAL_FEEDBACK_PROTOCOL.md) and local diagnostic are complete. The prototype has eleven operator-authored fixtures, nineteen focused tests and chain-localization evidence. No live formal-feedback intervention exists; adapter/materials/frozen plan remain future work. These diagnostics do not establish semantic fidelity or creativity.

E019, E020 and E021 remain immutable interrupted records. E022 is complete and reviewed; original partial reviews remain unchanged. Existing source, frozen plans and observations are preserved. Normal/optimized integrated suites previously passed 569 tests; this continuation uses the specific actual-material preflight rather than repeating that suite.

The attached ECS 2.0 is byte-identical to [the stored source](sources/ECS-2.0.pdf), SHA256 67bcb9512dd0fe93f2768cc429e71a8c5579a6a52b098d62da82a2f45d62138b. Gaps in definitions, candidate semantic counterexamples and implementation limitations must be reported separately. New interpretations or proposed repairs are new claims, not silent changes to ECS.

## Recovery discipline

Use the installed minireason-progress-ledger skill, one publisher and atomic activity logging. During active work, independently check both five-minute deadlines, publish every completed document immediately, and preserve stable partial evidence during larger uploads. Earlier cadence misses remain ledgered; no inactive period is claimed as monitored work. Verify remote main and exact local/remote trees. The [template-chain workflow](workflows/template-chain.md) supplies commands, but its original prepared-state descriptions are historical; this status and the latest ledger receipts give the current state.
