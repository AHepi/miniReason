"""W3-AUDITS - judge audits over readings already on record.

Every acceptance clause of the wave plan's W3-AUDITS entry has at least one
test here:

* "Calibration rows are true by construction and a clean control that sustains
  is scored as an error" - :class:`TrueByConstruction`.
* "a seeded flipping judge produces a paraphrase hit whose warrant collapses
  that seat's readings on recompute" - :class:`ASeededFlippingJudge`.
* "a ruling surviving deletion of its own decisive_point produces a premise
  hit" - :class:`PremiseDeletion`.
* "an error rate above JUDGE_ERR_MAX returns a Spawn signal" -
  :class:`TheSpawnSignal`.
* "every audit call reaches the log exactly once" - :class:`EveryCallLoggedOnce`.
* "audit findings carry their own validity nodes and are themselves
  attackable" - :class:`FindingsAreAttackable`.

The judge caller fixture is a scripted callable over the module's own
``judge_caller(seat, pack, coordinate) -> JudgeRuling | None`` boundary. The
one class that exercises a *call record* behind that boundary
(:class:`TheJudgeCallerBoundary`) drives a ``transport.OfflineProvider``
directly - the offline fixture W2-ROLES' own tests use - because in this
sandbox there is no ``tools/multicycle_commitment_study_multi_v2.py`` for
``seats.key_gate_for`` to import (the task's file list stops at ``src/``), so
``roles.call_judge`` would stop at ``RUNNER_NOT_IMPORTABLE`` here even though
the checkout it will run on supplies the runner. The audit module's provider
boundary is exercised with a real ``OfflineProvider`` and a real
``records_dir`` instead, so every re-ruling writes its call record; this is
recorded per the brief and held by :class:`TheJudgeCallerBoundary`.

Deviations from the design entry, and why:

* **``planted_flaw_calibration`` returns a ``CalibrationOutcome`` whose
  ``.share`` is the declared ``float|None``** rather than returning the bare
  float: a bare float carries no denominator, no error set and no Spawn
  signal, and a rate with no declared anchor is a meter (design 5, FW5:851).
  ``CalibrationOutcome.__float__`` and its equality against a float keep the
  bare reading a caller written to the plan's signature expects;
  :class:`TheCalibrationOutcome` holds both readings.
* **The calibration and disagreement arms ask the whole panel.**
  Design 2.5's calibration is over the panel, and the disagreement series is
  the *ensemble*'s; a reading record that names only one seat would leave one
  seat's two answers masquerading as a variance between two seats. The module
  declares the pre-registered pair (``audits._PANEL``) for the case where the
  graph's own records name none.
* **The warrant's target set is read off the returned ``AuditHit``,** which
  carries what the module handed to ``graph.register_audit_warrant`` - the
  sibling resolves a blank ``targets`` to the seat's window at registration
  time, so the module and the test agree by construction rather than by two
  walks of the same graph.
"""

from __future__ import annotations

import ast
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from minireason import provider_openai_compat as transport
from minireason.loop import contracts, graph, standard, audits as mod
from minireason.loop import types as loop_types
from minireason.loop.contracts import JudgeRuling
from minireason.loop.audits import (
    AUDITS_SCHEMA,
    NEW_CODES,
    SPAWN_AUDIT_THE_CRITIC,
    AuditReport,
    CalibrationOutcome,
    SpawnSignal,
    build_calibration_set,
    disagreement_series,
    paraphrase_invariance,
    planted_flaw_calibration,
    premise_deletion,
    run_audits,
)

SOURCE = Path(mod.__file__).resolve()

CONFIG = {
    "schema": "minireason.loop.config.v1",
    "run_id": "AUD-01",
    "study": "h005",
    "occurrences": ["experiments/h005/occurrence-01"],
    "runner": "tools/multicycle_commitment_study_multi_v2.py",
    "cycle_budget": 3,
    "max_calls": 240,
    "reading_set": ["p1/mini_fcl/cycle-1/n1#r3"],
    "obligations_path": "experiments/loops/AUD-01/obligations.json",
    "graph_root": "experiments/loops/AUD-01/graph",
    "reopen_reasons": ["new-material", "repaired-guard", "appellate-ruling"],
    "audit": {
        "period": 2,
        "judge_err_max": 0.2,
        "judge_err_max_account": ("the margin and the account that justifies it "
                                  "are frozen in the config and rendered together"),
        "streak_max": 5,
        "streak_max_account": "longer than any run of blocks the dry run produced",
    },
}

#: The real seat spelling: ``roles.Coordinate.seat_label`` is ``judge#1`` /
#: ``judge#2`` and ``judge-1`` is only the directory slug. The draft's fixture
#: agreed with a panel constant the module had invented in the slug spelling, so
#: every calibration warrant attached to an empty window and the tests could not
#: see it. The fixture now registers readings under the label W2-ROLES writes.
PANEL = ("judge#1", "judge#2")


# ------------------------------------------------------------------ fixtures


