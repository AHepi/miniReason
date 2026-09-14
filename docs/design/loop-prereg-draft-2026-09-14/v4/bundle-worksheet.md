# Bundle-revision worksheet — REVIEW-PREREG PR-01..PR-25

Prepared against `loop-prereg/REVIEW-PREREG.md` (sections A–F). Nothing in the bundle was edited; every byte-involved fact was computed by the scripts under `check/` (see `check/facts.json`). Classification: MECHANICAL (a rename, a recount, a digest, a spelling) or JUDGMENT (an obligation wording, an account, a resource condition, a design choice).

## Standard constants read from `src/minireason/loop/standard.py`

- `STANDARD_BODY_SHA256` (review 15:07 re-verification, still current in the sandbox source's anchor set): `6c894deb851982bf7b5e7317066896a36c4b5898308519c012a3cd1ef5100fcb`
- WAVE2-INTERFACE §9 records two later moves: PR-06 fix → `742c2a0bb239781102a063fcbeae3bbea4c9193e0f78e0310536424c52add839`, mirror re-pin → `a9007dc73c748cfff974a1a3d77098d380ec153b1b8cf93f513cafa3ea0572d7` (no plan was ever minted from any of these).
- `CEILING_SHA256`: `1e26be087483fd1b9c8e2c403cfae646fb07ebc773f23434a0c4dfab3ed04c1e`; recomputed from `src/minireason/loop/data/ceiling_v1.md` in this sandbox: `1e26be087483fd1b9c8e2c403cfae646fb07ebc773f23434a0c4dfab3ed04c1e` (they must equal; see check/facts.json).

`PINNED_SOURCE_PATHS` (parsed from `types.py`, 6 members):
- `src/minireason/data/endpoints.json`
- `src/minireason/graph_import_h005.py`
- `src/minireason/provider_openai_compat.py`
- `src/minireason/use_relation_h005.py`
- `tools/contrast_triple_study.py`
- `tools/multicycle_commitment_study_multi_v2.py`

`types.BLOCK_CODES` has **ten** members; `types.CEILING_BLOCK_REASONS` the **nine** bare ceiling reasons (both parsed from `types.py`).

---

## PR-01 — the bundle's own calibration.json carries a forbidden key, and p4 is protected — **MECHANICAL**

**Review finding (verbatim, first 400 characters):**

> `calibration.json:8`:
> 
> > `"scoring": "An error is an anchor whose observed outcome disagrees with its `error_if` clause, counted per (anchor, seat)…"`
> 
> `scoring` is a member of `standard.FORBIDDEN_KEYS`
> (`['best','better','creativity','grade','grades','merit','novelty','percentile','points','quality','rank','ranking','rank

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/calibration.json",
  "line": 8,
  "text": "\"scoring\": \"An error is an anchor whose observed outcome disagrees ...\""
}
```

**Proposed replacement:**

"error_rule": "An error is an anchor whose observed outcome disagrees ... (body text unchanged; only the key renamed; the review also names `calibration_rule` as an acceptable spelling)"

**Digest consequences (recomputed):**

```json
{
  "calibration.json before": "9ca9ad04672e99becc19096e3de4d4010d9f21c700a979695ef034f9c19aae95",
  "calibration.json after (check/calibration.pr01.json)": "46742f5f22c31d63d3466ab4bd7e3db313cb7b90574a81622036b1b639ca3a67",
  "also changes": "VALIDATION.md calibration row (published 9ca9ad04… stale after the rename) and the o5/ceiling calibration pin language wherever PREREG.md quotes it"
}
```


---

## PR-02 — the obligations sha256 the pre-registration publishes is not the one the plan will pin — **MECHANICAL**

**Review finding (verbatim, first 400 characters):**

> `PREREG.md:104-106`:
> 
> > "`obligations.json` is pinned at sha256
> > `713119a7cd255296058b18084a40cbac7a3353903bbf8cd260b6e78c173e4302` before cycle 1 and may
> > not shift inside this assessment (FW5:787)."
> 
> `obligations.json:296-297` computes that value over the canonical body with the two digest
> keys removed. But the implementation pins the **file**:

**Code side already resolved (WAVE2-INTERFACE.md §10):** **Applied.** `obligations.pin()` keeps the **file** sha256 — it is the only one `custody.pins`/`verify_pins` can re-derive from the tree — and a new `obligations.canonical_pin()` returns the **canonical-body** digest the bundle's prose publishes, so neither value is anonymous.

**Bundle consequence per WAVE2:** **Bundle consequence.** `PREREG.md` §3 must state **both** — the canonical-body digest `713119a7…` and the file digest that enters `loop_plan_id` — and say which is which. Leaving one unnamed is what the review refused.

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/PREREG.md",
  "line": 105,
  "text": "`713119a7cd255296058b18084a40cbac7a3353903bbf8cd260b6e78c173e4302`"
}
```

**Proposed replacement:**

PREREG.md §3 must state BOTH digests and say which is which: the canonical-body digest 713119a7cd255296058b18084a40cbac7a3353903bbf8cd260b6e78c173e4302 (recomputed here from the file with the two digest keys removed: 713119a7cd255296058b18084a40cbac7a3353903bbf8cd260b6e78c173e4302, recipe confirmed by the loader) AND the file digest 2913693abce664af387f1683c7cbfd622043a697343a6d415d89a8179d3652d6 that obligations.pin() folds into loop_plan_id. Exact replacement wording is the reviser's; the two values and the attribution are not.

**Digest consequences (recomputed):**

```json
{
  "file digest (the pin the identity carries)": "2913693abce664af387f1683c7cbfd622043a697343a6d415d89a8179d3652d6",
  "canonical-body digest (reproduces the declared one)": "713119a7cd255296058b18084a40cbac7a3353903bbf8cd260b6e78c173e4302",
  "canonical recipe reproduces declared digest": true
}
```


---

## PR-03 — p7 as written is violated by the loop's own first correct registration — **JUDGMENT**

**Review finding (verbatim, first 400 characters):**

> `PREREG.md:156` / `obligations.json:209`:
> 
> > "**p7** (P) — No reading mints an `att` or `dep` edge on any node under study. **The set of
> > `att` and `dep` edges whose target is an `E_row` or `E_cell` material artifact is empty**…"
> 
> Design §3(d) requires every `A_reading` to carry `dependence` → `E_row`, and §3's
> consequences depend on it: "Invalidate `E

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/obligations.json line 211 (statement) and PREREG.md line 156",
  "text": "No reading mints an `att` or `dep` edge on any node under study. The set of `att` and `dep` edges whose target is an `E_row` or `E_cell` material artifact is empty; every reading's attack targets its own `C_open`, and a declared `rejects-with-reason` relation creates no attack edge while a `re-deploys` relation creates no support edge."
}
```

**Design sentence it must satisfy (quoted):**

```json
{
  "design-s5 line 23": "*p7* no reading mints an `att` or `dep` edge on any node under study.",
  "design-s3 via review (quoted)": "No reading mints an `att` edge on any node under study. **No reading mints a `dep` edge between studied nodes.**"
}
```

**Open question for the reviser (one sentence, no answer proposed):** Will the reviser adopt the review's D(1) ruling text (the implementation's no_edges_on_studied_nodes wording: no `att` targeting a studied node, no studied node the source of any edge, and the reading's `dependence` ref required and not an edge), and name it in the bundle as a change made at pre-registration review?


---

## PR-04 — o5 as written is not the predicate the program evaluates — **JUDGMENT**

**Review finding (verbatim, first 400 characters):**

> `PREREG.md:144` / `obligations.json:83`:
> 
> > "**o5** (O) — An audit report artifact is in force: one registered `AuditReport` whose
> > `cycle` index n satisfies `current_cycle - n < audit.period` (= 2 for this run)…"
> 
> `obligations.py` module note 10:
> 
> > "**o5 does not take ``audit.period``.** The bundle's prose states o5 as a recency
> > comparison, ``current_cycle - n

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/obligations.json line 85 (statement) and PREREG.md line 144",
  "text": "An audit report artifact is in force: one registered `AuditReport` whose `cycle` index n satisfies `current_cycle - n < audit.period` (= 2 for this run), which covers both judge seats named in `config.seats.judges` by endpoint name, and which carries a planted-flaw calibration result computed against the nine calibration rows pinned in `calibration.json` at the sha256 recorded in `plan.json`."
}
```

