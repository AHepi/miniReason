"""Custody for the automated end-to-end harness loop - module ``W0-CUSTODY``.

Purpose
-------
Content-addressing of the files the loop pins, verification of those pins
against the tree that is supposed to still carry them, write-once record
creation that refuses to overwrite and refuses credential-bearing bytes, and
a path fence that keeps every write inside the run root.

Design of record
----------------
Implements the custody obligations of ``automated-loop-design.md``:

* **1.2 / D11** - the loop mints its own identity over ``config union pins``
  and touches no frozen plan, so it needs its own pin computation rather than
  a share of anyone else's.
* **4.2** - ``loop_plan_id = sha256(canonical(config union pins))``, where the
  pins are the sha256 of runner v2, ``graph_import_h005.py``,
  ``use_relation_h005.py``, ``contrast_triple_study.py``,
  ``provider_openai_compat.py``, ``endpoints.json``, every prompt template,
  ``obligations.json``, ``CEILING.md``, the standard body and each attached
  study's ``PLAN.md`` and ``material.json``.  :func:`pins` computes that map
  and :func:`fenced` protects the ``experiments/loops/<RUN-ID>/`` tree the
  design says the loop owns (occurrence trees are referenced, never written).
* **4.3** - the ``inputs_sha256`` / ``outputs_sha256`` / ``custody`` blocks of
  the write-once step receipt; :func:`digest` and :func:`sha256_bytes` are the
  identity helpers those fields are built from, and :func:`write_new` is the
  write-once discipline the receipts themselves are written under.
* **4.4** - *"Custody failure halts and records ... The loop never works
  around custody."*  Every check here either raises a :class:`CustodyMismatch`
  carrying a named code or reports one as a :class:`CustodyFinding`; nothing
  here repairs, retries, redacts or works around a mismatch.

Wave-plan entry ``W0-CUSTODY`` declares ``depends_on: []``.  The wave-0
integration added exactly one loop import - :class:`minireason.loop.types.LoopError`,
so that :class:`CustodyMismatch` is a ``LoopError`` and one ``except LoopError``
catches every wave-0 refusal - and ``types`` imports no sibling, so the module
graph stays acyclic and this module still pulls in nothing else of the loop.
It reaches ``minireason.provider_openai_compat`` lazily and optionally, so it
stays importable on its own.

Conventions reused rather than re-invented
------------------------------------------
* ``encoded`` / ``digest`` are byte-identical to
  ``tools/multicycle_commitment_study_multi_v2.py`` and
  ``src/minireason/provider_openai_compat.digest``.
* :func:`write_new` keeps the two drivers' shape - bytes verbatim, anything
  else canonical JSON; ``open('xb')``; ``fsync`` - and their
  ``CREDENTIAL_IN_OUTPUT`` spelling.
* The credential-name set comes from
  ``provider_openai_compat._secret_env_names()`` when the transport is
  importable, exactly as ``tools/contrast_triple_study.scanned_credential_envs``
  derives it, rather than from a name-shape scan of the environment.
* ``PATH_ESCAPES_RUN_ROOT`` mirrors ``graph_import_h005``'s
  ``PATH_ESCAPES_OCCURRENCE``; ``SOURCE_PIN_OUTSIDE_REPOSITORY`` and
  ``SOURCE_PIN_MISMATCH`` are runner v2's and ``contrast_triple_study``'s own
  spellings.

Deviations from the design, and why
-----------------------------------
1. :func:`verify_pins` **reports** rather than raises: its wave-plan type is
   ``-> list``, and section 4.4 requires the failure to be *named*.  The
   frozen-plan drivers compare the whole map at once
   (``sql_construction_study.py:206`` raises a bare ``RUNTIME_SOURCE_CHANGED``),
   which cannot say which file moved: the halt names the fact that *something*
   moved and the operator is left to find out what.  (This paragraph used to
   cite ``docs/lessons/operations.md`` E028 for that defect; E028 is about a
   frozen pin outliving the defect it froze and about when correcting a test is
   not a weakening, and records nothing of the kind.  The citation was wrong and
   is withdrawn rather than moved.)  A caller that wants the halt raises on a
   non-empty list; ``RUNTIME_SOURCE_CHANGED`` stays the aggregate name for that
   halt and is not emitted per path here.
2. Pin keys are canonicalised to POSIX separators before lookup.
   ``REC-20260913-I`` records a whole verification failing on path-key
   separator spelling alone while every sha256 matched exactly; a pin map
   frozen on one host must verify on another or it pins nothing.
3. :func:`fenced` refuses any ``..`` component outright, before resolution, and
   accepts an absolute path that is already inside the root.  A fence should
   not require the reader to normalise in their head, and the driver holds
   absolute run paths.
4. Names beyond the entry's five: the entry's purpose line names "digest
   helpers", which :func:`sha256_bytes`, :func:`sha256_path`, :func:`digest`
   and :func:`encoded` are; :class:`CustodyFinding` is the element type of
   ``verify_pins``' declared list; :class:`WriteOnceViolation` and
   :class:`CredentialInOutput` are subclasses of :class:`CustodyMismatch`, so
   the named interface still catches them, and they also inherit the historical
   ``FileExistsError`` / ``ValueError`` spellings the two drivers raise.
5. Sticky-until-acknowledged halt semantics are **not** here.  Section 4.4
   assigns them to the step ledger (``W1-STEPS``:
   ``ledger.acknowledge(step_key, reason)``).  This module supplies only the
   named code a halt records.
6. :func:`write_new` returns ``None``, matching both drivers.  It does not
   fence: the signature carries no root, so a caller writing under the run
   root passes ``fenced(run_root, relative)``.

Underspecified signatures, resolved the simplest way
----------------------------------------------------
* ``verify_pins(plan, repo)`` - ``plan`` is the loaded plan *body* and the map
  it checks is ``plan["pins"]`` (:data:`PIN_KEY`), the same key section 4.2
  folds into ``loop_plan_id``.  A bare ``{path: sha256}`` mapping is **not**
  accepted in its place: a plan body whose values all happened to be strings
  would be verified as a pin map, which is the sort of silent misreading this
  module exists to refuse.  ``repo`` is the tree the pins are re-read from.
* ``pins(repo, paths)`` - ``paths`` are repository-relative (an absolute path
  already inside ``repo`` is accepted and keyed relative to it).  A pinned file
  that lives outside any repository tree - the transport module resolved
  through ``PYTHONPATH``, say - is hashed by the caller with
  :func:`sha256_path` and merged into the map, as
  ``contrast_triple_study.check_transport_pins`` already does.
* ``write_new(path, value)`` - ``value`` is ``bytes`` (written verbatim) or any
  JSON value (written through :func:`encoded`).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

from minireason.loop.types import LoopError

__all__ = [
    "CustodyMismatch",
    "CredentialInOutput",
    "WriteOnceViolation",
    "CustodyFinding",
    "CUSTODY_CODES",
    "PIN_KEY",
    "ALWAYS_SCANNED_ENVS",
    "MIN_CREDENTIAL_LENGTH",
    "sha256_bytes",
    "sha256_path",
    "encoded",
    "digest",
    "scanned_credential_envs",
    "credential_names_in",
    "fenced",
    "write_new",
    "pins",
    "verify_pins",
]


#: Every code this module can name.  A halt records one of these; the operator
#: page (``W6-DOC``) lists them.  ``RUNTIME_SOURCE_CHANGED`` is deliberately
#: absent: it is the aggregate name a *caller* uses for a non-empty
#: :func:`verify_pins` result, not a per-path finding (deviation 1).
CUSTODY_CODES: tuple[str, ...] = (
    "CREDENTIAL_IN_OUTPUT",
    "CREDENTIAL_SCAN_INCOMPLETE",
    "PATH_ESCAPES_RUN_ROOT",
    "PATH_NOT_RESOLVABLE",
    "PIN_MAP_MISSING",
    "RECORD_NOT_SERIALISABLE",
    "RECORD_WRITE_FAILED",
    "SOURCE_PIN_MALFORMED",
    "SOURCE_PIN_MISMATCH",
    "SOURCE_PIN_MISSING",
    "SOURCE_PIN_NOT_A_FILE",
    "SOURCE_PIN_OUTSIDE_REPOSITORY",
    "WRITE_ONCE_VIOLATION",
)

#: The key :func:`verify_pins` reads a pin map out of a plan body under.
PIN_KEY = "pins"

#: Credential-bearing environment variable NAMES that are scanned whatever the
#: transport says.  Names only; no value is ever stored, returned or logged.
ALWAYS_SCANNED_ENVS: tuple[str, ...] = ("DEEPSEEK_API_KEY", "OLLAMA_API_KEY")

#: A value shorter than this is not searched for.  Equal to the transport's own
#: ``provider_openai_compat._MIN_SECRET_LENGTH``; a test pins that they agree.
#: A one-character placeholder in a key variable occurs in almost every record
#: by accident and would refuse unrelated writes.
MIN_CREDENTIAL_LENGTH = 8

#: The pin-value shape, anchored with ``\Z`` and applied with ``fullmatch``.
#: ``$`` matches before a trailing newline, so ``"<64 hex>\n"`` used to pass this
#: gate and be reported as ``SOURCE_PIN_MISMATCH`` - a statement about the tree
#: that was not true; the tree was fine and the pin was malformed. The same
#: bytes are ``PIN_INVALID`` in :mod:`minireason.loop.types`, and a test asserts
#: the two modules partition one key space the same way.
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")

def _pin_key_is_canonical(text: str) -> bool:
    """Whether a **plan's** pin key is spelled the one way a plan may spell it.

    ``types.loop_plan_id`` refuses an absolute key, a trailing slash, a ``.``
    component and a whitespace-padded component, and folds nothing: a key it
    refuses is a key no plan of this loop carries, so reading one here would be
    answering a question about a plan that was never frozen.

    Backslashes are the **one** difference from that key space, and deliberately
    so: deviation 2 and ``REC-20260913-I`` record a whole verification failing on
    separator spelling alone while every sha256 matched, and a pin map frozen on
    one host must verify on another or it pins nothing.  Such a map has no
    ``loop_plan_id`` of this loop's minting, so the looser reading here cannot
    admit a plan the identity would have refused; it can only read one that came
    from somewhere else.
    """

    normalised = text.replace("\\", "/")
    if not normalised or normalised.startswith("/") or normalised.endswith("/"):
        return False
    if normalised.startswith("~"):
        return False
    return all(part and part != "." and part == part.strip()
               for part in normalised.split("/"))


class CustodyMismatch(LoopError):
    """Custody failed under a named code; nothing was written or accepted.

    ``code`` is the stable erratum code (a member of :data:`CUSTODY_CODES`,
    which is a slice of ``types.FAILURE_CODES``); ``detail`` names the path or
    the environment variable names involved and never carries a credential
    value.  ``failure_code`` in ``tools/contrast_triple_study.py`` reads
    ``.code`` off an exception, so a halt receipt gets the code without parsing
    the message.

    A :class:`~minireason.loop.types.LoopError`, so one ``except LoopError``
    catches every wave-0 refusal.
    """

    def __init__(self, code: str, detail: str = "") -> None:
        LoopError.__init__(self, code, detail)


class CredentialInOutput(CustodyMismatch, ValueError):
    """A write was refused because its bytes carry a live credential.

    Refused, never redacted: ``docs/lessons/operations.md`` and section 4.5
    both require refusal.  Inherits ``ValueError`` so callers written against
    the drivers' ``ValueError('CREDENTIAL_IN_OUTPUT')`` keep working.
    """


class WriteOnceViolation(CustodyMismatch, FileExistsError):
    """A write was refused because the path already exists.

    Inherits ``FileExistsError`` so callers written against ``open('xb')``
    keep working, following ``graph_import_h005.OutRootRefused``'s precedent of
    keeping both historical spellings.
    """


@dataclass(frozen=True)
class CustodyFinding:
    """One named custody failure against one pinned path.

    ``expected`` is the pinned digest as the plan spells it; ``observed`` is
    what the tree holds now, or ``None`` where there is nothing to hash.
    """

    code: str
    path: str
    expected: str | None = None
    observed: str | None = None

    def __str__(self) -> str:
        text = f"{self.code}:{self.path}"
        if self.expected is not None and self.observed is not None:
            text += f" expected={self.expected} observed={self.observed}"
        return text

    def as_dict(self) -> dict[str, str | None]:
        """JSON-ready, for the step receipt's ``custody.checks`` list (4.3)."""

        return {"code": self.code, "path": self.path,
                "expected": self.expected, "observed": self.observed}


