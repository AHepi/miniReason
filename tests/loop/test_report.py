"""W3-REPORT - the run's rendered record, tested against its acceptance list.

Every acceptance clause of the W3-REPORT wave-plan entry has at least one test
named after it:

* "Rendering refuses without CEILING.md at its pinned sha" -
  :class:`RenderingRefusesWithoutThePinnedCeiling`.
* "every required ceiling sentence appears verbatim in every table and in the
  closing record" - :class:`EveryRequiredCeilingSentenceAppearsVerbatim`.
* "blocks print with counts by reason code" -
  :class:`BlocksPrintWithCountsByReasonCode`.
* "an all-blocked run renders as declined-to-read and never as no relations
  found" - :class:`AnAllBlockedRunRendersAsDeclinedToRead`.
* "unread, unresolved and machine-unresolved print as three distinct states" -
  :class:`TheThreeCellStatesPrintAsThreeThings`.
* "no rendered artifact contains a score, a rank, a combined register or the
  token 'exhaustion'" - :class:`NoRenderedArtifactCarriesAProhibitedToken`.
* "losses_outside_P is present when empty" -
  :class:`LossesOutsidePIsPresentWhenEmpty`.
* "appellate_rulings 0 renders the not-validated sentence" -
  :class:`AppellateRulingsZeroRendersNotValidated`.

House fixtures are what the wave-2 tests use: one temporary graph populated
only through ``minireason.loop.graph`` on a deterministic clock, a tiny frozen
plan whose pins map names the ceiling's own sha, and decisions built as
``decide.Decision`` rather than retyped.  No provider is ever imported; nothing
is written outside a temporary directory; nothing reaches a socket.
"""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from deepreason_core.canonical import sha256_hex

from minireason.loop import graph
from minireason.loop import report as R
from minireason.loop import standard
from minireason.loop import types as loop_types
from minireason.loop.decide import (
    CLAUSE_PROTECTED_LOSS,
    CLAUSE_RESOURCE_BOUNDARY,
    CONTINUE_OPEN,
    CLAUSE_NONE,
    STOP_PROTECTED_LOSS,
    Decision,
    Instrument,
    STOP_RESOURCE_BOUNDARY,
    WOULD_REOPEN,
    decide,
    situation,
)
from minireason.loop.custody import CustodyMismatch
from minireason.loop.standard import StandardInvalid
from minireason.loop.report import (
    APPELLATE_NOT_VALIDATED_SENTENCE,
    BLOCK_REGISTER_HEADINGS,
    CEILING_REQUIRED_SENTENCES,
    DECLINED_TO_READ_SENTENCE,
    INDETERMINATE_SENTENCE,
    LOSSES_OUTSIDE_P_SENTENCE,
    ClosingRun,
    CycleState,
    RegisterRow,
    ReportPlan,
    ReportRefused,
    ceiling_key_of,
    render_closing,
    render_comparison,
    render_cycle,
    render_reading_table,
)
from minireason.loop.types import CEILING_BLOCK_REASONS, LoopConfig, LoopError, block_code

MATERIAL = b'{"row_key": "r1", "cells": {}}'

CONFIG = {
    "schema": "minireason.loop.config.v1",
    "run_id": "W3REPORT",
    "study": "h005",
    "occurrences": ["experiments/h005/occurrence-01"],
    "runner": "tools/multicycle_commitment_study_multi_v2.py",
    "cycle_budget": 2,
    "max_calls": 240,
    "reading_set": ["r1/c1", "r1/c2", "r1/c3"],
    "obligations_path": "experiments/loops/W3REPORT/obligations.json",
    "graph_root": "experiments/loops/W3REPORT/graph",
    "reopen_reasons": ["new-material"],
    "audit": {
        "period": 2,
        "judge_err_max": 0.2,
        "judge_err_max_account": ("the margin and the account that justifies it "
                                  "are frozen in the config and rendered together"),
        "streak_max": 5,
        "streak_max_account": "longer than any run of blocks the dry run produced",
    },
}

#: One owner for the key: ``standard`` holds the ceiling, so it holds the
#: repo-relative spelling a plan pins it under. The draft rebuilt the key in
#: ``report.ceiling_key_of`` out of ``types.PINNED_SOURCE_PATHS[0].split("/")[0]``
#: and a retyped path, and this file retyped it a third time.
CEILING_PIN_KEY = standard.CEILING_PIN_KEY


def plan(**overrides) -> ReportPlan:
    """A frozen plan fragment: the ceiling pinned at its published sha."""
    pins = {CEILING_PIN_KEY: standard.CEILING_SHA256,
            **{f"src/minireason/loop/{name}": "b" * 64
               for name in ("types.py", "standard.py")}}
    pins.update(overrides.pop("pins", {}))
    return ReportPlan(loop_plan_id="c" * 64, pins=pins,
                      reading_set=overrides.pop("reading_set", None),
                      **overrides)


