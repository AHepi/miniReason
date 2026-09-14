"""Check 9: every date or run-id string in the bundle; distinct values and where
each appears. Scans the 7 bundle files (config/obligations/reading_set/
calibration/PREREG/VALIDATION/validate.py)."""
import json
import re
from collections import defaultdict
from pathlib import Path

FILES = ["config.json", "obligations.json", "reading_set.json",
         "calibration.json", "PREREG.md", "VALIDATION.md", "validate.py"]

PATS = {
    "iso_datetime": re.compile(r"\b20\d\d-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\dZ\b"),
    "iso_date": re.compile(r"\b20\d\d-[01]\d-[0-3]\d\b"),
    "run_id_like": re.compile(r"\bL\d{3}-[A-Za-z0-9_-]+-[0-9]{4}-[0-9]{2}-[0-9]{2}\b"),
    "rec_id": re.compile(r"\bREC-\d{8}-[A-Za-z0-9]+\b"),
    "snapshot_dir_like": re.compile(r"snapshot-20\d\d-\d\d-\d\d"),
}

found = defaultdict(lambda: defaultdict(list))
for f in FILES:
    text = (Path("loop-prereg") / f).read_text(encoding="utf-8")
    for ln, line in enumerate(text.splitlines(), 1):
        for name, pat in PATS.items():
            for m in pat.finditer(line):
                found[m.group(0)][f].append(ln)

# de-dup line lists, count mentions
values = {}
for tok in sorted(found):
    where = {f: {"lines": sorted(set(lns)), "n_mentions": len(lns)}
             for f, lns in sorted(found[tok].items())}
    values[tok] = where

distinct_dates = sorted({t[:10] for t in values if re.match(r"^20\d\d-", t)})
report = {
    "n_distinct_strings": len(values),
    "distinct_calendar_dates": distinct_dates,
    "values": values,
}
Path("out/check9-dates.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({k: v if k != "values" else {t: list(w.keys()) for t, w in v.items()}
                  for k, v in report.items()}, indent=2))
