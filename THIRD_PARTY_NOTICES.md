# Third-party notices

This repository contains code copied from another project. The notice below
names it, its licence, and every file that came from it.

---

## AHepi/DeepReason

- **Upstream:** <https://github.com/AHepi/DeepReason>
- **Commit:** `9607fba6f0a3066fbcab282c9ae0fad823e52e0c` (short: `9607fba`)
- **Licence:** MIT — full text at `src/deepreason_core/LICENSE`, copied
  verbatim from the upstream `LICENSE` at that commit
  (sha256 `772e479a9cf08762785c6d99da14d5266cafaff751a40cf097e52f9216874e86`).
- **Copyright:** Copyright (c) 2026 Aaron Hepi
- **Machine-readable provenance:** `docs/sources/deepreason-core-provenance.json`
  — per-file source and destination paths, sha256 digests, and the exact cut
  made to each file.
- **Human-readable rationale:** `docs/sources/deepreason-core-vendor-notes.md`, published alongside that
  provenance record — what was cut, why, and what could not be cut cleanly.

The vendored subset is the deterministic P0 core of the DeepReason harness
spec v1.3 (spec §16 P0 row). It is imported as `deepreason_core`, not
`deepreason`: every `deepreason.` import in the copied files was rewritten to
`deepreason_core.`, and each file carries a one-line header naming its
upstream path and this licence. Nothing else in the copied files was rewritten
— every other change is a deletion, with four exceptions listed in
`docs/sources/deepreason-core-vendor-notes.md`.

### Library files

| Vendored path | Upstream path | Form |
|---|---|---|
| `src/deepreason_core/__init__.py` | `src/deepreason/__init__.py` | verbatim |
| `src/deepreason_core/canonical.py` | `src/deepreason/canonical.py` | verbatim |
| `src/deepreason_core/frozen.py` | `src/deepreason/frozen.py` | verbatim |
| `src/deepreason_core/harness.py` | `src/deepreason/harness.py` | cut (P0 slice; two functions inlined from `src/deepreason/informal/trial.py`) |
| `src/deepreason_core/adjudication/__init__.py` | `src/deepreason/adjudication/__init__.py` | verbatim |
| `src/deepreason_core/adjudication/edges.py` | `src/deepreason/adjudication/edges.py` | cut |
| `src/deepreason_core/adjudication/grounded.py` | `src/deepreason/adjudication/grounded.py` | verbatim |
| `src/deepreason_core/adjudication/support.py` | `src/deepreason/adjudication/support.py` | verbatim |
| `src/deepreason_core/log/__init__.py` | `src/deepreason/log/__init__.py` | verbatim |
| `src/deepreason_core/log/event_log.py` | `src/deepreason/log/event_log.py` | verbatim |
| `src/deepreason_core/ontology/__init__.py` | `src/deepreason/ontology/__init__.py` | cut |
| `src/deepreason_core/ontology/artifact.py` | `src/deepreason/ontology/artifact.py` | cut |
| `src/deepreason_core/ontology/commitment.py` | `src/deepreason/ontology/commitment.py` | verbatim |
| `src/deepreason_core/ontology/event.py` | `src/deepreason/ontology/event.py` | cut |
| `src/deepreason_core/ontology/frozen.py` | `src/deepreason/ontology/frozen.py` | verbatim |
| `src/deepreason_core/ontology/problem.py` | `src/deepreason/ontology/problem.py` | cut |
| `src/deepreason_core/ontology/state.py` | `src/deepreason/ontology/state.py` | cut |
| `src/deepreason_core/ontology/warrant.py` | `src/deepreason/ontology/warrant.py` | verbatim |
| `src/deepreason_core/storage/__init__.py` | `src/deepreason/storage/__init__.py` | verbatim |
| `src/deepreason_core/storage/blobs.py` | `src/deepreason/storage/blobs.py` | verbatim |
| `src/deepreason_core/storage/objects.py` | `src/deepreason/storage/objects.py` | cut |
| `src/deepreason_core/LICENSE` | `LICENSE` | verbatim |

### Test files

Converted from the upstream pytest suite to `unittest`; assertions preserved
except where `provenance.json` records a deletion.

| Vendored path | Upstream path |
|---|---|
| `tests/graph_core/helpers.py` | `tests/conftest.py` |
| `tests/graph_core/test_adjudication.py` | `tests/test_adjudication.py` |
| `tests/graph_core/test_blob_store_long_paths.py` | `tests/test_blob_store_long_paths.py` |
| `tests/graph_core/test_ontology.py` | `tests/test_ontology.py` |
| `tests/graph_core/test_persistence_invariants.py` | `tests/test_persistence_invariants.py` |
| `tests/graph_core/test_torn_append.py` | `tests/test_torn_append.py` |

`tests/graph_core/__init__.py`, `tests/graph_core/golden_build.py`,
`tests/graph_core/test_p0_acceptance.py` and
`tests/graph_core/test_closures_and_fences.py` are original to this
repository, not copied from upstream. They exercise the vendored code and are
covered by this repository's own licence.

### Spec

`docs/sources/harness-spec-v1.3.md` is byte-identical to upstream
`docs/harness-spec-v1.3.md` at the same commit
(sha256 `9116c8592387ce22d436cde600d77077d2b08176225f49d1c01613eb8dfb5ca8`).

---

### MIT licence text

The full text as copied to `src/deepreason_core/LICENSE`:

```
MIT License

Copyright (c) 2026 Aaron Hepi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
