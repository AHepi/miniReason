"""W1-SEATS - who occupies which seat, decided once and pinned.

Purpose
-------
Turn the endpoint registry (``src/minireason/data/endpoints.json``) plus one
declared :class:`~minireason.loop.types.SeatsConfig` into a frozen
:class:`SeatPlan`: a critic seat, a defender seat, two (or more) judge seats
carrying distinct ``family`` labels, and a variator seat.  The plan is a pure
function of ``(registry, config)`` - the same two inputs give the same seats,
byte for byte - and :meth:`SeatPlan.pins` renders it as the canonical seat
table that goes into ``plan.json`` under its own ``sha256``.

The module also owns the one place the per-credential ceiling of design 4.6 is
computed (:func:`key_cap_for`) and the one place the loop reaches the outer
gate (:func:`key_gate_for`), which is
``tools/multicycle_commitment_study_multi_v2.key_gate`` **imported, never
copied**.  The inner gate is ``provider_openai_compat.slots_for``, acquired by
the provider itself; the loop adds no third gate.

Design section
--------------
Section 2.2 (Seats), with section 4.6 (key handling and the 5-per-key gate) and
the ``W1-SEATS`` entry of the section 7 wave plan.  Section 2.2's rule, verbatim:
*drawn from* ``endpoints.json`` *by a deterministic rule pinned in* ``plan.json``
*before dispatch: sort by* ``(family, name)``\\ *, then assign.*

The assignment, stated once so no caller has to read the code:

1.  Order every endpoint by ``(family, name)``; order the families by name.
2.  **Judges** take the first endpoint - by sorted name - of each of the first
    *lineages* in sorted family order, one lineage per judge seat.  Two judge
    seats never share a lineage: a registry that cannot supply that many
    lineages is refused with :data:`FAMILY_COUNT_INSUFFICIENT` rather than
    quietly seating two judges of one model.
3.  **Critic** takes the first unseated endpoint whose lineage is none of the
    judge lineages.
4.  **Defender** takes the first unseated endpoint whose lineage is neither the
    critic's nor a judge's; failing that, the first whose lineage is merely not
    the critic's; failing that, the first unseated endpoint at all.
5.  **Variator** takes the first unseated endpoint.  Section 2.2 constrains its
    family to *any*, so it may share a lineage with a judge, and in the default
    plan over the shipped registry it does.
6.  Every step a registry could not satisfy is recorded as a :class:`Relaxation`
    and published in the seat table, because section 2.2 requires that "the
    record says when it could not".

A seat named in the config pins that seat instead, and the remaining seats are
assigned around it by the same rule.  Section 2.2's other half is enforced by
the digest: seat identity - endpoint name, model, family, ``key_env``,
``timeout_seconds`` (and ``max_concurrency``, see below) - is frozen into the
table, so substituting an endpoint mints a new ``loop_plan_id``, which is a new
pre-registration and never an amendment.

Nothing here ever compares two endpoints for merit.  Seats are occasions, not
contestants: the only orderings in this module are ``sorted`` over a family
label and ``sorted`` over an endpoint name, both of which exist so that two
runs agree, and ``tests/loop/test_seats.py`` scans this source to keep it so.

Deviations, and why
-------------------
*   **``max_tokens`` is not part of seat identity, because the registry has no
    such field.**  The wave brief lists it beside model and timeout, but
    ``provider_openai_compat.Endpoint`` declares ``name``, ``base_url``,
    ``model``, ``key_env``, ``family``, ``chat_path``, ``native``,
    ``max_concurrency`` and ``timeout_seconds`` and nothing else; ``max_tokens``
    is a *per-call* argument of ``OpenAICompatProvider``.  It cannot be pinned
    from the registry, so W2-ROLES must pin the ``max_tokens`` it passes into
    the call record, and this table pins what the registry actually declares.
*   **``max_concurrency`` is pinned although section 2.2's list stops at
    ``timeout_seconds``.**  It is the input to :func:`key_cap_for`, so a silent
    change to it would change an authorisation already pre-registered without
    minting a new plan.  Pinning it makes that impossible.
*   **The number of judge seats is ``seats.min_judge_families``** (default 2,
    so the default plan is section 2.2's pair).  ``SeatsConfig`` already refuses
    a ``judges`` list shorter than ``min_judge_families``, so one number
    governs both, and every judge family is distinct rather than merely
    "at least that many distinct".
*   **The marker has no seat of its own.**  Section 2.2 says it reuses the
    judge pair, so no second identity is minted for it and the table records
    the reuse instead: :meth:`SeatPlan.marker_seats` returns the judges.
*   **This module imports ``contracts.ROLE_NAMES``** although its wave-plan
    ``depends_on`` names only W0-TYPES.  The role vocabulary has one owner, and
    re-typing it here would create a rival table.
*   **Three codes this module introduced** - see :data:`NEW_CODES`.  They are
    declared here with their reasons and the wave-1 integrator folded them into
    ``types.FAILURE_CODES``, exactly as open question O9 prescribes.
*   **"Distinct family" is compared over the LINEAGE, not the label**
    (wave-1 integration decision 3).  ``endpoints.json`` spells a family as
    route-and-lineage together, so ``deepseek`` and ``ollama-cloud/deepseek``
    are two labels over one model; sorted family order puts them adjacent, so a
    label comparison would have seated deepseek on both judge seats and
    reported two distinct families.  :func:`lineage` strips the host route and
    every family comparison in the assignment is over its result.  The table
    publishes the labels *and* ``judge_lineages``, so a reader sees what was
    assigned and what was compared.  This moved the default table's ``sha256``;
    ``tests/loop/test_seats.py`` pins both the old and the new value, and a run
    pre-registered under the old one is a new ``loop_plan_id``, never an
    amendment.
"""

