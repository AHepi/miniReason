"""W4-MARKER: register marking over the residue, and the falsifier evaluation.

Every class is named for one clause of the W4-MARKER acceptance list, and every
test in it is one reading of that clause.

**The guard is real.**  The draft this file replaces injected a fake runner
returning ``FakeTrialResult(outcome, blocks, transcript)`` and called
``trial.run_trial`` with ``mode="pairwise"`` - a call the trial as built
refuses twice over (``TRIAL_MODE_UNEXPECTED`` on the mode, and again on a
register cell key), which
:class:`TheRelationTrialRefusesAPairwiseCall` demonstrates by execution.  The
pairwise guard is W4-MARKER's own, and here it is driven end to end: W2-PACKS
renders the register pack and both presentation orders, W2-ROLES spends each
call through its own gates onto a scripted ``OfflineProvider`` and writes the
write-once record, W1-SURFACE resolves the two citations through
``markprep.resolve_pair``, and W1-GRAPH registers the marks.  The socket layer
is removed from under every call.
"""
from __future__ import annotations

import ast
import contextlib
import copy
import json
import shutil
import socket
import tempfile
import unittest
from pathlib import Path

from minireason import provider_openai_compat as transport
from minireason.loop import contracts as C
from minireason.loop import graph as G
from minireason.loop import marker as K
from minireason.loop import markprep as M
from minireason.loop import packs as P
from minireason.loop import seats
from minireason.loop import standard as STD
from minireason.loop import synthetic
from minireason.loop import trial as T
from minireason.loop import types as loop_types

MODULE = Path(K.__file__).resolve()

#: The fixture's own address space; nothing here is a published occurrence.
ADDRESSES = {"objection": "p.objection.0", "account": "p.account.0",
             "truncation_chars": 16}
COMPARISON = M.COMPARISON_LABELS[("ORIGINAL", "CONTROL")]


# --------------------------------------------------------------------------
# The socket guard
# --------------------------------------------------------------------------


class _SocketsUsed(AssertionError):
    pass


_PRISTINE = (socket.socket, socket.create_connection, transport._open)


def _refuse_socket(*args, **kwargs):
    raise _SocketsUsed("a test opened a socket")


@contextlib.contextmanager
def no_sockets():
    socket.socket = socket.create_connection = transport._open = _refuse_socket
    try:
        yield
    finally:
        socket.socket, socket.create_connection, transport._open = _PRISTINE


# --------------------------------------------------------------------------
# Cells
# --------------------------------------------------------------------------


def a_cell(case: str = "case-a", **kwargs) -> M.Cell:
    """One synthetic ORIGINAL-vs-CONTROL cell, D1's own comparison."""
    defaults = {"addresses": ADDRESSES, "objection_ids": ("a1", "a2")}
    defaults.update(kwargs)
    return M.cell_from_contrast_leg(synthetic.contrast_leg(), case, **defaults)


def baseline_exhibiting_cell() -> M.Cell:
    """A cell whose *within-ORIGINAL* replicates already differ on D's kinds.

    Two of the three ORIGINAL replicates carry a ``revises`` the first does
    not, so the frozen baseline's kind set for D holds ``disposition_value``
    and ``disposition_carrier_field`` - which is exactly what G9 downgrades a
    cross-case ``differs`` against.  ORIGINAL and CONTROL engage different
    criticisms, so the *comparison* stays in the residue.
    """
    leg = copy.deepcopy(synthetic.contrast_leg())
    replicates = leg["cases"]["case-a"]["replicates"]
    for name in sorted(replicates)[1:]:
        body = json.loads(replicates[name]["ORIGINAL"])
        body["records"][0]["revises"] = ["c0"]
        replicates[name]["ORIGINAL"] = json.dumps(body)
    return M.cell_from_contrast_leg(
        leg, "case-a", addresses=ADDRESSES, objection_ids=("a1", "a2"))


def byte_identical_cell() -> M.Cell:
    """A cell whose every ORIGINAL replicate is its CONTROL replicate's bytes."""
    leg = copy.deepcopy(synthetic.contrast_leg())
    replicates = leg["cases"]["case-d"]["replicates"]
    leg["cases"]["case-d"]["replicates"] = {
        name: {"ORIGINAL": sides["ORIGINAL"], "CONTROL": sides["ORIGINAL"],
               "byte_identical": True}
        for name, sides in replicates.items()
    }
    return M.cell_from_contrast_leg(
        leg, "case-d", addresses=ADDRESSES, objection_ids=("a1", "a2"))


