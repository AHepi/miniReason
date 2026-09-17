"""Regression tests derived from the 2026-09-17 live pilot response bytes."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from minireason import provider_openai_compat as provider
from minireason.pilot.inputs import TaskInputs
from minireason.pilot.manifest import get_host_schema
from minireason.pilot.pilot import Pilot
from minireason.pilot.router import select_template
from minireason.pilot.templates import normalize_inputs, validate_inputs
from minireason.reason.types import ReasonFailure


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).parent / "fixtures" / "live-20260917"
USECASES = ROOT / "research" / "deepseek-flash-pilot" / "usecases"
TASK_PATHS = {
    "UC1": USECASES / "UC1-blender-blocking" / "task.json",
    "UC2": USECASES / "UC2-hard-to-vary-story" / "task.json",
    "UC3": USECASES / "UC3-reading-between-lines" / "task.json",
    "UC4": USECASES / "UC4-fw5-adversarial-mapping" / "task.json",
}


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def read_json(path: Path) -> dict:
    return json.loads(read_text(path))


def live_body(name: str) -> str:
    return read_text(FIXTURES / f"{name}.response-body.json")


class LiveDeliveryRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=os.environ["TMP"], prefix="live-delivery-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        patcher = mock.patch.object(provider, "_open", side_effect=AssertionError("network forbidden"))
        patcher.start()
        self.addCleanup(patcher.stop)

    def pilot(self, usecase: str, name: str, scripted) -> Pilot:
        return Pilot(
            read_json(TASK_PATHS[usecase]),
            self.root / name,
            scripted=scripted,
            repo_root=ROOT,
        )

    @staticmethod
    def canonical_spawn(pilot: Pilot) -> dict:
        return {
            "subtasks": [{
                "template_id": pilot.route["template_id"],
                "inputs": copy.deepcopy(pilot.input_ref),
            }]
        }

    @staticmethod
    def spawn_packet(pilot: Pilot) -> dict:
        return {
            "template_id": pilot.route["template_id"],
            "inputs": copy.deepcopy(pilot.input_ref),
            "input_catalog": pilot.task_inputs.catalog(),
            "pass_number": pilot.pass_number,
            "instruction": "Copy the supplied input reference exactly.",
        }

    @staticmethod
    def set_live_route(pilot: Pilot, usecase: str) -> None:
        pilot.handle_tool("route", json.loads(live_body(f"{usecase}-c0001-a00")))

    def replay_bad_spawn_then_exact_repair(self, usecase: str, attempt: str) -> tuple[Pilot, list[dict]]:
        rejected = live_body(f"{usecase}-c0002-{attempt}")
        seen: list[dict] = []
        holder: dict[str, Pilot] = {}

        def scripted(**context):
            seen.append(context)
            if context["attempt"] == 0:
                return {"content": rejected}
            return {"content": json.dumps(self.canonical_spawn(holder["pilot"]), ensure_ascii=False)}

        pilot = self.pilot(usecase, f"{usecase.lower()}-{attempt}-repair", scripted)
        holder["pilot"] = pilot
        self.set_live_route(pilot, usecase)
        accepted = pilot.ask(
            "spawn",
            self.spawn_packet(pilot),
            get_host_schema("spawn"),
            max_tokens=2048,
            validator=pilot._validate_spawn,
        )
        self.assertEqual(accepted, self.canonical_spawn(pilot))
        expanded = pilot._validate_spawn(accepted)
        self.assertEqual(expanded[0]["inputs"], pilot.inputs)
        self.assertEqual([item["status"] for item in pilot.calls.receipts], ["contract_rejected", "accepted"])
        repair_messages = seen[1]["messages"]
        self.assertEqual(repair_messages[:2], seen[0]["messages"])
        self.assertEqual(repair_messages[-2], {"role": "assistant", "content": rejected})
        return pilot, seen

    def test_uc1_and_uc3_live_spawn_attempts_get_exact_context_repairs(self) -> None:
        for usecase in ("UC1", "UC3"):
            for attempt in ("a00", "a01"):
                with self.subTest(usecase=usecase, attempt=attempt):
                    _pilot, seen = self.replay_bad_spawn_then_exact_repair(usecase, attempt)
                    repair = seen[1]["messages"][-1]["content"]
                    self.assertIn("OUTER_INPUTS_MUST_MATCH_SEALED_TASK", repair)
                    self.assertIn("copy the packet inputs reference exactly", repair)
                    self.assertIn("do not reconstruct documents", repair)

    def test_uc1_and_uc3_original_repair_pairs_remain_refused(self) -> None:
        for usecase in ("UC1", "UC3"):
            with self.subTest(usecase=usecase):
                bodies = [live_body(f"{usecase}-c0002-a00"), live_body(f"{usecase}-c0002-a01")]
                seen: list[dict] = []

                def scripted(**context):
                    seen.append(context)
                    return {"content": bodies[min(context["attempt"], 1)]}

                pilot = self.pilot(usecase, f"{usecase.lower()}-original-pair", scripted)
                self.set_live_route(pilot, usecase)
                with self.assertRaises(ReasonFailure) as caught:
                    pilot.ask(
                        "spawn",
                        self.spawn_packet(pilot),
                        get_host_schema("spawn"),
                        max_tokens=2048,
                        validator=pilot._validate_spawn,
                    )
                self.assertEqual(caught.exception.code, "SCHEMA_REJECTED")
                self.assertEqual([item["status"] for item in pilot.calls.receipts],
                                 ["contract_rejected"] * 4)
                self.assertEqual(seen[1]["messages"][-2]["content"], bodies[0])
                second = read_json(pilot.root / "calls" / "c0001" / "a01" / "outcome.json")
                self.assertIn("OUTER_INPUTS_MUST_MATCH_SEALED_TASK", second["validation_error"])

    def test_uc1_and_uc3_original_live_sequences_stop_pass_after_three_repairs(self) -> None:
        for usecase in ("UC1", "UC3"):
            with self.subTest(usecase=usecase):
                def scripted(**context):
                    if context["role"] == "route":
                        return {"content": live_body(f"{usecase}-c0001-a00")}
                    if context["role"] == "spawn":
                        attempt = "a00" if context["attempt"] == 0 else "a01"
                        return {"content": live_body(f"{usecase}-c0002-{attempt}")}
                    packet = json.loads(context["messages"][-1]["content"])
                    return {"decision": "stop", "reason": packet["verification"]["verification_ref"] + " retains the exact custody refusal.",
                            "stop_rule": "Stop on preserved custody failure.", "what_changes_next": ""}
                pilot = self.pilot(usecase, f"{usecase.lower()}-pilot-run", scripted)
                result = pilot.run()
                self.assertEqual(result["status"], "partial")
                self.assertEqual(result["verification"]["failure_code"], "SCHEMA_REJECTED")
                self.assertEqual((result["logical_calls"], result["calls"]), (3, 6))
                outcomes = [read_json(pilot.root / "calls" / "c0002" / attempt / "outcome.json")
                            for attempt in ("a00", "a01", "a02", "a03")]
                self.assertTrue(all("OUTER_INPUTS_MUST_MATCH_SEALED_TASK" in item["validation_error"] for item in outcomes))

    def test_uc2_live_spawn_gets_precise_repair_then_exact_ref_passes(self) -> None:
        pilot, seen = self.replay_bad_spawn_then_exact_repair("UC2", "a00")
        repair = seen[1]["messages"][-1]["content"]
        self.assertIn("evidence_read requires nonempty inputs", repair)
        self.assertIn(
            "4cdab193ae0f51732f4055ef08cef75d04470058d26d04c5b0041b3d0ff25b3e",
            seen[1]["messages"][-2]["content"],
        )
        self.assertNotIn(
            "4cdab193ae0f51732f4055ef08cef75d04470058d26d04c5b0041b3d0ff25b3e",
            {unit["unit_id"] for unit in pilot.task["input_units"]},
        )

    def uc4_sources(self, pilot: Pilot) -> dict[str, str]:
        return pilot._quote_sources(pilot.inputs, [])

    def corrected_uc4_output(self, pilot: Pilot) -> dict:
        output = json.loads(live_body("UC4-c0003-a00"))
        sources = self.uc4_sources(pilot)
        source_id = "FW5-excerpts"
        exact = sources[source_id].encode("utf-8")[:64].decode("utf-8", errors="ignore")
        exact_bytes = exact.encode("utf-8")
        output["source_refs"] = [source_id]
        output["quotes"] = [{
            "claim": "Exact opening bytes from the supplied FW5 excerpt.",
            "source_id": source_id,
            "locator": f"bytes:0:{len(exact_bytes)}",
            "quote": exact,
        }]
        return output

    def test_uc4_live_quote_repair_carries_both_custody_failures_and_accepts_exact_bytes(self) -> None:
        rejected = live_body("UC4-c0003-a00")
        seen: list[dict] = []
        holder: dict[str, Pilot] = {}

        def scripted(**context):
            seen.append(context)
            if context["attempt"] == 0:
                return {"content": rejected}
            return {"content": json.dumps(self.corrected_uc4_output(holder["pilot"]), ensure_ascii=False)}

        pilot = self.pilot("UC4", "uc4-exact-repair", scripted)
        holder["pilot"] = pilot
        output = pilot.execute_template("evidence_read", pilot.inputs, 1)
        self.assertEqual(output["source_refs"], ["FW5-excerpts"])
        self.assertEqual([item["status"] for item in pilot.calls.receipts], ["contract_rejected", "accepted"])
        repair_messages = seen[1]["messages"]
        self.assertEqual(repair_messages[:2], seen[0]["messages"])
        self.assertEqual(repair_messages[-2], {"role": "assistant", "content": rejected})
        reason = repair_messages[-1]["content"]
        self.assertIn("QUOTE_CUSTODY_FAILURE: quotes[4]", reason)
        self.assertIn("quote does not resolve to exact UTF-8 bytes", reason)
        self.assertIn("UNAUTHORIZED_MODEL_REFERENCE", reason)
        self.assertIn("docs/sources/FW5-explanatory-construction.md", reason)
        self.assertIn("bytes:<start>:<end>", seen[0]["messages"][-1]["content"])
        self.assertIn("zero-based, end-exclusive UTF-8", seen[0]["messages"][-1]["content"])

    def test_uc4_original_quote_remains_refused_after_three_repairs(self) -> None:
        rejected = live_body("UC4-c0003-a00")
        seen: list[dict] = []

        def scripted(**context):
            seen.append(context)
            return {"content": rejected}

        pilot = self.pilot("UC4", "uc4-original-twice", scripted)
        with self.assertRaises(ReasonFailure) as caught:
            pilot.execute_template("evidence_read", pilot.inputs, 1)
        self.assertEqual(caught.exception.code, "SCHEMA_REJECTED")
        self.assertEqual(len(seen), 4)
        self.assertEqual([item["status"] for item in pilot.calls.receipts],
                         ["contract_rejected"] * 4)
        second = read_json(pilot.root / "calls" / "c0001" / "a01" / "outcome.json")
        self.assertIn("QUOTE_CUSTODY_FAILURE: quotes[4]", second["validation_error"])
        self.assertIn("UNAUTHORIZED_MODEL_REFERENCE", second["validation_error"])

    def test_undeclared_source_read_complete_without_evidence_and_fabricated_quote_are_refused(self) -> None:
        pilot = self.pilot("UC4", "negative-contracts", scripted=[])
        self.set_live_route(pilot, "UC4")
        undeclared = self.canonical_spawn(pilot)
        undeclared["subtasks"][0]["source_reads"] = [{
            "unit_id": "0" * 64,
            "start": 0,
            "end": 1,
            "limit": 1,
        }]
        with self.assertRaisesRegex(ValueError, "INPUT_UNPINNED"):
            pilot._validate_spawn(undeclared)

        sources = self.uc4_sources(pilot)
        unsupported = {
            "status": "complete",
            "answer": "unsupported",
            "source_refs": [],
            "unresolved": [],
            "verification_refs": [],
            "quotes": [],
            "contradictions": [],
            "not_found": [],
        }
        with self.assertRaisesRegex(ValueError, "EVIDENCE_COMPLETE_WITHOUT_SUPPORT"):
            pilot._validate_worker_output(unsupported, sources, evidence=True)
        fabricated = copy.deepcopy(unsupported)
        fabricated["status"] = "partial"
        fabricated["quotes"] = [{
            "claim": "fabricated",
            "source_id": "FW5-excerpts",
            "locator": "bytes:0:20",
            "quote": "not present in source",
        }]
        with self.assertRaisesRegex(ValueError, r"QUOTE_CUSTODY_FAILURE: quotes\[0\]"):
            pilot._validate_worker_output(fabricated, sources, evidence=True)

        wrong_source = copy.deepcopy(fabricated)
        wrong_source["quotes"][0].update({
            "source_id": "not-exposed",
            "locator": "bytes:0:1",
            "quote": sources["FW5-excerpts"][0],
        })
        with self.assertRaisesRegex(ValueError, "source_id is not an exposed document id"):
            pilot._validate_worker_output(wrong_source, sources, evidence=True)

        unicode_offset = next(index for index, character in enumerate(sources["FW5-excerpts"])
                              if len(character.encode("utf-8")) > 1)
        unicode_quote = sources["FW5-excerpts"][unicode_offset]
        byte_start = len(sources["FW5-excerpts"][:unicode_offset].encode("utf-8"))
        byte_end = byte_start + len(unicode_quote.encode("utf-8"))
        exact_unicode = copy.deepcopy(fabricated)
        exact_unicode["quotes"][0].update({
            "source_id": "FW5-excerpts",
            "locator": f"bytes:{byte_start}:{byte_end}",
            "quote": unicode_quote,
        })
        pilot._validate_worker_output(exact_unicode, sources, evidence=True)
        wrong_offset = copy.deepcopy(exact_unicode)
        wrong_offset["quotes"][0]["locator"] = f"bytes:{byte_start + 1}:{byte_end}"
        # P-A4 treats authored offsets as untrusted hints. Exact quote/source
        # bytes still pass and execute_template records authoritative spans.
        pilot._validate_worker_output(wrong_offset, sources, evidence=True)

    def test_live_fixture_custody_hashes_cover_every_replayed_body(self) -> None:
        custody = read_json(FIXTURES / "CUSTODY.json")
        self.assertEqual(custody["schema"], "minireason.pilot.live-response-fixture-custody.v1")
        self.assertEqual(len(custody["entries"]), 11)
        for entry in custody["entries"]:
            with self.subTest(fixture=entry["fixture"]):
                fixture = ROOT / entry["fixture"]
                raw = fixture.read_bytes()
                actual = hashlib.sha256(raw).hexdigest()
                self.assertEqual(len(raw), entry["byte_count"])
                self.assertEqual(actual, entry["fixture_sha256"])
                self.assertEqual(actual, entry["public_content_sha256"])
                self.assertFalse(entry["reasoning_content_present"])
                self.assertFalse(entry["reasoning_content_persisted"])

    def test_corrected_task_files_load_and_selected_template_inputs_validate(self) -> None:
        for usecase, task_path in TASK_PATHS.items():
            with self.subTest(usecase=usecase):
                task = read_json(task_path)
                store = TaskInputs.from_task(task, ROOT)
                inputs = normalize_inputs(task["task"], store.resolved_inputs)
                proposal = json.loads(live_body(f"{usecase}-c0001-a00"))
                selected = select_template({
                    "task": task["task"],
                    "features": task.get("features", {}),
                    "inputs": inputs,
                }, proposal)
                validate_inputs(selected["template_id"], inputs)
                compact = store.compact_inputs(inputs)
                self.assertEqual(store.expand_inputs(compact, call_id="task-load-test"), inputs)
                if usecase == "UC2":
                    self.assertTrue(inputs["documents"])


if __name__ == "__main__":
    unittest.main()
