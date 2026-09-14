"""Closed vocabularies and strict role schemas for the automated harness loop.

What this is
------------
The one place the loop says what a model is allowed to hand back. Five roles
(``critic``, ``defender``, ``judge``, ``marker``, ``variator``) each have a
JSON Schema that is closed at every level (``additionalProperties: false``,
every value enumerated where a vocabulary exists), a typed frozen record for
the output that survives validation, and a validator that either returns a
structured failure or raises :class:`SchemaInvalid` naming the reason. It also
carries the forbidden-key guard (G12) and re-exports, under the spellings the
wave plan published for this module, the closed vocabularies W0-STANDARD owns -
including the reading vocabulary and the instrument's banner, which no module of
this package retypes.

Design section implemented
--------------------------
W0-CONTRACTS of *The automated end-to-end harness loop — FINAL design of
record*: §2.3 "Prompt contracts and JSON schemas" in full, plus the schema and
vocabulary half of §2.4 — **G1** (schema; invalid output is a block, never a
repair), **G4** (closed vocabulary; a non-empty ``outside_vocabulary`` is
normalised here to :data:`NONE_RELATION` with the nominated token and the text
both preserved - the *cell* state that follows from it is W2's and W3's to
write, and this module names no cell state), the closed per-register
``difference_kind`` token set of **G9**/D4, and **G12** (no scoring key).

What this is NOT
----------------
It computes no relation, resolves no offset, calls no provider, opens no file
and writes none. It holds no block-code registry: ``BLOCK_CODES`` belongs to
W0-TYPES, and the reasons named here (:data:`SCHEMA_REASONS`) are the
sub-reasons of a single block code, not block codes. It ranks nothing: no
member of any vocabulary here is ordered against another, no field of any
schema is numeric, and there is no aggregate, count, majority or mean anywhere
in a role's output (FW5:851; PURPOSE.md, "no scalar progress meter").

**And it owns no shared vocabulary, and no longer owns §2.3's schemas.** Every
closed vocabulary this module validates against - :data:`READING_VOCABULARY`,
:data:`CRITIC_RELATIONS`, :data:`UNRESOLVED`, :data:`NONE_RELATION`,
:data:`OUTSIDE_VOCABULARY_FIELD`, :data:`REGISTERS`, :data:`MARKS`,
:data:`DIFFERENCE_KINDS`, :data:`ALL_DIFFERENCE_KINDS`, :data:`FORBIDDEN_KEYS`
and :data:`READING_BANNER` - and, since the wave-0 review, the §2.3 contracts
themselves - :data:`ROLE_NAMES`, :data:`ROLE_BINDING_FIELDS`,
:data:`WORD_LIMITS`, the five role schemas and :data:`SCHEMAS` - are imported
from :mod:`minireason.loop.standard`, which is their single owner, and
re-exported here under the spelling the wave plan published for this module. The
names on both sides are the *same objects*: there is nothing left to drift. The
edge is one-way and acyclic (``types -> standard -> contracts``); ``standard``
imports this module nowhere, and a test asserts it.

The schemas moved for one reason: a plan pins the standard body by sha256, and
until §2.3 was inside that body, editing a schema or a word limit changed **no
digest at all** - so §5's "changing any threshold after first look mints a new
``loop_plan_id``" did not reach the guard content this module holds. The body now
carries the word limits and ``sha256(canonical(SCHEMAS))``.

Deviations from the design, and why
-----------------------------------
* **``validate`` takes one keyword-only extra.** The design names
  ``validate(role, raw)``; that signature is exactly preserved. A marker's
  ``difference_kind`` is drawn from a *per-register* token set, and the role
  name alone does not say which register was asked, so the optional
  ``register=`` keyword narrows the check from the union of all tokens to that
  register's own set. Omitted, the union is used and nothing is weakened for
  callers that do not know the register.
* **``check`` beside ``validate``.** The design asks for a validator that
  returns a structured failure rather than raising (W2-ROLES turns an invalid
  output into ``unresolved`` at ``schema_repair_budget = 0``, which is a value,
  not an exception). :func:`check` never raises; :func:`validate` is
  ``check`` plus a raise. :data:`VALIDATORS` is the per-schema form.
* **``raw`` may arrive as JSON text.** A provider hands back bytes. Passing
  ``str``/``bytes`` is accepted and parsed; a parse failure is the reason
  ``not-json`` rather than a ``json`` exception escaping the contract layer.
* **Program checks beyond JSON Schema.** JSON Schema cannot count words, so
  the ``<= 400`` / ``<= 120`` word bounds of §2.3 are enforced in Python
  (:data:`WORD_LIMITS`, whitespace-separated tokens). Three further checks are
  enforced the same way because the vendored registration gate would otherwise
  reject the artifact later, with less to say about why:
  ``deepreason_core.harness.conforming_transcript`` requires a non-empty
  ``case`` and ``answer`` and a non-empty ``decisive_point``, so a critic that
  claims a relation must supply a case and a passage to quote, and a marker
  that claims ``differs`` must supply both sides' quotes and a
  ``difference_kind``. A critic answering ``none`` is held to none of this: it
  ends the row at one call (§2.3) and never reaches a transcript.
* **:data:`FORBIDDEN_KEYS` is not a copy of the tool's literal, but it is not
  an import from it either.** G12's guard is
  ``tools/contrast_triple_study.assert_no_scoring_keys``, which lives in a
  script directory that is not an importable package: a library module that
  reached into it would be unimportable from an installed wheel. The key set is
  therefore mirrored **once**, in W0-STANDARD, and imported from there;
  ``tests/loop/test_contracts.py`` parses the tool's own literal and asserts
  the sets are equal, so drift from the tool fails a test rather than passing
  silently. The behaviour of the guard here is identical to the tool's except
  that it also descends into tuples, which the tool's version does not: it
  refuses strictly more scoring keys and accepts none that the tool refuses.
* **``DIFFERENCE_KINDS`` is W0-STANDARD's, and it is finer than register
  grain.** D4 adopts "``design-loop``'s closed per-register
  ``difference_kind`` token set" *because* one token per register makes kind
  grain identical to register grain, which is the over-suppression of
  ``differs`` D4 rejects. This module originally carried a one-token-per-
  register set of its own; the wave-0 integration deleted it in favour of
  W0-STANDARD's, which keeps every token the design sketches
  (``target_set_membership``, ``record_engaged``, ``disposition_value``,
  ``grounds_source``) and adds only distinctions PLAN §8a itself draws in the
  register they belong to (``target_prefix_source``, ``engagement_form``,
  ``disposition_carrier_field``). The marker schema closes
  ``difference_kind`` over :data:`ALL_DIFFERENCE_KINDS`, which is now derived
  from that one set, so a token outside it is refused at the schema with
  reason ``not-in-enum`` before anything is registered.
* **:func:`assert_no_scoring_keys` refuses a rendered file rather than passing
  it.** G12's subjects are "every emitted artifact, every table header and every
  rendered file"; a ``str`` handed to a key-structure guard used to answer
  ``None`` in silence, which made §5's *p4* unfalsifiable on two of its three
  subjects. A ``str``/``bytes`` argument is now a :class:`ContractError`, and
  :func:`assert_no_scoring_headers` - W0-STANDARD's, re-exported here - is the
  scanner for a rendered file's table headers and headings. It raises
  ``StandardInvalid`` with the same ``SCORING_KEY_FORBIDDEN`` code, because one
  rule records one token.
* **A critic that both names a relation and writes ``outside_vocabulary`` is
  normalised, not refused** (see :class:`CriticOutput`). Refusing would discard
  the very text D6 exists to preserve.
* **:data:`VALIDATORS` forwards ``register=``.** Without it every marker
  validated through the mapping was held to the seven-token union rather than to
  its own register's set (O11).

Purity
------
Every callable here is a pure function of its arguments. No clock, no
randomness, no environment, no I/O, no global mutation, and no argument is
mutated: validation deep-copies nothing because it reads and never writes, and
the values it returns are frozen dataclasses. Importing this module imports
W0-STANDARD, which reads its two shipped data files once, at import; no
callable here opens anything.
"""
from __future__ import annotations

