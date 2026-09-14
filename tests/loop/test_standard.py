"""Offline tests for W0-STANDARD, one test per acceptance clause.

No provider call, no network, no credential and no write outside the temp dirs these
tests do not need.  The frozen C001 ``PLAN.md`` and ``material.json`` are read read-only
from this checkout, resolved from this file's own location so the suite never reaches
into another working tree.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import unittest
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterator
from unittest import mock

from minireason import use_relation_h005
from minireason.loop import standard, types as loop_types
from minireason.loop.standard import (
    CALIBRATION_ANCHORS,
    CEILING_CLAIM_TEMPLATE,
    CEILING_REQUIRED_SENTENCES,
    CEILING_SHA256,
    CEILING_TEXT,
    DIFFERENCE_KINDS,
    FALSIFIER_MAP,
    GUARD_PARAMETERS,
    MODE_ABSOLUTE,
    MODE_PAIRWISE,
    PLAN_8A_MIRROR,
    PLAN_8A_REGISTERS,
    READING_VOCABULARY,
    REGISTER_IDS,
    REOPEN_REASONS,
    RUBRIC_V1,
    SPEC_ID,
    STANDARD_BODY,
    STANDARD_BODY_SHA256,
    Register,
    StandardInvalid,
    build_standard,
    standard_body,
)

REPO = Path(__file__).resolve().parents[2]
PLAN = REPO / "experiments/diagnostics/C001-contrast-triple/PLAN.md"
MATERIAL = REPO / "experiments/diagnostics/C001-contrast-triple/material.json"


def walk(value: Any, path: str = "") -> Iterator[tuple[str, Any]]:
    """Every (dotted path, leaf) pair of a parsed JSON body."""
    if isinstance(value, dict):
        for key, item in value.items():
            yield from walk(item, f"{path}.{key}" if path else str(key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk(item, f"{path}[{index}]")
    else:
        yield path, value


def flat(text: str) -> str:
    """The same text with every run of whitespace collapsed, so a hard wrap is not a diff."""
    return " ".join(text.split())


def published_vocabulary_note() -> str:
    """The ``#:`` note published above ``ROOT_READING_VOCABULARY``, as the module ships it."""
    lines = Path(use_relation_h005.__file__).read_text(encoding="utf-8").split("\n")
    index = next(
        k for k, line in enumerate(lines) if line.startswith("ROOT_READING_VOCABULARY = (")
    )
    collected: list[str] = []
    k = index - 1
    while k >= 0 and lines[k].startswith("#:"):
        collected.append("" if lines[k] == "#:" else lines[k][2:].lstrip())
        k -= 1
    return "\n".join(reversed(collected))


class AcceptanceEveryPlan8aRegisterIsByteIdentical(unittest.TestCase):
    """Clause: every PLAN 8a register definition appears byte-identically against PLAN.md."""

    def test_every_plan_8a_register_definition_appears_byte_identically_against_plan_md(self):
        plan_bytes = PLAN.read_bytes()
        self.assertEqual(sorted(PLAN_8A_REGISTERS), sorted(REGISTER_IDS))
        for rid in REGISTER_IDS:
            register = PLAN_8A_REGISTERS[rid]
            with self.subTest(register=rid):
                self.assertIn(register.plan_text.encode("utf-8"), plan_bytes)
                self.assertTrue(register.plan_text.startswith(f"* **{rid} — "))
        for key in ("preamble", "replicate_baseline", "order_of_reading",
                    "register_to_falsifier", "two_readers"):
            with self.subTest(block=key):
                self.assertIn(PLAN_8A_MIRROR[key].encode("utf-8"), plan_bytes)

    #: The digest ``PLAN.md`` carried before commit ``2d7239a`` appended §15
    #: ("Successor occurrence-02 under driver v2", 88 lines added, none edited).
    #: A staging clone cut before that commit carries these bytes, and the pin
    #: names the live file, so the digest assertion skips there with this
    #: reason rather than failing over a file the checkout simply predates
    #: (wave-1 integration decision 51's precedent, applied to the plan).
    PLAN_BEFORE_SECTION_15 = (
        "601a0adc274f269f96c503e7336dc1df5e1386242569919459374f5714acadf5")

    def test_the_mirror_pins_the_frozen_plan_and_material_by_sha256(self):
        source = PLAN_8A_MIRROR["source"]
        observed = hashlib.sha256(PLAN.read_bytes()).hexdigest()
        self.assertEqual(
            source["material_sha256"], hashlib.sha256(MATERIAL.read_bytes()).hexdigest()
        )
        self.assertEqual(source["plan_path"], str(PLAN.relative_to(REPO)))
        self.assertEqual(source["material_path"], str(MATERIAL.relative_to(REPO)))
        if observed == self.PLAN_BEFORE_SECTION_15:
            self.skipTest(
                "this checkout predates commit 2d7239a, which appended PLAN.md §15; "
                "the mirror pins the live file. The section 8a text is asserted "
                "byte-identically against whichever PLAN.md is present, above, and "
                "that is what the mirror actually claims")
        self.assertEqual(source["plan_sha256"], observed)

    def test_the_appended_section_is_an_append_and_not_an_edit_of_section_8a(self):
        """Why the pin could move without the mirror moving with it.

        §15 was appended; §§1-14 were not touched. That is what makes re-pinning
        the digest a re-derivation rather than a re-reading: every mirrored
        block is still present byte-identically, which the test above asserts,
        and the new digest names the same section 8a it always named.
        """

        plan_bytes = PLAN.read_bytes()
        for rid in REGISTER_IDS:
            with self.subTest(register=rid):
                self.assertIn(PLAN_8A_REGISTERS[rid].plan_text.encode("utf-8"),
                              plan_bytes)
        self.assertIn(b"8a. What \"differs\" means, pre-declared", plan_bytes)
        self.assertEqual(PLAN_8A_MIRROR["source"]["plan_section"],
                         '8a. What "differs" means, pre-declared')

    def test_each_register_mirrors_the_frozen_material_reading_rule(self):
        rule = json.loads(MATERIAL.read_text(encoding="utf-8"))["reading_rule"]
        frozen = {entry["id"]: entry for entry in rule["registers"]}
        for rid in REGISTER_IDS:
            register = PLAN_8A_REGISTERS[rid]
            with self.subTest(register=rid):
                self.assertEqual(register.name, frozen[rid]["name"])
                self.assertEqual(register.reads, frozen[rid]["reads"])
                self.assertEqual(register.differs_iff, frozen[rid]["differs_iff"])
        self.assertEqual(list(standard.MARKS), list(rule["marks"]))


class AcceptanceFalsifierMap(unittest.TestCase):
    """Clause: FALSIFIER_MAP encodes that G alone never carries D1, and that F2/F3
    fire only on T, E or D."""

    def test_falsifier_map_encodes_that_g_alone_never_carries_d1(self):
        d1 = FALSIFIER_MAP["D1"]
        self.assertEqual(d1.comparison, ("ORIGINAL", "CONTROL"))
        self.assertFalse(d1.carries("G"))
        self.assertIn("G", d1.excluded_registers)
        self.assertTrue(all(d1.carries(rid) for rid in ("T", "E", "D")))
        self.assertEqual(PLAN_8A_REGISTERS["G"].carries_falsifiers, ())
        self.assertIn("forced by the design", d1.exclusion_reason)

    def test_falsifier_map_encodes_that_f2_and_f3_fire_only_on_t_e_or_d(self):
        self.assertEqual(FALSIFIER_MAP["F2"].comparison, ("ORIGINAL", "RECODING"))
        self.assertEqual(FALSIFIER_MAP["F3"].comparison, ("ORIGINAL", "CARRIER"))
        for fid in ("F2", "F3"):
            falsifier = FALSIFIER_MAP[fid]
            with self.subTest(falsifier=fid):
                self.assertEqual(falsifier.carrying_registers, ("T", "E", "D"))
                self.assertFalse(falsifier.carries("G"))
        for rid in ("T", "E", "D"):
            self.assertEqual(PLAN_8A_REGISTERS[rid].carries_falsifiers, ("D1", "F2", "F3"))

    def test_the_falsifier_rules_are_the_frozen_material_rules(self):
        frozen = json.loads(MATERIAL.read_text(encoding="utf-8"))["reading_rule"]
        for fid, rule in frozen["register_to_falsifier"].items():
            with self.subTest(falsifier=fid):
                self.assertEqual(FALSIFIER_MAP[fid].rule, rule)
        self.assertEqual(sorted(FALSIFIER_MAP), ["D1", "F2", "F3"])


