"""Publish-and-verify for the automated loop driver (design of record §4.5).

Purpose. One publisher, one discipline: stage the *named* paths only, scan the
bytes for any credential this process can see, commit with the supplied
message, push **non-forcibly** to the configured ``<remote>/<branch>``, read the
ref back off the remote with ``ls-remote``, byte-compare every published path,
and return the ``VERIFIED`` line. The line is *returned*, never written:
``W0-RECEIPTS`` owns the ledger and the driver wires the two together (wave
plan §7 — "``W0-RECEIPTS`` and ``W0-PUBLISH`` are deliberately decoupled:
``publish()`` returns the VERIFIED line rather than writing it"). For the same
reason nothing here shells ``tools/repo_activity.py``; the driver brackets a
publish step with its own activity records.

Design sections implemented:

* **§4.5 Receipt, activity and publication automation** — explicit-path ``git
  add`` (never ``-A``), ``provider_openai_compat.redact_with_names`` over the
  staged diff refusing on any hit, a non-forcing push, verification, the
  ``VERIFIED`` line, the equal-tree acceptance of a connector-authored remote
  commit with **both** commit ids recorded, and "a rejected push is re-fetched
  and re-attempted as a **new publish step**, never force-pushed; three
  non-converging attempts halt".
* **§4.4 Failure handling** — a timed-out push leaves publication *pending*
  (:class:`PublishPending`), which the driver treats as blocking every
  successor step, and the 90 s git wall clock. Network failure is retried on an
  exponential backoff (:data:`PUSH_BACKOFF_SECONDS`); a **rejected** push is
  never retried inside the call, because a non-fast-forward rejection is a
  divergence to be re-fetched and merged by the driver, not a transient.
* **§4.7 Dry-run acceptance gate** — "every git operation runs against a real
  bare repo in a temp dir through the same ``publish()`` path, so ``VERIFIED``
  is genuinely exercised rather than stubbed". :class:`LocalGit` is that path:
  a real ``git`` subprocess with an explicit ``cwd`` and an explicit ``-C``, so
  the process working directory is never load-bearing.

Compatibility. Ref parsing and its error codes mirror
``tools/multicycle_commitment_study_multi_v2`` (``PUBLISH_REF_INVALID``,
``PUBLISH_REF_UNRESOLVED``, ``PUBLISH_REF_CHANGED``, ``INPUT_NOT_PUBLISHED``)
and the read-back is that runner's ``ls-remote``-plus-byte-comparison, so a
``publication_check`` built on :func:`check_published` is a drop-in for its
``send_wave(publication_check=...)``. Nothing is imported from ``tools/``: this
module's ``depends_on`` is empty in the wave plan, and a library module
reaching into a script directory is a path dependency the loop does not need.

Deviations from the design, and the reason for each:

1. **The ``VERIFIED`` line keeps the repository's established prefix.** §4.5
   specifies ``VERIFIED <utc> local=<sha> remote=<sha> tree=<sha> ref=<ref>
   paths=<n>``; every VERIFIED line already in ``docs/DECISION_LEDGER.md``
   reads ``VERIFIED <commit> TREE <tree> ...``. :data:`VERIFIED_LINE` keeps the
   published commit and tree in the established leading position and appends
   §4.5's fields, so an existing reader still matches and no field the design
   named is lost.
2. **The rejected outcome is a :class:`PublishPending` carrying
   ``reason="PUSH_REJECTED"``** rather than a separate ``PublishRejected``
   type: the wave plan's public interface names one outcome type, and the
   driver's handling — re-fetch, re-attempt as a new step, never force — is
   identical for every pending reason.
3. **The credential scan runs over the working-tree bytes first and over the
   staged diff second.** §4.5 names only the staged diff. Scanning first means
   a planted credential is refused with the index still clean, because this
   module may not ``reset`` (see :class:`HistoryRewriteRefused`) and must not
   leave a credential staged behind a refusal.
4. **Optional keyword-only parameters** (``git``, ``sleep``, ``now``,
   ``attempt``) extend the wave plan's signatures. The positional signatures
   are exactly as published; the keywords are the injection seams the
   acceptance tests and the dry run need, and each defaults to the production
   behaviour.
5. **``check_published(repo, path_or_sha, ref=None)``** — the design names the
   predicate without a signature. An existing path wins over a 40-hex
   spelling, and a target that is neither raises rather than answering
   ``False``: a gate that cannot answer must say so.
6. **The argv guard is an allow-list** (:data:`ALLOWED_SUBCOMMANDS`), not a list
   of forbidden spellings. A deny-list passed ``push -d`` (the short form of the
   listed ``--delete``), ``push --mirror``, ``push --prune``, ``update-ref -d``,
   ``branch -D``, ``checkout --orphan`` and ``symbolic-ref`` — every one of which
   deletes or moves a recorded ref, and none of which anybody had thought of. Its
   failure mode is the entry nobody thought of, and :class:`LocalGit` is the seam
   every later wave uses, so the guard now refuses everything this module does not
   itself emit. The rewriting subcommands and flags are still checked *first*, so
   the code a receipt records still says which refusal it was.
7. **Verification compares committed trees, never the working tree.**
   :func:`verify_published` asks "is this commit's tree on the ref"; reading the
   files on disk to answer it made a genuinely published commit read as
   unpublished as soon as a later step wrote under the same paths.
   :func:`check_published` keeps the working-tree comparison, because *its*
   question is whether these bytes are the published bytes.
8. **The transport is imported at the call.** Importing it loads the whole
   endpoint registry from disk, which importing a publisher has no business doing.

Never: ``-A``, ``--force``, ``--amend``, ``rebase``, ``reset``, a ``+``-prefixed
push refspec, any ref deletion, or any other git invocation this module does not
itself need. :func:`_refuse_history_rewrite` inspects the argv before a process
is spawned, so the refusal holds for every caller of :class:`LocalGit`, not only
for this module's own code paths.
"""
from __future__ import annotations

import os
import re
import stat
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType
from typing import Callable, Iterable, Mapping, Sequence

from minireason.loop.types import LoopError

