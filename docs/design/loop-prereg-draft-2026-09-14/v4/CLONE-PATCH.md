# CLONE-PATCH — what `loop-impl/repo` must change for this bundle to validate

Written at the L001 pre-registration review, 2026-09-14, by the bundle reviser. **Nothing in
`loop-impl/repo` was edited by this review** — a wave-4 integrator holds that tree — and nothing in
`/home/user/miniReason` was touched. Every item below is a clone-side change the wave-5 integrator
must make, or explicitly decline, before S0 PREREGISTER. Items 1 and 2 are required: the bundle
does not validate against a clone that lacks them. Items 3 to 6 are declared gaps the bundle works
around and names; declining one leaves the bundle correct and the named consequence standing.

Where a value below is a digest, it is the value as read at this review and is marked
**to be re-read at PREFLIGHT after the clone freezes**.

---

## 1. REQUIRED — something must read `calibration.json` (PR-01's other half)

**State.** `audits.build_calibration_set` seeds the planted-flaw set from `standard.CALIBRATION_ANCHORS`
and the constructed exchanges in `audits._ANCHOR_EXCHANGES`. **No module reads `calibration.json`.**
WAVE3-INTERFACE §7 says so in terms. So the bundle's pinned calibration rows — their
`source_bytes` digests, their `error_if` clauses, their `ground_truth` — are pinned by
`plan.json` and read by nothing, and `o5`'s clause "carries a planted-flaw calibration result
computed against the calibration rows pinned in `plan.json` at their recorded sha256" cannot be
discharged as written.

**What is needed.** At S0 PREREGISTER the driver must (a) compute `sha256(calibration.json)`,
(b) write it into `plan.json` as `calibration_sha256`, and (c) at each audit window write that same
digest into the `AuditReport`'s `calibration_sha256` field, which `obligations.audit_in_force`
already reads:

```python
# obligations.audit_in_force, unchanged, already requires it:
calibration = _string(_field(node, "calibration_sha256"))
if situation.cycle_token in covers and seats and calibration:
```

Concretely, in W5-DRIVER at S0:

```python
calibration_bytes = (run_root / "calibration.json").read_bytes()
plan["calibration_sha256"] = hashlib.sha256(calibration_bytes).hexdigest()
```

and at the audit step, on the report body:

```python
body["calibration_sha256"] = plan["calibration_sha256"]
body["covers"] = [cycle_token]            # the cycles this record covers
body["seats"] = list(config.seats.judges)  # both judge seats, by endpoint name
```

**Why required.** Without it `o5` is unsatisfiable by the program that evaluates it, so the run
cannot reach clause 3 and the cycle-2 CONTINUE the honest-expectation paragraph predicts never
happens for the stated reason.

## 2. REQUIRED — `plan.json` must also pin `audits.CALIBRATION_EXCHANGES_SHA256`

**State.** The calibration anchors are pinned by `standard.STANDARD_BODY_SHA256`, but the
**exchange bytes** that make their ground truth true by construction are not: design §2.1 says the
standard carries "anchor exemplars", and `standard.CalibrationAnchor` carries a `construction` and
a `ground_truth_reason` and **no exchange**. `audits` pins them itself as
`CALIBRATION_EXCHANGES_SHA256` and records the gap for the bundle reviser (WAVE3-INTERFACE §8
item 8).

**Decision taken by this bundle.** The five constructed exchanges are **not** moved into the
standard body. Moving them would move `STANDARD_BODY_SHA256` a fourth time and therefore every
derived pin, and the recomputation order forbids a clone edit at this point. Instead the bundle
names the digest in `PREREG.md` §4a and this item requires the plan to pin it:

```python
pins["minireason.loop.audits.CALIBRATION_EXCHANGES_SHA256"] = audits.CALIBRATION_EXCHANGES_SHA256
```

Value at this review: `91c29e1e71719d815c21c2697f4aa68a7c983be21df945ad6b1e5042183981e5`
— **to be re-read at PREFLIGHT after the clone freezes.**

**Why required.** Otherwise the ground-truth bytes of the only lever whose truth is by
construction sit outside the plan identity, and a change to them would not move `loop_plan_id`.

## 3. DECLARED GAP — `types.AuditConfig` has no `period_account` field

**State.** `AuditConfig._REQUIRED` is exactly `{period, judge_err_max, streak_max,
judge_err_max_account, streak_max_account}` and `from_mapping` passes `optional=frozenset()`, so an
`audit.period_account` key in `config.json` is refused `CONFIG_UNKNOWN_KEY`. The module's own
docstring says "Each threshold carries an account, and the account is required" — and `period` is
the one threshold that carries none.

