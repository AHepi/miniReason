"""Offline H005 tests: synthetic artifacts only; no provider or operator oracle."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import hashlib
import json
import os
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from tools import multicycle_commitment_study as h


ARMS = ("bare", "native", "matched", "mini_prose", "mini_fcl")


def wire_payload(messages, settings, json_output=True):
    payload = {"model": settings.model, "messages": messages, "stream": False,
               "max_tokens": settings.max_tokens,
               "thinking": {"type": "enabled" if settings.thinking else "disabled"}}
    if settings.thinking:
        payload["reasoning_effort"] = settings.reasoning_effort
    if json_output:
        payload["response_format"] = {"type": "json_object"}
    return payload


def fixture_material():
    nodes = [
        {"id": "root", "instruction": "Draft an initial account.",
         "inputs": [{"source": "previous", "view": "both"}]},
        {"id": "body_view", "instruction": "Use the selected body.",
         "inputs": [{"source": "root", "view": "body"}]},
        {"id": "commitment_view", "instruction": "Use the selected commitments.",
         "inputs": [{"source": "root", "view": "commitments"}]},
        {"id": "both_view", "instruction": "Use both selected fields.",
         "inputs": [{"source": "root", "view": "both"}]},
        {"id": "final", "instruction": "Return the resulting account.",
         "inputs": [{"source": "body_view", "view": "body"},
                    {"source": "commitment_view", "view": "commitments"},
                    {"source": "both_view", "view": "both"}]},
    ]
    second = deepcopy(nodes)
    second.insert(-1, {"id": "extra", "instruction": "Consider the original problem.",
                       "inputs": [{"source": "origin", "view": "body"}]})
    second[-1]["inputs"].append({"source": "extra", "view": "both"})
    third = deepcopy(second)
    third.insert(-1, {"id": "other", "instruction": "Consider another application.",
                      "inputs": [{"source": "root", "view": "both"}]})
    third[-1]["inputs"].append({"source": "other", "view": "both"})
    return {"schema": "minireason.h005.material.v1",
            "system": "Common synthetic problem context. Preserve Unicode π.",
            "prose_instruction": "PROSE_POLICY_MARKER: write prose commitments.",
            "formal_instruction": "FORMAL_POLICY_MARKER: write formal commitments.",
            "bare_instruction": "BARE_POLICY_MARKER: answer the problem directly.",
            "problems": [{"id": "sample", "prose": "ORIGINAL_PROBLEM_MARKER: discuss a shared room.",
                          "templates": ["five", "six", "seven"]}],
            "templates": {"five": {"nodes": nodes}, "six": {"nodes": second},
                          "seven": {"nodes": third}}}


def response_record(payload, settings, content, *, partial=False):
    completion = settings.max_tokens if partial else 9
    return {"schema_version": "minireason.call.v1", "request": payload,
            "request_sha256": h.digest(payload), "settings": settings.to_dict(),
            "content": content, "status": "INCOMPLETE_GENERATION" if partial else "COMPLETE",
            "finish_reason": "length" if partial else "stop", "returned_model": "offline-fixture",
            "usage": {"prompt_tokens": 13, "completion_tokens": completion,
                      "total_tokens": 13 + completion},
            "reasoning_content_present": settings.thinking,
            "reasoning_content_persisted": False, "credential_redaction": False}


class FakeProvider:
    lock = threading.Lock()
    active = peak = calls = constructions = 0
    gate = False
    barrier = None
    sent = []
    malformed = False
    partial = False
    coordinate_mismatch = None

    def __init__(self, settings, records):
        with type(self).lock:
            type(self).constructions += 1
        if not type(self).gate:
            raise AssertionError("Publication must succeed before provider construction")
        self.settings, self.records = settings, Path(records)

    def complete(self, messages, *, json_output, coordinate):
        cls = type(self)
        if not json_output:
            raise AssertionError("Every arm must request the authored JSON envelope")
        with cls.lock:
            cls.calls += 1
            cls.active += 1
            cls.peak = max(cls.peak, cls.active)
            cls.sent.append(deepcopy(coordinate))
        try:
            if cls.barrier:
                cls.barrier.wait(timeout=10)
            time.sleep(0.005)
            marker = "|".join(str(coordinate[k]) for k in ("problem", "arm", "cycle", "node"))
            content = ("opaque exact public text \r\n π " if cls.malformed else
                       json.dumps({"body": "BODY[" + marker + "]",
                                   "commitments": "COMMIT[" + marker + "]"}, ensure_ascii=False))
            payload = wire_payload(messages, self.settings, json_output)
            record = response_record(payload, self.settings, content, partial=cls.partial)
            record['coordinate'] = deepcopy(coordinate)
            request_record = {"request": payload, "coordinate": deepcopy(coordinate),
                              "request_sha256": h.digest(payload), "settings": self.settings.to_dict()}
            if cls.coordinate_mismatch == "request":
                request_record["coordinate"]["node"] = "WRONG_COORDINATE"
            elif cls.coordinate_mismatch == "response":
                record["coordinate"]["node"] = "WRONG_COORDINATE"
            h.write_new(self.records / "call-0001.request.json", request_record)
            h.write_new(self.records / "call-0001.response.json", record)
            if cls.partial:
                raise RuntimeError("Synthetic length boundary; preserved provider record is authoritative")
            return record
        finally:
            with cls.lock:
                cls.active -= 1


class MultiCycleCommitmentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(h.__file__).resolve().parents[1]
        self.output = Path(self.temp.name) / "H005-offline"
        self.material_path = Path(self.temp.name) / "source-material.json"
        self.material = fixture_material()
        self.material_path.write_text(json.dumps(self.material, ensure_ascii=False), encoding="utf-8")
        self.plan = h.initialize(self.repo, self.output, self.material_path)
        FakeProvider.active = FakeProvider.peak = FakeProvider.calls = FakeProvider.constructions = 0
        FakeProvider.gate = False
        FakeProvider.barrier = None
        FakeProvider.sent = []
        FakeProvider.malformed = FakeProvider.partial = False
        FakeProvider.coordinate_mismatch = None
        self.env = patch.dict(os.environ, {"DEEPSEEK_API_KEY": "synthetic-offline-credential"})
        self.env.start()
        self.addCleanup(self.env.stop)

    def published(self, *args):
        FakeProvider.gate = True
        return "offline-verified-publication"

    def send(self, wave):
        return h.send_wave(self.repo, self.output, wave["wave_id"],
                           provider_factory=FakeProvider, publication_check=self.published,
                           notify=lambda line: None)

    def coord(self, arm, node="root", cycle=1):
        return {"problem": "sample", "arm": arm, "cycle": cycle, "node": node}

    def first_wave(self):
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        self.send(wave)
        return wave

    def test_material_custody_and_occurrence_no_clobber(self):
        material, plan = h.verify(self.repo, self.output)
        self.assertEqual(material, self.material)
        self.assertEqual(plan, self.plan)
        self.assertEqual((self.output / "material.json").read_bytes(), self.material_path.read_bytes())
        with self.assertRaisesRegex(ValueError, "OCCURRENCE_EXISTS"):
            h.initialize(self.repo, self.output, self.material_path)
        material_file = self.output / "material.json"
        material_file.write_bytes(material_file.read_bytes() + b" ")
        with self.assertRaises(ValueError):
            h.verify(self.repo, self.output)

    def test_invalid_graphs_references_and_cycle_counts_are_rejected(self):
        mutations = {
            "missing_source": lambda m: m["templates"]["five"]["nodes"][1]["inputs"][0].update(source="absent"),
            "forward_reference": lambda m: m["templates"]["five"]["nodes"][0]["inputs"].append({"source": "final", "view": "body"}),
            "self_reference": lambda m: m["templates"]["five"]["nodes"][0]["inputs"].append({"source": "root", "view": "body"}),
            "duplicate_node": lambda m: m["templates"]["five"]["nodes"][1].update(id="root"),
            "invalid_view": lambda m: m["templates"]["five"]["nodes"][1]["inputs"][0].update(view="inferred"),
            "missing_template": lambda m: m["problems"][0]["templates"].__setitem__(1, "absent"),
            "two_cycles": lambda m: m["problems"][0].update(templates=["five"] * 2),
            "six_cycles": lambda m: m["problems"][0].update(templates=["five"] * 6),
        }
        for name, mutate in mutations.items():
            with self.subTest(case=name):
                bad = deepcopy(self.material)
                mutate(bad)
                source = Path(self.temp.name) / (name + ".json")
                source.write_text(json.dumps(bad), encoding="utf-8")
                with self.assertRaises(ValueError):
                    h.initialize(self.repo, Path(self.temp.name) / name, source)

    def test_cycle_is_a_whole_template_invocation_with_distinct_node_coordinates(self):
        for cycle, template in enumerate(("five", "six", "seven"), 1):
            for _ in range(30):
                wave = h.prepare_wave(self.repo, self.output, "sample", cycle)
                if not wave["coordinates"]:
                    break
                self.assertLessEqual(len(wave["coordinates"]), 5)
                self.assertEqual({c["cycle"] for c in wave["coordinates"]}, {cycle})
                self.send(wave)
            else:
                self.fail("Dependency-ready scheduling did not terminate within the finite fixture")
            expected = {n["id"] for n in self.material["templates"][template]["nodes"]}
            for arm in ("matched", "mini_prose", "mini_fcl"):
                actual = {c["node"] for c in FakeProvider.sent if c["arm"] == arm and c["cycle"] == cycle}
                self.assertEqual(actual, expected)
        actual = [tuple(c[k] for k in ("problem", "arm", "cycle", "node")) for c in FakeProvider.sent]
        self.assertEqual(len(actual), len(set(actual)))
        for invalid in (0, 4, True):
            with self.subTest(cycle=invalid), self.assertRaises(ValueError):
                h.prepare_wave(self.repo, self.output, "sample", invalid)

    def test_body_commitment_and_both_views_are_separate_and_bound_to_parent_bytes(self):
        self.first_wave()
        for arm in ("mini_prose", "mini_fcl"):
            body = "BODY[sample|" + arm + "|1|root]"
            commitment = "COMMIT[sample|" + arm + "|1|root]"
            for node, want_body, want_commitment in (("body_view", True, False),
                                                    ("commitment_view", False, True),
                                                    ("both_view", True, True)):
                with self.subTest(arm=arm, node=node):
                    request, trace = h.render_node(self.repo, self.output, self.coord(arm, node))
                    prompt = "\n".join(m["content"] for m in request["messages"])
                    self.assertEqual(body in prompt, want_body)
                    self.assertEqual(commitment in prompt, want_commitment)
                    other = "mini_fcl" if arm == "mini_prose" else "mini_prose"
                    self.assertNotIn("BODY[sample|" + other + "|", prompt)
                    self.assertNotIn("COMMIT[sample|" + other + "|", prompt)
                    custody = json.dumps(trace, ensure_ascii=False)
                    self.assertIn(hashlib.sha256(body.encode("utf-8")).hexdigest(), custody)
                    self.assertIn(hashlib.sha256(commitment.encode("utf-8")).hexdigest(), custody)

    def test_settings_and_envelopes_are_explicit_for_every_arm(self):
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        self.assertEqual({c["arm"] for c in wave["coordinates"]}, set(ARMS))
        for coord in wave["coordinates"]:
            wrapper = h.load(h.at(self.output, "requests", coord))
            expected_template = coord["arm"] + "1" if coord["arm"] in ("bare", "native") else "five"
            self.assertEqual(wrapper["template_id"], expected_template)
            self.assertEqual(h.load(h.at(self.output, "traces", coord))["template_id"], expected_template)
            if coord["arm"] in ("bare", "native"):
                self.assertEqual(len(h.nodes_for(self.material, self.material["problems"][0], coord["arm"], 1)), 1)
            request = wrapper["provider_payload"]
            self.assertEqual(request["max_tokens"], 8192)
            self.assertEqual(request["thinking"], {"type": "enabled" if coord["arm"] == "native" else "disabled"})
            self.assertEqual(request["response_format"], {"type": "json_object"})
            if coord["arm"] == "native":
                self.assertEqual(request["reasoning_effort"], "low")

        for invocation in h.audit(self.repo, self.output)["invocations"]:
            if invocation["arm"] in ("bare", "native"):
                self.assertEqual(invocation["nodes"], 1)
                self.assertEqual(invocation["template_id"], invocation["arm"] + "1")
    def test_publication_failure_starts_no_provider_or_attempt(self):
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        def denied(*args):
            raise ValueError("UNPUBLISHED_SYNTHETIC_WAVE")
        with self.assertRaisesRegex(ValueError, "UNPUBLISHED_SYNTHETIC_WAVE"):
            h.send_wave(self.repo, self.output, wave["wave_id"],
                        provider_factory=FakeProvider, publication_check=denied)
        self.assertEqual(FakeProvider.calls, 0)
        self.assertEqual(FakeProvider.constructions, 0)
        self.assertFalse(any((self.output / "attempts").rglob("*.json")))

    def test_five_independent_ready_calls_overlap_and_cannot_be_replayed(self):
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        self.assertEqual(len(wave["coordinates"]), 5)
        FakeProvider.barrier = threading.Barrier(5)
        rows = self.send(wave)
        self.assertEqual(len(rows), 5)
        self.assertEqual(FakeProvider.peak, 5)
        self.assertEqual(FakeProvider.active, 0)
        before = FakeProvider.calls
        with self.assertRaises(FileExistsError):
            self.send(wave)
        self.assertEqual(FakeProvider.calls, before)

    def test_request_tampering_is_rejected_before_provider_construction(self):
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        path = h.at(self.output, "requests", wave["coordinates"][0])
        value = h.load(path)
        value["messages"][1]["content"] += "UNDECLARED_ADDITION"
        path.write_text(json.dumps(value), encoding="utf-8")
        with self.assertRaises(ValueError):
            self.send(wave)
        self.assertEqual(FakeProvider.constructions, 0)

    def test_pending_attempt_marker_is_a_no_retry_boundary(self):
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        h.write_new(h.at(self.output, "attempts", wave["coordinates"][0]),
                    {"status": "DISPATCH_STARTED", "usage": None})
        with self.assertRaises(FileExistsError):
            self.send(wave)
        self.assertEqual(FakeProvider.calls, 0)

    def test_provider_coordinate_mismatch_fails_usability_and_preserves_exact_raw_text(self):
        for side in ("request", "response"):
            with self.subTest(record=side):
                output = Path(self.temp.name) / ("coordinate-mismatch-" + side)
                h.initialize(self.repo, output, self.material_path)
                wave = h.prepare_wave(self.repo, output, "sample", 1)
                FakeProvider.coordinate_mismatch = side
                before = FakeProvider.calls
                receipts = h.send_wave(self.repo, output, wave["wave_id"],
                                       provider_factory=FakeProvider, publication_check=self.published,
                                       notify=lambda line: None)
                self.assertEqual(FakeProvider.calls - before, 5)
                self.assertEqual({row["status"] for row in receipts}, {"FAILED"})
                for coord in wave["coordinates"]:
                    provider_record = h.load(h.provider_dir(output, coord) / "call-0001.response.json")
                    self.assertEqual(h.at(output, "responses", coord, "txt").read_bytes(),
                                     provider_record["content"].encode("utf-8"))
                    self.assertFalse(h.at(output, "artifacts", coord).exists())
                with self.assertRaises(FileExistsError):
                    h.send_wave(self.repo, output, wave["wave_id"],
                                provider_factory=FakeProvider, publication_check=self.published,
                                notify=lambda line: None)
                self.assertEqual(FakeProvider.calls - before, 5)
    def test_required_publication_paths_include_transitive_provider_and_artifact_bytes(self):
        self.first_wave()
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        required = set(h.required_paths(self.repo, self.output, wave))
        for arm in ("matched", "mini_prose", "mini_fcl"):
            parent = self.coord(arm)
            for category in ("requests", "traces", "attempts", "responses", "artifacts"):
                self.assertIn(h.at(self.output, category, parent), required)
            self.assertIn(h.at(self.output, "responses", parent, "txt"), required)
            for filename in ("call-0001.request.json", "call-0001.response.json"):
                self.assertIn(h.provider_dir(self.output, parent) / filename, required)

    def test_publication_checks_actual_bytes_and_remote_head_without_git_mutation(self):
        # A tiny temporary checkout supplies the mandatory pin paths. Execution still
        # uses the already imported production compiler; this is a byte-custody fixture.
        fake_repo = Path(self.temp.name) / "publication-checkout"
        fake_helper = fake_repo / "tools" / "multicycle_commitment_study.py"
        fake_helper.parent.mkdir(parents=True)
        fake_helper.write_bytes(Path(h.__file__).read_bytes())
        for relative in ("src/minireason/provider.py", "tools/multicycle_language_probe.py"):
            destination = fake_repo / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((self.repo / relative).read_bytes())
        output = fake_repo / "occurrence"
        with patch.object(h, "__file__", str(fake_helper)):
            h.initialize(fake_repo, output, self.material_path)
            wave = h.prepare_wave(fake_repo, output, "sample", 1)
            required = h.required_paths(fake_repo, output, wave)
            committed = {p.relative_to(fake_repo).as_posix(): p.read_bytes() for p in required}
            head = "a" * 40
            def git_bytes(repo, *args):
                self.assertEqual(Path(repo), fake_repo)
                if args == ("rev-parse", "HEAD"):
                    return (head + "\n").encode("ascii")
                if args == ("ls-remote", "--refs", "origin", "refs/heads/main"):
                    return (head + "\trefs/heads/main\n").encode("ascii")
                if args[0] == "show":
                    commit, relative = args[1].split(":", 1)
                    self.assertEqual(commit, head)
                    return committed[relative]
                raise AssertionError("Unexpected Git command in publication check: " + repr(args))
            with patch.object(h, "git", side_effect=git_bytes):
                self.assertEqual(h.check_published(fake_repo, output, wave), head)
                target = h.at(output, "requests", wave["coordinates"][0])
                target.write_bytes(target.read_bytes() + b" ")
                with self.assertRaisesRegex(ValueError, "INPUT_NOT_PUBLISHED"):
                    h.check_published(fake_repo, output, wave)
            with patch.object(h, "git", side_effect=[(head + "\n").encode(), b"other refs/heads/main\n"]):
                with self.assertRaisesRegex(ValueError, "REMOTE_MAIN_CHANGED"):
                    h.check_published(fake_repo, output, wave)
        self.assertEqual(FakeProvider.calls, 0)
    def test_partial_delivery_remains_usable_without_retry_or_relabeling(self):
        FakeProvider.partial = True
        self.first_wave()
        self.assertEqual(FakeProvider.calls, 5)
        request, trace = h.render_node(self.repo, self.output, self.coord("mini_prose", "body_view"))
        prompt = "\n".join(m["content"] for m in request["messages"])
        self.assertIn("BODY[sample|mini_prose|1|root]", prompt)
        artifact = h.load(h.at(self.output, "artifacts", self.coord("mini_prose")))
        self.assertEqual(artifact["delivery_status"], "PARTIAL")
        self.assertEqual(artifact["envelope_status"], "AUTHORED")
        self.assertIn("PARTIAL", json.dumps(trace))
        self.assertEqual(FakeProvider.calls, 5)

    def test_mutated_parent_artifact_is_refused_before_dependent_rendering(self):
        self.first_wave()
        path = h.at(self.output, "artifacts", self.coord("mini_prose"))
        artifact = h.load(path)
        artifact["body"] = "UNPUBLISHED_REPLACEMENT_BODY"
        path.write_text(json.dumps(artifact), encoding="utf-8")
        with self.assertRaises(ValueError):
            h.render_node(self.repo, self.output, self.coord("mini_prose", "body_view"))
        self.assertEqual(FakeProvider.calls, 5)
    def test_decode_preserves_authored_fields_opaque_text_and_valid_partial_envelope(self):
        settings = h.Settings(thinking=False, reasoning_effort="low", max_tokens=8192, timeout_seconds=180)
        payload = wire_payload([{"role": "user", "content": "Synthetic request"}], settings)
        samples = [
            (json.dumps({"body": "Authored body π", "commitments": "Different commitment"}), False, "AUTHORED", "Authored body π", "Different commitment"),
            ("exact opaque text\r\nwith π and trailing spaces  ", False, "OPAQUE", "exact opaque text\r\nwith π and trailing spaces  ", ""),
            ('{"body":"text","commitments":17}', False, "OPAQUE", '{"body":"text","commitments":17}', ""),
            (json.dumps({"body": "Admitted partial body", "commitments": "Partial commitment"}), True, "AUTHORED", "Admitted partial body", "Partial commitment"),
        ]
        for content, partial, envelope, body, commitments in samples:
            with self.subTest(envelope=envelope, partial=partial, content=content):
                record = response_record(payload, settings, content, partial=partial)
                original = deepcopy(record)
                artifact = h.decode_contribution(record, payload, settings)
                self.assertEqual(record, original)
                self.assertEqual(artifact["body"], body)
                self.assertEqual(artifact["commitments"], commitments)
                self.assertEqual(artifact["delivery_status"], "PARTIAL" if partial else "COMPLETE")
                self.assertEqual(artifact["envelope_status"], envelope)
                for name, text in (("public_text", content), ("body", body), ("commitments", commitments)):
                    self.assertEqual(artifact[name + "_sha256"], hashlib.sha256(text.encode("utf-8")).hexdigest())

    def test_decode_refuses_custody_delivery_and_hidden_reasoning_mismatches(self):
        settings = h.Settings(thinking=False, reasoning_effort="low", max_tokens=8192, timeout_seconds=180)
        payload = wire_payload([{"role": "user", "content": "Synthetic request"}], settings)
        record = response_record(payload, settings, '{"body":"body","commitments":"commitments"}')
        changes = [
            {"request_sha256": "incorrect"},
            {"request": {"messages": []}},
            {"settings": {}},
            {"content": "  "},
            {"status": "TRANSPORT_OR_RESPONSE_ERROR"},
            {"reasoning_content_persisted": True},
            {"reasoning_content_present": True},
            {"credential_redaction": True},
            {"usage": {"prompt_tokens": 1, "completion_tokens": 8193, "total_tokens": 8194}},
        ]
        for change in changes:
            with self.subTest(change=change):
                bad = deepcopy(record)
                bad.update(change)
                with self.assertRaises(ValueError):
                    h.decode_contribution(bad, payload, settings)


if __name__ == "__main__":
    unittest.main()
