# The pre-registration bundle, revision v3 (L002) — still a DRAFT, and still not a pre-registration

This directory is published by `REC-20260914-AK` as **recoverable work in progress**. It is the
**third draft** of a pre-registration for the automated end-to-end harness loop's first cycle. It is
**not** a pre-registration, nothing in it is registered, and no run is authorised by any sentence in
it. `../` is v1 and `../v2/` is v2; both are **unedited**, because a superseded draft is the
evidence of what was superseded. This README is the only file here written by the publisher; the
other twelve are the revision's own bytes, unchanged.

## Why there is a v3

v2 was frozen into the first live run, **L001**, which stopped at the first SEND having spent
**zero provider calls**. `config.occurrences` named
`experiments/diagnostics/H005-open-prose-commitments/occurrence-01`, a published, closed study that
carries no `arms.json` — so runner v2's `verify()` raises — and a prepared-but-never-sent
`waves/wave0006.json` of five `daily`/cycle-2 coordinates with requests and no attempts — so
`pending_wave()` never clears and `prepare_wave` would refuse `PREPARED_WAVE_PENDING`.
`REC-20260914-AJ` repaired the driver so S1 refuses `OCCURRENCE_NOT_DISPATCHABLE` **before anything
is published**, and said in terms that what had to change was the pre-registration.
`REC-20260914-AI` is now closed as an operational failure with the run directory committed
unchanged. **v3 is that change, and it is L002 with a new `loop_plan_id` — not an amendment to
L001**: the occurrence set, the reading set and `max_calls` all move, and any one of those alone
mints a new identity.

## The decision v3 makes, and the fact that forced it

`config.occurrences` is **three lists at once** in `tools/auto_loop.py`: the dispatch list (S4
`prepare_wave`, S6 `send_round`), the import list (S8 `graph_import_h005.import_occurrence`) and the
use-table list (S9 `use_relation_h005.build_use_table`). S1 verifies every member of it. Checked
across the published trees while writing this revision: **`arms.json` is absent from every published
occurrence of both studies** — H005 occurrence-01, C001 occurrence-01 and C001 occurrence-02 — and
the only occurrence in the repository that carries one is F002 occurrence-03, written by the newer
runner. There was never a declarable published occurrence to choose. The ledger's three ways out and
their disposition: writing the missing `arms.json` is **refused** (it edits published material;
`p11` and AGENTS.md forbid it); a reading-only run is **unavailable** (`LoopConfig` refuses an empty
`occurrences`); a different occurrence is **taken**, and it is a new one.

| leg | what it is | cost |
|---|---|---|
| **dispatch** | `experiments/diagnostics/C001-contrast-triple/occurrence-03`, a **new** occurrence of the C001 contrast study under C001's frozen `plan_id 328b9452…`, declared before dispatch exactly as F002 occurrence-03 was (ruling 14), staged before S0 | 20 calls |
| **marking** | the 16 declared cells — 4 within-ORIGINAL baselines, 12 cross-case juxtapositions — over **published, closed** `…/occurrence-02`, through its published `comparison.json`; design §3(b)/§3(c) register those bytes as `E_cell` with `provenance.role = IMPORT` and open one `C_open` per cell before any call | 108 calls |
| **H005 rows** | none declared; the 22 published rows are named `unread` | 0 |

**Nothing is marked over the new occurrence's material, and the reason is pre-registered rather than
discovered.** S0's `seal_baselines` reads the contrast occurrence's `comparison.json` and
`_contrast_cells` skips an occurrence that has none; a new occurrence has none until
`tools/contrast_triple_study.py` builds one after its dispatch closes, and **no step S0–S15 builds
it**. Equally, occurrence-03's own use-table rows reach the run only at S9, from commitments S6 has
not yet sent, and a reading key must be named before first look and is self-tested at PREFLIGHT — so
those rows cannot be pre-registered either. They are `unread` under `o7`. **L002 therefore dispatches
material for a successor pre-registration to read, and itself reads and marks published bytes only.**
That is a smaller claim than L001's and it is the honest one available.