**Design sentence it must satisfy (quoted):**

```json
{
  "design-s5 line 14": "*o5*: the audit record in force is not older than `AUDIT_PERIOD` cycles.",
  "obligations.py note 10 (quoted)": "**o5 does not take ``audit.period``. The bundle's prose states o5 as a recency comparison, ``current_cycle - n < audit.period``. That is a threshold, and a threshold may not enter a predicate here, so ``audit_in_force`` asks instead whether a registered audit record *declares that it covers the cycle under evaluation*."
}
```

**Open question for the reviser (one sentence, no answer proposed):** Will the reviser adopt the review's D(1) ruling (the implementation's coverage-declaration membership predicate with the two bundle strengthenings retained and the cadence declared but not read), and reconcile the 'nine calibration rows' reference with the re-counted cal-01 set?


---

## PR-05 — p4 is unfalsifiable on the rendered files it names (REVIEW-WAVE1 B1, still open) — **JUDGMENT**

**Review finding (verbatim, first 400 characters):**

> `PREREG.md:153` scopes `p4` to "every artifact the run registers, **every table header and
> every file rendered under the run root**". The implementation, read at 12:0x
> (`obligations.py`, `no_scoring_key`):
> 
> > `"""p4 - no scoring key appears in any registered record."""`
> 
> It calls `_forbidden_hits`, which walks mapping **keys**; `RENDERED_FILES` appears in the
> module only as a constant name (`ob

**Code side already resolved (WAVE2-INTERFACE.md §10):** **Applied.** `obligations.no_scoring_key` now reads two surfaces: the **keys** of every registered record (as before) and the **headings and table header rows** of every file named by the `rendered_files` record.

**Bundle consequence per WAVE2:** **Bundle consequence.** `p4`'s wording may keep "every table header and every file rendered under the run root" — that is now the program — but it should add the quoted-material exemption in the same sentence, so the prose and the predicate are one obligation.

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/PREREG.md",
  "line": 153,
  "text": "No scoring key appears anywhere. `contracts.assert_no_scoring_keys` over every artifact the run registers, every table header and every file rendered under the run root returns no hit, and `SCORING_KEY_FORBIDDEN` is never suppressed."
}
```

**Design sentence it must satisfy (quoted):**

```json
{
  "design-s5 P list line 20": "*p4* no scoring key appears anywhere."
}
```

**Open question for the reviser (one sentence, no answer proposed):** What exact sentence adds the quoted-material exemption (headings and table header rows of files the loop wrote; quoted passages of the material exempt) without narrowing p4's first conjunct?


---

## PR-06 — calibration anchor cal-01 is unsatisfiable by construction and contradicts cal-07 — **JUDGMENT**

**Review finding (verbatim, first 400 characters):**

> `calibration.json` cal-01:
> 
> > `"construction": "The referring record and the target record are the same bytes … The
> > resolvable surface M is that record twice."`
> > `"true_by_construction": "… Any verbatim span of the record resolves inside a declared
> > region, so G2a and G3 are satisfiable."`
> > `"ground_truth": {"relation": "retains", "must_sust

**Code side already resolved (WAVE2-INTERFACE.md §10):** **Confirmed open, then fixed here.** … The anchor is now built **with the referring region alone** — W1-SURFACE's own rule, "a region the row does not carry is absent, not empty" — and the same probe resolves every window uniquely, on `side = referring_record`, inside a declared span.

**Bundle consequence per WAVE2:** **Bundle consequence.** `calibration.json` cal-01 must be re-worded to the referring-region-only construction and its `true_by_construction` clause corrected; `cal-07` keeps the two-copy construction and its `must block` ground truth, and the two are then no longer the same construction with opposite declared outcomes. `VALIDATION.md`'s `calibration.json` digest moves with it.

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/calibration.json row cal-01",
  "construction": "The referring record and the target record are the same bytes: `daily/mini_fcl/cycle01/account#c1` juxtaposed with itself, copied byte-identically from the published use table's `target_record_verbatim`. The resolvable surface M is that record twice.",
  "true_by_construction": "A record retains its own content because it *is* its own content. The ground truth is a property of how the anchor was assembled - one byte string used on both sides - not a reading of it. Any verbatim span of the record resolves inside a declared region, so G2a and G3 are satisfiable.",
  "cal01_still_two_copy": true,
  "cal07_contrast": {
    "true_by_construction": "`M.count(q) == 2` by construction, because the construction placed the second copy there. G2a requires exactly one occurrence and must block. The anchor separates 'the citation is fabricated' from 'the citation is ambiguous'; both are refusals to read, and neither is an absence of relations.",
    "ground_truth": {
      "relation": null,
      "must_sustain": false,
      "expected_outcome": "blocked:referential-integrity"
    }
  }
}
```

**Digest consequences:**

```json
{
  "note": "The module half is applied: standard.CALIBRATION_ANCHORS[0] in this sandbox already reads 'A row read against itself, built with the referring region alone' (parsed from standard.py source, module_anchor_repaired=True), and WAVE2-INTERFACE §9 records STANDARD_BODY_SHA256 moved to 742c2a0b… then a9007dc7…. The bundle half (calibration.json cal-01/cal-07 wording) is open: editing it changes the calibration.json digest 9ca9ad04672e99becc19096e3de4d4010d9f21c700a979695ef034f9c19aae95 and therefore VALIDATION.md's calibration row and every sentence quoting it."
}
```

**Design sentence it must satisfy (quoted):**

```json
{
  "design-s9.1 via review": "\"the only lever … whose ground truth is true by construction\"",
  "W1-SURFACE rule (quoted in WAVE2)": "a region the row does not carry is absent, not empty"
}
```

**Open question for the reviser (one sentence, no answer proposed):** What is cal-01's corrected construction and true_by_construction text now that the module anchor is built with the referring region alone, and does the corrected anchor set change the judge_err_max account's granularity claim?


---

## PR-07 — validate.py no longer runs against the implementation it validates — **MECHANICAL**

**Review finding (verbatim, first 400 characters):**

> Run from the bundle directory at 12:0x with `PYTHONPATH` pointing at
> `loop-impl/repo/src`:
> 
> ```
> PASS  LoopConfig.load(config.json) -> …
> PASS  cycle_budget=3 max_calls=396 provider_mode=live max_per_key=5 publish_ref=None
> PASS  audit={…}
> PASS  contrast={…}
> Traceback … validate.py line 26, in <module>
>     a = loop_plan_id(cfg, pins)
> minireason.loop.types.LoopError: PIN_INVALID: the plan i

