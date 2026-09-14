"""Acceptance tests for ``minireason.loop.publish`` (wave plan W0-PUBLISH).

Every test is named after the clause of the module's acceptance list it
discharges. Nothing here is simulated: each test builds a real temporary bare
repository and a real working clone under ``tempfile``, and every push and
read-back runs against that bare repo through the module's own
:class:`~minireason.loop.publish.LocalGit`. No network, no provider, no
credential — the one "credential" planted is a fixed non-secret literal
registered under a test-only environment name.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Callable, Sequence
from unittest import mock

from minireason import provider_openai_compat as compat
from minireason.loop import publish as publish_module
from minireason.loop import types as loop_types
from minireason.loop.publish import (
    CredentialInStagedDiff,
    GitOutcome,
    HistoryRewriteRefused,
    LocalGit,
    PublishError,
    PublishNotConverging,
    PublishPending,
    check_published,
    publish,
    verify_published,
)

#: A fixed, meaningless literal. It is not a credential; it is registered under
#: a test-only environment name so the module's real scanner has something to
#: find. No real key is read, written or referenced anywhere in this file.
PLANTED = "loop-publish-test-not-a-real-credential-0000"
PLANTED_ENV = "LOOP_PUBLISH_TEST_KEY"

VERIFIED_RE = re.compile(
    r"^VERIFIED (?P<commit>[0-9a-f]{40}) TREE (?P<tree>[0-9a-f]{40}) "
    r"at \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z "
    r"local=(?P<local>[0-9a-f]{40}) remote=(?P<remote>[0-9a-f]{40}) "
    r"ref=(?P<ref>\S+) paths=(?P<paths>\d+)$"
)

FORCE_TOKENS = ("--force", "--force-with-lease", "--force-if-includes", "-f", "--delete", "--amend")
SWEEPING_TOKENS = ("-A", "--all", "-a", ".", ":/", "*")


class RecordingGit(LocalGit):
    """Real git, with every argv recorded and an optional post-push hook."""

    def __init__(self, repo, *, after_push: Callable[[], None] | None = None, **kwargs) -> None:
        super().__init__(repo, **kwargs)
        self.argv: list[tuple[str, ...]] = []
        self.after_push = after_push

    def _invoke(self, tokens: Sequence[str]) -> GitOutcome:
        self.argv.append(tuple(str(token) for token in tokens))
        outcome = super()._invoke(tokens)
        if tokens and tokens[0] == "push" and outcome.ok and self.after_push is not None:
            self.after_push()
        return outcome

    def pushes(self) -> list[tuple[str, ...]]:
        return [row for row in self.argv if row and row[0] == "push"]


class FailingPushGit(LocalGit):
    """Real git for everything except the first ``failures`` pushes."""

    def __init__(self, repo, *, failures: int, timed_out: bool = False, **kwargs) -> None:
        super().__init__(repo, **kwargs)
        self.remaining = failures
        self.timed_out = timed_out
        self.argv: list[tuple[str, ...]] = []

    def _invoke(self, tokens: Sequence[str]) -> GitOutcome:
        self.argv.append(tuple(str(token) for token in tokens))
        if tokens and tokens[0] == "push" and self.remaining > 0:
            self.remaining -= 1
            if self.timed_out:
                return GitOutcome(-1, b"", b"", True, tuple(tokens))
            return GitOutcome(128, b"",
                              b"fatal: unable to access remote: Connection reset by peer",
                              False, tuple(tokens))
        return super()._invoke(tokens)


class PublishFixture(unittest.TestCase):
    """A real bare remote, a real clone, and one run directory to publish."""

    def raw(self, repo: Path, *args: str) -> str:
        """Plain git, bypassing the module, so a test can do what it refuses."""

        done = subprocess.run(["git", "-C", str(repo), *args], cwd=str(repo),
                              capture_output=True, check=True)
        return done.stdout.decode("utf-8").strip()

    def setUp(self) -> None:
        compat._reset_registered_secret_envs()
        self.addCleanup(compat._reset_registered_secret_envs)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.remote = self.root / "remote.git"
        self.repo = self.root / "checkout"
        self.raw(self.root, "init", "--bare", "--initial-branch=main", str(self.remote))
        self.raw(self.root, "init", "--initial-branch=main", str(self.repo))
        for key, value in (("user.name", "Loop Publish Test"),
                           ("user.email", "loop-publish@example.invalid"),
                           ("core.autocrlf", "false"), ("commit.gpgsign", "false")):
            self.raw(self.repo, "config", key, value)
        self.ledger = self.repo / "docs" / "DECISION_LEDGER.md"
        self.ledger.parent.mkdir(parents=True)
        self.ledger.write_bytes(b"# Decision ledger\n")
        self.raw(self.repo, "add", "--", "docs")
        self.raw(self.repo, "commit", "-m", "Initial publication fixture")
        self.raw(self.repo, "remote", "add", "origin", str(self.remote))
        self.raw(self.repo, "push", "--set-upstream", "origin", "HEAD:refs/heads/main")
        self.initial = self.raw(self.repo, "rev-parse", "HEAD")
        self.run_dir = self.repo / "experiments" / "loops" / "RUN-01"
        self.run_dir.mkdir(parents=True)
        self.ref = "origin/main"

    # -- helpers ---------------------------------------------------------- #

    def step(self, name: str = "0001-SEND.json", body: bytes = b'{"kind":"SEND"}\n') -> Path:
        path = self.run_dir / name
        path.write_bytes(body)
        return path

    def remote_head(self) -> str:
        return self.raw(self.remote, "rev-parse", "refs/heads/main")

    def rival_commit(self) -> str:
        """Advance the remote from a second clone, so our push is behind it."""

        other = self.root / "rival"
        subprocess.run(["git", "clone", "--quiet", "--branch", "main",
                        str(self.remote), str(other)], cwd=str(self.root), check=True,
                       capture_output=True)
        for key, value in (("user.name", "Rival Publisher"),
                           ("user.email", "rival@example.invalid"),
                           ("commit.gpgsign", "false")):
            self.raw(other, "config", key, value)
        (other / "rival.txt").write_bytes(b"a concurrent publisher\n")
        self.raw(other, "add", "--", "rival.txt")
        self.raw(other, "commit", "-m", "Concurrent remote advance")
        self.raw(other, "push", "origin", "HEAD:refs/heads/main")
        return self.raw(other, "rev-parse", "HEAD")

    def reauthor_remote_with_equal_tree(self) -> str:
        """What an authenticated connector does: a new commit, the same tree."""

        tree = self.raw(self.remote, "rev-parse", "refs/heads/main^{tree}")
        parent = self.raw(self.remote, "rev-parse", "refs/heads/main^")
        commit = self.raw(self.remote, "-c", "user.name=Connector",
                          "-c", "user.email=connector@example.invalid",
                          "commit-tree", tree, "-p", parent, "-m", "Connector re-authored")
        self.raw(self.remote, "update-ref", "refs/heads/main", commit)
        return commit

    def merge_the_remote(self) -> None:
        """The driver's reconciliation between two publish steps: never a rebase."""

        self.raw(self.repo, "fetch", "--no-tags", "origin", "refs/heads/main")
        self.raw(self.repo, "merge", "--no-edit", "FETCH_HEAD")


