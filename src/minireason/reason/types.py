"""Public failure vocabulary for the personal harness."""
from __future__ import annotations
from typing import Any

DISPOSITIONS = frozenset({"taken-up", "rejected-with-reason", "unresolved"})

class ReasonFailure(RuntimeError):
    """A named failure with public evidence only, never a credential value."""
    def __init__(self, code: str, detail: str, record: dict[str, Any] | None = None):
        self.code = code
        self.detail = detail
        self.record = record or {}
        super().__init__(f"{code}: {detail}")