**Code side already resolved (WAVE2-INTERFACE.md §10):** **Applied on the module side.** The refusal now names what a caller must supply: `PIN_INVALID: the plan identity is fixed by 6 source pins and pins supplies no digest for N of them: <paths>`.

**Bundle consequence per WAVE2:** **Bundle consequence.** `validate.py` must supply all six pins (the bundle's content is sound on this point; only its harness is stale), and `VALIDATION.md` must be regenerated **before** publication, never after — its `config.json` digest, its `audit={…}` line and its demonstration `loop_plan_id` are all stale, and a published observation is never modified.

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/validate.py",
  "text": "pins = {\"src/minireason/data/endpoints.json\": \"0\" * 64}",
  "pin_map_entries_passed": 1,
  "required_by_types": [
    "src/minireason/data/endpoints.json",
    "src/minireason/graph_import_h005.py",
    "src/minireason/provider_openai_compat.py",
    "src/minireason/use_relation_h005.py",
    "tools/contrast_triple_study.py",
    "tools/multicycle_commitment_study_multi_v2.py"
  ]
}
```

**Proposed replacement:**

Supply all six members of types.PINNED_SOURCE_PATHS in the pin map (the six paths parsed from types.py and listed under current_bytes.required_by_types), each with the file's real sha256 where the file is present or a declared placeholder where it is not; VALIDATION.md must then be regenerated (PR-08). Exact code edit is the reviser's.

**Digest consequences (recomputed):**

```json
{
  "validate.py before": "fd8015261e86cf34cf87f1fd576fd28fb98cc635a7889ee7cb63cb5dde41f25e"
}
```


---

## PR-08 — VALIDATION.md does not describe the bundle it sits beside — **MECHANICAL**

**Review finding (verbatim, first 400 characters):**

> `VALIDATION.md:108` pins `config.json` at
> `46495a6fa0ee5667b6ba5128adbaee9062ed5b6637310bb44b12efdf14c0da90`. Actual:
> `081dd939663156aa3969f3b000fcb0ca4b07086ab4340b0156057903b45b5110`. The other five digests
> still match. `config.json` was edited at 11:13, after `VALIDATION.md` (10:07), to add the
> two `*_account` fields — and `VALIDATION.md:47` still records the pre-ed

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/VALIDATION.md",
  "line": 108,
  "text": "| `config.json` | `46495a6fa0ee5667b6ba5128adbaee9062ed5b6637310bb44b12efdf14c0da90` |",
  "stale_vs_live": {
    "PREREG.md": {
      "published": "c04c2092f672b52572ea98a60575e3405c5072f6b381b9b55a30cb3f7dcd16d6",
      "live": "c04c2092f672b52572ea98a60575e3405c5072f6b381b9b55a30cb3f7dcd16d6",
      "current": true
    },
    "calibration.json": {
      "published": "9ca9ad04672e99becc19096e3de4d4010d9f21c700a979695ef034f9c19aae95",
      "live": "9ca9ad04672e99becc19096e3de4d4010d9f21c700a979695ef034f9c19aae95",
      "current": true
    },
    "config.json": {
      "published": "46495a6fa0ee5667b6ba5128adbaee9062ed5b6637310bb44b12efdf14c0da90",
      "live": "081dd939663156aa3969f3b000fcb0ca4b07086ab4340b0156057903b45b5110",
      "current": false
    },
    "obligations.json": {
      "published": "2913693abce664af387f1683c7cbfd622043a697343a6d415d89a8179d3652d6",
      "live": "2913693abce664af387f1683c7cbfd622043a697343a6d415d89a8179d3652d6",
      "current": true
    },
    "reading_set.json": {
      "published": "ef8c62a5ad6148c4bf676fadabba1ae0504babef26b4f793cce7d80ff37c728e",
      "live": "ef8c62a5ad6148c4bf676fadabba1ae0504babef26b4f793cce7d80ff37c728e",
      "current": true
    },
    "validate.py": {
      "published": "fd8015261e86cf34cf87f1fd576fd28fb98cc635a7889ee7cb63cb5dde41f25e",
      "live": "fd8015261e86cf34cf87f1fd576fd28fb98cc635a7889ee7cb63cb5dde41f25e",
      "current": true
    }
  }
}
```

**Proposed replacement:**

Regenerate VALIDATION.md wholesale (D(3) step 7): the transcript, the digest table for all six files, and a fresh demonstration loop_plan_id over the full pin set. Do not patch it. The live digest table to regenerate against is the one under item 5 of this worksheet.

**Digest consequences (recomputed):**

```json
{
  "config.json published": "46495a6fa0ee5667b6ba5128adbaee9062ed5b6637310bb44b12efdf14c0da90",
  "config.json live": "081dd939663156aa3969f3b000fcb0ca4b07086ab4340b0156057903b45b5110",
  "stale": true,
  "other five rows": {
    "PREREG.md": true,
    "calibration.json": true,
    "obligations.json": true,
    "reading_set.json": true,
    "validate.py": true
  }
}
```


---

