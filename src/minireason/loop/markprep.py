"""The C001 program pre-pass and the sealed within-ORIGINAL replicate baseline.

What this is
------------
Everything the *program* can settle about a C001 contrast cell before any
marker call is made, and nothing else.  One cell is one ``(endpoint, arm)``
table of a published C001 occurrence: four cases (ORIGINAL, RECODING, CARRIER,
CONTROL), five replicates each, read off ``comparison.json`` and the raw
delivered bytes in ``juxtaposition/<endpoint>__<arm>.md``.

Five things happen here, in the design's own order:

1. **The byte-identity defeater (G10(a)).**  PLAN §8's mechanical defeater:
   where every resolved ORIGINAL replicate's ``commitments`` is byte-identical
   to some resolved CONTROL replicate's, **D1 is not exhibited in that cell**.
   It is computed first, before anything else, and it is a program finding that
   stands in the falsifier evaluation beside the marks.
2. **The under-replication rule (G10(b)).**  A case with fewer than
   ``standard.GUARD_PARAMETERS["min_resolved_replicates_per_case"]`` resolved
   replicates yields **no residue at all** for the comparisons it is on.  It is
   reported as *absent data*, never as an absence of difference.
3. **The within-ORIGINAL baseline (§8a "order of reading", G8, G9).**  The kind
   set the ORIGINAL replicates already exhibit among themselves, per register,
   written once through :func:`minireason.loop.custody.write_new` behind
   :func:`minireason.loop.custody.fenced` and sealed by the sha256 of the file
   it wrote.  Nothing downstream is offered until that seal exists; revising the
   baseline changes a hash every later call record already carries.
4. **The program marks (G10(c) and G10(d)).**  Register **T** (both difference
   kinds) and register **D** (both difference kinds) are computed from the FCL
   parse wherever it succeeds; register **E** is prefix-resolved and a bare id
   token shared with the account document forces ``unresolved``; a program
   ``differs`` whose difference kind is already in the baseline's kind set for
   that register is written ``same`` by the program (G9), with the forcing
   replicate pair recorded.
5. **The residue.**  Exactly the rows the program could not decide, each naming
   the register, the difference kinds left open, and the replicate rows that
   defeated it.  That list — and only that list — is what W4-MARKER trials.

Design section implemented
--------------------------
W2-MARKPREP of *The automated end-to-end harness loop — FINAL design of record*:
§2.4 G8 (baseline seal), G9 (replicate baseline at kind grain), G10(a)-(d)
(program pre-empt), and the four registers of
``experiments/diagnostics/C001-contrast-triple/PLAN.md`` §8a as
:mod:`minireason.loop.standard` mirrors them
(:data:`~minireason.loop.standard.PLAN_8A_REGISTERS`,
:data:`~minireason.loop.standard.DIFFERENCE_KINDS`,
:data:`~minireason.loop.standard.FALSIFIER_MAP`).

What this is NOT
----------------
It calls no provider, opens no socket, mints no warrant, registers nothing in
the graph and renders no pack.  It never combines two registers, never sums or
ranks a mark, and exposes no count as a verdict: the one count it reads —
``min_resolved_replicates_per_case`` — is the pre-registered *grounded default*
that turns absent data into ``unresolved``, and it can only ever withhold a
reading, never produce one.  It repairs nothing: a delivered envelope that is
not strict JSON is a row the program could not read, named in the residue, and
never a row this module patched into readability.

Deviations from the wave-plan interface, and why
------------------------------------------------
* **The six named callables are all here with the wave plan's spelling; the
  module publishes more than six names.**  ``program_marks(cell)`` needs a
  ``cell``, so :func:`load_occurrence` / :class:`Occurrence` / :class:`Cell` /
  :class:`Replicate` and :func:`cell_from_contrast_leg` are published beside
  them, together with :func:`build_baseline`, :func:`read_baseline`,
  :func:`verify_baseline`, :func:`pairwise_surface` and :func:`resolve_pair` —
  the last two are the BUILD brief's pairwise surface, which the plan entry's
  six names do not spell.
* **``W1-SURFACE`` is a fourth dependency.**  The plan entry lists
  ``W0-CONTRACTS``, ``W0-STANDARD``, ``W0-CUSTODY``; the pairwise surface is
  built out of :class:`minireason.loop.surface.Surface` and
  :class:`~minireason.loop.surface.Span` and resolved with
  :func:`~minireason.loop.surface.resolve_unique` and
  :func:`~minireason.loop.surface.within_declared_span`, which is strictly
  earlier (wave 1) and is the one way not to own a second resolver.
* **The pairwise surface is constructed, not built through
  ``surface.build_surface``.**  ``build_surface`` derives every span's
  ``occurrence_path`` from a :class:`minireason.graph_import_h005.Coordinate`,
  whose layout is ``artifacts/<problem>/<arm>/cycle<NN>/<node>.json``; a C001
  replicate lives at ``artifacts/<endpoint>/<arm>/<case>/rep<N>.json`` and two
  of the six published endpoint slugs carry a ``.``, which
  ``graph_import_h005.safe_component`` refuses outright.  Passing a sanitised
  slug would publish a citation path no file is at.  The two :class:`Span`
  objects are therefore constructed directly — the dataclass is public and
  frozen, surface.py is not edited, and ``resolve_unique`` /
  ``within_declared_span`` read them unchanged.  ``file_start``/``file_end`` are
  code-point offsets into the ``commitments`` field of the named artifact, so
  ``json.load(occurrence / path)["commitments"][file_start:file_end] == region``
  holds, exactly as W1-SURFACE's S1 asks.
* **``ref_field`` / ``ref_verbatim`` / ``ref_grain`` on a pairwise surface carry
  the comparison, not a cross-document reference.**  A C001 pairwise surface is
  not a use-relation row and has no ref: ``ref_field`` is ``commitments`` (the
  field both sides are read out of), ``ref_grain`` is ``artifact`` (each side is
  a whole field, not one record), and ``ref_verbatim`` is the comparison label.
  They are descriptive slots on :class:`~minireason.loop.surface.Surface`, and
  this is what this module puts in them.
* **The baseline records what it could not read, not silence.**  Registers E and
  G are not program-read at kind grain (see below), so a baseline claiming
  ``{"E": [], "G": []}`` would assert that no E or G difference appears inside
  ORIGINAL — which the program never looked for.  :class:`Baseline` carries
  ``kinds`` **and** ``undecided_kinds`` per register, and the second is not
  empty on any real cell.
* **E and G are deliberately partial.**  §2.4 G10 gives the program registers T
  and D ("where the parse succeeds the mark is program-computed and no judge is
  called at all") and gives E only *prefix resolution and bare-token forcing*.
  This module does exactly that: E is decided only when a shared bare id token
  forces it ``unresolved``, because §8a admits engagement "by prefix-qualified
  reference **or by quotation of that record's own text**", and quotation is not
  a formal field.  G (``grounds_source``) is prose in every case and is never
  program-decided.  Both are named in the residue with their reason, so nothing
  is silently marked ``same`` on a register the program did not read.
* **``disposition_value`` and ``disposition_carrier_field`` are keyed by
  criticism.**  §8a: "``differs`` iff the disposition attached to **the same
  criticism** changes".  The program compares only objection records engaged on
  both sides; where the two sides engage no criticism in common there is no
  "same criticism" to read a change on, and the row goes to the residue rather
  than being called ``same``.
* **A case-level read is the union over its resolved, readable replicates** —
  literally §8a's "the set of values in ``target`` arrays" for that case.  The
  baseline is at replicate-pair grain inside ORIGINAL, which is §8a's own
  "at least one pair of replicates inside ORIGINAL".
* **New codes are raised through module constants, never as string literals in
  a constructor position** (the wave brief's rule).
  ``tests/loop/test_types.py``'s ``TOKEN_ARGUMENT`` scan reads a literal at
  argument 0; for this module the integrator should fold :data:`NEW_CODES` in by
  key rather than by source scan.

Reuse
-----
:data:`minireason.loop.standard.GUARD_PARAMETERS` is the only source of the
minimum-replicate rule; :data:`~minireason.loop.standard.DIFFERENCE_KINDS`,
:data:`~minireason.loop.standard.REGISTER_IDS`,
:data:`~minireason.loop.standard.MARKS` and
:data:`~minireason.loop.standard.FALSIFIER_MAP` are imported, never retyped.
:func:`minireason.loop.contracts.difference_kinds_for` is the per-register closed
kind set every mark is checked against (W0's O11: a marker call always knows its
register, and so does every row this module hands it).
:func:`minireason.loop.contracts.assert_no_scoring_keys` is G12, run over every
record this module emits.  :func:`minireason.loop.types.block_code` spells the
G9 downgrade's reason so it cannot drift from the ceiling's.
"""
from __future__ import annotations

import itertools
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from minireason.loop import custody
from minireason.loop import standard
from minireason.loop import surface as surface_module
from minireason.loop.contracts import assert_no_scoring_keys, difference_kinds_for
from minireason.loop.surface import (
    Offset,
    Span,
    Surface,
    resolve_unique,
    within_declared_span,
)
from minireason.loop.types import LoopError, block_code