class AcceptanceBuildIsByteStable(unittest.TestCase):
    """Clause: two builds from identical inputs are byte-identical."""

    def test_two_builds_from_identical_inputs_are_byte_identical(self):
        self.assertEqual(build_standard(), build_standard())
        self.assertEqual(build_standard(), STANDARD_BODY)
        explicit = build_standard(PLAN_8A_REGISTERS, READING_VOCABULARY, GUARD_PARAMETERS)
        self.assertEqual(explicit, STANDARD_BODY)
        self.assertEqual(
            build_standard(dict(PLAN_8A_REGISTERS), list(READING_VOCABULARY),
                           dict(GUARD_PARAMETERS)),
            STANDARD_BODY,
        )

    def test_item38_a_non_default_argument_is_refused_not_half_honoured(self):
        """Item 38: a successor standard is a source edit, never a call.

        ``build_standard(vocabulary=...)`` used to return a body whose
        ``vocabulary`` section was narrowed while the rubric's own values, the
        top-level ``reopen_reasons`` and ``role_contracts.schemas_sha256`` still
        carried the module defaults - a standard that contradicted itself.
        """

        for kwargs in (
            {"vocabulary": ("retains", "unresolved")},
            {"vocabulary": list(READING_VOCABULARY) + ["extends"]},
            {"params": {**GUARD_PARAMETERS, "judge_seats": 3}},
            {"params": {**GUARD_PARAMETERS, "reopen_reasons": ("appellate-ruling",)}},
            {"registers": {rid: PLAN_8A_REGISTERS[rid] for rid in ("T", "E", "D")}},
        ):
            with self.subTest(**{k: str(v)[:30] for k, v in kwargs.items()}):
                with self.assertRaises(StandardInvalid) as caught:
                    build_standard(**kwargs)
                self.assertEqual(caught.exception.code, "STANDARD_ARGUMENT_REFUSED")
        # The defaults, however spelled, still build the one body.
        self.assertEqual(build_standard(vocabulary=list(READING_VOCABULARY)),
                         STANDARD_BODY)

    def test_item38_a_source_edit_changes_the_bytes_and_the_digest(self):
        """The other half of item 38: the successor route that does work."""

        narrowed = MappingProxyType({**GUARD_PARAMETERS, "judge_seats": 3})
        with mock.patch.object(standard, "GUARD_PARAMETERS", narrowed):
            moved = build_standard()
        self.assertNotEqual(moved, STANDARD_BODY)
        self.assertNotEqual(hashlib.sha256(moved).hexdigest(), STANDARD_BODY_SHA256)
        self.assertEqual(build_standard(), STANDARD_BODY, "the change did not stick")
        # ... and the successor body agrees with itself at every site.
        body = standard_body(moved)
        self.assertEqual(body["guard_parameters"]["judge_seats"], 3)
        self.assertEqual(body["reopen_reasons"],
                         body["guard_parameters"]["reopen_reasons"])

    def test_build_standard_is_pure_and_does_not_mutate_the_module_defaults(self):
        before = dict(GUARD_PARAMETERS)
        body = standard_body(build_standard())
        body["guard_parameters"]["judge_seats"] = 99
        body["registers"]["T"]["plan_text"] = "tampered"
        self.assertEqual(dict(GUARD_PARAMETERS), before)
        self.assertEqual(PLAN_8A_REGISTERS["T"].plan_text,
                         PLAN_8A_MIRROR["registers"]["T"]["plan_text"])
        self.assertEqual(build_standard(), STANDARD_BODY)


class AcceptanceModes(unittest.TestCase):
    """Clause: the body declares mode absolute for relation trials and pairwise for marks."""

    def test_the_body_declares_mode_absolute_for_relation_trials_and_pairwise_for_marks(self):
        body = standard_body(STANDARD_BODY)
        self.assertEqual(body["rubric"]["relation"]["mode"], MODE_ABSOLUTE)
        self.assertEqual(body["rubric"]["contrast-mark"]["mode"], MODE_PAIRWISE)
        self.assertEqual(RUBRIC_V1["relation"].mode, MODE_ABSOLUTE)
        self.assertEqual(RUBRIC_V1["contrast-mark"].mode, MODE_PAIRWISE)
        self.assertEqual(sorted(body["rubric"]), ["contrast-mark", "relation"])
        self.assertEqual(body["rubric"]["relation"]["values"], list(READING_VOCABULARY))
        self.assertEqual(body["rubric"]["contrast-mark"]["values"], list(standard.MARKS))
        self.assertEqual(body["modes"], [MODE_ABSOLUTE, MODE_PAIRWISE])


class ContentAddressing(unittest.TestCase):
    """The body text, the anchors, the guard parameters and the ceiling are pinnable data."""

    def test_the_standard_body_and_the_ceiling_text_are_content_addressed_by_sha256(self):
        self.assertEqual(hashlib.sha256(STANDARD_BODY).hexdigest(), STANDARD_BODY_SHA256)
        self.assertEqual(
            hashlib.sha256(CEILING_TEXT.encode("utf-8")).hexdigest(), CEILING_SHA256
        )
        self.assertEqual(standard.CEILING_PATH.read_bytes(), CEILING_TEXT.encode("utf-8"))
        self.assertEqual(standard_body(STANDARD_BODY)["ceiling"]["sha256"], CEILING_SHA256)

    def test_the_shipped_data_files_live_under_the_package_data_directory(self):
        data = REPO / "src/minireason/loop/data"
        self.assertEqual(standard.PLAN_8A_MIRROR_PATH.parent, data)
        self.assertEqual(standard.CEILING_PATH.parent, data)
        for path in (standard.PLAN_8A_MIRROR_PATH, standard.CEILING_PATH):
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file())

    def test_the_anchor_exemplars_and_guard_parameters_are_inside_the_pinned_body(self):
        body = standard_body(STANDARD_BODY)
        self.assertEqual(
            [anchor["id"] for anchor in body["calibration_anchors"]],
            [anchor.id for anchor in CALIBRATION_ANCHORS],
        )
        self.assertEqual(len(CALIBRATION_ANCHORS), 5)
        sustaining = [a for a in CALIBRATION_ANCHORS if a.must_sustain]
        controls = [a for a in CALIBRATION_ANCHORS if not a.must_sustain]
        self.assertEqual(
            sorted(a.expected_relation for a in sustaining), ["rejects-with-reason", "retains"]
        )
        self.assertTrue(all(a.expected_relation is None for a in controls))
        self.assertTrue(all(a.ground_truth_reason.strip() for a in CALIBRATION_ANCHORS))
        self.assertEqual(body["guard_parameters"]["paraphrase_n"], 2)
        self.assertEqual(body["guard_parameters"]["schema_repair_budget"], 0)
        self.assertEqual(body["guard_parameters"]["judge_seats"], 2)
        self.assertEqual(body["guard_parameters"]["min_judge_families"], 2)
        self.assertIn("never averaged", body["guard_parameters"]["unanimity_rule"])


