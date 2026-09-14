"""Offline tests for the multi-provider H005 fork.

The owner's sixteen tests, ported to the fork with a multi-endpoint fixture,
plus the ones that exist only because of the fork: the per-key concurrency cap,
arm/endpoint validation, the configurable publication ref, the declared
`envelope_unwrap` decode step, and an END-TO-END test that runs a synthetic
fork5 occurrence for one problem with two arms on two endpoints through
prepare/send for all five nodes and then imports it with the published
`minireason.graph_import_h005`.

No socket is opened: every call goes through `provider_openai_compat`'s own
`OfflineProvider`, so the request bodies, the recorded settings view and the
write-once record layout under test are the real transport's, not a mock's.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import ast
import dataclasses
import hashlib
import inspect
import json
import os
import shutil
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

STAGE = Path(__file__).resolve().parents[1]
if str(STAGE) not in sys.path:
    sys.path.insert(0, str(STAGE))

from tools import multicycle_commitment_study_multi as h
from minireason import provider_openai_compat as oc
from minireason import graph_import_h005 as importer

PUBLISHED = Path("/home/user/miniReason/src/minireason")
H005 = Path("/home/user/miniReason/experiments/diagnostics/H005-open-prose-commitments")
OWNER_RUNNER = Path("/home/user/miniReason/tools/multicycle_commitment_study.py")
STUDY = Path(h.__file__).resolve().parents[1] / "experiments/diagnostics/F001-fork5-multifamily"

#: One credential each, so the per-key grouping has something to group.
ALPHA = oc.ENDPOINTS["deepseek-flash"]          # family deepseek, DEEPSEEK_API_KEY
BETA = oc.ENDPOINTS["ollama/gpt-oss-120b"]      # family ollama-cloud/gpt-oss, OLLAMA_API_KEY
REGISTRY = {ALPHA.name: ALPHA, BETA.name: BETA,
            "ollama/gemma4-31b": oc.ENDPOINTS["ollama/gemma4-31b"],
            "ollama/gpt-oss-120b.native": oc.ENDPOINTS["ollama/gpt-oss-120b.native"]}

CANONICAL_ARMS = {
    "bare": {"surface": "prose", "kind": "bare", "endpoint": ALPHA.name},
    "native": {"surface": "prose", "kind": "native", "endpoint": ALPHA.name},
    "matched": {"surface": "prose", "kind": "matched", "endpoint": ALPHA.name},
    "mini_prose": {"surface": "prose", "kind": "mini", "endpoint": ALPHA.name},
    "mini_fcl": {"surface": "fcl", "kind": "mini", "endpoint": ALPHA.name},
}
ARMS = tuple(CANONICAL_ARMS)

TWO_KEY_ARMS = {}
for _index in range(1, 6):
    TWO_KEY_ARMS[f"a{_index}_mini_fcl"] = {"surface": "fcl", "kind": "mini", "endpoint": ALPHA.name}
    TWO_KEY_ARMS[f"b{_index}_mini_fcl"] = {"surface": "fcl", "kind": "mini", "endpoint": BETA.name,
                                           "seed": 7}

#: Five arms on ONE credential: the shape two occurrences share in a round.
ALPHA_ARMS = {name: spec for name, spec in TWO_KEY_ARMS.items() if name.startswith("a")}
BETA_ARMS = {name: spec for name, spec in TWO_KEY_ARMS.items() if name.startswith("b")}
#: Seven on one credential and three on the other: more than `key_cap` is ready
#: on ALPHA while the wave as a whole stays under the total capacity, so the
#: per-key admission in `ready_coordinates` is the only thing that can truncate.
LOPSIDED_ARMS = {}
for _index in range(1, 8):
    LOPSIDED_ARMS[f"a{_index}_mini_fcl"] = {"surface": "fcl", "kind": "mini", "endpoint": ALPHA.name}
for _index in range(1, 4):
    LOPSIDED_ARMS[f"b{_index}_mini_fcl"] = {"surface": "fcl", "kind": "mini", "endpoint": BETA.name}


def arms_document(mapping, mode="offline"):
    return {"schema": "minireason.h005.arms.v1", "provider": mode, "arms": deepcopy(mapping)}


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
            "study_id": "F001-fork5-multifamily",
            "system": "Common synthetic problem context. Preserve Unicode π.",
            "prose_instruction": "PROSE_POLICY_MARKER: write prose commitments.",
            "formal_instruction": "FORMAL_POLICY_MARKER: write formal commitments.",
            "bare_instruction": "BARE_POLICY_MARKER: answer the problem directly.",
            "problems": [{"id": "sample", "prose": "ORIGINAL_PROBLEM_MARKER: discuss a shared room.",
                          "templates": ["five", "six", "seven"]}],
            "templates": {"five": {"nodes": nodes}, "six": {"nodes": second},
                          "seven": {"nodes": third}}}


def response_record(payload, settings, content, *, partial=False, reasoning=False):
    """A provider response record in the shape `decode_contribution` reads."""
    completion = settings.max_tokens if partial else 9
    return {"schema_version": "minireason.call.v2", "request": payload,
            "request_sha256": h.digest(payload), "settings": settings.to_dict(),
            "content": content, "status": "INCOMPLETE_GENERATION" if partial else "COMPLETE",
            "finish_reason": "length" if partial else "stop", "returned_model": "offline-fixture",
            "usage": {"prompt_tokens": 13, "completion_tokens": completion,
                      "total_tokens": 13 + completion},
            "reasoning_content_present": reasoning,
            "reasoning_content_persisted": False, "credential_redaction": False}


def envelope(marker, commitments=None):
    return json.dumps({"body": "BODY[" + marker + "]",
                       "commitments": commitments if commitments is not None
                       else "COMMIT[" + marker + "]"}, ensure_ascii=False)


class FakeProvider(oc.OfflineProvider):
    """`provider_openai_compat.OfflineProvider`, scripted per coordinate.

    Records, request bodies and the recorded settings view are the transport's
    own; only the scripted answer and the instrumentation are the test's.
    """

    lock = threading.Lock()
    active = peak = calls = constructions = 0
    per_key_active: dict = {}
    per_key_peak: dict = {}
    gate = False
    barrier = None
    sent: list = []
    seen: list = []
    malformed = False
    fenced = False
    control_chars = False
    partial = False
    reasoning = False
    coordinate_mismatch = None
    commitments_for = None
    #: Held open inside `complete` until the test releases it, so in-flight
    #: counts can be read at a known moment instead of raced for.
    hold = None
    #: `(code, detail)` raised as the transport's own `ProviderFailure`.
    failure = None
    fail_arms = ()

    @classmethod
    def reset(cls):
        cls.active = cls.peak = cls.calls = cls.constructions = 0
        cls.per_key_active, cls.per_key_peak = {}, {}
        cls.gate = False
        cls.barrier = None
        cls.sent, cls.seen = [], []
        cls.malformed = cls.fenced = cls.control_chars = False
        cls.partial = cls.reasoning = False
        cls.coordinate_mismatch = None
        cls.commitments_for = None
        cls.hold = None
        cls.failure = None
        cls.fail_arms = ()

    def __init__(self, endpoint, records):
        with type(self).lock:
            type(self).constructions += 1
        if not type(self).gate:
            raise AssertionError("Publication must succeed before provider construction")
        super().__init__(endpoint, records, script=())

    def _close_record(self, stem, record, *, status, started, **fields):
        if type(self).coordinate_mismatch == "response":
            record = dict(record)
            record["coordinate"] = {**record.get("coordinate", {}), "node": "WRONG_COORDINATE"}
        return super()._close_record(stem, record, status=status, started=started, **fields)

    def _scripted(self, coordinate, ceiling, thinking=None):
        cls = type(self)
        marker = "|".join(str(coordinate[k]) for k in ("problem", "arm", "cycle", "node"))
        if cls.malformed:
            content = "opaque exact public text \r\n π "
        elif cls.control_chars:
            content = ('{"body": "BODY[' + marker + ']", "commitments": "line one\n'
                       'line two of COMMIT[' + marker + ']"}')
        else:
            commitments = None if cls.commitments_for is None else cls.commitments_for(coordinate)
            content = envelope(marker, commitments)
            if cls.fenced:
                content = "```json\n" + content + "\n```"
        completion = ceiling if cls.partial else 9
        return {"content": content,
                "finish_reason": "length" if cls.partial else "stop",
                "returned_model": "offline-fixture",
                # A DeepSeek call that asked for thinking must come back with
                # reasoning present: the transport refuses the pair
                # (thinking on, no reasoning) as THINKING_MODE_MISMATCH, so a
                # script that answered a `native` arm without reasoning would be
                # scripting a response the wire cannot produce.
                "reasoning_content_present": cls.reasoning or bool(thinking),
                "usage": {"prompt_tokens": 13, "completion_tokens": completion,
                          "total_tokens": 13 + completion}}

    def complete(self, messages, **call):
        cls = type(self)
        coordinate = dict(call.get("coordinate") or {})
        key = self.endpoint.key_env
        with cls.lock:
            cls.calls += 1
            cls.active += 1
            cls.peak = max(cls.peak, cls.active)
            cls.per_key_active[key] = cls.per_key_active.get(key, 0) + 1
            cls.per_key_peak[key] = max(cls.per_key_peak.get(key, 0), cls.per_key_active[key])
            cls.sent.append(deepcopy(coordinate))
            cls.seen.append(self.endpoint.name)
        try:
            if cls.failure and coordinate.get("arm") in cls.fail_arms:
                raise oc.ProviderFailure(*cls.failure)
            if cls.hold is not None:
                cls.hold.wait(timeout=10)
            if cls.barrier:
                cls.barrier.wait(timeout=10)
            time.sleep(0.005)
            self._script = [self._scripted(coordinate, call.get("max_tokens", 8192),
                                           call.get("thinking"))]
            self._used = 0
            if cls.coordinate_mismatch == "both":
                call = dict(call, coordinate={**coordinate, "node": "WRONG_COORDINATE"})
            return super().complete(messages, **call)
        finally:
            with cls.lock:
                cls.active -= 1
                cls.per_key_active[key] -= 1


class ForkTestCase(unittest.TestCase):
    arms = CANONICAL_ARMS

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(h.__file__).resolve().parents[1]
        h.set_registry(REGISTRY)
        self.addCleanup(h.set_registry, None)
        # MULTI (b): the per-key gate is process-wide by design, so each test
        # starts from an empty registry of gates rather than inheriting one.
        h._reset_gates()
        self.addCleanup(h._reset_gates)
        self.output = Path(self.temp.name) / "F001-offline"
        self.material_path = Path(self.temp.name) / "source-material.json"
        self.arms_path = Path(self.temp.name) / "source-arms.json"
        self.material = fixture_material()
        self.material_path.write_text(json.dumps(self.material, ensure_ascii=False), encoding="utf-8")
        self.arms_path.write_text(json.dumps(arms_document(self.arms)), encoding="utf-8")
        self.plan = h.initialize(self.repo, self.output, self.material_path, self.arms_path)
        FakeProvider.reset()
        self.env = patch.dict(os.environ, {"DEEPSEEK_API_KEY": "synthetic-offline-credential",
                                           "OLLAMA_API_KEY": "synthetic-offline-credential-b"})
        self.env.start()
        self.addCleanup(self.env.stop)

    def published(self, *args):
        FakeProvider.gate = True
        return "offline-verified-publication"

    def send(self, wave, output=None):
        return h.send_wave(self.repo, output or self.output, wave["wave_id"],
                           provider_factory=FakeProvider, publication_check=self.published,
                           notify=lambda line: None)

    def coord(self, arm, node="root", cycle=1, problem="sample"):
        return {"problem": problem, "arm": arm, "cycle": cycle, "node": node}

    def first_wave(self):
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        self.send(wave)
        return wave

    def settings(self, arm="mini_prose"):
        return h.settings_for(arm, self.plan["arms"])

    def occurrence(self, arms, name, *, scope=None, mode="offline"):
        """A further occurrence in this test's tree, with its own arms and scope."""
        document = arms_document(arms, mode)
        if scope is not None:
            document["scope"] = scope
        path = Path(self.temp.name) / (name + "-arms.json")
        path.write_text(json.dumps(document), encoding="utf-8")
        output = Path(self.temp.name) / name
        return output, h.initialize(self.repo, output, self.material_path, path)

    def spawn(self, jobs):
        """Start one thread per job; failures are collected, never swallowed."""
        errors = []
        def run(job):
            try:
                job()
            except BaseException as exc:
                errors.append(exc)
        threads = [threading.Thread(target=run, args=(job,), daemon=True) for job in jobs]
        for thread in threads:
            thread.start()
        return threads, errors

    def wait_for(self, threads, errors):
        for thread in threads:
            thread.join(timeout=60)
        self.assertEqual([thread.name for thread in threads if thread.is_alive()], [])
        self.assertEqual([repr(error) for error in errors], [])

    def wait_until(self, predicate, timeout=20):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if predicate():
                return True
            time.sleep(0.01)
        return False

    def drain(self, output, problem="sample", cycle=1, limit=40):
        """Prepare and send until no coordinate remains; returns the wave count."""
        waves = 0
        for _ in range(limit):
            wave = h.prepare_wave(self.repo, output, problem, cycle)
            if not wave["coordinates"]:
                return waves
            self.send(wave, output)
            waves += 1
        self.fail("scheduling did not terminate")