__all__ = [
    "MARKPREP_SCHEMA",
    "BASELINE_SCHEMA",
    "PROGRAM_MARKS_SCHEMA",
    "RESIDUE_SCHEMA",
    "DEFEATER_SCHEMA",
    "PAIRWISE_SCHEMA",
    "BASELINE_FILENAME",
    "CASES",
    "BASELINE_CASE",
    "COMPARISONS",
    "COMPARISON_LABELS",
    "ARMS",
    "FCL_ARM",
    "PROSE_ARM",
    "REF_FIELDS",
    "REF_FORMS",
    "BARE_FORM",
    "UNRECOGNISED_FORM",
    "SOURCE_DOCUMENTS",
    "SOURCE_BARE",
    "SOURCE_UNRECOGNISED",
    "DISPOSITION_TOKENS",
    "DISPOSITION_CARRIER_FIELDS",
    "PROGRAM_KINDS",
    "KEYED_KINDS",
    "NOT_PROGRAM_READ",
    "PARSE_OK",
    "PARSE_FAILED",
    "PARSE_NOT_FCL",
    "PARSE_ENVELOPE_NOT_AUTHORED",
    "RESIDUE_REASONS",
    "MIN_RESOLVED_REPLICATES",
    "BASELINE_FORCED_SAME_BLOCK",
    "SIDE_LEFT",
    "SIDE_RIGHT",
    "NEW_CODES",
    "MarkprepError",
    "BaselineNotFirst",
    "BaselineSealBroken",
    "Reference",
    "FclRead",
    "Replicate",
    "Cell",
    "Occurrence",
    "BaselinePair",
    "Baseline",
    "ResidueRow",
    "PairQuotes",
    "load_occurrence",
    "cell_from_contrast_leg",
    "byte_identity_defeater",
    "under_replicated",
    "build_baseline",
    "baseline_kinds",
    "write_baseline",
    "read_baseline",
    "verify_baseline",
    "program_marks",
    "residue",
    "pairwise_surface",
    "resolve_pair",
]


# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

MARKPREP_SCHEMA = "minireason.loop.markprep.v1"
BASELINE_SCHEMA = "minireason.loop.markprep.baseline.v1"
PROGRAM_MARKS_SCHEMA = "minireason.loop.markprep.program_marks.v1"
RESIDUE_SCHEMA = "minireason.loop.markprep.residue.v1"
DEFEATER_SCHEMA = "minireason.loop.markprep.byte_identity.v1"
PAIRWISE_SCHEMA = "minireason.loop.markprep.pairwise.v1"

#: The one file :func:`write_baseline` writes, under the directory it is given.
BASELINE_FILENAME = "baseline.json"

#: PLAN §4's four cases, upper-cased as §8a and the ceiling spell them.
BASELINE_CASE = "ORIGINAL"
CASES: tuple[str, ...] = (BASELINE_CASE, "RECODING", "CARRIER", "CONTROL")

#: The three cross-case comparisons §8a renders, as ``(left, right)`` pairs, in
#: the order :data:`minireason.loop.standard.FALSIFIER_MAP` carries them.
COMPARISONS: tuple[tuple[str, str], ...] = (
    (BASELINE_CASE, "CONTROL"),
    (BASELINE_CASE, "RECODING"),
    (BASELINE_CASE, "CARRIER"),
)

#: ``(left, right) -> "ORIGINAL vs CONTROL"``, the label ``comparison.json``'s
#: own ``root_register_marks`` grid uses.
COMPARISON_LABELS: Mapping[tuple[str, str], str] = {
    pair: f"{pair[0]} vs {pair[1]}" for pair in COMPARISONS
}

FCL_ARM = "fcl"
PROSE_ARM = "prose"
ARMS: tuple[str, ...] = (FCL_ARM, PROSE_ARM)

#: The FCL-1 record fields that carry a reference, per
#: ``src/minireason/data/fcl1.schema.json``.
REF_FIELDS: tuple[str, ...] = ("target", "depends", "mentions", "revises", "withdraws")

#: How a reference's prefix resolved.  The rule is ``material.json``'s own:
#: a declared artifact address, that address truncated to its first
#: ``truncation_chars``, or the source name; anything else resolves to no
#: document, and a reference with no ``#`` is not a cross-document reference.
BARE_FORM = "BARE"
UNRECOGNISED_FORM = "UNRECOGNISED_PREFIX"
REF_FORMS: tuple[str, ...] = (
    "FULL_ADDRESS",
    "TRUNCATED_ADDRESS",
    "SOURCE_NAME",
    UNRECOGNISED_FORM,
    BARE_FORM,
)

#: The three documents put in front of the responder.
SOURCE_DOCUMENTS: tuple[str, ...] = ("objection", "account", "rival")
#: The two non-document source labels a target value can carry.  ``bare`` says
#: the value named no document at all, which is a fact about the reference and
#: never a claim about which document it meant.
SOURCE_BARE = "bare"
SOURCE_UNRECOGNISED = "unrecognised-prefix"

#: The dispositions §8a names — "use, leave open, revise, reject, or withdraw" —
#: plus ``act``, which is the ``action`` field §8a lists among D's carriers.
DISPOSITION_TOKENS: tuple[str, ...] = (
    "use",
    "leave-open",
    "revise",
    "reject",
    "withdraw",
    "act",
)

#: The formal fields §8a says D is read off on the FCL arm.
DISPOSITION_CARRIER_FIELDS: tuple[str, ...] = (
    "type",
    "uptake",
    "revises",
    "withdraws",
    "action",
)

#: The four difference kinds this module computes.  Every other member of
#: :data:`minireason.loop.standard.ALL_DIFFERENCE_KINDS` is in
#: :data:`NOT_PROGRAM_READ` with the reason it is not.
PROGRAM_KINDS: tuple[str, ...] = (
    "target_set_membership",
    "target_prefix_source",
    "disposition_value",
    "disposition_carrier_field",
)

#: The two program kinds read "attached to the same criticism" (§8a's D), so
#: they compare only over objection records engaged on both sides.
KEYED_KINDS: tuple[str, ...] = ("disposition_value", "disposition_carrier_field")

#: Kind -> why the program does not read it.  Both E kinds and G's one kind.
NOT_PROGRAM_READ: Mapping[str, str] = {
    "record_engaged": (
        "PLAN 8a admits engagement by prefix-qualified reference OR by quotation "
        "of the record's own text; quotation is not a formal field, so the "
        "program resolves prefixes and leaves the mark to the marker"
    ),
    "engagement_form": (
        "the form of engagement includes quotation, which no FCL field carries; "
        "the program publishes the prefix forms it resolved and marks nothing"
    ),
    "grounds_source": (
        "PLAN 8a reads G off whether the grounds cited are the objection's, the "
        "account's, the rival's or none, which is prose in every arm"
    ),
}

PARSE_OK = "OK"
PARSE_FAILED = "FAILED"
PARSE_NOT_FCL = "NOT_FCL"
PARSE_ENVELOPE_NOT_AUTHORED = "ENVELOPE_NOT_AUTHORED"

#: Why a row is in the residue.  One of these is on every residue row.
RESIDUE_REASONS: Mapping[str, str] = {
    "NOT_PROGRAM_READ": "the register's difference kinds are not program-readable at all",
    "REPLICATES_UNREADABLE": (
        "fewer than the minimum number of resolved replicates on one side could "
        "be read as an FCL document, so no case-level value exists to compare"
    ),
    "NO_SHARED_CRITICISM": (
        "the two sides engage no objection record in common, so there is no "
        "'same criticism' whose disposition could have changed"
    ),
    "BASELINE_UNREADABLE": (
        "the sealed baseline could read fewer than the minimum ORIGINAL "
        "replicates, so no program 'differs' is admissible against it"
    ),
}

#: The pre-registered grounded default, read from the standard and never from a
#: local literal.  It is a floor on *data*, never a score.
MIN_RESOLVED_REPLICATES: int = int(
    standard.GUARD_PARAMETERS["min_resolved_replicates_per_case"]
)

#: The reason a program ``differs`` is written ``same`` at kind grain (G9).  It
#: is one of the ceiling's nine named block reasons.
BASELINE_FORCED_SAME_BLOCK = block_code("baseline-forced-same")

#: The two sides of a pairwise surface, in W1-SURFACE's own vocabulary.
SIDE_LEFT = surface_module.SIDE_REFERRING_RECORD
SIDE_RIGHT = surface_module.SIDE_TARGET_RECORD

#: Codes this module raises that ``types.FAILURE_CODES`` does not yet carry.
#: The wave integrator folds them in; nothing here edits or narrows the table.
NEW_CODES: Mapping[str, str] = {
    "MARKPREP_INPUT_MALFORMED": (
        "the comparison table, the material or the contrast leg is not shaped "
        "like one, so no cell could be built from it"
    ),
    "COMPARISON_SCHEMA_UNKNOWN": (
        "comparison.json declares a schema this pre-pass does not read, and "
        "guessing at a successor layout would be a silent reinterpretation"
    ),
    "CELL_NOT_IN_OCCURRENCE": (
        "no comparison table in the occurrence carries that endpoint and arm"
    ),
    "REPLICATE_BYTES_DISAGREE": (
        "the juxtaposition bytes of a replicate do not hash to the sha256 the "
        "comparison table published for it, so the two records are not one row"
    ),
    "BASELINE_RESEALED": (
        "a second, different baseline seal was offered for a cell that already "
        "carries one; PLAN 8a writes the baseline first and never revises it"
    ),
    "BASELINE_SEAL_BROKEN": (
        "the sealed baseline file no longer hashes to the sha256 it was sealed "
        "with, so every call record carrying that sha is describing other bytes"
    ),
    "REGISTER_UNKNOWN": (
        "a register outside standard.REGISTER_IDS was asked for, and the four "
        "are closed by the frozen PLAN 8a mirror"
    ),
    "REPLICATE_UNKNOWN": (
        "a replicate key names no replicate of this cell, so no side of a "
        "pairwise surface could be addressed"
    ),
    "REPLICATE_NOT_READABLE": (
        "a pairwise surface was asked for over a replicate whose delivered "
        "bytes the program could not read, which would put framing in the "
        "material a quote is resolved against"
    ),
}

