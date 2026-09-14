"""B001 arm inventory: what arms are already published, and which of them the
published reading instrument can read.

What this is
------------
An offline, provider-free, read-only **inventory**. It walks published
occurrence directories of the H005-family studies, reads each occurrence's
``arms.json`` and ``plan.json`` as data, lists every coordinate that carries a
terminal artifact, and reports, per arm, whether
``minireason.use_relation_h005`` would read that arm's commitment surface at
all.

It exists because B001 was commissioned on a premise that the published bytes
refute -- "no published study yet has a bare-model arm" -- and because the one
mechanical fact that settles whether a *new* arm could be read by the permitted
instrument (``graph_import_h005.FCL_SURFACE_ARMS`` is an exact **arm-name**
membership test) is not visible in any register. Both questions are answerable
from committed bytes alone, and this file answers them the same way twice.

What this is NOT
----------------
It does not score, rank, classify, label, adjudicate or decide anything. It
mints no relation, builds no graph, reads no response content, and calls no
provider. It does not decide whether a proposed arm "is a replay": it reports,
field by field, which published arms a proposed declaration is identical to and
which fields differ, and leaves the decision to root.

Standing invariants, numbered to match ``use_relation_h005``'s U1-U7 where they
are the same invariant:

* **U1** offline, provider-free and read-only. Only files under a named study
  directory are read; every read is recorded with its sha256; nothing under any
  occurrence is ever written.
* **U2** no verdict is derived from a transport status. ``delivery_status`` and
  ``envelope_status`` are not read by this tool at all. An artifact's *presence*
  is reported; its content is not opened.
* **U3** nothing is inferred. Every field reported is a field some published
  document actually carries, or the presence of a published file.
* **U4** nothing is repaired. An occurrence missing ``plan.json`` or
  ``arms.json`` is listed as unreadable with the reason, never reconstructed.
* **U5** deterministic: no wall clock, no RNG, no environment, no dict-iteration
  order. Two builds over the same bytes are byte-identical.
* **U6** the tool classifies nothing. There is no score, rank, merit, status or
  label anywhere in its output, and a test asserts no such key exists.
* **U7** the reading is root's. Whether an already-published arm answers a
  question, and whether a proposed arm would be a replay, are root's calls.

Reuse
-----
The readability answer is **not reimplemented**. ``FCL_SURFACE_ARMS`` is
imported from ``minireason.graph_import_h005``, the very tuple the importer and
the use-relation instrument consult, so this tool cannot report an arm readable
that the instrument would decline, or the reverse.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

from minireason.graph_import_h005 import FCL_SURFACE_ARMS

__all__ = [
    "INSTRUMENT_VERSION",
    "INVENTORY_SCHEMA",
    "INVENTORY_BANNER",
    "FORBIDDEN_KEYS",
    "BUILD_FAILED_CODES",
    "InventoryError",
    "OutDirRefused",
    "SelectorMatchedNothing",
    "ArmRow",
    "CoordinateRow",
    "OccurrenceRow",
    "ProposalRow",
    "Inventory",
    "surface_read_by_instrument",
    "build_inventory",
    "compare_proposal",
    "write_inventory",
]

INSTRUMENT_VERSION = "b001_arm_inventory/1"
INVENTORY_SCHEMA = "b001.arm-inventory.v1"

#: Heads every INVENTORY.md. This tool's U6/U7 in one paragraph.
INVENTORY_BANNER = (
    "**This is an inventory of published bytes, not a reading of them.** It lists which "
    "arms exist, under which plan identity, at which ceiling and clock, which coordinates "
    "carry a terminal artifact, and whether the published use-relation instrument would "
    "read each arm's commitment surface at all. It scores nothing, ranks nothing, "
    "classifies nothing and compares no contribution with any other. `reads_commitment_"
    "surface` is a mechanical fact about "
    "`minireason.graph_import_h005.FCL_SURFACE_ARMS`, an exact arm-NAME membership test; "
    "it says nothing about whether an arm's contribution is good, complete or relevant. "
    "Whether an already-published arm answers a question, and whether a proposed arm "
    "would be a replay of one, are root's calls and are left to root."
)

#: No output key may carry any of these names (U6). Asserted by the suite.
FORBIDDEN_KEYS = frozenset({
    "score", "scores", "rank", "ranking", "ranked", "merit", "grade", "graded",
    "quality", "better", "worse", "best", "worst", "winner", "loser", "verdict",
    "average", "mean", "total_score", "weight", "weighted",
})

BUILD_FAILED_CODES = ("NO_STUDY_DIRECTORY", "MALFORMED_PROPOSAL")

#: The per-arm fields a proposal is compared on, in report order. Every one is
#: a field the published `arms.json` / `plan.json` actually carries.
COMPARED_FIELDS = ("endpoint", "kind", "surface", "max_tokens",
                   "timeout_seconds", "seed")

#: A proposal must declare exactly these keys. `cycle` is an int; the rest are
#: compared verbatim against published values.
PROPOSAL_REQUIRED = frozenset({"arm", "endpoint", "kind", "surface",
                               "max_tokens", "timeout_seconds", "seed",
                               "problem", "cycle"})


class InventoryError(Exception):
    """Well-formed request, inventory could not be built."""


class OutDirRefused(Exception):
    """The destination is inside a study, already exists, or cannot be written."""


class SelectorMatchedNothing(Exception):
    """`--study` named nothing this repository holds."""


# --------------------------------------------------------------------------
# Reading, with a sha256 per file (U1)
# --------------------------------------------------------------------------


class _Reader:
    """Path-confined reader. Refuses any path escaping the study roots."""

    def __init__(self, roots: Sequence[Path]) -> None:
        self._roots = tuple(Path(r).resolve() for r in roots)
        self._read: dict[str, str] = {}

    def _confine(self, path: Path) -> Path:
        resolved = Path(path).resolve()
        if not any(resolved == r or resolved.is_relative_to(r) for r in self._roots):
            raise InventoryError(f"PATH_OUTSIDE_STUDY: {path}")
        return resolved

    def key(self, path: Path) -> str:
        """The path as it is reported: relative to the shallowest root holding it."""
        resolved = self._confine(path)
        for root in self._roots:
            if resolved.is_relative_to(root):
                return (root.name + "/" + str(resolved.relative_to(root))).replace("\\", "/")
        raise InventoryError(f"PATH_OUTSIDE_STUDY: {path}")  # pragma: no cover

    def read_json(self, path: Path) -> Any:
        resolved = self._confine(path)
        raw = resolved.read_bytes()
        self._read[self.key(resolved)] = hashlib.sha256(raw).hexdigest()
        return json.loads(raw.decode("utf-8"))

    def note(self, path: Path) -> None:
        """Record a file's digest without parsing it (artifact presence, U2)."""
        resolved = self._confine(path)
        self._read.setdefault(
            self.key(resolved), hashlib.sha256(resolved.read_bytes()).hexdigest())

    @property
    def files_read(self) -> dict[str, str]:
        return dict(sorted(self._read.items()))