from __future__ import annotations

import importlib
import sys
import threading
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterator, Mapping

from deepreason_core.canonical import canonical_json, sha256_hex

from minireason.provider_openai_compat import ENDPOINTS_PATH, Endpoint, load_endpoints

from .contracts import ROLE_NAMES
from .types import LoopConfig, LoopError, SeatsConfig

__all__ = [
    "SEATS_SCHEMA",
    "REUSED_ROLES",
    "SEAT_ROLES",
    "SELECTION_RULE",
    "HOST_SEPARATOR",
    "lineage",
    "MAX_PER_KEY",
    "FAMILY_COUNT_INSUFFICIENT",
    "SEAT_COUNT_INSUFFICIENT",
    "REGISTRY_INVALID",
    "RUNNER_NOT_IMPORTABLE",
    "NEW_CODES",
    "SeatsRefused",
    "Relaxation",
    "Seat",
    "Registry",
    "SeatPlan",
    "load_registry",
    "select_seats",
    "require_cross_family_judges",
    "key_cap_for",
    "key_gate_for",
    "runner_module",
]

#: The schema name of the seat table :meth:`SeatPlan.pins` renders.
SEATS_SCHEMA = "minireason.loop.seats.v1"

#: Roles that reuse another role's seats rather than holding one of their own.
#: Section 2.2 gives the marker the judge pair, so it mints no second identity.
REUSED_ROLES: Mapping[str, str] = MappingProxyType({"marker": "judge"})

#: The roles that occupy a seat, in ``contracts.ROLE_NAMES``' own order. Derived
#: from that tuple rather than re-typed, so the role vocabulary keeps one owner.
SEAT_ROLES: tuple[str, ...] = tuple(role for role in ROLE_NAMES
                                    if role not in REUSED_ROLES)

#: Section 2.2's rule, recorded in the table so a reader of ``plan.json`` need
#: not read this module to know how the seats were arrived at.
SELECTION_RULE = "sorted family name, then sorted endpoint name"

#: The separator between the host route and the model lineage inside a
#: ``family`` label.  ``ollama-cloud/deepseek`` is the deepseek lineage reached
#: through the ollama-cloud route; ``deepseek`` is the same lineage reached
#: directly.
HOST_SEPARATOR = "/"


def lineage(family: str) -> str:
    """The model lineage a ``family`` label names, with the host route stripped.

    G0 wants two judge seats that are not the same model wearing two hats.
    ``endpoints.json`` labels a family by *route and lineage* together, so the
    registry's own ``family`` values ``deepseek`` and ``ollama-cloud/deepseek``
    are two labels over one lineage: seating both would satisfy a
    distinct-label test while seating deepseek twice, which is exactly what the
    cross-family rule exists to prevent.  The comparison is therefore over the
    lineage, and the *label* is still what the table publishes, so a reader can
    see both.  A label with no separator is its own lineage.
    """

    text = str(family)
    _, separator, tail = text.rpartition(HOST_SEPARATOR)
    return tail if separator and tail else text

