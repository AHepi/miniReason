"""Distinct followup template: inspect an encountered issue, then discriminate.

The contract preserves ordinary prose and permits no successor investigation.
It neither generates another joint construction nor installs a diagnosis.
"""
TEMPLATE_ID = "successor_discrimination_v1"
STAGES = ("locate", "discriminate")
SYSTEM_MESSAGE = (
    "Respond in ordinary prose, with optional formal expressions or fenced source code. "
    "No JSON envelope is required. Preserve uncertainty and substantive criticism. "
    "No scalar score, creativity verdict or semantic status assignment is requested."
)
STAGE_INSTRUCTIONS = {
    "locate": (
        "Examine the exact proposed successor and its actual parent occurrences. Identify the "
        "question or uncertainty it raises, what claim or use it could affect, and which source "
        "passages and assumptions its diagnosis depends on. Preserve the distinction between the "
        "original construction, its criticism, the proposed revision and the later suggestion. "
        "If the suggestion misattributes an earlier claim, changes the question, or supplies no "
        "distinct question, explain that possibility using the provided content. Do not presume "
        "a defect is present. A question about whether an objection bears is admissible; ordinary "
        "prose is sufficient. Do not generate another joint construction or silently amend the "
        "frozen source. No successor investigation starts from this response."
    ),
    "discriminate": (
        "Using the frozen material and the actual preceding examination, attempt a substantive "
        "argument or case that distinguishes the live accounts. State which facts are supplied, "
        "which premises you add, and which observations remain unavailable; a proposed test is "
        "not an executed observation. State what different outcomes would change about the "
        "original use and which claims or uses must remain distinguishable. Then give a "
        "successor investigation only if there is a reason to allocate work to it. You may "
        "instead retain the current question, suspend pending named evidence, or conclude that "
        "no further problem is presently warranted. Do not turn allocation into acceptance of "
        "a diagnosis, install a language change, or manufacture a progress verdict. Do not "
        "regenerate the original joint construction. Ordinary prose is sufficient."
    ),
}
BASELINE_INSTRUCTION = (
    "In one response, examine the exact proposed successor and its actual parent occurrences, "
    "identify the question and its source grounds, and attempt a substantive argument or case "
    "that distinguishes the live accounts. Preserve the distinction between original "
    "construction, criticism, revision and later suggestion. Do not presume a defect is present. "
    "State which facts are supplied, which premises you add, and what evidence remains unavailable; "
    "a proposed test is not an executed observation. State what different outcomes would change "
    "about the original use and which claims or uses must remain distinguishable. Give a successor "
    "investigation only if there is a reason to allocate work to it. You may instead retain the "
    "current question, suspend pending named evidence, or conclude that no further problem is "
    "presently warranted. A question about whether an objection bears is admissible. Do not "
    "turn allocation into acceptance of a diagnosis, install a language change, regenerate the "
    "original joint construction or manufacture a progress verdict. Ordinary prose is sufficient."
)


def template_contract():
    """Return a fresh explicit contract for the coordinator and study plan."""
    return {
        "schema": "minireason.template-contract.v1", "template_id": TEMPLATE_ID,
        "cycles": 1, "stages": list(STAGES),
        "stage_instructions": dict(STAGE_INSTRUCTIONS),
        "baseline_instruction": BASELINE_INSTRUCTION, "system_message": SYSTEM_MESSAGE,
        "input_contract": "whole verified handoff; actual locate only at discriminate",
        "automatic_successor_started": False,
    }
