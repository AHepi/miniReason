"""Acceptance tests for ``minireason.loop.steps`` (wave plan W1-STEPS).

Every test is named after the clause of the module's acceptance list it
discharges. Nothing is simulated away: the run tree is a real directory under
``tempfile``, the publication steps run through :func:`publish` against a real
temporary bare repository exactly as ``tests/loop/test_publish.py`` does, and a
"kill" is a step ledger that is abandoned mid-step and a *new* ledger opened
over the same directory - which is what resume actually sees.

No network, no provider call, no credential: the only clocks are injected and
the only bytes written are digests, receipts and one VERIFIED line.
"""
from __future__ import annotations

import json
import re
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from minireason import provider_openai_compat as compat
from minireason.loop import custody, receipts
from minireason.loop import steps as steps_module
from minireason.loop.publish import GitOutcome, LocalGit, PublishPending, PublishResult, publish
from minireason.loop.steps import (
    CUSTODY_HALT_CODES,
    MARKER_KEPT_CODES,
    NEW_CODES,
    PUBLICATION_STEPS,
    PublishBlocked,
    RunLock,
    RunLocked,
    StepError,
    StepLedger,
    StepNondeterministic,
    StepTimeout,
    StickyHalt,
    UnresolvedStep,
    completed_coordinates,
    scan_coordinates,
)
from minireason.loop.types import (
    FAILURE_CODES,
    LoopError,
    REPLAYABLE_STEPS,
    SPENDING_STEPS,
    StepReceipt,
    TimeoutsConfig,
    run_paths,
)

#: A stand-in plan identity. Any 64-hex string is a well-formed one; the
#: ledger never interprets it, it only refuses a receipt written under another.
PLAN_ID = "a" * 64
OTHER_PLAN_ID = "b" * 64

BASE_MOMENT = datetime(2026, 9, 14, 12, 0, 0, tzinfo=timezone.utc)


class Clock:
    """A tz-aware clock that advances one second per look."""

    def __init__(self, start: datetime = BASE_MOMENT) -> None:
        self.moment = start

    def __call__(self) -> datetime:
        self.moment = self.moment + timedelta(seconds=1)
        return self.moment


class Monotonic:
    """A monotonic seam a test can jump forward by hand."""

    def __init__(self) -> None:
        self.value = 0.0

    def __call__(self) -> float:
        return self.value

    def jump(self, seconds: float) -> None:
        self.value += seconds


class LedgerFixture(unittest.TestCase):
    """One run tree under ``tempfile``, and a ledger over it."""

    def setUp(self) -> None:
        compat._reset_registered_secret_envs()
        self.addCleanup(compat._reset_registered_secret_envs)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo_root = Path(self.temp.name) / "checkout"
        self.paths = run_paths(self.repo_root, "RUN-01")
        self.paths.run_root.mkdir(parents=True)
        self.ledger_file = self.repo_root / "docs" / "DECISION_LEDGER.md"
        self.ledger_file.parent.mkdir(parents=True, exist_ok=True)
        self.ledger_file.write_bytes(b"# Decision ledger\n")
        self.clock = Clock()
        self.monotonic = Monotonic()

    def build(self, *, plan_id: str = PLAN_ID,
              timeouts: TimeoutsConfig | None = None,
              with_ledger: bool = False) -> StepLedger:
        return StepLedger(
            self.paths.run_root, plan_id, timeouts=timeouts,
            ledger_path=self.ledger_file if with_ledger else None,
            receipt_id="REC-20260914-A" if with_ledger else None,
            clock=self.clock, monotonic=self.monotonic)

    # -- helpers ---------------------------------------------------------- #

    def step_files(self) -> list[str]:
        directory = self.paths.steps
        return sorted(path.name for path in directory.iterdir()) \
            if directory.is_dir() else []

    def receipt_body(self, index: int, kind: str) -> dict:
        raw = self.paths.step_path(index, kind).read_bytes()
        return json.loads(raw.decode("utf-8"))


# ------------------------------------------------------------------------- #
# The happy path: S0 .. S3 over a real bare remote
# ------------------------------------------------------------------------- #

