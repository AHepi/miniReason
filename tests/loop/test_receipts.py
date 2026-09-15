"""Tests for ``minireason.loop.receipts`` (W0-RECEIPTS).

Every test is named after the acceptance clause of the wave-plan entry it
covers, or after the property of design section 4.5 / section 8 it fixes.

The ledger fixture is a small copy with mixed CRLF and LF line endings and
non-ASCII prose, written into a tempfile. Every test that appends asserts that
the pre-existing region is byte-identical afterwards: the real
``docs/DECISION_LEDGER.md`` carries CRLF lines that must never be normalised,
and this suite would catch a writer that re-encoded them.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest import mock

from minireason import provider_openai_compat as compat
from minireason.loop import receipts


REPO = Path(__file__).resolve().parents[2]

#: Mixed CRLF/LF, an em dash and an accented word, two receipt ids already used.
FIXTURE = (
    b"# Decision ledger\n"
    b"\n"
    b"REC-20260914-A opened at 2026-09-14 00:01:00 UTC: the first receipt.\r\n"
    b"\r\n"
    b"REC-20260914-B outcome at 2026-09-14 00:02:00 UTC: caf\xc3\xa9 \xe2\x80\x94 second.\n"
    b"\n"
    b"VERIFIED 0f38f95 TREE 9045a94\r\n"
)

MOMENT = datetime.datetime(2026, 9, 14, 9, 30, 0, tzinfo=datetime.timezone.utc)


class LedgerTestCase(unittest.TestCase):
    """A temp ledger plus the byte-identity assertion every append must pass."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.ledger = self.root / "DECISION_LEDGER.md"
        self.ledger.write_bytes(FIXTURE)
        compat._reset_registered_secret_envs()
        self.addCleanup(compat._reset_registered_secret_envs)
        self.addCleanup(receipts.set_current_receipt, None)

    def data(self) -> bytes:
        return self.ledger.read_bytes()

    def assertPreExistingRegionUnchanged(self) -> None:
        self.assertEqual(self.data()[:len(FIXTURE)], FIXTURE)

    def tail(self) -> str:
        return self.data()[len(FIXTURE):].decode("utf-8")


class AppendDisciplineTests(LedgerTestCase):
    def test_the_pre_existing_region_is_byte_identical_after_every_append(self) -> None:
        receipt = receipts.open_receipt(
            title="Open a receipt", choice="write one paragraph", why="the rule requires it",
            contribution="wave 0", ledger_path=self.ledger, moment=MOMENT,
        )
        self.assertPreExistingRegionUnchanged()
        receipts.outcome_receipt(receipt, "the paragraph landed", ledger_path=self.ledger,
                                 moment=MOMENT)
        self.assertPreExistingRegionUnchanged()
        receipts.checkpoint_receipt(receipt, "still working", ledger_path=self.ledger,
                                    moment=MOMENT)
        self.assertPreExistingRegionUnchanged()
        receipts.erratum_receipt(receipt, "a count was wrong", "the count is four",
                                 ledger_path=self.ledger, moment=MOMENT)
        self.assertPreExistingRegionUnchanged()
        receipts.close_receipt(receipt, "done", ["sha256 abc"], ledger_path=self.ledger,
                               moment=MOMENT)
        self.assertPreExistingRegionUnchanged()

    def test_appends_never_re_encode_the_ledger_s_mixed_crlf_and_lf_lines(self) -> None:
        receipts.ledger_append("A plain paragraph.", self.ledger)
        receipts.ledger_append("Another plain paragraph.", self.ledger)
        data = self.data()
        self.assertPreExistingRegionUnchanged()
        self.assertEqual(data.count(b"\r\n"), FIXTURE.count(b"\r\n"))
        self.assertIn(b"caf\xc3\xa9 \xe2\x80\x94", data)
        self.assertNotIn(b"caf\xc3\x83\xc2\xa9", data)

    def test_an_append_only_adds_bytes_at_the_previous_end_of_file(self) -> None:
        appended = receipts.ledger_append("One paragraph.", self.ledger)
        self.assertEqual(appended.offset, len(FIXTURE))
        self.assertEqual(appended.end, len(self.data()))
        self.assertEqual(self.data()[appended.offset:], b"\nOne paragraph.\n")

    def test_a_paragraph_is_separated_from_the_previous_one_by_one_blank_line(self) -> None:
        receipts.ledger_append("First.", self.ledger)
        receipts.ledger_append("Second.", self.ledger)
        self.assertEqual(self.tail(), "\nFirst.\n\nSecond.\n")

    def test_appending_to_a_missing_ledger_creates_it_only_when_asked(self) -> None:
        """S2: ``open("ab")`` created a second ledger, and nothing said so.

        A mistyped path, a wrong repository root or a relative path resolved
        against the wrong working directory all used to *succeed*: a new file
        appeared whose receipt letters restarted at ``A``, which is the collision
        the minting lock exists to prevent, arrived at from the other side.
        """

        fresh = self.root / "fresh.md"
        with self.assertRaises(receipts.ReceiptError) as caught:
            receipts.ledger_append("First ever paragraph.", fresh)
        self.assertEqual(caught.exception.code, "LEDGER_NOT_FOUND")
        self.assertIn("create=True", str(caught.exception))
        self.assertFalse(fresh.exists(), "a refused append created the file anyway")

        receipts.ledger_append("First ever paragraph.", fresh, create=True)
        self.assertEqual(fresh.read_bytes(), b"First ever paragraph.\n")
        # Once it exists, no further permission is needed.
        receipts.ledger_append("Second paragraph.", fresh)
        self.assertTrue(fresh.read_bytes().endswith(b"\nSecond paragraph.\n"))

    def test_every_receipt_form_refuses_a_ledger_that_does_not_exist(self) -> None:
        absent = self.root / "nowhere" / "DECISION_LEDGER.md"
        forms = {
            "ledger_append": lambda: receipts.ledger_append("x", absent),
            "open_receipt": lambda: receipts.open_receipt(
                title="t", choice="c", why="w", contribution="k",
                ledger_path=absent, moment=MOMENT),
            "outcome_receipt": lambda: receipts.outcome_receipt(
                "REC-20260914-A", "x", ledger_path=absent, moment=MOMENT),
            "close_receipt": lambda: receipts.close_receipt(
                "REC-20260914-A", "x", ledger_path=absent, moment=MOMENT),
            "erratum_receipt": lambda: receipts.erratum_receipt(
                "REC-20260914-A", "d", "c", ledger_path=absent, moment=MOMENT),
            "checkpoint_receipt": lambda: receipts.checkpoint_receipt(
                "REC-20260914-A", "p", ledger_path=absent, moment=MOMENT),
            "open_preregistration": lambda: receipts.open_preregistration(
                absent, loop_plan_id="a" * 64, run_id="L001", moment=MOMENT),
        }
        for name, call in forms.items():
            with self.subTest(form=name):
                with self.assertRaises(receipts.ReceiptError) as caught:
                    call()
                self.assertEqual(caught.exception.code, "LEDGER_NOT_FOUND")
        self.assertFalse(absent.parent.exists())
        # create=True starts a ledger inside an existing tree; it never makes the
        # tree, because a missing directory is a wrong path, not a new ledger.
        with self.assertRaises(receipts.ReceiptError) as caught:
            receipts.ledger_append("x", absent, create=True)
        self.assertEqual(caught.exception.code, "LEDGER_NOT_FOUND")
        self.assertFalse(absent.parent.exists())
        # Only the forms that OPEN a receipt take create=.
        self.assertEqual(
            receipts.open_receipt(title="t", choice="c", why="w", contribution="k",
                                  ledger_path=self.root / "new.md", moment=MOMENT,
                                  create=True, set_current=False),
            "REC-20260914-A")

    def test_an_empty_paragraph_is_refused(self) -> None:
        with self.assertRaises(receipts.ReceiptError) as caught:
            receipts.ledger_append("   \n  ", self.ledger)
        self.assertEqual(caught.exception.code, "LEDGER_EMPTY_PARAGRAPH")
        self.assertEqual(self.data(), FIXTURE)

    def test_write_all_reassembles_a_record_across_short_writes(self) -> None:
        class ShortWriter:
            def __init__(self) -> None:
                self.buffer = bytearray()

            def write(self, data: memoryview) -> int:
                chunk = bytes(data[:5])
                self.buffer.extend(chunk)
                return len(chunk)

        record = ("a torn record would be a lost receipt " * 20).encode("utf-8")
        handle = ShortWriter()
        written = receipts._write_all(handle, record)
        self.assertEqual(written, len(record))
        self.assertEqual(bytes(handle.buffer), record)

    def test_a_write_returning_zero_raises_instead_of_looping(self) -> None:
        class DeadWriter:
            def write(self, data: memoryview) -> int:
                return 0

        with self.assertRaises(receipts.ReceiptError) as caught:
            receipts._write_all(DeadWriter(), b"bytes")
        self.assertEqual(caught.exception.code, "LEDGER_INCOMPLETE_WRITE")