class MultiCycleCommitmentTests(ForkTestCase):
    """The owner's sixteen offline tests, ported."""

    def test_material_custody_and_occurrence_no_clobber(self):
        material, plan = h.verify(self.repo, self.output)
        self.assertEqual(material, self.material)
        self.assertEqual(plan, self.plan)
        self.assertEqual((self.output / "material.json").read_bytes(), self.material_path.read_bytes())
        self.assertEqual((self.output / "arms.json").read_bytes(), self.arms_path.read_bytes())
        self.assertEqual(plan["arms_sha256"], h.sha(self.arms_path.read_bytes()))
        self.assertEqual(plan["runner_sha256"], h.sha(Path(h.__file__).read_bytes()))
        self.assertEqual(plan["runner_sha256"], plan["helper_sha256"])
        with self.assertRaisesRegex(ValueError, "OCCURRENCE_EXISTS"):
            h.initialize(self.repo, self.output, self.material_path, self.arms_path)
        for name in ("material.json", "arms.json"):
            with self.subTest(file=name):
                other = Path(self.temp.name) / ("clobber-" + name)
                other.mkdir()
                shutil.copy(self.output / "material.json", other / "material.json")
                shutil.copy(self.output / "arms.json", other / "arms.json")
                target = other / name
                target.write_bytes(target.read_bytes() + b" ")
                with self.assertRaises(ValueError):
                    h.initialize(self.repo, other, self.material_path, self.arms_path)
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
            "bad_study_id": lambda m: m.update(study_id="not a study id"),
        }
        for name, mutate in mutations.items():
            with self.subTest(case=name):
                bad = deepcopy(self.material)
                mutate(bad)
                source = Path(self.temp.name) / (name + ".json")
                source.write_text(json.dumps(bad), encoding="utf-8")
                with self.assertRaises(ValueError):
                    h.initialize(self.repo, Path(self.temp.name) / name, source, self.arms_path)

    def test_cycle_is_a_whole_template_invocation_with_distinct_node_coordinates(self):
        for cycle, template in enumerate(("five", "six", "seven"), 1):
            for _ in range(30):
                wave = h.prepare_wave(self.repo, self.output, "sample", cycle)
                if not wave["coordinates"]:
                    break
                self.assertLessEqual(len(wave["coordinates"]), h.wave_capacity(self.plan["arms"]))
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
                self.assertEqual(len(h.nodes_for(self.material, self.material["problems"][0],
                                                 coord["arm"], 1, self.plan["arms"])), 1)
            request = wrapper["provider_payload"]
            self.assertEqual(request["max_tokens"], 8192)
            self.assertEqual(request["response_format"], {"type": "json_object"})
            # Thinking controls are the DeepSeek family's; every arm here is on it.
            self.assertEqual(request["thinking"],
                             {"type": "enabled" if coord["arm"] == "native" else "disabled"})
            self.assertEqual("reasoning_effort" in request, coord["arm"] == "native")
            if coord["arm"] == "native":
                self.assertEqual(request["reasoning_effort"], "low")
            self.assertEqual(wrapper["settings"]["endpoint_name"], ALPHA.name)
            self.assertEqual(wrapper["settings"]["family"], "deepseek")
            self.assertEqual(self.plan["ceilings"][coord["arm"]],
                             {"max_tokens": 8192, "timeout_seconds": 180, "seed": None})
        for invocation in h.audit(self.repo, self.output)["invocations"]:
            if invocation["arm"] in ("bare", "native"):
                self.assertEqual(invocation["nodes"], 1)
                self.assertEqual(invocation["template_id"], invocation["arm"] + "1")
            self.assertEqual(invocation["endpoint"], ALPHA.name)

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
        for side in ("both", "response"):
            with self.subTest(record=side):
                output = Path(self.temp.name) / ("coordinate-mismatch-" + side)
                h.initialize(self.repo, output, self.material_path, self.arms_path)
                wave = h.prepare_wave(self.repo, output, "sample", 1)
                FakeProvider.coordinate_mismatch = side
                before = FakeProvider.calls
                receipts = h.send_wave(self.repo, output, wave["wave_id"],
                                       provider_factory=FakeProvider, publication_check=self.published,
                                       notify=lambda line: None)
                self.assertEqual(FakeProvider.calls - before, 5)
                self.assertEqual({row["status"] for row in receipts}, {"FAILED"})
                for coord in wave["coordinates"]:
                    record = h.load(h.provider_dir(output, coord) / "call-0001.response.json")
                    self.assertEqual(h.at(output, "responses", coord, "txt").read_bytes(),
                                     record["content"].encode("utf-8"))
                    self.assertFalse(h.at(output, "artifacts", coord).exists())
                with self.assertRaises(FileExistsError):
                    h.send_wave(self.repo, output, wave["wave_id"],
                                provider_factory=FakeProvider, publication_check=self.published,
                                notify=lambda line: None)
                self.assertEqual(FakeProvider.calls - before, 5)
                FakeProvider.coordinate_mismatch = None

    def test_required_publication_paths_include_transitive_provider_and_artifact_bytes(self):
        self.first_wave()
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        required = set(h.required_paths(self.repo, self.output, wave))
        self.assertIn(self.output / "arms.json", required)
        self.assertIn(self.repo / h.PROVIDER_MODULE_PATH, required)
        self.assertIn(self.repo / h.ENDPOINT_REGISTRY_PATH, required)
        for arm in ("matched", "mini_prose", "mini_fcl"):
            parent = self.coord(arm)
            for category in ("requests", "traces", "attempts", "responses", "artifacts"):
                self.assertIn(h.at(self.output, category, parent), required)
            self.assertIn(h.at(self.output, "responses", parent, "txt"), required)
            for filename in ("call-0001.request.json", "call-0001.response.json"):
                self.assertIn(h.provider_dir(self.output, parent) / filename, required)

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
        receipt = h.load(h.at(self.output, "responses", self.coord("mini_prose")))
        self.assertEqual(receipt["finish_reason"], "length")
        self.assertEqual(receipt["usage"]["completion_tokens"], 8192)
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
        settings = self.settings()
        payload = h.payload_for([{"role": "user", "content": "Synthetic json request"}], settings)
        samples = [
            (json.dumps({"body": "Authored body π", "commitments": "Different commitment"}), False, "AUTHORED", "Authored body π", "Different commitment"),
            ("exact opaque text\r\nwith π and trailing spaces  ", False, "OPAQUE", "exact opaque text\r\nwith π and trailing spaces  ", ""),
            ('{"body":"text","commitments":17}', False, "OPAQUE", '{"body":"text","commitments":17}', ""),
            (json.dumps({"body": "Admitted partial body", "commitments": "Partial commitment"}), True, "AUTHORED", "Admitted partial body", "Partial commitment"),
        ]
        for content, partial, status, body, commitments in samples:
            with self.subTest(envelope=status, partial=partial, content=content):
                record = response_record(payload, settings, content, partial=partial)
                original = deepcopy(record)
                artifact = h.decode_contribution(record, payload, settings)
                self.assertEqual(record, original)
                self.assertEqual(artifact["body"], body)
                self.assertEqual(artifact["commitments"], commitments)
                self.assertEqual(artifact["delivery_status"], "PARTIAL" if partial else "COMPLETE")
                self.assertEqual(artifact["envelope_status"], status)
                self.assertEqual(artifact["envelope_repairs"], [])
                self.assertEqual(artifact["strict_parse_would_succeed"], status == "AUTHORED")
                for name, text in (("public_text", content), ("body", body), ("commitments", commitments)):
                    self.assertEqual(artifact[name + "_sha256"], hashlib.sha256(text.encode("utf-8")).hexdigest())

    def test_decode_refuses_custody_delivery_and_hidden_reasoning_mismatches(self):
        settings = self.settings()
        payload = h.payload_for([{"role": "user", "content": "Synthetic json request"}], settings)
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


