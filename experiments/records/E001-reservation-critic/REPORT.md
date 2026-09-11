# E001-reservation-critic

Initial comparison of an original conjecture, grounded criticism and revision template against bare, native and matched multi-call controls. This is a construction and repair calibration; a ceiling result motivates a harder changed-assumption task, not repeated easy successes.

These are finite task observations. Explanation quality, reason use and creativity require separate review.

| Arm | Repeat | Outcome | Calls | Prompt tokens | Completion tokens |
|---|---:|---|---:|---:|---:|
| bare | 1 | OPERATIONAL_FAILURE | 1 | 1398 | 2515 |
| matched | 1 | CANDIDATE_EXECUTION_FAILURE | 3 | 9984 | 5153 |
| matched_native | 1 | OPERATIONAL_FAILURE | 1 | 1455 | 8192 |
| mini | 1 | OPERATIONAL_FAILURE | 3 | 8641 | 4577 |
| mini_native | 1 | OPERATIONAL_FAILURE | 1 | 1490 | 8192 |
| native | 1 | OPERATIONAL_FAILURE | 1 | 1423 | 8192 |

Inspect each arm's result.json, errata.json, calls, and Mini log where applicable. Complete requests and public answer text are retained. Native hidden reasoning text is omitted.