#: Key-env NAMES only, never values, and deliberately this wave's own: runner
#: v2's ``key_gate`` registry is process-wide and refuses a second cap for one
#: credential, so a fixture that reused ``SYNTHETIC_ALPHA_KEY`` (cap 2 in
#: ``loop.synthetic``) at cap 5 would make ``tests/loop/test_roles.py`` raise
#: CONCURRENCY_LIMIT_CONFLICT depending on discovery order.
def build_registry() -> dict:
    def endpoint(name: str, family: str, key_env: str) -> transport.Endpoint:
        return transport.Endpoint(
            name=name, base_url=f"https://{name.split('/')[-1]}.synthetic.invalid/v1",
            model=f"model-{name.split('/')[-1]}", key_env=key_env, family=family,
            chat_path="/chat/completions", native=False, max_concurrency=5,
            timeout_seconds=120)

    entries = [
        endpoint("synthetic/alpha-1", "alpha-family", "W4_ALPHA_KEY"),
        endpoint("synthetic/alpha-2", "alpha-family", "W4_ALPHA_KEY"),
        endpoint("synthetic/beta", "beta-family", "W4_BETA_KEY"),
        endpoint("synthetic/gamma", "gamma-family", "W4_GAMMA_KEY"),
        endpoint("synthetic/delta", "delta-family", "W4_DELTA_KEY"),
        endpoint("synthetic/epsilon", "epsilon-family", "W4_EPSILON_KEY"),
    ]
    return {e.name: e for e in entries}


def build_config() -> loop_types.LoopConfig:
    return loop_types.LoopConfig.from_mapping({
        "run_id": "marker-test", "study": "synthetic", "occurrences": ["occ"],
        "runner": "tools/multicycle_commitment_study_multi_v2.py",
        "cycle_budget": 1, "max_calls": 200, "reading_set": ["row-a"],
        "obligations_path": "obligations.json", "graph_root": "graph",
        "reopen_reasons": list(STD.REOPEN_REASONS),
        "audit": {"period": 4, "judge_err_max": 0.2, "streak_max": 3,
                  "judge_err_max_account": "one wrong anchor of five is one too many",
                  "streak_max_account": "three guard blocks in a row stop one role"},
    })


class Scripted:
    """One reply queue per ``(role, coordinate)``, consumed across calls."""

    def __init__(self, default=None, scripts=None) -> None:
        self.default = default
        self.scripts = {k: list(v) for k, v in (scripts or {}).items()}
        self.calls: list = []

    def __call__(self, role, coordinate, records_dir, *, seat=None, endpoint=None):
        self.calls.append((role, coordinate))
        queue = self.scripts.get((role, coordinate))
        if queue:
            reply = queue.pop(0)
        elif self.default is not None:
            reply = self.default
        else:
            raise AssertionError(f"unscripted call {role!r} {coordinate!r}")
        return transport.OfflineProvider(
            endpoint, records_dir, [json.dumps(reply)])


def mark_output(mark: str = "unresolved", kind: str | None = None,
                left: str = "", right: str = "",
                case: str = "the two sides read alike on this register") -> dict:
    return {"mark": mark, "difference_kind": kind, "left_quote": left,
            "right_quote": right, "case": case}