import copy
import json
from dataclasses import dataclass, fields, is_dataclass
from types import MappingProxyType
from typing import Any, Callable, Mapping, Sequence

from jsonschema import Draft202012Validator

from minireason.loop.standard import (
    ALL_DIFFERENCE_KINDS,
    CRITIC_RELATIONS,
    CRITIC_SCHEMA,
    DEFENDER_SCHEMA,
    DIFFERENCE_KINDS,
    DIFFERS_MARK,
    FORBIDDEN_KEYS,
    JUDGE_SCHEMA,
    MARKER_SCHEMA,
    MARKS,
    NONE_TOKEN,
    OUTSIDE_VOCABULARY_FIELD,
    READING_BANNER,
    READING_VOCABULARY,
    REGISTERS,
    ROLE_BINDING_FIELDS,
    ROLE_NAMES,
    SCHEMAS,
    UNRESOLVED_TOKEN,
    VARIATOR_SCHEMA,
    WORD_LIMITS,
    assert_no_scoring_headers,
)
from minireason.loop.types import LoopError

__all__ = [
    "CONTRACTS_VERSION",
    "READING_BANNER",
    "READING_VOCABULARY",
    "CRITIC_RELATIONS",
    "NONE_RELATION",
    "UNRESOLVED",
    "OUTSIDE_VOCABULARY_FIELD",
    "ROLE_BINDING_FIELDS",
    "ROLE_NAMES",
    "REGISTERS",
    "MARKS",
    "DIFFERENCE_KINDS",
    "ALL_DIFFERENCE_KINDS",
    "WORD_LIMITS",
    "FORBIDDEN_KEYS",
    "AGGREGATE_KEYS",
    "SCHEMA_REASONS",
    "SCHEMA_INVALID",
    "CONTRACT_VIOLATION",
    "SCORING_KEY_FORBIDDEN",
    "CRITIC_SCHEMA",
    "DEFENDER_SCHEMA",
    "JUDGE_SCHEMA",
    "MARKER_SCHEMA",
    "VARIATOR_SCHEMA",
    "SCHEMAS",
    "VALIDATORS",
    "ContractError",
    "SchemaInvalid",
    "ScoringKeyForbidden",
    "RoleBindings",
    "CriticOutput",
    "DefenderOutput",
    "JudgeRuling",
    "MarkerOutput",
    "VariatorOutput",
    "RoleOutput",
    "Validation",
    "assert_no_aggregate_fields",
    "assert_no_scoring_headers",
    "assert_no_scoring_keys",
    "check",
    "difference_kinds_for",
    "schema_for",
    "validate",
]

CONTRACTS_VERSION = "loop.contracts/1"

# --------------------------------------------------------------------- #
# Vocabularies. Every one of them is W0-STANDARD's object, re-exported.  #
# Nothing in this section defines a vocabulary; there is one owner.      #
# --------------------------------------------------------------------- #

