"""W1-SURFACE: the resolvable surface M, its offset map, and G2(a)/G3.

Every class below is named after one clause of the W1-SURFACE acceptance list
in the wave plan, and every test in it is one reading of that clause.  The
material is **published bytes**: the ``use_relation_h005`` tables under
``experiments/analyses/F001-fork5-multifamily-2026-09-14/`` and the H005
occurrence trees under ``experiments/diagnostics/F001-fork5-multifamily/`` that
those tables pin by sha256.  Nothing here is a hand-written imitation of a use
row except where a *refusal* is under test, and nothing here writes anything.
"""
from __future__ import annotations

import builtins
import hashlib
import json
import os
import re
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from minireason import use_relation_h005 as instrument
from minireason.graph_import_h005 import Coordinate, occurrence_path
from minireason.loop import surface as S
from minireason.loop import types as loop_types
from minireason.loop.contracts import FORBIDDEN_KEYS

REPO = Path(__file__).resolve().parents[2]
ANALYSES = REPO / "experiments" / "analyses" / "F001-fork5-multifamily-2026-09-14"
OCCURRENCES = REPO / "experiments" / "diagnostics" / "F001-fork5-multifamily"

#: The three published occurrences whose tables carry rows.  ``07`` is the
#: artifact-grain occurrence: every one of its rows resolves a ref that names a
#: contribution rather than a record, so no row has a target record.
POPULATED = ("01", "05", "07")


def table(occurrence: str) -> dict:
    return json.loads((ANALYSES / f"occurrence-{occurrence}" / "use-table" / "use_table.json").read_text(encoding="utf-8"))


def rows(occurrence: str) -> list[dict]:
    return table(occurrence)["rows"]


def artifact(occurrence: str, relative: str) -> dict:
    return json.loads((OCCURRENCES / f"occurrence-{occurrence}" / relative).read_text(encoding="utf-8"))


def every_row() -> list[tuple[str, int, dict]]:
    return [(o, i, row) for o in POPULATED for i, row in enumerate(rows(o))]


def as_use_row(row: dict) -> instrument.UseRow:
    """The published row as the instrument's own frozen :class:`UseRow`."""

    fields = dict(row)
    fields["referring_body_passages"] = tuple(
        instrument.Passage(
            start=p["start"],
            end=p["end"],
            text=p["text"],
            distinctive_tokens_present=tuple(p["distinctive_tokens_present"]),
        )
        for p in row["referring_body_passages"]
    )
    fields["resolver_notes"] = tuple(
        instrument.ResolverNote(code=n["code"], reason=n["reason"])
        for n in row["resolver_notes"]
    )
    for name in ("referring_record_source_span", "target_record_source_span"):
        if fields[name] is not None:
            fields[name] = tuple(fields[name])
    return instrument.UseRow(**fields)


#: One row of published bytes used as the worked example throughout: an
#: objection record targeting a claim record, six listed body passages, an em
#: dash in the first of them.
EXAMPLE = ("01", 0)
#: A phrase that occurs in the target record's ``grounds`` **and** in a listed
#: body passage of the same row: real, published, non-unique material.
TWICE = "agreeing and later disagreeing about what the agreement meant"
#: A phrase of the referring record that occurs exactly once in that surface.
ONCE = "disputes as mainly about"


def example() -> S.Surface:
    return S.build_surface(rows(EXAMPLE[0])[EXAMPLE[1]])


# ---------------------------------------------------------------------------