class CeilingIsData(unittest.TestCase):
    """The CEILING sentences are shipped data, and clause one is a template."""

    def test_every_required_ceiling_sentence_is_a_verbatim_paragraph_of_the_ceiling_text(self):
        self.assertEqual(len(CEILING_REQUIRED_SENTENCES), 11)
        for sentence in CEILING_REQUIRED_SENTENCES:
            with self.subTest(sentence=sentence[:48]):
                self.assertIn(sentence, CEILING_TEXT)
                self.assertNotIn("\n", sentence)
                self.assertFalse(sentence.startswith(">"))
        self.assertNotIn(CEILING_CLAIM_TEMPLATE, CEILING_REQUIRED_SENTENCES)
        self.assertTrue(CEILING_TEXT.startswith(CEILING_CLAIM_TEMPLATE))

    def test_the_ceiling_names_the_fw5_limits_the_run_may_not_claim(self):
        joined = "\n".join(CEILING_REQUIRED_SENTENCES)
        self.assertIn("This run cannot claim FW5:628's witness of reason use.", joined)
        self.assertIn("The strongest positive outcome available is *consistent-with*.", joined)
        self.assertIn("An unresolved cell proves neither presence nor absence", joined)
        self.assertIn("non-evaluability is not refutation", joined)
        self.assertIn("No count is an automatic warrant", joined)
        self.assertIn("never summed, averaged, weighted or ranked", joined)
        self.assertIn("never competitors", joined)
        self.assertIn("It is never an absence of relations.", joined)
        self.assertIn("unrefuted and unsupported, not excluded", joined)
        self.assertIn("does not describe the run as validated, checked or confirmed", joined)

    def test_the_ceiling_prints_unread_unresolved_and_machine_unresolved_as_three_states(self):
        joined = "\n".join(CEILING_REQUIRED_SENTENCES)
        self.assertIn("Three cell states are distinct and are printed as three things.", joined)
        for state in ("*unread*", "*unresolved*", "*machine-unresolved*"):
            with self.subTest(state=state):
                self.assertIn(state, joined)

    def test_the_ceiling_names_the_two_narrowings_of_published_instruments(self):
        joined = "\n".join(CEILING_REQUIRED_SENTENCES)
        self.assertIn("Two published instruments were narrowed", joined)
        self.assertIn("`ROOT_READING_VOCABULARY`", joined)
        self.assertIn("root has not read it", joined)

    def test_the_only_occurrence_of_the_token_exhaustion_is_the_ceilings_own_denial(self):
        body = STANDARD_BODY.decode("utf-8")
        occurrences = [
            sentence for sentence in CEILING_REQUIRED_SENTENCES if "exhaustion" in sentence
        ]
        self.assertEqual(len(occurrences), 1)
        self.assertIn("not exhaustion of the inquiry", occurrences[0])
        self.assertEqual(body.count("exhaustion"), body.count("not exhaustion of the inquiry"))
        self.assertEqual(body.count("exhaustion"), 1)


class TheCeilingAndTheBlockCodeTableAgree(unittest.TestCase):
    """Wave-0 integration decision 2: every reason the ceiling names by name has
    a BLOCK_CODES entry, and every BLOCK_CODES entry but one is named there."""

    def ceiling_reasons(self) -> list[str]:
        """The reasons the ceiling's block-register clause names, from its bytes."""

        clause = [s for s in CEILING_REQUIRED_SENTENCES
                  if "The block register by reason code" in s]
        self.assertEqual(len(clause), 1, "the ceiling names one block register")
        register = clause[0].split("The block register by reason code")[1]
        register = register.split("is printed with counts")[0]
        return re.findall(r"`([a-z][a-z-]*)`", register)

    def test_the_ceiling_names_nine_reasons_and_types_lists_the_same_nine(self):
        named = self.ceiling_reasons()
        self.assertEqual(len(named), 9)
        self.assertEqual(tuple(named), loop_types.CEILING_BLOCK_REASONS)

    def test_every_ceiling_named_reason_has_a_block_codes_entry(self):
        for reason in self.ceiling_reasons():
            with self.subTest(reason=reason):
                self.assertIn(f"blocked:{reason}", loop_types.BLOCK_CODES)
                self.assertEqual(loop_types.block_code(reason), f"blocked:{reason}")

    def test_every_block_codes_entry_but_constitution_is_named_by_the_ceiling(self):
        named = {f"blocked:{reason}" for reason in self.ceiling_reasons()}
        extra = set(loop_types.BLOCK_CODES) - named
        self.assertEqual(
            extra, {"blocked:constitution"},
            "constitution is the one block code the frozen ceiling does not name; "
            "anything else here is a code the ceiling promises to print and does not")
        self.assertNotIn("constitution", self.ceiling_reasons())

    def test_the_register_is_printed_with_counts_and_a_high_rate_is_not_an_absence(self):
        clause = [s for s in CEILING_REQUIRED_SENTENCES
                  if "The block register by reason code" in s][0]
        self.assertIn("A high block rate is the instrument declining to read.", clause)
        self.assertIn("It is never an absence of relations.", clause)
        self.assertIn("printed with counts on every table", clause)


class TheExhaustionScanExemptsTheCeilingsOwnDenial(unittest.TestCase):
    """Wave-0 integration decision 4: the token appears once, inside a denial."""

    def test_the_frozen_ceiling_passes_the_scan(self):
        self.assertIsNone(standard.assert_no_exhaustion_claim(CEILING_TEXT, "CEILING.md"))
        self.assertIsNone(standard.assert_no_exhaustion_claim(STANDARD_BODY.decode("utf-8")))
        for sentence in CEILING_REQUIRED_SENTENCES:
            with self.subTest(sentence=sentence[:40]):
                self.assertIsNone(standard.assert_no_exhaustion_claim(sentence))

    def test_the_exempt_phrase_is_the_ceilings_own_denial_and_occurs_once(self):
        self.assertEqual(standard.CEILING_EXHAUSTION_DENIAL,
                         "not exhaustion of the inquiry")
        self.assertEqual(CEILING_TEXT.count(standard.CEILING_EXHAUSTION_DENIAL), 1)
        self.assertEqual(CEILING_TEXT.count("exhaust"), 1)

    def test_a_renderer_string_carrying_the_token_outside_that_phrase_is_refused(self):
        for text in (
            "The loop stopped after exhaustion of the call budget.",
            "stop_reason: exhaustion",
            "The inquiry was exhausted.",
            "This is an exhaustive reading of the rows.",
            "EXHAUSTION OF THE INQUIRY",                      # not the denial
            CEILING_TEXT + "\n\nThe budget was reached; exhaustion followed.",
        ):
            with self.subTest(text=text[:48]):
                with self.assertRaises(StandardInvalid) as caught:
                    standard.assert_no_exhaustion_claim(text, "CLOSING.md")
                self.assertEqual(caught.exception.code, "RESOURCE_BOUNDARY_MISDESCRIBED")
                self.assertIn("CLOSING.md", str(caught.exception))
                self.assertIn(caught.exception.code, loop_types.FAILURE_CODES)

    def test_the_boundary_the_stop_vocabulary_actually_names_is_admitted(self):
        for text in ("stop_reason: resource_boundary",
                     "A reached ceiling is a declared resource boundary, "
                     "not exhaustion of the inquiry."):
            with self.subTest(text=text[:40]):
                self.assertIsNone(standard.assert_no_exhaustion_claim(text))
        self.assertIn("resource_boundary", loop_types.STOP_REASONS)

    def test_the_scan_is_pure(self):
        text = CEILING_TEXT
        standard.assert_no_exhaustion_claim(text)
        self.assertEqual(text, CEILING_TEXT)


class VocabularyIsClosedAgainstItsPublishedNote(unittest.TestCase):
    """The six values are imported, and the note they are closed against rides along."""

    def test_the_vocabulary_is_the_six_published_values_imported_not_retyped(self):
        self.assertEqual(READING_VOCABULARY, tuple(use_relation_h005.ROOT_READING_VOCABULARY))
        self.assertEqual(len(READING_VOCABULARY), 6)
        self.assertIn("unresolved", READING_VOCABULARY)
        self.assertEqual(
            standard.NOMINABLE_RELATIONS,
            tuple(v for v in READING_VOCABULARY if v != "unresolved"),
        )
        self.assertNotIn(standard.NONE_TOKEN, READING_VOCABULARY)

    def test_the_published_non_exclusivity_note_is_reproduced_verbatim(self):
        self.assertEqual(standard.VOCABULARY_NOTE, published_vocabulary_note())
        self.assertIn("It is not a closed single-valued enum", standard.VOCABULARY_NOTE)
        self.assertEqual(
            standard_body(STANDARD_BODY)["vocabulary"]["published_note"],
            standard.VOCABULARY_NOTE,
        )

    def test_the_instrument_banner_is_imported_not_retyped(self):
        self.assertEqual(standard.READING_BANNER, use_relation_h005.USE_RELATION_BANNER)
        self.assertIn("An empty cell is an **unread row**", standard.READING_BANNER)

    def test_the_outside_vocabulary_escape_forces_unresolved_and_preserves_the_text(self):
        self.assertEqual(standard.OUTSIDE_VOCABULARY_FIELD, "outside_vocabulary")
        effect = standard.OUTSIDE_VOCABULARY_EFFECT
        self.assertIn("unresolved", effect)
        self.assertIn("outside-vocabulary", effect)
        self.assertIn("preserves the text", effect)


