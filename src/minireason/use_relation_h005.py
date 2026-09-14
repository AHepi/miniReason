"""Use-relation instrument over one H005 occurrence (FW5 review, proposal P1).

What this is
------------
An offline **juxtaposition table**. For every cross-document reference an
FCL-1 document in scope makes to another document's record, it places side by
side: the referring record verbatim, the resolved target record verbatim, the
sentences of the referring node's BODY that share distinctive vocabulary with
the target record, the two documents' declared ``uptake``, and **four empty
cells reserved for root**.

What this is NOT
----------------
It does not score, rank, classify, label, adjudicate, or decide anything. It
mints no ``att`` and no ``dep`` edge, builds no graph, and calls no provider.
Every interpretive cell it emits is empty, and stays empty until a human
writes in it. A lexical overlap is **not** evidence of use: FCL-1's own rule
is that ``depends``/``mentions`` are "not automatically inferred from citation
or lexical overlap" (``docs/reviews/fcl1-language-proposition-2026-09-14.md``,
"Interpretation"), and the review's R3/R4/R10 say the same from FW5:628,
FW5:640 and FW5:1218/:1222. See :data:`USE_RELATION_BANNER`.

Standing invariants (numbered to match the importer's I1-I7 where they are the
same invariant):

* **U1** offline, provider-free and read-only: only files under the occurrence
  directory are read, through the importer's ``_Reader``, which refuses any
  path that escapes the occurrence and records the sha256 of every byte read.
  Nothing under the occurrence is ever written.
* **U2** no verdict is derived from a transport status. ``delivery_status`` /
  ``envelope_status`` are not read by this instrument at all.
* **U3** nothing is inferred. A relation appears in this table only because an
  author wrote a ref in a ref-valued FCL-1 field. Lexical overlap is reported
  as *lexical overlap*, never as a relation.
* **U4** nothing is repaired. A document the importer could not parse stays
  unparsed and is listed as such; prose is never mined for references.
* **U5** deterministic: no wall clock, no RNG, no dict-iteration order, no
  environment. Two builds over the same occurrence bytes are byte-identical.
* **U6** the tool classifies nothing. There is no score, no rank, no merit, no
  status and no label anywhere in its output, and ``root_reading`` -- the one
  cell that carries a vocabulary -- is emitted empty, with ``unresolved`` a
  legal value of it (FW5:634).
* **U7** the reading is root's. PROTOCOL.md, "Interpretation and possible
  fourth/fifth invocation": "Root alone reviews substantive outputs."

Reuse
-----
Parsing, schema validation, custody verification and reference resolution are
**not reimplemented**; they are imported from
``minireason.graph_import_h005`` and driven up to - and not past - the point
where the importer would begin building a graph. See NOTES.md, "What was
reused from the importer".

Reference resolution in particular is the importer's own **public** walk,
:func:`minireason.graph_import_h005.iter_references`: the same custody, scope
discovery, node loading, parsing, field order, wave-order availability and
``resolve_ref`` the import itself uses, yielding the import's own verdict on
every ref. This instrument no longer reaches into ``_Node.spec_id`` to stand in
for registration, so it cannot resolve a ref differently from the import, and
no sentinel of this module's can reach an importer residue field.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from minireason.graph_import_h005 import (
    EXTENSION_RESIDUE_CODES,
    REF_FIELDS as IMPORTER_REF_FIELDS,
    TASK_RESIDUE_CODE,
    UNRESOLVED_RESIDUE_CODES,
    Coordinate,
    CustodyError,
    MappingError,
    SelectorMatchedNothing,
    _Importer,
    _Node,
    iter_references,
    verify_custody,
)

__all__ = [
    "INSTRUMENT_VERSION",
    "USE_TABLE_SCHEMA",
    "USE_RELATION_BANNER",
    "ROOT_CELLS",
    "ROOT_READING_VOCABULARY",
    "PROSE_SURFACE_NOTE",
    "NO_OVERLAP_NOTE",
    "CustodyError",
    "MappingError",
    "SelectorMatchedNothing",
    "OutDirRefused",
    "Passage",
    "UseRow",
    "DocumentUptake",
    "NodeNotRead",
    "UnresolvedRef",
    "UseTable",
    "build_use_table",
    "uptake_buckets",
    "write_use_table",
]

INSTRUMENT_VERSION = "use_relation_h005/1"
USE_TABLE_SCHEMA = "h005-use-relation.use-table.v1"

#: The banner that heads every USE_TABLE.md and is repeated in the workflow
#: doc. It is this instrument's I7: it says what the output is not.
USE_RELATION_BANNER = (
    "**The tool records juxtapositions; the reading is root's.** This table places "
    "each authored cross-document reference beside passages a root reader may find "
    "worth starting from - a finding aid, never a closed search space - "
    "and stops there. It scores nothing, ranks nothing, classifies nothing and mints "
    "no relation of its own; it has no `att`, no `dep`, no status and no label. "
    "**A lexical overlap is not evidence of use.** FCL-1's own rule is that `depends` "
    "and `mentions` are \"not automatically inferred from citation or lexical "
    "overlap\"; a witness of reason use \"must preserve internal role bindings, not "
    "merely the endpoint string\" (FW5:628); actual use is \"not automatically "
    "machine-maintainable\" while prompt appearance is only a delivery fact "
    "(FW5:640); and no function of an input-output projection agrees with the "
    "accounting predicate across models differing in active route (FW5:1218), "
    "\"semantic use inferred from delivery logs\" included (FW5:1222) - all as "
    "summarised in the FW5-versus-harness-spec review, "
    "`fw5-vs-harness-spec-review.md` \u00a71 R2-R4, \u00a73.1 and \u00a75 P1/P6. Root fills "
    "the four empty cells by reading; `unresolved` is a legal value and stays "
    "unresolved (FW5:634). An empty cell is an **unread row**, not a reading of "
    "`unresolved`."
)

#: The four cells this instrument emits empty and never fills.
ROOT_CELLS = ("root_reading", "root_passage_cited", "root_notes", "root_initials_date")

#: A **suggested** vocabulary for ``root_reading``, published so that the cell
#: has a declared range and so that two readers of two tables mean the same
#: thing by the same word. It is not a closed single-valued enum: review §5 P1
#: names five relations without saying a row carries only one, and `qualifies`,
#: `repairs` and `rejects-with-reason` are not obviously exclusive on a record
#: that concedes one point while repairing another. Root may write more than
#: one, and may write a reading this vocabulary does not cover - and say so.
#: The instrument never selects from it, and nothing here is enforced in code.
ROOT_READING_VOCABULARY = (
    "re-deploys",
    "qualifies",
    "rejects-with-reason",
    "repairs",
    "retains",
    "unresolved",
)

PROSE_SURFACE_NOTE = (
    "commitment surface: prose (not parsed); references not extractable by this instrument"
)

NO_OVERLAP_NOTE = "no lexical overlap found"

#: Ref-valued FCL-1 record fields in the order this table **displays** them.
#: The set is the proposition's own production; ``uptake`` is document-level
#: and sorts after every record of its document. This is a presentation order
#: only: the order refs are *resolved* in is the importer's own published
#: :data:`minireason.graph_import_h005.REF_FIELDS`, which this instrument
#: consumes rather than copies, and both orders are printed in the output.
REF_FIELDS = ("target", "depends", "mentions", "revises", "withdraws")

#: The prose fields of an FCL-1 record, in the order they are concatenated to
#: form "the target record's text". ``id``, ``type`` and every ref array are
#: excluded: they are names and pointers, not content.
RECORD_PROSE_FIELDS = ("text", "scope", "action", "consequence", "grounds", "bearing")

#: A token is a maximal run of ASCII letters/digits in the lowercased string.
TOKEN_RE = re.compile(r"[a-z0-9]+")

#: A sentence boundary is either (a) one or more of ``. ! ?`` **preceded by a
#: lowercase letter or a closing bracket/quote** and followed by whitespace or
#: end-of-string, together with any closing quotes/brackets that follow it, or
#: (b) a run of newlines. The lowercase-letter lookbehind is what keeps a
#: numbered list marker ("1. Separate ...") from becoming its own span; an
#: abbreviation such as "e.g." does split, and the workflow doc says so.
SENTENCE_BOUNDARY_RE = re.compile(
    "(?<=[a-z\\)\\]\u2019'\"])[.!?]+[\"'\\)\\]\u201d]*(?=\\s|$)|\n+"
)

#: Minimum length, in characters of the lowercased token, for a token to be
#: eligible as distinctive.
MIN_TOKEN_LENGTH = 5

#: Closed stopword list. Every entry is >= MIN_TOKEN_LENGTH characters (shorter
#: words are already excluded by the length rule), so this list is exactly the
#: set of long common words the instrument declines to treat as distinctive.
#: It is frozen here, echoed verbatim into every USE_TABLE.md, and is the only
#: piece of English-language knowledge in the instrument.
STOPWORDS = (
    "about", "above", "across", "after", "again", "against", "almost", "alone",
    "along", "already", "also", "although", "always", "among", "another",
    "anyone", "anything", "around", "because", "become", "becomes", "before",
    "begin", "behind", "being", "below", "beside", "better", "between",
    "beyond", "cannot", "could", "does", "doing", "done", "during", "each",
    "either", "enough", "equally", "especially", "even", "every", "everything",
    "except", "exist", "exists", "first", "from", "further", "given", "goes",
    "going", "gone", "hardly", "have", "having", "hence", "here", "however",
    "inside", "instead", "into", "itself", "just", "keep", "kept", "later",
    "least", "less", "like", "likely", "made", "make", "makes", "making",
    "many", "maybe", "might", "more", "most", "much", "must", "near", "need",
    "needs", "neither", "never", "next", "nobody", "none", "nothing", "often",
    "once", "only", "onto", "other", "others", "ought", "over", "perhaps",
    "quite", "rather", "really", "same", "seem", "seems", "seen", "several",
    "shall", "should", "simply", "since", "some", "something", "sometimes",
    "still", "such", "take", "taken", "than", "that", "their", "them",
    "themselves", "then", "there", "therefore", "these", "they", "thing",
    "things", "think", "this", "those", "though", "three", "through", "thus",
    "together", "toward", "under", "unless", "until", "upon", "very", "well",
    "were", "what", "when", "where", "whether", "which", "while", "whole",
    "whom", "whose", "will", "with", "within", "without", "would", "your",
    "yours",
)

_STOPWORDS_SET = frozenset(STOPWORDS)

#: Residue codes for a ref that did NOT resolve to an owning coordinate, and
#: for one admitted by a declared extension. Both are the **importer's own**
#: published classification (``UNRESOLVED_RESIDUE_CODES`` /
#: ``EXTENSION_RESIDUE_CODES``), imported rather than copied: the severity
#: metadata alone cannot make the distinction - ``ref_through_unexposed_view``
#: is severity ``error`` on unit ``ref`` yet attaches to refs that DID resolve
#: - so a local copy would be a semantic judgement kept out of band, and a
#: fourth code added upstream would silently drop a ref out of a section
#: titled "residue, never dropped".
_UNRESOLVED_CODES = UNRESOLVED_RESIDUE_CODES
_EXTENSION_CODES = EXTENSION_RESIDUE_CODES
_TASK_CODE = TASK_RESIDUE_CODE


class OutDirRefused(ValueError, FileExistsError):
    """The destination directory already exists, or is inside the occurrence."""


# --------------------------------------------------------------------------- #
# mechanical text helpers - every rule here is published in the output         #
# --------------------------------------------------------------------------- #


def tokens(text: str) -> list[str]:
    """Lowercase, then every maximal run of ASCII letters/digits, in order."""
    return TOKEN_RE.findall(text.lower())


def record_prose(record: dict[str, Any]) -> str:
    """The record's prose fields, in :data:`RECORD_PROSE_FIELDS` order.

    Joined by a single space. Non-string values are skipped rather than
    coerced: the instrument does not repair a document (U4).
    """
    parts = [
        record[name]
        for name in RECORD_PROSE_FIELDS
        if isinstance(record.get(name), str) and record.get(name)
    ]
    return " ".join(parts)


def split_sentences(body: str) -> list[tuple[int, int, str]]:
    """Split one BODY into ``(start, end, text)`` spans.

    Offsets are Python string indices (Unicode code points) into ``body``;
    ``body[start:end] == text`` holds for every span. Leading and trailing
    whitespace is trimmed off each span *and out of its offsets*, so a cited
    span is exactly the sentence. Spans are non-overlapping and in body order;
    only whitespace lies between consecutive spans. The boundary rule is
    :data:`SENTENCE_BOUNDARY_RE` and nothing else - this is not linguistic
    sentence segmentation and does not pretend to be.
    """
    spans: list[tuple[int, int, str]] = []

    def emit(start: int, end: int) -> None:
        segment = body[start:end]
        lead = len(segment) - len(segment.lstrip())
        trail = len(segment) - len(segment.rstrip())
        a, b = start + lead, end - trail
        if b > a:
            spans.append((a, b, body[a:b]))

    cursor = 0
    for match in SENTENCE_BOUNDARY_RE.finditer(body):
        emit(cursor, match.end())
        cursor = match.end()
    emit(cursor, len(body))
    return spans


def _skip_ws(text: str, cursor: int) -> int:
    length = len(text)
    while cursor < length and text[cursor] in " \t\r\n":
        cursor += 1
    return cursor


def _records_array_start(commitments: str) -> int:
    """The offset just past the ``[`` of the **top-level** ``records`` array.

    Located by walking the top-level object's key/value pairs, not by the first
    textual match of ``"records"\s*:\s*[`` anywhere in the string: a prose
    field containing that literal would otherwise mislocate the cursor and a
    legal document would be refused.
    """
    decoder = json.JSONDecoder()
    length = len(commitments)
    cursor = _skip_ws(commitments, 0)
    if cursor >= length or commitments[cursor] != "{":
        raise MappingError("RECORDS_ARRAY_NOT_LOCATABLE")
    cursor = _skip_ws(commitments, cursor + 1)
    while cursor < length and commitments[cursor] == '"':
        try:
            key, cursor = decoder.raw_decode(commitments, cursor)
        except ValueError as exc:
            raise MappingError("RECORDS_ARRAY_NOT_LOCATABLE") from exc
        cursor = _skip_ws(commitments, cursor)
        if cursor >= length or commitments[cursor] != ":":
            raise MappingError("RECORDS_ARRAY_NOT_LOCATABLE")
        cursor = _skip_ws(commitments, cursor + 1)
        if key == "records":
            if cursor >= length or commitments[cursor] != "[":
                raise MappingError("RECORDS_ARRAY_NOT_LOCATABLE")
            return cursor + 1
        try:
            _value, cursor = decoder.raw_decode(commitments, cursor)
        except ValueError as exc:
            raise MappingError("RECORDS_ARRAY_NOT_LOCATABLE") from exc
        cursor = _skip_ws(commitments, cursor)
        if cursor < length and commitments[cursor] == ",":
            cursor = _skip_ws(commitments, cursor + 1)
            continue
        break
    raise MappingError("RECORDS_ARRAY_NOT_LOCATABLE")


def record_source_spans(commitments: str, document: dict[str, Any]) -> list[tuple[int, int]]:
    """Source spans of each record inside the decoded ``commitments`` string.

    Offsets are **code point offsets into the decoded ``commitments`` string**
    - Python string indices - exactly as in :func:`split_sentences`. They are
    NOT utf-8 byte offsets and they are NOT offsets into the artifact JSON
    file: ``commitments`` is itself a JSON-escaped string *value* inside that
    file, so the file must be decoded first and the value sliced by code point.
    A document carrying one non-ASCII character before a span makes the two
    kinds of offset differ, and ``daily/mini_fcl/cycle01/carry`` already does.

    The spans are what makes "verbatim" literal: ``commitments[start:end]`` is
    the record exactly as the author emitted it, whitespace and key order
    included. Every span is verified to re-parse equal to the parsed record
    before it is returned; a disagreement is a :class:`MappingError`, never a
    silent re-serialisation.
    """
    records = list(document.get("records", []))
    decoder = json.JSONDecoder()
    spans: list[tuple[int, int]] = []
    cursor = _records_array_start(commitments)
    length = len(commitments)
    while True:
        while cursor < length and commitments[cursor] in " \t\r\n":
            cursor += 1
        if cursor >= length:
            raise MappingError("RECORDS_ARRAY_UNTERMINATED")
        if commitments[cursor] == "]":
            break
        try:
            value, end = decoder.raw_decode(commitments, cursor)
        except ValueError as exc:  # pragma: no cover - defensive
            raise MappingError(f"RECORD_SPAN_UNPARSEABLE:{cursor}") from exc
        spans.append((cursor, end))
        if len(spans) > len(records):
            raise MappingError("RECORD_SPAN_COUNT_MISMATCH")
        if value != records[len(spans) - 1]:
            raise MappingError(f"RECORD_SPAN_DISAGREES:{len(spans) - 1}")
        cursor = end
        while cursor < length and commitments[cursor] in " \t\r\n":
            cursor += 1
        if cursor < length and commitments[cursor] == ",":
            cursor += 1
    if len(spans) != len(records):
        raise MappingError("RECORD_SPAN_COUNT_MISMATCH")
    return spans


# --------------------------------------------------------------------------- #
# the table                                                                    #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Passage:
    """One sentence of a referring BODY, with its offsets and its overlap."""

    start: int
    end: int
    text: str
    #: The distinctive tokens of the target record's text that occur in this
    #: sentence, sorted. An audit aid, never a measure: nothing is ordered,
    #: thresholded or compared by it.
    distinctive_tokens_present: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "start": self.start,
            "end": self.end,
            "text": self.text,
            "distinctive_tokens_present": list(self.distinctive_tokens_present),
        }


@dataclass(frozen=True)
class ResolverNote:
    """One note the importer's resolver attached to this ref, verbatim."""

    code: str
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {"code": self.code, "reason": self.reason}


@dataclass(frozen=True)
class UseRow:
    """One authored cross-document reference, juxtaposed with what it points at.

    Every field except the four ``root_*`` cells is a mechanical function of
    the occurrence bytes. The four ``root_*`` cells are emitted empty and are
    the only place a reading may be written.
    """

    referring_coordinate: dict[str, Any]
    referring_coordinate_key: str
    referring_record_id: str | None
    referring_record_type: str | None
    referring_record_verbatim: str | None
    referring_record_source_span: tuple[int, int] | None
    ref_field: str
    ref_verbatim: str
    #: "record" when the ref named a record of the owning document; "artifact"
    #: when it named the owning contribution as a whole (a bare exposed-artifact
    #: label, or the ``#BODY`` section header). Mechanical, not a judgement.
    ref_grain: str
    target_coordinate: dict[str, Any]
    target_coordinate_key: str
    target_record_id: str | None
    target_record_type: str | None
    target_record_verbatim: str | None
    target_record_source_span: tuple[int, int] | None
    #: What "the target's text" was taken to be for the overlap computation.
    overlap_subject: str
    referring_body_passages: tuple[Passage, ...]
    lexical_overlap_note: str
    declared_uptake_includes_referring_record: bool | None
    declared_uptake_includes_target_record: bool | None
    resolver_notes: tuple[ResolverNote, ...]
    # ---- reserved for root; emitted empty, never written by the tool ------- #
    root_reading: str = ""
    root_passage_cited: str = ""
    root_notes: str = ""
    root_initials_date: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "referring_coordinate": dict(self.referring_coordinate),
            "referring_coordinate_key": self.referring_coordinate_key,
            "referring_record_id": self.referring_record_id,
            "referring_record_type": self.referring_record_type,
            "referring_record_verbatim": self.referring_record_verbatim,
            "referring_record_source_span": (
                list(self.referring_record_source_span)
                if self.referring_record_source_span is not None
                else None
            ),
            "ref_field": self.ref_field,
            "ref_verbatim": self.ref_verbatim,
            "ref_grain": self.ref_grain,
            "target_coordinate": dict(self.target_coordinate),
            "target_coordinate_key": self.target_coordinate_key,
            "target_record_id": self.target_record_id,
            "target_record_type": self.target_record_type,
            "target_record_verbatim": self.target_record_verbatim,
            "target_record_source_span": (
                list(self.target_record_source_span)
                if self.target_record_source_span is not None
                else None
            ),
            "overlap_subject": self.overlap_subject,
            "referring_body_passages": [p.as_dict() for p in self.referring_body_passages],
            "lexical_overlap_note": self.lexical_overlap_note,
            "declared_uptake_includes_referring_record": (
                self.declared_uptake_includes_referring_record
            ),
            "declared_uptake_includes_target_record": (
                self.declared_uptake_includes_target_record
            ),
            "resolver_notes": [n.as_dict() for n in self.resolver_notes],
            "root_reading": self.root_reading,
            "root_passage_cited": self.root_passage_cited,
            "root_notes": self.root_notes,
            "root_initials_date": self.root_initials_date,
        }


@dataclass(frozen=True)
class UptakeEntry:
    """One declared ``uptake`` entry and what it resolved to."""

    ref_verbatim: str
    resolved_coordinate_key: str | None
    resolved_record_id: str | None
    resolver_notes: tuple[ResolverNote, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "ref_verbatim": self.ref_verbatim,
            "resolved_coordinate_key": self.resolved_coordinate_key,
            "resolved_record_id": self.resolved_record_id,
            "resolver_notes": [n.as_dict() for n in self.resolver_notes],
        }


@dataclass(frozen=True)
class DocumentUptake:
    """Declared ``uptake`` versus the records the document actually holds."""

    coordinate: dict[str, Any]
    coordinate_key: str
    commitment_surface: str
    records_present: tuple[str, ...]
    uptake_declared: tuple[str, ...]
    uptake_entries: tuple[UptakeEntry, ...]
    records_in_uptake: tuple[str, ...]
    records_omitted_from_uptake: tuple[str, ...]
    #: Disjoint and, with ``records_in_uptake``, exhaustive over
    #: ``uptake_entries``: the ref resolved to nothing; to another document; or
    #: to this contribution as a whole rather than to one of its records.
    uptake_entries_naming_nothing: tuple[str, ...]
    uptake_entries_naming_another_document: tuple[str, ...]
    uptake_entries_naming_this_contribution_not_a_record: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "coordinate": dict(self.coordinate),
            "coordinate_key": self.coordinate_key,
            "commitment_surface": self.commitment_surface,
            "records_present": list(self.records_present),
            "uptake_declared": list(self.uptake_declared),
            "uptake_entries": [e.as_dict() for e in self.uptake_entries],
            "records_in_uptake": list(self.records_in_uptake),
            "records_omitted_from_uptake": list(self.records_omitted_from_uptake),
            "uptake_entries_naming_nothing": list(self.uptake_entries_naming_nothing),
            "uptake_entries_naming_another_document": list(
                self.uptake_entries_naming_another_document
            ),
            "uptake_entries_naming_this_contribution_not_a_record": list(
                self.uptake_entries_naming_this_contribution_not_a_record
            ),
        }


