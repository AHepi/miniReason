"""Offline final-disposition, working isolation and frozen-resume regressions."""
import json
import unittest
from unittest import mock
from tests.reason import test_engine as fixture
from minireason.reason import config, engine
from minireason.reason.types import ReasonFailure

class Review12bEngineTests(unittest.TestCase):
    setUp = fixture.OfflineEngineTests.setUp
    tearDown = fixture.OfflineEngineTests.tearDown
    new_run = fixture.OfflineEngineTests.new_run

    def use_reply(self, role, cycle, objections):
        result = fixture.scripted_reply(role, cycle, objections)
        if role in ("critic", "return", "use"):
            result["working"] = "PRIVATE_PUBLIC_WORKING_" + role.upper()
        if role == "use":
            result["objections"] = [{"text": "The final use finds a missing boundary.",
                                     "defeats": "The returned universal claim."}]
        return result

    def test_working_never_delivered_and_closing_disposes_final_use(self):
        run = self.new_run(cycles=2)
        state = engine.execute(run, scripted=self.use_reply)
        self.assertEqual(state["stop_reason"], "cycle_budget")
        self.assertEqual(state["closing_return"], "complete")
        self.assertEqual(state["calls"], 10)
        self.assertFalse(any(o["status"] == "unresolved" for o in state["objections"]))
        for path in run.glob("calls/*/a*/request.json"):
            text = fixture.read(path)
            self.assertNotIn("PRIVATE_PUBLIC_WORKING_", text)
        for role, cid in [("critic", "c0001-k01"), ("return", "c0001-return"), ("use", "c0001-use")]:
            body = "PRIVATE_PUBLIC_WORKING_" + role.upper()
            self.assertIn(body, fixture.read(run / "calls" / cid / "a00/response.json"))
            self.assertIn(body, fixture.read(run / "cycles/c0001/CYCLE.md"))
        self.assertNotIn("PRIVATE_PUBLIC_WORKING_", fixture.read(run / "TRACE.md"))
        self.assertIn("closing return: **taken-up**", fixture.read(run / "TRACE.md"))
        self.assertIn("No open objection", fixture.read(run / "ANSWER.md"))
        saved = {p: fixture.read(p) for p in run.glob("calls/*/a*/*.json")}
        count = self.counter.offline
        again = engine.execute(run, scripted=self.use_reply)
        self.assertEqual(again["calls"], state["calls"])
        self.assertEqual(self.counter.offline, count)
        self.assertEqual(saved, {p: fixture.read(p) for p in saved})

    def test_closing_can_leave_honestly_unresolved_after_final_disposition(self):
        def reply(role, cycle, objections):
            result = self.use_reply(role, cycle, objections)
            if role == "return":
                for item in result["dispositions"]:
                    item.update(status="unresolved", reason="Still needs evidence.")
            return result
        run = self.new_run(cycles=1)
        state = engine.execute(run, scripted=reply)
        self.assertEqual(state["stop_reason"], "cycle_budget")
        self.assertEqual(state["calls"], 6)
        self.assertTrue(all(o["history"][-1]["phase"] == "closing_return" for o in state["objections"]))
        self.assertIn("Still needs evidence.", fixture.read(run / "ANSWER.md"))

    def test_disabled_recipe_retains_open_use(self):
        recipe = config.load_recipe("cross-family")["data"]
        recipe["closing_return"] = False
        path = self.case / "recipe.json"
        fixture.write(path, json.dumps(recipe))
        run = self.new_run(cycles=1, recipe=path)
        state = engine.execute(run, scripted=self.use_reply)
        self.assertEqual(state["calls"], 5)
        self.assertNotIn("closing_return", state)
        self.assertTrue(any(o["status"] == "unresolved" for o in state["objections"]))

    def test_no_use_objection_means_no_extra_call_even_with_open_critic(self):
        def reply(role, cycle, objections):
            result = fixture.scripted_reply(role, cycle, objections)
            if role == "return":
                for item in result["dispositions"]:
                    item.update(status="unresolved", reason="Needs more evidence.")
            return result
        run = self.new_run(cycles=1)
        state = engine.execute(run, scripted=reply)
        self.assertEqual(state["calls"], 5)
        self.assertNotIn("closing_return", state)

    def test_closing_failure_keeps_completed_cycle_and_evidence(self):
        original = engine.Adapter.call
        def fail(adapter, **kwargs):
            if kwargs["coordinate"]["call_id"].endswith("closing-return"):
                raise ReasonFailure("TRANSPORT_OR_RESPONSE_ERROR", "Offline closing failure.")
            return original(adapter, **kwargs)
        run = self.new_run(cycles=1)
        with mock.patch.object(engine.Adapter, "call", fail):
            state = engine.execute(run, scripted=self.use_reply)
        self.assertEqual(state["stop_reason"], "TRANSPORT_OR_RESPONSE_ERROR")
        self.assertEqual(state["completed_cycles"], 1)
        note = fixture.read(run / "cycles/c0001/CYCLE.md")
        self.assertIn("Working answer after return", note)
        self.assertIn("Closing return failed", note)

    def test_closing_unknown_outcome_is_not_replayed(self):
        class Interrupted(BaseException): pass
        original = engine.Adapter.call
        def fail(adapter, **kwargs):
            if kwargs["coordinate"]["call_id"].endswith("closing-return"):
                raise Interrupted()
            return original(adapter, **kwargs)
        run = self.new_run(cycles=1)
        with mock.patch.object(engine.Adapter, "call", fail):
            with self.assertRaises(Interrupted):
                engine.execute(run, scripted=self.use_reply)
        count = self.counter.offline
        resumed = engine.execute(run, scripted=self.use_reply)
        self.assertEqual(resumed["stop_reason"], "INTERRUPTED_CALL")
        self.assertEqual(self.counter.offline, count)

    def test_closing_is_in_budget_and_boolean_validated(self):
        run = self.new_run(cycles=2, baseline=True)
        state = engine.execute(run, scripted=fixture.scripted_reply)
        self.assertEqual(state["calls"], 11)
        report = fixture.read(run / "RUN.md")
        for phrase in ("planned logical calls without early stop: 12.",
                       "Completion allowance without repair/retry/fallback: 221184.",
                       "transport retries: 28;", "maximum completion allowance: 573440.",
                       "closing-return (conditional)"):
            self.assertIn(phrase, report)
        recipe = config.load_recipe("cross-family")["data"]
        for invalid in (0, 1, None, "true"):
            recipe["closing_return"] = invalid
            with self.assertRaises(ReasonFailure):
                config.validate_recipe(recipe)

    def test_legacy_contract_and_disabled_closing_are_frozen_on_resume(self):
        run = self.new_run(cycles=1)
        cfg = fixture.load(run / "config.json")
        cfg.pop("prompt_contract")
        cfg.pop("closing_return")
        fixture.write(run / "config.json", json.dumps(cfg))
        def reply(role, cycle, objections):
            value = self.use_reply(role, cycle, objections)
            value.pop("working", None)
            return value
        state = engine.execute(run, scripted=reply)
        self.assertEqual(state["calls"], 5)
        self.assertTrue(any(o["status"] == "unresolved" for o in state["objections"]))
        request = fixture.load(run / "calls/c0001-k01/a00/request.json")
        self.assertNotIn('"working"', request["prepared"]["messages"][0]["content"])
        with mock.patch.object(engine.Adapter, "call", side_effect=AssertionError("Replay")):
            again = engine.execute(run)
        self.assertEqual(again["calls"], 5)

    def test_completed_working_survives_a_later_cycle_failure(self):
        original = engine.Adapter.call
        def fail(adapter, **kwargs):
            if kwargs["role"] == "return":
                raise ReasonFailure("TRANSPORT_OR_RESPONSE_ERROR", "Offline return failure.")
            return original(adapter, **kwargs)
        run = self.new_run(cycles=1)
        with mock.patch.object(engine.Adapter, "call", fail):
            state = engine.execute(run, scripted=self.use_reply)
        self.assertEqual(state["stop_reason"], "TRANSPORT_OR_RESPONSE_ERROR")
        self.assertIn("PRIVATE_PUBLIC_WORKING_CRITIC", fixture.read(run / "cycles/c0001/CYCLE.md"))
        self.assertNotIn("PRIVATE_PUBLIC_WORKING_CRITIC", fixture.read(run / "TRACE.md"))

    def test_actual_baseline_bytes_need_no_repair_and_preserve_supplements(self):
        from tests.reason.test_review12b_prompts import FIXTURE
        content = fixture.read(FIXTURE)
        def reply(role, cycle, objections):
            if role == "baseline":
                return {"content": content}
            return fixture.scripted_reply(role, cycle, objections)
        run = self.new_run(cycles=1, baseline=True)
        state = engine.execute(run, scripted=reply)
        self.assertEqual(state["stop_reason"], "cycle_budget")
        for label in ("bare", "native"):
            self.assertFalse((run / "calls" / ("base-" + label) / "a01").exists())
        baseline = fixture.read(run / "BASELINE.md")
        original = json.loads(content)
        self.assertIn(original["assumptions"], baseline)
        self.assertIn(original["uncertainties"], baseline)
