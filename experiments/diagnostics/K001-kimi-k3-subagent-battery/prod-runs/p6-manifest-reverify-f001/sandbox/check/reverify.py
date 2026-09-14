#!/usr/bin/env python3
"""Re-verify every manifest and digest list in the published experiment dirs."""
import os, json, re, hashlib, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIRS = [
    "experiments/diagnostics/C001-contrast-triple",
    "experiments/diagnostics/F002-fork5-raised-clock",
    "experiments/diagnostics/B001-bare-and-native",
    "experiments/analyses/F002-fork5-raised-clock-2026-09-14",
    "experiments/analyses/B001-arm-inventory-2026-09-14",
    # also present in sandbox; verify everything published
    "experiments/analyses/F001-fork5-multifamily-2026-09-14",
]

HEX64 = re.compile(r'^[0-9a-f]{64}$')
KEYCAND = {"files", "entries", "sha256", "digests", "pins"}

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def walk(dirpath):
    out = []
    for dp, dns, fns in os.walk(os.path.join(ROOT, dirpath)):
        dns.sort(); fns.sort()
        for fn in fns:
            out.append(os.path.relpath(os.path.join(dp, fn), ROOT))
    return out

def looks_like_mapping(v):
    if not isinstance(v, dict):
        return False
    for val in v.values():
        if isinstance(val, str) and HEX64.match(val):
            continue
        if isinstance(val, dict) and any(HEX64.match(str(x)) for x in val.values()):
            continue
        return False
    return len(v) > 0

def find_manifest_files(dirs):
    found = []  # (path, format)
    for d in dirs:
        for p in walk(d):
            base = os.path.basename(p).lower()
            if 'manifest' in base or base.endswith('.sha256'):
                fmt = None
                if base.endswith('.json'):
                    fmt = 'json'
                else:
                    fmt = 'text-lines'
                found.append((p, fmt))
                continue
            if base.endswith('.json'):
                try:
                    with open(os.path.join(ROOT, p)) as f:
                        data = json.load(f)
                except Exception:
                    continue
                if isinstance(data, dict):
                    for k in KEYCAND:
                        if k in data:
                            v = data[k]
                            if looks_like_mapping(v) or isinstance(v, list):
                                found.append((p, 'json-key:' + k))
                            break
    return found

SHA_LINE = re.compile(r'^([0-9a-fA-F]{64})[ \t]{1,2}\*?(.+?)\s*$')

def parse_manifest(path, fmt):
    full = os.path.join(ROOT, path)
    entries = []  # (recorded, relpath_literal)
    unparsed = []
    if fmt == 'json' or fmt.startswith('json-key'):
        with open(full) as f:
            data = json.load(f)
        if fmt == 'json':
            # detect shape
            if isinstance(data, dict):
                if looks_like_mapping(data):
                    for k, v in data.items():
                        if isinstance(v, str):
                            entries.append((v, k))
                        elif isinstance(v, dict):
                            for kk, vv in v.items():
                                if isinstance(vv, str) and HEX64.match(vv):
                                    entries.append((vv, k))
                                else:
                                    unparsed.append({k: v})
                        else:
                            unparsed.append({k: v})
                else:
                    for k, v in data.items():
                        if k in KEYCAND:
                            fmt2 = 'json-key:' + k
                            e2, u2 = parse_manifest(path, fmt2)
                            return e2, u2, path, fmt2
                        else:
                            unparsed.append({k: v})
        else:
            key = fmt.split(':', 1)[1]
            v = data[key]
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    if isinstance(v2, str) and HEX64.match(v2):
                        entries.append((v2, k2))
                    elif isinstance(v2, dict):
                        got = False
                        for kk, vv in v2.items():
                            if kk == 'sha256' and isinstance(vv, str) and HEX64.match(vv):
                                entries.append((vv, k2)); got = True
                        if not got:
                            unparsed.append({k2: v2})
                    else:
                        unparsed.append({k2: v2})
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        h = item.get('sha256') or item.get('digest') or item.get('hash')
                        p = item.get('path') or item.get('file') or item.get('name')
                        if isinstance(h, str) and HEX64.match(h) and isinstance(p, str):
                            entries.append((h, p))
                        else:
                            unparsed.append(item)
                    else:
                        unparsed.append(item)
    else:
        with open(full) as f:
            for line in f:
                line = line.rstrip('\n')
                if not line.strip() or line.strip().startswith('#'):
                    continue
                m = SHA_LINE.match(line)
                if m:
                    entries.append((m.group(1).lower(), m.group(2).strip()))
                else:
                    unparsed.append(line)
    return entries, unparsed, path, fmt

def main():
    dirs = [d for d in DIRS if os.path.isdir(os.path.join(ROOT, d))]
    manifests = find_manifest_files(dirs)
    manifests = sorted(set(manifests))
    results = []
    totals = {"MATCH": 0, "MISMATCH": 0, "MISSING": 0, "UNPARSED": 0}
    non_match = []
    for path, fmt in manifests:
        entries, unparsed, path, fmt = parse_manifest(path, fmt)
        det = {
            "plain": "text-lines" if fmt == "text-lines" else
                     ("JSON mapping" if fmt == "json" else
                      "JSON key '%s'" % fmt.split(':',1)[1]),
            "fmt": fmt,
        }
        mdir = os.path.dirname(path)
        ev = []
        for recorded, lit in entries:
            cand1 = os.path.join(ROOT, mdir, lit)
            cand2 = os.path.join(ROOT, lit)
            verdict = None; actual = None; resol = None
            if os.path.isfile(cand1):
                resol = "manifest-dir"
                actual = sha256_of(cand1)
            elif os.path.isfile(cand2):
                resol = "repo-root"
                actual = sha256_of(cand2)
            else:
                verdict = "MISSING"
            if verdict is None:
                verdict = "MATCH" if actual == recorded else "MISMATCH"
            e = {"path": lit, "recorded": recorded, "verdict": verdict,
                 "resolution": resol, "actual": actual}
            ev.append(e)
            totals[verdict] += 1
            if verdict != "MATCH":
                non_match.append({"manifest": path, **e})
        for u in unparsed:
            totals["UNPARSED"] += 1
            non_match.append({"manifest": path, "verdict": "UNPARSED", "entry": u,
                              "path": None, "recorded": None, "actual": None,
                              "resolution": None})
        results.append({"manifest": path, "format": det, "entries": ev,
                        "unparsed": unparsed})

    # step 3: unreferenced files per directory
    unref = {}
    for d in dirs:
        files = walk(d)
        refs = set()
        for path, fmt in manifests:
            mdir = os.path.dirname(path)
            if mdir != d and not mdir.startswith(d + os.sep):
                continue
            entries, _, _, _ = parse_manifest(path, fmt)
            for recorded, lit in entries:
                c1 = os.path.normpath(os.path.join(mdir, lit)).replace(os.sep, '/')
                c2 = lit.replace(os.sep, '/')
                refs.add(c1); refs.add(c2)
        unref[d] = [f.replace(os.sep, '/') for f in files
                    if f.replace(os.sep, '/') not in refs]
    return results, totals, non_match, unref, dirs

if __name__ == '__main__':
    results, totals, non_match, unref, dirs = main()
    with open(os.path.join(ROOT, 'check', 'reverify-results.json'), 'w') as f:
        json.dump({"results": results, "totals": totals,
                   "non_match": non_match, "unreferenced": unref,
                   "dirs": dirs}, f, indent=2)
    print(json.dumps({"totals": totals,
                      "manifests": [r["manifest"] for r in results]}, indent=2))