class AQuoteOccurringExactlyOnceResolvesToTheCorrectOccurrenceFileSpan(unittest.TestCase):
    """Acceptance 1."""

    def test_a_target_record_quote_resolves_to_its_span_in_the_target_artifact(self):
        row = rows("01")[0]
        quote = row["target_record_verbatim"][:80]
        offset = S.resolve_unique(S.build_surface(row), quote)
        self.assertEqual(offset.side, S.SIDE_TARGET_RECORD)
        self.assertEqual(
            offset.occurrence_path, "artifacts/daily/mini_fcl/cycle01/account.json"
        )
        field = artifact("01", offset.occurrence_path)[offset.source_field]
        self.assertEqual(field[offset.file_start : offset.file_end], quote)

    def test_a_referring_record_quote_resolves_to_its_span_in_the_referring_artifact(self):
        row = rows("01")[0]
        offset = S.resolve_unique(S.build_surface(row), ONCE)
        self.assertEqual(offset.side, S.SIDE_REFERRING_RECORD)
        self.assertEqual(
            offset.occurrence_path, "artifacts/daily/mini_fcl/cycle01/objection.json"
        )
        field = artifact("01", offset.occurrence_path)[offset.source_field]
        self.assertEqual(field[offset.file_start : offset.file_end], ONCE)

    def test_every_declared_span_of_every_published_row_re_reads_its_own_bytes(self):
        """The whole offset table, over every published row, against the files.

        For each declared span: the surface bytes are the region's text, and
        ``artifact[source_field][file_start:file_end]`` is the same text.  This
        is the acceptance clause taken at full width rather than on one row.
        """

        checked = 0
        for occurrence, _index, row in every_row():
            built = S.build_surface(row)
            for span in built.spans:
                text = built.text[span.start : span.end].decode("utf-8")
                field = artifact(occurrence, span.occurrence_path)[span.source_field]
                self.assertEqual(field[span.file_start : span.file_end], text)
                checked += 1
        self.assertGreater(checked, 200)

    def test_every_body_passage_resolves_where_it_is_unique(self):
        checked = 0
        for occurrence, _index, row in every_row():
            built = S.build_surface(row)
            for span in built.spans:
                if span.side != S.SIDE_REFERRING_BODY_PASSAGE:
                    continue
                text = built.text[span.start : span.end].decode("utf-8")
                if built.count(text) != 1:
                    continue
                offset = S.resolve_unique(built, text)
                self.assertEqual(offset.side, S.SIDE_REFERRING_BODY_PASSAGE)
                self.assertEqual(offset.source_field, S.FIELD_BODY)
                self.assertEqual((offset.file_start, offset.file_end), (span.file_start, span.file_end))
                field = artifact(occurrence, offset.occurrence_path)[S.FIELD_BODY]
                self.assertEqual(field[offset.file_start : offset.file_end], text)
                checked += 1
        self.assertGreater(checked, 100)

    def test_the_occurrence_path_is_the_importers_own_convention(self):
        row = rows("01")[0]
        built = S.build_surface(row)
        expected = occurrence_path(
            Coordinate.from_dict(row["referring_coordinate"]), S.ARTIFACT_CATEGORY
        )
        self.assertEqual(built.spans[0].occurrence_path, expected)
        self.assertTrue((OCCURRENCES / "occurrence-01" / expected).is_file())

    def test_the_occurrence_files_the_spans_name_are_the_bytes_the_table_pinned(self):
        """The table's own ``files_read`` sha256 binds the analysis to the tree."""

        for occurrence in POPULATED:
            pins = {e["path"]: e["sha256"] for e in table(occurrence)["files_read"]}
            for _o, _i, row in [(occurrence, i, r) for i, r in enumerate(rows(occurrence))]:
                for span in S.build_surface(row).spans:
                    self.assertIn(span.occurrence_path, pins)
                    data = (OCCURRENCES / f"occurrence-{occurrence}" / span.occurrence_path).read_bytes()
                    self.assertEqual(hashlib.sha256(data).hexdigest(), pins[span.occurrence_path])

    def test_the_resolved_surface_span_is_the_quote_byte_for_byte(self):
        built = example()
        offset = S.resolve_unique(built, ONCE)
        self.assertEqual(built.text[offset.start : offset.end], ONCE.encode("utf-8"))
        self.assertEqual(offset.length, len(ONCE.encode("utf-8")))

    def test_the_transcript_entry_is_the_digest_beside_the_offset(self):
        built = example()
        offset = S.resolve_unique(built, ONCE)
        entry = {"surface": built.digest, **offset.as_dict()}
        self.assertEqual(
            sorted(entry),
            [
                "end",
                "file_end",
                "file_start",
                "occurrence_path",
                "side",
                "source_field",
                "start",
                "surface",
            ],
        )
        self.assertEqual(entry["surface"], hashlib.sha256(built.text).hexdigest())


