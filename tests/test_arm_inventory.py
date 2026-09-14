"""Offline suite for the B001 arm inventory.

Runs against the in-repo published occurrences and against synthetic trees. It
makes no provider call and writes nothing under any occurrence. Set
``MINIREASON_REPO`` to point at a checkout other than the one two levels above
``src``; the repository-backed tests **fail** if the published occurrences are
absent rather than skipping silently.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

from minireason.graph_import_h005 import FCL_SURFACE_ARMS

STAGE = Path(__file__).resolve().parents[1]
if str(STAGE) not in sys.path:
    sys.path.insert(0, str(STAGE))

from tools import arm_inventory as ai


def repo_root() -> Path:
    override = os.environ.get("MINIREASON_REPO")
    if override:
        return Path(override)
    return Path("/home/user/miniReason")


H005 = "experiments/diagnostics/H005-open-prose-commitments"
F001 = "experiments/diagnostics/F001-fork5-multifamily"
F002 = "experiments/diagnostics/F002-fork5-raised-clock"


def study(*names: str) -> list[str]:
    return [str(repo_root() / n) for n in names]


class SurfaceReadabilityTests(unittest.TestCase):
    """The one reused fact: readability is an arm-NAME membership test."""

    def test_only_mini_fcl_is_read(self):
        reads, reason = ai.surface_read_by_instrument("mini_fcl")
        self.assertTrue(reads)
        self.assertIn("FCL_SURFACE_ARMS", reason)

    def test_every_baseline_arm_name_is_unread(self):
        for arm in ("bare", "native", "matched", "mini_prose", "bare_concat"):
            reads, reason = ai.surface_read_by_instrument(arm)
            self.assertFalse(reads, arm)
            self.assertIn("arm NAME", reason)

    def test_answer_is_the_importers_own_tuple(self):
        """No second opinion: the tuple is imported, never restated."""
        self.assertEqual(ai.FCL_SURFACE_ARMS, FCL_SURFACE_ARMS)
        for arm in ("mini_fcl", "bare", "native", "matched", "anything_else"):
            self.assertEqual(ai.surface_read_by_instrument(arm)[0],
                             arm in FCL_SURFACE_ARMS, arm)

    def test_a_declared_fcl_surface_does_not_make_an_arm_readable(self):
        """The importer reads the name, so `surface: fcl` cannot rescue an arm."""
        inventory = ai.build_inventory(study(F001))
        rows = [a for occ in inventory.occurrences for a in occ.arms]
        self.assertTrue(rows)
        for arm in rows:
            self.assertEqual(arm.reads_commitment_surface,
                             arm.arm in FCL_SURFACE_ARMS, arm.arm)


class PublishedArmTests(unittest.TestCase):
    """What the committed bytes actually hold. These are the premise checks."""

    def test_h005_occurrence_01_publishes_all_five_arms(self):
        inventory = ai.build_inventory(study(H005))
        occ = {o.occurrence: o for o in inventory.occurrences}["occurrence-01"]
        self.assertTrue(occ.readable, occ.unreadable_reason)
        self.assertEqual(sorted(a.arm for a in occ.arms),
                         ["bare", "matched", "mini_fcl", "mini_prose", "native"])

    def test_h005_records_no_arm_kind_and_none_is_invented(self):
        """The owner's runner kept kinds in module constants, not in the plan."""
        inventory = ai.build_inventory(study(H005))
        occ = {o.occurrence: o for o in inventory.occurrences}["occurrence-01"]
        for arm in occ.arms:
            self.assertEqual(arm.kind_source, "plan_settings", arm.arm)
            self.assertIsNone(arm.kind, arm.arm)
            self.assertIsNone(arm.surface, arm.arm)
            self.assertIn("does not infer", arm.kind_note)

    def test_h005_thinking_control_distinguishes_bare_from_native_on_the_wire(self):
        """The one wire fact the owner's plan does record, reported as it stands."""
        inventory = ai.build_inventory(study(H005))
        occ = {o.occurrence: o for o in inventory.occurrences}["occurrence-01"]
        thinking = {a.arm: a.thinking for a in occ.arms}
        self.assertIs(thinking["bare"], False)
        self.assertIs(thinking["native"], True)

    def test_f001_occurrence_01_declares_bare_and_native_kinds(self):
        inventory = ai.build_inventory(study(F001))
        occ = {o.occurrence: o for o in inventory.occurrences}["occurrence-01"]
        kinds = {a.arm: a.kind for a in occ.arms}
        self.assertEqual(kinds["bare"], "bare")
        self.assertEqual(kinds["native"], "native")
        self.assertEqual(sorted(kinds), ["bare", "mini_fcl", "mini_prose", "native"])
        for arm in occ.arms:
            self.assertEqual(arm.kind_source, "arms_json", arm.arm)

    def test_h005_bare_and_native_carry_terminal_artifacts(self):
        inventory = ai.build_inventory(study(H005))
        occ = {o.occurrence: o for o in inventory.occurrences}["occurrence-01"]
        present = {(c.problem, c.arm, c.cycle, c.node)
                   for c in occ.coordinates if c.artifact_present}
        self.assertIn(("daily", "bare", 1, "answer"), present)
        self.assertIn(("daily", "native", 1, "answer"), present)

    def test_f001_declares_a_bare_arm_in_every_occurrence(self):
        inventory = ai.build_inventory(study(F001))
        readable = [o for o in inventory.occurrences if o.readable]
        self.assertEqual(len(readable), 8)
        for occ in readable:
            self.assertIn("bare", [a.arm for a in occ.arms], occ.occurrence)

    def test_f002_declares_only_mini_fcl(self):
        inventory = ai.build_inventory(study(F002))
        readable = [o for o in inventory.occurrences if o.readable]
        self.assertTrue(readable)
        for occ in readable:
            self.assertEqual([a.arm for a in occ.arms], ["mini_fcl"], occ.occurrence)

    def test_only_one_arm_per_occurrence_is_ever_readable(self):
        """The instrument reads at most one arm of any occurrence."""
        inventory = ai.build_inventory(study(H005, F001, F002))
        for occ in inventory.occurrences:
            if not occ.readable:
                continue
            readable = [a.arm for a in occ.arms if a.reads_commitment_surface]
            self.assertLessEqual(len(readable), 1, occ.occurrence)
            self.assertIn(readable, ([], ["mini_fcl"]), occ.occurrence)

    def test_ceilings_and_clocks_are_reported_as_published(self):
        inventory = ai.build_inventory(study(F001, F002))
        by = {(o.study, o.occurrence): o for o in inventory.occurrences if o.readable}
        occ07 = by[("F001-fork5-multifamily", "occurrence-07")]
        bare = {a.arm: a for a in occ07.arms}["bare"]
        self.assertEqual(bare.max_tokens, 32768)
        self.assertIsNone(bare.timeout_seconds_declared)
        self.assertEqual(bare.timeout_seconds_effective, 180)
        f002 = by[("F002-fork5-raised-clock", "occurrence-01")]
        mini = {a.arm: a for a in f002.arms}["mini_fcl"]
        self.assertEqual(mini.max_tokens, 32768)
        self.assertEqual(mini.timeout_seconds_declared, 600)


