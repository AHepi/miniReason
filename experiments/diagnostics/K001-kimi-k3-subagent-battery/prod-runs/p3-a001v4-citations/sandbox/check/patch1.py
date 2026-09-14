import re
p = 'check/extract.py'
t = open(p).read()
t = t.replace("pat = re.compile(r'(?:FW5)?:(\\d{2,4})(?:[-\\u2013](\\d{2,4}))?(?:\\s*s(\\d+)(?:-\\d+)?)?')",
              "pat = re.compile(r'(?:FW5)?+:(\\d{2,4})(?:[-\\u2013](\\d{2,4}))?(?:\\s*s(\\d+)(?:-(\\d+))?)?')")
t = t.replace("sn = int(m.group(3)) if m.group(3) else None",
              "sn = int(m.group(3)) if m.group(3) else None\n        sn_hi = int(m.group(4)) if m.group(4) else None")
old = """        if text is not None and sn:
            ss = sentences(text)
            text = ss[sn-1] if sn <= len(ss) else ''
            tgt += f' s{sn}'"""
new = """        if text is not None and sn:
            ss = sentences(text)
            hi2 = sn_hi if sn_hi else sn
            text = ' '.join(ss[sn-1:hi2]) if hi2 <= len(ss) else ''
            tgt += f' s{sn}' + (f'-s{sn_hi}' if sn_hi else '')"""
assert old in t
t = t.replace(old, new)
open(p, 'w').write(t)
print('patched')
