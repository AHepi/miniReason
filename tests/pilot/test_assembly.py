import unittest
from minireason.pilot.assemble import assemble

class AssemblyTests(unittest.TestCase):
    def result(self, ref="c1", status="accepted", unresolved=None):
        return {"result_ref": ref, "status": status, "output": {"status": "complete", "answer": "result", "unresolved": unresolved or []}}

    def test_single_and_hash_binding(self):
        result = assemble([self.result()])
        self.assertEqual(result["answer"], "result")
        self.assertEqual(result["status"], "complete")
        self.assertIn("c1", result["dependencies"])

    def test_unknown_duplicate_unaccepted(self):
        for refs in [["absent"], ["c1", "c1"]]:
            with self.assertRaises(ValueError): assemble([self.result()], result_refs=refs)
        with self.assertRaises(ValueError): assemble([self.result(status="unaccepted")])

    def test_missing_dependency_and_unresolved_are_partial(self):
        result = assemble([self.result(), self.result("c2")], result_refs=["c1"], answer="result")
        self.assertEqual(result["status"], "partial")
        self.assertIn("Omitted dependency: c2", result["unresolved"])
        self.assertEqual(assemble([self.result(unresolved=["missing proof"])])["status"], "partial")

    def test_multiple_results_require_synthesis(self):
        with self.assertRaises(ValueError): assemble([self.result(), self.result("c2")])
