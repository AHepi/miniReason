"""Review45 regressions for P-A2 JSON-unit and compact-record custody."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from minireason.pilot.inputs import InputError, TaskInputs
from minireason.pilot.pilot import Pilot

class Review45ContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_json_units_reject_duplicate_members_and_nonfinite_values(self):
        for text in ['{"candidate":"a","candidate":"b"}', '{"x":{"a":1,"a":1}}',
                     '{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}', '{"x":1e999}']:
            with self.subTest(text=text):
                raw = text.encode("utf-8")
                uid = hashlib.sha256(raw).hexdigest()
                with (self.root/"input.json").open("w",encoding="utf-8",newline="") as handle:
                    handle.write(text)
                task = {"task":"fixture", "inputs":{"unit_id":uid,"start":0,"end":len(raw),"encoding":"json"},
                        "input_units":[{"unit_id":uid,"sha256":uid,"byte_count":len(raw),
                        "path":"input.json","role":"task_input","media_type":"application/json"}]}
                with self.assertRaisesRegex(InputError,"INPUT_REFERENCE_INVALID"):
                    TaskInputs.from_task(task,self.root)

    def test_legacy_spawn_receipts_all_use_resolvable_content_references(self):
        content = "Large source fixture. " * 2000
        task = {"task":"Read the source", "inputs":{"documents":[{"id":"source","text":content}]}}
        output = {"status":"complete","answer":"done","source_refs":[],"verification_refs":[],"unresolved":[]}
        pilot = Pilot(task,self.root/"run",scripted=lambda **context:output)
        pilot.handle_tool("route",{"template_id":"direct_answer","reason":"Closed fixture."})
        pilot.handle_tool("spawn",{"subtasks":[{"template_id":"direct_answer","inputs":pilot.inputs}]})
        for field in ("spawned","spawned_refs"):
            reference = pilot.current[field][0]["inputs"]
            self.assertEqual(set(reference),{"unit_id","start","end","encoding"})
            self.assertEqual(pilot.task_inputs.expand_inputs(reference,"regression"),pilot.inputs)
        event = next(item for item in pilot.events if item["choice"]=="spawn")
        self.assertEqual(event["evidence"]["arguments"]["subtasks"],pilot.current["spawned_refs"])
        self.assertLess(len(json.dumps(pilot.current["spawned_refs"])),2048)
