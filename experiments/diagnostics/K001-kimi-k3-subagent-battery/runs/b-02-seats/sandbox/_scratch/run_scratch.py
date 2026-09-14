"""Scratch-only harness to iterate tests/loop/test_seats.py.

Builds faithful (docstring-derived) stand-ins for the absent wave-0 modules
(minireason.loop.types, minireason.loop.contracts) and a controlled owner-runner
(tools.multicycle_commitment_study_multi_v2) under the sandbox ``_scratch``
tree, writes a ``sitecustomize`` that orders ``sys.path`` so the sandbox and the
scratch tree beat any ambient copy of the real repository the interpreter can
import by default, and spawns the real ``run_tests.py`` in a child interpreter.
This runner and the whole ``_scratch`` tree are deleted before the task
finishes; nothing under tests/ or src/ is touched.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(ROOT)              # the sandbox root
SBX = os.path.join(ROOT, "_scratch")
SBX_SRC = os.path.join(SBX, "src")
TOOLS = os.path.join(SBX, "tools")


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as handle:
        handle.write(text)


RUNNER = '''
"""Scratch stand-in for the owner runner v2. Deleted before finishing."""
import threading

OWNER_MAX = 5
MAX_PER_KEY = 5

class _RunnerFailure(RuntimeError):
    def __init__(self, code, detail=""):
        self.code = code
        super().__init__(f"{code}: {detail}")

_LOCK = threading.Lock()
_REGISTRY = {}

def key_gate(key_env, cap):
    with _LOCK:
        existing = _REGISTRY.get(key_env)
        if existing is None:
            created = (threading.BoundedSemaphore(cap), cap)
            _REGISTRY[key_env] = created
            return created[0]
        sem, limit = existing
        if limit != cap:
            raise ValueError(
                f"{key_env} is already held to {limit} concurrent requests in this process; "
                f"a caller asking for {cap} would change an authorisation in force")
        return sem

def _reset():
    with _LOCK:
        _REGISTRY.clear()
'''

TYPES = '''
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
        if not isinstance(min_judge_families, int) or isinstance(min_judge_families, bool) \
                or min_judge_families < 1:
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
'''

CONTRACTS = '''
"""Scratch stand-in for wave-0 contracts. Deleted before finishing."""
ROLE_NAMES = ("critic", "defender", "judge", "marker", "variator")

class ContractError(Exception):
    pass
'''

# Exact __path__ stitches: the scratch copy first, then this sandbox's real copy,
# computed once here and baked in so the child never re-derives it from a CWD.
MINIREASON_INIT = "__path__ = [%r]\n" % ([SBX_SRC + "/minireason", os.path.join(ROOT, "src", "minireason")],)
LOOP_INIT = "__path__ = [%r]\n" % ([SBX_SRC + "/minireason/loop", os.path.join(ROOT, "src", "minireason", "loop")],)

# sitecustomize runs before the main script; it puts the wanted roots at the
# FRONT of sys.path so this tree outranks any site-admin copy of the repository.
SITECUSTOMIZE = (
    "import sys\n"
    "for _entry in [%r, %r, %r, %r]:\n"
    "    while _entry in sys.path:\n"
    "        sys.path.remove(_entry)\n"
    "    sys.path.insert(0, _entry)\n"
    % (SBX_SRC, SBX, os.path.join(ROOT, "src"), ROOT)
)

write(os.path.join(SBX, "sitecustomize.py"), SITECUSTOMIZE)
write(os.path.join(TOOLS, "__init__.py"), "")
write(os.path.join(TOOLS, "multicycle_commitment_study_multi_v2.py"), RUNNER)
write(os.path.join(SBX_SRC, "minireason", "__init__.py"), MINIREASON_INIT)
write(os.path.join(SBX_SRC, "minireason", "loop", "__init__.py"), LOOP_INIT)
write(os.path.join(SBX_SRC, "minireason", "loop", "types.py"), TYPES)
write(os.path.join(SBX_SRC, "minireason", "loop", "contracts.py"), CONTRACTS)


def main():
    env = dict(os.environ)
    env["PYTHONPATH"] = SBX + os.pathsep + env.get("PYTHONPATH", "")
    target = sys.argv[1] if len(sys.argv) > 1 else "tests.loop.test_seats"
    proc = subprocess.run(
        [sys.executable, "run_tests.py", target], cwd=ROOT, env=env)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
