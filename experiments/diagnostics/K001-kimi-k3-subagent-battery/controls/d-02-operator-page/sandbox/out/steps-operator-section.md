## The step ledger (`src/minireason/loop/steps.py`)

One run's `<run_root>/steps/` directory, read and written through one object.
`StepLedger` derives every transition's identity — its `step_key` — from the frozen
plan, writes exactly one **write-once** receipt when a step ends, and refuses to
start a successor while anything is unresolved. Resume is simply `run` again
against the same run root: the ledger replays what is on disk, skips what already
carries a `COMPLETE` receipt, re-runs and re-checks what is replayable, and halts
on anything it cannot account for.

`step_key = sha256(canonical(loop_plan_id, kind, cycle, wave, inputs_sha256))`
(`steps.py:840-845`, `types.py:1092-1110`). Two runs of the same frozen plan over
the same inputs produce the same key, which is what makes "already done" a fact
about the record rather than a guess. A receipt written under a different
`loop_plan_id` is `PLAN_ID_MISMATCH` and the run does not resume
(`steps.py:730`, `781-783`).

### Driving it

This module publishes objects, not a command. The driver holds the run lock,
then runs steps through the ledger:

```python
lock = RunLock(ledger.paths.lock, loop_plan_id).acquire()   # steps.py:417-503
ledger = StepLedger(run_root, loop_plan_id, timeouts=cfg.timeouts,
                    ledger_path=..., receipt_id=...)        # steps.py:733-753
ledger.run_step(kind, cycle, inputs, fn, wave=...)          # steps.py:1029-1052
ledger.publish_step(kind, repo, paths, message, ref=...)    # steps.py:1054-1108
ledger.acknowledge(step_key, reason)                        # steps.py:1135-1172
```

`StepLedger(run_root, ...)` takes the **run root** —
`run_paths(repo_root, run_id).run_root` — never the repository root and never
`steps/` itself (`steps.py:724-731`). `timeouts.step_seconds` is a per-kind
mapping; a kind absent from it has no step deadline
(`steps.py:1024`, `types.py:779`).

### What a run's `steps/` directory holds

The spelling of every name below comes from `types.RunPaths`
(`types.py:1262-1294`, `1313-1321`) and nowhere else; the ledger asks
`RunPaths.step_path(index, kind, open_marker=...)` for it so that
`NNNN-KIND.json[.open]` has exactly one spelling in the package.

```
experiments/loops/<RUN-ID>/
  run.lock                          RunPaths.lock — one driver per run
  steps/NNNN-KIND.json              the write-once step receipt
  steps/NNNN-KIND.json.open         the open marker of a spending step
  steps/NNNN-KIND.verified          a publication's VERIFIED line, verbatim
  errata/NNNN-KIND-HALT.md          the erratum stub a halt writes
  errata/ACK-NNNN-<step_key>.json   the acknowledgement that clears a halt
```

**The open marker is `steps/NNNN-KIND.json.open`** — the design's layout block at
4.2, not the `.open.json` of its 4.3 prose. Wave 0 settled this in its conventions
section ("Open step marker: `steps/NNNN-KIND.json.open`, via
`RunPaths.step_path(i, kind, open_marker=True)`",
`notes/WAVE0-INTERFACE.md:357-358`, restated at
`src/minireason/loop/__init__.py:69-72`), and `types.py:1320` builds exactly that
name. `NNNN` is the step index, zero-padded to four, `0000`–`9999`
(`types.py:1316-1320`).

A receipt carries `schema`, `step_key`, `index`, `kind`, `cycle`, `wave`,
`loop_plan_id`, `inputs_sha256`, `outputs_sha256`, `spending`, `started_utc`,
`finished_utc`, `status`, `custody`, `failure_code` and `published_commit`, and
nothing else — the schema is closed and a receipt with an unknown key is refused
(`types.py:1128-1134`). `status` is one of `COMPLETE`, `FAILED`, `HALTED`
(`types.py:429`); `PENDING` is not among them, which is why a pending publication
is recorded the way described below. There is no free-text field in a receipt: a
publication's `VERIFIED` line therefore lands in three places that must agree —
the sidecar bytes, the receipt's `outputs_sha256["verified_line"]` digest, and,
when `ledger_path` is wired, `docs/DECISION_LEDGER.md`
(`steps.py:1098-1106`, `187-190`).