# ----------------------------------------------------------------- digests

def sha256_bytes(raw: bytes) -> str:
    """The sha256 of RAW, hex."""

    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: str | Path) -> str:
    """The sha256 of the bytes at PATH, read in byte mode.

    Byte mode only: ``docs/lessons/operations.md`` (OPS-20260914-LEDGERCRLF)
    records a text-mode read-and-write silently normalising line endings that
    were part of the published bytes.
    """

    return sha256_bytes(Path(path).read_bytes())


def encoded(value: Any) -> bytes:
    """The canonical record encoding, byte-identical to both drivers'."""

    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def digest(value: Any) -> str:
    """Identity digest of a JSON value; identical to ``provider_openai_compat.digest``.

    No wall clock, no ambient state: the same value always digests the same.
    """

    try:
        body = json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":")).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise CustodyMismatch(
            "RECORD_NOT_SERIALISABLE",
            f"{type(value).__name__} is not a JSON record: {exc}") from exc
    return sha256_bytes(body)


# ------------------------------------------------------------- credentials

def _provider_module() -> Any | None:
    """The transport module, or ``None`` when it is not importable.

    Imported lazily and optionally so that this module stays usable with
    ``depends_on: []`` and so that importing custody never drags the transport
    (and its endpoint registry) in as a side effect.
    """

    try:
        from minireason import provider_openai_compat
    except Exception:  # pragma: no cover - the transport is optional here
        return None
    return provider_openai_compat


