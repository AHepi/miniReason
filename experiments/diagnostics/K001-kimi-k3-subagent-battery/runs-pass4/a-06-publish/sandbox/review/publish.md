# Adversarial review: W0-PUBLISH (`src/minireason/loop/publish.py`)

Method: every claim below was executed against the sandbox copy, running real `git`
(/usr/bin/git) through the module's own `LocalGit` seam against real temporary bare
repositories (the §4.7 dry-run acceptance path, which the module docstring names as
load-bearing). Probe scripts live in `probe/`, share `probe/fixture.py`, and were run
with `python3 probe/<name>.py`; the last full re-run of all sixteen probes exited 0.
The sandbox contains no `tests/loop/test_publish.py` (the sandbox's `tests/loop/`
holds only `__init__.py`), so where a "test that would hold the repair" is named it
is a test to write in the real repository.

Line numbers refer to `src/minireason/loop/publish.py` in this snapshot.

---

## BLOCKER

### B1 — The history-rewrite guard passes every spell of `git add` that sweeps the whole tree, and the deletion refspec `:ref`

**Claim:** `_refuse_history_rewrite` (`publish.py:269–289`) refuses none of `add -A`,
`add --all`, `add -u`, `add .` (repo-root pathspec), nor `push origin :refs/heads/x`
—a ref *deletion*—through the published `LocalGit` seam.

**Where:** `publish.py:269–289` (the guard), `publish.py:222–239` (`_subcommand`,
which never treats `.`/`-A` specially), `publish.py:200–205` (`REWRITING_FLAGS`, no
`-A`/`--all` entry; only the `+`-prefixed forcing refspec at line 284–285 is caught,
never the empty-source refspec).

**Contradicted text, quoted:**

* Module docstring, `publish.py:74–76`: *"Never: ``-A``, ``--force``, ``--amend``,
  ``rebase``, ``reset``, a ``+``-prefixed push refspec, **any ref deletion**, or any
  other git invocation this module does not itself need. ``_refuse_history_rewrite``
  inspects the argv before a process is spawned, so the refusal holds **for every
  caller of ``LocalGit``**, not only for this module's own code paths."*
* Deviation 6, `publish.py:58–69`: *"The argv guard is an allow-list … the guard now
  refuses everything this module does not itself emit."*
* `ALLOWED_SUBCOMMANDS` comment, `publish.py:145–152`: *"A test asserts that every
  argv ``publish``, ``verify_published`` and ``check_published`` actually emit is on
  this list, so the list cannot be wider than the module's own need."* The list is
  indeed minimal, but the guard polices only the subcommand name and the listed
  flags — never the *arguments* to an allowed subcommand.

`W0-PUBLISH`'s wave-plan acceptance names "explicit paths only, never -A". The module
never emits `-A` itself (probe `p7` re-derived publish()'s argv and the guard passes
its own argv), but the module's *own stated guarantee* for the seam is that the guard
refuses these spellings "for every caller of LocalGit", and it does not.

**Probe executed:** `python3 probe/p4_argv_guard.py`.

```
ALLOWED: git add -A (exit 0 )
ALLOWED: git add --all . (exit 0 )
ALLOWED: git add -u (exit 0 )
ALLOWED: git add . (exit 0 )
ALLOWED: git commit -a -m sweep everything (exit 1 )
refused HISTORY_REWRITE_REFUSED: git push --force origin HEAD:refs/heads/work
refused HISTORY_REWRITE_REFUSED: git push -f origin HEAD:refs/heads/work
refused HISTORY_REWRITE_REFUSED: git push --force-with-lease origin HEAD:refs/heads/work
refused HISTORY_REWRITE_REFUSED: git push -d origin work
refused HISTORY_REWRITE_REFUSED: git push --delete origin work
refused HISTORY_REWRITE_REFUSED: git push --mirror origin
refused HISTORY_REWRITE_REFUSED: git push --prune origin
refused HISTORY_REWRITE_REFUSED: git push origin +HEAD:refs/heads/work
ALLOWED: git push origin :refs/heads/work (exit 0 )
refused HISTORY_REWRITE_REFUSED: git commit --amend -m x
refused HISTORY_REWRITE_REFUSED: git rebase origin/work
refused HISTORY_REWRITE_REFUSED: git reset --hard HEAD~1
refused HISTORY_REWRITE_REFUSED: git reset HEAD~1
refused HISTORY_REWRITE_REFUSED: git update-ref -d refs/heads/work
refused HISTORY_REWRITE_REFUSED: git branch -D work
refused GIT_SUBCOMMAND_NOT_ALLOWED: git checkout --orphan tmp
refused GIT_SUBCOMMAND_NOT_ALLOWED: git symbolic-ref HEAD refs/heads/other
refused GIT_SUBCOMMAND_NOT_ALLOWED: git clean -fd
refused GIT_SUBCOMMAND_NOT_ALLOWED: git stash drop

remote refs/heads/work before: True
deletion push exit code: 0
remote refs/heads/work after: ''
'add -A' staged via LocalGit: ['outside.txt', 'run/in.txt']
```