## PR-09 — the two mandatory guard-rail accounts are provisional, and one is factually wrong — **JUDGMENT**

**Review finding (verbatim, first 400 characters):**

> `config.json:62`:
> 
> > `"judge_err_max_account": "PROVISIONAL, to be settled at pre-registration review: **the
> > planted-flaw calibration set is five anchors**, so the attainable granularity of a fraction
> > over it is 0.2 and this threshold means 'the first anchor a seat gets wrong ends the reading
> > arm and s

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/config.json",
  "judge_err_max_account_line": 62,
  "streak_max_account_line": 64,
  "text_judge": "PROVISIONAL, to be settled at pre-registration review: the planted-flaw calibration set is five anchors, so the attainable granularity of a fraction over it is 0.2 and this threshold means 'the first anchor a seat gets wrong ends the reading arm and spawns audit-the-reader'; …",
  "text_streak": "PROVISIONAL, to be settled at pre-registration review: twelve consecutive guard blocks is longer than any block run the C001 and H005 published material produced, …"
}
```

**Digest consequences:**

```json
{
  "note": "Any edit to config.json changes its digest (live 081dd939663156aa3969f3b000fcb0ca4b07086ab4340b0156057903b45b5110) and the loop_plan_id; D(2) fixes both accounts at this review, before S0."
}
```

**Design sentence it must satisfy (quoted):**

```json
{
  "design-s5 (guard rails, line 41)": "a guard-block streak above `STREAK_MAX` or a calibration error rate above `JUDGE_ERR_MAX` ⇒ `instrument_fault`, which stops the reading arm and Spawns `audit-the-reader`.",
  "design-s8 line 44": "Changing any of them after first look mints a new `loop_plan_id` and is a new pre-registration, not an amendment to this one.",
  "types.AuditConfig docstring (quoted)": "Each threshold carries an account, and the account is required."
}
```

**Open question for the reviser (one sentence, no answer proposed):** What are the settled judge_err_max and streak_max accounts (and the third account for audit.period) such that no PROVISIONAL string remains in a frozen field and the 0.2-over-nine-rows arithmetic is stated truthfully?


---

## PR-10 — the run's resource conditions are not pre-registered, and the seat evidence is drawn from conditions the run will not reproduce — **JUDGMENT**

**Review finding (verbatim, first 400 characters):**

> The bundle never names a per-call generation ceiling, the 300 s gateway wall, or the
> `thinking` setting. … The run will not use 32768/600. `roles.py` (read at 12:0x) pins, per role,
> `ROLE_MAX_TOKENS = {'critic': 2048, 'defender': 1024, 'judge': 2048, 'marker': 1024,
> 'variator': 4096}` against `wall = min(seat.timeout_seconds, GATEWAY_WALL_SECONDS) =
> min(180, 300

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/PREREG.md",
  "text": "Seats table evidence column (lines 64-68) cites 'max_tokens 32768 / timeout_seconds 600' evidence; nothing in the bundle declares ROLE_MAX_TOKENS, the min(timeout, 300) rule, or the thinking=False-on-deepseek-only rule."
}
```

**Design sentence it must satisfy (quoted):**

```json
{
  "design-s8": "settings, configurations … preserved (AGENTS.md, quoted by the review); ruling 13(d): the driver's planning treats 300 s as the effective wall.",
  "design-s6 ceiling (resources, line 53)": "A reached ceiling is a declared resource boundary, not exhaustion of the inquiry"
}
```

**Open question for the reviser (one sentence, no answer proposed):** How does the bundle declare ROLE_MAX_TOKENS, the min(timeout, 300) gateway-wall rule and the thinking=False-on-deepseek-only rule, and how is the 32768/600 seat evidence restated (or explicitly declared non-transferring) for the 1024–4096/180 conditions the run will actually use?


---

## PR-11 — publish_ref is null and the ruling-2 publication deviation is nowhere in the bundle — **JUDGMENT**

**Review finding (verbatim, first 400 characters):**

> `config.json:9`: `"publish_ref": null`. `types.py` makes it optional and the design's CLI
> defaults it to "the branch's upstream"; in this checkout that resolves to
> `origin/claude/project-state-direction-j5rbun`, which happens to be right. But ruling 2
> requires: "Publication target for this session is branch claude/project-state-direction-j5rbun
> by user mandate. **Every receipt records this a

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/config.json",
  "line": 9,
  "text": "\"publish_ref\": null,"
}
```

**Digest consequences:**

```json
{
  "note": "Setting publish_ref changes config.json's digest and loop_plan_id (D(3) step 3)."
}
```

**Design sentence it must satisfy (quoted):**

```json
{
  "ruling 2 (quoted in review)": "Publication target for this session is branch claude/project-state-direction-j5rbun by user mandate. **Every receipt records this as a deviation**, with main publication pending owner merge."
}
```

**Open question for the reviser (one sentence, no answer proposed):** What explicit publish_ref value, and what deviation sentence in PREREG.md (branch by user mandate, main publication pending owner merge)?


---

## PR-12 — block-code spelling and the block register disagree with types.BLOCK_CODES — **MECHANICAL**

**Review finding (verbatim, first 400 characters):**

> (a) `obligations.json` o1 and o2 admit reasons `"blocked:<code> for a code in
> types.BLOCK_CODES"`. But the members of `types.BLOCK_CODES` already carry the prefix:
> `{'blocked:schema','blocked:referential-integrity','blocked:operative-target', …}`. Read literally the bundle admits `blocked:blocked:schema`. o4
> gets it right; o1 and o2 do not.

**Code side already resolved (WAVE2-INTERFACE.md §10):** **Module side: `types` is the sole owner and there is now one spelling.** `types.BLOCK_CODES` holds the ten codes **with** the `blocked:` prefix; `types.CEILING_BLOCK_REASONS` holds the nine **bare** reasons the frozen ceiling prints, in the ceiling's own order; `types.block_code(reason)` is the only way to build a member and refuses a reason the table does not carry.

