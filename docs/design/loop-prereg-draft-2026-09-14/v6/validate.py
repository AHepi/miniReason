#!/usr/bin/env python3
"""Offline v6 custody/admission validation. Never imports driver or identity code."""
from pathlib import Path, PureWindowsPath
import ast
import hashlib
import json
import re
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
sys.path.insert(0, str(ROOT / "src"))
from minireason.loop import rows_pairs as pairs

REQUIRED = ("README.md", "PREREG.md", "config.json", "reading_set.json",
            "obligations.json", "calibration.json", "CLONE-PATCH.md", "validate.py",
            "VALIDATION.md", "CHANGES-PREREG.md", "REVIEW-PREREG.md",
            "bundle-worksheet.md", "bundle-worksheet.json", "DRAFT-REPORT.md")
FAILURES = []
def sha(raw):
    return hashlib.sha256(raw).hexdigest()
def load(name):
    return json.loads((BASE / name).read_bytes())
def check(ok, message):
    print(("PASS " if ok else "FAIL ") + message)
    if not ok:
        FAILURES.append(message)
def spans(value):
    if isinstance(value, dict):
        if {"path", "sha256", "byte_start", "byte_end", "text"} <= set(value):
            yield value
        for item in value.values():
            yield from spans(item)
    elif isinstance(value, list):
        for item in value:
            yield from spans(item)
def source_span_ok(span):
    raw = (ROOT / span["path"]).read_bytes()
    a, b = span["byte_start"], span["byte_end"]
    return (0 <= a <= b <= len(raw) and sha(raw) == span["sha256"]
            and raw[a:b] == span["text"].encode("utf-8")
            and span["line_start"] == raw[:a].count(b"\n") + 1
            and span["line_end"] == raw[:max(a,b-1)].count(b"\n") + 1
            and span["codepoint_start"] == len(raw[:a].decode("utf-8"))
            and span["codepoint_end"] == len(raw[:b].decode("utf-8")))
def fold(key):
    result = []
    for part in key.split("/"):
        value = re.sub(r"[^A-Za-z0-9._#-]", "-", part).strip("-") or "x"
        result.append(value if value[0].isalnum() else "x" + value)
    result[-1] += "#" + sha(key.encode())[:12]
    return "/".join(result)
