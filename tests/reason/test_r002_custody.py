"""Byte custody tests use copied files under the persistent test work directory."""
import copy
import hashlib
import json
from pathlib import Path
import unittest
import uuid
from tests.reason import artifact_root
from minireason.reason.config import R002_DIR
from minireason.reason.r002_custody import validate_coding
from minireason.reason.storage import read, write, get, put
from minireason.reason.types import ReasonFailure


def entry(data, problem_id="C01"):
    return next(row for row in data["candidates"] if row["candidate_id"] == problem_id)


class R002CustodyTests(unittest.TestCase):
    def setUp(self):
        self.directory = artifact_root() / "custody" / uuid.uuid4().hex[:8]
        self.directory.mkdir(parents=True)
        self.relations = get(R002_DIR / "problems/RELATIONS.json")
        self.forks = get(R002_DIR / "problems/FORKS.json")
        self.manifest = get(R002_DIR / "problems/RECODING_MAPS.json")

    def check(self, data=None, path=None, problem_id="C01"):
        return validate_coding(path or R002_DIR / "problems/RECODING_MAPS.json",
            data or self.manifest, problem_id, read(R002_DIR / f"problems/{problem_id}.txt"),
            entry(self.relations, problem_id), entry(self.forks, problem_id))

    def test_all_24_frozen_recodings_and_carriers_are_reversible(self):
        for number in range(1, 25):
            with self.subTest(candidate=number):
                self.assertEqual(len(self.check(problem_id=f"C{number:02d}")), 3)

    def test_wrong_paths_hashes_support_sets_and_inverse_are_refused(self):
        for mutation in ("path", "hash", "support", "inverse", "relations", "output"):
            data = copy.deepcopy(self.manifest); row = entry(data)
            if mutation == "path": row["problem_path"] = "../outside.txt"
            elif mutation == "hash": row["hashes"]["problem_sha256"] = "0" * 64
            elif mutation == "support": row["oracle_support_sha256"] = {}
            elif mutation == "inverse": row["inverse_order_map"] = list(row["forward_order_map"])
            elif mutation == "relations": row["relation_ids"] = []
            else: row["inverse_output_map"] = {"type": "trust-model"}
            with self.subTest(mutation=mutation), self.assertRaises(ReasonFailure):
                self.check(data)

    def test_carrier_change_refused_even_with_matching_new_file_hash(self):
        data = copy.deepcopy(self.manifest); row = entry(data)
        root = self.directory / "study"
        names = [row[key] for key in ("problem_path", "recoded_problem_path", "carrier_problem_path",
                                      "answer_path", "oracle_path")] + row["oracle_support_paths"]
        for name in names:
            write(root / name, read(R002_DIR / name))
        changed = read(root / row["carrier_problem_path"]) + "Changed premise.\n"
        write(root / row["carrier_problem_path"], changed, replace=True)
        row["hashes"]["carrier_problem_sha256"] = hashlib.sha256(changed.encode()).hexdigest()
        with self.assertRaises(ReasonFailure) as error:
            self.check(data, root / "problems/RECODING_MAPS.json")
        self.assertIn("Carrier changes", error.exception.detail)

    def create_native(self):
        from minireason.reason.engine import create_r002_native_run
        return create_r002_native_run(read(R002_DIR / "problems/C01.txt"), self.directory / "run",
            relation_registry=R002_DIR / "problems/RELATIONS.json", problem_id="C01")

    def test_saved_schema_prompt_or_config_change_prevents_dispatch(self):
        from minireason.reason.r002 import _validate_run
        run = self.create_native()
        _validate_run(run)
        for name in ("contracts/answer.schema.json", "prompt-contract.json", "config.json"):
            original = read(run / name)
            write(run / name, original + " ", replace=True)
            with self.subTest(name=name), self.assertRaises(ReasonFailure):
                _validate_run(run)
            write(run / name, original, replace=True)

    def test_native_ceiling_flag_cannot_be_silently_ignored(self):
        from minireason.reason.engine import create_r002_native_run
        with self.assertRaises(ReasonFailure):
            create_r002_native_run("fixture", self.directory / "bad", completion_tokens=8192,
                relation_registry=self.relations, problem_id="C01")
        self.assertFalse((self.directory / "bad").exists())

    def test_completed_resume_preserves_every_evidence_byte(self):
        from minireason.reason.engine import execute_r002
        run = self.create_native()
        first = execute_r002(run)
        hashes = lambda: {p.relative_to(run).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in run.rglob("*") if p.is_file()}
        before = hashes()
        self.assertEqual(execute_r002(run), first)
        self.assertEqual(hashes(), before)
