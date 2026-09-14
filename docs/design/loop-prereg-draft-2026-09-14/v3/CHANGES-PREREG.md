# CHANGES-PREREG — every edit made at the L001 pre-registration review

2026-09-14. Scope: `loop-prereg/` only. **No file in `loop-impl/repo` and no file in
`/home/user/miniReason` was edited by this revision**; both were read read-only. No provider call
was made and no credential was read or printed. Every edit below was made **before** S0
PREREGISTER — after S0 each of them mints a new `loop_plan_id` and is a new pre-registration, never
an amendment.

Applied in the recomputation order `REVIEW-PREREG.md` §D(3) fixes: standard body (clone, step 1) →
`calibration.json` (2) → `config.json` (3) → `obligations.json` (4) → `PREREG.md` (5) →
`validate.py` (6) → `VALIDATION.md` (7). `reading_set.json` is edited with step 4, since
`PREREG.md` quotes it.

The clone-side half of PR-01, PR-02, PR-05, PR-06, PR-07 and PR-12 had already landed in
`loop-impl/repo` under waves 2 and 3; those halves were **verified against the modules here**, not
assumed. What the clone must still do is `CLONE-PATCH.md`.

---

## Step 1 — the standard body (clone-side, verified, not edited)

Read at this review from `loop-impl/repo/src/minireason/loop/`:

- `standard.STANDARD_BODY_SHA256` = `a9007dc73c748cfff974a1a3d77098d380ec153b1b8cf93f513cafa3ea0572d7`.
  It has moved three times in the review window (`b4dc7f6a…` → `6c894deb…` → `742c2a0b…` →
  this value). **To be re-read at PREFLIGHT after the clone freezes.**
- `standard.CEILING_SHA256` = `1e26be087483fd1b9c8e2c403cfae646fb07ebc773f23434a0c4dfab3ed04c1e`,
  unmoved; `standard.CEILING_TEXT` is still byte-identical to `PREREG.md` §4, asserted by
  `validate.py`. **To be re-read at PREFLIGHT after the clone freezes.**
- `audits.CALIBRATION_EXCHANGES_SHA256` = `91c29e1e71719d815c21c2697f4aa68a7c983be21df945ad6b1e5042183981e5`.
  **To be re-read at PREFLIGHT after the clone freezes.**
- `standard.CALIBRATION_ANCHORS[0]` now reads "built with the referring region alone" — the PR-06
  repair has landed. Verified by probe, below.

---

## MECHANICAL items

### PR-01 — the forbidden key in the bundle's own `calibration.json` — **APPLIED**

**Was** (`calibration.json`, top-level key): `"scoring": "An error is an anchor whose observed
outcome disagrees with its `error_if` clause, counted per (anchor, seat)…"`.

**Checked before applying.** `scoring` is a member of `standard.FORBIDDEN_KEYS` (25 members, read
from the module). `contracts.assert_no_scoring_keys(json.load(open('calibration.json')))` raised
`SCORING_KEY_FORBIDDEN`; the other three bundle JSONs passed. WAVE3-INTERFACE §7 confirms nothing
in the code reads that field, so the rename costs nothing downstream.

**Now**: the key is `error_rule`. The rule is stated in prose in the same value, and it is stated
at **panel grain** to match `decide.instrument_bound_crossed` ("neither is computed per seat") and
`audits.planted_flaw_calibration`: one share for the judging panel, the per-`(anchor, seat)`
decomposition recorded only so an audit hit can name which exercise produced it, never divided per
seat, never compared between seats, never rendered as a per-endpoint rate. That closes the
`(iii)`-adjacent flag `REVIEW-PREREG.md` §B raised against the old value as well as PR-01 itself.

**Also applied**: `validate.py` now runs `contracts.assert_no_scoring_keys` over all four bundle
JSON documents. The review's diagnosis was right — the old validator ran only the standard's
forbidden-stop-token scan, which is why this passed unnoticed.

**Justification.** `p4` is a protected obligation and the calibration set is registered at S0. As
it stood, the first live run would either refuse at S0 or fail a protected obligation at the first
`decide()` and stop `protected_loss` — a stop caused by the pre-registration document rather than
by anything the run observed.

### PR-02 — two digests of one document — **APPLIED**

**Was** (`PREREG.md` §3): "`obligations.json` is pinned at sha256 `713119a7cd…`".

**Checked.** `obligations.canonical_pin()` returns the canonical-body digest (canonical JSON minus
the two digest keys); `obligations.pin()` returns the file digest and its docstring says "**This is
the one the plan identity carries**". Two different values over one document; the old text named
one and the identity folded the other.

**Now** §3 publishes both with their attribution: the canonical-body digest
`3bda592108ac11aee8fe34da5b4317001156d18417af397ee6957f310ce55900` (what
`obligations.json:obligations_sha256` declares and what this prose publishes) and the file digest
`910282bb43de93bd9fdd1498ec279a177fcaee3b815ebdc8e8a6eea4a9179045` (what `obligations.pin()`
returns and what enters `loop_plan_id` and `custody.verify_pins`), with the sentence explaining why
they differ. `validate.py` asserts both, asserts they are unequal, and asserts both appear in
`PREREG.md`. The `obligations.pin()` branch was taken and not the alternative of changing the
implementation, because the file digest is the only one re-derivable from the tree.

### PR-07 — `validate.py` ran against a five-pin-short pin map — **APPLIED**