@dataclass(frozen=True)
class NodeNotRead:
    """A node in scope whose commitment surface this instrument did not read."""

    coordinate: dict[str, Any]
    coordinate_key: str
    commitment_surface: str
    note: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "coordinate": dict(self.coordinate),
            "coordinate_key": self.coordinate_key,
            "commitment_surface": self.commitment_surface,
            "note": self.note,
        }


@dataclass(frozen=True)
class UnresolvedRef:
    """A ref an author wrote that resolves to nothing; residue, never dropped."""

    referring_coordinate_key: str
    referring_record_id: str | None
    ref_field: str
    ref_verbatim: str
    code: str
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "referring_coordinate_key": self.referring_coordinate_key,
            "referring_record_id": self.referring_record_id,
            "ref_field": self.ref_field,
            "ref_verbatim": self.ref_verbatim,
            "code": self.code,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class UseTable:
    """The whole instrument output: rows, uptake sections, residue, method."""

    schema: str
    instrument_version: str
    occurrence: str
    banner: str
    scope: tuple[dict[str, Any], ...]
    custody: dict[str, Any]
    method: dict[str, Any]
    rows: tuple[UseRow, ...]
    documents: tuple[DocumentUptake, ...]
    nodes_not_read: tuple[NodeNotRead, ...]
    unresolved_refs: tuple[UnresolvedRef, ...]
    reference_totals: dict[str, int]
    files_read: tuple[dict[str, str], ...]
    #: The resolved occurrence root, carried so that :func:`write_use_table`
    #: can enforce U1 ("nothing under the occurrence is ever written"). It is
    #: deliberately NOT serialised: an absolute path is machine-specific and
    #: would break the byte-identity of two builds on two checkouts. ``occurrence``
    #: above stays the display name.
    occurrence_root: str = ""

    # -- serialisation ------------------------------------------------------ #

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "instrument_version": self.instrument_version,
            "occurrence": self.occurrence,
            "banner": self.banner,
            "scope": [dict(c) for c in self.scope],
            "custody": self.custody,
            "method": self.method,
            "rows": [r.as_dict() for r in self.rows],
            "documents": [d.as_dict() for d in self.documents],
            "nodes_not_read": [n.as_dict() for n in self.nodes_not_read],
            "unresolved_refs": [u.as_dict() for u in self.unresolved_refs],
            "reference_totals": dict(self.reference_totals),
            "files_read": [dict(f) for f in self.files_read],
        }

    def to_json(self) -> str:
        """Deterministic JSON. No clock, no environment, no iteration order."""
        return json.dumps(self.as_dict(), ensure_ascii=False, indent=2) + "\n"

    # -- markdown ----------------------------------------------------------- #

    @staticmethod
    def _fence(text: str, language: str = "json") -> list[str]:
        """Fence a verbatim block without ever altering the bytes inside it."""
        ticks = "```"
        while ticks in text:
            ticks += "`"
        return [ticks + language, text, ticks]

    def _row_markdown(self, index: int, row: UseRow) -> list[str]:
        referring = (
            f"`{row.referring_coordinate_key}#{row.referring_record_id}`"
            if row.referring_record_id
            else f"`{row.referring_coordinate_key}` (document-level `{row.ref_field}`)"
        )
        target = (
            f"`{row.target_coordinate_key}#{row.target_record_id}`"
            if row.target_record_id
            else f"`{row.target_coordinate_key}` (whole contribution)"
        )
        out: list[str] = []
        out.append(f"### Row {index} - {referring} --{row.ref_field}--> {target}")
        out.append("")
        out.append("| field | value |")
        out.append("|---|---|")
        out.append(f"| referring coordinate | `{row.referring_coordinate_key}` |")
        out.append(
            "| referring record | "
            + (
                f"`{row.referring_record_id}` (type `{row.referring_record_type}`) |"
                if row.referring_record_id
                else "none - the ref is the document-level `uptake` list |"
            )
        )
        out.append(f"| ref field | `{row.ref_field}` |")
        out.append(f"| ref verbatim | `{row.ref_verbatim}` |")
        out.append(f"| ref grain | {row.ref_grain} |")
        out.append(f"| resolved target coordinate | `{row.target_coordinate_key}` |")
        out.append(
            "| resolved target record | "
            + (
                f"`{row.target_record_id}` (type `{row.target_record_type}`) |"
                if row.target_record_id
                else "none - the ref names the owning contribution, not a record |"
            )
        )
        out.append(
            "| declared_uptake_includes_referring_record | "
            + _yesno(row.declared_uptake_includes_referring_record)
            + " |"
        )
        out.append(
            "| declared_uptake_includes_target_record | "
            + _yesno(row.declared_uptake_includes_target_record)
            + " |"
        )
        out.append("")
        if row.resolver_notes:
            out.append("Resolver notes (from the importer, verbatim):")
            out.append("")
            for note in row.resolver_notes:
                out.append(f"- `{note.code}`: {note.reason}")
            out.append("")
        out.append(f"**Referring record, verbatim** (`{row.referring_coordinate_key}`"
                   + (f", `commitments[{row.referring_record_source_span[0]}:"
                      f"{row.referring_record_source_span[1]}]`, code point offsets "
                      "into the decoded `commitments` string)"
                      if row.referring_record_source_span else ")"))
        out.append("")
        if row.referring_record_verbatim is None:
            out.append("*(none: the ref is the document-level `uptake` list)*")
        else:
            out.extend(self._fence(row.referring_record_verbatim))
        out.append("")
        out.append(f"**Resolved target record, verbatim** (`{row.target_coordinate_key}`"
                   + (f", `commitments[{row.target_record_source_span[0]}:"
                      f"{row.target_record_source_span[1]}]`, code point offsets "
                      "into the decoded `commitments` string)"
                      if row.target_record_source_span else ")"))
        out.append("")
        if row.target_record_verbatim is None:
            out.append(
                "*(none: the ref names the owning contribution as a whole; the overlap "
                "subject below says what was compared)*"
            )
        else:
            out.extend(self._fence(row.target_record_verbatim))
        out.append("")
        out.append(
            f"**Referring BODY passages** (overlap subject: {row.overlap_subject}; "
            "offsets are code point offsets into the decoded `body` string). The "
            "listed passages are a finding aid, not a search space: root may cite any "
            "passage of either contribution, including one the rule did not surface."
        )
        out.append("")
        if not row.referring_body_passages:
            out.append(f"*{row.lexical_overlap_note}*")
        else:
            for passage in row.referring_body_passages:
                out.append(f"- `body[{passage.start}:{passage.end}]` - distinctive tokens "
                           + ", ".join(f"`{t}`" for t in passage.distinctive_tokens_present))
                out.extend("  " + line for line in self._fence(passage.text, "text"))
        out.append("")
        out.append("**Reserved for root - left empty by the instrument**")
        out.append("")
        out.append(
            "An empty cell is an **unread row**, not a reading of `unresolved`. See "
            "the Method block for the suggested `root_reading` vocabulary, which is a "
            "suggestion and not a closed single-valued enum."
        )
        out.append("")
        out.append("| root_reading | root_passage_cited | root_notes | root_initials_date |")
        out.append("|---|---|---|---|")
        out.append("|  |  |  |  |")
        out.append("")
        return out

    def to_markdown(self) -> str:
        out: list[str] = []
        out.append("# Use-relation table - H005 " + self.occurrence)
        out.append("")
        out.append(self.banner)
        out.append("")
        out.append(f"Instrument: `{self.instrument_version}`. Schema: `{self.schema}`.")
        out.append("")
        out.append("## Scope")
        out.append("")
        for coord in self.scope:
            out.append(
                "- `%s/%s/cycle%02d/%s`"
                % (coord["problem"], coord["arm"], coord["cycle"], coord["node"])
            )
        out.append("")
        out.append("## Custody")
        out.append("")
        out.append(f"- `plan_id`: `{self.custody['plan_id']}`")
        out.append(f"- `material_sha256`: `{self.custody['material_sha256']}`")
        out.append("")
        out.append("| check | kind | result |")
        out.append("|---|---|---|")
        for kind in ("cross_file", "self_consistency"):
            for check in self.custody["checks"].get(kind, []):
                out.append(f"| `{check['key']}` | {check['kind']} | {check['result']} |")
        out.append("")
        out.append(
            "Custody is the importer's own check, reused unchanged; a self-consistency "
            "check cannot detect a coherent rewrite of the one file it reads."
        )
        out.append("")
        out.append("## Method - exactly what the mechanical columns mean")
        out.append("")
        for line in self.method["prose"]:
            out.append(line)
            out.append("")
        out.append("Stopword list (closed, frozen in the module):")
        out.append("")
        out.append("> " + ", ".join(f"`{w}`" for w in self.method["stopwords"]))
        out.append("")
        out.append(
            "The two regular expressions, verbatim, so this page alone is enough to "
            "re-derive every passage:"
        )
        out.append("")
        out.append("| rule | pattern |")
        out.append("|---|---|")
        out.append("| `token_regex` | `" + self.method["token_regex"] + "` |")
        out.append(
            "| `sentence_boundary_regex` | `"
            + self.method["sentence_boundary_regex"]
            + "` |"
        )
        out.append("")
        out.append(
            "Offsets: " + self.method["span_offsets"] + ". To check a quote: decode the "
            "artifact JSON, take the `commitments` (or `body`) string value, and slice "
            "it by code point - a byte tool pointed at the file will not agree wherever "
            "a non-ASCII character precedes the span."
        )
        out.append("")
        out.append(
            "Resolution order (the importer's own): "
            + ", ".join(f"`{f}`" for f in self.method["ref_fields_resolution_order"])
            + ". Display order in this table: "
            + ", ".join(f"`{f}`" for f in self.method["ref_fields_walked"])
            + "."
        )
        out.append("")
        out.append(
            "`root_reading` has a suggested vocabulary: "
            + ", ".join(f"`{v}`" for v in self.method["root_reading_vocabulary"])
            + ". A row may carry more than one, and root may write a reading this "
            "vocabulary does not cover and say so; `unresolved` is legal and stays "
            "unresolved. The instrument never selects one."
        )
        out.append("")
        out.append("## Reference totals")
        out.append("")
        out.append("| quantity | count |")
        out.append("|---|---|")
        for key, value in self.reference_totals.items():
            out.append(f"| {key.replace('_', ' ')} | {value} |")
        out.append("")
        out.append(
            "These are counts of authored refs, reported as information. No count here "
            "warrants anything (FW5:851: counts \"are not outlawed as information\"; what "
            "is forbidden is a count entering as an *automatic* warrant)."
        )
        out.append("")
        out.append("## Rows")
        out.append("")
        if not self.rows:
            out.append("*No cross-document reference in scope.*")
            out.append("")
        for index, row in enumerate(self.rows, start=1):
            out.extend(self._row_markdown(index, row))
        out.append("## Declared uptake versus records present")
        out.append("")
        for document in self.documents:
            out.append(f"### `{document.coordinate_key}`")
            out.append("")
            out.append(f"- commitment surface: `{document.commitment_surface}`")
            out.append(
                "- records present ("
                + str(len(document.records_present))
                + "): "
                + (", ".join(f"`{r}`" for r in document.records_present) or "*none*")
            )
            out.append(
                "- declared `uptake` ("
                + str(len(document.uptake_declared))
                + "): "
                + (", ".join(f"`{r}`" for r in document.uptake_declared) or "*none*")
            )
            out.append(
                "- records in uptake ("
                + str(len(document.records_in_uptake))
                + "): "
                + (", ".join(f"`{r}`" for r in document.records_in_uptake) or "*none*")
            )
            out.append(
                "- records omitted from uptake ("
                + str(len(document.records_omitted_from_uptake))
                + "): "
                + (", ".join(f"`{r}`" for r in document.records_omitted_from_uptake) or "*none*")
            )
            out.append(
                "- uptake entries naming nothing ("
                + str(len(document.uptake_entries_naming_nothing))
                + "): "
                + (
                    ", ".join(f"`{r}`" for r in document.uptake_entries_naming_nothing)
                    or "*none*"
                )
            )
            out.append(
                "- uptake entries naming another document ("
                + str(len(document.uptake_entries_naming_another_document))
                + "): "
                + (
                    ", ".join(
                        f"`{r}`" for r in document.uptake_entries_naming_another_document
                    )
                    or "*none*"
                )
            )
            out.append(
                "- uptake entries naming this contribution, not one of its records ("
                + str(
                    len(document.uptake_entries_naming_this_contribution_not_a_record)
                )
                + "): "
                + (
                    ", ".join(
                        f"`{r}`"
                        for r in
                        document.uptake_entries_naming_this_contribution_not_a_record
                    )
                    or "*none*"
                )
            )
            out.append("")
            out.append(
                "The three buckets above are disjoint and, together with the records "
                "of this document that the list does name, exhaust `uptake`: a ref "
                "resolves to nothing, to another document, to this contribution as a "
                "whole, or to one of this document's own records."
            )
            out.append(
                "An omission from `uptake` is a fact about the declaration, not a defect "
                "and not a withdrawal. `uptake` \"is a local claim about standing, not a "
                "harness verdict or a truth label\" (FCL-1 proposition)."
            )
            out.append("")
        out.append("## Nodes whose commitment surface was not read")
        out.append("")
        if not self.nodes_not_read:
            out.append("*None in this scope.*")
        else:
            for node in self.nodes_not_read:
                out.append(f"- `{node.coordinate_key}` - {node.note}")
        out.append("")
        out.append("## Residue: refs that resolve to nothing")
        out.append("")
        if not self.unresolved_refs:
            out.append("*No unresolved ref in this scope.*")
        else:
            out.append("| referring coordinate | record | field | ref | code | reason |")
            out.append("|---|---|---|---|---|---|")
            for residue in self.unresolved_refs:
                out.append(
                    "| `%s` | `%s` | `%s` | `%s` | `%s` | %s |"
                    % (
                        residue.referring_coordinate_key,
                        residue.referring_record_id or "-",
                        residue.ref_field,
                        residue.ref_verbatim,
                        residue.code,
                        residue.reason,
                    )
                )
        out.append("")
        out.append("## Files read")
        out.append("")
        out.append(
            "Every byte this instrument read, with its sha256. Nothing under the "
            "occurrence was written."
        )
        out.append("")
        out.append("| path | sha256 |")
        out.append("|---|---|")
        for entry in self.files_read:
            out.append(f"| `{entry['path']}` | `{entry['sha256']}` |")
        out.append("")
        return "\n".join(out) + "\n"