# ------------------------------------------------------------------------- #
# Acceptance: explicit paths only, never -A
# ------------------------------------------------------------------------- #

class ExplicitPathsTests(PublishFixture):

    def test_explicit_paths_only_never_dash_A(self) -> None:
        target = self.step()
        (self.repo / "stray.txt").write_bytes(b"an unrelated untracked file\n")
        self.ledger.write_bytes(b"# Decision ledger\nan unrelated tracked edit\n")
        git = RecordingGit(self.repo)

        result = publish(self.repo, [target], "Publish one step receipt", self.ref, git=git)

        self.assertTrue(result.published)
        adds = [row for row in git.argv if row and row[0] == "add"]
        self.assertEqual(adds, [("add", "--", "experiments/loops/RUN-01/0001-SEND.json")])
        for row in git.argv:
            for token in row:
                self.assertNotIn(token, SWEEPING_TOKENS, f"sweeping token in {row}")
        # The unrelated files are still unpublished, and the tracked edit that
        # was never named is still the old bytes on the remote.
        listing = self.raw(self.remote, "ls-tree", "-r", "--name-only", "refs/heads/main")
        self.assertNotIn("stray.txt", listing.split("\n"))
        stored = subprocess.run(["git", "-C", str(self.remote), "show",
                                 "refs/heads/main:docs/DECISION_LEDGER.md"],
                                cwd=str(self.remote), capture_output=True, check=True).stdout
        self.assertEqual(stored, b"# Decision ledger\n")

    def test_explicit_paths_only_never_dash_A_refuses_every_sweeping_spelling(self) -> None:
        self.step()
        for spelling, code in ((".", "PATH_IS_REPO_ROOT"), ("-A", "PATH_NOT_EXPLICIT"),
                               ("--all", "PATH_NOT_EXPLICIT"), (":/", "PATH_NOT_EXPLICIT"),
                               ("experiments/**/*.json", "PATH_NOT_EXPLICIT"),
                               ("../outside.txt", "PATH_OUTSIDE_REPO"),
                               ("experiments/loops/RUN-01/absent.json", "PATH_MISSING")):
            with self.subTest(spelling=spelling):
                with self.assertRaises(PublishError) as caught:
                    publish(self.repo, [spelling], "refused", self.ref)
                self.assertEqual(caught.exception.code, code)
        self.assertEqual(self.remote_head(), self.initial)

    def test_explicit_paths_only_never_dash_A_refuses_a_pre_staged_stranger(self) -> None:
        target = self.step()
        (self.repo / "stray.txt").write_bytes(b"staged by somebody else\n")
        self.raw(self.repo, "add", "--", "stray.txt")
        with self.assertRaises(PublishError) as caught:
            publish(self.repo, [target], "Publish one step receipt", self.ref)
        self.assertEqual(caught.exception.code, "UNEXPECTED_STAGED_FILES")
        self.assertEqual(self.remote_head(), self.initial)


# ------------------------------------------------------------------------- #
# Acceptance: push is non-forcing
# ------------------------------------------------------------------------- #

