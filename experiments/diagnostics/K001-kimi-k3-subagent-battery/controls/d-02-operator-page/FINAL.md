# W1-STEPS operator section — delivered

Written to `out/steps-operator-section.md` inside the sandbox (340 lines). It is a
`##`-level section for `docs/workflows/automated-loop.md`, shaped after the house
exemplar `docs/workflows/provider-openai-compat.md`: what the thing is, how it is
driven, the record layout on disk, every refusal by code with the operator action
for each, and what it does not promise.

## What the section carries

* **Three sentences on the ledger**: `step_key` derived from the frozen plan,
  exactly one write-once receipt per transition, and resume as "`run` again —
  replay the ledger, skip `COMPLETE`, re-run what is replayable, halt on anything
  unaccounted for."
* **The on-disk layout** of `steps/` and the errata it writes, every name taken
  from `types.RunPaths` (`types.py:1262-1294`, `1313-1321`). The open-marker
  spelling is **`steps/NNNN-KIND.json.open`** — the design's 4.2 layout block,
  built by `RunPaths.step_path(index, kind, open_marker=True)` at `types.py:1320`,
  and settled as a convention at `notes/WAVE0-INTERFACE.md:357-358` and
  `src/minireason/loop/__init__.py:69-72`. The design's 4.3 *prose* says
  `.open.json`; the page says the module follows the layout block.
* **Replayable / spending / neither**, with what each means for a killed run:
  5 replayable kinds (re-run, digests must match, nothing was spent), 8 spending
  kinds (marker before the body; a marker that survived a kill means the body is
  **never re-entered** and the ledger halts `UNRESOLVED_STEP`), 4 kinds that are
  neither. Counts read off the module with
  `python3 -c "from minireason.loop import types; print(sorted(types.SPENDING_STEPS), sorted(types.REPLAYABLE_STEPS))"`.
  Also the coordinate-grain rule: `scan_coordinates` reports a request-or-attempt
  without a response as `INDETERMINATE`, never as an absence, and writes nothing.
* **Every failure code the module can raise**, in a four-column table (code /
  where it is raised / what the operator does next / what is refused until they
  do it): `UNRESOLVED_STEP`, the 17-member sticky-halt family, `PUBLISH_PENDING`,
  `STEP_TIMEOUT`, `STEP_NONDETERMINISTIC`, `STEP_BODY_FAILED`, `RUN_LOCKED`,
  `PLAN_ID_MISMATCH`, `STEP_CLASS_DISAGREEMENT`, `STEP_RECEIPT_INVALID`,
  `STEP_NOT_HALTED`, `STEP_OUTPUTS_INVALID`, `MOMENT_NOT_DATETIME`,
  `MOMENT_NOT_AWARE`; then, separately, the three that arrive *through* the module
  on writes it makes via `custody.write_new` / `custody.fenced` —
  `WRITE_ONCE_VIOLATION`, `CREDENTIAL_IN_OUTPUT`, `PATH_ESCAPES_RUN_ROOT`.
* **Halt and acknowledge**: a halt writes a `HALTED` receipt, an erratum stub
  `errata/NNNN-KIND-HALT.md`, and a ledger erratum when wired; it is **sticky**
  across processes and only an acknowledgement clears it; the acknowledgement is
  itself write-once at `errata/ACK-NNNN-<step_key>.json` and **records a reason**,
  which is refused if empty (`STEP_NOT_HALTED`) and appears in the erratum
  narrative. A second acknowledgement of the same halt is `WRITE_ONCE_VIOLATION`.
* **What `PublishPending` blocks**: every successor step, until a later attempt on
  the *same* `step_key` lands; `guard(step_key)` lets that one attempt through and
  nothing else. The attempt count lives in the ledger (`attempts_for`), so the
  publish attempt ceiling survives driver restarts.
* **`RunLock`**: a second driver on the same run sees `RunLocked` / `RUN_LOCKED`
  with the holder's pid and start time read out of `run.lock`; a different
  `loop_plan_id` in that file is `PLAN_ID_MISMATCH` instead, and the lock is
  released before the refusal. Exclusion is `flock(LOCK_EX | LOCK_NB)`, so a stale
  file cannot wedge a run.
