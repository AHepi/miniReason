"""R3-A3 EC01 fixed-parent fork regressions; offline fixtures only."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest

from minireason.reason import prompts, r002, r003_ec01
from tests.reason.test_r003_occurrence import OpenFixture


ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "experiments/diagnostics/R003-open-problems-trial-series"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree(path: Path) -> dict[str, str]:
    return {item.relative_to(path).as_posix(): digest(item)
            for item in path.rglob("*") if item.is_file()}


class EC01Fixture(OpenFixture):
    """Make the two cycle-1 routes visibly different without supplying an oracle."""

    def __init__(self, *, fail_branch: str | None = None,
                 interrupt_call: str | None = None):
        super().__init__(repair=False)
        self.fail_branch = fail_branch
        self.interrupt_call = interrupt_call
        self.coordinates: list[str] = []

    @staticmethod
    def _answer(text: str) -> dict:
        return {
            "decision": "answered",
            "answer": text,
            "missing_derivation": "",
            "claims": [{"relation_id": "working_position", "value": text, "quote": text}],
            "derivation_steps": [{"step_index": 1, "statement": text, "depends_on": []}],
        }

    def __call__(self, *, role, cycle, objections, coordinate, context):
        call_id = coordinate["call_id"]
        self.coordinates.append(call_id)
        if call_id == self.interrupt_call:
            raise KeyboardInterrupt("offline fixture interruption before response custody")
        if role == "prose_return":
            branch = "RETURNED" if call_id == "c0001-R-return" else (
                "ARCHIVED" if call_id == "c0001-A-return" else f"MAIN-CYCLE-{cycle}")
            if branch == self.fail_branch:
                return {"content": "OFFLINE FIXTURE: deliberately invalid branch response."}
            value = super().__call__(role=role, cycle=cycle, objections=objections,
                                     coordinate=coordinate, context=context)
            text = (
                "OFFLINE FIXTURE RETURNED: revise the decision because the delivered rival applies."
                if branch == "RETURNED" else
                "OFFLINE FIXTURE ARCHIVED: retain the decision because no objection was delivered."
                if branch == "ARCHIVED" else
                f"OFFLINE FIXTURE {branch}: keep the returned branch under further criticism."
            )
            value.update(self._answer(text))
            return value
        if role == "propagation_use":
            before_text = context["before"]["answer"]
            after_text = context["answer"]["answer"]
            shared_task = context.get("expected_use_task")
            conclusion = (
                "revise" if call_id == "c0001-R-use" else
                "retain" if call_id == "c0001-A-use" else
                f"continue-{cycle}"
            )
            return {
                "decision": "answered",
                "missing_derivation": "",
                "query_id": (shared_task or {"query_id": "use-" + call_id})["query_id"],
                "question": (shared_task or {
                    "question": "Should the proposal govern the later decision?"})["question"],
                "problem_derivation": "Compare the proposal with the named rival account.",
                "before": {"answer_quote": before_text,
                           "derivation": "The earlier proposal leaves the rival unresolved.",
                           "conclusion": "undecided"},
                "after": {"answer_quote": after_text,
                          "derivation": "Apply this branch's returned commitment only.",
                          "conclusion": conclusion},
                "dependency": {"relation_id": "working_position",
                               "before_quote": before_text,
                               "after_quote": after_text,
                               "result_depends_on_change": before_text != after_text,
                               "explanation": "The branch-local returned commitment controls this result."},
                "objections": [],
                "checker": None,
            }
        return super().__call__(role=role, cycle=cycle, objections=objections,
                                coordinate=coordinate, context=context)


class EmptyObjectionFixture(OpenFixture):
    """Both critics answer, but neither supplies an objection to route."""

    def __call__(self, *, role, cycle, objections, coordinate, context):
        if role == "prose_critic":
            return {"decision": "answered", "missing_derivation": "",
                    "working": "No objection survives in this offline fixture.",
                    "objections": []}
        value = super().__call__(role=role, cycle=cycle, objections=objections,
                                 coordinate=coordinate, context=context)
        if role == "propagation_use" and context.get("expected_use_task"):
            value = dict(value)
            value.update(context["expected_use_task"])
        return value


class ArchivedRepairFixture(EC01Fixture):
    """Force one archived schema repair, then supply the valid branch response."""

    invalid_archived = "OFFLINE FIXTURE: archive branch needs shape repair only."

    def __call__(self, *, role, cycle, objections, coordinate, context):
        if (role == "prose_return" and coordinate["call_id"] == "c0001-A-return"
                and coordinate["attempt"] == 0):
            self.coordinates.append(coordinate["call_id"])
            return {"content": self.invalid_archived}
        return super().__call__(role=role, cycle=cycle, objections=objections,
                                coordinate=coordinate, context=context)


class ChangedUseTaskFixture(EC01Fixture):
    """Change one branch's frozen task once or on every eligible repair."""

    def __init__(self, *, always_bad: bool):
        super().__init__()
        self.always_bad = always_bad

    def __call__(self, *, role, cycle, objections, coordinate, context):
        value = super().__call__(role=role, cycle=cycle, objections=objections,
                                 coordinate=coordinate, context=context)
        if (role == "propagation_use" and coordinate["call_id"] == "c0001-A-use"
                and (self.always_bad or coordinate["attempt"] == 0)):
            value = dict(value)
            value["query_id"] = "branch-selected-task"
            value["question"] = "A different archived-branch question."
        return value