class NonForcingPushTests(PublishFixture):

    def test_push_is_non_forcing(self) -> None:
        target = self.step()
        git = RecordingGit(self.repo)

        result = publish(self.repo, [target], "Publish one step receipt", self.ref, git=git)

        self.assertTrue(result.published)
        self.assertEqual(git.pushes(),
                         [("push", "--porcelain", "--set-upstream", "origin",
                           "HEAD:refs/heads/main")])
        for row in git.argv:
            for token in row:
                self.assertNotIn(token, FORCE_TOKENS, f"force token in {row}")
                self.assertFalse(token.startswith("+"), f"force refspec in {row}")
        self.assertEqual(self.remote_head(), result.remote_commit)
        self.assertEqual(self.raw(self.repo, "rev-parse", "HEAD^"), self.initial)

    def test_push_is_non_forcing_and_history_rewrites_are_refused(self) -> None:
        head = self.raw(self.repo, "rev-parse", "HEAD")
        git = LocalGit(self.repo)
        for tokens in (("commit", "--amend", "-m", "rewritten"),
                       ("push", "--force", "origin", "HEAD:refs/heads/main"),
                       ("push", "-f", "origin", "HEAD:refs/heads/main"),
                       ("push", "--force-with-lease", "origin", "HEAD:refs/heads/main"),
                       ("push", "origin", "+HEAD:refs/heads/main"),
                       ("push", "--delete", "origin", "main"),
                       ("reset", "--hard", "HEAD~1"),
                       ("rebase", "origin/main"),
                       ("filter-branch", "--all"),
                       ("gc", "--prune=now"),
                       ("-c", "user.name=x", "commit", "--amend", "-m", "rewritten"),
                       ("checkout", "-f", "main")):
            with self.subTest(tokens=tokens):
                with self.assertRaises(HistoryRewriteRefused) as caught:
                    git.run(*tokens)
                self.assertEqual(caught.exception.code, "HISTORY_REWRITE_REFUSED")
                with self.assertRaises(HistoryRewriteRefused):
                    git.status(*tokens)
        self.assertEqual(self.raw(self.repo, "rev-parse", "HEAD"), head)
        self.assertEqual(self.remote_head(), self.initial)
        self.assertEqual(git.text("rev-parse", "HEAD"), head)


# ------------------------------------------------------------------------- #
# Acceptance: an equal-tree remote commit is accepted, both ids recorded
# ------------------------------------------------------------------------- #

class EqualTreeRemoteTests(PublishFixture):

    def test_an_equal_tree_remote_commit_is_accepted_with_both_commit_ids_recorded(self) -> None:
        target = self.step()
        git = RecordingGit(self.repo, after_push=self.reauthor_remote_with_equal_tree)

        result = publish(self.repo, [target], "Publish one step receipt", self.ref, git=git)

        self.assertTrue(result.published)
        self.assertTrue(result.distinct_remote_commit)
        self.assertEqual(result.local_commit, self.raw(self.repo, "rev-parse", "HEAD"))
        self.assertEqual(result.remote_commit, self.remote_head())
        self.assertNotEqual(result.local_commit, result.remote_commit)
        self.assertEqual(result.tree, self.raw(self.remote, "rev-parse", "refs/heads/main^{tree}"))
        match = VERIFIED_RE.match(result.verified_line or "")
        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(match.group("local"), result.local_commit)
        self.assertEqual(match.group("remote"), result.remote_commit)
        self.assertEqual(match.group("commit"), result.remote_commit)
        receipt = result.as_receipt()
        self.assertEqual(receipt["published_commit"], result.remote_commit)
        self.assertEqual(receipt["local_commit"], result.local_commit)
        self.assertTrue(verify_published(self.repo, [target], result.local_commit, self.ref))

    def test_an_equal_tree_remote_commit_is_accepted_but_a_different_tree_is_not(self) -> None:
        target = self.step()

        def advance() -> None:
            self.rival_commit()

        git = RecordingGit(self.repo, after_push=advance)
        result = publish(self.repo, [target], "Publish one step receipt", self.ref, git=git)

        self.assertFalse(result.published)
        assert result.pending is not None
        self.assertEqual(result.pending.reason, publish_module.REMOTE_NOT_CONFIRMED)
        for row in git.argv:
            for token in row:
                self.assertNotIn(token, FORCE_TOKENS)


# ------------------------------------------------------------------------- #
# Acceptance: a planted secret in the staged diff refuses the publish
# ------------------------------------------------------------------------- #

class CredentialScanTests(PublishFixture):

    def test_a_planted_secret_in_the_staged_diff_refuses_the_publish(self) -> None:
        target = self.step(body=b'{"note":"' + PLANTED.encode("ascii") + b'"}\n')
        with mock.patch.dict(os.environ, {PLANTED_ENV: PLANTED}):
            compat.register_secret_envs([PLANTED_ENV])
            with self.assertRaises(CredentialInStagedDiff) as caught:
                publish(self.repo, [target], "Publish one step receipt", self.ref)
            detail = caught.exception.detail
            self.assertIn(PLANTED_ENV, detail)
            self.assertNotIn(PLANTED, detail)
            self.assertNotIn(PLANTED, str(caught.exception))
            # Refused with the index still clean and nothing committed or pushed.
            self.assertEqual(self.raw(self.repo, "diff", "--cached", "--name-only"), "")
            self.assertEqual(self.raw(self.repo, "rev-parse", "HEAD"), self.initial)
            self.assertEqual(self.remote_head(), self.initial)
            # The same refusal over a staged diff's text, which is where the
            # design places the scan.
            with self.assertRaises(CredentialInStagedDiff):
                publish_module._refuse_credential_text(
                    "+++ b/x\n+" + PLANTED + "\n", "staged diff")

    def test_a_planted_secret_in_the_staged_diff_refuses_the_publish_from_a_subdirectory(self) -> None:
        nested = self.run_dir / "readings" / "row-01"
        nested.mkdir(parents=True)
        (nested / "clean.json").write_bytes(b"{}\n")
        (nested / "dirty.json").write_bytes(PLANTED.encode("ascii") + b"\n")
        with mock.patch.dict(os.environ, {PLANTED_ENV: PLANTED}):
            compat.register_secret_envs([PLANTED_ENV])
            with self.assertRaises(CredentialInStagedDiff):
                publish(self.repo, [self.run_dir], "Publish the run tree", self.ref)
        self.assertEqual(self.remote_head(), self.initial)

    def test_the_git_child_environment_carries_no_credential(self) -> None:
        with mock.patch.dict(os.environ, {PLANTED_ENV: PLANTED, "DEEPSEEK_API_KEY": PLANTED,
                                          "OLLAMA_API_KEY": PLANTED}):
            compat.register_secret_envs([PLANTED_ENV])
            environment = LocalGit(self.repo).environment()
        for name in (PLANTED_ENV, "DEEPSEEK_API_KEY", "OLLAMA_API_KEY"):
            self.assertNotIn(name, environment)
        self.assertNotIn(PLANTED, "".join(environment.values()))


