"""How readings and marks enter the graph (wave 1, module W1-GRAPH).

Purpose
-------
A thin, well-typed layer over the vendored :mod:`deepreason_core` harness.  It owns the
six artifact shapes of the automated loop and nothing else: the standard artifact, the
material, the per-cell *unresolved* default, the reading (with its split validity nodes
and its rubric-typed demonstrative warrant), the audit finding, and the appellate ruling.
It registers them, and it reads a cell's standing back out of the adjudication.  It holds
no state of its own, writes no file the harness does not write, and never assigns a
status: every label in this module comes from the vendored two-pass grounded adjudicator,
whose only inputs are ``att`` and ``dep``.

The whole shape of the module follows from one sentence of the design: *for every cell,
first register a small unresolved artifact as the grounded default*.  The table therefore
starts, correctly, entirely unresolved, and it is not a rule that says so — the default is
unattacked, so pass 1 accepts it.  A reading is then an argumentative move against that
default: an artifact carrying a DEMONSTRATIVE warrant whose commitment is the rubric
``rubric:reading-v1``, whose ``validity_node`` cites the registered standard, and whose
``trace_ref`` is a conforming trial transcript.  ``Harness._validate_warrant`` refuses the
registration if the transcript does not conform, so the §10 guard is unbypassable
*because the commitment is rubric-typed* — not because anyone remembered to check.

Refuting the standard, a sustained audit hit against the judge seat's validity node, or an
appellate ruling against either validity node all collapse the reading the same way: the
vendored case-law, evidence and validity-node closures put an attack on the reading's
carrier, pass 1 stops accepting it, and the unresolved default is reinstated.  Nothing is
deleted, nothing is rewritten, and no status rule outside ``att``/``dep`` is consulted.
Marks enter by exactly the same path, one register at a time, and are never combined.

Design section implemented
--------------------------
Automated-loop design of record, §3 ("How readings and marks enter the graph") in full,
including its six shapes (a)-(f), its "what never registers" clause, its four computed
consequences, and its appellate paragraph; §2.4 G2b and G12 for what the transcript must
satisfy and what the scoring-key guard covers; §2.5 for the audit warrant's shape; and
the W1-GRAPH entry of §7 for the public interface and the acceptance conditions.

The vendored ``verdict`` field, and where G12 stops (O2)
-------------------------------------------------------
``verdict`` is a member of :data:`~minireason.loop.standard.FORBIDDEN_KEYS` (G12) *and*
the name of a field on the vendored ``Warrant`` record and inside the vendored trial
transcript.  Both are correct and neither may move: narrowing the key set would weaken
every other study that shares it, and editing the vendored ontology is vendoring drift.
G12's subject is the artifact **content** this loop authors, so that is exactly where the
guard runs.  Every loop-authored body — cell-open, reading, validity node, audit finding,
appellate ruling — is passed through ``contracts.assert_no_scoring_keys`` before it is
stored, and a body carrying a scoring key is refused, not stripped.  The two vendored
record shapes named in :data:`G12_EXEMPT` are not walked: the ``Warrant`` record
itself, and the trial transcript whose ``ruling.verdict`` spelling
``deepreason_core.harness.transcript_blob`` fixes and ``conforming_transcript`` reads.
The transcript is registered as an artifact (the validity node cites it as evidence), so
that exemption is one artifact wide and is named, not implied.

Deviations from the design, and why
-----------------------------------
1. **The validity node does not declare the material as evidence.**  §3(e) says
   ``ν_soundness`` carries ``evidence`` refs "to ``E_row`` and to the transcript
   artifact".  Under the vendored evidence closure that would make every attacker of
   ``E_row`` an attacker of the validity node, hence of the reading's carrier — so
   refuting the material would leave the reading **refuted**.  That contradicts both §3's
   own "Invalidate ``E_row`` ⇒ the reading becomes ``suspended_unsupported``, not
   ``refuted``.  Orphaned is not false" and the W1-GRAPH acceptance condition that
   repeats it.  The material is therefore carried where it belongs: as a ``dependence``
   ref on the reading and on the cell-open, so its refutation reaches them through pass 2
   as ``suspended_unsupported``.  The transcript stays an ``evidence`` ref, and carries no
   ``dependence`` ref of its own, so no lineage walk re-opens the same hole.
2. **``ν_soundness`` declares ``ν_bearing`` as evidence.**  §3(e) names the two nodes and
   says "a criticism can then land on bearing alone, which R2 requires", but it names no
   edge that would make that true: only a warrant's own ``validity_node`` is closed over,
   and the warrant has one.  Without an edge, attacking bearing would be inert.  The
   evidence closure is the calculus' own spelling for "this is load-bearing for that
   validity", so ``ν_soundness`` cites ``ν_bearing`` as evidence and an appeal against
   bearing alone collapses the reading in pass 1.
3. **Loop-authored content carries a ``schema`` field.**  The vendored ontology forbids a
   ``kind`` field *on the artifact record* — dispatch is on interface structure.  Content
   is opaque bytes plus a codec, and this module needs to read its own shapes back out of
   a graph it shares with imported material, so each body it authors names its schema
   inside the content, exactly as W0-STANDARD's body already does.  Nothing in the
   harness reads it; only :func:`cell_standing` and its siblings do.
4. **The design's "suspended" is the vendored ``refuted``.**  §3 says a sustained reading
   leaves the default suspended.  In the vendored status vocabulary a default with an
   accepted attacker is ``refuted``; ``suspended`` means an attack that pass 1 could not
   resolve, and ``suspended_unsupported`` means orphaned.  This module reports the
   vendored label unchanged and adds :data:`CELL_STATES`, a five-token read-back that
   keeps the two apart.
5. **``contracts`` is imported although the wave plan lists only W0-TYPES and
   W0-STANDARD.**  ``assert_no_scoring_keys`` is the one G12 guard in the repository;
   a second copy of it here would be a second thing to drift.  The edge
   ``graph -> contracts -> standard -> types`` is acyclic.

What this module refuses to do
------------------------------
It mints no ``att`` edge on any node under study and no ``dep`` edge between studied
nodes: a reading's only attack is on its own cell's unresolved default, and its only
dependence is on the material it reads.  It exposes no count, no score and no rank of
readings: two surviving rivals are returned as two identities and the cell is
``contested``, which is a problem to be discriminated, never an average.  It never writes
``status``; it never deletes; and ``unresolved`` is never *entered* as a reading, because
it is already the standing of every cell that no reading has attacked.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any

from deepreason_core.canonical import canonical_json, sha256_hex
from deepreason_core.harness import (
    Harness,
    ReadOnlyHarnessError,
    WellFormednessError,
    conforming_transcript,
    transcript_blob,
)
from deepreason_core.ontology import (
    Artifact,
    Commitment,
    Interface,
    LLMCall,
    Provenance,
    Ref,
    Rule,
    Status,
    Warrant,
    WarrantType,
)

from minireason.loop.contracts import assert_no_scoring_keys
from minireason.loop.standard import (
    DIFFERENCE_KINDS,
    MARKS,
    MODE_ABSOLUTE,
    MODE_PAIRWISE,
    READING_VOCABULARY,
    REGISTER_IDS,
    SPEC_ID,
    STANDARD_BODY,
    UNRESOLVED_TOKEN,
    assert_no_exhaustion_claim,
)
from minireason.loop.types import LoopError

__all__ = [
    "APPEAL_SCHEMA",
    "AUDIT_KINDS",
    "AUDIT_SCHEMA",
    "AppellateRuling",
    "AuditFinding",
    "CELL_OPEN_SCHEMA",
    "CELL_STATES",
    "CONTESTED",
    "CellKey",
    "CellStanding",
    "GraphError",
    "KAPPA_AUDIT_PREFIX",
    "KAPPA_READ_PREFIX",
    "NEW_CODES",
    "PRODUCED_SCHEMAS",
    "RECORD_FIELD",
    "RECORD_KINDS",
    "RECORDS_NOT_READ",
    "Production",
    "READING_SCHEMA",
    "READ",
    "ReadingIds",
    "ReadingResult",
    "G12_EXEMPT",
    "SUSPENDED",
    "Transcript",
    "UNRESOLVED",
    "UNSUPPORTED",
    "VALIDITY_SCHEMA",
    "ValidityNodes",
    "appellate_rulings",
    "apply_appeal",
    "cell_standing",
    "cell_standings",
    "cell_state",
    "fixed_clock",
    "mark_triples",
    "open_cells",
    "open_graph",
    "produced",
    "register_audit_warrant",
    "register_kappa_read",
    "register_mark",
    "register_material",
    "register_reading",
    "register_standard",
    "register_transcript",
    "resolve_graph_root",
    "split_validity_nodes",
    "validity_nodes_for_seat",
]


# --------------------------------------------------------------------- failures

#: Stable failure codes this module raises, each with the reason it exists.  Wave 0
#: deliberately does not enforce ``types.FAILURE_CODES`` membership at raise time (O9);
#: these are declared here so the integrator can fold them into that table in the same
#: commit that lands this module.
NEW_CODES: Mapping[str, str] = MappingProxyType({
    "GRAPH_ROOT_INVALID": "the harness root is empty, absolute where it must be relative, or climbs out of the repository",
    "GRAPH_READ_ONLY": "a registration was attempted through a time-travel materialization",
    "IDENTIFIER_INVALID": "a seat, spec id, ruling id or clock stamp is empty or carries the reserved separator",
    "APPEAL_MALFORMED": "an appellate ruling is missing its id, the node it attacks, or its stated ground",
    "CELL_KEY_INVALID": "a cell key is empty, names a register outside REGISTER_IDS, or carries the reserved separator",
    "CELL_NOT_OPEN": "a reading, mark, standing or appeal names a cell with no registered unresolved default",
    "STANDARD_NOT_REGISTERED": "a reading cites a standard artifact that is not in this graph, so the case-law closure could not fire",
    "READING_TOKEN_UNKNOWN": "the entered token is outside the closed vocabulary this cell is read under",
    "READING_TOKEN_UNRESOLVED": "unresolved is the grounded default and is never entered as a reading",
    "MARK_REGISTER_MISSING": "a mark was offered for a cell whose key names no single register; marks are never combined",
    "MARK_REGISTER_UNEXPECTED": "a relation reading was offered for a per-register cell, which only a mark may occupy",
    "DIFFERENCE_KIND_UNKNOWN": "a mark's difference_kind is not one of that register's closed tokens",
    "DIFFERENCE_KIND_UNEXPECTED": "a difference_kind was offered where the rubric admits none",
    "TRANSCRIPT_MALFORMED": "a trial transcript is missing case, answer, decisive_point or its checks mapping",
    "TRANSCRIPT_POINT_NOT_UNIQUE": "the decisive_point does not occur exactly once in case + newline + answer (G2b)",
    "TRANSCRIPT_NOT_CONFORMING": "the vendored registration gate refused the transcript, so no warrant was minted",
    "AUDIT_KIND_UNKNOWN": "an audit finding names a kind outside the three that mint warrants",
    "APPEAL_TARGET_UNKNOWN": "an appellate ruling names a node that is not registered in this graph",
    "REGISTRATION_REFUSED": "the vendored harness refused the registration on its own formation rules",
})

_GRAPH_ROOT_INVALID = "GRAPH_ROOT_INVALID"
_GRAPH_READ_ONLY = "GRAPH_READ_ONLY"
_IDENTIFIER_INVALID = "IDENTIFIER_INVALID"
_APPEAL_MALFORMED = "APPEAL_MALFORMED"
_CELL_KEY_INVALID = "CELL_KEY_INVALID"
_CELL_NOT_OPEN = "CELL_NOT_OPEN"
_STANDARD_NOT_REGISTERED = "STANDARD_NOT_REGISTERED"
_READING_TOKEN_UNKNOWN = "READING_TOKEN_UNKNOWN"
_READING_TOKEN_UNRESOLVED = "READING_TOKEN_UNRESOLVED"
_MARK_REGISTER_MISSING = "MARK_REGISTER_MISSING"
_MARK_REGISTER_UNEXPECTED = "MARK_REGISTER_UNEXPECTED"
_DIFFERENCE_KIND_UNKNOWN = "DIFFERENCE_KIND_UNKNOWN"
_DIFFERENCE_KIND_UNEXPECTED = "DIFFERENCE_KIND_UNEXPECTED"
_TRANSCRIPT_MALFORMED = "TRANSCRIPT_MALFORMED"
_TRANSCRIPT_POINT_NOT_UNIQUE = "TRANSCRIPT_POINT_NOT_UNIQUE"
_TRANSCRIPT_NOT_CONFORMING = "TRANSCRIPT_NOT_CONFORMING"
_AUDIT_KIND_UNKNOWN = "AUDIT_KIND_UNKNOWN"
_APPEAL_TARGET_UNKNOWN = "APPEAL_TARGET_UNKNOWN"
_REGISTRATION_REFUSED = "REGISTRATION_REFUSED"


class GraphError(LoopError):
    """A declared refusal from the graph layer.

    A :class:`~minireason.loop.types.LoopError`, so one ``except LoopError`` catches
    every loop refusal and ``.code`` is the token a receipt records.  The detail never
    changes the code.
    """


# --------------------------------------------------------------------- vocabulary

#: The content ``schema`` names this module authors.  A body that names none of them was
#: not written here (imported material, a foreign artifact) and is never parsed as one.
CELL_OPEN_SCHEMA = "minireason.loop.graph.cell-open.v1"
READING_SCHEMA = "minireason.loop.graph.reading.v1"
VALIDITY_SCHEMA = "minireason.loop.graph.validity-node.v1"
AUDIT_SCHEMA = "minireason.loop.graph.audit-finding.v1"
APPEAL_SCHEMA = "minireason.loop.graph.appellate-ruling.v1"

#: The standard body's own schema name, as W0-STANDARD writes it.  §3(a)
#: registers the body exactly as ``standard`` emits it, so it carries no
#: ``record`` token; :func:`_appealable` recognises it by this instead.
STANDARD_BODY_SCHEMA = "minireason.loop.reading-rubric.v1"
PRODUCED_SCHEMAS: tuple[str, ...] = (
    CELL_OPEN_SCHEMA, READING_SCHEMA, VALIDITY_SCHEMA, AUDIT_SCHEMA, APPEAL_SCHEMA,
)

#: The ``record`` field, and the token each loop-authored body carries in it.
#:
#: ``schema`` says *which shape this module wrote*; ``record`` says *what kind of
#: record it is* in the vocabulary W1-OBLIGATIONS' predicates read
#: (``obligations.RECORD_FIELD`` / ``obligations.RECORD_KINDS``).  Wave-1
#: integration decision 2 makes **this module the writer of record**: obligations
#: reads exactly these tokens and does not guess a kind from a schema name, and
#: ``tests/loop/test_obligations.py`` evaluates every predicate against a graph
#: this module populated.
#:
#: A reading is ``reading_row`` or ``cell_mark`` according to its cell: one mark
#: per register, never combined, so the two kinds are never one record.
RECORD_FIELD = "record"
RECORD_CELL_OPEN = "cell_open"
RECORD_READING_ROW = "reading_row"
RECORD_CELL_MARK = "cell_mark"
RECORD_VALIDITY_NODE = "validity_node"
RECORD_AUDIT_RECORD = "audit_record"
RECORD_APPELLATE_RULING = "appellate_ruling"

#: record token -> the schema of the body that carries it.
RECORD_KINDS: Mapping[str, str] = MappingProxyType({
    RECORD_CELL_OPEN: CELL_OPEN_SCHEMA,
    RECORD_READING_ROW: READING_SCHEMA,
    RECORD_CELL_MARK: READING_SCHEMA,
    RECORD_VALIDITY_NODE: VALIDITY_SCHEMA,
    RECORD_AUDIT_RECORD: AUDIT_SCHEMA,
    RECORD_APPELLATE_RULING: APPEAL_SCHEMA,
})

#: The two tokens this module writes that **no obligations predicate reads**, and
#: the reason each is written anyway.  A validity node and an appellate ruling are
#: nodes of the adjudication, not records an obligation quantifies over; they carry
#: a ``record`` so that a reader of the graph - and G12's scan - can tell what every
#: loop-authored body is without inferring it from a schema string.
RECORDS_NOT_READ: Mapping[str, str] = MappingProxyType({
    RECORD_VALIDITY_NODE:
        "a node of the calculus: what it supports is read through att/dep, never as a record",
    RECORD_APPELLATE_RULING:
        "precedent: W2-PACKS ranks it and p8 asks only that nothing BLOCKS on it",
})

#: What an appellate ruling may be aimed at (§3, Appellate; REVIEW-WAVE1 S1).
#: The design's own list: "``ν_bearing``, ``ν_soundness``, ``STD_READING``, a
#: register definition, or a marker's ``difference_kind`` set" - three node
#: kinds, none of which is a node under study.  An appeal aimed at an ``E_row``
#: or an ``E_cell`` would put a warrant edge onto the material itself, which is
#: a ``p7`` loss: the chain stops with a ``protected_loss`` at the next
#: decision, for a ruling nobody meant as an attack on the evidence.  It is
#: refused at the write instead, with the code that names the target.
#:
#: The standard is recognised by its artifact id rather than by a ``record``
#: token - §3(a) registers it as the standard body, which carries none - so the
#: check admits an appeal whose ``standard_id`` IS the target.
APPEALABLE_RECORDS: frozenset[str] = frozenset({
    RECORD_VALIDITY_NODE,
    RECORD_APPELLATE_RULING,
})

#: The material (§3(b)) deliberately carries **no** ``record`` field: its bytes are
#: the instrument's, registered exactly as emitted, and this module may not add a
#: key to them.  The ``material`` record an obligation reads is a record *about* the
#: material, registered beside it by W5-DRIVER, which is why ``p1`` and the material
#: half of ``o3`` read ``not_evaluable`` on a graph only this module has populated.
MATERIAL_CARRIES_NO_RECORD_FIELD = True

#: Commitment id prefixes.  ``rubric:`` is what makes the trial guard unbypassable;
#: ``program:`` is what lets an audit hit land without demanding a transcript of a
#: deterministic checker.
KAPPA_READ_PREFIX = "kappa:read:"
KAPPA_AUDIT_PREFIX = "kappa:audit:"

#: The audit arms that mint a warrant (§2.5).  Ensemble disagreement is deliberately not
#: here: the design records it as a Measure series, never as a verdict.
AUDIT_KINDS: tuple[str, ...] = (
    "paraphrase-invariance", "premise-deletion", "planted-flaw-calibration",
)

UNRESOLVED = "unresolved"
READ = "read"
CONTESTED = "contested"
SUSPENDED = "suspended"
UNSUPPORTED = "unsupported"

#: How a cell reads back out of the adjudication.  Five states, no sixth, and none of
#: them is a quantity: ``unresolved`` the grounded default still stands; ``read`` exactly
#: one reading is accepted; ``contested`` two or more rival readings survive, which §3
#: turns into a discrimination problem and never into an average; ``suspended`` an attack
#: on the default that pass 1 could not resolve; ``unsupported`` the material beneath the
#: cell is not accepted, so the cell is orphaned rather than false.
CELL_STATES: tuple[str, ...] = (UNRESOLVED, READ, CONTESTED, SUSPENDED, UNSUPPORTED)

#: The two vendored record shapes G12's scan does not walk, and why (O2).
G12_EXEMPT: Mapping[str, str] = MappingProxyType({
    "deepreason_core.ontology.Warrant.verdict":
        "the vendored warrant field name; FORBIDDEN_KEYS may not narrow and the ontology may not drift",
    "deepreason_core.harness.transcript_blob:ruling.verdict":
        "the trial transcript shape conforming_transcript reads; the registration gate fixes the spelling",
})

#: Registration rules, so a caller may assert which rule carried which shape.
RULE_STANDARD = Rule.REFL
RULE_IMPORT = Rule.REGISTER
RULE_CRITICISM = Rule.CRIT

ROLE_SEED = "seed"
ROLE_IMPORT = "import"
ROLE_CRITIC = "critic"
ROLE_USER = "user"

CODEC_JSON = "json"

_HEX64 = re.compile(r"[0-9a-f]{64}\Z")
_SEPARATOR = "|"
_TRANSCRIPT_RESERVED = frozenset({"case", "answer", "ruling", "checks"})
_READING_RESERVED = frozenset({
    "schema", "key", "cell", "register", "comparison", "relation", "seat", "mode",
    "standard", "soundness", "bearing", "transcript_ref", "roles", "difference_kind",
    "material", "state",
})

_SOUNDNESS_CLAIM = (
    "the guard as run is a sound procedure for deciding {relation!r} on the bytes of "
    "cell {cell}: the judge panel was cross-family, the cited offsets resolved uniquely "
    "inside the declared spans, the trial transcript conformed, the order swap agreed, "
    "no paraphrase flipped the ruling, and these endpoints, these prompt digests and "
    "this audit record were in force at ruling time"
)
_BEARING_CLAIM = (
    "the reading {relation!r}, if read at all, bears on the claim cell {cell} is offered "
    "for: it is a reading of the material and not of the pack that framed it"
)


# --------------------------------------------------------------------- cell keys

@dataclass(frozen=True)
class CellKey:
    """Which unresolved default a reading or a mark attacks.

    A bare ``cell`` is a relation cell, read under the rubric's absolute mode.  A cell
    that also names a ``register`` (and, on a contrast arm, a ``comparison``) is a mark
    cell, read pairwise.  §3(c) opens one default "for every row and every (cell,
    register, comparison)", and the register is part of the key precisely so that a mark
    can never be combined across registers: there is no key that names two.
    """

    cell: str
    register: str | None = None
    comparison: str | None = None

    def __post_init__(self) -> None:
        _segment(self.cell, "cell")
        if self.register is not None:
            _segment(self.register, "register")
            if self.register not in REGISTER_IDS:
                raise GraphError(
                    _CELL_KEY_INVALID,
                    f"register {self.register!r} is not one of {REGISTER_IDS}")
        if self.comparison is not None:
            _segment(self.comparison, "comparison")
            if self.register is None:
                raise GraphError(
                    _CELL_KEY_INVALID,
                    "a comparison names a per-register cell, so it needs a register")

    @property
    def token(self) -> str:
        """The canonical one-line spelling; unambiguous because no segment may hold
        :data:`_SEPARATOR`."""
        parts = [self.cell]
        if self.register is not None:
            parts.append(self.register)
        if self.comparison is not None:
            parts.append(self.comparison)
        return _SEPARATOR.join(parts)

    @property
    def is_register_cell(self) -> bool:
        return self.register is not None

    @property
    def mode(self) -> str:
        """Absolute for a relation trial, pairwise for a mark — the standard's own two
        modes, not a third."""
        return MODE_PAIRWISE if self.is_register_cell else MODE_ABSOLUTE

    def as_dict(self) -> dict[str, str]:
        body: dict[str, str] = {"cell": self.cell}
        if self.register is not None:
            body["register"] = self.register
        if self.comparison is not None:
            body["comparison"] = self.comparison
        return body

    @classmethod
    def coerce(cls, value: "CellKey | str | Mapping[str, Any]") -> "CellKey":
        """Accept a key, its canonical token, or its mapping form."""
        if isinstance(value, CellKey):
            return value
        if isinstance(value, str):
            parts = value.split(_SEPARATOR)
            if len(parts) > 3:
                raise GraphError(_CELL_KEY_INVALID, f"{value!r} has too many segments")
            return cls(*parts)
        if isinstance(value, Mapping):
            return cls(
                cell=str(value.get("cell", "")),
                register=_optional(value.get("register")),
                comparison=_optional(value.get("comparison")),
            )
        raise GraphError(_CELL_KEY_INVALID, f"{type(value).__name__} is not a cell key")


def _optional(value: Any) -> str | None:
    return None if value is None else str(value)


def _segment(value: Any, where: str, code: str = _CELL_KEY_INVALID) -> str:
    """One unambiguous identifier segment, refused under the caller's own code."""
    if not isinstance(value, str) or not value.strip():
        raise GraphError(code, f"{where} must be a non-empty string")
    if _SEPARATOR in value:
        raise GraphError(code, f"{where} may not contain {_SEPARATOR!r}: {value!r}")
    return value


