"""O and P: the pre-registered obligations, their program checks, and ProducedBy.

Purpose
-------
``obligations.json`` names two fixed sets of obligations - **O**, the failed
obligations this chain exists to discharge, and **P**, the protected
obligations that must not be lost - and, for each, a *named program predicate*
over the registered graph. This module loads and validates that file, pins it,
evaluates every obligation at a situation, attributes a newly satisfied
obligation to the cycle that produced it (``ProducedBy``), and computes the
``losses_outside_P`` register that is written every cycle, present even when
empty.

It decides nothing. Exactly one outcome per cycle is W2-DECIDE's program; this
module supplies the readings that program quantifies over.

Design of record
----------------
Section 5, "The decision rule - pre-registered, and not a scalar meter", and
its FW5 sources: FW5:787 (O and P are fixed for the comparison and may not
shift inside its assessment), FW5:791-797 (the repair condition (P)), FW5:800
(``ProducedBy`` is a construction account and "is not satisfied by temporal
succession alone"; a transport supplies the interpretation of *o* and *r*
across changed representations), FW5:802 ("Losses outside P must be exposed"),
FW5:810 (a cycle may be net withdrawal and still be progress), FW5:814 ("An
endorsement count or an ungrounded satisfaction report is not such an
obligation"), and FW5 R5 as section 4.4 states it: non-evaluability is not
refutation.

The one hard rule, enforced by test
-----------------------------------
**No predicate and no evaluation function in this module takes a count, a
rate, a threshold or a score as an input, and none returns one as its
verdict.** A verdict is one of three tokens. The module contains no arithmetic
operator, no ``len``/``sum``/``min``/``max``, and no numeric literal outside a
subscript; ``tests/loop/test_obligations.py`` asserts all of that over this
file's own syntax tree, and asserts that every registered predicate has the
signature ``(situation: Situation) -> Check``. Uniqueness of a citation is
expressed as "the quote occurs, and does not occur again in the remainder" -
a uniqueness predicate, not a quantity compared with a threshold. Coverage of
a declared key set is set containment, never a tally. The audit obligation
asks whether a registered audit record *declares that it covers the cycle
under evaluation*; the ``audit.period`` cadence that decides when a new record
is minted is the driver's declared attention-and-spend parameter and never
reaches a predicate.

The three verdicts, and why the third is not failure
----------------------------------------------------
``satisfied`` / ``not_satisfied`` / ``not_evaluable``. A predicate answers
``not_evaluable`` when the material it must read is not in the situation at
all - the renderer has not run, no audit exists to compare against, the
run has not declared the forbidden-key vocabulary. That verdict is never a
failure: it never makes a protected loss, it is never reported under a failure
name, and it never satisfies "all *o* satisfied". It is *not* used for a
prohibition whose vocabulary this module owns (``appellate_remains_optional``
holds vacuously and is satisfied), nor for an obligation whose whole subject
matter is the run's own artifacts (``audit_in_force`` on a graph carrying no
audit at all is **not satisfied** - that is precisely its state at the opening
situation, and what a later cycle discharges).

For O, an obligation "failed at xi" is any obligation not satisfied there,
whether it read ``not_satisfied`` or ``not_evaluable``: FW5's clause is the
negation ``not o(xi)``, and a cycle that first makes an obligation *readable*
and then satisfies it has produced the change. The two are kept apart in the
record so no reader can mistake the instrument declining to read for a finding
about the material.

For P, a loss requires ``satisfied`` at xi and ``not_satisfied`` at xi'.
A protected obligation that becomes unreadable is exposed as
``protected_not_evaluable`` and is never a ``protected_loss``.

ProducedBy, in two conjuncts
----------------------------
``produced_by(situation, obligation_id)`` returns the artifacts of the cycle
under evaluation that made the obligation hold, and it is empty unless both:

1. *attribution* - the evidence the predicate returned includes at least one
   artifact named by this cycle's own registration record
   (``Situation.registered``), and
2. *dependence* - withholding this cycle's registrations from the situation
   makes the obligation stop holding.

Conjunct 2 is what separates a construction account from temporal succession:
an obligation that already held without this cycle's contribution is not
discharged by it, however recently the artifacts appeared.

Deviations from the design of record and from the wave-plan entry
-----------------------------------------------------------------
1. **The pin is the file's byte sha256**, not the document's structure digest.
   The wave-plan acceptance clause is "the pin changes on any byte change",
   and ``custody.pins`` hashes file bytes, so ``pin()`` agrees with what
   ``loop_plan_id`` will fold. The structure digest a bundle declares about
   itself (``obligations_sha256``) is *verified* at load and exposed as
   ``Obligations.structure_digest``; a bundle whose self-declaration does not
   reproduce is refused with ``OBLIGATIONS_DIGEST_MISMATCH``.

   REVIEW-PREREG **PR-02** found that the published pre-registration names the
   *canonical-body* digest while the plan folds the *file* digest, so a reader
   checking one against the other finds a mismatch and cannot tell whether the
   document shifted. The ruling, applied here: **the file digest stays the one
   the identity carries** - it is the only one a custody check can re-derive
   from the tree - and the canonical-body digest is given a name of its own,
   :func:`canonical_pin`, so that neither value is anonymous. The bundle must
   publish both and say which enters ``loop_plan_id``; that half is the
   bundle's, and is recorded for its reviser in ``WAVE2-INTERFACE.md``.
2. **``losses_outside_p(prev, curr)`` takes situations, not evaluations.**
   W2-DECIDE's ``decide(prev, curr, ...)`` holds two situations, and a loss
   register needs both the obligations' verdicts and the artifacts' standing.
   ``prev`` may be ``None`` before cycle 1; the return is then a list that is
   present and empty.
3. **``protected_losses(prev, curr)`` is added.** Clause 1 of section 5 needs
   the P side of the same comparison, and "losses outside P" cannot by its
   name carry it.
4. **A situation carries its obligations.** FW5:787 fixes O and P for the
   assessment, so ``evaluate`` refuses a situation pinned to a different
   document (``OBLIGATIONS_PIN_SHIFTED``), and ``produced_by(situation, id)``
   can resolve the predicate from its two arguments.
5. **Withholding restricts the view; it does not re-adjudicate.**
   ``Situation.without`` drops nodes and the edges touching them and leaves
   the remaining statuses as the harness computed them. A caller that wants
   the stronger counterfactual can build the prior situation from
   ``Harness.at(seq)`` and compare.
6. **Every vocabulary a predicate needs comes from the situation**, not from a
   constant here - the declared key set, the register set, the forbidden and
   aggregate key lists, the studied node set, the ceiling's sentences. The two
   exceptions are ``types.BLOCK_CODES`` (W0-TYPES is this module's declared
   dependency and owns the closed block vocabulary) and the small token sets
   below, which are this module's own reading vocabulary.
7. **File-tree obligations enter through the graph.** Several pre-registered
   checks are about the run tree (nothing published is written; no scoring key
   in any rendered file). A predicate here reads the graph, so the driver
   registers its finding as a record artifact - ``observed_digests``,
   ``rendered_files`` - and the predicate compares it with the pinned
   declaration. Until it does, those obligations read ``not_evaluable``, which
   is never a failure.
8. **``standard.UNRESOLVED_TOKEN`` is mirrored, not imported.** W0-STANDARD is
   not in this module's ``depends_on``; ``UNRESOLVED_RELATION`` below carries
   the same token and a test in W2 or the integrator may assert identity.
9. **The registry carries the first live run's own check names.** The
   pre-registration bundle for ``L001`` declares nineteen obligations - seven
   in O, twelve in P - and names each check ``obligations.<name>``. Those
   names are the registry's names, so that document loads unamended; the
   programs behind them are this module's, and the ``obligations.`` prefix is
   the module's own namespace, stripped at load.
10. **o5 does not take ``audit.period``.** The bundle's prose states o5 as a
    recency comparison, ``current_cycle - n < audit.period``. That is a
    threshold, and a threshold may not enter a predicate here, so
    ``audit_in_force`` asks instead whether a registered audit record
    *declares that it covers the cycle under evaluation*. The cadence that
    decides when a new record is minted, and which cycles it covers, is the
    driver's; the obligation reads the declaration. On a graph carrying no
    audit at all the verdict is ``not_satisfied``, which is the bundle's own
    reading of o5 at the opening situation. **The bundle's o5 sentence must be
    reworded at its pre-registration review** to state the membership test
    rather than the recency comparison (wave-1 integration decision 5): o5 is
    "the cycle under evaluation is in some registered audit record's declared
    coverage", never ``current_cycle - n < audit.period``. A threshold inside a
    predicate is the thing this module's one hard rule forbids, and the
    cadence that mints records is the driver's declared attention-and-spend
    parameter, which is pinned in the config and reported, not read here.
11. **p7 is refined, not relaxed** (wave-1 integration decision 1). "No att
    *or dep* edge lands on a node under study" cannot hold beside W1-GRAPH's
    acceptance clause that refuting ``E_row`` must leave a reading
    ``suspended_unsupported``, which requires exactly a ``dep`` edge onto
    ``E_row``. ``no_edges_on_studied_nodes`` therefore asks two questions: no
    ``att`` edge may target a studied node, and no studied node may be the
    *source* of any edge. A ``dep`` from a reading to the material it reads is
    permitted, and is what makes a refuted material orphan the reading rather
    than refute it. The bundle's p7 sentence is to be reworded to this at the
    pre-registration review; the protection is not weakened, because the two
    directions that could hide a change to the material are both refused.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping, Sequence

from deepreason_core.canonical import canonical_json, sha256_hex

from minireason.loop.types import BLOCK_CODES, BLOCK_CODE_PREFIX, LoopError

__all__ = [
    # vocabulary
    "OBLIGATIONS_SCHEMA",
    "MEMBERSHIPS",
    "FAILED_SET",
    "PROTECTED_SET",
    "RECORD_FIELD",
    "RECORD_KINDS",
    "READING_KINDS",
    "DISPOSITION_REASONS",
    "CELL_STATES",
    "DECLARED_SIDES",
    "UNRESOLVED_RELATION",
    "APPELLATE_TOKENS",
    "NEW_CODES",
    # errors
    "ObligationsError",
    # records
    "Verdict",
    "Check",
    "Node",
    "Situation",
    "Obligation",
    "Obligations",
    "Loss",
    "Evaluation",
    # the registry
    "PREDICATES",
    "PREDICATE_QUESTIONS",
    "PREDICATE_READS",
    "predicate",
    # the interface
    "load_obligations",
    "pin",
    "canonical_pin",
    "evaluate",
    "produced_by",
    "production_of",
    "Production",
    "losses_outside_p",
    "protected_losses",
]


# --------------------------------------------------------------------------
# New stable codes (the integrator folds these into types.FAILURE_CODES)
# --------------------------------------------------------------------------

#: code -> the one-line reason it exists. Every one is UPPER_SNAKE_CASE and
#: belongs to ``types.FAILURE_CODES``; none is a semantic result.
NEW_CODES: Mapping[str, str] = MappingProxyType({
    "OBLIGATIONS_FILE_MISSING":
        "the pre-registered obligations file named by the config is not there",
    "OBLIGATIONS_MALFORMED":
        "the obligations file is not readable as JSON",
    "OBLIGATIONS_NOT_A_MAPPING":
        "the obligations document is not a JSON object",
    "OBLIGATIONS_SCHEMA_UNKNOWN":
        "the document declares a schema this loader does not implement",
    "OBLIGATIONS_UNKNOWN_KEY":
        "a top-level key outside the declared set would be pinned but never read",
    "OBLIGATIONS_MISSING_KEY":
        "the document omits a required top-level key",
    "OBLIGATIONS_DIGEST_MISMATCH":
        "the document's own obligations_sha256 does not reproduce from its content",
    "OBLIGATIONS_PIN_SHIFTED":
        "O and P may not shift inside an assessment (FW5:787)",
    "OBLIGATION_FIELD_MISSING":
        "an obligation entry omits id, set, statement or check",
    "OBLIGATION_FIELD_INVALID":
        "an obligation field is the wrong shape or is empty",
    "OBLIGATION_ID_MALFORMED":
        "an obligation id is not a short lower-case token",
    "OBLIGATION_ID_DUPLICATE":
        "two obligation entries share one id",
    "OBLIGATION_IN_BOTH_SETS":
        "an obligation is declared in O and in P; membership is exclusive",
    "OBLIGATION_MEMBERSHIP_UNKNOWN":
        "an obligation declares a set other than O or P",
    "OBLIGATION_CHECK_UNKNOWN":
        "an obligation names a program predicate this registry does not carry",
    "OBLIGATION_UNKNOWN":
        "an obligation id was asked for that the pinned document does not declare",
    "PREDICATE_CONTRACT_VIOLATED":
        "a registered predicate returned something other than a Check",
    "SITUATION_INVALID":
        "a situation was built without the fields every predicate reads",
})


# --------------------------------------------------------------------------
# The document's vocabulary
# --------------------------------------------------------------------------

#: The one document schema this loader implements.
OBLIGATIONS_SCHEMA = "minireason.loop.obligations.v1"

#: O - the failed obligations the chain exists to discharge.
FAILED_SET = "O"
#: P - the protected obligations, preserved or the chain stops.
PROTECTED_SET = "P"
#: Membership is exclusive: an obligation is in exactly one of them.
MEMBERSHIPS: tuple[str, str] = (FAILED_SET, PROTECTED_SET)

#: Required top-level keys.
REQUIRED_KEYS: tuple[str, ...] = ("schema", "obligations")
#: Optional top-level keys, carried verbatim on ``Obligations.preamble``. They
#: are prose for the operator and for the ledger, and no predicate reads them.
OPTIONAL_KEYS: tuple[str, ...] = (
    "run_id",
    "loop_design_section",
    "fixed_before_first_look",
    "material",
    "repair_condition",
    "no_clause_is_a_count",
    "transport",
    "notes",
)
#: The two self-describing digest keys, excluded from the structure digest.
DIGEST_KEYS: tuple[str, str] = ("obligations_sha256", "obligations_sha256_recipe")

#: Required keys of one obligation entry.
OBLIGATION_KEYS: tuple[str, ...] = ("id", "set", "statement", "check")
#: Optional keys of one obligation entry, carried verbatim.
OBLIGATION_OPTIONAL_KEYS: tuple[str, ...] = ("why_not_a_count",)
#: Keys of the ``check`` mapping. ``predicate`` names the program; ``artifact``
#: names where the material lives, for the operator and the driver; ``detail``
#: is the prose account of how the program reads it.
CHECK_KEYS: tuple[str, ...] = ("predicate", "artifact", "detail")

#: A pre-registration may spell a predicate ``obligations.<name>``; the prefix
#: names this module and is stripped before the registry is consulted.
PREDICATE_NAMESPACE = "obligations"

_ID = re.compile(r"[a-z][a-z0-9_]{0,63}\Z")


# --------------------------------------------------------------------------
# The graph's record vocabulary - what the predicates read
# --------------------------------------------------------------------------

#: The field every loop artifact's JSON content carries to say what it is.
RECORD_FIELD = "record"

READING_SET = "reading_set"
READING_ROW = "reading_row"
CELL_MARK = "cell_mark"
CELL_OPEN = "cell_open"
DISPOSITION = "disposition"
AUDIT_RECORD = "audit_record"
BASELINE = "baseline"
CALL_RECORD = "call_record"
RENDERED_STATES = "rendered_states"
RENDERED_FILES = "rendered_files"
MATERIAL = "material"
RECODING_TABLE = "recoding_table"
CASE_REQUEST = "case_request"
FORBIDDEN_KEYS = "forbidden_keys"
AGGREGATE_KEYS = "aggregate_keys"
STUDY_SET = "study_set"
PUBLISHED_UNRESOLVED = "published_unresolved"
PINNED_DIGESTS = "pinned_digests"
OBSERVED_DIGESTS = "observed_digests"
CEILING = "ceiling"

#: Every record kind a predicate here reads. W1-GRAPH and W5-DRIVER write
#: them; a kind absent from a situation makes its predicates not_evaluable.
RECORD_KINDS: tuple[str, ...] = (
    AUDIT_RECORD, BASELINE, CALL_RECORD, CASE_REQUEST, CEILING, CELL_MARK,
    CELL_OPEN, DISPOSITION, FORBIDDEN_KEYS, AGGREGATE_KEYS, MATERIAL,
    OBSERVED_DIGESTS, PINNED_DIGESTS, PUBLISHED_UNRESOLVED, READING_ROW,
    READING_SET, RECODING_TABLE, RENDERED_FILES, RENDERED_STATES, STUDY_SET,
)

#: The two record kinds that are readings of the material.
READING_KINDS: tuple[str, str] = (READING_ROW, CELL_MARK)

#: Mirrors ``standard.UNRESOLVED_TOKEN`` (deviation 8).
UNRESOLVED_RELATION = "unresolved"

#: Mirrors ``surface.DECLARED_SIDES``: the three regions G3 calls operative -
#: the referring record, the target record and a listed body passage. A quote
#: that resolved on ``surface.SIDE_FRAMING`` resolved inside the pack's own
#: scaffolding, which is not a reading of the material, so o3 refuses it. This
#: module imports no sibling of the package but ``types``, so the tuple is
#: mirrored here and ``tests/loop/test_obligations.py`` asserts the mirror.
DECLARED_SIDES: tuple[str, ...] = (
    "referring_record", "target_record", "referring_body_passage")

#: The non-block reasons a disposition record may carry, from the
#: pre-registration's own closed sets for o1 and o2. A reason spelled
#: ``blocked:<name>`` is checked against ``types.BLOCK_CODES`` instead.
DISPOSITION_REASONS: frozenset[str] = frozenset({
    "critic-none",
    "unresolved:outside-vocabulary",
    "NOT_DISPATCHED",
    "INDETERMINATE",
    "unreached",
    "program-computed",
    "baseline-forced-same",
    "under-replicated",
    "bare-token-ambiguity",
    "byte-identity-defeater",
})

#: The four printed states of a declared cell, kept apart so that unread and
#: machine-unresolved are never collapsed into unresolved-by-inquiry.
CELL_STATES: tuple[str, ...] = ("read", "unresolved", "machine-unresolved", "unread")

#: What a record may not declare itself blocked on: the appellate is optional.
APPELLATE_TOKENS: frozenset[str] = frozenset({"appeal", "appellate", "appellate_ruling"})

#: The adjudicated label an artifact must carry to stand as evidence.
STANDING = "accepted"

_INLINE_PREFIX = "inline:"


# --------------------------------------------------------------------------
# Error
# --------------------------------------------------------------------------


class ObligationsError(LoopError):
    """A refusal of this module, carrying a stable code from :data:`NEW_CODES`."""

    def __init__(self, token: str, detail: str = ""):
        super().__init__(token, detail)


def _refuse(token: str, detail: str) -> ObligationsError:
    return ObligationsError(token, detail)


# --------------------------------------------------------------------------
# Verdicts and checks
# --------------------------------------------------------------------------


class Verdict(str, Enum):
    """The only three answers a program check may give.

    There is no fourth, no order on these three, and no numeric shadow of
    them: a verdict is a token, never a quantity (FW5:814).
    """

    SATISFIED = "satisfied"
    NOT_SATISFIED = "not_satisfied"
    NOT_EVALUABLE = "not_evaluable"


@dataclass(frozen=True)
class Check:
    """One predicate's answer: a verdict, the artifacts that witness it, prose."""

    verdict: Verdict
    evidence: tuple[str, ...] = ()
    detail: str = ""

    @classmethod
    def satisfied(cls, evidence: Iterable[str] = (), detail: str = "") -> "Check":
        return cls(Verdict.SATISFIED, _ids(evidence), detail)

    @classmethod
    def not_satisfied(cls, evidence: Iterable[str] = (), detail: str = "") -> "Check":
        return cls(Verdict.NOT_SATISFIED, _ids(evidence), detail)

    @classmethod
    def not_evaluable(cls, evidence: Iterable[str] = (), detail: str = "") -> "Check":
        return cls(Verdict.NOT_EVALUABLE, _ids(evidence), detail)

    @property
    def holds(self) -> bool:
        return self.verdict is Verdict.SATISFIED

    def as_dict(self) -> dict[str, Any]:
        return {
            "verdict": self.verdict.value,
            "evidence": list(self.evidence),
            "detail": self.detail,
        }


