"""Offline end-to-end R002 engine tests; no provider, network, or dotenv access."""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import unittest
import uuid

from minireason.reason import engine
from minireason.reason.r002 import bind_checker_execution
from minireason.reason.storage import put
from minireason.reason.types import ReasonFailure


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "experiments/diagnostics/R002-episodes-under-calibrated-difficulty"
from tests.reason import artifact_root
WORK = artifact_root() / "r2e" / uuid.uuid4().hex[:6]


class FakeChecker:
    def __init__(self, comparison="disagrees"):
        self.comparison = comparison
        self.calls = []

    def run(self, proposal_bytes, policy, evidence_dir):
        proposal = json.loads(bytes(proposal_bytes).decode("utf-8"))
        self.calls.append((proposal, policy, Path(evidence_dir)))
        return self.record(proposal_bytes, policy, self.comparison)

    @staticmethod
    def record(proposal_bytes, policy, comparison="disagrees"):
        proposal = json.loads(bytes(proposal_bytes).decode("utf-8"))
        value = "9/10" if comparison == "disagrees" else proposal["working_value"]
        stdout = json.dumps({"relation_id": proposal["relation_id"], "value": value,
                             "derivation": "OFFLINE FIXTURE host computation"})
        return {"schema": "minireason.r002.checker-execution.v1",
                "proposal_sha256": hashlib.sha256(bytes(proposal_bytes)).hexdigest(),
                "policy_sha256": hashlib.sha256((json.dumps(policy, ensure_ascii=False, sort_keys=True,
                    separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")).hexdigest(),
                "sandbox_backend": "offline-test-fixture", "runtime_identity": "python-3.11-test",
                "runtime_sha256": "a" * 64, "source_sha256": hashlib.sha256(proposal["source"].encode("utf-8")).hexdigest(),
                "stdin_sha256": hashlib.sha256((json.dumps(proposal["stdin_json"], ensure_ascii=False,
                    sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")).hexdigest(),
                "started_utc": "2026-09-17T00:00:00Z", "elapsed_ms": 1, "status": "COMPLETE",
                "limit_breaches": [], "exit_code": 0, "stdout_utf8": stdout, "stderr_utf8": "",
                "comparison": comparison, "parsed": {"relation_id": proposal["relation_id"],
                "value": value, "derivation": "OFFLINE FIXTURE host computation"},
                "stdout_sha256": hashlib.sha256(stdout.encode("utf-8")).hexdigest()}


class R002EngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        WORK.mkdir(parents=True)
        cls.problem = (SPEC / "problems/C01.txt").read_text(encoding="utf-8")

    def setUp(self):
        self.case = WORK / hashlib.sha256(self._testMethodName.encode("utf-8")).hexdigest()[:6]
        self.case.mkdir(parents=True)

    def answer(self, red="2/3"):
        first = "C01.posterior_C = 1/2."
        second = f"C01.next_red = {red}."
        return {"decision": "answered", "answer": first + " " + second,
                "missing_derivation": "",
                "claims": [{"relation_id": "C01.posterior_C", "value": "1/2", "quote": first},
                           {"relation_id": "C01.next_red", "value": red, "quote": second}],
                "derivation_steps": [{"step_index": 1, "statement": first, "depends_on": []},
                                     {"step_index": 2, "statement": second, "depends_on": [1]}]}

    def proposal(self, answer):
        claim = answer["claims"][0]
        return {"query_id": "C01-use", "question": "What is the posterior?",
                "relation_id": claim["relation_id"], "working_claim_quote": claim["quote"],
                "working_value": claim["value"], "language": "python-3.11-restricted",
                "source": "import json\nprint(json.dumps({'relation_id':'C01.posterior_C','value':'1/2','derivation':'fixture'}))",
                "stdin_json": {},
                "expected_output_schema": {"relation_id": "string", "value": "json", "derivation": "string"}}

    def scripted(self, *, tail=False):
        def reply(role, cycle, objections, coordinate, context):
            if role == "answer":
                return self.answer()
            if role in {"tested_critic", "prose_critic"}:
                item = {"target_claim": "C01.next_red", "text": "The final conditional value is disputed.",
                        "defeats": "C01.next_red",
                        "fork": {"step_index": 2, "step_quote": context["answer"]["derivation_steps"][1]["statement"],
                                 "branch_point_id": "C01-fork", "earliest_reason": "This is the first public step asserting it."}}
                if role == "tested_critic":
                    item["check"] = {"check_id": coordinate["call_id"] + "-check", "kind": "value",
                                     "inputs": [{"name": "draw", "value": 4, "source": "problem"}],
                                     "procedure": "Enumerate the conditional draw.", "claimed_result": "2/3",
                                     "falsifies_when": "Enumeration produces the working value."}
                return {"decision": "answered", "missing_derivation": "", "working": "bounded fixture", "objections": [item]}
            if role in {"tested_return", "prose_return"}:
                before = context["before"]
                changed = tail and cycle == 1 and coordinate["call_id"] != "closing-return"
                after = self.answer("3/4") if changed else deepcopy(before)
                dispositions = []
                for obj in objections:
                    take = changed and obj["fork"]["step_index"] == 2
                    item = {"id": obj["id"], "status": "taken-up" if take else "unresolved",
                            "reason": "OFFLINE FIXTURE rederived" if take else "OFFLINE FIXTURE remains open",
                            "rederivation": {"from_step_index": 2 if take else None,
                                             "objection_id": obj["id"],
                                             "status": "rederived" if take else "retained",
                                             "steps": [after["derivation_steps"][1]] if take else [],
                                             "missing_derivation": ""}}
                    if role == "tested_return":
                        item["redo"] = {"check_id": obj["check"]["check_id"], "status": "redone",
                                        "method": "OFFLINE FIXTURE enumeration", "result": obj["check"]["claimed_result"],
                                        "comparison": "supports_objection" if take else "inconclusive"}
                    dispositions.append(item)
                return {**after, "dispositions": dispositions,
                        "changes": ([{"relation_id": "C01.next_red", "before_quote": before["claims"][1]["quote"],
                                      "after_quote": after["claims"][1]["quote"], "changed": True,
                                      "direction": "toward_objection"}] if changed else [])}
            if role == "propagation_use":
                before, after = context["before"], context["answer"]
                changed = before["claims"] != after["claims"]
                index = 1 if changed else 0
                b, a = before["claims"][index], after["claims"][index]
                proposal = self.proposal(after)
                proposal.update(relation_id=a["relation_id"], working_claim_quote=a["quote"],
                                working_value=a["value"])
                return {"decision": "answered", "missing_derivation": "", "query_id": "C01-use",
                        "question": "What is the posterior?", "problem_derivation": "OFFLINE FIXTURE derivation",
                        "before": {"answer_quote": b["quote"], "derivation": "from before", "conclusion": b["value"]},
                        "after": {"answer_quote": a["quote"], "derivation": "from after", "conclusion": a["value"]},
                        "dependency": {"relation_id": a["relation_id"], "before_quote": b["quote"],
                                       "after_quote": a["quote"], "result_depends_on_change": changed,
                                       "explanation": "The selected relation follows the recorded change." if changed else "The selected relation is retained."},
                        "objections": [], "checker": proposal}
            if role == "blind_coding_solve":
                coding_id = context["coding_id"]
                red = "3/4" if coding_id.endswith(("recoded", "carrier")) else "2/3"
                answer = self.answer(red)
                return {"decision": "answered", "missing_derivation": "", "coding_id": coding_id,
                        "claims": [{"relation_id": c["relation_id"], "value": c["value"],
                                    "support": c["quote"]} for c in answer["claims"]],
                        "derivation": "OFFLINE FIXTURE coded derivation",
                        "derivation_steps": answer["derivation_steps"]}
            if role in {"native_match_note", "native_match_synthesis"}:
                return {"decision": "answered", "missing_derivation": "",
                        "answer": "OFFLINE FIXTURE direct note", "derivation": "OFFLINE FIXTURE derivation"}
            raise AssertionError(role)
        return reply

    def new_loop(self, recipe, *, out=None):
        short = hashlib.sha256(recipe.encode("utf-8")).hexdigest()[:5]
        return engine.create_r002_run(
            self.problem, SPEC / "recipes" / recipe, out or self.case / short,
            mode="offline", problem_id="C01", relation_registry=SPEC / "problems/RELATIONS.json",
            fork_registry=SPEC / "problems/FORKS.json",
            coding_manifest=SPEC / "problems/RECODING_MAPS.json")

    def test_native_fixture_is_one_strict_call_and_resumes_byte_identically(self):
        run = engine.create_r002_native_run(
            self.problem, self.case / "native", mode="offline", problem_id="C01",
            schema_path=SPEC / "contracts/answer.schema.json",
            relation_registry=SPEC / "problems/RELATIONS.json")
        state = engine.execute_r002(run)
        self.assertEqual((state["stop_reason"], state["calls"], state["attempts"]), ("complete", 1, 1))
        original = {p.relative_to(run): p.read_bytes() for p in run.rglob("*") if p.is_file()}
        resumed = engine.execute_r002(run)
        self.assertEqual(resumed, state)
        self.assertEqual(original, {p.relative_to(run): p.read_bytes() for p in run.rglob("*") if p.is_file()})

    def test_every_recipe_runs_maximum_fourteen_calls_and_declared_switch(self):
        recipes = ["r002-cross-v2.json", "r002-tested-cross-v1.json", "r002-recoded-v1.json",
                   "r002-checker-v1.json", "r002-carrier-v1.json", "r002-cross-match-v1.json",
                   "r002-native-match-v1.json"]
        for name in recipes:
            with self.subTest(recipe=name):
                runner = FakeChecker()
                run = self.new_loop(name)
                state = engine.execute_r002(run, scripted=self.scripted(), checker_runner=runner)
                self.assertEqual(state["stop_reason"], "cycle_budget", state.get("detail"))
                self.assertEqual(state["calls"], 14)
                self.assertEqual(state["attempts"], 14)
                if name == "r002-native-match-v1.json":
                    self.assertEqual(state["stall_switches"], 0)
                else:
                    self.assertEqual(state["stall_switches"], 1)
                expected_checker = 3 if name == "r002-checker-v1.json" else 0
                self.assertEqual(state["checker_runs"], expected_checker)
                self.assertEqual(len(runner.calls), expected_checker)
                self.assertIn("Calls/attempts: 14/14", (run / "RUN.md").read_text(encoding="utf-8"))

    def test_blind_recoding_prompt_excludes_working_answer_and_history(self):
        run = self.new_loop("r002-recoded-v1.json")
        state = engine.execute_r002(run, scripted=self.scripted())
        self.assertEqual(state["stop_reason"], "cycle_budget")
        request = json.loads((run / "calls/c0001-signal-a/a00/request.json").read_text(encoding="utf-8"))
        text = request["prepared"]["messages"][1]["content"]
        self.assertNotIn("WORKING ANSWER", text)
        self.assertNotIn("PRIOR OBJECTIONS", text)
        self.assertNotIn("OFFLINE FIXTURE remains open", text)
        self.assertIn("CODED PROBLEM", text)
        self.assertIn("RESPONSE SCHEMA recoding-solve.schema.json", text)
        self.assertIn("RESPONSE SCHEMA DEPENDENCY answer.schema.json", text)

    def test_requests_supply_exact_schema_branches_and_sanitized_task_mode(self):
        run = self.new_loop("r002-tested-cross-v1.json")
        state = engine.execute_r002(run, scripted=self.scripted())
        self.assertEqual(state["stop_reason"], "cycle_budget", state.get("detail"))
        def content(call_id):
            request = json.loads((run / "calls" / call_id / "a00/request.json").read_text(encoding="utf-8"))
            return request["prepared"]["messages"][1]["content"]
        initial = content("initial")
        self.assertIn("RESPONSE SCHEMA answer.schema.json", initial)
        self.assertIn('"answered"', initial)
        self.assertIn('"cannot_decide"', initial)
        critic = content("c0001-signal-a")
        self.assertIn("RESPONSE SCHEMA tested-objection.schema.json", critic)
        returned = content("c0001-return")
        self.assertIn("RESPONSE SCHEMA tested-return.schema.json", returned)
        self.assertIn("RESPONSE SCHEMA DEPENDENCY answer.schema.json", returned)
        used = content("c0001-use")
        self.assertIn("RESPONSE SCHEMA propagation-use.schema.json", used)
        self.assertIn("RESPONSE SCHEMA DEPENDENCY checker-proposal.schema.json", used)
        self.assertIn("RESPONSE SCHEMA DEPENDENCY tested-objection.schema.json", used)
        self.assertIn("PUBLIC TASK MODE", used)
        self.assertIn('"checker_eligible":true', used)
        self.assertIn('"oracle_kind":"computable"', used)
        for forbidden in ("trap_label", "answer_path", "oracle_path", "answer_sha256", "trap"):
            self.assertNotIn(forbidden, used)

    def test_tail_edit_is_counted_and_trace_records_check_redo(self):
        run = self.new_loop("r002-tested-cross-v1.json")
        state = engine.execute_r002(run, scripted=self.scripted(tail=True))
        self.assertGreaterEqual(state["tail_edits"], 1)
        trace = (run / "TRACE.md").read_text(encoding="utf-8")
        self.assertIn("Target step: 2", trace)
        self.assertIn("check redone:", trace)
        self.assertTrue(any(entry.get("check_redone") == "agrees"
                            for obj in state["objections"] for entry in obj["history"]))
        self.assertTrue(list((run / "episodes").glob("*/*.json")))

    def test_strict_schema_failure_archives_once_without_repair_or_retry(self):
        run = self.new_loop("r002-tested-cross-v1.json")
        calls = []
        def invalid(**kwargs):
            calls.append(kwargs["coordinate"]["call_id"])
            return {"content": "not json"}
        state = engine.execute_r002(run, scripted=invalid)
        self.assertEqual(state["stop_reason"], "SCHEMA_FAILURE")
        self.assertEqual(calls, ["initial"])
        self.assertFalse((run / "calls/initial/a01").exists())
        again = engine.execute_r002(run, scripted=invalid)
        self.assertEqual(again["stop_reason"], "SCHEMA_FAILURE")
        self.assertEqual(calls, ["initial"])

    def test_checker_rejects_malformed_execution_and_preserves_runner_result(self):
        class Malformed:
            def run(self, *args):
                return {"schema": "minireason.r002.checker-execution.v1", "status": "COMPLETE"}
        run = self.new_loop("r002-checker-v1.json")
        state = engine.execute_r002(run, scripted=self.scripted(), checker_runner=Malformed())
        self.assertEqual(state["stop_reason"], "SCHEMA_FAILURE")
        saved = json.loads((run / "checker/c0001/runner-result.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["status"], "COMPLETE")
        self.assertFalse(any(obj["source"] == "host-checker" for obj in state["objections"]))

    def test_checker_saved_execution_is_recovered_without_second_host_run(self):
        class Interrupted(BaseException):
            pass
        class SaveThenInterrupt:
            def run(self, proposal_bytes, policy, evidence_dir):
                record = FakeChecker.record(proposal_bytes, policy)
                put(Path(evidence_dir) / "execution.json", record)
                raise Interrupted()
        run = self.new_loop("r002-checker-v1.json")
        with self.assertRaises(Interrupted):
            engine.execute_r002(run, scripted=self.scripted(), checker_runner=SaveThenInterrupt())
        resumed_runner = FakeChecker()
        state = engine.execute_r002(run, scripted=self.scripted(), checker_runner=resumed_runner)
        self.assertEqual(state["stop_reason"], "cycle_budget", state.get("detail"))
        self.assertEqual(state["checker_runs"], 3)
        self.assertEqual(len(resumed_runner.calls), 2)

    def test_checker_rejects_schema_valid_runner_receipt_for_wrong_policy(self):
        class WrongPolicy:
            def run(self, proposal_bytes, policy, evidence_dir):
                record = FakeChecker.record(proposal_bytes, policy)
                record["policy_sha256"] = "0" * 64
                return record
        run = self.new_loop("r002-checker-v1.json")
        state = engine.execute_r002(run, scripted=self.scripted(), checker_runner=WrongPolicy())
        self.assertEqual(state["stop_reason"], "RUN_INTEGRITY_ERROR")
        self.assertEqual(state["checker_runs"], 0)
        saved = json.loads((run / "checker/c0001/runner-result.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["policy_sha256"], "0" * 64)
        self.assertFalse(any(obj["source"] == "host-checker" for obj in state["objections"]))

    def test_checker_rejects_stale_saved_execution_before_delivery(self):
        class Interrupted(BaseException):
            pass
        class SaveStaleThenInterrupt:
            def run(self, proposal_bytes, policy, evidence_dir):
                record = FakeChecker.record(proposal_bytes, policy)
                record["proposal_sha256"] = "1" * 64
                put(Path(evidence_dir) / "execution.json", record)
                raise Interrupted()
        run = self.new_loop("r002-checker-v1.json")
        with self.assertRaises(Interrupted):
            engine.execute_r002(run, scripted=self.scripted(), checker_runner=SaveStaleThenInterrupt())
        state = engine.execute_r002(run, scripted=self.scripted(), checker_runner=FakeChecker())
        self.assertEqual(state["stop_reason"], "RUN_INTEGRITY_ERROR")
        self.assertEqual(state["checker_runs"], 0)
        self.assertIn("proposal_sha256", state["stop_detail"])

    def test_checker_binding_covers_all_four_hashes_and_parsed_relation(self):
        proposal = self.proposal(self.answer())
        proposal_bytes = (json.dumps(proposal, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")
        policy = {"policy": "restricted-python-v1", "timeout_seconds": 5,
                  "memory_mib": 256, "stdout_bytes": 65536, "stderr_bytes": 65536,
                  "network": "deny", "filesystem": "isolated-readonly-runtime-and-empty-workdir",
                  "source_bytes": 32768}
        record = FakeChecker.record(proposal_bytes, policy)
        bind_checker_execution(record, proposal_bytes, policy, proposal)
        for field in ("proposal_sha256", "policy_sha256", "source_sha256", "stdin_sha256"):
            altered = deepcopy(record); altered[field] = "f" * 64
            with self.subTest(field=field), self.assertRaises(ReasonFailure) as caught:
                bind_checker_execution(altered, proposal_bytes, policy, proposal)
            self.assertEqual(caught.exception.code, "RUN_INTEGRITY_ERROR")
        altered = deepcopy(record); altered["parsed"]["relation_id"] = "C01.other"
        with self.assertRaises(ReasonFailure) as caught:
            bind_checker_execution(altered, proposal_bytes, policy, proposal)
        self.assertEqual(caught.exception.code, "RUN_INTEGRITY_ERROR")


if __name__ == "__main__":
    unittest.main()