def scripted(answers: dict[str, JudgeRuling | None], default: JudgeRuling | None = None):
    """A judge caller: the module's one provider boundary, scripted by hand."""
    calls: list[tuple[str, str]] = []

    def caller(seat: str, pack: bytes, coordinate: str):
        calls.append((seat, coordinate))
        return answers.get(seat, default)

    caller.calls = calls
    return caller


def sustaining(point: str = "keeps the passage", note: str = "") -> JudgeRuling:
    return JudgeRuling(sustained=True, decisive_point=point,
                       reading_note=note or "the cited passage does the work")


def declining(point: str = "keeps the passage", note: str = "") -> JudgeRuling:
    return JudgeRuling(sustained=False, decisive_point=point,
                       reading_note=note or "on the restatement the link fails")


class AuditsTestCase(unittest.TestCase):
    """One harness; a reading by each seat of the panel, on its own cell.

    Two seats are on record because the panel an audit asks is read off the
    graph (``audits.PANEL_ON_RECORD``) unless the driver passes the pinned one.
    ``self.reading`` is the first seat's, on ``self.CELL``; the second seat's
    reading exists so that the ensemble arm has a pair to ask and so that a
    calibration hit has a real window to collapse.
    """

    CELL = "r1/c1"
    SECOND_CELL = "r2/c1"
    CASE = "the record keeps the passage and takes it up"
    ANSWER = "the defence says the two terms name one target"
    POINT = "keeps the passage"

    def setUp(self) -> None:
        super().setUp()
        self.root = Path(tempfile.mkdtemp(prefix="loop-audits-"))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.harness = graph.open_graph(
            self.root / "graph", clock=graph.fixed_clock())
        self.standard_id = graph.register_standard(self.harness)
        self.material = graph.register_material(self.harness, b'{"row_key": "r1"}')
        self.open()
        self.reading = self.read(seat=PANEL[0])
        self.open(self.SECOND_CELL)
        self.second_seat_reading = self.read(cell=self.SECOND_CELL, seat=PANEL[1])

    def open(self, cell: str | None = None) -> None:
        graph.open_cells(self.harness, [cell or self.CELL], material_id=self.material)

    def read(self, cell: str | None = None, relation: str = "retains",
             seat: str = PANEL[0], point: str = POINT) -> graph.ReadingIds:
        transcript = graph.Transcript(case=self.CASE, answer=self.ANSWER,
                                      decisive_point=point)
        return graph.register_reading(
            self.harness,
            graph.ReadingResult(
                key=graph.CellKey(cell or self.CELL), relation=relation,
                seat=seat, transcript=transcript, material_id=self.material),
            self.standard_id)

    def window(self, seat: str = PANEL[0]) -> tuple[str, ...]:
        return graph.validity_nodes_for_seat(self.harness, seat)

    def reopened(self):
        return graph.open_graph(self.root / "graph")

    def transcript_ref(self, reading: graph.ReadingIds | None = None) -> str:
        artifact = self.harness.state.artifacts[
            (reading or self.reading).reading]
        body = json.loads(self.harness.blobs.get(artifact.content_ref))
        return body["transcript_ref"]


# ------------------------------------------------------------------ the set


class TrueByConstruction(AuditsTestCase):
    """Acceptance clause 1: true by construction, so a disagreement with a row
    is an error the seat made, never a dispute."""

    def test_the_set_is_seeded_by_the_standards_own_five_anchors(self):
        rows = build_calibration_set(standard.STANDARD_BODY)
        self.assertEqual([row.anchor for row in rows],
                         [anchor.id for anchor in standard.CALIBRATION_ANCHORS])

    def test_every_row_carries_the_anchors_own_construction_and_reason(self):
        rows = {row.anchor: row
                for row in build_calibration_set(standard.STANDARD_BODY)}
        for anchor in standard.CALIBRATION_ANCHORS:
            with self.subTest(anchor=anchor.id):
                row = rows[anchor.id]
                self.assertEqual(row.construction, anchor.construction)
                self.assertEqual(row.ground_truth_reason, anchor.ground_truth_reason)
                self.assertEqual(row.expected_sustained, anchor.must_sustain)
                self.assertEqual(row.expected_relation, anchor.expected_relation)

    def test_the_set_is_fixed_and_two_builds_are_identical(self):
        first = build_calibration_set(standard.STANDARD_BODY)
        second = build_calibration_set(standard.STANDARD_BODY)
        self.assertEqual([row.as_dict() for row in first],
                         [row.as_dict() for row in second])
        self.assertIsInstance(first, list)

    def test_every_rows_ground_truth_is_stated_and_no_seat_answer_enters_it(self):
        for row in build_calibration_set(standard.STANDARD_BODY):
            with self.subTest(anchor=row.anchor):
                self.assertTrue(row.ground_truth_reason.strip())
                self.assertTrue(row.construction.strip())
                self.assertTrue(row.case.strip())
                self.assertTrue(row.answer.strip())
        relations = {row.anchor: row.expected_relation
                     for row in build_calibration_set(standard.STANDARD_BODY)
                     if row.expected_sustained}
        self.assertEqual(relations, {"self-juxtaposition": "retains",
                                     "quotes-and-rejects": "rejects-with-reason"})

    def test_a_clean_control_that_sustains_is_scored_as_an_error(self):
        rows = build_calibration_set(standard.STANDARD_BODY)
        controls = [row for row in rows if not row.expected_sustained]
        self.assertTrue(controls)
        for control in controls:
            with self.subTest(control=control.anchor):
                caller = scripted({}, default=sustaining())
                outcome = planted_flaw_calibration(self.harness, caller, [control],
                                                   panel=PANEL)
                self.assertTrue(outcome.errors, control.anchor)
                self.assertTrue(all(error.endswith(control.anchor)
                                    for error in outcome.errors))
        # ... and a must-sustain anchor declined is the same kind of error.
        must = [row for row in rows if row.expected_sustained][0]
        caller = scripted({}, default=declining())
        outcome = planted_flaw_calibration(self.harness, caller, [must], panel=PANEL)
        self.assertTrue(outcome.errors)
        self.assertTrue(must.expected_sustained)

    def test_a_clean_control_correctly_declined_scores_no_error(self):
        control = [row for row in build_calibration_set(standard.STANDARD_BODY)
                   if not row.expected_sustained][0]
        outcome = planted_flaw_calibration(
            self.harness, scripted({}, default=declining()), [control], panel=PANEL)
        self.assertEqual(outcome.errors, ())
        self.assertEqual(outcome.share, 0.0)

    def test_an_anchor_with_no_constructed_exchange_is_refused(self):
        from minireason.loop.standard import CalibrationAnchor
        invented = CalibrationAnchor(
            id="invented", construction="c", expected_relation=None,
            must_sustain=False, ground_truth_reason="r")
        with self.assertRaises(mod.AuditError):
            build_calibration_set([invented])


