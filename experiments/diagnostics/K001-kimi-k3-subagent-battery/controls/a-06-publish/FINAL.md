# Adversarial review — `src/minireason/loop/publish.py` (W0-PUBLISH)

Sandbox: a frozen snapshot of the staging clone. Read in this order:
`notes/WAVE0-INTERFACE.md`, `src/minireason/loop/publish.py`,
`design/design-s2-roles-and-guard.md`, `design/design-s7-wave-plan.md`,
`src/minireason/loop/__init__.py`, `src/minireason/loop/types.py`,
`src/minireason/provider_openai_compat.py`, `AGENTS.md`,
`docs/lessons/operations.md`.

Every finding below was executed. Probes live in `probe/` and are run with
`python3 probe/<name>.py` from the sandbox root; each one builds a real checkout
with a real bare remote in a temp directory and drives the module's production
path, which is what design §4.7 asks of this module ("every git operation runs
against a real bare repo in a temp dir through the same `publish()` path, so
`VERIFIED` is genuinely exercised rather than stubbed"). `probe/_lab.py` is the
shared scaffolding; `probe/p00_happy_path.py` establishes that the scaffolding
reaches the real code, so a later probe's result is the module's and not the
lab's.

Nothing under `src/` was edited. The sections below are **BLOCKER**,
**SHOULD-FIX** and **NOTE** as the task's ordering requires; that ordering is a
kind, not a rank, and no finding is scored against another.

Where a probe needs a credential, it uses the synthetic string
`PROBE-FAKE-CREDENTIAL-0123456789`, invented for the probe and registered
through `provider_openai_compat.register_secret_envs`. No real credential is
read, written or printed by anything here.

---

## BLOCKER

### B1. A bracketed path name reaches git as a pathspec glob, and publishes a file the caller never named and the credential scan never read

**Claim.** `_explicit_paths` refuses `*` and `?` but not `[` or `]`. Git's
pathspec matcher is wildmatch, in which `[ab]` is a character class, so an
explicit, existing, caller-named path can match *other* files. Those files are
staged, committed and pushed; the working-tree credential scan never reads them,
and the staged-diff scan cannot see inside them when git calls them binary.

**Where.** `src/minireason/loop/publish.py:507-535`, specifically the
metacharacter test at line 518. The consequences land at lines 803 (scan),
808 (`add`), 813 (`_tracked_files`) and 818 (`commit`), all of which pass the
same unescaped name to git as a pathspec.

**What it contradicts.**

`_explicit_paths`' own docstring, `publish.py:508-512`:

> Repo-relative POSIX names for the caller's explicit paths.
>
> Refuses pathspec magic, the repo root, anything outside the repo and
> anything absent. There is therefore no spelling of ``paths`` that reaches
> git as ``-A``, ``--all`` or a bare ``.``.

The module docstring, `publish.py:4-5`:

> stage the *named* paths only, scan the bytes for any credential this process
> can see

`design/design-s7-wave-plan.md:16`, W0-PUBLISH's `purpose` and `acceptance`:

> "purpose":"Explicit-path add, credential scan, commit, non-forcing push,
> remote and per-path byte verification, the VERIFIED line; LocalGit double over
> a real bare repo."
>
> "acceptance":"Against a temp bare repo: explicit paths only, never -A; …"

`AGENTS.md:17`:

> Stage explicit reviewed paths, scan for credentials, run relevant
> verification, commit and push normally to `main`, and verify the remote commit
> and tree.

**Probe 1 — `python3 probe/p01_bracket_pathspec.py`**, verbatim:

```
_explicit_paths accepted : ('report[1].md',)
status                   : PUBLISHED
result.paths (named)     : ('report[1].md',)
result.files (published) : ('report1.md', 'report[1].md')
VERIFIED line            : VERIFIED 87dfb014e899b40964bae0de1e9aa0d79e4ea525 TREE 7e42bf3db6f99f2e7d1a616b398ade1a8f4af02d at 2026-09-14T11:21:27Z local=87dfb014e899b40964bae0de1e9aa0d79e4ea525 remote=87dfb014e899b40964bae0de1e9aa0d79e4ea525 ref=origin/main paths=1
remote tree contents     : ['README.md', 'report1.md', 'report[1].md']
named file published?    : True
unnamed file published?  : True
bytes of what landed     : b'THE UNNAMED NEIGHBOUR\n'
```

One path was named. Two files were published. The VERIFIED line says `paths=1`.

**Probe 2 — `python3 probe/p02_bracket_defeats_credential_scan.py`**, verbatim:

```
registered secret env NAMES : ('PROBE_FAKE_KEY_ENV',)
scan 1 walked              : ('report[1].md',)
publish status             : PUBLISHED
publish files              : ('report1.md', 'report[1].md')
remote blob is binary      : True
remote blob carries value  : True
remote blob length         : 41
--- the whole text scan 2 reads ---
diff --git a/report1.md b/report1.md
new file mode 100644
index 0000000..5b0d1c4
Binary files /dev/null and b/report1.md differ
diff --git a/report[1].md b/report[1].md
new file mode 100644
index 0000000..0fbf996
--- /dev/null
+++ b/report[1].md
@@ -0,0 +1 @@
+the named file, clean

--- end ---
scan 2 finds the value      : False
scan 2 hit names            : []
```

Two scans stand between a byte and the remote. `_refuse_credentials`
(`publish.py:575-577`) walks the *named* paths in the working tree through
`_walk_files`, which resolves `repo/"report[1].md"` literally and never sees the
neighbour — line 1 of the output. `_refuse_credential_text` over
`git diff --cached` (`publish.py:809-811`) *does* receive the neighbour, because
the same glob is passed to `diff`, but git renders a file with a NUL byte as
`Binary files … differ` and prints none of its content. The publication
completed and the remote carries the planted value.

**Reachability, stated plainly.** Within the loop's own run tree this is not
reachable today: `types.RunPaths.reading_dir` folds every character outside
`[A-Za-z0-9_.-]` to `_` (`types.py:1333-1336`, `_SLUG_UNSAFE = re.compile(r"[^A-Za-z0-9_.-]")`),
and `run_paths` puts `run_id` through `_identifier`. The exposure is on any
*caller-supplied* path, which is exactly what `paths` is declared to be and
exactly what `PATH_NOT_EXPLICIT` exists to make safe — and AGENTS.md:9 requires
this seam to publish "every completed document" by "its explicit path",
including reviews, reports and errata whose names no wave-0 module folds.

**Repair.** Two changes, either of which closes it, and both are cheap:

1. Make every pathspec literal. Add `--literal-pathspecs` to the argv
   `LocalGit._invoke` builds (`publish.py:433`), or prefix each name with
   `:(literal)` at the point of use. `_subcommand` already skips leading-dash
   global options (`publish.py:361-375`), so the guard is unaffected.
2. Widen the refusal at `publish.py:518` to the rest of the wildmatch
   metacharacters — `[`, `]`, `\` — so a name git would read as a pattern is
   `PATH_NOT_EXPLICIT` rather than a pattern.

Independently, derive the credential-scan set from what git will actually stage
rather than from `Path.rglob`: run `_tracked_files` (or `git add --dry-run`)
first and scan those names, so the set that is scanned and the set that is
committed are the same set by construction.

**Test that would hold the repair.** In a repo containing both `report[1].md`
and `report1.md`, assert `publish(repo, ["report[1].md"], …).files ==
("report[1].md",)` and that `report1.md` is absent from the remote tree; and a
second test asserting `set(_walk_files(repo, names)) == set(_tracked_files(git, names))`
after the add, for a fixture whose names contain `[`, `]` and `\`.

---

### B2. The history-rewrite guard matches flags by exact token, so a force push gets through and rewrites a published ref

**Claim.** `_refuse_history_rewrite` tests `token in REWRITING_FLAGS` — exact
string equality. Git accepts an `=`-valued spelling of a long option and an
unambiguous abbreviation of one, neither of which is that exact string. The
guard therefore admits `push --force-with-lease=<ref>:<sha>` and
`commit --amen`. It also admits `add -A` and `commit -a`, which no flag in the
set names at all.

**Where.** `src/minireason/loop/publish.py:378-401` (the guard), with the set at
`publish.py:206-209`.

**What it contradicts.**

The module docstring, `publish.py:90-94`:

> Never: ``-A``, ``--force``, ``--amend``, ``rebase``, ``reset``, a ``+``-prefixed
> push refspec, any ref deletion, or any other git invocation this module does not
> itself need. :func:`_refuse_history_rewrite` inspects the argv before a process
> is spawned, so the refusal holds for every caller of :class:`LocalGit`, not only
> for this module's own code paths.

The comment over the set, `publish.py:201`:

> Refused wherever they appear in an argv.

Deviation 6, `publish.py:72-80`:

> **The argv guard is an allow-list** (:data:`ALLOWED_SUBCOMMANDS`), not a list
> of forbidden spellings. … Its failure mode is the entry nobody thought of, and
> :class:`LocalGit` is the seam every later wave uses, so the guard now refuses
> everything this module does not itself emit.

`design/design-s7-wave-plan.md:16`: `"acceptance":"… push is non-forcing; …"`.
`AGENTS.md:17`: "No force push or rewriting history."

**Probe — `python3 probe/p03_guard_argv_escapes.py`**, verbatim:

```
========================================================================
A. push --force-with-lease=<ref>:<sha> is admitted and rewrites the ref
========================================================================
remote main after honest push : e0d662a84dd21f6b4291e8609463bbfff23e61f2
local rival commit            : a3de68110041815ef6935047aed8c7edc58c843f
rival descends from published : False
honest push ok                : False | classify: PUSH_REJECTED
GUARD DID NOT FIRE            : exit 0
push output                   : To /tmp/w0publish-force-lease-hrsqrj28/remote.git
 + e0d662a...a3de681 HEAD -> main (forced update)
remote main afterwards        : a3de68110041815ef6935047aed8c7edc58c843f
remote ref now the rival      : True
published commit still on ref : False
========================================================================
B. commit --amen (unambiguous abbreviation of --amend) is admitted
========================================================================
GUARD DID NOT FIRE            : exit 0
HEAD before                   : 16f56606bb9ab12f6402f9b30db337afa9533bb4
HEAD after                    : 196fc5b829e328bd58f3cd427c6c40e1f025cd83
seed commit rewritten         : True
b.md folded into the amended commit : True
========================================================================
C. add -A and commit -a are admitted
========================================================================
GUARD DID NOT FIRE on add -A  : staged ['private/notes.md', 'wanted.md']
GUARD DID NOT FIRE, committed : ['private/notes.md', 'wanted.md']
========================================================================
D. for contrast: the spellings the guard does catch
========================================================================
git push --force origin main                      -> HISTORY_REWRITE_REFUSED
git commit --amend -m x                           -> HISTORY_REWRITE_REFUSED
git reset --hard                                  -> HISTORY_REWRITE_REFUSED
git push origin +refs/heads/main:refs/heads/main  -> HISTORY_REWRITE_REFUSED
git push -f origin main                           -> HISTORY_REWRITE_REFUSED
git update-ref refs/heads/main HEAD               -> GIT_SUBCOMMAND_NOT_ALLOWED
git checkout --orphan x                           -> GIT_SUBCOMMAND_NOT_ALLOWED
```

Section A is a real forced update through `LocalGit`: git itself says
`(forced update)`, the previously published commit is no longer on the remote
ref, and the ref now carries a commit that is not its descendant. Section D
shows the guard is not inert — it catches every spelling anybody wrote down.

**Repair.** Compare on the option *name*, not the token, and account for git's
prefix abbreviation:

* split each token at the first `=` and test the left half against
  `REWRITING_FLAGS`;
* for a long option, also refuse any token that is a proper prefix of a member
  of `REWRITING_FLAGS` (`--amen`, `--forc`, `--del`), since git resolves an
  unambiguous prefix to the full option;
* add the stage-everything spellings the docstring's "Never:" list already
  names — `-A`, `--all`, `--no-ignore-removal` for `add`, and `-a`/`--all` for
  `commit`.

The durable form of the same repair is the one deviation 6 already argues for
but stops one level short of: hold an allow-list of the *argv shapes* this
module emits (subcommand plus its permitted option set), not just of
subcommands. `probe/p08_argv_env_and_imports.py` prints the complete emitted set
— eleven subcommands over the 34 argvs that one `publish`, one
`verify_published` and three `check_published` calls emit, the count and the
list both printed by that command — so the list is available without guessing.

**Test that would hold the repair.** A parametrised case over
`push --force-with-lease=refs/heads/main:<sha>`, `push --force-with-lease`,
`push --forc`, `commit --amen`, `commit --amend=`, `add -A`, `add --all`,
`commit -a`, each asserting `HistoryRewriteRefused` (or
`GitSubcommandNotAllowed`) *and* that the bare remote's `refs/heads/main` is
byte-identical before and after the call.

---

## SHOULD-FIX

### S1. A read-back that cannot run raises out of `publish()` instead of returning a pending publication, after the push has landed

**Claim.** `REMOTE_NOT_CONFIRMED` is a published member of `PENDING_REASONS`,
but it is reachable only when `ls-remote` and `fetch` *succeed and disagree*.
When either command fails or hits the 90 s git wall clock, `LocalGit.run`/`.text`
raise `GitCommandFailed` straight out of `publish()` — with the commit made, the
push already on the remote, no `PublishResult`, no recorded commit identity and
no attempt number for the driver to carry.

**Where.** `src/minireason/loop/publish.py:732`, `:736-738` (unguarded `git.text`
/ `git.run` inside `_read_back`); the `try` at `:742-747` covers only
`_tree_blobs`. Reached from `publish.py:831`.

**What it contradicts.** `publish()`'s docstring, `publish.py:782-784`:

> Returns a :class:`PublishResult`. ``result.published`` is the only state
> that may precede a dispatch; a ``PENDING`` result carries a
> :class:`PublishPending` naming why, and blocks every successor step.

`PENDING_REASONS`' comment, `publish.py:160-161`:

> Every reason a publication can be left pending.

The module docstring's §4.4 paragraph, `publish.py:23-25`:

> **§4.4 Failure handling** — a timed-out push leaves publication *pending*
> (:class:`PublishPending`), which the driver treats as blocking every
> successor step, and the 90 s git wall clock.

And `docs/lessons/operations.md:11` (OPS-008), which is precisely about this
state: "an uploaded tree checkpoint, a local commit and a published branch are
distinct states."

**Probe — `python3 probe/p07_readback_failure.py`**, verbatim:

```
PENDING_REASONS : ('PUSH_REJECTED', 'PUSH_TIMEOUT', 'PUSH_TRANSPORT', 'REMOTE_NOT_CONFIRMED', 'PATH_NOT_PUBLISHED')

ls-remote timeout   -> raised GitCommandFailed GIT_OPERATION_FAILED
    detail            : git ls-remote --refs timed out:
    local HEAD         : 0531b2419c7e2e6b278a170d8fd5c10ba8ae291c
    remote refs/heads/main: 0531b2419c7e2e6b278a170d8fd5c10ba8ae291c
    the push DID land   : True
ls-remote transport -> raised GitCommandFailed GIT_OPERATION_FAILED
    detail            : git ls-remote --refs exit 128: fatal: unable to access remote: connection reset
    local HEAD         : 0531b2419c7e2e6b278a170d8fd5c10ba8ae291c
    remote refs/heads/main: 0531b2419c7e2e6b278a170d8fd5c10ba8ae291c
    the push DID land   : True
fetch timeout   -> raised GitCommandFailed GIT_OPERATION_FAILED
    detail            : git fetch --no-tags timed out:
    local HEAD         : 0531b2419c7e2e6b278a170d8fd5c10ba8ae291c
    remote refs/heads/main: 0531b2419c7e2e6b278a170d8fd5c10ba8ae291c
    the push DID land   : True
rev-parse transport -> raised GitCommandFailed GIT_OPERATION_FAILED
    detail            : git rev-parse FETCH_HEAD exit 128: fatal: unable to access remote: connection reset
    local HEAD         : 0531b2419c7e2e6b278a170d8fd5c10ba8ae291c
    remote refs/heads/main: 0531b2419c7e2e6b278a170d8fd5c10ba8ae291c
    the push DID land   : True
```

In all four the publication in fact succeeded — local HEAD and the bare remote's
`refs/heads/main` agree — and the caller is handed an exception instead of a
result.

**Repair.** Wrap `_read_back`'s own git calls the way `verify_published` already
wraps its call (`publish.py:877-880`): catch `GitCommandFailed` inside
`_read_back` and return
`_ReadBack(False, None, None, REMOTE_NOT_CONFIRMED, failed.detail)` so the
outcome is a `PublishPending` the driver's O7 attempt counter can carry. A
publication whose read-back could not run is unconfirmed, which is what that
reason word means; it is not a publication that failed.

**Test that would hold the repair.** The `BreakAfterPush` double in
`probe/p07_readback_failure.py` is the fixture: for each of `ls-remote`, `fetch`
and `rev-parse`, and for both `timed_out=True` and a non-zero exit, assert
`result.status == PENDING`, `result.pending.reason == REMOTE_NOT_CONFIRMED`,
`result.local_commit` is the local HEAD, and that a second call with
`attempt=3` raises `PublishNotConverging`.

---

### S2. A timed-out push is retried four more times inside the same call

**Claim.** `_push` breaks out early only for `PUSH_REJECTED`, so a timed-out
push is retried across the whole backoff ladder: five pushes and 30 s of sleep
per `publish()` call, and at the module's own 90 s git wall clock an upper bound
of 480 s inside one call.

**Where.** `src/minireason/loop/publish.py:689-698`, the condition at line 695.

**What it contradicts.** `design/design-s7-wave-plan.md:16`, W0-PUBLISH's
acceptance clause:

> a timed-out or rejected push returns PublishPending and is retried only as a
> new publish

and the module docstring, `publish.py:23-28`:

> **§4.4 Failure handling** — a timed-out push leaves publication *pending*
> (:class:`PublishPending`) … Network failure is retried on an exponential
> backoff (:data:`PUSH_BACKOFF_SECONDS`); a **rejected** push is never retried
> inside the call …

The docstring names two retry policies — network retried, rejection not — and
leaves the timeout, which the acceptance clause puts with the rejection.

**Probe — `python3 probe/p04_push_failure_paths.py`**, verbatim:

```
GIT_TIMEOUT_SECONDS = 90.0 | PUSH_BACKOFF_SECONDS = (2.0, 4.0, 8.0, 16.0) | MAX_PUBLISH_ATTEMPTS = 3
 rejected attempt=1: status=PENDING reason=PUSH_REJECTED; push invocations=1; sleeps=[] (total 0s); committed=True; verified_line=None
  timeout attempt=1: status=PENDING reason=PUSH_TIMEOUT; push invocations=5; sleeps=[2.0, 4.0, 8.0, 16.0] (total 30.0s); committed=True; verified_line=None
transport attempt=1: status=PENDING reason=PUSH_TRANSPORT; push invocations=5; sleeps=[2.0, 4.0, 8.0, 16.0] (total 30.0s); committed=True; verified_line=None

  timeout attempt=2: status=PENDING reason=PUSH_TIMEOUT; push invocations=5; sleeps=[2.0, 4.0, 8.0, 16.0] (total 30.0s); committed=True; verified_line=None
  timeout attempt=3: raised PublishNotConverging PUBLISH_NOT_CONVERGING; push invocations=5; sleeps=[2.0, 4.0, 8.0, 16.0] (total 30.0s)

worst-case wall clock inside ONE publish() call on a timing-out push:
    480.0 seconds = 8.0 minutes
```

The counts and the bound come from that command; `MAX_PUBLISH_ATTEMPTS`
behaviour in the last two lines is correct and is recorded here beside the
defect, not as a separate finding.

480 s is a resource boundary of the publish step, not a defect in itself — but
AGENTS.md:5 requires "a verified push to main at least every five minutes" and a
substantive receipt on the same clock, and one call that can occupy eight
minutes inside a single git subcommand makes that deadline unmeetable without
the operator being able to say why.

**Repair.** Add `PUSH_TIMEOUT` to the early return at `publish.py:695`
(`if reason in (PUSH_REJECTED, PUSH_TIMEOUT) or index == …`), so a timeout
returns pending on the first occurrence and the driver re-attempts it as a new
publish step, which is what the acceptance clause says. If the retry is wanted,
the docstring and the acceptance clause are the things to change, and the
worst-case wall clock belongs beside `GIT_TIMEOUT_SECONDS` where an operator
will read it.

**Test that would hold the repair.** The `ScriptedPush` double in
`probe/p04_push_failure_paths.py`: assert `git.pushes == 1` and `slept == []`
for `mode="timeout"`, unchanged `git.pushes == 5` for `mode="transport"`, and
`git.pushes == 1` for `mode="rejected"`.

---

### S3. Deviation 3's "refused with the index still clean" does not hold for two reachable inputs, and a commit that removes a credential can never be published

**Claim.** The working-tree scan runs before `git add`; the staged-diff scan
runs after it. Two ordinary inputs make the *second* scan the one that fires, so
the refusal lands with the caller's paths staged in a repository this module may
not `reset`. One of the two is the commit that removes an already-committed
credential, which this seam therefore cannot publish at all.

**Where.** `src/minireason/loop/publish.py:801-811` — the comment at 801-802,
the working-tree scan at 803, the add at 808, the staged-diff scan at 809-811.

**What it contradicts.** Deviation 3, `publish.py:58-62`:

> 3. **The credential scan runs over the working-tree bytes first and over the
>    staged diff second.** §4.5 names only the staged diff. Scanning first means
>    a planted credential is refused with the index still clean, because this
>    module may not ``reset`` (see :class:`HistoryRewriteRefused`) and must not
>    leave a credential staged behind a refusal.

and the same claim restated as a code comment at `publish.py:801-802`:

> Deviation 3: before the index is touched, so a refusal never leaves a
> credential staged in a repository this module may not reset.

**Probe — `python3 probe/p05_refusal_leaves_index_dirty.py`**, verbatim:

```
--- removal ---
staged before publish() : []
refused with            : SECRET_IN_STAGED_DIFF | staged diff: PROBE_FAKE_KEY_ENV
staged after refusal    : ['docs/leak.md']
index still clean?      : False

--- named ---
staged before publish() : []
refused with            : SECRET_IN_STAGED_DIFF | staged diff: PROBE_FAKE_KEY_ENV
staged after refusal    : ['docs/PROBE-FAKE-CREDENTIAL-0123456789.md']
index still clean?      : False

--- planted-in-working-tree ---
staged before publish() : []
refused with            : SECRET_IN_STAGED_DIFF | docs/planted.md: PROBE_FAKE_KEY_ENV
staged after refusal    : []
index still clean?      : True
```

`removal` is a file whose HEAD version carries the value and whose working-tree
version has it taken out: the deletion line `-<value>` is in the staged diff and
nowhere in the working tree. `named` is a file whose *name* carries the value:
the `diff --git a/<name>` header is in the staged diff and no file's content
carries it. The third block is the case deviation 3 is written about, and it
behaves exactly as written — which is why the first two are a gap and not a
misreading. (The refusal detail names the environment variable NAME only; the
value on the `staged after refusal` line is printed by the probe, from the
filename it created.)

The `removal` case is the operationally sharp one: the repair commit for a
leaked credential is refused by this seam every time it is attempted, and there
is no `redact`-and-continue path, by design — `src/minireason/loop/__init__.py:116-117`:
"a bearing record is **refused, not redacted**."

**Repair.** Two parts. (a) Scan the staged diff with the deletion side excluded
— compare against `git diff --cached --no-color --diff-filter=d` plus a scan of
the added lines only (`^\+`), so removing a credential is publishable while
adding one is not. (b) Scan the *names* of the paths, not only their contents,
before the add, so the `named` case is refused at `publish.py:803` where the
index is still clean. Both keep "refused, not redacted".

**Test that would hold the repair.** Three cases: a HEAD-resident credential
removed in the working tree publishes and the remote blob no longer carries it;
a path whose name carries a credential value is refused at the working-tree scan
with `lab.staged() == []`; a credential planted in a working-tree file is
refused with `lab.staged() == []` (already true, kept as the regression anchor).

---

### S4. The working-tree scan reads files git will never stage, so a publication is refused over bytes that are not in it

**Claim.** `_walk_files` walks the filesystem. It therefore reads ignored files
and, because its `.git` exclusion only looks at a path's *first* component, a
nested repository's own `.git/config` — which is where a credentialed remote URL
lives. A publication of a reviewed directory is then refused on account of bytes
git would never have published.

**Where.** `src/minireason/loop/publish.py:542-557`, specifically the exclusion
at line 553 (`if relative.split("/")[0] == ".git": continue`).

**What it contradicts.** `_walk_files`' docstring, `publish.py:543`:

> Every working-tree file under the explicit paths, ``.git`` excluded.

and `WAVE0-INTERFACE.md:445-451` (O8), which accepts the *cost* of the scan —
"Recommendation: accept the cost (it is the point)" — but on the ground that the
scan covers what is being published; it does not contemplate refusing a
publication over a file that is not.

**Probe — `python3 probe/p10_walk_scope.py`**, verbatim:

```
========================================================================
A. a nested .git below the top level is walked
========================================================================
_walk_files(['sub'])        : ('sub/.git/config', 'sub/note.md')
git add --dry-run -- sub    : ['add', "'sub/note.md'"]
publish(['sub'])            : SECRET_IN_STAGED_DIFF | sub/.git/config: PROBE_FAKE_KEY_ENV
========================================================================
B. the top-level .git is accepted as a path and skipped by the scan
========================================================================
_explicit_paths(['.git/config']) : ('.git/config',)
_walk_files(['.git/config'])     : ()
publish(['.git/config'])         : PUBLISH_PATHS_UNTRACKED | .git/config
```

and the ignored-file case, from **`python3 probe/p09_path_and_argument_refusals.py`**,
section E, verbatim:

```
========================================================================
E. an ignored file under a named directory
========================================================================
publish(['docs'])                              -> SECRET_IN_STAGED_DIFF  (docs/local.env: PROBE_FAKE_KEY_ENV)
what git would have staged              : ['add', "'docs/.gitignore'", 'add', "'docs/note.md'"]
```

Section B is the harmless half and is recorded beside it: `_explicit_paths`
accepts `.git/config` as a path, the scan skips it, and the publication is
refused at `PUBLISH_PATHS_UNTRACKED` rather than publishing a git config.

This refusal is in the safe direction, and a reader could reasonably call it
intended. It is here because its consequence is not conservative: the module
cannot `reset`, the refusal is sticky for as long as the untracked file is on
disk, and AGENTS.md:9 requires this seam to publish every completed document
immediately. A run whose `experiments/` tree contains an ignored scratch file
cannot publish the directory above it.

**Repair.** Derive the scan set from git, not from the filesystem: replace
`_walk_files` with `_tracked_files`-plus-`git add --dry-run` (or
`git ls-files -z --cached --others --exclude-standard -- <names>`), which is
also the repair B1 needs. Failing that, exclude any component named `.git`
rather than only the first, and skip files `git check-ignore` claims.

**Test that would hold the repair.** `publish(repo, ["docs"], …)` succeeds when
`docs/local.env` is git-ignored and carries a registered value, and the remote
tree does not contain `docs/local.env`; `publish(repo, ["sub"], …)` succeeds
when `sub/.git/config` carries one; and the planted-credential case in a
*tracked* file under `docs/` still refuses.

---

### S5. A path name that is not valid UTF-8 raises `UnicodeDecodeError` out of `publish()`, after the add

**Claim.** `_tracked_files` and `_staged_names` decode git's `-z` output with
`raw.decode("utf-8")` and no error handler. A filename that is not valid UTF-8 —
ordinary on Linux — raises `UnicodeDecodeError` out of `publish()`. It is not a
`LoopError`, so the package's single `except LoopError` does not catch it, and
it lands after `git add`, leaving the index staged.

**Where.** `src/minireason/loop/publish.py:564` (reached from `publish.py:813`);
the same pattern at `publish.py:587`.

**What it contradicts.** `src/minireason/loop/__init__.py:61-66`:

> **Every wave-0 exception is a** ``types.LoopError``, and keeps the base it
> already had … So ``except LoopError`` catches every refusal in the package

and `WAVE0-INTERFACE.md:370`: "Every wave-0 exception is a `types.LoopError` and
keeps its original base."

**Probe — `python3 probe/p15_non_utf8_path.py`**, verbatim:

```
path as python sees it : 'docs/caf\udce9.md'
_explicit_paths        : ('docs/caf\udce9.md',)
publish()              -> UnicodeDecodeError : 'utf-8' codec can't decode byte 0xe9 in position 8: invalid continuation byte
is it a LoopError?     : False
    publish.py:813  files = _tracked_files(resolved, names)
    publish.py:564  return tuple(sorted(entry for entry in raw.decode("utf-8").split("\0") if entry))
index left staged      : ['"docs/caf\\351.md"']
```

**Repair.** Decode with `os.fsdecode` (surrogateescape) in both helpers, which
round-trips back through `subprocess` unchanged, or refuse a non-decodable name
as `PATH_NOT_EXPLICIT` in `_explicit_paths` where the index is still clean.
Either way the failure becomes a named `LoopError`.

**Test that would hold the repair.** Create `docs/caf\xe9.md` by bytes and
assert that `publish()` either publishes it (and the remote tree carries the
same byte name) or raises a `LoopError` with `lab.staged() == []` — never a
`UnicodeDecodeError`.

---

## NOTE

### N1. `ALLOWED_SUBCOMMANDS` is wider than the module's need, which its own comment says it cannot be

`publish.py:187-189`:

> A test asserts that every argv ``publish``, ``verify_published`` and
> ``check_published`` actually emit is on this list, so the list cannot be wider
> than the module's own need.

The stated test bounds emitted ⊆ list, which does not bound list ⊆ emitted, and
the list is in fact wider. From **`python3 probe/p08_argv_env_and_imports.py`**,
section B:

```
subcommands emitted        : ['add', 'commit', 'diff', 'fetch', 'ls-files', 'ls-remote', 'ls-tree', 'merge-base', 'push', 'rev-parse', 'show']
ALLOWED_SUBCOMMANDS        : ['add', 'cat-file', 'commit', 'diff', 'fetch', 'ls-files', 'ls-remote', 'ls-tree', 'merge-base', 'push', 'rev-list', 'rev-parse', 'show', 'status']
allowed but never emitted  : ['cat-file', 'rev-list', 'status']
emitted but not allowed    : []
argvs emitted (count)     : 34
```

`cat-file`, `rev-list` and `status` are read-only and nothing turns on their
presence; the claim about the list is what is wrong. Repair: drop the three, and
add the reverse assertion (`ALLOWED_SUBCOMMANDS == set of emitted subcommands`)
that the comment describes.

### N2. A pending publication's `detail` never reaches the receipt, and `published_commit` on a pending receipt names a commit that is not ours

`as_receipt()` (`publish.py:637-652`) keeps `pending_reason` and drops
`pending.detail`, which is where the module puts the two runner-v2 codes its
compatibility paragraph names (`publish.py:35-38`: "`PUBLISH_REF_CHANGED`,
`INPUT_NOT_PUBLISHED`"). Neither is ever a `.code`; both are free text. From
**`python3 probe/p14_pending_receipt_detail.py`**, verbatim:

```
status          : PENDING
pending.reason  : REMOTE_NOT_CONFIRMED
pending.detail  : PUBLISH_REF_CHANGED
verified_line   : None
as_receipt()    :
    attempt           : 1
    committed         : True
    files             : ['docs/note.md']
    local_commit      : b5cf3f875a517f00a364e8842b02ebd9b31fd195
    paths             : ['docs/note.md']
    pending_reason    : REMOTE_NOT_CONFIRMED
    published_commit  : dc41f636e86a55dc8c8f258eca67511dfcba5548
    ref               : origin/main
    status            : PENDING
    tree              : 8d6c7f624598023b590e53d8cbf3de77d1a4b366
    verified_line     : None
detail in receipt?: False
```

Two things. `PUBLISH_REF_CHANGED` is in `types.FAILURE_CODES` (confirmed by
`python3 -c "from minireason.loop import types; print('PUBLISH_REF_CHANGED' in types.FAILURE_CODES)"`)
but no receipt can carry it, so `design/design-s2-roles-and-guard.md:108-110`'s "the block is logged with its
reason code" has no code to log below the grain of `REMOTE_NOT_CONFIRMED`. And
`published_commit` on this pending receipt is `dc41f63…`, which is the *other*
party's commit, not anything this step published. Repair: add `pending_detail`
to `as_receipt()`, and leave `published_commit` null unless the result is
`PUBLISHED`.

### N3. `_credential_env_names()` omits `_ALWAYS_SECRET_ENVS`; the divergence is latent today

`publish.py:345-358` builds the strip-list from the endpoint registry's
`key_env` values plus `registered_secret_envs()`. The transport's own
`_secret_env_names()` (`provider_openai_compat.py:152-168`) is that set **plus**
`_ALWAYS_SECRET_ENVS`. They agree today only because both members of
`_ALWAYS_SECRET_ENVS` happen to be endpoint `key_env` values. From
**`python3 probe/p08_argv_env_and_imports.py`**, section C:

```
transport declares          : ['DEEPSEEK_API_KEY', 'OLLAMA_API_KEY']
publish strips              : ('DEEPSEEK_API_KEY', 'OLLAMA_API_KEY')
names left in the child env : []

with no OLLAMA endpoint in the registry:
  transport declares        : ['DEEPSEEK_API_KEY', 'OLLAMA_API_KEY']
  publish strips            : ('DEEPSEEK_API_KEY',)
  still in the child env    : ['OLLAMA_API_KEY']
  and the scanner still flags it: ['OLLAMA_API_KEY']
```

`LocalGit.environment()`'s docstring says "The child environment, with every
known credential removed" (`publish.py:424`). Repair: call the transport's
`_secret_env_names()`, or add `_ALWAYS_SECRET_ENVS` to the union, so the set
that is stripped is the set that is scanned, by construction rather than by
coincidence. Nothing in this sandbox is currently exposed by it.

### N4. Three small behaviours worth writing down rather than fixing blind

From **`python3 probe/p09_path_and_argument_refusals.py`** and
**`python3 probe/p13_attacks_that_failed.py`**:

* A symlink is silently replaced by its target's repo-relative name:
  `_explicit_paths(['link.md']) (a symlink) -> ('docs/note.md',)`. The caller
  named one path and `result.paths` reports another; the symlink itself is never
  published. `.resolve()` at `publish.py:521` is doing it.
* A deletion cannot be published: `publish(['docs/note.md']) after unlink ->
  PATH_MISSING`, while the file is still in the index. `_explicit_paths` requires
  `exists()` (`publish.py:529`), so the removal of a published file has no route
  through this seam.
* The exact-token deny-list misfires harmlessly on ordinary content:
  `publish(message='--amend') -> HISTORY_REWRITE_REFUSED | git commit --amend`,
  because the commit message is a token in the argv the guard scans
  (`publish.py:391-393`, argv built at `publish.py:818`).

### N5. `notes/WAVE0-INTERFACE.md` §6 does not list three names the module publishes

`__all__` (`publish.py:109-140`) exports `ALLOWED_SUBCOMMANDS` and
`GitSubcommandNotAllowed`, and the module can raise
`GIT_SUBCOMMAND_NOT_ALLOWED`. `WAVE0-INTERFACE.md:316-345` lists neither
constant, nor the exception, nor the code. `types.FAILURE_CODES` *does* contain
`GIT_SUBCOMMAND_NOT_ALLOWED` (115 codes, from
`python3 -c "from minireason.loop import types; print(len(types.FAILURE_CODES), 'GIT_SUBCOMMAND_NOT_ALLOWED' in types.FAILURE_CODES)"`),
so the code table is reconciled and the integrator's record is the thing that is
behind. This is a defect in the note, not in the module; it is here because the
note is what a later wave reads first.

---

## Tried, and could not break

Each of these was an attempt to find a defect. Each failed, and the failure is
evidence about the module.

1. **Importing the module does not load the endpoint registry.** Deviation 8
   ("The transport is imported at the call", `publish.py:87-88`) and the N3
   comment at `publish.py:333-338` both claim it.
   `python3 probe/p08_argv_env_and_imports.py` section A, in a fresh
   interpreter: `provider loaded at import: False`. The two lazy import sites
   (`publish.py:340`, `:354`) are the only paths to it.

2. **The connector case works, and records both commit ids.** I re-authored the
   remote ref between the push and the read-back with a commit carrying an
   identical tree — the case design §4.5 requires to be accepted and
   `docs/lessons/operations.md:18` describes ("When a connector creates
   different commit metadata, exact shared tree and fresh main verification
   establish content publication"). `python3 probe/p06_verify_and_check.py`
   section B:

   ```
   status                    : PUBLISHED
   local_commit              : 849b767ade62fb18d48e4310c316ff4b6c135a7c
   remote_commit             : 39cbf7d659ffa0181beb35cda6ca9b8a396ab3e1
   distinct_remote_commit    : True
   both ids in the receipt   : 849b767ade62fb18d48e4310c316ff4b6c135a7c / 39cbf7d659ffa0181beb35cda6ca9b8a396ab3e1
   ```

   I could not find a spelling of the connector case that the equal-tree test at
   `publish.py:739` accepts wrongly: a re-authored commit over a *different*
   tree is `REMOTE_NOT_CONFIRMED` (`probe/p14_pending_receipt_detail.py`).

3. **`_classify_push_failure` did not misread a real transport failure as a
   divergence.** My suspicion was that `"failed to push some refs"` and
   `"fetch first"` in `_REJECTION_MARKERS` (`publish.py:223-230`) are printed by
   git for non-divergences too, which would make `_push` return without a single
   retry and tell the driver to merge a divergence that does not exist. I could
   not reproduce it. `python3 probe/p11_classify_real_failures.py`: a missing
   remote directory, a directory that is not a repository, and a genuine DNS
   failure (the sandbox has no network) all classify `PUSH_TRANSPORT`; a real
   non-fast-forward classifies `PUSH_REJECTED`.
   `python3 probe/p12_transport_dies_midpush.py`: a `receive-pack` killed
   mid-conversation prints `the remote end hung up unexpectedly`, matches no
   marker, and classifies `PUSH_TRANSPORT`; a `pre-receive` hook declining
   matches `['[remote rejected]', 'failed to push some refs']` and classifies
   `PUSH_REJECTED`. Both are the right answers. Unresolved: whether a
   *partially* completed HTTPS push behaves the same way — I have no network in
   this sandbox and could not construct one.

4. **No credential value reached an exception detail, a summary or the VERIFIED
   line.** `python3 probe/p13_attacks_that_failed.py` section B put the value in
   git's own stderr, in the shape it really takes (a credentialed remote URL):
   `GitOutcome.text()`, `.summary()` and the `GitCommandFailed` detail all read
   `https://x:[REDACTED_CREDENTIAL]@example.invalid/r.git`, and
   `value present? : False` in both. The refusal details elsewhere carry
   environment variable NAMES only (`probe/p05`, `probe/p09`, `probe/p10`), as
   `CredentialInStagedDiff`'s docstring promises (`publish.py:282-286`).

5. **`verify_published` and `check_published` could not be made to answer `True`
   about a remote that had moved.** `python3 probe/p13_attacks_that_failed.py`
   section C: on the ref `True`; after the remote advances to a different tree
   `False`; after `refs/heads/main` is deleted outright, both `False`. The live
   `ls-remote` at `publish.py:732` and the `fetched != remote_commit` test at
   `:739` are what close it; a stale local `FETCH_HEAD` does not satisfy either.

6. **`publish()` itself emits nothing forcing.** `python3 probe/p13_attacks_that_failed.py`
   section D recorded all 17 argvs of one publication: no token in
   `REWRITING_FLAGS`, no `+`-prefixed refspec, and exactly one push —
   `('push', '--porcelain', '--set-upstream', 'origin', 'HEAD:refs/heads/main')`.
   B2 is a hole in the guard for *other* callers of `LocalGit`, not a thing this
   module does.

7. **Ref injection through the `ref` argument failed every way I tried.**
   `python3 probe/p13_attacks_that_failed.py` section A: `origin/+main`,
   `origin/main:refs/heads/other`, `origin/main --force` and
   `origin/refs/heads/../../heads/main` are all `PUBLISH_REF_INVALID`.
   `origin/HEAD` is accepted and yields `refs/heads/HEAD` — a legal, if
   pathological, branch name, and not a way to move any other ref.

8. **Deviation 7's split holds.** `python3 probe/p06_verify_and_check.py`
   section A: after a later step rewrites the published file,
   `verify_published` is still `True` and `check_published` is `False`, which is
   what `publish.py:81-86` says each is for. A 40-hex sha that is the ref
   answers `True`, an ancestor answers `True`, an unknown sha answers `False`,
   and a target that is neither a path nor a sha raises `CHECK_TARGET_UNKNOWN`
   — "a gate that cannot answer must not answer ``False``" (`publish.py:894`).

9. **The path fence held everywhere except the bracket case.**
   `python3 probe/p09_path_and_argument_refusals.py` section A: `.` and
   `docs/..` are `PATH_IS_REPO_ROOT`; `../outside` and a symlink to
   `/etc/hostname` are `PATH_OUTSIDE_REPO`; `-A`, `:(glob)docs/*`, `docs/*` and
   `docs/?ote.md` are `PATH_NOT_EXPLICIT`; an absent path is `PATH_MISSING`;
   duplicates collapse. Section B: `attempt` of `0`, `-1`, `True` and `'1'` are
   all `PUBLISH_ATTEMPT_INVALID`, `attempt=4` is `PUBLISH_NOT_CONVERGING`, and a
   whitespace message is `PUBLISH_MESSAGE_EMPTY`. Section D: a file staged
   outside the named paths is `UNEXPECTED_STAGED_FILES`.

---

## What I could not determine

* **The module's own acceptance tests are not in this sandbox.** The wave plan
  names `tests/loop/test_publish.py` (`design-s7-wave-plan.md:16`) and the
  interface note reports "loop-only `224 tests OK`" on the quiesced tree
  (`WAVE0-INTERFACE.md:13-15`). `python3 run_tests.py tests.loop.test_publish`
  answers `ModuleNotFoundError: No module named 'tests.loop.test_publish'`, and
  bare `python3 run_tests.py` reports `Ran 0 tests`. I therefore could not check
  the module against the tests it was written against, could not check whether
  any finding here is already covered by an existing test, and could not run the
  test the ALLOWED_SUBCOMMANDS comment claims exists. Unresolved.

* **The other wave-0 modules are not in this sandbox either**, though the prompt
  says they are: `src/minireason/loop/` holds only `__init__.py`, `types.py`,
  `publish.py` and `data/`. Cross-module claims were therefore checked against
  `types.py`, `__init__.py` and `provider_openai_compat.py` only. In particular
  I could not check `custody.MIN_CREDENTIAL_LENGTH == 8`, the
  `custody.ALWAYS_SCANNED_ENVS` agreement, or anything about how `receipts`
  consumes the VERIFIED line. Unresolved.

* **Design §4.4, §4.5 and §4.7 are not in the sandbox** — only §2
  (`design-s2-roles-and-guard.md`) and §7 (`design-s7-wave-plan.md`). Every §4
  clause I judged against is the module's own quotation of it inside its
  docstring. Where a finding turns on a §4 clause (S1, S2, S3) I quoted the
  module's rendering and, where one exists, the wave-plan acceptance clause
  beside it. I could not verify that the module's quotations are faithful.

* **Deviation 1's premise is unverifiable here.** It says "every VERIFIED line
  already in ``docs/DECISION_LEDGER.md`` reads ``VERIFIED <commit> TREE <tree>
  ...``" (`publish.py:47-49`). There is no `docs/DECISION_LEDGER.md` in this
  sandbox (`docs/` holds only `lessons/operations.md`), so I could not check
  either the premise or the conclusion that "an existing reader still matches".
  I note without calling it a finding that the design's `tree=<sha>` spelling
  does not appear in `VERIFIED_LINE`; the tree's *value* does, behind `TREE `.

* **The runner v2 compatibility claims are unverifiable here.**
  `tools/multicycle_commitment_study_multi_v2` is not in the sandbox, so
  "byte-compatible with runner v2's function of the same name"
  (`split_publish_ref`, `publish.py:489-493`), the `upstream_ref` contract
  (`publish.py:477`) and "runner v2's ``ls-remote``-plus-byte-comparison"
  (`publish.py:38-40`) could not be tested against the thing they claim
  compatibility with.

* **Concurrency was not tested.** Two publishers racing on one checkout, and the
  "One publisher serialises commits" rule of `AGENTS.md:17`, are `W1-STEPS`'
  `RunLock`, not this module; `publish()` takes no lock and claims none. I did
  not probe it and have no finding either way.

* **A defect I suspected and could not reproduce** is recorded in "Tried, and
  could not break" item 3: a real transport failure being classified
  `PUSH_REJECTED` through the `"failed to push some refs"` marker. Every real
  failure I could construct classified correctly. I could not construct a
  partially completed HTTPS push, because the sandbox has no network, so that
  one case remains unresolved rather than cleared.

* **B1's reachability inside the loop's own run tree is bounded but not zero.**
  `types.RunPaths.reading_dir` folds bracket characters and `run_id` is an
  identifier, so no path W0-TYPES builds carries `[`. Whether any *caller* of
  `publish()` in a later wave supplies a path with a bracket is a question about
  code that does not exist yet, and I did not try to answer it. The finding is
  about the guard, which is in this sandbox and does not fire.