def scanned_credential_envs() -> tuple[str, ...]:
    """Environment variable NAMES :func:`write_new` refuses to let into a record.

    Derived, never guessed: :data:`ALWAYS_SCANNED_ENVS` plus whatever the
    transport itself treats as credential-bearing (the endpoint registry's own
    ``key_env`` values and any name a caller registered).

    When the transport cannot be reached, this narrows to the two always-scanned
    names - and says so through :func:`credential_scan_is_complete`, which
    :func:`write_new` consults before it writes anything. It used to narrow in
    silence, so a credential held under a runtime-registered name went into a
    record that the scan had, truthfully, found nothing in.
    """

    names, _ = _credential_env_names()
    return names


def _credential_env_names() -> tuple[tuple[str, ...], bool]:
    """``(names, complete)``: the second says whether the transport answered."""

    names = set(ALWAYS_SCANNED_ENVS)
    module = _provider_module()
    if module is None:
        return tuple(sorted(names)), False
    try:
        names.update(module._secret_env_names())
    except Exception:  # pragma: no cover - a transport without the helper
        return tuple(sorted(names)), False
    return tuple(sorted(names)), True


def credential_scan_is_complete() -> bool:
    """Whether :func:`scanned_credential_envs` reached the transport's own list.

    ``False`` means the scan knows only :data:`ALWAYS_SCANNED_ENVS`, which is a
    scan that cannot answer the question :func:`write_new` asks it. PREFLIGHT
    asserts this, and :func:`write_new` refuses rather than write a record it
    could not check.
    """

    return _credential_env_names()[1]


