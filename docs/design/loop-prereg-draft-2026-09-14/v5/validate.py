#!/usr/bin/env python3
"""Offline DRAFT checks only: no driver import, identity minting or provider calls."""
from pathlib import Path, PureWindowsPath
import ast
import hashlib
import json
import re
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
REQUIRED = ("README.md", "PREREG.md", "config.json", "reading_set.json",
            "obligations.json", "calibration.json", "CLONE-PATCH.md", "validate.py",
            "VALIDATION.md", "CHANGES-PREREG.md", "REVIEW-PREREG.md",
            "bundle-worksheet.md", "bundle-worksheet.json")
DIGEST_KEYS = ("obligations_sha256", "obligations_sha256_recipe")
failures = []

def check(ok, message):
    print(("PASS " if ok else "FAIL ") + message)
    if not ok:
        failures.append(message)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def read_json(name):
    return json.loads((BASE / name).read_bytes().decode("utf-8"))

def fold(key):
    parts = []
    for part in key.split("/"):
        text = re.sub(r"[^A-Za-z0-9._#-]", "-", part).strip("-") or "x"
        if not text[0].isalnum():
            text = "x" + text
        parts.append(text)
    parts[-1] += "#" + digest(key.encode("utf-8"))[:12]
    return "/".join(parts)

