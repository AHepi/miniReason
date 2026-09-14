# REVIEW-PREREG — adversarial review of the L001 pre-registration bundle

Review only. Nothing in the bundle, in `loop-impl/repo` or in `/home/user/miniReason` was
edited by this review; no provider call was made; `.env` and every `*key*` path were left
unopened. The only executions were `python3 validate.py` from the bundle, read-only greps,
and offline probes against `loop-impl/repo/src` recorded inline below.

**Concurrency note.** `loop-impl/repo/src/minireason/loop/` is under live edit by the
hardening agent throughout this review. `types.py` changed at 14:48 UTC *while this review
was running* and invalidated a check that had passed minutes earlier (PR-07). `standard.py`
(11:58), `markprep.py` (11:49), `contracts.py` (11:53), `packs.py` (11:51) and `roles.py`
(11:41) are all newer than `REVIEW-WAVE1.md` (11:45) or close to it. Every implementation
claim below carries the time it was read; re-check them against the tree at S0 PREFLIGHT.

**Re-verification at 15:07 UTC, after `standard.py` (14:50) and `types.py` (15:02) moved
again under this review.** Every finding below still stands unchanged:
`STANDARD_BODY_SHA256` = `6c894deb851982bf7b5e7317066896a36c4b5898308519c012a3cd1ef5100fcb`
(unmoved since 12:0x — the later edits did not touch the body), `CEILING_SHA256` =
`1e26be08…`, `CALIBRATION_ANCHORS` still the same five ids with `self-juxtaposition` first,
`PINNED_SOURCE_PATHS` still six, `assert_no_scoring_keys(calibration.json)` still raises
`SCORING_KEY_FORBIDDEN` (PR-01), and `obligations.pin()` still returns `2913693a…` rather
than the `713119a7…` the pre-registration publishes (PR-02). This review file is itself
inside `validate.py`'s `*.md` glob and passes the standard's forbidden-stop-token scan and
the credential scan.

**Independent mechanical cross-check.** A separate worker pass over the same bundle
(scripts and per-check output under `scratchpad/kimi/prod-runs/p2-prereg-mechanical/`)
confirmed by computation, and I re-confirmed here, that: every seat name, family and
`key_env` matches `endpoints.json` and no two judge seats share a family; the `max_calls`
arithmetic `0 + 108 + 242 + 46 + 0 = 396` equals `config.max_calls`; `cycle_budget = 3`
matches PREREG clause 5; the reading set is 38 = 16 + 22 and matches the `size` block;
|O| = 7, |P| = 12, 19 unique ids with every referenced id present; all four calibration
source paths are tracked files; no credential-shaped token over the bundle; one run id and
one date throughout. It independently reproduced `config.json` at `081dd939…` against
`VALIDATION.md`'s `46495a6f…` (PR-08, and D(3) row #6), and raised one finding I had not
made, adopted here as PR-25.