#: ``BASELINE_NOT_FIRST`` is **not** a new code: wave 0 already carries it in
#: ``types.FAILURE_CODES`` for W2-PACKS' ``BaselineNotFirst``, and G8 is one
#: refusal with one name whether the pack or the residue trips it.
BASELINE_NOT_FIRST = "BASELINE_NOT_FIRST"

MARKPREP_INPUT_MALFORMED = "MARKPREP_INPUT_MALFORMED"
COMPARISON_SCHEMA_UNKNOWN = "COMPARISON_SCHEMA_UNKNOWN"
CELL_NOT_IN_OCCURRENCE = "CELL_NOT_IN_OCCURRENCE"
REPLICATE_BYTES_DISAGREE = "REPLICATE_BYTES_DISAGREE"
BASELINE_RESEALED = "BASELINE_RESEALED"
BASELINE_SEAL_BROKEN = "BASELINE_SEAL_BROKEN"
REGISTER_UNKNOWN = "REGISTER_UNKNOWN"
REPLICATE_UNKNOWN = "REPLICATE_UNKNOWN"
REPLICATE_NOT_READABLE = "REPLICATE_NOT_READABLE"

#: The comparison-table schema this module reads.
COMPARISON_SCHEMA = "minireason.c001.comparison.v1"
#: The contrast-leg schema :func:`cell_from_contrast_leg` reads.
CONTRAST_LEG_SCHEMA = "minireason.loop.synthetic.v1.contrast"


class MarkprepError(LoopError, ValueError):
    """A C001 pre-pass input, or an ordering, the program refuses.

    ``(code, detail="")``, the argument order every wave-0 exception takes.  It
    is a :class:`~minireason.loop.types.LoopError`, so ``except LoopError``
    catches it, and it keeps ``ValueError``.  Every code it carries is a key of
    :data:`NEW_CODES`, and every raise names a module constant.
    """


class BaselineNotFirst(MarkprepError):
    """Something downstream of the baseline was asked for before the seal (G8)."""


class BaselineSealBroken(MarkprepError):
    """The sealed baseline file no longer hashes to its seal."""


# --------------------------------------------------------------------------
# The FCL read
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Reference:
    """One reference value, and how its prefix resolved.

    ``document`` is ``None`` where the prefix named no declared document —
    either because there was no prefix (:data:`BARE_FORM`) or because the prefix
    matched no declared address or source name (:data:`UNRECOGNISED_FORM`).
    """

    value: str
    field: str
    document: str | None
    record_id: str
    form: str

    @property
    def source(self) -> str:
        """The source label a target value contributes to ``target_prefix_source``."""

        if self.document is not None:
            return self.document
        return SOURCE_BARE if self.form == BARE_FORM else SOURCE_UNRECOGNISED

    def as_dict(self) -> dict[str, Any]:
        return {
            "value": self.value,
            "field": self.field,
            "document": self.document,
            "record_id": self.record_id,
            "form": self.form,
            "source": self.source,
        }


def _resolve_ref(value: str, addresses: Mapping[str, Any]) -> tuple[str | None, str, str]:
    """Split one reference into ``(document, record_id, form)``.

    ``material.json``'s declared rule, restated: the prefix is matched against
    each declared artifact address, that address truncated to its first
    ``truncation_chars``, and the source name itself.  An unrecognised prefix
    resolves to no document; a reference with no ``#`` is not a cross-document
    reference and stays in the bare-token channel.
    """

    text = str(value)
    if "#" not in text:
        return None, text, BARE_FORM
    prefix, record_id = text.split("#", 1)
    try:
        cut = int(addresses.get("truncation_chars") or 16)
    except (TypeError, ValueError):
        cut = 16
    for name in SOURCE_DOCUMENTS:
        address = str(addresses.get(name) or "")
        if not address:
            continue
        if prefix == address:
            return name, record_id, "FULL_ADDRESS"
        if len(address) >= cut and prefix == address[:cut]:
            return name, record_id, "TRUNCATED_ADDRESS"
        if prefix == name:
            return name, record_id, "SOURCE_NAME"
    return None, record_id, UNRECOGNISED_FORM


def _bare_token_counts(text: str, tokens: Iterable[str]) -> dict[str, int]:
    """Genuinely unqualified occurrences of each token in ``text``.

    A match preceded by ``#`` or ``.`` belongs to a structured reference and is
    already in the prefix-resolved channel; counting it here too would make two
    channels PLAN §7 keeps separate overlap by construction.
    """

    out: dict[str, int] = {}
    for token in tokens:
        pattern = r"(?<![A-Za-z0-9_#.])" + re.escape(str(token)) + r"(?![A-Za-z0-9_])"
        count = len(re.findall(pattern, text))
        if count:
            out[str(token)] = count
    return out


@dataclass(frozen=True)
class FclRead:
    """What the program read off one replicate's ``commitments`` document.

    ``parse`` is :data:`PARSE_OK` only where the whole chain succeeded: the
    delivered envelope was strict JSON, it carried a ``commitments`` string, and
    that string parsed as a document with a ``records`` array.  Every other
    value names where the chain stopped, and is what the residue reports.
    """

    parse: str
    language: str | None = None
    record_ids: tuple[str, ...] = ()
    references: tuple[Reference, ...] = ()
    targets: frozenset[str] = frozenset()
    target_sources: frozenset[str] = frozenset()
    engaged_records: frozenset[str] = frozenset()
    engagement_forms: frozenset[str] = frozenset()
    dispositions: Mapping[str, frozenset[str]] = field(default_factory=dict)
    carriers: Mapping[str, frozenset[str]] = field(default_factory=dict)
    bare_shared_tokens: Mapping[str, int] = field(default_factory=dict)
    detail: str = ""

    @property
    def readable(self) -> bool:
        return self.parse == PARSE_OK

    def as_dict(self) -> dict[str, Any]:
        return {
            "parse": self.parse,
            "language": self.language,
            "record_ids": list(self.record_ids),
            "targets": sorted(self.targets),
            "target_sources": sorted(self.target_sources),
            "engaged_records": sorted(self.engaged_records),
            "engagement_forms": sorted(self.engagement_forms),
            "dispositions": {k: sorted(v) for k, v in sorted(self.dispositions.items())},
            "carriers": {k: sorted(v) for k, v in sorted(self.carriers.items())},
            "bare_shared_tokens": dict(sorted(self.bare_shared_tokens.items())),
            "detail": self.detail,
        }


def _read_fcl(
    commitments: str,
    *,
    addresses: Mapping[str, Any],
    objection_ids: frozenset[str],
    shared_tokens: frozenset[str],
) -> FclRead:
    """The program's read of one FCL-1 commitments document.  Never repairs."""

    try:
        doc = json.loads(commitments)
    except (TypeError, ValueError) as exc:
        return FclRead(parse=PARSE_FAILED, detail=str(exc)[:120])
    if not isinstance(doc, dict) or not isinstance(doc.get("records"), list):
        return FclRead(parse=PARSE_NOT_FCL, detail="no records array")

    records = [r for r in doc["records"] if isinstance(r, dict)]
    uptake = {str(v) for v in doc.get("uptake") or []}

    references: list[Reference] = []
    targets: set[str] = set()
    target_sources: set[str] = set()
    engaged: set[str] = set()
    forms: set[str] = set()
    dispositions: dict[str, set[str]] = {}
    carriers: dict[str, set[str]] = {}

    for record in records:
        criticisms: set[str] = set()
        for name in REF_FIELDS:
            values = record.get(name)
            if not isinstance(values, (list, tuple)):
                continue
            for raw in values:
                value = str(raw)
                document, record_id, form = _resolve_ref(value, addresses)
                reference = Reference(value, name, document, record_id, form)
                references.append(reference)
                if name == "target":
                    targets.add(value)
                    target_sources.add(reference.source)
                if document == "objection" and record_id in objection_ids:
                    engaged.add(record_id)
                    forms.add(form)
                    criticisms.add(record_id)
        tokens, fields = _dispositions_of(record, uptake)
        for criticism in criticisms:
            dispositions.setdefault(criticism, set()).update(tokens)
            carriers.setdefault(criticism, set()).update(fields)

    return FclRead(
        parse=PARSE_OK,
        language=doc.get("language") if isinstance(doc.get("language"), str) else None,
        record_ids=tuple(str(r.get("id")) for r in records),
        references=tuple(references),
        targets=frozenset(targets),
        target_sources=frozenset(target_sources),
        engaged_records=frozenset(engaged),
        engagement_forms=frozenset(forms),
        dispositions={k: frozenset(v) for k, v in dispositions.items()},
        carriers={k: frozenset(v) for k, v in carriers.items()},
        bare_shared_tokens=_bare_token_counts(commitments, sorted(shared_tokens)),
    )


def _dispositions_of(
    record: Mapping[str, Any], uptake: set[str]
) -> tuple[frozenset[str], frozenset[str]]:
    """§8a's D, read off ``type``, ``uptake``, ``revises``, ``withdraws``, ``action``."""

    tokens: set[str] = set()
    fields: set[str] = set()
    if str(record.get("id")) in uptake:
        tokens.add("use")
        fields.add("uptake")
    if record.get("revises"):
        tokens.add("revise")
        fields.add("revises")
    if record.get("withdraws"):
        tokens.add("withdraw")
        fields.add("withdraws")
    if str(record.get("type")) == "objection":
        tokens.add("reject")
        fields.add("type")
    action = record.get("action")
    if isinstance(action, str) and action.strip():
        tokens.add("act")
        fields.add("action")
    if not tokens:
        tokens.add("leave-open")
    return frozenset(tokens), frozenset(fields)


