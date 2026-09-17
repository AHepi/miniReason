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


class LiveCliTransportBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work_parent = ROOT / "work" / "w38" / "test-pilot-transport"
        cls.work_parent.mkdir(parents=True, exist_ok=True)
        check = subprocess.run(
            ["git", "-C", str(ROOT), "check-ignore", "--no-index", "--quiet", "--", str(cls.work_parent)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
        )
        if check.returncode != 0:
            raise RuntimeError("pilot transport test work directory must be ignored")

    def run_live(self, force_repair: bool, pass_limit: int = 1) -> dict:
        tmp_parent = Path(os.environ["TMP"])
        tmp_parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=self.work_parent) as work_name, tempfile.TemporaryDirectory(dir=tmp_parent) as run_name:
            work = Path(work_name)
            run_root = Path(run_name) / "run"
            task_file = work / "task.json"
            transport = work / "transport"
            write_text(task_file, json.dumps(TASK, ensure_ascii=False, indent=2) + "\n")
            install_transport_double(transport)
            fixture_env = {
                "PYTHONPATH": str(transport) + os.pathsep + str(ROOT / "src") + os.pathsep + str(ROOT / "tests"),
                "MINIREASON_PILOT_TEST_FORCE_ROUTE_REPAIR": "1" if force_repair else "0",
                "MINIREASON_PILOT_TEST_PASS_LIMIT": str(pass_limit),
                "DEEPSEEK_API_KEY": DUMMY_VALUE,
            }
            captured = io.StringIO()
            with mock.patch.dict(os.environ, fixture_env), redirect_stdout(captured), mock.patch.object(
                provider, "_open", side_effect=AssertionError("parent process network forbidden")
            ):
                code = pilot_cli.main([
                    "run", "--task", str(task_file), "--mode", "live",
                    "--out", str(run_root), "--max-calls", "24",
                ])
            stdout = captured.getvalue()
            self.assertNotIn(DUMMY_VALUE, stdout)
            public = json.loads([line for line in stdout.splitlines() if line.strip()][-1])
            attempts = sorted((run_root / "calls").glob("c*/a*"))
            records = []
            for attempt in attempts:
                decision = read_json(attempt / "decision.json")
                request = read_json(attempt / "provider/call-0001.request.json")
                response = read_json(attempt / "provider/call-0001.response.json")
                outcome = read_json(attempt / "outcome.json")
                wire_sha = hashlib.sha256(request["wire_body_text"].encode("utf-8")).hexdigest()
                actual_sha = request["request_bytes_sha256"]
                self.assertEqual(decision["prepared_wire_sha256"], wire_sha)
                self.assertEqual(request["wire_body_sha256"], wire_sha)
                self.assertEqual(actual_sha, wire_sha)
                self.assertEqual(outcome["started_epoch"], request["recorded_epoch"])
                self.assertEqual(outcome["finished_epoch"], response["recorded_epoch"])
                self.assertEqual(outcome["usage"], response["usage"])
                self.assertFalse(response["reasoning_content_persisted"])
                self.assertFalse(outcome["hidden_reasoning_persisted"])
                self.assertNotIn("reasoning_content", response)
                records.append(outcome["status"])
            for path in run_root.rglob("*"):
                if path.is_file():
                    self.assertNotIn(DUMMY_VALUE.encode("utf-8"), path.read_bytes())
            return {"code": code, "public": public, "statuses": records, "attempts": len(attempts)}

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


if __name__ == "__main__":
    unittest.main()
