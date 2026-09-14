# Mini's requirement register — recovered source

This README is the only file in `docs/mini/` written in this repository. Every
other file here, together with [`../kernel.md`](../kernel.md) and
[`../failure-modes.md`](../failure-modes.md), is recovered **verbatim** from
[AHepi/h-EPI](https://github.com/AHepi/h-EPI) at commit
`b2a33283dc1e05fb83c3357b26e2cc12115f6b6c` — the same commit
[`../sources/extraction-provenance.json`](../sources/extraction-provenance.json)
names for the frozen engine under `src/creib/forge/mini/`. The recovered bytes
are unchanged: no reformatting, no relinking, no editorial note inside any of
them. Per-file source paths, digests and citing sites are in
[`../sources/mini-register-provenance.json`](../sources/mini-register-provenance.json);
the recovery itself is reviewed in
[`../reviews/mini-register-recovery-2026-09-14.md`](../reviews/mini-register-recovery-2026-09-14.md).

The engine cites these documents by path and by annotation label from its own
comments and docstrings. Before this recovery those citations were dangling: the
register was never extracted with the code.

## Mini's own authority chain

These documents are Mini's authority, and they are self-contained:

`REQUEST.md` → `DESIGN.md` → `SPEC.md`

`REQUEST.md` states it directly: "This file is the authority for everything else
under `docs/mini/`. Nothing in `DESIGN.md`, `SPEC.md`, or `DELIVERY.md` may claim
an obligation that does not trace to a number here." `DESIGN.md` names
`REQUEST.md` as its authority and is the design decided before the build;
`SPEC.md` names `REQUEST.md` and `DESIGN.md` and is written afterwards from the
code that exists and passes its tests.

## These documents are not harness-spec-v1.3

Mini was never specified against
[`../sources/harness-spec-v1.3.md`](../sources/harness-spec-v1.3.md). The string
`v1.3` and the title of that specification do not occur anywhere in the fifteen
recovered documents. The register's own obligations are the R-numbers of
`REQUEST.md`, not v1.3 clauses.

The absence of v1.3 status machinery from Mini is a stated design decision, not
an implementation shortfall. `DESIGN.md` §13, "What this design does not
attempt":

> No status, no standing, no elimination. The prototype produces artifacts and
> measures; nothing is accepted, refuted, or ranked.

`SPEC.md`, part one:

> **Nothing decides anything is true, or better.** No artifact stands or falls.
> Two runs can be set side by side, and `compare` will not order them, total
> anything, or say which is better — it refuses even to be asked for a score.

Read a v1.3 comparison against Mini as a difference between two designs, as
[`../../PURPOSE.md`](../../PURPOSE.md) already requires, not as erosion of a
conformance claim Mini never made.

## Recovered files

Byte counts and digests are of the recovered bytes as published here; "citing
sites" counts the places in `src/creib/` that cite the document, by path or by
an annotation label it resolves.

| File | SHA-256 | Bytes | Citing sites |
|---|---|---|---|
| `docs/failure-modes.md` | `f4081147d666c24bf43176d7b502dbe98c6348474c84d438f5f66cae2eb2bf76` | 103,426 | 3 |
| `docs/kernel.md` | `4296377d8feb21deba44dc5f2fccab160e2f6480c3c3d8f38fc80f02af203a62` | 18,268 | 3 |
| `docs/mini/ARCH_SWEEP.md` | `def4dad3d3ec083fe09cb480c3f3b43533dd38609b3b2e0f85ee1ec49839f810` | 12,026 | 0 |
| `docs/mini/AUDIT_RESPONSE.md` | `20c1bb3ea55c7736b585e9eda30f7754e2019eb053e5601500617e44279c5164` | 16,519 | 21 |
| `docs/mini/AUTONOMY.md` | `93bc3bd2a816a2413dcce90e59f3fbb92da2501a36b831f84a91995b4846c7d8` | 8,924 | 2 |
| `docs/mini/BUILD_TEST.md` | `f5be5b21b901505108978c260e0ee5a4a8b262febac0efa8aa09d96b67794e1e` | 16,151 | 1 |
| `docs/mini/CONFIG_MAP.md` | `bcc5a0e10d421ed7502cbe7af324452c2e1090148d45dc8a445bbb6a86b805d2` | 10,309 | 0 |
| `docs/mini/DELIVERY.md` | `9ef283aef89e09530549f5e418fadf784a33e52e727ee39599ded07ce8401c7e` | 23,142 | 0 |
| `docs/mini/DESIGN.md` | `36598df55e1f8d6cd0430462514d630c6a60da90a4b83f90a7509111055ad287` | 47,654 | 0 |
| `docs/mini/ERRATA.md` | `4f4a96fe37e0f42f2e789b06fd17040472abd43478eb5f1569a3102f18987ee7` | 10,521 | 1 |
| `docs/mini/FAILURE_MODES.md` | `f9360cb726298d5cb74543655e955a688ba82b5e175cb5c515830034835a1309` | 56,272 | 49 |
| `docs/mini/PIPELINE_MATH.md` | `36518db884c9cd1c552e7ce0fa0ea8a724aebf20e7c05ffa5e8b46534e3d095c` | 13,542 | 1 |
| `docs/mini/REQUEST.md` | `6ddfc11c8c528745420748d9a3cb79257ebc95ec451f23a6f0cde1dd7983bd79` | 35,355 | 28 |
| `docs/mini/SPEC.md` | `92832c1e6db90747c88539886c151f0c20c00f6b89f4cc8f7d17d61c4ef05bd2` | 41,668 | 3 |
| `docs/mini/USE_TEST.md` | `09948c2ba311121e123adb00dc0f6501a2ff58f03b23836e70b1508ba0d12eb1` | 23,504 | 2 |

`ARCH_SWEEP.md`, `CONFIG_MAP.md`, `DELIVERY.md` and `DESIGN.md` carry no direct
citation from `src/`; they are recovered because the cited documents depend on
them and because `DESIGN.md` is a link in the authority chain.

## What is not here

The recovered files name further h-EPI documents that were not part of this
recovery: `ARCHITECTURE_SPACE.md`, `CONFOUNDS.md`, `cycles.md`,
`what-the-records-refute.md`, `how-it-works.md`, `reasoning-levels.md`,
`small-models.md`, `semantics-battery.md` and `document-dependence.md`. Links to
them inside the recovered text do not resolve here. Only one is also referenced
from this repository — `docs/mini/ARCHITECTURE_SPACE.md`, from the docstring at
`tests/mini/test_configspace.py:37` — and that reference is documentary, not a
filesystem dependency. Recovering any of them is a separate decision.

## One citation does not resolve: P-08

`src/creib/forge/mini/conformance_kernels.py:9` describes the kernel table in
`docs/kernel.md` as "P-01 to P-08, R-01, R-02". The recovered `kernel.md` has no
P-08 row. Its P-series is P-01, P-02, P-03, P-04, P-05, P-06, P-07, P-09, P-10 —
nine rows, written out of numeric order, with no gap note.

This is a stale range citation in the upstream source, not a loss in this
recovery: the byte-identical upstream file has the same nine rows. Fifty-four of
the fifty-five annotation labels cited from the frozen engine resolve to a
recovered entry; P-08 is the one that does not. The frozen engine file is not
edited to correct the range — it is frozen, and its bytes are pinned. The defect
is recorded in [`../errata/sources.md`](../errata/sources.md) as SRC-002.