`max_calls` 396 → **174** = 0 (4 baselines) + 108 (12 cross-case × 9) + 0 (no row leg) + 46 (one
audit window) + 20 (occurrence-03 dispatch). **Whose budget the dispatch calls are: both, and the
record says both** — the C001 study's own, since occurrence-03 is an occurrence of C001 under C001's
plan_id whose arms, cases, replicates, seeds and endpoint scope its staging receipt fixes before
dispatch; **and** inside this loop's `max_calls`, because the loop's driver issues them in-process
and a bound that does not bound everything the process spends is not a bound (ruling 7).

`p13` is new (|P| 12 → 13): occurrence-03's `material.json`, `arms.json` and frozen `plan.json` stay
at the digests pinned at PREREGISTER and the occurrence declares C001's frozen `plan_id`. `p11`
gains one **named** exception: runner v2 writes the dispatch leg's records under occurrence-03 and
under no other path. `o1` now holds **vacuously** and says so — a vacuous `o1` is no evidence about
any of the 22 rows.

## The staging precondition, stated as a precondition

`…/occurrence-03` **does not exist, and this bundle does not create it.** No step S0–S15 creates an
occurrence — `prepare_wave` prepares a *wave inside* an initialized one — and the driver's only
stager is `dry_run`'s `_stage_dry_run_material`, which writes **synthetic** material and must never
be pointed at a real study path. It is staged by a separately identified act with its own receipt
under C001's own §13: `material.json` + `arms.json`, then `runner_v2.initialize` to freeze its
`plan.json`, with its `dispatch_scope` fixed there. **Until that receipt exists, S1 refuses this
config with `OCCURRENCE_NOT_DISPATCHABLE`, offline, before any publication, at no cost — and that
refusal is the correct behaviour, not a defect.** `validate.py` asserts the occurrence is *absent*
for exactly that reason.

## The offline dry run was not run, and why

`dry_run` calls `_stage_dry_run_material(root, cfg)`, which writes `synthetic.material_document`
and `synthetic.arms_document` into every path `cfg.occurrences` names and calls `runner.initialize`
on them. Pointed at this config it would **fabricate synthetic C001 material at a real study path
under a real plan_id**. It cannot take this bundle and it was not run. The machinery's offline
exercise is `docs/design/loop-impl/DRYRUN-RECORD.md` (exit 0, three cycles, zero live transports);
this bundle's offline evidence is `validate.py`.

## What was checked, and by what

`validate.py` from this directory with `PYTHONPATH` pointing at the **published** driver
`/home/user/miniReason/src`: **`ALL CHECKS PASSED`, exit 0**. `VALIDATION.md` is the transcript,
regenerated wholesale rather than patched, with the digest table for every file here, both digests
of `obligations.json`, the six source pins and the three clone-side pins each carrying *to be
re-read at PREFLIGHT after the clone freezes*. Whole suite at this commit: `Ran 3129 tests`, `OK
(skipped=2)` — **no code was added by this revision**. Credential scan over the staged paths: key
**names** only, no value, no assignment form, no secret-shaped token; neither `DEEPSEEK_API_KEY` nor
`OLLAMA_API_KEY` is set in the publisher's environment.

## What this bundle still does not do

It mints nothing: no `loop_plan_id`, no receipt id, no run timestamp — the labelled placeholders
(`REC-YYYYMMDD-X`, `<minted at S0>`) stand. It claims nothing about any arm, model, family, account
or cell, and ruling 7 holds over every number in it; `CHANGES-PREREG.md`'s metric-creep re-read
lists each number with the sentence that guards it and reports no class-(iii) quantity anywhere.
`CLONE-PATCH.md` carries what the driver must still do — most sharply, that an audit report must
carry `calibration_sha256` for `o5` to be discharged, and that nothing in S0–S15 stages an
occurrence. Publication is to the branch by owner mandate (ruling 2), with publication to `main`
**pending owner merge**.
