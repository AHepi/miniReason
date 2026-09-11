# Current recovery and research state

**E021 was interrupted by automatic approval review. Exact public-payload evidence is verified; E022 is its separately identified normal-path retry. E020 remains pending. The next target is one cycle in each of two distinct linked templates, with optional problem promotion.**

Updated during the 2026-09-12 Australia recovery (provider timestamps use UTC). Start with [DECISION_LEDGER](DECISION_LEDGER.md), [PURPOSE](../PURPOSE.md) and [the recovery workflow](workflows/continue.md). Authorized destination: AHepi/miniReason main; source h-EPI remains unchanged. One publisher owns the ledger and main.

## What the failed window left

E013 had completed six arms and eighteen calls, but its upload stopped after batch 1 of 53. Recovery published its exact tree at remote `e0309aef15346428b8854e3669476f44732d1eda`, matching local `506b716bb7a2b4504e9e4f0ba54966587ac36465`, tree `ebcd5631eba03a218c9a117e5407c46f2b532a67`. Four untracked reviews were preserved unchanged. E013's partial review retains its old in-progress statement; the separately published recovery supplement completes all instrument/native readings.

README/AGENTS and the ledger recovery instructions are published. The integrated reason-use instrument and completed E013 review were verified at remote `5201b1385d7ff433fd031da361f34a41cf3f1443`; reviewed materials, plans and zero-call preflights at `7fc2b9928a06d7f6ac75159dfcf447536a9a43bc`. Full integrated offline suite: 542 tests passed. These are instrument results, not creativity verdicts. The activation/review checkpoint preceding the current record was remote `c84999f21c2566077ac4b2e2149c07c8ac8a19cc`, local `c45b54a0688266d5c81a82e7ef5ba2fbf728bac2`, shared tree `27e6c040bfb8facf35642b46b824d028400b618e`.

## Current controlled block

| Test | Intervention | Execution state |
|---|---|---|
| E016-reason-original | Exact E015 J and R; account returned at use | All six arms / ten calls complete; published at 31b2db6; independent integrity and substantive review complete (separate review) |
| E017-reason-recoded | Reviewed whole recoding of R | All six arms / ten calls complete; published at 8363c4c; independent review complete |
| E018-reason-different | Scoped capacity criticism | All six arms / ten calls complete; published at 9e59d57; independent review complete |
| E019-reason-omitted | Zero-byte supplemental criticism | Interrupted: 9 attempts, 7 complete responses, 2 transport failures; no root summary |
| E020-reason-no-return | Empty use-account field; four staged controls | Frozen, preflight passed, not run because E019 was interrupted |
| E021-reason-omitted-retry | Exact separately identified E019 retry | Frozen and preflighted offline; blocked pending restored authorized network access |

All plans and original inputs are fixed under `experiments/plans` and `experiments/materials/reason-use-v1`. Use sees only its finite domain data/questions and the account when enabled. Source/J/R are not separate use-stage ports. Prospective interpretation and decision receipts are outside model-visible inputs. E020 retains/counts its first response but does not expose it at use. One shared baseline is one observation. No scalar merit measure or automatic language installation exists.

E016 publication is verified at `31b2db694023d4268dbbb08dbc695344475552d8`. E017 publication is verified at `8363c4cab3c39aab1223a884df109c4a5382b88a`. E018 publication is verified at `9e59d57696c81a34173bf0501179182eecf5f2ca`. The next exact task is to restore authorized provider access, then run E021 in its new output directory, review/publish and verify it, then run unchanged E020 under [the reason-use workflow](workflows/reason-use.md). Do not reuse an existing output directory. Do not dispatch a successor after publication or provider-access failure. If interrupted, inspect actual request, response, result and summary files; preserve partial evidence.

Only after authorized network access is restored; do not attempt this under the cancelled approval:

```sh
python -m minireason.reason_use_study run --plan experiments/plans/E021-reason-omitted-retry.json --output experiments/records/E021-reason-omitted-retry --jobs 5
```

The authorized credential is supplied at runtime through DEEPSEEK_API_KEY and is never committed. Git CLI lacks a write credential; the independently authenticated GitHub connector publishes explicit blobs/trees with non-forced ref updates. Check actual remote main and exact tree identity before claiming publication. Local/connector commit metadata can differ. A ledger receipt cannot name its own future commit; later receipts name prior verified checkpoints.

## Earlier observations retained

| Records | State and interpretation |
|---|---|
| E001–E002 | Completed calibration comparisons; not creativity verdicts |
| E003–E004 | Frozen initial corpus and both language proposals |
| E005 | Direct observations and zero-call Mini preparation failures retained |
| E006–E007 | Superseded without execution |
| E008–E010 | Complete source-grounded prose/Lean/non-Lean comparisons and separate reviews, published |
| E011 | Interrupted first construction attempt; never retroactively completed |
| E014 | One-word access probe only |
| E015 | Separate prose retry; six arms/eighteen complete calls and review, published |
| E012–E013 | Frozen Lean/non-Lean construction blocks; each six arms/eighteen calls and completed review coverage, published |

The source packet and both original languages remain unchanged. Prose is fully legitimate. Review finds both located textual repairs and propagated errors, including endpoint attainment, presumed projection restrictions, attribution and capacity interpretation. INT-001–INT-006 and the separate reviews preserve exact arguments. No Mini advantage, universal creativity result, language ranking or search exhaustion is established. The current block investigates a particular criticism/use mechanism; other scoped interventions remain open in RESEARCH_AGENDA.

## Current blocker and complete handover

Read [the dated recovery/report](reviews/2026-09-12-recovery-and-reason-use.md). E019's matched-native use failed with tunnel 403; Mini-native response failed with IncompleteRead; execution polling then returned cancelled network approval with no reason. Preserve its original partial files and separate recovery.json/RECOVERY.md; neither is a normal completed summary. Failed-call token costs remain unknown. No retry or network workaround was attempted. A new window alone does not prove permission restored. E021 changes only run identity/provenance from E019 and has zero-call preflight proof in docs/sources/E021-retry-preflight.json.

The frozen block remains incomplete. There is no E020 no-return observation, no account-necessity conclusion, and no general creativity or Mini-advantage verdict. Three complete new configurations and the partial fourth provide 37 complete responses; all requested offline preparation and review that can proceed without the blocked provider path is preserved in this checkpoint.

Final evidence publication is verified at remote `3e2e96e5684c1f8b464801739507a5d88dc10f1c`, local `ab2ab5ecdf2e2168ba9e41681d750e6b623ffa2b`, shared tree `bde248a2f1075f82f0c82eb4adc6b2da8a95b085`. This includes every completed review and the blocked-state records above. The enclosing final receipt commit is checked separately by the publisher. No live retry was made.

## Renewed continuation and next target

The user has instructed continuation after the reported cancellation. D025 records the unchanged E021 activation through the normal provider path, conditional on successful access, then E020. D026 commissions template retention and distinct-template handoff reviews before implementation. No completed observation is overwritten; this new authorization does not claim that transport access already works. The next target is problem promotion, including a legitimate no-promotion outcome. The same template must not be run for two cycles.

E021 retained five requests, no complete response and a zero-byte partial response; it has no normal summary. Original hashes are in its recovery.json. GitHub metadata confirms this repository is public, and the immutable published E021 plan contains all prompt material. E022-reason-omitted-public-retry preserves the same material/settings and passes zero-call preflight. D027 records the evidence that addresses the stated approval concern; any renewed rejection stops live work. E022 is the next normal-path attempt, followed by E020 only after successful record publication.