**Was**: `pins = {"src/minireason/data/endpoints.json": "0" * 64}` — one entry against
`types.PINNED_SOURCE_PATHS`' six. Reproduced here: `LoopError: PIN_INVALID: the plan identity is
fixed by 6 source pins and pins supplies no digest for 5 of them: …`, exit non-zero.

**Now** the validator builds the map from `PINNED_SOURCE_PATHS` itself, with each file's real
sha256 read from `/home/user/miniReason`, prints all six, asserts the identity is one value from
file and from object, asserts a changed pin changes it, and asserts that a five-entry map is still
refused `PIN_INVALID`. A pre-registration whose own acceptance evidence does not re-run is not
repeatable; it re-runs now, exit 0.

### PR-08 — `VALIDATION.md` did not describe the bundle beside it — **APPLIED**

**Was**: `config.json` pinned at `46495a6f…` against an actual `081dd939…`; an `audit={…}` line
predating the two account fields; a demonstration `loop_plan_id` `cc7c137f…` that no longer
computed.

**Now** `VALIDATION.md` is **regenerated wholesale** from the run actually performed, not patched:
the full transcript, the digest table for every bundle file, and a demonstration `loop_plan_id`
over the full six-pin map. AGENTS.md forbids modifying a published observation, which is why the
regeneration happens before publication and not after.

### PR-12 — block-code spelling, and the tenth code — **APPLIED, both halves**

(a) **Was** in `o1` and `o2`: a reason spelled ``` `blocked:<code>` for a `code` in
`types.BLOCK_CODES` ```. Checked: every member of `types.BLOCK_CODES` already carries the prefix
(`blocked:schema`, …, ten of them), so read literally the bundle admitted `blocked:blocked:schema`.
**Now** both use `o4`'s spelling: "a `block_code` that is a member of `types.BLOCK_CODES` (whose
members already carry the `blocked:` prefix, so the code is written once and not twice)".

(b) **Was**: the frozen ceiling enumerates nine bare reasons; `types.BLOCK_CODES` has ten.
The ceiling text is frozen and its digest is pinned, so it is **not** edited. **Now** `PREREG.md`
§3 states the reconciliation beside it: `report.BLOCK_REGISTER_HEADINGS` (verified: ten entries,
the ceiling's nine in the ceiling's order plus `constitution`) is what the rendered register
prints, so `blocked:constitution` has a printed home under `o4`. The same paragraph adds the
**FW5:688** anchor the review found missing from the whole bundle: *the inability to evaluate a
proposition is not a falsifying observation of the proposition*.

### PR-13 — the `unread` inventory, eleven against twelve — **APPLIED, count re-derived**

**How it was counted.** Read read-only from
`/home/user/miniReason/experiments/diagnostics/C001-contrast-triple/occurrence-01/comparison.json`:
its `tables` array has **12** entries. Each entry carries an `endpoint_slug` and an `arm`; the
twelve pairs are `deepseek-flash`, `ollama-gemma4-31b`, `ollama-glm-5.3`, `ollama-gpt-oss-120b`,
`ollama-kimi-k3` and `ollama-qwen3.5-397b`, each × `fcl` and `prose` — six slugs × two arms,
twelve distinct `(endpoint_slug, arm)` pairs, no repeats. `occurrence-02/comparison.json` has one
table, `deepseek-flash`/`fcl`, and it is the one the reading set names. So **all twelve** of
occurrence-01's are unread.

The earlier "eleven" was the eleven that remain after setting aside the `deepseek-flash`/`fcl`
juxtaposition that G10(b) pre-empts (1/20 replicates `COMPLETE`, 19 unresolved cells). That is not
the unread inventory: a pre-empted juxtaposition this run never reads is unread too.

**Now**: twelve in `PREREG.md` §5 and §6 with the derivation shown, twelve with the derivation in
`obligations.json:material.note`, and `reading_set.json` order rationale item 5 keeps its 11 × 12 =
132 arithmetic for the *cells* while saying all twelve juxtapositions are unread.

**Re-checked, unchanged**: `p10`'s other two figures, recomputed from both `comparison.json` files
— **78** empty `root_reading` cells (72 + 6) and **208** empty register-mark cells (192 + 16).
They verify exactly and were not touched.

### PR-18 — the placeholder receipt id was a live, published id — **APPLIED**

`REC-20260914-Z` is carried by `docs/DECISION_LEDGER.md` for F002 occurrence-03 (ruling 14).
**Now**: `**REC-YYYYMMDD-X opened at <minted at S0>: …**`, an id no ledger can ever carry, and the
note above it says why. `receipts.open_preregistration` mints the real one under the append lock.

### PR-22 — `p1`'s `material_sha256` — **APPLIED**

Checked: `occurrence-01/material.json`'s top-level keys are `schema`, `system`,
`prose_instruction`, `formal_instruction`, `bare_instruction`, `problems`, `templates`,
`source_pins` — no `material_sha256`. **Now** p1 says "the sha256 of
`experiments/diagnostics/H005-open-prose-commitments/occurrence-01/material.json` equals
`24ca4552…`" and names the absent field explicitly. The digest value does not change.

### PR-24 — `STOP_REASONS` omits `preregistered_condition:<id>` — **APPLIED as a note**

Checked: `types.STOP_REASONS` is exactly seven tokens and
`types.PREREGISTERED_CONDITION_PREFIX` exists for the prefixed form. **Now** `PREREG.md` §3 records
the omission as deliberate for L001 — nothing here declares such a condition and `LoopConfig` has
no field for one — so a later reader is not left to diff the design against the enum.

---

## JUDGMENT items

### PR-03 / D(1) — `p7` — **DECIDED: adopt the implementation's two conjuncts**

**Was**: "No reading mints an `att` or `dep` edge on any node under study. The set of `att` and
`dep` edges whose target is an `E_row` or `E_cell` material artifact is empty…"

**The constraint.** Design §3(d) *requires* every `A_reading` to carry `dependence` → `E_row`, and
§3's "invalidate `E_row` ⇒ the reading becomes `suspended_unsupported`, not `refuted`" depends on
it. The old sentence forbade exactly that ref.

**Decided.** `p7` now reads: no `att` edge may target a node under study, **and** no node under
study may be the **source** of any edge; a reading's `dependence` ref onto its own `E_row`/`E_cell`
is required and is not an edge on a node under study in the sense this clause protects. Verified
against `obligations.no_edges_on_studied_nodes`, which asks those two questions and no others.
This is design §3's precise statement rather than §5's compressed one; the difference is recorded
in `obligations.json:notes.p7` and in `PREREG.md` §7 because the design is the document of record.
The protection is not weakened — both directions that could hide a change to the material are
refused, and the old sentence was silent about the source direction.

### PR-04 / PR-16 / D(1) — `o5` — **DECIDED: adopt `audit_in_force`'s predicate, keep both strengthenings**

**Was**: "one registered `AuditReport` whose `cycle` index n satisfies `current_cycle - n <
audit.period` (= 2 for this run)…"

**Decided.** `o5` is now the predicate `obligations.audit_in_force` evaluates: a registered
`AuditReport` **declares** that its coverage includes the cycle under evaluation, names both judge
seats by endpoint name, and carries a planted-flaw result against the pinned rows. The bundle's two
genuine strengthenings survive; the cadence stays declared in `reading_set.json` and reported, and
is not read by the predicate. Note for the record: on the metric-creep question the review is right
that a recency comparison on a cycle index is a class-(ii) cadence parameter and not creep — the
reason for the change is not metric hygiene but that a pre-registration which fixes O by a text the
run discharges by a different program has fixed nothing.

**PR-16 folded in.** `o5`'s statement now says in terms that its discharge is **a repair of the
reader and never a repair concerning the material**, and `PREREG.md` §6 says the same at length:
cycle 2 can always manufacture that CONTINUE out of the loop's own artifacts, so "an obligation was
discharged, therefore progress" must not be read across from the instrument to the material
(FW5:785).

### PR-05 — `p4` — **DECIDED: keep the broad scope, add the quoted-material exemption**

The program half landed in wave 2: `obligations.no_scoring_key` now reads record **keys** and the
**headings and table header rows** of every file in the `rendered_files` record, and the
`| cell | score | rank |` fixture that used to pass now fails. So the bundle keeps "every table
header and every file rendered under the run root" — that is now what the program does — and adds
the exemption in the same sentence: quoted passages of the material are not scanned, because
refusing a run over a word in a passage it quotes would be the loop editing its own evidence
(`graph.G12_EXEMPT`). The alternative — narrowing p4's wording to the old program — was declined;
the review is right that silently publishing a broad wording over a narrow program is the worse of
the two, and the program is no longer narrow.

### PR-06 — `cal-01` — **DECIDED: mirror the repaired anchor, keep cal-07's contrast**

**Was**: "The referring record and the target record are the same bytes … The resolvable surface M
is that record twice", declared `must_sustain: true`. **Now**: built with the **referring region
alone** — the row carries a referring record, declares no target, and W1-SURFACE's own rule makes
that available ("a region the row does not carry is absent, not empty").

**Verified by probe, both directions**, on a real published row of
`use-table-golden/use_table.json`, and the probe is now a permanent check in `validate.py`:

| construction | window 20 | 40 | 80 | whole record |
|---|---|---|---|---|
| referring region alone | unique, in declared span | unique | unique | unique |
| both sides, same bytes (the old one) | no unique resolution | none | none | none |

`cal-07` keeps the two-copy construction and its `must block` ground truth, so the two are now a
contrast rather than a contradiction. `validate.py` also asserts that the module anchor and the
bundle row both carry the repaired construction, so they cannot drift apart again.

### PR-09 / D(2) — the guard-rail accounts — **DECIDED: all three settled, two premises withdrawn**

No string reading "PROVISIONAL" or "to be settled" survives anywhere in the bundle; `validate.py`
asserts it. Both config accounts now open "SETTLED at pre-registration review". The reasoning:

- **`judge_err_max` = 0.2.** The old account's denominator was wrong. Checked against the code
  rather than against the bundle: `audits.build_calibration_set` seeds from
  `standard.CALIBRATION_ANCHORS` — **five** anchor kinds — and `planted_flaw_calibration` appends
  one `exercised` entry per `(row, seat)`, so the denominator is at most **5 × 2 = 10**, and
  `_calibration_share` divides errors by *exercised*, not by the pinned row count. The rail fires
  on **strictly greater** (`share > bound`). So over ten exercises 2/10 = 0.2 does **not** fire and
  3/10 = 0.3 does: the **third** disagreeing exercise, not the first as the old account claimed,
  and not the second as a nine-row denominator would give. Where fewer were exercised the same
  bound fires sooner, and the account says so rather than letting a stop paragraph discover it. The
  account also states why the bound sits there — one or two disagreements are left to design §2.5's
  per-hit demonstrative warrants, the finer instrument — and that the share is panel-level and
  never a per-endpoint rate.
- **`streak_max` = 12.** The old premise ("longer than any block run the C001 and H005 published
  material produced") is **withdrawn as false**: neither study ran this guard and neither emits a
  block register, so the quantity does not exist in the published record. Twelve is re-anchored to
  something a reader can check in this bundle: the reading set is 38 cells — 4 baseline mark cells
  at zero calls, 12 cross-case mark cells, 22 H005 rows — so twelve consecutive blocks on one role
  is that role declining an unbroken run as long as the entire cross-case mark leg, or more than
  half the row leg. The account also carries the counter's definition verbatim (per role, dispatch
  order, reset by any non-blocked trial), because `decide.Instrument.block_streak` is declared and
  **unimplemented** and the driver must implement that definition or the account is false
  (CLONE-PATCH item 5).
- **`audit.period` = 2** gets the third account the review asked for. It could **not** go into
  `config.json`: `types.AuditConfig` accepts exactly five keys with `optional=frozenset()`, so a
  `period_account` key is `CONFIG_UNKNOWN_KEY`. It lives in
  `reading_set.json:audit_schedule_declaration` and is summarised in `PREREG.md` §3, and both say
  plainly that it is therefore pinned by that file's digest rather than by the config block of
  `loop_plan_id`. The clone patch to close that gap is CLONE-PATCH item 3.

Every account is phrased as an **instrument fault with no evidential reading**: crossing either
rail adjudicates no cell, discharges and defeats no obligation, and says nothing about the material
(ruling 7).

### PR-10 / PR-14 — resource conditions and seat evidence — **DECIDED: declared as bounds in a new §2a, evidence made truthful**

The conditions could not go into `config.json` either — `LoopConfig`'s key set is closed by design.
They are declared in `reading_set.json:resource_conditions` and printed as a table in `PREREG.md`
§2a, and `validate.py` asserts every value equal to the `roles` constant that will be sent, seat by
seat: per-role `max_tokens` (critic 2048, defender 1024, judge 2048, marker 1024, variator 4096 =
`paraphrase_n` × 2048); the wall as `min(seat.timeout_seconds, 300)` with all 24 registry entries
at 180 s, so every seat's wall here is 180 s (rulings 13, 14, with the five 300-s closes named);
the 8100-token wall ceiling; the 256-token floor and its refusal code; `thinking` **off where the
endpoint honours it** — `False` on the `deepseek`-family variator, never sent to any other family;
`temperature` 0.0 and the derived seed; the `PROVIDER_GATEWAY_WALL` block at 295 s.

The declared consequence is written down **before** it happens: the four Ollama seats are reasoning
models receiving no `thinking` control, so reasoning tokens are generated inside a 1024–2048 token
ceiling and the foreseeable failure is truncated JSON refused as `blocked:schema` at
`schema_repair_budget` = 0. That is this run's own budget choice, and declaring it in advance is
what stops it later reading as the instrument declining on the material.

**The seat evidence sentence is made truthful.** The evidence column's figures were gathered at
32768/600; this run asks at 1024–4096 inside 180 s. §2a now says the column is evidence of delivery
on a published occasion at a wider ceiling, that it does **not** transfer to this run's conditions,
and that nothing in the bundle treats it as a prediction — the same confound the variator's own row
already named in the other direction.

**PR-14** is recorded as the review classified it, **(ii) borderline**, with the sentence it asked
for: seat selection on delivery evidence is a resource decision made once at pre-registration,
never repeated inside the run, no seat is compared with another again for any purpose, and no
rendered file carries a per-endpoint delivery comparison.

### PR-11 — `publish_ref` and the ruling-2 deviation — **DECIDED**

`publish_ref` is now `origin/claude/project-state-direction-j5rbun` (validated against
`types._PUBLISH_REF`, which requires `<remote>/<branch>`). A new `PREREG.md` §2b carries the
ruling-2 paragraph: the branch is the publication target **by user mandate**, this is a declared
deviation from AGENTS.md's publish-to-`main` instruction, every receipt this run writes records it
as one, and publication to `main` remains **pending owner merge**. Publication before dispatch at
S2/S5/S7/S14 makes the ref load-bearing every cycle, which is why it is not left to the checkout.

### PR-15 — clause 1 — **DECIDED: FW5's held-then-failed form governs**

The bundle stated clause 1 two ways. **Checked against the current clone**, which settles it:
`obligations.protected_losses` registers a loss only where `was is Verdict.SATISFIED and now is
Verdict.NOT_SATISFIED`, and `decide` stops on that register. That is FW5:787's
`∀r∈P[r(ξ) ⇒ r(ξ′)]`, not the stricter form WAVE1-INTEGRATION-DECISIONS item 28(a) described — so
item 28(a) is superseded and `PREREG.md`'s sentence was the half that was wrong. `PREREG.md` clause
1 now states the transition form, cites the false-`protected_loss`-at-cycle-1 failure mode it
avoids, and notes that `protected_not_evaluable` never terminates the chain (FW5 R5).
`obligations.json:repair_condition` states the same condition once, in the same words.

### PR-17 — Account (𝓔) — **DECIDED: one paragraph in §6**

The absence was correct and silent. `PREREG.md` §6 now says that L001 tests no clause of
`Account(𝓔)`, that the FW5 Account sufficiency-or-necessity challenge is a separately identified
study (ruling 9(b), staged as A001) with its own claim, dependencies, grain, boundary, contrasts
and relinquishment fixed before evidence, and that no outcome of this run may be cited for or
against any Account condition.

### PR-19 — the predicted stop clause — **DECIDED: clause 3, with clause 4 named as the live alternative**

The old prediction (clause 4) was wrong, and predicting the wrong clause in the document written
"so that it cannot be narrated as a success afterwards" undercuts the point of writing it.
`decide` evaluates clause 3 before clause 4, and o1–o4, o6 and o7 are all satisfiable by **recorded
reasons** rather than by filled cells. §6 now names **clause 3, `obligations_discharged`, at cycle
3** as the more likely stop, names clause 4 as the live alternative, and states exactly what
separates them (an `INDETERMINATE` coordinate or a rendered-record gap leaving one *o* unsatisfied
while the triple set has stopped moving). It adds that **neither is a result about the material**.

### PR-20 — the C001 leg's known shape — **DECIDED: carry the shape, not the figures**

§6 now states the four guards that fix most of that leg before any call — G10(d) program-computing
T and D on the FCL arm with no judge called, G9 forcing `differs` to `same` against the frozen
baseline's kind set, G10(c) forcing E to `unresolved` on shared bare tokens, and
`FALSIFIER_MAP` excluding G from D1/F2/F3 so G is residue — and reports that the wave-1 offline
pass found that shape. It **does not re-assert that pass's figures**: WAVE3-INTERFACE records that
occurrence-02 was published after the clone was cut, so the pass is not reproducible there and the
run must recompute them. What is pre-registered is the *reading* of whatever it recomputes: a G9
`same` is the replicate-baseline rule firing and not a reading that the cases do not differ; a
G10(c) `unresolved` is absent data and never an absence of difference; a leg with no admissible
`differs` is a fact about the guard's pre-emption at N = 5 and leaves the recoding and carrier
rivals unrefuted and unsupported, not excluded.

### PR-21 — the four extra calibration anchors — **DECIDED: pinned by the bundle, not by the standard body**

**Checked by recomputation**: `standard.CALIBRATION_ANCHORS` carries five ids; `calibration.json`
carries nine; the four with no module entry are `fabricated-decisive-point`,
`duplicated-passage-non-unique-offset`, `order-swap-sensitive-pair` and `paraphrase-invariant-pair`.

**Decided: they do not enter the standard body**, which is the option that requires no clone edit
now — adding them would move `STANDARD_BODY_SHA256` for a fourth time and with it every derived
pin, and the recomputation order forbids a clone edit at this point. The consequence is declared
rather than left to be discovered: the four are **not reachable by the case-law closure** that
collapses every ν citing `std:reading-rubric/v1`; they are pinned by `calibration.json`'s own
sha256, recorded in `plan.json`, and are attacked through that pin. They also never enter the
`judge_err_max` share — cal-06 and cal-07 are program checks the guard must decline, cal-08 and
cal-09 register under the order-swap and paraphrase-invariance arms — which is what keeps the
settled `judge_err_max` account's denominator honest. Stated in `calibration.json:anchor_set_extension`,
in `PREREG.md` §3, and enforced by a `validate.py` assertion naming the four by id.

### PR-23 — `o7`'s four states against the ceiling's three — **DECIDED: one clause in o7**

`o7` now ends: the ceiling's three are this clause's three non-resolved states —`unresolved`,
`machine-unresolved:<block code>`, `unread` — and the fourth printed state is the resolved one, a
relation or a mark; the two are one enumeration counted from two ends. Verified against
`obligations.CELL_STATES` = `('read', 'unresolved', 'machine-unresolved', 'unread')`, which is
mirrored in `reading_set.json:vocabularies` and asserted by `validate.py`.

### PR-25 — the symbols the bundle is written against — **DECIDED: enumerate, mirror, assert**

A new `PREREG.md` §4b prints, verbatim from the modules: the six reading values (and the five
nominable relations inside them, and that a critic's `none` is an answer and not a member); the
three marks; the four closed per-register `difference_kind` sets; the ten block codes and how they
relate to the ceiling's nine; the four printed cell states; the three reopen reasons; and the five
calibration anchor kinds the standard body carries. `reading_set.json:vocabularies` carries the
same lists machine-readably with the module symbol named beside each, and `validate.py` asserts
every one of them equal to its constant *and* asserts each token is printed in `PREREG.md`, so a
drift in either direction fails the bundle. A new `PREREG.md` §4a names
`standard.STANDARD_BODY_SHA256`, `standard.CEILING_SHA256` and
`audits.CALIBRATION_EXCHANGES_SHA256` beside the ceiling, each with the sentence **to be re-read at
PREFLIGHT after the clone freezes**.

---

## E and NOTES items carried

- **The credential line now says what it does.** `validate.py`'s `os.environ.get(env)` read carries
  a comment: the value is compared against the bundle text and never printed, stored, logged or
  written; only the assertion fails, and its message carries no value (ruling 4, AGENTS.md).
- **FW5:688 is now cited** beside the block-code set, which the review found to be the one FW5
  anchor the bundle used without naming.
- **The error share is defined at panel grain**, closing §B's `(iii)`-adjacent flag against
  `calibration.json`'s old "counted per (anchor, seat)" definition, which disagreed with
  `decide.py`'s docstring and was one join away from a ranking of endpoints.
- **What the review asked not to lose was not lost**: the `max_calls` derivation and its
  `deviation_from_design` note, the `audit_schedule_declaration`, `p10`'s two verified
  enumerations, the `why_not_a_count` note on every clause, §6's refusal to let a thin table read
  as failure, and "Success for this pre-registration is not that any cell filled" are all
  unchanged except where an item above required a change.
- **Nothing was minted.** No `loop_plan_id`, no receipt id, no run timestamp. The labelled
  placeholders stand: `REC-YYYYMMDD-X`, `<minted at S0>`, and the `loop_plan_id` computed at S0.

---

## Digests after this revision

Recomputed over the bundle's own files at the end of the revision. `VALIDATION.md` carries the same
table generated from the validator run itself.

| file | before | after |
|---|---|---|
| `calibration.json` | `9ca9ad04672e99becc19096e3de4d4010d9f21c700a979695ef034f9c19aae95` | `eaf41d3eed98f7ba839ab604367c3daf3f92d7cf07a658694bd9cdd5539a5e38` (PR-01, PR-06, PR-21) |
| `config.json` | `081dd939663156aa3969f3b000fcb0ca4b07086ab4340b0156057903b45b5110` | `63879991dd632f016e9917ab336fca872b29f16a527e4b67621e189478c38ec0` (PR-09, PR-11) |
| `obligations.json` | `2913693abce664af387f1683c7cbfd622043a697343a6d415d89a8179d3652d6` | `910282bb43de93bd9fdd1498ec279a177fcaee3b815ebdc8e8a6eea4a9179045` |
| `obligations.json` canonical body | `713119a7cd255296058b18084a40cbac7a3353903bbf8cd260b6e78c173e4302` | `3bda592108ac11aee8fe34da5b4317001156d18417af397ee6957f310ce55900` |
| `reading_set.json` | `ef8c62a5ad6148c4bf676fadabba1ae0504babef26b4f793cce7d80ff37c728e` | `929868e8869788c8483029c1a36246b1cc9429f7fb90f0ab3934b80795e238e7` (PR-13, PR-10, PR-25, `audit.period` account) |
| `PREREG.md` | `c04c2092f672b52572ea98a60575e3405c5072f6b381b9b55a30cb3f7dcd16d6` | `0dbfae63f8f49b583e31e341c6149f4b6352a7497e387907fc5ef2867739ae28` (most items) |
| `validate.py` | `fd8015261e86cf34cf87f1fd576fd28fb98cc635a7889ee7cb63cb5dde41f25e` | `5f47c46bb2e80264ae56b316a4ab17b4162052c055150875cf7599247ea9d265` (PR-01, PR-06, PR-07, PR-10, PR-25) |
| `VALIDATION.md` | `62f2b71a90488852ed1b4e4af17138e22b77f60c31c0fb222326b085d257c413` (superseded) | regenerated wholesale from the run it transcribes |

The exact post-revision values for every file are in `VALIDATION.md`, generated by the run it
transcribes.

---

# METRIC-CREEP RE-READ — `REVIEW-PREREG.md` §B against the revised bundle

Ruling 7's classes, unchanged: **(i)** a resource boundary — allowed, reported as a boundary, never
as evidence; **(ii)** a guard-rail parameter — allowed **only** with a mandatory account when it
fires; **(iii)** an optimisation target, score, progress meter, success rate or ranking — not
allowed.

**Every number §B already cleared is unchanged**, except that the two it failed now pass. The
ruling-7 sentence §B checked for is still absent: `grep -niE "unresolved rate|success rate|progress
meter|worth running again"` over the revised bundle returns nothing, and nothing turns "mostly
unresolved" into a failure condition. **No (iii) appears anywhere in the revised bundle.**

