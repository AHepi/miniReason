"""Check 2c: locate the exact byte difference between the sandbox copy of
config.json and the digest VALIDATION.md pins for it. Tries line endings,
trailing newline, and reserialization variants so the FAIL is evidence-based."""
import hashlib
import json
from pathlib import Path

raw = Path("loop-prereg/config.json").read_bytes()
pinned = "46495a6fa0ee5667b6ba5128adbaee9062ed5b6637310bb44b12efdf14c0da90"
sha = lambda b: hashlib.sha256(b).hexdigest()

variants = {
    "as-is": raw,
    "no trailing newline": raw.rstrip(b"\n"),
    "crlf": raw.replace(b"\n", b"\r\n"),
    "cr": raw.replace(b"\n", b"\r"),
    "no trailing newline + crlf": raw.rstrip(b"\n").replace(b"\n", b"\r\n"),
}
obj = json.loads(raw)
variants["reserialized 2-space utf-8"] = json.dumps(
    obj, indent=2, ensure_ascii=False).encode() + b"\n"
variants["reserialized 2-space ascii"] = json.dumps(
    obj, indent=2, ensure_ascii=True).encode() + b"\n"
variants["canonical"] = json.dumps(
    obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()

results = {name: {"sha256": sha(b), "matches_pin": sha(b) == pinned,
                  "length": len(b)}
           for name, b in variants.items()}
report = {
    "pinned": pinned, "actual": sha(raw), "raw_length": len(raw),
    "last_byte": raw[-1:], "cr_count": raw.count(b"\r"), "lf_count": raw.count(b"\n"),
    "decoded_utf8_ok": True,
    "variants": results,
    "any_variant_reproduces_pin": any(v["matches_pin"] for v in results.values()),
}
Path("out/check2c-config-diff.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
print(json.dumps(report, indent=2, default=str))