class PublicationRefTests(ForkTestCase):
    """MULTI (c): the publication ref is configurable, and bytes still decide."""

    def checkout(self):
        fake_repo = Path(self.temp.name) / "publication-checkout"
        fake_helper = fake_repo / "tools" / "multicycle_commitment_study_multi.py"
        fake_helper.parent.mkdir(parents=True)
        fake_helper.write_bytes(Path(h.__file__).read_bytes())
        for relative in ("tools/multicycle_language_probe.py", "src/minireason/provider.py",
                         h.PROVIDER_MODULE_PATH, h.ENDPOINT_REGISTRY_PATH):
            destination = fake_repo / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((self.repo / relative).read_bytes())
        return fake_repo, fake_helper

    def test_publication_checks_actual_bytes_and_the_configured_ref_without_git_mutation(self):
        fake_repo, fake_helper = self.checkout()
        output = fake_repo / "occurrence"
        upstream = "origin/claude/project-state-direction-j5rbun"
        with patch.object(h, "__file__", str(fake_helper)):
            h.initialize(fake_repo, output, self.material_path, self.arms_path)
            wave = h.prepare_wave(fake_repo, output, "sample", 1)
            required = h.required_paths(fake_repo, output, wave)
            committed = {p.relative_to(fake_repo).as_posix(): p.read_bytes() for p in required}
            head = "a" * 40
            calls = []
            def git_bytes(repo, *args):
                self.assertEqual(Path(repo), fake_repo)
                calls.append(args)
                if args == ("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"):
                    return (upstream + "\n").encode("ascii")
                if args == ("rev-parse", "HEAD"):
                    return (head + "\n").encode("ascii")
                if args[:3] == ("ls-remote", "--refs", "origin"):
                    return (head + "\t" + args[3] + "\n").encode("ascii")
                if args[0] == "show":
                    commit, relative = args[1].split(":", 1)
                    self.assertEqual(commit, head)
                    return committed[relative]
                raise AssertionError("Unexpected Git command in publication check: " + repr(args))
            with patch.object(h, "git", side_effect=git_bytes):
                # Default: the current branch's upstream, never a hardcoded main.
                self.assertEqual(h.check_published(fake_repo, output, wave), head)
                self.assertIn(("ls-remote", "--refs", "origin",
                               "refs/heads/claude/project-state-direction-j5rbun"), calls)
                self.assertNotIn(("ls-remote", "--refs", "origin", "refs/heads/main"), calls)
                # An explicit ref overrides it.
                calls.clear()
                self.assertEqual(h.check_published(fake_repo, output, wave,
                                                   publish_ref="origin/main"), head)
                self.assertIn(("ls-remote", "--refs", "origin", "refs/heads/main"), calls)
                # Bytes still decide.
                target = h.at(output, "requests", wave["coordinates"][0])
                target.write_bytes(target.read_bytes() + b" ")
                with self.assertRaisesRegex(ValueError, "INPUT_NOT_PUBLISHED"):
                    h.check_published(fake_repo, output, wave, publish_ref=upstream)
            moved = [(upstream + "\n").encode(), (head + "\n").encode(),
                     b"other refs/heads/claude/project-state-direction-j5rbun\n"]
            with patch.object(h, "git", side_effect=moved):
                with self.assertRaisesRegex(ValueError, "PUBLISH_REF_CHANGED"):
                    h.check_published(fake_repo, output, wave)
        self.assertEqual(FakeProvider.calls, 0)

    def test_publish_ref_spellings_are_validated(self):
        self.assertEqual(h.split_publish_ref("origin/main"), ("origin", "refs/heads/main"))
        self.assertEqual(h.split_publish_ref("origin/claude/a-b_c"),
                         ("origin", "refs/heads/claude/a-b_c"))
        for bad in ("main", "", "origin/", "/main", "origin/../x", None, 7):
            with self.subTest(ref=bad), self.assertRaises(ValueError):
                h.split_publish_ref(bad)

    def test_unresolvable_upstream_is_a_refusal_not_a_guess(self):
        with patch.object(h, "git", side_effect=RuntimeError("no upstream")):
            with self.assertRaisesRegex(ValueError, "PUBLISH_REF_UNRESOLVED"):
                h.upstream_ref(Path(self.temp.name))
        with patch.object(h, "git", return_value=b"\n"):
            with self.assertRaisesRegex(ValueError, "PUBLISH_REF_UNRESOLVED"):
                h.upstream_ref(Path(self.temp.name))


class PerKeyConcurrencyTests(ForkTestCase):
    """MULTI (b): five in flight per credential, 5 x keys in total."""

    arms = TWO_KEY_ARMS

    def test_two_keys_reach_ten_in_flight_and_never_exceed_five_per_key(self):
        self.assertEqual(h.wave_capacity(self.plan["arms"]), 10)
        self.assertEqual(self.plan["max_concurrent_requests_per_key_env"],
                         {"DEEPSEEK_API_KEY": 5, "OLLAMA_API_KEY": 5})
        self.assertEqual(self.plan["max_concurrent_requests_total"], 10)
        self.assertEqual(sorted(self.plan["key_environment_names"]),
                         ["DEEPSEEK_API_KEY", "OLLAMA_API_KEY"])
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        self.assertEqual(len(wave["coordinates"]), 10)
        grouped = {}
        for coord in wave["coordinates"]:
            grouped.setdefault(h.arm_key_env(self.plan["arms"], coord["arm"]), []).append(coord)
        self.assertEqual({key: len(rows) for key, rows in grouped.items()},
                         {"DEEPSEEK_API_KEY": 5, "OLLAMA_API_KEY": 5})
        # Ten must be able to overlap; the barrier only clears if they do.
        FakeProvider.barrier = threading.Barrier(10)
        rows = self.send(wave)
        self.assertEqual(len(rows), 10)
        self.assertEqual(FakeProvider.peak, 10)
        self.assertEqual(FakeProvider.active, 0)
        self.assertEqual(FakeProvider.per_key_peak,
                         {"DEEPSEEK_API_KEY": 5, "OLLAMA_API_KEY": 5})
        self.assertLessEqual(max(FakeProvider.per_key_peak.values()), 5)

    def test_one_key_in_a_wave_is_never_widened_past_five(self):
        arms = {name: spec for name, spec in TWO_KEY_ARMS.items() if name.startswith("a")}
        path = Path(self.temp.name) / "one-key-arms.json"
        path.write_text(json.dumps(arms_document(arms)), encoding="utf-8")
        output = Path(self.temp.name) / "one-key"
        plan = h.initialize(self.repo, output, self.material_path, path)
        self.assertEqual(h.wave_capacity(plan["arms"]), 5)
        wave = h.prepare_wave(self.repo, output, "sample", 1)
        self.assertEqual(len(wave["coordinates"]), 5)
        FakeProvider.barrier = threading.Barrier(5)
        self.send(wave, output)
        self.assertEqual(FakeProvider.per_key_peak, {"DEEPSEEK_API_KEY": 5})

    def test_an_oversized_wave_is_refused_before_any_call(self):
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        path = h.wave_path(self.output, wave["wave_id"])
        record = h.load(path)
        extra = dict(record["coordinates"][0])
        record["coordinates"] = record["coordinates"] + [extra]
        path.write_bytes(h.encoded(record))
        with self.assertRaisesRegex(ValueError, "WAVE_SIZE_INVALID"):
            self.send(wave)
        self.assertEqual(FakeProvider.calls, 0)


