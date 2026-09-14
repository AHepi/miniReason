"""Deterministic pack rendering for every role, and the exchange surface ``E``.

What this is
------------
One pack is everything a seat is shown on one occasion, rendered as a pure
deterministic function of its arguments: the reading rubric body taken from the
pinned standard, the closed vocabulary with the instrument's own lexical-overlap
banner verbatim, the frozen material ``M`` embedded byte-for-byte, and — for a
judge — the case, the answer and the **precedent slice** selected by a
deterministic query whose text is logged into the pack record.  Every pack is
content-addressed: :func:`pack_sha` is the sha256 of its canonical bytes, and
that digest is what a call record pins.

Design section implemented
--------------------------
W2-PACKS of *The automated end-to-end harness loop — FINAL design of record*:
§2.3's five prompt contracts, §2.4's G2(b) exchange surface, G6's order swap,
G7's paraphrase spot-check input, G8's baseline seal and G12's no-scoring-key
scan, with §2.1's standard body as the rubric's only source.

What this is NOT
----------------
It calls no provider, opens no file, writes nothing anywhere, reads no clock and
draws no random number.  It resolves no reading and decides nothing: it lays out
what a seat is asked, never what the answer is worth.  It scores nothing, ranks
nothing and compares no two seats — *seats are occasions, not contestants*
(FW5:849, :851) — and the one ordering it does impose, the precedent slice, is
registration order behind the appellate rulings and is never a ranking by merit.

The five packs, and what §2.3 puts in each
------------------------------------------
=============  ===========================================================
``critic``     rubric body, closed vocabulary + banner, ``M``, the framing
               (uptake booleans, resolver notes, the lexical-overlap note),
               the output contract.
``defender``   ``M``, the claim under trial with its citation, the critic's
               case, the output contract.  No rubric: §2.3 does not give the
               defender one, and a pack does not carry what its role is not
               asked to apply.
``judge``      rubric body, ``M``, the claim under trial, the case, the
               answer, the precedent slice with its query, the contract.
``marker``     the pairwise rubric class, **one** register's PLAN §8a
               definition and its closed ``difference_kind`` tokens, the two
               sides under neutral aliases, the contract.  The sealed
               baseline's sha256 is pinned into the record (G8).
``variator``   the exchange, the spans that must survive byte-identically,
               the contract.  The material is never paraphrased.
=============  ===========================================================

Two surfaces, and why the exchange one lives here
-------------------------------------------------
:mod:`minireason.loop.surface` owns ``M`` and G2(a).  The *exchange* surface
``E = case + "\\n" + answer`` of G2(b) is owned here, as wave 1's open question
**S4** asks, so that G2(b) has exactly one implementation: :func:`exchange_surface`
builds it, :meth:`Exchange.count` counts occurrences **overlapping** — strictly
stronger than ``str.count``, which calls ``aa`` unique in ``aaa`` — and
:meth:`Exchange.resolve` reports the unique span and which part of the exchange
it fell in.  :meth:`Exchange.conforming` is the *vendored* predicate
(``decisive in exchange``) kept beside it, so W3-TRIAL can assert the program's
own stronger check first and the vendored one last, exactly as
``graph.register_transcript`` does at the registration gate.

``graph.Transcript.validated`` uses ``str.count`` on the same text.  Where this
module answers 1 the two agree; where an overlapping occurrence exists this
module says 2 and the vendored one says 1, and the stronger answer is the one a
guard must act on.  *Recommendation for W3-TRIAL: call* :meth:`Exchange.count`
*before building the* ``Transcript``, *never after.*

Coordinates.  :attr:`Exchange.text` is ``str`` and :class:`ExchangeOffset`
offsets are **code-point** offsets into it.  That is deliberately unlike
:class:`~minireason.loop.surface.Surface`, whose offsets are utf-8 **byte**
offsets into a frozen byte string that maps back to an occurrence file: no
occurrence file stands behind an exchange, so a byte coordinate would buy
nothing, and the vendored predicate and every ``str`` operation the trial
performs are already code-point based.  The two coordinate systems never meet.

Deviations from the wave-plan interface, and why
------------------------------------------------
1. **``render_exchange(pack, critic, defender)`` takes ``defender`` optionally.**
   §2.3 names two packs downstream of the row pack — the defender's (``M`` plus
   the critic's case) and the judge's (that, plus the answer and the precedent
   slice) — and the wave plan names one renderer.  With ``defender=None`` the
   result is the **defender** pack; with a defender it is the **judge** pack.
   The role is in :attr:`Pack.role` and in the pack's own title, so nothing has
   to infer which was built.  Both are rendered *from the row pack*, which is
   what makes the material reaching seat *n* byte-identical to the material
   reaching seat 0 (wave-1 open question **S7**); a test asserts it.
2. **``exchange_surface`` and ``paraphrase_surface`` are added here**, per S4.
3. **``precedent_slice`` returns a :class:`PrecedentSlice`, which *is* a
   ``list``** — the wave plan's ``-> list`` — carrying the query text that
   selected it.  A judge pack is refused without one: the acceptance clause
   requires the query recorded *with the pack*, and a bare list cannot carry it.
4. **The sides of a mark pack are shown as ``A`` and ``B``.**  G6 runs every
   pairwise judgement "in both presentation orders with labels reassigned"; a
   seat told which side is ORIGINAL is being told half the answer.  The alias to
   arm map is in the pack *record*, never in the pack *text*, so the program can
   de-alias ``left_quote``/``right_quote`` and the seat cannot.
5. **A mark pack carries the baseline's sha256 and never the baseline's kind
   set.**  G9's downgrade of ``differs`` to ``same`` at kind grain is the
   *program's*; a pack that listed the frozen kinds would be asking the seat to
   pre-empt it, and a seat that pre-empted it would make G9 untestable.
6. **``k`` for the precedent slice is this module's resource bound**
   (:data:`PRECEDENT_K`), not a guard parameter: §2.1 freezes no ``K``.  It is
   pinned into the pack record so a changed bound is visible in a diff.  It is a
   declared resource bound and never a threshold on anything read.
7. **G12 is run over the pack's structured parts and over the pack's *own*
   heading lines**, never over the material.  ``assert_no_scoring_keys`` sees
   keys this module chose; ``assert_no_scoring_headers`` sees the title and the
   ``##`` headings this module wrote.  The material is quoted matter — refusing
   a published record because its author wrote the word *better* in a table
   header would be this loop editing its own evidence, which is the boundary
   W1-GRAPH's ``G12_EXEMPT`` draws for the same reason.
8. **The judge pack carries the nominated relation and the cited passage.**
   §2.3's list for the judge is elliptical; rubric clause **R1** — "does the
   cited passage establish the relation the critic named?" — is unanswerable
   without both.  Neither is an outcome: the claim under trial is what the trial
   is *about*.
9. **G7's re-ruling pack is** ``render_exchange(..., exchange=paraphrase)``,
   not a sixth renderer.  A judge re-ruling a paraphrase is being shown the same
   material, the same claim, the same rubric and the same precedent slice, with
   one restated text where the case and the answer were; making that a separate
   function would have been a second place for the material to enter a pack.
10. **The precedent slice is the one declared exception to "a pack never
    contains another cell's outcome"** (wave-1 integration decision 26).  §2.3
    says a pack carries no other cell's outcome; §2.3 also gives the judge pack
    a precedent slice, which is *made of* readings of other cells.  The ruling,
    applied here: the slice is the explicit exception, and it is narrowed until
    it is not the thing the rule forbids.

    * What is rendered is the precedent's **relation and its cited passage** -
      what a prior panel read, and where it read it.
    * What is **not** rendered is every adjudication fact about it: no status,
      no label, no standing, no ``att``, no ``dep``, no ``sustained`` value.
      ``assert_no_adjudication_keys`` runs over the rendered parts and refuses
      any of them, and :data:`STANDING` never reaches the pack text.
    * The **query text** that selected the slice - which does name ``accepted``,
      because a precedent that is not standing is not precedent - is recorded
      with the pack *record*, never rendered into the prompt.  A seat is shown
      what was read, never what the graph currently thinks of it.
    * Authority is **pack ordering** and nothing else (§3, Appellate): the
      appellate rulings come first because they come first, not because they
      carry a privilege a seat can see.

11. **Two record keys are spelled around the guards.**  A precedent's place in
    the slice is ``position`` and not *rank*, because *rank* is a member of
    ``standard.FORBIDDEN_KEYS`` and G12 refuses it — a slice that called its own
    ordering by that name would be asserting the very thing precedent ordering
    is not.  A block's heading is ``name`` and not *label*, because §2.3 says a
    pack never contains a label and a key spelled that way invites exactly the
    confusion the rule is about.

Agreements asserted by test, never by import
--------------------------------------------
This module does not import :mod:`minireason.loop.graph` — its declared
dependencies are W0-CONTRACTS, W0-STANDARD and W1-SURFACE — so
:func:`precedent_slice` reads a ``deepreason_core`` harness through the same
duck-typed path :meth:`obligations.Situation.from_harness` uses
(``harness.state.artifacts``, ``harness.state.status``, ``harness.blobs``) and
mirrors four tokens: :data:`RECORD_FIELD`, :data:`RECORD_APPELLATE_RULING`,
:data:`RECORD_READING_ROW`, :data:`RECORD_CELL_MARK` and :data:`STANDING`.
``tests/loop/test_packs.py`` imports both modules and asserts every mirror.

Reuse
-----
The rubric body, the vocabulary, the banner, the registers, the word limits and
the guard parameters all come out of :mod:`minireason.loop.standard` — the pack
retypes none of them.  The output contract embedded in each pack is
``contracts.schema_for(role)``, the same object ``contracts.validate`` holds the
answer to, so a pack cannot describe a contract the validator does not enforce.
G12 is ``contracts.assert_no_scoring_keys`` and
``standard.assert_no_scoring_headers``.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from deepreason_core.canonical import canonical_json, sha256_hex

from minireason.loop.contracts import (
    assert_no_scoring_keys,
    difference_kinds_for,
    schema_for,
)
from minireason.loop.standard import (
    GUARD_PARAMETERS,
    READING_BANNER,
    REGISTER_IDS,
    SPEC_ID,
    STANDARD_NAME,
    STANDARD_SCHEMA,
    WORD_LIMITS,
    assert_no_exhaustion_claim,
    assert_no_scoring_headers,
    standard_body,
)
from minireason.loop.surface import Surface
from minireason.loop.types import LoopError

__all__ = [
    "PACKS_SCHEMA",
    "EXCHANGE_SCHEMA",
    "PACK_ROLES",
    "ROLE_CRITIC",
    "ROLE_DEFENDER",
    "ROLE_JUDGE",
    "ROLE_MARKER",
    "ROLE_VARIATOR",
    "RUBRIC_FOR_ROLE",
    "EXCHANGE_SEPARATOR",
    "EXCHANGE_PARTS",
    "PARAPHRASE_PART",
    "JOIN_PART",
    "TITLE_PREFIX",
    "HEADING_PREFIX",
    "BLOCK_SEPARATOR",
    "BLOCK_KINDS",
    "SIDE_KIND",
    "ORDER_AS_DECLARED",
    "ORDER_SWAPPED",
    "ORDERS",
    "ALIAS_A",
    "ALIAS_B",
    "ALIASES",
    "PRECEDENT_K",
    "PRECEDENT_QUERY",
    "PRECEDENT_KINDS",
    "RECORD_FIELD",
    "RECORD_APPELLATE_RULING",
    "RECORD_READING_ROW",
    "RECORD_CELL_MARK",
    "STANDING",
    "CELL_KEY_SEPARATOR",
    "FORBIDDEN_PACK_KEYS",
    "BASELINE_NOT_FIRST",
    "PACK_INPUT_INVALID",
    "PACK_ADJUDICATION_KEY",
    "EXCHANGE_MALFORMED",
    "PRECEDENT_QUERY_INVALID",
    "NEW_CODES",
    "PackError",
    "BaselineNotFirst",
    "Block",
    "Pack",
    "Exchange",
    "ExchangeOffset",
    "MarkSide",
    "Precedent",
    "PrecedentSlice",
    "assert_no_adjudication_keys",
    "assert_pack_clean",
    "both_orders",
    "exchange_surface",
    "held_spans_of",
    "pack_sha",
    "paraphrase_surface",
    "precedent_slice",
    "render_exchange",
    "render_paraphrase_request",
    "render_register",
    "render_row",
]


# --------------------------------------------------------------------------
# Codes
# --------------------------------------------------------------------------

#: G8's own name for a cross-case pack rendered before the baseline was sealed.
#: Already a member of ``types.FAILURE_CODES`` — the design names it — so it is
#: not in :data:`NEW_CODES`.
BASELINE_NOT_FIRST = "BASELINE_NOT_FIRST"

PACK_INPUT_INVALID = "PACK_INPUT_INVALID"
PACK_ADJUDICATION_KEY = "PACK_ADJUDICATION_KEY"
EXCHANGE_MALFORMED = "EXCHANGE_MALFORMED"
PRECEDENT_QUERY_INVALID = "PRECEDENT_QUERY_INVALID"

#: Codes this module raises that ``types.FAILURE_CODES`` does not yet carry,
#: each with the one-line reason it exists.  The wave-2 integrator folds them in
#: and adds ``("packs", "PackError"): 0`` to the scan's ``TOKEN_ARGUMENT``;
#: nothing here edits or narrows the table (W0-TYPES open question O9).
NEW_CODES: Mapping[str, str] = MappingProxyType({
    "PACK_INPUT_INVALID": (
        "an argument a pack is rendered from is missing, empty or not the shape "
        "the pack contract declares, so the pack would be a guess"
    ),
    "PACK_ADJUDICATION_KEY": (
        "a pack part carries an adjudication key - att, dep, a status or a "
        "standing - and a pack never shows a seat the state of the graph"
    ),
    "EXCHANGE_MALFORMED": (
        "an exchange surface was built from a missing or non-string part, so "
        "G2(b)'s uniqueness check would run over a text no seat was shown"
    ),
    "PRECEDENT_QUERY_INVALID": (
        "a precedent slice was requested with a non-positive k, from a source "
        "that is not a readable harness, or handed to a judge pack without the "
        "query text that selected it"
    ),
})


class PackError(LoopError):
    """A pack that cannot be rendered from what it was handed.

    ``(code, detail="")``, the argument order every wave-0 exception takes, and a
    :class:`~minireason.loop.types.LoopError`, so ``except LoopError`` catches it
    with every other refusal in the package.
    """


class BaselineNotFirst(PackError):
    """G8: no cross-case pack renders before that cell's baseline is sealed.

    ``(detail="")``.  The code is :data:`BASELINE_NOT_FIRST`, which the design
    names by that spelling.  PLAN §8a's "the baseline note is written first and
    is not revised afterwards" becomes physically irreversible here: the sha256
    this refuses to render without is pinned into the call record, so revising
    the baseline changes a hash every subsequent call record already carries.
    """

    def __init__(self, detail: str = "") -> None:
        super().__init__(BASELINE_NOT_FIRST, detail)


def _refuse(code: str, detail: str = "") -> PackError:
    return PackError(code, detail)


# --------------------------------------------------------------------------
# Vocabulary
# --------------------------------------------------------------------------

#: The emitted pack record's schema name.
PACKS_SCHEMA = "minireason.loop.packs.v1"

#: The emitted exchange record's schema name.
EXCHANGE_SCHEMA = "minireason.loop.packs.exchange.v1"

ROLE_CRITIC = "critic"
ROLE_DEFENDER = "defender"
ROLE_JUDGE = "judge"
ROLE_MARKER = "marker"
ROLE_VARIATOR = "variator"

#: The five roles a pack is rendered for.  ``decider`` is absent: it is a
#: program (§2.3) and is never handed a pack.
PACK_ROLES: tuple[str, ...] = (
    ROLE_CRITIC,
    ROLE_DEFENDER,
    ROLE_JUDGE,
    ROLE_MARKER,
    ROLE_VARIATOR,
)

#: Which question class of the standard each pack applies, where it applies one.
#: ``relation`` is tried in the absolute mode, ``contrast-mark`` pairwise.
RUBRIC_FOR_ROLE: Mapping[str, str] = MappingProxyType({
    ROLE_CRITIC: "relation",
    ROLE_JUDGE: "relation",
    ROLE_MARKER: "contrast-mark",
})

#: ``E = case + "\n" + answer`` — the separator is the design's own, spelled
#: once here so no caller retypes it.
EXCHANGE_SEPARATOR = "\n"

#: The two parts of a trial exchange, in the order they are joined.
EXCHANGE_PARTS: tuple[str, ...] = ("case", "answer")

#: The single part of a paraphrased exchange.
PARAPHRASE_PART = "paraphrase"

#: What :meth:`Exchange.side_at` reports for a span crossing the separator.
JOIN_PART = "join"

#: How a pack is laid out.  The title is one ATX level-1 heading; every block is
#: one level-2 heading and its body; blocks are separated by a blank line.
TITLE_PREFIX = "# "
HEADING_PREFIX = "## "
BLOCK_SEPARATOR = "\n\n"

SIDE_KIND = "side"

#: Every value :attr:`Block.kind` can take.
BLOCK_KINDS: tuple[str, ...] = (
    "instruction",
    "rubric",
    "vocabulary",
    "banner",
    "material",
    "framing",
    "claim",
    "register",
    SIDE_KIND,
    "exchange",
    "held-spans",
    "precedent",
    "contract",
)

#: G6: every pairwise judgement is run in both presentation orders.  These are
#: the two, and the one a pack is in is recorded inside its own digest.
ORDER_AS_DECLARED = "as-declared"
ORDER_SWAPPED = "swapped"
ORDERS: tuple[str, ...] = (ORDER_AS_DECLARED, ORDER_SWAPPED)

#: The neutral aliases the two sides of a mark pack are shown under.  Which arm
#: each one is lives in the pack record and never in the pack text.
ALIAS_A = "A"
ALIAS_B = "B"
ALIASES: tuple[str, ...] = (ALIAS_A, ALIAS_B)

#: This module's resource bound on the precedent slice (deviation 6).  Not a
#: guard parameter and not a threshold: it bounds how much precedent a pack
#: carries and nothing else.
PRECEDENT_K = 5

#: The deterministic query text logged into every judge pack beside the slice it
#: selected.  It is rendered with ``standard_id``, ``k`` and the excluded cells,
#: and it says in so many words that the order is registration order and never a
#: ranking by merit.
PRECEDENT_QUERY = (
    "select, in this order and no other: (1) every registered artifact whose "
    "`{field}` is `{appellate}`, in registration order; then (2) every registered "
    "artifact whose `{field}` is `{reading}` or `{mark}`, whose `standard` is "
    "`{standard_id}`, whose adjudicated status is `{standing}`, and whose `key` is "
    "not one of {excluded}, in registration order. Concatenate the two groups in "
    "that order and take the first {k}. Appellate rulings rank first because they "
    "are precedent, not because they are better: registration order is an ordering "
    "and never a ranking by merit, no two precedents are compared, and nothing here "
    "is a quantity."
)

#: The two kinds of precedent a slice can hold, in the rank order it holds them.
PRECEDENT_KINDS: tuple[str, ...] = ("appellate_ruling", "reading")

#: Mirrors ``graph.RECORD_FIELD`` / ``obligations.RECORD_FIELD``, and the three
#: ``graph.RECORD_KINDS`` tokens a precedent can carry.  Mirrored rather than
#: imported so that this module's dependency set stays the wave plan's three;
#: ``tests/loop/test_packs.py`` imports both modules and asserts every one.
RECORD_FIELD = "record"
RECORD_APPELLATE_RULING = "appellate_ruling"
RECORD_READING_ROW = "reading_row"
RECORD_CELL_MARK = "cell_mark"

#: Mirrors ``obligations.STANDING``: the adjudicated label an artifact must carry
#: to be selected as precedent.  Selection is the program's; the pack shows no
#: status token for any precedent.
STANDING = "accepted"

#: Mirrors ``graph.CellKey``'s segment separator, so a caller may hand
#: :func:`render_register` a canonical cell token and get the cell's own id out
#: of it.  Minting a key is W1-GRAPH's and W4-READER's; reading one is not.
CELL_KEY_SEPARATOR = "|"

#: Keys no pack part may carry: a pack never shows a seat the state of the
#: graph.  Disjoint from every role schema's own property names on purpose —
#: ``sustained``, ``mark`` and ``relation`` are what a seat is asked *for*, and
#: the output contract embedded in a pack has to be able to name them.
FORBIDDEN_PACK_KEYS: frozenset[str] = frozenset({
    "accepted",
    "adjudication",
    "att",
    "atts",
    "attack",
    "attacks",
    "cell_state",
    "dep",
    "deps",
    "dependence",
    "labels",
    "refuted",
    "standing",
    "status",
    "statuses",
    "suspended",
    "undecided",
})

_INLINE_PREFIX = "inline:"
_HEX = "0123456789abcdef"


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------


def _string(value: Any, where: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise _refuse(PACK_INPUT_INVALID, f"{where} must be a string")
    if not allow_empty and not value.strip():
        raise _refuse(PACK_INPUT_INVALID, f"{where} is empty")
    return value


def _sha256_hex(value: Any, where: str) -> str:
    text = _string(value, where)
    if len(text) != 64 or any(char not in _HEX for char in text):
        raise _refuse(PACK_INPUT_INVALID, f"{where} is not a sha256 hex digest")
    return text


def _mapping(value: Any, where: str) -> Mapping[str, Any]:
    """A mapping, or an object that publishes one through ``as_dict()``."""

    if isinstance(value, Mapping):
        return value
    as_dict = getattr(value, "as_dict", None)
    if callable(as_dict):
        candidate = as_dict()
        if isinstance(candidate, Mapping):
            return candidate
    raise _refuse(
        PACK_INPUT_INVALID,
        f"{where} must be a mapping or an object with as_dict()",
    )


def _plain(value: Any) -> Any:
    """A JSON-shaped deep copy: plain dicts, lists and scalars, nothing else."""

    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _bullets(lines: Iterable[str]) -> str:
    rendered = [f"- {line}" for line in lines]
    return "\n".join(rendered) if rendered else "- (none)"


def _json_block(value: Any) -> str:
    """A structure rendered for a seat to read: stable, sorted, indented."""

    return json.dumps(_plain(value), ensure_ascii=False, indent=2, sort_keys=True)


def _starts(hay: str, needle: str) -> tuple[int, ...]:
    """Every start offset of ``needle`` in ``hay``, **overlapping**.

    ``str.count`` counts non-overlapping occurrences, so it calls ``aa`` unique
    in ``aaa`` and a resolved span would then be an arbitrary one of two.  This
    is strictly stronger and never weaker.
    """

    found: list[int] = []
    index = hay.find(needle)
    while index != -1:
        found.append(index)
        index = hay.find(needle, index + 1)
    return tuple(found)


# --------------------------------------------------------------------------
# G12 and the adjudication-key scan
# --------------------------------------------------------------------------


def assert_no_adjudication_keys(value: Any, path: Sequence[str] = ()) -> None:
    """Refuse a pack part that carries an ``att``, a ``dep``, a status or a label.

    §2.3: *a pack never contains a label, an* ``att``\\ *, a* ``dep``\\ *, a
    status, another cell's outcome, or another seat's output.*  This is the key
    half of that rule, run over the structured parts of every pack.  Values are
    not inspected: a *word* is not a key, exactly as
    :func:`~minireason.loop.contracts.assert_no_scoring_keys` admits a scoring
    word in a value.

    Raises :class:`PackError` with :data:`PACK_ADJUDICATION_KEY`.  Pure.
    """

    if isinstance(value, Mapping):
        for key, item in value.items():
            here = (*path, str(key))
            if str(key).lower() in FORBIDDEN_PACK_KEYS:
                raise _refuse(PACK_ADJUDICATION_KEY, "/".join(here))
            assert_no_adjudication_keys(item, here)
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            assert_no_adjudication_keys(item, (*path, str(index)))


def assert_pack_clean(pack: "Pack") -> None:
    """Run G12 and the adjudication-key scan over one rendered pack.

    Three scans, on three different subjects, because G12's own subjects are
    three (§2.4: "every emitted artifact, every table header and every rendered
    file"):

    * :func:`~minireason.loop.contracts.assert_no_scoring_keys` over the pack's
      **structured parts** — the keys this module chose;
    * :func:`~minireason.loop.standard.assert_no_scoring_headers` over the
      pack's **own heading lines** — its title and its ``##`` headings, and not
      the material, which is quoted matter and not this loop's to edit
      (deviation 7);
    * :func:`assert_no_adjudication_keys` over the parts again, for §2.3's
      "never a label, an ``att``, a ``dep``, a status".

    and one more over the authored instruction prose:
    :func:`~minireason.loop.standard.assert_no_exhaustion_claim`, so a pack
    cannot be the first generated record to describe a boundary as the inquiry
    running out.  It is called on this module's own instructions only.

    Raises whatever the scan raises — ``ScoringKeyForbidden``,
    ``StandardInvalid`` or :class:`PackError` — and returns ``None``.  Pure.
    """

    parts = pack.as_dict()
    assert_no_scoring_keys(parts)
    assert_no_adjudication_keys(parts)
    assert_no_scoring_headers(pack.headings, f"{pack.role} pack")
    for block in pack.blocks:
        if block.kind == "instruction":
            assert_no_exhaustion_claim(block.body, f"{pack.role} pack instruction")


# --------------------------------------------------------------------------
# The exchange surface E — G2(b)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ExchangeOffset:
    """Where one ``decisive_point`` resolved in one exchange.

    ``start``/``end`` are **code-point** offsets into :attr:`Exchange.text`; see
    the module note on the two coordinate systems.  ``part`` is the exchange
    part the span lies in — a member of :data:`EXCHANGE_PARTS`,
    :data:`PARAPHRASE_PART`, or :data:`JOIN_PART` for a span that crosses the
    separator and therefore quotes across the join.
    """

    start: int
    end: int
    part: str
    exchange_digest: str

    @property
    def length(self) -> int:
        return self.end - self.start

    @property
    def spans_join(self) -> bool:
        """True where the point quotes across ``"\\n"``, taking in both parts."""

        return self.part == JOIN_PART

    def as_dict(self) -> dict[str, Any]:
        return {
            "start": self.start,
            "end": self.end,
            "part": self.part,
            "exchange_digest": self.exchange_digest,
        }


@dataclass(frozen=True)
class Exchange:
    """The surface G2(b) resolves a ``decisive_point`` against.

    ``E = case + "\\n" + answer`` for a trial, and the single paraphrase text for
    a paraphrase spot-check.  Both are the same shape so that G2(b) has one
    implementation for both: the guard does not become a different guard because
    the text under it was restated.

    :attr:`source_digest` is empty on a trial exchange and carries the digest of
    the exchange a paraphrase paraphrases, so a spot-check's record says what it
    was a spot-check *of*.
    """

    parts: tuple[str, ...]
    labels: tuple[str, ...]
    source_digest: str = ""
    schema: str = EXCHANGE_SCHEMA

    def __post_init__(self) -> None:
        if len(self.parts) != len(self.labels) or not self.parts:
            raise PackError(EXCHANGE_MALFORMED, "an exchange is its parts and their labels")
        for label, part in zip(self.labels, self.parts):
            if not isinstance(part, str) or not part.strip():
                raise PackError(EXCHANGE_MALFORMED, f"{label} is empty or not a string")

    # -- identity -------------------------------------------------------

    @property
    def text(self) -> str:
        """The surface itself: the parts joined by :data:`EXCHANGE_SEPARATOR`."""

        return EXCHANGE_SEPARATOR.join(self.parts)

    @property
    def digest(self) -> str:
        """``sha256`` of :attr:`text` as utf-8, hex.  A pure function of it."""

        return sha256_hex(self.text.encode("utf-8"))

    @property
    def is_paraphrase(self) -> bool:
        return bool(self.source_digest)

    @property
    def case(self) -> str:
        """The case, on a trial exchange; ``""`` on a paraphrase."""

        return self.parts[0] if self.labels == EXCHANGE_PARTS else ""

    @property
    def answer(self) -> str:
        """The answer, on a trial exchange; ``""`` on a paraphrase."""

        return self.parts[1] if self.labels == EXCHANGE_PARTS else ""

    def __len__(self) -> int:
        return len(self.text)

    # -- search ---------------------------------------------------------

    def occurrences(self, point: Any) -> tuple[int, ...]:
        """Every start offset of ``point`` in :attr:`text`, counted overlapping.

        An empty point designates nothing and has no occurrences.
        """

        if not isinstance(point, str):
            raise PackError(EXCHANGE_MALFORMED, "a decisive point is a string")
        if not point:
            return ()
        return _starts(self.text, point)

    def count(self, point: Any) -> int:
        """``E.count(d)`` of G2(b), counted overlapping.  See the module note."""

        return len(self.occurrences(point))

    def conforming(self, point: Any) -> bool:
        """The **vendored** predicate: ``decisive in exchange``, and no more.

        Kept beside :meth:`count` so that W3-TRIAL can assert the program's own
        stronger check first and this one last, which is what keeps the guard
        and ``graph.register_transcript``'s registration gate from diverging.
        """

        return isinstance(point, str) and bool(point) and point in self.text

    def side_at(self, start: int, end: int) -> str:
        """Which part ``[start, end)`` lies in, or :data:`JOIN_PART`."""

        cursor = 0
        for label, part in zip(self.labels, self.parts):
            lower, upper = cursor, cursor + len(part)
            if lower <= start and end <= upper:
                return label
            cursor = upper + len(EXCHANGE_SEPARATOR)
        return JOIN_PART

    def resolve(self, point: Any) -> ExchangeOffset | None:
        """G2(b): the one place ``point`` occurs in this exchange, or ``None``.

        ``None`` is returned for zero occurrences **and** for more than one —
        both are ``blocked:referential-integrity`` on this surface, and
        :meth:`count` says which, for the transcript.  The match is an exact
        search: nothing is trimmed, folded or normalised.
        """

        found = self.occurrences(point)
        if len(found) != 1:
            return None
        start = found[0]
        end = start + len(point)
        return ExchangeOffset(
            start=start,
            end=end,
            part=self.side_at(start, end),
            exchange_digest=self.digest,
        )

    # -- record ---------------------------------------------------------

    def as_dict(self) -> dict[str, Any]:
        record = {
            "schema": self.schema,
            "digest": self.digest,
            "characters": len(self.text),
            "parts": list(self.labels),
            "separator": EXCHANGE_SEPARATOR,
            "source_digest": self.source_digest,
        }
        assert_no_scoring_keys(record)
        return record


def exchange_surface(case: Any, answer: Any) -> Exchange:
    """``E = case + "\\n" + answer``, as a first-class surface (wave-1 **S4**).

    The one construction of G2(b)'s surface in the package: W3-TRIAL, W3-AUDITS
    and W4-READER all resolve a ``decisive_point`` through the object this
    returns, so there is no second spelling of ``E`` to drift from this one.
    ``graph.Transcript.exchange`` builds the same string for the registration
    gate; a test asserts the two agree byte for byte.

    Raises :class:`PackError` with :data:`EXCHANGE_MALFORMED` for a missing or
    blank part — a trial with no case or no answer has no exchange to guard.
    """

    return Exchange(parts=(_ex(case, "case"), _ex(answer, "answer")), labels=EXCHANGE_PARTS)


def _ex(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PackError(EXCHANGE_MALFORMED, f"{where} is empty or not a string")
    return value


def paraphrase_surface(paraphrase: Any, *, of: Exchange) -> Exchange:
    """One variator paraphrase, as the surface G2(b) re-runs against.

    The paraphrase stands for the whole exchange — §2.3's variator paraphrases
    ``case + answer`` and returns one string per paraphrase — so it is a
    one-part exchange carrying the digest of the exchange it restates.  *The
    material is never paraphrased*: nothing of ``M`` is here.
    """

    if not isinstance(of, Exchange):
        raise PackError(EXCHANGE_MALFORMED, "a paraphrase paraphrases an Exchange")
    return Exchange(
        parts=(_ex(paraphrase, "paraphrase"),),
        labels=(PARAPHRASE_PART,),
        source_digest=of.digest,
    )


def held_spans_of(critic: Any) -> tuple[str, ...]:
    """The spans a paraphrase must reproduce byte-identically.

    §2.3: *quoted spans are extracted, held out of the paraphrase, re-inserted
    byte-identically, and their survival asserted by program*.  The quoted span
    of a trial is the critic's ``passage_quote``, and this is the one place it is
    read off, so the pack's held-span list and the survival check cannot drift.
    Returns ``()`` where the critic quoted nothing — a critic answering ``none``
    ends the row at one call and there is no paraphrase to guard.
    """

    quote = getattr(critic, "passage_quote", None)
    if quote is None and isinstance(critic, Mapping):
        quote = critic.get("passage_quote")
    if isinstance(quote, str) and quote:
        return (quote,)
    return ()


# --------------------------------------------------------------------------
# Blocks and packs
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Block:
    """One labelled region of a pack: a heading this module wrote, and a body.

    ``kind`` is a member of :data:`BLOCK_KINDS`.  A block of kind
    :data:`SIDE_KIND` is one of the two sides of a pairwise pack and is what
    G6's order swap moves.  ``anonymous`` marks a side whose heading is a
    *position* (``side A``) rather than a name: on a swap its body and ``slot``
    move and its heading stays, which is G6's "labels reassigned".

    The field is ``name`` and not *label*: §2.3 says a pack never contains a
    label, and a record key spelled that way invites exactly the confusion
    between a heading and an adjudication label that the rule is about.
    """

    kind: str
    name: str
    body: str
    slot: str = ""
    anonymous: bool = False

    @property
    def heading(self) -> str:
        return f"{HEADING_PREFIX}{self.name}"

    @property
    def text(self) -> str:
        return f"{self.heading}\n{self.body}"

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "name": self.name,
            "slot": self.slot,
            "anonymous": self.anonymous,
            "characters": len(self.body),
        }


@dataclass(frozen=True)
class Pack:
    """One rendered pack: what a seat is shown, and the record of it.

    :attr:`text` is what goes to the seat.  :meth:`as_dict` is the record —
    the structured parts, the block map and the rendered text — and
    :meth:`canonical_bytes` is what :func:`pack_sha` addresses, so two renders
    from identical inputs carry the same digest and a changed byte anywhere
    changes it.

    The pack is a pure value: it holds no harness, no seat, no clock and no
    path.  Which seat it is sent to is W2-ROLES', and the pack digest is what
    that call record pins.
    """

    role: str
    title: str
    blocks: tuple[Block, ...]
    parts: Mapping[str, Any] = field(default_factory=dict)
    exchange: Exchange | None = None
    #: The parsed standard body this pack quoted its rubric out of.  Carried so
    #: that a pack rendered downstream of this one quotes the **same** frozen
    #: body, and deliberately **not** in :meth:`as_dict`: the record pins the
    #: standard by digest, and a pack that carried the whole standard twice
    #: would be addressing a copy rather than the artifact.
    standard: Mapping[str, Any] | None = None
    schema: str = PACKS_SCHEMA

    # -- rendering ------------------------------------------------------

    @property
    def text(self) -> str:
        """The pack as the seat sees it."""

        head = f"{TITLE_PREFIX}{self.title}"
        return BLOCK_SEPARATOR.join([head, *(block.text for block in self.blocks)])

    @property
    def headings(self) -> str:
        """This module's **own** heading lines, and nothing of the material.

        The subject of :func:`~minireason.loop.standard.assert_no_scoring_headers`
        for this pack (deviation 7).
        """

        return "\n".join(
            [f"{TITLE_PREFIX}{self.title}", *(block.heading for block in self.blocks)]
        )

    # -- identity -------------------------------------------------------

    def canonical_bytes(self) -> bytes:
        """The bytes :func:`pack_sha` hashes: canonical JSON of :meth:`as_dict`."""

        return canonical_json(self.as_dict())

    @property
    def sha(self) -> str:
        """``sha256`` of :meth:`canonical_bytes`, hex — the pack's address."""

        return sha256_hex(self.canonical_bytes())

    # -- read-back ------------------------------------------------------

    def block(self, kind: str) -> Block | None:
        """The first block of that kind, or ``None``."""

        for block in self.blocks:
            if block.kind == kind:
                return block
        return None

    @property
    def material(self) -> str:
        """The embedded surface, byte for byte, or ``""`` where there is none."""

        block = self.block("material")
        return block.body if block is not None else ""

    @property
    def material_digest(self) -> str:
        """The embedded surface's own ``sha256``, or ``""``."""

        subject = self.parts.get("subject", {})
        value = subject.get("surface_sha256", "") if isinstance(subject, Mapping) else ""
        return value if isinstance(value, str) else ""

    @property
    def order(self) -> str:
        """Which of :data:`ORDERS` this pack is presented in."""

        presentation = self.parts.get("presentation")
        if isinstance(presentation, Mapping):
            value = presentation.get("order")
            if isinstance(value, str):
                return value
        return ORDER_AS_DECLARED

    @property
    def is_pairwise(self) -> bool:
        """True where this pack has two sides, and so a swap to run (G6)."""

        return sum(1 for block in self.blocks if block.kind == SIDE_KIND) == 2

    # -- G6 -------------------------------------------------------------

    def swap(self) -> "Pack":
        """The same pack in the other presentation order (G6).

        An involution: ``pack.swap().swap()`` renders the pack it started from,
        byte for byte, and the two orders carry different digests, so the record
        of a pairwise judgement says which order produced which ruling.

        A named side (the case, the answer) travels with its label, because the
        label says what the body *is*.  An anonymous side (``side A``, ``side
        B``) keeps its label and exchanges its body and its arm, which is G6's
        "with labels reassigned"; the alias-to-arm map in the record is
        recomputed so a program can still de-alias the quotes it gets back.
        """

        if not self.is_pairwise:
            raise _refuse(
                PACK_INPUT_INVALID,
                f"a {self.role} pack has no two sides to swap",
            )
        blocks = list(self.blocks)
        where = [index for index, block in enumerate(blocks) if block.kind == SIDE_KIND]
        first, second = blocks[where[0]], blocks[where[1]]
        if first.anonymous or second.anonymous:
            blocks[where[0]] = replace(first, body=second.body, slot=second.slot)
            blocks[where[1]] = replace(second, body=first.body, slot=first.slot)
        else:
            blocks[where[0]], blocks[where[1]] = second, first
        parts = _plain(self.parts)
        presentation = parts.setdefault("presentation", {})
        order = ORDER_SWAPPED if self.order == ORDER_AS_DECLARED else ORDER_AS_DECLARED
        presentation["order"] = order
        presentation["swap_recorded"] = order == ORDER_SWAPPED
        aliases = {
            alias: blocks[index].slot
            for alias, index in zip(ALIASES, where)
            if blocks[index].anonymous
        }
        if aliases:
            presentation["side_aliases"] = aliases
        return Pack(
            role=self.role,
            title=self.title,
            blocks=tuple(blocks),
            parts=parts,
            exchange=self.exchange,
            standard=self.standard,
            schema=self.schema,
        )

    # -- record ---------------------------------------------------------

    def as_dict(self) -> dict[str, Any]:
        """The pack record: its parts, its block map and its rendered text.

        The text rides whole, because the pack's digest has to address what the
        seat was actually shown and not a summary of it.  G12 is run over the
        keys before it is returned.
        """

        record = {
            "schema": self.schema,
            "role": self.role,
            "title": self.title,
            "blocks": [block.as_dict() for block in self.blocks],
            "parts": _plain(self.parts),
            "text": self.text,
        }
        assert_no_scoring_keys(record)
        return record


def pack_sha(pack: Pack) -> str:
    """The pack's content address: ``sha256`` of its canonical bytes.

    This is the digest W2-ROLES pins into every call record and W3-TRIAL pins
    into the trial transcript, so what a seat was shown is recoverable from the
    record long after the call.  Two renders from identical inputs return the
    same digest; one changed byte anywhere — in the material, in the rubric, in
    the precedent query, in the presentation order — changes it.
    """

    if not isinstance(pack, Pack):
        raise _refuse(PACK_INPUT_INVALID, "pack_sha takes a Pack")
    return pack.sha


def both_orders(pack: Pack) -> tuple[Pack, Pack]:
    """The pairwise pack in both presentation orders (G6), as-declared first.

    ``order_swap_both_orders`` is a pinned guard parameter, so this is not an
    option a caller may decline: every pairwise judgement is run twice and a
    different real outcome is ``blocked:order-swap``.
    """

    if pack.order == ORDER_AS_DECLARED:
        return (pack, pack.swap())
    return (pack.swap(), pack)


# --------------------------------------------------------------------------
# The standard, as a pack reads it
# --------------------------------------------------------------------------


def _standard(value: Any) -> tuple[dict[str, Any], str]:
    """The parsed standard body and the sha256 of its canonical bytes.

    Accepts the bytes :func:`standard.build_standard` emits, the same text, or
    the parsed mapping.  Every acceptance runs through
    :func:`~minireason.loop.standard.standard_body`, which refuses a body that is
    not this standard, so a pack cannot quote a rubric from somewhere else.
    """

    if isinstance(value, (bytes, bytearray, str)):
        parsed = standard_body(value)
    elif isinstance(value, Mapping):
        parsed = standard_body(canonical_json(_plain(value)))
    else:
        raise _refuse(
            PACK_INPUT_INVALID,
            "a standard is its bytes, its text, or its parsed body",
        )
    return parsed, sha256_hex(canonical_json(parsed))


def _standard_parts(parsed: Mapping[str, Any], digest: str, rubric_id: str) -> dict[str, Any]:
    return {
        "name": parsed.get("standard_name", STANDARD_NAME),
        "spec_id": parsed.get("spec_id", SPEC_ID),
        "schema": parsed.get("schema", STANDARD_SCHEMA),
        "sha256": digest,
        "rubric_class": rubric_id,
        "mode": parsed["rubric"][rubric_id]["mode"],
    }


def _rubric_block(parsed: Mapping[str, Any], rubric_id: str) -> Block:
    rubric = parsed["rubric"][rubric_id]
    body = "\n".join(
        [
            f"question: {rubric['question']}",
            f"mode: {rubric['mode']}",
            "",
            rubric["body"],
        ]
    )
    return Block(
        kind="rubric",
        name=(
            f"the reading rubric of {parsed.get('standard_name', STANDARD_NAME)} "
            f"({rubric_id}, {rubric['mode']} mode)"
        ),
        body=body,
    )


def _vocabulary_block(parsed: Mapping[str, Any]) -> Block:
    vocabulary = parsed["vocabulary"]
    body = "\n".join(
        [
            "the closed values for this run:",
            _bullets(vocabulary["values"]),
            "",
            f"a critic may nominate: {', '.join(vocabulary['nominable_relations'])}, "
            f"or `{vocabulary['none_token']}`.",
            "",
            f"`{vocabulary['outside_vocabulary_field']}`: "
            f"{vocabulary['outside_vocabulary_effect']}",
            "",
            "the instrument's own published note on this vocabulary, verbatim:",
            "",
            vocabulary["published_note"],
        ]
    )
    return Block(kind="vocabulary", name="the closed vocabulary", body=body)


def _banner_block(parsed: Mapping[str, Any]) -> Block:
    banner = parsed["vocabulary"]["instrument_banner"]
    if banner != READING_BANNER:
        raise _refuse(
            PACK_INPUT_INVALID,
            "the standard's instrument banner is not the instrument's own",
        )
    return Block(
        kind="banner",
        name="the instrument's banner, verbatim",
        body=banner,
    )


def _contract_block(role: str, *, register: str | None = None) -> Block:
    schema = schema_for(role)
    if register is not None:
        schema["properties"]["difference_kind"]["enum"] = [
            *difference_kinds_for(register),
            None,
        ]
    limits = [
        f"`{field}`: at most {limit} whitespace-separated words"
        for (owner, field), limit in sorted(WORD_LIMITS.items())
        if owner == role
    ]
    body = "\n".join(
        [
            "Answer with one JSON object and nothing else. It is validated against "
            "this schema exactly; an invalid answer is `unresolved` and is not re-asked.",
            "",
            _json_block(schema),
            "",
            "declared length bounds:",
            _bullets(limits or ["(none declared for this role)"]),
            "",
            "A length bound is a declared resource bound. No two answers' lengths are "
            "ever compared, and a length is never a reading.",
        ]
    )
    return Block(kind="contract", name="your answer", body=body)


def _material_block(material: str, digest: str) -> Block:
    return Block(
        kind="material",
        name=f"the resolvable material, sha256 {digest}",
        body=material,
    )


# --------------------------------------------------------------------------
# The instructions this module authors
# --------------------------------------------------------------------------

CRITIC_INSTRUCTION = (
    "Draft the strongest case that exactly one named relation holds between the "
    "referring record and the target record, read on the frozen material below and "
    "on nothing else, quoting a passage of that material verbatim; or answer `none`.\n"
    "\n"
    "The quoted passage must occur **exactly once** in the material and must lie "
    "wholly inside the referring record, the target record or one listed referring "
    "body passage. A quote of this pack's own headings, instruction, vocabulary "
    "list, banner or framing is void: a reading grounded in the prompt's own "
    "scaffolding is not a reading of the material.\n"
    "\n"
    "Bind the four criticism constituents by name in `role_bindings`. A shared "
    "wording is not a use: a lexical overlap sustains nothing on its own.\n"
    "\n"
    "If the reading you want is not one of the closed values, leave `relation` as "
    "`none` and write the reading into `outside_vocabulary`; your text is preserved "
    "unaltered and the cell stays unresolved. `none` ends this row at this one call."
)

DEFENDER_INSTRUCTION = (
    "Answer the case below. The position you defend is that the juxtaposition does "
    "not establish the claimed relation.\n"
    "\n"
    "Answer on the frozen material below and on nothing else. You are not asked who "
    "is right and no ruling is yours to make; you are asked for the answer the case "
    "has to survive. Set `concedes` only if you have no answer to give."
)

JUDGE_INSTRUCTION = (
    "Rule on one question and no other: does the cited passage, read on the frozen "
    "material below and on nothing else, establish the relation the case names?\n"
    "\n"
    "`decisive_point` must be an **exact substring of the case followed by a newline "
    "followed by the answer**, and it must occur exactly once in that text. A point "
    "that quotes the material rather than the exchange, or that occurs twice, or that "
    "occurs nowhere, registers nothing: it is the difference between pointing at the "
    "argument and pointing at yourself.\n"
    "\n"
    "The strongest positive outcome available here is *consistent-with*. A sustained "
    "relation is not a witness of reason use. `unresolved` is a first-class outcome "
    "and non-evaluability is not refutation.\n"
    "\n"
    "You are one occasion, not a contestant. No other seat's ruling is shown to you, "
    "no ruling of yours is compared with another's, and nothing here is a quantity."
)

MARKER_INSTRUCTION = (
    "Mark **one** register of **one** comparison of **one** cell. You are shown one "
    "register's definition and you may not trade it against another; no call sees a "
    "second register, and the registers are never summed, averaged, weighted, ranked "
    "or reduced to one mark.\n"
    "\n"
    "The two sides are shown as `A` and `B`. Nothing here says which side is which "
    "arm, and this pack's presentation order is recorded outside it: the same "
    "comparison is put to you in both orders, and a mark that changes with the order "
    "is not a mark.\n"
    "\n"
    "`differs` only where this register's definition says the two sides differ, with "
    "the closed `difference_kind` token that names how. Quote the two sides you read. "
    "Where you cannot tell, answer `unresolved`: absent data is reported as absent "
    "data and never as an absence of difference."
)

VARIATOR_INSTRUCTION = (
    "Restate the exchange below {n} times. Each restatement must say the same thing "
    "in different words.\n"
    "\n"
    "Every held span listed below must appear in every restatement **byte for byte**: "
    "hold it out of the restatement and put it back unchanged. A restatement that "
    "alters a held span is discarded and the spot-check it was for is recorded as not "
    "performed.\n"
    "\n"
    "The material is never restated and is not shown here: its bytes are what the "
    "citations resolve against, and they do not change because an argument about them "
    "was put another way."
)


def _instruction_block(text: str) -> Block:
    return Block(kind="instruction", name="what you are asked", body=text)


# --------------------------------------------------------------------------
# render_row — the critic pack
# --------------------------------------------------------------------------


def _framing_block(surface: Surface, framing: Any) -> tuple[Block, dict[str, Any]]:
    """The §2.3 framing: uptake booleans, resolver notes, the overlap note.

    Everything here is the instrument's own mechanical output about the ref that
    made this juxtaposition.  Nothing is inferred and nothing is invented: a
    field the row does not carry is reported as ``null``, which is the
    instrument saying it did not say.
    """

    row: Mapping[str, Any] = {} if framing is None else _mapping(framing, "framing")

    def flag(key: str) -> Any:
        value = row.get(key)
        return value if isinstance(value, bool) else None

    notes: list[dict[str, str]] = []
    for entry in row.get("resolver_notes") or ():
        note = _mapping(entry, "framing.resolver_notes[]")
        notes.append(
            {
                "code": str(note.get("code", "")),
                "reason": str(note.get("reason", "")),
            }
        )

    parts = {
        "ref_field": surface.ref_field,
        "ref_verbatim": surface.ref_verbatim,
        "ref_grain": surface.ref_grain,
        "declared_uptake_includes_referring_record": flag(
            "declared_uptake_includes_referring_record"
        ),
        "declared_uptake_includes_target_record": flag(
            "declared_uptake_includes_target_record"
        ),
        "overlap_subject": str(row.get("overlap_subject", "")),
        "lexical_overlap_note": str(row.get("lexical_overlap_note", "")),
        "resolver_notes": notes,
    }

    def shown(value: Any) -> str:
        return "null" if value is None else ("true" if value is True else "false")

    lines = [
        f"the ref that made this juxtaposition: `{surface.ref_field}` = "
        f"{surface.ref_verbatim!r} (grain: {surface.ref_grain})",
        "declared uptake includes the referring record: "
        + shown(parts["declared_uptake_includes_referring_record"]),
        "declared uptake includes the target record: "
        + shown(parts["declared_uptake_includes_target_record"]),
    ]
    if parts["overlap_subject"]:
        lines.append(f"what the target's text was taken to be: {parts['overlap_subject']}")
    if parts["lexical_overlap_note"]:
        lines.append(f"lexical overlap note, verbatim: {parts['lexical_overlap_note']}")
    body = "\n".join(
        [
            _bullets(lines),
            "",
            "resolver notes, verbatim:",
            _bullets([f"`{note['code']}`: {note['reason']}" for note in notes]),
        ]
    )
    return Block(kind="framing", name="the framing", body=body), parts


def render_row(surface: Any, standard: Any, framing: Any = None) -> Pack:
    """The critic's pack for one juxtaposition row (§2.3).

    ``surface`` is the :class:`~minireason.loop.surface.Surface` W1-SURFACE built
    from the published use-relation row; ``standard`` is the pinned standard
    body (bytes, text or its parsed mapping); ``framing`` is that row's uptake
    booleans, resolver notes and lexical-overlap note, as a mapping or as the
    instrument's own ``UseRow``.

    The material is embedded as :attr:`Surface.decoded` **byte for byte** and its
    :attr:`Surface.digest` is in the pack's own heading, so the digest is inside
    the pack text and therefore inside the pack digest: wave-1 open question
    **S5** asks that a changed surface-label vocabulary be visible in a diff, and
    it is.

    Pure and byte-stable: two calls on the same arguments return packs with the
    same :func:`pack_sha`.  Raises :class:`PackError` with
    :data:`PACK_INPUT_INVALID` for anything that is not a surface or a standard,
    and ``StandardInvalid`` for a body that is not this standard.
    """

    if not isinstance(surface, Surface):
        raise _refuse(PACK_INPUT_INVALID, "render_row takes a Surface")
    parsed, digest = _standard(standard)
    rubric_id = RUBRIC_FOR_ROLE[ROLE_CRITIC]
    framing_block, framing_parts = _framing_block(surface, framing)

    blocks = (
        _instruction_block(CRITIC_INSTRUCTION),
        _rubric_block(parsed, rubric_id),
        _vocabulary_block(parsed),
        _banner_block(parsed),
        _material_block(surface.decoded, surface.digest),
        framing_block,
        _contract_block(ROLE_CRITIC),
    )
    parts = {
        "standard": _standard_parts(parsed, digest, rubric_id),
        "subject": {
            "surface_sha256": surface.digest,
            "surface_schema": surface.schema,
            "surface_bytes": len(surface.text),
            "referring_coordinate_key": surface.referring_coordinate_key,
            "target_coordinate_key": surface.target_coordinate_key,
            "referring_record_id": surface.referring_record_id,
            "target_record_id": surface.target_record_id,
            "declared_sides": [span.side for span in surface.spans],
        },
        "framing": framing_parts,
        "word_limits": {
            field: limit
            for (owner, field), limit in sorted(WORD_LIMITS.items())
            if owner == ROLE_CRITIC
        },
    }
    pack = Pack(
        role=ROLE_CRITIC,
        title=f"critic pack — {surface.referring_coordinate_key} "
        f"-> {surface.target_coordinate_key}",
        blocks=blocks,
        parts=parts,
        standard=parsed,
    )
    assert_pack_clean(pack)
    return pack


# --------------------------------------------------------------------------
# render_exchange — the defender pack and the judge pack
# --------------------------------------------------------------------------


def _claim_block(critic: Any) -> tuple[Block, dict[str, Any]]:
    relation = getattr(critic, "relation", None)
    quote = getattr(critic, "passage_quote", None)
    if relation is None and isinstance(critic, Mapping):
        relation = critic.get("relation")
        quote = critic.get("passage_quote")
    relation = _string(relation, "critic.relation")
    quote = _string(quote, "critic.passage_quote")
    body = "\n".join(
        [
            f"the relation the case names: `{relation}`",
            "",
            "the passage the case cites, verbatim from the material:",
            "",
            quote,
        ]
    )
    return (
        Block(kind="claim", name="the claim under trial", body=body),
        {"relation": relation, "passage_quote": quote},
    )


def _case_of(critic: Any) -> str:
    value = getattr(critic, "case", None)
    if value is None and isinstance(critic, Mapping):
        value = critic.get("case")
    return _string(value, "critic.case")


def _answer_of(defender: Any) -> str:
    value = getattr(defender, "answer", None)
    if value is None and isinstance(defender, Mapping):
        value = defender.get("answer")
    return _string(value, "defender.answer")


def _precedent_block(slice_: "PrecedentSlice") -> Block:
    entries = [
        "\n".join(
            [
                f"precedent {entry.position} ({entry.kind}):",
                *([f"  cell: {entry.cell}"] if entry.cell else []),
                *([f"  read as: `{entry.relation}`"] if entry.relation else []),
                *([f"  ground: {entry.ground}"] if entry.ground else []),
            ]
        )
        for entry in slice_
    ]
    body = "\n".join(
        [
            "the query that selected this slice, logged verbatim:",
            "",
            slice_.query,
            "",
            ("\n\n".join(entries) if entries else "no precedent is on record under this "
             "standard. That is a fact about the record and nothing else follows from it."),
        ]
    )
    return Block(kind="precedent", name="the precedent slice", body=body)


def render_exchange(
    pack: Pack,
    critic: Any,
    defender: Any = None,
    *,
    precedents: "PrecedentSlice | None" = None,
    order: str = ORDER_AS_DECLARED,
    offset: Any = None,
    exchange: Exchange | None = None,
) -> Pack:
    """The defender's pack, or the judge's, from the row pack the critic saw.

    With ``defender=None`` this renders the **defender** pack: ``M``, the claim
    under trial with its citation, and the critic's case (§2.3).  With a
    defender it renders the **judge** pack, which adds the answer and the
    precedent slice.  Deviation 1 explains why one renderer covers both.

    The material block is carried over from ``pack`` unchanged, which is what
    makes the bytes reaching the judge identical to the bytes reaching the critic
    (wave-1 open question **S7**); the material is never paraphrased and is never
    re-rendered.

    ``precedents`` is required for a judge pack and must be the
    :class:`PrecedentSlice` :func:`precedent_slice` returned, because the
    acceptance clause requires the query text to be recorded *with the pack*.
    ``order`` presents the case and the answer in either order (G6); the
    exchange ``E`` itself is **never** reordered — G2(b) resolves against
    ``case + "\\n" + answer`` whichever way the pack was laid out, or the guard
    would be running over two different surfaces.

    ``offset`` is the resolved :class:`~minireason.loop.surface.Offset` of the
    cited passage, recorded whole into the pack parts when given (wave-1 open
    question **S1**: carry it, never convert it).

    ``exchange`` is G7's re-ruling pack (deviation 9): pass the
    :func:`paraphrase_surface` of the trial's exchange and the judge pack
    presents **one** restated-exchange block in place of the case and the
    answer, with the paraphrase's own digest and the digest of what it restates
    in the record.  A one-sided pack has no presentation order to swap, so
    ``order`` must be :data:`ORDER_AS_DECLARED` there.  The material, the claim,
    the rubric and the precedent slice are unchanged: only the text under trial
    was put another way, which is the whole point of the spot-check.

    Raises :class:`PackError` with :data:`PACK_INPUT_INVALID` or
    :data:`PRECEDENT_QUERY_INVALID`.
    """

    if not isinstance(pack, Pack) or pack.role != ROLE_CRITIC:
        raise _refuse(PACK_INPUT_INVALID, "render_exchange builds on a critic pack")
    if order not in ORDERS:
        raise _refuse(PACK_INPUT_INVALID, f"order {order!r} is not one of {ORDERS}")
    material = pack.block("material")
    banner = pack.block("banner")
    if material is None or banner is None or pack.standard is None:
        raise _refuse(
            PACK_INPUT_INVALID,
            "a row pack carries its material, its banner and the standard it quoted",
        )

    claim_block, claim = _claim_block(critic)
    case = _case_of(critic)
    role = ROLE_DEFENDER if defender is None else ROLE_JUDGE
    parts: dict[str, Any] = {
        "standard": _plain(pack.parts.get("standard", {})),
        "subject": _plain(pack.parts.get("subject", {})),
        "claim": claim,
        "word_limits": {
            field_name: limit
            for (owner, field_name), limit in sorted(WORD_LIMITS.items())
            if owner == role
        },
    }
    if offset is not None:
        parts["citation_offset"] = _plain(_mapping(offset, "offset"))

    if defender is None:
        blocks = (
            _instruction_block(DEFENDER_INSTRUCTION),
            banner,
            claim_block,
            material,
            Block(kind=SIDE_KIND, name="the case", body=case, slot="case"),
            _contract_block(ROLE_DEFENDER),
        )
        built = Pack(
            role=ROLE_DEFENDER,
            title=pack.title.replace("critic pack", "defender pack", 1),
            blocks=blocks,
            parts=parts,
            standard=pack.standard,
        )
        assert_pack_clean(built)
        return built

    if not isinstance(precedents, PrecedentSlice):
        raise _refuse(
            PRECEDENT_QUERY_INVALID,
            "a judge pack records the deterministic query that selected its "
            "precedent slice; pass the PrecedentSlice precedent_slice() returned",
        )
    answer = _answer_of(defender)
    if exchange is None:
        surface = exchange_surface(case, answer)
        case_block = Block(kind=SIDE_KIND, name="the case", body=case, slot="case")
        answer_block = Block(kind=SIDE_KIND, name="the answer", body=answer, slot="answer")
        sides = (
            (case_block, answer_block)
            if order == ORDER_AS_DECLARED
            else (answer_block, case_block)
        )
    else:
        if not isinstance(exchange, Exchange) or not exchange.is_paraphrase:
            raise _refuse(
                PACK_INPUT_INVALID,
                "the re-ruling pack takes the paraphrase_surface() of this trial's "
                "exchange; a trial exchange is built from the case and the answer",
            )
        if exchange.source_digest != exchange_surface(case, answer).digest:
            raise _refuse(
                PACK_INPUT_INVALID,
                "the paraphrase restates a different exchange than this case and "
                "answer; a spot-check of another trial is not a spot-check of this one",
            )
        if order != ORDER_AS_DECLARED:
            raise _refuse(
                PACK_INPUT_INVALID,
                "a restated exchange is one text and has no presentation order to swap",
            )
        surface = exchange
        sides = (
            Block(
                kind="exchange",
                name="the exchange under trial, restated",
                body=exchange.text,
                slot=PARAPHRASE_PART,
            ),
        )
    rubric_id = RUBRIC_FOR_ROLE[ROLE_JUDGE]
    blocks = (
        _instruction_block(JUDGE_INSTRUCTION),
        _rubric_block(pack.standard, rubric_id),
        banner,
        claim_block,
        material,
        *sides,
        _precedent_block(precedents),
        _contract_block(ROLE_JUDGE),
    )
    parts["standard"]["rubric_class"] = rubric_id
    parts["standard"]["mode"] = pack.standard["rubric"][rubric_id]["mode"]
    parts["presentation"] = {"order": order, "swap_recorded": order == ORDER_SWAPPED}
    parts["exchange"] = surface.as_dict()
    parts["held_spans"] = list(held_spans_of(critic))
    parts["precedent"] = precedents.as_dict()
    built = Pack(
        role=ROLE_JUDGE,
        title=pack.title.replace("critic pack", "judge pack", 1),
        blocks=blocks,
        parts=parts,
        exchange=surface,
        standard=pack.standard,
    )
    assert_pack_clean(built)
    return built


# --------------------------------------------------------------------------
# render_register — the marker pack
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class MarkSide:
    """One side of a pairwise comparison: which arm it is, and its bytes.

    ``arm`` is recorded and never rendered; the seat sees :data:`ALIAS_A` or
    :data:`ALIAS_B` and the position it was shown in.
    """

    arm: str
    text: str

    @classmethod
    def coerce(cls, value: Any, where: str) -> "MarkSide":
        if isinstance(value, MarkSide):
            return value
        if isinstance(value, (list, tuple)) and len(value) == 2:
            return cls(arm=_string(value[0], f"{where}.arm"),
                       text=_string(value[1], f"{where}.text"))
        row = _mapping(value, where)
        return cls(
            arm=_string(row.get("arm"), f"{where}.arm"),
            text=_string(row.get("text"), f"{where}.text"),
        )

    def as_dict(self) -> dict[str, str]:
        return {"arm": self.arm, "text": self.text}


def _cell_id(cell: Any) -> str:
    """The cell's own id, however the caller spells a cell key.

    Accepts a string, a mapping with a ``cell`` key, or any object publishing
    ``.cell`` — which is ``graph.CellKey``'s spelling.  Minting a cell key is
    W1-GRAPH's and W4-READER's; this module only needs the name of the cell it
    is rendering for, and never invents one.
    """

    if isinstance(cell, str):
        return _string(cell.split(CELL_KEY_SEPARATOR, 1)[0], "cell")
    value = getattr(cell, "cell", None)
    if value is None and isinstance(cell, Mapping):
        value = cell.get("cell")
    if value is None:
        raise _refuse(PACK_INPUT_INVALID, "a cell is a key, a mapping or an object with .cell")
    return _string(value, "cell")


def _sides_of(cell: Any, sides: Any) -> tuple[MarkSide, MarkSide]:
    if sides is None:
        candidate = getattr(cell, "sides", None)
        if candidate is None and isinstance(cell, Mapping):
            candidate = cell.get("sides")
        sides = candidate
    if not isinstance(sides, (list, tuple)) or len(sides) != 2:
        raise _refuse(
            PACK_INPUT_INVALID,
            "a comparison has exactly two sides; pass sides=(MarkSide, MarkSide)",
        )
    first = MarkSide.coerce(sides[0], "sides[0]")
    second = MarkSide.coerce(sides[1], "sides[1]")
    if first.arm == second.arm:
        raise _refuse(PACK_INPUT_INVALID, "the two sides of a comparison are two arms")
    return first, second


def _register_block(parsed: Mapping[str, Any], register: str) -> Block:
    definition = parsed["registers"][register]
    kinds = [
        f"`{kind['token']}` — {kind['reads']}" for kind in definition["difference_kinds"]
    ]
    body = "\n".join(
        [
            f"register {definition['id']}: {definition['name']}",
            "",
            "PLAN §8a, verbatim:",
            "",
            definition["plan_text"],
            "",
            f"what it reads: {definition['reads']}",
            f"differs iff: {definition['differs_iff']}",
            "",
            "the closed `difference_kind` tokens for this register, and no others:",
            _bullets(kinds),
            "",
            parsed["plan_8a"]["never_aggregated"],
        ]
    )
    return Block(
        kind="register",
        name=f"the one register under this mark: {definition['id']}",
        body=body,
    )


def render_register(
    cell: Any,
    register: str,
    comparison: Any,
    baseline_sha: Any,
    standard: Any,
    *,
    sides: Any = None,
    order: str = ORDER_AS_DECLARED,
) -> Pack:
    """One marker pack: one cell, one comparison, one register, one call (M1).

    G8 is enforced here and nowhere else: ``baseline_sha`` must be a sha256 hex
    digest of the cell's sealed within-ORIGINAL baseline grid, or
    :class:`BaselineNotFirst` is raised and **no pack exists to send**.  The
    digest is pinned into the pack record, so every call record that carries the
    pack digest also carries the baseline's; revising the baseline afterwards
    changes a hash those records already hold.

    The pack carries the baseline's **digest** and never its kind set
    (deviation 5): G9's downgrade of ``differs`` to ``same`` at kind grain is the
    program's work, and a seat shown the frozen kinds would be pre-empting it.

    The two sides are shown as ``A`` and ``B``; which arm each one is lives in
    ``parts["presentation"]["side_aliases"]``.  Run both orders with
    :func:`both_orders`.

    Raises :class:`BaselineNotFirst`, or :class:`PackError` with
    :data:`PACK_INPUT_INVALID` for an unknown register, a missing comparison or
    a side that is not a side.
    """

    if register not in REGISTER_IDS:
        raise _refuse(
            PACK_INPUT_INVALID,
            f"register {register!r} is not one of {REGISTER_IDS}",
        )
    if order not in ORDERS:
        raise _refuse(PACK_INPUT_INVALID, f"order {order!r} is not one of {ORDERS}")
    cell_id = _cell_id(cell)
    try:
        sealed = _sha256_hex(baseline_sha, "baseline_sha")
    except PackError as exc:
        raise BaselineNotFirst(
            f"no cross-case pack renders for cell {cell_id!r} register "
            f"{register!r} until its within-ORIGINAL baseline is sealed: {exc.detail}"
        ) from exc

    comparison_id = _string(comparison, "comparison")
    first, second = _sides_of(cell, sides)
    parsed, digest = _standard(standard)
    rubric_id = RUBRIC_FOR_ROLE[ROLE_MARKER]

    shown = (first, second) if order == ORDER_AS_DECLARED else (second, first)
    side_blocks = tuple(
        Block(
            kind=SIDE_KIND,
            name=f"side {alias}",
            body=side.text,
            slot=side.arm,
            anonymous=True,
        )
        for alias, side in zip(ALIASES, shown)
    )
    blocks = (
        _instruction_block(MARKER_INSTRUCTION),
        _rubric_block(parsed, rubric_id),
        _register_block(parsed, register),
        *side_blocks,
        _contract_block(ROLE_MARKER, register=register),
    )
    parts = {
        "standard": _standard_parts(parsed, digest, rubric_id),
        "subject": {
            "cell": cell_id,
            "register": register,
            "comparison": comparison_id,
            "difference_kinds": list(difference_kinds_for(register)),
        },
        "baseline": {
            "sha256": sealed,
            "reads": (
                "the sealed within-ORIGINAL baseline grid for this cell and register. "
                "Its kind set is deliberately not in this pack: the downgrade of a "
                "differs whose kind the baseline already shows is the program's."
            ),
        },
        "presentation": {
            "order": order,
            "swap_recorded": order == ORDER_SWAPPED,
            "side_aliases": {alias: side.arm for alias, side in zip(ALIASES, shown)},
        },
        "word_limits": {
            field: limit
            for (owner, field), limit in sorted(WORD_LIMITS.items())
            if owner == ROLE_MARKER
        },
    }
    pack = Pack(
        role=ROLE_MARKER,
        title=f"marker pack — cell {cell_id}, register {register}, "
        f"comparison {comparison_id}",
        blocks=blocks,
        parts=parts,
        standard=parsed,
    )
    assert_pack_clean(pack)
    return pack


# --------------------------------------------------------------------------
# render_paraphrase_request — the variator pack
# --------------------------------------------------------------------------


def render_paraphrase_request(
    exchange: Any,
    *,
    held_spans: Sequence[str] | None = None,
    n: int | None = None,
) -> Pack:
    """The variator's pack: restate the exchange, hold the quoted spans (§2.3, G7).

    ``exchange`` is an :class:`Exchange`, or the judge :class:`Pack` the
    exchange belongs to — in which case the exchange and the held spans are read
    off that pack, so a spot-check cannot be run against a text the judge was
    not shown.

    The pack carries the exchange text and the **span-survival check input**: the
    spans that must come back byte-identically.  Whether they did is W3-TRIAL's
    check, and the input to it is pinned here, inside the pack digest, so the
    check cannot be run against a different list than the one the seat was given.

    ``n`` defaults to ``standard.GUARD_PARAMETERS["paraphrase_n"]`` — the pinned
    ``TRIAL_PARAPHRASE_N = 2``.  *The material is never paraphrased and is not in
    this pack.*
    """

    spans: tuple[str, ...]
    if isinstance(exchange, Pack):
        if exchange.exchange is None:
            raise _refuse(PACK_INPUT_INVALID, f"a {exchange.role} pack carries no exchange")
        recorded = exchange.parts.get("held_spans")
        spans = tuple(str(span) for span in recorded) if isinstance(recorded, (list, tuple)) else ()
        source = exchange.exchange
        title_of = exchange.title.split(" — ", 1)[-1]
    elif isinstance(exchange, Exchange):
        source = exchange
        spans = ()
        title_of = source.digest
    else:
        raise _refuse(PACK_INPUT_INVALID, "render_paraphrase_request takes an Exchange or a judge Pack")

    if held_spans is not None:
        if isinstance(held_spans, (str, bytes)):
            raise _refuse(PACK_INPUT_INVALID, "held_spans is a sequence of spans, not one string")
        spans = tuple(_string(span, "held_spans[]") for span in held_spans)

    count = GUARD_PARAMETERS["paraphrase_n"] if n is None else n
    if not isinstance(count, int) or isinstance(count, bool) or count < 1:
        raise _refuse(PACK_INPUT_INVALID, "n is a positive count of restatements")

    missing = [span for span in spans if span not in source.text]
    blocks = (
        _instruction_block(VARIATOR_INSTRUCTION.format(n=count)),
        Block(kind="exchange", name="the exchange to restate", body=source.text),
        Block(
            kind="held-spans",
            name="the spans that must survive byte for byte",
            body=_bullets(spans) if spans else "- (none: nothing was quoted in this exchange)",
        ),
        _contract_block(ROLE_VARIATOR),
    )
    parts = {
        "subject": {
            "exchange": source.as_dict(),
            "paraphrase_n": count,
        },
        "held_spans": list(spans),
        "held_spans_reads": (
            "the span-survival check input. Every span here must appear byte-identically "
            "in every restatement; a restatement that alters one is discarded and the "
            "spot-check is recorded as not performed, never as passed."
        ),
        "held_spans_absent_from_exchange": missing,
        "word_limits": {
            field: limit
            for (owner, field), limit in sorted(WORD_LIMITS.items())
            if owner == ROLE_VARIATOR
        },
    }
    pack = Pack(
        role=ROLE_VARIATOR,
        title=f"variator pack — {title_of}",
        blocks=blocks,
        parts=parts,
        exchange=source,
    )
    assert_pack_clean(pack)
    return pack


# --------------------------------------------------------------------------
# The precedent slice
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Precedent:
    """One selected precedent, and its rank in the slice.

    ``position`` is a place in a deterministic selection order — appellate
    rulings, then registration order — and is never a merit ordering: no two
    precedents are compared and nothing here is a quantity.  The field is
    ``position`` and not *rank* because *rank* is a member of
    ``standard.FORBIDDEN_KEYS``: G12 refuses the word as a key, and a slice that
    called its own ordering by that name would be asserting the very thing the
    design says precedent ordering is not.  A precedent also carries no
    adjudication status token: acceptance is the program's selection criterion
    and is not a thing a seat is shown.
    """

    position: int
    artifact_id: str
    kind: str
    cell: str = ""
    relation: str = ""
    ground: str = ""
    standard: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "position": self.position,
            "artifact_id": self.artifact_id,
            "kind": self.kind,
            "cell": self.cell,
            "relation": self.relation,
            "ground": self.ground,
            "standard": self.standard,
        }