def _merge_reads(reads: Sequence[FclRead]) -> FclRead:
    """The case-level read: the union over that case's readable replicates."""

    targets: set[str] = set()
    sources: set[str] = set()
    engaged: set[str] = set()
    forms: set[str] = set()
    dispositions: dict[str, set[str]] = {}
    carriers: dict[str, set[str]] = {}
    bare: dict[str, int] = {}
    for read in reads:
        targets |= set(read.targets)
        sources |= set(read.target_sources)
        engaged |= set(read.engaged_records)
        forms |= set(read.engagement_forms)
        for key, values in read.dispositions.items():
            dispositions.setdefault(key, set()).update(values)
        for key, values in read.carriers.items():
            carriers.setdefault(key, set()).update(values)
        for token, count in read.bare_shared_tokens.items():
            bare[token] = bare.get(token, 0) + count
    return FclRead(
        parse=PARSE_OK if reads else PARSE_FAILED,
        record_ids=tuple(rid for read in reads for rid in read.record_ids),
        targets=frozenset(targets),
        target_sources=frozenset(sources),
        engaged_records=frozenset(engaged),
        engagement_forms=frozenset(forms),
        dispositions={k: frozenset(v) for k, v in dispositions.items()},
        carriers={k: frozenset(v) for k, v in carriers.items()},
        bare_shared_tokens=bare,
    )


def _kind_difference(
    left: FclRead, right: FclRead, kind: str
) -> tuple[bool, bool, dict[str, Any]]:
    """``(decided, differs, evidence)`` for one difference kind over two reads."""

    if kind == "target_set_membership":
        return (
            True,
            left.targets != right.targets,
            {"left": sorted(left.targets), "right": sorted(right.targets)},
        )
    if kind == "target_prefix_source":
        return (
            True,
            left.target_sources != right.target_sources,
            {"left": sorted(left.target_sources), "right": sorted(right.target_sources)},
        )
    if kind in KEYED_KINDS:
        attribute = "dispositions" if kind == "disposition_value" else "carriers"
        left_map: Mapping[str, frozenset[str]] = getattr(left, attribute)
        right_map: Mapping[str, frozenset[str]] = getattr(right, attribute)
        shared = sorted(set(left_map) & set(right_map))
        evidence: dict[str, Any] = {
            "shared_criticisms": shared,
            "left": {k: sorted(left_map[k]) for k in shared},
            "right": {k: sorted(right_map[k]) for k in shared},
        }
        if not shared:
            return False, False, evidence
        differs = any(left_map[k] != right_map[k] for k in shared)
        evidence["criticisms_that_changed"] = [
            k for k in shared if left_map[k] != right_map[k]
        ]
        return True, differs, evidence
    return False, False, {"reason": NOT_PROGRAM_READ.get(kind, "not program-read")}


def _register_of(kind: str) -> str:
    for register in standard.REGISTER_IDS:
        if kind in difference_kinds_for(register):
            return register
    raise MarkprepError(REGISTER_UNKNOWN, kind)


# --------------------------------------------------------------------------
# Replicates, cells, occurrences
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Replicate:
    """One delivered replicate of one case of one cell.

    ``resolved`` is the occurrence's own ``comparable`` flag: a FAILED or
    PARTIAL delivery is not compared against another case (FW5:634).
    ``read`` is what the *program* could make of the bytes, which is a strictly
    later question and is ``PARSE_ENVELOPE_NOT_AUTHORED`` where the delivered
    envelope was not strict JSON.
    """

    case: str
    replicate: int
    resolved: bool
    read: FclRead
    commitments: str | None
    commitments_sha256: str | None
    artifact_path: str
    delivered_path: str | None
    delivery_status: str | None
    envelope_status: str | None
    unresolved_reason: str | None
    fence_stripped: bool = False
    envelope_repairs: tuple[str, ...] = ()
    strict_parse_would_succeed: bool | None = None

    @property
    def key(self) -> str:
        """``"ORIGINAL/rep3"`` — the row spelling the residue names."""

        return f"{self.case}/rep{self.replicate}"

    @property
    def readable(self) -> bool:
        """Resolved *and* read: the only replicates a program mark is built on."""

        return self.resolved and self.read.readable

    def as_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "case": self.case,
            "replicate": self.replicate,
            "resolved": self.resolved,
            "readable": self.readable,
            "parse": self.read.parse,
            "commitments_sha256": self.commitments_sha256,
            "artifact_path": self.artifact_path,
            "delivered_path": self.delivered_path,
            "delivery_status": self.delivery_status,
            "envelope_status": self.envelope_status,
            "unresolved_reason": self.unresolved_reason,
            "fence_stripped": self.fence_stripped,
            "envelope_repairs": list(self.envelope_repairs),
            "strict_parse_would_succeed": self.strict_parse_would_succeed,
        }


