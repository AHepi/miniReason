"""The published exception shapes.

Interface (sec.3): "`ContractError(LoopError, ValueError)` with
`(code=CONTRACT_VIOLATION, detail="")` ... `SchemaInvalid(ContractError)` with
`(role, reason, message, path=())`; `.code` is `SCHEMA_INVALID`, `.reason` is a
`SCHEMA_REASONS` member, `.path` and `.detail` carry the location and the message.
`ScoringKeyForbidden(ContractError)` with `(path=())`; `str(exc)` is exactly
`SCORING_KEY_FORBIDDEN`, so the existing study's `code_of` reads it unchanged."

types.LoopError.__init__ sets the argument as ``f"{code}: {detail}" if detail
else code``, so `str(exc)` is fixed when the exception is built.
"""
from __future__ import annotations

import _boot  # noqa: F401

from minireason.loop import contracts, types

try:
    contracts.assert_no_scoring_keys({"a": {"rank": 1}})
except contracts.ScoringKeyForbidden as exc:
    print("ScoringKeyForbidden:")
    print("  str(exc)      =", repr(str(exc)))
    print("  exc.code      =", repr(exc.code))
    print("  exc.detail    =", repr(exc.detail))
    print("  exc.path      =", exc.path)
    print("  class attr code:", repr(contracts.ScoringKeyForbidden.code))
    print("  isinstance LoopError/ValueError:",
          isinstance(exc, types.LoopError), isinstance(exc, ValueError))

try:
    contracts.validate("defender", {"answer": "a"})
except contracts.SchemaInvalid as exc:
    print()
    print("SchemaInvalid:")
    print("  str(exc)                 =", repr(str(exc)))
    print("  exc.code                 =", repr(exc.code))
    print("  exc.detail               =", repr(exc.detail))
    print("  exc.role/.reason/.path   =", exc.role, exc.reason, exc.path)
    print("  LoopError invariant str(exc) == f'{code}: {detail}':",
          str(exc) == f"{exc.code}: {exc.detail}")
    print("  the same invariant on a plain LoopError:")
    plain = types.LoopError("SOME_CODE", "some detail")
    print("    ", str(plain) == f"{plain.code}: {plain.detail}")

print()
print("SCHEMA_INVALID in types.FAILURE_CODES:",
      contracts.SCHEMA_INVALID in types.FAILURE_CODES)
print("CONTRACT_VIOLATION in types.FAILURE_CODES:",
      contracts.CONTRACT_VIOLATION in types.FAILURE_CODES)
print("SCORING_KEY_FORBIDDEN in types.FAILURE_CODES:",
      contracts.SCORING_KEY_FORBIDDEN in types.FAILURE_CODES)
print("types.is_failure_code on each:",
      [types.is_failure_code(c) for c in (contracts.SCHEMA_INVALID,
                                          contracts.CONTRACT_VIOLATION,
                                          contracts.SCORING_KEY_FORBIDDEN)])
print("blocked:schema is a BLOCK_CODE:",
      types.block_code("schema") in types.BLOCK_CODES,
      repr(types.block_code("schema")))
