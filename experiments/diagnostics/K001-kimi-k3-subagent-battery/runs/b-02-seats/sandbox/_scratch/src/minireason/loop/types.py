
"""Scratch stand-in for wave-0 types. Deleted before finishing."""
from __future__ import annotations

CODE_MESSAGE = {
    "CONFIG_NOT_A_MAPPING": "not a mapping",
    "CONFIG_SCHEMA_UNKNOWN": "schema unknown",
    "CONFIG_UNKNOWN_KEY": "unknown key",
    "CONFIG_MISSING_KEY": "a required config key is missing",
    "CONFIG_INVALID_VALUE": "invalid value",
    "PIN_INVALID": "pin invalid",
    "RUN_ID_INVALID": "run id invalid",
    "CYCLE_OUT_OF_RANGE": "cycle out of range",
    "STEP_RECEIPT_INVALID": "step receipt invalid",
    "STEP_KEY_MISMATCH": "step key mismatch",
    "BLOCK_CODE_UNKNOWN": "block code unknown",
    "FAMILY_COUNT_INSUFFICIENT": "family count insufficient",
    "SEAT_COUNT_INSUFFICIENT": "seat count insufficient",
    "REGISTRY_INVALID": "registry invalid",
    "RUNNER_NOT_IMPORTABLE": "runner not importable",
    "CONCURRENCY_LIMIT_CONFLICT": "concurrency limit conflict",
}
FAILURE_CODES = frozenset(CODE_MESSAGE)

class LoopError(RuntimeError):
    def __init__(self, code, detail=""):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)

class SeatsConfig:
    _FIELDS = ("critic", "defender", "judges", "variator", "min_judge_families")
    def __init__(self, *, critic=None, defender=None, judges=(), variator=None,
                 min_judge_families=2):
        self.critic = critic
        self.defender = defender
        self.judges = tuple(judges)
        self.variator = variator
        self.min_judge_families = min_judge_families
        for value in (critic, defender, variator):
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise LoopError("CONFIG_INVALID_VALUE",
                                "a pinned seat must name an endpoint by a non-empty string")
        if not isinstance(min_judge_families, int) or isinstance(min_judge_families, bool)                 or min_judge_families < 1:
            raise LoopError("CONFIG_INVALID_VALUE",
                            "min_judge_families must be a whole number of at least 1")
        for name in self.judges:
            if not isinstance(name, str) or not name.strip():
                raise LoopError("CONFIG_INVALID_VALUE",
                                "seats.judges must name endpoints by non-empty strings")
        if len(self.judges) < self.min_judge_families:
            raise LoopError("CONFIG_INVALID_VALUE",
                            f"seats.judges names {len(self.judges)} seats, fewer than "
                            f"min_judge_families {self.min_judge_families}")
    @classmethod
    def from_mapping(cls, raw):
        if not isinstance(raw, dict):
            raise LoopError("CONFIG_NOT_A_MAPPING", CODE_MESSAGE["CONFIG_NOT_A_MAPPING"])
        unknown = set(raw) - set(cls._FIELDS)
        if unknown:
            raise LoopError("CONFIG_UNKNOWN_KEY",
                            f"unknown seats config keys: {sorted(unknown)}")
        kwargs = {f: raw[f] for f in cls._FIELDS if f in raw}
        return cls(**kwargs)
    def as_dict(self):
        return {f: getattr(self, f) for f in self._FIELDS}

class LoopConfig:
    def __init__(self, seats=None, max_per_key=5):
        self.seats = seats if seats is not None else SeatsConfig()
        self.max_per_key = max_per_key
    @classmethod
    def from_mapping(cls, raw):
        if not isinstance(raw, dict):
            raise LoopError("CONFIG_NOT_A_MAPPING", CODE_MESSAGE["CONFIG_NOT_A_MAPPING"])
        seats = SeatsConfig.from_mapping(raw.get("seats", {}))
        return cls(seats=seats, max_per_key=raw.get("max_per_key", 5))
    def as_dict(self):
        return {"seats": self.seats.as_dict(), "max_per_key": self.max_per_key}
