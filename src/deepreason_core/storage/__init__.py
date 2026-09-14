# Vendored from AHepi/DeepReason@9607fba src/deepreason/storage/__init__.py (MIT, see src/deepreason_core/LICENSE); see docs/sources/deepreason-core-provenance.json
"""Storage (spec §14): namespaced content-addressed objects + JSONL, git-native.

New objects live below ``objects/<schema>/``; legacy flat records remain
readable. Save = git commit. Sealed holdout blobs live in a ``holdout/``
namespace excluded from pack rendering until their Reveal event (§10.5).
The refuted-index (embedding NN over refuted artifacts, §11.5) is rebuilt
deterministically from the log.
"""
