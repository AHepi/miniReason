# kimi-k3 battery runs, reclassified

Every run recorded under `runs/` (pass 1), `runs-pass2/` and `runs-pass3/`, re-read from its `result.json`, its `transcript.jsonl` and its task's `expected_outputs`, and labelled under the statuses the harness uses now. **Nothing here was re-run and no record was altered**: this file is a second reading of the same bytes, written beside them by `reclassify.py`.

## Why the recorded labels are wrong

The harness used to end its loop on *any* assistant turn that carried no tool call, and call that `COMPLETE`. Two different non-completions were swept into that word:

1. A turn that came back **`finish_reason: length` with empty content and no tool call** — the entire per-turn `max_tokens` budget was spent on native reasoning, so the turn produced neither an action nor an answer. That is a resource boundary on the turn, and it is now `INCOMPLETE_TURN` / `TURN_BUDGET_EXHAUSTED_BY_REASONING`.
2. A turn that finished on its own (`stop`) but left the task's declared outputs unwritten. The model talked; it did not deliver. That is now `NO_DELIVERABLE`.

`COMPLETE` now survives only when the final turn finished **and** every declared expected output exists.

## Rules applied here

| recorded | evidence re-read | reclassified |
|---|---|---|
| `HARNESS_FAILURE` | — | unchanged (the record already names how it stopped) |
| `ITERATION_CAP` | — | unchanged |
| `COMPLETE` | last `response` event: non-`stop` finish, no `tool_calls`, blank `content` | `INCOMPLETE_TURN` (`TURN_BUDGET_EXHAUSTED_BY_REASONING`) |
| `COMPLETE` | any declared `expected_output` absent from the run's sandbox | `NO_DELIVERABLE` |
| `COMPLETE` | finished turn, every declared output present | `COMPLETE` |

Expected-output marks: `[+]` exists and this run wrote it, `[=]` exists but came in with the task's context copy, `[-]` missing. A declared directory (trailing `/`) counts as present only when it holds at least one file.

## Every recorded run

