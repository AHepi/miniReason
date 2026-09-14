"""Offline tests for the multi-provider H005 fork, runner v3.

v3's whole claim is one sentence: v2's bytes, plus a per-arm wall clock, plus
nothing. This file proves it three ways.

* `V3DiffProofTests` normalises the module docstring away, diffs v3 against the
  published v2 and asserts that the hunks are exactly the eight declared in v3's
  header -- line for line, comments included -- and that every added block
  carries a `# V3` marker.
* `V3TimeoutDeclarationTests` and `V3ClockReachesTheTransportTests` are the
  behaviour: what an arm may declare, what it is refused for, what a plan
  freezes, and what value the transport is actually handed. The registry file
  `src/minireason/data/endpoints.json` is hashed before and after a dispatch and
  must not move: the clock is applied to the resolved `Endpoint` VALUE.
* `V3ParityTests` is the other half of the claim: where no arm declares a clock,
  a v3 plan is a v2 plan in every field but the two runner digests and the
  `plan_id` they feed.

`F002RegisterTests` reads the staged F002 register itself and asserts what each
occurrence is authorised to spend, at which ceiling and under which clock.

No socket is opened: every call goes through `provider_openai_compat`'s own
`OfflineProvider`, so the request bodies, the recorded settings view and the
write-once record layout under test are the real transport's, not a mock's.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
import ast
import dataclasses
import difflib
import hashlib
import inspect
import json
import os
import sys
import tempfile
import unittest

STAGE = Path(__file__).resolve().parents[1]
if str(STAGE) not in sys.path:
    sys.path.insert(0, str(STAGE))

from tools import multicycle_commitment_study_multi_v3 as h
#: v2 itself, so the successor can be compared with what it succeeds, and v1
#: beneath it, so "v3 pins its own bytes" is a claim about all three.
from tools import multicycle_commitment_study_multi_v2 as v2
from tools import multicycle_commitment_study_multi as v1
from minireason import provider_openai_compat as oc

REPO = Path(h.__file__).resolve().parents[1]
V1_RUNNER = REPO / "tools/multicycle_commitment_study_multi.py"
V2_RUNNER = REPO / "tools/multicycle_commitment_study_multi_v2.py"
V3_RUNNER = Path(h.__file__).resolve()
REGISTRY_FILE = REPO / "src/minireason/data/endpoints.json"
STUDY = REPO / "experiments/diagnostics/F002-fork5-raised-clock"

GLM = oc.ENDPOINTS["ollama/glm-5.3"]
KIMI = oc.ENDPOINTS["ollama/kimi-k3"]
REGISTRY = {GLM.name: GLM, KIMI.name: KIMI}

#: What F002 declares, in the fixture's vocabulary.
DECLARED = {"mini_fcl": {"surface": "fcl", "kind": "mini", "endpoint": GLM.name,
                         "max_tokens": 32768, "seed": 7, "timeout_seconds": 600}}
#: The same arm with no clock of its own -- the v2 declaration, verbatim.
UNDECLARED = {"mini_fcl": {"surface": "fcl", "kind": "mini", "endpoint": GLM.name,
                           "max_tokens": 32768, "seed": 7}}


def arms_document(mapping, mode="offline"):
    return {"schema": "minireason.h005.arms.v1", "provider": mode, "arms": deepcopy(mapping)}


def fixture_material():
    """The v2 suite's own synthetic material, with F002's study id.

    The runner refuses a material whose templates do not chain
    (`TEMPLATE_CHAIN`), so the shape is the published suite's, not a stub.
    """
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
            "study_id": "F002-fork5-raised-clock",
            "system": "Common synthetic problem context. Preserve Unicode \u03c0.",
            "prose_instruction": "PROSE_POLICY_MARKER: write prose commitments.",
            "formal_instruction": "FORMAL_POLICY_MARKER: write formal commitments.",
            "bare_instruction": "BARE_POLICY_MARKER: answer the problem directly.",
            "problems": [{"id": "sample", "prose": "ORIGINAL_PROBLEM_MARKER: a shared room.",
                          "templates": ["five", "six", "seven"]}],
            "templates": {"five": {"nodes": nodes}, "six": {"nodes": second},
                          "seven": {"nodes": third}}}


class CapturingProvider(oc.OfflineProvider):
    """The transport's own offline provider, with the endpoint it was handed recorded."""

    seen: list = []

    def __init__(self, endpoint, records):
        type(self).seen.append({"name": endpoint.name,
                                "timeout_seconds": endpoint.timeout_seconds,
                                "is_registry_object": any(endpoint is row for row in REGISTRY.values())})
        super().__init__(endpoint, records, script=())

    def complete(self, messages, **call):
        self._script = [{"content": json.dumps({"body": "BODY", "commitments": "COMMIT"}),
                         "finish_reason": "stop", "returned_model": "offline-fixture",
                         "reasoning_content_present": True,
                         "usage": {"prompt_tokens": 13, "completion_tokens": 9, "total_tokens": 22}}]
        self._used = 0
        return super().complete(messages, **call)


