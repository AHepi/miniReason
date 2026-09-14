#!/usr/bin/env python3
"""Re-verify every manifest and digest list in the published experiment records.

Walks the sandbox (repo-root layout), finds:
  * files whose name contains 'manifest' (any case) or ends with .sha256
  * JSON files with a top-level key mapping paths to 64-hex digests
    (files / entries / sha256 / digests / pins / files_read / *_pins)
  * Markdown tables of | `path` | `sha256` | rows
Re-hashes every referenced path (relative to the manifest's directory first,
then sandbox root) and emits out/manifest-reverify.json and out/manifest-reverify.md.
Also scans for credentials, inspects plan.json files, and checks the
byte-identity claim the analyses README makes about occurrence-02/03 bytes.
"""
import os, re, json, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEX64 = re.compile(r'^[0-9a-f]{64}$')

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def all_files():
    out = []
    for root, dirs, files in os.walk(ROOT):
        for f in files:
            out.append(os.path.relpath(os.path.join(root, f), ROOT).replace(os.sep, '/'))
    return sorted(p for p in out if not p.startswith(('out/', 'check/')))

def resolve(manifest_rel, entry_path):
    """Manifest dir first, then sandbox root. Return (abs, mode) or (None, None)."""
    cand1 = os.path.join(ROOT, os.path.dirname(manifest_rel), entry_path)
    if os.path.isfile(cand1):
        return cand1, 'manifest_dir'
    cand2 = os.path.join(ROOT, entry_path)
    if os.path.isfile(cand2):
        return cand2, 'sandbox_root'
    return None, None

def mk_entry(manifest_rel, entry_path, recorded, note=None):
    abs_p, mode = resolve(manifest_rel, entry_path)
    if abs_p is None:
        return {'path': entry_path, 'recorded': recorded, 'verdict': 'MISSING',
                'resolved': None, 'relative_to': None, 'computed': None,
                **({'note': note} if note else {})}
    actual = sha256_file(abs_p)
    return {'path': entry_path, 'recorded': recorded,
            'verdict': 'MATCH' if actual == recorded else 'MISMATCH',
            'resolved': os.path.relpath(abs_p, ROOT).replace(os.sep, '/'),
            'relative_to': mode, 'computed': actual,
            **({'note': note} if note else {})}

results = {'manifests': [], 'non_match': [], 'totals': {}, 'credential_hits': [],
           'plan_files': [], 'claims': [], 'name_candidates': [],
           'unreferenced_on_disk': {}}

def add_manifest(path, fmt, notes, entries):
    m = {'manifest': path, 'format': fmt, 'notes': notes, 'entries': entries,
         'counts': {}}
    for e in entries:
        m['counts'][e['verdict']] = m['counts'].get(e['verdict'], 0) + 1
        results['totals'][e['verdict']] = results['totals'].get(e['verdict'], 0) + 1
        if e['verdict'] != 'MATCH':
            results['non_match'].append(dict(e, manifest=path))
    results['manifests'].append(m)

files = all_files()

# --- name-based candidates -----------------------------------------------
results['name_candidates'] = [f for f in files
                              if 'manifest' in os.path.basename(f).lower()
                              or f.endswith('.sha256')]

# --- JSON top-level path->hex64 maps --------------------------------------
MAP_KEYS = ('files', 'entries', 'sha256', 'digests', 'pins', 'files_read',
            'source_pins', 'provider_pins', 'runtime_pins', 'source_pins_verified')

NOT_IN_SANDBOX_F001 = 'referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox'
NOT_IN_SANDBOX_OCC = 'referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory'

for f in files:
    if not f.endswith('.json'):
        continue
    try:
        d = json.load(open(os.path.join(ROOT, f)))
    except Exception:
        continue
    if not isinstance(d, dict) or 'plan.json' in f:
        continue
    for key in MAP_KEYS:
        v = d.get(key)
        if isinstance(v, dict) and v and all(isinstance(x, str) and HEX64.match(x) for x in v.values()):
            entries = []
            for pth, dig in sorted(v.items()):
                e = mk_entry(f, pth, dig)
                if e['verdict'] == 'MISSING':
                    e['note'] = NOT_IN_SANDBOX_F001 if 'B001-arm-inventory' in f else NOT_IN_SANDBOX_OCC
                entries.append(e)
            add_manifest(f, "JSON mapping (top-level key '%s' -> 64-hex)" % key,
                         'Bases: manifest_dir then sandbox root.', entries)

# --- plan.json files -------------------------------------------------------
RUNNER_V3 = 'tools/multicycle_commitment_study_multi_v3.py'
C001_DRIVER = 'tools/contrast_triple_study.py'

