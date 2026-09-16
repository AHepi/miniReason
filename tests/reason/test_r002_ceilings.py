"""A ceiling is a preserved unavailable result, never an empty critic list."""
import json
from pathlib import Path
import unittest
import uuid
from tests.reason import artifact_root
from minireason.reason.config import R002_DIR
from minireason.reason.engine import create_r002_native_run, create_r002_run, execute_r002
from minireason.reason.storage import read, get


class R002CeilingTests(unittest.TestCase):
    def setUp(self):
        self.out = artifact_root() / "ceil" / uuid.uuid4().hex[:8]
        self.common = {"problem_id": "C01", "relation_registry": R002_DIR / "problems/RELATIONS.json"}
        self.problem = read(R002_DIR / "problems/C01.txt")

    @staticmethod
    def ceiling(tokens):
        return {"content": "", "finish_reason": "length",
                "usage": {"prompt_tokens": 10, "completion_tokens": tokens, "total_tokens": tokens + 10}}

    def test_calibration_native_ceiling_is_one_preserved_unanswered_attempt(self):
        run = create_r002_native_run(self.problem, self.out, condition="CAL-NATIVE", **self.common)
        state = execute_r002(run, scripted=lambda **context: self.ceiling(32768))
        self.assertEqual(state["stop_reason"], "CEILING_HIT")
        self.assertEqual(state["calls"], 1)
        self.assertEqual(state["usage"]["completion_tokens"], 32768)
        self.assertIsNone(state["answer"])
        self.assertIn("No public answer", read(run / "ANSWER.md"))
        self.assertEqual(len(list((run / "calls/initial").glob("a*"))), 1)

    def test_critic_ceiling_is_fatal_censored_and_never_empty_objections(self):
        run = create_r002_run(self.problem, "r002-tested-cross-v1", self.out,
            fork_registry=R002_DIR / "problems/FORKS.json",
            coding_manifest=R002_DIR / "problems/RECODING_MAPS.json", **self.common)
        def response(**context):
            if context["role"] == "answer":
                return {"decision": "cannot_decide", "answer": "", "missing_derivation": "Fixture lacks derivation",
                        "claims": [], "derivation_steps": []}
            return self.ceiling(16384)
        state = execute_r002(run, scripted=response)
        self.assertEqual(state["stop_reason"], "CEILING_HIT")
        self.assertEqual(state["calls"], 2)
        self.assertEqual(state["completed_cycles"], 0)
        self.assertEqual(state["closing_return"], "not-run")
        failed = get(run / "calls/c0001-signal-a/a00/response.json")
        self.assertEqual(failed["status"], "CEILING_HIT")
        self.assertNotIn("parsed", failed)
        intent = get(run / "calls/c0001-signal-a/a00/request.json")
        self.assertEqual(intent["prepared"]["kwargs"]["max_tokens"], 16384)
        self.assertEqual(len(list((run / "calls/c0001-signal-a").glob("a*"))), 1)
