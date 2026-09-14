"""G12 for rendered files: standard.assert_no_scoring_headers must refuse a scoring
word in an ATX heading or a table header. Probe what it actually sees.

The function's own docstring claims it scans "every ATX Markdown heading, and the
header row of every Markdown table - the first row of each contiguous block of pipe
rows", and raises the same SCORING_KEY_FORBIDDEN code the key guard raises.
"""
from __future__ import annotations

from _probe_setup import check

from minireason.loop import standard


def outcome(text: str):
    try:
        standard.assert_no_scoring_headers(text, where="probe.md")
    except standard.StandardInvalid as exc:
        return ("raised", exc.code, str(exc)[:120])
    return ("ok", None, None)


def main() -> None:
    status, code, _ = outcome(standard.CEILING_TEXT)
    check("the frozen ceiling passes its own G12 scan", status == "ok", f"{status}")

    # -- headings ---------------------------------------------------------- #
    status, code, _ = outcome("## score summary\n\n| a | b |\n|---|---|\n| 1 | 2 |")
    check("a '#'-heading carrying 'score' is refused",
          status == "raised" and code == "SCORING_KEY_FORBIDDEN", f"{status} {code}")

    status, code, _ = outcome("Results\n=======\n\nplain prose")
    check("a setext heading is simply not a heading to this scanner (note only)",
          status == "ok", status)

    # -- tables ------------------------------------------------------------ #
    status, code, msg = outcome("| rank | cell |\n|---|---|\n| r1 | x |")
    check("a table whose header carries 'rank' is refused",
          status == "raised" and code == "SCORING_KEY_FORBIDDEN", f"{status} {code} {msg}")

    # Bare pipe rows with no delimiter row anywhere in the document:
    bare = "The cell outcome was the following:\n\nscore | 1\nrank | 2\nwinner | r1\n"
    status, code, _ = outcome(bare)
    check("pipe rows with NO delimiter row anywhere pass unscanned (note only)",
          status == "ok", status)

    # A prose line mentioning pipes that precedes a real table elsewhere in the file:
    # the prose line ends with '|' so '_is_pipe_row' takes it, and then
    # 'a | score' is seen as a body row and skipped... check both directions.
    prose_before_table = (
        "either a | b |\n\n| name | value |\n|---|---|\n| score | 1 |\n"
    )
    status, code, _ = outcome(prose_before_table)
    check("a scoring word in a table BODY cell passes (documented: body rows skipped)",
          status == "ok", status)

    # The classic smuggle: indent the header row so 'index and _is_pipe_row(prev)'
    # is skipped. A table whose header is the very FIRST line and uses no leading '|':
    header_first_line = "name | rank |\n|---|---|\n| cell | 1 |\n"
    status, code, msg = outcome(header_first_line)
    print(f"    header-as-first-line: {status} {code} {msg}")
    check("a non-prefixed header row on line 1 IS scanned (delimiter row does it)",
          status == "raised" and code == "SCORING_KEY_FORBIDDEN", f"{status} {code}")

    # Case: the scoring word in the header row but the row above is prose-with-pipe.
    above = "a | b\nname | better |\n|---|---|\n| x | 1 |\n"
    status, code, msg = outcome(above)
    print(f"    prose-pipe above header: {status} {code} {msg}")
    check("a header row directly under a pipe-prose line is skipped as a body row",
          status == "ok", f"{status}")

    # The multi-line table with a code-fence in between (does the scan see fences?).
    fenced_table = "```\n| rank | x |\n|---|---|\n| 1 | y |\n```\n"
    status, code, msg = outcome(fenced_table)
    print(f"    fenced table: {status} {code} {msg}")


if __name__ == "__main__":
    main()