class TheCalibrationOutcome(AuditsTestCase):
    """The declared ``-> float|None``, and what a bare float could not carry."""

    def test_the_share_is_the_errors_over_the_exercised_anchors(self):
        caller = scripted({}, default=sustaining())
        rows = build_calibration_set(standard.STANDARD_BODY)
        outcome = planted_flaw_calibration(self.harness, caller, rows)
        controls = [row.anchor for row in rows if not row.expected_sustained]
        seats = tuple(sorted({hit.split(":")[0] for hit in outcome.errors}))
        self.assertEqual(seats, PANEL)
        self.assertEqual(sorted(set(outcome.errors)),
                         sorted({f"{seat}:{anchor}" for seat in seats
                                 for anchor in controls}))
        expected_share = (len(seats) * len(controls)) / (len(seats) * len(rows))
        self.assertAlmostEqual(outcome.share, expected_share)

    def test_an_unexercised_set_carries_no_share_and_no_meter(self):
        caller = scripted({}, default=None)
        outcome = planted_flaw_calibration(
            self.harness, caller, build_calibration_set(standard.STANDARD_BODY),
            panel=PANEL)
        self.assertIsNone(outcome.share)
        self.assertEqual(outcome, None)
        with self.assertRaises(TypeError):
            float(outcome)

    def test_the_outcome_reads_as_the_declared_float_and_carries_the_errors(self):
        rows = build_calibration_set(standard.STANDARD_BODY)[-1:]
        outcome = planted_flaw_calibration(
            self.harness, scripted({}, default=sustaining()), rows, panel=PANEL)
        self.assertIsInstance(outcome, CalibrationOutcome)
        self.assertNotEqual(outcome, 0.0)
        self.assertEqual(float(outcome), outcome.share)
        self.assertTrue(outcome.errors)


# ------------------------------------------------------------------ paraphrase


class ASeededFlippingJudge(AuditsTestCase):
    """Acceptance clause 2: a seeded flipping judge produces a paraphrase hit
    whose warrant collapses that seat's readings on recompute."""

    def flipping(self):
        return scripted({}, default=declining())

    def test_a_sustained_seat_that_flips_on_a_paraphrase_registers_a_hit(self):
        hits = paraphrase_invariance(self.harness, self.flipping(),
                                     [self.reading.reading])
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].kind, "paraphrase-invariance")
        self.assertEqual(hits[0].seat, PANEL[0])
        self.assertIn("ruled True on the logged exchange", hits[0].detail)

    def test_the_hits_warrant_is_against_the_seats_whole_window(self):
        hits = paraphrase_invariance(self.harness, self.flipping(),
                                     [self.reading.reading])
        self.assertEqual(hits[0].targets, self.window(PANEL[0]))
        self.assertTrue(hits[0].targets)

    def test_the_hit_collapses_that_seats_readings_on_recompute(self):
        self.assertEqual(graph.cell_state(self.harness, self.CELL), graph.READ)
        paraphrase_invariance(self.harness, self.flipping(), [self.reading.reading])
        self.assertEqual(graph.cell_state(self.harness, self.CELL), graph.UNRESOLVED)
        self.assertEqual(graph.cell_state(self.reopened(), self.CELL),
                         graph.UNRESOLVED)

    def test_the_collapse_is_named_on_the_report_as_the_new_state(self):
        report = run_audits(self.harness, self.flipping(),
                            [self.reading.reading], CONFIG)
        self.assertIn((self.CELL, graph.UNRESOLVED), report.collapsed)

    def test_a_seat_that_stands_firm_registers_nothing(self):
        hits = paraphrase_invariance(self.harness,
                                     scripted({}, default=sustaining()),
                                     [self.reading.reading])
        self.assertEqual(hits, [])
        self.assertEqual(graph.cell_state(self.reopened(), self.CELL), graph.READ)

    def test_a_seat_that_did_not_answer_is_a_delivery_fact_and_never_a_hit(self):
        hits = paraphrase_invariance(self.harness, scripted({}, default=None),
                                     [self.reading.reading])
        self.assertEqual(hits, [])
        self.assertEqual(graph.cell_state(self.harness, self.CELL), graph.READ)


