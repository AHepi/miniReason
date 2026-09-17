"""R3-A1 byte-bound and occurrence-selection regression fixtures; never live calls."""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from minireason.reason.adapter import Adapter
from minireason.reason.r002_preflight import snapshot_tokenizers, token_preflight
from minireason.reason.types import ReasonFailure
from tests.reason.test_r003_launcher import launcher

DESCRIPTOR = launcher.STUDY / "R003-input-preflight.json"
ROUTE = "ollama/qwen3.5-397b.native"

class R3A1PreflightTests(unittest.TestCase):
    def descriptor(self, window=131072):
        data = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
        data["context_windows"][ROUTE]["context_window_tokens"] = window
        data["input_caps"][ROUTE] = window - 32768 - 2048
        return data

    def wire(self, length):
        messages = [{"role":"system", "content":"Return JSON."}, {"role":"user", "content":"x"}]
        seat = {"endpoint":ROUTE, "thinking":"off", "reasoning_effort":"medium"}
        adapter = Adapter("offline")
        baseline = adapter.prepare(seat=seat, messages=messages, max_tokens=32768)
        messages[1]["content"] += "x" * (length - len(baseline["wire_body_text"].encode("utf-8")))
        wire = adapter.prepare(seat=seat, messages=messages, max_tokens=32768)["wire_body_text"]
        self.assertEqual(len(wire.encode("utf-8")), length)
        return messages, wire

    def check(self, length, data=None):
        messages, wire = self.wire(length)
        return token_preflight(messages, ROUTE, data or self.descriptor(), "offline", wire_body_text=wire)

    def test_sixty_thousand_bytes_pass_131072_documented_window(self):
        result = self.check(60000)
        self.assertEqual(result["wire_utf8_bytes"], 60000)
        self.assertEqual(result["input_cap_tokens"], 96256)
        self.assertEqual(result["counted_tokens"], 60000)
        self.assertEqual(result["limit"], 96256)
        self.assertEqual(result["prompt_tokens_upper_bound_including_reserve"], 62048)
        self.assertEqual(result["outcome"], "accepted")

    def test_above_window_fails_closed_without_truncation(self):
        with self.assertRaises(ReasonFailure) as caught:
            self.check(131073)
        self.assertEqual(caught.exception.code, "PROMPT_TOKEN_CAP")
        self.assertFalse(caught.exception.record["truncated"])
        self.assertEqual(caught.exception.record["outcome"], "stop_no_truncate")

    def test_reserve_applies_at_exact_boundary(self):
        self.assertEqual(self.check(96256)["outcome"], "accepted")
        with self.assertRaises(ReasonFailure) as caught:
            self.check(96257)
        self.assertEqual(caught.exception.record["template_overhead_tokens"], 2048)

    def test_cap_equation_and_reserve_cannot_be_relaxed(self):
        for key in ("reserve_tokens", "completion_ceiling_tokens"):
            data = self.descriptor(); data["context_windows"][ROUTE][key] -= 1
            with self.assertRaises(ReasonFailure): snapshot_tokenizers(data, "offline")
        data = self.descriptor(); data["input_caps"][ROUTE] += 1
        with self.assertRaises(ReasonFailure): snapshot_tokenizers(data, "offline")

    def test_all_documented_routes_and_kimi_are_admitted(self):
        data = snapshot_tokenizers(DESCRIPTOR, "offline")
        self.assertEqual(data["input_caps"], {"deepseek-flash":967232, ROUTE:221184,
            "ollama/glm-5.3.native":965184, "ollama/kimi-k3.native":965184})
        for route in data["endpoints"]:
            messages=[{"role":"system","content":"Return JSON."},{"role":"user","content":"Fixture."}]
            prepared=Adapter("offline").prepare(seat={"endpoint":route,"thinking":"off"},messages=messages,max_tokens=32768)
            self.assertEqual(token_preflight(messages,route,data,"offline",wire_body_text=prepared["wire_body_text"])["outcome"],"accepted")

    def test_legacy_descriptor_retains_placeholder_cap(self):
        path = launcher.ROOT / "experiments/diagnostics/R002-episodes-under-calibrated-difficulty/calibration/main-tokenizer-pins.json"
        with self.assertRaises(ReasonFailure) as caught:
            self.check(60000, json.loads(path.read_text(encoding="utf-8")))
        self.assertEqual(caught.exception.record["limit"], 32768)