# --------------------------------------------------------------------------
# The one reused fact
# --------------------------------------------------------------------------


def surface_read_by_instrument(arm: str) -> tuple[bool, str]:
    """Would ``use_relation_h005`` parse this arm's commitment surface?

    The answer is the importer's own, not a second opinion:
    ``graph_import_h005._Node.surface`` returns ``"fcl1"`` iff
    ``coord.arm in FCL_SURFACE_ARMS`` and ``"prose"`` otherwise, and the
    use-relation instrument extracts references from FCL-1 documents only.
    The test is on the arm's **name**, not on its declared surface, its kind or
    the bytes it returned.
    """
    if arm in FCL_SURFACE_ARMS:
        return True, (
            "arm name is in graph_import_h005.FCL_SURFACE_ARMS %s, so the importer "
            "parses this arm's commitments as FCL-1 and the use-relation instrument "
            "extracts its authored references" % (list(FCL_SURFACE_ARMS),))
    return False, (
        "arm name is not in graph_import_h005.FCL_SURFACE_ARMS %s, so the importer "
        "reads this arm's commitments as prose and the use-relation instrument lists "
        "the node under 'Nodes whose commitment surface was not read'; no row is "
        "emitted for it. The test is on the arm NAME and cannot be satisfied by "
        "declaring surface 'fcl'" % (list(FCL_SURFACE_ARMS),))


# --------------------------------------------------------------------------
# Rows
# --------------------------------------------------------------------------