**Bundle consequence per WAVE2:** **Bundle consequence, both halves.** (a) `obligations.json` o1 and o2 … must be reworded to o4's spelling — "a `block_code` that is a member of `types.BLOCK_CODES`". (b) The ceiling enumerates nine bare reasons and `BLOCK_CODES` has ten: **`blocked:constitution` has no printed home in the register the ceiling promises**. … the bundle must either add the tenth reason to the printed register or state, in the ceiling's own words, that a constitution block is reported outside it and where.

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/obligations.json",
  "o1_line": 28,
  "o2_line": 42,
  "o1_carries_spelling": true,
  "o2_carries_spelling": true,
  "o4_correct_spell_line": 70,
  "types_BLOCK_CODES_members": [
    "blocked:baseline-forced-same",
    "blocked:constitution",
    "blocked:ensemble-split",
    "blocked:operative-target",
    "blocked:order-swap",
    "blocked:outside-vocabulary",
    "blocked:paraphrase-flip",
    "blocked:provider",
    "blocked:referential-integrity",
    "blocked:schema"
  ],
  "types_CEILING_BLOCK_REASONS": [
    "ensemble-split",
    "referential-integrity",
    "operative-target",
    "order-swap",
    "paraphrase-flip",
    "outside-vocabulary",
    "schema",
    "provider",
    "baseline-forced-same"
  ],
  "prereg_block_register_line": 193
}
```

**Proposed replacement:**

{
  "(a) o1/o2": "Replace `blocked:<code>` for a `code` in `types.BLOCK_CODES` with o4's spelling — a `block_code` that is a member of `types.BLOCK_CODES` — in both o1 (obligations.json line 28) and o2 (line 42).",
  "(b) register": "The ceiling/PREREG.md:193 lists nine bare reasons; types.BLOCK_CODES has ten (blocked:constitution is the extra). Per WAVE2 the fix is to the register: add the tenth reason to the printed register or state, in the ceiling's own words, where a constitution block is reported. No byte replacement is proposed here for (b) — the printed-home wording is judgment."
}

**Digest consequences (recomputed):**

```json
{
  "note": "Editing o1/o2 changes obligations.json's file digest and canonical-body digest (both recomputed at D(3) step 4)."
}
```


---

## PR-13 — the `unread` inventory contradicts itself, 11 against 12 — **MECHANICAL**

**Review finding (verbatim, first 400 characters):**

> `PREREG.md:214`: "more replicates, or **the eleven** C001 occurrence-01 juxtapositions this
> run names `unread`". `PREREG.md:241`: "**The eleven** C001 occurrence-01 juxtapositions …
> are **unread**".
> 
> `obligations.json:19`: "C001 occurrence-01's **12** juxtapositions are referenced by p10 as
> material that must stay unresolved, and

**Current bytes in the bundle:**

```json
{
  "PREREG.md line 214": "- more replicates, or the eleven C001 occurrence-01 juxtapositions this run names `unread`;",
  "PREREG.md line 241": "**The eleven C001 occurrence-01 juxtapositions and everything past the declared boundary are **unread** — unreached by spend.",
  "obligations.json line 19": "C001 occurrence-01's 12 juxtapositions are referenced by p10 as material that must stay unresolved, and are named `unread` - unreached by spend - not `unresolved`."
}
```

**Proposed replacement:**

PREREG.md:214 'the eleven C001 occurrence-01 juxtapositions' -> 'the twelve C001 occurrence-01 juxtapositions'; PREREG.md:241 '**The eleven C001 occurrence-01 juxtapositions' -> '**The twelve C001 occurrence-01 juxtapositions'. Applied to check/PREREG.pr13.md: 2 replacements, 0 'eleven' remaining.

**Digest consequences (recomputed):**

```json
{
  "PREREG.md before": "c04c2092f672b52572ea98a60575e3405c5072f6b381b9b55a30cb3f7dcd16d6",
  "PREREG.md after (check/PREREG.pr13.md)": "f98d0de50a8758a33f487f31fc72b6d567009ba55452e86e5a79cfe0f7e8c494",
  "note": "PREREG.md is also rewritten for other items; this digest is the isolated PR-13-only delta, recomputed on the check/ copy."
}
```


---

## PR-14 — seats were selected by comparing endpoints on a delivery count — **JUDGMENT**

**Review finding (verbatim, first 400 characters):**

> `PREREG.md:78-81`:
> 
> > "**`ollama/glm-5.3` was available and was not taken.** Its C001 occurrence-01 `fcl` arm
> > carried one unresolved cell (19/20) against the other four endpoints' 20/20. That is a
> > recorded difference between occasions, not a ranking (FW5:849); it is written down here
> > because a seat choice made on evidence m

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/PREREG.md",
  "text": "**`ollama/glm-5.3` was available and was not taken.** Its C001 occurrence-01 `fcl` arm carried one unresolved cell (19/20) against the other four endpoints' 20/20. …"
}
```

**Design sentence it must satisfy (quoted):**

```json
{
  "design-s6 ceiling (line 57-58)": "No count is an automatic warrant (FW5:851). … Endpoints are independent occasions to look for one pattern, never competitors (FW5:849).",
  "design-s2.2 via review": "seats are occasions, not contestants"
}
```

**Open question for the reviser (one sentence, no answer proposed):** What one added sentence states that seat selection on delivery evidence is a resource decision made once at pre-registration, never repeated inside the run, and that no seat is compared with another again for any purpose (classified (ii), borderline, per the review)?


---

## PR-15 — clause 1 is stricter than (P), and the bundle contradicts itself about it — **JUDGMENT**

**Review finding (verbatim, first 400 characters):**

> `PREREG.md:117`: "Any *p* fails ⇒ **STOP `protected_loss`**." FW5's conjunct is
> `∀r∈P[r(ξ) ⇒ r(ξ′)]` — only a protected obligation that *held* and then failed is a loss; a
> `p` that never held cannot be lost. `obligations.json`'s own `repair_condition` states the
> FW5 form correctly … while `PREREG.md:117` states the stricter form

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/PREREG.md",
  "line": 117,
  "text": "1. Any *p* fails ⇒ **STOP `protected_loss`**, the loss named and exposed. No continuation, no repair claim."
}
```

**Design sentence it must satisfy (quoted):**

```json
{
  "FW5:791-797 via review": "∀r∈P[r(ξ) ⇒ r(ξ′)] — only a protected obligation that *held* and then failed is a loss",
  "obligations.json repair_condition (quoted in review)": "AND every r in P that held at xi still holds at xi'.",
  "WAVE1-INTEGRATION-DECISIONS 28(a) (quoted)": "clause 1 fires on ANY p reading not_satisfied at ξ′ (not only a satisfied→not_satisfied transition), so a p already failing at cycle 1 stops the chain"
}
```

**Open question for the reviser (one sentence, no answer proposed):** Which reading of clause 1 governs — FW5's held-then-failed form or the implemented any-p-not-satisfied form — such that the two bundle statements become one condition, stated once?


---

## PR-16 — o5 is an obligation about the instrument and hands the run a guaranteed CONTINUE — **JUDGMENT**

**Review finding (verbatim, first 400 characters):**

> FW5:783 defines an obligation as "a specified predicate on a situation and its interpreted
> target", and FW5:785 warns "An obligation is not automatically appropriate because a
> participant adopts it. …" `o5` is "an audit report artifact is
> in force" — a predicate on the loop's own audit record, not on the interpreted target. The
> bundle's own §6 narrative makes the consequence explic

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/PREREG.md",
  "line": 234,
  "text": "cycle 2 runs the one audit window and discharges o5 by its own artifacts"
}
```

