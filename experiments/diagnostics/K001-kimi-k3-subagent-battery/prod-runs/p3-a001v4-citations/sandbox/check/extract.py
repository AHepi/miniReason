import re, json, hashlib
from pathlib import Path
from collections import Counter

src = Path('docs/sources/FW5-explanatory-construction.md')
staging = Path('staging/STAGING-v4.md')

data = src.read_bytes()
sha = hashlib.sha256(data).hexdigest()
EXPECTED = '8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a'
assert sha == EXPECTED, sha

srlines = src.read_text(encoding='utf-8').split('\n')
stlines = staging.read_text(encoding='utf-8').split('\n')

# extraction pattern: FW5:N, FW5:N-M, bare :N, :N-M, hyphen or en-dash, 2-4 digit numbers;
# optional trailing sentence annotation like s1 / s2-3 used by the staging table.
pat = re.compile(r'(?:FW5)?+:(\d{2,4})(?:[-\u2013](\d{2,4}))?(?:\s*s(\d+)(?:-s?(\d+))?)?')

def norm(s):
    s = s.replace('\u201c','"').replace('\u201d','"').replace('\u2018',"'").replace('\u2019',"'")
    return ' '.join(s.split())

def strip_markup(s):
    # second-tier normalisation: markdown emphasis, LaTeX inline delimiters,
    # leading citation labels like ':170 ', trailing/leading ellipses
    s = re.sub(r'\*\*|\*|__', '', s)
    s = s.replace('\\(', '').replace('\\)', '')
    s = re.sub(r'^(?:FW5)?:\d{2,4}\s*', '', s)
    s = s.strip(' .\u2026')
    return s

def frag_parts(f):
    # an ellipsis inside a quote means omitted source text: test each side separately
    parts = [p for p in re.split(r'\u2026|\.\.\.', f)]
    return [p.strip() for p in parts if len(norm(p.strip())) >= 12]

# find quoted fragments on a staging line, with positions
def fragments(line):
    frags = []
    for m in re.finditer(r'`([^`]+)`', line):
        frags.append((m.start(), m.group(1)))
    for m in re.finditer(r'\u201c(.+?)\u201d', line):
        frags.append((m.start(), m.group(1)))
    tmp = re.sub(r'`[^`]+`', lambda m:' '*len(m.group(0)), line)
    tmp = re.sub(r'\u201c.+?\u201d', lambda m:' '*len(m.group(0)), tmp)
    for m in re.finditer(r'"([^"\n]+)"', tmp):
        frags.append((m.start(), m.group(1)))
    for m in re.finditer(r'\\\((.*?)\\\)', line):
        frags.append((m.start(), '\\(' + m.group(1) + '\\)'))
    frags.sort()
    # drop mis-paired artifacts: fragments that themselves contain a citation token
    out = []
    for pos, f in frags:
        if len(norm(f)) < 12:
            continue
        if re.search(r'(?:FW5)?:\d{2,4}', f) and not re.match(r'^(?:FW5)?:\d{2,4}\s+\S{s}\s', f) and not re.match(r'^(?:FW5)?:\d{2,4}\s+[A-Z"\u201c]', f):
            continue
        out.append((pos, f))
    return out

def sentences(text):
    return re.split(r'(?<=[.!?]) ', text)

