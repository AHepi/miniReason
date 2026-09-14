# Vendored from AHepi/DeepReason@9607fba src/deepreason/log/__init__.py (MIT, see src/deepreason_core/LICENSE); see docs/sources/deepreason-core-provenance.json
"""Event log — append-only JSONL source of truth (spec §1, D8)."""

from deepreason_core.log.event_log import EventLog

__all__ = ["EventLog"]