# ------------------------------------------------------------------ deletion


class PremiseDeletion(AuditsTestCase):
    """Acceptance clause 3: a ruling surviving the deletion of its own
    ``decisive_point`` produces a premise hit."""

    def test_a_ruling_surviving_its_own_grounds_is_a_hit(self):
        hits = premise_deletion(self.harness, scripted({}, default=sustaining()),
                                [self.reading.reading])
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].kind, "premise-deletion")
        self.assertIn("survived the deletion", hits[0].detail)
        self.assertIn(self.POINT, hits[0].detail)

    def test_the_pack_really_removes_the_cited_point_from_the_exchange(self):
        seen: list[bytes] = []

        def caller(seat, pack, coordinate):
            seen.append(pack)
            return sustaining()

        premise_deletion(self.harness, caller, [self.reading.reading])
        self.assertEqual(len(seen), 1)
        text = seen[0].decode("utf-8")
        transcript = json.loads(self.harness.blobs.get(self.transcript_ref()))
        exchange = f"{transcript['case']}\n{transcript['answer']}"
        deleted = exchange.replace(self.POINT, "", 1)
        self.assertNotEqual(deleted, exchange)
        self.assertIn(deleted, text)
        self.assertNotIn(exchange, text)

    def test_a_ruling_that_falls_with_its_premise_registers_nothing(self):
        hits = premise_deletion(self.harness, scripted({}, default=declining()),
                                [self.reading.reading])
        self.assertEqual(hits, [])
        self.assertEqual(graph.cell_state(self.reopened(), self.CELL), graph.READ)

    def test_the_premise_hit_collapses_the_window_on_recompute(self):
        premise_deletion(self.harness, scripted({}, default=sustaining()),
                         [self.reading.reading])
        self.assertEqual(graph.cell_state(self.reopened(), self.CELL),
                         graph.UNRESOLVED)


# ------------------------------------------------------------------ calibration


class TheSpawnSignal(AuditsTestCase):
    """Acceptance clause 4: an error rate above JUDGE_ERR_MAX returns a Spawn
    signal - never a status change and never a raised code."""

    def test_a_share_above_the_declared_bound_spawns(self):
        report = run_audits(self.harness, scripted({}, default=sustaining()),
                            [self.reading.reading], CONFIG)
        signal = report.calibration.spawn
        self.assertIsNotNone(signal)
        self.assertEqual(signal.trigger, SPAWN_AUDIT_THE_CRITIC)
        self.assertGreater(signal.observed, signal.bound)
        self.assertEqual(signal.bound, CONFIG["audit"]["judge_err_max"])
        self.assertEqual(signal.account, CONFIG["audit"]["judge_err_max_account"])

    def test_the_spawn_names_every_exercised_anchor_and_carries_its_account(self):
        report = run_audits(self.harness, scripted({}, default=sustaining()),
                            [self.reading.reading], CONFIG)
        signal = report.calibration.spawn
        self.assertIsNotNone(signal)
        self.assertEqual(
            signal.anchors,
            tuple(sorted(anchor.id for anchor in standard.CALIBRATION_ANCHORS)))
        self.assertTrue(signal.prompt().startswith(SPAWN_AUDIT_THE_CRITIC))
        self.assertIn(signal.account, signal.prompt())

    def test_a_share_at_or_below_the_bound_spawns_nothing(self):
        rows = {row.anchor: row
                for row in build_calibration_set(standard.STANDARD_BODY)}

        def caller(seat, pack, coordinate):
            if coordinate.startswith("audit-cal/"):
                row = rows[coordinate.split("/")[1]]
                return JudgeRuling(sustained=row.expected_sustained,
                                   decisive_point="x", reading_note="correct")
            return sustaining()

        report = run_audits(self.harness, caller, [self.reading.reading], CONFIG)
        self.assertIsNone(report.calibration.spawn)
        self.assertEqual(report.calibration.share, 0.0)
        self.assertEqual(report.calibration.errors, ())

    def test_a_spawn_is_a_returned_signal_and_never_a_raised_code(self):
        report = run_audits(self.harness, scripted({}, default=sustaining()),
                            [self.reading.reading], CONFIG)
        self.assertIsInstance(report.calibration.spawn, SpawnSignal)
        self.assertNotIn(SPAWN_AUDIT_THE_CRITIC, loop_types.FAILURE_CODES)
        self.assertNotIn(SPAWN_AUDIT_THE_CRITIC, loop_types.STOP_REASONS)