class PrecedentSlice(list):
    """The selected precedents, in selection order, carrying the query that chose them.

    A ``list``, exactly as the wave plan's ``precedent_slice(...) -> list`` says,
    with the deterministic query text riding on it (deviation 3) so that a judge
    pack can record *how* its precedents were selected and not merely *which*.
    """

    def __init__(
        self,
        entries: Iterable[Precedent] = (),
        *,
        query: str,
        standard_id: str = "",
        k: int = PRECEDENT_K,
        excluded: Sequence[str] = (),
    ) -> None:
        super().__init__(entries)
        self.query = query
        self.standard_id = standard_id
        self.k = k
        self.excluded = tuple(excluded)

    @property
    def appellate_first(self) -> bool:
        """True where no reading precedes an appellate ruling in this slice."""

        seen_reading = False
        for entry in self:
            if entry.kind != RECORD_APPELLATE_RULING:
                seen_reading = True
            elif seen_reading:
                return False
        return True

    def as_dict(self) -> dict[str, Any]:
        record = {
            "query": self.query,
            "standard": self.standard_id,
            "k": self.k,
            "excluded": list(self.excluded),
            "appellate_rulings_first": True,
            "selection_order": list(PRECEDENT_KINDS),
            "entries": [entry.as_dict() for entry in self],
        }
        assert_no_scoring_keys(record)
        return record


