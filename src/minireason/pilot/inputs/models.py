# Port provenance: https://github.com/AHepi/DeepReason @ 9607fba6f0a3066fbcab282c9ae0fad823e52e0c
# Upstream: src/deepreason/evidence/models.py; MIT, Copyright (c) 2026 Aaron Hepi; see LICENSE.
"""Canonical admission records for a pre-freeze evidence dossier."""

from __future__ import annotations

from collections.abc import Mapping
from typing import ClassVar, Literal

from pydantic import ConfigDict, Field, StrictInt, field_validator, model_validator

from .canonical import canonical_json, sha256_hex
from .frozen import FrozenDict, FrozenRecord


_DIGEST = r"^[0-9a-f]{64}$"
_SOURCE_ID = r"^[A-Za-z][A-Za-z0-9._:-]{0,127}$"


def _canonical_digest(domain: str, payload: dict) -> str:
    return sha256_hex(domain.encode("utf-8") + b"\x00" + canonical_json(payload))


class _InputRecord(FrozenRecord):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        populate_by_name=True,
        serialize_by_alias=True,
    )


class AttachedSourceProvenanceV1(_InputRecord):
    """Operator-claimed provenance; informative and explicitly attackable."""

    supplied_by: str = Field(min_length=1, max_length=512)
    acquisition_method: str = Field(min_length=1, max_length=512)
    note: str | None = Field(default=None, max_length=4_096)

    @field_validator("supplied_by", "acquisition_method", "note")
    @classmethod
    def _nonblank(cls, value):
        if value is not None and not value.strip():
            raise ValueError("provenance text must be nonblank")
        return value


class AttachedSourceV1(_InputRecord):
    schema_: Literal["attached-source.v1"] = Field(
        "attached-source.v1", alias="schema"
    )
    id: str = Field(pattern=_SOURCE_ID)
    title: str = Field(min_length=1, max_length=1_024)
    source_locator: str = Field(min_length=1, max_length=4_096)
    source_class: Literal[
        "primary_paper",
        "official_hardware_documentation",
        "official_implementation",
        "reproducible_benchmark",
        "disputed_measurement",
        "synthetic_assumption",
        "other",
    ]
    media_type: str = Field(min_length=1, max_length=256)
    content_ref: str = Field(pattern=_DIGEST)
    content_sha256: str = Field(pattern=_DIGEST)
    byte_count: StrictInt = Field(ge=1, le=16 * 1024 * 1024)
    retrieved_at_claim: str | None = Field(default=None, max_length=128)
    license_or_usage_note: str | None = Field(default=None, max_length=4_096)
    provenance: AttachedSourceProvenanceV1
    declared_entities: tuple[str, ...] = Field(default=(), max_length=256)
    declared_facets: tuple[str, ...] = Field(default=(), max_length=256)

    @field_validator(
        "title",
        "source_locator",
        "media_type",
        "retrieved_at_claim",
        "license_or_usage_note",
    )
    @classmethod
    def _nonblank(cls, value):
        if value is not None and not value.strip():
            raise ValueError("source text fields must be nonblank")
        return value

    @field_validator("declared_entities", "declared_facets")
    @classmethod
    def _canonical_terms(cls, value):
        cleaned = tuple(term.strip() for term in value)
        if any(not term or len(term) > 256 for term in cleaned):
            raise ValueError("declared source terms must be bounded and nonblank")
        if cleaned != tuple(sorted(set(cleaned), key=lambda term: (term.casefold(), term))):
            raise ValueError("declared source terms must be unique and canonically sorted")
        return cleaned

    @model_validator(mode="after")
    def _content_identity(self):
        # BlobStore uses the raw-content SHA-256 as its reference. Keeping both
        # fields makes the provenance contract explicit without permitting two
        # disagreeing identities.
        if self.content_ref != self.content_sha256:
            raise ValueError("attached source content reference and digest differ")
        return self


