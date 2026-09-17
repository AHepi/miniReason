"""P-A5 replays immutable attempt-3 public bytes through corrected host paths."""
from copy import deepcopy
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from minireason import provider_openai_compat as provider
from minireason.pilot import __main__ as cli
from minireason.pilot.pilot import Pilot, tool_schema
from minireason.pilot.templates import normalize_inputs, validate_inputs
from .test_worker_recovery import scripted_content, user_packet, complete

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).parent / "fixtures/live-20260917"


def live(label, call, attempt="a00"):
    return (FIXTURES / f"{label}-attempt3-{call}-{attempt}.response-body.json").read_bytes().decode("utf-8")


def task(label):
    path = next((ROOT / "research/deepseek-flash-pilot/usecases").glob(label + "-*/task.json"))
    return json.loads(path.read_bytes())


class Attempt3MultipassTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=os.environ["TMP"], prefix="pa5-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        patch = mock.patch.object(provider, "_open", side_effect=AssertionError("NETWORK_FORBIDDEN"))
        patch.start()
        self.addCleanup(patch.stop)

    def pilot(self, label, scripted):
        return Pilot(task(label), self.root / label, scripted=scripted, repo_root=ROOT)

    def test_live_uc1_uc4_bad_input_namespace_receives_valid_id_repair(self):
        for label, call, attempt in [("UC1", "c0010", "a01"), ("UC4", "c0007", "a00")]:
            with self.subTest(label=label):
                seen, holder = [], {}
                raw = live(label, call, attempt)
                def scripted(**ctx):
                    seen.append(ctx)
                    if ctx["role"] == "plan":
                        if ctx["attempt"] == 0:
                            return scripted_content(raw)
                        ref = deepcopy(holder["pilot"].input_ref)
                        ref["overrides"] = {"task": "Extract one bounded decisive contribution for the parent objective."}
                        return scripted_content({"steps": [{"id": "leaf", "template_id": "direct_answer", "inputs": ref, "depends_on": []}]})
                    if ctx["role"] == "direct_answer":
                        return scripted_content(complete("Recorded bounded fixture contribution"))
                    raise AssertionError(ctx["role"])
                pilot = self.pilot(label, scripted)
                holder["pilot"] = pilot
                pilot.critics = []
                result = pilot.execute_template("decompose_synthesize", pilot.inputs, 1)
                self.assertEqual(result["status"], "partial")
                repair = next(ctx for ctx in seen if ctx["role"] == "plan" and ctx["attempt"] == 1)
                self.assertEqual(repair["messages"][-2]["content"], raw)
                self.assertIn("valid IDs", repair["messages"][-1]["content"])
                self.assertIn(pilot.input_ref["unit_id"], repair["messages"][-1]["content"])
                self.assertIn("reference_menu", user_packet(repair["messages"]))
                self.assertEqual([r["status"] for r in pilot.calls.receipts[:2]], ["contract_rejected", "accepted"])
                self.assertEqual(pilot.calls.receipts[0]["call_id"], pilot.calls.receipts[1]["call_id"])
                stored = json.loads((pilot.root / "calls/c0001/a00/provider/call-0001.response.json").read_bytes())
                self.assertEqual(stored["content"].encode("utf-8"), raw.encode("utf-8"))

    def test_live_uc3_repeated_unsupported_leaf_gets_three_repairs_then_host_split(self):
        raw = live("UC3", "c0010")
        seen = []
        def scripted(**ctx):
            seen.append(ctx)
            if ctx["role"] == "plan":
                return scripted_content(raw)
            if ctx["role"] == "direct_answer":
                value = complete("Exact bounded-range contribution")
                value.update(status="partial", unresolved=["Boundary dependency requires synthesis"])
                return scripted_content(value)
            raise AssertionError(ctx["role"])
        pilot = self.pilot("UC3", scripted)
        pilot.critics = []
        result = pilot.execute_template("decompose_synthesize", pilot.inputs, 1)
        self.assertEqual(result["status"], "partial")
        plans = [ctx for ctx in seen if ctx["role"] == "plan"]
        self.assertEqual(len(plans), 4)
        for index, ctx in enumerate(plans[1:], 1):
            repair = ctx["messages"][-1]["content"]
            self.assertIn("PLAN_NEEDS_BOUNDED_LEAF", repair)
            self.assertIn("host_fallback_leaf_bytes", repair)
            self.assertIn("4096", repair)
            self.assertIn("unit_sizes", repair)
            self.assertEqual(ctx["messages"][-2]["content"], raw)
            self.assertIn(f"schema repair {index} of 3", repair)
        action = next(e["evidence"] for e in pilot.events if e["choice"] == "host-plan-split")
        self.assertEqual(action["origin"], "host")
        ranges = action["ranges"]
        self.assertEqual(ranges[0]["start"], 0)
        self.assertEqual(ranges[-1]["end"], action["parent_range"]["end"])
        self.assertTrue(all(0 < r["end"]-r["start"] <= 4096 for r in ranges))
        self.assertTrue(all(a["end"] == b["start"] for a,b in zip(ranges, ranges[1:])))
        self.assertEqual(len(pilot.spawn_host._results), len(ranges))
        self.assertTrue(all(r["output_status"] == "partial" for r in pilot.spawn_host._results.values()))

    def test_live_uc2_partial_reaches_real_verification_and_two_decisions(self):
        raw = live("UC2", "c0003")
        seen, holder = [], {}
        def scripted(**ctx):
            packet = user_packet(ctx["messages"])
            seen.append((ctx["role"], packet))
            if ctx["role"] == "route":
                return scripted_content({"template_id": "evidence_read", "reason": "Read the supplied story evidence."})
            if ctx["role"] == "spawn":
                ref = deepcopy(holder["pilot"].input_ref)
                if packet["pass_number"] > 1:
                    ref["overrides"] = {"premises": [*holder["pilot"].inputs["premises"], "Re-examine the partial commitments for the second pass."]}
                return scripted_content({"subtasks": [{"template_id": "evidence_read", "inputs": ref}]})
            if ctx["role"] == "evidence_read":
                return scripted_content(raw)
            if ctx["role"] == "continue_or_stop":
                self.assertEqual(packet["artifact"]["status"], "partial")
                self.assertIn("Partial dependency c", "\n".join(packet["artifact"]["unresolved"]))
                self.assertNotEqual(packet["verification"]["kind"], "host-refusal")
                return scripted_content({"decision": "continue" if packet["pass_number"] == 1 else "stop",
                    "reason": packet["verification"]["verification_ref"] + " records the executed verification of the partial story artefact; unresolved commitments remain.",
                    "what_changes_next": "Re-spawn evidence_read with a changed premise requesting re-examination of partial commitments." if packet["pass_number"] == 1 else "",
                    "stop_rule": "Stop after the second fixture verification; no live capability claim."})
            raise AssertionError(ctx["role"])
        pilot = self.pilot("UC2", scripted)
        holder["pilot"] = pilot
        result = pilot.run()
        self.assertEqual(result["status"], "partial", result["detail"])
        self.assertTrue(result["readable_outcome"])
        self.assertEqual(len(result["passes"]), 2)
        self.assertEqual([p["continuation_decisions"][0]["decision"] for p in result["passes"]], ["continue", "stop"])
        self.assertEqual(result["logical_calls"], 8)
        self.assertIn("readable outcome, not a run failure", (pilot.root / "RUN.md").read_text(encoding="utf-8"))
        for role, packet in seen:
            self.assertIn("reference_menu", packet)
        second_route = [p for r,p in seen if r == "route"][1]
        menu = json.dumps(second_route["reference_menu"])
        self.assertIn("c0001", menu)
        self.assertIn(result["passes"][0]["assembled"]["artifact_ref"], menu)
        self.assertIn(result["passes"][0]["verification"]["verification_ref"], menu)
        self.assertTrue((pilot.root / "passes/p0001/verification/result.json").is_file())

    def test_current_task_files_load_and_validate(self):
        for label in ["UC1", "UC2", "UC3", "UC4"]:
            pilot = self.pilot(label, [])
            template = "direct_answer" if label == "UC1" else "evidence_read"
            validate_inputs(template, pilot.inputs)
            self.assertEqual(pilot.task_inputs.expand_inputs(pilot.input_ref, "test"), pilot.inputs)

    def test_cli_partial_with_decision_is_readable_and_env_file_is_never_loaded(self):
        task_path = self.root / "task.json"
        with task_path.open("w", encoding="utf-8", newline="") as f:
            json.dump({"task": "fixture"}, f)
        seed = self.root / "seed.json"
        with seed.open("w", encoding="utf-8", newline="") as f:
            f.write("[]")
        args = ["run", "--task", str(task_path), "--scripted", str(seed), "--out", str(self.root / "cli")]
        with mock.patch.object(cli, "Pilot") as constructor, redirect_stdout(io.StringIO()):
            constructor.return_value.run.return_value = {"status": "partial", "readable_outcome": True}
            self.assertEqual(cli.main(args), 0)
            constructor.return_value.run.return_value = {"status": "partial", "readable_outcome": False}
            self.assertEqual(cli.main(args), 2)
        with mock.patch.object(cli, "Pilot") as constructor, redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(args + ["--env-file", str(self.root / "forbidden-env")]), 2)
            constructor.assert_not_called()


if __name__ == "__main__":
    unittest.main()
