"""Regression: crash mid-append must not swallow the NEXT event.

Found by the MiniReason chaos battery (mini/tests/test_chaos.py): a torn
final line has no trailing newline, so a post-recovery append used to write
onto the fragment; the merged line was then dropped as "torn" on the next
read — an acknowledged, fsynced event lost after a clean recovery. The fix
truncates the never-durable tail at open.

Vendored from AHepi/DeepReason@9607fba tests/test_torn_append.py; see
VENDOR_NOTES.md.
"""

from __future__ import annotations

from deepreason_core.harness import Harness
from deepreason_core.ontology import Provenance

from .helpers import TempDirTestCase


class TornAppendTests(TempDirTestCase):
    def test_append_after_torn_tail_preserves_the_new_event(self) -> None:
        root = self.tmp_path / "run"
        h = Harness(root)
        h.create_artifact("survivor", provenance=Provenance(role="seed"))
        with open(root / "log.jsonl", "a") as f:
            f.write('{"seq": 1, "rule": "Meas')  # crash mid-append

        with self.assertWarnsRegex(UserWarning, "torn final line"):
            h2 = Harness(root)
        recovered = h2.create_artifact("post-crash", provenance=Provenance(role="seed"))

        # The post-crash event survives a fresh replay, on its own line.
        h3 = Harness(root)
        self.assertIn(recovered.id, h3.state.artifacts)
        self.assertEqual([e.seq for e in h3.log.read()], [0, 1])

    def test_interior_corruption_still_raises(self) -> None:
        h = Harness(self.tmp_path / "run")
        h.create_artifact("a", provenance=Provenance(role="seed"))
        h.create_artifact("b", provenance=Provenance(role="seed"))
        path = h.log.path
        lines = path.read_text().splitlines()
        lines[0] = lines[0][: len(lines[0]) // 2]
        path.write_text("\n".join(lines) + "\n")
        with self.assertRaises(Exception):
            Harness(self.tmp_path / "run")

    def test_concurrent_harnesses_conflict_loudly(self) -> None:
        """Two live Harnesses on one root: the stale writer raises instead of
        appending a duplicate seq (single-writer by design; also found by the
        mini chaos battery)."""
        from deepreason_core.log.event_log import ConcurrentWriterError

        root = self.tmp_path / "run"
        h1, h2 = Harness(root), Harness(root)
        h1.create_artifact("from-h1", provenance=Provenance(role="seed"))
        with self.assertRaises(ConcurrentWriterError):
            h2.create_artifact("from-h2", provenance=Provenance(role="seed"))