class TheHappyPathWalksSZeroToSThree(unittest.TestCase):
    """S0 PREREGISTER, S1 PREFLIGHT, S2 PUBLISH_PLAN, S3 CYCLE_OPEN."""

    def raw(self, repo: Path, *args: str) -> str:
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
        for key, value in (("user.name", "Loop Steps Test"),
                           ("user.email", "loop-steps@example.invalid"),
                           ("core.autocrlf", "false"), ("commit.gpgsign", "false")):
            self.raw(self.repo, "config", key, value)
        self.ledger_file = self.repo / "docs" / "DECISION_LEDGER.md"
        self.ledger_file.parent.mkdir(parents=True)
        self.ledger_file.write_bytes(b"# Decision ledger\n")
        self.raw(self.repo, "add", "--", "docs")
        self.raw(self.repo, "commit", "-m", "Initial step-ledger fixture")
        self.raw(self.repo, "remote", "add", "origin", str(self.remote))
        self.raw(self.repo, "push", "--set-upstream", "origin", "HEAD:refs/heads/main")
        self.paths = run_paths(self.repo, "RUN-01")
        self.paths.run_root.mkdir(parents=True)
        self.clock = Clock()
        self.ledger = StepLedger(self.paths.run_root, PLAN_ID,
                                 ledger_path=self.ledger_file,
                                 receipt_id="REC-20260914-A", clock=self.clock,
                                 monotonic=Monotonic())

    def test_s0_to_s3_writes_one_write_once_receipt_per_transition(self) -> None:
        config_bytes = b'{"run_id": "RUN-01"}\n'
        self.paths.config.write_bytes(config_bytes)

        s0 = self.ledger.run_step("PREREGISTER", None, {"config.json": config_bytes},
                                  lambda step: {"plan.json": b"frozen"})
        self.assertEqual(s0.status, "COMPLETE")

        s1 = self.ledger.run_step("PREFLIGHT", None, {"config.json": config_bytes},
                                  lambda step: {"preflight.json": b"planned==expected"})
        self.assertEqual(s1.status, "COMPLETE")

        s2 = self.ledger.publish_step(
            "PUBLISH_PLAN", self.repo, [self.paths.config],
            "Publish the frozen plan", ref="origin/main",
            inputs={"config.json": config_bytes})
        self.assertEqual(s2.status, "COMPLETE")
        self.assertTrue(s2.verified_line.startswith("VERIFIED "))

        s3 = self.ledger.run_step("CYCLE_OPEN", 1, {"budget": {"cycles": 1}},
                                  lambda step: {"cycle.json": b"open"})
        self.assertEqual(s3.status, "COMPLETE")

        names = sorted(path.name for path in self.paths.steps.iterdir())
        self.assertEqual(names, [
            "0001-PREREGISTER.json", "0002-PREFLIGHT.json",
            "0003-PUBLISH_PLAN.json", "0003-PUBLISH_PLAN.verified",
            "0004-CYCLE_OPEN.json",
        ])
        self.assertEqual([row.receipt.status for row in self.ledger.records()],
                         ["COMPLETE"] * 4)
        self.assertEqual(self.ledger.markers(), ())
        self.assertIsNone(self.ledger.blocking())

    def test_the_verified_line_reaches_the_sidecar_the_receipt_and_the_ledger(self) -> None:
        self.paths.config.write_bytes(b'{"run_id": "RUN-01"}\n')
        outcome = self.ledger.publish_step(
            "PUBLISH_PLAN", self.repo, [self.paths.config], "Publish the plan",
            ref="origin/main", inputs={"config.json": b"c"})

        line = outcome.verified_line
        self.assertEqual(self.ledger.verified_line(outcome.step_key), line)
        self.assertEqual(outcome.receipt.outputs_sha256["verified_line"],
                         custody.sha256_bytes(line.encode("utf-8")))
        self.assertIn(line, self.ledger_file.read_bytes().decode("utf-8"))
        self.assertEqual(outcome.receipt.published_commit,
                         self.raw(self.remote, "rev-parse", "refs/heads/main"))

    def test_a_publication_step_is_skipped_on_resume_and_never_pushes_twice(self) -> None:
        self.paths.config.write_bytes(b'{"run_id": "RUN-01"}\n')
        first = self.ledger.publish_step(
            "PUBLISH_PLAN", self.repo, [self.paths.config], "Publish the plan",
            ref="origin/main", inputs={"config.json": b"c"})

        resumed = StepLedger(self.paths.run_root, PLAN_ID, clock=Clock(),
                             monotonic=Monotonic())

        def refuse(*_a, **_k):  # pragma: no cover - the point is it is not called
            raise AssertionError("a COMPLETE publication must not publish again")

        again = resumed.publish_step(
            "PUBLISH_PLAN", self.repo, [self.paths.config], "Publish the plan",
            ref="origin/main", inputs={"config.json": b"c"}, publisher=refuse)
        self.assertEqual(again.status, "SKIPPED")
        self.assertEqual(again.step_key, first.step_key)
        self.assertEqual(again.verified_line, first.verified_line)

    def assert_noop_publication_resumes(self, paths):
        head = self.raw(self.repo, "rev-parse", "HEAD")
        with self.ledger_file.open(encoding="utf-8", newline="") as handle:
            ledger_before = handle.read()
        outcome = self.ledger.publish_step(
            "PUBLISH_CY", self.repo, paths, "Nothing new", ref="origin/main",
            cycle=1, inputs={"cycle": b"one"})
        self.assertEqual(outcome.status, "COMPLETE")
        self.assertFalse(outcome.value.published)
        self.assertEqual(outcome.value.paths, ())
        self.assertEqual(outcome.value.files, ())
        self.assertFalse(outcome.value.committed)
        self.assertIsNone(outcome.verified_line)
        self.assertIsNone(outcome.receipt.published_commit)
        self.assertEqual(outcome.receipt.outputs_sha256,
                         {"published": custody.sha256_bytes(b"false")})
        self.assertEqual(list(self.paths.steps.glob("*.verified")), [])
        with self.ledger_file.open(encoding="utf-8", newline="") as handle:
            self.assertEqual(handle.read(), ledger_before)
        self.assertEqual(self.raw(self.repo, "rev-parse", "HEAD"), head)
        resumed = StepLedger(self.paths.run_root, PLAN_ID, clock=Clock(),
                             monotonic=Monotonic())
        self.assertIsNone(resumed.pending_publication())
        self.assertIsNone(resumed.guard())
        self.assertEqual([row.action for row in resumed.resume_plan()], ["SKIP"])

        def refuse(*_args, **_kwargs):
            raise AssertionError("a completed no-op must not republish")

        again = resumed.publish_step(
            "PUBLISH_CY", self.repo, paths, "Nothing new", ref="origin/main",
            cycle=1, inputs={"cycle": b"one"}, publisher=refuse)
        self.assertEqual(again.status, "SKIPPED")
        self.assertEqual(resumed.run_step("CYCLE_OPEN", 2, {}, lambda _: None).status,
                         "COMPLETE")
        return outcome

    def test_an_empty_directory_completes_without_verified_and_resumes(self):
        empty = self.paths.run_root / "readings"
        empty.mkdir()
        self.assert_noop_publication_resumes([empty.relative_to(self.repo).as_posix()])

    def test_failed_git_retry_verifies_already_committed_paths_and_resumes(self):
        with self.paths.config.open("w", encoding="utf-8", newline="") as handle:
            handle.write("{}\n")
        selected = [self.paths.config.relative_to(self.repo).as_posix()]

        def failed(*_args, **_kwargs):
            raise LoopError("GIT_OPERATION_FAILED", "the former empty directory pathspec")

        with self.assertRaises(LoopError):
            self.ledger.publish_step(
                "PUBLISH_CY", self.repo, selected, "Publish cycle", ref="origin/main",
                cycle=1, inputs={"cycle": b"one"}, publisher=failed)
        old = self.paths.step_path(1, "PUBLISH_CY")
        with old.open(encoding="utf-8", newline="") as handle:
            before = handle.read()
        self.raw(self.repo, "add", "--", *selected)
        self.raw(self.repo, "commit", "-m", "External checkpoint")
        head = self.raw(self.repo, "rev-parse", "HEAD")
        self.assertEqual(self.ledger.resume_plan()[0].action, "RETRY")
        outcome = self.ledger.publish_step(
            "PUBLISH_CY", self.repo, selected, "Publish cycle", ref="origin/main",
            cycle=1, inputs={"cycle": b"one"})
        self.assertEqual((outcome.index, outcome.status), (2, "COMPLETE"))
        self.assertTrue(outcome.value.published)
        self.assertFalse(outcome.value.committed)
        self.assertEqual(outcome.receipt.published_commit, head)
        self.assertEqual(self.raw(self.remote, "rev-parse", "refs/heads/main"), head)
        self.assertTrue(outcome.verified_line.startswith("VERIFIED " + head))
        self.assertEqual(outcome.receipt.outputs_sha256["verified_line"],
                         custody.sha256_bytes(outcome.verified_line.encode("utf-8")))
        with (self.paths.steps / "0002-PUBLISH_CY.verified").open(
                encoding="utf-8", newline="") as handle:
            self.assertEqual(handle.read(), outcome.verified_line + "\n")
        with self.ledger_file.open(encoding="utf-8", newline="") as handle:
            self.assertIn(outcome.verified_line, handle.read())
        with old.open(encoding="utf-8", newline="") as handle:
            self.assertEqual(handle.read(), before)
        resumed = StepLedger(self.paths.run_root, PLAN_ID, clock=Clock(),
                             monotonic=Monotonic())
        self.assertIsNone(resumed.pending_publication())
        self.assertIsNone(resumed.guard())
        self.assertEqual([row.action for row in resumed.resume_plan()], ["SKIP"])
        again = resumed.publish_step(
            "PUBLISH_CY", self.repo, selected, "Publish cycle", ref="origin/main",
            cycle=1, inputs={"cycle": b"one"}, publisher=failed)
        self.assertEqual(again.status, "SKIPPED")
        self.assertEqual(again.verified_line, outcome.verified_line)
        self.assertEqual(resumed.run_step("CYCLE_OPEN", 2, {}, lambda _: None).status,
                         "COMPLETE")

    def test_a_failed_git_step_is_preserved_and_retried_as_a_noop(self):
        empty = self.paths.run_root / "readings"
        empty.mkdir()

        def failed(*_args, **_kwargs):
            raise LoopError("GIT_OPERATION_FAILED", "the former empty directory pathspec")

        with self.assertRaises(LoopError):
            self.ledger.publish_step(
                "PUBLISH_CY", self.repo, [empty.relative_to(self.repo).as_posix()], "Nothing new", ref="origin/main",
                cycle=1, inputs={"cycle": b"one"}, publisher=failed)
        old = self.paths.step_path(1, "PUBLISH_CY")
        with old.open(encoding="utf-8", newline="") as handle:
            before = handle.read()
        self.assertEqual(self.ledger.resume_plan()[0].action, "RETRY")
        outcome = self.assert_noop_publication_resumes([empty.relative_to(self.repo).as_posix()])
        self.assertEqual(outcome.index, 2)
        with old.open(encoding="utf-8", newline="") as handle:
            self.assertEqual(handle.read(), before)

    def test_deletion_only_timeout_retries_push_and_verification_after_reload(self):
        selected = self.repo / "selected"
        selected.mkdir()
        deleted = selected / "deleted.json"
        with deleted.open("w", encoding="utf-8", newline="") as handle:
            handle.write("{}\n")
        relative = deleted.relative_to(self.repo).as_posix()
        self.raw(self.repo, "add", "--", relative)
        self.raw(self.repo, "commit", "-m", "Seed deletion-only selection")
        self.raw(self.repo, "push", "origin", "HEAD:refs/heads/main")
        deleted.unlink()

        class RecordingGit(LocalGit):
            timeout_push = False

            def _invoke(self, tokens):
                self.calls.append(tuple(tokens))
                if tokens and tokens[0] == "push" and self.timeout_push:
                    return GitOutcome(-1, b"", b"", True, tuple(tokens))
                return super()._invoke(tokens)

        first_git = RecordingGit(self.repo)
        first_git.calls = []
        first_git.timeout_push = True
        first = self.ledger.publish_step(
            "PUBLISH_CY", self.repo, ["selected"], "Publish deletion", ref="origin/main",
            cycle=1, git=first_git)
        self.assertEqual((first.status, first.failure_code),
                         ("FAILED", "PUBLISH_PENDING"))
        self.assertTrue(first.value.committed)
        self.assertEqual(first.value.files, ())
        self.assertIsNone(first.verified_line)
        self.assertEqual(self.raw(self.repo, "ls-tree", "-r", "--name-only", "HEAD",
                                  "--", relative), "")
        self.assertEqual(self.raw(self.remote, "ls-tree", "-r", "--name-only",
                                  "refs/heads/main", "--", relative), relative)
        with self.paths.step_path(first.index, "PUBLISH_CY").open(
                encoding="utf-8", newline="") as handle:
            first_receipt = handle.read()
        resumed = StepLedger(self.paths.run_root, PLAN_ID, clock=Clock(),
                             monotonic=Monotonic())
        with self.assertRaises(PublishBlocked):
            resumed.run_step("CYCLE_OPEN", 2, {}, lambda _: None)
        retry_git = RecordingGit(self.repo)
        retry_git.calls = []
        landed = resumed.publish_step(
            "PUBLISH_CY", self.repo, ["selected"], "Publish deletion", ref="origin/main",
            cycle=1, git=retry_git)
        self.assertEqual((landed.status, landed.value.status), ("COMPLETE", "PUBLISHED"))
        self.assertFalse(landed.value.committed)
        self.assertTrue(landed.verified_line.startswith("VERIFIED "))
        self.assertEqual(landed.receipt.published_commit,
                         self.raw(self.remote, "rev-parse", "refs/heads/main"))
        verbs = [call[0] for call in retry_git.calls]
        self.assertIn("push", verbs)
        self.assertIn("ls-remote", verbs)
        self.assertIn("fetch", verbs)
        self.assertIn(("rev-parse", "FETCH_HEAD^{tree}"), retry_git.calls)
        self.assertEqual(self.raw(self.remote, "ls-tree", "-r", "--name-only",
                                  "refs/heads/main", "--", relative), "")
        with self.paths.step_path(first.index, "PUBLISH_CY").open(
                encoding="utf-8", newline="") as handle:
            self.assertEqual(handle.read(), first_receipt)
        self.assertIsNone(resumed.pending_publication())
        self.assertEqual(resumed.run_step("CYCLE_OPEN", 2, {}, lambda _: None).status,
                         "COMPLETE")

    def test_a_pending_push_with_clean_paths_still_retries_and_blocks(self):
        with self.paths.config.open("w", encoding="utf-8", newline="") as handle:
            handle.write("{}\n")

        class TimedOutPush(LocalGit):
            def _invoke(self, tokens):
                if tokens and tokens[0] == "push":
                    return GitOutcome(-1, b"", b"", True, tuple(tokens))
                return super()._invoke(tokens)

        for attempt in (1, 2):
            outcome = self.ledger.publish_step(
                "PUBLISH_PLAN", self.repo, [self.paths.config.relative_to(self.repo).as_posix()], "Publish plan",
                ref="origin/main", inputs={"config": b"c"}, git=TimedOutPush(self.repo))
            self.assertEqual((outcome.status, outcome.failure_code),
                             ("FAILED", "PUBLISH_PENDING"))
            self.assertEqual(outcome.value.attempt, attempt)
            self.assertIsNone(outcome.verified_line)
            self.assertIsNotNone(self.ledger.pending_publication())
            with self.assertRaises(PublishBlocked):
                self.ledger.run_step("CYCLE_OPEN", 1, {}, lambda _: None)
        landed = self.ledger.publish_step(
            "PUBLISH_PLAN", self.repo, [self.paths.config.relative_to(self.repo).as_posix()], "Publish plan",
            ref="origin/main", inputs={"config": b"c"})
        self.assertEqual(landed.status, "COMPLETE")
        self.assertTrue(landed.value.published)
        self.assertFalse(landed.value.committed)
        self.assertIsNone(self.ledger.pending_publication())


# ------------------------------------------------------------------------- #
# step_key
# ------------------------------------------------------------------------- #

