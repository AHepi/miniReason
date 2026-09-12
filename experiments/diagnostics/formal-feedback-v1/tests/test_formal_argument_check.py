"""Instrument tests using operator-authored arguments; zero LLM calls."""

from copy import deepcopy
import importlib.util
import itertools
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("formal_argument_check", ROOT / "tools" / "formal_argument_check.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


def fixture(name):
    return json.loads((ROOT / "fixtures" / (name + ".json")).read_text())


class FiniteArgumentTests(unittest.TestCase):
    def test_primitive_truth_tables(self):
        rows = [(False, False), (False, True), (True, False), (True, True)]
        expected = {"and": [False, False, False, True],
                    "or": [False, True, True, True],
                    "implies": [True, True, False, True],
                    "iff": [True, False, False, True]}
        for operator, truth_table in expected.items():
            actual = [checker.evaluate({operator: ["a", "b"]}, {"a": a, "b": b}) for a, b in rows]
            self.assertEqual(actual, truth_table, operator)
        self.assertEqual([checker.evaluate({"not": "a"}, {"a": a}) for a in (False, True)], [True, False])

    def test_every_declared_probe_has_its_expected_classification(self):
        manifest = json.loads((ROOT / "fixtures" / "manifest.json").read_text())
        for entry in manifest["fixtures"]:
            with self.subTest(entry["id"]):
                result = checker.check_file(ROOT / "fixtures" / entry["input"])
                self.assertEqual(result["classification"], entry["expected_classification"])

    def test_inconsistent_premises_never_certify_goal(self):
        arg = fixture("inconsistent_candidate")
        result = checker.check_argument(arg)
        self.assertEqual(result["classification"], "inconsistent")
        self.assertEqual(result["premise_model_count"], 0)
        self.assertEqual(result["valuations_checked"], 16)
        self.assertEqual(result["premise_ids"], [p["id"] for p in arg["premises"]])
        for key in ("satisfying_witness", "goal_countermodel", "negation_countermodel"):
            self.assertIsNone(result[key])
        self.assertNotIn("minimum_core", result)

    def test_conditional_entailment_reports_model_not_unconditional_truth(self):
        result = checker.check_argument(fixture("conditional_entailment"))
        self.assertEqual(result["classification"], "entailed")
        self.assertIsNone(result["goal_countermodel"])
        self.assertIsNotNone(result["negation_countermodel"])
        self.assertFalse(result["satisfying_witness"]["ack"])
        self.assertFalse(result["satisfying_witness"]["safe"])

    def test_refuted_claim_has_exact_countermodel(self):
        result = checker.check_argument(fixture("refuted_claim"))
        self.assertEqual(result["classification"], "refuted")
        self.assertEqual(result["premise_model_count"], 1)
        self.assertEqual(result["goal_countermodel"], {"a": True, "ack": True, "b": False, "safe": False})
        self.assertIsNone(result["negation_countermodel"])

    def test_underdetermination_exposes_both_incompatible_goal_values(self):
        result = checker.check_argument(fixture("underdetermined_claim"))
        self.assertEqual(result["classification"], "undetermined")
        self.assertEqual(result["premise_model_count"], 3)
        self.assertEqual(result["goal_countermodel"], {"a": False, "ack": True, "b": True, "safe": False})
        self.assertEqual(result["negation_countermodel"], {"a": True, "ack": True, "b": True, "safe": True})

    def test_inadequate_mapping_and_collision_still_formally_entail(self):
        for name in ("consistent_inadequate_mapping", "meaning_collision"):
            argument = fixture(name)
            result = checker.check_argument(argument)
            self.assertEqual(result["classification"], "entailed")
            self.assertEqual(result["original_argument"]["problem"], fixture("conditional_entailment")["problem"])
            self.assertEqual(result["original_argument"]["atoms"], argument["atoms"])
            self.assertFalse(result["feedback"]["semantic_endorsement"])
            self.assertIn("Atom meanings and prose objections are preserved but not evaluated", result["feedback"]["formal_limit"])

    def test_prose_and_objections_preserved_even_when_invalid(self):
        argument = fixture("invalid_symbol")
        argument["prose_objections"].append("∀ future loss: this temporal objection is legitimate prose.")
        before = deepcopy(argument)
        result = checker.check_argument(argument)
        self.assertEqual(argument, before)
        self.assertEqual(result["original_argument"], before)
        self.assertEqual(result["valuations_checked"], 0)
        self.assertFalse(result["feedback"]["automatic_problem_promotion"])

    def test_full_validation_precedes_any_evaluation(self):
        argument = fixture("conditional_entailment")
        argument["premises"].append({"id": "bad_late_premise", "formula": {"and": ["a", "missing"]}})
        argument["goal"]["formula"] = {"not": "another_missing"}
        with patch.object(checker, "evaluate", side_effect=AssertionError("evaluation must not start")):
            result = checker.check_argument(argument)
        self.assertEqual(result["classification"], "invalid")
        self.assertTrue(any("missing." in e["message"] for e in result["issues"]))
        self.assertTrue(any("another_missing" in e["message"] for e in result["issues"]))

    def test_atom_budget_and_invalidity_remain_distinct(self):
        argument = fixture("out_of_budget")
        result = checker.check_argument(argument)
        self.assertEqual(result["classification"], "unsupported")
        self.assertEqual(result["valuations_checked"], 0)
        argument["goal"]["formula"] = "undeclared"
        result = checker.check_argument(argument)
        self.assertEqual(result["classification"], "invalid")
        self.assertEqual({item["kind"] for item in result["issues"]}, {"unsupported", "invalid"})

    def test_depth_per_formula_and_total_node_limits(self):
        deep = fixture("conditional_entailment")
        formula = "a"
        for _ in range(checker.LIMITS["max_formula_depth"]):
            formula = {"not": formula}
        deep["goal"]["formula"] = formula
        wide = fixture("conditional_entailment")
        wide["goal"]["formula"] = {"and": ["a"] * checker.LIMITS["max_formula_nodes"]}
        total = fixture("conditional_entailment")
        total["premises"] = [{"id": f"p_{i}", "formula": {"and": ["a"] * 400}} for i in range(6)]
        for argument, label in ((deep, "depth"), (wide, "formula_nodes"), (total, "total_formula_nodes")):
            with self.subTest(label), patch.object(checker, "evaluate", side_effect=AssertionError("must not evaluate")):
                result = checker.check_argument(argument)
                self.assertEqual(result["classification"], "unsupported")
                self.assertTrue(any(label in item["message"] for item in result["issues"]))

    def test_exact_atom_limit_remains_executable(self):
        argument = fixture("out_of_budget")
        del argument["atoms"]["extra_6"]
        result = checker.check_argument(argument)
        self.assertEqual(result["classification"], "entailed")
        self.assertEqual(result["valuations_checked"], 1024)

    def test_bad_operators_arity_and_formula_ids_are_rejected(self):
        replacements = [{"exec": "arbitrary text"}, {"implies": ["a"]},
                        {"not": ["a"]}, {"and": []}, {"and": ["a", "b"], "or": ["a", "b"]}, 1]
        for formula in replacements:
            argument = fixture("conditional_entailment")
            argument["goal"]["formula"] = formula
            with self.subTest(formula):
                self.assertEqual(checker.check_argument(argument)["classification"], "invalid")
        argument = fixture("conditional_entailment")
        argument["goal"]["id"] = argument["premises"][0]["id"]
        self.assertEqual(checker.check_argument(argument)["classification"], "invalid")

    def test_duplicate_json_keys_cannot_silently_replace_prose(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            path.write_text('{"problem":"original", "problem":"replacement"}')
            result = checker.check_file(path)
            self.assertEqual(result["classification"], "invalid")
            self.assertIn("Duplicate JSON key", result["issues"][0]["message"])
            self.assertEqual(result["input_retained_at"], str(path))
            self.assertIn('"original"', path.read_text())

    def test_input_byte_limit_retains_original_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "large.json"
            original = '"' + 'x' * checker.LIMITS["max_input_bytes"] + '"'
            path.write_text(original)
            result = checker.check_file(path)
            self.assertEqual(result["classification"], "unsupported")
            self.assertEqual(result["valuations_checked"], 0)
            self.assertEqual(path.read_text(), original)

    def test_recoding_preserves_all_premise_models_and_goal_values(self):
        original, recoded = fixture("conditional_entailment"), fixture("valid_symbol_recoding")
        mapping = {"ack": "q", "a": "r", "b": "s", "safe": "t"}
        for values in itertools.product((False, True), repeat=4):
            valuation = dict(zip(sorted(original["atoms"]), values))
            renamed = {mapping[key]: value for key, value in valuation.items()}
            for left, right in zip(original["premises"] + [original["goal"]], recoded["premises"] + [recoded["goal"]]):
                self.assertEqual(checker.evaluate(left["formula"], valuation), checker.evaluate(right["formula"], renamed))
        self.assertEqual({mapping[k]: v for k, v in original["atoms"].items()}, recoded["atoms"])

    def test_deterministic_result_and_nonautomatic_supplied_revision(self):
        draft = fixture("inconsistent_candidate")
        revision = fixture("conditional_entailment")
        before = deepcopy((draft, revision))
        result = checker.supplied_revision_replay(draft, revision)
        self.assertEqual(result["draft"]["classification"], "inconsistent")
        self.assertEqual(result["supplied_revision"]["classification"], "entailed")
        self.assertFalse(result["revision_generated_by_checker"])
        self.assertFalse(result["revision_semantically_accepted"])
        self.assertEqual((draft, revision), before)
        self.assertEqual(result, checker.supplied_revision_replay(draft, revision))

    def test_satisfiable_vacuity_is_not_an_acknowledged_write_case(self):
        result = checker.check_argument(fixture("vacuous_conditional"))
        self.assertEqual(result["classification"], "entailed")
        self.assertEqual(result["premise_model_count"], 8)
        self.assertFalse(result["satisfying_witness"]["ack"])
        self.assertFalse(result["satisfying_witness"]["safe"])
        self.assertIn("Vacuity and circular support can pass", result["feedback"]["formal_limit"])

    def test_goal_as_premise_entails_without_independent_support(self):
        argument = fixture("circular_support")
        self.assertEqual(argument["premises"][0]["formula"], argument["goal"]["formula"])
        result = checker.check_argument(argument)
        self.assertEqual(result["classification"], "entailed")
        self.assertFalse(result["feedback"]["semantic_endorsement"])
        self.assertIn("assumed conclusion", result["feedback"]["possible_next_inquiry"])


if __name__ == "__main__":
    unittest.main()