def _ids(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({str(value) for value in values}))


#: A program check: one situation in, one Check out. Nothing else.
Predicate = Callable[["Situation"], Check]


# --------------------------------------------------------------------------
# The situation the predicates read
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Node:
    """One registered artifact, as an obligation reads it."""

    id: str
    status: str
    role: str
    record: Mapping[str, Any] = field(default_factory=dict)
    text: str = ""

    @property
    def kind(self) -> str:
        value = self.record.get(RECORD_FIELD, "")
        return value if isinstance(value, str) else ""

    @property
    def stands(self) -> bool:
        """Accepted by the two-pass adjudication: it may bear evidence."""
        return self.status == STANDING


@dataclass(frozen=True)
class Situation:
    """A cycle-end reading of the graph, under one pinned obligations document.

    ``registered`` is the cycle's own registration record - the artifact ids
    this cycle put into the graph. It is empty by default, and an empty
    registration record discharges nothing.
    """

    cycle: int
    obligations: "Obligations"
    nodes: Mapping[str, Node] = field(default_factory=dict)
    attacks: frozenset[tuple[str, str]] = frozenset()
    supports: frozenset[tuple[str, str]] = frozenset()
    registered: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not isinstance(self.obligations, Obligations):
            raise _refuse("SITUATION_INVALID", "a situation carries its pinned obligations")
        object.__setattr__(self, "nodes", MappingProxyType(dict(self.nodes)))
        object.__setattr__(self, "attacks", frozenset(self.attacks))
        object.__setattr__(self, "supports", frozenset(self.supports))
        object.__setattr__(self, "registered", frozenset(self.registered))

    @property
    def cycle_token(self) -> str:
        return str(self.cycle)

    @classmethod
    def from_harness(
        cls,
        harness: Any,
        *,
        cycle: int,
        obligations: "Obligations",
        registered: Iterable[str] = (),
    ) -> "Situation":
        """Read a ``deepreason_core`` harness into a situation.

        Statuses are the two-pass adjudication's own labels; content is the
        artifact's bytes decoded as JSON where it is JSON, and left as text
        where it is not. Nothing is written.
        """

        state = harness.state
        nodes: dict[str, Node] = {}
        for artifact_id, artifact in state.artifacts.items():
            status = state.status.get(artifact_id)
            nodes[artifact_id] = _read_node(harness, artifact_id, artifact, status)
        return cls(
            cycle=cycle,
            obligations=obligations,
            nodes=nodes,
            attacks=frozenset((source, target) for source, target in state.att),
            supports=frozenset((source, target) for source, target in state.dep),
            registered=frozenset(str(value) for value in registered),
        )

    def without(self, ids: Iterable[str]) -> "Situation":
        """The same situation with those artifacts withheld (deviation 5)."""

        withheld = frozenset(str(value) for value in ids)
        kept = {
            node_id: node for node_id, node in self.nodes.items()
            if node_id not in withheld
        }
        return Situation(
            cycle=self.cycle,
            obligations=self.obligations,
            nodes=kept,
            attacks=frozenset(
                edge for edge in self.attacks
                if edge[0] not in withheld and edge[1] not in withheld
            ),
            supports=frozenset(
                edge for edge in self.supports
                if edge[0] not in withheld and edge[1] not in withheld
            ),
            registered=self.registered.difference(withheld),
        )

    def records(self, kind: str) -> tuple[Node, ...]:
        """Every registered record of that kind, standing or not."""
        return tuple(
            node for node in self.nodes.values() if node.kind == kind
        )

    def standing(self, kind: str) -> tuple[Node, ...]:
        """Every accepted record of that kind: the ones that may bear evidence."""
        return tuple(node for node in self.records(kind) if node.stands)

    def one(self, kind: str) -> Node | None:
        """The accepted record of a kind declared at most once, or None."""
        for node in self.standing(kind):
            return node
        return None