results = []
targets = set()
blank_cited = set()
bad_ranges = []
items = []  # previous line's parsed citations, for wrapped-paragraph carry-over
for i, line in enumerate(stlines, 1):
    raw = []
    for m in pat.finditer(line):
        start = m.start()
        prev = line[max(0,start-16):start]
        if re.search(r'(?:\.md|\.json|\.py|\.toml|PLAN|SKILL)[`\*\)]*$', prev):
            continue  # file:line references to other documents, not FW5 citations
        raw.append(m)
    if raw:
        # build target text per match
        items = []
        for m in raw:
            n1 = int(m.group(1)); n2 = int(m.group(2)) if m.group(2) else None
            sn = int(m.group(3)) if m.group(3) else None
            sn_hi = int(m.group(4)) if m.group(4) else None
            if n2 is not None and n2 < n1:
                bad_ranges.append((i, m.group(0)))
            if n2:
                text = '\n'.join(srlines[n1-1:n2]) if n2 <= len(srlines) else None
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
        if not (items and line and re.match('[-\u2014a-z0-9\u201c\u2019)"\']', line[0])
                and not line.startswith(('|', '#', '>'))):
            items = []
            continue

    frags = fragments(line)
    if not items:
        continue

    def assign(pos, f):
        # prefer a citation on this line whose target contains the fragment
        nf = norm(strip_markup(f))
        hits = [it for it in items if it['text'] and (nf in norm(strip_markup(it['text'])) or f in it['text'])]
        if len(hits) >= 1:
            return hits[0]
        before = [it for it in items if it['m'].end() <= pos]
        if before:
            return max(before, key=lambda it: it['m'].end())
        return min(items, key=lambda it: it['m'].start() - pos)

    owned = {id(it): [] for it in items}
    for pos, f in frags:
        owned[id(assign(pos, f))].append(f)

    for it in items:
        m, n1, n2, text, tgt = it['m'], it['n1'], it['n2'], it['text'], it['tgt']
        cit = m.group(0)
        if n2 is not None and n2 < n1:
            results.append(dict(staging_line=i, citation=cit, target=tgt, fragments=[],
                                verdict='REVERSED-RANGE', note='range end precedes start'))
            continue
        if text is None or text == '':
            ln = n1 if n2 is None else n2
            results.append(dict(staging_line=i, citation=cit, target=tgt, fragments=[],
                                verdict='OUT-OF-RANGE',
                                note=f'target beyond source length {len(srlines)}' if text is None else 'sentence index beyond line length'))
            if n2:
                for l in range(n1, min(n2, len(srlines))+1): targets.add(l)
            elif n1 <= len(srlines): targets.add(n1)
            continue
        lo = n1; hi = n2 if n2 else n1
        for l in range(lo, hi+1):
            targets.add(l)
            if srlines[l-1].strip() == '':
                blank_cited.add(l)
        fr = owned[id(it)]
        if not fr:
            verdict = 'NO-QUOTE-TO-CHECK'; note = ''
        else:
            fails_exact, fails_norm, fails_all, diffs = [], [], [], []
            for f in fr:
                parts = frag_parts(f)
                if not parts:
                    continue
                ntext = norm(text); mtext = norm(strip_markup(text))
                ok_exact = all(p in text for p in parts)
                ok_norm  = all(norm(p) in ntext for p in parts)
                ok_mark  = all(norm(strip_markup(p)) in mtext for p in parts)
                if ok_exact: continue
                if ok_norm:
                    diffs.append(f'{f[:60]!r}: typographic quotes / whitespace'); continue
                if ok_mark:
                    diffs.append(f'{f[:60]!r}: markdown emphasis / LaTeX delimiters / line label'); continue
                fails_all.append(f)
            if not fails_all:
                if diffs:
                    verdict = 'CORRECT IN SUBSTANCE'
                    note = 'found only after normalisation: ' + '; '.join(diffs)
                else:
                    verdict = 'CORRECT'; note = ''
            else:
                verdict = 'WRONG'
                notes = []
                for f in fails_all:
                    for p in frag_parts(f):
                        nptest = norm(strip_markup(p))
                        if nptest in norm(strip_markup(text)):
                            continue
                        found = [j+1 for j, sl in enumerate(srlines) if nptest in norm(strip_markup(sl))]
                        notes.append(f'fragment {p[:80]!r} not in cited target; cited line {n1} starts: {srlines[n1-1][:120]!r}' +
                                     (f'; found at source line(s) {found[:5]}' if found else '; not found anywhere in source'))
                note = ' | '.join(notes)
        results.append(dict(staging_line=i, citation=cit, target=tgt, fragments=fr,
                            verdict=verdict, note=note))

Path('out').mkdir(exist_ok=True)
Path('out/citations-v4.json').write_text(json.dumps(dict(
    source='docs/sources/FW5-explanatory-construction.md', source_sha256=sha,
    expected_sha256=EXPECTED, sha256_match=True, source_lines=len(srlines),
    regex=pat.pattern,
    method=('fragments (>=12 chars after normalisation) extracted from each staging line; '
            'assigned to the citation on that line whose target contains them, else nearest; '
            'CORRECT = verbatim, CORRECT IN SUBSTANCE = after normalisation, WRONG = not found, '
            'NO-QUOTE-TO-CHECK = no fragment on the line'),
    total_citations=len(results), distinct_targets=len(targets),
    verdict_counts=dict(Counter(r['verdict'] for r in results)),
    blank_cited_lines=sorted(blank_cited), reversed_ranges=[c2 for _, c2 in bad_ranges],
    citations=results), indent=1, ensure_ascii=False))

