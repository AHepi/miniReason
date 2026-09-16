"""Acceptance cases preserve every fixture run under ignored work/w12."""
from __future__ import annotations
import contextlib
import hashlib
import json
import os
from pathlib import Path
import socket
import unittest
from unittest import mock
import uuid

from minireason import provider_openai_compat as transport
from minireason.reason import config, engine
from minireason.reason.types import ReasonFailure

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "work" / "review12" / "e"


def read(path):
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return handle.read()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(value)
    if read(path) != value:
        raise AssertionError("Fixture text changed on write")


def load(path):
    return json.loads(read(path))


class ProviderCounter:
    def __init__(self):
        self.live = 0
        self.offline = 0
        self.opened = 0
        self.completed_live = 0


@contextlib.contextmanager
def no_network(counter):
    live_init = transport.OpenAICompatProvider.__init__
    offline_init = transport.OfflineProvider.__init__

    def counted_live(provider, *args, **kwargs):
        counter.live += 1
        return live_init(provider, *args, **kwargs)

    def counted_offline(provider, *args, **kwargs):
        counter.offline += 1
        return offline_init(provider, *args, **kwargs)

    def refused_open(*args, **kwargs):
        counter.opened += 1
        raise AssertionError("Provider attempted a network request")

    def refused_complete(*args, **kwargs):
        counter.completed_live += 1
        raise AssertionError("Live provider completion was called")

    def refused_socket(*args, **kwargs):
        raise AssertionError("A socket was opened")

    with contextlib.ExitStack() as stack:
        stack.enter_context(mock.patch.object(transport.OpenAICompatProvider, "__init__", counted_live))
        stack.enter_context(mock.patch.object(transport.OfflineProvider, "__init__", counted_offline))
        stack.enter_context(mock.patch.object(transport.OpenAICompatProvider, "complete", refused_complete))
        stack.enter_context(mock.patch.object(transport, "_open", refused_open))
        stack.enter_context(mock.patch.object(socket, "socket", refused_socket))
        stack.enter_context(mock.patch.object(socket, "create_connection", refused_socket))
        yield counter


def scripted_reply(role, cycle, objections):
    if role in {"conjecture", "rival", "baseline"}:
        return {"answer": f"Working answer {cycle}: maintain the stated invariant."}
    if role == "critic":
        return {"objections": [{"text": f"Cycle {cycle}: the boundary case is unstated.",
                                 "defeats": "The universal scope of the working answer."}]}
    if role == "return":
        return {"answer": f"Revised answer {cycle}: the boundary condition is explicit.",
                "dispositions": [{"id": objection["id"], "status": "taken-up",
                                  "reason": "Added the named boundary condition."}
                                 for objection in objections]}
    if role == "use":
        return {"question": "What happens on the boundary case in the working answer?",
                "problem_derivation": "From the stated invariant, the boundary retains the specified condition.",
                "working_derivation": "Applying the returned boundary rule retains the same condition.", "objections": []}
    raise AssertionError(f"Unexpected role {role}")