def _read_node(harness: Any, artifact_id: str, artifact: Any, status: Any) -> Node:
    raw = _content_bytes(harness, artifact)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = ""
    record: Mapping[str, Any] = {}
    if text:
        try:
            loaded = json.loads(text)
        except ValueError:
            loaded = None
        if isinstance(loaded, dict):
            record = loaded
    provenance = getattr(artifact, "provenance", None)
    role = getattr(provenance, "role", "")
    return Node(
        id=artifact_id,
        status=str(getattr(status, "value", status or "")),
        role=str(getattr(role, "value", role or "")),
        record=MappingProxyType(dict(record)),
        text=text,
    )


def _content_bytes(harness: Any, artifact: Any) -> bytes:
    ref = str(getattr(artifact, "content_ref", ""))
    if ref.startswith(_INLINE_PREFIX):
        _, _, inline = ref.partition(_INLINE_PREFIX)
        return inline.encode("utf-8")
    try:
        raw = harness.blobs.get(ref)
    except (KeyError, OSError, ValueError):
        return b""
    return raw if isinstance(raw, bytes) else str(raw).encode("utf-8")


# --------------------------------------------------------------------------
# The document
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Obligation:
    """One pre-registered obligation: prose, a membership, a named program."""

    id: str
    membership: str
    statement: str
    check: str
    reads: tuple[str, ...] = ()
    detail: str = ""
    why: str = ""

    @property
    def is_protected(self) -> bool:
        return self.membership == PROTECTED_SET

    @property
    def predicate(self) -> Predicate:
        return predicate(self.check)

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "set": self.membership,
            "statement": self.statement,
            "check": self.check,
            "reads": list(self.reads),
            "detail": self.detail,
            "why": self.why,
        }


@dataclass(frozen=True)
class Obligations:
    """The pinned document: O, P, the bytes it was read from, its prose."""

    entries: tuple[Obligation, ...]
    source_bytes: bytes = b""
    path: Path | None = None
    preamble: Mapping[str, Any] = field(default_factory=dict)
    structure_digest: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "preamble", MappingProxyType(dict(self.preamble)))

    @property
    def failed(self) -> tuple[Obligation, ...]:
        """O, in the document's own order."""
        return tuple(o for o in self.entries if o.membership == FAILED_SET)

    @property
    def protected(self) -> tuple[Obligation, ...]:
        """P, in the document's own order."""
        return tuple(o for o in self.entries if o.membership == PROTECTED_SET)

    @property
    def ids(self) -> tuple[str, ...]:
        return tuple(o.id for o in self.entries)

    def by_id(self, obligation_id: str) -> Obligation:
        for entry in self.entries:
            if entry.id == obligation_id:
                return entry
        raise _refuse("OBLIGATION_UNKNOWN", f"no obligation {obligation_id!r} is declared")

    @property
    def pin(self) -> str:
        """The sha256 of the bytes this document was read from."""
        return hashlib.sha256(self.source_bytes).hexdigest()

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": OBLIGATIONS_SCHEMA,
            "pin": self.pin,
            "structure_digest": self.structure_digest,
            "obligations": [entry.as_dict() for entry in self.entries],
        }


def pin(obligations: Obligations) -> str:
    """The pin folded into ``loop_plan_id``: the file's sha256 (deviation 1).

    **This is the one the plan identity carries** (REVIEW-PREREG PR-02). It is
    the digest of the bytes on disk, so it is what ``custody.pins`` computes for
    that path, what ``custody.verify_pins`` re-derives from the tree, and what a
    reader with the file and nothing else can reproduce. The canonical-body
    digest is :func:`canonical_pin`, and the two are different values over one
    document: the bundle publishes both and says which is which.
    """

    if not isinstance(obligations, Obligations):
        raise _refuse("SITUATION_INVALID", "pin() takes a loaded Obligations")
    return obligations.pin


def canonical_pin(obligations: Obligations) -> str:
    """The document's canonical-body digest, verified at load (PR-02).

    Canonical JSON over the document with the two digest keys removed - the
    recipe a bundle declares about itself in ``obligations_sha256``, and the
    value the pre-registration prose publishes. It is **not** folded into
    ``loop_plan_id``: whitespace and key order are not part of it, so it cannot
    answer "did these bytes move", which is what a custody pin is for.

    Both are exposed so that neither is unnamed. The ruling the review asked for
    is: ``loop_plan_id`` carries :func:`pin`; the pre-registration text must
    state both values and say which enters the identity. A record that names one
    digest and folds the other leaves a later reader unable to tell whether the
    document shifted, which is exactly what FW5:787 is served by.
    """

    if not isinstance(obligations, Obligations):
        raise _refuse("SITUATION_INVALID", "canonical_pin() takes a loaded Obligations")
    return obligations.structure_digest


def load_obligations(path: Path | str) -> Obligations:
    """Read, validate and pin ``obligations.json``.

    Every refusal names one code and one place. The document's own
    ``obligations_sha256``, where present, is recomputed from its content and
    must reproduce.
    """

    source = Path(path)
    try:
        raw = source.read_bytes()
    except FileNotFoundError as error:
        raise _refuse("OBLIGATIONS_FILE_MISSING", str(source)) from error
    return obligations_from_bytes(raw, path=source)


def obligations_from_bytes(raw: bytes, *, path: Path | None = None) -> Obligations:
    """The loader's body, on bytes, so a document can be pinned without a file."""

    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as error:
        raise _refuse("OBLIGATIONS_MALFORMED", str(error)) from error
    if not isinstance(document, dict):
        raise _refuse("OBLIGATIONS_NOT_A_MAPPING", "the document must be a JSON object")

    declared = set(REQUIRED_KEYS).union(OPTIONAL_KEYS).union(DIGEST_KEYS)
    for key in sorted(document):
        if key not in declared:
            raise _refuse("OBLIGATIONS_UNKNOWN_KEY", f"top-level key {key!r}")
    for key in REQUIRED_KEYS:
        if key not in document:
            raise _refuse("OBLIGATIONS_MISSING_KEY", f"top-level key {key!r}")
    if document["schema"] != OBLIGATIONS_SCHEMA:
        raise _refuse("OBLIGATIONS_SCHEMA_UNKNOWN", str(document["schema"]))

    listed = document["obligations"]
    if not isinstance(listed, list):
        raise _refuse("OBLIGATION_FIELD_INVALID", "obligations must be a list")

    entries: list[Obligation] = []
    seen: dict[str, str] = {}
    for raw_entry in listed:
        entry = _obligation_from(raw_entry)
        prior = seen.get(entry.id)
        if prior is not None:
            if prior != entry.membership:
                raise _refuse("OBLIGATION_IN_BOTH_SETS", f"obligation {entry.id!r}")
            raise _refuse("OBLIGATION_ID_DUPLICATE", f"obligation {entry.id!r}")
        seen[entry.id] = entry.membership
        entries.append(entry)

    structure = _structure_digest(document)
    declared_digest = document.get(DIGEST_KEYS[0])
    if declared_digest is not None and declared_digest != structure:
        raise _refuse(
            "OBLIGATIONS_DIGEST_MISMATCH",
            f"declared {declared_digest!r}, recomputed {structure!r}",
        )
    preamble = {
        key: value for key, value in document.items()
        if key in set(OPTIONAL_KEYS).union(DIGEST_KEYS)
    }
    return Obligations(
        entries=tuple(entries),
        source_bytes=raw,
        path=path,
        preamble=preamble,
        structure_digest=structure,
    )


