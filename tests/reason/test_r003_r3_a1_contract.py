"""R3-A1 open-problem decomposition contract and repair regressions."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from minireason.reason import prompts, r002
from minireason.reason.types import ReasonFailure


ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "experiments/diagnostics/R003-open-problems-trial-series"


def commitment(number: int) -> dict:
    return {
        "kind": "relation",
        "claim": f"fixture relation {number} holds",
        "check_or_counterexample": f"a fixture case where relation {number} fails",
    }


def step(number: int, *, size: int = 40) -> dict:
    claim = commitment(number)
    return {
        "step": number,
        "derivation": "D" * size,
        "result": f"provisional result {number}\nCOMMITMENT: {claim['claim']}",
        "commitments": [claim],
        "cannot_decide": None,
    }


class R3A1Fixture:
    def __init__(self, *, bad_first_locator: bool = False):
        self.bad_first_locator = bad_first_locator

    @staticmethod
    def answer(decisive_step=3, decisive_claim=None):
        decisive_claim = decisive_claim or commitment(decisive_step)["claim"]
        text = "OFFLINE FIXTURE answer containing " + decisive_claim
        return {
            "decision": "answered", "answer": text, "missing_derivation": "",
            "claims": [{"relation_id": "working_position", "value": text, "quote": text}],
            "derivation_steps": [{"step_index": 1, "statement": text, "depends_on": []}],
            "decisive_step": decisive_step, "decisive_claim": decisive_claim,
        }

    def __call__(self, *, role, cycle, objections, coordinate, context):
        if role == "initial_decompose":
            first = step(1)
            first.pop("cannot_decide")
            return {
                "plan": [
                    {"step": 1, "goal": "Make a first testable relation", "depends_on": []},
                    {"step": 2, "goal": "Check a second relation", "depends_on": [1]},
                    {"step": 3, "goal": "State the decisive relation", "depends_on": [1, 2]},
                ],
                "decisive_step": 3, "first_step": first, "cannot_decide": None,
            }
        if role == "decomposed_step":
            return step(context["expected_step"]["step"])
        if role == "decomposed_critic":
            current = context["answer"]["derivation_steps"][0]
            if self.bad_first_locator and cycle == 1 and coordinate["attempt"] == 0:
                quote = "paraphrase instead of the exact current step"
            else:
                quote = current["statement"]
            item = {
                "target_claim": "working_position", "text": "A fixture rival may contradict the relation.",
                "defeats": "the current relation",
                "fork": {"step_index": current["step_index"], "step_quote": quote,
                         "branch_point_id": f"fixture-branch-{current['step_index']}",
                         "earliest_reason": "The current participant step first states the relation."},
                "check": {"check_id": f"fixture-check-{cycle}", "kind": "derivation_step",
                          "inputs": [{"name": "step", "value": current["statement"],
                                      "source": "CURRENT STEP"}],
                          "procedure": "Compare one stated counterexample with the relation.",
                          "claimed_result": "The counterexample is excluded.",
                          "falsifies_when": "The counterexample satisfies the relation."},
            }
            return {"decision": "answered", "missing_derivation": "", "working": "fixture", "objections": [item]}
        if role == "decomposed_return":
            before = context["before"]
            return {
                "decision": "answered", "missing_derivation": "", "step": before["step"],
                "derivation": before["derivation"], "result": before["result"],
                "commitments": before["commitments"],
                "dispositions": [{
                    "id": item["id"], "status": "rejected-with-reason",
                    "reason": "The fixture counterexample is outside the stated relation.",
                    "redo": {"check_id": item["check"]["check_id"], "status": "redone",
                             "method": "Compared the fixture counterexample with the relation.",
                             "result": "outside", "comparison": "opposes_objection"},
                } for item in objections],
            }
        if role == "decomposed_use":
            returned = context["answer"]
            return {"decision": "answered", "missing_derivation": "",
                    "step": context["expected_step"]["step"], "status": "agrees",
                    "method": "Applied the stated relation to the fixture case.",
                    "result": returned["result"]}
        if role == "decomposed_synthesis":
            return self.answer()
        if role == "decomposed_closing":
            answer = self.answer()
            answer["dispositions"] = []
            return answer
        raise AssertionError(role)


class R3A1ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture_root = Path(os.environ.get("TMP", "C:/tw30"))
        fixture_root.mkdir(parents=True, exist_ok=True)
        cls._contracts_temp = tempfile.TemporaryDirectory(dir=fixture_root)
        merged = Path(cls._contracts_temp.name)
        for directory in (ROOT / "experiments/diagnostics/R002-episodes-under-calibrated-difficulty/contracts",
                          STUDY / "contracts"):
            for source in directory.glob("*.schema.json"):
                with source.open("r", encoding="utf-8", newline="") as reader:
                    text = reader.read()
                with (merged / source.name).open("w", encoding="utf-8", newline="") as writer:
                    writer.write(text)
        cls.contracts = r002.ContractSet(merged)
        cls.relation = {"relations": [{"relation_id": "working_position"}]}

    @classmethod
    def tearDownClass(cls):
        cls._contracts_temp.cleanup()

    def test_long_open_prose_passes_only_versioned_contract(self):
        value = {
            "plan": [{"step": 1, "goal": "Reach a testable relation", "depends_on": []}],
            "decisive_step": 1, "first_step": step(1, size=60000), "cannot_decide": None,
        }
        value["first_step"].pop("cannot_decide")
        parsed = r002.parse_r002(
            "initial_decompose", json.dumps(value), self.contracts, relation=self.relation,
            study_profile="r003-open-v1", contract_version=prompts.R003_A1_CONTRACT)
        self.assertEqual(len(parsed["first_step"]["derivation"]), 60000)

        legacy = {"plan": value["plan"], "first_step": {
            key: value["first_step"][key] for key in ("step", "derivation", "result")},
            "cannot_decide": None}
        with self.assertRaises(ReasonFailure):
            r002.parse_r002("initial_decompose", json.dumps(legacy), self.contracts,
                            relation=self.relation, study_profile="r003-open-v1")

    def test_commitment_and_decisive_step_fail_closed_mechanically(self):
        base = {
            "plan": [{"step": 1, "goal": "Reach a testable relation", "depends_on": []}],
            "decisive_step": 1, "first_step": step(1), "cannot_decide": None,
        }
        base["first_step"].pop("cannot_decide")
        for mutate in (
            lambda value: value["first_step"].update(commitments=[]),
            lambda value: value["first_step"].update(result="restatement only"),
            lambda value: value.update(decisive_step=2),
            lambda value: value.update(plan=value["plan"] + [
                {"step": 2, "goal": "two", "depends_on": [1]},
                {"step": 3, "goal": "three", "depends_on": [2]},
                {"step": 4, "goal": "four", "depends_on": [3]}]),
        ):
            value = json.loads(json.dumps(base))
            mutate(value)
            with self.assertRaises(ReasonFailure):
                r002.parse_r002(
                    "initial_decompose", json.dumps(value), self.contracts,
                    relation=self.relation, study_profile="r003-open-v1",
                    contract_version=prompts.R003_A1_CONTRACT)

        # Shape validation records the participant's stated refutability; it does not decide its merit.
        shaped = json.loads(json.dumps(base))
        shaped["first_step"]["commitments"][0].update(
            claim="A participant labels this relation refutable",
            check_or_counterexample="A participant-proposed counterexample")
        shaped["first_step"]["result"] = (
            "definition-like prose\nCOMMITMENT: A participant labels this relation refutable")
        self.assertEqual(r002.parse_r002(
            "initial_decompose", json.dumps(shaped), self.contracts, relation=self.relation,
            study_profile="r003-open-v1", contract_version=prompts.R003_A1_CONTRACT
        )["decisive_step"], 1)

    def test_definition_only_initial_step_is_not_accepted_or_counted(self):
        def definition_only(*, role, cycle, objections, coordinate, context):
            self.assertEqual(role, "initial_decompose")
            return {
                "plan": [{"step": 1, "goal": "Define the requested terms", "depends_on": []}],
                "decisive_step": 1,
                "first_step": {
                    "step": 1,
                    "derivation": "A widget is defined as an object satisfying the widget definition.",
                    "result": "This step only records that definition.",
                    "commitments": [],
                },
                "cannot_decide": None,
            }

        fixture_root = Path(os.environ.get("TMP", "C:/tr30"))
        fixture_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=fixture_root) as raw:
            base = Path(raw)
            problem = (STUDY / "problems/O01.txt").read_text(encoding="utf-8")
            copied = base / "p/O01.txt"
            copied.parent.mkdir(parents=True)
            with copied.open("w", encoding="utf-8", newline="") as handle:
                handle.write(problem)
            canonical = base / "canonical.json"
            registry = {"schema_version": "minireason.reason.r003-canonical-registry.v1",
                        "study_profile": "r003-open-v1", "candidates": [{
                            "candidate_id": "O01", "canonical_problem": "p/O01.txt",
                            "problem_sha256": hashlib.sha256(copied.read_bytes()).hexdigest()}]}
            with canonical.open("w", encoding="utf-8", newline="") as handle:
                json.dump(registry, handle, ensure_ascii=False)
                handle.write("\n")
            run = r002.create_r002_run(
                problem, STUDY / "recipes/r003-decomposed-v2.json", base / "run",
                mode="offline", problem_id="O01", study_profile="r003-open-v1",
                relation_registry=STUDY / "public/RELATIONS.json",
                fork_registry=STUDY / "public/FORKS.json", canonical_registry=canonical)
            state = r002.execute_r002(run, scripted=definition_only)

            self.assertEqual(state["stop_reason"], "SCHEMA_FAILURE", state)
            self.assertEqual(state["completed_cycles"], 0, state)
            self.assertEqual(state.get("accepted_steps", []), [], state)
            self.assertFalse(any(item.get("event") == "decomposed_step_accepted"
                                 for item in state.get("events", [])), state)
            self.assertTrue((run / "calls/initial/a00/response.json").is_file())
            self.assertTrue((run / "calls/initial/a01/response.json").is_file())
            self.assertFalse((run / "calls/initial/a02").exists())

    def test_definition_only_later_step_does_not_increment_accepted_budget(self):
        class LaterDefinitionOnly(R3A1Fixture):
            def __call__(self, *, role, cycle, objections, coordinate, context):
                if role == "decomposed_step":
                    return {
                        "step": context["expected_step"]["step"],
                        "derivation": "A widget is defined as an object satisfying the widget definition.",
                        "result": "This step only records that definition.",
                        "commitments": [],
                        "cannot_decide": None,
                    }
                return super().__call__(role=role, cycle=cycle, objections=objections,
                                        coordinate=coordinate, context=context)

        fixture_root = Path(os.environ.get("TMP", "C:/tr30"))
        fixture_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=fixture_root) as raw:
            base = Path(raw)
            problem = (STUDY / "problems/O01.txt").read_text(encoding="utf-8")
            copied = base / "p/O01.txt"
            copied.parent.mkdir(parents=True)
            with copied.open("w", encoding="utf-8", newline="") as handle:
                handle.write(problem)
            canonical = base / "canonical.json"
            registry = {"schema_version": "minireason.reason.r003-canonical-registry.v1",
                        "study_profile": "r003-open-v1", "candidates": [{
                            "candidate_id": "O01", "canonical_problem": "p/O01.txt",
                            "problem_sha256": hashlib.sha256(copied.read_bytes()).hexdigest()}]}
            with canonical.open("w", encoding="utf-8", newline="") as handle:
                json.dump(registry, handle, ensure_ascii=False)
                handle.write("\n")
            run = r002.create_r002_run(
                problem, STUDY / "recipes/r003-decomposed-v2.json", base / "run",
                mode="offline", problem_id="O01", study_profile="r003-open-v1",
                relation_registry=STUDY / "public/RELATIONS.json",
                fork_registry=STUDY / "public/FORKS.json", canonical_registry=canonical)
            state = r002.execute_r002(run, scripted=LaterDefinitionOnly())

            self.assertEqual(state["stop_reason"], "SCHEMA_FAILURE", state)
            self.assertEqual(state["completed_cycles"], 1, state)
            self.assertEqual([item["step"] for item in state["accepted_steps"]], [1], state)
            accepted_events = [item for item in state.get("events", [])
                               if item.get("event") == "decomposed_step_accepted"]
            self.assertEqual([item["step"] for item in accepted_events], [1], state)
            self.assertTrue((run / "calls/c0002-step/a00/response.json").is_file())
            self.assertTrue((run / "calls/c0002-step/a01/response.json").is_file())
            self.assertFalse((run / "calls/c0002-step/a02").exists())
            self.assertFalse((run / "calls/c0002-critic").exists())

    def test_over_budget_plan_is_repaired_once_then_refused_before_acceptance(self):
        class FourStepPlan(R3A1Fixture):
            def __call__(self, *, role, cycle, objections, coordinate, context):
                if role == "initial_decompose":
                    first = step(1)
                    first.pop("cannot_decide")
                    return {
                        "plan": [
                            {"step": 1, "goal": "one", "depends_on": []},
                            {"step": 2, "goal": "two", "depends_on": [1]},
                            {"step": 3, "goal": "three", "depends_on": [2]},
                            {"step": 4, "goal": "decide", "depends_on": [3]},
                        ],
                        "decisive_step": 3,
                        "first_step": first,
                        "cannot_decide": None,
                    }
                return super().__call__(role=role, cycle=cycle, objections=objections,
                                        coordinate=coordinate, context=context)

        fixture_root = Path(os.environ.get("TMP", "C:/tr30"))
        fixture_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=fixture_root) as raw:
            base = Path(raw)
            problem = (STUDY / "problems/O01.txt").read_text(encoding="utf-8")
            copied = base / "p/O01.txt"
            copied.parent.mkdir(parents=True)
            with copied.open("w", encoding="utf-8", newline="") as handle:
                handle.write(problem)
            canonical = base / "canonical.json"
            registry = {"schema_version": "minireason.reason.r003-canonical-registry.v1",
                        "study_profile": "r003-open-v1", "candidates": [{
                            "candidate_id": "O01", "canonical_problem": "p/O01.txt",
                            "problem_sha256": hashlib.sha256(copied.read_bytes()).hexdigest()}]}
            with canonical.open("w", encoding="utf-8", newline="") as handle:
                json.dump(registry, handle, ensure_ascii=False)
                handle.write("\n")
            run = r002.create_r002_run(
                problem, STUDY / "recipes/r003-decomposed-v2.json", base / "run",
                mode="offline", problem_id="O01", study_profile="r003-open-v1",
                relation_registry=STUDY / "public/RELATIONS.json",
                fork_registry=STUDY / "public/FORKS.json", canonical_registry=canonical)
            state = r002.execute_r002(run, scripted=FourStepPlan())

            self.assertEqual(state["stop_reason"], "SCHEMA_FAILURE", state)
            self.assertEqual(state["completed_cycles"], 0, state)
            self.assertEqual(state.get("accepted_steps", []), [], state)
            self.assertFalse(any(item.get("event") == "decomposed_step_accepted"
                                 for item in state.get("events", [])), state)
            self.assertTrue((run / "calls/initial/a00/response.json").is_file())
            self.assertTrue((run / "calls/initial/a01/response.json").is_file())
            self.assertFalse((run / "calls/initial/a02").exists())

    def test_synthesis_copies_accepted_decisive_commitment(self):
        accepted = [{"step": 3, "commitments": [commitment(3)]}]
        answer = R3A1Fixture.answer()
        self.assertEqual(r002.parse_r002(
            "decomposed_synthesis", json.dumps(answer), self.contracts, relation=self.relation,
            accepted_steps=accepted, decisive_step=3, study_profile="r003-open-v1",
            contract_version=prompts.R003_A1_CONTRACT)["decisive_claim"], commitment(3)["claim"])
        answer["decisive_claim"] = "invented claim"
        with self.assertRaises(ReasonFailure):
            r002.parse_r002(
                "decomposed_synthesis", json.dumps(answer), self.contracts, relation=self.relation,
                accepted_steps=accepted, decisive_step=3, study_profile="r003-open-v1",
                contract_version=prompts.R003_A1_CONTRACT)

    def test_repair_has_original_quote_context_and_legacy_bytes_stay_old_shape(self):
        original = "BEGIN CURRENT STEP\nexact participant derivation\nEND CURRENT STEP"
        repaired = r002._repair_messages(
            "decomposed_critic", self.contracts, '{"bad":"locator"}',
            "Fork locator does not quote the named derivation step exactly",
            study_profile="r003-open-v1", contract_version=prompts.R003_A1_CONTRACT,
            original_user_content=original)
        self.assertEqual([item["role"] for item in repaired], ["system", "user"])
        self.assertIn("ORIGINAL PUBLIC TASK CONTEXT", repaired[1]["content"])
        self.assertIn("exact participant derivation", repaired[1]["content"])
        self.assertIn("RECORDED SCHEMA FAILURE", repaired[1]["content"])

        legacy = r002._repair_messages(
            "decomposed_critic", self.contracts, '{"bad":"locator"}',
            "Fork locator does not quote the named derivation step exactly",
            study_profile="r003-open-v1")
        self.assertNotIn("ORIGINAL PUBLIC TASK CONTEXT", legacy[1]["content"])
        self.assertNotIn("exact participant derivation", legacy[1]["content"])

    def test_one_repair_can_recover_exact_locator_and_complete(self):
        fixture_root = Path(os.environ.get("TMP", "C:/tw30"))
        fixture_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=fixture_root) as raw:
            base = Path(raw)
            problem = (STUDY / "problems/O01.txt").read_text(encoding="utf-8")
            copied = base / "p/O01.txt"
            copied.parent.mkdir(parents=True)
            with copied.open("w", encoding="utf-8", newline="") as handle:
                handle.write(problem)
            canonical = base / "canonical.json"
            registry = {"schema_version": "minireason.reason.r003-canonical-registry.v1",
                        "study_profile": "r003-open-v1", "candidates": [{
                            "candidate_id": "O01", "canonical_problem": "p/O01.txt",
                            "problem_sha256": hashlib.sha256(copied.read_bytes()).hexdigest()}]}
            with canonical.open("w", encoding="utf-8", newline="") as handle:
                json.dump(registry, handle, ensure_ascii=False)
                handle.write("\n")
            run = r002.create_r002_run(
                problem, STUDY / "recipes/r003-decomposed-v2.json", base / "run",
                mode="offline", problem_id="O01", study_profile="r003-open-v1",
                relation_registry=STUDY / "public/RELATIONS.json",
                fork_registry=STUDY / "public/FORKS.json", canonical_registry=canonical)
            state = r002.execute_r002(run, scripted=R3A1Fixture(bad_first_locator=True))
            self.assertEqual((state["stop_reason"], state["completed_cycles"]), ("complete", 3), state)
            first = json.loads((run / "calls/c0001-critic/a00/response.json").read_text(encoding="utf-8"))
            repair = json.loads((run / "calls/c0001-critic/a01/request.json").read_text(encoding="utf-8"))
            self.assertEqual(first["status"], "SCHEMA_FAILURE")
            self.assertIn("ORIGINAL PUBLIC TASK CONTEXT", repair["prepared"]["messages"][1]["content"])
            self.assertIn(step(1)["derivation"], repair["prepared"]["messages"][1]["content"])
            self.assertFalse((run / "calls/c0001-critic/a02").exists())

    def test_direct_live_creation_rejects_nonregistered_r3_a1_descriptor_before_mkdir(self):
        fixture_root = Path(os.environ.get("TMP", "C:/tw30"))
        fixture_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=fixture_root) as raw:
            base = Path(raw)
            problem = (STUDY / "problems/O01.txt").read_text(encoding="utf-8")
            copied = base / "p/O01.txt"
            copied.parent.mkdir(parents=True)
            with copied.open("w", encoding="utf-8", newline="") as handle:
                handle.write(problem)
            canonical = base / "canonical.json"
            registry = {"schema_version": "minireason.reason.r003-canonical-registry.v1",
                        "study_profile": "r003-open-v1", "candidates": [{
                            "candidate_id": "O01", "canonical_problem": "p/O01.txt",
                            "problem_sha256": hashlib.sha256(copied.read_bytes()).hexdigest()}]}
            with canonical.open("w", encoding="utf-8", newline="") as handle:
                json.dump(registry, handle, ensure_ascii=False)
                handle.write("\n")
            out = base / "must-not-exist"
            with (patch.object(r002, "validate_capability", return_value={"fixture": True}),
                  patch.object(r002, "snapshot_tokenizers",
                               return_value={"amendment": "R3-A1", "mutated": True})):
                with self.assertRaises(ReasonFailure) as caught:
                    r002.create_r002_run(
                        problem, STUDY / "recipes/r003-decomposed-v2.json", out,
                        mode="live", problem_id="O01", study_profile="r003-open-v1",
                        relation_registry=STUDY / "public/RELATIONS.json",
                        fork_registry=STUDY / "public/FORKS.json", canonical_registry=canonical,
                        tokenizer_pins={"ignored": "by mock"}, capability={"fixture": True})
            self.assertEqual(caught.exception.code, "TOKENIZER_MISMATCH")
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
