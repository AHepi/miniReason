"""R003 occurrence-1 offline fixture through launcher, CLI and shared engine."""
from __future__ import annotations
from contextlib import redirect_stdout, redirect_stderr
from copy import deepcopy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import unittest
import uuid
from unittest.mock import patch

from minireason.reason import engine, r002

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "experiments/diagnostics/R003-open-problems-trial-series"

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

launcher = module("w28_occurrence_launcher", STUDY / "run_R003.py")
cli = module("w28_occurrence_cli", ROOT / "tools/reason.py")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def tree(path):
    return {p.relative_to(path).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob("*") if p.is_file()}


class OpenFixture:
    """Deliberately fallible prose; shape validation supplies no answer oracle."""
    invalid_prose = "OFFLINE FIXTURE: a counterexample disputes the premise; format this unchanged."

    def __init__(self, *, repair=True, plan_length=3):
        self.repair = repair
        self.plan_length = plan_length
        self.calls = []

    @staticmethod
    def answer():
        text = "OFFLINE FIXTURE: preserve the competing account pending a discriminating observation."
        return {"decision": "answered", "answer": text, "missing_derivation": "",
                "claims": [{"relation_id": "working_position", "value": text, "quote": text}],
                "derivation_steps": [{"step_index": 1, "statement": text, "depends_on": []}]}

    @staticmethod
    def step(number):
        return {"step": number, "derivation": f"OFFLINE FIXTURE prose argument {number}.",
                "result": f"provisional result {number}", "cannot_decide": None}

    def __call__(self, *, role, cycle, objections, coordinate, context):
        self.calls.append((role, deepcopy(coordinate)))
        if role == "answer" or role == "decomposed_synthesis":
            return self.answer()
        if role == "initial_decompose":
            first = self.step(1)
            first.pop("cannot_decide")
            return {"plan": [{"step": i, "goal": f"Examine premise {i}",
                    "depends_on": [i-1] if i > 1 else []} for i in range(1, self.plan_length+1)],
                    "first_step": first, "cannot_decide": None}
        if role == "decomposed_step":
            return self.step(context["expected_step"]["step"])
        if role in {"prose_critic", "decomposed_critic"}:
            if (self.repair and role == "prose_critic" and cycle == 1
                    and coordinate["call_id"].endswith("signal-a") and coordinate["attempt"] == 0):
                return {"content": self.invalid_prose}
            step = context["answer"]["derivation_steps"][0]
            item = {"target_claim": "working_position", "text": "The premise may omit an alternative account.",
                    "defeats": "working_position", "fork": {"step_index": step["step_index"],
                    "step_quote": step["statement"], "branch_point_id": f"participant-step-{step['step_index']}",
                    "earliest_reason": "This participant step first commits to the disputed premise."}}
            if role == "decomposed_critic":
                item["check"] = {"check_id": coordinate["call_id"] + "-counterexample",
                    "kind": "derivation_step", "inputs": [{"name": "premise", "value": step["statement"],
                    "source": "participant step"}], "procedure": "Consider a rival account with the same observation.",
                    "claimed_result": "The rival could also fit.", "falsifies_when": "An independent reason rules out this rival."}
            return {"decision": "answered", "missing_derivation": "", "working": "OFFLINE prose fixture",
                    "objections": [item]}
        if role == "prose_return":
            answer = self.answer()
            return {**answer, "changes": [], "dispositions": [{"id": obj["id"],
                    "status": "unresolved", "reason": "The rival remains open.",
                    "rederivation": {"objection_id": obj["id"], "from_step_index": None,
                    "status": "retained", "steps": [], "missing_derivation": ""}} for obj in objections]}
        if role == "propagation_use":
            text = self.answer()["answer"]
            return {"decision": "answered", "missing_derivation": "", "query_id": f"use-{cycle}",
                    "question": "Should the current proposal be relied on for the later decision?",
                    "problem_derivation": "This later decision relies on the disputed premise.",
                    "before": {"answer_quote": text, "derivation": "The rival remains open.", "conclusion": "defer"},
                    "after": {"answer_quote": text, "derivation": "The rival still remains open.", "conclusion": "defer"},
                    "dependency": {"relation_id": "working_position", "before_quote": text, "after_quote": text,
                        "result_depends_on_change": False, "explanation": "No revision has settled the rival."},
                    "objections": [], "checker": None}
        if role == "decomposed_return":
            before = context["before"]
            return {"decision": "answered", "missing_derivation": "", "step": before["step"],
                    "derivation": before["derivation"], "result": before["result"],
                    "dispositions": [{"id": obj["id"], "status": "rejected-with-reason",
                    "reason": "The rival omits the condition stated in this step.", "redo": {
                    "check_id": obj["check"]["check_id"], "status": "redone",
                    "method": "Reconsidered the counterexample in the stated scope.",
                    "result": before["result"], "comparison": "opposes_objection"}} for obj in objections]}
        if role == "decomposed_use":
            number = context["expected_step"]["step"]
            return {"decision": "answered", "missing_derivation": "", "step": number,
                    "status": "agrees", "method": "Applied the provisional distinction to a later prose decision.",
                    "result": self.step(number)["result"]}
        if role == "decomposed_closing":
            return {**self.answer(), "dispositions": [{"id": obj["id"],
                    "status": "rejected-with-reason", "reason": "The earlier scope objection remains answered."}
                    for obj in objections if obj.get("status") == "unresolved"]}
        raise AssertionError(role)