def _structure_digest(document: Mapping[str, Any]) -> str:
    """The recipe a bundle declares: canonical JSON without the digest keys."""

    body = {key: value for key, value in document.items() if key not in DIGEST_KEYS}
    return sha256_hex(canonical_json(body))


def _obligation_from(raw_entry: Any) -> Obligation:
    if not isinstance(raw_entry, dict):
        raise _refuse("OBLIGATION_FIELD_INVALID", "an obligation entry must be an object")
    allowed = set(OBLIGATION_KEYS).union(OBLIGATION_OPTIONAL_KEYS)
    for key in sorted(raw_entry):
        if key not in allowed:
            raise _refuse("OBLIGATION_FIELD_INVALID", f"unknown obligation key {key!r}")
    for key in OBLIGATION_KEYS:
        if key not in raw_entry:
            raise _refuse("OBLIGATION_FIELD_MISSING", f"obligation key {key!r}")

    identifier = raw_entry["id"]
    if not isinstance(identifier, str) or _ID.fullmatch(identifier) is None:
        raise _refuse("OBLIGATION_ID_MALFORMED", repr(identifier))
    membership = raw_entry["set"]
    if membership not in MEMBERSHIPS:
        raise _refuse("OBLIGATION_MEMBERSHIP_UNKNOWN", f"{identifier}: {membership!r}")
    statement = raw_entry["statement"]
    if not isinstance(statement, str) or not statement.strip():
        raise _refuse("OBLIGATION_FIELD_INVALID", f"{identifier}: statement is empty")

    name, reads, detail = _check_from(identifier, raw_entry["check"])
    if name not in PREDICATES:
        raise _refuse("OBLIGATION_CHECK_UNKNOWN", f"{identifier}: {name!r}")
    why = raw_entry.get(OBLIGATION_OPTIONAL_KEYS[0], "")
    if not isinstance(why, str):
        raise _refuse("OBLIGATION_FIELD_INVALID", f"{identifier}: {OBLIGATION_OPTIONAL_KEYS[0]}")
    return Obligation(
        id=identifier,
        membership=membership,
        statement=statement,
        check=name,
        reads=reads,
        detail=detail,
        why=why,
    )


def _check_from(identifier: str, raw_check: Any) -> tuple[str, tuple[str, ...], str]:
    """``check`` is a predicate name, or a mapping naming one and its material."""

    if isinstance(raw_check, str):
        return _predicate_name(identifier, raw_check), (), ""
    if not isinstance(raw_check, dict):
        raise _refuse("OBLIGATION_FIELD_INVALID", f"{identifier}: check")
    for key in sorted(raw_check):
        if key not in CHECK_KEYS:
            raise _refuse("OBLIGATION_FIELD_INVALID", f"{identifier}: check key {key!r}")
    if CHECK_KEYS[0] not in raw_check:
        raise _refuse("OBLIGATION_FIELD_MISSING", f"{identifier}: check.{CHECK_KEYS[0]}")
    reads = raw_check.get(CHECK_KEYS[1], ())
    if isinstance(reads, str):
        reads = (reads,)
    if not isinstance(reads, (list, tuple)) or not all(
        isinstance(value, str) for value in reads
    ):
        raise _refuse("OBLIGATION_FIELD_INVALID", f"{identifier}: check.{CHECK_KEYS[1]}")
    detail = raw_check.get(CHECK_KEYS[2], "")
    if not isinstance(detail, str):
        raise _refuse("OBLIGATION_FIELD_INVALID", f"{identifier}: check.{CHECK_KEYS[2]}")
    return _predicate_name(identifier, raw_check[CHECK_KEYS[0]]), tuple(reads), detail


def _predicate_name(identifier: str, raw_name: Any) -> str:
    if not isinstance(raw_name, str) or not raw_name.strip():
        raise _refuse("OBLIGATION_FIELD_INVALID", f"{identifier}: check.predicate")
    head, marker, tail = raw_name.partition(".")
    if marker and head == PREDICATE_NAMESPACE:
        return tail
    return raw_name


# --------------------------------------------------------------------------
# Helpers the predicates share. None of them counts anything.
# --------------------------------------------------------------------------


def _field(node: Node, name: str) -> Any:
    return node.record.get(name)


def _string(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _listed(value: Any) -> tuple[Any, ...]:
    return tuple(value) if isinstance(value, (list, tuple)) else ()


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, dict) else {}


def _resolves_uniquely(text: str, quote: str) -> bool:
    """G2/G3 as a uniqueness predicate: **exactly one start offset**.

    Expressed as "it starts here, and it starts nowhere after here" rather than
    as a tally, so no quantity is computed and nothing is compared with a
    threshold.

    The earlier spelling used ``str.partition`` and then asked whether the quote
    appeared in the *tail after the match*, which reads ``aa`` as unique in
    ``aaa``: the second occurrence starts inside the first and is not in the
    tail at all (REVIEW-WAVE1 S3). ``str.find`` from one character past the
    first start finds the overlapping occurrence, which is what G2's
    "``M.count(q) == 1``" means and what W2-PACKS' ``Exchange.count`` already
    counts. The two now agree.
    """

    if not text or not quote:
        return False
    # A zero-width lookahead yields one match per START OFFSET, overlapping
    # occurrences included; the iterator is walked twice and never counted, so
    # the module still computes no quantity and compares nothing with a bound.
    starts = re.finditer(f"(?={re.escape(quote)})", text)
    if next(starts, None) is None:
        return False
    return next(starts, None) is None


def _is_block_reason(reason: str) -> bool:
    if reason.startswith(BLOCK_CODE_PREFIX):
        return reason in BLOCK_CODES
    return False


def _reason_is_closed(reason: str) -> bool:
    return reason in DISPOSITION_REASONS or _is_block_reason(reason)


def _keyed(nodes: Iterable[Node], name: str = "key") -> dict[str, list[Node]]:
    """Group records by a declared key. Grouping is not counting."""

    grouped: dict[str, list[Node]] = {}
    for node in nodes:
        key = _string(_field(node, name))
        if key:
            grouped.setdefault(key, []).append(node)
    return grouped


def _declared_keys(situation: Situation, name: str) -> tuple[str, ...] | None:
    declaring = situation.one(READING_SET)
    if declaring is None:
        return None
    listed = _field(declaring, name)
    if not isinstance(listed, (list, tuple)):
        return None
    return tuple(_string(value) for value in listed if _string(value))


def _walk_keys(value: Any) -> Iterable[str]:
    """Every mapping key at any depth of a record."""

    if isinstance(value, dict):
        for key, nested in value.items():
            yield str(key)
            for found in _walk_keys(nested):
                yield found
    elif isinstance(value, (list, tuple)):
        for nested in value:
            for found in _walk_keys(nested):
                yield found


def _declared_vocabulary(situation: Situation, kind: str) -> tuple[str, ...] | None:
    node = situation.one(kind)
    if node is None:
        return None
    listed = _field(node, "keys")
    if not isinstance(listed, (list, tuple)):
        return None
    return tuple(_string(value) for value in listed if _string(value))


def _forbidden_hits(situation: Situation, vocabulary: Sequence[str]) -> list[str]:
    banned = frozenset(vocabulary)
    hits: list[str] = []
    for node in situation.nodes.values():
        if node.kind in (FORBIDDEN_KEYS, AGGREGATE_KEYS):
            continue
        for key in _walk_keys(dict(node.record)):
            if key in banned:
                hits.append(node.id)
                break
    return hits


def _citation_resolves(situation: Situation, node: Node, name: str) -> bool:
    """G2 uniqueness **and** G3's operative target, on one citation.

    G3 is the half that was missing (REVIEW-WAVE1 S3): a quote resolving
    uniquely into the pack's banner, its vocabulary list or its resolver notes
    resolves perfectly well and is not a reading of the material. Where the
    citation records which side it resolved on, that side must be one of
    :data:`DECLARED_SIDES`; ``framing`` - and anything not in the closed set -
    is refused here rather than believed.
    """

    citation = _mapping(_field(node, name))
    quote = _string(citation.get("quote"))
    surface_id = _string(citation.get("surface"))
    if not quote or not surface_id:
        return False
    side = citation.get("side")
    if side is not None and _string(side) not in DECLARED_SIDES:
        return False
    surface = situation.nodes.get(surface_id)
    if surface is None or surface.kind != MATERIAL:
        return False
    return _resolves_uniquely(_string(_field(surface, "text")), quote)


# --------------------------------------------------------------------------
# O - the failed obligations this chain exists to discharge
# --------------------------------------------------------------------------


def row_disposition_complete(situation: Situation) -> Check:
    """o1 - every declared reading row carries a relation or a recorded reason."""

    declared = _declared_keys(situation, "rows")
    if declared is None:
        return Check.not_evaluable((), "no reading_set record declares the row key set")
    readings = _keyed(situation.standing(READING_ROW))
    dispositions = _keyed(situation.standing(DISPOSITION))
    witnesses: list[str] = []
    undisposed: list[str] = []
    unlisted: list[str] = []
    for key in declared:
        witness = None
        for node in readings.get(key, ()):
            relation = _string(_field(node, "relation"))
            if relation and relation != UNRESOLVED_RELATION:
                witness = node
                break
        if witness is None:
            for node in dispositions.get(key, ()):
                reason = _string(_field(node, "reason"))
                if _reason_is_closed(reason):
                    witness = node
                    break
                unlisted.append(node.id)
        if witness is None:
            undisposed.append(key)
        else:
            witnesses.append(witness.id)
    if undisposed or unlisted:
        return Check.not_satisfied(
            unlisted,
            f"rows carrying neither a relation nor a listed reason: {'; '.join(undisposed)}",
        )
    return Check.satisfied(witnesses, "every declared row carries a relation or a reason")


