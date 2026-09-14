
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
