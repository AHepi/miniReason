"""Deterministic host-side routing for the bounded Flash pilot."""

from __future__ import annotations

from typing import Any, Mapping

from .templates import TEMPLATE_IDS, normalize_inputs, validate_inputs

_KIND_MAP = {
    "direct": "direct_answer",
    "direct_answer": "direct_answer",
    "evidence": "evidence_read",
    "evidence_read": "evidence_read",
    "engineer": "engineer_patch",
    "engineer_patch": "engineer_patch",
    "critic": "critic_return",
    "critic_return": "critic_return",
    "decompose": "decompose_synthesize",
    "decompose_synthesize": "decompose_synthesize",
}


def _flag(features: Mapping[str, Any], *names: str) -> bool:
    return any(bool(features.get(name)) for name in names)


def _deterministic_choice(text: str, features: Mapping[str, Any], inputs: Mapping[str, Any]) -> tuple[str, str]:
    kind = features.get("kind") or features.get("task_kind") or features.get("template_hint")
    if isinstance(kind, str) and kind in _KIND_MAP:
        selected = _KIND_MAP[kind]
        return selected, f"Structured task kind selects {selected}."

    if features:
        if _flag(features, "separable_dependencies", "substantial_derivation", "prior_leaf_ceiling", "requires_decomposition", "long_derivation"):
            return "decompose_synthesize", "Structured features identify separable or substantial dependent work."
        if _flag(features, "exact_source", "evidence_required", "requires_citations", "read_supplied_material"):
            return "evidence_read", "Structured features require locating support in supplied sources."
        if _flag(features, "bounded_code_change", "code_change", "engineering"):
            return "engineer_patch", "Structured features request a bounded code change and checks."
        if _flag(features, "disputed_candidate", "has_candidate", "criticism"):
            return "critic_return", "Structured features identify an existing candidate that needs criticism and revision."
        return "direct_answer", "Structured features describe no dependency, source-reading, patch, or candidate-review requirement."

    # Input shape outranks wording when the caller did not supply structured features.
    if inputs.get("documents") and inputs.get("requested_claims"):
        return "evidence_read", "Supplied documents and requested claims require a source-bound reading."
    if inputs.get("allowed_files") or inputs.get("behavior_contract") or inputs.get("test_commands"):
        return "engineer_patch", "The input packet requests a bounded change under file and test constraints."
    if inputs.get("candidate"):
        return "critic_return", "The input packet supplies a candidate for criticism and revision."

    lowered = text.casefold()
    if any(token in lowered for token in ("separable dependencies", "substantial derivation", "decompose", "synthesize")):
        return "decompose_synthesize", "The task explicitly asks to decompose dependent work and synthesize the results."
    if any(token in lowered for token in ("source quote", "exact quote", "saved record", "supplied document")):
        return "evidence_read", "The task explicitly asks for support from supplied source material."
    if any(token in lowered for token in ("patch", "bounded code change", "modify file", "test command")):
        return "engineer_patch", "The task explicitly asks for a bounded implementation and checks."
    if any(token in lowered for token in ("critic", "critique", "disputed candidate", "revise this answer")):
        return "critic_return", "The task explicitly asks to challenge and revise an existing candidate."
    return "direct_answer", "The task is a short closed request without a declared dependency or source requirement."


def _proposal(proposed: Mapping[str, Any] | None) -> tuple[str, str] | None:
    if not isinstance(proposed, Mapping) or set(proposed) != {"template_id", "reason"}:
        return None
    template_id = proposed.get("template_id")
    reason = proposed.get("reason")
    if template_id not in TEMPLATE_IDS or not isinstance(reason, str) or not reason.strip():
        return None
    return str(template_id), reason.strip()


def select_template(task: dict[str, Any], proposed: dict[str, Any] | None = None) -> dict[str, Any]:
    """Select a catalogue template, correcting invalid or unsuitable proposals."""
    if not isinstance(task, dict):
        raise ValueError("task must be an object")
    extra = sorted(set(task) - {"task", "features", "inputs"})
    if extra:
        raise ValueError(f"task contains unknown fields: {extra!r}")
    text = task.get("task")
    if not isinstance(text, str):
        raise ValueError("task.task must be a string")
    raw_features = task.get("features", {})
    raw_inputs = task.get("inputs", {})
    if not isinstance(raw_features, dict):
        raise ValueError("task.features must be an object")
    if not isinstance(raw_inputs, dict):
        raise ValueError("task.inputs must be an object")

    parsed_proposal = _proposal(proposed)
    fallback = proposed is not None and parsed_proposal is None
    missing = raw_features.get("missing_inputs", [])
    if _flag(raw_features, "missing_critical_info", "critical_information_missing") or missing:
        detail = ", ".join(str(item) for item in missing) if isinstance(missing, list) else str(missing)
        reason = "Task-critical information is missing"
        if detail:
            reason += f": {detail}"
        return {"template_id": "cannot_decide", "reason": reason + ".", "fallback": fallback or proposed is not None}
    if not text.strip():
        return {"template_id": "cannot_decide", "reason": "Task text is required before routing.", "fallback": fallback or proposed is not None}

    try:
        inputs = normalize_inputs(text, raw_inputs)
    except ValueError as exc:
        return {"template_id": "cannot_decide", "reason": f"The input packet is invalid: {exc}.", "fallback": fallback or proposed is not None}
    selected, reason = _deterministic_choice(text, raw_features, inputs)
    try:
        validate_inputs(selected, inputs)
    except ValueError as exc:
        return {"template_id": "cannot_decide", "reason": f"The selected route lacks task-critical information: {exc}.", "fallback": fallback or proposed is not None}

    if parsed_proposal is not None and parsed_proposal[0] == selected:
        return {"template_id": selected, "reason": parsed_proposal[1], "fallback": False}
    if parsed_proposal is not None and parsed_proposal[0] != selected:
        return {"template_id": selected, "reason": reason, "fallback": True}
    return {"template_id": selected, "reason": reason, "fallback": fallback}
