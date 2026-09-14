# W6-DOC — Operating the automated end-to-end harness loop

This is the operator page for the automated loop of *The automated end-to-end
harness loop — FINAL design of record*. It states the command, the config, the
run directory layout, every failure code and block code the loop can emit, the
pre-registration template, the obligations template, and the claim ceiling
text verbatim.

**Status of this page.** The loop modules exist under `src/minireason/loop/`;
the **driver does not exist yet**. Everything marked *as designed* is quoted
from the design of record; the driver's actual argv is pinned at integration.
Every code table on this page is **generated from the modules** and pinned by
`tests/loop/test_docs_pins.py`; codes the driver adds are appended at integration.

A budget stop is a **resource boundary** — an attention-and-spend boundary —
never a claim that an inquiry ran out of things to say. No record this loop
mints carries a score, a rank or a meter, and the one token the stop
vocabulary refuses is named by its refusal in `types.py`.

## 1. The command

*As designed (design section 4.1/4.2); the driver's actual argv is pinned at integration.*

One command — S0 PREREGISTER through S15 CLOSE as a state machine:

```
python tools/auto_loop.py run --config <path>
```

Subcommands and flags, as designed:

```
tools/auto_loop.py {preregister|preflight|run|status|adjudicate|appeal|reopen|close|dry-run}
  --config PATH          frozen loop config (required for all but status)
  --cycles N             override the declared budget DOWNWARD only; upward => BUDGET_RAISED
  --mode live|offline    offline forces OfflineProvider everywhere
  --acknowledge KEY --reason TEXT   resume past a sticky halt (itself recorded)
  --ruling PATH          reopen only
  --publish-ref REF      default: the branch's upstream
  --dry-run-out DIR      dry-run only
```

`auto_loop dry-run` is the build's acceptance gate: the whole machine walks
S0→S15 against `OfflineProvider` and a real bare git repository in a temp dir,
with one induced instance of each failure family named by code on the closing
receipt, and zero network calls asserted by a provider-module counter.

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

