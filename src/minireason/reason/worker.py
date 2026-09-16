"""Isolated single-call worker. No retries and no stdout/stderr payloads."""
from __future__ import annotations
from pathlib import Path
import sys
import time
from .adapter import _execute, _read, _write
from .types import ReasonFailure

def main() -> int:
    spec, records = Path(sys.argv[1]), Path(sys.argv[2])
    try:
        prepared = _read(spec)
        if prepared.get("mode") != "live":
            raise ReasonFailure("CONFIG_ERROR", "Live worker received a non-live request")
        _execute(prepared, records)
        return 0
    except ReasonFailure as error:
        failure = {"code": error.code, "detail": error.detail, "recorded_epoch": time.time()}
    except BaseException:
        # An arbitrary transport exception can contain headers. Preserve a
        # classification only; never serialize exception values or traceback.
        failure = {"code": "TRANSPORT_OR_RESPONSE_ERROR", "detail": "Worker failed before completing its record", "recorded_epoch": time.time()}
    path = records / "worker-failure.json"
    if not path.exists():
        _write(path, failure)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
