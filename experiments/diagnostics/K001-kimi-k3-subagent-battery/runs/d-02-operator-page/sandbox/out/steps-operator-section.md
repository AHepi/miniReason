# W1-STEPS — the step ledger (`src/minireason/loop/steps.py`)

## What the step ledger is

A step's identity is its `step_key` — `sha256` over the canonical form of
`(loop_plan_id, kind, cycle, wave, inputs_sha256)`, recomputed from a receipt's own
fields every time the receipt is read, so no receipt can lie about what step it
records. Every transition writes exactly one write-once receipt under
`<run>/steps/`: an existing path is a custody refusal (`WRITE_ONCE_VIOLATION`),
never an overwrite, so the directory is the run's complete history of what was
attempted and what came of it. Resume is the driver run again on the same run
root: the ledger replays its own directory, skips completed steps, re-runs
replayable ones, and refuses to start anything while an open marker, an
unacknowledged halt, or a pending publication is on record — the *earliest*
unresolved thing blocks (`resume_plan`, steps.py:893).

The module decides nothing about the material under study. It reads no
material, issues no verdict, and never works around custody: a refusal here is
a refusal, recorded as a receipt carrying its code and then re-raised. The only
state that ever clears a halt is an operator's acknowledgement, which is itself
a write-once record naming a reason.

## Invocation

This section is written against the module; the design of record is sections
4.3 and 4.4 of `design/design-s4-driver.md`. The operator command is the
driver's (`python tools/auto_loop.py run --config <path>`, design 4.2); the
CLI lands on this module, and the module's entry points are:

```python
from minireason.loop.types import run_paths
from minireason.loop.steps import StepLedger, RunLock

paths  = run_paths(repo_root, run_id)                 # root is the REPOSITORY root
lock   = RunLock(paths.lock, loop_plan_id).acquire()  # one driver per run (4.6)
ledger = StepLedger(paths.run_root, loop_plan_id)     # run root, NOT repo root
out    = ledger.run_step("USE_TABLE", cycle=1, inputs={...}, fn=fn)
pub    = ledger.publish_step("PUBLISH_IN", repo, paths, message, cycle=1)
```

`paths` spellings come only from `types.RunPaths`; the module derives them and
never retypes them, so `NNNN-KIND.json[.open]` has exactly one spelling in the
package (the wave-0 convention, `notes/WAVE0-INTERFACE.md` §7). Two
configuration surfaces reach this module: `timeouts.step_seconds` (per step
kind; a kind absent from the mapping has no step deadline) and the step
classification tables in `types`, both frozen into `loop_plan_id` — changing
either after a run has begun is a new plan and a new run, not an edit.

`run_step` returns a `StepOutcome` whose `status` is one of `COMPLETE`,
`FAILED`, `HALTED` (the three receipt statuses) or `SKIPPED` / `REPLAYED` (no
new receipt; `outcome.ran` is false only for `SKIPPED`). Every exception this
module raises is a `types.LoopError` carrying `.code` and `.detail`, so
`except LoopError` catches every refusal in the package. Details are truncated
at 400 characters (`_DETAIL_LIMIT`, steps.py:195).

## The record layout on disk

A run lives under `<repo>/experiments/loops/<RUN-ID>/` (`types.LOOPS_ROOT`);
`StepLedger`'s first argument is that run root. Everything this module writes
is fenced inside it (`custody.fenced`):

```
experiments/loops/<RUN-ID>/
  run.lock                            one JSON record, rewritten on every acquire
  steps/0001-PREFLIGHT.json           a step receipt, schema minireason.loop.step.v1
  steps/0006-SEND.json.open           an open marker, spending steps only
  steps/0002-PUBLISH_PLAN.verified    the VERIFIED sidecar, publication steps only
  errata/0006-SEND-HALT.md            the erratum stub a halt writes
  errata/ACK-0006-<step_key>.json     one acknowledgement record, write-once
```

The open-marker spelling is `steps/NNNN-KIND.json.open` — `.open` appended to
the full receipt filename, from `types.RunPaths.step_path(index, kind,
open_marker=True)` (types.py:1313) and `notes/WAVE0-INTERFACE.md` §7. Design
4.3's prose spells the same marker `.open.json`; the module and the design's
own layout block (4.2) agree on `.json.open`, and this page follows the
module.

