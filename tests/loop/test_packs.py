"""W2-PACKS: deterministic pack rendering, the exchange surface, the precedent slice.

Every class below is named after one clause of the W2-PACKS acceptance list in
the wave plan, or after one of the reconciliations the wave-2 brief adds, and
every test in it is one reading of that clause.

The material is **published bytes** wherever a pack needs material: the
``use_relation_h005`` table under
``experiments/analyses/F001-fork5-multifamily-2026-09-14/occurrence-01/`` and the
frozen standard body :data:`minireason.loop.standard.STANDARD_BODY`.  The
contrast sides are :func:`minireason.loop.synthetic.contrast_leg`'s, and the
precedent slice is read out of a real graph that :mod:`minireason.loop.graph`
populated.  Nothing here is a hand-written imitation of published material
except where a *refusal* is under test, and nothing here writes into any
occurrence.

``graph`` and ``obligations`` are imported here and **not** by ``packs``: the
four tokens ``packs`` mirrors are asserted against their owners by a test that
imports both, which is the package's rule for two modules that must agree.
"""
from __future__ import annotations

import ast
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from minireason import use_relation_h005 as instrument
from minireason.loop import contracts as C
from minireason.loop import graph as G
from minireason.loop import obligations as OB
from minireason.loop import packs as P
from minireason.loop import standard as STD
from minireason.loop import surface as S
from minireason.loop import synthetic as SY
from minireason.loop import types as loop_types
from minireason.loop.contracts import ScoringKeyForbidden
from minireason.loop.standard import StandardInvalid
from minireason.loop.types import LoopError

REPO = Path(__file__).resolve().parents[2]
ANALYSES = REPO / "experiments" / "analyses" / "F001-fork5-multifamily-2026-09-14"
MODULE = Path(P.__file__).resolve()


def rows(occurrence: str = "01") -> list[dict]:
    path = ANALYSES / f"occurrence-{occurrence}" / "use-table" / "use_table.json"
    return json.loads(path.read_text(encoding="utf-8"))["rows"]


def published_row() -> dict:
    """The worked example: an objection record juxtaposed with a claim record."""

    return rows("01")[0]


def published_surface() -> S.Surface:
    return S.build_surface(published_row())


#: A phrase of the referring record occurring exactly once in that surface.
ONCE = "disputes as mainly about"


def critic(
    *,
    relation: str = "retains",
    quote: str = ONCE,
    case: str = "The referring record takes up the quoted passage and retains it.",
    outside: str = "",
) -> C.CriticOutput:
    return C.validate(
        "critic",
        {
            "relation": relation,
            "passage_quote": quote,
            "role_bindings": {
                "target": "the target record named by the ref",
                "defect": "none alleged",
                "grounds": "the quoted passage",
                "bearing": "if it does not hold the row stays unresolved",
            },
            "case": case,
            C.OUTSIDE_VOCABULARY_FIELD: outside,
        },
    )


def defender(answer: str = "The juxtaposition establishes no such relation.") -> C.DefenderOutput:
    return C.validate("defender", {"answer": answer, "concedes": False})


def hand_row(
    *,
    referring: str = "the referring record body",
    target: str | None = "the target record body",
) -> dict:
    """A minimal, clearly synthetic use row — only for refusals and for material
    a published occurrence does not contain."""

    coordinate = {"problem": "synth", "arm": "mini_fcl", "cycle": 1, "node": "objection"}
    other = dict(coordinate, node="account")
    row: dict = {
        "referring_coordinate": coordinate,
        "referring_coordinate_key": "synth/mini_fcl/cycle01/objection",
        "referring_record_id": "o1",
        "referring_record_verbatim": referring,
        "referring_record_source_span": [0, len(referring)],
        "ref_field": "mentions",
        "ref_verbatim": "p.account.0#a1",
        "ref_grain": "record",
        "target_coordinate": other,
        "target_coordinate_key": "synth/mini_fcl/cycle01/account",
        "target_record_id": "a1",
        "target_record_verbatim": target,
        "target_record_source_span": None if target is None else [0, len(target)],
        "referring_body_passages": [],
        "resolver_notes": [],
    }
    if target is None:
        row.pop("target_record_source_span")
        row["target_record_verbatim"] = None
    return row