class OfflineEngineTests(unittest.TestCase):
    def setUp(self):
        self.case = EVIDENCE / uuid.uuid4().hex[:8]
        self.case.mkdir(parents=True)
        write(self.case / "CASE.txt", self.id() + "\n")
        self.counter = ProviderCounter()
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(mock.patch("os.environ", {"PYTHONUTF8": "1"}))
        self.stack.enter_context(no_network(self.counter))

    def tearDown(self):
        self.assertEqual(self.counter.opened, 0)
        self.assertEqual(self.counter.completed_live, 0)
        write(self.case / "COUNTERS.json", json.dumps(vars(self.counter), indent=2) + "\n")

    def new_run(self, **kwargs):
        options = {"problem": "Find a sound answer with an explicit boundary condition.",
                   "cycles": 3, "out": self.case / "r", "mode": "offline"}
        options.update(kwargs)
        return engine.create_run(**options)

    def run_fixture(self, **kwargs):
        run = self.new_run(**kwargs)
        return run, engine.execute(run, scripted=scripted_reply)

    def responses(self, run):
        return sorted(run.glob("calls/*/a*/response.json"))

    def test_full_three_cycles(self):
        run, result = self.run_fixture()
        self.assertEqual(result["stop_reason"], "cycle_budget")
        self.assertEqual(result["completed_cycles"], 3)
        critics = len(load(run / "recipe.json")["seats"]["critics"])
        self.assertEqual(result["calls"], 1 + 3 * (critics + 2))
        self.assertEqual(len(self.responses(run)), result["calls"])
        self.assertEqual(self.counter.offline, result["calls"])
        self.assertEqual(self.counter.live, 0)
        for cycle in range(1, 4):
            self.assertTrue((run / "cycles" / f"c{cycle:04d}" / "CYCLE.md").is_file())
        for name in ("ANSWER.md", "TRACE.md", "RUN.md", "state.json"):
            self.assertTrue((run / name).is_file(), name)
        self.assertIn("Revised answer 3", read(run / "ANSWER.md"))
        self.assertEqual(engine.status(run)["stop_reason"], "cycle_budget")

    def test_stop_only_after_no_new_critic_or_use_objections(self):
        def quiet(role, cycle, objections):
            if role == "critic":
                return {"objections": []}
            return scripted_reply(role, cycle, objections)
        run = self.new_run(cycles=5)
        result = engine.execute(run, scripted=quiet)
        self.assertEqual(result["stop_reason"], "no_new_objections")
        self.assertEqual(result["completed_cycles"], 1)

    def test_completed_response_survives_interruption_without_replay(self):
        class Interrupted(BaseException):
            pass
        def interrupt(call_id, response):
            if call_id == "c0001-return":
                raise Interrupted()
        run = self.new_run()
        with self.assertRaises(Interrupted):
            engine.execute(run, scripted=scripted_reply, after_call=interrupt)
        before = {str(path.relative_to(run)): read(path) for path in self.responses(run)}
        completed_before = self.counter.offline
        result = engine.execute(run, scripted=scripted_reply)
        self.assertEqual(result["stop_reason"], "cycle_budget")
        self.assertEqual(self.counter.offline, result["calls"])
        self.assertGreater(self.counter.offline, completed_before)
        for name, original in before.items():
            self.assertEqual(read(run / name), original)
        final_counter = self.counter.offline
        replayed = engine.execute(run, scripted=scripted_reply)
        self.assertEqual(replayed["stop_reason"], "cycle_budget")
        self.assertEqual(replayed["completed_cycles"], 3)
        self.assertEqual(replayed["calls"], result["calls"])
        self.assertEqual(self.counter.offline, final_counter)

    def test_live_missing_keys_refuses_before_provider_or_network(self):
        run = self.new_run(mode="live")
        result = engine.execute(run)
        self.assertEqual(result["stop_reason"], "KEY_MISSING")
        self.assertEqual(result["completed_cycles"], 0)
        self.assertEqual(self.counter.live, 0)
        self.assertEqual(self.counter.offline, 0)
        self.assertEqual(self.counter.completed_live, 0)
        self.assertEqual(self.counter.opened, 0)
        self.assertIn("KEY_MISSING", read(run / "RUN.md"))

    def test_recipe_exact_bytes_hashed_into_run_identity(self):
        loaded = config.load_recipe("cross-family")
        run = self.new_run()
        cfg = load(run / "config.json")
        self.assertEqual(read(run / "recipe.json"), loaded["text"])
        self.assertEqual(cfg["recipe_sha256"],
                         hashlib.sha256(loaded["text"].encode("utf-8")).hexdigest())
        self.assertIn(cfg["recipe_sha256"][:10], cfg["run_id"])

    def test_recipe_content_change_changes_hash(self):
        loaded = config.load_recipe("single-family")
        path = self.case / "recipe.json"
        write(path, loaded["text"] + "\n")
        changed = config.load_recipe(path)
        self.assertEqual(changed["data"], loaded["data"])
        self.assertNotEqual(changed["sha256"], loaded["sha256"])

    def test_saved_recipe_tamper_is_refused_without_calls(self):
        run = self.new_run()
        write(run / "recipe.json", read(run / "recipe.json") + "\n")
        with self.assertRaises(ReasonFailure) as caught:
            engine.execute(run, scripted=scripted_reply)
        self.assertEqual(caught.exception.code, "RUN_INTEGRITY_ERROR")
        self.assertEqual(self.counter.offline, 0)

    def test_baseline_adds_bare_and_native_calls_on_same_seat(self):
        run = self.new_run(cycles=1, baseline=True)
        result = engine.execute(run, scripted=scripted_reply)
        self.assertEqual(result["stop_reason"], "cycle_budget")
        self.assertTrue((run / "calls" / "base-bare" / "a00" / "response.json").is_file())
        self.assertTrue((run / "calls" / "base-native" / "a00" / "response.json").is_file())
        seat = load(run / "recipe.json")["seats"]["conjecture"]
        for call in ("base-bare", "base-native", "initial"):
            request = load(run / "calls" / call / "a00" / "request.json")
            self.assertEqual(request["seat"], seat)
        critics = len(load(run / "recipe.json")["seats"]["critics"])
        self.assertEqual(result["calls"], 3 + critics + 2)

    def test_trace_contains_every_objection_and_disposition(self):
        run, result = self.run_fixture()
        trace = read(run / "TRACE.md")
        self.assertEqual(result["completed_cycles"], 3)
        for cycle in range(1, 4):
            response = load(run / "calls" / f"c{cycle:04d}-return" / "a00" / "response.json")
            for disposition in response["parsed"]["dispositions"]:
                self.assertIn(disposition["id"], trace)
                self.assertIn(disposition["status"], trace)
                self.assertIn(disposition["reason"], trace)
            self.assertIn(f"Cycle {cycle}: the boundary case is unstated.", trace)

    def test_return_cannot_silently_drop_an_objection(self):
        def missing_dispositions(role, cycle, objections):
            if role == "return":
                return {"answer": "Changed without explanation.", "dispositions": []}
            return scripted_reply(role, cycle, objections)
        run = self.new_run()
        result = engine.execute(run, scripted=missing_dispositions)
        self.assertEqual(result["stop_reason"], "SCHEMA_FAILURE")
        self.assertEqual(result["completed_cycles"], 0)
        self.assertFalse((run / "calls" / "c0001-use").exists())

    def test_use_failure_is_returned_in_next_cycle(self):
        carried = []
        def with_use(role, cycle, objections):
            if role == "critic":
                return {"objections": []}
            if role == "return":
                carried.append((cycle, [dict(objection) for objection in objections]))
            result = scripted_reply(role, cycle, objections)
            if role == "use" and cycle == 1:
                result["objections"] = [{"text": "The application omitted the empty case.",
                                          "defeats": "The claim that all cases were covered."}]
            return result
        run = self.new_run(cycles=3)
        result = engine.execute(run, scripted=with_use)
        self.assertEqual(result["stop_reason"], "no_new_objections")
        self.assertEqual(result["completed_cycles"], 2)
        self.assertEqual(carried[0], (1, []))
        self.assertEqual(carried[1][0], 2)
        self.assertEqual(carried[1][1][0]["text"], "The application omitted the empty case.")
        trace = read(run / "TRACE.md")
        self.assertIn("Cycle 1: **unresolved**", trace)
        self.assertIn("Cycle 2: **taken-up**", trace)

    def test_unresolved_dispositions_block_early_stop(self):
        def unresolved(role, cycle, objections):
            if role == "critic" and cycle > 1:
                return {"objections": []}
            result = scripted_reply(role, cycle, objections)
            if role == "return":
                for disposition in result["dispositions"]:
                    disposition.update(status="unresolved", reason="Further evidence is needed.")
            return result
        run = self.new_run(cycles=2)
        result = engine.execute(run, scripted=unresolved)
        self.assertEqual(result["stop_reason"], "cycle_budget")
        self.assertEqual(result["completed_cycles"], 2)
        self.assertIn("Current disposition: **unresolved**", read(run / "TRACE.md"))

    def test_verbatim_problem_and_objection_delivery(self):
        problem = "A prose problem: first line.\r\nSecond line; exact spacing  retained."
        objection = "An objection: first line.\r\nSecond line; exact spacing  retained."
        def literal(role, cycle, objections):
            if role == "critic":
                return {"objections": [{"text": objection, "defeats": "The exact proposition."}]}
            return scripted_reply(role, cycle, objections)
        run = self.new_run(problem=problem, cycles=1)
        engine.execute(run, scripted=literal)
        self.assertEqual(read(run / "problem.txt"), problem)
        for request_path in run.glob("calls/*/a*/request.json"):
            request = load(request_path)
            user_text = request["prepared"]["messages"][1]["content"]
            self.assertIn(problem, user_text)
        returned = load(run / "calls" / "c0001-return" / "a00" / "request.json")
        self.assertIn(objection, returned["prepared"]["messages"][1]["content"])

    def test_schema_failure_keeps_public_response(self):
        run = self.new_run()
        result = engine.execute(run, scripted=lambda *args: {"answer": ""})
        self.assertEqual(result["stop_reason"], "SCHEMA_FAILURE")
        self.assertEqual(result["calls"], 2)
        saved = load(run / "calls" / "initial" / "a00" / "response.json")
        self.assertEqual(json.loads(saved["result"]["content"]), {"answer": ""})

    def test_ceiling_hit_records_partial_answer_and_stops(self):
        def length_stop(*args):
            return {"content": "Partial answer retained.", "finish_reason": "length",
                    "usage": {"prompt_tokens": 7, "completion_tokens": 8192, "total_tokens": 8199}}
        run = self.new_run()
        result = engine.execute(run, scripted=length_stop)
        self.assertEqual(result["stop_reason"], "CEILING_HIT")
        self.assertEqual(result["calls"], 1)
        response = load(run / "calls" / "initial" / "a00" / "provider" / "call-0001.response.json")
        self.assertEqual(response["content"], "Partial answer retained.")
        self.assertEqual(response["usage"]["completion_tokens"], 8192)

    def test_non_length_incomplete_is_not_a_token_ceiling(self):
        run = self.new_run()
        result = engine.execute(run, scripted=lambda *args: {
            "content": "Public partial text.", "finish_reason": None})
        self.assertEqual(result["stop_reason"], "INCOMPLETE_GENERATION")
        self.assertEqual(result["calls"], 1)

    def test_transport_error_has_no_implicit_retry(self):
        attempts = []
        def transport_error(*args):
            attempts.append(args)
            raise ReasonFailure("TRANSPORT_OR_RESPONSE_ERROR", "Synthetic transport interruption")
        run = self.new_run()
        result = engine.execute(run, scripted=transport_error)
        self.assertEqual(result["stop_reason"], "TRANSPORT_OR_RESPONSE_ERROR")
        self.assertEqual(len(attempts), 1)
        self.assertEqual(result["calls"], 1)
        before = read(run / "calls" / "initial" / "a00" / "response.json")
        engine.execute(run, scripted=transport_error)
        self.assertEqual(len(attempts), 1)
        self.assertEqual(read(run / "calls" / "initial" / "a00" / "response.json"), before)

    def test_explicit_transport_retry_creates_a_new_recorded_attempt(self):
        failed = []
        def retryable(role, cycle, objections):
            if role == "conjecture" and not failed:
                failed.append(True)
                raise ReasonFailure("TRANSPORT_OR_RESPONSE_ERROR", "Synthetic transport interruption")
            return scripted_reply(role, cycle, objections)
        run = self.new_run(cycles=1, retry_transport=1)
        result = engine.execute(run, scripted=retryable)
        self.assertEqual(result["stop_reason"], "cycle_budget")
        first = load(run / "calls" / "initial" / "a00" / "response.json")
        second = load(run / "calls" / "initial" / "a01" / "response.json")
        self.assertEqual(first["status"], "TRANSPORT_OR_RESPONSE_ERROR")
        self.assertEqual(second["status"], "COMPLETE")
        self.assertEqual(result["calls"], self.counter.offline + 1)

    def test_ambiguous_interrupted_call_is_not_replayed(self):
        run = self.new_run()
        class Interrupted(BaseException):
            pass
        with mock.patch.object(engine.Adapter, "call", side_effect=Interrupted()):
            with self.assertRaises(Interrupted):
                engine.execute(run, scripted=scripted_reply)
        request = run / "calls" / "initial" / "a00" / "request.json"
        self.assertIn("prepared", load(request))
        result = engine.execute(run, scripted=scripted_reply)
        self.assertEqual(result["stop_reason"], "INTERRUPTED_CALL")
        self.assertEqual(self.counter.offline, 0)
        self.assertFalse((request.parent / "response.json").exists())

    def test_run_and_provider_paths_remain_under_200_characters(self):
        run, result = self.run_fixture(cycles=1)
        cfg = load(run / "config.json")
        durable_root = Path("C:/Dev/miniReason/runs") / cfg["run_id"]
        actual_files = [path for path in run.rglob("*") if path.is_file()]
        self.assertTrue(actual_files)
        lengths = [{"relative": str(path.relative_to(run)),
                    "actual": len(str(path.resolve())),
                    "default_runs": len(str(durable_root / path.relative_to(run)))}
                   for path in actual_files]
        write(self.case / "PATHS.json", json.dumps(lengths, indent=2) + "\n")
        for entry in lengths:
            self.assertLess(entry["actual"], 200, entry)
            self.assertLess(entry["default_runs"], 200, entry)

    def test_unsafe_long_output_path_is_refused_before_creation(self):
        output = self.case / ("long-" * 30)
        with self.assertRaises(ValueError) as caught:
            self.new_run(out=output)
        self.assertIn("PATH_TOO_LONG", str(caught.exception))
        self.assertFalse(output.exists())
        self.assertEqual(self.counter.offline, 0)

    def test_every_recipe_runs_offline_and_rival_is_delivered(self):
        for recipe in ("single-family", "cross-family", "cross-family-rival"):
            with self.subTest(recipe=recipe):
                run = self.new_run(recipe=recipe, cycles=1, out=self.case / recipe)
                result = engine.execute(run, scripted=scripted_reply)
                self.assertEqual(result["stop_reason"], "cycle_budget")
                seats = load(run / "recipe.json")["seats"]
                rival = run / "calls" / "c0001-rival" / "a00" / "response.json"
                self.assertEqual(rival.exists(), bool(seats["rival"]))
                if seats["rival"]:
                    answer = load(rival)["parsed"]["answer"]
                    request = load(run / "calls" / "c0001-return" / "a00" / "request.json")
                    self.assertIn(answer, request["prepared"]["messages"][1]["content"])

    def test_request_and_response_epochs_and_provider_custody(self):
        run, result = self.run_fixture(cycles=1)
        for request_path in run.glob("calls/*/a*/request.json"):
            request = load(request_path)
            response = load(request_path.parent / "response.json")
            self.assertIsInstance(request["epoch"], (float, int))
            self.assertIsInstance(response["epoch"], (float, int))
            self.assertLessEqual(request["epoch"], response["epoch"])
            prepared = request["prepared"]
            self.assertEqual(prepared["wall_seconds"], 300)
            self.assertEqual(prepared["kwargs"]["max_tokens"], 8192)
            expected = hashlib.sha256(prepared["wire_body_text"].encode("utf-8")).hexdigest()
            self.assertEqual(prepared["wire_body_sha256"], expected)
            provider_request = load(request_path.parent / "provider" / "call-0001.request.json")
            self.assertEqual(provider_request["wire_body_sha256"], expected)
        self.assertIn("working answer with its objections, not a finding", read(run / "RUN.md"))

    def test_mixed_missing_keys_refuses_all_seats_before_calls(self):
        with mock.patch.dict(os.environ, {"DEEPSEEK_API_KEY": "fixture-placeholder-key"}, clear=True):
            run = self.new_run(mode="live")
            result = engine.execute(run)
        self.assertEqual(result["stop_reason"], "KEY_MISSING")
        self.assertEqual(result["calls"], 0)
        self.assertEqual(self.counter.live, 0)
        self.assertEqual(self.counter.offline, 0)
        self.assertFalse((run / "calls").exists())

    def test_critic_siblings_receive_identical_prior_context(self):
        run, result = self.run_fixture(cycles=2)
        for cycle in (1, 2):
            first = load(run / "calls" / f"c{cycle:04d}-k01" / "a00" / "request.json")
            second = load(run / "calls" / f"c{cycle:04d}-k02" / "a00" / "request.json")
            self.assertEqual(first["prepared"]["messages"], second["prepared"]["messages"])
            context = first["prepared"]["messages"][1]["content"]
            self.assertNotIn(f"Cycle {cycle}: the boundary case is unstated.", context)
            if cycle == 2:
                self.assertIn("Cycle 1: the boundary case is unstated.", context)

    def test_baseline_bare_and_native_receive_identical_prompt(self):
        run, result = self.run_fixture(cycles=1, baseline=True)
        bare = load(run / "calls" / "base-bare" / "a00" / "request.json")["prepared"]
        native = load(run / "calls" / "base-native" / "a00" / "request.json")["prepared"]
        self.assertEqual(bare["messages"], native["messages"])
        self.assertEqual(bare["kwargs"]["max_tokens"], native["kwargs"]["max_tokens"])
        self.assertIs(bare["kwargs"]["thinking"], False)
        self.assertIs(native["kwargs"]["thinking"], True)
        record = load(run / "calls" / "base-native" / "a00" / "provider" / "call-0001.response.json")
        self.assertIs(record["reasoning_content_present"], True)
        self.assertIs(record["reasoning_content_persisted"], False)
        self.assertNotIn("reasoning_content", record)

    def test_mock_worker_wall_terminates_and_records_without_retry(self):
        from minireason.reason import adapter, prompts
        import subprocess
        child = mock.MagicMock()
        child.wait.side_effect = [subprocess.TimeoutExpired("offline-mocked-worker", 300), None]
        records = self.case / "wall"
        with mock.patch.dict(os.environ, {"DEEPSEEK_API_KEY": "fixture-placeholder-key"}, clear=True):
            with mock.patch.object(adapter.subprocess, "Popen", return_value=child) as popen:
                with self.assertRaises(ReasonFailure) as caught:
                    adapter.Adapter("live").call(
                        seat="deepseek-flash", messages=prompts.render("conjecture", "A small problem."),
                        records_dir=records)
        self.assertEqual(caught.exception.code, "TRANSPORT_OR_RESPONSE_ERROR")
        popen.assert_called_once()
        child.kill.assert_called_once()
        self.assertLessEqual(child.wait.call_args_list[0].kwargs["timeout"], 300)
        saved = load(records / "worker-failure.json")
        self.assertEqual(saved["code"], "TRANSPORT_OR_RESPONSE_ERROR")
        self.assertEqual(self.counter.live, 0)
        self.assertEqual(self.counter.opened, 0)

    def test_provider_terminal_response_recovers_before_outer_response_write(self):
        class Interrupted(BaseException):
            pass
        original = engine.Adapter.call
        interrupted = []
        def persist_then_interrupt(adapter, **kwargs):
            result = original(adapter, **kwargs)
            if not interrupted:
                interrupted.append(True)
                raise Interrupted()
            return result
        run = self.new_run(cycles=1)
        with mock.patch.object(engine.Adapter, "call", persist_then_interrupt):
            with self.assertRaises(Interrupted):
                engine.execute(run, scripted=scripted_reply)
        initial = run / "calls" / "initial" / "a00"
        self.assertTrue((initial / "provider" / "call-0001.response.json").exists())
        self.assertFalse((initial / "response.json").exists())
        original_response = read(initial / "provider" / "call-0001.response.json")
        self.assertEqual(self.counter.offline, 1)
        result = engine.execute(run, scripted=scripted_reply)
        self.assertEqual(result["stop_reason"], "cycle_budget")
        self.assertEqual(self.counter.offline, result["calls"])
        self.assertEqual(read(initial / "provider" / "call-0001.response.json"), original_response)
        self.assertTrue((initial / "response.json").exists())

    def test_corrupt_outer_response_refuses_replay_with_run_summary(self):
        class Interrupted(BaseException):
            pass
        def stop(call_id, response):
            if call_id == "initial":
                raise Interrupted()
        run = self.new_run(cycles=1)
        with self.assertRaises(Interrupted):
            engine.execute(run, scripted=scripted_reply, after_call=stop)
        response = run / "calls" / "initial" / "a00" / "response.json"
        write(self.case / "original-response.json", read(response))
        write(response, '{"incomplete":')
        before = self.counter.offline
        result = engine.execute(run, scripted=scripted_reply)
        self.assertEqual(result["stop_reason"], "RUN_INTEGRITY_ERROR")
        self.assertEqual(self.counter.offline, before)
        self.assertIn("RUN_INTEGRITY_ERROR", read(run / "RUN.md"))

    def test_default_three_cycle_baseline_completed_run_resumes_successfully(self):
        run = self.new_run(cycles=3, baseline=True)
        first = engine.execute(run)
        self.assertEqual(first["stop_reason"], "cycle_budget")
        self.assertEqual(first["completed_cycles"], 3)
        self.assertEqual(first["calls"], 15)
        originals = {str(path.relative_to(run)): read(path)
                     for path in (run / "calls").rglob("*") if path.is_file()}
        self.assertTrue(originals)
        counter = self.counter.offline
        resumed = engine.execute(run)
        self.assertEqual(resumed["stop_reason"], "cycle_budget")
        self.assertEqual(resumed["completed_cycles"], 3)
        self.assertEqual(resumed["calls"], 15)
        self.assertEqual(self.counter.offline, counter)
        self.assertEqual(set(originals),
                         {str(path.relative_to(run)) for path in (run / "calls").rglob("*")
                          if path.is_file()})
        for path, original in originals.items():
            self.assertEqual(read(run / path), original, path)


if __name__ == "__main__":
    unittest.main()