class TheStepKeyIsDerivedNotInvented(LedgerFixture):

    def test_the_key_is_types_step_receipt_key_over_the_same_five_fields(self) -> None:
        ledger = self.build()
        inputs = {"config.json": b"one", "plan.json": b"two"}
        digests = {"config.json": custody.sha256_bytes(b"one"),
                   "plan.json": custody.sha256_bytes(b"two")}
        self.assertEqual(ledger.step_key("SEND", 2, "w1", inputs),
                         StepReceipt.key(PLAN_ID, "SEND", 2, "w1", digests))

    def test_the_key_moves_with_the_plan_the_kind_the_cycle_the_wave_and_the_inputs(self) -> None:
        ledger = self.build()
        base = ledger.step_key("SEND", 1, "w1", {"a": b"x"})
        self.assertNotEqual(base, ledger.step_key("READ", 1, "w1", {"a": b"x"}))
        self.assertNotEqual(base, ledger.step_key("SEND", 2, "w1", {"a": b"x"}))
        self.assertNotEqual(base, ledger.step_key("SEND", 1, "w2", {"a": b"x"}))
        self.assertNotEqual(base, ledger.step_key("SEND", 1, "w1", {"a": b"y"}))
        self.assertNotEqual(base, self.build(plan_id=OTHER_PLAN_ID)
                            .step_key("SEND", 1, "w1", {"a": b"x"}))

    def test_an_already_computed_digest_and_its_bytes_give_the_same_key(self) -> None:
        ledger = self.build()
        self.assertEqual(ledger.step_key("IMPORT", 1, None, {"a": b"x"}),
                         ledger.step_key("IMPORT", 1, None,
                                         {"a": custody.sha256_bytes(b"x")}))

    def test_a_receipt_recomputes_its_own_key_from_its_own_bytes(self) -> None:
        ledger = self.build()
        outcome = ledger.run_step("PREREGISTER", None, {"a": b"x"}, lambda step: None)
        body = self.receipt_body(outcome.index, "PREREGISTER")
        self.assertEqual(body["step_key"],
                         StepReceipt.key(PLAN_ID, "PREREGISTER", None, None,
                                         body["inputs_sha256"]))


# ------------------------------------------------------------------------- #
# Write-once receipts and markers
# ------------------------------------------------------------------------- #

class ReceiptsAreWriteOnce(LedgerFixture):

    def test_a_spending_step_writes_its_marker_before_the_body_runs(self) -> None:
        ledger = self.build()
        seen: list[list[str]] = []
        ledger.run_step("SEND", 1, {"wave": b"w"},
                        lambda step: seen.append(self.step_files()), wave="w1")
        self.assertEqual(seen[0], ["0001-SEND.json.open"])
        self.assertEqual(self.step_files(), ["0001-SEND.json"])

    def test_a_replayable_step_writes_no_marker_at_all(self) -> None:
        ledger = self.build()
        seen: list[list[str]] = []
        ledger.run_step("IMPORT", 1, {}, lambda step: seen.append(self.step_files()))
        self.assertEqual(seen[0], [])
        self.assertEqual(self.step_files(), ["0001-IMPORT.json"])

    def test_a_second_receipt_at_one_index_is_a_write_once_violation(self) -> None:
        ledger = self.build()
        handle = ledger.begin("PREREGISTER", inputs={"a": b"x"})
        handle.complete(None)
        stale = ledger.begin("PREREGISTER", inputs={"a": b"y"})
        stale.index = 1
        with self.assertRaises(custody.WriteOnceViolation) as caught:
            stale.complete(None)
        self.assertEqual(caught.exception.code, "WRITE_ONCE_VIOLATION")

    def test_every_receipt_is_fenced_inside_the_run_root(self) -> None:
        ledger = self.build()
        ledger.run_step("PREREGISTER", None, {}, lambda step: None)
        for row in ledger.records():
            self.assertTrue(str(row.path).startswith(str(ledger.run_root)))

    def test_a_receipt_written_under_another_plan_id_is_plan_id_mismatch(self) -> None:
        self.build().run_step("PREREGISTER", None, {}, lambda step: None)
        with self.assertRaises(LoopError) as caught:
            self.build(plan_id=OTHER_PLAN_ID).records()
        self.assertEqual(caught.exception.code, "PLAN_ID_MISMATCH")

    def test_a_declared_spending_flag_that_fights_the_table_is_refused(self) -> None:
        ledger = self.build()
        with self.assertRaises(StepError) as caught:
            ledger.run_step("SEND", 1, {}, lambda step: None, False)
        self.assertEqual(caught.exception.code, "STEP_CLASS_DISAGREEMENT")
        self.assertEqual(
            ledger.run_step("IMPORT", 1, {}, lambda step: None, False).status,
            "COMPLETE")

    def test_an_unknown_step_kind_is_refused_before_anything_is_written(self) -> None:
        ledger = self.build()
        with self.assertRaises(LoopError) as caught:
            ledger.begin("NOT_A_STEP")
        self.assertEqual(caught.exception.code, "STEP_RECEIPT_INVALID")
        self.assertEqual(self.step_files(), [])


# ------------------------------------------------------------------------- #
# Resume: skip, replay, retry
# ------------------------------------------------------------------------- #

class ResumeSkipsWhatIsCompleteAndReplaysWhatIsReplayable(LedgerFixture):

    def test_a_complete_non_replayable_step_is_skipped_and_the_body_is_not_entered(self) -> None:
        first = self.build()
        first.run_step("PREREGISTER", None, {"a": b"x"}, lambda step: {"o": b"out"})

        calls: list[int] = []
        outcome = self.build().run_step("PREREGISTER", None, {"a": b"x"},
                                        lambda step: calls.append(1))
        self.assertEqual(outcome.status, "SKIPPED")
        self.assertFalse(outcome.ran)
        self.assertEqual(calls, [])
        self.assertEqual(self.step_files(), ["0001-PREREGISTER.json"])

    def test_a_complete_replayable_step_is_re_run_and_must_reproduce_its_bytes(self) -> None:
        body = lambda step: {"graph": b"deterministic bytes"}  # noqa: E731
        self.build().run_step("IMPORT", 1, {"a": b"x"}, body)

        calls: list[int] = []

        def again(step):
            calls.append(1)
            return {"graph": b"deterministic bytes"}

        outcome = self.build().run_step("IMPORT", 1, {"a": b"x"}, again)
        self.assertEqual(outcome.status, "REPLAYED")
        self.assertEqual(calls, [1])
        self.assertEqual(self.step_files(), ["0001-IMPORT.json"])

    def test_a_replayable_step_that_produces_other_bytes_raises_step_nondeterministic(self) -> None:
        self.build().run_step("IMPORT", 1, {"a": b"x"},
                              lambda step: {"graph": b"deterministic bytes"})
        ledger = self.build()
        with self.assertRaises(StepNondeterministic) as caught:
            ledger.run_step("IMPORT", 1, {"a": b"x"}, lambda step: {"graph": b"drift"})
        self.assertEqual(caught.exception.code, "STEP_NONDETERMINISTIC")
        self.assertEqual(caught.exception.differing, ("graph",))

    def test_a_nondeterministic_replay_is_itself_recorded_as_a_receipt(self) -> None:
        self.build().run_step("IMPORT", 1, {"a": b"x"}, lambda step: {"graph": b"one"})
        with self.assertRaises(StepNondeterministic):
            self.build().run_step("IMPORT", 1, {"a": b"x"},
                                  lambda step: {"graph": b"two"})
        recorded = self.receipt_body(2, "IMPORT")
        self.assertEqual(recorded["status"], "FAILED")
        self.assertEqual(recorded["failure_code"], "STEP_NONDETERMINISTIC")

    def test_a_missing_output_is_a_mismatch_just_as_a_changed_one_is(self) -> None:
        self.build().run_step("USE_TABLE", 1, {}, lambda step: {"table": b"rows"})
        with self.assertRaises(StepNondeterministic) as caught:
            self.build().run_step("USE_TABLE", 1, {}, lambda step: {})
        self.assertEqual(caught.exception.differing, ("table",))

    def test_resume_plan_names_the_action_for_every_recorded_step(self) -> None:
        ledger = self.build()
        ledger.run_step("PREREGISTER", None, {}, lambda step: None)
        ledger.run_step("PREFLIGHT", None, {}, lambda step: None)
        plan = self.build().resume_plan()
        self.assertEqual([(row.index, row.kind, row.action) for row in plan],
                         [(1, "PREREGISTER", "SKIP"), (2, "PREFLIGHT", "REPLAY")])
        self.assertIsNone(self.build().blocking())


# ------------------------------------------------------------------------- #
# Halt 1 - an unresolved open marker
# ------------------------------------------------------------------------- #

class AnOpenMarkerHaltsWithUnresolvedStep(LedgerFixture):

    def kill_mid_send(self) -> str:
        """Open a spending step and walk away: exactly what a kill leaves."""

        handle = self.build().begin("SEND", cycle=1, wave="w1", inputs={"a": b"x"})
        return handle.step_key

    def test_the_marker_survives_and_resume_halts_naming_the_step(self) -> None:
        self.kill_mid_send()
        self.assertEqual(self.step_files(), ["0001-SEND.json.open"])
        ledger = self.build()
        action = ledger.blocking()
        self.assertEqual((action.action, action.code, action.kind, action.index),
                         ("HALT", "UNRESOLVED_STEP", "SEND", 1))
        with self.assertRaises(UnresolvedStep) as caught:
            ledger.guard()
        self.assertEqual(caught.exception.code, "UNRESOLVED_STEP")
        self.assertIn("0001-SEND", str(caught.exception))

    def test_resume_never_re_runs_a_spending_step_that_may_have_been_billed(self) -> None:
        key = self.kill_mid_send()
        calls: list[int] = []
        ledger = self.build()
        with self.assertRaises(UnresolvedStep):
            ledger.run_step("SEND", 1, {"a": b"x"}, lambda step: calls.append(1),
                            wave="w1")
        self.assertEqual(calls, [])
        self.assertEqual(ledger.records(), ())
        self.assertEqual(ledger.blocking().step_key, key)

    def test_the_open_marker_blocks_every_other_step_too_not_only_its_own(self) -> None:
        self.kill_mid_send()
        with self.assertRaises(UnresolvedStep):
            self.build().run_step("IMPORT", 1, {}, lambda step: None)

    def test_the_marker_records_the_step_key_the_receipt_would_have_carried(self) -> None:
        key = self.kill_mid_send()
        index, kind, path = self.build().markers()[0]
        body = self.build().marker_body(path)
        self.assertEqual((index, kind), (1, "SEND"))
        self.assertEqual(body["step_key"], key)
        self.assertTrue(body["spending"])
        self.assertEqual(body["schema"], steps_module.MARKER_SCHEMA)


