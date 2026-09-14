"""write_new writes in place under the final name.  This probe kills the
process between the first half of the bytes and the second, and then asks what
the write-once discipline lets the next run do about the half-written record.

The kill is real: a forked child replaces Path.open with a handle whose write()
emits half the bytes, fsyncs, and calls os._exit(9).
"""
import _boot  # noqa: F401
import json
import os
import sys
import tempfile
from pathlib import Path

from minireason.loop import custody

RECORD = {"step_key": "0007-S7", "coordinate": "row-3#judge-b",
          "spent": True, "raw_ref": "blob:" + "9" * 40}


class TornHandle:
    """A file handle that writes half of what it is given, then dies."""

    def __init__(self, inner):
        self._inner = inner

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def write(self, raw):
        half = len(raw) // 2
        self._inner.write(raw[:half])
        self._inner.flush()
        os.fsync(self._inner.fileno())
        os._exit(9)          # the crash

    def flush(self):
        return self._inner.flush()

    def fileno(self):
        return self._inner.fileno()


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    target = root / "steps" / "0007-S7.json"
    whole = custody.encoded(RECORD)
    print("record would be", len(whole), "bytes")

    pid = os.fork()
    if pid == 0:
        real_open = Path.open

        def torn_open(self, *a, **k):
            return TornHandle(real_open(self, *a, **k))

        Path.open = torn_open
        try:
            custody.write_new(target, RECORD)
        except BaseException as exc:  # noqa: BLE001
            print("child raised", type(exc).__name__, exc)
        os._exit(0)

    _, status = os.waitpid(pid, 0)
    print("child exit status      :", os.WEXITSTATUS(status))
    print("file exists after crash:", target.exists())
    partial = target.read_bytes()
    print("bytes on disk          :", partial)
    print("is it the whole record :", partial == whole)
    try:
        json.loads(partial.decode("utf-8"))
    except ValueError as exc:
        print("json.loads(partial)    : ValueError:", exc)
    else:
        print("json.loads(partial)    : parsed")

    # what the next run can do about it
    try:
        custody.write_new(target, RECORD)
    except custody.CustodyMismatch as exc:
        print("re-write the record    :", exc.code, exc.detail)
    else:
        print("re-write the record    : WROTE")

    src = Path(custody.__file__).read_text(encoding="utf-8")
    print("os.link / os.replace / os.rename in custody.py:",
          [token for token in ("os.link", "os.replace", "os.rename") if token in src])
sys.stdout.flush()
