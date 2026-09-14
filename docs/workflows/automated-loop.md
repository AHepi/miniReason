# Operating the automated end-to-end harness loop

This is the operator page for the automated loop of *The automated end-to-end
harness loop — FINAL design of record*. It states the command, the config, the
run directory layout, every failure code and block code the loop can emit, the
pre-registration template, the obligations template, and the claim ceiling text
verbatim.

**How this page is kept true.** Every table below is **generated from the
modules and from the driver's own argument parser** by the wave-5 integration,
and `tests/loop/test_docs_pins.py` pins each one against its source: the
failure table against `types.FAILURE_CODES`, the block table against
`types.BLOCK_CODES`, the stop vocabulary against `types.STOP_REASONS`, the
argv against `tools/auto_loop.py`'s own parser, and the ceiling block against
the bytes of `src/minireason/loop/data/ceiling_v1.md`. A code a later wave adds
without regenerating this page fails that test file.

A budget stop is a **resource boundary** — an attention-and-spend boundary —
never a claim that an inquiry ran out of things to say. No record this loop
mints carries a score, a rank or a meter, and the one token the stop vocabulary
refuses is named by its refusal in `types.py`.

## 1. The command

One command — S0 PREREGISTER through S15 CLOSE as a state machine:

```
python tools/auto_loop.py run --config <path>
```

The subcommands and flags below are generated from the driver's own parser, so
the page cannot drift from the program:

```
python tools/auto_loop.py {preregister|preflight|run|status|adjudicate|appeal|reopen|close|dry-run}
  --acknowledge   resume past a sticky halt, with --reason; itself recorded   [run]
  --config        the frozen loop config   [dry-run, preflight, preregister, run]
  --cycles        override the declared budget DOWNWARD only; upward is BUDGET_RAISED   [preregister, run]
  --dry-run-out   dry-run only: where the synthetic occurrence is built   [dry-run]
  --mode          live|offline; a mode outside PROVIDER_MODES is CONFIG_INVALID_VALUE   [preflight, preregister, run]
  --path          appeal only: the ruling to stage   [appeal]
  --publish-ref   default: the branch's upstream   [preregister, run]
  --reason        the text --acknowledge and reopen record   [reopen, run]
  --ruling        reopen only: a ruling document carrying reopen_reason   [reopen]
  --run           the run root a read-only or after-the-fact entry is pointed at   [adjudicate, appeal, close, reopen, status]
```

`auto_loop dry-run` is the build's acceptance gate: the whole machine walks
S0→S15 against `OfflineProvider` and a real bare git repository in a temp
directory, with one induced instance of each failure family named by code on
the closing receipt, and zero network calls asserted by a provider-module
counter.

### 1.1 The states, and what runs each

| state | step kind | the function that runs it | what it does |
|---|---|---|---|
| S0 | `PREREGISTER` | `auto_loop.preregister` | freeze the config, mint `loop_plan_id`, stage the bundle, seal every contrast baseline, open every reading, register and juxtaposition cell |
| S1 | `PREFLIGHT` | `auto_loop.preflight` | offline: verify every pin, build the seat plan, self-test every reading key's coordinate and the guard-block streak definition, compare the opened register cells with what `markprep.program_marks` will produce, and refuse a planned-call figure past `max_calls` |
| S2 | `PUBLISH_PLAN` | `auto_loop.run/_publish_plan` | commit + push + verify the plan, and write the VERIFIED line three ways |
| S3 | `CYCLE_OPEN` | `auto_loop.run/_cycle_open` | the custody check, the budget check, the cycle receipt |
| S4 | `PREPARE` | `auto_loop.run/_prepare` | runner v2 `prepare_wave` per occurrence and problem, in-process |
| S5 | `PUBLISH_IN` | `auto_loop.run/_publish_in` | commit + push + verify the prepared wave inputs — before any socket |
| S6 | `SEND` | `auto_loop.run/_send` | runner v2 `send_round` in-process over one published HEAD; an ended arm is recorded from runner v2's own `arm_stopped` |
| S7 | `PUBLISH_EV` | `auto_loop.run/_publish_ev` | commit + push + verify the wave's records |
| S8 | `IMPORT` | `auto_loop.run/_import` | `graph_import_h005.import_occurrence` per occurrence, then the pins verified again |
| S9 | `USE_TABLE` | `auto_loop.run/_use_table` | `use_relation_h005.build_use_table` and `write_use_table`; every root cell starts empty |
| S10 | `READ` | `auto_loop.run/_read` | `reader.read_table` over the pre-registered rows, through the real guard |
| S11 | `MARK` | `auto_loop.run/_mark` | `marker.mark_cell` per contrast cell, against the baseline sealed at S0 |
| S12 | `ADJUDICATE` | `auto_loop.adjudicate` | render the tables, register the `rendered_files` record, read the situation |
| S13 | `DECIDE` | `auto_loop.run/_decide` | `decide.decide` — exactly one outcome — and `decision.json` |
| S14 | `PUBLISH_CY` | `auto_loop.run/_publish_cycle` | commit + push + verify the cycle, `CYCLE.md` included |
| S15 | `CLOSE` | `auto_loop.close` | `report.render_closing`, the ceiling verbatim, and the closing publication |
| — | `AUDIT` | `auto_loop._audit` | the section 2.5 audits when the schedule is due, as their own spending step |

Every transition writes exactly one write-once receipt. `PREPARE`,
`PUBLISH_IN`, `SEND` and `PUBLISH_EV` repeat, once per wave, until runner v2's
`ready_coordinates` is empty for the cycle; the wave label is read off the
occurrence's own wave files, so a resumed cycle re-enters at the wave the tree
is actually at.

### 1.2 The codes the driver itself adds

`tools/auto_loop.py` lives outside `src/minireason/loop/`, so these are folded
into `types.FAILURE_CODES` by hand and reached only from the driver;
`tests/loop/test_auto_loop.py` scans the driver's source and asserts each one
is raised there.

