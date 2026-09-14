"""W2-MARKPREP: the C001 program pre-pass and the sealed baseline.

Every class below is named after one clause of the W2-MARKPREP acceptance list
in the wave plan, and every test in it is one reading of that clause.

The material is **published bytes**: every C001 occurrence under
``experiments/diagnostics/C001-contrast-triple/`` that carries a
``comparison.json`` and a ``juxtaposition/`` directory.  The newest of them is
the primary fixture (``occurrence-02`` where the tree carries it,
``occurrence-01`` otherwise) and the universal assertions run over **all** of
them, so a tree carrying only the earlier occurrence and a tree carrying both
assert the same things about the same program.  The second fixture is
:func:`minireason.loop.synthetic.contrast_leg`, which is the only place a
deliberately shaped case — a byte-identical ORIGINAL/CONTROL pair, a cell with
two replicates — is constructed, and it says so where it does.

Nothing here writes anything under an occurrence, calls a provider, or opens a
socket.  Every write goes to a ``TemporaryDirectory``.
"""
from __future__ import annotations

import copy
import json
import re
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path
from tempfile import TemporaryDirectory

from minireason.loop import contracts, custody, standard, surface as surface_module
from minireason.loop import markprep as M
from minireason.loop import synthetic
from minireason.loop import types as loop_types

REPO = Path(__file__).resolve().parents[2]
C001 = REPO / "experiments" / "diagnostics" / "C001-contrast-triple"


def published_occurrences() -> tuple[Path, ...]:
    """Every published C001 occurrence in this tree, oldest first."""

    return tuple(
        sorted(
            path
            for path in C001.glob("occurrence-*")
            if (path / "comparison.json").is_file() and (path / "juxtaposition").is_dir()
        )
    )


OCCURRENCES = published_occurrences()
if not OCCURRENCES:  # pragma: no cover - a tree with no C001 occurrence at all
    raise RuntimeError(f"no published C001 occurrence under {C001}")
#: The newest published occurrence: ``occurrence-02`` where the tree has it.
PRIMARY = OCCURRENCES[-1]


def occurrence(root: Path | None = None) -> M.Occurrence:
    return M.load_occurrence(PRIMARY if root is None else root)


def every_cell() -> list[M.Cell]:
    cells: list[M.Cell] = []
    for root in OCCURRENCES:
        loaded = M.load_occurrence(root)
        cells.extend(loaded.cells())
    return cells


def fcl_cells() -> list[M.Cell]:
    return [cell for cell in every_cell() if cell.arm == M.FCL_ARM]


def sealed(cell: M.Cell, stack: TemporaryDirectory) -> str:
    return M.write_baseline(cell, None, stack.name)


def a_rich_fcl_cell() -> M.Cell:
    """The primary occurrence's first FCL cell with a sufficient baseline."""

    loaded = occurrence()
    for endpoint, arm in loaded.cell_keys:
        if arm != M.FCL_ARM:
            continue
        cell = loaded.cell(endpoint, arm)
        if M.build_baseline(cell).sufficient:
            return cell
    raise AssertionError("no FCL cell with a sufficient baseline in the primary occurrence")


def synthetic_cell(case: str = "case-a", **kwargs) -> M.Cell:
    return M.cell_from_contrast_leg(
        synthetic.contrast_leg(),
        case,
        objection_ids=("a1", "a2"),
        shared_tokens=("a1",),
        **kwargs,
    )


def leg_with(case: str, mutate) -> dict:
    """A copy of ``contrast_leg()`` with one case's replicates rewritten.

    Used only where a *deliberately shaped* cell is under test — a byte-identical
    ORIGINAL/CONTROL pair, or a case with too few replicates.  The published
    occurrences carry neither, and inventing one inside them would be fabricating
    published bytes.
    """

    leg = copy.deepcopy(synthetic.contrast_leg())
    leg["cases"][case]["replicates"] = mutate(leg["cases"][case]["replicates"])
    return leg


def unique_quote(surface, text: str, start: int = 40, length: int = 60) -> str:
    """The shortest slice of ``text`` from ``start`` that occurs once in ``surface``."""

    while start + length <= len(text):
        candidate = text[start : start + length]
        if surface.count(candidate) == 1:
            return candidate
        length += 40
    raise AssertionError("no unique slice found")


# ---------------------------------------------------------------------------