#: Two plan shapes are published in this repository and both are read as they
#: are, never normalised into each other.
#:
#: * ``arms_json`` -- the multi-family fork runner's. ``arms.json`` declares
#:   ``kind``, ``surface``, ``endpoint`` and the optional per-arm ceiling, clock
#:   and seed; ``plan["ceilings"]`` carries the effective values.
#: * ``plan_settings`` -- the owner's runner's. ``plan["arms"]`` is a LIST of
#:   names and ``plan["settings"]`` a per-arm transport view. **No arm kind and
#:   no commitment surface is recorded anywhere in such a plan**, so both are
#:   reported as ``null`` with ``kind_source`` saying why. They are not inferred
#:   from the arm's name (U3).
KIND_SOURCES = ("arms_json", "plan_settings")

NO_KIND_RECORDED = (
    "not recorded: this occurrence's plan was written by the owner's runner, "
    "whose `arms` is a list of names and whose `settings` is a transport view. "
    "Arm kind and commitment surface were module constants there, so no "
    "published byte of this occurrence carries them and this tool does not "
    "infer them from the arm's name (U3)."
)


@dataclass(frozen=True)
class ArmRow:
    arm: str
    kind: str | None
    surface: str | None
    kind_source: str
    kind_note: str | None
    endpoint: str | None
    max_tokens: int | None
    timeout_seconds_declared: int | None
    timeout_seconds_effective: int | None
    seed: int | None
    thinking: Any
    reads_commitment_surface: bool
    reads_commitment_surface_reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "arm": self.arm,
            "kind": self.kind,
            "surface": self.surface,
            "kind_source": self.kind_source,
            "kind_note": self.kind_note,
            "endpoint": self.endpoint,
            "max_tokens": self.max_tokens,
            "timeout_seconds_declared": self.timeout_seconds_declared,
            "timeout_seconds_effective": self.timeout_seconds_effective,
            "seed": self.seed,
            "thinking": self.thinking,
            "reads_commitment_surface": self.reads_commitment_surface,
            "reads_commitment_surface_reason": self.reads_commitment_surface_reason,
        }


@dataclass(frozen=True)
class CoordinateRow:
    problem: str
    arm: str
    cycle: int
    node: str
    artifact_present: bool

    def as_dict(self) -> dict[str, Any]:
        return {"problem": self.problem, "arm": self.arm, "cycle": self.cycle,
                "node": self.node, "artifact_present": self.artifact_present}


@dataclass(frozen=True)
class OccurrenceRow:
    study: str
    occurrence: str
    readable: bool
    unreadable_reason: str | None
    study_id: str | None
    plan_id: str | None
    runner_sha256: str | None
    helper_sha256: str | None
    provider_mode: str | None
    scope: dict[str, Any] | None
    max_calls: int | None
    arms: tuple[ArmRow, ...]
    coordinates: tuple[CoordinateRow, ...]
    provider_call_records: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "study": self.study,
            "occurrence": self.occurrence,
            "readable": self.readable,
            "unreadable_reason": self.unreadable_reason,
            "study_id": self.study_id,
            "plan_id": self.plan_id,
            "runner_sha256": self.runner_sha256,
            "helper_sha256": self.helper_sha256,
            "provider_mode": self.provider_mode,
            "scope": self.scope,
            "max_calls": self.max_calls,
            "arms": [a.as_dict() for a in self.arms],
            "coordinates": [c.as_dict() for c in self.coordinates],
            "provider_call_records": self.provider_call_records,
        }


@dataclass(frozen=True)
class ProposalRow:
    """One published arm placed beside a proposed declaration, field by field.

    No key here says "replay". ``fields_differing`` empty together with
    ``problem_and_cycle_match`` true is the mechanical fact; what follows from
    it is root's (U7).
    """

    study: str
    occurrence: str
    arm: str
    problem_and_cycle_match: bool
    terminal_artifacts_at_that_coordinate: int
    fields_identical: tuple[str, ...]
    fields_differing: tuple[str, ...]
    published_values: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "study": self.study,
            "occurrence": self.occurrence,
            "arm": self.arm,
            "problem_and_cycle_match": self.problem_and_cycle_match,
            "terminal_artifacts_at_that_coordinate":
                self.terminal_artifacts_at_that_coordinate,
            "fields_identical": list(self.fields_identical),
            "fields_differing": list(self.fields_differing),
            "published_values": self.published_values,
        }


