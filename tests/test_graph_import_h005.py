"""Offline H005 -> spec-v1.3 import tests: occurrence bytes only; no provider, no network.

These tests read the **real** occurrence,
``experiments/diagnostics/H005-open-prose-commitments/occurrence-01``, read-only.
There is no fixture copy: a partial copy is a second set of bytes that can drift
from the thing under test, and the copy that used to live here lacked the
matched arm's ``responses/`` and ``attempts/``, so it silently exercised a
receipt-less path that does not exist in the occurrence. ``tests/data/
h005_import_pins.json`` pins the sha256 of every occurrence file the tests
depend on; ``setUpModule`` re-hashes them, skips the module if the occurrence is
absent and fails loudly if a pinned hash differs. Tamper tests copy the
occurrence into a TemporaryDirectory and corrupt the copy.

The golden expectation is ``scratchpad/h005-import/expected_graph.md`` as
corrected by the adversarial reviews (see NOTES.md / docs/design/
h005-import-notes-2026-09-14.md), machine-checked against the vendored
adjudicator and hand-derived in those notes.
"""
from __future__ import annotations

import dataclasses
import filecmp
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from deepreason_core.harness import Harness
from deepreason_core.ontology import Interface

from minireason.graph_import_h005 import (
    COMMITMENT_SURFACE_STATES,
    MULTI_ARM_FRAMING_TAIL,
    RESIDUE_CODES,
    Coordinate,
    CustodyError,
    ImportReport,
    MappingError,
    OutRootRefused,
    SelectorMatchedNothing,
    _Importer,
    _Node,
    _Reader,
    import_occurrence,
    parse_fcl1_document,
    study_digest,
)

HERE = Path(__file__).resolve().parent
PINS_PATH = HERE / "data" / "h005_import_pins.json"
OCCURRENCE_RELATIVE = Path(
    "experiments/diagnostics/H005-open-prose-commitments/occurrence-01"
)
CLI = HERE.parent / "tools" / "import_h005.py"

SCOPE = {"problems": ["daily"], "arms": ["mini_fcl"], "cycles": [1]}
MATCHED_SCOPE = {"problems": ["daily"], "arms": ["mini_fcl", "matched"], "cycles": [1]}

EXPECTED_LABELS = {
    # node artifacts
    "daily/mini_fcl/cycle01/account": "refuted",
    "daily/mini_fcl/cycle01/objection": "accepted",
    "daily/mini_fcl/cycle01/rival": "accepted",
    "daily/mini_fcl/cycle01/response": "refuted",
    "daily/mini_fcl/cycle01/carry": "accepted",
    # the FCL-1 documents, registered as their own artifacts
    "daily/mini_fcl/cycle01/account#commitments": "accepted",
    "daily/mini_fcl/cycle01/objection#commitments": "accepted",
    "daily/mini_fcl/cycle01/rival#commitments": "accepted",
    "daily/mini_fcl/cycle01/response#commitments": "accepted",
    "daily/mini_fcl/cycle01/carry#commitments": "accepted",
    # validity nodes
    "nu:objection#o1->account": "accepted",
    "nu:objection#o2->account": "accepted",
    "nu:objection#o3->account": "accepted",
    "nu:response#k3->rival": "accepted",
    "nu:response#k7->rival": "refuted",
    "nu:carry#n3->response": "accepted",
    "nu:carry#n3->nu(response#k7)": "accepted",
}

EXPECTED_RESIDUE = {
    "adjudication_batched": 1,
    "bare_label_ref": 1,
    # 15 claim records in the five golden documents. uptake_refs_unmapped does
    # NOT cover them: rival.r1/r3/r4 are claims the author left out of uptake.
    "claim_record_unmapped": 15,
    "commitment_not_executable": 4,
    "commitment_record_not_in_uptake": 2,
    "consequence_on_non_commitment_record": 9,
    # objection.o4 -> o1 and o4 -> o2: criticism of a criticism carried by the
    # same artifact, deliberately NOT retargeted (it would self-attack through
    # the carrier closure).
    "criticism_of_criticism_intra_document_dropped": 2,
    "criticism_of_criticism_retargeted": 1,
    "dependence_cycle_rejected": 0,
    "depends_cross_document": 0,
    "depends_intra_document": 17,
    "grounds_absent_on_objection": 9,
    "mentions_intra_document": 9,
    "objection_self_target_only": 1,
    "objection_target_self_ref_dropped": 4,
    "objection_untargeted": 2,
    "opaque_envelope": 0,
    "parse_failure": 0,
    "problem_trigger_approximated": 5,
    "problem_trigger_research_not_in_v13_enum": 4,
    "projection_absent": 2,
    "projection_exposed_unreferenced": 2,
    "prose_commitment_surface": 0,
    "qualified_ref_body_pseudo_local": 1,
    "ref_through_absent_projection": 0,
    "ref_through_unexposed_view": 0,
    "ref_to_task_artifact": 0,
    "ref_to_unregistered_target_dropped": 0,
    "ref_unresolved": 0,
    "revises_unmapped": 0,
    "schema_failure": 0,
    "target_on_non_objection_record": 7,
    "uptake_lists_unmapped": 5,
    "uptake_refs_unmapped": 32,
    "use_record_unmapped": 9,
    "validity_node_minted_unasserted": 7,
    "warrant_edge_deduplicated": 2,
    "withdraws_unmapped": 0,
}

OCCURRENCE: Path | None = None
PINS: dict = {}


def _candidate_roots() -> list[Path]:
    """Where the repository might be, in staging and after publication."""
    roots: list[Path] = []
    override = os.environ.get("H005_OCCURRENCE_ROOT")
    if override:
        roots.append(Path(override))
    roots.extend(HERE.parents)
    try:  # the repository's own package, wherever it is on sys.path
        import minireason

        for portion in list(getattr(minireason, "__path__", [])):
            roots.append(Path(portion).resolve().parents[1])
    except Exception:  # pragma: no cover - defensive
        pass
    roots.append(Path.cwd())
    roots.extend(Path.cwd().parents)
    return roots


def setUpModule() -> None:
    """Locate the occurrence and re-hash every file the tests depend on."""
    global OCCURRENCE, PINS
    PINS = json.loads(PINS_PATH.read_text(encoding="utf-8"))
    for root in _candidate_roots():
        candidate = root / OCCURRENCE_RELATIVE
        if (candidate / "plan.json").is_file():
            OCCURRENCE = candidate.resolve()
            break
    if OCCURRENCE is None:
        # A skip is a green run that tested nothing. CI runs on a full
        # checkout, where the occurrence is always present, so its absence
        # there is a broken checkout and must be loud. A developer who really
        # wants to run the rest of the tree without it sets
        # H005_IMPORT_ALLOW_SKIP=1 and says so deliberately.
        message = f"occurrence not found under any candidate root: {OCCURRENCE_RELATIVE}"
        if os.environ.get("H005_IMPORT_ALLOW_SKIP") == "1":
            raise unittest.SkipTest(message + " (H005_IMPORT_ALLOW_SKIP=1)")
        raise AssertionError(
            "OCCURRENCE_ABSENT: " + message + ". These tests read the real occurrence and "
            "nothing else; without it they verify nothing. Set H005_IMPORT_ALLOW_SKIP=1 to "
            "skip the module deliberately, or H005_OCCURRENCE_ROOT to point at the checkout."
        )
    changed = []
    for relative, digest in sorted(PINS["files"].items()):
        path = OCCURRENCE / relative
        if not path.is_file():
            changed.append(f"{relative}: MISSING")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest:
            changed.append(f"{relative}: {digest} -> {actual}")
    if changed:
        # Same posture as the importer's own custody: refuse, do not adapt.
        raise AssertionError(
            "OCCURRENCE_PIN_MISMATCH: the write-once occurrence no longer matches "
            "tests/data/h005_import_pins.json:\n  " + "\n  ".join(changed)
        )


def named_labels(report: ImportReport) -> dict:
    return {report.names[aid]: status for aid, status in report.labels.items()}


