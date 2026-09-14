# C001 occurrence-02 — usage and envelope profile

Source: the twenty receipt records under
`experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/`
(`<endpoint_slug>/<arm>/<case>/rep<n>.json`). Computed by
`check/occ02_usage.py`, run as `python3 check/occ02_usage.py`; every figure below
was computed by that script from those records.

These are resource observations only. A reasoning share is a fact about how a
completion budget was spent, not a merit figure. The 8,192 comparison is against
the completion-token ceiling the same endpoint ran under in occurrence-01, not
against another family. Ranges are reported rather than medians or means: a
median convention is a choice and the range is not.

## Receipts, statuses, finish reasons

- Receipts: 20 (expected grid: 1 endpoint × 1 arm × 4 cases × 5 replicates = 20).
- `status`: COMPLETE × 20
- `finish_reason`: stop × 20

## Completion tokens (`usage.completion_tokens`)

- Total over 20 calls: 207,238.
- Range: 5,783 (deepseek-flash/fcl/original/rep5) to 15,470 (deepseek-flash/fcl/recoding/rep5).

## Reasoning tokens (`usage.completion_tokens_details.reasoning_tokens`)

- Total over 20 calls: 159,324.
- Range: 3,733 (deepseek-flash/fcl/original/rep5) to 12,470 (deepseek-flash/fcl/recoding/rep5).

## Per-call reasoning share of the completion

`reasoning_tokens / completion_tokens`, reported as a range over the twenty
calls, not an average:

- 0.6455 (deepseek-flash/fcl/original/rep5) to 0.8469 (deepseek-flash/fcl/recoding/rep1).

## Calls exceeding 8,192 completion tokens

- 15 of 20. 8,192 is the completion-token ceiling the same endpoint ran under in occurrence-01; the comparison is to that ceiling and to nothing else.
  - deepseek-flash/fcl/recoding/rep5: 15,470
  - deepseek-flash/fcl/recoding/rep1: 14,596
  - deepseek-flash/fcl/original/rep1: 14,579
  - deepseek-flash/fcl/original/rep4: 14,531
  - deepseek-flash/fcl/original/rep3: 14,360
  - deepseek-flash/fcl/carrier/rep1: 12,510
  - deepseek-flash/fcl/carrier/rep4: 12,089
  - deepseek-flash/fcl/carrier/rep3: 11,655
  - deepseek-flash/fcl/control/rep3: 9,918
  - deepseek-flash/fcl/recoding/rep4: 9,553
  - deepseek-flash/fcl/recoding/rep2: 9,425
  - deepseek-flash/fcl/recoding/rep3: 8,800
  - deepseek-flash/fcl/control/rep4: 8,754
  - deepseek-flash/fcl/original/rep2: 8,665
  - deepseek-flash/fcl/control/rep5: 8,263

## Prompt tokens (`usage.prompt_tokens`)

- Total over 20 calls: 102,445.

## Envelope

- `envelope_status`: AUTHORED × 20
- Non-empty `envelope_repairs`: 1 of 20.
  - deepseek-flash/fcl/control/rep2: ["json_strict_false"]
- `strict_parse_would_succeed`: true × 19; false (deepseek-flash/fcl/control/rep2).
- `timeout_seconds`: 600 × 20

## Failure codes

- None present. In every record `failure_class`, `failure_type`, `validation_failure_class`, `validation_failure_type` and `unresolved_reason` are null.

## Sensitivity to a single missing record

Which figures would change if one of the twenty records were missing:

Would change:
- Receipt count (20 → 19), for any removal.
- `status` and `finish_reason` counts, for any removal: the missing record's value-count drops by one. (The set of distinct values would survive any single removal here, since every observed value appears more than once.)
- Total completion tokens, total reasoning tokens and total prompt tokens, for any removal: every value is positive, so each total drops by the missing record's value.
- The over-8,192 completion-token count changes if and only if the missing record is one of the 15 calls listed above; a removal at or below the ceiling leaves it unchanged.
- The `strict_parse_would_succeed`-true count changes if and only if the missing record is one of the 19 true cases.
- The envelope-repair count changes if and only if the missing record is the repair carrier (deepseek-flash/fcl/control/rep2).

Would change only for a specific removal (computed from the current extremum
holders):
- Completion-token range: removing the sole minimum holder (5,783) moves its lower end; removing the sole maximum holder (15,470) moves its upper end.
- Reasoning-token range: removing the sole minimum holder (3,733) moves its lower end; removing the sole maximum holder (12,470) moves its upper end.
- Reasoning-share range: removing the sole minimum holder (0.6455) moves its lower end; removing the sole maximum holder (0.8469) moves its upper end.

Would not change:
- The comparison ceiling itself (8,192), which is occurrence-01's value,
  not a quantity computed from these records.
- The set of distinct `status` values (every value appears more than once).
- The set of distinct `finish_reason` values (every value appears more than once).
- The 8,192-exceedance status of any record that is not removed.