def stop_decision(*, cycle: int = 2, **kwargs) -> Decision:
    """The one decision a closing fixture needs, with its own sentences."""
    return Decision(
        cycle=cycle, stop=True, reason=STOP_RESOURCE_BOUNDARY,
        clause=CLAUSE_RESOURCE_BOUNDARY,
        detail="the cycle index 2 reached the declared budget 2",
        would_reopen=WOULD_REOPEN[STOP_RESOURCE_BOUNDARY],
        **kwargs)


class TheModuleRidesTheFrozenTablesOnly(unittest.TestCase):
    """W3-RECORD: the wave-2 frontier is empty, so this module declares no
    new codes and mints none of its own.  These tests are that rule's teeth:
    report.py's source is scanned the same way test_types.py scans the package,
    and its import edge to custody is pinned on the same table that edge
    violates (test_types asserts the frontier empty and test_contracts asserts
    the exact edge set; the integrator who lands the wave-3 trio updates both
    in the commit that folds them)."""

    SOURCE = Path(R.__file__).resolve()

    def test_new_codes_is_declared_and_is_empty(self):
        self.assertEqual(dict(R.NEW_CODES), {})

    def test_every_code_the_module_can_raise_is_already_declared(self):
        import ast
        tree = ast.parse(self.SOURCE.read_text(encoding="utf-8"))
        raised: set[str] = set()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", "")
            if name not in ("ReportRefused", "StandardInvalid", "CustodyMismatch"):
                continue
            if not node.args or not isinstance(node.args[0], ast.Constant):
                continue
            value = node.args[0].value
            if isinstance(value, str):
                raised.add(value)
        self.assertTrue(raised)
        for code in sorted(raised):
            with self.subTest(code=code):
                self.assertIn(code, loop_types.FAILURE_CODES)

    def test_every_exception_the_module_raises_is_a_loop_error(self):
        from minireason.loop.standard import StandardInvalid as SI
        from minireason.loop.custody import CustodyMismatch as CM
        for error in (SI("STANDARD_DATA_MALFORMED", "x"), R.ReportRefused("SOURCE_PIN_MISSING", "x")):
            with self.subTest(error=type(error).__name__):
                self.assertIsInstance(error, LoopError)

    def test_the_blocked_prefix_is_never_written_here(self):
        for line in self.SOURCE.read_text(encoding="utf-8").splitlines():
            if line.lstrip().startswith("#"):
                continue
            with self.subTest(line=line.strip()[:60]):
                self.assertNotIn('"blocked:', line)
                self.assertNotIn("'blocked:", line)


class ReportTestCase(unittest.TestCase):
    """One graph on a deterministic clock, three open cells."""

    def setUp(self) -> None:
        super().setUp()
        self.root = Path(tempfile.mkdtemp(prefix="loop-report-"))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.harness = graph.open_graph(self.root / "graph", clock=graph.fixed_clock())
        self.standard_id = graph.register_standard(self.harness)
        self.material = graph.register_material(self.harness, MATERIAL)
        self.cells = [graph.CellKey("r1/c1"),
                      graph.CellKey("r1/c2"),
                      graph.CellKey("r1/c3", "T", "original-vs-control")]
        self.opened = graph.open_cells(self.harness, self.cells,
                                       material_id=self.material)
        self.config = LoopConfig.from_mapping(CONFIG)

    def situation(self, cycle: int) -> "situation":
        from minireason.loop import obligations as ob
        from deepreason_core.canonical import canonical_json
        document = {
            "schema": ob.OBLIGATIONS_SCHEMA, "run_id": "W3REPORT",
            "obligations": [{
                "id": "p6", "set": "P", "statement": "no aggregation",
                "check": {"predicate": "obligations.no_aggregation",
                          "artifact": [], "detail": "read only"},
                "why_not_a_count": "a fixed universal predicate",
            }],
        }
        document["obligations_sha256"] = sha256_hex(canonical_json(document))
        path = self.root / "obligations.json"
        path.write_text(json.dumps(document, indent=2), encoding="utf-8")
        self.obligations = ob.load_obligations(path)
        return situation(self.harness, cycle, self.obligations)

    def mark(self, token: str = "differs") -> graph.ReadingIds:
        kind = "target_set_membership" if token == "differs" else None
        transcript = graph.Transcript(
            case="ORIGINAL names o1 where CONTROL names o2, so the target set differs",
            answer="the defence concedes they do not name one target set",
            decisive_point="the target set differs")
        return graph.register_mark(self.harness, graph.ReadingResult(
            key=self.cells[2], relation=token, seat="judge-1",
            transcript=transcript, difference_kind=kind,
            material_id=self.material), self.standard_id)


# ---------------------------------------------------------------------------
# Without the pinned ceiling, nothing renders
# ---------------------------------------------------------------------------