class ZeroOrMultipleOccurrencesReturnNone(unittest.TestCase):
    """Acceptance 2, and G2(a)'s block code."""

    def test_a_quote_absent_from_the_material_returns_none(self):
        built = example()
        self.assertEqual(built.count("a lexical overlap is not evidence of use"), 0)
        self.assertIsNone(S.resolve_unique(built, "a lexical overlap is not evidence of use"))

    def test_a_published_phrase_occurring_twice_returns_none(self):
        built = example()
        self.assertEqual(built.count(TWICE), 2)
        self.assertIsNone(S.resolve_unique(built, TWICE))

    def test_the_two_occurrences_are_the_target_record_and_a_body_passage(self):
        built = example()
        sides = [built.span_at(start, start + len(TWICE.encode("utf-8"))).side
                 for start in built.occurrences(TWICE)]
        self.assertEqual(sides, [S.SIDE_TARGET_RECORD, S.SIDE_REFERRING_BODY_PASSAGE])

    def test_count_distinguishes_the_two_refusals_for_the_transcript(self):
        built = example()
        self.assertEqual(built.count("no such words anywhere in this row"), 0)
        self.assertEqual(built.count(TWICE), 2)
        for quote in ("no such words anywhere in this row", TWICE):
            self.assertIsNone(S.resolve_unique(built, quote))

    def test_an_empty_quote_has_no_occurrences_and_returns_none(self):
        built = example()
        for empty in ("", b""):
            self.assertEqual(built.count(empty), 0)
            self.assertIsNone(S.resolve_unique(built, empty))

    def test_overlapping_occurrences_are_counted_where_bytes_count_would_not(self):
        built = S.build_surface(_synthetic_row("aaa"))
        self.assertEqual(built.text.count(b"aa"), 1)
        self.assertEqual(built.count("aa"), 2)
        self.assertIsNone(S.resolve_unique(built, "aa"))

    def test_bytes_count_agrees_with_this_count_wherever_it_returns_one(self):
        for _occurrence, _index, row in every_row():
            built = S.build_surface(row)
            for span in built.spans:
                text = built.text[span.start : span.end]
                if built.text.count(text) == 1:
                    self.assertEqual(built.count(text), 1)

    def test_the_refusal_carries_the_designs_reason_code(self):
        self.assertEqual(S.REFERENTIAL_INTEGRITY_BLOCK, "blocked:referential-integrity")
        self.assertIn(S.REFERENTIAL_INTEGRITY_BLOCK, loop_types.BLOCK_CODES)

    def test_a_quote_is_matched_by_exact_bytes_and_is_never_repaired(self):
        built = example()
        for mangled in (
            ONCE.upper(),
            ONCE.replace(" ", "  "),
            ONCE.replace(" ", "\n"),
            ONCE + " !!",
            ONCE.strip().capitalize(),
        ):
            self.assertNotEqual(mangled, ONCE)
            self.assertIsNone(S.resolve_unique(built, mangled), mangled)


