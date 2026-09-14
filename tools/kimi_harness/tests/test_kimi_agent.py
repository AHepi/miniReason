"""Offline tests for the kimi-k3 worker harness. No network, no credential.

Run:  python3 -m unittest discover -s kimi/tests -t kimi
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import kimi_agent as ka  # noqa: E402


# --------------------------------------------------------------------------
# Fakes
# --------------------------------------------------------------------------


def response(content="", tool_calls=None, finish_reason="stop", prompt=10, completion=20,
             reasoning="") -> ka.ChatResponse:
    body = {
        "id": "chatcmpl-fake", "model": "kimi-k3",
        "choices": [{"index": 0, "finish_reason": finish_reason, "message": {
            "role": "assistant", "content": content,
            "reasoning": reasoning,
            **({"tool_calls": tool_calls} if tool_calls else {})}}],
        "usage": {"prompt_tokens": prompt, "completion_tokens": completion,
                  "total_tokens": prompt + completion},
    }
    return ka.normalise(body, raw_sha="0" * 64, raw_bytes=len(json.dumps(body)),
                        latency_ms=5, request_sha="1" * 64, request_bytes=100,
                        http_status=200)


def tool_call(name, arguments, call_id="call_1"):
    text = arguments if isinstance(arguments, str) else json.dumps(arguments)
    return {"id": call_id, "type": "function",
            "function": {"name": name, "arguments": text}}


class FakeTransport:
    """Replays scripted :class:`ChatResponse` objects and records what it was sent."""

    def __init__(self, script):
        self.script = list(script)
        self.calls: list[dict] = []

    def chat(self, messages, **kwargs):
        self.calls.append({"messages": [dict(m) for m in messages], "kwargs": kwargs})
        if not self.script:
            raise AssertionError("fake transport script exhausted")
        item = self.script.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.repo = self.tmp / "repo"
        (self.repo / "pkg").mkdir(parents=True)
        (self.repo / "pkg" / "hello.py").write_text("def hello():\n    return 'hi'\n", encoding="utf-8")
        (self.repo / ".env").write_text("OLLAMA_API_KEY=sk-not-a-real-key-0123456789\n", encoding="utf-8")
        self.runs = self.tmp / "runs"
        self.addCleanup(self._tmp.cleanup)

    def spec(self, **overrides):
        data = dict(id="t-001", title="Test task", prompt="Do the thing.",
                    context_paths=("pkg",), expected_outputs=("pkg/hello.py",),
                    repo_root=str(self.repo), max_iterations=5)
        data.update(overrides)
        return ka.TaskSpec(**data)

    def transcript_events(self, task_id="t-001"):
        path = self.runs / task_id / "transcript.jsonl"
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


# --------------------------------------------------------------------------
# Sandbox confinement
# --------------------------------------------------------------------------


class SandboxTests(Base):
    def test_populate_copies_declared_paths_only(self):
        sandbox = ka.Sandbox(self.tmp / "sb1")
        sandbox.populate(self.repo, ["pkg"])
        self.assertTrue((sandbox.root / "pkg" / "hello.py").is_file())
        self.assertEqual(sorted(sandbox.snapshot()), ["pkg/hello.py"])

    def test_env_file_is_never_copied(self):
        (self.repo / "pkg" / ".env").write_text("OLLAMA_API_KEY=leak\n", encoding="utf-8")
        sandbox = ka.Sandbox(self.tmp / "sb2")
        sandbox.populate(self.repo, ["pkg"])
        self.assertFalse((sandbox.root / "pkg" / ".env").exists())
        with self.assertRaises(ka.HarnessFailure):
            ka.Sandbox(self.tmp / "sb3").populate(self.repo, [".env"])

    def test_absolute_and_parent_paths_are_refused(self):
        sandbox = ka.Sandbox(self.tmp / "sb4")
        for bad in ["/etc/passwd", "../outside.txt", "pkg/../../outside.txt"]:
            with self.assertRaises(ka.HarnessFailure) as caught:
                sandbox.resolve(bad)
            self.assertEqual(caught.exception.code, "PATH_REFUSED")

    def test_context_path_must_be_repo_relative(self):
        sandbox = ka.Sandbox(self.tmp / "sb5")
        with self.assertRaises(ka.HarnessFailure) as caught:
            sandbox.populate(self.repo, ["/etc"])
        self.assertEqual(caught.exception.code, "CONTEXT_PATH_REFUSED")

    def test_diff_reports_added_and_modified_with_sha256(self):
        sandbox = ka.Sandbox(self.tmp / "sb6")
        sandbox.populate(self.repo, ["pkg"])
        before = sandbox.snapshot()
        (sandbox.root / "pkg" / "new.py").write_text("x = 1\n", encoding="utf-8")
        (sandbox.root / "pkg" / "hello.py").write_text("def hello():\n    return 'yo'\n", encoding="utf-8")
        changes = {entry["path"]: entry for entry in sandbox.diff(before)}
        self.assertEqual(changes["pkg/new.py"]["change"], "added")
        self.assertEqual(changes["pkg/hello.py"]["change"], "modified")
        self.assertEqual(len(changes["pkg/new.py"]["sha256"]), 64)


# --------------------------------------------------------------------------
# Tool dispatch and the allow-list
# --------------------------------------------------------------------------


class ToolTests(Base):
    def box(self):
        sandbox = ka.Sandbox(self.tmp / "tools")
        sandbox.populate(self.repo, ["pkg"])
        return ka.ToolBox(sandbox)

    def test_read_list_grep_write(self):
        box = self.box()
        self.assertIn("def hello", box.dispatch("read_file", {"path": "pkg/hello.py"}))
        self.assertIn("pkg/hello.py", box.dispatch("list_dir", {"path": "pkg"}))
        self.assertIn("pkg/hello.py:1", box.dispatch("grep", {"pattern": "def hello", "path": "."}))
        self.assertIn("wrote pkg/new.py", box.dispatch("write_file",
                                                       {"path": "pkg/new.py", "content": "x = 1\n"}))
        self.assertEqual((box.sandbox.root / "pkg" / "new.py").read_text(), "x = 1\n")
        self.assertEqual(box.counts["read_file"], 1)
        self.assertEqual(box.files_written, ["pkg/new.py"])

    def test_write_outside_the_sandbox_is_refused(self):
        box = self.box()
        out = box.dispatch("write_file", {"path": "../escaped.py", "content": "boom"})
        self.assertTrue(out.startswith("ERROR: PATH_REFUSED"))
        self.assertFalse((self.tmp / "escaped.py").exists())
        out = box.dispatch("read_file", {"path": "/etc/passwd"})
        self.assertTrue(out.startswith("ERROR: PATH_REFUSED"))

    def test_unknown_tool_is_reported_not_raised(self):
        self.assertTrue(self.box().dispatch("rm_rf", {"path": "/"}).startswith("ERROR: unknown tool"))

    def test_bad_arguments_are_reported_not_raised(self):
        self.assertTrue(self.box().dispatch("read_file", {"wrong": 1}).startswith("ERROR: BAD_ARGUMENTS"))

    def test_allow_list_accepts_only_the_four_shapes(self):
        for good in ["python3 -m unittest discover", "python3 -m pytest -q",
                     "python3 -c 'print(1)'", "python3 pkg/hello.py"]:
            self.assertEqual(ka.check_command(good)[0], "python3")
        for bad in ["rm -rf /", "bash -c 'ls'", "python2 foo.py", "python3 -m pip install x",
                    "python3 --version", "", "python3 -m http.server"]:
            with self.assertRaises(ka.HarnessFailure, msg=bad) as caught:
                ka.check_command(bad)
            self.assertEqual(caught.exception.code, "COMMAND_REFUSED")

    def test_run_command_executes_inside_the_sandbox(self):
        box = self.box()
        out = box.dispatch("run_command", {"command": "python3 -c 'import os;print(os.getcwd())'"})
        self.assertIn("exit_code: 0", out)
        self.assertIn(str(box.sandbox.root), out)

    def test_run_command_refuses_anything_off_the_allow_list(self):
        self.assertTrue(self.box().dispatch(
            "run_command", {"command": "rm -rf ."}).startswith("ERROR: COMMAND_REFUSED"))

    def test_run_command_subprocess_cannot_see_the_credential(self):
        import os
        os.environ["OLLAMA_API_KEY"] = "sk-fake-value-for-this-test-only"
        self.addCleanup(os.environ.pop, "OLLAMA_API_KEY", None)
        out = self.box().dispatch(
            "run_command", {"command": "python3 -c 'import os;print(\"KEY=\"+str(os.environ.get(\"OLLAMA_API_KEY\")))'"})
        self.assertIn("KEY=None", out)

    def test_run_command_times_out(self):
        box = self.box()
        box.command_timeout = 1
        out = box.dispatch("run_command", {"command": "python3 -c 'import time;time.sleep(30)'"})
        self.assertTrue(out.startswith("ERROR: TIMEOUT"))

    def test_run_command_output_is_capped(self):
        box = self.box()
        box.output_cap = 200
        out = box.dispatch("run_command", {"command": "python3 -c 'print(\"a\"*10000)'"})
        self.assertLess(len(out), 600)
        self.assertIn("truncated", out)


# --------------------------------------------------------------------------
# Redaction
# --------------------------------------------------------------------------


class RedactionTests(unittest.TestCase):
    def test_key_and_prefix_are_replaced_raw_and_json_escaped(self):
        key = "sk-abcdefghijklmnopqrstuvwxyz-0123456789"
        redactor = ka.Redactor([key])
        self.assertNotIn(key, redactor.scrub(f"Authorization: Bearer {key}"))
        self.assertIn(ka.REDACTION, redactor.scrub(f"prefix only {key[:12]} here"))
        blob = json.dumps({"note": f"the key is {key}"})
        self.assertNotIn(key[:12], redactor.scrub(blob))
        self.assertTrue(redactor.clean("nothing to see"))
        self.assertFalse(redactor.clean(key[:12]))

    def test_short_values_are_not_treated_as_secrets(self):
        redactor = ka.Redactor(["abc"])
        self.assertEqual(redactor.scrub("abc def"), "abc def")

    def test_transcript_lines_are_redacted(self):
        key = "sk-zyxwvutsrqponmlkjihgfedcba-9876543210"
        redactor = ka.Redactor([key])
        with tempfile.TemporaryDirectory() as tmp:
            transcript = ka.Transcript(Path(tmp) / "t.jsonl", redactor)
            transcript.write("response", content=f"I found {key} in the file")
            text = (Path(tmp) / "t.jsonl").read_text(encoding="utf-8")
            self.assertNotIn(key, text)
            self.assertNotIn(key[:12], text)
            self.assertIn(ka.REDACTION, text)

    def test_a_credential_in_the_outgoing_payload_is_refused(self):
        key = "sk-payload-check-key-abcdefghijklmnop"
        redactor = ka.Redactor([key])
        client = ka.KimiClient.__new__(ka.KimiClient)
        client.redactor = redactor
        with self.assertRaises(ka.HarnessFailure) as caught:
            client.refuse_credential_in_request({"messages": [{"content": f"use {key}"}]})
        self.assertEqual(caught.exception.code, "SECRET_IN_REQUEST")

    def test_reasoning_text_is_never_carried_on_the_response(self):
        reply = response(content="done", reasoning="secret chain of thought" * 10)
        self.assertTrue(reply.reasoning_present)
        self.assertEqual(len(reply.reasoning_sha256), 64)
        self.assertNotIn("chain of thought", json.dumps(reply.__dict__, default=str))


# --------------------------------------------------------------------------
# The loop
# --------------------------------------------------------------------------


class LoopTests(Base):
    def test_tool_dispatch_round_trip_and_transcript_shape(self):
        transport = FakeTransport([
            response(tool_calls=[tool_call("read_file", {"path": "pkg/hello.py"})],
                     finish_reason="tool_calls", reasoning="thinking hard"),
            response(tool_calls=[tool_call("write_file",
                                           {"path": "pkg/hello.py", "content": "def hello():\n    return 'yo'\n"},
                                           call_id="call_2")], finish_reason="tool_calls"),
            response(tool_calls=[tool_call("run_command", {"command": "python3 -c 'print(1)'"},
                                           call_id="call_3")], finish_reason="tool_calls"),
            response(content="Rewrote pkg/hello.py and ran the check.", finish_reason="stop"),
        ])
        result = ka.run_task(self.spec(), transport=transport, runs_dir=self.runs)
        self.assertEqual(result.status, "COMPLETE")
        self.assertEqual(result.iterations, 4)
        self.assertEqual(result.tool_call_total, 3)
        self.assertEqual(result.tool_calls,
                         {"read_file": 1, "write_file": 1, "run_command": 1})
        self.assertEqual(result.total_tokens, 4 * 30)
        self.assertEqual([entry["path"] for entry in result.files_written], ["pkg/hello.py"])
        self.assertEqual(result.files_written[0]["change"], "modified")
        self.assertGreater(result.wall_seconds, 0)

        events = self.transcript_events()
        kinds = [event["event"] for event in events]
        self.assertEqual(kinds[0], "task_start")
        self.assertEqual(kinds[-1], "task_end")
        self.assertEqual(kinds.count("request"), 4)
        self.assertEqual(kinds.count("response"), 4)
        self.assertEqual(kinds.count("tool_call"), 3)
        self.assertEqual(kinds.count("tool_result"), 3)
        first_response = next(e for e in events if e["event"] == "response")
        self.assertTrue(first_response["reasoning_content_present"])
        self.assertEqual(len(first_response["reasoning_content_sha256"]), 64)
        self.assertFalse(first_response["reasoning_content_persisted"])
        self.assertNotIn("thinking hard", (self.runs / "t-001" / "transcript.jsonl").read_text())
        self.assertIn("usage", first_response)
        self.assertIn("latency_ms", first_response)
        self.assertEqual(first_response["finish_reason"], "tool_calls")
        # The tool schemas really were sent, and the tool reply really was fed back.
        self.assertEqual([t["function"]["name"] for t in transport.calls[0]["kwargs"]["tools"]],
                         list(ka.TOOL_NAMES))
        self.assertEqual(transport.calls[1]["messages"][-1]["role"], "tool")
        self.assertEqual(transport.calls[1]["messages"][-2]["role"], "assistant")
        self.assertTrue((self.runs / "t-001" / "result.json").is_file())

    def test_sandbox_escape_attempt_by_the_model_is_refused_and_recorded(self):
        transport = FakeTransport([
            response(tool_calls=[tool_call("write_file", {"path": "../../escape.py", "content": "boom"})],
                     finish_reason="tool_calls"),
            response(content="I could not escape.", finish_reason="stop"),
        ])
        result = ka.run_task(self.spec(), transport=transport, runs_dir=self.runs)
        self.assertEqual(result.status, "COMPLETE")
        self.assertEqual(result.files_written, [])
        self.assertFalse((self.runs / "escape.py").exists())
        tool_result = next(e for e in self.transcript_events() if e["event"] == "tool_result")
        self.assertFalse(tool_result["ok"])
        self.assertIn("PATH_REFUSED", tool_result["output"])

    def test_iteration_cap_stops_the_loop(self):
        script = [response(tool_calls=[tool_call("list_dir", {"path": "."}, call_id=f"c{i}")],
                           finish_reason="tool_calls") for i in range(10)]
        transport = FakeTransport(script)
        result = ka.run_task(self.spec(max_iterations=3), transport=transport, runs_dir=self.runs)
        self.assertEqual(result.status, "ITERATION_CAP")
        self.assertEqual(result.harness_failure, "ITERATION_CAP")
        self.assertEqual(result.iterations, 3)
        self.assertEqual(len(transport.calls), 3)

    def test_malformed_tool_call_json_is_retried_exactly_once(self):
        transport = FakeTransport([
            response(tool_calls=[tool_call("read_file", "{not json")], finish_reason="tool_calls"),
            response(tool_calls=[tool_call("read_file", {"path": "pkg/hello.py"})],
                     finish_reason="tool_calls"),
            response(content="Read it.", finish_reason="stop"),
        ])
        result = ka.run_task(self.spec(), transport=transport, runs_dir=self.runs)
        self.assertEqual(result.status, "COMPLETE")
        self.assertEqual(result.malformed_tool_call_retries, 1)
        kinds = [event["event"] for event in self.transcript_events()]
        self.assertEqual(kinds.count("malformed_tool_call"), 1)
        self.assertEqual(kinds.count("retry"), 1)
        # The unusable assistant turn was dropped before the retry.
        self.assertEqual(len(transport.calls[1]["messages"]), 2)

    def test_a_second_malformed_tool_call_fails_the_task(self):
        transport = FakeTransport([
            response(tool_calls=[tool_call("read_file", "{not json")], finish_reason="tool_calls"),
            response(tool_calls=[tool_call("read_file", "still not json")], finish_reason="tool_calls"),
        ])
        result = ka.run_task(self.spec(), transport=transport, runs_dir=self.runs)
        self.assertEqual(result.status, "HARNESS_FAILURE")
        self.assertEqual(result.harness_failure, "MALFORMED_TOOL_CALL_JSON")

    def test_http_error_fails_the_task_without_a_retry(self):
        transport = FakeTransport([ka.HarnessFailure("HTTP_429", "rate limited")])
        result = ka.run_task(self.spec(), transport=transport, runs_dir=self.runs)
        self.assertEqual(result.status, "HARNESS_FAILURE")
        self.assertEqual(result.harness_failure, "HTTP_429")
        self.assertEqual(len(transport.calls), 1)
        self.assertEqual([e["event"] for e in self.transcript_events()][-2], "harness_failure")

    def test_packed_context_mode_writes_fenced_blocks(self):
        body = ("Here is the change.\n\n```path=pkg/hello.py\ndef hello():\n    return 'yo'\n```\n"
                "```path=pkg/test_hello.py\nimport unittest\n```\n")
        transport = FakeTransport([response(content=body, finish_reason="stop")])
        result = ka.run_task(self.spec(mode="packed"), transport=transport, runs_dir=self.runs)
        self.assertEqual(result.status, "COMPLETE")
        self.assertEqual(result.mode, "packed")
        self.assertEqual(sorted(entry["path"] for entry in result.files_written),
                         ["pkg/hello.py", "pkg/test_hello.py"])
        # The declared files really were inlined into the single prompt.
        self.assertIn("def hello():", transport.calls[0]["messages"][1]["content"])

    def test_packed_mode_feeds_failing_test_output_back_for_one_more_turn(self):
        first = ("```path=pkg/m.py\nraise SystemExit(1)\n```")
        second = ("```path=pkg/m.py\nprint('ok')\n```")
        transport = FakeTransport([response(content=first), response(content=second)])
        result = ka.run_task(self.spec(mode="packed", verify_command="python3 pkg/m.py"),
                             transport=transport, runs_dir=self.runs)
        self.assertEqual(len(transport.calls), 2)
        self.assertIn("did not pass", transport.calls[1]["messages"][-1]["content"])
        self.assertEqual(result.iterations, 2)

    def test_a_budget_exhausted_turn_is_incomplete_not_complete(self):
        """finish_reason=length, no tool call, no content: a boundary, not a completion."""
        transport = FakeTransport([
            response(tool_calls=[tool_call("read_file", {"path": "pkg/hello.py"})],
                     finish_reason="tool_calls"),
            response(content="", finish_reason="length", completion=8192,
                     reasoning="reasoning that ate the whole turn " * 40),
        ])
        result = ka.run_task(self.spec(), transport=transport, runs_dir=self.runs)
        self.assertEqual(result.status, "INCOMPLETE_TURN")
        self.assertEqual(result.harness_failure, "TURN_BUDGET_EXHAUSTED_BY_REASONING")
        self.assertEqual(result.finish_reason, "length")
        self.assertEqual(result.iterations, 2)
        self.assertIn("8192 completion tokens", result.harness_detail)

        events = self.transcript_events()
        boundary = next(e for e in events if e["event"] == "incomplete_turn")
        self.assertEqual(boundary["code"], "TURN_BUDGET_EXHAUSTED_BY_REASONING")
        self.assertEqual(boundary["finish_reason"], "length")
        self.assertEqual(boundary["completion_tokens"], 8192)
        self.assertEqual(boundary["iteration"], 2)
        self.assertEqual(len(boundary["reasoning_content_sha256"]), 64)
        self.assertEqual(boundary["reasoning_content_chars"], len("reasoning that ate the whole turn " * 40))
        self.assertGreater(boundary["reasoning_tokens_estimated"], 0)
        self.assertFalse(boundary["reasoning_content_persisted"])
        # The reasoning text itself is still never written down.
        self.assertNotIn("reasoning that ate the whole turn",
                         (self.runs / "t-001" / "transcript.jsonl").read_text(encoding="utf-8"))
        self.assertEqual(json.loads((self.runs / "t-001" / "result.json").read_text())["status"],
                         "INCOMPLETE_TURN")

    def test_a_non_stop_finish_that_still_said_something_is_not_an_incomplete_turn(self):
        transport = FakeTransport([response(content="Partial answer, cut off mid-", finish_reason="length")])
        result = ka.run_task(self.spec(), transport=transport, runs_dir=self.runs)
        self.assertEqual(result.status, "COMPLETE")
        self.assertIsNone(result.harness_failure)
        self.assertEqual([e["event"] for e in self.transcript_events()].count("incomplete_turn"), 0)

    def test_a_stop_that_wrote_no_expected_output_is_no_deliverable(self):
        transport = FakeTransport([response(content="I have analysed it all.", finish_reason="stop")])
        result = ka.run_task(self.spec(expected_outputs=("out/report.md", "probe/")),
                             transport=transport, runs_dir=self.runs)
        self.assertEqual(result.status, "NO_DELIVERABLE")
        self.assertEqual(result.finish_reason, "stop")
        self.assertEqual(result.expected_outputs_present, [])
        self.assertEqual(result.expected_outputs_missing, ["out/report.md", "probe/"])
        self.assertIn("out/report.md", result.harness_detail)
        self.assertEqual(result.files_written, [])
        self.assertEqual(json.loads((self.runs / "t-001" / "result.json").read_text())["status"],
                         "NO_DELIVERABLE")
        end = self.transcript_events()[-1]
        self.assertEqual(end["status"], "NO_DELIVERABLE")
        self.assertEqual(end["expected_outputs_missing"], ["out/report.md", "probe/"])

    def test_complete_survives_only_when_every_expected_output_exists(self):
        def run(script, expected):
            transport = FakeTransport(script)
            return ka.run_task(self.spec(id="t-002", expected_outputs=expected),
                               transport=transport, runs_dir=self.runs)

        write_one = tool_call("write_file", {"path": "out/report.md", "content": "# report\n"})
        write_dir = tool_call("write_file", {"path": "probe/note.md", "content": "note\n"},
                              call_id="call_2")
        # Only one of the two declared outputs written: not a completion.
        partial = run([response(tool_calls=[write_one], finish_reason="tool_calls"),
                       response(content="Done.", finish_reason="stop")],
                      ("out/report.md", "probe/"))
        self.assertEqual(partial.status, "NO_DELIVERABLE")
        self.assertEqual(partial.expected_outputs_present, ["out/report.md"])
        self.assertEqual(partial.expected_outputs_missing, ["probe/"])
        # Both written — including a file inside the declared directory: COMPLETE.
        full = run([response(tool_calls=[write_one], finish_reason="tool_calls"),
                    response(tool_calls=[write_dir], finish_reason="tool_calls"),
                    response(content="Done.", finish_reason="stop")],
                   ("out/report.md", "probe/"))
        self.assertEqual(full.status, "COMPLETE")
        self.assertEqual(full.expected_outputs_missing, [])
        self.assertIsNone(full.harness_failure)

    def test_parse_path_fences(self):
        blocks = ka.parse_path_fences("noise\n```path=a/b.py\nx=1\n```\ntail\n```path=c.txt\nhi\n```")
        self.assertEqual(blocks, [("a/b.py", "x=1\n"), ("c.txt", "hi\n")])


class ReasoningControlTests(Base):
    """What the probes found, pinned: /v1 honours nothing, native honours ``think``."""

    def client(self, native: bool):
        endpoint = ka.Endpoint(name="test", base_url="https://example.invalid",
                               model="kimi-k3", key_env="TEST_KEY", family="test",
                               chat_path="/api/chat" if native else "/chat/completions",
                               native=native)
        return ka.KimiClient(endpoint, key="not-a-real-key-01234567")

    def test_the_v1_surface_sends_no_reasoning_control_at_all(self):
        client = self.client(native=False)
        self.assertIsNone(client.reasoning_control())
        for setting in ("default", "low", "off", None):
            payload = client.build_payload([{"role": "user", "content": "hi"}], reasoning=setting)
            self.assertNotIn("think", payload)
            self.assertNotIn("reasoning", payload)
            self.assertNotIn("reasoning_effort", payload)

    def test_the_native_surface_sends_think(self):
        client = self.client(native=True)
        self.assertEqual(client.reasoning_control(), "off")
        self.assertEqual(
            client.build_payload([{"role": "user", "content": "hi"}], reasoning="off")["think"],
            False)
        self.assertEqual(
            client.build_payload([{"role": "user", "content": "hi"}], reasoning="low")["think"],
            "low")
        self.assertNotIn("think",
                         client.build_payload([{"role": "user", "content": "hi"}],
                                              reasoning="default"))

    def test_an_incomplete_turn_is_retried_once_at_the_lowest_setting(self):
        class Retryable(FakeTransport):
            def reasoning_control(self):
                return "off"

        transport = Retryable([
            response(content="", finish_reason="length", completion=24576, reasoning="all budget"),
            response(tool_calls=[tool_call("read_file", {"path": "pkg/hello.py"})],
                     finish_reason="tool_calls"),
            response(content="Read it.", finish_reason="stop"),
        ])
        result = ka.run_task(self.spec(reasoning="low"), transport=transport, runs_dir=self.runs)
        self.assertEqual(result.status, "COMPLETE")
        self.assertIsNone(result.harness_failure)
        # The retry re-sent the same turn, once, at the lowest setting.
        self.assertEqual(len(transport.calls), 3)
        self.assertEqual(transport.calls[0]["kwargs"]["reasoning"], "low")
        self.assertEqual(transport.calls[1]["kwargs"]["reasoning"], "off")
        self.assertEqual(transport.calls[0]["messages"], transport.calls[1]["messages"])
        kinds = [event["event"] for event in self.transcript_events()]
        self.assertEqual(kinds.count("incomplete_turn_retry"), 1)
        self.assertEqual(kinds.count("incomplete_turn"), 1)
        retry = next(e for e in self.transcript_events() if e["event"] == "incomplete_turn_retry")
        self.assertEqual(retry["reason"], "TURN_BUDGET_EXHAUSTED_BY_REASONING")
        self.assertEqual((retry["reasoning_from"], retry["reasoning_to"]), ("low", "off"))

    def test_the_retry_happens_at_most_once_and_never_without_a_control(self):
        class Retryable(FakeTransport):
            def reasoning_control(self):
                return "off"

        budget_gone = [response(content="", finish_reason="length", completion=24576,
                                reasoning="all budget") for _ in range(4)]
        retryable = Retryable(list(budget_gone))
        result = ka.run_task(self.spec(), transport=retryable, runs_dir=self.runs)
        self.assertEqual(result.status, "INCOMPLETE_TURN")
        self.assertEqual(result.harness_failure, "TURN_BUDGET_EXHAUSTED_BY_REASONING")
        self.assertEqual(len(retryable.calls), 2)          # one turn, one retry, then stop
        kinds = [e["event"] for e in self.transcript_events()]
        self.assertEqual(kinds.count("incomplete_turn_retry"), 1)

        plain = FakeTransport(list(budget_gone))           # no reasoning_control at all
        result = ka.run_task(self.spec(id="t-003"), transport=plain, runs_dir=self.runs)
        self.assertEqual(result.status, "INCOMPLETE_TURN")
        self.assertEqual(len(plain.calls), 1)
        self.assertEqual([e["event"] for e in self.transcript_events("t-003")]
                         .count("incomplete_turn_retry"), 0)


def native_body(content="", tool_calls=None, done_reason="stop", prompt=10, completion=20,
                thinking=""):
    """One Ollama ``/api/chat`` body, in the shape probe-reasoning-native-tools recorded."""

    message = {"role": "assistant", "content": content, "thinking": thinking}
    if tool_calls:
        message["tool_calls"] = tool_calls
    return {"model": "kimi-k3", "created_at": "2026-09-14T15:04:38Z", "done": True,
            "done_reason": done_reason, "message": message,
            "prompt_eval_count": prompt, "eval_count": completion,
            "prompt_eval_cached_count": 3}


class NativeTransportTests(Base):
    """The translation, both ways, and the one fallback. No network."""

    def client(self, native=True, fallback=False, **kw):
        endpoint = ka.Endpoint(name="test", base_url="https://example.invalid",
                               model="kimi-k3", key_env="TEST_KEY", family="test",
                               chat_path="/api/chat" if native else "/chat/completions",
                               native=native)
        other = ka.Endpoint(name="test-v1", base_url="https://example.invalid",
                            model="kimi-k3", key_env="TEST_KEY", family="test")
        return ka.KimiClient(endpoint, key="not-a-real-key-01234567",
                             fallback_endpoint=other if fallback else None, **kw)

    # -- outbound: internal -> native ---------------------------------------

    def test_messages_are_translated_into_the_native_shape(self):
        internal = [
            {"role": "system", "content": "rules"},
            {"role": "user", "content": "do it"},
            {"role": "assistant", "content": "",
             "tool_calls": [tool_call("read_file", {"path": "pkg/hello.py"}, "call_7")]},
            {"role": "tool", "tool_call_id": "call_7", "name": "read_file", "content": "def hello()"},
        ]
        native = ka.to_native_messages(internal)
        self.assertEqual([m["role"] for m in native], ["system", "user", "assistant", "tool"])
        call = native[2]["tool_calls"][0]
        self.assertEqual(call["id"], "call_7")
        self.assertNotIn("type", call)                       # no /v1 wrapper
        self.assertEqual(call["function"]["name"], "read_file")
        # /v1 sends arguments as a JSON string; native takes an object.
        self.assertEqual(call["function"]["arguments"], {"path": "pkg/hello.py"})
        # A tool reply is addressed by name here, not by tool_call_id.
        self.assertEqual(native[3], {"role": "tool", "tool_name": "read_file",
                                     "content": "def hello()"})

    def test_the_native_payload_carries_the_budget_the_tools_and_think(self):
        client = self.client()
        payload = client.build_native_payload(
            [{"role": "user", "content": "hi"}], tools=ka.TOOL_SCHEMAS,
            tool_choice="auto", max_tokens=24576, reasoning="low")
        self.assertEqual(payload["options"]["num_predict"], 24576)   # not max_tokens
        self.assertEqual(payload["think"], "low")
        self.assertNotIn("tool_choice", payload)                     # no native equivalent
        self.assertEqual([t["function"]["name"] for t in payload["tools"]], list(ka.TOOL_NAMES))
        self.assertIs(client.build_native_payload([{"role": "user", "content": "hi"}],
                                                  reasoning="off")["think"], False)

    # -- inbound: native -> internal ----------------------------------------

    def test_a_native_reply_is_reduced_to_the_same_response_object(self):
        body = native_body(
            tool_calls=[{"id": "call_dlqgdpmd",
                         "function": {"index": 0, "name": "read_file",
                                      "arguments": {"path": "pkg/hello.py"}}}],
            completion=82, thinking="short thought")
        answer = ka.normalise_native(body, raw_sha="0" * 64, raw_bytes=10, latency_ms=5,
                                     request_sha="1" * 64, request_bytes=10, http_status=200)
        self.assertEqual(answer.finish_reason, "stop")               # done_reason
        self.assertEqual(answer.usage["completion_tokens"], 82)      # eval_count
        self.assertEqual(answer.usage["prompt_tokens"], 10)          # prompt_eval_count
        self.assertEqual(answer.usage["total_tokens"], 92)
        self.assertEqual(answer.usage["prompt_tokens_details"]["cached_tokens"], 3)
        self.assertEqual(answer.tool_calls[0]["id"], "call_dlqgdpmd")
        self.assertEqual(answer.tool_calls[0]["type"], "function")   # internal shape restored
        self.assertEqual(answer.tool_calls[0]["function"]["arguments"], {"path": "pkg/hello.py"})
        # Reasoning is hashed and counted here too, and the text is dropped.
        self.assertTrue(answer.reasoning_present)
        self.assertEqual(answer.reasoning_chars, len("short thought"))
        self.assertEqual(len(answer.reasoning_sha256), 64)
        self.assertNotIn("short thought", json.dumps(answer.__dict__, default=str))
        # A truncated native turn reads as a non-stop finish, like /v1's "length".
        self.assertFalse(ka.is_stop_finish(
            ka.normalise_native(native_body(done_reason="length"), raw_sha="0" * 64, raw_bytes=1,
                                latency_ms=1, request_sha="1" * 64, request_bytes=1,
                                http_status=200).finish_reason))

    def test_a_full_native_round_trip_drives_the_loop(self):
        """What the live probe did, offline: call, tool reply, answer."""

        sent: list[dict] = []

        class Wire(ka.KimiClient):
            def _post(self, url, body):
                sent.append(json.loads(body))
                if len(sent) == 1:
                    return (json.dumps(native_body(tool_calls=[
                        {"id": "call_1", "function": {"name": "read_file",
                                                      "arguments": {"path": "pkg/hello.py"}}}]))
                            .encode(), 200)
                return json.dumps(native_body(content="It says hi.")).encode(), 200

        endpoint = ka.Endpoint(name="t", base_url="https://example.invalid", model="kimi-k3",
                               key_env="TEST_KEY", family="test", chat_path="/api/chat",
                               native=True)
        client = Wire(endpoint, key="not-a-real-key-01234567")
        result = ka.run_task(self.spec(), transport=client, runs_dir=self.runs)
        self.assertEqual(result.status, "COMPLETE")
        self.assertEqual(result.transport_used, "native")
        self.assertEqual(result.tool_calls, {"read_file": 1})
        self.assertEqual(result.reasoning_chars, [0, 0])
        # The second request carried the tool reply in native shape.
        self.assertEqual(sent[1]["messages"][-1]["tool_name"], "read_file")
        self.assertEqual(sent[1]["messages"][-2]["tool_calls"][0]["function"]["arguments"],
                         {"path": "pkg/hello.py"})
        self.assertEqual(sent[0]["think"], "low")               # the production default

    # -- the fallback --------------------------------------------------------

    def test_a_native_transport_failure_falls_back_to_v1_once_and_is_recorded(self):
        events: list[tuple] = []
        calls: list[str] = []

        class Flaky(ka.KimiClient):
            def _post(self, url, body):
                calls.append(url)
                if self.endpoint.native:
                    raise ka.HarnessFailure("TRANSPORT_OR_RESPONSE_ERROR", "connection closed")
                return json.dumps({
                    "id": "chatcmpl-1", "model": "kimi-k3",
                    "choices": [{"finish_reason": "stop",
                                 "message": {"role": "assistant", "content": "done"}}],
                    "usage": {"prompt_tokens": 1, "completion_tokens": 1},
                }).encode(), 200

        client = self.client(fallback=True, on_event=lambda name, **kw: events.append((name, kw)))
        client.__class__ = Flaky
        answer = client.chat([{"role": "user", "content": "hi"}], max_tokens=16, reasoning="low")
        self.assertEqual(answer.content, "done")
        self.assertEqual(client.surface, "v1")
        self.assertEqual(client.fallbacks, 1)
        self.assertEqual([url.endswith("/api/chat") for url in calls], [True, False])
        self.assertEqual(events[0][0], "transport_fallback")
        self.assertEqual(events[0][1]["code"], "TRANSPORT_OR_RESPONSE_ERROR")
        self.assertEqual((events[0][1]["from_surface"], events[0][1]["to_surface"]),
                         ("native", "v1"))
        # Having fallen back, it stays fallen back: one switch per run.
        self.assertIsNone(client.fallback_endpoint)
        self.assertIsNone(client.reasoning_control())   # /v1 honours nothing

    def test_the_fallback_is_refused_after_a_tool_call_and_for_a_provider_error(self):
        client = self.client(fallback=True)
        client.tool_calls_seen = True
        self.assertFalse(client._may_fall_back(ka.HarnessFailure("TRANSPORT_OR_RESPONSE_ERROR", "")))
        client.tool_calls_seen = False
        self.assertTrue(client._may_fall_back(ka.HarnessFailure("TRANSPORT_OR_RESPONSE_ERROR", "")))
        # A provider 500 is a failure of the run, not evidence against the surface.
        self.assertFalse(client._may_fall_back(ka.HarnessFailure("HTTP_500", "")))
        self.assertFalse(self.client(fallback=False)._may_fall_back(
            ka.HarnessFailure("TRANSPORT_OR_RESPONSE_ERROR", "")))

    def test_a_task_can_pin_the_v1_surface(self):
        spec = ka.TaskSpec.from_mapping({"id": "x", "title": "t", "prompt": "p",
                                         "transport": "v1"})
        self.assertEqual(spec.transport, "v1")
        self.assertEqual(ka.TaskSpec.from_mapping({"id": "x", "title": "t",
                                                   "prompt": "p"}).transport, "native")
        with self.assertRaises(ka.HarnessFailure) as caught:
            ka.TaskSpec.from_mapping({"id": "x", "title": "t", "prompt": "p",
                                      "transport": "grpc"})
        self.assertEqual(caught.exception.code, "TASK_SPEC_INVALID")


class ConcurrencyTests(unittest.TestCase):
    def test_the_key_ceiling_is_eight_and_a_conflict_is_refused(self):
        ka._reset_slot_registry()
        self.addCleanup(ka._reset_slot_registry)
        semaphore = ka.slots_for("TEST_KEY_ENV")
        self.assertEqual(semaphore._initial_value, 8)
        self.assertIs(ka.slots_for("TEST_KEY_ENV"), semaphore)
        with self.assertRaises(ka.HarnessFailure) as caught:
            ka.slots_for("TEST_KEY_ENV", 5)
        self.assertEqual(caught.exception.code, "CONCURRENCY_LIMIT_CONFLICT")

    def test_max_concurrency_is_eight(self):
        self.assertEqual(ka.MAX_CONCURRENCY, 8)
        self.assertEqual(ka.MAX_TOKENS, 24576)   # the 300 s wall, not the model's ceiling
        self.assertEqual(ka.TIMEOUT_SECONDS, 600)


class TaskSpecTests(unittest.TestCase):
    def test_reasoning_must_be_a_known_setting(self):
        spec = ka.TaskSpec.from_mapping({"id": "x", "title": "t", "prompt": "p",
                                         "reasoning": "off"})
        self.assertEqual(spec.reasoning, "off")
        with self.assertRaises(ka.HarnessFailure) as caught:
            ka.TaskSpec.from_mapping({"id": "x", "title": "t", "prompt": "p",
                                      "reasoning": "medium-ish"})
        self.assertEqual(caught.exception.code, "TASK_SPEC_INVALID")

    def test_unknown_fields_are_refused(self):
        with self.assertRaises(ka.HarnessFailure):
            ka.TaskSpec.from_mapping({"id": "x", "title": "t", "prompt": "p", "nonsense": 1})

    def test_from_mapping_tuples_the_sequences(self):
        spec = ka.TaskSpec.from_mapping({"id": "x", "title": "t", "prompt": "p",
                                         "context_paths": ["a", "b"]})
        self.assertEqual(spec.context_paths, ("a", "b"))
        self.assertEqual(spec.max_iterations, 40)
        self.assertEqual(spec.max_tokens, 24576)
        self.assertEqual(spec.reasoning, "low")   # production default


if __name__ == "__main__":
    unittest.main()