class Cell:
    """One ``(endpoint, arm)`` contrast cell, and its write-once baseline seal.

    The seal is the one piece of state a cell carries.  It is set exactly once,
    by :func:`write_baseline`, and everything G8 puts downstream of the baseline
    — :func:`program_marks`, :func:`residue`, and a cross-case
    :func:`pairwise_surface` — refuses until it is there.  Re-sealing with a
    different sha is :data:`BASELINE_RESEALED`: *the baseline note is written
    first and is not revised afterwards.*
    """

    def __init__(
        self,
        *,
        cell_id: str,
        endpoint: str,
        arm: str,
        replicates: Sequence[Replicate],
        source: str,
        plan_id: str | None = None,
        objection_ids: frozenset[str] = frozenset(),
        shared_tokens: frozenset[str] = frozenset(),
        occurrence_root: Path | None = None,
    ) -> None:
        self.cell_id = cell_id
        self.endpoint = endpoint
        self.arm = arm
        self.source = source
        self.plan_id = plan_id
        self.objection_ids = frozenset(objection_ids)
        self.shared_tokens = frozenset(shared_tokens)
        self.occurrence_root = occurrence_root
        self.replicates: tuple[Replicate, ...] = tuple(replicates)
        self._by_key = {r.key: r for r in self.replicates}
        self._baseline_sha: str | None = None

    # -- seal -------------------------------------------------------------

    @property
    def baseline_sha(self) -> str | None:
        """The sha256 of the sealed baseline file, or ``None`` before the seal."""

        return self._baseline_sha

    @property
    def sealed(self) -> bool:
        return self._baseline_sha is not None

    def seal(self, sha256: str) -> str:
        """Record the baseline seal, once.  A different second seal raises."""

        if not isinstance(sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", sha256):
            raise MarkprepError(MARKPREP_INPUT_MALFORMED, "a seal is a sha256 hex digest")
        if self._baseline_sha is not None and self._baseline_sha != sha256:
            raise MarkprepError(
                BASELINE_RESEALED, f"{self.cell_id}: {self._baseline_sha} -> {sha256}"
            )
        self._baseline_sha = sha256
        return sha256

    def require_seal(self, what: str) -> str:
        if self._baseline_sha is None:
            raise BaselineNotFirst(BASELINE_NOT_FIRST, f"{self.cell_id}: {what}")
        return self._baseline_sha

    # -- views ------------------------------------------------------------

    @property
    def cases(self) -> tuple[str, ...]:
        """The cases this cell actually carries, in :data:`CASES` order."""

        present = {r.case for r in self.replicates}
        return tuple(case for case in CASES if case in present)

    @property
    def comparisons(self) -> tuple[tuple[str, str], ...]:
        present = set(self.cases)
        return tuple(p for p in COMPARISONS if p[0] in present and p[1] in present)

    def of(self, case: str) -> tuple[Replicate, ...]:
        return tuple(r for r in self.replicates if r.case == case)

    def resolved(self, case: str) -> tuple[Replicate, ...]:
        return tuple(r for r in self.of(case) if r.resolved)

    def readable(self, case: str) -> tuple[Replicate, ...]:
        return tuple(r for r in self.of(case) if r.readable)

    def replicate(self, key: str) -> Replicate:
        try:
            return self._by_key[str(key)]
        except KeyError as exc:
            raise MarkprepError(REPLICATE_UNKNOWN, f"{self.cell_id}: {key}") from exc

    def as_dict(self) -> dict[str, Any]:
        record = {
            "schema": MARKPREP_SCHEMA,
            "cell": self.cell_id,
            "endpoint": self.endpoint,
            "arm": self.arm,
            "source": self.source,
            "plan_id": self.plan_id,
            "baseline_sha256": self.baseline_sha,
            "objection_record_ids": sorted(self.objection_ids),
            "shared_bare_tokens": sorted(self.shared_tokens),
            "replicates": [r.as_dict() for r in self.replicates],
        }
        assert_no_scoring_keys(record)
        return record

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"<Cell {self.cell_id} sealed={self.sealed}>"


_BLOCK_FENCE = "```"
_ESCAPED_FENCE = "`​``"
_CASE_LINE = re.compile(r"^## case: (\S+)$")
_REP_LINE = re.compile(r"^### rep(\d+) \((.+)\)$")
_OUTER_FENCE = re.compile(r"^```[A-Za-z0-9_-]*\n(.*)\n```$", re.S)


def _juxtaposition_blocks(text: str) -> dict[tuple[str, int], str]:
    """``(case, replicate) -> the raw delivered bytes`` of one juxtaposition file.

    The renderer escapes a delivered triple backtick by inserting U+200B after
    the first one, so the study's own fences stay unambiguous; this undoes
    exactly that and nothing else.  A test asserts the result is byte-identical
    to the occurrence's ``responses/.../repN.txt``.
    """

    lines = text.split("\n")
    blocks: dict[tuple[str, int], str] = {}
    case: str | None = None
    index = 0
    while index < len(lines):
        line = lines[index]
        match = _CASE_LINE.match(line)
        if match:
            case = match.group(1)
            index += 1
            continue
        match = _REP_LINE.match(line)
        if match and case is not None:
            replicate = int(match.group(1))
            index += 1
            while index < len(lines) and lines[index] != _BLOCK_FENCE:
                index += 1
            index += 1
            body: list[str] = []
            while index < len(lines) and lines[index] != _BLOCK_FENCE:
                body.append(lines[index])
                index += 1
            blocks[(case, replicate)] = "\n".join(body).replace(
                _ESCAPED_FENCE, _BLOCK_FENCE
            )
            continue
        index += 1
    return blocks


def _commitments_of(raw: str) -> tuple[str | None, bool, str]:
    """``(commitments, fence_stripped, parse)`` for one delivered blob.

    At most one outer code fence is removed, which is the one repair the study's
    own ``envelope_repairs`` records and the only one that does not change a
    byte of the artifact inside it.  Anything else that will not parse strictly
    is :data:`PARSE_ENVELOPE_NOT_AUTHORED` — a row the program could not read,
    never a row it patched.
    """

    text = raw.strip()
    fence_stripped = False
    match = _OUTER_FENCE.match(text)
    if match:
        text = match.group(1)
        fence_stripped = True
    try:
        envelope = json.loads(text)
    except (TypeError, ValueError):
        return None, fence_stripped, PARSE_ENVELOPE_NOT_AUTHORED
    if not isinstance(envelope, dict) or not isinstance(envelope.get("commitments"), str):
        return None, fence_stripped, PARSE_ENVELOPE_NOT_AUTHORED
    return envelope["commitments"], fence_stripped, PARSE_OK


class Occurrence:
    """A published C001 occurrence: its comparison table and its material."""

    def __init__(self, root: Path, comparison: Mapping[str, Any], material: Mapping[str, Any]):
        self.root = Path(root)
        self.comparison = comparison
        self.material = material

    @property
    def plan_id(self) -> str | None:
        value = self.comparison.get("plan_id")
        return str(value) if isinstance(value, str) else None

    @property
    def cell_keys(self) -> tuple[tuple[str, str], ...]:
        return tuple(
            (str(t["endpoint_slug"]), str(t["arm"]))
            for t in self.comparison["tables"]
            if isinstance(t, Mapping)
        )

    def _arm_block(self, arm: str) -> Mapping[str, Any]:
        arms = self.material.get("arms")
        if not isinstance(arms, Mapping) or not isinstance(arms.get(arm), Mapping):
            raise MarkprepError(MARKPREP_INPUT_MALFORMED, f"material has no arm {arm!r}")
        return arms[arm]

    def cell(self, endpoint: str, arm: str) -> Cell:
        """The cell for one endpoint and arm, with every replicate read."""

        for table in self.comparison["tables"]:
            if str(table.get("endpoint_slug")) == endpoint and str(table.get("arm")) == arm:
                break
        else:
            raise MarkprepError(CELL_NOT_IN_OCCURRENCE, f"{endpoint}/{arm}")

        block = self._arm_block(arm)
        addresses = block.get("artifact_addresses") or {}
        by_document = block.get("record_ids_by_document") or {}
        objection_ids = frozenset(str(v) for v in (by_document.get("objection") or ()))
        account_ids = frozenset(str(v) for v in (by_document.get("account") or ()))
        shared = objection_ids & account_ids

        path = self.root / "juxtaposition" / f"{endpoint}__{arm}.md"
        blocks = _juxtaposition_blocks(path.read_text(encoding="utf-8"))

        replicates: list[Replicate] = []
        for lowered, rows in sorted(table["cases"].items()):
            case = str(lowered).upper()
            for row in rows:
                number = int(row["replicate"])
                raw = blocks.get((str(lowered), number))
                if raw is None:
                    raise MarkprepError(
                        MARKPREP_INPUT_MALFORMED,
                        f"{endpoint}/{arm}: {lowered}/rep{number} has no juxtaposition block",
                    )
                commitments, fence_stripped, envelope = _commitments_of(raw)
                repairs = tuple(str(v) for v in (row.get("envelope_repairs") or ()))
                published = row.get("commitments_sha256")
                if commitments is not None and isinstance(published, str):
                    observed = custody.sha256_bytes(commitments.encode("utf-8"))
                    if observed != published:
                        # An OPAQUE envelope is not an authored artifact: the
                        # study's own commitments string for it is not the one
                        # in the delivered bytes, and the program reads neither.
                        if str(row.get("envelope_status")) == "OPAQUE":
                            commitments, envelope = None, PARSE_ENVELOPE_NOT_AUTHORED
                        else:
                            raise MarkprepError(
                                REPLICATE_BYTES_DISAGREE,
                                f"{endpoint}/{arm}/{lowered}/rep{number}: "
                                f"{observed} != {published}",
                            )
                if commitments is None:
                    read = FclRead(
                        parse=envelope,
                        detail=(
                            "the delivered envelope is not strict JSON; the "
                            "occurrence declares the repairs "
                            f"{list(repairs)} and this pre-pass repairs nothing"
                        ),
                    )
                elif arm != FCL_ARM:
                    read = FclRead(
                        parse=PARSE_NOT_FCL,
                        detail="the prose arm carries no formal commitment document",
                        bare_shared_tokens=_bare_token_counts(commitments, sorted(shared)),
                    )
                else:
                    read = _read_fcl(
                        commitments,
                        addresses=addresses,
                        objection_ids=objection_ids,
                        shared_tokens=shared,
                    )
                replicates.append(
                    Replicate(
                        case=case,
                        replicate=number,
                        resolved=bool(row.get("comparable")),
                        read=read,
                        commitments=commitments,
                        commitments_sha256=published if isinstance(published, str) else None,
                        artifact_path=f"artifacts/{endpoint}/{arm}/{lowered}/rep{number}.json",
                        delivered_path=str(row["path"]) if row.get("path") else None,
                        delivery_status=row.get("delivery_status"),
                        envelope_status=row.get("envelope_status"),
                        unresolved_reason=row.get("unresolved_reason"),
                        fence_stripped=fence_stripped,
                        envelope_repairs=repairs,
                        strict_parse_would_succeed=(
                            None
                            if row.get("strict_parse_would_succeed") is None
                            else bool(row["strict_parse_would_succeed"])
                        ),
                    )
                )

        return Cell(
            cell_id=f"{endpoint}/{arm}",
            endpoint=endpoint,
            arm=arm,
            replicates=replicates,
            source=f"C001 occurrence at {self.root.name}",
            plan_id=self.plan_id,
            objection_ids=objection_ids,
            shared_tokens=shared,
            occurrence_root=self.root,
        )

    def cells(self) -> tuple[Cell, ...]:
        return tuple(self.cell(endpoint, arm) for endpoint, arm in self.cell_keys)


def load_occurrence(root: str | Path, *, material: str | Path | None = None) -> Occurrence:
    """Read a published C001 occurrence's ``comparison.json`` and its material.

    ``material`` defaults to ``<root>/material.json`` and falls back to the
    study's own ``material.json`` one directory up, which is where an occurrence
    built from the shared material keeps it.  Nothing under ``root`` is written.
    """

    root_path = Path(root)
    comparison = json.loads((root_path / "comparison.json").read_text(encoding="utf-8"))
    if not isinstance(comparison, Mapping) or not isinstance(comparison.get("tables"), list):
        raise MarkprepError(MARKPREP_INPUT_MALFORMED, f"{root_path}/comparison.json")
    declared = str(comparison.get("schema"))
    if declared != COMPARISON_SCHEMA:
        raise MarkprepError(COMPARISON_SCHEMA_UNKNOWN, declared)
    if material is not None:
        material_path = Path(material)
    elif (root_path / "material.json").exists():
        material_path = root_path / "material.json"
    else:
        material_path = root_path.parent / "material.json"
    body = json.loads(material_path.read_text(encoding="utf-8"))
    if not isinstance(body, Mapping):
        raise MarkprepError(MARKPREP_INPUT_MALFORMED, str(material_path))
    return Occurrence(root_path, comparison, body)


def cell_from_contrast_leg(
    leg: Mapping[str, Any],
    case: str,
    *,
    addresses: Mapping[str, Any] | None = None,
    objection_ids: Iterable[str] = (),
    shared_tokens: Iterable[str] = (),
    prefix: str = "synthetic",
) -> Cell:
    """One :class:`Cell` over ``synthetic.contrast_leg()``'s ORIGINAL/CONTROL pair.

    The synthetic leg carries two cases, not four, so the cell has exactly one
    comparison — ``ORIGINAL vs CONTROL``, the one D1 is read on.  Its artifact
    paths are the fixture's own address space (``<prefix>/<case>/...``) and the
    cell says so in ``source``: nothing here claims to be a published
    occurrence.
    """

    if not isinstance(leg, Mapping) or not isinstance(leg.get("cases"), Mapping):
        raise MarkprepError(MARKPREP_INPUT_MALFORMED, "a contrast leg carries cases")
    declared = str(leg.get("schema"))
    if declared != CONTRAST_LEG_SCHEMA:
        raise MarkprepError(COMPARISON_SCHEMA_UNKNOWN, declared)
    entry = leg["cases"].get(case)
    if not isinstance(entry, Mapping) or not isinstance(entry.get("replicates"), Mapping):
        raise MarkprepError(MARKPREP_INPUT_MALFORMED, f"contrast leg has no case {case!r}")

    ids = frozenset(str(v) for v in objection_ids)
    shared = frozenset(str(v) for v in shared_tokens)
    resolved_addresses = dict(addresses or {})

    replicates: list[Replicate] = []
    for index, (name, sides) in enumerate(sorted(entry["replicates"].items()), start=1):
        for side in (BASELINE_CASE, "CONTROL"):
            commitments = sides.get(side)
            if not isinstance(commitments, str):
                raise MarkprepError(
                    MARKPREP_INPUT_MALFORMED, f"{case}/{name}/{side} is not a string"
                )
            replicates.append(
                Replicate(
                    case=side,
                    replicate=index,
                    resolved=True,
                    read=_read_fcl(
                        commitments,
                        addresses=resolved_addresses,
                        objection_ids=ids,
                        shared_tokens=shared,
                    ),
                    commitments=commitments,
                    commitments_sha256=custody.sha256_bytes(commitments.encode("utf-8")),
                    artifact_path=f"{prefix}/{case}/{side.lower()}/{name}.json",
                    delivered_path=None,
                    delivery_status="COMPLETE",
                    envelope_status="AUTHORED",
                    unresolved_reason=None,
                )
            )

    return Cell(
        cell_id=f"contrast/{case}",
        endpoint="contrast",
        arm=FCL_ARM,
        replicates=replicates,
        source=f"synthetic.contrast_leg {case}",
        plan_id=None,
        objection_ids=ids,
        shared_tokens=shared,
    )


# --------------------------------------------------------------------------
# G10(a) — the byte-identity defeater
# --------------------------------------------------------------------------


def byte_identity_defeater(cell: Cell) -> dict[str, Any]:
    """PLAN §8's mechanical defeater, computed before anything else.

    *If, in a cell, every resolved ORIGINAL replicate's ``commitments`` is
    byte-identical to some resolved CONTROL replicate's, D1 is not exhibited in
    that cell and root records it so.*  The finding is a fact about bytes, needs
    no baseline and no call, and stands in the falsifier evaluation beside the
    marks — it is never itself a mark.

    A cell with no resolved ORIGINAL or no resolved CONTROL replicate exhibits
    nothing either way: ``d1_not_exhibited`` is ``False`` and
    ``computable`` is ``False``, because absent data is not a defeater.
    """

    originals = cell.resolved(BASELINE_CASE)
    controls = cell.resolved("CONTROL")
    control_shas = {r.commitments_sha256: r for r in controls if r.commitments_sha256}

    pairs: list[dict[str, str]] = []
    unmatched: list[str] = []
    for original in originals:
        match = control_shas.get(original.commitments_sha256) if original.commitments_sha256 else None
        if match is None:
            unmatched.append(original.key)
        else:
            pairs.append(
                {
                    "original": original.key,
                    "control": match.key,
                    "commitments_sha256": str(original.commitments_sha256),
                }
            )

    computable = bool(originals) and bool(controls)
    record = {
        "schema": DEFEATER_SCHEMA,
        "cell": cell.cell_id,
        "comparison": COMPARISON_LABELS[(BASELINE_CASE, "CONTROL")],
        "falsifier": "D1",
        "rule": (
            "every resolved ORIGINAL replicate's commitments is byte-identical to "
            "some resolved CONTROL replicate's (PLAN 8, mechanical defeaters)"
        ),
        "computable": computable,
        "d1_not_exhibited": computable and not unmatched,
        "computed_before_any_call": True,
        "resolved_original": [r.key for r in originals],
        "resolved_control": [r.key for r in controls],
        "identical_pairs": pairs,
        "original_without_identical_control": unmatched,
        "carrying_registers": list(standard.FALSIFIER_MAP["D1"].carrying_registers),
        "excluded_registers": list(standard.FALSIFIER_MAP["D1"].excluded_registers),
    }
    assert_no_scoring_keys(record)
    return record


# --------------------------------------------------------------------------
# G10(b) — under-replication
# --------------------------------------------------------------------------


def under_replicated(cell: Cell) -> set[str]:
    """The cases with fewer than the standard's minimum resolved replicates.

    The minimum is ``standard.GUARD_PARAMETERS["min_resolved_replicates_per_case"]``
    and is applied as the pre-registered grounded default: a case in this set
    yields **no residue**, no marker call and no mark, and is reported as absent
    data — *never* as an absence of difference.  The count is a floor on data
    and is never published as a verdict.
    """

    return {
        case
        for case in cell.cases
        if len(cell.resolved(case)) < MIN_RESOLVED_REPLICATES
    }


# --------------------------------------------------------------------------
# G8 / G9 — the within-ORIGINAL baseline
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class BaselinePair:
    """One pair of ORIGINAL replicates and the difference kinds between them."""

    left: str
    right: str
    kinds: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {"left": self.left, "right": self.right, "kinds": list(self.kinds)}


@dataclass(frozen=True)
class Baseline:
    """The within-ORIGINAL replicate spread, per register, at kind grain.

    ``kinds[register]`` is the set of difference kinds the ORIGINAL replicates
    already exhibit among themselves — G9's admissibility test for a later
    ``differs``.  ``undecided_kinds[register]`` is what the program could **not**
    read, and is never empty for E or G: a baseline that reported ``[]`` there
    would be claiming an absence it never looked for.
    """

    schema: str
    cell: str
    case: str
    replicates: tuple[str, ...]
    readable: tuple[str, ...]
    kinds: Mapping[str, tuple[str, ...]]
    undecided_kinds: Mapping[str, tuple[str, ...]]
    pairs: tuple[BaselinePair, ...]
    min_resolved_replicates: int
    sufficient: bool
    note: str

    def exhibits(self, register: str, kind: str) -> bool:
        """True where G9 forces a ``differs`` on ``kind`` to ``same``."""

        return kind in self.kinds.get(register, ())

    def as_dict(self) -> dict[str, Any]:
        record = {
            "schema": self.schema,
            "cell": self.cell,
            "case": self.case,
            "replicates": list(self.replicates),
            "readable": list(self.readable),
            "kinds": {k: list(v) for k, v in sorted(self.kinds.items())},
            "undecided_kinds": {
                k: list(v) for k, v in sorted(self.undecided_kinds.items())
            },
            "pairs": [p.as_dict() for p in self.pairs],
            "min_resolved_replicates": self.min_resolved_replicates,
            "sufficient": self.sufficient,
            "note": self.note,
        }
        assert_no_scoring_keys(record)
        return record


_BASELINE_NOTE = (
    "The within-ORIGINAL spread on all four registers, written before any other "
    "case's juxtaposition was opened for this cell and not revised afterwards "
    "(PLAN 8a, order of reading). A register is marked differs for a case pair "
    "only if the difference is one that does not already appear between a pair "
    "of replicates inside ORIGINAL."
)


def build_baseline(
    cell: Cell, replicates: Sequence[Replicate | str] | None = None
) -> Baseline:
    """The baseline record, computed and not yet written.

    ``replicates`` defaults to every resolved ORIGINAL replicate of the cell; a
    caller may name a subset, which must be ORIGINAL replicates of this cell.
    """

    chosen = _baseline_replicates(cell, replicates)
    readable = [r for r in chosen if r.readable]

    pairs: list[BaselinePair] = []
    exhibited: dict[str, set[str]] = {r: set() for r in standard.REGISTER_IDS}
    for left, right in itertools.combinations(readable, 2):
        kinds: list[str] = []
        for kind in PROGRAM_KINDS:
            decided, differs, _ = _kind_difference(left.read, right.read, kind)
            if decided and differs:
                kinds.append(kind)
                exhibited[_register_of(kind)].add(kind)
        pairs.append(BaselinePair(left.key, right.key, tuple(kinds)))

    sufficient = len(readable) >= MIN_RESOLVED_REPLICATES
    undecided: dict[str, tuple[str, ...]] = {}
    kinds_by_register: dict[str, tuple[str, ...]] = {}
    for register in standard.REGISTER_IDS:
        register_kinds = difference_kinds_for(register)
        not_read = [k for k in register_kinds if k in NOT_PROGRAM_READ]
        if not sufficient:
            not_read = list(register_kinds)
        undecided[register] = tuple(not_read)
        kinds_by_register[register] = tuple(
            k for k in register_kinds if k in exhibited[register]
        )

    return Baseline(
        schema=BASELINE_SCHEMA,
        cell=cell.cell_id,
        case=BASELINE_CASE,
        replicates=tuple(r.key for r in chosen),
        readable=tuple(r.key for r in readable),
        kinds=kinds_by_register,
        undecided_kinds=undecided,
        pairs=tuple(pairs),
        min_resolved_replicates=MIN_RESOLVED_REPLICATES,
        sufficient=sufficient,
        note=_BASELINE_NOTE,
    )


def _baseline_replicates(
    cell: Cell, replicates: Sequence[Replicate | str] | None
) -> tuple[Replicate, ...]:
    if replicates is None:
        return cell.resolved(BASELINE_CASE)
    chosen: list[Replicate] = []
    for entry in replicates:
        row = entry if isinstance(entry, Replicate) else cell.replicate(entry)
        if row.case != BASELINE_CASE:
            raise MarkprepError(
                MARKPREP_INPUT_MALFORMED,
                f"the baseline is within {BASELINE_CASE}; {row.key} is not",
            )
        if row not in cell.replicates:
            raise MarkprepError(REPLICATE_UNKNOWN, f"{cell.cell_id}: {row.key}")
        chosen.append(row)
    return tuple(chosen)


def baseline_kinds(cell: Cell) -> dict[str, tuple[str, ...]]:
    """``register -> the difference kinds the ORIGINAL replicates exhibit``.

    This is G9's admissibility set and nothing else.  A register whose kinds the
    program cannot read carries an empty tuple *and* a non-empty
    ``undecided_kinds`` entry on :class:`Baseline`; read the baseline, not this
    mapping alone, before concluding that a register exhibits nothing.
    """

    return dict(build_baseline(cell).kinds)


def write_baseline(
    cell: Cell,
    replicates: Sequence[Replicate | str] | None,
    out_dir: str | Path,
) -> str:
    """Write the baseline once, under ``out_dir``, and seal the cell with its sha.

    The path is fenced to ``out_dir`` and the write is
    :func:`minireason.loop.custody.write_new`, so a second write — an edit after
    the seal — raises :class:`~minireason.loop.custody.WriteOnceViolation`.  The
    returned sha256 is the **file's**, which is what G8 pins into every later
    call record: revising the baseline changes a hash they already carry.
    """

    baseline = build_baseline(cell, replicates)
    path = custody.fenced(out_dir, BASELINE_FILENAME)
    custody.write_new(path, baseline.as_dict())
    return cell.seal(custody.sha256_path(path))


def read_baseline(out_dir: str | Path) -> Baseline:
    """Read back a written baseline.  Pure: nothing is sealed or written."""

    path = custody.fenced(out_dir, BASELINE_FILENAME)
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, Mapping) or raw.get("schema") != BASELINE_SCHEMA:
        raise MarkprepError(MARKPREP_INPUT_MALFORMED, str(path))
    return Baseline(
        schema=str(raw["schema"]),
        cell=str(raw["cell"]),
        case=str(raw["case"]),
        replicates=tuple(str(v) for v in raw["replicates"]),
        readable=tuple(str(v) for v in raw["readable"]),
        kinds={k: tuple(v) for k, v in raw["kinds"].items()},
        undecided_kinds={k: tuple(v) for k, v in raw["undecided_kinds"].items()},
        pairs=tuple(
            BaselinePair(str(p["left"]), str(p["right"]), tuple(p["kinds"]))
            for p in raw["pairs"]
        ),
        min_resolved_replicates=int(raw["min_resolved_replicates"]),
        sufficient=bool(raw["sufficient"]),
        note=str(raw["note"]),
    )