# ``READING_BANNER``   - the instrument's own banner, verbatim (§2.3: the critic
#                        pack carries "the instrument's own lexical-overlap
#                        banner verbatim").
# ``READING_VOCABULARY``- the six-value reading vocabulary, the published tuple
#                        object itself. Its own docstring records that it is not
#                        a closed single-valued enum; D6 closes it for the
#                        machine and pays for the narrowing with
#                        ``OUTSIDE_VOCABULARY_FIELD`` and the claim ceiling. Its
#                        order is the published order and carries no rank.
# ``CRITIC_RELATIONS`` - what a critic may nominate: the vocabulary minus
#                        ``unresolved`` (the standing default, not a claim) plus
#                        ``none``.
# ``REGISTERS``        - C001 PLAN §8a's four register ids, in the plan's order;
#                        the register *definitions* are W0-STANDARD's, mirrored
#                        byte-identically from PLAN.md. Marked separately, never
#                        summed, averaged, weighted, ranked or reduced.
# ``MARKS``            - the three marks, in PLAN §8a's order.
# ``DIFFERENCE_KINDS`` - the closed per-register ``difference_kind`` token set
#                        (D4), at the finer-than-register grain D4 requires.
# ``FORBIDDEN_KEYS``   - G12's scoring-key set, mirrored from the contrast tool.
# All imported above.

#: The one token shared by the reading vocabulary and the mark vocabulary, and
#: the state every cell starts in (D3: it is the position that must be beaten).
UNRESOLVED = UNRESOLVED_TOKEN

#: The critic's own "no relation is established here" answer. It is *not* a
#: reading of ``unresolved``: the cell was read and nothing was found, which
#: ends the row at one call (§2.3) and leaves the cell where it started.
#: W0-STANDARD spells it ``NONE_TOKEN``; this is that object.
NONE_RELATION = NONE_TOKEN

# ``ROLE_NAMES``, ``ROLE_BINDING_FIELDS``, ``ALL_DIFFERENCE_KINDS``,
# ``WORD_LIMITS``, the five role schemas and ``SCHEMAS`` are imported above from
# W0-STANDARD for the reason its deviation 6 gives: §2.3 is pre-registered guard
# content, and until it was inside the standard body, editing a schema or a word
# limit changed no digest. The names here are those objects, re-exported under the
# spelling the wave plan published for this module.

# --------------------------------------------------------------------- #
# G12 — the forbidden-key guard                                          #
# --------------------------------------------------------------------- #

# ``FORBIDDEN_KEYS`` is imported from W0-STANDARD, which mirrors
# ``tools/contrast_triple_study.FORBIDDEN_KEYS``; the test asserts the two sets
# are equal. A label naming an outcome is not a quantity, and nothing in this
# loop may write a field whose name asserts one.

#: Names an *output schema* may not use. **Disjoint from** :data:`FORBIDDEN_KEYS`
#: - not wider than it, as this note used to claim: the two sets name different
#: things and :func:`assert_no_aggregate_fields` applies both, so a schema is
#: held to their union while an artifact is held to ``FORBIDDEN_KEYS`` alone.
#: The split is deliberate: a block register legitimately prints counts by reason
#: code (W3-REPORT), while a role's own output may never carry a count, a
#: majority, a mean or a confidence. This set is applied to the schemas at import
#: and by the test, never to artifacts.
AGGREGATE_KEYS: frozenset[str] = frozenset({
    'aggregate', 'aggregates', 'average', 'averages', 'combined', 'confidence',
    'count', 'counts', 'exhaustion', 'index', 'level', 'majority', 'mean', 'median',
    'overall', 'percent', 'percentage', 'probability', 'proportion', 'ratio',
    'severity', 'strength', 'sum', 'tally', 'total', 'totals', 'vote', 'votes',
})

#: The code the guard raises with, byte-identical to the existing tool's.
SCORING_KEY_FORBIDDEN = "SCORING_KEY_FORBIDDEN"

#: Every reason :class:`SchemaInvalid` can name. These are sub-reasons of one
#: block code (``blocked:schema``, W0-TYPES); they are not block codes.
SCHEMA_REASONS: tuple[str, ...] = (
    "unknown-role",
    "unknown-register",
    "not-json",
    "not-an-object",
    "missing-field",
    "unexpected-field",
    "wrong-type",
    "not-in-enum",
    "empty-field",
    "too-few-items",
    "not-unique",
    "word-limit",
    "case-required",
    "passage-quote-required",
    "difference-kind-required",
    "difference-kind-forbidden",
    "difference-kind-unknown",
    "quote-required",
)

_JSONSCHEMA_REASONS: Mapping[str, str] = MappingProxyType({
    "required": "missing-field",
    "additionalProperties": "unexpected-field",
    "type": "wrong-type",
    "enum": "not-in-enum",
    "minLength": "empty-field",
    "minItems": "too-few-items",
    "uniqueItems": "not-unique",
})


#: The code a receipt records for a contract failure that is not one of the two
#: named below. The sub-reason, where there is one, rides on ``.reason``.
CONTRACT_VIOLATION = "CONTRACT_VIOLATION"

#: The code a receipt records for a role output that failed its schema. The
#: *block* code is ``blocked:schema`` (W0-TYPES); this is the exception's own
#: stable token, and the sub-reason is on ``.reason``.
SCHEMA_INVALID = "SCHEMA_INVALID"


class ContractError(LoopError, ValueError):
    """A role's output, or a value about to be emitted, broke a contract.

    A subclass of :class:`~minireason.loop.types.LoopError`, so it carries a
    ``.code`` from ``types.FAILURE_CODES`` and one ``except LoopError`` catches
    every wave-0 refusal; still a ``ValueError``, so a caller written against
    the original spelling keeps working. The argument order is
    ``(code, detail)`` - the same order every other wave-0 exception takes, so
    a reader never has to remember which module inverts it.
    """

    def __init__(self, code: str = CONTRACT_VIOLATION, detail: str = "") -> None:
        LoopError.__init__(self, code, detail)


