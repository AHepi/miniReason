"""Tests for the H005 use-relation instrument, against the in-repo occurrence.

The occurrence is the subject, not a fixture: if it is absent the suite
**fails**, because a green run over no data would say nothing. The single
escape hatch is ``H005_IMPORT_ALLOW_SKIP=1`` (the same variable the importer's
own suite uses), and it prints what is missing and why the result is worthless
without it.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

STAGING = Path(__file__).resolve().parents[1]
if str(STAGING / "src") not in sys.path:
    sys.path.insert(0, str(STAGING / "src"))

from minireason.use_relation_h005 import (  # noqa: E402
    NO_OVERLAP_NOTE,
    PROSE_SURFACE_NOTE,
    REF_FIELDS,
    ROOT_CELLS,
    ROOT_READING_VOCABULARY,
    OutDirRefused,
    _display_key,
    _Resolution,
    build_use_table,
    record_prose,
    record_source_spans,
    split_sentences,
    uptake_buckets,
    write_use_table,
)
from minireason.graph_import_h005 import (  # noqa: E402
    Coordinate,
    MappingError,
    _Importer,
    iter_references,
    verify_custody,
)

#: A run with two different, pinned hash seeds: the determinism claim is about
#: dict/set iteration order, which only differs across processes.
HASH_SEEDS = ("0", "12345")


def _resolution_map_from_map_records(occurrence, **scope):
    """(coordinate, record_id, field, ref) -> (owner key, target record id).

    Spied on the importer's own resolver during a real ``map_records``, so it
    is what the import actually did - not a restatement of it.
    """
    importer = _Importer(occurrence, scope.get("problems"), scope.get("arms"),
                         scope.get("cycles"))
    custody = verify_custody(importer.reader, importer.ledger)
    importer.load_nodes(
        importer.discover_scope(custody["material"], custody["plan"]), custody["plan"])
    importer.parse_documents()
    seen = {}
    original = _Importer.resolve_ref

    def spy(self, node, ref, record, field_name):
        owner, record_id = original(self, node, ref, record, field_name)
        seen[(node.coord.key, None if record is None else record.get("id"),
              field_name, ref)] = (None if owner is None else owner.key, record_id)
        return owner, record_id

    _Importer.resolve_ref = spy
    try:
        importer.map_records()
    finally:
        _Importer.resolve_ref = original
    return seen, dict(importer.resolution)


def _resolution_map_from_instrument(occurrence, **scope):
    """The same map, taken from what the instrument put in front of root."""
    table = build_use_table(occurrence, **scope)
    seen = {}
    for row in table.rows:
        seen[(row.referring_coordinate_key, row.referring_record_id, row.ref_field,
              row.ref_verbatim)] = (row.target_coordinate_key, row.target_record_id)
    return table, seen

OCCURRENCE_RELATIVE = Path(
    "experiments/diagnostics/H005-open-prose-commitments/occurrence-01"
)
#: Keys that must never name a field of this instrument's output. The tool
#: does not score, rank, appraise or label; a key with one of these names would
#: be the first sign that it had started to.
FORBIDDEN_KEY_SUBSTRINGS = ("score", "rank", "merit", "status", "label")

#: The golden scope: the five FCL-1 documents of daily/mini_fcl/cycle01.
GOLDEN_ARMS = ["mini_fcl"]
GOLDEN_CYCLES = [1]


def _find_occurrence() -> Path | None:
    override = os.environ.get("H005_OCCURRENCE")
    if override:
        candidate = Path(override)
        return candidate if candidate.is_dir() else None
    candidates = [
        STAGING / OCCURRENCE_RELATIVE,
        STAGING.parent / OCCURRENCE_RELATIVE,
        Path("/home/user/miniReason") / OCCURRENCE_RELATIVE,
    ]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return None


OCCURRENCE = _find_occurrence()

if OCCURRENCE is None:
    _override = os.environ.get("H005_OCCURRENCE")
    _WHERE = (
        "$H005_OCCURRENCE is set to %r, which is not a directory" % _override
        if _override
        else "looked for %s under the staging tree, its parent and /home/user/miniReason, "
        "and $H005_OCCURRENCE is unset" % OCCURRENCE_RELATIVE
    )
    if os.environ.get("H005_IMPORT_ALLOW_SKIP") == "1":
        raise unittest.SkipTest(
            "H005 occurrence-01 not found (%s). H005_IMPORT_ALLOW_SKIP=1 is set, so this "
            "suite is skipped - but a skipped run has checked NOTHING about the "
            "instrument: every assertion here is about the real occurrence bytes." % _WHERE
        )
    raise AssertionError(
        "H005 occurrence-01 not found (%s). This suite tests the instrument against the "
        "real occurrence and refuses to pass without it. Set H005_OCCURRENCE to the "
        "occurrence directory, or H005_IMPORT_ALLOW_SKIP=1 to skip deliberately." % _WHERE
    )


def _tree_digest(root: Path) -> str:
    """A digest of every file under ``root``: path, size and content."""
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(str(path.relative_to(root)).encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def _keys(value, found=None):
    found = [] if found is None else found
    if isinstance(value, dict):
        for key, item in value.items():
            found.append(key)
            _keys(item, found)
    elif isinstance(value, list):
        for item in value:
            _keys(item, found)
    return found


class GoldenScopeTests(unittest.TestCase):
    """Everything that is a fact about daily/mini_fcl/cycle01."""

    @classmethod
    def setUpClass(cls):
        cls.table = build_use_table(OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)
        cls.payload = json.loads(cls.table.to_json())

    # -- the row count ----------------------------------------------------- #

    def test_row_count_is_the_cross_document_refs_the_resolver_resolved(self):
        """Rows == refs walked - intra-document - task refs - unresolved.

        The importer's own counters say the golden scope holds 84 authored
        refs: 82 under its ``resolved`` counter, 2 admitted by extension (the
        ``#BODY`` pseudo-local and the bare exposed-artifact label), 0 dangling.
        62 of the 84 resolve to a record of the referring document itself and
        are therefore not cross-document. 84 - 62 - 0 - 0 = **22 rows**;
        equivalently 82 - 62 = 20 strictly-resolved cross-document refs plus
        the 2 extension-admitted ones, which the row spec includes.
        """
        totals = self.table.reference_totals
        self.assertEqual(totals["refs_walked"], 84)
        self.assertEqual(totals["importer_resolved_counter"], 82)
        self.assertEqual(totals["importer_extension_counter"], 2)
        self.assertEqual(totals["importer_dangling_counter"], 0)
        self.assertEqual(totals["intra_document"], 62)
        self.assertEqual(totals["refs_to_exposed_task_artifact"], 0)
        self.assertEqual(totals["unresolved"], 0)
        computed = (
            totals["refs_walked"]
            - totals["intra_document"]
            - totals["refs_to_exposed_task_artifact"]
            - totals["unresolved"]
        )
        self.assertEqual(computed, 22)
        self.assertEqual(totals["cross_document_rows"], computed)
        self.assertEqual(len(self.table.rows), computed)
        # The two ways of counting the same 84 refs must agree.
        self.assertEqual(
            totals["importer_resolved_counter"]
            + totals["importer_extension_counter"]
            + totals["importer_dangling_counter"],
            totals["refs_walked"],
        )
        # And 82 - 62 = 20 of the rows are strictly-resolved, 2 by extension.
        by_extension = [
            row
            for row in self.table.rows
            if any(
                note.code in ("bare_label_ref", "qualified_ref_body_pseudo_local")
                for note in row.resolver_notes
            )
        ]
        self.assertEqual(len(by_extension), 2)
        self.assertEqual(len(self.table.rows) - len(by_extension), 20)

    def test_every_row_is_genuinely_cross_document(self):
        for row in self.table.rows:
            self.assertNotEqual(
                row.referring_coordinate_key,
                row.target_coordinate_key,
                msg="an intra-document ref reached the table: " + row.ref_verbatim,
            )

    def test_only_authored_ref_fields_produce_rows(self):
        self.assertEqual(
            sorted({row.ref_field for row in self.table.rows}), ["mentions", "target"]
        )

    # -- the four empty cells ---------------------------------------------- #

    def test_every_root_cell_is_empty_in_every_row(self):
        self.assertEqual(
            ROOT_CELLS,
            ("root_reading", "root_passage_cited", "root_notes", "root_initials_date"),
        )
        for index, row in enumerate(self.payload["rows"]):
            for cell in ROOT_CELLS:
                self.assertIn(cell, row, msg=f"row {index} has no {cell} cell")
                self.assertEqual(row[cell], "", msg=f"row {index}.{cell} is not empty")

    def test_the_root_reading_vocabulary_is_published_but_never_selected(self):
        self.assertEqual(
            list(ROOT_READING_VOCABULARY),
            self.payload["method"]["root_reading_vocabulary"],
        )
        self.assertIn("unresolved", ROOT_READING_VOCABULARY)
        rendered = self.table.to_markdown()
        self.assertIn("The instrument never selects one.", rendered)
        for row in self.table.rows:
            self.assertEqual(row.root_reading, "")

    # -- no scoring, no classification ------------------------------------- #

    def test_no_forbidden_key_anywhere_in_the_json(self):
        offenders = sorted(
            {
                key
                for key in _keys(self.payload)
                if any(bad in key.lower() for bad in FORBIDDEN_KEY_SUBSTRINGS)
            }
        )
        self.assertEqual(offenders, [], msg="forbidden key names in use_table.json")

    def test_no_attack_or_dependence_relation_is_emitted(self):
        rendered = self.table.to_json()
        for forbidden in ('"att"', '"dep"', '"att_edges"', '"dep_edges"', '"warrants"'):
            self.assertNotIn(forbidden, rendered)

    # -- verbatim ---------------------------------------------------------- #

    def test_every_verbatim_record_equals_the_source_bytes(self):
        commitments: dict[str, str] = {}
        for coordinate in self.table.scope:
            key = "%s/%s/cycle%02d/%s" % (
                coordinate["problem"],
                coordinate["arm"],
                coordinate["cycle"],
                coordinate["node"],
            )
            path = (
                OCCURRENCE
                / "artifacts"
                / coordinate["problem"]
                / coordinate["arm"]
                / ("cycle%02d" % coordinate["cycle"])
                / (coordinate["node"] + ".json")
            )
            commitments[key] = json.loads(path.read_text(encoding="utf-8"))["commitments"]
        checked = 0
        for row in self.table.rows:
            for key, verbatim, span in (
                (
                    row.referring_coordinate_key,
                    row.referring_record_verbatim,
                    row.referring_record_source_span,
                ),
                (
                    row.target_coordinate_key,
                    row.target_record_verbatim,
                    row.target_record_source_span,
                ),
            ):
                if verbatim is None:
                    self.assertIsNone(span)
                    continue
                source = commitments[key]
                self.assertEqual(verbatim, source[span[0]:span[1]])
                self.assertIn(verbatim, source)
                checked += 1
        self.assertGreater(checked, 0)

    def test_record_source_spans_round_trip_for_every_document(self):
        for coordinate in self.table.scope:
            path = (
                OCCURRENCE
                / "artifacts"
                / coordinate["problem"]
                / coordinate["arm"]
                / ("cycle%02d" % coordinate["cycle"])
                / (coordinate["node"] + ".json")
            )
            commitments = json.loads(path.read_text(encoding="utf-8"))["commitments"]
            document = json.loads(commitments)
            spans = record_source_spans(commitments, document)
            self.assertEqual(len(spans), len(document["records"]))
            for (start, end), record in zip(spans, document["records"]):
                self.assertEqual(json.loads(commitments[start:end]), record)

    # -- passages ----------------------------------------------------------- #

    def test_every_passage_offset_quotes_its_own_body(self):
        bodies: dict[str, str] = {}
        for coordinate in self.table.scope:
            key = "%s/%s/cycle%02d/%s" % (
                coordinate["problem"],
                coordinate["arm"],
                coordinate["cycle"],
                coordinate["node"],
            )
            path = (
                OCCURRENCE
                / "artifacts"
                / coordinate["problem"]
                / coordinate["arm"]
                / ("cycle%02d" % coordinate["cycle"])
                / (coordinate["node"] + ".json")
            )
            bodies[key] = json.loads(path.read_text(encoding="utf-8"))["body"]
        for row in self.table.rows:
            body = bodies[row.referring_coordinate_key]
            for passage in row.referring_body_passages:
                self.assertEqual(passage.text, body[passage.start:passage.end])
                self.assertTrue(passage.distinctive_tokens_present)
            if not row.referring_body_passages:
                self.assertEqual(row.lexical_overlap_note, NO_OVERLAP_NOTE)
            else:
                self.assertEqual(row.lexical_overlap_note, "")

    def test_sentence_spans_are_ordered_and_separated_only_by_whitespace(self):
        body = (
            "A first sentence about chores. A second one (e.g. bins)!\n\n"
            "1. A numbered item that must not split at the marker.\nTail"
        )
        spans = split_sentences(body)
        self.assertTrue(spans)
        previous_end = 0
        for start, end, text in spans:
            self.assertGreaterEqual(start, previous_end)
            self.assertEqual(text, body[start:end])
            self.assertEqual(text, text.strip())
            self.assertEqual(body[previous_end:start].strip(), "")
            previous_end = end
        self.assertTrue(
            any(t.startswith("1. A numbered item") for _, _, t in spans),
            msg="the numbered list marker split the sentence",
        )

    def test_record_prose_excludes_names_and_pointers(self):
        record = {
            "id": "zz1",
            "type": "claim",
            "text": "alpha",
            "scope": "beta",
            "grounds": "gamma",
            "target": ["p.x.0#c1"],
            "depends": ["zz0"],
        }
        self.assertEqual(record_prose(record), "alpha beta gamma")

    # -- uptake ------------------------------------------------------------- #

    def test_declared_uptake_versus_records_present(self):
        observed = {
            document.coordinate_key: (
                len(document.records_in_uptake),
                len(document.records_present),
                document.records_omitted_from_uptake,
            )
            for document in self.table.documents
        }
        self.assertEqual(
            observed["daily/mini_fcl/cycle01/account"], (5, 6, ("p1",))
        )
        self.assertEqual(
            observed["daily/mini_fcl/cycle01/objection"], (6, 8, ("o4", "p1"))
        )
        self.assertEqual(
            observed["daily/mini_fcl/cycle01/rival"],
            (4, 11, ("r1", "r3", "r4", "r5", "r8", "r10", "r11")),
        )
        self.assertEqual(observed["daily/mini_fcl/cycle01/response"], (9, 9, ()))
        self.assertEqual(observed["daily/mini_fcl/cycle01/carry"], (8, 8, ()))
        for document in self.table.documents:
            self.assertEqual(document.uptake_entries_naming_nothing, ())
            self.assertEqual(document.uptake_entries_naming_another_document, ())

    def test_uptake_columns_agree_with_the_per_document_section(self):
        in_uptake = {
            document.coordinate_key: set(document.records_in_uptake)
            for document in self.table.documents
        }
        for row in self.table.rows:
            if row.referring_record_id is None:
                self.assertIsNone(row.declared_uptake_includes_referring_record)
            else:
                self.assertEqual(
                    row.declared_uptake_includes_referring_record,
                    row.referring_record_id in in_uptake[row.referring_coordinate_key],
                )
            if row.target_record_id is None:
                self.assertIsNone(row.declared_uptake_includes_target_record)
            else:
                self.assertEqual(
                    row.declared_uptake_includes_target_record,
                    row.target_record_id in in_uptake[row.target_coordinate_key],
                )

    def test_no_unresolved_ref_in_the_golden_scope(self):
        self.assertEqual(self.table.unresolved_refs, ())
        self.assertIn(
            "*No unresolved ref in this scope.*", self.table.to_markdown()
        )


class DeterminismAndReadOnlyTests(unittest.TestCase):
    def test_two_builds_are_byte_identical(self):
        first = build_use_table(OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)
        second = build_use_table(OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)
        self.assertEqual(first.to_json().encode("utf-8"), second.to_json().encode("utf-8"))
        self.assertEqual(
            first.to_markdown().encode("utf-8"), second.to_markdown().encode("utf-8")
        )

    def test_two_cli_runs_write_byte_identical_files(self):
        with tempfile.TemporaryDirectory(prefix="use-relation-determinism-") as directory:
            first = Path(directory) / "a"
            second = Path(directory) / "b"
            for out in (first, second):
                result = _run_cli([str(OCCURRENCE), str(out), "--arm", "mini_fcl",
                                   "--cycle", "1"])
                self.assertEqual(result.returncode, 0, msg=result.stderr)
            for name in ("USE_TABLE.md", "use_table.json"):
                self.assertEqual(
                    (first / name).read_bytes(),
                    (second / name).read_bytes(),
                    msg=name + " differs between two runs",
                )

    def test_the_occurrence_is_not_touched(self):
        before = _tree_digest(OCCURRENCE)
        with tempfile.TemporaryDirectory(prefix="use-relation-readonly-") as directory:
            table = build_use_table(OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)
            write_use_table(table, Path(directory) / "out")
        self.assertEqual(before, _tree_digest(OCCURRENCE))

    def test_files_read_are_all_inside_the_occurrence(self):
        table = build_use_table(OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)
        self.assertTrue(table.files_read)
        for entry in table.files_read:
            self.assertFalse(entry["path"].startswith("/"))
            self.assertNotIn("..", entry["path"])
            self.assertTrue((OCCURRENCE / entry["path"]).is_file())
            self.assertEqual(
                hashlib.sha256((OCCURRENCE / entry["path"]).read_bytes()).hexdigest(),
                entry["sha256"],
            )


class ProseSurfaceTests(unittest.TestCase):
    """Prose arms are listed, never mined."""

    @classmethod
    def setUpClass(cls):
        cls.table = build_use_table(OCCURRENCE)

    def test_prose_nodes_are_listed_with_the_required_note(self):
        prose = [
            node
            for node in self.table.nodes_not_read
            if node.commitment_surface == "prose_not_parsed"
        ]
        self.assertTrue(prose, msg="the occurrence holds prose arms; none was listed")
        for node in prose:
            self.assertEqual(node.note, PROSE_SURFACE_NOTE)
        arms = {node.coordinate["arm"] for node in prose}
        self.assertTrue({"matched", "mini_prose", "bare", "native"} & arms)

    def test_no_row_or_document_section_comes_from_a_non_fcl1_arm(self):
        listed = {node.coordinate_key for node in self.table.nodes_not_read}
        for row in self.table.rows:
            self.assertNotIn(row.referring_coordinate_key, listed)
            self.assertNotIn(row.target_coordinate_key, listed)
        for document in self.table.documents:
            self.assertNotIn(document.coordinate_key, listed)
            self.assertEqual(document.commitment_surface, "read_fcl1")

    def test_the_full_occurrence_yields_the_same_rows_as_the_golden_scope(self):
        golden = build_use_table(OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)
        self.assertEqual(
            [r.ref_verbatim for r in self.table.rows],
            [r.ref_verbatim for r in golden.rows],
        )
        self.assertEqual(len(self.table.rows), 22)


def _run_cli(arguments: list[str], *, hash_seed: str | None = None) -> subprocess.CompletedProcess:
    environment = dict(os.environ)
    paths = [str(STAGING / "src")]
    existing = environment.get("PYTHONPATH")
    if existing:
        paths.append(existing)
    environment["PYTHONPATH"] = os.pathsep.join(paths)
    if hash_seed is not None:
        environment["PYTHONHASHSEED"] = hash_seed
    return subprocess.run(
        [sys.executable, str(STAGING / "tools" / "use_relation_h005.py")] + arguments,
        capture_output=True,
        text=True,
        env=environment,
    )


class CommandLineTests(unittest.TestCase):
    def test_exit_zero_and_both_files_written(self):
        with tempfile.TemporaryDirectory(prefix="use-relation-cli-") as directory:
            out = Path(directory) / "table"
            result = _run_cli([str(OCCURRENCE), str(out), "--arm", "mini_fcl",
                               "--cycle", "1"])
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertTrue((out / "USE_TABLE.md").is_file())
            self.assertTrue((out / "use_table.json").is_file())
            self.assertIn("22 cross-document rows", result.stdout)
            self.assertIn("the reading is root's", result.stdout)

    def test_exit_two_when_custody_fails(self):
        with tempfile.TemporaryDirectory(prefix="use-relation-custody-") as directory:
            broken = Path(directory) / "occurrence"
            broken.mkdir()
            (broken / "plan.json").write_text(
                json.dumps({"schema": "minireason.h005.plan.v1", "plan_id": "nope"}),
                encoding="utf-8",
            )
            result = _run_cli([str(broken), str(Path(directory) / "out")])
            self.assertEqual(result.returncode, 2, msg=result.stdout + result.stderr)
            self.assertIn("CUSTODY_REFUSED:", result.stderr)
            self.assertFalse((Path(directory) / "out").exists())

    def test_exit_two_when_the_occurrence_does_not_exist(self):
        with tempfile.TemporaryDirectory(prefix="use-relation-missing-") as directory:
            result = _run_cli(
                [str(Path(directory) / "absent"), str(Path(directory) / "out")]
            )
            self.assertEqual(result.returncode, 2, msg=result.stdout + result.stderr)
            self.assertIn("CUSTODY_REFUSED:", result.stderr)

    def test_exit_four_when_the_out_dir_exists(self):
        with tempfile.TemporaryDirectory(prefix="use-relation-outdir-") as directory:
            out = Path(directory) / "already"
            out.mkdir()
            result = _run_cli([str(OCCURRENCE), str(out), "--arm", "mini_fcl"])
            self.assertEqual(result.returncode, 4, msg=result.stdout + result.stderr)
            self.assertIn("OUT_DIR_REFUSED:", result.stderr)
            self.assertEqual(sorted(p.name for p in out.iterdir()), [])

    def test_exit_five_when_the_selector_matches_nothing(self):
        with tempfile.TemporaryDirectory(prefix="use-relation-selector-") as directory:
            result = _run_cli(
                [str(OCCURRENCE), str(Path(directory) / "out"), "--arm", "no_such_arm"]
            )
            self.assertEqual(result.returncode, 5, msg=result.stdout + result.stderr)
            self.assertIn("SELECTOR_MATCHED_NOTHING", result.stderr)
            self.assertFalse((Path(directory) / "out").exists())

    def test_written_markdown_matches_the_library(self):
        with tempfile.TemporaryDirectory(prefix="use-relation-match-") as directory:
            out = Path(directory) / "table"
            result = _run_cli([str(OCCURRENCE), str(out), "--arm", "mini_fcl",
                               "--cycle", "1"])
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            table = build_use_table(OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)
            self.assertEqual((out / "USE_TABLE.md").read_text(encoding="utf-8"),
                             table.to_markdown())
            self.assertEqual((out / "use_table.json").read_text(encoding="utf-8"),
                             table.to_json())


class ImporterEquivalenceTests(unittest.TestCase):
    """The coupling the whole design rests on, pinned.

    The instrument's value is that its resolutions ARE the import's. Nothing in
    the suite used to check that, which is why a shim that agreed with the
    importer only on this occurrence's happy shape could sit in it unnoticed.
    """

    def assert_equivalent(self, **scope):
        spied, counters = _resolution_map_from_map_records(OCCURRENCE, **scope)
        walked = {}
        for entry in iter_references(OCCURRENCE, **scope):
            walked[(entry.coordinate.key, entry.record_id, entry.field, entry.raw_ref)] = (
                None if entry.owner_coordinate is None else entry.owner_coordinate.key,
                entry.target_record_id,
            )
        self.assertEqual(walked, spied)
        table, rows = _resolution_map_from_instrument(OCCURRENCE, **scope)
        # Every row the instrument shows root is a cross-document entry of the
        # map the import itself produced, with the same owner and record id.
        for key, value in rows.items():
            self.assertIn(key, spied, msg="a row the import never resolved: %r" % (key,))
            self.assertEqual(value, spied[key], msg="row %r disagrees with the import" % (key,))
        cross = {
            key: value
            for key, value in spied.items()
            if value[0] is not None and value[0] != key[0]
        }
        self.assertEqual(set(rows), set(cross))
        totals = table.reference_totals
        self.assertEqual(totals["refs_walked"], counters["refs"])
        self.assertEqual(totals["importer_resolved_counter"], counters["resolved"])
        self.assertEqual(totals["importer_extension_counter"], counters["extensions"])
        self.assertEqual(totals["importer_dangling_counter"], counters["dangling"])
        self.assertEqual(totals["refs_to_exposed_task_artifact"], counters["task"])
        return table

    def test_the_golden_scope_resolutions_are_the_importers_own(self):
        table = self.assert_equivalent(arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)
        self.assertEqual(len(table.rows), 22)

    def test_the_full_occurrence_resolutions_are_the_importers_own(self):
        self.assert_equivalent()

    def test_the_instrument_writes_nothing_into_the_importers_structures(self):
        # The sentinel this instrument used to write into _Node.spec_id leaked
        # into residue[*].carrier.spec_artifact_id, a field that everywhere else
        # holds a content-addressed spec artifact id.
        table = build_use_table(OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)
        rendered = table.to_json()
        self.assertNotIn("use-relation:in-scope", rendered)
        for entry in iter_references(OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES):
            for _code, reason in entry.notes:
                self.assertNotIn("use-relation", reason)


class UnreadableSurfaceTests(unittest.TestCase):
    """A ref into a node whose commitment surface was not readable.

    Not reachable in occurrence-01 as it stands - no FCL-1 node has a
    cross-arm projection - but it is exactly the `matched` arm's own shape
    (prose parents, two `unavailable_decode_failure` surfaces), so it is
    synthesised here by making one in-scope FCL node's document unreadable
    *after* parsing while it remains the projection source of four later nodes.
    Both the import and the instrument see the same synthetic occurrence.
    """

    BROKEN = "daily/mini_fcl/cycle01/account"

    def setUp(self):
        original = _Importer.parse_documents
        broken = self.BROKEN

        def wrapper(importer):
            original(importer)
            for coord, node in importer.nodes.items():
                if coord.key == broken:
                    node.document = None
                    node.commitment_surface_state = "unavailable_decode_failure"

        _Importer.parse_documents = wrapper
        self.addCleanup(setattr, _Importer, "parse_documents", original)

    def test_the_instrument_and_the_import_still_resolve_alike(self):
        spied, counters = _resolution_map_from_map_records(
            OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)
        walked = {}
        for entry in iter_references(OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES):
            walked[(entry.coordinate.key, entry.record_id, entry.field, entry.raw_ref)] = (
                None if entry.owner_coordinate is None else entry.owner_coordinate.key,
                entry.target_record_id,
            )
        self.assertEqual(walked, spied)
        self.assertGreater(counters["dangling"], 0, "the fixture must break something")
        table, _rows = _resolution_map_from_instrument(
            OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)
        self.assertEqual(table.reference_totals["importer_dangling_counter"],
                         counters["dangling"])
        self.assertEqual(table.reference_totals["importer_extension_counter"],
                         counters["extensions"])

    def test_the_residue_carries_the_importers_own_reason_not_an_out_of_scope_one(self):
        table = build_use_table(OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)
        self.assertTrue(table.unresolved_refs, "the fixture must produce residue")
        reasons = {residue.reason for residue in table.unresolved_refs}
        codes = {residue.code for residue in table.unresolved_refs}
        self.assertIn(
            "the owning artifact has no readable FCL-1 document; dropped, never invented",
            reasons)
        self.assertEqual(codes, {"ref_unresolved"})
        for residue in table.unresolved_refs:
            self.assertNotIn("outside the imported scope", residue.reason)
            self.assertNotIn("not registered yet in wave order", residue.reason)

    def test_the_unreadable_node_is_listed_and_never_reconstructed(self):
        table = build_use_table(OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)
        listed = {node.coordinate_key: node for node in table.nodes_not_read}
        self.assertIn(self.BROKEN, listed)
        self.assertEqual(listed[self.BROKEN].commitment_surface,
                         "unavailable_decode_failure")
        self.assertNotIn(self.BROKEN,
                         [row.referring_coordinate_key for row in table.rows])

    def test_the_two_ways_of_counting_unresolved_refs_agree(self):
        table = build_use_table(OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)
        self.assertEqual(len(table.unresolved_refs),
                         table.reference_totals["unresolved"])


class RowOrderAndUptakeBucketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.table = build_use_table(OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)

    def test_an_uptake_row_sorts_after_every_record_row_of_its_document(self):
        # The docstring says uptake is document-level and sorts after every
        # record; the sub-key used to be -1, which sorts before all of them.
        class _StubNode:
            records = [{"id": "k1"}, {"id": "k2"}, {"id": "k3"}]

        def resolution(field_name, record_index):
            return _Resolution(
                node=_StubNode(), record=None, record_index=record_index,
                field_name=field_name, ref="x", ref_index=0, owner=None,
                record_id=None, notes=(), resolution="resolved")

        uptake = _display_key(resolution("uptake", None))
        for index in range(len(_StubNode.records)):
            for field_name in REF_FIELDS:
                self.assertLess(_display_key(resolution(field_name, index)), uptake)

    def test_the_three_uptake_buckets_are_disjoint_and_exhaustive(self):
        for document in self.table.documents:
            entries = [entry.ref_verbatim for entry in document.uptake_entries]
            buckets = (
                list(document.uptake_entries_naming_nothing),
                list(document.uptake_entries_naming_another_document),
                list(document.uptake_entries_naming_this_contribution_not_a_record),
            )
            for first in range(len(buckets)):
                for second in range(first + 1, len(buckets)):
                    self.assertFalse(
                        set(buckets[first]) & set(buckets[second]),
                        msg="%s: buckets %d and %d overlap" % (
                            document.coordinate_key, first, second),
                    )
            local = [
                entry.ref_verbatim
                for entry in document.uptake_entries
                if entry.resolved_coordinate_key == document.coordinate_key
                and entry.resolved_record_id is not None
            ]
            self.assertEqual(
                len(entries), sum(len(b) for b in buckets) + len(local),
                msg=document.coordinate_key + ": the buckets do not exhaust uptake")

    def test_a_ref_naming_a_whole_contribution_is_not_a_ref_naming_nothing(self):
        # The genuine case the old record-id gate put in two contradictory
        # buckets at once: owner set, record id None.
        here = Coordinate.from_dict(self.table.documents[0].coordinate)
        elsewhere = Coordinate.from_dict(self.table.documents[1].coordinate)

        def resolution(owner, record_id, ref):
            return _Resolution(
                node=None, record=None, record_index=None, field_name="uptake",
                ref=ref, ref_index=0, owner=owner, record_id=record_id, notes=(),
                resolution="resolved" if owner is not None else "unresolved")

        walked = [
            resolution(None, None, "dangling"),
            resolution(here, None, "whole-contribution"),
            resolution(elsewhere, "k1", "another-document"),
            resolution(here, "k1", "ordinary-local"),
        ]
        nothing, another, whole = uptake_buckets(walked, here)
        self.assertEqual(nothing, ("dangling",))
        self.assertEqual(another, ("another-document",))
        self.assertEqual(whole, ("whole-contribution",))
        self.assertNotIn("whole-contribution", nothing)

    def test_the_two_ways_of_counting_unresolved_refs_agree_on_the_golden_scope(self):
        self.assertEqual(len(self.table.unresolved_refs),
                         self.table.reference_totals["unresolved"])


class OutputContainmentTests(unittest.TestCase):
    """U1: nothing under the occurrence is ever written."""

    @classmethod
    def setUpClass(cls):
        cls.table = build_use_table(OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)

    def test_write_use_table_refuses_a_destination_inside_the_occurrence(self):
        before = _tree_digest(OCCURRENCE)
        with self.assertRaises(OutDirRefused) as raised:
            write_use_table(self.table, OCCURRENCE / "INSIDE")
        self.assertIn("OUT_DIR_INSIDE_OCCURRENCE", str(raised.exception))
        self.assertEqual(before, _tree_digest(OCCURRENCE))
        self.assertFalse((OCCURRENCE / "INSIDE").exists())

    def test_write_use_table_refuses_the_occurrence_itself(self):
        before = _tree_digest(OCCURRENCE)
        with self.assertRaises(OutDirRefused):
            write_use_table(self.table, OCCURRENCE)
        self.assertEqual(before, _tree_digest(OCCURRENCE))

    def test_write_use_table_refuses_an_existing_directory_at_the_library_level(self):
        with tempfile.TemporaryDirectory(prefix="use-relation-exists-") as directory:
            out = Path(directory) / "already"
            out.mkdir()
            with self.assertRaises(OutDirRefused) as raised:
                write_use_table(self.table, out)
            self.assertIn("OUT_DIR_EXISTS", str(raised.exception))
            self.assertEqual(sorted(p.name for p in out.iterdir()), [])

    def test_the_cli_refuses_a_destination_inside_the_occurrence(self):
        with tempfile.TemporaryDirectory(prefix="use-relation-inside-") as directory:
            occurrence = Path(directory) / "occurrence"
            shutil.copytree(OCCURRENCE, occurrence)
            before = _tree_digest(occurrence)
            result = _run_cli([str(occurrence), str(occurrence / "INSIDE"),
                               "--arm", "mini_fcl", "--cycle", "1"])
            self.assertEqual(result.returncode, 4, msg=result.stdout + result.stderr)
            self.assertIn("OUT_DIR_INSIDE_OCCURRENCE", result.stderr)
            self.assertEqual(before, _tree_digest(occurrence))


class CliFailureMappingTests(unittest.TestCase):
    """The exit codes the doc promises but no test used to reach."""

    def cli_module(self):
        sys.path.insert(0, str(STAGING / "tools"))
        try:
            import use_relation_h005 as cli
        finally:
            sys.path.pop(0)
        return cli

    def test_a_mapping_error_is_exit_three(self):
        cli = self.cli_module()
        with tempfile.TemporaryDirectory(prefix="use-relation-exit3-") as directory:
            original = cli.build_use_table

            def boom(*args, **kwargs):
                raise MappingError("EMPTY_SCOPE")

            cli.build_use_table = boom
            try:
                with contextlib.redirect_stderr(io.StringIO()) as captured:
                    code = cli.main([str(OCCURRENCE), str(Path(directory) / "out")])
            finally:
                cli.build_use_table = original
            self.assertIn("BUILD_FAILED", captured.getvalue())
            self.assertEqual(code, cli.EXIT_BUILD)
            self.assertFalse((Path(directory) / "out").exists())

    def test_an_oserror_while_writing_is_exit_four_not_a_traceback(self):
        cli = self.cli_module()
        with tempfile.TemporaryDirectory(prefix="use-relation-exit4-") as directory:
            original = cli.write_use_table

            def boom(*args, **kwargs):
                raise OSError(28, "No space left on device")

            cli.write_use_table = boom
            try:
                with contextlib.redirect_stderr(io.StringIO()) as captured:
                    code = cli.main([str(OCCURRENCE), str(Path(directory) / "out"),
                                     "--arm", "mini_fcl", "--cycle", "1"])
            finally:
                cli.write_use_table = original
            self.assertIn("OUT_DIR_UNWRITABLE", captured.getvalue())
            self.assertEqual(code, cli.EXIT_OUT_DIR)
            self.assertFalse((Path(directory) / "out").exists())


class HashSeedDeterminismTests(unittest.TestCase):
    def test_two_pinned_hash_seeds_write_byte_identical_files(self):
        digests = []
        with tempfile.TemporaryDirectory(prefix="use-relation-seed-") as directory:
            for seed in HASH_SEEDS:
                out = Path(directory) / ("seed-" + seed)
                result = _run_cli([str(OCCURRENCE), str(out), "--arm", "mini_fcl",
                                   "--cycle", "1"], hash_seed=seed)
                self.assertEqual(result.returncode, 0, msg=result.stderr)
                digests.append((
                    hashlib.sha256((out / "USE_TABLE.md").read_bytes()).hexdigest(),
                    hashlib.sha256((out / "use_table.json").read_bytes()).hexdigest(),
                ))
        self.assertEqual(digests[0], digests[1],
                         "output moved between two PYTHONHASHSEED values")


class RecordsArrayLocationTests(unittest.TestCase):
    def test_a_prose_field_that_looks_like_the_records_array_does_not_mislocate_it(self):
        document = {
            "schema": "h005.fcl1.v1",
            "note": 'the string \'"records": [\' appears here in prose',
            "records": [{"id": "k1", "type": "claim", "text": "x"}],
        }
        commitments = json.dumps(document, indent=2)
        spans = record_source_spans(commitments, document)
        self.assertEqual(len(spans), 1)
        self.assertEqual(json.loads(commitments[spans[0][0]:spans[0][1]]),
                         document["records"][0])

    def test_a_commitments_string_with_no_top_level_records_array_is_refused(self):
        document = {"schema": "h005.fcl1.v1"}
        with self.assertRaises(MappingError) as raised:
            record_source_spans(json.dumps(document), document)
        self.assertIn("RECORDS_ARRAY_NOT_LOCATABLE", str(raised.exception))

    def test_spans_are_code_point_offsets_not_utf8_byte_offsets(self):
        # daily/mini_fcl/cycle01/carry carries an en dash; the two kinds of
        # offset differ after it, and the published spans are the code point
        # ones. This is the column whose whole purpose is third-party checking.
        table = build_use_table(OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES)
        checked = 0
        for row in table.rows:
            for key, span, verbatim in (
                ("referring", row.referring_record_source_span,
                 row.referring_record_verbatim),
                ("target", row.target_record_source_span, row.target_record_verbatim),
            ):
                if span is None or verbatim is None:
                    continue
                self.assertEqual(len(verbatim), span[1] - span[0],
                                 msg="%s span is not a code point span" % key)
                checked += 1
        self.assertGreater(checked, 0)
        self.assertIn("code point offsets into the decoded `commitments` string",
                      table.to_markdown())


class PublishedCaveatTests(unittest.TestCase):
    """The two caveats must travel with the artifact root actually reads."""

    @classmethod
    def setUpClass(cls):
        cls.rendered = build_use_table(
            OCCURRENCE, arms=GOLDEN_ARMS, cycles=GOLDEN_CYCLES).to_markdown()

    def test_the_blank_cell_caveat_is_in_the_markdown(self):
        self.assertIn("unread row", self.rendered)
        self.assertIn("not a reading of `unresolved`", self.rendered)

    def test_the_finding_aid_caveat_is_in_the_markdown(self):
        self.assertIn("finding aid", self.rendered)
        self.assertIn("root may cite any passage", self.rendered.replace("**", ""))

    def test_the_banner_does_not_read_as_a_closed_search_space(self):
        self.assertNotIn("beside the passages a root reader needs", self.rendered)

    def test_both_regexes_are_printed_verbatim(self):
        from minireason.use_relation_h005 import SENTENCE_BOUNDARY_RE, TOKEN_RE

        self.assertIn("`" + TOKEN_RE.pattern + "`", self.rendered)
        self.assertIn("`" + SENTENCE_BOUNDARY_RE.pattern + "`", self.rendered)

    def test_the_root_vocabulary_is_offered_not_imposed(self):
        self.assertIn("suggested vocabulary", self.rendered)
        self.assertIn("may write a reading this vocabulary does not cover",
                      self.rendered)
        self.assertNotIn("may take exactly one of", self.rendered)
        self.assertIn("The instrument never selects one.", self.rendered)



if __name__ == "__main__":
    unittest.main()
