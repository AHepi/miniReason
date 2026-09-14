"""Shared builders for P0 acceptance tests (spec §16).

Vendored from AHepi/DeepReason@9607fba tests/conftest.py; the pytest
``harness`` fixture becomes ``HarnessTestCase`` and the ``tmp_path``
fixture becomes a per-test temporary directory. See VENDOR_NOTES.md.
"""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from deepreason_core.harness import Harness
from deepreason_core.ontology import Interface, Provenance, Warrant, WarrantType


class TempDirTestCase(unittest.TestCase):
    """Replaces pytest's ``tmp_path`` fixture."""

    def setUp(self) -> None:
        super().setUp()
        self.tmp_path = Path(tempfile.mkdtemp(prefix="deepreason-core-"))
        self.addCleanup(shutil.rmtree, self.tmp_path, ignore_errors=True)


class HarnessTestCase(TempDirTestCase):
    """Replaces pytest's ``harness`` fixture (``Harness(tmp_path / "run")``)."""

    def setUp(self) -> None:
        super().setUp()
        self.harness = Harness(self.tmp_path / "run")


def art(harness: Harness, text: str, *, interface: Interface | None = None, **kwargs):
    return harness.create_artifact(
        text,
        interface=interface,
        provenance=kwargs.pop("provenance", Provenance(role="seed")),
        **kwargs,
    )


def attack(harness: Harness, target_id: str, note: str, *, warrant_kwargs: dict | None = None):
    """Register nu + a critic artifact carrying a warrant against target."""
    nu = art(harness, f"nu: the attack '{note}' is sound and relevant")
    warrant = Warrant(
        id=f"w-{note}",
        target=target_id,
        type=WarrantType.ARGUMENTATIVE,
        validity_node=nu.id,
        **(warrant_kwargs or {}),
    )
    critic = harness.create_artifact(
        f"critic: {note}",
        provenance=Provenance(role="critic"),
        warrants=[warrant],
    )
    return critic, nu

