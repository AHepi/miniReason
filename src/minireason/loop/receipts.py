"""Ledger receipts, activity records and the cadence timer for the automated loop.

Purpose. This module is the loop's only writer of ``docs/DECISION_LEDGER.md`` and
its only caller of ``tools/repo_activity.py``. It mints a receipt id, appends a
receipt paragraph in the ledger's house style, brackets every repository act with
an activity record, and keeps the five-minute progress clock the repository's
operating rules require. It implements the automated end-to-end harness loop
design of record, section 4.5 ("Receipt, activity and publication automation")
and section 8 ("Pre-registration text for the ledger receipt"); module
``W0-RECEIPTS`` of the wave plan in section 7.

Three properties are load-bearing and are the reason this module exists at all.

* **Appends are byte mode and locked, and never rewrite or re-encode a byte that
  is already in the file.** ``docs/DECISION_LEDGER.md`` mixes LF and CRLF line
  endings (37 CRLF lines at the time of writing) and carries non-ASCII prose. A
  read-modify-write through a text handle would normalise both and would clobber
  a concurrent publisher's append. Every write here follows
  ``tools/repo_activity.append``'s discipline: ``open("ab", buffering=0)``
  (``"a+b"`` on Windows so locked reads use the same handle),
  an exclusive ``flock`` (``msvcrt.locking`` on Windows), ``seek(0, SEEK_END)``, a
  short-write loop over a ``memoryview``, ``flush``, unlock in ``finally``.
* **The receipt id is minted under the same lock that performs the append**, so
  two concurrent agents cannot mint the same letter. A caller that only wants to
  look at the next free id may call :func:`mint_receipt_id`, but only
  :func:`open_receipt` mints and writes atomically.
* **A receipt body carrying a registered credential is refused, never
  redacted.** The check is ``provider_openai_compat.redact_with_names``, the same
  scanner the transport uses, so the ledger and the wire agree about what a
  credential is. A refusal names the environment variable, never the value, and
  writes nothing.

Deviations from the design, each with its reason.

1. Section 4.5 says the id is minted "by scanning the ledger tail". This module
   scans the whole ledger under the lock instead. A fixed tail window can miss an
   earlier same-date id and mint a colliding letter; the file is ~0.5 MB, the read
   happens once per receipt, and correctness is worth the microseconds.
2. The design writes ``REC-<YYYYMMDD>-<letter>`` with a single letter and the
   ledger has never needed a second. Past ``Z`` this module continues ``AA``,
   ``AB``, ... (bijective base 26) rather than failing or wrapping, so a busy day
   cannot silently reuse ``A``. The letter sequence restarts at ``A`` on each new
   UTC date, which is what the 2026-09-14 block in the ledger does.
3. Section 8 shows its text as a Markdown blockquote. The quotation marks belong
   to the design document; the ledger's house form is unquoted paragraphs, so
   :func:`render_preregistration` emits it unquoted. Its bold paragraph headings,
   wording and order are preserved, and :data:`PREREGISTRATION_REQUIRED_SENTENCES`
   is asserted against the rendered text on every call.
4. The wave plan gives ``ledger_append(text)`` and ``activity(phase, action, why,
   goal, paths)`` without a ledger path or a decision id. Both are underspecified
   rather than fixed, so this module takes the simplest completion: an optional
   trailing ``ledger_path`` (defaulting to this checkout's ledger) and an optional
   ``decision`` keyword that falls back to the receipt this process last opened.
   The listed call shapes still work unchanged.
5. ``open_receipt``'s fields are the four AGENTS.md requires of every receipt —
   choice, reason, contribution, and pending state with evidence — plus an
   optional ``source_identity`` disclosure sentence, which is
   ``docs/lessons/operations.md`` line 20's rule (a changed repository-wide source
   digest must be disclosed, never silently edited into an old plan) given a
   place to live.
6. ``erratum_receipt`` is not named in the design's public interface; the task
   assigns it and the ledger's ``correction``/``erratum`` paragraphs are its house
   form. It appends; it never edits the receipt it corrects.
7. **A ledger that does not exist is refused unless ``create=True``.** ``open("ab")``
   creates silently, so a mistyped path or a wrong repository root used to succeed
   into a *second* ledger whose receipt letters restarted at ``A`` — the collision
   the id minting exists to prevent, arrived at from the other side. The code is
   ``LEDGER_NOT_FOUND``; ``ledger_append``, ``open_receipt`` and
   ``open_preregistration`` take ``create=``, and the follow-up forms never create.
8. **:data:`DEFAULT_REPO_ROOT` is found by walking up for
   ``tools/repo_activity.py``**, not by counting ``parents[3]``, and is ``None``
   when this module was not imported from a checkout — which is what an installed
   wheel is. ``None`` is a named refusal at the call (``LEDGER_NOT_FOUND`` /
   ``ACTIVITY_TOOL_MISSING``) rather than a write into whatever directory
   ``parents[3]`` happened to name. A driver should still pass ``ledger_path=`` and
   ``repo_root=`` explicitly (O3): these defaults are a convenience, not a
   mechanism.
9. **The transport is imported at the call, not at import.** Importing
   ``provider_openai_compat`` loads the whole endpoint registry from disk;
   ``custody`` avoids that deliberately and this module now does too. The scanner
   is the same function, and a test that registers a secret environment name still
   reaches it, because Python caches the module.

Nothing here publishes, commits or pushes: that is ``W0-PUBLISH``
(``loop/publish.py``). Nothing here reads or writes a credential.
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date as _date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Sequence

from minireason.loop.types import LoopError

if os.name == "nt":  # pragma: no cover - exercised on Windows only
    import msvcrt
else:
    import fcntl

__all__ = [
    "ACTIVITY_PHASES",
    "ACTIVITY_TOOL_RELATIVE",
    "C001_PLAN_ID",
    "CADENCE_DEADLINE_SECONDS",
    "CADENCE_WARN_SECONDS",
    "Cadence",
    "CadenceCheck",
    "CadenceMiss",
    "DEFAULT_AGENT",
    "DEFAULT_LEDGER_PATH",
    "DEFAULT_REPO_ROOT",
    "LEDGER_RELATIVE",
    "LedgerAppend",
    "PREREGISTRATION_REQUIRED_SENTENCES",
    "RECEIPT_ID_RE",
    "ReceiptError",
    "STAMP_FORMAT",
    "SecretInReceipt",
    "activity",
    "bracket",
    "checkpoint_receipt",
    "close_receipt",
    "current_receipt",
    "erratum_receipt",
    "ledger_append",
    "mint_receipt_id",
    "next_letter",
    "open_preregistration",
    "open_receipt",
    "outcome_receipt",
    "render_preregistration",
    "scan_receipt_ids",
    "set_current_receipt",
    "utc_stamp",
]

LEDGER_RELATIVE: str = "docs/DECISION_LEDGER.md"
ACTIVITY_TOOL_RELATIVE: str = "tools/repo_activity.py"


def _repository_root() -> Path | None:
    """The checkout this module was imported from, or ``None``.

    Found by walking up from this file for the marker that identifies *this*
    repository - ``tools/repo_activity.py``, the logger :func:`activity` shells -
    **beside a ``.git``**, and stopping at the first ``.git`` seen. A fixed
    ``parents[3]`` was correct in a source checkout and wrong in an installed
    wheel, where it names ``site-packages``' parent, so the default ledger became
    a *new* file in whatever directory that happened to be and two agents each
    minted ``REC-<date>-A`` into their own.

    The marker alone was not enough either. An installed wheel inside a virtual
    environment that happens to live under *some* checkout resolves to **that
    checkout**, and a default-path receipt then appends into a repository the
    caller never named. Two rules close it: a candidate must carry ``.git`` as
    well as the marker, and the walk stops at the first ``.git`` it meets (a
    nested checkout is not its parent), and any walk that passes through a
    ``site-packages`` directory answers ``None`` outright - an installed copy has
    no checkout of its own, whatever it happens to be sitting inside.

    ``None`` says the default is unresolved, which is a refusal a caller can
    read. A driver passes ``ledger_path=`` and ``repo_root=`` explicitly anyway;
    :func:`assert_explicit_paths` is the PREFLIGHT assertion that says so.
    """

    here = Path(__file__).resolve()
    for candidate in here.parents:
        if candidate.name == "site-packages" or candidate.name.endswith(".egg"):
            return None
        marker = (candidate / ACTIVITY_TOOL_RELATIVE).is_file()
        git = (candidate / ".git").exists()
        if marker and git:
            return candidate
        if git:
            # The first checkout boundary above this file, and it is not ours.
            return None
    return None


#: The checkout this module was imported from, or ``None`` outside one.
DEFAULT_REPO_ROOT: Path | None = _repository_root()

#: The ledger of that checkout, or ``None`` when there is no such checkout.
DEFAULT_LEDGER_PATH: Path | None = (
    None if DEFAULT_REPO_ROOT is None else DEFAULT_REPO_ROOT / LEDGER_RELATIVE
)
DEFAULT_AGENT: str = "auto_loop"


def assert_explicit_paths(ledger_path: Path | str | None,
                          repo_root: Path | str | None,
                          where: str = "PREFLIGHT") -> None:
    """Refuse a driver that leans on this module's defaults (O3).

    The defaults exist so an interactive call works inside the checkout; a run
    that writes receipts names its ledger and its repository root, because the
    default is a guess about where this file was imported from and a guess is
    not custody. PREFLIGHT calls this with what the driver will actually pass.
    """

    missing = [name for name, value in (("ledger_path", ledger_path),
                                        ("repo_root", repo_root)) if value is None]
    if missing:
        raise ReceiptError(
            "LEDGER_NOT_FOUND",
            f"{where} must pass {' and '.join(missing)} explicitly; the module "
            "default is where this file was imported from, not where the run is")

#: ``2026-09-14 09:12:33 UTC`` — the form most recent ledger paragraphs use.
STAMP_FORMAT: str = "%Y-%m-%d %H:%M:%S UTC"

#: ``REC-<YYYYMMDD>-<letters>``. Exposed so downstream waves parse rather than
#: re-invent the shape.
RECEIPT_ID_RE: re.Pattern[str] = re.compile(r"REC-(\d{8})-([A-Z]+)")
_RECEIPT_ID_BYTES_RE: re.Pattern[bytes] = re.compile(rb"REC-(\d{8})-([A-Z]+)")

#: AGENTS.md: the progress clock warns at 240 s and is overdue at 300 s. The
#: design's "``PROGRESS`` receipt at any step boundary past 240 s" is the warn
#: threshold; the five-minute rule is the deadline.
CADENCE_WARN_SECONDS: float = 240.0
CADENCE_DEADLINE_SECONDS: float = 300.0

ACTIVITY_PHASES: tuple[str, ...] = ("begin", "outcome", "event")

#: C001's frozen plan identity, quoted by section 8's "what it does not amend"
#: paragraph. Read from ``experiments/diagnostics/C001-contrast-triple/PLAN.md``;
#: it is quoted, never recomputed, and nothing here touches that study.
C001_PLAN_ID: str = "328b9452c66fed52203015c540652d3b8ad3107d44dece56b55ebe721da341c8"

#: Substrings that look like raw command text or a credential-bearing header.
#: The structural guarantee is stronger — :func:`activity` has no command
#: channel at all — but a caller can still paste a command into ``action``, and
#: AGENTS.md forbids "raw secret-bearing command text" in the activity log.
#: This is a scan for the **accident** - a command pasted into ``action``, a
#: header echoed into ``why`` - and not a defence against a caller trying to get
#: one past it. There is no such defence available here: the argument is free
#: text and a credential can be spelled in ways no substring list will see. The
#: structural guarantee is the one that holds: :func:`activity` has no command
#: channel, so nothing a caller writes is ever executed, and any *registered*
#: credential value is refused by name by :func:`_refuse_secret` whatever it is
#: embedded in.
_COMMAND_TEXT_MARKERS: tuple[str, ...] = (
    "$(", "`", "&&", "||", ">>", "2>&1",
    "Authorization", "authorization:", "Bearer ", "--header", "api_key=",
    "api-key:", "token=", "curl ", "export ",
    # Widened by the hardening pass: every one of these reached the activity
    # log untouched, and each is a way a credential is ordinarily written.
    "--api-key", "--apikey", "--key", "--token", "--password", "--secret",
    "x-api-key", "X-Api-Key", "X-API-KEY", "api_key:", "apikey=", "access_token",
    "wget ", "http://", "https://", "ssh ", "sudo ", "eval ",
)

#: ``scheme://user:password@host`` - a credential inside a URL, which no marker
#: above can see because both halves are the caller's own text.
_URL_CREDENTIAL = re.compile(r"[A-Za-z][A-Za-z0-9+.-]*://[^/\s]*:[^/\s@]+@")

#: Serialises appends inside this process as well as across processes. ``flock``
#: already excludes two open file descriptions in one process, but Windows'
#: ``msvcrt.locking`` does not exclude the locking process from itself, and an
#: in-process lock also makes the thread-contention test deterministic.
_APPEND_LOCK = threading.RLock()

#: Set while this thread is inside :func:`_append`. ``_APPEND_LOCK`` is an
#: ``RLock``, so a render callback that appended re-entered it happily and then
#: blocked on the *file* lock against itself - a deadlock with no refusal and no
#: receipt. The flag turns that into a named refusal.
_REENTRY = threading.local()

_CURRENT_RECEIPT: str | None = None
_CURRENT_LOCK = threading.Lock()


class ReceiptError(LoopError):
    """A refusal with a stable code. The detail never carries a credential.

    A :class:`~minireason.loop.types.LoopError`, so one ``except LoopError``
    catches every wave-0 refusal and every code here is listed in
    ``types.FAILURE_CODES``. The rendered message is unchanged.
    """

    def __init__(self, code: str, detail: str = "") -> None:
        LoopError.__init__(self, code, detail)


class SecretInReceipt(ReceiptError):
    """A registered credential was found in text bound for a record.

    Refused, not redacted: the design's rule for the ledger writer. ``names``
    holds the environment variable NAMES whose values matched, never a value.
    """

    def __init__(self, names: Sequence[str], where: str) -> None:
        super().__init__("SECRET_IN_RECEIPT", f"{where} carries {', '.join(names)}")
        self.names: tuple[str, ...] = tuple(names)
        self.where = where


@dataclass(frozen=True)
class LedgerAppend:
    """What one append did, in bytes, so a caller can prove it added only."""

    path: Path
    text: str
    receipt_id: str | None
    offset: int
    written: int
    sha256: str

    @property
    def end(self) -> int:
        return self.offset + self.written


@dataclass(frozen=True)
class CadenceCheck:
    """One look at the progress clock, at a stated moment."""

    now: datetime
    since: datetime
    elapsed_seconds: float
    deadline_utc: datetime
    state: str
    overdue_seconds: float

    @property
    def due(self) -> bool:
        """True once a progress receipt is owed (warn or overdue)."""

        return self.state != "ok"

    @property
    def missed(self) -> bool:
        return self.state == "overdue"


@dataclass(frozen=True)
class CadenceMiss:
    """A deadline that passed, recorded at the moment it was noticed.

    ``recorded_utc`` is the observation time and is never the deadline: a missed
    deadline is recorded truthfully and never backdated.
    """

    deadline_utc: datetime
    recorded_utc: datetime
    overdue_seconds: float

    def sentence(self) -> str:
        return (
            f"Cadence deadline {_stamp(self.deadline_utc)} was missed and is "
            f"recorded at the time it was noticed, {_stamp(self.recorded_utc)}, "
            f"{self.overdue_seconds:.0f} s overdue; it is not backdated."
        )


def utc_stamp(moment: datetime | None = None) -> str:
    """``moment`` in the ledger's stamp form. ``None`` means now, in UTC."""

    return _stamp(_utc(moment) if moment is not None else datetime.now(timezone.utc))


