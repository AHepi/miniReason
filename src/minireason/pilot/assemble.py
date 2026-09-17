"""Synthesis binds host-accounted dependencies; a proposal is not verification."""
from collections.abc import Mapping

from .util import digest


def carryable_result(result):
    """Return whether a child may be assembled without relabelling its status.

    Historical accepted/complete records omitted ``output_status``.  That one
    shape remains coherent when the nested output is complete.  Partial carry
    is deliberately stricter: both the host record and nested output must say
    partial, and the host record must retain its unaccepted status.
    """
    if not isinstance(result, Mapping):
        return False
    output = result.get("output")
    if not isinstance(output, Mapping):
        return False
    status = result.get("status")
    nested_status = output.get("status")
    if status == "accepted":
        output_status = result.get("output_status", nested_status)
        return output_status == "complete" and nested_status == "complete"
    if status == "unaccepted":
        return result.get("output_status") == "partial" and nested_status == "partial"
    return False


def _partial_refusal(result):
    reason = result.get("refusal_reason")
    if isinstance(reason, str) and reason.strip():
        return reason.strip()
    return "PARTIAL_CHILD_NOT_ACCEPTED: output_status 'partial' is carried without acceptance"


def assemble(results, *, result_refs=None, answer=None, unresolved=None):
    if not isinstance(results, list) or any(not isinstance(item, Mapping) for item in results):
        raise ValueError("RESULTS_MUST_BE_OBJECTS")
    if any(not isinstance(item.get("result_ref"), str) or not item["result_ref"] for item in results):
        raise ValueError("INVALID_RESULT_REF")
    index = {r["result_ref"]: r for r in results}
    if len(index) != len(results):
        raise ValueError("DUPLICATE_RESULT_REF")
    refs = list(index) if result_refs is None else list(result_refs)
    if len(refs) != len(set(refs)) or any(ref not in index for ref in refs):
        raise ValueError("UNKNOWN_OR_DUPLICATE_RESULT_REF")
    if any(not carryable_result(index[ref]) for ref in refs):
        raise ValueError("UNACCEPTED_DEPENDENCY")
    missing = [ref for ref in index if ref not in refs]
    pending = list(unresolved or [])
    has_partial = False
    for ref in refs:
        result = index[ref]
        output = result["output"]
        pending.extend(output.get("unresolved", []))
        if output.get("status") == "partial":
            has_partial = True
            pending.append(f"Partial dependency {ref}: {_partial_refusal(result)}")
    pending.extend("Omitted dependency: " + ref for ref in missing)
    if not refs:
        pending.append("No accepted results")
    if answer is None:
        if len(refs) != 1:
            raise ValueError("MULTIPLE_RESULTS_NEED_SYNTHESIS")
        answer = index[refs[0]]["output"]["answer"]
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("EMPTY_ASSEMBLY")
    artifact = {"status": "partial" if has_partial or pending else "complete", "answer": answer,
                "source_refs": refs, "unresolved": list(dict.fromkeys(pending)),
                "verification_refs": [],
                "dependencies": {ref: digest(index[ref]) for ref in refs}}
    artifact["artifact_ref"] = "sha256:" + digest(artifact)
    return artifact


__all__ = ["assemble", "carryable_result"]
