lines = open('check/extract.py').read().split('\n')
assert 'SyntaxError' not in ''.join(lines)
lines[77] = "        if items and line and re.match('[-\\u2014a-z0-9\\u201c\\u2019)\"\\']', line[0]) and not line.startswith(('|', '#', '>')):"
open('check/extract.py', 'w').write('\n'.join(lines))
compile(open('check/extract.py').read(), 'x', 'exec')
print('ok')