| pass | task | recorded | reclassified | iters | tool calls | prompt tok | completion tok | wall s | last finish | harness failure | expected outputs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pass1 | `a-01-types` | ITERATION_CAP | ITERATION_CAP | 40 | 52 | 1880898 | 21453 | 459.9 | tool_calls | ITERATION_CAP | `review/types.md` [-] `probe/` [+] |
| pass2 | `a-01-types` | COMPLETE | **INCOMPLETE_TURN** | 14 | 31 | 503365 | 15740 | 295.0 | length | TURN_BUDGET_EXHAUSTED_BY_REASONING | `review/types.md` [-] `probe/` [-] |
| pass1 | `a-02-contracts` | ITERATION_CAP | ITERATION_CAP | 40 | 58 | 3698138 | 52581 | 1053.6 | tool_calls | ITERATION_CAP | `review/contracts.md` [+] `probe/` [+] |
| pass2 | `a-02-contracts` | COMPLETE | COMPLETE | 56 | 68 | 5199979 | 29243 | 599.1 | stop | - | `review/contracts.md` [+] `probe/` [+] |
| pass1 | `a-03-standard` | ITERATION_CAP | ITERATION_CAP | 40 | 51 | 2979479 | 41362 | 889.5 | tool_calls | ITERATION_CAP | `review/standard.md` [-] `probe/` [+] |
| pass2 | `a-03-standard` | COMPLETE | **INCOMPLETE_TURN** | 6 | 8 | 165169 | 9133 | 168.9 | length | TURN_BUDGET_EXHAUSTED_BY_REASONING | `review/standard.md` [-] `probe/` [-] |
| pass1 | `a-04-custody` | COMPLETE | COMPLETE | 37 | 69 | 2464027 | 25768 | 539.5 | stop | - | `review/custody.md` [+] `probe/` [+] |
| pass1 | `a-05-receipts` | HARNESS_FAILURE | HARNESS_FAILURE | 8 | 12 | 203705 | 1230 | 338.1 | tool_calls | TRANSPORT_OR_RESPONSE_ERROR | `review/receipts.md` [-] `probe/` [-] |
| pass2 | `a-05-receipts` | COMPLETE | **INCOMPLETE_TURN** | 3 | 4 | 52791 | 8455 | 156.6 | length | TURN_BUDGET_EXHAUSTED_BY_REASONING | `review/receipts.md` [-] `probe/` [-] |
| pass1 | `a-06-publish` | HARNESS_FAILURE | HARNESS_FAILURE | 5 | 7 | 94134 | 489 | 322.2 | tool_calls | TRANSPORT_OR_RESPONSE_ERROR | `review/publish.md` [-] `probe/` [-] |
| pass2 | `a-06-publish` | HARNESS_FAILURE | HARNESS_FAILURE | 6 | 10 | 118304 | 1296 | 183.9 | tool_calls | HTTP_500 | `review/publish.md` [-] `probe/` [-] |
| pass3 | `a-06-publish` | COMPLETE | **INCOMPLETE_TURN** | 9 | 16 | 353378 | 9782 | 181.6 | length | TURN_BUDGET_EXHAUSTED_BY_REASONING | `review/publish.md` [-] `probe/` [-] |
| pass1 | `b-01-surface` | HARNESS_FAILURE | HARNESS_FAILURE | 11 | 17 | 565107 | 1605 | 356.7 | tool_calls | TRANSPORT_OR_RESPONSE_ERROR | `tests/loop/test_surface.py` [-] |
| pass2 | `b-01-surface` | COMPLETE | **INCOMPLETE_TURN** | 11 | 19 | 864375 | 19353 | 357.6 | length | TURN_BUDGET_EXHAUSTED_BY_REASONING | `tests/loop/test_surface.py` [-] |
| pass1 | `b-02-seats` | ITERATION_CAP | ITERATION_CAP | 40 | 52 | 2397932 | 27689 | 552.5 | tool_calls | ITERATION_CAP | `tests/loop/test_seats.py` [+] |
| pass2 | `b-02-seats` | COMPLETE | **INCOMPLETE_TURN** | 6 | 13 | 182577 | 11278 | 206.9 | length | TURN_BUDGET_EXHAUSTED_BY_REASONING | `tests/loop/test_seats.py` [-] |
| pass1 | `b-03-obligations` | HARNESS_FAILURE | HARNESS_FAILURE | 5 | 11 | 142947 | 2778 | 362.6 | tool_calls | TRANSPORT_OR_RESPONSE_ERROR | `tests/loop/test_obligations.py` [-] |
| pass2 | `b-03-obligations` | COMPLETE | **INCOMPLETE_TURN** | 8 | 22 | 464681 | 17152 | 313.6 | length | TURN_BUDGET_EXHAUSTED_BY_REASONING | `tests/loop/test_obligations.py` [-] |
| pass1 | `b-04-steps` | HARNESS_FAILURE | HARNESS_FAILURE | 6 | 14 | 228159 | 7165 | 448.9 | tool_calls | TRANSPORT_OR_RESPONSE_ERROR | `tests/loop/test_steps.py` [-] |
| pass2 | `b-04-steps` | HARNESS_FAILURE | HARNESS_FAILURE | 14 | 20 | 757167 | 9225 | 313.4 | tool_calls | HTTP_500 | `tests/loop/test_steps.py` [-] |
| pass3 | `b-04-steps` | COMPLETE | **INCOMPLETE_TURN** | 7 | 12 | 301192 | 9112 | 162.5 | length | TURN_BUDGET_EXHAUSTED_BY_REASONING | `tests/loop/test_steps.py` [-] |
| pass1 | `c-01-packs` | HARNESS_FAILURE | HARNESS_FAILURE | 14 | 26 | 915927 | 1735 | 359.5 | tool_calls | TRANSPORT_OR_RESPONSE_ERROR | `src/minireason/loop/packs.py` [-] `tests/loop/test_packs.py` [-] |
| pass2 | `c-01-packs` | HARNESS_FAILURE | HARNESS_FAILURE | 17 | 33 | 1241207 | 2727 | 206.5 | tool_calls | HTTP_500 | `src/minireason/loop/packs.py` [-] `tests/loop/test_packs.py` [-] |
| pass3 | `c-01-packs` | COMPLETE | **INCOMPLETE_TURN** | 11 | 26 | 1050595 | 17278 | 300.5 | length | TURN_BUDGET_EXHAUSTED_BY_REASONING | `src/minireason/loop/packs.py` [-] `tests/loop/test_packs.py` [-] |
| pass1 | `c-02-roles` | HARNESS_FAILURE | HARNESS_FAILURE | 16 | 28 | 942737 | 13880 | 560.7 | tool_calls | TRANSPORT_OR_RESPONSE_ERROR | `src/minireason/loop/roles.py` [+] `tests/loop/test_roles.py` [-] |
| pass2 | `c-02-roles` | COMPLETE | **INCOMPLETE_TURN** | 14 | 26 | 899618 | 10738 | 216.5 | length | TURN_BUDGET_EXHAUSTED_BY_REASONING | `src/minireason/loop/roles.py` [-] `tests/loop/test_roles.py` [-] |
| pass1 | `c-03-markprep` | HARNESS_FAILURE | HARNESS_FAILURE | 10 | 18 | 323759 | 2039 | 343.0 | tool_calls | TRANSPORT_OR_RESPONSE_ERROR | `src/minireason/loop/markprep.py` [-] `tests/loop/test_markprep.py` [-] |
| pass2 | `c-03-markprep` | COMPLETE | **INCOMPLETE_TURN** | 8 | 17 | 367440 | 9445 | 175.1 | length | TURN_BUDGET_EXHAUSTED_BY_REASONING | `src/minireason/loop/markprep.py` [-] `tests/loop/test_markprep.py` [-] |
| pass1 | `c-04-decide` | HARNESS_FAILURE | HARNESS_FAILURE | 11 | 19 | 541744 | 13812 | 558.5 | tool_calls | TRANSPORT_OR_RESPONSE_ERROR | `src/minireason/loop/decide.py` [-] `tests/loop/test_decide.py` [-] |
| pass2 | `c-04-decide` | COMPLETE | **INCOMPLETE_TURN** | 17 | 27 | 1298991 | 14171 | 282.3 | length | TURN_BUDGET_EXHAUSTED_BY_REASONING | `src/minireason/loop/decide.py` [+] `tests/loop/test_decide.py` [-] |
| pass1 | `d-01-receipt` | HARNESS_FAILURE | HARNESS_FAILURE | 4 | 8 | 28773 | 484 | 313.2 | tool_calls | TRANSPORT_OR_RESPONSE_ERROR | `out/receipt.md` [-] |
| pass2 | `d-01-receipt` | HARNESS_FAILURE | HARNESS_FAILURE | 5 | 8 | 43556 | 434 | 151.7 | tool_calls | HTTP_500 | `out/receipt.md` [-] |
| pass3 | `d-01-receipt` | COMPLETE | **INCOMPLETE_TURN** | 3 | 6 | 28773 | 8493 | 143.2 | length | TURN_BUDGET_EXHAUSTED_BY_REASONING | `out/receipt.md` [-] |
| pass1 | `d-02-operator-page` | COMPLETE | COMPLETE | 14 | 22 | 772986 | 39684 | 750.2 | stop | - | `out/steps-operator-section.md` [+] |
| pass1 | `d-03-decision-record` | COMPLETE | COMPLETE | 7 | 10 | 91063 | 10651 | 213.0 | stop | - | `out/decision-record.md` [+] |
| pass1 | `d-04-f002-outcome` | COMPLETE | COMPLETE | 8 | 15 | 135611 | 13920 | 312.2 | stop | - | `out/f002-closing.md` [+] |
| pass1 | `e-01-refute` | COMPLETE | COMPLETE | 24 | 48 | 764401 | 21124 | 481.0 | stop | - | `out/refutations.md` [+] `check/` [+] |
| pass1 | `e-02-metric-creep` | HARNESS_FAILURE | HARNESS_FAILURE | 3 | 12 | 44026 | 761 | 360.7 | tool_calls | TRANSPORT_OR_RESPONSE_ERROR | `out/metric-creep.md` [-] `probe/` [-] |
| pass2 | `e-02-metric-creep` | COMPLETE | **INCOMPLETE_TURN** | 3 | 7 | 84205 | 8742 | 165.1 | length | TURN_BUDGET_EXHAUSTED_BY_REASONING | `out/metric-creep.md` [-] `probe/` [-] |
| pass1 | `e-03-fw5-citations` | COMPLETE | COMPLETE | 20 | 26 | 927971 | 24679 | 542.0 | stop | - | `out/citations.md` [+] `check/` [+] |
| pass1 | `e-04-f001-classes` | COMPLETE | COMPLETE | 24 | 30 | 1262135 | 44523 | 766.0 | stop | - | `out/f001-classes.md` [+] `check/` [+] |
| pass1 | `f-01-c001-profile` | COMPLETE | COMPLETE | 25 | 36 | 832739 | 27118 | 529.8 | stop | - | `out/c001-profile.md` [+] `check/` [+] |
| pass1 | `f-02-commit-tree` | COMPLETE | COMPLETE | 29 | 35 | 1733457 | 56772 | 886.9 | stop | - | `out/commit-tree.md` [+] `check/` [+] |
| pass2 | `f-02-commit-tree` | COMPLETE | **INCOMPLETE_TURN** | 7 | 10 | 108081 | 8913 | 171.3 | length | TURN_BUDGET_EXHAUSTED_BY_REASONING | `out/commit-tree.md` [-] `check/` [-] |
| pass1 | `f-03-occ02-usage` | COMPLETE | COMPLETE | 16 | 22 | 247540 | 12896 | 248.1 | stop | - | `out/occ02-usage.md` [+] `check/` [+] |
| pass1 | `b-004` | HARNESS_FAILURE | HARNESS_FAILURE | 1 | 0 | 0 | 0 | 300.3 | - | TRANSPORT_OR_RESPONSE_ERROR | `probe/test_tasks_probe.py` [-] |
| pass2 | `b-004` | COMPLETE | **INCOMPLETE_TURN** | 2 | 2 | 11588 | 16384 | 281.0 | length | TURN_BUDGET_EXHAUSTED_BY_REASONING | `probe/test_tasks_probe.py` [-] |

