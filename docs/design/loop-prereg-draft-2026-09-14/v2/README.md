# The L001 pre-registration bundle, revision v2 — still a DRAFT, and still not a pre-registration

This directory is published by `REC-20260914-AE` as **recoverable work in progress**. It is the
**second draft** of a pre-registration for the automated end-to-end harness loop's first cycle. It
is **not** a pre-registration, nothing in it is registered, and no run is authorised by any sentence
in it.

The v1 draft is `../` and its bytes are **unedited** — a superseded draft is the evidence of what
was superseded. This README is the only file here written by the publisher; the other twelve are the
revision's own bytes, unchanged.

## What changed since v1

The revision answers `REVIEW-PREREG.md`, the bundle's own adversarial review, and closes every one
of its thirteen numbered blockers plus the twelve further items the review raised, applying them in
the review's own recomputation order — standard body (clone-side, verified and not edited) →
`calibration.json` → `config.json` → `obligations.json` and `reading_set.json` → `PREREG.md` →
`validate.py` → `VALIDATION.md`. Mechanically: the forbidden `scoring` key that would have failed
the bundle's own protected obligation at its first registration is renamed `error_rule` and restated
at **panel** grain (PR-01); `PREREG.md` now publishes **both** digests of `obligations.json` with
the attribution of each, the canonical-body digest it declares and the file digest that enters
`loop_plan_id` (PR-02); `validate.py` builds its pin map from `types.PINNED_SOURCE_PATHS` itself
instead of the one-entry map that made it pass vacuously, and now runs
`contracts.assert_no_scoring_keys` over all four bundle JSON documents (PR-07, PR-01);
`VALIDATION.md` is regenerated wholesale from the run it transcribes rather than describing a bundle
that no longer sat beside it (PR-08); the `blocked:` spelling and its tenth code are reconciled with
`types` (PR-12); the `unread` inventory is re-derived from the published bytes and is **twelve**, not
eleven (PR-13); and the placeholder receipt id that was a live published id is replaced by one that
cannot be minted (PR-18). By judgement: `p7` and `o5` were changed **in the bundle and not in the
program**, so that each now reads what `no_edges_on_studied_nodes` and `audit_in_force` actually
evaluate (PR-03, PR-04, PR-16); the three guard-rail accounts — `judge_err_max`, `streak_max`,
`audit.period` — are settled, with two false premises withdrawn in the accounts themselves (PR-09);
the run's resource conditions and the seat evidence are declared as bounds in a new §2a, with the
32768/600 evidence named **only** to say it does not transfer to this run's conditions (PR-10,
PR-14); `publish_ref` and the ruling-2 branch deviation are stated (PR-11); clause 1 is corrected to
FW5's held-then-failed form, the bundle's prose having been the half that was wrong (PR-15); and the
C001 leg carries its **shape** rather than the wave-1 pass's figures, because occurrence-02
postdates the clone and the run must recompute them (PR-20). `CHANGES-PREREG.md` records every edit
with the check that preceded it, and its metric-creep re-read (ruling 7) reports that the two
findings §B failed now pass, that the third is accounted, and that **no class-(iii) number — no
score, rank, progress meter or success rate — appears anywhere in the revised bundle**.

Four files are new here and have no v1 counterpart: `CHANGES-PREREG.md`, `CLONE-PATCH.md` and the
`bundle-worksheet.md`/`.json` pair. `REVIEW-PREREG.md` is carried over **byte-identical** to v1
(`a0b6ce60…`), because a review is not edited by the revision that answers it.

## Six things the driver integration owes this bundle

`CLONE-PATCH.md` is the list, and **not one of its items is done**. Two are **required** — the
bundle does not validate against a clone that lacks them:

1. **Something must read `calibration.json`.** No module does; `audits.build_calibration_set` seeds
   itself from `standard.CALIBRATION_ANCHORS`. W5-DRIVER must compute `sha256(calibration.json)` at
   S0, write it into `plan.json` as `calibration_sha256`, and copy it onto every `AuditReport` body,
   where `obligations.audit_in_force` already reads it. Without this, `o5` is unsatisfiable by the
   program that evaluates it.
2. **`plan.json` must also pin `audits.CALIBRATION_EXCHANGES_SHA256`.** The five constructed
   exchanges that make the anchors' ground truth true by construction are pinned by `audits` and by
   nothing in the plan identity, so a change to them would not move `loop_plan_id`.

Four are **declared gaps** that the bundle works around and names; declining one leaves the bundle
correct and the named consequence standing:

3. `types.AuditConfig` has no `period_account` field, so the settled account for `audit.period = 2`
   is pinned by `reading_set.json`'s digest rather than by the config block of `loop_plan_id`.
4. `types.LoopConfig` cannot carry the resource conditions, so `reading_set.json:resource_conditions`
   declares them and `validate.py` asserts each against the `roles` constant that will be sent.
5. **The guard-block streak counter is defined and unimplemented.** `decide.Instrument.block_streak`
   is a declared integer; W5-DRIVER must count consecutive blocks per role, in dispatch order within
   the reading arm, reset by any non-block outcome — and PREFLIGHT must assert that this is the
   definition in force, because any other definition makes `config.audit.streak_max_account` a false
   account of the number beside it, and that account is inside `loop_plan_id`.
6. **The complete `unread` inventory must be produced by W4-READER** — every cell nothing read,
   including the twelve C001 occurrence-01 juxtapositions and the ones the reading set never named.
   `o7`'s trichotomy and `p12`'s non-collapse clause both rest on that inventory being complete.

## Every pin here is to be re-read at PREFLIGHT

Nothing in this directory is a registration pin. The three clone-side values the bundle quotes —
`standard.STANDARD_BODY_SHA256` `a9007dc7…`, `standard.CEILING_SHA256` `1e26be08…` and
`audits.CALIBRATION_EXCHANGES_SHA256` `91c29e1e…` — were read at the review against the wave-4
clone, and the standard body moved **three times** inside the review window
(`b4dc7f6a…` → `6c894deb…` → `742c2a0b…` → `a9007dc7…`). They are to be **re-read at S0 PREFLIGHT
against the tree that exists then**, after the loop package is frozen and before `plan.json` is
written. A plan identity minted over a body that has since changed is the single failure this
apparatus exists to prevent.

The file digests of this revision, recorded so that a later revision is visible as a revision and
so that a reader can tell these bytes from v1's:

| file | sha256 |
| --- | --- |
| `PREREG.md` | `0dbfae63f8f49b583e31e341c6149f4b6352a7497e387907fc5ef2867739ae28` |
| `config.json` | `63879991dd632f016e9917ab336fca872b29f16a527e4b67621e189478c38ec0` |
| `obligations.json` | `910282bb43de93bd9fdd1498ec279a177fcaee3b815ebdc8e8a6eea4a9179045` |
| `reading_set.json` | `929868e8869788c8483029c1a36246b1cc9429f7fb90f0ab3934b80795e238e7` |
| `calibration.json` | `eaf41d3eed98f7ba839ab604367c3daf3f92d7cf07a658694bd9cdd5539a5e38` |
| `validate.py` | `5f47c46bb2e80264ae56b316a4ab17b4162052c055150875cf7599247ea9d265` |
| `VALIDATION.md` | `42b6e4f095a14634695356971110b6eb6c384238fd6d0065c866c76e658592e8` |
| `REVIEW-PREREG.md` | `a0b6ce60f439b3512fdecfb55c1e856c69d32f77782160fe16bd7a35596f7c2d` |
| `CHANGES-PREREG.md` | `6d6264b66338c57531ad109ae54705e7f0607452a47759081ad5a60409e7ae25` |
| `CLONE-PATCH.md` | `1e598cb7352c14dbbdb3ef0de6f9bee6b4bbcbe1e7400992497aa1c4d37c030d` |
| `bundle-worksheet.md` | `7a67ae5dc818def8ea27f4c41b89ebd91b11e1a445c66020c52bbd21b41905da` |
| `bundle-worksheet.json` | `6e88495d81bbb16206f10611cb405025b7cec4bbd8909ba4f6c85e3b75d5eff0` |

`obligations.json`'s **canonical-body** digest is
`3bda592108ac11aee8fe34da5b4317001156d18417af397ee6957f310ce55900`; it differs from the file digest
above on purpose, and `PREREG.md` §3 says which is which and why.

## What this directory does not do

It **authorises no provider call**. It **registers nothing**, **pins nothing**, and **adjudicates
nothing** about bearing, use or creativity. No `loop_plan_id`, no receipt id and no timestamp is
minted by anything here — `PREREG.md` carries a receipt placeholder that cannot be minted, precisely
so that no reader mistakes it for a record. No cell of any reading is filled by anything here, and no
number in these files is evidence about the bare, native, matched, `mini_prose` or `mini_fcl` arms.
The next authorised work is `CLONE-PATCH.md` inside the W5-DRIVER integration, and then a dry run
with zero provider calls — each a decision with its own receipt.