class ArmDeclarationTests(ForkTestCase):
    """MULTI (a): what a plan may and may not declare."""

    def declare(self, arms, name="decl"):
        path = Path(self.temp.name) / (name + "-arms.json")
        path.write_text(json.dumps(arms_document(arms)), encoding="utf-8")
        return h.initialize(self.repo, Path(self.temp.name) / name, self.material_path, path)

    def test_a_native_arm_is_refused_where_the_family_has_no_thinking_wire(self):
        # `provider_openai_compat` refuses `thinking=` for any family but DeepSeek.
        for endpoint in (BETA.name, "ollama/gemma4-31b", "ollama/gpt-oss-120b.native"):
            with self.subTest(endpoint=endpoint), self.assertRaisesRegex(ValueError, "ARM_NATIVE_WIRE_UNKNOWN"):
                self.declare({"native_x": {"surface": "prose", "kind": "native",
                                           "endpoint": endpoint}}, "native-" + endpoint.replace("/", "_"))
        # And it is accepted on the DeepSeek family.
        plan = self.declare({"native_ok": {"surface": "prose", "kind": "native",
                                           "endpoint": ALPHA.name}}, "native-ok")
        self.assertIs(h.settings_for("native_ok", plan["arms"]).thinking, True)
        self.assertIs(h.settings_for("mini_fcl", self.plan["arms"]).thinking, False)

    def test_unknown_endpoints_surfaces_kinds_and_baseline_surfaces_are_refused(self):
        cases = {
            "UNKNOWN_ENDPOINT": {"x": {"surface": "prose", "kind": "mini", "endpoint": "nope"}},
            "ARM_SURFACE_OR_KIND": {"x": {"surface": "formal", "kind": "mini", "endpoint": ALPHA.name}},
            "ARM_BASELINE_SURFACE": {"x": {"surface": "fcl", "kind": "bare", "endpoint": ALPHA.name}},
            "ARM_FIELDS": {"x": {"surface": "prose", "kind": "mini"}},
            "ARM_CEILING": {"x": {"surface": "prose", "kind": "mini", "endpoint": ALPHA.name,
                                  "max_tokens": 9999}},
            "ARM_SEED": {"x": {"surface": "prose", "kind": "mini", "endpoint": ALPHA.name,
                               "seed": "seven"}},
        }
        for code, arms in cases.items():
            with self.subTest(code=code), self.assertRaisesRegex(ValueError, code):
                self.declare(arms, code.lower())

    def test_arm_names_are_canonicalised_to_what_the_published_importer_accepts(self):
        self.assertEqual(h.canonical_arm("mini_fcl@gpt-oss-120b"), "mini_fcl__gpt-oss-120b")
        self.assertEqual(h.canonical_arm("mini_prose@qwen3.5:397b"), "mini_prose__qwen3_5_397b")
        self.assertEqual(h.canonical_arm("mini_fcl@ollama/gpt-oss-120b"),
                         "mini_fcl__ollama_gpt-oss-120b")
        for name in h.canonical_arm("mini_fcl@ollama/gpt-oss-120b"), "mini_fcl", "bare":
            self.assertRegex(name, importer._SAFE_COMPONENT)
        for bad in ("", "-leading", "a" * 65, "tab\tname"):
            with self.subTest(name=bad), self.assertRaises(ValueError):
                h.canonical_arm(bad)
        plan = self.declare({"mini_fcl@ollama/gpt-oss-120b":
                             {"surface": "fcl", "kind": "mini", "endpoint": BETA.name}}, "declared")
        spec = plan["arms"]["mini_fcl__ollama_gpt-oss-120b"]
        self.assertEqual(spec["declared_name"], "mini_fcl@ollama/gpt-oss-120b")
        self.assertEqual(spec["endpoint"], BETA.name)

    def test_the_published_importer_reads_an_fcl_surface_only_from_the_literal_arm_name(self):
        # A standing finding, pinned so it cannot be discovered after the calls
        # are spent: `graph_import_h005.FCL_SURFACE_ARMS` is an exact-membership
        # tuple, so an arm whose name carries its endpoint is read as a PROSE
        # arm and its FCL-1 document is never parsed. F001 therefore keeps the
        # canonical arm names and puts the endpoint in the occurrence.
        self.assertEqual(importer.FCL_SURFACE_ARMS, ("mini_fcl",))
        self.assertNotIn("mini_fcl__ollama_gpt-oss-120b", importer.FCL_SURFACE_ARMS)

    def test_a_deepseek_arm_is_byte_identical_to_the_owners_runner(self):
        """The fork must not move one byte of the DeepSeek arm it forked from."""
        messages = [{"role": "system", "content": "system json"},
                    {"role": "user", "content": "user"}]
        # `payload_for` from tools/multicycle_commitment_study.py, transcribed.
        owner = {"model": "deepseek-flash", "messages": messages, "stream": False,
                 "max_tokens": 8192, "thinking": {"type": "disabled"},
                 "response_format": {"type": "json_object"}}
        self.assertEqual(h.digest(h.payload_for(messages, self.settings("mini_prose"))),
                         h.digest(owner))
        owner_native = dict(owner, thinking={"type": "enabled"}, reasoning_effort="low")
        self.assertEqual(h.digest(h.payload_for(messages, self.settings("native"))),
                         h.digest(owner_native))
        # And the owner's closed-form call budget, recomputed by the fork's sum.
        material = json.loads((H005 / "material.json").read_bytes())
        self.assertEqual(
            sum(len(h.nodes_for(material, problem, arm, cycle, self.plan["arms"]))
                for problem in material["problems"] for arm in self.plan["arms"]
                for cycle in range(1, len(problem["templates"]) + 1)),
            240)

    def test_per_arm_ceilings_seeds_and_provider_records_reach_the_plan_and_the_wire(self):
        plan = self.declare({"mini_seeded": {"surface": "fcl", "kind": "mini",
                                             "endpoint": BETA.name, "seed": 7,
                                             "max_tokens": 4096}}, "seeded")
        self.assertEqual(plan["ceilings"]["mini_seeded"],
                         {"max_tokens": 4096, "timeout_seconds": 180, "seed": 7})
        settings = h.settings_for("mini_seeded", plan["arms"])
        payload = h.payload_for([{"role": "user", "content": "json please"}], settings)
        self.assertEqual(payload["seed"], 7)
        self.assertEqual(payload["max_tokens"], 4096)
        self.assertNotIn("thinking", payload)
        # The registry records the credential's environment variable NAME and
        # never its value; `write_new` refuses any output that carries one.
        self.assertEqual(plan["providers"][BETA.name]["key_env"], "OLLAMA_API_KEY")
        self.assertEqual(set(plan["providers"][BETA.name]), set(h.ENDPOINT_FIELDS))
        for value in (os.environ["OLLAMA_API_KEY"], os.environ["DEEPSEEK_API_KEY"]):
            self.assertNotIn(value, json.dumps(plan))
        with self.assertRaisesRegex(ValueError, "CREDENTIAL_IN_OUTPUT"):
            h.write_new(Path(self.temp.name) / "leak.json",
                        {"oops": os.environ["OLLAMA_API_KEY"]})


class EnvelopeUnwrapTests(ForkTestCase):
    """MULTI (g): two declared repairs, and nothing else."""

    def decode(self, content, *, arm="mini_prose"):
        settings = self.settings(arm)
        payload = h.payload_for([{"role": "user", "content": "Synthetic json request"}], settings)
        record = response_record(payload, settings, content)
        return h.decode_contribution(record, payload, settings)

    def test_a_single_outer_fence_is_stripped_and_recorded(self):
        inner = json.dumps({"body": "B", "commitments": "C"})
        for text in ("```json\n" + inner + "\n```", "```\n" + inner + "\n```",
                     "  ```json\n" + inner + "\n```  "):
            with self.subTest(text=text):
                result = self.decode(text)
                self.assertEqual(result["envelope_status"], "AUTHORED")
                self.assertEqual(result["body"], "B")
                self.assertEqual(result["commitments"], "C")
                self.assertEqual(result["envelope_repairs"], ["fence_stripped"])
                self.assertFalse(result["strict_parse_would_succeed"])
                # The raw bytes are what is hashed and stored.
                self.assertEqual(result["public_text_sha256"],
                                 hashlib.sha256(text.encode("utf-8")).hexdigest())

    def test_raw_control_characters_inside_a_string_are_parsed_leniently(self):
        text = '{"body": "first\nsecond", "commitments": "c1\nc2"}'
        result = self.decode(text)
        self.assertEqual(result["envelope_status"], "AUTHORED")
        self.assertEqual(result["body"], "first\nsecond")
        self.assertEqual(result["commitments"], "c1\nc2")
        self.assertEqual(result["envelope_repairs"], ["lenient_control_chars"])
        self.assertFalse(result["strict_parse_would_succeed"])

    def test_a_fenced_document_with_control_characters_needs_both_repairs(self):
        text = '```json\n{"body": "a\nb", "commitments": "c\nd"}\n```'
        result = self.decode(text)
        self.assertEqual(result["envelope_repairs"], ["fence_stripped", "lenient_control_chars"])
        self.assertEqual(result["envelope_status"], "AUTHORED")

    def test_nothing_else_is_repaired(self):
        cases = [
            "not json at all",
            '{"body": "only one field"}',
            '{"body": "text", "commitments": 17}',
            '{"body": "a", "commitments": "b", "extra": "c"}',
            '{"body": "a", "body": "a", "commitments": "b"}',
            "```json\n{\"body\": \"a\"}\n```",
            "prose before ```json\n{\"body\":\"a\",\"commitments\":\"b\"}\n``` prose after",
        ]
        for text in cases:
            with self.subTest(text=text):
                result = self.decode(text)
                self.assertEqual(result["envelope_status"], "OPAQUE")
                self.assertEqual(result["body"], text)
                self.assertEqual(result["commitments"], "")
                self.assertEqual(result["envelope_repairs"], [])
                self.assertFalse(result["strict_parse_would_succeed"])

    def test_the_declared_control_character_repair_rescues_the_records_it_cites(self):
        """PLAN.md cites two of the owner's own frozen H005 nodes; this is them.

        A pre-registration that motivates a decode repair with data must name
        the data, and the data must say what the register says it says.
        """
        cited = {"response.txt": "054b1c43c50e4d2a581023dc73cd08439665cf18b7663681559a8ab19345df3a",
                 "carry.txt": "c61e45da74b50542ae5d07b2e4af9a18e0696c789981ca26b42c944ec3913c8e"}
        for name, digest in cited.items():
            with self.subTest(record=name):
                path = H005 / "occurrence-01/responses/daily/matched/cycle01" / name
                raw = path.read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)
                text = raw.decode("utf-8")
                self.assertIn("\n", text)                  # a RAW newline, unescaped
                self.assertIsNone(h.parse_envelope(text, lenient=False))
                envelope, repairs, strict_ok = h.envelope_unwrap(text)
                self.assertEqual(repairs, ["lenient_control_chars"])
                self.assertFalse(strict_ok)
                self.assertEqual(set(envelope), {"body", "commitments"})
                self.assertTrue(envelope["commitments"].strip())
                # And the owner's frozen record shows the loss the repair
                # prevents: OPAQUE, with the sha256 of the empty string.
                receipt = json.loads((path.with_suffix(".json")).read_bytes())
                self.assertEqual(receipt["envelope_status"], "OPAQUE")
                self.assertEqual(receipt["status"], "COMPLETE")

    def test_a_clean_envelope_records_no_repair_and_the_strict_counterfactual(self):
        result = self.decode(json.dumps({"body": "B", "commitments": "C"}))
        self.assertEqual(result["envelope_repairs"], [])
        self.assertTrue(result["strict_parse_would_succeed"])

    def test_repairs_are_receipt_level_and_never_reach_the_artifact_record(self):
        FakeProvider.fenced = True
        self.first_wave()
        for arm in ("mini_prose", "mini_fcl", "matched"):
            coord = self.coord(arm)
            artifact = h.load(h.at(self.output, "artifacts", coord))
            receipt = h.load(h.at(self.output, "responses", coord))
            self.assertEqual(set(artifact) & set(h.REPAIR_FIELDS), set())
            self.assertEqual(receipt["envelope_repairs"], ["fence_stripped"])
            self.assertFalse(receipt["strict_parse_would_succeed"])
            self.assertEqual(artifact["envelope_status"], "AUTHORED")
            self.assertEqual(artifact["body"], "BODY[sample|" + arm + "|1|root]")
            self.assertEqual(artifact["commitments"], "COMMIT[sample|" + arm + "|1|root]")
            # The raw fenced text is on disk untouched.
            raw = h.at(self.output, "responses", coord, "txt").read_bytes().decode("utf-8")
            self.assertTrue(raw.startswith("```json"))
        counts = h.audit(self.repo, self.output)["counts"]
        self.assertEqual(counts["fence_stripped"], 5)
        self.assertEqual(counts["strict_parse_would_succeed"], 0)
        self.assertEqual(counts["OPAQUE"], 0)

    def test_a_tampered_repair_record_fails_terminal_custody(self):
        FakeProvider.fenced = True
        self.first_wave()
        coord = self.coord("mini_prose")
        path = h.at(self.output, "responses", coord)
        receipt = h.load(path)
        receipt["strict_parse_would_succeed"] = True
        path.write_bytes(h.encoded(receipt))
        with self.assertRaisesRegex(ValueError, "ARTIFACT_CUSTODY_MISMATCH"):
            h.read_terminal(self.output, coord, self.plan["arms"])

    def test_reasoning_without_a_thinking_control_is_recorded_not_refused(self):
        # MULTI (i): an Ollama family emits reasoning by default and offers no
        # switch; a DeepSeek arm asked for thinking disabled must still refuse.
        ollama = {"mini_fcl_b": {"surface": "fcl", "kind": "mini", "endpoint": BETA.name}}
        path = Path(self.temp.name) / "ollama-arms.json"
        path.write_text(json.dumps(arms_document(ollama)), encoding="utf-8")
        output = Path(self.temp.name) / "ollama"
        plan = h.initialize(self.repo, output, self.material_path, path)
        FakeProvider.reasoning = True
        wave = h.prepare_wave(self.repo, output, "sample", 1)
        rows = self.send(wave, output)
        self.assertEqual([row["status"] for row in rows], ["COMPLETE"])
        self.assertTrue(h.load(h.at(output, "responses", self.coord("mini_fcl_b")))
                        ["reasoning_content_present"])
        self.assertEqual(h.audit(self.repo, output)["counts"]["reasoning_present"], 1)
        deepseek = h.settings_for("mini_prose", self.plan["arms"])
        payload = h.payload_for([{"role": "user", "content": "json"}], deepseek)
        record = response_record(payload, deepseek, json.dumps({"body": "b", "commitments": "c"}),
                                 reasoning=True)
        with self.assertRaisesRegex(ValueError, "PROVIDER_CONTENT_CUSTODY"):
            h.decode_contribution(record, payload, deepseek)


