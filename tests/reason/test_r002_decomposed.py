"""Offline tests for the preregistered R002 decomposition amendment."""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
import unittest
import uuid

from minireason.reason import r002
from minireason.reason.config import R002_DIR
from minireason.reason.storage import read
from minireason.reason.types import ReasonFailure
from tests.reason import artifact_root


class R002DecomposedTests(unittest.TestCase):
    def setUp(self):
        self.out = artifact_root() / "decomposed" / uuid.uuid4().hex[:8]
        self.problem = read(R002_DIR / "problems/C01.txt")
        relations = json.loads(read(R002_DIR / "problems/RELATIONS.json"))
        forks = json.loads(read(R002_DIR / "problems/FORKS.json"))
        self.relation = next(item for item in relations["candidates"] if item["candidate_id"] == "C01")
        self.fork = next(item for item in forks["candidates"] if item["candidate_id"] == "C01")
        self.contracts = r002.ContractSet(R002_DIR / "contracts")

    def new_run(self, name="run", recipe="r002-decomposed-v1.json"):
        return r002.create_r002_run(
            self.problem, R002_DIR / "recipes" / recipe, self.out / name,
            mode="offline", problem_id="C01",
            relation_registry=R002_DIR / "problems/RELATIONS.json",
            fork_registry=R002_DIR / "problems/FORKS.json",
            coding_manifest=R002_DIR / "problems/RECODING_MAPS.json")

    @staticmethod
    def plan(length=3):
        return [{"step": number, "goal": f"derive component {number}",
                 "depends_on": [] if number == 1 else [number - 1]}
                for number in range(1, length + 1)]

    @staticmethod
    def step(number):
        return {"step": number, "derivation": f"public derivation for step {number}",
                "result": f"result-{number}", "cannot_decide": None}

    @staticmethod
    def answer():
        first = "C01.posterior_C = 1/2."
        second = "C01.next_red = 2/3."
        return {"decision": "answered", "answer": first + " " + second,
                "missing_derivation": "",
                "claims": [{"relation_id": "C01.posterior_C", "value": "1/2", "quote": first},
                           {"relation_id": "C01.next_red", "value": "2/3", "quote": second}],
                "derivation_steps": [{"step_index": 1, "statement": first, "depends_on": []},
                                     {"step_index": 2, "statement": second, "depends_on": [1]}]}

    def scripted(self, plan_length=3):
        calls = []

        def reply(role, cycle, objections, coordinate, context):
            calls.append((coordinate["call_id"], role, context))
            if role == "initial_decompose":
                first = self.step(1)
                first.pop("cannot_decide")
                return {"plan": self.plan(plan_length), "first_step": first, "cannot_decide": None}
            if role == "decomposed_step":
                return self.step(context["expected_step"]["step"])
            if role == "decomposed_critic":
                current = context["answer"]["derivation_steps"][0]
                return {"decision": "answered", "missing_derivation": "", "working": "checked",
                        "objections": [{"target_claim": f"step-{current['step_index']}",
                            "text": "Check the current finite derivation.",
                            "defeats": f"step-{current['step_index']}",
                            "check": {"check_id": coordinate["call_id"] + "-check", "kind": "derivation_step",
                                "inputs": [{"name": "step", "value": current["step_index"], "source": "plan"}],
                                "procedure": "Redo the displayed finite derivation.",
                                "claimed_result": "different", "falsifies_when": "The redo reproduces the result."},
                            "fork": {"step_index": current["step_index"], "step_quote": current["statement"],
                                "branch_point_id": "C01-fork", "earliest_reason": "This is the current step."}}]}
            if role == "decomposed_return":
                before = context["before"]
                return {"decision": "answered", "missing_derivation": "", "step": before["step"],
                        "derivation": before["derivation"], "result": before["result"],
                        "dispositions": [{"id": item["id"], "status": "rejected-with-reason",
                            "reason": "The independent redo reproduces the current result.",
                            "redo": {"check_id": item["check"]["check_id"], "status": "redone",
                                "method": "Redid the displayed finite derivation.", "result": before["result"],
                                "comparison": "opposes_objection"}} for item in objections]}
            if role == "decomposed_use":
                step = context["expected_step"]["step"]
                return {"decision": "answered", "missing_derivation": "", "step": step,
                        "status": "agrees", "method": "Recomputed from the problem and accepted dependencies.",
                        "result": f"result-{step}"}
            if role == "decomposed_synthesis":
                return self.answer()
            raise AssertionError(role)

        return reply, calls

    def test_three_steps_complete_and_synthesize_in_thirteen_calls(self):
        run = self.new_run()
        scripted, calls = self.scripted()
        state = r002.execute_r002(run, scripted=scripted)
        self.assertEqual(state["stop_reason"], "complete", state.get("stop_detail"))
        self.assertEqual((state["calls"], state["attempts"], state["completed_cycles"]), (13, 13, 3))
        self.assertEqual([item["step"] for item in state["accepted_steps"]], [1, 2, 3])
        self.assertEqual([call_id for call_id, _role, _context in calls], [
            "initial", "c0001-critic", "c0001-return", "c0001-use",
            "c0002-step", "c0002-critic", "c0002-return", "c0002-use",
            "c0003-step", "c0003-critic", "c0003-return", "c0003-use", "synthesis"])
        critic_endpoints = [json.loads((run / "calls" / call_id / "a00/request.json").read_text(encoding="utf-8"))["seat"]["endpoint"]
                            for call_id in ("c0001-critic", "c0002-critic", "c0003-critic")]
        self.assertEqual(critic_endpoints, ["ollama/qwen3.5-397b.native", "ollama/glm-5.3.native",
                                            "ollama/qwen3.5-397b.native"])
        settings = [json.loads(path.read_text(encoding="utf-8"))["prepared"]["thinking"]
                    for path in sorted((run / "calls").glob("*/a00/request.json"))]
        self.assertEqual(settings.count("native"), 5)
        self.assertEqual(settings.count("off"), 8)
        self.assertEqual(len(list((run / "episodes").glob("*/*.json"))), 6)
        self.assertEqual(len(list((run / "steps").glob("step-*/*.json"))), 6)
        for folder in (run / "episodes").iterdir():
            self.assertRegex(folder.name, r"^c\d{4}-critic-o\d{3}$")
            base = json.loads(next(path for path in folder.glob("*.json")
                                   if not path.name.endswith("-use.json")).read_text(encoding="utf-8"))
            supplement = json.loads(next(folder.glob("*-use.json")).read_text(encoding="utf-8"))
            self.assertNotIn("use_request", base)
            self.assertIsNotNone(supplement["use_request"])
            self.assertIsNotNone(supplement["use_response"])
            self.assertRegex(supplement["disposition_record"]["sha256"], r"^[0-9a-f]{64}$")

    def test_empty_critics_create_step_custody_but_zero_episode_records(self):
        run = self.new_run("empty-critics")
        normal, _calls = self.scripted()

        def empty(**context):
            if context["role"] == "decomposed_critic":
                return {"decision": "answered", "missing_derivation": "",
                        "working": "checked", "objections": []}
            return normal(**context)

        state = r002.execute_r002(run, scripted=empty)
        self.assertEqual((state["stop_reason"], state["episode_records"]), ("complete", 0))
        self.assertFalse((run / "episodes").exists())
        self.assertEqual(len(list((run / "steps").glob("step-*/*.json"))), 6)

    def test_four_step_plan_stops_at_budget_without_synthesis(self):
        run = self.new_run("budget")
        scripted, calls = self.scripted(plan_length=4)
        state = r002.execute_r002(run, scripted=scripted)
        self.assertEqual(state["stop_reason"], "step_budget")
        self.assertEqual((state["calls"], state["completed_cycles"]), (12, 3))
        self.assertFalse((run / "calls/synthesis").exists())
        self.assertNotIn("synthesis", [call_id for call_id, _role, _context in calls])

    def test_initial_ceiling_is_preserved_before_any_cycle(self):
        run = self.new_run("ceiling")
        ceiling = {"content": "", "finish_reason": "length",
                   "usage": {"prompt_tokens": 10, "completion_tokens": 32768, "total_tokens": 32778}}
        state = r002.execute_r002(run, scripted=lambda **_context: ceiling)
        self.assertEqual(state["stop_reason"], "CEILING_HIT")
        self.assertEqual((state["calls"], state["completed_cycles"]), (1, 0))
        self.assertFalse((run / "calls/c0001-critic").exists())

    def test_later_step_ceiling_preserves_the_prior_accepted_step(self):
        run = self.new_run("step-ceiling")
        normal, _calls = self.scripted()
        ceiling = {"content": "", "finish_reason": "length",
                   "usage": {"prompt_tokens": 10, "completion_tokens": 16384, "total_tokens": 16394}}

        def stop_at_step_two(**context):
            if context["role"] == "decomposed_step" and context["cycle"] == 2:
                return ceiling
            return normal(**context)

        state = r002.execute_r002(run, scripted=stop_at_step_two)
        self.assertEqual((state["stop_reason"], state["calls"], state["completed_cycles"]),
                         ("CEILING_HIT", 5, 1))
        self.assertEqual([item["step"] for item in state["accepted_steps"]], [1])
        self.assertFalse((run / "calls/c0002-critic").exists())
        self.assertIn("Accepted partial steps", (run / "ANSWER.md").read_text(encoding="utf-8"))

    def test_existing_tested_arm_initial_ceiling_still_stops_one_call_before_cycles(self):
        run = r002.create_r002_run(
            self.problem, R002_DIR / "recipes/r002-tested-cross-v1.json", self.out / "tested-ceiling",
            mode="offline", problem_id="C01",
            relation_registry=R002_DIR / "problems/RELATIONS.json",
            fork_registry=R002_DIR / "problems/FORKS.json",
            coding_manifest=R002_DIR / "problems/RECODING_MAPS.json")
        ceiling = {"content": "", "finish_reason": "length",
                   "usage": {"prompt_tokens": 10, "completion_tokens": 32768, "total_tokens": 32778}}
        state = r002.execute_r002(run, scripted=lambda **_context: ceiling)
        self.assertEqual((state["stop_reason"], state["calls"], state["completed_cycles"]),
                         ("CEILING_HIT", 1, 0))

    def test_critic_ceiling_preserves_partial_step_episode_and_hash_locators(self):
        run = self.new_run("critic-ceiling")
        normal, _calls = self.scripted()
        ceiling = {"content": "", "finish_reason": "length",
                   "usage": {"prompt_tokens": 10, "completion_tokens": 16384, "total_tokens": 16394}}

        def stop_at_critic(**context):
            return ceiling if context["role"] == "decomposed_critic" else normal(**context)

        state = r002.execute_r002(run, scripted=stop_at_critic)
        self.assertEqual((state["stop_reason"], state["calls"]), ("CEILING_HIT", 2))
        records = list((run / "steps/step-0001").glob("*.json"))
        self.assertEqual(len(records), 1)
        record = json.loads(records[0].read_text(encoding="utf-8"))
        self.assertEqual(record["status"], "incomplete")
        self.assertIsNotNone(record["step_request"])
        self.assertIsNotNone(record["step_response"])
        self.assertIsNotNone(record["critic_request"])
        self.assertIsNotNone(record["critic_response"])
        for key in ("step_request", "step_response", "critic_request", "critic_response"):
            self.assertRegex(record[key]["sha256"], r"^[0-9a-f]{64}$")
        self.assertFalse((run / "episodes").exists())

    def test_explicit_initial_cannot_decide_is_preserved_without_cycle_calls(self):
        run = self.new_run("cannot")
        response = {"plan": [], "first_step": None,
                    "cannot_decide": {"missing": "A bounded first derivation is missing."}}
        state = r002.execute_r002(run, scripted=lambda **_context: response)
        self.assertEqual(state["stop_reason"], "initial_cannot_decide")
        self.assertEqual((state["calls"], state["completed_cycles"],
                          state["cannot_decide_responses"]), (1, 0, 1))
        self.assertFalse((run / "calls/c0001-critic").exists())

    def test_use_disagreement_stops_partial_without_synthesis(self):
        run = self.new_run("disagree")
        normal, _calls = self.scripted()

        def disagree(**context):
            result = normal(**context)
            if context["role"] == "decomposed_use" and context["cycle"] == 2:
                result.update(status="disagrees", result="counter-result")
            return result

        state = r002.execute_r002(run, scripted=disagree)
        self.assertEqual(state["stop_reason"], "step_unresolved")
        self.assertEqual((state["calls"], state["completed_cycles"]), (8, 1))
        self.assertEqual([item["step"] for item in state["accepted_steps"]], [1])
        self.assertFalse((run / "calls/synthesis").exists())
        self.assertIn("Accepted partial steps", (run / "ANSWER.md").read_text(encoding="utf-8"))

    def test_contracts_reject_malformed_plan_wrong_step_and_missing_dependency(self):
        malformed = {"plan": [{"step": 1, "goal": "first", "depends_on": []},
                              {"step": 3, "goal": "third", "depends_on": [1]}],
                     "first_step": {"step": 1, "derivation": "d", "result": "r"},
                     "cannot_decide": None}
        with self.assertRaises(ReasonFailure):
            r002.parse_r002("initial_decompose", json.dumps(malformed), self.contracts,
                            relation=self.relation)
        with self.assertRaises(ReasonFailure):
            r002.parse_r002("decomposed_step", json.dumps(self.step(3)), self.contracts,
                            relation=self.relation,
                            expected_step={"step": 2, "goal": "second", "depends_on": [1]},
                            accepted_steps=[{"step": 1}])
        with self.assertRaises(ReasonFailure):
            r002.parse_r002("decomposed_step", json.dumps(self.step(2)), self.contracts,
                            relation=self.relation,
                            expected_step={"step": 2, "goal": "second", "depends_on": [1]},
                            accepted_steps=[])

    def test_contract_bounds_reject_nine_steps_long_derivation_and_bad_dependencies(self):
        nine = self.plan(9)
        nine[8]["step"] = 8
        initial = {"plan": nine,
                   "first_step": {"step": 1, "derivation": "d", "result": "r"},
                   "cannot_decide": None}
        with self.assertRaises(ReasonFailure):
            r002.parse_r002("initial_decompose", json.dumps(initial), self.contracts,
                            relation=self.relation)

        long_first = {"plan": self.plan(1),
                      "first_step": {"step": 1, "derivation": "x" * 2001, "result": "r"},
                      "cannot_decide": None}
        with self.assertRaises(ReasonFailure):
            r002.parse_r002("initial_decompose", json.dumps(long_first), self.contracts,
                            relation=self.relation)

        for dependencies in ([1, 1], [2]):
            value = {"plan": [{"step": 1, "goal": "first", "depends_on": []},
                              {"step": 2, "goal": "second", "depends_on": dependencies}],
                     "first_step": {"step": 1, "derivation": "d", "result": "r"},
                     "cannot_decide": None}
            with self.subTest(dependencies=dependencies), self.assertRaises(ReasonFailure):
                r002.parse_r002("initial_decompose", json.dumps(value), self.contracts,
                                relation=self.relation)

    def test_return_rejects_missing_duplicate_dispositions_and_wrong_check_id(self):
        objection = {"id": "step-o1", "check": {"check_id": "step-check"}}
        disposition = {"id": "step-o1", "status": "rejected-with-reason", "reason": "redo agrees",
                       "redo": {"check_id": "step-check", "status": "redone", "method": "redo",
                                "result": "r", "comparison": "opposes_objection"}}
        base = {"decision": "answered", "missing_derivation": "", "step": 1,
                "derivation": "derived", "result": "r", "dispositions": [disposition]}
        self.assertEqual(r002.parse_r002("decomposed_return", json.dumps(base), self.contracts,
                                        relation=self.relation,
                                        before={"step": 1}, objections=[objection]), base)
        invalid = []
        missing = deepcopy(base); missing["dispositions"] = []; invalid.append(missing)
        duplicate = deepcopy(base); duplicate["dispositions"].append(deepcopy(disposition)); invalid.append(duplicate)
        wrong = deepcopy(base); wrong["dispositions"][0]["redo"]["check_id"] = "wrong"; invalid.append(wrong)
        for value in invalid:
            with self.subTest(dispositions=value["dispositions"]), self.assertRaises(ReasonFailure):
                r002.parse_r002("decomposed_return", json.dumps(value), self.contracts,
                                relation=self.relation,
                                before={"step": 1}, objections=[objection])


    def test_a2_step_two_uses_qwen_and_repairs_on_that_same_lineage(self):
        run = self.new_run("a2-step-two-seat", "r002-decomposed-v2.json")
        normal, _calls = self.scripted()

        def step_two_repair(**context):
            if context["role"] == "decomposed_critic" and context["cycle"] == 2 \
                    and context["coordinate"]["attempt"] == 0:
                return {"content": "The current step appears sound; format this as JSON."}
            return normal(**context)

        state = r002.execute_r002(run, scripted=step_two_repair)
        self.assertEqual((state["stop_reason"], state["completed_cycles"], state["attempts"]),
                         ("complete", 3, 14), state.get("stop_detail"))
        for attempt in ("a00", "a01"):
            folder = run / "calls/c0002-critic" / attempt
            request = json.loads((folder / "request.json").read_text(encoding="utf-8"))
            wire = json.loads(request["prepared"]["wire_body_text"])
            self.assertEqual(request["seat"]["endpoint"], "ollama/qwen3.5-397b.native")
            self.assertEqual(wire["model"], "qwen3.5:397b")
            self.assertIs(wire["think"], False)
            self.assertEqual(wire["format"], "json")
            self.assertEqual(wire["options"]["num_predict"], 32768)
        legacy = json.loads((R002_DIR / "recipes/r002-decomposed-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(legacy["seats"]["critic_cycle_2"]["endpoint"], "ollama/glm-5.3.native")

    def test_a2_prose_critic_repairs_once_with_same_seat_ceiling_and_contract(self):
        run = self.new_run("a2-repair", "r002-decomposed-v2.json")
        normal, _calls = self.scripted()
        prose = "Let me analyze the current step carefully. The displayed finite derivation appears sound."

        def repair_once(**context):
            if context["role"] == "decomposed_critic" and context["cycle"] == 1 \
                    and context["coordinate"]["attempt"] == 0:
                return {"content": prose}
            return normal(**context)

        state = r002.execute_r002(run, scripted=repair_once)
        self.assertEqual((state["stop_reason"], state["calls"], state["attempts"]),
                         ("complete", 13, 14), state.get("stop_detail"))
        first = json.loads((run / "calls/c0001-critic/a00/request.json").read_text(encoding="utf-8"))
        repair = json.loads((run / "calls/c0001-critic/a01/request.json").read_text(encoding="utf-8"))
        self.assertFalse(first["schema_repair"])
        self.assertTrue(repair["schema_repair"])
        self.assertEqual(first["seat"], repair["seat"])
        self.assertEqual(first["prepared"]["kwargs"]["max_tokens"], 32768)
        self.assertEqual(repair["prepared"]["kwargs"]["max_tokens"], 32768)
        self.assertEqual(first["prepared"]["payload"]["format"], "json")
        self.assertEqual(repair["prepared"]["payload"]["format"], "json")
        self.assertEqual(len(repair["prepared"]["messages"]), 2)
        repair_text = repair["prepared"]["messages"][1]["content"]
        self.assertIn(prose, repair_text)
        self.assertIn("RESPONSE SCHEMA tested-objection.schema.json", repair_text)
        self.assertIn("Repair only its JSON structure", repair_text)
        step_record = json.loads((run / "steps/step-0001/record.json").read_text(encoding="utf-8"))
        self.assertEqual(step_record["critic_request"]["path"], "calls/c0001-critic/a01/request.json")
        self.assertEqual(step_record["critic_response"]["path"], "calls/c0001-critic/a01/response.json")
        run_text = (run / "RUN.md").read_text(encoding="utf-8")
        self.assertIn("Calls/attempts: 13/14. Schema repairs: 1.", run_text)
        self.assertIn("Base/max completion allowance: 344064/688128.", run_text)
        self.assertIn('Reached by repair: `["c0001-critic"]`.', run_text)
        self.assertIn('Reached without repair:', run_text)

    def test_a2_second_schema_failure_stops_without_a02(self):
        run = self.new_run("a2-second-failure", "r002-decomposed-v2.json")
        normal, _calls = self.scripted()

        def invalid_twice(**context):
            if context["role"] == "decomposed_critic":
                return {"content": "Let me analyze this before giving JSON."}
            return normal(**context)

        state = r002.execute_r002(run, scripted=invalid_twice)
        self.assertEqual((state["stop_reason"], state["calls"], state["attempts"]),
                         ("SCHEMA_FAILURE", 2, 3))
        self.assertTrue((run / "calls/c0001-critic/a00/response.json").is_file())
        self.assertTrue((run / "calls/c0001-critic/a01/response.json").is_file())
        self.assertFalse((run / "calls/c0001-critic/a02").exists())
        run_text = (run / "RUN.md").read_text(encoding="utf-8")
        self.assertIn("Reached by repair: `[]`.", run_text)
        self.assertIn('Repair attempted but not completed: `["c0001-critic"]`.', run_text)

    def test_a2_ceiling_hit_never_repairs_and_critic_uses_32768(self):
        run = self.new_run("a2-ceiling", "r002-decomposed-v2.json")
        normal, _calls = self.scripted()
        ceiling = {"content": "", "finish_reason": "length",
                   "usage": {"prompt_tokens": 10, "completion_tokens": 32768,
                             "total_tokens": 32778}}

        def critic_ceiling(**context):
            return ceiling if context["role"] == "decomposed_critic" else normal(**context)

        state = r002.execute_r002(run, scripted=critic_ceiling)
        self.assertEqual((state["stop_reason"], state["calls"], state["attempts"]),
                         ("CEILING_HIT", 2, 2))
        request = json.loads((run / "calls/c0001-critic/a00/request.json").read_text(encoding="utf-8"))
        self.assertEqual(request["prepared"]["kwargs"]["max_tokens"], 32768)
        self.assertFalse((run / "calls/c0001-critic/a01").exists())

    def test_a2_oversize_full_output_stops_preflight_without_repair_intent_or_truncation(self):
        run = self.new_run("a2-oversize", "r002-decomposed-v2.json")
        normal, _calls = self.scripted()
        prose = "P" * 40000

        def oversize(**context):
            if context["role"] == "decomposed_critic":
                return {"content": prose}
            return normal(**context)

        state = r002.execute_r002(run, scripted=oversize)
        self.assertEqual(state["stop_reason"], "PROMPT_TOKEN_CAP")
        self.assertFalse((run / "calls/c0001-critic/a01").exists())
        first = json.loads((run / "calls/c0001-critic/a00/response.json").read_text(encoding="utf-8"))
        self.assertEqual(first["result"]["content"], prose)

    def test_a2_interrupted_after_repair_resumes_without_resending_either_attempt(self):
        run = self.new_run("a2-resume", "r002-decomposed-v2.json")
        normal, _calls = self.scripted()
        prose = "Let me analyze before formatting the answer."

        def repair_once(**context):
            if context["role"] == "decomposed_critic" and context["cycle"] == 1 \
                    and context["coordinate"]["attempt"] == 0:
                return {"content": prose}
            return normal(**context)

        class Interrupted(BaseException):
            pass

        def interrupt_after_repair(call_id, _saved):
            if call_id == "c0001-critic" and (run / "calls/c0001-critic/a01/response.json").is_file():
                raise Interrupted()

        with self.assertRaises(Interrupted):
            r002.execute_r002(run, scripted=repair_once, after_call=interrupt_after_repair)
        first_bytes = (run / "calls/c0001-critic/a00/response.json").read_bytes()
        repair_bytes = (run / "calls/c0001-critic/a01/response.json").read_bytes()
        resumed_calls = []

        def resume(**context):
            resumed_calls.append((context["coordinate"]["call_id"], context["coordinate"]["attempt"]))
            return normal(**context)

        state = r002.execute_r002(run, scripted=resume)
        self.assertEqual(state["stop_reason"], "complete")
        self.assertNotIn(("c0001-critic", 0), resumed_calls)
        self.assertNotIn(("c0001-critic", 1), resumed_calls)
        self.assertEqual((run / "calls/c0001-critic/a00/response.json").read_bytes(), first_bytes)
        self.assertEqual((run / "calls/c0001-critic/a01/response.json").read_bytes(), repair_bytes)


if __name__ == "__main__":
    unittest.main()
