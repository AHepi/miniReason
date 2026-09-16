"""Adversarial engine corrections; all fixtures are offline and retained."""
import json
import unittest
from unittest import mock
from tests.reason import test_engine as fixture
from minireason.reason import engine
from minireason.reason.types import ReasonFailure

class JudgeEngineTests(unittest.TestCase):
    setUp = fixture.OfflineEngineTests.setUp
    tearDown = fixture.OfflineEngineTests.tearDown
    new_run = fixture.OfflineEngineTests.new_run

    def test_one_schema_repair_preserves_contract_settings_and_resumes(self):
        count = 0
        def reply(role, cycle, objections):
            nonlocal count
            if role == "conjecture":
                count += 1
                if count == 1:
                    return {"content": "My public answer without the JSON wrapper."}
            return fixture.scripted_reply(role, cycle, objections)
        run = self.new_run(cycles=1)
        state = engine.execute(run, scripted=reply)
        self.assertEqual(state["stop_reason"], "cycle_budget")
        before = fixture.load(run / "calls/initial/a00/request.json")
        repair = fixture.load(run / "calls/initial/a01/request.json")
        first_response = fixture.load(run / "calls/initial/a00/response.json")
        self.assertEqual(first_response["status"], "SCHEMA_FAILURE")
        self.assertTrue(repair["schema_repair"])
        self.assertEqual(repair["thinking"], before["thinking"])
        self.assertEqual(repair["prepared"]["messages"][:-2], before["prepared"]["messages"])
        self.assertEqual(repair["prepared"]["messages"][-2],
                         {"role": "assistant", "content": first_response["result"]["content"]})
        self.assertEqual(repair["prepared"]["kwargs"]["max_tokens"], before["prepared"]["kwargs"]["max_tokens"])
        self.assertIn("Schema repair calls: 1", fixture.read(run / "RUN.md"))
        originals = {p: fixture.read(p) for p in (run / "calls").rglob("*") if p.is_file()}
        prior = self.counter.offline
        again = engine.execute(run, scripted=reply)
        self.assertEqual(again["stop_reason"], "cycle_budget")
        self.assertEqual(self.counter.offline, prior)
        self.assertEqual({p: fixture.read(p) for p in originals}, originals)

    def test_second_schema_failure_stops_without_third_attempt(self):
        run = self.new_run(cycles=1, retry_transport=4)
        state = engine.execute(run, scripted=lambda *args: {"content": "invalid public object"})
        self.assertEqual(state["stop_reason"], "SCHEMA_FAILURE")
        self.assertEqual(state["calls"], 2)
        self.assertEqual(self.counter.offline, 2)
        self.assertFalse((run / "calls/initial/a02").exists())
        self.assertIn("Schema repair calls: 1", fixture.read(run / "RUN.md"))

    def test_repair_transport_failure_is_not_retried(self):
        count = 0
        def reply(*args):
            nonlocal count
            count += 1
            if count == 1:
                return {"content": "invalid public object"}
            raise ReasonFailure("TRANSPORT_OR_RESPONSE_ERROR", "offline failure")
        run = self.new_run(cycles=1, retry_transport=4)
        state = engine.execute(run, scripted=reply)
        self.assertEqual(state["stop_reason"], "TRANSPORT_OR_RESPONSE_ERROR")
        self.assertEqual(count, 2)
        self.assertEqual(state["calls"], 2)

    def test_repair_intent_without_outcome_is_never_replayed(self):
        class Interrupted(BaseException): pass
        original = engine.Adapter.call
        def interrupt(adapter, **kwargs):
            if kwargs["coordinate"]["schema_repair"]:
                raise Interrupted()
            return original(adapter, **kwargs)
        run = self.new_run(cycles=1)
        with mock.patch.object(engine.Adapter, "call", interrupt):
            with self.assertRaises(Interrupted):
                engine.execute(run, scripted=lambda *args: {"content": "invalid public object"})
        prior = self.counter.offline
        state = engine.execute(run)
        self.assertEqual(state["stop_reason"], "INTERRUPTED_CALL")
        self.assertEqual(self.counter.offline, prior)
        self.assertEqual(state["calls"], 2)

    def test_each_seat_thinking_and_baseline_override_are_recorded(self):
        run = self.new_run(cycles=1, baseline=True, recipe="cross-family-rival")
        state = engine.execute(run, scripted=fixture.scripted_reply)
        self.assertEqual(state["stop_reason"], "cycle_budget")
        expected = {"base-bare": "off", "base-native": "native", "initial": "native",
                    "c0001-rival": "gateway-default", "c0001-k01": "gateway-default",
                    "c0001-k02": "gateway-default", "c0001-return": "native", "c0001-use": "gateway-default"}
        for call, setting in expected.items():
            req = fixture.load(run / "calls" / call / "a00/request.json")
            self.assertEqual(req["thinking"], setting)
            self.assertEqual(req["prepared"]["thinking"], setting)
            payload = req["prepared"]["payload"]
            if setting == "gateway-default":
                self.assertNotIn("thinking", payload)
                self.assertNotIn("think", payload)
            else:
                self.assertEqual(payload["thinking"]["type"], "enabled" if setting == "native" else "disabled")
            self.assertIn(call, fixture.read(run / "RUN.md"))
        bare = fixture.load(run / "calls/base-bare/a00/request.json")
        native = fixture.load(run / "calls/base-native/a00/request.json")
        self.assertEqual(bare["prepared"]["messages"], native["prepared"]["messages"])

    def test_last_return_and_open_use_objection_are_in_answer(self):
        def reply(role, cycle, objections):
            result = fixture.scripted_reply(role, cycle, objections)
            if role == "use":
                result["objections"] = [{"text": "Independent derivation contradicts the stated boundary.",
                                         "defeats": "The returned boundary claim."}]
            return result
        run = self.new_run(cycles=2)
        state = engine.execute(run, scripted=reply)
        answer = fixture.read(run / "ANSWER.md")
        self.assertIn("Revised answer 2", answer)
        self.assertNotIn("Revised answer 1", answer)
        self.assertIn("c0002-use-o001", answer)
        self.assertIn("Independent derivation contradicts", answer)
        for obj in state["objections"]:
            for cycle in range(obj["born_cycle"], 3):
                self.assertTrue(any(item["cycle"] == cycle for item in obj["history"]))
        cycle = fixture.read(run / "cycles/c0002/CYCLE.md")
        self.assertIn("Independent derivation from PROBLEM", cycle)
        self.assertIn("Derivation from WORKING ANSWER", cycle)

    def test_fenced_public_json_does_not_spend_repair_call(self):
        def reply(role, cycle, objections):
            return {"content": "Public preamble\n```json\n" + json.dumps(fixture.scripted_reply(role, cycle, objections)) + "\n```\nPublic closing"}
        run = self.new_run(cycles=1)
        state = engine.execute(run, scripted=reply)
        self.assertEqual(state["stop_reason"], "cycle_budget")
        self.assertEqual(state["calls"], 5)
        self.assertIn("Schema repair calls: 0", fixture.read(run / "RUN.md"))

if __name__ == "__main__":
    unittest.main()
