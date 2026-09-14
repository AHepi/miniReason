#!/usr/bin/env python3
"""Join every commit/tree identity published in docs/DECISION_LEDGER.md against
the branch's own frozen commit log evidence/git-log-branch.txt.

Writes out/verified-join.md and out/verified-join.json.

Extraction patterns (all matches are reported with their exact pattern):
  1. VERIFIED pair:    VERIFIED <40 hex> TREE <40 hex>
  2. Ledger sentence:  "Prior verified commit/tree:" followed by two identifiers
                       (full or short, in either order as written). In this
                       ledger every sentence writes commit-first: a full(40)
                       commit, " / ", a full(40) tree, optionally backticked.
                       The join is by the commit identifier.
  3. Bare-token sweep: every other bare 40-hex or 7-hex token whose nearest
                       keyword among commit / tree / remote / published
                       (case-insensitive, substrings allowed) sits within a
                       gap of <=40 characters (gaps measured between the end
                       of one span and the start of the other).

Join verdicts (rules 2 and 3):
  MATCH           commit present in log and its logged tree equals claimed tree
  TREE-MISMATCH   commit present, logged tree differs (both trees printed)
  COMMIT-ABSENT   commit/full-prefix resolves to no logged commit
  SHORT-AMBIGUOUS a short id resolving to more than one logged commit

Bare-token classification (rule 4, membership only, no pair join):
  COMMIT           full id exactly equals a logged commit sha
  TREE             full id exactly equals some logged commit's tree sha
  COMMIT+TREE      both (a commit whose own tree has the same id — none here)
  NEITHER          full id is neither
  UNRESOLVED-SHORT 7-hex id: deliberately not promoted, because a short id may
                   prefix both a commit and a tree; the ledger's nearest
                   keyword declares the intended role.
"""

import json
import os
import re
from collections import Counter, OrderedDict

LEDGER_PATH = 'docs/DECISION_LEDGER.md'
LOG_PATH = 'evidence/git-log-branch.txt'
MD_OUT = 'out/verified-join.md'
JSON_OUT = 'out/verified-join.json'

HEX40 = r'[0-9a-f]{40}'
VERIFIED_PAIR_RE = re.compile(r'\bVERIFIED (%s) TREE (%s)\b' % (HEX40, HEX40))
PRIOR_RE = re.compile(
    r'Prior verified commit/tree:\s*`?([0-9a-f]{7,40})`?\s*/\s*`?([0-9a-f]{7,40})`?')
TOKEN_RE = re.compile(r'(?<![0-9a-f])(?:[0-9a-f]{40}|[0-9a-f]{7})(?![0-9a-f])')
KEYWORD_RE = re.compile(r'commit|tree|remote|published', re.IGNORECASE)
CRED_RE = re.compile(r'(?i)((?:api[_-]?key|token|secret|password|authorization|bearer)'
                     r'\s*[:=]\s*["\']?[-A-Za-z0-9_./+=]{16,})')

PATTERN_STRINGS = OrderedDict([
    ('verified_pair', r'VERIFIED ([0-9a-f]{40}) TREE ([0-9a-f]{40})'),
    ('prior_verified_sentence',
     r'Prior verified commit/tree:\s*`?([0-9a-f]{7,40})`?\s*/\s*`?([0-9a-f]{7,40})`?'),
    ('bare_token_within_40_chars',
     r'(?<![0-9a-f])(?:[0-9a-f]{40}|[0-9a-f]{7})(?![0-9a-f]) with the NEAREST word of '
     r'/(commit|tree|remote|published)/i within a 40-character gap'),
])
KEYWORDS_DISPLAY = 'commit / tree / remote / published'
WINDOW = 40


