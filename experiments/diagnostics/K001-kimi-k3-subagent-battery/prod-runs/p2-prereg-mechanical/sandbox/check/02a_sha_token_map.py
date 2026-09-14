"""Support computation: extract every sha256-looking token (64 lowercase hex)
from PREREG.md, VALIDATION.md and config.json; for each unique token record which
files it appears in and, per file, the line numbers."""
import json
import re
from pathlib import Path

DOC_FILES = {
    "PREREG.md": Path("loop-prereg/PREREG.md"),
    "VALIDATION.md": Path("loop-prereg/VALIDATION.md"),
    "config.json": Path("loop-prereg/config.json"),
}
HEX = re.compile(r"\b[0-9a-f]{64}\b")

tokens = {}
for name, path in DOC_FILES.items():
    for ln, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for m in HEX.finditer(line):
            tok = m.group(0)
            tokens.setdefault(tok, {}).setdefault(name, []).append(ln)

prefixes = {}
for name, path in DOC_FILES.items():
    for ln, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for m in re.finditer(r"\b[0-9a-f]{16}\u2026|\b[0-9a-f]{16}\.\.\.", line):
            prefixes.setdefault(m.group(0), {}).setdefault(name, []).append(ln)

out = {
    "regex": r"\b[0-9a-f]{64}\b",
    "n_distinct_tokens": len(tokens),
    "tokens": {t: v for t, v in sorted(tokens.items())},
    "prefix_mentions": prefixes,
}
Path("out/sha-token-map.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps({"n_distinct_tokens": len(tokens), "tokens": out["tokens"],
                  "prefix_mentions": prefixes}, indent=2))
