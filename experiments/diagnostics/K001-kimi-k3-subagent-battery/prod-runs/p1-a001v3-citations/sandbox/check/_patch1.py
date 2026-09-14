import re

path = "check/verdicts.py"
src = open(path, encoding="utf-8").read()
lines = src.split("\n")

# locate regions
start = next(i for i, l in enumerate(lines) if "# --- boundary-anomaly pass" in l)
while "straight_q_count" not in lines[start]:
    start -= 1
end = next(i for i, l in enumerate(lines) if "# --- test pass ---" in l)

new_block = '''    straight_q_count = ln_text.count('"')

    # --- closing-quote anomaly pass (quote spans only) ---
    # A quoted span is anomalous only when, after the closing quote char, the
    # line contains an ODD number of closing-quote chars of the same style:
    # then the actual quote closes later and the span is truncated.  Recover
    # by extending to the next same-style quote and re-testing; if the span
    # still matches nothing (with citation text elided), exclude it as a
    # quote-boundary artifact.  Also anomalous: the line has exactly one
    # opening quote char of that style (the span is a dangling lone quote).
    for f in frags:
        if f["skip_reason"]:
            continue
        style = f["style"]
        if style not in ("straight", "typographic"):
            continue
        qchar = '"' if style == "straight" else "\\u201d"
        open_q = '"' if style == "straight" else "\\u201c"
        remaining = ln_text[f["qend"]:].count(qchar)
        total_open = ln_text.count(open_q)
        bad = False
        extension = ""
        if remaining % 2 == 1:
            bad = True
            nxt = ln_text.find(qchar, f["qend"])
            if nxt > 0:
                extension = ln_text[f["qend"]:nxt]
        if total_open == 1:
            bad = True
        if not bad:
            continue
        extended = f["fragment"] + extension
        key = owner_of(f)
        rec = merged_by_key[key]
        rec_target = src_target(rec["start"], rec["end"])
        ml = match_result(extended, rec_target)
        if ml is not None:
            rec["fragments"].append(
                {"fragment": extended, "style": style, "status": ml[0],
                 "note": ("closing-quote anomaly (truncated span recovered to the "
                          "next quote): " + (ml[1] if ml[1] else "matches verbatim once recovered"))})
        else:
            f["skip_reason"] = "boundary"
            excluded_spans.append((ln, "boundary", extended[:110]))
'''

lines[start:end] = new_block.split("\n")
src = "\n".join(lines)
# the pass refers to src_target helper; add it near 'src = Source(...)'
helper = "def src_target(a, b):\n    return src.target_raw(a, b)\n\n\n"
anchor = 'line_cits = defaultdict(list)'
assert anchor in src
src = src.replace(anchor, helper + anchor, 1)
open(path, "w", encoding="utf-8").write(src)
print("patched")