def credential_names_in(raw: bytes) -> list[str]:
    """The NAMES of the credentials visible in RAW, sorted.  Never a value.

    Both renderings are searched - the raw value and the JSON-escaped one -
    because a record is encoded before it is written and a key containing a
    quote or a backslash would otherwise never match its own raw form.

    **UTF-8 renderings only.**  RAW is decoded as UTF-8 (with surrogate escape)
    and the credential's own ``str`` value is searched for in the result: a
    record that carried a credential base64-encoded, UTF-16-encoded, split
    across two fields or compressed would not match, and this function would
    truthfully report nothing.  It is a scan for the accident - a key echoed
    into a record - not a defence against a party trying to smuggle one out.
    """

    text = bytes(raw).decode("utf-8", "surrogateescape")
    hit: set[str] = set()
    for name in scanned_credential_envs():
        value = os.environ.get(name) or ""
        if len(value) < MIN_CREDENTIAL_LENGTH:
            continue
        if value in text or json.dumps(value)[1:-1] in text:
            hit.add(name)
    module = _provider_module()
    if module is not None:
        try:
            hit.update(module.redact_with_names(text)[1])
        except Exception:  # pragma: no cover - a transport without the helper
            pass
    return sorted(hit)


# ------------------------------------------------------------------ fence