FCL_DOCUMENTS = {
    "account": {"language": "FCL-1", "records": [
        {"id": "c1", "type": "claim", "text": "A rota that nobody wrote down is not an agreement.",
         "scope": "the shared flat"},
        {"id": "m1", "type": "commitment", "text": "Write the rota down before the next dispute.",
         "action": "record the agreed turns", "consequence": "a turn missed is checkable"}],
        "uptake": ["c1", "m1"]},
    "objection": {"language": "FCL-1", "records": [
        {"id": "o1", "type": "objection", "text": "Writing it down does not settle who agreed.",
         "bearing": "if the claim holds, the remedy still does not follow",
         "target": ["p.objection.0#c1"]}], "uptake": ["o1"]},
    "rival": {"language": "FCL-1", "records": [
        {"id": "r1", "type": "claim", "text": "The dispute is about effort, not about record keeping.",
         "depends": ["p.rival.0#c1"]}], "uptake": ["r1"]},
    "response": {"language": "FCL-1", "records": [
        {"id": "k1", "type": "objection", "text": "Effort is not observable between flatmates.",
         "bearing": "the rival account cannot be checked by the people in it",
         "target": ["p.response.2#r1"]}], "uptake": ["k1"]},
    "carry": {"language": "FCL-1", "records": [
        {"id": "n1", "type": "objection", "text": "Unobservable effort is still argued about daily.",
         "bearing": "the objection to the rival account overstates its own standard",
         "target": ["p.carry.0#k1"]},
        {"id": "u1", "type": "use", "text": "Use the written rota to settle the next missed turn.",
         "depends": ["p.carry.1#m1"]}], "uptake": ["n1", "u1"]},
}


def fcl_commitments(coordinate):
    """An FCL-1 document for the fcl arm; ordinary prose for anything else."""
    if coordinate["arm"] != "mini_fcl":
        return ("I commit to writing the rota down, and I depend on the account of the "
                "dispute given above. This is prose, not FCL-1.")
    document = FCL_DOCUMENTS.get(coordinate["node"])
    if document is None:
        return json.dumps({"language": "FCL-1", "records": [], "uptake": []}, ensure_ascii=False)
    return json.dumps(document, ensure_ascii=False)


class EndToEndImportTests(unittest.TestCase):
    """Byte-compatibility: a fork occurrence is read by the published importer.

    One problem, one fork5 invocation, two arms on two endpoints with two
    credentials, driven through prepare/send for all five nodes, then imported
    with `minireason.graph_import_h005.import_occurrence`.
    """

    @classmethod
    def setUpClass(cls):
        cls.stage = Path(h.__file__).resolve().parents[1]
        cls.temp = tempfile.TemporaryDirectory()
        h.set_registry(REGISTRY)
        FakeProvider.reset()
        FakeProvider.gate = True
        FakeProvider.commitments_for = fcl_commitments
        cls.env = patch.dict(os.environ, {"DEEPSEEK_API_KEY": "synthetic-offline-credential",
                                          "OLLAMA_API_KEY": "synthetic-offline-credential-b"})
        cls.env.start()
        root = Path(cls.temp.name)
        # The owner's H005 material verbatim, plus `study_id` - deliverable 3.
        material = json.loads((H005 / "material.json").read_bytes())
        material["study_id"] = "F001-fork5-multifamily"
        material_path = root / "material.json"
        material_path.write_bytes(h.encoded(material))
        arms = {"mini_fcl": {"surface": "fcl", "kind": "mini", "endpoint": ALPHA.name},
                "mini_prose": {"surface": "prose", "kind": "mini", "endpoint": BETA.name,
                               "seed": 7}}
        arms_path = root / "arms.json"
        arms_path.write_bytes(h.encoded(arms_document(arms)))
        cls.occurrence = root / "occurrence-01"
        cls.plan = h.initialize(cls.stage, cls.occurrence, material_path, arms_path)
        cls.waves = []
        for _ in range(12):
            wave = h.prepare_wave(cls.stage, cls.occurrence, "daily", 1)
            if not wave["coordinates"]:
                break
            cls.waves.append(wave)
            h.send_wave(cls.stage, cls.occurrence, wave["wave_id"],
                        provider_factory=FakeProvider,
                        publication_check=lambda *a: "offline-verified-publication",
                        notify=lambda line: None)
        cls.audit = h.audit(cls.stage, cls.occurrence)
        cls.report = importer.import_occurrence(cls.occurrence, root / "graph-root")

    @classmethod
    def tearDownClass(cls):
        cls.env.stop()
        h.set_registry(None)
        FakeProvider.reset()
        cls.temp.cleanup()

    def test_the_published_importer_is_the_one_under_test(self):
        self.assertEqual(
            hashlib.sha256(Path(importer.__file__).read_bytes()).hexdigest(),
            hashlib.sha256((PUBLISHED / "graph_import_h005.py").read_bytes()).hexdigest())

    def test_all_five_fork5_nodes_ran_on_both_arms_across_two_credentials(self):
        self.assertEqual(self.audit["counts"]["COMPLETE"], 10)
        self.assertEqual(self.audit["counts"]["FAILED"], 0)
        self.assertEqual(self.audit["counts"]["OPAQUE"], 0)
        self.assertEqual(sorted({name for name in FakeProvider.seen}),
                         sorted({ALPHA.name, BETA.name}))
        for arm in ("mini_fcl", "mini_prose"):
            nodes = {c["node"] for c in FakeProvider.sent if c["arm"] == arm}
            self.assertEqual(nodes, {"account", "objection", "rival", "response", "carry"})

    def test_import_verifies_custody_over_every_node(self):
        custody = self.report.custody
        self.assertEqual(custody["plan_id"], self.plan["plan_id"])
        self.assertEqual(custody["material_sha256"], self.plan["material_sha256"])
        for kind in ("cross_file", "self_consistency"):
            for check in custody[kind]:
                with self.subTest(check=check["key"]):
                    self.assertGreater(check["total"], 0)
                    self.assertTrue(check["result"].startswith("verified"))
                    if check["key"] == "projection_source":
                        # The only skips anywhere are the first invocation's
                        # absent `previous`/`origin` slots - structural, and the
                        # same four the owner's occurrence-01 reports.
                        self.assertEqual({row["missing"] for row in check["skipped"]},
                                         {"exposed source (the slot is absent)"})
                        self.assertEqual(len(check["skipped"]), 4)
                        self.assertEqual(check["ran"] + len(check["skipped"]), check["total"])
                    else:
                        self.assertEqual(check["skipped"], [])
                        self.assertEqual(check["ran"], check["total"])

    def test_import_produces_labels_edges_and_a_written_root(self):
        self.assertEqual(len(self.report.scope), 10)
        self.assertTrue(self.report.labels)
        self.assertLessEqual(set(self.report.labels.values()),
                             {"accepted", "refuted", "suspended", "suspended_unsupported"})
        self.assertIn("refuted", self.report.labels.values())
        self.assertIn("accepted", self.report.labels.values())
        self.assertTrue(self.report.att_edges)
        self.assertGreater(self.report.events_count, 0)
        self.assertTrue((Path(self.report.out_root) / "REPORT.md").exists())

    def test_the_fcl_surface_was_read_and_the_prose_surface_was_not(self):
        states = list(self.report.commitment_surface_states.values())
        self.assertEqual(states.count("read_fcl1"), 5)
        self.assertEqual(states.count("prose_not_parsed"), 5)
        self.assertEqual(self.report.residue_totals.get("parse_failure", 0), 0)
        self.assertEqual(self.report.residue_totals.get("schema_failure", 0), 0)
        self.assertEqual(self.report.residue_totals.get("prose_commitment_surface", 0), 5)

    def test_cross_document_references_resolve_and_mint_the_attack_relation(self):
        self.assertEqual(self.report.resolution,
                         {"refs": 12, "resolved": 12, "extensions": 0, "dangling": 0, "task": 0})
        # Three authored criticisms, three warrants: o1 -> account,
        # k1 -> rival, n1 -> the criticism k1 made.
        self.assertEqual(len(self.report.warrants), 3)
        names = {self.report.names[a] + " -> " + self.report.names[b]
                 for a, b in self.report.att_edges}
        self.assertIn("daily/mini_fcl/cycle01/objection -> daily/mini_fcl/cycle01/account", names)
        self.assertIn("daily/mini_fcl/cycle01/response -> daily/mini_fcl/cycle01/rival", names)
        self.assertIn("daily/mini_fcl/cycle01/carry -> nu:response#k1->rival", names)
        # The validity-node closure lifts that onto the carrier.
        self.assertIn("daily/mini_fcl/cycle01/carry -> daily/mini_fcl/cycle01/response", names)
        # The mechanism facts this study exists to compare across families.
        self.assertEqual(self.report.residue_totals["criticism_of_criticism_retargeted"], 1)
        self.assertEqual(self.report.residue_totals["depends_cross_document"], 2)
        self.assertEqual(self.report.residue_totals["validity_node_minted_unasserted"], 3)
        self.assertEqual(self.report.labels[
            self.report.resolve_artifact("daily/mini_fcl/cycle01/account")], "refuted")
        self.assertEqual(self.report.labels[
            self.report.resolve_artifact("daily/mini_prose/cycle01/account")], "accepted")

    def test_the_import_fires_one_error_severity_residue_from_the_fixture(self):
        """The published CLI prints this above the label table; do not omit it."""
        # `rival` depends on `p.rival.0#c1` - a commitment-surface record reached
        # through a projection the brief exposed as BODY only.  That is the
        # scripted document's doing, not the fork's record layout: every custody
        # check still runs, and `parse_failure` / `schema_failure` stay 0.
        self.assertEqual(self.report.residue_totals["ref_through_unexposed_view"], 1)
        self.assertEqual(self.report.residue_totals["ref_unresolved"], 0)
        self.assertEqual(self.report.residue_totals["parse_failure"], 0)

    def test_extra_receipt_fields_do_not_disturb_the_import(self):
        coord = {"problem": "daily", "arm": "mini_fcl", "cycle": 1, "node": "carry"}
        receipt = h.load(h.at(self.occurrence, "responses", coord))
        self.assertIn("envelope_repairs", receipt)
        self.assertIn("strict_parse_would_succeed", receipt)
        self.assertIn("reasoning_content_present", receipt)
        self.assertIn("failure_code", receipt)                       # MULTI (k)
        self.assertIsNone(receipt["failure_code"])
        self.assertEqual(receipt["envelope_repairs"], [])
        self.assertTrue(receipt["strict_parse_would_succeed"])
        # A second import of the same bytes is byte-identical (replay determinism).
        again = importer.import_occurrence(self.occurrence, Path(self.temp.name) / "graph-root-2")
        self.assertEqual(again.labels, self.report.labels)
        self.assertEqual(again.events_count, self.report.events_count)


