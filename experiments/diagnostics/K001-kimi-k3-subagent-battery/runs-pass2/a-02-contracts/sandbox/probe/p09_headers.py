"""Probe 9: assert_no_scoring_headers — contiguity and heading shapes.

The scanner marks "the **header row** of every Markdown table - the first row
of each contiguous block of pipe rows" and scans ATX headings. Two edge shapes:
 * a table whose rows are interrupted by a blank line (is the post-blank row
   then re-scanned as a "new" header? a body row with a scoring word would
   then refuse — a false positive), and
 * a heading that ends in a pipe.
Also: contracts re-export identity with standard's function.
"""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import contracts, standard
from minireason.loop.contracts import assert_no_scoring_headers

def outcome(text):
    try:
        assert_no_scoring_headers(text)
        return "passed"
    except Exception as exc:
        return f"raised {type(exc).__name__} code={getattr(exc,'code','-')}: {exc}"

# 9a: ordinary table, clean
good = "| reading | cell |\n|---|---|\n| retains | a |\n\nProse row mentioning score outside a table.\n"
print("9a clean table + prose word:", outcome(good))

# 9b: table whose header is clean but a BODY row carries a scoring word
body_score = "| reading | cell |\n|---|---|\n| score | a |\n"
print("9b scoring word in a body row:", outcome(body_score))

# 9c: two tables separated by ONE blank line, second table's header has scoring word
two_tables = ("| a | b |\n|---|---|\n| 1 | 2 |\n\n"
              "| rank | x |\n|---|---|\n| 1 | 2 |\n")
print("9c 2nd table header 'rank':", outcome(two_tables))

# 9d: second table separated by a PROSE line (not blank)
split_prose = ("| a | b |\n|---|---|\n| 1 | 2 |\n"
               "some intervening prose | with pipe\n"
               "| winner | x |\n|---|---|\n| 1 | 2 |\n")
print("9d broken-by-prose then 'winner' header:", outcome(split_prose))

# 9e: heading with a scoring tail
print("9e '## Block register | winner':", outcome("## Block register | winner"))
print("9e '## winner':", outcome("## winner"))
print("9e '####### seven hashes score' (not ATX):",
      outcome("####### seven hashes score"))

# 9f: delimiter-only line and a lone pipe row at EOF
print("9f '|---|---|' alone:", outcome("|---|---|"))
print("9g 'a | b' not followed by delimiter (prose):",
      outcome("a | b\nnext line plain"))
print("9h 'a | b' FOLLOWED by delimiter (implicit table):",
      outcome("score | b\n|---|---|"))

# 9i: identity of the contract's re-export
print("9i contracts.assert_no_scoring_headers is standard's:",
      contracts.assert_no_scoring_headers is standard.assert_no_scoring_headers)
print("done")