class SchemaInvalid(ContractError):
    """A role's output did not satisfy its contract. ``reason`` names why.

    ``reason`` is a member of :data:`SCHEMA_REASONS`; ``path`` is the location
    inside the output, outermost first; ``role`` is the role asked. The string
    form names all three, so a log line carries the reason without unpacking.
    ``.code`` is :data:`SCHEMA_INVALID`, which is what a receipt's
    ``failure_code`` carries; the cell's block code is ``blocked:schema``.
    """

    def __init__(
        self,
        role: str,
        reason: str,
        message: str,
        path: Sequence[str] = (),
    ) -> None:
        self.role = role
        self.reason = reason
        self.path: tuple[str, ...] = tuple(path)
        where = "/".join(self.path) if self.path else "<root>"
        #: The bare message, without the role/reason/path prefix.
        self.message = message
        # ``detail`` stays the composed string the base class put in ``str()``,
        # so :class:`~minireason.loop.types.LoopError`'s one invariant -
        # ``str(exc) == f"{code}: {detail}"`` - holds here too. The bare text is
        # on ``.message``; it used to overwrite ``.detail`` and break it.
        super().__init__(SCHEMA_INVALID, f"{role}: {reason}: {where}: {message}")


class ScoringKeyForbidden(ContractError):
    """A key whose name asserts a quantity appeared in a value (G12).

    ``str(exc)`` is exactly ``SCORING_KEY_FORBIDDEN`` and ``exc.code`` is the
    same string, so the existing study's ``code_of`` reads it unchanged; the
    offending location is on ``exc.path``.
    """

    code = SCORING_KEY_FORBIDDEN

    def __init__(self, path: Sequence[str] = ()) -> None:
        self.path: tuple[str, ...] = tuple(path)
        super().__init__(SCORING_KEY_FORBIDDEN)


# --------------------------------------------------------------------- #
# Typed role outputs                                                     #
# --------------------------------------------------------------------- #


@dataclass(frozen=True)
class RoleBindings:
    """The FW5:609 criticism constituents, as the critic bound them."""

    target: str
    defect: str
    grounds: str
    bearing: str

    def as_dict(self) -> dict[str, str]:
        return {field: getattr(self, field) for field in ROLE_BINDING_FIELDS}


@dataclass(frozen=True)
class CriticOutput:
    """One critic's case that exactly one named relation holds (§2.3).

    **D6 normalisation.** A seat may hand back both a named ``relation`` and a
    non-empty ``outside_vocabulary``. G4 says a non-empty ``outside_vocabulary``
    forces the cell to ``unresolved`` with reason ``outside-vocabulary`` and
    preserves the text; but ``.relation`` still named the relation, so a renderer
    reading ``.relation`` printed a relation for a cell that must read
    ``unresolved``. Refusing the output would have been the other repair, and it
    would have thrown away the very text D6 exists to preserve. So the output is
    **normalised, not refused**: ``.relation`` becomes :data:`NONE_RELATION`, the
    nominated token is kept on :attr:`nominated_relation` so nothing is lost, and
    the ``outside_vocabulary`` text is carried through unaltered. ``.as_dict()``
    emits the normalised relation, so what is recorded is what a renderer reads.
    """

    relation: str
    passage_quote: str
    role_bindings: RoleBindings
    case: str
    outside_vocabulary: str
    #: What the seat nominated before D6 normalisation, where it was normalised
    #: away; ``""`` otherwise. Never a claim: the cell stays unresolved.
    nominated_relation: str = ""

    def __post_init__(self) -> None:
        if self.outside_vocabulary and self.relation != NONE_RELATION:
            object.__setattr__(self, "nominated_relation", self.relation)
            object.__setattr__(self, "relation", NONE_RELATION)

    @property
    def is_outside_vocabulary(self) -> bool:
        """D6: the reading is outside the closed vocabulary, text preserved."""
        return bool(self.outside_vocabulary)

    @property
    def claims_relation(self) -> bool:
        """True when a trial is owed: a named relation, inside the vocabulary."""
        return self.relation != NONE_RELATION and not self.is_outside_vocabulary

    def as_dict(self) -> dict[str, Any]:
        """The five fields of the critic's §2.3 contract, and only those.

        :attr:`nominated_relation` is **not** among them: the contract names
        five fields and this is the record a pack, a transcript and a receipt
        carry, so adding a sixth would put a field into published artifacts that
        no schema declares. The nominated token survives on the object for a
        caller that wants to say what was normalised away - a W3-REPORT footnote
        that reads ``critic.nominated_relation`` - and a caller that means to
        record it records it under a name of its own.
        """

        return {
            "relation": self.relation,
            "passage_quote": self.passage_quote,
            "role_bindings": self.role_bindings.as_dict(),
            "case": self.case,
            OUTSIDE_VOCABULARY_FIELD: self.outside_vocabulary,
        }


@dataclass(frozen=True)
class DefenderOutput:
    """The defence of the null: the juxtaposition establishes no relation."""

    answer: str
    concedes: bool

    def as_dict(self) -> dict[str, Any]:
        return {"answer": self.answer, "concedes": self.concedes}


@dataclass(frozen=True)
class JudgeRuling:
    """One seat's ruling. ``sustained`` is a label, never a quantity."""

    sustained: bool
    decisive_point: str
    reading_note: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "sustained": self.sustained,
            "decisive_point": self.decisive_point,
            "reading_note": self.reading_note,
        }


@dataclass(frozen=True)
class MarkerOutput:
    """One (cell, comparison, register) mark. One register per call (§2.3)."""

    mark: str
    difference_kind: str | None
    left_quote: str
    right_quote: str
    case: str

    @property
    def claims_difference(self) -> bool:
        return self.mark == DIFFERS_MARK

    def as_dict(self) -> dict[str, Any]:
        return {
            "mark": self.mark,
            "difference_kind": self.difference_kind,
            "left_quote": self.left_quote,
            "right_quote": self.right_quote,
            "case": self.case,
        }