# --------------------------------------------------------------------- records

@dataclass(frozen=True)
class Transcript:
    """The trial transcript a rubric-derived warrant must carry (§2.4 G2b, §3(f)).

    ``meta`` holds what §3(f) asks the blob to hold beyond the exchange — pack digests,
    both seats' raw record paths, both rulings, the resolved offsets of the decisive
    point, every check result and every paraphrase re-ruling.  It is stored beside the
    vendored keys, never over them.
    """

    case: str
    answer: str
    decisive_point: str
    checks: Mapping[str, Any] = field(default_factory=dict)
    meta: Mapping[str, Any] = field(default_factory=dict)

    @property
    def exchange(self) -> str:
        """``case + "\\n" + answer`` — the surface G2b requires the point to be unique in."""
        return f"{self.case}\n{self.answer}"

    def validated(self) -> "Transcript":
        """Assert G2b and the vendored well-formedness, in that order.

        The program's own check is the strictly stronger one (exactly one occurrence);
        ``conforming_transcript`` is asserted last, at registration, so the guard and the
        registration gate cannot diverge.
        """
        for name, value in (("case", self.case), ("answer", self.answer),
                            ("decisive_point", self.decisive_point)):
            if not isinstance(value, str) or not value.strip():
                raise GraphError(_TRANSCRIPT_MALFORMED, f"{name} is empty")
        if not isinstance(self.checks, Mapping):
            raise GraphError(_TRANSCRIPT_MALFORMED, "checks must be a mapping")
        if not isinstance(self.meta, Mapping):
            raise GraphError(_TRANSCRIPT_MALFORMED, "meta must be a mapping")
        overlap = sorted(_TRANSCRIPT_RESERVED & set(map(str, self.meta)))
        if overlap:
            raise GraphError(
                _TRANSCRIPT_MALFORMED, f"meta may not restate {overlap}")
        found = self.exchange.count(self.decisive_point)
        if found != 1:
            raise GraphError(
                _TRANSCRIPT_POINT_NOT_UNIQUE,
                f"the decisive point resolves {found} times in case + newline + answer")
        return self