class BodyPassagesAreInsideTheResolvableSurfaceAndFramingIsNot(unittest.TestCase):
    """Acceptance 3, and G3's block code."""

    def test_every_listed_body_passage_is_a_declared_span_of_the_surface(self):
        for _occurrence, _index, row in every_row():
            built = S.build_surface(row)
            passages = [s for s in built.spans if s.side == S.SIDE_REFERRING_BODY_PASSAGE]
            self.assertEqual(len(passages), len(row["referring_body_passages"]))
            for span, published in zip(passages, row["referring_body_passages"]):
                self.assertEqual(built.text[span.start : span.end].decode("utf-8"), published["text"])
                self.assertTrue(S.within_declared_span(built, S.resolve_unique(built, published["text"]))
                                or built.count(published["text"]) != 1)

    def test_a_quote_of_a_label_line_resolves_uniquely_but_is_not_within_a_declared_span(self):
        built = example()
        label = "--- target record: daily/mini_fcl/cycle01/account#c1 ---"
        self.assertEqual(built.count(label), 1)
        offset = S.resolve_unique(built, label)
        self.assertIsNotNone(offset)
        self.assertEqual(offset.side, S.SIDE_FRAMING)
        self.assertFalse(S.within_declared_span(built, offset))

    def test_a_quote_crossing_a_region_boundary_is_framing(self):
        built = example()
        first, second = built.spans[0], built.spans[1]
        crossing = built.text[first.end - 12 : second.start + 12]
        offset = S.resolve_unique(built, crossing)
        self.assertEqual(offset.side, S.SIDE_FRAMING)
        self.assertFalse(S.within_declared_span(built, offset))

    def test_a_framing_offset_carries_no_occurrence_file_span(self):
        built = example()
        offset = S.resolve_unique(built, S.LABEL_OPEN + "referring record: ")
        self.assertEqual(offset.side, S.SIDE_FRAMING)
        self.assertIsNone(offset.occurrence_path)
        self.assertIsNone(offset.file_start)
        self.assertIsNone(offset.file_end)
        self.assertIsNone(offset.source_field)
        self.assertTrue(offset.is_framing)

    def test_the_framing_bytes_are_exactly_the_labels_and_the_separators(self):
        """Reconstructed from the row, not from the offset table it checks."""

        row = rows(EXAMPLE[0])[EXAMPLE[1]]
        built = S.build_surface(row)
        key = row["referring_coordinate_key"]
        expected_regions = [
            (S.SIDE_REFERRING_RECORD, row["referring_record_verbatim"],
             f"referring record: {key}#{row['referring_record_id']}"),
            (S.SIDE_TARGET_RECORD, row["target_record_verbatim"],
             f"target record: {row['target_coordinate_key']}#{row['target_record_id']}"),
        ] + [
            (S.SIDE_REFERRING_BODY_PASSAGE, passage["text"],
             f"referring body passage {ordinal}: {key}")
            for ordinal, passage in enumerate(row["referring_body_passages"], start=1)
        ]
        expected_framing = b"".join(
            (S.BLOCK_SEPARATOR if index else b"")
            + f"{S.LABEL_OPEN}{label}{S.LABEL_CLOSE}".encode("utf-8")
            + S.LABEL_TERMINATOR
            for index, (_side, _text, label) in enumerate(expected_regions)
        )
        covered = {i for span in built.spans for i in range(span.start, span.end)}
        self.assertEqual(
            bytes(b for i, b in enumerate(built.text) if i not in covered), expected_framing
        )
        self.assertEqual(
            b"".join(built.text[s.start : s.end] for s in built.spans),
            "".join(text for _side, text, _label in expected_regions).encode("utf-8"),
        )
        for index in range(len(built.text)):
            side = next(
                (s.side for s in built.spans if s.start <= index < s.end), S.SIDE_FRAMING
            )
            self.assertEqual(
                S.within_declared_span(built, S.Offset(index, index + 1, side, None, None, None)),
                index in covered,
            )

    def test_material_that_never_enters_the_surface_is_g2_and_not_g3(self):
        """The pack's banner, instruction and resolver notes are not in M at all.

        A quote of one of them occurs zero times, so it is
        ``blocked:referential-integrity``.  ``blocked:operative-target`` is
        reserved for a span that *is* in the surface and is still not a reading
        of the material.
        """

        built = example()
        for framing in (
            instrument.USE_RELATION_BANNER[:60],
            instrument.PROSE_SURFACE_NOTE,
            instrument.NO_OVERLAP_NOTE,
            rows("01")[0]["overlap_subject"],
        ):
            self.assertEqual(built.count(framing), 0, framing)
            self.assertIsNone(S.resolve_unique(built, framing))

    def test_the_refusal_carries_the_designs_reason_code(self):
        self.assertEqual(S.OPERATIVE_TARGET_BLOCK, "blocked:operative-target")
        self.assertIn(S.OPERATIVE_TARGET_BLOCK, loop_types.BLOCK_CODES)

    def test_within_declared_span_refuses_a_forged_side(self):
        built = example()
        honest = S.resolve_unique(built, ONCE)
        self.assertTrue(S.within_declared_span(built, honest))
        forged = S.Offset(
            honest.start, honest.end, S.SIDE_TARGET_RECORD, honest.occurrence_path,
            honest.file_start, honest.file_end,
        )
        self.assertFalse(S.within_declared_span(built, forged))

    def test_within_declared_span_is_false_for_none_and_for_an_empty_span(self):
        built = example()
        self.assertFalse(S.within_declared_span(built, None))
        self.assertFalse(
            S.within_declared_span(
                built, S.Offset(10, 10, S.SIDE_REFERRING_RECORD, "x", 0, 0)
            )
        )
        with self.assertRaises(S.SurfaceInvalid):
            S.within_declared_span(built, "not an offset")

    def test_the_declared_spans_are_disjoint_and_in_surface_order(self):
        for _occurrence, _index, row in every_row():
            built = S.build_surface(row)
            cursor = -1
            for span in built.spans:
                self.assertGreater(span.start, cursor)
                self.assertGreater(span.end, span.start)
                cursor = span.end
            self.assertLessEqual(cursor, len(built.text))