#: The owner's authorisation, mirrored from runner v2 so importing this module
#: does not import the runner.  :func:`key_gate_for` asserts the agreement.
MAX_PER_KEY = 5

#: Declared in ``types.FAILURE_CODES``: the registry cannot supply one family
#: per judge seat, or a plan's judge seats do not carry distinct families.
FAMILY_COUNT_INSUFFICIENT = "FAMILY_COUNT_INSUFFICIENT"

#: NEW: the registry has fewer distinct endpoints than the plan has seats.
SEAT_COUNT_INSUFFICIENT = "SEAT_COUNT_INSUFFICIENT"

#: NEW: ``endpoints.json`` is unreadable, malformed, or of an unknown schema.
REGISTRY_INVALID = "REGISTRY_INVALID"

#: NEW: runner v2 - the outer key gate - could not be imported.
RUNNER_NOT_IMPORTABLE = "RUNNER_NOT_IMPORTABLE"

#: Codes this module raises that ``types.FAILURE_CODES`` does not yet declare,
#: each with the one-line reason the wave integrator needs to fold it in.
NEW_CODES: Mapping[str, str] = MappingProxyType({
    SEAT_COUNT_INSUFFICIENT:
        "the registry holds fewer distinct endpoints than the plan has seats, "
        "which FAMILY_COUNT_INSUFFICIENT does not say",
    REGISTRY_INVALID:
        "endpoints.json is missing, malformed or of an unknown schema_version, "
        "so no seat may be assigned from it",
    RUNNER_NOT_IMPORTABLE:
        "the outer key gate is runner v2's key_gate imported, not copied; if "
        "that module cannot be imported the loop refuses rather than building "
        "a third gate",
})


class SeatsRefused(LoopError):
    """A seat assignment the registry, the config or the process refuses.

    Carries ``(code, detail="")`` like every other wave-0 loop exception.
    """


def _fail(code: str, detail: str) -> SeatsRefused:
    return SeatsRefused(code, detail)


# --------------------------------------------------------------------------
# Records
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Relaxation:
    """One family constraint of section 2.2 the registry could not satisfy."""

    seat: str
    constraint: str
    reason: str

    def as_dict(self) -> dict[str, str]:
        return {"seat": self.seat, "constraint": self.constraint,
                "reason": self.reason}


@dataclass(frozen=True)
class Seat:
    """One occasion: a role, its index within that role, and the endpoint.

    The endpoint is held whole rather than copied field by field, so a seat's
    identity cannot drift from the registry entry it was drawn from.
    """

    role: str
    index: int
    endpoint: Endpoint

    def __post_init__(self) -> None:
        if self.role not in SEAT_ROLES:
            raise _fail("CONFIG_INVALID_VALUE",
                        f"{self.role!r} is not a seated role")
        if type(self.index) is not int or self.index < 0:
            raise _fail("CONFIG_INVALID_VALUE", "a seat index is a whole number")

    @property
    def name(self) -> str:
        return self.endpoint.name

    @property
    def model(self) -> str:
        return self.endpoint.model

    @property
    def family(self) -> str:
        return self.endpoint.family

    @property
    def lineage(self) -> str:
        """The family label with its host route stripped (see :func:`lineage`)."""

        return lineage(self.endpoint.family)

    @property
    def key_env(self) -> str:
        """The NAME of the environment variable the seat spends. Never a value."""

        return self.endpoint.key_env

    @property
    def timeout_seconds(self) -> int:
        return self.endpoint.timeout_seconds

    @property
    def max_concurrency(self) -> int:
        return self.endpoint.max_concurrency

    @property
    def native(self) -> bool:
        return self.endpoint.native

    @property
    def label(self) -> str:
        """``critic`` for a single seat, ``judge#1`` / ``judge#2`` for a pair."""

        return f"{self.role}#{self.index + 1}" if self.role == "judge" else self.role

    def identity(self) -> dict[str, Any]:
        """What the plan freezes: substituting any of it mints a new plan."""

        return {"name": self.name, "model": self.model, "family": self.family,
                "key_env": self.key_env, "timeout_seconds": self.timeout_seconds,
                "max_concurrency": self.max_concurrency}

    def as_dict(self) -> dict[str, Any]:
        record = {"role": self.role, "index": self.index, "label": self.label}
        record.update(self.identity())
        return record