class MarkerCase(unittest.TestCase):
    """One temp run: a cell, its sealed baseline, an open graph, a seat plan."""

    def setUp(self) -> None:
        super().setUp()
        self.tmp = Path(tempfile.mkdtemp(prefix="loop-marker-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.harness = G.open_graph(self.tmp / "graph", clock=G.fixed_clock())
        self.standard_id = G.register_standard(self.harness, STD.STANDARD_BODY)
        self.records = self.tmp / "marks"
        self.records.mkdir()
        self.plan = seats.select_seats(build_registry())
        self.config = build_config()

    # -- helpers ----------------------------------------------------------

    def sealed(self, cell: M.Cell) -> str:
        self._seals = getattr(self, "_seals", 0) + 1
        out = self.tmp / f"baseline-{self._seals}"
        out.mkdir()
        return M.write_baseline(cell, None, out)

    def open_cells_for(self, cell: M.Cell) -> None:
        keys = [G.CellKey(cell=cell.cell_id, register=register, comparison=COMPARISON)
                for register in K.REGISTERS]
        G.open_cells(self.harness, keys)

    def prepare(self, cell: M.Cell) -> str:
        seal = self.sealed(cell)
        self.open_cells_for(cell)
        return seal

    def mark(self, cell: M.Cell, factory, *, seal: str | None = None,
             records: Path | None = None, **kwargs) -> K.CellMarks:
        with no_sockets():
            return K.mark_cell(
                self.harness, cell, seal if seal is not None else cell.baseline_sha,
                STD.STANDARD_BODY, self.plan, self.config,
                records_dir=records or self.records,
                provider_factory=factory, **kwargs)

    def quotes_for(self, cell: M.Cell, row: M.ResidueRow) -> tuple[str, str]:
        """Two citations that resolve uniquely, one per side of the surface."""
        left_key = row.left_replicates[0]
        right_key = row.right_replicates[0]
        surface = M.pairwise_surface(cell, left_key, right_key)
        left = cell.replicate(left_key).commitments
        right = cell.replicate(right_key).commitments
        return (_unique_span(surface, left), _unique_span(surface, right))


def _unique_span(surface, text: str) -> str:
    """The longest prefix-anchored span of ``text`` that resolves exactly once."""
    for size in (120, 90, 70, 50, 40, 30):
        for start in range(0, max(1, len(text) - size), 7):
            candidate = text[start:start + size]
            if candidate and surface.count(candidate) == 1:
                return candidate
    raise AssertionError("no uniquely resolving span in this side")


# --------------------------------------------------------------------------
# The reconciliation finding: the relation trial refuses a pairwise call
# --------------------------------------------------------------------------


class TheRelationTrialRefusesAPairwiseCall(MarkerCase):
    """Why this module owns the pairwise guard rather than calling W3-TRIAL."""

    def test_a_pairwise_mode_is_refused_by_the_trial(self):
        cell = a_cell()
        self.prepare(cell)
        surface = M.pairwise_surface(cell, "ORIGINAL/rep1", "CONTROL/rep1")
        with self.assertRaises(loop_types.LoopError) as caught:
            T.run_trial(self.harness, surface, STD.STANDARD_BODY, self.plan,
                        self.config, mode=STD.MODE_PAIRWISE, key="x",
                        records_dir=self.records)
        self.assertEqual(caught.exception.code, T.TRIAL_MODE_UNEXPECTED)

    def test_a_register_cell_key_is_refused_by_the_trial(self):
        cell = a_cell()
        self.prepare(cell)
        surface = M.pairwise_surface(cell, "ORIGINAL/rep1", "CONTROL/rep1")
        key = G.CellKey(cell=cell.cell_id, register="D", comparison=COMPARISON)
        with self.assertRaises(loop_types.LoopError) as caught:
            T.run_trial(self.harness, surface, STD.STANDARD_BODY, self.plan,
                        self.config, mode=STD.MODE_ABSOLUTE, key=key,
                        records_dir=self.records)
        self.assertEqual(caught.exception.code, T.TRIAL_MODE_UNEXPECTED)

    def test_this_module_never_calls_run_trial(self):
        source = MODULE.read_text(encoding="utf-8")
        body = source.split('"""', 2)[2]
        self.assertNotIn("run_trial", body)

    def test_the_block_vocabulary_is_the_trials_own(self):
        for code in (K.SCHEMA_BLOCK, K.PROVIDER_BLOCK, K.ENSEMBLE_SPLIT_BLOCK,
                     K.ORDER_SWAP_BLOCK, K.REFERENTIAL_INTEGRITY_BLOCK,
                     K.OPERATIVE_TARGET_BLOCK):
            self.assertIn(code, loop_types.BLOCK_CODES)


# --------------------------------------------------------------------------
# Clause 1 - no cross-case pack before the seal, and the sha is in the record
# --------------------------------------------------------------------------


class NoCrossCasePackRendersBeforeTheBaselineShaIsPinned(MarkerCase):
    """W4-MARKER acceptance clause 1 (G8)."""

    def test_an_unsealed_cell_refuses_before_any_call(self):
        cell = a_cell()
        self.open_cells_for(cell)
        factory = Scripted(default=mark_output())
        with self.assertRaises(M.BaselineNotFirst):
            with no_sockets():
                K.mark_cell(self.harness, cell, None, STD.STANDARD_BODY,
                            self.plan, self.config, records_dir=self.records,
                            provider_factory=factory)
        self.assertEqual(factory.calls, [])

    def test_a_sha_the_cell_does_not_carry_is_refused(self):
        cell = a_cell()
        self.prepare(cell)
        factory = Scripted(default=mark_output())
        with self.assertRaises(M.BaselineNotFirst):
            self.mark(cell, factory, seal="0" * 64)
        self.assertEqual(factory.calls, [])

    def test_the_pack_renderer_is_where_g8_lives(self):
        cell = a_cell()
        with self.assertRaises(P.BaselineNotFirst):
            P.render_register(cell.cell_id, "D", COMPARISON, None, STD.STANDARD_BODY,
                              sides=(P.MarkSide("ORIGINAL", "a"),
                                     P.MarkSide("CONTROL", "b")))

    def test_the_sha_is_pinned_into_every_call_record(self):
        cell = a_cell()
        seal = self.prepare(cell)
        out = self.mark(cell, Scripted(default=mark_output()))
        self.assertTrue(out.calls)
        for call in out.calls:
            self.assertEqual(call["baseline_sha256"], seal)
            record = json.loads(Path(call["record_path"]).read_text())
            self.assertEqual(record["settings"]["register"], call["register"])

    def test_the_sha_is_pinned_into_every_mark_row(self):
        cell = a_cell()
        seal = self.prepare(cell)
        out = self.mark(cell, Scripted(default=mark_output()))
        for block in out.comparisons.values():
            for row in block.rows.values():
                self.assertEqual(row.baseline_sha256, seal)


# --------------------------------------------------------------------------
# Clause 2 - G9's kind-grain downgrade, with the forcing pair recorded
# --------------------------------------------------------------------------


class ADiffersInTheBaselineKindSetIsWrittenSameByTheProgram(MarkerCase):
    """W4-MARKER acceptance clause 2 (G9)."""

    def setUp(self) -> None:
        super().setUp()
        self.cell = baseline_exhibiting_cell()
        self.seal = self.prepare(self.cell)
        self.row = next(r for r in M.residue(self.cell) if r.register == "D")
        self.left, self.right = self.quotes_for(self.cell, self.row)

    def differs_factory(self) -> Scripted:
        return Scripted(default=mark_output(
            "differs", "disposition_value", self.left, self.right,
            case="the two sides dispose of the criticism differently"))

    def test_the_baseline_really_exhibits_the_kind(self):
        self.assertIn("disposition_value", M.baseline_kinds(self.cell)["D"])

    def test_the_mark_written_is_same_and_the_source_is_the_program(self):
        out = self.mark(self.cell, self.differs_factory())
        row = out.row(COMPARISON, "D")
        self.assertEqual(row.mark, "same")
        self.assertEqual(row.source, K.PROGRAM_SOURCE)
        self.assertIsNone(row.difference_kind)

    def test_the_forcing_replicate_pair_is_recorded(self):
        out = self.mark(self.cell, self.differs_factory())
        row = out.row(COMPARISON, "D")
        self.assertTrue(row.forced_by)
        for pair in row.forced_by:
            self.assertIn("disposition_value", pair["kinds"])
            self.assertTrue(pair["left"].startswith("ORIGINAL/"))
            self.assertTrue(pair["right"].startswith("ORIGINAL/"))

    def test_the_downgrade_names_the_kind_it_came_from(self):
        out = self.mark(self.cell, self.differs_factory())
        row = out.row(COMPARISON, "D")
        self.assertEqual(row.evidence["downgraded_from_kind"], "disposition_value")
        self.assertEqual(row.block, M.BASELINE_FORCED_SAME_BLOCK)

    def test_a_kind_absent_from_the_baseline_stands_as_differs(self):
        cell = a_cell()          # its baseline exhibits nothing
        seal = self.prepare(cell)
        row = next(r for r in M.residue(cell) if r.register == "D")
        left, right = self.quotes_for(cell, row)
        out = self.mark(cell, Scripted(default=mark_output(
            "differs", "disposition_value", left, right)), seal=seal,
            records=self.tmp / "marks-2")
        marked = out.row(COMPARISON, "D")
        self.assertEqual(marked.mark, "differs")
        self.assertEqual(marked.source, K.TRIAL_SOURCE)
        self.assertEqual(marked.difference_kind, "disposition_value")


# --------------------------------------------------------------------------
# Clause 3 - an order-swap failure yields unresolved
# --------------------------------------------------------------------------


class AnOrderSwapFailureYieldsUnresolved(MarkerCase):
    """W4-MARKER acceptance clause 3 (G6)."""

    def setUp(self) -> None:
        super().setUp()
        self.cell = a_cell()
        self.seal = self.prepare(self.cell)
        self.row = next(r for r in M.residue(self.cell) if r.register == "D")
        self.left, self.right = self.quotes_for(self.cell, self.row)
        self.base = (f"{self.cell.cell_id}/ORIGINAL-vs-CONTROL/D")

    def flipping(self) -> Scripted:
        differs = mark_output("differs", "disposition_value", self.left, self.right)
        return Scripted(
            default=mark_output(),
            scripts={("marker", self.base): [differs, differs],
                     ("marker", self.base + "#order-swapped"):
                         [mark_output("same"), mark_output("same")]})

    def test_a_mark_that_changes_with_the_order_is_unresolved(self):
        out = self.mark(self.cell, self.flipping())
        row = out.row(COMPARISON, "D")
        self.assertEqual(row.mark, "unresolved")
        self.assertEqual(row.block, K.ORDER_SWAP_BLOCK)

    def test_both_presentations_are_recorded_verbatim(self):
        out = self.mark(self.cell, self.flipping())
        row = out.row(COMPARISON, "D")
        self.assertEqual(row.evidence[P.ORDER_AS_DECLARED]["mark"], "differs")
        self.assertEqual(row.evidence[P.ORDER_SWAPPED]["mark"], "same")

    def test_an_unresolved_row_registers_nothing(self):
        out = self.mark(self.cell, self.flipping())
        self.assertIsNone(out.row(COMPARISON, "D").registered)
        key = G.CellKey(cell=self.cell.cell_id, register="D", comparison=COMPARISON)
        self.assertEqual(G.cell_state(self.harness, key), G.UNRESOLVED)

    def test_both_orders_are_always_run(self):
        factory = Scripted(default=mark_output())
        self.mark(self.cell, factory)
        swapped = [c for c in factory.calls if c[1].endswith("#order-swapped")]
        declared = [c for c in factory.calls if not c[1].endswith("#order-swapped")]
        self.assertEqual(len(swapped), len(declared))
        self.assertTrue(swapped)

    def test_two_seats_disagreeing_at_one_presentation_is_a_split_not_a_vote(self):
        differs = mark_output("differs", "disposition_value", self.left, self.right)
        factory = Scripted(
            default=mark_output(),
            scripts={("marker", self.base): [differs, mark_output("same")],
                     ("marker", self.base + "#order-swapped"):
                         [differs, mark_output("same")]})
        out = self.mark(self.cell, factory)
        row = out.row(COMPARISON, "D")
        self.assertEqual(row.mark, "unresolved")
        self.assertEqual(row.block, K.ENSEMBLE_SPLIT_BLOCK)
        self.assertEqual(len(row.evidence["rulings"]), 2)


# --------------------------------------------------------------------------
# Clause 4 - the four registers marked separately, never combined
# --------------------------------------------------------------------------


class TheFourRegistersAreMarkedSeparatelyAndNeverCombined(MarkerCase):
    """W4-MARKER acceptance clause 4 (M1/M3)."""

    def setUp(self) -> None:
        super().setUp()
        self.cell = a_cell()
        self.seal = self.prepare(self.cell)

    def test_every_comparison_carries_exactly_the_four_registers(self):
        out = self.mark(self.cell, Scripted(default=mark_output()))
        for block in out.comparisons.values():
            self.assertEqual(sorted(block.rows), sorted(K.REGISTERS))

    def test_one_call_sees_one_register_and_no_second(self):
        factory = Scripted(default=mark_output())
        out = self.mark(self.cell, factory)
        for call in out.calls:
            self.assertIn(call["register"], K.REGISTERS)
            self.assertIn(f"/{call['register']}", call["coordinate"])
        registers = {call["register"] for call in out.calls}
        for register in registers:
            others = [r for r in K.REGISTERS if r != register]
            record = json.loads(
                Path(next(c["record_path"] for c in out.calls
                          if c["register"] == register)).read_text())
            self.assertEqual(record["settings"]["register"], register)
            self.assertNotIn("registers", record["settings"])
            del others

    def test_there_is_no_cell_level_mark_and_no_combined_view(self):
        out = self.mark(self.cell, Scripted(default=mark_output()))
        self.assertFalse(hasattr(out, "mark"))
        self.assertFalse(hasattr(out, "combined"))
        for block in out.comparisons.values():
            self.assertFalse(hasattr(block, "mark"))
            self.assertFalse(hasattr(block, "combined"))

    def test_the_rendered_record_carries_no_score_rank_or_aggregate(self):
        out = self.mark(self.cell, Scripted(default=mark_output()))
        text = json.dumps(out.as_dict())
        for forbidden in ('"score"', '"rank"', '"average"', '"majority"',
                          '"combined"', '"aggregate"', "exhaustion"):
            self.assertNotIn(forbidden, text)

    def test_a_register_the_program_settled_is_never_put_to_a_seat(self):
        factory = Scripted(default=mark_output())
        out = self.mark(self.cell, factory)
        # T is program-decided on this cell; no coordinate names it.
        self.assertEqual(out.row(COMPARISON, "T").source, K.PROGRAM_SOURCE)
        self.assertEqual([c for c in factory.calls if c[1].endswith("/T")], [])

    def test_a_row_the_program_decided_is_refused_if_offered(self):
        decided = M.ResidueRow(
            cell=self.cell.cell_id, comparison=COMPARISON,
            left_case="ORIGINAL", right_case="CONTROL", register="T",
            difference_kinds=("target_set_membership",),
            reason="offered by hand", detail="",
            left_replicates=("ORIGINAL/rep1",),
            right_replicates=("CONTROL/rep1",),
            unreadable_replicates=(), baseline_sha256=self.seal)
        with self.assertRaises(K.MarkerRefused) as caught:
            self.mark(self.cell, Scripted(default=mark_output()),
                      residue=[decided])
        self.assertEqual(caught.exception.code, K.MARKER_RESIDUE_CONTRADICTED)

    def test_register_e_forced_unresolved_by_a_bare_token_reaches_no_seat(self):
        cell = a_cell("case-b", shared_tokens=("a1",))
        seal = self.prepare(cell)
        factory = Scripted(default=mark_output())
        out = self.mark(cell, factory, seal=seal, records=self.tmp / "marks-e")
        row = out.row(COMPARISON, "E")
        self.assertEqual(row.mark, "unresolved")
        self.assertEqual(row.source, K.PROGRAM_SOURCE)
        self.assertTrue(row.evidence["forced_unresolved"])
        self.assertEqual([c for c in factory.calls if c[1].endswith("/E")], [])


# --------------------------------------------------------------------------
# Clauses 5 and 6 - G alone never carries D1; F2 and F3 fire only on T, E or D
# --------------------------------------------------------------------------


class TheFalsifierMapIsReadAndNeverRestated(MarkerCase):
    """W4-MARKER acceptance clauses 5 and 6."""

    def setUp(self) -> None:
        super().setUp()
        self.cell = a_cell()
        self.seal = self.prepare(self.cell)
        self.marks = self.mark(self.cell, Scripted(default=mark_output()))

    def test_g_is_excluded_from_every_falsifier(self):
        out = K.falsifiers(self.marks, None)
        for name, entry in out.items():
            self.assertNotIn("G", entry["carrying_registers"])
            self.assertIn("G", entry["excluded_registers"])
            del name

    def test_a_differs_on_g_alone_never_fires_d1(self):
        cell = a_cell("case-c")
        seal = self.prepare(cell)
        row = next(r for r in M.residue(cell) if r.register == "G")
        left, right = self.quotes_for(cell, row)
        base = f"{cell.cell_id}/ORIGINAL-vs-CONTROL/G"
        differs = mark_output("differs", "grounds_source", left, right)
        factory = Scripted(default=mark_output(),
                           scripts={("marker", base): [differs, differs],
                                    ("marker", base + "#order-swapped"):
                                        [differs, differs]})
        marks = self.mark(cell, factory, seal=seal, records=self.tmp / "marks-g")
        self.assertEqual(marks.row(COMPARISON, "G").mark, "differs")
        out = K.falsifiers(marks, None)
        self.assertFalse(out["D1"]["fired"])
        self.assertTrue(all(row["register"] != "G" for row in out["D1"]["carried"]))

    def test_f2_and_f3_carry_only_t_e_and_d(self):
        out = K.falsifiers(self.marks, None)
        for name in ("F2", "F3"):
            self.assertEqual(tuple(out[name]["carrying_registers"]), ("T", "E", "D"))

    def test_the_carrying_sets_are_the_standards_own_bytes(self):
        out = K.falsifiers(self.marks, None)
        for name, declared in STD.FALSIFIER_MAP.items():
            self.assertEqual(tuple(out[name]["carrying_registers"]),
                             tuple(declared.carrying_registers))
            self.assertEqual(tuple(out[name]["excluded_registers"]),
                             tuple(declared.excluded_registers))

    def test_the_module_restates_no_register_set(self):
        source = MODULE.read_text(encoding="utf-8")
        body = source.split('"""', 2)[2]
        self.assertNotIn('("T", "E", "D")', body)
        self.assertNotIn("carrying_registers =", body)

    def test_a_falsifier_that_did_not_fire_is_reported_not_fired(self):
        out = K.falsifiers(self.marks, None)
        self.assertIn("fired", out["F2"])
        self.assertIs(out["F2"]["fired"], False)

    def test_a_program_differs_on_a_carrying_register_fires_its_falsifier(self):
        out = K.falsifiers(self.marks, None)
        self.assertEqual(self.marks.row(COMPARISON, "T").mark, "differs")
        self.assertTrue(out["D1"]["fired"])
        self.assertEqual([row["register"] for row in out["D1"]["fired_rows"]], ["T"])


# --------------------------------------------------------------------------
# Clause 7 - a program finding of byte identity stands beside the marks
# --------------------------------------------------------------------------


class AProgramFindingOfByteIdentityStandsInTheFalsifierEvaluation(MarkerCase):
    """W4-MARKER acceptance clause 7 (G10(a))."""

    def setUp(self) -> None:
        super().setUp()
        self.cell = byte_identical_cell()
        self.seal = self.prepare(self.cell)
        self.marks = self.mark(self.cell, Scripted(default=mark_output()))

    def test_the_defeater_was_computed_before_any_call(self):
        finding = self.marks.program_findings["byte_identity"]
        self.assertTrue(finding["d1_not_exhibited"])
        self.assertTrue(finding["computed_before_any_call"])

    def test_d1_is_defeated_and_the_finding_rides_with_it(self):
        out = K.falsifiers(self.marks, None)
        self.assertTrue(out["D1"]["defeated"])
        self.assertTrue(out["D1"]["program_finding"]["d1_not_exhibited"])

    def test_the_defeat_stands_beside_the_marks_and_does_not_replace_them(self):
        out = K.falsifiers(self.marks, None)
        self.assertIn("carried", out["D1"])
        self.assertEqual(len(out["D1"]["carried"]), 3)
        self.assertIn("fired", out["D1"])

    def test_only_d1_can_be_defeated_by_byte_identity(self):
        out = K.falsifiers(self.marks, None)
        self.assertFalse(out["F2"]["defeated"])
        self.assertFalse(out["F3"]["defeated"])

    def test_findings_may_be_passed_in_explicitly(self):
        out = K.falsifiers(self.marks, self.marks.program_findings)
        self.assertTrue(out["D1"]["defeated"])

    def test_a_dict_of_marks_reads_the_same_as_the_record(self):
        out = K.falsifiers(self.marks.as_dict(), None)
        self.assertTrue(out["D1"]["defeated"])
        self.assertEqual(out["D1"]["comparison"], COMPARISON)


# --------------------------------------------------------------------------
# Registration, refusals and the module surface
# --------------------------------------------------------------------------


class MarksEnterTheGraphOneRegisterAtATime(MarkerCase):

    def setUp(self) -> None:
        super().setUp()
        self.cell = a_cell()
        self.seal = self.prepare(self.cell)

    def test_a_same_mark_registers_and_the_cell_reads(self):
        out = self.mark(self.cell, Scripted(default=mark_output(
            "same", case="the two sides read alike here")))
        row = out.row(COMPARISON, "D")
        self.assertEqual(row.mark, "same")
        self.assertTrue(row.registered)
        key = G.CellKey(cell=self.cell.cell_id, register="D", comparison=COMPARISON)
        self.assertEqual(G.cell_state(self.harness, key), G.READ)

    def test_the_mark_triples_the_decision_rule_compares_are_per_register(self):
        self.mark(self.cell, Scripted(default=mark_output("same")))
        triples = G.mark_triples(self.harness)
        registers = {register for _cell, register, _mark in triples}
        self.assertEqual(registers, set(K.REGISTERS))

    def test_a_cell_never_opened_is_named_before_any_call_is_spent(self):
        cell = a_cell("case-c")
        seal = self.sealed(cell)            # sealed, but no defaults opened
        factory = Scripted(default=mark_output())
        with self.assertRaises(K.MarkerRefused) as caught:
            self.mark(cell, factory, seal=seal, records=self.tmp / "marks-x")
        self.assertEqual(caught.exception.code, K.MARKER_INPUT_MALFORMED)
        self.assertEqual(factory.calls, [])

    def test_a_marks_record_is_written_write_once(self):
        out_dir = self.tmp / "cellmarks"
        self.mark(self.cell, Scripted(default=mark_output()), out_dir=out_dir)
        body = json.loads((out_dir / "marks.json").read_text())
        self.assertEqual(body["schema"], K.MARKER_SCHEMA)
        self.assertEqual(body["baseline_sha256"], self.seal)


class EveryRefusalIsNamedAndReachable(MarkerCase):

    def test_a_cell_that_is_not_a_markprep_cell_is_refused(self):
        with self.assertRaises(K.MarkerRefused) as caught:
            K.mark_cell(self.harness, {"cell": "x"}, "0" * 64, STD.STANDARD_BODY,
                        self.plan, self.config, records_dir=self.records)
        self.assertEqual(caught.exception.code, K.MARKER_INPUT_MALFORMED)

    def test_a_records_dir_is_required(self):
        cell = a_cell()
        seal = self.prepare(cell)
        with self.assertRaises(K.MarkerRefused) as caught:
            K.mark_cell(self.harness, cell, seal, STD.STANDARD_BODY, self.plan,
                        self.config)
        self.assertEqual(caught.exception.code, K.MARKER_INPUT_MALFORMED)

    def test_a_seat_plan_without_two_judge_seats_is_refused(self):
        cell = a_cell()
        seal = self.prepare(cell)
        with self.assertRaises(K.MarkerRefused) as caught:
            K.mark_cell(self.harness, cell, seal, STD.STANDARD_BODY, object(),
                        self.config, records_dir=self.records)
        self.assertEqual(caught.exception.code, K.MARKER_INPUT_MALFORMED)

    def test_marks_that_are_not_marks_are_refused_by_falsifiers(self):
        with self.assertRaises(K.MarkerRefused) as caught:
            K.falsifiers("marks", None)
        self.assertEqual(caught.exception.code, K.MARKER_INPUT_MALFORMED)

    def test_a_differs_without_a_kind_is_refused_by_the_row(self):
        with self.assertRaises(K.MarkerRefused) as caught:
            K.MarkRow(comparison=COMPARISON, left_case="ORIGINAL",
                      right_case="CONTROL", register="D", mark="differs",
                      difference_kind=None, source=K.TRIAL_SOURCE)
        self.assertEqual(caught.exception.code, K.MARKER_INPUT_MALFORMED)

    def test_a_kind_outside_the_registers_closed_set_is_refused(self):
        with self.assertRaises(K.MarkerRefused) as caught:
            K.MarkRow(comparison=COMPARISON, left_case="ORIGINAL",
                      right_case="CONTROL", register="D", mark="differs",
                      difference_kind="target_set_membership",
                      source=K.TRIAL_SOURCE)
        self.assertEqual(caught.exception.code, K.MARKER_INPUT_MALFORMED)

    def test_every_new_code_is_upper_snake_with_a_one_line_reason(self):
        for code, reason in K.NEW_CODES.items():
            self.assertRegex(code, r"^[A-Z][A-Z0-9_]*$")
            self.assertTrue(reason and "\n" not in reason)

    def test_every_new_code_is_folded_into_the_failure_table_only(self):
        for code in K.NEW_CODES:
            self.assertIn(code, loop_types.FAILURE_CODES)
            self.assertNotIn(code, loop_types.BLOCK_CODES)
            self.assertNotIn(code, loop_types.OUTCOME_CODES)

    def test_the_marker_error_is_a_loop_error(self):
        self.assertTrue(issubclass(K.MarkerRefused, loop_types.LoopError))


class TheModuleInventsNoShapeAndOpensNoSocket(unittest.TestCase):

    def test_the_registers_and_marks_are_the_standards_own(self):
        self.assertIs(K.REGISTERS, STD.REGISTER_IDS)
        self.assertIs(K.MARKS, STD.MARKS)
        self.assertEqual(sorted((K.DIFFERS, K.SAME, K.UNRESOLVED)),
                         sorted(C.MARKS))

    def test_the_module_imports_no_provider_module(self):
        source = MODULE.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
            elif isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
        self.assertNotIn("minireason.provider_openai_compat", imported)
        for name in imported:
            self.assertNotIn("socket", name)

    def test_the_only_sibling_edges_are_the_declared_ones(self):
        source = MODULE.read_text(encoding="utf-8")
        tree = ast.parse(source)
        siblings = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "minireason.loop":
                siblings.update(alias.name for alias in node.names)
        self.assertEqual(
            siblings,
            {"contracts", "custody", "graph", "markprep", "packs", "roles",
             "standard", "trial", "types"})

    def test_no_block_code_is_spelled_as_a_literal(self):
        source = MODULE.read_text(encoding="utf-8")
        body = source.split('"""', 2)[2]
        self.assertNotIn('"blocked:', body)
        self.assertNotIn("'blocked:", body)

    def test_the_module_names_no_token_the_stop_vocabulary_forbids(self):
        source = MODULE.read_text(encoding="utf-8").lower()
        self.assertNotIn("exhaustion", source)

    def test_the_falsifier_evaluation_orders_and_counts_nothing(self):
        """``falsifiers`` reads marks; it never ranks, sums or meters them."""
        import inspect
        tree = ast.parse(inspect.getsource(K.falsifiers))
        for node in ast.walk(tree):
            if isinstance(node, ast.Compare):
                for op in node.ops:
                    self.assertNotIsInstance(
                        op, (ast.Lt, ast.Gt, ast.LtE, ast.GtE),
                        "no mark, register or falsifier is ordered against another")
            if isinstance(node, ast.BinOp):
                self.assertNotIsInstance(
                    node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv),
                    "the falsifier evaluation computes no arithmetic")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertNotIn(node.func.id, {"sum", "max", "min", "sorted_by"})
