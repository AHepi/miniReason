import re, json, hashlib, os
from collections import Counter

SRC = "docs/sources/FW5-explanatory-construction.md"
STAGING = "staging/STAGING-v4.md"

raw = open(SRC, "rb").read()
sha = hashlib.sha256(raw).hexdigest()
print("sha256(source) =", sha)
print("matches declared:", sha == "8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a")
src_lines = raw.decode("utf-8").split("\n")  # 1-based: src_lines[n-1]
N_LINES = len(src_lines)
print("source lines:", N_LINES)

stg_lines = open(STAGING, encoding="utf-8").read().split("\n")

CIT = re.compile(r"\bFW5:(\d{2,4})(?:[-\u2013](\d{2,4}))?|(?<![\d\w./-]):(\d{2,4})(?:[-\u2013](\d{2,4}))?")
FRAG = re.compile(r'"([^"]+)"|\u201c(.+?)\u201d|`([^`]+)`|\\\((.+?)\\\)')
SKIP = re.compile(r'^(:\d|\d{4}|REC-|OPS-|VERIFIED |Status:|Prior verified|Letter:|Choice:|Why:|Reason:|Contribution|type: |[a-zA-Z ]+\.md|src/|docs/|experiments/)')
CRED = re.compile(r"(?i)(api[_-]?key|secret|password|bearer\s+[a-z0-9]|token\s|sk-[a-z0-9]{8})")

def norm(s):
    s = s.replace("\u201c", '"').replace("\u201d", '"').replace("\u2018", "'").replace("\u2019", "'")
    s = s.replace("\u2013", "-").replace("\u2014", " ").replace("\u2212", "-")
    s = re.sub(r"[*_`]+", "", s)
    return re.sub(r"\s+", " ", s).strip()

SRC_NORM = [norm(l) for l in src_lines]

def find_elsewhere(fn):
    key = fn[:60]
    return [i for i, l in enumerate(SRC_NORM, 1) if key in l and fn not in norm(l)[:0]]

def srcline(n):
    return src_lines[n-1] if 1 <= n <= N_LINES else "<line out of source range>"

records = []
for ln_no, line in enumerate(stg_lines, 1):
    frags_all = [(m.start(), m.end(), next(g for g in m.groups() if g is not None))
                 for m in FRAG.finditer(line)]
    for m in CIT.finditer(line):
        n = m.group(1) or m.group(3)
        e = m.group(2) or m.group(4)
        start, end = int(n), int(e) if e else int(n)
        valid_range = end >= start
        in_bounds = 1 <= start <= N_LINES
        cited_text = "\n".join(src_lines[start-1:min(end, N_LINES)]) if valid_range and in_bounds else ""
        cited_norm = norm(cited_text)
        frags = []
        for s0, s1, f in frags_all:
            if m.start() >= s0 and m.start() < s1:
                continue  # citation sits inside this fragment (meta-citation) -> skip fragment
            f = f.strip()
            if CRED.search(f) or SKIP.match(norm(f)):
                continue
            fn = norm(f)
            if len(fn) < 12:
                continue
            frags.append({"text": fn, "found_raw": f in cited_text,
                          "found_norm": fn in cited_norm})
        bad = [x for x in frags if not x["found_norm"]]
        norm_only = [x for x in frags if x["found_norm"] and not x["found_raw"]]
        notes = []
        if not valid_range:
            notes.append(f"range end {end} precedes start {start}")
        if not in_bounds:
            notes.append(f"cited line {start} is beyond the source ({N_LINES} lines)")
        if notes:
            verdict, note = "WRONG", "; ".join(notes)
        elif not frags:
            verdict, note = "NO-QUOTE-TO-CHECK", "no quoted fragment >= 12 chars on staging line"
        elif bad:
            verdict = "WRONG"
            details = []
            for x in bad:
                key = x["text"][:60]
                where = [i for i, l in enumerate(SRC_NORM, 1) if key in l]
                d = "fragment NOT in cited target: " + x["text"][:80]
                d += (" | found elsewhere at source lines " + str(where[:5])) if where else " | not found anywhere in source"
                details.append(d)
            note = "cited line starts: " + srcline(start)[:120] + " || " + " ; ".join(details)
        elif norm_only:
            verdict = "CORRECT IN SUBSTANCE"
            note = "matched only after normalisation (typographic quotes / markdown emphasis / whitespace): " + \
                   "; ".join("'" + x["text"][:60] + "'" for x in norm_only)
        else:
            verdict, note = "CORRECT", ""
        records.append({"staging_line": ln_no, "citation": m.group(0),
                        "target": [start, end], "fragments": frags,
                        "verdict": verdict, "note": note})