| code | why it exists |
|---|---|
| `APPEAL_PATH_INVALID` | appeal() was given no ruling path to stage, or a path that is not a readable appellate ruling document. |
| `APPEAL_TARGET_INVALID` | an appellate ruling names no registered target: a validity node, the standard, a prior ruling, or a cell:register token. |
| `BLOCK_STREAK_DEFINITION_MISMATCH` | PREFLIGHT's self-test of the guard-block streak counter did not reproduce the definition config.audit.streak_max_account states, so the account beside the number would be false. |
| `CALIBRATION_NOT_FOUND` | the run declares an audit schedule and its run root carries no calibration.json, so o5's planted-flaw clause could never be discharged by the program that evaluates it. |
| `OCCURRENCE_NOT_DISPATCHABLE` | a declared occurrence cannot be dispatched for: runner v2 refuses to verify it, or it carries a prepared wave the loop cannot drain, so the dispatch chain could never make progress and a cycle would spin instead of stopping. |
| `READING_KEY_INADMISSIBLE` | a pre-registered reading-set key folds to a coordinate W2-ROLES refuses, or two keys fold to one coordinate, so a call could not be addressed or two rows would share one records tree. |
| `READING_ROW_UNRESOLVED` | a pre-registered reading-set key names no row of the use table this cycle built, so the row could be neither read nor honestly reported as read. |
| `REGISTER_CELLS_DISAGREE` | the register cells opened at PREREGISTER are not the set markprep.program_marks will produce, so a mark would be refused after its calls were spent. |
| `RUN_NOT_FOUND` | status(), adjudicate(), appeal(), reopen() or close() could not locate a written plan for the run it was pointed at. |

## 2. The config — `minireason.loop.config.v1`

*As designed (design 4.2); the schema is implemented and strict in
`src/minireason/loop/types.py` (`LoopConfig`).*

Keys: `run_id`, `study`, `occurrences[]`, `runner`, `publish_ref`,
`cycle_budget`, `max_calls`, `reading_set[]`, `obligations_path`,
`seats{critic, defender, judges[], variator, min_judge_families, paraphrase_n,
schema_repair_budget}`, `contrast{attached, study, occurrences[]}`,
`audit{period, judge_err_max, streak_max}` — each audit threshold required and
carrying its `*_account` prose — `reopen_reasons[]`, `provider_mode`
(defaults to `offline`), `max_per_key`, `timeouts{step_seconds{}, git_seconds}`,
`graph_root`.

`loop_plan_id = sha256(canonical({"schema": PLAN_ID_SCHEMA, "config": ...,
"pins": ...}))`. The six fixed source pins are
`types.PINNED_SOURCE_PATHS` (`endpoints.json`, `graph_import_h005.py`,
`provider_openai_compat.py`, `use_relation_h005.py`,
`tools/contrast_triple_study.py`, runner v2); a pin map missing one is
`PIN_INVALID` naming the absent paths. The run-specific rest of design 4.2's
pin list — prompt templates, `obligations.json`, `CEILING.md`, the standard
body, each attached study's `PLAN.md` and `material.json`, and W2-DECIDE's own
`decide.py` pin under `decide.MODULE_PIN_KEY` — is the driver's to supply at
PREREGISTER.

### 2.1 The pins the driver supplies at S0

Beside the six fixed paths, `plan.json` carries, as this driver writes it: the
loop sources whose constants the plan leans on (`roles.py` — the declared
resource conditions are its constants, `decide.py`, `standard.py`,
`audits.py`), the run's own `obligations.json`, `CEILING.md` and
`calibration.json`, each occurrence's `plan.json` and `material.json`, each
attached contrast occurrence's `comparison.json` and `material.json`, and four
**named** module pins that are constants rather than paths —
`minireason.loop.standard.STANDARD_BODY_SHA256`,
`minireason.loop.standard.CEILING_SHA256`,
`minireason.loop.audits.CALIBRATION_EXCHANGES_SHA256` and
`minireason.loop.decide.DECIDE_SHA256` — plus the ceiling under its own pin key
`src/minireason/loop/data/ceiling_v1.md`, which is what the renderers refuse without.
`plan.json` also carries `calibration_sha256`, the digest of the run's
`calibration.json`, which every `AuditReport` this run registers writes back so
that `obligations.audit_in_force` can read it.

**A reading-set key is not a coordinate.** `roles.Coordinate` admits only
`[A-Za-z0-9][A-Za-z0-9._#-]*` per `/` segment, and a pre-registered key may
carry `->`. The driver folds each key to an admissible spelling and appends a
twelve-character digest of the exact key (`auto_loop.cell_key_for`); the
correspondence is written into `plan.json` under `reading_cells`, PREFLIGHT
asserts admissibility and injectivity over the declared set, and the plan's own
spelling stays the `row_key` on every record.

## 3. The directory layout

*As designed (design 4.2); every path is implemented by `types.run_paths`
against `<repo>/experiments/loops/<RUN-ID>/`.*

```
experiments/loops/<RUN-ID>/
  config.json  preregistration.md  obligations.json  CEILING.md  plan.json
  preflight.json  run.lock
  steps/NNNN-KIND.json[.open]
  graph/                              deepreason_core harness root (log.jsonl, blobs, objects)
  cycles/cycle-NN/{import,use-table,readings,contrast,decision.json,CYCLE.md}
  readings/<row_key>/{requests,attempts,responses,provider}/...   write-once, per role
  audits/  appeals/  errata/  CLOSING.md  READING_TABLE.md  COMPARISON.md
```

Occurrence trees stay where runner v2 and the contrast tool own them: the loop
**references them and writes nothing inside them**.

Every transition writes exactly one write-once receipt,
`steps/NNNN-KIND.json`, schema `minireason.loop.step.v1`, whose `step_key`
recomputes from the receipt's own fields and whose `spending` flag must match
design 4.3's classification of its kind. Replayable steps (PREFLIGHT, IMPORT,
USE_TABLE, ADJUDICATE, DECIDE) re-run on resume and must be byte-identical,
else `STEP_NONDETERMINISTIC`. Spending steps (SEND, READ, MARK, AUDIT, every
PUBLISH) open an `.open` marker first; an unresolved marker on resume halts
with `UNRESOLVED_STEP`. Resume past a sticky halt is
`--acknowledge <step_key> --reason "<text>"`, itself recorded.