class ProposalTests(unittest.TestCase):
    """A proposed arm placed beside published ones -- reported, never judged."""

    def proposal(self, **over):
        base = {"arm": "bare", "endpoint": "deepseek-flash", "kind": "bare",
                "surface": "prose", "max_tokens": 8192, "timeout_seconds": 180,
                "seed": None, "problem": "daily", "cycle": 1}
        base.update(over)
        return base

    def test_a_bare_deepseek_arm_matches_every_compared_field_of_a_published_one(self):
        """B001's central fact: the commissioned BARE arm already stands published.

        The proposal is the brief's arm (a) at H005/F001 occurrence-01's own
        conditions -- deepseek-flash, 8192, 180 s, no seed, daily, cycle 1.
        """
        inventory = ai.build_inventory(study(H005, F001), self.proposal())
        exact = [r for r in inventory.proposal_rows
                 if not r.fields_differing and r.problem_and_cycle_match]
        self.assertEqual([(r.study, r.occurrence, r.arm) for r in exact],
                         [("F001-fork5-multifamily", "occurrence-01", "bare")])
        self.assertEqual(exact[0].terminal_artifacts_at_that_coordinate, 1)
        self.assertEqual(list(exact[0].fields_identical), list(ai.COMPARED_FIELDS))

    def test_the_h005_bare_arm_differs_only_where_h005_records_nothing(self):
        """H005's row differs on `kind`/`surface` because its plan records neither."""
        inventory = ai.build_inventory(study(H005), self.proposal())
        row = {(r.occurrence, r.arm): r for r in inventory.proposal_rows}[
            ("occurrence-01", "bare")]
        self.assertEqual(sorted(row.fields_differing), ["kind", "surface"])
        self.assertTrue(row.problem_and_cycle_match)

    def test_a_native_proposal_also_already_stands_published(self):
        proposal = self.proposal(arm="native", kind="native")
        inventory = ai.build_inventory(study(F001), proposal)
        exact = [r for r in inventory.proposal_rows
                 if not r.fields_differing and r.problem_and_cycle_match]
        self.assertEqual([(r.occurrence, r.arm) for r in exact],
                         [("occurrence-01", "native")])

    def test_a_raised_clock_bare_arm_differs_from_every_published_one(self):
        """32768/600 on an Ollama family is not published anywhere."""
        proposal = self.proposal(endpoint="ollama/kimi-k3", max_tokens=32768,
                                 timeout_seconds=600, seed=7)
        inventory = ai.build_inventory(study(H005, F001, F002), proposal)
        for row in inventory.proposal_rows:
            self.assertIn("timeout_seconds", row.fields_differing,
                          "%s/%s" % (row.occurrence, row.arm))

    def test_no_row_says_replay(self):
        inventory = ai.build_inventory(study(F001), self.proposal())
        blob = inventory.to_json().lower()
        self.assertNotIn('"replay"', blob)
        self.assertNotIn("is_replay", blob)

    def test_malformed_proposals_are_refused(self):
        for bad in ({"arm": "bare"}, dict(self.proposal(), extra=1),
                    dict(self.proposal(), cycle="1"),
                    dict(self.proposal(), problem="")):
            with self.assertRaises(ai.InventoryError):
                ai.build_inventory(study(F001), bad)

    def test_a_bool_is_not_an_integer_cycle(self):
        with self.assertRaises(ai.InventoryError):
            ai.build_inventory(study(F001), dict(self.proposal(), cycle=True))


