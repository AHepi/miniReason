# Current recovery and research state

Updated during the 2026-09-12 Australia recovery (provider timestamps use UTC). Start with [DECISION_LEDGER](DECISION_LEDGER.md), [PURPOSE](../PURPOSE.md) and [the recovery workflow](workflows/continue.md). Authorized destination: AHepi/miniReason main; source h-EPI remains unchanged. One publisher owns the ledger and main.

## What the failed window left

E013 had completed six arms and eighteen calls, but its upload stopped after batch 1 of 53. Recovery published its exact tree at remote `e0309aef15346428b8854e3669476f44732d1eda`, matching local `506b716bb7a2b4504e9e4f0ba54966587ac36465`, tree `ebcd5631eba03a218c9a117e5407c46f2b532a67`. Four untracked reviews were preserved unchanged. E013's partial review retains its old in-progress statement; the separately published recovery supplement completes all instrument/native readings.

README/AGENTS and the ledger recovery instructions are published. The integrated reason-use instrument and completed E013 review were verified at remote `5201b1385d7ff433fd031da361f34a41cf3f1443`; reviewed materials, plans and zero-call preflights at `7fc2b9928a06d7f6ac75159dfcf447536a9a43bc`. Full integrated offline suite: 542 tests passed. These are instrument results, not creativity verdicts. The activation/review checkpoint preceding the current record was remote `c84999f21c2566077ac4b2e2149c07c8ac8a19cc`, local `c45b54a0688266d5c81a82e7ef5ba2fbf728bac2`, shared tree `27e6c040bfb8facf35642b46b824d028400b618e`.

## Current controlled block

| Test | Intervention | Execution state |
|---|---|---|
| E016-reason-original | Exact E015 J and R; account returned at use | All six arms / ten calls complete; published at 31b2db6; independent integrity and substantive review complete (separate review) |
| E017-reason-recoded | Reviewed whole recoding of R | All six arms / ten calls complete; published at 8363c4c; independent review complete |
| E018-reason-different | Scoped capacity criticism | All six arms / ten calls complete; published at 9e59d57; independent review finishing |
| E019-reason-omitted | Zero-byte supplemental criticism | Activation selected after verified E018; inspect actual records for live state |
| E020-reason-no-return | Empty use-account field; four staged controls | Frozen, preflight passed, not yet run |

All plans and original inputs are fixed under `experiments/plans` and `experiments/materials/reason-use-v1`. Use sees only its finite domain data/questions and the account when enabled. Source/J/R are not separate use-stage ports. Prospective interpretation and decision receipts are outside model-visible inputs. E020 retains/counts its first response but does not expose it at use. One shared baseline is one observation. No scalar merit measure or automatic language installation exists.

E016 publication is verified at `31b2db694023d4268dbbb08dbc695344475552d8`. E017 publication is verified at `8363c4cab3c39aab1223a884df109c4a5382b88a`. E018 publication is verified at `9e59d57696c81a34173bf0501179182eecf5f2ca`. The current exact task is to complete unchanged E019, then E020, reviewing/publishing each outcome under [the reason-use workflow](workflows/reason-use.md). Do not reuse an existing output directory. Do not dispatch a successor after publication or provider-access failure. If interrupted, inspect actual request, response, result and summary files; preserve partial evidence.

```sh
python -m minireason.reason_use_study run --plan experiments/plans/E019-reason-omitted.json --output experiments/records/E019-reason-omitted --jobs 5
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