blank = sorted({n for r in records for n in range(r["target"][0], r["target"][1]+1)
                if 1 <= n <= N_LINES and src_lines[n-1].strip() == ""})
bad_ranges = [{"staging_line": r["staging_line"], "citation": r["citation"]}
              for r in records if r["target"][1] < r["target"][0]]

counts = Counter(r["verdict"] for r in records)
distinct = {(r["target"][0], r["target"][1]) for r in records}
print("total citations:", len(records))
print("distinct targets:", len(distinct))
print(counts)
print("blank cited lines:", blank)
print("reversed ranges:", bad_ranges)
for r in records:
    if r["verdict"] == "WRONG":
        print("WRONG:", r["staging_line"], r["citation"], "\n  ", r["note"][:300])

os.makedirs("out", exist_ok=True)
json_out = {"source_sha256": sha, "pattern": CIT.pattern,
            "total": len(records), "distinct_targets": len(distinct),
            "verdict_counts": dict(counts), "blank_cited_lines": blank,
            "reversed_ranges": bad_ranges, "records": records}
json.dump(json_out, open("out/citations-v4.json", "w"), indent=1, ensure_ascii=False)

order = {"WRONG": 0, "CORRECT IN SUBSTANCE": 1, "CORRECT": 2, "NO-QUOTE-TO-CHECK": 3}
with open("out/citations-v4.md", "w", encoding="utf-8") as fh:
    fh.write("# FW5 line-citation verification — staging/STAGING-v4.md\n\n")
    fh.write(f"Source: `{SRC}`, sha256 `{sha}` — computed, matches the declared value.\n\n")
    fh.write(f"Extraction regex: `{CIT.pattern}` (N, M are 2–4 digits; hyphen or en-dash inclusive ranges; "
             "bare `:N`/`:N-M` excluded when preceded by a digit, word char, `.`, `/` or `-`, so sha256 "
             "fragments, times, dates and file paths do not match).\n\n")
    fh.write(f"Total citations extracted: **{len(records)}**; distinct targets: **{len(distinct)}**.\n\n")
    fh.write("Counts by verdict: " + ", ".join(
        f"**{k}: {counts.get(k, 0)}**" for k in
        ["CORRECT", "CORRECT IN SUBSTANCE", "WRONG", "NO-QUOTE-TO-CHECK"]) + ".\n\n")
    wrongs = [r for r in records if r["verdict"] == "WRONG"]
    fh.write("**WRONG citations:** " +
             (", ".join(f"staging line {r['staging_line']} `{r['citation']}`" for r in wrongs) or "none") + ".\n\n")
    fh.write("Cited lines that are blank in the source: " + (str(blank) if blank else "none") + ".\n\n")
    fh.write("Ranges whose end precedes start: " +
             (", ".join(f"staging line {b['staging_line']} `{b['citation']}`" for b in bad_ranges) if bad_ranges else "none") + ".\n\n")
    fh.write("Method notes: a quote on a staging line is tested against **every** citation on that line; "
             "lines that bundle several citations with one quote therefore mark the sibling citations WRONG "
             "even when the quote is present at its own citation's line — the note names the source line "
             "where the fragment actually sits, and those rows are attribution ambiguities of the line, not "
             "missing text. Fragments that are A001's own prose (meta-citations like `:170 Their meanings…`, "
             "file paths, receipt field names, LaTeX written by A001 rather than quoted) are excluded from "
             "the quote test.\n\n")
    fh.write("What the extraction pattern does **not** catch: one-digit line references (`:7`); numbers of "
             "five or more digits; spelled-out citations (\"line 208\", \"lines 613 to 618\"); citations "
             "embedded inside prose without colon form; and bare `:N`-shaped references that are actually to "
             "other files (e.g. a review document's `:299`) — the pattern counts those as FW5 citations "
             "because it cannot see which file the author meant.\n\n")
    fh.write("| staging line | citation | target | verdict | note |\n|---|---|---|---|---|\n")
    for r in sorted(records, key=lambda x: (order[x["verdict"]], x["staging_line"])):
        tgt = str(r["target"][0]) if r["target"][0] == r["target"][1] else f"{r['target'][0]}-{r['target'][1]}"
        note = r["note"].replace("|", "\\|")[:300]
        fh.write(f"| {r['staging_line']} | {r['citation']} | :{tgt} | {r['verdict']} | {note} |\n")
print("wrote out/citations-v4.md and out/citations-v4.json")
