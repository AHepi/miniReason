"""Check 8: credential scan over every file in the sandbox (pre-existing files
only). Patterns: sk-[0-9a-f]{32} and [0-9a-f]{32}\\.[A-Za-z0-9_-]{20,}.
NEVER print the matched text: path and line number only. Expect zero hits."""
import json
import re
from pathlib import Path

PATTERNS = {
    "sk-hex32": re.compile(r"sk-[0-9a-f]{32}"),
    "hex32.dot.token20+": re.compile(r"[0-9a-f]{32}\.[A-Za-z0-9_-]{20,}"),
}
# files that exist before our outputs; our check/ scripts and out/ files are
# excluded because the pattern strings themselves live there.
SKIP_DIRS = {"check", "out"}

hits = []
scanned = 0
for p in sorted(Path(".").rglob("*")):
    if not p.is_file():
        continue
    parts = p.parts[1:]
    if parts and parts[0] in SKIP_DIRS:
        continue
    rel = str(p)
    try:
        text = p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, ValueError):
        # binary: scan bytes-decoded latin-1 cheaply; report if matched
        text = p.read_bytes().decode("latin-1")
    scanned += 1
    for ln, line in enumerate(text.splitlines(), 1):
        for name, pat in PATTERNS.items():
            if pat.search(line):
                hits.append({"file": rel, "line": ln, "pattern": name})

report = {
    "patterns": {k: v.pattern for k, v in PATTERNS.items()},
    "files_scanned": scanned,
    "hit_count": len(hits),
    "hits": hits,
    "note": "Matched strings are intentionally not printed.",
}
Path("out").mkdir(exist_ok=True)
Path("out/check8-credentials.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