@dataclass(frozen=True)
class Inventory:
    instrument_version: str
    schema: str
    banner: str
    fcl_surface_arms: tuple[str, ...]
    occurrences: tuple[OccurrenceRow, ...]
    proposal: dict[str, Any] | None
    proposal_rows: tuple[ProposalRow, ...]
    files_read: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "instrument_version": self.instrument_version,
            "schema": self.schema,
            "banner": self.banner,
            "fcl_surface_arms": list(self.fcl_surface_arms),
            "occurrences": [o.as_dict() for o in self.occurrences],
            "proposal": self.proposal,
            "proposal_rows": [p.as_dict() for p in self.proposal_rows],
            "files_read": dict(self.files_read),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True,
                          ensure_ascii=False) + "\n"

    def to_markdown(self) -> str:
        out: list[str] = ["# B001 arm inventory", "", self.banner, "",
                          "Instrument `%s`, schema `%s`." % (self.instrument_version,
                                                             self.schema), "",
                          "`graph_import_h005.FCL_SURFACE_ARMS` = `%s`."
                          % (list(self.fcl_surface_arms),), ""]
        for occ in self.occurrences:
            out.append("## `%s/%s`" % (occ.study, occ.occurrence))
            out.append("")
            if not occ.readable:
                out += ["Not inventoried: %s" % occ.unreadable_reason, ""]
                continue
            out.append("plan_id `%s`, runner `%s`, provider mode `%s`, "
                       "`max_calls` %s, scope `%s`, %d provider call records."
                       % (occ.plan_id, occ.runner_sha256, occ.provider_mode,
                          occ.max_calls, json.dumps(occ.scope, sort_keys=True),
                          occ.provider_call_records))
            out += ["", "| arm | kind | surface | kind source | endpoint | max_tokens"
                        " | clock (declared/effective) | seed | use-relation reads"
                        " it? |",
                    "|---|---|---|---|---|---:|---|---:|---|"]
            for arm in occ.arms:
                out.append("| `%s` | %s | %s | `%s` | `%s` | %s | %s / %s | %s | %s |"
                           % (arm.arm,
                              arm.kind if arm.kind is not None else "*not recorded*",
                              arm.surface if arm.surface is not None
                              else "*not recorded*",
                              arm.kind_source, arm.endpoint,
                              arm.max_tokens, arm.timeout_seconds_declared,
                              arm.timeout_seconds_effective, arm.seed,
                              "yes" if arm.reads_commitment_surface else "**no**"))
            out.append("")
            notes = sorted({a.kind_note for a in occ.arms if a.kind_note})
            for note in notes:
                out += ["> %s" % note, ""]
            present = [c for c in occ.coordinates if c.artifact_present]
            out.append("Terminal artifacts, %d of %d listed coordinates:"
                       % (len(present), len(occ.coordinates)))
            out.append("")
            for coord in occ.coordinates:
                out.append("- `%s/%s/cycle%02d/%s` - artifact %s"
                           % (coord.problem, coord.arm, coord.cycle, coord.node,
                              "present" if coord.artifact_present else "absent"))
            out.append("")
        if self.proposal is not None:
            out += ["## Proposed arm placed beside the published ones", "",
                    "Proposal, verbatim:", "", "```json",
                    json.dumps(self.proposal, indent=2, sort_keys=True), "```", "",
                    self._proposal_note(), ""]
            if not self.proposal_rows:
                out += ["No published arm of any inventoried occurrence shares this "
                        "proposal's `kind` and `endpoint`.", ""]
            else:
                out += ["| published arm | problem/cycle match | terminal artifacts |"
                        " identical on | differs on |", "|---|---|---:|---|---|"]
                for row in self.proposal_rows:
                    out.append("| `%s/%s/%s` | %s | %d | %s | %s |"
                               % (row.study, row.occurrence, row.arm,
                                  "yes" if row.problem_and_cycle_match else "no",
                                  row.terminal_artifacts_at_that_coordinate,
                                  ", ".join("`%s`" % f for f in row.fields_identical)
                                  or "-",
                                  ", ".join("`%s`" % f for f in row.fields_differing)
                                  or "**nothing**"))
                out.append("")
        out += ["## Files read", "", "| path | sha256 |", "|---|---|"]
        for path, sha in self.files_read.items():
            out.append("| `%s` | `%s` |" % (path, sha))
        out.append("")
        return "\n".join(out)

    @staticmethod
    def _proposal_note() -> str:
        return ("A row whose `differs on` column is empty and whose problem/cycle "
                "match is `yes` reports that every compared field of this proposal "
                "already stands published at that coordinate. **This tool does not "
                "call that a replay**; it reports the fields. What follows is root's "
                "(U7).")