class OffsetsAreByteOffsetsAndAreDocumentedAsSuchForNonAscii(unittest.TestCase):
    """Acceptance 4."""

    def test_a_quote_after_an_em_dash_has_a_byte_offset_past_its_character_offset(self):
        built = example()
        quote = "who is carrying what"
        offset = S.resolve_unique(built, quote)
        self.assertIsNotNone(offset)
        prefix = built.text[: offset.start]
        self.assertGreater(len(prefix), len(prefix.decode("utf-8")))
        self.assertEqual(built.text[offset.start : offset.end].decode("utf-8"), quote)

    def test_the_file_span_of_a_quote_behind_non_ascii_is_code_points_not_bytes(self):
        """occurrence-05 row 0: non-ascii before the quote in the surface *and*
        before it in the body field, so the two coordinate systems disagree in
        both directions at once."""

        row = rows("05")[0]
        built = S.build_surface(row)
        span = [s for s in built.spans if s.side == S.SIDE_REFERRING_BODY_PASSAGE][1]
        text = built.text[span.start : span.end].decode("utf-8")
        field = artifact("05", span.occurrence_path)[S.FIELD_BODY]
        self.assertTrue(any(ord(c) > 127 for c in field[: span.file_start]))
        self.assertTrue(any(b > 127 for b in built.text[: span.start]))
        self.assertEqual(field[span.file_start : span.file_end], text)
        # the byte offset of the same point is strictly larger than the code
        # point offset, which is why the two are never interchanged.
        self.assertGreater(span.start, len(built.text[: span.start].decode("utf-8")))
        self.assertGreater(
            len(field[: span.file_start].encode("utf-8")), span.file_start
        )

    def test_a_non_ascii_quote_resolves_on_character_boundaries(self):
        built = example()
        quote = "naming — who is carrying what"
        offset = S.resolve_unique(built, quote)
        self.assertIsNotNone(offset)
        self.assertEqual(built.text[offset.start : offset.end].decode("utf-8"), quote)
        field = artifact("01", offset.occurrence_path)[offset.source_field]
        self.assertEqual(field[offset.file_start : offset.file_end], quote)

    def test_a_continuation_byte_run_never_matches_mid_character(self):
        built = S.build_surface(_synthetic_row("———"))
        tail = "—".encode("utf-8")[1:]
        self.assertIn(tail, built.text)
        self.assertEqual(built.count(tail), 0)
        self.assertIsNone(S.resolve_unique(built, tail))

    def test_the_module_documents_both_coordinate_systems(self):
        doc = S.__doc__
        self.assertIn("utf-8 byte offsets", doc)
        self.assertIn("code-point offsets", doc)
        self.assertIn("*not* utf-8 byte offsets", doc)
        self.assertIn("escaped", doc)
        for name in ("start", "end", "file_start", "file_end"):
            self.assertIn(name, S.Offset.__doc__)


class SurfaceBytesAreDeterministic(unittest.TestCase):
    """Acceptance 5, and "frozen, content-addressed, never paraphrased"."""

    def test_two_builds_of_one_row_are_byte_identical_and_share_a_digest(self):
        for _occurrence, _index, row in every_row():
            first, second = S.build_surface(row), S.build_surface(row)
            self.assertEqual(first.text, second.text)
            self.assertEqual(first.digest, second.digest)
            self.assertEqual([s.as_dict() for s in first.spans], [s.as_dict() for s in second.spans])

    def test_the_instruments_own_use_row_builds_the_same_bytes_as_its_mapping(self):
        for occurrence, _index, row in every_row():
            self.assertEqual(
                S.build_surface(as_use_row(row)).text, S.build_surface(row).text, occurrence
            )

    def test_the_digest_is_sha256_of_the_text(self):
        built = example()
        self.assertEqual(built.digest, hashlib.sha256(built.text).hexdigest())
        self.assertEqual(len(built.digest), 64)

    def test_a_one_character_change_to_the_material_changes_the_digest(self):
        row = json.loads(json.dumps(rows("01")[0]))
        before = S.build_surface(row).digest
        text = row["referring_body_passages"][0]["text"]
        row["referring_body_passages"][0]["text"] = text[:-1] + ("x" if text[-1] != "x" else "y")
        self.assertNotEqual(S.build_surface(row).digest, before)

    def test_building_does_not_mutate_the_row(self):
        row = rows("01")[0]
        before = json.dumps(row, sort_keys=True)
        S.build_surface(row)
        self.assertEqual(json.dumps(row, sort_keys=True), before)

    def test_the_region_order_is_referring_then_target_then_the_instruments_passages(self):
        built = example()
        self.assertEqual(
            [s.side for s in built.spans],
            [S.SIDE_REFERRING_RECORD, S.SIDE_TARGET_RECORD] + [S.SIDE_REFERRING_BODY_PASSAGE] * 6,
        )
        self.assertEqual([s.ordinal for s in built.spans if s.ordinal], [1, 2, 3, 4, 5, 6])

    def test_the_surface_the_offset_and_the_span_are_frozen(self):
        built = example()
        offset = S.resolve_unique(built, ONCE)
        for record, name, value in (
            (built, "text", b""),
            (offset, "start", 0),
            (built.spans[0], "side", "x"),
        ):
            with self.assertRaises(FrozenInstanceError):
                setattr(record, name, value)

    def test_the_text_is_bytes_and_the_decoded_form_is_a_string(self):
        built = example()
        self.assertIsInstance(built.text, bytes)
        self.assertIsInstance(built.decoded, str)
        self.assertEqual(built.decoded.encode("utf-8"), built.text)
        self.assertEqual(len(built), len(built.text))


