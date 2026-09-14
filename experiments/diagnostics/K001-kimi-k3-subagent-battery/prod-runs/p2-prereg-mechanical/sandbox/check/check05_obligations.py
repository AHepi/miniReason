"""Check 5: obligations.json counts vs PREREG.md statements; id uniqueness;
every obligation id referenced from config.json or PREREG.md exists."""
import json
import re
from collections import Counter
from pathlib import Path

ob = json.loads(Path("loop-prereg/obligations.json").read_bytes())
cfg = json.loads(Path("loop-prereg/config.json").read_bytes())
pre = Path("loop-prereg/PREREG.md").read_text(encoding="utf-8")

obls = ob["obligations"]
O = [o["id"] for o in obls if o["set"] == "O"]
P = [o["id"] for o in obls if o["set"] == "P"]
ids = [o["id"] for o in obls]
dupes = {i: c for i, c in Counter(ids).items() if c > 1}

# all id-like tokens o1..o12 / p1..p12 appearing in config.json text and PREREG.md
IDPAT = re.compile(r"\b(?:o|p)(?:1[0-2]|[1-9])\b")
cfg_text = json.dumps(cfg)
refs = {"config.json": sorted(set(IDPAT.findall(cfg_text))),
        "PREREG.md": sorted(set(IDPAT.findall(pre)))}

# PREREG.md's stated counts: pull the table line and prose numbers computation-based
prereg_count_claims = []
for ln, line in enumerate(pre.splitlines(), 1):
    if re.search(r"\*\*O\*\* \(\d+\)|\*\*P\*\* \(\d+\)|failed set.*protected set", line):
        prereg_count_claims.append({"line": ln, "text": line.strip()})

declared_ids = set(ids)
ref_check = {src: [r for r in lst if r in declared_ids]
             for src, lst in refs.items()}
missing_from_obligations = {src: [r for r in lst if r not in declared_ids]
                            for src, lst in refs.items()}
never_referenced_in_prereg = [i for i in ids
                              if i not in set(refs["PREREG.md"])]

# validate.py's output claims about |O| and |P| (from out/check1 files if present)
report = {
    "obligations_ids_in_file_order": ids,
    "O_count_actual": len(O), "O_ids": O,
    "P_count_actual": len(P), "P_ids": P,
    "total": len(obls),
    "duplicate_ids": dupes,
    "ids_unique": not dupes,
    "prereg_count_claims": prereg_count_claims,
    "id_references": refs,
    "references_that_exist": ref_check,
    "references_missing_from_obligations_json": missing_from_obligations,
    "obligation_ids_not_referenced_in_PREREG_md_by_token": never_referenced_in_prereg,
    "obligations_sha256_field_present": "obligations_sha256" in ob,
}
Path("out/check5-obligations.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