__all__ = [
    "VERIFIED_LINE",
    "PUBLISHED",
    "PENDING",
    "UNCHANGED",
    "PENDING_REASONS",
    "PUSH_REJECTED",
    "PUSH_TIMEOUT",
    "PUSH_TRANSPORT",
    "REMOTE_NOT_CONFIRMED",
    "PATH_NOT_PUBLISHED",
    "PUSH_BACKOFF_SECONDS",
    "MAX_PUBLISH_ATTEMPTS",
    "GIT_TIMEOUT_SECONDS",
    "ALLOWED_SUBCOMMANDS",
    "REWRITING_SUBCOMMANDS",
    "REWRITING_FLAGS",
    "PublishError",
    "GitCommandFailed",
    "HistoryRewriteRefused",
    "GitSubcommandNotAllowed",
    "CredentialInStagedDiff",
    "PublishNotConverging",
    "GitOutcome",
    "LocalGit",
    "PublishPending",
    "PublishResult",
    "publish",
    "verify_published",
    "check_published",
    "upstream_ref",
    "split_publish_ref",
]

#: The published line. Deviation 1: the design's field list, behind the prefix
#: ``docs/DECISION_LEDGER.md`` already uses. ``commit`` and ``remote`` are the
#: commit the remote ref actually carries; ``local`` is this checkout's HEAD.
#: They differ exactly when a connector re-authored the commit, and the design
#: requires both to be recorded.
VERIFIED_LINE: str = (
    "VERIFIED {commit} TREE {tree} at {utc} local={local} remote={remote} ref={ref} paths={paths}"
)

PUBLISHED: str = "PUBLISHED"
PENDING: str = "PENDING"
UNCHANGED: str = "UNCHANGED"

PUSH_REJECTED: str = "PUSH_REJECTED"
PUSH_TIMEOUT: str = "PUSH_TIMEOUT"
PUSH_TRANSPORT: str = "PUSH_TRANSPORT"
REMOTE_NOT_CONFIRMED: str = "REMOTE_NOT_CONFIRMED"
PATH_NOT_PUBLISHED: str = "PATH_NOT_PUBLISHED"

#: Every reason a publication can be left pending. A pending publication blocks
#: every successor step (§4.4); none of them is ever resolved by forcing.
PENDING_REASONS: tuple[str, ...] = (
    PUSH_REJECTED,
    PUSH_TIMEOUT,
    PUSH_TRANSPORT,
    REMOTE_NOT_CONFIRMED,
    PATH_NOT_PUBLISHED,
)

#: Exponential backoff between push attempts *inside one publish step*, on
#: network failure only.
PUSH_BACKOFF_SECONDS: tuple[float, ...] = (2.0, 4.0, 8.0, 16.0)

#: §4.5: "three non-converging attempts halt". The driver carries the count
#: across steps and passes it as ``attempt``.
MAX_PUBLISH_ATTEMPTS: int = 3

#: §4.4 layer 3: the git wall clock, runner v2's value.
GIT_TIMEOUT_SECONDS: float = 90.0

#: **The only git subcommands this module needs.** Everything else is refused,
#: whether or not anyone thought of it: a deny-list's failure mode is the entry
#: nobody thought of, and this class is the published seam every later wave uses.
#: ``update-ref``, ``branch``, ``stash``, ``checkout``, ``switch``, ``symbolic-ref``,
#: ``worktree``, ``tag``, ``notes``, ``am``, ``cherry-pick``, ``clean`` and every
#: other spelling of "move a ref" are absent because nothing here moves a ref
#: except a non-forcing ``push``. A test asserts that every argv ``publish``,
#: ``verify_published`` and ``check_published`` actually emit is on this list, so
#: the list cannot be wider than the module's own need.
#: ``cat-file``, ``rev-list`` and ``status`` were on this list and are not
#: emitted by anything here; a test now asserts the list is exactly the set the
#: module emits, in both directions, so it cannot drift wider again.
ALLOWED_SUBCOMMANDS: frozenset[str] = frozenset({
    "add", "commit", "diff", "fetch", "ls-files", "ls-remote", "ls-tree",
    "merge-base", "push", "rev-parse", "show",
})

#: Refused outright, ahead of the allow-list, so the refusal names the reason:
#: these rewrite, discard or delete recorded history.
REWRITING_SUBCOMMANDS: frozenset[str] = frozenset(
    {"rebase", "reset", "filter-branch", "filter-repo", "replace", "gc", "prune", "reflog"}
)

#: Refused wherever they appear in an argv. ``-d`` is the short form of
#: ``--delete`` and is what ``git push -d origin <branch>`` and
#: ``git update-ref -d <ref>`` use to delete a ref; ``--mirror``, ``--prune`` and
#: ``--prune-tags`` delete remote refs that this checkout does not carry. None of
#: them appears in any argv this module emits.
REWRITING_FLAGS: frozenset[str] = frozenset({
    "--amend", "--force", "--force-with-lease", "--force-if-includes", "--hard",
    "--delete", "-d", "-D", "--mirror", "--prune", "--prune-tags",
})

#: ``-f`` is a force flag only for these subcommands (``git add -f`` is not a
#: rewrite, ``git push -f`` is).
_FORCE_SENSITIVE: frozenset[str] = frozenset(
    {"push", "checkout", "switch", "restore", "branch", "tag", "clean"}
)

_GLOBAL_OPTIONS_WITH_VALUE: frozenset[str] = frozenset(
    {"-c", "-C", "--git-dir", "--work-tree", "--namespace", "--exec-path"}
)

#: Per-subcommand spellings of "stage everything". None of them rewrites
#: history, and every one of them publishes a file nobody named - which is the
#: same defect the explicit-path rule exists to prevent, so it carries the same
#: refusal.
_STAGE_EVERYTHING: Mapping[str, frozenset[str]] = MappingProxyType({
    "add": frozenset({"-A", "--all", "--no-ignore-removal", "-u", "--update"}),
    "commit": frozenset({"-a", "--all"}),
})

#: Options whose NEXT token is a value rather than an option. The value is the
#: caller's text - a commit message, a format string - and is not scanned as an
#: argv token: ``git commit -m "--amend the record"`` amends nothing.
_OPTION_VALUES: Mapping[str, frozenset[str]] = MappingProxyType({
    "commit": frozenset({"-m", "--message", "-F", "--file"}),
})

#: Lower-cased markers git prints for a refusal to fast-forward. Matching any
#: of them means the push is a divergence, never a transient.
_REJECTION_MARKERS: tuple[str, ...] = (
    "[rejected]",
    "[remote rejected]",
    "non-fast-forward",
    "fetch first",
    "updates were rejected",
    "failed to push some refs",
)

