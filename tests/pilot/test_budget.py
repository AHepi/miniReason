from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path
import tempfile
import unittest

from minireason.pilot.budget import Budget, estimate_spend, load_price_table


def receipt(
    *,
    name="deepseek-flash",
    model="deepseek-flash",
    usage=None,
    status="accepted",
    call_id="c0001",
    attempt=0,
):
    return {
        "call_id": call_id,
        "attempt": attempt,
        "status": status,
        "endpoint": {
            "name": name,
            "model": model,
            "family": "test-family",
            "lineage": "test-lineage",
        },
        "usage": usage if usage is not None else {},
    }


class BudgetTests(unittest.TestCase):
    def test_default_table_is_strict_and_has_official_sources(self):
        table = load_price_table()
        self.assertEqual(table.currency, "USD")
        self.assertEqual(table.date_read, "2026-09-17")
        self.assertEqual(len(table.sha256), 64)
        self.assertEqual(
            {provider for provider, _url, _date in table.sources},
            {"DeepSeek", "Ollama"},
        )
        self.assertEqual(
            table.resolve({"name": "ollama/kimi-k3.native", "model": "kimi-k3"}).output_per_million,
            Decimal("15.00"),
        )
        self.assertEqual(table.to_dict()["schema_version"], table.schema_version)
        self.assertEqual(table.to_dict()["routes"][0]["input_usd_per_million"], "0.30")

    def test_reasoning_is_reported_but_completion_is_charged_once(self):
        usage = {
            "prompt_tokens": 1000,
            "completion_tokens": 200,
            "total_tokens": 1200,
            "prompt_cache_hit_tokens": 400,
            "prompt_cache_miss_tokens": 600,
            "completion_tokens_details": {"reasoning_tokens": 150},
        }
        snapshot = Budget().snapshot([receipt(usage=usage)])
        # 600*0.30 + 400*0.006 + 200*1.20, all per million.
        self.assertEqual(snapshot.estimated_usd, Decimal("0.0004224"))
        self.assertEqual(snapshot.usage["completion_tokens"], 200)
        self.assertEqual(snapshot.usage["reasoning_tokens"], 150)
        self.assertTrue(snapshot.dispatch_allowed)

    def test_missing_usage_on_priced_dispatch_stops_as_unknown(self):
        snapshot = Budget().snapshot([receipt(usage={})])
        self.assertEqual(snapshot.stop_reason, "SPEND_UNKNOWN")
        self.assertFalse(snapshot.dispatch_allowed)
        self.assertIsNone(snapshot.estimated_usd)
        self.assertIsNone(snapshot.remaining_usd)
        self.assertEqual(snapshot.missing_usage_receipts, ("c0001/a00",))

    def test_not_dispatched_receipt_does_not_create_zero_usage(self):
        snapshot = Budget().snapshot([receipt(status="not_dispatched", usage={})])
        self.assertTrue(snapshot.dispatch_allowed)
        self.assertEqual(snapshot.estimated_usd, Decimal(0))
        self.assertEqual(snapshot.receipts[0]["cost_status"], "not_dispatched")

    def test_unknown_route_is_token_only_and_visible(self):
        usage = {"prompt_tokens": 11, "completion_tokens": 7}
        snapshot = Budget().snapshot([
            receipt(name="ollama/future-model", model="future-model", usage=usage)
        ])
        self.assertTrue(snapshot.dispatch_allowed)
        self.assertIsNone(snapshot.estimated_usd)
        self.assertEqual(snapshot.known_estimated_usd, Decimal(0))
        self.assertEqual(snapshot.usage["total_tokens"], 18)
        self.assertEqual(snapshot.unknown_price_routes, ("ollama/future-model",))

    def test_ceiling_equality_stops_and_snapshot_serializes(self):
        usage = {"prompt_tokens": 0, "completion_tokens": 1_000_000}
        snapshot = estimate_spend([receipt(usage=usage)], max_spend_usd="1.20")
        self.assertEqual(snapshot.stop_reason, "SPEND_CEILING")
        self.assertTrue(snapshot.ceiling_reached)
        self.assertFalse(snapshot.dispatch_allowed)
        self.assertEqual(snapshot.remaining_usd, Decimal(0))
        encoded = json.dumps(snapshot.to_dict())
        self.assertIn("Estimate from published prices", encoded)

    def test_sliced_receipts_give_per_pass_and_cumulative_snapshots(self):
        receipts = [
            receipt(usage={"prompt_tokens": 100, "completion_tokens": 10}, call_id="c0001"),
            receipt(usage={"prompt_tokens": 200, "completion_tokens": 20}, call_id="c0002"),
        ]
        budget = Budget()
        first = budget.snapshot(receipts[:1])
        second = budget.snapshot(receipts[1:])
        cumulative = budget.snapshot(receipts)
        self.assertEqual(
            cumulative.known_estimated_usd,
            first.known_estimated_usd + second.known_estimated_usd,
        )
        self.assertEqual(cumulative.usage["total_tokens"], 330)

    def test_cached_price_falls_back_to_input_when_unpublished(self):
        usage = {
            "prompt_tokens": 100,
            "completion_tokens": 0,
            "prompt_tokens_details": {"cached_tokens": 100},
        }
        snapshot = Budget().snapshot([
            receipt(name="ollama/qwen3.5-397b.native", model="qwen3.5:397b", usage=usage)
        ])
        self.assertEqual(snapshot.estimated_usd, Decimal("0.000060"))

    def test_malformed_usage_is_not_silently_counted(self):
        malformed = {"prompt_tokens": 10, "completion_tokens": 4,
                     "completion_tokens_details": {"reasoning_tokens": 5}}
        snapshot = Budget().snapshot([receipt(usage=malformed)])
        self.assertEqual(snapshot.stop_reason, "SPEND_UNKNOWN")
        self.assertEqual(snapshot.usage["total_tokens"], 0)

    def test_limit_must_be_positive(self):
        for value in (0, "0", -1, True, "NaN", "Infinity"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    Budget(max_spend_usd=value)

    def test_table_rejects_duplicate_aliases(self):
        source = Path("research/deepseek-flash-pilot/PRICES.json")
        data = json.loads(source.read_text(encoding="utf-8"))
        data["routes"][1]["endpoint_names"].append("deepseek-flash")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "prices.json"
            path.write_text(json.dumps(data), encoding="utf-8", newline="")
            with self.assertRaisesRegex(ValueError, "overlap"):
                load_price_table(path)


if __name__ == "__main__":
    unittest.main()