def fenced(root: str | Path, path: str | Path) -> Path:
    """Check PATH is inside ROOT, and return it as a path under the resolved root.

    Accepts a root-relative path, ``''``/``'.'`` for the root itself, and an
    absolute path that is already inside the root.  Refuses any ``..``
    component outright, and refuses a path that **resolves** outside the root -
    which is what catches an intermediate symlink pointing away.  The path need
    not exist: this is the gate a write goes through before it is created.

    What comes back is the coordinate **as the caller named it**, under the
    resolved root - not the fully resolved path.  The two differ exactly when a
    symlink stands at the coordinate itself, and that is a custody event for
    :func:`write_new` to refuse rather than something for this function to
    silently follow (see :func:`_unresolved_inside`).

    A relative ROOT is resolved against the current working directory.
    """

    root_path = Path(root)
    candidate = Path(path)
    text = str(path)
    if any(part == ".." for part in candidate.parts):
        raise CustodyMismatch("PATH_ESCAPES_RUN_ROOT", text)
    if candidate.is_absolute():
        target = candidate
    elif text in ("", "."):
        target = root_path
    else:
        target = root_path / candidate
    resolved_root = _resolved(root_path, str(root))
    resolved = _resolved(target, text)
    if resolved != resolved_root and resolved_root not in resolved.parents:
        raise CustodyMismatch("PATH_ESCAPES_RUN_ROOT", text)
    return _unresolved_inside(root_path, resolved_root, candidate, text, resolved)


def _unresolved_inside(root_path: Path, resolved_root: Path, candidate: Path,
                       text: str, resolved: Path) -> Path:
    """The coordinate as the caller named it, under the resolved root.

    The escape check above **resolves**, because that is what catches an
    intermediate symlink pointing away.  What comes back does not, because a
    caller writing to ``steps/0001-SEND.json`` means that name: returning the
    resolved path handed :func:`write_new` a path with no symlink left in it,
    and the documented pairing ``write_new(fenced(root, rel), value)`` then
    wrote *through* a link planted at the coordinate - the record landing under
    a name nobody asked for, and the true owner of that name refused as spent
    ever after.  A link at the coordinate is now :func:`write_new`'s to see.
    """

    if text in ("", "."):
        return resolved_root
    if not candidate.is_absolute():
        return resolved_root.joinpath(candidate)
    for base in (resolved_root, root_path):
        try:
            return resolved_root.joinpath(candidate.relative_to(base))
        except ValueError:
            continue
    # An absolute path that is inside the root only once resolved: there is no
    # spelling of it under the root to hand back, so the resolved one it is.
    return resolved


def _resolved(path: Path, text: str) -> Path:
    """``Path.resolve`` with every operating-system refusal given a code.

    A NUL byte in a name is a ``ValueError``, a name past ``NAME_MAX`` an
    ``OSError``, a symlink cycle a ``RuntimeError``: none of them is a
    :class:`~minireason.loop.types.LoopError`, so a caller that catches one saw
    nothing - and a ``ValueError`` in particular reads as
    :class:`CredentialInOutput` to a caller that catches *that*.
    """

    try:
        return path.resolve()
    except (OSError, ValueError, RuntimeError) as exc:
        raise CustodyMismatch("PATH_NOT_RESOLVABLE",
                              f"{text}: {type(exc).__name__}") from exc


# ------------------------------------------------------------- write-once

