# Source errata

## SRC-001 — ECS PDF rendering gaps

The supplied ECS 2.0 PDF has missing or clipped mathematical notation. A read-only visual review found the graded-accounting expression at printed §2.3 on PDF page 4 incomplete (`[ Account` remains), and the HardToVary formula at §3.4 on page 5 clipped. Several Greek symbols are absent. This is visible in the page render, so extraction alone cannot restore it.

Impact: no complete transcription or formal conformance claim may rest on reconstructed missing symbols. The readable prose and intact §2.2 clauses support a limited experimental interpretation, with unresolved formal expressions explicitly retained. Corrective action would be a repaired source export; none has been supplied. The experiments do not silently invent the missing equations.

## SRC-002 — A stale kernel-table range cites a row that does not exist

`src/creib/forge/mini/conformance_kernels.py:9` describes the kernel table in `docs/kernel.md` as covering "P-01 to P-08, R-01, R-02". Observation: when the requirement register was recovered from AHepi/h-EPI at commit `b2a33283dc1e05fb83c3357b26e2cc12115f6b6c` and its annotation labels were resolved, 54 of 55 labels cited from the frozen engine found an entry and P-08 did not. The recovered `docs/kernel.md` contains nine P-rows — P-01 through P-07, then P-09 and P-10, written out of numeric order — with no P-08 and no note of a gap.

What failed: a range citation names a row the cited document does not define. Impact: bounded. The citation still identifies the right document and the right table, and the nine rows that exist are unambiguous, so no check, test or published record depends on a P-08. The failure is that a reader following the range looks for a tenth row and cannot tell whether it was lost in extraction, renumbered, or never written.

Cause, established rather than suspected: the recovered file is byte-identical to its upstream source (`docs/sources/mini-register-provenance.json`), so the row is absent upstream and the range was stale when it was written. Competing explanations considered and rejected by that digest: loss during extraction from h-EPI, and loss during this recovery. Which upstream edit removed or renumbered the row was not traced; that remains open and would need the h-EPI history, not this repository.

Corrective action: documented in `docs/mini/README.md`, which states the actual P-series and that the range is stale. The frozen engine file is not edited — it is `src/creib/forge/mini/` code, pinned by plan `runtime_files` maps, and editing a comment there would change a verified identity to fix a citation that already points at the right document. Checked: the corrective action is a documentation statement, and the fact it states — nine P-rows, no P-08 — was verified directly against the recovered bytes.
