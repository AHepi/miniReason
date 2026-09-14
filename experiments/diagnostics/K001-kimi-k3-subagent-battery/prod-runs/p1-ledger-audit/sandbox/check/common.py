"""Shared mechanical computations for the docs/DECISION_LEDGER.md audit.

Every value is computed from the sandbox bytes of docs/DECISION_LEDGER.md;
nothing is transcribed from memory.
"""

import os
import re
from collections import OrderedDict

LEDGER_PATH = os.path.join("docs", "DECISION_LEDGER.md")
OUT_DIR = "out"
TODAY = "20260914"

RECEIPT_PATTERN = r"REC-\d{8}-[A-Z]+"
RECEIPT_RE = re.compile(RECEIPT_PATTERN)

VERIFIED_TREE_PATTERN = r"VERIFIED ([0-9a-f]{40}) TREE ([0-9a-f]{40})"
VERIFIED_TREE_RE = re.compile(VERIFIED_TREE_PATTERN)

PRIOR_MARKER = "Prior verified commit/tree:"

CREDENTIAL_PATTERNS = OrderedDict([
    ("sk-hex32", re.compile(r"sk-[0-9a-f]{32}")),
    ("hex32-dot-token", re.compile(r"[0-9a-f]{32}\.[A-Za-z0-9_-]{20,}")),
])


def load_bytes(path=LEDGER_PATH):
    with open(path, "rb") as fh:
        return fh.read()


def load_lines(path=LEDGER_PATH):
    """Return a list of (line_number, content, terminator).

    line_number is 1-based; content is the decoded line without its
    terminator; terminator is "\\r\\n", "\\n", or "" when the final line of
    the file has no terminator at all.
    """
    raw = load_bytes(path)
    parts = raw.split(b"\n")
    if parts and parts[-1] == b"":
        parts = parts[:-1]
    ends_with_lf = raw.endswith(b"\n")
    lines = []
    n = len(parts)
    for i, part in enumerate(parts):
        if i == n - 1 and not ends_with_lf:
            lines.append((i + 1, part.decode("utf-8"), ""))
        elif part.endswith(b"\r"):
            lines.append((i + 1, part[:-1].decode("utf-8"), "\r\n"))
        else:
            lines.append((i + 1, part.decode("utf-8"), "\n"))
    return lines


def line_census(lines):
    """Item 1: total lines, CRLF count, bare-LF count, CRLF line numbers."""
    crlf = [n for n, _c, t in lines if t == "\r\n"]
    bare_lf = [n for n, _c, t in lines if t == "\n"]
    unterminated = [n for n, _c, t in lines if t == ""]
    return OrderedDict([
        ("total_lines", len(lines)),
        ("crlf_line_count", len(crlf)),
        ("bare_lf_line_count", len(bare_lf)),
        ("unterminated_final_line_count", len(unterminated)),
        ("crlf_line_numbers", crlf),
    ])


def receipt_ids(lines):
    """Item 2: distinct REC-\\d{8}-[A-Z]+ tokens, first-appearance order.

    For each id: line number of first appearance and the number of distinct
    lines containing the id at least once.
    """
    first_line = OrderedDict()
    line_count = {}
    for n, content, _t in lines:
        seen_on_line = set()
        for m in RECEIPT_RE.finditer(content):
            rid = m.group(0)
            if rid not in first_line:
                first_line[rid] = n
            seen_on_line.add(rid)
        for rid in seen_on_line:
            line_count[rid] = line_count.get(rid, 0) + 1
    rows = []
    for rid in first_line:
        rows.append(OrderedDict([
            ("id", rid),
            ("first_appearance_line", first_line[rid]),
            ("lines_carrying_id", line_count[rid]),
        ]))
    return rows


def today_receipts(receipt_rows):
    """Item 3: ids dated TODAY in first-appearance order, letter sequence,
    whether A..Z is fully used, and whether a two-letter (after-Z) id exists.
    """
    prefix = "REC-" + TODAY + "-"
    todays = [r for r in receipt_rows if r["id"].startswith(prefix)]
    letters = [r["id"][len(prefix):] for r in todays]
    single_letters = sorted({s for s in letters if len(s) == 1})
    alphabet = [chr(c) for c in range(ord("A"), ord("Z") + 1)]
    a_to_z_fully_used = single_letters == alphabet
    multi = [r["id"] for r in todays if len(r["id"][len(prefix):]) >= 2]
    return OrderedDict([
        ("date", TODAY),
        ("prefix", prefix),
        ("count_distinct_ids", len(todays)),
        ("ids_in_first_appearance_order", todays),
        ("letter_sequence_first_appearance", letters),
        ("single_letter_suffixes_present", single_letters),
        ("a_to_z_fully_used", a_to_z_fully_used),
        ("two_letter_or_longer_suffix_exists", len(multi) > 0),
        ("two_letter_or_longer_ids", multi),
    ])