class RenderingRefusesWithoutThePinnedCeiling(ReportTestCase):

    def test_a_plan_that_pins_the_ceiling_at_another_sha_is_refused(self):
        """The custody vocabulary's own code: a pin that moved."""
        wrong = ReportPlan(pins={CEILING_PIN_KEY: "0" * 64})
        for renderer in (render_reading_table, render_comparison):
            with self.subTest(renderer=renderer.__name__):
                with self.assertRaises(ReportRefused) as caught:
                    renderer(self.harness, wrong)
                self.assertEqual(caught.exception.code, "SOURCE_PIN_MISMATCH")
                self.assertIsInstance(caught.exception, CustodyMismatch)

    def test_a_plan_that_does_not_pin_the_ceiling_at_all_is_refused(self):
        bare = ReportPlan(pins={"src/minireason/loop/types.py": "b" * 64})
        with self.assertRaises(ReportRefused) as caught:
            render_reading_table(self.harness, bare)
        self.assertEqual(caught.exception.code, "SOURCE_PIN_MISSING")
        self.assertIn("CEILING.md", str(caught.exception))

    def test_a_plan_body_without_a_pins_map_is_a_plan_refusal_not_a_ceiling_one(self):
        with self.assertRaises(ReportRefused) as caught:
            render_reading_table(self.harness, {"not-pins": {}})
        self.assertEqual(caught.exception.code, "PIN_MAP_MISSING")

    def test_a_plan_that_is_not_a_plan_is_refused(self):
        with self.assertRaises(StandardInvalid) as caught:
            render_reading_table(self.harness, object())
        self.assertEqual(caught.exception.code, "STANDARD_DATA_MALFORMED")

    def test_a_supplied_ceiling_text_that_is_not_the_pinned_bytes_is_refused(self):
        """The ceiling text the run carried is checked as bytes, not only the pin."""
        substituted = plan(ceiling_text="a ceiling somebody typed out again")
        for renderer in (render_reading_table, render_comparison):
            with self.subTest(renderer=renderer.__name__):
                with self.assertRaises(StandardInvalid) as caught:
                    renderer(self.harness, substituted)
                self.assertEqual(caught.exception.code, "STANDARD_DATA_MALFORMED")

    def test_the_frozen_ceiling_itself_passes(self):
        self.assertEqual(
            ceiling_key_of(plan()),
            "src/minireason/loop/data/ceiling_v1.md")

    def test_render_cycle_and_render_closing_hold_the_same_pin_through_the_plan(self):
        """CYCLE and CLOSING refuse a plan that lies about the ceiling too."""
        with self.assertRaises(ReportRefused) as caught:
            render_closing(ClosingRun(plan=ReportPlan(pins={CEILING_PIN_KEY: "1" * 64}),
                                      decision=stop_decision()))
        self.assertEqual(caught.exception.code, "SOURCE_PIN_MISMATCH")

    def test_the_ceiling_pin_key_has_exactly_one_owner(self):
        self.assertEqual(standard.CEILING_PATH.name, "ceiling_v1.md")
        self.assertEqual(
            standard.CEILING_PIN_KEY,
            standard.CEILING_PATH.relative_to(
                Path(standard.__file__).resolve().parents[3]).as_posix())
        self.assertEqual(
            ceiling_key_of({"pins": {standard.CEILING_PIN_KEY:
                                     standard.CEILING_SHA256}}),
            standard.CEILING_PIN_KEY)
        source = Path(R.__file__).resolve().read_text(encoding="utf-8")
        self.assertNotIn("loop/data/", source,
                         "report may not spell the ceiling's path: standard owns it")

    def test_the_ceiling_sentences_are_the_frozen_files_own(self):
        self.assertEqual(len(CEILING_REQUIRED_SENTENCES), 11)
        for sentence in CEILING_REQUIRED_SENTENCES:
            self.assertIn(sentence, standard.CEILING_TEXT)


# ---------------------------------------------------------------------------
# Every required ceiling sentence, verbatim, everywhere
# ---------------------------------------------------------------------------


class EveryRequiredCeilingSentenceAppearsVerbatim(ReportTestCase):

    def test_every_required_sentence_is_verbatim_in_the_reading_table(self):
        text = render_reading_table(self.harness, plan())
        for sentence in CEILING_REQUIRED_SENTENCES:
            with self.subTest(sentence=sentence[:40]):
                self.assertIn(sentence, text)

    def test_every_required_sentence_is_verbatim_in_the_comparison(self):
        text = render_comparison(self.harness, plan())
        for sentence in CEILING_REQUIRED_SENTENCES:
            with self.subTest(sentence=sentence[:40]):
                self.assertIn(sentence, text)

    def test_every_required_sentence_is_verbatim_in_a_cycle_record(self):
        before = self.situation(1)
        outcome = decide(before, self.situation(2), 2, self.config, self.obligations)
        text = render_cycle(outcome, CycleState())
        for sentence in CEILING_REQUIRED_SENTENCES:
            with self.subTest(sentence=sentence[:40]):
                self.assertIn(sentence, text)

    def test_every_required_sentence_is_verbatim_in_the_closing_record(self):
        text = render_closing(ClosingRun(plan=plan(), decision=stop_decision()))
        for sentence in CEILING_REQUIRED_SENTENCES:
            with self.subTest(sentence=sentence[:40]):
                self.assertIn(sentence, text)

    def test_the_list_exported_is_the_standards_own_object(self):
        """One owner: re-exported, never retyped (module deviation 1)."""
        self.assertIs(CEILING_REQUIRED_SENTENCES, standard.CEILING_REQUIRED_SENTENCES)

    def test_each_sentence_is_printed_as_its_own_plain_paragraph(self):
        text = render_reading_table(self.harness, plan())
        for sentence in CEILING_REQUIRED_SENTENCES:
            with self.subTest(sentence=sentence[:40]):
                marker = f"\n\n{sentence}\n\n"
                self.assertIn(marker, f"\n{text}\n")


