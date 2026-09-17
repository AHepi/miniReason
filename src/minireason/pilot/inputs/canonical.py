# Port provenance: https://github.com/AHepi/DeepReason @ 9607fba6f0a3066fbcab282c9ae0fad823e52e0c
# Upstream: src/deepreason/canonical.py; MIT, Copyright (c) 2026 Aaron Hepi; see LICENSE.
"""Canonical serialization (spec §1).

Artifact ids are sha256 over canonical JSON of (content_ref, codec,
interface); blobs are sha256 over raw bytes. Canonical = sorted keys,
compact separators, UTF-8.
"""

import hashlib
import json


def canonical_json(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
