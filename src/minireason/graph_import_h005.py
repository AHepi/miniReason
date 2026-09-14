"""Offline importer: one H005 occurrence -> one harness-spec-v1.3 epistemic graph.

Replays a hash-pinned, write-once H005 occurrence (produced by
``tools/multicycle_commitment_study.py``) into a DeepReason P0 graph root using
the vendored core ``deepreason_core``. The decided contract is
``scratchpad/h005-import/mapping.md`` as corrected by the adversarial review
recorded in ``NOTES.md``; every construct neither can carry is reported in
``residue.json`` rather than dropped.

Standing invariants:

* **I1** offline and provider-free: only files under the occurrence directory
  are read; no provider call, no network, no credential is ever touched;
* **I2** no verdict is ever derived from a transport status
  (``delivery_status``, ``envelope_status``, ``finish_reason``,
  ``failure_type``, ``status`` are provenance only);
* **I3** ``dependence`` is never inferred - only an explicit FCL ``depends``
  ref that resolves to a *different* artifact becomes a dependence ref;
* **I4** nothing is repaired: a malformed ``commitments`` string stays opaque;
* **I5** every unmapped construct is reported with its verbatim text, at the
  granularities the closed residue vocabulary names (``ref``, ``record``,
  ``document``, ``edge``, ``artifact``, ``problem``, ``file``). Every FCL record
  in scope is either mapped to a spec construct or carries a residue code -
  ``claim`` and ``use`` records, which map to nothing, each get one - and
  ``side_table.json.records[]`` shows which, per record. This is record-level
  completeness, not a claim that a mapped record's every nuance survived;
* **I6** deterministic: no wall clock, no RNG, no dict-iteration order. Every
  id, every ``ts`` and every ``seq`` is a pure function of the occurrence
  bytes, so two imports of the same occurrence produce byte-identical roots;
* **I7** no label produced by this import is a semantic attribution. Statuses
  are mechanism bookkeeping over the imported attack relation; they do not bear
  on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root
  alone interprets substantive output (PROTOCOL.md §Interpretation).
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

from jsonschema import Draft202012Validator

from deepreason_core.adjudication.edges import build_att, build_dep, toposort
from deepreason_core.adjudication.grounded import label0 as compute_label0
from deepreason_core.adjudication.support import final_labels
from deepreason_core.canonical import canonical_json, sha256_hex
from deepreason_core.harness import Harness
from deepreason_core.ontology import (
    Artifact,
    Budget,
    Commitment,
    Interface,
    Problem,
    ProblemProvenance,
    Provenance,
    Ref,
    Rule,
    SpawnTrigger,
    Warrant,
    WarrantType,
)
from deepreason_core.ontology.artifact import ProvenanceRole, RefRole

IMPORTER_VERSION = "import_h005/1"
SIDE_TABLE_SCHEMA = "h005-import.side-table.v1"
RESIDUE_SCHEMA = "h005-import.residue.v1"
REPORT_SCHEMA = "h005-import.report.v1"

ARTIFACT_RECORD_SCHEMA = "minireason.h005.artifact.v1"
TRACE_RECORD_SCHEMA = "minireason.h005.trace.v1"
ATTEMPT_RECORD_SCHEMA = "minireason.h005.attempt.v1"
RECEIPT_RECORD_SCHEMA = "minireason.h005.receipt.v1"
WAVE_RECORD_SCHEMA = "minireason.h005.wave.v1"
PLAN_RECORD_SCHEMA = "minireason.h005.plan.v1"
MATERIAL_RECORD_SCHEMA = "minireason.h005.material.v1"

FCL_SCHEMA_PATH = Path(__file__).resolve().parent / "data" / "fcl1.schema.json"

#: Arms whose declared commitment surface is the FCL-1 formal language. Every
#: other arm was instructed in prose and its ``commitments`` string is not an
#: FCL-1 document, so it is never parsed as one (invariant I4).
FCL_SURFACE_ARMS = ("mini_fcl",)

#: The banner that heads every REPORT.md (invariant I7).
I7_BANNER = (
    "**No label produced by this import is a semantic attribution.** Statuses are "
    "mechanism bookkeeping over the imported attack relation; they do not bear on the "
    "FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone "
    "interprets substantive output (PROTOCOL.md §Interpretation)."
)

#: Closed residue vocabulary: code -> (severity, counting unit).
RESIDUE_CODES: dict[str, dict[str, str]] = {
    "depends_intra_document": {"severity": "lossy", "unit": "ref"},
    "depends_cross_document": {"severity": "informational", "unit": "ref"},
    "mentions_intra_document": {"severity": "lossy", "unit": "ref"},
    "uptake_refs_unmapped": {"severity": "unmapped", "unit": "ref"},
    "uptake_lists_unmapped": {"severity": "unmapped", "unit": "document"},
    "target_on_non_objection_record": {"severity": "informational", "unit": "record"},
    "use_record_unmapped": {"severity": "unmapped", "unit": "record"},
    "claim_record_unmapped": {"severity": "unmapped", "unit": "record"},
    "consequence_on_non_commitment_record": {"severity": "informational", "unit": "record"},
    "commitment_record_not_in_uptake": {"severity": "informational", "unit": "record"},
    "grounds_absent_on_objection": {"severity": "informational", "unit": "record"},
    "objection_untargeted": {"severity": "lossy", "unit": "record"},
    "objection_self_target_only": {"severity": "lossy", "unit": "record"},
    "objection_target_self_ref_dropped": {"severity": "lossy", "unit": "ref"},
    "warrant_edge_deduplicated": {"severity": "informational", "unit": "edge"},
    "validity_node_minted_unasserted": {"severity": "informational", "unit": "artifact"},
    "criticism_of_criticism_retargeted": {"severity": "informational", "unit": "edge"},
    "criticism_of_criticism_intra_document_dropped": {"severity": "lossy", "unit": "ref"},
    "qualified_ref_body_pseudo_local": {"severity": "extension", "unit": "ref"},
    "bare_label_ref": {"severity": "extension", "unit": "ref"},
    "ref_to_task_artifact": {"severity": "informational", "unit": "ref"},
    "projection_absent": {"severity": "informational", "unit": "document"},
    "projection_exposed_unreferenced": {"severity": "informational", "unit": "document"},
    "problem_trigger_approximated": {"severity": "lossy", "unit": "problem"},
    "problem_trigger_research_not_in_v13_enum": {"severity": "informational", "unit": "problem"},
    "commitment_not_executable": {"severity": "informational", "unit": "record"},
    "adjudication_batched": {"severity": "informational", "unit": "file"},
    "revises_unmapped": {"severity": "unmapped", "unit": "ref"},
    "withdraws_unmapped": {"severity": "unmapped", "unit": "ref"},
    "ref_unresolved": {"severity": "error", "unit": "ref"},
    "ref_through_absent_projection": {"severity": "error", "unit": "ref"},
    "ref_through_unexposed_view": {"severity": "error", "unit": "ref"},
    "ref_to_unregistered_target_dropped": {"severity": "error", "unit": "ref"},
    "opaque_envelope": {"severity": "informational", "unit": "artifact"},
    "prose_commitment_surface": {"severity": "informational", "unit": "artifact"},
    "parse_failure": {"severity": "error", "unit": "document"},
    "schema_failure": {"severity": "error", "unit": "document"},
    "dependence_cycle_rejected": {"severity": "error", "unit": "edge"},
}

#: Every coordinate component the importer turns into a path segment must
#: match this. Nothing else may ever be joined onto the occurrence root: a
#: component such as ``..`` or ``/etc`` would make ``occurrence_path`` address
#: bytes outside the occurrence, which invariant I1 forbids.
_SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9_-]+$")

_BRIEF_LABEL_LINE = re.compile(
    r"^\[([0-9a-f]{16})\] \((?:h005\.[a-z0-9]+\.)?(p\.[a-z_]+\.\d+)\)$", re.MULTILINE
)
_BRIEF_TASK_LINE = re.compile(r"^\[([0-9a-f]{16})\] \(h005\.task\.v1\)$", re.MULTILINE)
_TASK_ALIAS = "h005.task.v1"
_BODY_PSEUDO_LOCAL = "BODY"


class CustodyError(RuntimeError):
    """The occurrence failed its custody check; nothing was imported."""


class MappingError(RuntimeError):
    """The occurrence is well-custodied but cannot be mapped as specified."""


class SelectorMatchedNothing(MappingError):
    """The occurrence has coordinates, but the requested selectors match none.

    Distinct from ``EMPTY_SCOPE`` (a plain :class:`MappingError`), which means
    the *occurrence* carries no coordinate at all. This one is an operator
    mistake - a misspelt ``--arm``, a cycle that was never run - and the fix is
    to change the selector, not the occurrence, so it gets its own CLI exit
    code and lists what the occurrence actually holds. It subclasses
    ``MappingError`` so callers written against that keep working.
    """


class OutRootRefused(ValueError, FileExistsError):
    """The requested output root is not usable; nothing was imported.

    Distinct from :class:`CustodyError` (the occurrence is bad) and from
    :class:`MappingError` (the occurrence cannot be mapped): the *occurrence* is
    fine and the *destination* is refused, which is a different thing for an
    operator to fix. It inherits both ``ValueError`` (the historical spelling
    for ``OUT_ROOT_INSIDE_OCCURRENCE``) and ``FileExistsError`` (the historical
    spelling for a write-once root that already exists), so callers written
    against either keep working.
    """


#: Commitment-surface states recorded per node in ``side_table.json``.
#: ``read_fcl1``                  an FCL-1 document was parsed and mapped;
#: ``prose_not_parsed``           the arm's declared surface is prose;
#: ``unavailable_decode_failure`` the commitments string is empty because the
#:                               study harness's strict JSON decode failed;
#: ``parse_failure``/``schema_failure`` an FCL-surface arm's document did not
#:                               parse or did not validate.
COMMITMENT_SURFACE_STATES = (
    "read_fcl1",
    "prose_not_parsed",
    "unavailable_decode_failure",
    "parse_failure",
    "schema_failure",
)

#: How each commitment-surface state is rendered in the labels table. A label
#: is only as informative as the surface it was computed over, so the surface
#: is printed in the same row as the status rather than left to the side
#: table. ``n/a`` is for an artifact that has no commitment surface at all -
#: a validity node or an FCL-1 document artifact.
SURFACE_COLUMN: dict[str, str] = {
    "read_fcl1": "read",
    "prose_not_parsed": "NOT READ (prose)",
    "unavailable_decode_failure": "UNAVAILABLE (decode)",
    "parse_failure": "PARSE FAILURE",
    "schema_failure": "SCHEMA FAILURE",
}
SURFACE_NOT_APPLICABLE = "n/a"

#: Root's published review of the matched-arm envelope loss (repo-relative).
ENVELOPE_REVIEW_PATH = "docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md"

#: The wording every accept-by-position explanation uses. An unattacked
#: artifact is accepted because nothing in *this import* targets it, and this
#: import only ever reified criticism out of an FCL-1 commitment surface.
ACCEPT_BY_POSITION = (
    "accept-by-position: no warrant in this import targets it. This import reified "
    "criticism only from an FCL-1 commitment surface, so the absence of an attacker is "
    "not evidence that the contribution was uncriticised."
)

#: Why an empty ``commitments`` string is not a missing commitment.
OPAQUE_ENVELOPE_REASON = (
    "The commitments string is empty because the study harness's strict JSON decode of "
    "the returned envelope failed and `decode_contribution` took its failure branch, "
    "storing the whole returned text as `body` and `\"\"` as `commitments` "
    "(`commitments_sha256` is the sha256 of the empty string). Root's published review, "
    "`" + ENVELOPE_REVIEW_PATH + "`, measured that the same bytes parsed non-strictly do "
    "contain a commitments field: the commitments were authored and lost in decoding. The "
    "commitment surface is therefore **UNAVAILABLE, not absent**, and this is not evidence "
    "that the author declined to commit. This import does not repair it (I4): the artifact "
    "carries an empty Interface - no commitment surface, no refs - and the recorded "
    "envelope_status is metadata, never a verdict (I2)."
)

#: The invariant half of the multi-arm paragraph. Only the inventory of arms
#: in front of it is per-run; every claim it makes is fixed here, so no run can
#: soften it.
MULTI_ARM_FRAMING_TAIL = (
    "A prose commitment surface is never parsed, so no warrant, no attack edge and no "
    "refuted label can arise from a prose arm under this import. The distribution of "
    "statuses across arms is therefore a property of the carrier this importer reads, not "
    "a comparison between the arms. Any cross-arm reading is root's, not this instrument's."
)

#: Why a prose arm's commitment string is not parsed, and what its label means.
PROSE_SURFACE_REASON = (
    "declares a prose commitment surface, so the string is not an FCL-1 document and is "
    "never parsed as one - the author was never asked for FCL-1. The artifact IS "
    "adjudicated: it is registered, it is in the graph, and it is labelled. With no "
    "commitment surface read it has no attacker, so grounded semantics labels it accepted "
    "by position, and that label carries no information about the arm. The text is "
    "preserved verbatim as a blob and in the side table."
)


# --------------------------------------------------------------------------- #
# small deterministic helpers                                                  #
# --------------------------------------------------------------------------- #


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def safe_component(value: Any, what: str) -> str:
    """Refuse any coordinate component that is not a plain path segment.

    The occurrence's own coordinates are alphanumeric, but they arrive from
    files (``waves/*.json``, ``material.json``, record ``coordinate`` blocks)
    and are concatenated into read paths. A component is therefore checked
    before it is ever joined, not after.
    """
    text = str(value)
    if not _SAFE_COMPONENT.match(text):
        raise CustodyError(f"COORDINATE_COMPONENT_UNSAFE:{what}:{text!r}")
    return text


def study_digest(value: Any) -> str:
    """``minireason.provider.digest`` re-implemented (read, not imported).

    Importing ``tools.multicycle_commitment_study`` would insert repository
    paths into ``sys.path`` at import time and pull in the live DeepSeek
    transport module; the importer must stay provider-free, so the one hashing
    rule its custody check needs is re-implemented from the source and pinned
    by a test against the recorded ``plan_id``.
    """
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


@dataclass(frozen=True, order=True)
class Coordinate:
    problem: str
    arm: str
    cycle: int
    node: str

    @property
    def key(self) -> str:
        return f"{self.problem}/{self.arm}/cycle{self.cycle:02d}/{self.node}"

    @property
    def wave_label(self) -> str:
        """The spelling used by ``waves/*.json``.``request_hashes``."""
        return f"{self.problem}/{self.arm}/cycle-{self.cycle}/{self.node}"

    def as_dict(self) -> dict[str, Any]:
        return {"problem": self.problem, "arm": self.arm, "cycle": self.cycle, "node": self.node}

    @classmethod
    def from_dict(cls, raw: Any) -> "Coordinate":
        """Build a coordinate from a recorded ``coordinate`` block.

        Every component is validated against ``_SAFE_COMPONENT`` before the
        object exists, because ``key``/``wave_label``/:func:`occurrence_path`
        turn all four straight into read paths.
        """
        if not isinstance(raw, dict):
            raise CustodyError("COORDINATE_MALFORMED")
        try:
            problem, arm, node = str(raw["problem"]), str(raw["arm"]), str(raw["node"])
            cycle = int(raw["cycle"])
        except (KeyError, TypeError, ValueError) as exc:  # pragma: no cover - defensive
            raise CustodyError("COORDINATE_MALFORMED") from exc
        safe_component(problem, "problem")
        safe_component(arm, "arm")
        safe_component(node, "node")
        safe_component(cycle, "cycle")
        return cls(problem, arm, cycle, node)


def occurrence_path(coord: Coordinate, category: str, suffix: str = "json") -> str:
    return f"{category}/{coord.problem}/{coord.arm}/cycle{coord.cycle:02d}/{coord.node}.{suffix}"


def provider_call_path(coord: Coordinate, part: str) -> str:
    """``provider/<problem>/<arm>/cycle<NN>/<node>/call-0001.<part>.json``."""
    return (
        f"provider/{coord.problem}/{coord.arm}/cycle{coord.cycle:02d}/{coord.node}"
        f"/call-0001.{part}.json"
    )


class _Reader:
    """Reads occurrence bytes and records the sha256 of every file read.

    A missing or malformed occurrence file is a custody failure, not a stray
    ``OSError``/``ValueError``: the caller refuses the import and nothing is
    written, and the CLI can map the whole class to one exit code.
    """

    def __init__(self, root: Path) -> None:
        self.root = root
        self.files: dict[str, str] = {}

    def _inside(self, relative: str) -> Path:
        """Resolve one occurrence-relative path, refusing anything outside.

        Coordinate components are validated at the boundary
        (:meth:`Coordinate.from_dict`, :meth:`_Importer.discover_scope`,
        :meth:`_Importer.load_waves`), and this is the second, unconditional
        gate: no read and no existence probe may address bytes that are not
        the occurrence's own, whatever composed the path (invariant I1).
        """
        candidate = self.root / relative
        root = self.root.resolve()
        resolved = candidate.resolve()
        if resolved != root and root not in resolved.parents:
            raise CustodyError(f"PATH_ESCAPES_OCCURRENCE:{relative}")
        return candidate

    def read_bytes(self, relative: str) -> bytes:
        path = self._inside(relative)
        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise CustodyError(f"OCCURRENCE_FILE_MISSING:{relative}") from exc
        self.files[relative] = sha256_bytes(raw)
        return raw

    def parse_json(self, relative: str, raw: bytes) -> Any:
        """Decode occurrence bytes already read, as a custody failure on error."""
        try:
            return json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            raise CustodyError(f"OCCURRENCE_FILE_MALFORMED_JSON:{relative}: {exc}") from exc

    def read_json(self, relative: str) -> Any:
        return self.parse_json(relative, self.read_bytes(relative))

    def exists(self, relative: str) -> bool:
        return self._inside(relative).exists()


class _Clock:
    """Deterministic event clock handed to ``Harness(clock=...)``.

    The staged core gained one optional constructor parameter for this (see
    NOTES.md, "vendored-core extension"): ``Event.ts`` must be a pure function
    of the occurrence bytes, so two replays under different machine load cannot
    fork the log.
    """

    def __init__(self) -> None:
        self.ts: str | None = None

    def __call__(self) -> str:
        if self.ts is None:  # pragma: no cover - defensive
            raise MappingError("EVENT_TIMESTAMP_NOT_PINNED")
        return self.ts


# --------------------------------------------------------------------------- #
# custody                                                                      #
# --------------------------------------------------------------------------- #


@dataclass
class _Check:
    """One custody check, with how many subjects it actually ran over.

    ``kind`` separates a check that compares two independently written files
    (``cross_file``) from one that only compares a file against itself
    (``self_consistency``). A self-consistency check cannot detect a coherent
    rewrite of that one file; saying so is the point of the split.
    """

    key: str
    kind: str  # "cross_file" | "self_consistency"
    text: str
    unit: str  # "node" | "projection" | "occurrence" | "manifest"
    total: int = 0
    ran: int = 0
    skipped: list[dict[str, str]] = field(default_factory=list)

    @property
    def result(self) -> str:
        plural = self.unit + ("" if self.total == 1 else "s")
        if self.total == 0:
            return f"not applicable in this scope (0 {plural})"
        if not self.skipped:
            return f"verified ({self.ran}/{self.total} {plural})"
        missing = sorted({entry["missing"] for entry in self.skipped})
        subjects = ", ".join(f"`{entry['subject']}`" for entry in self.skipped)
        return (
            f"verified ({self.ran}/{self.total} {plural}; {len(self.skipped)} "
            f"{self.unit}(s) had no {' / '.join(missing)}: {subjects})"
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "kind": self.kind,
            "check": self.text,
            "unit": self.unit,
            "ran": self.ran,
            "total": self.total,
            "skipped": list(self.skipped),
            "result": self.result,
        }


class _CustodyLedger:
    """Per-check ran/total counters, so the report cannot say a flat "verified".

    A check that could not run over a coordinate (no receipt, no attempt, no
    request record, no provider call directory) is *not* a failure - the
    coordinate is admitted with its absent inputs recorded - but it is also not
    a verification, and the report must not spell it as one.
    """

    #: key -> (kind, text, unit). Order is the render order.
    DECLARED: tuple[tuple[str, str, str, str], ...] = (
        ("plan_identity", "self_consistency",
         "plan_id == study_digest(plan without plan_id)", "occurrence"),
        ("material_pin", "cross_file",
         "plan.material_sha256 == sha256(material.json)", "occurrence"),
        ("manifest_pins", "cross_file",
         "plan.manifests[tid] == sha256(manifests/<tid>.json)", "manifest"),
        ("artifact_self_hash", "self_consistency",
         "per node: sha256(body) == body_sha256, sha256(commitments) == "
         "commitments_sha256, and <field>_ref == <field>_sha256", "node"),
        ("artifact_coordinate", "self_consistency",
         "per node: the artifact record's own coordinate is the one it is filed under",
         "node"),
        ("receipt_present", "cross_file",
         "per node: receipt present (responses/<node>.json)", "node"),
        ("artifact_bytes_vs_receipt", "cross_file",
         "per node: sha256(artifacts/<node>.json) == receipt.artifact_sha256", "node"),
        ("status_vs_receipt", "cross_file",
         "per node: receipt.status == delivery_status and receipt.envelope_status == "
         "envelope_status (recorded, never read as a verdict)", "node"),
        ("public_text", "cross_file",
         "per node: sha256(responses/<node>.txt) == artifact.public_text_sha256", "node"),
        ("attempt_vs_receipt", "cross_file",
         "per node: attempt.request_sha256 == receipt.request_sha256", "node"),
        ("request_record", "cross_file",
         "per node: study_digest(requests/<node>.json) == attempt.request_sha256 == "
         "receipt.request_sha256", "node"),
        ("trace_pinned", "cross_file",
         "per node: request.trace_sha256 == study_digest(traces/<node>.json), checked "
         "before the trace is read by the label index or the projection resolver; counted "
         "as run only where the request record is itself pinned by an attempt or a receipt",
         "node"),
        ("provider_bytes", "cross_file",
         "per node: sha256(provider/<coord>/call-0001.{request,response}.json) == "
         "receipt.provider_{request,response}_sha256 (skipped only for a FAILED receipt)",
         "node"),
        ("wave_placement", "cross_file",
         "per node: attempt.wave_id is the wave listing the coordinate and "
         "wave.request_hashes[<coordinate>] == attempt.request_sha256", "node"),
        ("brief_pinned", "self_consistency",
         "per node: sha256(trace.original_brief) == trace.original_brief_sha256", "node"),
        ("brief_label_index", "self_consistency",
         "per node: every [label] line in the brief indexes the projection slot it names, "
         "and the brief's label set equals the projection set", "node"),
        ("task_label", "self_consistency",
         "per node: the exposed task label agrees with trace.task_artifact.artifact_id",
         "node"),
        ("projection_source", "cross_file",
         "per projection: selected_source artifact_id/body_sha256/commitments_sha256 equal "
         "the authored artifact record it names", "projection"),
    )

    def __init__(self) -> None:
        self.checks: dict[str, _Check] = {
            key: _Check(key=key, kind=kind, text=text, unit=unit)
            for key, kind, text, unit in self.DECLARED
        }

    def total(self, key: str, count: int) -> None:
        self.checks[key].total = count

    def node_totals(self, count: int) -> None:
        for check in self.checks.values():
            if check.unit == "node":
                check.total = count

    def ran(self, key: str) -> None:
        self.checks[key].ran += 1

    def skipped(self, key: str, subject: str, missing: str) -> None:
        self.checks[key].skipped.append({"subject": subject, "missing": missing})

    def as_dict(self) -> dict[str, list[dict[str, Any]]]:
        return {
            kind: [c.as_dict() for c in self.checks.values() if c.kind == kind]
            for kind in ("cross_file", "self_consistency")
        }


def verify_custody(reader: _Reader, ledger: _CustodyLedger) -> dict[str, Any]:
    """Occurrence-local custody: plan identity, material and manifest pins.

    ``multicycle_commitment_study.verify()`` recomputes the whole plan body from
    a repository checkout (runtime pins, compiled manifests). That check is not
    available to an importer handed only an occurrence directory, so the subset
    that is a pure function of the occurrence's own bytes is re-implemented
    here: ``plan_id == digest(plan without plan_id)``, ``material_sha256 ==
    sha256(material.json)`` and ``manifests[tid] == sha256(manifests/tid.json)``
    for every manifest the occurrence carries.
    """
    plan = reader.read_json("plan.json")
    if not isinstance(plan, dict) or plan.get("schema") != PLAN_RECORD_SCHEMA:
        raise CustodyError("PLAN_SCHEMA")
    stored_id = plan.get("plan_id")
    if not isinstance(stored_id, str) or not stored_id:
        raise CustodyError("PLAN_ID_MISSING")
    if study_digest({k: v for k, v in plan.items() if k != "plan_id"}) != stored_id:
        raise CustodyError("IMMUTABLE_PLAN_MISMATCH")
    ledger.total("plan_identity", 1)
    ledger.ran("plan_identity")

    material_raw = reader.read_bytes("material.json")
    material = reader.parse_json("material.json", material_raw)
    if not isinstance(material, dict) or material.get("schema") != MATERIAL_RECORD_SCHEMA:
        raise CustodyError("MATERIAL_SCHEMA")
    if sha256_bytes(material_raw) != plan.get("material_sha256"):
        raise CustodyError("MATERIAL_PIN_MISMATCH")
    ledger.total("material_pin", 1)
    ledger.ran("material_pin")

    pins = dict(plan.get("manifests") or {})
    ledger.total("manifest_pins", len(pins))
    manifests: dict[str, dict[str, Any]] = {}
    for template_id, pin in sorted(pins.items()):
        relative = f"manifests/{template_id}.json"
        if not reader.exists(relative):
            manifests[template_id] = {"pin": pin, "verified": None, "present": False}
            ledger.skipped("manifest_pins", template_id, "manifest file")
            continue
        if sha256_bytes(reader.read_bytes(relative)) != pin:
            raise CustodyError("MANIFEST_PIN_MISMATCH")
        manifests[template_id] = {"pin": pin, "verified": True, "present": True}
        ledger.ran("manifest_pins")

    return {
        "plan_id": stored_id,
        "material_sha256": plan["material_sha256"],
        "manifests": manifests,
        "material": material,
        "plan": plan,
    }


def _verify_node_custody(
    reader: _Reader, coord: Coordinate, record: dict[str, Any], ledger: _CustodyLedger
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, dict[str, Any], list[str]]:
    """Per-node custody, including the trace-pinning chain.

    Returns ``(receipt, attempt, trace, absent_inputs)``. The trace is read and
    **pinned here**, before any caller can use it: ``requests/<coord>.json``
    fixes the trace by ``trace_sha256`` and is itself fixed by
    ``attempt.request_sha256`` and ``receipt.request_sha256``, so a rewritten
    trace cannot reach the label index or the projection resolver. A
    coordinate with no request record is refused (``REQUEST_RECORD_MISSING``):
    an unpinned trace is not admitted, because everything this import reads
    out of a trace is load-bearing. Where the request record exists but
    neither an attempt nor a receipt pins it, the chain is still checked but
    the ledger records ``trace_pinned`` and ``request_record`` as *not run*.

    This reproduces the occurrence-local links of
    ``tools/multicycle_commitment_study.py`` ``read_terminal``; the links that
    need a repository checkout (recomputing ``payload_for``/``settings_for``
    and re-deriving the artifact through ``decode_contribution``) are not
    reproduced, and the workflow doc says so.
    """
    absent: list[str] = []
    if record.get("schema") != ARTIFACT_RECORD_SCHEMA:
        raise CustodyError(f"ARTIFACT_SCHEMA:{coord.key}")
    if Coordinate.from_dict(record.get("coordinate")) != coord:
        raise CustodyError(f"ARTIFACT_COORDINATE_MISMATCH:{coord.key}")
    ledger.ran("artifact_coordinate")
    for name in ("body", "commitments"):
        text = record.get(name)
        if not isinstance(text, str):
            raise CustodyError(f"ARTIFACT_FIELD_NOT_A_STRING:{coord.key}:{name}")
        if sha256_bytes(text.encode("utf-8")) != record.get(name + "_sha256"):
            raise CustodyError(f"ARTIFACT_CONTENT_CHANGED:{coord.key}:{name}")
        if record.get(name + "_ref") != record.get(name + "_sha256"):
            raise CustodyError(f"ARTIFACT_REF_MISMATCH:{coord.key}:{name}")
    ledger.ran("artifact_self_hash")

    receipt_relative = occurrence_path(coord, "responses")
    receipt: dict[str, Any] | None = None
    if reader.exists(receipt_relative):
        ledger.ran("receipt_present")
        artifact_bytes = reader.read_bytes(occurrence_path(coord, "artifacts"))
        receipt = reader.read_json(receipt_relative)
        if receipt.get("schema") != RECEIPT_RECORD_SCHEMA:
            raise CustodyError(f"RECEIPT_SCHEMA:{coord.key}")
        if Coordinate.from_dict(receipt.get("coordinate")) != coord:
            raise CustodyError(f"RECEIPT_COORDINATE_MISMATCH:{coord.key}")
        if sha256_bytes(artifact_bytes) != receipt.get("artifact_sha256"):
            raise CustodyError(f"ARTIFACT_BYTES_CHANGED:{coord.key}")
        ledger.ran("artifact_bytes_vs_receipt")
        if receipt.get("status") != record.get("delivery_status"):
            raise CustodyError(f"DELIVERY_STATUS_MISMATCH:{coord.key}")
        if receipt.get("envelope_status") != record.get("envelope_status"):
            raise CustodyError(f"ENVELOPE_STATUS_MISMATCH:{coord.key}")
        ledger.ran("status_vs_receipt")
        text_relative = occurrence_path(coord, "responses", "txt")
        if reader.exists(text_relative):
            if sha256_bytes(reader.read_bytes(text_relative)) != record.get("public_text_sha256"):
                raise CustodyError(f"PUBLIC_TEXT_CHANGED:{coord.key}")
            ledger.ran("public_text")
        else:
            absent.append(text_relative)
            ledger.skipped("public_text", coord.key, "public text")
    else:
        absent.append(receipt_relative)
        for key in (
            "receipt_present",
            "artifact_bytes_vs_receipt",
            "status_vs_receipt",
            "public_text",
            "provider_bytes",
        ):
            ledger.skipped(key, coord.key, "receipt")

    attempt_relative = occurrence_path(coord, "attempts")
    attempt: dict[str, Any] | None = None
    if reader.exists(attempt_relative):
        attempt = reader.read_json(attempt_relative)
        if attempt.get("schema") != ATTEMPT_RECORD_SCHEMA:
            raise CustodyError(f"ATTEMPT_SCHEMA:{coord.key}")
        if Coordinate.from_dict(attempt.get("coordinate")) != coord:
            raise CustodyError(f"ATTEMPT_COORDINATE_MISMATCH:{coord.key}")
        if receipt is not None:
            if attempt.get("request_sha256") != receipt.get("request_sha256"):
                raise CustodyError(f"REQUEST_HASH_MISMATCH:{coord.key}")
            ledger.ran("attempt_vs_receipt")
        else:
            ledger.skipped("attempt_vs_receipt", coord.key, "receipt")
    else:
        absent.append(attempt_relative)
        ledger.skipped("attempt_vs_receipt", coord.key, "attempt")

    # -- the trace-pinning chain, before the trace is used by anything -------- #
    trace_relative = occurrence_path(coord, "traces")
    trace = reader.read_json(trace_relative)
    if trace.get("schema") != TRACE_RECORD_SCHEMA:
        raise CustodyError(f"TRACE_SCHEMA:{coord.key}")
    if Coordinate.from_dict(trace.get("coordinate")) != coord:
        raise CustodyError(f"TRACE_COORDINATE_MISMATCH:{coord.key}")

    # The request record is the trace's only pin, and the trace is the most
    # load-bearing input this import has: the label index, the projection
    # index and every two-hop reference are read off it. A coordinate whose
    # request record is absent is therefore REFUSED rather than admitted with
    # an unpinned trace - the same posture as NO_LEADING_RECEIPT, and unlike a
    # missing receipt, which costs only bookkeeping. All 22 request records
    # exist in occurrence-01.
    request_relative = occurrence_path(coord, "requests")
    if not reader.exists(request_relative):
        raise CustodyError(f"REQUEST_RECORD_MISSING:{coord.key}")
    request = reader.read_json(request_relative)
    if Coordinate.from_dict(request.get("coordinate")) != coord:
        raise CustodyError(f"REQUEST_COORDINATE_MISMATCH:{coord.key}")
    request_digest = study_digest(request)
    pinned_by = [
        source.get("request_sha256") for source in (attempt, receipt) if source is not None
    ]
    if any(pin != request_digest for pin in pinned_by):
        raise CustodyError(f"REQUEST_RECORD_MISMATCH:{coord.key}")
    if request.get("trace_sha256") != study_digest(trace):
        raise CustodyError(f"TRACE_NOT_PINNED:{coord.key}")
    if pinned_by:
        ledger.ran("request_record")
        # The trace hash chains through the request record, so it is only as
        # good as the request record's own pin. With neither an attempt nor a
        # receipt to fix it, `request.trace_sha256 == digest(trace)` is one
        # file agreeing with another file that nothing independent pins, and
        # the ledger must not spell that as a cross-file verification.
        ledger.ran("trace_pinned")
    else:
        ledger.skipped("request_record", coord.key, "attempt or receipt")
        ledger.skipped("trace_pinned", coord.key, "attempt or receipt")

    # -- provider call bytes against the receipt's recorded hashes ------------ #
    if receipt is not None:
        if receipt.get("status") == "FAILED":
            # read_terminal admits a FAILED terminal with no provider record.
            ledger.skipped("provider_bytes", coord.key, "provider call (FAILED receipt)")
        else:
            for part in ("request", "response"):
                relative = provider_call_path(coord, part)
                expected = receipt.get(f"provider_{part}_sha256")
                # Absent hash and absent file used to compare None == None and
                # pass, so a non-FAILED receipt with its provider record
                # deleted verified silently. Both must be there.
                if not isinstance(expected, str) or not expected:
                    raise CustodyError(f"PROVIDER_HASH_MISSING:{coord.key}:{part}")
                if not reader.exists(relative):
                    raise CustodyError(f"PROVIDER_HASH_MISSING:{coord.key}:{part}")
                if sha256_bytes(reader.read_bytes(relative)) != expected:
                    raise CustodyError(f"PROVIDER_BYTES_CHANGED:{coord.key}:{part}")
            ledger.ran("provider_bytes")
    return receipt, attempt, trace, absent


# --------------------------------------------------------------------------- #
# FCL-1 parsing (strict; never repaired)                                       #
# --------------------------------------------------------------------------- #


def fcl1_validator() -> Draft202012Validator:
    schema = json.loads(FCL_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def parse_fcl1_document(
    raw: str, validator: Draft202012Validator | None = None
) -> tuple[dict[str, Any] | None, str | None, str]:
    """Strictly parse and validate one FCL-1 document.

    Returns ``(document, failure_code, detail)``. ``failure_code`` is
    ``parse_failure`` (not JSON) or ``schema_failure`` (fails
    ``fcl1.schema.json`` or its out-of-schema local-name uniqueness rule); the
    caller keeps such an artifact opaque and never repairs it.
    """
    validator = validator or fcl1_validator()
    try:
        document = json.loads(raw)
    except ValueError as exc:
        return None, "parse_failure", f"commitments string is not JSON: {exc}"
    errors = sorted(validator.iter_errors(document), key=lambda e: list(e.absolute_path))
    if errors:
        detail = "; ".join(
            "%s: %s" % ("/".join(str(p) for p in e.absolute_path) or "<root>", e.message)
            for e in errors
        )
        return None, "schema_failure", detail
    ids = [r.get("id") for r in document.get("records", [])]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    if duplicates:
        return None, "schema_failure", f"duplicate local names: {duplicates}"
    return document, None, ""


# --------------------------------------------------------------------------- #
# the report                                                                   #
# --------------------------------------------------------------------------- #


def attack_index(att_edges: Sequence[tuple[str, str]]) -> dict[str, list[str]]:
    """target artifact id -> its attackers, sorted.

    One spelling for the CLI table, the why chains and REPORT.md: three
    renderings of the same relation must not be able to disagree about it.
    """
    index: dict[str, list[str]] = {}
    for source, target in att_edges:
        index.setdefault(target, []).append(source)
    return {target: sorted(sources) for target, sources in index.items()}


def label_order(labels: dict[str, str], names: dict[str, str]) -> list[str]:
    """The one display order for artifacts: readable name first, then id."""
    return sorted(labels, key=lambda aid: (names.get(aid, ""), aid))


DEVIATIONS: tuple[dict[str, str], ...] = (
    {
        "code": "adjudication_batched",
        "what": "no separate terminal Adj event is emitted",
        "why": (
            "spec §3 recomputes after every registration and the vendored P0 Harness does "
            "exactly that inside each registration event, but it exposes no public Adj "
            "emitter; the import writes through the registration API only and never forges "
            "a log line, so the terminal adjudication is the state after the last event"
        ),
    },
    {
        "code": "problem_trigger_approximated",
        "what": "imported FCL problem records use SpawnTrigger.SEED",
        "why": (
            "the vendored enum has no 'import' member; 'seed' is the only trigger that does "
            "not assert an in-graph derivation. The clean fix is an enum addition, requested "
            "rather than papered over"
        ),
    },
    {
        "code": "problem_trigger_research_not_in_v13_enum",
        "what": "research problems use SpawnTrigger.RESEARCH with empty criteria",
        "why": (
            "the vendored enum has the member and §12 is exactly this path, but the trigger "
            "is not part of the v1.3 enum text; criteria stay empty because no instantiated "
            "commitment id is a criterion"
        ),
    },
    {
        "code": "depends_intra_document",
        "what": "document-local depends refs are dropped, not turned into dep edges",
        "why": (
            "at node granularity they would be dep self-loops, i.e. cycles; toposort rejects "
            "them and a self-loop asserts nothing the author declared"
        ),
    },
    {
        "code": "objection_self_target_only",
        "what": "a self-targeting objection mints no warrant",
        "why": (
            "a Dung self-attack means 'this argument is self-defeating', which is not what an "
            "intra-document caveat asserts; minting it would flip two labels for reasons that "
            "have nothing to do with the evidence"
        ),
    },
    {
        "code": "criticism_of_criticism_retargeted",
        "what": (
            "an objection against a record this import reified as a warrant attacks that "
            "warrant's validity node, not the node artifact"
        ),
        "why": (
            "spec §1 closure: attackers of a validity node attack the warrant and every "
            "carrier of it, so criticism of a criticism keeps its force instead of collapsing "
            "into a plain edge onto the carrier"
        ),
    },
    {
        "code": "criticism_of_criticism_intra_document_dropped",
        "what": (
            "the retargeting rule above has ONE exception: an objection against a "
            "criticism carried by the SAME artifact is not retargeted"
        ),
        "why": (
            "the §1 closure lifts an attack on a validity node onto every carrier of the "
            "warrant, and for an intra-document criticism of a criticism that carrier is the "
            "objector itself, so retargeting would mint a self-attack through the closure "
            "and make the artifact self-defeating - which is not what an author asserts by "
            "qualifying their own earlier objection. `objection.o4` against `o1`/`o2` is "
            "exactly this case; it is dropped, not retargeted, and counted under its own "
            "code so the loss is visible rather than silent"
        ),
    },
    {
        "code": "claim_record_unmapped",
        "what": "an FCL `claim` record maps to no spec construct",
        "why": (
            "a claim asserts content without proposing a test, so it is neither an "
            "observation-valued commitment nor a criticism nor a problem; it survives in the "
            "artifact body and in the FCL-1 document artifact, and is reported here because "
            "`uptake_refs_unmapped` covers only the claims the author put in `uptake`"
        ),
    },
)


@dataclass(frozen=True)
class ImportReport:
    """The outcome of one import; also written as ``report.json``."""

    occurrence: str
    out_root: str | None
    dry_run: bool
    scope: tuple[dict[str, Any], ...]
    spec_id_table: dict[str, str]
    names: dict[str, str]
    events_count: int
    labels: dict[str, str]
    att_edges: tuple[tuple[str, str], ...]
    dep_edges: tuple[tuple[str, str], ...]
    warrants: tuple[dict[str, Any], ...]
    commitments: tuple[dict[str, Any], ...]
    problems: tuple[dict[str, Any], ...]
    residue: tuple[dict[str, Any], ...]
    residue_totals: dict[str, int]
    resolution: dict[str, int]
    custody: dict[str, Any]
    why_chains: dict[str, str]
    #: The fixed multi-arm paragraph, or None for a single-arm scope.
    multi_arm_framing: str | None = None
    #: node spec artifact id -> one of COMMITMENT_SURFACE_STATES.
    commitment_surface_states: dict[str, str] = field(default_factory=dict)
    deviations: tuple[dict[str, str], ...] = DEVIATIONS

    @property
    def error_severity_totals(self) -> dict[str, int]:
        """Nonzero residue counts whose severity is ``error``."""
        return {
            code: count
            for code, count in sorted(self.residue_totals.items())
            if count and RESIDUE_CODES[code]["severity"] == "error"
        }

    def why(self, artifact_id: str) -> str:
        """The attack/defence chain justifying an artifact's label (spec §13)."""
        return self.why_chains[self.resolve_artifact(artifact_id)]

    def resolve_artifact(self, reference: str) -> str:
        """Resolve an artifact id, a unique id prefix, or a readable name."""
        if reference in self.labels:
            return reference
        by_name = [aid for aid, name in sorted(self.names.items()) if name == reference]
        if len(by_name) == 1:
            return by_name[0]
        by_prefix = [aid for aid in sorted(self.labels) if aid.startswith(reference)]
        if len(by_prefix) == 1:
            return by_prefix[0]
        if not by_prefix and not by_name:
            raise KeyError(f"no artifact matches {reference!r}")
        raise KeyError(f"{reference!r} is ambiguous")

    def surface_of(self, artifact_id: str) -> str:
        """The rendered commitment-surface state for one artifact, or ``n/a``.

        Only node artifacts have a commitment surface; a validity node and an
        FCL-1 document artifact have none, and say so rather than inheriting
        the carrier's.
        """
        state = self.commitment_surface_states.get(artifact_id)
        if state is None:
            return SURFACE_NOT_APPLICABLE
        return SURFACE_COLUMN.get(state, state)

    def labels_table(self) -> str:
        """The labels table the CLI prints."""
        attackers = attack_index(self.att_edges)
        rows = [("artifact", "id", "status", "surface", "attacked by")]
        for aid in label_order(self.labels, self.names):
            rows.append(
                (
                    self.names.get(aid, "?"),
                    aid[:16],
                    self.labels[aid],
                    self.surface_of(aid),
                    ", ".join(self.names.get(a, a[:12]) for a in attackers.get(aid, [])) or "-",
                )
            )
        columns = len(rows[0])
        widths = [max(len(row[i]) for row in rows) for i in range(columns)]
        lines = []
        for index, row in enumerate(rows):
            lines.append("  ".join(value.ljust(widths[i]) for i, value in enumerate(row)).rstrip())
            if index == 0:
                lines.append("  ".join("-" * widths[i] for i in range(columns)))
        return "\n".join(lines)

    def residue_summary(self) -> str:
        lines = []
        for code, count in sorted(self.residue_totals.items()):
            if count:
                lines.append(
                    "  %-46s %-14s %-9s %d"
                    % (code, RESIDUE_CODES[code]["severity"], RESIDUE_CODES[code]["unit"], count)
                )
        zeros = sorted(code for code, count in self.residue_totals.items() if not count)
        lines.append(f"  ({len(zeros)} codes with count 0: {', '.join(zeros)})")
        return "\n".join(lines)

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": REPORT_SCHEMA,
            "importer_version": IMPORTER_VERSION,
            "occurrence": self.occurrence,
            "dry_run": self.dry_run,
            "invariant_i7": I7_BANNER,
            "multi_arm_framing": self.multi_arm_framing,
            "commitment_surface_states": dict(self.commitment_surface_states),
            "error_severity_residue": self.error_severity_totals,
            "scope": list(self.scope),
            "events_count": self.events_count,
            "spec_id_table": dict(self.spec_id_table),
            "names": dict(self.names),
            "labels": dict(self.labels),
            "att_edges": [list(edge) for edge in self.att_edges],
            "dep_edges": [list(edge) for edge in self.dep_edges],
            "warrants": [dict(w) for w in self.warrants],
            "commitments": [dict(c) for c in self.commitments],
            "problems": [dict(p) for p in self.problems],
            "residue": [dict(r) for r in self.residue],
            "residue_totals": dict(self.residue_totals),
            "reference_resolution": dict(self.resolution),
            "custody": dict(self.custody),
            "why": dict(self.why_chains),
            "declared_deviations": [dict(d) for d in self.deviations],
        }

    def to_json(self) -> str:
        return json.dumps(self.as_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


# --------------------------------------------------------------------------- #
# per-node working state                                                       #
# --------------------------------------------------------------------------- #


@dataclass
class _Node:
    coord: Coordinate
    record: dict[str, Any]
    trace: dict[str, Any]
    receipt: dict[str, Any] | None
    attempt: dict[str, Any] | None
    absent_inputs: list[str]
    wave_id: str
    wave_ordinal: int
    wave_index: int
    document: dict[str, Any] | None = None
    #: one of COMMITMENT_SURFACE_STATES; what this import did with the
    #: authored ``commitments`` string, and why.
    commitment_surface_state: str = "read_fcl1"
    ts: str = ""
    label_index: dict[str, int] = field(default_factory=dict)
    task_labels: tuple[str, ...] = ()
    projections: list[dict[str, Any]] = field(default_factory=list)
    referenced_projections: set[int] = field(default_factory=set)
    commitment_records: list[dict[str, Any]] = field(default_factory=list)
    problem_records: list[dict[str, Any]] = field(default_factory=list)
    commitments: list[Commitment] = field(default_factory=list)
    problems: list[Problem] = field(default_factory=list)
    research_problems: list[Problem] = field(default_factory=list)
    mapped_to: dict[str, list[str]] = field(default_factory=dict)
    document_artifact_id: str = ""
    document_artifact_new: bool = False
    spec_id: str = ""
    interface: Interface = field(default_factory=Interface)
    register_seq: int = -1
    document_seq: int = -1

    @property
    def records(self) -> list[dict[str, Any]]:
        return list((self.document or {}).get("records", []))

    @property
    def local_ids(self) -> set[str]:
        return {r.get("id") for r in self.records}

    @property
    def surface(self) -> str:
        return "fcl1" if self.coord.arm in FCL_SURFACE_ARMS else "prose"


@dataclass
class _PlannedWarrant:
    warrant: Warrant
    carrier: _Node
    record_id: str
    target_id: str
    target_key: str
    target_kind: str  # "artifact" | "validity_node"
    nu_content: str
    nu_interface: Interface
    nu_id: str
    nu_seq: int = -1
    crit_seq: int = -1


# --------------------------------------------------------------------------- #
# the importer                                                                 #
# --------------------------------------------------------------------------- #


class _Importer:
    def __init__(
        self,
        occurrence_dir: Path,
        problems: Sequence[str] | None,
        arms: Sequence[str] | None,
        cycles: Sequence[int] | None,
    ) -> None:
        self.occurrence = Path(occurrence_dir)
        self.reader = _Reader(self.occurrence)
        self.ledger = _CustodyLedger()
        self.validator = fcl1_validator()
        self.wanted_problems = list(problems) if problems else None
        self.wanted_arms = list(arms) if arms else None
        self.wanted_cycles = [int(c) for c in cycles] if cycles else None
        self.residue: list[dict[str, Any]] = []
        self.record_codes: dict[tuple[str, str], list[str]] = {}
        self.nodes: dict[Coordinate, _Node] = {}
        self.order: list[Coordinate] = []
        self.planned_warrants: list[_PlannedWarrant] = []
        self.reified: dict[tuple[str, str], list[_PlannedWarrant]] = {}
        self.task_problems: dict[str, Problem] = {}
        self.records_table: list[dict[str, Any]] = []
        self.dep_edges: list[tuple[str, str]] = []
        self.document_artifacts: dict[str, str] = {}
        self.names: dict[str, str] = {}
        self.planned_events: list[dict[str, Any]] = []
        self.resolution = {"refs": 0, "resolved": 0, "extensions": 0, "dangling": 0, "task": 0}
        self.events_count = 0
        self.first_ts = ""
        self.last_ts = ""

    # -- residue ---------------------------------------------------------- #

    def add_residue(
        self,
        code: str,
        *,
        node: _Node | None = None,
        record: dict[str, Any] | None = None,
        field_name: str | None = None,
        ref: str | None = None,
        resolved_to: dict[str, Any] | None = None,
        reason: str = "",
        verbatim: str = "",
    ) -> None:
        if code not in RESIDUE_CODES:  # pragma: no cover - defensive
            raise MappingError(f"RESIDUE_CODE_OUTSIDE_VOCABULARY:{code}")
        carrier = None
        if node is not None:
            carrier = {
                "coordinate": node.coord.as_dict(),
                "spec_artifact_id": node.spec_id or None,
                "source_path": occurrence_path(node.coord, "artifacts"),
            }
        self.residue.append(
            {
                "code": code,
                "severity": RESIDUE_CODES[code]["severity"],
                "unit": RESIDUE_CODES[code]["unit"],
                "carrier": carrier,
                "record_id": (record or {}).get("id"),
                "record_type": (record or {}).get("type"),
                "field": field_name,
                "ref": ref,
                "resolved_to": resolved_to,
                "reason": reason,
                "verbatim": verbatim,
            }
        )
        if node is not None and record is not None and record.get("id"):
            self.record_codes.setdefault((node.coord.key, record["id"]), []).append(code)

    def residue_code_count(self, code: str) -> int:
        """How many entries this import has raised under one code so far."""
        if code not in RESIDUE_CODES:  # pragma: no cover - defensive
            raise MappingError(f"RESIDUE_CODE_OUTSIDE_VOCABULARY:{code}")
        return sum(1 for entry in self.residue if entry["code"] == code)

    # -- scope and waves --------------------------------------------------- #

    def discover_scope(self, material: dict[str, Any], plan: dict[str, Any]) -> list[Coordinate]:
        """Every coordinate the occurrence holds, then the ones the selectors keep.

        The two halves are separated so that a selector that matches nothing
        can say what the occurrence *does* hold. An occurrence with no
        coordinate at all is a different failure (``EMPTY_SCOPE``) from a
        selector that matched none of the coordinates there are
        (:class:`SelectorMatchedNothing`), and an operator fixes them
        differently. Every component is validated before it is used as a path
        segment.
        """
        available: list[Coordinate] = []
        artifacts_root = self.occurrence / "artifacts"
        for problem in [p["id"] for p in material.get("problems", [])]:
            safe_component(problem, "problem")
            for arm in list(plan.get("arms", [])):
                safe_component(arm, "arm")
                arm_dir = artifacts_root / problem / arm
                if not arm_dir.is_dir():
                    continue
                for cycle_dir in sorted(arm_dir.iterdir()):
                    if not cycle_dir.is_dir() or not cycle_dir.name.startswith("cycle"):
                        continue
                    digits = cycle_dir.name[len("cycle"):]
                    safe_component(digits, "cycle")
                    if not digits.isdigit():
                        raise CustodyError(f"COORDINATE_COMPONENT_UNSAFE:cycle:{digits!r}")
                    cycle = int(digits)
                    for path in sorted(cycle_dir.glob("*.json")):
                        safe_component(path.stem, "node")
                        available.append(Coordinate(problem, arm, cycle, path.stem))
        if not available:
            raise MappingError("EMPTY_SCOPE")
        coords = [
            coord
            for coord in available
            if not (self.wanted_problems and coord.problem not in self.wanted_problems)
            and not (self.wanted_arms and coord.arm not in self.wanted_arms)
            and not (self.wanted_cycles and coord.cycle not in self.wanted_cycles)
        ]
        if not coords:
            raise SelectorMatchedNothing(
                "SELECTOR_MATCHED_NOTHING: "
                + "; ".join(
                    f"--{name} {' '.join(str(v) for v in wanted)}"
                    for name, wanted in (
                        ("problem", self.wanted_problems or []),
                        ("arm", self.wanted_arms or []),
                        ("cycle", self.wanted_cycles or []),
                    )
                    if wanted
                )
                + f" matched none of this occurrence's {len(available)} coordinate(s). "
                + "It has problems: "
                + ", ".join(sorted({c.problem for c in available}))
                + "; arms: "
                + ", ".join(sorted({c.arm for c in available}))
                + "; cycles: "
                + ", ".join(str(c) for c in sorted({c.cycle for c in available}))
                + "."
            )
        return coords

    def load_waves(self) -> dict[Coordinate, tuple[str, int, int]]:
        placement: dict[Coordinate, tuple[str, int, int]] = {}
        wave_dir = self.occurrence / "waves"
        if not wave_dir.is_dir():
            raise CustodyError("WAVES_DIRECTORY_MISSING")
        for path in sorted(wave_dir.glob("wave*.json")):
            wave = self.reader.read_json(f"waves/{path.name}")
            if not isinstance(wave, dict) or wave.get("schema") != WAVE_RECORD_SCHEMA:
                raise CustodyError(f"WAVE_SCHEMA:{path.name}")
            wave_id = wave.get("wave_id")
            # The wave id is both a path segment (`waves/<wave_id>.json`, read
            # again in load_nodes) and an ordering key, so its shape is checked
            # rather than assumed: `wave["wave_id"][4:]` used to reach int()
            # unguarded and could raise a bare ValueError out of custody.
            if not isinstance(wave_id, str) or not re.match(r"^wave[0-9]+$", wave_id):
                raise CustodyError(f"WAVE_ID_MALFORMED:{path.name}:{wave_id!r}")
            safe_component(wave_id, "wave_id")
            if f"{wave_id}.json" != path.name:
                raise CustodyError(f"WAVE_ID_MISMATCH:{path.name}")
            ordinal = int(wave_id[4:])
            for index, raw in enumerate(wave.get("coordinates", [])):
                coord = Coordinate.from_dict(raw)
                if coord in placement:
                    raise CustodyError(f"COORDINATE_IN_TWO_WAVES:{coord.key}")
                placement[coord] = (wave_id, ordinal, index)
        return placement

    # -- node loading ------------------------------------------------------ #

    def load_nodes(self, scope: Sequence[Coordinate], plan: dict[str, Any]) -> None:
        placement = self.load_waves()
        self.ledger.node_totals(len(scope))
        for coord in scope:
            record = self.reader.read_json(occurrence_path(coord, "artifacts"))
            receipt, attempt, trace, absent = _verify_node_custody(
                self.reader, coord, record, self.ledger
            )
            if coord not in placement:
                raise CustodyError(f"COORDINATE_NOT_IN_ANY_WAVE:{coord.key}")
            wave_id, ordinal, index = placement[coord]
            if attempt is not None:
                if attempt.get("wave_id") != wave_id:
                    raise CustodyError(f"WAVE_ID_DISAGREES_WITH_ATTEMPT:{coord.key}")
                wave = self.reader.read_json(f"waves/{wave_id}.json")
                if wave.get("plan_id") != plan.get("plan_id"):
                    raise CustodyError(f"WAVE_PLAN_ID_MISMATCH:{wave_id}")
                if (wave.get("request_hashes") or {}).get(coord.wave_label) != attempt.get(
                    "request_sha256"
                ):
                    raise CustodyError(f"WAVE_REQUEST_HASH_MISMATCH:{coord.key}")
                self.ledger.ran("wave_placement")
            else:
                self.ledger.skipped("wave_placement", coord.key, "attempt")
            self.nodes[coord] = _Node(
                coord=coord,
                record=record,
                trace=trace,
                receipt=receipt,
                attempt=attempt,
                absent_inputs=absent,
                wave_id=wave_id,
                wave_ordinal=ordinal,
                wave_index=index,
            )
        self.order = sorted(
            self.nodes, key=lambda c: (self.nodes[c].wave_ordinal, self.nodes[c].wave_index, c)
        )
        self._assign_timestamps()
        # Custody for EVERY node, parsed document or not: the brief, the
        # projection index and the task label are read off the trace whatever
        # the commitment surface turns out to be.
        for coord in self.order:
            self._verify_projection_custody(self.nodes[coord])
        self._verify_projection_sources()

    def _assign_timestamps(self) -> None:
        """``Event.ts`` comes from ``responses/....finished_utc``; never a clock.

        A coordinate whose receipt is absent carries the timestamp of the
        *previous* coordinate in registration order: that is an observed time,
        not an invented one, and it keeps ``ts`` inside the interval the
        occurrence actually ran in. There is no previous coordinate for the
        first one, so a scope whose leading coordinate has no receipt is
        **refused** (``NO_LEADING_RECEIPT``) rather than back-dated to a
        timestamp that belongs to some later node. A scope with no receipt at
        all is refused as ``NO_FINISHED_UTC_IN_SCOPE``.

        ``ts`` is not required to be nondecreasing: a wave runs several arms
        concurrently and their ``finished_utc`` values interleave. Only ``seq``
        is contiguous (spec §14).
        """
        stamps = [
            self.nodes[c].receipt["finished_utc"]
            for c in self.order
            if self.nodes[c].receipt is not None
        ]
        if not stamps:
            raise CustodyError("NO_FINISHED_UTC_IN_SCOPE")
        if self.order and self.nodes[self.order[0]].receipt is None:
            raise CustodyError(f"NO_LEADING_RECEIPT:{self.order[0].key}")
        previous = ""
        for coord in self.order:
            node = self.nodes[coord]
            if node.receipt is None:
                node.ts = previous
                continue
            finished = node.receipt.get("finished_utc")
            if not isinstance(finished, str) or not finished:
                raise CustodyError(f"FINISHED_UTC_MISSING:{coord.key}")
            node.ts = previous = finished
        self.first_ts = min(stamps)
        self.last_ts = max(stamps)

    # -- documents and label index ----------------------------------------- #

    def parse_documents(self) -> None:
        """Dispatch on the parse outcome of the commitments string.

        ``envelope_status`` stays metadata (invariant I2): an empty commitments
        string is what actually makes the attack surface empty, and an arm that
        was instructed in prose never claimed to carry an FCL-1 document.
        """
        for coord in self.order:
            node = self.nodes[coord]
            raw = node.record.get("commitments", "")
            if raw == "":
                node.commitment_surface_state = "unavailable_decode_failure"
                self.add_residue(
                    "opaque_envelope",
                    node=node,
                    reason=OPAQUE_ENVELOPE_REASON + " " + ACCEPT_BY_POSITION,
                    verbatim=node.record.get("envelope_status", ""),
                )
                continue
            if node.surface != "fcl1":
                node.commitment_surface_state = "prose_not_parsed"
                self.add_residue(
                    "prose_commitment_surface",
                    node=node,
                    reason=f"arm {coord.arm!r} " + PROSE_SURFACE_REASON,
                    verbatim=raw[:2000],
                )
                continue
            document, failure, detail = parse_fcl1_document(raw, self.validator)
            if failure is not None:
                node.commitment_surface_state = failure
                self.add_residue(
                    failure,
                    node=node,
                    reason=(
                        detail + " - the artifact stays opaque; nothing is repaired (I4). "
                        "The commitment surface is UNAVAILABLE to this import, which is not "
                        "the same as the author having declined to commit. " +
                        ACCEPT_BY_POSITION
                    ),
                    verbatim=raw[:2000],
                )
                continue
            node.document = document
            node.commitment_surface_state = "read_fcl1"

    def _verify_projection_custody(self, node: _Node) -> None:
        """Custody half of the old ``_build_label_index``: runs for EVERY node.

        The brief hash, the projection-id shape, the agreement between the
        brief's rendered labels and the projection slots, and the task label are
        properties of the *trace*, not of the commitments string. A node whose
        commitment surface was never read still has a trace, and refusing to
        check it because the arm wrote prose would leave a whole arm
        uncustodied. The resolver half - actually *using* this index to resolve
        an FCL ref - is gated on a parsed document in :meth:`resolve_ref`.
        """
        projections = list(node.trace.get("projection_artifacts") or [])
        node.projections = projections
        index: dict[str, int] = {}
        for position, projection in enumerate(projections):
            artifact_id = projection.get("artifact_id")
            if not isinstance(artifact_id, str) or len(artifact_id) != 64:
                raise CustodyError(f"PROJECTION_ARTIFACT_ID:{node.coord.key}")
            index[artifact_id[:16]] = position
        brief = node.trace.get("original_brief") or ""
        if sha256_bytes(brief.encode("utf-8")) != node.trace.get("original_brief_sha256"):
            raise CustodyError(f"BRIEF_SHA256_MISMATCH:{node.coord.key}")
        self.ledger.ran("brief_pinned")
        seen: set[str] = set()
        for match in _BRIEF_LABEL_LINE.finditer(brief):
            hex_label, alias = match.group(1), match.group(2)
            position = int(alias.rsplit(".", 1)[1])
            if (
                position >= len(projections)
                or projections[position]["artifact_id"][:16] != hex_label
            ):
                raise CustodyError(f"BRIEF_LABEL_INDEX_DISAGREES:{node.coord.key}:{alias}")
            index[alias] = position
            seen.add(hex_label)
        if seen != {p["artifact_id"][:16] for p in projections}:
            raise CustodyError(f"BRIEF_LABEL_SET_DISAGREES:{node.coord.key}")
        self.ledger.ran("brief_label_index")
        node.label_index = index
        # The task artifact is exposed under the same line shape; it is not a
        # projection slot and resolves to the task problem, never to an edge.
        task = node.trace.get("task_artifact") or {}
        task_labels = [match.group(1) for match in _BRIEF_TASK_LINE.finditer(brief)]
        if task.get("artifact_id"):
            if task_labels and task_labels != [task["artifact_id"][:16]]:
                raise CustodyError(f"TASK_LABEL_DISAGREES:{node.coord.key}")
            node.task_labels = (task["artifact_id"][:16], _TASK_ALIAS)
        elif task_labels:
            node.task_labels = (task_labels[0], _TASK_ALIAS)
        self.ledger.ran("task_label")

    def projection_subject(self, node: _Node, index: int) -> str:
        """``<coordinate>#<slot>`` - one projection, named the way the brief names it."""
        alias = next(
            (
                label
                for label, position in sorted(node.label_index.items())
                if position == index and "." in label
            ),
            node.projections[index]["artifact_id"][:16],
        )
        return f"{node.coord.key}#{alias}"

    def _verify_projection_sources(self) -> None:
        """Hop-2 integrity, counted per projection rather than per node.

        Each non-absent projection names the artifact record it exposed and
        repeats that record's hashes. When the named coordinate is inside the
        imported scope the two must agree; when it is outside - or when the
        slot exposed nothing at all - the check cannot run *for that slot*.
        Counting per node hid that: one checkable projection made the whole
        node count as verified, so a node with three out-of-scope sources and
        one in-scope source rendered exactly like a node with four in-scope
        sources. The unit is the projection, and every slot the check could not
        run over is named in the rendered result.
        """
        total = 0
        for coord in self.order:
            node = self.nodes[coord]
            for index, projection in enumerate(node.projections):
                total += 1
                source = projection.get("selected_source") or {}
                if source.get("absent"):
                    self.ledger.skipped(
                        "projection_source",
                        self.projection_subject(node, index),
                        "exposed source (the slot is absent)",
                    )
                    continue
                owner = Coordinate.from_dict(source.get("coordinate"))
                owner_node = self.nodes.get(owner)
                if owner_node is None:
                    self.ledger.skipped(
                        "projection_source",
                        self.projection_subject(node, index),
                        "in-scope owner (%s)" % owner.key,
                    )
                    continue
                for name in ("artifact_id", "body_sha256", "commitments_sha256"):
                    if owner_node.record.get(name) != source.get(name):
                        raise CustodyError(f"PROJECTION_SOURCE_MISMATCH:{owner.key}:{name}")
                self.ledger.ran("projection_source")
        self.ledger.total("projection_source", total)

    # -- reference resolution (mapping.md §6) ------------------------------- #

    def resolve_ref(
        self, node: _Node, ref: str, record: dict[str, Any] | None, field_name: str
    ) -> tuple[Coordinate | None, str | None]:
        """Two-hop resolution of one FCL ref to an owning coordinate."""
        self.resolution["refs"] += 1
        label = ref.partition("#")[0] if "#" in ref else ref
        if label in node.task_labels:
            self.resolution["task"] += 1
            self.resolution["resolved"] += 1
            self.add_residue(
                "ref_to_task_artifact",
                node=node,
                record=record,
                field_name=field_name,
                ref=ref,
                reason=(
                    "resolves to the exposed task artifact, which this import registers as "
                    "the root Problem, not as an artifact; no ref and no edge is minted"
                ),
                verbatim=ref,
            )
            return None, None
        if "#" in ref:
            return self._resolve_qualified(node, ref, record, field_name)
        if ref in node.local_ids:
            self.resolution["resolved"] += 1
            return node.coord, ref
        position = node.label_index.get(ref)
        if position is not None:
            owner, _view = self._projection_source(node, position, record, field_name, ref)
            if owner is None:
                return None, None
            self.resolution["extensions"] += 1
            self.add_residue(
                "bare_label_ref",
                node=node,
                record=record,
                field_name=field_name,
                ref=ref,
                resolved_to={"coordinate": owner.as_dict(), "record_id": None},
                reason=(
                    "bare exposed-artifact label with no '#LocalName'; local resolution was "
                    "tried first, so it resolves to the owning artifact (deviation D2)"
                ),
                verbatim=ref,
            )
            return owner, None
        self._unresolved(
            node, record, field_name, ref,
            "neither a local record name nor an exposed-artifact label",
        )
        return None, None

    def _resolve_qualified(
        self, node: _Node, ref: str, record: dict[str, Any] | None, field_name: str
    ) -> tuple[Coordinate | None, str | None]:
        label, _, local = ref.partition("#")
        position = node.label_index.get(label)
        if position is None:
            self._unresolved(
                node, record, field_name, ref,
                "exposed-artifact label is not in this node's projection index",
            )
            return None, None
        owner, view = self._projection_source(node, position, record, field_name, ref)
        if owner is None:
            return None, None
        owner_node = self.nodes[owner]
        if local in owner_node.local_ids:
            # A real local name always wins, including the name "BODY".
            self.resolution["resolved"] += 1
            if view == "body":
                self.add_residue(
                    "ref_through_unexposed_view",
                    node=node,
                    record=record,
                    field_name=field_name,
                    ref=ref,
                    resolved_to={"coordinate": owner.as_dict(), "record_id": local},
                    reason=(
                        "the projection exposed view == 'body', so this record-level name "
                        "was never readable through it; resolved anyway because the record "
                        "does exist"
                    ),
                    verbatim=ref,
                )
            return owner, local
        if local == _BODY_PSEUDO_LOCAL:
            self.resolution["extensions"] += 1
            self.add_residue(
                "qualified_ref_body_pseudo_local",
                node=node,
                record=record,
                field_name=field_name,
                ref=ref,
                resolved_to={"coordinate": owner.as_dict(), "record_id": None},
                reason=(
                    "no local record is named BODY in the owning document, so the rendered "
                    "section header is admitted by convention and resolves to the owning "
                    "artifact (deviation D1)"
                ),
                verbatim=ref,
            )
            if view == "commitments":
                # The BODY convention names a section the projection did not
                # render: under view == 'commitments' the brief carried a
                # COMMITMENTS section and no BODY section at all, so the author
                # cited a heading that was not in front of them.
                self.add_residue(
                    "ref_through_unexposed_view",
                    node=node,
                    record=record,
                    field_name=field_name,
                    ref=ref,
                    resolved_to={"coordinate": owner.as_dict(), "record_id": None},
                    reason=(
                        "the projection exposed view == 'commitments', so no BODY section "
                        "was rendered in this brief; the pseudo-local BODY header was never "
                        "readable through it. Resolved to the owning artifact anyway, and "
                        "reported."
                    ),
                    verbatim=ref,
                )
            return owner, None
        if owner_node.document is None:
            self._unresolved(
                node, record, field_name, ref,
                "the owning artifact has no readable FCL-1 document",
                resolved_to={"coordinate": owner.as_dict(), "record_id": local},
            )
            return None, None
        self._unresolved(
            node, record, field_name, ref,
            "no record with that local name in the owning document",
            resolved_to={"coordinate": owner.as_dict(), "record_id": local},
        )
        return None, None

    def _unresolved(
        self,
        node: _Node,
        record: dict[str, Any] | None,
        field_name: str,
        ref: str,
        reason: str,
        resolved_to: dict[str, Any] | None = None,
        code: str = "ref_unresolved",
    ) -> None:
        self.resolution["dangling"] += 1
        self.add_residue(
            code,
            node=node,
            record=record,
            field_name=field_name,
            ref=ref,
            resolved_to=resolved_to,
            reason=reason + "; dropped, never invented",
            verbatim=ref,
        )

    def _projection_source(
        self,
        node: _Node,
        position: int,
        record: dict[str, Any] | None,
        field_name: str,
        ref: str,
    ) -> tuple[Coordinate | None, str | None]:
        source = node.projections[position].get("selected_source") or {}
        if source.get("absent"):
            self._unresolved(
                node, record, field_name, ref,
                "selected_source.absent == true: the projection exposed nothing",
                code="ref_through_absent_projection",
            )
            return None, None
        owner = Coordinate.from_dict(source.get("coordinate"))
        owner_node = self.nodes.get(owner)
        if owner_node is None or not owner_node.spec_id:
            self._unresolved(
                node, record, field_name, ref,
                f"the owning artifact {owner.key} is outside the imported scope or is not "
                "registered yet in wave order",
                resolved_to={"coordinate": owner.as_dict(), "record_id": None},
                code="ref_to_unregistered_target_dropped",
            )
            return None, None
        # Hop 2 integrity (mapping.md §6) is verified for every projection of
        # every node in _verify_projection_sources, before any ref is resolved;
        # re-checking it here would be the same comparison twice.
        node.referenced_projections.add(position)
        return owner, source.get("view")

    # -- record mapping ----------------------------------------------------- #

    def map_records(self) -> None:
        for coord in self.order:
            node = self.nodes[coord]
            if node.document is None:
                node.interface = Interface()
                self._name_artifact(node)
                # Projection residue is custody-shaped, not document-shaped: a
                # node whose commitment surface was never read still had
                # material exposed to it, and that exposure is reportable.
                self._record_projection_residue(node)
                continue
            self._register_document_artifact(node)
            self._map_content(node)
            self._name_artifact(node)
            self._attach_provenance(node)
            self._map_objections(node)
            self._record_projection_residue(node)
            for record in node.records:
                self.records_table.append(
                    {
                        "coordinate": coord.as_dict(),
                        "record_id": record.get("id"),
                        "record_type": record.get("type"),
                        "record_sha256": sha256_hex(canonical_json(record)),
                        "owning_spec_artifact_id": node.spec_id,
                        "mapped_to": node.mapped_to.get(record.get("id"), []),
                        "residue_codes": sorted(
                            set(self.record_codes.get((coord.key, record.get("id")), []))
                        ),
                    }
                )

    def _register_document_artifact(self, node: _Node) -> None:
        """The FCL-1 document is an addressable artifact of its own.

        codec ``json``, content_ref the recorded ``commitments_sha256``, empty
        Interface. The node artifact carries a ``mention`` ref to it, which is
        inert in ``build_att``, so ``theory(id)`` and ``why`` can reach the
        document without it acquiring an attack surface.
        """
        content_ref = node.record["commitments_sha256"]
        document_id = Artifact.compute_id(content_ref, "json", Interface())
        node.document_artifact_id = document_id
        node.document_artifact_new = document_id not in self.document_artifacts
        if node.document_artifact_new:
            self.document_artifacts[document_id] = node.coord.key
            self.names[document_id] = f"{node.coord.key}#commitments"

    def _map_content(self, node: _Node) -> None:
        """Pass 1: everything that does not need the carrier's own spec id."""
        mentions: set[str] = set()
        dependences: list[str] = []
        document = node.document or {}
        uptake = list(document.get("uptake", []))
        for record in node.records:
            record_type = record.get("type")
            if record_type == "commitment":
                self._map_commitment(node, record, uptake)
            elif record_type == "problem":
                self._map_problem_record(node, record)
            elif record_type == "use":
                self.add_residue(
                    "use_record_unmapped",
                    node=node,
                    record=record,
                    reason=(
                        "a use record proposes future uptake; it is neither a testable "
                        "commitment nor a criticism and has no spec construct"
                    ),
                    verbatim=json.dumps(record, ensure_ascii=False, sort_keys=True),
                )
            elif record_type == "claim":
                self.add_residue(
                    "claim_record_unmapped",
                    node=node,
                    record=record,
                    reason=(
                        "a claim record asserts content without proposing a test: it is "
                        "neither an observation-valued commitment (no action/consequence to "
                        "schedule), nor a criticism, nor a problem, so it maps to no spec "
                        "construct and survives only as part of the artifact body and of the "
                        "FCL-1 document artifact. Its own refs are still resolved and "
                        "reported. A claim in the document's uptake list is additionally "
                        "covered by uptake_refs_unmapped; a claim the author left OUT of "
                        "uptake is covered by nothing else, which is why this code exists."
                    ),
                    verbatim=json.dumps(record, ensure_ascii=False, sort_keys=True),
                )
            if record_type != "commitment" and "consequence" in record:
                self.add_residue(
                    "consequence_on_non_commitment_record",
                    node=node,
                    record=record,
                    field_name="consequence",
                    reason=(
                        "testable content outside interface.commitments; the importer does "
                        "not promote it, which would override the author's own typing"
                    ),
                    verbatim=record["consequence"],
                )
            if record_type != "objection" and "target" in record:
                self.add_residue(
                    "target_on_non_objection_record",
                    node=node,
                    record=record,
                    field_name="target",
                    reason=(
                        "'target' here means 'about', not 'attacks'; only type == 'objection' "
                        "mints a warrant (observed deviation D3)"
                    ),
                    verbatim=json.dumps(record["target"], ensure_ascii=False),
                )
            mentions.update(self._map_mention_refs(node, record))
            dependences.extend(self._map_depends_refs(node, record))
        self.add_residue(
            "uptake_lists_unmapped",
            node=node,
            field_name="uptake",
            reason=(
                "uptake is a local claim about standing, never a harness verdict, status or "
                "acceptance"
            ),
            verbatim=json.dumps(uptake, ensure_ascii=False),
        )
        for ref in uptake:
            self.resolve_ref(node, ref, None, "uptake")
            self.add_residue(
                "uptake_refs_unmapped",
                node=node,
                field_name="uptake",
                ref=ref,
                reason="uptake refs are never mapped to an edge, a status or a label",
                verbatim=ref,
            )
        mentions.add(node.document_artifact_id)
        refs = [Ref(target=t, role=RefRole.DEPENDENCE) for t in sorted(set(dependences))]
        refs += [Ref(target=t, role=RefRole.MENTION) for t in sorted(mentions - set(dependences))]
        node.interface = Interface(
            commitments=sorted(self._commitment_id(node, r) for r in node.commitment_records),
            refs=sorted(refs, key=lambda r: (r.target, r.role.value)),
        )

    def _name_artifact(self, node: _Node) -> None:
        node.spec_id = Artifact.compute_id(node.record["body_sha256"], "utf8", node.interface)
        self.names[node.spec_id] = node.coord.key

    @staticmethod
    def _commitment_id(node: _Node, record: dict[str, Any]) -> str:
        return f"k:h005.fcl1:{node.coord.key}#{record['id']}"

    def _attach_provenance(self, node: _Node) -> None:
        """Build commitments and problems now the carrier's spec id exists.

        ``budget.extra`` deliberately uses the prefixed key
        ``h005_source_artifact``: ``adjudication/edges.py`` reserves the bare
        ``source_artifact`` key for its source-artifact attack closure, and no
        closure may fire by accident on imported material.
        """
        node.commitments = [
            Commitment(
                id=self._commitment_id(node, record),
                # Deliberately OUTSIDE the three executable eval classes
                # (program:/rubric:/predicate:) so nothing can dispatch it.
                # Content-addressed, so two importers over the same bytes mint
                # the same string. Spec §12 routes the gap into a research
                # problem instead of a verdict.
                eval=f"observation:h005.fcl1@{sha256_hex(canonical_json(record))}",
                budget=Budget(
                    steps=0,
                    time_ms=0,
                    extra={
                        "h005_record_id": record["id"],
                        "h005_source_artifact": node.spec_id,
                        "h005_scope": record.get("scope", ""),
                        "h005_action": record.get("action", ""),
                        "h005_consequence": record.get("consequence", ""),
                    },
                ),
                observation_valued=True,
            )
            for record in node.commitment_records
        ]
        for commitment in node.commitments:
            if commitment.eval.split(":", 1)[0] in ("program", "rubric", "predicate"):
                raise MappingError(f"COMMITMENT_EVAL_LOOKS_EXECUTABLE:{commitment.id}")
        node.problems = [
            Problem(
                id=f"pi:h005.fcl1:{node.coord.key}#{record['id']}",
                description=record.get("text", ""),
                criteria=[],
                provenance=ProblemProvenance.model_validate(
                    {"trigger": SpawnTrigger.SEED.value, "from": [node.spec_id]}
                ),
            )
            for record in node.problem_records
        ]
        by_id = {self._commitment_id(node, r): r for r in node.commitment_records}
        node.research_problems = [
            Problem(
                id=f"pi:h005.fcl1.research:{commitment_id}",
                description=(
                    "Observation-valued commitment with no covering evidence "
                    f"({node.coord.key}#{by_id[commitment_id]['id']}): "
                    f"{by_id[commitment_id].get('text', '')}"
                ),
                # criteria stay empty: an instantiated commitment id is not a
                # criterion (criteria are commitment SCHEMA ids, spec §1). The
                # originating commitment is named in provenance.from.
                criteria=[],
                provenance=ProblemProvenance.model_validate(
                    {
                        "trigger": SpawnTrigger.RESEARCH.value,
                        "from": [node.spec_id, commitment_id],
                    }
                ),
            )
            for commitment_id in sorted(by_id)
        ]
        for research in node.research_problems:
            self.add_residue(
                "problem_trigger_research_not_in_v13_enum",
                node=node,
                field_name="provenance.trigger",
                reason=(
                    f"{research.id} uses SpawnTrigger.RESEARCH, which the vendored enum has "
                    "and spec §12 describes, but which is not part of the v1.3 enum text; "
                    "criteria are empty and the originating commitment is in provenance.from"
                ),
                verbatim=research.id,
            )

    def _map_commitment(
        self, node: _Node, record: dict[str, Any], uptake: Sequence[str]
    ) -> None:
        commitment_id = self._commitment_id(node, record)
        node.commitment_records.append(record)
        node.mapped_to.setdefault(record["id"], []).extend(
            [f"commitment:{commitment_id}", f"problem:pi:h005.fcl1.research:{commitment_id}"]
        )
        self.add_residue(
            "commitment_not_executable",
            node=node,
            record=record,
            reason=(
                "observation-valued commitment with no covering evidence artifact: it spawns "
                "a research problem (spec §12) and stays scheduled-pending, never failed. The "
                "eval string is a content-addressed placeholder outside every executable "
                "eval class, so nothing can dispatch it."
            ),
            verbatim=record.get("text", ""),
        )
        if record["id"] not in uptake:
            self.add_residue(
                "commitment_record_not_in_uptake",
                node=node,
                record=record,
                field_name="uptake",
                reason=(
                    "the author did not put this commitment in the document's uptake list. "
                    "Uptake is a local standing claim and never a status, so the commitment "
                    "is imported unchanged; the divergence is reported, not resolved."
                ),
                verbatim=record.get("text", ""),
            )

    def _map_problem_record(self, node: _Node, record: dict[str, Any]) -> None:
        problem_id = f"pi:h005.fcl1:{node.coord.key}#{record['id']}"
        node.problem_records.append(record)
        node.mapped_to.setdefault(record["id"], []).append(f"problem:{problem_id}")
        self.add_residue(
            "problem_trigger_approximated",
            node=node,
            record=record,
            field_name="provenance.trigger",
            reason=(
                "SpawnTrigger has no 'import' member; 'seed' is the only trigger that does "
                "not assert an in-graph derivation, but it slightly over-claims for a problem "
                "carried in from another study. The clean fix is an enum addition."
            ),
            verbatim=record.get("text", ""),
        )

    def _map_mention_refs(self, node: _Node, record: dict[str, Any]) -> set[str]:
        """``mentions`` plus ``target`` on non-objection records -> mention refs."""
        owners: set[str] = set()
        fields = ["mentions", "revises", "withdraws"]
        if record.get("type") != "objection":
            fields.append("target")
        for field_name in fields:
            for ref in record.get(field_name, []) or []:
                owner, record_id = self.resolve_ref(node, ref, record, field_name)
                if field_name in ("revises", "withdraws"):
                    self.add_residue(
                        f"{field_name}_unmapped",
                        node=node,
                        record=record,
                        field_name=field_name,
                        ref=ref,
                        reason=(
                            "the spec has no supersession relation; nothing is deleted and "
                            "status is computed, so this becomes a mention ref only"
                        ),
                        verbatim=ref,
                    )
                if owner is None:
                    continue
                if owner == node.coord:
                    self.add_residue(
                        "mentions_intra_document",
                        node=node,
                        record=record,
                        field_name=field_name,
                        ref=ref,
                        resolved_to={"coordinate": owner.as_dict(), "record_id": record_id},
                        reason=(
                            "resolves to the carrier itself; a self-mention carries no "
                            "artifact-level information and is dropped. The record-level "
                            "relation survives only in the side table."
                        ),
                        verbatim=ref,
                    )
                    continue
                owners.add(self.nodes[owner].spec_id)
        return owners

    def _map_depends_refs(self, node: _Node, record: dict[str, Any]) -> list[str]:
        targets: list[str] = []
        for ref in record.get("depends", []) or []:
            owner, record_id = self.resolve_ref(node, ref, record, "depends")
            if owner is None:
                continue
            resolved = {"coordinate": owner.as_dict(), "record_id": record_id}
            if owner == node.coord:
                self.add_residue(
                    "depends_intra_document",
                    node=node,
                    record=record,
                    field_name="depends",
                    ref=ref,
                    resolved_to=resolved,
                    reason=(
                        "resolves to the carrier itself; a dep self-loop is a cycle (spec §1), "
                        "so the edge is dropped"
                    ),
                    verbatim=ref,
                )
                continue
            candidate = (node.coord.key, owner.key)
            if self._would_cycle(candidate):
                self.add_residue(
                    "dependence_cycle_rejected",
                    node=node,
                    record=record,
                    field_name="depends",
                    ref=ref,
                    resolved_to=resolved,
                    reason="the later-registered dependence edge would make dep cyclic",
                    verbatim=ref,
                )
                continue
            if candidate not in self.dep_edges:
                self.dep_edges.append(candidate)
            targets.append(self.nodes[owner].spec_id)
            self.add_residue(
                "depends_cross_document",
                node=node,
                record=record,
                field_name="depends",
                ref=ref,
                resolved_to=resolved,
                reason="explicit cross-document depends: mapped to a dependence ref",
                verbatim=ref,
            )
        return targets

    def _would_cycle(self, candidate: tuple[str, str]) -> bool:
        edges = list(self.dep_edges) + [candidate]
        try:
            toposort({n for edge in edges for n in edge}, edges)
        except Exception:
            return True
        return False

    def _map_objections(self, node: _Node) -> None:
        """Pass 2: objections, which need the carrier's and targets' spec ids."""
        for record in node.records:
            if record.get("type") != "objection":
                continue
            if "grounds" not in record:
                self.add_residue(
                    "grounds_absent_on_objection",
                    node=node,
                    record=record,
                    field_name="grounds",
                    reason=(
                        "the validity node carries text + bearing (+ scope) only; no grounds "
                        "were authored"
                    ),
                    verbatim=record.get("bearing", ""),
                )
            targets = record.get("target")
            if not targets:
                self.add_residue(
                    "objection_untargeted",
                    node=node,
                    record=record,
                    field_name="target",
                    reason="no target field: nothing to attack, so no warrant is minted",
                    verbatim=record.get("text", ""),
                )
                continue
            chosen: dict[str, tuple[str, Any]] = {}
            for ref in targets:
                owner, record_id = self.resolve_ref(node, ref, record, "target")
                if owner is None:
                    continue
                if owner == node.coord:
                    self.add_residue(
                        "objection_target_self_ref_dropped",
                        node=node,
                        record=record,
                        field_name="target",
                        ref=ref,
                        resolved_to={"coordinate": owner.as_dict(), "record_id": record_id},
                        reason=(
                            "a target ref resolving to the carrier is removed: at node "
                            "granularity it would be a Dung self-attack, which is not what "
                            "the author asserted"
                        ),
                        verbatim=ref,
                    )
                    local = self.reified.get((owner.key, record_id)) if record_id else None
                    if local:
                        # The declared exception to the §2(7) retargeting rule.
                        self.add_residue(
                            "criticism_of_criticism_intra_document_dropped",
                            node=node,
                            record=record,
                            field_name="target",
                            ref=ref,
                            resolved_to={
                                "coordinate": owner.as_dict(),
                                "record_id": record_id,
                            },
                            reason=(
                                "intra-document criticism of a criticism: the referenced "
                                "record was itself reified as a warrant ("
                                + ", ".join(sorted(p.warrant.id for p in local))
                                + "), but its carrier is this same artifact, so retargeting "
                                "onto that warrant's validity node would become a SELF-attack "
                                "through the spec §1 carrier closure - an attack on the nu is "
                                "lifted onto every carrier of the warrant, and the carrier "
                                "here is the objector itself. That would make the artifact "
                                "self-defeating, which is not what an intra-document "
                                "criticism asserts. It is therefore NOT retargeted; it is "
                                "dropped and counted here so the loss stays visible."
                            ),
                            verbatim=ref,
                        )
                    continue
                reified = self.reified.get((owner.key, record_id)) if record_id else None
                if reified:
                    # Criticism of a criticism: attack the validity node of the
                    # warrant this import minted from that record (spec §1
                    # closure lifts it onto the warrant and its carriers).
                    for planned in reified:
                        chosen[planned.nu_id] = ("validity_node", planned)
                    self.add_residue(
                        "criticism_of_criticism_retargeted",
                        node=node,
                        record=record,
                        field_name="target",
                        ref=ref,
                        resolved_to={"coordinate": owner.as_dict(), "record_id": record_id},
                        reason=(
                            "the referenced record was itself reified as a warrant, so this "
                            "criticism attacks that warrant's validity node ("
                            + ", ".join(sorted(p.warrant.id for p in reified))
                            + ") rather than the node artifact"
                        ),
                        verbatim=ref,
                    )
                else:
                    chosen[self.nodes[owner].spec_id] = ("artifact", owner)
            if not chosen:
                self.add_residue(
                    "objection_self_target_only",
                    node=node,
                    record=record,
                    field_name="target",
                    reason=(
                        "every target was document-local: intra-document dialectic is lost at "
                        "node granularity and mints nothing"
                    ),
                    verbatim=record.get("text", ""),
                )
                continue
            for target_id in sorted(chosen):
                kind, handle = chosen[target_id]
                planned = self._mint_warrant(node, record, target_id, kind, handle)
                node.mapped_to.setdefault(record["id"], []).append(
                    f"warrant:{planned.warrant.id}"
                )
                self.reified.setdefault((node.coord.key, record["id"]), []).append(planned)

    def _mint_warrant(
        self,
        node: _Node,
        record: dict[str, Any],
        target_id: str,
        kind: str,
        handle: Any,
    ) -> _PlannedWarrant:
        if kind == "validity_node":
            target_key = f"nu({handle.warrant.id})"
            target_display = f"nu({handle.carrier.coord.node}#{handle.record_id})"
        else:
            target_key = handle.key
            target_display = handle.node
        lines = [
            f"nu: {node.coord.key}#{record['id']} is an authored criticism directed at "
            f"{target_id}; its soundness and relevance are not asserted by this import.",
            f"TEXT: {record.get('text', '')}",
        ]
        for key in ("grounds", "bearing", "scope"):
            if key in record:
                lines.append(f"{key.upper()}: {record[key]}")
        lines.append(f"TARGET-REFS: {', '.join(record.get('target', []))}")
        nu_content = "\n".join(lines)
        # Literal order: target first, carrier second. Both are mentions, which
        # build_att treats as inert.
        nu_interface = Interface(
            refs=[
                Ref(target=target_id, role=RefRole.MENTION),
                Ref(target=node.spec_id, role=RefRole.MENTION),
            ]
        )
        nu_id = Artifact.compute_id(sha256_bytes(nu_content.encode("utf-8")), "utf8", nu_interface)
        planned = _PlannedWarrant(
            warrant=Warrant(
                id=f"w:h005.fcl1:{node.coord.key}#{record['id']}->{target_key}",
                target=target_id,
                type=WarrantType.ARGUMENTATIVE,
                commitment=None,
                verdict=None,
                trace_ref=None,
                validity_node=nu_id,
            ),
            carrier=node,
            record_id=record["id"],
            target_id=target_id,
            target_key=target_key,
            target_kind=kind,
            nu_content=nu_content,
            nu_interface=nu_interface,
            nu_id=nu_id,
        )
        self.planned_warrants.append(planned)
        self.names[nu_id] = f"nu:{node.coord.node}#{record['id']}->{target_display}"
        self.add_residue(
            "validity_node_minted_unasserted",
            node=node,
            record=record,
            reason=(
                "spec §1 has the validity node assert that the test is sound and relevant. "
                "This import asserts no such thing: the node is minted so the warrant is "
                "attackable (N1) and carries the author's criticism verbatim. Its own label "
                "is bookkeeping, not an endorsement."
            ),
            verbatim=nu_id,
        )
        return planned

    def _record_projection_residue(self, node: _Node) -> None:
        for index, projection in enumerate(node.projections):
            source = projection.get("selected_source") or {}
            alias = self.projection_subject(node, index).partition("#")[2]
            if source.get("absent"):
                self.add_residue(
                    "projection_absent",
                    node=node,
                    field_name="projection_artifacts",
                    ref=alias,
                    reason=(
                        f"projection slot {alias} (source {source.get('source')!r}) exposed "
                        "nothing; any ref through it is unresolvable"
                    ),
                    verbatim=json.dumps(source, ensure_ascii=False, sort_keys=True),
                )
            elif index not in node.referenced_projections:
                because = (
                    "but no FCL ref cites it"
                    if node.document is not None
                    else (
                        "but this node's commitment surface was not read by this import "
                        f"(commitment_surface_state = {node.commitment_surface_state!r}), so "
                        "no ref could cite it. Nothing is implied about whether the author "
                        "used the exposed material"
                    )
                )
                self.add_residue(
                    "projection_exposed_unreferenced",
                    node=node,
                    field_name="projection_artifacts",
                    ref=alias,
                    reason=(
                        f"projection slot {alias} (source {source.get('source')!r}) was "
                        f"exposed in the brief {because}"
                    ),
                    verbatim=json.dumps(
                        source.get("coordinate"), ensure_ascii=False, sort_keys=True
                    ),
                )

    def backfill_residue_carriers(self) -> None:
        """Fill in ``carrier.spec_artifact_id`` for entries raised before naming.

        Residue is emitted throughout the mapping, and a good deal of it is
        raised *before* the carrier's content-addressed spec id exists (the id
        depends on the interface, which depends on the refs, which is what the
        residue is about). Leaving those entries with a null id makes
        ``residue.json`` unjoinable against ``side_table.json`` for exactly the
        codes that matter most, so the ids are backfilled once every node has
        been named.
        """
        by_key = {coord.key: self.nodes[coord].spec_id for coord in self.order}
        for entry in self.residue:
            carrier = entry.get("carrier")
            if not carrier or carrier.get("spec_artifact_id"):
                continue
            coordinate = carrier.get("coordinate") or {}
            key = Coordinate.from_dict(coordinate).key if coordinate else None
            carrier["spec_artifact_id"] = by_key.get(key)

    def arm_surfaces(self) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """(prose arms in scope, FCL-1 arms in scope), both sorted."""
        arms = sorted({coord.arm for coord in self.order})
        prose = tuple(a for a in arms if a not in FCL_SURFACE_ARMS)
        formal = tuple(a for a in arms if a in FCL_SURFACE_ARMS)
        return prose, formal

    @staticmethod
    def arm_phrase(arms: Sequence[str]) -> str:
        """``2 arms (bare, native)`` / ``1 arm (mini_fcl)`` / ``no arms``."""
        if not arms:
            return "no arms"
        return f"{len(arms)} arm{'' if len(arms) == 1 else 's'} ({', '.join(arms)})"

    def multi_arm_framing(self) -> str | None:
        """The paragraph a multi-arm scope must carry, or None.

        The two parentheticals name the arms **actually in this scope**. They
        used to be hard-coded to the five arms of the whole occurrence, so a
        two-arm scope was told it contained `bare, native, matched, mini_prose`
        - a report that named arms it had not read. Everything the paragraph
        *claims* is still the fixed :data:`MULTI_ARM_FRAMING_TAIL`; only the
        inventory is per-run, so no run can soften the claim.
        """
        prose, formal = self.arm_surfaces()
        if len(prose) + len(formal) < 2:
            return None
        return (
            f"This scope contains {self.arm_phrase(prose)} whose declared commitment "
            f"surface is prose and {self.arm_phrase(formal)} whose surface is FCL-1. "
            + MULTI_ARM_FRAMING_TAIL
        )

    def surface_state_by_artifact(self) -> dict[str, str]:
        """Node spec id -> commitment_surface_state, for the why chains."""
        return {
            self.nodes[coord].spec_id: self.nodes[coord].commitment_surface_state
            for coord in self.order
            if self.nodes[coord].spec_id
        }

    def report_edge_dedupe(self) -> None:
        """Report every att edge that more than one warrant collapses onto."""
        by_edge: dict[tuple[str, str], list[_PlannedWarrant]] = {}
        for planned in self.planned_warrants:
            by_edge.setdefault((planned.carrier.spec_id, planned.target_id), []).append(planned)
        for edge, group in sorted(
            by_edge.items(), key=lambda item: sorted(p.warrant.id for p in item[1])
        ):
            if len(group) < 2:
                continue
            self.add_residue(
                "warrant_edge_deduplicated",
                node=group[0].carrier,
                reason=(
                    f"{len(group)} separable criticisms collapse onto one att edge "
                    f"({self.names.get(edge[0], edge[0])} -> {self.names.get(edge[1], edge[1])}); "
                    "att is a set of pairs, and each criticism stays independently attackable "
                    "through its own validity node"
                ),
                verbatim=", ".join(sorted(p.warrant.id for p in group)),
            )

    # -- the deterministic event plan --------------------------------------- #

    def plan_events(self, material: dict[str, Any]) -> None:
        prose = {p["id"]: p.get("prose", "") for p in material.get("problems", [])}
        seq = 0
        for problem_id in sorted({c.problem for c in self.order}):
            task = Problem(
                id=f"pi:h005.task:{problem_id}",
                description=prose.get(problem_id, ""),
                criteria=[],
                provenance=ProblemProvenance.model_validate(
                    {"trigger": SpawnTrigger.SEED.value, "from": []}
                ),
            )
            self.task_problems[problem_id] = task
            self.planned_events.append(
                {"seq": seq, "phase": "0", "rule": "Spawn", "ts": self.first_ts, "what": task.id}
            )
            seq += 1
        for coord in self.order:
            node = self.nodes[coord]
            if node.document_artifact_new:
                node.document_seq = seq
                self.planned_events.append(
                    {"seq": seq, "phase": "A0", "rule": "Register", "ts": node.ts,
                     "what": node.document_artifact_id}
                )
                seq += 1
            for commitment in sorted(node.commitments, key=lambda c: c.id):
                self.planned_events.append(
                    {"seq": seq, "phase": "A1", "rule": "Register", "ts": node.ts,
                     "what": commitment.id}
                )
                seq += 1
            node.register_seq = seq
            self.planned_events.append(
                {"seq": seq, "phase": "A2", "rule": "Register", "ts": node.ts,
                 "what": node.spec_id}
            )
            seq += 1
            for problem in node.problems:
                self.planned_events.append(
                    {"seq": seq, "phase": "A3", "rule": "Spawn", "ts": node.ts,
                     "what": problem.id}
                )
                seq += 1
            for research in node.research_problems:
                self.planned_events.append(
                    {"seq": seq, "phase": "A4", "rule": "Spawn", "ts": node.ts,
                     "what": research.id}
                )
                seq += 1
        for planned in self.planned_warrants:
            planned.nu_seq = seq
            self.planned_events.append(
                {"seq": seq, "phase": "B1", "rule": "Register", "ts": self.last_ts,
                 "what": planned.nu_id}
            )
            seq += 1
            planned.crit_seq = seq
            self.planned_events.append(
                {"seq": seq, "phase": "B2", "rule": "Crit", "ts": self.last_ts,
                 "what": planned.warrant.id}
            )
            seq += 1
        self.events_count = seq
        if len({p.nu_id for p in self.planned_warrants}) != len(self.planned_warrants):
            raise MappingError("VALIDITY_NODE_ID_COLLISION")
        identities = [n.spec_id for n in self.nodes.values()]
        if len(set(identities)) != len(identities):
            raise MappingError("ARTIFACT_ID_COLLISION")
        self.add_residue(
            "adjudication_batched",
            reason=(
                "the vendored P0 Harness re-adjudicates inside every registration event and "
                "exposes no public Adj emitter, so this import emits no separate terminal Adj "
                "event (mapping.md §8.2 asked for one). Status flips are recorded in each "
                "registration event's state_diff.status_changed; the import writes through "
                "the registration API only and never forges a log line."
            ),
            verbatim=f"{self.events_count} events, seq 0..{self.events_count - 1}",
        )

    # -- registration through the harness's public API ----------------------- #

    def register(self, harness: Harness, clock: _Clock) -> None:
        def expect(seq: int) -> None:
            if harness._next_seq != seq:
                raise MappingError(
                    f"EVENT_SEQUENCE_DRIFT: expected {seq}, harness is at {harness._next_seq}"
                )

        for problem_id in sorted(self.task_problems):
            clock.ts = self.first_ts
            harness.register_problem(self.task_problems[problem_id])
        for coord in self.order:
            node = self.nodes[coord]
            clock.ts = node.ts
            if node.document_artifact_new:
                expect(node.document_seq)
                document = harness.create_artifact(
                    node.record["commitments"].encode("utf-8"),
                    codec="json",
                    interface=Interface(),
                    provenance=Provenance(
                        role=ProvenanceRole.IMPORT, school=None, event_seq=node.document_seq
                    ),
                    problem_id=self.task_problems[coord.problem].id,
                    rule=Rule.REGISTER,
                )
                if document.id != node.document_artifact_id:
                    raise MappingError(f"DOCUMENT_ARTIFACT_ID_DRIFT:{coord.key}")
            elif node.document is not None:
                # A second node authored byte-identical commitments; the
                # content-addressed document artifact already exists.
                harness.blobs.put(node.record["commitments"].encode("utf-8"))
            else:
                # Opaque or prose surface: the string is still preserved as a
                # blob so nothing authored is lost.
                harness.blobs.put(node.record.get("commitments", "").encode("utf-8"))
            for commitment in sorted(node.commitments, key=lambda c: c.id):
                harness.register_commitment(commitment)
            expect(node.register_seq)
            artifact = harness.create_artifact(
                node.record["body"].encode("utf-8"),
                codec="utf8",
                interface=node.interface,
                provenance=Provenance(
                    role=ProvenanceRole.IMPORT, school=None, event_seq=node.register_seq
                ),
                problem_id=self.task_problems[coord.problem].id,
                rule=Rule.REGISTER,
            )
            if artifact.id != node.spec_id or artifact.content_ref != node.record["body_sha256"]:
                raise MappingError(f"ARTIFACT_ID_DRIFT:{coord.key}")
            for problem in node.problems:
                harness.register_problem(problem)
            for research in node.research_problems:
                harness.register_problem(research)
        clock.ts = self.last_ts
        for planned in self.planned_warrants:
            expect(planned.nu_seq)
            nu = harness.create_artifact(
                planned.nu_content.encode("utf-8"),
                codec="utf8",
                interface=planned.nu_interface,
                # IMPORT, not CRITIC, for EVERY artifact this import mints -
                # node, FCL-1 document and validity node alike. CRITIC would
                # say this process produced a criticism of its own; it did not.
                # It transcribed one the authors wrote.
                provenance=Provenance(
                    role=ProvenanceRole.IMPORT, school=None, event_seq=planned.nu_seq
                ),
                rule=Rule.REGISTER,
            )
            if nu.id != planned.nu_id:
                raise MappingError(f"VALIDITY_NODE_ID_DRIFT:{planned.warrant.id}")
            expect(planned.crit_seq)
            # Carriage is declared through register_batch and lives ONLY in the
            # harness's carry relation: the stored artifact record keeps an
            # empty ``warrants`` list, and state.carries is authoritative.
            carrier = harness.state.artifacts[planned.carrier.spec_id]
            harness.register_batch(
                [(carrier.model_copy(update={"warrants": [planned.warrant.id]}),
                  [planned.warrant])],
                rule=Rule.CRIT,
            )

    # -- labels ------------------------------------------------------------- #

    def adjudicate_offline(
        self,
    ) -> tuple[dict[str, str], list[tuple[str, str]], list[tuple[str, str]]]:
        """Adjudicate in memory with the vendored functions (used by --dry-run)."""
        artifacts: dict[str, Artifact] = {}
        warrants: dict[str, Warrant] = {}
        carries: list[tuple[str, str]] = []
        for coord in self.order:
            node = self.nodes[coord]
            if node.document_artifact_id:
                artifacts[node.document_artifact_id] = Artifact(
                    id=node.document_artifact_id,
                    content_ref=node.record["commitments_sha256"],
                    codec="json",
                    interface=Interface(),
                    warrants=[],
                    provenance=Provenance(
                        role=ProvenanceRole.IMPORT, event_seq=node.document_seq
                    ),
                )
            artifacts[node.spec_id] = Artifact(
                id=node.spec_id,
                content_ref=node.record["body_sha256"],
                codec="utf8",
                interface=node.interface,
                warrants=[],
                provenance=Provenance(role=ProvenanceRole.IMPORT, event_seq=node.register_seq),
            )
        for planned in self.planned_warrants:
            artifacts[planned.nu_id] = Artifact(
                id=planned.nu_id,
                content_ref=sha256_bytes(planned.nu_content.encode("utf-8")),
                codec="utf8",
                interface=planned.nu_interface,
                warrants=[],
                provenance=Provenance(role=ProvenanceRole.IMPORT, event_seq=planned.nu_seq),
            )
            warrants[planned.warrant.id] = planned.warrant
            carries.append((planned.carrier.spec_id, planned.warrant.id))
        att = build_att(artifacts, warrants, {}, carries)
        dep = build_dep(artifacts)
        final = final_labels(compute_label0(set(artifacts), att), dep)
        return {aid: final[aid].value for aid in artifacts}, sorted(att), sorted(dep)

    # -- why (spec §13) ------------------------------------------------------ #

    def display(self, artifact_id: str) -> str:
        return f"{self.names.get(artifact_id, '?')} [{artifact_id[:12]}]"

    def build_why(
        self,
        labels: dict[str, str],
        att: Sequence[tuple[str, str]],
        dep: Sequence[tuple[str, str]],
    ) -> dict[str, str]:
        attackers = attack_index(att)
        carried: dict[tuple[str, str], list[str]] = {}
        for planned in self.planned_warrants:
            carried.setdefault((planned.carrier.spec_id, planned.target_id), []).append(
                planned.warrant.id
            )
        nu_of: dict[str, str] = {p.nu_id: p.warrant.id for p in self.planned_warrants}
        supports: dict[str, list[str]] = {aid: [] for aid in labels}
        for dependent, dependency in dep:
            supports.setdefault(dependent, []).append(dependency)
        surface_state = self.surface_state_by_artifact()
        surface_note = {
            "unavailable_decode_failure": (
                "  commitment surface: UNAVAILABLE (unavailable_decode_failure). The "
                "authored commitments string is empty in the record because the study "
                "harness's strict JSON decode failed; root's review `"
                + ENVELOPE_REVIEW_PATH
                + "` measured that the returned bytes do contain commitments. This import "
                "read no commitment surface for this artifact, so it could mint no warrant "
                "from it and no warrant against it. The label above is silent about what "
                "the author committed to."
            ),
            "prose_not_parsed": (
                "  commitment surface: NOT READ (prose_not_parsed). This arm's declared "
                "commitment surface is prose; the author was never asked for FCL-1 and the "
                "string is never parsed as one. No warrant, no attack edge and no refuted "
                "label can arise from it under this import, so the label above is a "
                "property of the carrier, not of the contribution."
            ),
            "parse_failure": (
                "  commitment surface: UNAVAILABLE (parse_failure). The arm declares an "
                "FCL-1 surface and the string did not parse as JSON; nothing was repaired "
                "(I4), so no commitment surface was read and the label above is silent "
                "about what the author committed to."
            ),
            "schema_failure": (
                "  commitment surface: UNAVAILABLE (schema_failure). The arm declares an "
                "FCL-1 surface and the document did not validate against fcl1.schema.json; "
                "nothing was repaired (I4), so no commitment surface was read and the label "
                "above is silent about what the author committed to."
            ),
        }

        def chain(aid: str, depth: int, seen: tuple[str, ...]) -> list[str]:
            pad = "  " * (depth + 1)
            mine = attackers.get(aid, [])
            if not mine:
                return [f"{pad}(no attacker in the imported relation)"]
            lines: list[str] = []
            for attacker in mine:
                lines.append(
                    f"{pad}<- attacked by {self.display(attacker)} -- "
                    f"{labels.get(attacker, '?')}"
                )
                for wid in sorted(carried.get((attacker, aid), [])):
                    lines.append(f"{pad}     via warrant {wid}")
                if aid in nu_of:
                    lines.append(
                        f"{pad}     (closure: attacking this validity node disables "
                        f"{nu_of[aid]} and every carrier of it)"
                    )
                if attacker in seen:
                    lines.append(f"{pad}     (cycle: already shown above)")
                    continue
                lines.extend(chain(attacker, depth + 1, seen + (aid,)))
            return lines

        chains: dict[str, str] = {}
        for aid, label in sorted(labels.items()):
            mine = attackers.get(aid, [])
            out = [
                f"why({aid})",
                f"  artifact : {self.names.get(aid, '?')}",
                f"  status   : {label}",
                "",
                f"  {self.display(aid)} -- {label}",
            ]
            out.extend(chain(aid, 0, (aid,)))
            out.append("")
            if label == "accepted" and not mine:
                out.append(
                    "  accepted: unattacked in the imported attack relation, so it enters the "
                    "grounded extension at the first Kleene step. This is "
                    + ACCEPT_BY_POSITION
                )
            elif label == "accepted":
                out.append(
                    "  accepted by reinstatement (spec §4 pass 1, Lemma 3.1): every attacker "
                    "is itself attacked from the grounded extension."
                )
                for defender in sorted(
                    {
                        d
                        for attacker in mine
                        for d in attackers.get(attacker, [])
                        if labels.get(d) == "accepted"
                    }
                ):
                    out.append(f"    reinstating attacker: {self.display(defender)}")
            elif label == "refuted":
                out.append(
                    "  refuted: attacked from the grounded extension by "
                    + ", ".join(self.display(a) for a in mine if labels.get(a) == "accepted")
                    + ", and nothing in the imported relation attacks that attacker."
                )
            elif label == "suspended":
                out.append(
                    "  suspended: neither in the grounded extension nor attacked from it -- "
                    "the import has not adjudicated it."
                )
            else:
                out.append(
                    "  suspended_unsupported: accepted in the attack semantics, but a declared "
                    "dependence is not accepted (spec §4 pass 2). Orphaned != false."
                )
            if supports.get(aid):
                out.append("  declared dependence (dep):")
                for dependency in sorted(supports[aid]):
                    out.append(
                        f"    -> {self.display(dependency)} -- {labels.get(dependency, '?')}"
                    )
            else:
                out.append(
                    "  declared dependence (dep): none, so pass 2 is a no-op for this artifact."
                )
            note = surface_note.get(surface_state.get(aid, "read_fcl1"))
            if note:
                out.append(note)
            out.append("  I7: " + I7_BANNER.replace("**", ""))
            chains[aid] = "\n".join(out)
        return chains


# --------------------------------------------------------------------------- #
# outputs                                                                      #
# --------------------------------------------------------------------------- #


def _side_table(
    importer: _Importer, labels: dict[str, str], custody: dict[str, Any]
) -> dict[str, Any]:
    artifacts = []
    for coord in importer.order:
        node = importer.nodes[coord]
        receipt = node.receipt or {}
        artifacts.append(
            {
                "coordinate": coord.as_dict(),
                "source_path": occurrence_path(coord, "artifacts"),
                "h005_artifact_id": node.record.get("artifact_id"),
                "h005_body_sha256": node.record.get("body_sha256"),
                "h005_commitments_sha256": node.record.get("commitments_sha256"),
                "h005_public_text_sha256": node.record.get("public_text_sha256"),
                "delivery_status": node.record.get("delivery_status"),
                "envelope_status": node.record.get("envelope_status"),
                "commitment_surface": node.surface,
                # What this import actually did with the commitments string,
                # and why. "unavailable_decode_failure" is NOT "the author
                # wrote no commitments" - see the residue entry and
                # docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md.
                "commitment_surface_state": node.commitment_surface_state,
                "exposed_labels": sorted(node.label_index),
                "task_labels": list(node.task_labels),
                "spec_artifact_id": node.spec_id,
                "spec_content_ref": node.record.get("body_sha256"),
                "spec_codec": "utf8",
                "document_spec_artifact_id": node.document_artifact_id or None,
                "register_event_seq": node.register_seq,
                "status": labels.get(node.spec_id),
                "commitments": sorted(c.id for c in node.commitments),
                "problems": [p.id for p in node.problems]
                + [p.id for p in node.research_problems],
                "warrants_carried": [
                    p.warrant.id for p in importer.planned_warrants if p.carrier is node
                ],
                "absent_inputs": node.absent_inputs,
                "provider_receipt": (
                    {
                        "response_path": occurrence_path(coord, "responses"),
                        "finished_utc": receipt.get("finished_utc"),
                        "returned_model": receipt.get("returned_model"),
                        "finish_reason": receipt.get("finish_reason"),
                        "provider_request_sha256": receipt.get("provider_request_sha256"),
                        "provider_response_sha256": receipt.get("provider_response_sha256"),
                        "wave_id": node.wave_id,
                    }
                    if node.receipt is not None
                    else None
                ),
            }
        )
    label_rows = []
    for coord in importer.order:
        node = importer.nodes[coord]
        for label, index in sorted(node.label_index.items()):
            source = node.projections[index].get("selected_source") or {}
            owner = None
            if not source.get("absent"):
                owner_node = importer.nodes.get(Coordinate.from_dict(source.get("coordinate")))
                owner = owner_node.spec_id if owner_node else None
            label_rows.append(
                {
                    "carrier_coordinate": coord.as_dict(),
                    "label": label,
                    "projection_index": index,
                    "projection_artifact_id": node.projections[index].get("artifact_id"),
                    "selected_source_artifact_id": source.get("artifact_id"),
                    "selected_source_coordinate": source.get("coordinate"),
                    "view": source.get("view"),
                    "absent": bool(source.get("absent")),
                    "resolves_to_spec_artifact_id": owner,
                }
            )
    return {
        "schema": SIDE_TABLE_SCHEMA,
        "occurrence": importer.occurrence.name,
        "occurrence_plan_id": custody["plan_id"],
        "importer_version": IMPORTER_VERSION,
        "scope": [c.as_dict() for c in importer.order],
        "artifacts": artifacts,
        "documents": [
            {"spec_artifact_id": document_id, "first_carrier": carrier, "codec": "json",
             "status": labels.get(document_id)}
            for document_id, carrier in sorted(importer.document_artifacts.items())
        ],
        "validity_nodes": [
            {
                "warrant_id": p.warrant.id,
                "spec_artifact_id": p.nu_id,
                "name": importer.names.get(p.nu_id),
                "content_sha256": sha256_bytes(p.nu_content.encode("utf-8")),
                "carrier_spec_artifact_id": p.carrier.spec_id,
                "target_spec_artifact_id": p.target_id,
                "target_kind": p.target_kind,
                "register_event_seq": p.nu_seq,
                "status": labels.get(p.nu_id),
            }
            for p in importer.planned_warrants
        ],
        "labels": label_rows,
        "records": importer.records_table,
    }


def _residue_document(importer: _Importer, totals: dict[str, int]) -> dict[str, Any]:
    return {
        "schema": RESIDUE_SCHEMA,
        "occurrence": importer.occurrence.name,
        "importer_version": IMPORTER_VERSION,
        "scope": [c.as_dict() for c in importer.order],
        "units": {code: meta["unit"] for code, meta in RESIDUE_CODES.items()},
        "totals": totals,
        "entries": importer.residue,
    }


def _report_markdown(importer: _Importer, report: ImportReport) -> str:
    lines: list[str] = [
        "# H005 -> spec-v1.3 import report",
        "",
        "> " + I7_BANNER,
        "",
    ]
    errors = report.error_severity_totals
    if errors:
        lines += [
            "> **Error-severity residue fired in this import:** "
            + ", ".join(f"`{code}` ({count})" for code, count in errors.items())
            + ". An `error` severity means a construct the mapping could not carry at all - "
            "a reference that resolved to nothing, a projection that exposed nothing, or a "
            "commitments string that claimed FCL-1 and did not parse. Read the Residue "
            "section and `residue.json` before reading any label below.",
            "",
        ]
    lines += [
        f"- occurrence: `{report.occurrence}`",
        f"- plan_id: `{report.custody['plan_id']}`",
        f"- importer: `{IMPORTER_VERSION}`",
        "- scope: " + ", ".join(
            f"`{c['problem']}/{c['arm']}/cycle{c['cycle']:02d}/{c['node']}`"
            for c in report.scope
        ),
        f"- events: {report.events_count} (`seq` 0..{report.events_count - 1}), "
        "every `Event.llm` is null and every `ts` comes from the occurrence's `finished_utc`",
        f"- references: {report.resolution['resolved']}/{report.resolution['refs']} resolved, "
        f"{report.resolution['extensions']} admitted by extension, "
        f"{report.resolution['dangling']} dangling",
        "",
        "## What this is, and what it is not",
        "",
        "The statuses below are **computed standing inside the imported attack relation**: "
        "the grounded extension of the attacks the authors themselves declared, then the "
        "support cascade over declared dependence. They are not a semantic verdict on any "
        "contribution, not a rubric judgement, and not an interpretation of the root problem. "
        "No provider was called, no `demonstrative` warrant was minted, and no transport "
        "status (`delivery_status`, `envelope_status`, `finish_reason`, `status`) was ever "
        "read as a verdict. An unattacked artifact is `accepted` **by position** - "
        + ACCEPT_BY_POSITION,
        "",
    ]
    if report.multi_arm_framing:
        lines += [report.multi_arm_framing, ""]
    if report.residue_totals.get("opaque_envelope"):
        lines += [
            "**On the "
            + str(report.residue_totals["opaque_envelope"])
            + " artifact(s) with an empty commitments string.** "
            + OPAQUE_ENVELOPE_REASON,
            "",
        ]
    lines += [
        "## Custody",
        "",
        "Every row says how many subjects the check actually ran over. A check that could "
        "not run over a coordinate - no receipt, no attempt, no request record, no provider "
        "call - is not a failure and not a verification; the coordinate is admitted with its "
        "absent inputs recorded in `side_table.json.artifacts[].absent_inputs`.",
        "",
        "### Cross-file custody",
        "",
        "Each of these compares two independently written files, so a coherent rewrite of "
        "any one of them is detected.",
        "",
        "| check | result |",
        "|---|---|",
    ]
    for check in report.custody["cross_file"]:
        lines.append(f"| {check['check']} | {check['result']} |")
    monotone = report.custody.get("event_ts_nondecreasing")
    if monotone is None:
        ts_result = "not evaluated (dry run: no log was written)"
    elif monotone:
        ts_result = "yes"
    else:
        ts_result = (
            "no - and that is a **declared deviation**, not a fault: a wave runs several "
            "arms concurrently and their `finished_utc` values interleave. Spec §14 requires "
            "contiguous `seq`, not ordered `ts`. Clamping would report a time that was never "
            "observed, so the import reports the fact instead."
        )
    lines.append(f"| event ts nondecreasing | {ts_result} |")
    lines.append(f"| files read and hashed | {len(report.custody['files'])} |")
    lines += [
        "",
        "### Internal consistency only",
        "",
        "These compare a file against **itself**. They catch a truncated or incoherently "
        "edited file; they cannot detect a coherent rewrite, because nothing independent "
        "pins the value they check against.",
        "",
        "| check | result |",
        "|---|---|",
    ]
    for check in report.custody["self_consistency"]:
        lines.append(f"| {check['check']} | {check['result']} |")
    lines += [
        "",
        "## Labels",
        "",
    ]
    if report.multi_arm_framing:
        lines += [report.multi_arm_framing, ""]
    lines += [
        "The **surface** column is the commitment surface this import actually read for "
        "that artifact: `read` (an FCL-1 document was parsed), `NOT READ (prose)` (the arm "
        "declared a prose surface, never parsed), `UNAVAILABLE (decode)` (the commitments "
        "string is empty because the study harness's strict decode failed), `PARSE FAILURE` "
        "/ `SCHEMA FAILURE` (an FCL-surface arm's document did not parse or did not "
        "validate), or `n/a` for an artifact that has no commitment surface - a validity "
        "node or an FCL-1 document. A status computed over a surface that was not read "
        "carries no information about the contribution; read the two columns together.",
        "",
        "| artifact | id | status | surface | attacked by | carries |",
        "|---|---|---|---|---|---|",
    ]
    attackers = attack_index(report.att_edges)
    carriers: dict[str, list[str]] = {}
    for planned in importer.planned_warrants:
        carriers.setdefault(planned.carrier.spec_id, []).append(planned.warrant.id)
    for aid in label_order(report.labels, importer.names):
        attacked_by = (
            ", ".join(importer.names.get(a, a[:12]) for a in attackers.get(aid, [])) or "-"
        )
        carried = f"{len(carriers[aid])} warrant(s)" if aid in carriers else "-"
        lines.append(
            f"| `{importer.names.get(aid, '?')}` | `{aid[:16]}` | **{report.labels[aid]}** "
            f"| {report.surface_of(aid)} | {attacked_by} | {carried} |"
        )
    lines += [
        "",
        f"`|att|` = {len(report.att_edges)}, `|dep|` = {len(report.dep_edges)}, "
        f"warrants = {len(report.warrants)}, artifacts = {len(report.labels)}.",
        "",
        "### Attack edges",
        "",
    ]
    for source, target in report.att_edges:
        lines.append(
            f"- `{importer.names.get(source, source)}` -> `{importer.names.get(target, target)}`"
        )
    if not report.att_edges:
        lines.append("- (none)")
    lines += ["", "### Support edges (`dep`)", ""]
    if report.dep_edges:
        for source, target in report.dep_edges:
            lines.append(
                f"- `{importer.names.get(source, source)}` -> "
                f"`{importer.names.get(target, target)}`"
            )
    else:
        intra = report.residue_totals.get("depends_intra_document", 0)
        rejected = report.residue_totals.get("dependence_cycle_rejected", 0)
        if not intra and not rejected:
            lines.append(
                "- **none, and no `depends` ref was authored anywhere in this scope.** `dep` "
                "is empty because the authors declared no dependence at all, not because "
                "the mapping dropped anything. Pass 2 is the identity here."
            )
        elif intra and not rejected:
            lines.append(
                f"- **none.** All {intra} `depends` refs in this scope were document-local, "
                "so at node granularity each would have been a `dep` self-loop - a cycle, "
                "which spec §1 forbids - and each was dropped and reported under "
                "`depends_intra_document`. That is a property of the node-granularity "
                "mapping, not a result about the occurrence. Pass 2 is a no-op and "
                "`suspended_unsupported` is unreachable in this scope."
            )
        else:
            lines.append(
                f"- **none.** {intra} `depends` ref(s) in this scope were document-local and "
                f"{rejected} would have closed a `dep` cycle; both classes were dropped and "
                "reported (`depends_intra_document`, `dependence_cycle_rejected`). Pass 2 is "
                "a no-op and `suspended_unsupported` is unreachable in this scope."
            )
    lines += [
        "",
        "## Warrants",
        "",
        "| warrant | carrier | target | target kind | validity node |",
        "|---|---|---|---|---|",
    ]
    for entry in report.warrants:
        lines.append(
            f"| `{entry['id']}` | `{entry['carrier_name']}` | `{entry['target_name']}` | "
            f"{entry['target_kind']} | `{entry['validity_node'][:16]}` |"
        )
    if not report.warrants:
        lines.append("| (none) | | | | |")
    lines += [
        "",
        "Every warrant is `argumentative` with `commitment = null`, `verdict = null` and "
        "`trace_ref = null`: no kappa was run and a bare verdict is never an edge. A warrant "
        "whose target kind is `validity_node` is criticism of a criticism: spec §1 closure "
        "lifts it onto the attacked warrant and every carrier of it.",
        "",
        "## Commitments and spawned problems",
        "",
        "| commitment | observation-valued | eval | research problem |",
        "|---|---|---|---|",
    ]
    for entry in report.commitments:
        lines.append(
            f"| `{entry['id']}` | {str(entry['observation_valued']).lower()} | "
            f"`{entry['eval'][:44]}...` | `{entry['research_problem']}` |"
        )
    if not report.commitments:
        lines.append("| (none) | | | |")
    lines += [
        "",
        "An observation-valued commitment with no covering evidence is **scheduled-pending, "
        "never failed** (spec §12): it spawns a research problem instead of a verdict. The "
        "`eval` string is outside every executable class, so nothing can dispatch it.",
        "",
        "## Residue",
        "",
        "| code | severity | unit | count |",
        "|---|---|---|---|",
    ]
    for code, count in sorted(report.residue_totals.items()):
        lines.append(
            f"| `{code}` | {RESIDUE_CODES[code]['severity']} | {RESIDUE_CODES[code]['unit']} "
            f"| {count} |"
        )
    lines += [
        "",
        "Counts follow the unit column: `ref` counts references, `record` counts FCL records, "
        "`document` counts FCL-1 documents or trace documents, `edge` counts attack or "
        "dependence edges, `artifact` counts artifacts, `problem` counts problems, `file` "
        "counts occurrence files. Full entries, each with the verbatim source text that was "
        "not mapped, are in `residue.json`.",
        "",
        "**What this table does and does not claim.** Every FCL record in scope is accounted "
        "for at record granularity: each record is either mapped to a spec construct or "
        "reported under a residue code, and `side_table.json.records[]` shows which, per "
        "record, with the codes it raised. The same holds for every reference this import "
        "resolved. It is **not** a claim that every nuance inside a mapped record survived "
        "the mapping: a record that became a `Commitment` kept its text and lost its prose "
        "structure, and the codes above are the granularities the closed vocabulary names "
        "(`ref`, `record`, `document`, `edge`, `artifact`, `problem`, `file`), not a proof "
        "of semantic completeness.",
        "",
        "## Declared deviations",
        "",
    ]
    for deviation in report.deviations:
        count = report.residue_totals.get(deviation["code"])
        if count:
            suffix = f" ({count} in this scope)"
        elif count == 0:
            suffix = " **(not triggered in this scope)**"
        else:
            suffix = ""
        lines.append(
            f"- **`{deviation['code']}`**{suffix} - {deviation['what']}. {deviation['why']}."
        )
    lines += [
        "",
        "## How to read this report",
        "",
        "1. **Labels** is the standing of each artifact inside the imported relation; read it "
        "together with the attack edges, never alone, and never as merit.",
        "2. **`side_table.json`** maps every H005 coordinate to its spec id and back, names "
        "every validity node and FCL-1 document artifact, and records which FCL record "
        "produced which object. Nothing in it may be read by adjudication.",
        "3. **`residue.json`** is the honest cost of the mapping: what the spec ontology could "
        "not carry, with verbatim source text and a counting unit per code.",
        "4. **Why** below is the attack/defence chain behind each label.",
        "",
        "## Why",
        "",
    ]
    for aid in label_order(report.labels, importer.names):
        lines += ["```", report.why_chains[aid], "```", ""]
    return "\n".join(lines)


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _write_new(path: Path, raw: bytes) -> None:
    with path.open("xb") as handle:
        handle.write(raw)


def _verify_event_log(harness: Harness, importer: _Importer) -> bool:
    """Check the written log against the plan; return whether ``ts`` is monotone.

    ``seq`` contiguity is the spec §14 requirement and the ``EventLog`` enforces
    it on every append. A nondecreasing ``ts`` is *not* required: a wave runs
    several arms concurrently, so their ``finished_utc`` values interleave. The
    importer reports the fact rather than clamping a timestamp it did not
    observe.
    """
    events = list(harness.log.read())
    if len(events) != importer.events_count:
        raise MappingError(
            f"EVENT_COUNT_MISMATCH: logged {len(events)}, planned {importer.events_count}"
        )
    planned = {entry["seq"]: entry for entry in importer.planned_events}
    monotone = True
    previous = ""
    for event in events:
        if event.llm is not None:
            raise MappingError("EVENT_LLM_NOT_NONE")
        if event.ts != planned[event.seq]["ts"]:
            raise MappingError(f"EVENT_TS_NOT_PINNED:{event.seq}")
        monotone = monotone and event.ts >= previous
        previous = event.ts
    for planned_warrant in importer.planned_warrants:
        if planned_warrant.warrant.id not in harness.carried_warrant_ids(
            planned_warrant.carrier.spec_id
        ):
            raise MappingError(f"CARRIAGE_NOT_RECORDED:{planned_warrant.warrant.id}")
        stored = harness.state.artifacts[planned_warrant.carrier.spec_id]
        if stored.warrants:
            raise MappingError(f"CARRIAGE_WRITTEN_ONTO_ARTIFACT:{stored.id}")
    return monotone


# --------------------------------------------------------------------------- #
# public entry point                                                           #
# --------------------------------------------------------------------------- #


def import_occurrence(
    occurrence_dir: Path,
    out_root: Path,
    *,
    problems: list[str] | None = None,
    arms: list[str] | None = None,
    cycles: list[int] | None = None,
    dry_run: bool = False,
) -> ImportReport:
    """Import one H005 occurrence into a new ``deepreason_core`` graph root.

    ``out_root`` is write-once - it must not already exist, which is checked
    **before any work is done** - and may never lie inside ``occurrence_dir``;
    the occurrence itself is only ever read. With ``dry_run=True`` nothing is
    written anywhere and the labels are computed by the same pure adjudication
    functions the harness uses.

    **Nothing is written at ``out_root`` until everything is written.** The
    graph root and the four report files are built in a uniquely named
    temporary sibling directory and renamed into place only after the last
    file is written and :func:`_verify_event_log` has passed; on any failure
    the temporary directory is removed. A `MappingError` raised late - after
    the log is written but before the report is - therefore leaves exactly
    what a custody refusal leaves: nothing. Without that, "nothing was
    written" held for exit 2 and not for exit 3, and an operator could be
    handed a graph root with a log and no report.
    """
    occurrence = Path(occurrence_dir).resolve()
    if not occurrence.is_dir():
        raise CustodyError(f"OCCURRENCE_NOT_A_DIRECTORY:{occurrence}")
    target = Path(out_root).resolve()
    if target == occurrence or occurrence in target.parents:
        raise OutRootRefused("OUT_ROOT_INSIDE_OCCURRENCE")
    if not dry_run and target.exists():
        # Write-once, refused before a single occurrence byte is read: the
        # operator's fix is a different destination, and making them wait for
        # a full import to learn that is pointless.
        raise OutRootRefused(f"OUT_ROOT_EXISTS:{target}")

    importer = _Importer(occurrence, problems, arms, cycles)
    custody = verify_custody(importer.reader, importer.ledger)
    material = custody.pop("material")
    plan = custody.pop("plan")
    scope = importer.discover_scope(material, plan)
    importer.load_nodes(scope, plan)
    importer.parse_documents()
    importer.map_records()
    importer.plan_events(material)
    importer.report_edge_dedupe()
    importer.backfill_residue_carriers()

    labels, att, dep = importer.adjudicate_offline()
    monotone: bool | None = None
    staging: Path | None = None
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(
            tempfile.mkdtemp(prefix=f".{target.name}.importing-", dir=target.parent)
        )
    try:
        if staging is not None:
            clock = _Clock()
            try:
                harness = Harness(staging, clock=clock)
            except TypeError as exc:
                # The vendored core gained one optional `clock` parameter so
                # that Event.ts is a pure function of the occurrence bytes.
                # Without it the log forks on machine load and replay
                # determinism is gone; the importer refuses rather than
                # writing a root it cannot reproduce.
                raise MappingError(
                    "CORE_CLOCK_UNSUPPORTED: this deepreason_core.harness.Harness does not "
                    "accept the optional `clock` parameter, so Event.ts would come from the "
                    f"wall clock and two imports of the same bytes would differ ({exc})"
                ) from exc
            importer.register(harness, clock)
            live = {aid: status.value for aid, status in harness.state.status.items()}
            if live != labels:  # pragma: no cover - defensive
                raise MappingError("LABELS_DISAGREE_WITH_HARNESS")
            labels, att, dep = live, sorted(harness.state.att), sorted(harness.state.dep)
            monotone = _verify_event_log(harness, importer)

        report = _build_report(
            importer, occurrence, target, dry_run, custody, labels, att, dep, monotone
        )

        if staging is not None:
            _write_new(
                staging / "side_table.json", _json_bytes(_side_table(importer, labels, custody))
            )
            _write_new(
                staging / "residue.json",
                _json_bytes(_residue_document(importer, report.residue_totals)),
            )
            _write_new(staging / "report.json", report.to_json().encode("utf-8"))
            _write_new(
                staging / "REPORT.md",
                (_report_markdown(importer, report) + "\n").encode("utf-8"),
            )
            if target.exists():  # pragma: no cover - lost a race with another writer
                raise OutRootRefused(f"OUT_ROOT_EXISTS:{target}")
            staging.rename(target)
            staging = None
    except BaseException:
        if staging is not None:
            shutil.rmtree(staging, ignore_errors=True)
        raise
    return report


def _build_report(
    importer: _Importer,
    occurrence: Path,
    target: Path,
    dry_run: bool,
    custody: dict[str, Any],
    labels: dict[str, str],
    att: Sequence[tuple[str, str]],
    dep: Sequence[tuple[str, str]],
    monotone: bool | None,
) -> ImportReport:
    """Assemble the ImportReport once the graph is built (or computed dry)."""
    custody["event_ts_nondecreasing"] = monotone
    custody.update(importer.ledger.as_dict())
    custody["files"] = dict(sorted(importer.reader.files.items()))
    totals = {code: 0 for code in RESIDUE_CODES}
    for entry in importer.residue:
        totals[entry["code"]] += 1

    report = ImportReport(
        occurrence=occurrence.name,
        out_root=None if dry_run else str(target),
        dry_run=dry_run,
        scope=tuple(c.as_dict() for c in importer.order),
        spec_id_table={c.key: importer.nodes[c].spec_id for c in importer.order},
        names=dict(sorted(importer.names.items())),
        events_count=importer.events_count,
        labels=dict(sorted(labels.items())),
        att_edges=tuple(sorted(att)),
        dep_edges=tuple(sorted(dep)),
        warrants=tuple(
            {
                "id": p.warrant.id,
                "carrier": p.carrier.spec_id,
                "carrier_name": p.carrier.coord.key,
                "target": p.target_id,
                "target_name": p.target_key,
                "target_kind": p.target_kind,
                "type": p.warrant.type.value,
                "record_id": p.record_id,
                "validity_node": p.nu_id,
                "commitment": p.warrant.commitment,
                "verdict": p.warrant.verdict,
            }
            for p in importer.planned_warrants
        ),
        commitments=tuple(
            {
                "id": commitment.id,
                "carrier": importer.nodes[coord].spec_id,
                "eval": commitment.eval,
                "observation_valued": commitment.observation_valued,
                "research_problem": f"pi:h005.fcl1.research:{commitment.id}",
            }
            for coord in importer.order
            for commitment in sorted(importer.nodes[coord].commitments, key=lambda c: c.id)
        ),
        problems=tuple(
            {"id": p.id, "trigger": p.provenance.trigger.value, "description": p.description}
            for p in (
                [importer.task_problems[k] for k in sorted(importer.task_problems)]
                + [p for c in importer.order for p in importer.nodes[c].problems]
                + [p for c in importer.order for p in importer.nodes[c].research_problems]
            )
        ),
        residue=tuple(
            {
                "code": entry["code"],
                "unit": entry["unit"],
                "coordinate": (entry["carrier"] or {}).get("coordinate"),
                "spec_artifact_id": (entry["carrier"] or {}).get("spec_artifact_id"),
                "record_id": entry["record_id"],
                "detail": entry["reason"],
            }
            for entry in importer.residue
        ),
        residue_totals=totals,
        resolution=dict(importer.resolution),
        custody=custody,
        why_chains=importer.build_why(labels, att, dep),
        multi_arm_framing=importer.multi_arm_framing(),
        commitment_surface_states=dict(sorted(importer.surface_state_by_artifact().items())),
    )
    return report