def _stamp(moment: datetime) -> str:
    return _utc(moment).strftime(STAMP_FORMAT)


def _utc(moment: datetime) -> datetime:
    if not isinstance(moment, datetime):
        raise ReceiptError("MOMENT_NOT_DATETIME", type(moment).__name__)
    if moment.tzinfo is None:
        raise ReceiptError("MOMENT_NOT_AWARE", "a naive datetime has no UTC meaning")
    return moment.astimezone(timezone.utc)


def _redact_with_names(text: str) -> tuple[str, Sequence[str]]:
    """``provider_openai_compat.redact_with_names``, imported at the call.

    Imported lazily so that importing this module does not drag the transport -
    and the twenty-four endpoints it loads from ``endpoints.json`` at *its* import -
    in as a side effect. ``custody`` already avoids that deliberately; two of six
    wave-0 modules did it anyway. The module object is the same one a test patches
    or registers an environment name on, because Python caches it.
    """

    from minireason.provider_openai_compat import redact_with_names

    return redact_with_names(text)


def _refuse_secret(text: str, where: str) -> str:
    redacted, names = _redact_with_names(text)
    if names:
        raise SecretInReceipt(names, where)
    del redacted
    return text


def _refuse_command_text(value: str, where: str) -> str:
    if any(character in value for character in "\r\n\t\x00"):
        raise ReceiptError("ACTIVITY_CONTROL_CHARACTER", where)
    lowered = value.casefold()
    for marker in _COMMAND_TEXT_MARKERS:
        if marker.casefold() in lowered:
            raise ReceiptError("ACTIVITY_RAW_COMMAND_TEXT", f"{where} contains {marker!r}")
    if _URL_CREDENTIAL.search(value):
        raise ReceiptError("ACTIVITY_RAW_COMMAND_TEXT",
                           f"{where} carries a URL with a credential in it")
    return value