**The three §B findings are closed.**

- `audit.judge_err_max` — §B: "**Account fails** — provisional and arithmetically wrong". Now
  settled, with the denominator taken from `audits.planted_flaw_calibration` rather than from the
  bundle's row count.
- `audit.streak_max` — §B: "**Account fails** — provisional, premise unsupported". Now settled,
  with the false premise withdrawn in the account itself and the figure re-anchored to the
  pre-registered reading set.
- `audit.period` — §B: "**No account is attached**". Now accounted, in
  `reading_set.json:audit_schedule_declaration` (the config's schema cannot hold it; CLONE-PATCH
  item 3).
- §B's `(iii)`-adjacent flag against `calibration.json`'s "counted per (anchor, seat)" is closed:
  the quantity is defined at **panel** grain, matching `decide.instrument_bound_crossed`, with the
  per-exercise decomposition recorded only to name a hit.
- **PR-14** is recorded as §B classified it — **(ii), borderline** — with the sentence §B
  recommended, in `PREREG.md` §2.

## Every number this revision added, and the sentence that guards it

| number | where | class | the guard sentence that stands beside it |
|---|---|---|---|
| `max_tokens` 2048 / 1024 / 2048 / 1024 / 4096 | §2a, `resource_conditions.role_max_tokens` | (i) | Per **role**, derived from that role's own contract word limits — not per seat, so no cross-seat comparison is expressible from them. "A reached ceiling is a declared resource boundary, not exhaustion of the inquiry." |
| 300 s gateway wall; 180 s seat wall; `min(timeout, 300)` | §2a | (i) | A limit of the **host**, observed five times on one day; never used to raise a timeout. A `blocked:provider` at the wall is a delivery fact and never a reading of the cell. |
| 8100-token wall ceiling; 0.5 generation share; 90 tokens/s; 256-token floor; 295 s | §2a | (i) | Terms of one arithmetic recorded in every call record so the bound carries its own account. None is compared against an outcome; a seat whose ceiling fell below the floor is **refused, not truncated**. |
| 32768 / 600, in the seat-evidence sentence | §2a | (i) | Named **only** to say the evidence gathered at those settings **does not transfer** to this run's conditions and is not offered as a prediction. |
| 20/20 against 19/20, the `glm-5.3` paragraph | §2 | (ii) borderline | "A recorded difference between occasions, not a ranking (FW5:849)" — plus the new closure: a seat is never dropped, preferred or compared for a delivery figure again inside this `loop_plan_id`, and no rendered file carries a per-endpoint delivery comparison. |
| the `judge_err_max` denominator: five anchors × two seats = **at most ten** exercises; 2/10 = 0.2 does not fire, 3/10 = 0.3 does | `config.json`, `calibration.json`, §3 | (ii) | "It is a **panel-level** quantity, one share for the judging panel, never computed per seat, never compared between seats and never rendered as a per-endpoint rate. Crossing it names `instrument_fault` … It adjudicates no cell, discharges and defeats no obligation of O or P, and carries no evidential reading whatever about the material." |
| the `streak_max` anchor: 38 cells = 4 + 12 + 22, so twelve is as long as the whole cross-case leg | `config.json`, §3 | (i) enumeration inside a (ii) account | An enumeration of the **pre-registered key set**, used to anchor a bound on the instrument and compared against no outcome. "A high block rate is the instrument declining to read and is never an absence of relations." It is **not a prediction** that the run will produce fewer than twelve blocks. |
| the `audit.period` arithmetic: one window costs 46 of 396 | `reading_set.json`, §3 | (i) | An attention-and-spend comparison between two declared budgets. "`period` fires no stop, adjudicates no cell and enters no clause of O or P." |
| **twelve** occurrence-01 juxtapositions; six slugs × two arms; 11 × 12 = 132 cells | §5, §6, `obligations.json`, `reading_set.json` | (i) enumeration | An inventory of what was **not read**, counted from the published bytes. "An *unread* cell is one nobody and nothing has read … Conflating any two would let an unfinished worksheet read as a finding." Naming the unread is the opposite of a result. |
| nine pinned rows; five standard anchor kinds; four bundle-pinned guard probes | §3, `calibration.json` | (i) enumeration | Set sizes of a declared, closed set. The four extras "never enter the `judge_err_max` share", so the split cannot be read as a partial score. |
| 18 calls per window, restated as a **ceiling** | `calibration.json` | (i) | "A budget is an upper bound and never a target"; where the leg spends less the record reports the spend. |
| five closes in a 183 ms band; 300,270 ms; 300,453 ms; 300–301 s | §2a | (i) | Delivery observations about a **host**, cited as the evidence for a resource condition (rulings 13, 14). They describe no reading and no seat's standing. |