# ---------------------------------------------------------- the composed seam


class TheCalibrationHitsAttachToRealSeats(AuditsTestCase):
    """The composed seam the wave-3 review was asked to check: an audit warrant
    must attach to the validity nodes of the seat's readings *through* ``graph``,
    and it can only do that if the seat label is the one the graph stored.

    The draft asked an invented panel spelled ``judge-1`` while ``graph`` held
    the seat as ``judge#1`` (``roles.Coordinate.seat_label``), so on the
    integration probe six calibration errors each registered a warrant against
    an empty window: a hit that reads as a hit and collapses nothing. The draft's
    own fixture agreed with the invented spelling, which is why no test saw it.
    """

    def test_the_panel_is_the_seats_on_record_when_none_is_passed(self):
        self.assertEqual(graph.seats_on_record(self.harness), PANEL)
        seen: list[str] = []

        def caller(seat, pack, coordinate):
            seen.append(seat)
            return sustaining()

        planted_flaw_calibration(
            self.harness, caller, build_calibration_set(standard.STANDARD_BODY))
        self.assertEqual(sorted(set(seen)), sorted(PANEL))

    def test_an_invented_seat_label_would_collapse_nothing(self):
        self.assertEqual(graph.validity_nodes_for_seat(self.harness, "judge-1"), ())
        self.assertTrue(graph.validity_nodes_for_seat(self.harness, PANEL[0]))

    def test_a_calibration_error_collapses_that_seats_readings(self):
        self.assertEqual(graph.cell_state(self.harness, self.CELL), graph.READ)
        control = [row for row in build_calibration_set(standard.STANDARD_BODY)
                   if not row.expected_sustained][0]
        outcome = planted_flaw_calibration(
            self.harness,
            scripted({PANEL[0]: sustaining()}, default=declining()),
            [control])
        self.assertEqual([hit.seat for hit in outcome.hits], [PANEL[0]])
        self.assertEqual(outcome.hits[0].targets, self.window(PANEL[0]))
        self.assertTrue(outcome.hits[0].targets)
        self.assertEqual(graph.cell_state(self.reopened(), self.CELL),
                         graph.UNRESOLVED)
        self.assertEqual(graph.cell_state(self.reopened(), self.SECOND_CELL),
                         graph.READ)

    def test_every_calibration_hit_is_named_on_the_report(self):
        report = run_audits(self.harness, scripted({}, default=sustaining()),
                            [self.reading.reading], CONFIG)
        self.assertTrue(report.calibration.hits)
        self.assertIn("planted-flaw-calibration",
                      {hit.kind for hit in report.findings})
        self.assertEqual(
            [hit.finding_id for hit in report.calibration.hits],
            [hit.finding_id for hit in report.findings
             if hit.kind == "planted-flaw-calibration"],
            "a collapse the report cannot name is a collapse nobody can attack")


class TheDeclaredMargin(AuditsTestCase):
    """Ruling 7: ``judge_err_max`` is a bound on the instrument, and its firing
    must carry an account. Both are the frozen config's.

    The draft read an invented ``0.2`` with an invented account inside
    ``planted_flaw_calibration`` and relabelled the signal with the config's
    values afterwards, so a config bound *below* 0.2 could be crossed with no
    signal at all (probed: share 0.1 against a declared 0.05, ``spawn=None``),
    and a signal minted against 0.2 could be published naming a bound it had not
    crossed. The invented account was REVIEW-PREREG PR-09's own defect, retyped.
    """

    def a_caller_wrong_on_one_anchor(self):
        rows = {row.anchor: row
                for row in build_calibration_set(standard.STANDARD_BODY)}
        wrong = sorted(rows)[0]

        def caller(seat, pack, coordinate):
            if coordinate.startswith("audit-cal/"):
                anchor = coordinate.split("/")[1]
                sustained = rows[anchor].expected_sustained
                if anchor == wrong and seat == PANEL[0]:
                    sustained = not sustained
                return JudgeRuling(sustained=sustained, decisive_point="x",
                                   reading_note="n")
            return declining()

        return caller

    def test_a_bound_below_the_drafts_fallback_still_spawns(self):
        config = json.loads(json.dumps(CONFIG))
        config["audit"]["judge_err_max"] = 0.05
        report = run_audits(self.harness, self.a_caller_wrong_on_one_anchor(),
                            [self.reading.reading], config)
        self.assertIsNotNone(report.calibration.spawn)
        self.assertEqual(report.calibration.spawn.bound, 0.05)
        self.assertGreater(report.calibration.share, 0.05)
        self.assertLess(report.calibration.share, 0.2)

    def test_the_signal_carries_the_configs_own_bound_and_account(self):
        report = run_audits(self.harness, scripted({}, default=sustaining()),
                            [self.reading.reading], CONFIG)
        signal = report.calibration.spawn
        self.assertEqual(signal.bound, CONFIG["audit"]["judge_err_max"])
        self.assertEqual(signal.account, CONFIG["audit"]["judge_err_max_account"])
        self.assertIn(signal.account, signal.prompt())
        self.assertNotIn("PROVISIONAL", signal.account)

    def test_no_margin_and_no_account_is_spelled_in_this_module(self):
        source = SOURCE.read_text(encoding="utf-8")
        self.assertNotIn("0.2", source)
        self.assertNotIn("judge_err_max =", source)

    def test_a_config_with_no_audit_block_is_refused(self):
        with self.assertRaises(mod.AuditError) as caught:
            run_audits(self.harness, scripted({}, default=sustaining()),
                       [self.reading.reading], {})
        self.assertEqual(caught.exception.code, "CONFIG_MISSING_KEY")

    def test_a_margin_with_an_empty_account_is_refused(self):
        config = json.loads(json.dumps(CONFIG))
        config["audit"]["judge_err_max_account"] = "   "
        with self.assertRaises(mod.AuditError) as caught:
            run_audits(self.harness, scripted({}, default=sustaining()),
                       [self.reading.reading], config)
        self.assertEqual(caught.exception.code, "CONFIG_INVALID_VALUE")

    def test_the_calibration_arm_alone_mints_no_signal_without_a_bound(self):
        outcome = planted_flaw_calibration(
            self.harness, scripted({}, default=sustaining()),
            build_calibration_set(standard.STANDARD_BODY), panel=PANEL)
        self.assertIsNone(outcome.spawn)
        self.assertGreater(outcome.share, 0.0)