# ------------------------------------------------------------------------- #
# Halt 2 - a custody mismatch, sticky until acknowledged
# ------------------------------------------------------------------------- #

class ACustodyMismatchHaltsAndIsSticky(LedgerFixture):

    def induce(self, ledger: StepLedger | None = None) -> str:
        ledger = ledger if ledger is not None else self.build(with_ledger=True)
        finding = custody.CustodyFinding(
            code="SOURCE_PIN_MISMATCH", path="tools/runner.py",
            expected="0" * 64, observed="1" * 64)

        def body(step):
            step.record_custody([finding])
            raise custody.CustodyMismatch("SOURCE_PIN_MISMATCH", "tools/runner.py")

        with self.assertRaises(custody.CustodyMismatch):
            ledger.run_step("IMPORT", 1, {"a": b"x"}, body)
        return ledger.step_key("IMPORT", 1, None, {"a": b"x"})

    def test_the_step_is_halted_and_its_custody_findings_reach_the_receipt(self) -> None:
        self.induce()
        body = self.receipt_body(1, "IMPORT")
        self.assertEqual(body["status"], "HALTED")
        self.assertEqual(body["failure_code"], "SOURCE_PIN_MISMATCH")
        self.assertEqual(body["custody"], {"verified": False,
                                           "checks": ["SOURCE_PIN_MISMATCH"]})

    def test_the_halt_writes_an_erratum_stub_under_the_run_errata_directory(self) -> None:
        self.induce()
        stub = self.paths.errata / "0001-IMPORT-HALT.md"
        text = stub.read_bytes().decode("utf-8")
        self.assertIn("SOURCE_PIN_MISMATCH", text)
        self.assertIn("The loop never works around custody", text)

    def test_the_halt_reaches_the_decision_ledger_as_an_erratum(self) -> None:
        self.induce()
        text = self.ledger_file.read_bytes().decode("utf-8")
        self.assertIn("REC-20260914-A", text)
        self.assertIn("SOURCE_PIN_MISMATCH", text)

    def test_the_halt_is_sticky_and_blocks_every_successor_step_by_its_own_code(self) -> None:
        self.induce()
        ledger = self.build()
        with self.assertRaises(StickyHalt) as caught:
            ledger.run_step("USE_TABLE", 1, {}, lambda step: None)
        self.assertEqual(caught.exception.code, "SOURCE_PIN_MISMATCH")
        self.assertEqual(ledger.blocking().action, "HALT")

    def test_a_custody_mismatch_raised_as_any_custody_code_halts_not_fails(self) -> None:
        for code in sorted(CUSTODY_HALT_CODES)[:4]:
            with self.subTest(code=code):
                self.setUp()
                ledger = self.build()

                def body(step, code=code):
                    raise LoopError(code, "induced")

                with self.assertRaises(LoopError):
                    ledger.run_step("IMPORT", 1, {}, body)
                self.assertEqual(self.receipt_body(1, "IMPORT")["status"], "HALTED")


# ------------------------------------------------------------------------- #
# Acknowledgement
# ------------------------------------------------------------------------- #

class AcknowledgementClearsTheStickyHaltExactlyOnce(LedgerFixture):

    def induce_custody_halt(self) -> str:
        ledger = self.build(with_ledger=True)

        def body(step):
            step.record_custody([custody.CustodyFinding(code="SOURCE_PIN_MISMATCH",
                                                        path="tools/runner.py")])
            raise custody.CustodyMismatch("SOURCE_PIN_MISMATCH", "tools/runner.py")

        with self.assertRaises(custody.CustodyMismatch):
            ledger.run_step("IMPORT", 1, {"a": b"x"}, body)
        return ledger.step_key("IMPORT", 1, None, {"a": b"x"})

    def test_the_acknowledgement_is_write_once_and_records_the_reason(self) -> None:
        key = self.induce_custody_halt()
        path = self.build(with_ledger=True).acknowledge(
            key, "the pinned runner was re-published unchanged; pin re-taken")
        record = json.loads(path.read_bytes().decode("utf-8"))
        self.assertEqual(record["schema"], steps_module.ACK_SCHEMA)
        self.assertEqual(record["step_key"], key)
        self.assertEqual(record["failure_code"], "SOURCE_PIN_MISMATCH")
        self.assertIn("pin re-taken", record["reason"])
        self.assertIn("Acknowledged by the operator", record["erratum"])

    def test_the_second_acknowledgement_of_one_halt_is_refused(self) -> None:
        key = self.induce_custody_halt()
        ledger = self.build()
        ledger.acknowledge(key, "first and only")
        with self.assertRaises(custody.WriteOnceViolation) as caught:
            ledger.acknowledge(key, "a second bite")
        self.assertEqual(caught.exception.code, "WRITE_ONCE_VIOLATION")

    def test_after_acknowledgement_successor_steps_run_again(self) -> None:
        key = self.induce_custody_halt()
        ledger = self.build()
        with self.assertRaises(StickyHalt):
            ledger.run_step("USE_TABLE", 1, {}, lambda step: None)
        ledger.acknowledge(key, "re-pinned and re-verified by hand")
        self.assertIsNone(self.build().blocking())
        outcome = self.build().run_step("USE_TABLE", 1, {}, lambda step: None)
        self.assertEqual(outcome.status, "COMPLETE")

    def test_an_acknowledgement_also_clears_an_unresolved_open_marker(self) -> None:
        handle = self.build().begin("SEND", cycle=1, wave="w1", inputs={"a": b"x"})
        ledger = self.build()
        with self.assertRaises(UnresolvedStep):
            ledger.guard()
        ledger.acknowledge(handle.step_key,
                           "the provider log shows no dispatch for this wave")
        self.assertIsNone(self.build().blocking())

    def test_acknowledging_a_key_with_nothing_unresolved_is_refused(self) -> None:
        ledger = self.build()
        ledger.run_step("PREREGISTER", None, {}, lambda step: None)
        with self.assertRaises(StepError) as caught:
            ledger.acknowledge(ledger.step_key("PREREGISTER", None, None, {}), "why")
        self.assertEqual(caught.exception.code, "STEP_NOT_HALTED")

    def test_an_acknowledgement_without_a_reason_is_refused(self) -> None:
        key = self.induce_custody_halt()
        with self.assertRaises(StepError) as caught:
            self.build().acknowledge(key, "   ")
        self.assertEqual(caught.exception.code, "STEP_NOT_HALTED")

    def test_a_later_halt_on_the_same_key_is_not_covered_by_the_old_acknowledgement(self) -> None:
        key = self.induce_custody_halt()
        self.build().acknowledge(key, "re-pinned once")
        ledger = self.build()

        def body(step):
            raise custody.CustodyMismatch("SOURCE_PIN_MISMATCH", "again")

        with self.assertRaises(custody.CustodyMismatch):
            ledger.run_step("IMPORT", 1, {"a": b"x"}, body)
        blocking = self.build().blocking()
        self.assertEqual((blocking.index, blocking.code), (2, "SOURCE_PIN_MISMATCH"))


# ------------------------------------------------------------------------- #
# Halt 3 - a pending publication
# ------------------------------------------------------------------------- #