def main():
    print("OFFLINE DRAFT CHECK ONLY - no pre-registration validation")
    check(all((BASE / n).is_file() for n in REQUIRED), "13 required bundle files present")
    cfg, rows, obs, cal = [read_json(n) for n in
                          ("config.json", "reading_set.json", "obligations.json", "calibration.json")]
    check(rows["reading_set_status"] == "UNRESOLVED: awaiting row builder"
          and rows["builder"]["status"] == "UNIMPLEMENTED"
          and rows["loop_plan_id"] == "<UNMINTED>",
          "draft status, unimplemented builder and unminted placeholder explicit")
    check(cfg["reading_set"] == rows["rows"] == []
          and cfg["occurrences"] == ["experiments/diagnostics/F001-fork5-multifamily/occurrence-09"]
          and cfg["contrast"]["attached"] is False
          and not cfg["contrast"]["occurrences"],
          "reading arrays empty; frozen occurrence retained; no contrast attachment")
    check(cfg["cycle_budget"] == 0 and cfg["provider_mode"] == "DRAFT-NO-RUN"
          and cfg["max_calls"] == 0 and "reading_set_status" not in cfg,
          "invalid execution sentinels present; closed-schema status stored separately")
    print("NOTE max_calls=0 alone does not enforce a stop; runtime counts spending-step receipts")
    source_pins = rows["source_pins"]
    needed = rows["required_fixed_pin_paths"]
    check(all(p in source_pins for p in needed), "all six fixed source pins present")
    check(all((ROOT / p).is_file() and digest((ROOT / p).read_bytes()) == h
              for p, h in source_pins.items()),
          str(len(source_pins)) + " draft source file hashes match")
    inv = rows["source_inventory"]
    check(len(inv) == 11 and all(source_pins.get(x["path"]) == x["sha256"]
                                and (ROOT / x["path"]).stat().st_size == x["bytes"] for x in inv),
          "eleven response texts retained as source inventory, not reading rows")
    body = {k: v for k, v in obs.items() if k not in DIGEST_KEYS}
    canonical = digest(json.dumps(body, ensure_ascii=False, sort_keys=True,
                                  separators=(",", ":")).encode("utf-8"))
    file_hash = digest((BASE / "obligations.json").read_bytes())
    check(canonical == obs["obligations_sha256"] == rows["obligations_digests"]["canonical_body"],
          "obligations canonical-body digest matches")
    check(file_hash == rows["obligations_digests"]["file_sha256"],
          "obligations complete-file digest matches")
    print("CANONICAL_BODY_SHA256 " + canonical)
    print("FILE_SHA256 " + file_hash)
    check([o["id"] for o in obs["obligations"] if o["set"] == "O"] == ["o1","o3","o4","o5","o7"]
          and len([o for o in obs["obligations"] if o["set"] == "P"]) == 10
          and set(obs["notes"]["retired"]) == {"o2","o6","p2","p3","p9"},
          "five active O, ten active P and five explicit retired dispositions")
    old_cal = json.loads((ROOT / "docs/design/loop-prereg-draft-2026-09-14/v4/calibration.json").read_bytes())
    expected_rows = json.loads(json.dumps(old_cal["rows"]))
    expected_rows[4]["source_bytes"][2]["bytes"] = 1254
    qualified_ids = {"cal-01", "cal-02", "cal-03", "cal-04", "cal-09"}
    for current, expected in zip(cal["rows"], expected_rows):
        if current["id"] in qualified_ids:
            expected["true_by_construction"] = current["true_by_construction"]
    check(cal["rows"] == expected_rows and cal["pinned_before_first_call"] is False
          and cal["draft_disposition"]["draft_instrument_expectations_only"] is True
          and digest((ROOT / cal["draft_disposition"]["source_file"]).read_bytes())
              == cal["draft_disposition"]["source_file_sha256"],
          "nine inherited anchor constructions retain source provenance; documented judge corrections; no L004 pin completion")
    # Read the literal key vocabulary without importing any repository module.
    tree = ast.parse((ROOT / "src/minireason/loop/standard.py").read_text(encoding="utf-8"))
    forbidden = next(set(ast.literal_eval(n.value.args[0])) for n in tree.body
                     if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)
                     and n.target.id == "FORBIDDEN_KEYS")
    def bad_keys(value):
        if isinstance(value, dict):
            return any(str(k).lower() in forbidden or bad_keys(v) for k, v in value.items())
        if isinstance(value, list):
            return any(bad_keys(v) for v in value)
        return False
    check(not any(bad_keys(json.loads(p.read_bytes())) for p in BASE.glob("*.json")),
          "bundle JSON keys contain no forbidden evaluation fields; quoted prose is not rewritten")
    ut = json.loads((ROOT / 'experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14/use-table-golden/use_table.json').read_bytes())
    recs = {}
    for row in ut['rows']:
        for side in ('referring', 'target'):
            value = row[side + '_record_verbatim']
            if value:
                recs[row[side + '_coordinate_key'] + '#' + row[side + '_record_id']] = value
    record_hashes = []
    for row in cal['rows']:
        for source in row['source_bytes']:
            if 'record' in source:
                raw = recs[source['record']].encode('utf-8')
                record_hashes.append(digest(raw) == source['sha256'] and len(raw) == source['bytes'])
            elif source.get('field') == 'banner':
                raw = ut['banner'].encode('utf-8')
                record_hashes.append(digest(raw) == source['sha256'] and len(raw) == source['bytes'])
            elif 'value' in source:
                value = json.loads((ROOT / source['source_file']).read_bytes())
                for word, index in re.findall(r'([A-Za-z_][A-Za-z_0-9]*)|\[(\d+)\]', source['field']):
                    value = value[word] if word else value[int(index)]
                record_hashes.append(value == source['value'])
            else:
                record_hashes.append(False)
        for quote in row.get('quoted_spans', []):
            record_hashes.append(recs[quote['from']].count(quote['text']) == 1)
    check(bool(record_hashes) and all(record_hashes), 'calibration UTF-8 string hashes/byte lengths, source values and quoted spans match')
    # Hypothetical grammar expansion only. No instance is saved as an admitted key.
    probes = ["h005-row/" + a + later + "#u/ref/" + earlier
              for a in ("p","f") for later, earlier in (("r","o"),("r","v"),("c","r"))]
    cells = [fold(k) for k in probes]
    admissible = all(all(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._#-]*", part)
                         for part in c.split("/")) for c in cells)
    check(admissible and len(set(probes)) == len(set(cells)) == 6,
          "proposed grammar is admissible and injective over its six hypothetical positions")
    prefix = PureWindowsPath("C:/Dev/miniReason/experiments/loops") / cfg["run_id"] / "readings"
    lengths = {}
    for suffix, label in (("", "original"),("#order-swapped","order-swapped"),("#paraphrase-1","paraphrase")):
        lengths[label] = max(len(str(prefix / k / (c + suffix) / "judge-1" / "provider"
                                    / "call-0001.response.json")) for k, c in zip(probes,cells))
    check(max(map(len,probes)) == 19 and max(map(len,cells)) == 32
          and len(str(prefix)) == 81 and lengths == {"original":175,"order-swapped":189,"paraphrase":188}
          and max(lengths.values()) < 240,
          "conditional Windows path bounds: original=175, order-swapped=189, paraphrase=188; all <240")
    print("UNRESOLVED actual key admissibility, injectivity and output paths: no admitted rows")
    check(sum(rows["budget"]["row_components"].values()) == 11
          and rows["budget"]["conditional_calls"] == "11R + 46W"
          and rows["budget"]["R"] is None and rows["budget"]["W"] is None,
          "conditional call arithmetic retained; R and finalized budget unresolved")
    print("UNRESOLVED builder/source-map pin and future S0 coverage: NOT FOUND")
    print("UNRESOLVED audit O5, relation-only stop semantics and executable budget enforcement")
    print("UNRESOLVED/FAIL rows: rows=[]; awaiting proposed row builder; not a finding about material")
    if failures:
        print("RESULT FAIL (STRUCTURE): " + str(len(failures)) + " checks failed; rows also UNRESOLVED")
    else:
        print("RESULT FAIL (UNRESOLVED): draft is not ready for pre-registration or execution")
    return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print("FAIL offline draft check raised " + type(error).__name__ + ": " + str(error))
        sys.exit(1)