class TheSetIsPinned(AuditsTestCase):
    """"Fixed at pin time" is a checkable statement here, not a promise."""

    def test_the_constructed_exchanges_carry_a_digest(self):
        import hashlib
        expected = hashlib.sha256(
            "\n".join(f"{anchor}\u0000{case}\u0000{answer}"
                      for anchor, (case, answer)
                      in sorted(mod._ANCHOR_EXCHANGES.items())
                      ).encode("utf-8")).hexdigest()
        self.assertEqual(mod.CALIBRATION_EXCHANGES_SHA256, expected)

    def test_every_anchor_of_the_standard_has_an_exchange_and_no_more(self):
        self.assertEqual(
            sorted(mod._ANCHOR_EXCHANGES),
            sorted(anchor.id for anchor in standard.CALIBRATION_ANCHORS))


# ------------------------------------------------------------------ the series


class EnsembleDisagreementIsAMeasureNeverAVerdict(AuditsTestCase):
    """Design 2.5, and graph's own rule: the series is a Measure, and
    ``graph.AUDIT_KINDS`` deliberately excludes it, so the arm cannot mint a
    warrant by mistake."""

    def test_a_split_pair_is_recorded_as_unresolved_and_mints_no_warrant(self):
        caller = scripted({PANEL[0]: sustaining(), PANEL[1]: declining()})
        series = disagreement_series(self.harness, caller, [self.reading.reading])
        self.assertEqual(len(series), 1)
        row = series[0]
        self.assertTrue(row.disagrees)
        self.assertEqual(row.as_dict()["outcome"], standard.UNRESOLVED_TOKEN)
        self.assertEqual(graph.cell_state(self.harness, self.CELL), graph.READ)

    def test_the_disagreement_kind_cannot_register_a_warrant(self):
        self.assertNotIn("ensemble-disagreement", graph.AUDIT_KINDS)
        with self.assertRaises(graph.GraphError):
            graph.register_audit_warrant(self.harness, graph.AuditFinding(
                seat=PANEL[0], kind="ensemble-disagreement", detail="split"))

    def test_a_seat_that_did_not_answer_is_a_null_answer_never_a_vote(self):
        caller = scripted({PANEL[0]: sustaining()}, default=None)
        series = disagreement_series(self.harness, caller, [self.reading.reading])
        self.assertEqual(len(series), 1)
        row = series[0]
        self.assertFalse(row.disagrees)
        self.assertIsNone(row.right_sustained)

    def test_a_panel_of_one_seat_yields_no_row_and_spends_no_call(self):
        """One seat's two answers are never a variance between two seats, so
        the arm asks nothing rather than inventing the second seat. The draft
        fell back to its own ``_PANEL`` constant here, which is how a
        fabricated pair could have been printed as an agreeing ensemble."""
        caller = scripted({}, default=sustaining())
        series = disagreement_series(self.harness, caller,
                                     [self.reading.reading], panel=(PANEL[0],))
        self.assertEqual(series, ())
        self.assertEqual(caller.calls, [])

    def test_the_readings_own_roles_name_the_pair_where_it_has_them(self):
        transcript = graph.Transcript(case=self.CASE, answer=self.ANSWER,
                                      decisive_point=self.POINT)
        self.open("r3/c1")
        named = graph.register_reading(
            self.harness,
            graph.ReadingResult(
                key=graph.CellKey("r3/c1"), relation="retains", seat=PANEL[0],
                transcript=transcript, material_id=self.material,
                roles={"judge#1": "seat-alpha", "judge#2": "seat-beta"}),
            self.standard_id)
        caller = scripted({}, default=sustaining())
        series = disagreement_series(self.harness, caller, [named.reading],
                                     panel=PANEL)
        self.assertEqual(len(series), 1)
        self.assertEqual((series[0].left_seat, series[0].right_seat),
                         ("seat-alpha", "seat-beta"))