# ------------------------------------------------------------------------- #
# Acceptance: a timed-out or rejected push returns PublishPending and is
# retried only as a new publish
# ------------------------------------------------------------------------- #

class PendingPublicationTests(PublishFixture):

    def test_a_rejected_push_returns_PublishPending_and_is_retried_only_as_a_new_publish(self) -> None:
        rival = self.rival_commit()
        target = self.step()
        sleeps: list[float] = []
        git = RecordingGit(self.repo)

        first = publish(self.repo, [target], "Publish one step receipt", self.ref,
                        attempt=1, git=git, sleep=sleeps.append)

        self.assertFalse(first.published)
        self.assertEqual(first.status, publish_module.PENDING)
        self.assertIsInstance(first.pending, PublishPending)
        assert first.pending is not None
        self.assertEqual(first.pending.reason, publish_module.PUSH_REJECTED)
        self.assertEqual(first.pending.attempt, 1)
        self.assertIsNone(first.verified_line)
        # A rejection is a divergence, not a transient: no backoff, no retry
        # inside the step, one push on the wire, and no force anywhere.
        self.assertEqual(sleeps, [])
        self.assertEqual(len(git.pushes()), 1)
        for row in git.argv:
            for token in row:
                self.assertNotIn(token, FORCE_TOKENS)
                self.assertFalse(token.startswith("+"))
        self.assertEqual(self.remote_head(), rival)

        # The driver re-fetches and reconciles, then publishes again as a NEW
        # step. Nothing is rewritten: the rival commit is still an ancestor.
        self.merge_the_remote()
        second = publish(self.repo, [target], "Publish one step receipt", self.ref,
                         attempt=2, git=git, sleep=sleeps.append)
        self.assertTrue(second.published)
        self.assertEqual(second.attempt, 2)
        self.assertFalse(second.committed)
        self.assertEqual(sleeps, [])
        self.assertEqual(self.remote_head(), second.remote_commit)
        self.assertEqual(subprocess.run(["git", "-C", str(self.repo), "merge-base",
                                         "--is-ancestor", rival, str(second.remote_commit)],
                                        cwd=str(self.repo), capture_output=True).returncode, 0)

    def test_a_timed_out_push_returns_PublishPending_and_is_retried_only_as_a_new_publish(self) -> None:
        target = self.step()
        sleeps: list[float] = []
        git = FailingPushGit(self.repo, failures=10, timed_out=True)

        first = publish(self.repo, [target], "Publish one step receipt", self.ref,
                        attempt=1, git=git, sleep=sleeps.append)

        self.assertFalse(first.published)
        assert first.pending is not None
        self.assertEqual(first.pending.reason, publish_module.PUSH_TIMEOUT)
        # Item 45(b): PENDING on the FIRST timeout, with no backoff at all. A
        # push that timed out may have landed, so a second push is a second act
        # on an unknown remote state, not a retry of a failed one.
        self.assertEqual(sleeps, [])
        self.assertEqual(self.remote_head(), self.initial)
        self.assertIsNone(first.verified_line)
        self.assertTrue(first.committed)

        second = publish(self.repo, [target], "Publish one step receipt", self.ref,
                         attempt=2, sleep=sleeps.append)
        self.assertTrue(second.published)
        self.assertEqual(second.attempt, 2)
        self.assertEqual(self.remote_head(), second.remote_commit)

    def test_a_network_failure_retries_on_the_exponential_backoff_2_4_8_16(self) -> None:
        target = self.step()
        sleeps: list[float] = []
        git = FailingPushGit(self.repo, failures=2)

        result = publish(self.repo, [target], "Publish one step receipt", self.ref,
                         git=git, sleep=sleeps.append)

        self.assertTrue(result.published)
        self.assertEqual(sleeps, [2.0, 4.0])

        other = self.step(name="0002-SEND.json")
        sleeps.clear()
        always = FailingPushGit(self.repo, failures=99)
        pending = publish(self.repo, [other], "Publish a second receipt", self.ref,
                          git=always, sleep=sleeps.append)
        self.assertFalse(pending.published)
        assert pending.pending is not None
        self.assertEqual(pending.pending.reason, publish_module.PUSH_TRANSPORT)
        self.assertEqual(sleeps, [2.0, 4.0, 8.0, 16.0])


# ------------------------------------------------------------------------- #
# Acceptance: three non-converging attempts raise
# ------------------------------------------------------------------------- #

class ConvergenceTests(PublishFixture):

    def test_three_non_converging_attempts_raise(self) -> None:
        rival = self.rival_commit()
        target = self.step()
        sleeps: list[float] = []

        first = publish(self.repo, [target], "Publish one step receipt", self.ref,
                        attempt=1, sleep=sleeps.append)
        second = publish(self.repo, [target], "Publish one step receipt", self.ref,
                         attempt=2, sleep=sleeps.append)
        self.assertEqual((first.status, second.status),
                         (publish_module.PENDING, publish_module.PENDING))

        with self.assertRaises(PublishNotConverging) as caught:
            publish(self.repo, [target], "Publish one step receipt", self.ref,
                    attempt=3, sleep=sleeps.append)
        self.assertEqual(caught.exception.code, "PUBLISH_NOT_CONVERGING")
        self.assertIn(publish_module.PUSH_REJECTED, caught.exception.detail)

        with self.assertRaises(PublishNotConverging):
            publish(self.repo, [target], "Publish one step receipt", self.ref, attempt=4)
        for bad in (0, -1, "2", True):
            with self.assertRaises(PublishError):
                publish(self.repo, [target], "Publish one step receipt", self.ref, attempt=bad)
        self.assertEqual(self.remote_head(), rival)


