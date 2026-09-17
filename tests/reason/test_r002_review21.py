"""Boundary regression for the user-designated R002 review21 output root."""
from pathlib import Path
import os
import unittest
from minireason.reason import r002_launcher as launcher

class Review21RunRootTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "nt", "Windows-specific absolute review root")
    def test_designated_review_root_accepts_only_descendants(self):
        repo = Path(__file__).resolve().parents[2]
        self.assertEqual(launcher.validate_run_root(repo, Path("C:/tr21/main-proof")),
                         Path("C:/tr21/main-proof").resolve())
        for refused in ("C:/tr21", "C:/tr21/../escape", "C:/tr21-other/proof"):
            with self.subTest(path=refused), self.assertRaises(launcher.LauncherError):
                launcher.validate_run_root(repo, Path(refused))
        with self.assertRaisesRegex(launcher.LauncherError, "too long"):
            launcher.validate_run_root(repo, Path("C:/tr21/" + "x" * 120))

if __name__ == "__main__":
    unittest.main()