**Design sentence it must satisfy (quoted):**

```json
{
  "FW5:785 (quoted in review)": "An obligation is not automatically appropriate because a participant adopts it. The legitimacy of the purpose or requirement can itself be a question."
}
```

**Open question for the reviser (one sentence, no answer proposed):** What sentence states in terms that o5's discharge is a repair of the reader and never a repair concerning the material?


---

## PR-17 — Account (E) absence is correct but silent — **JUDGMENT**

**Review finding (verbatim, first 400 characters):**

> The *absence* is correct but silent. The design's non-goals list is not reproduced in the
> bundle, so a later reader of the published run has no sentence telling them that L001 is not
> evidence about FW5's Account conditions and is not a partial run of A001. Add one line to §6 or
> to the "Not authorised" paragraph: this run tests no

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/PREREG.md",
  "text": "No sentence anywhere in PREREG.md names Account(𝓔) or A001 (the review's grep found nothing)."
}
```

**Design sentence it must satisfy (quoted):**

```json
{
  "review's own instruction": "this run tests no clause of `Account(𝓔)`, and the FW5 Account sufficiency-or-necessity challenge is a separately identified study.",
  "design-s9.2 non-goals via review": "establish … an `Account` predicate"
}
```

**Open question for the reviser (one sentence, no answer proposed):** What one line, placed in §6 or the 'Not authorised' paragraph, states that L001 tests no clause of Account(𝓔) and is not a partial run of A001?


---

## PR-18 — the placeholder receipt id REC-20260914-Z is a live, published id — **MECHANICAL**

**Review finding (verbatim, first 400 characters):**

> `PREREG.md:34`: "**REC-20260914-Z opened at 2026-09-14T00:00:00Z: pre-register the automated
> end-to-end harness loop…**". `docs/DECISION_LEDGER.md:1481` already carries
> "REC-20260914-Z opened at 2026-09-14 11:14 UTC" for F002 occurrence-03 … Use an obviously
> impossible placeholder (`REC-YYYYMMDD-X`) or the literal `<m

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/PREREG.md",
  "line": 34,
  "text": "**REC-20260914-Z opened at 2026-09-14T00:00:00Z: pre-register the automated end-to-end harness loop as a mechanism intervention with its own identity.**"
}
```

**Proposed replacement:**

**REC-YYYYMMDD-X opened at <minted at S0>: pre-register the automated end-to-end harness loop as a mechanism intervention with its own identity.**

**Digest consequences (recomputed):**

```json
{
  "PREREG.md before": "c04c2092f672b52572ea98a60575e3405c5072f6b381b9b55a30cb3f7dcd16d6",
  "PREREG.md after (check/PREREG.pr18.md, this change alone)": "4b8d7a30c567f74d75f6f8abf2742a9f25082e96b7c1bbef9f4d8fd2873d52a8"
}
```


---

## PR-19 — §6's predicted stop clause is probably wrong — **JUDGMENT**

**Review finding (verbatim, first 400 characters):**

> `PREREG.md:234-238` predicts "cycle 3 has nothing new to read … so the mark-triple set is identical to cycle 2's and
> the run stops at clause 4, `no_new_reading_changes`." But o1–o4, o6 and o7 are all
> satisfiable by recorded *reasons* … o5 is discharged at cycle 2; and clause 3 ("all *o* satisfied ⇒ STOP
> `obligations_discharged`") is evaluated **before** clause

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/PREREG.md",
  "lines": "234-238",
  "text": "cycle 2 runs the one audit window and discharges o5 by its own artifacts; cycle 3 has nothing new to read — G11 forbids re-reading an `unresolved` cell without a `reopen_reason` — so the mark-triple set is identical to cycle 2's and the run stops at clause 4, `no_new_reading_changes`."
}
```

**Design sentence it must satisfy (quoted):**

```json
{
  "design-s5 clause order (lines 30-37)": "3. Else, all *o* satisfied ⇒ **STOP `obligations_discharged`**. … 4. Else, this cycle's set of `(cell, register, mark)` triples is identical to the previous cycle's ⇒ **STOP `no_new_reading_changes`**."
}
```

**Open question for the reviser (one sentence, no answer proposed):** Does §6 name clause 3 at cycle 3 as the likely stop (or name both clauses and say why), so the document's prediction is honest?


---

## PR-20 — the C001 leg's outcome is already known offline and should be in §6 — **JUDGMENT**

**Review finding (verbatim, first 400 characters):**

> `WAVE1-INTEGRATION-DECISIONS.md` item 53 reports a program pass over the published
> occurrence-02 bytes: all ten program-computed T/D kind-rows G9-forced to `same`, **zero
> admissible program `differs`**, E forced unresolved by shared bare tokens on six rows, G
> prose-only residue. … it means the
> contrast leg's shape is largely determined before a call is made. Put it in §6's h

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/PREREG.md §6",
  "text": "§6 currently carries no statement of the offline-determined shape of the occurrence-02 contrast leg."
}
```

**Design sentence it must satisfy (quoted):**

```json
{
  "WAVE2 item 53 caveat (quoted)": "The decision's occurrence-02 numbers (ten T/D rows all forced, zero admissible differs, six E rows forced by shared bare tokens) are not reproducible here — occurrence-02 was published after the clone was cut — and must be recomputed by the loop's first run rather than asserted by hand."
}
```

**Open question for the reviser (one sentence, no answer proposed):** How does §6 carry the known-in-advance shape of the occurrence-02 contrast leg (program-computed T/D forced to same, zero admissible differs, E forced on six rows, G residue) without asserting numbers the run has not recomputed?


---

## PR-21 — four of the nine calibration rows name anchors the frozen standard does not carry — **JUDGMENT**

**Review finding (verbatim, first 400 characters):**

> `calibration.json` rows cal-06 (`fabricated-decisive-point`), cal-07
> (`duplicated-passage-non-unique-offset`), cal-08 (`order-swap-sensitive-pair`) and cal-09
> (`paraphrase-invariant-pair`) have no entry in `standard.CALIBRATION_ANCHORS` (which holds
> `self-juxtaposition`, `no-shared-reference`, `quotes-and-rejects`,
> `clean-control-lexical-overlap-only`, `clean-c

**Current bytes in the bundle:**

