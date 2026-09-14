# Vendored from AHepi/DeepReason@9607fba src/deepreason/adjudication/__init__.py (MIT, see src/deepreason_core/LICENSE); see docs/sources/deepreason-core-provenance.json
"""Adjudication — two-pass labeling (spec §4).

Inputs are ``att`` and ``dep`` ONLY. Measures, school membership,
novelty/diversity signals, and Pareto rank MUST NOT enter label computation
(§0): they act upstream via Spawn, budgeted commitments, or attention.
"""
