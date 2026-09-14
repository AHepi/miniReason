#!/usr/bin/env python3
"""Tests for the commit/tree join checker.

Run from the sandbox root:
    python3 -m unittest check.test_commit_tree -v
"""

import re
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import commit_tree as ct

LOG_ROWS, LOG_BY_FULL = ct.load_log(ct.LOG)

GIT40 = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")


def tree_claim_paragraphs(text):
    """Whole paragraphs whose prose claims a git TREE identity, i.e. the
    paragraph carries one of the tree-claim phrases and at least one
    boundary-checked 40-hex token. Plain words like 'tree'/'trees' in
    non-identity senses (staging tree, publication tree, working tree) do
    not trigger this — the phrases below are the only tree-claim layouts the
    receipts use."""
    out = []
    for para in re.split(r"\n\s*\n", text):
        if ("Prior verified commit/tree:" in para or
                " TREE " in para or
                re.search(r"remote `[^`]*` at %s, tree " % ct.HEX40, para)):
            if GIT40.search(para):
                out.append(para)
    return out


class TestLogExtract(unittest.TestCase):
    """The frozen extract must be well-formed, since it is the reference."""

    def test_row_count(self):
        self.assertEqual(len(LOG_ROWS), 122)

    def test_columns_well_formed(self):
        for r in LOG_ROWS:
            self.assertRegex(r["full"], r"^[0-9a-f]{40}$")
            self.assertRegex(r["tree"], r"^[0-9a-f]{40}$")
            self.assertEqual(r["full"][:7], r["short"])
            self.assertIn("T", r["date"])

    def test_short_ids_unique(self):
        shorts = [r["short"] for r in LOG_ROWS]
        self.assertEqual(len(shorts), len(set(shorts)))


class TestExtraction(unittest.TestCase):
    """Pattern coverage over the two receipts."""

    @classmethod
    def setUpClass(cls):
        cls.texts = {}
        cls.paras = {}
        for receipt, p in ct.RECEIPTS:
            cls.texts[receipt], cls.paras[receipt] = ct.paragraphs(p)

    def test_paragraph_counts(self):
        self.assertEqual(len(self.paras["REC-20260914-U"]), 9)
        self.assertEqual(len(self.paras["REC-20260914-X"]), 9)

    def test_pair_layouts_cover_every_tree_claim(self):
        """Every paragraph that claims a tree identity must be fully covered
        by the pair patterns: all its git-shaped 40-hex tokens (boundary-
        checked, so SHA-256 digests never match) must be captured."""
        pair_res = [rx for name, rx, _l in ct.RULES
                    if name in ("PAIR_FULL", "PAIR_MARKED", "PAIR_PROSE")]
        for receipt, text in self.texts.items():
            for para in tree_claim_paragraphs(text):
                captured = set()
                for rx in pair_res:
                    for m in rx.finditer(para):
                        captured.add(m.group("c"))
                        captured.add(m.group("t"))
                claimed = set(GIT40.findall(para))
                self.assertEqual(claimed, captured,
                                 "uncovered tree-claim token in %s: %s"
                                 % (receipt, claimed - captured))

    def test_sha256_digests_never_extracted(self):
        """A 64-hex digest (plan_id, material, runner pins) contains 40-hex
        prefixes that must never be read as git ids anywhere in the
        receipts."""
        for p in self.paras["REC-20260914-U"] + self.paras["REC-20260914-X"]:
            for digest in re.findall(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])", p):
                for name, rx, _l in ct.RULES:
                    for m in rx.finditer(p):
                        c = m.groupdict().get("c") or ""
                        t = m.groupdict().get("t") or ""
                        self.assertFalse(digest.startswith(c) and len(c) == 40)
                        self.assertFalse(digest.startswith(t) and len(t) == 40)

    def test_no_zero_width_spaces(self):
        for text in self.texts.values():
            self.assertNotIn("​", text)

    def test_rules_have_expected_hit_counts(self):
        expected = {"PAIR_FULL": 3, "PAIR_MARKED": 3, "PAIR_PROSE": 2,
                    "PAIR_MARKED_C": 3, "PAIR_PROSE_C": 0, "PROSE_CTX": 3,
                    "FROM_RANGE": 2}
        counts = dict.fromkeys([n for n, _, _ in ct.RULES], 0)
        for receipt in self.texts:
            for para in self.paras[receipt]:
                for name, rx, _layout in ct.RULES:
                    n = len(rx.findall(para))
                    if name == "SINGLE_SHORT":
                        # admitted only in subject-mention prose
                        if not any(k in para for k in ct.SUBJECT_MENTION_MARKERS):
                            continue
                    counts[name] += n
        for name, want in expected.items():
            self.assertEqual(counts[name], want, name)
        # 18 raw 7-hex tokens in subject-mention prose: U-02's `ad3e347`
        # mention, X-09's fifteen enumerated labels, and the range-start
        # tokens `ad3e347` (U-08) / `96ca2eb` (X-08), which the checker
        # dedupes into the two FROM_RANGE rows -> 16 SINGLE_SHORT rows.
        self.assertEqual(counts["SINGLE_SHORT"], 18)


