# Wave 0 — the integrated public interface

Read this before reading any wave-0 module. It is the integrator's record of what
the six modules actually expose after reconciliation, which module owns each
shared constant, what every exception carries, and what the six authors left open
for later waves.

Clone: `scratchpad/loop-impl/repo`, branch `claude/project-state-direction-j5rbun`.
Sources: `src/minireason/loop/{__init__,types,contracts,standard,custody,receipts,publish}.py`;
data: `src/minireason/loop/data/{ceiling_v1.md,plan_8a_mirror.json}`;
tests: `tests/loop/test_{types,contracts,standard,custody,receipts,publish}.py`.

Verified on the quiesced tree: loop-only `224 tests OK`; full suite
`1467 tests OK (skipped=1)` under
`PYTHONPATH=src python3 -X utf8 -m unittest discover -s tests`.

---

## 0. The one-page map

```
types  ──────────────► standard ──────────► contracts
  │  (LoopError only)      (every shared vocabulary)
  ├──► custody
  ├──► receipts
  └──► publish
```

`types` imports **no sibling** and is the root. `standard` imports `types` for
`LoopError` and nothing else of the package. `contracts` imports `standard` and
`types`. There is no cycle, and
`tests/loop/test_contracts.py::WOneOwnerPerSharedConstant::test_the_wave_zero_import_graph_is_acyclic`
walks the whole package and asserts it.

**Owner of every shared constant — `standard.py`.**