c = Counter(r['verdict'] for r in results)
wrong = [r for r in results if r['verdict'] == 'WRONG']

md = []
md.append('# FW5 line-citation verification of staging/STAGING-v4.md\n')
md.append(f'Source: `docs/sources/FW5-explanatory-construction.md`, sha256 `{sha}` — **verified by computation before anything else; identical to the designated sha256.**')
md.append(f'Source has {len(srlines)} newline-split segments.\n')
md.append(f'Extraction regex: `{pat.pattern}`')
md.append('Context filter: matches preceded by `.md`, `.json`, `.py`, `.toml`, `PLAN` or `SKILL` (allowing a trailing backtick/asterisk/paren) are file:line references to other documents and are excluded.')
md.append('Quoted fragments (straight/typographic quotes, backticks, `\\(...\\)` LaTeX, >= 12 characters) on each staging line are assigned to the citation whose target contains them where identifiable, otherwise to the nearest citation on the line. Ellipses inside a quote split the fragment into separately-tested parts. `s1`-style suffixes name a numbered sentence of the cited line.\n')
md.append(f'Total citations checked: **{len(results)}**; distinct cited source lines: **{len(targets)}**.\n')
md.append('## Summary')
md.append(f'- citations: {len(results)}')
for v in ['CORRECT', 'CORRECT IN SUBSTANCE', 'WRONG', 'NO-QUOTE-TO-CHECK', 'REVERSED-RANGE', 'OUT-OF-RANGE']:
    md.append(f'- {v}: {c.get(v,0)}')
md.append('')
if wrong:
    md.append('**WRONG citations:**')
    for r in wrong:
        md.append(f'- staging line {r["staging_line"]}: `{r["citation"]}` (target {r["target"]}) — {r["note"]}')
else:
    md.append('**WRONG citations: none.**')
md.append('')
for v in ['OUT-OF-RANGE']:
    if c.get(v):
        md.append(f'**{v}:**')
        for r in results:
            if r['verdict'] == v:
                md.append(f'- staging line {r["staging_line"]}: `{r["citation"]}` — {r["note"]}')
        md.append('')
md.append('Cited source lines that are blank (cited singly or inside a cited range): '
          + (', '.join(':'+str(n) for n in sorted(blank_cited)) if blank_cited else 'none'))
md.append('Ranges whose end precedes start: '
          + (', '.join(f'`{c2}` (staging line {sl})' for sl, c2 in bad_ranges) if bad_ranges else 'none'))
md.append('\n## Table\n')
md.append('| staging line | citation | target | verdict | note |')
md.append('|---|---|---|---|---|')
for r in results:
    note = r['note'].replace('|', '\\|').replace('\n', ' ')
    md.append(f'| {r["staging_line"]} | `{r["citation"]}` | {r["target"]} | {r["verdict"]} | {note} |')
md.append('\n## What the extraction pattern would not catch')
md.append('- Line references with no colon prefix: "line 617", "FW5 line 617", "FW5 617", "lines 613 through 618", "613 to 618".')
md.append('- Numbers outside the 2-4 digit width: `:8` or `:15000` match nothing.')
md.append('- Range separators other than hyphen/en-dash (em-dash, spaces around the dash: ":613 - 618").')
md.append('- Compound forms like ":950-:952": the trailing `:952` is captured as a separate bare citation, so the check still visits line 952 but does not treat it as the range end of one citation.')
md.append('- Citations spanning a staging line break, and fragments (e.g. block-quote lines) that sit on a staging line carrying no citation at all — those are never extracted, hence never tested.')
md.append('- Fragments shorter than 12 characters, and paraphrases with no quote at all: such citations can only ever get NO-QUOTE-TO-CHECK, which is not an endorsement.')
md.append('- A citation whose quoted fragment is genuinely present but whose *surrounding claim* about the line is wrong: only substring presence is tested, not what the staging text asserts about the line.')
Path('out/citations-v4.md').write_text('\n'.join(md))

print('sha OK:', sha, '| source lines:', len(srlines))
print('total:', len(results), 'distinct targets:', len(targets))
print(c)
print('blank cited:', sorted(blank_cited))
print('bad ranges:', bad_ranges)
for w in wrong:
    print('WRONG: staging', w['staging_line'], w['citation'], '->', w['note'][:260])
for r in results:
    if r['verdict'] == 'OUT-OF-RANGE':
        print('OOR: staging', r['staging_line'], r['citation'], r['note'])