## Two numbers I looked at hardest, and why each stays

1. **The calibration share is a rate, and a rate over a judged set is the classic (iii) shape.** It
   stays because ruling 7 admits it by name ("`judge_err_max` raising an audit-the-judge signal"),
   because every anchor's ground truth is **true by construction** so the share measures the
   reader and never the material, and because three independent places now forbid the one move that
   would make it (iii): `decide.instrument_bound_crossed` computes it panel-level, the revised
   `error_rule` says it is never divided or compared per seat, and `p6` makes any aggregate,
   ranked or weighted field over rulings unexpressible in a registered artifact at all. The
   remaining risk is a **join** — a per-exercise decomposition beside a seat column in some future
   render — and the bundle now names that risk and forbids it rather than relying on nobody
   thinking of it.
2. **`0 admissible differs` on the C001 leg would be a number that reads like a finding.** It is
   not in the bundle: §6 carries the leg's *shape* and explicitly declines to re-assert the wave-1
   pass's figures, because occurrence-02 postdates the clone and the run must recompute them. What
   §6 pre-registers is the **reading** of whatever is recomputed: a G9 `same` is the
   replicate-baseline rule firing and not a reading that the cases do not differ; a G10(c)
   `unresolved` is absent data and never an absence of difference; a leg with no admissible
   `differs` is a fact about the guard's pre-emption at N = 5 and leaves the recoding and carrier
   rivals **unrefuted and unsupported, not excluded**.