A **receipt** (`steps/NNNN-KIND.json`, write-once) carries:

```json
{"schema":"minireason.loop.step.v1","step_key":"<64 hex>","index":12,
 "kind":"SEND","cycle":2,"wave":null,"loop_plan_id":"<64 hex>",
 "inputs_sha256":{},"outputs_sha256":{},"spending":true,
 "started_utc":"...Z","finished_utc":"...Z","status":"COMPLETE|FAILED|HALTED",
 "custody":{"verified":true,"checks":[]},"failure_code":null,
 "published_commit":null}
```

A `COMPLETE` receipt carries `failure_code: null`; a `FAILED` or `HALTED`
receipt must name one — `types.StepReceipt` refuses to load either mismatch.
The receipt has **no detail field**: a detail lives on the raised exception and,
for a halt, in the `errata/` stub. A receipt validates itself on load — its
`step_key` is recomputed from its own bytes and its `spending` flag must equal
the closed classification of its kind — so a receipt that disagrees with the
rule it was written under cannot be read at all.

An **open marker** (`steps/NNNN-KIND.json.open`, schema
`minireason.loop.step-open.v1`, steps.py:150) is written *before* a spending
step runs and carries its `step_key`, `index`, `kind`, `cycle`, `wave`,
`inputs_sha256`, `started_utc` and `spending: true`. An **acknowledgement**
(schema `minireason.loop.step-acknowledgement.v1`) carries the `step_key`,
`index`, the `failure_code` it clears, the operator's `reason`, the
`acknowledged_utc` stamp and an `erratum` narrative. `run.lock` (schema
`minireason.loop.run-lock.v1`) carries `pid`, `started_utc` and
`loop_plan_id`, and is written for the human reading a refusal, not as a
record — see the lock section.

## The three step classes, and what a kill means for each

The classification is a closed table in `types` (`REPLAYABLE_STEPS`,
`SPENDING_STEPS`, types.py:418 / 424); a receipt's `spending` flag is checked
against it on every load.

* **Replayable** — `PREFLIGHT`, `IMPORT`, `USE_TABLE`, `ADJUDICATE`, `DECIDE`:
  offline, deterministic, pure. On resume a replayable step with a `COMPLETE`
  receipt is **re-run**, and its fresh output digests must equal what the
  receipt recorded or `STEP_NONDETERMINISTIC` is raised — a live check, not a
  formality. A kill mid-step leaves nothing on disk; the step simply re-runs.
* **Spending** — `SEND`, `READ`, `MARK`, `AUDIT` and the four publication
  steps (`PUBLISH_PLAN`, `PUBLISH_IN`, `PUBLISH_EV`, `PUBLISH_CY`): a call may
  have been billed, or a remote may have moved. The `.open` marker is written
  before the step and removed when the receipt records an outcome that says
  what happened. A kill between marker and receipt leaves the marker; on
  resume that is `UNRESOLVED_STEP` and the step body is **never re-entered**.
* **Everything else** — `PREREGISTER`, `CYCLE_OPEN`, `PREPARE`, `CLOSE`: a
  `COMPLETE` receipt means skip on resume; nothing is replayed and no marker
  is ever written, so a kill mid-step just runs the step again.

`SEND`, `READ`, `MARK` and `AUDIT` resume at **coordinate grain** (design
4.3): within a re-entered step, per-coordinate write-once
request/attempt/response records make resumption safe;
`scan_coordinates(out_dir)` reports a coordinate with a request or attempt but
no response as `INDETERMINATE` — **never as an absence** — and re-sending it
is refused (`completed_coordinates` returns only the answered set;
steps.py:347 / 372).

What resume plans for one recorded step, in index order (`RESUME_ACTIONS`,
steps.py:160):

```
SKIP    COMPLETE receipt, not replayable: pass over it
REPLAY  COMPLETE receipt, replayable kind: re-run, assert identical digests
RETRY   FAILED receipt, latest for its key, marker resolved: re-run the step
HALT    marker unacknowledged, sticky halt, or PENDING publication: refuse
```