class EvidenceDossierV1(_InputRecord):
    schema_: Literal["evidence-dossier.v1"] = Field(
        "evidence-dossier.v1", alias="schema"
    )
    dossier_digest: str = Field(pattern=_DIGEST)
    problem_ref: str = Field(min_length=1, max_length=512)
    sources: tuple[AttachedSourceV1, ...] = Field(max_length=1_000)
    total_byte_count: StrictInt = Field(ge=0, le=64 * 1024 * 1024)
    creation_provenance: AttachedSourceProvenanceV1

    IDENTITY_DOMAIN: ClassVar[str] = "evidence-dossier.v1"

    @classmethod
    def create(cls, **values) -> "EvidenceDossierV1":
        payload = cls._identity_payload_from_values(values)
        return cls(dossier_digest=_canonical_digest(cls.IDENTITY_DOMAIN, payload), **values)

    @classmethod
    def _identity_payload_from_values(cls, values: dict) -> dict:
        provisional = cls.model_construct(dossier_digest="0" * 64, **values)
        return provisional.model_dump(
            mode="json", by_alias=True, exclude={"dossier_digest"}
        )

    def identity_payload(self) -> dict:
        return self.model_dump(
            mode="json", by_alias=True, exclude={"dossier_digest"}
        )

    @field_validator("sources")
    @classmethod
    def _canonical_sources(cls, value):
        ids = tuple(source.id for source in value)
        if ids != tuple(sorted(ids)) or len(ids) != len(set(ids)):
            raise ValueError("dossier sources must be ID-unique and sorted")
        return tuple(value)

    @model_validator(mode="after")
    def _identity_and_size(self):
        if self.total_byte_count != sum(source.byte_count for source in self.sources):
            raise ValueError("dossier total byte count does not match its sources")
        expected = _canonical_digest(self.IDENTITY_DOMAIN, self.identity_payload())
        if self.dossier_digest != expected:
            raise ValueError("dossier digest does not match its canonical payload")
        return self


class AdmissionBlockV1(_InputRecord):
    """One canonical, content-addressed unit admitted from a source.

    Span blocks (``section``/``paragraph``/``table``/``csv_sample``) never
    inline their text: the canonical text is the exact byte slice
    ``source_bytes[span_start:span_end]`` decoded as UTF-8, recoverable
    deterministically from the content-addressed source, and pinned here by
    ``text_sha256``.  Projection blocks (``csv_schema``/``csv_stats``) are
    deterministic computations over the whole source, so their bounded text
    is inlined; their span covers the entire source they project.
    """

    schema_: Literal["admission-block.v1"] = Field(
        "admission-block.v1", alias="schema"
    )
    id: str = Field(pattern=_DIGEST)
    source_sha256: str = Field(pattern=_DIGEST)
    kind: Literal[
        "section",
        "paragraph",
        "table",
        "csv_schema",
        "csv_stats",
        "csv_sample",
        # Adapter-extracted text without byte-span fidelity: inlined,
        # tier-capped by the adapter's declared span fidelity class.
        "extracted",
    ]
    tier: Literal["evidence", "workshop", "memory"]
    span_start: StrictInt = Field(ge=0)
    span_end: StrictInt = Field(ge=1)
    text_sha256: str = Field(pattern=_DIGEST)
    text: str | None = Field(default=None, min_length=1, max_length=8_192)
    title: str | None = Field(default=None, min_length=1, max_length=256)

    IDENTITY_DOMAIN: ClassVar[str] = "admission-block.v1"

    @classmethod
    def create(cls, *, parser_version: str, **values) -> "AdmissionBlockV1":
        provisional = cls.model_construct(id="0" * 64, **values)
        payload = {
            "parser_version": parser_version,
            **provisional.model_dump(
                mode="json", by_alias=True, exclude={"id", "text", "title"}
            ),
        }
        return cls(id=_canonical_digest(cls.IDENTITY_DOMAIN, payload), **values)

    @model_validator(mode="after")
    def _span_and_projection_shape(self):
        if self.span_end <= self.span_start:
            raise ValueError("admission block span must be non-empty")
        inlined = self.kind in {"csv_schema", "csv_stats", "extracted"}
        if inlined != (self.text is not None):
            raise ValueError(
                "projection blocks inline their text; span blocks never do"
            )
        if self.kind == "extracted" and self.tier == "evidence":
            raise ValueError(
                "extracted blocks lack byte-span fidelity and cannot enter "
                "the evidence tier"
            )
        if self.text is not None and sha256_hex(
            self.text.encode("utf-8")
        ) != self.text_sha256:
            raise ValueError("inlined block text does not match its digest")
        return self


class AdmissionRefusalV1(_InputRecord):
    """A typed, durable reason content did not enter the dossier."""

    schema_: Literal["admission-refusal.v1"] = Field(
        "admission-refusal.v1", alias="schema"
    )
    code: Literal[
        "ADMISSION_SOURCE_EMPTY",
        "ADMISSION_SOURCE_TOO_LARGE",
        "ADMISSION_TOTAL_TOO_LARGE",
        "ADMISSION_SOURCE_UNREADABLE",
        "ADMISSION_MEDIA_UNSUPPORTED",
        "ADMISSION_BLOCK_BUDGET_EXCEEDED",
    ]
    detail: str = Field(min_length=1, max_length=2_048)
    source_sha256: str | None = Field(default=None, pattern=_DIGEST)
    source_locator: str | None = Field(default=None, max_length=4_096)