class HouseRules(unittest.TestCase):
    """No scalar meter, no scoring key, no count doing warrant work."""

    def test_no_scoring_key_appears_anywhere_in_the_body(self):
        body = standard_body(STANDARD_BODY)
        forbidden = {
            "score", "scores", "scoring", "rank", "ranking", "ranks", "merit", "grade",
            "grades", "rating", "ratings", "points", "novelty", "creativity", "quality",
            "winner", "win", "best", "worst", "better", "worse", "weight", "weights",
            "percentile", "verdict",
        }
        keys = {path.split(".")[-1].split("[")[0] for path, _ in walk(body)}
        self.assertEqual(keys & forbidden, set())

    def test_every_integer_in_the_body_is_a_declared_bound(self):
        """Ruling 7's own check, at this layer: no number in the body is a metric.

        Two prefixes and no others. ``guard_parameters.`` are the seat counts and
        spend bounds §2.1 freezes; ``role_contracts.word_limits.`` are §2.3's prose
        bounds, which moved into the body so that editing one changes the digest a
        plan pins (S4). Each is a declared bound on what the machinery may do, and
        none of them is a measure of any reading. There are still no floats at all.
        """

        body = standard_body(STANDARD_BODY)
        allowed = ("guard_parameters.", "role_contracts.word_limits.")
        integers = [
            (path, value)
            for path, value in walk(body)
            if isinstance(value, int) and not isinstance(value, bool)
        ]
        self.assertTrue(integers)
        for path, value in integers:
            with self.subTest(path=path):
                self.assertTrue(path.startswith(allowed), path)
        self.assertFalse([v for _, v in walk(body) if isinstance(v, float)])
        # And the word limits in the body are the ones the contracts enforce.
        limits = body["role_contracts"]["word_limits"]
        self.assertEqual(
            {(role, field): limit
             for role, fields in limits.items() for field, limit in fields.items()},
            dict(standard.WORD_LIMITS))

    def test_the_rubric_says_a_reading_is_not_a_merit_predicate_and_unresolved_is_first_class(self):
        relation = flat(RUBRIC_V1["relation"].body)
        self.assertIn("no merit predicate here (FW5:849)", relation)
        self.assertIn("never competitors", relation)
        self.assertIn("`unresolved` is a first-class outcome", relation)
        self.assertIn("Non-evaluability is not refutation", relation)
        self.assertIn("neither presence nor absence (FW5:634)", relation)
        self.assertIn("never averaged and never settled by majority", relation)
        self.assertIn("never an attack edge", relation)
        self.assertIn("*consistent-with*", relation)

    def test_the_mark_rubric_refuses_aggregation_and_reports_absent_data_as_absent(self):
        marks = flat(RUBRIC_V1["contrast-mark"].body)
        self.assertIn("never summed, averaged, weighted, ranked or reduced to one mark", marks)
        self.assertIn("Counts may defeat; they never warrant.", marks)
        self.assertIn("never as an absence of difference", marks)
        self.assertIn("never `differs`", marks)


class ReopenReasonsAndDifferenceKinds(unittest.TestCase):
    """The pre-registered reopen list, and the closed per-register kind sets."""

    def test_the_reopen_reason_list_is_the_three_pre_registered_reasons(self):
        self.assertEqual(REOPEN_REASONS, ("new-material", "repaired-guard", "appellate-ruling"))
        self.assertEqual(
            standard_body(STANDARD_BODY)["reopen_reasons"], list(REOPEN_REASONS)
        )
        self.assertEqual(tuple(GUARD_PARAMETERS["reopen_reasons"]), REOPEN_REASONS)

    def test_the_difference_kind_sets_are_closed_and_keep_every_sketched_token(self):
        sketched = {
            "T": "target_set_membership",
            "E": "record_engaged",
            "D": "disposition_value",
            "G": "grounds_source",
        }
        for rid, token in sketched.items():
            with self.subTest(register=rid):
                self.assertIn(token, DIFFERENCE_KINDS[rid])
        self.assertEqual(sorted(DIFFERENCE_KINDS), sorted(REGISTER_IDS))
        for rid in REGISTER_IDS:
            tokens = DIFFERENCE_KINDS[rid]
            with self.subTest(register=rid):
                self.assertEqual(len(set(tokens)), len(tokens))
                self.assertTrue(tokens)
        self.assertEqual(len(DIFFERENCE_KINDS["G"]), 1)
        for rid in ("T", "E", "D"):
            self.assertGreater(len(DIFFERENCE_KINDS[rid]), 1, rid)
        all_tokens = [t for rid in REGISTER_IDS for t in DIFFERENCE_KINDS[rid]]
        self.assertEqual(len(set(all_tokens)), len(all_tokens))


class Refusals(unittest.TestCase):
    """build_standard and standard_body refuse, by declared code, rather than degrade."""

    def build_with_default(self, name, value):
        """Build after a **source edit**: the successor route item 38 leaves open."""

        with mock.patch.object(standard, name, value):
            return build_standard()

    def test_build_standard_refuses_a_register_set_that_is_not_the_four_plan_8a_registers(self):
        three = {rid: PLAN_8A_REGISTERS[rid] for rid in ("T", "E", "D")}
        with self.assertRaises(StandardInvalid) as caught:
            self.build_with_default("PLAN_8A_REGISTERS", three)
        self.assertEqual(caught.exception.code, "REGISTER_SET_MISMATCH")

    def test_build_standard_refuses_a_register_with_empty_plan_text(self):
        hollow = dict(PLAN_8A_REGISTERS)
        source = PLAN_8A_REGISTERS["G"]
        hollow["G"] = Register(
            id="G", name=source.name, plan_text="   ", reads=source.reads,
            differs_iff=source.differs_iff, difference_kinds=source.difference_kinds,
            carries_falsifiers=source.carries_falsifiers,
        )
        with self.assertRaises(StandardInvalid) as caught:
            self.build_with_default("PLAN_8A_REGISTERS", hollow)
        self.assertEqual(caught.exception.code, "REGISTER_TEXT_EMPTY")

    def test_build_standard_refuses_a_vocabulary_that_is_not_closed_under_the_published_six(self):
        with self.assertRaises(StandardInvalid) as caught:
            standard._validate_vocabulary(READING_VOCABULARY + ("extends",))
        self.assertEqual(caught.exception.code, "VOCABULARY_NOT_CLOSED")

    def test_build_standard_refuses_a_vocabulary_that_drops_unresolved(self):
        with self.assertRaises(StandardInvalid) as caught:
            self.build_with_default("READING_VOCABULARY", standard.NOMINABLE_RELATIONS)
        self.assertEqual(caught.exception.code, "UNRESOLVED_NOT_IN_VOCABULARY")

    def test_build_standard_refuses_an_unknown_missing_or_out_of_range_guard_parameter(self):
        cases = {
            "GUARD_PARAMETER_UNKNOWN": {**GUARD_PARAMETERS, "audit_period": 4},
            "GUARD_PARAMETER_MISSING": {
                k: v for k, v in GUARD_PARAMETERS.items() if k != "paraphrase_n"
            },
            "GUARD_PARAMETER_INVALID": {**GUARD_PARAMETERS, "judge_seats": 1},
        }
        for code, params in cases.items():
            with self.subTest(code=code):
                with self.assertRaises(StandardInvalid) as caught:
                    self.build_with_default("GUARD_PARAMETERS", MappingProxyType(params))
                self.assertEqual(caught.exception.code, code)

    def test_build_standard_refuses_a_reopen_reason_outside_the_pre_registered_list(self):
        with self.assertRaises(StandardInvalid) as caught:
            self.build_with_default(
                "GUARD_PARAMETERS",
                MappingProxyType({**GUARD_PARAMETERS, "reopen_reasons": ("try-again",)}))
        self.assertEqual(caught.exception.code, "REOPEN_REASON_UNKNOWN")

    def test_item40_standard_body_refuses_every_body_build_standard_would(self):
        """Item 40(a): the parse door used to admit what the build door refused."""

        cases = {
            "REGISTER_SET_MISMATCH": lambda b: b["registers"].pop("G"),
            "REGISTER_TEXT_EMPTY": lambda b: b["registers"]["G"].update(plan_text="  "),
            "DIFFERENCE_KIND_SET_EMPTY":
                lambda b: b["registers"]["G"].update(difference_kinds=[]),
            "UNRESOLVED_NOT_IN_VOCABULARY":
                lambda b: b["vocabulary"].update(values=["retains"]),
            "VOCABULARY_NOT_CLOSED":
                lambda b: b["vocabulary"]["values"].append("is-better-than"),
            "GUARD_PARAMETER_INVALID":
                lambda b: b["guard_parameters"].update(judge_seats=1),
            "GUARD_PARAMETER_UNKNOWN":
                lambda b: b["guard_parameters"].update(audit_period=4),
        }
        for code, damage in cases.items():
            with self.subTest(code=code):
                body = json.loads(STANDARD_BODY.decode("utf-8"))
                damage(body)
                with self.assertRaises(StandardInvalid) as caught:
                    standard_body(json.dumps(body))
                self.assertEqual(caught.exception.code, code)

    def test_item40_the_two_reopen_lists_of_a_body_must_agree(self):
        body = json.loads(STANDARD_BODY.decode("utf-8"))
        body["reopen_reasons"] = list(REOPEN_REASONS)[:1]
        with self.assertRaises(StandardInvalid) as caught:
            standard_body(json.dumps(body))
        self.assertEqual(caught.exception.code, "REOPEN_REASON_UNKNOWN")
        self.assertIn("disagree", caught.exception.detail)

    def test_standard_body_round_trips_the_built_bytes_and_the_same_text(self):
        parsed = standard_body(STANDARD_BODY)
        self.assertEqual(parsed, standard_body(STANDARD_BODY.decode("utf-8")))
        self.assertEqual(parsed["spec_id"], SPEC_ID)
        self.assertEqual(parsed["standard_name"], "std:reading-rubric/v1")
        self.assertEqual(parsed["commitment_eval"], "rubric:reading-v1")

    def test_standard_body_refuses_malformed_foreign_or_truncated_content(self):
        good = json.loads(STANDARD_BODY.decode("utf-8"))
        cases = {
            "STANDARD_BODY_MALFORMED": b"{not json",
            "STANDARD_SCHEMA_MISMATCH": json.dumps({**good, "schema": "other"}).encode(),
            "SPEC_ID_MISMATCH": json.dumps({**good, "spec_id": "reading-v2"}).encode(),
            "STANDARD_SECTION_MISSING": json.dumps(
                {k: v for k, v in good.items() if k != "falsifiers"}
            ).encode(),
        }
        for code, raw in cases.items():
            with self.subTest(code=code):
                with self.assertRaises(StandardInvalid) as caught:
                    standard_body(raw)
                self.assertEqual(caught.exception.code, code)

    def test_standard_body_refuses_a_body_carrying_a_scoring_key(self):
        good = json.loads(STANDARD_BODY.decode("utf-8"))
        good["registers"]["T"]["rank"] = 1
        with self.assertRaises(StandardInvalid) as caught:
            standard_body(json.dumps(good).encode())
        self.assertEqual(caught.exception.code, "SCORING_KEY_FORBIDDEN")

    def test_a_non_object_body_is_refused(self):
        with self.assertRaises(StandardInvalid) as caught:
            standard_body(b"[1, 2, 3]")
        self.assertEqual(caught.exception.code, "STANDARD_BODY_MALFORMED")


