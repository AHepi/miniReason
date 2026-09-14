# Adversarial review — W0-RECEIPTS (`src/minireason/loop/receipts.py`)

Reviewed against `notes/WAVE0-INTERFACE.md` §5, the module's own docstring,
and the wave-plan acceptance clause (design-s7 §7):

> "Concurrent appends from two threads interleave with no loss and no torn record
> under simulated short writes; id minting under contention never collides; a
> secret-bearing body is refused, not redacted; a missed cadence deadline is
> recorded and never backdated; activity records carry no raw command text."

Every finding below was executed by a probe under `probe/`; the printed output is
quoted verbatim. Probes were run as `python3 probe/<name>.py` with `src` made
importable inside the probe (`sys.path.insert(0, "src")`).

---

## BLOCKER

### B1 — `bracket()` masks the caller's real exception when the outcome log fails

**Claim.** When the guarded body raises and the "outcome" activity record then
also fails, `bracket` discards the original exception entirely: the `ReceiptError`
from the logging failure escapes with no chaining, and no record of the original
failure is ever emitted.

**Location.** `src/minireason/loop/receipts.py`, the `bracket` contextmanager —
the `except BaseException` block (`activity("outcome", ...)` inside it, then
`raise`), lines containing:

```python
    except BaseException as error:
        activity("outcome", action, f"{why}; interrupted by {type(error).__name__}",
                 goal, paths, **kwargs)
        raise
```