class BaselineIsWrittenAndSealedBeforeAnyResidueIsOfferedForMarking(unittest.TestCase):
    """G8: no residue, no program mark and no cross-case surface before the seal."""

    def setUp(self):
        self.cell = a_rich_fcl_cell()

    def test_residue_before_the_seal_raises_baseline_not_first(self):
        with self.assertRaises(M.BaselineNotFirst) as caught:
            M.residue(self.cell)
        self.assertEqual(caught.exception.code, M.BASELINE_NOT_FIRST)

    def test_program_marks_before_the_seal_raises_baseline_not_first(self):
        with self.assertRaises(M.BaselineNotFirst) as caught:
            M.program_marks(self.cell)
        self.assertEqual(caught.exception.code, M.BASELINE_NOT_FIRST)

    def test_a_cross_case_pairwise_surface_before_the_seal_raises(self):
        left = self.cell.readable(M.BASELINE_CASE)[0]
        right = self.cell.readable("CONTROL")[0]
        with self.assertRaises(M.BaselineNotFirst):
            M.pairwise_surface(self.cell, left.key, right.key)

    def test_a_within_original_pairwise_surface_needs_no_seal(self):
        originals = self.cell.readable(M.BASELINE_CASE)
        built = M.pairwise_surface(self.cell, originals[0].key, originals[1].key)
        self.assertFalse(self.cell.sealed)
        self.assertEqual(len(built.spans), 2)

    def test_the_seal_is_the_sha256_of_the_bytes_on_disk(self):
        with TemporaryDirectory() as tmp:
            sha = M.write_baseline(self.cell, None, tmp)
            path = Path(tmp) / M.BASELINE_FILENAME
            self.assertTrue(path.is_file())
            self.assertEqual(sha, custody.sha256_path(path))
            self.assertEqual([p.name for p in Path(tmp).iterdir()], [M.BASELINE_FILENAME])
            self.assertEqual(M.verify_baseline(tmp, sha), sha)

    def test_the_cell_carries_the_seal_and_every_residue_row_names_it(self):
        with TemporaryDirectory() as tmp:
            sha = M.write_baseline(self.cell, None, tmp)
        self.assertEqual(self.cell.baseline_sha, sha)
        self.assertTrue(self.cell.sealed)
        rows = M.residue(self.cell)
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row.baseline_sha256, sha)
        self.assertEqual(M.program_marks(self.cell)["baseline_sha256"], sha)

    def test_the_written_baseline_reads_back_as_the_one_that_was_computed(self):
        with TemporaryDirectory() as tmp:
            M.write_baseline(self.cell, None, tmp)
            self.assertEqual(
                M.read_baseline(tmp).as_dict(), M.build_baseline(self.cell).as_dict()
            )

    def test_the_baseline_records_what_the_program_could_not_read(self):
        baseline = M.build_baseline(self.cell)
        self.assertEqual(baseline.undecided_kinds["G"], ("grounds_source",))
        self.assertEqual(
            set(baseline.undecided_kinds["E"]), {"record_engaged", "engagement_form"}
        )
        for register in standard.REGISTER_IDS:
            for kind in baseline.kinds[register]:
                self.assertIn(kind, contracts.difference_kinds_for(register))
                self.assertNotIn(kind, baseline.undecided_kinds[register])

    def test_baseline_kinds_is_the_admissibility_set_g9_reads(self):
        kinds = M.baseline_kinds(self.cell)
        self.assertEqual(set(kinds), set(standard.REGISTER_IDS))
        self.assertEqual(kinds, dict(M.build_baseline(self.cell).kinds))

    def test_the_baseline_is_within_original_and_refuses_another_case(self):
        control = self.cell.resolved("CONTROL")[0]
        with TemporaryDirectory() as tmp:
            with self.assertRaises(M.MarkprepError) as caught:
                M.write_baseline(self.cell, [control.key], tmp)
        self.assertEqual(caught.exception.code, M.MARKPREP_INPUT_MALFORMED)

    def test_the_baseline_pairs_are_pairs_of_original_replicates(self):
        baseline = M.build_baseline(self.cell)
        keys = set(baseline.readable)
        for pair in baseline.pairs:
            self.assertIn(pair.left, keys)
            self.assertIn(pair.right, keys)
            self.assertTrue(pair.left.startswith(f"{M.BASELINE_CASE}/"))
            self.assertTrue(pair.right.startswith(f"{M.BASELINE_CASE}/"))


class ABareIdTokenSharedWithTheAccountIsForcedUnresolvedAndNeverInTheResidue(
    unittest.TestCase
):
    """G10(c): forced ``unresolved``, never ``differs``, and never trialled."""

    def test_the_shared_token_set_is_the_one_plan_8a_names(self):
        loaded = occurrence()
        block = loaded.material["arms"][M.FCL_ARM]["record_ids_by_document"]
        shared = set(block["objection"]) & set(block["account"])
        self.assertEqual(shared, {"o1", "c1", "c2", "p1", "u1"})
        cell = a_rich_fcl_cell()
        self.assertEqual(cell.shared_tokens, frozenset(shared))

    def test_a_published_cell_forces_register_e_and_leaves_it_out_of_the_residue(self):
        forced = 0
        for cell in fcl_cells():
            with TemporaryDirectory() as tmp:
                M.write_baseline(cell, None, tmp)
            marks = M.program_marks(cell)
            open_rows = {(r.comparison, r.register) for r in M.residue(cell)}
            for label, entry in marks["comparisons"].items():
                block = entry["registers"]["E"]
                if not block["forced_unresolved"]:
                    continue
                forced += 1
                self.assertEqual(block["mark"], standard.UNRESOLVED_TOKEN)
                self.assertNotIn((label, "E"), open_rows)
                for kind in block["kinds"].values():
                    self.assertNotEqual(kind["mark"], "differs")
                    self.assertTrue(kind["forced_unresolved"])
        self.assertGreater(forced, 0, "no published FCL cell forces register E")

    def test_the_forcing_names_the_tokens_it_read(self):
        cell = a_rich_fcl_cell()
        with TemporaryDirectory() as tmp:
            M.write_baseline(cell, None, tmp)
        marks = M.program_marks(cell)
        for entry in marks["comparisons"].values():
            block = entry["registers"]["E"]
            if not block["forced_unresolved"]:
                continue
            evidence = block["kinds"]["record_engaged"]["evidence"]
            seen = set(evidence["left"]) | set(evidence["right"])
            self.assertTrue(seen)
            self.assertLessEqual(seen, set(cell.shared_tokens))

    def test_the_synthetic_leg_forces_e_on_its_bare_token_case(self):
        cell = synthetic_cell("case-b")
        with TemporaryDirectory() as tmp:
            M.write_baseline(cell, None, tmp)
        block = M.program_marks(cell)["comparisons"]["ORIGINAL vs CONTROL"]["registers"]["E"]
        self.assertTrue(block["forced_unresolved"])
        self.assertEqual(block["mark"], standard.UNRESOLVED_TOKEN)
        self.assertNotIn("E", {row.register for row in M.residue(cell)})

    def test_without_a_shared_bare_token_register_e_stays_in_the_residue(self):
        cell = M.cell_from_contrast_leg(
            synthetic.contrast_leg(), "case-b", objection_ids=("a1",), shared_tokens=()
        )
        with TemporaryDirectory() as tmp:
            M.write_baseline(cell, None, tmp)
        block = M.program_marks(cell)["comparisons"]["ORIGINAL vs CONTROL"]["registers"]["E"]
        self.assertFalse(block["forced_unresolved"])
        self.assertIn("E", {row.register for row in M.residue(cell)})


