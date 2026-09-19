"""
What this file does
-------------------
Builds the run-level comparison table for file 26: for each (method, model) folder it
counts replies, empties, cut streams, and reports median/max reply length, seconds,
completion tokens and reasoning tokens, plus the share of replies that carry the
skill's report markers. Control = the plain run adjudicated in file 21.
Usage: python3 compare_runs.py
"""
import json, glob, os, statistics as st
RUNS = [("plain (file 21)", "deepseek-flash", "replies_rev_deepseek"),
        ("plain (file 21)", "Atria-Dawn-Preview", "replies_rev_atria"),
        ("hard-to-vary", "deepseek-flash", "replies_htv_deepseek"),
        ("hard-to-vary", "Atria-Dawn-Preview", "replies_htv_atria"),
        ("story-critique", "deepseek-flash", "replies_sc_deepseek"),
        ("story-critique", "Atria-Dawn-Preview", "replies_sc_atria")]
HTV = ["frozen", "held", "loose", "idle", "borrowed", "unknown", "next step"]
SC = ["correction", "unsure", "next step", "held", "free", "idle"]
def med(xs): return int(st.median(xs)) if xs else None
rows = []
for method, model, d in RUNS:
    fs = sorted(glob.glob(d + "/*.json"))
    if not fs: rows.append((method, model, 0)); continue
    js = [json.load(open(f)) for f in fs]
    replies = [j.get("reply") or "" for j in js]
    nonempty = [r for r in replies if r]
    usage = [j.get("usage") or {} for j in js]
    ct = [u.get("completion_tokens") for u in usage if u.get("completion_tokens")]
    rt = [(u.get("completion_tokens_details") or {}).get("reasoning_tokens") for u in usage]
    rt = [x for x in rt if x]
    secs = [j.get("seconds") for j in js if j.get("seconds")]
    marks = HTV if method == "hard-to-vary" else SC
    adher = [sum(1 for m in marks if m in r.lower()) >= len(marks) - 1 for r in nonempty]
    finds = [len(__import__("re").findall(r"(?im)^\s*(?:\*\*)?(?:F|N|Finding |Note )?\d+[\.\)]", r)) for r in nonempty]
    rows.append((method, model, len(js), len(js) - len(nonempty), med([len(r) for r in nonempty]), max(len(r) for r in nonempty) if nonempty else 0,
                 med(secs), max(secs) if secs else None, med(ct), med(rt) if rt else None, f"{sum(adher)}/{len(nonempty)}", med(finds)))
print("| Method | Model | Calls | Empty | Median chars | Max chars | Median s | Max s | Median completion tokens | Median reasoning tokens | Report markers present | Median numbered items |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    print("| " + " | ".join(str(x) for x in r) + " |")