@dataclass(frozen=True)
class VariatorOutput:
    """Paraphrases of the exchange. The material is never paraphrased."""

    paraphrases: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {"paraphrases": list(self.paraphrases)}


RoleOutput = (
    CriticOutput | DefenderOutput | JudgeRuling | MarkerOutput | VariatorOutput
)


@dataclass(frozen=True)
class Validation:
    """The structured outcome of :func:`check`. Never raised, always returned."""

    ok: bool
    role: str
    value: RoleOutput | None
    reason: str | None
    path: tuple[str, ...]
    message: str

    def raise_for_failure(self) -> RoleOutput:
        if self.ok and self.value is not None:
            return self.value
        raise SchemaInvalid(self.role, self.reason or "not-an-object",
                            self.message, self.path)


# --------------------------------------------------------------------- #
# Schemas (§2.3). Closed at every level; no numeric field anywhere.       #
# W0-STANDARD owns them (its deviation 6); they are imported above and     #
# re-exported here, and the standard body pins their digest.              #
# --------------------------------------------------------------------- #


def _is_role(role: Any) -> bool:
    """``role`` names a role. Typed before it is looked up: an unhashable
    argument (a list, a dict) used to raise ``TypeError`` out of the membership
    test itself, where the answer the caller is owed is ``unknown-role``."""

    return isinstance(role, str) and role in SCHEMAS


def _is_register(register: Any) -> bool:
    """``register`` names a C001 register; typed before it is looked up."""

    return isinstance(register, str) and register in DIFFERENCE_KINDS


def schema_for(role: str) -> dict[str, Any]:
    """A deep copy of ``role``'s schema, safe for a caller to embed or edit."""
    if not _is_role(role):
        raise SchemaInvalid(str(role), "unknown-role", f"no schema for role {role!r}")
    return copy.deepcopy(SCHEMAS[role])


def difference_kinds_for(register: str) -> tuple[str, ...]:
    """The closed ``difference_kind`` token set for one C001 register."""
    if not _is_register(register):
        raise SchemaInvalid("marker", "unknown-register",
                            f"no register {register!r}")
    return DIFFERENCE_KINDS[register]


# --------------------------------------------------------------------- #
# Guards                                                                 #
# --------------------------------------------------------------------- #


def assert_no_scoring_keys(value: Any, path: Sequence[str] = ()) -> None:
    """Raise :class:`ScoringKeyForbidden` if a scoring key appears anywhere.

    G12, over a **key structure**. Mappings are checked by key and descended;
    lists and tuples are descended by index. A nested ``str`` is a *value* and is
    not inspected: a scoring word in content is not a scoring key, and this guard
    never reads content.

    **A leaf whose type the guard does not know is refused.** A ``deque``, a
    generator, ``dict.values()``, a ``memoryview``, a ``set``: none of them is a
    mapping or a list, so the descent used to walk past them in silence, and a
    scoring key one attribute down was never looked at. The admissible leaves
    are exactly JSON's (``str``, ``bytes``, ``int``, ``float``, ``bool``,
    ``None``); anything else is a :class:`ContractError` telling the caller to
    hand over the record it would publish - ``as_dict()`` - rather than the
    object it holds it in.

    **A dataclass instance is descended, not refused.** Its field names are its
    keys, and the loop's own records are frozen dataclasses: refusing them would
    have made the guard unusable on exactly the values it is for, while walking
    past them is the hole. So the fields are scanned as keys and their values
    descended, and a ``score`` field is refused wherever it is spelled.

    Handing the whole guard a ``str`` or ``bytes`` is a different matter and is
    refused with :class:`ContractError`. G12's subjects are "every emitted
    artifact, **every table header and every rendered file**" (§2.4), and a
    rendered file passed here used to answer ``None`` in silence - so a
    ``READING_TABLE.md`` with a ``score`` column satisfied §5's protected
    obligation *p4* without being looked at. A rendered file is not a key
    structure: scan it with :func:`assert_no_scoring_headers`, which W0-STANDARD
    owns and this module re-exports.
    """
    if isinstance(value, (str, bytes, bytearray)):
        raise ContractError(
            CONTRACT_VIOLATION,
            f"{'/'.join(str(part) for part in path) or '<root>'}: "
            f"a {type(value).__name__} is a rendered file, not a key structure; "
            "scan it with assert_no_scoring_headers",
        )
    _scan_for_scoring_keys(value, path)


#: What a leaf of a key structure may be: JSON's own scalars. Anything else is
#: an object with an interior this guard cannot see into.
_SCANNABLE_LEAVES: tuple[type, ...] = (str, bytes, bool, int, float)


def _scan_for_scoring_keys(value: Any, path: Sequence[str] = ()) -> None:
    """The descent :func:`assert_no_scoring_keys` performs, keys only."""
    if isinstance(value, Mapping):
        for key, item in value.items():
            here = (*path, str(key))
            if str(key).lower() in FORBIDDEN_KEYS:
                raise ScoringKeyForbidden(here)
            _scan_for_scoring_keys(item, here)
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _scan_for_scoring_keys(item, (*path, str(index)))
    elif is_dataclass(value) and not isinstance(value, type):
        # A frozen record is a key structure written another way: its field
        # names are its keys, and they are scanned as such. Walking past it -
        # which is what "not a Mapping, not a list" used to mean - left a
        # ``score`` field unlooked at inside a record that would be published.
        for field in fields(value):
            here = (*path, field.name)
            if field.name.lower() in FORBIDDEN_KEYS:
                raise ScoringKeyForbidden(here)
            _scan_for_scoring_keys(getattr(value, field.name), here)
    elif value is None or isinstance(value, _SCANNABLE_LEAVES):
        return
    else:
        raise ContractError(
            CONTRACT_VIOLATION,
            f"{'/'.join(str(part) for part in path) or '<root>'}: "
            f"a {type(value).__name__} is not a key structure this guard can read; "
            "hand it the record you would publish (as_dict()) instead",
        )