class TestJoin(unittest.TestCase):
    """Every claimed pair must verify; spot-check the key ones."""

    def test_all_six_plus_two_pairs(self):
        pairs = [
            ("f50db28cafd4f84683564aab7f5943393ed5e99c",
             "4e7c6622aa734d0ceebc523daaa1aa5bd842a893"),
            ("ad3e347b7c629414582a952c2bea8e4031bea702",
             "89c4f9142b3c9c7eef12e7a33b3e28adfe48efab"),
            ("d6b7e30fbb15d86834bef0e6f86ed9239a6768fc",
             "14b776dbe7b8d651f3d418a9546e83361cf1bffa"),
            ("8b25a306332cd0c560b53214d94550eddf673919",
             "fe03802edd79351f6cace4e1d3862cd4f10215b2"),
            ("96ca2eb3188beeb3ca1d399cddb203a9d38ec8a9",
             "da1d4bff5619b9a189575e11058c3b7a66d6be7b"),
            ("7bff688f89cbb7cdbb5a6f76c63fed6db8cb80e9",
             "9b354336e5cc54c20e63a0795f69de7914a42c85"),
            ("f25b4a93723c88a40ade062c065df20fd22490e9",
             "908d0f5ee884a989772eecd00cb68aaf44bb8a87"),
            ("958f2f4173da679283388c1820d218a209dffdbb",
             "79cbdfe9d1a03192d4bea8d84dc605d7862abdb8"),
        ]
        for commit, tree in pairs:
            row = LOG_BY_FULL.get(commit)
            self.assertIsNotNone(row, commit + " not in log")
            self.assertEqual(row["tree"], tree,
                             "MISMATCH_TREE for " + commit)

    def test_lone_commits_resolve(self):
        for commit in ("a1e516c54673c8a3ea2968ca3362ec6d1d725fb8",
                       "e9d9c47d96f45f8e9f356d7300ff7a8b4796b044",
                       "48ca127540a40dee7dee62b7d1f4a8386174d0ba",
                       "7b0303f182289142bc0d79794aa95a1823b12a10",
                       "e8357c3d236c4c837a27920c96ae8c7301c447c4",
                       "d6157cf39f07aa60abf209e32c46ae0d57535c7d"):
            self.assertIn(commit, LOG_BY_FULL)

    def test_short_ids_unique_resolution(self):
        for short in ("ad3e347", "96ca2eb", "7bff688", "9967e3c", "a1e516c",
                      "e9d9c47", "48ca127", "73d193f", "7b0303f", "e8357c3",
                      "d99ab67", "d6157cf", "63ae4b6", "ff29eca", "e1a6f1a",
                      "f25b4a9"):
            hits = ct.resolve_short(short, LOG_ROWS)
            self.assertEqual(len(hits), 1, short)

    def test_no_claimed_tree_on_wrong_commit(self):
        """A tree claimed in a receipt must not belong to any other log row's
        commit than the one claimed."""
        claimed = {
            "4e7c6622aa734d0ceebc523daaa1aa5bd842a893":
                "f50db28cafd4f84683564aab7f5943393ed5e99c",
            "89c4f9142b3c9c7eef12e7a33b3e28adfe48efab":
                "ad3e347b7c629414582a952c2bea8e4031bea702",
            "14b776dbe7b8d651f3d418a9546e83361cf1bffa":
                "d6b7e30fbb15d86834bef0e6f86ed9239a6768fc",
            "fe03802edd79351f6cace4e1d3862cd4f10215b2":
                "8b25a306332cd0c560b53214d94550eddf673919",
            "da1d4bff5619b9a189575e11058c3b7a66d6be7b":
                "96ca2eb3188beeb3ca1d399cddb203a9d38ec8a9",
            "9b354336e5cc54c20e63a0795f69de7914a42c85":
                "7bff688f89cbb7cdbb5a6f76c63fed6db8cb80e9",
            "908d0f5ee884a989772eecd00cb68aaf44bb8a87":
                "f25b4a93723c88a40ade062c065df20fd22490e9",
            "79cbdfe9d1a03192d4bea8d84dc605d7862abdb8":
                "958f2f4173da679283388c1820d218a209dffdbb",
        }
        for tree, commit in claimed.items():
            owners = [r["full"] for r in LOG_ROWS if r["tree"] == tree]
            self.assertEqual(owners, [commit])


class TestScriptEndToEnd(unittest.TestCase):
    def test_script_exits_zero_and_report_is_deterministic(self):
        first = ct.OUT.read_text(encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "check/commit_tree.py"],
            capture_output=True, text=True, cwd=Path(__file__).resolve().parent.parent)
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        self.assertIn("anomalies=0", proc.stdout)
        self.assertEqual(ct.OUT.read_text(encoding="utf-8"), first,
                         "report must be deterministic across runs")


if __name__ == "__main__":
    unittest.main()