class PublicInterface(unittest.TestCase):
    """Downstream waves import these names; they are exported and they are stable."""

    def test_the_module_exports_the_wave_plan_public_interface(self):
        for name in ("RUBRIC_V1", "SPEC_ID", "build_standard", "standard_body",
                     "PLAN_8A_REGISTERS", "FALSIFIER_MAP", "REOPEN_REASONS"):
            with self.subTest(name=name):
                self.assertIn(name, standard.__all__)
                self.assertTrue(hasattr(standard, name))
        for name in standard.__all__:
            with self.subTest(exported=name):
                self.assertTrue(hasattr(standard, name))

    def test_the_spec_id_is_the_half_after_rubric_in_the_commitment_eval(self):
        self.assertEqual(SPEC_ID, "reading-v1")
        self.assertEqual(standard.RUBRIC_EVAL, f"rubric:{SPEC_ID}")
        self.assertTrue(standard.RUBRIC_EVAL.startswith("rubric:"))
        self.assertEqual(standard.STANDARD_NAME, "std:reading-rubric/v1")


class TheShippedBytesAreTheBytesThatWerePinned(unittest.TestCase):
    """S1: a CRLF checkout would move two digests and nothing would say so.

    ``standard`` reads its data files in text mode for the required sentences and
    in byte mode for the digest, so a checkout that translated LF to CRLF parsed
    every clause exactly as before while ``CEILING_SHA256`` - and through it
    ``STANDARD_BODY_SHA256``, and through that ``loop_plan_id`` - moved. The
    repository's own rule (``docs/lessons/operations.md``, OPS-20260914-LEDGERCRLF)
    is that the scope is any tracked file whose bytes are evidence; ``.gitattributes``
    marks these two and the ledger, and these are the digests it protects.
    """

    #: Computed from the shipped LF bytes. A literal, not a recomputation: a test
    #: that re-derives the number it is checking cannot fail.
    CEILING = "1e26be087483fd1b9c8e2c403cfae646fb07ebc773f23434a0c4dfab3ed04c1e"
    #: Moved twice, deliberately, and each move is named here.
    #:
    #: 1. The hardening pass, item 41: two ``plan_grounding`` strings that
    #:    paraphrased the plan (an em dash written as a hyphen in T's
    #:    ``target_prefix_source``; E's ``record_engaged`` truncated) were
    #:    replaced with the plan's own bytes, inside a body whose M2 says "not
    #:    paraphrased". ``6c894deb851982bf7b5e7317066896a36c4b5898308519c012a3cd1ef5100fcb``.
    #: 2. The wave-2 integration, REVIEW-WAVE1 B3 / REVIEW-PREREG PR-06: the
    #:    ``self-juxtaposition`` calibration anchor was built from two copies of
    #:    one record, so every substring of it occurred twice, no quote could
    #:    satisfy G2(a), and an anchor declared ``must_sustain`` blocked on every
    #:    window for every seat for ever. It is now built with the referring
    #:    region alone.
    #:
    #: The ceiling's bytes did not move in either, and no other section did.
    #: 3. The wave-2 integration again: ``plan_8a_mirror.json`` pinned C001's
    #:    ``PLAN.md`` at its pre-append bytes, and the live file on the branch
    #:    carries an appended §15 (commit ``2d7239a``, 88 lines added, none
    #:    edited). The mirror was re-derived against the live bytes - every
    #:    mirrored §8a block is byte-identical in them - so the pin moved and
    #:    the body's ``source`` block with it. No plan was ever minted, so no
    #:    published identity moved.
    BODY = "a9007dc73c748cfff974a1a3d77098d380ec153b1b8cf93f513cafa3ea0572d7"

    def test_the_shipped_data_files_carry_no_carriage_return(self):
        for path in (standard.CEILING_PATH, standard.PLAN_8A_MIRROR_PATH):
            with self.subTest(path=path.name):
                self.assertNotIn(b"\r", path.read_bytes())

    def test_the_two_digests_are_the_pinned_literals(self):
        self.assertEqual(CEILING_SHA256, self.CEILING)
        self.assertEqual(STANDARD_BODY_SHA256, self.BODY)
        self.assertEqual(hashlib.sha256(standard.CEILING_PATH.read_bytes()).hexdigest(),
                         self.CEILING)

    def test_gitattributes_marks_every_file_whose_bytes_are_evidence(self):
        attributes = REPO / ".gitattributes"
        self.assertTrue(attributes.is_file(), "no .gitattributes at the repository root")
        text = attributes.read_text(encoding="utf-8")
        rules = [line.split() for line in text.splitlines()
                 if line.strip() and not line.lstrip().startswith("#")]
        marked = {pattern: tuple(rest) for pattern, *rest in rules}
        self.assertEqual(marked, {"src/minireason/loop/data/**": ("-text",),
                                  "docs/DECISION_LEDGER.md": ("-text",)})
        # No global rule: this repository carries historical CRLF in tracked files
        # and renormalising them all would bury the two that are evidence.
        self.assertNotIn("text=auto", text.split("#")[0] if "#" in text else text)
        for pattern in marked:
            self.assertNotIn("*", pattern.replace("**", ""), pattern)

    def test_a_crlf_copy_of_the_data_would_move_the_digest(self):
        crlf = standard.CEILING_PATH.read_bytes().replace(b"\n", b"\r\n")
        self.assertNotEqual(hashlib.sha256(crlf).hexdigest(), CEILING_SHA256)
        # ... while every required sentence still parses, which is why only the
        # digest catches it.
        text = crlf.decode("utf-8")
        for sentence in CEILING_REQUIRED_SENTENCES:
            self.assertIn(sentence, text.replace("\r\n", "\n"))


