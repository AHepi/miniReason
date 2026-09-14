"""Proof-of-concept for the existence pre-check in write_new.

Claim under test (docstring sentence): "The credential scan runs before
anything is created, so a refused write leaves no file and no parent directory
behind."

The scan-then-check order means the "leave nothing behind" promise fails when
the path is created between the credential scan and the existence check, using
only the module's own public functions (in-process adversary). The repair must
also keep "nothing was written or accepted" true on this path: the intruder's
file must be unlinked inside the except handler, or the refusal leaves the
very bytes it named on disk.
"""
from __future__ import annotations

import os
import sys
import tempfile
import threading
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import custody

INTRUDER = b"intruder-created content"
TRIGGER = b"clean payload the defender tries to write"


def main() -> None:
    with tempfile.TemporaryDirectory() as scratch:
        target = Path(scratch) / "record.bin"
        holds: list[threading.Event] = []
        real_names_in = custody.credential_names_in

        def adversarial_scan(raw: bytes):
            # The attack happens while the module is executing its own scan:
            # the file appears on disk between the scan and the existence check.
            hold = threading.Event()
            holds.append(hold)
            Path(target).write_bytes(INTRUDER)
            hold.wait(2.0)  # hold the scan a beat so the window is certain
            return real_names_in(raw)

        custody.credential_names_in = adversarial_scan
        try:
            defender = threading.Thread(
                target=lambda: _attempt(target), name="defender")
            defender.start()
            defender.join(5.0)
        finally:
            for hold in holds:
                hold.set()
            defender.join(5.0)
            custody.credential_names_in = real_names_in
        present = target.exists()
        content = target.read_bytes() if present else None
        print("RESULT", "PASS" if not present else "FAIL",
              "after a WriteOnceViolation raised on the TOCTOU path,",
              "the named path exists:", present,
              "| bytes there:", None if content is None else content[:40])
        print("RESULT NOTE the violation was raised; the intruder's bytes are what",
              "remains. An existence-first order would have raised before the",
              "intruder could exist; a fail-closed order raises only after it no",
              "longer exists.")


def _attempt(target: Path) -> None:
    try:
        custody.write_new(target, TRIGGER)
    except custody.WriteOnceViolation as exc:
        print("RESULT NOTE defender thread:", type(exc).__name__, exc.code)
    except Exception as exc:
        print("RESULT NOTE defender thread unexpected:", type(exc).__name__, exc)


if __name__ == "__main__":
    main()
