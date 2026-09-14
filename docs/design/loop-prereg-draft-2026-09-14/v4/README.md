# The pre-registration bundle, revision v4 (L003) — still a DRAFT, and still not a pre-registration

Published by `REC-20260914-AN` as **recoverable work in progress**. It is the **fourth draft** of a
pre-registration for the automated end-to-end harness loop's first cycle. It is **not** a
pre-registration, nothing in it is registered, and no run is authorised by any sentence in it. `../`
is v1, `../v2/` v2, `../v3/` v3 — all **unedited**, because a superseded draft is the evidence of
what was superseded. This README is the only file here written by the publisher.

## Why there is a v4, and what it overturns in v3

v3 was frozen into **L002**, which exited 0 at S0 and **1 at S1** with `OCCURRENCE_NOT_DISPATCHABLE`
— *offline, before S2*, so **nothing was published and nothing was spent**. Staging the C001
occurrence v3 §2d declared was then attempted and **stopped before any byte was written**, on a fact
that is not about staging:

> **Runner v2 — the driver's only dispatch seam (WAVE5 S4/S6) — verifies and dispatches only
> H005-style occurrences.** `verify()` requires `material.json` at schema
> `minireason.h005.material.v1`, a `plan.json` byte-equal to the runner's own `plan_body`
> (`minireason.h005.plan.v1`) and `manifests/<tid>.json` at their pinned digests; `prepare_wave`
> iterates `material['problems']` and its templates, cycles and nodes.

C001's material is `minireason.c001.material.v1`, indexed by endpoint, arm, case and replicate. **No
occurrence of C001 can ever verify there.** v3's `p13` was unsatisfiable as written, and its "20
calls under C001's `plan_id 328b9452…`" was impossible twice over: `contrast_triple_study.py` plans
240 calls at that id, and the twenty coordinates belong to occurrence-02's id `1d9f47ac…`.

**v3 §2c's other premise is false, and is corrected by measurement**, not by argument. Runner v2's
own `verify()`/`pending_wave()` over every occurrence in `experiments/diagnostics/`:

| occurrence | result |
|---|---|
| `F001-fork5-multifamily/occurrence-07`, `-08` | **VERIFY**, `pending_wave` `None`, `max_calls` 11, plan_ids `77aa01f4…` / `04c26f24…` |
| `F001-fork5-multifamily/occurrence-01`…`-06` | `IMMUTABLE_PLAN_MISMATCH` |
| `F002-fork5-raised-clock/occurrence-01`…`-03` | `ARM_FIELDS` |
| `H005-open-prose-commitments/occurrence-01` | `FileNotFoundError` (no `arms.json`) |
| `C001-contrast-triple/occurrence-01`, `-02` | `MATERIAL_SCHEMA` |

Published occurrences *do* verify. **They are still ineligible, and for this programme's reason and
not the runner's: they are published, and the loop never re-dispatches into or writes into a
published occurrence.**

## What v4 declares

| leg | what it is | cost |
|---|---|---|
| **dispatch** | `experiments/diagnostics/F001-fork5-multifamily/occurrence-09`, staged before S0 through runner v2's own `initialize` at **zero calls** (`REC-20260914-AM`), sharing F001 occurrence-08's frozen `plan_id 04c26f24…` | **11** |
| **marking** | the 16 declared cells — 4 within-ORIGINAL baselines, 12 cross-case juxtapositions — over **published, closed** C001 occurrence-02 via its published `comparison.json` | 108 |
| **H005 rows** | none declared; the 22 published rows are `unread`, and `o1` holds vacuously and says so | 0 |
| **audit** | one window at cycle 2 | 46 |

`max_calls` 174 → **165** = 0 + 108 + 0 + 46 + 11. Those 11 are **both** F001's own calls (an
occurrence of F001 under F001's frozen plan, its arms, problems, cycles, nodes, seed and endpoint
fixed by `REC-20260914-AM` before dispatch) **and** inside this loop's `max_calls`, because the
loop's driver issues them in-process — and the record says both.

**Why 11, and why the scope is forced rather than chosen.** The scope lives inside `arms.json`, and
the plan identity is a pure function of (repository pins, material bytes, arms bytes, scope) — so
sharing occurrence-08's plan_id **pins the scope** to `{problems: ['daily'], cycles: [1]}`; any other
scope is different arms bytes, a different plan_id, a different occurrence. Under it `call_count`
sums, per arm, the nodes the cycle admits: `bare` 1 + `mini_prose` 5 + `mini_fcl` 5 = **11**, which
is what both occurrences' frozen `plan.json` record. It is the smallest that plan admits: cycle 2
costs 15, cycle 3 costs 13, the full material envelope 156.

**occurrence-08 and not -07 as the base**, deliberately: -07's arm is `ollama/glm-5.3`, whose long
generations ruling 14 records meeting the 300 s host gateway wall at three different nodes with no
terminal record; -08's is `ollama/kimi-k3`.

**The reading and marking legs are unchanged from v3**, because the dispatch change never touched
them. Nothing is marked over occurrence-09, now for two independent reasons: it is an F001 occurrence
and has **no contrast grid at all**, and its use-table rows arrive only at S9 from commitments S6 has
not sent, while a reading key must be named before first look. L003 therefore dispatches material
**for a successor pre-registration to read** and reads and marks only published bytes.

`p13` is rewritten to pin all six files `initialize` wrote, by digest, and to require the shared
plan_id and the runner's own `verify()`/`pending_wave()` answers. `p11`'s named exception points at
occurrence-09 and says in terms that **no published occurrence is written to or re-dispatched —
including the two the runner does verify**.

## What was checked

`validate.py` from this directory with `PYTHONPATH` at the **published** driver: **`ALL CHECKS
PASSED`, exit 0** — and it now **asserts the dispatch occurrence VERIFIES**, where v3's asserted only
that it was *absent*: runner v2's `verify()` and `pending_wave()`, the shared plan_id checked against
occurrence-08's `plan.json`, `max_calls` 11, the pinned scope, no delivery directory yet, and `p13`'s
six digests re-verified byte-for-byte. Whole suite: `Ran 3129 tests`, `OK (skipped=2)` — **no code
was added**. Credential scan over the staged paths: key **names** only; neither `DEEPSEEK_API_KEY`
nor `OLLAMA_API_KEY` is set in the publisher's environment.

**On identity.** `validate.py` is **not** pinned in the run's plan — `loop_plan_id` folds
`config.json` and the run-root copies of `obligations.json`, `calibration.json` and `CEILING.md` — so
validator edits move no id, while `config.json` and `obligations.json` edits do. Both moved here,
which is why L003 is a new pre-registration and not an amendment.

## What this bundle still does not do

It mints nothing: no `loop_plan_id`, no receipt id, no run timestamp — the labelled placeholders
stand. It claims nothing about any arm, model, family, account or cell; ruling 7 holds over every
number in it and `CHANGES-PREREG.md`'s metric-creep re-read lists each with its guard sentence.
`CLONE-PATCH.md` carries what the driver must still do. Publication is to the branch by owner mandate
(ruling 2), with publication to `main` **pending owner merge**.
