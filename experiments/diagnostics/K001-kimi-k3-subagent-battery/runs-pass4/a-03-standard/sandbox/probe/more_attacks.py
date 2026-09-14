"""Suspected: _is_pipe_row misclassifies a delimiter row as a header row when it
is the first row of the block. Also standard_body refusing unknown sections."""
import json
import sys

sys.path.insert(0, "src")

from minireason.loop import standard as s

def attempt(label, text):
    try:
        s.assert_no_scoring_headers(text)
        print(f"{label}: PASSED")
    except s.StandardInvalid as e:
        print(f"{label}: refused -> {e.code} | {e.detail[:100]}")

# table with empty header cells
attempt("empty header cells", "|  |  |\n|---|---|\n| a | b |")

# a setext second line that is all dashes - delimiter-like but no pipe
attempt("setext second line of dashes after prose with pipe",
        "some | prose\n---\n")

# multiple tables, second one's header
attempt("second table header with scoring word",
        "| a | b |\n|---|---|\n| 1 | 2 |\n\n| cell | rank |\n|---|---|")

# standard_body tolerates extra sections?
body = json.loads(s.STANDARD_BODY)
body["extra_section"] = {"note": "added later"}
try:
    s.standard_body(json.dumps(body))
    print("extra section in parsed body: accepted")
except s.StandardInvalid as e:
    print("extra section in parsed body: refused ->", e.code)

# standard_body: register text tamper inside registers section
body2 = json.loads(s.STANDARD_BODY)
body2["registers"]["T"]["plan_text"] = "rewritten register text"
try:
    out = s.standard_body(json.dumps(body2))
    print("tampered register text on read: accepted; plan_text now:",
          out["registers"]["T"]["plan_text"][:40])
except s.StandardInvalid as e:
    print("tampered register text on read: refused ->", e.code)