`custody.verified` **defaults to `false`** (`types.py:964`). A receipt whose
driver ran no custody check says so rather than implying one. The only way a
check that did run reaches the receipt is
`StepHandle.record_custody(findings)` → `CustodyReport.from_findings`
(`steps.py:608-612`).

An open marker carries `schema` (`minireason.loop.step-open.v1`), `step_key`,
`index`, `kind`, `cycle`, `wave`, `inputs_sha256`, `started_utc` and
`spending: true` (`steps.py:1180-1190`). It is written **before** the step body
runs (`steps.py:1025-1026`).

### Replayable, spending, and neither

The classification is a closed table in `types.py`, not a caller's opinion
(`types.py:410-427`). Seventeen step kinds fall into three classes; the counts
below came from
`python3 -c "from minireason.loop import types; print(sorted(types.SPENDING_STEPS), sorted(types.REPLAYABLE_STEPS))"`.

* **Replayable** — 5 kinds: `PREFLIGHT`, `IMPORT`, `USE_TABLE`, `ADJUDICATE`,
  `DECIDE`. Offline, deterministic, pure. On resume the step is **re-run** and its
  named outputs must digest to what the existing receipt recorded; a difference is
  `STEP_NONDETERMINISTIC` and is filed as its own receipt beside the record it
  failed to reproduce (`steps.py:1226-1251`). This is a live check, not a
  formality. For a killed run this class costs nothing but time: nothing was
  spent, so everything is simply done again.
* **Spending** — 8 kinds: `SEND`, `READ`, `MARK`, `AUDIT`, and all four
  publications `PUBLISH_PLAN`, `PUBLISH_IN`, `PUBLISH_EV`, `PUBLISH_CY`. A call
  may have been billed or a remote may have moved. An `.open` marker is written
  before the step and removed only by an outcome that says what happened
  (`steps.py:1193-1204`). For a killed run this is the whole point: if the driver
  died between the marker and the receipt, **the step body is never re-entered**
  on resume — the ledger halts with `UNRESOLVED_STEP` and waits for a person.
* **Neither** — 4 kinds: `PREREGISTER`, `CYCLE_OPEN`, `PREPARE`, `CLOSE`. A
  `COMPLETE` receipt is skipped on resume and nothing is replayed
  (`steps.py:33-34`, `1042-1046`).

A marker is resolved by an outcome that says what happened. A stable code
(`HTTP_429`, a custody halt, `PUBLISH_PENDING`) does; the two members of
`MARKER_KEPT_CODES` — `STEP_TIMEOUT` and `STEP_BODY_FAILED` — do not, because
neither tells anyone whether a call was billed, so their markers survive
deliberately (`steps.py:168-170`, `1198-1199`).

Inside `SEND`, `READ`, `MARK` and `AUDIT`, resumption is at **coordinate** grain.
`scan_coordinates(out_dir)` reads `requests/`, `attempts/` and `responses/` under
a reading tree and returns three frozensets: `complete` (a response is on record —
terminal, skipped), `indeterminate` (a request or attempt but no response) and
`started` (`steps.py:340-367`). A coordinate in `indeterminate` refuses re-send
and is reported `INDETERMINATE`, **never as an absence**. The function only reads;
it writes nothing anywhere (`steps.py:358-360`).

### Every refusal this module can raise, and what the operator does next

All of them are `types.LoopError` subclasses, so `except LoopError` catches every
refusal in the package, and each carries `.code` and `.detail`
(`steps.py:203-207`). The detail is truncated to 400 characters
(`steps.py:195`, `207`).

