"""Judge regressions for conclusion-only edits and executable-check delivery."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
import uuid
from tests.reason import artifact_root
from tests.reason import test_r002_contracts as contract_fixtures
from tests.reason import test_r002_engagement as engagement_fixtures
from minireason.reason import engine
from minireason.reason.r002 import detect_tail_edit, construct_checker_objection, _return_blocks
from minireason.reason.config import R002_DIR


class Review20Tests(unittest.TestCase):
    def test_wholly_copied_derivation_records_changed_conclusion(self):
        fixture = contract_fixtures.R002ContractTests()
        before = fixture.answer()
        after = fixture.answer(red="3/4")
        after["derivation_steps"] = deepcopy(before["derivation_steps"])
        self.assertTrue(detect_tail_edit(before, after, {"status": "taken-up"}))
        self.assertFalse(detect_tail_edit(before, before, {"status": "taken-up"}))
        self.assertFalse(detect_tail_edit(before, after, {"status": "unresolved"}))
        after["derivation_steps"][0]["statement"] = "Recompute the early likelihood."
        self.assertFalse(detect_tail_edit(before, after, {"status": "taken-up"}))

    def test_checker_return_contains_exact_source_and_host_output(self):
        fixture = engagement_fixtures.R002EngagementTests()
        answer = fixture.answer()
        proposal = fixture.proposal(answer)
        execution = {"status": "COMPLETE", "comparison": "disagrees",
            "parsed": {"relation_id": "C01.next_red", "value": "3/4", "derivation": "host"},
            "stdout_utf8": '{"relation_id":"C01.next_red","value":"3/4","derivation":"host"}',
            "stdout_sha256": "a" * 64}
        fork = {"branch_point_id": "C01-fork"}
        objection = construct_checker_objection(execution, proposal, answer, fork)
        blocks = _return_blocks("problem", answer, [objection], {}, fork)
        delivered = json.loads(dict(blocks)["OPEN AND NEW OBJECTIONS"])[0]
        values = {item["name"]: item["value"] for item in delivered["check"]["inputs"]}
        self.assertEqual(values["source"], proposal["source"])
        self.assertEqual(values["stdout_utf8"], execution["stdout_utf8"])
        self.assertEqual(values["host_result"], execution["parsed"])

    def test_conclusion_only_edit_reaches_run_and_episode_counter(self):
        fixture = engagement_fixtures.R002EngagementTests()
        run = artifact_root() / "tail" / uuid.uuid4().hex[:8]
        engine.create_r002_run((R002_DIR / "problems/C01.txt").read_text(encoding="utf-8"),
            "r002-tested-cross-v1", run, cycles=1, problem_id="C01",
            relation_registry=R002_DIR / "problems/RELATIONS.json",
            fork_registry=R002_DIR / "problems/FORKS.json",
            coding_manifest=R002_DIR / "problems/RECODING_MAPS.json")
        def response(role, cycle, objections, coordinate, context):
            if role == "answer":
                return fixture.answer()
            if role == "tested_critic":
                obj = fixture.objection(context["answer"])
                obj["check"]["check_id"] = coordinate["call_id"] + "-check"
                return {"decision": "answered", "missing_derivation": "", "working": "probe", "objections": [obj]}
            if role == "tested_return":
                before = context["before"]
                after = fixture.answer("3/4")
                after["derivation_steps"] = deepcopy(before["derivation_steps"])
                dispositions = [{"id": obj["id"], "status": "taken-up", "reason": "Conclusion patched only.",
                    "redo": {"check_id": obj["check"]["check_id"], "status": "redone", "method": "asserted redo", "result": "3/4", "comparison": "supports_objection"},
                    "rederivation": {"from_step_index": 2, "objection_id": obj["id"], "status": "rederived", "steps": [after["derivation_steps"][1]], "missing_derivation": ""}} for obj in objections]
                return {**after, "dispositions": dispositions, "changes": []}
            if role == "propagation_use":
                return fixture.use(context["before"], context["answer"])
            raise AssertionError(role)
        state = engine.execute_r002(run, scripted=response)
        self.assertEqual(state["stop_reason"], "cycle_budget")
        self.assertEqual(state["tail_edits"], 1)
        self.assertIn("Tail edits: 1.", (run / "RUN.md").read_text(encoding="utf-8"))
        episodes = [json.loads(p.read_text(encoding="utf-8")) for p in (run / "episodes").glob("*/c0001-return.json")]
        self.assertTrue(episodes)
        self.assertTrue(all(item["tail_edit"] for item in episodes))

    def test_wording_change_cannot_invent_propagation_value_change(self):
        fixture = engagement_fixtures.R002EngagementTests()
        fixture.setUpClass()
        before = fixture.answer()
        after = deepcopy(before)
        after["answer"] = after["answer"].replace("2/3.", "2/3 exactly.")
        after["claims"][1]["quote"] = after["claims"][1]["quote"].replace("2/3.", "2/3 exactly.")
        from minireason.reason.types import ReasonFailure
        with self.assertRaisesRegex(ReasonFailure, "Unchanged evaluations"):
            fixture.parse_use(fixture.use(before, after, depends=True), before, after)
        self.assertTrue(fixture.parse_use(fixture.use(before, after, depends=False), before, after))