## The halt-and-acknowledge rule

A custody halt is **sticky**: a step whose receipt is `HALTED` blocks every
successor step on every resume until the operator acknowledges that exact
halt. The loop never works around custody. When a halt is recorded the module
writes the receipt, removes the marker if the code says what happened, writes
an erratum stub `errata/NNNN-KIND-HALT.md` (prose over the receipt's stable
fields — no count, no score, no claim about the material: a halt is a fact
about the instrument), and appends an erratum receipt to the decision ledger
when one is wired in.

Resuming past the halt requires the acknowledgement, recorded:

```python
ledger.acknowledge(step_key, reason)   # the CLI lands here:
# run --acknowledge <step_key> --reason "<text>"   (design 4.2 / 4.4)
```

`acknowledge()` requires a non-empty reason and an actually-unresolved halt at
that key, writes the write-once record
`errata/ACK-NNNN-<step_key>.json`, and appends the acknowledgement narrative
("Acknowledged by the operator, who gave this reason: …") to the ledger. Three
consequences the operator should know, all read off the module
(steps.py:1135–1174):

* The acknowledgement records the reason verbatim; the module checks only
  that it is non-empty, not that it is true.
* The record is write-once: a second acknowledgement of the *same* halt (same
  step_key and index) is refused as `WRITE_ONCE_VIOLATION`. A later,
  *different* halt on the same key is a different record and needs its own
  acknowledgement.
* The ledger erratum append runs **after** the ACK file is written. If the
  ledger append refuses (for instance `SECRET_IN_RECEIPT`, because the reason
  text carried a credential value visible to the process), the halt is already
  acknowledged on disk — do not retry the acknowledgement; fix the ledger
  condition, then resume.

Once acknowledged at `(step_key, index)`, the resume plan no longer emits the
`HALT` action for it and the run proceeds past that step.

## Publication and `PUBLISH_PENDING`

`publish_step` runs `publish.publish` for a publication kind and files the
`VERIFIED` line three ways: verbatim in the write-once sidecar
`steps/NNNN-KIND.verified`, as a sha256 under
`outputs_sha256["verified_line"]` in the receipt, and as a ledger line when a
ledger is wired (design 4.5's "into both the ledger and the step receipt",
with the bytes kept where the receipt can name them).

A `PENDING` result is **returned, not raised**: it is recorded as a `FAILED`
receipt carrying `PUBLISH_PENDING`, and the guard then blocks **every
successor step** — any `begin`/`run_step` for a different `step_key` raises
`PublishBlocked` (code `PUBLISH_PENDING`, steps.py:252) — until a later
attempt on the same `step_key` returns `PUBLISHED`. The next attempt of the
same publication is the one call the guard lets through (design O7). The
attempt count is reconstructed from the ledger itself (`attempts_for` counts
the publication receipts on that key), and three non-converging attempts halt:
`publish` raises `PUBLISH_NOT_CONVERGING` at a fourth (`MAX_PUBLISH_ATTEMPTS`,
publish.py:176). The pending *reason* — one of the five `PENDING_REASONS` in
publish.py:162 — rides on the returned `StepOutcome.value.pending.reason`; the
receipt itself names only `PUBLISH_PENDING`, so a driver that exits without
naming the reason leaves the code as the on-disk record.

## `run.lock`: one driver per run

The per-credential concurrency gate holds only inside one process (design
4.6), so a second driver on the same run — a second process with its own
slots — is refused, not shared. `RunLock(paths.lock, loop_plan_id).acquire()`
takes the kernel's exclusive non-blocking `flock` on the run's `run.lock` and
holds it for the driver's lifetime; the kernel releases it when the holder
dies, so a stale lock file can never wedge a run — **there is no stale-lock
state and no operator action is ever "delete run.lock"**. A second driver on
the same run sees `RunLocked` (code `RUN_LOCKED`) whose detail names the
holder from the file's contents: `held by pid <pid> since <started_utc>`. The
exception is `PLAN_ID_MISMATCH`: if the lock file on disk was opened under a
different `loop_plan_id`, even the would-be holder is refused — the run
directory belongs to a different frozen plan. Exclusion is mandatory on one
run, advisory across runs, and per design 4.6 nothing here covers drivers on
two machines.