# ---------------------------------------------------------------------------
# The block register
# ---------------------------------------------------------------------------


class BlocksPrintWithCountsByReasonCode(ReportTestCase):

    def state_with_blocks(self) -> CycleState:
        return CycleState(
            blocks=(("r1/c1", "ensemble-split"), ("r1/c2", "ensemble-split"),
                    ("r1/c3|T|original-vs-control", "order-swap")))

    def test_the_headings_are_the_ceilings_nine_reasons_plus_the_constitution_extra(self):
        self.assertEqual(tuple(BLOCK_REGISTER_HEADINGS),
                         tuple(CEILING_BLOCK_REASONS) + ("constitution",))

    def test_every_heading_prints_every_time_with_its_count(self):
        text = render_cycle(stop_decision(), self.state_with_blocks())
        self.assertIn("| `ensemble-split` x2 | r1/c1, r1/c2 |", text)
        self.assertIn("| `order-swap` x1 | r1/c3|T|original-vs-control |", text)
        for reason in BLOCK_REGISTER_HEADINGS:
            with self.subTest(reason=reason):
                if reason not in ("ensemble-split", "order-swap"):
                    self.assertIn(f"| `{reason}` x0 | - |", text)

    def test_a_run_with_no_blocks_prints_the_complete_empty_register(self):
        text = render_cycle(stop_decision(), CycleState())
        for reason in CEILING_BLOCK_REASONS:
            with self.subTest(reason=reason):
                self.assertIn(f"| `{reason}` x0 |", text)

    def test_the_counts_are_the_ceilings_own_requirement_and_print_nowhere_else(self):
        text = render_cycle(stop_decision(), CycleState(
            blocks=(("r1/c1", "schema"),)))
        self.assertIn("| `schema` x1 | r1/c1 |", text)
        self.assertIn("printed with counts", text)
        self.assertNotIn("x2", text)

    def test_the_closing_register_is_over_the_runs_blocks_not_one_cycles(self):
        run = ClosingRun(plan=plan(), decision=stop_decision(),
                         blocks=(("r1/c1", "provider"), ("r1/c2", "provider")))
        text = render_closing(run)
        self.assertIn("| `provider` x2 | r1/c1, r1/c2 |", text)

    def test_a_reason_outside_the_closed_vocabulary_is_refused_not_rendered(self):
        for reason in ("made-up-block", "SCORE", ""):
            with self.subTest(reason=reason):
                with self.assertRaises(StandardInvalid) as caught:
                    CycleState(blocks=(("r1/c1", reason),))
                self.assertEqual(caught.exception.code, "STANDARD_DATA_MALFORMED")


# ---------------------------------------------------------------------------
# Declined to read
# ---------------------------------------------------------------------------


class AnAllBlockedRunRendersAsDeclinedToRead(ReportTestCase):

    def closing(self) -> ClosingRun:
        standings = graph.cell_standings(self.harness)
        return ClosingRun(
            plan=plan(), decision=stop_decision(), standings=standings,
            blocks=((standing.key, "ensemble-split") for standing in standings))

    def test_the_sentence_and_the_word_print(self):
        text = render_closing(self.closing())
        self.assertIn(DECLINED_TO_READ_SENTENCE, text)
        self.assertIn("declined", text)

    def test_the_run_is_never_described_as_an_absence_of_relations(self):
        text = render_closing(self.closing())
        for forbidden in ("no relations found", "no relation found",
                          "nothing was found", "no readings found"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text.lower())

    def test_an_empty_reading_table_carries_the_sentence_too(self):
        harness = graph.open_graph(self.root / "empty", clock=graph.fixed_clock())
        text = render_reading_table(harness, plan())
        self.assertIn(DECLINED_TO_READ_SENTENCE, text)
        self.assertNotIn("no relations found", text.lower())

    def test_a_run_with_a_read_cell_does_not_claim_declined(self):
        self.mark()
        text = render_closing(ClosingRun(
            plan=plan(), decision=stop_decision(),
            standings=graph.cell_standings(self.harness)))
        self.assertNotIn(DECLINED_TO_READ_SENTENCE, text)


