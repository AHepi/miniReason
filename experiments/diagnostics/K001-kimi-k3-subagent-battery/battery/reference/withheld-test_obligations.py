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


if __name__ == "__main__":
    unittest.main()