**What the bundle did instead.** The settled `audit.period = 2` account is written into
`reading_set.json:max_calls_derivation.audit_schedule_declaration` and summarised in `PREREG.md`
§3. It is therefore pinned by `reading_set.json`'s sha256 rather than by the config block of
`loop_plan_id`, and `PREREG.md` states that difference rather than hiding it.

**The patch, if the integrator wants the account inside the identity** (this moves
`config.json`'s digest and `loop_plan_id`, so it must land before step 3 of the recomputation
order, not after):

```diff
-    period: int
-    judge_err_max: float
-    streak_max: int
-    judge_err_max_account: str
-    streak_max_account: str
+    period: int
+    period_account: str
+    judge_err_max: float
+    streak_max: int
+    judge_err_max_account: str
+    streak_max_account: str

     _REQUIRED = frozenset({"period", "judge_err_max", "streak_max",
-                           "judge_err_max_account", "streak_max_account"})
+                           "period_account", "judge_err_max_account",
+                           "streak_max_account"})
```
with the matching `_text(raw["period_account"], "audit.period_account")` in `from_mapping` and the
key in `as_dict`. The account text to paste is the one in
`reading_set.json:audit_schedule_declaration`, from "ACCOUNT FOR audit.period = 2" onward.

## 4. DECLARED GAP — `types.LoopConfig` cannot carry the resource conditions

**State.** `LoopConfig._REQUIRED`/`_OPTIONAL` are closed and an unknown key is `CONFIG_UNKNOWN_KEY`
by design ("a key the loader drops is a pre-registration the run does not honour"). There is no
field for `ROLE_MAX_TOKENS`, for the `min(timeout, 300)` rule or for `thinking`.

**What the bundle did instead.** `reading_set.json:resource_conditions` declares them and
`validate.py` asserts each value equal to the `roles` constant that will be sent, seat by seat.
Nothing further is required of the clone: `roles` already owns and records every one of these at
call time. **If** the integrator wants them inside `loop_plan_id`'s config block rather than
inside a pinned bundle file, the `roles` module's own source digest must be added to
`types.PINNED_SOURCE_PATHS` — which today names six paths, none of them `minireason/loop/*`.

## 5. DECLARED GAP — the guard-block streak counter is defined but unimplemented

**State.** WAVE3-INTERFACE §8 item 1 settles the definition and says `trial` cannot hold it:
`decide.Instrument.block_streak` is the declared integer and **W5-DRIVER must implement the
counter**. The bundle's settled `streak_max_account` states that definition verbatim, so the
account and the counter must agree or the account is false.

**What is needed.** W5-DRIVER counts consecutive guard blocks **per role**, over that role's trials
**in dispatch order within the reading arm**, **reset by any trial of that role whose outcome is
not a block**, and PREFLIGHT asserts that this is the definition in force. Any other definition
(per run, per cell order, not reset) makes `config.audit.streak_max_account` a false account of the
number beside it, and that account is inside `loop_plan_id`.

## 6. DECLARED GAP — the complete `unread` inventory must be produced by the reader

**State.** `report.render_reading_table` unions the plan's undelivered reading-set rows with the
caller's `state.unread`, so a cell the reading set never named can still print as unread — but it
does not compute the set. WAVE3-INTERFACE §8 item 3: **W4-READER must produce `state.unread` as
every cell nothing read**, including cells the reading set never named.

**What is needed for this bundle specifically.** `state.unread` must include all **twelve** C001
occurrence-01 juxtapositions — six endpoint slugs by two arms, counted from the `tables` array of
`occurrence-01/comparison.json` — and not the eleven that remain after setting aside the
`deepseek-flash`/`fcl` one that G10(b) pre-empts. A pre-empted juxtaposition this run never reads
is unread too. `o7`'s trichotomy and `p12`'s non-collapse clause both rest on that inventory being
complete.

---

## Clone-side pins as read at this review

| pin | value | status |
|---|---|---|
| `standard.STANDARD_BODY_SHA256` | `a9007dc73c748cfff974a1a3d77098d380ec153b1b8cf93f513cafa3ea0572d7` | to be re-read at PREFLIGHT after the clone freezes |
| `standard.CEILING_SHA256` | `1e26be087483fd1b9c8e2c403cfae646fb07ebc773f23434a0c4dfab3ed04c1e` | to be re-read at PREFLIGHT after the clone freezes |
| `audits.CALIBRATION_EXCHANGES_SHA256` | `91c29e1e71719d815c21c2697f4aa68a7c983be21df945ad6b1e5042183981e5` | to be re-read at PREFLIGHT after the clone freezes |

