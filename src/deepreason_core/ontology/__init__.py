# Vendored from AHepi/DeepReason@9607fba src/deepreason/ontology/__init__.py (MIT, see src/deepreason_core/LICENSE); see docs/sources/deepreason-core-provenance.json
"""Ontology — the one schema (spec §1).

Artifacts are untyped (no ``kind`` field, ever). Dispatch is on interface
structure only: a warrant against a target contributes an attack edge; a
``dependence`` ref contributes a support edge. ``dep`` must remain a DAG.
"""

from deepreason_core.ontology.artifact import Artifact, Interface, Provenance, Ref
from deepreason_core.ontology.commitment import Budget, Commitment
from deepreason_core.ontology.event import (
    Event,
    LLMCall,
    Rule,
    StateDiff,
)
from deepreason_core.ontology.problem import Problem, ProblemProvenance, SpawnTrigger
from deepreason_core.ontology.state import EpistemicState, Status
from deepreason_core.ontology.warrant import Warrant, WarrantType

__all__ = [
    "Artifact",
    "Budget",
    "Commitment",
    "EpistemicState",
    "Event",
    "Interface",
    "LLMCall",
    "Problem",
    "ProblemProvenance",
    "Provenance",
    "Ref",
    "Rule",
    "SpawnTrigger",
    "StateDiff",
    "Status",
    "Warrant",
    "WarrantType",
]
