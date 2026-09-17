from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from minireason.pilot.inputs import InputError, TaskInputs
from minireason.pilot.manifest import TOOLS, validate_tool_args
from minireason.pilot.pilot import Pilot
from minireason.pilot.recording import RecordedCalls
from minireason.pilot.spawn import SpawnHost
from minireason.pilot.templates import OUTPUT_SCHEMA, normalize_inputs
from minireason.reason.types import ReasonFailure


ACTIVE_ROOT = Path(__file__).resolve().parents[2]
TEST_TEMP_ROOT = ACTIVE_ROOT.parent / "t" if ACTIVE_ROOT.name == "staged" else ACTIVE_ROOT / "work" / "w45" / "t"


def complete(answer="42"):
    return {"status":"complete", "answer":answer, "source_refs":[],
            "unresolved":[], "verification_refs":[]}


def read_json(path):
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return json.load(handle)


class InputPortIntegrationTests(unittest.TestCase):
    def setUp(self):
        TEST_TEMP_ROOT.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT, prefix="p-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def test_manifest_accepts_compact_spawn_ref_and_scoped_read(self):
        ref = {"unit_id":"a"*64, "start":0, "end":17, "encoding":"json"}
        packet = {"subtasks":[{"template_id":"direct_answer", "inputs":ref}]}
        self.assertEqual(validate_tool_args("spawn", packet), packet)
        enhanced = {"subtasks":[{"template_id":"direct_answer", "inputs":ref,
                                  "source_reads":[{"unit_id":"b"*64,"start":0,"end":12,"limit":12}]}]}
        self.assertEqual(validate_tool_args("spawn", enhanced), enhanced)
        read = {"unit_id":"b"*64, "start":0, "end":12, "limit":8}
        self.assertEqual(validate_tool_args("read_source", read), read)
        self.assertEqual([item["function"]["name"] for item in TOOLS],
                         ["route","spawn","assemble","read_source","verify","continue_or_stop"])
        with self.assertRaises(ValueError):
            validate_tool_args("spawn", {"subtasks":[{"template_id":"direct_answer", "inputs":{}}]})
        with self.assertRaises(ValueError):
            validate_tool_args("read_source", {**read, "path":"unscoped.txt"})

    def test_spawn_expands_compact_inputs_once_before_validation(self):
        normalized = normalize_inputs("Solve the pinned fixture.")
        store = TaskInputs.from_task({"task":"fixture", "inputs":normalized}, self.root)
        ref = store.compact_inputs(normalized)
        calls = type("CallsStub", (), {"root":self.root / "calls"})()
        host = SpawnHost(calls, input_expander=store.expand_inputs,
                         executor=lambda _template, inputs, _depth: complete(inputs["task"]))
        compact = [{"id":"leaf", "template_id":"direct_answer", "inputs":ref}]
        expanded = host.expand_subtasks(compact, call_id="outer")
        self.assertEqual(expanded[0]["inputs"], normalized)
        self.assertEqual(compact[0]["inputs"], ref)
        result = host.spawn(expanded, receipt="sealed-spawn")
        self.assertEqual(result[0]["output"]["answer"], normalized["task"])
        self.assertTrue(any(item["call_id"] == "outer/leaf" for item in store.receipts))

    def test_full_pilot_control_packets_use_ref_worker_gets_exact_inputs(self):
        task = {
            "task":"What is 6 times 7? Return the integer as plain text.",
            "check":{
                "source":"import json,sys\nx=json.load(sys.stdin)\nprint(json.dumps({'relation_id':'pilot-result','value':x['artifact']['answer']=='42','derivation':'exact fixture'}))\n",
                "expected":True,
                "scope":"The answer is exactly 42.",
                "fixtures":{},
            },
        }
        packets = {}
        def scripted(**context):
            packet = json.loads(context["messages"][-1]["content"])
            packets[context["role"]] = packet
            if context["role"] == "route":
                return {"template_id":"direct_answer", "reason":"Short closed task."}
            if context["role"] == "spawn":
                return {"subtasks":[{"template_id":"direct_answer", "inputs":packet["inputs"]}]}
            if context["role"] == "direct_answer":
                return complete()
            if context["role"] == "continue_or_stop":
                return {"decision":"stop", "reason":packet["verification"]["verification_ref"] + " checker agrees.",
                        "what_changes_next":"", "stop_rule":"Stop when the exact answer is verified."}
            raise AssertionError("unexpected role " + context["role"])
        pilot = Pilot(task, self.root / "run", scripted=scripted, max_calls=4, repo_root=self.root)
        result = pilot.run()
        self.assertEqual((result["status"], result["answer"], result["logical_calls"]), ("complete","42",4))
        self.assertEqual(packets["spawn"]["inputs"], pilot.input_ref)
        self.assertNotIn("documents", packets["spawn"]["inputs"])
        self.assertEqual(packets["direct_answer"]["inputs"], pilot.inputs)
        route_decision = read_json(pilot.root / "calls" / "c0001" / "a00" / "decision.json")
        spawn_decision = read_json(pilot.root / "calls" / "c0002" / "a00" / "decision.json")
        worker_decision = read_json(pilot.root / "calls" / "c0003" / "a00" / "decision.json")
        self.assertEqual(route_decision["source_reads"], [])
        self.assertEqual(spawn_decision["source_reads"], [])
        self.assertTrue(any(item["unit_id"] == pilot.input_ref["unit_id"] for item in worker_decision["source_reads"]))
        self.assertEqual(worker_decision["input_preflight"]["status"], "accepted")
        recorded_spawn = result["passes"][0]["spawned"][0]["inputs"]
        self.assertEqual(set(recorded_spawn), {"unit_id", "start", "end", "encoding"})
        self.assertEqual(pilot.task_inputs.expand_inputs(recorded_spawn, call_id="test-replay"), pilot.inputs)
        spawn_event = next(event for event in pilot.events if event["choice"] == "spawn")
        self.assertEqual(spawn_event["evidence"]["arguments"]["subtasks"][0]["inputs"], recorded_spawn)

    def test_host_read_source_is_pinned_bounded_and_state_preserving(self):
        raw_inputs = json.dumps({"premises":["Pinned premise."]}, ensure_ascii=False,
                                sort_keys=True, separators=(",",":")).encode("utf-8")
        source = "alpha \u03b2eta gamma".encode("utf-8")
        input_path = self.root / "inputs.json"
        source_path = self.root / "source.txt"
        with input_path.open("w", encoding="utf-8", newline="") as handle:
            handle.write(raw_inputs.decode("utf-8"))
        with source_path.open("w", encoding="utf-8", newline="") as handle:
            handle.write(source.decode("utf-8"))
        input_id = hashlib.sha256(raw_inputs).hexdigest()
        source_id = hashlib.sha256(source).hexdigest()
        def card(uid, raw, path, role, media):
            return {"unit_id":uid,"sha256":uid,"byte_count":len(raw),"path":path,
                    "media_type":media,"role":role}
        task = {
            "task":"Read the pinned public source.",
            "inputs":{"unit_id":input_id,"start":0,"end":len(raw_inputs),"encoding":"json"},
            "input_units":[card(input_id,raw_inputs,"inputs.json","task_input","application/json"),
                           card(source_id,source,"source.txt","public_source","text/plain")],
        }
        pilot = Pilot(task, self.root / "read-run", scripted=[], repo_root=self.root)
        call = {"id":"tool-read-1","type":"function","function":{"name":"read_source",
                "arguments":json.dumps({"unit_id":source_id,"start":0,"end":len(source),"limit":7})}}
        result = json.loads(pilot.dispatch(call)["content"])
        self.assertEqual(pilot.state, "SEALED_TASK")
        self.assertEqual(result["result"]["content"], "alpha ")
        receipt = result["result"]["receipt"]
        self.assertEqual(receipt["unit_sha256"], source_id)
        self.assertTrue(receipt["omitted_ranges"])
        self.assertEqual(pilot.dispatch(call)["content"], json.dumps(result, ensure_ascii=False, sort_keys=True, allow_nan=False, separators=(",",":")))
        bad = {"unit_id":"0"*64,"start":0,"end":1,"limit":1}
        with self.assertRaises(InputError):
            pilot.handle_tool("read_source", bad)

    def test_spawn_selected_public_source_is_resolved_into_worker_call(self):
        raw_inputs = b"{}"
        source = b"public auxiliary source"
        input_id = hashlib.sha256(raw_inputs).hexdigest()
        source_id = hashlib.sha256(source).hexdigest()
        with (self.root / "task-input.json").open("w", encoding="utf-8", newline="") as handle:
            handle.write(raw_inputs.decode("utf-8"))
        with (self.root / "public.txt").open("w", encoding="utf-8", newline="") as handle:
            handle.write(source.decode("utf-8"))
        def card(uid, raw, path, role, media):
            return {"unit_id":uid,"sha256":uid,"byte_count":len(raw),"path":path,
                    "media_type":media,"role":role}
        task = {"task":"Return the pinned public source text.",
                "inputs":{"unit_id":input_id,"start":0,"end":len(raw_inputs),"encoding":"json"},
                "input_units":[card(input_id,raw_inputs,"task-input.json","task_input","application/json"),
                               card(source_id,source,"public.txt","public_source","text/plain")],
                "check":{"source":"import json,sys\nx=json.load(sys.stdin)\nprint(json.dumps({'relation_id':'pilot-result','value':x['artifact']['answer']=='public auxiliary source','derivation':'exact source'}))\n",
                         "expected":True,"scope":"Answer equals pinned source.","fixtures":{}}}
        packets = {}
        def scripted(**context):
            packet = json.loads(context["messages"][-1]["content"])
            packets[context["role"]] = packet
            if context["role"] == "route":
                return {"template_id":"direct_answer","reason":"Short source task."}
            if context["role"] == "spawn":
                return {"subtasks":[{"template_id":"direct_answer","inputs":packet["inputs"],
                        "source_reads":[{"unit_id":source_id,"start":0,"end":len(source),"limit":len(source)}]}]}
            if context["role"] == "direct_answer":
                return complete("public auxiliary source")
            if context["role"] == "continue_or_stop":
                return {"decision":"stop","reason":packet["verification"]["verification_ref"] + " checker agrees.",
                        "what_changes_next":"","stop_rule":"Stop after exact source verification."}
            raise AssertionError(context["role"])
        pilot = Pilot(task, self.root / "auto-read", scripted=scripted, max_calls=4, repo_root=self.root)
        result = pilot.run()
        self.assertEqual(result["status"], "complete")
        delivered = packets["direct_answer"]["resolved_source_reads"]
        self.assertEqual(delivered[0]["content"], "public auxiliary source")
        self.assertEqual(delivered[0]["receipt"]["unit_id"], source_id)
        decision = read_json(pilot.root / "calls" / "c0003" / "a00" / "decision.json")
        self.assertTrue(any(item["unit_id"] == source_id for item in decision["source_reads"]))
        self.assertEqual(decision["input_preflight"]["status"], "accepted")

    def test_actual_uc4_spawn_uses_compact_ref_and_validated_pinned_read(self):
        task_path = ACTIVE_ROOT / "research" / "deepseek-flash-pilot" / "usecases" / "UC4-fw5-adversarial-mapping" / "task.json"
        task = read_json(task_path)
        source = next(unit for unit in task["input_units"] if unit["role"] == "public_source")
        request = {"unit_id":source["unit_id"], "start":0,
                   "end":min(source["byte_count"], 256), "limit":256}
        seen = {}
        def scripted(**context):
            seen.update(context)
            packet = json.loads(context["messages"][-1]["content"])
            return {"subtasks":[{"template_id":"evidence_read", "inputs":packet["inputs"],
                                 "source_reads":[request]}]}
        pilot = Pilot(task, self.root / "uc4-run", scripted=scripted, repo_root=ACTIVE_ROOT)
        proposal = pilot.ask("spawn", {"inputs":pilot.input_ref,
                             "input_catalog":pilot.task_inputs.catalog(),
                             "instruction":"Return JSON for one bounded evidence subtask."},
                             next(item["function"]["parameters"] for item in TOOLS
                                  if item["function"]["name"] == "spawn"), max_tokens=2048)
        validated = validate_tool_args("spawn", proposal)
        expanded = pilot.spawn_host.expand_subtasks(validated["subtasks"], call_id="uc4-actual")
        pilot.spawn_host._validate_batch(expanded, 1, "uc4-actual-spawn-receipt")
        self.assertEqual(proposal["subtasks"][0]["inputs"], pilot.input_ref)
        self.assertEqual(expanded[0]["inputs"], pilot.inputs)
        self.assertEqual(expanded[0]["source_reads"], [request])
        decision = read_json(pilot.root / "calls" / "c0001" / "a00" / "decision.json")
        self.assertEqual(decision["input_preflight"]["status"], "accepted")
        self.assertLess(decision["input_preflight"]["total_bound"], 1000000)
        self.assertEqual(seen["role"], "spawn")

    def test_read_specific_source_ref_quotes_only_delivered_range(self):
        raw_inputs = json.dumps({"documents":[{"id":"base","text":"base text"}],
                                 "requested_claims":["quote the source"]},
                                sort_keys=True, separators=(",", ":")).encode("utf-8")
        source = b"inside outside"
        input_id = hashlib.sha256(raw_inputs).hexdigest()
        source_id = hashlib.sha256(source).hexdigest()
        for path, body in (("citation-input.json", raw_inputs), ("citation-source.txt", source)):
            with (self.root / path).open("w", encoding="utf-8", newline="") as handle:
                handle.write(body.decode("utf-8"))
        def card(uid, raw, path, role, media):
            return {"unit_id":uid,"sha256":uid,"byte_count":len(raw),"path":path,
                    "media_type":media,"role":role}
        task = {"task":"Quote only the delivered source range.",
                "inputs":{"unit_id":input_id,"start":0,"end":len(raw_inputs),"encoding":"json"},
                "input_units":[card(input_id,raw_inputs,"citation-input.json","task_input","application/json"),
                               card(source_id,source,"citation-source.txt","public_source","text/plain")]}
        def run_case(quote, run_name):
            holder = {}
            def scripted(**_context):
                source_ref = holder["read"]["receipt"]["source_ref"]
                return {"status":"complete","answer":quote,"source_refs":[source_ref],
                        "unresolved":[],"verification_refs":[],
                        "quotes":[{"claim":"delivered text","source_id":source_ref,
                                   "locator":source_ref,"quote":quote}],
                        "contradictions":[],"not_found":[]}
            pilot = Pilot(task, self.root / run_name, scripted=scripted, repo_root=self.root)
            holder["read"] = pilot.task_inputs.read_source(source_id, start=0, end=6,
                                                            limit=6, call_id=run_name)
            return pilot, holder["read"]
        accepted, delivered = run_case("inside", "quote-ok")
        output = accepted.execute_template("evidence_read", accepted.inputs, 1,
                                           resolved_source_reads=[delivered])
        self.assertEqual(output["source_refs"], [delivered["receipt"]["source_ref"]])
        refused, delivered = run_case("outside", "quote-refused")
        with self.assertRaises(ReasonFailure) as caught:
            refused.execute_template("evidence_read", refused.inputs, 1,
                                     resolved_source_reads=[delivered])
        self.assertEqual(caught.exception.code, "SCHEMA_REJECTED")
        self.assertEqual(refused.calls.count, 4)
        outcomes = [read_json(refused.root / "calls" / "c0001" / attempt / "outcome.json")
                    for attempt in ("a00", "a01", "a02", "a03")]
        self.assertEqual([item["status"] for item in outcomes],
                         ["contract_rejected"] * 4)
        self.assertTrue(all("QUOTE_CUSTODY_FAILURE: quotes[0]" in item["validation_error"]
                            for item in outcomes))
        self.assertTrue(all("quote does not resolve to exact UTF-8 bytes" in item["validation_error"]
                            for item in outcomes))

    def test_nested_plan_uses_refs_and_propagates_source_to_leaf_and_critic(self):
        raw_inputs = b"{}"
        source = b"nested public source"
        input_id = hashlib.sha256(raw_inputs).hexdigest()
        source_id = hashlib.sha256(source).hexdigest()
        with (self.root / "nested-input.json").open("w",encoding="utf-8",newline="") as handle:
            handle.write(raw_inputs.decode("utf-8"))
        with (self.root / "nested-source.txt").open("w",encoding="utf-8",newline="") as handle:
            handle.write(source.decode("utf-8"))
        def card(uid,raw,path,role,media):
            return {"unit_id":uid,"sha256":uid,"byte_count":len(raw),"path":path,"media_type":media,"role":role}
        task={"task":"Decompose a pinned-source question.",
              "inputs":{"unit_id":input_id,"start":0,"end":len(raw_inputs),"encoding":"json"},
              "input_units":[card(input_id,raw_inputs,"nested-input.json","task_input","application/json"),
                             card(source_id,source,"nested-source.txt","public_source","text/plain")],
              "critic_seats":["ollama/qwen3.5-397b.native"]}
        packets={}
        pilot_holder={}
        request={"unit_id":source_id,"start":0,"end":len(source),"limit":len(source)}
        def scripted(**context):
            packet=json.loads(context["messages"][-1]["content"])
            packets[context["role"]]=packet
            pilot=pilot_holder["pilot"]
            if context["role"] == "plan":
                leaf=normalize_inputs("Answer the nested leaf.")
                ref=pilot.task_inputs.compact_inputs(leaf)
                return {"steps":[{"id":"s1","template_id":"direct_answer","inputs":ref,
                                  "source_reads":[request],"depends_on":[]}]}
            if context["role"] == "direct_answer":
                return complete("nested public source")
            if context["role"] == "decompose-critic":
                return {"verdict":"supported","reason":"Pinned source is present.","objections":[]}
            if context["role"] == "synthesis":
                return {**complete("nested public source"),"steps":["s1"],"dependencies":[],"synthesis":"nested public source"}
            raise AssertionError(context["role"])
        pilot=Pilot(task,self.root/"nested-run",scripted=scripted,repo_root=self.root)
        pilot_holder["pilot"]=pilot
        result=pilot.execute_template("decompose_synthesize",pilot.inputs,1)
        self.assertEqual(result["answer"],"nested public source")
        self.assertIn("unit_id",packets["plan"]["inputs"])
        self.assertNotIn("task",packets["plan"]["inputs"])
        self.assertNotIn("resolved_source_reads",packets["plan"])
        self.assertEqual(packets["direct_answer"]["resolved_source_reads"][0]["content"],"nested public source")
        self.assertEqual(packets["decompose-critic"]["resolved_source_reads"][0]["content"],"nested public source")
        self.assertEqual(packets["synthesis"]["resolved_source_reads"][0]["content"],"nested public source")
        self.assertEqual(packets["decompose-critic"]["resolved_source_reads"],packets["synthesis"]["resolved_source_reads"])
        self.assertEqual(pilot.current["nested_spawns"][0]["source_reads"],[request])
        leaf_uid=packets["plan"]["inputs"]["unit_id"]
        self.assertTrue((pilot.root/"input-units"/(leaf_uid+".txt")).is_file())

    def test_template_critic_receives_resolved_source_context(self):
        task={"task":"Criticize the candidate.","inputs":{"candidate":"candidate text",
              "premises":["public premise"],"objections":["possible defect"],
              "protected_obligations":["preserve the task"]},
              "critic_seats":["ollama/qwen3.5-397b.native"]}
        packets={}
        read={"content":"critical public source","receipt":{"schema":"pilot.source-read.pa2.v1",
              "unit_id":"f"*64,"unit_sha256":"f"*64,"start":0,"end":22,"byte_count":22,
              "source_ref":"unit:"+("f"*64)+"@0:22",
              "excerpt_sha256":"f"*64,"omitted_ranges":[]}}
        def scripted(**context):
            packet=json.loads(context["messages"][-1]["content"])
            packets[context["role"]]=packet
            if context["role"] == "template-critic":
                return {"verdict":"supported","reason":"Source supports review.","objections":[]}
            if context["role"] == "return":
                return {**complete("candidate text"),
                        "objections":[{"id":"o0001","target":"candidate text","grounds":"possible defect"}],
                        "dispositions":[{"id":"o0001","status":"rejected-with-reason","reason":"premise supports candidate"}],
                        "revision":"candidate text","dependent_use":""}
            if context["role"] == "use":
                return complete("candidate implication")
            raise AssertionError(context["role"])
        pilot=Pilot(task,self.root/"critic-run",scripted=scripted,repo_root=self.root)
        output=pilot.execute_template("critic_return",pilot.inputs,1,resolved_source_reads=[read])
        self.assertEqual(output["answer"],"candidate text")
        self.assertEqual(packets["template-critic"]["resolved_source_reads"][0]["content"],"critical public source")

    def test_preflight_refuses_before_physical_attempt(self):
        calls = RecordedCalls(self.root / "refusal", scripted=lambda **_context: self.fail("dispatch occurred"))
        refusal = InputError("INPUT_WINDOW_EXCEEDED", "fixture", {"status":"refused"})
        with mock.patch("minireason.pilot.recording.preflight_for_endpoint", side_effect=refusal):
            with self.assertRaises(InputError) as caught:
                calls.call("answer", [{"role":"user","content":"Return json for this small fixture."}], schema=OUTPUT_SCHEMA)
        self.assertEqual(caught.exception.code, "INPUT_WINDOW_EXCEEDED")
        self.assertEqual(calls.count, 0)
        self.assertEqual(calls.logical_count, 1)
        record = read_json(self.root / "refusal" / "calls" / "c0001" / "a00" / "preflight-refusal.json")
        self.assertEqual(record["status"], "not_dispatched")
        self.assertEqual(record["failure_code"], "INPUT_WINDOW_EXCEEDED")
        self.assertEqual(record["input_preflight"]["status"], "refused")
        prepared = read_json(self.root / "refusal" / "calls" / "c0001" / "a00" / "prepared-request.json")
        self.assertIn("Return json for this small fixture.", prepared["wire_body_text"])
        self.assertEqual(hashlib.sha256(prepared["wire_body_text"].encode("utf-8")).hexdigest(),
                         prepared["wire_body_sha256"])
        self.assertFalse((self.root / "refusal" / "calls" / "c0001" / "a00" / "provider").exists())

    def test_actual_over_window_call_refuses_before_dispatch_with_reason(self):
        calls = RecordedCalls(self.root / "actual-over-window", mode="live")
        with mock.patch.object(calls.adapter, "call", side_effect=AssertionError("dispatch occurred")) as dispatch:
            with self.assertRaisesRegex(InputError, "INPUT_WINDOW_EXCEEDED"):
                calls.call("oversized", [{"role":"user", "content":"json " + "x" * 1_000_000}], schema=OUTPUT_SCHEMA)
        dispatch.assert_not_called()
        self.assertEqual(calls.count, 0)
        record = read_json(calls.calls_root / "c0001" / "a00" / "preflight-refusal.json")
        self.assertEqual(record["failure_code"], "INPUT_WINDOW_EXCEEDED")
        self.assertIn("complete request exceeds", record["reason"])
        self.assertGreater(record["input_preflight"]["total_bound"], record["input_preflight"]["context_window"])
        self.assertFalse((calls.calls_root / "c0001" / "a00" / "provider").exists())

    def test_repair_keeps_source_context_and_repreflights_complete_wire(self):
        normalized = normalize_inputs("Quote the supplied source.",
            {"documents":[{"id":"source","text":"Exact quoted source context."}]})
        store = TaskInputs.from_task({"task":"fixture", "inputs":normalized}, self.root)
        messages = [{"role":"system","content":"Return the JSON contract."},
                    {"role":"user","content":json.dumps({"inputs":normalized}, ensure_ascii=False)}]
        seen = []
        def scripted(**context):
            seen.append(context)
            return {"status":"complete"} if context["attempt"] == 0 else complete("Exact quoted source context.")
        calls = RecordedCalls(self.root / "repair", scripted=scripted, task_inputs=store)
        result = calls.call("evidence", messages, schema=OUTPUT_SCHEMA)
        self.assertEqual(result["answer"], "Exact quoted source context.")
        self.assertEqual(calls.count, 2)
        self.assertEqual(seen[1]["messages"][:2], seen[0]["messages"])
        first = read_json(self.root / "repair" / "calls" / "c0001" / "a00" / "decision.json")
        second = read_json(self.root / "repair" / "calls" / "c0001" / "a01" / "decision.json")
        self.assertEqual(first["input_preflight"]["status"], "accepted")
        self.assertEqual(second["input_preflight"]["status"], "accepted")
        self.assertGreater(second["input_preflight"]["wire_bytes"], first["input_preflight"]["wire_bytes"])
        self.assertTrue(first["source_reads"])
        self.assertTrue(second["source_reads"])


if __name__ == "__main__":
    unittest.main()