| Code | Raised at | Operator action | Refused until then |
|---|---|---|---|
| `UNRESOLVED_STEP` | `steps.py:978`, out of `guard()`; `UnresolvedStep` also carries `.step_key`, `.index`, `.kind` | Read the marker body and the run's `readings/…` tree for that coordinate; decide by hand whether a call was billed. Then `acknowledge(step_key, reason)` with what was found. The body is not re-entered on your behalf | Every step. `begin()` calls `guard()` before it opens anything (`steps.py:1013`), so no step starts |
| a custody halt code (17 of them, listed below) | `steps.py:988`, as `StickyHalt`, re-raising **the halted receipt's own code** rather than a second name for it | Read `errata/NNNN-KIND-HALT.md`, settle the custody question at its source (re-pin, re-publish the input, restore the moved file), then `acknowledge(step_key, reason)` | Every step. A halt is sticky; only an acknowledgement clears it (`steps.py:931-937`) |
| `PUBLISH_PENDING` | `steps.py:985` out of `guard()` as `PublishBlocked`; also written as a `FAILED` receipt at `steps.py:1094` | Fix what the push is waiting on (network, rejected ref, unconfirmed remote), then call `publish_step` again on the **same** `step_key` | Every successor step. `guard(step_key)` lets the next attempt of that same publication through and nothing else (`steps.py:982-984`) |
| `STEP_TIMEOUT` | `steps.py:637`, from `StepHandle.check_deadline()`; also checked once more at completion (`steps.py:649`) | Treat it as a **resource boundary**, not as a finished inquiry: raise `timeouts.step_seconds` for that kind, or reduce what the step is asked to cover, and resume. On a spending step, first clear the marker it deliberately left — see `UNRESOLVED_STEP` | Nothing directly; but on a spending step the surviving marker refuses every successor at the next `guard()` |
| `STEP_NONDETERMINISTIC` | `steps.py:1246`; `.differing` names the output keys that disagree | Find why a pure step moved — an unpinned input, an unfrozen clock, a set iteration order — and fix that. Re-running will not settle it | Nothing is blocked by the code itself; the failed replay is recorded at a fresh index and offered as `RETRY` |
| `STEP_BODY_FAILED` | Recorded, not raised: `_classify` (`steps.py:717`) files it when a body raised something with no stable `.code`, and the original exception is re-raised unchanged | Read the traceback the driver logged, name the real defect, and give the failing dependency a stable code so the next occurrence is not anonymous | On a spending step the marker survives (`MARKER_KEPT_CODES`), so the next `guard()` refuses every step with `UNRESOLVED_STEP` |
| `RUN_LOCKED` | `steps.py:464`, from `RunLock.acquire()` | See "`run.lock`" below: find the other driver by the pid in the refusal and stop it, or wait for it | This driver never starts |
| `PLAN_ID_MISMATCH` | `steps.py:471-474` (the lock was opened under another plan) and `steps.py:782-783` (a receipt in `steps/` was written under another plan) | The config or a pin changed, so this is a different plan. Start a new run id; do not resume into someone else's ledger. If the change was unintended, restore the frozen config and pins | `records()`, and therefore every resume and every step |
| `STEP_CLASS_DISAGREEMENT` | `steps.py:1008-1010` (an explicit `spending=` flag contradicting `SPENDING_STEPS`) and `steps.py:1073-1074` (`publish_step` called with a kind outside `PUBLICATION_STEPS`) | A caller bug, refused before a call number is spent. Drop the explicit flag — `spending=None` means "take it from the table" — or call `run_step` instead of `publish_step` | That step only; nothing is written |
| `STEP_RECEIPT_INVALID` | `steps.py:1005` (unknown kind), `645`/`683` (a handle ended twice), `779` (unreadable JSON in `steps/`), `785` (a receipt disagreeing with its own filename) | For a caller bug, fix the call. For a file: the receipt on disk has been edited or truncated. **Do not edit it back** — quarantine the run, record an erratum, and start a new run id | `records()` raises, so the whole resume stops |
| `STEP_NOT_HALTED` | `steps.py:1147` (empty reason) and `steps.py:1150` (nothing unresolved under that key) | Give a non-empty reason; or check the `step_key` — `resume_plan()`/`blocking()` print the key of the thing that is actually blocking | The acknowledgement only |
| `STEP_OUTPUTS_INVALID` | `steps.py:308`/`312`, from `_digest_map` over `inputs` or `outputs` | Pass a mapping of non-empty string names to digestible values. A failure receipt is never blocked by the outputs that failed (`steps.py:685-688`), but a `COMPLETE` is | That step's completion |
| `MOMENT_NOT_DATETIME`, `MOMENT_NOT_AWARE` | `steps.py:279` and `steps.py:281`, from `_stamp` | Feed the ledger a timezone-aware `datetime` from the harness clock. A naive moment has no UTC meaning and is refused rather than assumed | Any receipt, marker, acknowledgement or lock write that needs a stamp |