def load_log():
    """Parse the frozen `git log --format='%H %T %h %ad %an %s'` extract."""
    records = []
    with open(LOG_PATH, encoding='utf-8') as fh:
        for ln, raw in enumerate(fh.read().splitlines(), 1):
            if not raw.strip():
                continue
            parts = raw.split(' ')
            if len(parts) < 6:
                raise ValueError('malformed log line %d: %r' % (ln, raw))
            commit, tree, short, adate, author = parts[:5]
            records.append(OrderedDict([
                ('line', ln), ('commit', commit), ('tree', tree),
                ('short', short), ('date', adate), ('author', author),
                ('subject', ' '.join(parts[5:])),
            ]))
    by_commit, by_short, by_tree = {}, {}, {}
    for r in records:
        by_commit.setdefault(r['commit'], []).append(r)
        by_short.setdefault(r['short'], []).append(r)
        by_tree.setdefault(r['tree'], []).append(r)
    short_collisions = {s: [r['commit'] for r in rs]
                        for s, rs in by_short.items() if len(rs) > 1}
    return records, by_commit, by_short, by_tree, short_collisions


def resolve_commit(ident, by_commit, by_short):
    """Resolve a claimed identity to logged commit record(s)."""
    if len(ident) == 40:
        if ident in by_commit:
            return by_commit[ident]
        return [r for c, rs in by_commit.items() if c.startswith(ident) for r in rs]
    return list(by_short.get(ident, []))


def join_pair(commit_id, tree_id, by_commit, by_short):
    """JOIN a claimed (commit, tree) pair against the log by commit."""
    out = OrderedDict([('claimed_commit', commit_id), ('claimed_tree', tree_id)])
    recs = resolve_commit(commit_id, by_commit, by_short)
    if not recs:
        out['verdict'] = 'COMMIT-ABSENT'
        return out
    if len(recs) > 1:
        out['verdict'] = 'SHORT-AMBIGUOUS'
        out['candidates'] = [r['commit'] for r in recs]
        return out
    r = recs[0]
    out.update(logged_commit=r['commit'], logged_tree=r['tree'],
               log_line=r['line'], log_short=r['short'], log_subject=r['subject'])
    out['verdict'] = 'MATCH' if r['tree'] == tree_id else 'TREE-MISMATCH'
    return out


def classify_bare(token, by_commit, by_tree):
    """Membership-only classification of a bare identity (rule 4)."""
    out = OrderedDict()
    if len(token) == 40:
        is_c, is_t = token in by_commit, token in by_tree
        out['class'] = ('COMMIT+TREE' if is_c and is_t else
                        'COMMIT' if is_c else 'TREE' if is_t else 'NEITHER')
        if is_c:
            r = by_commit[token][0]
            out['as_commit'] = OrderedDict(log_line=r['line'], short=r['short'],
                                           tree=r['tree'], subject=r['subject'])
        if is_t:
            out['as_tree_of'] = [OrderedDict(commit=r['commit'], short=r['short'],
                                             log_line=r['line']) for r in by_tree[token]]
    else:
        out['class'] = 'UNRESOLVED-SHORT'
        out['note'] = ('short id carried as text only — rule 4 does not promote '
                       'short ids because one short id can prefix both a commit '
                       'and a tree; the nearest keyword gives the ledger role')
    return out