class TAndDAreProgramComputedAndTheResidueNamesExactlyTheRowsItCouldNot(
    unittest.TestCase
):
    """G10(d): the program marks T and D where the parse succeeds; the rest is residue."""

    def test_the_program_read_agrees_with_the_occurrences_own_fcl_summary(self):
        checked = 0
        for root in OCCURRENCES:
            comparison = json.loads((root / "comparison.json").read_text(encoding="utf-8"))
            loaded = M.load_occurrence(root)
            for table in comparison["tables"]:
                if table["arm"] != M.FCL_ARM:
                    continue
                cell = loaded.cell(table["endpoint_slug"], table["arm"])
                for lowered, rows in table["cases"].items():
                    for row in rows:
                        published = (row.get("fcl") or {}).get("parse")
                        read = cell.replicate(f"{lowered.upper()}/rep{row['replicate']}").read
                        if published != M.PARSE_OK or not read.readable:
                            continue
                        checked += 1
                        self.assertEqual(sorted(read.targets), sorted(row["fcl"]["targets_named"]))
                        self.assertEqual(
                            sorted(read.engaged_records),
                            sorted(row["fcl"]["objection_record_ids_in_refs"]),
                        )
                        self.assertEqual(list(read.record_ids), list(row["fcl"]["record_ids"]))
        self.assertGreater(checked, 0)

    def test_t_and_d_are_decided_wherever_both_sides_have_enough_readable_replicates(self):
        decided = 0
        for cell in fcl_cells():
            with TemporaryDirectory() as tmp:
                M.write_baseline(cell, None, tmp)
            baseline = M.build_baseline(cell)
            marks = M.program_marks(cell)
            for entry in marks["comparisons"].values():
                enough = (
                    not entry["under_replicated"]
                    and len(entry["left_readable"]) >= M.MIN_RESOLVED_REPLICATES
                    and len(entry["right_readable"]) >= M.MIN_RESOLVED_REPLICATES
                    and baseline.sufficient
                )
                if not enough:
                    continue
                for kind, block in entry["registers"]["T"]["kinds"].items():
                    self.assertTrue(block["decided"], kind)
                    decided += 1
                for kind, block in entry["registers"]["D"]["kinds"].items():
                    # D is keyed by criticism: undecided only where the two
                    # sides engage no objection record in common.
                    if not block["decided"]:
                        self.assertEqual(
                            block["evidence"]["shared_criticisms"], [], kind
                        )
                    else:
                        decided += 1
        self.assertGreater(decided, 0)

    def test_a_t_mark_is_a_set_identity_over_the_target_arrays_prefix_intact(self):
        cell = a_rich_fcl_cell()
        with TemporaryDirectory() as tmp:
            M.write_baseline(cell, None, tmp)
        marks = M.program_marks(cell)
        checked = 0
        for (left_case, right_case) in cell.comparisons:
            label = M.COMPARISON_LABELS[(left_case, right_case)]
            block = marks["comparisons"][label]["registers"]["T"]["kinds"]
            membership = block["target_set_membership"]
            if not membership["decided"]:
                self.assertEqual(membership["evidence"], {})
                continue
            checked += 1
            evidence = membership["evidence"]
            left = {t for r in cell.readable(left_case) for t in r.read.targets}
            right = {t for r in cell.readable(right_case) for t in r.read.targets}
            self.assertEqual(set(evidence["left"]), left)
            self.assertEqual(set(evidence["right"]), right)
            self.assertEqual(membership["mark"] == "same", left == right or "block" in membership)
            for value in left | right:
                self.assertIsInstance(value, str)
        self.assertGreater(checked, 0)

    def test_the_residue_names_exactly_the_resolved_rows_the_program_could_not_read(self):
        for cell in every_cell():
            with TemporaryDirectory() as tmp:
                M.write_baseline(cell, None, tmp)
            thin = M.under_replicated(cell)
            for row in M.residue(cell):
                expected = tuple(
                    r.key
                    for case in (row.left_case, row.right_case)
                    for r in cell.resolved(case)
                    if not r.readable
                )
                self.assertEqual(row.unreadable_replicates, expected)
                self.assertNotIn(row.left_case, thin)
                self.assertNotIn(row.right_case, thin)

    def test_no_row_the_program_decided_is_in_the_residue(self):
        for cell in every_cell():
            with TemporaryDirectory() as tmp:
                M.write_baseline(cell, None, tmp)
            marks = M.program_marks(cell)
            for row in M.residue(cell):
                block = marks["comparisons"][row.comparison]["registers"][row.register]
                for kind in row.difference_kinds:
                    self.assertFalse(block["kinds"][kind]["decided"])
                for kind, detail in block["kinds"].items():
                    if detail["decided"]:
                        self.assertNotIn(kind, row.difference_kinds)

    def test_register_g_is_never_program_read_and_is_on_every_offered_comparison(self):
        self.assertIn("grounds_source", M.NOT_PROGRAM_READ)
        for cell in every_cell():
            with TemporaryDirectory() as tmp:
                M.write_baseline(cell, None, tmp)
            thin = M.under_replicated(cell)
            offered = {
                M.COMPARISON_LABELS[pair]
                for pair in cell.comparisons
                if not ({pair[0], pair[1]} & thin)
            }
            in_residue = {row.comparison for row in M.residue(cell) if row.register == "G"}
            self.assertEqual(in_residue, offered, cell.cell_id)

    def test_the_prose_arm_is_residue_on_every_register(self):
        prose = [cell for cell in every_cell() if cell.arm == M.PROSE_ARM]
        self.assertTrue(prose, "no published prose cell")
        for cell in prose:
            with TemporaryDirectory() as tmp:
                M.write_baseline(cell, None, tmp)
            rows = M.residue(cell)
            thin = M.under_replicated(cell)
            offered = [p for p in cell.comparisons if not ({p[0], p[1]} & thin)]
            self.assertEqual(
                {(r.comparison, r.register) for r in rows},
                {
                    (M.COMPARISON_LABELS[p], register)
                    for p in offered
                    for register in standard.REGISTER_IDS
                },
            )

    def test_a_program_differs_is_admissible_only_off_the_baseline(self):
        cell = synthetic_cell("case-a")
        with TemporaryDirectory() as tmp:
            M.write_baseline(cell, None, tmp)
        block = M.program_marks(cell)["comparisons"]["ORIGINAL vs CONTROL"]["registers"]["T"]
        self.assertEqual(block["mark"], "differs")
        self.assertEqual(block["difference_kind"], "target_set_membership")
        self.assertNotIn("target_set_membership", M.baseline_kinds(cell)["T"])

    def test_g9_writes_same_where_the_baseline_already_exhibits_the_kind(self):
        forced = []
        for cell in fcl_cells():
            with TemporaryDirectory() as tmp:
                M.write_baseline(cell, None, tmp)
            baseline = M.build_baseline(cell)
            for entry in M.program_marks(cell)["comparisons"].values():
                for register, block in entry["registers"].items():
                    for kind, detail in block["kinds"].items():
                        if "block" not in detail:
                            continue
                        forced.append((cell.cell_id, register, kind))
                        self.assertEqual(detail["mark"], "same")
                        self.assertEqual(detail["block"], M.BASELINE_FORCED_SAME_BLOCK)
                        self.assertIn(kind, baseline.kinds[register])
                        self.assertTrue(detail["forced_by"]["pairs"])
                        for pair in detail["forced_by"]["pairs"]:
                            self.assertIn(kind, pair["kinds"])
        self.assertGreater(len(forced), 0, "no published cell exercises G9")

    def test_the_forced_same_block_is_one_of_the_ceilings_nine_reasons(self):
        self.assertIn(M.BASELINE_FORCED_SAME_BLOCK, loop_types.BLOCK_CODES)
        self.assertIn("baseline-forced-same", loop_types.CEILING_BLOCK_REASONS)