The seventeen sticky-halt codes are `CUSTODY_HALT_CODES` (`steps.py:174-183`):
every member of `custody.CUSTODY_CODES` — `CREDENTIAL_IN_OUTPUT`,
`PATH_ESCAPES_RUN_ROOT`, `PIN_MAP_MISSING`, `SOURCE_PIN_MALFORMED`,
`SOURCE_PIN_MISMATCH`, `SOURCE_PIN_MISSING`, `SOURCE_PIN_NOT_A_FILE`,
`SOURCE_PIN_OUTSIDE_REPOSITORY`, `WRITE_ONCE_VIOLATION` — plus
`CUSTODY_MISMATCH`, `REQUEST_NOT_FROM_PLAN`,
`ARTIFACT_NOT_DERIVED_FROM_DELIVERY`, `TIMEOUT_NOT_APPLIED`,
`PROVIDER_REQUEST_FILE_CHANGED`, `TRANSPORT_PIN_MISMATCH`,
`RUNTIME_SOURCE_CHANGED` and `INPUT_NOT_PUBLISHED`. The count and the membership
were read off the module with
`python3 -c "from minireason.loop import steps; print(len(steps.CUSTODY_HALT_CODES)); print(sorted(steps.CUSTODY_HALT_CODES))"`,
which prints `17`. Any of these reaching a step body — raised, or passed to
`StepHandle.fail(code)` — is recorded `HALTED` rather than `FAILED`
(`steps.py:665`, `709-717`).

Three further codes reach the operator **through** this module rather than from
it, on writes the ledger makes through `custody.fenced` / `custody.write_new`
(`steps.py:1100`, `1168-1170`, `1177-1180`, `1217-1219`, `1262-1268`):
`WRITE_ONCE_VIOLATION` (the path already exists — named in `acknowledge`'s own
docstring at `steps.py:1141`, where a second acknowledgement of one halt is
exactly this), `CREDENTIAL_IN_OUTPUT` (the bytes carry a live credential; the
write is **refused, not redacted**, and leaves no file behind) and
`PATH_ESCAPES_RUN_ROOT` (a path resolving outside the run root). All three are
also members of `CUSTODY_HALT_CODES`, so a body that lets one through halts.
Operator action for the first: nothing was overwritten — that is the guarantee —
so find out why the same record was written twice. For the second: the record was
never created; remove the credential from what the step was about to file, never
from the record after the fact. For the third: the step tried to write outside its
own run; fix the caller.

A code not in these tables is a code this module does not raise. An operator page
that listed one would be describing an instrument that does not exist.

### The halt-and-acknowledge rule

The loop never works around custody. A halt writes its receipt (`HALTED`, with
the custody code in `failure_code`), an erratum stub
`errata/NNNN-KIND-HALT.md`, and — when `ledger_path` and `receipt_id` are wired —
an erratum receipt into the decision ledger (`steps.py:1206-1224`, `1255-1280`).
The erratum's prose is built from the receipt's own stable fields and says, in
fixed words, that "this step registered nothing and its successors were refused"
(`steps.py:376-394`). It carries no count, no score and no claim about the
material: a halt is a fact about the instrument.

**A halt is sticky.** It survives the process. `resume_plan()` reports it as
`HALT` with the detail "a custody halt is sticky until it is acknowledged"
(`steps.py:931-937`), and `guard()` re-raises the receipt's own code on every
subsequent attempt to start anything. The earliest unresolved thing is what
blocks: actions are sorted by index with halting entries first, so a custody halt
at step 3 outranks a stale marker at step 9 (`steps.py:893-899`, `955`).

**An acknowledgement records a reason, and happens once.**
`acknowledge(step_key, reason)` refuses an empty reason (`STEP_NOT_HALTED`,
`steps.py:1145-1147`) and refuses a key with nothing unresolved under it
(`steps.py:1148-1151`). What it writes is itself a write-once record under
`errata/ACK-NNNN-<step_key>.json` carrying `schema`, `step_key`, `index`,
`failure_code`, `reason`, `acknowledged_utc` and the `erratum` narrative — which
ends with the operator's own words: *"Acknowledged by the operator, who gave this
reason: …"* (`steps.py:1159-1170`, `391-393`). Because the record is write-once, a
second acknowledgement of the same halt is `WRITE_ONCE_VIOLATION`; a later,
*different* halt on the same key is a different record and is not covered by the
first (`steps.py:1140-1143`).

