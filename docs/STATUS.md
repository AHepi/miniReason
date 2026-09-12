# Current recovery and research state

**E022 is complete and verified on main. The next live task is the original frozen E020 no-return control. Distinct-template implementation is being recovered in separate staging.**

Updated 2026-09-12 UTC. Read [DECISION_LEDGER](DECISION_LEDGER.md), [PURPOSE](../PURPOSE.md) and [recovery workflow](workflows/continue.md). Destination: `AHepi/miniReason`, branch `main`; source h-EPI is unchanged. One publisher owns main and the ledger. Publish and verify every completed document immediately, including reviews, before proceeding to another document. Supporting ledger/STATUS updates may accompany that document. Publish every completed or interrupted configuration before successor dispatch.

## Exact recovery checkpoint

The last window completed E022 and committed it locally but stopped during upload at batch 6 of 14. Recovery finished that upload: remote `814649dba32264dddd7ccd466dbbd57e32c63bcb`, local `b4c0ae2a8e87e57fdbf2b3b06651d4110de8ebdd`, shared tree `ae6eb00407373a78b30337617c06cc7f71abbb6e`. Exact tree equality and main reference were verified. This enclosing status/ledger checkpoint is published separately. Git CLI lacks a write credential; the independently authenticated GitHub connector uses non-force updates and verifies the same intended local tree. No history is rewritten.

The recovered `docs/reviews/E022-reason-use-review.md` is an unchanged partial draft. A separate completion review is being prepared; its existence is not yet a completed interpretation. Only `successor_data.py` and partial receipts survived in external promotion staging; no finished B adapter/driver/coordinator was found. Canonical source remains unchanged pending E020.

## Controlled block

| Test | State |
|---|---|
| E016 original reason | Six arms / ten complete calls; published; independent review complete |
| E017 recoded reason | Six arms / ten complete calls; published; independent review complete |
| E018 different reason | Six arms / ten complete calls; published; independent review complete |
| E019 omission | Preserved partial: nine attempts, seven complete responses, two transport failures; no root summary |
| E021 omission retry | Preserved partial after approval rejection: five requests, no complete response, one incomplete file; no root summary |
| E022 public-payload omission retry | Six arms / ten complete calls, no operational alarms; 102,272 prompt and 61,500 completion tokens; publication verified above |
| E020 no returned account | Frozen/preflighted; no calls yet; next authorized live task after this checkpoint |

E019 and E021 remain unchanged interrupted records; missing costs are unknown. Public-payload evidence addressed the prior sensitivity rejection before E022 succeeded through the normal provider path. No endpoint or credential rerouting occurred. A new access rejection stops further dispatch.

## Next exact task

Run once from this checkout, with the previously authorized key supplied at runtime through `DEEPSEEK_API_KEY`:

```sh
python -m minireason.reason_use_study run --plan experiments/plans/E020-reason-no-return.json --output experiments/records/E020-reason-no-return --jobs 5
```

First check that this output directory does not already exist. If it does, inspect/preserve it instead of rerunning. E020 has four staged arms/eight calls and retains/counts the first response while exposing an empty account at use. Review actual account exclusion, custody and public content, then publish the result immediately. Keep all source files frozen until this source-bound run completes. The integrated offline baseline is 542 tests passing; no code has changed since that freeze.

After E020 closes, integrate and verify the staged `successor_discrimination_v1` adapter and A-to-B coordinator under D028/D029/D033. The retained family is prose-capable `joint_construction_v1`; carrier sweeps, repetition of the arithmetic block and same-template repetition are shelved for this target. Use the [template disposition](reviews/template-disposition-for-promotion.md) and [handoff design](reviews/distinct-template-handoff-design.md). Final live materials remain to be selected after control review.

Freeze a chain before A: A `joint_construction_v1` once, selected arm `mini-r01`; B `successor_discrimination_v1` once, locate/discriminate, separate one-cycle manifests/logs. Publish A before freezing its whole-output handoff; publish the handoff and B plan before B. All B controls receive the same preselected A output bundle. No arm substitution, automatic third episode, or forced problem promotion.

## Interpretation and historical work

E001–E018 records, initial language proposals and all earlier reviews remain available unchanged. E011/E019/E021 are partial, not negative semantic results; E006/E007 were superseded without execution. Source custody and operational success do not establish bearing, creativity, language ranking or Mini advantage. Equal matched/Mini conditional provider requests have the limitations explained in [route identifiability](reviews/reason-use-route-identifiability.md). No E020 outcome or account-necessity conclusion exists yet. Prose remains fully legitimate, and the inquiry remains open.
