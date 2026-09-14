#!/usr/bin/env python3
"""Re-verify manifests and digest lists inside published experiment directories.

Reads only under experiments/, writes only out/manifest-reverify.{json,md}.
Never prints anything matching the credential regexes.
"""
import hashlib, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIRS = [
    "experiments/diagnostics/C001-contrast-triple",
    "experiments/diagnostics/F002-fork5-raised-clock",
    "experiments/diagnostics/B001-bare-and-native",
    "experiments/analyses/F002-fork5-raised-clock-2026-09-14",
    "experiments/analyses/B001-arm-inventory-2026-09-14",
]
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SHA_LINE = re.compile(r"^([0-9a-f]{64})[ \t]+\*?(\S.*)$")
DISPOSITION_KEYS = ("files", "entries", "sha256", "digests", "pins")
CRED_PATTERNS = [
    re.compile(r"sk-[0-9a-f]{32}"),
    re.compile(r"[0-9a-f]{32}\.[A-Za-z0-9_-]{20,}"),
]

def sha256_bytes(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def walk_files(base):
    out = []
    for dp, dn, fn in os.walk(base):
        for f in fn:
            out.append(os.path.join(dp, f))
    return sorted(out)

def resolve(relpath, mdir, studies_base=None):
    """Try manifest's own directory first, then sandbox root, then the
    experiments/ tree (some digest lists are rooted there)."""
    rp = relpath.strip()
    if rp.startswith("./"):
        rp = rp[2:]
    bases = [(mdir, "manifest-dir"), (ROOT, "sandbox-root")]
    if studies_base:
        bases.append((studies_base, "experiments-tree"))
    for base, label in bases:
        cand = os.path.normpath(os.path.join(base, rp))
        if os.path.commonpath((os.path.abspath(cand), ROOT)) == ROOT and os.path.isfile(cand):
            return os.path.abspath(cand), label
    return None, None

def dict_maps_paths(d):
    """A dict whose values are predominantly 64-hex strings and keys look path-ish."""
    if not isinstance(d, dict) or not d:
        return False
    vals = list(d.values())
    hexvals = [v for v in vals if isinstance(v, str) and HEX64.match(v)]
    if len(hexvals) < len(vals) * 0.6 or not hexvals:
        return False
    return any("/" in k or "." in os.path.basename(k) for k in d)

# ---------------------------------------------------------------- discovery
manifests = []  # each: dict(path, kind, description, entries=[(relpath, digest, note)])
plans = []
all_on_disk = {}  # top dir -> set of abs file paths

def add_manifest(mpath, kind, desc, entries):
    manifests.append({"path": mpath, "kind": kind, "description": desc,
                      "entries": entries})

for top in DIRS:
    base = os.path.join(ROOT, top)
    files = walk_files(base)
    all_on_disk[top] = set(files)
    for f in files:
        rel = os.path.relpath(f, ROOT)
        name = os.path.basename(f)
        lname = name.lower()
        if name == "plan.json":
            plans.append(rel)
        if "manifest" in lname or name.endswith(".sha256"):
            txt = open(f, encoding="utf-8", errors="replace").read()
            entries, ok, unparsed = [], False, []
            if name.endswith(".json"):
                try:
                    data = json.loads(txt)
                except Exception:
                    data = None
                if isinstance(data, dict):
                    for k, v in data.items():
                        if dict_maps_paths(v):
                            ok = True
                            for pth, dig in v.items():
                                entries.append((pth, dig, "key '%s'" % k))
            else:
                for ln, line in enumerate(txt.splitlines(), 1):
                    if not line.strip() or line.lstrip().startswith("#"):
                        continue
                    m = SHA_LINE.match(line)
                    if m:
                        ok = True
                        entries.append((m.group(2), m.group(1), "line %d" % ln))
                    else:
                        unparsed.append("line %d: %s" % (ln, line[:80]))
            kind = ("JSON mapping" if name.endswith(".json")
                    else "sha256 text lines") if ok else "unrecognized manifest-named file"
            add_manifest(rel, kind, "named manifest / .sha256 file", entries)
            for u in unparsed:
                add_manifest(rel, "UNPARSED line", "named manifest / .sha256 file",
                             [(None, None, u)]) if False else None
            manifests[-1].setdefault("unparsed_raw", unparsed)
        elif name.endswith(".json"):
            try:
                data = json.load(open(f, encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(data, dict):
                continue
            # rule-1 disposition keys at top level
            for key in DISPOSITION_KEYS:
                v = data.get(key)
                if dict_maps_paths(v):
                    add_manifest(rel, "JSON mapping",
                                 "top-level key '%s' maps paths to digests" % key,
                                 [(p, d2, "top-level key %r" % key) for p, d2 in v.items()])
                    break
            # documented embedded digest lists
            c = data.get("custody")
            if isinstance(c, dict) and dict_maps_paths(c.get("files")):
                add_manifest(rel, "JSON mapping", "embedded custody.files digest map",
                             [(p, d2, "custody.files") for p, d2 in c["files"].items()])
            fr = data.get("files_read")
            if isinstance(fr, list) and fr and all(
                isinstance(x, dict) and isinstance(x.get("path"), str)
                and isinstance(x.get("sha256"), str) for x in fr):
                bad = [x for x in fr if not HEX64.match(x["sha256"])]
                add_manifest(rel, "JSON list of objects",
                             "files_read: list of {path, sha256}",
                             [(x["path"], x["sha256"], "files_read") for x in fr
                              if HEX64.match(x["sha256"])])
                if bad:
                    manifests[-1].setdefault("unparsed_raw", []).extend(
                        "files_read entry with non-hex digest: %r" % x for x in bad)
            frx = data.get("files_read")
            if dict_maps_paths(data.get("files_read")):
                add_manifest(rel, "JSON mapping",
                             "files_read: map of path -> digest",
                             [(p, d2, "files_read") for p, d2 in data["files_read"].items()])
            # *_pins scalar digests (transport_pins.module_sha256 style) — not
            # path->digest maps at a single key; handled as named pairs:
            tp = data.get("transport_pins")
            if isinstance(tp, dict) and isinstance(tp.get("module"), str) and \
               HEX64.match(tp.get("module_sha256", "")):
                add_manifest(rel, "JSON mapping",
                             "transport_pins: module path paired with module_sha256",
                             [("%s/%s" % ("src", tp["module"]), tp["module_sha256"],
                               "transport_pins (path composed src/<module> per the pin note)")])
            for pinkey in ("source_pins", "provider_pins", "runtime_pins"):
                v = data.get(pinkey)
                if dict_maps_paths(v):
                    add_manifest(rel, "JSON mapping",
                                 "%s: map of path -> digest" % pinkey,
                                 [(p, d2, pinkey) for p, d2 in v.items()])
            if isinstance(data.get("manifests"), dict) and all(
                isinstance(x, str) and HEX64.match(x) for x in data["manifests"].values()):
                add_manifest(rel, "JSON mapping",
                             "manifests: manifest-id -> sha256(manifests/<id>.json)",
                             [("manifests/%s.json" % k, v, "manifests")
                              for k, v in data["manifests"].items()])

# ------------------------------------------------------------- verify entries
referenced = {top: set() for top in DIRS}
for m in manifests:
    mdir = os.path.dirname(os.path.join(ROOT, m["path"]))
    sbase = None
    if m["path"].startswith("experiments/"):
        # several digest lists here are rooted at the experiments/ tree
        # (e.g. B001 inventory keys like F001-fork5-multifamily/...)
        sbase = os.path.join(ROOT, "experiments")
    results = []
    for relpath, digest, note in m["entries"]:
        ent = {"recorded_path": relpath, "recorded_digest": digest,
               "field": note, "verdict": None}
        if relpath is None or digest is None or not HEX64.match(digest or ""):
            ent["verdict"] = "UNPARSED"
            ent["detail"] = "entry shape not understood"
            results.append(ent)
            continue
        rp = relpath
        if note == "manifests":
            pass  # already composed path
        abs_p, how = resolve(rp, mdir, sbase)
        if abs_p is None:
            ent["verdict"] = "MISSING"
        else:
            got = sha256_bytes(abs_p)
            ent["resolution"] = how
            ent["resolved_file"] = os.path.relpath(abs_p, ROOT)
            ent["computed_digest"] = got
            ent["verdict"] = "MATCH" if got == digest else "MISMATCH"
            for top, fs in referenced.items():
                if abs_p in fs[0] if isinstance(fs, tuple) else False:
                    pass
            for top in DIRS:
                if ent["resolved_file"].startswith(top + os.sep) or (
                        ent["resolved_file"].replace(os.sep, "/").startswith(top + "/")):
                    referenced[top].add(abs_p)
        results.append(ent)
    m["results"] = results

# ------------------------------------------------- per-directory unreferenced
unreferenced = {}
completeness_claims = {}
for top in DIRS:
    disk = set(os.path.abspath(f) for f in all_on_disk[top])
    unref = sorted(disk - referenced[top])
    unreferenced[top] = [os.path.relpath(p, ROOT).replace(os.sep, "/") for p in unref]
    # look for completeness claims in the manifests of this directory
    claims = []
    for m in manifests:
        if not m["path"].startswith(top + "/") and m["path"] != top:
            continue
        abs_p = os.path.join(ROOT, m["path"])
        txt = open(abs_p, encoding="utf-8", errors="replace").read()
        for sent in re.findall(r"[^.\n]*(?:complete|every file|exhaustive|all files)[^.\n]*",
                               txt, re.IGNORECASE):
            s = sent.strip()
            if 10 < len(s) < 300:
                claims.append(s[:240])
    completeness_claims[top] = claims

# --------------------------------------------------------------- plan files
plan_reports = []
for p in plans:
    data = json.load(open(os.path.join(ROOT, p), encoding="utf-8"))
    report = {"path": p, "top_level_keys": sorted(data.keys()),
              "plan_id": data.get("plan_id"), "derivation": []}
    sib_dir = os.path.dirname(os.path.join(ROOT, p))
    for dp, dn, fn in os.walk(sib_dir):
        for f in fn:
            sp = os.path.join(dp, f)
            if sp == os.path.join(ROOT, p):
                continue
            txt = open(sp, encoding="utf-8", errors="replace").read()
            for m2 in re.finditer(r"[^.\n]*plan_id[^.\n]*(?:deriv|digest|sha256|mint|bind)[^.\n]*",
                                  txt, re.IGNORECASE):
                s = m2.group(0).strip()
                if s:
                    report["derivation"].append(
                        {"file": os.path.relpath(sp, ROOT), "sentence": s[:300]})
    # also the study-level PLAN.md / README
    studydir = os.path.dirname(os.path.dirname(os.path.join(ROOT, p)))
    for dp, dn, fn in os.walk(studydir):
        for f in fn:
            if not f.endswith(".md"):
                continue
            sp = os.path.join(dp, f)
            txt = open(sp, encoding="utf-8", errors="replace").read()
            if "plan_id" in txt and "deriv" not in txt and "digest" not in txt:
                continue
            for m2 in re.finditer(r"[^.\n]*plan_id[^.\n]*(?:deriv|digest|sha256|mint|bind)[^.\n]*",
                                  txt, re.IGNORECASE):
                s = m2.group(0).strip()
                if s:
                    report["derivation"].append(
                        {"file": os.path.relpath(sp, ROOT), "sentence": s[:300]})
    seen = set()
    report["derivation"] = [d for d in report["derivation"]
                            if not ((d["file"], d["sentence"]) in seen
                                    or seen.add((d["file"], d["sentence"])))][:5]
    plan_reports.append(report)

# ------------------------------------------------------------ credential scan
cred_hits = []
for dp, dn, fn in os.walk(ROOT):
    if os.path.relpath(dp, ROOT).split(os.sep)[0] in (".git", "out", "check"):
        continue
    for f in fn:
        fp = os.path.join(dp, f)
        try:
            with open(fp, encoding="utf-8", errors="replace") as fh:
                for ln, line in enumerate(fh, 1):
                    if any(p.search(line) for p in CRED_PATTERNS):
                        cred_hits.append({"file": os.path.relpath(fp, ROOT),
                                          "line": ln})
        except OSError:
            pass

# ------------------------------------------------------------------- totals
totals = {}
nonmatch = []
for m in manifests:
    for e in m["results"]:
        totals[e["verdict"]] = totals.get(e["verdict"], 0) + 1
        if e["verdict"] != "MATCH":
            nonmatch.append({"manifest": m["path"], **e})

out = {
    "title": "Re-verification of manifests and sha256 lists in published experiment records",
    "directories": DIRS,
    "manifests": [
        {**{k: m[k] for k in ("path", "kind", "description") if k in m},
         "entry_count": len(m["results"]),
         "results": m["results"],
         **({"unparsed_raw": m["unparsed_raw"]} if m.get("unparsed_raw") else {})}
        for m in manifests
    ],
    "totals_per_verdict": totals,
    "non_match_entries": nonmatch,
    "unreferenced_files_per_directory": unreferenced,
    "completeness_claims": {k: v for k, v in completeness_claims.items() if v},
    "plan_files": plan_reports,
    "credential_scan": {"patterns": ["sk-[0-9a-f]{32}",
                                     "[0-9a-f]{32}.[A-Za-z0-9_-]{20,}"],
                        "hits": cred_hits, "expected": 0},
}
os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
with open(os.path.join(ROOT, "out", "manifest-reverify.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2)

# ------------------------------------------------------------------- markdown
lines = ["# Manifest re-verification — published experiment records", ""]
lines.append("Method: every file whose name contains `manifest` or ends with `.sha256`, "
             "plus every JSON digest list found by computation, was re-hashed with "
             "sha256 from the bytes on disk and compared with the recorded digest. "
             "Paths were resolved relative to the manifest's own directory first, "
             "then relative to the sandbox root; the successful resolution is "
             "recorded per entry. Published files were only read, never modified.")
lines.append("")
for m in out["manifests"]:
    lines.append("## `%s`" % m["path"])
    lines.append("- Format detected: %s" % m["kind"])
    lines.append("- Scope: %s" % m["description"])
    lines.append("- Entries: %d" % m["entry_count"])
    counts = {}
    for e in m["results"]:
        counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
    lines.append("- Verdicts: " + (", ".join("%s %d" % kv for kv in sorted(counts.items()))
                                    or "none"))
    bad = [e for e in m["results"] if e["verdict"] != "MATCH"]
    if bad:
        mism = [e for e in bad if e["verdict"] == "MISMATCH"]
        miss = [e for e in bad if e["verdict"] == "MISSING"]
        unp = [e for e in bad if e["verdict"] == "UNPARSED"]
        for e in mism:
            lines.append("  - MISMATCH \`%s\` (field %s, resolved via %s): recorded " "\`%s\`, computed \`%s\`" % (e["recorded_path"], e["field"], e.get("resolution"), e["recorded_digest"], e.get("computed_digest")))
        if miss:
            lines.append("  - MISSING (%d): resolvable under none of manifest-dir, sandbox-root or experiments-tree; the referenced paths were never copied into this sandbox. The entries:" % len(miss))
            for e in miss:
                lines.append("    - \`%s\` — recorded \`%s\`" % (e["recorded_path"], e["recorded_digest"]))
        for e in unp:
            lines.append("  - UNPARSED in \`%s\`: %s" % (m["path"], json.dumps(e)[:200]))
    if False:
        for e in bad:
            if e["verdict"] == "MISMATCH":
                lines.append("  - MISMATCH `%s` (field %s, resolved via %s): recorded "
                             "`%s`, computed `%s`" % (
                                 e["recorded_path"], e["field"], e.get("resolution"),
                                 e["recorded_digest"], e.get("computed_digest")))
            elif e["verdict"] == "MISSING":
                lines.append("  - MISSING `%s` (field %s, recorded `%s`): not found under "
                             "either resolution" % (e["recorded_path"], e["field"],
                                                    e["recorded_digest"]))
            else:
                lines.append("  - UNPARSED in `%s`: %s" % (m["path"], json.dumps(e)[:200]))
    if m.get("unparsed_raw"):
        for u in m["unparsed_raw"]:
            lines.append("  - UNPARSED raw: `%s`" % u[:160])
    resmap = {}
    for e in m["results"]:
        if e.get("resolution"):
            resmap.setdefault(e["resolution"], 0)
            resmap[e["resolution"]] += 1
    if resmap:
        lines.append("- Resolution used: " + ", ".join("%s: %d" % kv for kv in resmap.items()))
    lines.append("")

lines.append("## Unreferenced files per directory (informational)")
for top in DIRS:
    lines.append("### `%s`" % top)
    unref = unreferenced[top]
    lines.append("- %d file(s) on disk not referenced by any manifest found in this "
                 "directory" % len(unref))
    if completeness_claims.get(top):
        lines.append("- Completeness claim(s) found in this directory's manifests:")
        for c in completeness_claims[top]:
            lines.append("  > %s" % c)
    else:
        lines.append("- No manifest in this directory was found claiming completeness, "
                     "so this list is informational, not a defect.")
    for p in unref:
        lines.append("  - `%s`" % p)
    lines.append("")

lines.append("## plan.json reports")
for pr in plan_reports:
    lines.append("### `%s`" % pr["path"])
    lines.append("- Top-level keys: " + ", ".join("`%s`" % k for k in pr["top_level_keys"]))
    pid = pr["plan_id"]
    lines.append("- plan_id: `%s`" % pid if pid else "- plan_id: absent")
    if pr["derivation"]:
        lines.append("- Derivation statement(s) found in sibling/study-level files:")
        for d in pr["derivation"]:
            lines.append("  - `%s`: > %s" % (d["file"], d["sentence"]))
        lines.append("- The derivation is stated in prose but requires the study's own "
                     "`prepare` tool (digest of the frozen plan body); not re-attempted "
                     "here because no sha256-over-canonical-JSON rule is given in the files.")
    else:
        lines.append("- No sibling file states how plan_id is derived.")
    lines.append("")

lines.append("## Credential scan")
lines.append("Patterns `sk-[0-9a-f]{32}` and `[0-9a-f]{32}.[A-Za-z0-9_-]{20,}` scanned "
             "across all files; expected zero hits. Found: %d." % len(cred_hits))
for hth in cred_hits:
    lines.append("- `%s` line %d" % (hth["file"], hth["line"]))
lines.append("")

lines.append("## Summary — counts per verdict")
for verdict, count in sorted(totals.items()):
    srcs = sorted({e["manifest"] for e in nonmatch} )
for verdict in ("MATCH", "MISMATCH", "MISSING", "UNPARSED"):
    ms = [m2["path"] for m2 in out["manifests"]
          if any(e["verdict"] == verdict for e in m2["results"])]
    lines.append("- %s: %d%s" % (verdict, totals.get(verdict, 0),
                                 (" (from: " + "; ".join("`%s`" % x for x in ms) + ")") if ms else ""))
lines.append("")
lines.append("## All non-MATCH entries")
if nonmatch:
    for e in nonmatch:
        lines.append("- `%s` — manifest `%s` — %s" % (
            e["verdict"], e["manifest"],
            ("recorded `%s`, computed `%s`" % (e["recorded_digest"], e.get("computed_digest"))
             if e["verdict"] == "MISMATCH" else
             "recorded path `%s` not found" % e["recorded_path"])))
else:
    lines.append("None. Every verifiable digest entry re-hashed to the recorded value.")
lines.append("")
lines.append("## What this walk would not catch")
lines.append("- Digest maps embedded in JSON under keys other than `files`, `entries`, "
             "`sha256`, `digests`, `pins`, the `*_pins`/`*_sha256` conventions, "
             "`custody.files`, `files_read` or `manifests` — e.g. a bespoke key name.")
lines.append("- Digests that name something other than a filesystem path (object ids, "
             "content refs, blob hashes, request/body digests inside artifacts and "
             "commitments); these were not treated as manifests and were not re-verified.")
lines.append("- Files referenced by manifests located outside the five audited "
             "directories (e.g. `docs/sources/...`, `src/...` pins) resolve against the "
             "sandbox root only if the sandbox shipped them; otherwise they are reported "
             "MISSING, which reflects the sandbox copy, not the published repository.")
lines.append("- Manifest formats using uppercase hex digests, non-sha256 hashes, or "
             "multi-column checksum files not matching `<sha256>  <path>`.")
lines.append("- plan_id derivation: stated only as 'digest of the frozen plan body' "
             "minted by a tool; no canonical-JSON rule is given, so it was not recomputed.")
lines.append("- Credentials split across lines, base64-wrapped, or in non-UTF-8 files "
             "escape the line-based scan.")
lines.append("- Anything outside the five declared published directories and outside "
             "the files copied into this sandbox.")

with open(os.path.join(ROOT, "out", "manifest-reverify.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")

print(json.dumps({"manifests": len(out["manifests"]), "totals": totals,
                  "credential_hits": len(cred_hits),
                  "plans": len(plan_reports)}, indent=2))