@dataclasses.dataclass(frozen=True)
class ClampingEndpoint:
    """An endpoint type that refuses to carry a raised clock.

    `dataclasses.replace` is an external function on an external class. If the
    resolved endpoint ever stops carrying the field -- a clamp, a slot, a
    stand-in -- v3 must refuse BEFORE the call rather than spend it and fail
    custody on the record afterwards. This is that type.
    """

    name: str
    base_url: str
    model: str
    key_env: str
    family: str
    chat_path: str = "/chat/completions"
    native: bool = False
    max_concurrency: int = 5
    timeout_seconds: int = 180

    def __post_init__(self):
        object.__setattr__(self, "timeout_seconds", 180)   # the clamp


class ForkV3TestCase(unittest.TestCase):
    arms = DECLARED

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = REPO
        h.set_registry(REGISTRY)
        self.addCleanup(h.set_registry, None)
        h._reset_gates()
        self.addCleanup(h._reset_gates)
        self.material_path = Path(self.temp.name) / "source-material.json"
        self.material_path.write_text(json.dumps(fixture_material(), ensure_ascii=False),
                                      encoding="utf-8")
        self.output, self.plan = self.occurrence(self.arms, "declared")
        CapturingProvider.seen = []
        self.env = patch.dict(os.environ, {"OLLAMA_API_KEY": "synthetic-offline-credential"})
        self.env.start()
        self.addCleanup(self.env.stop)

    def occurrence(self, arms, name, mode="offline"):
        path = Path(self.temp.name) / (name + "-arms.json")
        path.write_text(json.dumps(arms_document(arms, mode)), encoding="utf-8")
        output = Path(self.temp.name) / name
        return output, h.initialize(self.repo, output, self.material_path, path)

    def published(self, *args):
        return "offline-verified-publication"

    def send(self, output, wave):
        return h.send_wave(self.repo, output, wave["wave_id"],
                           provider_factory=CapturingProvider,
                           publication_check=self.published, notify=lambda line: None)


