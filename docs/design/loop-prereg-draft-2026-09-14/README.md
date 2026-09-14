# The L001 pre-registration bundle — a DRAFT, and not a pre-registration

This directory is published by `REC-20260914-AA` as **recoverable work in progress**. It is
the draft of a pre-registration for the automated end-to-end harness loop's first cycle. It
is **not** a pre-registration, nothing in it is registered, and no run is authorised by any
sentence in it.

This README is the only file here written by the publisher. The other eight are the draft's
own bytes, unchanged.

## Why it is a draft and not a registration

A pre-registration in this repository is **minted** — at the loop's `S0 PREFLIGHT` step,
against the tree that exists at that moment, with every pin re-derived from that tree's own
bytes and folded into a `loop_plan_id` that is then frozen. Nothing of that has happened.
These files were written against a scratchpad clone, and the loop has **never been run**: no
driver exists, no cycle has executed, and no plan has been minted at any commit on any ref.
A file that says `PREREG` is not a pre-registration until the mint records it, in the same way
that a plan body is not a plan until its identity is fixed.

## The pins in this bundle are known stale

Stated so that no reader re-uses a digest from these files.

- **`STANDARD_BODY_SHA256` is stale by two generations.** Every occurrence of it in this
  directory predates two moves of the standard body. It went to
  `6c894deb851982bf7b5e7317066896a36c4b5898308519c012a3cd1ef5100fcb` under wave-1 hardening,
  and then to **`a9007dc73c748cfff974a1a3d77098d380ec153b1b8cf93f513cafa3ea0572d7`** at the
  wave-2 `cal-01` repair (PR-06). The **ceiling** digest did not move in either. See
  `../loop-impl/WAVE2-INTERFACE.md` §9.
- **`VALIDATION.md` describes a bundle that no longer sits beside it.** Its §4 table pins
  `config.json` at `46495a6fa0ee5667b6ba5128adbaee9062ed5b6637310bb44b12efdf14c0da90`; the
  `config.json` published here digests to
  `081dd939663156aa3969f3b000fcb0ca4b07086ab4340b0156057903b45b5110`. Its
  `calibration.json` (`9ca9ad04…`) and `obligations.json` (`2913693a…`) pins do still hold
  against these bytes, and its demonstration `loop_plan_id` (`cc7c137f…`) is a demonstration
  value only. This is blocker **PR-08**. `VALIDATION.md` must be **regenerated before** the
  bundle is published as a registration, never after it.
- **`validate.py` no longer runs against the implementation it validates** (PR-07). The
  module side of that mismatch is repaired; the bundle's harness is not.

The file digests of this directory's eight draft files, taken at publication, are:

| file | sha256 |
| --- | --- |
| `PREREG.md` | `c04c2092f672b52572ea98a60575e3405c5072f6b381b9b55a30cb3f7dcd16d6` |
| `config.json` | `081dd939663156aa3969f3b000fcb0ca4b07086ab4340b0156057903b45b5110` |
| `obligations.json` | `2913693abce664af387f1683c7cbfd622043a697343a6d415d89a8179d3652d6` |
| `reading_set.json` | `ef8c62a5ad6148c4bf676fadabba1ae0504babef26b4f793cce7d80ff37c728e` |
| `calibration.json` | `9ca9ad04672e99becc19096e3de4d4010d9f21c700a979695ef034f9c19aae95` |
| `validate.py` | `fd8015261e86cf34cf87f1fd576fd28fb98cc635a7889ee7cb63cb5dde41f25e` |
| `VALIDATION.md` | `62f2b71a90488852ed1b4e4af17138e22b77f60c31c0fb222326b085d257c413` |
| `REVIEW-PREREG.md` | `a0b6ce60f439b3512fdecfb55c1e856c69d32f77782160fe16bd7a35596f7c2d` |

These are the digests of the draft, recorded so that a later revision is visible as a
revision. They are **not** registration pins and nothing folds them into an identity.

## Thirteen blockers, all open as bundle edits

`REVIEW-PREREG.md` is the bundle's own adversarial review and it lists **PR-01 through
PR-13**. Every one of them must be closed before any live run. **Not one bundle edit is made
by this publication**: the eight files are published exactly as the draft left them, because a
publisher that quietly edits the bytes it was asked to publish is not publishing them.

Five of the thirteen have a **code half**, and that half is repaired and recorded in
`../loop-impl/WAVE2-INTERFACE.md` §10 — **PR-02** (`obligations.pin()` keeps the file digest
and a new `canonical_pin()` returns the canonical-body digest, so neither value is anonymous),
**PR-05** (`no_scoring_key` now reads headings and GFM table header rows of the rendered files,
with a declared exemption for quoted material), **PR-06** (`cal-01` rebuilt on the referring
region alone, which is what moved `STANDARD_BODY_SHA256` the second time), **PR-07**
(`PIN_INVALID` now names what a caller must supply) and **PR-12** (`types` is the sole owner of
the `blocked:` spelling). **The bundle half of each of those five is still owed**, and each is
named as a "bundle consequence" in that section. The remaining eight — **PR-01, PR-03, PR-04,
PR-08, PR-09, PR-10, PR-11, PR-13** — are bundle edits with no code half and are wholly owed.
Among them: `calibration.json` carries a forbidden `scoring` key and would fail its own
protected obligation on its first registration (PR-01); `p7` and `o5` as written are not the
predicates the program evaluates (PR-03, PR-04); the two mandatory guard-rail accounts are
provisional and one is arithmetically wrong (PR-09); the run's resource conditions are not
pre-registered (PR-10); `publish_ref` is null and the ruling-2 branch deviation appears nowhere
in the bundle (PR-11); and the `unread` inventory contradicts itself, 11 against 12 (PR-13).

## What this directory does not do

It **authorises no provider call**. It **registers nothing**, **pins nothing**, and
**adjudicates nothing** about bearing, use or creativity. No cell of any reading is filled by
anything here, and no number in these files is evidence about the bare, native, matched,
`mini_prose` or `mini_fcl` arms. The next authorised work on this bundle is the revision
against `REVIEW-PREREG.md`, which is a decision with its own receipt.