class TheReadingTableCarriesItsOwnBlockRegister(ReportTestCase):
    """The draft's ``render_reading_table`` built ``machine = []`` and never
    filled it, so READING_TABLE.md printed ``x0`` against every reason on a run
    that was entirely blocked, and its machine-unresolved section was always
    empty. A blocked trial registers nothing, so the blocks can only arrive from
    the caller; the renderer now takes the cycle's own ``CycleState``."""

    def blocked_state(self) -> CycleState:
        return CycleState(
            standings=graph.cell_standings(self.harness),
            blocks=(("r1/c1", "ensemble-split"), ("r1/c2", "paraphrase-flip")))

    def test_the_reading_table_prints_the_register_with_counts(self):
        text = render_reading_table(self.harness, plan(), state=self.blocked_state())
        self.assertIn("| `ensemble-split` x1 | r1/c1 |", text)
        self.assertIn("| `paraphrase-flip` x1 | r1/c2 |", text)
        self.assertIn("| `provider` x0 | - |", text)

    def test_the_reading_table_names_the_code_that_declined_each_cell(self):
        text = render_reading_table(self.harness, plan(), state=self.blocked_state())
        self.assertIn(R.block_line("r1/c1", "ensemble-split"), text)
        self.assertIn(R.block_line("r1/c2", "paraphrase-flip"), text)

    def test_an_all_blocked_reading_table_renders_as_declined_to_read(self):
        text = render_reading_table(self.harness, plan(), state=self.blocked_state())
        self.assertIn(DECLINED_TO_READ_SENTENCE, text)
        for forbidden in ("no relations found", "no relation was found"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text.lower())

    def test_a_deliberate_unresolved_run_does_not_claim_the_instrument_declined(self):
        """Three ways to read nothing, and they are not one fact. A run whose
        cells were read and stayed at the grounded default is unresolved, not
        declined; the draft's closing-record condition called it declined."""
        text = render_reading_table(self.harness, plan(), state=CycleState(
            standings=graph.cell_standings(self.harness)))
        self.assertNotIn(DECLINED_TO_READ_SENTENCE, text)
        self.assertIn("### unresolved", text)
        closing = render_closing(ClosingRun(
            plan=plan(), decision=stop_decision(),
            standings=graph.cell_standings(self.harness)))
        self.assertNotIn(DECLINED_TO_READ_SENTENCE, closing)

    def test_the_declared_two_argument_call_still_renders(self):
        text = render_reading_table(self.harness, plan())
        self.assertIn("| `ensemble-split` x0 | - |", text)

    def test_the_unread_inventory_unions_the_plan_and_the_callers_own(self):
        """REVIEW-PREREG PR-13: the plan's ``reading_set`` is not the whole
        unread inventory - a cell the reading set never named is unread too, and
        the trichotomy clause rests on the inventory being complete. The caller
        may hand its own list and the two are unioned, minus whatever opened."""
        text = render_reading_table(
            self.harness, plan(reading_set=("r1/c1", "r8/c8")),
            state=CycleState(unread=("r9/c9",)))
        self.assertIn(f"- r8/c8: {R.UNREAD_SENTENCE}", text)
        self.assertIn(f"- r9/c9: {R.UNREAD_SENTENCE}", text)
        self.assertNotIn(f"- r1/c1: {R.UNREAD_SENTENCE}", text)

    def test_a_blocked_cell_that_never_opened_prints_in_exactly_one_state(self):
        """The draft printed such a cell as ``unread`` in the trichotomy table
        while also listing it under machine-unresolved, so one cell appeared in
        two of the three states the ceiling says are distinct."""
        text = render_reading_table(
            self.harness, plan(),
            state=CycleState(blocks=(("r9/c9", "referential-integrity"),),
                             unread=("r9/c9",)))
        self.assertIn(R.block_line("r9/c9", "referential-integrity"), text)
        self.assertNotIn(f"- r9/c9: {R.UNREAD_SENTENCE}", text)
        row = [line for line in text.splitlines() if line.startswith("| r9/c9 |")]
        self.assertEqual(len(row), 1)
        self.assertIn(R.CELL_MACHINE_WORD, row[0])
        self.assertNotIn(f"| {R.CELL_UNREAD_SENTENCE} |", row[0])

    def test_a_state_that_is_not_a_cycle_state_is_refused(self):
        for renderer in (render_reading_table, render_comparison):
            with self.subTest(renderer=renderer.__name__):
                with self.assertRaises(StandardInvalid):
                    renderer(self.harness, plan(), state={"blocks": ()})

    def test_the_comparison_prints_the_register_it_promises(self):
        text = render_comparison(self.harness, plan(), state=CycleState(
            blocks=(("r1/c3|T|original-vs-control", "order-swap"),)))
        self.assertIn("| `order-swap` x1 | r1/c3|T|original-vs-control |", text)
        self.assertIn("printed with counts", text)

    def test_the_comparison_reads_the_cell_key_through_the_graph(self):
        self.mark()
        text = render_comparison(self.harness, plan())
        self.assertIn("| r1/c3 | T | original-vs-control | differs |", text)
        source = Path(R.__file__).resolve().read_text(encoding="utf-8")
        self.assertNotIn('split("|")', source,
                         "the cell key's separator is graph.CellKey's, not this "
                         "module's")