class NothingIsWrittenUnderTheOccurrence(unittest.TestCase):
    """Acceptance 6."""

    def test_building_every_published_surface_leaves_the_occurrence_bytes_unchanged(self):
        watched = sorted(
            p for occurrence in POPULATED
            for p in (OCCURRENCES / f"occurrence-{occurrence}").rglob("*")
            if p.is_file() and p.suffix == ".json" and p.parent.name.startswith("cycle")
        )
        self.assertGreater(len(watched), 20)

        def snapshot() -> list[tuple[str, int, int, str]]:
            return [
                (
                    str(p.relative_to(REPO)),
                    p.stat().st_size,
                    p.stat().st_mtime_ns,
                    hashlib.sha256(p.read_bytes()).hexdigest(),
                )
                for p in watched
            ]

        before = snapshot()
        for _occurrence, _index, row in every_row():
            built = S.build_surface(row)
            S.resolve_unique(built, ONCE)
            built.as_dict()
        self.assertEqual(snapshot(), before)

    def test_building_and_resolving_open_no_file_at_all(self):
        row = rows("01")[0]
        use_row = as_use_row(row)
        real_open, real_os_open = builtins.open, os.open

        def refuse(*args, **kwargs):  # pragma: no cover - the point is that it is not hit
            raise AssertionError("surface.py opened a file")

        builtins.open, os.open = refuse, refuse
        try:
            built = S.build_surface(use_row)
            offset = S.resolve_unique(built, ONCE)
            S.within_declared_span(built, offset)
            built.as_dict()
            built.digest
        finally:
            builtins.open, os.open = real_open, real_os_open
        self.assertEqual(offset.side, S.SIDE_REFERRING_RECORD)

    def test_the_module_calls_no_filesystem_function(self):
        """Read the module's own syntax tree, not its prose."""

        import ast

        tree = ast.parse((REPO / "src" / "minireason" / "loop" / "surface.py").read_text(encoding="utf-8"))
        called = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                called.add(func.id if isinstance(func, ast.Name) else getattr(func, "attr", ""))
        forbidden = {
            "open", "write", "writelines", "write_text", "write_bytes", "mkdir",
            "makedirs", "unlink", "rename", "remove", "read_text", "read_bytes",
            "rmtree", "touch", "chmod",
        }
        self.assertEqual(called & forbidden, set())
        imported = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        } | {
            node.module.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        }
        self.assertEqual(imported & {"os", "io", "pathlib", "shutil", "tempfile"}, set())