# ------------------------------------------------------------------------- #
# The driver's contract: the VERIFIED line, read-back, and the dispatch gate
# ------------------------------------------------------------------------- #

class VerifiedLineTests(PublishFixture):

    def test_the_VERIFIED_line_is_returned_and_never_written(self) -> None:
        target = self.step()
        before = {path: path.read_bytes() for path in self.repo.rglob("*")
                  if path.is_file() and ".git" not in path.relative_to(self.repo).parts}
        moment = publish_module.datetime(2026, 9, 14, 12, 34, 56,
                                         tzinfo=publish_module.timezone.utc)

        result = publish(self.repo, [target], "Publish one step receipt", self.ref,
                         now=lambda: moment)

        match = VERIFIED_RE.match(result.verified_line or "")
        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(match.group("commit"), result.remote_commit)
        self.assertEqual(match.group("local"), match.group("remote"))
        self.assertEqual(match.group("tree"), result.tree)
        self.assertEqual(match.group("ref"), "origin/main")
        self.assertEqual(match.group("paths"), "1")
        self.assertIn("at 2026-09-14T12:34:56Z", result.verified_line or "")
        after = {path: path.read_bytes() for path in self.repo.rglob("*")
                 if path.is_file() and ".git" not in path.relative_to(self.repo).parts}
        self.assertEqual(before, after)
        for path, data in after.items():
            self.assertNotIn(b"VERIFIED ", data, f"a VERIFIED line was written to {path}")

    def test_verify_published_compares_the_remote_bytes_of_every_named_path(self) -> None:
        target = self.step()
        result = publish(self.repo, [target], "Publish one step receipt", self.ref)

        self.assertTrue(verify_published(self.repo, [target], result.local_commit, self.ref))
        self.assertTrue(verify_published(self.repo, [self.run_dir], result.local_commit, self.ref))
        self.assertFalse(verify_published(self.repo, [target], self.initial, self.ref))
        self.assertFalse(verify_published(self.repo, [target], "0" * 40, self.ref))

        # N4: the question is about a COMMIT's tree, not about the files on disk.
        # Editing the working tree does not unpublish the commit that was
        # published; ``check_published`` is the predicate that asks about bytes.
        target.write_bytes(b'{"kind":"SEND","edited":true}\n')
        self.assertTrue(verify_published(self.repo, [target], result.local_commit, self.ref))
        self.assertFalse(check_published(self.repo, target, self.ref))
        # A commit whose tree is genuinely not on the ref is still False, and a
        # path the published commit does not carry is still False.
        self.assertFalse(verify_published(self.repo, [target], self.initial, self.ref))

    def test_check_published_is_the_publication_before_dispatch_predicate(self) -> None:
        target = self.step()
        self.assertFalse(check_published(self.repo, target, self.ref))

        result = publish(self.repo, [target], "Publish one step receipt", self.ref)
        self.assertTrue(check_published(self.repo, target, self.ref))
        self.assertTrue(check_published(self.repo, self.run_dir, self.ref))
        self.assertTrue(check_published(self.repo, result.local_commit, self.ref))
        self.assertFalse(check_published(self.repo, "0" * 40, self.ref))

        target.write_bytes(b'{"kind":"SEND","edited":true}\n')
        self.assertFalse(check_published(self.repo, target, self.ref))

        later = self.step(name="0002-SEND.json")
        second = publish(self.repo, [target, later], "Publish two step receipts", self.ref)
        self.assertTrue(check_published(self.repo, second.local_commit, self.ref))
        self.assertTrue(check_published(self.repo, result.local_commit, self.ref))

        with self.assertRaises(PublishError) as caught:
            check_published(self.repo, "experiments/loops/RUN-01/absent.json", self.ref)
        self.assertEqual(caught.exception.code, "CHECK_TARGET_UNKNOWN")

    def test_the_publish_ref_defaults_to_the_branch_upstream_and_refuses_a_bad_ref(self) -> None:
        target = self.step()
        result = publish(self.repo, [target], "Publish one step receipt")
        self.assertTrue(result.published)
        self.assertEqual(result.ref, "origin/main")
        self.assertEqual(publish_module.upstream_ref(self.repo), "origin/main")
        self.assertEqual(publish_module.split_publish_ref("origin/feature/x"),
                         ("origin", "refs/heads/feature/x"))
        for bad in ("origin", "/main", "origin/", "origin/../main", ""):
            with self.assertRaises(PublishError) as caught:
                publish_module.split_publish_ref(bad)
            self.assertEqual(caught.exception.code, "PUBLISH_REF_INVALID")

    def test_every_git_invocation_carries_an_explicit_cwd_and_an_explicit_dash_C(self) -> None:
        target = self.step()
        seen: list[tuple[tuple[str, ...], str | None]] = []
        real = subprocess.run

        def recorder(argv, *args, **kwargs):
            seen.append((tuple(str(token) for token in argv), kwargs.get("cwd")))
            return real(argv, *args, **kwargs)

        with mock.patch.object(publish_module.subprocess, "run", recorder):
            result = publish(self.repo, [target], "Publish one step receipt", self.ref)

        self.assertTrue(result.published)
        self.assertTrue(seen)
        expected = str(self.repo.resolve())
        for argv, cwd in seen:
            # --literal-pathspecs on every argv (item 43): a caller's path names
            # the file it spells and never a wildmatch pattern.
            self.assertEqual(argv[:4], ("git", "--literal-pathspecs", "-C", expected))
            self.assertEqual(cwd, expected)


