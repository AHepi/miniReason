"""Published-price spend estimates for one sealed pilot task.

Reasoning tokens are reported separately but are a subset of completion
tokens, so they are never charged a second time.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


DEFAULT_PRICE_PATH = (
    Path(__file__).resolve().parents[3]
    / "research"
    / "deepseek-flash-pilot"
    / "PRICES.json"
)
_MILLION = Decimal(1_000_000)


def _decimal(value: Any, field: str, *, allow_none: bool = False) -> Decimal | None:
    if value is None and allow_none:
        return None
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError(f"{field} must be a nonnegative decimal string")
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError) as error:
        raise ValueError(f"{field} must be a nonnegative decimal string") from error
    if not parsed.is_finite() or parsed < 0:
        raise ValueError(f"{field} must be a nonnegative finite decimal")
    return parsed


def _positive_limit(value: Any) -> Decimal:
    parsed = _decimal(value, "max_spend_usd")
    assert parsed is not None
    if parsed <= 0:
        raise ValueError("max_spend_usd must be positive")
    return parsed


def _money(value: Decimal | None) -> str | None:
    return None if value is None else format(value, "f")


def _string_set(value: Any, field: str) -> frozenset[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"{field} must be a list of nonempty strings")
    return frozenset(value)


@dataclass(frozen=True)
class RoutePrice:
    route_id: str
    provider: str
    endpoint_names: frozenset[str]
    models: frozenset[str]
    input_per_million: Decimal
    cached_input_per_million: Decimal | None
    output_per_million: Decimal
    rate_basis: str

    def matches(self, endpoint: Mapping[str, Any]) -> bool:
        return endpoint.get("name") in self.endpoint_names or endpoint.get("model") in self.models


@dataclass(frozen=True)
class PriceTable:
    path: str
    sha256: str
    schema_version: str
    currency: str
    unit_tokens: int
    date_read: str
    estimate_policy: str
    sources: tuple[tuple[str, str, str], ...]
    routes: tuple[RoutePrice, ...]

    def resolve(self, endpoint: Mapping[str, Any]) -> RoutePrice | None:
        matches = [route for route in self.routes if route.matches(endpoint)]
        if len(matches) > 1:
            raise ValueError("endpoint metadata matches multiple price routes")
        return matches[0] if matches else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "currency": self.currency,
            "unit_tokens": self.unit_tokens,
            "date_read": self.date_read,
            "estimate_policy": self.estimate_policy,
            "sources": [
                {"provider": provider, "url": url, "date_read": date_read}
                for provider, url, date_read in self.sources
            ],
            "routes": [
                {
                    "id": route.route_id,
                    "provider": route.provider,
                    "endpoint_names": sorted(route.endpoint_names),
                    "models": sorted(route.models),
                    "input_usd_per_million": _money(route.input_per_million),
                    "cached_input_usd_per_million": _money(route.cached_input_per_million),
                    "output_usd_per_million": _money(route.output_per_million),
                    "rate_basis": route.rate_basis,
                }
                for route in self.routes
            ],
        }


@dataclass(frozen=True)
class BudgetSnapshot:
    max_spend_usd: Decimal
    estimated_usd: Decimal | None
    known_estimated_usd: Decimal
    remaining_usd: Decimal | None
    ceiling_reached: bool
    dispatch_allowed: bool
    stop_reason: str | None
    usage: Mapping[str, int]
    unknown_price_routes: tuple[str, ...]
    missing_usage_receipts: tuple[str, ...]
    receipts: tuple[Mapping[str, Any], ...]
    price_table_sha256: str
    price_date_read: str
    estimate_policy: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "minireason.pilot.budget-snapshot.v1",
            "max_spend_usd": _money(self.max_spend_usd),
            "estimated_usd": _money(self.estimated_usd),
            "known_estimated_usd": _money(self.known_estimated_usd),
            "remaining_usd": _money(self.remaining_usd),
            "ceiling_reached": self.ceiling_reached,
            "dispatch_allowed": self.dispatch_allowed,
            "stop_reason": self.stop_reason,
            "usage": dict(self.usage),
            "unknown_price_routes": list(self.unknown_price_routes),
            "missing_usage_receipts": list(self.missing_usage_receipts),
            "receipts": [dict(item) for item in self.receipts],
            "price_table_sha256": self.price_table_sha256,
            "price_date_read": self.price_date_read,
            "estimate_policy": self.estimate_policy,
            "label": "Estimate from published prices; not a bill.",
        }


def load_price_table(path: Path | str = DEFAULT_PRICE_PATH) -> PriceTable:
    source = Path(path)
    raw = source.read_bytes()
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("price table must be UTF-8 JSON") from error
    required = {
        "schema_version", "currency", "unit_tokens", "date_read",
        "estimate_policy", "sources", "routes",
    }
    if not isinstance(data, dict) or set(data) != required:
        raise ValueError("price table has unknown or missing top-level fields")
    if data["schema_version"] != "minireason.pilot.prices.v1":
        raise ValueError("unsupported price table schema")
    if data["currency"] != "USD" or data["unit_tokens"] != 1_000_000:
        raise ValueError("price table must use USD per one million tokens")
    if not isinstance(data["date_read"], str) or not data["date_read"]:
        raise ValueError("price table date_read is required")
    if not isinstance(data["estimate_policy"], str) or not data["estimate_policy"]:
        raise ValueError("price table estimate_policy is required")
    if not isinstance(data["sources"], list) or not data["sources"]:
        raise ValueError("price table sources are required")
    sources: list[tuple[str, str, str]] = []
    for index, item in enumerate(data["sources"]):
        if not isinstance(item, dict) or set(item) != {"provider", "url", "date_read"}:
            raise ValueError(f"source {index} has invalid fields")
        if any(not isinstance(item[key], str) or not item[key] for key in item):
            raise ValueError(f"source {index} values must be nonempty strings")
        if not item["url"].startswith("https://"):
            raise ValueError(f"source {index} URL must use HTTPS")
        sources.append((item["provider"], item["url"], item["date_read"]))
    if not isinstance(data["routes"], list) or not data["routes"]:
        raise ValueError("price table routes are required")
    route_fields = {
        "id", "provider", "endpoint_names", "models",
        "input_usd_per_million", "cached_input_usd_per_million",
        "output_usd_per_million", "rate_basis",
    }
    routes: list[RoutePrice] = []
    ids: set[str] = set()
    endpoint_names: set[str] = set()
    models: set[str] = set()
    for index, item in enumerate(data["routes"]):
        if not isinstance(item, dict) or set(item) != route_fields:
            raise ValueError(f"route {index} has invalid fields")
        route_id = item["id"]
        if not isinstance(route_id, str) or not route_id or route_id in ids:
            raise ValueError(f"route {index} id is missing or duplicated")
        ids.add(route_id)
        names = _string_set(item["endpoint_names"], f"route {route_id} endpoint_names")
        route_models = _string_set(item["models"], f"route {route_id} models")
        if endpoint_names.intersection(names) or models.intersection(route_models):
            raise ValueError(f"route {route_id} aliases overlap another route")
        endpoint_names.update(names)
        models.update(route_models)
        if not isinstance(item["provider"], str) or not item["provider"]:
            raise ValueError(f"route {route_id} provider is required")
        if not isinstance(item["rate_basis"], str) or not item["rate_basis"]:
            raise ValueError(f"route {route_id} rate_basis is required")
        routes.append(RoutePrice(
            route_id=route_id,
            provider=item["provider"],
            endpoint_names=names,
            models=route_models,
            input_per_million=_decimal(item["input_usd_per_million"], "input price"),
            cached_input_per_million=_decimal(
                item["cached_input_usd_per_million"], "cached input price", allow_none=True
            ),
            output_per_million=_decimal(item["output_usd_per_million"], "output price"),
            rate_basis=item["rate_basis"],
        ))
    return PriceTable(
        path=str(source),
        sha256=hashlib.sha256(raw).hexdigest(),
        schema_version=data["schema_version"],
        currency=data["currency"],
        unit_tokens=data["unit_tokens"],
        date_read=data["date_read"],
        estimate_policy=data["estimate_policy"],
        sources=tuple(sources),
        routes=tuple(routes),
    )


def _token(value: Any) -> int | None:
    return value if type(value) is int and value >= 0 else None


def _receipt_id(receipt: Mapping[str, Any], index: int) -> str:
    call_id = receipt.get("call_id")
    attempt = receipt.get("attempt")
    if isinstance(call_id, str) and type(attempt) is int:
        return f"{call_id}/a{attempt:02d}"
    return f"receipt-{index + 1}"


def _usage(usage: Any) -> dict[str, int] | None:
    if not isinstance(usage, Mapping):
        return None
    prompt = _token(usage.get("prompt_tokens"))
    completion = _token(usage.get("completion_tokens"))
    if prompt is None or completion is None:
        return None
    details = usage.get("completion_tokens_details", {})
    reasoning_raw = usage.get("reasoning_tokens")
    if reasoning_raw is None and isinstance(details, Mapping):
        reasoning_raw = details.get("reasoning_tokens")
    reasoning = 0 if reasoning_raw is None else _token(reasoning_raw)
    if reasoning is None or reasoning > completion:
        return None
    hit_raw = usage.get("prompt_cache_hit_tokens")
    miss_raw = usage.get("prompt_cache_miss_tokens")
    prompt_details = usage.get("prompt_tokens_details", {})
    if hit_raw is None and isinstance(prompt_details, Mapping):
        hit_raw = prompt_details.get("cached_tokens")
    hit = None if hit_raw is None else _token(hit_raw)
    miss = None if miss_raw is None else _token(miss_raw)
    if (hit_raw is not None and hit is None) or (miss_raw is not None and miss is None):
        return None
    if hit is None and miss is None:
        hit, miss = 0, prompt
    elif hit is None:
        assert miss is not None
        if miss > prompt:
            return None
        hit = prompt - miss
    elif miss is None:
        if hit > prompt:
            return None
        miss = prompt - hit
    elif hit + miss != prompt:
        return None
    return {
        "prompt_tokens": prompt,
        "cached_prompt_tokens": hit,
        "uncached_prompt_tokens": miss,
        "completion_tokens": completion,
        "reasoning_tokens": reasoning,
        "total_tokens": prompt + completion,
    }


class Budget:
    def __init__(self, max_spend_usd: Any = "6.00", prices: PriceTable | None = None) -> None:
        self.max_spend_usd = _positive_limit(max_spend_usd)
        self.prices = prices or load_price_table()

    def snapshot(self, receipts: Sequence[Mapping[str, Any]]) -> BudgetSnapshot:
        if not isinstance(receipts, Sequence) or isinstance(receipts, (str, bytes, bytearray)):
            raise ValueError("receipts must be a sequence of mappings")
        totals = {
            "prompt_tokens": 0,
            "cached_prompt_tokens": 0,
            "uncached_prompt_tokens": 0,
            "completion_tokens": 0,
            "reasoning_tokens": 0,
            "total_tokens": 0,
        }
        known_cost = Decimal(0)
        unknown_routes: set[str] = set()
        missing_usage: list[str] = []
        breakdown: list[dict[str, Any]] = []
        for index, receipt in enumerate(receipts):
            if not isinstance(receipt, Mapping):
                raise ValueError(f"receipt {index + 1} must be a mapping")
            receipt_id = _receipt_id(receipt, index)
            status = receipt.get("status")
            endpoint = receipt.get("endpoint")
            endpoint = endpoint if isinstance(endpoint, Mapping) else {}
            route = self.prices.resolve(endpoint)
            item: dict[str, Any] = {
                "receipt": receipt_id,
                "status": status,
                "endpoint": {key: endpoint.get(key) for key in ("name", "model", "family", "lineage")},
                "price_route": route.route_id if route else None,
                "estimated_usd": None,
            }
            if status == "not_dispatched":
                item["cost_status"] = "not_dispatched"
                item["usage"] = None
                breakdown.append(item)
                continue
            parsed = _usage(receipt.get("usage"))
            if parsed is None:
                item["cost_status"] = "missing_usage"
                item["usage"] = None
                missing_usage.append(receipt_id)
                breakdown.append(item)
                continue
            item["usage"] = dict(parsed)
            for key in totals:
                totals[key] += parsed[key]
            if route is None:
                identity = str(endpoint.get("name") or endpoint.get("model") or "unknown-route")
                unknown_routes.add(identity)
                item["cost_status"] = "unknown_price"
                breakdown.append(item)
                continue
            cached_rate = route.cached_input_per_million
            if cached_rate is None:
                cached_rate = route.input_per_million
            cost = (
                Decimal(parsed["uncached_prompt_tokens"]) * route.input_per_million
                + Decimal(parsed["cached_prompt_tokens"]) * cached_rate
                + Decimal(parsed["completion_tokens"]) * route.output_per_million
            ) / _MILLION
            known_cost += cost
            item["cost_status"] = "estimated"
            item["estimated_usd"] = _money(cost)
            breakdown.append(item)
        priced_missing = any(item["cost_status"] == "missing_usage" and item["price_route"] for item in breakdown)
        cost_complete = not unknown_routes and not missing_usage
        estimated = known_cost if cost_complete else None
        ceiling_reached = known_cost >= self.max_spend_usd
        if priced_missing:
            stop_reason = "SPEND_UNKNOWN"
        elif ceiling_reached:
            stop_reason = "SPEND_CEILING"
        else:
            stop_reason = None
        remaining = max(Decimal(0), self.max_spend_usd - known_cost)
        return BudgetSnapshot(
            max_spend_usd=self.max_spend_usd,
            estimated_usd=estimated,
            known_estimated_usd=known_cost,
            remaining_usd=remaining if not priced_missing else None,
            ceiling_reached=ceiling_reached,
            dispatch_allowed=stop_reason is None,
            stop_reason=stop_reason,
            usage=totals,
            unknown_price_routes=tuple(sorted(unknown_routes)),
            missing_usage_receipts=tuple(missing_usage),
            receipts=tuple(breakdown),
            price_table_sha256=self.prices.sha256,
            price_date_read=self.prices.date_read,
            estimate_policy=self.prices.estimate_policy,
        )


def estimate_spend(
    receipts: Sequence[Mapping[str, Any]],
    prices: PriceTable | None = None,
    *,
    max_spend_usd: Any = "6.00",
) -> BudgetSnapshot:
    return Budget(max_spend_usd=max_spend_usd, prices=prices).snapshot(receipts)


__all__ = [
    "Budget",
    "BudgetSnapshot",
    "DEFAULT_PRICE_PATH",
    "PriceTable",
    "RoutePrice",
    "estimate_spend",
    "load_price_table",
]