## Failure and refusal codes, with the operator action for each

Every code below is one the module can raise or record, read off
`src/minireason/loop/steps.py`; pass-through codes are named as such. A code
on a receipt never mints a warrant: `FAILED` receipts carry the deliverer
module's stable code, and a provider failure ends a coordinate or an arm, it
never produces a semantic result. A timeout deadline is a declared resource
boundary (`timeouts.step_seconds`), never a claim about the inquiry.

The module's own codes. The five newest are declared on `steps.NEW_CODES`
(steps.py:141) with the reason for each; wave-1 integration decision 6 binds
them into `types.FAILURE_CODES`, and in the tree this page was written against
they are not yet there (`is_failure_code` does not know them).

| Code | What it means on disk | Operator action; what is refused until then |
|---|---|---|
| `UNRESOLVED_STEP` (steps.py:210) | An `.open` marker survived a kill: a call may have been billed or a remote moved. No receipt exists for the spend. | Determine what the spend did — the coordinate-grain records under `readings/`, the remote ref state — then acknowledge the step_key with a reason, or leave the run halted. **Refused until then: every step of the run** (the guard raises before any `begin`), and the step body is never re-entered. |
| `STEP_TIMEOUT` (steps.py:231) | The step exceeded `timeouts.step_seconds[kind]`. Receipt `FAILED` carrying the code; on a spending step the marker is deliberately kept (`MARKER_KEPT_CODES`) because a timeout does not say whether a call was billed. | On a spending kind, resume sees `UNRESOLVED_STEP`: determine what the spend did, then acknowledge, or leave it. Widening the deadline is a config change and mints a new `loop_plan_id` — a new run, not an edit. |
| `STEP_BODY_FAILED` (`NEW_CODES`) | A step body raised something carrying no stable code; the receipt names the absence rather than inventing one. On a spending step the marker is kept. | The detail (`str(exc)`) is on the re-raised exception, not the receipt — capture the driver's output. Then as for `STEP_TIMEOUT`: spending kind ⇒ acknowledge to resume, fixing the defect first. **Refused until then: the whole run, via the marker.** |
| `STEP_NONDETERMINISTIC` (steps.py:221) | A replayable step re-ran and produced different output digests; the exception's `.differing` names the outputs and the mismatch is filed as its own `FAILED` receipt beside the record it failed to reproduce. | A live check found real nondeterminism in a step declared pure. Do not edit or delete either receipt. Find the differing outputs, fix the body (or rebuild the run). Nothing is permanently blocked — the step re-fails at the same place on each resume until fixed. |
| `PUBLISH_PENDING` | A publication attempt did not confirm the remote. `FAILED` receipt; marker resolved (the outcome says what happened). | See the publication section: re-run the driver's publish step for the same step key; the guard blocks **every other step** until an attempt returns `PUBLISHED`. After `PUBLISH_NOT_CONVERGING` (third failure) no fourth attempt exists in this module — reconcile the remote manually per the pending reason. |
| `RUN_LOCKED` (`NEW_CODES`) | A live second driver holds this run's `run.lock`. | Find the holder named in the detail. If that driver is genuinely finished, its death released the lock and a retry succeeds; never delete the file. **Refused until then: acquiring this run at all.** |
| `STEP_CLASS_DISAGREEMENT` (`NEW_CODES`) | A caller passed `spending=` or a publication `kind` that disagrees with the closed classification tables. Raised in `begin`/`publish_step` before any write. | Fix the caller to match the tables (or pass nothing and let the table decide). Nothing was written; nothing else is refused. |
| `STEP_OUTPUTS_INVALID` (`NEW_CODES`) | A body's returned outputs (or a caller's inputs) are not a mapping of names to digestible values. | Fix the body to return a mapping of string names. On inputs the step never opened (no marker, no receipt); on outputs a `FAILED` receipt is already on record and the step simply retries on resume. |
| `STEP_NOT_HALTED` (`NEW_CODES`) | `acknowledge()` was given an empty reason, or a step_key with nothing unresolved. | Give a real reason, and point at the step_key that the halt detail named. To find it: the `errata/NNNN-KIND-HALT.md` filename and the exception detail both carry the key. |
| `STEP_RECEIPT_INVALID` (steps.py:203 via many checks) | A receipt on disk fails to load or disagrees with its own filename/index/kind; or `begin` was given an unknown step kind; or one handle was completed twice (a driver defect). | A receipt the module cannot read is evidence, not an obstacle: preserve the file, never hand-edit it. The ledger refuses every resume while the file stands; the run tree is finished as an instrument and any continuation is a new run. For the caller-error forms, fix the caller — nothing was written. |
| `PLAN_ID_MISMATCH` (steps.py:472, 782) | A receipt (or the lock file) was written under a different `loop_plan_id`: the frozen plan changed beneath a live run directory, or the wrong run root was opened. | Confirm the run root. If the plan really changed, that is a new run under a new `loop_plan_id`; the old tree stays untouched. **Refused: reading the directory at all — `records()` raises before anything else.** |
| `MOMENT_NOT_DATETIME` / `MOMENT_NOT_AWARE` (steps.py:279–281) | A clock handed to the ledger produced something that is not a tz-aware datetime. | A wiring defect in the driver's clock injection; fix it to supply aware datetimes. No record is ever stamped from a bad moment. |