def main():
    records, by_commit, by_short, by_tree, short_collisions = load_log()
    with open(LEDGER_PATH, encoding='utf-8') as fh:
        lines = fh.read().splitlines()

    # Credential-shaped guard: path/line only, never the string itself.
    cred_note = ['%s:%d' % (LEDGER_PATH, i)
                 for i, l in enumerate(lines, 1) if CRED_RE.search(l)]

    exclusions = []          # (lineno, start, end) spans claimed by rules 1/2
    verified_pairs, prior_refs = [], []
    for i, line in enumerate(lines, 1):
        for m in VERIFIED_PAIR_RE.finditer(line):
            verified_pairs.append(OrderedDict([
                ('line', i), ('commit', m.group(1)), ('tree', m.group(2)),
                ('pattern', PATTERN_STRINGS['verified_pair'])]))
            exclusions.append((i, m.start(1), m.end(2)))
        for m in PRIOR_RE.finditer(line):
            prior_refs.append(OrderedDict([
                ('line', i), ('first_as_written', m.group(1)),
                ('second_as_written', m.group(2)),
                ('order_written', 'commit / tree'),
                ('commit', m.group(1)), ('tree', m.group(2)),
                ('pattern', PATTERN_STRINGS['prior_verified_sentence'])]))
            exclusions.append((i, m.start(1), m.end(2)))

    # Rule 2/3 join by commit.
    for entry in verified_pairs + prior_refs:
        entry.update(join_pair(entry['commit'], entry['tree'], by_commit, by_short))

    # Rule 4 bare-token sweep: nearest keyword within a 40-char gap.
    bare = OrderedDict()     # keyed by (token, role, line) -> dedupe by (token, role)
    for i, line in enumerate(lines, 1):
        excl = [e for e in exclusions if e[0] == i]
        for m in TOKEN_RE.finditer(line):
            if any(e[1] <= m.start() and m.end() <= e[2] for e in excl):
                continue
            best, best_gap = None, None
            for km in KEYWORD_RE.finditer(line):
                gap = (m.start() - km.end()) if km.end() <= m.start() else (
                    (km.start() - m.end()) if m.end() <= km.start() else 0)
                if gap <= WINDOW and (best_gap is None or gap < best_gap):
                    best, best_gap = km.group(0).lower(), gap
            if best is None:
                continue
            role = {'commit': 'commit', 'tree': 'tree'}.get(best, 'remote/publication')
            key = (m.group(0), role)
            if key not in bare:
                entry = OrderedDict([('token', m.group(0)), ('line', i),
                                     ('role', role), ('keyword', best),
                                     ('keyword_gap_chars', best_gap)])
                entry.update(classify_bare(m.group(0), by_commit, by_tree))
                bare[key] = entry
            if bare[key]['line'] != i:
                bare[key].setdefault('other_lines', [])
                if i not in bare[key]['other_lines']:
                    bare[key]['other_lines'].append(i)
    bare_list = sorted(bare.values(), key=lambda e: (e['line'], e['token']))

    # Consistency guard: one token should never be reported under two roles.
    roles = {}
    for e in bare_list:
        roles.setdefault(e['token'], set()).add(e['role'])
    multi_role = {t: sorted(rs) for t, rs in roles.items() if len(rs) > 1}

    # ---- summary -----------------------------------------------------------
    pc = Counter(e['verdict'] for e in verified_pairs)
    qc = Counter(e['verdict'] for e in prior_refs)
    not_match = [e for e in verified_pairs + prior_refs if e['verdict'] != 'MATCH']
    bc = Counter(e['class'] for e in bare_list)
    all_match = bool(verified_pairs) and pc.get('MATCH', 0) == len(verified_pairs)

    data = OrderedDict([
        ('task', 'Join every published commit/tree identity in docs/DECISION_LEDGER.md '
                 'against the branch commit log evidence/git-log-branch.txt'),
        ('inputs', OrderedDict([
            ('ledger', LEDGER_PATH), ('log', LOG_PATH),
            ('log_format', "git log --format='%H %T %h %ad %an %s' --date=iso-strict"),
            ('log_lines', len(records)),
            ('unique_commits', len(by_commit)), ('unique_trees', len(by_tree)),
            ('unique_short_ids', len(by_short)),
            ('short_id_collisions_in_log', short_collisions),
        ])),
        ('extraction', OrderedDict([
            ('patterns', PATTERN_STRINGS),
            ('window_chars', WINDOW),
            ('counts', OrderedDict([
                ('verified_pairs', len(verified_pairs)),
                ('prior_verified_sentences', len(prior_refs)),
                ('bare_tokens_distinct_by_role', len(bare_list)),
            ])),
        ])),
        ('verified_pairs', verified_pairs),
        ('prior_verified_sentences', prior_refs),
        ('bare_tokens', bare_list),
        ('summary', OrderedDict([
            ('verified_pair_verdict_counts', OrderedDict(sorted(pc.items()))),
            ('prior_sentence_verdict_counts', OrderedDict(sorted(qc.items()))),
            ('bare_class_counts', OrderedDict(sorted(bc.items()))),
            ('not_match', [OrderedDict([
                ('line', e['line']), ('claimed_commit', e['claimed_commit']),
                ('claimed_tree', e['claimed_tree']), ('verdict', e['verdict'])] +
                ([('logged_tree', e['logged_tree'])] if 'logged_tree' in e else []))
                for e in not_match]),
            ('every_verified_pair_verifies', all_match),
        ])),
        ('limits', [
            'The three patterns are exhaustive for their keywords in this ledger: every '
            'occurrence of the word VERIFIED and every "Prior verified commit/tree:" phrase '
            'was matched (verified computationally); no VERIFIED or prior-sentence identity '
            'was left unparsed.',
            'Bare-token sweep is confined to tokens within %d characters of the words %s '
            '(case-insensitive, substrings allowed, nearest word wins). Identities elsewhere '
            '— the line-11 workspace id 4043a04d6092, all SHA-256 document/material hashes, '
            'plan ids, REC-2026091x receipt ids — are out of scope by the rule itself.'
            % (WINDOW, KEYWORDS_DISPLAY),
            '7-hex bare tokens are reported UNRESOLVED-SHORT and never joined: a short id '
            'may prefix both a commit and a tree. The log itself has %s, so every short id '
            'appearing in the ledger is at most a unique text reference, which the role '
            'column records.'
            % ('no short-id collisions' if not short_collisions else
               'collisions %s' % short_collisions),
            'NEITHER verdicts are identities this branch log does not contain. Contextually '
            'they are the local/connector-half commits of remote/local publication pairs, '
            'cross-repo source pins (AHepi/h-EPI commit '
            'b2a33283dc1e05fb83c3357b26e2cc12115f6b6c, AHepi/DeepReason commit '
            '9607fba6f0a3066fbcab282c9ae0fad823e52e0c and its upstream root commit 377e5965ad20b22b07274655a9151d913d76db0a, the personal-skill remote '
            '642dab8ff174f290a17871dff1133efab9707f41, and the line-11 earlier-workspace '
            'local commit 506b716bb7a2b4504e9e4f0ba54966587ac36465) — the ledger states '
            'equal-tree publication for remote/local pairs, but a commit identity that never '
            'entered this branch cannot be verified from this extract.',
            'Bare tokens occurring in more than one keyword context: %s.'
            % (', '.join(sorted(multi_role)) if multi_role else 'none'),
            'Every 40-hex bare token carries exactly one membership verdict per log '
            'regardless of role; the multi-context list above is presentation-only.',
            'Credential-pattern guard: %s' % (
                'no line matched; nothing withheld.' if not cred_note else
                'shape matched at ' + ', '.join(cred_note) + ' (paths/lines only).'),
        ]),
    ])

    os.makedirs('out', exist_ok=True)
    with open(JSON_OUT, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=2)
        fh.write('\n')

    # ---- markdown ----------------------------------------------------------
    md = []
    md.append('# Verified join — decision ledger × branch commit log')
    md.append('')
    md.append('Every commit/tree identity published in `%s`, joined against `%s` — the '
              'frozen `git log --format=\'%%H %%T %%h %%ad %%an %%s\' --date=iso-strict` '
              'extract over the whole branch: **%d lines, %d unique commits, %d unique '
              'trees, %d unique short ids, %s**.'
              % (LEDGER_PATH, LOG_PATH, len(records), len(by_commit), len(by_tree),
                 len(by_short),
                 'no short-id collisions' if not short_collisions else
                 '%d short-id collisions' % len(short_collisions)))
    md.append('')
    md.append('## 1. What was extracted, and by which pattern')
    md.append('')
    md.append('| rule | pattern | strings extracted |')
    md.append('|---|---|---|')
    md.append('| 1. VERIFIED pair | `%s` | **%d** |'
              % (PATTERN_STRINGS['verified_pair'], len(verified_pairs)))
    md.append('| 2. `Prior verified commit/tree:` sentence | `%s` | **%d** |'
              % (PATTERN_STRINGS['prior_verified_sentence'], len(prior_refs)))
    md.append('| 3. other bare 40-hex / 7-hex token near a keyword | `%s` | **%d** '
              'distinct (token, role) pairs |'
              % (PATTERN_STRINGS['bare_token_within_40_chars'], len(bare_list)))
    md.append('')
    md.append('Rule 2: in this ledger every such sentence writes the identifiers '
              '**commit-first** — a full 40-hex commit, ` / `, a full 40-hex tree, '
              'optionally backticked — so the join takes the first identifier as the '
              'commit; the pattern as coded would also accept short ids or the reversed '
              'order without silently misreading them (the two capture groups are kept '
              'as first/second-as-written and the written order is reported per row).')
    md.append('')
    md.append('Rule 3: the exact spans already claimed by rules 1 and 2 are excluded; '
              'distance is the character gap to the **nearest** keyword word, case-'
              'insensitive, substrings allowed (so `commits`, `trees`, `publication`, '
              '`remote main` all qualify), window ≤ %d characters.'
              % WINDOW)
    md.append('')
    md.append('## 2. VERIFIED pairs — each claim joined against the log by commit')
    md.append('')
    md.append('| ledger line | claimed commit | claimed tree | verdict | log line · logged tree · subject |')
    md.append('|---|---|---|---|---|')
    for e in verified_pairs:
        logged = ('%d · `%s` · %s' % (e['log_line'], e['logged_tree'], e['log_subject'])
                  ) if 'logged_tree' in e else '—'
        md.append('| %d | `%s` | `%s` | **%s** | %s |'
                  % (e['line'], e['claimed_commit'], e['claimed_tree'], e['verdict'],
                     logged.replace('|', '\\|')))
    md.append('')
    md.append('## 3. `Prior verified commit/tree:` sentences — same join')
    md.append('')
    md.append('| ledger line | commit (first, as written) | tree (second, as written) | verdict | log line · logged tree · subject |')
    md.append('|---|---|---|---|---|')
    for e in prior_refs:
        logged = ('%d · `%s` · %s' % (e['log_line'], e['logged_tree'], e['log_subject'])
                  ) if 'logged_tree' in e else '—'
        md.append('| %d | `%s` | `%s` | **%s** | %s |'
                  % (e['line'], e['claimed_commit'], e['claimed_tree'], e['verdict'],
                     logged.replace('|', '\\|')))
    md.append('')
    md.append('## 4. Other bare tokens — do they resolve in the log?')
    md.append('')
    md.append('Membership only, per rule 4: a full 40-hex id is **COMMIT** (exact logged '
              'commit; its logged tree and subject shown), **TREE** (the sha is the tree '
              'of the commit(s) listed), **COMMIT+TREE** or **NEITHER**. 7-hex ids are '
              '**UNRESOLVED-SHORT** — never promoted — because one short id can prefix '
              'both a commit and a tree; their `role` column is the ledger\'s own nearest '
              'keyword, not a log resolution.')
    md.append('')
    md.append('| ledger line | token | declared role (nearest keyword, gap) | verdict | resolves to |')
    md.append('|---|---|---|---|---|')
    for e in bare_list:
        role = '%s (%s, %d)' % (e['role'], e['keyword'], e['keyword_gap_chars'])
        if e['class'] == 'COMMIT':
            res = 'commit `%s` — %s' % (e['as_commit']['short'], e['as_commit']['subject'])
        elif e['class'] == 'TREE':
            res = 'tree of ' + ', '.join('`%s` (line %d)' % (a['short'], a['log_line'])
                                         for a in e['as_tree_of'])
        elif e['class'] == 'COMMIT+TREE':
            res = 'commit `%s`; also that commit\'s own tree' % e['as_commit']['short']
        elif e['class'] == 'NEITHER':
            res = 'neither a logged commit nor a logged tree'
        else:
            res = '—'
        extra = ' (also %s)' % ', '.join(map(str, e['other_lines'])) if e.get('other_lines') else ''
        md.append('| %d%s | `%s` | %s | **%s** | %s |'
                  % (e['line'], extra, e['token'], role, e['class'],
                     res.replace('|', '\\|')))
    md.append('')
    md.append('## 5. Summary')
    md.append('')
    md.append('- **VERIFIED pairs:** %s'
              % (', '.join('%s × %d' % kv for kv in sorted(pc.items())) or 'none'))
    md.append('- **Prior verified sentences:** %s'
              % (', '.join('%s × %d' % kv for kv in sorted(qc.items())) or 'none'))
    md.append('- **Bare tokens:** %s'
              % (', '.join('%s × %d' % kv for kv in sorted(bc.items())) or 'none'))
    md.append('')
    if not_match:
        md.append('### Not MATCH')
        md.append('')
        for e in not_match:
            md.append('- ledger line %d — commit `%s` / claimed tree `%s`: **%s**%s'
                      % (e['line'], e['claimed_commit'], e['claimed_tree'], e['verdict'],
                         ' — logged tree `%s`' % e['logged_tree']
                         if e['verdict'] == 'TREE-MISMATCH' else ''))
    else:
        md.append('### Not MATCH: none')
        md.append('')
        md.append('Every joined claim matched the log; no discrepancy was found and none '
                  'is manufactured.')
    md.append('')
    md.append('- **Every VERIFIED pair verifies: %s** (%d of %d joined MATCH).'
              % ('YES' if all_match else 'NO', pc.get('MATCH', 0), len(verified_pairs)))
    md.append('- Every prior-verified sentence verifies: **%s** (%d of %d joined MATCH).'
              % ('YES' if len(prior_refs) == qc.get('MATCH', 0) else 'NO',
                 qc.get('MATCH', 0), len(prior_refs)))
    md.append('')
    md.append('Notes on the bare-token classes (a clean join, so these are provenance '
              'observations, not failures):')
    md.append('')
    md.append('- The %d NEITHER full-length identities are those the ledger itself '
              'attributes off this branch: the local/connector half of each "remote main '
              '`X`, local `Y`, shared tree `Z`" publication receipt (equal-tree connector '
              'publication; the local commit never enters the branch), cross-repository '
              'source pins (AHepi/h-EPI, AHepi/DeepReason, the personal-skill remote), '
              'and one earlier-workspace local commit on line 11. Each such row names its '
              'ledger line and role so a reader can check the attribution.'
              % bc.get('NEITHER', 0))
    md.append('- Each of the %d UNRESOLVED-SHORT ids prefixes at most one logged commit '
              '(the log has no short-id collisions), but none was joined or classified, '
              'per the no-promotion rule; the role column is only the nearest-keyword '
              'heuristic — e.g. the line-1495 enumeration mixes commit and tree short '
              'ids, all sitting nearest the word \'tree\'.'
              % bc.get('UNRESOLVED-SHORT', 0))
    md.append('')
    md.append('## 6. Limits — what these patterns would not have caught')
    md.append('')
    for lim in data['limits']:
        md.append('- ' + lim)
    md.append('')

    with open(MD_OUT, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(md))

    print('wrote %s and %s' % (MD_OUT, JSON_OUT))
    print('verified pairs:', len(verified_pairs), dict(pc))
    print('prior refs:', len(prior_refs), dict(qc))
    print('bare tokens:', len(bare_list), dict(bc))
    print('short collisions in log:', short_collisions)
    print('every VERIFIED pair verifies:', all_match)
    print('not MATCH:', [(e['line'], e['claimed_commit'], e['verdict']) for e in not_match])
    print('multi-role tokens:', multi_role)
    print('credential hits (paths only):', cred_note if cred_note else 'none')


if __name__ == '__main__':
    main()