* **What it does not promise**: it decides nothing and reads no material; it does
  not run a custody check (`custody.verified` defaults to `false`); it does not
  pre-empt a body; it does not retry; it does not take the run lock for you
  (`StepLedger` never acquires `RunLock` and `guard()` never consults it); it does
  not cover a cross-machine run; it does not enforce `FAILURE_CODES` membership;
  and it does not guarantee a receipt for every started step (see the finding
  below). Plus the house line: a step timeout is a **resource boundary**, never an
  exhausted inquiry.

## Where the module and the design disagree, as the page says

Recorded in the page as its own subsection, module-first in each case: the marker
spelling (4.2 layout block over 4.3 prose); a marker resolved only by an outcome
that says what happened, so `MARKER_KEPT_CODES` = {`STEP_TIMEOUT`,
`STEP_BODY_FAILED`} survive (reconciling 4.3's "resolved by the receipt" with
4.4's "leaves the open marker … deliberately"); `PENDING` recorded as a `FAILED`
receipt carrying `PUBLISH_PENDING` and **returned**, not raised, because `PENDING`
is not in `types.STEP_STATUSES`; `run_step`'s `spending` defaulting to `None`
rather than the wave plan's `False`; a halting set of 17 codes where 4.4's
sentence names six plus "any `CustodyError`"; and the `VERIFIED` line in a
write-once sidecar with only its digest in the closed receipt schema.

## Two findings, each with the command beside it

1. **All five of this module's `NEW_CODES` are missing from `types.FAILURE_CODES`.**
   `python3 -c "from minireason.loop import steps, types; print(sorted(set(steps.NEW_CODES) - set(types.FAILURE_CODES)))"`
   prints `['RUN_LOCKED', 'STEP_BODY_FAILED', 'STEP_CLASS_DISAGREEMENT',
   'STEP_NOT_HALTED', 'STEP_OUTPUTS_INVALID']`.
   `notes/WAVE1-INTEGRATION-DECISIONS.md` item 6 requires them to be folded in.
   All 17 members of `CUSTODY_HALT_CODES` are already in the table (same command,
   with `CUSTODY_HALT_CODES` substituted, prints `[]`).
2. **A started step can end with no receipt at all.** A named output that is not
   JSON-serialisable escapes `StepHandle.complete()` as a bare `TypeError` from
   `custody.digest` (`steps.py:301` → `custody.py:269`); `complete()` is called
   *outside* `run_step`'s `except BaseException` (`steps.py:1047-1052`), so
   `fail_from` never runs. Observed directly: on a `SEND` step this left
   `steps/0001-SEND.json.open` alone in the directory and the next `guard()`
   refused with `UNRESOLVED_STEP`; on a non-spending `CLOSE` step no `steps/`
   directory was created at all. `STEP_OUTPUTS_INVALID` covers only a non-mapping
   container or a non-name key (`steps.py:304-314`), not a non-digestible value,
   despite `NEW_CODES`' own one-line reason for it (`steps.py:146`). The page
   states this under "does not promise" and tells the operator to keep outputs to
   `bytes`, a `Path`, a 64-char hex digest or plain JSON data.

## How the claims were checked

No test module for W1-STEPS exists in the sandbox (`tests/loop/` holds only
`__init__.py`), so `python3 run_tests.py tests.loop.test_steps` had nothing to
run. Instead I exercised the module directly with `python3 -c` programs against
throwaway run trees created and then deleted under `out/`, confirming by
observation: the marker and receipt filenames; `SKIPPED` without re-entering the
body; `UNRESOLVED_STEP` after a killed spending step and the acknowledgement that
clears it; `WRITE_ONCE_VIOLATION` on a second acknowledgement; a custody halt's
`HALTED` receipt, its `errata/0001-READ-HALT.md` stub and its sticky
re-refusal; a step timeout leaving both receipt and marker; a `PUBLISH_PENDING`
receipt blocking a successor with `PublishBlocked` and a second attempt landing at
a new index with its `.verified` sidecar; `RUN_LOCKED` and the lock's
`PLAN_ID_MISMATCH`; `STEP_NONDETERMINISTIC` on a replay; `STEP_CLASS_DISAGREEMENT`
both ways; `PLAN_ID_MISMATCH` on a foreign receipt; and `scan_coordinates`'
three-way split. `out/` now contains only the deliverable.

Every UPPER_SNAKE token in the page was checked against the module:
`python3 -c "..."` comparing the page's tokens to
`re.findall(...)` over `steps.py` plus the computed `CUSTODY_HALT_CODES` leaves
only `DECISION_LEDGER` (part of a path), `USE_TABLE` (a step kind from
`types.STEP_KINDS`) and `PENDING_REASONS` / `MAX_PUBLISH_ATTEMPTS`, which the page
names explicitly as W0-PUBLISH's and not as step failure codes. No fenced block in
the page exceeds seven lines.

## Failure codes found in the module that I could not give an operator action for

* **The eight halting codes `steps.py` classifies but never raises** —
  `CUSTODY_MISMATCH`, `REQUEST_NOT_FROM_PLAN`,
  `ARTIFACT_NOT_DERIVED_FROM_DELIVERY`, `TIMEOUT_NOT_APPLIED`,
  `PROVIDER_REQUEST_FILE_CHANGED`, `TRANSPORT_PIN_MISMATCH`,
  `RUNTIME_SOURCE_CHANGED`, `INPUT_NOT_PUBLISHED` (`steps.py:174-183`). The page
  gives them **one family action** (read the erratum stub, settle the custody
  question at its source, then acknowledge with a reason) and no per-code remedy,
  because the modules that raise them — the importer, runner v2, the delivery
  custody check — are not in this sandbox and I could not read what each one
  means at its own raise site. A per-code action for these belongs to the
  W1-GRAPH and runner-v2 sections of the same operator page.
* **`REMOTE_NOT_CONFIRMED`** (`steps.py:1093`) is the fallback reason the ledger
  writes into a `PUBLISH_PENDING` detail when the `PublishPending` object names
  none. It is a W0-PUBLISH pending reason rather than a step failure code, and the
  page gives it no action of its own beyond the `PUBLISH_PENDING` row.
* **`HTTP_429`** (`steps.py:52`) appears only as the docstring's example of a
  stable provider code that resolves a marker. It is the provider's code, not one
  this module raises, so the page uses it as an illustration and gives it no
  operator row.

## What I could not determine

* **The command and the flags.** `tools/auto_loop.py` is not in the sandbox, so I
  could not verify that `--acknowledge <step_key> --reason "<text>"` is wired to
  `StepLedger.acknowledge`, nor check any other CLI spelling. The page attributes
  that spelling to design 4.2/4.4 and describes only the calls `steps.py` itself
  publishes. Unresolved.
* **The rest of the operator page.** `docs/workflows/automated-loop.md` does not
  exist in the sandbox; the config block, the directory layout beyond `steps/`,
  the block-code register, the pre-registration and obligations templates and the
  ceiling text belong to other W6-DOC sections and are not written here. The one
  ceiling file present, `src/minireason/loop/data/ceiling_v1.md`, was left to
  whoever writes that section.
* **Windows behaviour.** `steps.py:103-106` and `401-407` take an `msvcrt` path
  marked `pragma: no cover - exercised on Windows only`. This sandbox is Linux, so
  the page's `RUN_LOCKED` claims were observed under `fcntl.flock` only; I could
  not exercise `msvcrt.locking`, and `docs/errata/REC-20260913-windows-execution.md`
  is not in the sandbox to read against it.
* **No test evidence for W1-STEPS.** There is no `tests/loop/test_steps.py` here,
  so I cannot report a test count for this module, and nothing in this section is
  backed by a passing suite — only by direct observation of the module, recorded
  above. I could not determine whether such a test module exists elsewhere in the
  repository.
* **Whether `PublishNotConverging` can reach an operator through this module.**
  `publish()` raises it at the attempt ceiling and `publish_step` records and
  re-raises whatever the publisher raised (`steps.py:1088-1090`), but its code
  (`PUBLISH_NOT_CONVERGING`) does not appear in `steps.py`, so per the rule
  against naming codes the module cannot raise I left it out of the table rather
  than guess at its operator action.
* **The `INDETERMINATE` token's downstream home.** `steps.py:77` and `347` say a
  coordinate is "reported `INDETERMINATE`", but `scan_coordinates` returns
  frozensets and writes nothing; which record carries that word to a reader is
  decided outside this module and I could not determine where.