for f in files:
    if os.path.basename(f) != 'plan.json':
        continue
    d = json.load(open(os.path.join(ROOT, f)))
    is_c001 = '/C001-contrast-triple/' in '/' + f
    entries = []
    entries.append(mk_entry(f, 'material.json', d.get('material_sha256', ''),
                            note='field material_sha256'))
    if not is_c001:
        if d.get('arms_sha256'):
            entries.append(mk_entry(f, 'arms.json', d['arms_sha256'],
                                    note='field arms_sha256'))
        for k in ('runner_sha256', 'helper_sha256'):
            if d.get(k):
                entries.append(mk_entry(f, RUNNER_V3, d[k],
                                        note="field %s; analyses README records the runner as %s" % (k, RUNNER_V3)))
        for key, sub in (('source_pins', ''), ('provider_pins', ''), ('runtime_pins', ''),
                         ('manifests', 'manifests/{}.json')):
            v = d.get(key)
            if isinstance(v, dict):
                for pth, dig in sorted(v.items()):
                    epath = sub.format(pth) if '{}' in sub else pth
                    e = mk_entry(f, epath, dig, note='plan field %s[%s]' % (key, pth))
                    entries.append(e)
        add_manifest(f, 'JSON pinned fields (material_sha256, arms_sha256, runner/helper_sha256, source/provider/runtime_pins, manifests)',
                     '', entries)
    else:
        if d.get('helper_sha256'):
            e = mk_entry(f, C001_DRIVER, d['helper_sha256'],
                         note="field helper_sha256; C001 PLAN.md names the driver as tools/contrast_triple_study.py")
            if e['verdict'] == 'MISSING':
                e['note'] += ' (not copied into this sandbox)'
            entries.append(e)
        v = d.get('source_pins')
        if isinstance(v, dict):
            for pth, dig in sorted(v.items()):
                entries.append(mk_entry(f, pth, dig, note='plan field source_pins'))
        add_manifest(f, 'JSON pinned fields (material_sha256, helper_sha256, source_pins)',
                     '', entries)
    results['plan_files'].append({
        'plan': f, 'top_level_keys': sorted(d.keys()), 'plan_id': d.get('plan_id'),
        'derivation_statement': None})

# --- Markdown | `path` | `sha256` | tables ---------------------------------
md_row = re.compile(r'^\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]{64})`\s*\|')
for f in files:
    if not f.endswith('.md'):
        continue
    text = open(os.path.join(ROOT, f), encoding='utf-8').read()
    rows = [(m.group(1), m.group(2)) for line in text.splitlines()
            if (m := md_row.match(line))]
    if not rows:
        continue
    claim = ''
    for sent in re.split(r'(?<=\.)\s+', text):
        lw = sent.lower()
        if 'every byte' in lw and 'sha256' in lw:
            claim = sent.strip().replace('\n', ' ')[:220]
            break
    notes = ''
    if '/use-table/' in f or 'INVENTORY.md' in f:
        notes = ('Completeness claim: %r. Entry bases are the original study occurrence trees '
                 '(experiments/diagnostics/...), not this analyses directory; the occurrence file '
                 'name is derived only from the table\'s own custody header (H005 occurrence-0N). '
                 'A row therefore can only be re-verified when the same bytes happen to exist under '
                 'manifest-relative or sandbox-root resolution.' % claim) if claim else ''
    if 'PLAN.md' in f and 'C001' in f:
        notes = 'Rows pin material/driver by repo-root path; the driver tools/contrast_triple_study.py was not copied into this sandbox.'
    entries = []
    for pth, dig in rows:
        e = mk_entry(f, pth, dig)
        if e['verdict'] == 'MISSING':
            e['note'] = NOT_IN_SANDBOX_OCC if 'use-table' in f else (
                NOT_IN_SANDBOX_F001 if 'INVENTORY' in f else 'pinned bytes not copied into this sandbox')
        entries.append(e)
    add_manifest(f, 'markdown table rows `| path | sha256 |`', notes, entries)

# --- filename-only candidates ----------------------------------------------
covered = {m['manifest'] for m in results['manifests']}
for f in results['name_candidates']:
    if f not in covered:
        n = {'path': f, 'recorded': None, 'verdict': 'UNPARSED',
             'resolved': f, 'relative_to': 'self',
             'computed': sha256_file(os.path.join(ROOT, f)),
             'note': 'filename matches the manifest rule but the content is not a path->digest list (it is source code / a template-schema JSON; F002 manifests/*.json are pinned by plan.json.manifests)'}
        add_manifest(f, 'filename match only (not a digest list)', '', [n])