Recorded: COMPLETE 27, HARNESS_FAILURE 16, ITERATION_CAP 4.

Reclassified: COMPLETE 11, HARNESS_FAILURE 16, INCOMPLETE_TURN 16, ITERATION_CAP 4.

16 of 47 rows change label: 16 to `INCOMPLETE_TURN`, 0 to `NO_DELIVERABLE`.

## Runs whose recorded COMPLETE does not survive

| pass | task | recorded | reclassified | why |
|---|---|---|---|---|
| pass2 | `a-01-types` | COMPLETE | INCOMPLETE_TURN | final turn finished as 'length' with no tool call and no content |
| pass2 | `a-03-standard` | COMPLETE | INCOMPLETE_TURN | final turn finished as 'length' with no tool call and no content |
| pass2 | `a-05-receipts` | COMPLETE | INCOMPLETE_TURN | final turn finished as 'length' with no tool call and no content |
| pass3 | `a-06-publish` | COMPLETE | INCOMPLETE_TURN | final turn finished as 'length' with no tool call and no content |
| pass2 | `b-01-surface` | COMPLETE | INCOMPLETE_TURN | final turn finished as 'length' with no tool call and no content |
| pass2 | `b-02-seats` | COMPLETE | INCOMPLETE_TURN | final turn finished as 'length' with no tool call and no content |
| pass2 | `b-03-obligations` | COMPLETE | INCOMPLETE_TURN | final turn finished as 'length' with no tool call and no content |
| pass3 | `b-04-steps` | COMPLETE | INCOMPLETE_TURN | final turn finished as 'length' with no tool call and no content |
| pass3 | `c-01-packs` | COMPLETE | INCOMPLETE_TURN | final turn finished as 'length' with no tool call and no content |
| pass2 | `c-02-roles` | COMPLETE | INCOMPLETE_TURN | final turn finished as 'length' with no tool call and no content |
| pass2 | `c-03-markprep` | COMPLETE | INCOMPLETE_TURN | final turn finished as 'length' with no tool call and no content |
| pass2 | `c-04-decide` | COMPLETE | INCOMPLETE_TURN | final turn finished as 'length' with no tool call and no content |
| pass3 | `d-01-receipt` | COMPLETE | INCOMPLETE_TURN | final turn finished as 'length' with no tool call and no content |
| pass2 | `e-02-metric-creep` | COMPLETE | INCOMPLETE_TURN | final turn finished as 'length' with no tool call and no content |
| pass2 | `f-02-commit-tree` | COMPLETE | INCOMPLETE_TURN | final turn finished as 'length' with no tool call and no content |
| pass2 | `b-004` | COMPLETE | INCOMPLETE_TURN | final turn finished as 'length' with no tool call and no content |

