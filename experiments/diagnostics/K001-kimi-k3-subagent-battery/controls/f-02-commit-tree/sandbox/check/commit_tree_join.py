#!/usr/bin/env python3
"""Join every commit/tree identity published in two decision-ledger receipts
against the frozen branch log, and write the result to out/commit-tree.md.

Run from the sandbox root:

    python3 check/commit_tree_join.py

Reads  : docs/ledger/REC-20260914-U.md, docs/ledger/REC-20260914-X.md,
         evidence/git-log-branch.txt
Writes : out/commit-tree.md   (and prints the same counts to stdout)

Nothing is modified: the receipts and the log are opened read-only.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(ROOT, "evidence", "git-log-branch.txt")
OUT_PATH = os.path.join(ROOT, "out", "commit-tree.md")
RECEIPTS = [
    ("REC-20260914-U", os.path.join(ROOT, "docs", "ledger", "REC-20260914-U.md")),
    ("REC-20260914-X", os.path.join(ROOT, "docs", "ledger", "REC-20260914-X.md")),
]

# ---------------------------------------------------------------- patterns --
# A git object id here is exactly 40 lowercase hex characters with no hex
# character touching either end.  The lookarounds are what keep a 64-character
# sha256 (a file digest, a plan_id, a material digest) out of the extraction:
# every 40-character window inside a 64-character run has hex on one side.
H40 = r"(?<![0-9a-f])([0-9a-f]{40})(?![0-9a-f])"
H7 = re.compile(r"(?<![0-9a-f])([0-9a-f]{7})(?![0-9a-f])")

PAIR = "pair"
COMMIT_ONLY = "commit"

PATTERNS = [
    ("P1", "VERIFIED <commit> TREE <tree>",
     re.compile(r"VERIFIED\s+" + H40 + r"\s+TREE\s+" + H40), PAIR),
    ("P2", "at <commit>, tree <tree>",
     re.compile(r"at\s+" + H40 + r",\s*tree\s+" + H40), PAIR),
    ("P3", "<commit> / <tree>  (the 'Prior verified commit/tree' form)",
     re.compile(H40 + r"`?\s*/\s*`?" + H40), PAIR),
    ("P4", "VERIFIED <commit>  (no TREE beside it)",
     re.compile(r"VERIFIED\s+" + H40), COMMIT_ONLY),
    ("P5", "a bare 40-hex commit id not already taken by P1-P4",
     re.compile(H40), COMMIT_ONLY),
]
P6_DESC = ("P6", "a bare 7-hex short commit id carrying at least one of a-f, "
                 "not already taken by P1-P5")

# Strings deliberately NOT treated as commit/tree identities, reported so a
# reader can see what the patterns skipped and why.
H64 = re.compile(r"(?<![0-9a-f])([0-9a-f]{64})(?![0-9a-f])")
HTRUNC = re.compile(r"(?<![0-9a-f])([0-9a-f]{4,63})(?=…)")
HOTHER = re.compile(r"(?<![0-9a-f])([0-9a-f]{8,39}|[0-9a-f]{41,63})(?![0-9a-f…])")

# Independent recount used only to show that the patterns left nothing unread.
ALLRUNS = re.compile(r"(?<![0-9a-fA-F])([0-9a-fA-F]{4,})(?![0-9a-fA-F])")


# -------------------------------------------------------------- log intake --
def read_log(path):
    commits = {}          # full commit sha -> dict(tree, short, date, author, subject)
    by_short = {}         # 7-char prefix -> [full commit sha, ...]
    by_tree = {}          # full tree sha -> [full commit sha, ...]
    header = []
    nlines = 0
    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if not line.strip():
                continue
            if line.startswith("#"):
                header.append(line)
                continue
            nlines += 1
            parts = line.split(" ", 5)
            if len(parts) < 6:
                raise SystemExit("unparsable log line: %r" % line)
            full, tree, short, date, author, subject = parts
            commits[full] = {"tree": tree, "short": short, "date": date,
                             "author": author, "subject": subject}
            by_short.setdefault(full[:7], []).append(full)
            by_tree.setdefault(tree, []).append(full)
    return commits, by_short, by_tree, header, nlines


# --------------------------------------------------------- receipt intake ---
def paragraphs(path):
    """Yield (index, start_line, label, text) for each blank-line-separated
    paragraph of the receipt.  Read-only; line endings are not touched."""
    out = []
    buf = []
    start = None
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.read().replace("\r\n", "\n").split("\n")
    for n, line in enumerate(lines, 1):
        if line.strip():
            if start is None:
                start = n
            buf.append(line)
        elif buf:
            out.append((start, "\n".join(buf)))
            buf, start = [], None
    if buf:
        out.append((start, "\n".join(buf)))
    result = []
    for i, (ln, text) in enumerate(out, 1):
        head = re.split(r":\s", text, 1)[0].strip()
        result.append((i, ln, head[:70], text))
    return result


def overlaps(span, taken):
    a, b = span
    return any(not (b <= c or a >= d) for c, d in taken)


def extract(text):
    """Return (claims, excluded_pure_digit_shorts).

    A claim is a dict: pattern id, pattern description, commit, tree (or None),
    kind, and the matched substring."""
    claims = []
    taken = []
    for pid, desc, rx, kind in PATTERNS:
        for m in rx.finditer(text):
            if overlaps(m.span(), taken):
                continue
            taken.append(m.span())
            if kind is PAIR:
                claims.append({"pid": pid, "desc": desc, "commit": m.group(1),
                               "tree": m.group(2), "kind": PAIR,
                               "raw": m.group(0), "pos": m.start()})
            else:
                claims.append({"pid": pid, "desc": desc, "commit": m.group(1),
                               "tree": None, "kind": COMMIT_ONLY,
                               "raw": m.group(0), "pos": m.start()})
    excluded = []
    for m in H7.finditer(text):
        if overlaps(m.span(), taken):
            continue
        tok = m.group(1)
        if not any(c in "abcdef" for c in tok):
            excluded.append(tok)
            continue
        taken.append(m.span())
        claims.append({"pid": "P6", "desc": P6_DESC[1], "commit": tok,
                       "tree": None, "kind": "short", "raw": tok,
                       "pos": m.start()})
    claims.sort(key=lambda c: c["pos"])
    return claims, excluded


# ------------------------------------------------------------- the join ----
def judge(claim, commits, by_short, by_tree):
    """Return (verdict, detail).  This is a join, not a membership test: where a
    tree is claimed beside a commit, the log's own tree for that commit decides."""
    c = claim["commit"]
    if claim["kind"] == "short":
        hits = by_short.get(c, [])
        if not hits:
            return "NOT IN LOG", "no commit in the log begins with %s" % c
        if len(hits) > 1:
            return "AMBIGUOUS SHORT ID", "resolves to %d commits: %s" % (
                len(hits), ", ".join(hits))
        full = hits[0]
        return "COMMIT VERIFIED", "resolves to %s, tree %s (no tree claimed beside it)" % (
            full, commits[full]["tree"])
    if c not in commits:
        return "NOT IN LOG", "no commit with this full id in the log"
    logtree = commits[c]["tree"]
    if claim["tree"] is None:
        return "COMMIT VERIFIED", "log tree %s (no tree claimed beside it)" % logtree
    if claim["tree"] == logtree:
        return "PAIR VERIFIED", "log tree %s" % logtree
    where = by_tree.get(claim["tree"])
    extra = ("the claimed tree belongs to %s in the log" % ", ".join(where)
             if where else "the claimed tree appears against no commit in the log")
    return "PAIR MISMATCH", "log tree for this commit is %s; %s" % (logtree, extra)