def entry_counts(lines):
    """Item 4: entry count under three separate definitions."""
    a_lines = [n for n, c, _t in lines if c.startswith("REC-")]
    b_lines = [n for n, c, _t in lines
               if c.startswith("REC-") or c.startswith("**REC-")]

    blocks = []
    current = []
    for n, c, _t in lines:
        if c.strip() == "":
            if current:
                blocks.append(current)
                current = []
        else:
            current.append((n, c))
    if current:
        blocks.append(current)

    c_blocks = []
    for block in blocks:
        block_text = "\n".join(c for _n, c in block).lstrip()
        first_token = block_text.split(None, 1)[0] if block_text else ""
        if first_token.startswith("REC-") or first_token.startswith("**REC-"):
            c_blocks.append(block[0][0])

    return OrderedDict([
        ("definition_a", OrderedDict([
            ("label", "(a) lines beginning with REC-"),
            ("definition",
             "Lines with content starting with 'REC-' at column 0 "
             "(line.startswith('REC-'))."),
            ("count", len(a_lines)),
            ("line_numbers", a_lines),
        ])),
        ("definition_b", OrderedDict([
            ("label", "(b) lines beginning with REC- or **REC-"),
            ("definition",
             "Lines with content starting with 'REC-' or with the markdown "
             "bold opener '**REC-' at column 0."),
            ("count", len(b_lines)),
            ("line_numbers", b_lines),
        ])),
        ("definition_c", OrderedDict([
            ("label", "(c) paragraphs opening with REC- or **REC-"),
            ("definition",
             "Blank-line separated blocks (blank = empty or whitespace-only) "
             "whose first non-space token starts with 'REC-' or '**REC-'."),
            ("count", len(c_blocks)),
            ("first_line_numbers", c_blocks),
        ])),
    ])


def prior_marker(lines):
    """Item 5: lines containing the exact substring PRIOR_MARKER."""
    hits = [n for n, c, _t in lines if PRIOR_MARKER in c]
    return OrderedDict([
        ("substring", PRIOR_MARKER),
        ("line_count", len(hits)),
        ("line_numbers", hits),
    ])


def verified_tree(lines):
    """Item 6: VERIFIED <40 hex> TREE <40 hex> lines.

    Reports line number, commit, tree, and the receipt id nearest above
    (last token on the nearest preceding line carrying a receipt id),
    plus the last such line in the file.
    """
    ids_by_line = {n: RECEIPT_RE.findall(c) for n, c, _t in lines}
    matches = []
    for idx, (n, c, _t) in enumerate(lines):
        m = VERIFIED_TREE_RE.search(c)
        if not m:
            continue
        nearest_id = None
        nearest_line = None
        for j in range(idx - 1, -1, -1):
            candidates = ids_by_line[lines[j][0]]
            if candidates:
                nearest_id = candidates[-1]
                nearest_line = lines[j][0]
                break
        matches.append(OrderedDict([
            ("line", n),
            ("commit", m.group(1)),
            ("tree", m.group(2)),
            ("nearest_receipt_above", nearest_id),
            ("nearest_receipt_line", nearest_line),
        ]))
    return OrderedDict([
        ("pattern", VERIFIED_TREE_PATTERN),
        ("count", len(matches)),
        ("matches", matches),
        ("last_match", matches[-1] if matches else None),
    ])


def credential_scan(lines):
    """Item 7: credential-pattern hits. Returns ONLY line numbers.

    Matched text is never stored or printed.
    """
    hit_lines = []
    for n, c, _t in lines:
        for pattern in CREDENTIAL_PATTERNS.values():
            if pattern.search(c):
                hit_lines.append(n)
                break
    return OrderedDict([
        ("patterns_searched", list(CREDENTIAL_PATTERNS)),
        ("hit_line_count", len(hit_lines)),
        ("hit_line_numbers", sorted(hit_lines)),
        ("note", "By design, only line numbers are reported; "
                 "matched text is never printed or stored."),
    ])


def last_five(lines):
    """Item 8: the last five lines, verbatim, with line numbers."""
    tail = lines[-5:]
    return [OrderedDict([
        ("line", n),
        ("terminator", t),
        ("content", c),
    ]) for n, c, t in tail]