### The turns that ran out of budget

| pass | task | turn | finish | completion tokens | turn budget (`max_tokens`) | reasoning chars | reasoning tokens (est.) | reasoning sha256 |
|---|---|---|---|---|---|---|---|---|
| pass2 | `a-01-types` | 14 | length | 8192 | 8192 | 32760 | 8190 | `78a1afa3f0addc3c` |
| pass2 | `a-03-standard` | 6 | length | 8192 | 8192 | 33396 | 8349 | `e8e78cf546f5d465` |
| pass2 | `a-05-receipts` | 3 | length | 8192 | 8192 | 33500 | 8375 | `d16d60b23b8d972a` |
| pass3 | `a-06-publish` | 9 | length | 8192 | 8192 | 34316 | 8579 | `bd10f4f7dca7bd05` |
| pass2 | `b-01-surface` | 11 | length | 8192 | 8192 | 32953 | 8238 | `75744442fbeaf144` |
| pass2 | `b-02-seats` | 6 | length | 8192 | 8192 | 34444 | 8611 | `3270257f9a22d861` |
| pass2 | `b-03-obligations` | 8 | length | 8192 | 8192 | 33589 | 8397 | `2df1df6d22d0cedb` |
| pass3 | `b-04-steps` | 7 | length | 8192 | 8192 | 34441 | 8610 | `100ef8da9fec179f` |
| pass3 | `c-01-packs` | 11 | length | 8192 | 8192 | 35225 | 8806 | `5743696f47897067` |
| pass2 | `c-02-roles` | 14 | length | 8192 | 8192 | 36797 | 9199 | `3b5c5078669a3b57` |
| pass2 | `c-03-markprep` | 8 | length | 8192 | 8192 | 34203 | 8550 | `86197db6687b783d` |
| pass2 | `c-04-decide` | 17 | length | 8192 | 8192 | 34652 | 8663 | `4fe075865f31771b` |
| pass3 | `d-01-receipt` | 3 | length | 8192 | 8192 | 32229 | 8057 | `f5d4fed39ea24f4d` |
| pass2 | `e-02-metric-creep` | 3 | length | 8192 | 8192 | 35029 | 8757 | `ef27be1a9c334203` |
| pass2 | `f-02-commit-tree` | 7 | length | 8192 | 8192 | 27777 | 6944 | `0d9d6371682e1d1e` |
| pass2 | `b-004` | 2 | length | 8192 | 8192 | 30372 | 7593 | `eedd81fc48f24448` |