_SHA_RE = re.compile(r"[0-9a-f]{40}")
_REMOTE_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*")
_BRANCH_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_./-]*")
_DETAIL_LIMIT = 400


# --------------------------------------------------------------------------- #
# Failures
# --------------------------------------------------------------------------- #

class PublishError(LoopError):
    """A loud publication failure with a stable code and a sanitised detail.

    A :class:`~minireason.loop.types.LoopError`, so one ``except LoopError``
    catches every wave-0 refusal and every code here is listed in
    ``types.FAILURE_CODES``. The rendered message is unchanged.
    """

    def __init__(self, code: str, detail: str = "") -> None:
        LoopError.__init__(self, code, detail)


class GitCommandFailed(PublishError):
    """A git invocation exited non-zero, timed out, or could not be spawned."""

    def __init__(self, detail: str = "") -> None:
        super().__init__("GIT_OPERATION_FAILED", detail)


class HistoryRewriteRefused(PublishError):
    """An argv that would rewrite, discard or delete recorded history."""

    def __init__(self, detail: str = "") -> None:
        super().__init__("HISTORY_REWRITE_REFUSED", detail)


class GitSubcommandNotAllowed(HistoryRewriteRefused):
    """An argv naming a subcommand this module does not need.

    A subclass of :class:`HistoryRewriteRefused` so that every caller written
    against the guard's published exception still catches it, with its own code:
    the refusal is "nothing here does that", not "that would rewrite history",
    and a receipt should be able to tell the two apart.
    """

    def __init__(self, detail: str = "") -> None:
        PublishError.__init__(self, "GIT_SUBCOMMAND_NOT_ALLOWED", detail)


class CredentialInStagedDiff(PublishError):
    """A credential this process can see appears in the bytes to be published.

    The detail carries the environment variable NAMES only, never a value and
    never a fragment of one.
    """

    def __init__(self, detail: str = "") -> None:
        super().__init__("SECRET_IN_STAGED_DIFF", detail)


class PublishNotConverging(PublishError):
    """Three attempts at one publication did not converge (§4.5)."""

    def __init__(self, detail: str = "") -> None:
        super().__init__("PUBLISH_NOT_CONVERGING", detail)


# --------------------------------------------------------------------------- #
# Git, by subprocess, with an explicit cwd
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class GitOutcome:
    """One git invocation's raw result. ``code`` is -1 when nothing ran."""

    code: int
    stdout: bytes
    stderr: bytes
    timed_out: bool
    args: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return self.code == 0 and not self.timed_out

    def text(self) -> str:
        """stdout and stderr together, decoded leniently and redacted."""

        blob = (self.stdout + b"\n" + self.stderr).decode("utf-8", "replace")
        return _redact_with_names(blob)[0]

    def summary(self) -> str:
        """A short, credential-free description fit for an exception detail."""

        head = " ".join(self.args[:2])
        state = "timed out" if self.timed_out else f"exit {self.code}"
        return f"git {head} {state}: {self.text().strip()[:_DETAIL_LIMIT]}"


def _redact_with_names(text: str) -> tuple[str, Sequence[str]]:
    """``provider_openai_compat.redact_with_names``, imported at the call.

    Lazy so that importing this module does not load the twenty-four endpoints
    from disk as a side effect — ``custody`` avoids exactly that deliberately, and
    this module used to do it anyway. Python caches the module, so a test that
    registers a secret environment name still reaches the same scanner.
    """

    from minireason.provider_openai_compat import redact_with_names

    return redact_with_names(text)


def _credential_env_names() -> tuple[str, ...]:
    """Every environment variable name known to be credential-bearing.

    The endpoint registry's own ``key_env`` values plus whatever a caller
    registered with ``provider_openai_compat.register_secret_envs``. Git never
    needs any of them, so they are removed from every child environment. The
    registry is read here, at the call, rather than at import (N3).
    """

    from minireason import provider_openai_compat as transport

    try:
        # The transport's own list: the registry's key_env values, the names a
        # caller registered, AND the always-secret names the registry does not
        # mention. Reading only the first two left those out of every child
        # environment's exclusion list.
        return tuple(sorted(transport._secret_env_names()))
    except AttributeError:  # pragma: no cover - a transport without the helper
        names = {endpoint.key_env for endpoint in transport.ENDPOINTS.values()}
        names.update(transport.registered_secret_envs())
        return tuple(sorted(names))


def _subcommand(tokens: Sequence[str]) -> str:
    """The git subcommand in an argv, skipping global options and their values."""

    skip = False
    for token in tokens:
        if skip:
            skip = False
            continue
        if token in _GLOBAL_OPTIONS_WITH_VALUE:
            skip = True
            continue
        if token.startswith("-"):
            continue
        return token
    return ""


def _option_name(token: str) -> str:
    """``--force-with-lease=origin/main:abc`` -> ``--force-with-lease``."""

    return token.split("=", 1)[0]


def _is_rewriting_option(token: str) -> bool:
    """Whether ``token`` names a rewriting flag, however git would read it.

    Three spellings used to walk past an exact-token comparison:

    * ``--force-with-lease=<ref>:<sha>`` - the option with its value attached,
      which performed a **real forced update** through :class:`LocalGit`;
    * ``--amen``, ``--forc`` - git accepts any unambiguous abbreviation of a
      long option, so a proper prefix of a refused flag is that flag;
    * the stage-everything spellings ``add -A`` / ``add --all`` and
      ``commit -a``, which are not rewrites but publish files the credential
      scan never read, and are refused with the same code for the same reason.
    """

    name = _option_name(token)
    if name in REWRITING_FLAGS:
        return True
    if not name.startswith("--") or len(name) <= 2:
        return False
    return any(flag.startswith(name) for flag in REWRITING_FLAGS if flag.startswith("--"))