def _yesno(value: bool | None) -> str:
    if value is None:
        return "n/a"
    return "true" if value else "false"


# --------------------------------------------------------------------------- #
# building                                                                     #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class _Resolution:
    """One walked ref and everything the importer's resolver said about it.

    Built from a :class:`minireason.graph_import_h005.ReferenceRecord`: the
    owner, the target record id, the verdict and the notes are the import's
    own, not this module's reading of them.
    """

    node: _Node
    record: dict[str, Any] | None
    record_index: int | None
    field_name: str
    ref: str
    ref_index: int
    owner: Coordinate | None
    record_id: str | None
    notes: tuple[ResolverNote, ...]
    #: The importer's own verdict: ``resolved``/``extension``/``unresolved``/
    #: ``task``.
    resolution: str

    @property
    def is_task(self) -> bool:
        return self.resolution == "task"

    @property
    def is_unresolved(self) -> bool:
        return self.resolution == "unresolved"

    @property
    def is_extension(self) -> bool:
        return self.resolution == "extension"

    @property
    def is_cross_document(self) -> bool:
        return self.owner is not None and self.owner != self.node.coord


def _walk_references(
    occurrence_dir: str | Path,
    importer: _Importer,
    *,
    problems: Sequence[str] | None,
    arms: Sequence[str] | None,
    cycles: Sequence[int] | None,
) -> list[_Resolution]:
    """Every authored ref in scope, resolved by the importer's own public walk.

    :func:`minireason.graph_import_h005.iter_references` owns the field order,
    the two-phase-per-node split and the wave-order availability set - every
    node becomes available when it is reached, document or not, exactly as
    ``map_records`` names every node in ``self.order``. This function only
    re-attaches each yielded ref to the parsed record it came from, so the
    table can quote it; it makes no resolution decision of its own and writes
    nothing into any importer structure.
    """
    index_by_id: dict[str, dict[Any, int]] = {}
    for coord in importer.order:
        node = importer.nodes[coord]
        if node.document is None:
            continue
        positions: dict[Any, int] = {}
        for position, record in enumerate(node.records):
            positions.setdefault(record.get("id"), position)
        index_by_id[coord.key] = positions

    counters: dict[tuple[str, Any, str], int] = {}
    resolutions: list[_Resolution] = []
    for entry in iter_references(
        occurrence_dir, problems=problems, arms=arms, cycles=cycles
    ):
        node = importer.nodes[entry.coordinate]
        record = None
        record_index = None
        if entry.record_id is not None:
            record_index = index_by_id[entry.coordinate.key][entry.record_id]
            record = node.records[record_index]
        counter_key = (entry.coordinate.key, entry.record_id, entry.field)
        ref_index = counters.get(counter_key, 0)
        counters[counter_key] = ref_index + 1
        resolutions.append(
            _Resolution(
                node=node,
                record=record,
                record_index=record_index,
                field_name=entry.field,
                ref=entry.raw_ref,
                ref_index=ref_index,
                owner=entry.owner_coordinate,
                record_id=entry.target_record_id,
                notes=tuple(
                    ResolverNote(code=code, reason=reason) for code, reason in entry.notes
                ),
                resolution=entry.resolution,
            )
        )
    return resolutions