class PerKeyAdmissionTests(ForkTestCase):
    """MULTI (b), first line: what wave construction admits per credential."""

    arms = TWO_KEY_ARMS

    def test_more_than_five_ready_on_one_key_is_truncated_to_five(self):
        # Seven arms on DEEPSEEK and three on OLLAMA: ten are ready and the
        # total capacity is ten, so ONLY the per-key admission can truncate.
        output, plan = self.occurrence(LOPSIDED_ARMS, "lopsided")
        self.assertEqual(h.wave_capacity(plan["arms"]), 10)
        self.assertEqual(h.key_caps(plan["arms"]),
                         {"DEEPSEEK_API_KEY": 5, "OLLAMA_API_KEY": 5})
        wave = h.prepare_wave(self.repo, output, "sample", 1)
        grouped = {}
        for coord in wave["coordinates"]:
            grouped.setdefault(h.arm_key_env(plan["arms"], coord["arm"]), []).append(coord)
        self.assertEqual({key: len(rows) for key, rows in grouped.items()},
                         {"DEEPSEEK_API_KEY": 5, "OLLAMA_API_KEY": 3})
        self.assertEqual(len(wave["coordinates"]), 8)
        held_back = {"a6_mini_fcl", "a7_mini_fcl"}
        self.assertEqual({c["arm"] for c in wave["coordinates"]} & held_back, set())
        # They are held back, not lost: the queue keeps them until the credential
        # has room, and every arm still runs every node.
        self.send(wave, output)
        self.drain(output)
        report = h.audit(self.repo, output)
        self.assertEqual(report["counts"]["COMPLETE"], 50)     # ten arms, five nodes
        self.assertEqual(report["counts"]["FAILED"], 0)
        self.assertEqual({row["complete"] for row in report["invocations"]
                          if row["cycle"] == 1}, {True})
        # No wave ever put more than five of them in flight on one credential.
        self.assertLessEqual(max(FakeProvider.per_key_peak.values()), 5)
        self.assertEqual(sorted(FakeProvider.per_key_peak),
                         ["DEEPSEEK_API_KEY", "OLLAMA_API_KEY"])

    def test_a_wave_carrying_six_coordinates_on_one_key_is_refused(self):
        # Six on DEEPSEEK and four on OLLAMA: ten in total, within capacity, so
        # only the per-key half of WAVE_SIZE_INVALID can refuse it.
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        path = h.wave_path(self.output, wave["wave_id"])
        record = h.load(path)
        alpha = [c for c in record["coordinates"]
                 if h.arm_key_env(self.plan["arms"], c["arm"]) == "DEEPSEEK_API_KEY"]
        beta = [c for c in record["coordinates"]
                if h.arm_key_env(self.plan["arms"], c["arm"]) == "OLLAMA_API_KEY"]
        record["coordinates"] = alpha + [dict(alpha[0])] + beta[:4]
        self.assertEqual(len(record["coordinates"]), 10)
        path.write_bytes(h.encoded(record))
        with self.assertRaisesRegex(ValueError, "WAVE_SIZE_INVALID"):
            self.send(wave)
        self.assertEqual(FakeProvider.calls, 0)
        self.assertEqual(FakeProvider.constructions, 0)
        self.assertFalse(any((self.output / "attempts").rglob("*.json")))

    def test_an_endpoint_asking_for_less_than_five_narrows_its_key(self):
        narrow = dataclasses.replace(BETA, name="ollama/narrow", key_env="NARROW_API_KEY",
                                     max_concurrency=2)
        h.set_registry({**REGISTRY, narrow.name: narrow})
        arms = {f"n{index}_mini_fcl": {"surface": "fcl", "kind": "mini", "endpoint": narrow.name}
                for index in range(1, 4)}
        output, plan = self.occurrence(arms, "narrow")
        self.assertEqual(plan["max_concurrent_requests_per_key_env"], {"NARROW_API_KEY": 2})
        self.assertEqual(plan["max_concurrent_requests_total"], 2)
        self.assertEqual(h.wave_capacity(plan["arms"]), 2)
        wave = h.prepare_wave(self.repo, output, "sample", 1)
        self.assertEqual(len(wave["coordinates"]), 2)


class ProcessWideGateTests(ForkTestCase):
    """MULTI (b), second line: the gate that holds across `send_wave` calls."""

    arms = ALPHA_ARMS

    def test_the_gate_is_one_process_wide_registry_keyed_by_key_env(self):
        first = h.key_gate("SYNTHETIC_KEY_A", 5)
        self.assertIs(h.key_gate("SYNTHETIC_KEY_A", 5), first)
        self.assertIsNot(h.key_gate("SYNTHETIC_KEY_B", 5), first)
        with self.assertRaisesRegex(ValueError, "CONCURRENCY_LIMIT_CONFLICT"):
            h.key_gate("SYNTHETIC_KEY_A", 3)
        for bad in ("", None, 7):
            with self.subTest(key=bad), self.assertRaises(ValueError):
                h.key_gate(bad, 5)

    def test_two_concurrent_send_waves_on_one_key_never_exceed_five_in_flight(self):
        first, _ = self.occurrence(ALPHA_ARMS, "round-a")
        second, _ = self.occurrence(ALPHA_ARMS, "round-b")
        waves = [h.prepare_wave(self.repo, occurrence, "sample", 1)
                 for occurrence in (first, second)]
        for wave in waves:
            self.assertEqual(len(wave["coordinates"]), 5)
        FakeProvider.hold = threading.Event()
        threads, errors = self.spawn([
            (lambda occurrence=occurrence, wave=wave: self.send(wave, occurrence))
            for occurrence, wave in zip((first, second), waves)])
        try:
            self.assertTrue(self.wait_until(lambda: FakeProvider.calls >= 5),
                            "the first five calls never started")
            # Settle: with a gate scoped to one `send_wave` call, the other five
            # would have been admitted by now and both peaks would read ten.
            time.sleep(0.3)
            self.assertEqual(FakeProvider.per_key_active, {"DEEPSEEK_API_KEY": 5})
            self.assertEqual(FakeProvider.peak, 5)
            self.assertEqual(FakeProvider.calls, 5)
            # And the attempt marker is written under the gate, so the five that
            # are waiting have not claimed a coordinate either.
            attempts = len(list((first / "attempts").rglob("*.json"))) + \
                len(list((second / "attempts").rglob("*.json")))
            self.assertEqual(attempts, 5)
        finally:
            FakeProvider.hold.set()
        self.wait_for(threads, errors)
        self.assertEqual(FakeProvider.calls, 10)
        self.assertEqual(FakeProvider.per_key_peak, {"DEEPSEEK_API_KEY": 5})
        self.assertEqual(FakeProvider.active, 0)
        for occurrence in (first, second):
            self.assertEqual(len(list((occurrence / "responses").rglob("*.json"))), 5)

    def test_two_concurrent_send_waves_on_two_keys_reach_ten(self):
        first, _ = self.occurrence(ALPHA_ARMS, "keys-a")
        second, _ = self.occurrence(BETA_ARMS, "keys-b")
        waves = [h.prepare_wave(self.repo, occurrence, "sample", 1)
                 for occurrence in (first, second)]
        # The barrier only clears if all ten are in flight at once.
        FakeProvider.barrier = threading.Barrier(10)
        threads, errors = self.spawn([
            (lambda occurrence=occurrence, wave=wave: self.send(wave, occurrence))
            for occurrence, wave in zip((first, second), waves)])
        self.wait_for(threads, errors)
        self.assertEqual(FakeProvider.peak, 10)
        self.assertEqual(FakeProvider.per_key_peak,
                         {"DEEPSEEK_API_KEY": 5, "OLLAMA_API_KEY": 5})
        self.assertEqual(FakeProvider.calls, 10)

    def test_send_round_sends_several_occurrences_against_one_commit(self):
        first, _ = self.occurrence(ALPHA_ARMS, "send-round-a")
        second, _ = self.occurrence(BETA_ARMS, "send-round-b")
        third, _ = self.occurrence(ALPHA_ARMS, "send-round-c")
        for occurrence in (first, second):
            h.prepare_wave(self.repo, occurrence, "sample", 1)
        # `third` has no prepared wave: a round reports it and sends nothing.
        FakeProvider.barrier = threading.Barrier(10)
        rows = h.send_round(self.repo, [first, second, third],
                            provider_factory=FakeProvider, publication_check=self.published,
                            notify=lambda line: None)
        self.assertEqual(sorted(rows), sorted(p.as_posix() for p in (first, second, third)))
        self.assertEqual(rows[third.as_posix()], {"wave_id": None, "terminal": 0, "statuses": []})
        for occurrence in (first, second):
            self.assertEqual(rows[occurrence.as_posix()]["terminal"], 5)
            self.assertEqual(set(rows[occurrence.as_posix()]["statuses"]), {"COMPLETE"})
        self.assertEqual(FakeProvider.calls, 10)
        self.assertEqual(FakeProvider.per_key_peak,
                         {"DEEPSEEK_API_KEY": 5, "OLLAMA_API_KEY": 5})
        # A repeated round replays nothing: every coordinate already has a receipt.
        FakeProvider.barrier = None
        again = h.send_round(self.repo, [first, second],
                             provider_factory=FakeProvider, publication_check=self.published,
                             notify=lambda line: None)
        self.assertEqual({row["wave_id"] for row in again.values()}, {None})
        self.assertEqual(FakeProvider.calls, 10)
        with self.assertRaisesRegex(ValueError, "OCCURRENCE_REPEATED"):
            h.send_round(self.repo, [first, first], provider_factory=FakeProvider,
                         publication_check=self.published, notify=lambda line: None)
        # A path that is not an occurrence is an error in its own row, never a
        # quiet "nothing prepared".
        missing = Path(self.temp.name) / "not-an-occurrence"
        row = h.send_round(self.repo, [missing], provider_factory=FakeProvider,
                           publication_check=self.published, notify=lambda line: None)
        self.assertIn("error", row[missing.as_posix()])
        self.assertEqual(FakeProvider.calls, 10)