class SourceAdapterBindingV1(_InputRecord):
    """Version-bound identity of the adapter that admitted one source.

    Binding into the dossier digest means a different adapter or adapter
    version mints a different dossier — inspecting or reproducing a dossier
    without the recorded adapter version is a typed refusal, never silent
    divergence.
    """

    schema_: Literal["source-adapter-binding.v1"] = Field(
        "source-adapter-binding.v1", alias="schema"
    )
    source_sha256: str = Field(pattern=_DIGEST)
    adapter_id: str = Field(min_length=1, max_length=64)
    adapter_version: str = Field(min_length=1, max_length=64)
    span_fidelity: Literal["exact_spans", "approximate", "none"]


class EvidenceDossierV2(_InputRecord):
    """Admission-era dossier: sources plus their canonical admission blocks.

    The digest covers the parser version, every block identity, and every
    refusal, so a different parser version — or any difference in what was
    admitted or refused — mints a different dossier digest and therefore a
    different run identity.  Improvement is never silent mutation.
    """

    schema_: Literal["evidence-dossier.v2"] = Field(
        "evidence-dossier.v2", alias="schema"
    )
    dossier_digest: str = Field(pattern=_DIGEST)
    problem_ref: str = Field(min_length=1, max_length=512)
    parser_version: str = Field(min_length=1, max_length=128)
    sources: tuple[AttachedSourceV1, ...] = Field(max_length=1_000)
    blocks: tuple[AdmissionBlockV1, ...] = Field(default=(), max_length=4_000)
    refusals: tuple[AdmissionRefusalV1, ...] = Field(default=(), max_length=1_000)
    adapters: tuple[SourceAdapterBindingV1, ...] = Field(
        default=(), max_length=1_000
    )
    total_byte_count: StrictInt = Field(ge=0, le=64 * 1024 * 1024)
    creation_provenance: AttachedSourceProvenanceV1

    IDENTITY_DOMAIN: ClassVar[str] = "evidence-dossier.v2"

    @classmethod
    def create(cls, **values) -> "EvidenceDossierV2":
        provisional = cls.model_construct(dossier_digest="0" * 64, **values)
        payload = provisional.model_dump(
            mode="json", by_alias=True, exclude={"dossier_digest"}
        )
        return cls(
            dossier_digest=_canonical_digest(cls.IDENTITY_DOMAIN, payload),
            **values,
        )

    def identity_payload(self) -> dict:
        return self.model_dump(
            mode="json", by_alias=True, exclude={"dossier_digest"}
        )

    @field_validator("sources")
    @classmethod
    def _canonical_sources(cls, value):
        ids = tuple(source.id for source in value)
        if ids != tuple(sorted(ids)) or len(ids) != len(set(ids)):
            raise ValueError("dossier sources must be ID-unique and sorted")
        return tuple(value)

    @field_validator("blocks")
    @classmethod
    def _canonical_blocks(cls, value):
        ids = tuple(block.id for block in value)
        if ids != tuple(sorted(ids)) or len(ids) != len(set(ids)):
            raise ValueError("dossier blocks must be ID-unique and sorted")
        return tuple(value)

    @model_validator(mode="after")
    def _identity_size_and_references(self):
        if self.total_byte_count != sum(source.byte_count for source in self.sources):
            raise ValueError("dossier total byte count does not match its sources")
        known = {source.content_sha256 for source in self.sources}
        for block in self.blocks:
            if block.source_sha256 not in known:
                raise ValueError("admission block references an unknown source")
        bound = [binding.source_sha256 for binding in self.adapters]
        if len(bound) != len(set(bound)):
            raise ValueError("a source binds at most one admitting adapter")
        for binding in self.adapters:
            if binding.source_sha256 not in known:
                raise ValueError("adapter binding references an unknown source")
        expected = _canonical_digest(self.IDENTITY_DOMAIN, self.identity_payload())
        if self.dossier_digest != expected:
            raise ValueError("dossier digest does not match its canonical payload")
        return self


EvidenceDossier = EvidenceDossierV1 | EvidenceDossierV2