## What remains open, and is open by declaration rather than by omission

- The `audit.period` account is pinned by `reading_set.json`'s digest and **not** by the config
  block of `loop_plan_id`, because `types.AuditConfig` has no field for it. Named in `PREREG.md`
  §3 and CLONE-PATCH item 3.
- The `streak_max` account states a counter definition that **is not yet implemented**
  (`decide.Instrument.block_streak` is a declared integer; W5-DRIVER must supply it). If the driver
  implements a different counter, the account beside the number becomes false — which is why
  CLONE-PATCH item 5 requires PREFLIGHT to assert the definition rather than trusting it.

---

# v3 (L002) — what the first live SEND forced, and what changed

2026-09-14, after L001. Scope: `loop-prereg/` only; no module was edited and **no code was added**.
`validate.py` was re-run with `PYTHONPATH=/home/user/miniReason/src`, the **published** driver.

**What happened.** L001 minted `REC-20260914-AI` at S0, published its plan at `b419027`, spun
sixty-four waves at S6 SEND and stopped, **zero provider calls spent**. Root cause, from the
repaired driver's own record: `config.occurrences` named
`experiments/diagnostics/H005-open-prose-commitments/occurrence-01`, which carries no `arms.json`
(runner v2's `verify()` raises) and a prepared-but-never-sent `waves/wave0006.json` of five
`daily`/cycle-2 coordinates with requests and no attempts (`pending_wave()` never clears;
`prepare_wave` would refuse `PREPARED_WAVE_PENDING`). `REC-20260914-AJ` at `2897496c` repaired the
driver: S1 now refuses `OCCURRENCE_NOT_DISPATCHABLE` before anything is published,
`types.FAILURE_CODES` is 219, suite `Ran 3129 OK (skipped=2)`.

**Checked here, and it widens the finding.** `arms.json` is absent from **every** published
occurrence of both studies — H005 occurrence-01, C001 occurrence-01 **and** C001 occurrence-02 —
so no published occurrence of either study can be declared in `config.occurrences` at all. The
only published occurrence in the tree that carries one is F002 occurrence-03, written by the newer
runner.

**The decision, from design §3/§4 and from what the driver actually does.**
`config.occurrences` is three lists at once — dispatch (S4/S6), import (S8) and use-table (S9) —
and S1 verifies every member before publication. So:

- **dispatch leg**: a **new** occurrence, `experiments/diagnostics/C001-contrast-triple/occurrence-03`,
  minted under C001's frozen `plan_id 328b9452…` and declared before dispatch as F002
  occurrence-03 was (ruling 14). 20 planned calls — 4 cases × 5 replicates × 1 arm × 1 endpoint,
  the shape occurrence-02 declared and spent.
- **marking leg**: the 16 declared cells — 4 within-ORIGINAL baselines and 12 cross-case
  juxtapositions — over **published, closed** occurrence-02, through its published
  `comparison.json`. Design §3(b)/§3(c): the bytes register as `E_cell` with
  `provenance.role = IMPORT` and one `C_open` opens per cell before any call. No dispatch, and
  `p10`/`p11` hold unchanged.
- **not over the new occurrence, and the reason is pre-registered**: S0's `seal_baselines` reads
  the contrast occurrence's `comparison.json` and `_contrast_cells` skips an occurrence that has
  none; a new occurrence has none until `tools/contrast_triple_study.py` builds one after its
  dispatch closes, and **no step S0–S15 builds it**. Marking occurrence-03 would pre-register
  cells the program can never open.
- **the 22 H005 rows**: dropped and named `unread`. Declaring them means declaring their
  occurrence, which is the refusal L001 already bought. They stay reading-only precedent material,
  still pinned by `p1` and still the source of `calibration.json`'s anchors. `o1` therefore holds
  **vacuously** and says so, and a vacuous `o1` is no evidence about any of those rows.
- **occurrence-03's own rows are not pre-registered either**: they reach the run only at S9, from
  commitments S6 has not yet sent, and a reading key must be named before first look and is
  self-tested at PREFLIGHT. They are `unread` under `o7`. So L002 dispatches material **for a
  successor pre-registration to read** and itself reads and marks published bytes only.

**`max_calls` 396 → 174**: `0` (4 baselines) `+ 108` (12 cross-case × 9) `+ 0` (no row leg)
`+ 46` (one audit window) `+ 20` (occurrence-03 dispatch). **Whose budget the dispatch calls are:
both, and the record says both.** They are the C001 study's own calls — occurrence-03 is an
occurrence of C001 under C001's plan_id, and its arms, cases, replicates, seeds and endpoint scope
are fixed by its own staging receipt before dispatch — **and** they are inside this loop's
`max_calls`, because the loop's driver issues them in-process through `send_round` and a bound on
spend that does not bound everything the process spends is not a bound (ruling 7).

**New protected obligation `p13`** — |P| 12 → 13: occurrence-03's `material.json`, `arms.json` and
frozen `plan.json` stay at the digests pinned at PREREGISTER, and the occurrence declares C001's
frozen `plan_id`. **`p11` gains one named exception**: runner v2 writes the dispatch leg's
requests, attempts, responses, traces, artifacts and wave records under occurrence-03 and under no
other path; no byte of any occurrence-01 or occurrence-02 is touched.

**The staging precondition, stated as a precondition.** Occurrence-03 does not exist and this
bundle does not create it. No step S0–S15 creates an occurrence — `prepare_wave` prepares a *wave
inside* an initialized occurrence — and the driver's only stager is `dry_run`'s
`_stage_dry_run_material`, which writes **synthetic** material and must never be pointed at a real
study path. It is staged by a separately identified act with its own receipt under C001's own §13:
`material.json` + `arms.json`, then `runner_v2.initialize` to freeze its `plan.json`. Until then
**S1 refuses this config, offline and before any publication, and that refusal is correct**;
`validate.py` asserts the occurrence is absent for exactly that reason.

**The offline dry run cannot take this bundle, and that is recorded rather than worked around.**
`dry_run` calls `_stage_dry_run_material(root, cfg)`, which writes
`synthetic.material_document(seed)` and `synthetic.arms_document()` into every path
`cfg.occurrences` names and then calls `runner.initialize` on them. Pointed at this config it
would fabricate synthetic C001 material at
`experiments/diagnostics/C001-contrast-triple/occurrence-03` — a real study path under a real
plan_id. It was **not run**. The dry run's own record (`docs/design/loop-impl/DRYRUN-RECORD.md`,
exit 0, three cycles, zero live transports) stands as the offline exercise of the machinery; this
bundle's offline evidence is `validate.py`, exit 0, against the published driver.

**Digests after v3** — `config.json` `7b4785f4…`, `obligations.json` file `1e5a50c6…` / canonical
`90dfbebc…`, `reading_set.json` `f381ddbb…`, `calibration.json` `98b25a05…`, `PREREG.md`
`6827d277…`, `validate.py` `4f0d57cc…`, `VALIDATION.md` regenerated. Nothing minted: no
`loop_plan_id`, no receipt id, no run timestamp.
