"""Verify twenty FW5 line citations in staging/a001-STAGING.md.

Prints, for each of the twenty citation pointers:
  - the STAGING line the citation appears on (with its line number), and
  - the FW5 line or inclusive range that the pointer names (with line numbers).

Also verifies the identity of the FW5 reading edition: sha256 and line count.
Citation convention: FW5:N is line N of docs/sources/FW5-explanatory-construction.md,
1-based, splitting on newline; FW5:N-M is the inclusive range.
"""

import hashlib
import os

FW5_PATH = "docs/sources/FW5-explanatory-construction.md"
STAGING_PATH = "staging/a001-STAGING.md"
EXPECTED_SHA = "8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a"

# (staging_line, fw5_start, fw5_end) -- fw5_end == fw5_start for single lines.
CITATIONS = [
    (21, 172, 172),
    (23, 164, 168),
    (26, 216, 224),
    (28, 226, 226),
    (30, 228, 228),
    (34, 614, 620),
    (35, 831, 831),
    (40, 1364, 1364),
    (43, 1502, 1502),
    (45, 1192, 1192),
    (52, 1390, 1390),
    (87, 640, 640),
    (103, 728, 728),
    (109, 133, 133),
    (112, 210, 210),
    (112, 630, 630),
    (113, 630, 630),
    (113, 1200, 1206),
    (135, 1390, 1390),
    (142, 1372, 1372),
]


def read_lines(path):
    with open(path, "rb") as f:
        data = f.read()
    return data, data.decode("utf-8").split("\n")


def excerpt(text, limit=600):
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def main():
    raw, fw5 = read_lines(FW5_PATH)
    sha = hashlib.sha256(raw).hexdigest()
    trailing_newline = raw.endswith(b"\n")
    n_lines = len(fw5) - (1 if trailing_newline else 0)
    print("FW5 file:", FW5_PATH)
    print("  sha256:", sha)
    print("  sha256 matches expected:", sha == EXPECTED_SHA)
    print("  lines (split on newline, trailing newline not a line):", n_lines)
    print("  bytes end with newline:", trailing_newline)
    _, staging = read_lines(STAGING_PATH)
    print("STAGING file:", STAGING_PATH, "lines:", len(staging) - (1 if staging and staging[-1] == "" else 0))
    print("=" * 100)

    for i, (sline, lo, hi) in enumerate(CITATIONS, start=1):
        print()
        print("### Citation %d: staging line %d -> FW5:%s" % (i, sline, str(lo) if lo == hi else "%d-%d" % (lo, hi)))
        print("--- STAGING line %d ---" % sline)
        if 1 <= sline < len(staging) + 1:
            print(excerpt(staging[sline - 1]))
        else:
            print("<OUT OF RANGE: staging has only %d lines>" % len(staging))
        print("--- FW5:%s ---" % (str(lo) if lo == hi else "%d-%d" % (lo, hi)))
        for n in range(lo, hi + 1):
            if 1 <= n <= len(fw5):
                print("[FW5:%d] %s" % (n, excerpt(fw5[n - 1])))
            else:
                print("[FW5:%d] <OUT OF RANGE: FW5 has only %d lines>" % (n, len(fw5)))
        print("=" * 100)


if __name__ == "__main__":
    main()
