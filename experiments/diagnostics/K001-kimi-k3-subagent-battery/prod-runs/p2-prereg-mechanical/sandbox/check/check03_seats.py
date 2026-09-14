"""Check 3: seats in config.json vs src/minireason/data/endpoints.json (name,
family, key_env); judge seats sharing a family."""
import json
from pathlib import Path

cfg = json.loads(Path("loop-prereg/config.json").read_bytes())
reg = {e["name"]: e for e in json.loads(
    Path("src/minireason/data/endpoints.json").read_bytes())["endpoints"]}

seats = {
    "critic": cfg["seats"]["critic"],
    "defender": cfg["seats"]["defender"],
    "variator": cfg["seats"]["variator"],
}
for i, j in enumerate(cfg["seats"]["judges"], 1):
    seats[f"judge-{i}"] = j

rows = []
for role, name in seats.items():
    e = reg.get(name)
    rows.append({
        "role": role,
        "endpoint_name": name,
        "exists_in_registry": e is not None,
        "registry_family": e["family"] if e else None,
        "registry_key_env": e["key_env"] if e else None,
        "registry_timeout_seconds": e["timeout_seconds"] if e else None,
    })

j1, j2 = cfg["seats"]["judges"]
judge_family_check = {
    "judge-1": {"name": j1, "family": reg[j1]["family"] if j1 in reg else None},
    "judge-2": {"name": j2, "family": reg[j2]["family"] if j2 in reg else None},
}
same_family = (j1 in reg and j2 in reg
               and reg[j1]["family"] == reg[j2]["family"])
distinct_families = {r["registry_family"] for r in rows if r["registry_family"]}

# also: the family/key_env values PREREG.md's seat table claims, extracted from
# the markdown table rows, compared against the registry
prereg = Path("loop-prereg/PREREG.md").read_text(encoding="utf-8").splitlines()
prereg_rows = []
for ln, line in enumerate(prereg, 1):
    s = line.strip()
    if s.startswith("| `") and "`ollama" in s.replace("` `", "") or s.startswith("| `variator`"):
        parts = [p.strip() for p in s.split("|")][1:-1]
        prereg_rows.append({"line": ln, "cells": parts[1:5]})

report = {
    "seat_lookup": rows,
    "all_seats_exist": all(r["exists_in_registry"] for r in rows),
    "mismatches": [r for r in rows if not r["exists_in_registry"]],
    "judge_family_check": judge_family_check,
    "judge_seats_share_a_family": same_family,
    "n_distinct_families_over_5_seats": len(distinct_families),
    "prereg_seat_table_rows": prereg_rows,
}
Path("out/check3-seats.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