Generated from `types.FAILURE_CODES` (201 members, complete for all sixteen
loop modules after wave 2) with the module that owns each, computed from the
module sources. **Codes the driver adds are appended at integration.**

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
| `APPEAL_TARGET_UNKNOWN` | `minireason/loop/graph.py` |
| `ARTIFACT_NOT_DERIVED_FROM_DELIVERY` | `minireason/loop/steps.py` |
| `AUDIT_KIND_UNKNOWN` | `minireason/loop/graph.py` |
| `BASELINE_NOT_FIRST` | `minireason/loop/packs.py` |
| `BASELINE_RESEALED` | `minireason/loop/markprep.py` |
| `BASELINE_SEAL_BROKEN` | `minireason/loop/markprep.py` |
| `BLOCK_CODE_UNKNOWN` | `minireason/loop/types.py` |
| `BUDGET_RAISED` | `minireason/loop/types.py` |
| `CADENCE_BACKDATED` | `minireason/loop/receipts.py` |
| `CADENCE_THRESHOLDS_INVERTED` | `minireason/loop/receipts.py` |
| `CADENCE_THRESHOLD_INVALID` | `minireason/loop/receipts.py` |
| `CEILING_TEXT_MALFORMED` | `minireason/loop/standard.py` |
| `CELL_KEY_INVALID` | `minireason/loop/graph.py` |
| `CELL_NOT_IN_OCCURRENCE` | `minireason/loop/markprep.py` |
| `CELL_NOT_OPEN` | `minireason/loop/graph.py` |
| `CHECK_TARGET_UNKNOWN` | `minireason/loop/publish.py` |
| `COMPARISON_SCHEMA_UNKNOWN` | `minireason/loop/markprep.py` |
| `CONCURRENCY_LIMIT_CONFLICT` | `minireason/loop/seats.py` |
| `CONFIG_INVALID_VALUE` | `minireason/loop/seats.py` |
| `CONFIG_MISSING_KEY` | `minireason/loop/seats.py` |
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
| `HTTP_429` | `minireason/loop/steps.py` |
| `IDENTIFIER_INVALID` | `minireason/loop/graph.py` |
| `INDETERMINATE` | `minireason/loop/steps.py` |
| `INPUT_NOT_PUBLISHED` | `minireason/loop/publish.py` |
| `KEY_MISSING` | `minireason/loop/roles.py` |
| `LEDGER_APPEND_NOT_VERIFIED` | `minireason/loop/receipts.py` |
| `LEDGER_APPEND_REENTERED` | `minireason/loop/receipts.py` |
| `LEDGER_EMPTY_PARAGRAPH` | `minireason/loop/receipts.py` |
| `LEDGER_INCOMPLETE_WRITE` | `minireason/loop/receipts.py` |
| `LEDGER_NOT_FOUND` | `minireason/loop/receipts.py` |
| `MARKPREP_INPUT_MALFORMED` | `minireason/loop/markprep.py` |
| `MARK_REGISTER_MISSING` | `minireason/loop/graph.py` |
| `MARK_REGISTER_UNEXPECTED` | `minireason/loop/graph.py` |
| `MOMENT_NOT_AWARE` | `minireason/loop/receipts.py` |
| `MOMENT_NOT_DATETIME` | `minireason/loop/receipts.py` |
| `NEW_PREREGISTRATION_REQUIRED` | `minireason/loop/types.py` |
| `NOT_DISPATCHED` | `minireason/loop/obligations.py` |
| `NO_REPLAY` | `minireason/loop/synthetic.py` |
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
| `PACK_ADJUDICATION_KEY` | `minireason/loop/packs.py` |
| `PACK_INPUT_INVALID` | `minireason/loop/packs.py` |
| `PATH_ESCAPES_RUN_ROOT` | `minireason/loop/custody.py` |
| `PATH_INVALID` | `minireason/loop/receipts.py` |
| `PATH_IS_REPO_ROOT` | `minireason/loop/publish.py` |
| `PATH_MISSING` | `minireason/loop/publish.py` |
| `PATH_NOT_EXPLICIT` | `minireason/loop/publish.py` |
| `PATH_NOT_RESOLVABLE` | `minireason/loop/custody.py` |
| `PATH_OUTSIDE_REPO` | `minireason/loop/publish.py` |
| `PIN_INVALID` | `minireason/loop/custody.py` |
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
| `READING_TOKEN_UNKNOWN` | `minireason/loop/graph.py` |
| `READING_TOKEN_UNRESOLVED` | `minireason/loop/graph.py` |
| `RECEIPT_BODY_AMBIGUOUS` | `minireason/loop/receipts.py` |
| `RECEIPT_FIELDS_MISSING` | `minireason/loop/receipts.py` |
| `RECEIPT_FORM_MALFORMED` | `minireason/loop/receipts.py` |
| `RECEIPT_ID_MALFORMED` | `minireason/loop/receipts.py` |
| `RECEIPT_SUFFIX_MALFORMED` | `minireason/loop/receipts.py` |
| `RECORD_NOT_SERIALISABLE` | `minireason/loop/custody.py` |
| `RECORD_WRITE_FAILED` | `minireason/loop/custody.py` |
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
| `RUNTIME_SOURCE_CHANGED` | `minireason/loop/custody.py` |
| `RUN_ID_INVALID` | `minireason/loop/types.py` |
| `RUN_LOCKED` | `minireason/loop/steps.py` |
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
| `STANDARD_DATA_MALFORMED` | `minireason/loop/standard.py` |
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
| `TRANSPORT_OR_RESPONSE_ERROR` | `minireason/loop/synthetic.py` |
| `TRANSPORT_PIN_MISMATCH` | `minireason/loop/steps.py` |
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
| `all_arms_ended` | guard rail: every arm ended on a provider failure |
| `custody_halt` | guard rail: a custody failure halted the loop; never worked around |
| `instrument_fault` | guard rail: the instrument signalled a fault (audits) |
| `no_new_reading_changes` | clause 4: the cycle changed no reading (set identity) |
| `obligations_discharged` | clause 3: every failed obligation of O now holds |
| `protected_loss` | clause 1: a protected obligation held and no longer does |
| `resource_boundary` | clause 5: a declared budget — an attention-and-spend boundary, never a claim the inquiry ran out of things to say |
| `preregistered_condition:<id>` | the declared-condition clause; `types.is_stop_reason` refuses an id carrying the refused stem |

### 4.2 Outcome codes

`types.OUTCOME_CODES`: a token a record may carry to name something the loop
**did**, disjoint from the failure table:

| outcome code | owning module | what it names |
|---|---|---|
| `APPELLATE_RULING_APPLIED` | `minireason/loop/synthetic.py` | an appellate ruling was ingested and pass 1 recomputed under it, so a label moved. W1-SYNTHETIC induces exactly this in the dry run and the closing receipt names it; it is never a refusal and never a block. |

## 5. Block codes the guard can emit

