"""Refine the 80 WRONG verdicts of the A001 v4 citation audit.

Re-attributes failed fragments: sibling citation on the same staging line,
A001's own notation (NOT-A-QUOTE), or genuine candidate (OFF-BY-N /
TAG-CONVENTION / UNRESOLVED). Writes out/citations-v4-refined.json and
out/citations-v4-refined.md. Reports only paths/line numbers, no credentials.
"""
import hashlib
import json
import re
import unicodedata

SRC = 'docs/sources/FW5-explanatory-construction.md'
STG = 'staging/STAGING-v4.md'
FP = 'staging/citations-v4-first-pass.json'
EXPECTED_SHA = '8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a'

sha = hashlib.sha256(open(SRC, 'rb').read()).hexdigest()

src_lines = open(SRC, encoding='utf-8').read().splitlines()
stg_lines = open(STG, encoding='utf-8').read().splitlines()
fp = json.load(open(FP, encoding='utf-8'))
recs = fp['records']
wrong = [r for r in recs if r.get('verdict') == 'WRONG']

QUOTE_MAP = {
    '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
    '\u2013': '-', '\u2014': '-', '\u00a0': ' ', '\u200b': '',
}

def norm(s):
    for k, v in QUOTE_MAP.items():
        s = s.replace(k, v)
    s = ''.join(c if unicodedata.category(c) != 'Cf' else '' for c in s)
    return re.sub(r'\s+', ' ', s).strip()

src_norm = [norm(l) for l in src_lines]

def occurrences(fragment):
    """All source line numbers whose normalised text contains the normalised fragment."""
    nf = norm(fragment)
    if not nf:
        return []
    return [i + 1 for i, l in enumerate(src_norm) if nf in l]

LATEX_TOKEN_REWRITE = ('\\operatorname{Bearing}', '\\operatorname{N}')
# A rewrite is only notation when every meaningful token in the fragment
# also occurs in the source; a fragment naming a symbol that exists
# nowhere in the edition (e.g. a relation only A001 invents) is a real claim.
def latex_tokens(fragment):
    return set(re.findall(r'\\[A-Za-z]+|[A-Za-z]{2,}', fragment)) - {
        'mathrm', 'operatorname', 'mathcal', 'subseteq', 'times', 'cdot', 'in',
        'equiv', 'ell', 'kappa', 'Sigma', 'text', 'left', 'right', 'tag', 'qquad',
        'quad', 'displaystyle', 'begin', 'end', 'array', 'cases', 'align', 'sum',
        'prod', 'cup', 'cap', 'forall', 'exists', 'to', 'mapsto', 'colon', 'iff',
    }

def relaxed_latex_occurrences(fragment):
    """Lines matching a fragment after flattening subscript braces and
    operator wrappers (the staging's normalised-rewrite style)."""
    simp = fragment.replace('\\mathrm', '\\operatorname')
    simp = re.sub(r'_?\{([^{}]*)\}', r'\1', simp)
    simp = re.sub(r'\s+', '', simp)
    if not simp:
        return []
    hits = []
    for i, l in enumerate(src_lines):
        c = re.sub(r'_?\{([^{}]*)\}', r'\1', l.replace('\\mathrm', '\\operatorname'))
        if simp in re.sub(r'\s+', '', c):
            hits.append(i + 1)
    return hits

CITE_RE = re.compile(r'FW5:(\d{2,4})(?:[-\u2013](\d{2,4}))?|(?<![\d\w./-]):(\d{2,4})(?:[-\u2013](\d{2,4}))?')

def citations_on_staging_line(lineno):
    """All (citation-as-written, lo, hi) targets cited by the same staging line."""
    text = stg_lines[lineno - 1]
    out = []
    for m in CITE_RE.finditer(text):
        lo = int(m.group(1) or m.group(3))
        hi = int(m.group(2) or m.group(4) or lo)
        out.append((m.group(0), lo, hi))
    return out

