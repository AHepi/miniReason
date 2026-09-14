"""Check 7: the six-value reading vocabulary. PREREG.md asserts a closure to six
values but the bundle JSONs carry no vocabulary list; verify that by scanning for
ROOT_READING_VOCABULARY / NOMINABLE_RELATIONS and for candidate relation tokens
across the bundle, and extract PREREG.md's own wording (line numbers)."""
import json
import re
from pathlib import Path

FILES = ["config.json", "obligations.json", "reading_set.json",
         "calibration.json", "PREREG.md", "VALIDATION.md", "validate.py"]
hits = {}
for f in FILES:
    text = (Path("loop-prereg") / f).read_text(encoding="utf-8")
    lines = []
    for ln, line in enumerate(text.splitlines(), 1):
        if ("ROOT_READING_VOCABULARY" in line or "NOMINABLE_RELATIONS" in line
                or "vocabular" in line.lower()):
            lines.append({"line": ln, "text": line.strip()[:400]})
    if lines:
        hits[f] = lines

# candidate six values: relation tokens used in calibration/PREREG
cal = json.loads(Path("loop-prereg/calibration.json").read_bytes())
relations_in_calibration = sorted({
    r["ground_truth"]["relation"] for r in cal["rows"]
    if r["ground_truth"].get("relation")})

vocab_key_values_in_json = []
for f in ("config.json", "obligations.json", "reading_set.json", "calibration.json"):
    obj = json.loads((Path("loop-prereg") / f).read_bytes())
    def walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if "vocab" in k.lower():
                    vocab_key_values_in_json.append({"file": f, "key": path + k, "value": v})
                walk(v, path + k + ".")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{path}[{i}].")
    walk(obj)

report = {
    "files_mentioning_vocabulary": hits,
    "relation_strings_used_in_calibration_ground_truth": relations_in_calibration,
    "vocabulary_keys_found_in_bundle_json": vocab_key_values_in_json,
    "config_json_keys": sorted(json.loads(Path("loop-prereg/config.json").read_bytes()).keys()),
}
Path("out/check7-vocab.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