@dataclass(frozen=True)
class Registry:
    """The endpoint registry, ordered the one way section 2.2 orders it."""

    endpoints: tuple[Endpoint, ...]

    def __post_init__(self) -> None:
        if not self.endpoints:
            raise _fail(REGISTRY_INVALID, "the registry declares no endpoint")
        names = [endpoint.name for endpoint in self.endpoints]
        if len(set(names)) != len(names):
            raise _fail(REGISTRY_INVALID, "the registry repeats an endpoint name")
        object.__setattr__(self, "endpoints",
                           tuple(sorted(self.endpoints,
                                        key=lambda e: (e.family, e.name))))

    @classmethod
    def of(cls, source: "Registry | Mapping[str, Endpoint] | Any") -> "Registry":
        """Accept a :class:`Registry`, a ``{name: Endpoint}`` map, or a sequence."""

        if isinstance(source, Registry):
            return source
        if isinstance(source, Mapping):
            values = tuple(source.values())
        else:
            try:
                values = tuple(source)
            except TypeError as exc:
                raise _fail(REGISTRY_INVALID,
                            "a registry is a mapping or a sequence of endpoints") from exc
        for endpoint in values:
            if not isinstance(endpoint, Endpoint):
                raise _fail(REGISTRY_INVALID,
                            "every registry entry is a provider Endpoint")
        return cls(values)

    def __len__(self) -> int:
        return len(self.endpoints)

    def __iter__(self) -> Iterator[Endpoint]:
        return iter(self.endpoints)

    def __contains__(self, name: object) -> bool:
        return any(endpoint.name == name for endpoint in self.endpoints)

    def __getitem__(self, name: str) -> Endpoint:
        for endpoint in self.endpoints:
            if endpoint.name == name:
                return endpoint
        raise _fail("CONFIG_INVALID_VALUE",
                    f"the registry carries no endpoint named {name!r}")

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(endpoint.name for endpoint in self.endpoints)

    @property
    def families(self) -> tuple[str, ...]:
        return tuple(sorted({endpoint.family for endpoint in self.endpoints}))

    @property
    def key_envs(self) -> tuple[str, ...]:
        """Every credential NAME the registry spends, sorted. Never a value."""

        return tuple(sorted({endpoint.key_env for endpoint in self.endpoints}))

    @property
    def lineages(self) -> tuple[str, ...]:
        """Every distinct model lineage the registry can seat, sorted."""

        return tuple(sorted({lineage(e.family) for e in self.endpoints}))

    def in_family(self, family: str) -> tuple[Endpoint, ...]:
        return tuple(e for e in self.endpoints if e.family == family)

    def view(self) -> list[dict[str, Any]]:
        """The registry as the plan is allowed to describe it: no credential."""

        return [{"name": e.name, "model": e.model, "family": e.family,
                 "key_env": e.key_env, "timeout_seconds": e.timeout_seconds,
                 "max_concurrency": e.max_concurrency, "native": e.native}
                for e in self.endpoints]

    @property
    def digest(self) -> str:
        return sha256_hex(canonical_json(self.view()))


def load_registry(path: Path | str = ENDPOINTS_PATH) -> Registry:
    """Read ``endpoints.json`` into an ordered :class:`Registry`.

    Loading goes through ``provider_openai_compat.load_endpoints``, so the
    registry the seats are drawn from is the same object the transport uses;
    every way that can fail becomes :data:`REGISTRY_INVALID`.
    """

    try:
        loaded = load_endpoints(path)
    except (OSError, ValueError, TypeError) as exc:
        raise _fail(REGISTRY_INVALID, f"{path}: {exc}") from exc
    return Registry.of(loaded)


