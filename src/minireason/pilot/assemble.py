"""Synthesis binds host-accepted dependencies; a proposal is not verification."""
from .util import digest

def assemble(results, *, result_refs=None, answer=None, unresolved=None):
    index = {r["result_ref"]: r for r in results}
    if len(index) != len(results):
        raise ValueError("DUPLICATE_RESULT_REF")
    refs = list(index) if result_refs is None else result_refs
    if len(refs) != len(set(refs)) or any(ref not in index for ref in refs):
        raise ValueError("UNKNOWN_OR_DUPLICATE_RESULT_REF")
    if any(index[ref]["status"] != "accepted" for ref in refs):
        raise ValueError("UNACCEPTED_DEPENDENCY")
    missing = [ref for ref in index if ref not in refs]
    pending = list(unresolved or [])
    for ref in refs:
        output = index[ref]["output"]
        pending.extend(output.get("unresolved", []))
        if output.get("status") != "complete":
            pending.append("Incomplete dependency: " + ref)
    pending.extend("Omitted dependency: " + ref for ref in missing)
    if not refs:
        pending.append("No accepted results")
    if answer is None:
        if len(refs) != 1:
            raise ValueError("MULTIPLE_RESULTS_NEED_SYNTHESIS")
        answer = index[refs[0]]["output"]["answer"]
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("EMPTY_ASSEMBLY")
    artifact = {"status": "partial" if pending else "complete", "answer": answer,
                "source_refs": refs, "unresolved": list(dict.fromkeys(pending)),
                "verification_refs": [],
                "dependencies": {ref: digest(index[ref]) for ref in refs}}
    artifact["artifact_ref"] = "sha256:" + digest(artifact)
    return artifact