@dataclass(frozen=True)
class ReadingResult:
    """What a guarded trial hands the graph (W3-TRIAL's ``TrialResult``, W4-MARKER's mark).

    ``body`` is the reading's own content beyond the fields named here: the resolved
    passage offsets and their occurrence-file spans, the seat identities and families, the
    literal role names, the prompt and raw blob refs and every guard result (§3(d)).  It
    is walked by G12 before it is stored, so a scoring key anywhere inside it is a
    refusal.
    """

    key: CellKey
    relation: str
    seat: str
    transcript: Transcript
    body: Mapping[str, Any] = field(default_factory=dict)
    roles: Mapping[str, str] = field(default_factory=dict)
    difference_kind: str | None = None
    school: str | None = None
    material_id: str | None = None
    llm: LLMCall | None = None

    def validated(self) -> "ReadingResult":
        """Refuse every token the rubric does not admit for this cell.

        ``unresolved`` is refused outright: it is the standing of a cell no reading has
        attacked, so entering it as a reading would be a second way of saying the same
        thing — and the only way a cell could become unresolved by fiat rather than by
        adjudication.
        """
        vocabulary = MARKS if self.key.is_register_cell else READING_VOCABULARY
        if self.relation == UNRESOLVED_TOKEN:
            raise GraphError(
                _READING_TOKEN_UNRESOLVED,
                f"{self.key.token}: unresolved is the grounded default, never a reading")
        if self.relation not in vocabulary:
            raise GraphError(
                _READING_TOKEN_UNKNOWN,
                f"{self.key.token}: {self.relation!r} is outside {tuple(vocabulary)}")
        if self.key.is_register_cell:
            kinds = DIFFERENCE_KINDS[self.key.register]
            if self.relation == "differs" and self.difference_kind not in kinds:
                raise GraphError(
                    _DIFFERENCE_KIND_UNKNOWN,
                    f"{self.key.token}: {self.difference_kind!r} is outside {kinds}")
            if self.relation != "differs" and self.difference_kind is not None:
                raise GraphError(
                    _DIFFERENCE_KIND_UNEXPECTED,
                    f"{self.key.token}: only a differs mark carries a difference_kind")
        elif self.difference_kind is not None:
            raise GraphError(
                _DIFFERENCE_KIND_UNEXPECTED,
                f"{self.key.token}: a relation reading carries no difference_kind")
        if not isinstance(self.seat, str) or not self.seat.strip():
            raise GraphError(_READING_TOKEN_UNKNOWN, "a reading names its judge seat")
        if not isinstance(self.body, Mapping) or not isinstance(self.roles, Mapping):
            raise GraphError(_READING_TOKEN_UNKNOWN, "body and roles are mappings")
        restated = sorted(_READING_RESERVED & set(map(str, self.body)))
        if restated:
            raise GraphError(
                _READING_TOKEN_UNKNOWN,
                f"{self.key.token}: the reading body may not restate {restated}")
        self.transcript.validated()
        return self