Sticky custody halts — receipt status `HALTED`, cleared only by
`acknowledge()`. `CUSTODY_HALT_CODES` (steps.py:174) is the nine members of
`custody.CUSTODY_CODES` joined with eight delivery- and publication-custody
codes; the count and membership are read off that line:

`CREDENTIAL_IN_OUTPUT`, `PATH_ESCAPES_RUN_ROOT`, `PIN_MAP_MISSING`,
`SOURCE_PIN_MALFORMED`, `SOURCE_PIN_MISMATCH`, `SOURCE_PIN_MISSING`,
`SOURCE_PIN_NOT_A_FILE`, `SOURCE_PIN_OUTSIDE_REPOSITORY`,
`WRITE_ONCE_VIOLATION`, plus `CUSTODY_MISMATCH` (also the fallback code a
sticky halt surfaces under when a halted receipt somehow names none,
steps.py:988), `REQUEST_NOT_FROM_PLAN`,
`ARTIFACT_NOT_DERIVED_FROM_DELIVERY`, `TIMEOUT_NOT_APPLIED`,
`PROVIDER_REQUEST_FILE_CHANGED`, `TRANSPORT_PIN_MISMATCH`,
`RUNTIME_SOURCE_CHANGED`, `INPUT_NOT_PUBLISHED`.

Operator actions by cluster:

* **Pin codes** (`SOURCE_PIN_*`, `PIN_MAP_MISSING`, `TRANSPORT_PIN_MISMATCH`,
  `RUNTIME_SOURCE_CHANGED`): a file the frozen plan pins moved, vanished, or
  was never a file. Restore the pinned bytes and acknowledge — or accept that
  the plan no longer holds and start a new run. The halt receipt's
  `custody.checks` and the `errata/` stub name each finding, one code per
  finding, never collapsed.
* **Write codes** (`WRITE_ONCE_VIOLATION`, `CREDENTIAL_IN_OUTPUT`,
  `PATH_ESCAPES_RUN_ROOT`): a write this module attempted through
  `custody.write_new`/`fenced` was refused — the path already exists (this is
  also what a second acknowledgement of one halt raises), or the bytes carry a
  live credential (record carries the environment variable **name**, never the
  value; rotate the credential and clean the source text), or the path would
  escape the run root. Nothing was written. If a receipt path itself
  collides, the directory already contains the record you were about to
  duplicate — read it; that is the answer.
* **Delivery custody** (`REQUEST_NOT_FROM_PLAN`,
  `ARTIFACT_NOT_DERIVED_FROM_DELIVERY`, `PROVIDER_REQUEST_FILE_CHANGED`,
  `TIMEOUT_NOT_APPLIED`, `CUSTODY_MISMATCH`): the bytes sent disagreed with
  the bytes planned, or the endpoint's wall clock disagreed with the frozen
  plan's `timeout_seconds`. The step never registered anything and its
  successors were refused. Inspect the stub, repair the instrument, then
  acknowledge to resume or close the run.