class _ShortWriteHandle:
    """A real append handle that writes at most ``chunk`` bytes per call."""

    def __init__(self, handle, chunk: int) -> None:
        self._handle = handle
        self._chunk = chunk

    def write(self, data) -> int:
        return self._handle.write(bytes(memoryview(data)[:self._chunk]))

    def __getattr__(self, name: str):
        return getattr(self._handle, name)

    def __enter__(self):
        self._handle.__enter__()
        return self

    def __exit__(self, *exc) -> None:
        self._handle.__exit__(*exc)


class ContentionTests(LedgerTestCase):
    def _short_write_opener(self, chunk: int = 7):
        real = receipts._open_append

        def opener(path: Path):
            return _ShortWriteHandle(real(path), chunk)

        return opener

    def test_concurrent_appends_from_two_threads_interleave_with_no_loss_and_no_torn_record(self) -> None:
        paragraphs = [
            f"Thread {worker} paragraph {index}: " + "π\U0001f680 " * 200
            for worker in (0, 1) for index in range(12)
        ]
        start = threading.Barrier(2)

        def append(worker: int) -> None:
            start.wait()
            for index in range(12):
                receipts.ledger_append(paragraphs[worker * 12 + index], self.ledger)

        with mock.patch.object(receipts, "_open_append", self._short_write_opener()):
            threads = [threading.Thread(target=append, args=(worker,)) for worker in (0, 1)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

        data = self.data()
        self.assertPreExistingRegionUnchanged()
        for paragraph in paragraphs:
            encoded = paragraph.encode("utf-8")
            self.assertEqual(data.count(encoded), 1, paragraph[:40])
            index = data.index(encoded)
            self.assertEqual(data[index - 1:index], b"\n")
            self.assertEqual(data[index + len(encoded):index + len(encoded) + 1], b"\n")
        expected = len(FIXTURE) + sum(len(p.encode("utf-8")) + 2 for p in paragraphs)
        self.assertEqual(len(data), expected)

    def test_two_concurrent_verified_appends_preserve_tail_bytes_and_digests(self) -> None:
        # Use real handles and native locks, including msvcrt.locking on Windows.
        paragraphs = ("VERIFIED first TREE one", "VERIFIED second TREE two")
        for ending, separators in ((b"", 2), (b"\n", 1), (b"\r\n", 1),
                                   (b"\n\n", 0), (b"\r\n\r\n", 0), (b"\n\r\n", 0)):
            for newline in (b"\n", b"\r\n"):
                with self.subTest(ending=ending, newline=newline):
                    prefix = FIXTURE.rstrip(b"\r\n") + ending
                    with self.ledger.open("w", encoding="utf-8", newline="") as handle:
                        handle.write(prefix.decode("utf-8"))
                    start = threading.Barrier(2)

                    def append(paragraph: str):
                        start.wait(timeout=10)
                        return receipts.ledger_append(paragraph, self.ledger, newline=newline)

                    with ThreadPoolExecutor(max_workers=2) as workers:
                        futures = [workers.submit(append, paragraph) for paragraph in paragraphs]
                        appends = sorted((future.result(timeout=30) for future in futures),
                                         key=lambda result: result.offset)
                    self.assertCountEqual([result.text for result in appends], paragraphs)
                    expected = prefix
                    for index, result in enumerate(appends):
                        payload = (newline * (separators if index == 0 else 1)
                                   + result.text.encode("utf-8") + newline)
                        self.assertEqual(result.offset, len(expected))
                        self.assertEqual(result.written, len(payload))
                        expected += payload
                        self.assertEqual(result.sha256, hashlib.sha256(expected).hexdigest())
                    self.assertEqual(self.data(), expected)
                    self.assertEqual(self.data()[:len(prefix)], prefix)

    def test_id_minting_under_contention_never_collides(self) -> None:
        minted: list[str] = []
        lock = threading.Lock()
        start = threading.Barrier(8)

        def open_one(index: int) -> None:
            start.wait()
            receipt = receipts.open_receipt(
                title=f"Concurrent receipt {index}", choice="mint under the append lock",
                why="two agents may open a receipt at the same instant",
                contribution="wave 0", ledger_path=self.ledger, moment=MOMENT,
                set_current=False,
            )
            with lock:
                minted.append(receipt)

        with mock.patch.object(receipts, "_open_append", self._short_write_opener()):
            threads = [threading.Thread(target=open_one, args=(index,)) for index in range(8)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

        self.assertEqual(len(minted), 8)
        self.assertEqual(len(set(minted)), 8)
        self.assertEqual(
            sorted(minted),
            [f"REC-20260914-{letter}" for letter in "CDEFGHIJ"],
        )
        data = self.data()
        for receipt in minted:
            self.assertEqual(data.count(receipt.encode("ascii")), 1)
        self.assertPreExistingRegionUnchanged()

    def test_concurrent_processes_append_under_the_file_lock_without_loss(self) -> None:
        worker_source = (
            "import sys\n"
            "sys.path.insert(0, sys.argv[1])\n"
            "from minireason.loop import receipts\n"
            "ledger, worker = sys.argv[2], sys.argv[3]\n"
            "sys.stdin.readline()\n"
            "for index in range(8):\n"
            "    receipts.ledger_append('Process %s paragraph %d: ' % (worker, index)\n"
            "                           + '\\u03c0\\U0001f680 ' * 400, ledger)\n"
        )
        script = self.root / "worker.py"
        script.write_text(worker_source, encoding="utf-8")
        processes = [
            subprocess.Popen(
                [sys.executable, "-X", "utf8", str(script), str(REPO / "src"),
                 str(self.ledger), str(worker)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True,
            )
            for worker in (0, 1)
        ]
        for process in processes:
            process.stdin.write("go\n")
            process.stdin.flush()
        for process in processes:
            _out, err = process.communicate(timeout=120)
            self.assertEqual(process.returncode, 0, err)
        data = self.data()
        self.assertPreExistingRegionUnchanged()
        for worker in (0, 1):
            for index in range(8):
                marker = f"Process {worker} paragraph {index}: ".encode("utf-8")
                self.assertEqual(data.count(marker), 1)
        self.assertEqual(data.decode("utf-8").count("\U0001f680"), 2 * 8 * 400)


class ReceiptIdTests(LedgerTestCase):
    def test_opening_a_receipt_mints_the_next_free_letter(self) -> None:
        self.assertEqual(receipts.mint_receipt_id(self.ledger, today=MOMENT), "REC-20260914-C")
        first = receipts.open_receipt(
            title="First", choice="c", why="w", contribution="k",
            ledger_path=self.ledger, moment=MOMENT,
        )
        second = receipts.open_receipt(
            title="Second", choice="c", why="w", contribution="k",
            ledger_path=self.ledger, moment=MOMENT,
        )
        self.assertEqual((first, second), ("REC-20260914-C", "REC-20260914-D"))

    def test_the_letter_sequence_continues_past_z_without_reusing_a(self) -> None:
        self.assertEqual(receipts.next_letter([]), "A")
        self.assertEqual(receipts.next_letter(["A", "B", "C"]), "D")
        self.assertEqual(receipts.next_letter(["Z"]), "AA")
        self.assertEqual(receipts.next_letter(["AA", "B"]), "AB")
        self.assertEqual(receipts.next_letter(["AZ"]), "BA")

    def test_the_letter_sequence_restarts_at_a_on_each_utc_date(self) -> None:
        tomorrow = MOMENT + datetime.timedelta(days=1)
        receipt = receipts.open_receipt(
            title="Next day", choice="c", why="w", contribution="k",
            ledger_path=self.ledger, moment=tomorrow,
        )
        self.assertEqual(receipt, "REC-20260915-A")

    def test_ids_are_scanned_in_byte_mode_from_the_whole_ledger(self) -> None:
        self.assertEqual(receipts.scan_receipt_ids(FIXTURE, "20260914"), ("A", "B"))
        self.assertEqual(receipts.scan_receipt_ids(FIXTURE, "20260913"), ())
        self.assertEqual(receipts.scan_receipt_ids(b"\xff\xfe REC-20260914-Q x", "20260914"), ("Q",))

    def test_minting_against_a_missing_ledger_starts_at_a(self) -> None:
        self.assertEqual(
            receipts.mint_receipt_id(self.root / "absent.md", today=MOMENT.date()),
            "REC-20260914-A",
        )

    def test_a_follow_up_to_a_malformed_receipt_id_is_refused(self) -> None:
        with self.assertRaises(receipts.ReceiptError) as caught:
            receipts.close_receipt("REC-2026-9-14-A", "done", ledger_path=self.ledger)
        self.assertEqual(caught.exception.code, "RECEIPT_ID_MALFORMED")
        self.assertEqual(self.data(), FIXTURE)

    def test_an_opening_receipt_without_the_four_house_fields_is_refused(self) -> None:
        with self.assertRaises(receipts.ReceiptError) as caught:
            receipts.open_receipt(title="only a title", ledger_path=self.ledger)
        self.assertEqual(caught.exception.code, "RECEIPT_FIELDS_MISSING")
        self.assertEqual(self.data(), FIXTURE)


class HouseStyleTests(LedgerTestCase):
    def test_the_opening_paragraph_carries_choice_why_contribution_and_pending_state(self) -> None:
        receipt = receipts.open_receipt(
            title="Publish the receipts module",
            choice="add one module and one test file",
            why="the loop must write its own receipts",
            contribution="wave 0 of the automated loop",
            evidence="tests pending",
            paths=["src/minireason/loop/receipts.py"],
            source_identity="new modules change the repository-wide source digest",
            ledger_path=self.ledger, moment=MOMENT,
        )
        paragraph = self.tail().strip()
        self.assertTrue(paragraph.startswith(f"{receipt} opened at 2026-09-14 09:30:00 UTC: "))
        for clause in ("Choice:", "Why:", "Contribution:", "Paths:", "Source identity:",
                       "Evidence:", "State: pending."):
            self.assertIn(clause, paragraph)
        self.assertIn("`src/minireason/loop/receipts.py`", paragraph)
        self.assertPreExistingRegionUnchanged()

    def test_outcome_checkpoint_closing_and_erratum_use_the_house_forms(self) -> None:
        receipt = "REC-20260914-A"
        receipts.outcome_receipt(receipt, "the wave landed", "commit abc",
                                 ledger_path=self.ledger, moment=MOMENT)
        receipts.checkpoint_receipt(receipt, "three of six modules written",
                                    next_action="write the tests",
                                    ledger_path=self.ledger, moment=MOMENT)
        receipts.close_receipt(receipt, "everything promised is published",
                               ["commit abc", "tree def"],
                               ledger_path=self.ledger, moment=MOMENT)
        receipts.erratum_receipt(receipt, "one count was wrong", "the count is four",
                                 ledger_path=self.ledger, moment=MOMENT)
        tail = self.tail()
        self.assertIn(f"{receipt} outcome at 2026-09-14 09:30:00 UTC: the wave landed."
                      " Evidence: commit abc.", tail)
        self.assertIn(f"{receipt} progress at 2026-09-14 09:30:00 UTC: three of six modules"
                      " written.", tail)
        self.assertIn(f"{receipt} closed at 2026-09-14 09:30:00 UTC: State pending -> "
                      "**closed**. ", tail)
        self.assertIn(f"{receipt} erratum at 2026-09-14 09:30:00 UTC: Defect: ", tail)
        self.assertIn("This is appended rather than edited into the receipt above, because "
                      "this ledger is append-only.", tail)
        self.assertIn("Next: write the tests.", tail)
        self.assertIn("Evidence: commit abc; tree def.", tail)
        self.assertPreExistingRegionUnchanged()

    def test_a_receipt_paragraph_is_a_single_line_terminated_by_one_newline(self) -> None:
        receipts.outcome_receipt("REC-20260914-A", "one\nline\nafter\nfolding",
                                 ledger_path=self.ledger, moment=MOMENT)
        self.assertEqual(self.tail(), "\nREC-20260914-A outcome at 2026-09-14 09:30:00 UTC: "
                                      "one line after folding.\n")

    def test_a_malformed_receipt_form_is_refused(self) -> None:
        with self.assertRaises(receipts.ReceiptError) as caught:
            receipts.outcome_receipt("REC-20260914-A", "x", form="outcome: extra",
                                     ledger_path=self.ledger, moment=MOMENT)
        self.assertEqual(caught.exception.code, "RECEIPT_FORM_MALFORMED")
        self.assertEqual(self.data(), FIXTURE)


class SecretRefusalTests(LedgerTestCase):
    SECRET = "SYNTHETIC-LOOP-TEST-VALUE-NOT-A-CREDENTIAL"

    def _register(self) -> None:
        patcher = mock.patch.dict(os.environ, {"LOOP_TEST_FAKE_KEY": self.SECRET})
        patcher.start()
        self.addCleanup(patcher.stop)
        compat.register_secret_envs(["LOOP_TEST_FAKE_KEY"])

    def test_a_secret_bearing_body_is_refused_not_redacted(self) -> None:
        self._register()
        with self.assertRaises(receipts.SecretInReceipt) as caught:
            receipts.ledger_append(f"Evidence: the call used {self.SECRET}.", self.ledger)
        self.assertEqual(caught.exception.names, ("LOOP_TEST_FAKE_KEY",))
        self.assertNotIn(self.SECRET, str(caught.exception))
        self.assertEqual(self.data(), FIXTURE)
        self.assertNotIn(compat.REDACTION.encode("ascii"), self.data())

    def test_a_secret_bearing_receipt_field_is_refused_before_an_id_is_spent(self) -> None:
        self._register()
        with self.assertRaises(receipts.SecretInReceipt):
            receipts.open_receipt(title="Dispatch", choice=f"use {self.SECRET}",
                                  why="w", contribution="k",
                                  ledger_path=self.ledger, moment=MOMENT)
        self.assertEqual(self.data(), FIXTURE)
        self.assertEqual(receipts.mint_receipt_id(self.ledger, today=MOMENT), "REC-20260914-C")

    def test_a_secret_bearing_activity_field_is_refused_not_redacted(self) -> None:
        self._register()
        calls: list[list[str]] = []
        with self.assertRaises(receipts.SecretInReceipt):
            receipts.activity("begin", f"call with {self.SECRET}", "why", "goal",
                              decision="REC-20260914-A", repo_root=REPO,
                              runner=lambda argv, **kw: calls.append(argv))
        self.assertEqual(calls, [])


class ActivityTests(LedgerTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.repo = self.root / "repo"
        (self.repo / "tools").mkdir(parents=True)
        (self.repo / "docs").mkdir()
        (self.repo / "tools" / "repo_activity.py").write_bytes(
            (REPO / "tools" / "repo_activity.py").read_bytes()
        )
        self.log = self.repo / "docs" / "AGENT_ACTIVITY.jsonl"

    def events(self) -> list[dict]:
        return [json.loads(line) for line in self.log.read_text("utf-8").splitlines()]

    def test_activity_records_carry_no_raw_command_text(self) -> None:
        argv = receipts.activity(
            "begin", "read the frozen plan and its pins",
            "custody must be checked before dispatch", "publish before dispatching",
            ["experiments/loops/L001/plan.json"],
            decision="REC-20260914-A", repo_root=self.repo,
        )
        self.assertNotIn("--", argv[2:])
        event = self.events()[0]
        self.assertNotIn("command_sha256", event)
        self.assertNotIn("returncode", event)
        self.assertEqual(event["action"], "read the frozen plan and its pins")
        self.assertEqual(event["paths"], ["experiments/loops/L001/plan.json"])
        for marker in ("$(", "&&", "Authorization", "curl "):
            self.assertNotIn(marker, json.dumps(event))

    def test_command_shaped_text_in_an_activity_field_is_refused(self) -> None:
        for field in ("action", "why", "goal"):
            fields = {"action": "a", "why": "w", "goal": "g"}
            fields[field] = "git push && curl -H 'Authorization: Bearer x' https://host"
            with self.assertRaises(receipts.ReceiptError) as caught:
                receipts.activity("begin", fields["action"], fields["why"], fields["goal"],
                                  decision="REC-20260914-A", repo_root=self.repo)
            self.assertEqual(caught.exception.code, "ACTIVITY_RAW_COMMAND_TEXT")
        self.assertFalse(self.log.exists())

    def test_activity_shells_the_repository_logger_with_agent_decision_and_phase(self) -> None:
        receipts.activity("outcome", "publish the wave", "the rule requires a receipt",
                          "keep the record recoverable", decision="REC-20260914-B",
                          repo_root=self.repo)
        argv = receipts.activity("begin", "dispatch one wave", "spending step",
                                 "produce the material", decision="REC-20260914-B",
                                 repo_root=self.repo)
        self.assertEqual(argv[1], str(self.repo / "tools" / "repo_activity.py"))
        self.assertIn("--agent", argv)
        self.assertEqual(argv[argv.index("--agent") + 1], receipts.DEFAULT_AGENT)
        self.assertEqual(argv[argv.index("--decision") + 1], "REC-20260914-B")
        self.assertEqual(argv[argv.index("--phase") + 1], "begin")
        phases = [event["phase"] for event in self.events()]
        self.assertEqual(phases, ["outcome", "begin"])

    def test_the_decision_defaults_to_the_receipt_this_process_opened(self) -> None:
        receipt = receipts.open_receipt(
            title="Open", choice="c", why="w", contribution="k",
            ledger_path=self.ledger, moment=MOMENT,
        )
        receipts.activity("event", "note the open receipt", "why", "goal",
                          repo_root=self.repo)
        self.assertEqual(self.events()[0]["decision"], receipt)

    def test_an_activity_call_without_any_open_receipt_is_refused(self) -> None:
        receipts.set_current_receipt(None)
        with self.assertRaises(receipts.ReceiptError) as caught:
            receipts.activity("begin", "a", "w", "g", repo_root=self.repo)
        self.assertEqual(caught.exception.code, "ACTIVITY_DECISION_MISSING")

    def test_a_phase_outside_the_logger_s_vocabulary_is_refused(self) -> None:
        with self.assertRaises(receipts.ReceiptError) as caught:
            receipts.activity("finish", "a", "w", "g", decision="REC-20260914-A",
                              repo_root=self.repo)
        self.assertEqual(caught.exception.code, "ACTIVITY_PHASE_UNKNOWN")

    def test_bracket_reports_an_interruption_by_type_and_never_its_message(self) -> None:
        with self.assertRaises(ValueError):
            with receipts.bracket("run the guard", "every act is bracketed", "keep the record",
                                  decision="REC-20260914-A", repo_root=self.repo):
                raise ValueError("a message that could contain anything")
        events = self.events()
        self.assertEqual([event["phase"] for event in events], ["begin", "outcome"])
        self.assertIn("interrupted by ValueError", events[1]["why"])
        self.assertNotIn("a message that could contain anything", json.dumps(events))


class CadenceTests(LedgerTestCase):
    def test_a_missed_cadence_deadline_is_recorded_and_never_backdated(self) -> None:
        cadence = receipts.Cadence(MOMENT, ledger_path=self.ledger)
        late = MOMENT + datetime.timedelta(seconds=451)
        appended = cadence.record_checkpoint(late, "REC-20260914-A",
                                             "the step ran long", "step receipt 0012")
        self.assertEqual(len(cadence.misses), 1)
        miss = cadence.misses[0]
        self.assertEqual(miss.deadline_utc, MOMENT + datetime.timedelta(seconds=300))
        self.assertEqual(miss.recorded_utc, late)
        self.assertAlmostEqual(miss.overdue_seconds, 151.0)
        self.assertIn("2026-09-14 09:37:31 UTC", appended.text)
        self.assertIn("was missed and is recorded at the time it was noticed", appended.text)
        self.assertIn("it is not backdated", appended.text)
        self.assertNotIn("REC-20260914-A progress at 2026-09-14 09:30:00 UTC", self.tail())
        self.assertEqual(cadence.since, late)
        self.assertPreExistingRegionUnchanged()

    def test_the_clock_refuses_to_be_moved_backwards(self) -> None:
        cadence = receipts.Cadence(MOMENT, ledger_path=self.ledger)
        cadence.check(MOMENT + datetime.timedelta(seconds=310))
        with self.assertRaises(receipts.ReceiptError) as caught:
            cadence.acknowledge(MOMENT + datetime.timedelta(seconds=300))
        self.assertEqual(caught.exception.code, "CADENCE_BACKDATED")
        with self.assertRaises(receipts.ReceiptError):
            cadence.check(MOMENT)

    def test_the_clock_warns_at_240_seconds_and_is_overdue_at_300(self) -> None:
        cadence = receipts.Cadence(MOMENT, ledger_path=self.ledger)
        self.assertEqual(cadence.check(MOMENT + datetime.timedelta(seconds=239)).state, "ok")
        self.assertEqual(receipts.CADENCE_WARN_SECONDS, 240.0)
        self.assertEqual(receipts.CADENCE_DEADLINE_SECONDS, 300.0)
        warn = cadence.check(MOMENT + datetime.timedelta(seconds=240))
        self.assertEqual(warn.state, "warn")
        self.assertTrue(warn.due)
        self.assertFalse(warn.missed)
        self.assertEqual(cadence.misses, ())
        overdue = cadence.check(MOMENT + datetime.timedelta(seconds=300))
        self.assertEqual(overdue.state, "overdue")
        self.assertTrue(overdue.missed)
        self.assertEqual(len(cadence.misses), 1)
        cadence.check(MOMENT + datetime.timedelta(seconds=420))
        self.assertEqual(len(cadence.misses), 1)

    def test_an_acknowledged_receipt_restarts_the_five_minute_clock(self) -> None:
        cadence = receipts.Cadence(MOMENT, ledger_path=self.ledger)
        cadence.record_checkpoint(MOMENT + datetime.timedelta(seconds=250),
                                  "REC-20260914-A", "progress")
        state = cadence.check(MOMENT + datetime.timedelta(seconds=300))
        self.assertEqual(state.state, "ok")
        self.assertEqual(cadence.misses, ())

    def test_a_naive_moment_is_refused_because_it_has_no_utc_meaning(self) -> None:
        with self.assertRaises(receipts.ReceiptError) as caught:
            receipts.Cadence(datetime.datetime(2026, 9, 14, 9, 30, 0))
        self.assertEqual(caught.exception.code, "MOMENT_NOT_AWARE")


class PreregistrationTests(LedgerTestCase):
    def test_the_preregistration_carries_every_required_sentence_verbatim(self) -> None:
        text = receipts.render_preregistration("REC-20260914-C", "2026-09-14 09:30:00 UTC")
        self.assertEqual(len(receipts.PREREGISTRATION_REQUIRED_SENTENCES), 10)
        for sentence in receipts.PREREGISTRATION_REQUIRED_SENTENCES:
            self.assertIn(sentence, text)

    def test_the_preregistration_names_c001_s_frozen_plan_id_and_amends_nothing(self) -> None:
        text = receipts.render_preregistration("REC-20260914-C", "2026-09-14 09:30:00 UTC")
        self.assertIn(receipts.C001_PLAN_ID, text)
        self.assertIn("It does not amend, reopen, supersede or reinterpret C001", text)
        self.assertIn("**Not authorised under this receipt.**", text)
        self.assertNotIn("exhaustion", text)

    def test_the_renderer_refuses_when_a_required_sentence_is_missing(self) -> None:
        extra = receipts.PREREGISTRATION_REQUIRED_SENTENCES + ("a sentence never rendered",)
        with mock.patch.object(receipts, "PREREGISTRATION_REQUIRED_SENTENCES", extra):
            with self.assertRaises(receipts.ReceiptError) as caught:
                receipts.render_preregistration("REC-20260914-C", "2026-09-14 09:30:00 UTC")
        self.assertEqual(caught.exception.code, "PREREGISTRATION_SENTENCE_MISSING")

    def test_the_preregistration_is_appended_under_the_minted_receipt_id(self) -> None:
        receipt = receipts.open_preregistration(self.ledger, loop_plan_id="a" * 64,
                                                run_id="L001", moment=MOMENT)
        self.assertEqual(receipt, "REC-20260914-C")
        tail = self.tail()
        self.assertTrue(tail.startswith(
            "\n**REC-20260914-C opened at 2026-09-14 09:30:00 UTC: pre-register the automated "
            "end-to-end harness loop as a mechanism intervention with its own identity.**\n\n"
        ))
        self.assertIn("The identity minted for this run is `loop_plan_id " + "a" * 64 + "`.", tail)
        self.assertIn("Its run directory is `experiments/loops/L001/`.", tail)
        for sentence in receipts.PREREGISTRATION_REQUIRED_SENTENCES:
            self.assertIn(sentence, tail)
        self.assertPreExistingRegionUnchanged()

    def test_a_source_identity_disclosure_is_rendered_when_one_is_given(self) -> None:
        text = receipts.render_preregistration(
            "REC-20260914-C", "2026-09-14 09:30:00 UTC",
            source_identity="new loop modules change the repository-wide source digest",
        )
        self.assertIn("Source identity disclosed: new loop modules change the "
                      "repository-wide source digest.", text)

    def test_a_malformed_receipt_id_is_refused_by_the_renderer(self) -> None:
        with self.assertRaises(receipts.ReceiptError) as caught:
            receipts.render_preregistration("REC-A", "2026-09-14 09:30:00 UTC")
        self.assertEqual(caught.exception.code, "RECEIPT_ID_MALFORMED")


class ModuleSurfaceTests(unittest.TestCase):
    def test_every_exported_name_exists(self) -> None:
        for name in receipts.__all__:
            self.assertTrue(hasattr(receipts, name), name)

    def test_the_module_writes_nothing_outside_the_ledger_and_the_activity_log(self) -> None:
        self.assertEqual(receipts.LEDGER_RELATIVE, "docs/DECISION_LEDGER.md")
        self.assertEqual(receipts.ACTIVITY_TOOL_RELATIVE, "tools/repo_activity.py")
        self.assertTrue((REPO / receipts.ACTIVITY_TOOL_RELATIVE).is_file())
        self.assertEqual(receipts.DEFAULT_LEDGER_PATH, REPO / receipts.LEDGER_RELATIVE)


class TheDefaultsAreFoundRatherThanCounted(unittest.TestCase):
    """S2: ``parents[3]`` is the repository only in a source checkout.

    In an installed wheel it names ``site-packages``' parent, which carries no
    ``tools/repo_activity.py`` — so the default ledger was a *new* file in
    whatever directory that happened to be, and two agents each minted
    ``REC-<date>-A`` into their own copy.
    """

    def test_the_repository_root_is_the_one_carrying_the_activity_logger(self) -> None:
        self.assertEqual(receipts.DEFAULT_REPO_ROOT, REPO)
        self.assertTrue((receipts.DEFAULT_REPO_ROOT
                         / receipts.ACTIVITY_TOOL_RELATIVE).is_file())
        self.assertEqual(receipts.DEFAULT_LEDGER_PATH, REPO / receipts.LEDGER_RELATIVE)

    def test_outside_a_checkout_the_default_is_none_and_the_refusal_is_named(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            elsewhere = Path(directory) / "site-packages" / "minireason" / "loop"
            elsewhere.mkdir(parents=True)
            with mock.patch.object(receipts, "__file__", str(elsewhere / "receipts.py")):
                self.assertIsNone(receipts._repository_root())
        for call in (lambda: receipts.ledger_append("x", None),
                     lambda: receipts.mint_receipt_id(None),
                     lambda: receipts.open_receipt(title="t", choice="c", why="w",
                                                   contribution="k", ledger_path=None)):
            with self.assertRaises(receipts.ReceiptError) as caught:
                call()
            self.assertEqual(caught.exception.code, "LEDGER_NOT_FOUND")
        with self.assertRaises(receipts.ReceiptError) as caught:
            receipts.activity("begin", "a", "w", "g", decision="REC-20260914-A",
                              repo_root=None)
        self.assertEqual(caught.exception.code, "ACTIVITY_TOOL_MISSING")


class TheActivityLoggerFailsUnderACode(LedgerTestCase):
    """S3: a timed-out logger escaped the code table entirely."""

    def setUp(self) -> None:
        super().setUp()
        self.repo = self.root / "repo"
        (self.repo / "tools").mkdir(parents=True)
        (self.repo / "tools" / "repo_activity.py").write_bytes(
            (REPO / "tools" / "repo_activity.py").read_bytes())

    def call(self, runner):
        return receipts.activity("begin", "a", "w", "g", decision="REC-20260914-A",
                                 repo_root=self.repo, runner=runner)

    def test_a_timed_out_logger_raises_activity_logger_failed(self) -> None:
        def timing_out(argv, **kwargs):
            raise subprocess.TimeoutExpired(argv, kwargs.get("timeout", 30.0))

        with self.assertRaises(receipts.ReceiptError) as caught:
            self.call(timing_out)
        self.assertEqual(caught.exception.code, "ACTIVITY_LOGGER_FAILED")
        self.assertIn("timed out", caught.exception.detail)
        # It is a LoopError, so one ``except LoopError`` names a failure_code.
        self.assertIsInstance(caught.exception, receipts.LoopError)

    def test_a_runner_that_returns_no_returncode_is_not_a_silent_success(self) -> None:
        class NoReturncode:
            pass

        with self.assertRaises(receipts.ReceiptError) as caught:
            self.call(lambda argv, **kwargs: NoReturncode())
        self.assertEqual(caught.exception.code, "ACTIVITY_LOGGER_FAILED")
        self.assertIn("returncode", caught.exception.detail)

    def test_a_non_zero_exit_still_names_the_exit_status(self) -> None:
        class Failed:
            returncode = 3

        with self.assertRaises(receipts.ReceiptError) as caught:
            self.call(lambda argv, **kwargs: Failed())
        self.assertEqual(caught.exception.code, "ACTIVITY_LOGGER_FAILED")
        self.assertIn("exit 3", caught.exception.detail)

    def test_check_false_still_asks_nothing_of_the_result(self) -> None:
        argv = receipts.activity("begin", "a", "w", "g", decision="REC-20260914-A",
                                 repo_root=self.repo, check=False,
                                 runner=lambda argv, **kwargs: None)
        self.assertEqual(argv[argv.index("--phase") + 1], "begin")


class MintingIsCollisionFreeAcrossProcesses(LedgerTestCase):
    """S9: the load-bearing claim is about two processes, and only threads were tested.

    ``_APPEND_LOCK`` is an ``RLock``, which already serialises eight threads in one
    process, so the threaded test could not fail for the reason the claim is about.
    This runs three real processes that mint and append under the ``flock``.
    """

    WORKER = (
        "import sys\n"
        "sys.path.insert(0, sys.argv[1])\n"
        "from minireason.loop import receipts\n"
        "import datetime\n"
        "ledger, worker = sys.argv[2], sys.argv[3]\n"
        "moment = datetime.datetime(2026, 9, 14, 9, 30, tzinfo=datetime.timezone.utc)\n"
        "sys.stdin.readline()\n"
        "for index in range(12):\n"
        "    print(receipts.open_receipt(\n"
        "        title='Process %s receipt %d' % (worker, index),\n"
        "        choice='mint under the append lock', why='two agents may open at once',\n"
        "        contribution='wave 0', ledger_path=ledger, moment=moment,\n"
        "        set_current=False))\n"
    )

    def test_three_processes_minting_at_once_never_reuse_a_letter(self) -> None:
        script = self.root / "minting_worker.py"
        script.write_text(self.WORKER, encoding="utf-8")
        processes = [
            subprocess.Popen(
                [sys.executable, "-X", "utf8", str(script), str(REPO / "src"),
                 str(self.ledger), str(worker)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True)
            for worker in range(3)
        ]
        for process in processes:            # the barrier: nobody starts until all exist
            process.stdin.write("go\n")
            process.stdin.flush()
        minted: list[str] = []
        for process in processes:
            out, err = process.communicate(timeout=180)
            self.assertEqual(process.returncode, 0, err)
            minted.extend(line.strip() for line in out.splitlines() if line.strip())

        self.assertEqual(len(minted), 36)
        self.assertEqual(len(set(minted)), 36, "two processes minted the same id")
        data = self.data()
        for receipt in minted:
            with self.subTest(receipt=receipt):
                self.assertEqual(data.count(receipt.encode("ascii")), 1,
                                 "one receipt, one paragraph")
        # C and D were already used by the fixture's A and B... no: the fixture
        # carries A and B, so the 36 ids are the next 36 letters in sequence.
        self.assertEqual(sorted(minted), sorted(
            f"REC-20260914-{letter}" for letter in
            [chr(c) for c in range(ord("C"), ord("Z") + 1)]
            + ["A" + chr(c) for c in range(ord("A"), ord("L") + 1)]))
        self.assertPreExistingRegionUnchanged()


class ImportingTheModuleLoadsNoEndpointRegistry(unittest.TestCase):
    """N3: importing a ledger writer has no business reading endpoints.json."""

    def test_importing_receipts_does_not_import_the_transport(self) -> None:
        probe = (
            "import sys\n"
            "sys.path.insert(0, sys.argv[1])\n"
            "import minireason.loop.receipts\n"
            "print('minireason.provider_openai_compat' in sys.modules)\n"
        )
        done = subprocess.run([sys.executable, "-X", "utf8", "-c", probe,
                               str(REPO / "src")],
                              capture_output=True, text=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(done.stdout.strip(), "False", done.stdout)

    def test_the_credential_scan_still_reaches_the_transports_own_scanner(self) -> None:
        secret = "SYNTHETIC-LOOP-TEST-OTHER-VALUE-NOT-A-CREDENTIAL"
        with mock.patch.dict(os.environ, {"LOOP_TEST_LAZY_KEY": secret}):
            compat.register_secret_envs(["LOOP_TEST_LAZY_KEY"])
            self.assertEqual(list(receipts._redact_with_names(f"a {secret} b")[1]),
                             ["LOOP_TEST_LAZY_KEY"])


class HardeningFindings(LedgerTestCase):
    """One test per item of the wave-1 integration decisions, items 29-32."""

    def test_item29_a_render_that_omits_the_minted_id_spends_no_letter(self):
        """Item 29: the id was minted and the paragraph never carried it.

        Two callers then got the same id with no contention at all, and the
        second receipt's paragraphs were addressed to the first's.
        """

        before = self.data()
        for render in (lambda rid, stamp: f"**opened at {stamp}: no id here.**",
                       lambda rid, stamp: f"**{rid.lower()} opened at {stamp}.**",
                       lambda rid, stamp: "**REC-19700101-A opened.**"):
            with self.subTest(render=render(  "REC-20260914-Z", "now")[:24]):
                with self.assertRaises(receipts.ReceiptError) as caught:
                    receipts.open_receipt(render=render, ledger_path=self.ledger)
                self.assertEqual(caught.exception.code, "RECEIPT_ID_MALFORMED")
        self.assertEqual(self.data(), before, "the ledger moved on a refusal")
        # Two renders that DO carry the id get two ids.
        first = receipts.open_receipt(
            render=lambda rid, stamp: f"**{rid} opened at {stamp}: one.**",
            ledger_path=self.ledger)
        second = receipts.open_receipt(
            render=lambda rid, stamp: f"**{rid} opened at {stamp}: two.**",
            ledger_path=self.ledger)
        self.assertNotEqual(first, second)

    def test_item30_the_default_root_needs_a_git_beside_the_marker(self):
        """Item 30: an installed wheel under someone else's checkout."""

        self.assertIs(receipts._repository_root.__module__, receipts.__name__)
        outer = self.root / "someones-checkout"
        (outer / ".git").mkdir(parents=True)
        (outer / "tools").mkdir()
        (outer / "tools" / "repo_activity.py").write_text("#\n", encoding="utf-8")
        venv = outer / ".venv" / "lib" / "python3.11" / "site-packages"
        package = venv / "minireason" / "loop"
        package.mkdir(parents=True)
        planted = package / "receipts.py"
        planted.write_text("#\n", encoding="utf-8")
        with mock.patch.object(receipts, "__file__", str(planted)):
            self.assertIsNone(receipts._repository_root())
        # Stop at the fixture boundary even when TMP is inside a real checkout.
        (self.root / ".git").mkdir()
        # A marker with no .git beside it is not a checkout either.
        bare = self.root / "not-a-checkout"
        (bare / "tools").mkdir(parents=True)
        (bare / "tools" / "repo_activity.py").write_text("#\n", encoding="utf-8")
        deep = bare / "a" / "b"
        deep.mkdir(parents=True)
        with mock.patch.object(receipts, "__file__", str(deep / "receipts.py")):
            self.assertIsNone(receipts._repository_root())
        # This checkout still resolves, because it has both.
        self.assertEqual(receipts._repository_root(), receipts.DEFAULT_REPO_ROOT)

    def test_item30_preflight_refuses_a_driver_that_leans_on_the_default(self):
        for ledger, root in ((None, self.root), (self.ledger, None), (None, None)):
            with self.subTest(ledger=ledger, root=root):
                with self.assertRaises(receipts.ReceiptError) as caught:
                    receipts.assert_explicit_paths(ledger, root)
                self.assertEqual(caught.exception.code, "LEDGER_NOT_FOUND")
        self.assertIsNone(receipts.assert_explicit_paths(self.ledger, self.root))

    def test_item31a_a_refused_first_append_leaves_no_zero_byte_ledger(self):
        fresh = self.root / "new" / "LEDGER.md"
        fresh.parent.mkdir()
        with self.assertRaises(receipts.ReceiptError) as caught:
            receipts.ledger_append("   ", fresh, create=True)
        self.assertEqual(caught.exception.code, "LEDGER_EMPTY_PARAGRAPH")
        self.assertFalse(fresh.exists(), "a zero-byte ledger was left behind")
        # ... so the next caller still starts at A in a ledger it meant to make.
        receipt = receipts.open_receipt(title="T.", choice="C.", why="W.",
                                        contribution="K.", ledger_path=fresh,
                                        create=True)
        self.assertTrue(receipt.endswith("-A"))

    def test_item31b_a_logger_that_cannot_be_run_is_a_receipt_error(self):
        def explode(*args, **kwargs):
            raise OSError("Exec format error: /usr/bin/python3 --api-key sk-xyz")

        with self.assertRaises(receipts.ReceiptError) as caught:
            receipts.activity("begin", "act", "why", "goal",
                              decision="REC-20260914-A", repo_root=self.repo_root(),
                              runner=explode)
        self.assertEqual(caught.exception.code, "ACTIVITY_LOGGER_FAILED")
        self.assertIn("OSError", caught.exception.detail)
        self.assertNotIn("sk-xyz", str(caught.exception))

    def test_item31c_a_logger_failure_never_replaces_the_bracketed_failure(self):
        calls = []

        def failing_outcome(argv, **kwargs):
            calls.append(argv)
            if "--phase" in argv and argv[argv.index("--phase") + 1] == "outcome":
                raise subprocess.SubprocessError("the logger died")
            return subprocess.CompletedProcess(argv, 0)

        receipts.set_current_receipt("REC-20260914-A")
        with self.assertRaises(ZeroDivisionError) as caught:
            with receipts.bracket("act", "why", "goal", repo_root=self.repo_root(),
                                  runner=failing_outcome):
                raise ZeroDivisionError("the act that actually failed")
        notes = " ".join(getattr(caught.exception, "__notes__", ()))
        self.assertIn("ACTIVITY_LOGGER_FAILED", notes)
        self.assertEqual(len(calls), 2)

    def test_item31d_a_receipt_says_one_thing_and_says_it_with_content(self):
        cases = (
            ("RECEIPT_FIELDS_MISSING",
             dict(title="  ", choice="C.", why="W.", contribution="K.")),
            ("RECEIPT_FIELDS_MISSING", dict(body="   ")),
            ("RECEIPT_BODY_AMBIGUOUS", dict(body="A body.", title="T.")),
            ("RECEIPT_BODY_AMBIGUOUS",
             dict(body="A body.", source_identity="sha256:abc")),
            ("RECEIPT_BODY_AMBIGUOUS",
             dict(render=lambda rid, stamp: f"**{rid}**", choice="C.")),
            ("RECEIPT_FIELDS_MISSING",
             dict(title="T.", choice="C.", why="W.", contribution="K.",
                  paths="docs/one.md")),
        )
        for code, kwargs in cases:
            with self.subTest(code=code, kwargs=sorted(kwargs)):
                with self.assertRaises(receipts.ReceiptError) as caught:
                    receipts.open_receipt(ledger_path=self.ledger, **kwargs)
                self.assertEqual(caught.exception.code, code)

    def test_item31e_the_command_text_scan_reads_the_spellings_it_names(self):
        for text in ("--api-key sk-1", "--key sk-1", "X-Api-Key: sk-1",
                     "x-api-key: sk-1", "https://user:pw@example.invalid/x",
                     "--token abc", "wget http://example.invalid"):
            with self.subTest(text=text[:24]):
                with self.assertRaises(receipts.ReceiptError) as caught:
                    receipts.activity("begin", text, "why", "goal",
                                      decision="REC-20260914-A",
                                      repo_root=self.repo_root(),
                                      runner=lambda argv, **k:
                                      subprocess.CompletedProcess(argv, 0))
                self.assertEqual(caught.exception.code, "ACTIVITY_RAW_COMMAND_TEXT")
        # Ordinary prose still passes.
        self.assertTrue(receipts.activity(
            "begin", "read the ledger", "to find the open receipt", "close it",
            decision="REC-20260914-A", repo_root=self.repo_root(),
            runner=lambda argv, **k: subprocess.CompletedProcess(argv, 0)))

    def test_item31f_a_path_that_is_an_option_is_refused_before_argv(self):
        for paths in (["--agent"], ["-rf"], ["  "], "docs/one.md"):
            with self.subTest(paths=paths):
                with self.assertRaises(receipts.ReceiptError) as caught:
                    receipts.activity("begin", "act", "why", "goal", paths,
                                      decision="REC-20260914-A",
                                      repo_root=self.repo_root(),
                                      runner=lambda argv, **k:
                                      subprocess.CompletedProcess(argv, 0))
                self.assertEqual(caught.exception.code, "ACTIVITY_PATH_INVALID")

    def test_item31g_one_miss_is_disclosed_with_one_set_of_numbers(self):
        started = datetime.datetime(2026, 9, 14, 9, 0, tzinfo=datetime.timezone.utc)
        clock = receipts.Cadence(started, ledger_path=self.ledger)
        noticed = started + datetime.timedelta(seconds=400)
        check = clock.check(noticed)
        self.assertTrue(check.missed)
        written = noticed + datetime.timedelta(seconds=120)
        receipt = receipts.open_receipt(title="T.", choice="C.", why="W.",
                                        contribution="K.", ledger_path=self.ledger,
                                        moment=started)
        appended = receipts.checkpoint_receipt(receipt, "still going", cadence=check,
                                               ledger_path=self.ledger, moment=written)
        text = appended.text
        # The miss keeps the numbers the clock recorded ...
        self.assertIn(receipts._stamp(check.deadline_utc), text)
        self.assertIn(receipts._stamp(check.now), text)
        self.assertIn(f"{check.overdue_seconds:.0f} s overdue", text)
        # ... and the paragraph's own lateness is named as its own fact.
        self.assertIn("written 220 s after that deadline", text)

    def test_item32_the_append_digest_is_taken_before_the_lock_is_released(self):
        receipt = receipts.open_receipt(title="T.", choice="C.", why="W.",
                                        contribution="K.", ledger_path=self.ledger)
        appended = receipts.outcome_receipt(receipt, "it worked",
                                            ledger_path=self.ledger)
        import hashlib
        self.assertEqual(appended.sha256,
                         hashlib.sha256(self.data()).hexdigest())
        self.assertEqual(self.data()[appended.offset:appended.end],
                         (appended.text + "\n").encode("utf-8")
                         if appended.offset == 0 else
                         self.data()[appended.offset:appended.end])

    def test_item32_a_render_that_appends_is_refused_rather_than_deadlocked(self):
        def appends(receipt_id, stamp):
            receipts.ledger_append("**a second paragraph.**", self.ledger)
            return f"**{receipt_id} opened at {stamp}: one.**"

        with self.assertRaises(receipts.ReceiptError) as caught:
            receipts.open_receipt(render=appends, ledger_path=self.ledger)
        self.assertEqual(caught.exception.code, "LEDGER_APPEND_REENTERED")

    def test_item32_a_follow_up_may_not_be_stamped_before_the_one_above_it(self):
        first = datetime.datetime(2026, 9, 14, 9, 0, tzinfo=datetime.timezone.utc)
        receipt = receipts.open_receipt(title="T.", choice="C.", why="W.",
                                        contribution="K.", ledger_path=self.ledger,
                                        moment=first)
        receipts.outcome_receipt(receipt, "step one", ledger_path=self.ledger,
                                 moment=first + datetime.timedelta(minutes=5))
        with self.assertRaises(receipts.ReceiptError) as caught:
            receipts.outcome_receipt(receipt, "step zero", ledger_path=self.ledger,
                                     moment=first)
        self.assertEqual(caught.exception.code, "CADENCE_BACKDATED")
        # A second ledger is a second record and is not ordered by the first.
        other = self.root / "OTHER.md"
        other.write_bytes(FIXTURE)
        self.assertTrue(receipts.outcome_receipt(receipt, "step zero elsewhere",
                                                 ledger_path=other, moment=first))

    def test_item32_a_negative_cadence_threshold_is_refused(self):
        started = datetime.datetime(2026, 9, 14, 9, 0, tzinfo=datetime.timezone.utc)
        for kwargs in ({"warn_seconds": -1.0, "deadline_seconds": 300.0},
                       {"warn_seconds": 0.0, "deadline_seconds": 300.0},
                       {"warn_seconds": 240.0, "deadline_seconds": -300.0}):
            with self.subTest(**kwargs):
                with self.assertRaises(receipts.ReceiptError) as caught:
                    receipts.Cadence(started, ledger_path=self.ledger, **kwargs)
                self.assertIn(caught.exception.code,
                              ("CADENCE_THRESHOLD_INVALID",
                               "CADENCE_THRESHOLDS_INVERTED"))

    def test_item32_activity_refuses_a_decision_that_is_not_a_receipt_id(self):
        for decision in ("REC-2026-A", "rec-20260914-a", "nothing", "REC-20260914-"):
            with self.subTest(decision=decision):
                with self.assertRaises(receipts.ReceiptError) as caught:
                    receipts.activity("begin", "act", "why", "goal",
                                      decision=decision, repo_root=self.repo_root(),
                                      runner=lambda argv, **k:
                                      subprocess.CompletedProcess(argv, 0))
                self.assertEqual(caught.exception.code, "RECEIPT_ID_MALFORMED")

    def repo_root(self) -> Path:
        root = self.root / "repo-for-activity"
        tool = root / "tools" / "repo_activity.py"
        if not tool.exists():
            tool.parent.mkdir(parents=True, exist_ok=True)
            tool.write_text("#\n", encoding="utf-8")
        return root


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
