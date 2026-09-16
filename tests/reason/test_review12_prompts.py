"""Offline judge checks for public prompt contracts and response framing."""
from __future__ import annotations
import copy
import json
import unittest
from minireason.reason import prompts
from minireason.reason.types import ReasonFailure


class Review12PromptTests(unittest.TestCase):
    def assert_schema_failure(self, role, content, **kwargs):
        with self.assertRaises(ReasonFailure) as caught:
            prompts.parse(role, content, **kwargs)
        self.assertEqual(caught.exception.code, "SCHEMA_FAILURE")

    def test_fenced_object_and_surrounding_prose_are_accepted(self):
        expected = {"answer": "A public working answer."}
        payload = json.dumps(expected)
        for content in [payload, "```json\n" + payload + "\n```",
                        "Here is the answer.\n" + payload + "\nThis is the end.",
                        "Public preamble.\n```JSON\n" + payload + "\n```\nPublic suffix."]:
            with self.subTest(content=content):
                self.assertEqual(prompts.parse("conjecture", content), expected)

    def test_balanced_brace_notation_in_prose_is_skipped(self):
        content = 'Use {x, y} and [case notation] here.\n{"answer": "A public conclusion."}'
        self.assertEqual(prompts.parse("conjecture", content)["answer"], "A public conclusion.")

    def test_quoted_braces_and_escaped_quotes_do_not_end_object(self):
        expected = {"answer": 'A set {x, y}, a bracket ], an escaped "quote", and a path \\ are public. ' + chr(955)}
        self.assertEqual(prompts.parse("baseline", "Preamble. " + json.dumps(expected) + " suffix."), expected)

    def test_first_object_is_used_even_when_a_later_object_matches(self):
        self.assert_schema_failure("conjecture", '{"wrong": "first"} {"answer": "later"}')
        self.assertEqual(prompts.parse("conjecture", '{"answer": "first"} {"answer": "later"}'),
                         {"answer": "first"})

    def test_nested_objects_in_array_or_malformed_enclosure_are_not_salvaged(self):
        for content in ['[{"answer": "nested"}]', '{bad: {"answer": "nested"}}',
                        'Preamble {"missing": {"answer": "nested"}', 'No object present.', None]:
            with self.subTest(content=content):
                self.assert_schema_failure("conjecture", content)

    def test_minimal_use_contract_accepts_two_public_derivations(self):
        result = {"question": "Determine whether the proposed rule includes the empty case.",
                  "problem_derivation": "The PROBLEM quantifies over every finite set. The empty set is finite, so it is included.",
                  "working_derivation": "The WORKING ANSWER restricts its rule to nonempty sets. It cannot decide the empty case.",
                  "objections": [{"text": "The rule cannot decide the empty case included by the problem.",
                                  "defeats": "The claim that the rule handles every finite set."}]}
        self.assertEqual(prompts.parse("use", json.dumps(result)), result)

    def test_use_rejects_legacy_contract_extra_blank_or_nonstrings(self):
        valid = {"question": "Determine the empty-case result.", "problem_derivation": "Public independent derivation and conclusion.",
                 "working_derivation": "Public working-answer derivation and conclusion.", "objections": []}
        variants = [{"question": valid["question"], "answer": "Applied result.", "dependency": "Prior answer.", "objections": []}]
        for key in ("question", "problem_derivation", "working_derivation"):
            for invalid in ("", "  ", [], None, 1):
                variants.append({**valid, key: invalid})
        variants.append({**valid, "extra": "Not in the contract."})
        variants.append({**valid, "objections": [{"text": "An objection.", "defeats": ""}]})
        for result in variants:
            with self.subTest(result=result):
                self.assert_schema_failure("use", json.dumps(result), contract_version="public-working-v1")

    def test_use_contract_requires_independence_and_disagreement_objection(self):
        contract = prompts.render("use", "Original problem.", answer="Current working answer.")[0]["content"]
        for wording in ("concrete question", "PROBLEM alone", "without relying on the WORKING ANSWER",
                        "Separately derive", "show the public derivation and its conclusion",
                        "conclusions disagree", "WORKING ANSWER cannot decide", "trivially confirmatory",
                        '"problem_derivation"', '"working_derivation"'):
            self.assertIn(wording, contract)

    def test_critic_contract_requires_checkable_objections_and_rejects_caveat_requests(self):
        contract = prompts.render("critic", "Original problem.")[0]["content"]
        for wording in ("specific and checkable", "exact step or claim", "evidence or derivation",
                        "show it wrong", "merely request more caveats", "concrete failure in its recorded disposition"):
            self.assertIn(wording, contract)

    def test_critic_render_preserves_objections_dispositions_history_and_rival(self):
        objection = {"id": "c0001-k01-o001", "text": "First objection.\r\nExact  spacing.",
                     "defeats": "The universal claim.", "status": "rejected-with-reason",
                     "reason": "The displayed derivation covers the case."}
        history = [{"cycle": 1, "answer": "Prior returned answer.", "dispositions": [dict(objection)]}]
        messages = prompts.render("critic", "Original  problem.\r\nNext line.", answer="Current answer.",
                                  objections=[objection], history=history, rival="Independent rival wording.")
        content = messages[1]["content"]
        for value in ("Original  problem.\r\nNext line.", "Current answer.", "Independent rival wording.",
                      objection["text"], objection["defeats"], objection["status"], objection["reason"]):
            self.assertIn(value, content)
        encoded_history = content.split("Prior disposition history (exact JSON values):\n", 1)[1]
        self.assertEqual(json.loads(encoded_history), history)

    def test_repair_preserves_messages_and_adds_own_output_with_exact_contract(self):
        for role in ("baseline", "conjecture", "critic", "return", "use", "rival"):
            with self.subTest(role=role):
                original = prompts.render(role, "Exact problem.", answer="Exact working answer.")
                before = copy.deepcopy(original)
                content = 'Public response {"not": "the role schema"}.'
                repaired = prompts.repair(original, content, role)
                self.assertEqual(original, before)
                self.assertEqual(repaired[:-2], before)
                self.assertIsNot(repaired[0], original[0])
                self.assertEqual(repaired[-2], {"role": "assistant", "content": content})
                self.assertEqual(repaired[-1]["role"], "user")
                self.assertTrue(repaired[-1]["content"].endswith(prompts._contracts(prompts.CURRENT_CONTRACT)[role]))
                self.assertIn("Preserve its substantive content and conclusions", repaired[-1]["content"])
                self.assertIn("do not solve again", repaired[-1]["content"])

    def test_repair_unknown_role_is_configuration_failure(self):
        with self.assertRaises(ReasonFailure) as caught:
            prompts.repair([], "Public output.", "unknown")
        self.assertEqual(caught.exception.code, "CONFIG_ERROR")

    def test_fenced_return_keeps_exact_disposition_validation(self):
        objection = {"id": "c0001-k01-o001"}
        data = {"answer": "Updated working answer.", "dispositions": [
            {"id": objection["id"], "status": "taken-up", "reason": "The counterexample changes the rule."}]}
        self.assertEqual(prompts.parse("return", "```json\n" + json.dumps(data) + "\n```", objections=[objection]), data)
        data["dispositions"].append(dict(data["dispositions"][0]))
        self.assert_schema_failure("return", json.dumps(data), objections=[objection])


if __name__ == "__main__":
    unittest.main()
