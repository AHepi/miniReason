"""R3-A3 occurrence-4 EC01 selection; offline fixtures only."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from minireason.reason import config, r002_preflight
from tests.reason.test_r003_launcher import launcher


class R3A3SelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        fixture_root = Path(os.environ.get("TMP", "C:/tw36"))
        fixture_root.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="a3-", dir=fixture_root)
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

    def test_o004_cross_only_preserves_o001_through_o003(self) -> None:
        series = self.root / "series"
        markers = [
            self._marker(series / occurrence, f"immutable {occurrence}\n")
            for occurrence in ("o001", "o002", "o003")
        ]
        before = {marker: marker.read_bytes() for marker in markers}

        directory = launcher.create(
            series, ["O01", "O02"], launcher.R3_A3_CONDITIONS,
            "Same occurrence question.", "offline", amendment="R3-A3",
            expected_occurrence="o004",
        )
        manifest = launcher.verify(directory)

        self.assertEqual(directory.name, "o004")
        self.assertEqual(
            [(row["problem"], row["condition"]) for row in manifest["matrix"]],
            [("O01", "LOOP-CROSS"), ("O02", "LOOP-CROSS")],
        )
        self.assertTrue(all("r003-cross-v4.json" in " ".join(row["argv"])
                            for row in manifest["matrix"]))
        amendment = launcher.read_json(directory / "inputs/amendment.json")
        self.assertEqual(amendment["amendment"], "R3-A3")
        self.assertEqual(amendment["route_intervention"], "EC01")
        self.assertEqual(amendment["branches"], ["RETURNED", "ARCHIVED"])
        self.assertIn("R3-A2 contracts", amendment["resource_inheritance"])
        descriptor = launcher.read_json(directory / "inputs/tokenizer-pins.json")
        self.assertEqual(descriptor["amendment"], "R3-A1")
        for marker, raw in before.items():
            self.assertEqual(marker.read_bytes(), raw)

    def test_native_decomposed_number_and_descriptor_refuse(self) -> None:
        for conditions in (["NATIVE"], ["LOOP-DECOMPOSED"]):
            with self.subTest(conditions=conditions), self.assertRaisesRegex(
                    launcher.Refused, "R3_A3_ONLY_LOOP_CROSS"):
                launcher.create(
                    self.root / ("refused-" + conditions[0]), ["O01"], conditions,
                    "Fixture.", "offline", amendment="R3-A3",
                    expected_occurrence="o004",
                )
        with self.assertRaisesRegex(
                launcher.Refused, "R3_A3_EXPECTED_OCCURRENCE_O004_REQUIRED"):
            launcher.create(
                self.root / "missing-number", ["O01"], launcher.R3_A3_CONDITIONS,
                "Fixture.", "offline", amendment="R3-A3",
            )

        series = self.root / "number"
        for occurrence in ("o001", "o002"):
            self._marker(series / occurrence, occurrence + "\n")
        with self.assertRaisesRegex(launcher.Refused, "OCCURRENCE_NUMBER_CHANGED"):
            launcher.create(
                series, ["O01"], launcher.R3_A3_CONDITIONS,
                "Fixture.", "offline", amendment="R3-A3",
                expected_occurrence="o004",
            )
        self.assertFalse((series / "o003").exists())

        wrong = self.root / "wrong-descriptor.json"
        data = launcher.read_json(launcher.DEFAULT_PREFLIGHT)
        data["amendment"] = "R3-A3"
        with wrong.open("w", encoding="utf-8", newline="") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        with self.assertRaisesRegex(
                launcher.Refused, "R3_A3_INHERITED_INPUT_DESCRIPTOR_REQUIRED"):
            launcher.create(
                self.root / "descriptor", ["O01"], launcher.R3_A3_CONDITIONS,
                "Fixture.", "offline", amendment="R3-A3",
                tokenizer_pins=wrong, expected_occurrence="o004",
            )

    def test_cli_explicit_a3_selects_cross_and_forwards_o004(self) -> None:
        with (patch.object(launcher, "create", return_value=self.root / "o004") as create,
              patch.object(launcher, "execute", return_value={"failed": 0})):
            code = launcher.main([
                "new", "--series", str(self.root), "--amendment", "R3-A3",
                "--expected-occurrence", "o004", "--question", "Fixture.",
                "--mode", "offline",
            ])
        self.assertEqual(code, 0)
        self.assertEqual(create.call_args.args[1], [f"O{number:02d}" for number in range(1, 9)])
        self.assertEqual(create.call_args.args[2], launcher.R3_A3_CONDITIONS)
        self.assertEqual(create.call_args.kwargs["amendment"], "R3-A3")
        self.assertEqual(create.call_args.kwargs["expected_occurrence"], "o004")

    def test_v4_inherits_a2_contract_and_envelopes_but_adds_ec01(self) -> None:
        recipes = launcher.STUDY / "recipes"
        prior = config.load_r003_recipe(recipes / "r003-cross-v3.json")["data"]
        current = config.load_r003_recipe(recipes / "r003-cross-v4.json")["data"]

        self.assertEqual(current["contract_version"], "r003-open-v1-r3-a2")
        for key in ("cycles", "stop", "closing_return", "attempt_policy", "seats"):
            self.assertEqual(current[key], prior[key])
        for key in ("off_completion_tokens", "native_completion_tokens", "prompt_tokens",
                    "wall_seconds", "critic_completion_tokens"):
            self.assertEqual(current["ceilings"][key], prior["ceilings"][key])
        self.assertEqual(current["ceilings"]["logical_calls"], 16)
        self.assertEqual(current["ceilings"]["attempts"], 32)
        self.assertEqual(current["ceilings"]["base_completion_tokens_total"], 458752)
        self.assertEqual(current["ceilings"]["completion_tokens_total"], 917504)
        self.assertEqual(current["route_intervention"], {
            "id": "EC01",
            "fork_after_cycle": 1,
            "branches": ["RETURNED", "ARCHIVED"],
            "order": ["RETURNED", "ARCHIVED"],
            "continuation_branch": "RETURNED",
            "archived_branch_end": "after_use",
            "archived_objection_delivery": "none",
        })

        capability = r002_preflight.r003_capability_snapshot()
        self.assertEqual(capability["r3_a3"]["contract"], "r003-open-v1-r3-a2")
        self.assertEqual(capability["r3_a3"]["route_intervention"],
                         current["route_intervention"])
        self.assertIn("r003_ec01.py", capability["runtime_sha256"])
        self.assertEqual(capability["recipe_sha256"]["r003-cross-v4.json"],
                         config.R003_RECIPE_SHA256["r003-cross-v4.json"])


if __name__ == "__main__":
    unittest.main()