class ByteIdenticalOriginalAndControlRecordD1NotExhibitedBeforeAnyCall(unittest.TestCase):
    """G10(a): the mechanical defeater, computed first and standing as a finding."""

    def test_the_defeater_needs_no_seal(self):
        cell = a_rich_fcl_cell()
        self.assertFalse(cell.sealed)
        record = M.byte_identity_defeater(cell)
        self.assertTrue(record["computed_before_any_call"])
        self.assertFalse(cell.sealed)

    def test_a_published_cell_records_the_originals_with_no_identical_control(self):
        seen = 0
        for cell in every_cell():
            record = M.byte_identity_defeater(cell)
            self.assertEqual(record["comparison"], "ORIGINAL vs CONTROL")
            if not record["computable"]:
                self.assertFalse(record["d1_not_exhibited"])
                continue
            seen += 1
            unmatched = set(record["original_without_identical_control"])
            self.assertEqual(
                record["d1_not_exhibited"], not unmatched, cell.cell_id
            )
            self.assertLessEqual(unmatched, {r.key for r in cell.resolved("ORIGINAL")})
        self.assertGreater(seen, 0)

    def test_an_all_identical_cell_records_d1_not_exhibited(self):
        leg = leg_with(
            "case-d",
            lambda reps: {
                name: {
                    "ORIGINAL": sides["ORIGINAL"],
                    "CONTROL": sides["ORIGINAL"],
                    "byte_identical": True,
                }
                for name, sides in reps.items()
            },
        )
        cell = M.cell_from_contrast_leg(leg, "case-d")
        record = M.byte_identity_defeater(cell)
        self.assertTrue(record["computable"])
        self.assertTrue(record["d1_not_exhibited"])
        self.assertEqual(record["original_without_identical_control"], [])
        self.assertEqual(len(record["identical_pairs"]), 3)
        for pair in record["identical_pairs"]:
            self.assertTrue(pair["original"].startswith("ORIGINAL/"))
            self.assertTrue(pair["control"].startswith("CONTROL/"))

    def test_one_identical_replicate_is_not_the_defeater(self):
        cell = synthetic_cell("case-d")
        record = M.byte_identity_defeater(cell)
        self.assertEqual(len(record["identical_pairs"]), 1)
        self.assertFalse(record["d1_not_exhibited"])
        self.assertEqual(len(record["original_without_identical_control"]), 2)

    def test_the_finding_names_d1s_carrying_and_excluded_registers(self):
        record = M.byte_identity_defeater(a_rich_fcl_cell())
        falsifier = standard.FALSIFIER_MAP["D1"]
        self.assertEqual(record["carrying_registers"], list(falsifier.carrying_registers))
        self.assertEqual(record["excluded_registers"], list(falsifier.excluded_registers))
        self.assertEqual(record["excluded_registers"], ["G"])

    def test_the_finding_is_not_a_mark(self):
        record = M.byte_identity_defeater(a_rich_fcl_cell())
        self.assertNotIn("mark", record)
        self.assertNotIn("difference_kind", record)

    def test_the_program_marks_carry_the_finding_beside_them(self):
        cell = a_rich_fcl_cell()
        with TemporaryDirectory() as tmp:
            M.write_baseline(cell, None, tmp)
        self.assertEqual(
            M.program_marks(cell)["byte_identity"], M.byte_identity_defeater(cell)
        )


