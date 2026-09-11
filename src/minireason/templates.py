"""Original experiment templates built from Mini's public interfaces.

Names below describe experimental interventions, not epistemic types. No inherited
experiment manifest or prompt is reused. Every comparison must retain the exact
task contract and program language; visible test feedback is a separately named
intervention, not a free advantage attributed to artifact bookkeeping.
"""
from __future__ import annotations

import json
from typing import Any

from .tasks import evaluate, task_prompt

PROPOSAL = "minireason.proposal.v1"
FEEDBACK = "minireason.execution.v1"
CRITIC = "minireason.criticism.v1"
FINAL = "mini.verdict.v1"

TEMPLATES = {
    "critic_revision_v1": {
        "hypothesis": "Concrete objections with the candidate and its execution visible can guide a valid repair.",
        "proposal": "Construct a general program and explain its mechanism. Derive the order of operations from the contract. State a discriminating failure case and what behavior must survive any revision.",
        "critic": "Inspect the actual program, the prose account, and the execution evidence separately. Identify a concrete mismatch if one exists, name the clause and smallest distinguishing case, and explain the cause. An interpreter error is a construction or translation failure, not proof the prose account is false. If no defect is supported, say unresolved or no demonstrated defect; do not invent a fault. Your commitments should be ordinary prose, not a replacement program.",
        "revision": "Return the complete executable program in commitments and its explanatory account in body. Resolve the criticism by a causal repair, or retain the candidate if the criticism fails. State the operative change, why it addresses the actual failure, and which previously successful behavior is preserved. You may criticize the task interpretation or checker without being required to agree with them.",
    },
    "preservation_revision_v1": {
        "hypothesis": "Explicitly preserving prior successful cases prevents a local repair from damaging other obligations.",
        "proposal": "Construct a general program. In the body bind every important operation to a contract obligation and explain how the operations compose. Include a protected replay/reordering case and an independently discriminating boundary case. Commitments contains only the executable program.",
        "critic": "Try to defeat the program's account of the interactions among its operations. Use the actual execution evidence. Distinguish incorrect ordering of operations from a mistaken interpretation and a mere language error. Explain a minimal causal change and identify the established successful cases that change could break. Check the proposed criticism against those protected cases. If unsupported, retain the uncertainty; a mandatory criticism is not a mandatory accusation. Commitments is ordinary prose.",
        "revision": "Construct the full revised program. Give a preservation argument: name the operation changed, trace the failing case through the changed organization, and trace a previously successful case through it too. If no supported fault exists, preserve the implementation and strengthen the explanation only where justified. Program goes in commitments; prose stays in body.",
    },
    "rival_construction_v1": {
        "hypothesis": "A rival organization tested against a discriminating case can expose a shared mistake in the first organization.",
        "proposal": "Derive a program from the contract. Explain the organizational choice that is most at risk: which operation precedes another, why, and what observation distinguishes the reverse order. Give the complete executable program in commitments.",
        "critic": "Construct a substantially different organization at the level of operations, not a paraphrase. Compare its consequences with the supplied candidate and evidence on one case where they diverge. Say which organization the contract supports and why; if no divergence can be established, say so. Do not select by novelty, eloquence, number of components, or a scalar score. Commitments is your prose analysis, not necessarily a program.",
        "revision": "Use the rival's discriminating case to construct or preserve the organization warranted by the contract. Do not average the accounts. Explain the live route from the contrast to the operative decision. Give the complete general program in commitments and preserve known successful behavior.",
    },
}


def _port(name: str, *, window: str = "this_cycle") -> dict[str, Any]:
    return {"port_id": name, "port_type": name, "window": window}