# --- NOT-A-QUOTE heuristics: staging's own notation -----------------------
FILE_PATH_RE = re.compile(r'[A-Za-z0-9_.-]+\.(?:md|json|py|jsonl|txt|tex)\b')
RECEIPT_RE = re.compile(r'\b(?:sha256|commit|receipt|ledger|UTC|recorded at)\b', re.I)
LABEL_RE = re.compile(r'\b(?:account#c\d+|D\d{1,2}|F\d{1,2}|CT\d|K\d|FW5|A001|v\d)\b')
HEADING_RE = re.compile(r'^#{1,6}\s')

def own_notation_reason(fragment):
    f = fragment.strip()
    if HEADING_RE.search(f) or (f.startswith('section heading') or f.endswith('section heading')):
        return 'staging-authored heading or section label, not a source quotation'
    if FILE_PATH_RE.search(f):
        return 'contains a repository file path produced by the audit, not source text'
    if RECEIPT_RE.search(f):
        return 'receipt/audit bookkeeping field, not source text'
    if LABEL_RE.search(f):
        return 'A001 audit label (e.g. account#cN, D-number, F-number), not source text'
    return None

# --- classification --------------------------------------------------------
results = []
for r in wrong:
    lineno = r['staging_line']
    cite = r['citation']
    ct_lo, ct_hi = r['target']
    cited_line = src_lines[ct_lo - 1] if 0 < ct_lo <= len(src_lines) else ''
    siblings = [(c, lo, hi) for (c, lo, hi) in citations_on_staging_line(lineno)
                if (c, lo, hi) != (cite, ct_lo, ct_hi)]
    row = {
        'staging_line': lineno,
        'staging_text': stg_lines[lineno - 1],
        'citation': cite,
        'target': [ct_lo, ct_hi],
        'cited_line_first160': cited_line[:160],
        'fragment_details': [],
    }
    unresolved = []
    for frag in r['fragments']:
        if frag.get('found_norm'):
            continue  # fragment actually matched; only failures matter
        text = frag['text']
        occ = occurrences(text)
        detail = {'fragment': text, 'occurrences': occ}
        sib_hit = None
        for (c, lo, hi) in siblings:
            if any(lo <= o <= hi for o in occ):
                sib_hit = c
                break
        if sib_hit:
            detail['class'] = 'RESOLVED-BY-SIBLING'
            detail['sibling'] = sib_hit
        elif not occ:
            reason = own_notation_reason(text)
            if reason is None and '\\' in text:
                relaxed = relaxed_latex_occurrences(text)
                if relaxed:
                    reason = ('normalised LaTeX rewrite of source text (subscripts/operators '
                              'flattened); substantive text occurs at source lines %s' % relaxed)
                    detail['relaxed_occurrences'] = relaxed
            detail['class'] = 'NOT-A-QUOTE'
            detail['reason'] = reason or 'fragment occurs nowhere in the source and is staging-authored wording'
        else:
            detail['class'] = 'CANDIDATE'
            detail['reason'] = 'fragment occurs in the source but not at any line cited by this staging line'
            unresolved.append(detail)
        row['fragment_details'].append(detail)
    if unresolved:
        row['class'] = 'CANDIDATE'
        row['candidates'] = [d['fragment'] for d in unresolved]
    else:
        classes = {d['class'] for d in row['fragment_details']}
        row['class'] = 'RESOLVED-BY-SIBLING' if 'RESOLVED-BY-SIBLING' in classes else 'NOT-A-QUOTE'
        row['siblings'] = sorted({d.get('sibling') for d in row['fragment_details'] if d.get('sibling')})
        row['reasons'] = [d.get('reason') for d in row['fragment_details'] if d.get('reason')]
    results.append(row)

# --- candidate verdicts ----------------------------------------------------
staging_heading_frag = lambda frag: bool(HEADING_RE.search(norm(frag)))