def verify_baseline(out_dir: str | Path, sha256: str) -> str:
    """Re-hash the sealed baseline file and refuse a changed one.

    This is the other half of the seal: :func:`write_baseline` makes an edit
    impossible through this module, and this makes an edit made *around* it —
    by hand, by another process — a named refusal rather than a silent drift.
    """

    path = custody.fenced(out_dir, BASELINE_FILENAME)
    observed = custody.sha256_path(path)
    if observed != sha256:
        raise BaselineSealBroken(
            BASELINE_SEAL_BROKEN, f"{path}: sealed {sha256}, now {observed}"
        )
    return observed


# --------------------------------------------------------------------------
# G10(c) and G10(d) — the program marks
# --------------------------------------------------------------------------


def _forced_unresolved_tokens(cell: Cell, case: str) -> dict[str, int]:
    """Bare id tokens shared with the account document, over a case's resolved rows."""

    counts: dict[str, int] = {}
    for row in cell.resolved(case):
        for token, count in row.read.bare_shared_tokens.items():
            counts[token] = counts.get(token, 0) + count
    return dict(sorted(counts.items()))


def program_marks(cell: Cell) -> dict[str, Any]:
    """Every mark the program can write, per comparison, per register, at kind grain.

    Requires the baseline seal (G8): the G9 downgrade is read off the baseline,
    so a mark computed before the baseline exists would be one the baseline
    could later contradict.  ``BASELINE_NOT_FIRST`` otherwise.

    Registers are never combined and no mark is a quantity.  A register's mark
    is ``differs`` where one of *its own* kinds differs and the baseline does not
    already exhibit that kind, ``same`` where every one of its kinds is decided
    and none differs, and ``unresolved`` otherwise — including where a bare id
    token shared with the account document forces it (G10(c)), which is
    ``unresolved`` and is **never** ``differs``.
    """

    sha = cell.require_seal("program_marks")
    baseline = build_baseline(cell)
    thin = under_replicated(cell)
    reads = {
        case: _merge_reads([r.read for r in cell.readable(case)]) for case in cell.cases
    }

    comparisons: dict[str, Any] = {}
    for left_case, right_case in cell.comparisons:
        label = COMPARISON_LABELS[(left_case, right_case)]
        entry: dict[str, Any] = {
            "left_case": left_case,
            "right_case": right_case,
            "left_resolved": [r.key for r in cell.resolved(left_case)],
            "right_resolved": [r.key for r in cell.resolved(right_case)],
            "left_readable": [r.key for r in cell.readable(left_case)],
            "right_readable": [r.key for r in cell.readable(right_case)],
            "under_replicated": sorted({left_case, right_case} & thin),
            "registers": {},
        }
        thin_here = bool(entry["under_replicated"])
        enough = (
            not thin_here
            and len(entry["left_readable"]) >= MIN_RESOLVED_REPLICATES
            and len(entry["right_readable"]) >= MIN_RESOLVED_REPLICATES
            and baseline.sufficient
        )
        for register in standard.REGISTER_IDS:
            entry["registers"][register] = _register_mark(
                cell,
                baseline,
                reads,
                left_case,
                right_case,
                register,
                enough=enough,
                under_replicated=thin_here,
            )
        comparisons[label] = entry

    record = {
        "schema": PROGRAM_MARKS_SCHEMA,
        "cell": cell.cell_id,
        "endpoint": cell.endpoint,
        "arm": cell.arm,
        "source": cell.source,
        "baseline_sha256": sha,
        "baseline_sufficient": baseline.sufficient,
        "min_resolved_replicates": MIN_RESOLVED_REPLICATES,
        "under_replicated_cases": sorted(thin),
        "byte_identity": byte_identity_defeater(cell),
        "comparisons": comparisons,
        "note": (
            "Marks stand and fall separately by register; nothing here sums, "
            "averages, weights or ranks them, and no count is a verdict."
        ),
    }
    assert_no_scoring_keys(record)
    return record


