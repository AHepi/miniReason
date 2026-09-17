"""Independent judge regressions; synthetic seals never open the study briefs."""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from minireason.reason import r002_launcher
from tests.reason import test_r003_occurrence as occ
from tests.reason import test_r003_engine as eng

launcher = occ.launcher

class R003JudgeRegressionTests(unittest.TestCase):
    def setUp(self):
        Path("C:/tr28").mkdir(exist_ok=True)
        self.base = Path(tempfile.mkdtemp(prefix="judge-", dir="C:/tr28"))

    def put(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")

    def test_authorized_judge_root_and_caller_tmp(self):
        self.assertEqual(launcher.allowed_write(self.base), self.base.resolve())
        self.assertEqual(r002_launcher.validate_run_root(occ.ROOT, self.base), self.base.resolve())
        with patch.dict(os.environ, {"TMP": "C:/tr28"}):
            self.assertEqual(launcher._subprocess_environment()["TMP"], "C:/tr28")
        with self.assertRaises(launcher.Refused):
            launcher.allowed_write(Path("C:/tr28-sibling/forbidden"))

    def test_capability_binds_launcher_and_provider_drift(self):
        from minireason.reason.r002_preflight import r003_capability_snapshot, validate_capability
        from minireason.reason.types import ReasonFailure
        snapshot = r003_capability_snapshot("Judge regression fixture")
        self.assertEqual(snapshot["launcher_sha256"], launcher.digest(launcher.STUDY / "run_R003.py"))
        self.assertIn("provider.py", snapshot["provider_sha256"])
        self.assertIn("provider_openai_compat.py", snapshot["provider_sha256"])
        for field in ("launcher_sha256", "provider_sha256"):
            altered = deepcopy(snapshot)
            altered[field] = "0" * 64 if field == "launcher_sha256" else {}
            with self.assertRaises(ReasonFailure) as caught:
                validate_capability(altered, "NATIVE", "live", "r003-open-v1")
            self.assertEqual(caught.exception.code, "CAPABILITY_REFUSED")

    def make_custodian_seal(self):
        study = self.base / "study"
        rows = []
        for number in (1, 2):
            pid = f"O{number:02d}"
            for rel, text in ((f"problems/{pid}.txt", "Synthetic prose problem."),
                              (f"briefs/{pid}.md", "Synthetic sealed fixture only.")):
                path = study / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("w", encoding="utf-8", newline="") as handle:
                    handle.write(text)
            rows.append({"problem_id": pid, "problem_path": f"problems/{pid}.txt",
                         "problem_sha256": launcher.digest(study / f"problems/{pid}.txt"),
                         "brief_path": f"briefs/{pid}.md",
                         "brief_sha256": launcher.digest(study / f"briefs/{pid}.md")})
        metadata = {"schema": "minireason.r003.sealed-reader-briefs.v1", "status": "SEALED",
                    "path_base": study.relative_to(self.base).as_posix(),
                    "selected_problem_ids": ["O01", "O02"],
                    "sealed_utc": "2026-09-17T00:00:00+00:00",
                    "author": {"name": "Synthetic reader", "provider": "OpenAI", "model": "fixture",
                               "lineage": "OpenAI/GPT", "distinct_from_participant_lineages": ["DeepSeek", "Qwen", "GLM"]},
                    "exposure": {"fully_blind": False, "declaration": "Fixture exposure disclosed."},
                    "custody": {"independent_custodian_agent": False},
                    "limitations": ["No independent custodian."], "briefs": rows}
        manifest = study / "briefs/MANIFEST.json"
        self.put(manifest, metadata)
        return study, manifest, metadata

    def test_existing_custodian_schema_is_adapted_without_rewriting(self):
        study, manifest, metadata = self.make_custodian_seal()
        original = manifest.read_bytes()
        with patch.object(launcher, "STUDY", study), patch.object(launcher, "ROOT", self.base):
            result = launcher.validate_sealed_briefs(manifest, ["O01", "O02"])
            self.assertEqual(result["records"][0]["author"], metadata["author"])
            self.assertEqual(result["records"][0]["exposure"], metadata["exposure"])
            self.assertEqual(result["custodian_metadata"]["limitations"], metadata["limitations"])
            self.assertEqual(manifest.read_bytes(), original)
            with (study / "briefs/O01.md").open("a", encoding="utf-8", newline="") as f:
                f.write("changed")
            with self.assertRaisesRegex(launcher.Refused, "HASH_MISMATCH"):
                launcher.validate_sealed_briefs(manifest, ["O01", "O02"])

    def test_custodian_seal_rejects_path_metadata_identity_and_future_timestamp(self):
        study, manifest, original = self.make_custodian_seal()
        mutations = [lambda v: v.update(path_base="wrong"),
                     lambda v: v["briefs"][0].update(brief_path="../outside.md"),
                     lambda v: v["author"].update(lineage="DeepSeek"),
                     lambda v: v.update(exposure={}),
                     lambda v: v.update(sealed_utc="2999-01-01T00:00:00Z"),
                     lambda v: v.update(selected_problem_ids=["O01"])]
        with patch.object(launcher, "STUDY", study), patch.object(launcher, "ROOT", self.base):
            for mutate in mutations:
                value = deepcopy(original)
                mutate(value)
                self.put(manifest, value)
                with self.assertRaises(launcher.Refused):
                    launcher.validate_sealed_briefs(manifest, ["O01", "O02"])

    def test_partial_closure_receives_latest_disputed_step_without_accepting_it(self):
        directory = launcher.create(self.base / "partial", ["O01"], ["LOOP-DECOMPOSED"],
                                    "Does the closing see the actual disputed current step?", "offline")
        normal = eng.BoundLocatorFixture(repair=False)
        marker = "A specific still-disputed returned step for the closure."
        def reply(**context):
            value = normal(**context)
            if context["role"] == "decomposed_return" and context["cycle"] == 2:
                value["derivation"] = marker
            if context["role"] == "decomposed_use" and context["cycle"] == 2:
                value["status"] = "disagrees"
            return value
        case = occ.R003OccurrenceIntegrationTests()
        self.assertEqual(case.execute_fixture(directory, reply)["failed"], 0)
        run = directory / "r/O01/d"
        request = occ.load(run / "calls/closing-return/a00/request.json")
        self.assertIn(marker, request["prepared"]["messages"][1]["content"])
        state = occ.load(run / "state.json")
        self.assertEqual(state["stop_reason"], "step_unresolved")
        self.assertEqual([row["step"] for row in state["accepted_steps"]], [1])

if __name__ == "__main__":
    unittest.main()