class ValidityNodes(tuple):
    """``(soundness, bearing, evidence)`` — one reading's split validity node (§3(e)).

    The first two are the split the rubric draws.  The third is the transcript artifact
    ``ν_soundness`` cites as evidence, which the caller needs by id because attacking it
    is one of the three ways a reading falls.
    """

    __slots__ = ()

    def __new__(cls, soundness: str, bearing: str, evidence: str) -> "ValidityNodes":
        return super().__new__(cls, (soundness, bearing, evidence))

    @property
    def soundness(self) -> str:
        return self[0]

    @property
    def bearing(self) -> str:
        return self[1]

    @property
    def evidence(self) -> str:
        """The registered transcript artifact."""
        return self[2]


@dataclass(frozen=True)
class ReadingIds:
    """Every id one reading put into the graph, so a caller may cite them later."""

    key: str
    target: str
    reading: str
    soundness: str
    bearing: str
    evidence: str
    transcript: str
    warrant: str

    @property
    def artifact_ids(self) -> tuple[str, ...]:
        """The four artifacts, in registration order.  ``transcript`` is the trace_ref
        blob, not an artifact id, and the warrant is not an artifact either."""
        return (self.evidence, self.bearing, self.soundness, self.reading)

    def as_dict(self) -> dict[str, str]:
        return {
            "key": self.key, "target": self.target, "reading": self.reading,
            "soundness": self.soundness, "bearing": self.bearing,
            "evidence": self.evidence, "transcript": self.transcript,
            "warrant": self.warrant,
        }


@dataclass(frozen=True)
class AuditFinding:
    """One audit hit (§2.5), on its way to becoming an ``eval:program`` warrant.

    ``targets`` names the validity nodes to attack.  Left empty, every ``ν_soundness``
    this seat carries on record is used — the whole window, which is what D10's closure
    collapses.  A finding that reaches no reading still registers: a recorded hit against
    a seat that has read nothing yet is a fact about the instrument.
    """

    seat: str
    kind: str
    detail: str = ""
    targets: tuple[str, ...] = ()
    body: Mapping[str, Any] = field(default_factory=dict)

    def validated(self) -> "AuditFinding":
        if self.kind not in AUDIT_KINDS:
            raise GraphError(
                _AUDIT_KIND_UNKNOWN,
                f"{self.kind!r} is outside {AUDIT_KINDS}; ensemble disagreement is a "
                "Measure series, never a warrant")
        _segment(self.seat, "seat", _IDENTIFIER_INVALID)
        return self


@dataclass(frozen=True)
class AppellateRuling:
    """A committed ruling file, ingested as a precedent artifact (§3, Appellate).

    Argumentative: it carries no commitment, so no trial transcript is demanded of a
    human.  It is itself attackable (N1), and its authority is pack ordering — W2-PACKS
    ranks it first — never status privilege.
    """

    ruling_id: str
    target: str
    ground: str
    standard_id: str | None = None
    body: Mapping[str, Any] = field(default_factory=dict)

    def validated(self) -> "AppellateRuling":
        _segment(self.ruling_id, "ruling_id", _APPEAL_MALFORMED)
        if not isinstance(self.target, str) or not self.target.strip():
            raise GraphError(_APPEAL_MALFORMED, "a ruling names the node it attacks")
        if not isinstance(self.ground, str) or not self.ground.strip():
            raise GraphError(_APPEAL_MALFORMED, "a ruling states its ground")
        assert_no_exhaustion_claim(self.ground, f"appeal {self.ruling_id}")
        return self


@dataclass(frozen=True)
class CellStanding:
    """A cell read back out of the adjudication, and nothing else.

    ``accepted`` is a tuple of identities in registration order, never a quantity: two
    surviving rivals are two ids and a ``contested`` state, which §3 turns into a
    discrimination problem.  ``relation`` is filled only when exactly one reading stands.
    """

    key: str
    state: str
    default_id: str
    default_status: str
    standing: tuple[str, ...]
    accepted: tuple[str, ...]
    relation: str | None = None
    register: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "key": self.key, "state": self.state, "default_id": self.default_id,
            "default_status": self.default_status, "standing": list(self.standing),
            "accepted": list(self.accepted), "relation": self.relation,
            "register": self.register,
        }