* **`INPUT_NOT_PUBLISHED`**: dispatch was attempted against an input not on
  the remote. The fix is upstream: get the publication step to `PUBLISHED`,
  then acknowledge.

Pass-through codes: the receipts this module files. `run_step` and
`publish_step` record whatever a body raised under its own stable code and
re-raise it (`_classify`, steps.py:709): any `custody.CustodyMismatch` is
`HALTED`; any other `LoopError` is `HALTED` if its code is in the set above
and `FAILED` otherwise, with the code carried unchanged; anything that is not
a `LoopError` is `FAILED` with `STEP_BODY_FAILED`. Consequently the receipt
may name codes this module does not own. The families an operator will
actually meet:

* **Provider / delivery codes** (`HTTP_429`, `KEY_MISSING`,
  `TRANSPORT_OR_RESPONSE_ERROR`, `SECRET_IN_REQUEST`, and runner v2's) arrive
  from the step body's own machinery. A `FAILED` receipt on a spending step
  with one of these resolves the marker — the outcome says what happened — so
  resume plans `RETRY` for that step. These are documented fully on the
  transport's operator page (`docs/workflows/provider-openai-compat.md`); this
  ledger only carries the code through.
* **Publication codes** (`GIT_OPERATION_FAILED`, `PUBLISH_REF_UNRESOLVED`,
  `PUBLISH_REF_INVALID`, `PUBLISH_PATHS_EMPTY`, `PUBLISH_PATHS_UNTRACKED`,
  `PUBLISH_MESSAGE_EMPTY`, `UNEXPECTED_STAGED_FILES`,
  `REPO_NOT_A_GIT_CHECKOUT`, `CHECK_TARGET_UNKNOWN`, `PATH_NOT_EXPLICIT`,
  `PATH_IS_REPO_ROOT`, `PATH_OUTSIDE_REPO`, `PATH_MISSING`,
  `HISTORY_REWRITE_REFUSED`, `GIT_SUBCOMMAND_NOT_ALLOWED`,
  `SECRET_IN_STAGED_DIFF`, `PUBLISH_NOT_CONVERGING`, `PUBLISH_ATTEMPT_INVALID`)
  are publish.py's, raised out of `publish_step` and recorded as `FAILED`
  receipts with the marker resolved; the step retries on resume. The
  ref/path/staging codes are operator-fixable (fix the ref, the paths, or the
  checkout state and rerun). `HISTORY_REWRITE_REFUSED` and
  `GIT_SUBCOMMAND_NOT_ALLOWED` are never retry-worthy — they name what the
  publish design forbids. `PUBLISH_NOT_CONVERGING` means a fourth attempt was
  requested; reconcile the remote by hand. `SECRET_IN_STAGED_DIFF` means the
  staged diff carried a credential that therefore never reached the remote;
  rotate it and clean the content.
* **Ledger-wiring codes** (`SECRET_IN_RECEIPT`, `LEDGER_NOT_FOUND`,
  `LEDGER_EMPTY_PARAGRAPH`, `LEDGER_INCOMPLETE_WRITE`,
  `LEDGER_APPEND_NOT_VERIFIED`, `RECEIPT_ID_MALFORMED`,
  `RECEIPT_FORM_MALFORMED`) are receipts.py's, reachable when
  `ledger_path`/`receipt_id` are wired. Fix the wiring: pass the run's own
  ledger path explicitly (O3), keep credential values out of every text bound
  for the ledger. Two recorded states make the failure mode non-obvious: a
  ledger refusal *inside* `publish_step` happens after the remote confirmed
  but before the receipt is written, so the marker stays open and resume sees
  `UNRESOLVED_STEP` even though the remote holds the commit — reconcile the
  remote manually, fix the ledger condition, then acknowledge; and a ledger
  refusal while *recording a halt's erratum* happens after the halt receipt is
  on disk, so the run is genuinely halted and the acknowledgement flow applies
  once the wiring is fixed.
* **Read-time codes from receipt validation** (`STEP_KEY_MISMATCH`,
  `CONFIG_NOT_A_MAPPING`): raised by `types.StepReceipt` while the ledger
  loads the directory — a receipt file whose key does not recompute from its
  own bytes, or a file that parses as JSON but is not an object. Same action
  as `STEP_RECEIPT_INVALID` on read: preserve, never hand-edit, the run cannot
  be resumed by this ledger.

## What this module does not promise

* **No judgement.** It reads no material and decides nothing; a
  `COMPLETE` receipt is a record that a step ran, never a claim about any
  material under study, and no code here is a semantic result.
* **No pre-emption.** The step deadline is cooperative: a body polls
  `check_deadline()`, and completion checks it once more, so an overrun is
  always *recorded* but a running body is never killed (steps.py:624).
* **No silent retry of a spend.** A step whose outcome does not say what
  happened (`STEP_TIMEOUT`, `STEP_BODY_FAILED`, a bare kill) is never
  re-entered; only operator acknowledgement moves past it. Steps whose
  recorded outcome does say what happened retry on resume, and coordinate
  grain inside `SEND`/`READ`/`MARK`/`AUDIT` resumes each already-terminal
  coordinate as terminal.
* **No custody workaround.** There is no override flag, no force path, and no
  redaction-on-write path for a refusal; a refusal is a receipt plus a raise.
* **No cross-machine exclusion.** `run.lock` is the kernel's `flock` on one
  filesystem; design 4.6 says so and the module inherits the limit.
* **No guarantee the detail survives.** `detail` rides the exception and the
  `errata/` stub, not the receipt; pending reasons ride the returned outcome.
  A driver that swallows either loses it, and the receipt still tells the
  truth — by code.
* **No truth check on an acknowledgement.** The reason is recorded verbatim;
  the record proves an operator acknowledged and said why, not that the why
  was sound.
* **No protection of records it does not own.** The ledger's write-once
  guarantee covers `steps/`, `errata/` and its own sidecars; the lock file is
  deliberately *not* write-once (it is rewritten on every acquire), and
  nothing here reads or guards occurrence trees.

## Where this page follows the module over the design text

The module's docstring records its deviations; where the two disagree this
page states the module's behaviour:

* **Marker spelling**: design 4.3's prose says `.open.json`; the module and
  design 4.2's layout block agree on `.json.open`, and that spelling is used
  throughout.
* **`run_step`'s `spending` parameter defaults to `None`**, meaning *take the
  classification from the closed table*, not the wave plan's `False`; an
  explicit flag that disagrees is `STEP_CLASS_DISAGREEMENT`. Calls written
  against the published `spending=False` signature behave exactly as
  published.
* **The marker survives exactly two outcomes** — `STEP_TIMEOUT` and
  `STEP_BODY_FAILED` (`MARKER_KEPT_CODES`) — reconciling 4.3 ("resolved by
  the receipt") with 4.4 (a timeout "leaves the open marker and therefore
  halts on resume — deliberately"): a marker is resolved by an outcome that
  says what happened; a stable provider code and a custody halt both do, a
  timeout and an unclassified crash do not.
* **`PENDING` is not a receipt status**: it is recorded as `FAILED` with
  `PUBLISH_PENDING` and *returned* by `publish_step`, with the guard blocking
  every successor step (design O7) until a later attempt on the same key lands
  `PUBLISHED`.
* **The `VERIFIED` line lives in a `.verified` sidecar** with its sha256 in
  the receipt and its text in the ledger — three places that must agree — and
  `custody.verified` on a receipt whose driver ran no custody check records
  `false` rather than claiming a check.
* **`run.lock` is rewritten, not write-once-written**: it is a mutual
  exclusion re-taken on every resume, and its bytes are for the human reading
  a `RUN_LOCKED` detail.
* **`scan_coordinates` gained beside `completed_coordinates`**: 4.3 requires
  a coordinate with a request or attempt but no response to be reported
  `INDETERMINATE` and never as an absence, which the completed set alone
  cannot express.