| constant | owner | `contracts` spelling |
|---|---|---|
| `READING_VOCABULARY` (6 published values, the instrument's own tuple object) | `standard` | same |
| `NOMINABLE_RELATIONS` (5, vocabulary − `unresolved`) | `standard` | — |
| `CRITIC_RELATIONS` (5 + `none`) | `standard` | same |
| `UNRESOLVED_TOKEN` | `standard` | `UNRESOLVED` |
| `NONE_TOKEN` | `standard` | `NONE_RELATION` |
| `OUTSIDE_VOCABULARY_FIELD` | `standard` | same |
| `READING_BANNER` (`use_relation_h005.USE_RELATION_BANNER`) | `standard` | same |
| `MARKS` (`differs`, `same`, `unresolved`) | `standard` | same |
| `REGISTER_IDS` (`T`,`E`,`D`,`G`) | `standard` | `REGISTERS` (same object) |
| `DIFFERENCE_KINDS` (7 tokens over 4 registers) | `standard` | same object |
| `FORBIDDEN_KEYS` (G12, 24 keys) | `standard` | same object |
| `CEILING_REQUIRED_SENTENCES` (11) | `standard` | — (W3-REPORT imports from `standard`) |
| `REOPEN_REASONS`, `FALSIFIER_MAP`, `GUARD_PARAMETERS`, `CALIBRATION_ANCHORS` | `standard` | — |
| `STOP_REASONS`, `BLOCK_CODES`, `FAILURE_CODES`, `STEP_KINDS` | `types` | — |
| `SCHEMA_REASONS` (sub-reasons of `blocked:schema`) | `contracts` | — |
| `CUSTODY_CODES` (a slice of `FAILURE_CODES`) | `custody` | — |

`contracts` **defines** none of the shared vocabularies; the names on both sides
are the same objects, asserted by identity (`assertIs`), not by equality.

---

## 1. `types.py` — W0-TYPES

Config schema and loader, `loop_plan_id`, step receipts, run layout, and the four
closed code tables. Imports `deepreason_core.canonical` and nothing of the loop.

### Constants

```python
CONFIG_SCHEMA = "minireason.loop.config.v1"      # STEP_SCHEMA, PLAN_ID_SCHEMA, STEP_KEY_SCHEMA alongside
LOOPS_ROOT = "experiments/loops"
PINNED_SOURCE_PATHS: tuple[str, ...]             # the 6 fixed repo-relative files folded into loop_plan_id
STOP_REASONS: frozenset[str]                     # 7 + the parameterised preregistered_condition:<id>
PREREGISTERED_CONDITION_PREFIX = "preregistered_condition:"
BLOCK_CODES: frozenset[str]                      # 10: the ceiling's 9 + blocked:constitution
CEILING_BLOCK_REASONS: tuple[str, ...]           # the 9, in the ceiling's order, un-prefixed
BLOCK_CODE_PREFIX = "blocked:"
FAILURE_CODES: frozenset[str]                    # complete for wave 0; scanned by a test
STEP_KINDS: tuple[str, ...]                      # 17: S0..S15 plus AUDIT
REPLAYABLE_STEPS / SPENDING_STEPS: frozenset[str] # disjoint subsets of STEP_KINDS
STEP_STATUSES = ("COMPLETE", "FAILED", "HALTED")
PROVIDER_MODES = ("live", "offline")
```

### Callables and records

```python
is_stop_reason(token: Any) -> bool
is_failure_code(code: Any) -> bool
block_code(reason: str) -> str                                  # "blocked:<reason>"; BLOCK_CODE_UNKNOWN otherwise
loop_plan_id(config: LoopConfig | Mapping[str, Any], pins: Mapping[str, str]) -> str
run_paths(root: Path | str, run_id: str) -> RunPaths            # root is the REPOSITORY root

class LoopError(RuntimeError):  __init__(code: str, detail: str = "")
class SeatsConfig:      from_mapping(raw) -> SeatsConfig; as_dict() -> dict
class ContrastConfig:   from_mapping(raw) -> ContrastConfig; as_dict() -> dict
class AuditConfig:      from_mapping(raw) -> AuditConfig; as_dict() -> dict          # no defaults, by design
class TimeoutsConfig:   from_mapping(raw) -> TimeoutsConfig; as_dict() -> dict       # step_seconds, git_seconds
class LoopConfig:       load(path) -> LoopConfig; from_mapping(raw) -> LoopConfig; as_dict() -> dict; canonical_bytes() -> bytes
class CustodyReport:    from_mapping(raw) -> CustodyReport; from_findings(findings) -> CustodyReport; as_dict() -> dict
class StepReceipt:      key(loop_plan_id, kind, cycle, wave, inputs_sha256) -> str   # @staticmethod
                        build(*, loop_plan_id, index, kind, started_utc, cycle=None, wave=None,
                              inputs_sha256=None, status="COMPLETE", **rest) -> StepReceipt
                        from_dict(raw) -> StepReceipt; as_dict() -> dict
                        .replayable: bool; .filename: str                            # "NNNN-KIND.json"
class CyclePaths:       .import_dir .use_table .readings .contrast .decision .cycle_md; as_dict()
class RunPaths:         .config .preregistration .obligations .ceiling .plan .preflight .lock
                        .steps .graph .cycles .readings .audits .appeals .errata
                        .closing .reading_table .comparison
                        cycle(cycle: int) -> CyclePaths
                        step_path(index: int, kind: str, *, open_marker: bool = False) -> Path
                        reading_dir(row_key: str) -> Path; as_dict()
```

`CustodyReport.from_findings(findings)` (**decision 8**) is the one adapter between
`custody.verify_pins`' `CustodyFinding` objects and the receipt's `checks` tuple.
Import-free: it accepts any object with a `.code`, or a bare string. `verified` is
true exactly when the findings are empty; `checks` keeps **one code per finding**,
in `verify_pins`' order, and does not de-duplicate.

**Exception:** `LoopError(code, detail="")`, `.code`, `.detail`. The code shape
(`^[A-Z][A-Z0-9_]*$`) is enforced; `FAILURE_CODES` membership is **not** enforced
at raise time. Codes raised here: `CONFIG_NOT_A_MAPPING`, `CONFIG_SCHEMA_UNKNOWN`,
`CONFIG_UNKNOWN_KEY`, `CONFIG_MISSING_KEY`, `CONFIG_INVALID_VALUE`, `PIN_INVALID`,
`RUN_ID_INVALID`, `CYCLE_OUT_OF_RANGE`, `STEP_RECEIPT_INVALID`, `STEP_KEY_MISMATCH`,
`BLOCK_CODE_UNKNOWN`.

---

## 2. `standard.py` — W0-STANDARD

The `std:reading-rubric/v1` body, and the owner of every shared vocabulary.

```python
SPEC_ID = "reading-v1";  STANDARD_NAME = "std:reading-rubric/v1"
RUBRIC_EVAL = "rubric:reading-v1";  STANDARD_SCHEMA = "minireason.loop.reading-rubric.v1"
STANDARD_BODY: bytes;  STANDARD_BODY_SHA256: str          # canonical JSON, byte-stable
CEILING_TEXT: str;  CEILING_SHA256: str;  CEILING_PATH: Path
CEILING_CLAIM_TEMPLATE: str                                # clause 1, carries per-cell placeholders
CEILING_REQUIRED_SENTENCES: tuple[str, ...]                # the 11 invariant clauses (W3-REPORT imports this)
CEILING_EXHAUSTION_DENIAL = "not exhaustion of the inquiry"
MODES = ("absolute", "pairwise");  RUBRIC_V1: Mapping[str, RubricClass]
PLAN_8A_MIRROR: Mapping;  PLAN_8A_MIRROR_PATH: Path;  PLAN_8A_REGISTERS: Mapping[str, Register]
FALSIFIER_MAP: Mapping[str, Falsifier]                     # D1, F2, F3; G carries none of them
GUARD_PARAMETERS: Mapping[str, Any];  GUARD_PARAMETER_KEYS: frozenset[str]
REOPEN_REASONS = ("new-material", "repaired-guard", "appellate-ruling")
CALIBRATION_ANCHORS: tuple[CalibrationAnchor, ...]         # 5: 2 that must sustain, 3 clean controls

build_standard(registers=None, vocabulary=None, params=None) -> bytes
standard_body(raw: bytes | str) -> dict[str, Any]
assert_no_exhaustion_claim(text: str, where: str = "record") -> None

class RubricClass:      id mode question body values; as_json()
class DifferenceKind:   token reads plan_grounding; as_json()
class Register:         id name plan_text reads differs_iff difference_kinds carries_falsifiers
                        .kind_tokens: tuple[str, ...]; as_json()
class Falsifier:        id comparison carrying_registers excluded_registers rule exclusion_reason
                        carries(register) -> bool; as_json()
class CalibrationAnchor: id construction expected_relation must_sustain ground_truth_reason; as_json()
```

`DIFFERENCE_KINDS` — the closed per-register token set, **finer than register
grain** as D4 requires:

```
T: target_set_membership, target_prefix_source
E: record_engaged,        engagement_form
D: disposition_value,     disposition_carrier_field
G: grounds_source
```

**Exception:** `StandardInvalid(LoopError, ValueError)` with `(code, detail="")`.
Codes: `SCORING_KEY_FORBIDDEN`, `REGISTER_SET_MISMATCH`, `REGISTER_TEXT_EMPTY`,
`DIFFERENCE_KIND_SET_EMPTY`, `DIFFERENCE_KIND_DUPLICATE`, `VOCABULARY_EMPTY`,
`VOCABULARY_DUPLICATE`, `VOCABULARY_NOT_CLOSED`, `UNRESOLVED_NOT_IN_VOCABULARY`,
`GUARD_PARAMETER_UNKNOWN`, `GUARD_PARAMETER_MISSING`, `GUARD_PARAMETER_INVALID`,
`REOPEN_REASON_SET_EMPTY`, `REOPEN_REASON_UNKNOWN`, `STANDARD_BODY_MALFORMED`,
`STANDARD_SCHEMA_MISMATCH`, `SPEC_ID_MISMATCH`, `STANDARD_SECTION_MISSING`,
`RESOURCE_BOUNDARY_MISDESCRIBED`.

---

## 3. `contracts.py` — W0-CONTRACTS

```python
CONTRACTS_VERSION = "loop.contracts/1"
ROLE_NAMES = ("critic", "defender", "judge", "marker", "variator")   # "decider" is a program
ROLE_BINDING_FIELDS = ("target", "defect", "grounds", "bearing")
ALL_DIFFERENCE_KINDS: tuple[str, ...]           # the 7 tokens, sorted; the marker enum
WORD_LIMITS: Mapping[tuple[str, str], int]      # critic/case 400, defender/answer 400, judge/reading_note 120, marker/case 120
AGGREGATE_KEYS: frozenset[str]                  # schema-name ban, wider than FORBIDDEN_KEYS; NOT applied to artifacts
SCHEMA_REASONS: tuple[str, ...]                 # 18 sub-reasons of blocked:schema
SCORING_KEY_FORBIDDEN = "SCORING_KEY_FORBIDDEN"; SCHEMA_INVALID; CONTRACT_VIOLATION
CRITIC_SCHEMA DEFENDER_SCHEMA JUDGE_SCHEMA MARKER_SCHEMA VARIATOR_SCHEMA; SCHEMAS; VALIDATORS

check(role: str, raw: Any, *, register: str | None = None) -> Validation     # never raises
validate(role: str, raw: Any, *, register: str | None = None) -> RoleOutput  # check + raise
schema_for(role: str) -> dict[str, Any]                                      # deep copy
difference_kinds_for(register: str) -> tuple[str, ...]
assert_no_scoring_keys(value: Any, path: Sequence[str] = ()) -> None         # G12
assert_no_aggregate_fields(schema: Any, path: Sequence[str] = ()) -> None    # schema audit, run at import

class RoleBindings:   target defect grounds bearing; as_dict()
class CriticOutput:   relation passage_quote role_bindings case outside_vocabulary
                      .is_outside_vocabulary .claims_relation; as_dict()
class DefenderOutput: answer concedes; as_dict()
class JudgeRuling:    sustained decisive_point reading_note; as_dict()
class MarkerOutput:   mark difference_kind left_quote right_quote case; .claims_difference; as_dict()
class VariatorOutput: paraphrases; as_dict()
class Validation:     ok role value reason path message; raise_for_failure() -> RoleOutput
```

**Exceptions.** `ContractError(LoopError, ValueError)` with `(code=CONTRACT_VIOLATION,
detail="")` — the argument order every wave-0 exception takes.
`SchemaInvalid(ContractError)` with `(role, reason, message, path=())`; `.code` is
`SCHEMA_INVALID`, `.reason` is a `SCHEMA_REASONS` member, `.path` and `.detail`
carry the location and the message. The **block** code a receipt records for a
`SchemaInvalid` is `blocked:schema`; `.reason` is the sub-reason.
`ScoringKeyForbidden(ContractError)` with `(path=())`; `str(exc)` is exactly
`SCORING_KEY_FORBIDDEN`, so the existing study's `code_of` reads it unchanged.

---

## 4. `custody.py` — W0-CUSTODY

```python
CUSTODY_CODES: tuple[str, ...]        # 9, sorted; a slice of types.FAILURE_CODES
PIN_KEY = "pins";  ALWAYS_SCANNED_ENVS = ("DEEPSEEK_API_KEY", "OLLAMA_API_KEY")
MIN_CREDENTIAL_LENGTH = 8             # == provider_openai_compat._MIN_SECRET_LENGTH

sha256_bytes(raw: bytes) -> str
sha256_path(path: str | Path) -> str                       # byte mode only
encoded(value: Any) -> bytes                               # the RECORD form: indent=2, trailing \n
digest(value: Any) -> str                                  # the IDENTITY form: compact, sorted
scanned_credential_envs() -> tuple[str, ...]               # NAMES only, never a value
credential_names_in(raw: bytes) -> list[str]
fenced(root: str | Path, path: str | Path) -> Path
write_new(path: str | Path, value: Any) -> None            # does NOT fence; pair with fenced()
pins(repo: str | Path, paths: Iterable[str | Path]) -> dict[str, str]     # sorted keys, POSIX
verify_pins(plan: Mapping[str, Any], repo: str | Path) -> list[CustodyFinding]   # reads plan["pins"]

class CustodyFinding: code path expected observed; as_dict() -> dict[str, str | None]
```

**Exceptions.** `CustodyMismatch(LoopError)` with `(code, detail="")`;
`CredentialInOutput(CustodyMismatch, ValueError)`;
`WriteOnceViolation(CustodyMismatch, FileExistsError)`. Codes:
`CREDENTIAL_IN_OUTPUT`, `PATH_ESCAPES_RUN_ROOT`, `PIN_MAP_MISSING`,
`SOURCE_PIN_MALFORMED`, `SOURCE_PIN_MISMATCH`, `SOURCE_PIN_MISSING`,
`SOURCE_PIN_NOT_A_FILE`, `SOURCE_PIN_OUTSIDE_REPOSITORY`, `WRITE_ONCE_VIOLATION`.
`RUNTIME_SOURCE_CHANGED` is the **caller's** aggregate name for a non-empty
`verify_pins` result and is never a per-path finding.

**Digest identity (decision 7), asserted on one shared fixture:**
`custody.digest(v) == provider_openai_compat.digest(v) == sha256_hex(canonical_json(v))`,
and `canonical_json(v)` is byte-identical to the compact `json.dumps` that
`custody.digest` hashes. `custody.encoded` is deliberately a *different* encoding
(the drivers' record form) that round-trips to a value the three digests agree on.

---

## 5. `receipts.py` — W0-RECEIPTS

```python
DEFAULT_REPO_ROOT: Path;  LEDGER_RELATIVE = "docs/DECISION_LEDGER.md"
ACTIVITY_TOOL_RELATIVE = "tools/repo_activity.py";  DEFAULT_LEDGER_PATH: Path
DEFAULT_AGENT = "auto_loop";  STAMP_FORMAT = "%Y-%m-%d %H:%M:%S UTC"
RECEIPT_ID_RE = re.compile(r"REC-(\d{8})-([A-Z]+)")
CADENCE_WARN_SECONDS = 240.0;  CADENCE_DEADLINE_SECONDS = 300.0
ACTIVITY_PHASES = ("begin", "outcome", "event");  C001_PLAN_ID: str
PREREGISTRATION_REQUIRED_SENTENCES: tuple[str, ...]        # 10; section 8's text

utc_stamp(moment=None) -> str
next_letter(existing: Iterable[str]) -> str                # bijective base 26: A..Z, AA, AB, ...
scan_receipt_ids(data: bytes, date_token: str) -> tuple[str, ...]
mint_receipt_id(ledger_path=DEFAULT_LEDGER_PATH, *, today=None) -> str      # advisory on its own
ledger_append(text, ledger_path=DEFAULT_LEDGER_PATH, *, newline=b"\n") -> LedgerAppend
set_current_receipt(receipt_id: str | None) -> None;  current_receipt() -> str | None
open_receipt(*, title, choice, why, contribution, evidence, paths, source_identity,
             state="pending", body, render, form="opened", ledger_path, moment,
             set_current=True) -> str                       # mints and appends under ONE lock
outcome_receipt(receipt_id, outcome, evidence=None, *, form="outcome", paths, ledger_path, moment) -> LedgerAppend
checkpoint_receipt(receipt_id, progress, evidence=None, *, cadence, next_action, ledger_path, moment) -> LedgerAppend
close_receipt(receipt_id, outcome, evidence=None, *, state_from="pending", ledger_path, moment) -> LedgerAppend
erratum_receipt(receipt_id, defect, correction, evidence=None, *, form="erratum", ledger_path, moment) -> LedgerAppend
render_preregistration(receipt_id, stamp, *, loop_plan_id=None, run_id=None, source_identity=None) -> str
open_preregistration(ledger_path=DEFAULT_LEDGER_PATH, *, loop_plan_id, run_id, source_identity, moment) -> str
activity(phase, action, why, goal, paths=None, *, decision=None, agent=DEFAULT_AGENT,
         repo_root=DEFAULT_REPO_ROOT, runner=subprocess.run, timeout=30.0, check=True) -> tuple[str, ...]
bracket(action, why, goal, paths=None, **kwargs)            # contextmanager: begin / outcome

class LedgerAppend: path text receipt_id offset written sha256; .end
class CadenceCheck: now since elapsed_seconds deadline_utc state overdue_seconds; .due .missed
class CadenceMiss:  deadline_utc recorded_utc overdue_seconds; sentence() -> str
class Cadence(started: datetime, *, warn_seconds, deadline_seconds, ledger_path)
      .since .deadline .misses
      check(now: datetime) -> CadenceCheck                  # tz-AWARE datetime, from the harness clock
      acknowledge(moment: datetime) -> None                 # refuses to move backwards
      record_checkpoint(now, receipt_id, progress, evidence=None, *, next_action=None) -> LedgerAppend
```

**Exceptions.** `ReceiptError(LoopError)` with `(code, detail="")`;
`SecretInReceipt(ReceiptError)` with `(names, where)`, `.names` holding environment
variable NAMES and never a value. Codes: `SECRET_IN_RECEIPT`,
`LEDGER_EMPTY_PARAGRAPH`, `LEDGER_INCOMPLETE_WRITE`, `LEDGER_APPEND_NOT_VERIFIED`,
`RECEIPT_ID_MALFORMED`, `RECEIPT_SUFFIX_MALFORMED`, `RECEIPT_FORM_MALFORMED`,
`RECEIPT_BODY_AMBIGUOUS`, `RECEIPT_FIELDS_MISSING`, `PREREGISTRATION_SENTENCE_MISSING`,
`ACTIVITY_PHASE_UNKNOWN`, `ACTIVITY_DECISION_MISSING`, `ACTIVITY_TOOL_MISSING`,
`ACTIVITY_LOGGER_FAILED`, `ACTIVITY_RAW_COMMAND_TEXT`, `ACTIVITY_CONTROL_CHARACTER`,
`CADENCE_BACKDATED`, `CADENCE_THRESHOLDS_INVERTED`, `MOMENT_NOT_AWARE`,
`MOMENT_NOT_DATETIME`.

---

## 6. `publish.py` — W0-PUBLISH

```python
VERIFIED_LINE = "VERIFIED {commit} TREE {tree} at {utc} local={local} remote={remote} ref={ref} paths={paths}"
PUBLISHED = "PUBLISHED";  PENDING = "PENDING"
PENDING_REASONS = (PUSH_REJECTED, PUSH_TIMEOUT, PUSH_TRANSPORT, REMOTE_NOT_CONFIRMED, PATH_NOT_PUBLISHED)
PUSH_BACKOFF_SECONDS = (2.0, 4.0, 8.0, 16.0);  MAX_PUBLISH_ATTEMPTS = 3;  GIT_TIMEOUT_SECONDS = 90.0
REWRITING_SUBCOMMANDS / REWRITING_FLAGS: frozenset[str]

publish(repo, paths, message, ref=None, *, attempt=1, git=None, sleep=None, now=None) -> PublishResult
verify_published(repo, paths, commit, ref=None, *, git=None) -> bool
check_published(repo, path_or_sha, ref=None, *, git=None) -> bool   # publication-before-dispatch predicate
upstream_ref(repo, *, git=None) -> str
split_publish_ref(ref: str) -> tuple[str, str]                     # "origin/x" -> ("origin","refs/heads/x")

class GitOutcome:     code stdout stderr timed_out args; .ok; text(); summary()
class LocalGit(repo, *, timeout=GIT_TIMEOUT_SECONDS, env=None)
      environment() -> dict[str, str]                              # every credential removed
      status(*tokens) -> GitOutcome;  run(*tokens) -> bytes;  text(*tokens) -> str
class PublishPending: reason attempt ref local_commit remote_commit detail
class PublishResult:  status ref paths files attempt committed local_commit remote_commit
                      tree verified_line pending; .published .distinct_remote_commit; as_receipt()
```

**Exceptions.** `PublishError(LoopError)` with `(code, detail="")`;
`GitCommandFailed` (`GIT_OPERATION_FAILED`), `HistoryRewriteRefused`
(`HISTORY_REWRITE_REFUSED`), `CredentialInStagedDiff` (`SECRET_IN_STAGED_DIFF`),
`PublishNotConverging` (`PUBLISH_NOT_CONVERGING`) — each `(detail="")`. Other codes:
`PUBLISH_REF_UNRESOLVED`, `PUBLISH_REF_INVALID`, `PUBLISH_PATHS_EMPTY`,
`PUBLISH_PATHS_UNTRACKED`, `PUBLISH_MESSAGE_EMPTY`, `PUBLISH_ATTEMPT_INVALID`,
`UNEXPECTED_STAGED_FILES`, `REPO_NOT_A_GIT_CHECKOUT`, `CHECK_TARGET_UNKNOWN`,
`PATH_NOT_EXPLICIT`, `PATH_IS_REPO_ROOT`, `PATH_OUTSIDE_REPO`, `PATH_MISSING`.

`publish()` **returns** the VERIFIED line and writes nothing to the ledger, and
shells no activity logger: the driver wires `publish` to `receipts`.

---

## 7. Conventions, restated

They are also in the package docstring (`src/minireason/loop/__init__.py`), which
imports nothing and is safe to read first.

* Open step marker: `steps/NNNN-KIND.json.open`, via
  `RunPaths.step_path(i, kind, open_marker=True)`.
* `run_paths(root, run_id)` takes the **repository root**; the run tree is
  `<root>/experiments/loops/<run_id>`.
* `StepLedger(run_root, loop_plan_id)` takes the **run root** (`RunPaths.run_root`).
* `Cadence.check(now)` takes a **tz-aware** datetime from the harness clock.
* `publish()` returns the VERIFIED line; `receipts` owns the ledger.
* `write_new` does **not** fence; pair it with `fenced(run_root, relative)`.
* `loop_plan_id` refuses a null, non-hex, absolute or `..`-bearing pin (`PIN_INVALID`).
  Pin *order* does not affect the identity; a declared config value does.
* The provider wall clock is the endpoint's `timeout_seconds` off the frozen plan,
  never a config key; disagreement is `TIMEOUT_NOT_APPLIED`.
* The credential floor is 8 bytes; a bearing record is **refused, not redacted**.
* Every wave-0 exception is a `types.LoopError` and keeps its original base.

---

## 8. Open questions the six authors flagged, with a recommendation

Nine were closed by the integration decisions (owner of the vocabularies; the
`DIFFERENCE_KINDS` divergence; `FORBIDDEN_KEYS` duplication; the ceiling ↔
`BLOCK_CODES` reconciliation; the exhaustion-scan exemption; the exception
hierarchy; the code tables; `CustodyReport.from_findings`; the `.open` spelling).
These remain.

**O1 — `LoopConfig.graph_root` vs `RunPaths.graph`. Two names for the harness root.**
`types.RunPaths.graph` is `<run_root>/graph`; `LoopConfig.graph_root` is a
repo-relative path the operator declares, and the docstring says it "overrides"
the property. Nothing enforces that they agree, and `graph_root` is inside
`loop_plan_id` while `RunPaths.graph` is not. *Recommendation (W1-GRAPH):* treat
`config.graph_root` as authoritative and resolve it as `repo_root / graph_root`;
make `RunPaths.graph` the **default** written into the config at PREREGISTER, and
add a PREFLIGHT check that `repo_root / config.graph_root == RunPaths.graph` unless
the operator declared otherwise, recording which.

**O2 — the vendored warrant's `verdict` field collides with G12's `FORBIDDEN_KEYS`.**
Design D2 gives the reading warrant `verdict: "fail"`; `verdict` is a member of
`tools/contrast_triple_study.FORBIDDEN_KEYS`, which `standard.FORBIDDEN_KEYS`
mirrors and may not narrow without weakening every other study that shares the
set. Neither wave-0 author flagged this; the integrator found it and pinned it with
`tests/loop/test_contracts.py::test_the_guard_refuses_the_vendored_warrants_own_verdict_field_name`.
*Recommendation (W1-GRAPH):* keep both. G12's subject is "every emitted artifact,
every table header and every rendered file" — the artifact **content** the loop
builds. Run `assert_no_scoring_keys` over artifact content only, never over the
vendored `Warrant`/`Commitment` records, and say so in W1-GRAPH's docstring. Do not
edit the vendored ontology (that is vendoring drift) and do not narrow the key set.

**O3 — `receipts.DEFAULT_REPO_ROOT` is `Path(__file__).parents[3]`.**
Correct in a source checkout, wrong in an installed wheel, where `parents[3]` is
`site-packages`' parent and carries no `tools/repo_activity.py`. *Recommendation
(W1-STEPS / the driver):* always pass `repo_root=` explicitly to `activity()` and
`ledger_path=` explicitly to every receipt call, from the run's own resolved repo
root; leave the defaults as the convenience they are and never rely on them in the
driver. A PREFLIGHT assertion that `ACTIVITY_TOOL_RELATIVE` exists under the
resolved root would turn the failure into a named refusal.

**O4 — two "required sentence" tables, two owners.**
`standard.CEILING_REQUIRED_SENTENCES` (11, the claim ceiling, §6) and
`receipts.PREREGISTRATION_REQUIRED_SENTENCES` (10, the ledger receipt, §8). They
are different documents and both are correct, but a renderer that confuses them
will assert the wrong set. *Recommendation (W3-REPORT):* import the ceiling set
from `standard`, never from `receipts`; the pre-registration set is asserted by
`render_preregistration` against its own output and needs no second consumer.

**O5 — `CEILING_CLAIM_TEMPLATE` carries four unfilled placeholders.**
`digest …`, relation *r*, paraphrase count *N*, audit record *A*. It is
deliberately not a verbatim-required sentence. *Recommendation (W3-REPORT):* give
it a typed fill function in W3 (not in wave 0), assert that the filled clause
contains no remaining `…`/`*r*`/`*N*`/`*A*`, and keep the eleven invariant clauses
byte-verbatim beside it.

**O6 — `verify_pins` requires `plan["pins"]`, and pins for files outside the repo.**
`custody.verify_pins` refuses a bare `{path: sha}` map with `PIN_MAP_MISSING` (by
design), and `pins()` refuses a path outside the repository tree — but the design's
pin list includes the transport module, which may resolve through `PYTHONPATH` from
outside. *Recommendation (W1-STEPS):* write `plan.json` with a top-level `pins`
key; for any pinned file outside the tree, hash it with `custody.sha256_path` and
merge it into the map under a stable synthetic key, exactly as
`contrast_triple_study.check_transport_pins` already does, and record in the plan
that the key is synthetic.

**O7 — `MAX_PUBLISH_ATTEMPTS` is carried by the caller, not by `publish()`.**
`publish(..., attempt=n)` raises `PublishNotConverging` at the third attempt, but
nothing persists `n` across steps. *Recommendation (W1-STEPS):* keep the attempt
count in the step ledger, keyed by the publication's `step_key`, and pass it in; a
`PublishPending` result must block every successor step until a later attempt
returns `PUBLISHED`.

**O8 — `_refuse_credentials` reads and decodes every file under the named paths.**
Linear in the size of the published tree on every publish step, and it can only see
credentials present in *this process's* environment. *Recommendation:* accept the
cost (it is the point), but W1-STEPS should publish at step grain rather than
re-publishing the whole run tree, and the closing record should state that the scan
covers the credentials this process could see — not a proof that no credential is
present.

**O9 — `LoopError` does not enforce `FAILURE_CODES` membership at raise time.**
Deliberate: later waves own codes wave 0 cannot enumerate. The table is complete
for wave 0 and a test keeps it so. *Recommendation:* every later wave adds its own
codes to `types.FAILURE_CODES` in the same commit that raises them; the scan in
`tests/loop/test_types.py::TheCodeTablesAreComplete` extends by adding the new
exception class to `TOKEN_ARGUMENT`, and it names the module and the token when it
fails.

**O10 — `G` has a single `difference_kind`, so kind grain = register grain there.**
PLAN §8a gives G one axis whose values already include "none", so inventing a
second token would not be mirroring. *Recommendation:* leave it. If a later
pre-registration needs a finer G, that is a successor standard and a new
`loop_plan_id`, never an edit — and `DIFFERENCE_KINDS`' shape (register → closed
tuple) already admits it without changing any caller.

**O11 — `contracts.check(role, raw, register=None)` falls back to the union.**
Called without `register`, a marker's `difference_kind` is checked against all
seven tokens rather than that register's own. *Recommendation (W2-MARKPREP):*
always pass `register=`; the union fallback exists only for a caller that genuinely
does not know which register was asked, and no marker call is ever in that
position.

---

## 9. Carried to later waves

Appended by the wave-0 review fix pass (`REVIEW-WAVE0.md`). Four of that review's
notes are **not** wave-0 defects: nothing in wave 0 renders a record, builds a
distribution or spends a step's wall clock, so each one becomes an obligation on
the wave that first does. They are recorded here because W3-REPORT and W5 read
this file and will not read the review.

**N1 — the block register must print counts with no denominator and no rate
(W3-REPORT).** Ceiling clause 7 (`data/ceiling_v1.md`) promises the block register
"is printed with counts on every table" and states no denominator and no anchor,
which R9 requires of any rate. A renderer must print **per-code counts** and never
a computed rate, a percentage or a fraction: ruling 7 and FW5:851 make a count
information and never an automatic warrant, and a rate over an unstated
denominator is a meter. *W3 test:* the rendered block register contains no `/`,
no `%` and no float; `standard.assert_no_scoring_headers` is run over the rendered
file (it is the other half of G12 and W3 is its first caller).

**N5 — one publish step can exceed the 300 s cadence deadline by construction
(W1-STEPS / W5).** `publish.PUSH_BACKOFF_SECONDS` sums to 30 s and each of up to
five push attempts carries `GIT_TIMEOUT_SECONDS = 90`, so a single publish step
can burn 5x90 + 30 s against `receipts.CADENCE_DEADLINE_SECONDS = 300.0`. That is
not a bug in either module — the git wall clock is §4.4 layer 3 and the cadence is
AGENTS.md's five-minute rule — but the driver must expect it: a publish step needs
a `Cadence.check` **before** it starts and a checkpoint receipt written on the way
in, or the deadline is missed by a step that is behaving correctly. `CadenceMiss`
already records the miss honestly and never backdates it; the point is to not be
surprised.

**N7 — no test asserts the two data files ship in a built distribution
(W6-DOC / packaging).** `tests/loop/test_standard.py` checks the source tree only.
`pyproject.toml` declares the `package-data` entry, and it is unverified: a wheel
built without `src/minireason/loop/data/*` imports `standard` and dies at import,
because the module reads both files at import time. The review could not build a
wheel in the staging container (setuptools 68.1.2 against the declared `>=75`;
Debian's `install_layout`). *Obligation:* whoever first builds or installs a wheel
asserts that `CEILING_PATH` and `PLAN_8A_MIRROR_PATH` exist **inside the built
distribution**, not just in the tree.

**N9 — `assert_no_exhaustion_claim` must be called on a generated record
(W3-REPORT).** Design §4.4 promises "a test asserts [the token *exhaustion*] never
appears in a generated record". Wave 0 asserts it of the closed vocabularies and of
`types.py`'s own source, which is all wave 0 can assert: it generates no record.
W3-REPORT generates the first ones (`CLOSING.md`, `READING_TABLE.md`, `CYCLE.md`,
the audit record) and must call `standard.assert_no_exhaustion_claim` on each
before it is written. The scan now normalises whitespace and case (wave-0 review
S5), so a re-wrapped or sentence-cased ceiling denial passes and only a claim is
refused.

**Where the wave-0 interface itself moved.** Sections 1-8 above describe wave 0 as
integrated. The review fix pass changed several of those signatures and behaviours
(the §2.3 schemas moved to `standard`, `AuditConfig` gained two required account
fields, `assert_no_scoring_keys` refuses a rendered file, `LocalGit` refuses every
subcommand it does not itself emit, `verify_published` compares committed trees,
`ledger_append` takes `create=`). The fix pass's own report is the record of every
one of them; this file is not rewritten, by instruction.