class TheSectionTwoThreeContractsArePinnedIntoTheBody(unittest.TestCase):
    """S4: editing a role schema or a word limit now changes the pinned digest."""

    def test_the_body_carries_the_word_limits_and_the_schema_digest(self):
        section = standard_body(STANDARD_BODY)["role_contracts"]
        self.assertEqual(section["roles"], list(standard.ROLE_NAMES))
        self.assertEqual(section["schemas_sha256"], standard.ROLE_SCHEMAS_SHA256)
        self.assertEqual(section["word_limits"]["critic"]["case"], 400)
        self.assertEqual(section["word_limits"]["judge"]["reading_note"], 120)

    def test_mutating_a_word_limit_changes_the_body_digest(self):
        raised = dict(standard.WORD_LIMITS)
        raised[("judge", "reading_note")] = 121
        with mock.patch.object(standard, "WORD_LIMITS", MappingProxyType(raised)):
            moved = build_standard()
        self.assertNotEqual(hashlib.sha256(moved).hexdigest(), STANDARD_BODY_SHA256)
        self.assertEqual(build_standard(), STANDARD_BODY, "the change did not stick")

    def test_mutating_a_role_schema_changes_the_body_digest(self):
        edited = {role: json.loads(json.dumps(schema))
                  for role, schema in standard.SCHEMAS.items()}
        edited["judge"]["properties"]["reading_note"]["minLength"] = 1
        with mock.patch.object(standard, "SCHEMAS", MappingProxyType(edited)):
            moved = build_standard()
        self.assertNotEqual(hashlib.sha256(moved).hexdigest(), STANDARD_BODY_SHA256)
        self.assertEqual(build_standard(), STANDARD_BODY)

    def test_the_contracts_module_re_exports_the_standards_own_objects(self):
        from minireason.loop import contracts

        for name in ("SCHEMAS", "WORD_LIMITS", "ROLE_NAMES", "ROLE_BINDING_FIELDS",
                     "ALL_DIFFERENCE_KINDS", "CRITIC_SCHEMA", "DEFENDER_SCHEMA",
                     "JUDGE_SCHEMA", "MARKER_SCHEMA", "VARIATOR_SCHEMA"):
            with self.subTest(name=name):
                self.assertIs(getattr(contracts, name), getattr(standard, name))


class TheUnanimityRuleDescribesEveryAdmissiblePanel(unittest.TestCase):
    """S7: a successor standard with three seats must not ship a rule about two."""

    NUMERALS = ("both", "two", "three", "four", "five", "six", "seven", "eight",
                "pair", "either")

    def rendered_rule(self, judge_seats: int) -> str:
        params = MappingProxyType({**GUARD_PARAMETERS, "judge_seats": judge_seats})
        with mock.patch.object(standard, "GUARD_PARAMETERS", params):
            body = standard_body(build_standard())
        return body["guard_parameters"]["unanimity_rule"]

    def test_the_rule_names_no_number_of_seats_at_any_admissible_panel_size(self):
        low, high = standard._INT_PARAMS["judge_seats"]
        for seats in range(low, high + 1):
            with self.subTest(judge_seats=seats):
                rule = self.rendered_rule(seats)
                self.assertIn("every judge seat", rule.lower())
                self.assertIn("never settled by majority", rule)
                # No word-numeral, and no digit outside the FW5 citation.
                for numeral in self.NUMERALS:
                    self.assertNotIn(numeral, rule.lower(), numeral)
                self.assertFalse(
                    [ch for ch in re.sub(r"\(FW5:\d+\)", "", rule) if ch.isdigit()],
                    rule)

    def test_the_relation_rubric_agrees_with_the_rule(self):
        relation = flat(RUBRIC_V1["relation"].body)
        self.assertIn("Where the judge seats do not return the same ruling", relation)
        self.assertNotIn("both rulings", relation)
        self.assertNotIn("the two judge seats", relation)


class TheExhaustionScanSurvivesARenderer(unittest.TestCase):
    """S5: the exemption was byte-exact, and refused the ceiling it protects."""

    def test_the_denial_passes_re_wrapped_sentence_cased_and_upper_cased(self):
        for text in (
            "A reached ceiling is a declared resource boundary, Not exhaustion of "
            "the inquiry.",
            "NOT EXHAUSTION OF THE INQUIRY",
            "A reached ceiling is a declared resource boundary, not exhaustion of the\n"
            "inquiry, and this record states which was reached.",
            "  not   exhaustion\tof the\n  inquiry  ",
            standard.CEILING_EXHAUSTION_DENIAL.upper(),
        ):
            with self.subTest(text=" ".join(text.split())[:48]):
                self.assertIsNone(standard.assert_no_exhaustion_claim(text, "CLOSING.md"))

    def test_the_claim_is_still_refused_in_every_case_and_spelling(self):
        for text in ("the reading was exhaustive",
                     "The inquiry is EXHAUSTED.",
                     "stop_reason: Exhaustion",
                     "This is an exhaustive reading of the rows.",
                     # the smuggle: the denial embedded inside the claim
                     "The inquiry is exhaust" + standard.CEILING_EXHAUSTION_DENIAL + "ed.",
                     CEILING_TEXT + "\n\nThe budget was reached; exhaustion followed."):
            with self.subTest(text=" ".join(text.split())[:48]):
                with self.assertRaises(StandardInvalid) as caught:
                    standard.assert_no_exhaustion_claim(text, "CLOSING.md")
                self.assertEqual(caught.exception.code,
                                 "RESOURCE_BOUNDARY_MISDESCRIBED")


class TheHeaderScanIsTheOtherHalfOfG12(unittest.TestCase):
    """B2: G12 runs over every table header and every rendered file."""

    def test_a_header_row_carrying_any_forbidden_key_is_refused(self):
        for key in sorted(standard.FORBIDDEN_KEYS):
            for line in (f"| cell | {key} |\n|---|---|\n| a | b |\n",
                         f"| cell | relation |\n|---|---|\n",
                         f"# The {key} of each endpoint"):
                if key not in line:
                    continue
                with self.subTest(key=key, line=line[:40]):
                    with self.assertRaises(StandardInvalid) as caught:
                        standard.assert_no_scoring_headers(line, "READING_TABLE.md")
                    self.assertEqual(caught.exception.code, "SCORING_KEY_FORBIDDEN")
                    self.assertIn("READING_TABLE.md", str(caught.exception))
            with self.subTest(key=key, shape="heading"):
                with self.assertRaises(StandardInvalid):
                    standard.assert_no_scoring_headers(f"## {key.title()} by endpoint")
            with self.subTest(key=key, shape="delimited table"):
                with self.assertRaises(StandardInvalid):
                    standard.assert_no_scoring_headers(
                        f"cell | {key}\n--- | ---\na | b\n")

    def test_the_frozen_ceiling_and_a_clean_table_pass_unchanged(self):
        self.assertIsNone(standard.assert_no_scoring_headers(CEILING_TEXT, "CEILING.md"))
        self.assertIsNone(standard.assert_no_scoring_headers(
            STANDARD_BODY.decode("utf-8"), "standard body"))
        for sentence in CEILING_REQUIRED_SENTENCES:
            self.assertIsNone(standard.assert_no_scoring_headers(sentence))
        clean = (
            "# Reading table\n\n"
            "| cell | relation | passage | block reason |\n"
            "|---|---|---|---|\n"
            "| p1/n1#r3 | unresolved | - | blocked:operative-target |\n"
        )
        self.assertIsNone(standard.assert_no_scoring_headers(clean, "READING_TABLE.md"))

    def test_a_body_row_is_prose_and_a_scoring_word_in_it_is_not_a_header(self):
        table = ("| cell | note |\n"
                 "|---|---|\n"
                 "| p1/n1#r3 | the score of the match is not a key here |\n")
        self.assertIsNone(standard.assert_no_scoring_headers(table))

    def test_the_scan_is_pure_and_reads_only_its_argument(self):
        text = CEILING_TEXT
        standard.assert_no_scoring_headers(text)
        self.assertEqual(text, CEILING_TEXT)


