from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from minireason.reason import config, r002_launcher
from minireason.reason.adapter import Adapter
from minireason.reason.r002_preflight import snapshot_tokenizers, token_preflight
from minireason.reason.types import ReasonFailure


REPO = Path(__file__).resolve().parents[2]
STUDY = REPO / "experiments" / "diagnostics" / "R002-episodes-under-calibrated-difficulty"
PINS = STUDY / "calibration" / "main-tokenizer-pins.json"
PYTHON = Path(r"C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe")


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return json.load(handle)


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


class R002ConservativeByteBoundTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.descriptor = snapshot_tokenizers(PINS, "offline")

    def test_all_24_preserved_usage_rows_have_byte_margin(self) -> None:
        evidence = self.descriptor["calibration_evidence"]
        self.assertEqual(evidence["row_count"], 24)
        self.assertEqual(evidence["minimum_prompt_tokens_to_wire_bytes"], "0.235968765")
        self.assertEqual(evidence["maximum_prompt_tokens_to_wire_bytes"], "0.266547406")
        self.assertEqual(evidence["minimum_byte_margin"], 2954)
        self.assertEqual(
            {row["candidate_id"] for row in evidence["rows"]},
            {f"C{number:02d}" for number in range(1, 25)},
        )
        for row in evidence["rows"]:
            self.assertLessEqual(row["prompt_tokens"], row["wire_utf8_bytes"])
            self.assertEqual(row["byte_margin"], row["wire_utf8_bytes"] - row["prompt_tokens"])

    def test_33000_byte_canonical_wire_fails_closed_without_truncation(self) -> None:
        messages = [
            {"role": "system", "content": "Return JSON."},
            {"role": "user", "content": "x"},
        ]
        payload = {
            "model": "deepseek-flash",
            "messages": messages,
            "stream": False,
            "max_tokens": 32768,
            "response_format": {"type": "json_object"},
            "thinking": {"type": "enabled"},
            "reasoning_effort": "medium",
        }
        empty_wire = json.dumps(payload)
        messages[1]["content"] += "x" * (33000 - len(empty_wire.encode("utf-8")))
        wire = json.dumps(payload)
        self.assertEqual(len(wire.encode("utf-8")), 33000)
        with self.assertRaises(ReasonFailure) as caught:
            token_preflight(
                messages, "deepseek-flash", self.descriptor, "offline",
                wire_body_text=wire, condition="NATIVE", role="answer",
            )
        self.assertEqual(caught.exception.code, "PROMPT_TOKEN_CAP")
        self.assertEqual(caught.exception.record["counted_tokens"], 33000)
        self.assertEqual(caught.exception.record["wire_utf8_bytes"], 33000)
        self.assertEqual(caught.exception.record["outcome"], "stop_no_truncate")
        self.assertEqual(
            caught.exception.record["counted_tokens_semantics"],
            "conservative-upper-bound-not-tokenizer-count",
        )

    def test_preflight_hash_is_the_offline_transport_would_send_hash(self) -> None:
        cases = (
            ("deepseek-flash", "native", 32768),
            ("deepseek-flash", "off", 16384),
            ("ollama/qwen3.5-397b.native", "off", 16384),
            ("ollama/glm-5.3.native", "off", 16384),
        )
        messages = [
            {"role": "system", "content": "Return one JSON object."},
            {"role": "user", "content": "Use the exact transport builder."},
        ]
        with tempfile.TemporaryDirectory(dir=r"C:\tw22") as temporary:
            adapter = Adapter("offline", {"data": config.load_endpoint_snapshot()["data"]})
            for index, (endpoint, thinking, ceiling) in enumerate(cases):
                coordinate = {
                    "call_id": f"proof-{index}", "cycle": 0, "attempt": 0,
                    "condition": "NATIVE" if index == 0 else "LOOP-TESTED", "strict": True,
                }
                prepared = adapter.prepare(
                    seat=endpoint, messages=messages, max_tokens=ceiling,
                    thinking=thinking, role="answer", coordinate=coordinate,
                )
                preflight = token_preflight(
                    messages, endpoint, self.descriptor, "offline",
                    wire_body_text=prepared["wire_body_text"],
                    condition=coordinate["condition"], role="answer",
                )
                records = Path(temporary) / f"p{index}"
                adapter.call(
                    seat=endpoint, messages=messages, records_dir=records,
                    max_tokens=ceiling, thinking=thinking, role="answer",
                    coordinate=coordinate, scripted={"content": "{}"},
                )
                transport = read_json(records / "call-0001.request.json")
                self.assertEqual(prepared["wire_body_text"], transport["wire_body_text"])
                self.assertEqual(prepared["wire_body_sha256"], transport["wire_body_sha256"])
                self.assertEqual(preflight["wire_body_sha256"], transport["wire_body_sha256"])
                self.assertEqual(
                    transport["wire_body_sha256"],
                    hashlib.sha256(transport["wire_body_text"].encode("utf-8")).hexdigest(),
                )
                self.assertEqual(preflight["wire_utf8_bytes"], transport["would_send_bytes"])
                self.assertIsNone(transport["url"])
                self.assertTrue(transport["not_contacted_url"])
                self.assertEqual(transport["request_header_names"], [])

    def test_malformed_or_unsubstantiated_descriptor_is_rejected(self) -> None:
        mutations = []
        missing_endpoint = copy.deepcopy(self.descriptor)
        del missing_endpoint["endpoints"]["ollama/glm-5.3.native"]
        mutations.append(missing_endpoint)
        changed_scope = copy.deepcopy(self.descriptor)
        changed_scope["qualification_scope"] = "observations prove all providers"
        mutations.append(changed_scope)
        changed_builder = copy.deepcopy(self.descriptor)
        changed_builder["transport_serialization"]["source_sha256"][
            "src/minireason/reason/adapter.py"
        ] = "0" * 64
        mutations.append(changed_builder)
        changed_evidence = copy.deepcopy(self.descriptor)
        changed_evidence["calibration_evidence"]["rows"][0][
            "prompt_tokens_to_wire_bytes"
        ] = "1.000000000"
        mutations.append(changed_evidence)
        for descriptor in mutations:
            with self.subTest(mutation=len(mutations)):
                with self.assertRaises(ReasonFailure):
                    snapshot_tokenizers(descriptor, "offline")

    def test_offline_main_accepts_descriptor_through_launcher(self) -> None:
        candidate_id = "C05"
        candidate = r002_launcher.candidate_record(STUDY, candidate_id)
        admission = {
            "schema": r002_launcher.ADMISSION_SCHEMA,
            "evidence_kind": "offline-test-fixture",
            "records": [{
                "candidate_id": candidate_id,
                "verdict": "no_answer",
                "admitted": True,
                "operational_status": "ceiling_hit",
                "native_final_answer_path": None,
                "problem_sha256": candidate["problem_sha256"],
                "sealed_answer_sha256": candidate["sealed_answer_sha256"],
                "oracle_sha256": candidate["oracle_sha256"],
                "oracle_kind": candidate["oracle_kind"],
            }],
        }
        with tempfile.TemporaryDirectory(dir=r"C:\tw22") as temporary:
            root = Path(temporary)
            admission_path = root / "admission.json"
            write_json(admission_path, admission)
            environment = os.environ.copy()
            environment.pop("DEEPSEEK_API_KEY", None)
            environment.pop("OLLAMA_API_KEY", None)
            environment.update({
                "PYTHONPATH": os.pathsep.join((str(REPO / "src"), str(REPO / "tests"))),
                "PYTHONUTF8": "1",
                "PYTHONIOENCODING": "utf-8",
                "PYTHONDONTWRITEBYTECODE": "1",
                "TMP": r"C:\tw22",
            })
            completed = subprocess.run(
                [
                    str(PYTHON), "-B", "-X", "utf8", str(REPO / "tools" / "run_R002.py"),
                    "--phase", "main", "--mode", "offline", "--run-root", str(root / "run"),
                    "--admission-receipt", str(admission_path), "--problems", candidate_id,
                    "--tokenizer-pins", str(PINS),
                ],
                cwd=REPO, env=environment, capture_output=True, text=True,
                encoding="utf-8", errors="strict", check=False,
            )
            child_logs = "\n".join(
                f"{path.name}:\n{path.read_text(encoding='utf-8', errors='strict')}"
                for pattern in ("*.stdout.txt", "*.stderr.txt")
                for path in sorted((root / "run").rglob(pattern))
            )
            self.assertEqual(
                completed.returncode, 0,
                completed.stdout + completed.stderr + "\nCHILD STDERR:\n" + child_logs,
            )
            manifest = read_json(root / "run" / "manifest.json")
            phase = manifest["phases"]["main-occurrence-001"]
            self.assertEqual(phase["selected_candidates"], [candidate_id])
            self.assertEqual(phase["tokenizer_pins_sha256"], hashlib.sha256(PINS.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