class WaveSafetyInvariantTests(ForkTestCase):
    """The three declared refusals that guard a wave, each with zero calls."""

    def test_a_prepared_wave_that_was_not_sent_blocks_the_next_prepare(self):
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        self.assertTrue(wave["coordinates"])
        with self.assertRaisesRegex(ValueError, "PREPARED_WAVE_PENDING"):
            h.prepare_wave(self.repo, self.output, "sample", 1)
        self.assertEqual(FakeProvider.calls, 0)
        self.assertEqual(len(list((self.output / "waves").glob("wave*.json"))), 1)
        # Once it is sent, the next wave is prepared normally.
        self.send(wave)
        self.assertTrue(h.prepare_wave(self.repo, self.output, "sample", 1)["coordinates"])

    def test_an_attempt_with_no_receipt_stops_the_arm_before_any_new_wave(self):
        h.write_new(h.at(self.output, "attempts", self.coord("mini_prose")),
                    {"schema": "minireason.h005.attempt.v1",
                     "coordinate": self.coord("mini_prose"), "started_utc": "synthetic"})
        with self.assertRaisesRegex(ValueError, "UNRESOLVED_ATTEMPT"):
            h.prepare_wave(self.repo, self.output, "sample", 1)
        self.assertEqual(FakeProvider.calls, 0)
        self.assertFalse(any((self.output / "waves").glob("wave*.json")))
        counts = h.audit(self.repo, self.output)["counts"]
        self.assertEqual(counts["unresolved_attempts"], 1)

    def test_a_wave_whose_coordinates_drifted_is_refused_before_any_call(self):
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        path = h.wave_path(self.output, wave["wave_id"])
        record = h.load(path)
        stale = dict(self.coord("mini_fcl", "body_view"))
        record["coordinates"] = [c for c in record["coordinates"]
                                 if not (c["arm"] == "mini_fcl" and c["node"] == "root")] + [stale]
        self.assertEqual(len(record["coordinates"]), len(wave["coordinates"]))
        path.write_bytes(h.encoded(record))
        with self.assertRaisesRegex(ValueError, "WAVE_NOT_DEPENDENCY_READY"):
            self.send(wave)
        self.assertEqual(FakeProvider.calls, 0)
        self.assertEqual(FakeProvider.constructions, 0)
        self.assertFalse(any((self.output / "attempts").rglob("*.json")))


class RegistrySeamTests(ForkTestCase):
    """MULTI (a): `set_registry` is the only seam, and it is honoured whole."""

    PUBLIC = ("settings_for", "read_arms", "occurrence_arms", "initialize", "verify",
              "plan_body", "render_node", "ready_coordinates", "prepare_wave",
              "wave_capacity", "key_caps", "arm_key_env", "required_paths",
              "read_terminal", "read_artifact", "send_wave", "send_round", "audit")

    def test_no_public_function_takes_a_second_registry(self):
        for name in self.PUBLIC:
            with self.subTest(function=name):
                self.assertNotIn("registry", inspect.signature(getattr(h, name)).parameters)

    def test_every_resolution_follows_the_installed_registry(self):
        h.prepare_wave(self.repo, self.output, "sample", 1)
        # A registry that no longer carries the arms' endpoint must refuse
        # everywhere rather than let one path resolve and another not.
        h.set_registry({"ollama/gemma4-31b": REGISTRY["ollama/gemma4-31b"]})
        for name, call in (
                ("settings_for", lambda: h.settings_for("mini_prose", self.plan["arms"])),
                ("key_caps", lambda: h.key_caps(self.plan["arms"])),
                ("wave_capacity", lambda: h.wave_capacity(self.plan["arms"])),
                ("verify", lambda: h.verify(self.repo, self.output)),
                ("render_node", lambda: h.render_node(self.repo, self.output,
                                                      self.coord("mini_prose"))),
                ("prepare_wave", lambda: h.prepare_wave(self.repo, self.output, "sample", 1)),
                ("audit", lambda: h.audit(self.repo, self.output))):
            with self.subTest(function=name), self.assertRaises(ValueError):
                call()
        self.assertEqual(FakeProvider.calls, 0)


class ProviderFailureTests(ForkTestCase):
    """MULTI (k): what a failed call records, and what it costs the arm."""

    def test_a_provider_failure_records_its_code_and_ends_that_arm(self):
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        FakeProvider.failure = ("HTTP_429", "rate limited by the endpoint")
        FakeProvider.fail_arms = ("mini_prose",)
        rows = self.send(wave)
        failed = [row for row in rows if row["coordinate"]["arm"] == "mini_prose"]
        self.assertEqual(len(failed), 1)
        self.assertEqual(failed[0]["status"], "FAILED")
        self.assertEqual(failed[0]["failure_type"], "ProviderFailure")
        self.assertEqual(failed[0]["failure_code"], "HTTP_429")
        self.assertEqual({row["status"] for row in rows if row is not failed[0]}, {"COMPLETE"})
        receipt = h.load(h.at(self.output, "responses", self.coord("mini_prose")))
        self.assertEqual(receipt["failure_code"], "HTTP_429")
        # The code is not in the message alone: a rate limit and a key problem
        # are distinguishable from the receipt, without opening the records.
        FakeProvider.failure = ("KEY_MISSING", "the variable is not set")
        FakeProvider.fail_arms = ("matched",)
        following = h.prepare_wave(self.repo, self.output, "sample", 1)
        self.assertNotIn("mini_prose", {c["arm"] for c in following["coordinates"]})
        self.send(following)
        self.assertEqual(h.load(h.at(self.output, "responses", self.coord("matched", "body_view")))
                         ["failure_code"], "KEY_MISSING")
        # One FAILED node ends the arm: no later wave carries it, and the audit
        # is where that shows - FAILED, `unvisited` nodes, `complete: false`.
        FakeProvider.failure = None
        FakeProvider.fail_arms = ()
        for _ in range(12):
            wave = h.prepare_wave(self.repo, self.output, "sample", 1)
            if not wave["coordinates"]:
                break
            self.assertEqual({c["arm"] for c in wave["coordinates"]} & {"mini_prose", "matched"},
                             set())
            self.send(wave)
        report = h.audit(self.repo, self.output)
        # One mini_prose node, and the three matched nodes that were already in
        # flight in the wave where matched first failed.
        self.assertEqual(report["counts"]["FAILED"], 4)
        # The rest of both arms is simply never visited - `prepare-wave` returns
        # fewer coordinates and refuses nothing.  In cycle 1 that is mini_prose's
        # four remaining nodes and matched's final node.
        cycle_one_unvisited = [
            (arm, node["id"]) for arm in ("mini_prose", "matched")
            for node in h.nodes_for(self.material, self.material["problems"][0], arm, 1,
                                    self.plan["arms"])
            if not h.at(self.output, "responses", self.coord(arm, node["id"])).exists()]
        self.assertEqual(len(cycle_one_unvisited), 5)
        self.assertEqual(report["counts"]["unvisited"], 48)   # plus cycles 2 and 3
        stopped = [row for row in report["invocations"]
                   if row["arm"] in ("mini_prose", "matched") and row["cycle"] == 1]
        self.assertEqual([row["complete"] for row in stopped], [False, False])
        self.assertLessEqual(max(FakeProvider.per_key_peak.values()), 5)


class ScopeTests(ForkTestCase):
    """MULTI (j): the plan authorises the declared problems and cycles only."""

    def test_a_declared_scope_bounds_the_plan_and_refuses_the_rest(self):
        output, plan = self.occurrence(CANONICAL_ARMS, "scoped",
                                       scope={"problems": ["sample"], "cycles": [1]})
        self.assertEqual(plan["scope"], {"problems": ["sample"], "cycles": [1]})
        # bare 1 + native 1 + matched 5 + mini_prose 5 + mini_fcl 5 on cycle 1.
        self.assertEqual(plan["max_calls"], 17)
        self.assertEqual(plan["max_calls_envelope"], 60)
        self.assertEqual(self.plan["max_calls"], self.plan["max_calls_envelope"])
        for cycle in (2, 3):
            with self.subTest(cycle=cycle), self.assertRaisesRegex(ValueError, "SCOPE_EXCLUDED"):
                h.prepare_wave(self.repo, output, "sample", cycle)
        self.assertEqual(FakeProvider.calls, 0)
        self.drain(output)
        report = h.audit(self.repo, output)
        self.assertEqual(report["scope"], {"problems": ["sample"], "cycles": [1]})
        self.assertEqual(report["counts"]["COMPLETE"], 17)
        self.assertEqual(report["counts"]["unvisited"], 0)
        self.assertEqual(report["counts"]["out_of_scope"], 0)
        self.assertEqual(report["max_calls"], 17)
        # A wave file that names an unauthorised cycle is refused on its own.
        wave = {"schema": "minireason.h005.wave.v1", "wave_id": "wave9999",
                "plan_id": plan["plan_id"], "problem": "sample", "cycle": 2,
                "coordinates": [self.coord("mini_prose", "root", cycle=2)],
                "request_hashes": {}}
        h.write_new(h.wave_path(output, "wave9999"), wave)
        with self.assertRaisesRegex(ValueError, "SCOPE_EXCLUDED"):
            h.send_wave(self.repo, output, "wave9999", provider_factory=FakeProvider,
                        publication_check=self.published, notify=lambda line: None)

    def test_a_malformed_scope_is_refused(self):
        for bad in ({"problems": [], "cycles": [1]}, {"problems": ["sample"], "cycles": []},
                    {"problems": ["sample"]}, {"problems": ["sample"], "cycles": [0]},
                    {"problems": ["sample"], "cycles": ["1"]}, {"problems": "sample", "cycles": [1]},
                    {"problems": ["sample"], "cycles": [1], "arms": ["bare"]}, []):
            with self.subTest(scope=bad), self.assertRaisesRegex(ValueError, "SCOPE_DECLARATION"):
                h.validate_scope(bad)
        with self.assertRaisesRegex(ValueError, "UNKNOWN_PROBLEM"):
            self.occurrence(CANONICAL_ARMS, "absent-problem",
                            scope={"problems": ["not_in_this_material"], "cycles": [1]})
        self.assertIsNone(h.validate_scope(None))