def write_new(path: str | Path, value: Any) -> None:
    """Write VALUE to PATH once.  An existing path is a custody failure.

    ``bytes`` are written verbatim; anything else is written as canonical JSON
    through :func:`encoded` - the convention both drivers already use, so a
    ``str`` is written as a JSON string, not as raw text.  The credential scan
    runs before anything is created, so a refused write leaves no file and no
    parent directory behind.  The bytes are flushed and ``fsync``ed, **and the
    parent directory is ``fsync``ed after them**: a receipt that resolves a spent
    call must survive the process, and on a crash between the two an ``fsync`` of
    the file alone can leave durable bytes under a name that was never committed
    to the directory - a spent call with no receipt, which is the one failure this
    function exists to prevent.  A directory ``fsync`` that the platform refuses
    (Windows, and some network filesystems) is not a write failure and does not
    fail the write; the bytes are already durable.

    **The name appears only once the bytes are complete.**  The record is written
    to a sibling temporary, ``fsync``ed, and ``os.link``ed to its coordinate;
    see :func:`_link_into_place` for the two failures that pairing answers and
    the one it inherits (``EEXIST`` on the link is the write-once violation).

    Every refusal is a :class:`CustodyMismatch` with a code: an existing name or
    a parent that is a file is ``WRITE_ONCE_VIOLATION``, a value that is not a
    JSON record is ``RECORD_NOT_SERIALISABLE``, an operating-system refusal (a
    NUL in the name, a name past ``NAME_MAX``, a symlink cycle, a full disk) is
    ``RECORD_WRITE_FAILED``, and a credential scan that could not reach the
    transport's own name list is ``CREDENTIAL_SCAN_INCOMPLETE`` - a record this
    function could not check is a record it does not write.
    """

    if isinstance(value, (bytes, bytearray)):
        raw = bytes(value)
    else:
        try:
            raw = encoded(value)
        except (TypeError, ValueError) as exc:
            raise CustodyMismatch(
                "RECORD_NOT_SERIALISABLE",
                f"{type(value).__name__} is not a JSON record: {exc}") from exc
    target = Path(path)
    if not credential_scan_is_complete():
        raise CustodyMismatch(
            "CREDENTIAL_SCAN_INCOMPLETE",
            f"{target}: the transport's credential-name list is unavailable, so a "
            "credential held under a runtime-registered name would not be seen")
    names = credential_names_in(raw)
    if names:
        raise CredentialInOutput("CREDENTIAL_IN_OUTPUT", f"{target}:{','.join(names)}")
    try:
        taken = target.exists() or target.is_symlink()
    except (OSError, ValueError) as exc:
        raise CustodyMismatch("RECORD_WRITE_FAILED",
                              f"{target}: {type(exc).__name__}") from exc
    if taken:
        raise WriteOnceViolation("WRITE_ONCE_VIOLATION", str(target))
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
    except FileExistsError as exc:
        raise WriteOnceViolation("WRITE_ONCE_VIOLATION", str(target.parent)) from exc
    except (OSError, ValueError, RuntimeError) as exc:
        raise CustodyMismatch("RECORD_WRITE_FAILED",
                              f"{target}: {type(exc).__name__}") from exc
    _link_into_place(target, raw)
    _fsync_directory(target.parent)


def _link_into_place(target: Path, raw: bytes) -> None:
    """Write RAW to a sibling temporary, then ``link`` it to TARGET.

    Two failures the obvious ``open(target, "xb")`` cannot answer:

    * **A crash mid-write** left a truncated record under the target's name, and
      write-once forbids repairing it. The bytes are complete and ``fsync``ed
      before the name exists, so the name never addresses a half record.
    * **A symlink already standing at the coordinate.** ``fenced()`` returns the
      *resolved* path, so the documented pairing ``write_new(fenced(root, rel),
      value)`` had nothing left to see, and the record landed at the symlink's
      target while the true owner of that coordinate was later refused as spent.
      ``os.link`` never follows a symlink at its destination: an existing name,
      symlink included, is ``EEXIST`` and therefore a write-once violation.

    The temporary is opened ``O_EXCL|O_NOFOLLOW`` so it, too, cannot be aimed
    somewhere else, and is unlinked whatever happens.
    """

    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
    temporary = target.parent / f".{target.name}.{os.getpid()}.{id(raw):x}.part"
    try:
        descriptor = os.open(str(temporary), flags, 0o600)
    except FileExistsError as exc:  # pragma: no cover - a colliding temporary
        raise CustodyMismatch("RECORD_WRITE_FAILED", str(temporary)) from exc
    except (OSError, ValueError) as exc:
        raise CustodyMismatch("RECORD_WRITE_FAILED",
                              f"{temporary}: {type(exc).__name__}") from exc
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(str(temporary), str(target))
        except FileExistsError as exc:
            raise WriteOnceViolation("WRITE_ONCE_VIOLATION", str(target)) from exc
        except (OSError, ValueError) as exc:
            raise CustodyMismatch("RECORD_WRITE_FAILED",
                                  f"{target}: {type(exc).__name__}") from exc
    finally:
        try:
            os.unlink(str(temporary))
        except OSError:  # pragma: no cover - already gone
            pass


