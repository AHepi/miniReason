"""Check 2: sha256 of each bundle JSON + PREREG.md, compared against every
sha256-looking token in PREREG.md, VALIDATION.md and config.json (token map:
out/sha-token-map.json). Also: does the obligations.json pin reproduce over
canonical bytes with the recipe obligations.json itself states."""
import hashlib
import json
from pathlib import Path

FILES = ["config.json", "obligations.json", "reading_set.json",
         "calibration.json", "PREREG.md", "validate.py", "VALIDATION.md"]
SHA_FILES = ["config.json", "obligations.json", "reading_set.json",
             "calibration.json", "PREREG.md"]  # JSON files + PREREG.md, per task

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

actual = {f: sha((Path("loop-prereg") / f).read_bytes()) for f in FILES}
token_map = json.loads(Path("out/sha-token-map.json").read_text(encoding="utf-8"))["tokens"]

# every token vs every file digest
matches = []
unmatched = []
for tok, where in sorted(token_map.items()):
    hit = [f for f, d in actual.items() if d == tok]
    (matches if hit else unmatched).append if False else None
    rec = {"token": tok, "appears_in": where,
           "matches_file": hit}
    (matches if hit else unmatched).append(rec)

# which VALIDATION.md-table row says each token pins which file: pull the table
val_lines = Path("loop-prereg/VALIDATION.md").read_text(encoding="utf-8").splitlines()
pin_table = []
for ln in range(100, 116):
    line = val_lines[ln - 1] if ln - 1 < len(val_lines) else ""
    if line.startswith("| `"):
        parts = [p.strip().strip("`") for p in line.split("|")]
        pin_table.append({"line": ln, "file": parts[1], "digest": parts[2]})

table_rows = []
for f in FILES:
    pin = next((r["digest"] for r in pin_table if r["file"] == f), None)
    table_rows.append({
        "file": f,
        "actual_sha256": actual[f],
        "pinned_in_VALIDATION.md": pin,
        "match": (pin == actual[f]) if pin else None,
    })

# obligations canonical digest reproduction
ob = json.loads(Path("loop-prereg/obligations.json").read_bytes())
pin = ob["obligations_sha256"]
body = {k: v for k, v in ob.items()
        if k not in ("obligations_sha256", "obligations_sha256_recipe")}
canon = json.dumps(body, ensure_ascii=False, sort_keys=True,
                   separators=(",", ":")).encode("utf-8")
canon_digest = sha(canon)
prereg = Path("loop-prereg/PREREG.md").read_text(encoding="utf-8")

report = {
    "files_hashed": actual,
    "validation_md_pin_table": table_rows,
    "token_matches_bundle_file": matches,
    "tokens_matching_no_bundle_file": unmatched,
    "obligations_canonical": {
        "pin_in_obligations.json": pin,
        "recomputed_over_canonical_bytes": canon_digest,
        "reproduces": canon_digest == pin,
        "recipe_stated": ob["obligations_sha256_recipe"],
        "pin_appears_in_PREREG.md": pin in prereg,
        "pin_appears_in_VALIDATION.md": pin in Path("loop-prereg/VALIDATION.md").read_text(encoding="utf-8"),
    },
}
Path("out/check2-digests.json").write_text(json.dumps(report, indent=2),
                                           encoding="utf-8")
print(json.dumps(report, indent=2))