The deletion push really deleted the remote branch (`ls-remote` returns empty
afterwards), and `add -A` staged a file *outside* the published path.

**Repair.** In `_refuse_history_rewrite`, for subcommand `push` refuse any refspec
token containing `":" `whose left side is empty (`token.startswith(":")`), matching
the existing `+` check at `publish.py:284–285`; and for subcommand `add` refuse the
tokens `-A`, `--all`, `-u`, `--update`, and any non-`--` pathspec that resolves to the
repo root (this module only ever emits `add -- <explicit names>`, so the narrowest
correct fix is: for `add`, require `--` and permit nothing before it). A test drives
each of the spellings above through `LocalGit.status` on a temp repo and asserts
`HistoryRewriteRefused`, and asserts a live remote branch survives the `:ref` attack.

### B2 — A transport failure during the post-push read-back raises `GIT_OPERATION_FAILED` instead of returning `PublishPending(REMOTE_NOT_CONFIRMED)`

**Claim:** If the push succeeds and the network then blips at `ls-remote`, `publish()`
raises `GitCommandFailed` (code `GIT_OPERATION_FAILED`) out of `_read_back`, although
the module's own outcome model reserves `REMOTE_NOT_CONFIRMED` in `PENDING_REASONS`
and promises pendings — never unclassified raises — for "a publication that did not
complete".

**Where:** `publish.py:432–442` (`_read_back` calls `git.text("ls-remote", …)` and
`git.run("fetch", …)` through `LocalGit.run`, which *raises* `GitCommandFailed` at
`publish.py:338–343`), reached unguarded from `publish()` at `publish.py:560`.
Contrast `publish.py:454–476`: `verify_published` and `check_published` both wrap the
same primaries in `except GitCommandFailed: return False` — only `publish()` does not.

**Contradicted text, quoted:**

* Module docstring, `publish.py:13–14`: *"a timed-out push leaves publication
  *pending* (``PublishPending``), which the driver treats as blocking every successor
  step"*.
* Deviation 2, `publish.py:51–56`: *"the wave plan's public interface names one
  outcome type, and the driver's handling — re-fetch, re-attempt as a new step, never
  force — is identical for every pending reason."*
* `publish()` docstring, `publish.py:491–496`: *"Returns a ``PublishResult``. … a
  ``PENDING`` result carries a ``PublishPending`` naming why, and blocks every
  successor step."*
* `PENDING_REASONS` comment, `publish.py:126–129`: *"Every reason a publication can
  be left pending."* — `REMOTE_NOT_CONFIRMED` is in the tuple, but no push-transport
  failure at read-back time can ever produce it: that path is only reachable on a
  *mismatch*, never on a *failure*.