@dataclass(frozen=True)
class Production:
    """What one cycle put into the graph, for W1-OBLIGATIONS' ProducedBy discharge.

    ``upto_seq`` is the log position to hand back as ``since_seq`` next cycle, so an
    obligation satisfied by artifacts that are *not* in ``artifact_ids`` does not count as
    discharged this cycle.
    """

    artifact_ids: frozenset[str]
    upto_seq: int


# --------------------------------------------------------------------- opening

def fixed_clock(stamp: str = "2026-01-01T00:00:00+00:00") -> Callable[[], str]:
    """A deterministic ``Event.ts`` source, so the log does not fork on machine load.

    §3 opens the harness "with the deterministic ``clock`` parameter"; ordering is
    carried by ``Event.seq``, so a constant stamp is enough and makes two builds of the
    same registrations byte-identical.
    """
    if not isinstance(stamp, str) or not stamp.strip():
        raise GraphError(_IDENTIFIER_INVALID, "a clock stamp is a non-empty iso8601 string")
    return lambda: stamp


def resolve_graph_root(repo_root: Path | str, graph_root: str) -> Path:
    """``repo_root / config.graph_root`` (O1: the declared root is authoritative).

    ``RunPaths.graph`` is the *default* an operator's config should carry; whether the two
    agree is a PREFLIGHT question for W1-STEPS, not a question this module can answer,
    because only the plan records which the operator declared.
    """
    if not isinstance(graph_root, str) or not graph_root.strip():
        raise GraphError(_GRAPH_ROOT_INVALID, "graph_root is empty")
    candidate = Path(graph_root)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise GraphError(
            _GRAPH_ROOT_INVALID, f"graph_root must stay inside the repository: {graph_root!r}")
    return Path(repo_root) / candidate


def open_graph(
    root: Path | str,
    *,
    clock: Callable[[], str] | None = None,
    upto_seq: int | None = None,
    read_only: bool | None = None,
) -> Harness:
    """Open (or create) the harness at ``root``.

    Every registration in this module adjudicates on commit, and reopening replays the
    log and adjudicates once at the end, so a reopened harness and a live one carry the
    same labels by construction rather than by a second code path.
    """
    if root is None or str(root).strip() == "":
        raise GraphError(_GRAPH_ROOT_INVALID, "a harness root is required")
    return Harness(Path(root), clock=clock, upto_seq=upto_seq, read_only=read_only)


# --------------------------------------------------------------------- internals

def _content(body: Mapping[str, Any], *, where: str) -> bytes:
    """Canonical bytes for a loop-authored body, G12 asserted first (§2.4 G12).

    The guard runs here and only here: this is every body this module authors, and the
    two vendored shapes named in :data:`G12_EXEMPT` do not pass through it.
    """
    assert_no_scoring_keys(body)
    del where  # the guard's own exception carries the path
    return canonical_json(body)


def _writable(harness: Harness) -> None:
    """Refuse a time-travel view before a byte is written.

    The vendored store raises a bare ``RuntimeError`` from inside ``put``, which would
    reach a caller with no loop code on it; this refusal keeps the code.
    """
    if getattr(harness.blobs, "read_only", False):
        raise GraphError(_GRAPH_READ_ONLY, "this harness is a time-travel materialization")


def _artifact(
    harness: Harness,
    body: Mapping[str, Any] | bytes,
    *,
    role: str,
    interface: Interface | None = None,
    codec: str = CODEC_JSON,
    school: str | None = None,
    warrants: Sequence[Warrant] = (),
    where: str = "artifact",
) -> Artifact:
    """Build a content-addressed artifact record; the blob is stored, not the artifact."""
    _writable(harness)
    raw = body if isinstance(body, bytes) else _content(body, where=where)
    ref = harness.blobs.put(raw)
    interface = interface or Interface()
    return Artifact(
        id=Artifact.compute_id(ref, codec, interface),
        content_ref=ref,
        codec=codec,
        interface=interface,
        warrants=[w.id for w in warrants],
        provenance=Provenance(role=role, school=school),
    )


def _warrant_id(payload: Mapping[str, Any]) -> str:
    """Content-address the warrant, so re-registering an identical one is a no-op."""
    return f"w:{sha256_hex(canonical_json(payload))}"


def _register(
    harness: Harness,
    entries: list[tuple[Artifact, list[Warrant]]],
    *,
    rule: Rule,
    llm: LLMCall | None = None,
) -> None:
    """One ``register_batch``, with the vendored refusals re-raised under loop codes."""
    try:
        harness.register_batch(entries, rule=rule, llm=llm)
    except ReadOnlyHarnessError as error:
        raise GraphError(_GRAPH_READ_ONLY, str(error)) from error
    except WellFormednessError as error:
        text = str(error)
        code = (_TRANSCRIPT_NOT_CONFORMING
                if "conforming trial transcript" in text else _REGISTRATION_REFUSED)
        raise GraphError(code, text) from error


def _decode(harness: Harness, artifact: Artifact) -> dict[str, Any] | None:
    """The loop-authored body of an artifact, or ``None`` if it is not one of ours."""
    if artifact.codec != CODEC_JSON:
        return None
    ref = artifact.content_ref
    if not isinstance(ref, str) or _HEX64.fullmatch(ref) is None:
        return None
    try:
        body = json.loads(harness.blobs.get(ref))
    except (KeyError, ValueError, OSError):
        return None
    return body if isinstance(body, dict) else None


def _bodies(harness: Harness, schema: str) -> list[tuple[str, dict[str, Any]]]:
    """Every artifact of one authored schema, in registration order."""
    found: list[tuple[str, dict[str, Any]]] = []
    for artifact_id, artifact in harness.state.artifacts.items():
        body = _decode(harness, artifact)
        if body is not None and body.get("schema") == schema:
            found.append((artifact_id, body))
    return found


def _cell_index(harness: Harness) -> dict[str, tuple[str, dict[str, Any]]]:
    """Cell key -> its unresolved default, refusing a second default for one key.

    A dict comprehension let the LAST registration win silently, so a graph with
    two ``C_open`` artifacts for one cell answered every question about that
    cell from one of them and never said which (wave-1 integration decision 49).
    Two defaults for one cell is not a state the adjudication can read: the
    readings attack one of them and the other stands unattacked for ever.
    """

    index: dict[str, tuple[str, dict[str, Any]]] = {}
    for artifact_id, body in _bodies(harness, CELL_OPEN_SCHEMA):
        key = body.get("key")
        if not isinstance(key, str):
            continue
        seen = index.get(key)
        if seen is not None and seen[0] != artifact_id:
            raise GraphError(
                _CELL_KEY_INVALID,
                f"{key} has two unresolved defaults, {seen[0]} and {artifact_id}; "
                "a cell opens once")
        index[key] = (artifact_id, body)
    return index


def _status(harness: Harness, artifact_id: str) -> str:
    label = harness.state.status.get(artifact_id)
    return label.value if isinstance(label, Status) else str(label or "")


# --------------------------------------------------------------------- (a) standard

def register_standard(
    harness: Harness,
    body: bytes = STANDARD_BODY,
    *,
    mention: str | None = None,
) -> str:
    """Register ``std:reading-rubric/v1`` — content-addressed, so calling twice is a no-op.

    §3(a): ``Rule.REFL``, ``provenance.role = SEED``, and a ``mention`` ref to the
    pre-registration text that fixed it.  Every reading's ``ν_soundness`` mentions the id
    this returns, which is what arms the case-law closure: refute the standard and every
    reading under it falls in one pass.
    """
    if not isinstance(body, (bytes, bytearray)) or not body:
        raise GraphError(_STANDARD_NOT_REGISTERED, "the standard body is empty")
    refs = [Ref(target=mention, role="mention")] if mention else []
    artifact = _artifact(
        harness, bytes(body), role=ROLE_SEED, interface=Interface(refs=refs),
        where="standard")
    _register(harness, [(artifact, [])], rule=RULE_STANDARD)
    return artifact.id


def register_kappa_read(harness: Harness, spec_id: str = SPEC_ID) -> str:
    """Register ``κ_read``, the rubric commitment every cell-open declares.

    ``eval`` is ``rubric:<spec-id>``.  That single string is what makes the guard
    unbypassable: ``_validate_warrant`` demands a conforming trial transcript of any
    warrant carrying it, and ``build_att`` runs the case-law closure over any validity
    node citing the standard it resolves to.
    """
    _segment(spec_id, "spec_id", _IDENTIFIER_INVALID)
    commitment = Commitment(id=f"{KAPPA_READ_PREFIX}{spec_id}", eval=f"rubric:{spec_id}")
    try:
        harness.register_commitment(commitment)
    except ReadOnlyHarnessError as error:
        raise GraphError(_GRAPH_READ_ONLY, str(error)) from error
    except WellFormednessError as error:
        raise GraphError(_REGISTRATION_REFUSED, str(error)) from error
    return commitment.id


