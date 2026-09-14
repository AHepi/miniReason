"""W1-STEPS - the step ledger: step keys, write-once receipts, halts and resume.

Implements the wave-1 module ``W1-STEPS`` of *The automated end-to-end harness
loop - FINAL design of record*, section 4.3 (*Step receipts and resume*) and the
halt, timeout and publication clauses of section 4.4 and 4.5.

What this module is
-------------------

One run's ``<run_root>/steps/`` directory, read and written through one object.
:class:`StepLedger` derives a step's identity (``step_key``) from the frozen
plan, writes the ``.open`` marker a spending step needs *before* the step runs,
writes exactly one write-once receipt when it ends, and refuses to start a
successor step while anything is unresolved: an open marker, an unacknowledged
custody halt, or a publication that is still ``PENDING``.

What this module is **not**: it decides nothing, it reads no material, and it
never works around custody.  A refusal here is a refusal, recorded as a receipt
with its code and re-raised.  The only state that ever clears a halt is an
operator's acknowledgement, which is itself a write-once record naming a reason.

The three step classes (design 4.3)
-----------------------------------

* **Replayable** - :data:`~minireason.loop.types.REPLAYABLE_STEPS`.  Offline,
  deterministic, pure.  On resume the step is **re-run** and its outputs must
  digest to what the existing receipt recorded, or :class:`StepNondeterministic`
  is raised - a live check, not a formality.
* **Spending** - :data:`~minireason.loop.types.SPENDING_STEPS`.  A call may have
  been billed or a remote may have moved.  An ``.open`` marker is written before
  the step and resolved by the receipt; an unresolved marker on resume halts
  with ``UNRESOLVED_STEP`` and the step body is **never** re-entered.
* Everything else (``PREREGISTER``, ``CYCLE_OPEN``, ``PREPARE``, ``CLOSE``) is
  neither: a ``COMPLETE`` receipt is skipped on resume and nothing is replayed.

Deviations from the design, and why
-----------------------------------

*  **``run_step``'s ``spending`` parameter defaults to ``None``, not
   ``False``.**  The wave plan publishes ``run_step(kind, cycle, inputs, fn,
   spending=False)``, but the classification is already a closed table
   (:data:`~minireason.loop.types.SPENDING_STEPS`) and the receipt refuses a
   receipt whose flag disagrees with it.  ``None`` means *take it from the
   table*; an explicit ``bool`` is **asserted** against the table and a
   disagreement is ``STEP_CLASS_DISAGREEMENT``.  Every call written against the
   published signature behaves exactly as published.
*  **A spending step's marker survives two outcomes** - :data:`MARKER_KEPT_CODES`
   (``STEP_TIMEOUT`` and ``STEP_BODY_FAILED``).  Section 4.3 says the marker is
   "resolved by the receipt"; section 4.4 says a step timeout "leaves the open
   marker and therefore halts on resume - deliberately".  Both hold once the
   rule is stated as *a marker is resolved by an outcome that says what
   happened*: a stable provider code (``HTTP_429``) and a custody halt both do;
   a timeout and an unclassified crash do not, because neither tells us whether
   a call was billed.
*  **A ``PENDING`` publication is recorded as a ``FAILED`` receipt carrying
   ``PUBLISH_PENDING``**, because ``PENDING`` is not a member of
   :data:`~minireason.loop.types.STEP_STATUSES` and section 4.4 makes it a
   retryable *state of the publication* rather than an end state of the run.
   :meth:`StepLedger.publish_step` therefore **returns** it instead of raising,
   and the guard blocks every successor step until a later attempt on the same
   ``step_key`` returns ``PUBLISHED`` (design O7).
*  **The ``VERIFIED`` line is written to a write-once sidecar**
   ``steps/NNNN-KIND.verified`` and the receipt records its sha256 under
   ``outputs_sha256["verified_line"]``.  The receipt schema is closed and has no
   free-text field; a digest in the receipt plus the bytes beside it plus the
   ledger's own copy is three places that must agree, which is the point.
*  **``custody.verified`` defaults to ``false``.**  A receipt whose driver ran no
   custody check says so.  :meth:`StepHandle.record_custody` is how a check that
   *did* run reaches the receipt, through
   :meth:`~minireason.loop.types.CustodyReport.from_findings` and nothing else.
*  **``run.lock`` is written, not ``write_new``-written.**  It is not a record of
   what happened; it is a mutual exclusion re-taken on every resume.  Exclusion
   itself is ``flock(LOCK_EX | LOCK_NB)``, which the kernel releases when the
   holder dies, so a stale file can never wedge a run.
*  **``completed_coordinates`` gained a sibling**, :func:`scan_coordinates`.
   Section 4.3 requires a coordinate with a request or attempt but no response
   to be reported ``INDETERMINATE`` *and never as an absence*, and the completed
   set alone cannot express that difference.

   **This module makes that difference visible; it does not report it.**
   :func:`scan_coordinates` returns three frozensets and writes nothing at all -
   no record here carries the word ``INDETERMINATE`` to any reader, and no
   receipt this ledger writes names it.  Turning ``CoordinateScan.indeterminate``
   into a line a reader sees is **W3-REPORT**'s (the reading table's per-cell
   state) and **W5-DRIVER**'s (the resume decision the operator is shown); the
   code itself is declared in ``types.FAILURE_CODES`` for the receipt a
   *delivery* writes under it.  Until one of those two lands, a coordinate that
   was asked and never answered is visible only to a caller that asks this
   function for it, and the guarantee "never as an absence" holds only in this
   module's return value.
"""
from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping, Sequence

from minireason.loop import custody, publish as publish_module, receipts
from minireason.loop.types import (
    CustodyReport,
    LoopError,
    RunPaths,
    SPENDING_STEPS,
    STEP_KINDS,
    StepReceipt,
    TimeoutsConfig,
)

if os.name == "nt":  # pragma: no cover - exercised on Windows only
    import msvcrt
else:
    import fcntl

__all__ = [
    "ACK_SCHEMA",
    "CUSTODY_HALT_CODES",
    "CoordinateScan",
    "LOCK_SCHEMA",
    "MARKER_KEPT_CODES",
    "MARKER_SCHEMA",
    "NEW_CODES",
    "PUBLICATION_STEPS",
    "PublishBlocked",
    "RESUME_ACTIONS",
    "ResumeAction",
    "RunLock",
    "RunLocked",
    "STEP_OUTCOMES",
    "StepError",
    "StepHandle",
    "StepLedger",
    "StepNondeterministic",
    "StepOutcome",
    "StepRecord",
    "StepTimeout",
    "StickyHalt",
    "UnresolvedStep",
    "VERIFIED_SUFFIX",
    "completed_coordinates",
    "erratum_text",
    "scan_coordinates",
]