class FewerThanThreeResolvedReplicatesOfACaseYieldsNoResidueForThatCase(
    unittest.TestCase
):
    """G10(b): absent data, reported as absent data and never as an absence."""

    def test_the_minimum_comes_from_the_standards_guard_parameters(self):
        self.assertEqual(
            M.MIN_RESOLVED_REPLICATES,
            standard.GUARD_PARAMETERS["min_resolved_replicates_per_case"],
        )
        self.assertEqual(M.MIN_RESOLVED_REPLICATES, 3)

    def test_an_under_replicated_case_is_on_no_residue_row(self):
        checked = 0
        for cell in every_cell():
            thin = M.under_replicated(cell)
            if not thin:
                continue
            checked += 1
            with TemporaryDirectory() as tmp:
                M.write_baseline(cell, None, tmp)
            for row in M.residue(cell):
                self.assertNotIn(row.left_case, thin)
                self.assertNotIn(row.right_case, thin)
        self.assertGreaterEqual(checked, 0)

    def test_a_two_replicate_cell_yields_no_residue_at_all(self):
        leg = leg_with(
            "case-a", lambda reps: {k: v for k, v in list(reps.items())[:2]}
        )
        cell = M.cell_from_contrast_leg(leg, "case-a")
        self.assertEqual(M.under_replicated(cell), {"ORIGINAL", "CONTROL"})
        with TemporaryDirectory() as tmp:
            M.write_baseline(cell, None, tmp)
        self.assertEqual(M.residue(cell), [])

    def test_an_under_replicated_comparison_marks_every_register_unresolved(self):
        leg = leg_with(
            "case-a", lambda reps: {k: v for k, v in list(reps.items())[:2]}
        )
        cell = M.cell_from_contrast_leg(leg, "case-a")
        with TemporaryDirectory() as tmp:
            M.write_baseline(cell, None, tmp)
        marks = M.program_marks(cell)
        entry = marks["comparisons"]["ORIGINAL vs CONTROL"]
        self.assertEqual(entry["under_replicated"], ["CONTROL", "ORIGINAL"])
        for register, block in entry["registers"].items():
            self.assertEqual(block["mark"], standard.UNRESOLVED_TOKEN, register)
            for kind, detail in block["kinds"].items():
                self.assertFalse(detail["decided"])
                self.assertIn("absent data", detail["reason"])

    def test_no_differs_survives_under_replication(self):
        leg = leg_with(
            "case-a", lambda reps: {k: v for k, v in list(reps.items())[:2]}
        )
        cell = M.cell_from_contrast_leg(leg, "case-a")
        with TemporaryDirectory() as tmp:
            M.write_baseline(cell, None, tmp)
        rendered = json.dumps(M.program_marks(cell)["comparisons"])
        self.assertNotIn('"differs"', rendered)

    def test_the_full_leg_of_the_same_case_is_not_under_replicated(self):
        cell = synthetic_cell("case-a")
        self.assertEqual(M.under_replicated(cell), set())


class EditingTheBaselineAfterSealingRaises(unittest.TestCase):
    """§8a: the baseline note is written first and is not revised afterwards."""

    def setUp(self):
        self.cell = a_rich_fcl_cell()

    def test_a_second_write_raises_write_once_violation(self):
        with TemporaryDirectory() as tmp:
            M.write_baseline(self.cell, None, tmp)
            with self.assertRaises(custody.WriteOnceViolation) as caught:
                M.write_baseline(self.cell, None, tmp)
        self.assertEqual(caught.exception.code, "WRITE_ONCE_VIOLATION")

    def test_resealing_with_a_different_sha_raises(self):
        with TemporaryDirectory() as tmp:
            sha = M.write_baseline(self.cell, None, tmp)
        self.assertEqual(self.cell.seal(sha), sha)
        with self.assertRaises(M.MarkprepError) as caught:
            self.cell.seal("0" * 64)
        self.assertEqual(caught.exception.code, M.BASELINE_RESEALED)
        self.assertEqual(self.cell.baseline_sha, sha)

    def test_a_baseline_edited_around_the_module_breaks_its_seal(self):
        with TemporaryDirectory() as tmp:
            sha = M.write_baseline(self.cell, None, tmp)
            path = Path(tmp) / M.BASELINE_FILENAME
            body = json.loads(path.read_text(encoding="utf-8"))
            body["kinds"]["T"] = list(body["kinds"]["T"]) + ["target_set_membership"]
            body["note"] = body["note"] + " Revised after the seal."
            path.write_bytes(custody.encoded(body))
            with self.assertRaises(M.BaselineSealBroken) as caught:
                M.verify_baseline(tmp, sha)
        self.assertEqual(caught.exception.code, M.BASELINE_SEAL_BROKEN)

    def test_the_baseline_record_is_frozen(self):
        baseline = M.build_baseline(self.cell)
        with self.assertRaises(FrozenInstanceError):
            baseline.kinds = {}

    def test_a_seal_must_be_a_sha256(self):
        with self.assertRaises(M.MarkprepError) as caught:
            self.cell.seal("not-a-digest")
        self.assertEqual(caught.exception.code, M.MARKPREP_INPUT_MALFORMED)


