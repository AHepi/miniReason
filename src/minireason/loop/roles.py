"""W2-ROLES - one call per seat, recorded once, never retried.

Purpose
-------
The one place the loop speaks to a model.  Five callers - :func:`call_critic`,
:func:`call_defender`, :func:`call_judge`, :func:`call_variator`,
:func:`call_marker` - each take a rendered pack (bytes plus its digest) and a
:class:`~minireason.loop.seats.Seat`, acquire the two concurrency gates in one
fixed order, hand the pack to ``provider_openai_compat`` under a strict JSON
response format, validate the reply through ``contracts``, write one write-once
call record, and return a typed :class:`RoleResult`.

Four things this module does *not* do, each of them load-bearing:

*   **It never retries.**  One :func:`call_role` is one ``provider.complete``.
    A re-ask is a different coordinate (``…#repair1``), it is budgeted, and the
    budget is ``0`` - so at the pre-registered standard a re-ask is refused
    outright (:data:`ROLE_REPAIR_REFUSED`).  Retrying until something validates
    is the failure mode the whole design exists to make impossible.
*   **It never raises for a provider failure.**  A route that does not answer is
    a delivery fact, not a reading: the caller gets a ``RoleResult`` carrying
    ``blocked:provider`` and the transport's own code, and the cell stays
    unresolved.  Exceptions here name plan errors only - a role that is not a
    role, a coordinate already spent, a pack that cannot be sent.
*   **It registers nothing.**  W1-GRAPH owns the graph; this module writes one
    JSON record under ``records_dir`` and hands back what was said.
*   **It persists no reasoning text.**  The transport already refuses to
    (``CallResult.reasoning_content_persisted`` is a constant ``False``), and
    this record carries only the *presence* flag and the token count where the
    provider reported one - never the text, and never a digest of a text this
    module was never given.

Design section
--------------
Section 2.3 (prompt contracts and JSON schemas), section 2.4 G1 (schema) and
G12 (no scoring key), section 4.6 (key handling and the 5-per-key gate), and the
``W2-ROLES`` entry of the section 7 wave plan.  Wave-1 interface seats Q1, Q5
and Q7 are answered here in full; Q4 (the marker has no seat) is obeyed by
refusing any seat for ``marker`` that is not the judge seat
``SeatPlan.for_role("marker", i)`` hands out.

The two gates, in **one fixed order** (Q5, design 4.6)
------------------------------------------------------
1.  ``seats.key_gate_for(seat, max_per_key)`` - runner v2's own
    ``key_gate``, *imported, never copied*, so a reading call and a dispatch
    call in flight together are held to five per credential between them.
2.  ``provider_openai_compat.slots_for(key_env, max_concurrency)`` - acquired
    by ``OpenAICompatProvider`` itself, inside ``complete``.

Outer first, inner second, always: two acquirers taking one pair of locks in two
orders is the textbook deadlock, and both gates are keyed by ``key_env``, so a
seat waiting on the inner gate while holding the outer one is the only ordering
in which nothing can wait on a holder of its own successor.  **The loop adds no
third gate**, and :data:`GATE_ORDER` names the two so that a reader does not
have to take it on trust.  ``tests/loop/test_roles.py`` scans this source for a
semaphore construction and fails if one appears.

Per-seat ``max_tokens``, and the arithmetic behind it (Q1 and Q7)
----------------------------------------------------------------
``max_tokens`` is a **per-call** argument of the transport, not a registry
field, so it cannot be part of seat identity (seats' own first deviation).  It
is therefore pinned *per seat* into the plan and into **every** call record,
where a changed bound is visible in a diff even though the seat table cannot
carry it.

It is chosen against the **300 s gateway wall**, not against the endpoint's
declared ``timeout_seconds``.  The Ollama cloud host closes any request still
open at 300 s whatever the endpoint declares (observed four times on
2026-09-14: F002 occurrence-01 ``glm-5.3`` at 300,270 ms, and three ``kimi-k3``
calls closed 300-301 s after their requests).  So the wall in force for a seat
is ``min(seat.timeout_seconds, 300)`` - **the smaller of the two, never the
larger**: neither this number nor ``timeouts.step_seconds`` may be used to raise
the plan's section 4.4 layer-1 timeout, which stays the endpoint's own
declaration and is what ``TIMEOUT_NOT_APPLIED`` guards.

Of that wall this module lets generation claim
:data:`GENERATION_SHARE` = 0.5.  The other half is prompt evaluation, the queue
behind the per-credential gate, TLS setup and the response body - none of which
this module can measure, so it takes half and says so rather than pretending the
whole wall is available to the decoder.  At the observed
:data:`OBSERVED_TOKENS_PER_SECOND` = 90 tokens/s (the floor of the observed
90-100 band; taking the floor makes the estimate conservative in the one
direction that matters):

    wall_ceiling(seat) = floor( min(timeout_seconds, 300) x 0.5 x 90 )

    shipped registry, timeout_seconds = 180  ->  floor(90 x 90)  = 8100 tokens
    synthetic fixture, timeout_seconds =  30  ->  floor(15 x 90)  = 1350 tokens

The **role budget** is derived from the role's own contract - the word limits
``contracts.WORD_LIMITS`` publishes, plus the quoted material each schema
carries - at a conservative 1.6 tokens per English word (byte-pair encoders
average 1.3-1.5 on prose; 1.6 leaves room for punctuation and for the JSON
escaping of a quoted span), plus 64 tokens of JSON scaffolding, rounded **up**
to the next power of two:

    role       contract content                                  words  x1.6  +64   pinned
    critic     case 400 + passage_quote 200 + 4 bindings 160       800   1280  1344  2048
               + relation/outside_vocabulary 40
    defender   answer 400 + concedes                               410    656   720  1024
    judge      decisive_point <= case+answer 800 + note 120        920   1472  1536  2048
    marker     case 120 + left_quote 120 + right_quote 120         370    592   656  1024
               + mark/difference_kind 10
    variator   paraphrase_n (2) x (case + answer) 800 each        1600   2560  2624  4096

and what each pinned bound costs against the two walls:

    role       pinned  / 90 tok/s   of the 180 s declared wall   of the 300 s gateway wall
    critic      2048     22.8 s              12.6 %                       7.6 %
    defender    1024     11.4 s               6.3 %                       3.8 %
    judge       2048     22.8 s              12.6 %                       7.6 %
    marker      1024     11.4 s               6.3 %                       3.8 %
    variator    4096     45.5 s              25.3 %                      15.2 %

The variator's entry is not a free number: it is
``paraphrase_n x`` :data:`VARIATOR_TOKENS_PER_PARAPHRASE`, and
:data:`VARIATOR_TOKENS_PER_PARAPHRASE` = 2048 is one paraphrase of a full
case+answer exchange at the same 1.6 tokens/word.  At the pre-registered
``paraphrase_n = 2`` that is the 4096 in the table; a successor standard that
raises ``paraphrase_n`` re-derives the bound through
:func:`max_tokens_for`, and - because a raised ``paraphrase_n`` is a new
``loop_plan_id`` - it is re-pre-registered with it.

The bound actually sent is ``min(role_budget, wall_ceiling(seat))``, and
:class:`TokenBound` carries every term of the arithmetic into the call record,
so the number carries its own account exactly as an audit threshold does.  A
seat so tight that the ceiling falls below :data:`MIN_MAX_TOKENS` = 256 - fewer
tokens than the smallest conforming reply of any role - is refused with
:data:`ROLE_TOKEN_BUDGET_UNREACHABLE` rather than dispatched to be truncated.

The response format, and the mode the record names
--------------------------------------------------
Where the endpoint supports it the call goes out as
``response_format={"type": "json_schema", "json_schema": {..., "strict": true}}``
carrying ``contracts.schema_for(role)`` itself - already closed
(``additionalProperties: false``, every property required), so it is a strict
schema without an edit.  A **native** Ollama endpoint gets the same object; the
transport's ``_native_format`` unwraps it to Ollama's ``format`` field.  A
``deepseek``-family endpoint gets ``{"type": "json_object"}`` instead, because
DeepSeek's OpenAI-compatible surface documents JSON *mode* and not strict JSON
*schema*; the transport's own ``_check_json_mode_prompt`` exists for exactly
that endpoint, and this module refuses a pack that would trip it
(:data:`ROLE_PACK_NOT_JSON_MODE_READY`) rather than appending words of its own
to a pack whose bytes are pinned by a digest.  Either way the mode is recorded
as ``settings.response_format_mode``, so no reader has to infer from the family
label what contract the reply was asked under.

A **marker** call carries the register's own closed ``difference_kind`` token
set on the wire, not the seven-token union (wave-0 open question O11): the seat
never sees another register's vocabulary, which is section 2.3's "never sees
more than one register, so no call can trade registers off" made structural
rather than instructional.

What the record carries, and who reads it
-----------------------------------------
One ``call.json`` per coordinate, written with ``custody.write_new`` - so it is
write-once, it is refused if it carries a credential, and a second call on a
spent coordinate is :data:`NO_REPLAY` **before** the provider is built.  The
coordinate directory is created with ``mkdir(exist_ok=False)``, which is the
atomic claim: the evidence that a coordinate was spent exists before anything
could be sent.

The record carries ``record: "call_record"`` beside its ``schema``, and the
three fields ``obligations.write_once_no_replay`` (p5) reads - ``coordinate``,
``digest`` and ``replay_of``.  ``replay_of`` is present and **empty** rather
than absent, the same discipline ``losses_outside_p`` keeps: a register of
replays that says nothing is not the same as one that says none.  This module
does not import ``obligations``; the agreement is asserted by a test that
imports both, exactly as wave 1's two agreements are.

Deviations, and why
-------------------
*   **The wave-plan signature ``call_role(role, seat, pack, schema,
    records_dir, *, repair=0)`` is kept, but ``schema`` may only be the
    contract's own.**  ``None`` (the normal case) means
    ``contracts.schema_for(role)``, with the marker's register narrowing
    applied.  Anything else must compare equal to that, or it is
    :data:`ROLE_SCHEMA_NOT_THE_CONTRACT`.  A dispatcher free to substitute a
    schema is a second owner of the role contracts, and two owners is how a
    seat ends up answering a question nobody pre-registered.
*   **``coordinate`` is a required keyword, not a positional.**  The wave plan's
    signature has no coordinate, yet ``NO_REPLAY``, the repair suffix and the
    records layout are all keyed by one.  It is required rather than derived:
    deriving a coordinate from a pack digest would make two identical packs at
    two cells one coordinate.
*   **``max_tokens``, ``seed`` and ``temperature`` are pinned by this module,
    not by the caller.**  All three are recorded.  ``temperature`` is
    :data:`TEMPERATURE` = 0.0 and ``seed`` is derived from the coordinate token
    (:func:`seed_for`), so a repeat of one coordinate asks for the same
    sampling; neither is a guarantee of determinism from any provider, and the
    record says the seed was derived rather than declared.
*   **``thinking`` is sent as ``False`` on a ``deepseek``-family seat and is
    never sent to any other family.**  The control is DeepSeek's and the
    transport refuses it elsewhere; switching it off keeps native reasoning text
    from being generated at all, which is the cheapest way to honour "reasoning
    text is never persisted".  ``ollama-cloud/deepseek`` is a different family
    label and gets nothing, which is what the transport's own comparison does.
*   **A declared pack digest is recorded and compared, never enforced.**
    W2-PACKS' ``pack_sha`` is being written in the same wave and its convention
    is not yet fixed, so this module records ``pack_sha256`` (its own sha256 of
    the bytes it sent), ``pack_declared_digest`` and ``pack_digest_agrees``.
    A declared digest that is not 64 lowercase hex characters is
    :data:`ROLE_PACK_INVALID`; one that simply disagrees is a recorded fact for
    the integrator, not a refusal by a module that cannot yet know which of the
    two conventions is right.
*   **The 300 s gateway wall is named as a reason, not left as a bare transport
    error** (seats Q7's recommendation to W5-DRIVER, taken here because this is
    the first module that can see the elapsed time).  A
    ``TRANSPORT_OR_RESPONSE_ERROR`` whose call was open for at least
    ``300 - 5`` seconds is recorded with ``reason``
    :data:`PROVIDER_GATEWAY_WALL` and the transport's own code beside it as
    ``transport_code``.  The block code is still ``blocked:provider``; what
    changes is that the receipt can say *the route closed the socket at its
    wall* instead of *something went wrong*.
*   **Ten codes this module introduces** - see :data:`NEW_CODES`.  They are
    declared here with their reasons for the wave-2 integrator to fold into
    ``types.FAILURE_CODES``, exactly as open question O9 prescribes.
    :data:`PROVIDER_GATEWAY_WALL` is the one of the ten that no exception
    carries - it is a *reason* on a returned result - so it will need an
    ``UNREACHED`` entry beside ``HTTP_429`` and the transport's other codes.
    ``NO_REPLAY`` is **not** new and is **not** retyped here: ``types`` owns
    the spelling, this module imports it, and this module is the first thing in
    the package to raise it.
*   **The material is passed through byte-for-byte** (surface S7).  This module
    sends the pack it is handed and nothing else - one ``user`` message, no
    system preamble of its own - so the bytes reaching seat *n* are the bytes
    the pack renderer produced, and a test asserts it.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Mapping

from minireason.provider_openai_compat import (
    CallResult,
    Endpoint,
    OpenAICompatProvider,
    ProviderFailure,
)

from .contracts import (
    ROLE_NAMES,
    RoleOutput,
    Validation,
    assert_no_scoring_keys,
    check,
    difference_kinds_for,
    schema_for,
)
from .custody import digest as value_digest
from .custody import fenced, sha256_bytes, write_new
from .seats import MAX_PER_KEY, REUSED_ROLES, Seat, key_cap_for, key_gate_for
from .types import NO_REPLAY, LoopError, block_code

__all__ = [
    "ROLES_SCHEMA",
    "ROLES",
    "RECORD_FIELD",
    "RECORD_KIND",
    "GATE_ORDER",
    "GATE_HELD_BY",
    "MESSAGE_ROLE",
    "TEMPERATURE",
    "SCHEMA_REPAIR_BUDGET",
    "OBSERVED_TOKENS_PER_SECOND",
    "GATEWAY_WALL_SECONDS",
    "GATEWAY_WALL_TOLERANCE_SECONDS",
    "GENERATION_SHARE",
    "TOKENS_PER_WORD",
    "MIN_MAX_TOKENS",
    "ROLE_MAX_TOKENS",
    "VARIATOR_TOKENS_PER_PARAPHRASE",
    "JSON_SCHEMA_MODE",
    "JSON_OBJECT_MODE",
    "JSON_OBJECT_ONLY_FAMILIES",
    "SCHEMA_BLOCK",
    "PROVIDER_BLOCK",
    "STATUS_OK",
    "STATUS_BLOCKED",
    "ARM_ENDING_CODES",
    "NO_REPLAY",
    "PROVIDER_GATEWAY_WALL",
    "ROLE_UNKNOWN",
    "ROLE_SEAT_MISMATCH",
    "ROLE_COORDINATE_INVALID",
    "ROLE_PACK_INVALID",
    "ROLE_PACK_NOT_JSON_MODE_READY",
    "ROLE_SCHEMA_NOT_THE_CONTRACT",
    "ROLE_REGISTER_REQUIRED",
    "ROLE_REPAIR_REFUSED",
    "ROLE_TOKEN_BUDGET_UNREACHABLE",
    "NEW_CODES",
    "RoleRefused",
    "ProviderArmEnded",
    "Ref",
    "RolePack",
    "Coordinate",
    "TokenBound",
    "RoleResult",
    "role_pack",
    "seed_for",
    "max_tokens_for",
    "response_format_for",
    "provider_reason",
    "default_provider_factory",
    "call_role",
    "call_critic",
    "call_defender",
    "call_judge",
    "call_variator",
    "call_marker",
]


# --------------------------------------------------------------------------
# Vocabulary
# --------------------------------------------------------------------------

ROLES_SCHEMA = "minireason.loop.roles.v1"

#: The five seated roles, the same object ``contracts`` owns. Not retyped: a
#: second role vocabulary is a second thing to drift.
ROLES: tuple[str, ...] = ROLE_NAMES

#: Mirrored from ``obligations.RECORD_FIELD`` / ``RECORD_KINDS`` rather than
#: imported, so this module keeps the wave-plan dependency set it was built
#: from. ``tests/loop/test_roles.py`` imports both and asserts the mirror.
RECORD_FIELD = "record"
RECORD_KIND = "call_record"

#: The two gates, in the order they are acquired. Outer first, inner second.
GATE_ORDER: tuple[str, ...] = ("seats.key_gate_for", "provider_openai_compat.slots_for")

#: Who acquires each gate, recorded on every call (wave-1 integration decision
#: 42(c)).  The outer one is acquired **here**, in ``call_role``; the inner one
#: is acquired by ``OpenAICompatProvider.complete`` itself, and this module must
#: never acquire it a second time - two acquisitions of one semaphore for one
#: call halve the credential's real ceiling and nothing would say so.
#: ``OfflineProvider`` holds no inner gate at all, which is why the record says
#: who holds it rather than asserting that somebody does.
GATE_HELD_BY: Mapping[str, str] = MappingProxyType({
    "seats.key_gate_for": "minireason.loop.roles.call_role",
    "provider_openai_compat.slots_for":
        "provider_openai_compat.OpenAICompatProvider.complete",
})

#: The pack is sent as one message in this role. There is no system preamble:
#: the pack renderer is the only author of a prompt (design 2.3).
MESSAGE_ROLE = "user"

#: Greedy decoding. The instrument wants the same reply to the same pack, and a
#: sampled one is a second source of variation nobody pre-registered.
TEMPERATURE = 0.0

#: Design 2.3: a re-ask is a new coordinate, and the budget for one is zero.
#: Mirrors ``standard.GUARD_PARAMETERS["schema_repair_budget"]`` and
#: ``types.SeatsConfig.schema_repair_budget``; a test imports all three.
SCHEMA_REPAIR_BUDGET = 0


# -- the token arithmetic (seats Q1 and Q7; the module docstring derives it) --

#: Observed generation rate on the Ollama cloud host, tokens per second. The
#: floor of the observed 90-100 band, so the estimate errs long.
OBSERVED_TOKENS_PER_SECOND = 90

#: The remote closes any request still open at this many seconds, whatever the
#: endpoint's ``timeout_seconds`` declares. Never used to *raise* a timeout.
GATEWAY_WALL_SECONDS = 300

#: How close to the wall an elapsed time has to come before a transport error is
#: read as the wall. The four observations were 300-301 s.
GATEWAY_WALL_TOLERANCE_SECONDS = 5

#: The share of the wall generation may claim. The rest is prompt evaluation,
#: the queue behind the credential gate, TLS setup and the response body.
GENERATION_SHARE = 0.5

#: Tokens per English word, conservatively. Only ever used to *derive* the
#: table below; nothing computes with it at call time.
TOKENS_PER_WORD = 1.6

#: Below this the seat cannot generate the smallest conforming reply of any
#: role, so the call is refused rather than dispatched to be truncated.
MIN_MAX_TOKENS = 256

#: Per-role completion ceiling, derived in the module docstring from each
#: role's own contract. The bound actually sent is the lower of this and the
#: seat's wall ceiling.
ROLE_MAX_TOKENS: Mapping[str, int] = MappingProxyType({
    "critic": 2048,
    "defender": 1024,
    "judge": 2048,
    "marker": 1024,
    "variator": 4096,
})

#: One paraphrase of a full case+answer exchange. ``variator``'s entry above is
#: exactly ``paraphrase_n`` of these at the pre-registered ``paraphrase_n = 2``.
VARIATOR_TOKENS_PER_PARAPHRASE = 2048


# -- the response format ----------------------------------------------------

JSON_SCHEMA_MODE = "json_schema"
JSON_OBJECT_MODE = "json_object"

#: Families whose OpenAI-compatible surface documents JSON *mode* but not strict
#: JSON *schema*. The transport's ``_check_json_mode_prompt`` guards the same
#: family, which is the evidence this set is a fact about the route and not a
#: preference of this module.
JSON_OBJECT_ONLY_FAMILIES: frozenset[str] = frozenset({"deepseek"})


# -- blocks and statuses ----------------------------------------------------

#: G1. A schema-invalid reply blocks; at ``schema_repair_budget = 0`` the cell
#: stays ``unresolved`` and nothing is re-asked.
SCHEMA_BLOCK = block_code("schema")

#: A delivery fact about a route, never a reading of any material.
PROVIDER_BLOCK = block_code("provider")

STATUS_OK = "OK"
STATUS_BLOCKED = "BLOCKED"

#: Transport codes that end an *arm* rather than one call, with the reason each
#: does. Design 4.7's induced provider failure is the last of them. Every other
#: code the transport can raise ends one call and leaves the arm running.
#: W5-DRIVER owns the consequence; this module only declares the reading.
ARM_ENDING_CODES: Mapping[str, str] = MappingProxyType({
    "KEY_MISSING":
        "the credential this seat spends is not set; every later call on it fails alike",
    "SECRET_IN_REQUEST":
        "a credential reached a prompt; the arm stops rather than forming a second one",
    "CONCURRENCY_LIMIT_CONFLICT":
        "two authorisations for one credential disagree, so no call on it is admissible",
    "TRANSPORT_OR_RESPONSE_ERROR":
        "the route did not answer; design 4.7's induced arm failure is exactly this code",
})


# --------------------------------------------------------------------------
# Codes
# --------------------------------------------------------------------------

#: ``types.NO_REPLAY``, **imported and re-exported, never retyped** (wave-2
#: integration, Kimi family-C judge finding 2). ``types`` owns the spelling of
#: every stable token in the package; this module is the first thing in the
#: package to *raise* this one - a second call on a spent coordinate - and
#: raising a code is not owning it. The name stays in this module's
#: ``__all__`` so ``roles.NO_REPLAY`` keeps working for every caller and test.

PROVIDER_GATEWAY_WALL = "PROVIDER_GATEWAY_WALL"
ROLE_UNKNOWN = "ROLE_UNKNOWN"
ROLE_SEAT_MISMATCH = "ROLE_SEAT_MISMATCH"
ROLE_COORDINATE_INVALID = "ROLE_COORDINATE_INVALID"
ROLE_PACK_INVALID = "ROLE_PACK_INVALID"
ROLE_PACK_NOT_JSON_MODE_READY = "ROLE_PACK_NOT_JSON_MODE_READY"
ROLE_SCHEMA_NOT_THE_CONTRACT = "ROLE_SCHEMA_NOT_THE_CONTRACT"
ROLE_REGISTER_REQUIRED = "ROLE_REGISTER_REQUIRED"
ROLE_REPAIR_REFUSED = "ROLE_REPAIR_REFUSED"
ROLE_TOKEN_BUDGET_UNREACHABLE = "ROLE_TOKEN_BUDGET_UNREACHABLE"

#: Every code this module introduces, with the one-line reason it exists. The
#: wave-2 integrator folds these into ``types.FAILURE_CODES`` (open question
#: O9). ``NO_REPLAY`` is deliberately absent: it is already declared.
NEW_CODES: Mapping[str, str] = MappingProxyType({
    PROVIDER_GATEWAY_WALL:
        "the route closed a request open at its 300 s wall; a named delivery fact about "
        "the route rather than a bare transport error (seats Q7). Carried as a result's "
        "reason, never raised - it will need an UNREACHED entry.",
    ROLE_UNKNOWN:
        "a role that is not one of contracts.ROLE_NAMES was asked to speak.",
    ROLE_SEAT_MISMATCH:
        "the seat handed in does not hold the role asked for; a marker must be handed "
        "the judge seat it reuses (seats Q4), never a minted identity.",
    ROLE_COORDINATE_INVALID:
        "a coordinate that cannot be a write-once path: empty, absolute, or carrying a "
        "segment outside the declared character set.",
    ROLE_PACK_INVALID:
        "the pack is not bytes, is empty, or declares a digest that is not 64 lowercase "
        "hex characters.",
    ROLE_PACK_NOT_JSON_MODE_READY:
        "a json_object-mode endpoint was handed a pack that never says 'json'; the "
        "transport would refuse it, and appending words of our own to a digested pack "
        "would make this module a second author of the prompt.",
    ROLE_SCHEMA_NOT_THE_CONTRACT:
        "a schema was supplied that is not contracts.schema_for(role); the role "
        "contracts have one owner.",
    ROLE_REGISTER_REQUIRED:
        "a marker call arrived without the register whose closed difference_kind set the "
        "mark must be held to (wave-0 open question O11).",
    ROLE_REPAIR_REFUSED:
        "a re-ask past the pre-registered schema_repair_budget, which is 0; the re-ask "
        "would be a new coordinate and there is no budget for one.",
    ROLE_TOKEN_BUDGET_UNREACHABLE:
        "the seat's wall leaves fewer than MIN_MAX_TOKENS tokens of generation, so no "
        "conforming reply of any role fits inside it.",
})


class RoleRefused(LoopError):
    """A plan error: this module will not form the call at all.

    Never a provider failure and never a schema failure - both of those are
    *returned* as a blocked :class:`RoleResult`, because a route that did not
    answer and a seat that answered badly are outcomes the record has to carry,
    not exceptions the driver has to catch.
    """


class ProviderArmEnded(RoleRefused):
    """Raised **only** by :meth:`RoleResult.raise_if_arm_ended`, never by a call.

    It carries the transport's own code, so a caller that opts into the
    exception shape still records the same token the result carries. Design 4.7
    requires that one provider failure end one arm and leave the others running;
    this is the shape a driver that prefers an exception to a predicate uses.
    """

    def __init__(self, code: str, detail: str = "", *, result: "RoleResult | None" = None):
        super().__init__(code, detail)
        self.result = result


def _fail(code: str, detail: str = "") -> RoleRefused:
    return RoleRefused(code, detail)


# --------------------------------------------------------------------------
# Packs, coordinates, refs
# --------------------------------------------------------------------------

_HEX64 = re.compile(r"\A[0-9a-f]{64}\Z")
_SEGMENT = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._#-]*\Z")


@dataclass(frozen=True)
class Ref:
    """Where a blob is and what it hashes to. ``str(ref)`` is the path."""

    path: str
    sha256: str | None = None

    def __str__(self) -> str:
        return self.path

    def as_dict(self) -> dict[str, Any]:
        return {"path": self.path, "sha256": self.sha256}


@dataclass(frozen=True)
class RolePack:
    """A rendered pack: the bytes that go on the wire, and their digest.

    ``declared`` is whatever the renderer called the pack's digest, kept beside
    ``digest`` (this module's sha256 of the same bytes) rather than in place of
    it, so the two conventions can be compared instead of assumed equal.
    """

    text: bytes
    declared: str | None = None

    @property
    def digest(self) -> str:
        return sha256_bytes(self.text)

    @property
    def agrees(self) -> bool | None:
        return None if self.declared is None else self.declared == self.digest

    @property
    def decoded(self) -> str:
        return self.text.decode("utf-8", "replace")

    def as_dict(self) -> dict[str, Any]:
        return {"pack_bytes": len(self.text), "pack_sha256": self.digest,
                "pack_declared_digest": self.declared,
                "pack_digest_agrees": self.agrees}


def role_pack(value: Any) -> RolePack:
    """Coerce a rendered pack into a :class:`RolePack`.

    Accepts ``bytes``, ``str``, a mapping carrying ``bytes``/``text`` (and
    optionally ``sha256``/``digest``), or any object exposing those as
    attributes - which is the shape W2-PACKS' ``Pack`` is being written to, and
    which this module deliberately duck-types rather than imports: ``packs`` is
    a sibling of the same wave and is not in this module's ``depends_on``.
    """

    if isinstance(value, RolePack):
        return value
    declared: Any = None
    text: Any = None
    if isinstance(value, (bytes, bytearray)):
        text = bytes(value)
    elif isinstance(value, str):
        text = value.encode("utf-8")
    elif isinstance(value, Mapping):
        for key in ("bytes", "text", "body", "content"):
            if key in value:
                text = value[key]
                break
        for key in ("sha256", "digest", "pack_sha", "pack_sha256"):
            if value.get(key) is not None:
                declared = value[key]
                break
    else:
        for key in ("canonical_bytes", "text", "bytes", "body", "content"):
            candidate = getattr(value, key, None)
            if candidate is None:
                continue
            text = candidate() if callable(candidate) else candidate
            break
        for key in ("sha256", "digest", "pack_sha", "pack_sha256"):
            candidate = getattr(value, key, None)
            if candidate is None:
                continue
            declared = candidate() if callable(candidate) else candidate
            break
    if isinstance(text, str):
        text = text.encode("utf-8")
    if not isinstance(text, (bytes, bytearray)):
        raise _fail(ROLE_PACK_INVALID, "a pack is bytes, or an object carrying them")
    text = bytes(text)
    if not text:
        raise _fail(ROLE_PACK_INVALID, "the pack is empty")
    if declared is not None:
        if not isinstance(declared, str) or not _HEX64.fullmatch(declared):
            raise _fail(ROLE_PACK_INVALID,
                        "a declared pack digest is 64 lowercase hex characters")
    return RolePack(text, declared)


#: Roles that hold more than one seat, so their coordinate has to say which.
_MULTI_SEAT_ROLES: frozenset[str] = frozenset({"judge", "marker"})


@dataclass(frozen=True)
class Coordinate:
    """One spent occasion: a role, a seat index, a key, and a repair number.

    ``token`` is the published identity and ``slug`` is where the record lives.
    They differ in one way only: the repair suffix is spelled ``#repair1`` in
    the token (design 2.3's own spelling) and ``.repair1`` in the directory, so
    that one coordinate is one directory and nothing has to be escaped.
    """

    role: str
    key: str
    seat_index: int = 0
    repair: int = 0

    def __post_init__(self) -> None:
        if self.role not in ROLES:
            raise _fail(ROLE_UNKNOWN, f"{self.role!r} is not a seated role")
        if type(self.key) is not str or not self.key:
            raise _fail(ROLE_COORDINATE_INVALID, "a coordinate key is a non-empty string")
        if self.key.startswith("/") or self.key.endswith("/"):
            raise _fail(ROLE_COORDINATE_INVALID, f"{self.key!r} is not a relative key")
        for segment in self.key.split("/"):
            if not _SEGMENT.fullmatch(segment):
                raise _fail(ROLE_COORDINATE_INVALID,
                            f"{segment!r} is not an admissible coordinate segment")
        if type(self.seat_index) is not int or self.seat_index < 0:
            raise _fail(ROLE_COORDINATE_INVALID, "a seat index is a whole number")
        if type(self.repair) is not int or self.repair < 0:
            raise _fail(ROLE_COORDINATE_INVALID, "a repair number is a whole number")

    @property
    def seat_label(self) -> str:
        """``critic`` for a single seat, ``judge#1`` / ``judge#2`` for a pair."""

        return f"{self.role}#{self.seat_index + 1}" if self.role in _MULTI_SEAT_ROLES else self.role

    @property
    def token(self) -> str:
        suffix = f"#repair{self.repair}" if self.repair else ""
        return f"{self.seat_label}@{self.key}{suffix}"

    @property
    def slug(self) -> str:
        tail = self.seat_label.replace("#", "-")
        if self.repair:
            tail += f".repair{self.repair}"
        return f"{self.key}/{tail}"

    def as_dict(self) -> dict[str, Any]:
        return {"token": self.token, "key": self.key, "role": self.role,
                "seat_index": self.seat_index, "repair": self.repair,
                "slug": self.slug}


def seed_for(coordinate: Coordinate) -> int:
    """A sampling seed derived from the coordinate token, not declared.

    Deterministic and recorded: a repeat of one coordinate asks for the same
    sampling. It is not a claim that any provider honours a seed - the record
    says the seed was *derived*, and ``settings.seed_source`` says from what.
    """

    raw = hashlib.sha256(coordinate.token.encode("utf-8")).hexdigest()
    return int(raw[:8], 16) & 0x7FFFFFFF


# --------------------------------------------------------------------------
# The token bound
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class TokenBound:
    """``max_tokens`` for one seat and role, carrying its whole arithmetic."""

    role: str
    seat_timeout_seconds: int
    wall_seconds: int
    rate_tokens_per_second: int
    generation_share: float
    wall_ceiling: int
    role_budget: int
    max_tokens: int
    paraphrase_n: int | None = None

    @property
    def clamped(self) -> bool:
        """True when the seat's wall, not the role's contract, set the bound."""

        return self.max_tokens < self.role_budget

    @property
    def expected_seconds(self) -> float:
        return round(self.max_tokens / self.rate_tokens_per_second, 1)

    def arithmetic(self) -> str:
        """The bound's own account, in one line, for the record and a receipt."""

        return (
            f"min(timeout {self.seat_timeout_seconds}s, gateway wall "
            f"{GATEWAY_WALL_SECONDS}s) = {self.wall_seconds}s "
            f"x {self.generation_share} generation share "
            f"x {self.rate_tokens_per_second} tokens/s = {self.wall_ceiling} tokens; "
            f"{self.role} contract budget {self.role_budget} tokens; "
            f"min = {self.max_tokens} tokens ~ {self.expected_seconds}s "
            f"of generation, {round(100.0 * self.max_tokens / self.rate_tokens_per_second / GATEWAY_WALL_SECONDS, 1)}% "
            f"of the gateway wall"
        )

    def as_dict(self) -> dict[str, Any]:
        return {"role": self.role, "max_tokens": self.max_tokens,
                "role_budget": self.role_budget, "wall_ceiling": self.wall_ceiling,
                "wall_seconds": self.wall_seconds,
                "seat_timeout_seconds": self.seat_timeout_seconds,
                "gateway_wall_seconds": GATEWAY_WALL_SECONDS,
                "rate_tokens_per_second": self.rate_tokens_per_second,
                "generation_share": self.generation_share,
                "paraphrase_n": self.paraphrase_n,
                "clamped_by_wall": self.clamped,
                "expected_generation_seconds": self.expected_seconds,
                "arithmetic": self.arithmetic()}


def max_tokens_for(seat: Seat, role: str, *, paraphrase_n: int | None = None) -> TokenBound:
    """The completion ceiling for one seat and role, with every term recorded.

    The module docstring derives the table; this applies it.  ``paraphrase_n``
    re-derives the variator's budget as ``n x VARIATOR_TOKENS_PER_PARAPHRASE``
    and is ignored for every other role.
    """

    if role not in ROLES:
        raise _fail(ROLE_UNKNOWN, f"{role!r} is not a seated role")
    if not isinstance(seat, Seat):
        raise _fail("CONFIG_INVALID_VALUE", "max_tokens_for takes a Seat")
    timeout = int(seat.timeout_seconds)
    wall = min(timeout, GATEWAY_WALL_SECONDS)
    ceiling = int(wall * GENERATION_SHARE * OBSERVED_TOKENS_PER_SECOND)
    budget = ROLE_MAX_TOKENS[role]
    if role == "variator" and paraphrase_n is not None:
        if type(paraphrase_n) is not int or paraphrase_n < 1:
            raise _fail("CONFIG_INVALID_VALUE", "paraphrase_n is a whole number of at least 1")
        budget = paraphrase_n * VARIATOR_TOKENS_PER_PARAPHRASE
    bound = min(budget, ceiling)
    if bound < MIN_MAX_TOKENS:
        raise _fail(
            ROLE_TOKEN_BUDGET_UNREACHABLE,
            f"{seat.name} allows {ceiling} tokens inside its {wall}s wall at "
            f"{OBSERVED_TOKENS_PER_SECOND} tokens/s, below the {MIN_MAX_TOKENS}-token "
            f"floor a conforming {role} reply needs")
    return TokenBound(
        role=role, seat_timeout_seconds=timeout, wall_seconds=wall,
        rate_tokens_per_second=OBSERVED_TOKENS_PER_SECOND,
        generation_share=GENERATION_SHARE, wall_ceiling=ceiling,
        role_budget=budget, max_tokens=bound,
        paraphrase_n=paraphrase_n if role == "variator" else None)


# --------------------------------------------------------------------------
# The response format
# --------------------------------------------------------------------------


def response_format_for(seat: Seat, role: str, *,
                        register: str | None = None) -> tuple[str, dict[str, Any], dict[str, Any]]:
    """``(mode, response_format, schema)`` for one seat, role and register.

    Strict ``json_schema`` wherever the endpoint supports it - which is every
    family but the ones in :data:`JSON_OBJECT_ONLY_FAMILIES`, native endpoints
    included (the transport unwraps the schema into Ollama's ``format``). A
    marker's schema carries that register's own closed ``difference_kind`` token
    set, never the seven-token union.
    """

    if role not in ROLES:
        raise _fail(ROLE_UNKNOWN, f"{role!r} is not a seated role")
    schema = schema_for(role)
    if role == "marker":
        if register is None:
            raise _fail(ROLE_REGISTER_REQUIRED,
                        "a marker call names the register its mark is held to (O11)")
        schema["properties"]["difference_kind"]["enum"] = list(
            difference_kinds_for(register)) + [None]
    if seat.endpoint.family in JSON_OBJECT_ONLY_FAMILIES:
        return JSON_OBJECT_MODE, {"type": JSON_OBJECT_MODE}, schema
    return (JSON_SCHEMA_MODE,
            {"type": JSON_SCHEMA_MODE,
             "json_schema": {"name": schema.get("title", f"loop.{role}.v1"),
                             "strict": True, "schema": schema}},
            schema)


# --------------------------------------------------------------------------
# Providers
# --------------------------------------------------------------------------

#: ``factory(role, coordinate, records_dir, *, seat=None, endpoint=None)`` - the
#: loop's own shape, which ``synthetic.ScriptedProviders.provider`` already has.
ProviderFactory = Callable[..., Any]


def _bind_factory(factory: Any) -> Callable[..., Any]:
    """The loop-shaped call on ``factory``.

    ``synthetic.ScriptedProviders`` carries **two** shapes: ``__call__`` is
    runner v2's ``(endpoint, records_dir)`` and ``.provider`` is the loop's.
    Handing this module the object itself must reach the loop's, or the fixture
    silently answers a dispatch call's script to a seat's question - so a
    factory exposing ``.provider`` is bound to it, and a plain callable is used
    as it is.
    """

    bound = getattr(factory, "provider", None)
    return bound if callable(bound) else factory


def default_provider_factory(role: str, coordinate: str, records_dir: Path | str, *,
                             seat: str | None = None,
                             endpoint: Endpoint | None = None) -> OpenAICompatProvider:
    """The live transport, bound to the seat's own endpoint.

    ``role``, ``coordinate`` and ``seat`` are part of the protocol an offline
    factory needs and are unused here: a live provider is addressed by its
    endpoint alone.
    """

    if endpoint is None:
        raise _fail("CONFIG_INVALID_VALUE", "a provider is built for a declared endpoint")
    return OpenAICompatProvider(endpoint, records_dir)


# --------------------------------------------------------------------------
# The result
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class RoleResult:
    """One spent call: what was said, or the block that stands in its place."""

    role: str
    coordinate: Coordinate
    seat: Mapping[str, Any]
    status: str
    output: RoleOutput | None
    block: str | None
    reason: str | None
    detail: str
    prompt_ref: Ref
    raw_ref: Ref
    record_path: str
    record: Mapping[str, Any]
    arm_ended: bool = False

    @property
    def ok(self) -> bool:
        return self.status == STATUS_OK

    @property
    def blocked(self) -> bool:
        return self.status == STATUS_BLOCKED

    @property
    def family(self) -> str:
        return str(self.seat["family"])

    @property
    def key_env(self) -> str:
        return str(self.seat["key_env"])

    @property
    def pack_sha(self) -> str:
        return str(self.record["pack_sha256"])

    @property
    def max_tokens(self) -> int:
        return int(self.record["settings"]["max_tokens"])

    def raise_if_arm_ended(self) -> "RoleResult":
        """Opt in to :class:`ProviderArmEnded`; otherwise return ``self``.

        Nothing in this module calls it. A driver that would rather unwind than
        test a predicate calls it; one that wants to keep the other arms running
        reads :attr:`arm_ended` instead.
        """

        if self.arm_ended:
            raise ProviderArmEnded(str(self.reason), self.detail, result=self)
        return self

    def as_dict(self) -> dict[str, Any]:
        return {"role": self.role, "coordinate": self.coordinate.as_dict(),
                "seat": dict(self.seat), "status": self.status,
                "block": self.block, "reason": self.reason, "detail": self.detail,
                "output": self.output.as_dict() if self.output is not None else None,
                "prompt_ref": self.prompt_ref.as_dict(),
                "raw_ref": self.raw_ref.as_dict(),
                "record_path": self.record_path, "arm_ended": self.arm_ended}


# --------------------------------------------------------------------------
# The call
# --------------------------------------------------------------------------


def _seat_view(seat: Seat, coordinate: Coordinate) -> dict[str, Any]:
    view = {"role": coordinate.role, "seat_role": seat.role, "index": seat.index,
            "label": coordinate.seat_label, "lineage": seat.lineage,
            "native": bool(seat.native)}
    view.update(seat.identity())
    return view


def _check_seat(role: str, seat: Seat) -> None:
    if not isinstance(seat, Seat):
        raise _fail("CONFIG_INVALID_VALUE", "call_role takes a seats.Seat")
    resolved = REUSED_ROLES.get(role, role)
    if seat.role != resolved:
        raise _fail(
            ROLE_SEAT_MISMATCH,
            f"a {role} call needs a {resolved} seat; this seat holds {seat.role!r}. "
            "The marker reuses the judge pair and mints no identity of its own.")


def _check_schema(role: str, supplied: Any, contract: Mapping[str, Any]) -> None:
    if supplied is None:
        return
    if supplied != contract:
        raise _fail(ROLE_SCHEMA_NOT_THE_CONTRACT,
                    f"the schema supplied for {role!r} is not contracts.schema_for({role!r}); "
                    "the role contracts have one owner")


def _claim(records_dir: Path | str, coordinate: Coordinate) -> Path:
    """Create the coordinate's directory, atomically, or refuse as a replay.

    The directory is the claim, and it is made **before** anything could be
    sent, so a process killed mid-call leaves a coordinate that is visibly
    spent.  A claimed directory with no call record is therefore
    ``INDETERMINATE`` in W1-STEPS' sense - a request with no response - and is
    never re-sent by this module: the resume plan, not a retry, decides what
    follows.

    **Corrected at wave-5 integration (WAVE4-INTERFACE section 8, item 2).**
    An earlier wording said ``steps.scan_coordinates`` reads this claim as
    started.  It does not, and cannot: that function reads a
    ``requests/``-``attempts/``-``responses/`` tree, which is runner v2's
    dispatch layout, while this one is ``<records_dir>/<key>/<role>/`` with a
    ``provider`` subdirectory.  The reading arm's list is
    ``reader.unanswered_coordinates``, which reads *this* layout; W5-DRIVER
    files both lists side by side at READ and neither stands in for the other.
    """

    target = fenced(records_dir, coordinate.slug)
    try:
        target.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        raise _fail(
            NO_REPLAY,
            f"{coordinate.token} already has a record at {target}; a spent coordinate is "
            "never re-sent, and a re-ask is a new coordinate with its own budget") from None
    return target


def _provider_refs(provider_dir: Path, record: Mapping[str, Any] | None) -> tuple[Ref, Ref]:
    number: int | None = None
    if isinstance(record, Mapping) and type(record.get("call_number")) is int:
        number = int(record["call_number"])
    if number is None:
        found = sorted(provider_dir.glob("call-*.request.json"))
        if found:
            number = int(found[0].name.split("-", 1)[1].split(".", 1)[0])
    if number is None:
        return Ref(""), Ref("")
    stem = f"call-{number:04d}"
    request = provider_dir / (stem + ".request.json")
    response = provider_dir / (stem + ".response.json")
    carried = dict(record or {})
    return (Ref(str(request) if request.exists() else "", carried.get("request_sha256")),
            Ref(str(response) if response.exists() else "",
                carried.get("provider_response_sha256")))


def provider_reason(failure: ProviderFailure) -> tuple[str, str | None]:
    """``(reason, transport_code)`` - the gateway wall named where it applies."""

    record = failure.record if isinstance(failure.record, Mapping) else {}
    elapsed = record.get("elapsed_ms")
    at_the_wall = (
        failure.code == "TRANSPORT_OR_RESPONSE_ERROR"
        and type(elapsed) is int
        and elapsed >= (GATEWAY_WALL_SECONDS - GATEWAY_WALL_TOLERANCE_SECONDS) * 1000
    )
    if at_the_wall:
        return PROVIDER_GATEWAY_WALL, failure.code
    return failure.code, None


def call_role(role: str, seat: Seat, pack: Any, schema: Any,
              records_dir: Path | str, *,
              coordinate: str,
              register: str | None = None,
              repair: int = 0,
              seat_index: int | None = None,
              seat_token: str | None = None,
              paraphrase_n: int | None = None,
              provider_factory: ProviderFactory | None = None,
              max_per_key: int = MAX_PER_KEY,
              repair_budget: int = SCHEMA_REPAIR_BUDGET) -> RoleResult:
    """One call, one record, no retry. Returns a :class:`RoleResult`.

    ``schema`` is the wave plan's positional argument and may only be ``None``
    (the contract's own, which is the normal case) or a value equal to it.
    ``coordinate`` is the cell or mark key the call is spent on; ``repair``
    makes it a different coordinate (``…#repair1``) and is refused above
    ``repair_budget``, which is ``0`` at the pre-registered standard.

    A provider failure is **returned**, never raised: ``blocked:provider`` with
    the transport's own code as the reason. A schema-invalid reply is returned
    as ``blocked:schema`` with the ``contracts.SCHEMA_REASONS`` sub-reason, and
    nothing is re-asked.
    """

    if role not in ROLES:
        raise _fail(ROLE_UNKNOWN, f"{role!r} is not a seated role")
    _check_seat(role, seat)
    if type(repair) is not int or repair < 0:
        raise _fail(ROLE_COORDINATE_INVALID, "a repair number is a whole number")
    if repair > repair_budget:
        raise _fail(
            ROLE_REPAIR_REFUSED,
            f"repair {repair} is past the pre-registered schema_repair_budget of "
            f"{repair_budget}; a re-ask is a new coordinate and there is no budget for one")
    body = role_pack(pack)
    where = Coordinate(role=role, key=coordinate,
                       seat_index=seat.index if seat_index is None else seat_index,
                       repair=repair)
    mode, response_format, contract = response_format_for(seat, role, register=register)
    _check_schema(role, schema, contract)
    if mode == JSON_OBJECT_MODE and "json" not in body.decoded.lower():
        raise _fail(
            ROLE_PACK_NOT_JSON_MODE_READY,
            f"{seat.name} is answered in {JSON_OBJECT_MODE} mode, which needs the word "
            "'json' in the prompt; the pack does not say it, and this module does not "
            "add words to a pack whose bytes are digested")
    bound = max_tokens_for(seat, role, paraphrase_n=paraphrase_n)
    seed = seed_for(where)
    thinking = False if seat.endpoint.family == "deepseek" else None

    root = _claim(records_dir, where)
    provider_dir = root / "provider"
    provider_dir.mkdir(parents=False, exist_ok=False)

    factory = _bind_factory(provider_factory or default_provider_factory)
    settings = {
        "response_format_mode": mode,
        "response_format_strict": mode == JSON_SCHEMA_MODE,
        "schema_title": contract.get("title"),
        "register": register,
        "max_tokens": bound.max_tokens,
        "timeout_seconds": seat.timeout_seconds,
        "gateway_wall_seconds": GATEWAY_WALL_SECONDS,
        "temperature": TEMPERATURE,
        "seed": seed,
        "seed_source": "sha256(coordinate.token)[:8]",
        "thinking": thinking,
        "schema_repair_budget": repair_budget,
        "repair": where.repair,
        "retries": 0,
        "gate_order": list(GATE_ORDER),
        "key_cap": key_cap_for(seat, max_per_key),
        "max_per_key": max_per_key,
        "token_bound": bound.as_dict(),
        # Decision 42(c): the record says which gate was acquired where, and by
        # what. ``inner_held_by`` is filled in once the provider exists - it is
        # null for a provider that holds no inner gate, the offline one - so a
        # reader can tell "not held" from "not recorded".
        "gates": {
            "order": list(GATE_ORDER),
            "outer": GATE_ORDER[0],
            "outer_held_by": GATE_HELD_BY[GATE_ORDER[0]],
            "inner": GATE_ORDER[1],
            "inner_held_by": None,
        },
    }

    result: CallResult | None = None
    failure: ProviderFailure | None = None
    gate = key_gate_for(seat, max_per_key)
    with gate:                                   # outer: runner v2's key gate
        provider = factory(role, where.key, provider_dir,
                           seat=seat_token if seat_token is not None else where.seat_label,
                           endpoint=seat.endpoint)
        if isinstance(provider, OpenAICompatProvider):
            settings["gates"]["inner_held_by"] = GATE_HELD_BY[GATE_ORDER[1]]
        try:
            # inner: provider_openai_compat.slots_for, acquired by the provider.
            result = provider.complete(
                [{"role": MESSAGE_ROLE, "content": body.decoded}],
                response_format=response_format,
                max_tokens=bound.max_tokens,
                temperature=TEMPERATURE,
                seed=seed,
                thinking=thinking,
                coordinate={"loop_coordinate": where.token, "role": role,
                            "seat": where.seat_label, "pack_sha256": body.digest},
            )
        except ProviderFailure as exc:
            failure = exc

    prompt_ref, raw_ref = _provider_refs(
        provider_dir, result.record if result is not None else (failure.record if failure else None))

    usage: Mapping[str, Any] = dict(result.usage) if result is not None else {}
    reasoning = {
        "reasoning_content_present": bool(result.reasoning_content_present) if result else False,
        "reasoning_content_persisted": False,
        "reasoning_tokens": _reasoning_tokens(usage),
        "reasoning_content_sha256": None,
    }

    validation: Validation | None = None
    output: RoleOutput | None = None
    block: str | None = None
    reason: str | None = None
    detail = ""
    transport_code: str | None = None
    arm_ended = False

    if failure is not None:
        block = PROVIDER_BLOCK
        reason, transport_code = provider_reason(failure)
        detail = str(failure)
        arm_ended = failure.code in ARM_ENDING_CODES
    else:
        assert result is not None
        validation = check(role, result.content, register=register)
        if validation.ok:
            output = validation.value
        else:
            block = SCHEMA_BLOCK
            reason = validation.reason
            detail = validation.message

    identity = {
        "schema": ROLES_SCHEMA,
        RECORD_FIELD: RECORD_KIND,
        "coordinate": where.token,
        "coordinate_body": where.as_dict(),
        "role": role,
        "seat": _seat_view(seat, where),
        "settings": settings,
        "replay_of": "",
        **body.as_dict(),
    }
    outcome = {
        "status": STATUS_BLOCKED if block else STATUS_OK,
        "block": block,
        "reason": reason,
        "transport_code": transport_code,
        "detail": detail,
        "schema_reason": validation.reason if validation is not None else None,
        "schema_path": list(validation.path) if validation is not None else [],
        "arm_ended": arm_ended,
        "provider_status": result.status if result is not None else None,
        "finish_reason": result.finish_reason if result is not None else None,
        "returned_model": result.returned_model if result is not None else None,
        "elapsed_ms": result.elapsed_ms if result is not None else _elapsed_of(failure),
        "usage": dict(usage),
        "response_sha256": (sha256_bytes(result.content.encode("utf-8"))
                            if result is not None else None),
        "prompt_ref": prompt_ref.as_dict(),
        "raw_ref": raw_ref.as_dict(),
        "output": output.as_dict() if output is not None else None,
        **reasoning,
    }
    record: dict[str, Any] = dict(identity)
    record["digest"] = value_digest(identity)
    record["outcome"] = outcome
    assert_no_scoring_keys(record)               # G12, before anything is written
    path = root / "call.json"
    write_new(path, record)

    return RoleResult(
        role=role, coordinate=where, seat=record["seat"],
        status=outcome["status"], output=output, block=block, reason=reason,
        detail=detail, prompt_ref=prompt_ref, raw_ref=raw_ref,
        record_path=str(path), record=record, arm_ended=arm_ended)


def _reasoning_tokens(usage: Mapping[str, Any]) -> int | None:
    """The reasoning token COUNT where the provider reported one. Never text."""

    direct = usage.get("reasoning_tokens")
    if type(direct) is int:
        return direct
    details = usage.get("completion_tokens_details")
    if isinstance(details, Mapping) and type(details.get("reasoning_tokens")) is int:
        return int(details["reasoning_tokens"])
    return None


def _elapsed_of(failure: ProviderFailure | None) -> int | None:
    if failure is None or not isinstance(failure.record, Mapping):
        return None
    elapsed = failure.record.get("elapsed_ms")
    return elapsed if type(elapsed) is int else None


# --------------------------------------------------------------------------
# One caller per role
# --------------------------------------------------------------------------


def call_critic(seat: Seat, pack: Any, records_dir: Path | str, *,
                coordinate: str, **kwargs: Any) -> RoleResult:
    """Section 2.3's critic: the strongest case that one named relation holds."""

    return call_role("critic", seat, pack, None, records_dir,
                     coordinate=coordinate, **kwargs)


def call_defender(seat: Seat, pack: Any, records_dir: Path | str, *,
                  coordinate: str, **kwargs: Any) -> RoleResult:
    """Section 2.3's defender: the juxtaposition does not establish the claim."""

    return call_role("defender", seat, pack, None, records_dir,
                     coordinate=coordinate, **kwargs)


def call_judge(seat: Seat, pack: Any, records_dir: Path | str, *,
               coordinate: str, seat_index: int | None = None,
               **kwargs: Any) -> RoleResult:
    """One judge seat of the cross-family pair. The pair's packs are identical.

    ``seat_index`` defaults to the seat's own, which is what keeps two judge
    seats from writing one coordinate.
    """

    return call_role("judge", seat, pack, None, records_dir,
                     coordinate=coordinate, seat_index=seat_index, **kwargs)


def call_variator(seat: Seat, pack: Any, records_dir: Path | str, *,
                  coordinate: str, paraphrase_n: int | None = None,
                  **kwargs: Any) -> RoleResult:
    """Section 2.3's variator, over the *exchange* only.

    The material is never paraphrased: its bytes are what the offsets resolve
    against (surface S7). This module sends the pack it is handed, so the rule
    is the pack renderer's to keep and this one cannot break it.
    """

    return call_role("variator", seat, pack, None, records_dir,
                     coordinate=coordinate, paraphrase_n=paraphrase_n, **kwargs)


def call_marker(seat: Seat, pack: Any, records_dir: Path | str, *,
                coordinate: str, register: str, seat_index: int | None = None,
                **kwargs: Any) -> RoleResult:
    """One (cell, comparison, register) mark, on the judge seat it reuses.

    ``register`` is required: the wire schema carries that register's own closed
    ``difference_kind`` set, so the seat never sees another register's tokens
    and no call can trade registers off (section 2.3, wave-0 question O11).
    """

    return call_role("marker", seat, pack, None, records_dir,
                     coordinate=coordinate, register=register,
                     seat_index=seat_index, **kwargs)
