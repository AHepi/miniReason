"""Offline acceptance tests for the R002 bounded checker host."""
from __future__ import annotations

import json
import os
from pathlib import Path
import unittest
from unittest import mock
import uuid

import jsonschema

from minireason.reason.checker import BACKEND, CheckerRunner, run_checker


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((
    ROOT / "experiments/diagnostics/R002-episodes-under-calibrated-difficulty"
    / "contracts/checker-execution.schema.json"
).read_text(encoding="utf-8"))
TMP = Path(os.environ.get("TMP", "C:/tr20"))


def source(value_expression: str = "data['n'] * 2", *, relation: str = "r1") -> str:
    return (
        "import json\n"
        "import sys\n"
        "data = json.load(sys.stdin)\n"
        f"value = {value_expression}\n"
        f"print(json.dumps({{'relation_id': '{relation}', 'value': value, "
        "'derivation': 'computed from explicit stdin'}, separators=(',', ':')))\n"
    )


def proposal(*, checker_source: str | None = None, working_value=6, stdin=None) -> dict:
    return {
        "query_id": "q1",
        "question": "What is twice n?",
        "relation_id": "r1",
        "working_claim_quote": "Twice n is 6.",
        "working_value": working_value,
        "language": "python-3.11-restricted",
        "source": checker_source if checker_source is not None else source(),
        "stdin_json": {"n": 3} if stdin is None else stdin,
        "expected_output_schema": {
            "relation_id": "string", "value": "json", "derivation": "string"
        },
    }


