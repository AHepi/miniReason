t = open('check/extract.py').read()
old = "results = []\ntargets = set()\nblank_cited = set()\nbad_ranges = []"
new = "results = []\ntargets = set()\nblank_cited = set()\nbad_ranges = []\nitems = []  # previous line's parsed citations, for wrapped-paragraph carry-over"
assert old in t
t = t.replace(old, new)
open('check/extract.py', 'w').write(t)
print('ok')
