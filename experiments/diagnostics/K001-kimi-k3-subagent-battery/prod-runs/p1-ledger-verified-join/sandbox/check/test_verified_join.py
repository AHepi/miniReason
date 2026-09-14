#!/usr/bin/env python3
"""Unit tests for check/verified_join.py join logic on synthetic fixtures,
plus a regression test of the real outputs against the real inputs."""

import json
import unittest

import verified_join as vj


def fake_log():
    recs = [
        {'line': 1, 'commit': 'a' * 40, 'tree': '1' * 40, 'short': 'aaaaaaa',
         'date': '2026-01-01', 'author': 'X', 'subject': 's1'},
        {'line': 2, 'commit': 'b' * 40, 'tree': '2' * 40, 'short': 'bbbbbbb',
         'date': '2026-01-02', 'author': 'X', 'subject': 's2'},
        {'line': 3, 'commit': 'c' * 40, 'tree': '3' * 40, 'short': 'bbbbbbb',  # collision
         'date': '2026-01-03', 'author': 'X', 'subject': 's3'},
    ]
    by_commit, by_short, by_tree = {}, {}, {}
    for r in recs:
        by_commit.setdefault(r['commit'], []).append(r)
        by_short.setdefault(r['short'], []).append(r)
        by_tree.setdefault(r['tree'], []).append(r)
    return by_commit, by_short, by_tree


class JoinTests(unittest.TestCase):
    def setUp(self):
        self.by_commit, self.by_short, self.by_tree = fake_log()

    def test_match(self):
        r = vj.join_pair('a' * 40, '1' * 40, self.by_commit, self.by_short)
        self.assertEqual(r['verdict'], 'MATCH')
        self.assertEqual(r['logged_tree'], '1' * 40)

    def test_tree_mismatch_prints_both(self):
        r = vj.join_pair('a' * 40, '9' * 40, self.by_commit, self.by_short)
        self.assertEqual(r['verdict'], 'TREE-MISMATCH')
        self.assertEqual(r['claimed_tree'], '9' * 40)
        self.assertEqual(r['logged_tree'], '1' * 40)

    def test_commit_absent(self):
        r = vj.join_pair('f' * 40, '1' * 40, self.by_commit, self.by_short)
        self.assertEqual(r['verdict'], 'COMMIT-ABSENT')
        self.assertNotIn('logged_tree', r)

    def test_short_ambiguous(self):
        r = vj.join_pair('bbbbbbb', '2' * 40, self.by_commit, self.by_short)
        self.assertEqual(r['verdict'], 'SHORT-AMBIGUOUS')
        self.assertEqual(len(r['candidates']), 2)

    def test_short_unambiguous_match(self):
        r = vj.join_pair('aaaaaaa', '1' * 40, self.by_commit, self.by_short)
        self.assertEqual(r['verdict'], 'MATCH')

    def test_classify_bare(self):
        self.assertEqual(vj.classify_bare('a' * 40, self.by_commit, self.by_tree)['class'],
                         'COMMIT')
        self.assertEqual(vj.classify_bare('1' * 40, self.by_commit, self.by_tree)['class'],
                         'TREE')
        self.assertEqual(vj.classify_bare('7' * 40, self.by_commit, self.by_tree)['class'],
                         'NEITHER')
        self.assertEqual(vj.classify_bare('aaaaaaa', self.by_commit, self.by_tree)['class'],
                         'UNRESOLVED-SHORT')


class RealOutputTests(unittest.TestCase):
    """Regress the produced deliverables against the real ledger and log."""

    @staticmethod
    def _ledger_text():
        with open(vj.LEDGER_PATH, encoding='utf-8') as fh:
            return fh.read()

    def test_patterns_cover_every_keyword_occurrence(self):
        text = self._ledger_text()
        pairs = vj.VERIFIED_PAIR_RE.findall(text)
        priors = vj.PRIOR_RE.findall(text)
        # 3 VERIFIED words legitimately carry no TREE (F002 record receipts);
        # everything else must be a pair.
        self.assertEqual(text.count('VERIFIED'), len(pairs) + 3)
        self.assertEqual(text.count('Prior verified commit/tree:'), len(priors))
        for bad in vj.CRED_RE.finditer(text):
            self.fail('credential-shaped line at %s:%d' %
                      (vj.LEDGER_PATH, text[:bad.start()].count('\n') + 1))

    def test_every_pair_matches_frozen_log(self):
        records, by_commit, by_short, by_tree, coll = vj.load_log()
        self.assertEqual(coll, {}, 'log extract must have no short-id collisions')
        text = self._ledger_text()
        for c, t in vj.VERIFIED_PAIR_RE.findall(text) + vj.PRIOR_RE.findall(text):
            self.assertIn(c, by_commit, c)
            self.assertEqual(by_commit[c][0]['tree'], t, c)

    def test_summary_consistent(self):
        with open(vj.JSON_OUT, encoding='utf-8') as fh:
            d = json.load(fh)
        self.assertTrue(d['summary']['every_verified_pair_verifies'])
        self.assertEqual(d['summary']['not_match'], [])
        self.assertEqual(d['summary']['verified_pair_verdict_counts'], {'MATCH': 79})
        self.assertEqual(d['summary']['prior_sentence_verdict_counts'], {'MATCH': 25})


if __name__ == '__main__':
    unittest.main()