## 4. Failure codes the loop can emit

Generated from `types.FAILURE_CODES` (218 members, every
loop module and the driver folded in) with the module that owns each, computed
from the sources. Every code the driver itself adds is in this table and in
section 1.2.

The one parameterised family: `HTTP_<status>` for a three-digit status in
classes 1–5 (`types.is_failure_code` admits it; `HTTP_429` stays an explicit
member).

| failure code | owning module |
|---|---|
| `ACTIVITY_CONTROL_CHARACTER` | `minireason/loop/receipts.py` |
| `ACTIVITY_DECISION_MISSING` | `minireason/loop/receipts.py` |
| `ACTIVITY_LOGGER_FAILED` | `minireason/loop/receipts.py` |
| `ACTIVITY_PATH_INVALID` | `minireason/loop/receipts.py` |
| `ACTIVITY_PHASE_UNKNOWN` | `minireason/loop/receipts.py` |
| `ACTIVITY_RAW_COMMAND_TEXT` | `minireason/loop/receipts.py` |
| `ACTIVITY_TOOL_MISSING` | `minireason/loop/receipts.py` |
| `APPEAL_MALFORMED` | `minireason/loop/graph.py` |
| `APPEAL_PATH_INVALID` | `tools/auto_loop.py` |
| `APPEAL_TARGET_INVALID` | `tools/auto_loop.py` |
| `APPEAL_TARGET_UNKNOWN` | `minireason/loop/graph.py` |
| `ARTIFACT_NOT_DERIVED_FROM_DELIVERY` | `minireason/loop/steps.py` |
| `AUDIT_KIND_UNKNOWN` | `minireason/loop/graph.py` |
| `BASELINE_NOT_FIRST` | `minireason/loop/markprep.py` |
| `BASELINE_RESEALED` | `minireason/loop/markprep.py` |
| `BASELINE_SEAL_BROKEN` | `minireason/loop/markprep.py` |
| `BLOCK_CODE_UNKNOWN` | `minireason/loop/types.py` |
| `BLOCK_STREAK_DEFINITION_MISMATCH` | `tools/auto_loop.py` |
| `BUDGET_RAISED` | `tools/auto_loop.py` |
| `CADENCE_BACKDATED` | `minireason/loop/receipts.py` |
| `CADENCE_THRESHOLDS_INVERTED` | `minireason/loop/receipts.py` |
| `CADENCE_THRESHOLD_INVALID` | `minireason/loop/receipts.py` |
| `CALIBRATION_NOT_FOUND` | `tools/auto_loop.py` |
| `CEILING_TEXT_MALFORMED` | `minireason/loop/report.py` |
| `CELL_KEY_INVALID` | `minireason/loop/graph.py` |
| `CELL_NOT_IN_OCCURRENCE` | `minireason/loop/markprep.py` |
| `CELL_NOT_OPEN` | `minireason/loop/graph.py` |
| `CHECK_TARGET_UNKNOWN` | `minireason/loop/publish.py` |
| `COMPARISON_SCHEMA_UNKNOWN` | `minireason/loop/markprep.py` |
| `CONCURRENCY_LIMIT_CONFLICT` | `minireason/loop/roles.py` |
| `CONFIG_INVALID_VALUE` | `minireason/loop/audits.py` |
| `CONFIG_MISSING_KEY` | `minireason/loop/audits.py` |
| `CONFIG_NOT_A_MAPPING` | `minireason/loop/seats.py` |
| `CONFIG_NOT_FOUND` | `minireason/loop/types.py` |
| `CONFIG_SCHEMA_UNKNOWN` | `minireason/loop/types.py` |
| `CONFIG_UNKNOWN_KEY` | `minireason/loop/types.py` |
| `CONTRACT_VIOLATION` | `minireason/loop/contracts.py` |
| `CREDENTIAL_IN_OUTPUT` | `minireason/loop/custody.py` |
| `CREDENTIAL_SCAN_INCOMPLETE` | `minireason/loop/custody.py` |
| `CUSTODY_MISMATCH` | `minireason/loop/steps.py` |
| `CYCLE_OUT_OF_RANGE` | `minireason/loop/types.py` |
| `DECISION_CONFIG_INVALID` | `minireason/loop/decide.py` |
| `DECISION_CYCLE_INVALID` | `minireason/loop/decide.py` |
| `DECISION_INSTRUMENT_INVALID` | `minireason/loop/decide.py` |
| `DECISION_REASON_UNKNOWN` | `minireason/loop/decide.py` |
| `DECISION_SITUATION_INVALID` | `minireason/loop/decide.py` |
| `DECISION_WOULD_REOPEN_MISSING` | `minireason/loop/decide.py` |
| `DIFFERENCE_KIND_DUPLICATE` | `minireason/loop/standard.py` |
| `DIFFERENCE_KIND_SET_EMPTY` | `minireason/loop/standard.py` |
| `DIFFERENCE_KIND_UNEXPECTED` | `minireason/loop/graph.py` |
| `DIFFERENCE_KIND_UNKNOWN` | `minireason/loop/graph.py` |
| `EXCHANGE_MALFORMED` | `minireason/loop/packs.py` |
| `FAMILY_COUNT_INSUFFICIENT` | `minireason/loop/seats.py` |
| `GIT_OPERATION_FAILED` | `minireason/loop/publish.py` |
| `GIT_SUBCOMMAND_NOT_ALLOWED` | `minireason/loop/publish.py` |
| `GRAPH_READ_ONLY` | `minireason/loop/graph.py` |
| `GRAPH_ROOT_INVALID` | `minireason/loop/graph.py` |
| `GUARD_PARAMETER_INVALID` | `minireason/loop/standard.py` |
| `GUARD_PARAMETER_MISSING` | `minireason/loop/standard.py` |
| `GUARD_PARAMETER_UNKNOWN` | `minireason/loop/standard.py` |
| `HISTORY_REWRITE_REFUSED` | `minireason/loop/publish.py` |
| `HTTP_429` | `minireason/loop/types.py` |
| `IDENTIFIER_INVALID` | `minireason/loop/graph.py` |
| `INDETERMINATE` | `minireason/loop/obligations.py` |
| `INPUT_NOT_PUBLISHED` | `minireason/loop/steps.py` |
| `KEY_MISSING` | `minireason/loop/roles.py` |
| `LEDGER_APPEND_NOT_VERIFIED` | `minireason/loop/receipts.py` |
| `LEDGER_APPEND_REENTERED` | `minireason/loop/receipts.py` |
| `LEDGER_EMPTY_PARAGRAPH` | `minireason/loop/receipts.py` |
| `LEDGER_INCOMPLETE_WRITE` | `minireason/loop/receipts.py` |
| `LEDGER_NOT_FOUND` | `minireason/loop/receipts.py` |
| `MARKER_INPUT_MALFORMED` | `minireason/loop/marker.py` |
| `MARKER_RESIDUE_CONTRADICTED` | `minireason/loop/marker.py` |
| `MARKPREP_INPUT_MALFORMED` | `minireason/loop/markprep.py` |
| `MARK_REGISTER_MISSING` | `minireason/loop/graph.py` |
| `MARK_REGISTER_UNEXPECTED` | `minireason/loop/graph.py` |
| `MOMENT_NOT_AWARE` | `minireason/loop/receipts.py` |
| `MOMENT_NOT_DATETIME` | `minireason/loop/receipts.py` |
| `NEW_PREREGISTRATION_REQUIRED` | `minireason/loop/types.py` |
| `NOT_DISPATCHED` | `minireason/loop/obligations.py` |
| `NO_REPLAY` | `minireason/loop/roles.py` |
| `OBLIGATIONS_DIGEST_MISMATCH` | `minireason/loop/obligations.py` |
| `OBLIGATIONS_FILE_MISSING` | `minireason/loop/obligations.py` |
| `OBLIGATIONS_MALFORMED` | `minireason/loop/obligations.py` |
| `OBLIGATIONS_MISSING_KEY` | `minireason/loop/obligations.py` |
| `OBLIGATIONS_NOT_A_MAPPING` | `minireason/loop/obligations.py` |
| `OBLIGATIONS_PIN_SHIFTED` | `minireason/loop/obligations.py` |
| `OBLIGATIONS_SCHEMA_UNKNOWN` | `minireason/loop/obligations.py` |
| `OBLIGATIONS_UNKNOWN_KEY` | `minireason/loop/obligations.py` |
| `OBLIGATION_CHECK_UNKNOWN` | `minireason/loop/obligations.py` |
| `OBLIGATION_FIELD_INVALID` | `minireason/loop/obligations.py` |
| `OBLIGATION_FIELD_MISSING` | `minireason/loop/obligations.py` |
| `OBLIGATION_ID_DUPLICATE` | `minireason/loop/obligations.py` |
| `OBLIGATION_ID_MALFORMED` | `minireason/loop/obligations.py` |
| `OBLIGATION_IN_BOTH_SETS` | `minireason/loop/obligations.py` |
| `OBLIGATION_MEMBERSHIP_UNKNOWN` | `minireason/loop/obligations.py` |
| `OBLIGATION_UNKNOWN` | `minireason/loop/obligations.py` |
| `OCCURRENCE_NOT_DISPATCHABLE` | `tools/auto_loop.py` |
| `PACK_ADJUDICATION_KEY` | `minireason/loop/packs.py` |
| `PACK_INPUT_INVALID` | `minireason/loop/packs.py` |
| `PATH_ESCAPES_RUN_ROOT` | `minireason/loop/custody.py` |
| `PATH_INVALID` | `minireason/loop/types.py` |
| `PATH_IS_REPO_ROOT` | `minireason/loop/publish.py` |
| `PATH_MISSING` | `minireason/loop/publish.py` |
| `PATH_NOT_EXPLICIT` | `minireason/loop/publish.py` |
| `PATH_NOT_RESOLVABLE` | `minireason/loop/custody.py` |
| `PATH_OUTSIDE_REPO` | `minireason/loop/publish.py` |
| `PIN_INVALID` | `minireason/loop/types.py` |
| `PIN_MAP_MISSING` | `minireason/loop/custody.py` |
| `PLAN_ID_MISMATCH` | `minireason/loop/steps.py` |
| `PLAN_MIRROR_MALFORMED` | `minireason/loop/standard.py` |
| `PRECEDENT_QUERY_INVALID` | `minireason/loop/packs.py` |
| `PREDICATE_CONTRACT_VIOLATED` | `minireason/loop/obligations.py` |
| `PREREGISTRATION_SENTENCE_MISSING` | `minireason/loop/receipts.py` |
| `PROVIDER_GATEWAY_WALL` | `minireason/loop/roles.py` |
| `PROVIDER_REQUEST_FILE_CHANGED` | `minireason/loop/steps.py` |
| `PUBLISH_ATTEMPT_INVALID` | `minireason/loop/publish.py` |
| `PUBLISH_MESSAGE_EMPTY` | `minireason/loop/publish.py` |
| `PUBLISH_NOT_CONVERGING` | `minireason/loop/publish.py` |
| `PUBLISH_PATHS_EMPTY` | `minireason/loop/publish.py` |
| `PUBLISH_PATHS_UNTRACKED` | `minireason/loop/publish.py` |
| `PUBLISH_PENDING` | `minireason/loop/steps.py` |
| `PUBLISH_REF_CHANGED` | `minireason/loop/publish.py` |
| `PUBLISH_REF_INVALID` | `minireason/loop/publish.py` |
| `PUBLISH_REF_UNRESOLVED` | `minireason/loop/publish.py` |
| `READER_OUTCOME_UNKNOWN` | `minireason/loop/reader.py` |
| `READER_ROW_DUPLICATE` | `minireason/loop/reader.py` |
| `READER_ROW_INVALID` | `minireason/loop/reader.py` |
| `READING_KEY_INADMISSIBLE` | `tools/auto_loop.py` |
| `READING_ROW_UNRESOLVED` | `tools/auto_loop.py` |
| `READING_TOKEN_UNKNOWN` | `minireason/loop/graph.py` |
| `READING_TOKEN_UNRESOLVED` | `minireason/loop/graph.py` |
| `RECEIPT_BODY_AMBIGUOUS` | `minireason/loop/receipts.py` |
| `RECEIPT_FIELDS_MISSING` | `minireason/loop/receipts.py` |
| `RECEIPT_FORM_MALFORMED` | `minireason/loop/receipts.py` |
| `RECEIPT_ID_MALFORMED` | `minireason/loop/receipts.py` |
| `RECEIPT_SUFFIX_MALFORMED` | `minireason/loop/receipts.py` |
| `RECORD_NOT_SERIALISABLE` | `minireason/loop/custody.py` |
| `RECORD_WRITE_FAILED` | `minireason/loop/custody.py` |
| `REGISTER_CELLS_DISAGREE` | `tools/auto_loop.py` |
| `REGISTER_SET_MISMATCH` | `minireason/loop/standard.py` |
| `REGISTER_TEXT_EMPTY` | `minireason/loop/standard.py` |
| `REGISTER_UNKNOWN` | `minireason/loop/markprep.py` |
| `REGISTRATION_REFUSED` | `minireason/loop/graph.py` |
| `REGISTRY_INVALID` | `minireason/loop/seats.py` |
| `REOPEN_REASON_SET_EMPTY` | `minireason/loop/standard.py` |
| `REOPEN_REASON_UNKNOWN` | `minireason/loop/standard.py` |
| `REOPEN_REFUSED` | `minireason/loop/synthetic.py` |
| `REPLICATE_BYTES_DISAGREE` | `minireason/loop/markprep.py` |
| `REPLICATE_NOT_READABLE` | `minireason/loop/markprep.py` |
| `REPLICATE_UNKNOWN` | `minireason/loop/markprep.py` |
| `REPO_NOT_A_GIT_CHECKOUT` | `minireason/loop/publish.py` |
| `REQUEST_NOT_FROM_PLAN` | `minireason/loop/steps.py` |
| `RESOURCE_BOUNDARY_MISDESCRIBED` | `minireason/loop/standard.py` |
| `ROLE_COORDINATE_INVALID` | `minireason/loop/roles.py` |
| `ROLE_PACK_INVALID` | `minireason/loop/roles.py` |
| `ROLE_PACK_NOT_JSON_MODE_READY` | `minireason/loop/roles.py` |
| `ROLE_REGISTER_REQUIRED` | `minireason/loop/roles.py` |
| `ROLE_REPAIR_REFUSED` | `minireason/loop/roles.py` |
| `ROLE_SCHEMA_NOT_THE_CONTRACT` | `minireason/loop/roles.py` |
| `ROLE_SEAT_MISMATCH` | `minireason/loop/roles.py` |
| `ROLE_TOKEN_BUDGET_UNREACHABLE` | `minireason/loop/roles.py` |
| `ROLE_UNKNOWN` | `minireason/loop/roles.py` |
| `RUNNER_NOT_IMPORTABLE` | `minireason/loop/seats.py` |
| `RUNTIME_SOURCE_CHANGED` | `minireason/loop/steps.py` |
| `RUN_ID_INVALID` | `minireason/loop/types.py` |
| `RUN_LOCKED` | `minireason/loop/steps.py` |
| `RUN_NOT_FOUND` | `tools/auto_loop.py` |
| `SCHEMA_INVALID` | `minireason/loop/contracts.py` |
| `SCORING_KEY_FORBIDDEN` | `minireason/loop/contracts.py` |
| `SEAT_COUNT_INSUFFICIENT` | `minireason/loop/seats.py` |
| `SECRET_IN_RECEIPT` | `minireason/loop/receipts.py` |
| `SECRET_IN_REQUEST` | `minireason/loop/roles.py` |
| `SECRET_IN_STAGED_DIFF` | `minireason/loop/publish.py` |
| `SITUATION_INVALID` | `minireason/loop/obligations.py` |
| `SOURCE_PIN_MALFORMED` | `minireason/loop/custody.py` |
| `SOURCE_PIN_MISMATCH` | `minireason/loop/custody.py` |
| `SOURCE_PIN_MISSING` | `minireason/loop/custody.py` |
| `SOURCE_PIN_NOT_A_FILE` | `minireason/loop/custody.py` |
| `SOURCE_PIN_OUTSIDE_REPOSITORY` | `minireason/loop/custody.py` |
| `SPEC_ID_MISMATCH` | `minireason/loop/standard.py` |
| `STANDARD_ARGUMENT_REFUSED` | `minireason/loop/standard.py` |
| `STANDARD_BODY_MALFORMED` | `minireason/loop/standard.py` |
| `STANDARD_DATA_MALFORMED` | `minireason/loop/report.py` |
| `STANDARD_DATA_MISSING` | `minireason/loop/standard.py` |
| `STANDARD_NOT_REGISTERED` | `minireason/loop/graph.py` |
| `STANDARD_SCHEMA_MISMATCH` | `minireason/loop/standard.py` |
| `STANDARD_SECTION_MISSING` | `minireason/loop/standard.py` |
| `STEP_BODY_FAILED` | `minireason/loop/steps.py` |
| `STEP_CLASS_DISAGREEMENT` | `minireason/loop/steps.py` |
| `STEP_KEY_MISMATCH` | `minireason/loop/types.py` |
| `STEP_NONDETERMINISTIC` | `minireason/loop/steps.py` |
| `STEP_NOT_HALTED` | `minireason/loop/steps.py` |
| `STEP_OUTPUTS_INVALID` | `minireason/loop/steps.py` |
| `STEP_RECEIPT_INVALID` | `minireason/loop/steps.py` |
| `STEP_TIMEOUT` | `minireason/loop/steps.py` |
| `STOP_REASON_UNKNOWN` | `minireason/loop/types.py` |
| `SURFACE_NO_MATERIAL` | `minireason/loop/surface.py` |
| `SURFACE_ROW_MALFORMED` | `minireason/loop/surface.py` |
| `SURFACE_SPAN_DISAGREES` | `minireason/loop/surface.py` |
| `SYNTHETIC_COORDINATE_UNSCRIPTED` | `minireason/loop/synthetic.py` |
| `SYNTHETIC_INDUCTION_UNKNOWN` | `minireason/loop/synthetic.py` |
| `TIMEOUT_NOT_APPLIED` | `minireason/loop/steps.py` |
| `TRANSCRIPT_MALFORMED` | `minireason/loop/graph.py` |
| `TRANSCRIPT_NOT_CONFORMING` | `minireason/loop/graph.py` |
| `TRANSCRIPT_POINT_NOT_UNIQUE` | `minireason/loop/graph.py` |
| `TRANSPORT_OR_RESPONSE_ERROR` | `minireason/loop/roles.py` |
| `TRANSPORT_PIN_MISMATCH` | `minireason/loop/steps.py` |
| `TRIAL_ARGUMENT_INVALID` | `minireason/loop/trial.py` |
| `TRIAL_MODE_UNEXPECTED` | `minireason/loop/trial.py` |
| `TRIAL_PRIOR_STATE_UNREADABLE` | `minireason/loop/trial.py` |
| `TRIAL_SEAT_PLAN_INVALID` | `minireason/loop/trial.py` |
| `UNEXPECTED_STAGED_FILES` | `minireason/loop/publish.py` |
| `UNRESOLVED_NOT_IN_VOCABULARY` | `minireason/loop/standard.py` |
| `UNRESOLVED_STEP` | `minireason/loop/steps.py` |
| `VOCABULARY_DUPLICATE` | `minireason/loop/standard.py` |
| `VOCABULARY_EMPTY` | `minireason/loop/standard.py` |
| `VOCABULARY_NOT_CLOSED` | `minireason/loop/standard.py` |
| `WRITE_ONCE_VIOLATION` | `minireason/loop/custody.py` |