def next_letter(existing: Iterable[str]) -> str:
    """The next free suffix after every suffix in ``existing``.

    ``A``..``Z``, then ``AA``, ``AB``, ... — bijective base 26, so no suffix is
    ever reused. An empty input gives ``A``.
    """

    highest = 0
    for suffix in existing:
        value = 0
        for character in suffix:
            if not ("A" <= character <= "Z"):
                raise ReceiptError("RECEIPT_SUFFIX_MALFORMED", suffix)
            value = value * 26 + (ord(character) - 64)
        highest = max(highest, value)
    value = highest + 1
    letters = ""
    while value:
        value, remainder = divmod(value - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def scan_receipt_ids(data: bytes, date_token: str) -> tuple[str, ...]:
    """Every receipt suffix already used on ``date_token`` in ``data``.

    Byte mode on purpose: the ledger is never decoded to find an id, so a stray
    undecodable byte cannot stop a receipt from being written.
    """

    wanted = date_token.encode("ascii")
    found = {
        match.group(2).decode("ascii")
        for match in _RECEIPT_ID_BYTES_RE.finditer(data)
        if match.group(1) == wanted
    }
    return tuple(sorted(found, key=lambda suffix: (len(suffix), suffix)))


def _date_token(moment: datetime) -> str:
    return _utc(moment).strftime("%Y%m%d")


def _next_id(data: bytes, date_token: str) -> str:
    return f"REC-{date_token}-{next_letter(scan_receipt_ids(data, date_token))}"


def mint_receipt_id(ledger_path: Path | str | None = DEFAULT_LEDGER_PATH,
                    *, today: _date | datetime | None = None) -> str:
    """The next free ``REC-<YYYYMMDD>-<letter>`` for ``today``.

    Advisory on its own: the value is correct at the moment of the locked read,
    but only :func:`open_receipt` mints and appends under one lock and is
    therefore collision-free under contention. Never call this from inside a
    render callback — the append lock is not re-entrant across threads.
    """

    if today is None:
        token = _date_token(datetime.now(timezone.utc))
    elif isinstance(today, datetime):
        token = _date_token(today)
    else:
        token = today.strftime("%Y%m%d")
    path = _ledger(ledger_path)
    with _APPEND_LOCK:
        return _next_id(_read_bytes(path), token)


def _ledger(ledger_path: Path | str | None) -> Path:
    """The ledger to append to, or a named refusal when there is no default."""

    if ledger_path is None:
        raise ReceiptError(
            "LEDGER_NOT_FOUND",
            "no ledger_path was given and this module was not imported from a "
            f"checkout carrying {ACTIVITY_TOOL_RELATIVE}, so there is no default",
        )
    return Path(ledger_path)


def _read_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        return b""


def _open_append(path: Path) -> Any:
    """Open ``path`` for unbuffered binary append. A documented test seam."""

    return path.open("a+b" if os.name == "nt" else "ab", buffering=0)


def _read_locked_bytes(path: Path, handle: Any) -> bytes:
    """Read under the append lock without a second Windows handle."""

    if os.name == "nt":
        handle.seek(0)
        return handle.read()
    return _read_bytes(path)


def _lock(handle: Any) -> None:
    if os.name == "nt":  # pragma: no cover - exercised on Windows only
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
    else:
        fcntl.flock(handle, fcntl.LOCK_EX)


def _unlock(handle: Any) -> None:
    if os.name == "nt":  # pragma: no cover - exercised on Windows only
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        fcntl.flock(handle, fcntl.LOCK_UN)


def _write_all(handle: Any, record: bytes) -> int:
    """Write every byte of ``record`` under the caller's lock.

    A short write is the reason this loop exists: closing after a partial write
    would leave a torn record, and retrying the whole buffer would duplicate the
    part that landed.
    """

    remaining = memoryview(record)
    written_total = 0
    while remaining:
        written = handle.write(remaining)
        if not written:
            raise ReceiptError("LEDGER_INCOMPLETE_WRITE", f"{written_total} of {len(record)} bytes")
        remaining = remaining[written:]
        written_total += written
    return written_total


def _separator(data: bytes, newline: bytes) -> bytes:
    """The bytes needed before a new paragraph, given what is already there.

    Only ever adds. The existing tail is inspected in both LF and CRLF forms so
    a CRLF-terminated ledger is not given a spurious blank line.
    """

    if not data:
        return b""
    if data.endswith(b"\n\n") or data.endswith(b"\r\n\r\n") or data.endswith(b"\n\r\n"):
        return b""
    if data.endswith(b"\n"):
        return newline
    return newline * 2


_Render = Callable[[bytes], "tuple[str, str | None]"]


def _append(path: Path, render: _Render, *, newline: bytes = b"\n",
            create: bool = False) -> LedgerAppend:
    """Mint (if the caller mints) and append, under one exclusive lock.

    ``render`` is handed the ledger's current bytes and returns
    ``(paragraph, receipt_id)``. It must not itself append.

    A ledger that does not exist is refused with ``LEDGER_NOT_FOUND`` unless the
    caller passes ``create=True``. Opening ``"ab"`` creates the file silently, so
    a mistyped path, a wrong repository root or a relative path resolved against
    the wrong working directory used to *succeed*: a second ledger appeared, its
    receipt letters restarted at ``A``, and nothing said so. Creating a ledger is
    a deliberate act and now looks like one.
    """

    if not create and not path.exists():
        raise ReceiptError(
            "LEDGER_NOT_FOUND",
            f"{path} does not exist; pass create=True to start a new ledger",
        )
    if not path.parent.is_dir():
        raise ReceiptError(
            "LEDGER_NOT_FOUND",
            f"{path.parent} is not a directory; a ledger is created inside an "
            "existing tree, never by making one",
        )
    if getattr(_REENTRY, "appending", False):
        raise ReceiptError(
            "LEDGER_APPEND_REENTERED",
            f"{path}: a render callback appended to the ledger it is rendering "
            "into; the append lock is held and the second append would wait on "
            "the first for ever")
    with _APPEND_LOCK:
        if not path.exists():
            # create=True. Clear the paragraph BEFORE the file is created, so a
            # refusal - an empty body, a credential - leaves no zero-byte ledger
            # behind for the next caller to mint ``A`` into.
            _cleared(render(b"")[0], path)
        _REENTRY.appending = True
        try:
            with _open_append(path) as handle:
                _lock(handle)
                try:
                    data = _read_locked_bytes(path, handle)
                    text, receipt_id = render(data)
                    text = _cleared(text, path)
                    payload = _separator(data, newline) + text.encode("utf-8") + newline
                    offset = len(data)
                    handle.seek(0, os.SEEK_END)
                    written = _write_all(handle, payload)
                    handle.flush()
                    # Read back while the lock is still held: a digest taken
                    # after it is released is a digest of whatever the next
                    # writer had already added, attributed to this append.
                    after = _read_locked_bytes(path, handle)
                finally:
                    _unlock(handle)
        finally:
            _REENTRY.appending = False
        if after[offset:offset + written] != payload:
            raise ReceiptError("LEDGER_APPEND_NOT_VERIFIED", str(path))
        return LedgerAppend(
            path=path, text=text, receipt_id=receipt_id, offset=offset,
            written=written, sha256=hashlib.sha256(after).hexdigest(),
        )


def _cleared(text: str, path: Path) -> str:
    """One paragraph, stripped and checked: non-empty, and carrying no secret."""

    text = str(text).strip("\n")
    if not text.strip():
        raise ReceiptError("LEDGER_EMPTY_PARAGRAPH", str(path))
    _refuse_secret(text, "ledger paragraph")
    return text


def ledger_append(text: str, ledger_path: Path | str | None = DEFAULT_LEDGER_PATH,
                  *, newline: bytes = b"\n", create: bool = False) -> LedgerAppend:
    """Append ``text`` as one ledger paragraph, in byte mode, under the lock.

    Existing bytes are never read back through a text handle, never re-encoded
    and never rewritten: the appended region begins at the previous end of file.
    A ledger that does not exist is refused with ``LEDGER_NOT_FOUND`` unless
    ``create=True`` says a new ledger is intended.
    """

    return _append(_ledger(ledger_path), lambda _data: (text, None),
                   newline=newline, create=create)


def set_current_receipt(receipt_id: str | None) -> None:
    """Remember the receipt this process is working under, for :func:`activity`."""

    global _CURRENT_RECEIPT
    with _CURRENT_LOCK:
        _CURRENT_RECEIPT = receipt_id


def current_receipt() -> str | None:
    with _CURRENT_LOCK:
        return _CURRENT_RECEIPT


def _clause(label: str, value: str | Sequence[str] | None) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        value = "; ".join(str(item) for item in value)
    body = _sentence(value)
    return f" {label}: {body}" if body else ""


def _sentence(text: str) -> str:
    cleaned = " ".join(str(text).split())
    if not cleaned:
        return ""
    return cleaned if cleaned[-1] in ".?!" else cleaned + "."


def _paths_clause(paths: Sequence[str] | None) -> str:
    if not paths:
        return ""
    rendered = ", ".join(f"`{path}`" for path in paths)
    return f" Paths: {rendered}."


def _receipt_paragraph(receipt_id: str, form: str, stamp: str, body: str) -> str:
    form = " ".join(str(form).split())
    if not form or ":" in form:
        raise ReceiptError("RECEIPT_FORM_MALFORMED", repr(form))
    return f"{receipt_id} {form} at {stamp}: {body.strip()}"


def open_receipt(*,
                 title: str | None = None,
                 choice: str | None = None,
                 why: str | None = None,
                 contribution: str | None = None,
                 evidence: str | Sequence[str] | None = None,
                 paths: Sequence[str] | None = None,
                 source_identity: str | None = None,
                 state: str = "pending",
                 body: str | None = None,
                 render: Callable[[str, str], str] | None = None,
                 form: str = "opened",
                 ledger_path: Path | str | None = DEFAULT_LEDGER_PATH,
                 moment: datetime | None = None,
                 set_current: bool = True,
                 create: bool = False) -> str:
    """Mint the next receipt id and append the opening paragraph. Returns the id.

    The id is minted from the ledger's own bytes under the same lock that writes
    the paragraph, so two agents opening a receipt at the same instant get
    different letters.

    Three mutually exclusive ways to say what the receipt says: the four house
    fields (``title``/``choice``/``why``/``contribution``, what AGENTS.md
    requires), a pre-composed ``body`` to which the ``REC-... opened at ...:``
    prefix is added, or a ``render(receipt_id, stamp)`` callable that returns the
    whole paragraph — which is how section 8's pre-registration text, whose own
    first line carries the id, is written.
    """

    house = {"title": title, "choice": choice, "why": why,
             "contribution": contribution, "evidence": evidence, "paths": paths,
             "source_identity": source_identity}
    given = [name for name, value in (("body", body), ("render", render)) if value is not None]
    if len(given) > 1:
        raise ReceiptError("RECEIPT_BODY_AMBIGUOUS", " and ".join(given))
    if given:
        # A caller that passes both a body (or a render) and the house fields is
        # saying two things; the house fields used to be dropped in silence, so
        # the receipt said the other one.
        also = sorted(name for name, value in house.items() if value not in (None, ()))
        if also:
            raise ReceiptError("RECEIPT_BODY_AMBIGUOUS",
                               f"{given[0]} with {', '.join(also)}")
    else:
        blank = [name for name in ("title", "choice", "why", "contribution")
                 if not str(house[name] or "").strip()]
        if blank:
            raise ReceiptError(
                "RECEIPT_FIELDS_MISSING",
                f"{', '.join(blank)}: title, choice, why and contribution are "
                "required without body or render, and none of them may be blank")
    if body is not None and not str(body).strip():
        raise ReceiptError("RECEIPT_FIELDS_MISSING", "body is blank")
    if isinstance(paths, (str, bytes, bytearray)):
        raise ReceiptError(
            "RECEIPT_FIELDS_MISSING",
            f"paths must be a sequence of paths, not a {type(paths).__name__} "
            "(which would be read one character per path)")
    when = _utc(moment) if moment is not None else datetime.now(timezone.utc)
    stamp = _stamp(when)
    token = _date_token(when)

    def _render(data: bytes) -> tuple[str, str | None]:
        receipt_id = _next_id(data, token)
        if render is not None:
            paragraph = render(receipt_id, stamp)
            suffix = receipt_id.rsplit("-", 1)[-1]
            if suffix not in scan_receipt_ids(str(paragraph).encode("utf-8"), token):
                # The letter is spent by the paragraph that carries it. A render
                # that omitted the id (or lower-cased it) spent nothing, and the
                # next caller minted the same id with no contention at all.
                raise ReceiptError(
                    "RECEIPT_ID_MALFORMED",
                    f"the rendered paragraph does not carry {receipt_id}, so the "
                    "id it was minted under is not spent")
            return paragraph, receipt_id
        if body is not None:
            composed = body
        else:
            composed = (
                _sentence(title or "")
                + _clause("Choice", choice)
                + _clause("Why", why)
                + _clause("Contribution", contribution)
                + _paths_clause(paths)
                + _clause("Source identity", source_identity)
                + _clause("Evidence", evidence)
                + _clause("State", state)
            )
        return _receipt_paragraph(receipt_id, form, stamp, composed), receipt_id

    appended = _append(_ledger(ledger_path), _render, create=create)
    receipt_id = appended.receipt_id or ""
    if set_current:
        set_current_receipt(receipt_id)
    return receipt_id


#: The latest moment a paragraph has been stamped with **in each ledger**, and
#: the lock that guards the table. The free follow-up seams take ``moment=`` from
#: the caller, so a paragraph could be stamped before the one above it in the
#: same file - a record reading as though the outcome preceded the opening. It is
#: keyed by ledger, not held once for the process: two ledgers are two records
#: and neither orders the other. Across processes the ledger's own order is the
#: record, and this table says nothing about it.
_LAST_MOMENT: dict[str, datetime] = {}
_MOMENT_LOCK = threading.Lock()


def _forward_only(path: Path, moment: datetime | None) -> datetime:
    """The moment to stamp with, refusing one earlier than this ledger's last."""

    when = _utc(moment) if moment is not None else datetime.now(timezone.utc)
    key = str(path)
    with _MOMENT_LOCK:
        previous = _LAST_MOMENT.get(key)
        if previous is not None and when < previous:
            raise ReceiptError(
                "CADENCE_BACKDATED",
                f"{_stamp(when)} is earlier than {_stamp(previous)}, the last "
                f"moment a paragraph of {path.name} was stamped with")
        _LAST_MOMENT[key] = when
    return when


def _follow_up(receipt_id: str, form: str, body: str,
               ledger_path: Path | str | None, moment: datetime | None) -> LedgerAppend:
    if not RECEIPT_ID_RE.fullmatch(str(receipt_id)):
        raise ReceiptError("RECEIPT_ID_MALFORMED", str(receipt_id))
    stamp = _stamp(_forward_only(_ledger(ledger_path), moment))
    paragraph = _receipt_paragraph(receipt_id, form, stamp, body)
    return _append(_ledger(ledger_path), lambda _data: (paragraph, receipt_id))


def outcome_receipt(receipt_id: str, outcome: str,
                    evidence: str | Sequence[str] | None = None,
                    *, form: str = "outcome",
                    paths: Sequence[str] | None = None,
                    ledger_path: Path | str | None = DEFAULT_LEDGER_PATH,
                    moment: datetime | None = None) -> LedgerAppend:
    """Append an outcome paragraph under an already-open receipt."""

    body = _sentence(outcome) + _paths_clause(paths) + _clause("Evidence", evidence)
    return _follow_up(receipt_id, form, body, ledger_path, moment)


def checkpoint_receipt(receipt_id: str, progress: str,
                       evidence: str | Sequence[str] | None = None,
                       *, cadence: CadenceCheck | CadenceMiss | None = None,
                       next_action: str | None = None,
                       ledger_path: Path | str | None = DEFAULT_LEDGER_PATH,
                       moment: datetime | None = None) -> LedgerAppend:
    """Append the five-minute substantive progress paragraph.

    ``moment`` is the time the paragraph is written, never the deadline it may
    have missed: a missed deadline is disclosed in the text and the stamp stays
    honest.
    """

    body = _sentence(progress)
    miss: CadenceMiss | None = None
    if isinstance(cadence, CadenceMiss):
        miss = cadence
    elif isinstance(cadence, CadenceCheck) and cadence.missed:
        # The clock's own recorded miss is what :meth:`Cadence.record_checkpoint`
        # hands over; a CadenceCheck passed directly carries the same three
        # numbers, so the miss is *read* from it and not invented with a second
        # clock reading. The one number this paragraph adds is its own: how late
        # the paragraph itself is, which is a different fact from how late the
        # deadline was noticed, and disclosing one as the other gave a reader two
        # numbers for one miss.
        miss = CadenceMiss(cadence.deadline_utc, cadence.now, cadence.overdue_seconds)
    if miss is not None:
        body += " " + miss.sentence()
        written = _utc(moment) if moment is not None else datetime.now(timezone.utc)
        late = (written - miss.deadline_utc).total_seconds()
        if abs(late - miss.overdue_seconds) >= 1.0:
            body += (f" This paragraph was written {late:.0f} s after that "
                     f"deadline.")
    body += _clause("Next", next_action) + _clause("Evidence", evidence)
    return _follow_up(receipt_id, "progress", body, ledger_path, moment)


def close_receipt(receipt_id: str, outcome: str,
                  evidence: str | Sequence[str] | None = None,
                  *, state_from: str = "pending",
                  ledger_path: Path | str | None = DEFAULT_LEDGER_PATH,
                  moment: datetime | None = None) -> LedgerAppend:
    """Append the closing paragraph: ``State pending -> **closed**.``"""

    body = f"State {state_from} -> **closed**. " + _sentence(outcome) + _clause("Evidence", evidence)
    return _follow_up(receipt_id, "closed", body, ledger_path, moment)


def erratum_receipt(receipt_id: str, defect: str, correction: str,
                    evidence: str | Sequence[str] | None = None,
                    *, form: str = "erratum",
                    ledger_path: Path | str | None = DEFAULT_LEDGER_PATH,
                    moment: datetime | None = None) -> LedgerAppend:
    """Append an erratum. It never rewrites the receipt it corrects."""

    body = (
        "Defect: " + _sentence(defect)
        + " Correction: " + _sentence(correction)
        + " This is appended rather than edited into the receipt above, because this"
        " ledger is append-only."
        + _clause("Evidence", evidence)
    )
    return _follow_up(receipt_id, form, body, ledger_path, moment)


_PREREGISTRATION_HEADER = (
    "**{receipt_id} opened at {stamp}: pre-register the automated end-to-end "
    "harness loop as a mechanism intervention with its own identity.**"
)

_PREREGISTRATION_BODY: tuple[str, ...] = (
    "**What this is.** A new instrument, not an observation and not an amendment. It "
    "automates three acts the published instruments reserve for root — the "
    "`use_relation_h005` reading cells, the C001 PLAN §8a contrast-register marks, and "
    "the continue/stop decision — together with the dispatch, import and publication "
    "that produce the material they read. It mints its own identity, `loop_plan_id = "
    "sha256(canonical(config ∪ pins))`, where the pins cover runner v2, the importer, "
    "the use-relation module, the contrast tool, the provider transport, `endpoints.json`, "
    "every prompt template, `obligations.json`, `CEILING.md` and the reading-rubric "
    "standard body. That identity is written to `experiments/loops/<RUN-ID>/plan.json` and "
    "published before the first provider call; the pre-registration timestamp precedes the "
    "first call and the record shows it.",

    "**What it does not amend.** It does not amend, reopen, supersede or reinterpret C001 "
    "(`plan_id " + C001_PLAN_ID + "`) or H005, and it registers no finding on either. "
    "C001's material, its recoding table, its endpoint set, its replicate count, its §8a "
    "reading rule and its claim ceiling are consumed exactly as frozen and are not edited, "
    "reformatted or re-hashed. Any change to a frozen value would mint a new `plan_id` for "
    "that study under its own §13 and is out of scope here.",

    "**Why a mechanism intervention rather than an experiment.** The object under change is "
    "the instrument, not the world: what this run produces is a table of guarded readings "
    "and a decision record, and its own claim ceiling states that a reading is a registered, "
    "attackable `judge`-role artifact and not a finding, not a merit assessment, and never "
    "FW5:628's witness of reason use. Success for this receipt is that the mechanism runs "
    "from a config to a closing receipt without a human step, publishes before it dispatches, "
    "resumes without re-sending a spent coordinate, and records honestly what it declined to "
    "read. It is not that any cell filled.",

    "**Pre-registered before first look, and unchangeable inside this chain.** The cycle "
    "budget and `max_calls`; the stopping rule with its guard rails and its five O/P clauses; "
    "`obligations.json` with the failed set O and the protected set P, pinned by sha256; the "
    "reading set; the seat assignment with families and `key_env`; the audit schedule, "
    "`JUDGE_ERR_MAX` and `STREAK_MAX`; the planted-flaw calibration set; the guard parameters "
    "including `TRIAL_PARAPHRASE_N` and `schema_repair_budget`; the reopen-reason list; and "
    "`CEILING.md`. Changing any of them after first look mints a new `loop_plan_id` and is a "
    "new pre-registration, not an amendment to this one.",

    "**Two declared narrowings of published instruments.** First, "
    "`use_relation_h005.ROOT_READING_VOCABULARY` is published as a suggestion a row may "
    "exceed and root may write outside; this run closes it to six values so the cell is "
    "machine-fillable, and routes anything outside to `unresolved:outside-vocabulary` with "
    "the text preserved. Second, where that instrument's banner says \"the reading is "
    "root's\", this run's table says the reading is a guarded judge-role artifact and root "
    "has not read it. Both narrowings are in the claim ceiling and in the rendered tables.",

    "**Not authorised under this receipt.** Any edit to `src/creib/**`, to "
    "`src/minireason/provider.py`, to `src/deepreason_core/**` (including the one-line "
    "`ProvenanceRole` addition, which is declined as vendoring drift against "
    "`AHepi/DeepReason@9607fba`), to any published occurrence, or to any frozen plan. Any "
    "force push, amend, rebase, reset or history rewrite. Any credential written into any "
    "file, log, receipt or commit. Any retry of a spent provider call. Any averaging or "
    "majority vote over a judge disagreement. Any aggregate, weighted, ranked or summed field "
    "over the four registers or over any reading.",

    "**Honest consequence, stated in advance.** The guard is strict enough that this run may "
    "return mostly `unresolved` and stop at the no-new-reading-changes clause having resolved "
    "little. That is the rule working and is reported as a result about the instrument's "
    "reach, never as evidence about the material. A run that reads few rows before the "
    "declared ceiling is reported as a resource boundary with the unreached rows named as "
    "unreached, never as unresolved by inquiry.",

    "Pending until PREFLIGHT reports planned calls equal to dispatched with zero provider "
    "calls, the dry-run acceptance gate is green, and the plan is published and verified.",
)

#: Sentences section 8 fixes. :func:`render_preregistration` asserts every one of
#: them against its own output, so a later edit cannot quietly drop one.
PREREGISTRATION_REQUIRED_SENTENCES: tuple[str, ...] = (
    "A new instrument, not an observation and not an amendment.",
    "It mints its own identity, `loop_plan_id = sha256(canonical(config ∪ pins))`",
    "It does not amend, reopen, supersede or reinterpret C001",
    "and it registers no finding on either.",
    "Success for this receipt is that the mechanism runs from a config to a closing receipt "
    "without a human step, publishes before it dispatches, resumes without re-sending a spent "
    "coordinate, and records honestly what it declined to read. It is not that any cell filled.",
    "Changing any of them after first look mints a new `loop_plan_id` and is a new "
    "pre-registration, not an amendment to this one.",
    "**Two declared narrowings of published instruments.**",
    "**Not authorised under this receipt.**",
    "That is the rule working and is reported as a result about the instrument's reach, never "
    "as evidence about the material.",
    "Pending until PREFLIGHT reports planned calls equal to dispatched with zero provider "
    "calls, the dry-run acceptance gate is green, and the plan is published and verified.",
)


def render_preregistration(receipt_id: str, stamp: str, *,
                           loop_plan_id: str | None = None,
                           run_id: str | None = None,
                           source_identity: str | None = None) -> str:
    """Section 8's pre-registration text, as one ledger receipt.

    ``loop_plan_id`` and ``run_id`` add a concrete-identity sentence when they
    are known; the section 8 wording, including its `<RUN-ID>` placeholder, is
    reproduced either way. ``source_identity`` renders the disclosure
    ``docs/lessons/operations.md`` line 20 requires when a repository-wide source
    digest has changed.
    """

    if not RECEIPT_ID_RE.fullmatch(str(receipt_id)):
        raise ReceiptError("RECEIPT_ID_MALFORMED", str(receipt_id))
    paragraphs = [_PREREGISTRATION_HEADER.format(receipt_id=receipt_id, stamp=stamp)]
    paragraphs.extend(_PREREGISTRATION_BODY)
    extra: list[str] = []
    if loop_plan_id:
        extra.append(f"The identity minted for this run is `loop_plan_id {loop_plan_id}`.")
    if run_id:
        extra.append(f"Its run directory is `experiments/loops/{run_id}/`.")
    if source_identity:
        extra.append("Source identity disclosed: " + _sentence(source_identity))
    if extra:
        paragraphs.insert(2, " ".join(extra))
    text = "\n\n".join(paragraphs)
    missing = [sentence for sentence in PREREGISTRATION_REQUIRED_SENTENCES if sentence not in text]
    if missing:
        raise ReceiptError("PREREGISTRATION_SENTENCE_MISSING", missing[0][:60])
    return text


def open_preregistration(ledger_path: Path | str | None = DEFAULT_LEDGER_PATH, *,
                         loop_plan_id: str | None = None,
                         run_id: str | None = None,
                         source_identity: str | None = None,
                         moment: datetime | None = None,
                         create: bool = False) -> str:
    """Mint the id and append section 8's pre-registration. Returns the id."""

    def _render(receipt_id: str, stamp: str) -> str:
        return render_preregistration(
            receipt_id, stamp, loop_plan_id=loop_plan_id, run_id=run_id,
            source_identity=source_identity,
        )

    return open_receipt(render=_render, ledger_path=ledger_path, moment=moment,
                        create=create)


def activity(phase: str, action: str, why: str, goal: str,
             paths: Sequence[str] | None = None, *,
             decision: str | None = None,
             agent: str = DEFAULT_AGENT,
             repo_root: Path | str | None = DEFAULT_REPO_ROOT,
             runner: Callable[..., Any] = subprocess.run,
             timeout: float = 30.0,
             check: bool = True) -> tuple[str, ...]:
    """Shell ``tools/repo_activity.py`` for one activity record. Returns its argv.

    The logger is shelled, never reimplemented: it owns the atomic locked append
    to ``docs/AGENT_ACTIVITY.jsonl`` and this module has no business owning a
    second implementation of it. No command is ever forwarded — the wrapper has
    no command channel at all, so no record can carry raw command text — and any
    field carrying a registered credential is refused rather than redacted.

    Every way the logger can fail carries a code from the table. A timeout used to
    propagate ``subprocess.TimeoutExpired`` unchanged, which is not a
    :class:`~minireason.loop.types.LoopError`, so ``except LoopError`` missed it
    and the step could name no ``failure_code``; it is now
    ``ACTIVITY_LOGGER_FAILED``. Under ``check`` a runner that returns no
    ``returncode`` at all is the same failure rather than a silent success.
    """

    if phase not in ACTIVITY_PHASES:
        raise ReceiptError("ACTIVITY_PHASE_UNKNOWN", str(phase))
    receipt_id = decision or current_receipt()
    if not receipt_id:
        raise ReceiptError("ACTIVITY_DECISION_MISSING", "no receipt is open in this process")
    if not RECEIPT_ID_RE.fullmatch(str(receipt_id)):
        # An activity record is addressed to a receipt; a decision id that is not
        # one addresses nothing, and the record is unreadable rather than wrong.
        raise ReceiptError("RECEIPT_ID_MALFORMED", str(receipt_id))
    fields = {"agent": agent, "decision": receipt_id, "action": action, "why": why, "goal": goal}
    for name, value in fields.items():
        _refuse_secret(str(value), f"activity {name}")
        _refuse_command_text(str(value), f"activity {name}")
    if isinstance(paths, (str, bytes, bytearray)):
        raise ReceiptError("ACTIVITY_PATH_INVALID",
                           f"paths must be a sequence, not a {type(paths).__name__}")
    listed = [str(path) for path in (paths or ())]
    for path in listed:
        _refuse_secret(path, "activity path")
        _refuse_command_text(path, "activity path")
        if path.startswith("-"):
            # ``--foo`` in the paths list is an OPTION to the logger, not a path:
            # it was forwarded into argv unescaped and the logger read it as one.
            raise ReceiptError("ACTIVITY_PATH_INVALID",
                               f"a path may not begin with '-': {path!r}")
        if not path.strip():
            raise ReceiptError("ACTIVITY_PATH_INVALID", "a path may not be blank")
    if repo_root is None:
        raise ReceiptError(
            "ACTIVITY_TOOL_MISSING",
            "no repo_root was given and this module was not imported from a "
            f"checkout carrying {ACTIVITY_TOOL_RELATIVE}",
        )
    tool = Path(repo_root) / ACTIVITY_TOOL_RELATIVE
    if not tool.is_file():
        raise ReceiptError("ACTIVITY_TOOL_MISSING", str(tool))
    argv = [
        sys.executable, str(tool),
        "--agent", agent, "--decision", receipt_id,
        "--action", action, "--why", why, "--goal", goal,
        "--phase", phase,
    ]
    if listed:
        argv.extend(["--paths", *listed])
    try:
        result = runner(argv, capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as expired:
        raise ReceiptError(
            "ACTIVITY_LOGGER_FAILED", f"timed out after {timeout} s"
        ) from expired
    except (OSError, subprocess.SubprocessError) as failure:
        # The TYPE only: an exception message from a process launch can carry the
        # argv, and the argv is the one thing this wrapper never logs.
        raise ReceiptError(
            "ACTIVITY_LOGGER_FAILED", f"the logger could not be run: "
            f"{type(failure).__name__}") from failure
    if check:
        returncode = getattr(result, "returncode", None)
        if returncode is None:
            raise ReceiptError("ACTIVITY_LOGGER_FAILED",
                               f"{type(result).__name__} carries no returncode")
        if returncode != 0:
            raise ReceiptError("ACTIVITY_LOGGER_FAILED", f"exit {returncode}")
    return tuple(argv)


@contextmanager
def bracket(action: str, why: str, goal: str, paths: Sequence[str] | None = None,
            **kwargs: Any) -> Iterator[None]:
    """Bracket one repository act with ``begin`` and ``outcome`` records.

    An exception is reported by type only; an exception message can carry
    anything, including a credential, and is never logged.
    """

    activity("begin", action, why, goal, paths, **kwargs)
    try:
        yield
    except BaseException as error:
        # The bracketed failure is the one the caller must see. A logger that
        # fails while recording it used to REPLACE it, so the act that went wrong
        # was reported as a logging problem; it now rides along on the original.
        try:
            activity("outcome", action,
                     f"{why}; interrupted by {type(error).__name__}", goal,
                     paths, **kwargs)
        except ReceiptError as logging_failure:
            _note(error, f"the outcome activity record was not written: "
                         f"{logging_failure.code}")
        raise
    activity("outcome", action, why, goal, paths, **kwargs)


def _note(error: BaseException, text: str) -> None:
    """Attach ``text`` to ``error.__notes__`` (PEP 678), on any Python."""

    try:
        error.add_note(text)                     # 3.11+
    except AttributeError:  # pragma: no cover - older interpreters
        notes = list(getattr(error, "__notes__", ()))
        notes.append(text)
        error.__notes__ = notes


class Cadence:
    """The five-minute progress clock.

    ``check(now)`` says whether a substantive receipt is owed. Only a receipt
    that was actually appended resets the clock (:meth:`acknowledge`), and the
    clock refuses to move backwards: a missed deadline is recorded at the moment
    it was noticed and is never backdated.
    """

    def __init__(self, started: datetime, *,
                 warn_seconds: float = CADENCE_WARN_SECONDS,
                 deadline_seconds: float = CADENCE_DEADLINE_SECONDS,
                 ledger_path: Path | str | None = DEFAULT_LEDGER_PATH) -> None:
        for name, value in (("warn_seconds", warn_seconds),
                            ("deadline_seconds", deadline_seconds)):
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise ReceiptError("CADENCE_THRESHOLD_INVALID",
                                   f"{name} is not a number")
            if value <= 0:
                # A clock whose deadline has already passed at zero elapsed
                # seconds is owed a receipt before the work it reports on.
                raise ReceiptError("CADENCE_THRESHOLD_INVALID",
                                   f"{name}={value} is not a positive interval")
        if deadline_seconds < warn_seconds:
            raise ReceiptError("CADENCE_THRESHOLDS_INVERTED",
                               f"{deadline_seconds} < {warn_seconds}")
        self.warn_seconds = float(warn_seconds)
        self.deadline_seconds = float(deadline_seconds)
        self.ledger_path = None if ledger_path is None else Path(ledger_path)
        self._since = _utc(started)
        self._seen = self._since
        self._misses: list[CadenceMiss] = []

    @property
    def since(self) -> datetime:
        """The moment the last acknowledged receipt was appended."""

        return self._since

    @property
    def deadline(self) -> datetime:
        return self._since + timedelta(seconds=self.deadline_seconds)

    @property
    def misses(self) -> tuple[CadenceMiss, ...]:
        return tuple(self._misses)

    def check(self, now: datetime) -> CadenceCheck:
        """Look at the clock at ``now``. A passed deadline is recorded once."""

        moment = self._advance(now)
        elapsed = (moment - self._since).total_seconds()
        deadline = self.deadline
        if elapsed >= self.deadline_seconds:
            state, overdue = "overdue", elapsed - self.deadline_seconds
            if not any(miss.deadline_utc == deadline for miss in self._misses):
                self._misses.append(CadenceMiss(deadline, moment, overdue))
        elif elapsed >= self.warn_seconds:
            state, overdue = "warn", 0.0
        else:
            state, overdue = "ok", 0.0
        return CadenceCheck(now=moment, since=self._since, elapsed_seconds=elapsed,
                            deadline_utc=deadline, state=state, overdue_seconds=overdue)

    def acknowledge(self, moment: datetime) -> None:
        """Reset the clock to ``moment``, the time a receipt was appended.

        Refuses a moment earlier than the last one already observed: that is
        what backdating a missed deadline would look like.
        """

        self._since = self._advance(moment)

    def record_checkpoint(self, now: datetime, receipt_id: str, progress: str,
                          evidence: str | Sequence[str] | None = None,
                          *, next_action: str | None = None) -> LedgerAppend:
        """Append a progress receipt stamped ``now`` and reset the clock to it."""

        check = self.check(now)
        miss = self._misses[-1] if check.missed and self._misses else None
        appended = checkpoint_receipt(
            receipt_id, progress, evidence, cadence=miss, next_action=next_action,
            ledger_path=_ledger(self.ledger_path), moment=check.now,
        )
        self.acknowledge(check.now)
        return appended

    def _advance(self, moment: datetime) -> datetime:
        value = _utc(moment)
        if value < self._seen:
            raise ReceiptError(
                "CADENCE_BACKDATED",
                f"{_stamp(value)} precedes {_stamp(self._seen)}",
            )
        self._seen = value
        return value
