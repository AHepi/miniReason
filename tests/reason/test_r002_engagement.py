"""Mechanical engagement-contract coverage for R002 helper APIs."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest
import uuid

from minireason.reason import engine
from minireason.reason.r002 import ContractSet, construct_checker_objection, parse_r002
from minireason.reason.types import ReasonFailure


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "experiments/diagnostics/R002-episodes-under-calibrated-difficulty"


class R002EngagementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contracts = ContractSet(SPEC / "contracts")
        relations = json.loads((SPEC / "problems/RELATIONS.json").read_text(encoding="utf-8"))
        forks = json.loads((SPEC / "problems/FORKS.json").read_text(encoding="utf-8"))
        cls.relation = next(item for item in relations["candidates"]
                            if item["candidate_id"] == "C01")
        cls.fork = next(item for item in forks["candidates"]
                        if item["candidate_id"] == "C01")

    def answer(self, red="2/3"):
        first = "C01.posterior_C = 1/2."
        second = f"C01.next_red = {red}."
        return {
            "decision": "answered", "answer": first + " " + second,
            "missing_derivation": "",
            "claims": [
                {"relation_id": "C01.posterior_C", "value": "1/2", "quote": first},
                {"relation_id": "C01.next_red", "value": red, "quote": second},
            ],
            "derivation_steps": [
                {"step_index": 1, "statement": first, "depends_on": []},
                {"step_index": 2, "statement": second, "depends_on": [1]},
            ],
        }

    def objection(self, answer, *, quote=None):
        return {
            "target_claim": "C01.next_red",
            "text": "The final conditional value is disputed.",
            "defeats": "C01.next_red",
            "check": {
                "check_id": "check-1", "kind": "value",
                "inputs": [{"name": "draw", "value": 4, "source": "problem"}],
                "procedure": "Enumerate the conditional draw.",
                "claimed_result": "3/4",
                "falsifies_when": "Enumeration produces 2/3.",
            },
            "fork": {
                "step_index": 2,
                "step_quote": quote if quote is not None else answer["derivation_steps"][1]["statement"],
                "branch_point_id": "C01-fork",
                "earliest_reason": "This is the first step asserting the value.",
            },
        }

    def proposal(self, after, relation_id="C01.next_red"):
        claim = next(item for item in after["claims"] if item["relation_id"] == relation_id)
        return {
            "query_id": "C01-use", "question": "What is the next-red probability?",
            "relation_id": relation_id, "working_claim_quote": claim["quote"],
            "working_value": claim["value"], "language": "python-3.11-restricted",
            "source": "import json\nprint(json.dumps({'relation_id':'C01.next_red','value':'3/4','derivation':'fixture'}))",
            "stdin_json": {},
            "expected_output_schema": {
                "relation_id": "string", "value": "json", "derivation": "string"
            },
        }

    def use(self, before, after, *, relation_id="C01.next_red", depends=True,
            objections=None, checker=True):
        before_claim = next(item for item in before["claims"] if item["relation_id"] == relation_id)
        after_claim = next(item for item in after["claims"] if item["relation_id"] == relation_id)
        return {
            "decision": "answered", "missing_derivation": "",
            "query_id": "C01-use", "question": "What is the next-red probability?",
            "problem_derivation": "Enumerate the stated transition.",
            "before": {"answer_quote": before_claim["quote"], "derivation": "before",
                       "conclusion": before_claim["value"]},
            "after": {"answer_quote": after_claim["quote"], "derivation": "after",
                      "conclusion": after_claim["value"]},
            "dependency": {
                "relation_id": relation_id, "before_quote": before_claim["quote"],
                "after_quote": after_claim["quote"], "result_depends_on_change": depends,
                "explanation": "The selected relation controls this use.",
            },
            "objections": list(objections or []),
            "checker": self.proposal(after, relation_id) if checker else None,
        }

    def parse_use(self, value, before, after):
        return parse_r002(
            "propagation_use", json.dumps(value), self.contracts,
            relation=self.relation, before=before, answer=after, fork=self.fork,
            checker_eligible=True,
        )

    def test_propagation_binds_changed_relation(self):
        before, after = self.answer(), self.answer("3/4")
        parsed = self.parse_use(self.use(before, after), before, after)
        self.assertEqual(parsed["dependency"]["relation_id"], "C01.next_red")
        wrong_relation = self.use(before, after, relation_id="C01.posterior_C", depends=False)
        with self.assertRaisesRegex(ReasonFailure, "bind a changed relation"):
            self.parse_use(wrong_relation, before, after)

    def test_unchanged_use_cannot_claim_dependence_on_change(self):
        answer = self.answer()
        with self.assertRaisesRegex(ReasonFailure, "Unchanged evaluations"):
            self.parse_use(self.use(answer, deepcopy(answer), depends=True), answer, answer)

    def test_use_seat_objection_requires_exact_fork_quote(self):
        before, after = self.answer(), self.answer("3/4")
        value = self.use(before, after, objections=[self.objection(after, quote="fabricated")])
        with self.assertRaisesRegex(ReasonFailure, "Fork locator"):
            self.parse_use(value, before, after)

    def test_checker_working_value_binds_selected_after_claim(self):
        before, after = self.answer(), self.answer("3/4")
        valid = self.use(before, after)
        self.parse_use(valid, before, after)
        invalid = deepcopy(valid)
        invalid["checker"]["working_value"] = "2/3"
        with self.assertRaisesRegex(ReasonFailure, "working_value"):
            self.parse_use(invalid, before, after)

    def test_cannot_decide_return_retains_prior_state(self):
        before = self.answer()
        objection = {"id": "o1", "status": "unresolved", **self.objection(before)}
        value = {
            **deepcopy(before), "decision": "cannot_decide",
            "missing_derivation": "the conditional enumeration is unavailable",
            "dispositions": [{
                "id": "o1", "status": "unresolved", "reason": "Cannot redo the missing enumeration.",
                "redo": {"check_id": "check-1", "status": "cannot_redo",
                         "method": "The required enumeration is missing.", "result": None,
                         "comparison": "inconclusive"},
                "rederivation": {"from_step_index": None, "objection_id": "o1",
                                 "status": "cannot_decide", "steps": [],
                                 "missing_derivation": "the conditional enumeration is unavailable"},
            }],
            "changes": [],
        }
        parsed = parse_r002(
            "tested_return", json.dumps(value), self.contracts,
            relation=self.relation, before=before, objections=[objection],
        )
        self.assertEqual(parsed["claims"], before["claims"])
        self.assertEqual(parsed["derivation_steps"], before["derivation_steps"])
        changed = deepcopy(value)
        changed["claims"][1]["value"] = "3/4"
        with self.assertRaisesRegex(ReasonFailure, "retain prior claims"):
            parse_r002("tested_return", json.dumps(changed), self.contracts,
                       relation=self.relation, before=before, objections=[objection])

    def test_host_checker_mismatch_constructs_one_objection_and_match_none(self):
        working = self.answer()
        proposal = self.proposal(working)
        execution = {
            "status": "COMPLETE", "comparison": "disagrees",
            "parsed": {"relation_id": "C01.next_red", "value": "3/4",
                       "derivation": "host fixture"},
            "stdout_sha256": "a" * 64,
        }
        objection = construct_checker_objection(execution, proposal, working, self.fork)
        self.assertIsNotNone(objection)
        self.assertEqual(objection["target_claim"], "C01.next_red")
        self.assertEqual(objection["fork"]["step_index"], 2)
        matched = deepcopy(execution)
        matched.update(comparison="agrees")
        self.assertIsNone(construct_checker_objection(matched, proposal, working, self.fork))

    def test_closing_only_tail_edit_is_counted_and_marked_without_propagation(self):
        problem = (SPEC / "problems/C01.txt").read_text(encoding="utf-8")
        from tests.reason import artifact_root
        run = artifact_root() / "engagement" / uuid.uuid4().hex
        engine.create_r002_run(
            problem, SPEC / "recipes/r002-tested-cross-v1.json", run,
            mode="offline", cycles=1, problem_id="C01",
            relation_registry=SPEC / "problems/RELATIONS.json",
            fork_registry=SPEC / "problems/FORKS.json",
            coding_manifest=SPEC / "problems/RECODING_MAPS.json",
        )

        def scripted(role, cycle, objections, coordinate, context):
            if role == "answer":
                return self.answer()
            if role == "tested_critic":
                item = self.objection(context["answer"])
                item["check"]["check_id"] = coordinate["call_id"] + "-check"
                return {"decision": "answered", "missing_derivation": "",
                        "working": "bounded closing fixture", "objections": [item]}
            if role == "tested_return":
                closing = coordinate["call_id"] == "closing-return"
                before = context["before"]
                after = self.answer("3/4") if closing else deepcopy(before)
                dispositions = []
                for objection in objections:
                    dispositions.append({
                        "id": objection["id"],
                        "status": "taken-up" if closing else "unresolved",
                        "reason": "closing fixture rederived" if closing else "held open for closing",
                        "redo": {
                            "check_id": objection["check"]["check_id"], "status": "redone",
                            "method": "enumerated the conditional draw",
                            "result": "3/4" if closing else "inconclusive",
                            "comparison": "supports_objection" if closing else "inconclusive",
                        },
                        "rederivation": {
                            "from_step_index": 2 if closing else None,
                            "objection_id": objection["id"],
                            "status": "rederived" if closing else "retained",
                            "steps": [after["derivation_steps"][1]] if closing else [],
                            "missing_derivation": "",
                        },
                    })
                return {**after, "dispositions": dispositions,
                        "changes": ([{"relation_id": "C01.next_red",
                                      "before_quote": before["claims"][1]["quote"],
                                      "after_quote": after["claims"][1]["quote"],
                                      "changed": True, "direction": "toward_objection"}]
                                    if closing else [])}
            if role == "propagation_use":
                before, after = context["before"], context["answer"]
                value = self.use(before, after, depends=False)
                value["dependency"]["explanation"] = "The cycle return retained the relation."
                return value
            raise AssertionError(role)

        state = engine.execute_r002(run, scripted=scripted)
        self.assertEqual(state["stop_reason"], "cycle_budget", state.get("detail"))
        self.assertEqual(state["tail_edits"], 1)
        self.assertTrue(state["objections"])
        self.assertTrue(all(item["check_redone"] == "agrees" for item in state["objections"]))
        for objection in state["objections"]:
            record_path = run / "episodes" / objection["id"] / "closing-return.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            self.assertEqual(record["assembly_status"], "closed_without_propagation")
            self.assertTrue(record["tail_edit"])
            self.assertEqual(record["redo"]["status"], "redone")
            self.assertFalse((record_path.parent / "closing-return-use.json").exists())
        run_text = (run / "RUN.md").read_text(encoding="utf-8")
        self.assertIn("Tail edits: 1.", run_text)
        self.assertIn("check redone: agrees", (run / "TRACE.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