def _register_mark(
    cell: Cell,
    baseline: Baseline,
    reads: Mapping[str, FclRead],
    left_case: str,
    right_case: str,
    register: str,
    *,
    enough: bool,
    under_replicated: bool = False,
) -> dict[str, Any]:
    """One register's program mark for one comparison, at kind grain.

    Under-replication dominates every other reason: a comparison touching a case
    with too few resolved replicates is ``unresolved`` because the data is
    absent, and saying anything finer about it — even that a bare token forced
    it — would be reading a case that was never resolved.
    """

    forced_left = _forced_unresolved_tokens(cell, left_case)
    forced_right = _forced_unresolved_tokens(cell, right_case)
    forced = (not under_replicated) and register == "E" and bool(forced_left or forced_right)

    kinds: dict[str, Any] = {}
    for kind in difference_kinds_for(register):
        if under_replicated:
            kinds[kind] = {
                "mark": standard.UNRESOLVED_TOKEN,
                "decided": False,
                "forced_unresolved": False,
                "reason": (
                    "fewer than the minimum resolved replicates of a case in "
                    "this comparison: absent data, never an absence of "
                    "difference (PLAN 8; design 2.4 G10(b))"
                ),
                "evidence": {},
            }
            continue
        if forced:
            kinds[kind] = {
                "mark": standard.UNRESOLVED_TOKEN,
                "decided": True,
                "forced_unresolved": True,
                "reason": (
                    "a bare id token shared with the account document is "
                    "unresolved for register E and is never differs (PLAN 8a)"
                ),
                "evidence": {"left": forced_left, "right": forced_right},
            }
            continue
        if kind in NOT_PROGRAM_READ or not enough:
            kinds[kind] = {
                "mark": standard.UNRESOLVED_TOKEN,
                "decided": False,
                "forced_unresolved": False,
                "reason": NOT_PROGRAM_READ.get(
                    kind,
                    RESIDUE_REASONS["BASELINE_UNREADABLE"]
                    if not baseline.sufficient
                    else RESIDUE_REASONS["REPLICATES_UNREADABLE"],
                ),
                "evidence": {},
            }
            continue
        decided, differs, evidence = _kind_difference(
            reads[left_case], reads[right_case], kind
        )
        if not decided:
            kinds[kind] = {
                "mark": standard.UNRESOLVED_TOKEN,
                "decided": False,
                "forced_unresolved": False,
                "reason": RESIDUE_REASONS["NO_SHARED_CRITICISM"],
                "evidence": evidence,
            }
            continue
        entry: dict[str, Any] = {
            "mark": "differs" if differs else "same",
            "decided": True,
            "forced_unresolved": False,
            "reason": "",
            "evidence": evidence,
        }
        if differs and baseline.exhibits(register, kind):
            entry["mark"] = "same"
            entry["block"] = BASELINE_FORCED_SAME_BLOCK
            entry["forced_by"] = {
                "rule": (
                    "the same kind of difference already appears between a pair "
                    "of replicates inside ORIGINAL, so the register is same for "
                    "this pair and the fact is recorded (PLAN 8a)"
                ),
                "pairs": [
                    p.as_dict() for p in baseline.pairs if kind in p.kinds
                ],
            }
        kinds[kind] = entry

    marks = {k: v["mark"] for k, v in kinds.items()}
    carried = [k for k, v in kinds.items() if v["mark"] == "differs"]
    if carried:
        mark, difference_kind = "differs", carried[0]
    elif all(v["decided"] for v in kinds.values()) and not forced:
        mark, difference_kind = "same", None
    else:
        mark, difference_kind = standard.UNRESOLVED_TOKEN, None

    assert mark in standard.MARKS
    return {
        "register": register,
        "mark": mark,
        "difference_kind": difference_kind,
        "forced_unresolved": forced,
        "program_decided": all(v["decided"] for v in kinds.values()),
        "kinds": kinds,
        "kind_marks": marks,
    }