class APendingPublicationBlocksEverySuccessorStep(LedgerFixture):

    def pending_publisher(self, reason: str = "PUSH_REJECTED"):
        def publisher(repo, paths, message, ref, *, attempt=1, **_kwargs):
            return PublishResult(
                status="PENDING", ref=ref or "origin/main", paths=("p",), files=("p",),
                attempt=attempt, committed=True, local_commit="c" * 40,
                pending=PublishPending(reason=reason, attempt=attempt,
                                       ref=ref or "origin/main"))
        return publisher

    def landing_publisher(self):
        def publisher(repo, paths, message, ref, *, attempt=1, **_kwargs):
            line = ("VERIFIED " + "d" * 40 + " TREE " + "e" * 40
                    + " at 2026-09-14T12:00:00Z local=" + "d" * 40
                    + " remote=" + "d" * 40 + " ref=origin/main paths=1")
            return PublishResult(
                status="PUBLISHED", ref=ref or "origin/main", paths=("p",),
                files=("p",), attempt=attempt, committed=True,
                local_commit="d" * 40, remote_commit="d" * 40, tree="e" * 40,
                verified_line=line)
        return publisher

    def test_a_pending_result_is_recorded_as_a_failed_receipt_carrying_the_code(self) -> None:
        ledger = self.build()
        outcome = ledger.publish_step("PUBLISH_IN", self.repo_root, ["x"], "m",
                                      cycle=1, wave="w1", inputs={"a": b"x"},
                                      publisher=self.pending_publisher())
        self.assertEqual((outcome.status, outcome.failure_code),
                         ("FAILED", "PUBLISH_PENDING"))
        body = self.receipt_body(1, "PUBLISH_IN")
        self.assertEqual(body["failure_code"], "PUBLISH_PENDING")
        self.assertIn("PUSH_REJECTED", str(outcome.value.pending.reason))

    def test_it_blocks_the_next_dispatch_publication_before_dispatch(self) -> None:
        ledger = self.build()
        ledger.publish_step("PUBLISH_IN", self.repo_root, ["x"], "m", cycle=1,
                            wave="w1", inputs={"a": b"x"},
                            publisher=self.pending_publisher())
        with self.assertRaises(PublishBlocked) as caught:
            ledger.run_step("SEND", 1, {"a": b"x"}, lambda step: None, wave="w1")
        self.assertEqual(caught.exception.code, "PUBLISH_PENDING")

    def test_the_next_attempt_on_the_same_publication_is_let_through(self) -> None:
        ledger = self.build()
        ledger.publish_step("PUBLISH_IN", self.repo_root, ["x"], "m", cycle=1,
                            wave="w1", inputs={"a": b"x"},
                            publisher=self.pending_publisher())
        seen: list[int] = []

        def publisher(repo, paths, message, ref, *, attempt=1, **kwargs):
            seen.append(attempt)
            return self.landing_publisher()(repo, paths, message, ref,
                                            attempt=attempt, **kwargs)

        outcome = ledger.publish_step("PUBLISH_IN", self.repo_root, ["x"], "m",
                                      cycle=1, wave="w1", inputs={"a": b"x"},
                                      publisher=publisher)
        self.assertEqual(seen, [2])
        self.assertEqual(outcome.status, "COMPLETE")
        self.assertIsNone(self.build().pending_publication())
        self.assertEqual(
            self.build().run_step("SEND", 1, {"a": b"x"}, lambda step: None,
                                  wave="w1").status,
            "COMPLETE")

    def test_pending_survives_a_later_publication_exception(self) -> None:
        first = self.build().publish_step(
            "PUBLISH_CY", self.repo_root, ["selected"], "m", cycle=1,
            publisher=self.pending_publisher("PUSH_TIMEOUT"))
        seen = []

        def failed(*_args, **kwargs):
            seen.append(kwargs.get("retry_pending"))
            raise LoopError("GIT_OPERATION_FAILED", "read-back unavailable")

        with self.assertRaises(LoopError):
            self.build().publish_step(
                "PUBLISH_CY", self.repo_root, ["selected"], "m", cycle=1,
                publisher=failed)
        self.assertEqual(seen, [True])
        resumed = self.build()
        self.assertEqual(resumed.pending_publication().index, first.index)
        self.assertEqual(resumed.latest(first.step_key).receipt.failure_code,
                         "GIT_OPERATION_FAILED")
        with self.assertRaises(PublishBlocked):
            resumed.run_step("CYCLE_OPEN", 2, {}, lambda _: None)
        landed = resumed.publish_step(
            "PUBLISH_CY", self.repo_root, ["selected"], "m", cycle=1,
            publisher=self.landing_publisher())
        self.assertEqual(landed.status, "COMPLETE")
        self.assertIsNone(self.build().pending_publication())

    def test_an_unchanged_retry_cannot_clear_pending(self) -> None:
        self.build().publish_step(
            "PUBLISH_CY", self.repo_root, ["selected"], "m", cycle=1,
            publisher=self.pending_publisher("PUSH_TIMEOUT"))
        seen = []

        def unchanged(*_args, attempt=1, **kwargs):
            seen.append(kwargs.get("retry_pending"))
            return PublishResult(status="UNCHANGED", ref="origin/main",
                                 paths=(), files=(), attempt=attempt, committed=False)

        outcome = self.build().publish_step(
            "PUBLISH_CY", self.repo_root, ["selected"], "m", cycle=1,
            publisher=unchanged)
        self.assertEqual(seen, [True])
        self.assertEqual((outcome.status, outcome.failure_code),
                         ("FAILED", "PUBLISH_PENDING"))
        self.assertIsNone(outcome.verified_line)
        self.assertIsNone(outcome.receipt.published_commit)
        self.assertEqual(list(self.paths.steps.glob("*.verified")), [])
        resumed = self.build()
        self.assertIsNotNone(resumed.pending_publication())
        with self.assertRaises(PublishBlocked):
            resumed.run_step("CYCLE_OPEN", 2, {}, lambda _: None)
        landed = resumed.publish_step(
            "PUBLISH_CY", self.repo_root, ["selected"], "m", cycle=1,
            publisher=self.landing_publisher())
        self.assertEqual(landed.status, "COMPLETE")
        self.assertIsNone(self.build().pending_publication())

    def test_an_old_unpublished_complete_receipt_does_not_skip_pending_retry(self) -> None:
        first = self.build().publish_step(
            "PUBLISH_CY", self.repo_root, ["selected"], "m", cycle=1,
            publisher=self.pending_publisher("PUSH_TIMEOUT"))
        # Preserve a receipt written by the former empty-selection retry bug.
        self.build().begin("PUBLISH_CY", cycle=1).complete({"published": False})
        resumed = self.build()
        self.assertEqual(resumed.pending_publication().index, first.index)
        with self.assertRaises(PublishBlocked):
            resumed.run_step("CYCLE_OPEN", 2, {}, lambda _: None)
        landed = resumed.publish_step(
            "PUBLISH_CY", self.repo_root, ["selected"], "m", cycle=1,
            publisher=self.landing_publisher())
        self.assertEqual((landed.index, landed.status), (3, "COMPLETE"))
        self.assertTrue(landed.value.published)
        self.assertIsNone(self.build().pending_publication())

    def test_the_attempt_count_lives_in_the_ledger_not_in_publish(self) -> None:
        ledger = self.build()
        for expected in (1, 2):
            attempts: list[int] = []

            def publisher(repo, paths, message, ref, *, attempt=1, **_kwargs):
                attempts.append(attempt)
                return self.pending_publisher()(repo, paths, message, ref,
                                                attempt=attempt)

            ledger.publish_step("PUBLISH_EV", self.repo_root, ["x"], "m", cycle=1,
                                wave="w1", inputs={"a": b"x"}, publisher=publisher)
            self.assertEqual(attempts, [expected])
        key = ledger.step_key("PUBLISH_EV", 1, "w1", {"a": b"x"})
        self.assertEqual(ledger.attempts_for(key), 2)

    def test_a_non_publication_kind_is_refused_by_the_publication_wrapper(self) -> None:
        with self.assertRaises(StepError) as caught:
            self.build().publish_step("SEND", self.repo_root, ["x"], "m")
        self.assertEqual(caught.exception.code, "STEP_CLASS_DISAGREEMENT")
        self.assertEqual(PUBLICATION_STEPS,
                         ("PUBLISH_PLAN", "PUBLISH_IN", "PUBLISH_EV", "PUBLISH_CY"))

    def test_a_publication_that_raises_is_recorded_before_it_is_re_raised(self) -> None:
        def publisher(*_a, **_k):
            raise LoopError("PUBLISH_NOT_CONVERGING", "three attempts")

        ledger = self.build()
        with self.assertRaises(LoopError) as caught:
            ledger.publish_step("PUBLISH_CY", self.repo_root, ["x"], "m", cycle=1,
                                inputs={"a": b"x"}, publisher=publisher)
        self.assertEqual(caught.exception.code, "PUBLISH_NOT_CONVERGING")
        self.assertEqual(self.receipt_body(1, "PUBLISH_CY")["failure_code"],
                         "PUBLISH_NOT_CONVERGING")


# ------------------------------------------------------------------------- #
# Halt 4 - the step deadline
# ------------------------------------------------------------------------- #

class AStepDeadlineFailsWithStepTimeout(LedgerFixture):

    def test_a_body_that_overruns_is_failed_with_step_timeout(self) -> None:
        ledger = self.build(timeouts=TimeoutsConfig(step_seconds={"IMPORT": 30}))

        def body(step):
            self.monotonic.jump(31.0)

        with self.assertRaises(StepTimeout) as caught:
            ledger.run_step("IMPORT", 1, {}, body)
        self.assertEqual(caught.exception.code, "STEP_TIMEOUT")
        self.assertEqual(self.receipt_body(1, "IMPORT")["failure_code"], "STEP_TIMEOUT")

    def test_a_body_may_poll_the_deadline_and_stop_itself(self) -> None:
        ledger = self.build(timeouts=TimeoutsConfig(step_seconds={"READ": 10}))
        reached: list[str] = []

        def body(step):
            self.monotonic.jump(11.0)
            step.check_deadline()
            reached.append("never")  # pragma: no cover

        with self.assertRaises(StepTimeout):
            ledger.run_step("READ", 1, {}, body, wave="w1")
        self.assertEqual(reached, [])

    def test_a_timed_out_spending_step_keeps_its_marker_and_halts_on_resume(self) -> None:
        ledger = self.build(timeouts=TimeoutsConfig(step_seconds={"SEND": 5}))
        with self.assertRaises(StepTimeout):
            ledger.run_step("SEND", 1, {"a": b"x"},
                            lambda step: self.monotonic.jump(6.0), wave="w1")
        self.assertEqual(self.step_files(), ["0001-SEND.json", "0001-SEND.json.open"])
        action = self.build().blocking()
        self.assertEqual(action.code, "UNRESOLVED_STEP")
        self.assertIn("STEP_TIMEOUT", action.detail)
        self.assertEqual(MARKER_KEPT_CODES, frozenset({"STEP_TIMEOUT",
                                                       "STEP_BODY_FAILED"}))

    def test_a_step_kind_with_no_declared_deadline_never_times_out(self) -> None:
        ledger = self.build(timeouts=TimeoutsConfig(step_seconds={"SEND": 5}))
        self.monotonic.jump(10_000.0)
        self.assertEqual(
            ledger.run_step("IMPORT", 1, {}, lambda step: None).status, "COMPLETE")

    def test_a_step_that_finished_inside_its_deadline_is_complete(self) -> None:
        ledger = self.build(timeouts=TimeoutsConfig(step_seconds={"IMPORT": 30}))
        self.monotonic.jump(29.0)
        self.assertEqual(
            ledger.run_step("IMPORT", 1, {}, lambda step: None).status, "COMPLETE")


# ------------------------------------------------------------------------- #
# Failures are recorded, never swallowed
# ------------------------------------------------------------------------- #