@dataclass(frozen=True)
class SeatPlan:
    """The frozen seat table of one ``loop_plan_id``."""

    critic: Seat
    defender: Seat
    judges: tuple[Seat, ...]
    variator: Seat
    max_per_key: int = MAX_PER_KEY
    relaxations: tuple[Relaxation, ...] = ()
    registry_digest: str = ""
    families: tuple[str, ...] = field(default=())

    @property
    def seats(self) -> tuple[Seat, ...]:
        """Every seat, in ``SEAT_ROLES`` order."""

        return (self.critic, self.defender) + self.judges + (self.variator,)

    @property
    def judge_families(self) -> tuple[str, ...]:
        return tuple(seat.family for seat in self.judges)

    @property
    def judge_lineages(self) -> tuple[str, ...]:
        """The judge seats' lineages - the values the cross-family rule compares."""

        return tuple(seat.lineage for seat in self.judges)

    def marker_seats(self) -> tuple[Seat, ...]:
        """Section 2.2: the marker reuses the judge pair and mints no seat."""

        return self.judges

    def for_role(self, role: str, index: int = 0) -> Seat:
        """One seat by role; ``marker`` resolves to the judge at that index."""

        resolved = REUSED_ROLES.get(role, role)
        if resolved == "judge":
            if not 0 <= index < len(self.judges):
                raise _fail("CONFIG_INVALID_VALUE",
                            f"the plan has no judge seat at index {index}")
            return self.judges[index]
        if resolved not in SEAT_ROLES:
            raise _fail("CONFIG_INVALID_VALUE", f"{role!r} is not a seated role")
        if index != 0:
            raise _fail("CONFIG_INVALID_VALUE", f"{resolved} holds one seat")
        return getattr(self, resolved)

    def key_envs(self) -> dict[str, list[str]]:
        """Credential NAME -> the endpoint names seated on it, both sorted."""

        grouped: dict[str, list[str]] = {}
        for seat in self.seats:
            grouped.setdefault(seat.key_env, []).append(seat.name)
        return {key: sorted(set(names)) for key, names in sorted(grouped.items())}

    def table(self) -> dict[str, Any]:
        """The seat table body - everything but its own digest."""

        return {
            "schema": SEATS_SCHEMA,
            "rule": SELECTION_RULE,
            "families": list(self.families),
            "registry_sha256": self.registry_digest,
            "max_per_key": self.max_per_key,
            "seats": {
                "critic": self.critic.identity(),
                "defender": self.defender.identity(),
                "judge": [seat.identity() for seat in self.judges],
                "variator": self.variator.identity(),
            },
            "reused_roles": dict(REUSED_ROLES),
            "judge_families": list(self.judge_families),
            "judge_lineages": list(self.judge_lineages),
            "key_envs": self.key_envs(),
            "key_caps": self.key_caps(),
            "relaxations": [r.as_dict() for r in self.relaxations],
        }

    def seats_on(self, key_env: str) -> tuple[Seat, ...]:
        """Every seat spending ``key_env``, in table order."""

        found = tuple(seat for seat in self.seats if seat.key_env == key_env)
        if not found:
            raise _fail("CONFIG_INVALID_VALUE", f"no seat spends {key_env}")
        return found

    def key_caps(self) -> dict[str, int]:
        """Credential NAME -> the in-flight ceiling in force for it.

        The lowest ceiling any seat on that credential declares, exactly as
        runner v2's ``key_caps`` takes the lowest: a plan may not state an
        authorisation wider than the narrowest endpoint spending the key.
        """

        return {key: min(key_cap_for(seat, self.max_per_key)
                         for seat in self.seats_on(key))
                for key in sorted(self.key_envs())}

    def canonical_bytes(self) -> bytes:
        return canonical_json(self.table())

    @property
    def digest(self) -> str:
        return sha256_hex(self.canonical_bytes())

    def pins(self) -> dict[str, Any]:
        """The canonical seat table plus its ``sha256``, for ``plan.json``.

        The digest covers :meth:`table` - the body without the digest - so a
        reader recomputes it by dropping ``sha256`` and hashing the canonical
        JSON of what remains.
        """

        pinned = self.table()
        pinned["sha256"] = self.digest
        return pinned

    def as_dict(self) -> dict[str, Any]:
        """The fuller record, for a receipt rather than for the plan digest."""

        return {"seats": [seat.as_dict() for seat in self.seats],
                "relaxations": [r.as_dict() for r in self.relaxations],
                "pins": self.pins()}


# --------------------------------------------------------------------------
# Selection
# --------------------------------------------------------------------------


def _seats_config(config: Any) -> tuple[SeatsConfig, int]:
    """Accept ``None``, a LoopConfig, a SeatsConfig, or either as a mapping.

    A mapping carrying ``seats`` or ``max_per_key`` is read as a loop config
    body; any other mapping is read as the ``seats`` block itself.  Either way
    validation is ``types``', so a config that loads here loads there.
    """

    if config is None:
        return SeatsConfig(), MAX_PER_KEY
    if isinstance(config, LoopConfig):
        return config.seats, config.max_per_key
    if isinstance(config, SeatsConfig):
        return config, MAX_PER_KEY
    if not isinstance(config, Mapping):
        raise _fail("CONFIG_NOT_A_MAPPING",
                    "a seat config is a LoopConfig, a SeatsConfig or a mapping")
    if "seats" in config or "max_per_key" in config:
        return (SeatsConfig.from_mapping(config.get("seats", {})),
                _cap(config.get("max_per_key", MAX_PER_KEY)))
    return SeatsConfig.from_mapping(config), MAX_PER_KEY


