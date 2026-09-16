"""W16 regressions for explicit schema evidence and carried dispositions."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest import mock
import uuid

from minireason.reason import engine, prompts
from minireason.reason.types import ReasonFailure
from tests.reason import test_engine as fixture


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "work" / "w16" / "test-contract"
CLI_SPEC = importlib.util.spec_from_file_location("w16_reason_cli", ROOT / "tools" / "reason.py")
CLI = importlib.util.module_from_spec(CLI_SPEC)
CLI_SPEC.loader.exec_module(CLI)


def objection(ident: str, *, status: str = "unresolved", reason: str = "Still open.", born: int = 1):
    return {
        "id": ident,
        "text": "The named boundary case is not handled.",
        "defeats": "The claimed universal coverage.",
        "status": status,
        "reason": reason,
        "born_cycle": born,
    }


def disposition(ident: str, *, status: str = "taken-up", reason: str = "Added the boundary case."):
    return {"id": ident, "status": status, "reason": reason}


class ParserContractTests(unittest.TestCase):
    def assert_schema(self, content, objections=(), *fragments):
        with self.assertRaises(ReasonFailure) as caught:
            prompts.parse("return", content, objections=objections,
                          contract_version="public-working-v2")
        self.assertEqual(caught.exception.code, "SCHEMA_FAILURE")
        for fragment in fragments:
            self.assertIn(fragment, caught.exception.detail)
        return caught.exception

    def test_v2_names_the_failed_contract_check(self):
        open_item = objection("o-open")
        valid = {"answer": "Revised answer.", "dispositions": [disposition("o-open")]}
        cases = [
            ({"answer": "Revised answer."}, (open_item,), ("missing", "dispositions")),
            ({"answer": "Revised answer.", "dispositions": {}}, (open_item,),
             ("dispositions", "list")),
            ({"answer": "", "dispositions": [disposition("o-open")]}, (open_item,),
             ("answer", "nonempty")),
            ({**valid, "dispositions": [{**disposition("o-open"), "note": "unexpected"}]},
             (open_item,), ("key set", "note")),
            ({**valid, "dispositions": [disposition("o-open", status="ignored")]},
             (open_item,), ("invalid status", "ignored")),
            ({"answer": "Revised answer.", "dispositions": []}, (open_item,),
             ("missing", "o-open")),
            ({**valid, "dispositions": [disposition("o-open"), disposition("o-open")]},
             (open_item,), ("duplicate", "o-open")),
            ({**valid, "dispositions": [disposition("o-open"), disposition("ghost")]},
             (open_item,), ("extra", "ghost")),
        ]
        for value, supplied, fragments in cases:
            with self.subTest(fragments=fragments):
                self.assert_schema(json.dumps(value), supplied, *fragments)

    def test_truncated_and_malformed_json_have_byte_specific_reasons(self):
        truncated = '{"answer":"Revised", "dispositions": ['
        failure = self.assert_schema(truncated, (), "JSON truncated at byte")
        self.assertIn(str(len(truncated.encode("utf-8"))), failure.detail)

        unicode_prefix = '{"answer":"' + chr(955)
        failure = self.assert_schema(unicode_prefix, (), "JSON truncated at byte")
        self.assertIn(str(len(unicode_prefix.encode("utf-8"))), failure.detail)

        malformed = '{"answer": ]}'
        failure = self.assert_schema(malformed, (), "JSON invalid at byte")
        self.assertIn(str(len('{"answer": '.encode("utf-8"))), failure.detail)

    def test_extra_fields_are_not_optional_contract_fields_of_other_roles(self):
        value = {"answer": "Conclusion.", "working": {"public": "kept"}}
        self.assertEqual(prompts.parse("baseline", json.dumps(value)), value)
        value = {"objections": [], "assumptions": {"public": "kept"}}
        self.assertEqual(prompts.parse("critic", json.dumps(value)), value)
        with self.assertRaises(ReasonFailure):
            prompts.parse("critic", '{"objections":[],"working":{}}')

    def test_v2_carries_resolved_omissions_and_retains_extra_top_level_keys(self):
        resolved = objection("o-old", status="taken-up", reason="Already incorporated.")
        open_item = objection("o-new", born=2)
        value = {
            "type": "json_object",
            "vendor_note": "retained public metadata",
            "answer": "Revised answer.",
            "dispositions": [disposition("o-new")],
        }
        parsed = prompts.parse("return", json.dumps(value), objections=(resolved, open_item),
                               contract_version="public-working-v2")
        self.assertEqual(parsed["type"], "json_object")
        self.assertEqual(parsed["vendor_note"], "retained public metadata")
        self.assertEqual([item["id"] for item in parsed["dispositions"]], ["o-new"])

        value["dispositions"].append(
            disposition("o-old", status="rejected-with-reason", reason="Rechecked explicitly."))
        parsed = prompts.parse("return", json.dumps(value), objections=(resolved, open_item),
                               contract_version="public-working-v2")
        self.assertEqual({item["id"] for item in parsed["dispositions"]}, {"o-old", "o-new"})

        with self.assertRaises(ReasonFailure):
            prompts.parse("return", json.dumps(value), objections=(resolved, open_item),
                          contract_version="public-working-v1")


class EngineContractTests(unittest.TestCase):
    def setUp(self):
        self.case = EVIDENCE / uuid.uuid4().hex[:10]
        self.case.mkdir(parents=True)
        fixture.write(self.case / "CASE.txt", self.id() + "\n")
        self.counter = fixture.ProviderCounter()
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(mock.patch("os.environ", {"PYTHONUTF8": "1"}))
        self.stack.enter_context(fixture.no_network(self.counter))

    def tearDown(self):
        self.assertEqual(self.counter.opened, 0)
        self.assertEqual(self.counter.completed_live, 0)
        fixture.write(self.case / "COUNTERS.json", json.dumps(vars(self.counter), indent=2) + "\n")

    def new_run(self, name="run", *, cycles=1):
        return engine.create_run(
            problem="Determine whether the stated invariant covers every boundary case.",
            cycles=cycles,
            recipe="single-family",
            out=self.case / name,
            mode="offline",
        )

    def records(self, run):
        return {
            str(path.relative_to(run)): fixture.read(path)
            for path in sorted(run.glob("calls/*/a*/*.json"))
        }

    def test_resolved_disposition_is_carried_and_completed_resume_is_byte_stable(self):
        seen_returns = []

        def reply(role, cycle, supplied):
            if role == "critic":
                return {"objections": [{
                    "text": f"Cycle {cycle} boundary omission.",
                    "defeats": "The universal coverage claim.",
                }]}
            if role == "return":
                seen_returns.append([dict(item) for item in supplied])
                required = [item for item in supplied if item["status"] == "unresolved"]
                return {
                    "answer": f"Answer after cycle {cycle}.",
                    "dispositions": [disposition(item["id"], reason=f"Cycle {cycle} repair.")
                                     for item in required],
                }
            return fixture.scripted_reply(role, cycle, supplied)

        run = self.new_run(cycles=2)
        state = engine.execute(run, scripted=reply)
        self.assertEqual(state["stop_reason"], "cycle_budget")
        self.assertEqual(len(seen_returns), 2)
        self.assertEqual(len(seen_returns[0]), 1)
        self.assertEqual(len(seen_returns[1]), 2)
        old_id = seen_returns[0][0]["id"]
        new_id = next(item["id"] for item in seen_returns[1] if item["id"] != old_id)

        cycle_two = fixture.load(run / "calls" / "c0002-return" / "a00" / "response.json")
        self.assertEqual([item["id"] for item in cycle_two["parsed"]["dispositions"]], [new_id])
        saved = fixture.load(run / "state.json")
        old = next(item for item in saved["objections"] if item["id"] == old_id)
        self.assertEqual(old["status"], "taken-up")
        self.assertEqual(old["reason"], "Cycle 1 repair.")
        self.assertEqual(old["history"][-1]["cycle"], 2)
        self.assertTrue(old["history"][-1]["carried"])
        self.assertEqual(old["history"][-1]["reason"], "Cycle 1 repair.")
        trace = fixture.read(run / "TRACE.md")
        self.assertIn(old_id, trace)
        self.assertIn("carried", trace.lower())

        before = self.records(run)
        calls = self.counter.offline
        resumed = engine.execute(run, scripted=reply)
        self.assertEqual(resumed["stop_reason"], "cycle_budget")
        self.assertEqual(self.counter.offline, calls)
        self.assertEqual(self.records(run), before)

    def test_cycle_with_only_resolved_ids_accepts_empty_or_explicit_redisposition(self):
        for explicit in (False, True):
            with self.subTest(explicit=explicit):
                seen = []

                def reply(role, cycle, supplied):
                    if role == "critic":
                        if cycle == 1:
                            return {"objections": [{
                                "text": "The boundary case is omitted.",
                                "defeats": "The universal claim.",
                            }]}
                        return {"objections": []}
                    if role == "return":
                        seen.append([dict(item) for item in supplied])
                        if cycle == 1:
                            items = [disposition(supplied[0]["id"], reason="Cycle 1 settled it.")]
                            return {"answer": "Cycle 1 answer.", "dispositions": items}
                        self.assertEqual(len(supplied), 1)
                        self.assertEqual(supplied[0]["status"], "taken-up")
                        items = []
                        if explicit:
                            items = [disposition(
                                supplied[0]["id"],
                                status="rejected-with-reason",
                                reason="Cycle 2 explicitly reconsidered it.",
                            )]
                        return {
                            "type": "json_object",
                            "answer": "Cycle 2 answer.",
                            "dispositions": items,
                        }
                    return fixture.scripted_reply(role, cycle, supplied)

                run = self.new_run("resolved-explicit" if explicit else "resolved-carried", cycles=2)
                state = engine.execute(run, scripted=reply)
                self.assertEqual(state["stop_reason"], "no_new_objections")
                self.assertEqual(len(seen), 2)
                self.assertEqual([item["id"] for item in seen[1]], [seen[0][0]["id"]])
                outcome = fixture.load(run / "calls" / "c0002-return" / "a00" / "response.json")
                self.assertEqual(outcome["parsed"]["type"], "json_object")
                self.assertEqual(outcome["extra_keys"], ["type"])
                saved = fixture.load(run / "state.json")["objections"][0]
                if explicit:
                    self.assertEqual(saved["status"], "rejected-with-reason")
                    self.assertEqual(saved["history"][-1]["reason"],
                                     "Cycle 2 explicitly reconsidered it.")
                    self.assertNotIn("carried", saved["history"][-1])
                else:
                    self.assertEqual(outcome["parsed"]["dispositions"], [])
                    self.assertEqual(saved["status"], "taken-up")
                    self.assertEqual(saved["history"][-1]["reason"], "Cycle 1 settled it.")
                    self.assertTrue(saved["history"][-1]["carried"])

    def test_extra_keys_are_retained_and_named_in_the_attempt_outcome(self):
        def reply(role, cycle, supplied):
            value = fixture.scripted_reply(role, cycle, supplied)
            if role == "conjecture":
                value = {"type": "json_object", "vendor_note": "kept", **value}
            return value

        run = self.new_run()
        state = engine.execute(run, scripted=reply)
        self.assertEqual(state["stop_reason"], "cycle_budget")
        outcome = fixture.load(run / "calls" / "initial" / "a00" / "response.json")
        self.assertEqual(outcome["parsed"]["type"], "json_object")
        self.assertEqual(outcome["parsed"]["vendor_note"], "kept")
        self.assertEqual(outcome["extra_keys"], ["type", "vendor_note"])

    def test_schema_detail_reaches_repair_state_and_reports(self):
        run = self.new_run()
        state = engine.execute(run, scripted=lambda *args: {"answer": ""})
        self.assertEqual(state["stop_reason"], "SCHEMA_FAILURE")
        first = fixture.load(run / "calls" / "initial" / "a00" / "response.json")
        repair = fixture.load(run / "calls" / "initial" / "a01" / "request.json")
        second = fixture.load(run / "calls" / "initial" / "a01" / "response.json")
        self.assertIn("answer", first["detail"])
        self.assertIn(first["detail"], repair["prepared"]["messages"][-1]["content"])
        self.assertEqual(state["stop_detail"], second["detail"])
        for name in ("TRACE.md", "RUN.md"):
            self.assertIn(second["detail"], fixture.read(run / name))

    def test_finish_reason_length_uses_existing_native_fallback(self):
        run = self.new_run()
        state = engine.execute(run, scripted=lambda *args: {
            "content": '{"answer":"cut',
            "finish_reason": "length",
            "usage": {"prompt_tokens": 3, "completion_tokens": 32768, "total_tokens": 32771},
        })
        self.assertEqual(state["stop_reason"], "CEILING_HIT")
        self.assertEqual(fixture.load(run / "calls" / "initial" / "a00" / "response.json")["status"],
                         "CEILING_HIT")
        fallback = fixture.load(run / "calls" / "initial" / "a01" / "request.json")
        self.assertTrue(fallback["ceiling_fallback"])
        self.assertEqual(fallback["thinking"], "off")
        self.assertFalse((run / "calls" / "initial" / "a02").exists())

    def test_cap_sized_truncated_json_with_stop_is_ceiling_but_other_syntax_is_schema(self):
        attempts = 0

        def cap_then_valid(role, cycle, supplied):
            nonlocal attempts
            if role == "conjecture":
                attempts += 1
                if attempts == 1:
                    return {
                        "content": '{"answer":"cut',
                        "finish_reason": "stop",
                        "usage": {"prompt_tokens": 5, "completion_tokens": 32768,
                                  "total_tokens": 32773},
                    }
            return fixture.scripted_reply(role, cycle, supplied)

        run = self.new_run("cap-truncated")
        state = engine.execute(run, scripted=cap_then_valid)
        self.assertEqual(state["stop_reason"], "cycle_budget")
        first = fixture.load(run / "calls" / "initial" / "a00" / "response.json")
        self.assertEqual(first["status"], "CEILING_HIT")
        self.assertIn("JSON truncated at byte", first["detail"])
        fallback = fixture.load(run / "calls" / "initial" / "a01" / "request.json")
        self.assertTrue(fallback["ceiling_fallback"])
        self.assertFalse(fallback["schema_repair"])

        for name, content, completion in (
            ("under-cap", '{"answer":"cut', 32767),
            ("bad-syntax", '{"answer": ]}', 32768),
        ):
            with self.subTest(name=name):
                other = self.new_run(name)
                stopped = engine.execute(other, scripted=lambda *args, c=content, n=completion: {
                    "content": c,
                    "finish_reason": "stop",
                    "usage": {"prompt_tokens": 5, "completion_tokens": n, "total_tokens": n + 5},
                })
                self.assertEqual(stopped["stop_reason"], "SCHEMA_FAILURE")
                first = fixture.load(other / "calls" / "initial" / "a00" / "response.json")
                self.assertEqual(first["status"], "SCHEMA_FAILURE")
                repair = fixture.load(other / "calls" / "initial" / "a01" / "request.json")
                self.assertTrue(repair["schema_repair"])
                self.assertFalse(repair["ceiling_fallback"])

    def test_cli_terminal_json_includes_specific_stop_detail(self):
        result = {
            "run_id": "fixture-run",
            "stop_reason": "SCHEMA_FAILURE",
            "stop_detail": "dispositions missing for ids ['o-open']",
            "completed_cycles": 1,
            "calls": 7,
        }
        output = io.StringIO()
        with mock.patch.object(CLI, "execute", return_value=result), \
                contextlib.redirect_stdout(output):
            code = CLI.main(["resume", "--run", str(self.case / "saved-run")])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(output.getvalue()), result)


if __name__ == "__main__":
    unittest.main()