# ------------------------------------------------------------------------- #
# Acceptance: the argv guard is an allow-list, and the module lives inside it
# ------------------------------------------------------------------------- #

class TheArgvGuardIsAnAllowList(PublishFixture):
    """B1: the deny-list passed eight destructive argvs.

    ``LocalGit`` is the published seam every later wave uses, and its docstring
    is the reason a W1 author will not add a second guard. Each argv below
    deletes, moves or discards a recorded ref; none of them was refused before.
    """

    #: Each one is refused, and ``push -d`` and ``update-ref -d`` are named
    #: because they are the two the deny-list came closest to catching: ``-d`` is
    #: the short form of the ``--delete`` it already listed.
    DESTRUCTIVE = (
        ("push", "-d", "origin", "claude/project-state-direction-j5rbun"),
        ("push", "--delete", "origin", "main"),
        ("push", "--mirror", "origin"),
        ("push", "--prune", "origin", "HEAD:refs/heads/main"),
        ("push", "--prune-tags", "origin", "HEAD:refs/heads/main"),
        ("update-ref", "-d", "refs/heads/main"),
        ("update-ref", "refs/heads/main", "0" * 40),
        ("branch", "-D", "main"),
        ("branch", "-d", "main"),
        ("branch", "-f", "main", "HEAD~1"),
        ("tag", "-d", "v1"),
        ("stash", "push"),
        ("stash", "drop"),
        ("checkout", "--orphan", "fresh"),
        ("switch", "-C", "main"),
        ("symbolic-ref", "HEAD", "refs/heads/other"),
        ("worktree", "add", "../elsewhere"),
        ("clean", "-fdx"),
        ("rm", "-r", "--cached", "docs"),
        ("update-index", "--force-remove", "docs/DECISION_LEDGER.md"),
        ("cherry-pick", "HEAD~1"),
        ("am", "--abort"),
        ("notes", "prune"),
        ("remote", "remove", "origin"),
    )

    def test_every_destructive_argv_is_refused_before_a_process_is_spawned(self) -> None:
        head = self.raw(self.repo, "rev-parse", "HEAD")
        git = LocalGit(self.repo)
        spawned: list[tuple[str, ...]] = []
        real = subprocess.run

        def recorder(argv, *args, **kwargs):
            spawned.append(tuple(str(token) for token in argv))
            return real(argv, *args, **kwargs)

        self.assertGreaterEqual(len(self.DESTRUCTIVE), 12)
        with mock.patch.object(publish_module.subprocess, "run", recorder):
            for tokens in self.DESTRUCTIVE:
                with self.subTest(tokens=" ".join(tokens)):
                    with self.assertRaises(HistoryRewriteRefused) as caught:
                        git.run(*tokens)
                    self.assertIn(caught.exception.code,
                                  ("HISTORY_REWRITE_REFUSED", "GIT_SUBCOMMAND_NOT_ALLOWED"))
                    self.assertIn(caught.exception.code, loop_types.FAILURE_CODES)
                    with self.assertRaises(HistoryRewriteRefused):
                        git.status(*tokens)
        self.assertEqual(spawned, [], "a refused argv reached a subprocess")
        self.assertEqual(self.raw(self.repo, "rev-parse", "HEAD"), head)
        self.assertEqual(self.remote_head(), self.initial)

    def test_push_dash_d_and_update_ref_dash_d_are_named_and_refused(self) -> None:
        git = LocalGit(self.repo)
        for tokens in (("push", "-d", "origin", "main"),
                       ("update-ref", "-d", "refs/heads/main")):
            with self.subTest(tokens=" ".join(tokens)):
                with self.assertRaises(HistoryRewriteRefused) as caught:
                    git.run(*tokens)
                self.assertEqual(caught.exception.code, "HISTORY_REWRITE_REFUSED")
        self.assertIn("-d", publish_module.REWRITING_FLAGS)
        self.assertIn("--mirror", publish_module.REWRITING_FLAGS)
        self.assertIn("--prune", publish_module.REWRITING_FLAGS)
        self.assertIn("--prune-tags", publish_module.REWRITING_FLAGS)
        self.assertIn("-D", publish_module.REWRITING_FLAGS)
        self.assertNotIn("update-ref", publish_module.ALLOWED_SUBCOMMANDS)

    def test_a_subcommand_this_module_does_not_need_names_its_own_code(self) -> None:
        git = LocalGit(self.repo)
        with self.assertRaises(publish_module.GitSubcommandNotAllowed) as caught:
            git.run("symbolic-ref", "HEAD", "refs/heads/other")
        self.assertEqual(caught.exception.code, "GIT_SUBCOMMAND_NOT_ALLOWED")
        # A caller written against the published exception still catches it.
        self.assertIsInstance(caught.exception, HistoryRewriteRefused)
        self.assertIsInstance(caught.exception, PublishError)
        # ... and a genuine rewrite still says that it was a rewrite.
        with self.assertRaises(HistoryRewriteRefused) as rewrite:
            git.run("reset", "--hard", "HEAD~1")
        self.assertEqual(rewrite.exception.code, "HISTORY_REWRITE_REFUSED")

    def test_every_argv_the_module_emits_is_on_the_allow_list(self) -> None:
        """The other direction: the list is no wider than the module's own need."""

        target = self.step()
        git = RecordingGit(self.repo)
        result = publish(self.repo, [target], "Publish one step receipt", self.ref,
                         git=git)
        self.assertTrue(result.published)
        self.assertTrue(verify_published(self.repo, [target], result.local_commit,
                                         self.ref, git=git))
        self.assertTrue(check_published(self.repo, target, self.ref, git=git))
        self.assertTrue(check_published(self.repo, result.local_commit, self.ref, git=git))
        self.assertFalse(check_published(self.repo, "0" * 40, self.ref, git=git))
        publish_module.upstream_ref(self.repo, git=git)

        # A rejected publication, so the pending path's argvs are recorded too.
        rival = RecordingGit(self.repo)
        self.rival_commit()
        later = self.step(name="0002-SEND.json")
        pending = publish(self.repo, [later], "Publish a second receipt", self.ref,
                          attempt=1, git=rival, sleep=lambda _s: None)
        self.assertFalse(pending.published)

        emitted = git.argv + rival.argv
        self.assertTrue(emitted)
        seen = set()
        for row in emitted:
            subcommand = publish_module._subcommand(row)
            seen.add(subcommand)
            with self.subTest(argv=" ".join(row)):
                self.assertIn(subcommand, publish_module.ALLOWED_SUBCOMMANDS)
                self.assertIsNone(publish_module._refuse_history_rewrite(row))
        # The allow-list is not padded with subcommands nothing uses: every entry
        # is either emitted here or named in the module for a path this fixture
        # cannot reach (a bare repository has no status to read).
        self.assertLessEqual(publish_module.ALLOWED_SUBCOMMANDS - seen,
                             {"cat-file", "rev-list", "status"})


