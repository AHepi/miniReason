"""R3-A2 prose locator and commitment contract regressions; offline only."""
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
from tests.reason.test_r003_r3_a1_contract import R3A1Fixture, step


ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "experiments/diagnostics/R003-open-problems-trial-series"
R002_CONTRACTS = ROOT / "experiments/diagnostics/R002-episodes-under-calibrated-difficulty/contracts"
R003_CONTRACTS = ROOT / "experiments/diagnostics/R003-open-problems-trial-series/contracts"


class R3A2ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._temporary = tempfile.TemporaryDirectory()
        merged = Path(cls._temporary.name)
        for directory in (R002_CONTRACTS, R003_CONTRACTS):
            for source in directory.glob("*.schema.json"):
                (merged / source.name).write_bytes(source.read_bytes())
        cls.contracts = r002.ContractSet(merged)
        cls.relation = {"relations": [{"relation_id": "working_position"}]}

    @classmethod
    def tearDownClass(cls):
        cls._temporary.cleanup()

    @staticmethod
    def _answer(statement: str) -> dict:
        return {"derivation_steps": [{"step_index": 1, "statement": statement, "depends_on": []}]}

    @staticmethod
    def _critic(step_quote: str, *, step_index: int = 1, branch: str = "participant-branch") -> dict:
        return {
            "decision": "answered",
            "missing_derivation": "",
            "working": "The proposed relation has a counterexample.",
            "objections": [{
                "target_claim": "working_position",
                "text": "The stated relation fails for the named boundary case.",
                "defeats": "The step's universal relation.",
                "check": {
                    "check_id": "check-1",
                    "kind": "derivation_step",
                    "inputs": [{"name": "case", "value": "boundary", "source": "problem"}],
                    "procedure": "Apply the stated relation to the boundary case.",
                    "claimed_result": "counterexample",
                    "falsifies_when": "The relation holds for that case.",
                },
                "fork": {
                    "step_index": step_index,
                    "step_quote": step_quote,
                    "branch_point_id": branch,
                    "earliest_reason": "This is the first paragraph asserting the relation.",
                },
            }],
        }

    def _parse_critic(self, value: dict, statement: str, *, contract=prompts.R003_A2_CONTRACT,
                      prior=()):
        return r002.parse_r002(
            "decomposed_critic", json.dumps(value, ensure_ascii=False), self.contracts,
            relation=self.relation, answer=self._answer(statement), fork={"branch_point_id": "root"},
            study_profile="r003-open-v1", contract_version=contract,
            prior_objections=prior)

    def test_reflowed_whitespace_curly_quotes_and_case_pass(self):
        statement = (
            "The first paragraph says “Alpha relates to Beta” whenever the boundary condition holds, "
            "and this public relation is the commitment under review."
        )
        quote = (
            "THE FIRST PARAGRAPH SAYS \"ALPHA RELATES TO BETA\"   WHENEVER\n"
            "THE BOUNDARY CONDITION HOLDS"
        )
        parsed = self._parse_critic(self._critic(quote), statement)
        self.assertEqual(parsed["objections"][0]["fork"]["step_index"], 1)

    def test_explicit_index_with_empty_quote_passes(self):
        statement = "A real prose paragraph states a decision and the observation that would refute it."
        parsed = self._parse_critic(self._critic(""), statement)
        self.assertEqual(parsed["objections"][0]["fork"]["step_quote"], "")

    def test_fabricated_nonempty_quote_and_missing_index_fail(self):
        statement = "A real prose paragraph states a decision and the observation that would refute it."
        with self.assertRaises(ReasonFailure) as fabricated:
            self._parse_critic(
                self._critic("This fabricated quotation is long enough but does not occur in the real step."),
                statement)
        self.assertIn("candidate targeted step text", str(fabricated.exception))
        self.assertIn(statement, str(fabricated.exception))

        with self.assertRaises(ReasonFailure) as missing:
            self._parse_critic(self._critic("", step_index=2), statement)
        self.assertIn("<missing>", str(missing.exception))

    def test_wrong_step_whitespace_only_and_compatibility_equivalence_fail(self):
        first = "The first paragraph states a distinct relation with enough text for a locator test."
        second = "The second paragraph states another distinct relation with enough text for a locator test."
        answer = {"derivation_steps": [
            {"step_index": 1, "statement": first, "depends_on": []},
            {"step_index": 2, "statement": second, "depends_on": [1]},
        ]}
        with self.assertRaises(ReasonFailure):
            r002.parse_r002(
                "decomposed_critic", json.dumps(self._critic(second, step_index=1)), self.contracts,
                relation=self.relation, answer=answer, fork={"branch_point_id": "root"},
                study_profile="r003-open-v1", contract_version=prompts.R003_A2_CONTRACT)
        with self.assertRaises(ReasonFailure):
            self._parse_critic(self._critic(" \t\n  "), first)

        superscript = "The claimed relation maps x³ to a boundary witness and remains publicly refutable."
        plain = "The claimed relation maps x3 to a boundary witness and remains publicly refutable."
        with self.assertRaises(ReasonFailure):
            self._parse_critic(self._critic(plain), superscript)

    def test_a1_still_requires_the_full_exact_statement(self):
        statement = "This sufficiently long statement contains a real internal quotation for testing."
        with self.assertRaisesRegex(ReasonFailure, "exactly"):
            self._parse_critic(self._critic(statement[:45]), statement,
                               contract=prompts.R003_A1_CONTRACT)

    def test_label_consistency_uses_real_target_not_quote_format(self):
        statement = (
            "The participant states “a stable relation across cases” and identifies a concrete refuter."
        )
        prior = self._critic("THE PARTICIPANT STATES \"A STABLE RELATION ACROSS CASES\"")["objections"]
        parsed = self._parse_critic(self._critic("", branch="participant-branch"), statement, prior=prior)
        self.assertEqual(len(parsed["objections"]), 1)

    def test_repair_exposes_failed_check_and_candidate_step_text(self):
        statement = "Candidate paragraph text that the repaired locator must actually identify."
        try:
            self._parse_critic(self._critic("A fabricated quotation of more than forty characters is still false."),
                               statement)
        except ReasonFailure as failure:
            messages = r002._repair_messages(
                "decomposed_critic", self.contracts, '{"bad":"locator"}', str(failure),
                study_profile="r003-open-v1", contract_version=prompts.R003_A2_CONTRACT,
                original_user_content="BEGIN CURRENT STEP\n" + statement + "\nEND CURRENT STEP")
        else:
            self.fail("fabricated locator unexpectedly passed")
        repair = messages[1]["content"]
        self.assertIn("R3-A2 fork locator check failed", repair)
        self.assertIn("candidate targeted step text", repair)
        self.assertIn(statement, repair)
        self.assertIn("empty step_quote", repair)

    def test_duplicate_keys_remain_rejected_with_actionable_a2_message(self):
        for duplicate in (
            '{"result_depends_on_change":true,"result_depends_on_change":false}',
            '{"result_depends_on_change":true,"result_depends_on_change":true}',
        ):
            with self.assertRaises(ReasonFailure) as a2:
                r002._response_object(duplicate, contract_version=prompts.R003_A2_CONTRACT)
            self.assertIn("Duplicate JSON key: result_depends_on_change", str(a2.exception))
            self.assertIn("exactly one occurrence", str(a2.exception))

        duplicate = '{"result_depends_on_change":true,"result_depends_on_change":false}'
        with self.assertRaises(ReasonFailure) as a1:
            r002._response_object(duplicate, contract_version=prompts.R003_A1_CONTRACT)
        self.assertTrue(str(a1.exception).endswith("Duplicate JSON key: result_depends_on_change"))
        self.assertNotIn("exactly one occurrence", str(a1.exception))

    def test_relation_and_decision_commitments_pass_but_definition_only_fails(self):
        for kind in ("relation", "decision"):
            claim = f"The prose {kind} remains viable under the stated boundary."
            value = {
                "plan": [{"step": 1, "goal": "Make a refutable prose commitment", "depends_on": []}],
                "decisive_step": 1,
                "first_step": {
                    "step": 1,
                    "derivation": "Compare the proposed position with its boundary case.",
                    "result": "Public prose result.\nCOMMITMENT: " + claim,
                    "commitments": [{
                        "kind": kind,
                        "claim": claim,
                        "check_or_counterexample": "A named boundary case contradicting the claim.",
                    }],
                },
                "cannot_decide": None,
            }
            parsed = r002.parse_r002(
                "initial_decompose", json.dumps(value), self.contracts, relation=self.relation,
                study_profile="r003-open-v1", contract_version=prompts.R003_A2_CONTRACT)
            self.assertEqual(parsed["first_step"]["commitments"][0]["kind"], kind)

        definition_only = json.loads(json.dumps(value))
        definition_only["first_step"].update(
            derivation="A widget is defined as an object satisfying the widget definition.",
            result="This restates the definition.", commitments=[])
        with self.assertRaises(ReasonFailure):
            r002.parse_r002(
                "initial_decompose", json.dumps(definition_only), self.contracts,
                relation=self.relation, study_profile="r003-open-v1",
                contract_version=prompts.R003_A2_CONTRACT)

    def test_a2_prompt_names_versioned_schemas_and_current_step_scope(self):
        critic = prompts.render_r002(
            "decomposed_critic", [("CURRENT STEP", "fixture")],
            study_profile="r003-open-v1", contract_version=prompts.R003_A2_CONTRACT)[0]["content"]
        use = prompts.render_r002(
            "decomposed_use", [("RETURNED STEP", "fixture")],
            study_profile="r003-open-v1", contract_version=prompts.R003_A2_CONTRACT)[0]["content"]
        self.assertIn("tested-objection-r3-a2.schema.json", critic)
        self.assertNotIn("quote that current step derivation", critic)
        self.assertIn("later planned steps", critic)
        self.assertIn("CURRENT PLAN STEP", use)
        self.assertIn("no numeric value is required", prompts.R003_A2_SUFFIXES["initial_decompose"])

    def test_propagation_use_locator_binds_real_after_step_and_repairs_with_source(self):
        before_text = "Before position states the provisional relation."
        after_text = "After position states “the revised prose relation” with a public counterexample."
        before = {
            "decision": "answered", "answer": before_text, "missing_derivation": "",
            "claims": [{"relation_id": "working_position", "value": before_text, "quote": before_text}],
            "derivation_steps": [{"step_index": 1, "statement": before_text, "depends_on": []}],
        }
        after = {
            "decision": "answered", "answer": after_text, "missing_derivation": "",
            "claims": [{"relation_id": "working_position", "value": after_text, "quote": after_text}],
            "derivation_steps": [{"step_index": 1, "statement": after_text, "depends_on": []}],
        }
        value = {
            "decision": "answered", "missing_derivation": "", "query_id": "q-1",
            "question": "Does the boundary case refute the relation?",
            "problem_derivation": "Apply the boundary case directly.",
            "before": {"answer_quote": before_text, "derivation": "Before derivation.", "conclusion": "open"},
            "after": {"answer_quote": after_text, "derivation": "After derivation.", "conclusion": "refuted"},
            "dependency": {"relation_id": "working_position", "before_quote": before_text,
                           "after_quote": after_text, "result_depends_on_change": True,
                           "explanation": "The revised relation supplies the boundary condition."},
            "objections": self._critic(
                "AFTER POSITION STATES \"THE REVISED PROSE RELATION\" WITH A PUBLIC COUNTEREXAMPLE."
            )["objections"],
            "checker": None,
        }
        parsed = r002.parse_r002(
            "propagation_use", json.dumps(value, ensure_ascii=False), self.contracts,
            relation=self.relation, before=before, answer=after, fork={"branch_point_id": "root"},
            checker_eligible=False, study_profile="r003-open-v1",
            contract_version=prompts.R003_A2_CONTRACT)
        self.assertEqual(parsed["objections"][0]["fork"]["step_index"], 1)

        value["objections"][0]["fork"]["step_quote"] = (
            "A fabricated after-step quotation that is sufficiently long but absent."
        )
        with self.assertRaises(ReasonFailure) as failure:
            r002.parse_r002(
                "propagation_use", json.dumps(value), self.contracts, relation=self.relation,
                before=before, answer=after, fork={"branch_point_id": "root"},
                checker_eligible=False, study_profile="r003-open-v1",
                contract_version=prompts.R003_A2_CONTRACT)
        repair = r002._repair_messages(
            "propagation_use", self.contracts, json.dumps(value), str(failure.exception),
            study_profile="r003-open-v1", contract_version=prompts.R003_A2_CONTRACT,
            original_user_content="BEGIN AFTER ANSWER\n" + after_text + "\nEND AFTER ANSWER")
        self.assertIn(after_text, repair[1]["content"])
        self.assertIn("candidate targeted step text", repair[1]["content"])

    def _create_decomposed_run(self, base: Path, *, mode="offline",
                               tokenizer_pins=None, capability=None) -> Path:
        problem = (STUDY / "problems/O01.txt").read_text(encoding="utf-8")
        copied = base / "p/O01.txt"
        copied.parent.mkdir(parents=True)
        with copied.open("w", encoding="utf-8", newline="") as handle:
            handle.write(problem)
        canonical = base / "canonical.json"
        registry = {
            "schema_version": "minireason.reason.r003-canonical-registry.v1",
            "study_profile": "r003-open-v1",
            "candidates": [{
                "candidate_id": "O01", "canonical_problem": "p/O01.txt",
                "problem_sha256": hashlib.sha256(copied.read_bytes()).hexdigest(),
            }],
        }
        with canonical.open("w", encoding="utf-8", newline="") as handle:
            json.dump(registry, handle, ensure_ascii=False)
            handle.write("\n")
        return r002.create_r002_run(
            problem, STUDY / "recipes/r003-decomposed-v3.json", base / "run",
            mode=mode, problem_id="O01", study_profile="r003-open-v1",
            relation_registry=STUDY / "public/RELATIONS.json",
            fork_registry=STUDY / "public/FORKS.json", canonical_registry=canonical,
            tokenizer_pins=tokenizer_pins, capability=capability)

    def test_engine_repairs_locator_then_completes_three_steps_and_synthesis(self):
        fixture_root = Path(os.environ.get("TMP", "C:/tw32"))
        fixture_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=fixture_root) as raw:
            run = self._create_decomposed_run(Path(raw))
            state = r002.execute_r002(run, scripted=R3A1Fixture(bad_first_locator=True))
            self.assertEqual((state["stop_reason"], state["completed_cycles"]), ("complete", 3), state)
            failed = json.loads((run / "calls/c0001-critic/a00/response.json").read_text(encoding="utf-8"))
            repaired = json.loads((run / "calls/c0001-critic/a01/response.json").read_text(encoding="utf-8"))
            request = json.loads((run / "calls/c0001-critic/a01/request.json").read_text(encoding="utf-8"))
            self.assertEqual(failed["status"], "SCHEMA_FAILURE")
            self.assertEqual(repaired["status"], "COMPLETE")
            self.assertIn("candidate targeted step text", request["prepared"]["messages"][1]["content"])
            use_request = json.loads(
                (run / "calls/c0001-use/a00/request.json").read_text(encoding="utf-8"))
            first_refuter = "a fixture case where relation 1 fails"
            self.assertNotIn(first_refuter, step(1)["derivation"])
            self.assertNotIn(first_refuter, step(1)["result"])
            self.assertIn(first_refuter, use_request["prepared"]["messages"][1]["content"])
            self.assertTrue((run / "calls/synthesis/a00/response.json").is_file())

    def test_a2_use_port_adds_commitments_without_changing_a1_or_legacy_blocks(self):
        returned = step(1)
        plan_step = {"step": 1, "goal": "State a relation", "depends_on": []}
        legacy = r002._decomposed_use_blocks("problem", plan_step, returned, [])
        a1 = r002._decomposed_use_blocks(
            "problem", plan_step, returned, [], contract_version=prompts.R003_A1_CONTRACT)
        a2 = r002._decomposed_use_blocks(
            "problem", plan_step, returned, [], contract_version=prompts.R003_A2_CONTRACT)
        self.assertEqual(a1, legacy)
        self.assertNotIn("commitments", dict(legacy)["RETURNED STEP"])
        self.assertNotIn(commitment_refuter := returned["commitments"][0]["check_or_counterexample"],
                         returned["derivation"] + returned["result"])
        self.assertIn(commitment_refuter, dict(a2)["RETURNED STEP"])

    def test_engine_rejects_definition_only_before_accepting_a_step(self):
        class DefinitionOnly(R3A1Fixture):
            def __call__(self, *, role, cycle, objections, coordinate, context):
                if role == "initial_decompose":
                    first = step(1)
                    first.pop("cannot_decide")
                    first.update(
                        derivation="A widget is defined as an object satisfying the widget definition.",
                        result="This merely restates the definition.", commitments=[])
                    return {
                        "plan": [{"step": 1, "goal": "Define the terms", "depends_on": []}],
                        "decisive_step": 1, "first_step": first, "cannot_decide": None,
                    }
                return super().__call__(role=role, cycle=cycle, objections=objections,
                                        coordinate=coordinate, context=context)

        fixture_root = Path(os.environ.get("TMP", "C:/tw32"))
        fixture_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=fixture_root) as raw:
            run = self._create_decomposed_run(Path(raw))
            state = r002.execute_r002(run, scripted=DefinitionOnly())
            self.assertEqual((state["stop_reason"], state["completed_cycles"]), ("SCHEMA_FAILURE", 0), state)
            self.assertEqual(state.get("accepted_steps", []), [])
            self.assertTrue((run / "calls/initial/a01/response.json").is_file())
            self.assertFalse((run / "calls/initial/a02").exists())

    def test_direct_live_a2_creation_inherits_exact_descriptor_gate(self):
        fixture_root = Path(os.environ.get("TMP", "C:/tw32"))
        fixture_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=fixture_root) as raw:
            base = Path(raw)
            with (patch.object(r002, "validate_capability", return_value={"fixture": True}),
                  patch.object(r002, "snapshot_tokenizers",
                               return_value={"amendment": "R3-A2", "mutated": True})):
                with self.assertRaises(ReasonFailure) as caught:
                    self._create_decomposed_run(
                        base, mode="live", tokenizer_pins={"ignored": "by mock"},
                        capability={"fixture": True})
            self.assertEqual(caught.exception.code, "TOKENIZER_MISMATCH")
            self.assertIn("R3-A2 live runs", str(caught.exception))
            self.assertFalse((base / "run").exists())


if __name__ == "__main__":
    unittest.main()
