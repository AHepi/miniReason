"""Security boundary tests for the restricted optional compiler route."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "check_lean_declarations", Path(__file__).with_name("check_lean_declarations.py"))
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class GuardTests(unittest.TestCase):
    def test_data_declarations_and_recursion_are_admitted(self):
        result = checker.guard("""inductive Evidence where
  | observed : String -> Evidence
  | combined : List Evidence -> Evidence
structure Claim where
  name : String
  evidence : Option Evidence
  assertion : Prop
""")
        self.assertEqual(result["declarations"], 2)

    def test_executable_and_external_syntax_is_refused_before_spawn(self):
        samples = [
            '#eval IO.println "secret"',
            'import Lean\nstructure S where\n  x : String',
            'run_cmd IO.println "secret"',
            'unsafe def leak := IO.FS.readFile "/tmp/secret"',
            'structure S where\n  x : IO Unit',
            'structure S where\n  x : String := "value"',
            'structure S where\n  x : (by exact String)',
            'structure S where\n  x : String\n#eval 1',
            'structure S where\n  x : String -- comment\n',
            'structure S where\n  x : Lean.Elab.Command.CommandElabM Unit',
            'structure S where\n  x : ℕ',
            'structure S where\n  x : String\nderiving Repr',
            'structure S where\n  x : (String',
            'structure S where\n  x : String)',
            'structure S where\n  x : -> String',
            'structure S where\n  x : String ->',
        ]
        with patch.object(checker.subprocess, "run") as run:
            for sample in samples:
                with self.subTest(sample=sample):
                    result = checker.check(sample, Path("/does/not/matter"), "test", "refusal test")
                    self.assertEqual(result["status"], "NOT_EXECUTED_OUTSIDE_SAFE_SUBSET")
            run.assert_not_called()

    def test_limits_and_unknown_type_names_are_refused(self):
        for source in ["structure S where\n  field : Unknown", "a" * 32769,
                       "structure String where\n  field : Nat"]:
            with self.assertRaises(checker.UnsafeOrUnsupported):
                checker.guard(source)


if __name__ == "__main__":
    unittest.main()
