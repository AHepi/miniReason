# R002 budget evidence from R001

Draft planning calculation; no R002 usage observed. Current R001 REPORT.md:70-78 provides the operational totals, elapsed and outlier boundary. Recomputed from each unique current LOOP-CROSS and LOOP-SINGLE RUN.md, excluding BARE/NATIVE alias copies and all old1/old2 directories. Raw review arithmetic is work/review16/R001-USAGE.json.

|Source|Cycles|Usage begins at line|
|---|---:|---:|
|experiments/diagnostics/R001-reason-cli-vs-baselines/runs/LOOP-CROSS/P01/RUN.md|2|299|
|experiments/diagnostics/R001-reason-cli-vs-baselines/runs/LOOP-CROSS/P02/RUN.md|3|404|
|experiments/diagnostics/R001-reason-cli-vs-baselines/runs/LOOP-CROSS/P03/RUN.md|1|239|
|experiments/diagnostics/R001-reason-cli-vs-baselines/runs/LOOP-CROSS/P04/RUN.md|3|374|
|experiments/diagnostics/R001-reason-cli-vs-baselines/runs/LOOP-CROSS/P05/RUN.md|3|374|
|experiments/diagnostics/R001-reason-cli-vs-baselines/runs/LOOP-CROSS/P06/RUN.md|1|239|
|experiments/diagnostics/R001-reason-cli-vs-baselines/runs/LOOP-CROSS/P07/RUN.md|2|284|
|experiments/diagnostics/R001-reason-cli-vs-baselines/runs/LOOP-CROSS/P08/RUN.md|3|374|
|experiments/diagnostics/R001-reason-cli-vs-baselines/runs/LOOP-SINGLE/P01/RUN.md|1|152|
|experiments/diagnostics/R001-reason-cli-vs-baselines/runs/LOOP-SINGLE/P02/RUN.md|1|152|
|experiments/diagnostics/R001-reason-cli-vs-baselines/runs/LOOP-SINGLE/P03/RUN.md|1|152|
|experiments/diagnostics/R001-reason-cli-vs-baselines/runs/LOOP-SINGLE/P04/RUN.md|1|152|
|experiments/diagnostics/R001-reason-cli-vs-baselines/runs/LOOP-SINGLE/P05/RUN.md|1|152|
|experiments/diagnostics/R001-reason-cli-vs-baselines/runs/LOOP-SINGLE/P06/RUN.md|1|152|
|experiments/diagnostics/R001-reason-cli-vs-baselines/runs/LOOP-SINGLE/P07/RUN.md|1|152|
|experiments/diagnostics/R001-reason-cli-vs-baselines/runs/LOOP-SINGLE/P08/RUN.md|2|197|

```json
{
  "all_current": {
    "n": 144,
    "prompt": 334459,
    "completion": 818930,
    "unknown": 0
  },
  "native_eight": {
    "n": 8,
    "prompt": 3295,
    "completion": 78749,
    "unknown": 0
  },
  "cross_loops_actual": {
    "n": 93,
    "prompt": 285085,
    "completion": 355419,
    "unknown": 0
  },
  "cross_loops_primary": {
    "n": 80,
    "prompt": 218810,
    "completion": 350948,
    "unknown": 0
  },
  "cross_cycles": 18,
  "initial": {
    "n": 8,
    "prompt": 3303,
    "completion": 76606,
    "unknown": 0
  },
  "return": {
    "n": 18,
    "prompt": 51812,
    "completion": 132397,
    "unknown": 0
  },
  "critic": {
    "n": 36,
    "prompt": 103462,
    "completion": 132449,
    "unknown": 0
  },
  "use": {
    "n": 18,
    "prompt": 60233,
    "completion": 9496,
    "unknown": 0
  }
}
```

The 80 CROSS primary calls include eight initial, eighteen return, thirty-six critic and eighteen use calls. Repair attempts are separately counted; no fallbacks occur in selected current runs. Nine GLM primary critics are ceiling-censored and included in resource totals. R002 forecast does not claim those would complete at the larger allowance. PLAN section 6 applies each measured role mean to the changed schedule, explicitly adding a closing return that R001 did not dispatch.