# ------------------------------------------------------------------ the report


class EveryCallLoggedOnce(AuditsTestCase):
    """Acceptance clause 5: every audit call reaches the log exactly once."""

    def test_every_coordinate_spent_appears_once_in_the_reports_log(self):
        self.open("r1/c2")
        second = self.read(cell="r1/c2", point="takes it up")
        caller = scripted({}, default=sustaining())
        report = run_audits(
            self.harness, caller, [self.reading.reading, second.reading], CONFIG)
        self.assertEqual(sorted(report.logs), sorted(set(report.logs)),
                         "one coordinate logged twice")
        self.assertTrue(report.logs)
        for coordinate in report.logs:
            with self.subTest(coordinate=coordinate):
                self.assertTrue(coordinate.startswith("audit-"))

    def test_the_log_counts_the_calls_the_caller_spent(self):
        caller = scripted({}, default=sustaining())
        report = run_audits(self.harness, caller, [self.reading.reading], CONFIG)
        self.assertEqual(list(report.logs),
                         [coordinate for _seat, coordinate in caller.calls])

    def test_a_report_is_well_formed_and_self_described(self):
        report = run_audits(self.harness, scripted({}, default=sustaining()),
                            [self.reading.reading], CONFIG)
        self.assertIsInstance(report, AuditReport)
        record = report.as_dict()
        self.assertEqual(record["schema"], AUDITS_SCHEMA)
        self.assertEqual(record["logs"], list(report.logs))


# ------------------------------------------------------------------ attackable


class FindingsAreAttackable(AuditsTestCase):
    """Acceptance clause 6: audit findings carry their own validity nodes and
    are themselves attackable."""

    def _bodies(self, harness, schema: str) -> dict[str, dict]:
        found = {}
        for artifact_id, artifact in harness.state.artifacts.items():
            body = graph._decode(harness, artifact)
            if isinstance(body, dict) and body.get("schema") == schema:
                found[artifact_id] = body
        return found

    def _nu_audit_of(self, harness, hit_target: str) -> str:
        for warrant in harness.warrants.values():
            if (warrant.target == hit_target and warrant.commitment
                    and str(warrant.commitment).startswith(graph.KAPPA_AUDIT_PREFIX)):
                return warrant.validity_node
        raise AssertionError("no audit warrant reached the target")

    def test_every_finding_artifact_carries_its_own_validity_node(self):
        paraphrase_invariance(self.harness, scripted({}, default=declining()),
                              [self.reading.reading])
        findings = self._bodies(self.harness, graph.AUDIT_SCHEMA)
        self.assertTrue(findings)
        audit_nodes = {artifact_id for artifact_id, body
                       in self._bodies(self.harness, graph.VALIDITY_SCHEMA).items()
                       if body.get("aspect") == "audit"}
        self.assertTrue(audit_nodes)
        for finding_id in findings:
            warrants = [self.harness.warrants[wid]
                        for wid in self.harness.carried_warrant_ids(finding_id)]
            self.assertTrue(warrants)
            for warrant in warrants:
                self.assertIn(warrant.validity_node, audit_nodes)

    def test_attacking_a_findings_validity_node_reinstates_the_reading(self):
        hits = paraphrase_invariance(self.harness, scripted({}, default=declining()),
                                     [self.reading.reading])
        self.assertEqual(graph.cell_state(self.harness, self.CELL), graph.UNRESOLVED)
        nu_audit = self._nu_audit_of(self.harness, hits[0].targets[0])
        graph.apply_appeal(self.harness, graph.AppellateRuling(
            ruling_id="APP-001", target=nu_audit,
            ground="the paraphrase audit misread the restatement"))
        self.assertEqual(graph.cell_state(self.reopened(), self.CELL), graph.READ)


# ------------------------------------------------------------------ the boundary