class AProtectedLossStillSaysWhatWouldReopenIt(ReportTestCase):
    """Design 5: "Every stop carries a mandatory would_reopen prose field."
    The draft printed the protected-loss sentence *instead of* would_reopen, so
    the one stop that most needs to say what would reopen the question was the
    one record that did not."""

    def loss_decision(self) -> Decision:
        return Decision(
            cycle=1, stop=True, reason=STOP_PROTECTED_LOSS,
            clause=CLAUSE_PROTECTED_LOSS,
            detail="p6 was satisfied and is not",
            would_reopen=WOULD_REOPEN[STOP_PROTECTED_LOSS])

    def test_the_cycle_record_prints_both(self):
        text = render_cycle(self.loss_decision(), CycleState())
        from minireason.loop import decide as D
        self.assertIs(R.PROTECTED_LOSS_SENTENCE, D.PROTECTED_LOSS_SENTENCE)
        self.assertIs(R.LOSSES_OUTSIDE_P_SENTENCE, D.NET_WITHDRAWAL_SENTENCE)
        self.assertIn(f"- would_reopen: {WOULD_REOPEN[STOP_PROTECTED_LOSS]}", text)

    def test_the_closing_record_prints_would_reopen_for_every_stop(self):
        text = render_closing(ClosingRun(plan=plan(),
                                         decision=self.loss_decision()))
        self.assertIn(f"- would_reopen: {WOULD_REOPEN[STOP_PROTECTED_LOSS]}", text)


class TheRenderedFilesRecordHasOneOwner(ReportTestCase):
    """WAVE2-INTERFACE open question 3: p4 and p12 both read a ``rendered_files``
    record and nothing wrote one. This module owns the shape, and the text in it
    is the rendered bytes, because p4 tokenises headings out of the text."""

    def test_the_shape_is_the_one_the_obligation_reads(self):
        record = R.rendered_files_record({"CLOSING.md": "# x\n"})
        self.assertEqual(record, {"record": R.RENDERED_FILES_RECORD,
                                  "files": {"CLOSING.md": "# x\n"}})
        self.assertEqual(R.RENDERED_FILES_RECORD, "rendered_files")

    def test_p4_reads_the_rendered_bytes_of_a_real_render(self):
        from minireason.loop import obligations as ob
        text = render_closing(ClosingRun(plan=plan(), decision=stop_decision()))
        record = R.rendered_files_record({"CLOSING.md": text})
        self.assertEqual(ob.RENDERED_FILES, record["record"])
        self.assertEqual(record["files"]["CLOSING.md"], text)

    def test_a_forbidden_header_in_a_rendered_file_is_refused_before_it_is_written(self):
        with self.assertRaises(LoopError):
            standard.assert_no_scoring_headers(
                "| cell | rank |\n| --- | --- |\n", "a fixture")


# ---------------------------------------------------------------------------
# The trichotomy
# ---------------------------------------------------------------------------


class TheThreeCellStatesPrintAsThreeThings(ReportTestCase):

    def state(self) -> CycleState:
        self.mark()
        standings = graph.cell_standings(self.harness)
        unread_key = "r1/c9"
        machine = ("r1/c2", "outside-vocabulary")
        return CycleState(standings=standings,
                          blocks=(machine,),
                          unread=(unread_key,))

    def test_three_words_three_sections_three_distinct_spellings(self):
        text = render_cycle(stop_decision(), self.state())
        for heading in ("### unread", "### unresolved", "### machine-unresolved"):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)
        self.assertIn("| r1/c9 | unread | - |", text)
        self.assertIn("| r1/c1 | unresolved | - |", text)
        self.assertIn("| r1/c2 | machine-unresolved (outside-vocabulary) | "
                      "`outside-vocabulary` |", text)

    def test_the_mark_cell_prints_its_own_register_state_not_anothers(self):
        text = render_cycle(stop_decision(), self.state())
        self.assertIn("| r1/c3|T|original-vs-control | read: differs | - |", text)

    def test_no_two_states_share_a_word(self):
        words = set()
        text = render_cycle(stop_decision(), self.state())
        for word in ("unread", "unresolved", "machine-unresolved"):
            with self.subTest(word=word):
                self.assertNotIn(word, words)
                words.add(word)
        self.assertIn("Conflating any two would let an unfinished worksheet "
                      "read as a finding.", text)

    def test_a_contested_cell_prints_as_a_discrimination_problem(self):
        """Two survivors are never an average, and print as their own word.

        The contest is exercised in ``render_reading_table``, the one renderer
        whose purpose is the word; the trichotomy row carries ``contested`` and
        the read-below print carries the prose."""
        self.mark(token="same")
        self.mark(token="differs")
        standings = graph.cell_standings(self.harness)
        self.assertIn("contested", {s.state for s in standings})
        cycle = render_cycle(stop_decision(), CycleState(standings=standings))
        self.assertIn("| r1/c3|T|original-vs-control | contested | - |", cycle)
        text = render_reading_table(self.harness, plan())
        self.assertIn("r1/c3|T|original-vs-control: contested; two rival "
                      "readings survive", text)
        self.assertIn("discrimination problem", text.lower())

    def test_an_indeterminate_coordinate_is_a_delivery_fact_never_a_reading(self):
        text = render_cycle(stop_decision(), CycleState(
            indeterminate=("r1/c1/critic#0",)))
        self.assertIn(INDETERMINATE_SENTENCE, text)
        self.assertIn("- r1/c1/critic#0", text)

    def test_an_unknown_cell_state_is_not_invented_by_the_renderer(self):
        with self.assertRaises(StandardInvalid):
            CycleState(standings=(object(),))