def _artifact_bodies(harness: Any) -> list[tuple[str, dict[str, Any], str]]:
    """``(artifact_id, body, status)`` for every JSON artifact, in registration order.

    Read through the same duck-typed path
    :meth:`obligations.Situation.from_harness` uses, so that this module keeps
    the three dependencies the wave plan declares and still reads the graph
    W1-GRAPH wrote.  Nothing is written and no exception escapes: an artifact
    whose bytes are not a JSON object is simply not a precedent.
    """

    state = getattr(harness, "state", None)
    artifacts = getattr(state, "artifacts", None)
    if artifacts is None:
        raise _refuse(
            PRECEDENT_QUERY_INVALID,
            "precedent_slice reads a deepreason_core harness (state.artifacts)",
        )
    status_map = getattr(state, "status", {}) or {}
    blobs = getattr(harness, "blobs", None)
    found: list[tuple[str, dict[str, Any], str]] = []
    for artifact_id, artifact in artifacts.items():
        ref = str(getattr(artifact, "content_ref", ""))
        if ref.startswith(_INLINE_PREFIX):
            raw: Any = ref[len(_INLINE_PREFIX):].encode("utf-8")
        elif blobs is None:
            continue
        else:
            try:
                raw = blobs.get(ref)
            except (KeyError, OSError, ValueError):
                continue
        if isinstance(raw, (bytes, bytearray)):
            try:
                raw = raw.decode("utf-8")
            except UnicodeDecodeError:
                continue
        if not isinstance(raw, str):
            continue
        try:
            body = json.loads(raw)
        except ValueError:
            continue
        if not isinstance(body, dict):
            continue
        label = status_map.get(artifact_id)
        found.append((artifact_id, body, str(getattr(label, "value", label or ""))))
    return found