The standard body has already moved three times during the review window
(`b4dc7f6a…` → `6c894deb…` → `742c2a0b…` → `a9007dc7…`). **Freeze
`loop-impl/repo/src/minireason/loop/` before the bundle's digests are published and do not accept
further edits until `plan.json` is written.** A plan identity minted over a body that has since
changed is the single failure this apparatus exists to prevent; `PLAN_ID_MISMATCH` on the next
resume is the good outcome and a silent divergence is the bad one.

## What this bundle does NOT ask the clone to change

- **The four extra calibration anchors stay out of the standard body** (PR-21). They are pinned by
  `calibration.json`'s own digest and the bundle says so, precisely so that no clone edit and no
  further move of `STANDARD_BODY_SHA256` is needed now.
- **`obligations.pin()` keeps the file digest.** The review offered the alternative of changing it
  to the canonical-body digest; the bundle takes the other branch and publishes both values with
  their attribution, because the file digest is the only one `custody.verify_pins` can re-derive
  from the tree.
- **`p7` and `o5` were changed in the bundle, not in the program.** Both now read what
  `no_edges_on_studied_nodes` and `audit_in_force` evaluate.
- **Clause 1 needs no change.** `obligations.protected_losses` already implements FW5's
  held-then-failed transition (`was is Verdict.SATISFIED and now is Verdict.NOT_SATISFIED`), which
  supersedes WAVE1-INTEGRATION-DECISIONS item 28(a); the bundle's prose was the half that was
  wrong and it has been corrected.
- **`p4` needs no change.** `obligations.no_scoring_key` already reads record keys and rendered
  headings, and `report` already refuses to emit an artifact carrying one.
- **The block register needs no change.** `report.BLOCK_REGISTER_HEADINGS` already prints ten rows
  including `constitution`; the bundle states where a constitution block is printed rather than
  editing the frozen ceiling text.

---

## v3 disposition (L002), 2026-09-14

Items 1–6 were written against the wave-3/4 staging clone. Read again against the **published**
driver after the first live SEND:

- **Item 1 is now partly satisfied.** S0 stages `calibration.json` under the run root and records
  `plan["calibration_sha256"]`; S1 refuses `CALIBRATION_NOT_FOUND` if the file is absent and
  reports the digest and the anchor count. What is still not done is the audit report carrying that
  digest in `calibration_sha256` for `obligations.audit_in_force` to read at cycle 2 — the half
  `o5` depends on.
- **Item 2 stands.** `plan.json` still does not pin `audits.CALIBRATION_EXCHANGES_SHA256`.
- **Items 3, 4, 5, 6 stand** unchanged.
- **New item 7, forced by the first live run.** Nothing in S0–S15 creates or stages an occurrence,
  and the only stager is `dry_run`'s, which writes synthetic material. A loop that is to dispatch a
  new occurrence of a frozen study therefore needs that occurrence staged by a separate act with
  its own receipt before S0, or a driver entry that stages one from a **named frozen plan** rather
  than from `synthetic`. L002 takes the first road and declares it as a precondition; the second
  would be a driver change and is not asked for here.
- **New item 8.** A publication step that stages no change still emits a `VERIFIED` line
  indistinguishable from one that moved the ref (`0004-PUBLISH_IN` and `0006-PUBLISH_EV` of L001
  named the same commit and tree as `0001-PUBLISH_PLAN`). Recorded as an open defect by
  `REC-20260914-AJ` and not repaired there.
- **New item 9.** Running `preflight` as a diagnostic against a run whose `preflight.json` is
  already published **overwrites** it with the truncated record a refusal writes. It was restored
  byte-for-byte in L001 and the defect is unrepaired: a refusal record needs somewhere else to go.

---

## v4 disposition (L003), 2026-09-15

- **New item 10, and it supersedes item 7's framing.** Runner v2 verifies and dispatches only
  H005-style occurrences (`minireason.h005.material.v1`, its own `plan_body`, `manifests/<tid>.json`,
  `prepare_wave` over problems/templates/cycles/nodes). A loop that is to dispatch for a study of
  another shape needs either a second dispatch seam or a material bridge; neither exists and neither
  is asked for here. L003 sidesteps it by dispatching a **runner-v2-native** study (F001) and marking
  a foreign one (C001) from its **published** bytes, which costs no dispatch at all.
- **Item 7 is otherwise satisfied in practice**: the occurrence is staged by a separate receipt
  (`REC-20260914-AM`) through the runner's own `initialize`, at zero calls. The gap it named — that
  no S-step stages an occurrence — stands unchanged.
- **Items 1–6, 8, 9 stand** unchanged.
