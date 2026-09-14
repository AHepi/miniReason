#!/usr/bin/env python3
"""Steps 2-4 of the FW5 citation verification.

Per citation on a staging line: collect the line's quoted fragments (straight or
typographic double quotes, backticks, \\( ... \\) LaTeX spans), filter out
non-quote artifacts, assign each remaining fragment to its nearest citation,
test it against the cited line/range.

Fragment filtering (every filtered span is listed in the report):
  short      < 12 chars after normalisation
  symbolonly backtick span with no alphabetic character (e.g. `\\[`)
  pointer    the span is a citation-shaped artifact (':35-47', ':1208-1218',
             "':170'") or a bare pointer ('" FW5:228 — "')
  boundary   closing-quote anomaly: the span's closing quote touches a
             citation, a closing paren, or closing emphasis (quote-boundary
             artifacts such as '... FW5:728 (' or ', not under :1362's '),
             or (straight quotes only) the span's closing quote is a dangling
             quote by the line's quote parity.  If eliding citation text from
             such a span yields a match, the span is instead TESTED in that
             form (status cite_stripped) and the anomaly is named.

Match levels per tested fragment:
  verbatim       raw fragment is a raw substring of the raw cited line/range
  normalised     substring after typographic->straight quotes + whitespace
                 collapse (the task's declared normalisation); difference named
  cite_stripped  matches only with citation text embedded in the quoted span
                 elided; named
  ellipsis       fragment contains an ellipsis and every part separated by it
                 matches the cited line(s) individually (not verbatim, so it
                 counts under CORRECT IN SUBSTANCE); named
  emphasis       matches only after also removing markdown emphasis markers
                 (``**``/``__``) from both sides; named explicitly
  not_found      none of the above: the cited line's first 120 chars are
                 shown plus a grep of the whole normalised source saying where
                 the text actually is, or that it is the staging document's
                 own prose.

Rehoming: a fragment matching nothing for its own citation but matching
another target cited on the same staging line is moved to that citation's
fragment list (with a note) instead of counting against either.

Verdicts:
  CORRECT                every tested fragment is verbatim
  CORRECT IN SUBSTANCE   every tested fragment matched, at least one not
                         verbatim (the difference is named)
  WRONG                  some tested (12+ char) fragment matched nothing cited
                         on the line
  NO-QUOTE-TO-CHECK      no testable fragment for this citation
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from citecommon import (SRC, STAGING, Source, fragments_on_line, load_lines,
                        normalise, norm_typo, MIN_FRAG)

src = Source(load_lines(SRC))
staging_lines = load_lines(STAGING)
hits = json.load(open("out/extracted.json", encoding="utf-8"))["hits"]

line_cits = defaultdict(list)
for h in hits:
    line_cits[h["staging_line"]].append(h)
line_frags = {ln: fragments_on_line(staging_lines[ln - 1]) for ln in line_cits}

PTR_FULL = re.compile(r"^\s*(?:FW5)?:?\d{2,4}[-\u2013:]?\d*\s*(?:\u2014|-|\.)?\s*$")
CITE_STRIP = re.compile(r"(?:FW5)?:\d{2,4}(?:[-\u2013]:?\d{2,4})?")
HAS_ALPHA = re.compile(r"[A-Za-z\u00C0-\u017F]")
ELLIPSIS = re.compile(r"\u2026|\.\.\.")


def emph_strip(s):
    return s.replace("**", "").replace("__", "")


def collapse_changes(frag):
    t = norm_typo(frag)
    return re.sub(r"\s+", " ", t).strip() != t


def ellipsis_parts_ok(frag, target_norm):
    parts = [normalise(p) for p in ELLIPSIS.split(norm_typo(frag))]
    parts = [p for p in parts if len(p) >= 8]
    return len(parts) >= 2 and all(p in target_norm for p in parts)


def match_result(frag, target_raw):
    """Return (status, note) or None."""
    if frag in target_raw:
        return "verbatim", ""
    nfrag = normalise(frag)
    tnorm = normalise(target_raw)
    if nfrag in tnorm:
        diffs = []
        if norm_typo(frag) != frag:
            diffs.append("typographic quotes straightened")
        if collapse_changes(frag):
            diffs.append("whitespace collapsed")
        return "normalised", "; ".join(diffs) or "whitespace/quote normalisation"
    stripped = CITE_STRIP.sub("", frag)
    estripped = emph_strip(stripped)
    if stripped != frag and normalise(stripped) in tnorm:
        return "cite_stripped", "citation text embedded in the quoted span elided"
    if (stripped != frag or estripped != frag) and \
            normalise(estripped) in normalise(emph_strip(target_raw)):
        if estripped != stripped and stripped != frag:
            return "cite_stripped", "citation text embedded in the quoted span elided and emphasis markers removed"
        if stripped != frag:
            return "cite_stripped", "citation text embedded in the quoted span elided"
        return "emphasis", "markdown emphasis markers (**) present only on one side (removed for the test)"
    if ellipsis_parts_ok(frag, tnorm):
        return "ellipsis_parts", ("the fragment contains an ellipsis, so it is not verbatim, but "
                                  "every part separated by the ellipsis matches the cited line(s) individually")
    return None


def elsewhere(frag, exclude):
    """Grep the whole source (normalised) for the fragment: per line; then
    citation-stripped; then emphasis-stripped; then spanning."""
    nf = normalise(frag)
    got = [i for i in src.find_lines(nf) if not (exclude[0] <= i <= exclude[1])]
    if got:
        return "found elsewhere at source line(s) " + ",".join(map(str, got))
    stripped = CITE_STRIP.sub("", frag)
    if stripped != frag:
        nsf = normalise(stripped)
        got = [i for i in src.find_lines(nsf) if not (exclude[0] <= i <= exclude[1])]
        if got:
            return ("found elsewhere at source line(s) " + ",".join(map(str, got))
                    + " once the citation text embedded in the quoted span is elided")
        nsf = normalise(emph_strip(stripped))
        got = [i for i in src.find_lines(nsf) if not (exclude[0] <= i <= exclude[1])]
        if got:
            return ("found elsewhere at source line(s) " + ",".join(map(str, got))
                    + " once embedded citation text and emphasis markers are removed")
    nef = normalise(emph_strip(frag))
    if nef != nf:
        got = [i for i in src.find_lines(nef) if not (exclude[0] <= i <= exclude[1])]
        if got:
            return ("found elsewhere at source line(s) " + ",".join(map(str, got))
                    + " once markdown emphasis is removed from both sides")
    sp = src.find_anywhere(nf)
    if sp and not (exclude[0] <= sp <= exclude[1]):
        return f"found spanning source line {sp}"
    return "not found anywhere in the source (it is the staging document's own prose, not a quote of FW5)"


def dist(a0, a1, b0, b1):
    if a1 <= b0:
        return b0 - a1
    if b1 <= a0:
        return a0 - b1
    return 0


records = []
excluded_spans = []  # (staging_line, reason, span_text)
for ln in sorted(line_cits):
    occ = line_cits[ln]
    ln_text = staging_lines[ln - 1]
    frags = [dict(f) for f in line_frags[ln]]
    for f in frags:
        f["end"] = f["start"] + len(f["fragment"])
        f["norm_len"] = len(normalise(f["fragment"]))
        f["qend"] = f["end"] + (2 if f["style"] == "latex" else 1)
        f["skip_reason"] = None
        frag = f["fragment"]
        if f["norm_len"] < MIN_FRAG:
            f["skip_reason"] = "short"
        elif f["style"] == "backtick" and not HAS_ALPHA.search(frag):
            f["skip_reason"] = "symbolonly"
        elif PTR_FULL.match(frag):
            f["skip_reason"] = "pointer"
        if f["skip_reason"] and f["skip_reason"] != "short":
            excluded_spans.append((ln, f["skip_reason"], frag[:90]))

    # merge same-line occurrences of the same target
    merged, seen = [], {}
    for h in occ:
        key = (h["start"], h["end"])
        if key in seen:
            seen[key]["occurrences"].append(h["citation"])
        else:
            rec = {"staging_line": ln, "citation": h["citation"],
                   "start": h["start"], "end": h["end"],
                   "occurrences": [h["citation"]], "fragments": []}
            seen[key] = rec
            merged.append(rec)
    merged_by_key = {(r["start"], r["end"]): r for r in merged}

    cites_with_span = []
    pos = 0
    for h in occ:
        idx = ln_text.index(h["citation"], pos)
        cites_with_span.append((h["start"], h["end"], idx, idx + len(h["citation"])))
        pos = idx + len(h["citation"])

    def owner_of(f):
        best = min(cites_with_span, key=lambda c: dist(f["start"], f["end"], c[2], c[3]))
        return (best[0], best[1])

    straight_q_count = ln_text.count('"')

    # --- boundary-anomaly pass (quotes only) ---
    for f in frags:
        if f["skip_reason"]:
            continue
        if f["style"] not in ("straight", "typographic"):
            continue
        bad = False
        extension = ""
        # citation touching the closing quote
        if any(dist(f["qend"], f["qend"] + 1, c[2], c[3]) == 0 for c in cites_with_span):
            bad = True
        # ") closing immediately after the closing quote (* emphasis too)
        ch1 = ln_text[f["qend"]:f["qend"] + 1]
        ch2 = ln_text[f["qend"] + 1:f["qend"] + 2]
        ch3 = ln_text[f["qend"] + 2:f["qend"] + 3]
        for a, b in ((ch1, ln_text[f["qend"] - 1:f["qend"]]), (ch2, ch1), (ch3, ch2)):
            if a == ")" and b != "\\":
                bad = True
            if a == "*" and b == "*":
                bad = True
        if f["style"] == "straight":
            if ch1 == '"' and straight_q_count % 2 == 1:
                bad = True
                nxt = ln_text.find('"', f["qend"] + 1)
                if nxt > 0:
                    extension = ln_text[f["qend"] + 1:nxt]
            closing_idx = f["qend"]  # index of the closing '"' char
            if straight_q_count % 2 == 0 and ln_text.find('"', closing_idx + 1) < 0:
                bad = True
        if not bad:
            continue
        # recovery attempt with citation text elided (and unmatched-quote extension)
        key = owner_of(f)
        rec = merged_by_key[key]
        rec_target = src.target_raw(rec["start"], rec["end"])
        ml = match_result(f["fragment"] + extension, rec_target)
        if ml is not None and ml[0] == "cite_stripped":
            rec["fragments"].append(
                {"fragment": f["fragment"] + extension if extension else f["fragment"],
                 "style": f["style"], "status": "cite_stripped",
                 "note": "closing-quote anomaly on the span: " + ml[1]})
        else:
            f["skip_reason"] = "boundary"
            excluded_spans.append((ln, "boundary",
                                   (f["fragment"] + extension)[:90]))

    # --- test pass ---
    for f in frags:
        if f["skip_reason"]:
            if f["skip_reason"] == "short":
                key = owner_of(f)
                merged_by_key[key]["fragments"].append(
                    {"fragment": f["fragment"], "style": f["style"], "status": "short",
                     "note": f"< {MIN_FRAG} chars after normalisation, not tested"})
            continue
        key = owner_of(f)
        rec = merged_by_key[key]
        target_raw = src.target_raw(rec["start"], rec["end"])
        ml = match_result(f["fragment"], target_raw)
        if ml is not None:
            rec["fragments"].append(
                {"fragment": f["fragment"], "style": f["style"], "status": ml[0],
                 "note": ml[1]})
            continue
        # rehome to a co-cited target on the same line, if any
        rehomed = None
        for other in merged:
            if (other["start"], other["end"]) == key:
                continue
            otr = src.target_raw(other["start"], other["end"])
            ml2 = match_result(f["fragment"], otr)
            if ml2 is not None:
                rehomed = (other, ml2)
                break
        if rehomed:
            other, ml2 = rehomed
            other["fragments"].append(
                {"fragment": f["fragment"], "style": f["style"], "status": ml2[0],
                 "note": ((ml2[1] + " ") if ml2[1] else "") +
                         f"(nearest citation on its line was {rec['citation']}; the text is in this co-cited target)"})
            continue
        # not found anywhere on the line's targets
        notes = []
        if ELLIPSIS.search(norm_typo(f["fragment"])):
            parts = [normalise(p) for p in ELLIPSIS.split(norm_typo(f["fragment"]))]
            parts = [p for p in parts if len(p) >= 8]
            miss = [p for p in parts if p not in normalise(target_raw)]
            notes.append(f"contains an ellipsis; {len(miss)} of {len(parts)} parts separated "
                         f"by it are not in the cited line(s): {miss[0][:70]!r}")
        notes.append(elsewhere(f["fragment"], (rec["start"], rec["end"])))
        rec["fragments"].append(
            {"fragment": f["fragment"], "style": f["style"], "status": "not_found",
             "note": "; ".join(notes)})

    # --- verdicts ---
    for rec in merged:
        target_raw = src.target_raw(rec["start"], rec["end"])
        results = rec["fragments"]
        testable = [r for r in results
                    if r["status"] in ("verbatim", "normalised", "cite_stripped",
                                       "ellipsis_parts", "emphasis", "not_found")]
        if not testable:
            verdict = "NO-QUOTE-TO-CHECK"
            if not results:
                note = "no quoted fragment on the staging line"
            else:
                note = (f"{len(results)} quoted fragment(s) on the line, all < "
                        f"{MIN_FRAG} chars after normalisation, none tested")
        elif any(r["status"] == "not_found" for r in testable):
            verdict = "WRONG"
            note = " | ".join(f"[{r['style']}] {r['fragment'][:100]!r}: {r['note']}"
                               for r in testable if r["status"] == "not_found")
        elif any(r["status"] != "verbatim" for r in testable):
            verdict = "CORRECT IN SUBSTANCE"
            note = " | ".join(f"[{r['style']}] {r['fragment'][:80]!r}: {r['note']}"
                              for r in testable if r["status"] != "verbatim")
        else:
            verdict = "CORRECT"
            note = ""
        rec["cited_first_120"] = target_raw[:120]
        rec["cited_blank"] = target_raw.strip() == ""
        rec["inverted_range"] = rec["end"] < rec["start"]
        rec["verdict"] = verdict
        rec["note"] = note
        records.append(rec)

json.dump(records, open("out/verdicts-raw.json", "w", encoding="utf-8"), indent=2)

# ---------------------------------------------------------------- diagnostics
diag = open("out/diagnostics.txt", "w", encoding="utf-8")
c = Counter(r["verdict"] for r in records)
occ_total = sum(len(r["occurrences"]) for r in records)
diag.write(f"citation occurrences: {occ_total}\n")
diag.write(f"merged (same-line,same-target) citation records: {len(records)}\n")
diag.write(f"distinct targets: {len({(r['start'], r['end']) for r in records})}\n")
diag.write(f"verdict counts over records: {dict(c)}\n")
diag.write(f"excluded spans by reason: {Counter(r for _, r, _ in excluded_spans)}\n\n")

for v in ("WRONG", "CORRECT IN SUBSTANCE"):
    diag.write(f"===== {v} =====\n")
    for r in records:
        if r["verdict"] != v:
            continue
        tgt = f":{r['start']}" + (f"-{r['end']}" if r['end'] != r['start'] else "")
        diag.write(f"\nstaging L{r['staging_line']} cite {r['citation']} -> {tgt}\n")
        diag.write(f"  cited first 120: {r['cited_first_120']!r}\n")
        for fr in r["fragments"]:
            if fr["status"] not in ("verbatim", "short"):
                diag.write(f"  [{fr['style']}/{fr['status']}] {fr['fragment'][:170]!r}\n")
                diag.write(f"      note: {fr['note']}\n")

diag.write("\n===== CORRECT (full listing) =====\n")
for r in records:
    if r["verdict"] == "CORRECT":
        frags = [f["fragment"][:70] for f in r["fragments"] if f["status"] == "verbatim"]
        diag.write(f"L{r['staging_line']} {r['citation']} -> :{r['start']}"
                   f"{'-' + str(r['end']) if r['end'] != r['start'] else ''}  {frags}\n")

diag.write("\n===== NO-QUOTE-TO-CHECK with short fragments =====\n")
for r in records:
    if r["verdict"] == "NO-QUOTE-TO-CHECK":
        for f in r["fragments"]:
            if f["status"] == "short":
                diag.write(f"L{r['staging_line']} {r['citation']} short[{f['style']}]: {f['fragment'][:140]!r}\n")

diag.write("\n===== excluded spans =====\n")
for ln_, reason, txt in excluded_spans:
    diag.write(f"L{ln_} {reason}: {txt!r}\n")

diag.write("\n===== cited blank targets / inverted ranges =====\n")
for r in records:
    if r["cited_blank"] or r["inverted_range"]:
        diag.write(f"L{r['staging_line']} {r['citation']} blank={r['cited_blank']} inverted={r['inverted_range']}\n")
diag.close()
print(open("out/diagnostics.txt", encoding="utf-8").read())