def _cap(value: Any) -> int:
    if type(value) is not int or not 1 <= value <= MAX_PER_KEY:
        raise _fail("CONFIG_INVALID_VALUE",
                    f"max_per_key is a whole number from 1 to {MAX_PER_KEY}")
    return value


def _pinned(registry: Registry, name: str | None, where: str,
            taken: dict[str, str]) -> Endpoint | None:
    if name is None:
        return None
    endpoint = registry[name]
    if endpoint.name in taken:
        raise _fail("CONFIG_INVALID_VALUE",
                    f"{where} names {name!r}, already seated as {taken[endpoint.name]}")
    taken[endpoint.name] = where
    return endpoint


def _first(registry: Registry, taken: Mapping[str, str],
           avoid: frozenset[str]) -> Endpoint | None:
    """The first endpoint in ``(family, name)`` order that is free and allowed.

    ``avoid`` holds **lineages**, not family labels: two routes to one lineage
    are one lineage here (see :func:`lineage`).
    """

    for endpoint in registry:
        if endpoint.name in taken or lineage(endpoint.family) in avoid:
            continue
        return endpoint
    return None


def _assign(registry: Registry, taken: dict[str, str], role: str,
            attempts: tuple[tuple[frozenset[str], str, str], ...],
            relaxations: list[Relaxation]) -> Endpoint:
    """Try each family constraint in turn, recording every one that gave way."""

    for position, (avoid, constraint, reason) in enumerate(attempts):
        endpoint = _first(registry, taken, avoid)
        if endpoint is not None:
            for skipped in attempts[:position]:
                relaxations.append(Relaxation(role, skipped[1], skipped[2]))
            taken[endpoint.name] = role
            return endpoint
    raise _fail(SEAT_COUNT_INSUFFICIENT,
                f"the registry has no endpoint left for the {role} seat")


def _judges(registry: Registry, taken: dict[str, str], wanted: int,
            pinned: tuple[str, ...], avoid: frozenset[str],
            relaxations: list[Relaxation]) -> tuple[Endpoint, ...]:
    """One endpoint per lineage, over the first families in sorted order.

    ``avoid`` and the distinctness test are over :func:`lineage`, so
    ``deepseek`` and ``ollama-cloud/deepseek`` are one lineage and never take
    two judge seats between them.  The published table still names the family
    labels, and :attr:`SeatPlan.judge_lineages` names what was compared.
    """

    if pinned:
        chosen = tuple(registry[name] for name in pinned)
        seen = [lineage(endpoint.family) for endpoint in chosen]
        if len(set(seen)) != len(seen):
            raise _fail(FAMILY_COUNT_INSUFFICIENT,
                        "seats.judges names two judge seats of one lineage")
        if len(chosen) < wanted:
            raise _fail(FAMILY_COUNT_INSUFFICIENT,
                        f"seats.judges names {len(chosen)} seats, not {wanted}")
        return chosen
    for excluded, relaxed in ((avoid, False), (frozenset(), True)):
        chosen: list[Endpoint] = []
        lineages: set[str] = set()
        for endpoint in registry:
            here = lineage(endpoint.family)
            if endpoint.name in taken or here in lineages or here in excluded:
                continue
            chosen.append(endpoint)
            lineages.add(here)
            if len(chosen) == wanted:
                break
        if len(chosen) == wanted:
            if relaxed and avoid:
                relaxations.append(Relaxation(
                    "judge", "family-distinct-from-the-pinned-seats",
                    "the registry has too few lineages to keep every judge out "
                    "of a lineage the config pinned"))
            for endpoint in chosen:
                taken[endpoint.name] = "judge"
            return tuple(chosen)
    raise _fail(FAMILY_COUNT_INSUFFICIENT,
                f"the registry declares {len(registry.lineages)} lineages over "
                f"{len(registry.families)} family labels and {wanted} judge "
                f"seats need {wanted} distinct lineages")


