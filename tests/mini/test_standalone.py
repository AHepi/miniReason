"""Extraction gates: runtime data travels with the package and imports stay closed."""
from __future__ import annotations

import importlib
import subprocess
import sys
import unittest
from pathlib import Path

from creib.forge.mini.common import MINI_POLICY_DIR, MINI_SCHEMA_DIR
from creib.forge.mini.openkernels import OPEN_MODULES, OPEN_PACKAGE


class StandaloneExtractionTests(unittest.TestCase):
    def test_runtime_data_is_owned_by_the_package(self) -> None:
        package = Path(importlib.import_module("creib.forge.mini").__file__).parent
        self.assertEqual(MINI_SCHEMA_DIR.parent, package / "data")
        self.assertTrue((MINI_SCHEMA_DIR / "mini-manifest.schema.json").is_file())
        self.assertTrue((MINI_POLICY_DIR / "mini.policy.default.v1.json").is_file())

    def test_every_advertised_open_module_is_shipped(self) -> None:
        for name in OPEN_MODULES:
            with self.subTest(module=name):
                self.assertIsNotNone(importlib.import_module(OPEN_PACKAGE + name))

    def test_core_import_does_not_load_the_outer_runner(self) -> None:
        probe = "import sys; import creib.forge.mini.runner; raise SystemExit('creib.forge.conformance.runner' in sys.modules)"
        completed = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