# --------------------------------------------------------------------- (b) material

def register_material(
    harness: Harness,
    row: bytes | str,
    *,
    codec: str = CODEC_JSON,
    role: str = ROLE_IMPORT,
) -> str:
    """Register ``E_row``/``E_cell`` — the instrument's bytes, exactly as emitted (§3(b)).

    Registered before any provider call, and never re-encoded: the artifact id is the
    content address of those bytes, so a re-import at a different grain is a different
    artifact rather than an edit.
    """
    raw = row.encode("utf-8") if isinstance(row, str) else bytes(row)
    if not raw:
        raise GraphError(_REGISTRATION_REFUSED, "material bytes are empty")
    artifact = _artifact(harness, raw, role=role, codec=codec, where="material")
    _register(harness, [(artifact, [])], rule=RULE_IMPORT)
    return artifact.id


# --------------------------------------------------------------------- (c) the default

def open_cells(
    harness: Harness,
    keys: Iterable["CellKey | str | Mapping[str, Any]"],
    *,
    material_id: str | None = None,
    commitment_id: str | None = None,
) -> dict[str, str]:
    """Register the unresolved default of every cell (§3(c)); returns ``token -> id``.

    Each default is ``{"cell": …, "state": "unresolved"}``, declares ``κ_read`` on its
    interface as the commitment a reading must fail it on, and depends on the material it
    is a cell of.  It is unattacked, therefore accepted: **the table starts, correctly,
    entirely unresolved** — computed by pass 1, not written down by anyone.
    """
    commitment = commitment_id or register_kappa_read(harness)
    refs = [Ref(target=material_id, role="dependence")] if material_id else []
    entries: list[tuple[Artifact, list[Warrant]]] = []
    opened: dict[str, str] = {}
    for raw_key in keys:
        key = CellKey.coerce(raw_key)
        body = {"schema": CELL_OPEN_SCHEMA, RECORD_FIELD: RECORD_CELL_OPEN,
                "key": key.token, "state": UNRESOLVED, **key.as_dict()}
        artifact = _artifact(
            harness, body, role=ROLE_IMPORT,
            interface=Interface(commitments=[commitment], refs=refs),
            where=f"cell-open {key.token}")
        entries.append((artifact, []))
        opened[key.token] = artifact.id
    if entries:
        _register(harness, entries, rule=RULE_IMPORT)
    return opened


# --------------------------------------------------------------------- (d-f) readings

def register_transcript(harness: Harness, transcript: Transcript) -> str:
    """Store the trial transcript; returns the ``trace_ref`` blob hash.

    G2b first — the decisive point must occur *exactly once* in ``case + "\\n" + answer``,
    which is strictly stronger than the vendored predicate — then the vendored
    ``conforming_transcript`` last, so the guard and the registration gate cannot diverge.
    """
    _writable(harness)
    transcript.validated()
    assert_no_scoring_keys(dict(transcript.checks))
    assert_no_scoring_keys(dict(transcript.meta))
    ref = transcript_blob(
        harness,
        case=transcript.case,
        answer=transcript.answer,
        decisive_point=transcript.decisive_point,
        checks=dict(transcript.checks),
        **dict(transcript.meta),
    )
    if not conforming_transcript(harness.blobs, ref):
        raise GraphError(
            _TRANSCRIPT_NOT_CONFORMING,
            "the vendored gate refused the transcript, so no warrant was minted")
    return ref


def split_validity_nodes(
    harness: Harness,
    result: ReadingResult,
    standard_id: str,
) -> ValidityNodes:
    """Register ``ν_soundness`` and ``ν_bearing`` plus the transcript artifact (§3(e)).

    Two nodes, because the rubric distinguishes two claims and R2 requires that a
    criticism be able to land on bearing alone.  Both mention the standard, which arms the
    case-law closure on the node the warrant actually cites.  ``ν_soundness`` declares the
    transcript and ``ν_bearing`` as *evidence*: an attack on either — an audit that shows
    the transcript misrecords the exchange, an appeal that says the reading does not bear
    — lifts onto the validity node and thence onto the reading's carrier, in pass 1.

    The material is deliberately **not** evidence here; it is a ``dependence`` of the
    reading, so refuting it leaves the reading ``suspended_unsupported`` rather than
    refuted.  Orphaned is not false.
    """
    result.validated()
    if standard_id not in harness.state.artifacts:
        raise GraphError(
            _STANDARD_NOT_REGISTERED, f"{standard_id} is not registered in this graph")
    trace_ref = register_transcript(harness, result.transcript)
    transcript_artifact = _artifact(
        harness, harness.blobs.get(trace_ref), role=ROLE_CRITIC, codec=CODEC_JSON,
        school=result.school, where="transcript")

    common = {"key": result.key.token, "relation": result.relation, "seat": result.seat,
              "mode": result.key.mode, "standard": standard_id, **result.key.as_dict()}
    claim_fields = {"relation": result.relation, "cell": result.key.token}
    bearing_claim = _BEARING_CLAIM.format(**claim_fields)
    soundness_claim = _SOUNDNESS_CLAIM.format(**claim_fields)
    assert_no_exhaustion_claim(bearing_claim, "nu_bearing")
    assert_no_exhaustion_claim(soundness_claim, "nu_soundness")

    bearing = _artifact(
        harness,
        {"schema": VALIDITY_SCHEMA, RECORD_FIELD: RECORD_VALIDITY_NODE,
         "aspect": "bearing", "claim": bearing_claim, **common},
        role=ROLE_CRITIC, school=result.school,
        interface=Interface(refs=[Ref(target=standard_id, role="mention")]),
        where="nu_bearing")
    soundness = _artifact(
        harness,
        {"schema": VALIDITY_SCHEMA, RECORD_FIELD: RECORD_VALIDITY_NODE,
         "aspect": "soundness", "claim": soundness_claim,
         "transcript_ref": trace_ref, **common},
        role=ROLE_CRITIC, school=result.school,
        interface=Interface(refs=[
            Ref(target=standard_id, role="mention"),
            Ref(target=transcript_artifact.id, role="evidence"),
            Ref(target=bearing.id, role="evidence"),
        ]),
        where="nu_soundness")
    _register(
        harness,
        [(transcript_artifact, []), (bearing, []), (soundness, [])],
        rule=RULE_CRITICISM)
    return ValidityNodes(soundness.id, bearing.id, transcript_artifact.id)


def register_reading(
    harness: Harness,
    result: ReadingResult,
    standard_id: str,
) -> ReadingIds:
    """Enter one guarded reading (§3(d)-(f)).

    The reading is an artifact carrying a DEMONSTRATIVE warrant against *its own cell's
    unresolved default* and against nothing else: no ``att`` edge on any node under study,
    no ``dep`` edge between studied nodes.  The warrant's commitment is ``κ_read``
    (``rubric:reading-v1``), so the vendored gate refuses the registration outright unless
    ``trace_ref`` holds a conforming trial transcript.
    """
    result.validated()
    if result.key.is_register_cell:
        raise GraphError(
            _MARK_REGISTER_UNEXPECTED,
            f"{result.key.token} is a per-register cell; use register_mark")
    return _enter(harness, result, standard_id)


def register_mark(
    harness: Harness,
    result: ReadingResult,
    standard_id: str,
) -> ReadingIds:
    """Enter one mark, for one register (§3, "marks enter the same way per register").

    Identical machinery, one register at a time.  A key that names no register is refused
    here rather than silently marked across registers: there is no artifact in this graph
    that holds a mark for two registers at once, so no renderer can combine them.
    """
    result.validated()
    if not result.key.is_register_cell:
        raise GraphError(
            _MARK_REGISTER_MISSING,
            f"{result.key.token} names no register; a mark is never combined")
    return _enter(harness, result, standard_id)