def manifest_for(task_id: str = "reservation_replay_v1", template_id: str = "critic_revision_v1",
                 *, cycles: int = 1, feedback: bool = True, return_path: bool = True,
                 completion_tokens_per_call: int | None = None) -> dict[str, Any]:
    """Build a manifest with three model calls per cycle and explicit complete wiring.

    ``feedback=False`` is a no-execution-feedback control. ``return_path=False``
    withholds the critic and its evidence from final revision while retaining their
    exact bytes in the record; it is a diagnostic ablation, not bare inference.
    """
    if type(cycles) is not int or not 1 <= cycles <= 20:
        raise ValueError("cycles must be an integer between 1 and 20")
    template = TEMPLATES[template_id]
    port_types = [
        {"port_type": name, "draws_from": {"artifact_kinds": [kind]},
         "render": {"rule": "list_bodies_and_commitments", "header": header}}
        for name, kind, header in [("candidate", PROPOSAL, "Candidate and operative program"),
                                  ("observations", FEEDBACK, "Recorded executable observations"),
                                  ("criticism", CRITIC, "Criticism and its grounds"),
                                  ("previous", FINAL, "Previous completed revision")]
    ]

    def kind(kind_id: str, title: str, instruction: str, ports: list[dict[str, Any]]) -> dict[str, Any]:
        return {"kind_id": kind_id, "title": title, "instruction": instruction,
                "commitment_call": "single", "input_ports": ports,
                "output_port": {"port_id": "out", "produces_kind": kind_id},
                "failure_policy": {"retries": 0, "tolerance": 0, "action": "stop"}}

    proposal_ports = [_port("problem", window="all")]
    if cycles > 1 and return_path:
        proposal_ports.append(_port("previous", window="previous_cycle"))
    critic_ports = [_port("problem", window="all"), _port("candidate")]
    if feedback:
        critic_ports.append(_port("observations"))
    final_ports = [_port("problem", window="all"), _port("candidate")]
    if return_path:
        final_ports.append(_port("criticism"))
        if feedback:
            final_ports.append(_port("observations"))
    kinds = [kind(PROPOSAL, "Construct", template["proposal"], proposal_ports),
             kind(FEEDBACK, "Execute public cases", "Deterministic task interpreter.", [_port("candidate")]),
             kind(CRITIC, "Criticize", template["critic"], critic_ports),
             kind(FINAL, "Return a completed revision", template["revision"], final_ports)]
    stages = [{"stage_id": "conjecture", "kind_id": PROPOSAL, "ports": [p["port_id"] for p in proposal_ports]}]
    if feedback:
        stages.append({"stage_id": "execute", "kind_id": FEEDBACK, "seat": "machine", "ports": ["candidate"]})
    stages.extend([
        {"stage_id": "criticise", "kind_id": CRITIC, "ports": [p["port_id"] for p in critic_ports]},
        {"stage_id": "revise", "kind_id": FINAL, "ports": [p["port_id"] for p in final_ports]},
        {"stage_id": "end", "end": True},
    ])
    caps: dict[str, Any] = {"max_cycles": cycles, "max_calls": cycles * 3}
    if completion_tokens_per_call is not None:
        caps.update({"completion_tokens_per_call": completion_tokens_per_call,
                     "max_completion_tokens": cycles * 3 * completion_tokens_per_call})
    return {"schema_version": "creib.mini.manifest.v1",
            "manifest_id": f"minireason.{task_id}.{template_id}.feedback-{feedback}.return-{return_path}.cycles-{cycles}",
            "problem": task_prompt(task_id), "cycles": caps, "port_types": port_types,
            "kinds": kinds, "stages": stages,
            "sources": [{"source_id": "task-contract", "text": task_prompt(task_id)}]}


def register_task_seats() -> None:
    """Register in every CLI process before calling Mini; safe to invoke repeatedly."""
    from creib.forge.mini.machines import MachineSeat, register_machine_seat, registered_machine_seats

    if FEEDBACK in {seat.kind_id for seat in registered_machine_seats()}:
        return

    def answer(context: Any) -> str:
        admits = context.admits(PROPOSAL)
        candidates = [context.state.artifacts[key] for key in context.state.artifact_order
                      if context.state.artifacts[key]["kind_id"] == PROPOSAL
                      and admits(context.state.artifacts[key])]
        if not candidates:
            raise ValueError("EXPERIMENT_CANDIDATE_PORT_EMPTY: public checker has no candidate")
        candidate = candidates[-1]
        result = evaluate(context.commitments(candidate))
        return json.dumps({"body": "Observed behavior of the current candidate on the public cases. "
                                   "This is a finite executable check; it makes no creativity verdict.",
                           "commitments": json.dumps(result, sort_keys=True),
                           "about": [candidate["artifact_id"]]})

    register_machine_seat(MachineSeat(FEEDBACK, "Evaluate a candidate on public reservation cases.", answer))
