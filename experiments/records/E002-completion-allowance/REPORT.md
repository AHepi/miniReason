# E002-completion-allowance

E001 native-mode arms terminated at exactly their 8192-token ceilings before complete answers. Raise only the per-call ceiling to 32768, retaining model, reasoning effort, task, original template, wiring and all six arms. This tests truncation as the cause of unusable native output. Non-native repeats also expose whether prior format failures recur; no template repair is credited to this resource change.

These are finite task observations. Explanation quality, reason use and creativity require separate review.

| Arm | Repeat | Outcome | Calls | Prompt tokens | Completion tokens |
|---|---:|---|---:|---:|---:|
| bare | 1 | CANDIDATE_EXECUTION_FAILURE | 1 | 1398 | 2084 |
| matched | 1 | OPERATIONAL_FAILURE | 3 | 7982 | 3430 |
| matched_native | 1 | CANDIDATE_EXECUTION_FAILURE | 3 | 8274 | 58264 |
| mini | 1 | CANDIDATE_EXECUTION_FAILURE | 3 | 7936 | 4247 |
| mini_native | 1 | OPERATIONAL_FAILURE | 1 | 1490 | 32768 |
| native | 1 | TASK_SURVIVED | 1 | 1423 | 18926 |

Inspect each arm's result.json, errata.json, calls, and Mini log where applicable. Complete requests and public answer text are retained. Native hidden reasoning text is omitted.