class ImportingTheModuleLoadsNoEndpointRegistry(unittest.TestCase):
    """N3: importing a publisher has no business reading endpoints.json."""

    def test_importing_publish_does_not_import_the_transport(self) -> None:
        probe = (
            "import sys\n"
            "sys.path.insert(0, sys.argv[1])\n"
            "import minireason.loop.publish\n"
            "print('minireason.provider_openai_compat' in sys.modules)\n"
        )
        root = Path(__file__).resolve().parents[2] / "src"
        done = subprocess.run([sys.executable, "-X", "utf8", "-c", probe, str(root)],
                              capture_output=True, text=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(done.stdout.strip(), "False", done.stdout)


class HardeningFindings(PublishFixture):
    """One test per item of the wave-1 integration decisions, items 43-46."""

    def test_item43_a_bracketed_path_never_reaches_git_as_a_pathspec(self):
        """Item 43: ``publish(["report[1].md"])`` also published ``report1.md``.

        The neighbour was staged, committed and pushed; the working-tree
        credential scan never read it, and a planted credential reached the
        remote inside it.
        """

        named = self.run_dir / "report[1].md"
        named.write_bytes(b"the file the caller named\n")
        neighbour = self.run_dir / "report1.md"
        # The planted line is an ENV NAME with an unmistakably synthetic value.
        # ``publish``'s scanner compares the environment's real values, never a
        # shape, so nothing here depends on the value looking key-like - and a
        # test file that carries a key-shaped literal is a file every future
        # credential gate has to be told to ignore. No ``sk-`` prefix, no hex
        # run, no digit run: the word SYNTHETIC is the whole value.
        neighbour.write_bytes(
            b"DEEPSEEK_API_KEY=SYNTHETIC-TEST-VALUE-NOT-A-CREDENTIAL\n")
        with self.assertRaises(PublishError) as caught:
            publish(self.repo, [named], "Publish the named report", self.ref)
        self.assertEqual(caught.exception.code, "PATH_NOT_EXPLICIT")
        self.assertEqual(self.remote_head(), self.initial)
        for magic in ("a*.md", "a?.md", "a[1].md", "a]x.md", "a\\b.md"):
            with self.subTest(path=magic):
                with self.assertRaises(PublishError) as caught:
                    publish(self.repo, [self.run_dir / magic], "m", self.ref)
                self.assertEqual(caught.exception.code, "PATH_NOT_EXPLICIT")

    def test_item43_what_is_scanned_is_what_git_would_stage(self):
        target = self.step()
        git = publish_module.LocalGit(self.repo)
        self.assertEqual(
            set(publish_module._scan_set(git, [str(target.relative_to(self.repo))])),
            {str(target.relative_to(self.repo))})
        # An ignored neighbour is neither staged nor scanned ...
        (self.repo / ".gitignore").write_bytes(b"experiments/loops/RUN-01/ignored.txt\n")
        (self.run_dir / "ignored.txt").write_bytes(b"not published\n")
        scanned = publish_module._scan_set(git, ["experiments/loops/RUN-01"])
        self.assertNotIn("experiments/loops/RUN-01/ignored.txt", scanned)
        self.assertIn("experiments/loops/RUN-01/0001-SEND.json", scanned)
        # ... and a nested checkout's own config is never read by the walk.
        nested = self.run_dir / "nested" / ".git"
        nested.mkdir(parents=True)
        (nested / "config").write_bytes(b"[remote]\n url = https://u:pw@example.invalid\n")
        walked = publish_module._walk_files(self.repo, ["experiments/loops/RUN-01"])
        self.assertNotIn("experiments/loops/RUN-01/nested/.git/config", walked)

    def test_item44_a_rewriting_flag_is_refused_however_it_is_spelled(self):
        """Item 44: an exact-token comparison let four spellings through."""

        git = publish_module.LocalGit(self.repo)
        before = self.remote_head()
        spellings = (
            ["push", "--force-with-lease=refs/heads/main:" + "0" * 40, "origin",
             "HEAD:refs/heads/main"],
            ["push", "--force-with-lease", "origin", "HEAD:refs/heads/main"],
            ["push", "--force=x", "origin", "HEAD:refs/heads/main"],
            ["commit", "--amen", "-m", "x"],
            ["commit", "--amend", "-m", "x"],
            ["add", "-A"],
            ["add", "--all"],
            ["commit", "-a", "-m", "x"],
            ["commit", "--all", "-m", "x"],
            ["push", "--delete=x", "origin", "main"],
            ["push", "--mirro", "origin"],
        )
        for tokens in spellings:
            with self.subTest(argv=" ".join(tokens)):
                with self.assertRaises(HistoryRewriteRefused):
                    git.status(*tokens)
                self.assertEqual(self.remote_head(), before,
                                 "the bare remote moved on a refused argv")

    def test_item44_a_commit_message_is_a_message_and_not_an_option(self):
        target = self.step()
        result = publish(self.repo, [target], "--amend the published record", self.ref)
        self.assertTrue(result.published)
        self.assertIn("--amend the published record",
                      self.raw(self.repo, "log", "-1", "--pretty=%s"))

    def test_item45a_a_read_back_that_cannot_run_is_pending_not_an_exception(self):
        target = self.step()

        class BlindAfterPush(publish_module.LocalGit):
            def _invoke(self, tokens):
                if tokens and tokens[0] == "ls-remote":
                    return publish_module.GitOutcome(
                        1, b"", b"ssh: connect to host example.invalid: timed out",
                        False, tuple(tokens))
                return super()._invoke(tokens)

        result = publish(self.repo, [target], "Publish one step receipt", self.ref,
                         git=BlindAfterPush(self.repo))
        self.assertFalse(result.published)
        assert result.pending is not None
        self.assertEqual(result.pending.reason, publish_module.REMOTE_NOT_CONFIRMED)
        # The push DID land, which is exactly why this may not raise.
        self.assertNotEqual(self.remote_head(), self.initial)
        self.assertIsNone(result.as_receipt()["published_commit"])
        self.assertIsNotNone(result.as_receipt()["pending_detail"])

    def test_item45c_a_commit_that_removes_a_credential_is_publishable(self):
        secret = "SYNTHETIC-LOOP-TEST-VALUE-NOT-A-CREDENTIAL"
        compat.register_secret_envs(["LOOP_PUBLISH_TEST_KEY"])
        with mock.patch.dict(os.environ, {"LOOP_PUBLISH_TEST_KEY": secret}):
            leaked = self.run_dir / "leaked.txt"
            leaked.write_bytes(f"key={secret}\n".encode("utf-8"))
            self.raw(self.repo, "add", "--", str(leaked.relative_to(self.repo)))
            self.raw(self.repo, "commit", "-m", "The leak, already in HEAD")
            # The repair: the credential leaves the tree.
            leaked.write_bytes(b"key=REDACTED\n")
            result = publish(self.repo, [leaked], "Remove the leaked key", self.ref)
        self.assertTrue(result.published)

    def test_item45c_a_credential_in_a_path_name_is_refused(self):
        secret = "SYNTHETIC-LOOP-TEST-VALUE-NOT-A-CREDENTIAL"
        compat.register_secret_envs(["LOOP_PUBLISH_TEST_KEY"])
        with mock.patch.dict(os.environ, {"LOOP_PUBLISH_TEST_KEY": secret}):
            named = self.run_dir / f"key-{secret}.json"
            named.write_bytes(b"{}\n")
            with self.assertRaises(CredentialInStagedDiff):
                publish(self.repo, [named], "Publish a badly named file", self.ref)
        self.assertEqual(self.remote_head(), self.initial)

    def test_item45e_a_non_utf8_path_name_is_refused_before_the_add(self):
        raw = os.fsdecode(b"experiments/loops/RUN-01/\xff\xfe.json")
        (self.repo / raw).write_bytes(b"{}\n")
        with self.assertRaises(PublishError) as caught:
            publish(self.repo, [raw.encode("utf-8", "surrogateescape")],
                    "Publish an undecodable name", self.ref)
        self.assertEqual(caught.exception.code, "PATH_NOT_EXPLICIT")
        self.assertEqual(self.remote_head(), self.initial)

    def test_item46_the_allowed_subcommands_are_exactly_what_is_emitted(self):
        target = self.step()
        seen: set[str] = set()
        real = publish_module.LocalGit._invoke

        def record(self_git, tokens):
            seen.add(publish_module._subcommand(tokens))
            return real(self_git, tokens)

        with mock.patch.object(publish_module.LocalGit, "_invoke", record):
            result = publish(self.repo, [target], "Publish one step receipt", self.ref)
            self.assertTrue(result.published)
            publish_module.verify_published(self.repo, [target], result.remote_commit,
                                            self.ref)
            publish_module.check_published(self.repo, target, ref=self.ref)
            # The other branch of check_published: a commit id, which is the
            # only caller of ``merge-base``.
            publish_module.check_published(self.repo, self.initial, ref=self.ref)
        self.assertLessEqual(seen, set(publish_module.ALLOWED_SUBCOMMANDS))
        self.assertEqual(set(publish_module.ALLOWED_SUBCOMMANDS) - seen, set(),
                         "the allow-list names a subcommand nothing here emits")

    def test_item46_the_child_environment_excludes_every_secret_name(self):
        git = publish_module.LocalGit(self.repo)
        compat.register_secret_envs(["LOOP_PUBLISH_TEST_KEY"])
        names = set(publish_module._credential_env_names())
        self.assertLessEqual(set(compat._secret_env_names()), names)
        with mock.patch.dict(os.environ, {name: "x" for name in names}):
            child = git.environment()
        for name in names:
            self.assertNotIn(name, child)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