class V3TimeoutDeclarationTests(ForkV3TestCase):
    """V3 (c)(d)(e)(f)(g): what an arm may declare, and what a plan then says."""

    def test_the_bound_is_the_transports_own_and_no_default_constant_is_invented(self):
        self.assertEqual(h.MAX_TIMEOUT, 600)
        # Mirrored, not guessed: the transport refuses 601 in two places.
        self.assertIn("1 <= self.timeout_seconds <= 600",
                      inspect.getsource(oc.Endpoint.__post_init__))
        self.assertIn("1 <= self.timeout_seconds <= 600",
                      inspect.getsource(h.EndpointSettings.__post_init__))
        with self.assertRaises(ValueError):
            dataclasses.replace(GLM, timeout_seconds=h.MAX_TIMEOUT + 1)
        # There is no DEFAULT_TIMEOUT: the default is the endpoint record's own.
        self.assertFalse(hasattr(h, "DEFAULT_TIMEOUT"))
        self.assertFalse(hasattr(v2, "MAX_TIMEOUT"))

    def test_a_declared_clock_is_frozen_read_back_and_surfaced_in_the_plan(self):
        self.assertEqual(self.plan["arms"]["mini_fcl"]["timeout_seconds"], 600)
        self.assertEqual(self.plan["ceilings"]["mini_fcl"],
                         {"max_tokens": 32768, "seed": 7, "timeout_seconds": 600})
        self.assertEqual(self.plan["settings"]["mini_fcl"]["timeout_seconds"], 600)
        settings = h.settings_for("mini_fcl", self.plan["arms"])
        self.assertEqual(settings.timeout_seconds, 600)
        self.assertEqual(settings.to_dict()["timeout_seconds"], 600)
        # And it survives the round trip through the occurrence's own bytes.
        _, plan = h.verify(self.repo, self.output)
        self.assertEqual(plan["ceilings"]["mini_fcl"]["timeout_seconds"], 600)

    def test_an_undeclared_clock_freezes_no_key_and_takes_the_endpoint_record(self):
        _, plan = self.occurrence(UNDECLARED, "undeclared")
        self.assertNotIn("timeout_seconds", plan["arms"]["mini_fcl"])
        self.assertEqual(plan["ceilings"]["mini_fcl"]["timeout_seconds"],
                         h.endpoint_record(GLM)["timeout_seconds"])
        self.assertEqual(plan["ceilings"]["mini_fcl"]["timeout_seconds"], 180)
        self.assertEqual(h.settings_for("mini_fcl", plan["arms"]).timeout_seconds, 180)

    def test_an_out_of_range_or_non_integer_clock_is_refused(self):
        for value in (0, -1, 601, 6000, 600.0, "600", None, True):
            with self.subTest(timeout=value):
                declared = {"mini_fcl": {**UNDECLARED["mini_fcl"], "timeout_seconds": value}}
                with self.assertRaisesRegex(ValueError, "ARM_TIMEOUT"):
                    h.validate_arms(declared, REGISTRY)
        # The bounds themselves are admitted.
        for value in (1, 180, 600):
            with self.subTest(timeout=value):
                declared = {"mini_fcl": {**UNDECLARED["mini_fcl"], "timeout_seconds": value}}
                self.assertEqual(h.validate_arms(declared, REGISTRY)["mini_fcl"]["timeout_seconds"],
                                 value)

    def test_v2_refuses_the_very_declaration_v3_accepts(self):
        v2.set_registry(REGISTRY)
        self.addCleanup(v2.set_registry, None)
        self.assertEqual(v2.ARM_OPTIONAL, {"declared_name", "max_tokens", "seed"})
        with self.assertRaisesRegex(ValueError, "ARM_FIELDS"):
            v2.validate_arms(deepcopy(DECLARED), REGISTRY)
        self.assertEqual(h.ARM_OPTIONAL,
                         {"declared_name", "max_tokens", "seed", "timeout_seconds"})
        self.assertEqual(h.validate_arms(deepcopy(DECLARED), REGISTRY)["mini_fcl"]["timeout_seconds"],
                         600)


class V3ClockReachesTheTransportTests(ForkV3TestCase):
    """V3 (h): the value the provider is constructed with, and the file that is not written."""

    def test_the_declared_clock_reaches_the_endpoint_the_provider_is_built_with(self):
        before = hashlib.sha256(REGISTRY_FILE.read_bytes()).hexdigest()
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        receipts = self.send(self.output, wave)
        self.assertEqual([row["status"] for row in receipts], ["COMPLETE"])
        self.assertEqual(len(CapturingProvider.seen), 1)
        self.assertEqual(CapturingProvider.seen[0]["timeout_seconds"], 600)
        self.assertEqual(CapturingProvider.seen[0]["name"], GLM.name)
        # The registry row itself is untouched: a VALUE was replaced, not a file
        # and not a shared object.
        self.assertFalse(CapturingProvider.seen[0]["is_registry_object"])
        self.assertEqual(GLM.timeout_seconds, 180)
        self.assertEqual(h.endpoints()[GLM.name].timeout_seconds, 180)
        self.assertEqual(hashlib.sha256(REGISTRY_FILE.read_bytes()).hexdigest(), before)

    def test_the_written_record_and_the_terminal_custody_check_both_say_600(self):
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        self.send(self.output, wave)
        coord = wave["coordinates"][0]
        record = json.loads((h.provider_dir(self.output, coord) /
                             "call-0001.response.json").read_bytes())
        self.assertEqual(record["settings"]["timeout_seconds"], 600)
        # `read_terminal` compares the record's settings view field for field
        # against `settings.to_dict()`, so this is the custody chain agreeing.
        h.read_terminal(self.output, coord, self.plan["arms"])

    def test_an_endpoint_that_will_not_carry_the_clock_is_refused_before_the_call(self):
        clamped = ClampingEndpoint(name=GLM.name, base_url=GLM.base_url, model=GLM.model,
                                   key_env=GLM.key_env, family=GLM.family)
        self.assertEqual(dataclasses.replace(clamped, timeout_seconds=600).timeout_seconds, 180)
        wave = h.prepare_wave(self.repo, self.output, "sample", 1)
        h.set_registry({GLM.name: clamped})
        with self.assertRaisesRegex(ValueError, "TIMEOUT_NOT_APPLIED"):
            self.send(self.output, wave)
        # The refusal lands before the per-key gate, before the attempt marker
        # and before any provider is constructed: nothing is spent, and no
        # attempt is stranded without a receipt.
        coord = wave["coordinates"][0]
        self.assertEqual(CapturingProvider.seen, [])
        self.assertFalse(h.at(self.output, "attempts", coord).exists())
        self.assertFalse(h.at(self.output, "responses", coord).exists())
        self.assertFalse((h.provider_dir(self.output, coord) /
                          "call-0001.request.json").exists())
        # And the very same wave succeeds once the endpoint can carry the clock.
        h.set_registry(REGISTRY)
        self.assertEqual([row["status"] for row in self.send(self.output, wave)], ["COMPLETE"])