# --------------------------------------------------------------------------
# Building
# --------------------------------------------------------------------------


def _occurrence_dirs(study: Path) -> list[Path]:
    return sorted((p for p in study.iterdir()
                   if p.is_dir() and p.name.startswith("occurrence")),
                  key=lambda p: p.name)


def _arm_rows_from_arms_json(arms: dict[str, Any],
                             ceilings: dict[str, Any]) -> tuple[ArmRow, ...]:
    rows = []
    for name in sorted(arms):
        spec = arms[name] if isinstance(arms[name], dict) else {}
        effective = ceilings.get(name) if isinstance(ceilings, dict) else None
        effective = effective if isinstance(effective, dict) else {}
        reads, reason = surface_read_by_instrument(name)
        rows.append(ArmRow(
            arm=name,
            kind=spec.get("kind"),
            surface=spec.get("surface"),
            kind_source="arms_json",
            kind_note=None,
            endpoint=spec.get("endpoint"),
            max_tokens=spec.get("max_tokens", effective.get("max_tokens")),
            timeout_seconds_declared=spec.get("timeout_seconds"),
            timeout_seconds_effective=effective.get("timeout_seconds"),
            seed=spec.get("seed", effective.get("seed")),
            thinking=None,
            reads_commitment_surface=reads,
            reads_commitment_surface_reason=reason))
    return tuple(rows)


def _arm_rows_from_plan_settings(names: Sequence[str],
                                 settings: dict[str, Any]) -> tuple[ArmRow, ...]:
    """The owner's runner's shape. Kind and surface stay null (U3)."""
    rows = []
    for name in sorted(str(n) for n in names):
        spec = settings.get(name) if isinstance(settings, dict) else None
        spec = spec if isinstance(spec, dict) else {}
        reads, reason = surface_read_by_instrument(name)
        rows.append(ArmRow(
            arm=name,
            kind=None,
            surface=None,
            kind_source="plan_settings",
            kind_note=NO_KIND_RECORDED,
            endpoint=spec.get("model"),
            max_tokens=spec.get("max_tokens"),
            timeout_seconds_declared=None,
            timeout_seconds_effective=spec.get("timeout_seconds"),
            seed=spec.get("seed"),
            thinking=spec.get("thinking"),
            reads_commitment_surface=reads,
            reads_commitment_surface_reason=reason))
    return tuple(rows)


def _coordinate_rows(reader: _Reader, occ_dir: Path) -> tuple[CoordinateRow, ...]:
    """Every `artifacts/<problem>/<arm>/cycleNN/<node>.json` under the occurrence.

    Presence only: the file is digested, never opened (U2).
    """
    artifacts = occ_dir / "artifacts"
    if not artifacts.is_dir():
        return ()
    rows: list[CoordinateRow] = []
    for path in sorted(artifacts.glob("*/*/cycle*/*.json")):
        cycle_dir = path.parent.name
        if not cycle_dir.startswith("cycle") or not cycle_dir[5:].isdigit():
            continue
        reader.note(path)
        rows.append(CoordinateRow(problem=path.parent.parent.parent.name,
                                  arm=path.parent.parent.name,
                                  cycle=int(cycle_dir[5:]),
                                  node=path.stem,
                                  artifact_present=True))
    return tuple(sorted(rows, key=lambda r: (r.problem, r.arm, r.cycle, r.node)))


def _provider_call_count(occ_dir: Path) -> int:
    provider = occ_dir / "provider"
    if not provider.is_dir():
        return 0
    return sum(1 for _ in provider.glob("**/call-*.response.json"))