def _enter(harness: Harness, result: ReadingResult, standard_id: str) -> ReadingIds:
    index = _cell_index(harness)
    entry = index.get(result.key.token)
    if entry is None:
        raise GraphError(
            _CELL_NOT_OPEN,
            f"{result.key.token} has no unresolved default; open_cells runs first")
    target_id, _ = entry
    # The commitment a reading must fail the cell on is the one that cell declared, not
    # one this function assumes: the guard is unbypassable because THAT eval is rubric-
    # typed, so reading it off the target is the honest spelling.
    declared = list(harness.state.artifacts[target_id].interface.commitments)
    if not declared:
        raise GraphError(
            _CELL_NOT_OPEN, f"{result.key.token}: the default declares no commitment")
    commitment_id = declared[0]
    nodes = split_validity_nodes(harness, result, standard_id)
    soundness_body = _decode(harness, harness.state.artifacts[nodes.soundness]) or {}
    trace_ref = str(soundness_body.get("transcript_ref", ""))

    refs = []
    if result.material_id:
        refs.append(Ref(target=result.material_id, role="dependence"))
    refs.append(Ref(target=standard_id, role="mention"))

    warrant = Warrant(
        id=_warrant_id({"target": target_id, "commitment": commitment_id,
                        "validity_node": nodes.soundness, "trace_ref": trace_ref,
                        "type": WarrantType.DEMONSTRATIVE.value}),
        target=target_id,
        type=WarrantType.DEMONSTRATIVE,
        commitment=commitment_id,
        verdict="fail",
        trace_ref=trace_ref,
        validity_node=nodes.soundness,
    )
    body = {
        "schema": READING_SCHEMA,
        RECORD_FIELD: (RECORD_CELL_MARK if result.key.is_register_cell
                       else RECORD_READING_ROW),
        "key": result.key.token,
        "relation": result.relation,
        "seat": result.seat,
        "mode": result.key.mode,
        "standard": standard_id,
        "soundness": nodes.soundness,
        "bearing": nodes.bearing,
        "transcript_ref": trace_ref,
        "roles": dict(result.roles),
        **result.key.as_dict(),
        **({"difference_kind": result.difference_kind}
           if result.difference_kind is not None else {}),
        **({"material": result.material_id} if result.material_id else {}),
        **dict(result.body),
    }
    reading = _artifact(
        harness, body, role=ROLE_CRITIC, school=result.school,
        interface=Interface(refs=refs), warrants=[warrant],
        where=f"reading {result.key.token}")
    _register(harness, [(reading, [warrant])], rule=RULE_CRITICISM, llm=result.llm)
    return ReadingIds(
        key=result.key.token, target=target_id, reading=reading.id,
        soundness=nodes.soundness, bearing=nodes.bearing, evidence=nodes.evidence,
        transcript=trace_ref, warrant=warrant.id)


# --------------------------------------------------------------------- audits

def validity_nodes_for_seat(harness: Harness, seat: str) -> tuple[str, ...]:
    """Every ``ν_soundness`` this judge seat carries, in registration order.

    This is the window D10's closure collapses when an audit hit lands on the seat.
    """
    return tuple(
        artifact_id for artifact_id, body in _bodies(harness, VALIDITY_SCHEMA)
        if body.get("aspect") == "soundness" and body.get("seat") == seat)


def register_audit_warrant(harness: Harness, finding: AuditFinding) -> str:
    """Enter one audit hit as an ``eval:program`` DEMONSTRATIVE warrant (§2.5).

    The commitment is program-typed, so the vendored gate demands no trial transcript of a
    deterministic checker.  One warrant per validity node in the seat's window, all
    carried by the one finding artifact and all sharing the finding's own ``ν_audit`` —
    so the audit is itself attackable, and attacking it reinstates every reading it
    collapsed.  By the validity-node closure this collapses the seat's readings in pass 1
    without anyone deciding to withdraw them.
    """
    _writable(harness)
    finding.validated()
    targets = tuple(finding.targets) or validity_nodes_for_seat(harness, finding.seat)
    unknown = [t for t in targets if t not in harness.state.artifacts]
    if unknown:
        raise GraphError(
            _APPEAL_TARGET_UNKNOWN, f"audit targets not registered: {sorted(unknown)}")

    commitment = Commitment(
        id=f"{KAPPA_AUDIT_PREFIX}{finding.kind}",
        eval=f"program:minireason.loop.audits/{finding.kind}")
    try:
        harness.register_commitment(commitment)
    except WellFormednessError as error:
        raise GraphError(_REGISTRATION_REFUSED, str(error)) from error

    body = {"schema": AUDIT_SCHEMA, RECORD_FIELD: RECORD_AUDIT_RECORD,
            "seat": finding.seat, "kind": finding.kind,
            "detail": finding.detail, "window": list(targets), **dict(finding.body)}
    trace_ref = harness.blobs.put(_content(body, where="audit"))
    nu = _artifact(
        harness,
        {"schema": VALIDITY_SCHEMA, RECORD_FIELD: RECORD_VALIDITY_NODE,
         "aspect": "audit", "seat": finding.seat,
         "kind": finding.kind,
         "claim": f"the {finding.kind} check as run is a sound and relevant test of the "
                  f"readings seat {finding.seat} carried in this window"},
        role=ROLE_CRITIC, where="nu_audit")
    _register(harness, [(nu, [])], rule=RULE_CRITICISM)

    warrants = [
        Warrant(
            id=_warrant_id({"target": target, "commitment": commitment.id,
                            "validity_node": nu.id, "trace_ref": trace_ref,
                            "type": WarrantType.DEMONSTRATIVE.value}),
            target=target,
            type=WarrantType.DEMONSTRATIVE,
            commitment=commitment.id,
            verdict="fail",
            trace_ref=trace_ref,
            validity_node=nu.id,
        )
        for target in targets
    ]
    artifact = _artifact(
        harness, body, role=ROLE_CRITIC, warrants=warrants, where="audit")
    _register(harness, [(artifact, list(warrants))], rule=RULE_CRITICISM)
    return artifact.id


# --------------------------------------------------------------------- appellate

def apply_appeal(harness: Harness, ruling: AppellateRuling) -> str:
    """Ingest a committed appellate ruling as a precedent artifact (§3, Appellate).

    ``provenance.role = USER``, a ``mention`` ref to the standard it calibrates, and an
    **argumentative** warrant against whichever node it names — ``ν_bearing``,
    ``ν_soundness``, the standard, a register definition or a marker's ``difference_kind``
    set.  Argumentative warrants carry no commitment, so no trial transcript is demanded
    of a human.  Exactly two effects follow: pass 1 recomputes, and W2-PACKS ranks the
    precedent first.  Authority is pack ordering, never status privilege, and the ruling
    is itself attackable through its own validity node.
    """
    ruling.validated()
    if ruling.target not in harness.state.artifacts:
        raise GraphError(
            _APPEAL_TARGET_UNKNOWN, f"{ruling.target} is not registered in this graph")
    if ruling.standard_id and ruling.standard_id not in harness.state.artifacts:
        raise GraphError(
            _STANDARD_NOT_REGISTERED, f"{ruling.standard_id} is not registered")
    _appealable(harness, ruling)

    mention = ([Ref(target=ruling.standard_id, role="mention")]
               if ruling.standard_id else [])
    nu = _artifact(
        harness,
        {"schema": VALIDITY_SCHEMA, RECORD_FIELD: RECORD_VALIDITY_NODE,
         "aspect": "appellate", "ruling": ruling.ruling_id,
         "claim": f"appellate ruling {ruling.ruling_id} is a sound and relevant ground "
                  f"for reconsidering {ruling.target}"},
        role=ROLE_USER, interface=Interface(refs=mention), where="nu_appeal")
    _register(harness, [(nu, [])], rule=RULE_CRITICISM)

    warrant = Warrant(
        id=_warrant_id({"target": ruling.target, "validity_node": nu.id,
                        "ruling": ruling.ruling_id,
                        "type": WarrantType.ARGUMENTATIVE.value}),
        target=ruling.target,
        type=WarrantType.ARGUMENTATIVE,
        validity_node=nu.id,
    )
    body = {"schema": APPEAL_SCHEMA, RECORD_FIELD: RECORD_APPELLATE_RULING,
            "ruling": ruling.ruling_id, "target": ruling.target,
            "ground": ruling.ground,
            **({"standard": ruling.standard_id} if ruling.standard_id else {}),
            **dict(ruling.body)}
    artifact = _artifact(
        harness, body, role=ROLE_USER, interface=Interface(refs=mention),
        warrants=[warrant], where=f"appeal {ruling.ruling_id}")
    _register(harness, [(artifact, [warrant])], rule=RULE_CRITICISM)
    return artifact.id