# ---------------------------------------------------------------------------
# The prohibited tokens
# ---------------------------------------------------------------------------


class NoRenderedArtifactCarriesAProhibitedToken(ReportTestCase):

    def artifacts(self) -> dict:
        before = self.situation(1)
        outcome = decide(before, self.situation(2), 2, self.config, self.obligations)
        return {
            "READING_TABLE.md": render_reading_table(self.harness, plan()),
            "COMPARISON.md": render_comparison(self.harness, plan()),
            "CYCLE.md": render_cycle(outcome, CycleState(
                indeterminate=("r1/c1/critic#0",))),
            "CLOSING.md": render_closing(ClosingRun(
                plan=plan(), decision=stop_decision())),
        }

    def test_no_score_no_rank_anywhere(self):
        """The guard is ``assert_no_scoring_headers`` over the headings, plus
        a body-line scan once the ceiling's own prose (which mentions the words
        it forbids) has had its sentences accounted for."""
        for name, text in self.artifacts().items():
            with self.subTest(artifact=name):
                standard.assert_no_scoring_headers(text, name)
                scanned = text
                for sentence in (CEILING_REQUIRED_SENTENCES
                                 + (R.CEILING_PRELUDE,)):
                    scanned = scanned.replace(sentence, "")
                for token in (" rank ", " score ", " scoring"):
                    self.assertNotIn(token, scanned.lower())

    def test_the_exhaustion_token_survives_only_inside_the_ceilings_denial(self):
        for name, text in self.artifacts().items():
            with self.subTest(artifact=name):
                standard.assert_no_exhaustion_claim(text, name)
                scanned = text.replace(standard.CEILING_EXHAUSTION_DENIAL, "")
                for sentence in CEILING_REQUIRED_SENTENCES:
                    scanned = scanned.replace(sentence, "")
                self.assertNotIn("exhaust", scanned.casefold())

    def test_no_combined_register_field_is_ever_emitted(self):
        """No field holds two registers at once; the one place the word
        "combined" may appear is the design's own denial sentence."""
        self.mark()
        text = render_comparison(self.harness, plan())
        denied = "marked separately and never combined"
        self.assertIn(denied, text)
        scanned = text.lower().replace(denied, "")
        for sentence in CEILING_REQUIRED_SENTENCES:
            scanned = scanned.replace(sentence.lower(), "")
        for forbidden in ("combined", "across registers", "t+e"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, scanned)

    def test_marks_are_reported_per_register_and_never_merged(self):
        self.mark(token="differs")
        text = render_comparison(self.harness, plan())
        self.assertIn("| r1/c3 | T | original-vs-control | differs |", text)
        self.assertNotIn("r1/c3 | T +", text)

    def test_every_artifact_is_a_record_the_scoring_key_guard_accepts(self):
        for name, text in self.artifacts().items():
            with self.subTest(artifact=name):
                from minireason.loop import contracts
                contracts.assert_no_scoring_keys(
                    {"record": "rendered_files", "files": {name: text}})

    def test_report_refusals_are_declared_codes_and_loop_errors(self):
        for code, why in R.NEW_CODES.items():
            with self.subTest(code=code):
                self.assertEqual(getattr(R, code), code)
                self.assertTrue(why.strip())
                self.assertNotIn("\n", why)
                self.assertNotIn(code, loop_types.FAILURE_CODES)
        with self.assertRaises(LoopError):
            render_reading_table(self.harness, ReportPlan(
                pins={CEILING_PIN_KEY: "f" * 64}))


# ---------------------------------------------------------------------------
# losses_outside_P
# ---------------------------------------------------------------------------


