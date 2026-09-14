"""W1-OBLIGATIONS: the pre-registered O and P, their program checks, ProducedBy.

Every acceptance clause of the wave-plan entry has at least one test here:

* "An o satisfied by artifacts not registered this cycle does not count as
  discharged" - :class:`ProducedByIsNotTemporalSuccession`.
* "losses_outside_p returns a list that is present and empty rather than
  absent when there are none" - :class:`TheLossRegisters`.
* "evaluation is pure and reads only artifacts, never counts" -
  :class:`TheHardRuleAgainstScalarMeters` and
  :class:`EvaluationIsPureAndReadsTheGraph`.
* "the pin changes on any byte change" - :class:`TheDocumentIsLoadedAndPinned`.

The graph fixture is a real ``deepreason_core`` harness under a temporary
directory: artifacts are registered, adjudicated by the two-pass grounded
adjudication, and read back through :meth:`Situation.from_harness`. No
provider, no socket, no write outside the temporary directory.
"""

from __future__ import annotations

import ast
import hashlib
import inspect
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from deepreason_core.canonical import canonical_json, sha256_hex
from deepreason_core.harness import Harness
from deepreason_core.ontology import Provenance, Warrant, WarrantType

from minireason.loop import graph
from minireason.loop import obligations as mod
from minireason.loop.obligations import (
    CELL_STATES,
    FAILED_SET,
    OBLIGATIONS_SCHEMA,
    PREDICATES,
    PREDICATE_QUESTIONS,
    PREDICATE_READS,
    PROTECTED_SET,
    Check,
    Evaluation,
    Loss,
    Obligations,
    ObligationsError,
    Situation,
    Verdict,
    evaluate,
    load_obligations,
    canonical_pin,
    losses_outside_p,
    pin,
    predicate,
    produced_by,
    protected_losses,
)

SOURCE = Path(mod.__file__)

#: id -> (membership, predicate name), in the pre-registration's own order.
DECLARED: tuple[tuple[str, str, str], ...] = (
    ("o1", FAILED_SET, "row_disposition_complete"),
    ("o2", FAILED_SET, "mark_disposition_complete"),
    ("o3", FAILED_SET, "citations_reresolve"),
    ("o4", FAILED_SET, "blocks_named"),
    ("o5", FAILED_SET, "audit_in_force"),
    ("o6", FAILED_SET, "baseline_sealed_and_carried"),
    ("o7", FAILED_SET, "trichotomy_rendered"),
    ("p1", PROTECTED_SET, "original_bytes_unchanged"),
    ("p2", PROTECTED_SET, "recoding_table_complete"),
    ("p3", PROTECTED_SET, "shared_envelope_intact"),
    ("p4", PROTECTED_SET, "no_scoring_key"),
    ("p5", PROTECTED_SET, "write_once_no_replay"),
    ("p6", PROTECTED_SET, "no_aggregation"),
    ("p7", PROTECTED_SET, "no_edges_on_studied_nodes"),
    ("p8", PROTECTED_SET, "appellate_optional"),
    ("p9", PROTECTED_SET, "baseline_still_pinned"),
    ("p10", PROTECTED_SET, "published_unresolved_preserved"),
    ("p11", PROTECTED_SET, "published_tree_untouched"),
    ("p12", PROTECTED_SET, "ceiling_and_trichotomy_intact"),
)


def entry(identifier: str, membership: str, check: str) -> dict:
    return {
        "id": identifier,
        "set": membership,
        "statement": f"the pre-registered prose of {identifier}",
        "check": {
            "predicate": f"obligations.{check}",
            "artifact": [f"experiments/loops/T001/{identifier}.json"],
            "detail": f"how the program reads {identifier}",
        },
        "why_not_a_count": "a universal quantification over a fixed named key set",
    }


def document(entries: list[dict] | None = None, **overrides) -> dict:
    body = {
        "schema": OBLIGATIONS_SCHEMA,
        "run_id": "T001",
        "obligations": [entry(*row) for row in DECLARED] if entries is None else entries,
    }
    body.update(overrides)
    body["obligations_sha256"] = sha256_hex(canonical_json(body))
    return body


class DocumentTestCase(unittest.TestCase):
    """A temporary directory and one written obligations document."""

    def setUp(self) -> None:
        super().setUp()
        self.root = Path(tempfile.mkdtemp(prefix="loop-obligations-"))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def write(self, body: dict, name: str = "obligations.json") -> Path:
        path = self.root / name
        path.write_text(json.dumps(body, indent=2), encoding="utf-8")
        return path

    def load(self, body: dict | None = None) -> Obligations:
        return load_obligations(self.write(document() if body is None else body))

    def refusal(self, body: dict, token: str) -> ObligationsError:
        with self.assertRaises(ObligationsError) as caught:
            load_obligations(self.write(body))
        self.assertEqual(caught.exception.code, token)
        return caught.exception


# ---------------------------------------------------------------------------
# The fixture graph
# ---------------------------------------------------------------------------

MATERIAL_TEXT = "alpha beta gamma delta epsilon"
BASELINE_BODY = "T same; E same; D same; G same"
CEILING_SENTENCE = "What this run claims."
CEILING_BODY = f"{CEILING_SENTENCE} Under registered standard std:reading-rubric/v1."


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class GraphFixture:
    """A small in-memory harness carrying one of every record kind."""

    def __init__(self, root: Path) -> None:
        self.harness = Harness(root)
        self.ids: dict[str, str] = {}

    def add(self, name: str, record: dict, *, role: str = "import") -> str:
        artifact = self.harness.create_artifact(
            json.dumps(record, sort_keys=True).encode("utf-8"),
            codec="json",
            provenance=Provenance(role=role),
        )
        self.ids[name] = artifact.id
        return artifact.id

    def attack(self, target: str, note: str) -> str:
        nu = self.harness.create_artifact(
            f"nu: the attack {note} is sound and relevant".encode("utf-8"),
            provenance=Provenance(role="critic"),
        )
        warrant = Warrant(
            id=f"w-{note}",
            target=target,
            type=WarrantType.ARGUMENTATIVE,
            validity_node=nu.id,
        )
        critic = self.harness.create_artifact(
            f"critic: {note}".encode("utf-8"),
            provenance=Provenance(role="critic"),
            warrants=[warrant],
        )
        self.ids[f"attack-{note}"] = critic.id
        return critic.id

    def build(self) -> "GraphFixture":
        material = self.add("material", {
            "record": "material",
            "occurrence_path": "occ/material.json",
            "text": MATERIAL_TEXT,
            "sha256": _digest(MATERIAL_TEXT),
        })
        self.add("reading_set", {
            "record": "reading_set",
            "rows": ["h005-row/r1", "h005-row/r2"],
            "marks": ["c001-mark/m1"],
            "registers": ["T", "E", "D", "G"],
        })
        self.add("reading_row", {
            "record": "reading_row",
            "key": "h005-row/r1",
            "relation": "re-deploys",
            "citation": {"quote": "beta", "surface": material},
            "transcript": {
                "case": "the case names beta",
                "answer": "the answer stands",
                "decisive_point": "names beta",
            },
            "rulings": [{"seat": "s1", "sustained": "yes"},
                        {"seat": "s2", "sustained": "yes"}],
        }, role="critic")
        self.add("block", {
            "record": "disposition",
            "key": "h005-row/r2",
            "reason": "blocked:provider",
            "prompt_ref": "a" * 64,
            "raw_ref": "b" * 64,
        })
        self.add("cell_mark", {
            "record": "cell_mark",
            "key": "c001-mark/m1",
            "mark": "differs",
            "difference_kind": "target_set_membership",
            "left_citation": {"quote": "alpha", "surface": material},
            "right_citation": {"quote": "gamma", "surface": material},
            "baseline_sha256": _digest(BASELINE_BODY),
        }, role="critic")
        self.add("baseline", {
            "record": "baseline",
            "sha256": _digest(BASELINE_BODY),
            "body": BASELINE_BODY,
            "registers": ["T", "E", "D", "G"],
        })
        self.add("call_record", {
            "record": "call_record",
            "coordinate": "seat-a/c001-mark/m1",
            "digest": "c" * 64,
            "cross_case": True,
            "baseline_sha256": _digest(BASELINE_BODY),
        })
        self.add("audit_record", {
            "record": "audit_record",
            "covers": ["1", "2"],
            "seats": ["judge-a", "judge-b"],
            "calibration_sha256": "d" * 64,
        })
        self.add("rendered_states", {
            "record": "rendered_states",
            "states": {
                "h005-row/r1": "read",
                "h005-row/r2": "machine-unresolved",
                "c001-mark/m1": "read",
            },
        })
        self.add("recoding_table", {
            "record": "recoding_table",
            "covers": ["unit-1"],
            "entries": {"unit-1": "original-1"},
        })
        self.add("request_a", {
            "record": "case_request", "group": "g1",
            "frame": "FRAME", "objection": "the first objection",
        })
        self.add("request_b", {
            "record": "case_request", "group": "g1",
            "frame": "FRAME", "objection": "the second objection",
        })
        self.add("forbidden_keys", {
            "record": "forbidden_keys", "keys": ["rank", "tally", "grade"],
        })
        self.add("aggregate_keys", {
            "record": "aggregate_keys", "keys": ["mean", "majority", "weighted"],
        })
        studied = self.add("studied", {"record": "cell_open", "key": "c001-cell/x"})
        self.add("study_set", {"record": "study_set", "keys": [studied]})
        self.add("published_unresolved", {
            "record": "published_unresolved", "keys": ["c001-cell/x"],
        })
        digests = {"occ/material.json": _digest(MATERIAL_TEXT), "docs/PLAN.md": "e" * 64}
        self.add("pinned_digests", {"record": "pinned_digests", "digests": digests})
        self.add("observed_digests", {"record": "observed_digests", "digests": digests})
        self.add("ceiling", {
            "record": "ceiling",
            "body": CEILING_BODY,
            "sha256": _digest(CEILING_BODY),
            "sentences": [CEILING_SENTENCE],
        })
        self.add("rendered_files", {
            "record": "rendered_files",
            "files": {"READING_TABLE.md": f"# table\n\n{CEILING_BODY}\n"},
        })
        return self