#: Where the vendored trial transcript keeps the decisive point, and the
#: top-level fallback.  ``deepreason_core.harness.transcript_blob`` nests it
#: under ``ruling``; only the **string** is ever lifted out of that blob,
#: because the blob also carries the vendored warrant's own ``verdict`` field,
#: which is a member of ``standard.FORBIDDEN_KEYS`` (wave-0 open question O2)
#: and may not be copied into a loop-authored record.
_GROUND_PATHS: tuple[tuple[str, ...], ...] = (
    ("ruling", "decisive_point"),
    ("decisive_point",),
)


def _ground_of(harness: Any, body: Mapping[str, Any]) -> str:
    """A reading precedent's stated ground: its decisive point, where readable.

    A precedent without its ground is an authority claim rather than a reason,
    which is not what a rubric-governed trial is shown precedent for.  The
    transcript blob is read defensively — a ref that does not decode leaves the
    ground empty rather than inventing one — and **only the decisive point
    string** is taken out of it; see :data:`_GROUND_PATHS`.
    """

    ref = body.get("transcript_ref")
    blobs = getattr(harness, "blobs", None)
    if not isinstance(ref, str) or blobs is None:
        return ""
    try:
        raw = blobs.get(ref)
    except (KeyError, OSError, ValueError):
        return ""
    if isinstance(raw, (bytes, bytearray)):
        try:
            raw = raw.decode("utf-8")
        except UnicodeDecodeError:
            return ""
    try:
        transcript = json.loads(raw)
    except (TypeError, ValueError):
        return ""
    for path in _GROUND_PATHS:
        found: Any = transcript
        for segment in path:
            found = found.get(segment) if isinstance(found, dict) else None
        if isinstance(found, str) and found:
            return found
    return ""