# --- cross-manifest claims ------------------------------------------------
# F002 analyses README line ~261: material.json and all three manifests of
# occurrence-02 and occurrence-03 are byte-identical to occurrence-01's.
f002d = 'experiments/diagnostics/F002-fork5-raised-clock'
identical_ok = True
detail = []
for name in ('material.json', 'manifests/fork5.json', 'manifests/return6.json',
             'manifests/weave7.json'):
    a = sha256_file(os.path.join(ROOT, f002d, 'occurrence-01', name))
    bs = [sha256_file(os.path.join(ROOT, f002d, occ, name))
          for occ in ('occurrence-02', 'occurrence-03')]
    ok = all(b == a for b in bs)
    identical_ok = identical_ok and ok
    detail.append('%s -> %s' % (name, 'byte-identical across occurrences' if ok else 'DIFFERS'))
results['claims'].append({
    'source': 'experiments/analyses/F002-fork5-raised-clock-2026-09-14/README.md',
    'claim': '"material.json and all three manifests are byte-identical to occurrence-01\'s" (occurrence-02 and -03)',
    'check': 'sha256 comparison of the four files under all three diagnostic occurrences',
    'result': 'CONFIRMED' if identical_ok else 'CONTRADICTED',
    'detail': detail})

# --- plan_id derivation statement (step 4) ---------------------------------
doc_cache = {f: open(os.path.join(ROOT, f), encoding='utf-8', errors='replace').read()
             for f in files if f.endswith('.md')}
for info in results['plan_files']:
    is_c001 = '/C001-contrast-triple/' in '/' + info['plan']
    docs = ['experiments/diagnostics/C001-contrast-triple/PLAN.md'] if is_c001 else \
           ['experiments/diagnostics/F002-fork5-raised-clock/PLAN.md']
    for doc in docs:
        t = doc_cache.get(doc, '')
        m = re.search(r'plan_?id[^\n]*digest[^\n]*', t) or re.search(r'plan_?id[^\n]*sha256[^\n]*', t)
        if m:
            info['derivation_statement'] = '%s: \u201c%s\u201d' % (doc, m.group(0).strip()[:220])
            break

# --- unreferenced files per directory (step 3) ------------------------------
referenced = {e['resolved'] for m in results['manifests'] for e in m['entries']
              if e.get('resolved')}
for td in [x for x in files if '/occurrence-01/' in x and 'use-table' not in x]:
    pass
# Per analysis directory: which disk files no manifest references?
for base in ('experiments/analyses/F002-fork5-raised-clock-2026-09-14',
             'experiments/analyses/B001-arm-inventory-2026-09-14',
             'experiments/diagnostics/C001-contrast-triple',
             'experiments/diagnostics/F002-fork5-raised-clock',
             'experiments/diagnostics/B001-bare-and-native'):
    listed = [f for f in files if f.startswith(base + '/') and f not in referenced]
    if listed:
        results['unreferenced_on_disk'][base] = listed

# --- credential scan --------------------------------------------------------
cred1 = re.compile(r'sk-[0-9a-f]{32}')
cred2 = re.compile(r'[0-9a-f]{32}\.[A-Za-z0-9_-]{20,}')
for f in files:
    try:
        data = open(os.path.join(ROOT, f), 'rb').read().decode('utf-8', errors='replace')
    except Exception:
        continue
    for i, line in enumerate(data.splitlines(), 1):
        if cred1.search(line) or cred2.search(line):
            results['credential_hits'].append({'path': f, 'line': i})

os.makedirs(os.path.join(ROOT, 'out'), exist_ok=True)
with open(os.path.join(ROOT, 'out', 'manifest-reverify.json'), 'w') as fh:
    json.dump(results, fh, indent=2)

# --- markdown --------------------------------------------------------------
L = []
L.append('# Manifest re-verification, computed\n')
L.append('Walked the sandbox copy of the published experiment trees '
         '(`experiments/diagnostics/{C001-contrast-triple, F002-fork5-raised-clock, '
         'B001-bare-and-native}`, `experiments/analyses/{F002-fork5-raised-clock-2026-09-14, '
         'B001-arm-inventory-2026-09-14}`) plus every pinned-bytes file copied at its '
         'repository path (`docs/`, `src/`, `tools/`). Every recorded digest was re-hashed '
         'with sha256; paths were resolved relative to the manifest\'s own directory first, '
         'then to the sandbox root. Verdicts: MATCH, MISMATCH, MISSING, UNPARSED.\n')
L.append('## Name-based candidates\n')
for c in results['name_candidates']:
    L.append('- `%s`' % c)
