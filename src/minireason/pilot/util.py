"""Write-once UTF-8 custody helpers for the new pilot namespace."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

def utc():
    return datetime.now(timezone.utc).isoformat()

def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False, separators=(",", ":"))

def digest(value):
    return hashlib.sha256(encoded(value).encode("utf-8")).hexdigest()

def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"
    with path.open("x", encoding="utf-8", newline="") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    with path.open(encoding="utf-8", newline="") as handle:
        if handle.read() != text:
            raise ValueError("CUSTODY_MISMATCH")

def strict_loads(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("DUPLICATE_KEY")
            result[key] = value
        return result
    def reject(value):
        raise ValueError("NONFINITE_JSON")
    return json.loads(text, object_pairs_hook=pairs, parse_constant=reject)