class V3ParityTests(ForkV3TestCase):
    """The other half of the claim: undeclared, v3 plans exactly as v2 plans."""

    def test_where_no_arm_declares_a_clock_v3_plans_like_v2(self):
        v2.set_registry(REGISTRY)
        self.addCleanup(v2.set_registry, None)
        path = Path(self.temp.name) / "parity-arms.json"
        path.write_text(json.dumps(arms_document(UNDECLARED)), encoding="utf-8")
        three = h.initialize(self.repo, Path(self.temp.name) / "parity-v3",
                             self.material_path, path)
        two = v2.initialize(self.repo, Path(self.temp.name) / "parity-v2",
                            self.material_path, path)
        moved = sorted(key for key in set(three) | set(two) if three.get(key) != two.get(key))
        self.assertEqual(moved, ["helper_sha256", "plan_id", "runner_sha256"])
        self.assertEqual(three["arms"], two["arms"])
        self.assertEqual(three["ceilings"], two["ceilings"])
        self.assertEqual(three["settings"], two["settings"])
        self.assertEqual(three["manifests"], two["manifests"])

    def test_a_declared_clock_is_the_only_thing_that_moves_a_plan_otherwise(self):
        _, undeclared = self.occurrence(UNDECLARED, "undeclared-plan")
        moved = sorted(key for key in set(self.plan) | set(undeclared)
                       if self.plan.get(key) != undeclared.get(key))
        self.assertEqual(moved, ["arms", "arms_sha256", "ceilings", "plan_id", "settings"])