class R003OccurrenceIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.series = Path(os.environ.get("MINIREASON_TEST_WORK", "C:/tr28")) / "occ" / uuid.uuid4().hex[:8]

    def dispatch(self, command, **kwargs):
        self.assertIn("--study-profile", command)
        self.assertEqual(command[command.index("--study-profile")+1], "r003-open-v1")
        self.assertEqual(command[command.index("--mode")+1], "offline")
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(command[command.index(str(ROOT / "tools/reason.py"))+1:])
        return subprocess.CompletedProcess(command, code, out.getvalue(), err.getvalue())

    def test_two_problem_three_condition_matrix_repair_closure_resume_and_path_bound(self):
        fixture = OpenFixture()
        directory = launcher.create(self.series, ["O01", "O02"], list(launcher.CONDITIONS),
            "Do these offline fixtures preserve the declared occurrence-1 instruments?", "offline",
            env_file=ROOT / "work/w28/never-read.env")
        with (patch.object(launcher.subprocess, "run", side_effect=self.dispatch),
              patch.object(engine, "execute_r002", side_effect=lambda directory, **kw:
                  r002.execute_r002(directory, scripted=fixture, **kw)),
              patch.object(cli, "load_env_file", side_effect=AssertionError("dotenv accessed offline")),
              patch("socket.socket.connect", side_effect=AssertionError("network accessed offline"))):
            result = launcher.execute(directory)
        self.assertEqual(result.get("failed", 0), 0, result)
        self.assertEqual(len(launcher.verify(directory)["matrix"]), 6)
        for problem in ("O01", "O02"):
            for alias, expected in (("n", (1, 1)), ("x", (14, 15)), ("d", (14, 14))):
                run = directory / "r" / problem / alias
                state = load(run / "state.json")
                self.assertEqual((state["calls"], state["attempts"]), expected, state)
                self.assertEqual(state["checker_runs"], 0)
                self.assertEqual(state["stall_switches"], 0)
                self.assertEqual(load(run / "config.json")["study_profile"], "r003-open-v1")
                self.assertTrue((run / "RUN.md").read_text(encoding="utf-8").startswith("# R003 run\n"))
                self.assertTrue((run / "TRACE.md").read_text(encoding="utf-8").startswith("# R003 objection trace\n"))
                if alias != "n":
                    self.assertEqual(state["completed_cycles"], 3)
                    self.assertEqual(state["closing_return"], "complete")
                if alias == "d":
                    self.assertEqual([s["step"] for s in state["accepted_steps"]], [1, 2, 3])
                    self.assertTrue((run / "calls/closing-return/a00/request.json").exists())
                for path in run.rglob("*"):
                    if path.is_file():
                        projected = Path("C:/Dev/miniReason/runs/r3/o001") / path.relative_to(directory)
                        self.assertLess(len(str(projected)), 200, str(projected))
            run = directory / "r" / problem / "x"
            a0 = load(run / "calls/c0001-signal-a/a00/request.json")
            a1 = load(run / "calls/c0001-signal-a/a01/request.json")
            self.assertEqual(a0["seat"], a1["seat"])
            self.assertEqual(a0["prepared"]["kwargs"]["max_tokens"], 16384)
            self.assertEqual(a1["prepared"]["kwargs"]["max_tokens"], 16384)
            self.assertIn(OpenFixture.invalid_prose, a1["prepared"]["messages"][1]["content"])
            self.assertFalse((run / "calls/c0001-signal-a/a02").exists())
        before = tree(directory)
        with patch.object(launcher.subprocess, "run", side_effect=AssertionError("terminal cell replayed")):
            self.assertEqual(launcher.execute(directory).get("failed", 0), 0)
        self.assertEqual(before, tree(directory))


    def execute_fixture(self, directory, fixture):
        with (patch.object(launcher.subprocess, "run", side_effect=self.dispatch),
              patch.object(engine, "execute_r002", side_effect=lambda directory, **kw:
                  r002.execute_r002(directory, scripted=fixture, **kw)),
              patch.object(cli, "load_env_file", side_effect=AssertionError("dotenv accessed offline")),
              patch("socket.socket.connect", side_effect=AssertionError("network accessed offline"))):
            return launcher.execute(directory)

    def test_native_failure_has_no_repair_and_only_failed_successor_is_new(self):
        original = launcher.create(self.series, ["O01"], ["NATIVE"],
            "Does a native schema failure remain a single immutable attempt?", "offline")
        result = self.execute_fixture(original, lambda **kw: {"content": "Unformatted public answer."})
        self.assertEqual(result["failed"], 1)
        state = load(original / "r/O01/n/state.json")
        self.assertEqual((state["stop_reason"], state["calls"], state["attempts"]),
                         ("SCHEMA_FAILURE", 1, 1))
        self.assertFalse((original / "r/O01/n/calls/initial/a01").exists())
        before = tree(original)
        with patch.object(launcher.subprocess, "run", side_effect=AssertionError("failed cell replayed")):
            self.assertEqual(launcher.execute(original)["failed"], 1)
        successor = launcher.rerun(original,
            "Can the separately declared successor deliver a shaped fixture?",
            "Offline fixture repair of delivery only; original evidence is preserved.", "offline")
        self.assertEqual(successor.name, "o002")
        self.assertEqual(launcher.verify(successor)["parent"], str(original))
        self.assertEqual(self.execute_fixture(successor, OpenFixture())["failed"], 0)
        self.assertEqual(before, tree(original))

    def test_semantic_partial_and_zero_cycle_terminals_are_delivered_not_rerun_failures(self):
        for expected in ("step_budget", "step_unresolved", "initial_cannot_decide"):
            with self.subTest(expected=expected):
                directory = launcher.create(self.series, ["O01"], ["LOOP-DECOMPOSED"],
                    "Is the declared semantic terminal preserved as a delivered partial outcome?", "offline")
                normal = OpenFixture(plan_length=4 if expected == "step_budget" else 3)
                def reply(**context):
                    if expected == "initial_cannot_decide" and context["role"] == "initial_decompose":
                        return {"plan": [], "first_step": None,
                                "cannot_decide": {"missing": "No warranted bounded plan is available."}}
                    if (expected == "step_unresolved" and context["role"] == "decomposed_step"
                            and context["cycle"] == 2):
                        return {"step": 2, "derivation": "", "result": "",
                                "cannot_decide": {"missing": "The next premise remains disputed."}}
                    return normal(**context)
                self.assertEqual(self.execute_fixture(directory, reply)["failed"], 0)
                state = load(directory / "r/O01/d/state.json")
                self.assertEqual(state["stop_reason"], expected)
                if expected == "initial_cannot_decide":
                    self.assertEqual(state["completed_cycles"], 0)
                    self.assertFalse((directory / "r/O01/d/calls/closing-return").exists())
                else:
                    self.assertEqual(state["closing_return"], "complete")
                    self.assertFalse((directory / "r/O01/d/calls/synthesis").exists())
                with self.assertRaisesRegex(launcher.Refused, "NO_KNOWN_FAILED_CELLS"):
                    launcher.rerun(directory, "Is any delivery failure available?", "fixture", "offline")


if __name__ == "__main__":
    unittest.main()