class CriticRepairFixture(EC01Fixture):
    """Force a critic repair so every attempt's provider custody is archived."""

    def __call__(self, *, role, cycle, objections, coordinate, context):
        if (coordinate["call_id"] == "c0001-signal-a" and coordinate["attempt"] == 0):
            self.coordinates.append(coordinate["call_id"])
            return {"content": "OFFLINE FIXTURE: invalid critic requiring shape repair."}
        return super().__call__(role=role, cycle=cycle, objections=objections,
                                coordinate=coordinate, context=context)


class R003R3A3ForkTests(unittest.TestCase):
    def setUp(self):
        fixture_root = Path(os.environ.get("TMP", "C:/tw36"))
        fixture_root.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=fixture_root)
        self.base = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def new_run(self, name: str = "run") -> Path:
        problem = (STUDY / "problems/O01.txt").read_text(encoding="utf-8")
        copied = self.base / name / "p/O01.txt"
        copied.parent.mkdir(parents=True)
        copied.write_text(problem, encoding="utf-8", newline="")
        canonical = self.base / name / "canonical.json"
        canonical.write_text(json.dumps({
            "schema_version": "minireason.reason.r003-canonical-registry.v1",
            "study_profile": "r003-open-v1",
            "candidates": [{
                "candidate_id": "O01",
                "canonical_problem": "p/O01.txt",
                "problem_sha256": digest(copied),
            }],
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="")
        return r002.create_r002_run(
            problem, STUDY / "recipes/r003-cross-v4.json", self.base / name / "cell",
            mode="offline", problem_id="O01", study_profile="r003-open-v1",
            relation_registry=STUDY / "public/RELATIONS.json",
            fork_registry=STUDY / "public/FORKS.json", canonical_registry=canonical)

    @staticmethod
    def user_bytes(run: Path, call_id: str) -> bytes:
        request = load(run / "calls" / call_id / "a00/request.json")
        return request["prepared"]["messages"][1]["content"].encode("utf-8")

    def test_fixed_parent_exact_deletion_archive_branch_records_and_reports(self):
        run = self.new_run()
        fixture = EC01Fixture()
        state = r002.execute_r002(run, scripted=fixture)
        self.assertEqual((state["stop_reason"], state["completed_cycles"]),
                         ("cycle_budget", 3), state)
        self.assertEqual((state["calls"], state["attempts"]), (16, 16), state)

        counts = Counter(fixture.coordinates)
        self.assertEqual(counts["initial"], 1)
        self.assertEqual(counts["c0001-signal-a"], 1)
        self.assertEqual(counts["c0001-signal-b"], 1)
        self.assertEqual(
            fixture.coordinates[:7],
            ["initial", "c0001-signal-a", "c0001-signal-b",
             "c0001-R-return", "c0001-R-use", "c0001-A-return", "c0001-A-use"])
        self.assertFalse((run / "calls/c0002-A-return").exists())
        self.assertTrue((run / "calls/c0002-return/a00/response.json").is_file())
        self.assertTrue((run / "calls/closing-return/a00/response.json").is_file())

        parent = load(run / "ec01/parent.json")
        returned = load(run / "ec01/RETURNED.json")
        archived = load(run / "ec01/ARCHIVED.json")
        self.assertEqual(returned["branch_id"], "RETURNED")
        self.assertEqual(archived["branch_id"], "ARCHIVED")
        self.assertEqual(returned["parent_state_sha256"], archived["parent_state_sha256"])
        self.assertEqual(returned["parent_state_sha256"], digest(run / "ec01/parent.json"))
        self.assertEqual(returned["identical_inputs_sha256"], archived["identical_inputs_sha256"])
        self.assertEqual(returned["identical_inputs_sha256"], parent["identical_inputs_sha256"])
        self.assertEqual(returned["shared_use_task"], archived["shared_use_task"])
        self.assertEqual(returned["shared_use_task"], parent["shared_use_task"])
        self.assertEqual(returned["shared_use_task_sha256"], parent["shared_use_task_sha256"])
        self.assertTrue(returned["delivered_objection_ids"])
        self.assertEqual(returned["archived_objection_ids"], [])
        self.assertEqual(archived["delivered_objection_ids"], [])
        self.assertEqual(archived["archived_objection_ids"], returned["delivered_objection_ids"])
        self.assertEqual(returned["return"]["status"], "COMPLETE")
        self.assertEqual(returned["use"]["status"], "COMPLETE")
        self.assertEqual(archived["return"]["status"], "COMPLETE")
        self.assertEqual(archived["use"]["status"], "COMPLETE")

        difference = load(run / "ec01/prompt-difference.json")
        returned_bytes = self.user_bytes(run, "c0001-R-return")
        archived_bytes = self.user_bytes(run, "c0001-A-return")
        start, end = difference["utf8_start"], difference["utf8_end"]
        removed = difference["removed_block"].encode("utf-8")
        self.assertEqual(returned_bytes[start:end], removed)
        self.assertEqual(returned_bytes[:start] + returned_bytes[end:], archived_bytes)
        self.assertEqual(hashlib.sha256(removed).hexdigest(), difference["removed_sha256"])
        self.assertEqual(
            difference["removed_labels"], ["OPEN AND NEW OBJECTIONS", "PUBLIC SIGNALS"])
        self.assertIn(b"BEGIN OPEN AND NEW OBJECTIONS", removed)
        self.assertIn(b"BEGIN PUBLIC SIGNALS", removed)
        wire = difference["wire"]
        returned_wire = load(run / "calls/c0001-R-return/a00/request.json")[
            "prepared"]["wire_body_text"].encode("utf-8")
        archived_wire = load(run / "calls/c0001-A-return/a00/request.json")[
            "prepared"]["wire_body_text"].encode("utf-8")
        wire_start = wire["utf8_start"]
        wire_removed = wire["removed_block"].encode("utf-8")
        wire_end = wire_start + len(wire_removed)
        self.assertEqual(returned_wire[wire_start:wire_end], wire_removed)
        self.assertEqual(returned_wire[:wire_start] + returned_wire[wire_end:], archived_wire)
        self.assertEqual(hashlib.sha256(wire_removed).hexdigest(), wire["removed_sha256"])
        self.assertEqual(hashlib.sha256(returned_wire).hexdigest(), wire["returned_sha256"])
        self.assertEqual(hashlib.sha256(archived_wire).hexdigest(), wire["archived_sha256"])
        objection_archive = (run / "archive/c0001-objections.json").read_bytes()
        for objection in load(run / "archive/c0001-objections.json"):
            encoded = objection["text"].encode("utf-8")
            self.assertIn(encoded, returned_bytes)
            self.assertNotIn(encoded, archived_bytes)
        self.assertEqual(parent["objection_archive"]["sha256"],
                         hashlib.sha256(objection_archive).hexdigest())
        for critic in ("c0001-signal-a", "c0001-signal-b"):
            source_root = run / "calls" / critic
            archive_root = run / "archive" / critic
            source_files = {path.relative_to(source_root).as_posix(): path
                            for path in source_root.rglob("*") if path.is_file()}
            archive_files = {path.relative_to(archive_root).as_posix(): path
                             for path in archive_root.rglob("*") if path.is_file()}
            self.assertEqual(set(source_files), set(archive_files))
            for name, source in source_files.items():
                self.assertEqual(source.read_bytes(), archive_files[name].read_bytes(), name)

        returned_request = load(run / "calls/c0001-R-return/a00/request.json")
        archived_request = load(run / "calls/c0001-A-return/a00/request.json")
        for key in ("seat", "cycle", "schema_repair"):
            self.assertEqual(returned_request[key], archived_request[key])
        for key in ("endpoint", "thinking", "reasoning_effort", "kwargs", "wall_seconds"):
            if key == "kwargs":
                left = {k: v for k, v in returned_request["prepared"][key].items()
                        if k != "coordinate"}
                right = {k: v for k, v in archived_request["prepared"][key].items()
                         if k != "coordinate"}
                self.assertEqual(left, right)
            else:
                self.assertEqual(returned_request["prepared"][key],
                                 archived_request["prepared"][key])

        cfg, recipe, problem, relation, fork, _coding, _endpoints = r002._validate_run(run)
        contracts = r002.ContractSet(run / "contracts")
        expected_blocks = r002._return_blocks(
            problem, parent["before_answer"], parent["objections"], relation, fork,
            parent["critic_outputs"])
        expected_messages = prompts.render_r002(
            "prose_return",
            [*expected_blocks, *contracts.prompt_blocks("prose_return", prompts.R003_A2_CONTRACT)],
            study_profile="r003-open-v1", contract_version=prompts.R003_A2_CONTRACT)
        self.assertEqual(returned_request["prepared"]["messages"], expected_messages)

        returned_use_request = load(run / "calls/c0001-R-use/a00/request.json")
        archived_use_request = load(run / "calls/c0001-A-use/a00/request.json")
        shared_task_json = json.dumps(parent["shared_use_task"], ensure_ascii=False,
                                      sort_keys=True, separators=(",", ":"))
        for use_request in (returned_use_request, archived_use_request):
            system = use_request["prepared"]["messages"][0]["content"]
            user = use_request["prepared"]["messages"][1]["content"]
            self.assertIn("already been selected in SHARED EC01 USE TASK", system)
            self.assertIn(shared_task_json, user)
        self.assertEqual(
            r003_ec01.envelope(returned_use_request["prepared"], cfg, recipe),
            r003_ec01.envelope(archived_use_request["prepared"], cfg, recipe))
        self.assertEqual(returned_use_request["seat"], archived_use_request["seat"])
        self.assertEqual(returned_use_request["preflight"]["limit"],
                         archived_use_request["preflight"]["limit"])

        returned_use = self.user_bytes(run, "c0001-R-use")
        archived_use = self.user_bytes(run, "c0001-A-use")
        returned_answer = returned["return"]["parsed"]["answer"].encode("utf-8")
        archived_answer = archived["return"]["parsed"]["answer"].encode("utf-8")
        self.assertIn(returned_answer, returned_use)
        self.assertNotIn(archived_answer, returned_use)
        self.assertIn(archived_answer, archived_use)
        self.assertNotIn(returned_answer, archived_use)

        comparison = load(run / "ec01/comparison.json")
        rendered = json.dumps(comparison, ensure_ascii=False)
        self.assertIn("Mechanical", rendered)
        self.assertIn("semantic", rendered)
        self.assertTrue(comparison["mechanical_decisive_commitment_diff"])
        for report_name in ("TRACE.md", "RUN.md", "EPISODES.md"):
            report = (run / report_name).read_text(encoding="utf-8")
            self.assertIn("RETURNED", report, report_name)
            self.assertIn("ARCHIVED", report, report_name)
            self.assertIn(parent["shared_use_task_sha256"], report, report_name)
            self.assertIn("Use after conclusion", report, report_name)

    def test_changed_shared_use_task_repairs_or_is_refused(self):
        repaired_run = self.new_run("changed-task-repaired")
        repaired = r002.execute_r002(
            repaired_run, scripted=ChangedUseTaskFixture(always_bad=False))
        self.assertEqual(repaired["stop_reason"], "cycle_budget", repaired)
        archived = load(repaired_run / "ec01/ARCHIVED.json")
        self.assertEqual([item["status"] for item in archived["use"]["attempts"]],
                         ["SCHEMA_FAILURE", "COMPLETE"])
        self.assertEqual(archived["use"]["parsed"]["query_id"], "ec01-shared-use")

        refused_run = self.new_run("changed-task-refused")
        refused = r002.execute_r002(
            refused_run, scripted=ChangedUseTaskFixture(always_bad=True))
        self.assertEqual(refused["stop_reason"], "cycle_budget", refused)
        archived = load(refused_run / "ec01/ARCHIVED.json")
        self.assertEqual(archived["status"], "SCHEMA_FAILURE")
        self.assertEqual([item["status"] for item in archived["use"]["attempts"]],
                         ["SCHEMA_FAILURE", "SCHEMA_FAILURE"])

    def test_repaired_critic_archive_copies_every_provider_file(self):
        run = self.new_run("critic-repair-custody")
        state = r002.execute_r002(run, scripted=CriticRepairFixture())
        self.assertEqual(state["stop_reason"], "cycle_budget", state)
        source_root = run / "calls/c0001-signal-a"
        archive_root = run / "archive/c0001-signal-a"
        source = {path.relative_to(source_root).as_posix(): path.read_bytes()
                  for path in source_root.rglob("*") if path.is_file()}
        archived = {path.relative_to(archive_root).as_posix(): path.read_bytes()
                    for path in archive_root.rglob("*") if path.is_file()}
        self.assertEqual(source, archived)
        self.assertTrue(any(name.startswith("a01/provider/") for name in archived))

    def test_branch_failure_is_local_and_returned_failure_stops_continuation(self):
        archived_run = self.new_run("archived-failure")
        archived_state = r002.execute_r002(
            archived_run, scripted=EC01Fixture(fail_branch="ARCHIVED"))
        self.assertEqual(archived_state["completed_cycles"], 3, archived_state)
        self.assertTrue((archived_run / "calls/c0002-signal-a/a00/request.json").is_file())
        archived = load(archived_run / "ec01/ARCHIVED.json")
        self.assertEqual(archived["return"]["status"], "SCHEMA_FAILURE")
        self.assertEqual(archived["use"]["status"], "not-run")

        returned_run = self.new_run("returned-failure")
        returned_state = r002.execute_r002(
            returned_run, scripted=EC01Fixture(fail_branch="RETURNED"))
        self.assertEqual(returned_state["stop_reason"], "SCHEMA_FAILURE", returned_state)
        self.assertEqual(returned_state["completed_cycles"], 0, returned_state)
        self.assertTrue((returned_run / "calls/c0001-A-return/a00/request.json").is_file())
        self.assertFalse((returned_run / "calls/c0002-signal-a").exists())
        self.assertEqual(load(returned_run / "ec01/RETURNED.json")["return"]["status"],
                         "SCHEMA_FAILURE")

    def test_zero_objections_is_a_recorded_no_op(self):
        run = self.new_run("zero-objections")
        state = r002.execute_r002(run, scripted=EmptyObjectionFixture(repair=False))
        self.assertEqual((state["stop_reason"], state["completed_cycles"]),
                         ("no_new_objections", 1), state)
        returned = load(run / "ec01/RETURNED.json")
        archived = load(run / "ec01/ARCHIVED.json")
        self.assertEqual(returned["delivered_objection_ids"], [])
        self.assertEqual(archived["archived_objection_ids"], [])
        self.assertEqual(returned["return"]["parsed"], archived["return"]["parsed"])
        self.assertEqual(returned["use"]["parsed"], archived["use"]["parsed"])
        comparison = load(run / "ec01/comparison.json")
        self.assertTrue(comparison["fields_equal"])
        self.assertEqual(comparison["mechanical_decisive_commitment_diff"], "")

    def test_archived_schema_repair_has_only_archived_context_and_terminal_replay_is_stable(self):
        run = self.new_run("archived-repair")
        fixture = ArchivedRepairFixture()
        state = r002.execute_r002(run, scripted=fixture)
        self.assertEqual((state["stop_reason"], state["completed_cycles"]),
                         ("cycle_budget", 3), state)
        archived = load(run / "ec01/ARCHIVED.json")
        self.assertEqual(archived["return"]["status"], "COMPLETE")
        self.assertEqual([attempt["status"] for attempt in archived["return"]["attempts"]],
                         ["SCHEMA_FAILURE", "COMPLETE"])

        parent = load(run / "ec01/parent.json")
        returned_answer = load(run / "ec01/RETURNED.json")["return"]["parsed"]["answer"]
        repair = load(run / "calls/c0001-A-return/a01/request.json")
        repair_user = repair["prepared"]["messages"][1]["content"]
        self.assertIn(ArchivedRepairFixture.invalid_archived, repair_user)
        self.assertNotIn("BEGIN OPEN AND NEW OBJECTIONS", repair_user)
        self.assertNotIn("BEGIN PUBLIC SIGNALS", repair_user)
        self.assertNotIn(returned_answer, repair_user)
        for objection in parent["objections"]:
            self.assertNotIn(objection["text"], repair_user)
        archived_original = load(run / "calls/c0001-A-return/a00/request.json")[
            "prepared"]["messages"][1]["content"]
        self.assertIn(archived_original, repair_user)

        before = tree(run)
        replayed = r002.execute_r002(
            run, scripted=lambda **_context: self.fail("terminal call was replayed"))
        self.assertEqual(replayed, state)
        self.assertEqual(tree(run), before)

    def test_safe_interruption_resumes_without_repeating_consumed_calls(self):
        run = self.new_run("resume")
        fixture = EC01Fixture()

        def interrupt_after_return(call_id, _saved):
            if call_id == "c0001-R-return":
                raise KeyboardInterrupt("offline interruption after durable response")

        with self.assertRaises(KeyboardInterrupt):
            r002.execute_r002(run, scripted=fixture, after_call=interrupt_after_return)
        frozen_hash = digest(run / "ec01/parent.json")
        consumed = list(fixture.coordinates)
        state = r002.execute_r002(run, scripted=fixture)
        self.assertEqual(state["stop_reason"], "cycle_budget", state)
        self.assertEqual(digest(run / "ec01/parent.json"), frozen_hash)
        for call_id in consumed:
            self.assertEqual(fixture.coordinates.count(call_id), consumed.count(call_id), call_id)

    def test_unknown_request_intent_is_not_replayed(self):
        run = self.new_run("unknown-intent")
        fixture = EC01Fixture(interrupt_call="c0001-R-return")
        with self.assertRaises(KeyboardInterrupt):
            r002.execute_r002(run, scripted=fixture)
        self.assertTrue((run / "calls/c0001-R-return/a00/request.json").is_file())
        self.assertFalse((run / "calls/c0001-R-return/a00/response.json").exists())
        before = fixture.coordinates.count("c0001-R-return")
        state = r002.execute_r002(run, scripted=fixture)
        self.assertEqual(state["stop_reason"], "INTERRUPTED_CALL", state)
        self.assertEqual(fixture.coordinates.count("c0001-R-return"), before)
        self.assertFalse((run / "calls/c0001-R-return/a01").exists())
        self.assertTrue((run / "calls/c0001-A-return/a00/response.json").is_file())


if __name__ == "__main__":
    unittest.main()