### 4.1 Stop vocabulary

`stop_reason` is a member of this closed set (`types.STOP_REASONS`), plus the
one parameterised member `preregistered_condition:<id>`:

| stop reason | what it names |
|---|---|
| `all_arms_ended` | guard rail: every declared arm ended on a delivery failure |
| `custody_halt` | guard rail: a custody failure halted the loop; never worked around |
| `instrument_fault` | guard rail: a guard-block streak past `streak_max`, or a calibration error share past `judge_err_max`; it stops the reading arm and spawns audit-the-reader |
| `no_new_reading_changes` | clause 4: this cycle's `(cell, register, mark)` set is identical to the previous cycle's — a set identity, never a count |
| `obligations_discharged` | clause 3: every failed obligation of O now holds |
| `protected_loss` | clause 1: a protected obligation held and no longer does |
| `resource_boundary` | clause 5: a declared budget or `max_calls` — an attention-and-spend boundary, never a claim the inquiry ran out of things to say |
| `preregistered_condition:<id>` | the declared-condition clause, evaluated after clause 5 so it masks nothing; `types.is_stop_reason` refuses an id carrying the refused stem |

### 4.2 Outcome codes

`types.OUTCOME_CODES`: a token a record may carry to name something the loop
**did**, disjoint from the failure table:

| outcome code | owning module | what it names |
|---|---|---|
| `APPELLATE_RULING_APPLIED` | `minireason/loop/synthetic.py` | an appellate ruling was ingested and pass 1 recomputed under it, so a label moved. The driver files it at S3 and the closing record names it; it is never a refusal and never a block. |

## 5. Block codes the guard can emit

A block registers nothing, leaves the cell unresolved, and is counted by its
code; a high block rate is the instrument declining to read, never an absence
of relations. Spelled `blocked:<name>` and built only through
`types.block_code(reason)`. Generated from `types.BLOCK_CODES` (10
members): nine are exactly the reasons the frozen ceiling's block-register
clause names in its own order (`types.CEILING_BLOCK_REASONS`);
`blocked:constitution` is the one extra (the G0 channel), reported outside the
printed register.

Every row names `types.py` in its middle column, and that is the point
(REVIEW-PREREG PR-12): **no module writes a `blocked:` prefix in a string
literal.** `types.BLOCK_CODES` is the one owner of every spelling and
`types.block_code(reason)` is the one builder; `trial` and `marker` import the
codes they return. The right-hand column names the guard that returns each.

| block code | where the spelling lives | which guard returns it |
|---|---|---|
| `blocked:baseline-forced-same` | `minireason/loop/types.py` | G9: the program wrote `same` over a `differs` whose difference kind the sealed within-ORIGINAL baseline already exhibits |
| `blocked:constitution` | `minireason/loop/types.py` | G0: the seat constitution declined the coordinate before anything was dispatched; the one block code the frozen ceiling does not print in its register |
| `blocked:ensemble-split` | `minireason/loop/types.py` | G5: the two judge seats did not agree at the as-declared presentation; both rulings are recorded verbatim and nothing is voted |
| `blocked:operative-target` | `minireason/loop/types.py` | G3: the citation resolved outside the declared referring record, target record or listed body passage |
| `blocked:order-swap` | `minireason/loop/types.py` | G6: a seat's ruling did not survive reading the exchange in both presentation orders |
| `blocked:outside-vocabulary` | `minireason/loop/types.py` | G4/D6: the critic wrote outside the closed six-value vocabulary; the text is preserved verbatim and the cell stays unresolved |
| `blocked:paraphrase-flip` | `minireason/loop/types.py` | G7: the ruling did not survive the pre-registered meaning-preserving paraphrases; no warrant is registered |
| `blocked:provider` | `minireason/loop/types.py` | the route did not deliver: the transport's own stable code rides beside it, and a delivery failure mints no warrant |
| `blocked:referential-integrity` | `minireason/loop/types.py` | G2: the cited passage does not resolve to a unique offset on its surface |
| `blocked:schema` | `minireason/loop/types.py` | G1: a role's output did not conform to its contract; the sub-reason rides on `contracts.SCHEMA_REASONS` |

