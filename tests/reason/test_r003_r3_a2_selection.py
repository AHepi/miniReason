"""R3-A2 occurrence-3 recipe and launcher selection; offline fixtures only."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from minireason.reason import config
from tests.reason.test_r003_launcher import launcher


class R3A2SelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        fixture_root = Path(os.environ.get("TMP", "C:/tw32"))
        fixture_root.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="a2-", dir=fixture_root)
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @staticmethod
    def _marker(directory: Path, text: str) -> Path:
        path = directory / "marker.txt"
        directory.mkdir(parents=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            handle.write(text)
        return path

    def test_o003_loops_only_preserves_o001_and_o002(self) -> None:
        series = self.root / "series"
        first = self._marker(series / "o001", "immutable occurrence one\n")
        second = self._marker(series / "o002", "immutable occurrence two\n")
        before = {first: first.read_bytes(), second: second.read_bytes()}

        directory = launcher.create(
            series, ["O01", "O02"], launcher.R3_A2_CONDITIONS,
            "Same occurrence question.", "offline", amendment="R3-A2",
            expected_occurrence="o003",
        )
        manifest = launcher.verify(directory)

        self.assertEqual(directory.name, "o003")
        self.assertEqual(
            [(row["problem"], row["condition"]) for row in manifest["matrix"]],
            [(problem, condition) for problem in ("O01", "O02")
             for condition in launcher.R3_A2_CONDITIONS],
        )
        self.assertTrue(all("-v3.json" in " ".join(row["argv"])
                            for row in manifest["matrix"]))
        amendment = launcher.read_json(directory / "inputs/amendment.json")
        self.assertEqual(amendment["amendment"], "R3-A2")
        self.assertIn("Exact R3-A1 input descriptor", amendment["resource_inheritance"])
        descriptor = launcher.read_json(directory / "inputs/tokenizer-pins.json")
        self.assertEqual(descriptor["amendment"], "R3-A1")
        for marker, raw in before.items():
            self.assertEqual(marker.read_bytes(), raw)

    def test_native_replay_wrong_number_and_noninherited_descriptor_refuse(self) -> None:
        with self.assertRaisesRegex(launcher.Refused, "R3_A2_REUSES_NATIVE"):
            launcher.create(
                self.root / "native", ["O01"], ["NATIVE"], "Fixture.", "offline",
                amendment="R3-A2",
            )
        series = self.root / "number"
        self._marker(series / "o001", "one\n")
        with self.assertRaisesRegex(launcher.Refused, "OCCURRENCE_NUMBER_CHANGED"):
            launcher.create(
                series, ["O01"], launcher.R3_A2_CONDITIONS, "Fixture.", "offline",
                amendment="R3-A2", expected_occurrence="o003",
            )
        self.assertFalse((series / "o002").exists())

        wrong = self.root / "wrong-descriptor.json"
        data = launcher.read_json(launcher.DEFAULT_PREFLIGHT)
        data["amendment"] = "R3-A2"
        with wrong.open("w", encoding="utf-8", newline="") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        with self.assertRaisesRegex(launcher.Refused, "R3_A2_INHERITED_INPUT_DESCRIPTOR_REQUIRED"):
            launcher.create(
                self.root / "descriptor", ["O01"], launcher.R3_A2_CONDITIONS,
                "Fixture.", "offline", amendment="R3-A2", tokenizer_pins=wrong,
            )

    def test_cli_explicit_a2_selects_only_amended_loops(self) -> None:
        with (patch.object(launcher, "create", return_value=self.root / "o003") as create,
              patch.object(launcher, "execute", return_value={"failed": 0})):
            code = launcher.main([
                "new", "--series", str(self.root), "--problems", "O01", "O02",
                "--amendment", "R3-A2", "--question", "Fixture.", "--mode", "offline",
            ])
        self.assertEqual(code, 0)
        self.assertEqual(create.call_args.args[2], launcher.R3_A2_CONDITIONS)
        self.assertEqual(create.call_args.kwargs["amendment"], "R3-A2")

    def test_versioned_recipes_bind_a2_contract_without_resource_drift(self) -> None:
        recipes = launcher.STUDY / "recipes"
        cross = config.load_r003_recipe(recipes / "r003-cross-v3.json")["data"]
        decomposed = config.load_r003_recipe(recipes / "r003-decomposed-v3.json")["data"]
        self.assertEqual(cross["contract_version"], "r003-open-v1-r3-a2")
        self.assertEqual(decomposed["contract_version"], "r003-open-v1-r3-a2")
        self.assertEqual(
            cross["ceilings"],
            config.load_r003_recipe(recipes / "r003-cross-v2.json")["data"]["ceilings"],
        )
        self.assertEqual(
            decomposed["ceilings"],
            config.load_r003_recipe(recipes / "r003-decomposed-v2.json")["data"]["ceilings"],
        )
        self.assertEqual(cross["seats"]["signal_b"]["endpoint"], "ollama/kimi-k3.native")
        self.assertEqual(decomposed["seats"]["critic_cycle_1"]["endpoint"],
                         "ollama/qwen3.5-397b.native")


if __name__ == "__main__":
    unittest.main()