#: The keywords whose presence means a schema is describing an **object**, so
#: that an object which does not close itself is refused whether or not it
#: bothered to enumerate any property. ``properties`` alone used to stand for
#: this, which is exactly how ``{"type": "object"}`` - which admits
#: ``{"total": 3}`` - passed the guard.
_OBJECT_KEYWORDS: frozenset[str] = frozenset({
    "properties", "patternProperties", "additionalProperties", "propertyNames",
    "dependentSchemas", "dependentRequired", "required", "minProperties",
    "maxProperties",
})

#: Sub-schemas reached by one name.
_SUBSCHEMA_KEYS: tuple[str, ...] = (
    "items", "contains", "not", "if", "then", "else", "propertyNames",
    "unevaluatedItems", "unevaluatedProperties", "additionalItems",
)

#: Sub-schemas reached by a list of them.
_SUBSCHEMA_LISTS: tuple[str, ...] = ("anyOf", "oneOf", "allOf", "prefixItems")

#: Sub-schemas reached through a mapping of name -> schema.
_SUBSCHEMA_MAPS: tuple[str, ...] = ("$defs", "definitions", "dependentSchemas",
                                    "patternProperties")


def _refuse_aggregate(path: Sequence[str], why: str) -> None:
    raise ContractError(CONTRACT_VIOLATION, f"{'/'.join(path) or '<root>'}: {why}")


def assert_no_aggregate_fields(schema: Any, path: Sequence[str] = ()) -> None:
    """Raise :class:`ContractError` if a schema could express an aggregate.

    A role output may name no quantity and hold none: no property name in
    :data:`FORBIDDEN_KEYS` or :data:`AGGREGATE_KEYS`, no ``number`` or
    ``integer`` type anywhere (including one enumerated by ``enum``/``const``
    with no ``type`` beside it), and no open object through which one could
    arrive.

    "Open" is the whole of the repair. Closedness used to be tested only where
    ``properties`` was present, so ``{"type": "object"}`` - which admits
    ``{"mean": 0.5}`` - passed; and the descent visited only ``items``,
    ``contains``, ``not`` and the four combinators, so a number hidden under
    ``patternProperties``, ``propertyNames``, ``if``/``then``/``else``,
    ``dependentSchemas`` or ``$defs`` was never looked at. Every one of those is
    now visited, and two constructs are refused outright rather than followed:

    * ``$ref`` - a role schema says what it admits in one place; a reference
      moves the answer somewhere this guard would have to resolve, and a
      remote one somewhere it cannot see at all.
    * ``patternProperties`` - a property name given as a pattern cannot be
      enumerated, so ``additionalProperties: false`` does not close the object
      against it.

    A boolean sub-schema is read as JSON Schema reads it: ``True`` admits
    anything (refused), ``False`` admits nothing (accepted).
    """
    if schema is True:
        _refuse_aggregate(path, "a schema of `true` admits any value, a number included")
    if schema is False or not isinstance(schema, Mapping):
        return
    if "$ref" in schema or "$dynamicRef" in schema:
        _refuse_aggregate(path, "a role schema is written in one place; $ref is refused")
    if "patternProperties" in schema:
        _refuse_aggregate(path, "patternProperties cannot be enumerated, so the "
                                "object is not closed")
    types = schema.get("type")
    for name in (types,) if isinstance(types, str) else tuple(types or ()):
        if name in ("number", "integer"):
            _refuse_aggregate(path, "numeric field in a role schema")
    for key in ("enum", "const"):
        if key not in schema:
            continue
        values = schema[key] if key == "enum" else [schema[key]]
        for value in values if isinstance(values, (list, tuple)) else []:
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                _refuse_aggregate(path, f"{key} admits the number {value!r}")
    if _OBJECT_KEYWORDS & set(schema) or types == "object" or (
            not isinstance(types, str) and "object" in tuple(types or ())):
        if schema.get("additionalProperties") is not False:
            _refuse_aggregate(path, "object schema is not closed")
    properties = schema.get("properties")
    if isinstance(properties, Mapping):
        for key, sub in properties.items():
            lowered = str(key).lower()
            if lowered in FORBIDDEN_KEYS or lowered in AGGREGATE_KEYS:
                _refuse_aggregate((*path, str(key)), "aggregate field name")
            assert_no_aggregate_fields(sub, (*path, str(key)))
    for key in _SUBSCHEMA_KEYS:
        if key in schema:
            assert_no_aggregate_fields(schema[key], (*path, key))
    for key in _SUBSCHEMA_LISTS:
        for index, sub in enumerate(schema.get(key, ()) or ()):
            assert_no_aggregate_fields(sub, (*path, key, str(index)))
    for key in _SUBSCHEMA_MAPS:
        entries = schema.get(key)
        if isinstance(entries, Mapping):
            for name, sub in entries.items():
                lowered = str(name).lower()
                if key != "$defs" and (lowered in FORBIDDEN_KEYS
                                       or lowered in AGGREGATE_KEYS):
                    _refuse_aggregate((*path, key, str(name)), "aggregate field name")
                assert_no_aggregate_fields(sub, (*path, key, str(name)))


# --------------------------------------------------------------------- #
# Validation                                                             #
# --------------------------------------------------------------------- #