class HarnessTestCase(DocumentTestCase):
    """A document plus a fixture graph built on a real harness."""

    def setUp(self) -> None:
        super().setUp()
        self.obligations = self.load()
        self.graph = GraphFixture(self.root / "graph").build()

    def situation(self, *, cycle: int = 1, registered=(), obligations=None) -> Situation:
        return Situation.from_harness(
            self.graph.harness,
            cycle=cycle,
            obligations=self.obligations if obligations is None else obligations,
            registered=registered,
        )


# ---------------------------------------------------------------------------


class TheDocumentIsLoadedAndPinned(DocumentTestCase):

    def test_a_well_formed_document_separates_the_failed_set_from_the_protected_set(self):
        loaded = self.load()
        self.assertEqual([o.id for o in loaded.failed], ["o1", "o2", "o3", "o4", "o5", "o6", "o7"])
        self.assertEqual([o.id for o in loaded.protected], [f"p{n}" for n in range(1, 13)])

    def test_every_entry_carries_an_id_a_statement_a_check_and_one_membership(self):
        for obligation in self.load().entries:
            with self.subTest(obligation=obligation.id):
                self.assertTrue(obligation.statement)
                self.assertIn(obligation.check, PREDICATES)
                self.assertIn(obligation.membership, (FAILED_SET, PROTECTED_SET))
                self.assertEqual(obligation.is_protected, obligation.membership == PROTECTED_SET)

    def test_an_obligation_declared_in_both_sets_is_refused(self):
        entries = [entry(*row) for row in DECLARED]
        entries.append(entry("o1", PROTECTED_SET, "appellate_optional"))
        self.refusal(document(entries), "OBLIGATION_IN_BOTH_SETS")

    def test_a_duplicate_id_inside_one_set_is_refused(self):
        entries = [entry(*row) for row in DECLARED]
        entries.append(entry("o1", FAILED_SET, "audit_in_force"))
        self.refusal(document(entries), "OBLIGATION_ID_DUPLICATE")

    def test_a_membership_outside_o_and_p_is_refused(self):
        self.refusal(document([entry("o1", "Q", "audit_in_force")]),
                     "OBLIGATION_MEMBERSHIP_UNKNOWN")

    def test_a_check_naming_an_unregistered_program_is_refused(self):
        self.refusal(document([entry("o1", FAILED_SET, "count_the_readings")]),
                     "OBLIGATION_CHECK_UNKNOWN")

    def test_an_unknown_top_level_key_is_refused_rather_than_pinned_and_unread(self):
        self.refusal(document(budget="three cycles"), "OBLIGATIONS_UNKNOWN_KEY")

    def test_a_missing_required_key_is_refused(self):
        body = document()
        del body["obligations"]
        self.refusal(body, "OBLIGATIONS_MISSING_KEY")

    def test_an_unknown_schema_is_refused(self):
        self.refusal(document(schema="minireason.loop.obligations.v2"),
                     "OBLIGATIONS_SCHEMA_UNKNOWN")

    def test_a_document_that_is_not_json_is_refused(self):
        path = self.root / "obligations.json"
        path.write_text("{not json", encoding="utf-8")
        with self.assertRaises(ObligationsError) as caught:
            load_obligations(path)
        self.assertEqual(caught.exception.code, "OBLIGATIONS_MALFORMED")

    def test_a_missing_file_is_refused_by_name(self):
        with self.assertRaises(ObligationsError) as caught:
            load_obligations(self.root / "absent.json")
        self.assertEqual(caught.exception.code, "OBLIGATIONS_FILE_MISSING")

    def test_an_empty_statement_is_refused(self):
        entries = [entry("o1", FAILED_SET, "audit_in_force")]
        entries[0]["statement"] = "   "
        self.refusal(document(entries), "OBLIGATION_FIELD_INVALID")

    def test_an_entry_missing_a_required_field_is_refused(self):
        entries = [entry("o1", FAILED_SET, "audit_in_force")]
        del entries[0]["check"]
        self.refusal(document(entries), "OBLIGATION_FIELD_MISSING")

    def test_a_self_declared_digest_that_does_not_reproduce_is_refused(self):
        body = document()
        body["obligations_sha256"] = "0" * 64
        self.refusal(body, "OBLIGATIONS_DIGEST_MISMATCH")

    def test_the_declared_structure_digest_reproduces_from_the_content(self):
        loaded = self.load()
        self.assertEqual(loaded.structure_digest, loaded.preamble["obligations_sha256"])

    def test_the_pin_is_the_file_sha256_and_two_loads_agree(self):
        path = self.write(document())
        first, second = load_obligations(path), load_obligations(path)
        self.assertEqual(pin(first), pin(second))
        self.assertEqual(pin(first), hashlib.sha256(path.read_bytes()).hexdigest())

    def test_the_pin_changes_on_any_byte_change_including_whitespace(self):
        path = self.write(document())
        before = pin(load_obligations(path))
        path.write_bytes(path.read_bytes().replace(b"\n", b"\n ", 1))
        after = pin(load_obligations(path))
        self.assertNotEqual(before, after)

    def test_the_structure_digest_is_not_the_pin_and_survives_whitespace(self):
        path = self.write(document())
        before = load_obligations(path).structure_digest
        path.write_bytes(path.read_bytes().replace(b"\n", b"\n ", 1))
        after = load_obligations(path)
        self.assertEqual(before, after.structure_digest)
        self.assertNotEqual(after.structure_digest, pin(after))

    def test_a_bare_string_check_is_accepted_and_the_module_prefix_is_stripped(self):
        entries = [entry("o1", FAILED_SET, "audit_in_force")]
        entries[0]["check"] = "audit_in_force"
        self.assertEqual(load_obligations(self.write(document(entries))).entries[0].check,
                         "audit_in_force")

    def test_the_declared_material_paths_ride_on_the_obligation(self):
        self.assertEqual(self.load().by_id("o3").reads, ("experiments/loops/T001/o3.json",))

    def test_an_unknown_obligation_id_is_refused_by_name(self):
        with self.assertRaises(ObligationsError) as caught:
            self.load().by_id("o99")
        self.assertEqual(caught.exception.code, "OBLIGATION_UNKNOWN")


class ThePredicateRegistry(unittest.TestCase):

    def test_every_registered_predicate_takes_one_situation_and_returns_a_check(self):
        for name, program in sorted(PREDICATES.items()):
            with self.subTest(predicate=name):
                signature = inspect.signature(program)
                self.assertEqual(tuple(signature.parameters), ("situation",))
                annotation = signature.parameters["situation"].annotation
                self.assertIn("Situation", str(annotation))
                self.assertIn("Check", str(signature.return_annotation))

    def test_the_registry_its_questions_and_its_declared_reads_carry_one_name_set(self):
        self.assertEqual(set(PREDICATES), set(PREDICATE_QUESTIONS))
        self.assertEqual(set(PREDICATES), set(PREDICATE_READS))

    def test_every_declared_check_of_the_pre_registration_resolves(self):
        for _, _, name in DECLARED:
            with self.subTest(check=name):
                self.assertIs(predicate(name), PREDICATES[name])

    def test_an_unregistered_program_name_is_refused(self):
        with self.assertRaises(ObligationsError) as caught:
            predicate("mean_reading_quality")
        self.assertEqual(caught.exception.code, "OBLIGATION_CHECK_UNKNOWN")

    def test_every_predicate_question_is_a_question_and_names_no_quantity(self):
        for name, question in sorted(PREDICATE_QUESTIONS.items()):
            with self.subTest(predicate=name):
                self.assertTrue(question.endswith("?"))


