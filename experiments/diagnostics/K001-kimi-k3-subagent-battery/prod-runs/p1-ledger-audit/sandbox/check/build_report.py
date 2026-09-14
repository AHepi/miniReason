"""Build out/ledger-audit.json and out/ledger-audit.md from the computed audit.

Everything is recomputed from docs/DECISION_LEDGER.md via check/common.py.
"""
import json
import os

import common

LIMITATIONS = (
    "What these patterns would NOT catch: they match fixed byte patterns on "
    "whole lines, so anything presented differently is invisible to them. A "
    "receipt id split across lines (for example a line break inside "
    "'REC-20260914-') matches nothing on either side, and the same is true of "
    "a VERIFIED/TREE line whose hashes wrap onto the next line. Ids with "
    "lowercase letters, a wrong-length date field, extra characters glued on "
    "either end, or 'REC' written with look-alike characters are not "
    "receipt ids as far as the pattern is concerned. A 40-hex commit or tree "
    "shorter than 40 digits, uppercase, or separated from 'VERIFIED'/'TREE' "
    "by different spacing escapes item 6, and a 'Prior verified commit/tree:' "
    "line with extra inner spacing or a trailing colon variant is missed by "
    "item 5. Entry counting by 'starts with REC-/'**REC-' on lines and "
    "blocks cannot see receipts introduced mid-sentence (for example 'See "
    "REC-...'), indented occurrences, or two receipts opened inside one "
    "paragraph, and paragraph splitting depends entirely on blank lines. The "
    "credential scan is only as strong as its two regular expressions: "
    "credentials of any other shape (different length, characters, or "
    "prefix, or broken across lines) would not be found, so zero hits means "
    "'no match to these two patterns', not 'the file contains no secret of "
    "any kind'. Finally, line numbers are 1-based over raw split lines and "
    "presume the file is UTF-8; a file whose final line lacks a terminator "
    "or that mixes endings is handled, but counts refer to the exact current "
    "bytes, and any later append invalidates them."
)


def md_line_list_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(str(x) for x in row) + " |")
    if len(rows) == 0:
        out.append("| " + " | ".join(["(none)"] + [""] * (len(headers) - 1)) + " |")
    return "\n".join(out)


