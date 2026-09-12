"""Offline, adversarial custody checks; these outputs are not model evidence."""
from copy import deepcopy
from pathlib import Path
import json
import shutil
import subprocess
import tempfile
import unittest

from minireason.inquiry_study import freeze_occurrence, make_plan, run_test, STAGES, _signed
from minireason.provider import digest, write_new
from minireason.template_chain import (construction_contract, freeze_handoff,
    make_chain_plan, render_handoff, verify_chain_plan, verify_handoff)


BASE = Path(__file__).resolve().parents[1]
OUTPUTS = {"construct": "J: λ possibly relates these accounts.\n",
    "criticize": "The relation may conflate ‘can’ with ‘does’.\n",
    "revise": "J′: the original uncertainty remains.\n\n",
    "promote": "No distinct successor is justified by the supplied evidence.\n???\n"}


class RecordedFake:
    def __init__(self, settings, root):
        self.settings, self.root = settings, root
        self.calls = self.prompt_tokens = self.completion_tokens = 0

    def complete(self, messages, *, json_output, coordinate):
        self.calls += 1
        self.prompt_tokens += 7
        self.completion_tokens += 5
        request = {"model": self.settings.model, "messages": messages, "stream": False,
            "max_tokens": self.settings.max_tokens, "thinking": {"type": "disabled"}}
        record = {"schema_version": "minireason.call.v1", "request": request,
            "request_sha256": digest(request), "settings": self.settings.to_dict(),
            "coordinate": coordinate, "started_at": "OFFLINE-FIXTURE"}
        stem = self.root / f"call-{self.calls:04d}"
        write_new(stem.with_suffix(".request.json"), record)
        response = {**record, "status": "COMPLETE", "finish_reason": "stop",
            "returned_model": self.settings.model, "reasoning_content_present": False,
            "reasoning_content_persisted": False, "content": OUTPUTS[coordinate["stage"]],
            "usage": {"prompt_tokens": 7, "completion_tokens": 5}}
        write_new(stem.with_suffix(".response.json"), response)
        return response


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().strip()


def checkpoint(repo):
    source_paths = json.loads((repo / "plan.json").read_text())["source"]["files"]
    for relative in source_paths:
        destination = repo / relative
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(BASE / relative, destination)
    git(repo, "add", "--", "chain.json", "plan.json", "record", *source_paths)
    git(repo, "-c", "user.name=Offline fixture", "-c", "user.email=fixture@example.invalid",
        "commit", "-m", "Offline custody fixture")
    commit, tree = git(repo, "rev-parse", "HEAD"), git(repo, "rev-parse", "HEAD^{tree}")
    return {"local_commit": commit, "remote_commit": commit, "tree_sha": tree,
        "remote_verified": True, "verification_scope": "offline fixture, no remote exists"}


class TemplateChainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name) / "parent"
        cls.root.mkdir()
        packet = json.loads((BASE / "experiments/records/E004-paired-languages/packet.json").read_text())
        issue = freeze_occurrence("What, if anything, survives? λ\n", {"source": "OFFLINE-FIXTURE"}, packet["packet_id"])
        cls.a = make_plan("OFFLINE-A", packet, issue, "prose", "Instrument fixture only.", arms=["mini"])
        cls.chain = make_chain_plan("OFFLINE-CHAIN", cls.a, "OFFLINE-B", "Examine the actual unresolved occurrence.")
        write_new(cls.root / "plan.json", cls.a)
        write_new(cls.root / "chain.json", cls.chain)
        summary = run_test(cls.root / "plan.json", cls.root / "record", provider_factory=RecordedFake)
        if summary["arms"][0]["status"] != "OBSERVATIONS_RECORDED":
            raise AssertionError(summary)
        git(cls.root, "init", "-q")
        cls.publication = checkpoint(cls.root)
        cls.handoff = freeze_handoff(cls.root / "chain.json", cls.root / "record", cls.root, cls.publication)

    def mutated_repository(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name) / "copy"
        shutil.copytree(self.root, root)
        return root

    def test_whole_outputs_and_no_promotion_survive_portably(self):
        verify_handoff(self.handoff)
        rendered = render_handoff(self.handoff)
        self.assertEqual([row["text"] for row in self.handoff["material"]["occurrences"]],
                         [OUTPUTS[stage] for stage in STAGES])
        for text in OUTPUTS.values():
            self.assertEqual(rendered.count(text), 1)
        self.assertFalse(self.handoff["automatic_successor_started"])
        self.assertEqual(self.handoff["standing_effect"], "none")
        self.assertNotIn("git_tree_objects", rendered)

    def test_same_template_with_changed_label_is_rejected(self):
        alias = construction_contract()
        alias["template_id"] = "alias-with-new-name"
        with self.assertRaisesRegex(ValueError, "DISTINCT_TEMPLATES_REQUIRED"):
            make_chain_plan("alias", self.a, "B", "Fixture", b_contract=alias)

    def test_second_cycle_or_repetition_is_rejected(self):
        for field in ("cycles", "repetitions"):
            plan = deepcopy(self.a)
            plan[field] = 2
            plan = _signed({k: v for k, v in plan.items() if k != "plan_id"}, "plan_id")
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "A_TEMPLATE_OR_EXECUTION"):
                make_chain_plan("extra", plan, "B", "Fixture")

    def test_resigned_mapping_cannot_rebind_source(self):
        altered = deepcopy(self.handoff)
        altered["mapping"][0]["source"] = "promote"
        altered = _signed({k: v for k, v in altered.items() if k != "handoff_id"}, "handoff_id")
        with self.assertRaises(ValueError):
            verify_handoff(altered)

    def test_resigned_material_cannot_replace_output(self):
        altered = deepcopy(self.handoff)
        altered["material"]["occurrences"][0]["text"] += "changed"
        altered = _signed({k: v for k, v in altered.items() if k != "handoff_id"}, "handoff_id")
        with self.assertRaisesRegex(ValueError, "HANDOFF_PARENT_OR_MAPPING_CHANGED"):
            verify_handoff(altered)

    def test_empty_tree_path_cannot_bypass_published_chain_proof(self):
        altered = deepcopy(self.handoff)
        altered["chain_file"]["path"] = "."
        altered = _signed({k: v for k, v in altered.items() if k != "handoff_id"}, "handoff_id")
        with self.assertRaisesRegex(ValueError, "UNSAFE_EVIDENCE_PATH"):
            verify_handoff(altered)

    def test_resigned_evidence_cannot_escape_published_git_tree(self):
        altered = deepcopy(self.handoff)
        path = "mini-r01/construct.artifact.json"
        altered["evidence"]["files"][path] += " "
        import hashlib
        altered["evidence"]["sha256"][path] = hashlib.sha256(altered["evidence"]["files"][path].encode()).hexdigest()
        altered = _signed({k: v for k, v in altered.items() if k != "handoff_id"}, "handoff_id")
        with self.assertRaisesRegex(ValueError, "PUBLISHED_FILE_PROOF_CHANGED"):
            verify_handoff(altered)

    def test_published_host_source_disagrees_with_declared_source_is_rejected(self):
        root = self.mutated_repository()
        relative = next(iter(self.a["source"]["files"]))
        path = root / relative
        path.write_bytes(path.read_bytes() + b"\n")
        publication = checkpoint(root)
        with self.assertRaisesRegex(ValueError, "PARENT_DECLARED_SOURCE_CHANGED"):
            freeze_handoff(root / "chain.json", root / "record", root, publication)

    def test_source_archive_is_complete_and_outside_model_visible_render(self):
        evidence = self.handoff["source_evidence"]
        self.assertEqual(evidence["sha256"], self.a["source"]["files"])
        self.assertEqual(set(evidence["files"]), set(self.a["source"]["files"]))
        self.assertNotIn("source_evidence", render_handoff(self.handoff))
        altered = deepcopy(self.handoff)
        altered["source_evidence"]["files"].pop(next(iter(evidence["files"])))
        altered = _signed({k: v for k, v in altered.items() if k != "handoff_id"}, "handoff_id")
        with self.assertRaisesRegex(ValueError, "PARENT_DECLARED_SOURCE_CHANGED"):
            verify_handoff(altered)

    def test_published_contradictory_preflight_is_rejected(self):
        root = self.mutated_repository()
        path = root / "record/preflight.json"
        preflight = json.loads(path.read_text())
        preflight["status"] = "CONFIGURATION_PREFLIGHT_FAILED"
        path.write_text(json.dumps(preflight))
        publication = checkpoint(root)
        with self.assertRaisesRegex(ValueError, "PARENT_PREFLIGHT_CHANGED"):
            freeze_handoff(root / "chain.json", root / "record", root, publication)

    def test_unpublished_parent_bytes_fail_freeze(self):
        root = self.mutated_repository()
        with (root / "record/mini-r01/promote.artifact.json").open("a") as handle:
            handle.write(" ")
        with self.assertRaisesRegex(ValueError, "UNPUBLISHED_PARENT_BYTES"):
            freeze_handoff(root / "chain.json", root / "record", root, self.publication)

    def test_published_wrong_completion_is_still_rejected(self):
        root = self.mutated_repository()
        path = root / "record/mini-r01/result.json"
        result = json.loads(path.read_text())
        result["status"] = "OPERATIONAL_FAILURE"
        path.write_text(json.dumps(result))
        publication = checkpoint(root)
        with self.assertRaisesRegex(ValueError, "PARENT_COMPLETION_OR_COORDINATE_CHANGED"):
            freeze_handoff(root / "chain.json", root / "record", root, publication)

    def test_published_changed_occurrence_and_missing_stage_are_rejected(self):
        for mutation in ("origin", "stage"):
            root = self.mutated_repository()
            path = root / "record/mini-r01/result.json"
            result = json.loads(path.read_text())
            if mutation == "origin":
                result["history"][0]["origin"]["repeat"] = 2
                row = result["history"][0]
                result["history"][0] = _signed({k: v for k, v in row.items() if k != "occurrence_id"}, "occurrence_id")
            else:
                result["history"].pop()
            path.write_text(json.dumps(result))
            publication = checkpoint(root)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                freeze_handoff(root / "chain.json", root / "record", root, publication)

    def test_published_changed_mini_blob_is_rejected(self):
        root = self.mutated_repository()
        files = list((root / "record/mini-r01/run/blobs").iterdir())
        target = next(path for path in files if path.read_text() == OUTPUTS["construct"])
        target.write_bytes(b"altered public output")
        publication = checkpoint(root)
        with self.assertRaises(Exception):
            freeze_handoff(root / "chain.json", root / "record", root, publication)

    def test_published_changed_wire_request_is_rejected(self):
        root = self.mutated_repository()
        path = root / "record/mini-r01/calls/call-0002.request.json"
        request = json.loads(path.read_text())
        request["coordinate"]["stage"] = "promote"
        path.write_text(json.dumps(request))
        publication = checkpoint(root)
        with self.assertRaisesRegex(ValueError, "PARENT_PUBLIC_RESPONSE_OR_REQUEST_CHANGED"):
            freeze_handoff(root / "chain.json", root / "record", root, publication)

    def test_missing_predeclared_selected_arm_cannot_be_substituted(self):
        chain = deepcopy(self.chain)
        chain["a_selection"] = {"arm": "mini_native", "repeat": 1}
        chain = _signed({k: v for k, v in chain.items() if k != "chain_plan_id"}, "chain_plan_id")
        with self.assertRaisesRegex(ValueError, "CHAIN_SELECTION_OR_MAPPING_CHANGED"):
            verify_chain_plan(chain)


if __name__ == "__main__":
    unittest.main()