class R002CheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TMP.mkdir(parents=True, exist_ok=True)

    def check_schema(self, record):
        jsonschema.Draft202012Validator(SCHEMA).validate(record)

    def test_match_runs_once_and_preserves_schema_record(self):
        record = run_checker(proposal())
        self.check_schema(record)
        self.assertEqual(record["status"], "COMPLETE")
        self.assertEqual(record["comparison"], "agrees")
        self.assertEqual(record["parsed"]["value"], 6)
        self.assertEqual(record["sandbox_backend"], BACKEND)
        self.assertEqual(record["limit_breaches"], [])
        self.assertEqual(record["exit_code"], 0)

    def test_canonical_json_comparison_preserves_types(self):
        record = run_checker(proposal(
            checker_source=source("1"), working_value=True))
        self.check_schema(record)
        self.assertEqual(record["status"], "COMPLETE")
        self.assertEqual(record["comparison"], "disagrees")
        self.assertEqual(record["parsed"]["value"], 1)
        self.assertIs(type(record["parsed"]["value"]), int)

    def test_mismatch_is_reported_without_declaring_a_winner(self):
        record = run_checker(proposal(working_value=7))
        self.check_schema(record)
        self.assertEqual(record["status"], "COMPLETE")
        self.assertEqual(record["comparison"], "disagrees")
        self.assertNotIn("winner", record)

    def test_forbidden_import_families_are_refused_statically(self):
        cases = {
            "os": "import os\n",
            "subprocess": "import subprocess\n",
            "socket": "import socket\n",
            "urllib": "import urllib.request\n",
            "requests": "import requests\n",
        }
        for expected_breach, checker_source in cases.items():
            with self.subTest(module=expected_breach):
                record = run_checker(proposal(checker_source=checker_source))
                self.check_schema(record)
                self.assertEqual(record["status"], "REFUSED_POLICY")
                category = "network" if expected_breach in {"socket", "urllib", "requests"} else (
                    "filesystem" if expected_breach == "os" else "nondeterministic_api")
                self.assertIn(category, record["limit_breaches"])
                self.assertIsNone(record["exit_code"])

    def test_filesystem_dynamic_import_and_reflection_are_refused(self):
        cases = [
            "print(open('outside.txt').read())\n",
            "module = __import__('os')\n",
            "import sys\nprint(sys.modules)\n",
            "print((1).__class__)\n",
            "print(getattr({}, 'keys'))\n",
            "from sys import modules\n",
            "import operator\nprint(operator.attrgetter('__class__')(1))\n",
            "from operator import methodcaller as invoke\nprint(invoke('keys')({}))\n",
            "print('{0.__class__}'.format(1))\n",
            "print('{x.__class__}'.format_map({'x': 1}))\n",
        ]
        for checker_source in cases:
            with self.subTest(source=checker_source):
                record = run_checker(proposal(checker_source=checker_source))
                self.check_schema(record)
                self.assertEqual(record["status"], "REFUSED_POLICY")
                self.assertIsNone(record["parsed"])

    def test_timeout_kills_the_checker(self):
        checker_source = "while True:\n    pass\n"
        record = run_checker(proposal(checker_source=checker_source), policy={
            "policy": "restricted-python-v1", "timeout_seconds": 0.08
        })
        self.check_schema(record)
        self.assertEqual(record["status"], "TIMEOUT")
        self.assertIn("wall_seconds", record["limit_breaches"])
        self.assertLess(record["elapsed_ms"], 3000)

    def test_stdout_and_stderr_limits_are_bounded(self):
        cases = [
            ("print('x' * 10000)\n", "stdout_bytes"),
            ("import sys\nprint('x' * 10000, file=sys.stderr)\n", "stderr_bytes"),
        ]
        for checker_source, breach in cases:
            with self.subTest(breach=breach):
                record = run_checker(proposal(checker_source=checker_source), policy={
                    "policy": "restricted-python-v1",
                    "stdout_bytes": 512,
                    "stderr_bytes": 512,
                })
                self.check_schema(record)
                self.assertEqual(record["status"], "OUTPUT_LIMIT")
                self.assertIn(breach, record["limit_breaches"])
                self.assertLessEqual(len(record["stdout_utf8"].encode("utf-8")), 512)
                self.assertLessEqual(len(record["stderr_utf8"].encode("utf-8")), 512)

    def test_fast_oversized_output_is_not_misclassified_complete(self):
        checker_source = (
            "import json\n"
            "print(json.dumps({'relation_id':'r1','value':6,'derivation':'d'}))\n"
            "print('x' * 10000)\n"
        )
        record = run_checker(proposal(checker_source=checker_source), policy={
            "policy": "restricted-python-v1", "stdout_bytes": 512
        })
        self.check_schema(record)
        self.assertEqual(record["status"], "OUTPUT_LIMIT")
        self.assertIn("stdout_bytes", record["limit_breaches"])
        self.assertIsNone(record["parsed"])

    def test_large_stdin_cannot_block_timeout_monitor(self):
        record = run_checker(
            proposal(checker_source="while True:\n    pass\n", stdin={"blob": "x" * 200000}),
            policy={"policy": "restricted-python-v1", "timeout_seconds": 0.08},
        )
        self.check_schema(record)
        self.assertEqual(record["status"], "TIMEOUT")
        self.assertLess(record["elapsed_ms"], 3000)

    def test_invalid_numeric_policy_is_refused_without_conversion_error(self):
        for invalid in ("large", float("nan"), float("inf")):
            with self.subTest(value=invalid):
                record = run_checker(proposal(), policy={
                    "policy": "restricted-python-v1", "source_bytes": invalid
                })
                self.check_schema(record)
                self.assertEqual(record["status"], "REFUSED_POLICY")

    def test_memory_limit_stops_large_allocation(self):
        record = run_checker(
            proposal(checker_source="data = bytearray(160 * 1024 * 1024)\n"),
            policy={"policy": "restricted-python-v1", "memory_mib": 64},
        )
        self.check_schema(record)
        self.assertEqual(record["status"], "NONZERO_EXIT")
        self.assertNotEqual(record["exit_code"], 0)
        self.assertIn("memory_mib", record["limit_breaches"])

    def test_nonzero_and_invalid_output_are_distinct(self):
        nonzero = run_checker(proposal(checker_source="raise RuntimeError('fixture')\n"))
        invalid = run_checker(proposal(checker_source="print('{}')\n"))
        self.check_schema(nonzero)
        self.check_schema(invalid)
        self.assertEqual(nonzero["status"], "NONZERO_EXIT")
        self.assertEqual(invalid["status"], "OUTPUT_INVALID")
        self.assertEqual(nonzero["comparison"], "not_compared")
        self.assertEqual(invalid["comparison"], "not_compared")

    def test_extra_proposal_fields_and_oversized_source_are_refused(self):
        extra = proposal()
        extra["execution_result"] = "model-claimed"
        first = run_checker(extra)
        second = run_checker(proposal(checker_source="#" * 33000))
        self.check_schema(first)
        self.check_schema(second)
        self.assertEqual(first["status"], "REFUSED_POLICY")
        self.assertEqual(second["status"], "REFUSED_POLICY")

    def test_live_mode_fails_closed_on_unreviewed_runtime(self):
        with mock.patch("minireason.reason.checker.REVIEWED_RUNTIME_SHA256", "0" * 64):
            record = run_checker(proposal(), mode="live")
        self.check_schema(record)
        self.assertEqual(record["status"], "REFUSED_POLICY")
        self.assertIsNone(record["exit_code"])

    def test_runner_writes_exact_write_once_evidence(self):
        from tests.reason import artifact_root
        evidence = artifact_root() / "checker" / uuid.uuid4().hex
        runner = CheckerRunner(mode="offline")
        raw = json.dumps(proposal(), ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
        record = runner.run(raw, None, evidence)
        self.check_schema(record)
        self.assertEqual((evidence / "proposal.json").read_bytes(), raw)
        self.assertTrue((evidence / "policy.json").read_bytes())
        self.assertEqual(json.loads((evidence / "execution.json").read_text(
            encoding="utf-8")), record)
        self.assertEqual((evidence / "checker.py").read_text(
            encoding="utf-8"), proposal()["source"])
        with self.assertRaises(FileExistsError):
            runner.run(raw, None, evidence)

    def test_child_environment_does_not_inherit_parent_marker(self):
        # A proposal cannot import os or reach sys.modules, which closes the
        # public route to the environment.  The parent marker must not affect
        # an otherwise identical deterministic execution record.
        with mock.patch.dict(os.environ, {"R002_SECRET_FIXTURE": "dummy"}):
            record = run_checker(proposal())
        self.check_schema(record)
        self.assertEqual(record["status"], "COMPLETE")
        self.assertNotIn("dummy", record["stdout_utf8"] + record["stderr_utf8"])

    def test_fixed_hash_seed_makes_set_order_repeatable(self):
        checker_source = (
            "import json\n"
            "value = list({'alpha', 'beta', 'gamma', 'delta', 'epsilon'})\n"
            "print(json.dumps({'relation_id':'r1','value':value,'derivation':'set order'}, "
            "separators=(',', ':')))\n"
        )
        first = run_checker(proposal(checker_source=checker_source, working_value=[]))
        second = run_checker(proposal(checker_source=checker_source, working_value=[]))
        self.check_schema(first)
        self.check_schema(second)
        self.assertEqual(first["status"], "COMPLETE")
        self.assertEqual(second["status"], "COMPLETE")
        self.assertEqual(first["stdout_utf8"], second["stdout_utf8"])
        self.assertEqual(first["stdout_sha256"], second["stdout_sha256"])
        self.assertEqual(first["parsed"], second["parsed"])

    def test_invalid_json_proposal_hashes_the_original_bytes(self):
        raw = b'{"truncated":'
        record = run_checker(raw)
        self.check_schema(record)
        import hashlib
        self.assertEqual(record["status"], "REFUSED_POLICY")
        self.assertEqual(record["proposal_sha256"], hashlib.sha256(raw).hexdigest())

    def test_unreadable_runtime_digest_fails_before_execution(self):
        with mock.patch("minireason.reason.checker.Path.read_bytes", side_effect=OSError("fixture")):
            with self.assertRaisesRegex(RuntimeError, "runtime bytes are unavailable"):
                run_checker(proposal(checker_source="import os\n"))


if __name__ == "__main__":
    unittest.main()