def _refuse_history_rewrite(tokens: Sequence[str]) -> None:
    """Refuse every argv but the ones this module needs.

    The order matters, because the code a receipt records should say *why*: an
    argv that rewrites, discards or deletes history is ``HISTORY_REWRITE_REFUSED``
    whatever its subcommand, and only then is an argv refused merely for naming a
    subcommand nothing here uses (``GIT_SUBCOMMAND_NOT_ALLOWED``, which is a
    subclass, so one ``except HistoryRewriteRefused`` still catches both).

    Options are compared by **name** - the part before ``=`` - and by prefix, so
    neither a value attached to a flag nor git's own abbreviation of one gets
    past. See :func:`_is_rewriting_option`.
    """

    subcommand = _subcommand(tokens)
    if subcommand in REWRITING_SUBCOMMANDS:
        raise HistoryRewriteRefused(f"git {subcommand}")
    scanned = list(tokens[1:] if tokens and tokens[0] == subcommand else tokens)
    values = _OPTION_VALUES.get(subcommand, frozenset())
    skip = False
    for index, token in enumerate(scanned):
        if skip:
            # The VALUE of an option, not an option: a commit message reading
            # ``--amend`` is a message, and refusing it refused a publication for
            # what it said rather than for what it did.
            skip = False
            continue
        if token in values:
            skip = True
            continue
        if token == "--" :
            break            # everything after ``--`` is a path, not an option
        if _is_rewriting_option(token):
            raise HistoryRewriteRefused(f"git {subcommand} {token}")
        if token == "-f" and subcommand in _FORCE_SENSITIVE:
            raise HistoryRewriteRefused(f"git {subcommand} -f")
        if token in _STAGE_EVERYTHING.get(subcommand, ()):
            raise HistoryRewriteRefused(
                f"git {subcommand} {token} stages every changed file, including "
                "files the credential scan never read")
        if subcommand == "push" and token.startswith("+") and ":" in token:
            raise HistoryRewriteRefused(f"git push {token}")
    if subcommand not in ALLOWED_SUBCOMMANDS:
        raise GitSubcommandNotAllowed(
            f"git {subcommand or '<none>'} is not one of the subcommands this "
            f"module needs: {', '.join(sorted(ALLOWED_SUBCOMMANDS))}")


class LocalGit:
    """Every git invocation this module makes, against one explicit checkout.

    The checkout path is resolved once and passed twice — as ``git -C`` and as
    the subprocess ``cwd`` — so the process working directory is never relied
    on. This is also the seam the dry run and the tests replace: the double
    runs real git against a real temporary bare repo, which is what makes
    ``VERIFIED`` an exercised claim rather than a stub.
    """

    def __init__(self, repo: str | os.PathLike[str], *, timeout: float = GIT_TIMEOUT_SECONDS,
                 env: dict[str, str] | None = None) -> None:
        self.repo: Path = Path(repo).resolve()
        marker = self.repo / ".git"
        if not marker.exists() and not (self.repo / "HEAD").exists():
            raise PublishError("REPO_NOT_A_GIT_CHECKOUT", str(self.repo))
        self.timeout: float = float(timeout)
        self._env: dict[str, str] | None = dict(env) if env is not None else None

    def environment(self) -> dict[str, str]:
        """The child environment, with every known credential removed."""

        base = dict(os.environ) if self._env is None else dict(self._env)
        for name in _credential_env_names():
            base.pop(name, None)
        return base

    def _invoke(self, tokens: Sequence[str]) -> GitOutcome:
        _refuse_history_rewrite(tokens)
        # --literal-pathspecs: every path this module passes is a file name a
        # caller wrote, never a pattern. Without it ``report[1].md`` is a
        # wildmatch that also names ``report1.md``, and a neighbour nobody
        # named - and the credential scan never read - is staged with it.
        argv = ["git", "--literal-pathspecs", "-C", str(self.repo), *tokens]
        try:
            done = subprocess.run(argv, cwd=str(self.repo), capture_output=True,
                                  timeout=self.timeout, env=self.environment(), check=False)
        except subprocess.TimeoutExpired as expired:
            return GitOutcome(-1, expired.stdout or b"", expired.stderr or b"", True, tuple(tokens))
        except OSError as error:
            return GitOutcome(-1, b"", str(error).encode("utf-8", "replace"), False, tuple(tokens))
        return GitOutcome(done.returncode, done.stdout, done.stderr, False, tuple(tokens))

    def status(self, *tokens: str) -> GitOutcome:
        """Run git and return the outcome, whatever it is."""

        return self._invoke(tokens)

    def run(self, *tokens: str) -> bytes:
        """Run git, returning stdout bytes; raise :class:`GitCommandFailed`."""

        outcome = self._invoke(tokens)
        if not outcome.ok:
            raise GitCommandFailed(outcome.summary())
        return outcome.stdout

    def text(self, *tokens: str) -> str:
        """:meth:`run`, decoded as UTF-8 and stripped."""

        return self.run(*tokens).decode("utf-8").strip()


def _git_for(repo: str | os.PathLike[str] | LocalGit, git: LocalGit | None) -> LocalGit:
    if git is not None:
        return git
    if isinstance(repo, LocalGit):
        return repo
    return LocalGit(repo)


# --------------------------------------------------------------------------- #
# Refs
# --------------------------------------------------------------------------- #

