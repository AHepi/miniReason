# Port provenance: https://github.com/AHepi/DeepReason @ 9607fba6f0a3066fbcab282c9ae0fad823e52e0c
# Upstream: src/deepreason/evidence/citations.py:66-87; MIT, Copyright (c) 2026 Aaron Hepi; see LICENSE.
# Port provenance: AHepi/DeepReason @ 9607fba6f0a3066fbcab282c9ae0fad823e52e0c
# src/deepreason/evidence/citations.py:66-87; MIT, see LICENSE.
import hashlib
from .models import AdmissionBlockV1

class CitationIntegrityError(ValueError):
    pass

def canonical_block_text(block: AdmissionBlockV1, source_bytes: bytes) -> str:
    """Recover a block's canonical text, verifying it against the dossier.

    Projection and extracted blocks inline their text (already pinned by the
    block's identity); span blocks are the exact byte slice of the admitted
    source. Any divergence from the recorded ``text_sha256`` is an integrity
    error, never a silently different text.
    """

    if block.text is not None:
        return block.text
    # P-A2 additionally binds the complete source, not only a coincident slice.
    if hashlib.sha256(source_bytes).hexdigest() != block.source_sha256:
        raise CitationIntegrityError("source bytes do not match the admitted source digest")
    window = source_bytes[block.span_start : block.span_end]
    if hashlib.sha256(window).hexdigest() != block.text_sha256:
        raise CitationIntegrityError(
            f"block {block.id[:12]} span bytes do not match the admitted text digest"
        )
    try:
        return window.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CitationIntegrityError(
            f"block {block.id[:12]} span bytes are not valid UTF-8"
        ) from error



def exact_quote(block, source_bytes, quote: str) -> bool:
    """Pilot adaptation: no whitespace-folding fallback for exact locators."""
    return bool(quote) and quote.encode("utf-8") in canonical_block_text(block, source_bytes).encode("utf-8")
