# E026 SQL construction workflow

E026 is the prepared construction episode for the [SQL construction/use/return protocol](../SQL_CONSTRUCTION_RETURN_PROTOCOL.md). Its [frozen plan](../../experiments/plans/E026-sql-construction/plan.json), exact six requests, source copy and zero-call preflight were published at `6e972954612c7c2828af73dca086ef2145e8088c`. There is no live E026 record. The current environment timed out on two credential-free DeepSeek reachability attempts; the credential was not tested and no completion request was sent.

The current plan ID is `f8c3ab9ecb3285ea3d1d167427e413be2a30a1583a05fd5a411210430390a197`. Adapter SHA-256 is `d6813f3848e7f0138af64b397825af9cff257ecda4a9b75ecc789066c2a65354`; source SHA-256 is `1ca90ff7a3a0b0db10b117b8476d791035aeb6c68d8d260bf1c4a6e494954cd0`. The plan hashes the actual adapter, imported provider and Mini implementation/data. Any relevant source or implementation change requires a separately identified freeze and reviewed publication.

| Arm | Thinking | Provider-facing prompt |
|---|---|---|
| direct-disabled | Disabled | Shared system instruction and exact participant source |
| direct-native | Enabled, low effort | Shared system instruction and exact participant source |
| prompt-control-disabled | Disabled | Exact transformed Mini prompt |
| prompt-control-native | Enabled, low effort | Exact transformed Mini prompt |
| mini-disabled | Disabled | One construction stage, one cycle, one call |
| mini-native | Enabled, low effort | One construction stage, one cycle, one call |

The order is fixed as shown. Each call has an 8192 completion-token ceiling; six calls have a 49,152 aggregate completion-token ceiling, with separate prompt usage. These are ceilings, not expected usage or a fixed monetary price. Calls are sequential, retries are zero, and the runner stops on the first operational failure while preserving completed arms and the unattempted arm list. This one-stage study examines construction outputs, prompt changes and routing custody. Single samples cannot isolate chance or model drift; it cannot establish a multistage orchestration advantage.

## Offline verification

From the installed repository root, use:

```sh
python -m minireason.sql_construction_study verify --repo . --root experiments/plans/E026-sql-construction
```

Verification performs no provider call and does not inspect credentials. The completed [root receipt](../../experiments/plans/E026-sql-construction/verification.json) records 24 passing focused tests across material and adapter suites. Tests include a six-arm fake-provider run, partial failure, arbitrary-prose custody, exact request equality, source/manifest/request tampering, and fourteen rehashed effective-metadata changes. The actual-source preflight uses one scripted engine call; its answer is explicitly an offline probe, not a SQL construction.

To reproduce material preparation in a fresh path rather than overwrite the canonical freeze:

```sh
python -m minireason.sql_construction_study prepare --repo . --root /absolute/fresh/E026-preflight --source experiments/materials/SQL001-join-construction/participant/construction.json
```

Compare the resulting plan ID with the pinned identity. A discrepancy is evidence to investigate, not a reason to alter frozen bytes until the hash matches.

## Next live action when the declared destination is reachable

Read STATUS and the latest ledger first. Verify remote publication and the unchanged plan, establish same-destination transport availability, and record the actual dispatch decision. The user has supplied the credential for continuing this project; use it through `DEEPSEEK_API_KEY` in the process environment without writing it into files, command receipts or repository content. Keep the session publisher active and preserve stable running progress under the five-minute cadence. No repeated disclosure question is needed merely because an earlier window ended; honor any new concrete runtime rejection if one occurs.

The exact future command, with the output directory absent, is:

```sh
python -m minireason.sql_construction_study run --repo . --root experiments/plans/E026-sql-construction --output experiments/records/E026-sql-construction --expected-plan-id f8c3ab9ecb3285ea3d1d167427e413be2a30a1583a05fd5a411210430390a197
```

The destination is `https://api.deepseek.com/v1/chat/completions`. Payload is only the published participant source and the frozen public instructions shown in the request files; no FW5 full text, operator SQL cases, expected results, prior E024/E025 outputs or hidden reasoning are added. This command is prepared, not executed in REC-20260912-G. Do not rerun if the record already exists. Preserve any interrupted result and make a separate evidence-based continuation decision.

Mini's mandatory `mini.verdict.v1` terminal kind is used solely as transport for the construction artifact. It assigns no semantic standing. The adapter validates the complete routed brief before removing the exact host JSON-return suffix. It requests ordinary public text, wraps it internally for Mini, and checks that the full original public text is preserved in both body and commitments. It never parses the model's prose into an admission condition. The existing provider retains wire requests, public responses, identities, settings and usage while discarding hidden native reasoning.

## After the construction episode

Publish all completed or interrupted original E026 evidence before successor work. The selected occurrence is fixed as mini-disabled; use its entire public output or preserve its insufficiency. Do not substitute another arm after failure. Preserve source, settings, returned provider identity and exact original prose.

The next study needs an explicit interpretation and state-initialization bridge from that actual candidate. No bridge, B plan or B live runner is implemented by E026. A sufficiently informative construction allows preparation of the distinct one-cycle use/criticism/return template. If the proposed account cannot carry the needed distinction, report that result rather than supply the oracle's incremental solution. A future bridge must keep construction, decoding and operator contributions attributable, audit actual allowlisted input routes, and compare operative return with archive-only under the declared information differences. E025 and a third episode are never started automatically.

## Preserved preparation failures

[startup-errata.json](../../experiments/plans/E026-sql-construction/startup-errata.json) preserves the earlier staged verification receipt and its three implementation failures: absent mandatory terminal kind, incorrect first-attempt index, and a transient Path in JSON output. The fixes use the terminal kind without semantic appraisal, zero-based attempt validation, and a normalized offline outcome path. These were offline failures with zero provider calls.

[preparation-errata.json](../../experiments/plans/E026-sql-construction/preparation-errata.json) is the agent's later verification receipt. Its literal `prior_startup_errata: verification.json` refers to the earlier staging filename now preserved as startup-errata.json, not the root's canonical verification.json. Its current adapter and plan identities match the canonical freeze. Both provenance receipts remain unchanged; this paragraph resolves their naming ambiguity.