class InvariantTests(unittest.TestCase):

    def test_u5_deterministic(self):
        first = ai.build_inventory(study(F001)).to_json()
        second = ai.build_inventory(study(F001)).to_json()
        self.assertEqual(first, second)

    def test_u6_no_scoring_key_anywhere(self):
        payload = json.loads(ai.build_inventory(study(H005, F001, F002)).to_json())

        def walk(node):
            if isinstance(node, dict):
                for key, value in node.items():
                    self.assertNotIn(key.lower(), ai.FORBIDDEN_KEYS, key)
                    walk(value)
            elif isinstance(node, list):
                for item in node:
                    walk(item)

        walk(payload)

    def test_u1_every_file_read_is_digested(self):
        inventory = ai.build_inventory(study(F002))
        self.assertTrue(inventory.files_read)
        for path, sha in inventory.files_read.items():
            self.assertRegex(sha, r"\A[0-9a-f]{64}\Z")
            self.assertFalse(path.startswith("/"), path)

    def test_u2_no_artifact_content_is_reported(self):
        """Presence only. No body, no commitments, no delivery status."""
        payload = ai.build_inventory(study(H005)).to_json().lower()
        for forbidden in ('"body"', '"commitments"', "delivery_status",
                          "envelope_status"):
            self.assertNotIn(forbidden, payload)

    def test_banner_is_carried_into_both_outputs(self):
        inventory = ai.build_inventory(study(F002))
        self.assertIn(ai.INVENTORY_BANNER, inventory.to_markdown())
        self.assertIn(ai.INVENTORY_BANNER, json.loads(inventory.to_json())["banner"])


class WriterTests(unittest.TestCase):

    def test_writes_two_files_into_a_new_directory(self):
        inventory = ai.build_inventory(study(F002))
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "inv"
            markdown, payload = ai.write_inventory(inventory, out)
            self.assertTrue(markdown.is_file() and payload.is_file())
            self.assertEqual(json.loads(payload.read_text())["schema"],
                             ai.INVENTORY_SCHEMA)

    def test_refuses_an_existing_directory(self):
        inventory = ai.build_inventory(study(F002))
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ai.OutDirRefused):
                ai.write_inventory(inventory, tmp)

    def test_nothing_is_written_under_the_occurrence(self):
        before = sorted(p.name for p in (repo_root() / F002).iterdir())
        ai.build_inventory(study(F002))
        self.assertEqual(before,
                         sorted(p.name for p in (repo_root() / F002).iterdir()))

    def test_cli_refuses_an_out_dir_inside_the_study(self):
        inside = str(repo_root() / F002 / "inventory-out")
        code = ai.main([inside, "--study", str(repo_root() / F002)])
        self.assertEqual(code, 4)
        self.assertFalse(Path(inside).exists())


class SelectorTests(unittest.TestCase):

    def test_unknown_study_is_selector_matched_nothing(self):
        with self.assertRaises(ai.SelectorMatchedNothing):
            ai.build_inventory([str(repo_root() / "experiments/diagnostics/NOPE")])

    def test_a_study_with_no_occurrence_is_build_failed(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "notes").mkdir()
            with self.assertRaises(ai.InventoryError):
                ai.build_inventory([tmp])

    def test_an_occurrence_missing_its_plan_is_listed_not_repaired(self):
        with tempfile.TemporaryDirectory() as tmp:
            occ = Path(tmp) / "occurrence-01"
            occ.mkdir()
            (occ / "arms.json").write_text(json.dumps(
                {"schema": "minireason.h005.arms.v1", "arms": {}}))
            inventory = ai.build_inventory([tmp])
            row = inventory.occurrences[0]
            self.assertFalse(row.readable)
            self.assertIn("plan.json", row.unreadable_reason)

    def test_a_plan_with_no_arm_declaration_is_listed_not_repaired(self):
        with tempfile.TemporaryDirectory() as tmp:
            occ = Path(tmp) / "occurrence-01"
            occ.mkdir()
            (occ / "plan.json").write_text(json.dumps({"plan_id": "x"}))
            row = ai.build_inventory([tmp]).occurrences[0]
            self.assertFalse(row.readable)
            self.assertIn("no arm declaration", row.unreadable_reason)

    def test_reader_refuses_a_path_outside_the_study(self):
        with tempfile.TemporaryDirectory() as tmp:
            reader = ai._Reader([Path(tmp)])
            with self.assertRaises(ai.InventoryError):
                reader.read_json(Path(tmp).parent / "elsewhere.json")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