## 6. The two narrowings of published instruments

The run narrows two published instruments to make the reading cells
machine-fillable, and the narrowing is part of the claim. Quoted from the frozen
ceiling's own clause:

> **Two published instruments were narrowed to make these cells machine-fillable, and the narrowing is part of the claim.** `ROOT_READING_VOCABULARY` is published as a suggestion that a row may exceed and that root may write outside; this run closes it to six values and routes anything outside to `unresolved:outside-vocabulary` with the text preserved.

> And where the published instrument says "the reading is root's", this table says the reading is a guarded `judge`-role artifact and **root has not read it**.

Both narrowings are in the claim ceiling below and in every rendered table.

## 7. Concurrency and the gateway wall

The two-credential concurrency fact, from `notes/WAVE2-INTERFACE.md` and the
design (4.6): `endpoints.json` declares 24 endpoints but only two `key_env`
values, and the process-wide ceiling is **five concurrent calls per
credential** (`provider_openai_compat.slots_for(key_env, cap)`, with runner
v2's `key_gate` imported — never copied — as the outer mirror), so wave
capacity is 5 × 2 = 10 and 22 endpoints share one gate. A reading call and a
dispatch call in flight together are held to five per credential between them.
This holds only inside one process: the driver imports runner v2 and calls
`send_round` in-process, and `run.lock` refuses a second concurrent driver on
the same run.

Independently of the endpoints' declared `timeout_seconds`, the study
transport closes a request open at the **300 s gateway wall**
(`roles.GATEWAY_WALL_SECONDS`): the wall in force for a seat is
`min(seat.timeout_seconds, 300)`. A route closed at the wall is recorded with
reason `PROVIDER_GATEWAY_WALL` and the transport's own code beside it — a
named delivery fact, never a semantic verdict, and it mints no warrant.

## 8. The pre-registration template

*As designed (design section 8); the driver emits `preregistration.md` at S0
and `receipts.open_receipt` appends the ledger receipt before any call. The
text below is the template's field list; the receipt's own prose is design
section 8 verbatim and is asserted sentence-wise by the receipts module
(`PREREGISTRATION_SENTENCE_MISSING`).*

A pre-registration under this loop declares, **before first look and
unchangeable inside this chain**:

- **Budget** — `cycle_budget` and `max_calls`; `--cycles` may only override
  the budget downward, and an upward override is `BUDGET_RAISED`. A reached
  budget is a declared resource boundary, and the closing record states which
  was reached.
- **Stop conditions** — the decision rule with its three guard rails
  (`custody_halt`, `all_arms_ended`, `instrument_fault`), its five clauses in
  `types.STOP_REASONS` order, the declared-condition clause
  (`preregistered_condition:<id>`), the audit thresholds with their accounts,
  and the open continuation.
- **Reading set** — `reading_set[]`, frozen into `loop_plan_id`.
- **O and P** — `obligations.json` with the failed set O and the protected
  set P, pinned by sha256 (both digests named: the file digest that enters
  `loop_plan_id`, and the canonical-body digest `obligations.canonical_pin`).
- **Falsifiers** — the planted-flaw calibration set with its
  `true_by_construction` grounds, the audit schedule with `judge_err_max` and
  `streak_max`, and the guard parameters (`TRIAL_PARAPHRASE_N`,
  `schema_repair_budget`) under which a misread is caught rather than
  published. The honest consequence is stated in advance: the guard is strict
  enough that the run may return mostly `unresolved` and stop at the
  no-new-reading-changes clause, and that is reported as a result about the
  instrument's reach, never as evidence about the material.
- **Would-reopen** — the `reopen_reasons[]` list and the ceiling's own
  reopening clause: an appellate ruling; a successful attack on
  `std:reading-rubric/v1` or on a register definition; a custody correction; a
  third judge family; more replicates; a raised budget under a new
  `loop_plan_id`.

Changing anything above after first look mints a new `loop_plan_id` and is a
new pre-registration, not an amendment.

## 9. The obligations template — `minireason.loop.obligations.v1`

Mirrors the schema of `src/minireason/loop/obligations.py` (`load_obligations`).
Shape:

```json
{
  "schema": "minireason.loop.obligations.v1",
  "run_id": "<RUN-ID>",
  "obligations": [
    {
      "id": "o1",
      "set": "O",
      "statement": "the prose obligation, in the document's own words",
      "check": {
        "predicate": "obligations.row_disposition_complete",
        "artifact": ["reading_set"],
        "detail": "how the program reads the artifact"
      },
      "why_not_a_count": "why this obligation's verdict is a token, not a quantity"
    }
  ],
  "obligations_sha256": "<canonical-body digest, key omitted from itself>",
  "obligations_sha256_recipe": "canonical JSON over the document minus the digest keys"
}
```

Rules the loader enforces, each with its refusal code in the table of section
4: exactly the declared top-level keys; `"set"` is `O` or `P` and membership
is exclusive; `id` is a short lower-case token, unique; `check` names a
predicate of the registry below; a declared `obligations_sha256` must
reproduce from the content (`OBLIGATIONS_DIGEST_MISMATCH`). The pin folded
into `loop_plan_id` is the file's byte sha256 (`obligations.pin`); the
canonical-body digest is `obligations.canonical_pin`, and the bundle publishes
both and says which is which (REVIEW-PREREG PR-02).

The program predicates a check may name (`obligations.PREDICATES`; every one
answers with `satisfied` / `not_satisfied` / `not_evaluable`, and
not-evaluable is never a failure — FW5 R5):

| predicate | the question it answers |
|---|---|
| `obligations.appellate_optional` | does no record declare itself blocked on the appellate? |
| `obligations.audit_in_force` | does a registered audit record declare that it covers this cycle, naming its seats and calibration? |
| `obligations.baseline_sealed_and_carried` | is the baseline sealed over every declared register and carried by every cross-case call record? |
| `obligations.baseline_still_pinned` | does every marked cell carry the sealed baseline's own digest? |
| `obligations.blocks_named` | does every block carry a code from types.BLOCK_CODES and both of its blob refs? |
| `obligations.ceiling_and_trichotomy_intact` | does every rendered file carry each required ceiling sentence verbatim, at the pinned body? |
| `obligations.citations_reresolve` | does every relation's and every mark's quote occur exactly once on its recorded surface? |
| `obligations.mark_disposition_complete` | does every declared mark cell carry a mark (with a difference kind where it differs), or a reason? |
| `obligations.no_aggregation` | is there no aggregate field, and did every split ruling leave its row unresolved? |
| `obligations.no_edges_on_studied_nodes` | is the set of att edges landing on a studied node empty, and is the set of edges sourced at one empty, a dep landing on one being the permitted case? |
| `obligations.no_scoring_key` | is the graph free of every key the declared forbidden-key vocabulary names? |
| `obligations.original_bytes_unchanged` | does every material record still hash to the digest it and the pinned map declare? |
| `obligations.published_tree_untouched` | do the observed digests of the published tree match the map pinned at PREREGISTER? |
| `obligations.published_unresolved_preserved` | does every published-unresolved cell still stand, unless a guarded reading attacks it? |
| `obligations.recoding_table_complete` | does every recoded unit the table declares it covers have a correspondence row? |
| `obligations.row_disposition_complete` | does every declared reading row carry a relation with a citation, or a reason from the closed set? |
| `obligations.shared_envelope_intact` | do the cases of one group share a byte-identical frame outside the objection block? |
| `obligations.trichotomy_rendered` | is every declared cell rendered under exactly one of read / unresolved / machine-unresolved / unread? |
| `obligations.write_once_no_replay` | does each coordinate carry one record, with no rewrite and no declared replay? |

## 10. The claim ceiling, verbatim

The bytes below are `src/minireason/loop/data/ceiling_v1.md` at sha256
`1e26be087483fd1b9c8e2c403cfae646fb07ebc773f23434a0c4dfab3ed04c1e`, reproduced byte for byte.
`report.py` refuses to render any table or record without it, and
`tests/loop/test_docs_pins.py` asserts this block equals the file.

<!-- CEILING:BEGIN -->
**What this run claims.** Under registered standard `std:reading-rubric/v1` (digest …), a cross-family judge ensemble unanimously sustained relation *r* for this cell, citing a passage that resolves by program to a unique byte offset [s,e) inside the declared referring record, target record or listed body passage; the ruling survived order-swap and *N* meaning-preserving paraphrases of the exchange; the seats' audit record at ruling time was *A*. The reading is a registered, attackable artifact of `provenance.role = critic` carrying the literal role name `judge`, and it falls automatically if the standard, the evidence, or the seats' reliability is successfully attacked.

**This run cannot claim FW5:628's witness of reason use.** A transcript supplies no structural map from the represented objection organization into a response suborganization preserving internal role bindings on an active dependency route, and neither does an ensemble of readers of that transcript. The strongest positive outcome available is *consistent-with*.

**A null on the recoding or the carrier leg leaves those rival explanations unrefuted and unsupported, not excluded.** At N = 5 this is a limit of the design, not a finding.

**Agreement between two cross-family readers is agreement between two conditioned generators, not corroboration by two independent observers.** The guard measures behavioural stability under paraphrase, order and adversarial answer — not truth. Ten `family` labels over 24 endpoints and two credentials is a delivery fact, not an independence proof.

**An unresolved cell proves neither presence nor absence** (FW5:634). Ended arms, guard blocks, PARTIAL deliveries, bare-token ambiguity and under-replication are silent about content; non-evaluability is not refutation.

**Three cell states are distinct and are printed as three things.** An *unread* cell is one nobody and nothing has read. An *unresolved* cell is a deliberate reading that stays unresolved. A *machine-unresolved* cell is one the guard declined to resolve, and it names the block code that declined it. Conflating any two would let an unfinished worksheet read as a finding.

**A high block rate is the instrument declining to read. It is never an absence of relations.** The block register by reason code — `ensemble-split`, `referential-integrity`, `operative-target`, `order-swap`, `paraphrase-flip`, `outside-vocabulary`, `schema`, `provider`, `baseline-forced-same` — is printed with counts on every table.

**No count is an automatic warrant** (FW5:851). Marks are reported per register and are never summed, averaged, weighted or ranked. Endpoints are independent occasions to look for one pattern, never competitors (FW5:849).

**A reached ceiling is a declared resource boundary, not exhaustion of the inquiry**, and this record states which was reached and what would reopen the question.

**`appellate_rulings: N`.** Where N = 0, this record does not describe the run as validated, checked or confirmed. That the loop ran without a human is a fact about the loop, not a fact about the readings.

**Two published instruments were narrowed to make these cells machine-fillable, and the narrowing is part of the claim.** `ROOT_READING_VOCABULARY` is published as a suggestion that a row may exceed and that root may write outside; this run closes it to six values and routes anything outside to `unresolved:outside-vocabulary` with the text preserved. And where the published instrument says "the reading is root's", this table says the reading is a guarded `judge`-role artifact and **root has not read it**.

**What would reopen this:** an appellate ruling; a successful attack on `std:reading-rubric/v1` or on a register definition, which collapses every ν citing it in pass 1; a custody correction; a third judge family; more replicates; a raised budget under a new `loop_plan_id`.
<!-- CEILING:END -->
