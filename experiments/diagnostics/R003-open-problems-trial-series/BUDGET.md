# R003 participant budget - draft envelopes, not spend predictions

An occurrence is a selected matrix; each problem/condition cell is one CLI run. Default eight problems and three conditions. A first O01-only occurrence has the per-problem envelope below. Full success is not assumed, and early stops reduce calls. Reader brief authorship/readings and any optional controls are outside participant totals, unallocated until separately declared. No dollar estimate is offered without a later rate check.

## Exact requested three-cycle arithmetic

| Condition per problem | Logical calls, no repair | Completion without repair | Attempts with allowed repairs | Maximum completion | Maximum input at32768/attempt |
|---|---:|---:|---:|---:|---:|
| NATIVE |1|32768|1|32768|32768|
| LOOP-CROSS + A2 repair |14|311296|28|622592|917504|
| LOOP-DECOMPOSED A2 + requested closing |14|376832|28|753664|917504|
| All three |29|720896|57|1409024|1867776|
| All eight problems |232|5767168|456|11272192|14942208|

CROSS: one initial +3*(two critics +return +use) +one closing =14. Five native calls at32768, nine off at16384:311296. One additional attempt for each schema failure can double that sum. It cannot retry transport or repair CEILING_HIT. The original R002 CROSS was14 strict attempts; this R003 repair extension is not installed.

For a complete s-step decomposition, 1<=s<=3: initial +(s-1) STEP +s critic +s return +s use +synthesis =4s+1. A2 without requested closure has13 logical/26 attempts at s=3:8*32768+5*16384=344064 without repair,688128 with repair. R003 adds one native closing response:4s+2 logical calls; at s=3,9*32768+5*16384=376832, doubled753664. Of the nine32768 slots, six are native and three are off critics. A longer-than-three-step plan lacks synthesis:12 A2 logical calls, plus at most one proposed closing =13; hard ceiling remains below the full14-slot case. Closing after terminal schema, ceiling or transport failure is forbidden. A partial final explanation does not complete the plan.

Per problem maximum combined input+completion:3276800. Eight-problem combined maximum:26214400. No-repair input allowance is29*32768=950272 per problem,7602176 for eight; no-repair combined13369344 for eight. A300-second outer supervised wall per attempt gives17100 aggregate seconds (4h45m) per problem,136800 (38h) for eight at the repair maximum, excluding setup/reading/publication. These are sums of bounded attempt allowances, not elapsed forecasts. Unknown spend after interrupted delivery stays unknown.

The unchanged A2 version, if selected by a separate design decision without R003 closure, would reduce the three-condition per-problem maximum to55 attempts and1343488 completion. It does not satisfy the current requested closing-return condition and is not silently substituted.

## Measured basis and uncertain working projection

[R001 REPORT](../R001-reason-cli-vs-baselines/REPORT.md), Operational record, reports131 logical calls/144 attempts;334459 prompt +818930 completion=1153389 known tokens. [R002 BUDGET_EVIDENCE](../R002-episodes-under-calibrated-difficulty/BUDGET_EVIDENCE.md) separates eight native calls (3295 prompt/78749 completion), and eight CROSS loops with18 cycles,80 primary calls (218810 prompt/350948 completion) plus13 repairs (66275 prompt/4471 completion). Nine primary GLM critics were ceiling-censored; these means do not predict healthy critics. Aliased baseline copies are not extra calls. No closing return occurred in those R001 runs.

R002 [calibration ADMISSION](../R002-episodes-under-calibrated-difficulty/calibration/ADMISSION.md) measured24 attempts,24995 prompt/363057 completion=388052 total, including344049 reasoning tokens within completion. Four exhausted the completion allowance. Mean native per call:1041.458 prompt and15127.375 completion, compared with R001411.875 and9843.625. Those are observed resource averages, not accuracy/quality scores or open-problem forecasts.

For transparency, transfer R001 public role means to a full CROSS schedule with a closing return: initial1, return4, critic6, use3. This yields about62655 completion and39210 prompt per problem (rounded upward). A deliberately weak decomposition planning proxy uses initial1, return-like5 (three returns, synthesis, closing), critic3, and use-like5 (two STEP, three use); it yields about60028 completion and40159 prompt. STEP/synthesis do not have measured equivalent means in these sources, so that second figure is a scenario, not an R002 measured decomposition forecast. Add the R002 native mean: about137811 completion and80409 prompt per problem, about1.103M completion and0.644M prompt for eight, before uncertain repair costs.

A provisional planning allowance is0.14-0.35M completion and0.08-0.20M prompt per selected problem, or1.12-2.80M completion and0.64-1.60M prompt for eight, below the independent hard maxima. Open questions, rich prose, schema-repair input growth and new closing calls may exceed this extrapolation. Record actual per-attempt usage and revisit the allocation after each occurrence; an estimate overrun does not authorize extra attempts. The measured R001 current mean28.544s/attempt would give about1.84 aggregate hours for232 base calls or3.62 hours for456 attempts; R002 calibration mean57.703s shows how weak that time extrapolation is. No total-series bound is implied by the two-no-new-kind stopping rule.

All maxima require the future qualified exact-wire input preflight. A32768 input limit is enforced before credential loading/send, not estimated from word counts; repair output may itself make a request too large. Input refusal does not cause truncation or a fallback. Schema field counts and public character caps do not guarantee a native reasoning budget will suffice.

No matched multi-call arm is enabled. A loop-versus-NATIVE difference therefore remains confounded by calls, tokens, seat lineages and modes. Before claiming a criticism-specific advantage, a separate occurrence must declare a neutral matched-call control, its same-information route, exact repair/ceiling allowances and extra budget. No optional RECODED or control calls are hidden in the totals above.

## Independent recomputation, 2026-09-17

R001 selected + R002 calibration: 155 logical calls, 168 attempts; 359454 prompt +1181987 completion =1541441 known tokens. R001 archived predecessors separately contain six unknown-usage attempts; they are not zero spend or an extra independent matched baseline. Source totals: R001 REPORT L70-L76 and R002 calibration/ADMISSION L38. Exact role-mean transfer (before rounding):80408.931 prompt and137810.069 completion per problem; for eight, ceiling643272 prompt and1102481 completion. These extrapolations are not measured R003 usage. Full recomputation and source locators: work/review25/budget/FACTS.md and calculations.json.

Planned occurrence 2 EC01 adds one ARCHIVED return/use pair per selected problem, sharing the original initial/critic calls: +2 logical calls, +4 maximum attempts, +49152 base completion, +98304 maximum completion and +131072 maximum input. Per problem totals become31 logical/61attempts/1507328completion/1998848input. For eight:248logical/488attempts/12058624completion/15990784input=28049408combined maximum. No additional critic generation or hidden control calls. Branch pair envelopes match locally; full main versus short archived branch is not a matched final-answer comparison. This prospective budget does not authorize dispatch or imply implemented engine support.
