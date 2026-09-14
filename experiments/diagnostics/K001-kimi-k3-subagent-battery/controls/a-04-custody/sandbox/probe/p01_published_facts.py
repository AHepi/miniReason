"""The published claims of notes/WAVE0-INTERFACE.md section 4, executed.

CUSTODY_CODES shape and membership, the credential floor's agreement with the
transport, and the three-way digest identity of decision 7.
"""
import _boot  # noqa: F401
import json

from minireason.loop import custody
from minireason.loop import types
from minireason import provider_openai_compat as tx
from deepreason_core.canonical import canonical_json, sha256_hex

print("CUSTODY_CODES len      :", len(custody.CUSTODY_CODES))
print("CUSTODY_CODES sorted   :", list(custody.CUSTODY_CODES) == sorted(custody.CUSTODY_CODES))
missing = [c for c in custody.CUSTODY_CODES if c not in types.FAILURE_CODES]
print("not in FAILURE_CODES   :", missing)
print("PIN_KEY                :", repr(custody.PIN_KEY))
print("ALWAYS_SCANNED_ENVS    :", custody.ALWAYS_SCANNED_ENVS)
print("MIN_CREDENTIAL_LENGTH  :", custody.MIN_CREDENTIAL_LENGTH,
      "== tx._MIN_SECRET_LENGTH", tx._MIN_SECRET_LENGTH,
      custody.MIN_CREDENTIAL_LENGTH == tx._MIN_SECRET_LENGTH)
print("ALWAYS envs agree      :", tuple(custody.ALWAYS_SCANNED_ENVS) == tuple(tx._ALWAYS_SECRET_ENVS))

FIXTURE = {
    "b": [1, 2, {"z": None, "a": True}],
    "a": "café — 日本語",
    "c": {"nested": {"k": "v"}, "empty": {}},
    "d": 1.5,
    "e": "quote\" backslash\\ newline\n tab\t",
}
d_cust = custody.digest(FIXTURE)
d_tx = tx.digest(FIXTURE)
d_can = sha256_hex(canonical_json(FIXTURE))
print("digest custody         :", d_cust)
print("digest transport       :", d_tx)
print("digest canonical_json  :", d_can)
print("three-way identity     :", d_cust == d_tx == d_can)

raw_compact = json.dumps(FIXTURE, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
print("canonical_json bytes eq:", canonical_json(FIXTURE) == raw_compact)

enc = custody.encoded(FIXTURE)
print("encoded ends with \\n   :", enc.endswith(b"\n"))
print("encoded is indent=2    :", enc.startswith(b'{\n  "a"'))
print("encoded round-trips    :", custody.digest(json.loads(enc.decode("utf-8"))) == d_cust)
print("__all__ complete       :",
      sorted(custody.__all__) == sorted(n for n in custody.__all__))
print("scanned_credential_envs:", custody.scanned_credential_envs())