class TheRowsTheSurfaceRefuses(unittest.TestCase):
    """The three refusals, and the codes they carry."""

    def test_a_span_whose_length_contradicts_its_text_is_refused(self):
        row = json.loads(json.dumps(rows("01")[0]))
        row["referring_record_source_span"] = [31, 600]
        with self.assertRaises(S.SurfaceInvalid) as caught:
            S.build_surface(row)
        self.assertEqual(caught.exception.code, "SURFACE_SPAN_DISAGREES")

    def test_a_passage_span_that_contradicts_its_text_is_refused(self):
        row = json.loads(json.dumps(rows("01")[0]))
        row["referring_body_passages"][0]["end"] += 1
        with self.assertRaises(S.SurfaceInvalid) as caught:
            S.build_surface(row)
        self.assertEqual(caught.exception.code, "SURFACE_SPAN_DISAGREES")

    def test_a_coordinate_that_is_not_its_own_key_is_refused(self):
        row = json.loads(json.dumps(rows("01")[0]))
        row["referring_coordinate_key"] = "daily/mini_fcl/cycle01/account"
        with self.assertRaises(S.SurfaceInvalid) as caught:
            S.build_surface(row)
        self.assertEqual(caught.exception.code, "SURFACE_ROW_MALFORMED")

    def test_a_coordinate_that_could_escape_the_occurrence_is_refused(self):
        row = json.loads(json.dumps(rows("01")[0]))
        row["referring_coordinate"]["node"] = "../../etc/passwd"
        with self.assertRaises(S.SurfaceInvalid) as caught:
            S.build_surface(row)
        self.assertEqual(caught.exception.code, "SURFACE_ROW_MALFORMED")

    def test_a_row_with_no_quotable_region_is_refused(self):
        row = json.loads(json.dumps(rows("07")[0]))
        row["referring_record_verbatim"] = None
        row["referring_record_source_span"] = None
        row["referring_body_passages"] = []
        with self.assertRaises(S.SurfaceInvalid) as caught:
            S.build_surface(row)
        self.assertEqual(caught.exception.code, "SURFACE_NO_MATERIAL")

    def test_a_missing_field_and_a_wrong_type_are_refused(self):
        for mutate in (
            lambda r: r.pop("ref_field"),
            lambda r: r.__setitem__("ref_grain", 3),
            lambda r: r.__setitem__("referring_body_passages", "not a list"),
            lambda r: r.__setitem__("referring_record_verbatim", ""),
        ):
            row = json.loads(json.dumps(rows("01")[0]))
            mutate(row)
            with self.assertRaises(S.SurfaceInvalid) as caught:
                S.build_surface(row)
            self.assertEqual(caught.exception.code, "SURFACE_ROW_MALFORMED")

    def test_something_that_is_not_a_use_row_is_refused(self):
        for thing in (None, 7, "a row", ["a row"]):
            with self.assertRaises(S.SurfaceInvalid):
                S.build_surface(thing)

    def test_resolve_unique_and_within_declared_span_refuse_a_non_surface(self):
        with self.assertRaises(S.SurfaceInvalid):
            S.resolve_unique("not a surface", ONCE)
        with self.assertRaises(S.SurfaceInvalid):
            S.within_declared_span("not a surface", None)

    def test_a_quote_that_is_neither_text_nor_bytes_is_refused(self):
        with self.assertRaises(S.SurfaceInvalid):
            S.resolve_unique(example(), 12)

    def test_surface_invalid_is_a_loop_error_and_a_value_error(self):
        error = S.SurfaceInvalid("SURFACE_NO_MATERIAL", "why")
        self.assertIsInstance(error, loop_types.LoopError)
        self.assertIsInstance(error, ValueError)
        self.assertEqual(error.code, "SURFACE_NO_MATERIAL")
        self.assertEqual(error.detail, "why")

    def test_every_code_the_module_raises_is_declared(self):
        source = (REPO / "src" / "minireason" / "loop" / "surface.py").read_text(encoding="utf-8")
        raised = set(re.findall(r'SurfaceInvalid\(\s*"([A-Z][A-Z0-9_]*)"', source))
        self.assertTrue(raised)
        for code in raised:
            self.assertTrue(
                code in S.NEW_CODES or loop_types.is_failure_code(code),
                f"{code} is neither in NEW_CODES nor in types.FAILURE_CODES",
            )

    def test_new_codes_are_declared_upstream_and_each_carries_a_reason(self):
        """Folded into ``types.FAILURE_CODES`` by the wave-1 integrator (O9).
        The reason stays here, beside the code that needs it."""

        for code, reason in S.NEW_CODES.items():
            self.assertRegex(code, r"\A[A-Z][A-Z0-9_]*\Z")
            self.assertIn(code, loop_types.FAILURE_CODES)
            self.assertGreater(len(reason.split()), 6)


class TheArtifactGrainRowHasNoTargetRegion(unittest.TestCase):
    """A ref naming a contribution rather than a record."""

    def test_every_occurrence_07_row_carries_no_target_record_span(self):
        for row in rows("07"):
            self.assertEqual(row["ref_grain"], "artifact")
            self.assertIsNone(row["target_record_verbatim"])
            built = S.build_surface(row)
            self.assertEqual([s.side for s in built.spans if s.side == S.SIDE_TARGET_RECORD], [])
            self.assertIsNone(built.target_record_id)
            self.assertEqual(built.target_coordinate_key, "daily/mini_fcl/cycle01/account")

    def test_a_row_with_no_body_passages_still_builds_from_its_records(self):
        row = next(r for r in rows("01") if not r["referring_body_passages"])
        built = S.build_surface(row)
        self.assertEqual(
            [s.side for s in built.spans], [S.SIDE_REFERRING_RECORD, S.SIDE_TARGET_RECORD]
        )