Read in order: `SESSION_RULINGS.md`; `PURPOSE.md`, `AGENTS.md`;
`design-loop/automated-loop-design.md`; `docs/sources/FW5-explanatory-construction.md`
(located through `docs/reviews/fw5-vs-harness-spec-2026-09-14.md`, which is where the
`R1`–`R10` numbering the design cites is defined — the FW5 source itself uses `[R2]`/`[R5]`
as bibliography markers, not rule names, so "FW5 R8" means that review's R8 at FW5:787–810);
the bundle; `loop-impl/repo/src/minireason/loop/**`,
`loop-impl/WAVE1-INTEGRATION-DECISIONS.md` items 24–54 and `loop-impl/REVIEW-WAVE1.md`.

---

# A. BLOCKERS

## PR-01 — the bundle's own `calibration.json` carries a forbidden key, and `p4` is protected

`calibration.json:8`:

> `"scoring": "An error is an anchor whose observed outcome disagrees with its `error_if` clause, counted per (anchor, seat)…"`

`scoring` is a member of `standard.FORBIDDEN_KEYS`
(`['best','better','creativity','grade','grades','merit','novelty','percentile','points','quality','rank','ranking','ranks','rating','ratings','score','scores','scoring','verdict','weight','weights','win','winner','worse','worst']`).
Probe, against `loop-impl/repo` at 12:0x:

```
contracts.assert_no_scoring_keys(json.load(open('calibration.json')))
-> ScoringKeyForbidden: SCORING_KEY_FORBIDDEN
```

`config.json`, `obligations.json` and `reading_set.json` pass; `calibration.json` does not.

The calibration set is registered at S0 PREREGISTER (design §4.1 S0: "register STD_READING,
kappa_read, GUARD_PROC, DECISION_RULE, **the calibration set** and every C_open artifact")
and `p4` (`PREREG.md:153`, `obligations.json:168`) is protected:

> "No scoring key appears anywhere. `contracts.assert_no_scoring_keys` over every artifact
> the run registers … returns no hit, and `SCORING_KEY_FORBIDDEN` is never suppressed."

So the first live run either refuses at S0 or, if the key survives registration, fails a
protected obligation at the first `decide()` and stops `protected_loss` — a stop caused by
the pre-registration document rather than by anything the run observed. `validate.py` never
runs `assert_no_scoring_keys` over the bundle (it runs only the standard's forbidden-stop-token
scan, `validate.py:168-171`), which is why this passed unnoticed.

**Fix:** rename the key (`error_rule`, `calibration_rule`) and add
`contracts.assert_no_scoring_keys` over every bundle JSON to `validate.py`.

## PR-02 — the obligations sha256 the pre-registration publishes is not the one the plan will pin

`PREREG.md:104-106`:

> "`obligations.json` is pinned at sha256
> `713119a7cd255296058b18084a40cbac7a3353903bbf8cd260b6e78c173e4302` before cycle 1 and may
> not shift inside this assessment (FW5:787)."

`obligations.json:296-297` computes that value over the canonical body with the two digest
keys removed. But the implementation pins the **file**:

`loop-impl/repo/src/minireason/loop/obligations.py`, `pin()`:

> `"""The pin folded into ``loop_plan_id``: the file's sha256 (deviation 1)."""`

Probe: `obligations.pin(load_obligations('obligations.json'))` →
`2913693abce664af387f1683c7cbfd622043a697343a6d415d89a8179d3652d6`
(which is also the file digest `VALIDATION.md:109` records).

Two different digests, one named in the published pre-registration text and the other
folded into `loop_plan_id` and written to `plan.json`. A later reader checking the
pre-registration's declared pin against the plan finds a mismatch and cannot tell whether
`obligations.json` shifted. FW5:787 ("both fixed for that comparison … they must not shift
inside its assessment") is served by a pin only if the pin the record names is the pin the
identity carries.

**Fix:** state both in `PREREG.md` §3 — the canonical-body digest *and* the file digest
that enters `loop_plan_id` — and say which is which; or change `obligations.pin` to the
canonical-body digest and re-derive. Do not leave one unnamed.

## PR-03 — `p7` as written is violated by the loop's own first correct registration

`PREREG.md:156` / `obligations.json:209`:

> "**p7** (P) — No reading mints an `att` or `dep` edge on any node under study. **The set of
> `att` and `dep` edges whose target is an `E_row` or `E_cell` material artifact is empty**…"

Design §3(d) requires every `A_reading` to carry `dependence` → `E_row`, and §3's
consequences depend on it: "Invalidate `E_row` … ⇒ the reading becomes
`suspended_unsupported`, not `refuted`." The implementation says so in as many words —
`obligations.py` module note 11:

> "'No att *or dep* edge lands on a node under study' cannot hold beside W1-GRAPH's
> acceptance clause that refuting `E_row` must leave a reading `suspended_unsupported`,
> which requires exactly a `dep` edge onto `E_row`. … **The bundle's p7 sentence is to be
> reworded to this at the pre-registration review**."

Combined with `WAVE1-INTEGRATION-DECISIONS.md` item 28(a) — "clause 1 fires on ANY p reading
not_satisfied at ξ′ (not only a satisfied→not_satisfied transition), so a p already failing
at cycle 1 stops the chain" — the literal `p7` stops the run at cycle 1 with a false
`protected_loss`. The program that actually runs (`no_edges_on_studied_nodes`) asks a
different pair of questions (no `att` edge targets a studied node; no studied node is the
*source* of any edge), so the pre-registered sentence and the evaluated predicate are not
the same obligation. See §D(1) for the ruling.

## PR-04 — `o5` as written is not the predicate the program evaluates

`PREREG.md:144` / `obligations.json:83`:

> "**o5** (O) — An audit report artifact is in force: one registered `AuditReport` whose
> `cycle` index n satisfies `current_cycle - n < audit.period` (= 2 for this run)…"

`obligations.py` module note 10:

> "**o5 does not take ``audit.period``.** The bundle's prose states o5 as a recency
> comparison, ``current_cycle - n < audit.period``. That is a threshold, and a threshold may
> not enter a predicate here, so ``audit_in_force`` asks instead whether a registered audit
> record *declares that it covers the cycle under evaluation*. … **The bundle's o5 sentence
> must be reworded at its pre-registration review**."

A pre-registration fixes O by its text; the run discharges O by its program. Where they
differ, nothing was fixed. This is the same class as PR-03 and both are unresolved because
the review the implementation defers to is this one. See §D(1).

## PR-05 — `p4` is unfalsifiable on the rendered files it names (REVIEW-WAVE1 B1, still open)

`PREREG.md:153` scopes `p4` to "every artifact the run registers, **every table header and
every file rendered under the run root**". The implementation, read at 12:0x
(`obligations.py`, `no_scoring_key`):

> `"""p4 - no scoring key appears in any registered record."""`

It calls `_forbidden_hits`, which walks mapping **keys**; `RENDERED_FILES` appears in the
module only as a constant name (`obligations.py:328`) and no predicate reads the file text.
`REVIEW-WAVE1.md` B1 demonstrated `p4 → SATISFIED` on a fixture whose `READING_TABLE.md`
carries `| cell | score | rank |`. `obligations.py` has not been edited since 11:07, before
that review (11:45), and `WAVE1-INTEGRATION-DECISIONS.md` item 47 still lists the fix as
pending. As shipped, the protected obligation the design calls G12's whole point cannot
fail on a rendered table — while PR-01 shows the bundle would be caught by the scan that
*is* implemented. The bundle must either narrow `p4`'s wording to what the program does, or
the fix must land before S0; silently publishing the broad wording over the narrow program
is the worse of the two.

## PR-06 — calibration anchor `cal-01` is unsatisfiable by construction and contradicts `cal-07`

`calibration.json` cal-01:

> `"construction": "The referring record and the target record are the same bytes … The
> resolvable surface M is that record twice."`
> `"true_by_construction": "… Any verbatim span of the record resolves inside a declared
> region, so G2a and G3 are satisfiable."`
> `"ground_truth": {"relation": "retains", "must_sustain": true, …}`

The last clause is false. Probe against `surface.py` (unmodified since 10:18), using a real
published row from `use-table-golden/use_table.json` with the target side set to the
referring side's bytes:

```
whole-record count: 2
20-char prefix  count=2  resolve_unique=None
40-char prefix  count=2  resolve_unique=None
80-char prefix  count=2  resolve_unique=None
```

Every substring occurs exactly twice, so no `passage_quote` can satisfy G2(a) and the anchor
blocks `blocked:referential-integrity` on every window, for both seats, forever. This is
`REVIEW-WAVE1.md` B3 verbatim, and it is **not yet fixed**: the anchor text in
`standard.py` (`CALIBRATION_ANCHORS[0]`) still reads "the referring record and the target
record are the same bytes", and `surface.py` is untouched.

Worse, `cal-07` is the *same* construction with the *opposite* declared ground truth:

> cal-07 `"true_by_construction": "`M.count(q) == 2` by construction … G2a requires exactly
> one occurrence and must block."` `"expected_outcome": "blocked:referential-integrity"`

So the bundle pins two anchors whose constructions both yield `count == 2`, one declared
`must_sustain: true` and the other declared `must block`. The calibration set is, per design
§9.1, "the only lever … whose ground truth is true by construction"; a permanently-wrong
anchor inside it consumes over half the headroom to `judge_err_max` (1/9 = 0.111 against
0.2) on every window for reasons that have nothing to do with either seat, and the ceiling's
claim that the audit record `A` means something is thereby false.

**Fix:** build cal-01 with only the referring region present (design's own surface rule:
"A region the row does not carry is absent, not empty"), or state G2(a) per declared region
for `mode: absolute` anchors. Either changes `STANDARD_BODY` or `calibration.json` and
therefore the pins — see §D(3).

## PR-07 — `validate.py` no longer runs against the implementation it validates

Run from the bundle directory at 12:0x with `PYTHONPATH` pointing at
`loop-impl/repo/src`:

```
PASS  LoopConfig.load(config.json) -> …
PASS  cycle_budget=3 max_calls=396 provider_mode=live max_per_key=5 publish_ref=None
PASS  audit={…}
PASS  contrast={…}
Traceback … validate.py line 26, in <module>
    a = loop_plan_id(cfg, pins)
minireason.loop.types.LoopError: PIN_INVALID: the plan identity pins
['src/minireason/graph_import_h005.py', 'src/minireason/provider_openai_compat.py',
 'src/minireason/use_relation_h005.py', 'tools/contrast_triple_study.py',
 'tools/multicycle_commitment_study_multi_v2.py'], which pins names none of
```

`validate.py:25` supplies a one-entry pin map; `types.PINNED_SOURCE_PATHS` (added by the
hardening agent; `types.py` mtime 14:48) now requires six. Supplying the full set, every
remaining check passes and `ALL CHECKS PASSED` is reached — so the bundle's *content* is
sound on this point and only the harness is stale. But as it stands the bundle ships a
validator that exits non-zero, and `VALIDATION.md` records a passing run that cannot be
reproduced. A pre-registration whose own acceptance evidence does not re-run is not
repeatable.

## PR-08 — `VALIDATION.md` does not describe the bundle it sits beside

`VALIDATION.md:108` pins `config.json` at
`46495a6fa0ee5667b6ba5128adbaee9062ed5b6637310bb44b12efdf14c0da90`. Actual:
`081dd939663156aa3969f3b000fcb0ca4b07086ab4340b0156057903b45b5110`. The other five digests
still match. `config.json` was edited at 11:13, after `VALIDATION.md` (10:07), to add the
two `*_account` fields — and `VALIDATION.md:47` still records the pre-edit output:

> `PASS  audit={'period': 2, 'judge_err_max': 0.2, 'streak_max': 12}`

The live run prints those two long account strings. `VALIDATION.md:49`'s demonstration
`loop_plan_id` `cc7c137f…` likewise no longer computes (it is `c2806cef…` with the current
config and the six required pins). Never modify a published observation (AGENTS.md) — so
regenerate `VALIDATION.md` **before** anything is published, not after.

## PR-09 — the two mandatory guard-rail accounts are provisional, and one is factually wrong

`config.json:62`:

> `"judge_err_max_account": "PROVISIONAL, to be settled at pre-registration review: **the
> planted-flaw calibration set is five anchors**, so the attainable granularity of a fraction
> over it is 0.2 and this threshold means 'the first anchor a seat gets wrong ends the reading
> arm and spawns audit-the-reader'…"`

`config.json:64`:

> `"streak_max_account": "PROVISIONAL, to be settled at pre-registration review: twelve
> consecutive guard blocks is longer than any block run the C001 and H005 published material
> produced…"`

Three defects.

(a) **The arithmetic is wrong.** `standard.CALIBRATION_ANCHORS` has five *anchor kinds*;
`calibration.json` materialises **nine rows** (`calls_per_window: 18`, `calls_arithmetic:
"9 anchors x 2 judge seats = 18"`), and `PREREG.md:12` and `o5` both say "nine". At nine
rows the granularity is 1/9 = 0.111, so 0.2 does **not** mean "the first anchor a seat gets
wrong ends the reading arm" — it means the *second* does. The account misstates what the
threshold it accounts for actually does.

(b) **The streak account's premise is unsupported.** C001 and H005 ran no guard and emit no
block register, so "longer than any block run the C001 and H005 published material produced"
compares against a quantity that does not exist in the published record.

(c) **"PROVISIONAL, to be settled at pre-registration review" is published verbatim when
the rail fires.** `decide.py`, `instrument_bound_crossed`:

```
return (f"the guard-block streak reached {streak}, above the declared "
        f"bound {config.audit.streak_max}: "
        f"{config.audit.streak_max_account}")
```

so an `instrument_fault` stop paragraph in `decision.json`, `CYCLE.md` and `CLOSING.md`
would read "…above the declared bound 12: PROVISIONAL, to be settled at pre-registration
review…". See §D(2): a provisional account cannot satisfy the mandatory-account rule, and
because the accounts are fields of the frozen config they are inside `loop_plan_id` —
settling them later is a new pre-registration, not an amendment.

## PR-10 — the run's resource conditions are not pre-registered, and the seat evidence is drawn from conditions the run will not reproduce

The bundle never names a per-call generation ceiling, the 300 s gateway wall, or the
`thinking` setting. `grep -n "300\|gateway\|max_tokens\|thinking"` over the bundle returns
only `CYCLE_OPEN: 300` (a step timeout), two row keys containing the hex substring `a300`,
and one `max_tokens` — inside the *seat evidence* column:

`PREREG.md:64-68`:

> "| `critic` | `ollama/kimi-k3` | … | C001 occurrence-01, both arms at `max_tokens` 32768 /
> `timeout_seconds` 600: 40/40 replicates `COMPLETE`, `unresolved_cells` empty |"

The run will not use 32768/600. `roles.py` (read at 12:0x) pins, per role,
`ROLE_MAX_TOKENS = {'critic': 2048, 'defender': 1024, 'judge': 2048, 'marker': 1024,
'variator': 4096}` against `wall = min(seat.timeout_seconds, GATEWAY_WALL_SECONDS) =
min(180, 300) = 180`, giving a wall ceiling of 8100 tokens. So every seat in this run is
selected on delivery evidence gathered at a 32768-token ceiling and a 600 s clock, and will
be asked at 1024–4096 tokens under a 180 s clock — the very confound `PREREG.md:68` itself
invokes for the variator ("Its 19 PARTIALs in occurrence-01 were at that occurrence's
8192/180 ceiling"). AGENTS.md requires the comparison be respected "under declared
information and resource conditions" and that "settings, configurations" be preserved.

On ruling 13 specifically: the *implementation* handles the wall correctly and explicitly
— `roles.py` GATEWAY_WALL_SECONDS = 300, `min(timeout, 300)` "**the smaller of the two,
never the larger**", and a `TRANSPORT_OR_RESPONSE_ERROR` open ≥ 295 s is recorded with
reason `PROVIDER_GATEWAY_WALL` under block code `blocked:provider`. Nothing in the run can
cross the 300 s wall, because the layer-1 timeout is the endpoint's own 180 s (verified: all
24 `endpoints.json` entries carry `timeout_seconds: 180`, `max_concurrency: 5`) and
`timeouts.step_seconds` may not raise it. **The blocker is that none of this is in the
pre-registration.** A per-call generation ceiling is a declared resource condition; the
design's §8 fixes "the guard parameters" before first look; ruling 13(d) requires the
driver's planning to treat 300 s as the effective wall. The bundle must declare
`ROLE_MAX_TOKENS`, the `min(timeout, 300)` rule and `thinking=False`-on-deepseek-only, and
must restate the seat evidence under the conditions the run will actually use, or say in
terms that the evidence is about delivery at a wider ceiling and does not transfer.

Related and unnamed: four of the five seats (`kimi-k3`, `gpt-oss-120b`, `qwen3.5-397b`,
`gemma4-31b`) are reasoning models and receive no `thinking` control (`roles.py`: "`thinking`
is sent as `False` on a `deepseek`-family seat and is never sent to any other family"), so
reasoning tokens are generated inside a 2048-token judge ceiling. Ruling 13(c) warns
precisely here ("a tool-loop turn rarely needs more than 8–16k … reasoning-heavy turns will
hit the wall"). The foreseeable consequence is truncated JSON → `blocked:schema` at
`schema_repair_budget = 0`, i.e. a block register dominated by an undeclared budget choice.
That is a resource fact that must be pre-registered so it cannot later be read as the
instrument declining on the material.

## PR-11 — `publish_ref` is null and the ruling-2 publication deviation is nowhere in the bundle

`config.json:9`: `"publish_ref": null`. `types.py` makes it optional and the design's CLI
defaults it to "the branch's upstream"; in this checkout that resolves to
`origin/claude/project-state-direction-j5rbun`, which happens to be right. But ruling 2
requires: "Publication target for this session is branch claude/project-state-direction-j5rbun
by user mandate. **Every receipt records this as a deviation**, with main publication pending
owner merge." `grep -niE "branch|publish_ref|deviation|owner merge"` over `PREREG.md` returns
nothing. Publication-before-dispatch (S2/S5/S7/S14) makes the ref load-bearing on every
cycle; a null ref means the run's publication target is a property of whatever checkout it
starts in, which is neither repeatable nor resumable elsewhere, and the required deviation
paragraph is absent. Set `publish_ref` explicitly and add the deviation sentence.

## PR-12 — block-code spelling and the block register disagree with `types.BLOCK_CODES`

(a) `obligations.json` o1 and o2 admit reasons `"blocked:<code> for a code in
types.BLOCK_CODES"`. But the members of `types.BLOCK_CODES` already carry the prefix:
`{'blocked:schema','blocked:referential-integrity','blocked:operative-target',
'blocked:order-swap','blocked:paraphrase-flip','blocked:ensemble-split',
'blocked:outside-vocabulary','blocked:provider','blocked:baseline-forced-same',
'blocked:constitution'}`. Read literally the bundle admits `blocked:blocked:schema`. o4
gets it right ("a `block_code` that is a member of `types.BLOCK_CODES`"); o1 and o2 do not.

(b) The frozen ceiling (`PREREG.md:193`) enumerates **nine** bare codes —
`ensemble-split, referential-integrity, operative-target, order-swap, paraphrase-flip,
outside-vocabulary, schema, provider, baseline-forced-same` — while `BLOCK_CODES` has
**ten**: `blocked:constitution` is missing from the register. o4 requires that "no rendered
file names a block code outside `types.BLOCK_CODES`", and the ceiling names nine strings
that are not members of it. A `blocked:constitution` outcome (G0 unsatisfiable, design
§2.4: "the coordinates are `NOT_DISPATCHED` with an operational reason") therefore has no
printed home in the register the claim ceiling promises — which is exactly the
non-evaluability channel FW5:688 needs kept open (see §C).

## PR-13 — the `unread` inventory contradicts itself, 11 against 12

`PREREG.md:214`: "more replicates, or **the eleven** C001 occurrence-01 juxtapositions this
run names `unread`". `PREREG.md:241`: "**The eleven** C001 occurrence-01 juxtapositions …
are **unread**".

`obligations.json:19`: "C001 occurrence-01's **12** juxtapositions are referenced by p10 as
material that must stay unresolved, and are named `unread`".

Counted from the published bytes: `occurrence-01/comparison.json` carries **12** tables
(and `occurrence-02` one). `reading_set.json` order_rationale item 5 explains the
discrepancy — it counts occurrence-01's `deepseek-flash`/`fcl` juxtaposition separately and
then says "its other eleven" — but that twelfth is *also* unread, since the reading set
names only occurrence-**02**. So all twelve are unread and the PREREG says eleven.

This is not a cosmetic miscount. The claim ceiling's whole trichotomy clause ("An *unread*
cell is one nobody and nothing has read … Conflating any two would let an unfinished
worksheet read as a finding") rests on the unread inventory being complete, and `p10` is a
protected obligation over exactly these cells. Its two other counts do verify exactly:
recomputed from both `comparison.json` files, empty `root_reading` cells = **78** and empty
register-mark cells = **208**, as `p10` states.

## Credentials, human steps, spent coordinates — checked, and what was found

- **No credential value anywhere.** `DEEPSEEK_API_KEY` and `OLLAMA_API_KEY` appear only as
  `key_env` *names* in `PREREG.md:62-68` and in `validate.py`'s own scan. `validate.py:180`
  reads `os.environ.get(env)` to assert the value is absent from the bundle and never prints
  it — acceptable, but note it is the one place the bundle touches a secret at all, and it
  should carry a comment saying the value is compared and never emitted.
- **No retry of a spent coordinate.** `schema_repair_budget: 0` closes the design's one
  repair-coordinate door; `p5` asserts at-most-one response per coordinate and `NO_REPLAY`
  never bypassed; resume is coordinate-grain with `INDETERMINATE` for request-without-response.
  Nothing in the bundle authorises a re-send.
- **Human dependence (ruling 6).** One real instance: the two `PROVISIONAL, to be settled at
  pre-registration review` accounts (PR-09) plus `obligations.py`'s two "must be reworded at
  its pre-registration review" notes (PR-03, PR-04) make three frozen values contingent on a
  review step. That is legitimate *now* — this review is that step — but nothing may remain
  provisional at S0. Otherwise the bundle is clean: the appellate is optional by `p8`, the
  receipt id is minted by `receipts.open_preregistration` under the lock, and no state waits
  on a person.

---

# B. METRIC-CREEP AUDIT (ruling 7)

Classification: **(i)** resource boundary — allowed, reported as a boundary, never as
evidence; **(ii)** guard-rail parameter — allowed only with a mandatory account when it
fires; **(iii)** optimisation target, score, progress meter, success rate or ranking — not
allowed for the orchestrator to impose.

## config.json, field by field

| field | value | class | finding |
|---|---|---|---|
| `cycle_budget` | 3 | (i) | Clean. Clause 5 names it `resource_boundary`; `PREREG.md:126-128` calls it "a declared attention-and-spend boundary, never an adjudication". |
| `max_calls` | 396 | (i) | Clean and unusually well derived (`reading_set.json:max_calls_derivation`, arithmetic `0+108+242+46+0`). `boundary_statement` explicitly refuses to treat it as a prediction. |
| `max_per_key` | 5 | (i) | Clean; mirrors `provider_openai_compat.slots_for`, adds no third gate. |
| `timeouts.step_seconds` (17 entries) | 300–7200 | (i) | Clean. None is a per-call clock; none can raise the endpoint's 180 s (`roles.py` forbids it). |
| `timeouts.git_seconds` | 90 | (i) | Clean; design §4.4 layer 3. |
| `audit.period` | 2 | (ii) | Allowed as a schedule. **No account is attached** — unlike the other two audit parameters. The phase is declared in `reading_set.json:audit_schedule_declaration` ("n mod audit.period == 0 … that is cycle 2 and only cycle 2"), which is good; the account belongs in `config.json` beside it. |
| `audit.judge_err_max` | 0.2 | (ii) | Allowed in kind. **Account fails** — provisional and arithmetically wrong (PR-09a). |
| `audit.streak_max` | 12 | (ii) | Allowed in kind. **Account fails** — provisional, premise unsupported (PR-09b). |
| `seats.min_judge_families` | 2 | (ii) | Clean; pinned equal to `standard.GUARD_PARAMETERS`. |
| `seats.paraphrase_n` | 2 | (ii) | Clean; pinned equal to the standard; enters `roles.max_tokens_for` for the variator. |
| `seats.schema_repair_budget` | 0 | (ii) | Clean; `types` pins the range 0..0, so a raised budget is a successor standard. |
| `reopen_reasons` (3) | — | (ii) | Clean; byte-equal to `standard.REOPEN_REASONS`. |
| `provider_mode` | live | — | Not a number. |

**No (iii) in `config.json`.**

## obligations.json, clause by clause

Every numeral in O and P is an enumeration of a named key set, a digest equality, a
uniqueness predicate or a set-membership test. Checked individually:

- o1 "22 rows", o2 "16 cells", o6 "twelve cross-case cells", o7 "38 declared cells",
  p1 "five ORIGINAL replicates"/"ten recorded digests", p10 "78 … and the 208 …" — all
  **(i)/enumeration**, all over fixed pre-registered key sets, none compared against a
  threshold. p10's two figures verify exactly against the published bytes.
- o3 `M.count(q) == 1`, `E.count(d) == 1`, p5 "at most one response record" —
  uniqueness predicates, not quantities. The `why_not_a_count` note is right that
  "`count == 1` is a uniqueness predicate, not a quantity compared against a threshold".
- o5 `current_cycle - n < audit.period` — **(ii)**, a recency comparison on a cycle index,
  i.e. an attention/schedule parameter. Permitted under ruling 7 as a bound on the
  instrument's cadence, **not** creep. (The implementation disagrees and refuses it as a
  threshold-in-a-predicate; that disagreement is PR-04, a text-vs-program problem, not a
  metric problem.)
- o4 "The register prints counts; **this obligation reads the headings, never the counts**"
  — exemplary discipline; the block-register counts are information (FW5:851) and no clause
  reads them.
- `no_clause_is_a_count` (`obligations.json`) correctly carves out the two places a number
  *is* read — "The block register and the audit error rate are printed for a reader and read
  by the instrument-fault guard rail, which is a declared threshold on the instrument's own
  behaviour and is not a clause of this repair condition."

**No (iii) in `obligations.json`.**

## calibration.json

- `calls_per_window: 18`, `calls_arithmetic` — **(i)**, clean.
- Per-row `ground_truth` / `error_if` — not metrics; each is a constructed truth plus a
  disagreement predicate.
- `anchor_coverage` — a coverage map by anchor kind, not a score.
- **`scoring` (the key itself)** — PR-01. Beyond being forbidden, the *name* is the creep
  shape the repository's own guard exists to catch; the body disclaims what the key name
  asserts.
- **FLAG (iii)-adjacent — the error rate is defined per seat.** `calibration.json:8`:
  "counted **per (anchor, seat)**". `decide.py` (`instrument_bound_crossed`) says the
  opposite in its docstring: "Both are panel-level signals … **neither is computed per
  seat**". A per-seat error rate over a shared anchor set is one join away from a ranking of
  endpoints, which FW5:849 and the design's §2.2 ("seats are occasions, not contestants")
  forbid. The bundle should define the quantity at panel grain to match `decide.py`, or say
  in the pre-registration that the per-seat decomposition is recorded for the audit arm and
  is never compared across seats.

## The PREREG stop rule

- Clause 4 is a **set-identity** test on `(cell, register, mark)` triples, not a count —
  correct, and `PREREG.md:124-125` says so.
- Clause 5 names `cycle_budget` and `max_calls` as a boundary, with the ceiling sentence
  the ceiling's own "A reached ceiling is a declared resource boundary" clause.
- Guard rails are evaluated before clauses 1–5 and are stated as instrument faults
  ("a fault in the instrument, never a finding about the material").
- `PREREG.md:143-149` ("No clause is a count") enumerates the permitted predicate shapes and
  the claim holds on inspection.

**Ruling 7's named item is correctly absent.** The design's §9.1 sentence — "The
pre-registration names the unresolved rate at which the instrument would be judged not worth
running again" — does **not** appear in the bundle. `grep -niE "unresolved rate|success
rate|progress meter|worth running again"` returns nothing. Ruling 7's "candidate for
removal" was removed.

**Nothing turns "mostly unresolved" into a failure condition.** The opposite:
`PREREG.md:222-238` ("This run may resolve very little, and that is the instrument's reach,
not evidence about the material … A table that is mostly `unresolved` and
`machine-unresolved` at the end of that is the rule working") and `PREREG.md:247`
("**Success for this pre-registration is not that any cell filled.**"). No clause reads the
number of resolved cells.

## One further (iii) candidate the orchestrator should rule on

**PR-14 — seats were selected by comparing endpoints on a delivery count.**
`PREREG.md:78-81`:

> "**`ollama/glm-5.3` was available and was not taken.** Its C001 occurrence-01 `fcl` arm
> carried one unresolved cell (19/20) against the other four endpoints' 20/20. That is a
> recorded difference between occasions, not a ranking (FW5:849); it is written down here
> because a seat choice made on evidence must show the evidence it was made on."

The disclaimer is the right one and the transparency is exactly what the record should
carry. But the operation performed *is* a selection over endpoints driven by a quantity
(20/20 against 19/20), and the seat table's entire "evidence" column is per-endpoint
delivery counts. Under ruling 7 this is defensible as a bound on the **instrument** —
delivery completeness is a resource fact, not a reading's standing — and it is not an
optimisation target, since nothing in the run re-ranks or re-selects. Classify **(ii),
borderline**, and record it as such: the danger is not this run but the precedent that a
seat may be dropped for a delivery figure. Recommend one added sentence: that seat selection
on delivery evidence is a resource decision made once at pre-registration, is never repeated
inside the run, and no seat is compared with another again for any purpose. Also note the
smaller point that PR-10 raises: those delivery figures were obtained at 32768/600 and do
not transfer to 180 s.

---

# C. FW5 CONFORMANCE

## The stop rule against R8 (FW5:787–810)

FW5:787: "Let \(O\) be the explicitly claimed repair obligations and \(P\) the protected
obligations for a comparison, both fixed for that comparison. … they must not shift inside
its assessment." FW5 (P) reads
`∃o∈O[¬o(ξ) ∧ o(ξ′)] ∧ ∀r∈P[r(ξ) ⇒ r(ξ′)] ∧ ProducedBy(Δ,ξ,ξ′;O)`.

Clause 2 is faithful: "≥1 *o* failed at ξ and is satisfied at ξ′, **and** the artifacts
making it satisfied were registered by this cycle (`ProducedBy` discharged, not temporal
succession)" — FW5:800 in the terms FW5:800 uses. `losses_outside_P` "present even when
empty" is FW5:802. The net-withdrawal sentence is FW5:810. The `transport` field of
`obligations.json` answers FW5:800's "A transport supplies the interpretation of o and r
across changed representations; without one they are not silently compared" by naming the
key maps in `reading_set.json`. All good.

**PR-15 — clause 1 is stricter than (P), and the bundle contradicts itself about it.**
`PREREG.md:117`: "Any *p* fails ⇒ **STOP `protected_loss`**." FW5's conjunct is
`∀r∈P[r(ξ) ⇒ r(ξ′)]` — only a protected obligation that *held* and then failed is a loss; a
`p` that never held cannot be lost. `obligations.json`'s own `repair_condition` states the
FW5 form correctly:

> "AND every r in P that held at xi still holds at xi'."

while `PREREG.md:117` states the stricter form, and `WAVE1-INTEGRATION-DECISIONS.md` item
28(a) confirms the implementation follows the stricter one ("clause 1 fires on ANY p reading
not_satisfied at ξ′ … so a p already failing at cycle 1 stops the chain"). Two consequences:
the bundle's two statements of the repair condition are not the same condition, and the
implemented one is not R8's. Being stricter is not automatically safe — it converts a
never-held protection into a false `protected_loss`, which is precisely how PR-03 fires.
Decide which reading governs, state it once, and make the other match. (`not_evaluable`
correctly never terminates — `decide.py`: "an obligation answering `not_evaluable` never
terminates the chain", printed as `protected_not_evaluable`, which is FW5 R5 handled well.)

**PR-16 — o5 is an obligation about the instrument, discharged by the instrument's own
artifacts, and it hands the run a guaranteed CONTINUE.** FW5:783 defines an obligation as "a
specified predicate on a situation and its interpreted target", and FW5:785 warns "An
obligation is not automatically appropriate because a participant adopts it. The legitimacy
of the purpose or requirement can itself be a question." `o5` is "an audit report artifact is
in force" — a predicate on the loop's own audit record, not on the interpreted target. The
bundle's own §6 narrative makes the consequence explicit (`PREREG.md:234-236`): "cycle 2 runs
the one audit window and **discharges o5 by its own artifacts**". Under clause 2 that is a
CONTINUE the run can always manufacture, independent of anything read. It is not fatal —
the audit genuinely is a repair of the instrument, and the design wants the instrument under
repair — but the pre-registration should say in terms that o5's discharge is a repair of the
reader and never a repair concerning the material, so that a later reader cannot read
"an obligation was discharged, therefore progress" across the two.

**O and P are stated as obligations, not counts.** Every *o* is "the graph holds either (a)
… or (b) …" over a named key set; every *p* is a preservation or a prohibition ("remain",
"stays complete", "no …", "at most one", "still at the sha"). No clause is a tally. This is
the part of the bundle that is strongest.

## The three-case contrast (FW5:630) — survives, and is not collapsed

FW5:630: "Its contrast contract must include a content-changing case, a content-preserving
recoding, and the distinction between a change in the objection and an irrelevant carrier
disturbance wherever those distinctions are claimed."

It survives structurally, in the C001 leg rather than in the vocabulary:
`config.json:17-28` carries `original-vs-control` (D1, content-changing),
`original-vs-recoding` (F2, content-preserving recoding) and `original-vs-carrier` (F3,
carrier disturbance), each over all four PLAN §8a registers, with `standard.FALSIFIER_MAP`
mapping D1/F2/F3 to carrying registers `(T, E, D)` and excluding G from all three.
`reading_set.json` order_rationale item 3 keeps them in falsifier order.

The **reading vocabulary** is separately intact at six values and is not where the three-case
contrast lives. Verified byte-identical:
`use_relation_h005.ROOT_READING_VOCABULARY == standard.READING_VOCABULARY ==
('re-deploys','qualifies','rejects-with-reason','repairs','retains','unresolved')`, with
`NOMINABLE_RELATIONS` the first five and `none` handled as a critic *answer* rather than a
vocabulary member. Note for the record: the design's §2.3 critic schema lists the sixth
enum value as `none`, where the published vocabulary's sixth is `unresolved`; the
implementation resolves this correctly and the bundle inherits the correct form through
`standard.py`. No collapse.

One thing the bundle should say and does not: this run reads the three-case contrast on
**one** juxtaposition (`occurrence-02`, `deepseek-flash`, `fcl`), and
`WAVE1-INTEGRATION-DECISIONS.md` item 53 already reports, from an offline program pass over
those published bytes, that "all ten program-computed T/D kind-rows are G9-forced to `same`
because the within-ORIGINAL replicate spread already exhibits those kinds; **zero admissible
program `differs`**; E forced unresolved by shared bare tokens on six rows; G prose-only →
residue." That is a known-in-advance shape of the contrast leg and belongs in §6's honest
expectation, so that the run's C001 output cannot later read as a finding about the
material. See PR-20.

## Non-evaluability (FW5:688) — has a home, with one gap

FW5:688: "Eligibility is a separate predicate. … **The inability to evaluate a proposition is
not a falsifying observation of the proposition.**"

It has several homes and they are kept distinct, which is the design's best work:
the ten `types.BLOCK_CODES`; the closed reason sets in o1 (`critic-none`,
`unresolved:outside-vocabulary`, `NOT_DISPATCHED`, `INDETERMINATE`, `unreached`) and o2
(`program-computed`, `baseline-forced-same`, `under-replicated`, `bare-token-ambiguity`,
`byte-identity-defeater`, `unreached`); and o7's four printed states, of which
`machine-unresolved:<block code>` and `unread` are the non-evaluability channels. The ceiling
carries "Ended arms, guard blocks, PARTIAL deliveries, bare-token ambiguity and
under-replication are silent about content; non-evaluability is not refutation."

**Gap:** `blocked:constitution` has no home in the printed register (PR-12b), and the bundle
never cites FW5:688 anywhere — every FW5 citation in the bundle is :628 (×3, all denials),
:634, :787, :800, :802, :810, :849 (×2), :851. Add the :688 anchor beside the block-code set
so a later reader can check the rule at its source.

## FW5:628 — nothing claims the witness

All three occurrences are denials: `PREREG.md:183` (the ceiling's own sentence, "**This run
cannot claim FW5:628's witness of reason use**"), and `calibration.json` cal-04, which cites
:628's "must preserve internal role bindings" as the requirement a lexical overlap fails.
`PREREG.md:42` states the same in the receipt paragraph. Correct and consistent.

## Account (E) (FW5:172–:228) — not referenced, and not conflated

The bundle contains no reference to `Account(𝓔)`, anchoring, fidelity, question fidelity,
non-circular dependence or non-vacuity. That is the right outcome: ruling 9(b) stages the
"Account sufficiency or necessity challenge" as a **separate** study (A001) with its own
claim, dependencies, grain, boundary, contrasts and relinquishment fixed before evidence,
and the design's §9.2 non-goals include "establish … an `Account` predicate". Nothing in
L001 bears on A001 and nothing in the bundle suggests it does.

**PR-17 (should-fix, recorded here because it belongs to this section).** The *absence* is
correct but silent. The design's non-goals list is not reproduced in the bundle, so a later
reader of the published run has no sentence telling them that L001 is not evidence about
FW5's Account conditions and is not a partial run of A001. Add one line to §6 or to the
"Not authorised" paragraph: this run tests no clause of `Account(𝓔)`, and the FW5 Account
sufficiency-or-necessity challenge is a separately identified study.

---

# D. THE THREE ITEMS THE INTEGRATOR FLAGGED

## D(1) — `p7` and `o5`: is the rewording faithful?

### `p7` — the bundle's rewording is **not faithful; it is wrong, and it must change**

Design §5 P: "*p7* no reading mints an `att` or `dep` edge on any node under study."
Design §3, which is the precise statement: "No reading mints an `att` edge on any node under
study. **No reading mints a `dep` edge between studied nodes.**"

Those are different. §3 forbids a `dep` edge *between two studied nodes* — the error
FW5:653 names and the design says "this programme has already made once": promoting a
declared `rejects-with-reason` into an adjudicative edge between the referring record and
the target record. §5's compressed phrasing drops "between studied nodes", and the bundle
took the compressed phrasing and made it a program predicate over *edge targets*:

> `obligations.json:209` — "The set of `att` and `dep` edges whose target is an `E_row` or
> `E_cell` material artifact is empty"

That forbids the `dependence` ref from `A_reading` to `E_row` that design §3(d) *mandates*
and on which §3's "orphaned is not false" consequence depends. The bundle's p7 is therefore
narrower than the design in one direction (it says nothing about edges whose *source* is a
studied node, so a `dep` from material to a reading passes) and fatally wider in another (it
forbids the required dependence). The implementation's `no_edges_on_studied_nodes` gets both
directions right, and says so:

> `obligations.py` note 11 — "``no_edges_on_studied_nodes`` therefore asks two questions: no
> ``att`` edge may target a studied node, and no studied node may be the *source* of any
> edge. A ``dep`` from a reading to the material it reads is permitted, and is what makes a
> refuted material orphan the reading rather than refute it. … the protection is not
> weakened, because the two directions that could hide a change to the material are both
> refused."

**Ruling for this review: adopt the implementation's wording.** It is faithful to design §3
and to FW5:653's actual concern (a declared relation must not become an adjudicative edge),
it is strictly stronger than the design's §5 sentence on the source side, and it is the only
version under which the run can register a legal reading at all. Rewrite `p7` in
`obligations.json` and `PREREG.md:156` as:

> *p7* — No reading mints an `att` edge on any node under study, and no node under study is
> the source of any edge. A reading's `dependence` ref onto its `E_row`/`E_cell` is required
> and is not an edge on a node under study in the sense this clause protects: it is what
> makes a refuted material leave the reading `suspended_unsupported` rather than refuted.
> A declared `rejects-with-reason` creates no attack edge and a declared `re-deploys` creates
> no support edge.

Also record in the pre-registration that this differs from design §5's compressed sentence
and why, since the design is the document of record.

### `o5` — the bundle's statement is **defensible in substance but is not what runs; adopt the implementation's, and keep the schedule visible**

Design §5 O: "*o5*: the audit record in force is not older than `AUDIT_PERIOD` cycles."
The bundle renders that as `current_cycle - n < audit.period` plus two genuine
strengthenings — that the report covers both named judge seats, and that it carries a
planted-flaw result against the pinned calibration set. Those strengthenings are good and
should survive.

The recency comparison, however, is not evaluated. `obligations.py` note 10 replaces it with
a coverage-declaration membership test on the ground that "a threshold may not enter a
predicate here". On the metric-creep question I disagree with that reasoning — a recency
comparison on a cycle index is a cadence/attention parameter, class (ii), and ruling 7
expressly permits bounds "on the instrument"; the bundle's own `no_clause_is_a_count`
lists "a recency comparison on a cycle index" among the permitted shapes. But the
*engineering* argument is sound and decides it: the cadence that mints audit records is the
driver's, the obligation should read what the record declares rather than recompute the
schedule, and a predicate that reads `config.audit.period` couples O to a config field in a
way that makes "O is fixed" harder to check.

**Ruling for this review: adopt the implementation's predicate, keep the bundle's two
strengthenings, and keep the schedule declared in the bundle where it already is.** Rewrite
`o5` as:

> *o5* — An audit report artifact is in force: some registered `AuditReport` declares that
> its coverage includes the cycle under evaluation; it names both judge seats of
> `config.seats.judges` by endpoint name; and it carries a planted-flaw calibration result
> computed against the calibration rows pinned in `plan.json` at their recorded sha256.
> Absence of any audit report fails this obligation, which is its state at the opening
> situation. The cadence that mints records — `audit.period = 2`, phase `n mod period == 0`,
> so cycle 2 and only cycle 2 inside `cycle_budget = 3` — is a declared attention-and-spend
> parameter recorded in `reading_set.json:audit_schedule_declaration` and reported, not read
> by this predicate.

Fix the "nine calibration rows" reference so it agrees with `config.json`'s account
(PR-09a), and add the sentence PR-16 asks for.

**Neither rewording may be made silently.** Both change the text of a document whose sha256
is pinned into `loop_plan_id`; both must be made *before* S0, and both must be named in the
pre-registration as changes made at pre-registration review with the reasons above — because
after S0 the same change is a new `loop_plan_id` and a new pre-registration, never an
amendment.

## D(2) — what exactly is "provisional", and can a provisional account satisfy the mandatory-account rule?

**What is provisional.** Exactly two strings, both in `config.json`, both first-class fields
of `types.AuditConfig` (neither has a default — "a threshold that appears by default was
never pre-registered", `VALIDATION.md:26`), and therefore both inside
`config.canonical_bytes()` and inside `loop_plan_id`:

- `config.json:62` `audit.judge_err_max_account` — provisional, and its substantive claim
  ("the planted-flaw calibration set is five anchors", so 0.2 means the first wrong anchor
  fires the rail) is **false** for the set actually pinned: `standard.CALIBRATION_ANCHORS`
  holds five anchor *kinds*, `calibration.json` materialises nine rows, `calls_per_window` is
  18, and at nine rows 0.2 fires on the second error, not the first.
- `config.json:64` `audit.streak_max_account` — provisional, and its premise ("longer than
  any block run the C001 and H005 published material produced") refers to a quantity the
  published material does not contain, since neither study ran a guard or emitted a block
  register.

Nothing else in the bundle is marked provisional. `audit.period` carries no account at all.

**Can a provisional account satisfy the mandatory-account rule? No, on three independent
grounds.**

1. **It is published verbatim as the reason the run stopped.** `decide.py`
   `instrument_bound_crossed` interpolates the account string into the stop prose, which
   lands in `decision.json`, `CYCLE.md` and `CLOSING.md`. A closing record reading "above the
   declared bound 12: PROVISIONAL, to be settled at pre-registration review…" is not an
   account of why the rail fired; it is a note that the parameter was never accounted for.
   The design requires the rail to be "rendered attackable rather than merely declared"
   (`decide.py`, citing R9) — an unsettled account is unattackable, because there is nothing
   yet to attack.

2. **It cannot be settled later.** The accounts are inside `loop_plan_id`. Editing either
   after S0 mints a new plan identity and is a new pre-registration (design §8: "Changing any
   of them after first look mints a new `loop_plan_id`"). So "to be settled at
   pre-registration review" is only true if the review happens **before** S0 — which is now
   — and is false the moment the plan is published. A frozen document may not contain a
   promise to change itself.

3. **It is a dependence on a step outside the loop (ruling 6).** The harness "must run end
   to end without a human in the loop … a human is an optional appellate, never a required
   step." A config whose guard-rail accounts declare themselves contingent on a review makes
   a human step a precondition of the record being honest, even though it is not a
   precondition of the run executing.

**Ruling:** both accounts must be settled in this review and the word PROVISIONAL removed.
Concretely: recompute `judge_err_max`'s account against the nine pinned calibration rows and
state plainly what 0.2 does over nine (fires on the second disagreeing anchor, not the
first) — or, if the intent really was "the first error ends the arm", set the bound below
1/9 and say so. Replace `streak_max`'s empirical premise with one that can be checked: there
is no published block run to compare against, so the honest account is that 12 is chosen as
a length no legitimate stretch of the 38-cell reading set is expected to produce and that
the figure is itself attackable on the first run's block register. Add a third account for
`audit.period = 2`. And after PR-06 is fixed, re-check the `judge_err_max` account against
whatever the corrected anchor set is.

## D(3) — what changes when the standard body changes, and the exact recomputation order

**First, the state of the pin as read at 12:0x.** `standard.STANDARD_BODY_SHA256` is now
`6c894deb851982bf7b5e7317066896a36c4b5898308519c012a3cd1ef5100fcb`. It is **not**
`b4dc7f6a…`, the value `WAVE1-INTERFACE.md:414` records. `CEILING_SHA256` is
`1e26be087483fd1b9c8e2c403cfae646fb07ebc773f23434a0c4dfab3ed04c1e` and `CEILING_TEXT` is
still byte-identical to `PREREG.md` §4 (the patched validation reached
`PASS PREREG.md contains standard.CEILING_TEXT byte-for-byte, all 11
CEILING_REQUIRED_SENTENCES, all 10 PREREGISTRATION_REQUIRED_SENTENCES`), so whatever moved
the body did not touch the ceiling.

**Second, and this is the key fact: no bundle file names any of these digests.**
`grep -rn "b4dc7f6a\|6c894deb\|1e26be08\|d735be9a"` over `loop-prereg/` returns nothing, and
`WAVE1-INTERFACE.md:414` says the same — "`STANDARD_BODY_SHA256` moving to `b4dc7f6a…` — no
wave-1 module **or bundle file** names it." The `loop_plan_id` `d735be9a…` named in the
review brief does not appear anywhere in the scratchpad; the only plan id in the bundle is
`VALIDATION.md:49`'s demonstration digest `cc7c137fbcb37b4f…`, explicitly labelled
"a **demonstration digest only** … taken over a one-entry placeholder pin map"
(`VALIDATION.md:113-115`). Treat `d735be9a…` as not-in-this-bundle and do not chase it.

**Third, B3 is not yet fixed** (PR-06), so the standard body is going to move again. The
anchor's own text in `standard.CALIBRATION_ANCHORS[0]` still reads "the referring record and
the target record are the same bytes", `surface.py` is unmodified since 10:18, and the probe
above still returns `count == 2` / `resolve_unique = None` for every span.

### Every pin and derived id, and what depends on what

| # | pin / id | where it lives | moves when |
|---|---|---|---|
| 1 | `standard.STANDARD_BODY_SHA256` | computed from `build_standard()`; **named by no bundle file** — PR-25 asks that `PREREG.md` §4 carry it | any edit to the rubric text, the six-value vocabulary, the PLAN §8a mirror, the difference-kind sets, `GUARD_PARAMETERS`, `REOPEN_REASONS`, the falsifier map, **or the calibration anchors** (the B3 fix) |
| 2 | `standard.CEILING_SHA256` | `data/ceiling_v1.md`; body reproduced at `PREREG.md:180-206` | any edit to the ceiling text — none is required by B3 |
| 3 | `calibration.json` file digest | `VALIDATION.md:107` (`9ca9ad04…`) | the cal-01 repair (PR-06), the `scoring` rename (PR-01) |
| 4 | `obligations.json` canonical-body digest | `obligations.json:296`, `PREREG.md:105` (`713119a7…`) | the `p7` and `o5` rewordings (D(1)), the o1/o2 block-code spelling (PR-12a), the o5 "nine rows" reference |
| 5 | `obligations.json` file digest | `VALIDATION.md:109` (`2913693a…`); **this is what `obligations.pin()` folds into the plan** (PR-02) | same edits as #4, plus any whitespace change |
| 6 | `config.json` file digest | `VALIDATION.md:108` (`46495a6f…`, already stale — actual `081dd939…`) | the account rewrites (D(2)), `publish_ref` (PR-11), any declared `max_tokens` (PR-10) |
| 7 | `PREREG.md`, `reading_set.json`, `validate.py` file digests | `VALIDATION.md:106,110,111` | any edit to those files |
| 8 | `loop_plan_id` | minted at S0 into `plan.json`; only a **demonstration** value is in the bundle (`VALIDATION.md:49`) | **any** of #1–#7 plus the six `types.PINNED_SOURCE_PATHS` entries, `CEILING.md`, every prompt template, and each attached study's `PLAN.md` and `material.json` |
| 9 | the C001 within-ORIGINAL baseline sha256 | minted at S11 into `plan.json` and carried by every cross-case call record (o6, p9) | not affected by the standard body; it is sealed inside the run |

### The exact recomputation order

Run strictly top to bottom; each step's inputs are frozen by the steps above it. Steps 1–5
are bundle edits and must all be complete before step 6.

1. **Land the B3 anchor repair and the other content fixes in `standard.py` first**, because
   the standard body is the deepest pin. Build cal-01 with one region present (or make G2(a)
   region-local for `mode: absolute` anchors), and land whatever else the hardening agent is
   applying to the body. Then read `standard.STANDARD_BODY_SHA256` once and record it with
   the UTC time; it is pin #1. Confirm `CEILING_SHA256` is unchanged at `1e26be08…` and that
   `CEILING_TEXT` still matches `PREREG.md` §4 byte-for-byte — if it moved, `PREREG.md` §4
   must be regenerated before anything else.
2. **Edit `calibration.json`**: repair the cal-01 row to match the repaired anchor, rename
   the `scoring` key (PR-01), and reconcile "9 anchors" against the anchor kinds so the
   account in step 3 can be written. Then run
   `contracts.assert_no_scoring_keys` over all four bundle JSON files until clean.
3. **Edit `config.json`**: settle both accounts against the step-2 calibration set (D(2)),
   add an `audit.period` account, set `publish_ref` explicitly, and declare the resource
   conditions PR-10 names. Re-run `LoopConfig.load` and
   `standard.assert_config_matches_standard`.
4. **Edit `obligations.json`**: apply the `p7` and `o5` rewordings (D(1)), the o1/o2
   block-code spelling (PR-12a), the o5 calibration-count reference, and the `12
   juxtapositions` / `eleven` reconciliation (PR-13). Then recompute **both** obligations
   digests — the canonical-body digest that replaces `713119a7…` in
   `obligations.json:296` **and** the file digest that `obligations.pin()` will fold into
   the plan — and carry both forward.
5. **Edit `PREREG.md`** last among the content files, because it quotes everything above:
   §3's obligations pin (both values, per PR-02), the `o5`/`p7`/`p10` clause texts, the
   eleven→twelve inventory, the seat-evidence restatement (PR-10), the publication-branch
   deviation (PR-11), the block-register/`blocked:constitution` reconciliation (PR-12b), the
   Account (E) non-goal sentence (PR-17), the placeholder receipt id (PR-18), **the
   enumerated six values / three marks / difference-kind sets / block codes, and the
   step-1 `STANDARD_BODY_SHA256` written into §4 beside the ceiling digest (PR-25)**.
   Re-assert `standard.CEILING_TEXT in PREREG.md` and both required-sentence sets, and
   assert each newly enumerated list equal to its module constant.
6. **Fix and re-run `validate.py`**: supply `types.PINNED_SOURCE_PATHS` (PR-07), add the
   `assert_no_scoring_keys` sweep, add an assertion that the obligations *file* digest equals
   whatever `obligations.pin()` returns, and add a probe that every
   `standard.CALIBRATION_ANCHORS` entry admits at least one uniquely-resolving quote inside a
   declared span (the test `REVIEW-WAVE1.md` B3 asks for). Require exit 0.
7. **Regenerate `VALIDATION.md` wholesale** from that run — the transcript, the digest table
   for all six files, and a fresh demonstration `loop_plan_id` over the full pin set. Do not
   patch it; a stale line here is how PR-08 happened.
8. **Only then S0 PREREGISTER**, which computes the real `loop_plan_id` over the resolved
   config plus the six `PINNED_SOURCE_PATHS`, `CEILING.md`, the `STD_READING` body, every
   prompt template, `obligations.json`, and each attached study's `PLAN.md` and
   `material.json`, writes `plan.json`, and publishes it before the first call.
9. **Re-verify at S1 PREFLIGHT** that `STANDARD_BODY_SHA256` still equals the step-1 value.
   The hardening agent has moved it at least once during this review; if it moves between
   step 1 and step 8 the plan identity is for a body that no longer exists, and `PLAN_ID_MISMATCH`
   on the next resume is the good outcome. **Freeze `loop-impl/repo/src/minireason/loop/`
   before step 1 and do not accept further edits until step 8 completes.** This is the single
   largest operational risk in the sequence.

---

# E. SHOULD-FIX AND NOTES

**PR-18 — the placeholder receipt id `REC-20260914-Z` is a live, published id.**
`PREREG.md:34`: "**REC-20260914-Z opened at 2026-09-14T00:00:00Z: pre-register the automated
end-to-end harness loop…**". `docs/DECISION_LEDGER.md:1481` already carries
"REC-20260914-Z opened at 2026-09-14 11:14 UTC" for F002 occurrence-03, with outcome,
correction and two dispatch checkpoints at :1483–:1489. The bundle does say the id is a
placeholder (`PREREG.md:22`), and `receipts.open_preregistration` mints the real one under
the lock — but if `PREREG.md` is copied into the run directory as written, the published
record contains a pre-registration paragraph bearing another decision's id. Use an obviously
impossible placeholder (`REC-YYYYMMDD-X`) or the literal `<minted at S0>`.

**PR-19 — §6's predicted stop clause is probably wrong.** `PREREG.md:234-238` predicts
"cycle 3 has nothing new to read … so the mark-triple set is identical to cycle 2's and the
run stops at clause 4, `no_new_reading_changes`." But o1–o4, o6 and o7 are all satisfiable by
recorded *reasons* (blocks, `critic-none`, `unreached`), so they are likely satisfied at the
end of cycle 1; o5 is discharged at cycle 2; and clause 3 ("all *o* satisfied ⇒ STOP
`obligations_discharged`") is evaluated **before** clause 4. The likely stop is clause 3 at
cycle 3, not clause 4. Predicting the wrong clause in the document written "so that it cannot
be narrated as a success afterwards" undercuts the point of writing it. Either restate the
prediction or say both clauses are live and why.

**PR-20 — the C001 leg's outcome is already known offline and should be in §6.**
`WAVE1-INTEGRATION-DECISIONS.md` item 53 reports a program pass over the published
occurrence-02 bytes: all ten program-computed T/D kind-rows G9-forced to `same`, **zero
admissible program `differs`**, E forced unresolved by shared bare tokens on six rows, G
prose-only residue. Consistent with `reading_set.json`'s "-54" expectation, but it means the
contrast leg's shape is largely determined before a call is made. Put it in §6's honest
expectation, so the published C001 columns cannot be read as a finding produced by the run.

**PR-21 — four of the nine calibration rows name anchors the frozen standard does not
carry.** `calibration.json` rows cal-06 (`fabricated-decisive-point`), cal-07
(`duplicated-passage-non-unique-offset`), cal-08 (`order-swap-sensitive-pair`) and cal-09
(`paraphrase-invariant-pair`) have no entry in `standard.CALIBRATION_ANCHORS` (which holds
`self-juxtaposition`, `no-shared-reference`, `quotes-and-rejects`,
`clean-control-lexical-overlap-only`, `clean-control-framing-only-passage`).
`validate.py:141-142` asserts only the *reverse* direction. The four extra anchors are
therefore outside the standard body and so are not reachable by the case-law closure that
`PREREG.md:211` promises ("a successful attack on `std:reading-rubric/v1` … collapses every ν
citing it"). Either add them to the standard body (changing pin #1) or state in `PREREG.md`
that the pinned calibration set extends the standard's anchor kinds and is attacked through
`calibration.json`'s own pin instead.

**PR-22 — `p1`'s `material_sha256` reads like a field name and is a file digest.**
`PREREG.md:150` / `obligations.json` p1: "the H005 occurrence-01 `material_sha256` equals
`24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927`". There is no
`material_sha256` field in `occurrence-01/material.json` (its top-level keys are `schema`,
`system`, `prose_instruction`, `formal_instruction`, `bare_instruction`, `problems`,
`templates`, `source_pins`); the value is the sha256 of the file, which is correct and which
I verified. Say "the sha256 of `.../occurrence-01/material.json`".

**PR-23 — `o7` says four states, `p12` and the ceiling say three.** `PREREG.md:149` ("exactly
one of four printed states") and `PREREG.md:161` / the ceiling ("**Three cell states are
distinct and are printed as three things**"). They are reconcilable — the ceiling's three are
the non-resolved states and the fourth is "a relation or a mark" — but a reader checking p12
against o7 has to work that out. One clause in o7 saying so would fix it.

**PR-24 — `STOP_REASONS` omits the design's `preregistered_condition:<id>`.** Design §4.4's
stop vocabulary includes it; `types.STOP_REASONS` is the seven other tokens. Nothing in this
run needs it and the omission is probably right, but the bundle should note the deviation
rather than leave a later reader to diff the design against the enum.

**PR-25 — the bundle is written against symbol names in a module it neither enumerates nor
pins, so its two declared narrowings cannot be checked from the record.**
Raised by an independent mechanical pass over the same bundle and confirmed here.
`PREREG.md:46` and `PREREG.md:201` both say the run "closes it to six values", and
`PREREG.md:227` says "G4 routes anything outside the six-value vocabulary to
`unresolved:outside-vocabulary`" — but **no file in the bundle lists the six**.
`grep` over `*.md`/`*.json` finds `retains` and `rejects-with-reason` only incidentally,
as ground-truth values inside `calibration.json` rows. The same holds throughout: o1 names
`standard.NOMINABLE_RELATIONS` and `types.BLOCK_CODES`, o2 names `standard.MARKS` and
`standard.DIFFERENCE_KINDS[<register>]`, o4 and o7 name `types.BLOCK_CODES`, and `p12`
names `standard.CEILING_REQUIRED_SENTENCES` — every one a symbol reference into
`loop-impl/repo/src/minireason/loop/`, which is not a bundle file, is under live edit, and
whose `STANDARD_BODY_SHA256` **no bundle file names** (see D(3)).

I verified the values do match — `use_relation_h005.ROOT_READING_VOCABULARY` and
`standard.READING_VOCABULARY` are byte-identical at
`('re-deploys','qualifies','rejects-with-reason','repairs','retains','unresolved')` — so
this is not a disagreement (§A) but an unverifiability. The claim ceiling says the narrowing
"**is part of the claim**"; a claim a later reader cannot check against the record is not
yet part of it. Enumerate the six values, the three marks, the per-register difference-kind
sets and the block-code set in `PREREG.md` (or in a bundle file that `validate.py` asserts
equal to the module constants), and name `STANDARD_BODY_SHA256` in `PREREG.md` §4 beside
the ceiling digest so the symbols resolve to pinned bytes.

**Note — what is strong, and should not be lost in the rewrite.** The `max_calls` derivation
is the best-argued number in the bundle: it derives 11 rather than the design's "roughly
nine" calls per guarded row, states the deviation and its reason ("a split is only observable
if both seats rule"), and declares the audit phase the design left ambiguous
(`audit_schedule_declaration`). `p10`'s two enumerations verify exactly against the published
bytes. The `why_not_a_count` note on every clause is the right discipline and made this audit
possible. §6 refuses in advance to let a thin table read as failure, and `PREREG.md:247`
("Success for this pre-registration is not that any cell filled") is exactly the sentence
ruling 7 and PURPOSE.md want. None of the blockers above touch any of that.

---

# F. VERDICT

**Publishable after fixes PR-01, PR-02, PR-03, PR-04, PR-05, PR-06, PR-07, PR-08, PR-09,
PR-10, PR-11, PR-12 and PR-13, applied in the order set out in D(3), and with PR-14 through
PR-25 addressed or explicitly declined in the published text.**

Nothing in the bundle requires abandoning the design, and no finding is about the
pre-registration reaching for a result. The defects are of three kinds: a document that
would fail its own protected obligation on its first registration (PR-01); pre-registered
text that is not the predicate the program evaluates (PR-02, PR-03, PR-04, PR-05, PR-12);
and a frozen record that does not yet describe the conditions it will run under or the
bundle it sits beside (PR-06, PR-07, PR-08, PR-09, PR-10, PR-11, PR-13). All are fixable
before S0 and all must be, because after S0 every one of them is a new `loop_plan_id`.

Two conditions on the fix window. The rewordings D(1) settles are made *at* pre-registration
review and must be named as such in the published text, not applied silently. And
`loop-impl/repo/src/minireason/loop/` must be frozen from step 1 of D(3) until the plan is
published — the standard body moved once during this review, and a plan identity minted over
a body that has since changed is the one failure this whole apparatus exists to prevent.
