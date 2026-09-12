# Continue through two distinct templates

This workflow implements D028 and D042: one construction episode followed by one successor-discrimination episode, with an exact published handoff. Each Mini template has max_cycles=1. A retains construct, criticize, revise and promote. B performs locate and discriminate. A candidate question, a suspension and an explicit no-promotion answer are all legitimate input/output; none automatically starts a third episode or endorses a diagnosis.

Read [STATUS](../STATUS.md), [DECISION_LEDGER](../DECISION_LEDGER.md) and [AGENT_ACTIVITY](../AGENT_ACTIVITY.jsonl) first. Every agent records each repository search, read, edit and test through tools/repo_activity.py. Publish and verify each completed document immediately and each completed or partial run before any successor. The source h-EPI repository remains untouched.

## What is retained for this target

| Component | Allocation and reason |
|---|---|
| Prose-capable joint construction family | Retained as A: prior complete records contain both substantive distinctions and propagated errors, suitable for an actual downstream inquiry. |
| Whole occurrences, original sources and matched/native controls | Retained: they expose what each later response really received and preserve comparisons. |
| New successor discrimination family | Retained as B: it investigates the proposed issue and alternatives rather than repeating construction. |
| Reason-use diagnostic | Retained to finish the owed no-return control; further repetitions of this same arithmetic block are shelved unless a distinct mechanism question arises. |
| Full carrier sweeps and reservation-program templates | Shelved for this promotion target; preserved unchanged for the reopening conditions in the disposition review. |
| WHL and RSS | Retained as frozen specimens; neither is installed as the operative carrier in this first chain. Prose remains fully legitimate. |
| Repeating the same template for two cycles | Excluded by the user's scope. Changing names does not make templates distinct. |

The [disposition review](../reviews/template-disposition-for-promotion.md) supplies the original evidence and reopening conditions; [E022 completion review](../reviews/E022-completion-review.md) adds the completed omission evidence. E020 remains interrupted. The chosen implementation and prospective chain do not depend on inventing its missing result. Review the eventual E023 observation before activating A; if it defeats this allocation, record a new decision and superseding plan instead of editing frozen bytes.

## Current live boundary and the owed control

Automatic approval review rejected the E020 execution because it judged the DeepSeek destination and project-data disclosure not explicitly authorized. The captured run has no complete public answer or use call. Further live dispatch requires explicit approval to send the published experiment material and generated outputs to the declared DeepSeek endpoint. Public availability and an earlier successful run are not themselves a new review approval. No retry is authorized by this workflow alone.

E023 is a separately identified retry with the same model-visible respond/use messages, account omission, four controls and provider settings. Its source identity adds only the four new successor/coordinator modules; every original source byte remains equal. See its [zero-call proof](../sources/E023-retry-preflight.json). After the explicit disclosure approval, and only if the output directory is absent:

```sh
python -m minireason.reason_use_study run --plan experiments/plans/E023-reason-no-return-retry.json --output experiments/records/E023-reason-no-return-retry --jobs 5
```

Inspect exact omission and every captured response, preserve any interruption, write the substantive review, then publish and verify. E020 is never overwritten. A failure blocks further live dispatch; it is not a semantic verdict. E023's four staged controls plan eight calls and retain/count the unexposed first response.

## A and the predeclared chain

The frozen [E024 A plan](../../experiments/plans/E024-chain-construction.json) preserves E015's complete original packet, selected issue and P7/P9/question parent material. The new allocation/test metadata are declared. [C001](../../experiments/plans/C001-construction-to-successor.json) fixes both contracts, B settings and controls, all input mappings and A mini-r01 before any A output exists. No handoff or B plan exists yet.

After E023's publication/review and a ledgered activation confirming this allocation:

```sh
python -m minireason.inquiry_study run --plan experiments/plans/E024-chain-construction.json --output experiments/records/E024-chain-construction --jobs 5
```

A has six arms and eighteen planned calls: bare/native each construct once; matched and Mini variants execute four stages. Those A one-call arms do not independently answer B's later endpoint. Each staged A arm has one cycle. If mini-r01 does not complete all four stages, preserve/publish that failure and leave the chain unavailable; never substitute a more attractive successful arm.

Publish the whole A record, verify the remote main commit and tree, and record the observed remote/local correspondence. The publisher then creates a publication JSON receipt with remote_commit, local_commit, tree_sha and remote_verified=true, using actual verified values. That receipt is evidence of the publisher's checks; setting a boolean is not a remote verification procedure. The local commit's tree must equal the verified remote tree. Keep the chain's pre-A publication checkpoint in the ledger as well.

## Freeze the actual output-to-input handoff

Only after A publication is verified, use the receipt created above:

```sh
python -m minireason.template_chain freeze-handoff --chain-plan experiments/plans/C001-construction-to-successor.json --parent-record experiments/records/E024-chain-construction --repository . --publication docs/sources/E024-publication.json --output experiments/materials/C001-handoff.json
```

The coordinator checks the complete parent record, signed occurrences, actual public requests/responses, original source material, host source archive, actual preflight and ended Mini replay against the supplied published tree. Its portable tree proof verifies byte inclusion; it cannot independently authenticate external execution or establish that the plan was published before A. Those chronological and remote facts remain the publisher's responsibility. The whole source and all four A public outputs are rendered for B. Custody proofs and host code archives are excluded from model input.

```sh
python -m minireason.template_chain verify-handoff --handoff experiments/materials/C001-handoff.json
python -m minireason.successor_study plan --handoff experiments/materials/C001-handoff.json --output experiments/plans/E025-chain-successor.json
python -m minireason.successor_study preflight --plan experiments/plans/E025-chain-successor.json --output experiments/preflights/E025-chain-successor
```

Freeze/publish each completed handoff/plan/preflight artifact without waiting for B. Verify the final checkpoint before dispatch. These commands make no model call and must refuse existing output paths. Do not write a placeholder handoff or populate absent A output with a scripted test fixture.

## B and analysis

```sh
python -m minireason.successor_study run --plan experiments/plans/E025-chain-successor.json --output experiments/records/E025-chain-successor --jobs 5
```

B plans ten calls across six arms. Bare/native address the complete follow-up endpoint once. Matched/Mini variants locate then discriminate in two calls, with the exact locate text supplied to the second stage. Every arm receives the same preselected A bundle; no arm-dependent handoff selection occurs. The two Mini episodes have separate manifests, roots and logs, each with one cycle.

All plans use deepseek-flash at https://api.deepseek.com/v1, with paired thinking-disabled/enabled controls, the inherited 32,768 completion ceiling and recorded actual usage. The credential is read only at runtime from DEEPSEEK_API_KEY. Reaching a finite ceiling is not exhaustion of inquiry. Same conditional matched/Mini prompts establish parity, not a new reasoning input or a general Mini advantage.

After B, preserve/publish the complete or partial record and review the actual text. Examine whether its proposed issue faithfully identifies A's claim and uncertainty, whether the offered case distinguishes live readings, which premises or observations remain missing, and what the proposed successor, suspension or no-promotion would change. Do not count the word promote or a queue record as a successful promotion. A later episode needs a separate allocation; none starts automatically.

The [independent implementation review](../reviews/distinct-template-implementation-review.md) and [integrated verification](../sources/2026-09-12-template-chain-verification.json) document 27 focused fake-provider checks and 569 passing normal/optimized tests. They establish finite operational properties, with zero live A/B observations. The current next action remains explicit provider disclosure approval, followed by E023.