def select_seats(registry: "Registry | Mapping[str, Endpoint]",
                 config: Any = None) -> SeatPlan:
    """Assign every seat by section 2.2's rule. Pure in ``(registry, config)``.

    ``config`` may be ``None`` (every seat assigned), a
    :class:`~minireason.loop.types.LoopConfig`, a
    :class:`~minireason.loop.types.SeatsConfig`, or either one as a mapping.
    A seat the config names is pinned; the rest are assigned around it.
    """

    registry = Registry.of(registry)
    seats_config, max_per_key = _seats_config(config)
    taken: dict[str, str] = {}
    relaxations: list[Relaxation] = []

    for name in seats_config.judges:
        _pinned(registry, name, "judge", taken)
    critic = _pinned(registry, seats_config.critic, "critic", taken)
    defender = _pinned(registry, seats_config.defender, "defender", taken)
    variator = _pinned(registry, seats_config.variator, "variator", taken)

    wanted = len(seats_config.judges) or seats_config.min_judge_families
    if wanted < 2:
        raise _fail(FAMILY_COUNT_INSUFFICIENT,
                    "section 2.2 seats two judges from two distinct families")
    pinned_lineages = frozenset(
        lineage(endpoint.family) for endpoint in (critic, defender)
        if endpoint is not None)
    judges = _judges(registry, taken, wanted, seats_config.judges,
                     pinned_lineages, relaxations)
    judge_lineages = frozenset(lineage(endpoint.family) for endpoint in judges)

    if critic is None:
        critic = _assign(registry, taken, "critic", (
            (judge_lineages, "family-distinct-from-every-judge",
             "every lineage outside the judge seats was already seated"),
            (frozenset(), "", ""),
        ), relaxations)
    elif lineage(critic.family) in judge_lineages:
        relaxations.append(Relaxation(
            "critic", "family-distinct-from-every-judge",
            "the config pinned the critic into a judge lineage"))

    critic_lineage = lineage(critic.family)
    if defender is None:
        defender = _assign(registry, taken, "defender", (
            (judge_lineages | {critic_lineage},
             "family-distinct-from-the-critic-and-every-judge",
             "every lineage outside the critic and judge seats was already seated"),
            (frozenset({critic_lineage}), "family-distinct-from-the-critic",
             "the registry has no lineage left outside the critic's"),
            (frozenset(), "", ""),
        ), relaxations)
    elif lineage(defender.family) == critic_lineage:
        relaxations.append(Relaxation(
            "defender", "family-distinct-from-the-critic",
            "the config pinned the defender into the critic's lineage"))

    if variator is None:
        variator = _assign(registry, taken, "variator",
                           ((frozenset(), "", ""),), relaxations)

    plan = SeatPlan(
        critic=Seat("critic", 0, critic),
        defender=Seat("defender", 0, defender),
        judges=tuple(Seat("judge", index, endpoint)
                     for index, endpoint in enumerate(judges)),
        variator=Seat("variator", 0, variator),
        max_per_key=max_per_key,
        relaxations=tuple(relaxations),
        registry_digest=registry.digest,
        families=registry.families,
    )
    require_cross_family_judges(plan)
    return plan


def require_cross_family_judges(plan: "SeatPlan | Mapping[str, Any]") -> tuple[str, ...]:
    """Refuse a plan whose judge seats do not carry distinct families.

    Accepts a :class:`SeatPlan`, the mapping :meth:`SeatPlan.pins` renders, or
    a whole ``plan.json`` body carrying that mapping under ``seats``, so
    PREFLIGHT can check the frozen plan without rebuilding it.  Returns the
    judge families on success.
    """

    families = _judge_families(plan)
    if len(families) < 2:
        raise _fail(FAMILY_COUNT_INSUFFICIENT,
                    "section 2.2 seats two judges from two distinct families; "
                    f"this plan has {len(families)}")
    lineages = tuple(lineage(family) for family in families)
    if len(set(lineages)) != len(lineages):
        raise _fail(FAMILY_COUNT_INSUFFICIENT,
                    f"two judge seats share the lineage {lineages!r} "
                    f"(family labels {families!r})")
    return families