class GraphFixture(unittest.TestCase):
    """One harness on a deterministic clock, with two readings and one appeal."""

    def setUp(self) -> None:
        super().setUp()
        self.tmp = Path(tempfile.mkdtemp(prefix="loop-packs-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.harness = G.open_graph(self.tmp / "graph", clock=G.fixed_clock())
        self.standard = G.register_standard(self.harness, STD.STANDARD_BODY)
        self.material = G.register_material(self.harness, b'{"row_key": "r1"}')
        G.open_cells(
            self.harness, ["r1/c1", "r1/c2", "r1/c3"], material_id=self.material
        )

    def reading(self, cell: str, relation: str, point: str, seat: str = "judge-1"):
        transcript = G.Transcript(
            case="the later record re-deploys the earlier term without qualification",
            answer="the defence disputes that the two terms are the same term at all",
            decisive_point=point,
            checks={"unique_offset": True},
        )
        return G.register_reading(
            self.harness,
            G.ReadingResult(
                key=G.CellKey(cell),
                relation=relation,
                seat=seat,
                transcript=transcript,
                material_id=self.material,
            ),
            self.standard,
        )

    def appeal(self, target: str, ruling_id: str = "APP-001") -> str:
        return G.apply_appeal(
            self.harness,
            G.AppellateRuling(
                ruling_id=ruling_id,
                target=target,
                standard_id=self.standard,
                ground="the relation as read does not bear on the claim it was offered for",
            ),
        )

    def slice_(self, k: int = P.PRECEDENT_K, **kwargs) -> P.PrecedentSlice:
        return P.precedent_slice(self.harness, self.standard, k, **kwargs)


class PackFixture(GraphFixture):
    """A row pack over published bytes, and the three packs built on it."""

    def setUp(self) -> None:
        super().setUp()
        self.row = published_row()
        self.surface = published_surface()
        self.critic = critic()
        self.defender = defender()
        self.row_pack = P.render_row(self.surface, STD.STANDARD_BODY, self.row)

    def defender_pack(self) -> P.Pack:
        return P.render_exchange(self.row_pack, self.critic)

    def judge_pack(self, **kwargs) -> P.Pack:
        kwargs.setdefault("precedents", self.slice_())
        return P.render_exchange(self.row_pack, self.critic, self.defender, **kwargs)

    def marker_pack(self, **kwargs) -> P.Pack:
        leg = SY.contrast_leg()
        replicate = leg["cases"]["case-a"]["replicates"]["rep-1"]
        kwargs.setdefault(
            "sides",
            (
                P.MarkSide("ORIGINAL", replicate["ORIGINAL"]),
                P.MarkSide("CONTROL", replicate["CONTROL"]),
            ),
        )
        return P.render_register(
            "case-a", "T", "original-vs-control", "b" * 64, STD.STANDARD_BODY, **kwargs
        )

    def every_pack(self) -> tuple[P.Pack, ...]:
        judge = self.judge_pack()
        return (
            self.row_pack,
            self.defender_pack(),
            judge,
            self.marker_pack(),
            P.render_paraphrase_request(judge),
        )


# ---------------------------------------------------------------------------
# Acceptance 1
# ---------------------------------------------------------------------------


class IdenticalInputsGiveIdenticalBytes(PackFixture):
    """Acceptance 1.  A pack is a pure deterministic render."""

    def test_two_renders_of_one_row_are_byte_identical(self):
        again = P.render_row(self.surface, STD.STANDARD_BODY, self.row)
        self.assertEqual(again.text, self.row_pack.text)
        self.assertEqual(again.canonical_bytes(), self.row_pack.canonical_bytes())
        self.assertEqual(P.pack_sha(again), P.pack_sha(self.row_pack))

    def test_two_renders_of_one_exchange_are_byte_identical(self):
        for build in (self.defender_pack, self.judge_pack):
            with self.subTest(build=build.__name__):
                self.assertEqual(build().canonical_bytes(), build().canonical_bytes())

    def test_two_renders_of_one_register_pack_are_byte_identical(self):
        self.assertEqual(self.marker_pack().sha, self.marker_pack().sha)

    def test_two_renders_of_one_paraphrase_request_are_byte_identical(self):
        judge = self.judge_pack()
        first = P.render_paraphrase_request(judge)
        second = P.render_paraphrase_request(judge)
        self.assertEqual(first.canonical_bytes(), second.canonical_bytes())

    def test_a_standard_handed_over_as_bytes_text_or_mapping_renders_the_same_pack(self):
        parsed = STD.standard_body(STD.STANDARD_BODY)
        shas = {
            P.render_row(self.surface, body, self.row).sha
            for body in (
                STD.STANDARD_BODY,
                STD.STANDARD_BODY.decode("utf-8"),
                parsed,
            )
        }
        self.assertEqual(len(shas), 1)

    def test_a_different_surface_changes_the_digest(self):
        other = S.build_surface(rows("01")[1])
        self.assertNotEqual(
            P.render_row(other, STD.STANDARD_BODY, rows("01")[1]).sha, self.row_pack.sha
        )

    def test_a_different_presentation_order_changes_the_digest(self):
        declared = self.judge_pack(order=P.ORDER_AS_DECLARED)
        swapped = self.judge_pack(order=P.ORDER_SWAPPED)
        self.assertNotEqual(declared.sha, swapped.sha)

    def test_a_different_precedent_bound_changes_the_digest(self):
        self.reading("r1/c1", "retains", "without qualification")
        wide = P.render_exchange(
            self.row_pack, self.critic, self.defender, precedents=self.slice_(5)
        )
        narrow = P.render_exchange(
            self.row_pack, self.critic, self.defender, precedents=self.slice_(1)
        )
        self.assertNotEqual(wide.sha, narrow.sha)

    def test_the_module_reads_no_clock_and_draws_no_random_number(self):
        """Determinism is structural, not observed: nothing here can vary."""

        tree = ast.parse(MODULE.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        for banned in ("random", "time", "datetime", "os", "secrets", "uuid", "socket"):
            with self.subTest(module=banned):
                self.assertNotIn(banned, imported)

    def test_the_module_opens_no_file_and_writes_nothing(self):
        source = MODULE.read_text(encoding="utf-8")
        for banned in ("open(", "write_text", "write_bytes", "Path("):
            with self.subTest(token=banned):
                self.assertNotIn(banned, source)


# ---------------------------------------------------------------------------
# Acceptance 2
# ---------------------------------------------------------------------------


class NoPackContainsALabelAnAttADepAStatusOrAnotherSeatsOutput(PackFixture):
    """Acceptance 2, at the grain the rule is actually about.

    The rule is structural.  A word-level scan would be the wrong test and would
    fail on the standard's own rubric, whose clause R8 tells a critic in so many
    words that "no reading of any value mints an ``att`` or a ``dep``" — which is
    the opposite of a pack carrying one.
    """

    def test_no_rendered_pack_record_carries_an_adjudication_key(self):
        for pack in self.every_pack():
            with self.subTest(role=pack.role):
                P.assert_no_adjudication_keys(pack.as_dict())

    def test_a_planted_status_key_is_refused_by_name(self):
        with self.assertRaises(P.PackError) as caught:
            P.assert_no_adjudication_keys({"subject": {"status": "accepted"}})
        self.assertEqual(caught.exception.code, P.PACK_ADJUDICATION_KEY)
        self.assertIn("subject/status", caught.exception.detail)

    def test_a_planted_att_or_dep_key_is_refused_at_any_depth(self):
        for key in ("att", "dep", "standing", "cell_state", "refuted"):
            with self.subTest(key=key):
                with self.assertRaises(P.PackError):
                    P.assert_no_adjudication_keys({"a": [{"b": {key: 1}}]})

    def test_every_forbidden_pack_key_is_disjoint_from_every_role_schemas_properties(self):
        """The ban may not collide with what a seat is asked *for*."""

        for role in C.ROLE_NAMES:
            properties = set(C.schema_for(role).get("properties", {}))
            with self.subTest(role=role):
                self.assertEqual(properties & P.FORBIDDEN_PACK_KEYS, set())

    def test_a_precedent_carries_no_adjudication_status_token(self):
        ids = self.reading("r1/c1", "retains", "without qualification")
        self.assertEqual(G.cell_state(self.harness, "r1/c1"), G.READ)
        entry = self.slice_()[0]
        self.assertNotIn("status", entry.as_dict())
        self.assertEqual(entry.artifact_id, ids.reading)
        P.assert_no_adjudication_keys(self.slice_().as_dict())

    def test_the_precedent_slice_excludes_the_cell_under_judgement(self):
        self.reading("r1/c1", "retains", "without qualification")
        self.reading("r1/c2", "re-deploys", "the same term at all")
        kept = [entry.cell for entry in self.slice_(exclude=["r1/c1"])]
        self.assertEqual(kept, ["r1/c2"])

    def test_a_judge_pack_carries_no_other_judges_ruling(self):
        """Its only seat outputs are the critic's case and the defender's answer.

        Structural, not lexical: the rubric tells this seat what a *sustained*
        trial is and the contract asks it for ``sustained``, so the word is in
        the pack on purpose.  What is never there is a filled ruling.
        """

        self.reading("r1/c1", "retains", "without qualification", seat="judge-9")
        judge = self.judge_pack()
        kinds = {block.kind for block in judge.blocks}
        self.assertEqual(kinds - set(P.BLOCK_KINDS), set())
        self.assertEqual(
            [block.slot for block in judge.blocks if block.kind == P.SIDE_KIND],
            ["case", "answer"],
        )
        for key in ("sustained", "decisive_point", "reading_note", "ruling"):
            with self.subTest(key=key):
                self.assertNotIn(key, judge.parts)
        self.assertEqual(judge.parts["claim"]["passage_quote"], ONCE)

    def test_no_precedent_carries_the_seat_that_produced_it(self):
        """No seat is ever compared with another: a precedent is an occasion on
        record, not a seat's track record."""

        self.reading("r1/c1", "retains", "without qualification", seat="judge-9")
        judge = self.judge_pack()
        self.assertNotIn("judge-9", judge.text)
        self.assertNotIn("seat", self.slice_()[0].as_dict())

    def test_a_marker_pack_names_exactly_one_register(self):
        pack = self.marker_pack()
        self.assertEqual(pack.parts["subject"]["register"], "T")
        for other in ("E", "D", "G"):
            with self.subTest(register=other):
                self.assertNotIn(
                    STD.PLAN_8A_REGISTERS[other].plan_text, pack.text
                )
        self.assertIn(STD.PLAN_8A_REGISTERS["T"].plan_text, pack.text)

    def test_a_marker_pack_shows_no_arm_name_and_records_the_alias_map(self):
        pack = self.marker_pack()
        self.assertEqual(
            pack.parts["presentation"]["side_aliases"],
            {"A": "ORIGINAL", "B": "CONTROL"},
        )
        for block in pack.blocks:
            if block.kind == P.SIDE_KIND:
                with self.subTest(name=block.name):
                    self.assertIn(block.name, ("side A", "side B"))
                    self.assertNotIn("ORIGINAL", block.name)
                    self.assertNotIn("CONTROL", block.name)


# ---------------------------------------------------------------------------
# Acceptance 3
# ---------------------------------------------------------------------------


class TheLexicalOverlapBannerIsPresentVerbatim(PackFixture):
    """Acceptance 3."""

    def test_the_banner_is_the_instruments_own_object_and_is_not_retyped(self):
        self.assertIs(STD.READING_BANNER, instrument.USE_RELATION_BANNER)
        self.assertNotIn('"**The tool records juxtapositions', MODULE.read_text(encoding="utf-8"))

    def test_every_reading_pack_carries_the_banner_byte_for_byte(self):
        for pack in (self.row_pack, self.defender_pack(), self.judge_pack()):
            with self.subTest(role=pack.role):
                self.assertIn(STD.READING_BANNER, pack.text)
                self.assertEqual(pack.block("banner").body, STD.READING_BANNER)

    def test_the_banner_reaches_every_seat_as_one_object(self):
        packs = (self.row_pack, self.defender_pack(), self.judge_pack())
        bodies = {pack.block("banner").body for pack in packs}
        self.assertEqual(len(bodies), 1)

    def test_a_standard_whose_banner_was_altered_is_refused(self):
        body = STD.standard_body(STD.STANDARD_BODY)
        body["vocabulary"]["instrument_banner"] = "a shorter banner"
        with self.assertRaises(P.PackError) as caught:
            P.render_row(self.surface, body, self.row)
        self.assertEqual(caught.exception.code, P.PACK_INPUT_INVALID)

    def test_the_published_vocabulary_note_rides_with_the_banner(self):
        self.assertIn(STD.VOCABULARY_NOTE, self.row_pack.text)


# ---------------------------------------------------------------------------
# Acceptance 4
# ---------------------------------------------------------------------------


class ARegisterPackWithoutBaselineShaRaisesBaselineNotFirst(PackFixture):
    """Acceptance 4 — G8, the baseline seal."""

    def sides(self):
        replicate = SY.contrast_leg()["cases"]["case-a"]["replicates"]["rep-1"]
        return (
            P.MarkSide("ORIGINAL", replicate["ORIGINAL"]),
            P.MarkSide("CONTROL", replicate["CONTROL"]),
        )

    def test_a_missing_empty_or_malformed_baseline_sha_refuses_the_render(self):
        for value in (None, "", "   ", "not-a-digest", "b" * 63, "B" * 64, 12345):
            with self.subTest(baseline_sha=value):
                with self.assertRaises(P.BaselineNotFirst) as caught:
                    P.render_register(
                        "case-a", "T", "original-vs-control", value,
                        STD.STANDARD_BODY, sides=self.sides(),
                    )
                self.assertEqual(caught.exception.code, P.BASELINE_NOT_FIRST)

    def test_baseline_not_first_is_a_pack_error_and_a_loop_error(self):
        error = P.BaselineNotFirst("no seal")
        self.assertIsInstance(error, P.PackError)
        self.assertIsInstance(error, LoopError)
        self.assertIn(P.BASELINE_NOT_FIRST, loop_types.FAILURE_CODES)

    def test_a_sealed_sha_renders_and_is_pinned_into_the_pack_record(self):
        pack = self.marker_pack()
        self.assertEqual(pack.parts["baseline"]["sha256"], "b" * 64)
        self.assertIn("b" * 64, pack.canonical_bytes().decode("utf-8"))

    def test_a_changed_baseline_sha_changes_the_pack_digest(self):
        first = self.marker_pack()
        second = P.render_register(
            "case-a", "T", "original-vs-control", "c" * 64,
            STD.STANDARD_BODY, sides=self.sides(),
        )
        self.assertNotEqual(first.sha, second.sha)

    def test_the_pack_carries_the_baselines_digest_and_never_its_kind_set(self):
        """G9's downgrade is the program's; a seat shown the frozen kinds would
        be pre-empting it."""

        pack = self.marker_pack()
        self.assertNotIn("baseline_kinds", pack.canonical_bytes().decode("utf-8"))
        self.assertIn("difference_kinds", pack.parts["subject"])
        self.assertEqual(
            tuple(pack.parts["subject"]["difference_kinds"]),
            STD.DIFFERENCE_KINDS["T"],
        )

    def test_an_unknown_register_is_refused_before_any_pack_exists(self):
        with self.assertRaises(P.PackError) as caught:
            P.render_register(
                "case-a", "X", "original-vs-control", "b" * 64,
                STD.STANDARD_BODY, sides=self.sides(),
            )
        self.assertEqual(caught.exception.code, P.PACK_INPUT_INVALID)

    def test_two_sides_of_one_arm_are_refused(self):
        with self.assertRaises(P.PackError):
            P.render_register(
                "case-a", "T", "original-vs-control", "b" * 64, STD.STANDARD_BODY,
                sides=(P.MarkSide("ORIGINAL", "a"), P.MarkSide("ORIGINAL", "b")),
            )

    def test_a_cell_key_token_yields_the_cells_own_id(self):
        pack = P.render_register(
            G.CellKey("case-a", "T", "original-vs-control").token,
            "T", "original-vs-control", "b" * 64, STD.STANDARD_BODY,
            sides=self.sides(),
        )
        self.assertEqual(pack.parts["subject"]["cell"], "case-a")


# ---------------------------------------------------------------------------
# Acceptance 5
# ---------------------------------------------------------------------------


class ThePrecedentQueryIsRecordedWithThePackAndRanksAppellateRulingsFirst(PackFixture):
    """Acceptance 5, and W1-GRAPH's open question **G1**."""

    def test_an_empty_slice_still_carries_its_query(self):
        empty = self.slice_()
        self.assertEqual(list(empty), [])
        self.assertIn(self.standard, empty.query)
        self.assertIn(str(P.PRECEDENT_K), empty.query)

    def test_the_query_text_is_in_the_pack_record_and_in_the_pack_text(self):
        judge = self.judge_pack()
        self.assertEqual(judge.parts["precedent"]["query"], self.slice_().query)
        self.assertIn(self.slice_().query, judge.text)

    def test_the_query_says_the_order_is_not_a_ranking_by_merit(self):
        self.assertIn("never a ranking by merit", self.slice_().query)
        self.assertIn("registration order", self.slice_().query)

    def test_an_appellate_ruling_ranks_first_even_when_registered_last(self):
        first = self.reading("r1/c1", "retains", "without qualification")
        self.reading("r1/c2", "re-deploys", "the same term at all")
        self.appeal(first.bearing)
        entries = self.slice_()
        self.assertEqual(entries[0].kind, P.RECORD_APPELLATE_RULING)
        self.assertTrue(entries.appellate_first)
        self.assertEqual(entries[0].position, 1)
        self.assertNotIn(P.RECORD_APPELLATE_RULING, [e.kind for e in entries[1:]])

    def test_appellate_rulings_are_first_in_the_declared_selection_order(self):
        self.assertEqual(P.PRECEDENT_KINDS[0], P.RECORD_APPELLATE_RULING)
        self.assertTrue(self.slice_().as_dict()["appellate_rulings_first"])

    def test_readings_are_selected_in_registration_order(self):
        self.reading("r1/c1", "retains", "without qualification")
        self.reading("r1/c2", "re-deploys", "the same term at all")
        self.reading("r1/c3", "qualifies", "the two terms are the same term")
        self.assertEqual([e.cell for e in self.slice_()], ["r1/c1", "r1/c2", "r1/c3"])

    def test_the_slice_is_truncated_to_k_and_k_is_pinned_into_the_record(self):
        for cell, point in (("r1/c1", "without qualification"),
                            ("r1/c2", "the same term at all"),
                            ("r1/c3", "the two terms are the same term")):
            self.reading(cell, "retains", point)
        narrow = self.slice_(2)
        self.assertEqual(len(narrow), 2)
        self.assertEqual(narrow.as_dict()["k"], 2)
        self.assertEqual([e.position for e in narrow], [1, 2])

    def test_a_reading_that_does_not_stand_is_not_precedent(self):
        ids = self.reading("r1/c1", "retains", "without qualification")
        self.assertEqual(len(self.slice_()), 1)
        self.appeal(ids.bearing)
        kinds = [entry.kind for entry in self.slice_()]
        self.assertEqual(kinds, [P.RECORD_APPELLATE_RULING])

    def test_a_reading_under_another_standard_is_not_precedent_here(self):
        self.reading("r1/c1", "retains", "without qualification")
        self.assertEqual(P.precedent_slice(self.harness, "f" * 64, 5), [])

    def test_a_precedent_carries_its_stated_ground(self):
        self.reading("r1/c1", "retains", "without qualification")
        self.assertEqual(self.slice_()[0].ground, "without qualification")

    def test_an_appellate_precedent_carries_the_rulings_own_ground(self):
        ids = self.reading("r1/c1", "retains", "without qualification")
        self.appeal(ids.bearing)
        self.assertIn("does not bear", self.slice_()[0].ground)

    def test_a_precedent_slice_is_a_list(self):
        self.assertIsInstance(self.slice_(), list)

    def test_a_non_positive_k_or_a_source_that_is_not_a_harness_is_refused(self):
        for bad in (0, -1, True, 1.5, "5"):
            with self.subTest(k=bad):
                with self.assertRaises(P.PackError) as caught:
                    P.precedent_slice(self.harness, self.standard, bad)
                self.assertEqual(caught.exception.code, P.PRECEDENT_QUERY_INVALID)
        with self.assertRaises(P.PackError) as caught:
            P.precedent_slice(object(), self.standard, 3)
        self.assertEqual(caught.exception.code, P.PRECEDENT_QUERY_INVALID)

    def test_a_judge_pack_without_the_query_is_refused(self):
        with self.assertRaises(P.PackError) as caught:
            P.render_exchange(self.row_pack, self.critic, self.defender, precedents=[])
        self.assertEqual(caught.exception.code, P.PRECEDENT_QUERY_INVALID)

    def test_the_slice_reads_the_graph_and_writes_nothing(self):
        before = (self.tmp / "graph" / "log.jsonl").read_bytes()
        self.reading("r1/c1", "retains", "without qualification")
        after = (self.tmp / "graph" / "log.jsonl").read_bytes()
        self.slice_()
        self.assertEqual((self.tmp / "graph" / "log.jsonl").read_bytes(), after)
        self.assertTrue(after.startswith(before))


# ---------------------------------------------------------------------------
# Content addressing, and the embedded surface
# ---------------------------------------------------------------------------


class ThePackIsContentAddressedAndEmbedsTheSurfaceByteForByte(PackFixture):
    """The wave-2 brief: content-addressed packs, and wave-1 **S3** / **S5**."""

    def test_the_pack_sha_is_the_sha256_of_its_canonical_bytes(self):
        from deepreason_core.canonical import sha256_hex

        for pack in self.every_pack():
            with self.subTest(role=pack.role):
                self.assertEqual(P.pack_sha(pack), sha256_hex(pack.canonical_bytes()))
                self.assertEqual(pack.sha, P.pack_sha(pack))

    def test_the_canonical_bytes_are_canonical_json_of_the_record(self):
        from deepreason_core.canonical import canonical_json

        self.assertEqual(
            self.row_pack.canonical_bytes(), canonical_json(self.row_pack.as_dict())
        )

    def test_pack_sha_refuses_anything_that_is_not_a_pack(self):
        for value in ({"role": "critic"}, "critic", None):
            with self.subTest(value=value):
                with self.assertRaises(P.PackError) as caught:
                    P.pack_sha(value)
                self.assertEqual(caught.exception.code, P.PACK_INPUT_INVALID)

    def test_the_surface_is_embedded_exactly_once_byte_for_byte(self):
        self.assertIn(self.surface.decoded, self.row_pack.text)
        self.assertEqual(self.row_pack.material, self.surface.decoded)
        self.assertEqual(
            self.row_pack.text.encode("utf-8").count(self.surface.text), 1
        )

    def test_the_surface_digest_is_in_the_pack_text_and_in_the_record(self):
        self.assertIn(self.surface.digest, self.row_pack.text)
        self.assertIn(self.surface.digest, self.row_pack.headings)
        self.assertEqual(self.row_pack.material_digest, self.surface.digest)
        self.assertEqual(
            self.row_pack.parts["subject"]["surface_sha256"], self.surface.digest
        )

    def test_the_standard_is_pinned_by_digest_and_matches_the_frozen_body(self):
        self.assertEqual(
            self.row_pack.parts["standard"]["sha256"], STD.STANDARD_BODY_SHA256
        )
        self.assertEqual(self.row_pack.parts["standard"]["spec_id"], STD.SPEC_ID)

    def test_the_record_carries_the_rendered_text_so_the_digest_addresses_it(self):
        self.assertEqual(self.row_pack.as_dict()["text"], self.row_pack.text)

    def test_a_body_that_is_not_this_standard_is_refused(self):
        with self.assertRaises(StandardInvalid):
            P.render_row(self.surface, b'{"schema": "something.else"}', self.row)

    def test_something_that_is_not_a_surface_is_refused(self):
        with self.assertRaises(P.PackError) as caught:
            P.render_row(self.row, STD.STANDARD_BODY, self.row)
        self.assertEqual(caught.exception.code, P.PACK_INPUT_INVALID)


class TheMaterialReachingEverySeatIsTheMaterialReachingTheFirst(PackFixture):
    """Wave-1 open question **S7**: the material is never paraphrased, and the
    bytes reaching seat *n* are the bytes reaching seat 0."""

    def test_the_defender_and_the_judge_see_the_critics_material_unchanged(self):
        for pack in (self.defender_pack(), self.judge_pack()):
            with self.subTest(role=pack.role):
                self.assertEqual(pack.material, self.row_pack.material)
                self.assertEqual(pack.material_digest, self.surface.digest)
                self.assertIn(self.surface.decoded, pack.text)

    def test_the_variator_pack_carries_no_material_at_all(self):
        variator = P.render_paraphrase_request(self.judge_pack())
        self.assertEqual(variator.material, "")
        self.assertNotIn(self.surface.decoded, variator.text)

    def test_a_downstream_pack_without_a_row_pack_is_refused(self):
        with self.assertRaises(P.PackError) as caught:
            P.render_exchange(self.judge_pack(), self.critic)
        self.assertEqual(caught.exception.code, P.PACK_INPUT_INVALID)


# ---------------------------------------------------------------------------
# The exchange surface — wave-1 S4, design G2(b)
# ---------------------------------------------------------------------------


class TheExchangeSurfaceIsBuiltHereSoG2bHasOneImplementation(unittest.TestCase):
    """Wave-1 open question **S4**."""

    def exchange(self) -> P.Exchange:
        return P.exchange_surface("the case as put", "the answer as given")

    def test_the_exchange_is_case_newline_answer(self):
        self.assertEqual(self.exchange().text, "the case as put\nthe answer as given")
        self.assertEqual(P.EXCHANGE_SEPARATOR, "\n")

    def test_it_agrees_byte_for_byte_with_the_registration_gates_own_exchange(self):
        transcript = G.Transcript(
            case="the case as put",
            answer="the answer as given",
            decisive_point="as put",
        )
        self.assertEqual(self.exchange().text, transcript.exchange)

    def test_a_point_occurring_once_resolves_with_the_part_it_fell_in(self):
        offset = self.exchange().resolve("as put")
        self.assertEqual(offset.part, "case")
        self.assertEqual(self.exchange().text[offset.start:offset.end], "as put")
        self.assertEqual(offset.exchange_digest, self.exchange().digest)

    def test_a_point_in_the_answer_reports_the_answer(self):
        self.assertEqual(self.exchange().resolve("as given").part, "answer")

    def test_a_point_crossing_the_separator_reports_the_join(self):
        offset = self.exchange().resolve("put\nthe answer")
        self.assertTrue(offset.spans_join)
        self.assertEqual(offset.part, P.JOIN_PART)

    def test_zero_and_more_than_one_occurrence_both_resolve_to_none(self):
        exchange = P.exchange_surface("a claim about x", "a claim about y")
        self.assertIsNone(exchange.resolve("a claim about"))
        self.assertEqual(exchange.count("a claim about"), 2)
        self.assertIsNone(exchange.resolve("nowhere in here"))
        self.assertEqual(exchange.count("nowhere in here"), 0)

    def test_occurrences_are_counted_overlapping_which_str_count_is_not(self):
        exchange = P.exchange_surface("aaa", "b")
        self.assertEqual(exchange.count("aa"), 2)
        self.assertEqual(exchange.text.count("aa"), 1)

    def test_the_vendored_predicate_is_kept_beside_the_stronger_one(self):
        exchange = P.exchange_surface("aaa", "b")
        self.assertTrue(exchange.conforming("aa"))
        self.assertIsNone(exchange.resolve("aa"))

    def test_an_empty_point_designates_nothing(self):
        self.assertEqual(self.exchange().count(""), 0)
        self.assertIsNone(self.exchange().resolve(""))

    def test_an_empty_case_or_answer_is_refused(self):
        for case, answer in (("", "a"), ("a", ""), ("   ", "a"), (None, "a"), ("a", 3)):
            with self.subTest(case=case, answer=answer):
                with self.assertRaises(P.PackError) as caught:
                    P.exchange_surface(case, answer)
                self.assertEqual(caught.exception.code, P.EXCHANGE_MALFORMED)

    def test_a_paraphrase_is_the_same_shape_and_carries_what_it_restates(self):
        source = self.exchange()
        paraphrase = P.paraphrase_surface("the case restated, answered likewise", of=source)
        self.assertTrue(paraphrase.is_paraphrase)
        self.assertEqual(paraphrase.source_digest, source.digest)
        self.assertEqual(paraphrase.labels, (P.PARAPHRASE_PART,))
        self.assertEqual(paraphrase.resolve("restated").part, P.PARAPHRASE_PART)
        self.assertNotEqual(paraphrase.digest, source.digest)

    def test_a_paraphrase_of_something_that_is_not_an_exchange_is_refused(self):
        with self.assertRaises(P.PackError) as caught:
            P.paraphrase_surface("text", of="not an exchange")
        self.assertEqual(caught.exception.code, P.EXCHANGE_MALFORMED)

    def test_the_exchange_record_carries_no_scoring_key(self):
        C.assert_no_scoring_keys(self.exchange().as_dict())
        self.assertEqual(self.exchange().as_dict()["parts"], list(P.EXCHANGE_PARTS))


# ---------------------------------------------------------------------------
# G6 — the order swap
# ---------------------------------------------------------------------------


class TheOrderSwapPresentsBothOrdersAndRecordsTheSwap(PackFixture):
    """Design §2.4 G6, and the wave-2 brief's order-swap pack for marks."""

    def test_both_orders_returns_the_declared_order_first(self):
        declared, swapped = P.both_orders(self.marker_pack())
        self.assertEqual(declared.order, P.ORDER_AS_DECLARED)
        self.assertEqual(swapped.order, P.ORDER_SWAPPED)
        self.assertNotEqual(declared.sha, swapped.sha)

    def test_both_orders_is_stable_whichever_order_it_is_handed(self):
        declared, swapped = P.both_orders(self.marker_pack())
        again = P.both_orders(swapped)
        self.assertEqual(again[0].sha, declared.sha)
        self.assertEqual(again[1].sha, swapped.sha)

    def test_a_mark_pack_swaps_its_bodies_and_keeps_its_position_labels(self):
        declared, swapped = P.both_orders(self.marker_pack())
        sides = [b for b in declared.blocks if b.kind == P.SIDE_KIND]
        after = [b for b in swapped.blocks if b.kind == P.SIDE_KIND]
        self.assertEqual([b.name for b in after], [b.name for b in sides])
        self.assertEqual(after[0].body, sides[1].body)
        self.assertEqual(after[1].body, sides[0].body)

    def test_the_alias_map_is_reassigned_with_the_sides(self):
        declared, swapped = P.both_orders(self.marker_pack())
        self.assertEqual(
            declared.parts["presentation"]["side_aliases"],
            {"A": "ORIGINAL", "B": "CONTROL"},
        )
        self.assertEqual(
            swapped.parts["presentation"]["side_aliases"],
            {"A": "CONTROL", "B": "ORIGINAL"},
        )

    def test_the_swap_is_recorded_inside_the_pack_digest(self):
        _, swapped = P.both_orders(self.marker_pack())
        self.assertTrue(swapped.parts["presentation"]["swap_recorded"])
        self.assertIn(P.ORDER_SWAPPED, swapped.canonical_bytes().decode("utf-8"))

    def test_the_swap_is_an_involution(self):
        pack = self.marker_pack()
        self.assertEqual(pack.swap().swap().canonical_bytes(), pack.canonical_bytes())

    def test_a_judge_pack_reverses_the_case_and_the_answer(self):
        declared, swapped = P.both_orders(self.judge_pack())
        labels = [b.name for b in swapped.blocks if b.kind == P.SIDE_KIND]
        self.assertEqual(labels, ["the answer", "the case"])
        self.assertEqual(
            [b.name for b in declared.blocks if b.kind == P.SIDE_KIND],
            ["the case", "the answer"],
        )

    def test_the_exchange_surface_is_never_reordered_by_a_presentation_swap(self):
        """G2(b) resolves against ``case + "\\n" + answer`` whichever way the
        pack was laid out, or the guard would run over two different surfaces."""

        declared, swapped = P.both_orders(self.judge_pack())
        self.assertEqual(declared.exchange.text, swapped.exchange.text)
        self.assertEqual(
            declared.parts["exchange"]["digest"], swapped.parts["exchange"]["digest"]
        )

    def test_a_pack_with_no_two_sides_refuses_to_swap(self):
        for pack in (self.row_pack, self.defender_pack()):
            with self.subTest(role=pack.role):
                with self.assertRaises(P.PackError) as caught:
                    pack.swap()
                self.assertEqual(caught.exception.code, P.PACK_INPUT_INVALID)

    def test_the_order_swap_is_a_pinned_guard_parameter(self):
        self.assertTrue(STD.GUARD_PARAMETERS["order_swap_both_orders"])
        self.assertEqual(P.ORDERS, (P.ORDER_AS_DECLARED, P.ORDER_SWAPPED))

    def test_an_unknown_order_is_refused(self):
        with self.assertRaises(P.PackError):
            self.judge_pack(order="sideways")


# ---------------------------------------------------------------------------
# G7 — the paraphrase pack
# ---------------------------------------------------------------------------


class TheParaphrasePackCarriesTheTextAndTheSpanSurvivalCheckInput(PackFixture):
    """Design §2.3's variator and §2.4 G7."""

    def test_the_pack_carries_the_exchange_it_restates(self):
        judge = self.judge_pack()
        variator = P.render_paraphrase_request(judge)
        self.assertEqual(variator.role, P.ROLE_VARIATOR)
        self.assertIn(judge.exchange.text, variator.text)
        self.assertEqual(
            variator.parts["subject"]["exchange"]["digest"], judge.exchange.digest
        )

    def test_the_held_spans_are_the_quoted_span_and_are_pinned_in_the_record(self):
        variator = P.render_paraphrase_request(self.judge_pack())
        self.assertEqual(variator.parts["held_spans"], [ONCE])
        self.assertIn(ONCE, variator.text)
        self.assertIn(ONCE, variator.canonical_bytes().decode("utf-8"))

    def test_held_spans_of_reads_the_critics_quote_and_nothing_else(self):
        self.assertEqual(P.held_spans_of(self.critic), (ONCE,))
        self.assertEqual(P.held_spans_of({"passage_quote": "x"}), ("x",))

    def test_a_critic_answering_none_holds_no_span(self):
        none_critic = critic(relation="none", quote="", case="")
        self.assertEqual(P.held_spans_of(none_critic), ())

    def test_n_defaults_to_the_pinned_trial_paraphrase_n(self):
        variator = P.render_paraphrase_request(self.judge_pack())
        expected = STD.GUARD_PARAMETERS["paraphrase_n"]
        self.assertEqual(variator.parts["subject"]["paraphrase_n"], expected)
        self.assertEqual(expected, 2)
        self.assertIn(f"{expected} times", variator.text)

    def test_a_held_span_absent_from_the_exchange_is_recorded_not_dropped(self):
        exchange = P.exchange_surface("a case", "an answer")
        variator = P.render_paraphrase_request(exchange, held_spans=["not present"])
        self.assertEqual(variator.parts["held_spans"], ["not present"])
        self.assertEqual(
            variator.parts["held_spans_absent_from_exchange"], ["not present"]
        )

    def test_an_exchange_with_no_held_spans_renders_and_says_so(self):
        variator = P.render_paraphrase_request(P.exchange_surface("a case", "an answer"))
        self.assertEqual(variator.parts["held_spans"], [])
        self.assertIn("nothing was quoted", variator.text)

    def test_a_bare_string_of_held_spans_is_refused(self):
        with self.assertRaises(P.PackError) as caught:
            P.render_paraphrase_request(
                P.exchange_surface("a case", "an answer"), held_spans="one span"
            )
        self.assertEqual(caught.exception.code, P.PACK_INPUT_INVALID)

    def test_a_non_positive_n_is_refused(self):
        for bad in (0, -2, True, "2"):
            with self.subTest(n=bad):
                with self.assertRaises(P.PackError):
                    P.render_paraphrase_request(
                        P.exchange_surface("a case", "an answer"), n=bad
                    )

    def test_a_pack_that_carries_no_exchange_cannot_be_paraphrased(self):
        with self.assertRaises(P.PackError) as caught:
            P.render_paraphrase_request(self.row_pack)
        self.assertEqual(caught.exception.code, P.PACK_INPUT_INVALID)

    def test_the_re_ruling_pack_shows_one_restated_exchange_in_place_of_two_sides(self):
        judge = self.judge_pack()
        restated = P.paraphrase_surface(
            "The row is retained, say the objectors; the defence denies it.",
            of=judge.exchange,
        )
        again = P.render_exchange(
            self.row_pack, self.critic, self.defender,
            precedents=self.slice_(), exchange=restated,
        )
        self.assertEqual(again.role, P.ROLE_JUDGE)
        self.assertEqual(again.exchange, restated)
        self.assertIn(restated.text, again.text)
        self.assertNotIn(self.defender.answer, again.text)
        self.assertEqual(
            again.parts["exchange"]["source_digest"], judge.exchange.digest
        )
        self.assertFalse(again.is_pairwise)

    def test_the_re_ruling_pack_shows_the_same_material_claim_rubric_and_precedent(self):
        judge = self.judge_pack()
        restated = P.paraphrase_surface("The row is retained; denied.", of=judge.exchange)
        again = P.render_exchange(
            self.row_pack, self.critic, self.defender,
            precedents=self.slice_(), exchange=restated,
        )
        self.assertEqual(again.material, judge.material)
        self.assertEqual(again.parts["claim"], judge.parts["claim"])
        self.assertEqual(again.block("rubric").body, judge.block("rubric").body)
        self.assertEqual(again.parts["precedent"], judge.parts["precedent"])
        self.assertNotEqual(again.sha, judge.sha)

    def test_a_paraphrase_of_another_trial_is_refused_as_a_re_ruling_pack(self):
        other = P.paraphrase_surface(
            "a restatement", of=P.exchange_surface("another case", "another answer")
        )
        with self.assertRaises(P.PackError) as caught:
            P.render_exchange(
                self.row_pack, self.critic, self.defender,
                precedents=self.slice_(), exchange=other,
            )
        self.assertEqual(caught.exception.code, P.PACK_INPUT_INVALID)

    def test_a_trial_exchange_is_not_a_re_ruling_and_a_restated_one_cannot_be_swapped(self):
        judge = self.judge_pack()
        with self.assertRaises(P.PackError):
            P.render_exchange(
                self.row_pack, self.critic, self.defender,
                precedents=self.slice_(), exchange=judge.exchange,
            )
        restated = P.paraphrase_surface("The row is retained; denied.", of=judge.exchange)
        with self.assertRaises(P.PackError):
            P.render_exchange(
                self.row_pack, self.critic, self.defender,
                precedents=self.slice_(), exchange=restated,
                order=P.ORDER_SWAPPED,
            )

    def test_a_paraphrase_surface_re_runs_g2b_against_the_restatement(self):
        judge = self.judge_pack()
        restated = P.paraphrase_surface(
            "The row is retained, say the objectors; the defence denies it.",
            of=judge.exchange,
        )
        self.assertEqual(restated.source_digest, judge.exchange.digest)
        self.assertEqual(restated.count("the defence denies it"), 1)


# ---------------------------------------------------------------------------
# G12
# ---------------------------------------------------------------------------


class NoPackContainsAScoringKey(PackFixture):
    """Design §2.4 G12, over the pack's structured parts and its own headings."""

    def test_every_rendered_pack_passes_both_scans(self):
        for pack in self.every_pack():
            with self.subTest(role=pack.role):
                P.assert_pack_clean(pack)
                C.assert_no_scoring_keys(pack.as_dict())
                STD.assert_no_scoring_headers(pack.headings, pack.role)

    def test_a_scoring_key_planted_in_the_parts_is_refused(self):
        planted = P.Pack(
            role=P.ROLE_CRITIC,
            title="critic pack",
            blocks=(P.Block(kind="instruction", name="what you are asked", body="do it"),),
            parts={"subject": {"score": 3}},
        )
        with self.assertRaises(ScoringKeyForbidden):
            P.assert_pack_clean(planted)

    def test_a_scoring_word_planted_in_a_heading_is_refused(self):
        planted = P.Pack(
            role=P.ROLE_CRITIC,
            title="critic pack",
            blocks=(P.Block(kind="material", name="the best material", body="x"),),
        )
        with self.assertRaises(StandardInvalid) as caught:
            P.assert_pack_clean(planted)
        self.assertEqual(caught.exception.code, "SCORING_KEY_FORBIDDEN")

    def test_the_material_is_not_scanned_for_headers(self):
        """The material is quoted matter.  Refusing a published record because
        its author wrote a scoring word is this loop editing its own evidence."""

        row = hand_row(referring="| rank | best |\n|---|---|\n| a | b |")
        pack = P.render_row(S.build_surface(row), STD.STANDARD_BODY, row)
        self.assertIn("| rank | best |", pack.text)
        self.assertNotIn("rank", pack.headings)

    def test_the_headings_scanned_are_this_modules_own_and_all_of_them(self):
        lines = self.row_pack.headings.split("\n")
        self.assertTrue(lines[0].startswith(P.TITLE_PREFIX))
        self.assertEqual(len(lines), 1 + len(self.row_pack.blocks))
        for line, block in zip(lines[1:], self.row_pack.blocks):
            with self.subTest(name=block.name):
                self.assertEqual(line, f"{P.HEADING_PREFIX}{block.name}")
                self.assertIn(line, self.row_pack.text)

    def test_no_pack_instruction_describes_a_boundary_as_the_inquiry_running_out(self):
        for pack in self.every_pack():
            for block in pack.blocks:
                if block.kind == "instruction":
                    with self.subTest(role=pack.role):
                        STD.assert_no_exhaustion_claim(block.body, pack.role)

    def test_a_pack_instruction_that_claims_exhaustion_is_refused(self):
        planted = P.Pack(
            role=P.ROLE_CRITIC,
            title="critic pack",
            blocks=(
                P.Block(
                    kind="instruction",
                    name="what you are asked",
                    body="stop when the inquiry is exhausted",
                ),
            ),
        )
        with self.assertRaises(StandardInvalid) as caught:
            P.assert_pack_clean(planted)
        self.assertEqual(caught.exception.code, "RESOURCE_BOUNDARY_MISDESCRIBED")


# ---------------------------------------------------------------------------
# The rubric, the vocabulary and the output contract come from their owners
# ---------------------------------------------------------------------------


class TheRubricAndTheContractComeFromTheirOwnersAndAreNotRetyped(PackFixture):
    """§2.1's standard is the only source of the rubric; §2.3's schema is the
    only source of the contract."""

    def test_the_relation_rubric_body_is_in_the_critic_and_the_judge_pack(self):
        body = STD.RUBRIC_V1["relation"].body
        for pack in (self.row_pack, self.judge_pack()):
            with self.subTest(role=pack.role):
                self.assertIn(body, pack.text)
                self.assertEqual(pack.parts["standard"]["mode"], STD.MODE_ABSOLUTE)

    def test_the_pairwise_rubric_body_is_in_the_marker_pack(self):
        pack = self.marker_pack()
        self.assertIn(STD.RUBRIC_V1["contrast-mark"].body, pack.text)
        self.assertEqual(pack.parts["standard"]["mode"], STD.MODE_PAIRWISE)
        self.assertNotIn(STD.RUBRIC_V1["relation"].body, pack.text)

    def test_the_defender_pack_carries_no_rubric(self):
        """§2.3 gives the defender ``M`` and the case; a pack does not carry what
        its role is not asked to apply."""

        self.assertIsNone(self.defender_pack().block("rubric"))

    def test_the_embedded_contract_is_the_validators_own_schema(self):
        for pack, role in (
            (self.row_pack, "critic"),
            (self.defender_pack(), "defender"),
            (self.judge_pack(), "judge"),
        ):
            with self.subTest(role=role):
                schema = json.dumps(
                    C.schema_for(role), ensure_ascii=False, indent=2, sort_keys=True
                )
                self.assertIn(schema, pack.block("contract").body)

    def test_the_marker_contract_narrows_difference_kind_to_this_register(self):
        """W0-CONTRACTS' open question **O11**, answered at the pack: a marker is
        never in the position of not knowing which register was asked."""

        pack = self.marker_pack()
        body = pack.block("contract").body
        for token in STD.DIFFERENCE_KINDS["T"]:
            with self.subTest(token=token):
                self.assertIn(token, body)
        for token in STD.DIFFERENCE_KINDS["E"]:
            with self.subTest(absent=token):
                self.assertNotIn(token, body)

    def test_the_word_limits_in_a_pack_are_the_standards_own(self):
        for pack, role in (
            (self.row_pack, "critic"),
            (self.defender_pack(), "defender"),
            (self.judge_pack(), "judge"),
            (self.marker_pack(), "marker"),
        ):
            with self.subTest(role=role):
                expected = {
                    field: limit
                    for (owner, field), limit in STD.WORD_LIMITS.items()
                    if owner == role
                }
                self.assertEqual(pack.parts["word_limits"], expected)
                for field, limit in expected.items():
                    self.assertIn(f"`{field}`: at most {limit}", pack.block("contract").body)

    def test_the_framing_reports_what_the_instrument_said_and_invents_nothing(self):
        parts = self.row_pack.parts["framing"]
        self.assertEqual(parts["ref_field"], self.row["ref_field"])
        self.assertEqual(parts["ref_verbatim"], self.row["ref_verbatim"])
        self.assertEqual(
            parts["lexical_overlap_note"], self.row["lexical_overlap_note"]
        )
        self.assertEqual(
            [note["code"] for note in parts["resolver_notes"]],
            [note["code"] for note in self.row["resolver_notes"]],
        )

    def test_an_absent_uptake_boolean_is_reported_as_null_and_never_as_false(self):
        row = hand_row()
        pack = P.render_row(S.build_surface(row), STD.STANDARD_BODY, row)
        parts = pack.parts["framing"]
        self.assertIsNone(parts["declared_uptake_includes_referring_record"])
        self.assertIn("declared uptake includes the referring record: null", pack.text)

    def test_the_framing_accepts_the_instruments_own_use_row(self):
        fields = dict(self.row)
        fields["referring_body_passages"] = tuple(
            instrument.Passage(
                start=p["start"], end=p["end"], text=p["text"],
                distinctive_tokens_present=tuple(p["distinctive_tokens_present"]),
            )
            for p in self.row["referring_body_passages"]
        )
        fields["resolver_notes"] = tuple(
            instrument.ResolverNote(code=n["code"], reason=n["reason"])
            for n in self.row["resolver_notes"]
        )
        for name in ("referring_record_source_span", "target_record_source_span"):
            if fields[name] is not None:
                fields[name] = tuple(fields[name])
        use_row = instrument.UseRow(**fields)
        pack = P.render_row(self.surface, STD.STANDARD_BODY, use_row)
        self.assertEqual(pack.sha, self.row_pack.sha)

    def test_the_claim_under_trial_names_the_relation_and_the_cited_passage(self):
        for pack in (self.defender_pack(), self.judge_pack()):
            with self.subTest(role=pack.role):
                self.assertEqual(pack.parts["claim"]["relation"], "retains")
                self.assertEqual(pack.parts["claim"]["passage_quote"], ONCE)
                self.assertIn(ONCE, pack.block("claim").body)

    def test_a_resolved_offset_is_carried_whole_and_never_converted(self):
        """Wave-1 open question **S1**: carry ``Offset.as_dict()``, do not convert."""

        offset = S.resolve_unique(self.surface, ONCE)
        pack = self.judge_pack(offset=offset)
        self.assertEqual(pack.parts["citation_offset"], offset.as_dict())
        self.assertEqual(pack.parts["citation_offset"]["side"], S.SIDE_REFERRING_RECORD)

    def test_a_critic_whose_case_or_quote_is_missing_is_refused(self):
        with self.assertRaises(P.PackError) as caught:
            P.render_exchange(self.row_pack, {"relation": "retains"})
        self.assertEqual(caught.exception.code, P.PACK_INPUT_INVALID)


# ---------------------------------------------------------------------------
# The mirrors, and the code table
# ---------------------------------------------------------------------------


class TheMirroredTokensAgreeWithTheModulesThatOwnThem(unittest.TestCase):
    """``packs`` does not import ``graph`` or ``obligations``; this test imports
    all three and asserts every token it mirrors."""

    def test_the_record_field_is_the_one_graph_writes_and_obligations_reads(self):
        self.assertEqual(P.RECORD_FIELD, G.RECORD_FIELD)
        self.assertEqual(P.RECORD_FIELD, OB.RECORD_FIELD)

    def test_every_mirrored_record_token_is_one_graph_writes(self):
        for token in (
            P.RECORD_APPELLATE_RULING,
            P.RECORD_READING_ROW,
            P.RECORD_CELL_MARK,
        ):
            with self.subTest(token=token):
                self.assertIn(token, G.RECORD_KINDS)

    def test_the_two_reading_tokens_are_the_two_obligations_calls_readings(self):
        self.assertEqual(
            (P.RECORD_READING_ROW, P.RECORD_CELL_MARK), OB.READING_KINDS
        )

    def test_the_standing_label_is_the_one_obligations_requires_of_evidence(self):
        self.assertEqual(P.STANDING, OB.STANDING)

    def test_the_cell_key_separator_is_the_one_graph_mints_keys_with(self):
        self.assertEqual(
            P.CELL_KEY_SEPARATOR,
            G.CellKey("cell", "T", "cmp").token.replace("cell", "").replace("T", "")[0],
        )
        self.assertEqual(
            G.CellKey("cell", "T", "cmp").token,
            P.CELL_KEY_SEPARATOR.join(("cell", "T", "cmp")),
        )

    def test_the_five_pack_roles_are_the_standards_five_model_roles(self):
        self.assertEqual(P.PACK_ROLES, STD.ROLE_NAMES)
        self.assertNotIn("decider", P.PACK_ROLES)

    def test_every_rubric_named_for_a_role_is_a_class_of_the_standard(self):
        for role, rubric_id in P.RUBRIC_FOR_ROLE.items():
            with self.subTest(role=role):
                self.assertIn(role, P.PACK_ROLES)
                self.assertIn(rubric_id, STD.RUBRIC_V1)

    def test_the_registers_are_the_standards_and_are_never_retyped(self):
        self.assertIs(P.render_register.__globals__["REGISTER_IDS"], STD.REGISTER_IDS)


class TheCodesThisModuleRaisesAreDeclared(unittest.TestCase):
    """W0-TYPES open question **O9**: a later wave declares its codes."""

    def test_every_new_code_is_an_upper_snake_token_with_a_reason(self):
        for code, reason in P.NEW_CODES.items():
            with self.subTest(code=code):
                self.assertRegex(code, r"\A[A-Z][A-Z0-9_]*\Z")
                self.assertTrue(reason.strip())

    def test_every_new_code_is_folded_into_the_failure_table(self):
        """O9, the wave-2 integrator's side of it.

        While this module was on the frontier the assertion was the opposite -
        ``set(NEW_CODES) & FAILURE_CODES == set()``, which is what "new" meant
        on the day the module landed. The fold-in makes ``types`` the owner of
        all four, so the contract is now membership: a code declared here and
        absent from the table would be one a record could carry that no reader
        can look up.
        """

        self.assertEqual(set(P.NEW_CODES) - loop_types.FAILURE_CODES, set())
        self.assertEqual(set(P.NEW_CODES) & set(loop_types.OUTCOME_CODES), set())

    def test_baseline_not_first_is_already_in_the_table_and_is_not_new(self):
        self.assertIn(P.BASELINE_NOT_FIRST, loop_types.FAILURE_CODES)
        self.assertNotIn(P.BASELINE_NOT_FIRST, P.NEW_CODES)

    def test_every_code_this_module_raises_is_declared_somewhere(self):
        source = MODULE.read_text(encoding="utf-8")
        raised = set(re.findall(r"_refuse\(\s*([A-Z][A-Z0-9_]*)", source))
        raised |= set(re.findall(r"PackError\(\s*([A-Z][A-Z0-9_]*)(?![A-Za-z])", source))
        raised |= {P.BASELINE_NOT_FIRST}
        known = set(P.NEW_CODES) | loop_types.FAILURE_CODES
        self.assertTrue(raised)
        self.assertEqual(raised - known, set())

    def test_every_code_is_raised_as_a_module_constant_and_never_as_a_literal(self):
        source = MODULE.read_text(encoding="utf-8")
        self.assertEqual(re.findall(r'_refuse\(\s*"', source), [])
        self.assertEqual(re.findall(r'PackError\(\s*"', source), [])

    def test_every_pack_error_is_a_loop_error(self):
        self.assertTrue(issubclass(P.PackError, LoopError))
        self.assertTrue(issubclass(P.BaselineNotFirst, P.PackError))

    def test_the_public_interface_the_wave_plan_names_is_present(self):
        for name in (
            "render_row",
            "render_exchange",
            "render_register",
            "render_paraphrase_request",
            "precedent_slice",
            "pack_sha",
            "BaselineNotFirst",
            "exchange_surface",
        ):
            with self.subTest(name=name):
                self.assertIn(name, P.__all__)
                self.assertTrue(hasattr(P, name))

    def test_the_module_imports_only_its_declared_dependencies(self):
        tree = ast.parse(MODULE.read_text(encoding="utf-8"))
        siblings = set()
        for node in ast.walk(tree):
            module = getattr(node, "module", None)
            if isinstance(node, ast.ImportFrom) and module and module.startswith(
                "minireason.loop."
            ):
                siblings.add(module.rsplit(".", 1)[-1])
        self.assertEqual(siblings, {"contracts", "standard", "surface", "types"})


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