The practical consequence: `GIT_OPERATION_FAILED` here is in a real sense
misclassified — the push already landed on the remote (probe shows the remote tip
equals local HEAD). The driver flow (O7: "a `PublishPending` result must block every
successor step until a later attempt returns `PUBLISHED`") has a receipt shape for
this; a bare raise carries none of `local_commit`, `attempt`, or `ref`.

**Probe executed:** `python3 probe/p8_readback_raise.py` (a `LocalGit` subclass that
runs the push for real and returns exit-128 "connection reset" for every later
`ls-remote`/`fetch`).

```
RAISED GitCommandFailed code: GIT_OPERATION_FAILED
detail: git ls-remote --refs exit 128: fatal: connection reset by peer
remote tip after the call: f43c63171162
push had already landed: True
```

**Repair.** In `_read_back`, catch `GitCommandFailed` around the `ls-remote`,
`fetch`, and `rev-parse` primaries and return
`_ReadBack(False, None, None, REMOTE_NOT_CONFIRMED, "PUBLISH_REF_CHANGED " +
failed.summary())` — the pending reason that already exists and is already a member
of `types.FAILURE_CODES`. A test injects a `LocalGit` that pushes successfully then
fails `ls-remote`, and asserts `publish()` returns
`PublishResult(status=PENDING, pending.reason=REMOTE_NOT_CONFIRMED)`.

---

## SHOULD-FIX

### S1 — The credential scan never scans the commit message, which is published bytes

**Where:** `publish.py:516–523` (the two `_refuse_credentials`/`_refuse_credential_text`
calls cover the working-tree bytes and the staged diff) versus `publish.py:524–527`
(`resolved.run("commit", "-m", str(message), ...)` — the message reaches the commit
unscanned).

**Contradicted text, quoted:** module docstring, `publish.py:6–9`: *"One publisher,
one discipline: stage the *named* paths only, **scan the bytes for any credential
this process can see**, commit with the supplied message, …"*. The byte surfaces the
publisher publishes are the staged files *and the commit object it authors*; nothing
in the docstring scopes the scan to files only, and the refusal list in
`CredentialInStagedDiff` ("a credential this process can see appears **in the bytes
to be published**", `publish.py:171–175`) covers anything the step publishes.

**Probe executed:** `python3 probe/p13_scan_coverage.py`, case D:

```
D: publish with credential in the commit MESSAGE: PUBLISHED
   remote commit message carries the credential: True
```

**Repair.** Run `_refuse_credential_text(str(message), "commit message")` beside the
`PUBLISH_MESSAGE_EMPTY` check. Test: a message containing a registered secret env
value raises `CredentialInStagedDiff` naming the env *name* only.

### S2 — `check_published`'s path branch can pass on bytes that were never committed

**Where:** `publish.py:632–644`: the path branch compares `resolved.run("show",
remote_commit + ":" + name)` against the **working tree** and never against the
published commit. A caller with a dirty tree (file rewritten by hand to the published
bytes after an unpushed local commit) passes the gate although the repository's
committed content under that path differs from the remote.

**Contradicted text, quoted:** `check_published` docstring, `publish.py:606–612`:
*"A path (absolute or repo-relative, file or directory) answers 'are the
working-tree bytes under it exactly the bytes on the published ref' — runner v2's
``INPUT_NOT_PUBLISHED`` comparison, as a predicate."* — the *comparison* it
implements, but as a **publication-before-dispatch** predicate (the interface's own
name for it, WAVE0-INTERFACE §6) the gate answers True for content that the commit
graph has never carried: the "published bytes" it certifies are the working tree's
current bytes, with no requirement that they be committed anywhere.

**Probe executed:** `python3 probe/p15_check_uncommitted.py`:

```
git status --porcelain run: 'M run/a.txt'
a.txt committed at HEAD: v2, committed locally, never pushed
a.txt on the remote    : published v1
check_published('run'): True
-> True means: the gate passed although HEAD under 'run' differs
   from what is published (its own commit is unpushed).
```

**Repair.** Either document the predicate explicitly as byte-shaped
("certifies the bytes on disk, whatever HEAD says") and route the driver's dispatch
gate through the sha branch, or additionally require `git status --porcelain -- <paths>`
to be clean (`diff --quiet HEAD -- <paths>`) before answering True. A test commits an
unpushed change, restores the working tree to the published bytes, and asserts the
repaired gate answers False (or the docstring names the byte-level scope).

### S3 — The scan is byte-naive: a credential split by one invalid UTF-8 byte, or rendered in UTF-16, passes

**Where:** `publish.py:397–404` — `(repo / name).read_bytes().decode("utf-8",
"replace")` — and the staged-diff scan decodes the same way.

**Contradicted/limited text, quoted:** *"scan the bytes for any credential this
process can see"* (docstring, above). To its credit, O8 in `WAVE0-INTERFACE.md`
already scopes the honest claim: *"the closing record should state that the scan
covers the credentials this process could see — not a proof that no credential is
present"*; and `provider_openai_compat._renderings` deliberately covers only the raw
and JSON-escaped forms. But the module's own docstring still states the guarantee in
byte terms while the implementation is a lossy text decode, so the boundary belongs
here as a recorded limitation, not in the docstring as a blanket promise.

**Probe executed:** `python3 probe/p10_scan_encodings.py`:

```
invalid-utf8 wrapper -> refused SECRET_IN_STAGED_DIFF | detail: run/blob.bin: PROBE_CRED
   secret in detail: False
split by invalid byte -> PUBLISHED (scan did not see it)
utf-16-le encoding -> PUBLISHED (scan did not see it)
rot13 rendering -> PUBLISHED (scan did not see it)
```

(A credential with pure-ASCII bytes survives `decode(..., "replace")` intact — so
the wrapper case is refused correctly; only a *split* or *re-encoded* credential
escapes.)

**Repair.** Document the scan as an ASCII/UTF-8-substring scan in the docstring
(one sentence), or scan the raw bytes with `value.encode()` in addition to the
decoded text. Test: a file containing `secret[:6] + b"\xff" + secret[6:]` is either
refused after the repair or pinned as out of scope by an explicitly-tested sentence.

---

## NOTE

### N1 — A `LocalGit(env=...)` credential is stripped from the child only if it is a *registered* name

`publish.py:320–326`: `environment()` pops only `_credential_env_names()` — registry
`key_env` values plus `register_secret_envs` names. An ad-hoc `env` dict passed to
`LocalGit(repo, env={...})` whose keys were never registered is forwarded verbatim.
The seam is caller-supplied and the docstring says "with every **known** credential
removed", so this is a documented bound, not a hole — but later waves using the seam
should know the child's environment is only as clean as the registry. Probe
`p13_scan_coverage.py` case A printed `SECRET_VALUE in env … True (not a registry
name -> kept)`.

### N2 — The `REMOTE_NOT_CONFIRMED` wording conflates "ref changed" with "ref absent"

`_read_back` (`publish.py:432–437`) returns `REMOTE_NOT_CONFIRMED`/`PUBLISH_REF_CHANGED`
both when `ls-remote` returns nothing (ref absent — the plausible state after a
connector deleted the branch, which B1 shows is reachable) and when the commit id differs.
`PUBLISH_REF_UNRESOLVED` exists as a code but is used only by `upstream_ref`. Cosmetic;
the driver handling is identical per deviation 2.

### N3 — Suspected, could not reproduce: `verify_published` reading the index for its expected side

I suspected `_read_back`'s expected side (`_tracked_files` = `ls-files --cached`,
`publish.py:386–391`) could make `verify_published` answer False for a genuinely
published commit whose tree the remote still carries, when the local index has moved
on. Probe `p9_index_vs_commit.py` executed this: roll the remote ref back to v1 while
the local index holds v2 under the same path — `verify_published(v1)` answered
**True**, because `_tree_blobs(source)` reads the *commit's* tree objects, and the
index only supplies the path list. Verified: `index (ls-files --cached) content for
run/a.txt: v2` / `verify_published(v1): True`. Not a defect in this sandbox.

The residual corner — an expected path absent from `commit`'s tree silently dropping
out of both blob maps — could not be reached here either, because `verify_published`
computes `files` from `commit`'s own tree-relative paths (`ls-files --cached`
constrained by the caller's paths); I could not construct an input where a published
path is missing from its own commit. Unresolved at zero findings; recorded per the
house rules.

---

## Tried, and could not break

* **Forcing past a rejected push.** After the remote advanced, `publish()` returned
  `PublishPending(PUSH_REJECTED)` with no retry and no forced flag anywhere in argv
  (probe `p3`, second half: `divergent remote -> status: PENDING / pending reason:
  PUSH_REJECTED`, and the probe's sleep list stayed empty — a rejection takes zero
  backoff sleeps, as documented). Resubmission after the driver's fetch+merge
  succeeded on attempt 2 exactly as deviation 2 describes.
* **Hook refusals misclassifying as transport.** A real `pre-receive` hook refusal
  (`[remote rejected]`) classifies `PUSH_REJECTED`, not `PUSH_TRANSPORT` (probe
  `p16`: `hook refusal -> PENDING PUSH_REJECTED`); a nonexistent remote classifies
  `PUSH_TRANSPORT` with exactly the four recorded backoff sleeps `[2.0, 4.0, 8.0,
  16.0]` and `PublishNotConverging` on attempt 3 (probe `p5`).
* **Ref/path parsing attacks.** `split_publish_ref` refused every malformed spelling
  offered (`""`, `origin`, `/leading`, `trailing/`, spaces, `..`, `?`, `//`, `.`),
  and `_explicit_paths` refused `-A`, `--all`, `:`-magic, glob magic, the repo root
  (`.` *and* the absolute spelling), `..`-escapes, and absent paths, with duplicates
  collapsed (probe `p14`). `PATH_OUTSIDE_REPO`/`PATH_IS_REPO_ROOT`/`PATH_MISSING` all
  fire before any index mutation.
* **Credential refusal soundness on the honest path.** A planted credential in an
  *unstaged* file under the published path refused with `SECRET_IN_STAGED_DIFF`,
  detail carrying the env *name* only (`secret value in detail: False`), the index
  left byte-clean before and after (`staged after publish(): ''`), and the child
  environment scrubbed (`PROBE_CRED in child env: False`) — probe `p1`.
* **Working-tree-vs-commit confusion (deviation 7).** After a post-publish local
  edit, `verify_published` still answers True (committed trees compared) while
  `check_published` answers False (bytes compared) — probe `p6`; both answers are
  the docstrings' own semantics.
* **Connector equal-tree acceptance.** A re-authored remote commit over an equal
  tree, after the driver's fetch+merge, yields `PUBLISHED` with both ids on the
  VERIFIED line — probe `p12`.
* **Exhaustion-token hygiene.** `as_receipt()` and the VERIFIED line carry no
  occurrence of the token `exhaustion` (probe `p16`).
* **`publish()`'s own argv passes its own guard.** All 16 argv shapes the module
  emits pass `_refuse_history_rewrite`, and an empty argv is refused (probe `p4`),
  consistent with the allow-list comment at `publish.py:145–152`.

---

## Summary of locations

| id | file:lines | kind |
|---|---|---|
| B1 | `publish.py:269–289`, `200–205` | guard does not fire: `add -A/-u/--all`, root pathspec, `:ref` deletion |
| B2 | `publish.py:432–442`, reached at `560` | read-back transport failure raises instead of pending |
| S1 | `publish.py:516–523` vs `524–527` | commit message unscanned for credentials |
| S2 | `publish.py:632–644` | `check_published` path branch ignores uncommitted divergence |
| S3 | `publish.py:397–404` | byte-naive decode; split/non-UTF-8 credentials pass |
| N1 | `publish.py:320–326` | env scrubbing limited to registered names |
| N2 | `publish.py:432–437` | `REMOTE_NOT_CONFIRMED` conflates absent ref with changed ref |
| N3 | — | suspected, could not reproduce |

Probes: `probe/fixture.py`, `probe/util_codes.py`, `probe/p1_credential_refusal.py`,
`probe/p2_untracked_no_upstream.py`, `probe/p3_happy_and_diverged.py`,
`probe/p4_argv_guard.py`, `probe/p5_push_failures.py`, `probe/p6_check_published.py`,
`probe/p7_verify_semantics.py`, `probe/p8_readback_raise.py`,
`probe/p9_index_vs_commit.py`, `probe/p10_scan_encodings.py`, `probe/p11_leftovers.py`,
`probe/p12_connector_equal_tree.py`, `probe/p14_refs_and_paths.py`,
`probe/p15_check_uncommitted.py`, `probe/p16_rejection_markers.py`. Last full re-run:
all sixteen probe scripts, exit 0 (invoked via a `python3 -c` driver over
`subprocess.run`, one process per probe).