def mark_disposition_complete(situation: Situation) -> Check:
    """o2 - every declared mark cell carries a mark or a per-register reason."""

    declared = _declared_keys(situation, "marks")
    if declared is None:
        return Check.not_evaluable((), "no reading_set record declares the mark key set")
    marks = _keyed(situation.standing(CELL_MARK))
    dispositions = _keyed(situation.standing(DISPOSITION))
    witnesses: list[str] = []
    undisposed: list[str] = []
    malformed: list[str] = []
    for key in declared:
        witness = None
        for node in marks.get(key, ()):
            mark = _string(_field(node, "mark"))
            if not mark:
                continue
            if mark == "differs" and not _string(_field(node, "difference_kind")):
                malformed.append(node.id)
                continue
            witness = node
            break
        if witness is None:
            for node in dispositions.get(key, ()):
                if _reason_is_closed(_string(_field(node, "reason"))):
                    witness = node
                    break
        if witness is None:
            undisposed.append(key)
        else:
            witnesses.append(witness.id)
    if undisposed or malformed:
        return Check.not_satisfied(
            malformed,
            f"mark cells carrying neither a mark nor a listed reason: {'; '.join(undisposed)}",
        )
    return Check.satisfied(witnesses, "every declared mark cell is disposed")


def citations_reresolve(situation: Situation) -> Check:
    """o3 - every relation and every mark cites a passage that re-resolves.

    The quote must occur on the recorded surface and not occur again there;
    where a reading carries its transcript, the judge's decisive point must
    re-resolve the same way inside case + newline + answer.
    """

    readings = tuple(situation.standing(READING_ROW))
    marks = tuple(situation.standing(CELL_MARK))
    if not readings and not marks:
        return Check.not_evaluable((), "no reading or mark is registered")
    resolved: list[str] = []
    unresolved: list[str] = []
    for node in readings:
        relation = _string(_field(node, "relation"))
        if not relation or relation == UNRESOLVED_RELATION:
            continue
        if not _citation_resolves(situation, node, "citation"):
            unresolved.append(node.id)
            continue
        transcript = _mapping(_field(node, "transcript"))
        if transcript:
            exchange = f"{_string(transcript.get('case'))}\n{_string(transcript.get('answer'))}"
            if not _resolves_uniquely(exchange, _string(transcript.get("decisive_point"))):
                unresolved.append(node.id)
                continue
        resolved.append(node.id)
    for node in marks:
        if not _string(_field(node, "mark")):
            continue
        sides = ("left_citation", "right_citation")
        if all(_citation_resolves(situation, node, name) for name in sides):
            resolved.append(node.id)
        else:
            unresolved.append(node.id)
    if unresolved:
        return Check.not_satisfied(unresolved, "citations that do not re-resolve uniquely")
    if not resolved:
        return Check.not_evaluable((), "no relation or mark carries a citation to re-resolve")
    return Check.satisfied(resolved, "every citation re-resolves uniquely on its surface")


def blocks_named(situation: Situation) -> Check:
    """o4 - a blocked cell names a code from the closed set and both blobs."""

    blocked = tuple(
        node for node in situation.records(DISPOSITION)
        if _string(_field(node, "reason")).startswith(BLOCK_CODE_PREFIX)
    )
    if not blocked:
        return Check.not_evaluable((), "no cell records a block")
    named: list[str] = []
    unnamed: list[str] = []
    for node in blocked:
        reason = _string(_field(node, "reason"))
        refs = all(_string(_field(node, name)) for name in ("prompt_ref", "raw_ref"))
        if reason in BLOCK_CODES and refs:
            named.append(node.id)
        else:
            unnamed.append(node.id)
    if unnamed:
        return Check.not_satisfied(
            unnamed, "blocks without a closed reason code or without both blob refs"
        )
    return Check.satisfied(named, "every block names a closed reason code and its blobs")


def audit_in_force(situation: Situation) -> Check:
    """o5 - an audit record declares that it covers the cycle under evaluation.

    The ``audit.period`` cadence is the driver's declared parameter and never
    reaches this predicate: the record itself says which cycles it covers, and
    this is a membership test on that declaration.
    """

    records = tuple(situation.standing(AUDIT_RECORD))
    if not records:
        return Check.not_satisfied((), "no audit record is registered")
    in_force: list[str] = []
    for node in records:
        covers = tuple(str(value) for value in _listed(_field(node, "covers")))
        seats = tuple(_string(value) for value in _listed(_field(node, "seats")))
        calibration = _string(_field(node, "calibration_sha256"))
        if situation.cycle_token in covers and seats and calibration:
            in_force.append(node.id)
    if not in_force:
        return Check.not_satisfied(
            [node.id for node in records],
            f"no registered audit record covers cycle {situation.cycle_token}",
        )
    return Check.satisfied(in_force, "an audit record covers this cycle")


def baseline_sealed_and_carried(situation: Situation) -> Check:
    """o6 - the within-ORIGINAL baseline is sealed and every cross-case call carries it."""

    sealed = situation.one(BASELINE)
    registers = _declared_keys(situation, "registers")
    if sealed is None or registers is None:
        return Check.not_evaluable(
            (), "no sealed baseline, or no declared register set to cover"
        )
    digest = _string(_field(sealed, "sha256"))
    covered = frozenset(_string(value) for value in _listed(_field(sealed, "registers")))
    if not digest or not frozenset(registers).issubset(covered):
        return Check.not_satisfied(
            [sealed.id], "the baseline is unsealed or does not cover every declared register"
        )
    uncarried = [
        node.id for node in situation.records(CALL_RECORD)
        if _field(node, "cross_case") is True
        and _string(_field(node, "baseline_sha256")) != digest
    ]
    if uncarried:
        return Check.not_satisfied(uncarried, "cross-case call records without the baseline pin")
    return Check.satisfied([sealed.id], "the baseline is sealed and carried by every cross-case call")


def trichotomy_rendered(situation: Situation) -> Check:
    """o7 - every declared cell is rendered under exactly one of the four states."""

    rendered = situation.one(RENDERED_STATES)
    rows = _declared_keys(situation, "rows")
    marks = _declared_keys(situation, "marks")
    if rendered is None or rows is None or marks is None:
        return Check.not_evaluable((), "nothing rendered yet, or no declared key set")
    states = _mapping(_field(rendered, "states"))
    declared = frozenset(rows).union(marks)
    printed = frozenset(str(key) for key in states)
    missing = declared.difference(printed)
    extra = printed.difference(declared)
    outside = sorted(
        str(key) for key, value in states.items() if _string(value) not in CELL_STATES
    )
    if missing or extra or outside:
        return Check.not_satisfied(
            [rendered.id],
            "declared keys unrendered: "
            f"{'; '.join(sorted(missing))}; rendered but undeclared: "
            f"{'; '.join(sorted(extra))}; states outside the four: {'; '.join(outside)}",
        )
    return Check.satisfied([rendered.id], "every declared cell is rendered under one of four states")


# --------------------------------------------------------------------------
# P - the protected obligations
# --------------------------------------------------------------------------


def original_bytes_unchanged(situation: Situation) -> Check:
    """p1 - the ORIGINAL bytes are still the occurrence's bytes."""

    materials = tuple(situation.records(MATERIAL))
    if not materials:
        return Check.not_evaluable((), "no material record is registered")
    pinned = situation.one(PINNED_DIGESTS)
    declared = _mapping(_field(pinned, "digests")) if pinned is not None else {}
    intact: list[str] = []
    changed: list[str] = []
    for node in materials:
        text = _string(_field(node, "text"))
        stated = _string(_field(node, "sha256"))
        if not text or not stated:
            continue
        recomputed = hashlib.sha256(text.encode("utf-8")).hexdigest()
        where = _string(_field(node, "occurrence_path"))
        against = _string(declared.get(where)) if where else ""
        if recomputed != stated or (against and against != stated):
            changed.append(node.id)
        else:
            intact.append(node.id)
    if changed:
        return Check.not_satisfied(changed, "material whose bytes no longer hash to their pin")
    if not intact:
        return Check.not_evaluable((), "no material record carries both its bytes and its pin")
    return Check.satisfied(intact, "every material record still hashes to its pinned digest")


def recoding_table_complete(situation: Situation) -> Check:
    """p2 - the recoding correspondence table still covers every recoded unit."""

    table = situation.one(RECODING_TABLE)
    if table is None:
        return Check.not_evaluable((), "no recoding table is registered")
    covers = frozenset(_string(value) for value in _listed(_field(table, "covers")))
    entries = _mapping(_field(table, "entries"))
    missing = sorted(
        unit for unit in covers if not _string(entries.get(unit))
    )
    if missing:
        return Check.not_satisfied(
            [table.id], f"recoded units without a correspondence row: {'; '.join(missing)}"
        )
    return Check.satisfied([table.id], "every recoded unit has a correspondence row")


def shared_envelope_intact(situation: Situation) -> Check:
    """p3 - no case's request differs outside the objection block."""

    requests = tuple(situation.records(CASE_REQUEST))
    if not requests:
        return Check.not_evaluable((), "no case request is registered")
    differing: list[str] = []
    intact: list[str] = []
    for group, nodes in sorted(_keyed(requests, "group").items()):
        reference = _string(_field(nodes[0], "frame"))
        for node in nodes:
            if _string(_field(node, "frame")) == reference:
                intact.append(node.id)
            else:
                differing.append(node.id)
    if differing:
        return Check.not_satisfied(differing, "requests differing outside the objection block")
    return Check.satisfied(intact, "every case in a group shares one envelope")


#: A GFM delimiter row: every cell is dashes, optionally colon-anchored. The
#: header row of a table is the line **immediately above** one of these - not
#: "a line ending in a pipe", which a prose sentence can be (REVIEW-WAVE1 B3's
#: sibling finding against the same rule in ``standard.py``).
_DELIMITER_ROW = re.compile(r"\A\s*\|?(?:\s*:?-+:?\s*\|)+\s*:?-*:?\s*\|?\s*\Z")

#: A setext underline, so that a heading written with one is read as a heading.
_SETEXT_UNDERLINE = re.compile(r"\A\s*(?:=+|--+)\s*\Z")

#: The local tokeniser. ``obligations`` may not import ``standard`` - the
#: pre-registration's forbidden vocabulary reaches this module through the
#: graph, never through a second owner - so the split is spelled here: every
#: run of letters and digits is a token, casefolded.
_WORD = re.compile(r"[0-9A-Za-z]+")


