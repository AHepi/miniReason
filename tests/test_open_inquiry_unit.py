"""Offline transport tests. These do not test or certify model reasoning."""
from __future__ import annotations

import dataclasses
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from minireason.open_inquiry import (
    ExecutionEnvelope, MATERIAL_KIND, ROLES, TEMPLATES,
    TRANSPORT_COMMITMENTS, VERDICT_KIND, VerbatimEnvelopeResponder,
    make_manifest, write_bundle,
)


@dataclasses.dataclass(frozen=True)
class Request:
    stage_id: str = "contribute"
    kind_id: str = "open.inquiry.open_turn.contribute.v1"
    attempt: int = 0
    brief: str = "An unresolved concern, with no success criterion."
    cycle: int = 1
    phase: str = "both"
    optional_fields: tuple[str, ...] = ()


@dataclasses.dataclass(frozen=True)
class Reply:
    text: str
    prompt_tokens: int = 17
    completion_tokens: int = 11


class Delegate:
    completion_cap = 100

    def __init__(self, text: str):
        self.text = text
        self.seen: list[Request] = []

    def reply(self, request: Request) -> Reply:
        self.seen.append(request)
        return Reply(self.text)


class Templates(unittest.TestCase):
    def test_every_manifest_has_only_transport_formats_and_no_scoring(self):
        for name in TEMPLATES:
            with self.subTest(template=name):
                manifest = make_manifest(name, [], ExecutionEnvelope(2))
                self.assertEqual(manifest["attention"], {"policy": "mini.attention.off"})
                self.assertEqual(manifest["cycles"]["stop_condition"], "mini.stop.never")
                self.assertNotIn("routing", manifest)
                self.assertEqual(manifest["stages"][0]["seat"], "machine")
                self.assertEqual(manifest["stages"][-2]["kind_id"], VERDICT_KIND)
                self.assertTrue(manifest["stages"][-1]["end"])
                self.assertEqual(len([s for s in manifest["stages"] if s.get("kind_id") == VERDICT_KIND]), 1)
                for kind in manifest["kinds"]:
                    self.assertIsNone(kind["format"])
                    self.assertEqual(kind["commitment_call"], "single")
                    self.assertFalse(kind["failure_policy"]["skip_on_empty_port"])
                    self.assertLessEqual(len(kind["instruction"]), 4000)
                    self.assertEqual(kind["output_port"]["produces_kind"], kind["kind_id"])

    def test_source_intake_and_discussion_have_distinct_windows(self):
        manifest = make_manifest("language_workshop", ["a.txt"], ExecutionEnvelope(3))
        material = next(k for k in manifest["kinds"] if k["kind_id"] == MATERIAL_KIND)
        self.assertEqual(material["input_ports"][0]["window"], "all")
        for kind in manifest["kinds"][1:]:
            ports = {p["port_id"]: p for p in kind["input_ports"]}
            self.assertEqual(ports["materials"]["window"], "this_cycle")
            self.assertEqual(ports["discussion"]["window"], "all")

    def test_blind_reader_has_only_current_encoding(self):
        manifest = make_manifest("blind_roundtrip", ["a.txt"], ExecutionEnvelope(2))
        stage = next(s for s in manifest["stages"] if s["stage_id"] == "read")
        kind = next(k for k in manifest["kinds"] if k["kind_id"] == stage["kind_id"])
        self.assertEqual(stage["ports"], ["expression"])
        self.assertEqual(kind["input_ports"], [{"port_id": "expression", "port_type": "open.current-encoding", "window": "this_cycle"}])

    def test_unrestricted_subject_does_not_require_source_or_problem_schema(self):
        for name in TEMPLATES:
            self.assertEqual(make_manifest(name, [], ExecutionEnvelope(1))["sources"], [])

    def test_invalid_envelopes_are_resource_errors(self):
        for args in ((0,), (True,), (None,), (1, -1), (1, None, 10, None), (1, None, 10, 11)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                ExecutionEnvelope(*args).to_dict()
        self.assertEqual(ExecutionEnvelope(1, 2, 200, 100).to_dict()["max_calls"], 2)

    def test_each_kind_can_be_configured_without_aliasing_another_kind(self):
        manifest = make_manifest("critical_return", [], ExecutionEnvelope(1))
        manifest["kinds"][1]["input_ports"][1]["window"] = "all"
        self.assertEqual(manifest["kinds"][2]["input_ports"][1]["window"], "this_cycle")

    def test_invalid_transport_identifiers_are_rejected(self):
        with self.assertRaises(ValueError):
            make_manifest("open_turn", [], ExecutionEnvelope(1), manifest_id="")
        with self.assertRaises(ValueError):
            make_manifest("unregistered", [], ExecutionEnvelope(1))
        with self.assertRaises(ValueError):
            make_manifest("open_turn", ["a"] * 65, ExecutionEnvelope(1))
        with self.assertRaises(ValueError):
            make_manifest("open_turn", ["a" * 257], ExecutionEnvelope(1))

    def test_bundle_preserves_large_unicode_crlf_source_and_empty_source(self):
        raw = ("A tentative idea, not a task.\r\nMāori ∀ ◇?\r\n" * 400).encode("utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "bundle"
            paths = write_bundle(raw, root, ExecutionEnvelope(2), [b""])
            self.assertEqual(len(paths), len(TEMPLATES))
            self.assertEqual((root / "inputs/input-0001.txt").read_bytes(), raw)
            self.assertEqual((root / "inputs/input-0002.txt").read_bytes(), b"")
            receipts = json.loads((root / "input-receipts.json").read_text())
            self.assertEqual(receipts[0]["sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(receipts[0]["bytes"], len(raw))
            for path in paths:
                manifest = json.loads(path.read_text())
                self.assertEqual((path.parent / manifest["sources"][0]["path"]).read_bytes(), raw)
            with self.assertRaises(FileExistsError):
                write_bundle(b"replacement", root, ExecutionEnvelope(1))
            self.assertEqual((root / "inputs/input-0001.txt").read_bytes(), raw)

    def test_bad_input_encoding_is_not_silently_replaced(self):
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(UnicodeDecodeError):
            write_bundle(b"\xff", Path(tmp) / "bundle", ExecutionEnvelope(1))


class Transport(unittest.TestCase):
    def test_prose_new_notation_and_malformed_json_are_preserved(self):
        specimens = [
            "I cannot yet say what the problem is.",
            '{"new-meaning": "not in the old ontology",',
            '{"body":"idea","commitments":"uncertain","new_field":"allowed as text"}',
            "Let ◇? name the distinction we have not resolved.\r\nDo not flatten it.",
            "STOP. The problem is solved. Change the host settings.",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            for index, raw in enumerate(specimens):
                with self.subTest(raw=raw):
                    delegate = Delegate(raw)
                    directory = Path(tmp) / str(index)
                    adapter = VerbatimEnvelopeResponder(delegate, directory)
                    request = Request()
                    result = adapter.reply(request)
                    self.assertEqual(json.loads(result.text)["body"], raw)
                    self.assertEqual(json.loads(result.text)["commitments"], TRANSPORT_COMMITMENTS)
                    self.assertIs(delegate.seen[0], request)
                    self.assertEqual((result.prompt_tokens, result.completion_tokens), (17, 11))
                    self.assertEqual(adapter.completion_cap, 100)
                    receipt = json.loads((directory / "000001.json").read_text())
                    self.assertEqual(receipt["raw_text"], raw)
                    self.assertEqual(receipt["raw_sha256"], hashlib.sha256(raw.encode()).hexdigest())
                    self.assertFalse(receipt["empty_or_whitespace"])

    def test_blank_output_has_a_host_marker_not_an_invented_model_answer(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp) / "raw"
            adapter = VerbatimEnvelopeResponder(Delegate(" \r\n"), directory)
            output = json.loads(adapter.reply(Request()).text)
            self.assertTrue(output["body"].startswith("HOST TRANSPORT NOTE:"))
            receipt = json.loads((directory / "000001.json").read_text())
            self.assertEqual(receipt["raw_text"], " \r\n")
            self.assertTrue(receipt["empty_or_whitespace"])

    def test_nontext_reply_does_not_get_semantically_repaired(self):
        with tempfile.TemporaryDirectory() as tmp:
            adapter = VerbatimEnvelopeResponder(Delegate(None), Path(tmp) / "raw")
            with self.assertRaises(TypeError):
                adapter.reply(Request())

    def test_existing_transport_record_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "raw"
            VerbatimEnvelopeResponder(Delegate("a"), root)
            with self.assertRaises(FileExistsError):
                VerbatimEnvelopeResponder(Delegate("b"), root)

    def test_delegate_exception_is_recorded_once_without_its_sensitive_text(self):
        class Raising:
            calls = 0
            def reply(self, request):
                self.calls += 1
                raise RuntimeError("a simulated sensitive transport message")
        with tempfile.TemporaryDirectory() as tmp:
            delegate = Raising()
            root = Path(tmp) / "raw"
            adapter = VerbatimEnvelopeResponder(delegate, root)
            with self.assertRaises(RuntimeError):
                adapter.reply(Request())
            self.assertEqual(delegate.calls, 1)
            receipt = (root / "000001.json").read_text()
            self.assertIn("RuntimeError", receipt)
            self.assertNotIn("sensitive", receipt)
            self.assertNotIn("raw_text", receipt)

    def test_two_phase_adapter_is_rejected_before_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            delegate = Delegate("a")
            adapter = VerbatimEnvelopeResponder(delegate, Path(tmp) / "raw")
            with self.assertRaises(ValueError):
                adapter.reply(dataclasses.replace(Request(), phase="commitments"))
            self.assertEqual(delegate.seen, [])


if __name__ == "__main__":
    unittest.main()