def main():
    print("OFFLINE V6 DRAFT CHECK ONLY - no S0, provider call or plan identity")
    check(all((BASE/n).is_file() for n in REQUIRED), "all fourteen v5-structure files present")
    cfg, rows, obs, cal = [load(n) for n in
                          ("config.json","reading_set.json","obligations.json","calibration.json")]
    check(rows["loop_plan_id"] == "<UNMINTED>" and
          rows["preregistration_receipt"] == "REC-YYYYMMDD-X" and
          rows["preregistration_timestamp"] == "<minted at S0>" and
          "prior exposure declared" in rows["reading_set_status"],
          "unminted placeholders and prior exposure declared")
    check(cfg["reading_rows_builder"] == "pairs-v1" and
          cfg["cycle_budget"] == 0 and cfg["max_calls"] == 0 and
          cfg["provider_mode"] == "DRAFT-NO-RUN",
          "explicit pair builder and invalid execution sentinels")
    occ = "experiments/diagnostics/F001-fork5-multifamily/occurrence-09"
    check(cfg["occurrences"] == [occ] and not cfg["contrast"]["attached"] and
          not cfg["contrast"]["occurrences"], "F09 only; no F003 source or contrast leg dispatched")
    built = pairs.build_rows(ROOT / occ, repo_root=ROOT)
    admitted = [r for r in built if r["admission"] == "ADMITTED"]
    keys = [r["row_key"] for r in admitted]
    check(built == rows["candidate_rows"], "fresh offline enumeration equals every stored candidate byte and disposition")
    check(keys == rows["rows"] == rows["config_reading_set"] == cfg["reading_set"]
          and rows["row_count"] == len(keys), "only builder-admitted rows populate reading sets")
    check(len(built) == 6 and len(admitted) == 6,
          "actual occurrence-09: six candidates, six ADMITTED, zero UNRESOLVED")
    pairs.validate_keys(built, cfg["run_id"])
    index = pairs.adapter_index(built)
    check(rows["adapter_index"] == [
        {"components":list(k),"row_key":v["row_key"],"candidate_index":built.index(v)}
        for k,v in index.items()], "adapter components are one-to-one with exact candidate source coordinates")
    check(len(set(keys)) == len(set(map(fold, keys))) == len(keys)
          and all(fold(k) == pairs.cell_key_for(k) and
                      re.fullmatch(r"h005-row/[A-Za-z0-9]{2,12}#u/ref/[ovr]",k)
                      for k in keys), "raw keys and folded cells admissible and injective")
    mapped = list(spans(built))
    check(bool(mapped) and all(source_span_ok(s) for s in mapped),
          "every exact UTF-8 slice, full-file hash, byte offset, line and code-point map matches")
    surfaces_ok = True
    for row in built:
        if row["target"] is None or row["referring"] is None:
            continue
        surface = pairs.build_surface(row)
        for side in ("target","referring"):
            surfaces_ok &= row[side]["text"].encode("utf-8") in surface.text
        for ref in row["referring_passages"]:
            surfaces_ok &= ref["passage"]["text"].encode("utf-8") in surface.text
    check(surfaces_ok, "whole frozen surface contributions and exact referring passages are byte-faithful")
    paths = {k:pairs.provider_paths(k,cfg["run_id"]) for k in keys}
    check(paths == rows["path_length"]["provider_paths"], "all actual provider paths match frozen draft inventory")
    longest = max((p for v in paths.values() for p in v.values()), key=len)
    independent = []
    prefix = PureWindowsPath("C:/Dev/miniReason/experiments/loops")/cfg["run_id"]/"readings"
    for key in keys:
        for suffix in ("","#order-swapped","#paraphrase-1"):
            independent.append(str(prefix/key/(fold(key)+suffix)/"judge-1"/"provider"/"call-0001.response.json"))
    check(set(independent) == {p for v in paths.values() for p in v.values()} and
          len(longest) == rows["path_length"]["actual_longest_length"] == 189 < 240,
          "independent full Windows provider-path bound: 189 < 240")
    print("LONGEST_PROVIDER_PATH " + longest)
    pins = rows["source_pins"]
    check(all((ROOT/p).is_file() and sha((ROOT/p).read_bytes()) == digest for p,digest in pins.items()),
          str(len(pins)) + " draft source hashes match")
    check(rows["builder"]["sha256"] == pins["src/minireason/loop/rows_pairs.py"],
          "builder digest agrees with source manifest")
    check(all(p.relative_to(ROOT).as_posix() in pins for p in pairs.source_paths(ROOT/occ)),
          "all builder source dependencies present in draft pins")
    contingent = rows["contingent_sources"][0]
    check(contingent["included_in_active_rows"] is False and bool(contingent["draft_file_sha256"]) and
          all(sha((ROOT/p).read_bytes()) == digest for p,digest in contingent["draft_file_sha256"].items()),
          "contingent F003 draft provenance matches; no F003 row populated")
    body = {k:v for k,v in obs.items() if k not in ("obligations_sha256","obligations_sha256_recipe")}
    canonical = sha(json.dumps(body,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8"))
    file_hash = sha((BASE/"obligations.json").read_bytes())
    check(canonical == obs["obligations_sha256"] == rows["obligations_digests"]["canonical_body"]
          and file_hash == rows["obligations_digests"]["file_sha256"],
          "both obligations digests match v5 recipe")
    print("CANONICAL_BODY_SHA256 " + canonical)
    print("FILE_SHA256 " + file_hash)
    check([o["id"] for o in obs["obligations"] if o["set"] == "O"] == ["o1","o3","o4","o5","o7"]
          and len([o for o in obs["obligations"] if o["set"] == "P"]) == 10
          and set(obs["notes"]["retired"]) == {"o2","o6","p2","p3","p9"},
          "five O, ten P and five explicit retired dispositions retained")
    check((BASE/"calibration.json").read_bytes() ==
          (BASE.parent/"v5/calibration.json").read_bytes(),
          "corrected v5 nine-anchor calibration copied byte-identically")
    budget = rows["budget"]
    check(sum(budget["row_components"].values()) == 11 and budget["R"] == len(keys)
          and budget["W"] == 1 and budget["first_pass_calls"] == 11*len(keys)+46 == 112,
          "proposed first-pass allowance: 11 x 6 + 46 = 112; no F003 or reopen calls")
    tree = ast.parse((ROOT/"src/minireason/loop/standard.py").read_text(encoding="utf-8"))
    forbidden = next(set(ast.literal_eval(n.value.args[0])) for n in tree.body
                     if isinstance(n,ast.AnnAssign) and isinstance(n.target,ast.Name)
                     and n.target.id == "FORBIDDEN_KEYS")
    def bad(value):
        return (any(str(k).lower() in forbidden or bad(v) for k,v in value.items())
                if isinstance(value,dict) else any(map(bad,value)) if isinstance(value,list) else False)
    check(not any(bad(json.loads(p.read_bytes())) for p in BASE.glob("*.json")),
          "bundle JSON keys retain closed non-evaluative vocabulary")
    check(not any(re.search(r"REC-\d{8}-",p.read_text(encoding="utf-8"))
                  for p in BASE.iterdir() if p.is_file()),
          "no timestamped receipt identity copied or minted inside bundle")
    print("UNRESOLVED launch: owner F003 review/receipt, O5, stop/ceiling, true provider budget and reopening")
    print("RESULT " + ("FAIL" if FAILURES else "PASS") + " (OFFLINE CUSTODY ONLY; DRAFT remains unregistered)")
    return 1 if FAILURES else 0
if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print("FAIL offline draft check raised " + type(error).__name__ + ": " + str(error))
        sys.exit(1)