class EveryFailureIsRecordedAsAReceiptWithItsCode(LedgerFixture):

    def test_a_provider_failure_code_rides_into_the_receipt_and_ends_that_step(self) -> None:
        ledger = self.build()

        def body(step):
            raise LoopError("HTTP_429", "the endpoint refused the wave")

        with self.assertRaises(LoopError):
            ledger.run_step("SEND", 1, {"a": b"x"}, body, wave="w1")
        recorded = self.receipt_body(1, "SEND")
        self.assertEqual((recorded["status"], recorded["failure_code"]),
                         ("FAILED", "HTTP_429"))

    def test_a_stable_provider_failure_resolves_the_marker_and_does_not_halt(self) -> None:
        ledger = self.build()
        with self.assertRaises(LoopError):
            ledger.run_step("SEND", 1, {"a": b"x"},
                            lambda step: (_ for _ in ()).throw(
                                LoopError("HTTP_429", "refused")), wave="w1")
        self.assertEqual(self.step_files(), ["0001-SEND.json"])
        self.assertIsNone(self.build().blocking())

    def test_an_unclassified_crash_is_recorded_as_step_body_failed(self) -> None:
        ledger = self.build()

        def body(step):
            raise ZeroDivisionError("the body did something nobody named")

        with self.assertRaises(ZeroDivisionError):
            ledger.run_step("IMPORT", 1, {}, body)
        self.assertEqual(self.receipt_body(1, "IMPORT")["failure_code"],
                         "STEP_BODY_FAILED")

    def test_an_unclassified_crash_on_a_spending_step_keeps_the_marker(self) -> None:
        ledger = self.build()
        with self.assertRaises(ValueError):
            ledger.run_step("MARK", 1, {"a": b"x"},
                            lambda step: (_ for _ in ()).throw(ValueError("boom")))
        self.assertIn("0001-MARK.json.open", self.step_files())
        self.assertEqual(self.build().blocking().code, "UNRESOLVED_STEP")

    def test_outputs_that_are_not_a_mapping_are_refused_and_recorded(self) -> None:
        ledger = self.build()
        handle = ledger.begin("IMPORT", cycle=1)
        handle.outputs = ["not a mapping"]
        with self.assertRaises(StepError) as caught:
            handle.complete(None)
        self.assertEqual(caught.exception.code, "STEP_OUTPUTS_INVALID")
        self.assertEqual(self.receipt_body(1, "IMPORT")["failure_code"],
                         "STEP_OUTPUTS_INVALID")

    def test_a_failed_step_that_carries_a_stable_code_is_offered_as_a_retry(self) -> None:
        ledger = self.build()
        with self.assertRaises(LoopError):
            ledger.run_step("SEND", 1, {"a": b"x"},
                            lambda step: (_ for _ in ()).throw(
                                LoopError("HTTP_429", "refused")), wave="w1")
        plan = self.build().resume_plan()
        self.assertEqual([(row.action, row.code) for row in plan],
                         [("RETRY", "HTTP_429")])

    def test_the_context_manager_form_records_the_same_receipt(self) -> None:
        ledger = self.build()
        with self.assertRaises(LoopError):
            with ledger.begin("IMPORT", cycle=1, inputs={"a": b"x"}) as step:
                step.record_output("graph", b"partial")
                raise LoopError("ARTIFACT_NOT_DERIVED_FROM_DELIVERY", "no delivery")
        body = self.receipt_body(1, "IMPORT")
        self.assertEqual(body["status"], "HALTED")
        self.assertEqual(body["outputs_sha256"]["graph"],
                         custody.sha256_bytes(b"partial"))


# ------------------------------------------------------------------------- #
# Custody reporting
# ------------------------------------------------------------------------- #

class TheCustodyBlockSaysWhatWasChecked(LedgerFixture):

    def test_a_step_that_ran_no_custody_check_does_not_claim_one(self) -> None:
        ledger = self.build()
        ledger.run_step("PREREGISTER", None, {}, lambda step: None)
        self.assertEqual(self.receipt_body(1, "PREREGISTER")["custody"],
                         {"verified": False, "checks": []})

    def test_an_empty_finding_list_is_the_only_thing_that_reads_verified(self) -> None:
        ledger = self.build()
        ledger.run_step("IMPORT", 1, {}, lambda step: step.record_custody([]))
        self.assertEqual(self.receipt_body(1, "IMPORT")["custody"],
                         {"verified": True, "checks": []})

    def test_two_findings_are_two_checks_and_are_not_collapsed(self) -> None:
        ledger = self.build()
        findings = [custody.CustodyFinding(code="SOURCE_PIN_MISMATCH", path="a"),
                    custody.CustodyFinding(code="SOURCE_PIN_MISMATCH", path="b")]

        def body(step):
            step.record_custody(findings)

        ledger.run_step("IMPORT", 1, {}, body)
        self.assertEqual(self.receipt_body(1, "IMPORT")["custody"]["checks"],
                         ["SOURCE_PIN_MISMATCH", "SOURCE_PIN_MISMATCH"])


# ------------------------------------------------------------------------- #
# Coordinate-grain resumption
# ------------------------------------------------------------------------- #

class CoordinateGrainResumptionSkipsOnlyTerminalCoordinates(LedgerFixture):

    def records_dir(self) -> Path:
        root = self.paths.reading_dir("problem/arm/cycle-1/node#r3")
        for phase in ("requests", "attempts", "responses"):
            (root / phase).mkdir(parents=True)
        return root

    def test_a_coordinate_with_a_response_is_complete(self) -> None:
        root = self.records_dir()
        for phase in ("requests", "attempts", "responses"):
            (root / phase / "critic-0.json").write_bytes(b"{}")
        self.assertEqual(completed_coordinates(root), {"critic-0"})
        self.assertEqual(scan_coordinates(root).indeterminate, frozenset())

    def test_a_request_or_attempt_with_no_response_is_indeterminate_not_absent(self) -> None:
        root = self.records_dir()
        (root / "requests" / "critic-0.json").write_bytes(b"{}")
        (root / "attempts" / "judge-1.json").write_bytes(b"{}")
        (root / "responses" / "critic-0.json").write_bytes(b"{}")
        scan = scan_coordinates(root)
        self.assertEqual(scan.complete, frozenset({"critic-0"}))
        self.assertEqual(scan.indeterminate, frozenset({"judge-1"}))
        self.assertEqual(scan.started, frozenset({"critic-0", "judge-1"}))

    def test_a_nested_record_keeps_its_coordinate_path(self) -> None:
        root = self.records_dir()
        (root / "requests" / "repair-1").mkdir()
        (root / "requests" / "repair-1" / "critic.json").write_bytes(b"{}")
        self.assertEqual(scan_coordinates(root).indeterminate,
                         frozenset({"repair-1/critic"}))

    def test_a_directory_that_does_not_exist_scans_to_nothing_and_writes_nothing(self) -> None:
        missing = self.paths.run_root / "readings" / "never-created"
        self.assertEqual(completed_coordinates(missing), set())
        self.assertFalse(missing.exists())


# ------------------------------------------------------------------------- #
# run.lock
# ------------------------------------------------------------------------- #

class RunLockRefusesASecondDriver(LedgerFixture):

    def test_a_second_lock_on_one_run_is_refused_by_code(self) -> None:
        first = RunLock(self.paths.lock, PLAN_ID, clock=self.clock).acquire()
        self.addCleanup(first.release)
        with self.assertRaises(RunLocked) as caught:
            RunLock(self.paths.lock, PLAN_ID, clock=self.clock).acquire()
        self.assertEqual(caught.exception.code, "RUN_LOCKED")
        self.assertEqual(NEW_CODES["RUN_LOCKED"][:4], "a se")

    def test_the_lock_records_pid_start_time_and_plan_id(self) -> None:
        with RunLock(self.paths.lock, PLAN_ID, pid=4242, clock=self.clock) as lock:
            holder = lock.holder()
        self.assertEqual(holder["pid"], 4242)
        self.assertEqual(holder["loop_plan_id"], PLAN_ID)
        self.assertEqual(holder["schema"], steps_module.LOCK_SCHEMA)
        self.assertTrue(holder["started_utc"].endswith("Z"))

    def test_releasing_the_lock_lets_the_next_driver_in(self) -> None:
        RunLock(self.paths.lock, PLAN_ID, clock=self.clock).acquire().release()
        second = RunLock(self.paths.lock, PLAN_ID, clock=self.clock).acquire()
        self.addCleanup(second.release)
        self.assertTrue(second.held)

    def test_a_lock_left_by_another_plan_id_is_a_plan_id_mismatch(self) -> None:
        RunLock(self.paths.lock, OTHER_PLAN_ID, clock=self.clock).acquire().release()
        with self.assertRaises(StepError) as caught:
            RunLock(self.paths.lock, PLAN_ID, clock=self.clock).acquire()
        self.assertEqual(caught.exception.code, "PLAN_ID_MISMATCH")

    def test_a_plan_id_mismatch_preserves_the_record_when_diagnostics_are_unavailable(self) -> None:
        RunLock(self.paths.lock, OTHER_PLAN_ID, clock=self.clock).acquire().release()
        with self.paths.lock.open(encoding="utf-8", newline="") as handle:
            before = handle.read()
        released = json.loads(before)
        self.assertIsNone(released["pid"])
        self.assertIsNone(released["started_utc"])
        self.assertTrue(released["released_utc"].endswith("Z"))
        second = RunLock(self.paths.lock, PLAN_ID, clock=self.clock)
        self.addCleanup(second.release)
        with patch.object(second, "holder", return_value=None):
            with self.assertRaises(StepError) as caught:
                second.acquire()
        self.assertEqual(caught.exception.code, "PLAN_ID_MISMATCH")
        self.assertFalse(second.held)
        with self.paths.lock.open(encoding="utf-8", newline="") as handle:
            self.assertEqual(handle.read(), before)
        with RunLock(self.paths.lock, OTHER_PLAN_ID, clock=self.clock) as resumed:
            self.assertTrue(resumed.held)


# ------------------------------------------------------------------------- #
# The module's own discipline
# ------------------------------------------------------------------------- #