#: One validator per role, built over a **deep copy** taken at import. The
#: schema objects W0-STANDARD publishes are ordinary nested dicts and lists
#: inside their ``MappingProxyType``, so ``CRITIC_SCHEMA["properties"]
#: ["relation"]["enum"].append("outperforms")`` used to change what
#: :func:`check` accepts for the rest of the process - a vocabulary widened at
#: run time, under a standard whose digest never moved. Validation now reads a
#: copy nobody holds a reference to; :func:`schema_for` stays the supported way
#: to get a schema you may edit, and it copies too.
_VALIDATORS: Mapping[str, Draft202012Validator] = MappingProxyType({
    role: Draft202012Validator(copy.deepcopy(schema)) for role, schema in SCHEMAS.items()
})


def _path_key(path: Any) -> tuple[tuple[int, Any], ...]:
    """An order over schema paths that reads an array index as a number.

    ``str(part)`` put ``paraphrases/10`` before ``paraphrases/2``, so "the first
    error" depended on how many items the list had. Integers sort among
    themselves and before names, which are compared as text.
    """

    return tuple((0, part) if isinstance(part, int) and not isinstance(part, bool)
                 else (1, str(part)) for part in path)


def _word_count(text: str) -> int:
    return len(text.split())


def _fail(role: str, reason: str, message: str,
          path: Sequence[str] = ()) -> Validation:
    return Validation(False, role, None, reason, tuple(path), message)


#: The deepest nesting a role's output may carry, counted in open brackets.
#: A **declared resource boundary**, not a judgement: it bounds the work one
#: malformed answer can ask of the parser, and it says nothing about any
#: material. Five levels is the deepest any shipped schema describes, and this
#: is two orders of magnitude above it, so no conforming output comes near.
#:
#: It exists because ``json.loads`` is recursive: without it, roughly a thousand
#: open brackets (about two kilobytes) raise ``RecursionError`` - not a
#: ``LoopError``, not a :class:`Validation` - out of :func:`check`, which
#: promises never to raise. The cell would then get no block at all.
MAX_JSON_NESTING = 500


class _DuplicateKey(Exception):
    """A JSON object named one key twice. Not a ``ValueError``: see below."""

    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__(key)