L.append('')
for m in results['manifests']:
    L.append('## `%s`\n' % m['manifest'])
    L.append('- format detected: %s' % m['format'])
    L.append('- counts: %s' % json.dumps(m['counts'], sort_keys=True))
    if m['notes']:
        L.append('- %s' % m['notes'])
    L.append('')
    L.append('| path | recorded sha256 | verdict | resolution |')
    L.append('|---|---|---|---|')
    for e in m['entries']:
        rec = '`%s`' % e['recorded'] if e['recorded'] else '-'
        if e['verdict'] == 'MATCH':
            res = '%s (%s)' % (e['relative_to'], e['resolved'])
            L.append('| `%s` | %s | MATCH | %s |' % (e['path'], rec, res))
        elif e['verdict'] == 'MISMATCH':
            L.append('| `%s` | %s | MISMATCH computed `%s` | %s |' % (e['path'], rec, e['computed'], e['resolved']))
        elif e['verdict'] == 'MISSING':
            note = (' -- ' + e['note']) if e.get('note') else ''
            L.append('| `%s` | %s | MISSING%s | neither base |' % (e['path'], rec, note))
        else:
            L.append('| `%s` | - | UNPARSED: %s | - |' % (e['path'], e.get('note', '')[:120]))
    L.append('')
L.append('## plan.json identity statements (step 4)\n')
L.append('| plan | top-level keys | plan_id | derivation statement in a sibling file |')
L.append('|---|---|---|---|')
for p in results['plan_files']:
    L.append('| `%s` | %s | `%s` | %s |' % (
        p['plan'], '`' + '`, `'.join(p['top_level_keys']) + '`',
        p['plan_id'] or '-', p['derivation_statement'] or 'none found'))
L.append('')
L.append('## Cross-manifest claims re-computed\n')
for c in results['claims']:
    L.append('- from `%s`: %s -- **%s** (%s): %s' % (
        c['source'], c['claim'], c['result'], c['check'], '; '.join(c['detail'])))
L.append('')
L.append('## Files present on disk that no manifest references (informational)\n')
for base, listed in results['unreferenced_on_disk'].items():
    L.append('### `%s` (%d files)\n' % (base, len(listed)))
    for f in listed:
        L.append('- `%s`' % f)
    L.append('')
L.append('A completeness claim is present: the use-table pages state *"Every byte this '
         'instrument read, with its sha256. Nothing under the occurrence was written."* and the '
         'B001 inventory carries a matching "Files read" table -- these claims bind the tables\' '
         'own reads, not the whole directory, so unreferenced files above are informational only.\n')
L.append('## Summary\n')
L.append('Counts per verdict (each entry carries its manifest):\n')
L.append('| verdict | total | per manifest |')
L.append('|---|---|---|')
for v in ('MATCH', 'MISMATCH', 'MISSING', 'UNPARSED'):
    per = ['%s: %d' % (m['manifest'], m['counts'].get(v, 0))
           for m in results['manifests'] if m['counts'].get(v)]
    L.append('| %s | %d | %s |' % (v, results['totals'].get(v, 0), '; '.join(per) or '-'))
L.append('')
L.append('### Every non-MATCH entry\n')
L.append('| manifest | path | verdict | detail |')
L.append('|---|---|---|---|')
for e in results['non_match']:
    det = e.get('note') or (('computed `%s`' % e['computed']) if e.get('computed') else '')
    L.append('| `%s` | `%s` | %s | %s |' % (e['manifest'], e['path'], e['verdict'], det))
L.append('')
L.append('### Credential scan\n')
L.append('Patterns `sk-[0-9a-f]{32}` and `[0-9a-f]{32}\\.[A-Za-z0-9_-]{20,}` over every '
         'walked file: **%d hits**%s.\n' % (
             len(results['credential_hits']),
             '' if results['credential_hits'] else ' (expected zero)')
         + ('' if not results['credential_hits'] else ' -- ' +
            '; '.join('`%s` line %d' % (h['path'], h['line']) for h in results['credential_hits'])))
L.append('### Blind spots of this walk\n')
L.append('- It sees only files that were copied into this sandbox; a MISSING verdict means '
         '"the pinned bytes are not in this copy", not that the digest in the manifest is wrong.')
L.append('- Digests keyed by something other than a file path (node coordinates, spec ids, '
         '`record_sha256`/`provider_*_sha256` fields, `helper_sha256` of absent drivers) are '
         'reported but cannot be cross-checked against their canonical object by hashing a path.')
L.append('- Nested (non top-level) path-to-digest maps under other key names than the scanned '
         'set, and digest lists inside prose without the ``| `path` | `sha256` |`` shape, are not found.')
L.append('- plan_id itself ("digest of the frozen plan body") was not re-derived: the files '
         'state it is a digest but do not state the canonical-JSON rule in a way this script implements.')
L.append('')
with open(os.path.join(ROOT, 'out', 'manifest-reverify.md'), 'w') as fh:
    fh.write('\n'.join(L))

print('manifests:', len(results['manifests']))
print('totals:', results['totals'])
print('claims:', [(c['claim'][:40], c['result']) for c in results['claims']])
mm = [e for e in results['non_match'] if e['verdict'] == 'MISMATCH']
print('MISMATCH:', len(mm))
print('credential hits:', results['credential_hits'])