class TheModuleKeepsItsOwnRules(LedgerFixture):

    def test_new_codes_are_folded_in_and_each_carries_one_line_of_reason(self) -> None:
        """The wave-1 integrator folded all five into ``types.FAILURE_CODES``
        (O9).  The reason each exists stays here, beside the code."""

        for code, reason in NEW_CODES.items():
            with self.subTest(code=code):
                self.assertRegex(code, r"\A[A-Z][A-Z0-9_]*\Z")
                self.assertIn(code, FAILURE_CODES)
                self.assertNotIn("\n", reason)
                self.assertGreater(len(reason), 30)

    def test_every_other_code_the_module_raises_is_already_a_failure_code(self) -> None:
        source = Path(steps_module.__file__).read_bytes().decode("utf-8")
        import re

        raised = set(re.findall(r'(?:StepError|LoopError|StickyHalt)\(\s*"([A-Z_]+)"',
                                source))
        raised |= {"UNRESOLVED_STEP", "STEP_NONDETERMINISTIC", "STEP_TIMEOUT",
                   "PUBLISH_PENDING"}
        self.assertTrue(raised)
        for code in sorted(raised - set(NEW_CODES)):
            with self.subTest(code=code):
                self.assertIn(code, FAILURE_CODES)

    def test_the_classification_is_taken_from_types_and_not_retyped(self) -> None:
        self.assertTrue(set(PUBLICATION_STEPS) <= SPENDING_STEPS)
        self.assertFalse(set(PUBLICATION_STEPS) & REPLAYABLE_STEPS)
        self.assertFalse(SPENDING_STEPS & REPLAYABLE_STEPS)

    def test_every_refusal_is_a_loop_error_so_one_except_catches_them_all(self) -> None:
        for cls in (StepError, UnresolvedStep, StepNondeterministic, StepTimeout,
                    StickyHalt, PublishBlocked, RunLocked):
            with self.subTest(cls=cls.__name__):
                self.assertTrue(issubclass(cls, LoopError))

    def test_the_open_marker_spelling_comes_from_run_paths(self) -> None:
        self.build().begin("SEND", cycle=1, wave="w1", inputs={"a": b"x"})
        self.assertTrue(self.paths.step_path(1, "SEND", open_marker=True).is_file())
        self.assertEqual(self.step_files(), ["0001-SEND.json.open"])

    def test_the_ledger_takes_the_run_root_not_the_repository_root(self) -> None:
        ledger = self.build()
        self.assertEqual(ledger.paths.run_root, ledger.run_root)
        self.assertEqual(ledger.run_root.resolve(), self.paths.run_root.resolve())
        ledger.run_step("PREREGISTER", None, {}, lambda step: None)
        self.assertTrue((self.paths.run_root / "steps"
                         / "0001-PREREGISTER.json").is_file())

    def test_resume_plan_writes_nothing_at_all(self) -> None:
        ledger = self.build()
        ledger.run_step("PREREGISTER", None, {}, lambda step: None)
        before = sorted(p.name for p in self.paths.run_root.rglob("*"))
        ledger.resume_plan()
        ledger.resume_plan()
        self.assertEqual(sorted(p.name for p in self.paths.run_root.rglob("*")),
                         before)

    def test_the_module_names_its_purpose_its_design_section_and_its_deviations(self) -> None:
        doc = steps_module.__doc__ or ""
        self.assertIn("W1-STEPS", doc)
        self.assertIn("section 4.3", doc)
        self.assertIn("Deviations from the design", doc)
        self.assertEqual(sorted(steps_module.__all__), list(steps_module.__all__))


# ------------------------------------------------------------------------- #
# Kill and resume, end to end
# ------------------------------------------------------------------------- #

class KillAndResumeLeavesNoCoordinateResent(LedgerFixture):

    def test_a_kill_mid_spending_step_halts_and_the_body_is_never_re_entered(self) -> None:
        first = self.build()
        first.run_step("PREREGISTER", None, {}, lambda step: None)
        handle = first.begin("SEND", cycle=1, wave="w1", inputs={"a": b"x"})
        del handle  # the process died here: the marker is all that is left

        entered: list[int] = []
        resumed = self.build()
        plan = resumed.resume_plan()
        self.assertEqual([(row.index, row.action) for row in plan],
                         [(1, "SKIP"), (2, "HALT")])
        with self.assertRaises(UnresolvedStep):
            resumed.run_step("SEND", 1, {"a": b"x"},
                             lambda step: entered.append(1), wave="w1")
        self.assertEqual(entered, [])

        key = resumed.blocking().step_key
        resumed.acknowledge(key, "the provider records show no attempt for this wave")
        after = self.build()
        self.assertIsNone(after.blocking())
        self.assertEqual(
            after.run_step("SEND", 1, {"a": b"x"}, lambda step: entered.append(2),
                           wave="w1").status,
            "COMPLETE")
        self.assertEqual(entered, [2])

    def test_a_kill_mid_replayable_step_re_runs_and_reproduces_its_bytes(self) -> None:
        first = self.build()
        first.begin("IMPORT", cycle=1, inputs={"a": b"x"})  # killed: no receipt
        self.assertEqual(self.step_files(), [])

        runs: list[int] = []

        def body(step):
            runs.append(1)
            return {"graph": b"the same bytes every time"}

        second = self.build()
        self.assertEqual(second.run_step("IMPORT", 1, {"a": b"x"}, body).status,
                         "COMPLETE")
        third = self.build()
        outcome = third.run_step("IMPORT", 1, {"a": b"x"}, body)
        self.assertEqual(outcome.status, "REPLAYED")
        self.assertEqual(len(runs), 2)
        self.assertEqual(outcome.outputs,
                         {"graph": custody.sha256_bytes(b"the same bytes every time")})
        self.assertEqual(self.step_files(), ["0001-IMPORT.json"])

    def test_the_terminal_coordinates_of_a_killed_send_are_not_re_sent(self) -> None:
        root = self.paths.reading_dir("problem/arm/cycle-1/node#r3")
        for phase in ("requests", "attempts", "responses"):
            (root / phase).mkdir(parents=True)
        for coordinate in ("critic-0", "defender-0"):
            (root / "requests" / f"{coordinate}.json").write_bytes(b"{}")
            (root / "responses" / f"{coordinate}.json").write_bytes(b"{}")
        (root / "requests" / "judge-0.json").write_bytes(b"{}")

        handle = self.build().begin("READ", cycle=1, wave="w1", inputs={"a": b"x"})
        del handle
        with self.assertRaises(UnresolvedStep):
            self.build().guard()

        scan = scan_coordinates(root)
        self.assertEqual(scan.complete, frozenset({"critic-0", "defender-0"}))
        self.assertEqual(scan.indeterminate, frozenset({"judge-0"}))


# ------------------------------------------------------------------------- #
# The wiring to receipts and publish is real, not re-implemented
# ------------------------------------------------------------------------- #

class TheLedgerWiresPublishToReceiptsAndOwnsNeither(LedgerFixture):

    def test_publish_is_the_module_function_and_the_ledger_appends_the_line(self) -> None:
        self.assertIs(steps_module.publish_module.publish, publish)
        ledger = self.build(with_ledger=True)
        line = ("VERIFIED " + "f" * 40 + " TREE " + "0" * 40
                + " at 2026-09-14T12:00:00Z local=" + "f" * 40
                + " remote=" + "f" * 40 + " ref=origin/main paths=2")

        def publisher(repo, paths, message, ref, *, attempt=1, **_kwargs):
            return PublishResult(status="PUBLISHED", ref="origin/main", paths=("a",),
                                 files=("a",), attempt=attempt, committed=True,
                                 local_commit="f" * 40, remote_commit="f" * 40,
                                 tree="0" * 40, verified_line=line)

        outcome = ledger.publish_step("PUBLISH_CY", self.repo_root, ["a"], "m",
                                      cycle=1, inputs={"a": b"x"},
                                      publisher=publisher)
        self.assertEqual(outcome.verified_line, line)
        self.assertIn(line, self.ledger_file.read_bytes().decode("utf-8"))
        self.assertEqual(
            (self.paths.steps / "0001-PUBLISH_CY.verified").read_bytes(),
            line.encode("utf-8") + b"\n")

    def test_a_missing_ledger_is_named_and_never_created_by_the_loop(self) -> None:
        """Wave-0 review S2 / wave-1 integration: ``receipts.ledger_append``
        refuses a missing ledger unless ``create=True``, and this module never
        passes it.  A driver pointed at the wrong path is told so at the first
        publication instead of starting a second ledger beside the real one."""

        missing = self.repo_root / "docs" / "NOT_THE_LEDGER.md"
        ledger = StepLedger(self.paths.run_root, PLAN_ID, ledger_path=missing,
                            receipt_id="REC-20260914-A", clock=self.clock,
                            monotonic=self.monotonic)
        line = ("VERIFIED " + "f" * 40 + " TREE " + "0" * 40
                + " at 2026-09-14T12:00:00Z local=" + "f" * 40
                + " remote=" + "f" * 40 + " ref=origin/main paths=1")

        def publisher(repo, paths, message, ref, *, attempt=1, **_kwargs):
            return PublishResult(status="PUBLISHED", ref="origin/main", paths=("a",),
                                 files=("a",), attempt=attempt, committed=True,
                                 local_commit="f" * 40, remote_commit="f" * 40,
                                 tree="0" * 40, verified_line=line)

        with self.assertRaises(LoopError) as caught:
            ledger.publish_step("PUBLISH_CY", self.repo_root, ["a"], "m",
                                cycle=1, inputs={"a": b"x"}, publisher=publisher)
        self.assertEqual(caught.exception.code, "LEDGER_NOT_FOUND")
        self.assertFalse(missing.exists(), "the loop created a ledger")
        # Item 47: the receipt is written BEFORE the ledger append, so the
        # publication that did happen has a record of it. It used to have none:
        # the marker stayed, the next guard() raised UNRESOLVED_STEP with nothing
        # to explain it, acknowledge() wrote an erratum saying the body was not
        # re-entered (false), and the next begin() re-published at attempt 1.
        files = self.step_files()
        self.assertIn("0001-PUBLISH_CY.json", files)
        self.assertIn("0001-PUBLISH_CY.verified", files)
        self.assertEqual([name for name in files if name.endswith(".open")], [])
        body = self.receipt_body(1, "PUBLISH_CY")
        self.assertEqual(body["status"], "COMPLETE")
        self.assertIsNone(body["failure_code"])
        self.assertEqual(body["published_commit"], "f" * 40)
        self.assertIn("verified_line", body["outputs_sha256"])
        # ... and the ledger failure is recorded as its own erratum.
        errata = sorted(p.name for p in self.paths.errata.iterdir())
        self.assertTrue(errata, "no erratum names the ledger that could not be written")
        text = "\n".join((self.paths.errata / name).read_text(encoding="utf-8")
                         for name in errata)
        self.assertIn("LEDGER_NOT_FOUND", text)
        # ... and a resume does not re-publish: the step is COMPLETE.
        again = StepLedger(self.paths.run_root, PLAN_ID, ledger_path=None,
                           clock=self.clock, monotonic=self.monotonic)
        plan = again.resume_plan()
        self.assertEqual([action.action for action in plan], ["SKIP"])
        self.assertFalse(any(action.halting for action in plan))
        self.assertIsNone(again.blocking())
        # The test's own ledger is a temp file it created first, which is the
        # other half of the rule: create=True is the test's call, never the loop's.
        self.assertTrue(self.ledger_file.is_file())
        receipts.ledger_append("a paragraph", self.ledger_file)
        fresh = self.repo_root / "docs" / "A_NEW_LEDGER.md"
        receipts.ledger_append("a paragraph", fresh, create=True)
        self.assertTrue(fresh.is_file())

    def test_the_erratum_text_uses_the_receipts_module_and_names_no_count(self) -> None:
        self.assertIs(steps_module.receipts, receipts)
        receipt = StepReceipt.build(
            loop_plan_id=PLAN_ID, index=7, kind="IMPORT",
            started_utc="2026-09-14T12:00:00Z", cycle=1, status="HALTED",
            failure_code="SOURCE_PIN_MISMATCH",
            custody={"verified": False, "checks": ["SOURCE_PIN_MISMATCH"]})
        text = steps_module.erratum_text(receipt, reason="re-pinned by hand")
        self.assertIn("0007-IMPORT", text)
        self.assertIn("SOURCE_PIN_MISMATCH", text)
        self.assertIn("re-pinned by hand", text)
        self.assertNotIn("exhaustion", text)