class EmptyGraphReadsNotEvaluableAndNeverFailure(DocumentTestCase):
    """FW5 R5: non-evaluability is not refutation, and never a failure."""

    def setUp(self) -> None:
        super().setUp()
        self.obligations = self.load()
        self.empty = Situation(cycle=1, obligations=self.obligations)

    def test_no_predicate_raises_on_a_graph_that_carries_nothing(self):
        for name, program in sorted(PREDICATES.items()):
            with self.subTest(predicate=name):
                self.assertIsInstance(program(self.empty), Check)

    def test_the_only_answers_on_an_empty_graph_are_not_evaluable_and_two_declared_exceptions(self):
        answers = {name: program(self.empty).verdict for name, program in PREDICATES.items()}
        self.assertIs(answers["appellate_optional"], Verdict.SATISFIED)
        self.assertIs(answers["audit_in_force"], Verdict.NOT_SATISFIED)
        rest = {
            name: verdict for name, verdict in answers.items()
            if name not in ("appellate_optional", "audit_in_force")
        }
        self.assertEqual(set(rest.values()), {Verdict.NOT_EVALUABLE})

    def test_not_evaluable_is_listed_apart_from_not_satisfied_in_the_record(self):
        record = evaluate(self.obligations, self.empty).as_dict()
        self.assertIn("o1", record["not_evaluable"])
        self.assertNotIn("o1", record["not_satisfied"])
        self.assertNotIn("o1", record["satisfied"])

    def test_not_evaluable_never_makes_every_o_satisfied_true(self):
        self.assertFalse(evaluate(self.obligations, self.empty).every_o_satisfied)

    def test_a_not_evaluable_obligation_is_still_failed_and_so_still_dischargeable(self):
        found = evaluate(self.obligations, self.empty)
        self.assertIn("o1", found.failed)
        self.assertIn("o5", found.failed)


class EvaluationIsPureAndReadsTheGraph(HarnessTestCase):

    def test_the_fixture_graph_satisfies_every_pre_registered_obligation(self):
        found = evaluate(self.obligations, self.situation())
        for obligation in self.obligations.entries:
            with self.subTest(obligation=obligation.id):
                self.assertIs(found.verdict(obligation.id), Verdict.SATISFIED,
                              found.checks[obligation.id].detail)
        self.assertTrue(found.every_o_satisfied)

    def test_every_check_cites_artifact_ids_that_are_registered(self):
        situation = self.situation()
        for obligation in self.obligations.entries:
            with self.subTest(obligation=obligation.id):
                for artifact_id in evaluate(self.obligations, situation).checks[obligation.id].evidence:
                    self.assertIn(artifact_id, situation.nodes)

    def test_a_citation_that_does_not_resolve_uniquely_is_named_by_o3(self):
        offender = self.graph.add("bad_reading", {
            "record": "reading_row",
            "key": "h005-row/r9",
            "relation": "re-deploys",
            "citation": {"quote": "not in the material",
                         "surface": self.graph.ids["material"]},
        }, role="critic")
        found = evaluate(self.obligations, self.situation())
        self.assertIs(found.verdict("o3"), Verdict.NOT_SATISFIED)
        self.assertIn(offender, found.checks["o3"].evidence)

    def test_a_quote_occurring_twice_does_not_resolve(self):
        material = self.graph.add("twice", {
            "record": "material", "occurrence_path": "occ/twice.json",
            "text": "beta and beta", "sha256": _digest("beta and beta"),
        })
        self.graph.add("bad_reading", {
            "record": "reading_row", "key": "h005-row/r9", "relation": "re-deploys",
            "citation": {"quote": "beta", "surface": material},
        }, role="critic")
        self.assertIs(evaluate(self.obligations, self.situation()).verdict("o3"),
                      Verdict.NOT_SATISFIED)

    def test_a_row_carrying_neither_a_relation_nor_a_reason_is_named_by_o1(self):
        self.graph.add("wider_set", {
            "record": "reading_set",
            "rows": ["h005-row/r1", "h005-row/r2", "h005-row/r3"],
            "marks": ["c001-mark/m1"],
            "registers": ["T", "E", "D", "G"],
        })
        self.graph.attack(self.graph.ids["reading_set"], "narrow")
        found = evaluate(self.obligations, self.situation())
        self.assertIs(found.verdict("o1"), Verdict.NOT_SATISFIED)
        self.assertIn("h005-row/r3", found.checks["o1"].detail)

    def test_a_block_without_a_closed_reason_code_is_named_by_o4(self):
        offender = self.graph.add("open_block", {
            "record": "disposition", "key": "h005-row/r4",
            "reason": "blocked:because-i-said-so",
            "prompt_ref": "f" * 64, "raw_ref": "0" * 64,
        })
        found = evaluate(self.obligations, self.situation())
        self.assertIs(found.verdict("o4"), Verdict.NOT_SATISFIED)
        self.assertIn(offender, found.checks["o4"].evidence)

    def test_a_split_ruling_that_did_not_stay_unresolved_is_a_protected_failure(self):
        offender = self.graph.add("split", {
            "record": "reading_row", "key": "h005-row/r5", "relation": "repairs",
            "citation": {"quote": "delta", "surface": self.graph.ids["material"]},
            "rulings": [{"seat": "s1", "sustained": "yes"},
                        {"seat": "s2", "sustained": "no"}],
        }, role="critic")
        found = evaluate(self.obligations, self.situation())
        self.assertIs(found.verdict("p6"), Verdict.NOT_SATISFIED)
        self.assertIn(offender, found.checks["p6"].evidence)

    def test_an_edge_landing_on_a_node_under_study_is_a_protected_failure(self):
        attacker = self.graph.attack(self.graph.ids["studied"], "reading-as-attack")
        found = evaluate(self.obligations, self.situation())
        self.assertIs(found.verdict("p7"), Verdict.NOT_SATISFIED)
        self.assertIn(attacker, found.checks["p7"].evidence)

    def test_material_whose_bytes_no_longer_hash_to_their_pin_is_a_protected_failure(self):
        offender = self.graph.add("moved", {
            "record": "material", "occurrence_path": "occ/moved.json",
            "text": "edited bytes", "sha256": _digest("the original bytes"),
        })
        found = evaluate(self.obligations, self.situation())
        self.assertIs(found.verdict("p1"), Verdict.NOT_SATISFIED)
        self.assertIn(offender, found.checks["p1"].evidence)

    def test_a_rewritten_coordinate_is_a_protected_failure(self):
        self.graph.add("replayed", {
            "record": "call_record", "coordinate": "seat-a/c001-mark/m1",
            "digest": "9" * 64,
        })
        self.assertIs(evaluate(self.obligations, self.situation()).verdict("p5"),
                      Verdict.NOT_SATISFIED)

    def test_a_record_blocked_on_the_appellate_is_a_protected_failure(self):
        offender = self.graph.add("waiting", {
            "record": "disposition", "key": "h005-row/r6", "blocked_on": "appellate",
        })
        found = evaluate(self.obligations, self.situation())
        self.assertIs(found.verdict("p8"), Verdict.NOT_SATISFIED)
        self.assertIn(offender, found.checks["p8"].evidence)

    def test_a_refuted_record_no_longer_bears_evidence(self):
        self.graph.attack(self.graph.ids["recoding_table"], "recoding-unsound")
        self.assertIs(evaluate(self.obligations, self.situation()).verdict("p2"),
                      Verdict.NOT_EVALUABLE)

    def test_evaluate_refuses_a_situation_pinned_to_another_document(self):
        other = load_obligations(self.write(document(run_id="T002"), name="other.json"))
        with self.assertRaises(ObligationsError) as caught:
            evaluate(other, self.situation())
        self.assertEqual(caught.exception.code, "OBLIGATIONS_PIN_SHIFTED")

    def test_evaluation_is_pure_over_the_graph_and_over_itself(self):
        before = tuple(event.seq for event in self.graph.harness.log.read())
        first = evaluate(self.obligations, self.situation()).as_dict()
        second = evaluate(self.obligations, self.situation()).as_dict()
        self.assertEqual(first, second)
        self.assertEqual(before, tuple(event.seq for event in self.graph.harness.log.read()))


