from __future__ import annotations

import unittest

from minireason.pilot.router import select_template
from minireason.pilot.templates import (
    CATALOGUE_VERSION,
    COMMON_INPUT_SCHEMA,
    OUTPUT_SCHEMA,
    TEMPLATES,
    normalize_inputs,
    validate,
    validate_inputs,
)


class CatalogueTests(unittest.TestCase):
    def test_catalogue_has_five_bounded_entries(self) -> None:
        self.assertEqual(
            set(TEMPLATES),
            {"direct_answer", "evidence_read", "engineer_patch", "critic_return", "decompose_synthesize"},
        )
        for template_id, entry in TEMPLATES.items():
            self.assertEqual(entry["id"], template_id)
            self.assertEqual(entry["version"], CATALOGUE_VERSION)
            self.assertEqual(entry["thinking"], "off")
            self.assertLessEqual(entry["ceilings"]["max_children"], 3)
            self.assertLessEqual(entry["ceilings"]["max_depth"], 2)
            self.assertTrue(entry["repair_rule"])
            self.assertFalse(entry["cost_envelope"]["price_promise_without_bound"])
            self.assertTrue(entry["evidence_refs"])

    def test_common_input_normalization_is_strict(self) -> None:
        inputs = normalize_inputs("How many?", {"premises": ["2+2"]})
        self.assertEqual(inputs["answer_shape"], "plain answer")
        self.assertEqual(inputs["decisive_question"], "How many?")
        validate(inputs, COMMON_INPUT_SCHEMA)
        validate_inputs("direct_answer", inputs)
        with self.assertRaises(ValueError):
            normalize_inputs("x", {"invented": True})

    def test_common_output_rejects_extra_fields(self) -> None:
        output = {
            "status": "complete",
            "answer": "4",
            "source_refs": [],
            "unresolved": [],
            "verification_refs": [],
        }
        validate(output, OUTPUT_SCHEMA)
        output["hidden_reasoning"] = "must not persist"
        with self.assertRaises(ValueError):
            validate(output, OUTPUT_SCHEMA)


    def test_critic_output_requires_structured_dispositions(self) -> None:
        schema = TEMPLATES["critic_return"]["output_schema"]
        output = {
            "status": "complete",
            "answer": "revised",
            "source_refs": [],
            "unresolved": [],
            "verification_refs": [],
            "objections": [{"id": "o1", "target": "claim", "grounds": "counterexample"}],
            "dispositions": [{"id": "o1", "status": "taken-up", "reason": "fixed"}],
            "revision": "revised",
            "dependent_use": "the implication still holds",
        }
        validate(output, schema)
        output["dispositions"] = ["o1"]
        with self.assertRaises(ValueError):
            validate(output, schema)


class RouterTests(unittest.TestCase):
    def test_structured_features_override_misleading_words(self) -> None:
        result = select_template({
            "task": "Critique this wording, but use the supplied records.",
            "features": {"exact_source": True},
            "inputs": {
                "documents": [{"id": "r1", "text": "decisive evidence"}],
                "requested_claims": ["the decisive claim"],
            },
        })
        self.assertEqual(result["template_id"], "evidence_read")
        self.assertFalse(result["fallback"])

    def test_all_obvious_structured_routes(self) -> None:
        cases = [
            ({"short_closed": True}, {}, "direct_answer"),
            ({"exact_source": True}, {"documents": [{"id": "d", "text": "x"}], "requested_claims": ["x"]}, "evidence_read"),
            ({"bounded_code_change": True}, {"allowed_files": ["a.py"], "documents": [{"id": "a.py", "text": "pass"}], "behavior_contract": "return 1", "test_commands": ["test"]}, "engineer_patch"),
            ({"disputed_candidate": True}, {"candidate": "claim", "premises": ["p"], "objections": ["o1"], "protected_obligations": ["keep p"]}, "critic_return"),
            ({"separable_dependencies": True}, {}, "decompose_synthesize"),
        ]
        for features, inputs, expected in cases:
            with self.subTest(expected=expected):
                result = select_template({"task": "bounded task", "features": features, "inputs": inputs})
                self.assertEqual(result["template_id"], expected)

    def test_invalid_and_unsuitable_proposals_fall_back(self) -> None:
        task = {"task": "What is 2 + 2?", "features": {"short_closed": True}}
        invalid = select_template(task, {"template_id": "invented", "reason": "because"})
        self.assertEqual(invalid["template_id"], "direct_answer")
        self.assertTrue(invalid["fallback"])
        unsuitable = select_template(task, {"template_id": "evidence_read", "reason": "read it"})
        self.assertEqual(unsuitable["template_id"], "direct_answer")
        self.assertTrue(unsuitable["fallback"])
        accepted = select_template(task, {"template_id": "direct_answer", "reason": "Short closed arithmetic."})
        self.assertFalse(accepted["fallback"])
        self.assertEqual(accepted["reason"], "Short closed arithmetic.")

    def test_missing_critical_information_stops(self) -> None:
        result = select_template({
            "task": "Quote the file.",
            "features": {"exact_source": True},
        })
        self.assertEqual(result["template_id"], "cannot_decide")
        self.assertIn("task-critical", result["reason"])


if __name__ == "__main__":
    unittest.main()