class LossesOutsidePIsPresentWhenEmpty(ReportTestCase):

    def test_the_cycle_record_prints_the_section_present_and_empty(self):
        before = self.situation(1)
        outcome = decide(before, self.situation(2), 2, self.config, self.obligations)
        text = render_cycle(outcome, CycleState())
        self.assertIn("## losses_outside_P", text)
        section = text.split("## losses_outside_P")[1].split("##")[0]
        self.assertIn(LOSSES_OUTSIDE_P_SENTENCE, section)
        self.assertIn(R.NO_LOSSES_OUTSIDE_P, section)

    def test_the_closing_record_prints_it_present_and_empty(self):
        outcome = stop_decision()
        text = render_closing(ClosingRun(plan=plan(), decision=outcome))
        self.assertIn("## losses_outside_P", text)
        section = text.split("## losses_outside_P")[1].split("##")[0]
        self.assertIn("- none", section)

    def test_a_loss_prints_with_its_membership_and_detail(self):
        from minireason.loop.obligations import Loss
        outcome = stop_decision()
        text = render_closing(ClosingRun(plan=plan(), decision=Decision(
            cycle=2, stop=True, reason="protected_loss",
            clause="clause_one_protected_loss",
            detail="the protected obligations lost here are p3",
            would_reopen=WOULD_REOPEN["protected_loss"],
            losses_outside_p=(Loss(kind="loss", subject="p6", was="satisfied",
                                   now="not_satisfied", detail="read"),))))
        self.assertIn("- loss: p6 was satisfied, now not_satisfied "
                      "[outside P] - read", text)


# ---------------------------------------------------------------------------
# The appellate declaration
# ---------------------------------------------------------------------------


class AppellateRulingsZeroRendersNotValidated(ReportTestCase):

    def test_zero_rulings_render_the_not_validated_sentence(self):
        text = render_closing(ClosingRun(plan=plan(), decision=stop_decision(),
                                         appellate_rulings=()))
        self.assertIn("`appellate_rulings: 0`", text)
        self.assertIn(APPELLATE_NOT_VALIDATED_SENTENCE, text)
        for forbidden in ("validated", "checked", "confirmed"):
            with self.subTest(forbidden=forbidden):
                self.assertIn(forbidden, APPELLATE_NOT_VALIDATED_SENTENCE)

    def test_the_sentence_appears_where_the_count_is_printed(self):
        text = render_closing(ClosingRun(plan=plan(), decision=stop_decision()))
        self.assertLess(text.index("`appellate_rulings: 0`"),
                        text.index(APPELLATE_NOT_VALIDATED_SENTENCE))

    def test_rulings_present_name_them_and_do_not_claim_validation(self):
        ruling = "ruling-1"
        text = render_closing(ClosingRun(plan=plan(), decision=stop_decision(),
                                         appellate_rulings=(ruling,)))
        self.assertIn("`appellate_rulings: 1`", text)
        self.assertIn(f"- {ruling}", text)
        self.assertNotIn(APPELLATE_NOT_VALIDATED_SENTENCE, text)


# ---------------------------------------------------------------------------
# The closing record's own anatomy
# ---------------------------------------------------------------------------


class TheClosingRecord(ReportTestCase):

    def test_an_open_chain_is_refused_rather_than_rendered_as_closed(self):
        continuing = Decision(cycle=1, stop=False, reason=CONTINUE_OPEN,
                              clause=CLAUSE_NONE, would_reopen="prose")
        with self.assertRaises(StandardInvalid) as caught:
            render_closing(ClosingRun(plan=plan(), decision=continuing))
        self.assertEqual(caught.exception.code, "STANDARD_DATA_MALFORMED")

    def test_the_stopping_sentence_is_the_decisions_own(self):
        outcome = stop_decision()
        text = render_closing(ClosingRun(plan=plan(), decision=outcome))
        self.assertIn("## the stopping sentence", text)
        self.assertIn(f"STOP: {STOP_RESOURCE_BOUNDARY}", text)
        self.assertIn(outcome.would_reopen, text)

    def test_every_section_a_closing_record_promises_is_there(self):
        text = render_closing(ClosingRun(
            plan=plan(), decision=stop_decision(),
            audit_findings=({"seat": "judge-1", "kind": "paraphrase-invariance",
                             "detail": "no flip"},),
            indeterminate=("r1/c3/marker#1",)))
        for heading in ("## the frozen ceiling block",
                        "## block register by reason code",
                        "## the audit record in force",
                        "## the stopping sentence", "## losses_outside_P",
                        "## INDETERMINATE", "## appellate_rulings",
                        "## the unread / unresolved / machine-unresolved trichotomy"):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)
        self.assertIn("- paraphrase-invariance for judge-1: no flip", text)

    def test_the_identity_and_the_pin_line_carry_the_plan(self):
        text = render_closing(ClosingRun(plan=plan(), decision=stop_decision()))
        self.assertIn(f"- loop_plan_id: {'c' * 64}", text)
        self.assertIn(f"- ceiling_sha256: {standard.CEILING_SHA256}", text)
        self.assertIn(f"- ceiling_pinned_at: {CEILING_PIN_KEY}", text)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
