"""Offline resume proof over the preserved L003 record; never runs the driver.

The fixture keeps the original repository-relative run paths, so rendered-files
and decision-file identities are compared with the actual 0024/0025 receipts.
All fixture copies preserve the original UTF-8 bytes and line endings.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from types import SimpleNamespace

from minireason.loop import custody, graph, obligations, reader, report, steps
from minireason.loop.types import LoopConfig, LoopError
from tools import auto_loop


REPOSITORY = Path(__file__).resolve().parents[2]
RUN_RELATIVE = Path("experiments/loops/L003-loop-first-live-2026-09-14")
TEMP_ROOT = Path(tempfile.gettempdir()) / "resume-reload"


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as stream:
        return stream.read()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        stream.write(text)
    if read_text(path) != text:
        raise AssertionError(f"UTF-8 copy changed bytes: {path}")


def read_json(path: Path):
    return json.loads(read_text(path))


def file_digest(path: Path) -> str:
    return hashlib.sha256(read_text(path).encode("utf-8")).hexdigest()


def copy_text_tree(source: Path, target: Path) -> None:
    for path in sorted(source.rglob("*")):
        if path.is_file():
            write_text(target / path.relative_to(source), read_text(path))


def refuse_external(*_args, **_kwargs):
    raise AssertionError("resume reload proof attempted a provider, socket or subprocess")


class ResumeReloadL003Tests(unittest.TestCase):
    def setUp(self):
        source = REPOSITORY / RUN_RELATIVE
        if not (source / "steps/0024-ADJUDICATE.json").is_file():
            self.skipTest("NOT FOUND: preserved L003 steps/0024-ADJUDICATE.json")
        TEMP_ROOT.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="reload-", dir=TEMP_ROOT)
        self.root = Path(self.temporary.name).resolve()
        self.assertTrue(self.root.is_relative_to(TEMP_ROOT.resolve()))
        self.addCleanup(self.temporary.cleanup)
        self.run_root = self.root / RUN_RELATIVE
        copy_text_tree(source, self.run_root)
        # _mark_cells resolves the declared C001 source for deterministic order.
        contrast = Path("experiments/diagnostics/C001-contrast-triple/occurrence-02")
        for relative in ("comparison.json", "material.json",
                         "juxtaposition/deepseek-flash__fcl.md"):
            write_text(self.root / contrast / relative,
                       read_text(REPOSITORY / contrast / relative))
        self.source_digests = {
            str(path.relative_to(source)): file_digest(path)
            for path in source.rglob("*") if path.is_file()
        }
        self.guard = contextlib.ExitStack()
        self.addCleanup(self.guard.close)
        for target in ("socket.socket", "socket.create_connection",
                       "subprocess.Popen", "subprocess.run",
                       "minireason.provider_openai_compat._open",
                       "minireason.provider_openai_compat.OpenAICompatProvider.__init__",
                       "minireason.provider_openai_compat.OfflineProvider.__init__"):
            self.guard.enter_context(mock.patch(target, side_effect=refuse_external))
        config = LoopConfig.from_mapping(read_json(self.run_root / "config.json"))
        self.driver = auto_loop._Driver(
            config, auto_loop.Modules(repo_root=self.root,
                                      provider_factory=refuse_external))
        drv = self.driver
        drv.plan = read_json(self.run_root / "plan.json")
        drv.plan_id = drv.plan["loop_plan_id"]
        drv.ledger = steps.StepLedger(self.run_root, drv.plan_id,
                                      timeouts=config.timeouts, ledger_path=None)
        drv.harness = graph.open_graph(self.run_root / "graph",
                                       clock=graph.fixed_clock())
        drv.obligations = obligations.load_obligations(
            self.root / config.obligations_path)
        state = read_json(self.run_root / "_run.json")
        drv.ended_arms = list(state.get("arms_ended", []))
        drv.since_seq = int(state.get("since_seq", 0))

    def tearDown(self):
        source = REPOSITORY / RUN_RELATIVE
        self.assertEqual(self.source_digests, {
            str(path.relative_to(source)): file_digest(path)
            for path in source.rglob("*") if path.is_file()
        }, "the original L003 evidence must remain unchanged")

    def receipt(self, filename: str):
        return read_json(self.run_root / "steps" / filename)

    def reload_cycle(self):
        outcomes = {}
        run_step = self.driver._run_step

        def capture(kind, cycle, inputs, fn, **kwargs):
            outcome = run_step(kind, cycle, inputs, fn, **kwargs)
            outcomes[kind] = outcome
            return outcome

        with mock.patch.object(self.driver, "_run_step", side_effect=capture):
            readings = auto_loop._read(self.driver, 1, [])
            auto_loop._mark(self.driver, 1)
        self.assertEqual("SKIPPED", outcomes["READ"].status)
        self.assertEqual("SKIPPED", outcomes["MARK"].status)
        self.assertIsNotNone(readings)
        self.assertEqual(0, readings.planned)
        self.assertEqual(0, readings.dispatched)
        self.assertEqual(0, self.driver.block_streaks[1])
        self.assertEqual(1, len(self.driver.marks_by_cycle[1]))
        marks = self.driver.marks_by_cycle[1][0]
        self.assertEqual(
            ("ORIGINAL vs CONTROL", "ORIGINAL vs RECODING", "ORIGINAL vs CARRIER"),
            tuple(marks.comparisons))
        for comparison in marks.comparisons.values():
            self.assertEqual(("T", "E", "D", "G"), tuple(comparison.rows))
            for row in comparison.rows.values():
                self.assertIsInstance(row.forced_by, tuple)
        blocks = auto_loop._cycle_state(self.driver, 1).blocks
        self.assertEqual(9, len(blocks))
        self.assertEqual(5, sum(reason == "baseline-forced-same" for _, reason in blocks))
        self.assertEqual(4, sum(reason == "provider" for _, reason in blocks))
        return outcomes

    def test_real_l003_replays_identical_adjudicate_and_decide_digests(self):
        drv = self.driver
        original_tables = {
            drv.rel(drv.paths.reading_table): read_text(drv.paths.reading_table),
            drv.rel(drv.paths.comparison): read_text(drv.paths.comparison),
        }
        self.reload_cycle()
        rendered = auto_loop._render_tables(drv, 1)
        self.assertEqual(original_tables, rendered)
        # Assert disk bytes too: default newline translation used to add CR on Windows.
        for relative, text in rendered.items():
            self.assertEqual(text.encode("utf-8"),
                             read_text(self.root / relative).encode("utf-8"))
        outcomes = {}
        run_step = drv._run_step

        def capture(kind, cycle, inputs, fn, **kwargs):
            outcome = run_step(kind, cycle, inputs, fn, **kwargs)
            outcomes[kind] = outcome
            return outcome

        with mock.patch.object(drv, "_run_step", side_effect=capture):
            situation = auto_loop.adjudicate(_driver=drv, _cycle=1)
            decision = auto_loop._decide(drv, 1, None, situation, None)
        for kind, filename in (("ADJUDICATE", "0024-ADJUDICATE.json"),
                               ("DECIDE", "0025-DECIDE.json")):
            self.assertEqual("REPLAYED", outcomes[kind].status)
            expected = self.receipt(filename)["outputs_sha256"]
            self.assertEqual(expected, dict(outcomes[kind].outputs))
            print(f"L003 {filename}: exact outputs_sha256 MATCH {json.dumps(expected, sort_keys=True)}")
        self.assertFalse(decision.stop)
        self.assertEqual("chain_open", decision.reason)
        self.assertEqual(26, len(drv.ledger.records()))

    def test_cycle_publication_writes_lf_bytes(self):
        drv = self.driver
        self.reload_cycle()
        situation = auto_loop.adjudicate(_driver=drv, _cycle=1)
        decision = auto_loop._decide(drv, 1, None, situation, None)
        # Exercise the real renderer and file write with Git publication disabled.
        with mock.patch.object(drv, "_publish") as publish:
            auto_loop._publish_cycle(drv, 1, decision)
        publish.assert_called_once()
        body = read_text(drv.paths.cycle(1).cycle_md).encode("utf-8")
        self.assertIn(b"\n", body)
        self.assertNotIn(b"\r\n", body)
        expected = report.render_cycle(decision, auto_loop._cycle_state(drv, 1))
        self.assertEqual(expected.encode("utf-8"), body)

    def test_missing_reload_would_change_real_adjudicate_identity(self):
        drv = self.driver
        rendered = auto_loop._render_tables(drv, 1)
        material_id = custody.sha256_bytes(custody.encoded(report.rendered_files_record(rendered)))
        digest = custody.digest({"files": sorted(rendered), "id": material_id})
        expected = self.receipt("0024-ADJUDICATE.json")["outputs_sha256"]["rendered_files"]
        self.assertNotEqual(expected, digest)
        self.assertEqual((), auto_loop._cycle_state(drv, 1).blocks)

    def test_repeated_skips_do_not_duplicate_blocks(self):
        self.reload_cycle()
        before = auto_loop._cycle_state(self.driver, 1)
        self.reload_cycle()
        self.assertEqual(before.blocks, auto_loop._cycle_state(self.driver, 1).blocks)

    def test_corrupt_mark_result_is_refused_before_render(self):
        path = self.run_root / "cycles/cycle-01/contrast/deepseek-flash__fcl/marks.json"
        record = read_json(path)
        comparison = next(iter(record["comparisons"].values()))
        row = next(iter(comparison["registers"].values()))
        row["block"] = None if row["block"] else "blocked:provider"
        write_text(path, json.dumps(record, ensure_ascii=False, indent=2) + "\n")
        with self.assertRaises(steps.StepNondeterministic) as caught:
            auto_loop._mark(self.driver, 1)
        self.assertEqual(["marks"], list(caught.exception.differing))
        self.assertNotIn(1, self.driver.marks_by_cycle)

    def test_missing_mark_result_is_refused_before_render(self):
        path = self.run_root / "cycles/cycle-01/contrast/deepseek-flash__fcl/marks.json"
        path.unlink()
        with self.assertRaises((OSError, LoopError)):
            auto_loop._mark(self.driver, 1)
        self.assertNotIn(1, self.driver.marks_by_cycle)


    def test_nonempty_read_records_restore_and_later_cycle_skips(self):
        drv = self.driver
        keys = ["synthetic/blocked", "synthetic/registered",
                "synthetic/indeterminate", "synthetic/disposition"]
        cells = [auto_loop.cell_key_for(key) for key in keys]
        rows = [{"row_key": key, "cell": cell} for key, cell in zip(keys, cells)]
        block = reader.BlockRecord(keys[0], cells[0], "blocked:provider", "delivery",
                                   prompt_ref_path="row/critic/provider/call.request.json")
        reading = reader.RegisteredReading(
            keys[1], cells[1], "att", "judge-1", {"critic": "critic"},
            graph.ReadingIds(cells[1], *(["a" * 64] * 7)))
        pending = reader.IndeterminateRecord(keys[2], "pending/critic", "unanswered")
        disposition = reader.RowDisposition(keys[3], cells[3],
                                            reader.DISPOSITION_OUTSIDE_VOCABULARY,
                                            "preserve the proposed relation")
        original = reader.Readings(
            blocks=(block,), registered=(reading,), indeterminate=(pending,),
            dispositions=(disposition,), unread=frozenset([cells[0], *cells[2:]]),
            planned=4, dispatched=3)
        for key, filename, record in (
                (keys[0], "block-00.json", block),
                (keys[1], "reading.json", reading),
                (keys[2], "indeterminate-00.json", pending),
                (keys[3], "disposition.json", disposition)):
            write_text(drv.paths.readings / key / filename,
                       json.dumps(record.as_dict(), ensure_ascii=False) + "\n")
        outputs = {
            "already_read": [], "reopen_reason": "", "planned": 4, "dispatched": 3,
            "block_streak": 1,
            "readings": {"planned": 4, "dispatched": 3, "registered": [keys[1]],
                         "blocks": [[keys[0], "blocked:provider"]],
                         "dispositions": [[keys[3], reader.DISPOSITION_OUTSIDE_VOCABULARY]],
                         "unread": sorted(original.unread)},
            "indeterminate": {"roles_layout": [pending.coordinate], "dispatch_tree": []},
        }
        outcome = SimpleNamespace(kind="READ", step_key="synthetic-read",
                                  outputs={key: custody.digest(value)
                                           for key, value in outputs.items()})
        with mock.patch.object(auto_loop, "_reading_rows", return_value=(rows, [])), \
                mock.patch.object(graph, "cell_standings", return_value=[
                    graph.CellStanding(cell, "unresolved", "default", "IN", (), ())
                    for cell in cells]):
            auto_loop._reload_read(drv, 1, [], outcome)
            self.assertEqual(original, drv.readings_by_cycle[1])
            self.assertEqual(1, drv.block_streaks[1])
            self.assertEqual(((cells[0], "provider"),), auto_loop._cycle_state(drv, 1).blocks)
            self.assertEqual((pending.coordinate,), auto_loop._cycle_state(drv, 1).indeterminate)
            # The next cycle selects no already-spent row, but still lists unread cells.
            outputs.update(already_read=sorted(keys), planned=0, dispatched=0,
                           block_streak=0,
                           readings={"planned": 0, "dispatched": 0, "registered": [],
                                     "blocks": [], "dispositions": [], "unread": sorted(cells)},
                           indeterminate={"roles_layout": [], "dispatch_tree": []})
            outcome.outputs = {key: custody.digest(value) for key, value in outputs.items()}
            auto_loop._reload_read(drv, 2, [], outcome)
            self.assertEqual(reader.Readings(unread=frozenset(cells)), drv.readings_by_cycle[2])
            outcome.outputs["block_streak"] = custody.digest(99)
            with self.assertRaises(steps.StepNondeterministic):
                auto_loop._reload_read(drv, 3, [], outcome)
            self.assertNotIn(3, drv.readings_by_cycle)


if __name__ == "__main__":
    unittest.main()
