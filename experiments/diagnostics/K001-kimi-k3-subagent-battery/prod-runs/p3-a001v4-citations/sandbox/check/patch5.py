t = open('check/extract.py').read()
old = """    if not raw:
        if items and line and re.match('[-\\u2014a-z0-9\\u201c\\u2019)"\\']', line[0]) and not line.startswith(('|', '#', '>')):
            pass  # wrapped continuation of the previous paragraph: reuse its citations
        else:
            items = []
            continue

    # build target text per match
    items = []
    for m in raw:"""
new = """    if raw:
        # build target text per match
        items = []
        for m in raw:"""
assert old in t
t = t.replace(old, new)
# reindent the match-building block
old = """        n1 = int(m.group(1)); n2 = int(m.group(2)) if m.group(2) else None
        sn = int(m.group(3)) if m.group(3) else None
        sn_hi = int(m.group(4)) if m.group(4) else None
        if n2 is not None and n2 < n1:
            bad_ranges.append((i, m.group(0)))
        if n2:
            text = '\\n'.join(srlines[n1-1:n2]) if n2 <= len(srlines) else None
            tgt = f'{n1}-{n2}'
        else:
            text = srlines[n1-1] if n1 <= len(srlines) else None
            tgt = str(n1)
        if text is not None and sn:
            ss = sentences(text)
            hi2 = sn_hi if sn_hi else sn
            text = ' '.join(ss[sn-1:hi2]) if hi2 <= len(ss) else ''
            tgt += f' s{sn}' + (f'-s{sn_hi}' if sn_hi else '')
        items.append(dict(m=m, n1=n1, n2=n2, text=text, tgt=tgt))

    frags = fragments(line)"""
new = """            n1 = int(m.group(1)); n2 = int(m.group(2)) if m.group(2) else None
            sn = int(m.group(3)) if m.group(3) else None
            sn_hi = int(m.group(4)) if m.group(4) else None
            if n2 is not None and n2 < n1:
                bad_ranges.append((i, m.group(0)))
            if n2:
                text = '\\n'.join(srlines[n1-1:n2]) if n2 <= len(srlines) else None
                tgt = f'{n1}-{n2}'
            else:
                text = srlines[n1-1] if n1 <= len(srlines) else None
                tgt = str(n1)
            if text is not None and sn:
                ss = sentences(text)
                hi2 = sn_hi if sn_hi else sn
                text = ' '.join(ss[sn-1:hi2]) if hi2 <= len(ss) else ''
                tgt += f' s{sn}' + (f'-s{sn_hi}' if sn_hi else '')
            items.append(dict(m=m, n1=n1, n2=n2, text=text, tgt=tgt))
    else:
        # no new citation: a wrapped-paragraph continuation line (starting mid-
        # sentence, not a table/heading/blockquote line) inherits the previous
        # line's citations; anything else ends carry-over.
        if not (items and line and re.match('[-\\u2014a-z0-9\\u201c\\u2019)"\\']', line[0])
                and not line.startswith(('|', '#', '>'))):
            items = []
            continue

    frags = fragments(line)
    if not items:
        continue"""
assert old in t, 'block2 missing'
t = t.replace(old, new)

# assign(): guard empty items (already guarded by items check above), and results
# loop must emit each citation only once per staging line even under carry-over:
old = """    for it in items:"""
new = """    for it in items:"""
open('check/extract.py', 'w').write(t)
print('ok')