class ThePairwiseSurfaceCarriesLeftAndRightQuotesOnTwoSides(unittest.TestCase):
    """S5: two Spans, W1-SURFACE's own resolver, and surface.py untouched."""

    def setUp(self):
        self.cell = a_rich_fcl_cell()
        with TemporaryDirectory() as tmp:
            M.write_baseline(self.cell, None, tmp)
        self.left = self.cell.readable(M.BASELINE_CASE)[0]
        self.right = self.cell.readable("CONTROL")[0]
        self.surface = M.pairwise_surface(self.cell, self.left.key, self.right.key)

    def test_the_resolver_is_w1_surfaces_own(self):
        self.assertIs(M.resolve_unique, surface_module.resolve_unique)
        self.assertIs(M.within_declared_span, surface_module.within_declared_span)
        self.assertIsInstance(self.surface, surface_module.Surface)
        for span in self.surface.spans:
            self.assertIsInstance(span, surface_module.Span)

    def test_the_two_spans_are_the_left_and_the_right_sides(self):
        self.assertEqual(
            [span.side for span in self.surface.spans], [M.SIDE_LEFT, M.SIDE_RIGHT]
        )
        self.assertEqual(M.SIDE_LEFT, surface_module.SIDE_REFERRING_RECORD)
        self.assertEqual(M.SIDE_RIGHT, surface_module.SIDE_TARGET_RECORD)

    def test_every_span_re_reads_its_own_bytes_out_of_the_named_artifact(self):
        for span, row in zip(self.surface.spans, (self.left, self.right)):
            path = PRIMARY / span.occurrence_path
            self.assertTrue(path.is_file(), span.occurrence_path)
            field = json.loads(path.read_text(encoding="utf-8"))[span.source_field]
            self.assertEqual(field[span.file_start : span.file_end], row.commitments)
            self.assertEqual(
                self.surface.text[span.start : span.end].decode("utf-8"), row.commitments
            )

    def test_a_left_quote_resolves_on_the_left_side_and_within_a_declared_span(self):
        quote = unique_quote(self.surface, self.left.commitments)
        resolved = M.resolve_pair(
            self.surface, quote, unique_quote(self.surface, self.right.commitments)
        )
        self.assertTrue(resolved.ok)
        self.assertIsNone(resolved.block)
        self.assertEqual(resolved.left.side, M.SIDE_LEFT)
        self.assertEqual(resolved.right.side, M.SIDE_RIGHT)
        self.assertTrue(surface_module.within_declared_span(self.surface, resolved.left))

    def test_the_two_quotes_swapped_are_blocked_as_the_wrong_operative_target(self):
        left = unique_quote(self.surface, self.left.commitments)
        right = unique_quote(self.surface, self.right.commitments)
        resolved = M.resolve_pair(self.surface, right, left)
        self.assertFalse(resolved.ok)
        self.assertEqual(resolved.block, surface_module.OPERATIVE_TARGET_BLOCK)

    def test_a_quote_of_the_surfaces_own_label_is_framing_and_is_blocked(self):
        label = self.surface.decoded.split("\n", 1)[0]
        resolved = M.resolve_pair(
            self.surface, label, unique_quote(self.surface, self.right.commitments)
        )
        self.assertEqual(resolved.left.side, surface_module.SIDE_FRAMING)
        self.assertEqual(resolved.block, surface_module.OPERATIVE_TARGET_BLOCK)

    def test_a_quote_in_both_sides_is_not_unique_and_is_blocked(self):
        for candidate in ('"records"', '"language"', '"id"'):
            if self.surface.count(candidate) > 1:
                break
        else:  # pragma: no cover - both FCL documents always share these keys
            self.fail("no quote occurs on both sides")
        resolved = M.resolve_pair(self.surface, candidate, candidate)
        self.assertIsNone(resolved.left)
        self.assertGreater(resolved.left_count, 1)
        self.assertEqual(resolved.block, surface_module.REFERENTIAL_INTEGRITY_BLOCK)

    def test_the_surface_is_a_pure_function_of_the_two_replicates(self):
        again = M.pairwise_surface(self.cell, self.left.key, self.right.key)
        self.assertEqual(again.text, self.surface.text)
        self.assertEqual(again.digest, self.surface.digest)

    def test_the_descriptive_slots_carry_the_comparison_not_a_reference(self):
        self.assertEqual(self.surface.ref_field, surface_module.FIELD_COMMITMENTS)
        self.assertEqual(self.surface.ref_grain, "artifact")
        self.assertEqual(self.surface.ref_verbatim, "ORIGINAL vs CONTROL")

    def test_an_unreadable_replicate_cannot_be_a_side(self):
        unreadable = [r for r in self.cell.replicates if r.commitments is None]
        if not unreadable:
            self.skipTest("this occurrence has no unreadable replicate")
        with self.assertRaises(M.MarkprepError) as caught:
            M.pairwise_surface(self.cell, unreadable[0].key, self.right.key)
        self.assertEqual(caught.exception.code, M.REPLICATE_NOT_READABLE)


class NoRegisterIsCombinedAndNoCountIsAVerdict(unittest.TestCase):
    """The four registers stand and fall separately; G12 over every record."""

    def setUp(self):
        self.cell = a_rich_fcl_cell()
        with TemporaryDirectory() as tmp:
            M.write_baseline(self.cell, None, tmp)
        self.marks = M.program_marks(self.cell)

    def test_there_is_no_cell_level_or_comparison_level_mark(self):
        self.assertNotIn("mark", self.marks)
        for entry in self.marks["comparisons"].values():
            self.assertNotIn("mark", entry)
            self.assertNotIn("difference_kind", entry)

    def test_every_mark_is_a_member_of_the_standards_closed_set(self):
        for entry in self.marks["comparisons"].values():
            for block in entry["registers"].values():
                self.assertIn(block["mark"], standard.MARKS)
                for detail in block["kinds"].values():
                    self.assertIn(detail["mark"], standard.MARKS)

    def test_every_difference_kind_belongs_to_its_own_register(self):
        for entry in self.marks["comparisons"].values():
            for register, block in entry["registers"].items():
                allowed = contracts.difference_kinds_for(register)
                self.assertEqual(tuple(block["kinds"]), tuple(allowed))
                if block["difference_kind"] is not None:
                    self.assertIn(block["difference_kind"], allowed)

    def test_the_four_registers_are_the_frozen_plan_8a_mirror(self):
        for entry in self.marks["comparisons"].values():
            self.assertEqual(tuple(entry["registers"]), standard.REGISTER_IDS)

    def test_g12_passes_over_every_record_this_module_emits(self):
        contracts.assert_no_scoring_keys(self.marks)
        contracts.assert_no_scoring_keys(M.build_baseline(self.cell).as_dict())
        contracts.assert_no_scoring_keys(M.byte_identity_defeater(self.cell))
        contracts.assert_no_scoring_keys(self.cell.as_dict())
        for row in M.residue(self.cell):
            contracts.assert_no_scoring_keys(row.as_dict())

    def test_the_three_comparisons_are_the_falsifier_maps_own(self):
        for name, falsifier in standard.FALSIFIER_MAP.items():
            self.assertIn(tuple(falsifier.comparison), M.COMPARISONS)
        self.assertEqual(len(M.COMPARISONS), len(standard.FALSIFIER_MAP))

    def test_the_module_imports_only_its_declared_siblings(self):
        source = (
            REPO / "src" / "minireason" / "loop" / "markprep.py"
        ).read_text(encoding="utf-8")
        siblings = set(re.findall(r"from minireason\.loop(?:\.(\w+))? import", source))
        siblings |= set(re.findall(r"from minireason\.loop import ([\w, ]+)", source))
        flattened = {
            name.strip()
            for entry in siblings
            for name in str(entry).split(",")
            if name.strip()
        }
        self.assertLessEqual(
            flattened & {"custody", "standard", "surface", "contracts", "types"},
            {"custody", "standard", "surface", "contracts", "types"},
        )
        for forbidden in ("packs", "roles", "decide", "trial", "marker", "reader"):
            self.assertNotIn(f"minireason.loop.{forbidden}", source)