def _occurrence_row(reader: _Reader, study: Path, occ_dir: Path) -> OccurrenceRow:
    """One occurrence, read in whichever of the two published plan shapes it has."""
    arms_path, plan_path = occ_dir / "arms.json", occ_dir / "plan.json"
    if not plan_path.is_file():
        return OccurrenceRow(
            study=study.name, occurrence=occ_dir.name, readable=False,
            unreadable_reason="missing plan.json", study_id=None, plan_id=None,
            runner_sha256=None, helper_sha256=None, provider_mode=None, scope=None,
            max_calls=None, arms=(), coordinates=(), provider_call_records=0)
    plan = reader.read_json(plan_path)
    if not isinstance(plan, dict):
        return OccurrenceRow(
            study=study.name, occurrence=occ_dir.name, readable=False,
            unreadable_reason="plan.json is not a JSON object", study_id=None,
            plan_id=None, runner_sha256=None, helper_sha256=None, provider_mode=None,
            scope=None, max_calls=None, arms=(), coordinates=(),
            provider_call_records=0)
    arms_doc: dict[str, Any] = {}
    if arms_path.is_file():
        loaded = reader.read_json(arms_path)
        arms_doc = loaded if isinstance(loaded, dict) else {}
    declared = arms_doc.get("arms")
    if isinstance(declared, dict):
        ceilings = plan.get("ceilings")
        arms = _arm_rows_from_arms_json(
            declared, ceilings if isinstance(ceilings, dict) else {})
    elif isinstance(plan.get("arms"), list):
        settings = plan.get("settings")
        arms = _arm_rows_from_plan_settings(
            plan["arms"], settings if isinstance(settings, dict) else {})
    else:
        return OccurrenceRow(
            study=study.name, occurrence=occ_dir.name, readable=False,
            unreadable_reason="no arm declaration: arms.json carries no `arms` "
                              "mapping and plan.json carries no `arms` list",
            study_id=plan.get("study_id"), plan_id=plan.get("plan_id"),
            runner_sha256=plan.get("runner_sha256"),
            helper_sha256=plan.get("helper_sha256"), provider_mode=None, scope=None,
            max_calls=plan.get("max_calls"), arms=(),
            coordinates=_coordinate_rows(reader, occ_dir),
            provider_call_records=_provider_call_count(occ_dir))
    return OccurrenceRow(
        study=study.name, occurrence=occ_dir.name, readable=True,
        unreadable_reason=None,
        study_id=plan.get("study_id"), plan_id=plan.get("plan_id"),
        runner_sha256=plan.get("runner_sha256"),
        helper_sha256=plan.get("helper_sha256"),
        provider_mode=plan.get("provider_mode", arms_doc.get("provider")),
        scope=plan.get("scope", arms_doc.get("scope")),
        max_calls=plan.get("max_calls"),
        arms=arms,
        coordinates=_coordinate_rows(reader, occ_dir),
        provider_call_records=_provider_call_count(occ_dir))


def _validate_proposal(proposal: Any) -> dict[str, Any]:
    if not isinstance(proposal, dict) or set(proposal) != PROPOSAL_REQUIRED:
        raise InventoryError(
            "MALFORMED_PROPOSAL: expected exactly the keys %s"
            % sorted(PROPOSAL_REQUIRED))
    if not isinstance(proposal.get("cycle"), int) or isinstance(proposal["cycle"], bool):
        raise InventoryError("MALFORMED_PROPOSAL: cycle must be an integer")
    if not isinstance(proposal.get("problem"), str) or not proposal["problem"]:
        raise InventoryError("MALFORMED_PROPOSAL: problem must be a non-empty string")
    return dict(proposal)


def compare_proposal(proposal: dict[str, Any],
                     occurrences: Iterable[OccurrenceRow]) -> tuple[ProposalRow, ...]:
    """Place a proposed arm beside every published arm of the same kind+endpoint.

    Nothing here is a verdict. ``fields_differing`` is the report (U6/U7).
    """
    rows: list[ProposalRow] = []
    for occ in occurrences:
        if not occ.readable:
            continue
        for arm in occ.arms:
            # An arm is placed beside the proposal when it carries the same NAME,
            # or the same declared kind on the same endpoint. The first clause
            # matters because an owner-runner occurrence records no kind at all
            # (`kind_source` `plan_settings`), and dropping those rows would hide
            # exactly the published arms a proposal is most likely to duplicate.
            same_name = arm.arm == proposal["arm"]
            same_kind_and_endpoint = (arm.kind is not None
                                      and arm.kind == proposal["kind"]
                                      and arm.endpoint == proposal["endpoint"])
            if not (same_name or same_kind_and_endpoint):
                continue
            published = {
                "endpoint": arm.endpoint, "kind": arm.kind, "surface": arm.surface,
                "max_tokens": arm.max_tokens, "seed": arm.seed,
                "timeout_seconds": (arm.timeout_seconds_declared
                                    if arm.timeout_seconds_declared is not None
                                    else arm.timeout_seconds_effective),
            }
            identical = tuple(f for f in COMPARED_FIELDS
                              if published.get(f) == proposal.get(f))
            differing = tuple(f for f in COMPARED_FIELDS if f not in identical)
            at_coord = sum(1 for c in occ.coordinates
                           if c.arm == arm.arm and c.problem == proposal["problem"]
                           and c.cycle == proposal["cycle"] and c.artifact_present)
            rows.append(ProposalRow(
                study=occ.study, occurrence=occ.occurrence, arm=arm.arm,
                problem_and_cycle_match=at_coord > 0,
                terminal_artifacts_at_that_coordinate=at_coord,
                fields_identical=identical, fields_differing=differing,
                published_values=published))
    return tuple(sorted(rows, key=lambda r: (r.study, r.occurrence, r.arm)))


