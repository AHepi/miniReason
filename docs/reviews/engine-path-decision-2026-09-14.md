# The engine path: what was vendored, what was designed and not built

Root decision record, REC-20260914-M, 2026-09-14.

The upstream facts this rests on are in
[`upstream-deepreason-inventory-2026-09-14.md`](upstream-deepreason-inventory-2026-09-14.md).
The design that was not built is carried verbatim at
[`../design/engine-design-of-record-2026-09-14.md`](../design/engine-design-of-record-2026-09-14.md).
The inventory, the vendoring map, three candidate designs, three judgements and
the synthesized design were produced by delegated Opus 5 agents under this
session's orchestration mandate; the decision below is this session's.

## Finding

Harness spec v1.3 is implemented in full upstream — every section, with a
5,215-test gate last recorded green. This repository holds the spec document
byte-identically and none of the machinery.

Mini was never specified against it. Mini's own authority chain is closed:
[`../mini/DESIGN.md`](../mini/DESIGN.md) §13 — "No status, no standing, no
elimination. The prototype produces artifacts and measures; nothing is accepted,
refuted, or ranked." That is a design decision recorded upstream of this
repository, not a capability lost here.

H005 is running live on Mini under a frozen protocol. So the repository's
research question — whether a criticism returns to operative use — is at present
asked with no mechanical notion of a criticism *landing*: no att edge, no
warrant, no label, nothing that distinguishes a criticism taken up from one
written down beside the thing it criticises.

## Decision 1 — executed

Vendor the v1.3 P0 core from `AHepi/DeepReason@9607fba6` as
`src/deepreason_core/`: ontology, att/dep edge construction with the three v1.3
closures, the grounded and support passes, the append-only event log, the object
store, and the P0 slice of the harness — about 2,000 lines after documented cuts
back to v1.3-exact. The cuts are deletions of v1.4+ material, not rewrites: 75 of
79 object-store schema rows, the typed event payloads and LLM record hierarchy,
the fourth (source-artifact) att closure, the extra `Rule`, `ProvenanceRole` and
`SpawnTrigger` members, and the RunManifest/workflow/bridge/scratch branches of
the harness. It adds one runtime dependency, `pydantic>=2.7`, and carries
upstream's MIT licence. Provenance goes in
`docs/sources/deepreason-core-provenance.json`, in the shape of the existing
h-EPI extraction record, recording `source_sha256` and `destination_sha256` per
file so every edited file is visible as edited.

Its purpose is narrow and offline. `tools/import_h005.py` replays one H005
occurrence's hash-pinned evidence into a spec graph and reports labels, edges,
warrants and residue. It makes no provider call, changes nothing in the live run,
and adds no arm. Statuses it produces are mechanism bookkeeping, never semantic
verdicts: `PROTOCOL.md:62` reserves substantive review of outputs to root, and
this instrument does not touch that reservation.

The core and the importer are written but **not published**. They will be
published under their own receipts, or not at all.

## Decision 2 — not executed, preserved

The alternative was a fresh, vendor-free `src/deepreason/` engine: 25 modules in
8 waves, jsonschema-only with no new dependency, and a float-free canonical
profile reusing this repository's own encoder. Two of three judges ranked the
design it is built on first. It is published as the design of record, unbuilt,
because:

- DeepReason already implements P1–P6. Building a second engine here would
  re-derive, at much greater cost, what exists and is tested.
- A second engine is a maintenance surface the owner has not asked for.
- H005 is the owner's live protocol. A session-authored driver that competes
  with it is not a contribution to it.

## Governance

`AGENTS.md:7` authorises extraction from `AHepi/h-EPI` and says nothing about
`AHepi/DeepReason`. The vendoring therefore proceeds under this session's user
instruction — the owner supplied the spec and instructed continuation — and not
under a standing authorisation. Three containments make it reversible: it is
confined to one package outside `src/creib/`, so `runtime_files` is unchanged and
every frozen plan still verifies; it touches nothing under `experiments/`; and it
arrives in a single publication commit that a revert undoes. The owner may
instead adopt Decision 2, or neither.

## The judgements

Three delegated judges scored three candidate designs out of 35 across spec
fidelity, governance compliance, parallel buildability, determinism and
testability, path to live P1, research value and risk.

| Design | Spec-fidelity lens | Engineering-lead lens | Principal-investigator lens |
|---|---|---|---|
| purist | **30** | **28** | 25 |
| research | 28 | 27 | **28** |
| reuse | 22 | 24 | 23 |

Winners: purist, purist, research. The three headline objections, kept because
they survive the decision:

1. **Governance gate.** Two judges made the authorisation question the first
   fatal flaw against the vendoring designs: `AGENTS.md` authorises h-EPI, not
   DeepReason, and a design whose whole schedule is ports has no critical path if
   authorisation is refused. Decision 1 answers this by naming the instruction it
   relies on and by keeping the package revertible — not by claiming an
   authorisation that does not exist.
2. **Identity divergence.** The cheapest design computed artifact ids as
   `sha256(domain + NUL + canonical(payload))` rather than §1's
   `sha256(canonical(content_ref, codec, interface))`, so no id it produced would
   ever agree with the spec or with any other implementation.
3. **Prose-arm confound.** Registering free-prose artifacts "with an empty
   interface" leaves them undemarcated, minting no edges, while the FCL-1 arm
   gets validity nodes, warrants and a live dependence cascade. That makes the
   arms differ in mechanism rather than in notation, which is the opposite of the
   declared control, and it is exactly the substitution `PURPOSE.md` forbids:
   syntax and executable tests cannot be made the definition of bearing.

## What would reopen this

- Owner authorisation, either way: to keep the vendored core, or to build
  Decision 2 instead.
- H005 completing three cycles, at which point the import becomes a multi-cycle
  question rather than a single-occurrence one.
- A decision to run *new* occurrences on spec machinery rather than replay
  finished ones into it. That is a different decision from this one, with a
  different claim ceiling, and it is not taken here.
