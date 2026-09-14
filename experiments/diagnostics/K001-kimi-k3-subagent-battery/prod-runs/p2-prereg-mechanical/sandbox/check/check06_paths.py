"""Check 6: every file path referenced in calibration.json and reading_set.json;
does it appear exactly in evidence/repo-files.txt?"""
import json
import re
from pathlib import Path

repo_files = set(Path("evidence/repo-files.txt").read_text(encoding="utf-8").splitlines())

def walk(obj, acc):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("file", "source_file", "rendered_in") and isinstance(v, str):
                acc.append(v)
            else:
                walk(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, acc)
    return acc

cal = json.loads(Path("loop-prereg/calibration.json").read_bytes())
rs = json.loads(Path("loop-prereg/reading_set.json").read_bytes())

cal_paths = sorted(set(walk(cal, [])))
rs_paths = sorted(set(walk(rs, [])))

report = {
    "repo_files_line_count": len(repo_files),
    "calibration_paths": [
        {"path": p, "in_repo_files": p in repo_files} for p in cal_paths],
    "reading_set_paths": [
        {"path": p, "in_repo_files": p in repo_files} for p in rs_paths],
    "missing": sorted({p for p in cal_paths + rs_paths if p not in repo_files}),
}
Path("out/check6-paths.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