def build_inventory(study_dirs: Sequence[str | Path],
                    proposal: dict[str, Any] | None = None) -> Inventory:
    """Inventory every ``occurrence*`` directory under each named study."""
    studies = [Path(s) for s in study_dirs]
    present = [s for s in studies if s.is_dir()]
    if not present:
        raise SelectorMatchedNothing(
            "SELECTOR_MATCHED_NOTHING: none of %s is a directory"
            % [str(s) for s in studies])
    reader = _Reader(present)
    occurrences: list[OccurrenceRow] = []
    for study in sorted(present, key=lambda p: p.name):
        for occ_dir in _occurrence_dirs(study):
            occurrences.append(_occurrence_row(reader, study, occ_dir))
    if not occurrences:
        raise InventoryError(
            "NO_STUDY_DIRECTORY: no occurrence directory under %s"
            % [str(s) for s in present])
    checked = _validate_proposal(proposal) if proposal is not None else None
    rows = compare_proposal(checked, occurrences) if checked is not None else ()
    return Inventory(
        instrument_version=INSTRUMENT_VERSION, schema=INVENTORY_SCHEMA,
        banner=INVENTORY_BANNER, fcl_surface_arms=tuple(FCL_SURFACE_ARMS),
        occurrences=tuple(occurrences), proposal=checked, proposal_rows=rows,
        files_read=reader.files_read)


def write_inventory(inventory: Inventory, out_dir: str | Path) -> tuple[Path, Path]:
    """Write ``INVENTORY.md`` and ``inventory.json`` into a **new** directory."""
    out = Path(out_dir)
    try:
        out.mkdir(parents=True, exist_ok=False)
    except FileExistsError as exc:
        raise OutDirRefused("OUT_DIR_REFUSED: %s already exists" % out) from exc
    except OSError as exc:
        raise OutDirRefused("OUT_DIR_REFUSED: %s (%s)" % (out, exc)) from exc
    markdown, payload = out / "INVENTORY.md", out / "inventory.json"
    markdown.write_text(inventory.to_markdown(), encoding="utf-8")
    payload.write_text(inventory.to_json(), encoding="utf-8")
    return markdown, payload


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("out_dir", help="new directory to write into")
    parser.add_argument("--study", action="append", required=True,
                        help="a study directory holding occurrence* dirs; repeatable")
    parser.add_argument("--proposal", default=None,
                        help="JSON file declaring one proposed arm to place beside "
                             "the published ones")
    args = parser.parse_args(argv)
    proposal = None
    if args.proposal is not None:
        try:
            proposal = json.loads(Path(args.proposal).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print("MALFORMED_PROPOSAL: %s" % exc, file=sys.stderr)
            return 3
    out = Path(args.out_dir).resolve()
    for study in args.study:
        study_resolved = Path(study).resolve()
        if out == study_resolved or out.is_relative_to(study_resolved):
            print("OUT_DIR_REFUSED: %s is inside the study %s" % (out, study),
                  file=sys.stderr)
            return 4
    try:
        inventory = build_inventory(args.study, proposal)
    except SelectorMatchedNothing as exc:
        print(str(exc), file=sys.stderr)
        return 5
    except InventoryError as exc:
        print(str(exc), file=sys.stderr)
        return 3
    try:
        markdown, payload = write_inventory(inventory, out)
    except OutDirRefused as exc:
        print(str(exc), file=sys.stderr)
        return 4
    print(json.dumps({"inventory_markdown": str(markdown),
                      "inventory_json": str(payload),
                      "occurrences": len(inventory.occurrences),
                      "proposal_rows": len(inventory.proposal_rows)},
                     sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
