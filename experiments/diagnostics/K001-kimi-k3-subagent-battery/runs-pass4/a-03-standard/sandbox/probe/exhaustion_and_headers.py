"""Attacks on the two scans: exhaustion and scoring headers."""
import sys

sys.path.insert(0, "src")

from minireason.loop import standard as s


def attempt(label, fn):
    try:
        fn()
        print(f"{label}: PASSED (no refusal)")
    except s.StandardInvalid as e:
        print(f"{label}: refused -> {e.code} | {e.detail[:80]}")
    except Exception as e:  # noqa
        print(f"{label}: other error {type(e).__name__}: {e}")


# A) ceiling passes both scans
attempt("ceiling passes exhaustion scan", lambda: s.assert_no_exhaustion_claim(s.CEILING_TEXT))
attempt("ceiling passes header scan (frozen ceiling claim)",
        lambda: s.assert_no_scoring_headers(s.CEILING_TEXT))

# B) rewrapped denial: exemption is whitespace-insensitive
rewrapped = "A reached ceiling is a declared resource boundary, not\nexhaustion\nof the inquiry"
attempt("rewrapped denial", lambda: s.assert_no_exhaustion_claim(rewrapped))

# C) smuggle around the denial: removing it should re-expose the joined claim
smuggle1 = "the tokens run out: the inquiry is not exhaustion of the inquiry, it is simply exhausted"
attempt("denial + real claim appended", lambda: s.assert_no_exhaustion_claim(smuggle1))

# C2: claim woven BETWEEN halves of the denial so string-remove leaves the stem intact
smuggle2 = "not exhaustion of the inquirY was the claim we made"  # case-variant only
attempt("case-variant denial only", lambda: s.assert_no_exhaustion_claim(smuggle2))

# D) plain violation
plain = "the run stopped because the context window was exhausted"
attempt("plain exhaustion claim", lambda: s.assert_no_exhaustion_claim(plain))

# D2: stem only as part of another word
attempt("'exhaustive' variant", lambda: s.assert_no_exhaustion_claim("an exhaustive check"))

# E) header scan: heading with scoring word
attempt("heading '## Score by cell'",
        lambda: s.assert_no_scoring_headers("## Score by cell\n"))
attempt("heading '## Scores'", lambda: s.assert_no_scoring_headers("## Scores per cell"))

# F) table header with scoring word
attempt("table header | cell | score |",
        lambda: s.assert_no_scoring_headers("| cell | score |\n|---|---|\n| a | 1 |"))

# G) body row carrying the word is admitted by design (docstring says so)
attempt("table body carrying word",
        lambda: s.assert_no_scoring_headers(
            "| cell | note |\n|---|---|\n| a | the word score appears in prose |"))

# H) ATX heading inside a fenced code block
fenced = "```markdown\n## Scores by cell\n```"
attempt("scoring heading inside fenced code", lambda: s.assert_no_scoring_headers(fenced))

# I) setext heading (underlined) - not ATX
setext = "Scores by cell\n=========="
attempt("setext heading with 'Scores'", lambda: s.assert_no_scoring_headers(setext))

# J) markdown table inside fenced code
fenced_table = "```\n| cell | rating |\n|---|---|\n| a | 9 |\n```"
attempt("scoring table inside fenced code", lambda: s.assert_no_scoring_headers(fenced_table))

# K) HTML table header
html_table = "<table><tr><th>score</th></tr></table>"
attempt("HTML table header", lambda: s.assert_no_scoring_headers(html_table))

# L) case variants in headings
attempt("heading '## RANKING'", lambda: s.assert_no_scoring_headers("## RANKING"))

# M) word as part of a longer token ('scorer' etc.)
attempt("heading '## Scorer notes'", lambda: s.assert_no_scoring_headers("## Scorer notes"))

# N) multi-word-table-in-prose line with pipe but not a table row
prose_pipe = "the pipe | character in a sentence about grade inflation"
attempt("prose sentence with pipe", lambda: s.assert_no_scoring_headers(prose_pipe))

# O) header row detection when a table follows prose containing a pipe
mixed = "a | b\n---\n| cell | score |\n|---|---|"
attempt("delimiter after prose-pipe line", lambda: s.assert_no_scoring_headers(mixed))