def upstream_ref(repo: str | os.PathLike[str] | LocalGit, *, git: LocalGit | None = None) -> str:
    """The current branch's upstream, e.g. ``origin/claude/project-state-...``.

    Same contract and same error code as runner v2's ``upstream_ref``.
    """

    resolved = _git_for(repo, git)
    outcome = resolved.status("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    ref = outcome.stdout.decode("utf-8", "replace").strip() if outcome.ok else ""
    if not ref:
        raise PublishError("PUBLISH_REF_UNRESOLVED", str(resolved.repo))
    return ref


def split_publish_ref(ref: str) -> tuple[str, str]:
    """``origin/feature/x`` -> ``("origin", "refs/heads/feature/x")``.

    Byte-compatible with runner v2's function of the same name, including its
    ``PUBLISH_REF_INVALID`` refusal.
    """

    if not isinstance(ref, str) or "/" not in ref or ref.startswith("/") or ref.endswith("/"):
        raise PublishError("PUBLISH_REF_INVALID", str(ref))
    remote, branch = ref.split("/", 1)
    if not _REMOTE_RE.fullmatch(remote) or ".." in branch or not _BRANCH_RE.fullmatch(branch):
        raise PublishError("PUBLISH_REF_INVALID", str(ref))
    return remote, "refs/heads/" + branch


# --------------------------------------------------------------------------- #
# Paths and credentials
# --------------------------------------------------------------------------- #

def _explicit_paths(repo: Path, paths: Iterable[str | os.PathLike[str]], *,
                    allow_empty: bool = False) -> tuple[str, ...]:
    """Repo-relative POSIX names for the caller's explicit paths.

    Refuses pathspec magic, the repo root, anything outside the repo and
    anything absent. There is therefore no spelling of ``paths`` that reaches
    git as ``-A``, ``--all`` or a bare ``.``.
    """

    names: list[str] = []
    for entry in paths:
        try:
            raw = entry if isinstance(entry, str) else os.fsdecode(entry)
        except (UnicodeDecodeError, TypeError, ValueError):
            # A name whose bytes are not this filesystem's encoding: it cannot be
            # written into an argv or compared with git's own listing, and
            # decoding it "leniently" would stage a different file.
            raise PublishError("PATH_NOT_EXPLICIT", repr(entry)) from None
        raw = str(raw)
        try:
            raw.encode("utf-8")
        except UnicodeEncodeError:
            # A name whose bytes are not valid UTF-8: git's own ``-z`` listings
            # are decoded as UTF-8 here, so such a name could be staged and then
            # never matched against what was staged.
            raise PublishError("PATH_NOT_EXPLICIT", ascii(raw)) from None
        if not raw or "\x00" in raw or raw != raw.strip():
            raise PublishError("PATH_NOT_EXPLICIT", repr(raw))
        candidate = Path(raw)
        if ".." in candidate.parts:
            raise PublishError("PATH_OUTSIDE_REPO", raw)
        if candidate.is_absolute():
            try:
                candidate = candidate.relative_to(repo)
            except ValueError:
                raise PublishError("PATH_OUTSIDE_REPO", raw) from None
        # Native Windows separators and drive prefixes are path syntax, not
        # Git pathspec syntax. Validate the repository-relative POSIX spelling.
        raw = candidate.as_posix()
        if any(character in raw for character in _PATHSPEC_MAGIC):
            # ``report[1].md`` reaches git as a WILDMATCH pathspec, so
            # ``report1.md`` is staged, committed and pushed as well - a file the
            # working-tree credential scan never read, under a name nobody wrote.
            raise PublishError("PATH_NOT_EXPLICIT", raw)
        if not raw or raw.startswith("-") or raw.startswith(":"):
            raise PublishError("PATH_NOT_EXPLICIT", raw)
        if "\x00" in raw or raw != raw.strip():
            raise PublishError("PATH_NOT_EXPLICIT", repr(raw))
        candidate = Path(raw)
        resolved = (candidate if candidate.is_absolute() else repo / candidate).resolve()
        try:
            relative = resolved.relative_to(repo)
        except ValueError:
            raise PublishError("PATH_OUTSIDE_REPO", raw) from None
        name = relative.as_posix()
        if name in ("", "."):
            raise PublishError("PATH_IS_REPO_ROOT", raw)
        if not resolved.exists():
            raise PublishError("PATH_MISSING", name)
        if name not in names:
            names.append(name)
    if not names and not allow_empty:
        raise PublishError("PUBLISH_PATHS_EMPTY", "")
    return tuple(names)


#: Every character git reads as pathspec magic under the default wildmatch. A
#: name carrying one is refused rather than escaped: ``--literal-pathspecs`` is
#: also set on every argv (see :meth:`LocalGit._invoke`), and the two together
#: mean a caller's path names exactly the file it spells, both when git reads it
#: and when this module does.
_PATHSPEC_MAGIC: str = "*?[]\\"


def _covered(name: str, names: Sequence[str]) -> bool:
    return any(name == entry or name.startswith(entry + "/") for entry in names)


def _walk_files(repo: Path, names: Sequence[str]) -> tuple[str, ...]:
    """Every working-tree file under the explicit paths, ``.git`` excluded.

    The fallback for a caller with no git to ask. It skips a ``.git`` at **any**
    depth, not only the first path component, because a nested checkout's
    ``.git/config`` is a file full of credentials that nobody meant to scan and
    that git itself would never stage.
    """

    found: list[str] = []
    for name in names:
        target = repo / name
        candidates = [target] if target.is_file() else sorted(
            path for path in target.rglob("*") if path.is_file()
        )
        for path in candidates:
            relative = path.relative_to(repo).as_posix()
            if ".git" in relative.split("/"):
                continue
            if relative not in found:
                found.append(relative)
    return tuple(found)


def _scan_set(git: LocalGit, names: Sequence[str]) -> tuple[str, ...]:
    """The files a publish of ``names`` would stage, as **git** lists them.

    Derived from git rather than from a directory walk, so what is scanned and
    what is committed are one set by construction: the walk read files git
    ignores (and, before the fix above, a nested ``.git/config``), and missed
    nothing only by luck. A git that cannot answer falls back to the walk, which
    is the wider of the two and therefore the safe side to fail to.
    """

    outcome = git.status("ls-files", "-z", "--cached", "--others",
                         "--exclude-standard", "--", *names)
    if not outcome.ok:
        return _walk_files(git.repo, names)
    return tuple(entry for entry in outcome.stdout.decode("utf-8", "replace").split("\0")
                 if entry)


def _publication_files(git: LocalGit, paths: Iterable[str | os.PathLike[str]]
                       ) -> tuple[str, ...]:
    """Expand regular files and tracked deletions without following links."""
    paths = tuple(paths)
    names = _explicit_paths(git.repo, paths, allow_empty=True)
    found: set[str] = set()
    directories = [name for name in names if (git.repo / name).is_dir()]

    def inspect(path: Path) -> os.stat_result:
        info = path.lstat()
        if (stat.S_ISLNK(info.st_mode)
                or getattr(info, "st_file_attributes", 0)
                & stat.FILE_ATTRIBUTE_REPARSE_POINT):
            raise PublishError("PATH_NOT_EXPLICIT", str(path))
        return info

    # _explicit_paths resolves caller paths; refuse links before using those
    # resolved names, including links in a selected path's parent components.
    for entry in paths:
        target = Path(entry)
        target = target if target.is_absolute() else git.repo / target
        for path in (target, *target.parents):
            if path == git.repo:
                break
            inspect(path)

    def visit(path: Path) -> None:
        relative = path.relative_to(git.repo).as_posix()
        if ".git" in relative.split("/"):
            return
        info = inspect(path)
        if stat.S_ISREG(info.st_mode):
            found.add(relative)
        elif stat.S_ISDIR(info.st_mode):
            for child in path.iterdir():
                visit(child)

    for name in names:
        visit(git.repo / name)
    if directories:
        # Preserve Git's existing directory ignore semantics. Explicitly named
        # files stay explicit, including ignored files that git add will refuse.
        admitted = set(_scan_set(git, directories))
        explicit = set(names) - set(directories)
        found = {name for name in found if name in explicit or name in admitted}
    # A deleted tracked regular file still names a file in HEAD. Preserve
    # directory-selected deletions, including ones already staged in the index.
    if directories and git.status("rev-parse", "--verify", "--quiet", "HEAD").ok:
        raw = git.run("ls-tree", "-r", "-z", "HEAD", "--", *directories)
        for entry in raw.decode("utf-8").split("\0"):
            if not entry:
                continue
            meta, name = entry.split("\t", 1)
            if (meta.split()[0] in ("100644", "100755")
                    and not (git.repo / name).exists()):
                found.add(name)
    return tuple(sorted(found))


def _tracked_files(git: LocalGit, names: Sequence[str]) -> tuple[str, ...]:
    """The tracked files the pathspec names, as git itself lists them."""

    raw = git.run("ls-files", "-z", "--cached", "--", *names)
    return tuple(sorted(entry for entry in raw.decode("utf-8").split("\0") if entry))


def _refuse_credential_text(text: str, where: str) -> None:
    """Refuse if any credential visible to this process appears in ``text``."""

    _redacted, hit = _redact_with_names(text)
    if hit:
        raise CredentialInStagedDiff(f"{where}: {', '.join(hit)}")


def _refuse_credentials(repo: Path, names: Sequence[str],
                        git: LocalGit | None = None) -> None:
    """Scan, before the index is touched, exactly what a publish would stage.

    The **name** of each file is scanned as well as its bytes: a credential can
    be the file's own name (``keys/sk-live-....json``), and deviation 3's "the
    index is still clean" check reads the diff, which does not carry the name in
    a form the scan saw.
    """

    listed = _scan_set(git, names) if git is not None else _walk_files(repo, names)
    for name in listed:
        _refuse_credential_text(name, f"path name {name}")
        path = repo / name
        if not path.is_file():
            continue
        _refuse_credential_text(path.read_bytes().decode("utf-8", "replace"), name)


def _refuse_added_lines(diff: str, where: str) -> None:
    """Scan the **added** lines of a unified diff, and the file names in it.

    Deviation 3 scanned the whole diff, so a commit that *removes* a credential
    already in HEAD was refused for carrying it - the leak-repair commit was the
    one commit this module would not publish. A removal line is the credential
    leaving the tree; only what is being added is what is being published.
    """

    added: list[str] = []
    for line in diff.split("\n"):
        if line.startswith("+++") or line.startswith("---"):
            # The name half of a file header: scanned, because a credential can
            # be a file's own name and the +/- lines never carry it.
            added.append(line[4:])
        elif line.startswith("+"):
            added.append(line[1:])
        elif line.startswith("diff --git "):
            added.append(line[len("diff --git "):])
    _refuse_credential_text("\n".join(added), where)


def _staged_names(git: LocalGit) -> tuple[str, ...]:
    """Names staged in the index relative to HEAD (or the whole index if none)."""

    if git.status("rev-parse", "--verify", "--quiet", "HEAD").ok:
        raw = git.run("diff", "--cached", "--name-only", "-z")
    else:
        raw = git.run("ls-files", "--cached", "-z")
    return tuple(entry for entry in raw.decode("utf-8").split("\0") if entry)


# --------------------------------------------------------------------------- #
# Outcomes
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class PublishPending:
    """A publication that did not complete and must not be forced.

    ``reason`` is a member of :data:`PENDING_REASONS`. The driver re-fetches,
    reconciles, and re-attempts as a **new** publish step with ``attempt + 1``.
    """

    reason: str
    attempt: int
    ref: str
    local_commit: str | None = None
    remote_commit: str | None = None
    detail: str = ""


@dataclass(frozen=True)
class PublishResult:
    """What one publish step did, and the VERIFIED line for the driver to file."""

    status: str
    ref: str
    paths: tuple[str, ...]
    files: tuple[str, ...]
    attempt: int
    committed: bool
    local_commit: str | None = None
    remote_commit: str | None = None
    tree: str | None = None
    verified_line: str | None = None
    pending: PublishPending | None = None

    @property
    def published(self) -> bool:
        return self.status == PUBLISHED

    @property
    def distinct_remote_commit(self) -> bool:
        """True when the connector authored its own commit over an equal tree."""

        return bool(self.local_commit and self.remote_commit
                    and self.local_commit != self.remote_commit)

    def as_receipt(self) -> dict[str, object]:
        """The step-receipt fields §4.3 keeps for a publication."""

        return {
            "status": self.status,
            "ref": self.ref,
            "paths": list(self.paths),
            "files": list(self.files),
            "attempt": self.attempt,
            "committed": self.committed,
            # Only a PUBLISHED result has a published commit. On a PENDING one
            # ``remote_commit`` is whatever the OTHER party put on the ref, and
            # recording that as "the commit this step published" is a false
            # statement about this run's own work.
            "published_commit": self.remote_commit if self.published else None,
            "remote_commit": self.remote_commit,
            "local_commit": self.local_commit,
            "tree": self.tree,
            "verified_line": self.verified_line,
            "pending_reason": self.pending.reason if self.pending else None,
            "pending_detail": self.pending.detail if self.pending else None,
        }


@dataclass(frozen=True)
class _ReadBack:
    ok: bool
    remote_commit: str | None = None
    remote_tree: str | None = None
    reason: str = ""
    detail: str = ""


# --------------------------------------------------------------------------- #
# The publication
# --------------------------------------------------------------------------- #

def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _stamp(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _classify_push_failure(outcome: GitOutcome) -> str:
    if outcome.timed_out:
        return PUSH_TIMEOUT
    blob = outcome.text().lower()
    if any(marker in blob for marker in _REJECTION_MARKERS):
        return PUSH_REJECTED
    return PUSH_TRANSPORT


def _push(git: LocalGit, remote: str, qualified: str,
          sleep: Callable[[float], None]) -> tuple[str, str] | None:
    """Push non-forcibly, retrying network failure only. ``None`` means pushed."""

    for index in range(len(PUSH_BACKOFF_SECONDS) + 1):
        outcome = git.status("push", "--porcelain", "--set-upstream", remote,
                             "HEAD:" + qualified)
        if outcome.ok:
            return None
        reason = _classify_push_failure(outcome)
        # A timeout is PENDING on the FIRST one, as the acceptance clause says.
        # Retrying it four more times spent up to 480 s inside one call, and a
        # push that timed out may well have landed: re-pushing is not a retry of
        # a failed act, it is a second act on an unknown state.
        if reason in (PUSH_REJECTED, PUSH_TIMEOUT) or index == len(PUSH_BACKOFF_SECONDS):
            return reason, outcome.summary()
        sleep(PUSH_BACKOFF_SECONDS[index])
    raise AssertionError("unreachable")  # pragma: no cover


def _tree_blobs(git: LocalGit, commit: str, files: Sequence[str]) -> dict[str, str]:
    """``{path: blob id}`` for ``files`` as the tree of ``commit`` carries them.

    ``git ls-tree`` reads the committed objects, so this answers what was
    *published* rather than what the working tree happens to hold now.
    """

    raw = git.run("ls-tree", "-r", "-z", commit, "--", *files)
    blobs: dict[str, str] = {}
    for entry in raw.decode("utf-8").split("\0"):
        if not entry or "\t" not in entry:
            continue
        meta, name = entry.split("\t", 1)
        fields = meta.split()
        if len(fields) >= 3 and fields[1] == "blob":
            blobs[name] = fields[2]
    return blobs


def _read_back(git: LocalGit, remote: str, qualified: str, tree: str,
               files: Sequence[str], source: str) -> _ReadBack:
    """Read the ref off the remote and compare the published objects.

    ``source`` is the commit whose bytes were supposed to be published. Both
    sides of the comparison are **tree objects**: the working tree is not
    consulted at all, because it is not what was published and it moves on. The
    earlier form compared the remote's blobs with the files on disk, so
    :func:`verify_published` answered ``False`` for a genuinely published commit
    as soon as the next step wrote anything under those paths.
    """

    try:
        rows = git.text("ls-remote", "--refs", remote, qualified).split()
    except GitCommandFailed as failed:
        # The push already landed. A read-back that cannot RUN says nothing
        # about the remote, and raising here turned a publication that may well
        # have succeeded into an exception out of publish() with no result at
        # all - so the driver could neither proceed nor re-attempt.
        return _ReadBack(False, None, None, REMOTE_NOT_CONFIRMED,
                         "the read-back could not be run: " + failed.detail[:80])
    if len(rows) < 2 or rows[1] != qualified:
        return _ReadBack(False, None, None, REMOTE_NOT_CONFIRMED, "PUBLISH_REF_CHANGED")
    remote_commit = rows[0]
    try:
        git.run("fetch", "--no-tags", remote, qualified)
        fetched = git.text("rev-parse", "FETCH_HEAD")
        remote_tree = git.text("rev-parse", "FETCH_HEAD^{tree}")
    except GitCommandFailed as failed:
        return _ReadBack(False, remote_commit, None, REMOTE_NOT_CONFIRMED,
                         "the read-back could not be run: " + failed.detail[:80])
    if fetched != remote_commit or remote_tree != tree:
        return _ReadBack(False, remote_commit, remote_tree, REMOTE_NOT_CONFIRMED,
                         "PUBLISH_REF_CHANGED")
    try:
        published = _tree_blobs(git, remote_commit, files)
        expected = _tree_blobs(git, source, files)
    except GitCommandFailed as failed:
        return _ReadBack(False, remote_commit, remote_tree, PATH_NOT_PUBLISHED,
                         "INPUT_NOT_PUBLISHED " + failed.detail[:80])
    for name in files:
        if name not in published or published[name] != expected.get(name):
            return _ReadBack(False, remote_commit, remote_tree, PATH_NOT_PUBLISHED,
                             "INPUT_NOT_PUBLISHED " + name)
    return _ReadBack(True, remote_commit, remote_tree)


def _pending_result(pending: PublishPending, *, ref: str, names: tuple[str, ...],
                    files: tuple[str, ...], committed: bool, tree: str | None) -> PublishResult:
    if pending.attempt >= MAX_PUBLISH_ATTEMPTS:
        raise PublishNotConverging(
            f"{pending.attempt} attempts on {ref}, last {pending.reason}: {pending.detail}")
    return PublishResult(status=PENDING, ref=ref, paths=names, files=files,
                         attempt=pending.attempt, committed=committed,
                         local_commit=pending.local_commit, remote_commit=pending.remote_commit,
                         tree=tree, verified_line=None, pending=pending)


def publish(repo: str | os.PathLike[str] | LocalGit,
            paths: Iterable[str | os.PathLike[str]],
            message: str,
            ref: str | None = None,
            *,
            attempt: int = 1,
            retry_pending: bool = False,
            git: LocalGit | None = None,
            sleep: Callable[[float], None] | None = None,
            now: Callable[[], datetime] | None = None) -> PublishResult:
    """Stage, scan, commit, push non-forcibly, verify, and return the line.

    ``paths`` are explicit repo-relative or absolute paths that must exist;
    nothing else is ever staged. ``ref`` defaults to the branch's upstream.
    ``attempt`` is the driver's count of publish steps for this publication:
    the third non-converging attempt raises :class:`PublishNotConverging`.

    Directories expand to regular files in sorted order. Only an empty
    selection returns ``UNCHANGED``, with published=false and no VERIFIED line.
    Already-committed files still go through push and remote read-back.
    ``retry_pending`` retains that obligation even if a prior deletion commit
    emptied the selection. A remote-tracking difference also prevents a no-op;
    only the push and remote read-back below can establish publication.
    A ``PENDING`` result blocks every successor step; dispatch still checks
    its input custody independently.
    """

    resolved = _git_for(repo, git)
    wait = sleep if sleep is not None else time.sleep
    clock = now if now is not None else _utc_now
    if not isinstance(attempt, int) or isinstance(attempt, bool) or attempt < 1:
        raise PublishError("PUBLISH_ATTEMPT_INVALID", repr(attempt))
    if attempt > MAX_PUBLISH_ATTEMPTS:
        raise PublishNotConverging(f"attempt {attempt} exceeds {MAX_PUBLISH_ATTEMPTS}")
    if not str(message).strip():
        raise PublishError("PUBLISH_MESSAGE_EMPTY", "")

    paths = tuple(paths)
    names = _publication_files(resolved, paths)
    if not names and not retry_pending:
        selected = _explicit_paths(resolved.repo, paths, allow_empty=True)
        if selected:
            # A committed deletion disappears from HEAD and the working tree.
            # The last observed remote tree still carries its selected name.
            if ref:
                split_publish_ref(ref)
            previous = resolved.status(
                "rev-parse", "--verify", "--quiet",
                "refs/remotes/" + ref if ref else "@{u}")
            if previous.ok:
                retry_pending = bool(resolved.run(
                    "diff", "--name-only", "-z", previous.stdout.decode("utf-8").strip(),
                    "HEAD", "--", *selected))
    if not names and not retry_pending:
        return PublishResult(status=UNCHANGED, ref=ref or "", paths=names,
                             files=names, attempt=attempt, committed=False)
    publish_ref = ref or upstream_ref(resolved)
    remote, qualified = split_publish_ref(publish_ref)

    # Deviation 3: before the index is touched, so a refusal never leaves a
    # credential staged in a repository this module may not reset.
    if names:
        _refuse_credentials(resolved.repo, names, resolved)
    stray = [name for name in _staged_names(resolved) if not _covered(name, names)]
    if stray:
        raise PublishError("UNEXPECTED_STAGED_FILES", ", ".join(sorted(stray)[:8]))

    files: tuple[str, ...] = ()
    committed = False
    if names:
        # An already-staged deletion is absent from both disk and index: git add
        # rejects that explicit pathspec. Leave it staged, while still adding
        # missing files that remain in the index to stage unstaged deletions.
        indexed = set(_tracked_files(resolved, names))
        stageable = tuple(name for name in names
                         if name in indexed or (resolved.repo / name).is_file())
        if stageable:
            resolved.run("add", "--", *stageable)
        _refuse_added_lines(
            resolved.run("diff", "--cached", "--no-color", "--", *names).decode("utf-8", "replace"),
            "staged diff")

        files = _tracked_files(resolved, names)
        committed = bool(_staged_names(resolved))
        if not files and not committed:
            raise PublishError("PUBLISH_PATHS_UNTRACKED", ", ".join(names))
        if committed:
            resolved.run("commit", "-m", str(message), "--", *names)

    local = resolved.text("rev-parse", "HEAD")
    tree = resolved.text("rev-parse", "HEAD^{tree}")

    failure = _push(resolved, remote, qualified, wait)
    if failure is not None:
        reason, detail = failure
        return _pending_result(
            PublishPending(reason=reason, attempt=attempt, ref=publish_ref,
                           local_commit=local, detail=detail),
            ref=publish_ref, names=names, files=files, committed=committed, tree=tree)

    read = _read_back(resolved, remote, qualified, tree, files, local)
    if not read.ok:
        return _pending_result(
            PublishPending(reason=read.reason, attempt=attempt, ref=publish_ref,
                           local_commit=local, remote_commit=read.remote_commit,
                           detail=read.detail),
            ref=publish_ref, names=names, files=files, committed=committed, tree=tree)

    line = VERIFIED_LINE.format(commit=read.remote_commit, tree=tree, utc=_stamp(clock()),
                                local=local, remote=read.remote_commit, ref=publish_ref,
                                paths=len(names))
    return PublishResult(status=PUBLISHED, ref=publish_ref, paths=names, files=files,
                         attempt=attempt, committed=committed, local_commit=local,
                         remote_commit=read.remote_commit, tree=tree, verified_line=line,
                         pending=None)


def verify_published(repo: str | os.PathLike[str] | LocalGit,
                     paths: Iterable[str | os.PathLike[str]],
                     commit: str,
                     ref: str | None = None,
                     *,
                     git: LocalGit | None = None) -> bool:
    """Is ``commit``'s tree on ``ref``, with these paths' objects published?

    True also when the remote carries a *different* commit id over an equal
    tree — the connector case §4.5 requires to be accepted — and the caller
    records both ids from the :class:`PublishResult`.

    The comparison is between two **committed trees**: ``commit``'s and the
    remote ref's. The working tree is not read, and a later step writing under
    the same paths does not make a published commit unpublished. Ask
    :func:`check_published` about the bytes on disk; that is its question.
    """

    resolved = _git_for(repo, git)
    names = _explicit_paths(resolved.repo, paths)
    publish_ref = ref or upstream_ref(resolved)
    remote, qualified = split_publish_ref(publish_ref)
    try:
        tree = resolved.text("rev-parse", str(commit) + "^{tree}")
        files = _tracked_files(resolved, names)
    except GitCommandFailed:
        return False
    if not files:
        return False
    try:
        return _read_back(resolved, remote, qualified, tree, files, str(commit)).ok
    except GitCommandFailed:
        return False


def check_published(repo: str | os.PathLike[str] | LocalGit,
                    path_or_sha: str | os.PathLike[str],
                    ref: str | None = None,
                    *,
                    git: LocalGit | None = None) -> bool:
    """Publication-before-dispatch: are these bytes, or this commit, on the ref?

    A path (absolute or repo-relative, file or directory) answers "are the
    working-tree bytes under it exactly the bytes on the published ref" — runner
    v2's ``INPUT_NOT_PUBLISHED`` comparison, as a predicate. A 40-hex sha
    answers "is that commit the published ref or an ancestor of it". Anything
    that is neither raises: a gate that cannot answer must not answer ``False``.
    """

    resolved = _git_for(repo, git)
    publish_ref = ref or upstream_ref(resolved)
    remote, qualified = split_publish_ref(publish_ref)
    raw = str(path_or_sha)
    candidate = Path(raw)
    target = candidate if candidate.is_absolute() else resolved.repo / candidate

    try:
        rows = resolved.text("ls-remote", "--refs", remote, qualified).split()
    except GitCommandFailed:
        return False
    if len(rows) < 2 or rows[1] != qualified:
        return False
    remote_commit = rows[0]

    if target.exists():
        names = _explicit_paths(resolved.repo, [raw])
        files = _tracked_files(resolved, names)
        if not files:
            return False
        try:
            resolved.run("fetch", "--no-tags", remote, qualified)
            for name in files:
                if resolved.run("show", remote_commit + ":" + name) != (resolved.repo / name).read_bytes():
                    return False
        except GitCommandFailed:
            return False
        return True

    if _SHA_RE.fullmatch(raw):
        if raw == remote_commit:
            return True
        try:
            resolved.run("fetch", "--no-tags", remote, qualified)
        except GitCommandFailed:
            return False
        return resolved.status("merge-base", "--is-ancestor", raw, "FETCH_HEAD").ok

    raise PublishError("CHECK_TARGET_UNKNOWN", raw)