def _appealable(harness: Harness, ruling: "AppellateRuling") -> None:
    """S1: refuse an appeal aimed at anything but a node the design names.

    ``ν_bearing`` / ``ν_soundness`` (both ``validity_node``), the standard body,
    and a prior appellate ruling.  A ruling aimed at a reading, a cell-open, an
    audit record or - the one that actually stopped a chain - the **material**
    is refused here, because an argumentative warrant onto a studied node is a
    ``p7`` loss and would stop the next decision with a ``protected_loss`` that
    named a ruling nobody meant as an attack on the evidence.

    The standard is admitted by identity: §3(a) registers its body with no
    ``record`` token, so a target equal to the ruling's own ``standard_id``, or
    to a registered standard artifact, is appealable.
    """

    target = ruling.target
    if ruling.standard_id and target == ruling.standard_id:
        return
    artifact = harness.state.artifacts.get(target)
    body = _decode(harness, artifact) if artifact is not None else None
    token = str(body.get(RECORD_FIELD, "")) if isinstance(body, Mapping) else ""
    if token in APPEALABLE_RECORDS:
        return
    if isinstance(body, Mapping) and body.get("schema") == STANDARD_BODY_SCHEMA:
        return
    raise GraphError(
        _APPEAL_TARGET_UNKNOWN,
        f"{target} carries record {token or '<none>'}; an appellate ruling may "
        f"name a validity node, the standard, or a prior ruling, and nothing "
        f"under study")


def appellate_rulings(harness: Harness) -> tuple[str, ...]:
    """Every precedent artifact on record, in registration order.

    W2-PACKS ranks these first in a judge pack and W3-REPORT states when there are none;
    the tuple is an ordering, never a standing.
    """
    return tuple(artifact_id for artifact_id, _ in _bodies(harness, APPEAL_SCHEMA))


# --------------------------------------------------------------------- read-back

def cell_standing(harness: Harness, key: "CellKey | str | Mapping[str, Any]") -> CellStanding:
    """Read one cell's current standing out of the adjudication, and out of nothing else.

    Which artifact is accepted — the reading or the unresolved default — is the whole
    answer, and every label here is the vendored two-pass adjudicator's.  The order of the
    branches is the order the calculus imposes: an unsupported cell first, because
    orphaned is not false; then the surviving rivals, because two of them are a problem
    and not an average; then the default.
    """
    cell = CellKey.coerce(key)
    index = _cell_index(harness)
    entry = index.get(cell.token)
    if entry is None:
        raise GraphError(_CELL_NOT_OPEN, f"{cell.token} has no unresolved default")
    default_id, _ = entry
    return _standing(harness, cell, default_id, _view(harness))


@dataclass(frozen=True)
class _View:
    """One walk of the graph, shared by every cell a caller asks about."""

    att: frozenset[tuple[str, str]]
    readings: Mapping[str, tuple[str, ...]]
    relations: Mapping[str, str]


def _view(harness: Harness) -> _View:
    readings: dict[str, list[str]] = {}
    relations: dict[str, str] = {}
    for artifact_id, body in _bodies(harness, READING_SCHEMA):
        key = body.get("key")
        if isinstance(key, str):
            readings.setdefault(key, []).append(artifact_id)
        relation = body.get("relation")
        if isinstance(relation, str):
            relations[artifact_id] = relation
    return _View(
        att=frozenset(tuple(edge) for edge in harness.state.att),
        readings={key: tuple(value) for key, value in readings.items()},
        relations=relations,
    )


def _standing(
    harness: Harness, cell: CellKey, default_id: str, view: _View
) -> CellStanding:
    default = harness.state.artifacts[default_id]
    default_status = _status(harness, default_id)
    standing = tuple(
        artifact_id for artifact_id in view.readings.get(cell.token, ())
        if (artifact_id, default_id) in view.att)
    accepted = tuple(a for a in standing if _status(harness, a) == Status.ACCEPTED.value)

    supports = [ref.target for ref in default.interface.refs if ref.role == "dependence"]
    orphaned = any(_status(harness, s) != Status.ACCEPTED.value for s in supports
                   if s in harness.state.artifacts)
    if orphaned:
        state = UNSUPPORTED
    elif accepted[1:]:
        # Two rivals is a PROBLEM, never a tally: the test is "is there a
        # second one", spelled as a slice so that nothing here counts
        # (wave-1 integration decision 49).
        state = CONTESTED
    elif accepted:
        state = READ
    elif default_status == Status.ACCEPTED.value:
        state = UNRESOLVED
    elif default_status == Status.SUSPENDED_UNSUPPORTED.value:
        state = UNSUPPORTED
    else:
        state = SUSPENDED

    relation: str | None = view.relations.get(accepted[0]) if state == READ else None
    return CellStanding(
        key=cell.token, state=state, default_id=default_id,
        default_status=default_status, standing=standing, accepted=accepted,
        relation=relation, register=cell.register)


def cell_state(harness: Harness, key: "CellKey | str | Mapping[str, Any]") -> str:
    """The cell's state token — a member of :data:`CELL_STATES`."""
    return cell_standing(harness, key).state


def cell_standings(harness: Harness) -> tuple[CellStanding, ...]:
    """Every opened cell's standing, in the order the defaults were registered."""
    view = _view(harness)
    return tuple(
        _standing(harness, CellKey.coerce(body), artifact_id, view)
        for artifact_id, body in _bodies(harness, CELL_OPEN_SCHEMA))


def mark_triples(harness: Harness) -> frozenset[tuple[str, str, str]]:
    """The ``(cell, register, mark)`` set the pre-registered decision rule compares.

    One triple per register cell, never one per cell: a mark is never combined across
    registers, and there is no key in this graph that could hold a combined one.  A cell
    standing at its unresolved default contributes its ``unresolved`` mark, because that
    *is* its standing; a contested or unsupported cell contributes none, so a cell that
    goes from unresolved to contested changes the set rather than hiding inside it.  The
    rule compares set identity, never a count.

    **The identity W2-DECIDE compares (wave-1 integration decision 4).**  Clause 4 of
    design §5 asks whether the mark set changed between two cycles.  *This function's
    return value, as it stands, is that set* - there is no second spelling of it, no
    normalisation step between here and the decision, and no per-cycle snapshot to
    reconcile.  Stated so that W2-DECIDE can be written against it without reading this
    module:

    * **Membership is by triple**, ``(cell, register, mark)``, with ``cell`` the cell
      key's ``cell`` segment and ``register`` its register segment - not the cell's
      one-line ``token``, so a comparison spelled over tokens is a different set.
    * **A cell at its unresolved default contributes** ``(cell, register,
      "unresolved")``.  The grounded default is a standing, not an absence, and a
      decision rule that dropped it could not tell "read as unresolved" from "not asked".
    * **A ``contested`` or ``unsupported`` cell contributes nothing.**  Two surviving
      rivals are a discrimination problem (§3) and an orphaned cell is not false, so
      neither has *a* mark; a move into either state therefore changes the set.
    * **A relation cell contributes nothing** - only register cells carry marks.
    * ``decide(prev, curr, ...)`` compares ``prev_triples != curr_triples`` and nothing
      else.  Set identity: no count of triples, no fraction that changed, no direction.
      "The set changed" is the whole reading, and which triples moved is the record.
    """
    triples: set[tuple[str, str, str]] = set()
    for standing in cell_standings(harness):
        if standing.register is None:
            continue
        cell = CellKey.coerce(standing.key)
        if standing.state == READ and standing.relation:
            triples.add((cell.cell, cell.register, standing.relation))
        elif standing.state == UNRESOLVED:
            triples.add((cell.cell, cell.register, UNRESOLVED_TOKEN))
    return frozenset(triples)


def produced(harness: Harness, *, since_seq: int = 0) -> Production:
    """The artifact ids registered at or after ``since_seq`` (ProducedBy discharge).

    W1-OBLIGATIONS asks whether an obligation was satisfied by artifacts *this cycle*
    produced; this is the set it intersects.  ``upto_seq`` is what to pass back as
    ``since_seq`` next cycle.
    """
    ids: set[str] = set()
    upto = since_seq
    for event in harness.log.read():
        upto = max(upto, event.seq + 1)
        if event.seq < since_seq:
            continue
        ids.update(output for output in event.outputs if output in harness.state.artifacts)
    return Production(artifact_ids=frozenset(ids), upto_seq=upto)