def _display_key(resolution: _Resolution) -> tuple[Any, ...]:
    """Row order: node in wave order, record in document order, field, ref index.

    ``uptake`` is document-level and sorts after every record of its document:
    its sub-key is ``len(node.records)``, one past the last record index.
    """
    field_rank = (
        len(REF_FIELDS)
        if resolution.field_name == "uptake"
        else REF_FIELDS.index(resolution.field_name)
    )
    return (
        len(resolution.node.records)
        if resolution.record_index is None
        else resolution.record_index,
        field_rank,
        resolution.ref_index,
    )


def uptake_buckets(
    walked: Sequence["_Resolution"], coordinate: Coordinate
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """The three non-ordinary outcomes of a document's ``uptake`` refs.

    Returns ``(naming_nothing, naming_another_document,
    naming_this_contribution_not_a_record)``. The three are **disjoint**, and
    together with the ordinary outcome - the ref resolves to a record of this
    same document, reported as ``records_in_uptake`` - they are **exhaustive**
    over ``uptake_entries``.

    "Naming nothing" is gated on the OWNER being ``None``, not on the record id:
    the resolver returns ``(owner, None)`` for a ref that names a whole
    contribution (a bare exposed-artifact label, or a ``#BODY`` pseudo-local),
    which names something. Gating on the record id put such a ref in
    "naming nothing" and in "naming another document" at once - two
    contradictory cells of the same section, read directly by root.
    """
    nothing = tuple(r.ref for r in walked if r.owner is None)
    another = tuple(r.ref for r in walked if r.owner is not None and r.owner != coordinate)
    whole = tuple(
        r.ref
        for r in walked
        if r.owner is not None and r.owner == coordinate and r.record_id is None
    )
    return nothing, another, whole


def _document_frequency(importer: _Importer) -> tuple[dict[str, int], int]:
    """Token -> how many in-scope FCL-1 documents have it in their record prose."""
    frequency: dict[str, int] = {}
    documents = 0
    for coord in importer.order:
        node = importer.nodes[coord]
        if node.document is None:
            continue
        documents += 1
        seen = {
            token
            for record in node.records
            for token in tokens(record_prose(record))
        }
        for token in seen:
            frequency[token] = frequency.get(token, 0) + 1
    return frequency, documents


def _passages(
    body: str,
    target_text: str,
    frequency: dict[str, int],
    threshold: int,
) -> tuple[tuple[Passage, ...], str]:
    """The referring BODY sentences that carry a distinctive token of the target."""
    distinctive = {
        token
        for token in tokens(target_text)
        if len(token) >= MIN_TOKEN_LENGTH
        and token not in _STOPWORDS_SET
        and frequency.get(token, 0) <= threshold
    }
    found: list[Passage] = []
    for start, end, text in split_sentences(body):
        present = sorted(distinctive.intersection(tokens(text)))
        if present:
            found.append(
                Passage(start=start, end=end, text=text, distinctive_tokens_present=tuple(present))
            )
    return tuple(found), ("" if found else NO_OVERLAP_NOTE)


def _method(
    importer: _Importer, threshold: int, corpus_documents: Sequence[str]
) -> dict[str, Any]:
    prose = [
        "**Sentence.** The referring node's `body` is cut at every match of the published "
        "boundary regular expression and nowhere else; leading and trailing whitespace is "
        "trimmed out of each span *and out of its offsets*, so `body[start:end]` is exactly "
        "the quoted sentence. The boundary is one or more of `.` `!` `?` preceded by a "
        "lowercase letter or a closing bracket/quote and followed by whitespace or "
        "end-of-string, together with any closing quotes that follow it; or a run of "
        "newlines. This is not linguistic sentence segmentation: a numbered list marker "
        "(\"1. Separate ...\") does not split, and an abbreviation such as \"e.g.\" does.",
        "**Token.** The string is lowercased and every maximal run of ASCII letters and "
        "digits is a token, in order of occurrence.",
        "**The target record's text.** The concatenation, separated by single spaces, of "
        "the target record's prose fields in this order: "
        + ", ".join(f"`{name}`" for name in RECORD_PROSE_FIELDS)
        + ". `id`, `type` and every ref array are excluded: they are names and pointers, "
        "not content. When the ref names the owning contribution as a whole rather than "
        "one of its records - a bare exposed-artifact label, or the `#BODY` section header "
        "- the subject is instead the same concatenation over **every** record of the "
        "owning document, in document order, and the row says so in `overlap_subject`.",
        "**Distinctive token.** A token `t` of the target record's text is *distinctive* "
        "when all three hold: (1) `len(t) >= "
        + str(MIN_TOKEN_LENGTH)
        + "` characters after lowercasing; (2) `t` is not in the closed stopword list "
        "below; (3) `document_frequency(t) <= "
        + str(threshold)
        + "`, where `document_frequency(t)` is the number of in-scope FCL-1 documents "
        "whose record prose contains `t`, and the threshold is `max(2, number_of_in_scope_"
        "FCL-1_documents // 2)` - here `max(2, "
        + str(len(corpus_documents))
        + " // 2)`. Clause (3) makes the criterion **scope-dependent**: it is computed "
        "over the documents listed under `corpus_documents`, and re-running over a "
        "different scope can change which tokens count. That is stated rather than hidden, "
        "because a partition-invariance question about this instrument (review \u00a75 P5) has "
        "to be answerable from its own output.",
        "**A passage is listed** when the sentence contains at least one distinctive token "
        "of the target record's text. Passages are listed in body order, never ordered or "
        "selected by how many tokens they carry; `distinctive_tokens_present` is an audit "
        "aid so a reader can see *why* a sentence was listed, and is not a measure. When no "
        "sentence qualifies the row says `"
        + NO_OVERLAP_NOTE
        + "`.",
        "**What a listed passage is not.** It is not evidence that the referring node used "
        "the target's content, and its absence is not evidence that it did not. Shared "
        "vocabulary is shared vocabulary. The relation columns of this table report what an "
        "author *wrote* in a ref-valued field; the passage columns report what a mechanical "
        "string comparison found; neither is a reading, and the four `root_*` cells are "
        "where a reading would go.",
        "**Declared uptake columns.** `declared_uptake_includes_referring_record` is true "
        "when the referring record's local name is in its own document's `uptake` list; "
        "`declared_uptake_includes_target_record` is true when the target record's local "
        "name is in the *target* document's `uptake` list. `n/a` means the row has no such "
        "record to look up (a document-level `uptake` ref has no referring record; a ref to "
        "a whole contribution has no target record).",
    ]
    prose = prose + [
        "**What a blank root cell means.** An empty `root_reading`, "
        "`root_passage_cited`, `root_notes` or `root_initials_date` is an "
        "**unread row**: nobody has read it yet. It is *not* a reading of "
        "`unresolved`, and it is not a finding of indeterminacy. `unresolved` is a "
        "reading root may write, deliberately, and it then stays unresolved "
        "(FW5:634); a blank cell asserts nothing at all. Conflating the two would "
        "let an unfinished worksheet read as a finding, which is exactly the move "
        "FW5:688 forbids.",
        "**What the listed passages are.** A finding aid, not a search space. The "
        "overlap rule is mechanical and shallow; root may cite **any** passage of "
        "either contribution, including one this rule did not surface, and a row "
        "with `"
        + NO_OVERLAP_NOTE
        + "` is not a row with nothing to read. `root_passage_cited` is free text "
        "for that reason.",
        "**The `root_reading` vocabulary is a suggestion.** The six values below "
        "are published so that two readers of two tables mean the same thing by the "
        "same word, not to constrain root to one of them: a row may carry more than "
        "one, and root may write a reading the vocabulary does not cover and say so. "
        "Nothing about it is enforced in code.",
    ]
    return {
        "prose": prose,
        "token_regex": TOKEN_RE.pattern,
        "sentence_boundary_regex": SENTENCE_BOUNDARY_RE.pattern,
        "record_prose_fields": list(RECORD_PROSE_FIELDS),
        #: The order refs are RESOLVED in - the importer's own published order,
        #: consumed from ``graph_import_h005.REF_FIELDS``, not copied. An
        #: objection's ``target`` is resolved in a second pass, after the
        #: carrier is available in wave order.
        "ref_fields_resolution_order": list(IMPORTER_REF_FIELDS)
        + ["uptake", "target (objection, pass 2)"],
        #: The order rows are DISPLAYED in. Presentation only.
        "ref_fields_walked": list(REF_FIELDS) + ["uptake"],
        "span_offsets": (
            "code point offsets into the decoded `commitments` string (Python "
            "string indices), not utf-8 byte offsets and not offsets into the "
            "artifact JSON file"
        ),
        "min_token_length": MIN_TOKEN_LENGTH,
        "stopwords": list(STOPWORDS),
        "distinctive_document_frequency_threshold": threshold,
        "corpus_documents": list(corpus_documents),
        "root_cells": list(ROOT_CELLS),
        "root_reading_vocabulary": list(ROOT_READING_VOCABULARY),
        "reused_from_importer": [
            "verify_custody",
            "parse_fcl1_document / fcl1_validator (FCL-1 schema validation)",
            "_Reader (read-only, path-confined, sha256-recording occurrence reader)",
            "_Importer.discover_scope / load_nodes / parse_documents",
            "iter_references (the import's own public reference walk: field "
            "order, wave-order availability and two-hop resolution)",
            "UNRESOLVED_RESIDUE_CODES / EXTENSION_RESIDUE_CODES (the import's "
            "own classification of what a residue code means for a ref)",
        ],
        "not_used_from_importer": [
            "graph construction (Harness, registration, events)",
            "adjudication (build_att / build_dep / label computation)",
            "every status and label the importer computes",
        ],
    }


def build_use_table(
    occurrence_dir: str | Path,
    *,
    problems: Sequence[str] | None = None,
    arms: Sequence[str] | None = None,
    cycles: Sequence[int] | None = None,
) -> UseTable:
    """Build the use-relation table for one H005 occurrence.

    Read-only on the occurrence; nothing is written. Raises
    :class:`CustodyError` if the occurrence fails the importer's custody check,
    :class:`SelectorMatchedNothing` if the selectors match no coordinate, and
    :class:`MappingError` for a structural failure (no coordinate at all, a
    record whose source span cannot be recovered).
    """
    importer = _Importer(occurrence_dir, problems, arms, cycles)
    custody = verify_custody(importer.reader, importer.ledger)
    scope = importer.discover_scope(custody["material"], custody["plan"])
    importer.load_nodes(scope, custody["plan"])
    importer.parse_documents()

    frequency, document_count = _document_frequency(importer)
    threshold = max(2, document_count // 2)
    corpus_documents = [
        coord.key for coord in importer.order if importer.nodes[coord].document is not None
    ]

    spans: dict[str, list[tuple[int, int]]] = {}
    for coord in importer.order:
        node = importer.nodes[coord]
        if node.document is None:
            continue
        spans[coord.key] = record_source_spans(node.record["commitments"], node.document)

    resolutions = _walk_references(
        occurrence_dir, importer, problems=problems, arms=arms, cycles=cycles
    )

    # Declared uptake, per document, from the walked uptake resolutions.
    uptake_by_document: dict[str, list[_Resolution]] = {}
    for resolution in resolutions:
        if resolution.field_name == "uptake":
            uptake_by_document.setdefault(resolution.node.coord.key, []).append(resolution)

    uptake_records: dict[str, set[str]] = {}
    documents: list[DocumentUptake] = []
    for coord in importer.order:
        node = importer.nodes[coord]
        if node.document is None:
            continue
        walked = uptake_by_document.get(coord.key, [])
        entries = tuple(
            UptakeEntry(
                ref_verbatim=r.ref,
                resolved_coordinate_key=r.owner.key if r.owner is not None else None,
                resolved_record_id=r.record_id,
                resolver_notes=r.notes,
            )
            for r in walked
        )
        local = tuple(
            r.record_id
            for r in walked
            if r.owner == coord and r.record_id is not None
        )
        uptake_records[coord.key] = set(local)
        buckets = uptake_buckets(walked, coord)
        present = tuple(str(record.get("id")) for record in node.records)
        documents.append(
            DocumentUptake(
                coordinate=coord.as_dict(),
                coordinate_key=coord.key,
                commitment_surface=node.commitment_surface_state,
                records_present=present,
                uptake_declared=tuple(str(r) for r in (node.document.get("uptake") or [])),
                uptake_entries=entries,
                records_in_uptake=tuple(rid for rid in present if rid in set(local)),
                records_omitted_from_uptake=tuple(
                    rid for rid in present if rid not in set(local)
                ),
                uptake_entries_naming_nothing=buckets[0],
                uptake_entries_naming_another_document=buckets[1],
                uptake_entries_naming_this_contribution_not_a_record=buckets[2],
            )
        )

    # Rows: every cross-document ref, in display order.
    ordered = sorted(
        (r for r in resolutions if r.is_cross_document),
        key=lambda r: (importer.order.index(r.node.coord),) + _display_key(r),
    )
    rows: list[UseRow] = []
    for resolution in ordered:
        node = resolution.node
        owner = resolution.owner
        assert owner is not None
        owner_node = importer.nodes[owner]
        target_record = None
        target_span = None
        if resolution.record_id is not None:
            for index, record in enumerate(owner_node.records):
                if record.get("id") == resolution.record_id:
                    target_record = record
                    target_span = spans[owner.key][index]
                    break
            if target_record is None:  # pragma: no cover - resolver guarantees it
                raise MappingError(f"TARGET_RECORD_VANISHED:{owner.key}#{resolution.record_id}")
            target_text = record_prose(target_record)
            overlap_subject = (
                f"the prose fields of `{owner.key}#{resolution.record_id}`"
            )
            grain = "record"
        else:
            target_text = " ".join(record_prose(record) for record in owner_node.records)
            overlap_subject = (
                f"the prose fields of every record of `{owner.key}` "
                "(the ref names the contribution, not a record)"
            )
            grain = "artifact"
        referring_verbatim = None
        referring_span = None
        if resolution.record is not None and resolution.record_index is not None:
            referring_span = spans[node.coord.key][resolution.record_index]
            referring_verbatim = node.record["commitments"][referring_span[0]:referring_span[1]]
        passages, note = _passages(
            node.record["body"], target_text, frequency, threshold
        )
        rows.append(
            UseRow(
                referring_coordinate=node.coord.as_dict(),
                referring_coordinate_key=node.coord.key,
                referring_record_id=(
                    None if resolution.record is None else str(resolution.record.get("id"))
                ),
                referring_record_type=(
                    None if resolution.record is None else str(resolution.record.get("type"))
                ),
                referring_record_verbatim=referring_verbatim,
                referring_record_source_span=referring_span,
                ref_field=resolution.field_name,
                ref_verbatim=resolution.ref,
                ref_grain=grain,
                target_coordinate=owner.as_dict(),
                target_coordinate_key=owner.key,
                target_record_id=resolution.record_id,
                target_record_type=(
                    None if target_record is None else str(target_record.get("type"))
                ),
                target_record_verbatim=(
                    None
                    if target_span is None
                    else owner_node.record["commitments"][target_span[0]:target_span[1]]
                ),
                target_record_source_span=target_span,
                overlap_subject=overlap_subject,
                referring_body_passages=passages,
                lexical_overlap_note=note,
                declared_uptake_includes_referring_record=(
                    None
                    if resolution.record is None
                    else str(resolution.record.get("id"))
                    in uptake_records.get(node.coord.key, set())
                ),
                declared_uptake_includes_target_record=(
                    None
                    if resolution.record_id is None
                    else resolution.record_id in uptake_records.get(owner.key, set())
                ),
                resolver_notes=resolution.notes,
            )
        )

    nodes_not_read = tuple(
        NodeNotRead(
            coordinate=importer.nodes[coord].coord.as_dict(),
            coordinate_key=coord.key,
            commitment_surface=importer.nodes[coord].commitment_surface_state,
            note=(
                PROSE_SURFACE_NOTE
                if importer.nodes[coord].commitment_surface_state == "prose_not_parsed"
                else "commitment surface: "
                + importer.nodes[coord].commitment_surface_state
                + "; references not extractable by this instrument"
            ),
        )
        for coord in importer.order
        if importer.nodes[coord].document is None
    )

    unresolved = tuple(
        UnresolvedRef(
            referring_coordinate_key=resolution.node.coord.key,
            referring_record_id=(
                None if resolution.record is None else str(resolution.record.get("id"))
            ),
            ref_field=resolution.field_name,
            ref_verbatim=resolution.ref,
            code=note.code,
            reason=note.reason,
        )
        for resolution in resolutions
        if resolution.is_unresolved
        for note in resolution.notes
        if note.code in _UNRESOLVED_CODES
    )

    totals = {
        "refs_walked": len(resolutions),
        "cross_document_rows": len(rows),
        "intra_document": sum(
            1 for r in resolutions if r.owner is not None and r.owner == r.node.coord
        ),
        "refs_to_exposed_task_artifact": sum(1 for r in resolutions if r.is_task),
        "unresolved": sum(1 for r in resolutions if r.is_unresolved),
        # The importer's own verdict on each ref, tallied. `resolved` is the
        # importer's counter, which counts a task ref as resolved (it resolves
        # to the root Problem, which is not an artifact).
        "importer_resolved_counter": sum(
            1 for r in resolutions if r.resolution in ("resolved", "task")
        ),
        "importer_extension_counter": sum(1 for r in resolutions if r.is_extension),
        "importer_dangling_counter": sum(1 for r in resolutions if r.is_unresolved),
    }

    return UseTable(
        schema=USE_TABLE_SCHEMA,
        instrument_version=INSTRUMENT_VERSION,
        occurrence=Path(occurrence_dir).name,
        occurrence_root=str(Path(occurrence_dir).resolve()),
        banner=USE_RELATION_BANNER,
        scope=tuple(coord.as_dict() for coord in importer.order),
        custody={
            "plan_id": custody["plan_id"],
            "material_sha256": custody["material_sha256"],
            "checks": importer.ledger.as_dict(),
        },
        method=_method(importer, threshold, corpus_documents),
        rows=tuple(rows),
        documents=tuple(documents),
        nodes_not_read=nodes_not_read,
        unresolved_refs=unresolved,
        reference_totals=totals,
        files_read=tuple(
            {"path": path, "sha256": digest}
            for path, digest in sorted(importer.reader.files.items())
        ),
    )


def write_use_table(table: UseTable, out_dir: str | Path) -> tuple[Path, Path]:
    """Write ``USE_TABLE.md`` and ``use_table.json`` into a NEW directory.

    Two refusals, both :class:`OutDirRefused`:

    * ``OUT_DIR_INSIDE_OCCURRENCE`` - the destination is the occurrence or lies
      inside it. Standing invariant U1 says nothing under the occurrence is
      ever written, and the published importer has exactly this guard
      (``OUT_ROOT_INSIDE_OCCURRENCE``); checked first, before anything is
      created.
    * ``OUT_DIR_EXISTS`` - the directory already exists. An instrument output is
      written once and is then a citable artifact, so a re-run names a new
      destination rather than overwriting a table someone may already have read
      or annotated.
    """
    target = Path(out_dir)
    resolved = target.resolve()
    if table.occurrence_root:
        root = Path(table.occurrence_root).resolve()
        if resolved == root or root in resolved.parents:
            raise OutDirRefused(f"OUT_DIR_INSIDE_OCCURRENCE:{target}")
    if target.exists():
        raise OutDirRefused(f"OUT_DIR_EXISTS:{target}")
    target.mkdir(parents=True, exist_ok=False)
    markdown = target / "USE_TABLE.md"
    document = target / "use_table.json"
    try:
        markdown.write_text(table.to_markdown(), encoding="utf-8")
        document.write_text(table.to_json(), encoding="utf-8")
    except OSError:
        # Never leave half an output directory behind: a partially written
        # table is not a citable artifact and must not look like one.
        for path in (markdown, document):
            try:
                path.unlink()
            except OSError:
                pass
        try:
            target.rmdir()
        except OSError:
            pass
        raise
    return markdown, document
