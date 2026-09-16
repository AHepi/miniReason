"""Offline R001 launcher rerun and manifest-history integration test."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
import uuid


REPO = Path(__file__).resolve().parents[2]
FIXTURE = REPO / "work" / "w16" / ("lf-" + uuid.uuid4().hex[:8])
STUDY = Path("experiments/diagnostics/R001-reason-cli-vs-baselines")


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def copy_text(source: Path, target: Path) -> None:
    write_text(target, read_text(source))


def copy_text_tree(source: Path, target: Path) -> None:
    for path in sorted(source.rglob("*")):
        if path.is_file() and path.suffix in {".py", ".json"}:
            copy_text(path, target / path.relative_to(source))


def write_json(path: Path, value: dict) -> None:
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): digest(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class R001LauncherRerunTests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        (FIXTURE / STUDY / "problems").mkdir(parents=True)
        copy_text(REPO / STUDY / "run_R001.py", FIXTURE / STUDY / "run_R001.py")
        copy_text(REPO / "tools" / "reason.py", FIXTURE / "tools" / "reason.py")
        copy_text_tree(REPO / "src" / "minireason", FIXTURE / "src" / "minireason")
        copy_text(REPO / STUDY / "problems" / "P01.txt", FIXTURE / STUDY / "problems" / "P01.txt")
        source_paths = [
            "tools/reason.py",
            "src/minireason/provider_openai_compat.py",
            "src/minireason/data/endpoints.json",
        ]
        source_paths.extend(
            path.relative_to(FIXTURE).as_posix()
            for path in sorted((FIXTURE / "src" / "minireason" / "reason").rglob("*"))
            if path.is_file() and path.suffix in {".py", ".json"}
        )
        problem = FIXTURE / STUDY / "problems" / "P01.txt"
        pins = {
            "source_files": {
                relative: {
                    "sha256": digest(FIXTURE / relative),
                    "bytes": (FIXTURE / relative).stat().st_size,
                }
                for relative in source_paths
            },
            "sealed_task_files": {
                "problems/P01.txt": {
                    "sha256": digest(problem),
                    "bytes": problem.stat().st_size,
                }
            },
        }
        write_json(FIXTURE / STUDY / "SOURCE_PINS.json", pins)

    def invoke(self, *arguments: str, log_name: str) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(FIXTURE / STUDY / "run_R001.py"), *arguments]
        environment = os.environ.copy()
        environment.pop("DEEPSEEK_API_KEY", None)
        environment.pop("OLLAMA_API_KEY", None)
        environment.update({
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": os.pathsep.join(("src", "tests")),
            "TMP": r"C:\tw16",
        })
        completed = subprocess.run(
            command, cwd=FIXTURE, env=environment, capture_output=True, text=True,
            encoding="utf-8", errors="strict", check=False,
        )
        write_text(
            FIXTURE / log_name,
            "COMMAND " + subprocess.list2cmdline(command) + "\n"
            + "RETURN " + str(completed.returncode) + "\nSTDOUT\n" + completed.stdout
            + "\nSTDERR\n" + completed.stderr,
        )
        return completed

    def test_real_offline_run_failed_and_interrupted_reruns(self) -> None:
        control = FIXTURE / "control"
        first = self.invoke(
            "--mode", "offline", "--problems", "P01", "--run-root", str(control),
            log_name="launcher-offline-first.txt",
        )
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        manifest_path = control / "manifest.json"
        manifest = json.loads(read_text(manifest_path))
        self.assertEqual(manifest["schema"], "minireason.r001.launcher.v2")
        occurrence_root = FIXTURE / manifest["run_root"]
        cross = occurrence_root / "R001-P01-cross"
        single = occurrence_root / "R001-P01-single"
        self.assertTrue(cross.is_dir())
        self.assertTrue(single.is_dir())

        # Recreate the published v1 shape: attempts stay represented only by the
        # occurrence/condition records, and the original source snapshot is kept.
        manifest["schema"] = "minireason.r001.launcher.v1"
        manifest.pop("source_versions")
        manifest.pop("active_source_version")
        for occurrence in manifest["problems"]["P01"]["occurrences"].values():
            occurrence.pop("attempts")
            occurrence.pop("occurrence_id")
            occurrence.pop("source_version")
        for condition in manifest["problems"]["P01"]["conditions"].values():
            condition.pop("occurrence_id")
            condition.pop("source_version")
        write_json(manifest_path, manifest)

        failed_state = json.loads(read_text(cross / "state.json"))
        failed_state["stop_reason"] = "running"
        write_json(cross / "state.json", failed_state)
        engine_path = FIXTURE / "src" / "minireason" / "reason" / "engine.py"
        write_text(engine_path, read_text(engine_path) + "\n# fixture engineering source version\n")
        refused = self.invoke(
            "--mode", "offline", "--problems", "P01", "--run-root", str(control),
            log_name="launcher-offline-source-drift-refused.txt",
        )
        self.assertEqual(refused.returncode, 2)
        self.assertIn("use --rerun-failed", refused.stderr)
        self.assertTrue(cross.is_dir())

        failed_state["stop_reason"] = "SCHEMA_FAILURE"
        write_json(cross / "state.json", failed_state)
        recorded_manifest = json.loads(read_text(manifest_path))
        recorded_manifest["problems"]["P01"]["occurrences"]["cross"]["returncode"] = 2
        write_json(manifest_path, recorded_manifest)
        failed_hashes = tree_hashes(cross)
        interrupted_run_id = json.loads(read_text(single / "config.json"))["run_id"]
        intent = single / "calls" / "c9999-interrupted" / "a00" / "request.json"
        write_json(intent, {"intent": "fixture saved before delivery"})
        interrupted_hashes = tree_hashes(single)

        rerun = self.invoke(
            "--mode", "offline", "--problems", "P01", "--run-root", str(control),
            "--rerun-failed", log_name="launcher-offline-rerun-failed.txt",
        )
        self.assertEqual(rerun.returncode, 0, rerun.stdout + rerun.stderr)
        archived_cross = occurrence_root / "R001-P01-cross-failed-1"
        self.assertEqual(tree_hashes(archived_cross), failed_hashes)
        manifest = json.loads(read_text(manifest_path))
        self.assertEqual(manifest["active_source_version"], 2)
        self.assertEqual(len(manifest["source_versions"]), 2)
        self.assertIn(
            "experiments/diagnostics/R001-reason-cli-vs-baselines/run_R001.py",
            manifest["source_versions"][-1]["source_sha256"],
        )
        cross_record = manifest["problems"]["P01"]["occurrences"]["cross"]
        self.assertEqual(len(cross_record["attempts"]), 2)
        self.assertEqual(cross_record["attempts"][0]["status"], "archived-failed")
        self.assertEqual(cross_record["attempts"][0]["returncode"], 2)
        self.assertEqual(cross_record["attempts"][0]["source_version"], 1)
        self.assertEqual(cross_record["attempts"][1]["source_version"], 2)
        self.assertNotEqual(
            cross_record["attempts"][0]["occurrence_id"],
            cross_record["attempts"][1]["occurrence_id"],
        )
        alias = manifest["problems"]["P01"]["conditions"]["LOOP-CROSS"]
        self.assertEqual(alias["occurrence_id"], cross_record["occurrence_id"])
        single_record = manifest["problems"]["P01"]["occurrences"]["single"]
        archived_single = occurrence_root / "R001-P01-single-failed-1"
        self.assertEqual(tree_hashes(archived_single), interrupted_hashes)
        self.assertEqual(len(single_record["attempts"]), 2)
        self.assertEqual(single_record["attempts"][0]["stop_reason"], "INTERRUPTED_CALL")
        self.assertEqual(single_record["attempts"][0]["run_id"], interrupted_run_id)
        self.assertEqual(single_record["attempts"][0]["status"], "archived-failed")
        self.assertEqual(single_record["attempts"][0]["source_version"], 1)
        self.assertEqual(single_record["attempts"][1]["source_version"], 2)
        self.assertTrue((archived_single / intent.relative_to(single)).is_file())

        # Simulate process loss after the planned-archive receipt and rename but
        # before the manifest finalization. The targeted rerun reconciles it.
        current_cross_state = json.loads(read_text(cross / "state.json"))
        current_cross_state["stop_reason"] = "SCHEMA_FAILURE"
        write_json(cross / "state.json", current_cross_state)
        second_failed_hashes = tree_hashes(cross)
        archived_cross_2 = occurrence_root / "R001-P01-cross-failed-2"
        manifest = json.loads(read_text(manifest_path))
        cross_record = manifest["problems"]["P01"]["occurrences"]["cross"]
        cross_record["stop_reason"] = "SCHEMA_FAILURE"
        cross_record["attempts"][-1]["stop_reason"] = "SCHEMA_FAILURE"
        cross_record["pending_archive"] = {
            "directory": archived_cross_2.relative_to(FIXTURE).as_posix(),
            "fresh_source_version": manifest["active_source_version"],
        }
        write_json(manifest_path, manifest)
        cross.rename(archived_cross_2)
        write_text(engine_path, read_text(engine_path) + "\n# second fixture engineering source version\n")
        specific = self.invoke(
            "--mode", "offline", "--run-root", str(control), "--rerun", "P01:cross",
            log_name="launcher-offline-rerun-specific.txt",
        )
        self.assertEqual(specific.returncode, 0, specific.stdout + specific.stderr)
        self.assertEqual(tree_hashes(archived_cross_2), second_failed_hashes)
        manifest = json.loads(read_text(manifest_path))
        cross_record = manifest["problems"]["P01"]["occurrences"]["cross"]
        self.assertEqual(len(cross_record["attempts"]), 3)
        self.assertEqual(cross_record["attempts"][1]["stop_reason"], "SCHEMA_FAILURE")
        self.assertEqual(cross_record["attempts"][1]["status"], "archived-failed")
        self.assertEqual(cross_record["attempts"][2]["source_version"], 3)
        self.assertEqual(cross_record["attempts"][1]["source_version"], 2)



if __name__ == "__main__":
    unittest.main()