def _rendered_scan_lines(text: str) -> list[str]:
    """The lines of a rendered file p4 reads: headings and table header rows.

    Not the whole body. A rendered artifact **quotes the material**, and the
    material is a published record this loop may not edit: refusing a run
    because a quoted passage carries a forbidden word would be the loop editing
    its own evidence, which is the boundary ``graph.G12_EXEMPT`` draws for the
    same reason. What the loop *wrote* is its headings and its table headers,
    and those are what G12 is about.

    A table's header row is "the line immediately above a delimiter row", which
    is GFM's rule and not "a line ending in a pipe" - a prose sentence can end
    in a pipe and would otherwise hide the next table's header. The pairing is
    done by zipping the lines with their own tail, so this module still adds
    nothing to anything.
    """

    lines = text.splitlines()
    wanted: list[str] = []
    for line, following in zip(lines, [*lines[1:], ""]):
        stripped = line.strip()
        if stripped.startswith("#"):
            wanted.append(line)
            continue
        if not stripped:
            continue
        if "|" in stripped and _DELIMITER_ROW.match(following):
            wanted.append(line)
            continue
        if _SETEXT_UNDERLINE.match(following):
            wanted.append(line)
    return wanted


def _rendered_forbidden_hits(situation: Situation,
                             vocabulary: Sequence[str]) -> list[str]:
    """Every rendered file whose headings or table headers name a banned token.

    Returns the file's own path, so ``p4`` names the offending file and not
    only the record that carried it (REVIEW-WAVE1 B1; REVIEW-PREREG PR-05).
    """

    banned = {str(token).casefold() for token in vocabulary}
    banned.discard("")
    node = situation.one(RENDERED_FILES)
    if node is None:
        return []
    offending: list[str] = []
    for where, text in sorted(_mapping(_field(node, "files")).items()):
        content = _string(text)
        for line in _rendered_scan_lines(content):
            tokens = {match.group().casefold() for match in _WORD.finditer(line)}
            named = sorted(tokens & banned)
            if named:
                offending.append(f"{where}: {', '.join(named)}")
                break
    return offending


def no_scoring_key(situation: Situation) -> Check:
    """p4 - no scoring key appears in any registered record or rendered file.

    Two surfaces, because the pre-registration scopes p4 to "every artifact the
    run registers, **every table header and every file rendered under the run
    root**" and the design's G12 to "every emitted artifact, every table header
    and every rendered file":

    1. the **keys** of every registered record, which is what a scoring key is
       when it is a field; and
    2. the **headings and table header rows** of every file named by the
       ``rendered_files`` record, which is what a scoring key is when it is a
       column. Only what the loop wrote: a quoted passage of the material is
       evidence this loop may not edit (see :func:`_rendered_scan_lines`).

    Until wave 2 this predicate read surface 1 alone, so a ``READING_TABLE.md``
    carrying ``| cell | score | rank |`` passed it - the protected obligation
    the design calls G12's whole point could not fail on a rendered table
    (REVIEW-WAVE1 B1, REVIEW-PREREG PR-05). The witness list now names the
    offending file and the tokens found in it.
    """

    vocabulary = _declared_vocabulary(situation, FORBIDDEN_KEYS)
    if vocabulary is None:
        return Check.not_evaluable((), "no forbidden-key vocabulary is declared in the graph")
    hits = _forbidden_hits(situation, vocabulary)
    rendered = _rendered_forbidden_hits(situation, vocabulary)
    if hits or rendered:
        detail = "records carrying a forbidden scoring key"
        if rendered:
            where = "; ".join(rendered)
            detail = f"{detail}; rendered files naming one in a heading or a header row: {where}"
        witnesses = list(hits)
        node = situation.one(RENDERED_FILES)
        if rendered and node is not None:
            witnesses.append(node.id)
        return Check.not_satisfied(witnesses, detail)
    clean = "no registered record carries a forbidden scoring key"
    scanned = situation.one(RENDERED_FILES)
    if scanned is None:
        return Check.satisfied((), clean)
    return Check.satisfied(
        [scanned.id],
        f"{clean}, and no rendered heading or header row names one")


def write_once_no_replay(situation: Situation) -> Check:
    """p5 - provider and study records stay write-once with no replay."""

    records = tuple(situation.records(CALL_RECORD))
    if not records:
        return Check.not_evaluable((), "no call record is registered")
    digests: dict[str, str] = {}
    offending: list[str] = []
    for node in sorted(records, key=lambda item: item.id):
        coordinate = _string(_field(node, "coordinate"))
        digest = _string(_field(node, "digest"))
        if _string(_field(node, "replay_of")):
            offending.append(node.id)
            continue
        if not coordinate:
            continue
        prior = digests.setdefault(coordinate, digest)
        if prior != digest:
            offending.append(node.id)
    if offending:
        return Check.not_satisfied(offending, "coordinates rewritten, or a call replayed")
    return Check.satisfied(
        [node.id for node in records], "every coordinate carries one record and no replay"
    )


def no_aggregation(situation: Situation) -> Check:
    """p6 - no reading is averaged or majority-voted; disagreement stays unresolved."""

    vocabulary = _declared_vocabulary(situation, AGGREGATE_KEYS)
    readings = tuple(situation.records(READING_ROW))
    if vocabulary is None and not readings:
        return Check.not_evaluable((), "no aggregate vocabulary declared and no reading registered")
    offending: list[str] = []
    if vocabulary is not None:
        offending.extend(_forbidden_hits(situation, vocabulary))
    voted: list[str] = []
    for node in readings:
        rulings = _listed(_field(node, "rulings"))
        if not rulings:
            continue
        reference = _mapping(rulings[0]).get("sustained")
        split = any(_mapping(ruling).get("sustained") != reference for ruling in rulings)
        if split and _string(_field(node, "relation")) != UNRESOLVED_RELATION:
            voted.append(node.id)
    if offending or voted:
        return Check.not_satisfied(
            sorted(frozenset(offending).union(voted)),
            "an aggregate field, or a split ruling that did not stay unresolved",
        )
    return Check.satisfied(
        [node.id for node in readings], "no aggregate field, and every split stayed unresolved"
    )


def no_edges_on_studied_nodes(situation: Situation) -> Check:
    """p7 - nothing the loop mints attacks a node under study, and no node under
    study argues.

    Two conjuncts, and they are not the same prohibition:

    1.  **No ``att`` edge may target a studied node.** The material is read, not
        argued with: an attack on it would make the loop a participant in the
        material's own dispute rather than a reader of it.
    2.  **No studied node may be the SOURCE of any edge**, ``att`` or ``dep``. A
        studied node that attacks or supports something is doing work in the
        adjudication, which is exactly what "under study, not in play" denies.

    A ``dep`` edge *onto* a studied node is permitted, and is the mechanism
    §3 requires: a reading depends on the material it reads, so refuting that
    material leaves the reading ``suspended_unsupported`` - orphaned, not
    refuted - through pass 2. Reading p7's pre-registered prose literally ("no
    att *or dep* edge lands on a node under study") would forbid that edge and
    with it the W1-GRAPH acceptance clause that names it, which is why the
    refinement is stated here rather than worked around in the graph.

    **The pre-registration bundle's p7 sentence must be reworded at its review**
    to this refinement (wave-1 integration decision 1). Nothing about the
    protection is relaxed: the direction that could hide a change to the
    material - the loop attacking it, or the material arguing back - is refused,
    and the detail names which conjunct failed.
    """

    studied = _declared_vocabulary(situation, STUDY_SET)
    if studied is None:
        studied_node = situation.one(STUDY_SET)
        if studied_node is None:
            return Check.not_evaluable((), "no study_set record declares the nodes under study")
        studied = tuple(_string(value) for value in _listed(_field(studied_node, "nodes")))
    under_study = frozenset(studied)
    attacked: list[str] = []
    arguing: list[str] = []
    for source, target in sorted(situation.attacks):
        if target in under_study:
            attacked.append(source)
        if source in under_study:
            arguing.append(source)
    for source, target in sorted(situation.supports):
        if source in under_study:
            arguing.append(source)
    if attacked or arguing:
        return Check.not_satisfied(
            sorted(frozenset(attacked).union(arguing)),
            "artifacts minting an att edge onto a node under study: "
            f"{'; '.join(sorted(frozenset(attacked)))}; nodes under study that are "
            f"themselves the source of an edge: {'; '.join(sorted(frozenset(arguing)))}",
        )
    return Check.satisfied(
        (),
        "nothing attacks a node under study, and no node under study is the source "
        "of an att or a dep edge; a dep onto one is the reading's own dependence",
    )


def appellate_optional(situation: Situation) -> Check:
    """p8 - no state blocks on the appellate.

    A prohibition whose vocabulary this module owns: it holds vacuously on a
    graph that declares no blocker, and bites the moment one is declared.
    """

    waiting = sorted(
        node.id for node in situation.nodes.values()
        if _string(_field(node, "blocked_on")).lower() in APPELLATE_TOKENS
    )
    if waiting:
        return Check.not_satisfied(waiting, "records declaring themselves blocked on the appellate")
    return Check.satisfied((), "no record declares itself blocked on the appellate")


def baseline_still_pinned(situation: Situation) -> Check:
    """p9 - every marked cell's baseline is still at the sha its call records carry."""

    marked = tuple(
        node for node in situation.records(CELL_MARK)
        if _string(_field(node, "baseline_sha256"))
    )
    if not marked:
        return Check.not_evaluable((), "no mark carries a baseline pin")
    sealed = situation.one(BASELINE)
    if sealed is None:
        return Check.not_satisfied(
            [node.id for node in marked], "marks carry a baseline pin but no baseline is registered"
        )
    digest = _string(_field(sealed, "sha256"))
    body = _string(_field(sealed, "body"))
    if body and hashlib.sha256(body.encode("utf-8")).hexdigest() != digest:
        return Check.not_satisfied([sealed.id], "the baseline no longer hashes to its own pin")
    adrift = [
        node.id for node in marked
        if _string(_field(node, "baseline_sha256")) != digest
    ]
    if adrift:
        return Check.not_satisfied(adrift, "marks pinned to a baseline other than the sealed one")
    return Check.satisfied([sealed.id], "every marked cell is pinned to the sealed baseline")


