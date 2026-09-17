"""Focused offline checks for the additive r003-open-v1 engine profile."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest

from minireason.reason import config, r002
from minireason.reason.r002_preflight import r003_capability_snapshot
from minireason.reason.types import ReasonFailure
from tests.reason.test_r003_occurrence import OpenFixture


ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "experiments/diagnostics/R003-open-problems-trial-series"


class BoundLocatorFixture(OpenFixture):
    def __call__(self, **context):
        result = super().__call__(**context)
        if context["role"] in {"prose_critic", "decomposed_critic"} and isinstance(result, dict):
            for objection in result.get("objections", []):
                quote = objection["fork"]["step_quote"].encode("utf-8")
                objection["fork"]["branch_point_id"] = "participant-" + hashlib.sha256(quote).hexdigest()[:12]
        return result


class R003EngineTests(unittest.TestCase):
    def setUp(self):
        fixture_root = Path(os.environ.get("TMP", "C:/tr28"))
        fixture_root.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=fixture_root)
        self.base = Path(self.temp.name)
        self.problem = (STUDY / "problems/O01.txt").read_text(encoding="utf-8")
        copied = self.base / "p/O01.txt"
        copied.parent.mkdir(parents=True)
        copied.write_text(self.problem, encoding="utf-8", newline="")
        registry = {
            "schema_version": "minireason.reason.r003-canonical-registry.v1",
            "study_profile": "r003-open-v1",
            "candidates": [{"candidate_id": "O01", "canonical_problem": "p/O01.txt",
                            "problem_sha256": hashlib.sha256(copied.read_bytes()).hexdigest()}],
        }
        self.canonical = self.base / "canonical.json"
        self.canonical.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
                                  encoding="utf-8", newline="")

    def tearDown(self):
        self.temp.cleanup()

    def new_run(self, name, recipe="r003-decomposed-v1.json"):
        return r002.create_r002_run(
            self.problem, STUDY / "recipes" / recipe, self.base / name,
            mode="offline", problem_id="O01", study_profile="r003-open-v1",
            relation_registry=STUDY / "public/RELATIONS.json",
            fork_registry=STUDY / "public/FORKS.json",
            canonical_registry=self.canonical)

    def test_decomposed_semantic_terminal_closes_after_completed_cycles(self):
        run = self.new_run("partial")
        fixture = BoundLocatorFixture(repair=False, plan_length=4)
        state = r002.execute_r002(run, scripted=fixture)
        self.assertEqual((state["stop_reason"], state["completed_cycles"], state["calls"]),
                         ("step_budget", 3, 13))
        self.assertEqual(state["closing_return"], "complete")
        self.assertTrue((run / "calls/closing-return/a00/request.json").is_file())
        self.assertEqual([item["step"] for item in state["accepted_steps"]], [1, 2, 3])

    def test_zero_cycle_and_fatal_delivery_do_not_close(self):
        zero = self.new_run("zero")
        response = {"plan": [], "first_step": None,
                    "cannot_decide": {"missing": "No bounded first step."}}
        state = r002.execute_r002(zero, scripted=lambda **_context: response)
        self.assertEqual((state["stop_reason"], state["completed_cycles"], state["calls"]),
                         ("initial_cannot_decide", 0, 1))
        self.assertFalse((zero / "calls/closing-return").exists())

        fatal = self.new_run("fatal")
        normal = BoundLocatorFixture(repair=False)
        ceiling = {"content": "", "finish_reason": "length",
                   "usage": {"prompt_tokens": 10, "completion_tokens": 16384,
                             "total_tokens": 16394}}
        def stop(**context):
            if context["role"] == "decomposed_step" and context["cycle"] == 2:
                return ceiling
            return normal(**context)
        state = r002.execute_r002(fatal, scripted=stop)
        self.assertEqual((state["stop_reason"], state["completed_cycles"]), ("CEILING_HIT", 1))
        self.assertFalse((fatal / "calls/closing-return").exists())

    def test_cross_second_schema_failure_stops_and_decomposed_repairs_same_seat(self):
        cross = self.new_run("cross", "r003-cross-v1.json")
        normal = BoundLocatorFixture(repair=False)
        def invalid_cross(**context):
            if context["role"] == "prose_critic":
                return {"content": "Complete public prose with no JSON object."}
            return normal(**context)
        state = r002.execute_r002(cross, scripted=invalid_cross)
        self.assertEqual(state["stop_reason"], "SCHEMA_FAILURE")
        self.assertTrue((cross / "calls/c0001-signal-a/a01/response.json").is_file())
        self.assertFalse((cross / "calls/c0001-signal-a/a02").exists())
        self.assertFalse((cross / "calls/closing-return").exists())

        decomposed = self.new_run("decomposed-repair")
        fixture = BoundLocatorFixture(repair=False)
        prose = "Complete prose critic to be repaired once without re-solving."
        def repair(**context):
            if (context["role"] == "decomposed_critic" and context["cycle"] == 1
                    and context["coordinate"]["attempt"] == 0):
                return {"content": prose}
            return fixture(**context)
        state = r002.execute_r002(decomposed, scripted=repair)
        self.assertEqual((state["stop_reason"], state["calls"], state["attempts"]),
                         ("complete", 14, 15))
        a0 = json.loads((decomposed / "calls/c0001-critic/a00/request.json").read_text(encoding="utf-8"))
        a1 = json.loads((decomposed / "calls/c0001-critic/a01/request.json").read_text(encoding="utf-8"))
        self.assertEqual(a0["seat"], a1["seat"])
        self.assertEqual(a0["prepared"]["kwargs"]["max_tokens"], 32768)
        self.assertEqual(a1["prepared"]["kwargs"]["max_tokens"], 32768)
        self.assertIn(prose, a1["prepared"]["messages"][1]["content"])

    def test_canonical_hash_and_working_position_type_are_fail_closed(self):
        data = json.loads(self.canonical.read_text(encoding="utf-8"))
        data["candidates"][0]["problem_sha256"] = "0" * 64
        self.canonical.write_text(json.dumps(data) + "\n", encoding="utf-8", newline="")
        with self.assertRaises(ReasonFailure) as caught:
            self.new_run("drift")
        self.assertEqual(caught.exception.code, "RUN_INTEGRITY_ERROR")

        answer = OpenFixture.answer()
        answer["claims"][0]["value"] = {"not": "prose"}
        # Supply the inherited answer schema too, as a real run's merged snapshot does.
        merged = self.base / "contracts"
        merged.mkdir()
        for source in (config.R002_DIR / "contracts").glob("*.schema.json"):
            with source.open("r", encoding="utf-8", newline="") as reader:
                text = reader.read()
            with (merged / source.name).open("w", encoding="utf-8", newline="") as writer:
                writer.write(text)
        for source in (STUDY / "contracts").glob("*.schema.json"):
            with source.open("r", encoding="utf-8", newline="") as reader:
                text = reader.read()
            with (merged / source.name).open("w", encoding="utf-8", newline="") as writer:
                writer.write(text)
        contracts = r002.ContractSet(merged)
        with self.assertRaises(ReasonFailure) as caught:
            r002.parse_r002("answer", json.dumps(answer), contracts,
                            relation={"relations": [{"relation_id": "working_position"}]},
                            study_profile="r003-open-v1")
        self.assertEqual(caught.exception.code, "SCHEMA_FAILURE")

    def test_capability_contains_exact_profile_pins(self):
        snapshot = r003_capability_snapshot()
        self.assertEqual(snapshot["capability"], "r003-open-v1")
        self.assertEqual(snapshot["recipe_sha256"], config.R003_RECIPE_SHA256)
        self.assertEqual(snapshot["schema_sha256"], config.R003_SCHEMA_SHA256)
        self.assertFalse(snapshot["checker_execution"])
        self.assertFalse(snapshot["stall_switch"])

    def test_working_position_string_equality_does_not_adjudicate_use_dependence(self):
        run = self.new_run("prose-use")
        answer = OpenFixture.answer()
        text = answer["answer"]
        use = {
            "decision": "answered", "missing_derivation": "", "query_id": "prose-use",
            "question": "Does the later choice depend on the returned distinction?",
            "problem_derivation": "The problem leaves two live accounts.",
            "before": {"answer_quote": text, "derivation": "The distinction is absent.",
                       "conclusion": "defer"},
            "after": {"answer_quote": text, "derivation": "The returned reason separates the cases.",
                      "conclusion": "defer"},
            "dependency": {"relation_id": "working_position", "before_quote": text,
                           "after_quote": text, "result_depends_on_change": True,
                           "explanation": "The same label now has a supplied case distinction."},
            "objections": [], "checker": None,
        }
        parsed = r002.parse_r002(
            "propagation_use", json.dumps(use), r002.ContractSet(run / "contracts"),
            relation={"relations": [{"relation_id": "working_position"}]},
            before=answer, answer=answer, fork={"branch_points": []},
            study_profile="r003-open-v1")
        self.assertTrue(parsed["dependency"]["result_depends_on_change"])


if __name__ == "__main__":
    unittest.main()