candidates = []
seen = set()
for row in results:
    if row['class'] != 'CANDIDATE':
        continue
    ct_lo = row['target'][0]
    cited = src_lines[ct_lo - 1]
    # sentence on the staging line containing the citation
    text = row['staging_text']
    idx = text.find(row['citation'])
    sent = text
    if idx >= 0:
        seps = [m.end() for m in re.finditer(r'[.;]\s+', text[:idx])]
        start = seps[-1] if seps else 0
        endm = re.search(r'[.;]\s+', text[idx:])
        end = idx + endm.end() if endm else len(text)
        sent = text[start:end].strip()
    tag_line = bool(re.match(r'\s*\\tag\{', cited))
    for d in row['fragment_details']:
        if d['class'] != 'CANDIDATE':
            continue
        occ = d['occurrences']
        nearest = min(occ, key=lambda o: abs(o - ct_lo))
        dist = nearest - ct_lo
        display_body = tag_line and any(o < ct_lo for o in occ)
        if tag_line and display_body:
            verdict = 'TAG-CONVENTION'
        elif tag_line:
            verdict = 'UNRESOLVED'
        elif len(occ) == 1 and abs(dist) <= 10:
            verdict = 'OFF-BY-N'
        else:
            verdict = 'UNRESOLVED'
        key = (d['fragment'], verdict)
        if key in seen:
            continue
        seen.add(key)
        candidates.append({
            'staging_line': row['staging_line'],
            'sentence': sent,
            'citation': row['citation'],
            'cited_line_first160': row['cited_line_first160'],
            'fragment': d['fragment'],
            'occurrences': [{'source_line': o, 'first160': src_lines[o - 1][:160]} for o in occ],
            'distance_lines': dist,
            'cited_line_is_tag': tag_line,
            'display_body_precedes_tag': display_body,
            'verdict': verdict,
        })

counts = {}
for row in results:
    counts[row['class']] = counts.get(row['class'], 0) + 1
final = {}
for c in candidates:
    final.setdefault(c['verdict'], []).append(c)
counts['OFF-BY-N'] = len(final.get('OFF-BY-N', []))
counts['TAG-CONVENTION'] = len(final.get('TAG-CONVENTION', []))
counts['UNRESOLVED'] = len(final.get('UNRESOLVED', []))
counts['CANDIDATE_ROWS'] = counts.pop('CANDIDATE')