def published_unresolved_preserved(situation: Situation) -> Check:
    """p10 - a published-unresolved cell stays unresolved unless a guarded reading attacks it."""

    declaring = situation.one(PUBLISHED_UNRESOLVED)
    if declaring is None:
        return Check.not_evaluable((), "no published_unresolved record declares the cells")
    declared = tuple(_string(value) for value in _listed(_field(declaring, "keys")))
    opens = _keyed(situation.records(CELL_OPEN))
    guarded = frozenset(
        node.id for node in situation.standing(READING_ROW)
        if _citation_resolves(situation, node, "citation")
    )
    preserved: list[str] = []
    lost: list[str] = []
    for key in declared:
        for node in opens.get(key, ()):
            if node.stands:
                preserved.append(node.id)
                continue
            attackers = frozenset(
                source for source, target in situation.attacks if target == node.id
            )
            if attackers and attackers.issubset(guarded):
                preserved.append(node.id)
            else:
                lost.append(node.id)
    if lost:
        return Check.not_satisfied(lost, "published-unresolved cells moved without a guarded reading")
    if not preserved:
        return Check.not_evaluable((), "no cell-open artifact exists for the declared keys")
    return Check.satisfied(preserved, "every published-unresolved cell is preserved")


def published_tree_untouched(situation: Situation) -> Check:
    """p11 - nothing published is written: the observed digests match the pinned map."""

    pinned = situation.one(PINNED_DIGESTS)
    observed = situation.one(OBSERVED_DIGESTS)
    if pinned is None or observed is None:
        return Check.not_evaluable((), "no pinned map, or the run registered no observation of it")
    declared = _mapping(_field(pinned, "digests"))
    seen = _mapping(_field(observed, "digests"))
    changed = sorted(
        str(where) for where, digest in declared.items()
        if _string(seen.get(where)) != _string(digest)
    )
    if changed:
        return Check.not_satisfied(
            [observed.id], f"published paths whose bytes moved: {'; '.join(changed)}"
        )
    return Check.satisfied([observed.id], "every pinned published path still hashes to its digest")


def ceiling_and_trichotomy_intact(situation: Situation) -> Check:
    """p12 - the ceiling is present verbatim in every rendered file, at its pin."""

    ceiling = situation.one(CEILING)
    rendered = situation.one(RENDERED_FILES)
    if ceiling is None or rendered is None:
        return Check.not_evaluable((), "no ceiling record, or nothing rendered yet")
    body = _string(_field(ceiling, "body"))
    digest = _string(_field(ceiling, "sha256"))
    if body and digest and hashlib.sha256(body.encode("utf-8")).hexdigest() != digest:
        return Check.not_satisfied([ceiling.id], "the ceiling body no longer hashes to its pin")
    sentences = tuple(_string(value) for value in _listed(_field(ceiling, "sentences")))
    files = _mapping(_field(rendered, "files"))
    absent: list[str] = []
    for where, text in sorted(files.items()):
        content = _string(text)
        for sentence in sentences:
            if sentence and sentence not in content:
                absent.append(str(where))
                break
    if absent:
        return Check.not_satisfied(
            [rendered.id], f"rendered files missing a required ceiling sentence: {'; '.join(absent)}"
        )
    return Check.satisfied([ceiling.id, rendered.id], "every rendered file carries the ceiling verbatim")


# --------------------------------------------------------------------------
# The registry
# --------------------------------------------------------------------------

#: name -> program. Every value has the signature ``(situation) -> Check``.
PREDICATES: Mapping[str, Predicate] = MappingProxyType({
    "row_disposition_complete": row_disposition_complete,
    "mark_disposition_complete": mark_disposition_complete,
    "citations_reresolve": citations_reresolve,
    "blocks_named": blocks_named,
    "audit_in_force": audit_in_force,
    "baseline_sealed_and_carried": baseline_sealed_and_carried,
    "trichotomy_rendered": trichotomy_rendered,
    "original_bytes_unchanged": original_bytes_unchanged,
    "recoding_table_complete": recoding_table_complete,
    "shared_envelope_intact": shared_envelope_intact,
    "no_scoring_key": no_scoring_key,
    "write_once_no_replay": write_once_no_replay,
    "no_aggregation": no_aggregation,
    "no_edges_on_studied_nodes": no_edges_on_studied_nodes,
    "appellate_optional": appellate_optional,
    "baseline_still_pinned": baseline_still_pinned,
    "published_unresolved_preserved": published_unresolved_preserved,
    "published_tree_untouched": published_tree_untouched,
    "ceiling_and_trichotomy_intact": ceiling_and_trichotomy_intact,
})

#: name -> the question the program answers, in one line.
PREDICATE_QUESTIONS: Mapping[str, str] = MappingProxyType({
    "row_disposition_complete":
        "does every declared reading row carry a relation with a citation, or a reason from the closed set?",
    "mark_disposition_complete":
        "does every declared mark cell carry a mark (with a difference kind where it differs), or a reason?",
    "citations_reresolve":
        "does every relation's and every mark's quote occur exactly once on its recorded surface?",
    "blocks_named":
        "does every block carry a code from types.BLOCK_CODES and both of its blob refs?",
    "audit_in_force":
        "does a registered audit record declare that it covers this cycle, naming its seats and calibration?",
    "baseline_sealed_and_carried":
        "is the baseline sealed over every declared register and carried by every cross-case call record?",
    "trichotomy_rendered":
        "is every declared cell rendered under exactly one of read / unresolved / machine-unresolved / unread?",
    "original_bytes_unchanged":
        "does every material record still hash to the digest it and the pinned map declare?",
    "recoding_table_complete":
        "does every recoded unit the table declares it covers have a correspondence row?",
    "shared_envelope_intact":
        "do the cases of one group share a byte-identical frame outside the objection block?",
    "no_scoring_key":
        "is the graph free of every key the declared forbidden-key vocabulary names?",
    "write_once_no_replay":
        "does each coordinate carry one record, with no rewrite and no declared replay?",
    "no_aggregation":
        "is there no aggregate field, and did every split ruling leave its row unresolved?",
    "no_edges_on_studied_nodes":
        "is the set of att edges landing on a studied node empty, and is the set of "
        "edges sourced at one empty, a dep landing on one being the permitted case?",
    "appellate_optional":
        "does no record declare itself blocked on the appellate?",
    "baseline_still_pinned":
        "does every marked cell carry the sealed baseline's own digest?",
    "published_unresolved_preserved":
        "does every published-unresolved cell still stand, unless a guarded reading attacks it?",
    "published_tree_untouched":
        "do the observed digests of the published tree match the map pinned at PREREGISTER?",
    "ceiling_and_trichotomy_intact":
        "does every rendered file carry each required ceiling sentence verbatim, at the pinned body?",
})

#: name -> the record kinds the program reads out of the situation.
PREDICATE_READS: Mapping[str, tuple[str, ...]] = MappingProxyType({
    "row_disposition_complete": (READING_SET, READING_ROW, DISPOSITION),
    "mark_disposition_complete": (READING_SET, CELL_MARK, DISPOSITION),
    "citations_reresolve": (READING_ROW, CELL_MARK, MATERIAL),
    "blocks_named": (DISPOSITION,),
    "audit_in_force": (AUDIT_RECORD,),
    "baseline_sealed_and_carried": (READING_SET, BASELINE, CALL_RECORD),
    "trichotomy_rendered": (READING_SET, RENDERED_STATES),
    "original_bytes_unchanged": (MATERIAL, PINNED_DIGESTS),
    "recoding_table_complete": (RECODING_TABLE,),
    "shared_envelope_intact": (CASE_REQUEST,),
    "no_scoring_key": (FORBIDDEN_KEYS,),
    "write_once_no_replay": (CALL_RECORD,),
    "no_aggregation": (AGGREGATE_KEYS, READING_ROW),
    "no_edges_on_studied_nodes": (STUDY_SET,),
    "appellate_optional": (),
    "baseline_still_pinned": (CELL_MARK, BASELINE),
    "published_unresolved_preserved": (PUBLISHED_UNRESOLVED, CELL_OPEN, READING_ROW),
    "published_tree_untouched": (PINNED_DIGESTS, OBSERVED_DIGESTS),
    "ceiling_and_trichotomy_intact": (CEILING, RENDERED_FILES),
})


def predicate(name: str) -> Predicate:
    """The program a pre-registration named, refusing an unregistered name."""

    found = PREDICATES.get(name)
    if found is None:
        raise _refuse("OBLIGATION_CHECK_UNKNOWN", repr(name))
    return found


# --------------------------------------------------------------------------
# Evaluation, ProducedBy, and the loss registers
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Evaluation:
    """Every obligation's verdict at one situation, and what this cycle produced."""

    pin: str
    cycle: int
    obligations: Obligations
    checks: Mapping[str, Check] = field(default_factory=dict)
    produced_by: Mapping[str, tuple[str, ...]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "checks", MappingProxyType(dict(self.checks)))
        object.__setattr__(self, "produced_by", MappingProxyType(dict(self.produced_by)))

    def verdict(self, obligation_id: str) -> Verdict:
        found = self.checks.get(obligation_id)
        if found is None:
            raise _refuse("OBLIGATION_UNKNOWN", repr(obligation_id))
        return found.verdict

    def _ids_where(self, membership: str | None, verdict: Verdict) -> tuple[str, ...]:
        return tuple(
            entry.id for entry in self.obligations.entries
            if (membership is None or entry.membership == membership)
            and self.checks[entry.id].verdict is verdict
        )

    @property
    def satisfied(self) -> tuple[str, ...]:
        return self._ids_where(None, Verdict.SATISFIED)

    @property
    def not_satisfied(self) -> tuple[str, ...]:
        return self._ids_where(None, Verdict.NOT_SATISFIED)

    @property
    def not_evaluable(self) -> tuple[str, ...]:
        return self._ids_where(None, Verdict.NOT_EVALUABLE)

    @property
    def failed(self) -> tuple[str, ...]:
        """O members that do not hold here - read or unread (see the docstring)."""
        return tuple(
            entry.id for entry in self.obligations.failed
            if not self.checks[entry.id].holds
        )

    @property
    def every_o_satisfied(self) -> bool:
        """Clause 3's antecedent. A not_evaluable obligation never makes it true."""
        return all(self.checks[entry.id].holds for entry in self.obligations.failed)

    @property
    def protected_not_evaluable(self) -> tuple[str, ...]:
        """Exposed, never a loss (FW5 R5)."""
        return self._ids_where(PROTECTED_SET, Verdict.NOT_EVALUABLE)

    @property
    def discharged(self) -> tuple[str, ...]:
        """O members that hold here and were produced by this cycle's artifacts."""
        return tuple(
            entry.id for entry in self.obligations.failed
            if self.checks[entry.id].holds and self.produced_by.get(entry.id)
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "obligations_pin": self.pin,
            "cycle": self.cycle,
            "checks": {
                key: self.checks[key].as_dict() for key in sorted(self.checks)
            },
            "produced_by": {
                key: list(self.produced_by[key]) for key in sorted(self.produced_by)
            },
            "satisfied": list(self.satisfied),
            "not_satisfied": list(self.not_satisfied),
            "not_evaluable": list(self.not_evaluable),
            "failed": list(self.failed),
            "discharged": list(self.discharged),
            "protected_not_evaluable": list(self.protected_not_evaluable),
        }


