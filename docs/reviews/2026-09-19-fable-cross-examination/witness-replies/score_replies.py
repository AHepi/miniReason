"""
What this file does
-------------------
Reads every reply in a folder and prints, per reply: length, finish reason, seconds,
whether the reply is empty, and which of the skill's report markers appear (so
"did the witness follow the method" can be checked before reading). It also probes
for each of the twenty-seven defect groups of file 21 with a few keywords per group,
as a first pass only; every hit and miss is then confirmed by reading.
Usage: python3 score_replies.py <reply_dir> [<reply_dir> ...]
"""
import json, glob, os, re, sys

HTV_MARKERS = ["frozen", "held", "loose", "idle", "borrowed", "unknown", "fitted", "built", "asserted",
               "change list", "remove", "swap", "flip", "poke", "reverse", "rival", "patch", "look inside", "next step"]
SC_MARKERS = ["correction", "scene", "sequence", "held", "free", "idle", "two routes", "plant", "pay", "choice test",
              "flip", "cost", "pattern count", "mirror", "unsure", "next step", "stock note"]
DEFECTS = {
 "1.1 five/six conjuncts": [r"five conditions", r"six conjunct", r"five conjunct", r"counts? (five|six)"],
 "1.2 owned/Can cycle": [r"\bowned\b.*\bCan\b|\bCan\b.*\bowned\b", r"ownership"],
 "1.3 active route / represented input": [r"active route", r"represented input"],
 "1.4 condition 3 definable": [r"definable as Sol", r"condition 3", r"projection of it"],
 "1.5 identity/modular lookup anchored": [r"identity transport", r"modular (table|lookup)", r"E ?= ?D"],
 "1.6 properness singleton": [r"single-?component", r"proper sub-?block", r"\|Γ\| ?= ?1|singleton"],
 "1.7 contract adequacy": [r"protective", r"contract adequacy", r"adequacy"],
 "1.8 baseline pairs excluded": [r"baseline pair", r"\(1, ?b\)", r"boundary-only|only in state"],
 "1.9 forward kind arity": [r"forward kind.*(anchor|subnetwork)", r"subnetwork"],
 "1.10 historical kinds borrow witnesses": [r"historical kind", r"provenance.*(component|question)"],
 "1.11 Sel clauses": [r"causally responsible", r"non-?triviality", r"blindness", r"no target instantiated"],
 "1.12 precedence rule": [r"precedence", r"constructed over selected|earliest"],
 "1.13 merit condition": [r"merit"],
 "1.14 Derivation 5": [r"Derivation 5", r"question-organization"],
 "1.15 surprise entails loss": [r"surprise", r"loss of \(R\)|Deploy"],
 "1.16 S K disjoint complements": [r"complement", r"S ?= ?K"],
 "1.17 C_adm typing": [r"C_adm.*(pair|typed|type)"],
 "1.18 Ans_E undefined": [r"Ans_E|Ans_S", r"query translation"],
 "1.19 arity slips (EK)": [r"\(EK\)", r"arity", r"system instantiates"],
 "1.20 reversed calculation parenthetical": [r"reversed? (calculation|organization)", r"parenthetical"],
 "1.21 Derivation 6 undefined predicates": [r"Derivation 6", r"problem-directed|explanatory use|role binding|Admit|Poss"],
 "1.22 Derivation 3 equivalence": [r"Derivation 3", r"sufficien.*surviv|surviv.*sufficien"],
 "1.23 Derivation 8 solution preservation": [r"Derivation 8", r"solution preserv"],
 "1.24 grain admissibility": [r"grain admissib", r"realizes"],
 "1.25 open cases mis-sorted": [r"symmetry", r"artefact|artifact", r"impossibility", r"mathematics"],
 "1.26 Part 0 dichotomy as fact": [r"Part 0", r"dichotomy|conjecture"],
 "1.27 smaller (relevant, β Ω, I3, understanding)": [r"\brelevant\b", r"β|Ω|beta|Omega", r"\(I3\)", r"understanding"],
}

def scan(folder):
    rows = []
    for f in sorted(glob.glob(os.path.join(folder, "*.json"))):
        j = json.load(open(f))
        r = j.get("reply") or ""
        u = j.get("usage") or {}
        markers = HTV_MARKERS if "htv" in folder or "rev" in folder else SC_MARKERS
        mk = sum(1 for m in markers if m in r.lower())
        hits = {k: any(re.search(p, r, re.I) for p in ps) for k, ps in DEFECTS.items()}
        rows.append((j["id"], j["sample"], len(r), u.get("finish_reason"), u.get("completion_tokens"), j.get("seconds"),
                     mk, len(markers), sum(hits.values()), hits, len(re.findall(r"^\s*(\d+)[\.\)]\s", r, re.M))))
    return rows

if __name__ == "__main__":
    for folder in sys.argv[1:]:
        rows = scan(folder)
        print(f"\n== {folder}: {len(rows)} replies, {sum(1 for r in rows if r[2]==0)} empty")
        for r in rows:
            print(f"  {r[0]:28s} s{r[1]} {r[2]:6d}ch fin={r[3]} tok={r[4]} {r[5]}s markers={r[6]}/{r[7]} defect-probes={r[8]}/27 numbered={r[10]}")
        agg = {}
        for r in rows:
            for k, v in r[9].items():
                agg[k] = agg.get(k, 0) + int(v)
        print("  probe hits per defect group (replies mentioning):")
        for k, v in agg.items():
            print(f"    {v:3d}  {k}")