# --------------------------------------------------------------------------
# The residue
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ResidueRow:
    """One row the program could not decide, and what it needs to be decided.

    ``register`` is on every row so that W4-MARKER can pass ``register=`` to
    :func:`minireason.loop.contracts.check` (wave 0's O11): no marker call is
    ever in the position of not knowing which register it was asked about.
    """

    cell: str
    comparison: str
    left_case: str
    right_case: str
    register: str
    difference_kinds: tuple[str, ...]
    reason: str
    detail: str
    left_replicates: tuple[str, ...]
    right_replicates: tuple[str, ...]
    unreadable_replicates: tuple[str, ...]
    baseline_sha256: str

    def as_dict(self) -> dict[str, Any]:
        record = {
            "schema": RESIDUE_SCHEMA,
            "cell": self.cell,
            "comparison": self.comparison,
            "left_case": self.left_case,
            "right_case": self.right_case,
            "register": self.register,
            "difference_kinds": list(self.difference_kinds),
            "reason": self.reason,
            "detail": self.detail,
            "left_replicates": list(self.left_replicates),
            "right_replicates": list(self.right_replicates),
            "unreadable_replicates": list(self.unreadable_replicates),
            "baseline_sha256": self.baseline_sha256,
        }
        assert_no_scoring_keys(record)
        return record


def residue(cell: Cell) -> list[ResidueRow]:
    """Exactly the rows the program could not decide, and nothing else.

    Requires the baseline seal (G8): *the baseline is written and sealed before
    any residue is offered for marking.*  Three things are **not** here:

    * every register of every comparison the program decided;
    * every comparison touching a case with fewer than
      :data:`MIN_RESOLVED_REPLICATES` resolved replicates — that case is absent
      data and is never trialled;
    * register E where a bare id token shared with the account document forced
      it ``unresolved`` — it is never ``differs`` and never reaches a trial.
    """

    sha = cell.require_seal("residue")
    marks = program_marks(cell)
    rows: list[ResidueRow] = []
    for (left_case, right_case) in cell.comparisons:
        label = COMPARISON_LABELS[(left_case, right_case)]
        entry = marks["comparisons"][label]
        if entry["under_replicated"]:
            continue
        unreadable = tuple(
            r.key
            for case in (left_case, right_case)
            for r in cell.resolved(case)
            if not r.readable
        )
        for register in standard.REGISTER_IDS:
            block = entry["registers"][register]
            if block["forced_unresolved"]:
                continue
            open_kinds = tuple(
                kind
                for kind, detail in block["kinds"].items()
                if not detail["decided"]
            )
            if not open_kinds:
                continue
            rows.append(
                ResidueRow(
                    cell=cell.cell_id,
                    comparison=label,
                    left_case=left_case,
                    right_case=right_case,
                    register=register,
                    difference_kinds=open_kinds,
                    reason=_residue_reason(block, open_kinds, unreadable),
                    detail=block["kinds"][open_kinds[0]]["reason"],
                    left_replicates=tuple(entry["left_readable"]),
                    right_replicates=tuple(entry["right_readable"]),
                    unreadable_replicates=unreadable,
                    baseline_sha256=sha,
                )
            )
    return rows


def _residue_reason(
    block: Mapping[str, Any], open_kinds: tuple[str, ...], unreadable: tuple[str, ...]
) -> str:
    if all(kind in NOT_PROGRAM_READ for kind in open_kinds):
        return "NOT_PROGRAM_READ"
    detail = block["kinds"][open_kinds[0]]["reason"]
    if detail == RESIDUE_REASONS["NO_SHARED_CRITICISM"]:
        return "NO_SHARED_CRITICISM"
    if detail == RESIDUE_REASONS["BASELINE_UNREADABLE"]:
        return "BASELINE_UNREADABLE"
    return "REPLICATES_UNREADABLE" if unreadable else "NOT_PROGRAM_READ"


# --------------------------------------------------------------------------
# The pairwise surface (S5)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class PairQuotes:
    """Where a marker's ``left_quote`` and ``right_quote`` resolved, if they did.

    ``ok`` is true only when both resolved uniquely (G2) *and* each landed on
    its own declared side (G3) — a left quote found in the right replicate is a
    quote of the other side and is not a left quote.
    """

    left: Offset | None
    right: Offset | None
    left_count: int
    right_count: int
    block: str | None

    @property
    def ok(self) -> bool:
        return self.block is None

    def as_dict(self) -> dict[str, Any]:
        return {
            "left": None if self.left is None else self.left.as_dict(),
            "right": None if self.right is None else self.right.as_dict(),
            "left_count": self.left_count,
            "right_count": self.right_count,
            "block": self.block,
        }


def pairwise_surface(
    cell: Cell, left: Replicate | str, right: Replicate | str
) -> Surface:
    """The two-sided material a pairwise mark's quotes resolve against.

    One :class:`~minireason.loop.surface.Surface` whose two declared spans are
    the ``commitments`` documents of ``left`` (:data:`SIDE_LEFT`) and ``right``
    (:data:`SIDE_RIGHT`), laid out in W1-SURFACE's own label framing so that a
    quote of a label, or one crossing the boundary between the two sides,
    resolves as ``framing`` and is refused by
    :func:`~minireason.loop.surface.within_declared_span`.

    A **cross-case** surface requires the baseline seal: G8's "the marker
    refuses to render any cross-case pack for a cell until that cell's
    within-ORIGINAL baseline grid exists and its sha256 is pinned".  A
    within-ORIGINAL surface is the baseline's own reading and needs no seal.
    """

    left_row = left if isinstance(left, Replicate) else cell.replicate(left)
    right_row = right if isinstance(right, Replicate) else cell.replicate(right)
    for row in (left_row, right_row):
        if row not in cell.replicates:
            raise MarkprepError(REPLICATE_UNKNOWN, f"{cell.cell_id}: {row.key}")
        if row.commitments is None:
            raise MarkprepError(REPLICATE_NOT_READABLE, f"{cell.cell_id}: {row.key}")
    if left_row.case != right_row.case or left_row.case != BASELINE_CASE:
        cell.require_seal(f"pairwise_surface {left_row.key} vs {right_row.key}")

    parts: list[bytes] = []
    spans: list[Span] = []
    cursor = 0
    for side, row in ((SIDE_LEFT, left_row), (SIDE_RIGHT, right_row)):
        if parts:
            parts.append(surface_module.BLOCK_SEPARATOR)
            cursor += len(surface_module.BLOCK_SEPARATOR)
        what = "left" if side == SIDE_LEFT else "right"
        label = (
            f"{surface_module.LABEL_OPEN}{what} {row.key}: {cell.cell_id}"
            f"{surface_module.LABEL_CLOSE}"
        ).encode("utf-8") + surface_module.LABEL_TERMINATOR
        parts.append(label)
        cursor += len(label)
        content = row.commitments.encode("utf-8")
        spans.append(
            Span(
                side=side,
                start=cursor,
                end=cursor + len(content),
                occurrence_path=row.artifact_path,
                source_field=surface_module.FIELD_COMMITMENTS,
                file_start=0,
                file_end=len(row.commitments),
                coordinate_key=f"{cell.cell_id}/{row.key}",
                record_id=None,
                ordinal=None,
            )
        )
        parts.append(content)
        cursor += len(content)

    return Surface(
        text=b"".join(parts),
        spans=tuple(spans),
        referring_coordinate_key=f"{cell.cell_id}/{left_row.key}",
        target_coordinate_key=f"{cell.cell_id}/{right_row.key}",
        referring_record_id=None,
        target_record_id=None,
        ref_field=surface_module.FIELD_COMMITMENTS,
        ref_verbatim=f"{left_row.case} vs {right_row.case}",
        ref_grain="artifact",
    )


def resolve_pair(surface: Surface, left_quote: Any, right_quote: Any) -> PairQuotes:
    """G2(a) and G3 for a pairwise mark's two quotes, one per side.

    Each quote is resolved with :func:`~minireason.loop.surface.resolve_unique`
    and checked with :func:`~minireason.loop.surface.within_declared_span`; the
    left quote must land on :data:`SIDE_LEFT` and the right on
    :data:`SIDE_RIGHT`.  ``block`` carries W1-SURFACE's own two codes and is
    ``None`` only where both quotes passed both checks.
    """

    left = resolve_unique(surface, left_quote)
    right = resolve_unique(surface, right_quote)
    left_count = surface.count(left_quote)
    right_count = surface.count(right_quote)

    block: str | None = None
    if left is None or right is None:
        block = surface_module.REFERENTIAL_INTEGRITY_BLOCK
    elif not (within_declared_span(surface, left) and left.side == SIDE_LEFT):
        block = surface_module.OPERATIVE_TARGET_BLOCK
    elif not (within_declared_span(surface, right) and right.side == SIDE_RIGHT):
        block = surface_module.OPERATIVE_TARGET_BLOCK
    return PairQuotes(left, right, left_count, right_count, block)
