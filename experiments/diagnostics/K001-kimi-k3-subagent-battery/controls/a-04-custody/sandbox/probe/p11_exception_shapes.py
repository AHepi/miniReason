"""The exception contract WAVE0-INTERFACE section 4 publishes:
CustodyMismatch(code, detail=""), CredentialInOutput a ValueError,
WriteOnceViolation a FileExistsError, and every one a types.LoopError with a
.code a receipt can read without parsing the message.
"""
import _boot  # noqa: F401

from minireason.loop.custody import (CustodyMismatch, CredentialInOutput,
                                     WriteOnceViolation)
from minireason.loop.types import LoopError

for cls in (CustodyMismatch, CredentialInOutput, WriteOnceViolation):
    exc = cls("WRITE_ONCE_VIOLATION", "/run/steps/0001-S0.json")
    print(f"{cls.__name__}")
    print("   isinstance LoopError    :", isinstance(exc, LoopError))
    print("   isinstance ValueError   :", isinstance(exc, ValueError))
    print("   isinstance FileExistsErr:", isinstance(exc, FileExistsError))
    print("   isinstance OSError      :", isinstance(exc, OSError))
    print("   .code                   :", getattr(exc, "code", None))
    print("   .detail                 :", getattr(exc, "detail", None))
    print("   str(exc)                :", repr(str(exc)))
    print("   .args                   :", exc.args)
    print("   .errno / .strerror      :", getattr(exc, "errno", "-"),
          "/", getattr(exc, "strerror", "-"))
    print("   MRO                     :", [c.__name__ for c in cls.__mro__][:8])

# default detail
print()
print("default detail:", repr(str(CustodyMismatch("PIN_MAP_MISSING"))))

# the shape gate the interface says types enforces
for bad in ("lower_case", "Has-Hyphen", "", "9LEADING"):
    try:
        CustodyMismatch(bad)
    except Exception as exc:  # noqa: BLE001
        print(f"CustodyMismatch({bad!r:14}) -> {type(exc).__name__}: {exc}")
    else:
        print(f"CustodyMismatch({bad!r:14}) -> accepted")

# a code custody can raise that is not in CUSTODY_CODES?
from minireason.loop import custody
print()
print("CUSTODY_CODES              :", custody.CUSTODY_CODES)
src = open(custody.__file__, encoding="utf-8").read()
import re
raised = sorted(set(re.findall(r'CustodyMismatch\("([A-Z_]+)"', src)
                    + re.findall(r'CredentialInOutput\("([A-Z_]+)"', src)
                    + re.findall(r'WriteOnceViolation\("([A-Z_]+)"', src)
                    + re.findall(r'CustodyFinding\("([A-Z_]+)"', src)))
print("codes literally constructed:", raised)
print("constructed but undeclared :", [c for c in raised if c not in custody.CUSTODY_CODES])
print("declared but never used    :", [c for c in custody.CUSTODY_CODES if c not in raised])