```json
{
  "module anchor ids (parsed from standard.py)": [
    "self-juxtaposition",
    "no-shared-reference",
    "quotes-and-rejects",
    "clean-control-lexical-overlap-only",
    "clean-control-framing-only-passage"
  ],
  "bundle anchor ids (calibration.json)": [
    "self-juxtaposition",
    "no-shared-reference",
    "quotes-and-rejects",
    "clean-control-lexical-overlap-only",
    "clean-control-framing-only-passage",
    "fabricated-decisive-point",
    "duplicated-passage-non-unique-offset",
    "order-swap-sensitive-pair",
    "paraphrase-invariant-pair"
  ],
  "absent from the standard": [
    "fabricated-decisive-point",
    "duplicated-passage-non-unique-offset",
    "order-swap-sensitive-pair",
    "paraphrase-invariant-pair"
  ],
  "note": "Computed here: four bundle anchors have no entry in the module list, confirming the review's table by recomputation over the sandbox files."
}
```

**Design sentence it must satisfy (quoted):**

```json
{
  "PREREG.md:211 via review": "a successful attack on `std:reading-rubric/v1` … collapses every ν citing it"
}
```

**Open question for the reviser (one sentence, no answer proposed):** Are the four extra anchors added to the standard body (changing STANDARD_BODY_SHA256, pin #1), or does PREREG.md state that the pinned calibration set extends the standard's anchor kinds and is attacked through calibration.json's own pin?


---

## PR-22 — p1's material_sha256 reads like a field name and is a file digest — **MECHANICAL**

**Review finding (verbatim, first 400 characters):**

> `PREREG.md:150` / `obligations.json` p1: "the H005 occurrence-01 `material_sha256` equals
> `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927`". There is no
> `material_sha256` field in `occurrence-01/material.json` … the value is the sha256 of the file, which is correct and which
> I verified. Say "the sha256 of `.../occu

**Current bytes in the bundle:**

```json
{
  "file": "loop-prereg/PREREG.md line 150",
  "text": "… and the H005 occurrence-01 `material_sha256` equals `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927`.",
  "also_in": "loop-prereg/obligations.json p1 statement (line 127)"
}
```

**Proposed replacement:**

… and the sha256 of `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/material.json` equals `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927`. (Same replacement in obligations.json p1 statement.)

**Digest consequences (recomputed):**

```json
{
  "note": "The digest value does not change; both files' digests do (PREREG.md and obligations.json) and are re-registered under D(3)."
}
```


---

## PR-23 — o7 says four states, p12 and the ceiling say three — **JUDGMENT**

**Review finding (verbatim, first 400 characters):**

> `PREREG.md:149` ("exactly
> one of four printed states") and `PREREG.md:161` / the ceiling ("**Three cell states are
> distinct and are printed as three things**"). They are reconcilable — the ceiling's three are
> the non-resolved states and the fourth is "a relation or a mark" — but a reader checking p12
> against o7 has to work that out. One clause in o7 saying so

**Current bytes in the bundle:**

```json
{
  "PREREG.md line 146 (o7)": "- **o7** (O) — Every one of the 38 declared reading-set cells appears in the rendered record under exactly one of four printed states: a relation or a mark; `unresolved` (a deliberate reading that stays unresolved); `machine-unresolved:<block code>`; or `unread` (never dispatched, named as unreached by spend).",
  "PREREG.md line 161 (p12)": "… the three cell states are never collapsed. …",
  "ceiling": "**Three cell states are distinct and are printed as three things.** …"
}
```

**Design sentence it must satisfy (quoted):**

```json
{
  "design-s6 ceiling (line 37)": "**Three cell states are distinct and are printed as three things.** An *unread* cell is one nobody and nothing has read. An *unresolved* cell is a deliberate reading that stays unresolved. A *machine-unresolved* cell is one the guard declined to resolve, and it names the block code that declined it."
}
```

**Open question for the reviser (one sentence, no answer proposed):** What one clause in o7 states that the ceiling's three are the non-resolved states and the fourth is 'a relation or a mark', so p12 and o7 check against each other directly?


---

## PR-24 — STOP_REASONS omits the design's preregistered_condition:<id> — **MECHANICAL**

**Review finding (verbatim, first 400 characters):**

> Design §4.4's
> stop vocabulary includes it; `types.STOP_REASONS` is the seven other tokens. Nothing in this
> run needs it and the omission is probably right, but the bundle should note the deviation
> rather than leave a later reader to diff the design against the enum.

**Current bytes in the bundle:**

```json
{
  "types.py": "STOP_REASONS (line 227) = seven tokens; PREREGISTERED_CONDITION_PREFIX handled by is_stop_reason, not a member of the frozenset.",
  "bundle": "PREREG.md carries no sentence naming the omission."
}
```

**Proposed replacement:**

A note sentence in PREREG.md (a one-line deviation note, e.g. beside the stop-rule section 3 or the 'Not authorised' paragraph): types.STOP_REASONS omits design §4.4's `preregistered_condition:<id>` and the omission is deliberate for this run. Exact wording is the reviser's; the fix is one sentence, no digest-bearing value.

**Digest consequences (recomputed):**

```json
{
  "note": "PREREG.md digest changes; no other file."
}
```


---

## PR-25 — the bundle is written against symbol names in a module it neither enumerates nor pins — **JUDGMENT**

**Review finding (verbatim, first 400 characters):**

> `PREREG.md:46` and `PREREG.md:201` both say the run "closes it to six values", and
> `PREREG.md:227` says "G4 routes anything outside the six-value vocabulary to
> `unresolved:outside-vocabulary`" — but **no file in the bundle lists the six**. … o1 names
> `standard.NOMINABLE_RELATIONS` and `types.BLOCK_CODES`, o2 names `standard.MARKS` and
> `standard.DIFFERENCE_KINDS[<register>]`, o4 and o7

**Current bytes in the bundle:**

```json
{
  "PREREG.md line 46": "this run closes it to six values so the cell is machine-fillable",
  "PREREG.md line 201 (ceiling clause)": "this run closes it to six values and routes anything outside to `unresolved:outside-vocabulary`",
  "note": "No file in the bundle lists the six values, the three marks, the per-register difference-kind sets, or the block-code set; STANDARD_BODY_SHA256 is named by no bundle file."
}
```

**Design sentence it must satisfy (quoted):**

```json
{
  "design-s6 ceiling (line 60-61)": "**Two published instruments were narrowed to make these cells machine-fillable, and the narrowing is part of the claim.**",
  "D(3) step 5 (review)": "the enumerated six values / three marks / difference-kind sets / block codes, and the step-1 `STANDARD_BODY_SHA256` written into §4 beside the ceiling digest (PR-25)"
}
```

**Open question for the reviser (one sentence, no answer proposed):** Where does the bundle enumerate the six values, the three marks, the per-register difference-kind sets and the block-code set (with validate.py asserting each equal to its module constant), and what sentence in PREREG.md §4 names STANDARD_BODY_SHA256 beside the ceiling digest?


---

## 5. Every sha256 the bundle publishes, recomputed

Against the files in this sandbox (`check/collect_facts.py`):

| file | published in VALIDATION.md | recomputed live | status |
|---|---|---|---|
| `PREREG.md` | `c04c2092f672b525…` | `c04c2092f672b525…` | current |
| `calibration.json` | `9ca9ad04672e99be…` | `9ca9ad04672e99be…` | current |
| `config.json` | `46495a6fa0ee5667…` | `081dd939663156aa…` | **STALE** |
| `obligations.json` | `2913693abce664af…` | `2913693abce664af…` | current |
| `reading_set.json` | `ef8c62a5ad6148c4…` | `ef8c62a5ad6148c4…` | current |
| `validate.py` | `fd8015261e86cf34…` | `fd8015261e86cf34…` | current |

Full values:

```json
{
  "stale": [
    "config.json"
  ],
  "current": [
    "PREREG.md",
    "calibration.json",
    "obligations.json",
    "reading_set.json",
    "validate.py"
  ],
  "note": "VALIDATION.md pins config.json at 46495a6fa0ee5667b6ba5128adbaee9062ed5b6637310bb44b12efdf14c0da90; live is 081dd939663156aa3969f3b000fcb0ca4b07086ab4340b0156057903b45b5110 (PR-08). The other five published rows match. The obligations pin published in PREREG.md:105 (713119a7…) is the canonical-body digest; the file digest (what obligations.pin folds into loop_plan_id) is 2913693abce664af387f1683c7cbfd622043a697343a6d415d89a8179d3652d6 (PR-02)."
}
```

Two obligations digests (PR-02), recomputed:

- canonical-body digest: `713119a7cd255296058b18084a40cbac7a3353903bbf8cd260b6e78c173e4302` (reproduces the declared `obligations_sha256` and the value PREREG.md:105 publishes)
- file digest (what `obligations.pin()` folds into `loop_plan_id`): `2913693abce664af387f1683c7cbfd622043a697343a6d415d89a8179d3652d6`

`VALIDATION.md:49`'s demonstration `loop_plan_id` `cc7c137f…` no longer computes (review: `c2806cef…` with the current config and the six required pins); the config digest at `VALIDATION.md` line 108 is stale (PR-08).

---

## 6. Recomputation order — REVIEW-PREREG section D(3), as a checklist

1. **Land the B3 anchor repair and other content fixes in standard.py (deepest pin); read STANDARD_BODY_SHA256 once with the UTC time; confirm CEILING_SHA256 unchanged at 1e26be08… and CEILING_TEXT byte-matches PREREG.md §4.**
   - files that change: `src/minireason/loop/standard.py`, `src/minireason/loop/data/*`
   - digests to re-read afterwards: STANDARD_BODY_SHA256 (pin #1); CEILING_SHA256 (pin #2)
2. **Edit calibration.json: repair cal-01 to the referring-region-only construction (PR-06), rename the scoring key (PR-01), reconcile the 9-anchors count; run contracts.assert_no_scoring_keys over all four bundle JSONs until clean.**
   - files that change: `loop-prereg/calibration.json`
   - digests to re-read afterwards: calibration.json file sha256 (pin #3)
3. **Edit config.json: settle both audit accounts and add an audit.period account (D(2)/PR-09), set publish_ref explicitly (PR-11), declare the resource conditions (PR-10); re-run LoopConfig.load and standard.assert_config_matches_standard.**
   - files that change: `loop-prereg/config.json`
   - digests to re-read afterwards: config.json file sha256 (pin #6)
4. **Edit obligations.json: p7 and o5 rewordings (D(1)/PR-03/PR-04), o1/o2 block-code spelling (PR-12a), o5 calibration-count reference, the 12/eleven reconciliation (PR-13 note line), p1 material_sha256 wording (PR-22); recompute BOTH obligations digests.**
   - files that change: `loop-prereg/obligations.json`
   - digests to re-read afterwards: canonical-body digest replacing 713119a7… (pin #4); file digest replacing 2913693a… — the one obligations.pin folds into the plan (pin #5)
5. **Edit PREREG.md last among content files: §3 names both obligations digests (PR-02), the o5/p7/p10 clause texts, the eleven→twelve inventory (PR-13), seat-evidence restatement (PR-10), publication-branch deviation (PR-11), blocked:constitution register reconciliation (PR-12b), Account(𝓔) non-goal sentence (PR-17), placeholder receipt id (PR-18), the PR-25 enumerations and the step-1 STANDARD_BODY_SHA256 written into §4 beside the ceiling digest; re-assert CEILING_TEXT in PREREG.md and both required-sentence sets, each enumeration equal to its module constant.**
   - files that change: `loop-prereg/PREREG.md`
   - digests to re-read afterwards: PREREG.md file sha256 (pin #7); STANDARD_BODY_SHA256 as quoted in §4 against the step-1 value
6. **Fix and re-run validate.py: supply all six PINNED_SOURCE_PATHS (PR-07), add the assert_no_scoring_keys sweep, assert the obligations file digest equals obligations.pin(), add the anchor unique-resolution probe; require exit 0.**
   - files that change: `loop-prereg/validate.py`
   - digests to re-read afterwards: validate.py file sha256; obligations.json file digest as pin()-checks
7. **Regenerate VALIDATION.md wholesale from that run: transcript, all six file digests, fresh demonstration loop_plan_id over the full pin set. Do not patch (PR-08).**
   - files that change: `loop-prereg/VALIDATION.md`
   - digests to re-read afterwards: every one of the six pinned file digests as regenerated
8. **Only then S0 PREREGISTER: compute the real loop_plan_id over the resolved config plus the six PINNED_SOURCE_PATHS, CEILING.md, the STD_READING body, every prompt template, obligations.json, and each attached study's PLAN.md/material.json; write plan.json; publish before the first call.**
   - files that change: `experiments/loops/<RUN-ID>/plan.json`, `published plan`
   - digests to re-read afterwards: loop_plan_id (pin #8)
9. **Re-verify at S1 PREFLIGHT that STANDARD_BODY_SHA256 still equals the step-1 value; freeze loop-impl/repo/src/minireason/loop/ from step 1 until step 8 completes (single largest operational risk).**
   - files that change: (none)
   - digests to re-read afterwards: STANDARD_BODY_SHA256 against the step-1 value

*End of worksheet. No opinions on the design; no scores.*