The design's CLI spelling for this is
`--acknowledge <step_key> --reason "<text>"` (design 4.2, 4.4). An acknowledged
`.open` marker is **left on disk** — it is the record of what happened — and the
resume plan skips it from then on (`steps.py:907-920`); the retried step takes a
fresh index (`steps.py:833-838`).

### What a `PENDING` publication blocks

`publish()` can come back not-published, carrying a reason from its own
`publish.PENDING_REASONS` vocabulary; the ledger reads it off the result and
falls back to `REMOTE_NOT_CONFIRMED` when the pending object names none
(`steps.py:1092-1093`). Those reasons belong to W0-PUBLISH and are not step
failure codes. `PENDING` is not a member of `types.STEP_STATUSES`, so
`publish_step` records it as a **`FAILED` receipt carrying `PUBLISH_PENDING`**
and, unusually for this module, **returns** rather than raising: pending is a
retryable state of the publication, not an end state of the run
(`steps.py:55-61`, `1091-1096`).

It blocks **every successor step**. `pending_publication()` finds it
(`steps.py:866-877`), `resume_plan()` reports it as `HALT` with
"a pending publication blocks every successor step" (`steps.py:939-943`), and
`guard(step_key)` refuses every step except a further attempt on that same
publication's key (`steps.py:982-987`). The attempt count is kept in the ledger
itself, keyed by `step_key` (`attempts_for`, `steps.py:860-864`), and passed to
`publish()` as `attempt=`, so `publish.MAX_PUBLISH_ATTEMPTS` is enforced across driver
restarts and not only within one process. Each attempt is its own step at its own
index — a **new publish step**, never a retry and never a force-push. When an
attempt finally lands, the `VERIFIED` line is written to
`steps/NNNN-KIND.verified`, its digest into the receipt, and its text into the
ledger, and the block lifts (`steps.py:1098-1108`).

### `run.lock`, and what a second driver sees

The five-per-credential ceiling is a process-wide registry inside
`provider_openai_compat`, so it holds only inside one process. A second driver on
the same run would be a second process and a second set of slots, so it is refused
(`steps.py:417-426`). `RunLock(path, loop_plan_id)` takes
`RunPaths.lock` = `<run_root>/run.lock` and locks it with
`flock(LOCK_EX | LOCK_NB)` — on Windows, `msvcrt.locking(LK_NBLCK)`
(`steps.py:401-414`).

A second driver sees `RunLocked`, code `RUN_LOCKED`, with a detail naming the run
lock's path and the holder read out of the file itself, in the shape
`<path>/run.lock: held by pid <pid> since <started_utc>` (`steps.py:464-466`).
Operator action:
identify that pid; if it is alive, wait or stop it deliberately. **A stale file
can never wedge a run** — exclusion is the kernel's, released when the holder
dies, so the file's contents (`schema`, `pid`, `started_utc`, `loop_plan_id`) are
for the human reading the refusal and are re-written on every acquire, not
write-once (`steps.py:71-74`, `454-487`).

If the lock file names a *different* `loop_plan_id`, acquiring it is
`PLAN_ID_MISMATCH` instead (`steps.py:468-474`): the lock is released and closed
first, so a refusal never leaves the run locked.

### Where this section follows the module rather than the design

Where the two disagree, the module is what runs, and this page describes the
module.

1. **The marker's name.** Design 4.3's prose says `.open.json`; its own 4.2 layout
   block says `steps/NNNN-KIND.json[.open]`. `types.RunPaths.step_path`
   (`types.py:1320`) builds the layout block's spelling, and wave 0 recorded that
   choice (`notes/WAVE0-INTERFACE.md:357-358`).
2. **A marker is not always resolved by the receipt.** 4.3 says "resolved by the
   receipt"; 4.4 says a step timeout "leaves the open marker and therefore halts
   on resume — deliberately". The module holds both by resolving a marker only on
   an outcome that says what happened, and keeping it for `STEP_TIMEOUT` and
   `STEP_BODY_FAILED` (`steps.py:47-54`, `170`).