class V3DiffProofTests(unittest.TestCase):
    """The whole v3 claim: v2's bytes plus exactly the hunks the header declares."""

    #: (removed lines, added lines) per hunk, EXACTLY as they appear in the two
    #: files, comments included and indentation preserved. v2's own proof
    #: excluded comments and forbade removing one; this one declares them, so a
    #: comment v3 rewrites is on the record rather than outside the proof.
    DECLARED_HUNKS = (
        # (b) the one new name, and the transport's own idiom for it.
        (("from dataclasses import asdict, dataclass",),
         ("from dataclasses import asdict, dataclass, replace   # V3 (b)",)),
        # (c) the bound, mirrored from the transport; no default constant.
        ((),
         ("# V3 (c): the wall clock becomes a per-arm declaration.  The bound is the",
          "# transport's own - `Endpoint.__post_init__` and `EndpointSettings`",
          "# both admit 1..600 and refuse 601 - and there is deliberately no default",
          "# constant beside it: an arm that declares no clock takes the endpoint",
          "# record's own value, which is how v2 settles every arm.",
          "MAX_TIMEOUT = 600")),
        # (d) the vocabulary an arm declaration is validated against.
        (("ARM_OPTIONAL = {'declared_name', 'max_tokens', 'seed'}",),
         ("ARM_OPTIONAL = {'declared_name', 'max_tokens', 'seed', 'timeout_seconds'}  # V3 (d)",)),
        # (e) read and bound.
        ((),
         ("        # V3 (e): the wall clock, read from the arm where it is declared and",
          "        # from the endpoint record otherwise, bounded by the transport's own",
          "        # maximum rather than by a figure this file invents.",
          "        timeout = spec.get('timeout_seconds', record['timeout_seconds'])",
          "        if type(timeout) is not int or not 1 <= timeout <= MAX_TIMEOUT:",
          "            raise ValueError('ARM_TIMEOUT')")),
        # (e) frozen, and only where it was declared.
        ((),
         ("        # V3 (e): a DECLARED clock is frozen beside the ceiling; an arm that",
          "        # declares none carries no key at all, so a v3 plan built from a v2",
          "        # arms.json is v2's plan in every field but the runner digests.",
          "        if 'timeout_seconds' in spec:",
          "            arms[canonical]['timeout_seconds'] = timeout")),
        # (f) the arm's clock, or the endpoint record's.
        (("        max_concurrency=record['max_concurrency'], timeout_seconds=record['timeout_seconds'],",),
         ("        max_concurrency=record['max_concurrency'],",
          "        # V3 (f): the arm's declared clock, or the endpoint record's.",
          "        timeout_seconds=spec.get('timeout_seconds', record['timeout_seconds']),")),
        # (g) the sentence in `plan_body` that v3 makes false.
        (("            # `max_tokens` and `seed` are the arm's own declarations; the",
          "            # timeout is surfaced per arm but READ FROM THE ENDPOINT - it is not",
          "            # in ARM_OPTIONAL and no arm declaration can change it."),
         ("            # V3 (g): `max_tokens`, `seed` AND the timeout are the arm's own",
          "            # declarations now; an arm that declares no clock still surfaces",
          "            # the endpoint record's, which is what v2 surfaced for every arm.")),
        # (h) applied to the resolved value, and refused if it did not take.
        (("        endpoint = resolved[settings.endpoint]",),
         ("        # V3 (h): the arm's clock is applied to the resolved `Endpoint` value",
          "        # here, by `dataclasses.replace`, so that `endpoints.json` - a pinned",
          "        # published file other plans hash - is never written.  The refusal",
          "        # below ties the value the transport is about to receive to the arm's",
          "        # frozen declaration; the provider then records it, and",
          "        # `decode_contribution` compares that record against `to_dict()`.",
          "        endpoint = replace(resolved[settings.endpoint],",
          "                           timeout_seconds=settings.timeout_seconds)",
          "        if endpoint.timeout_seconds != settings.timeout_seconds:",
          "            raise ValueError('TIMEOUT_NOT_APPLIED')")),
    )

    @staticmethod
    def body(path):
        """The file with its module docstring normalised away -- difference (a)."""
        text = Path(path).read_text(encoding="utf-8")
        docstring = ast.parse(text).body[0]
        assert isinstance(docstring, ast.Expr) and isinstance(docstring.value, ast.Constant)
        return text.splitlines(keepends=True)[docstring.end_lineno:]

    @staticmethod
    def definitions(path):
        source = Path(path).read_text(encoding="utf-8")
        return {node.name: ast.get_source_segment(source, node)
                for node in ast.parse(source).body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}

    def hunks(self):
        diff = list(difflib.unified_diff(self.body(V2_RUNNER), self.body(V3_RUNNER),
                                         "v2", "v3", n=0))
        self.assertEqual(diff[:2], ["--- v2\n", "+++ v3\n"])
        groups, current = [], None
        for line in diff[2:]:
            if line.startswith("@@"):
                current = ([], [])
                groups.append(current)
            elif line.startswith("-"):
                current[0].append(line[1:].rstrip("\n"))
            elif line.startswith("+"):
                current[1].append(line[1:].rstrip("\n"))
            else:                                  # no context line exists at n=0
                self.fail("unexpected diff line: %r" % line)
        return groups

    def test_v3_is_v2_plus_exactly_the_declared_hunks_and_nothing_else(self):
        groups = self.hunks()
        self.assertEqual(len(groups), len(self.DECLARED_HUNKS))
        for index, ((removed, added), declared) in enumerate(zip(groups, self.DECLARED_HUNKS)):
            with self.subTest(hunk=index):
                self.assertEqual(tuple(removed), declared[0])
                self.assertEqual(tuple(added), declared[1])
                # Every hunk is marked in the source, as the header claims.
                self.assertIn("# V3", "\n".join(added))

    def test_only_the_declared_definitions_differ_from_v2(self):
        two = self.definitions(V2_RUNNER)
        three = self.definitions(V3_RUNNER)
        self.assertEqual(sorted(two), sorted(three))
        self.assertEqual(sorted(name for name in two if two[name] != three[name]),
                         ["plan_body", "send_wave", "settings_for", "validate_arms"])
        for name in ("plan_body", "send_wave", "settings_for", "validate_arms"):
            self.assertIn("# V3", three[name])

    def test_the_header_says_v3_names_the_v2_bytes_and_lists_every_difference(self):
        self.assertTrue(h.__doc__.startswith("H005 multi-provider fork v3:"),
                        h.__doc__.split("\n", 1)[0])
        self.assertIn(hashlib.sha256(V2_RUNNER.read_bytes()).hexdigest(), h.__doc__)
        for letter in ("(a)", "(b)", "(c)", "(d)", "(e)", "(f)", "(g)", "(h)"):
            self.assertIn(letter, h.__doc__)
        self.assertIn("MAX_TIMEOUT = 600", h.__doc__)
        self.assertIn("TIMEOUT_NOT_APPLIED", h.__doc__)
        # v2's own header survives intact underneath the provenance block, and
        # v1's beneath that, so the whole chain is readable in one file.
        self.assertIn(v2.__doc__.split("\n", 1)[1].strip(), h.__doc__)
        self.assertIn(v1.__doc__.split("\n", 1)[1].strip(), h.__doc__)

    def test_v3_pins_its_own_bytes_so_no_plan_can_collide_with_v1s_or_v2s(self):
        digests = {name: hashlib.sha256(path.read_bytes()).hexdigest()
                   for name, path in (("v1", V1_RUNNER), ("v2", V2_RUNNER), ("v3", V3_RUNNER))}
        self.assertEqual(len(set(digests.values())), 3, digests)
        self.assertIn("'runner_sha256': sha(Path(__file__).read_bytes())",
                      V3_RUNNER.read_text(encoding="utf-8"))

    def test_the_motive_is_the_published_failure_and_the_header_names_it(self):
        # The two F001 failures v3 exists to answer: a wall clock, not a ceiling.
        self.assertIn("TRANSPORT_OR_RESPONSE_ERROR", h.__doc__)
        self.assertIn("180,368", h.__doc__)
        self.assertIn("180,456", h.__doc__)