#: Codes this module introduces, with the one-line reason each exists.  Every
#: other code it raises is already a member of ``types.FAILURE_CODES``; these
#: extend that table in the same wave that raises them (wave-0 open question O9).
NEW_CODES: Mapping[str, str] = MappingProxyType({
    "RUN_LOCKED": "a second driver holds this run's run.lock; design 4.6 refuses it rather than sharing the per-credential gate.",
    "STEP_BODY_FAILED": "a step body raised something that carries no stable code, so the receipt names the absence rather than inventing one.",
    "STEP_CLASS_DISAGREEMENT": "a caller declared a spending flag, or a publication kind, that disagrees with the closed table in types.",
    "STEP_NOT_HALTED": "acknowledge() was given a step_key with nothing unresolved to acknowledge.",
    "STEP_OUTPUTS_INVALID": "a step body returned outputs that are not a mapping of name to digestible value.",
})

#: The schema token of an open marker, an acknowledgement and the run lock.
MARKER_SCHEMA = "minireason.loop.step-open.v1"
ACK_SCHEMA = "minireason.loop.step-acknowledgement.v1"
LOCK_SCHEMA = "minireason.loop.run-lock.v1"

#: The four publication transitions of design 4.1.
PUBLICATION_STEPS: tuple[str, ...] = (
    "PUBLISH_PLAN", "PUBLISH_IN", "PUBLISH_EV", "PUBLISH_CY",
)

#: What :meth:`StepLedger.resume_plan` can say about one recorded step.
RESUME_ACTIONS: tuple[str, ...] = ("SKIP", "REPLAY", "RETRY", "HALT")

#: What one call to :meth:`StepLedger.run_step` did.  The first three are also
#: receipt statuses; ``SKIPPED`` and ``REPLAYED`` write no new receipt.
STEP_OUTCOMES: tuple[str, ...] = (
    "COMPLETE", "FAILED", "HALTED", "SKIPPED", "REPLAYED",
)

#: The two outcomes that leave a spending step's ``.open`` marker in place,
#: because neither of them tells us whether a call was billed (design 4.4).
MARKER_KEPT_CODES: frozenset[str] = frozenset({"STEP_TIMEOUT", "STEP_BODY_FAILED"})

#: Design 4.4's halting set: every custody code, plus the delivery-custody codes
#: the importer and runner v2 raise.  A halt is sticky; a failure is not.
#:
#: **This module classifies the eight below and raises none of them.**  Each is
#: recorded here when a *caller* hands one in - through :meth:`StepHandle.halt`,
#: or as the code of an exception a body raised - and each has a different raise
#: site, so a receipt carrying one needs a per-code operator action rather than
#: the family action "a custody halt: re-verify and acknowledge".  W6-DOC owes
#: one action per code, sourced from the site named beside it:
#:
#: ============================== ==========================================
#: code                           raised by
#: ============================== ==========================================
#: ``CUSTODY_MISMATCH``           a caller's aggregate name for a non-empty
#:                                ``custody.verify_pins`` result
#: ``RUNTIME_SOURCE_CHANGED``     the same, where the moved file is a pinned
#:                                *source* of the run
#: ``REQUEST_NOT_FROM_PLAN``      W1-ROLES / runner v2 delivery custody: the
#:                                request bytes are not the plan's
#: ``ARTIFACT_NOT_DERIVED_FROM_DELIVERY`` W1-GRAPH: an imported artifact whose
#:                                provenance does not reach a delivery
#: ``TIMEOUT_NOT_APPLIED``        runner v2: the wall clock the plan declared
#:                                was not the one the transport used
#: ``PROVIDER_REQUEST_FILE_CHANGED`` runner v2: the on-disk request moved
#:                                between writing and dispatch
#: ``TRANSPORT_PIN_MISMATCH``     PREFLIGHT: the transport module is not at
#:                                its pinned bytes
#: ``INPUT_NOT_PUBLISHED``        W0-PUBLISH's read-back: an input that was to
#:                                be published is not on the ref
#: ============================== ==========================================
CUSTODY_HALT_CODES: frozenset[str] = frozenset(custody.CUSTODY_CODES) | frozenset({
    "CUSTODY_MISMATCH",
    "REQUEST_NOT_FROM_PLAN",
    "ARTIFACT_NOT_DERIVED_FROM_DELIVERY",
    "TIMEOUT_NOT_APPLIED",
    "PROVIDER_REQUEST_FILE_CHANGED",
    "TRANSPORT_PIN_MISMATCH",
    "RUNTIME_SOURCE_CHANGED",
    "INPUT_NOT_PUBLISHED",
})

#: The write-once sidecar beside a publication receipt that holds its
#: ``VERIFIED`` line verbatim.
VERIFIED_SUFFIX = ".verified"

#: The receipt key the ``VERIFIED`` line's digest is filed under.
VERIFIED_OUTPUT_KEY = "verified_line"

_HEX64 = re.compile(r"[0-9a-f]{64}\Z")
_RECEIPT_NAME = re.compile(r"(\d{4})-([A-Z_]+)\.json\Z")
_MARKER_NAME = re.compile(r"(\d{4})-([A-Z_]+)\.json\.open\Z")
_DETAIL_LIMIT = 400


# --------------------------------------------------------------------------- #
# Refusals.  Every one is a types.LoopError, so ``except LoopError`` catches
# every refusal in the package (the package convention).
# --------------------------------------------------------------------------- #

class StepError(LoopError):
    """Anything the step ledger refuses.  ``(code, detail="")``."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code, detail[:_DETAIL_LIMIT])


class UnresolvedStep(StepError):
    """An ``.open`` marker survived a kill: a call may have been billed."""

    def __init__(self, detail: str = "", *, step_key: str | None = None,
                 index: int | None = None, kind: str | None = None) -> None:
        super().__init__("UNRESOLVED_STEP", detail)
        self.step_key = step_key
        self.index = index
        self.kind = kind


class StepNondeterministic(StepError):
    """A replayable step re-ran and did not reproduce its recorded bytes."""

    def __init__(self, detail: str = "", *, step_key: str | None = None,
                 differing: Sequence[str] = ()) -> None:
        super().__init__("STEP_NONDETERMINISTIC", detail)
        self.step_key = step_key
        self.differing = tuple(differing)


class StepTimeout(StepError):
    """``timeouts.step_seconds`` for this kind was exceeded (design 4.4)."""

    def __init__(self, detail: str = "") -> None:
        super().__init__("STEP_TIMEOUT", detail)


class StickyHalt(StepError):
    """A recorded ``HALTED`` step that no acknowledgement has cleared.

    ``code`` is the halted receipt's **own** failure code, so the driver exits
    naming the same code the record names rather than a second name for it.
    """

    def __init__(self, code: str, detail: str = "", *, step_key: str | None = None,
                 index: int | None = None) -> None:
        super().__init__(code, detail)
        self.step_key = step_key
        self.index = index


class PublishBlocked(StepError):
    """A publication is ``PENDING``; it blocks every successor step (4.4)."""

    def __init__(self, detail: str = "", *, step_key: str | None = None) -> None:
        super().__init__("PUBLISH_PENDING", detail)
        self.step_key = step_key


class RunLocked(StepError):
    """A second driver already holds this run's ``run.lock`` (design 4.6)."""

    def __init__(self, detail: str = "") -> None:
        super().__init__("RUN_LOCKED", detail)


# --------------------------------------------------------------------------- #
# Small pure helpers
# --------------------------------------------------------------------------- #