# ------------------------------------------------------------------------- #
# Odds and ends the acceptance list implies
# ------------------------------------------------------------------------- #

class TheRemainingClauses(LedgerFixture):

    def test_an_empty_run_tree_has_nothing_to_resume_and_nothing_to_halt_on(self) -> None:
        ledger = self.build()
        self.assertEqual(ledger.records(), ())
        self.assertEqual(ledger.markers(), ())
        self.assertEqual(ledger.resume_plan(), [])
        self.assertIsNone(ledger.blocking())
        self.assertIsNone(ledger.guard())
        self.assertEqual(ledger.next_index(), 1)

    def test_a_spending_flag_that_agrees_with_the_table_is_accepted(self) -> None:
        ledger = self.build()
        outcome = ledger.run_step("AUDIT", 1, {"a": b"x"}, lambda step: None, True)
        self.assertEqual(outcome.status, "COMPLETE")
        self.assertTrue(outcome.receipt.spending)

    def test_a_pending_publication_resolves_its_own_marker_so_a_retry_can_run(self) -> None:
        def publisher(repo, paths, message, ref, *, attempt=1, **_kwargs):
            return PublishResult(status="PENDING", ref="origin/main", paths=("a",),
                                 files=("a",), attempt=attempt, committed=True,
                                 local_commit="a" * 40,
                                 pending=PublishPending(reason="PUSH_TIMEOUT",
                                                        attempt=attempt,
                                                        ref="origin/main"))

        ledger = self.build()
        ledger.publish_step("PUBLISH_PLAN", self.repo_root, ["a"], "m",
                            inputs={"a": b"x"}, publisher=publisher)
        self.assertEqual(self.step_files(), ["0001-PUBLISH_PLAN.json"])
        action = ledger.blocking()
        self.assertEqual(action.code, "PUBLISH_PENDING")

    def test_a_skipped_step_hands_back_the_receipt_already_on_record(self) -> None:
        self.build().run_step("PREPARE", 1, {"a": b"x"},
                              lambda step: {"wave": b"prepared"}, wave="w1")
        outcome = self.build().run_step("PREPARE", 1, {"a": b"x"},
                                        lambda step: None, wave="w1")
        self.assertEqual(outcome.status, "SKIPPED")
        self.assertEqual(outcome.index, 1)
        self.assertEqual(outcome.outputs,
                         {"wave": custody.sha256_bytes(b"prepared")})

    def test_a_path_input_is_digested_as_the_bytes_at_it(self) -> None:
        target = self.paths.run_root / "config.json"
        target.write_bytes(b'{"run_id": "RUN-01"}\n')
        ledger = self.build()
        self.assertEqual(ledger.step_key("PREFLIGHT", None, None, {"c": target}),
                         ledger.step_key("PREFLIGHT", None, None,
                                         {"c": custody.sha256_path(target)}))

    def test_a_refused_begin_writes_nothing_into_the_steps_directory(self) -> None:
        self.build().begin("SEND", cycle=1, wave="w1", inputs={"a": b"x"})
        before = self.step_files()
        with self.assertRaises(UnresolvedStep):
            self.build().begin("IMPORT", cycle=1)
        self.assertEqual(self.step_files(), before)

    def test_the_acknowledgement_record_is_fenced_under_the_run_errata(self) -> None:
        handle = self.build().begin("MARK", cycle=1, wave="w1", inputs={"a": b"x"})
        path = self.build().acknowledge(handle.step_key, "no marks were dispatched")
        self.assertEqual(path.parent.resolve(), self.paths.errata.resolve())
        self.assertTrue(path.name.startswith("ACK-0001-"))

    def test_the_published_outcome_vocabulary_is_closed(self) -> None:
        self.assertEqual(steps_module.STEP_OUTCOMES,
                         ("COMPLETE", "FAILED", "HALTED", "SKIPPED", "REPLAYED"))
        self.assertEqual(steps_module.RESUME_ACTIONS,
                         ("SKIP", "REPLAY", "RETRY", "HALT"))

    def test_a_naive_clock_is_refused_because_it_has_no_utc_meaning(self) -> None:
        ledger = StepLedger(self.paths.run_root, PLAN_ID,
                            clock=lambda: datetime(2026, 9, 14, 12, 0, 0),
                            monotonic=self.monotonic)
        with self.assertRaises(StepError) as caught:
            ledger.begin("PREREGISTER")
        self.assertEqual(caught.exception.code, "MOMENT_NOT_AWARE")


class HardeningFindings(LedgerFixture):
    """One test per item of the wave-1 integration decisions, items 11-13."""

    def test_item11_an_undigestible_output_ends_with_a_receipt(self):
        """Item 11: it escaped ``complete()`` as a bare ``TypeError``.

        ``complete()`` runs outside ``run_step``'s ``except BaseException``, so
        ``fail_from`` never ran: a spending step ended with its ``.open`` marker
        standing and no receipt to explain it, and a non-spending step left no
        ``steps/`` entry at all.
        """

        ledger = self.build()
        with self.assertRaises(LoopError) as caught:
            ledger.run_step("SEND", 1, {"a": b"x"}, lambda handle: {"x": object()})
        self.assertEqual(caught.exception.code, "STEP_OUTPUTS_INVALID")
        self.assertEqual(self.step_files(), ["0001-SEND.json"])
        body = self.receipt_body(1, "SEND")
        self.assertEqual(body["status"], "FAILED")
        self.assertEqual(body["failure_code"], "STEP_OUTPUTS_INVALID")
        self.assertTrue(body["spending"], "SEND is a spending step")
        # The marker is resolved BY that receipt: nothing is left unexplained.
        fresh = self.build()
        blocking = fresh.blocking()
        self.assertIsNone(blocking, "a spending step was left unresolved")

    def test_item11_a_non_spending_step_leaves_a_receipt_too(self):
        ledger = self.build()
        with self.assertRaises(LoopError) as caught:
            ledger.run_step("IMPORT", 1, {"a": b"x"},
                            lambda handle: {"x": {1, 2, 3}})
        self.assertEqual(caught.exception.code, "STEP_OUTPUTS_INVALID")
        self.assertIn("0001-IMPORT.json", self.step_files())

    def test_item11_record_output_refuses_at_the_call_that_recorded_it(self):
        ledger = self.build()
        seen: list[str] = []

        def body(handle):
            try:
                handle.record_output("x", object())
            except LoopError as exc:
                seen.append(exc.code)
            handle.record_output("ok", b"bytes are fine")
            return None

        outcome = ledger.run_step("IMPORT", 1, {"a": b"x"}, body)
        self.assertEqual(seen, ["STEP_OUTPUTS_INVALID"])
        self.assertEqual(outcome.status, "COMPLETE")
        self.assertEqual(sorted(outcome.outputs), ["ok"])

    def test_item12_every_halting_code_this_module_classifies_is_documented(self):
        """Item 12: eight halting codes are classified here and raised elsewhere."""

        source = Path(steps_module.__file__).read_text(encoding="utf-8")
        elsewhere = ("CUSTODY_MISMATCH", "REQUEST_NOT_FROM_PLAN",
                     "ARTIFACT_NOT_DERIVED_FROM_DELIVERY", "TIMEOUT_NOT_APPLIED",
                     "PROVIDER_REQUEST_FILE_CHANGED", "TRANSPORT_PIN_MISMATCH",
                     "RUNTIME_SOURCE_CHANGED", "INPUT_NOT_PUBLISHED")
        table = source.split("CUSTODY_HALT_CODES: frozenset")[0]
        for code in elsewhere:
            with self.subTest(code=code):
                self.assertIn(code, CUSTODY_HALT_CODES)
                self.assertIn(code, FAILURE_CODES)
                # Named in the table of raise sites above the constant, so W6-DOC
                # can give each a per-code action rather than a family action.
                self.assertIn(code, table)
        # None of them is raised by this module: the table is the whole record.
        raised = set(re.findall(r"StepError\(\s*\"([A-Z_]+)\"", source))
        raised |= set(re.findall(r"StickyHalt\(\s*\"([A-Z_]+)\"", source))
        self.assertEqual(raised & set(elsewhere), set())

    def test_item13_the_indeterminate_promise_is_stated_truthfully(self):
        """Item 13: the word is promised to a reader and reaches none."""

        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            for phase in ("requests", "attempts", "responses"):
                (out / phase).mkdir()
            (out / "requests" / "row-1.json").write_bytes(b"{}")
            (out / "responses" / "row-2.json").write_bytes(b"{}")
            (out / "requests" / "row-2.json").write_bytes(b"{}")
            scan = scan_coordinates(out)
            self.assertEqual(scan.indeterminate, frozenset({"row-1"}))
            self.assertEqual(scan.complete, frozenset({"row-2"}))
            # Nothing was written, and nothing carries the word to a reader.
            self.assertEqual(sorted(p.name for p in out.iterdir()),
                             ["attempts", "requests", "responses"])
        docstring = steps_module.__doc__ or ""
        self.assertIn("does not report it", docstring)
        self.assertIn("W3-REPORT", docstring)
        self.assertIn("W5-DRIVER", docstring)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