def _no_duplicate_keys(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
    """``object_pairs_hook`` that refuses a repeated key instead of keeping one.

    ``json.loads`` keeps the last of two spellings in silence, so an output
    carrying ``{"mark": "same", "mark": "differs"}`` validated as whichever the
    seat put second and the other was never seen. A record is what it says, not
    what a parser kept.
    """

    seen: set[str] = set()
    for key, _ in pairs:
        if key in seen:
            raise _DuplicateKey(key)
        seen.add(key)
    return dict(pairs)


def _nesting_depth(text: str) -> int:
    """The deepest run of open brackets outside a string literal.

    A cheap pre-parse scan: it over-counts nothing that matters (a bracket
    inside a string is skipped) and never recurses, so it can answer for input
    the parser itself could not survive.
    """

    depth = maximum = 0
    in_string = escaped = False
    for character in text:
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character in "[{":
            depth += 1
            maximum = max(maximum, depth)
        elif character in "]}":
            depth -= 1
    return maximum


def _as_object(role: str, raw: Any) -> tuple[dict[str, Any] | None, Validation | None]:
    if isinstance(raw, (str, bytes, bytearray)):
        try:
            text = raw if isinstance(raw, str) else bytes(raw).decode("utf-8")
        except UnicodeDecodeError as exc:
            return None, _fail(role, "not-json", f"output is not JSON: {exc}")
        depth = _nesting_depth(text)
        if depth > MAX_JSON_NESTING:
            return None, _fail(
                role, "not-json",
                f"output nests {depth} levels deep, past the declared boundary of "
                f"{MAX_JSON_NESTING}; it is not read")
        try:
            raw = json.loads(text, object_pairs_hook=_no_duplicate_keys)
        except _DuplicateKey as exc:
            return None, _fail(role, "unexpected-field",
                               f"the output names {exc.key!r} twice", (exc.key,))
        except RecursionError as exc:
            # Belt and braces: the boundary above is the declared refusal, and
            # this is the guarantee that check() returns rather than raises
            # whatever the interpreter's own limit happens to be today.
            return None, _fail(role, "not-json", f"output is not JSON: {exc!r}")
        except (ValueError, UnicodeDecodeError) as exc:
            return None, _fail(role, "not-json", f"output is not JSON: {exc}")
    if not isinstance(raw, dict):
        return None, _fail(role, "not-an-object",
                           f"output is {type(raw).__name__}, not an object")
    return raw, None


def _schema_failure(role: str, body: dict[str, Any]) -> Validation | None:
    """The first schema error, chosen deterministically (path, validator, text)."""
    errors = sorted(
        _VALIDATORS[role].iter_errors(body),
        key=lambda err: (
            _path_key(err.absolute_path),
            str(err.validator),
            err.message,
        ),
    )
    if not errors:
        return None
    error = errors[0]
    reason = _JSONSCHEMA_REASONS.get(str(error.validator), "wrong-type")
    path = [str(part) for part in error.absolute_path]
    if reason == "missing-field" and isinstance(error.instance, dict):
        missing = sorted(set(error.validator_value) - set(error.instance))
        path += missing[:1]
    elif reason == "unexpected-field" and isinstance(error.instance, dict):
        declared = set((error.schema or {}).get("properties", {}))
        path += sorted(set(error.instance) - declared)[:1]
    return _fail(role, reason, error.message, path)


def _word_limit_failure(role: str, body: Mapping[str, Any]) -> Validation | None:
    for (limit_role, field), limit in WORD_LIMITS.items():
        if limit_role != role:
            continue
        value = body.get(field, "")
        if isinstance(value, str) and _word_count(value) > limit:
            return _fail(role, "word-limit",
                         f"{field} is longer than {limit} words", (field,))
    return None


def _critic_failure(body: Mapping[str, Any]) -> Validation | None:
    if body["relation"] == NONE_RELATION or body[OUTSIDE_VOCABULARY_FIELD]:
        # §2.3: "none" ends the row at one call and a non-empty
        # outside_vocabulary forces unresolved. Neither reaches a transcript,
        # so neither owes a case or a passage.
        return None
    if not body["case"]:
        return _fail("critic", "case-required",
                     "a nominated relation needs a case", ("case",))
    if not body["passage_quote"]:
        return _fail("critic", "passage-quote-required",
                     "a nominated relation needs a passage to quote",
                     ("passage_quote",))
    return None


def _marker_failure(body: Mapping[str, Any],
                    register: str | None) -> Validation | None:
    kind = body["difference_kind"]
    if body["mark"] == DIFFERS_MARK:
        if kind is None:
            return _fail("marker", "difference-kind-required",
                         "a differs mark needs a difference_kind",
                         ("difference_kind",))
        admitted = ALL_DIFFERENCE_KINDS
        if register is not None:
            if not _is_register(register):
                return _fail("marker", "unknown-register",
                             f"no register {register!r}")
            admitted = DIFFERENCE_KINDS[register]
        if kind not in admitted:
            return _fail("marker", "difference-kind-unknown",
                         f"{kind!r} is not a difference_kind of "
                         f"register {register!r}", ("difference_kind",))
        for side in ("left_quote", "right_quote"):
            if not body[side]:
                return _fail("marker", "quote-required",
                             f"a differs mark needs {side}", (side,))
        return None
    if kind is not None:
        return _fail("marker", "difference-kind-forbidden",
                     f"a {body['mark']} mark carries no difference_kind",
                     ("difference_kind",))
    if register is not None and not _is_register(register):
        return _fail("marker", "unknown-register", f"no register {register!r}")
    return None


def _build(role: str, body: Mapping[str, Any]) -> RoleOutput:
    if role == "critic":
        return CriticOutput(
            relation=body["relation"],
            passage_quote=body["passage_quote"],
            role_bindings=RoleBindings(
                **{field: body["role_bindings"][field]
                   for field in ROLE_BINDING_FIELDS}),
            case=body["case"],
            outside_vocabulary=body[OUTSIDE_VOCABULARY_FIELD],
        )
    if role == "defender":
        return DefenderOutput(answer=body["answer"], concedes=body["concedes"])
    if role == "judge":
        return JudgeRuling(
            sustained=body["sustained"],
            decisive_point=body["decisive_point"],
            reading_note=body["reading_note"],
        )
    if role == "marker":
        return MarkerOutput(
            mark=body["mark"],
            difference_kind=body["difference_kind"],
            left_quote=body["left_quote"],
            right_quote=body["right_quote"],
            case=body["case"],
        )
    return VariatorOutput(paraphrases=tuple(body["paraphrases"]))


def check(role: str, raw: Any, *, register: str | None = None) -> Validation:
    """Validate ``raw`` as ``role``'s output and **return** the outcome.

    Never raises. A failure carries the reason (a member of
    :data:`SCHEMA_REASONS`), the path inside the output and a message. Pass
    ``register`` to hold a marker's ``difference_kind`` to that register's own
    closed token set instead of the union of all of them.

    A ``register`` that names no C001 register is ``unknown-register`` **for
    every role**, not only for the marker: a caller that passes one has asked a
    question about a register that does not exist, and answering ``ok`` to it
    would let a typo travel as a validated reading.
    """
    if not _is_role(role):
        return _fail(str(role), "unknown-role", f"no schema for role {role!r}")
    if register is not None and not _is_register(register):
        return _fail(role, "unknown-register", f"no register {register!r}")
    body, failure = _as_object(role, raw)
    if failure is not None:
        return failure
    assert body is not None
    # Sequential, not a comprehension: every check after the schema check
    # assumes the schema check passed, so none of them may be evaluated first.
    failure = _schema_failure(role, body)
    if failure is not None:
        return failure
    failure = _word_limit_failure(role, body)
    if failure is not None:
        return failure
    if role == "critic":
        failure = _critic_failure(body)
    elif role == "marker":
        failure = _marker_failure(body, register)
    if failure is not None:
        return failure
    return Validation(True, role, _build(role, body), None, (), "")


def validate(role: str, raw: Any, *, register: str | None = None) -> RoleOutput:
    """Validate ``raw`` as ``role``'s output, or raise :class:`SchemaInvalid`.

    G1: a schema-invalid output is a block. The exception names the reason; the
    caller maps it to one block code and registers nothing.
    """
    return check(role, raw, register=register).raise_for_failure()


#: One validator per schema, for a caller that holds a role rather than asks
#: for one. Each returns a :class:`Validation`; none raises. ``register=`` is
#: forwarded to :func:`check`, so a marker validated through this mapping can be
#: held to its own register's closed token set rather than to the seven-token
#: union (O11) - which it could not be while these lambdas took ``raw`` alone.
VALIDATORS: Mapping[str, Callable[..., Validation]] = MappingProxyType({
    role: (lambda raw, *, register=None, _role=role: check(_role, raw, register=register))
    for role in SCHEMAS
})


# Structural self-check: the schemas are well-formed, closed, and can express
# no aggregate. Deterministic and pure; it reads only this module's constants.
for _role, _schema in SCHEMAS.items():
    Draft202012Validator.check_schema(_schema)
    assert_no_aggregate_fields(_schema)
del _role, _schema