A block registers nothing, leaves the cell unresolved, and is counted by its
code; a high block rate is the instrument declining to read, never an absence
of relations. Spelled `blocked:<name>` and built only through
`types.block_code(reason)`. Generated from `types.BLOCK_CODES` (ten members):
nine are exactly the reasons the frozen ceiling's block-register clause names
in its own order (`types.CEILING_BLOCK_REASONS`); `blocked:constitution` is
the one extra (the G0 channel), reported outside the printed register.

| block code | owning module(s) | what it names |
|---|---|---|
| `blocked:baseline-forced-same` | `minireason/loop/types.py`, `minireason/loop/standard.py`, `minireason/loop/obligations.py`, `minireason/loop/synthetic.py`, `minireason/loop/markprep.py` | the program wrote `same` over a `differs` the sealed baseline forbids |
| `blocked:constitution` | `minireason/loop/types.py`, `minireason/loop/standard.py` | the constitution guard declined the coordinate; the one block code the frozen ceiling does not print in its register |
| `blocked:ensemble-split` | `minireason/loop/types.py`, `minireason/loop/standard.py`, `minireason/loop/synthetic.py` | the judge ensemble did not rule unanimously; the cell stays unresolved |
| `blocked:operative-target` | `minireason/loop/types.py`, `minireason/loop/standard.py`, `minireason/loop/surface.py` | the citation resolved outside the declared referring record, target record or listed body passage |
| `blocked:order-swap` | `minireason/loop/types.py`, `minireason/loop/standard.py`, `minireason/loop/packs.py` | the ruling did not survive reading the exchange in both orders |
| `blocked:outside-vocabulary` | `minireason/loop/types.py`, `minireason/loop/contracts.py`, `minireason/loop/standard.py`, `minireason/loop/receipts.py`, `minireason/loop/obligations.py` | the reading wrote outside the closed six-value vocabulary; the text is preserved and the cell forced unresolved |
| `blocked:paraphrase-flip` | `minireason/loop/types.py`, `minireason/loop/standard.py`, `minireason/loop/synthetic.py` | the ruling did not survive the pre-registered meaning-preserving paraphrases; no warrant is registered |
| `blocked:provider` | `minireason/loop/types.py`, `minireason/loop/custody.py`, `minireason/loop/contracts.py`, `minireason/loop/standard.py`, `minireason/loop/receipts.py`, `minireason/loop/publish.py`, `minireason/loop/steps.py`, `minireason/loop/surface.py`, `minireason/loop/seats.py`, `minireason/loop/graph.py`, `minireason/loop/obligations.py`, `minireason/loop/synthetic.py`, `minireason/loop/packs.py`, `minireason/loop/roles.py`, `minireason/loop/markprep.py`, `minireason/loop/decide.py` | delivery ended the arm; no semantic verdict is issued for its coordinates |
| `blocked:referential-integrity` | `minireason/loop/types.py`, `minireason/loop/standard.py`, `minireason/loop/surface.py`, `minireason/loop/synthetic.py`, `minireason/loop/packs.py` | the cited passage does not re-resolve to a unique offset on its surface |
| `blocked:schema` | `minireason/loop/types.py`, `minireason/loop/contracts.py`, `minireason/loop/standard.py`, `minireason/loop/receipts.py`, `minireason/loop/steps.py`, `minireason/loop/surface.py`, `minireason/loop/seats.py`, `minireason/loop/graph.py`, `minireason/loop/obligations.py`, `minireason/loop/synthetic.py`, `minireason/loop/packs.py`, `minireason/loop/roles.py`, `minireason/loop/markprep.py`, `minireason/loop/decide.py` | a role's output did not conform to its contract (the sub-reason rides on `contracts.SCHEMA_REASONS`) |

## 6. The two narrowings of published instruments

The run narrows two published instruments to make the reading cells
machine-fillable, and the narrowing is part of the claim. Quoted from design
section 6:

> `ROOT_READING_VOCABULARY` is published as a > suggestion that a row may exceed and that root may write outside; this run closes it to > six values and routes anything outside to `unresolved:outside-vocabulary` with the text > preserved.

> nd where the published instrument says "the reading is root's", this table > says the reading is a guarded `judge`-role artifact and **root has not read it**. > > **What would reopen this:** an appellate ruling; a successful attack on > `std:reading-rubric/v1` or on a register definition, which collapses every ν citing it > in pass 1; a custody correction; a third judge family; more replicates; a raised budget > under a new `loop_plan_id`.

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

The text below is **byte-identical to `src/minireason/loop/data/ceiling_v1.md`**
(`standard.CEILING_TEXT`, `standard.CEILING_SHA256`); the driver freezes it as
the run's `CEILING.md` at S0, folds its sha256 into `loop_plan_id`, and the
renderer refuses to emit any table or report without it. Pinned by the test.

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