class F001RegisterTests(unittest.TestCase):
    """The staged register itself: what each occurrence is authorised to spend."""

    EXPECTED = {"occurrence-01": {"bare": 1, "native": 1, "mini_fcl": 5, "mini_prose": 5},
                "occurrence-02": {"bare": 1, "mini_fcl": 5, "mini_prose": 5},
                "occurrence-03": {"bare": 1, "mini_fcl": 5, "mini_prose": 5},
                "occurrence-04": {"bare": 1, "mini_fcl": 5, "mini_prose": 5},
                "occurrence-05": {"bare": 1, "mini_fcl": 5, "mini_prose": 5},
                "occurrence-06": {"bare": 1, "mini_fcl": 5, "mini_prose": 5}}

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(h.__file__).resolve().parents[1]
        h.set_registry(None)          # the shipped 24-endpoint registry

    def test_each_occurrence_authorises_exactly_the_declared_calls(self):
        material = json.loads((STUDY / "material.json").read_bytes())
        total = 0
        for name, per_arm in self.EXPECTED.items():
            with self.subTest(occurrence=name):
                plan = h.initialize(self.repo, Path(self.temp.name) / name,
                                    STUDY / "material.json", STUDY / name / "arms.json")
                self.assertEqual(plan["scope"], {"problems": ["daily"], "cycles": [1]})
                self.assertEqual(sorted(plan["arms"]), sorted(per_arm))
                daily = h.problem_for(material, "daily")
                counted = {arm: len(h.nodes_for(material, daily, arm, 1, plan["arms"]))
                           for arm in plan["arms"]}
                self.assertEqual(counted, per_arm)
                self.assertEqual(plan["max_calls"], sum(per_arm.values()))
                self.assertEqual(plan["max_calls_envelope"], 156 + (12 if "native" in per_arm else 0))
                self.assertEqual(sorted(plan["key_environment_names"]),
                                 ["DEEPSEEK_API_KEY"] if name == "occurrence-01"
                                 else ["OLLAMA_API_KEY"])
                self.assertEqual(plan["max_concurrent_requests_total"], 5)
                total += plan["max_calls"]
        self.assertEqual(total, 67)

    def test_the_native_arm_is_declared_only_where_the_wire_supports_it(self):
        for name in self.EXPECTED:
            with self.subTest(occurrence=name):
                _, arms, _ = h.read_arms(STUDY / name / "arms.json")
                families = {h.settings_for(arm, arms).family for arm in arms}
                self.assertEqual(len(families), 1)
                family = families.pop()
                self.assertEqual("native" in arms, family in h.THINKING_WIRE)
                if "native" in arms:
                    self.assertIs(h.settings_for("native", arms).thinking, True)
                    self.assertIs(h.settings_for("bare", arms).thinking, False)
                else:
                    # ARM_NATIVE_WIRE_UNKNOWN: the declaration is refused here.
                    self.assertIsNone(h.settings_for("bare", arms).thinking)
                    with self.assertRaisesRegex(ValueError, "ARM_NATIVE_WIRE_UNKNOWN"):
                        h.validate_arms({"native": {"surface": "prose", "kind": "native",
                                                    "endpoint": arms["bare"]["endpoint"]}},
                                        h.endpoints())


class ForkHygieneTests(ForkTestCase):
    """The claims the header and NOTES.md make about this file."""

    @staticmethod
    def definitions(path):
        source = Path(path).read_text(encoding="utf-8")
        return {node.name: ast.get_source_segment(source, node)
                for node in ast.parse(source).body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}

    def test_every_changed_definition_carries_a_multi_marker(self):
        owner = self.definitions(OWNER_RUNNER)
        fork = self.definitions(Path(h.__file__))
        self.assertEqual([name for name in owner if name not in fork], [])
        identical = sorted(name for name in owner if fork[name] == owner[name])
        changed = sorted(name for name in owner if fork[name] != owner[name])
        self.assertEqual(identical, sorted(
            ["sha", "encoded", "load", "utc", "identifier", "safe_source", "kind",
             "projection_id", "manifest_for", "runtime_pins", "problem_for", "coordinate",
             "label", "provider_dir", "wave_path", "git"]))
        self.assertEqual(len(changed), 25)
        self.assertEqual([name for name in changed if "MULTI" not in fork[name]], [])

    def test_a_credential_too_short_to_be_one_is_not_a_leak(self):
        self.assertEqual(h.MIN_CREDENTIAL_LENGTH, 16)
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "x"}):
            h.write_new(Path(self.temp.name) / "short.json", {"note": "x marks the spot"})
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "0123456789abcdef"}):
            with self.assertRaisesRegex(ValueError, "CREDENTIAL_IN_OUTPUT"):
                h.write_new(Path(self.temp.name) / "long.json", {"note": "0123456789abcdef"})

    def test_a_refused_receipt_never_strands_a_spent_attempt(self):
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        original, refused = h.write_new, []
        def guard(path, value):
            parts = Path(path).parts
            if (parts[-5:-2] == ("responses", "sample", "bare")
                    and parts[-1].endswith(".json") and not refused):
                refused.append(path)
                raise ValueError("CREDENTIAL_IN_OUTPUT")
            return original(path, value)
        with patch.object(h, "write_new", side_effect=guard):
            self.send(wave)
        self.assertEqual(len(refused), 1)
        receipt = h.load(h.at(self.output, "responses", self.coord("bare", "answer")))
        self.assertEqual(receipt["status"], "FAILED")
        self.assertEqual(receipt["validation_failure_type"], "RECEIPT_REFUSED")
        self.assertEqual(h.audit(self.repo, self.output)["counts"]["unresolved_attempts"], 0)

    def test_a_declared_name_must_fold_to_the_arm_it_names(self):
        good = {"mini_fcl@ollama/gpt-oss-120b": {"surface": "fcl", "kind": "mini",
                                                 "endpoint": BETA.name,
                                                 "declared_name": "mini_fcl@ollama/gpt-oss-120b"}}
        arms = h.validate_arms(good, REGISTRY)
        self.assertEqual(arms["mini_fcl__ollama_gpt-oss-120b"]["declared_name"],
                         "mini_fcl@ollama/gpt-oss-120b")
        for bad in ("another_arm", "", "   ", "tab\tname", 7, None, ["mini_fcl"]):
            with self.subTest(declared_name=bad), self.assertRaisesRegex(ValueError, "ARM_DECLARED_NAME"):
                h.validate_arms({"mini_fcl": {"surface": "fcl", "kind": "mini",
                                              "endpoint": BETA.name, "declared_name": bad}},
                                REGISTRY)

    def test_a_mixed_provider_mode_is_refused_not_reduced(self):
        declaration = {"x": {"surface": "fcl", "kind": "mini", "endpoint": ALPHA.name}}
        live = h.validate_arms(declaration, REGISTRY, "live")
        offline = h.validate_arms({"y": dict(declaration["x"])}, REGISTRY, "offline")
        self.assertEqual(h.provider_mode(live), "live")
        self.assertEqual(h.provider_mode(offline), "offline")
        with self.assertRaisesRegex(ValueError, "PROVIDER_MODE_MIXED"):
            h.provider_mode({**live, **offline})

    def test_the_timeout_is_the_endpoints_and_no_arm_may_declare_one(self):
        self.assertEqual(h.ARM_OPTIONAL, {"declared_name", "max_tokens", "seed"})
        with self.assertRaisesRegex(ValueError, "ARM_FIELDS"):
            h.validate_arms({"x": {"surface": "fcl", "kind": "mini", "endpoint": ALPHA.name,
                                   "timeout_seconds": 30}}, REGISTRY)
        self.assertEqual(self.plan["ceilings"]["mini_fcl"]["timeout_seconds"],
                         h.endpoint_record(ALPHA)["timeout_seconds"])

    def test_every_endpoint_names_a_credential_so_no_unkeyed_group_exists(self):
        self.assertEqual(h.arm_key_env(self.plan["arms"], "mini_fcl"), "DEEPSEEK_API_KEY")
        unkeyed = dataclasses.replace(ALPHA)
        object.__setattr__(unkeyed, "key_env", "")
        with self.assertRaisesRegex(ValueError, "ENDPOINT_FIELD_INVALID"):
            h.endpoint_record(unkeyed)
        with self.assertRaisesRegex(ValueError, "INVALID_ENDPOINT_SETTINGS"):
            dataclasses.replace(self.settings(), key_env="")
        self.assertTrue(all(h.endpoint_record(endpoint)["key_env"]
                            for endpoint in oc.ENDPOINTS.values()))

    def test_the_arm_component_rule_bites_where_an_arm_is_not_folded(self):
        # `canonical_arm` folds the one character ARM_COMPONENT rejects, so the
        # rule is an assertion there; in `at()` the arm comes from a coordinate.
        self.assertEqual(h.canonical_arm("mini_prose@qwen3.5:397b"), "mini_prose__qwen3_5_397b")
        self.assertRegex("mini_prose__qwen3_5_397b", h.ID)
        with self.assertRaisesRegex(ValueError, "INVALID_COORDINATE"):
            h.at(self.output, "requests", {"problem": "sample", "arm": "mini.prose",
                                           "cycle": 1, "node": "root"})
        self.assertRegex("mini.prose", h.ID)      # the owner's ID would admit it


if __name__ == "__main__":
    unittest.main()
