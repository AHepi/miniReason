"""Offline regressions grounded in the immutable smoke-3 public response."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import unittest

from minireason.reason import prompts
from minireason.reason.types import ReasonFailure

FIXTURE = Path(__file__).parent / "fixtures" / "smoke3-base-bare-a00-public.txt"
LEGACY_HASHES = {'conjecture': {'render': '6bbf5150e3d503d6e04471cbc3819f3c00660b7f8116c561e3830ebb52214f11', 'repair': '87864aab3e9887ec79a493b7aa284f3241b637012c6325f8f93390fafe4220a4'}, 'baseline': {'render': 'ad5f6c979d089dd7087ccb30c85a26cfca9396e964215f8a7418b118e4782bcf', 'repair': 'd9989979e681c85adecf53d5a7977f7ec42afff6ed1a41b80f7ef5a7d5cb0fa3'}, 'critic': {'render': 'aa16dd79b43164e11c980257d191fcdf40328497c5bbf3a5284694d5cc8b1d28', 'repair': '0fe100aa0d633f843448098e47e8326f4c1aeb2d5b12a5e0d95bccff68766fd2'}, 'return': {'render': '0d76944c12e860a40b0faba111dab7c759e5a8e5eb8103cc4e1961789d3d0a50', 'repair': '6e26bf4de6ef6d4708f3e642fe40c7250e48acd29a17126562cce35a9fb0635b'}, 'use': {'render': '15908cf61191226c7119778e729438d31ec68bec2ac3f17c94466fe2fb55fa5d', 'repair': '46154c822b39f1ce2b09b587e44f53cb939c053d30f0e3fc161352d7da922b75'}, 'rival': {'render': '060453e795f3c663a6cd8c94d0f24a949e9e8c77917d358d3b95cc520d86e3dd', 'repair': 'e625bc832bcff361e6f30fb8c90729a37385979d44d44eb4b75d948325fb8665'}}


class Review12bPromptTests(unittest.TestCase):
    def content(self):
        with FIXTURE.open(encoding="utf-8", newline="") as handle:
            return handle.read()

    def fails(self, role, data, reason="", **kwargs):
        with self.assertRaises(ReasonFailure) as caught:
            prompts.parse(role, json.dumps(data), **kwargs)
        self.assertEqual(caught.exception.code, "SCHEMA_FAILURE")
        self.assertIn(reason, caught.exception.detail)

    def test_actual_smoke3_baseline_is_strict_json_with_supplemental_fields(self):
        content = self.content()
        self.assertEqual(hashlib.sha256(content.encode("utf-8")).hexdigest(),
                         "954ba0a3cafaba294867a45bd4b976b4d12f9cbdd444e11e3e9ca3e187e2e351")
        original = json.loads(content)
        self.assertEqual(set(original), {"answer", "assumptions", "uncertainties"})
        parsed = prompts.parse("baseline", content)
        self.assertEqual(parsed["assumptions"], original["assumptions"])
        self.assertEqual(parsed["uncertainties"], original["uncertainties"])
        self.assertEqual(parsed["answer"], original["answer"] + "\n\nAssumptions:\n" +
                         original["assumptions"] + "\n\nUncertainties:\n" + original["uncertainties"])

    def test_actual_smoke3_baseline_legacy_schema_still_rejects_extra_fields(self):
        self.fails("baseline", json.loads(self.content()), contract_version="legacy-v1")

    def test_supplemental_lists_are_preserved_and_rendered_for_answer_roles(self):
        data = {"answer": "Conclusion.", "assumptions": ["First premise.", "Second premise."],
                "uncertainties": "Open limitation."}
        for role in ("baseline", "conjecture", "rival"):
            parsed = prompts.parse(role, json.dumps(data))
            self.assertEqual(parsed["assumptions"], data["assumptions"])
            self.assertEqual(parsed["uncertainties"], data["uncertainties"])
            for statement in data["assumptions"] + [data["uncertainties"]]:
                self.assertIn(statement, parsed["answer"])

    def test_supplemental_fields_reject_invalid_values_and_unknown_fields(self):
        for bad in (None, 3, {}, [], [""], ["Premise.", 7], " "):
            self.fails("baseline", {"answer": "Conclusion.", "assumptions": bad},
                       "ANSWER_SUPPLEMENT_NOT_TEXT")
        self.fails("baseline", {"answer": "Conclusion.", "unused": "Not supported."})
        self.fails("critic", {"objections": [], "assumptions": "Not this role."})

    def test_raw_control_characters_are_tolerated_only_in_new_contract(self):
        content = '{"answer":"Line one\nLine two\twith a tab"}'
        with self.assertRaises(json.JSONDecodeError):
            json.loads(content)
        self.assertEqual(prompts.parse("baseline", "Public preamble. " + content)["answer"],
                         "Line one\nLine two\twith a tab")
        with self.assertRaises(ReasonFailure) as caught:
            prompts.parse("baseline", content, contract_version="legacy-v1")
        self.assertEqual(caught.exception.code, "SCHEMA_FAILURE")

    def test_working_is_optional_separate_public_text(self):
        examples = {
            "critic": {"objections": []},
            "use": {"question": "Determine the boundary result.", "problem_derivation": "Independent derivation.",
                    "working_derivation": "Applied derivation.", "objections": []},
            "return": {"answer": "Returned answer.", "dispositions": []},
        }
        for role, data in examples.items():
            self.assertEqual(prompts.parse(role, json.dumps(data)), data)
            for working in ("", "Public exploratory explanation.\nNo final objection remains."):
                with self.subTest(role=role, working=working):
                    result = {**data, "working": working}
                    self.assertEqual(prompts.parse(role, json.dumps(result)), result)
                    self.fails(role, result, contract_version="legacy-v1")
            self.fails(role, {**data, "working": []}, "WORKING_NOT_TEXT")
        self.fails("baseline", {"answer": "Answer.", "working": "Not a supported field for this role."})

    def test_objection_text_bound_applies_to_critic_and_use_only_new_contract(self):
        for role in ("critic", "use"):
            data = {"objections": [{"text": "x" * 1200, "defeats": "Specific claim."}]}
            if role == "use":
                data.update(question="Case.", problem_derivation="Independent result.",
                            working_derivation="Working result.")
            self.assertEqual(prompts.parse(role, json.dumps(data)), data)
            data["objections"][0]["text"] += "x"
            self.fails(role, data, "OBJECTION_TEXT_TOO_LONG")
            self.assertEqual(prompts.parse(role, json.dumps(data), contract_version="legacy-v1"), data)

    def test_working_length_does_not_expand_objection_text(self):
        data = {"working": "Public exploration. " * 400,
                "objections": [{"text": "The zero boundary is omitted.", "defeats": "The universal rule."}]}
        parsed = prompts.parse("critic", json.dumps(data))
        self.assertEqual(parsed, data)
        messages = prompts.render("return", "Problem.", answer="Answer.",
                                  objections=[{"id": "o1", **parsed["objections"][0]}])
        self.assertNotIn(data["working"], messages[1]["content"])
        self.assertIn(data["objections"][0]["text"], messages[1]["content"])

    def test_return_still_requires_every_disposition_with_working(self):
        data = {"answer": "Confirmed with no changes.", "working": "Public explanation.", "dispositions": []}
        self.fails("return", data, objections=[{"id": "o1"}])
        data["dispositions"] = [{"id": "o1", "status": "rejected-with-reason", "reason": "The rule covers the case."}]
        self.assertEqual(prompts.parse("return", json.dumps(data), objections=[{"id": "o1"}]), data)

    def test_contracts_require_separate_working_and_final_objections(self):
        for role in ("critic", "use"):
            system = prompts.render(role, "Problem.")[0]["content"]
            for phrase in ('"working"', "never delivered to the return seat", "final objection statement only",
                           "at most 1200 characters", "empty objections list", "no retracing"):
                self.assertIn(phrase, system)
        returned = prompts.render("return", "Problem.")[0]["content"]
        self.assertIn('"working"', returned)
        self.assertNotIn("return an empty objections list", returned)

    def test_repair_keeps_prior_public_objections_and_named_failure(self):
        content = "The rule omits the empty case; this defeats the claim of complete coverage."
        messages = prompts.render("critic", "Problem.", answer="Answer.")
        repaired = prompts.repair(messages, content, "critic", failure_reason="OBJECTION_TEXT_TOO_LONG")
        self.assertEqual(repaired[-2], {"role": "assistant", "content": content})
        instruction = repaired[-1]["content"]
        for phrase in ("Faithfully convert YOUR OWN preceding public output", "Preserve each concrete objection",
                       "do not drop it", "explicitly withdrawn", "not a fresh answer", "OBJECTION_TEXT_TOO_LONG",
                       "Move exploratory explanation", "Do not invent an objection"):
            self.assertIn(phrase, instruction)
        self.assertEqual(repaired[:-2], messages)
        self.assertTrue(instruction.endswith(prompts._CONTRACTS["critic"]))

    def test_legacy_render_and_repair_match_original_hashes_for_all_roles(self):
        for role, expected in LEGACY_HASHES.items():
            messages = prompts.render(role, "Original problem.", answer="Working answer.",
                                      objections=[{"id": "o1", "text": "Objection.", "defeats": "Claim.",
                                                   "status": "unresolved", "reason": "Pending."}],
                                      rival="Rival.", history=[{"cycle": 1, "answer": "Prior answer."}],
                                      contract_version="legacy-v1")
            repaired = prompts.repair(messages, "Prior public output.", role,
                                      contract_version="legacy-v1", failure_reason="Ignored for frozen legacy bytes.")
            for kind, result in (("render", messages), ("repair", repaired)):
                with self.subTest(role=role, kind=kind):
                    digest = hashlib.sha256(json.dumps(result, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
                    self.assertEqual(digest, expected[kind])

    def test_unknown_contract_version_refuses(self):
        for operation in (
            lambda: prompts.render("critic", "Problem.", contract_version="unknown"),
            lambda: prompts.repair([], "Public output.", "critic", contract_version="unknown"),
            lambda: prompts.parse("critic", '{"objections":[]}', contract_version="unknown"),
        ):
            with self.assertRaises(ReasonFailure) as caught:
                operation()
            self.assertEqual(caught.exception.code, "CONFIG_ERROR")


if __name__ == "__main__":
    unittest.main()