class ProducedByIsNotTemporalSuccession(HarnessTestCase):
    """Clause 2: discharged means produced by this cycle, not merely followed by it."""

    def setUp(self) -> None:
        super().setUp()
        self.audit = self.graph.ids["audit_record"]

    def test_an_obligation_satisfied_by_this_cycle_s_artifacts_is_discharged(self):
        situation = self.situation(registered=[self.audit])
        self.assertEqual(produced_by(situation, "o5"), frozenset({self.audit}))
        self.assertIn("o5", evaluate(self.obligations, situation).discharged)

    def test_an_o_satisfied_by_artifacts_not_registered_this_cycle_is_not_discharged(self):
        situation = self.situation(registered=())
        self.assertEqual(produced_by(situation, "o5"), frozenset())
        self.assertEqual(evaluate(self.obligations, situation).discharged, ())

    def test_registering_something_else_this_cycle_discharges_nothing(self):
        situation = self.situation(registered=[self.graph.ids["request_a"]])
        self.assertEqual(produced_by(situation, "o5"), frozenset())
        self.assertNotIn("o5", evaluate(self.obligations, situation).discharged)

    def test_an_obligation_that_still_holds_with_this_cycle_withheld_is_not_discharged(self):
        later = self.graph.add("second_audit", {
            "record": "audit_record", "covers": ["1", "2"],
            "seats": ["judge-c", "judge-d"], "calibration_sha256": "e" * 64,
        })
        situation = self.situation(registered=[later])
        self.assertIn(later, evaluate(self.obligations, situation).checks["o5"].evidence)
        self.assertEqual(produced_by(situation, "o5"), frozenset())

    def test_an_unsatisfied_obligation_produces_nothing(self):
        situation = self.situation(cycle=9, registered=[self.audit])
        self.assertIs(evaluate(self.obligations, situation).verdict("o5"), Verdict.NOT_SATISFIED)
        self.assertEqual(produced_by(situation, "o5"), frozenset())

    def test_produced_by_refuses_an_obligation_the_document_does_not_declare(self):
        with self.assertRaises(ObligationsError) as caught:
            produced_by(self.situation(), "o99")
        self.assertEqual(caught.exception.code, "OBLIGATION_UNKNOWN")


class TheLossRegisters(HarnessTestCase):
    """FW5:802 - losses outside P are exposed, every cycle, even when empty."""

    def test_the_register_is_present_and_empty_before_the_first_cycle(self):
        found = losses_outside_p(None, self.situation())
        self.assertIsInstance(found, list)
        self.assertEqual(found, [])

    def test_the_register_is_present_and_empty_when_nothing_was_lost(self):
        prev = self.situation(cycle=1)
        curr = self.situation(cycle=2)
        self.assertEqual(losses_outside_p(prev, curr), [])
        self.assertEqual(protected_losses(prev, curr), [])

    def test_a_withdrawn_artifact_is_exposed_with_both_of_its_standings(self):
        prev = self.situation(cycle=1)
        target = self.graph.ids["recoding_table"]
        self.graph.attack(target, "recoding-unsound")
        found = losses_outside_p(prev, self.situation(cycle=2))
        withdrawn = [loss for loss in found if loss.subject == target]
        self.assertEqual([loss.kind for loss in withdrawn], ["standing_withdrawn"])
        self.assertEqual((withdrawn[0].was, withdrawn[0].now), ("accepted", "refuted"))

    def test_an_obligation_of_o_that_regressed_is_exposed_outside_p(self):
        prev = self.situation(cycle=1)
        found = losses_outside_p(prev, self.situation(cycle=9))
        self.assertIn("o5", [loss.subject for loss in found])
        regression = [loss for loss in found if loss.subject == "o5"][0]
        self.assertEqual(regression.kind, "obligation_regressed")
        self.assertEqual(regression.membership, FAILED_SET)

    def test_a_protected_regression_is_not_in_the_outside_register_but_in_its_own(self):
        prev = self.situation(cycle=1)
        self.graph.add("split", {
            "record": "reading_row", "key": "h005-row/r5", "relation": "repairs",
            "citation": {"quote": "delta", "surface": self.graph.ids["material"]},
            "rulings": [{"seat": "s1", "sustained": "yes"},
                        {"seat": "s2", "sustained": "no"}],
        }, role="critic")
        curr = self.situation(cycle=2)
        self.assertNotIn("p6", [loss.subject for loss in losses_outside_p(prev, curr)])
        protected = protected_losses(prev, curr)
        self.assertEqual([loss.subject for loss in protected], ["p6"])
        self.assertEqual(protected[0].kind, "protected_loss")
        self.assertIn("p6", protected[0].detail)

    def test_a_protected_obligation_that_became_unreadable_is_exposed_and_is_not_a_loss(self):
        prev = self.situation(cycle=1)
        self.graph.attack(self.graph.ids["recoding_table"], "recoding-unsound")
        curr = self.situation(cycle=2)
        self.assertEqual([loss.subject for loss in protected_losses(prev, curr)], [])
        self.assertIn("p2", evaluate(self.obligations, curr).protected_not_evaluable)

    def test_an_obligation_that_became_unreadable_is_exposed_under_its_own_kind(self):
        prev = self.situation(cycle=1)
        self.graph.attack(self.graph.ids["reading_set"], "reading-set-unsound")
        found = losses_outside_p(prev, self.situation(cycle=2))
        unreadable = [loss for loss in found if loss.subject == "o1"]
        self.assertEqual([loss.kind for loss in unreadable], ["obligation_unevaluable"])

    def test_a_cycle_may_be_net_withdrawal_and_still_carry_a_discharge(self):
        bare = GraphFixture(self.root / "bare")
        bare.add("keeper", {"record": "material", "occurrence_path": "occ/k.json",
                            "text": "kept", "sha256": _digest("kept")})
        prev = Situation.from_harness(bare.harness, cycle=1, obligations=self.obligations)
        bare.attack(bare.ids["keeper"], "withdrawn")
        audit = bare.add("audit_record", {
            "record": "audit_record", "covers": ["2"], "seats": ["judge-a"],
            "calibration_sha256": "d" * 64,
        })
        curr = Situation.from_harness(bare.harness, cycle=2,
                                      obligations=self.obligations, registered=[audit])
        self.assertIn("o5", evaluate(self.obligations, curr).discharged)
        self.assertTrue(losses_outside_p(prev, curr))

    def test_both_registers_refuse_two_situations_under_different_documents(self):
        other = load_obligations(self.write(document(run_id="T002"), name="other.json"))
        prev = self.situation(cycle=1)
        curr = self.situation(cycle=2, obligations=other)
        for register in (losses_outside_p, protected_losses):
            with self.subTest(register=register.__name__):
                with self.assertRaises(ObligationsError) as caught:
                    register(prev, curr)
                self.assertEqual(caught.exception.code, "OBLIGATIONS_PIN_SHIFTED")

    def test_every_loss_renders_as_strings_the_operator_can_read(self):
        prev = self.situation(cycle=1)
        self.graph.attack(self.graph.ids["recoding_table"], "recoding-unsound")
        for loss in losses_outside_p(prev, self.situation(cycle=2)):
            with self.subTest(subject=loss.subject):
                self.assertIsInstance(loss, Loss)
                self.assertIn(loss.kind, mod.LOSS_KINDS)
                for value in loss.as_dict().values():
                    self.assertIsInstance(value, str)