class TheEmittedSurfaceRecord(unittest.TestCase):
    """What goes into the transcript, and G12 over it."""

    def test_the_record_carries_the_digest_and_the_offset_table_and_no_second_copy(self):
        built = example()
        record = built.as_dict()
        self.assertEqual(record["schema"], S.SURFACE_SCHEMA)
        self.assertEqual(record["digest"], built.digest)
        self.assertEqual(record["bytes"], len(built.text))
        self.assertEqual(len(record["spans"]), len(built.spans))
        self.assertNotIn("text", record)
        self.assertNotIn("decoded", record)

    def test_the_record_carries_no_scoring_key_anywhere(self):
        record = example().as_dict()

        def keys(value, out):
            if isinstance(value, dict):
                for k, v in value.items():
                    out.add(str(k).lower())
                    keys(v, out)
            elif isinstance(value, list):
                for v in value:
                    keys(v, out)
            return out

        self.assertEqual(keys(record, set()) & set(FORBIDDEN_KEYS), set())

    def test_the_record_names_no_relation_mark_status_or_label(self):
        record = json.dumps(example().as_dict()).lower()
        for token in ("relation", "\"mark\"", "sustained", "status", "label", "att", "dep"):
            self.assertNotIn(token, record, token)

    def test_the_record_is_json_serialisable_and_stable(self):
        built = example()
        self.assertEqual(json.dumps(built.as_dict(), sort_keys=True),
                         json.dumps(S.build_surface(rows(EXAMPLE[0])[EXAMPLE[1]]).as_dict(), sort_keys=True))


class TheModuleContract(unittest.TestCase):
    """The wave plan's public interface, spelled as the plan spells it."""

    def test_the_public_interface_is_present(self):
        for name in (
            "build_surface", "Surface", "Offset", "resolve_unique", "within_declared_span",
        ):
            self.assertIn(name, S.__all__)
            self.assertTrue(hasattr(S, name))
        for name in ("text", "spans"):
            self.assertIn(name, S.Surface.__dataclass_fields__, name)
        self.assertIsInstance(S.Surface.__dict__["digest"], property)
        self.assertEqual(
            [f for f in S.Offset.__dataclass_fields__],
            ["start", "end", "side", "occurrence_path", "file_start", "file_end"],
        )

    def test_the_docstring_states_purpose_design_section_and_deviations(self):
        doc = S.__doc__
        self.assertIn("W1-SURFACE", doc)
        self.assertIn("G2", doc)
        self.assertIn("G3", doc)
        self.assertIn("Deviations from the wave-plan interface", doc)

    def test_the_module_imports_its_vocabularies_rather_than_retyping_them(self):
        self.assertEqual(S.REFERENTIAL_INTEGRITY_BLOCK, loop_types.block_code("referential-integrity"))
        self.assertEqual(S.OPERATIVE_TARGET_BLOCK, loop_types.block_code("operative-target"))
        self.assertEqual(S.ARTIFACT_CATEGORY, "artifacts")
        self.assertEqual(set(S.SOURCE_FIELDS), set(S.DECLARED_SIDES))
        self.assertNotIn(S.SIDE_FRAMING, S.DECLARED_SIDES)
        self.assertEqual(S.SIDES, (*S.DECLARED_SIDES, S.SIDE_FRAMING))

    def test_the_module_is_annotated(self):
        for name in ("build_surface", "resolve_unique", "within_declared_span"):
            self.assertTrue(getattr(S, name).__annotations__, name)


# ---------------------------------------------------------------------------
# synthetic rows - used only where the property under test needs bytes no
# published occurrence happens to carry (an overlapping repeat, a lone
# continuation byte).  Everything else in this file is published material.
# ---------------------------------------------------------------------------


def _synthetic_row(text: str) -> dict:
    return {
        "referring_coordinate": {"problem": "daily", "arm": "mini_fcl", "cycle": 1, "node": "objection"},
        "referring_coordinate_key": "daily/mini_fcl/cycle01/objection",
        "referring_record_id": "o1",
        "referring_record_verbatim": text,
        "referring_record_source_span": [0, len(text)],
        "ref_field": "target",
        "ref_verbatim": "p.objection.0#c1",
        "ref_grain": "record",
        "target_coordinate": {"problem": "daily", "arm": "mini_fcl", "cycle": 1, "node": "account"},
        "target_coordinate_key": "daily/mini_fcl/cycle01/account",
        "target_record_id": None,
        "target_record_verbatim": None,
        "target_record_source_span": None,
        "referring_body_passages": [],
    }



if __name__ == "__main__":  # pragma: no cover
    unittest.main()
