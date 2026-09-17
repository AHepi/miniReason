"""Live pilot CLI tests with an actual worker and no network/provider call."""
from __future__ import annotations

from contextlib import redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

from minireason import provider_openai_compat as provider
from minireason.pilot import __main__ as pilot_cli

from ._transport_fixture import DUMMY_VALUE, install_transport_double, write_text


ROOT = Path(__file__).resolve().parents[2]
TASK = {
    "task": "What is 6 times 7? Return the integer as plain text.",
    "features": {"short_closed": True},
    "check": {
        "source": (
            "import json, sys\n"
            "x = json.load(sys.stdin)\n"
            "value = x['artifact']['answer'] == '42'\n"
            "print(json.dumps({'relation_id':'pilot-result','value':value,'derivation':'fixture'}))\n"
        ),
        "expected": True,
        "scope": "The answer is 42.",
        "fixtures": {},
    },
}


def read_json(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return json.load(handle)


def pinned_source_task(work: Path) -> tuple[dict, str, str]:
    source_text = "The pinned value is exactly 42."
    inputs = {
        "documents": [{"id": "source-selection", "text": "Read the selected pinned source range."}],
        "requested_claims": ["Identify the exact pinned value."],
    }
    input_text = json.dumps(inputs, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    input_bytes = input_text.encode("utf-8")
    source_bytes = source_text.encode("utf-8")
    input_sha = hashlib.sha256(input_bytes).hexdigest()
    source_sha = hashlib.sha256(source_bytes).hexdigest()
    write_text(work / "task-inputs.json", input_text)
    write_text(work / "source.txt", source_text)
    task = json.loads(json.dumps(TASK))
    task["task"] = "Read the supplied public source and return its exact pinned value."
    task["features"] = {"kind": "evidence"}
    task["inputs"] = {"unit_id": input_sha, "start": 0, "end": len(input_bytes), "encoding": "json"}
    task["input_units"] = [
        {"unit_id": input_sha, "sha256": input_sha, "byte_count": len(input_bytes),
         "path": "task-inputs.json", "media_type": "application/json", "role": "task_input"},
        {"unit_id": source_sha, "sha256": source_sha, "byte_count": len(source_bytes),
         "path": "source.txt", "media_type": "text/plain", "role": "public_source"},
    ]
    return task, source_sha, source_text


class LiveCliTransportBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work_parent = ROOT / "work" / "w45" / "test-pilot-transport"
        cls.work_parent.mkdir(parents=True, exist_ok=True)
        check = subprocess.run(
            ["git", "-C", str(ROOT), "check-ignore", "--no-index", "--quiet", "--", str(cls.work_parent)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
        )
        if check.returncode != 0:
            raise RuntimeError("pilot transport test work directory must be ignored")

    def run_live(self, force_repair: bool, pass_limit: int = 1, pinned_source: bool = False) -> dict:
        tmp_parent = Path(os.environ["TMP"])
        tmp_parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=self.work_parent) as work_name, tempfile.TemporaryDirectory(dir=tmp_parent) as run_name:
            work = Path(work_name)
            run_root = Path(run_name) / "run"
            task_file = work / "task.json"
            transport = work / "transport"
            capture_dir = work / "captured-wire"
            task = TASK
            source_sha = None
            source_text = None
            if pinned_source:
                task, source_sha, source_text = pinned_source_task(work)
            write_text(task_file, json.dumps(task, ensure_ascii=False, indent=2) + "\n")
            install_transport_double(transport)
            fixture_env = {
                "PYTHONPATH": str(transport) + os.pathsep + str(ROOT / "src") + os.pathsep + str(ROOT / "tests"),
                "MINIREASON_PILOT_TEST_FORCE_ROUTE_REPAIR": "1" if force_repair else "0",
                "MINIREASON_PILOT_TEST_PASS_LIMIT": str(pass_limit),
                "MINIREASON_PILOT_TEST_CAPTURE_DIR": str(capture_dir),
                "DEEPSEEK_API_KEY": DUMMY_VALUE,
            }
            captured = io.StringIO()
            with mock.patch.dict(os.environ, fixture_env), redirect_stdout(captured), mock.patch.object(
                provider, "_open", side_effect=AssertionError("parent process network forbidden")
            ):
                code = pilot_cli.main([
                    "run", "--task", str(task_file), "--repo-root", str(work), "--mode", "live",
                    "--out", str(run_root), "--max-calls", "24",
                ])
            stdout = captured.getvalue()
            self.assertNotIn(DUMMY_VALUE, stdout)
            public = json.loads([line for line in stdout.splitlines() if line.strip()][-1])
            attempts = sorted((run_root / "calls").glob("c*/a*"))
            records = []
            call_records = []
            expected_capture_hashes = []
            for attempt in attempts:
                decision = read_json(attempt / "decision.json")
                request = read_json(attempt / "provider/call-0001.request.json")
                response = read_json(attempt / "provider/call-0001.response.json")
                outcome = read_json(attempt / "outcome.json")
                wire_sha = hashlib.sha256(request["wire_body_text"].encode("utf-8")).hexdigest()
                actual_sha = request["request_bytes_sha256"]
                self.assertEqual(decision["prepared_wire_sha256"], wire_sha)
                self.assertEqual(decision["input_preflight"]["wire_sha256"], wire_sha)
                self.assertEqual(outcome["input_preflight"]["wire_sha256"], wire_sha)
                self.assertEqual(request["wire_body_sha256"], wire_sha)
                self.assertEqual(actual_sha, wire_sha)
                expected_capture_hashes.append(wire_sha)
                self.assertEqual(outcome["started_epoch"], request["recorded_epoch"])
                self.assertEqual(outcome["finished_epoch"], response["recorded_epoch"])
                self.assertEqual(outcome["usage"], response["usage"])
                self.assertFalse(response["reasoning_content_persisted"])
                self.assertFalse(outcome["hidden_reasoning_persisted"])
                self.assertNotIn("reasoning_content", response)
                records.append(outcome["status"])
                user_packets = []
                for message in request["request"]["messages"]:
                    if message.get("role") != "user":
                        continue
                    try:
                        candidate = json.loads(message["content"])
                    except (TypeError, ValueError):
                        continue
                    if isinstance(candidate, dict):
                        user_packets.append(candidate)
                call_records.append({
                    "role": decision["role"], "user_packets": user_packets,
                    "source_reads": outcome.get("source_reads", []),
                })
            captured_wires = sorted(capture_dir.glob("*.wire"))
            self.assertEqual(len(captured_wires), len(attempts))
            self.assertCountEqual(
                [hashlib.sha256(path.read_bytes()).hexdigest() for path in captured_wires],
                expected_capture_hashes,
            )
            for path in run_root.rglob("*"):
                if path.is_file():
                    self.assertNotIn(DUMMY_VALUE.encode("utf-8"), path.read_bytes())
            return {"code": code, "public": public, "statuses": records, "attempts": len(attempts),
                    "calls": call_records, "source_sha": source_sha, "source_text": source_text}

    def test_live_cli_worker_transport_and_custody(self):
        result = self.run_live(False)
        self.assertEqual(result["code"], 0)
        self.assertEqual(result["public"]["status"], "complete")
        self.assertEqual(result["statuses"], ["accepted", "accepted", "accepted", "accepted"])
        self.assertEqual(result["attempts"], 4)

    def test_live_cli_schema_repair_preserves_wire_custody(self):
        result = self.run_live(True)
        self.assertEqual(result["code"], 0)
        self.assertEqual(result["public"]["status"], "complete")
        self.assertEqual(result["statuses"], ["contract_rejected", "accepted", "accepted", "accepted", "accepted"])
        self.assertEqual(result["attempts"], 5)

    def test_live_cli_transport_completes_two_full_passes(self):
        result = self.run_live(False, pass_limit=2)
        self.assertEqual(result["code"], 0)
        self.assertEqual(result["public"]["status"], "complete")
        self.assertEqual(result["public"]["logical_calls"], 8)
        self.assertEqual(result["statuses"], ["accepted"] * 8)
        self.assertEqual(result["attempts"], 8)

    def test_live_cli_pinned_source_uses_compact_spawn_and_exact_exposure(self):
        result = self.run_live(False, pinned_source=True)
        self.assertEqual((result["code"], result["public"]["status"]), (0, "complete"))
        spawn_call = next(item for item in result["calls"] if item["role"] == "spawn")
        spawn_packet = next(packet for packet in spawn_call["user_packets"] if "input_catalog" in packet)
        self.assertEqual(set(spawn_packet["inputs"]), {"unit_id", "start", "end", "encoding"})
        self.assertNotIn(result["source_text"], json.dumps(spawn_packet, ensure_ascii=False))
        worker_call = next(item for item in result["calls"] if item["role"] == "evidence_read")
        exact_reads = [receipt for receipt in worker_call["source_reads"]
                       if receipt.get("schema") == "pilot.source-read.pa2.v1"
                       and receipt.get("delivery") == "outgoing tool-result data"]
        self.assertEqual(len(exact_reads), 1)
        self.assertEqual(exact_reads[0]["unit_id"], result["source_sha"])
        self.assertEqual(exact_reads[0]["unit_sha256"], result["source_sha"])
        self.assertEqual(exact_reads[0]["excerpt_sha256"], result["source_sha"])
        self.assertEqual(exact_reads[0]["omitted_ranges"], [])
        worker_packet = next(packet for packet in worker_call["user_packets"] if "resolved_source_reads" in packet)
        self.assertEqual(worker_packet["resolved_source_reads"][0]["content"], result["source_text"])


if __name__ == "__main__":
    unittest.main()
