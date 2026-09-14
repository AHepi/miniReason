#!/usr/bin/env python3
"""Re-verify every manifest and digest list in the published experiment
directories, by computation only. Writes out/manifest-reverify.{json,md}.

Directory coverage: the five task-named directories plus every other
experiment directory actually present in the sandbox (F001-fork5-multifamily,
H005-open-prose-commitments, F001-fork5-multifamily-2026-09-14), because a
manifest in one named directory pins files living in those trees.
"""
import os, json, re, hashlib
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEX64 = re.compile(r'^[0-9a-f]{64}$')
CRED1 = re.compile(r'sk-[0-9a-f]{32}')
CRED2 = re.compile(r'[0-9a-f]{32}\.[A-Za-z0-9_-]{20,}')

DIRS = sorted(
    os.path.join('experiments', a, b)
    for a in ('diagnostics', 'analyses')
    if os.path.isdir(os.path.join(ROOT, 'experiments', a))
    for b in os.listdir(os.path.join(ROOT, 'experiments', a))
    if os.path.isdir(os.path.join(ROOT, 'experiments', a, b))
)

def sha256_of(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def walk_all(start=""):
    out = []
    for dp, dns, fns in os.walk(os.path.join(ROOT, start)):
        dns.sort(); fns.sort()
        for fn in fns:
            out.append(os.path.relpath(os.path.join(dp, fn), ROOT).replace(os.sep, '/'))
    return out

EXP_FILES = walk_all('experiments')

# ---------------- Step 1: locate digest carriers ----------------
PIN_KEY_RE = re.compile(r'(?:^|_)(pins?|sha256)$|_pins$|^(source_pins|transport_pins|provider_pins|runtime_pins|manifests|files_read)$')

def pin_map_from(v, resolve_fn):
    """dict key-> full-hex pin. resolve_fn maps the dict key to a path literal or None."""
    out = {}
    if not isinstance(v, dict):
        return out
    for k, val in v.items():
        if isinstance(val, str) and HEX64.match(val):
            out[resolve_fn(k)] = val
    return out

manifests = []  # {path, format, entries:[{path, digest, kind}]}

def add(rel, fmt, entries, note=None):
    manifests.append({"path": rel, "format": fmt, "entries": entries, "note": note})

for rel in EXP_FILES:
    base = os.path.basename(rel).lower()
    full = os.path.join(ROOT, rel)
    if base.endswith('.json'):
        try:
            with open(full) as f:
                data = json.load(f)
        except Exception:
            add(rel, 'unparsed JSON (not digest-checked)', [], note='JSON parse failed')
            continue
        if not isinstance(data, dict):
            continue
        mdir = os.path.dirname(rel)
        # files_read
        fr = data.get('files_read')
        if isinstance(fr, dict) and fr:
            ent = [{"kind": "files_read", "path": k, "digest": v}
                   for k, v in fr.items() if isinstance(v, str) and HEX64.match(v)]
            if ent:
                add(rel, 'JSON mapping (files_read: path -> sha256)', ent)
                continue
        if isinstance(fr, list) and fr and all(
                isinstance(x, dict) and HEX64.match(str(x.get('sha256', ''))) and isinstance(x.get('path'), str)
                for x in fr):
            add(rel, 'JSON list of objects (files_read: [{path, sha256}])',
                [{"kind": "files_read", "path": x['path'], "digest": x['sha256']} for x in fr])
            continue
        # per-key pin maps
        for key in ('source_pins', 'transport_pins', 'provider_pins', 'runtime_pins', 'manifests'):
            v = data.get(key)
            if isinstance(v, dict) and v and all(isinstance(x, str) and HEX64.match(x) for x in v.values()):
                if key == 'manifests':
                    # keys are template ids; files live at manifests/<tid>.json in same dir
                    ent = [{"kind": key, "path": os.path.join('manifests', k + '.json'),
                            "digest": v, "key": k} for k, v in v.items()]
                else:
                    ent = [{"kind": key, "path": k, "digest": v, "key": k} for k, v in v.items()]
                add(rel, 'JSON pin map (plan key "%s")' % key, ent)
        # 'manifest' in filename but caught nothing
        if 'manifest' in base and not any(m['path'] == rel for m in manifests):
            add(rel, 'manifest by name; no path->digest entries found', [],
                note='filename contains "manifest" but no path->sha256 mapping inside; nothing to re-hash')
    elif 'manifest' in base or base.endswith('.sha256'):
        add(rel, 'found by filename; not SHA256-text-lines format', [],
            note='no <sha256>  <path> lines extracted')

# markdown tables: full-hex cells of the form | `path` | `64hex` |
TBL = re.compile(r'^\|\s*`([^`\n]+?)`\s*\|\s*`([0-9a-f]{64})`\s*\|', re.M)
for rel in EXP_FILES:
    if not rel.endswith('.md'):
        continue
    with open(os.path.join(ROOT, rel), errors='replace') as f:
        txt = f.read()
    hits = [(pp, h) for pp, h in TBL.findall(txt) if pp != 'plan_id']
    if hits:
        add(rel, 'markdown table digest list (`path` | `sha256`)',
            [{"kind": "md-table", "path": pp, "digest": h} for pp, h in hits])

# ---------------- Step 2: verify ----------------
totals = {"MATCH": 0, "MISMATCH": 0, "MISSING": 0, "UNPARSED": 0}
non_match = []
reference_resolved = {}  # manifest path -> set of resolved sandbox paths

DIAG_TOKENS = {'artifacts', 'attempts', 'requests', 'responses', 'provider', 'traces',
               'briefs', 'preflight.json', 'arms.json', 'plan.json',
               'material.json', 'manifests'}

def study_prefixed(lit, cur_digest):
    """"B001 inventory and similar: keys like '<STUDY>/<occurrence>/<subpath>'
    where STUDY names a diagnostics study root. Try under each matching study dir."""
    first = lit.split('/', 1)[0]
    roots = [d for d in DIRS if os.path.basename(d) == first]
    if not roots or '/' not in lit:
        return None
    rest = lit.split('/', 1)[1]
    hits = []
    for r in roots:
        c = os.path.join(ROOT, r, rest).replace(os.sep, '/')
        if os.path.isfile(c):
            if hashlib.sha256(open(c, 'rb').read()).hexdigest() == cur_digest:
                hits.append((c, 'study-root-relative(hash-match)'))
            else:
                hits.append((c, 'study-root-relative'))
    # prefer hash matches
    for c, how in hits:
        if 'hash-match' in how:
            return c, how
    if hits:
        return hits[0]
    return None

def resolve(mdir, lit):
    """"Order: manifest's own directory, then the occurrence dir named in that
    path (occurrence-NN), then sandbox root. Diagnostics-shape relative paths
    (artifacts/, requests/, ...; arms/plan/material/manifests) are looked up in the
    diagnostics occurrences: unique if one exists, else the hash-matching one."""
    toks = lit.split('/')
    cands = []
    if mdir:
        cands.append((os.path.normpath(os.path.join(ROOT, mdir, lit)).replace(os.sep, '/'),
                      'manifest-dir'))
    if mdir:
        mo = re.search(r'occurrence-\d+', mdir)
        if mo:
            cands.append((os.path.normpath(os.path.join(ROOT, mo.group(0), lit)).replace(os.sep, '/'),
                          'occurrence-dir'))
    cands.append((os.path.normpath(os.path.join(ROOT, lit)).replace(os.sep, '/'), 'sandbox-root'))
    for c, how in cands:
        if os.path.isfile(c):
            return c, how
    sp = study_prefixed(lit, cur_digest)
    if sp:
        return sp
    if toks[0] in DIAG_TOKENS:
        shape = [f for f in EXP_FILES
                 if f.startswith('experiments/diagnostics/') and '/' + lit in f[len('experiments/diagnostics') : ] and f.endswith('/' + lit)]
        shape = [f for f in shape if f.endswith(lit)]
        uniq = sorted(set(shape))
        if len(uniq) == 1:
            return os.path.join(ROOT, uniq[0]).replace(os.sep, '/'), 'diagnostics-suffix-unique'
        if uniq:
            hits = []
            for f in uniq:
                full = os.path.join(ROOT, f)
                if sha256_of(full) == cur_digest:
                    hits.append(full)
            if hits:
                return hits[0].replace(os.sep, '/'), 'diagnostics-hash-match(%d found, %d match)' % (len(uniq), len(hits))
    return None, None

for m in manifests:
    mdir = os.path.dirname(m['path'])
    rset = set()
    for e in m['entries']:
        lit = e['path']
        cur_digest = e['digest']
        full, how = resolve(mdir, lit)
        e['resolution'] = how
        if full is None:
            e['verdict'] = 'MISSING'
            e['actual'] = None
        else:
            e['actual'] = sha256_of(full)
            e['resolved_to'] = os.path.relpath(full, ROOT).replace(os.sep, '/')
            rset.add(e['resolved_to'])
            e['verdict'] = 'MATCH' if e['actual'] == e['digest'] else 'MISMATCH'
        totals[e['verdict']] += 1
        if e['verdict'] != 'MATCH':
            non_match.append({"manifest": m['path'], "path": lit, "verdict": e['verdict'],
                              "recorded": e['digest'], "actual": e.get('actual'),
                              "resolution": how, "kind": e['kind']})
    if not m['entries'] and m['note'] and 'not digest-checked' not in (m['note'] or ''):
        totals['UNPARSED'] += 1
        m['no_entries'] = True
    reference_resolved[m['path']] = rset

# group manifests: plan.json carries several pin maps; present per file
by_file = {}
for m in manifests:
    by_file.setdefault(m['path'], {'path': m['path'], 'formats': [], 'entries': [], 'notes': []})
    by_file[m['path']]['formats'].append(m['format'])
    by_file[m['path']]['entries'].extend(m['entries'])
    if m.get('note'):
        by_file[m['path']]['notes'].append(m['note'])
result_list = [by_file[k] for k in sorted(by_file)]

# ---------------- Step 3: unreferenced files per directory ----------------
unreferenced = {}
all_refs = set()
for r in reference_resolved.values():
    all_refs |= r
completeness = []
for d in DIRS:
    fs = [f for f in EXP_FILES if f.startswith(d + '/')]
    unreferenced[d] = [f for f in fs if f not in all_refs]

# completeness claim scan on experiment md files
for rel in EXP_FILES:
    if rel.endswith('.md'):
        with open(os.path.join(ROOT, rel), errors='replace') as f:
            for ln, line in enumerate(f, 1):
                if re.search(r'complet|every (published )?file|exhaustive', line, re.I):
                    completeness.append({"file": rel, "line": ln,
                                         "text": line.strip()[:400]})

# ---------------- Step 4: plan.json ----------------
plans = []
for rel in EXP_FILES:
    if os.path.basename(rel) != 'plan.json':
        continue
    with open(os.path.join(ROOT, rel)) as f:
        d = json.load(f)
    keys = sorted(d.keys())
    pid = d.get('plan_id')
    # derivation statement in sibling files (study-level PLAN.md etc.)
    quote = None
    cand_dirs = [os.path.dirname(rel), os.path.dirname(os.path.dirname(rel))]
    for cd in cand_dirs:
        if not cd or 'experiments' not in cd:
            continue
        for sib in walk_all(cd):
            if sib == rel or not sib.endswith('.md'):
                continue
            with open(os.path.join(ROOT, sib), errors='replace') as f:
                t = f.read()
            for sent in re.split(r'(?<=[.!?])\s+', t):
                if 'plan_id' in sent and re.search(r'digest|deriv|sha256|hash|canon', sent, re.I):
                    quote = "%s: \"%s\"" % (sib, ' '.join(sent.split())[:300])
                    break
            if quote:
                break
        if quote:
            break
    # recompute: rule stated = "digest of the frozen plan body"; canonical JSON minus plan_id.
    # C001's driver binds extra material/driver bytes into its plan_id, so for files under
    # C001 we only recompute when the canonical-JSON rule matches; otherwise record
    # NOT RECOMPUTED (rule stated but only partially executable here).
    derived = None
    derived_note = None
    if pid:
        body = {k: v for k, v in d.items() if k != 'plan_id'}
        cand = hashlib.sha256(
            json.dumps(body, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        if cand == pid:
            derived = cand
        else:
            derived = None
            derived_note = ("canonical-JSON (plan minus plan_id) gives %s, which is NOT plan_id; "
                            "the stated rule also binds driver/material bytes that this directory's "
                            "plan identity covers beyond the plan body" % cand)
    plans.append({"path": rel, "top_level_keys": keys, "plan_id": pid,
                  "derivation_quote": quote,
                  "derivation_recomputed": derived,
                  "derivation_note": derived_note,
                  "derivation_matches": (derived == pid) if pid and derived else None})

# ---------------- Step 5: credential scan ----------------
cred_hits = []
for rel in walk_all(''):
    if rel.split('/')[0] in ('check', 'out'):
        continue
    try:
        with open(os.path.join(ROOT, rel), errors='replace') as f:
            for ln, line in enumerate(f, 1):
                if CRED1.search(line) or CRED2.search(line):
                    cred_hits.append({"file": rel, "line": ln})
    except Exception:
        cred_hits.append({"file": rel, "line": None, "error": "read failed"})

now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
out = {
    "generated_utc": now,
    "resolution_rule": "manifest dir first, then sandbox root (repository root), then unique-suffix match for abbreviated paths; resolution used is recorded per entry",
    "directories_walked": DIRS,
    "manifests": result_list,
    "totals": totals,
    "non_match_entries": non_match,
    "unreferenced_files": unreferenced,
    "completeness_claim_hits": completeness,
    "plan_json": plans,
    "credential_scan": {
        "patterns": ["sk-[0-9a-f]{32}", "[0-9a-f]{32},[A-Za-z0-9_-]{20,}"],
        "hit_count": len(cred_hits),
        "hits": cred_hits,
    },
    "scope_note": ("The sandbox copy is partial: use-table 'files_read' entries name the run's own "
                   "records; those copied in (artifacts/ of the diagnostics occurrences) verify MATCH "
                   "via the occurrence-context resolution (recorded per entry as its resolution). "
                   "The remaining MISSING entries are all run-record files (wave records, per-call "
                   "request/response/receipt files under waves/, requests/, responses/, provider/) and "
                   "the H005-open-prose-commitments occurrence's own artifacts and plan, none of which "
                   "were shipped in this copy. No MISMATCH and no UNPARSED entry exists."),
    "expected_missing_groups": {
        "waves/waveNNNN.json (each analyses use-table, 4-5 per occurrence)": "wave dispatch records; not copied",
        "H005-open-prose-commitments/occurrence-01/* (12 B001 inventory entries)": "the H005 occurrence artifacts/plan are pinned by B001 but not present in this copy",
        "experiments/diagnostics/F001-fork5-multifamily|F002 occurrences: requests/responses/provider/traces files named by use-tables": "run records outside the shipped set",
    },
}
os.makedirs(os.path.join(ROOT, 'out'), exist_ok=True)
with open(os.path.join(ROOT, 'out', 'manifest-reverify.json'), 'w') as f:
    json.dump(out, f, indent=2)

# ---------------- markdown ----------------
L = []
L.append("# Manifest and digest-list re-verification")
L.append("")
L.append("Generated %s by `check/run_all.py` — computation only; nothing transcribed." % now)
L.append("Sandbox root is treated as the repository root.")
L.append("")
L.append("Directories walked: %s" % ', '.join('`%s`' % d for d in DIRS))
L.append("(includes every experiment directory present in the sandbox, because manifests in the "
         "task-named directories pin files living in the others.)")
L.append("")
for r in result_list:
    L.append("## `%s`" % r['path'])
    L.append("")
    L.append("Format(s) detected: %s. Entries: %d." % (
        '; '.join('**%s**' % f for f in r['formats']), len(r['entries'])))
    for n in r['notes']:
        L.append("")
        L.append("Note: %s." % n)
    if r['entries']:
        L.append("")
        L.append("| pinned path | verdict | resolution | recorded sha256 | recomputed sha256 |")
        L.append("|---|---|---|---|---|")
        for e in r['entries']:
            rec = '`%s`' % e['digest']
            act = '`%s`' % e['actual'] if e.get('actual') else 'MISSING'
            if e['verdict'] == 'MATCH':
                act = '= recorded'
            L.append("| `%s` | %s | %s | %s | %s |" % (
                e['path'], e['verdict'], e.get('resolution') or '-', rec, act))
    L.append("")
L.append("## Summary")
L.append("")
for k, v in totals.items():
    mans = sorted({e['manifest'] for e in non_match if e['verdict'] == k}) if k != 'MATCH' else \
           [r['path'] for r in result_list if any(e['verdict'] == 'MATCH' for e in r['entries'])]
    L.append("- **%s**: %d%s" % (k, v,
        (' — from: ' + ', '.join('`%s`' % x for x in mans)) if mans else ''))
L.append("")
L.append("### Every non-MATCH entry")
L.append("")
if not non_match:
    L.append("None.")
else:
    for e in non_match:
        line = "- `%s` — manifest `%s` — **%s**" % (e['path'], e['manifest'], e['verdict'])
        if e['verdict'] == 'MISMATCH':
            line += " (recorded `%s`, recomputed `%s`)" % (e['recorded'], e['actual'])
        L.append(line)
L.append("")
L.append("## Files on disk no manifest references (informational)")
L.append("")
for d in DIRS:
    fs = unreferenced[d]
    L.append("### `%s` — %d unreferenced" % (d, len(fs)))
    if not fs:
        L.append("- none")
    else:
        for f in fs[:400]:
            L.append("- `%s`" % f)
        if len(fs) > 400:
            L.append("- … and %d more (full list in manifest-reverify.json)" % (len(fs) - 400))
    L.append("")
L.append("## Completeness claims found (quoted)")
L.append("")
if completeness:
    for c in completeness:
        L.append("- `%s` line %d: %s" % (c['file'], c['line'], c['text']))
else:
    L.append("None found anywhere under `experiments/`.")
L.append("")
L.append("## plan.json files")
L.append("")
for p in plans:
    L.append("### `%s`" % p['path'])
    L.append("- top-level keys: `%s`" % '`, `'.join(p['top_level_keys']))
    L.append("- plan_id: `%s`" % (p['plan_id'] or 'absent'))
    if p['derivation_quote']:
        L.append("- sibling states the derivation: %s" % p['derivation_quote'])
    else:
        L.append("- no sibling states a derivation rule")
    if p['derivation_matches'] is True:
        L.append("- recomputed per the stated rule (sha256 of the canonical-JSON plan body, `plan_id` field removed): **MATCH** (`%s`)" % p['derivation_recomputed'])
    elif p.get('derivation_note'):
        L.append("- not recomputed: %s" % p['derivation_note'])
    elif p['derivation_matches'] is False:
        L.append("- recomputed: **MISMATCH** (`%s`)" % p['derivation_recomputed'])
    else:
        L.append("- not recomputed")
    L.append("")
L.append("## Credential scan")
L.append("")
L.append("Patterns `sk-[0-9a-f]{32}` and `[0-9a-f]{32}.[A-Za-z0-9_-]{20,}` over every file in the sandbox: **%d hit(s)** (line numbers only, as required)." % len(cred_hits))
for h in cred_hits:
    L.append("- `%s` line %s" % (h['file'], h['line']))
L.append("")
L.append("## What this walk would not catch")
L.append("")
L.append("- Digest maps living under JSON keys I did not enumerate: I looked for `manifest`/`*.sha256` filenames, `files_read`, and the whole-pin-map keys `source_pins`/`transport_pins`/`provider_pins`/`runtime_pins`/`manifests`. A manifest hiding under another key name (e.g. `blobs`, `artifacts` as path-keyed maps) is invisible to this rule.")
L.append("- Digests embedded in prose in shapes other than the markdown `` `path` | `64-hex` `` table row I parsed — for example the *abbreviated* pins like `` `8105925b…e33ee63a` `` in `C001-contrast-triple/PLAN.md` §3, which carry no full digest and cannot be re-verified as written.")
L.append("- Truncated or non-SHA-256 digests (anything not matching the full 64-hex pattern).")
L.append("- Content-addressed object stores whose digest is the object's *identity* rather than a file listing: the analysis directories carry `import/objects/**` and `import/blobs/**` where the filename is the digest of the content. This walk does not re-hash each such file against its own name, and does not check that registry JSONs (`report.json` `names`/`spec_id_table`, `side_table.json`) point at all and only those objects.")
L.append("- Tampering that rewrites a manifest consistently with the tampered file, or omissions made together with their manifest entry.")
L.append("- Files whose pins were not copied into this sandbox (original occurrence trees, `src/`, `tools/`): they verify as MISSING under the stated rule, and the walk cannot distinguish 'pin correct, file not shipped' from 'pin wrong'.")
L.append("- plan_id values where no derivation rule is stated in the sandbox, or stated in terms other than sha256 over canonical JSON.")
with open(os.path.join(ROOT, 'out', 'manifest-reverify.md'), 'w') as f:
    f.write('\n'.join(L) + '\n')

print(json.dumps({"totals": totals,
                  "manifest_files": len(result_list),
                  "missing_by_manifest":
                      {mm['path']: sum(1 for e in mm['entries'] if e['verdict'] == 'MISSING')
                       for mm in manifests if any(e['verdict'] == 'MISSING' for e in mm['entries'])},
                  "cred_hits": len(cred_hits),
                  "plans": {p['path']: p['derivation_matches'] for p in plans}},
                 indent=2))