class TheStandardReconcilesAConfig(unittest.TestCase):
    """B3: one function settles which owner of a guard parameter wins."""

    def test_the_frozen_defaults_reconcile_with_themselves(self):
        self.assertIsNone(standard.assert_config_matches_standard(
            {key: GUARD_PARAMETERS[key]
             for key in ("min_judge_families", "paraphrase_n", "schema_repair_budget")},
            REOPEN_REASONS))
        self.assertIsNone(standard.assert_config_matches_standard(None, None))

    def test_a_seats_block_that_is_not_a_mapping_is_refused(self):
        with self.assertRaises(StandardInvalid) as caught:
            standard.assert_config_matches_standard(["critic"], ())
        self.assertEqual(caught.exception.code, "GUARD_PARAMETER_INVALID")

    def test_every_refusal_names_a_code_the_failure_table_declares(self):
        for call in ((lambda: standard.assert_config_matches_standard(
                          {"paraphrase_n": 0}, ())),
                     (lambda: standard.assert_config_matches_standard(
                          {}, ["try-again"]))):
            with self.assertRaises(StandardInvalid) as caught:
                call()
            self.assertIn(caught.exception.code, loop_types.FAILURE_CODES)


class TheShippedDataFilesAreCheckedAtImport(unittest.TestCase):
    """Item 39: the two data files were loaded with no shape check at all."""

    def reload_with_data(self, **files: bytes):
        """Import a private copy of the module against a damaged data directory."""

        import importlib.util
        import tempfile

        source = Path(standard.__file__)
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory) / "data"
            data.mkdir()
            for name, shipped in (("ceiling_v1.md", standard.CEILING_PATH),
                                  ("plan_8a_mirror.json", standard.PLAN_8A_MIRROR_PATH)):
                body = files.get(name, shipped.read_bytes())
                if body is not None:
                    (data / name).write_bytes(body)
            copy = Path(directory) / "standard_under_test.py"
            copy.write_bytes(source.read_bytes())
            spec = importlib.util.spec_from_file_location(
                "minireason.loop._standard_under_test", copy)
            module = importlib.util.module_from_spec(spec)
            # ``dataclasses`` resolves annotations through ``sys.modules``, so the
            # module has to be registered before its body runs, and removed after
            # so no other test sees this copy.
            sys.modules[spec.name] = module
            try:
                spec.loader.exec_module(module)
            finally:
                sys.modules.pop(spec.name, None)
            return module

    def test_the_shipped_files_load_and_the_ceiling_holds_eleven_sentences(self):
        self.assertEqual(len(CEILING_REQUIRED_SENTENCES), 11)
        self.assertEqual(len(standard._CEILING_CLAUSES), 12)
        module = self.reload_with_data()
        self.assertEqual(module.STANDARD_BODY_SHA256, STANDARD_BODY_SHA256)

    def test_a_truncated_ceiling_is_refused_rather_than_silently_emptied(self):
        text = standard.CEILING_TEXT
        damaged = {
            "one clause": text.split("\n\n")[0] + "\n",
            "eleven clauses": "\n\n".join(text.split("\n\n")[:-1]),
            "thirteen clauses": text + "\n\n**And another thing.** Indeed.\n",
            "clause 0 replaced": "**What this run says.**" + text.split("**", 3)[-1],
        }
        for label, body in damaged.items():
            with self.subTest(damage=label):
                with self.assertRaises(loop_types.LoopError) as caught:
                    self.reload_with_data(ceiling_v1_md=None, **{
                        "ceiling_v1.md": body.encode("utf-8")})
                self.assertEqual(caught.exception.code, "CEILING_TEXT_MALFORMED")

    def test_a_ceiling_that_drops_a_block_reason_or_the_denial_is_refused(self):
        text = standard.CEILING_TEXT
        for damage in (text.replace("`provider`, ", ""),
                       text.replace("not exhaustion of the inquiry",
                                    "not the end of the inquiry")):
            with self.subTest(damage=damage[:0]):
                with self.assertRaises(loop_types.LoopError) as caught:
                    self.reload_with_data(**{"ceiling_v1.md": damage.encode("utf-8")})
                self.assertEqual(caught.exception.code, "CEILING_TEXT_MALFORMED")

    def test_a_widened_or_short_plan_mirror_is_refused(self):
        mirror = json.loads(standard.PLAN_8A_MIRROR_PATH.read_text(encoding="utf-8"))
        cases = {
            "PLAN_MIRROR_MALFORMED": [
                {**mirror, "marks": ["differs", "same", "unresolved", "better"]},
                {**mirror, "marks": ["differs", "same"]},
                {k: v for k, v in mirror.items() if k != "preamble"},
            ],
            "REGISTER_SET_MISMATCH": [
                {**mirror, "registers": {k: v for k, v in mirror["registers"].items()
                                         if k != "G"}},
                {**mirror, "registers": {**mirror["registers"], "Q": {}}},
            ],
            "REGISTER_TEXT_EMPTY": [
                {**mirror, "registers": {**mirror["registers"],
                                         "G": {**mirror["registers"]["G"],
                                               "plan_text": "   "}}},
            ],
        }
        for code, bodies in cases.items():
            for index, body in enumerate(bodies):
                with self.subTest(code=code, case=index):
                    with self.assertRaises(loop_types.LoopError) as caught:
                        self.reload_with_data(**{
                            "plan_8a_mirror.json": json.dumps(body).encode("utf-8")})
                    self.assertEqual(caught.exception.code, code)

    def test_a_missing_or_unparsable_data_file_is_a_loop_error_with_a_code(self):
        with self.assertRaises(loop_types.LoopError) as caught:
            self.reload_with_data(**{"plan_8a_mirror.json": None})
        self.assertEqual(caught.exception.code, "STANDARD_DATA_MISSING")
        with self.assertRaises(loop_types.LoopError) as caught:
            self.reload_with_data(**{"ceiling_v1.md": None})
        self.assertEqual(caught.exception.code, "STANDARD_DATA_MISSING")
        with self.assertRaises(loop_types.LoopError) as caught:
            self.reload_with_data(**{"plan_8a_mirror.json": b"{not json"})
        self.assertEqual(caught.exception.code, "STANDARD_DATA_MALFORMED")
        for code in ("STANDARD_DATA_MISSING", "STANDARD_DATA_MALFORMED",
                     "CEILING_TEXT_MALFORMED", "PLAN_MIRROR_MALFORMED",
                     "STANDARD_ARGUMENT_REFUSED"):
            self.assertIn(code, loop_types.FAILURE_CODES)