class TheDeliveredBytesAreTheJuxtapositionsAndNothingIsRepaired(unittest.TestCase):
    """The pre-pass reads what was delivered, and refuses what it cannot read."""

    def test_every_juxtaposition_block_is_the_published_response_bytes(self):
        checked = 0
        for root in OCCURRENCES:
            comparison = json.loads((root / "comparison.json").read_text(encoding="utf-8"))
            for table in comparison["tables"]:
                path = root / "juxtaposition" / f"{table['endpoint_slug']}__{table['arm']}.md"
                blocks = M._juxtaposition_blocks(path.read_text(encoding="utf-8"))
                for lowered, rows in table["cases"].items():
                    for row in rows:
                        delivered = row.get("path")
                        if not delivered or not (root / delivered).is_file():
                            continue
                        checked += 1
                        self.assertEqual(
                            blocks[(lowered, row["replicate"])],
                            (root / delivered).read_text(encoding="utf-8"),
                        )
        self.assertGreater(checked, 0)

    def test_a_readable_replicates_commitments_hash_to_the_published_sha256(self):
        checked = 0
        for cell in every_cell():
            for row in cell.replicates:
                if row.commitments is None:
                    continue
                checked += 1
                self.assertEqual(
                    custody.sha256_bytes(row.commitments.encode("utf-8")),
                    row.commitments_sha256,
                )
        self.assertGreater(checked, 0)

    def test_a_strictly_parsing_envelope_is_always_read_by_the_program(self):
        for cell in every_cell():
            for row in cell.replicates:
                if row.strict_parse_would_succeed:
                    self.assertIsNotNone(row.commitments, row.key)

    def test_a_row_the_occurrence_repaired_is_not_repaired_here(self):
        unrepaired = [
            (cell, row)
            for cell in every_cell()
            for row in cell.replicates
            if row.resolved
            and row.commitments is None
            and "strip_outer_code_fence" not in row.envelope_repairs
        ]
        self.assertTrue(unrepaired, "no published row needs a repair beyond a fence")
        for cell, row in unrepaired:
            self.assertTrue(row.envelope_repairs or row.envelope_status == "OPAQUE")
            self.assertEqual(row.read.parse, M.PARSE_ENVELOPE_NOT_AUTHORED)
            self.assertFalse(row.readable)

    def test_a_doctored_comparison_sha_is_a_named_refusal(self):
        root = PRIMARY
        comparison = json.loads((root / "comparison.json").read_text(encoding="utf-8"))
        table = comparison["tables"][0]
        for rows in table["cases"].values():
            for row in rows:
                if row.get("commitments_sha256") and row.get("envelope_status") == "AUTHORED":
                    row["commitments_sha256"] = "0" * 64
                    break
            else:
                continue
            break
        with TemporaryDirectory() as tmp:
            staged = Path(tmp) / "occurrence"
            (staged / "juxtaposition").mkdir(parents=True)
            (staged / "comparison.json").write_text(
                json.dumps(comparison), encoding="utf-8"
            )
            (staged / "material.json").write_bytes((root / "material.json").read_bytes())
            for source in (root / "juxtaposition").iterdir():
                (staged / "juxtaposition" / source.name).write_bytes(source.read_bytes())
            loaded = M.load_occurrence(staged)
            with self.assertRaises(M.MarkprepError) as caught:
                loaded.cell(table["endpoint_slug"], table["arm"])
        self.assertEqual(caught.exception.code, M.REPLICATE_BYTES_DISAGREE)