def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _stamp(moment: datetime) -> str:
    """The receipt's ISO-8601 UTC form.  A naive moment has no UTC meaning."""

    if not isinstance(moment, datetime):
        raise StepError("MOMENT_NOT_DATETIME", type(moment).__name__)
    if moment.tzinfo is None:
        raise StepError("MOMENT_NOT_AWARE", "a naive datetime has no UTC meaning")
    return (moment.astimezone(timezone.utc).replace(microsecond=0)
            .isoformat().replace("+00:00", "Z"))


def _digest_of(value: Any) -> str:
    """The digest this ledger files a named input or output under.

    ``bytes`` are hashed as bytes; a :class:`~pathlib.Path` is hashed as the
    bytes at it; a 64-character lowercase hex string is taken as an
    already-computed digest; anything else is hashed as canonical JSON through
    :func:`custody.digest`, which is byte-identical to the transport's.
    """

    if isinstance(value, (bytes, bytearray, memoryview)):
        return custody.sha256_bytes(bytes(value))
    if isinstance(value, Path):
        try:
            return custody.sha256_path(value)
        except OSError as exc:
            raise StepError("STEP_OUTPUTS_INVALID",
                            f"{value} cannot be read: {type(exc).__name__}") from exc
    if isinstance(value, str) and _HEX64.fullmatch(value):
        return value
    try:
        return custody.digest(value)
    except LoopError as exc:
        # A value that cannot be digested is an invalid OUTPUT, whatever the
        # digest helper calls it: the receipt's own code says which of the step's
        # promises was broken, and STEP_OUTPUTS_INVALID is the one that was.
        raise StepError("STEP_OUTPUTS_INVALID", f"{exc.code}: {exc.detail}") from exc
    except (TypeError, ValueError) as exc:  # pragma: no cover - belt and braces
        raise StepError("STEP_OUTPUTS_INVALID",
                        f"{type(value).__name__} cannot be digested: {exc}") from exc


def _digest_map(value: Any, where: str) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise StepError("STEP_OUTPUTS_INVALID", f"{where} must be a mapping")
    out: dict[str, str] = {}
    for name, item in value.items():
        if not isinstance(name, str) or not name:
            raise StepError("STEP_OUTPUTS_INVALID", f"{where} keys must be names")
        out[name] = _digest_of(item)
    return dict(sorted(out.items()))


def _coordinate(relative: Path) -> str:
    """The coordinate one record file belongs to: its path with suffixes gone."""

    name = relative.name
    while True:
        stem = Path(name).stem
        if stem == name:
            break
        name = stem
    parent = relative.parent
    return name if str(parent) == "." else (parent / name).as_posix()


def _phase_coordinates(directory: Path) -> set[str]:
    if not directory.is_dir():
        return set()
    found: set[str] = set()
    for path in sorted(directory.rglob("*")):
        if path.is_file():
            found.add(_coordinate(path.relative_to(directory)))
    return found


@dataclass(frozen=True)
class CoordinateScan:
    """Coordinate-grain resume state for one records directory (design 4.3)."""

    #: A response is on record: the coordinate is terminal and is skipped.
    complete: frozenset[str]
    #: A request or an attempt but no response.  Re-sending is refused and the
    #: coordinate is reported ``INDETERMINATE`` - never as an absence.
    indeterminate: frozenset[str]
    #: Every coordinate the directory knows about, terminal or not.
    started: frozenset[str]


def scan_coordinates(out_dir: str | os.PathLike[str]) -> CoordinateScan:
    """Read ``requests/``, ``attempts/`` and ``responses/`` under ``out_dir``.

    The reading tree of design 4.2 is
    ``readings/<row_key>/{requests,attempts,responses,provider}/...`` and every
    record in it is write-once, which is exactly what makes per-coordinate
    resumption safe: this function only *reads*, and writes nothing anywhere.
    """

    root = Path(out_dir)
    asked = _phase_coordinates(root / "requests") | _phase_coordinates(root / "attempts")
    answered = _phase_coordinates(root / "responses")
    return CoordinateScan(complete=frozenset(answered),
                          indeterminate=frozenset(asked - answered),
                          started=frozenset(asked | answered))


def completed_coordinates(out_dir: str | os.PathLike[str]) -> set[str]:
    """The coordinates under ``out_dir`` that already have a response."""

    return set(scan_coordinates(out_dir).complete)


def erratum_text(receipt: StepReceipt, *, reason: str | None = None) -> str:
    """The erratum a halt writes, and the acknowledgement that clears it.

    Plain prose over the receipt's own stable fields: no count, no score and no
    claim about the material - a halt is a fact about the instrument.
    """

    checks = ", ".join(receipt.custody.checks) or "none recorded"
    text = (
        f"step {receipt.index:04d}-{receipt.kind} halted with "
        f"{receipt.failure_code} at {receipt.finished_utc or receipt.started_utc}; "
        f"step_key {receipt.step_key}; custody checks: {checks}. "
        "The loop never works around custody: this step registered nothing and "
        "its successors were refused."
    )
    if reason is not None:
        text += (" Acknowledged by the operator, who gave this reason: "
                 f"{reason.strip()}")
    return text


# --------------------------------------------------------------------------- #
# run.lock - one driver per run (design 4.6)
# --------------------------------------------------------------------------- #

def _lock_exclusive(handle: Any) -> None:
    if os.name == "nt":  # pragma: no cover - exercised on Windows only
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
    else:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)


def _unlock(handle: Any) -> None:
    if os.name == "nt":  # pragma: no cover - exercised on Windows only
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        fcntl.flock(handle, fcntl.LOCK_UN)