def _judge_families(plan: Any) -> tuple[str, ...]:
    if isinstance(plan, SeatPlan):
        return plan.judge_families
    if not isinstance(plan, Mapping):
        raise _fail("CONFIG_NOT_A_MAPPING", "a seat plan is a SeatPlan or a mapping")
    body = plan
    for _ in range(2):
        if "judge_families" in body:
            declared = body["judge_families"]
            if isinstance(declared, (str, bytes)):
                # ``tuple("ollama")`` is six one-character families, two of them
                # distinct, so a plan that spelled one family as a bare string
                # passed the cross-family rule (wave-1 integration decision 49).
                raise _fail(
                    "CONFIG_INVALID_VALUE",
                    "judge_families is a sequence of family labels, not a string")
            if not isinstance(declared, (list, tuple)):
                raise _fail("CONFIG_INVALID_VALUE",
                            "judge_families must be a list of family labels")
            return tuple(declared)
        if "seats" in body and isinstance(body["seats"], Mapping):
            judges = body["seats"].get("judge")
            if isinstance(judges, (list, tuple)):
                return tuple(entry.get("family", "") if isinstance(entry, Mapping)
                             else "" for entry in judges)
            body = body["seats"]
            continue
        break
    raise _fail("CONFIG_MISSING_KEY", "the plan carries no judge seats")


# --------------------------------------------------------------------------
# The 5-per-key gate (design 4.6) - imported, never copied
# --------------------------------------------------------------------------

_RUNNER_NAME = "tools.multicycle_commitment_study_multi_v2"
_RUNNER_RELATIVE = "tools/multicycle_commitment_study_multi_v2.py"
_RUNNER_LOCK = threading.Lock()
_RUNNER: Any = None


def _repository_root() -> Path | None:
    """The checkout this package was imported from, if it carries the runner."""

    root = Path(__file__).resolve().parents[3]
    return root if (root / _RUNNER_RELATIVE).is_file() else None


def runner_module() -> Any:
    """Runner v2, imported under its one canonical name.

    One process must hold one gate registry, so the module is imported as
    ``tools.multicycle_commitment_study_multi_v2`` and never loaded a second
    time under another name.  If the repository root is not importable the
    checkout's root is put on ``sys.path`` first - a documented side effect,
    taken lazily on the first gate acquisition rather than at import.
    """

    global _RUNNER
    with _RUNNER_LOCK:
        if _RUNNER is not None:
            return _RUNNER
        try:
            _RUNNER = importlib.import_module(_RUNNER_NAME)
            return _RUNNER
        except ImportError:
            pass
        root = _repository_root()
        if root is not None and str(root) not in sys.path:
            sys.path.insert(0, str(root))
        try:
            _RUNNER = importlib.import_module(_RUNNER_NAME)
        except ImportError as exc:
            raise _fail(RUNNER_NOT_IMPORTABLE,
                        f"{_RUNNER_RELATIVE} is the loop's outer key gate and "
                        f"may not be reimplemented: {exc}") from exc
        return _RUNNER


def key_cap_for(seat: Seat, max_per_key: int = MAX_PER_KEY) -> int:
    """The in-flight ceiling for this seat's credential (design 4.6).

    The lowest of the owner's five, the plan's ``max_per_key`` and the
    endpoint's own ``max_concurrency``: one number, used by both gates, so the
    outer gate and ``provider_openai_compat.slots_for`` can never disagree.
    """

    if not isinstance(seat, Seat):
        raise _fail("CONFIG_INVALID_VALUE", "key_cap_for takes a Seat")
    return min(MAX_PER_KEY, _cap(max_per_key), seat.max_concurrency)


def key_gate_for(seat: Seat, max_per_key: int = MAX_PER_KEY) -> threading.BoundedSemaphore:
    """The outer per-credential gate this seat's calls are held by.

    This is ``multicycle_commitment_study_multi_v2.key_gate`` itself - the same
    module-level registry runner v2's own waves acquire - so a reading call and
    a dispatch call in flight together are held to five per credential between
    them.  The inner gate is ``provider_openai_compat.slots_for``, acquired by
    the provider; the loop adds no third gate.

    **Source checkout only** (wave-1 integration decision 49).  Runner v2 lives
    in ``tools/``, which no wheel ships: an installed ``minireason`` cannot
    import it, and :func:`runner_module` raises ``RUNNER_NOT_IMPORTABLE``
    rather than substituting a gate of this module's own.  A loop run is a
    run from a checkout, and PREFLIGHT asserts it.
    """

    runner = runner_module()
    if runner.MAX_PER_KEY != MAX_PER_KEY:
        raise _fail("CONCURRENCY_LIMIT_CONFLICT",
                    f"runner v2 authorises {runner.MAX_PER_KEY} per credential, "
                    f"this module says {MAX_PER_KEY}")
    try:
        return runner.key_gate(seat.key_env, key_cap_for(seat, max_per_key))
    except ValueError as exc:
        raise _fail("CONCURRENCY_LIMIT_CONFLICT",
                    f"{seat.key_env}: {exc}") from exc