class TheJudgeCallerBoundary(unittest.TestCase):
    """The declared caller protocol, exercised against a real OfflineProvider
    call record per re-ruling.

    ``roles.call_judge`` is not used here: in this sandbox
    ``seats.key_gate_for`` - runner v2's ``key_gate``, imported, never copied -
    cannot import, because the sandbox carries no ``tools/`` runner. The audit
    module's *boundary* is exercised with the transport's offline fixture
    directly, so every re-ruling still writes its call record.
    """

    def test_a_role_result_is_accepted_at_the_boundary(self):
        self.assertTrue(mod._ruling(_FakeResult(ok=True,
                                                output=sustaining())).sustained)
        self.assertIsNone(mod._ruling(_FakeResult(ok=False, output=None)))
        self.assertIsNone(mod._ruling(None))

    def test_an_answer_that_is_not_a_ruling_is_refused_at_the_boundary(self):
        with self.assertRaises(mod.AuditError):
            mod._ruling("not a ruling")

    def test_a_real_offline_provider_record_backs_each_re_ruling(self):
        from minireason.loop import synthetic

        root = Path(tempfile.mkdtemp(prefix="loop-audits-boundary-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        harness = graph.open_graph(root / "graph", clock=graph.fixed_clock())
        standard_id = graph.register_standard(harness)
        material = graph.register_material(harness, b'{"row_key": "r1"}')
        graph.open_cells(harness, ["r1/c1"], material_id=material)
        reading = graph.register_reading(
            harness,
            graph.ReadingResult(
                key=graph.CellKey("r1/c1"), relation="retains", seat=PANEL[0],
                transcript=graph.Transcript(
                    case="the record keeps the passage and takes it up",
                    answer="the defence says the two terms name one target",
                    decisive_point="keeps the passage"),
                material_id=material),
            standard_id)

        endpoint = synthetic.endpoints_registry()["synthetic/alpha"]
        reply = {"sustained": False, "decisive_point": "keeps the passage",
                 "reading_note": "on the paraphrase the link fails"}

        def judge_caller(seat_label: str, pack: bytes, coordinate: str):
            records = root / "records" / seat_label / coordinate.replace("/", "_")
            records.mkdir(parents=True, exist_ok=True)
            provider = transport.OfflineProvider(endpoint, records,
                                                 [json.dumps(reply)])
            result = provider.complete(
                [{"role": "user", "content": pack.decode("utf-8")}],
                response_format={"type": "json_schema"},
                max_tokens=2048)
            checked = contracts.check("judge", result.content)
            return mod._ruling(_FakeResult(ok=checked.ok, output=checked.value))

        hits = paraphrase_invariance(harness, judge_caller, [reading.reading])
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].kind, "paraphrase-invariance")
        self.assertEqual(graph.cell_state(harness, "r1/c1"), graph.UNRESOLVED)
        written = sorted((root / "records").rglob("call-*.request.json"))
        self.assertEqual(len(written), 1)


class _FakeResult:
    def __init__(self, *, ok: bool, output) -> None:
        self.ok = ok
        self.output = output


# ------------------------------------------------------------------ the module


class TheModuleDeclaresItself(unittest.TestCase):
    """The wave plan's interface, the package's rules, and the empty NEW_CODES."""

    def test_the_module_introduces_no_failure_code_of_its_own(self):
        self.assertEqual(dict(NEW_CODES), {})

    def test_every_refusal_is_a_code_an_earlier_wave_owns(self):
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        constants = {
            node.targets[0].id: node.value.value
            for node in tree.body
            if isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        }
        raised = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "_fail":
                first = node.args[0]
                token = (first.value if isinstance(first, ast.Constant)
                         else constants.get(getattr(first, "id", "")))
                if token:
                    raised.append(token)
        self.assertTrue(raised, "the scan found no _fail call at all")
        for token in raised:
            with self.subTest(token=token):
                self.assertIn(token, loop_types.FAILURE_CODES)

    def test_the_module_imports_only_its_declared_dependencies(self):
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        siblings = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                siblings.update(
                    alias.name.rsplit(".", 1)[-1]
                    for alias in node.names
                    if alias.name.startswith("minireason.loop."))
            elif isinstance(node, ast.ImportFrom):
                base = node.module or ""
                if base.startswith("minireason.loop."):
                    siblings.add(base.rsplit(".", 1)[-1])
                elif node.level == 1:
                    if base:
                        siblings.add(base.split(".")[0])
                    else:
                        # ``from . import graph``: the sibling is the name.
                        siblings.update(
                            alias.name.split(".")[0] for alias in node.names)
        self.assertEqual(siblings, {"contracts", "graph", "standard", "types"})

    def test_the_module_opens_no_socket_and_calls_no_provider(self):
        source = SOURCE.read_text(encoding="utf-8")
        for banned in ("provider_openai_compat", "OpenAICompatProvider",
                       "OfflineProvider", "urlopen"):
            with self.subTest(token=banned):
                self.assertNotIn(banned, source)

    def test_no_audit_arm_is_a_meter(self):
        """No score, rank, average, majority vote or percentage anywhere: the
        only arithmetic the module computes is the pre-registered error share,
        declared in one named function with its stated denominator."""
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        divisions = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
        ]
        self.assertEqual(len(divisions), 1)
        owners = {
            function.name for function in ast.walk(tree)
            if isinstance(function, ast.FunctionDef)
            and any(cand is divisions[0] for cand in ast.walk(function))
        }
        self.assertEqual(owners, {"_calibration_share"})

    def test_the_public_interface_is_exactly_what_the_wave_plan_declares(self):
        for name in ("build_calibration_set", "paraphrase_invariance",
                     "premise_deletion", "planted_flaw_calibration",
                     "run_audits"):
            with self.subTest(name=name):
                self.assertIn(name, mod.__all__)
                self.assertTrue(callable(getattr(mod, name)))

    def test_the_module_compiles_clean_of_the_known_use_relation_defect(self):
        """WAVE2 INTERFACE section 9: ``use_relation_h005.py`` carries an
        unescaped backslash-s at line 304, a published instrument no agent may
        edit. This module never imports it directly; what is asserted here is
        that this module *adds nothing* to the pile - the house rule's own
        half of the defect."""
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            compile(SOURCE.read_text(encoding="utf-8"), str(SOURCE), "exec")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