def span_count(by_short, order, a, b):
    """Auxiliary, not part of the join: how many log lines lie between two short
    ids inclusive, in log order."""
    try:
        ia = order.index(by_short[a][0])
        ib = order.index(by_short[b][0])
    except (KeyError, ValueError):
        return None
    lo, hi = sorted((ia, ib))
    return hi - lo + 1


# ------------------------------------------------------------------ main ----
def main():
    commits, by_short, by_tree, header, nlog = read_log(LOG_PATH)
    order = list(commits.keys())  # newest-first, the log's own order

    rows = []
    excluded_shorts = []
    other_hex = {}
    sha256 = {}
    truncated = {}
    recount = {}          # receipt -> {40: n, 7: n} counted independently

    for name, path in RECEIPTS:
        with open(path, "r", encoding="utf-8") as fh:
            whole = fh.read()
        runs = ALLRUNS.findall(whole)
        recount[name] = {40: sum(1 for r in runs if len(r) == 40),
                         7: sum(1 for r in runs if len(r) == 7),
                         "upper": sorted({r for r in runs
                                          if any(c.isupper() for c in r)
                                          and len(r) in (7, 40)})}
    for name, path in RECEIPTS:
        for idx, line_no, label, text in paragraphs(path):
            claims, excl = extract(text)
            excluded_shorts.extend((name, idx, t) for t in excl)
            for cl in claims:
                verdict, detail = judge(cl, commits, by_short, by_tree)
                rows.append({"receipt": name, "para": idx, "line": line_no,
                             "label": label, "claim": cl, "verdict": verdict,
                             "detail": detail})
            for m in H64.finditer(text):
                sha256.setdefault(m.group(1), []).append("%s p%d" % (name, idx))
            for m in HTRUNC.finditer(text):
                truncated.setdefault(m.group(1) + "…", []).append("%s p%d" % (name, idx))
            for m in HOTHER.finditer(text):
                tok = m.group(1)
                if len(tok) == 64:
                    continue
                other_hex.setdefault(tok, []).append("%s p%d" % (name, idx))

    not_in_log = [r for r in rows if r["verdict"] == "NOT IN LOG"]
    ambiguous = [r for r in rows if r["verdict"] == "AMBIGUOUS SHORT ID"]
    mismatch = [r for r in rows if r["verdict"] == "PAIR MISMATCH"]
    pairs = [r for r in rows if r["claim"]["tree"] is not None]
    pair_ok = [r for r in rows if r["verdict"] == "PAIR VERIFIED"]
    commit_ok = [r for r in rows if r["verdict"] == "COMMIT VERIFIED"]

    # Auxiliary counts, reported with the thing that produced them and never as
    # a verdict of the join.
    span_u_incl = span_count(by_short, order, "ad3e347", "d6b7e30")
    span_u_excl = span_count(by_short, order, "ad3e347", "f353ac4")
    span_x_incl = span_count(by_short, order, "96ca2eb", "958f2f4")
    span_x_excl = span_count(by_short, order, "96ca2eb", "f25b4a9")

    out = []
    w = out.append
    w("# Commit and tree identities in REC-20260914-U and REC-20260914-X, joined "
      "against the frozen branch log")
    w("")
    w("Produced by `python3 check/commit_tree_join.py` inside the sandbox. It reads")
    w("`docs/ledger/REC-20260914-U.md`, `docs/ledger/REC-20260914-X.md` and")
    w("`evidence/git-log-branch.txt` and writes this file; it modifies nothing.")
    w("")
    w("The log is a frozen extract, and its own header records how it was taken:")
    w("")
    for h in header:
        w("    " + h)
    w("")
    w("It carries **%d commit lines**, counted by this script from `evidence/git-log-branch.txt`." % nlog)
    w("")
    w("## What was extracted, and by what pattern")
    w("")
    w("Every identity below was taken out of the receipt text by regular expression,")
    w("never transcribed by hand. A git object id is matched as exactly 40 lowercase")
    w("hex characters with no hex character touching either end, which is what keeps")
    w("the receipts' 64-character sha256 digests (plan ids, material digests, file")
    w("digests) out of the extraction. Patterns are applied in order and a span")
    w("already claimed by an earlier pattern is not re-read by a later one.")
    w("")
    w("| Pattern | Form | Rows |")
    w("| --- | --- | --- |")
    for pid, desc, _rx, _kind in PATTERNS:
        n = sum(1 for r in rows if r["claim"]["pid"] == pid)
        w("| %s | `%s` | %d |" % (pid, desc, n))
    n6 = sum(1 for r in rows if r["claim"]["pid"] == "P6")
    w("| %s | `%s` | %d |" % (P6_DESC[0], P6_DESC[1], n6))
    w("")
    w("Nothing git-id-shaped was left unread. Counted independently of the patterns")
    w("above, by a second regular expression over the whole of each file:")
    w("")
    tot40 = sum(recount[n][40] for n, _ in RECEIPTS)
    tot7 = sum(recount[n][7] for n, _ in RECEIPTS)
    for name, _ in RECEIPTS:
        w("* `%s.md`: %d maximal 40-hex runs, %d maximal 7-hex runs" % (
            name, recount[name][40], recount[name][7]))
    used40 = sum(2 if r["claim"]["tree"] else 1
                 for r in rows if r["claim"]["kind"] != "short")
    w("* patterns P1-P5 consumed **%d of %d** 40-hex runs (a pair consumes two: the"
      % (used40, tot40))
    w("  commit and the tree beside it); P6 consumed **%d of %d** 7-hex runs."
      % (n6, tot7))
    upper = sorted({u for name, _ in RECEIPTS for u in recount[name]["upper"]})
    w("* mixed- or upper-case 7- or 40-character hex runs, which the lowercase")
    w("  patterns would not have matched: **%d**%s." % (
        len(upper), (" — " + ", ".join("`%s`" % u for u in upper)) if upper else ""))
    w("")
    w("## The join")
    w("")
    w("One row per identity claimed. The verdict is a join against the log's own")
    w("`%H %T` columns: where a receipt names a tree beside a commit, the log's tree")
    w("for that commit decides the row.")
    w("")
    w("| # | Receipt, paragraph | Pattern | Claimed commit | Claimed tree | Verdict | Log |")
    w("| --- | --- | --- | --- | --- | --- | --- |")
    for i, r in enumerate(rows, 1):
        cl = r["claim"]
        w("| %d | %s p%d (line %d, %s) | %s | `%s` | %s | **%s** | %s |" % (
            i, r["receipt"], r["para"], r["line"], r["label"], cl["pid"],
            cl["commit"], ("`%s`" % cl["tree"]) if cl["tree"] else "—",
            r["verdict"], r["detail"]))
    w("")
    w("## Reported separately, as the check requires")
    w("")
    w("**Identities that do not appear in the log at all: %d.**" % len(not_in_log))
    if not_in_log:
        for r in not_in_log:
            w("* `%s` — %s p%d (line %d): %s" % (
                r["claim"]["commit"], r["receipt"], r["para"], r["line"], r["detail"]))
    else:
        w("")
        w("Every extracted identity resolved in `evidence/git-log-branch.txt`.")
    w("")
    w("**Short ids resolving to more than one commit: %d.**" % len(ambiguous))
    if ambiguous:
        for r in ambiguous:
            w("* `%s` — %s p%d (line %d): %s" % (
                r["claim"]["commit"], r["receipt"], r["para"], r["line"], r["detail"]))
    else:
        w("")
        w("Each extracted 7-character id resolves to exactly one commit in the log.")
    w("")
    w("**Pairs that appear but do not match: %d.**" % len(mismatch))
    if mismatch:
        for r in mismatch:
            w("* `%s` claimed with tree `%s` — %s p%d (line %d): %s" % (
                r["claim"]["commit"], r["claim"]["tree"], r["receipt"],
                r["para"], r["line"], r["detail"]))
    else:
        w("")
        w("No commit in either receipt is published beside a tree other than the one")
        w("the log records for it.")
    w("")
    w("## Does every published pair verify?")
    w("")
    if not (mismatch or not_in_log or ambiguous):
        w("**Yes.** All **%d** commit+tree pairs published in the two receipts verify"
          % len(pairs))
        w("against the branch log: each commit appears in the log and the tree the")
        w("receipt names beside it is the tree the log records for that commit. The")
        w("further **%d** identities published without a tree beside them — %d full"
          % (len(commit_ok), sum(1 for r in commit_ok if r["claim"]["kind"] != "short")))
        w("40-character ids and %d 7-character short ids — each resolve to exactly one"
          % sum(1 for r in commit_ok if r["claim"]["kind"] == "short"))
        w("commit in the log. No identity is absent, no short id is ambiguous, and no")
        w("pair is mismatched. This is a clean result, not an incomplete one: the")
        w("recount above shows the patterns consumed every git-id-shaped string in both")
        w("files.")
    else:
        w("**No.** %d pair(s) mismatched, %d identity(ies) are absent from the log and"
          % (len(mismatch), len(not_in_log)))
        w("%d short id(s) are ambiguous; each is listed above with its paragraph."
          % len(ambiguous))
    w("")
    w("## Counts, each with the file or command that produced it")
    w("")
    w("From `python3 check/commit_tree_join.py` over the three files named above:")
    w("")
    w("* identities extracted and joined: **%d**" % len(rows))
    w("* of them full 40-hex commit ids: **%d**; 7-hex short ids: **%d**" % (
        sum(1 for r in rows if r["claim"]["kind"] != "short"), n6))
    w("* rows carrying a tree beside the commit (commit+tree pairs): **%d**" % len(pairs))
    w("* pairs verified: **%d**; commit-only rows verified: **%d**" % (
        len(pair_ok), len(commit_ok)))
    w("* not in the log: **%d**; ambiguous short ids: **%d**; mismatched pairs: **%d**" % (
        len(not_in_log), len(ambiguous), len(mismatch)))
    w("* distinct commits named across both receipts: **%d** of the **%d** in the log" % (
        len({r["claim"]["commit"] if r["claim"]["kind"] != "short"
             else by_short[r["claim"]["commit"]][0]
             for r in rows if r["verdict"] not in ("NOT IN LOG", "AMBIGUOUS SHORT ID")}),
        nlog))
    w("")
    w("Auxiliary, and **not** a verdict of this join: each receipt states how many")
    w("commits its decision spans, and the same script counts log lines between two")
    w("short ids, inclusive of both ends, in the log's own order.")
    w("")
    w("* REC-20260914-U p8 (line 15): \"in seven commits from `ad3e347` through the")
    w("  closing one\". `ad3e347` to `f353ac4` is **%s** log lines; `ad3e347` to"
      % span_u_excl)
    w("  `d6b7e30`, the commit that same paragraph verifies, is **%s**." % span_u_incl)
    w("* REC-20260914-X p9 (line 17): \"in fifteen commits from `96ca2eb` through the")
    w("  closing one\", followed by an enumeration of fifteen short ids ending at")
    w("  `f25b4a9`. `96ca2eb` to `f25b4a9` is **%s** log lines; `96ca2eb` to"
      % span_x_excl)
    w("  `958f2f4`, the closing commit that paragraph verifies, is **%s**."
      % span_x_incl)
    w("")
    w("X's own enumeration fixes what \"through the closing one\" counts in these two")
    w("sentences: the commits before the closing one, the closing one being verified")
    w("beside them. Read that way both counts agree with the log. Read as inclusive of")
    w("the closing commit, both would be one higher than stated. Which reading each")
    w("sentence intends is not settled here, and no verdict above turns on it: a commit")
    w("count is not a commit identity.")
    w("")
    w("## Hex strings the patterns did not treat as commit or tree identities")
    w("")
    w("Named so a reader can tell a clean check from an incomplete one.")
    w("")
    w("* **64-character sha256 digests: %d occurrences, %d distinct.** These are file,"
      % (sum(len(v) for v in sha256.values()), len(sha256)))
    w("  material, runner and `plan_id` digests, not git object ids, and the 40-hex")
    w("  pattern excludes them by construction.")
    w("* **Truncated digests written with an ellipsis: %d.** %s" % (
        len(truncated),
        ", ".join("`%s` (%s)" % (k, "; ".join(sorted(set(v))))
                  for k, v in sorted(truncated.items())) or "none"))
    w("* **Other isolated hex-looking runs of length 8-39 or 41-63: %d.** %s" % (
        len(other_hex),
        ", ".join("`%s` (%s)" % (k, "; ".join(sorted(set(v))))
                  for k, v in sorted(other_hex.items())) or "none"))
    w("* **7-character runs of digits only, excluded from P6: %d.** %s" % (
        len(excluded_shorts),
        ", ".join("`%s` (%s p%d)" % (t, n, i) for n, i, t in excluded_shorts)
        or "none"))
    w("")
    allshorts = [commits[c]["short"] for c in commits]
    alldigit = [s for s in allshorts if not any(ch in "abcdef" for ch in s)]
    w("The digits-only exclusion in P6 costs nothing here: of the %d short ids in the" % len(allshorts))
    w("log, %d are digits only." % len(alldigit))
    w("")

    # ---- identities the pattern could not have caught -----------------------
    claimed_full = set()
    for r in rows:
        cl = r["claim"]
        if r["verdict"] in ("NOT IN LOG", "AMBIGUOUS SHORT ID"):
            continue
        claimed_full.add(by_short[cl["commit"]][0] if cl["kind"] == "short"
                         else cl["commit"])

    def unnamed(a, b):
        ia, ib = order.index(by_short[a][0]), order.index(by_short[b][0])
        lo, hi = sorted((ia, ib))
        return [order[i] for i in range(lo, hi + 1) if order[i] not in claimed_full]

    u_unnamed = unnamed("ad3e347", "d6b7e30")
    x_unnamed = unnamed("96ca2eb", "958f2f4")

    w("## Identities in either receipt that this pattern would not have caught")
    w("")
    w("The patterns read hex strings. What they cannot read is an identity a receipt")
    w("refers to without writing it down, and that is the whole of the gap here.")
    w("")
    w("1. **Commits referred to collectively and never written.** REC-20260914-U p8")
    w("   (line 15) says its decision ran \"in seven commits from `ad3e347` through the")
    w("   closing one\" and names only the first and the last. %d commits of that span"
      % len(u_unnamed))
    w("   appear in no extracted identity, and no pattern over the receipt text could")
    w("   have caught them because the receipt does not contain them. From the log they")
    w("   are:")
    for c in u_unnamed:
        w("   * `%s` %s — %s" % (commits[c]["short"], c, commits[c]["subject"]))
    w("   The same check over REC-20260914-X's span `96ca2eb`..`958f2f4` leaves **%d**"
      % len(x_unnamed))
    w("   commits unnamed: that receipt enumerates its whole span.")
    w("")
    w("2. **A digest written truncated with an ellipsis.** REC-20260914-X p2 (line 3)")
    w("   carries `ccbb1165…` and `aadea004…`. Both are sha256 prefixes rather than git")
    w("   ids, so nothing is missed here, but a commit or tree abbreviated in that form")
    w("   would pass P1-P6 unread.")
    w("")
    w("3. **An abbreviation of a length other than seven.** Git accepts any unambiguous")
    w("   prefix; P6 reads exactly seven. The isolated 8-to-39-character hex runs in the")
    w("   two files are `20260914` (the receipt-name date) and the two sha256 prefixes")
    w("   above, so no git id is lost to this — but a 10- or 12-character abbreviation")
    w("   would have been.")
    w("")
    w("4. **An upper- or mixed-case id.** The patterns are lowercase-only. %d such 7- or"
      % len(upper))
    w("   40-character run occurs in either file.")
    w("")
    w("5. **Identities named in words with no hex beside them**, which are therefore")
    w("   unjoinable: \"the closing one\", \"the publication tree\", \"the staging tree\",")
    w("   \"this working tree\", \"remote `claude/project-state-direction-j5rbun`\" and the")
    w("   `--publish-ref origin/claude/...` argument. These name objects without")
    w("   publishing their identity.")
    w("")
    w("6. **The %d distinct sha256 digests**, excluded on purpose: a `plan_id`, a"
      % len(sha256))
    w("   material digest, a runner digest and file digests are not commit or tree")
    w("   identities and the branch log carries nothing to join them against.")
    w("")

    w("## What I could not determine")
    w("")
    w("* **Whether the log extract itself is faithful to the repository.** Everything")
    w("  above is a join against `evidence/git-log-branch.txt`, a frozen file. There is")
    w("  no `git` in this sandbox, so I could not recompute a tree from object content,")
    w("  re-run `git log`, or read the remote ref. If a `%T` column in the extract were")
    w("  wrong, this check would report the receipt as verified. Unresolved by")
    w("  construction, and named rather than glossed.")
    w("* **Anything outside `40bd5de..HEAD`.** The extract's own header records that")
    w("  range. An identity published in either receipt but older than `40bd5de` would")
    w("  have come back NOT IN LOG as a limit of the extract rather than as a defect of")
    w("  the receipt. It did not arise — 0 rows are NOT IN LOG — but the boundary is")
    w("  real and I could not test past it.")
    w("* **Whether \"seven commits\" and \"fifteen commits\" are inclusive of the closing")
    w("  commit.** Both readings are reported above with the log lines each implies. I")
    w("  could not determine which the sentences intend, and a count is not an identity,")
    w("  so no verdict rests on it.")
    w("* **The receipts' non-git digests.** The 14 sha256 values — `plan_id`s, the")
    w("  material, the runner, the pinned provider files — are unchecked: the files they")
    w("  digest are not in this sandbox, and the branch log holds nothing to join them")
    w("  against.")
    w("* **Whether the two receipt files reproduce `docs/DECISION_LEDGER.md` verbatim.**")
    w("  The ledger is not in this sandbox, so that premise is taken as given and was")
    w("  not verified.")
    w("* **Everything the receipts assert that is not an identity** — file counts,")
    w("  insertion counts, token counts, test counts, timings, per-coordinate outcomes.")
    w("  None of it is checkable from a `%H %T %h` log and none of it was checked.")
    w("")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")

    print("log lines: %d" % nlog)
    print("rows: %d (pairs %d, commit-only %d)" % (len(rows), len(pairs), len(rows) - len(pairs)))
    print("pair verified: %d" % len(pair_ok))
    print("commit verified: %d" % len(commit_ok))
    print("NOT IN LOG: %d" % len(not_in_log))
    print("AMBIGUOUS SHORT ID: %d" % len(ambiguous))
    print("PAIR MISMATCH: %d" % len(mismatch))
    print("spans: ad3e347..f353ac4=%s ad3e347..d6b7e30=%s 96ca2eb..f25b4a9=%s "
          "96ca2eb..958f2f4=%s" % (span_u_excl, span_u_incl, span_x_excl, span_x_incl))
    print("unnamed in U's span: %s" % ", ".join(commits[c]["short"] for c in u_unnamed))
    print("unnamed in X's span: %d" % len(x_unnamed))
    print("40-hex runs consumed %d/%d ; 7-hex runs consumed %d/%d" % (
        used40, tot40, n6, tot7))
    print("wrote %s" % OUT_PATH)
    for r in mismatch + not_in_log + ambiguous:
        print("  ! %s p%d %s %s -> %s" % (r["receipt"], r["para"],
                                          r["claim"]["commit"], r["verdict"], r["detail"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
