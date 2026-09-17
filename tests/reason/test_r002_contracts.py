"""Focused R002 schema and semantic contract tests; no provider or network."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from minireason.reason.r002 import (
    ContractSet, _response_object, construct_recoding_objections,
    detect_tail_edit, parse_r002, stall_switch_due,
)
from minireason.reason.types import ReasonFailure


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "experiments/diagnostics/R002-episodes-under-calibrated-difficulty"


class R002ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contracts = ContractSet(SPEC / "contracts")
        relations = json.loads((SPEC / "problems/RELATIONS.json").read_text(encoding="utf-8"))
        forks = json.loads((SPEC / "problems/FORKS.json").read_text(encoding="utf-8"))
        cls.relation = next(item for item in relations["candidates"] if item["candidate_id"] == "C01")
        cls.fork = next(item for item in forks["candidates"] if item["candidate_id"] == "C01")

    def answer(self, posterior="1/2", red="2/3"):
        first = f"C01.posterior_C = {posterior}."
        second = f"C01.next_red = {red}."
        return {"decision": "answered", "answer": first + " " + second,
                "missing_derivation": "",
                "claims": [{"relation_id": "C01.posterior_C", "value": posterior, "quote": first},
                           {"relation_id": "C01.next_red", "value": red, "quote": second}],
                "derivation_steps": [{"step_index": 1, "statement": first, "depends_on": []},
                                     {"step_index": 2, "statement": second, "depends_on": [1]}]}

    def objection(self, *, tested=True, check_id="check-1", step=1):
        item = {"target_claim": "C01.posterior_C", "text": "The likelihood omits an ordered draw.",
                "defeats": "C01.posterior_C",
                "fork": {"step_index": step,
                         "step_quote": self.answer()["derivation_steps"][step - 1]["statement"],
                         "branch_point_id": "C01-fork", "earliest_reason": "This is the first likelihood."}}
        if tested:
            item["check"] = {"check_id": check_id, "kind": "instance",
                             "inputs": [{"name": "draw", "value": 2, "source": "problem"}],
                             "procedure": "Enumerate the ordered draws.", "claimed_result": "1/2",
                             "falsifies_when": "Enumeration agrees with the working value."}
        return item

    def test_every_published_schema_accepts_its_published_or_answered_fixture(self):
        self.contracts.validate("answer.schema.json", self.answer())
        self.contracts.validate("prose-objection.schema.json",
                                {"decision": "answered", "missing_derivation": "", "working": "checked",
                                 "objections": [self.objection(tested=False)]})
        self.contracts.validate("tested-objection.schema.json",
                                {"decision": "answered", "missing_derivation": "", "working": "checked",
                                 "objections": [self.objection()]})
        objection = {"id": "o1", **self.objection()}
        rederivation = {"from_step_index": 1, "objection_id": "o1", "status": "rederived",
                        "steps": self.answer()["derivation_steps"], "missing_derivation": ""}
        self.contracts.validate("tested-return.schema.json",
            {**self.answer(), "dispositions": [{"id": "o1", "status": "taken-up", "reason": "redone",
              "redo": {"check_id": "check-1", "status": "redone", "method": "enumerated",
                       "result": "1/2", "comparison": "supports_objection"}, "rederivation": rederivation}],
             "changes": []})
        prose = {**self.answer(), "dispositions": [{"id": "o1", "status": "taken-up",
                 "reason": "rederived", "rederivation": rederivation}], "changes": []}
        self.contracts.validate("prose-return.schema.json", prose)
        solve = {"decision": "answered", "missing_derivation": "", "coding_id": "C01-recoded",
                 "claims": [{"relation_id": "C01.posterior_C", "value": "1/2", "support": "derived"},
                            {"relation_id": "C01.next_red", "value": "2/3", "support": "derived"}],
                 "derivation": "public derivation", "derivation_steps": self.answer()["derivation_steps"]}
        self.contracts.validate("recoding-solve.schema.json", solve)
        proposal = {"query_id": "q1", "question": "Compute it", "relation_id": "C01.posterior_C",
                    "working_claim_quote": "C01.posterior_C = 1/2.", "working_value": "1/2",
                    "language": "python-3.11-restricted", "source": "print('{}')", "stdin_json": {},
                    "expected_output_schema": {"relation_id": "string", "value": "json", "derivation": "string"}}
        self.contracts.validate("checker-proposal.schema.json", proposal)
        execution = {"schema": "minireason.r002.checker-execution.v1", "proposal_sha256": "a" * 64,
                     "policy_sha256": "b" * 64, "sandbox_backend": "fixture", "runtime_identity": "python",
                     "runtime_sha256": "c" * 64, "source_sha256": "d" * 64, "stdin_sha256": "e" * 64,
                     "started_utc": "2026-09-17T00:00:00Z", "elapsed_ms": 1, "status": "COMPLETE",
                     "limit_breaches": [], "exit_code": 0, "stdout_utf8": "{}", "stderr_utf8": "",
                     "stdout_sha256": "f" * 64,
                     "parsed": {"relation_id": "C01.posterior_C", "value": "1/2", "derivation": "fixture"},
                     "comparison": "agrees"}
        self.contracts.validate("checker-execution.schema.json", execution)
        use = {"decision": "answered", "missing_derivation": "", "query_id": "q1",
               "question": "Compute it", "problem_derivation": "derived", "before": {"answer_quote": "C01.posterior_C = 1/2.", "derivation": "d", "conclusion": "1/2"},
               "after": {"answer_quote": "C01.posterior_C = 1/2.", "derivation": "d", "conclusion": "1/2"},
               "dependency": {"relation_id": "C01.posterior_C", "before_quote": "C01.posterior_C = 1/2.",
                              "after_quote": "C01.posterior_C = 1/2.", "result_depends_on_change": False,
                              "explanation": "retained"}, "objections": [], "checker": proposal}
        self.contracts.validate("propagation-use.schema.json", use)
        self.contracts.validate("native-match-note.schema.json",
                                {"decision": "answered", "missing_derivation": "", "answer": "fixture", "derivation": "fixture"})
        self.contracts.validate("relations.schema.json",
                                json.loads((SPEC / "problems/RELATIONS.json").read_text(encoding="utf-8")))
        self.contracts.validate("coding-manifest.schema.json",
                                json.loads((SPEC / "problems/RECODING_MAPS.json").read_text(encoding="utf-8")))

    def test_every_response_role_accepts_explicit_cannot_decide(self):
        missing = "the likelihood derivation is absent"
        fixtures = {
            "answer.schema.json": {"decision": "cannot_decide", "answer": "", "missing_derivation": missing, "claims": [], "derivation_steps": []},
            "prose-objection.schema.json": {"decision": "cannot_decide", "missing_derivation": missing, "working": "", "objections": []},
            "tested-objection.schema.json": {"decision": "cannot_decide", "missing_derivation": missing, "working": "", "objections": []},
            "recoding-solve.schema.json": {"decision": "cannot_decide", "missing_derivation": missing, "coding_id": "C01-recoded", "claims": [], "derivation": "", "derivation_steps": []},
            "native-match-note.schema.json": {"decision": "cannot_decide", "missing_derivation": missing, "answer": "", "derivation": ""},
        }
        for schema, value in fixtures.items():
            with self.subTest(schema=schema):
                self.contracts.validate(schema, value)

    def test_strict_json_rejects_surrounding_text_duplicate_keys_and_nan(self):
        for text in ('before {"a":1}', '{"a":1} after', '{"a":1,"a":2}', '{"a":NaN}'):
            with self.subTest(text=text), self.assertRaises(ReasonFailure):
                _response_object(text)

    def test_role_schema_closures_resolve_every_local_reference(self):
        expected = {
            "answer": {"answer.schema.json"},
            "initial_decompose": {"initial-decompose.schema.json"},
            "decomposed_step": {"decomposed-step.schema.json"},
            "decomposed_critic": {"tested-objection.schema.json"},
            "decomposed_return": {"decomposed-return.schema.json"},
            "decomposed_use": {"decomposed-use.schema.json"},
            "decomposed_synthesis": {"answer.schema.json"},
            "prose_critic": {"prose-objection.schema.json"},
            "tested_critic": {"tested-objection.schema.json"},
            "prose_return": {"prose-return.schema.json", "answer.schema.json", "tested-return.schema.json"},
            "tested_return": {"tested-return.schema.json", "answer.schema.json"},
            "propagation_use": {"propagation-use.schema.json", "tested-objection.schema.json", "checker-proposal.schema.json"},
            "blind_coding_solve": {"recoding-solve.schema.json", "answer.schema.json"},
            "native_match_note": {"native-match-note.schema.json"},
            "native_match_synthesis": {"native-match-note.schema.json"},
        }
        for role, names in expected.items():
            with self.subTest(role=role):
                closure = self.contracts.closure(role)
                self.assertEqual({name for name, _schema in closure}, names)
                self.assertEqual(closure[0][0], next(name for name in names if name.startswith({
                    "answer": "answer", "prose_critic": "prose-objection", "tested_critic": "tested-objection",
                    "initial_decompose": "initial-decompose", "decomposed_step": "decomposed-step",
                    "decomposed_critic": "tested-objection", "decomposed_return": "decomposed-return",
                    "decomposed_use": "decomposed-use", "decomposed_synthesis": "answer",
                    "prose_return": "prose-return", "tested_return": "tested-return",
                    "propagation_use": "propagation-use", "blind_coding_solve": "recoding-solve",
                    "native_match_note": "native-match-note", "native_match_synthesis": "native-match-note",
                }[role])))
                text = "\n".join(block for _label, block in self.contracts.prompt_blocks(role))
                for _name, schema in closure:
                    self.assertIn(json.dumps(schema["$id"]), text)
                if role not in {"native_match_note", "native_match_synthesis"}:
                    self.assertIn("cannot_decide", text)

    def test_answer_rejects_missing_relation_bad_quote_and_noncontiguous_steps(self):
        for mutate in (
            lambda value: value["claims"].pop(),
            lambda value: value["claims"][0].update(quote="not in answer"),
            lambda value: value["derivation_steps"][1].update(step_index=3),
        ):
            value = self.answer()
            mutate(value)
            with self.assertRaises(ReasonFailure):
                parse_r002("answer", json.dumps(value), self.contracts, relation=self.relation)

    def test_tested_critic_requires_exact_fork_and_unique_check_ids(self):
        data = {"decision": "answered", "missing_derivation": "", "working": "checked",
                "objections": [self.objection(check_id="same"), self.objection(check_id="same", step=2)]}
        with self.assertRaises(ReasonFailure):
            parse_r002("tested_critic", json.dumps(data), self.contracts, relation=self.relation,
                       answer=self.answer(), fork=self.fork)
        data["objections"] = [self.objection()]
        data["objections"][0]["fork"]["step_quote"] = "late fabricated quote"
        with self.assertRaises(ReasonFailure):
            parse_r002("tested_critic", json.dumps(data), self.contracts, relation=self.relation,
                       answer=self.answer(), fork=self.fork)

    def test_tested_return_requires_exact_redo_and_rederivation_suffix(self):
        before = self.answer()
        objection = {"id": "o1", "status": "unresolved", **self.objection()}
        data = {**before, "dispositions": [{"id": "o1", "status": "rejected-with-reason", "reason": "no",
                "redo": {"check_id": "wrong", "status": "redone", "method": "redo", "result": None,
                         "comparison": "inconclusive"},
                "rederivation": {"from_step_index": None, "objection_id": "o1", "status": "retained",
                                 "steps": [], "missing_derivation": ""}}], "changes": []}
        with self.assertRaises(ReasonFailure):
            parse_r002("tested_return", json.dumps(data), self.contracts, relation=self.relation,
                       before=before, objections=[objection])
        data["dispositions"][0]["redo"].update(check_id="check-1", status="cannot_redo")
        with self.assertRaises(ReasonFailure):
            parse_r002("tested_return", json.dumps(data), self.contracts, relation=self.relation,
                       before=before, objections=[objection])

    def test_tail_edit_recoding_disagreement_and_stall_gate(self):
        before = self.answer()
        after = self.answer(red="3/4")
        self.assertTrue(detect_tail_edit(before, after, {"status": "taken-up"}))
        canonical = {"decision": "answered", "claims": [
            {"relation_id": "C01.posterior_C", "value": "1/2"},
            {"relation_id": "C01.next_red", "value": "2/3"}], "derivation": "canonical"}
        recoded = deepcopy(canonical)
        recoded["claims"][1]["value"] = "3/4"
        objections = construct_recoding_objections(canonical, recoded, before, self.fork,
                                                    map_identity='{"type":"identity"}')
        self.assertEqual(len(objections), 1)
        self.assertEqual(objections[0]["target_claim"], "C01.next_red")
        open_item = {"id": "o1", "fork": {"step_index": 1}}
        ids = [item["relation_id"] for item in self.relation["relations"]]
        self.assertTrue(stall_switch_due(before, deepcopy(before), deepcopy(before), [open_item], ids))
        changed = self.answer(red="3/4")
        self.assertFalse(stall_switch_due(before, changed, changed, [open_item], ids))
        unknown = deepcopy(before); unknown["claims"].pop()
        self.assertIsNone(stall_switch_due(before, unknown, unknown, [open_item], ids))


if __name__ == "__main__":
    unittest.main()
