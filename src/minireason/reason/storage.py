"""Short-path, UTF-8 custody for personal runs; no study publication machinery."""
from __future__ import annotations
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path


def read(path):
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return handle.read()


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def guard(path):
    if len(str(Path(path).resolve())) >= 200:
        raise ValueError("PATH_TOO_LONG")
    return Path(path)


def write(path, text, *, replace=False):
    path = guard(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    target = guard(path.with_name(path.name + ".tmp")) if replace else path
    with target.open("w" if replace else "x", encoding="utf-8", newline="") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    if read(target) != text:
        raise OSError("WRITE_VERIFICATION_FAILED")
    if replace:
        os.replace(target, path)
    if read(path) != text:
        raise OSError("WRITE_VERIFICATION_FAILED")


def put(path, value, *, replace=False):
    write(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", replace=replace)


def get(path):
    from .types import ReasonFailure
    try:
        return json.loads(read(path))
    except (ValueError, UnicodeError) as exc:
        raise ReasonFailure("RUN_INTEGRITY_ERROR", "Saved JSON is incomplete or invalid") from exc


@contextmanager
def run_lock(directory):
    path = guard(Path(directory) / ".lock")
    with path.open("a+", encoding="utf-8", newline="") as handle:
        handle.seek(0, 2)
        if handle.tell() == 0:
            handle.write("0")
            handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                raise RuntimeError("RUN_BUSY") from exc
        else:
            import fcntl
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                raise RuntimeError("RUN_BUSY") from exc
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)
