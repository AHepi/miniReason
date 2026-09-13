"""Exercise H001 through the frozen compiler, renderer and route validator."""
from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest
from tools import luna_routing_probe as p


class LunaRoutingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.output = self.root / "probe"
        self.repo = p.PortableRepositoryPath(Path(p.__file__).resolve().parents[1])
        p.initialize(self.repo, self.output)

    def tearDown(self):
        self.tmp.cleanup()

    def complete(self, call):
        p.make_request(self.repo, self.output, call)
        source = self.root / f"answer-{call}.txt"
        source.write_bytes(f'Public fixture {call}: π\n  preserve indentation\n{{"quoted":"opaque"}}\n'.encode())
        p.record_answer(self.output, call, source, "scripted-fixture")
        return source.read_bytes().decode()

    def test_real_rendering_six_responses_eight_routes_and_isolation(self):
        texts = {call: self.complete(call) for call in (1, 2, 3, 5, 4, 6)}
        result = p.check_all(self.repo, self.output)
        self.assertEqual((result["rendered_stage_deliveries"], result["reused_prefix_deliveries"]), (8, 2))
        self.assertTrue(result["shared_prefix_messages_equal"])
        self.assertFalse(result["full_scheduler_qualified"])
        for call in range(1, 7):
            self.assertEqual(p.answer(self.output, call), texts[call])
        returned = p.load_json(self.output / "requests/0003.json")
        archived = p.load_json(self.output / "requests/0005.json")
        self.assertIn(texts[2], returned["messages"][1]["content"])
        self.assertNotIn(texts[2], archived["messages"][1]["content"])
        self.assertEqual(archived["parent_stages"], ["use_before"])
        for call, parent in ((4, 3), (6, 5)):
            request = p.load_json(self.output / f"requests/{call:04d}.json")
            self.assertEqual(request["input_ports"], ["u1"])
            self.assertEqual(request["parent_stages"], ["apply_return"])
            self.assertIn(texts[parent], request["messages"][1]["content"])
            self.assertNotIn(texts[1], request["messages"][1]["content"])
            self.assertNotIn(texts[2], request["messages"][1]["content"])

    def test_missing_parent_refuses_before_packet_creation(self):
        with self.assertRaises(FileNotFoundError):
            p.make_request(self.repo, self.output, 2)
        self.assertFalse((self.output / "packets/0002.json").exists())

    def test_changed_response_refuses_next_packet(self):
        self.complete(1)
        (self.output / "responses/0001.txt").write_bytes(b"changed\n")
        with self.assertRaisesRegex(ValueError, "RESPONSE_BYTES_CHANGED"):
            p.make_request(self.repo, self.output, 2)
        self.assertFalse((self.output / "packets/0002.json").exists())

    def test_actual_validator_rejects_extra_criticism_and_wrong_coordinate(self):
        self.complete(1)
        self.complete(2)
        _, (request, manifest, answers, system) = p.render(self.repo, self.output, 1, 2)
        with self.assertRaisesRegex(ValueError, "ACTUAL_MINI_ROUTE_CHANGED"):
            p.study.routed_messages(replace(request, brief=request.brief + "\nINJECTED CRITICISM"),
                                    manifest, p.study.ARMS[1], answers, system)
        with self.assertRaisesRegex(ValueError, "UNEXPECTED_MINI_COORDINATE"):
            p.study.routed_messages(replace(request, cycle=2), manifest, p.study.ARMS[1], answers, system)

    def test_participant_packet_mutation_refuses_before_accepting_response(self):
        p.make_request(self.repo, self.output, 1)
        (self.output / "packets/0001.json").write_text('{"messages":[]}', encoding="utf-8")
        source = self.root / "answer.txt"
        source.write_text("Public response", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "PARTICIPANT_PACKET_CHANGED"):
            p.record_answer(self.output, 1, source, "scripted-fixture")
        self.assertFalse((self.output / "responses/0001.txt").exists())
    def test_existing_packet_answer_and_plan_preserved(self):
        self.complete(1)
        packet = self.output / "packets/0001.json"
        original = packet.read_bytes()
        with self.assertRaises(FileExistsError):
            p.make_request(self.repo, self.output, 1)
        with self.assertRaises(FileExistsError):
            p.record_answer(self.output, 1, self.root / "answer-1.txt", "duplicate")
        with self.assertRaises(FileExistsError):
            p.initialize(self.repo, self.output)
        self.assertEqual(packet.read_bytes(), original)
        self.assertIsNone(p.load_json(self.output / "responses/0001.json")["usage"])


if __name__ == "__main__":
    unittest.main()