def precedent_slice(
    harness: Any,
    standard_id: Any,
    k: int = PRECEDENT_K,
    *,
    exclude: Sequence[str] = (),
) -> PrecedentSlice:
    """The judge pack's precedent slice, selected by a deterministic logged query.

    §2.3: *the top-K accepted precedent readings citing this standard, appellate
    rulings ranked first, selected by a deterministic query whose text is
    logged.*  The query is :data:`PRECEDENT_QUERY`, rendered with its own
    arguments and carried on the returned slice, and the ordering is:

    1. every registered appellate ruling, in **registration order**;
    2. then every accepted reading or mark whose ``standard`` is ``standard_id``
       and whose cell is not in ``exclude``, in **registration order**;

    truncated to ``k``.  *The ordering is not a ranking by merit.*  Appellate
    rulings come first because they are precedent — "authority is pack ordering,
    never status privilege", as W1-GRAPH's ``apply_appeal`` puts it — and within
    each group the order is the order the graph was written in.  No two
    precedents are compared, nothing is scored, and the slice carries no
    adjudication status token for any entry.

    ``exclude`` is the cell under judgement and any cell of its own comparison:
    a pack never shows a seat the outcome of the cell it is being asked about.
    Case law from *other* cells is what §2.3 asks for and is not that.

    Pure and read-only: it writes nothing and registers nothing.  Raises
    :class:`PackError` with :data:`PRECEDENT_QUERY_INVALID` for a non-positive
    ``k`` or a source that is not a readable harness.
    """

    if not isinstance(k, int) or isinstance(k, bool) or k < 1:
        raise _refuse(PRECEDENT_QUERY_INVALID, "k is a positive resource bound")
    wanted = _string(standard_id, "standard_id")
    excluded = tuple(str(value) for value in exclude)
    query = PRECEDENT_QUERY.format(
        field=RECORD_FIELD,
        appellate=RECORD_APPELLATE_RULING,
        reading=RECORD_READING_ROW,
        mark=RECORD_CELL_MARK,
        standard_id=wanted,
        standing=STANDING,
        excluded=list(excluded),
        k=k,
    )

    rulings: list[tuple[str, dict[str, Any]]] = []
    readings: list[tuple[str, dict[str, Any]]] = []
    for artifact_id, body, status in _artifact_bodies(harness):
        kind = body.get(RECORD_FIELD)
        if kind == RECORD_APPELLATE_RULING:
            rulings.append((artifact_id, body))
        elif kind in (RECORD_READING_ROW, RECORD_CELL_MARK):
            if status != STANDING:
                continue
            if body.get("standard") != wanted:
                continue
            if str(body.get("key", "")) in excluded:
                continue
            readings.append((artifact_id, body))

    entries: list[Precedent] = []
    for artifact_id, body in rulings:
        entries.append(
            Precedent(
                position=len(entries) + 1,
                artifact_id=artifact_id,
                kind=RECORD_APPELLATE_RULING,
                ground=str(body.get("ground", "")),
                standard=str(body.get("standard", "")),
            )
        )
        if len(entries) == k:
            break
    for artifact_id, body in readings:
        if len(entries) >= k:
            break
        entries.append(
            Precedent(
                position=len(entries) + 1,
                artifact_id=artifact_id,
                kind=str(body.get(RECORD_FIELD, "")),
                cell=str(body.get("key", "")),
                relation=str(body.get("relation", "")),
                ground=_ground_of(harness, body),
                standard=str(body.get("standard", "")),
            )
        )
    return PrecedentSlice(entries, query=query, standard_id=wanted, k=k, excluded=excluded)