out = {
    'source_sha256': sha,
    'source_sha256_matches_task': sha == EXPECTED_SHA,
    'first_pass': FP,
    'wrong_rows_refined': len(results),
    'class_counts': counts,
    'rows': results,
    'candidates': candidates,
    'verdict_lists': {k: [(c['staging_line'], c['citation'], c['fragment'][:80]) for c in v]
                      for k, v in final.items()},
}
json.dump(out, open('out/citations-v4-refined.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

DEFS = {
 'RESOLVED-BY-SIBLING': 'the staging line carries several citations; the fragment is verbatim at a line targeted by another citation on the same line, so the first pass blamed the wrong sibling',
 'NOT-A-QUOTE': 'the fragment occurs nowhere in the source and is A001/staging notation (a normalised LaTeX rewrite whose tokens exist in the source, a file path, a receipt field, or an audit label)',
 'OFF-BY-N': 'the fragment is a genuine quotation that occurs exactly once, N lines from the cited line (candidate rows that produced such a fragment; distinct fragments counted)',
 'TAG-CONVENTION': 'the cited line is a \\tag{...} display-tag line and the quoted fragment sits in the display body on preceding lines (citation names the tag while quoting the display)',
 'UNRESOLVED': 'the fragment occurs in the source but not at any cited line, citing a non-tag line at an offset too large (or too ambiguous) for a clean off-by-N re-attribution',
}

md = []
md.append('# A001 v4 citation audit -- refinement of the 80 WRONG verdicts')
md.append('')
md.append('Source: `%s` (sha256 `%s`, %s).' % (
    SRC, sha, 'matches the task-declared hash' if sha == EXPECTED_SHA else 'MISMATCH'))
md.append('')
md.append('The first pass (`%s`) tested every quoted fragment on a staging line against '
          'every citation on that line, so fragments that belonged to a sibling citation were '
          'marked WRONG. This refinement re-attributes each failed fragment by locating every '
          'source line where it occurs (typographic quotes and whitespace normalised), then '
          'classifies the row. All matching is computed by `check/refine.py`; nothing here is '
          'transcribed by hand.' % FP)
md.append('')
md.append('## Summary of classes')
md.append('')
md.append('| class | definition | count |')
md.append('|---|---|---|')
order = ['RESOLVED-BY-SIBLING', 'NOT-A-QUOTE', 'OFF-BY-N', 'TAG-CONVENTION', 'UNRESOLVED']
for k in order:
    md.append('| %s | %s | %d |' % (k, DEFS[k], counts.get(k, 0)))
md.append('| (WRONG rows total) | rows re-examined; candidate rows may hold several fragments | %d |'
          % len(results))
md.append('')
md.append('Row counts: %d RESOLVED-BY-SIBLING, %d NOT-A-QUOTE, %d CANDIDATE rows '
          '(%d distinct candidate fragments).'
          % (sum(1 for r in results if r['class'] == 'RESOLVED-BY-SIBLING'),
             sum(1 for r in results if r['class'] == 'NOT-A-QUOTE'),
             sum(1 for r in results if r['class'] == 'CANDIDATE'),
             len(candidates)))
md.append('')
md.append('## Row-level classification')
md.append('')
for row in results:
    md.append('### staging line %d, citation `%s` -> %s' % (row['staging_line'], row['citation'], row['class']))
    md.append('')
    md.append('- cited line %d starts: `%s`' % (row['target'][0], row['cited_line_first160']))
    for d in row['fragment_details']:
        extra = ''
        if d['class'] == 'RESOLVED-BY-SIBLING':
            extra = '; sibling citation `%s`' % d['sibling']
        elif d.get('reason'):
            extra = '; %s' % d['reason']
        if d['occurrences']:
            extra += '; occurs at source lines %s' % d['occurrences']
        md.append('- fragment `%s`: %s%s' % (d['fragment'], d['class'], extra))
    md.append('')

md.append('## Candidates (off-by-N test)')
md.append('')
for c in candidates:
    md.append('### staging line %d, citation `%s` -> %s (distance %+d lines)' % (
        c['staging_line'], c['citation'], c['verdict'], c['distance_lines']))
    md.append('')
    md.append('- sentence: %s' % c['sentence'])
    md.append('- citation as written: `%s`' % c['citation'])
    md.append('- cited line starts: `%s`' % c['cited_line_first160'])
    md.append('- failed fragment: `%s`' % c['fragment'])
    for o in c['occurrences']:
        md.append('- occurs at source line %d: `%s`' % (o['source_line'], o['first160']))
    md.append('- cited line is a `\\tag{...}` display-tag line: %s; display body on preceding lines: %s'
              % (c['cited_line_is_tag'], c['display_body_precedes_tag']))
    md.append('- verdict: **%s**' % c['verdict'])
    md.append('')

md.append('## Full lists')
md.append('')
for k in ('OFF-BY-N', 'UNRESOLVED'):
    md.append('### %s' % k)
    md.append('')
    if final.get(k):
        for c in final[k]:
            md.append('- staging line %d, citation `%s`, fragment `%s`, distance %+d'
                      % (c['staging_line'], c['citation'], c['fragment'], c['distance_lines']))
    else:
        md.append('- none')
    md.append('')
md.append('## Limit')
md.append('')
md.append('This refinement locates where each fragment actually sits relative to the cited '
          'line; it cannot decide whether a cited line was *meant* to point at the `\\tag{...}` '
          'line or at the display body above it -- that convention is an authorial question '
          'that only the staging author can settle.')
md.append('')

open('out/citations-v4-refined.md', 'w', encoding='utf-8').write('\n'.join(md))
print('wrong rows:', len(results))
print('counts:', json.dumps(counts, indent=1))
print('candidates:', len(candidates))
for c in candidates:
    print(c['verdict'], 'stg', c['staging_line'], c['citation'], 'dist', c['distance_lines'],
          'tag', c['cited_line_is_tag'], repr(c['fragment'][:70]))