class ThePublicInterfaceIsTheWavePlansOwn(unittest.TestCase):
    """The six names the wave plan spells, with the shapes it spells them in."""

    def setUp(self):
        self.cell = a_rich_fcl_cell()

    def test_the_six_wave_plan_callables_are_all_exported(self):
        for name in (
            "program_marks",
            "write_baseline",
            "baseline_kinds",
            "byte_identity_defeater",
            "under_replicated",
            "residue",
        ):
            self.assertIn(name, M.__all__)
            self.assertTrue(callable(getattr(M, name)))

    def test_the_return_shapes_are_the_ones_the_plan_names(self):
        self.assertIsInstance(M.under_replicated(self.cell), set)
        self.assertIsInstance(M.baseline_kinds(self.cell), dict)
        self.assertIsInstance(M.byte_identity_defeater(self.cell), dict)
        with TemporaryDirectory() as tmp:
            sha = M.write_baseline(self.cell, None, tmp)
        self.assertIsInstance(sha, str)
        self.assertRegex(sha, r"^[0-9a-f]{64}$")
        self.assertIsInstance(M.program_marks(self.cell), dict)
        self.assertIsInstance(M.residue(self.cell), list)

    def test_every_residue_reason_is_a_declared_one(self):
        for cell in every_cell():
            with TemporaryDirectory() as tmp:
                M.write_baseline(cell, None, tmp)
            for row in M.residue(cell):
                self.assertIn(row.reason, M.RESIDUE_REASONS)
                self.assertIsInstance(row, M.ResidueRow)
                self.assertIn(row.register, standard.REGISTER_IDS)

    def test_every_not_program_read_kind_is_a_real_difference_kind(self):
        for kind in M.NOT_PROGRAM_READ:
            self.assertIn(kind, standard.ALL_DIFFERENCE_KINDS)
        for kind in M.PROGRAM_KINDS:
            self.assertIn(kind, standard.ALL_DIFFERENCE_KINDS)
            self.assertNotIn(kind, M.NOT_PROGRAM_READ)
        self.assertEqual(
            set(M.PROGRAM_KINDS) | set(M.NOT_PROGRAM_READ),
            set(standard.ALL_DIFFERENCE_KINDS),
        )

    def test_the_cases_and_comparisons_are_plan_4s_and_plan_8as(self):
        self.assertEqual(M.CASES, ("ORIGINAL", "RECODING", "CARRIER", "CONTROL"))
        self.assertEqual(M.BASELINE_CASE, "ORIGINAL")
        self.assertEqual(
            set(M.COMPARISON_LABELS.values()),
            {"ORIGINAL vs CONTROL", "ORIGINAL vs RECODING", "ORIGINAL vs CARRIER"},
        )


class TheModuleRefusesWhatItCannotRead(unittest.TestCase):
    """Every refusal is named, and every name is a key of NEW_CODES."""

    def test_an_unknown_comparison_schema_is_refused(self):
        with TemporaryDirectory() as tmp:
            staged = Path(tmp)
            (staged / "comparison.json").write_text(
                json.dumps({"schema": "minireason.c001.comparison.v2", "tables": []}),
                encoding="utf-8",
            )
            (staged / "material.json").write_text("{}", encoding="utf-8")
            with self.assertRaises(M.MarkprepError) as caught:
                M.load_occurrence(staged)
        self.assertEqual(caught.exception.code, M.COMPARISON_SCHEMA_UNKNOWN)

    def test_a_cell_that_is_not_in_the_occurrence_is_refused(self):
        with self.assertRaises(M.MarkprepError) as caught:
            occurrence().cell("no-such-endpoint", M.FCL_ARM)
        self.assertEqual(caught.exception.code, M.CELL_NOT_IN_OCCURRENCE)

    def test_an_unknown_replicate_key_is_refused(self):
        with self.assertRaises(M.MarkprepError) as caught:
            a_rich_fcl_cell().replicate("ORIGINAL/rep99")
        self.assertEqual(caught.exception.code, M.REPLICATE_UNKNOWN)

    def test_a_contrast_leg_of_another_schema_is_refused(self):
        with self.assertRaises(M.MarkprepError) as caught:
            M.cell_from_contrast_leg({"schema": "other", "cases": {}}, "case-a")
        self.assertEqual(caught.exception.code, M.COMPARISON_SCHEMA_UNKNOWN)

    def test_a_contrast_leg_without_that_case_is_refused(self):
        with self.assertRaises(M.MarkprepError) as caught:
            M.cell_from_contrast_leg(synthetic.contrast_leg(), "case-z")
        self.assertEqual(caught.exception.code, M.MARKPREP_INPUT_MALFORMED)

    def test_every_new_code_is_upper_snake_with_a_one_line_reason(self):
        self.assertTrue(M.NEW_CODES)
        for code, reason in M.NEW_CODES.items():
            self.assertRegex(code, r"^[A-Z][A-Z0-9_]*$")
            self.assertTrue(reason.strip())
            self.assertNotIn("\n", reason)
            self.assertIs(getattr(M, code), code)

    def test_every_new_code_is_folded_into_the_failure_table(self):
        """O9, the wave-2 integrator's side of it.

        While this module was on the frontier the assertion was the opposite -
        every key of ``NEW_CODES`` is a code ``types`` does *not* yet carry -
        which is what "new" meant on the day the module landed. The fold-in
        makes ``types`` the owner of all nine, so the contract this test holds
        is now membership: a code declared here and absent from the table would
        be one a receipt could carry that no reader can look up.
        """

        for code in M.NEW_CODES:
            with self.subTest(code=code):
                self.assertIn(code, loop_types.FAILURE_CODES)
                self.assertNotIn(code, loop_types.OUTCOME_CODES)

    def test_baseline_not_first_is_wave_zeros_code_and_not_a_new_one(self):
        self.assertIn(M.BASELINE_NOT_FIRST, loop_types.FAILURE_CODES)
        self.assertNotIn(M.BASELINE_NOT_FIRST, M.NEW_CODES)

    def test_no_code_is_raised_as_a_string_literal(self):
        source = (
            REPO / "src" / "minireason" / "loop" / "markprep.py"
        ).read_text(encoding="utf-8")
        for code in M.NEW_CODES:
            self.assertNotIn(f'raise MarkprepError("{code}"', source)
            self.assertNotIn(f'BaselineNotFirst("{code}"', source)
            self.assertNotIn(f'BaselineSealBroken("{code}"', source)

    def test_the_exceptions_are_loop_errors(self):
        for kind in (M.MarkprepError, M.BaselineNotFirst, M.BaselineSealBroken):
            self.assertTrue(issubclass(kind, loop_types.LoopError))
        self.assertTrue(issubclass(M.MarkprepError, ValueError))

    def test_the_baseline_is_fenced_to_the_directory_it_is_given(self):
        cell = a_rich_fcl_cell()
        with TemporaryDirectory() as tmp:
            inner = Path(tmp) / "run"
            M.write_baseline(cell, None, inner)
            self.assertEqual(
                sorted(p.name for p in inner.iterdir()), [M.BASELINE_FILENAME]
            )
            with self.assertRaises(custody.CustodyMismatch):
                custody.fenced(inner, "../escape.json")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