def _fsync_directory(directory: Path) -> None:
    """``fsync`` a directory so a newly created name is itself durable."""

    try:
        fileno = os.open(str(directory), getattr(os, "O_DIRECTORY", os.O_RDONLY))
    except OSError:  # pragma: no cover - platforms that cannot open a directory
        return
    try:
        os.fsync(fileno)
    except OSError:  # pragma: no cover - filesystems that refuse the call
        pass
    finally:
        os.close(fileno)


# --------------------------------------------------------------- pin maps

def _pin_key(entry: str | Path, root: Path) -> str:
    """The repository-relative POSIX key for one pinned path.

    Separators are canonicalised (deviation 2); an absolute path is accepted
    only when it is already inside ROOT and is returned relative to it.
    """

    text = str(entry).replace("\\", "/")
    candidate = Path(text)
    if candidate.is_absolute():
        try:
            return candidate.resolve().relative_to(root.resolve()).as_posix()
        except ValueError as exc:
            raise CustodyMismatch("SOURCE_PIN_OUTSIDE_REPOSITORY", text) from exc
    if text in ("", ".") or ".." in candidate.parts:
        raise CustodyMismatch("SOURCE_PIN_OUTSIDE_REPOSITORY", text)
    return PurePosixPath(text).as_posix()


def _pinned_path(root: Path, name: str) -> Path:
    """The fenced tree path for one pin key, as its own named failure."""

    try:
        return fenced(root, name)
    except CustodyMismatch as exc:
        raise CustodyMismatch("SOURCE_PIN_OUTSIDE_REPOSITORY", name) from exc


def pins(repo: str | Path, paths: Iterable[str | Path]) -> dict[str, str]:
    """Content-address every path in PATHS against the tree at REPO.

    Returns ``{repository-relative POSIX path: sha256 hex}`` in sorted key
    order, so two runs over the same files give byte-identical JSON and the
    map can be folded straight into ``loop_plan_id`` (4.2).

    Raises :class:`CustodyMismatch` - freezing a pin you cannot compute is the
    one thing a pin must never do - with ``SOURCE_PIN_OUTSIDE_REPOSITORY``,
    ``SOURCE_PIN_MISSING`` or ``SOURCE_PIN_NOT_A_FILE``.
    """

    root = Path(repo)
    out: dict[str, str] = {}
    for entry in paths:
        name = _pin_key(entry, root)
        path = _pinned_path(root, name)
        if not path.exists():
            raise CustodyMismatch("SOURCE_PIN_MISSING", name)
        if not path.is_file():
            raise CustodyMismatch("SOURCE_PIN_NOT_A_FILE", name)
        out[name] = sha256_path(path)
    return {name: out[name] for name in sorted(out)}


def _pin_map(plan: Mapping[str, Any]) -> Mapping[str, Any]:
    """The pin map a plan body carries under :data:`PIN_KEY`.

    Required, not guessed: a plan body whose every value happened to be a
    string would otherwise be read as a pin map and verified as one, which is
    the kind of silent misreading a custody module exists to refuse.  A caller
    holding a bare ``{path: sha256}`` map passes ``{"pins": map}``.
    """

    if not isinstance(plan, Mapping):
        raise CustodyMismatch("PIN_MAP_MISSING", type(plan).__name__)
    inner = plan.get(PIN_KEY)
    if not isinstance(inner, Mapping):
        raise CustodyMismatch("PIN_MAP_MISSING", PIN_KEY)
    return inner