class R3A1SelectionTests(unittest.TestCase):
    def setUp(self):
        fixture_root = Path(os.environ.get("TMP", "C:/tr30"))
        fixture_root.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="a1-", dir=fixture_root)
        self.root = Path(self.temp.name)
    def tearDown(self): self.temp.cleanup()

    def test_o002_loops_only_preserves_o001(self):
        series=self.root/"series"; old=series/"o001";old.mkdir(parents=True)
        marker=old/"marker.txt"
        with marker.open("w",encoding="utf-8",newline="") as f:f.write("immutable occurrence one\n")
        before=marker.read_bytes()
        directory=launcher.create(series,["O01","O02"],launcher.R3_A1_CONDITIONS,
            "Same occurrence question.","offline",amendment="R3-A1",expected_occurrence="o002")
        manifest=launcher.verify(directory)
        self.assertEqual(directory.name,"o002")
        self.assertEqual([(r["problem"],r["condition"]) for r in manifest["matrix"]],
            [(p,c) for p in ["O01","O02"] for c in launcher.R3_A1_CONDITIONS])
        self.assertTrue(all("-v2.json" in " ".join(r["argv"]) for r in manifest["matrix"]))
        self.assertEqual(marker.read_bytes(),before)
        self.assertEqual(launcher.read_json(directory/"inputs/tokenizer-pins.json")["amendment"],"R3-A1")

    def test_native_replay_and_wrong_occurrence_number_refused(self):
        with self.assertRaisesRegex(launcher.Refused,"REUSES_NATIVE"):
            launcher.create(self.root/"native",["O01"],["NATIVE"],"Fixture.","offline",amendment="R3-A1")
        with self.assertRaisesRegex(launcher.Refused,"OCCURRENCE_NUMBER_CHANGED"):
            launcher.create(self.root/"fresh",["O01"],launcher.R3_A1_CONDITIONS,"Fixture.","offline",
                amendment="R3-A1",expected_occurrence="o002")
        self.assertFalse((self.root/"fresh/o001").exists())

    def test_cli_defaults_select_only_amended_loops(self):
        with patch.object(launcher,"create",return_value=self.root/"o002") as create, patch.object(launcher,"execute",return_value={"failed":0}):
            self.assertEqual(launcher.main(["new","--series",str(self.root),"--problems","O01","O02","--question","Fixture.","--mode","offline"]),0)
        self.assertEqual(create.call_args.args[2],launcher.R3_A1_CONDITIONS)
        self.assertEqual(create.call_args.kwargs["amendment"],"R3-A1")

    def test_kimi_reader_lineage_is_refused_only_for_r3_a1(self):
        study = self.root / "study"
        problem = study / "problems/O01.txt"
        brief = study / "briefs/O01.md"
        problem.parent.mkdir(parents=True)
        brief.parent.mkdir(parents=True)
        with problem.open("w", encoding="utf-8", newline="") as handle:
            handle.write("Synthetic problem fixture.\n")
        with brief.open("w", encoding="utf-8", newline="") as handle:
            handle.write("Synthetic brief fixture.\n")
        manifest = study / "briefs/MANIFEST.json"
        data = {
            "schema": "minireason.r003.sealed-reader-briefs.v1",
            "status": "SEALED",
            "path_base": study.relative_to(self.root).as_posix(),
            "selected_problem_ids": ["O01"],
            "sealed_utc": "2026-09-17T00:00:00+00:00",
            "author": {"name": "Synthetic reader", "provider": "Ollama",
                       "model": "kimi-k3", "lineage": "Kimi"},
            "exposure": {"fully_blind": False, "declaration": "Synthetic fixture."},
            "briefs": [{
                "problem_id": "O01", "problem_path": "problems/O01.txt",
                "problem_sha256": hashlib.sha256(problem.read_bytes()).hexdigest(),
                "brief_path": "briefs/O01.md",
                "brief_sha256": hashlib.sha256(brief.read_bytes()).hexdigest(),
            }],
        }
        with manifest.open("w", encoding="utf-8", newline="") as handle:
            json.dump(data, handle, ensure_ascii=False, sort_keys=True)
            handle.write("\n")
        with patch.object(launcher, "STUDY", study), patch.object(launcher, "ROOT", self.root):
            self.assertEqual(
                launcher.validate_sealed_briefs(manifest, ["O01"])["records"][0]["lineage"],
                "Kimi",
            )
            with self.assertRaisesRegex(launcher.Refused, "LINEAGE_NOT_INDEPENDENT"):
                launcher.validate_sealed_briefs(manifest, ["O01"], "R3-A1")

    def test_verify_reuses_r3_a1_reader_lineages(self):
        directory = launcher.create(
            self.root / "verify-lineage", ["O01"], launcher.R3_A1_CONDITIONS,
            "Fixture.", "plan", amendment="R3-A1",
        )
        manifest_path = directory / "MANIFEST.json"
        manifest = launcher.read_json(manifest_path)
        seal = {
            "manifest_path": str(self.root / "synthetic-seal.json"),
            "records": [{"problem_id": "O01"}],
        }
        manifest["mode"] = "live"
        manifest["live_authorized"] = True
        manifest["sealed_briefs"] = seal
        with manifest_path.open("w", encoding="utf-8", newline="") as handle:
            json.dump(manifest, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        with (directory / "MANIFEST.sha256").open("w", encoding="utf-8", newline="") as handle:
            handle.write(launcher.digest(manifest_path) + "\n")
        with patch.object(launcher, "validate_sealed_briefs", return_value=seal) as validate:
            launcher.verify(directory)
        validate.assert_called_once_with(Path(seal["manifest_path"]), ["O01"], "R3-A1")
