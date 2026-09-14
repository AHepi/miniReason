p = 'check/run_all.py'
s = open(p).read()

# exclude 'plan_id' rows from md-table extraction: plan identity is a value, not a path pin
old = """    hits = TBL.findall(txt)
    if hits:
        add(rel, 'markdown table digest list (`path` | `sha256`)',
            [{"kind": "md-table", "path": p, "digest": h} for p, h in hits])
"""
new = """    hits = [(pp, h) for pp, h in TBL.findall(txt) if pp != 'plan_id']
    if hits:
        add(rel, 'markdown table digest list (`path` | `sha256`)',
            [{"kind": "md-table", "path": pp, "digest": h} for pp, h in hits])
"""
assert old in s
s = s.replace(old, new)

# update scope_note / expected_missing_exceptions
old2 = """    "scope_note": (\"The\""""
old2 = """    "scope_note": ("MISSING verdicts are, with named exceptions below, expected under the task's "
                   "partial copy: the sandbox is stated to contain the named directories plus every "
                   "file the manifests pin outside them 'copied in at its repository path'. Entries "
                   "whose pins were copied in verify as MATCH; entries pointing into the original "
                   "occurrence trees (artifacts/, attempts/, requests/, material.json, src/, tools/), "
                   "which were not copied in, verify as MISSING under the stated rule."),
    "expected_missing_exceptions": [
        "experiments/diagnostics/C001-contrast-triple/PLAN.md pins material.json and occurrence-01 brief/request bytes that are absent from the sandbox copy (named by the plan as its own material)",
    ],
"""
new2 = """    "scope_note": ("The sandbox copy is partial: use-table 'files_read' entries name the run's own "
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
"""
assert old2 in s
s = s.replace(old2, new2)
open(p, 'w').write(s)
print('patched')
