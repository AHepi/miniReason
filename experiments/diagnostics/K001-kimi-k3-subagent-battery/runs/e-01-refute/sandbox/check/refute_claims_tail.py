#!/usr/bin/env python3
"""Tail cross-checks for the C001 section-2 wording that accompanies claims 1 and 3.

Run: python3 check/refute_claims_tail.py
"""
import json
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
C001 = ROOT / "experiments/diagnostics/C001-contrast-triple/occurrence-01/responses"

recs = []
for p in sorted(C001.glob("*/*/*/rep*.json")):
    d = json.loads(p.read_text(encoding="utf-8"))
    d["_coord"] = (
        f'{d["coordinate"]["endpoint_slug"]}/{d["coordinate"]["arm"]}/'
        f'{d["coordinate"]["case"]}/rep{d["coordinate"]["replicate"]}'
    )
    d["_cell"] = (d["coordinate"]["endpoint_slug"], d["coordinate"]["arm"])
    recs.append(d)

def ct(r):
    u = r.get("usage")
    return u.get("completion_tokens") if isinstance(u, dict) else None

def rt(r):
    u = r.get("usage")
    if isinstance(u, dict):
        return (u.get("completion_tokens_details") or {}).get("reasoning_tokens")
    return None

cell = [r for r in recs if r["_cell"] == ("deepseek-flash", "fcl")]
p9 = [r for r in recs if r["status"] == "PARTIAL"]
print(f"PARTIAL receipts: {len(p9)}")
for r in p9:
    print(f'  {r["_coord"]}: completion_tokens={ct(r)} reasoning_tokens={rt(r)}')

at8192 = [r for r in cell if ct(r) == 8192]
print(f"\ndeepseek-flash x fcl at completion_tokens 8192: {len(at8192)} of 20")
print(f"  with reasoning_tokens == 8192: {sum(1 for r in at8192 if rt(r) == 8192)}")
print(f"  with usage null: {sum(1 for r in cell if r.get('usage') is None)}")
f11 = [r for r in cell if r["status"] == "FAILED"]
print(f"\neleven FAILED (coord, status, usage null, reasoning_tokens, completion_tokens):")
for r in f11:
    print(f'  {r["_coord"]}: usage_null={r.get("usage") is None} rt={rt(r)} ct={ct(r)}')
pd8 = [r for r in cell if r["status"] == "PARTIAL"]
print(f"\neight PARTIAL of the cell (coord, reasoning_tokens):")
for r in pd8:
    print(f'  {r["_coord"]}: rt={rt(r)}')
vals = sorted(rt(r) for r in pd8)
print(f"  reasoning range: {vals[0]}..{vals[-1]}")

prose = [r for r in recs if r["_cell"] == ("deepseek-flash", "prose")]
print(f"\ndeepseek-flash x prose: n={len(prose)} statuses={dict(Counter(r['status'] for r in prose))}")
cts = sorted(ct(r) for r in prose)
print(f"  completion_tokens range: {cts[0]}..{cts[-1]}")

ds = [r for r in recs if r["_cell"][0] == "deepseek-flash"]
print(f"\ndeepseek-flash receipts: {len(ds)}; reasoning_content_present counts: "
      f"{dict(Counter(r['reasoning_content_present'] for r in ds))}")

# which coordinates carry json_strict_false / where strict true sits per arm
jsf = [r for r in recs if r["envelope_repairs"] and "json_strict_false" in r["envelope_repairs"]]
print(f"\njson_strict_false coordinates: {[r['_coord'] for r in jsf]}")
by_status_strict = Counter((r["status"], r["strict_parse_would_succeed"]) for r in recs)
print(f"(status, strict_parse_would_succeed) cross-tab: {dict(by_status_strict)}")
rep_strict_false = [r["_coord"] for r in recs
                    if r["envelope_repairs"] and r["strict_parse_would_succeed"] is False]
print(f"repaired and strict false: {len(rep_strict_false)}")
unrepaired_delivered = [r for r in recs
                        if r["envelope_repairs"] == [] and r["strict_parse_would_succeed"] is not None]
unrep_false = [r for r in unrepaired_delivered if r["strict_parse_would_succeed"] is False]
unrep_true = [r for r in unrepaired_delivered if r["strict_parse_would_succeed"] is True]
print(f"delivered receipts: {len(unrepaired_delivered) + len([r for r in recs if r['envelope_repairs']])}")
print(f"unrepaired delivered and strict false: {len(unrep_false)}")
print(f"unrepaired delivered and strict true:  {len(unrep_true)}")
print(f"OPAQUE envelopes: {sum(1 for r in recs if r['envelope_status'] == 'OPAQUE')}")
print(f"AUTHORED envelopes: {sum(1 for r in recs if r['envelope_status'] == 'AUTHORED')}")