def tree_hashes(root: Path) -> dict:
    return {
        str(path.relative_to(root)).replace("\\", "/"): hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def copy_occurrence(destination: Path, *, arms: tuple[str, ...] = ("mini_fcl",)) -> Path:
    """A writable copy of the occurrence, narrowed to the arms a test needs.

    ``ignore`` is called with the SOURCE directory being visited, so the
    arm-level prune is keyed on ``OCCURRENCE/<category>/<problem>``.
    """
    keep = set(arms)

    def ignore(directory, names):
        source = Path(directory)
        if source.parent.parent == OCCURRENCE:  # <category>/<problem>: arm names
            return [name for name in names if name not in keep]
        return []

    shutil.copytree(OCCURRENCE, destination, ignore=ignore)
    return destination


def labels_row(markdown: str, name: str) -> str:
    """The REPORT.md labels-table row for one artifact, by readable name."""
    prefix = f"| `{name}` |"
    rows = [line for line in markdown.splitlines() if line.startswith(prefix)]
    assert len(rows) == 1, f"{len(rows)} rows for {name}"
    return rows[0]


def run_cli(*arguments: str) -> subprocess.CompletedProcess:
    environment = dict(os.environ)
    environment.setdefault("PYTHONPATH", os.pathsep.join(sys.path[1:]))
    environment["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(CLI), *arguments],
        capture_output=True,
        text=True,
        env=environment,
    )


class GoldenImportTest(unittest.TestCase):
    """daily / mini_fcl / cycle01, template fork5, read from the real occurrence."""

    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory(prefix="h005-import-golden-")
        cls.root = Path(cls.directory.name) / "graph"
        cls.report = import_occurrence(OCCURRENCE, cls.root, **SCOPE)

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def test_labels_are_exactly_the_expected_graph(self):
        self.assertEqual(named_labels(self.report), EXPECTED_LABELS)
        counts = {}
        for status in self.report.labels.values():
            counts[status] = counts.get(status, 0) + 1
        self.assertEqual(counts, {"accepted": 14, "refuted": 3})
        self.assertNotIn("suspended", counts)
        self.assertNotIn("suspended_unsupported", counts)

    def test_graph_shape_and_the_empty_dependence_relation(self):
        self.assertEqual(len(self.report.labels), 17)
        self.assertEqual(len(self.report.spec_id_table), 5)
        self.assertEqual(len(self.report.warrants), 7)
        self.assertEqual(len({w["validity_node"] for w in self.report.warrants}), 7)
        self.assertEqual(len(self.report.att_edges), 4)
        self.assertEqual(self.report.dep_edges, ())
        names = self.report.names
        self.assertEqual(
            sorted((names[a], names[b]) for a, b in self.report.att_edges),
            [
                ("daily/mini_fcl/cycle01/carry", "daily/mini_fcl/cycle01/response"),
                ("daily/mini_fcl/cycle01/carry", "nu:response#k7->rival"),
                ("daily/mini_fcl/cycle01/objection", "daily/mini_fcl/cycle01/account"),
                ("daily/mini_fcl/cycle01/response", "daily/mini_fcl/cycle01/rival"),
            ],
        )

    def test_criticism_of_a_criticism_attacks_the_validity_node(self):
        retargeted = [w for w in self.report.warrants if w["target_kind"] == "validity_node"]
        self.assertEqual(len(retargeted), 1)
        self.assertEqual(retargeted[0]["record_id"], "n3")
        self.assertEqual(
            self.report.names[retargeted[0]["target"]], "nu:response#k7->rival"
        )
        # The attacked validity node is refuted, which is what disables W_k7.
        self.assertEqual(self.report.labels[retargeted[0]["target"]], "refuted")

    def test_intra_document_criticism_of_criticism_is_a_declared_exception(self):
        """o4 criticises o1/o2, which this import reified. It is NOT retargeted."""
        entries = [
            e for e in self.report.residue
            if e["code"] == "criticism_of_criticism_intra_document_dropped"
        ]
        self.assertEqual([e["record_id"] for e in entries], ["o4", "o4"])
        for entry in entries:
            self.assertIn("SELF-attack", entry["detail"])
            self.assertIn("carrier closure", entry["detail"])
        # o4 minted nothing at all, and no warrant targets a nu carried by the
        # objection artifact itself.
        self.assertNotIn("o4", [w["record_id"] for w in self.report.warrants])
        objection = self.report.spec_id_table["daily/mini_fcl/cycle01/objection"]
        self.assertNotIn((objection, objection), self.report.att_edges)
        deviation = next(
            d for d in self.report.deviations
            if d["code"] == "criticism_of_criticism_intra_document_dropped"
        )
        self.assertIn("ONE exception", deviation["what"])

    def test_every_claim_record_is_reported_as_unmapped(self):
        claims = [e for e in self.report.residue if e["code"] == "claim_record_unmapped"]
        self.assertEqual(len(claims), 15)
        self.assertEqual(RESIDUE_CODES["claim_record_unmapped"]["severity"], "unmapped")
        self.assertEqual(RESIDUE_CODES["claim_record_unmapped"]["unit"], "record")
        # The three the uptake codes really do not cover.
        rival_claims = sorted(
            e["record_id"] for e in claims
            if e["coordinate"]["node"] == "rival"
        )
        self.assertEqual(rival_claims, ["r1", "r2", "r3", "r4"])
        uptake = json.loads(
            (OCCURRENCE / "artifacts/daily/mini_fcl/cycle01/rival.json").read_text(
                encoding="utf-8"
            )
        )["commitments"]
        self.assertEqual(
            [r for r in ("r1", "r3", "r4") if r in json.loads(uptake)["uptake"]], []
        )

    def test_references_resolve_eighty_two_of_eighty_four(self):
        self.assertEqual(
            self.report.resolution,
            {"refs": 84, "resolved": 82, "extensions": 2, "dangling": 0, "task": 0},
        )

    def test_no_warrant_carries_a_verdict_or_a_commitment(self):
        for warrant in self.report.warrants:
            self.assertEqual(warrant["type"], "argumentative")
            self.assertIsNone(warrant["verdict"])
            self.assertIsNone(warrant["commitment"])

    def test_every_artifact_in_the_written_root_has_provenance_role_import(self):
        harness = Harness(self.root, upto_seq=self.report.events_count - 1, read_only=True)
        roles = {
            artifact.provenance.role.value for artifact in harness.state.artifacts.values()
        }
        self.assertEqual(roles, {"import"})
        self.assertEqual(len(harness.state.artifacts), 17)
        # Including the validity nodes, which are transcription, not criticism
        # this process performed.
        for warrant in self.report.warrants:
            nu = harness.state.artifacts[warrant["validity_node"]]
            self.assertEqual(nu.provenance.role.value, "import")

    def test_commitment_eval_is_outside_every_executable_class(self):
        self.assertEqual(len(self.report.commitments), 4)
        for commitment in self.report.commitments:
            self.assertTrue(commitment["observation_valued"])
            self.assertTrue(commitment["eval"].startswith("observation:h005.fcl1@"))
            for executable in ("program:", "rubric:", "predicate:"):
                self.assertFalse(commitment["eval"].startswith(executable))

    def test_research_problems_have_empty_criteria_and_name_their_commitment(self):
        harness = Harness(self.root, upto_seq=self.report.events_count - 1, read_only=True)
        research = [p for p in harness.state.problems.values() if ".research:" in p.id]
        self.assertEqual(len(research), 4)
        for problem in research:
            self.assertEqual(list(problem.criteria), [])
            self.assertEqual(problem.provenance.trigger.value, "research")
            self.assertEqual(len(problem.provenance.from_), 2)
            self.assertTrue(problem.provenance.from_[1].startswith("k:h005.fcl1:"))

    def test_residue_totals_match_the_corrected_contract(self):
        self.assertEqual(self.report.residue_totals, EXPECTED_RESIDUE)
        for entry in self.report.residue:
            self.assertIn(
                entry["unit"],
                ("ref", "record", "document", "edge", "artifact", "problem", "file"),
            )
        dropped = [e for e in self.report.residue if e["code"] == "depends_intra_document"]
        self.assertEqual(
            sorted(entry["record_id"] for entry in dropped),
            ["k5", "k5", "k5", "k8", "n4", "n4", "n7", "n7", "r10", "r11",
             "r3", "r4", "r6", "r7", "r7", "r8", "r8"],
        )
        self.assertEqual(
            [e["record_id"] for e in self.report.residue
             if e["code"] == "objection_self_target_only"],
            ["o4"],
        )
        self.assertEqual(
            sorted(e["record_id"] for e in self.report.residue
                   if e["code"] == "objection_target_self_ref_dropped"),
            ["k7", "o4", "o4", "o4"],
        )
        self.assertEqual(
            sorted(e["record_id"] for e in self.report.residue
                   if e["code"] == "commitment_record_not_in_uptake"),
            ["r10", "r11"],
        )
        self.assertEqual(
            len([e for e in self.report.residue if e["code"].startswith("uptake_")]), 37
        )

    def test_every_residue_carrier_in_scope_names_its_spec_artifact(self):
        table = set(self.report.spec_id_table.values())
        seen = 0
        for entry in self.report.residue:
            coordinate = entry["coordinate"]
            if coordinate is None:
                continue
            key = Coordinate.from_dict(coordinate).key
            self.assertIn(key, self.report.spec_id_table)
            self.assertIsNotNone(entry["spec_artifact_id"], entry["code"])
            self.assertIn(entry["spec_artifact_id"], table)
            self.assertEqual(entry["spec_artifact_id"], self.report.spec_id_table[key])
            seen += 1
        self.assertGreater(seen, 100)
        written = json.loads((self.root / "residue.json").read_text(encoding="utf-8"))
        for entry in written["entries"]:
            carrier = entry["carrier"]
            if carrier is None:
                continue
            self.assertIsNotNone(carrier["spec_artifact_id"], entry["code"])
            self.assertIn(carrier["spec_artifact_id"], table)

    def test_self_targeting_objection_minted_nothing(self):
        minted = sorted(w["record_id"] for w in self.report.warrants)
        self.assertEqual(minted, ["k3", "k7", "n3", "n3", "o1", "o2", "o3"])
        self.assertNotIn("o4", minted)

    def test_the_fcl_document_is_its_own_artifact_mentioned_by_the_node(self):
        harness = Harness(self.root, upto_seq=self.report.events_count - 1, read_only=True)
        account = harness.state.artifacts[
            self.report.spec_id_table["daily/mini_fcl/cycle01/account"]
        ]
        document_id = next(
            aid for aid, name in self.report.names.items()
            if name == "daily/mini_fcl/cycle01/account#commitments"
        )
        document = harness.state.artifacts[document_id]
        self.assertEqual(document.codec, "json")
        self.assertEqual(document.interface, Interface())
        self.assertEqual(
            document.content_ref,
            json.loads(
                (OCCURRENCE / "artifacts/daily/mini_fcl/cycle01/account.json").read_text(
                    encoding="utf-8"
                )
            )["commitments_sha256"],
        )
        self.assertIn(
            (document_id, "mention"),
            [(ref.target, ref.role.value) for ref in account.interface.refs],
        )
        self.assertEqual(
            json.loads(harness.blobs.get(document.content_ref).decode("utf-8"))["language"],
            "FCL-1",
        )

    def test_carriage_lives_in_the_harness_relation_only(self):
        harness = Harness(self.root, upto_seq=self.report.events_count - 1, read_only=True)
        for warrant in self.report.warrants:
            self.assertIn(warrant["id"], harness.carried_warrant_ids(warrant["carrier"]))
            self.assertEqual(list(harness.state.artifacts[warrant["carrier"]].warrants), [])
        self.assertEqual(len(harness.state.carries), 7)

    def test_event_log_has_no_wall_clock_and_no_llm_call(self):
        events = [
            json.loads(line)
            for line in (self.root / "log.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        self.assertEqual(len(events), self.report.events_count)
        self.assertEqual(len(events), 38)
        self.assertEqual([e["seq"] for e in events], list(range(len(events))))
        stamps = {
            json.loads(
                (OCCURRENCE / "responses/daily/mini_fcl/cycle01" / f"{node}.json").read_text(
                    encoding="utf-8"
                )
            )["finished_utc"]
            for node in ("account", "objection", "rival", "response", "carry")
        }
        for event in events:
            self.assertIsNone(event["llm"])
            self.assertIn(event["ts"], stamps)
        self.assertEqual([e["ts"] for e in events], sorted(e["ts"] for e in events))
        self.assertIs(self.report.custody["event_ts_nondecreasing"], True)
        # Registration API only: no forged terminal Adj event.
        self.assertEqual(sorted({e["rule"] for e in events}), ["Crit", "Register", "Spawn"])
        self.assertEqual(events[0]["rule"], "Spawn")
        self.assertEqual(events[-1]["rule"], "Crit")

    def test_custody_is_split_and_counted_per_check(self):
        custody = self.report.custody
        self.assertEqual(
            custody["plan_id"],
            json.loads((OCCURRENCE / "plan.json").read_text(encoding="utf-8"))["plan_id"],
        )
        self.assertTrue(custody["manifests"]["fork5"]["verified"])
        cross = {c["key"]: c for c in custody["cross_file"]}
        internal = {c["key"]: c for c in custody["self_consistency"]}
        self.assertIn("trace_pinned", cross)
        self.assertIn("request_record", cross)
        self.assertIn("provider_bytes", cross)
        self.assertIn("receipt_present", cross)
        self.assertIn("plan_identity", internal)
        self.assertIn("brief_pinned", internal)
        self.assertNotIn("plan_identity", cross)
        for key in ("receipt_present", "request_record", "trace_pinned", "provider_bytes"):
            self.assertEqual((cross[key]["ran"], cross[key]["total"]), (5, 5), key)
            self.assertEqual(cross[key]["result"], "verified (5/5 nodes)")
        # trace_pinned is a cross-file claim only where the request record that
        # carries the trace hash is itself pinned; here every node has both an
        # attempt and a receipt, so it really did run 5/5.
        self.assertEqual(cross["trace_pinned"]["skipped"], [])
        self.assertIn("only where the request record is itself pinned",
                      cross["trace_pinned"]["check"])
        # projection_source counts projections, not nodes: one checkable slot
        # used to make a whole node read as verified.
        projections = cross["projection_source"]
        self.assertEqual(projections["unit"], "projection")
        self.assertEqual((projections["ran"], projections["total"]), (8, 10))
        self.assertEqual(
            projections["result"],
            "verified (8/10 projections; 2 projection(s) had no exposed source (the slot "
            "is absent): `daily/mini_fcl/cycle01/account#p.account.0`, "
            "`daily/mini_fcl/cycle01/carry#p.carry.3`)",
        )
        for relative, digest in custody["files"].items():
            self.assertEqual(
                hashlib.sha256((OCCURRENCE / relative).read_bytes()).hexdigest(), digest
            )
        # The request records and provider call bytes are now read.
        self.assertIn("requests/daily/mini_fcl/cycle01/carry.json", custody["files"])
        self.assertIn(
            "provider/daily/mini_fcl/cycle01/carry/call-0001.response.json", custody["files"]
        )
        markdown = (self.root / "REPORT.md").read_text(encoding="utf-8")
        self.assertIn("### Cross-file custody", markdown)
        self.assertIn("### Internal consistency only", markdown)
        self.assertIn("| event ts nondecreasing | yes |", markdown)

    def test_why_for_the_rival_names_the_reinstating_attacker(self):
        text = self.report.why("daily/mini_fcl/cycle01/rival")
        self.assertIn("accepted", text.splitlines()[2])
        self.assertIn("reinstating attacker: daily/mini_fcl/cycle01/carry", text)
        self.assertIn("attacked by daily/mini_fcl/cycle01/response", text)
        self.assertIn("w:h005.fcl1:daily/mini_fcl/cycle01/carry#n3", text)
        self.assertIn("Lemma 3.1", text)
        self.assertIn("No label produced by this import is a semantic attribution", text)
        rival = self.report.spec_id_table["daily/mini_fcl/cycle01/rival"]
        self.assertEqual(self.report.why(rival), text)

    def test_accept_by_position_never_says_nothing_criticised_it(self):
        carry = self.report.why("daily/mini_fcl/cycle01/carry")
        self.assertIn("no warrant in this import targets it", carry)
        self.assertIn(
            "the absence of an attacker is not evidence that the contribution was "
            "uncriticised",
            carry,
        )
        markdown = (self.root / "REPORT.md").read_text(encoding="utf-8")
        for text in (markdown, json.dumps(self.report.as_dict(), ensure_ascii=False)):
            self.assertNotIn("nothing criticised it", text)
            self.assertNotIn("nothing criticises it", text)

    def test_why_for_the_attacked_validity_node_explains_the_closure(self):
        nu = next(
            aid for aid, name in self.report.names.items()
            if name == "nu:response#k7->rival"
        )
        text = self.report.why(nu)
        self.assertIn("refuted", text.splitlines()[2])
        self.assertIn("closure", text)
        self.assertIn("daily/mini_fcl/cycle01/carry", text)

    def test_report_files_are_written_and_self_consistent(self):
        for name in ("REPORT.md", "report.json", "residue.json", "side_table.json"):
            self.assertTrue((self.root / name).is_file(), name)
        written = json.loads((self.root / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(written, json.loads(self.report.to_json()))
        residue = json.loads((self.root / "residue.json").read_text(encoding="utf-8"))
        self.assertEqual(residue["totals"], EXPECTED_RESIDUE)
        self.assertEqual(len(residue["entries"]), sum(EXPECTED_RESIDUE.values()))
        side = json.loads((self.root / "side_table.json").read_text(encoding="utf-8"))
        self.assertEqual(len(side["records"]), 42)
        self.assertEqual(len(side["validity_nodes"]), 7)
        self.assertEqual(len(side["documents"]), 5)
        for row in side["artifacts"]:
            self.assertIn(row["commitment_surface_state"], COMMITMENT_SURFACE_STATES)
            self.assertEqual(row["commitment_surface_state"], "read_fcl1")
            self.assertNotIn("opaque_reason", row)
        markdown = (self.root / "REPORT.md").read_text(encoding="utf-8")
        self.assertIn("No label produced by this import is a semantic attribution", markdown)
        self.assertIn("PROTOCOL.md §Interpretation", markdown)
        self.assertIn("standing inside the imported attack relation", markdown)
        # Single-arm scope: no multi-arm framing paragraph.
        self.assertIsNone(self.report.multi_arm_framing)
        self.assertNotIn("Any cross-arm reading is root's", markdown)
        # Every declared deviation carries its count in this scope, or says it
        # did not fire; none is stated as though it always applies.
        for deviation in self.report.deviations:
            count = self.report.residue_totals[deviation["code"]]
            suffix = (
                f"({count} in this scope)" if count else "**(not triggered in this scope)**"
            )
            self.assertIn(f"**`{deviation['code']}`** {suffix}", markdown)
        # No error-severity residue here, so no error banner.
        self.assertEqual(self.report.error_severity_totals, {})
        self.assertNotIn("Error-severity residue fired", markdown)
        # dep is empty because every depends ref was document-local.
        self.assertIn("were document-local", markdown)
        self.assertIn("not a result about the occurrence", markdown)


class FullOccurrenceTest(unittest.TestCase):
    """All five arms: custody and projection residue run for every node."""

    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory(prefix="h005-import-full-")
        cls.root = Path(cls.directory.name) / "graph"
        cls.report = import_occurrence(OCCURRENCE, cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def test_scope_and_shape(self):
        self.assertEqual(len(self.report.spec_id_table), 17)
        self.assertEqual(len(self.report.labels), 29)
        self.assertEqual(self.report.events_count, 50)
        counts = {}
        for status in self.report.labels.values():
            counts[status] = counts.get(status, 0) + 1
        self.assertEqual(counts, {"accepted": 26, "refuted": 3})

    def test_custody_ran_for_every_node_not_only_the_parsed_ones(self):
        custody = self.report.custody
        internal = {c["key"]: c for c in custody["self_consistency"]}
        cross = {c["key"]: c for c in custody["cross_file"]}
        for key in ("brief_pinned", "brief_label_index", "task_label", "artifact_self_hash"):
            self.assertEqual((internal[key]["ran"], internal[key]["total"]), (17, 17), key)
        for key in ("receipt_present", "request_record", "trace_pinned", "provider_bytes"):
            self.assertEqual((cross[key]["ran"], cross[key]["total"]), (17, 17), key)
        projections = cross["projection_source"]
        self.assertEqual(projections["unit"], "projection")
        self.assertEqual((projections["ran"], projections["total"]), (16, 20))
        # The four slots the check could not run over are named, not folded
        # into the node count.
        self.assertEqual(
            sorted(entry["subject"] for entry in projections["skipped"]),
            [
                "daily/mini_fcl/cycle01/account#p.account.0",
                "daily/mini_fcl/cycle01/carry#p.carry.3",
                "daily/mini_prose/cycle01/account#p.account.0",
                "daily/mini_prose/cycle01/carry#p.carry.3",
            ],
        )
        for entry in projections["skipped"]:
            self.assertEqual(entry["missing"], "exposed source (the slot is absent)")

    def test_projection_residue_runs_for_every_node(self):
        totals = self.report.residue_totals
        self.assertEqual(totals["projection_absent"], 4)
        self.assertEqual(totals["projection_exposed_unreferenced"], 10)
        unread = [
            e for e in self.report.residue
            if e["code"] == "projection_exposed_unreferenced"
            and e["coordinate"]["arm"] != "mini_fcl"
        ]
        self.assertTrue(unread)
        for entry in unread:
            self.assertIn("commitment surface was not read", entry["detail"])

    def test_opaque_and_prose_surfaces_are_counted_and_attributed(self):
        totals = self.report.residue_totals
        self.assertEqual(totals["opaque_envelope"], 2)
        self.assertEqual(totals["prose_commitment_surface"], 10)
        self.assertEqual(totals["parse_failure"], 0)
        self.assertEqual(totals["schema_failure"], 0)
        states = {}
        for aid, state in self.report.commitment_surface_states.items():
            states[state] = states.get(state, 0) + 1
        self.assertEqual(
            states,
            {"read_fcl1": 5, "prose_not_parsed": 10, "unavailable_decode_failure": 2},
        )
        opaque = [e for e in self.report.residue if e["code"] == "opaque_envelope"]
        self.assertEqual(
            sorted(e["coordinate"]["node"] for e in opaque), ["carry", "response"]
        )
        for entry in opaque:
            self.assertEqual(entry["coordinate"]["arm"], "matched")
            self.assertIn("strict JSON decode", entry["detail"])
            self.assertIn(
                "docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md",
                entry["detail"],
            )
            self.assertIn("UNAVAILABLE, not absent", entry["detail"])
            self.assertIn("not evidence", entry["detail"])
            self.assertIn("declined to commit", entry["detail"])
        prose = next(e for e in self.report.residue if e["code"] == "prose_commitment_surface")
        self.assertIn("artifact IS", prose["detail"])
        self.assertIn("accepted by position", prose["detail"])
        self.assertIn("no information about the arm", prose["detail"])

    def test_the_multi_arm_framing_paragraph_is_emitted_twice(self):
        framing = self.report.multi_arm_framing
        self.assertIsNotNone(framing)
        # The arms are the ones actually in this scope, spelled out.
        self.assertIn(
            "This scope contains 4 arms (bare, matched, mini_prose, native) whose declared "
            "commitment surface is prose and 1 arm (mini_fcl) whose surface is FCL-1.",
            framing,
        )
        self.assertIn(MULTI_ARM_FRAMING_TAIL, framing)
        self.assertIn("no refuted label can arise from a prose arm", framing)
        self.assertIn("Any cross-arm reading is root's, not this instrument's.", framing)
        markdown = (self.root / "REPORT.md").read_text(encoding="utf-8")
        self.assertEqual(markdown.count(framing), 2)
        what_it_is = markdown.index("## What this is, and what it is not")
        labels = markdown.index("| artifact | id | status | surface | attacked by | carries |")
        first, second = [
            index for index in range(len(markdown))
            if markdown.startswith(framing, index)
        ]
        self.assertLess(what_it_is, first)
        self.assertLess(first, markdown.index("## Custody"))
        self.assertLess(markdown.index("## Labels"), second)
        self.assertLess(second, labels)

    def test_the_opaque_nodes_why_chain_names_the_surface_state(self):
        for node in ("response", "carry"):
            aid = self.report.spec_id_table[f"daily/matched/cycle01/{node}"]
            text = self.report.why(aid)
            self.assertIn("commitment surface: UNAVAILABLE", text)
            self.assertIn("unavailable_decode_failure", text)
            self.assertIn("no warrant in this import targets it", text)
        prose = self.report.why(self.report.spec_id_table["daily/mini_prose/cycle01/rival"])
        self.assertIn("commitment surface: NOT READ (prose_not_parsed)", prose)
        read = self.report.why(self.report.spec_id_table["daily/mini_fcl/cycle01/rival"])
        self.assertNotIn("commitment surface:", read)

    def test_the_golden_labels_are_unchanged_by_the_other_arms(self):
        subset = {
            name: status
            for name, status in named_labels(self.report).items()
            if name.startswith("daily/mini_fcl/") or name.startswith("nu:")
        }
        self.assertEqual(subset, EXPECTED_LABELS)

    def test_the_labels_table_names_the_commitment_surface(self):
        """A status is only as informative as the surface it was computed over."""
        markdown = (self.root / "REPORT.md").read_text(encoding="utf-8")
        self.assertIn("| artifact | id | status | surface | attacked by | carries |", markdown)
        # The two matched-arm nodes whose commitments string was lost in
        # decoding: accepted, over a surface that was never available.
        for node in ("response", "carry"):
            row = labels_row(markdown, f"daily/matched/cycle01/{node}")
            self.assertIn("**accepted**", row)
            self.assertIn("| UNAVAILABLE (decode) |", row)
            aid = self.report.spec_id_table[f"daily/matched/cycle01/{node}"]
            self.assertEqual(self.report.surface_of(aid), "UNAVAILABLE (decode)")
        self.assertIn(
            "| NOT READ (prose) |", labels_row(markdown, "daily/mini_prose/cycle01/rival")
        )
        self.assertIn("| read |", labels_row(markdown, "daily/mini_fcl/cycle01/rival"))
        # An artifact with no commitment surface of its own says so.
        self.assertIn("| n/a |", labels_row(markdown, "nu:response#k7->rival"))
        self.assertIn(
            "| n/a |", labels_row(markdown, "daily/mini_fcl/cycle01/rival#commitments")
        )
        # The same four spellings in the plain-text table the CLI prints.
        table = self.report.labels_table()
        self.assertIn("artifact", table.splitlines()[0])
        self.assertIn("surface", table.splitlines()[0])
        for node, expected in (
            ("daily/matched/cycle01/carry", "UNAVAILABLE (decode)"),
            ("daily/mini_prose/cycle01/rival", "NOT READ (prose)"),
            ("daily/mini_fcl/cycle01/rival", "read"),
        ):
            line = next(l for l in table.splitlines() if l.startswith(node + " "))
            self.assertIn(expected, line)

    def test_a_narrowed_scope_names_only_the_arms_it_read(self):
        """The parentheticals are the scope's arms, not the occurrence's five."""
        with tempfile.TemporaryDirectory(prefix="h005-import-two-arms-") as directory:
            report = import_occurrence(
                OCCURRENCE, Path(directory) / "graph", dry_run=True, **MATCHED_SCOPE
            )
            framing = report.multi_arm_framing
            self.assertEqual(
                framing,
                "This scope contains 1 arm (matched) whose declared commitment surface is "
                "prose and 1 arm (mini_fcl) whose surface is FCL-1. "
                + MULTI_ARM_FRAMING_TAIL,
            )
            for absent in ("bare", "native", "mini_prose"):
                self.assertNotIn(absent, framing)

    def test_event_ts_is_not_monotone_and_the_report_says_why(self):
        self.assertIs(self.report.custody["event_ts_nondecreasing"], False)
        markdown = (self.root / "REPORT.md").read_text(encoding="utf-8")
        self.assertIn("| event ts nondecreasing | no -", markdown)
        self.assertIn("declared deviation", markdown)
        self.assertIn("never observed", markdown)


class ReceiptlessCoordinateTest(unittest.TestCase):
    """A coordinate with no receipt is admitted, and the report says so."""

    def test_a_missing_receipt_is_recorded_not_refused(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-noreceipt-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            # The LAST coordinate in registration order, so the ts rule has a
            # previous observed stamp to carry forward.
            for category, suffix in (("responses", "json"), ("responses", "txt"),
                                     ("attempts", "json")):
                (occurrence / category / "daily/mini_fcl/cycle01" / f"carry.{suffix}").unlink()
            root = Path(directory) / "graph"
            report = import_occurrence(occurrence, root, **SCOPE)

            cross = {c["key"]: c for c in report.custody["cross_file"]}
            self.assertEqual(
                cross["receipt_present"]["result"],
                "verified (4/5 nodes; 1 node(s) had no receipt: "
                "`daily/mini_fcl/cycle01/carry`)",
            )
            self.assertEqual(cross["receipt_present"]["ran"], 4)
            self.assertEqual(
                cross["receipt_present"]["skipped"],
                [{"subject": "daily/mini_fcl/cycle01/carry", "missing": "receipt"}],
            )
            for key in ("provider_bytes", "attempt_vs_receipt", "public_text"):
                self.assertEqual(cross[key]["ran"], 4, key)

            # The request record for `carry` is still there and its trace hash
            # still matches - but with neither an attempt nor a receipt, the
            # request record itself is pinned by nothing, so `trace_pinned` is
            # a self-consistency claim dressed as a cross-file one. It is
            # counted as NOT run, and the absent input is named.
            for key in ("request_record", "trace_pinned"):
                self.assertEqual((cross[key]["ran"], cross[key]["total"]), (4, 5), key)
                self.assertEqual(
                    cross[key]["skipped"],
                    [{
                        "subject": "daily/mini_fcl/cycle01/carry",
                        "missing": "attempt or receipt",
                    }],
                    key,
                )
                self.assertEqual(
                    cross[key]["result"],
                    "verified (4/5 nodes; 1 node(s) had no attempt or receipt: "
                    "`daily/mini_fcl/cycle01/carry`)",
                    key,
                )

            markdown = (root / "REPORT.md").read_text(encoding="utf-8")
            rows = [
                line for line in markdown.splitlines()
                if line.startswith("| ") and line.rstrip().endswith("|")
            ]
            plain = [row for row in rows if row.rstrip().endswith("| verified |")]
            self.assertEqual(plain, [], "a custody row still claims a plain 'verified'")
            self.assertIn("had no receipt: `daily/mini_fcl/cycle01/carry`", markdown)

            side = json.loads((root / "side_table.json").read_text(encoding="utf-8"))
            row = next(
                a for a in side["artifacts"] if a["coordinate"]["node"] == "carry"
            )
            self.assertEqual(
                sorted(row["absent_inputs"]),
                [
                    "attempts/daily/mini_fcl/cycle01/carry.json",
                    "responses/daily/mini_fcl/cycle01/carry.json",
                ],
            )
            self.assertIsNone(row["provider_receipt"])
            # Admitted, registered, labelled - not refused.
            self.assertEqual(named_labels(report), EXPECTED_LABELS)

    def test_a_scope_whose_first_coordinate_has_no_receipt_is_refused(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-leading-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            (occurrence / "responses/daily/mini_fcl/cycle01/account.json").unlink()
            root = Path(directory) / "graph"
            with self.assertRaises(CustodyError) as caught:
                import_occurrence(occurrence, root, **SCOPE)
            self.assertIn("NO_LEADING_RECEIPT", str(caught.exception))
            self.assertFalse(root.exists())


class TracePinningTest(unittest.TestCase):
    def test_one_tampered_selected_source_field_is_refused_before_any_write(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-trace-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            path = occurrence / "traces/daily/mini_fcl/cycle01/rival.json"
            trace = json.loads(path.read_text(encoding="utf-8"))
            source = trace["projection_artifacts"][0]["selected_source"]
            original = source["body_sha256"]
            source["body_sha256"] = "0" * 64
            self.assertNotEqual(original, source["body_sha256"])
            path.write_text(
                json.dumps(trace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            root = Path(directory) / "graph"
            with self.assertRaises(CustodyError) as caught:
                import_occurrence(occurrence, root, **SCOPE)
            # Caught by the trace pin, not by a lazy check during resolution.
            self.assertIn("TRACE_NOT_PINNED", str(caught.exception))
            self.assertIn("daily/mini_fcl/cycle01/rival", str(caught.exception))
            self.assertFalse(root.exists())

    def test_a_tampered_request_record_is_refused(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-request-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            path = occurrence / "requests/daily/mini_fcl/cycle01/response.json"
            request = json.loads(path.read_text(encoding="utf-8"))
            request["template_id"] = request["template_id"] + "-tampered"
            path.write_text(
                json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            root = Path(directory) / "graph"
            with self.assertRaises(CustodyError) as caught:
                import_occurrence(occurrence, root, **SCOPE)
            self.assertIn("REQUEST_RECORD_MISMATCH", str(caught.exception))
            self.assertFalse(root.exists())

    def test_tampered_provider_bytes_are_refused(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-provider-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            path = (
                occurrence
                / "provider/daily/mini_fcl/cycle01/objection/call-0001.response.json"
            )
            raw = bytearray(path.read_bytes())
            raw[32] ^= 0x01
            path.write_bytes(bytes(raw))
            root = Path(directory) / "graph"
            with self.assertRaises(CustodyError) as caught:
                import_occurrence(occurrence, root, **SCOPE)
            self.assertIn("PROVIDER_BYTES_CHANGED", str(caught.exception))
            self.assertFalse(root.exists())


class RequestRecordTest(unittest.TestCase):
    """The trace's only pin. No request record, no import."""

    def test_a_missing_request_record_is_refused(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-norequest-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            (occurrence / "requests/daily/mini_fcl/cycle01/carry.json").unlink()
            root = Path(directory) / "graph"
            with self.assertRaises(CustodyError) as caught:
                import_occurrence(occurrence, root, **SCOPE)
            self.assertIn(
                "REQUEST_RECORD_MISSING:daily/mini_fcl/cycle01/carry", str(caught.exception)
            )
            self.assertFalse(root.exists())
            self.assertEqual(sorted(p.name for p in Path(directory).iterdir()), ["occurrence"])

    def test_every_coordinate_in_the_occurrence_has_one(self):
        """The refusal above costs nothing here: all 22 request records exist."""
        requests = {
            str(path.relative_to(OCCURRENCE / "requests"))
            for path in (OCCURRENCE / "requests").rglob("*.json")
        }
        artifacts = {
            str(path.relative_to(OCCURRENCE / "artifacts"))
            for path in (OCCURRENCE / "artifacts").rglob("*.json")
        }
        self.assertEqual(len(requests), 22)
        self.assertEqual(artifacts - requests, set())


class ProviderBytesTest(unittest.TestCase):
    """A non-FAILED receipt must have both provider hashes AND both call files."""

    def test_a_deleted_provider_call_file_is_refused(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-nocall-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            (
                occurrence
                / "provider/daily/mini_fcl/cycle01/rival/call-0001.response.json"
            ).unlink()
            root = Path(directory) / "graph"
            with self.assertRaises(CustodyError) as caught:
                import_occurrence(occurrence, root, **SCOPE)
            self.assertIn(
                "PROVIDER_HASH_MISSING:daily/mini_fcl/cycle01/rival:response",
                str(caught.exception),
            )
            self.assertFalse(root.exists())

    def test_a_nulled_provider_hash_is_refused(self):
        """None == None must never satisfy a byte check."""
        with tempfile.TemporaryDirectory(prefix="h005-import-nullhash-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            path = occurrence / "responses/daily/mini_fcl/cycle01/rival.json"
            receipt = json.loads(path.read_text(encoding="utf-8"))
            self.assertNotEqual(receipt["status"], "FAILED")
            self.assertIsInstance(receipt["provider_request_sha256"], str)
            receipt["provider_request_sha256"] = None
            path.write_text(
                json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            # The matching call file is left in place: the old check compared
            # None to None when both were missing, and this half of the pair
            # is what a rewriter would null first.
            root = Path(directory) / "graph"
            with self.assertRaises(CustodyError) as caught:
                import_occurrence(occurrence, root, **SCOPE)
            self.assertIn(
                "PROVIDER_HASH_MISSING:daily/mini_fcl/cycle01/rival:request",
                str(caught.exception),
            )
            self.assertFalse(root.exists())


class ReplayStabilityTest(unittest.TestCase):
    def test_two_imports_are_byte_identical_across_hash_seeds(self):
        """The second root is built in a subprocess with a different PYTHONHASHSEED.

        Determinism inside one process proves only that the code is a function
        of its inputs; it does not prove the output is independent of Python's
        per-process string hash randomisation, which is what would silently
        reorder a set iteration.
        """
        with tempfile.TemporaryDirectory(prefix="h005-import-replay-") as directory:
            first = Path(directory) / "one"
            second = Path(directory) / "two"
            report_one = import_occurrence(OCCURRENCE, first, **SCOPE)

            environment = dict(os.environ)
            environment.setdefault("PYTHONPATH", os.pathsep.join(sys.path[1:]))
            environment["PYTHONHASHSEED"] = "12345"
            self.assertNotEqual(
                environment["PYTHONHASHSEED"], str(os.environ.get("PYTHONHASHSEED"))
            )
            completed = subprocess.run(
                [
                    sys.executable, "-X", "utf8", "-c",
                    "import sys;from pathlib import Path;"
                    "from minireason.graph_import_h005 import import_occurrence;"
                    "r=import_occurrence(Path(sys.argv[1]),Path(sys.argv[2]),"
                    "problems=['daily'],arms=['mini_fcl'],cycles=[1]);"
                    "print(r.events_count)",
                    str(OCCURRENCE), str(second),
                ],
                capture_output=True, text=True, env=environment,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(completed.stdout.strip(), str(report_one.events_count))

            self.assertEqual(
                (first / "log.jsonl").read_bytes(), (second / "log.jsonl").read_bytes()
            )
            self.assertEqual(tree_hashes(first / "objects"), tree_hashes(second / "objects"))
            self.assertEqual(tree_hashes(first / "blobs"), tree_hashes(second / "blobs"))
            for name in ("REPORT.md", "report.json", "residue.json", "side_table.json"):
                self.assertTrue(filecmp.cmp(first / name, second / name, shallow=False), name)

    def test_out_root_is_write_once(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-once-") as directory:
            root = Path(directory) / "graph"
            import_occurrence(OCCURRENCE, root, **SCOPE)
            with self.assertRaises(FileExistsError):
                import_occurrence(OCCURRENCE, root, **SCOPE)
            with self.assertRaises(OutRootRefused):
                import_occurrence(OCCURRENCE, root, **SCOPE)


class AtomicOutRootTest(unittest.TestCase):
    """Either the whole root appears, or nothing does - for every failure kind."""

    def test_a_late_mapping_error_leaves_no_out_root_and_no_temp_directory(self):
        import minireason.graph_import_h005 as library

        def refuse(harness, importer):
            # As late as a failure can be: the log, the objects and the blobs
            # are all written by now. Before the temp-directory build this
            # left a graph root with a log and no report behind.
            raise MappingError("SYNTHETIC_LATE_FAILURE")

        original = library._verify_event_log
        library._verify_event_log = refuse
        try:
            with tempfile.TemporaryDirectory(prefix="h005-import-atomic-") as directory:
                root = Path(directory) / "graph"
                with self.assertRaises(MappingError) as caught:
                    import_occurrence(OCCURRENCE, root, **SCOPE)
                self.assertIn("SYNTHETIC_LATE_FAILURE", str(caught.exception))
                self.assertFalse(root.exists())
                # ... and no half-built sibling left lying next to it.
                self.assertEqual(sorted(Path(directory).iterdir()), [])
        finally:
            library._verify_event_log = original

    def test_a_successful_import_leaves_only_the_root(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-atomic-ok-") as directory:
            root = Path(directory) / "graph"
            import_occurrence(OCCURRENCE, root, **SCOPE)
            self.assertEqual([p.name for p in sorted(Path(directory).iterdir())], ["graph"])
            for name in ("log.jsonl", "REPORT.md", "report.json", "residue.json",
                         "side_table.json"):
                self.assertTrue((root / name).is_file(), name)

    def test_an_existing_out_root_is_refused_before_any_work(self):
        """Write-once, decided before the occurrence is opened at all."""
        import minireason.graph_import_h005 as library

        def refuse(reader, ledger):
            raise AssertionError("custody must not run for a refused out-root")

        original = library.verify_custody
        library.verify_custody = refuse
        try:
            with tempfile.TemporaryDirectory(prefix="h005-import-once-early-") as directory:
                root = Path(directory) / "graph"
                root.mkdir()
                marker = root / "keep-me"
                marker.write_text("untouched", encoding="utf-8")
                with self.assertRaises(OutRootRefused) as caught:
                    import_occurrence(OCCURRENCE, root, **SCOPE)
                self.assertIn("OUT_ROOT_EXISTS", str(caught.exception))
                self.assertEqual(marker.read_text(encoding="utf-8"), "untouched")
                self.assertEqual(
                    [p.name for p in sorted(Path(directory).iterdir())], ["graph"]
                )
        finally:
            library.verify_custody = original


class PathContainmentTest(unittest.TestCase):
    """No composed path may address bytes outside the occurrence (I1)."""

    def test_an_unsafe_coordinate_component_is_refused(self):
        for raw, component in (
            ({"problem": "../../etc", "arm": "mini_fcl", "cycle": 1, "node": "rival"},
             "problem"),
            ({"problem": "daily", "arm": "..", "cycle": 1, "node": "rival"}, "arm"),
            ({"problem": "daily", "arm": "mini_fcl", "cycle": 1, "node": "a/b"}, "node"),
            ({"problem": "daily", "arm": "mini_fcl", "cycle": 1, "node": "rival.json"},
             "node"),
        ):
            with self.subTest(component=component, raw=raw):
                with self.assertRaises(CustodyError) as caught:
                    Coordinate.from_dict(raw)
                self.assertIn("COORDINATE_COMPONENT_UNSAFE:" + component,
                              str(caught.exception))
        # The occurrence's own coordinates are of course fine.
        self.assertEqual(
            Coordinate.from_dict(
                {"problem": "daily", "arm": "mini_fcl", "cycle": 1, "node": "rival"}
            ).key,
            "daily/mini_fcl/cycle01/rival",
        )

    def test_a_wave_id_that_is_not_a_wave_id_is_refused(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-waveid-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            path = occurrence / "waves/wave0001.json"
            wave = json.loads(path.read_text(encoding="utf-8"))
            wave["wave_id"] = "not-a-wave"
            path.write_text(
                json.dumps(wave, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            root = Path(directory) / "graph"
            with self.assertRaises(CustodyError) as caught:
                import_occurrence(occurrence, root, **SCOPE)
            self.assertIn("WAVE_ID_MALFORMED:wave0001.json", str(caught.exception))
            self.assertFalse(root.exists())

    def test_the_reader_refuses_a_path_that_escapes_the_occurrence(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-escape-") as directory:
            root = Path(directory) / "occurrence"
            (root / "artifacts").mkdir(parents=True)
            (root / "artifacts" / "inside.json").write_text("{}", encoding="utf-8")
            (Path(directory) / "outside.json").write_text("{}", encoding="utf-8")
            reader = _Reader(root)
            self.assertEqual(reader.read_bytes("artifacts/inside.json"), b"{}")
            for escape in ("../outside.json", "artifacts/../../outside.json", "/etc/hostname"):
                with self.subTest(escape=escape):
                    with self.assertRaises(CustodyError) as caught:
                        reader.read_bytes(escape)
                    self.assertIn("PATH_ESCAPES_OCCURRENCE", str(caught.exception))
                    with self.assertRaises(CustodyError):
                        reader.exists(escape)
            # Nothing outside was hashed into the custody record.
            self.assertEqual(sorted(reader.files), ["artifacts/inside.json"])


class SelectorTest(unittest.TestCase):
    """A selector that matches nothing is an operator mistake, not a mapping failure."""

    def test_selectors_that_match_nothing_name_what_the_occurrence_holds(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-selector-") as directory:
            with self.assertRaises(SelectorMatchedNothing) as caught:
                import_occurrence(
                    OCCURRENCE, Path(directory) / "graph", dry_run=True,
                    problems=["daily"], arms=["mini_fcl_typo"], cycles=[7],
                )
            message = str(caught.exception)
            self.assertIn("SELECTOR_MATCHED_NOTHING", message)
            self.assertIn("--arm mini_fcl_typo", message)
            self.assertIn("--cycle 7", message)
            self.assertIn("arms: bare, matched, mini_fcl, mini_prose, native", message)
            self.assertIn("cycles: 1", message)
            self.assertIn("problems: daily", message)
            # It is a MappingError, so existing callers keep working - but a
            # distinct one, so the CLI can give it its own exit code.
            self.assertIsInstance(caught.exception, MappingError)
            self.assertEqual(sorted(Path(directory).iterdir()), [])

    def test_an_occurrence_with_no_coordinate_at_all_is_still_empty_scope(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-empty-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            shutil.rmtree(occurrence / "artifacts")
            (occurrence / "artifacts").mkdir()
            with self.assertRaises(MappingError) as caught:
                import_occurrence(occurrence, Path(directory) / "graph", dry_run=True)
            self.assertEqual(str(caught.exception), "EMPTY_SCOPE")
            self.assertNotIsInstance(caught.exception, SelectorMatchedNothing)


class CustodyRefusalTest(unittest.TestCase):
    def test_a_tampered_response_text_is_refused_before_any_write(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-custody-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            target = occurrence / "responses/daily/mini_fcl/cycle01/response.txt"
            raw = bytearray(target.read_bytes())
            raw[64] ^= 0x01
            target.write_bytes(bytes(raw))
            root = Path(directory) / "graph"
            with self.assertRaises(CustodyError) as caught:
                import_occurrence(occurrence, root, **SCOPE)
            self.assertIn("PUBLIC_TEXT_CHANGED", str(caught.exception))
            self.assertFalse(root.exists())

    def test_a_tampered_plan_is_refused(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-plan-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            plan = json.loads((occurrence / "plan.json").read_text(encoding="utf-8"))
            plan["max_calls"] = plan["max_calls"] + 1
            (occurrence / "plan.json").write_text(
                json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
            root = Path(directory) / "graph"
            with self.assertRaises(CustodyError) as caught:
                import_occurrence(occurrence, root, **SCOPE)
            self.assertIn("IMMUTABLE_PLAN_MISMATCH", str(caught.exception))
            self.assertFalse(root.exists())

    def test_a_missing_occurrence_file_is_a_custody_error(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-missing-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            (occurrence / "traces/daily/mini_fcl/cycle01/rival.json").unlink()
            root = Path(directory) / "graph"
            with self.assertRaises(CustodyError) as caught:
                import_occurrence(occurrence, root, **SCOPE)
            self.assertIn("OCCURRENCE_FILE_MISSING", str(caught.exception))
            self.assertFalse(root.exists())

    def test_malformed_occurrence_json_is_a_custody_error(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-malformed-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            (occurrence / "waves/wave0001.json").write_text("{not json", encoding="utf-8")
            root = Path(directory) / "graph"
            with self.assertRaises(CustodyError) as caught:
                import_occurrence(occurrence, root, **SCOPE)
            self.assertIn("OCCURRENCE_FILE_MALFORMED_JSON", str(caught.exception))
            self.assertFalse(root.exists())

    def test_a_malformed_material_file_is_a_custody_error_not_a_valueerror(self):
        """material.json used to be json.loads'd directly, outside the wrapper."""
        with tempfile.TemporaryDirectory(prefix="h005-import-material-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            raw = (occurrence / "material.json").read_bytes()
            (occurrence / "material.json").write_bytes(raw[: len(raw) // 2])
            root = Path(directory) / "graph"
            with self.assertRaises(CustodyError) as caught:
                import_occurrence(occurrence, root, **SCOPE)
            self.assertIn("OCCURRENCE_FILE_MALFORMED_JSON:material.json",
                          str(caught.exception))
            self.assertFalse(root.exists())

    def test_a_malformed_wave_file_is_a_custody_error(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-wavejson-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            (occurrence / "waves/wave0001.json").write_text("{\"wave_id\": ", encoding="utf-8")
            root = Path(directory) / "graph"
            with self.assertRaises(CustodyError) as caught:
                import_occurrence(occurrence, root, **SCOPE)
            self.assertIn("OCCURRENCE_FILE_MALFORMED_JSON:waves/wave0001.json",
                          str(caught.exception))
            self.assertFalse(root.exists())

    def test_the_re_implemented_digest_reproduces_the_recorded_plan_id(self):
        plan = json.loads((OCCURRENCE / "plan.json").read_text(encoding="utf-8"))
        stored = plan.pop("plan_id")
        self.assertEqual(study_digest(plan), stored)


class DryRunTest(unittest.TestCase):
    def test_dry_run_writes_nothing_and_agrees_with_the_written_import(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-dry-") as directory:
            dry_root = Path(directory) / "never-written"
            dry = import_occurrence(OCCURRENCE, dry_root, dry_run=True, **SCOPE)
            self.assertFalse(dry_root.exists())
            self.assertEqual(sorted(Path(directory).iterdir()), [])
            self.assertIsNone(dry.out_root)
            wet = import_occurrence(OCCURRENCE, Path(directory) / "graph", **SCOPE)
            self.assertEqual(dry.labels, wet.labels)
            self.assertEqual(dry.att_edges, wet.att_edges)
            self.assertEqual(dry.events_count, wet.events_count)
            self.assertEqual(dry.residue_totals, wet.residue_totals)
            self.assertEqual(dry.resolution, wet.resolution)


class OccurrenceIsReadOnlyTest(unittest.TestCase):
    def test_the_occurrence_bytes_are_untouched_by_an_import(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-readonly-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            before = tree_hashes(occurrence)
            import_occurrence(occurrence, Path(directory) / "graph", **SCOPE)
            self.assertEqual(tree_hashes(occurrence), before)

    def test_an_out_root_inside_the_occurrence_is_refused(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-inside-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            with self.assertRaises(ValueError):
                import_occurrence(occurrence, occurrence / "graph", **SCOPE)
            with self.assertRaises(OutRootRefused):
                import_occurrence(occurrence, occurrence / "graph", **SCOPE)


class CommandLineTest(unittest.TestCase):
    def test_a_successful_run_prints_the_i7_banner_before_the_labels(self):
        with tempfile.TemporaryDirectory(prefix="h005-cli-ok-") as directory:
            root = Path(directory) / "graph"
            done = run_cli(str(OCCURRENCE), str(root), "--problem", "daily",
                           "--arm", "mini_fcl", "--cycle", "1")
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertIn("I7: No label produced by this import is a semantic attribution",
                          done.stdout)
            self.assertLess(done.stdout.index("I7: No label"), done.stdout.index("LABELS"))
            self.assertIn("daily/mini_fcl/cycle01/account", done.stdout)
            self.assertIn("RESIDUE", done.stdout)
            self.assertTrue((root / "REPORT.md").is_file())

    def test_the_multi_arm_framing_is_printed_when_the_scope_spans_arms(self):
        with tempfile.TemporaryDirectory(prefix="h005-cli-arms-") as directory:
            done = run_cli(str(OCCURRENCE), str(Path(directory) / "graph"))
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertIn("Any cross-arm reading is root's, not this instrument's.",
                          done.stdout)
            self.assertLess(
                done.stdout.index("This scope contains 4 arms"),
                done.stdout.index("LABELS"),
            )

    def test_dry_run_leaves_no_out_root(self):
        with tempfile.TemporaryDirectory(prefix="h005-cli-dry-") as directory:
            root = Path(directory) / "graph"
            done = run_cli(str(OCCURRENCE), str(root), "--problem", "daily",
                           "--arm", "mini_fcl", "--cycle", "1", "--dry-run")
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertIn("dry run: nothing written", done.stdout)
            self.assertFalse(root.exists())
            self.assertEqual(sorted(Path(directory).iterdir()), [])

    def test_a_tampered_occurrence_exits_two_with_custody_refused(self):
        with tempfile.TemporaryDirectory(prefix="h005-cli-custody-") as directory:
            occurrence = copy_occurrence(Path(directory) / "occurrence")
            target = occurrence / "responses/daily/mini_fcl/cycle01/response.txt"
            raw = bytearray(target.read_bytes())
            raw[64] ^= 0x01
            target.write_bytes(bytes(raw))
            root = Path(directory) / "graph"
            done = run_cli(str(occurrence), str(root), "--problem", "daily",
                           "--arm", "mini_fcl", "--cycle", "1")
            self.assertEqual(done.returncode, 2)
            self.assertIn("CUSTODY_REFUSED", done.stderr)
            self.assertIn("PUBLIC_TEXT_CHANGED", done.stderr)
            self.assertFalse(root.exists())

    def test_an_unresolvable_why_still_exits_zero(self):
        with tempfile.TemporaryDirectory(prefix="h005-cli-why-") as directory:
            root = Path(directory) / "graph"
            done = run_cli(str(OCCURRENCE), str(root), "--problem", "daily",
                           "--arm", "mini_fcl", "--cycle", "1",
                           "--why", "daily/mini_fcl/cycle01/carrry")
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertIn("WHY_UNRESOLVED: daily/mini_fcl/cycle01/carrry", done.stderr)
            self.assertIn("daily/mini_fcl/cycle01/carry", done.stderr)
            self.assertIn("the import itself succeeded", done.stderr)
            # The import really did succeed.
            self.assertTrue((root / "REPORT.md").is_file())
            self.assertIn("LABELS", done.stdout)

    def test_a_resolvable_why_is_printed(self):
        with tempfile.TemporaryDirectory(prefix="h005-cli-why-ok-") as directory:
            done = run_cli(str(OCCURRENCE), str(Path(directory) / "graph"),
                           "--problem", "daily", "--arm", "mini_fcl", "--cycle", "1",
                           "--why", "daily/mini_fcl/cycle01/rival")
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertIn("Lemma 3.1", done.stdout)
            self.assertEqual(done.stderr, "")

    def test_an_out_root_that_exists_exits_four(self):
        with tempfile.TemporaryDirectory(prefix="h005-cli-outroot-") as directory:
            root = Path(directory) / "graph"
            root.mkdir()
            done = run_cli(str(OCCURRENCE), str(root), "--problem", "daily",
                           "--arm", "mini_fcl", "--cycle", "1")
            self.assertEqual(done.returncode, 4)
            self.assertIn("OUT_ROOT_REFUSED", done.stderr)

    def test_a_selector_that_matches_nothing_exits_five(self):
        with tempfile.TemporaryDirectory(prefix="h005-cli-selector-") as directory:
            root = Path(directory) / "graph"
            done = run_cli(str(OCCURRENCE), str(root), "--problem", "daily",
                           "--arm", "mini_fcl", "--cycle", "9")
            self.assertEqual(done.returncode, 5, done.stderr)
            self.assertIn("SELECTOR_MATCHED_NOTHING", done.stderr)
            self.assertIn("--cycle 9", done.stderr)
            self.assertIn("cycles: 1", done.stderr)
            # Not a custody refusal and not a mapping failure.
            self.assertNotIn("CUSTODY_REFUSED", done.stderr)
            self.assertNotIn("IMPORT_FAILED", done.stderr)
            self.assertFalse(root.exists())
            self.assertEqual(sorted(Path(directory).iterdir()), [])

    def test_the_labels_table_carries_a_surface_column(self):
        with tempfile.TemporaryDirectory(prefix="h005-cli-surface-") as directory:
            done = run_cli(str(OCCURRENCE), str(Path(directory) / "graph"))
            self.assertEqual(done.returncode, 0, done.stderr)
            header = done.stdout.splitlines()[done.stdout.splitlines().index("LABELS") + 1]
            self.assertIn("surface", header)
            row = next(
                line for line in done.stdout.splitlines()
                if line.startswith("daily/matched/cycle01/carry ")
            )
            self.assertIn("UNAVAILABLE (decode)", row)


# --------------------------------------------------------------------------- #
# synthetic scopes: paths the occurrence does not exercise                     #
# --------------------------------------------------------------------------- #


def synthetic_document(records, uptake=()):
    return {"language": "FCL-1", "records": list(records), "uptake": list(uptake)}


def synthetic_artifact_id(node_name: str) -> str:
    return hashlib.sha256(("h005-synthetic:" + node_name).encode()).hexdigest()


def label(node_name: str) -> str:
    """The exposed-artifact label a brief would carry for this synthetic node."""
    return synthetic_artifact_id(node_name)[:16]


def synthetic_node(importer, arm, node_name, document, *, index):
    """A hand-built node: enough state for map_records, no occurrence on disk."""
    coord = Coordinate("synthetic", arm, 1, node_name)
    commitments = json.dumps(document, ensure_ascii=False, sort_keys=True)
    body = f"body of {node_name}"
    digest = hashlib.sha256(body.encode()).hexdigest()
    record = {
        "schema": "minireason.h005.artifact.v1",
        "coordinate": coord.as_dict(),
        "artifact_id": synthetic_artifact_id(node_name),
        "body": body,
        "body_sha256": digest,
        "body_ref": digest,
        "commitments": commitments,
        "commitments_sha256": hashlib.sha256(commitments.encode()).hexdigest(),
        "commitments_ref": hashlib.sha256(commitments.encode()).hexdigest(),
        "public_text_sha256": digest,
        "delivery_status": "COMPLETE",
        "envelope_status": "OK",
    }
    built = _Node(
        coord=coord,
        record=record,
        trace={},
        receipt={"finished_utc": "2026-09-11T00:00:0%dZ" % index},
        attempt=None,
        absent_inputs=[],
        wave_id="wave0001",
        wave_ordinal=1,
        wave_index=index,
    )
    built.ts = built.receipt["finished_utc"]
    importer.nodes[coord] = built
    return built


def projection_to(node):
    return {
        "artifact_id": node.record["artifact_id"],
        "selected_source": {
            "source": "previous",
            "view": "both",
            "absent": False,
            "coordinate": node.coord.as_dict(),
            "artifact_id": node.record["artifact_id"],
            "body_sha256": node.record["body_sha256"],
            "commitments_sha256": node.record["commitments_sha256"],
        },
    }


def build_synthetic(nodes_spec, seed_dep=()):
    """Run the mapping over a hand-built scope; return (importer, labels, att, dep).

    ``nodes_spec`` is ``[(arm, node_name, document, [names it can see])]`` in
    registration order. Every node is built first, then the projections are
    attached, so a scope may declare a cycle. ``seed_dep`` pre-loads the
    mapper's own dependence-edge accumulator with ``(carrier_key, owner_key)``
    pairs - see the cycle test for why that is the only way to reach the guard.
    """
    importer = _Importer(Path("/nonexistent-synthetic-occurrence"), None, None, None)
    built = {}
    for index, (arm, name, document, _visible) in enumerate(nodes_spec):
        built[name] = synthetic_node(importer, arm, name, document, index=index)
    for _arm, name, _document, visible in nodes_spec:
        node = built[name]
        node.projections = [projection_to(built[other]) for other in visible]
        node.label_index = {
            projection["artifact_id"][:16]: position
            for position, projection in enumerate(node.projections)
        }
    importer.order = [built[name].coord for _a, name, _d, _v in nodes_spec]
    importer.first_ts = "2026-09-11T00:00:00Z"
    importer.last_ts = "2026-09-11T00:00:09Z"
    importer.dep_edges.extend(
        (built[carrier].coord.key, built[owner].coord.key) for carrier, owner in seed_dep
    )
    importer.parse_documents()
    importer.map_records()
    importer.plan_events({"problems": [{"id": "synthetic", "prose": "synthetic"}]})
    importer.report_edge_dedupe()
    importer.backfill_residue_carriers()
    labels, att, dep = importer.adjudicate_offline()
    return importer, labels, att, dep


class SyntheticDependenceTest(unittest.TestCase):
    """The occurrence has no cross-document `depends`; these paths still must work."""

    def test_a_cross_document_depends_makes_a_dep_edge_and_can_suspend(self):
        # beta objects to alpha (att beta->alpha, so alpha is refuted) and beta
        # also declares a cross-document dependence on alpha. Pass 1 accepts
        # beta; pass 2 finds its declared premise refuted, so beta is
        # suspended_unsupported - orphaned, not false.
        alpha = synthetic_document([{"id": "a1", "type": "claim", "text": "premise"}])
        beta = synthetic_document(
            [
                {"id": "b1", "type": "objection", "text": "the premise fails",
                 "bearing": "decisive", "target": [f"{label('alpha')}#a1"]},
                {"id": "b2", "type": "claim", "text": "built on the premise",
                 "depends": [f"{label('alpha')}#a1"]},
            ]
        )
        importer, labels, att, dep = build_synthetic(
            [
                ("mini_fcl", "alpha", alpha, []),
                ("mini_fcl", "beta", beta, ["alpha"]),
            ]
        )
        alpha_node = importer.nodes[Coordinate("synthetic", "mini_fcl", 1, "alpha")]
        beta_node = importer.nodes[Coordinate("synthetic", "mini_fcl", 1, "beta")]

        self.assertIn((beta_node.spec_id, alpha_node.spec_id), dep)
        self.assertEqual(
            [e["record_id"] for e in importer.residue
             if e["code"] == "depends_cross_document"],
            ["b2"],
        )
        dependence = [
            ref for ref in beta_node.interface.refs if ref.role.value == "dependence"
        ]
        self.assertEqual([ref.target for ref in dependence], [alpha_node.spec_id])
        self.assertEqual(labels[alpha_node.spec_id], "refuted")
        self.assertEqual(labels[beta_node.spec_id], "suspended_unsupported")
        why = importer.build_why(labels, att, dep)[beta_node.spec_id]
        self.assertIn("suspended_unsupported", why)
        self.assertIn("Orphaned != false", why)
        self.assertIn("declared dependence (dep):", why)

    def test_a_mutual_depends_cannot_even_be_expressed_in_registration_order(self):
        """Why the cycle guard cannot fire on a real occurrence, stated as a test.

        A ref is resolved against the projections exposed to its carrier, and a
        projection's source must already be registered; so every admitted `dep`
        edge points from a later coordinate to an earlier one, and the relation
        is acyclic by construction. The mutual-dependence half of the pair is
        not "rejected as a cycle" - it is dropped earlier, as a ref to an
        artifact that is not registered yet.
        """
        alpha = synthetic_document(
            [{"id": "a1", "type": "claim", "text": "a", "depends": [f"{label('beta')}#b1"]}]
        )
        beta = synthetic_document(
            [{"id": "b1", "type": "claim", "text": "b", "depends": [f"{label('alpha')}#a1"]}]
        )
        importer, labels, att, dep = build_synthetic(
            [
                ("mini_fcl", "alpha", alpha, ["beta"]),
                ("mini_fcl", "beta", beta, ["alpha"]),
            ]
        )
        self.assertEqual(len(dep), 1, dep)
        self.assertEqual(importer.residue_code_count("depends_cross_document"), 1)
        self.assertEqual(importer.residue_code_count("dependence_cycle_rejected"), 0)
        dropped = [
            e for e in importer.residue
            if e["code"] == "ref_to_unregistered_target_dropped"
        ]
        self.assertEqual([e["record_id"] for e in dropped], ["a1"])
        self.assertIn("is not registered yet", dropped[0]["reason"])

    def test_a_depends_that_would_close_a_cycle_is_rejected_and_reported(self):
        """The guard itself, driven with an edge already in the accumulator.

        `_would_cycle` is reached by seeding the mapper's dependence-edge
        accumulator with `alpha -> beta`; `beta`'s authored `depends` on
        `alpha` would then close the cycle, so it is refused and reported
        instead of being admitted and blowing up in `toposort` later.
        """
        alpha = synthetic_document([{"id": "a1", "type": "claim", "text": "a"}])
        beta = synthetic_document(
            [{"id": "b1", "type": "claim", "text": "b", "depends": [f"{label('alpha')}#a1"]}]
        )
        importer, labels, att, dep = build_synthetic(
            [
                ("mini_fcl", "alpha", alpha, []),
                ("mini_fcl", "beta", beta, ["alpha"]),
            ],
            seed_dep=[("alpha", "beta")],
        )
        self.assertEqual(dep, [])
        self.assertEqual(importer.residue_code_count("depends_cross_document"), 0)
        rejected = [e for e in importer.residue if e["code"] == "dependence_cycle_rejected"]
        self.assertEqual(len(rejected), 1)
        self.assertEqual(rejected[0]["record_id"], "b1")
        self.assertIn("would make dep cyclic", rejected[0]["reason"])
        self.assertIsNotNone(rejected[0]["carrier"]["spec_artifact_id"])
        self.assertEqual(set(labels.values()), {"accepted"})
        # No dependence ref reached the interface either.
        beta_node = importer.nodes[Coordinate("synthetic", "mini_fcl", 1, "beta")]
        self.assertEqual(
            [r for r in beta_node.interface.refs if r.role.value == "dependence"], []
        )


class SyntheticProjectionSourceTest(unittest.TestCase):
    """The out-of-scope branch of the per-projection custody count.

    Every projection in occurrence-01 names an owner inside its own arm, so a
    real scope never reaches this branch; a synthetic one does, and the
    rendered result must name the slot rather than let a sibling projection
    make the node read as verified.
    """

    def test_an_out_of_scope_owner_is_a_named_skip_not_a_silent_pass(self):
        importer = _Importer(Path("/nonexistent-synthetic-occurrence"), None, None, None)
        seen = synthetic_node(importer, "mini_fcl", "seen", synthetic_document([]), index=0)
        unseen = synthetic_node(importer, "mini_fcl", "unseen", synthetic_document([]), index=1)
        node = synthetic_node(importer, "mini_fcl", "citer", synthetic_document([]), index=2)
        # `unseen` is exposed to `citer` but is not part of the imported scope.
        del importer.nodes[unseen.coord]
        node.projections = [projection_to(seen), projection_to(unseen)]
        node.label_index = {
            projection["artifact_id"][:16]: position
            for position, projection in enumerate(node.projections)
        }
        importer.order = [seen.coord, node.coord]
        importer.ledger.node_totals(len(importer.order))
        importer._verify_projection_sources()

        check = importer.ledger.checks["projection_source"]
        self.assertEqual(check.unit, "projection")
        self.assertEqual((check.ran, check.total), (1, 2))
        slot = "synthetic/mini_fcl/cycle01/citer#" + unseen.record["artifact_id"][:16]
        self.assertEqual(
            check.skipped,
            [{
                "subject": slot,
                "missing": "in-scope owner (synthetic/mini_fcl/cycle01/unseen)",
            }],
        )
        self.assertIn("1 projection(s) had no in-scope owner", check.result)
        self.assertIn("citer#", check.result)


class SyntheticProseDispatchTest(unittest.TestCase):
    def test_a_prose_arm_with_a_valid_fcl_string_is_still_not_parsed(self):
        """Dispatch is on the declared surface, never on whether it happens to parse."""
        document = synthetic_document(
            [
                {"id": "m1", "type": "objection", "text": "an objection in a prose arm",
                 "bearing": "decisive", "target": [f"{label('other')}#x1"]},
                {"id": "m2", "type": "commitment", "text": "a commitment",
                 "scope": "s", "action": "a", "consequence": "c"},
            ],
            uptake=["m1", "m2"],
        )
        importer, labels, att, dep = build_synthetic(
            [
                ("mini_fcl", "other", synthetic_document(
                    [{"id": "x1", "type": "claim", "text": "x"}]), []),
                ("matched", "carry", document, ["other"]),
            ]
        )
        node = importer.nodes[Coordinate("synthetic", "matched", 1, "carry")]
        # It IS valid FCL-1 ...
        parsed, failure, detail = parse_fcl1_document(node.record["commitments"])
        self.assertIsNone(failure, detail)
        self.assertEqual(len(parsed["records"]), 2)
        # ... and the importer still refuses to read it as a commitment surface,
        # because the arm never declared one. No warrant, no edge, no refutation.
        self.assertIsNone(node.document)
        self.assertEqual(node.commitment_surface_state, "prose_not_parsed")
        self.assertEqual(node.interface, Interface())
        self.assertEqual(importer.residue_code_count("prose_commitment_surface"), 1)
        self.assertEqual(importer.residue_code_count("parse_failure"), 0)
        self.assertEqual(importer.residue_code_count("schema_failure"), 0)
        self.assertEqual(importer.planned_warrants, [])
        self.assertEqual(att, [])
        self.assertEqual(labels[node.spec_id], "accepted")
        entry = next(e for e in importer.residue if e["code"] == "prose_commitment_surface")
        self.assertIn("artifact IS", entry["reason"])
        self.assertIn("accepted by position", entry["reason"])
        # And the exposed material it never cited is still reported.
        self.assertEqual(importer.residue_code_count("projection_exposed_unreferenced"), 1)


class DocumentParsingTest(unittest.TestCase):
    """A malformed document stays opaque; nothing is ever repaired."""

    def test_valid_documents_parse(self):
        raw = json.loads(
            (OCCURRENCE / "artifacts/daily/mini_fcl/cycle01/rival.json").read_text(
                encoding="utf-8"
            )
        )["commitments"]
        document, failure, detail = parse_fcl1_document(raw)
        self.assertIsNone(failure, detail)
        self.assertEqual(len(document["records"]), 11)

    def test_malformed_documents_are_reported_never_repaired(self):
        samples = [
            ("not json at all", "parse_failure"),
            ('{"language": "FCL-2", "records": [], "uptake": []}', "schema_failure"),
            ('{"records": [], "uptake": []}', "schema_failure"),
            (
                json.dumps(
                    {
                        "language": "FCL-1",
                        "uptake": [],
                        "records": [
                            {"id": "c1", "type": "claim", "text": "one"},
                            {"id": "c1", "type": "claim", "text": "two"},
                        ],
                    }
                ),
                "schema_failure",
            ),
        ]
        for raw, expected in samples:
            with self.subTest(raw=raw[:40]):
                document, failure, detail = parse_fcl1_document(raw)
                self.assertIsNone(document)
                self.assertEqual(failure, expected)
                self.assertTrue(detail)


class ErrorSeverityBannerTest(unittest.TestCase):
    """No error-severity code fires on this occurrence, so pin both halves."""

    def test_an_unresolvable_ref_is_error_severity_and_surfaces_as_such(self):
        document = synthetic_document(
            [{"id": "a1", "type": "claim", "text": "a", "mentions": ["nowhere#x9"]}]
        )
        importer, _labels, _att, _dep = build_synthetic(
            [("mini_fcl", "alpha", document, [])]
        )
        self.assertEqual(importer.residue_code_count("ref_unresolved"), 1)
        self.assertEqual(RESIDUE_CODES["ref_unresolved"]["severity"], "error")
        self.assertEqual(importer.resolution["dangling"], 1)

    def test_the_banner_property_reports_only_nonzero_error_codes(self):
        with tempfile.TemporaryDirectory(prefix="h005-import-banner-") as directory:
            report = import_occurrence(
                OCCURRENCE, Path(directory) / "graph", dry_run=True, **SCOPE
            )
            self.assertEqual(report.error_severity_totals, {})
            doctored = dataclasses.replace(
                report,
                residue_totals={
                    **report.residue_totals,
                    "ref_unresolved": 3,
                    "parse_failure": 0,
                },
            )
            self.assertEqual(doctored.error_severity_totals, {"ref_unresolved": 3})
            self.assertEqual(doctored.as_dict()["error_severity_residue"],
                             {"ref_unresolved": 3})


class CoreDependencyTest(unittest.TestCase):
    def test_a_core_without_the_clock_parameter_is_refused_by_name(self):
        """The vendored core's one extension is a hard dependency, not a nicety."""
        import minireason.graph_import_h005 as library

        class LegacyHarness:
            def __init__(self, root, *, upto_seq=None, read_only=None):
                raise AssertionError("unreachable")

        original = library.Harness
        library.Harness = LegacyHarness
        try:
            with tempfile.TemporaryDirectory(prefix="h005-import-clock-") as directory:
                with self.assertRaises(MappingError) as caught:
                    import_occurrence(OCCURRENCE, Path(directory) / "graph", **SCOPE)
            self.assertIn("CORE_CLOCK_UNSUPPORTED", str(caught.exception))
        finally:
            library.Harness = original


if __name__ == "__main__":
    unittest.main()
