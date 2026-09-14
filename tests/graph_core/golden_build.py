"""Standalone builder for the byte-identity golden (spec §16 P0, item 6).

Deliberately self-contained: it imports ``deepreason_core`` and the standard
library ONLY, never ``unittest`` or the sibling helpers. That is what lets the
byte-identity test run this exact code in a SEPARATE interpreter — started
with a different ``PYTHONHASHSEED`` — and compare the two roots' bytes. A
builder that needed the test harness to import it could not be launched that
way, and an in-process "second build" cannot see a hash-seed-dependent
iteration order, which is the failure mode this golden exists to catch.

Run directly (``python golden_build.py <root>``) or as a module
(``python -m tests.graph_core.golden_build <root>``). Either way it prints a
one-line JSON receipt on stdout so the parent can prove the build really
happened in another interpreter.
"""

from __future__ import annotations

import contextlib
import datetime as _datetime
import json
import os
import sys
import unittest.mock
from pathlib import Path

from deepreason_core.harness import Harness
from deepreason_core.ontology import (
    Commitment,
    Interface,
    Problem,
    ProblemProvenance,
    Provenance,
    Ref,
    Warrant,
    WarrantType,
)

# The wall clock is the ONLY nondeterministic input to the event log: ids are
# content addresses, object/blob bytes are canonical, and edge sets are
# sorted. Freezing it is what turns "replay is deterministic" into a byte
# assertion instead of a structural one.
FIXED_TS = _datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=_datetime.timezone.utc)

# Shape of the reference graph below, asserted before any equality check so an
# empty or truncated build cannot pass by comparing nothing to nothing.
EXPECTED_EVENTS = 9
EXPECTED_ARTIFACTS = 6
EXPECTED_OBJECTS = 10  # 6 artifacts + 1 commitment + 1 problem + 2 warrants
EXPECTED_BLOBS = 1


class _FrozenDatetime(_datetime.datetime):
    """``datetime`` whose ``now`` is constant, for byte-identity tests."""

    @classmethod
    def now(cls, tz=None):  # noqa: D102 - mirrors datetime.datetime.now
        return FIXED_TS if tz is None else FIXED_TS.astimezone(tz)


@contextlib.contextmanager
def frozen_clock():
    """Pin ``Event.ts`` so two independent builds are byte-comparable.

    Patches the module-level ``datetime`` the harness stamps events with, so
    it holds whether or not a caller also passes an explicit clock.
    """

    import deepreason_core.harness as harness_module

    with unittest.mock.patch.object(harness_module, "datetime", _FrozenDatetime):
        yield


def _attack(harness: Harness, target_id: str, note: str):
    """Register nu + a critic artifact carrying a warrant against target.

    Mirrors ``helpers.attack``; kept local so this module stays importable
    with no test-package context (see the module docstring).
    """
    nu = harness.create_artifact(
        f"nu: the attack '{note}' is sound and relevant",
        provenance=Provenance(role="seed"),
    )
    warrant = Warrant(
        id=f"w-{note}",
        target=target_id,
        type=WarrantType.ARGUMENTATIVE,
        validity_node=nu.id,
    )
    critic = harness.create_artifact(
        f"critic: {note}",
        provenance=Provenance(role="critic"),
        warrants=[warrant],
    )
    return critic, nu


def build_reference_graph(root) -> Harness:
    """A small but complete P0 graph: a problem, a commitment, a support
    chain, an attack, a reinstatement, and a Measure payload."""
    harness = Harness(root)
    harness.register_commitment(Commitment(id="kappa-golden", eval="predicate:True"))
    problem = harness.register_problem(
        Problem(
            id="pi-golden",
            description="the golden problem",
            criteria=["kappa-golden"],
            provenance=ProblemProvenance.model_validate(
                {"trigger": "seed", "from": []}
            ),
        )
    )
    premise = harness.create_artifact(
        b"premise bytes stored as a blob",
        codec="raw",
        provenance=Provenance(role="seed"),
        problem_id=problem.id,
    )
    dependent = harness.create_artifact(
        "a claim that depends on the premise",
        interface=Interface(
            commitments=["kappa-golden"],
            refs=[Ref(target=premise.id, role="dependence")],
        ),
        provenance=Provenance(role="conjecturer"),
        problem_id=problem.id,
    )
    critic, nu = _attack(harness, dependent.id, "golden-critic")
    _attack(harness, nu.id, "golden-counter-critic")
    harness.record_measure(
        hv={dependent.id: 0.25}, reach={dependent.id: 0.5}, inputs=[dependent.id]
    )
    return harness


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: golden_build.py <root>", file=sys.stderr)
        return 2
    root = Path(argv[1])
    with frozen_clock():
        harness = build_reference_graph(root)
    receipt = {
        "pid": os.getpid(),
        "executable": sys.executable,
        "pythonhashseed": os.environ.get("PYTHONHASHSEED", "<unset>"),
        "events": len(list(harness.log.read())),
        "objects": sum(1 for p in (root / "objects").rglob("*") if p.is_file()),
        "blobs": sum(1 for p in (root / "blobs").rglob("*") if p.is_file()),
        "artifacts": len(harness.state.artifacts),
    }
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