class RunLock:
    """Advisory-across-runs, mandatory-on-this-run exclusion for one run tree.

    Design 4.6: the five-per-credential ceiling is a process-wide registry
    inside ``provider_openai_compat``, so it holds only inside one process.  A
    second driver on the same run would be a second process and a second set of
    slots, so it is refused.  The exclusion is the kernel's ``flock``, which is
    released when the holder dies; the file's contents (pid, start time,
    ``loop_plan_id``) are for the human reading the refusal.
    """

    def __init__(self, path: str | os.PathLike[str], loop_plan_id: str, *,
                 pid: int | None = None,
                 clock: Callable[[], datetime] | None = None) -> None:
        self.path = Path(path)
        self.loop_plan_id = str(loop_plan_id)
        self.pid = os.getpid() if pid is None else int(pid)
        self._clock = clock if clock is not None else _utc_now
        self._handle: Any | None = None

    @property
    def held(self) -> bool:
        return self._handle is not None

    def holder(self) -> dict[str, Any] | None:
        """What the lock file says, or ``None`` when it says nothing legible."""

        try:
            raw = self.path.read_bytes()
        except OSError:
            return None
        try:
            value = json.loads(raw.decode("utf-8"))
        except Exception:
            return None
        return value if isinstance(value, dict) else None

    def acquire(self) -> "RunLock":
        if self._handle is not None:
            return self
        self.path.parent.mkdir(parents=True, exist_ok=True)
        handle = self.path.open("a+b", buffering=0)
        try:
            _lock_exclusive(handle)
        except OSError:
            prior = self.holder() or {}
            handle.close()
            raise RunLocked(
                f"{self.path}: held by pid {prior.get('pid')} since "
                f"{prior.get('started_utc')}") from None
        prior = self.holder()
        if prior and prior.get("loop_plan_id") not in (None, self.loop_plan_id):
            _unlock(handle)
            handle.close()
            raise StepError(
                "PLAN_ID_MISMATCH",
                f"{self.path} was opened under loop_plan_id "
                f"{prior.get('loop_plan_id')}")
        record = {
            "schema": LOCK_SCHEMA,
            "pid": self.pid,
            "started_utc": _stamp(self._clock()),
            "loop_plan_id": self.loop_plan_id,
        }
        handle.seek(0)
        handle.truncate(0)
        handle.write(custody.encoded(record))
        handle.flush()
        os.fsync(handle.fileno())
        self._handle = handle
        return self

    def release(self) -> None:
        """Drop the flock and clear the holder record.

        The lock file's contents are for the human reading a refusal - "held by
        pid N since T" - and a released lock whose file still names a pid tells
        that human the opposite of the truth (wave-1 integration decision 49).
        The flock is what excludes; the record is cleared inside it, before the
        handle is closed, so no second driver can read a stale holder.
        """

        handle, self._handle = self._handle, None
        if handle is None:
            return
        try:
            try:
                handle.seek(0)
                handle.truncate(0)
                handle.write(custody.encoded({
                    "schema": LOCK_SCHEMA,
                    "pid": None,
                    "started_utc": None,
                    "released_utc": _stamp(self._clock()),
                    "loop_plan_id": self.loop_plan_id,
                }))
                handle.flush()
                os.fsync(handle.fileno())
            except OSError:
                # A lock whose record could not be cleared is still released:
                # the flock is the exclusion, and the record is the note.
                pass
            _unlock(handle)
        finally:
            handle.close()

    def __enter__(self) -> "RunLock":
        return self.acquire()

    def __exit__(self, *_exc: Any) -> bool:
        self.release()
        return False


# --------------------------------------------------------------------------- #
# Records
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class StepRecord:
    """One receipt, and the file it was read from."""

    receipt: StepReceipt
    path: Path

    @property
    def index(self) -> int:
        return self.receipt.index

    @property
    def step_key(self) -> str:
        return self.receipt.step_key


@dataclass(frozen=True)
class ResumeAction:
    """What resume should do about one recorded step, in index order."""

    action: str
    index: int
    kind: str
    step_key: str
    code: str | None = None
    detail: str = ""

    @property
    def halting(self) -> bool:
        return self.action == "HALT"


@dataclass(frozen=True)
class StepOutcome:
    """What one call to :meth:`StepLedger.run_step` did."""

    status: str
    kind: str
    step_key: str
    index: int
    receipt: StepReceipt | None = None
    value: Any = None
    outputs: Mapping[str, str] = field(default_factory=dict)
    failure_code: str | None = None
    verified_line: str | None = None

    @property
    def ran(self) -> bool:
        """Did the body actually execute this time?"""

        return self.status != "SKIPPED"


# --------------------------------------------------------------------------- #
# One step in flight
# --------------------------------------------------------------------------- #

class StepHandle:
    """One step between its marker and its receipt.

    Also a context manager: leaving the block normally completes the step,
    leaving it by an exception records the failure and re-raises.
    """

    def __init__(self, ledger: "StepLedger", *, index: int, kind: str,
                 cycle: int | None, wave: str | None,
                 inputs: Mapping[str, str], step_key: str, spending: bool,
                 prior: StepRecord | None, replay: bool, skipped: bool,
                 started: datetime, deadline_seconds: int | None) -> None:
        self.ledger = ledger
        self.index = index
        self.kind = kind
        self.cycle = cycle
        self.wave = wave
        self.inputs: Mapping[str, str] = MappingProxyType(dict(inputs))
        self.step_key = step_key
        self.spending = spending
        self.prior = prior
        self.replay = replay
        self.skipped = skipped
        self.started = started
        self.started_utc = _stamp(started)
        self.deadline_seconds = deadline_seconds
        #: Named outputs the body records; digested on completion.
        self.outputs: dict[str, Any] = {}
        #: The commit a publication landed on, for the receipt.
        self.published_commit: str | None = None
        self._custody: CustodyReport = CustodyReport()
        self._elapsed_start = ledger.monotonic()
        self._finished = False

    # -- what the body may record ------------------------------------------ #

    def record_output(self, name: str, value: Any) -> None:
        """File one named output under its digest.

        The digest is taken **now**, not at completion: a value that cannot be
        digested used to escape :meth:`complete` as a bare ``TypeError`` from
        ``custody.digest``, outside every handler that writes a receipt, so a
        started step could end with no receipt at all - and, on a spending step,
        with its ``.open`` marker still standing and nothing to explain it.
        Raising here names the output that is wrong, at the call that recorded it.
        """

        if not isinstance(name, str) or not name:
            raise StepError("STEP_OUTPUTS_INVALID", "an output name is a non-empty string")
        _digest_of(value)
        self.outputs[name] = value

    def record_custody(self, findings: Iterable[Any]) -> CustodyReport:
        """File what ``custody.verify_pins`` found, through the one adapter."""

        self._custody = CustodyReport.from_findings(findings)
        return self._custody

    @property
    def custody(self) -> CustodyReport:
        return self._custody

    # -- the step deadline (design 4.4, layer 2) --------------------------- #

    @property
    def elapsed_seconds(self) -> float:
        return self.ledger.monotonic() - self._elapsed_start

    def check_deadline(self) -> None:
        """Raise :class:`StepTimeout` if this kind's deadline has passed.

        The loop does not pre-empt a body; nothing portable can.  A long body
        polls this, and completion checks it once more, so a step that overran
        is recorded as having overrun even when its body returned.
        """

        limit = self.deadline_seconds
        if limit is None:
            return
        elapsed = self.elapsed_seconds
        if elapsed > limit:
            raise StepTimeout(f"{self.kind} took {elapsed:.3f}s of {limit}s")

    # -- ending it ---------------------------------------------------------- #

    def complete(self, returned: Any = None) -> StepOutcome:
        """End the step successfully, or record why it could not end so."""

        if self._finished:
            raise StepError("STEP_RECEIPT_INVALID", f"step {self.index} already ended")
        try:
            if isinstance(returned, Mapping):
                # Digested before they are merged, so a returned mapping carrying
                # an undigestible value is refused with a receipt written rather
                # than at some later point with none.
                _digest_map(returned, "outputs")
                self.outputs.update(returned)
            self.check_deadline()
            outputs = _digest_map(self.outputs, "outputs")
        except LoopError as exc:
            self.fail_from(exc)
            raise
        if self.replay:
            return self.ledger._finish_replay(self, outputs, returned)
        receipt = self.ledger._write_receipt(
            self, status="COMPLETE", outputs=outputs, failure_code=None)
        return StepOutcome(status="COMPLETE", kind=self.kind, step_key=self.step_key,
                           index=self.index, receipt=receipt, value=returned,
                           outputs=outputs)

    def fail(self, code: str, detail: str = "") -> StepOutcome:
        """Record a failure the body determined, without raising."""

        return self._record_failure(code, detail, halted=code in CUSTODY_HALT_CODES)

    def halt(self, code: str, detail: str = "") -> StepOutcome:
        """Record a custody halt: sticky until acknowledged."""

        return self._record_failure(code, detail, halted=True)

    def fail_from(self, exc: BaseException) -> StepOutcome | None:
        """Record whatever a body raised, under a stable code."""

        if self._finished:
            return None
        status, code = _classify(exc)
        detail = getattr(exc, "detail", "") or str(exc)
        return self._record_failure(code, detail, halted=status == "HALTED")

    def _record_failure(self, code: str, detail: str, *, halted: bool) -> StepOutcome:
        if self._finished:
            raise StepError("STEP_RECEIPT_INVALID", f"step {self.index} already ended")
        status = "HALTED" if halted else "FAILED"
        try:
            outputs = _digest_map(self.outputs, "outputs") if self.outputs else {}
        except LoopError:
            # A failure receipt is never blocked by the outputs that failed.
            outputs = {}
        receipt = self.ledger._write_receipt(self, status=status, outputs=outputs,
                                             failure_code=code, detail=detail)
        return StepOutcome(status=status, kind=self.kind, step_key=self.step_key,
                           index=self.index, receipt=receipt, outputs=outputs,
                           failure_code=code)

    # -- context manager ---------------------------------------------------- #

    def __enter__(self) -> "StepHandle":
        return self

    def __exit__(self, kind: Any, exc: BaseException | None, _tb: Any) -> bool:
        if exc is not None:
            self.fail_from(exc)
        elif not self._finished:
            self.complete(None)
        return False