class TheHardRuleAgainstScalarMeters(HarnessTestCase):
    """No count, rate, threshold or score is an input or a verdict anywhere here."""

    FORBIDDEN = frozenset({
        "count", "counts", "rate", "rates", "threshold", "thresholds", "score",
        "scores", "scoring", "ratio", "percent", "percentage", "mean", "median",
        "average", "avg", "total", "sum", "tally", "majority", "weighted", "num",
        "n", "quantity", "amount", "many", "size", "length", "len", "rank",
    })
    #: The only string literals outside a docstring that may carry one of the
    #: tokens: the pre-registered document's own field names, and the name of
    #: the prohibition p4 states.
    ALLOWED_STRINGS = frozenset({
        "no_clause_is_a_count",
        "why_not_a_count",
        "no_scoring_key",
        "no registered record carries a forbidden scoring key",
        "records carrying a forbidden scoring key",
    })
    ARITHMETIC = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod,
                  ast.Pow, ast.MatMult, ast.LShift, ast.RShift)
    BANNED_CALLS = frozenset({"len", "sum", "min", "max", "abs", "round"})

    #: The only functions an ordering comparison may appear in: the two
    #: the pre-registration names as instrument bounds, and nothing else.
    ORDERING_ALLOWED = ()

    @staticmethod
    def exempt_constants(tree) -> set:
        """Numeric literals an index may legitimately carry.

        The slice ITSELF (``row[1]``), or a bound of a ``Slice`` (``span[2:3]``)
        - not every constant anywhere inside a subscript's subtree, which is
        what the exemption used to be (REVIEW-WAVE1 S5).
        """

        exempt = set()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Subscript):
                continue
            inner = node.slice
            if isinstance(inner, ast.Constant):
                exempt.add(inner.value)
            elif isinstance(inner, ast.Slice):
                for bound in (inner.lower, inner.upper, inner.step):
                    if isinstance(bound, ast.Constant):
                        exempt.add(bound.value)
            elif isinstance(inner, ast.UnaryOp) and isinstance(inner.operand,
                                                               ast.Constant):
                exempt.add(inner.operand.value)
        return exempt

    def enclosing_function(self, target) -> str:
        """The name of the function a node sits in, or "" at module level."""

        for node in ast.walk(self.tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for inner in ast.walk(node):
                if inner is target:
                    return node.name
        return ""

    # -- REVIEW-WAVE1 S5: the guard's own holes, each closed and probed ------ #

    #: Comparison operators that read a MAGNITUDE. ``==`` and ``!=`` are not
    #: here: set identity and token equality are the two things this program is
    #: allowed to do, and clause four is exactly a set-identity test.
    ORDERING = (ast.Lt, ast.LtE, ast.Gt, ast.GtE)

    #: Callables that produce, order or tally a quantity. ``sorted`` is banned
    #: for a different reason from ``len``: an ORDER over readings is the rank
    #: the vocabulary has no room for. A sort of record IDS or of a rendered
    #: block, which is what this module actually does, goes through
    #: ``_ordered``/``sorted`` at a call site the exemption below names.
    BANNED_ORDERING_CALLS = frozenset({"statistics", "Counter", "mean", "median"})

    def test_the_module_compares_no_magnitudes(self):
        """S5: ``>`` and ``<`` were not in the arithmetic assertion at all.

        A module that computes no arithmetic can still read a threshold, and a
        ``>`` is how it would. Every ordering comparison in these two modules
        is either absent or, where one is the pre-registered instrument bound,
        confined to the function the decision names.
        """

        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Compare):
                continue
            for operator in node.ops:
                if not isinstance(operator, self.ORDERING):
                    continue
                where = self.enclosing_function(node)
                with self.subTest(line=node.lineno, function=where):
                    self.assertIn(where, self.ORDERING_ALLOWED,
                                  "an ordering comparison outside the functions "
                                  "the pre-registration names")

    def test_the_module_imports_no_statistics_and_counts_nothing(self):
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = ([alias.name for alias in node.names]
                         + [getattr(node, "module", "") or ""])
                for name in names:
                    with self.subTest(imported=name):
                        self.assertNotIn(name.split(".")[0].casefold(),
                                         {"statistics", "collections", "numpy"})
            if isinstance(node, ast.Call):
                name = getattr(node.func, "id", getattr(node.func, "attr", ""))
                with self.subTest(call=name):
                    self.assertNotIn(name, self.BANNED_ORDERING_CALLS)

    def test_the_token_scan_is_case_folded(self):
        """S5: ``Count`` and ``COUNT`` walked past a case-sensitive membership."""

        for spelling in ("Count", "COUNT", "Rank", "TALLY", "Score"):
            with self.subTest(spelling=spelling):
                self.assertEqual(self.tokens(spelling.casefold()) & self.FORBIDDEN,
                                 {spelling.casefold()})

    def test_the_numeric_exemption_covers_only_a_constant_that_is_the_slice(self):
        """S5: the exemption used to cover every Constant ANYWHERE in a slice.

        ``table[compute(2 * 3)]`` was exempt because both literals were inside
        a ``Subscript.slice`` subtree. The exemption is now the slice itself,
        or a literal directly inside a slice's ``Slice`` bounds.
        """

        tree = ast.parse("table[compute(7)]\nrow[1]\nspan[2:3]\n")
        exempt = self.exempt_constants(tree)
        found = {node.value for node in ast.walk(tree)
                 if isinstance(node, ast.Constant)}
        self.assertEqual(found - exempt, {7},
                         "a literal buried in a call inside a slice is not an index")
        self.assertEqual({1, 2, 3} - exempt, set())

    @classmethod
    def setUpClass(cls) -> None:
        cls.tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        cls.docstrings = set()
        for node in ast.walk(cls.tree):
            body = getattr(node, "body", None)
            if not isinstance(body, list) or not body:
                continue
            head = body[0]
            if isinstance(head, ast.Expr) and isinstance(head.value, ast.Constant):
                if isinstance(head.value.value, str):
                    cls.docstrings.add(id(head.value))

    def tokens(self, identifier: str) -> set[str]:
        return {part for part in str(identifier).split("_") if part}

    def test_no_identifier_in_the_module_names_a_count_a_rate_a_threshold_or_a_score(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Name):
                found = node.id
            elif isinstance(node, ast.arg):
                found = node.arg
            elif isinstance(node, ast.Attribute):
                found = node.attr
            elif isinstance(node, ast.keyword):
                found = node.arg or ""
            elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                found = node.name
            else:
                continue
            if found.startswith("no_"):
                continue  # a prohibition may name what must not appear
            with self.subTest(identifier=found):
                self.assertEqual(self.tokens(found) & self.FORBIDDEN, set())

    def test_no_string_outside_a_docstring_names_one_save_the_pre_registered_fields(self):
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Constant) or id(node) in self.docstrings:
                continue
            if not isinstance(node.value, str) or node.value in self.ALLOWED_STRINGS:
                continue
            words = node.value.replace(".", " ").replace("_", " ").replace("-", " ").split()
            with self.subTest(text=node.value[:60]):
                self.assertEqual({word.lower() for word in words} & self.FORBIDDEN, set())

    def test_the_module_computes_no_arithmetic(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.BinOp):
                self.assertNotIsInstance(node.op, self.ARITHMETIC)
            if isinstance(node, ast.AugAssign):
                self.assertNotIsInstance(node.op, self.ARITHMETIC)

    def test_the_module_carries_no_numeric_literal_outside_a_subscript(self):
        indexed = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Subscript):
                for inner in ast.walk(node.slice):
                    if isinstance(inner, ast.Constant):
                        indexed.add(id(inner))
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Constant) and id(node) not in indexed:
                with self.subTest(line=node.lineno):
                    self.assertNotIn(type(node.value), (int, float))

    def test_the_module_calls_no_counting_builtin(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertNotIn(node.func.id, self.BANNED_CALLS)

    def test_every_public_entry_point_takes_named_arguments_that_are_not_quantities(self):
        for name in ("evaluate", "produced_by", "losses_outside_p", "protected_losses",
                     "pin", "load_obligations", "predicate"):
            signature = inspect.signature(getattr(mod, name))
            for argument in signature.parameters:
                with self.subTest(function=name, argument=argument):
                    self.assertEqual(self.tokens(argument) & self.FORBIDDEN, set())

    def test_a_verdict_is_one_of_three_tokens_and_never_a_number(self):
        situation = self.situation()
        for obligation in self.obligations.entries:
            answer = evaluate(self.obligations, situation).verdict(obligation.id)
            with self.subTest(obligation=obligation.id):
                self.assertIsInstance(answer, Verdict)
                self.assertNotIsInstance(answer.value, (int, float))

    def test_the_evaluation_record_carries_no_number_but_the_cycle_index(self):
        record = evaluate(self.obligations, self.situation(cycle=2)).as_dict()
        self.assertEqual(record["cycle"], 2)

        def walk(value, where):
            if isinstance(value, dict):
                for key, nested in value.items():
                    walk(nested, f"{where}.{key}")
            elif isinstance(value, list):
                for item in value:
                    walk(item, where)
            else:
                with self.subTest(where=where):
                    self.assertNotIsInstance(value, (int, float), where)

        for key, value in record.items():
            if key != "cycle":
                walk(value, key)


# ---------------------------------------------------------------------------
# Wave-1 integration decisions 1 and 2: W1-GRAPH is the writer of ``record``
# ---------------------------------------------------------------------------


class AGraphW1GraphPopulatedIsReadByThesePredicates(DocumentTestCase):
    """Decision 2: reconcile :data:`RECORD_KINDS` with the shapes W1-GRAPH writes
    by making W1-GRAPH the writer of ``record`` and reading exactly those tokens.

    The fixture graph elsewhere in this file is hand-built, which proves the
    predicates read *a* shape. This one is populated **only** through
    ``minireason.loop.graph``: the standard, the material bytes, the two
    unresolved defaults, one guarded reading, one mark and one audit finding,
    every one of them registered by the module W5-DRIVER will call. What the
    predicates then read is what the loop will actually produce.

    Fifteen predicates still answer ``not_evaluable`` here, and that is the
    honest answer rather than a gap: their records are written by W4-READER and
    W5-DRIVER, which do not exist yet. :data:`NOT_EVALUABLE_UNTIL_W4_W5` is the
    allow-list, and it names the record kind each is waiting for, so a predicate
    that silently stops reading a record W1-GRAPH *does* write fails here.
    """

    #: obligation id -> (predicate, the record kind whose writer is W4/W5).
    NOT_EVALUABLE_UNTIL_W4_W5 = {
        "o1": ("row_disposition_complete", "reading_set"),
        "o2": ("mark_disposition_complete", "reading_set"),
        "o4": ("blocks_named", "disposition"),
        "o6": ("baseline_sealed_and_carried", "baseline + reading_set"),
        "o7": ("trichotomy_rendered", "rendered_states + reading_set"),
        "p1": ("original_bytes_unchanged", "material"),
        "p2": ("recoding_table_complete", "recoding_table"),
        "p3": ("shared_envelope_intact", "case_request"),
        "p4": ("no_scoring_key", "forbidden_keys"),
        "p5": ("write_once_no_replay", "call_record"),
        "p7": ("no_edges_on_studied_nodes", "study_set"),
        "p9": ("baseline_still_pinned", "baseline"),
        "p10": ("published_unresolved_preserved", "published_unresolved"),
        "p11": ("published_tree_untouched", "pinned_digests + observed_digests"),
        "p12": ("ceiling_and_trichotomy_intact", "ceiling + rendered_files"),
    }

    RELATION_CELL = "r1/c1"
    QUOTE = "re-deploys the earlier term"

    def setUp(self) -> None:
        super().setUp()
        self.obligations = self.load()
        self.harness = graph.open_graph(self.root / "graph", clock=graph.fixed_clock())
        self.standard = graph.register_standard(self.harness)
        self.material_bytes = b'{"row_key": "r1", "cells": {}}'
        self.material = graph.register_material(self.harness, self.material_bytes)
        self.mark_cell = graph.CellKey(self.RELATION_CELL, "T", "original-vs-control")
        self.opened = graph.open_cells(
            self.harness, [graph.CellKey(self.RELATION_CELL), self.mark_cell],
            material_id=self.material)

    # -- builders, every one of them a call W5-DRIVER will make -------------- #

    def reading(self, **body) -> graph.ReadingIds:
        transcript = graph.Transcript(
            case="the later record re-deploys the earlier term without qualification",
            answer="the defence disputes that the two terms are the same term at all",
            decisive_point="without qualification",
            checks={"unique_offset": True}, meta={"pack_sha": "a" * 64})
        return graph.register_reading(self.harness, graph.ReadingResult(
            key=graph.CellKey(self.RELATION_CELL), relation="re-deploys",
            seat="judge-1", transcript=transcript, material_id=self.material,
            school="family-a+family-b",
            roles={"critic": "seat-c", "defender": "seat-d", "judge": "judge-1"},
            body=body), self.standard)

    def mark(self) -> graph.ReadingIds:
        transcript = graph.Transcript(
            case="ORIGINAL names o1 where CONTROL names o2, so the target set differs",
            answer="the defence concedes the two commitments do not name one target",
            decisive_point="the target set differs")
        return graph.register_mark(self.harness, graph.ReadingResult(
            key=self.mark_cell, relation="differs", seat="judge-1",
            transcript=transcript, difference_kind="target_set_membership",
            material_id=self.material), self.standard)

    def audit(self) -> str:
        return graph.register_audit_warrant(self.harness, graph.AuditFinding(
            seat="judge-2", kind="paraphrase-invariance", detail="no flip",
            body={"covers": ["1"], "seats": ["judge-1", "judge-2"],
                  "calibration_sha256": "d" * 64}))

    def driver_record(self, record: dict) -> str:
        """One record W5-DRIVER will register beside the graph, not a graph shape."""

        artifact = self.harness.create_artifact(
            json.dumps(record, sort_keys=True).encode("utf-8"), codec="json",
            provenance=Provenance(role="import"))
        return artifact.id

    def situation(self, *, cycle: int = 1, registered=()) -> Situation:
        return Situation.from_harness(self.harness, cycle=cycle,
                                      obligations=self.obligations,
                                      registered=registered)

    # -- the reconciliation ------------------------------------------------- #

    def test_the_two_modules_name_the_record_field_the_same_way(self):
        self.assertEqual(graph.RECORD_FIELD, mod.RECORD_FIELD)

    def test_the_mirrored_unresolved_token_is_the_standards_own_token(self):
        """Deviation 8 invited this assertion: ``obligations`` may not import
        ``standard`` (W0-STANDARD is not in its ``depends_on``), so the token is
        mirrored - and the integrator asserts the two spellings agree, here,
        where both modules are already imported."""

        from minireason.loop import standard

        self.assertEqual(mod.UNRESOLVED_RELATION, standard.UNRESOLVED_TOKEN)
        self.assertEqual(mod.UNRESOLVED_RELATION, graph.UNRESOLVED)
        self.assertIn(mod.UNRESOLVED_RELATION, standard.READING_VOCABULARY)
        self.assertIn(mod.UNRESOLVED_RELATION, standard.MARKS)

    def test_the_mirrored_declared_sides_are_the_surfaces_own_three(self):
        """REVIEW-WAVE1 S3: o3 must check G3's side, and cannot import surface.

        ``obligations`` imports no sibling but ``types``, so the three operative
        regions are mirrored here. The mirror is asserted where both modules are
        already imported, exactly as the unresolved token's is.
        """

        from minireason.loop import surface

        self.assertEqual(mod.DECLARED_SIDES, surface.DECLARED_SIDES)
        self.assertNotIn(surface.SIDE_FRAMING, mod.DECLARED_SIDES)
        self.assertEqual(set(surface.SIDES) - set(mod.DECLARED_SIDES),
                         {surface.SIDE_FRAMING})

    def test_o3_counts_an_overlapping_second_occurrence_as_not_unique(self):
        """REVIEW-WAVE1 S3: ``aa`` was read as unique in ``aaa``."""

        self.assertFalse(mod._resolves_uniquely("aaa", "aa"))
        self.assertFalse(mod._resolves_uniquely("xyx", "x"))
        self.assertTrue(mod._resolves_uniquely("aab", "aa"))
        self.assertTrue(mod._resolves_uniquely("abc", "abc"))
        self.assertFalse(mod._resolves_uniquely("abc", ""))
        self.assertFalse(mod._resolves_uniquely("", "abc"))

    def test_every_kind_w1_graph_writes_is_a_kind_this_module_reads_or_is_named(self):
        written, read = set(graph.RECORD_KINDS), set(mod.RECORD_KINDS)
        not_read = set(graph.RECORDS_NOT_READ)
        self.assertEqual(written - not_read - read, set(),
                         "W1-GRAPH writes a record kind no predicate here reads and "
                         "that RECORDS_NOT_READ does not name")
        self.assertEqual(not_read & read, set(),
                         "a kind declared unread is read by a predicate after all")
        for token, reason in graph.RECORDS_NOT_READ.items():
            with self.subTest(token=token):
                self.assertIn(token, written)
                self.assertTrue(reason.strip())

    def test_the_material_bytes_carry_no_record_field_and_are_unchanged(self):
        """§3(b): the instrument's bytes, exactly as emitted. W1-GRAPH may not add
        a key to them, so the ``material`` record p1 reads is a record *about* the
        material that W5-DRIVER registers beside it."""

        node = self.situation().nodes[self.material]
        self.assertEqual(node.text, self.material_bytes.decode("utf-8"))
        self.assertNotIn(mod.RECORD_FIELD, node.record)
        self.assertEqual(node.kind, "")
        self.assertEqual(self.situation().records(mod.MATERIAL), ())

    def test_each_shape_w1_graph_registers_is_found_under_its_own_kind(self):
        self.reading()
        self.mark()
        self.audit()
        situation = self.situation()
        for kind, count in ((mod.CELL_OPEN, 2), (mod.READING_ROW, 1),
                            (mod.CELL_MARK, 1), (mod.AUDIT_RECORD, 1)):
            with self.subTest(kind=kind):
                self.assertEqual(len(situation.records(kind)), count)
        # The reading and the mark are the same schema and two different kinds,
        # because a mark is never combined across registers.
        reading_row = situation.records(mod.READING_ROW)[0]
        cell_mark = situation.records(mod.CELL_MARK)[0]
        self.assertEqual(reading_row.record["schema"], graph.READING_SCHEMA)
        self.assertEqual(cell_mark.record["schema"], graph.READING_SCHEMA)
        self.assertEqual(cell_mark.record["register"], "T")

    def test_every_predicate_whose_record_exists_reaches_a_verdict(self):
        self.reading()
        self.mark()
        self.audit()
        found = evaluate(self.obligations, self.situation())
        for identifier, _membership, check in DECLARED:
            with self.subTest(obligation=identifier, predicate=check):
                verdict = found.verdict(identifier)
                if identifier in self.NOT_EVALUABLE_UNTIL_W4_W5:
                    predicate, waiting_for = self.NOT_EVALUABLE_UNTIL_W4_W5[identifier]
                    self.assertEqual(check, predicate)
                    self.assertIs(verdict, Verdict.NOT_EVALUABLE, waiting_for)
                else:
                    self.assertIsNot(
                        verdict, Verdict.NOT_EVALUABLE,
                        f"{check} reads records W1-GRAPH writes and must reach a "
                        "verdict; if it genuinely cannot, say so in "
                        "NOT_EVALUABLE_UNTIL_W4_W5 with the kind it waits for")

    def test_the_allow_list_names_only_predicates_this_registry_carries(self):
        declared = {identifier: check for identifier, _m, check in DECLARED}
        for identifier, (check, waiting_for) in self.NOT_EVALUABLE_UNTIL_W4_W5.items():
            with self.subTest(obligation=identifier):
                self.assertEqual(declared[identifier], check)
                self.assertIn(check, PREDICATES)
                self.assertTrue(waiting_for)

    def test_o5_reads_the_audit_records_own_declaration_of_coverage(self):
        """Decision 5: membership of this cycle in the record's declared coverage,
        never ``current_cycle - n < period``."""

        self.assertIs(evaluate(self.obligations, self.situation()).verdict("o5"),
                      Verdict.NOT_SATISFIED)
        self.audit()
        self.assertIs(evaluate(self.obligations, self.situation()).verdict("o5"),
                      Verdict.SATISFIED)
        self.assertIs(evaluate(self.obligations, self.situation(cycle=9)).verdict("o5"),
                      Verdict.NOT_SATISFIED)

    def test_o3_reads_the_citation_w4_reader_puts_in_the_reading_body(self):
        """The remaining half of the reconciliation: W1-GRAPH passes
        ``ReadingResult.body`` through verbatim, so the citation W4-READER writes
        arrives in the record o3 reads, and the surface it names is W5-DRIVER's
        ``material`` record beside the material bytes."""

        found = evaluate(self.obligations, self.situation())
        self.assertIs(found.verdict("o3"), Verdict.NOT_EVALUABLE)

        surface = self.driver_record({
            "record": mod.MATERIAL, "occurrence_path": "occ/r1.json",
            "text": f"the later record {self.QUOTE} in its own words",
            "sha256": _digest(f"the later record {self.QUOTE} in its own words"),
        })
        self.reading(citation={"quote": self.QUOTE, "surface": surface})
        found = evaluate(self.obligations, self.situation())
        self.assertIs(found.verdict("o3"), Verdict.SATISFIED)
        self.assertIs(found.verdict("p1"), Verdict.SATISFIED)

    # -- decision 1: p7 ----------------------------------------------------- #

    def test_p7_permits_the_dep_edge_from_a_reading_to_the_material_it_reads(self):
        """Decision 1, conjunct by conjunct, on a graph W1-GRAPH populated.

        The material is under study. The reading depends on it - a ``dep`` edge
        landing on a studied node - which is the edge §3 requires so that
        refuting the material leaves the reading ``suspended_unsupported``
        rather than refuted. Nothing attacks the material and the material is
        the source of nothing, so p7 holds.
        """

        self.reading()
        self.mark()
        studied = self.driver_record(
            {"record": mod.STUDY_SET, "keys": [self.material]})
        self.assertTrue(studied)
        situation = self.situation()
        self.assertIn((self.opened[self.RELATION_CELL], self.material),
                      situation.supports)
        self.assertTrue(any(target == self.material
                            for _source, target in situation.supports))
        self.assertFalse(any(target == self.material
                             for _source, target in situation.attacks))
        found = evaluate(self.obligations, situation)
        self.assertIs(found.verdict("p7"), Verdict.SATISFIED)
        self.assertIn("dep onto one", found.checks["p7"].detail)

    def test_p7_refuses_an_att_edge_that_targets_a_node_under_study(self):
        self.reading()
        self.driver_record({"record": mod.STUDY_SET, "keys": [self.material]})
        nu = self.harness.create_artifact(
            b"nu: the attack on the material is sound and relevant",
            provenance=Provenance(role="user"))
        attacker = self.harness.create_artifact(
            b"critic: the material is wrong",
            provenance=Provenance(role="critic"),
            warrants=[Warrant(id="w-material", target=self.material,
                              type=WarrantType.ARGUMENTATIVE, validity_node=nu.id)])
        found = evaluate(self.obligations, self.situation())
        self.assertIs(found.verdict("p7"), Verdict.NOT_SATISFIED)
        self.assertIn(attacker.id, found.checks["p7"].evidence)

    def test_p7_refuses_a_node_under_study_that_is_itself_the_source_of_an_edge(self):
        """Declaring the cell-open nodes under study breaks the second conjunct:
        the default depends on the material and is attacked by the reading, so it
        is both an att target and an edge source. p7 names both."""

        ids = self.reading()
        default = self.opened[self.RELATION_CELL]
        self.driver_record({"record": mod.STUDY_SET, "keys": [default]})
        situation = self.situation()
        self.assertIn((ids.reading, default), situation.attacks)
        self.assertIn((default, self.material), situation.supports)
        found = evaluate(self.obligations, situation)
        self.assertIs(found.verdict("p7"), Verdict.NOT_SATISFIED)
        self.assertIn(default, found.checks["p7"].evidence)
        self.assertIn(ids.reading, found.checks["p7"].evidence)
        self.assertIn("att edge onto a node under study", found.checks["p7"].detail)
        self.assertIn("source of an edge", found.checks["p7"].detail)


class ThePreRegisteredBundleLoadsAsItStands(unittest.TestCase):
    """The first live run's own obligations.json, loaded without amendment."""

    @staticmethod
    def locate() -> Path | None:
        declared = os.environ.get("MINIREASON_LOOP_PREREG")
        candidates = [Path(declared)] if declared else []
        here = Path(__file__).resolve()
        for step in (4, 3):
            if len(here.parents) > step:
                candidates.append(here.parents[step] / "loop-prereg" / "obligations.json")
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        return None

    def test_the_pre_registration_bundle_loads_and_every_check_resolves(self):
        found = self.locate()
        if found is None:
            self.skipTest("the pre-registration bundle is not beside this checkout")
        loaded = load_obligations(found)
        self.assertEqual(len(loaded.failed), 7)
        self.assertEqual(len(loaded.protected), 12)
        self.assertEqual(loaded.structure_digest, loaded.preamble["obligations_sha256"])
        self.assertEqual(pin(loaded), hashlib.sha256(found.read_bytes()).hexdigest())
        for obligation in loaded.entries:
            with self.subTest(obligation=obligation.id):
                self.assertIn(obligation.check, PREDICATES)
                self.assertTrue(obligation.reads)
                self.assertIn(obligation.membership, (FAILED_SET, PROTECTED_SET))


# ---------------------------------------------------------------------------
# The two pre-registration review items this module owns
# ---------------------------------------------------------------------------


class TheTwoDigestsOfOneDocumentAreBothNamed(DocumentTestCase):
    """REVIEW-PREREG PR-02: one document, two digests, neither anonymous.

    The pre-registration text publishes the canonical-body digest; the plan
    identity folds the file digest. They are different values, and a reader who
    finds the plan's pin unequal to the pre-registration's cannot tell whether
    the document shifted. The ruling applied in deviation 1: the file digest
    stays the one ``loop_plan_id`` carries, and the canonical-body digest gets
    a name, so the bundle can publish both and say which is which.
    """

    def setUp(self) -> None:
        super().setUp()
        self.path = self.write(document())
        self.loaded = load_obligations(self.path)

    def test_the_two_digests_of_one_document_differ(self):
        self.assertNotEqual(pin(self.loaded), canonical_pin(self.loaded))

    def test_pin_is_the_bytes_on_disk_and_is_what_custody_would_compute(self):
        self.assertEqual(pin(self.loaded),
                         hashlib.sha256(self.path.read_bytes()).hexdigest())

    def test_canonical_pin_is_the_body_without_the_two_digest_keys(self):
        body = {key: value
                for key, value in json.loads(
                    self.path.read_text(encoding="utf-8")).items()
                if key not in mod.DIGEST_KEYS}
        self.assertEqual(canonical_pin(self.loaded),
                         sha256_hex(canonical_json(body)))
        self.assertEqual(canonical_pin(self.loaded),
                         self.loaded.preamble["obligations_sha256"])

    def test_whitespace_moves_the_file_digest_and_not_the_canonical_one(self):
        """Which is exactly why the identity carries the file digest."""

        respaced = self.path.with_name("respaced.json")
        respaced.write_text(
            json.dumps(json.loads(self.path.read_text(encoding="utf-8")),
                       indent=4),
            encoding="utf-8")
        other = load_obligations(respaced)
        self.assertNotEqual(pin(self.loaded), pin(other))
        self.assertEqual(canonical_pin(self.loaded), canonical_pin(other))

    def test_both_accessors_refuse_anything_that_is_not_a_loaded_document(self):
        for accessor in (pin, canonical_pin):
            with self.subTest(accessor=accessor.__name__):
                with self.assertRaises(ObligationsError) as caught:
                    accessor({"obligations": []})
                self.assertEqual(caught.exception.code, "SITUATION_INVALID")


class ProtectedObligationFourReadsTheRenderedFiles(HarnessTestCase):
    """REVIEW-WAVE1 B1 / REVIEW-PREREG PR-05, fixed and pinned.

    ``p4`` is scoped by the pre-registration to "every artifact the run
    registers, every table header and every file rendered under the run root".
    Until wave 2 the predicate read registered mapping KEYS alone, so a
    ``READING_TABLE.md`` whose header row was ``| cell | rank | tally |``
    satisfied it - the protected obligation the design calls G12's whole point
    could not fail on a rendered table. Each test below is the probe that
    demonstrated it.
    """

    BANNED = ("rank", "tally", "grade")

    def render(self, text: str, where: str = "READING_TABLE.md") -> None:
        """Replace the fixture's clean rendered record with this one.

        ``Situation.one`` reads the first STANDING record of a kind, so the
        fixture's own ``rendered_files`` is withdrawn by an attack before the
        probe's is added - which is also the only way a record leaves a
        situation here: nothing is deleted.
        """

        self.graph.attack(self.graph.ids["rendered_files"], "rendered-replaced")
        self.graph.add("rendered_files_probe",
                       {"record": "rendered_files", "files": {where: text}})

    def verdict(self):
        return mod.no_scoring_key(self.situation())

    def test_a_clean_rendered_table_still_satisfies_the_obligation(self):
        self.assertEqual(self.verdict().verdict, Verdict.SATISFIED)

    def test_a_rendered_table_header_naming_a_forbidden_token_fails_it(self):
        self.render("# Readings\n\n| cell | rank |\n| --- | --- |\n| r1 | x |\n")
        outcome = self.verdict()
        self.assertEqual(outcome.verdict, Verdict.NOT_SATISFIED)
        self.assertIn("READING_TABLE.md", outcome.detail)
        self.assertIn("rank", outcome.detail)

    def test_a_rendered_heading_naming_a_forbidden_token_fails_it(self):
        self.render("## Tally of readings\n\nnothing here\n")
        outcome = self.verdict()
        self.assertEqual(outcome.verdict, Verdict.NOT_SATISFIED)
        self.assertIn("tally", outcome.detail)

    def test_a_quoted_passage_of_the_material_does_not_fail_it(self):
        """The G12 exemption: a rendered file QUOTES the material.

        Refusing a run because a published passage under study carries the word
        is the loop editing its own evidence, which is the boundary
        ``graph.G12_EXEMPT`` draws for the same reason. Only what the loop wrote
        - its headings and its header rows - is read.
        """

        self.render("# Readings\n\n> the account says the rival account ranks "
                    "higher, and the tally it reports is its own\n")
        self.assertEqual(self.verdict().verdict, Verdict.SATISFIED)

    def test_a_prose_line_ending_in_a_pipe_does_not_hide_the_next_header(self):
        """GFM's rule, not "a line ending in a pipe" (standard.py item 40(d))."""

        self.render("# Readings\n\nsee the table below |\n\n| cell | grade |\n"
                    "| --- | --- |\n| r1 | x |\n")
        outcome = self.verdict()
        self.assertEqual(outcome.verdict, Verdict.NOT_SATISFIED)
        self.assertIn("grade", outcome.detail)

    def test_the_witness_list_names_the_rendered_record(self):
        self.render("| cell | rank |\n| --- | --- |\n")
        outcome = self.verdict()
        self.assertIn(self.graph.ids["rendered_files_probe"], outcome.evidence)

    def test_the_vocabulary_is_the_graphs_and_never_a_local_list(self):
        """``obligations`` may not import ``standard``: the ban comes through
        the graph, and a document that declares none leaves p4 unevaluable."""

        source = SOURCE.read_text(encoding="utf-8")
        self.assertNotIn("from minireason.loop.standard", source)
        self.assertNotIn("from .standard", source)
        for token in self.BANNED:
            self.assertIn(token, self.graph_vocabulary())

    def graph_vocabulary(self):
        node = self.situation().one(mod.FORBIDDEN_KEYS)
        return tuple(node.record["keys"])


class ObligationThreeChecksTheOperativeTargetAndNotOnlyUniqueness(HarnessTestCase):
    """REVIEW-WAVE1 S3, the G3 half: a unique resolution is not an operative one.

    A quote resolving uniquely into the pack's banner, its vocabulary list or
    its resolver notes resolves perfectly well and is not a reading of the
    material. Where a citation records which side it resolved on, that side must
    be one of the three ``surface`` calls declared.
    """

    def test_a_citation_that_resolved_in_the_framing_does_not_satisfy_o3(self):
        """G3's half of o3: a unique resolution is not an operative one."""

        here = self.situation()
        node = next((n for n in here.nodes.values()
                     if n.kind == mod.READING_ROW and n.record.get("citation")), None)
        self.assertIsNotNone(node, "the fixture registers a reading row")
        citation = dict(node.record["citation"])
        self.assertTrue(mod._citation_resolves(here, node, "citation"))
        for side, expected in ((mod.DECLARED_SIDES[0], True),
                               ("framing", False),
                               ("not-a-side", False)):
            with self.subTest(side=side):
                probe = mod.Node(id=node.id, status=node.status, role=node.role,
                                 record={**node.record,
                                         "citation": {**citation, "side": side}},
                                 text=node.text)
                self.assertEqual(
                    mod._citation_resolves(here, probe, "citation"), expected)



class ProductionKeepsTheNonEvaluabilityDistinction(HarnessTestCase):
    """Wave-1 integration decision 49: R5 inside ``produced_by``.

    Two different things make an attribution non-empty - the obligation stops
    holding without this cycle's records, or it becomes unreadable without them
    - and ``produced_by`` returns the same shape for both. FW5 R5 is exactly
    that distinction, so :func:`production_of` carries the withheld verdict and
    a reading of it beside the set.
    """

    def test_produced_by_is_the_artifacts_of_production_of(self):
        for entry in self.obligations.entries:
            with self.subTest(obligation=entry.id):
                self.assertEqual(
                    mod.produced_by(self.situation(), entry.id),
                    mod.production_of(self.situation(), entry.id).artifacts)

    def test_a_cycle_that_registered_nothing_has_nothing_to_withhold(self):
        production = mod.production_of(self.situation(), "o1")
        self.assertIsNone(production.withheld_verdict)
        self.assertEqual(production.artifacts, frozenset())
        self.assertIn("nothing to withhold", production.withheld_reading)

    def test_the_withheld_verdict_is_carried_on_the_record(self):
        registered = tuple(self.graph.ids.values())
        production = mod.production_of(
            self.situation(registered=registered), "o1")
        self.assertIn(production.withheld_verdict,
                      (Verdict.SATISFIED, Verdict.NOT_SATISFIED,
                       Verdict.NOT_EVALUABLE))
        self.assertTrue(production.withheld_reading.strip())
        self.assertEqual(production.as_dict()["obligation"], "o1")

    def test_an_unreadable_withheld_view_is_read_as_absence_and_not_as_loss(self):
        registered = tuple(self.graph.ids.values())
        for entry in self.obligations.entries:
            production = mod.production_of(
                self.situation(registered=registered), entry.id)
            if production.withheld_verdict is not Verdict.NOT_EVALUABLE:
                continue
            with self.subTest(obligation=entry.id):
                self.assertIn("absence of evidence", production.withheld_reading)
                self.assertIn("FW5 R5", production.withheld_reading)
                break

    def test_production_of_refuses_anything_that_is_not_a_situation(self):
        with self.assertRaises(ObligationsError) as caught:
            mod.production_of({"nodes": {}}, "o1")
        self.assertEqual(caught.exception.code, "SITUATION_INVALID")


if __name__ == "__main__":
    unittest.main()