@dataclass(frozen=True)
class Loss:
    """One exposed loss: what it is about, how it stood, how it stands now."""

    kind: str
    subject: str
    was: str
    now: str
    membership: str = ""
    detail: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "subject": self.subject,
            "was": self.was,
            "now": self.now,
            "set": self.membership,
            "detail": self.detail,
        }


#: The loss kinds this module can expose.
LOSS_KINDS: tuple[str, ...] = (
    "protected_loss",
    "obligation_regressed",
    "obligation_unevaluable",
    "standing_withdrawn",
    "artifact_absent",
)


def _run(entry: Obligation, situation: Situation) -> Check:
    result = entry.predicate(situation)
    if not isinstance(result, Check):
        raise _refuse("PREDICATE_CONTRACT_VIOLATED", f"{entry.id}: {entry.check}")
    return result


def evaluate(obligations: Obligations, situation: Situation) -> Evaluation:
    """Every obligation's verdict at this situation, with ProducedBy attributed.

    Pure: it reads the situation and writes nothing. It refuses a situation
    pinned to a different document, because O and P may not shift inside an
    assessment (FW5:787).
    """

    if not isinstance(obligations, Obligations):
        raise _refuse("SITUATION_INVALID", "evaluate() takes a loaded Obligations")
    if not isinstance(situation, Situation):
        raise _refuse("SITUATION_INVALID", "evaluate() takes a Situation")
    if situation.obligations.pin != obligations.pin:
        raise _refuse(
            "OBLIGATIONS_PIN_SHIFTED",
            f"situation pinned to {situation.obligations.pin}, asked for {obligations.pin}",
        )
    checks = {entry.id: _run(entry, situation) for entry in obligations.entries}
    withheld = situation.without(situation.registered) if situation.registered else None
    attributed: dict[str, tuple[str, ...]] = {}
    for entry in obligations.entries:
        attributed[entry.id] = _attribute(entry, situation, checks[entry.id], withheld)
    return Evaluation(
        pin=obligations.pin,
        cycle=situation.cycle,
        obligations=obligations,
        checks=checks,
        produced_by=attributed,
    )


def _attribute(
    entry: Obligation,
    situation: Situation,
    result: Check,
    withheld: Situation | None,
) -> tuple[str, ...]:
    """The two conjuncts of ProducedBy; empty unless both hold."""

    if not result.holds or withheld is None:
        return ()
    attribution = frozenset(result.evidence).intersection(situation.registered)
    if not attribution:
        return ()
    if _run(entry, withheld).holds:
        return ()
    return tuple(sorted(attribution))


@dataclass(frozen=True)
class Production:
    """What withholding this cycle's registrations did to one obligation.

    ``produced_by`` answers with a set of artifacts and nothing else, and two
    very different things make that set non-empty: the obligation **stopped
    holding** without this cycle's records, or it became **unreadable** without
    them. FW5 R5 - non-evaluability is not refutation - is exactly the
    distinction between those two, and a record that prints only the set has
    thrown it away (wave-1 integration decision 49).

    ``withheld_verdict`` is the verdict the predicate gives on the withheld
    view, so a reader can tell which happened. ``holds_here`` is the verdict on
    the situation as it stands.
    """

    obligation_id: str
    artifacts: frozenset[str]
    verdict: Verdict
    withheld_verdict: Verdict | None

    #: The R5 reading of ``withheld_verdict``, in the record's own words.
    WITHHELD_READING: Mapping[str, str] = field(default_factory=lambda: dict(
        _WITHHELD_READING), repr=False, compare=False)

    @property
    def attributed(self) -> bool:
        return bool(self.artifacts)

    @property
    def withheld_reading(self) -> str:
        if self.withheld_verdict is None:
            return _WITHHELD_READING["not_withheld"]
        return _WITHHELD_READING[self.withheld_verdict.value]

    def as_dict(self) -> dict[str, Any]:
        return {
            "obligation": self.obligation_id,
            "artifacts": sorted(self.artifacts),
            "verdict": self.verdict.value,
            "withheld_verdict": (None if self.withheld_verdict is None
                                 else self.withheld_verdict.value),
            "withheld_reading": self.withheld_reading,
        }


#: The three readings of a withheld verdict, spelled once (R5).
_WITHHELD_READING: Mapping[str, str] = MappingProxyType({
    "not_satisfied":
        "withholding this cycle's registrations makes the obligation stop "
        "holding, which is what attribution to this cycle means",
    "not_evaluable":
        "withholding this cycle's registrations makes the obligation "
        "unreadable, which is an absence of evidence and not a loss of the "
        "obligation (FW5 R5); the attribution is recorded with this reading "
        "beside it and is never reported as a stronger one",
    "satisfied":
        "the obligation holds without this cycle's registrations, so nothing "
        "this cycle registered produced it (FW5:800)",
    "not_withheld":
        "this cycle registered nothing, so there was nothing to withhold",
})


def production_of(situation: Situation, obligation_id: str) -> Production:
    """:func:`produced_by`'s answer, with the R5 distinction kept.

    Same attribution, plus the verdict the predicate gives on the withheld
    view, so a record can say whether the obligation *stopped holding* without
    this cycle or merely became *unreadable* without it.
    """

    if not isinstance(situation, Situation):
        raise _refuse("SITUATION_INVALID", "production_of() takes a Situation")
    entry = situation.obligations.by_id(obligation_id)
    result = _run(entry, situation)
    withheld = situation.without(situation.registered) if situation.registered else None
    artifacts = frozenset(_attribute(entry, situation, result, withheld))
    return Production(
        obligation_id=str(obligation_id),
        artifacts=artifacts,
        verdict=result.verdict,
        withheld_verdict=None if withheld is None else _run(entry, withheld).verdict,
    )


def produced_by(situation: Situation, obligation_id: str) -> frozenset[str]:
    """The artifacts of this cycle that made that obligation hold.

    Empty when the obligation does not hold, when no artifact of this cycle is
    among the evidence, or when the obligation still holds with this cycle's
    registrations withheld - the last being exactly the case FW5:800 rules
    out, where succession is mistaken for production.

    A non-empty answer does **not** distinguish "stopped holding without this
    cycle" from "became unreadable without it"; :func:`production_of` returns
    both, and the second is FW5 R5's non-evaluability, which is never a
    stronger claim than it is.
    """

    return production_of(situation, obligation_id).artifacts


def _both(prev: Situation | None, curr: Situation) -> tuple[Evaluation | None, Evaluation]:
    if not isinstance(curr, Situation):
        raise _refuse("SITUATION_INVALID", "the cycle-end situation is required")
    if prev is not None:
        if not isinstance(prev, Situation):
            raise _refuse("SITUATION_INVALID", "the prior situation must be a Situation or None")
        if prev.obligations.pin != curr.obligations.pin:
            raise _refuse(
                "OBLIGATIONS_PIN_SHIFTED",
                "the two situations are pinned to different obligations documents",
            )
    before = evaluate(prev.obligations, prev) if prev is not None else None
    return before, evaluate(curr.obligations, curr)


def losses_outside_p(prev: Situation | None, curr: Situation) -> list[Loss]:
    """The register FW5:802 requires, written every cycle, present even when empty.

    It carries what fell outside the protected set: an obligation of O that
    held and no longer does, an obligation that became unreadable, and every
    artifact that stood at the prior situation and no longer stands. A cycle
    may be net withdrawal and still be progress (FW5:810); that judgement is
    W2-DECIDE's, and this register is what it must not hide.
    """

    before, after = _both(prev, curr)
    losses: list[Loss] = []
    if before is None or prev is None:
        return losses
    for entry in curr.obligations.failed:
        was = before.verdict(entry.id)
        now = after.verdict(entry.id)
        if was is not Verdict.SATISFIED:
            continue
        if now is Verdict.NOT_SATISFIED:
            losses.append(Loss(
                kind=LOSS_KINDS[1], subject=entry.id, was=was.value, now=now.value,
                membership=FAILED_SET, detail=entry.statement,
            ))
        elif now is Verdict.NOT_EVALUABLE:
            losses.append(Loss(
                kind=LOSS_KINDS[2], subject=entry.id, was=was.value, now=now.value,
                membership=FAILED_SET, detail=after.checks[entry.id].detail,
            ))
    for node_id in sorted(prev.nodes):
        was_node = prev.nodes[node_id]
        if not was_node.stands:
            continue
        now_node = curr.nodes.get(node_id)
        if now_node is None:
            losses.append(Loss(
                kind=LOSS_KINDS[4], subject=node_id, was=was_node.status,
                now="absent", detail=was_node.kind,
            ))
        elif not now_node.stands:
            losses.append(Loss(
                kind=LOSS_KINDS[3], subject=node_id, was=was_node.status,
                now=now_node.status, detail=now_node.kind,
            ))
    return losses


def protected_losses(prev: Situation | None, curr: Situation) -> list[Loss]:
    """Clause 1's register: a protected obligation that held and no longer does.

    A protected obligation that became unreadable is **not** a loss; it is
    exposed on ``Evaluation.protected_not_evaluable`` instead (FW5 R5).
    """

    before, after = _both(prev, curr)
    losses: list[Loss] = []
    if before is None:
        return losses
    for entry in curr.obligations.protected:
        was = before.verdict(entry.id)
        now = after.verdict(entry.id)
        if was is Verdict.SATISFIED and now is Verdict.NOT_SATISFIED:
            losses.append(Loss(
                kind=LOSS_KINDS[0], subject=entry.id, was=was.value, now=now.value,
                membership=PROTECTED_SET, detail=entry.statement,
            ))
    return losses
