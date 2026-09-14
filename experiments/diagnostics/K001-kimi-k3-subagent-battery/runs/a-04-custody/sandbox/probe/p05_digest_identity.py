"""Probe 5: digest identity (wave-0 integration decision 7) and encoding forms.

Claims under test (notes/WAVE0-INTERFACE.md section 4):
  "custody.digest(v) == provider_openai_compat.digest(v) ==
   sha256_hex(canonical_json(v)), and canonical_json(v) is byte-identical to
   the compact json.dumps that custody.digest hashes.  custody.encoded is
   deliberately a *different* encoding (the drivers' record form) that
   round-trips to a value the three digests agree on."

Exercises that fixture claim directly, plus the non-ASCII character the
compact identity form must not lose. Prints RESULT lines.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from deepreason_core.canonical import canonical_json, sha256_hex
from minireason.loop import custody
from minireason import provider_openai_compat as provider

FIXTURES = [
    {"nested": {"list": [1, 2, 3], "unicode": "caf￩ x"}, "n": None},
    {"non_ascii_identity_char": "￩"},          # U+FFE9: identity vs record form
    {"a": 1, "b": [True, False], "s": "x"},
    [],
    "a bare string",
    3.25,
]


def result(ok: bool, *parts: object) -> None:
    print("RESULT", "PASS" if ok else "FAIL", *parts)


def main() -> None:
    for i, value in enumerate(FIXTURES):
        c = custody.digest(value)
        p = provider.digest(value)
        d = sha256_hex(canonical_json(value))
        compact = json.dumps(value, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")).encode("utf-8")
        result(c == p == d, f"fixture[{i}] three-way digest identity")
        result(canonical_json(value) == compact,
               f"fixture[{i}] canonical_json byte-identical to the hashed compact form")
        roundtrip = json.loads(custody.encoded(value).decode("utf-8"))
        result(roundtrip == value and custody.digest(roundtrip) == c,
               f"fixture[{i}] record form round-trips to the same digest")
    # encoded is intended to *differ* from canonical: confirm the claim is not vacuous
    value = FIXTURES[0]
    result(custody.encoded(value) != canonical_json(value)
           and custody.encoded(value).endswith(b"\n"),
           "encoded differs from canonical on a nested fixture (indent=2, trailing \\n)")

    # MIN_CREDENTIAL_LENGTH agreement, pinned by the docstrings of both modules
    result(custody.MIN_CREDENTIAL_LENGTH == provider._MIN_SECRET_LENGTH == 8,
           "MIN_CREDENTIAL_LENGTH == provider_openai_compat._MIN_SECRET_LENGTH == 8")

    # CUSTODY_CODES sits inside types.FAILURE_CODES
    from minireason.loop import types
    result(set(custody.CUSTODY_CODES) <= types.FAILURE_CODES,
           "CUSTODY_CODES is a slice of FAILURE_CODES;",
           sorted(set(custody.CUSTODY_CODES) - types.FAILURE_CODES))
    result(sorted(custody.CUSTODY_CODES) == list(custody.CUSTODY_CODES)
           and len(custody.CUSTODY_CODES) == 9,
           "CUSTODY_CODES sorted, 9 members")

    # every custody exception is a LoopError keeping its historical base
    result(issubclass(custody.CustodyMismatch, types.LoopError)
           and issubclass(custody.CredentialInOutput, ValueError)
           and issubclass(custody.WriteOnceViolation, FileExistsError),
           "exception hierarchy as published")


if __name__ == "__main__":
    main()
