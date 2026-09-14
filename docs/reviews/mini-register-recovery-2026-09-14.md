# Mini's requirement register: what was missing, what was recovered

REC-20260914-K, 2026-09-14.

Mechanical recovery, digest verification and citation resolution were performed
by a delegated Opus 5 agent under the orchestrator's session mandate, read-only
against this repository. The last section is interpretation and belongs to the
publishing session, not to the delegate.

## What was missing

The frozen engine under `src/creib/forge/mini/` was extracted from
[AHepi/h-EPI](https://github.com/AHepi/h-EPI) at commit
`b2a33283dc1e05fb83c3357b26e2cc12115f6b6c`, as
[`../sources/extraction-provenance.json`](../sources/extraction-provenance.json)
records. Its documentation was not extracted with it. Before this recovery
`docs/mini/`, `docs/kernel.md` and `docs/failure-modes.md` did not exist here.

Two kinds of citation were therefore dangling. Twelve citations name a document
by path — `docs/mini/USE_TEST.md` and `docs/mini/AUTONOMY.md` twice each,
`docs/kernel.md` and `docs/failure-modes.md` twice each, and
`docs/mini/SPEC.md`, `docs/mini/PIPELINE_MATH.md`, `docs/mini/ERRATA.md`,
`docs/mini/BUILD_TEST.md` once each. Beyond those, comments and docstrings in
the engine cite 55 distinct annotation labels — the `R`-numbers of the request,
`F`/`F-` audit findings, `M`/`H` failure modes, `P-` kernel rows and two numbered
`SPEC` contracts. Those 55 labels occur as 87 label-and-site pairs at 77 distinct
`file:line` sites across 25 modules of `src/creib/forge/mini/`; the two counts
differ because a single line can carry more than one label. `runner.py` (14
sites), `blindspot.py` (11) and `campaign.py` (6) carry the most. None of these
labels could be looked up in this repository.

## What was recovered

Fifteen documents, byte-identical to the upstream commit: thirteen under
`docs/mini/` plus `docs/kernel.md` and `docs/failure-modes.md`. Per-file source
path, SHA-256, byte count and citing sites are in
[`../sources/mini-register-provenance.json`](../sources/mini-register-provenance.json),
written in the shape of the existing extraction record. For all fifteen,
`source_sha256` equals `destination_sha256`. The digests were verified again
after the copy into this repository. The source repository was not modified, and
no file under `src/` or `tests/` was touched by this recovery.

[`../mini/README.md`](../mini/README.md) is the one new file inside the recovered
directory. It is the only editorial content added; the recovered documents carry
no inserted note, no relinking and no reformatting.

Fifty-four of the fifty-five annotation labels now resolve to a specific entry in
a specific recovered file. Where each resolves is recorded with the label, its
first citing site and the target file and line. The large registers do most of
the work: `docs/mini/REQUEST.md` resolves 22 labels, `docs/mini/FAILURE_MODES.md`
16, `docs/mini/AUDIT_RESPONSE.md` 12, `docs/mini/SPEC.md` two, and `kernel.md`
and `failure-modes.md` one each.

## What the recovery does not close

The fifteen files close every citation that runs from `src/` into the register.
They do not close every reference the register makes. The recovered text names
nine further h-EPI documents that were not recovered — `ARCHITECTURE_SPACE.md`,
`CONFOUNDS.md`, `cycles.md`, `what-the-records-refute.md`, `how-it-works.md`,
`reasoning-levels.md`, `small-models.md`, `semantics-battery.md` and
`document-dependence.md` — so links inside the recovered documents can still fail
to resolve. Of those, only `docs/mini/ARCHITECTURE_SPACE.md` is also named in
this repository, at `tests/mini/test_configspace.py:37`, in a docstring that
describes what the test enumerates rather than reading the file. Nothing here
depends on those documents at run time; recovering them would be a separate
decision with its own receipt.

## The one that does not resolve: P-08

`src/creib/forge/mini/conformance_kernels.py:9` describes the kernel table in
`docs/kernel.md` as "P-01 to P-08, R-01, R-02". The recovered `kernel.md`
contains nine P-rows — P-01 through P-07, then P-09 and P-10, written out of
numeric order — and no P-08 and no note of a gap. The upstream file at that
commit is the file recovered here, so this is a stale range citation written
upstream, not a loss in extraction or in this recovery.

The corrective action is documentation, recorded as SRC-002 in
[`../errata/sources.md`](../errata/sources.md) and in
[`../mini/README.md`](../mini/README.md). The engine file is not edited: it is
frozen, its bytes are pinned by plan `runtime_files` maps, and the citation is
wrong about a range, not about which document to read.

## Extraction fidelity of the engine this register describes

The recovery is only useful if the code it documents is the code the register
was written against. Of the 29 files under `src/creib/forge/mini/` listed in
`extraction-provenance.json`, 27 are byte-identical between source and
destination. The two that differ, `common.py` and `openkernels.py`, are both
named in that file's own `modified` list and explained in its
`extraction_changes`: schemas and policies moved under package data for normal
installation, and the advertised conformance module list narrowed to the seven
support modules actually shipped. Across all of `src/creib/`, exactly four files
were mechanically edited at extraction — those two plus
`conformance/__init__.py` and `conformance/common.py` — and all four are
declared. No undeclared source edit was found.

Re-hashing every one of the 195 recorded destinations against the current working
tree, 194 still match. The exception is `tests/mini/test_audit_findings.py`,
which matches `HEAD` but not its recorded `destination_sha256`; it was changed by
a later committed change in this repository (`e63f8d5`, "Freeze H004 wave 3 exact
dependency-ready inputs"). That is a post-extraction repository change, not
working-tree drift, and it is a test rather than engine code. It is noted here
because the extraction record does not yet carry that disposition.

## Interpretation: the v1.3 gap is a design decision

The facts above are mechanical. What follows is interpretation.

[`../../PURPOSE.md`](../../PURPOSE.md) and
[`../SEMANTIC_GUIDE.md`](../SEMANTIC_GUIDE.md) both record that Mini uses kind
records and does not implement all of harness v1.3's epistemic graph semantics,
and both call that a difference to analyse rather than a conformance claim. The
recovered register settles what kind of difference it is.

Mini was never specified against v1.3. The string `v1.3` and the title of that
specification occur nowhere in the fifteen recovered documents. Mini's
obligations are the R-numbers of `docs/mini/REQUEST.md`, which declares itself
the authority for everything else under `docs/mini/`; `DESIGN.md` names
`REQUEST.md` as its authority, and `SPEC.md` is written afterwards from the code
that exists and passes its tests. That chain — `REQUEST.md` → `DESIGN.md` →
`SPEC.md` — is closed, and no clause of it points outside the register.

The missing status machinery is refused on purpose. `DESIGN.md` §13, the section
naming what the design does not attempt, states "No status, no standing, no
elimination. The prototype produces artifacts and measures; nothing is accepted,
refuted, or ranked." `SPEC.md` states "Nothing decides anything is true, or
better. No artifact stands or falls," and records that `compare` refuses even to
be asked for a score. `REQUEST.md` R27 requires exactly that of the compare
command.

So the gap between Mini and v1.3 is a design decision that predates this
repository and is written down in Mini's own authority, not erosion of a
capability Mini once had or claimed. Two consequences follow. An experiment that
wants status, standing or elimination must build it outside Mini and say so; it
cannot be described as restoring something Mini lost. And a criticism of Mini for
lacking v1.3 adjudication is a criticism of a design that declined it, which has
to argue against §13 rather than report a shortfall.

This settles the provenance of the absence. It does not establish that declining
status machinery was the right decision for the present research, and nothing
here licenses treating `compare`'s refusal to rank as itself an epistemic result.
