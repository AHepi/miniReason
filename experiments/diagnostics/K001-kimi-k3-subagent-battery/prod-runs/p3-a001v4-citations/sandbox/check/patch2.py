p = 'check/extract.py'
t = open(p).read()

t = t.replace(
  "pat = re.compile(r'(?:FW5)?+:(\\d{2,4})(?:[-\\u2013](\\d{2,4}))?(?:\\s*s(\\d+)(?:-(\\d+))?)?')",
  "pat = re.compile(r'(?:FW5)?+:(\\d{2,4})(?:[-\\u2013](\\d{2,4}))?(?:\\s*s(\\d+)(?:-s?(\\d+))?)?')")

# paragraph carry-over: a citation-less continuation line of a wrapped paragraph
# (starts mid-sentence: lowercase, dash, closing quote ...) inherits citations
old = """    if not raw:
        continue

    # build target text per match"""
new = """    if not raw:
        if items and line and re.match(r'[-\\u2014a-z0-9\\u201c\\u2019)"\\'']', line[0]) and not line.startswith(('|', '#', '>')):
            pass  # wrapped continuation of the previous paragraph: reuse its citations
        else:
            items = []
            continue

    # build target text per match"""
assert old in t
t = t.replace(old, new)
open(p, 'w').write(t)
print('ok')