def verify_pins(plan: Mapping[str, Any], repo: str | Path) -> list[CustodyFinding]:
    """Re-read every pinned file and report, by name, each one that moved.

    PLAN is the loop plan body; its :data:`PIN_KEY` map is what is checked,
    and a caller holding a bare ``{path: sha256}`` map passes ``{"pins":
    map}``.  Returns the findings sorted by ``(path, code, expected,
    observed)`` - the last two are in the key so two findings that agree on the
    first two still have one order; an empty list means every pinned file is
    still at its pinned bytes.  The caller decides what a non-empty list means -
    section 4.4 says it halts, records an erratum and never works around it.

    **A plan's pin key is held to the plan's key space.**  A key that
    ``types.loop_plan_id`` would refuse to write is named rather than quietly
    canonicalised and read: ``..`` and an absolute path outside the tree stay
    ``SOURCE_PIN_OUTSIDE_REPOSITORY`` (which says more than "malformed"), and an
    absolute path *inside* it, a trailing slash, a ``.`` component and a
    whitespace-padded component are ``SOURCE_PIN_MALFORMED``.  A backslash is the
    one spelling still canonicalised rather than refused; see
    :func:`_pin_key_is_canonical` for the receipt that says why.  :func:`pins`
    accepts every one of these *from a caller* and returns the one canonical
    form (deviation 2); it is the frozen map that is held tight.

    **A pin addresses bytes, not an inode.**  A pinned path that is a symlink is
    followed and its target's bytes are digested, with no finding: the pin says
    what the file must contain, and a tree that reaches those bytes through a
    link still contains them.  :func:`write_new` is the opposite case and treats
    a symlink at a *write* coordinate as a custody event, because there the
    question is which name the record was committed under.

    Pure in the sense the acceptance list means: it writes nothing, mutates
    neither argument, keeps no state between calls, and depends on nothing but
    ``(plan, tree)`` - so it is order-stable under any iteration order of the
    pin map.  Raises only :class:`CustodyMismatch` ``PIN_MAP_MISSING``, for a
    plan that carries no pin map at all, which is a caller error rather than a
    custody fact.
    """

    mapping = _pin_map(plan)
    root = Path(repo)
    findings: list[CustodyFinding] = []
    for raw_key in sorted(mapping, key=str):
        expected = mapping[raw_key]
        if not isinstance(raw_key, str):
            findings.append(CustodyFinding("SOURCE_PIN_MALFORMED", str(raw_key)))
            continue
        try:
            name = _pin_key(raw_key, root)
        except CustodyMismatch as exc:
            findings.append(CustodyFinding(exc.code, str(raw_key)))
            continue
        if not _pin_key_is_canonical(raw_key):
            findings.append(CustodyFinding("SOURCE_PIN_MALFORMED", str(raw_key)))
            continue
        if not (isinstance(expected, str) and _SHA256.fullmatch(expected)):
            findings.append(CustodyFinding("SOURCE_PIN_MALFORMED", name))
            continue
        try:
            path = _pinned_path(root, name)
        except CustodyMismatch as exc:
            findings.append(CustodyFinding(exc.code, name, expected))
            continue
        try:
            if not path.exists():
                findings.append(CustodyFinding("SOURCE_PIN_MISSING", name, expected))
            elif not path.is_file():
                findings.append(CustodyFinding("SOURCE_PIN_NOT_A_FILE", name, expected))
            else:
                observed = sha256_path(path)
                if observed != expected:
                    findings.append(
                        CustodyFinding("SOURCE_PIN_MISMATCH", name, expected, observed))
        except (OSError, ValueError, RuntimeError) as exc:
            # A name the operating system will not answer about is a finding,
            # not an escape: a pin the tree cannot be asked about is exactly
            # what this function is for.
            findings.append(CustodyFinding("PATH_NOT_RESOLVABLE", name, expected))
            del exc
    findings.sort(key=lambda finding: (finding.path, finding.code,
                                       finding.expected or "", finding.observed or ""))
    return findings