def build():
    lines = common.load_lines()
    census = common.line_census(lines)
    ids = common.receipt_ids(lines)
    today = common.today_receipts(ids)
    entries = common.entry_counts(lines)
    prior = common.prior_marker(lines)
    verified = common.verified_tree(lines)
    creds = common.credential_scan(lines)
    tail = common.last_five(lines)

    audit = {
        "audit_subject": {
            "path": common.LEDGER_PATH,
        },
        "line_census": census,
        "receipt_ids": {
            "pattern": common.RECEIPT_PATTERN,
            "distinct_count": len(ids),
            "ids": ids,
        },
        "today_receipts": today,
        "entry_counts": entries,
        "prior_verified_marker": prior,
        "verified_tree_lines": verified,
        "credential_scan": creds,
        "last_five_lines": tail,
    }

    os.makedirs(common.OUT_DIR, exist_ok=True)
    with open(os.path.join(common.OUT_DIR, "ledger-audit.json"), "w",
              encoding="utf-8") as fh:
        json.dump(audit, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    md = []
    md.append("# Mechanical audit of `docs/DECISION_LEDGER.md`")
    md.append("")
    md.append("Subject file: `%s`. Computed by the scripts under `check/`; "
              "no value is transcribed." % common.LEDGER_PATH)
    md.append("")
    md.append("## 1. Line census")
    md.append("")
    md.append(md_line_list_table(
        ["metric", "value"],
        [["total lines", census["total_lines"]],
         ["lines ending CRLF (\\r\\n)", census["crlf_line_count"]],
         ["lines ending bare LF (\\n)", census["bare_lf_line_count"]],
         ["unterminated final line count",
          census["unterminated_final_line_count"]]]))
    md.append("")
    md.append("CRLF line numbers: "
              + (", ".join(str(n) for n in census["crlf_line_numbers"])
                 if census["crlf_line_numbers"] else "(none)"))
    md.append("")
    md.append("## 2. Receipt ids (`%s`), first-appearance order"
              % common.RECEIPT_PATTERN)
    md.append("")
    md.append("Distinct ids: **%d**" % len(ids))
    md.append("")
    md.append(md_line_list_table(
        ["id", "first appearance line", "lines carrying id"],
        [[r["id"], r["first_appearance_line"], r["lines_carrying_id"]]
         for r in ids]))
    md.append("")
    md.append("## 3. Today's receipts (date %s)" % today["date"])
    md.append("")
    md.append(md_line_list_table(
        ["metric", "value"],
        [["distinct ids dated %s" % today["date"], today["count_distinct_ids"]],
         ["letter sequence (first-appearance order)",
          ", ".join(today["letter_sequence_first_appearance"]) or "(none)"],
         ["single-letter suffixes present",
          ", ".join(today["single_letter_suffixes_present"]) or "(none)"],
         ["A..Z fully used?", "yes" if today["a_to_z_fully_used"] else "no"],
         ["any id after Z (two-or-more-letter suffix)?",
          "yes" if today["two_letter_or_longer_suffix_exists"] else "no"],
         ["two-or-more-letter ids",
          ", ".join(today["two_letter_or_longer_ids"]) or "(none)"]]))
    md.append("")
    md.append("## 4. Entry count under three definitions (no single count chosen)")
    md.append("")
    md.append(md_line_list_table(
        ["definition", "count"],
        [[d["label"] + " — " + d["definition"], d["count"]]
         for d in (entries["definition_a"],
                   entries["definition_b"],
                   entries["definition_c"])]))
    md.append("")
    if today["count_distinct_ids"] or census["total_lines"]:
        pass
    md.append("Detail line numbers are in `ledger-audit.json` "
              "(`entry_counts.*.line_numbers` / `first_line_numbers`).")
    md.append("")
    md.append("## 5. Lines containing `%s`" % prior["substring"])
    md.append("")
    md.append(md_line_list_table(
        ["metric", "value"],
        [["line count", prior["line_count"]],
         ["line numbers",
          ", ".join(str(n) for n in prior["line_numbers"]) or "(none)"]]))
    md.append("")
    md.append("## 6. `VERIFIED <40 hex> TREE <40 hex>` lines")
    md.append("")
    md.append("Matches: **%d**" % verified["count"])
    md.append("")
    md.append(md_line_list_table(
        ["line", "commit", "tree", "nearest receipt id above"],
        [[m["line"], "`%s`" % m["commit"], "`%s`" % m["tree"],
          "%s (line %s)" % (m["nearest_receipt_above"], m["nearest_receipt_line"])
          if m["nearest_receipt_above"] else "(none)"]
         for m in verified["matches"]]))
    md.append("")
    last = verified["last_match"]
    if last:
        md.append("Last such line in file: line %d — commit `%s`, tree `%s`, "
                  "nearest receipt above %s (line %s)."
                  % (last["line"], last["commit"], last["tree"],
                     last["nearest_receipt_above"], last["nearest_receipt_line"]))
    else:
        md.append("Last such line in file: (none)")
    md.append("")
    md.append("## 7. Credential scan")
    md.append("")
    md.append(md_line_list_table(
        ["metric", "value"],
        [["patterns searched", "; ".join(creds["patterns_searched"])],
         ["hit line count", creds["hit_line_count"]],
         ["hit line numbers (only numbers are ever reported)",
          ", ".join(str(n) for n in creds["hit_line_numbers"]) or "(none)"]]))
    md.append("")
    md.append("## 8. Last five lines, verbatim")
    md.append("")
    for item in tail:
        md.append("Line %d (`%s`):" % (item["line"],
                                       item["terminator"] or "no terminator"))
        md.append("")
        md.append("```text")
        md.append(item["content"])
        md.append("```")
        md.append("")
    md.append("## Limitations of these patterns")
    md.append("")
    md.append(LIMITATIONS)
    md.append("")

    with open(os.path.join(common.OUT_DIR, "ledger-audit.md"), "w",
              encoding="utf-8") as fh:
        fh.write("\n".join(md))

    print("wrote out/ledger-audit.json and out/ledger-audit.md")


if __name__ == "__main__":
    build()
