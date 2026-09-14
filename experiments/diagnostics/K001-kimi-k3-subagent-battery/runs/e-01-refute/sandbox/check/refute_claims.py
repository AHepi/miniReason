#!/usr/bin/env python3
"""Refutation checks for three claims in
docs/reviews/session-orchestration-report-2026-09-14.md, section 4 ("Live spend").

Every aggregate here is computed from the receipts on disk, never eyeballed.
Run: python3 check/refute_claims.py
"""
import json
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
C001 = ROOT / "experiments/diagnostics/C001-contrast-triple/occurrence-01/responses"
F001 = ROOT / "experiments/diagnostics/F001-fork5-multifamily"


def load_c001():
    recs = []
    for p in sorted(C001.glob("*/*/*/rep*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        d["_path"] = p.relative_to(ROOT).as_posix()
        d["_cell"] = (d["coordinate"]["endpoint_slug"], d["coordinate"]["arm"])
        d["_coord"] = (
            f'{d["coordinate"]["endpoint_slug"]}/{d["coordinate"]["arm"]}/'
            f'{d["coordinate"]["case"]}/rep{d["coordinate"]["replicate"]}'
        )
        recs.append(d)
    return recs


def load_f001():
    recs = []
    for occ in range(1, 9):
        od = F001 / f"occurrence-{occ:02d}" / "responses"
        if not od.is_dir():
            continue
        for p in sorted(od.glob("*/*/cycle01/*.json")):
            d = json.loads(p.read_text(encoding="utf-8"))
            d["_path"] = p.relative_to(ROOT).as_posix()
            d["_occ"] = f"occurrence-{occ:02d}"
            c = d["coordinate"]
            d["_coord"] = f'occurrence-{occ:02d}/{c["problem"]}/{c["arm"]}/cycle01/{c["node"]}'
            recs.append(d)
    return recs


def usage_tokens(d):
    u = d.get("usage")
    return u.get("completion_tokens") if isinstance(u, dict) else None


def main():
    c001 = load_c001()
    f001_all = load_f001()
    v1 = [r for r in f001_all if r["_occ"] <= "occurrence-06"]
    v2 = [r for r in f001_all if r["_occ"] >= "occurrence-07"]

    print("=" * 78)
    print("CLAIM 1 — `INCOMPLETE_GENERATION`: 20 in C001 occurrence-01, the eleven")
    print("FAILED plus the nine PARTIAL of the `deepseek-flash` x `fcl` cell, the")
    print("provider raising it on both.")
    print("=" * 78)
    print(f"receipts loaded: {len(c001)}")
    cells = Counter(r["_cell"] for r in c001)
    print(f"distinct (endpoint, arm) cells: {len(cells)}")
    for cell, n in sorted(cells.items()):
        assert n == 20, (cell, n)
    print("each cell carries exactly 20 receipts")

    by_code = Counter(r["failure_type"] for r in c001)
    print(f"\nfailure_type counts (null = no failure): {dict(by_code)}")
    ig = [r for r in c001 if r["failure_type"] == "INCOMPLETE_GENERATION"]
    print(f"\nINCOMPLETE_GENERATION receipts: {len(ig)}")
    print(f"statuses among them: {Counter(r['status'] for r in ig)}")
    print(f"cells among them:    {Counter(r['_cell'] for r in ig)}")
    print("coordinates:")
    for r in ig:
        print(f'  {r["_path"]}: status={r["status"]} '
              f'finish_reason={r["finish_reason"]} provider_status={r["provider_status"]} '
              f'validation_failure_type={r["validation_failure_type"]}')

    cell = lambda r: r["_cell"] == ("deepseek-flash", "fcl")
    df_fcl = [r for r in c001 if cell(r)]
    df_fcl_failed = [r for r in df_fcl if r["status"] == "FAILED"]
    df_fcl_partial = [r for r in df_fcl if r["status"] == "PARTIAL"]
    print(f"\ndeepseek-flash x fcl receipts: {len(df_fcl)}")
    print(f"  FAILED: {len(df_fcl_failed)}  PARTIAL: {len(df_fcl_partial)}  "
          f"COMPLETE: {sum(1 for r in df_fcl if r['status'] == 'COMPLETE')}")
    print(f"  INCOMPLETE_GENERATION in cell: "
          f"{sum(1 for r in df_fcl if r['failure_type'] == 'INCOMPLETE_GENERATION')}")
    print(f"  FAILED with provider raising it (failure_type non-null): "
          f"{sum(1 for r in df_fcl_failed if r['failure_type'] == 'INCOMPLETE_GENERATION')}")
    print(f"  FAILED with provider_status non-null: "
          f"{sum(1 for r in df_fcl_failed if r['provider_status'] is not None)}")
    print(f"  FAILED usages (provider usage block): "
          f"{[ (r['_coord'], r['usage']) for r in df_fcl_failed ]}")
    print(f"  FAILED validation_failure_type: "
          f"{Counter(r['validation_failure_type'] for r in df_fcl_failed)}")
    print(f"  PARTIAL provider_status values: "
          f"{Counter(r['provider_status'] for r in df_fcl_partial)}")

    # Non-cell INCOMPLETE_GENERATION receipts (the counter-examples to the attribution clause)
    outside = [r for r in ig if not cell(r)]
    print(f"\nINCOMPLETE_GENERATION receipts OUTSIDE deepseek-flash x fcl: {len(outside)}")
    for r in outside:
        print(f'  {r["_path"]}: status={r["status"]} '
              f'completion_tokens={usage_tokens(r)} finish_reason={r["finish_reason"]}'
              f' unresolved_reason={r["unresolved_reason"]!r}')

    print()
    print("=" * 78)
    print("CLAIM 2 — `INCOMPLETE_GENERATION`: 7 in F001 v1 (occurrences 01-06),")
    print("every one at finish_reason: length and exactly 8,192 completion tokens,")
    print("five returning zero bytes.")
    print("=" * 78)
    print(f"F001 v1 receipts (occ 01-06): {len(v1)}; occurrences 07-08: {len(v2)}")
    codes_v1 = Counter(r["failure_code"] for r in v1)
    print(f"failure_code counts in v1 (None = no failure): {dict(codes_v1)}")
    ig1 = [r for r in v1 if r.get("failure_code") == "INCOMPLETE_GENERATION"]
    print(f"\nINCOMPLETE_GENERATION in v1: {len(ig1)}")
    for r in ig1:
        art = r.get("artifact_sha256")
        print(f'  {r["_coord"]}: status={r["status"]} finish_reason={r["finish_reason"]} '
              f'completion_tokens={usage_tokens(r)} artifact_sha256={art} '
              f'returned_model={r.get("returned_model")}')
    print(f"  at finish_reason 'length': {sum(1 for r in ig1 if r['finish_reason'] == 'length')}")
    print(f"  at exactly 8192 completion tokens: {sum(1 for r in ig1 if usage_tokens(r) == 8192)}")
    print(f"  no artifact (artifact_sha256 null): {sum(1 for r in ig1 if not r.get('artifact_sha256'))}")
    print(f"  with an artifact (non-empty delivered bytes captured): "
          f"{sum(1 for r in ig1 if r.get('artifact_sha256'))}")
    with_art = [r["_coord"] for r in ig1 if r.get("artifact_sha256")]
    print(f"  coordinates carrying artifact_sha256: {with_art}")
    txt_anywhere = list(F001.rglob("*.txt"))
    print(f"  *.txt sibling files anywhere under F001: {len(txt_anywhere)}")
    # status table of v1 failures, to cross-read the 'five PARTIAL? no' question
    print(f"\n  statuses of the seven: {Counter(r['status'] for r in ig1)}")
    # Also check occurrences 07-08 for context
    codes_v2 = Counter(r["failure_code"] for r in v2)
    print(f"failure_code counts in 07-08 (context, not part of claim): {dict(codes_v2)}")

    print()
    print("=" * 78)
    print("CLAIM 3 — C001 occurrence-01: envelope_repairs on 93 of 240 calls")
    print("(strip_outer_code_fence 92, json_strict_false 1) against")
    print("strict_parse_would_succeed 122 of 240.")
    print("=" * 78)
    n = len(c001)
    repaired = [r for r in c001 if r["envelope_repairs"]]
    print(f"receipts: {n}")
    print(f"envelope_repairs non-empty: {len(repaired)}")
    flat = Counter(x for r in repaired for x in r["envelope_repairs"])
    print(f"repair-name counts (flattened): {dict(flat)}")
    multi = [r for r in repaired if len(r["envelope_repairs"]) > 1]
    print(f"receipts with more than one repair entry: {len(multi)}")
    for r in multi:
        print(f'  {r["_path"]}: {r["envelope_repairs"]}')
    null_repair = [r for r in c001 if r["envelope_repairs"] is None]
    print(f"envelope_repairs null (no delivery to decode): {len(null_repair)}")
    print(f"  statuses of the null-repair receipts: {Counter(r['status'] for r in null_repair)}")
    strict_true = [r for r in c001 if r["strict_parse_would_succeed"] is True]
    strict_false = [r for r in c001 if r["strict_parse_would_succeed"] is False]
    strict_null = [r for r in c001 if r["strict_parse_would_succeed"] is None]
    print(f"\nstrict_parse_would_succeed true:  {len(strict_true)}")
    print(f"strict_parse_would_succeed false: {len(strict_false)}")
    print(f"strict_parse_would_succeed null:  {len(strict_null)}")
    # Where did json_strict_false fire?
    jsf = [r for r in repaired if "json_strict_false" in r["envelope_repairs"]]
    print(f"\njson_strict_false coordinates: {[r['_coord'] for r in jsf]}")
    # cross-tab
    both = [r for r in c001 if r["envelope_repairs"] and r["strict_parse_would_succeed"] is True]
    print(f"repaired AND strict true: {len(both)}")
    rep_status = Counter(r["status"] for r in repaired)
    print(f"statuses of repaired receipts: {dict(rep_status)}")

    print()
    print("=" * 78)
    print("CROSS-CHECKS against the report's own section-2 wording")
    print("=" * 78)
    # 'Of the nine PARTIAL, eight are that cell at 8,192 and one is glm-5.3 fcl CONTROL rep2 at 32,768'
    p9 = [r for r in c001 if r["status"] == "PARTIAL"]
    print(f"PARTIAL receipts: {len(p9)}")
    for r in p9:
        print(f'  {r["_coord"]}: completion_tokens={usage_tokens(r)} '
              f'cell={r["_cell"]} repairs={r["envelope_repairs"]}')
    # 19 of 20 coords at 8192, eleven reasoning_tokens == 8192
    toks = [(r["_coord"], usage_tokens(r),
             (r["usage"] or {}).get("completion_tokens_details", {}).get("reasoning_tokens")
             if isinstance(r.get("usage"), dict) else None)
            for r in df_fcl]
    at8192 = [t for t in toks if t[1] == 8192]
    reasoning_full = [t for t in toks if t[2] == 8192]
    print(f"\ndeepseek-flash x fcl coords at completion_tokens 8192: {len(at8192)}")
    print(f"  of which reasoning_tokens 8192: {len(reasoning_full)}")
    print(f"  usage UNKNOWN (usage null) coords: "
          f"{[t[0] for t in toks if t[1] is None]}")
    f11_reasoning = [(r["_coord"],
                      (r["usage"] or {}).get("completion_tokens_details", {}).get("reasoning_tokens")
                      if isinstance(r.get("usage"), dict) else None,
                      usage_tokens(r)) for r in df_fcl_failed]
    print(f"  eleven FAILED (coord, reasoning_tokens, completion_tokens):")
    for t in f11_reasoning:
        print(f"    {t}")
    p9_reason = [(r["_coord"],
                  (r["usage"] or {}).get("completion_tokens_details", {}).get("reasoning_tokens")
                  if isinstance(r.get("usage"), dict) else None)
                 for r in df_fcl_partial]
    print(f"  nine PARTIAL (coord, reasoning_tokens):")
    for t in p9_reason:
        print(f"    {t}")
    # deepseek-flash prose 20/20 COMPLETE control
    prose = [r for r in c001 if r["_cell"] == ("deepseek-flash", "prose")]
    print(f"\ndeepseek-flash x prose receipts: {len(prose)}, statuses: "
          f"{Counter(r['status'] for r in prose)}, "
          f"completion tokens min/max: "
          f"{min(usage_tokens(r) for r in prose)}/{max(usage_tokens(r) for r in prose)}")
    rcp = Counter((r["_cell"][0], r["reasoning_content_present"]) for r in c001)
    print(f"reasoning_content_present on deepseek-flash receipts: "
          f"{dict((k, v) for k, v in rcp.items() if k[0] == 'deepseek-flash')}")


if __name__ == "__main__":
    main()
