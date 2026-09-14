"""Probe 6: write-once under a race, pin-key torture cases, odd payloads.

Claims under test:
* write_new's underlying discipline is open("xb") - two racing writers must
  produce exactly one success and one named WriteOnceViolation.
* custody docstring deviation 2: "Pin keys are canonicalised to POSIX
  separators before lookup."  Its justification is separator *spelling*, so
  the question is what other spellings of one key do.
* credential_names_in decodes arbitrary bytes with surrogateescape, so the
  scan must never crash on non-UTF-8 payload bytes.

Exercises: a threaded double-write; duplicate pins given under backslash vs
forward-slash spelling of one key; pins() and verify_pins() disagreeing over a
'./'-spelled key; non-UTF-8 payload bytes; a NUL-bearing credential value (the
environment cannot carry one - the probe prints that boundary itself); and a
pin-map key that is not a string at all. Uses only tempfile space. Prints
RESULT lines.
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


def result(ok: bool, *parts: object) -> None:
    print("RESULT", "PASS" if ok else "FAIL", *parts)


def race_write() -> None:
    with tempfile.TemporaryDirectory() as scratch:
        target = Path(scratch) / "once.bin"
        outcomes: list[str] = []
        barrier = threading.Barrier(2)

        def writer(tag: bytes) -> None:
            barrier.wait()
            try:
                custody.write_new(target, tag + b"-payload")
                outcomes.append(f"{tag.decode()}: wrote")
            except custody.WriteOnceViolation:
                outcomes.append(f"{tag.decode()}: refused")
            except Exception as exc:  # anything else is itself notable
                outcomes.append(f"{tag.decode()}: {type(exc).__name__} {exc}")
        threads = [threading.Thread(target=writer, args=(b"a",)),
                   threading.Thread(target=writer, args=(b"b",))]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        wrote = sum("wrote" in outcome for outcome in outcomes)
        refused = sum("refused" in outcome for outcome in outcomes)
        result(wrote == 1 and refused == 1 and target.exists()
               and target.read_bytes() in (b"a-payload", b"b-payload"),
               "racing writers:", sorted(outcomes), "| final bytes:", target.read_bytes())


def duplicate_spellings() -> None:
    with tempfile.TemporaryDirectory() as scratch:
        repo = Path(scratch)
        (repo / "src").mkdir()
        (repo / "src" / "a.py").write_bytes(b"alpha\n")

        # One key spelled with slashes and backslashes, given as TWO entries.
        frozen = custody.pins(repo, ["src\\a.py", "src/a.py"])
        single = custody.pins(repo, ["src/a.py"])
        result(frozen == single,
               "two spellings of one key collapse silently:",
               "entries in:", 2, "entries out:", len(frozen))

        # The same collapsing applied to './':
        findings = custody.verify_pins({"pins": {"./src/a.py": frozen["src/a.py"]}}, repo)
        result(findings == [],
               "verify_pins accepts the './' spelling pins() refuses:", findings)

        # Can a single pin map ever hold both spellings? Only via construction:
        plan = {"pins": {"src/a.py": frozen["src/a.py"],
                         "src\\a.py": "0" * 64}}
        findings = custody.verify_pins(plan, repo)
        result([f.code for f in findings] == ["SOURCE_PIN_MISMATCH"],
               "both spellings in one plan: key after canonicalisation is",
               [f.path for f in findings])


def odd_payloads() -> None:
    with tempfile.TemporaryDirectory() as scratch:
        # Non-UTF-8 payload bytes: the scan decodes with surrogateescape and
        # must not crash the scan; the write itself is clean.
        raw = b"\xb5\x27\x00\xfe not utf-8"
        try:
            hits = custody.credential_names_in(raw)
        except Exception as exc:
            result(False, "credential_names_in over non-UTF-8 bytes raised:",
                   type(exc).__name__, exc)
        else:
            result(hits == [], "credential_names_in over non-UTF-8 bytes returns:", hits)
        target = Path(scratch) / "raw-bytes.bin"
        custody.write_new(target, raw)
        result(target.read_bytes() == raw, "non-UTF-8 bytes written verbatim")

        # A credential value containing a NUL byte cannot be set through
        # os.environ at all (the interpreter refuses it):
        try:
            os.environ["DEEPSEEK_API_KEY"] = "probe-key\x00-tail"
        except ValueError as exc:
            print("RESULT NOTE os.environ refuses a NUL-bearing value itself:",
                  type(exc).__name__, "-", exc)

    # The escaped-form check: a credential containing a quote is searched both
    # raw and JSON-escaped.
    saved = os.environ.get("DEEPSEEK_API_KEY")
    try:
        quirky = 'quo"te-key-1234'
        os.environ["DEEPSEEK_API_KEY"] = quirky
        escaped_hits = custody.credential_names_in(b'{"k": "quo\\"te-key-1234"}')
        result("DEEPSEEK_API_KEY" in escaped_hits,
               "JSON-escaped rendering of a quote-bearing key is caught:", escaped_hits)
    finally:
        if saved is None:
            os.environ.pop("DEEPSEEK_API_KEY", None)
        else:
            os.environ["DEEPSEEK_API_KEY"] = saved


def nonstring_key() -> None:
    with tempfile.TemporaryDirectory() as scratch:
        try:
            custody.verify_pins({"pins": {7: "0" * 64}}, scratch)
        except custody.CustodyMismatch as exc:
            result(False, "non-string key raised CustodyMismatch code=", exc.code)
        except Exception as exc:
            result(type(exc).__name__ == "TypeError",
                   "non-string key:", type(exc).__name__, "(a finding is the escape, not the type)")
        else:
            result(False, "non-string key: verified with no complaint")


def main() -> None:
    race_write()
    duplicate_spellings()
    odd_payloads()
    nonstring_key()


if __name__ == "__main__":
    main()