class TheHardeningPassPins(unittest.TestCase):
    """Items 40(b)-(d) and 41."""

    def test_item40b_preflight_compares_against_the_registered_body(self):
        """The comparison used to be against this module's own defaults."""

        registered = standard_body(STANDARD_BODY)["guard_parameters"]
        successor = {**registered, "paraphrase_n": 4, "judge_seats": 3}
        matching = {"paraphrase_n": 4, "min_judge_families": 2,
                    "schema_repair_budget": 0, "judges": ["a", "b", "c"]}
        # Against the successor body it registered, the matching config passes ...
        self.assertIsNone(standard.assert_config_matches_standard(
            matching, REOPEN_REASONS, guard_parameters=successor))
        # ... and the config that matches this module's defaults is refused.
        with self.assertRaises(StandardInvalid) as caught:
            standard.assert_config_matches_standard(
                {"paraphrase_n": 2}, REOPEN_REASONS, guard_parameters=successor)
        self.assertEqual(caught.exception.code, "GUARD_PARAMETER_INVALID")
        # The two-argument call still binds and still means the module default.
        self.assertIsNone(standard.assert_config_matches_standard(
            {"paraphrase_n": GUARD_PARAMETERS["paraphrase_n"]}, None))
        # A guard_parameters block missing what it is asked about is a refusal,
        # never a silent pass.
        with self.assertRaises(StandardInvalid) as caught:
            standard.assert_config_matches_standard({}, (), guard_parameters={})
        self.assertEqual(caught.exception.code, "GUARD_PARAMETER_MISSING")

    def test_item40c_the_denial_survives_every_rendering_of_it(self):
        """The exemption failed on the blockquote §6 uses, and on emphasis."""

        clause = [c for c in standard._CEILING_CLAUSES
                  if standard.CEILING_EXHAUSTION_DENIAL in c][0]
        renderings = []
        for width in (40, 50, 60, 70, 80):
            words, line, lines = clause.split(), "", []
            for word in words:
                if line and len(line) + 1 + len(word) > width:
                    lines.append(line)
                    line = word
                else:
                    line = f"{line} {word}".strip()
            lines.append(line)
            renderings.append("> " + "\n> ".join(lines))
            renderings.append("- " + "\n  ".join(lines))
            renderings.append("\n".join(lines))
        renderings.append(clause.replace("exhaustion", "*exhaustion*"))
        renderings.append(clause.replace("not exhaustion", "**not** exhaustion"))
        renderings.append("> " + clause)
        for text in renderings:
            with self.subTest(text=" ".join(text.split())[:44]):
                self.assertIsNone(standard.assert_no_exhaustion_claim(text, "CLOSING.md"))
        # The smuggle direction is unchanged.
        with self.assertRaises(StandardInvalid):
            standard.assert_no_exhaustion_claim(
                "> the inquiry was exhausted at cycle 3", "CLOSING.md")
        with self.assertRaises(StandardInvalid):
            standard.assert_no_exhaustion_claim("the run was *exhaust*ive", "CLOSING.md")

    def test_item40d_the_header_row_is_the_line_above_a_delimiter_row(self):
        """A prose line ending in '|' used to hide the next table's header."""

        hidden = ("A column may be read left to right |\n"
                  "| cell | score |\n"
                  "|---|---|\n"
                  "| a | b |\n")
        with self.assertRaises(StandardInvalid) as caught:
            standard.assert_no_scoring_headers(hidden, "READING_TABLE.md")
        self.assertEqual(caught.exception.code, "SCORING_KEY_FORBIDDEN")
        # A thematic break under prose is not a table header row.
        self.assertIsNone(standard.assert_no_scoring_headers(
            "the score of the match\n---\n\nnext section\n"))
        # A body row is still prose.
        self.assertIsNone(standard.assert_no_scoring_headers(
            "| cell | note |\n|---|---|\n| a | the score here |\n"))

    def test_item41_the_module_tables_are_read_only_views(self):
        for name in ("PLAN_8A_MIRROR", "RUBRIC_V1", "PLAN_8A_REGISTERS",
                     "DIFFERENCE_KINDS", "FALSIFIER_MAP", "GUARD_PARAMETERS",
                     "WORD_LIMITS", "SCHEMAS"):
            with self.subTest(name=name):
                table = getattr(standard, name)
                self.assertIsInstance(table, MappingProxyType)
                with self.assertRaises(TypeError):
                    table["nope"] = 1

    def test_item41_every_plan_grounding_is_the_plans_own_bytes(self):
        """M2 says "not paraphrased"; two strings were paraphrases."""

        mirror = json.loads(standard.PLAN_8A_MIRROR_PATH.read_text(encoding="utf-8"))
        for rid in REGISTER_IDS:
            flat = " ".join(mirror["registers"][rid]["plan_text"].split())
            for kind in PLAN_8A_REGISTERS[rid].difference_kinds:
                with self.subTest(register=rid, token=kind.token):
                    self.assertIn(" ".join(kind.plan_grounding.split()), flat)

    def test_item41_the_vocabulary_note_is_the_instruments_own_comment_block(self):
        source = Path(use_relation_h005.__file__).read_text(encoding="utf-8")
        block = []
        for line in source.split("\n"):
            if line.startswith("ROOT_READING_VOCABULARY"):
                break
            if line.startswith("#: "):
                block.append(line[3:])
            elif not line.startswith("#:"):
                block = []
        self.assertEqual(" ".join(" ".join(block).split()),
                         " ".join(standard.VOCABULARY_NOTE.split()))

    def test_item41_the_two_owners_of_schema_repair_budget_are_literally_equal(self):
        self.assertEqual(standard._INT_PARAMS["schema_repair_budget"], (0, 0))
        low, high = standard._INT_PARAMS["schema_repair_budget"]
        self.assertEqual(GUARD_PARAMETERS["schema_repair_budget"], low)
        self.assertEqual(low, high)

    def test_item41_a_token_scan_reads_what_a_reader_reads(self):
        """NFKC and format characters: a zero-width joiner is not a new word."""

        with self.assertRaises(StandardInvalid):
            standard.assert_no_scoring_headers(
                "| cell | sc​ore |\n|---|---|\n| a | b |\n")
        with self.assertRaises(StandardInvalid):
            standard.assert_no_scoring_headers(
                "| cell | ｓcore |\n|---|---|\n| a | b |\n")
        with self.assertRaises(StandardInvalid):
            standard.assert_no_exhaustion_claim("the inquiry was exhaus​ted")


class EveryCalibrationAnchorAdmitsAUniquelyResolvingQuote(unittest.TestCase):
    """REVIEW-WAVE1 B3 / REVIEW-PREREG PR-06, fixed and pinned.

    The calibration set is, by design 9.1, "the only lever whose ground truth is
    true by construction". ``self-juxtaposition`` was built from two copies of
    one record, so ``M.count(q) == 2`` for **every** substring: no
    ``passage_quote`` could satisfy G2(a), the anchor blocked
    ``blocked:referential-integrity`` on every window for both seats for ever,
    and an anchor declared ``must_sustain: true`` consumed the panel's headroom
    to ``judge_err_max`` for a reason that had nothing to do with either seat.
    Worse, ``cal-07`` of the pre-registration bundle is the *same* construction
    with the opposite declared ground truth.

    The repair is W1-SURFACE's own rule: "a region the row does not carry is
    absent, not empty". Built with the referring region alone, the record's
    bytes appear once and every span of it resolves.

    These tests use a published row, so what they demonstrate is a fact about
    the shipped resolver and not about a fixture.
    """

    TABLE = (REPO / "experiments" / "analyses"
             / "F001-fork5-multifamily-2026-09-14" / "occurrence-01"
             / "use-table" / "use_table.json")

    @classmethod
    def setUpClass(cls) -> None:
        cls.row = json.loads(cls.TABLE.read_text(encoding="utf-8"))["rows"][0]
        cls.record = cls.row["referring_record_verbatim"]

    def two_copies(self) -> dict:
        """The construction the anchor USED to name: the same bytes twice."""

        row = dict(self.row)
        row["target_record_verbatim"] = self.record
        row["target_record_source_span"] = self.row["referring_record_source_span"]
        return row

    def referring_only(self) -> dict:
        """The construction it names now: the referring region alone."""

        row = dict(self.row)
        row["target_record_verbatim"] = None
        row["target_record_source_span"] = None
        row["referring_body_passages"] = []
        return row

    def windows(self):
        return (self.record[:20], self.record[:40], self.record[:80], self.record)

    def test_the_anchor_no_longer_declares_the_two_copy_construction(self):
        anchor = {a.id: a for a in CALIBRATION_ANCHORS}["self-juxtaposition"]
        self.assertNotIn("are the same bytes", anchor.construction)
        self.assertIn("referring region alone", anchor.construction)
        self.assertIn("exactly once", " ".join(anchor.construction.split()))

    def test_the_old_construction_resolves_no_quote_at_all(self):
        from minireason.loop import surface

        built = surface.build_surface(self.two_copies())
        for quote in self.windows():
            with self.subTest(window=len(quote)):
                self.assertIsNone(surface.resolve_unique(built, quote))

    def test_the_declared_construction_resolves_every_window_inside_a_region(self):
        from minireason.loop import surface

        built = surface.build_surface(self.referring_only())
        for quote in self.windows():
            with self.subTest(window=len(quote)):
                offset = surface.resolve_unique(built, quote)
                self.assertIsNotNone(offset)
                self.assertEqual(offset.side, surface.SIDE_REFERRING_RECORD)
                self.assertTrue(surface.within_declared_span(built, offset))

    def test_every_anchor_names_its_construction_and_its_ground_truth(self):
        for anchor in CALIBRATION_ANCHORS:
            with self.subTest(anchor=anchor.id):
                self.assertTrue(anchor.construction.strip())
                self.assertTrue(anchor.ground_truth_reason.strip())
                self.assertIsInstance(anchor.must_sustain, bool)

    def test_a_sustaining_anchor_declares_a_construction_a_quote_can_reach(self):
        """The rule B3 asks for, stated over the shipped set.

        An anchor a seat is expected to SUSTAIN must be buildable so that some
        quote resolves; the clean controls are the ones that may be
        unresolvable, and two of them are unresolvable on purpose.
        """

        for anchor in CALIBRATION_ANCHORS:
            if not anchor.must_sustain:
                continue
            with self.subTest(anchor=anchor.id):
                self.assertNotIn("the same bytes", anchor.construction)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