3. **`PENDING` is a `FAILED` receipt carrying `PUBLISH_PENDING`, and is returned,
   not raised** (`steps.py:55-61`) — because `PENDING` is not a member of
   `STEP_STATUSES` (`types.py:429`).
4. **`run_step`'s `spending` parameter defaults to `None`, not `False`.** The wave
   plan publishes `spending=False`; the module takes `None` to mean "read it off
   `SPENDING_STEPS`" and asserts an explicit flag against that table
   (`steps.py:39-46`, `1006-1010`). Every call written against the published
   signature behaves exactly as published.
5. **The halting set is wider than 4.4's sentence.** 4.4 names six codes plus
   "any `CustodyError`"; `CUSTODY_HALT_CODES` resolves that to seventeen, adding
   `CUSTODY_MISMATCH`, `RUNTIME_SOURCE_CHANGED` and `INPUT_NOT_PUBLISHED`
   (`steps.py:174-183`).
6. **The `VERIFIED` line is not stored in the receipt.** The receipt schema is
   closed and has no free-text field, so the line goes to a write-once sidecar and
   the receipt keeps its digest under `outputs_sha256["verified_line"]`
   (`steps.py:62-66`).

### What this section does not promise

* **It decides nothing and reads no material.** The ledger records transitions.
  No verdict, no warrant, no label is minted here, and nothing in a receipt or an
  erratum ranks a run, an arm, a model family or an endpoint against another.
* **It does not run a custody check.** It records one that a step body ran, through
  `record_custody` and no other route; `custody.verified` stays `false` otherwise
  (`steps.py:67-70`, `608-612`).
* **It does not pre-empt a step body.** Nothing portable can. A long body must poll
  `handle.check_deadline()`; completion checks once more, so a step that overran is
  *recorded* as having overrun even when its body returned — but a body that never
  polls and never returns is not stopped by this module (`steps.py:624-630`).
* **It does not retry anything.** A further publication attempt is a new step at a
  new index, counted in the ledger. There is no back-off loop here and no
  force-push anywhere.
* **It does not take the run lock for you.** `StepLedger` never acquires
  `RunLock`; `guard()` does not consult `run.lock`. A driver that skips
  `RunLock.acquire()` gets no exclusion at all.
* **It does not cover a cross-machine run.** `flock` is one kernel's. The lock is
  advisory across runs and mandatory on the same run on one machine, and this page
  claims nothing beyond that (design 4.6 says the same).
* **It does not validate a code against `types.FAILURE_CODES` at raise time.**
  That is deliberate (wave-0 open question O9): later waves own codes wave 0 could
  not enumerate. As of this module,
  `python3 -c "from minireason.loop import steps, types; print(sorted(set(steps.NEW_CODES) - set(types.FAILURE_CODES)))"`
  prints all five of `RUN_LOCKED`, `STEP_BODY_FAILED`,
  `STEP_CLASS_DISAGREEMENT`, `STEP_NOT_HALTED`, `STEP_OUTPUTS_INVALID` — they are
  raised but not yet folded into the table, which
  `notes/WAVE1-INTEGRATION-DECISIONS.md` item 6 requires.
* **It does not guarantee a receipt for every started step.** A named output that
  is not JSON-serialisable escapes `complete()` as a bare `TypeError` from
  `custody.digest` (`steps.py:301` → `custody.py:269`), and `complete()` is called
  outside `run_step`'s `except` (`steps.py:1047-1052`), so no receipt is written.
  On a spending step this leaves the `.open` marker alone on disk and the next
  `guard()` refuses with `UNRESOLVED_STEP`. Digest every output to `bytes`, a
  `Path`, a 64-character hex digest or plain JSON data (`steps.py:286-301`).
* **`scan_coordinates` reports `INDETERMINATE`, and never an absence.** A
  coordinate with a request or attempt but no response is not "not asked". The
  function only reads; the decision about such a coordinate is the operator's and
  the reader's, not this module's.
* **A timeout, a call budget and a closed connection are resource boundaries.**
  A `STEP_TIMEOUT` receipt says a declared limit was reached, and never that an
  inquiry was exhausted. `unresolved` stays a first-class outcome throughout.
