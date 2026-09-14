"""The resolvable material surface ``M``, and the unique-substring resolver.

What this is
------------
One juxtaposition row of the ``use_relation_h005`` table becomes one **frozen
byte string** — the referring record verbatim, the resolved target record
verbatim, and the listed ``referring_body_passages``, each under a label line —
together with an **offset table** that maps every byte of the declared regions
back to the occurrence file it came from.  A quote is then resolved against
those bytes by exact search, and the resolved span is reported with the
occurrence-file span beside it, so a reading can be checked against the material
long after the call that produced it.

This is G2(a) and G3 of the design, and nothing else:

* **G2(a) — referential integrity by uniqueness.**  A quote must occur exactly
  once in ``M``.  Zero occurrences or more than one is
  :data:`REFERENTIAL_INTEGRITY_BLOCK`; :func:`resolve_unique` returns ``None``
  and :meth:`Surface.count` says which of the two it was.
* **G3 — operative target (R10).**  The resolved span must lie wholly inside one
  declared region: the referring record, the target record, or one listed body
  passage.  A span that lies in, or crosses, the surface's own label framing
  resolves uniquely but is not a reading of the material, and
  :func:`within_declared_span` returns ``False`` ⇒
  :data:`OPERATIVE_TARGET_BLOCK`.  *A reading grounded in the prompt's own
  scaffolding is not a reading of the material.*

Design section implemented
--------------------------
W1-SURFACE of *The automated end-to-end harness loop — FINAL design of record*:
§2.4 G2(a) and G3, and the ``E_row`` half of §3(b) — "the ``UseRow`` bytes
exactly as the instrument emitted them".  §2.3's rule for the variator is the
reason the surface is frozen and content-addressed: **the material is never
paraphrased; its bytes are what the offsets resolve against.**

What this is NOT
----------------
It opens no file, reads nothing under any occurrence and writes nothing
anywhere.  Every byte it emits came out of the use-relation row it was handed.
It calls no provider, mints no edge, scores nothing and reads nothing: it says
where a quote *is*, never whether the quote is apt.  It does not normalise,
trim, case-fold, unify whitespace or repair a quote in any way — a quote that
does not match the material byte for byte does not match, and that is a block,
not a near miss.  It does not mint a cell key: which coordinate a row becomes is
W4-READER's and W1-GRAPH's, not this module's.

Coordinate systems, stated once
-------------------------------
Two, and they are different on purpose.

* ``Surface.text`` is **bytes**, and ``Offset.start`` / ``Offset.end`` are
  **utf-8 byte offsets** into it.  On a row carrying an em dash, a byte offset
  and a character offset differ, and every published F001 table has such rows.
* ``Offset.file_start`` / ``Offset.file_end`` are **code-point offsets into one
  named string field of one occurrence artifact** — ``commitments`` for a
  record, ``body`` for a body passage — which is the coordinate system the
  instrument itself publishes in ``use_relation_h005.record_source_spans`` and
  ``use_relation_h005.split_sentences``.  That docstring is emphatic and this
  module does not contradict it: they are *not* utf-8 byte offsets and *not*
  offsets into the artifact JSON file, whose string values are escaped.  The
  check they satisfy is
  ``json.load(occurrence / offset.occurrence_path)[offset.source_field][file_start:file_end]``
  ``== quote``, and a test asserts exactly that against published bytes.

Deviations from the wave-plan interface, and why
------------------------------------------------
* **``Surface.text`` is ``bytes``, not ``str``.**  The wave plan names the
  attribute ``text``; the acceptance clause requires byte offsets, and the
  design calls the material "a frozen byte string".  Holding ``str`` and
  reporting byte offsets would be two representations of one thing with a
  silent conversion between them.  :attr:`Surface.decoded` is the utf-8 string
  for W2-PACKS to render.
* **Occurrences are counted overlapping.**  The design writes ``M.count(q) ==
  1``.  ``bytes.count`` counts *non-overlapping* occurrences, so it calls
  ``aa`` unique in ``aaa`` — and then ``M.index(q)`` picks the first of two
  equally good spans and the transcript records an arbitrary one.  This module
  counts every start position, which is strictly stronger and never weaker;
  where ``bytes.count`` returns 1 the two agree, and a test pins that.
* **A fourth side, ``framing``.**  :data:`SIDE_FRAMING` is the side
  :func:`resolve_unique` reports for a unique match that no declared region
  contains.  It is what makes the G2/G3 split decidable by the caller: ``None``
  is G2, ``framing`` is G3.  Its ``occurrence_path`` and file offsets are
  ``None``, because no occurrence file carries the surface's own label bytes.
* **``build_surface`` accepts a mapping as well as a ``UseRow``.**  The loop
  reads a published ``use_table.json``, whose rows are dicts; the instrument's
  own ``UseRow`` is accepted through its ``as_dict()``.  Nothing else is.
* **``Span`` is named here.**  The wave plan names ``Surface.spans`` without
  naming the entry type.
* **The label vocabulary is this module's choice.**  The design fixes what is
  *in* the surface, not how the three regions are announced inside it.  The
  labels are framing by construction (they are outside every declared span), so
  a quote into one is G3 rather than a false reading.

Reuse
-----
The occurrence path convention is :func:`graph_import_h005.occurrence_path` and
the coordinate is :class:`graph_import_h005.Coordinate`, imported rather than
retyped: ``Coordinate.from_dict`` validates all four components against the
importer's own ``safe_component`` before they are turned into a path, so a
malformed coordinate cannot become a traversal.  The block codes are
:func:`minireason.loop.types.block_code`.  G12 is
:func:`minireason.loop.contracts.assert_no_scoring_keys`, run over the emitted
surface record — over its *keys*, which are this module's, never over the
material in its values.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Mapping

from minireason.graph_import_h005 import (
    Coordinate,
    CustodyError,
    occurrence_path as _occurrence_path,
)
from minireason.loop.contracts import assert_no_scoring_keys
from minireason.loop.types import LoopError, block_code

__all__ = [
    "SURFACE_SCHEMA",
    "ARTIFACT_CATEGORY",
    "SIDE_REFERRING_RECORD",
    "SIDE_TARGET_RECORD",
    "SIDE_REFERRING_BODY_PASSAGE",
    "SIDE_FRAMING",
    "DECLARED_SIDES",
    "SIDES",
    "SOURCE_FIELDS",
    "FIELD_COMMITMENTS",
    "FIELD_BODY",
    "LABEL_OPEN",
    "LABEL_CLOSE",
    "LABEL_TERMINATOR",
    "BLOCK_SEPARATOR",
    "REFERENTIAL_INTEGRITY_BLOCK",
    "OPERATIVE_TARGET_BLOCK",
    "NEW_CODES",
    "SurfaceInvalid",
    "Span",
    "Offset",
    "Surface",
    "build_surface",
    "resolve_unique",
    "within_declared_span",
]


# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

#: The emitted surface record's schema name.
SURFACE_SCHEMA = "minireason.loop.surface.v1"

#: The occurrence category every record and body string is read out of by the
#: importer.  ``artifacts/<problem>/<arm>/cycle<NN>/<node>.json``.
ARTIFACT_CATEGORY = "artifacts"

#: The three declared regions G3 names, in the order the surface lays them out.
SIDE_REFERRING_RECORD = "referring_record"
SIDE_TARGET_RECORD = "target_record"
SIDE_REFERRING_BODY_PASSAGE = "referring_body_passage"

#: The side a unique match gets when no declared region contains it: the
#: surface's own label bytes, and any span crossing a region boundary.  It is
#: never a member of :data:`DECLARED_SIDES` and never carries a file span.
SIDE_FRAMING = "framing"

#: The operative sides — the ones G3 admits.
DECLARED_SIDES: tuple[str, ...] = (
    SIDE_REFERRING_RECORD,
    SIDE_TARGET_RECORD,
    SIDE_REFERRING_BODY_PASSAGE,
)

#: Every value ``Offset.side`` can take.
SIDES: tuple[str, ...] = (*DECLARED_SIDES, SIDE_FRAMING)

#: The artifact string field each declared side's offsets index into.
FIELD_COMMITMENTS = "commitments"
FIELD_BODY = "body"
SOURCE_FIELDS: Mapping[str, str] = {
    SIDE_REFERRING_RECORD: FIELD_COMMITMENTS,
    SIDE_TARGET_RECORD: FIELD_COMMITMENTS,
    SIDE_REFERRING_BODY_PASSAGE: FIELD_BODY,
}

#: A region is announced by ``LABEL_OPEN + what + LABEL_CLOSE`` on its own line,
#: then :data:`LABEL_TERMINATOR`, then the region's bytes.  Regions are joined
#: by :data:`BLOCK_SEPARATOR`.  All of it is framing: no label byte lies inside
#: any declared span.
LABEL_OPEN = "--- "
LABEL_CLOSE = " ---"
LABEL_TERMINATOR = b"\n"
BLOCK_SEPARATOR = b"\n\n"

#: The two block codes this module's two refusals map to.  Built through
#: :func:`types.block_code` so the spelling cannot drift from the ceiling's.
REFERENTIAL_INTEGRITY_BLOCK = block_code("referential-integrity")
OPERATIVE_TARGET_BLOCK = block_code("operative-target")

#: Codes this module raises that ``types.FAILURE_CODES`` does not yet carry.
#: The wave integrator adds them to the table; nothing here narrows or edits it.
NEW_CODES: Mapping[str, str] = {
    "SURFACE_ROW_MALFORMED": (
        "the use-relation row is missing a field the surface is built from, or "
        "one has the wrong type or a coordinate that is not its own key"
    ),
    "SURFACE_SPAN_DISAGREES": (
        "a published source span's length does not match its verbatim text, so "
        "the map back to the occurrence file would be a guess"
    ),
    "SURFACE_NO_MATERIAL": (
        "the row declares no quotable region at all - no record verbatim on "
        "either side and no body passage - so no quote could resolve against it"
    ),
}


class SurfaceInvalid(LoopError, ValueError):
    """A use-relation row the surface cannot be built from.

    ``(code, detail="")``, the argument order every wave-0 exception takes.  It
    is a :class:`~minireason.loop.types.LoopError`, so ``except LoopError``
    catches it, and it keeps ``ValueError`` so an existing caller's ``except
    ValueError`` keeps working.  Every code it carries is a key of
    :data:`NEW_CODES`.
    """


# --------------------------------------------------------------------------
# Byte helpers
# --------------------------------------------------------------------------


def _is_char_boundary(buf: bytes, index: int) -> bool:
    """True where ``index`` falls between two utf-8 characters of ``buf``."""

    if index <= 0 or index >= len(buf):
        return True
    return not 0x80 <= buf[index] < 0xC0


def _code_points(buf: bytes, start: int, end: int) -> int:
    """The number of characters in ``buf[start:end]``, which must be utf-8."""

    return len(buf[start:end].decode("utf-8"))


def _as_bytes(quote: Any) -> bytes:
    """A quote as utf-8 bytes.  ``str`` is encoded; ``bytes`` is taken as-is."""

    if isinstance(quote, bytes):
        return quote
    if isinstance(quote, bytearray):
        return bytes(quote)
    if isinstance(quote, str):
        return quote.encode("utf-8")
    raise SurfaceInvalid("SURFACE_ROW_MALFORMED", "a quote is str or bytes")


def _starts(hay: bytes, needle: bytes) -> tuple[int, ...]:
    """Every character-aligned start offset of ``needle`` in ``hay``.

    Overlapping occurrences are all reported: ``bytes.count`` would call ``aa``
    unique in ``aaa`` and the resolved span would then be arbitrary.  A match
    landing inside a utf-8 character is not a match of any characters and is
    dropped; on valid utf-8 input that case cannot arise, and it is here so that
    a caller handing over raw bytes cannot manufacture one.
    """

    found: list[int] = []
    width = len(needle)
    index = hay.find(needle)
    while index != -1:
        if _is_char_boundary(hay, index) and _is_char_boundary(hay, index + width):
            found.append(index)
        index = hay.find(needle, index + 1)
    return tuple(found)


# --------------------------------------------------------------------------
# The offset table and the resolved offset
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Span:
    """One declared region of the surface, and where its bytes came from.

    ``start``/``end`` are utf-8 byte offsets into :attr:`Surface.text`;
    ``file_start``/``file_end`` are code-point offsets into
    :attr:`source_field` of the artifact at :attr:`occurrence_path`.  Spans are
    disjoint, in surface order, and cover exactly the operative bytes: every
    byte of the surface outside every span is framing.
    """

    side: str
    start: int
    end: int
    occurrence_path: str
    source_field: str
    file_start: int
    file_end: int
    coordinate_key: str
    record_id: str | None = None
    ordinal: int | None = None

    @property
    def length(self) -> int:
        return self.end - self.start

    def contains(self, start: int, end: int) -> bool:
        """True where ``[start, end)`` is a non-empty sub-range of this span."""

        return self.start <= start and end <= self.end and end > start

    def as_dict(self) -> dict[str, Any]:
        return {
            "side": self.side,
            "start": self.start,
            "end": self.end,
            "occurrence_path": self.occurrence_path,
            "source_field": self.source_field,
            "file_start": self.file_start,
            "file_end": self.file_end,
            "coordinate_key": self.coordinate_key,
            "record_id": self.record_id,
            "ordinal": self.ordinal,
        }


@dataclass(frozen=True)
class Offset:
    """Where one quote resolved: in the surface, and in the occurrence file.

    The field order is the wave plan's:
    ``Offset(start, end, side, occurrence_path, file_start, file_end)``.
    ``start``/``end`` are utf-8 byte offsets into :attr:`Surface.text`;
    ``file_start``/``file_end`` are code-point offsets into
    :attr:`source_field` of the named artifact.  For :data:`SIDE_FRAMING` the
    last three are ``None``: the surface's own label bytes are in no occurrence
    file, and saying ``0`` there would be a fabricated citation.

    The transcript entry the design asks for — ``(surface, start, end,
    occurrence_path, file_start, file_end)`` — is :attr:`Surface.digest` beside
    :meth:`as_dict`.
    """

    start: int
    end: int
    side: str
    occurrence_path: str | None
    file_start: int | None
    file_end: int | None

    @property
    def length(self) -> int:
        return self.end - self.start

    @property
    def is_framing(self) -> bool:
        return self.side == SIDE_FRAMING

    @property
    def source_field(self) -> str | None:
        """``commitments``, ``body``, or ``None`` for framing."""

        return SOURCE_FIELDS.get(self.side)

    def as_dict(self) -> dict[str, Any]:
        return {
            "start": self.start,
            "end": self.end,
            "side": self.side,
            "occurrence_path": self.occurrence_path,
            "source_field": self.source_field,
            "file_start": self.file_start,
            "file_end": self.file_end,
        }


# --------------------------------------------------------------------------
# The surface
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Surface:
    """The frozen, content-addressed material surface ``M`` of one row.

    :attr:`text` is the material and nothing else is: two builds from the same
    row are byte-identical, and :attr:`digest` addresses those bytes.  Nothing
    about the row's *reading* is here — no relation, no mark, no label, no
    status, no count of anything under study.
    """

    text: bytes
    spans: tuple[Span, ...]
    referring_coordinate_key: str
    target_coordinate_key: str
    referring_record_id: str | None
    target_record_id: str | None
    ref_field: str
    ref_verbatim: str
    ref_grain: str
    schema: str = SURFACE_SCHEMA

    # -- identity ---------------------------------------------------------

    @property
    def digest(self) -> str:
        """``sha256`` of :attr:`text`, hex.  A pure function of the bytes."""

        return hashlib.sha256(self.text).hexdigest()

    @property
    def decoded(self) -> str:
        """:attr:`text` as utf-8, for a renderer.  Offsets do not apply to it."""

        return self.text.decode("utf-8")

    def __len__(self) -> int:
        return len(self.text)

    # -- search -----------------------------------------------------------

    def occurrences(self, quote: Any) -> tuple[int, ...]:
        """Every character-aligned start byte offset of ``quote``, overlapping.

        An empty quote designates no passage and has no occurrences.
        """

        needle = _as_bytes(quote)
        if not needle:
            return ()
        return _starts(self.text, needle)

    def count(self, quote: Any) -> int:
        """``M.count(q)`` of G2(a), counted overlapping.  See the module note."""

        return len(self.occurrences(quote))

    def span_at(self, start: int, end: int) -> Span | None:
        """The declared span wholly containing ``[start, end)``, or ``None``."""

        for span in self.spans:
            if span.contains(start, end):
                return span
        return None

    # -- record -----------------------------------------------------------

    def as_dict(self) -> dict[str, Any]:
        """The surface's identity and its offset table — not a second copy.

        The bytes are the material; a record of them is their digest and their
        map.  G12 is run over this record's keys before it is returned.
        """

        record = {
            "schema": self.schema,
            "digest": self.digest,
            "bytes": len(self.text),
            "referring_coordinate_key": self.referring_coordinate_key,
            "target_coordinate_key": self.target_coordinate_key,
            "referring_record_id": self.referring_record_id,
            "target_record_id": self.target_record_id,
            "ref_field": self.ref_field,
            "ref_verbatim": self.ref_verbatim,
            "ref_grain": self.ref_grain,
            "spans": [span.as_dict() for span in self.spans],
        }
        assert_no_scoring_keys(record)
        return record


# --------------------------------------------------------------------------
# Building
# --------------------------------------------------------------------------


def _row_mapping(use_row: Any) -> Mapping[str, Any]:
    if isinstance(use_row, Mapping):
        return use_row
    as_dict = getattr(use_row, "as_dict", None)
    if callable(as_dict):
        candidate = as_dict()
        if isinstance(candidate, Mapping):
            return candidate
    raise SurfaceInvalid(
        "SURFACE_ROW_MALFORMED",
        "a use row is a mapping or an object with as_dict()",
    )


def _required(row: Mapping[str, Any], key: str) -> Any:
    if key not in row:
        raise SurfaceInvalid("SURFACE_ROW_MALFORMED", f"{key} is missing")
    return row[key]


def _text_or_none(value: Any, where: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise SurfaceInvalid("SURFACE_ROW_MALFORMED", f"{where} must be a string")
    if not value:
        raise SurfaceInvalid("SURFACE_ROW_MALFORMED", f"{where} is empty, not absent")
    return value


def _string(value: Any, where: str) -> str:
    if not isinstance(value, str):
        raise SurfaceInvalid("SURFACE_ROW_MALFORMED", f"{where} must be a string")
    return value


def _optional_id(value: Any, where: str) -> str | None:
    if value is None:
        return None
    return _string(value, where)


def _source_span(value: Any, text: str, where: str) -> tuple[int, int]:
    """A published ``[start, end]`` checked against the length of its text."""

    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise SurfaceInvalid("SURFACE_ROW_MALFORMED", f"{where} must be [start, end]")
    start, end = value
    if not isinstance(start, int) or not isinstance(end, int):
        raise SurfaceInvalid("SURFACE_ROW_MALFORMED", f"{where} must be two integers")
    if isinstance(start, bool) or isinstance(end, bool):
        raise SurfaceInvalid("SURFACE_ROW_MALFORMED", f"{where} must be two integers")
    if start < 0 or end < start:
        raise SurfaceInvalid("SURFACE_ROW_MALFORMED", f"{where} is not a forward span")
    if end - start != len(text):
        raise SurfaceInvalid(
            "SURFACE_SPAN_DISAGREES",
            f"{where} spans {end - start} code points, its text is {len(text)}",
        )
    return start, end


def _coordinate(row: Mapping[str, Any], prefix: str) -> tuple[Coordinate, str]:
    """The coordinate and its key, each checked against the other."""

    key = _string(_required(row, f"{prefix}_coordinate_key"), f"{prefix}_coordinate_key")
    try:
        coord = Coordinate.from_dict(_required(row, f"{prefix}_coordinate"))
    except CustodyError as exc:
        raise SurfaceInvalid(
            "SURFACE_ROW_MALFORMED", f"{prefix}_coordinate: {exc}"
        ) from exc
    if coord.key != key:
        raise SurfaceInvalid(
            "SURFACE_ROW_MALFORMED",
            f"{prefix}_coordinate_key {key!r} is not {coord.key!r}",
        )
    return coord, key


def _label(side: str, coordinate_key: str, record_id: str | None, ordinal: int | None) -> str:
    if side == SIDE_REFERRING_BODY_PASSAGE:
        what = f"referring body passage {ordinal}"
        where = coordinate_key
    else:
        what = "referring record" if side == SIDE_REFERRING_RECORD else "target record"
        where = coordinate_key if record_id is None else f"{coordinate_key}#{record_id}"
    return f"{LABEL_OPEN}{what}: {where}{LABEL_CLOSE}"


def build_surface(use_row: Any) -> Surface:
    """The resolvable surface ``M`` of one juxtaposition row.

    ``use_row`` is a ``use_relation_h005.UseRow`` or one row of a published
    ``use_table.json``.  Its bytes are laid out in one fixed order — referring
    record, target record, then each listed ``referring_body_passages`` entry in
    the instrument's own order — each announced by a label line and separated by
    a blank line.  A region the row does not carry is absent, not empty: an
    ``artifact``-grain ref resolves to no target record and the surface simply
    has no target region.

    Nothing is read from disk and nothing is written anywhere: every byte comes
    out of the row.  Two calls on one row return byte-identical surfaces.

    Raises :class:`SurfaceInvalid` with ``SURFACE_ROW_MALFORMED`` for a row that
    is not shaped like one, ``SURFACE_SPAN_DISAGREES`` where a published span's
    length contradicts its own verbatim text, and ``SURFACE_NO_MATERIAL`` where
    a row declares nothing quotable at all.
    """

    row = _row_mapping(use_row)
    referring_coord, referring_key = _coordinate(row, "referring")
    target_coord, target_key = _coordinate(row, "target")
    referring_path = _occurrence_path(referring_coord, ARTIFACT_CATEGORY)
    target_path = _occurrence_path(target_coord, ARTIFACT_CATEGORY)

    referring_id = _optional_id(row.get("referring_record_id"), "referring_record_id")
    target_id = _optional_id(row.get("target_record_id"), "target_record_id")

    regions: list[tuple[str, str, str, str, str | None, int | None, int, int]] = []

    referring_verbatim = _text_or_none(
        row.get("referring_record_verbatim"), "referring_record_verbatim"
    )
    if referring_verbatim is not None:
        start, end = _source_span(
            _required(row, "referring_record_source_span"),
            referring_verbatim,
            "referring_record_source_span",
        )
        regions.append(
            (
                SIDE_REFERRING_RECORD,
                referring_verbatim,
                referring_path,
                referring_key,
                referring_id,
                None,
                start,
                end,
            )
        )

    target_verbatim = _text_or_none(
        row.get("target_record_verbatim"), "target_record_verbatim"
    )
    if target_verbatim is not None:
        start, end = _source_span(
            _required(row, "target_record_source_span"),
            target_verbatim,
            "target_record_source_span",
        )
        regions.append(
            (
                SIDE_TARGET_RECORD,
                target_verbatim,
                target_path,
                target_key,
                target_id,
                None,
                start,
                end,
            )
        )

    passages = row.get("referring_body_passages") or ()
    if not isinstance(passages, (list, tuple)):
        raise SurfaceInvalid(
            "SURFACE_ROW_MALFORMED", "referring_body_passages must be a sequence"
        )
    for ordinal, passage in enumerate(passages, start=1):
        entry = _row_mapping(passage)
        where = f"referring_body_passages[{ordinal - 1}]"
        text = _text_or_none(_required(entry, "text"), f"{where}.text")
        if text is None:
            raise SurfaceInvalid("SURFACE_ROW_MALFORMED", f"{where}.text is null")
        start, end = _source_span(
            [_required(entry, "start"), _required(entry, "end")], text, where
        )
        regions.append(
            (
                SIDE_REFERRING_BODY_PASSAGE,
                text,
                referring_path,
                referring_key,
                referring_id,
                ordinal,
                start,
                end,
            )
        )

    if not regions:
        raise SurfaceInvalid(
            "SURFACE_NO_MATERIAL",
            f"{referring_key} -> {target_key} declares no quotable region",
        )

    parts: list[bytes] = []
    spans: list[Span] = []
    cursor = 0
    for side, text, path, key, record_id, ordinal, file_start, file_end in regions:
        if parts:
            parts.append(BLOCK_SEPARATOR)
            cursor += len(BLOCK_SEPARATOR)
        label = _label(side, key, record_id, ordinal).encode("utf-8") + LABEL_TERMINATOR
        parts.append(label)
        cursor += len(label)
        content = text.encode("utf-8")
        spans.append(
            Span(
                side=side,
                start=cursor,
                end=cursor + len(content),
                occurrence_path=path,
                source_field=SOURCE_FIELDS[side],
                file_start=file_start,
                file_end=file_end,
                coordinate_key=key,
                record_id=record_id,
                ordinal=ordinal,
            )
        )
        parts.append(content)
        cursor += len(content)

    return Surface(
        text=b"".join(parts),
        spans=tuple(spans),
        referring_coordinate_key=referring_key,
        target_coordinate_key=target_key,
        referring_record_id=referring_id,
        target_record_id=target_id,
        ref_field=_string(_required(row, "ref_field"), "ref_field"),
        ref_verbatim=_string(_required(row, "ref_verbatim"), "ref_verbatim"),
        ref_grain=_string(_required(row, "ref_grain"), "ref_grain"),
    )


# --------------------------------------------------------------------------
# G2(a) and G3
# --------------------------------------------------------------------------


def resolve_unique(surface: Surface, quote: Any) -> Offset | None:
    """G2(a): the one place ``quote`` occurs in ``surface``, or ``None``.

    ``None`` is returned for zero occurrences and for more than one — both are
    :data:`REFERENTIAL_INTEGRITY_BLOCK`, and :meth:`Surface.count` says which,
    for the transcript.  An empty quote is zero occurrences.

    The match is an **exact byte search**.  No whitespace is unified, no case is
    folded, no quotation mark is normalised and nothing is trimmed: the material
    is never paraphrased, and a quote that does not match its bytes is a quote of
    something else.

    A unique match that no declared region wholly contains — a quote of a label
    line, or one running across a region boundary — resolves with
    :data:`SIDE_FRAMING` and no file span.  That is G3's case and
    :func:`within_declared_span` is the predicate for it.
    """

    if not isinstance(surface, Surface):
        raise SurfaceInvalid("SURFACE_ROW_MALFORMED", "resolve_unique takes a Surface")
    needle = _as_bytes(quote)
    starts = surface.occurrences(needle)
    if len(starts) != 1:
        return None
    start = starts[0]
    end = start + len(needle)
    span = surface.span_at(start, end)
    if span is None:
        return Offset(start, end, SIDE_FRAMING, None, None, None)
    file_start = span.file_start + _code_points(surface.text, span.start, start)
    file_end = file_start + _code_points(surface.text, start, end)
    return Offset(start, end, span.side, span.occurrence_path, file_start, file_end)


def within_declared_span(surface: Surface, offset: Offset | None) -> bool:
    """G3: does ``offset`` lie wholly inside one declared region of ``surface``?

    False for ``None``, for a framing offset, for an empty span, and for an
    offset whose ``side`` does not agree with the region its bytes fall in —
    the last so that a hand-built :class:`Offset` cannot claim an operative
    target it does not have.  A span in the surface's labels, or across a region
    boundary, is void: *a reading grounded in the prompt's own scaffolding is
    not a reading of the material.*
    """

    if not isinstance(surface, Surface):
        raise SurfaceInvalid(
            "SURFACE_ROW_MALFORMED", "within_declared_span takes a Surface"
        )
    if offset is None:
        return False
    if not isinstance(offset, Offset):
        raise SurfaceInvalid(
            "SURFACE_ROW_MALFORMED", "within_declared_span takes an Offset"
        )
    if offset.side == SIDE_FRAMING:
        return False
    span = surface.span_at(offset.start, offset.end)
    return span is not None and span.side == offset.side