class F002RegisterTests(unittest.TestCase):
    """The staged register itself: what each occurrence may spend, and how."""

    EXPECTED = {"occurrence-01": "ollama/glm-5.3", "occurrence-02": "ollama/kimi-k3"}

    def setUp(self):
        if not STUDY.exists():
            self.skipTest("F002 register is not staged in this checkout")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        h.set_registry(None)          # the shipped registry
        self.addCleanup(h.set_registry, None)

    def test_the_material_is_f001s_material_with_one_key_changed(self):
        f002 = json.loads((STUDY / "material.json").read_bytes())
        f001 = json.loads((REPO / "experiments/diagnostics/F001-fork5-multifamily"
                                  "/material.json").read_bytes())
        self.assertEqual(f002["study_id"], "F002-fork5-raised-clock")
        self.assertEqual({k: v for k, v in f002.items() if k != "study_id"},
                         {k: v for k, v in f001.items() if k != "study_id"})

    def test_each_occurrence_authorises_five_calls_at_32768_under_a_600_second_clock(self):
        total = 0
        for name, endpoint in self.EXPECTED.items():
            with self.subTest(occurrence=name):
                plan = h.initialize(REPO, Path(self.temp.name) / name,
                                    STUDY / "material.json", STUDY / name / "arms.json")
                self.assertEqual(sorted(plan["arms"]), ["mini_fcl"])
                self.assertEqual(plan["arms"]["mini_fcl"]["endpoint"], endpoint)
                self.assertEqual(plan["scope"], {"problems": ["daily"], "cycles": [1]})
                self.assertEqual(plan["ceilings"]["mini_fcl"],
                                 {"max_tokens": 32768, "seed": 7, "timeout_seconds": 600})
                self.assertEqual(plan["max_calls"], 5)
                self.assertEqual(plan["key_environment_names"], ["OLLAMA_API_KEY"])
                self.assertEqual(plan["max_concurrent_requests_total"], 5)
                self.assertEqual(plan["automatic_retries"], 0)
                self.assertEqual(plan["provider_mode"], "live")
                total += plan["max_calls"]
        self.assertEqual(total, 10)

    def test_the_two_occurrences_share_one_credential_and_one_gate(self):
        plans = [h.initialize(REPO, Path(self.temp.name) / ("gate-" + name),
                              STUDY / "material.json", STUDY / name / "arms.json")
                 for name in self.EXPECTED]
        self.assertEqual({tuple(plan["key_environment_names"]) for plan in plans},
                         {("OLLAMA_API_KEY",)})
        self.assertEqual({plan["max_concurrent_requests_per_key_env"]["OLLAMA_API_KEY"]
                          for plan in plans}, {5})

    def test_the_two_occurrences_are_two_identities(self):
        ids = {name: h.initialize(REPO, Path(self.temp.name) / ("id-" + name),
                                  STUDY / "material.json", STUDY / name / "arms.json")["plan_id"]
               for name in self.EXPECTED}
        self.assertEqual(len(set(ids.values())), 2, ids)


if __name__ == "__main__":
    unittest.main()