def _classify(exc: BaseException) -> tuple[str, str]:
    """The receipt status and stable code one raised exception is recorded as."""

    if isinstance(exc, custody.CustodyMismatch):
        return "HALTED", exc.code
    if isinstance(exc, LoopError):
        code = exc.code
        return ("HALTED" if code in CUSTODY_HALT_CODES else "FAILED"), code
    return "FAILED", "STEP_BODY_FAILED"


# --------------------------------------------------------------------------- #
# The ledger
# --------------------------------------------------------------------------- #

class StepLedger:
    """``<run_root>/steps/`` - the write-once record of every transition.

    ``run_root`` is the run directory ``run_paths(repo_root, run_id).run_root``,
    never the repository root and never ``steps/`` itself.  ``loop_plan_id`` is
    the frozen plan's identity: a receipt written under a different one is
    ``PLAN_ID_MISMATCH`` and the run does not resume.

    **``ledger_path`` names a ledger that already exists, and the loop never
    creates one.**  ``receipts.ledger_append`` refuses a missing ledger with
    ``LEDGER_NOT_FOUND`` unless ``create=True`` is passed, and this module never
    passes it: a driver pointed at the wrong path would otherwise start a second
    ``DECISION_LEDGER.md`` and mint ``REC-...-A`` into it while the real ledger
    stood at ``-U``, which is exactly the failure ``create=`` was added to name
    (wave-0 review S2).  So:

    * the **driver** passes ``ledger_path=`` explicitly, resolved from the run's
      own repository root - never ``receipts.DEFAULT_LEDGER_PATH``, which is
      ``None`` outside a source checkout;
    * a **test** that wants a ledger creates its temp file first (or calls
      ``receipts.ledger_append(..., create=True)`` itself) and then hands the
      path here;
    * ``ledger_path=None`` - the default - wires no ledger at all, and every
      ledger write this class would make is skipped rather than redirected.

    A ``LEDGER_NOT_FOUND`` out of :meth:`publish_step` is therefore a
    misconfigured driver, reported under its own name at the first publication
    rather than discovered later as a split ledger.
    """

    def __init__(self, run_root: str | os.PathLike[str], loop_plan_id: str, *,
                 timeouts: TimeoutsConfig | None = None,
                 ledger_path: str | os.PathLike[str] | None = None,
                 receipt_id: str | None = None,
                 clock: Callable[[], datetime] | None = None,
                 monotonic: Callable[[], float] | None = None) -> None:
        root = Path(run_root)
        self.run_root = root.resolve() if root.exists() else root
        self.loop_plan_id = str(loop_plan_id)
        self.timeouts = timeouts if timeouts is not None else TimeoutsConfig()
        self.ledger_path = None if ledger_path is None else Path(ledger_path)
        self.receipt_id = receipt_id
        self._clock = clock if clock is not None else _utc_now
        self._monotonic = monotonic if monotonic is not None else _monotonic
        parents = self.run_root.parents
        repo_root = parents[2] if len(parents) >= 3 else self.run_root
        #: Path spellings only.  ``repo_root`` is derived and never used here,
        #: so that ``NNNN-KIND.json[.open]`` has exactly one spelling in the
        #: package (the wave-0 convention).
        self.paths = RunPaths(repo_root=repo_root, run_id=self.run_root.name,
                              run_root=self.run_root)

    # -- clocks ------------------------------------------------------------- #

    def now(self) -> datetime:
        return self._clock()

    def monotonic(self) -> float:
        return self._monotonic()

    # -- reading the directory --------------------------------------------- #

    def records(self) -> tuple[StepRecord, ...]:
        """Every receipt, in index order.  Raises on a foreign or broken one."""

        directory = self.paths.steps
        if not directory.is_dir():
            return ()
        rows: list[StepRecord] = []
        for path in sorted(directory.iterdir()):
            match = _RECEIPT_NAME.fullmatch(path.name)
            if match is None or not path.is_file():
                continue
            try:
                raw = json.loads(path.read_bytes().decode("utf-8"))
            except Exception as exc:
                raise StepError("STEP_RECEIPT_INVALID", f"{path.name}: {exc}") from exc
            receipt = StepReceipt.from_dict(raw)
            if receipt.loop_plan_id != self.loop_plan_id:
                raise StepError("PLAN_ID_MISMATCH",
                                f"{path.name} was written under a different plan")
            if receipt.index != int(match.group(1)) or receipt.kind != match.group(2):
                raise StepError("STEP_RECEIPT_INVALID",
                                f"{path.name} disagrees with its own index or kind")
            rows.append(StepRecord(receipt=receipt, path=path))
        rows.sort(key=lambda row: (row.index, row.receipt.kind))
        return tuple(rows)

    def markers(self) -> tuple[tuple[int, str, Path], ...]:
        """Every ``.open`` marker on disk, in index order."""

        directory = self.paths.steps
        if not directory.is_dir():
            return ()
        found: list[tuple[int, str, Path]] = []
        for path in sorted(directory.iterdir()):
            match = _MARKER_NAME.fullmatch(path.name)
            if match is not None and path.is_file():
                found.append((int(match.group(1)), match.group(2), path))
        return tuple(sorted(found))

    def marker_body(self, path: Path) -> dict[str, Any]:
        try:
            value = json.loads(path.read_bytes().decode("utf-8"))
        except Exception:
            return {}
        return value if isinstance(value, dict) else {}

    def acknowledgements(self) -> tuple[dict[str, Any], ...]:
        """Every acknowledgement record under ``errata/``, oldest name first."""

        directory = self.paths.errata
        if not directory.is_dir():
            return ()
        out: list[dict[str, Any]] = []
        for path in sorted(directory.iterdir()):
            if not path.is_file() or not path.name.startswith("ACK-"):
                continue
            try:
                value = json.loads(path.read_bytes().decode("utf-8"))
            except Exception:
                continue
            if isinstance(value, dict):
                out.append(value)
        return tuple(out)

    def _acknowledged(self) -> set[tuple[str, int]]:
        return {(str(row.get("step_key")), int(row.get("index", -1)))
                for row in self.acknowledgements()}

    def next_index(self) -> int:
        """The next free step index: one past everything on disk."""

        used = [row.index for row in self.records()]
        used += [index for index, _kind, _path in self.markers()]
        return (max(used) + 1) if used else 1

    def step_key(self, kind: str, cycle: int | None = None, wave: str | None = None,
                 inputs: Mapping[str, Any] | None = None) -> str:
        """``sha256(canonical(loop_plan_id, kind, cycle, wave, inputs))``."""

        return StepReceipt.key(self.loop_plan_id, kind, cycle, wave,
                               _digest_map(inputs, "inputs"))

    def latest(self, step_key: str) -> StepRecord | None:
        """The highest-indexed receipt carrying ``step_key``."""

        rows = [row for row in self.records() if row.step_key == step_key]
        return rows[-1] if rows else None

    def completed(self, step_key: str) -> StepRecord | None:
        """The ``COMPLETE`` receipt for ``step_key``, if there is one."""

        rows = [row for row in self.records()
                if row.step_key == step_key and row.receipt.status == "COMPLETE"]
        return rows[-1] if rows else None

    def attempts_for(self, step_key: str) -> int:
        """How many publication attempts this ``step_key`` already recorded."""

        return sum(1 for row in self.records() if row.step_key == step_key
                   and row.receipt.kind in PUBLICATION_STEPS)

    def pending_publication(self) -> StepRecord | None:
        """The publication that is still ``PENDING``, if any (design O7)."""

        seen: dict[str, StepRecord] = {}
        for row in self.records():
            if row.receipt.kind in PUBLICATION_STEPS:
                seen[row.step_key] = row
        for row in sorted(seen.values(), key=lambda item: item.index):
            if (row.receipt.status == "FAILED"
                    and row.receipt.failure_code == "PUBLISH_PENDING"):
                return row
        return None

    def verified_line(self, step_key: str) -> str | None:
        """The ``VERIFIED`` line this publication filed beside its receipt."""

        row = self.completed(step_key)
        if row is None:
            return None
        sidecar = row.path.with_suffix("").with_suffix(VERIFIED_SUFFIX)
        try:
            return sidecar.read_bytes().decode("utf-8").strip()
        except OSError:
            return None

    # -- resume ------------------------------------------------------------- #

    def resume_plan(self) -> list[ResumeAction]:
        """What resume should do, in index order.  Pure: it writes nothing.

        The first :attr:`ResumeAction.halting` entry is what
        :meth:`guard` raises on, so the *earliest* unresolved thing is what
        blocks - a custody halt at step 3 outranks a stale marker at step 9.
        """

        acknowledged = self._acknowledged()
        rows = self.records()
        by_index = {row.index: row for row in rows}
        actions: list[ResumeAction] = []
        marker_indices: set[int] = set()

        for index, kind, path in self.markers():
            body = self.marker_body(path)
            key = str(body.get("step_key", ""))
            marker_indices.add(index)
            if (key, index) in acknowledged:
                continue
            sibling = by_index.get(index)
            detail = f"{path.name} was never resolved by a receipt"
            if sibling is not None:
                detail = (f"{path.name} survived a {sibling.receipt.status} receipt "
                          f"carrying {sibling.receipt.failure_code}")
            actions.append(ResumeAction(action="HALT", index=index, kind=kind,
                                        step_key=key, code="UNRESOLVED_STEP",
                                        detail=detail))

        pending = self.pending_publication()
        latest_by_key: dict[str, int] = {}
        for row in rows:
            latest_by_key[row.step_key] = row.index

        for row in rows:
            receipt = row.receipt
            if row.index in marker_indices:
                continue  # the marker above already speaks for this index
            if receipt.status == "HALTED":
                if (row.step_key, row.index) in acknowledged:
                    continue
                actions.append(ResumeAction(
                    action="HALT", index=row.index, kind=receipt.kind,
                    step_key=row.step_key, code=receipt.failure_code,
                    detail="a custody halt is sticky until it is acknowledged"))
                continue
            if pending is not None and row.index == pending.index:
                actions.append(ResumeAction(
                    action="HALT", index=row.index, kind=receipt.kind,
                    step_key=row.step_key, code="PUBLISH_PENDING",
                    detail="a pending publication blocks every successor step"))
                continue
            if receipt.status == "COMPLETE":
                action = "REPLAY" if receipt.replayable else "SKIP"
                actions.append(ResumeAction(action=action, index=row.index,
                                            kind=receipt.kind, step_key=row.step_key))
                continue
            if latest_by_key.get(row.step_key) == row.index:
                actions.append(ResumeAction(
                    action="RETRY", index=row.index, kind=receipt.kind,
                    step_key=row.step_key, code=receipt.failure_code,
                    detail="this step ended with a stable code and may be re-run"))
        actions.sort(key=lambda item: (item.index, 0 if item.halting else 1))
        return actions

    def blocking(self) -> ResumeAction | None:
        """The first halting resume action, or ``None`` when resume is clear."""

        for action in self.resume_plan():
            if action.halting:
                return action
        return None

    def guard(self, step_key: str | None = None) -> None:
        """Refuse to start anything while something is unresolved.

        ``step_key`` names the step about to begin, so that the *next attempt*
        of a pending publication is allowed through while every other step is
        refused - design O7's "blocks every successor step".
        """

        for action in self.resume_plan():
            if not action.halting:
                continue
            if action.code == "UNRESOLVED_STEP":
                raise UnresolvedStep(
                    f"{action.index:04d}-{action.kind}: {action.detail}",
                    step_key=action.step_key or None, index=action.index,
                    kind=action.kind)
            if action.code == "PUBLISH_PENDING":
                if step_key is not None and action.step_key == step_key:
                    continue
                raise PublishBlocked(
                    f"{action.index:04d}-{action.kind}: {action.detail}",
                    step_key=action.step_key)
            raise StickyHalt(action.code or "CUSTODY_MISMATCH",
                             f"{action.index:04d}-{action.kind}: {action.detail}",
                             step_key=action.step_key, index=action.index)

    # -- beginning and ending a step --------------------------------------- #

    def begin(self, kind: str, cycle: int | None = None, wave: str | None = None,
              inputs: Mapping[str, Any] | None = None, *,
              spending: bool | None = None) -> StepHandle:
        """Open one step: guard, derive the key, write the marker if spending.

        The returned handle says what to do with it: ``skipped`` when a
        ``COMPLETE`` receipt already covers this key and the kind is not
        replayable, ``replay`` when it is.
        """

        if kind not in STEP_KINDS:
            raise StepError("STEP_RECEIPT_INVALID", f"unknown step kind: {kind!r}")
        classified = kind in SPENDING_STEPS
        if spending is not None and bool(spending) is not classified:
            raise StepError(
                "STEP_CLASS_DISAGREEMENT",
                f"{kind} is {'' if classified else 'not '}a spending step")
        digests = _digest_map(inputs, "inputs")
        key = StepReceipt.key(self.loop_plan_id, kind, cycle, wave, digests)
        self.guard(key)

        prior = self.completed(key)
        replay = prior is not None and prior.receipt.replayable
        skipped = prior is not None and not replay
        index = prior.index if skipped else self.next_index()
        started = self.now()
        handle = StepHandle(
            self, index=index, kind=kind, cycle=cycle, wave=wave, inputs=digests,
            step_key=key, spending=classified, prior=prior, replay=replay,
            skipped=skipped, started=started,
            deadline_seconds=self.timeouts.step_seconds.get(kind))
        if not skipped and not replay and classified:
            self._write_marker(handle)
        return handle

    def run_step(self, kind: str, cycle: int | None, inputs: Mapping[str, Any] | None,
                 fn: Callable[[StepHandle], Any], spending: bool | None = None, *,
                 wave: str | None = None) -> StepOutcome:
        """Run one step under the ledger.  ``fn`` is called as ``fn(handle)``.

        A ``COMPLETE`` receipt for this key short-circuits: a replayable kind is
        re-run and must reproduce its digests, anything else is skipped without
        the body ever being entered.  Every failure is recorded as a receipt
        carrying its code and then re-raised - nothing is swallowed.
        """

        handle = self.begin(kind, cycle=cycle, wave=wave, inputs=inputs,
                            spending=spending)
        if handle.skipped:
            assert handle.prior is not None
            return StepOutcome(status="SKIPPED", kind=kind, step_key=handle.step_key,
                               index=handle.index, receipt=handle.prior.receipt,
                               outputs=dict(handle.prior.receipt.outputs_sha256))
        try:
            returned = fn(handle)
        except BaseException as exc:  # noqa: BLE001 - recorded, then re-raised
            handle.fail_from(exc)
            raise
        return handle.complete(returned)

    def publish_step(self, kind: str, repo: Any, paths: Iterable[Any], message: str, *,
                     ref: str | None = None, cycle: int | None = None,
                     wave: str | None = None,
                     inputs: Mapping[str, Any] | None = None,
                     publisher: Callable[..., Any] | None = None,
                     git: Any = None, sleep: Any = None,
                     now: Any = None) -> StepOutcome:
        """Publish for a step and file the ``VERIFIED`` line three ways.

        The line goes into a write-once sidecar beside the receipt, its digest
        into the receipt's ``outputs_sha256``, and its text into the ledger
        through :func:`receipts.ledger_append` - design 4.5's "into both the
        ledger and the step receipt", with the bytes kept where the receipt can
        name them.  A ``PENDING`` result is **returned**, not raised: it is a
        retryable state of the publication, and the guard blocks every successor
        step until a later attempt on this key lands.
        """

        if kind not in PUBLICATION_STEPS:
            raise StepError("STEP_CLASS_DISAGREEMENT",
                            f"{kind} is not one of {list(PUBLICATION_STEPS)}")
        run = publisher if publisher is not None else publish_module.publish
        key = self.step_key(kind, cycle, wave, inputs)
        attempt = self.attempts_for(key) + 1
        handle = self.begin(kind, cycle=cycle, wave=wave, inputs=inputs)
        if handle.skipped:
            assert handle.prior is not None
            return StepOutcome(status="SKIPPED", kind=kind, step_key=key,
                               index=handle.index, receipt=handle.prior.receipt,
                               outputs=dict(handle.prior.receipt.outputs_sha256),
                               verified_line=self.verified_line(key))
        try:
            result = run(repo, paths, message, ref, attempt=attempt, git=git,
                         sleep=sleep, now=now)
        except BaseException as exc:  # noqa: BLE001 - recorded, then re-raised
            handle.fail_from(exc)
            raise
        if not result.published:
            pending = result.pending
            reason = getattr(pending, "reason", "REMOTE_NOT_CONFIRMED")
            outcome = handle.fail("PUBLISH_PENDING",
                                  f"{reason} on attempt {attempt} of {result.ref}")
            return replace(outcome, value=result)

        line = str(result.verified_line)
        sidecar = self.paths.steps / f"{handle.index:04d}-{kind}{VERIFIED_SUFFIX}"
        try:
            custody.write_new(custody.fenced(self.run_root, sidecar),
                              line.encode("utf-8") + b"\n")
            handle.record_output(VERIFIED_OUTPUT_KEY,
                                 custody.sha256_bytes(line.encode("utf-8")))
            handle.published_commit = result.remote_commit
        except BaseException as exc:  # noqa: BLE001 - recorded, then re-raised
            handle.fail_from(exc)
            raise
        # The receipt is written BEFORE the ledger append. The push has landed
        # and the sidecar is on disk; a ledger that cannot be appended to is a
        # fact about the ledger, and leaving the step with no receipt for it left
        # the marker standing, made the next guard() raise UNRESOLVED_STEP with
        # nothing to explain it, made acknowledge() write an erratum saying the
        # body was not re-entered (which was false), and let the next begin()
        # re-publish the same paths at attempt 1.
        outcome = handle.complete(None)
        if self.ledger_path is not None:
            # create=False, deliberately: the loop never creates the repository's
            # ledger.  A missing path is LEDGER_NOT_FOUND and a misconfigured
            # driver, never a second ledger quietly started beside the real one.
            try:
                receipts.ledger_append(line, self.ledger_path)
            except LoopError as exc:
                # Its own erratum, appended to the run: the publication happened
                # and its receipt says so; what did not happen is the ledger line.
                # The refusal is then re-raised, because a driver pointed at the
                # wrong ledger must still be told at the first publication - what
                # changed is that it is now told with the receipt already written
                # and the marker already resolved, instead of leaving a spent
                # publication that the next resume would re-publish at attempt 1.
                self._write_run_erratum(
                    f"{handle.index:04d}-{kind}-LEDGER.md",
                    f"# The VERIFIED line is not in the ledger\n\n"
                    f"{kind} at step {handle.index:04d} published "
                    f"{result.remote_commit} and its receipt says so. The line "
                    f"could not be appended to {self.ledger_path}: {exc.code}: "
                    f"{exc.detail}\n\n"
                    f"The step receipt and the .verified sidecar carry the line "
                    f"verbatim; a reader of the ledger will not find it there. "
                    f"Append it by hand under the open receipt, or record why it "
                    f"stays absent. The publication itself is not in doubt.\n\n"
                    f"{line}\n")
                # The erratum goes under the RUN, not into the ledger: the ledger
                # is the thing that could not be written to.
                self._erratum(
                    f"{kind} published {result.remote_commit} and the VERIFIED line "
                    f"could not be appended to {self.ledger_path}: {exc.code}",
                    "The step receipt and the .verified sidecar carry the line.",
                    self.now())
                raise
        return replace(outcome, value=result, verified_line=line)

    # -- acknowledgement ---------------------------------------------------- #

    def unresolved_for(self, step_key: str
                       ) -> tuple[int, str, StepReceipt | None] | None:
        """The latest halt on ``step_key``: ``(index, code, receipt | None)``.

        Independent of whether an acknowledgement already covers it, so that
        write-once - and not the resume plan - is what makes an
        acknowledgement happen exactly once.
        """

        found: list[tuple[int, str, StepReceipt | None]] = []
        for index, _kind, path in self.markers():
            if str(self.marker_body(path).get("step_key", "")) == step_key:
                found.append((index, "UNRESOLVED_STEP", None))
        for row in self.records():
            if row.step_key == step_key and row.receipt.status == "HALTED":
                found.append((row.index,
                              row.receipt.failure_code or "CUSTODY_MISMATCH",
                              row.receipt))
        if not found:
            return None
        return max(found, key=lambda item: item[0])


    def acknowledge(self, step_key: str, reason: str) -> Path:
        """Clear one sticky halt, exactly once, and say why in the record.

        Design 4.4: "Resuming past a sticky halt requires ``--acknowledge
        <step_key> --reason "<text>"``, itself recorded."  The record is
        write-once under ``errata/``, so a second acknowledgement of the same
        halt is ``WRITE_ONCE_VIOLATION``; a later, *different* halt on the same
        key is a different record and is not covered by this one.
        """

        text = str(reason).strip()
        if not text:
            raise StepError("STEP_NOT_HALTED", "an acknowledgement must give a reason")
        target = self.unresolved_for(step_key)
        if target is None:
            raise StepError("STEP_NOT_HALTED",
                            f"{step_key} has nothing unresolved to acknowledge")
        index, code, receipt = target
        moment = self.now()
        narrative = (erratum_text(receipt, reason=text) if receipt is not None else
                     f"step {index:04d} halted with {code}; step_key {step_key}. "
                     "The step never resolved its open marker, so its body was not "
                     "re-entered. Acknowledged by the operator, who gave this "
                     f"reason: {text}")
        record = {
            "schema": ACK_SCHEMA,
            "step_key": step_key,
            "index": index,
            "failure_code": code,
            "reason": text,
            "acknowledged_utc": _stamp(moment),
            "erratum": narrative,
        }
        path = custody.fenced(self.run_root,
                             self.paths.errata / f"ACK-{index:04d}-{step_key}.json")
        custody.write_new(path, record)
        self._erratum(f"a halted step was acknowledged: {code}", narrative, moment)
        return path

    # -- writing ------------------------------------------------------------ #

    def _write_marker(self, handle: StepHandle) -> Path:
        path = custody.fenced(
            self.run_root,
            self.paths.step_path(handle.index, handle.kind, open_marker=True))
        custody.write_new(path, {
            "schema": MARKER_SCHEMA,
            "step_key": handle.step_key,
            "index": handle.index,
            "kind": handle.kind,
            "cycle": handle.cycle,
            "wave": handle.wave,
            "inputs_sha256": dict(handle.inputs),
            "started_utc": handle.started_utc,
            "spending": True,
        })
        return path

    def _resolve_marker(self, handle: StepHandle, *, failure_code: str | None) -> None:
        """Remove a spending step's marker when the outcome says what happened."""

        if not handle.spending:
            return
        if failure_code in MARKER_KEPT_CODES:
            return
        path = self.paths.step_path(handle.index, handle.kind, open_marker=True)
        try:
            path.unlink()
        except FileNotFoundError:
            pass

    def _write_receipt(self, handle: StepHandle, *, status: str,
                       outputs: Mapping[str, str], failure_code: str | None,
                       detail: str = "") -> StepReceipt:
        moment = self.now()
        receipt = StepReceipt.build(
            loop_plan_id=self.loop_plan_id, index=handle.index, kind=handle.kind,
            started_utc=handle.started_utc, cycle=handle.cycle, wave=handle.wave,
            inputs_sha256=dict(handle.inputs), status=status,
            outputs_sha256=dict(outputs), finished_utc=_stamp(moment),
            custody=handle.custody, failure_code=failure_code,
            published_commit=handle.published_commit)
        path = custody.fenced(self.run_root,
                              self.paths.step_path(handle.index, handle.kind))
        custody.write_new(path, receipt.as_dict())
        handle._finished = True
        self._resolve_marker(handle, failure_code=failure_code)
        if status == "HALTED":
            self._write_halt_erratum(receipt, detail, moment)
        return receipt

    def _finish_replay(self, handle: StepHandle, outputs: Mapping[str, str],
                       returned: Any) -> StepOutcome:
        """Compare a replayed step's outputs to the receipt already on record."""

        assert handle.prior is not None
        recorded = dict(handle.prior.receipt.outputs_sha256)
        fresh = dict(outputs)
        differing = sorted(set(recorded) ^ set(fresh))
        differing += sorted(name for name in set(recorded) & set(fresh)
                            if recorded[name] != fresh[name])
        if differing:
            detail = (f"{handle.kind} replayed differently at: "
                      + ", ".join(sorted(set(differing))))
            failure = StepNondeterministic(detail, step_key=handle.step_key,
                                           differing=sorted(set(differing)))
            # ``handle.index`` is already a fresh index (a replay never reuses
            # the one the recorded receipt occupies), so the mismatch is filed
            # as its own receipt beside the record it failed to reproduce.
            handle.replay = False
            handle._record_failure("STEP_NONDETERMINISTIC", detail, halted=False)
            raise failure
        handle._finished = True
        return StepOutcome(status="REPLAYED", kind=handle.kind,
                           step_key=handle.step_key, index=handle.prior.index,
                           receipt=handle.prior.receipt, value=returned,
                           outputs=fresh)

    # -- errata and the ledger ---------------------------------------------- #

    def _write_halt_erratum(self, receipt: StepReceipt, detail: str,
                            moment: datetime) -> Path:
        """The erratum stub design 4.4 requires under ``<run>/errata/``."""

        narrative = erratum_text(receipt)
        if detail:
            narrative += f" Detail: {detail}"
        path = custody.fenced(
            self.run_root,
            self.paths.errata / f"{receipt.index:04d}-{receipt.kind}-HALT.md")
        body = (f"# Halt at step {receipt.index:04d}-{receipt.kind}\n\n"
                f"{narrative}\n")
        try:
            custody.write_new(path, body.encode("utf-8"))
        except custody.WriteOnceViolation:
            pass
        self._erratum(f"a step halted: {receipt.failure_code}", narrative, moment)
        return path

    def _write_run_erratum(self, name: str, body: str) -> Path | None:
        """One erratum file under ``<run>/errata/``, write-once.

        The record for a fact that cannot reach the decision ledger - because
        the ledger is what failed. Nothing here raises: this is the last record
        written on a path that is already reporting a failure.
        """

        try:
            path = custody.fenced(self.run_root, self.paths.errata / name)
            custody.write_new(path, body.encode("utf-8"))
            return path
        except LoopError:
            return None

    def _erratum(self, defect: str, correction: str, moment: datetime) -> None:
        """Append an erratum to the decision ledger, when one is wired up."""

        if self.ledger_path is None or self.receipt_id is None:
            return
        receipts.erratum_receipt(self.receipt_id, defect, correction,
                                 ledger_path=self.ledger_path, moment=moment)


def _monotonic() -> float:
    return time.monotonic()