The reasoning **text** was never persisted by the harness and is not recoverable from these records; the digest, the character count and the derived token count are what the transcript kept.

Every one of these turns spent its **entire** per-turn budget: 8192 completion tokens against a `max_tokens` of 8192, with 27,777-36,797 characters of native reasoning behind them and nothing left for a tool call or an answer. The budget was lowered to that figure for these passes — pass 1 ran at 32768 — so this is a boundary the harness set, not one the provider imposed. The runs are cheap and fast *and* they deliver nothing; the recorded `COMPLETE` labels made that trade invisible.

## Per task: the latest pass that is genuinely COMPLETE

- `a-01-types` — latest genuinely COMPLETE pass: **none** (pass1 ITERATION_CAP, pass2 COMPLETE -> INCOMPLETE_TURN)
- `a-02-contracts` — latest genuinely COMPLETE pass: **pass2** (pass1 ITERATION_CAP, pass2 COMPLETE)
- `a-03-standard` — latest genuinely COMPLETE pass: **none** (pass1 ITERATION_CAP, pass2 COMPLETE -> INCOMPLETE_TURN)
- `a-04-custody` — latest genuinely COMPLETE pass: **pass1** (pass1 COMPLETE)
- `a-05-receipts` — latest genuinely COMPLETE pass: **none** (pass1 HARNESS_FAILURE, pass2 COMPLETE -> INCOMPLETE_TURN)
- `a-06-publish` — latest genuinely COMPLETE pass: **none** (pass1 HARNESS_FAILURE, pass2 HARNESS_FAILURE, pass3 COMPLETE -> INCOMPLETE_TURN)
- `b-01-surface` — latest genuinely COMPLETE pass: **none** (pass1 HARNESS_FAILURE, pass2 COMPLETE -> INCOMPLETE_TURN)
- `b-02-seats` — latest genuinely COMPLETE pass: **none** (pass1 ITERATION_CAP, pass2 COMPLETE -> INCOMPLETE_TURN)
- `b-03-obligations` — latest genuinely COMPLETE pass: **none** (pass1 HARNESS_FAILURE, pass2 COMPLETE -> INCOMPLETE_TURN)
- `b-04-steps` — latest genuinely COMPLETE pass: **none** (pass1 HARNESS_FAILURE, pass2 HARNESS_FAILURE, pass3 COMPLETE -> INCOMPLETE_TURN)
- `c-01-packs` — latest genuinely COMPLETE pass: **none** (pass1 HARNESS_FAILURE, pass2 HARNESS_FAILURE, pass3 COMPLETE -> INCOMPLETE_TURN)
- `c-02-roles` — latest genuinely COMPLETE pass: **none** (pass1 HARNESS_FAILURE, pass2 COMPLETE -> INCOMPLETE_TURN)
- `c-03-markprep` — latest genuinely COMPLETE pass: **none** (pass1 HARNESS_FAILURE, pass2 COMPLETE -> INCOMPLETE_TURN)
- `c-04-decide` — latest genuinely COMPLETE pass: **none** (pass1 HARNESS_FAILURE, pass2 COMPLETE -> INCOMPLETE_TURN)
- `d-01-receipt` — latest genuinely COMPLETE pass: **none** (pass1 HARNESS_FAILURE, pass2 HARNESS_FAILURE, pass3 COMPLETE -> INCOMPLETE_TURN)
- `d-02-operator-page` — latest genuinely COMPLETE pass: **pass1** (pass1 COMPLETE)
- `d-03-decision-record` — latest genuinely COMPLETE pass: **pass1** (pass1 COMPLETE)
- `d-04-f002-outcome` — latest genuinely COMPLETE pass: **pass1** (pass1 COMPLETE)
- `e-01-refute` — latest genuinely COMPLETE pass: **pass1** (pass1 COMPLETE)
- `e-02-metric-creep` — latest genuinely COMPLETE pass: **none** (pass1 HARNESS_FAILURE, pass2 COMPLETE -> INCOMPLETE_TURN)
- `e-03-fw5-citations` — latest genuinely COMPLETE pass: **pass1** (pass1 COMPLETE)
- `e-04-f001-classes` — latest genuinely COMPLETE pass: **pass1** (pass1 COMPLETE)
- `f-01-c001-profile` — latest genuinely COMPLETE pass: **pass1** (pass1 COMPLETE)
- `f-02-commit-tree` — latest genuinely COMPLETE pass: **pass1** (pass1 COMPLETE, pass2 COMPLETE -> INCOMPLETE_TURN)
- `f-03-occ02-usage` — latest genuinely COMPLETE pass: **pass1** (pass1 COMPLETE)
- `b-004` — latest genuinely COMPLETE pass: **none** (pass1 HARNESS_FAILURE, pass2 COMPLETE -> INCOMPLETE_TURN)

11 of 26 battery tasks have a genuinely COMPLETE pass; 15 have none.

## Outside the battery

Recorded runs that are not battery tasks, listed for completeness and not scored: their `expected_outputs` are prose, not paths.

| pass | run | recorded | iters | tool calls | wall s | last finish |
|---|---|---|---|---|---|---|
| pass1 | `smoke-001` | COMPLETE | 6 | 8 | 34.0 | stop |