**Contradicted claim.** The docstring states the design intent: "An exception is
reported by type only; an exception message can carry anything, including a
credential, and is never logged." The purpose of that sentence is to keep the
*original* failure visible as an operational failure (operations.md: "An
interrupted or truncated response must remain visible as an operational
failure"). As written, a failing outcome logger makes the original exception
invisible: `except OriginalError` catches nothing, and the `ACTIVITY_LOGGER_FAILED`
that escapes carries no `__cause__`/`__context__` naming the type of what was
actually being bracketed.

**Probe** (`probe/bracket_masking.py`), verbatim output:

```
original exception MASKED by ACTIVITY_LOGGER_FAILED
```

**Repair.** In the `except` block, wrap the outcome `activity(...)` call in
`try: ... except Exception as log_err: ... raise ... from None` is not the shape;
use:

```python
    except BaseException as error:
        try:
            activity("outcome", action, f"{why}; interrupted by {type(error).__name__}",
                     goal, paths, **kwargs)
        except LoopError:
            raise error   # the caller's failure outranks a logging failure
        raise
```

(or, alternatively, chain: `raise ReceiptError(...) from error` — but the first
form preserves the published contract that a real failure surfaces as itself).

**Test that would hold the repair.** A `bracket` context whose body raises a
named exception class and whose `runner` returns `returncode != 0` on the second
call must propagate the body's exception, and a caller asserting
`pytest.raises(OriginalError)` stays green.

---

## SHOULD-FIX

### S1 — A runner raising `OSError` escapes `activity()` as a non-`LoopError`

**Claim.** `activity()` converts only `subprocess.TimeoutExpired`; a runner that
raises `OSError` (executable vanished, EMFILE, EACCES on `sys.executable`)
propagates a bare `OSError`, so the promised "one `except LoopError` catches
every wave-0 refusal" misses it and a step can name no `failure_code`.

**Location.** `activity()`, the `try:/except subprocess.TimeoutExpired` around
`runner(...)` (the only `except` clause; `OSError` is not caught), at
`src/minireason/loop/receipts.py` in the block beginning
`try: result = runner(argv, ...)`.

**Contradicted claim.** The docstring: "Every way the logger can fail carries a
code from the table. A timeout used to propagate `subprocess.TimeoutExpired`
unchanged, which is not a `LoopError`, so `except LoopError` missed it and the
step could name no `failure_code`; it is now `ACTIVITY_LOGGER_FAILED`." The
rationale applies verbatim to `OSError`, which is left unconverted — the fix
covered one member of the failure class it describes.

**Probe** (`probe/activity_runner_errors.py`), verbatim output:

```
negative timeout: LoopError ACTIVITY_LOGGER_FAILED
OSError runner: NON-LoopError OSError No such file or directory
timeout runner: LoopError ACTIVITY_LOGGER_FAILED
```

(The negative-timeout line also shows `subprocess.run`'s own `ValueError` for an
invalid timeout is caught somewhere upstream of my expectation — it surfaced as
`ACTIVITY_LOGGER_FAILED` here because `subprocess` raised inside its own wrapper;
that path is fine. The `OSError` path is not.)

**Repair.** Add `except OSError as error: raise ReceiptError("ACTIVITY_LOGGER_FAILED",
str(redact(type(error).__name__))) from error` beside the `TimeoutExpired` handler.
Detail must not echo the errno string verbatim if it could embed a path carrying
a credential — `type(error).__name__` suffices.

**Test.** A runner double raising `OSError` must produce `ReceiptError` with
`.code == "ACTIVITY_LOGGER_FAILED"` and `isinstance(e, LoopError)`.

---

### S2 — A render callback (or any caller-supplied code) can deadlock the append path

**Claim.** `open_receipt(render=...)` runs the caller's callable while holding
`_APPEND_LOCK` (a `threading.RLock`) and while holding an exclusive `flock` on
the ledger handle. Because the RLock is re-entrant *in the same thread*, a render
callback that calls any published append/minting function re-enters, opens a
second file description of the ledger, and blocks in `fcntl.flock` forever —
same thread, same process, no exception, no code, and the RLock now held forever
for every other thread.

**Location.** `src/minireason/loop/receipts.py`: `_APPEND_LOCK = threading.RLock()`
(class-level lock), the `with _APPEND_LOCK:` block in `_append()` which calls
`render(data)` between `_lock(handle)` and `_unlock(handle)`; and
`mint_receipt_id`'s docstring.

**Contradicted claim.** `mint_receipt_id`'s docstring: "Never call this from
inside a render callback — the append lock is not re-entrant across threads."
That sentence warns about `mint_receipt_id` while (a) the hazard it gestures at
is worded backwards — the lock *is* re-entrant in the same thread, which is where
render runs, and it is the re-entrancy combined with a same-process `flock` on a
second description that hangs; and (b) the warning covers one function while the
seam `open_receipt(render=...)` publishes admits *any* append call, with no guard.
The interface entry in WAVE0-INTERFACE §5 publishes `open_receipt(...,
render, ...)` with no note about re-entry at all.

**Probe.** Two runs. First (`probe/render_render_reenter.py`, SIGALRM-bounded):

```
platform: linux
_APPEND_LOCK type: RLock
DEADLOCK: re-entrant ledger_append from a render callback hung on flock in the same thread; no exception, no code
```

A second probe calling `mint_receipt_id` from the callback (`probe/render_collision.py`)
completed with `completed: REC-20260915-A (no deadlock)` only because
`mint_receipt_id` reads but never writes — so it grabs the RLock re-entrantly and
returns *without* opening the ledger for append. It prints a correct-looking id
that is, however, minted from state mid-hold; the docstring warns against it and
nothing enforces the warning. Both behaviours (hang vs. silent advisory id under
a lock the caller thought was exclusive) are unsound at a published seam.

**Repair.** Reject re-entry: make `_append` record the owning thread (or use a
non-reentrant `threading.Lock` plus an internal `_render` channel that never
touches the lock), and raise a coded refusal (`ReceiptError("LEDGER_REENTRANT_RENDER",
...)`, added to `types.FAILURE_CODES`) when `render` or any nested call attempts
to re-enter. At minimum, fix the docstring sentence so it describes the same-thread
hang it actually means, and refuse in `open_receipt` if `render` is not `None`
while the lock is already held by this thread — that converts a silent deadlock
into a named refusal.

**Test.** A render callback that calls `ledger_append` must raise (the new code)
in bounded time; assert with a watchdog thread that the call returns within N
seconds rather than hanging, and that `_APPEND_LOCK` is free afterwards.

---

## NOTE

### N1 — `_CURRENT_LOCK` is a second, independent lock; `activity()` reads the current receipt without it

**Claim.** `current_receipt()` takes `_CURRENT_LOCK`, but `activity()` reads
`current_receipt()` *after* building nothing and the two calls in `activity()`
(`receipt_id = decision or current_receipt()`) and `open_receipt`'s
`set_current_receipt(...)` are not atomic: a process running two receipts on two
threads can log an activity under the other thread's receipt id. This is a design
limitation of a process-global "current receipt", documented as "the receipt this
process last opened", so I record it as a note: the published interface
acknowledges the global (`set_current_receipt` / `current_receipt`) and the
driver guidance is to pass `decision=` explicitly, but `bracket()`'s keyword
pass-through makes it easy to forget, and a wrong `--decision` is written to the
activity log silently.

**Location.** `_CURRENT_RECEIPT` global and `activity()`'s `receipt_id = decision
or current_receipt()` line in `src/minireason/loop/receipts.py`.

**Contradicted claim.** WAVE0-INTERFACE §5 deviation 4: "an optional `decision`
keyword that falls back to the receipt this process last opened" — accurate; the
note is that the fallback is racy across threads with no guard and no test seam
asserting thread-locality.

**Probe.** Not separately scripted beyond code reading plus the thread-contention
run in `probe/attacks_failed.py` (80 mints, all unique, but all with
`set_current=False`; with the default `True` two threads would interleave
`set_current_receipt`). I could not construct a *corrupt* record from this —
`activity()` refuses to run with no receipt at all — so this stays a NOTE, not
a defect.

**Repair.** Accept the global, but document in `bracket`'s docstring that the
fallback is process-global, or make `_CURRENT_RECEIPT` a `threading.local`.

### N2 — `_secret_items()` in the transport excludes values shorter than 8 chars; an 8-character boundary means a 7-char credential is never scanned

Not a defect of `receipts.py` (the floor is a documented transport decision,
`_MIN_SECRET_LENGTH = 8`, and my first probe attempt failed precisely because an
undeclared env var name is outside the scanner's declared set). Recorded so the
review does not overclaim: the ledger writer's refusal is exactly as strong as
the transport's declared credential set, no stronger.

---

## Tried, and could not break

Four attacks, all executed, all failed; the module held each claim they targeted.

1. **Id-minting under thread contention** (acceptance: "id minting under
   contention never collides"). `probe/attacks_failed.py` ran 4 threads × 20
   `open_receipt` calls each against one ledger:
   `minted: 80 unique: 80 errors: 0 -> attack failed`.

2. **Secret-bearing body refused, value never echoed** (acceptance: "a
   secret-bearing body is refused, not redacted"). After declaring the credential
   name through the transport's own `register_secret_envs` (the honest route —
   the scanner's set is declared, not ambient), and again with the always-secret
   `DEEPSEEK_API_KEY`:
   `refused: SECRET_IN_RECEIPT | names: ('PROBE_REG_CRED',) | value leaked into exception: False`
   and `ledger unchanged: True` (`probe/secret_refusal_fixed.py`).
   My first attempt at this attack *failed to find a bug* in a way that is itself
   evidence: an undeclared env var holding an 8+-char value sails through
   (`attack SUCCEEDED` in the first version of the probe) — but that is the
   transport's documented "declared set, not a name-shape scan" design, and
   `receipts.py` correctly delegates to it. Not a finding.

3. **Cadence miss recorded at notice time, never backdated** (acceptance: "a
   missed cadence deadline is recorded and never backdated"). A clock 400 s past
   its deadline reports `overdue`, the `CadenceMiss` records the deadline and the
   *notice* time separately, and a backdated `acknowledge` is refused:
   `3a. state: overdue ... deadline: 2026-09-15 00:05:00` /
   `3b. refused with CADENCE_BACKDATED -> attack failed`.

4. **Suffix minting past `Z` is bijective, never reuses `A`** (module docstring
   deviation 2). Thirty successive mints give `B C D ... Z AA AB AC AD AE`, no
   reuse: `reused: False`.

Plus a byte-mode control (`probe/byte_mode_add_only.py`): over a CRLF-terminated
ledger, the prefix bytes survive untouched (`prefix preserved: True`), no spurious
blank line is inserted, and `LedgerAppend.end` accounts exactly for the final
size — the property the whole module exists to keep (the 37-CRLF-line ledger in
`docs/lessons/operations.md`).
